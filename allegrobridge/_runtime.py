# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
from __future__ import annotations

import logging
import socket
from pathlib import Path
from subprocess import Popen, TimeoutExpired
from tempfile import TemporaryDirectory
from time import monotonic, sleep

import psutil

from .exceptions import AllegroLaunchError, AllegroTimeoutError

_LOG = logging.getLogger(__name__)
_POLL_INTERVAL = 0.1
_PROCESS_EXIT_TIMEOUT = 5.0


class CliRuntime:
    def __init__(self, *, endpoint: int | None = None) -> None:
        self.endpoint = endpoint
        self.temp_dir = TemporaryDirectory(prefix='allegrobridge-')
        self.script_path = Path(self.temp_dir.name) / 'startup.scr'
        self._process: Popen[bytes] | None = None
        self._root_process: psutil.Process | None = None
        self._known_processes: dict[int, psutil.Process] = {}
        self._closed = False

    @property
    def process(self) -> Popen[bytes]:
        if self._process is None:
            raise AllegroLaunchError('Allegro process has not been started')
        return self._process

    def start(self, command: list[str], script: str) -> None:
        if self.endpoint is not None:
            self._check_endpoint_available()
        self.script_path.write_text(script, encoding='utf-8')
        command = [*command, '-s', self.script_path.as_posix()]
        self._process = Popen(  # ruff: ignore[subprocess-without-shell-equals-true]
            command,
            shell=False,
        )
        self._root_process = psutil.Process(self._process.pid)
        self._discover_descendants()

    def poll(self) -> int | None:
        self._discover_descendants()
        return self.process.poll()

    def close(self, *, wait_for_endpoint: bool = True) -> None:
        if self._closed:
            return
        errors: list[BaseException] = []
        try:
            try:
                self._stop_processes()
            except Exception as cleanup_error:  # ruff: ignore[blind-except]
                errors.append(cleanup_error)
            if wait_for_endpoint and self.endpoint is not None and self._process is not None:
                try:
                    self._wait_for_endpoint_release()
                except Exception as cleanup_error:  # ruff: ignore[blind-except]
                    errors.append(cleanup_error)
        finally:
            try:
                self.temp_dir.cleanup()
            except Exception as cleanup_error:  # ruff: ignore[blind-except]
                errors.append(cleanup_error)
        if errors:
            for additional_error in errors[1:]:
                _LOG.error('Additional runtime cleanup failure', exc_info=additional_error)
            raise errors[0]
        self._closed = True

    def _check_endpoint_available(self) -> None:
        assert self.endpoint is not None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            try:
                probe.bind(('localhost', self.endpoint))
            except OSError as error:
                raise AllegroLaunchError(
                    f'Allegro server port {self.endpoint} is already in use'
                ) from error

    def _discover_descendants(self) -> None:
        if self._remember_root_descendants():
            return
        root_pid = self._process.pid if self._process is not None else None
        if root_pid is None:
            return
        children: dict[int, list[psutil.Process]] = {}
        for process in psutil.process_iter(['pid', 'ppid']):
            parent_pid = self._parent_pid(process)
            if parent_pid is not None:
                children.setdefault(parent_pid, []).append(process)
        pending = [root_pid]
        while pending:
            parent_pid = pending.pop()
            for process in children.get(parent_pid, []):
                self._known_processes.setdefault(process.pid, process)
                pending.append(process.pid)

    def _remember_root_descendants(self) -> bool:
        if self._root_process is None:
            return False
        try:
            descendants = self._root_process.children(recursive=True)
        except psutil.NoSuchProcess:
            return False
        except psutil.AccessDenied as error:
            raise AllegroLaunchError(
                f'Access denied while inspecting process {error.pid}'
            ) from error
        for process in descendants:
            self._known_processes.setdefault(process.pid, process)
        return True

    @staticmethod
    def _parent_pid(process: psutil.Process) -> int | None:
        try:
            return process.ppid()
        except psutil.NoSuchProcess:
            return None
        except psutil.AccessDenied as error:
            raise AllegroLaunchError(
                f'Access denied while inspecting process {error.pid}'
            ) from error

    def _stop_processes(self) -> None:
        discovery_error: AllegroLaunchError | None = None
        try:
            self._discover_descendants()
        except AllegroLaunchError as error:
            discovery_error = error
        targets, denied = self._terminate_descendants()
        alive = self._wait_and_kill(targets, denied)
        root_error: Exception | None = None
        try:
            self._stop_root()
        except Exception as error:  # ruff: ignore[blind-except]
            root_error = error
        if alive:
            if root_error is not None:
                _LOG.error('Root process cleanup also failed', exc_info=root_error)
            raise AllegroTimeoutError(
                'Allegro descendant processes did not exit: '
                + ', '.join(str(process.pid) for process in alive)
            )
        if denied:
            if root_error is not None:
                _LOG.error('Root process cleanup also failed', exc_info=root_error)
            raise AllegroLaunchError(
                'Access denied while stopping Allegro descendant processes: '
                + ', '.join(str(pid) for pid in denied)
            )
        if discovery_error is not None:
            if root_error is not None:
                _LOG.error('Root process cleanup also failed', exc_info=root_error)
            raise discovery_error
        if root_error is not None:
            raise root_error

    def _terminate_descendants(self) -> tuple[list[psutil.Process], list[int]]:
        targets: list[psutil.Process] = []
        denied: list[int] = []
        for process in self._known_processes.values():
            outcome = CliRuntime._signal_process(process, kill=False)
            if outcome == 'signaled':
                targets.append(process)
            elif outcome == 'denied':
                denied.append(process.pid)
        return targets, denied

    @staticmethod
    def _wait_and_kill(targets: list[psutil.Process], denied: list[int]) -> list[psutil.Process]:
        if not targets:
            return []
        _, alive = psutil.wait_procs(targets, timeout=_PROCESS_EXIT_TIMEOUT)
        retry: list[psutil.Process] = []
        for process in alive:
            outcome = CliRuntime._signal_process(process, kill=True)
            if outcome == 'denied':
                denied.append(process.pid)
            elif outcome == 'signaled':
                retry.append(process)
        if retry:
            _, retry = psutil.wait_procs(retry, timeout=_PROCESS_EXIT_TIMEOUT)
        return retry

    @staticmethod
    def _signal_process(process: psutil.Process, *, kill: bool) -> str:
        try:
            process.kill() if kill else process.terminate()
        except psutil.NoSuchProcess:
            return 'gone'
        except psutil.AccessDenied:
            return 'denied'
        return 'signaled'

    def _stop_root(self) -> None:
        process = self._process
        if process is None:
            return
        if process.poll() is not None:
            process.wait(timeout=_PROCESS_EXIT_TIMEOUT)
            return
        process.terminate()
        try:
            process.wait(timeout=_PROCESS_EXIT_TIMEOUT)
        except TimeoutExpired:
            process.kill()
            process.wait(timeout=_PROCESS_EXIT_TIMEOUT)

    def _wait_for_endpoint_release(self) -> None:
        assert self.endpoint is not None
        deadline = monotonic() + _PROCESS_EXIT_TIMEOUT
        while self._endpoint_is_listening():
            if monotonic() >= deadline:
                detail = self._listener_detail()
                raise AllegroTimeoutError(
                    f'Allegro server port {self.endpoint} was not released{detail}'
                )
            sleep(_POLL_INTERVAL)

    def _endpoint_is_listening(self) -> bool:
        assert self.endpoint is not None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.settimeout(_POLL_INTERVAL)
            return probe.connect_ex(('localhost', self.endpoint)) == 0

    def _listener_detail(self) -> str:
        assert self.endpoint is not None
        try:
            connections = psutil.net_connections(kind='tcp')
        except psutil.Error:
            return ' (listener details unavailable)'
        for connection in connections:
            if (
                connection.status == psutil.CONN_LISTEN
                and connection.laddr
                and connection.laddr.port == self.endpoint
            ):
                if connection.pid is None:
                    return ' (listener PID unavailable)'
                try:
                    command = psutil.Process(connection.pid).cmdline()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    command = []
                suffix = f': {command!r}' if command else ''
                return f' (listener PID {connection.pid}{suffix})'
        return ''
