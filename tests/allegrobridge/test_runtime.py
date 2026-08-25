from __future__ import annotations

import socket
import subprocess
import sys
from contextlib import suppress
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import psutil
import pytest

from allegrobridge._runtime import CliRuntime  # ruff: ignore[import-private-name]
from allegrobridge.exceptions import AllegroLaunchError

_PYTHON = getattr(sys, '_base_executable', None) or sys.executable


def test_start_rejects_occupied_endpoint_before_popen(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with socket.socket() as listener:
        listener.bind(('localhost', 0))
        listener.listen()
        port = listener.getsockname()[1]
        popen = Mock()
        monkeypatch.setattr('allegrobridge._runtime.Popen', popen)

        runtime = CliRuntime(endpoint=port)
        with pytest.raises(RuntimeError, match=f'port {port} is already in use'):
            runtime.start(['allegro.exe'], 'exit\n')

        popen.assert_not_called()


def test_start_owns_script_until_close(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    process = Mock(pid=123, poll=Mock(return_value=None))
    monkeypatch.setattr('allegrobridge._runtime.Popen', Mock(return_value=process))
    root = Mock()
    root.children.return_value = []
    monkeypatch.setattr('allegrobridge._runtime.psutil.Process', Mock(return_value=root))
    runtime = CliRuntime()

    runtime.start(['allegro.exe'], 'skill hi\n')
    script_path = runtime.script_path

    assert script_path.read_text(encoding='utf-8') == 'skill hi\n'
    monkeypatch.setattr(runtime, '_stop_processes', Mock())
    runtime.close()
    assert not script_path.exists()


def test_close_retries_after_endpoint_release_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = CliRuntime(endpoint=7788)
    runtime._process = Mock()
    stop = Mock()
    wait = Mock(side_effect=[TimeoutError('busy'), None])
    monkeypatch.setattr(runtime, '_stop_processes', stop)
    monkeypatch.setattr(runtime, '_wait_for_endpoint_release', wait)

    with pytest.raises(TimeoutError, match='busy'):
        runtime.close()
    runtime.close()

    assert stop.call_count == 2
    assert wait.call_count == 2


def test_close_skips_endpoint_wait_when_process_never_started(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = CliRuntime(endpoint=7788)
    stop = Mock()
    wait = Mock()
    monkeypatch.setattr(runtime, '_stop_processes', stop)
    monkeypatch.setattr(runtime, '_wait_for_endpoint_release', wait)

    runtime.close()

    stop.assert_called_once_with()
    wait.assert_not_called()


def test_stop_processes_kills_wait_procs_survivors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    child = Mock(pid=12)
    process = Mock(pid=11, poll=Mock(return_value=None))
    process.wait.return_value = 0
    runtime = CliRuntime()
    runtime._process = process
    runtime._known_processes = {12: child}
    monkeypatch.setattr(runtime, '_discover_descendants', Mock())
    monkeypatch.setattr(
        'allegrobridge._runtime.psutil.wait_procs',
        Mock(side_effect=[([], [child]), ([child], [])]),
    )

    runtime._stop_processes()

    child.terminate.assert_called_once_with()
    child.kill.assert_called_once_with()
    process.terminate.assert_called_once_with()
    process.wait.assert_called_once()


def test_stop_processes_reports_survivors_after_two_waits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    child = Mock(pid=12)
    process = Mock(pid=11, poll=Mock(return_value=None))
    process.wait.return_value = 0
    runtime = CliRuntime()
    runtime._process = process
    runtime._known_processes = {12: child}
    monkeypatch.setattr(runtime, '_discover_descendants', Mock())
    monkeypatch.setattr(
        'allegrobridge._runtime.psutil.wait_procs',
        Mock(side_effect=[([], [child]), ([], [child])]),
    )

    with pytest.raises(TimeoutError, match='12'):
        runtime._stop_processes()
    process.terminate.assert_called_once_with()


def test_stop_processes_treats_no_such_process_as_gone(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    child = Mock(pid=12)
    child.terminate.side_effect = psutil.NoSuchProcess(12)
    runtime = CliRuntime()
    runtime._known_processes = {12: child}
    monkeypatch.setattr(runtime, '_discover_descendants', Mock())
    wait_procs = Mock(return_value=([], []))
    monkeypatch.setattr('allegrobridge._runtime.psutil.wait_procs', wait_procs)

    runtime._stop_processes()

    wait_procs.assert_not_called()


def test_stop_processes_reports_access_denied(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    child = Mock(pid=12)
    child.terminate.side_effect = psutil.AccessDenied(12)
    runtime = CliRuntime()
    runtime._known_processes = {12: child}
    monkeypatch.setattr(runtime, '_discover_descendants', Mock())

    with pytest.raises(RuntimeError, match=r'Access denied.*12'):
        runtime._stop_processes()


def test_stop_processes_still_reaps_root_when_discovery_is_denied(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    process = Mock(pid=11, poll=Mock(return_value=None))
    process.wait.return_value = 0
    runtime = CliRuntime()
    runtime._process = process
    monkeypatch.setattr(
        runtime,
        '_discover_descendants',
        Mock(side_effect=AllegroLaunchError('Access denied while inspecting process 11')),
    )

    with pytest.raises(RuntimeError, match=r'Access denied.*11'):
        runtime._stop_processes()

    process.terminate.assert_called_once_with()


def test_discovery_uses_current_ppid_graph_after_root_exits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = Mock()
    root.children.side_effect = psutil.NoSuchProcess(11)
    child = Mock(pid=12, ppid=Mock(return_value=11))
    grandchild = Mock(pid=13, ppid=Mock(return_value=12))
    runtime = CliRuntime()
    runtime._process = Mock(pid=11)
    runtime._root_process = root
    monkeypatch.setattr(
        'allegrobridge._runtime.psutil.process_iter',
        Mock(return_value=[child, grandchild]),
    )

    runtime._discover_descendants()

    assert runtime._known_processes == {12: child, 13: grandchild}


def test_discovery_preserves_saved_process_identity() -> None:
    saved = Mock(pid=12)
    replacement = Mock(pid=12)
    root = Mock()
    root.children.return_value = [replacement]
    runtime = CliRuntime()
    runtime._root_process = root
    runtime._known_processes = {12: saved}

    runtime._discover_descendants()

    assert runtime._known_processes[12] is saved


def test_close_always_removes_temporary_directory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = CliRuntime()
    path = Path(runtime.temp_dir.name)
    monkeypatch.setattr(runtime, '_stop_processes', Mock(side_effect=RuntimeError('stop')))

    with pytest.raises(RuntimeError, match='stop'):
        runtime.close()

    assert not path.exists()


def test_endpoint_timeout_reports_listener_without_killing_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runtime = CliRuntime(endpoint=7788)
    listener = SimpleNamespace(
        status=psutil.CONN_LISTEN,
        laddr=SimpleNamespace(port=7788),
        pid=42,
    )
    process = Mock()
    process.cmdline.return_value = ['python_server.exe']
    monkeypatch.setattr(runtime, '_endpoint_is_listening', Mock(return_value=True))
    monkeypatch.setattr('allegrobridge._runtime.monotonic', Mock(side_effect=[0.0, 6.0]))
    monkeypatch.setattr(
        'allegrobridge._runtime.psutil.net_connections', Mock(return_value=[listener])
    )
    monkeypatch.setattr('allegrobridge._runtime.psutil.Process', Mock(return_value=process))

    with pytest.raises(TimeoutError, match=r'7788.*PID 42.*python_server'):
        runtime._wait_for_endpoint_release()

    process.kill.assert_not_called()


@pytest.mark.skipif(sys.platform != 'win32', reason='Windows process lifecycle')
def test_close_waits_until_recursive_descendants_exit() -> None:
    parent_script = (
        'import subprocess, sys, time\n'
        f'child = subprocess.Popen([{_PYTHON!r}, "-c", "import time; time.sleep(60)"])\n'
        'print(child.pid, flush=True)\n'
        'time.sleep(60)\n'
    )
    parent = subprocess.Popen(
        [_PYTHON, '-c', parent_script],
        stdout=subprocess.PIPE,
        text=True,
    )
    runtime = CliRuntime()
    runtime._process = parent
    runtime._root_process = psutil.Process(parent.pid)
    child_pid = int(parent.stdout.readline())
    try:
        runtime._discover_descendants()
        runtime.close()
        assert parent.poll() is not None
        assert not psutil.pid_exists(child_pid)
    finally:
        for pid in (child_pid, parent.pid):
            with suppress(psutil.NoSuchProcess):
                psutil.Process(pid).kill()


@pytest.mark.skipif(sys.platform != 'win32', reason='Windows process lifecycle')
def test_close_uses_saved_identity_after_parent_exits() -> None:
    parent_script = (
        'import subprocess, sys\n'
        f'child = subprocess.Popen([{_PYTHON!r}, "-c", "import time; time.sleep(60)"])\n'
        'print(child.pid, flush=True)\n'
        'sys.stdin.buffer.read(1)\n'
    )
    parent = subprocess.Popen(
        [_PYTHON, '-c', parent_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    runtime = CliRuntime()
    runtime._process = parent
    runtime._root_process = psutil.Process(parent.pid)
    child_pid = int(parent.stdout.readline())
    try:
        runtime._discover_descendants()
        parent.stdin.close()
        parent.wait(timeout=5)
        runtime.close()
        assert not psutil.pid_exists(child_pid)
    finally:
        for pid in (child_pid, parent.pid):
            with suppress(psutil.NoSuchProcess):
                psutil.Process(pid).kill()
