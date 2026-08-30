from __future__ import annotations

import os
import subprocess
import sys
import tarfile
from pathlib import Path
from zipfile import ZipFile

import pytest

_ROOT = Path(__file__).parents[1]
_RUNTIME_FILES = {
    'allegrobridge/assets/api_names.txt',
    'allegrobridge/client/_axl_stubs.pyi',
    'allegrobridge/py.typed',
    'allegrobridge/server/allegro_server.il',
    'allegrobridge/server/extensions/__init__.py',
    'allegrobridge/server/extensions/drc.il',
    'allegrobridge/server/extensions/routes.il',
    'allegrobridge/server/extensions/shapes.il',
    'allegrobridge/server/extensions/vias.il',
    'allegrobridge/_kernel/py.typed',
    'allegrobridge/_kernel/server/python_server.il',
}


@pytest.fixture(scope='module')
def distributions(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, Path]:
    output = tmp_path_factory.mktemp('dist')
    subprocess.run(
        [sys.executable, '-m', 'build', '--no-isolation', '--outdir', output],
        cwd=_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return next(output.glob('*.whl')), next(output.glob('*.tar.gz'))


@pytest.mark.integration
def test_wheel_and_sdist_contain_runtime_files(distributions: tuple[Path, Path]) -> None:
    wheel, sdist = distributions

    with ZipFile(wheel) as archive:
        wheel_files = set(archive.namelist())
    with tarfile.open(sdist, 'r:gz') as archive:
        sdist_files = {'/'.join(Path(name).parts[1:]) for name in archive.getnames()}

    assert wheel_files >= _RUNTIME_FILES
    assert sdist_files >= _RUNTIME_FILES


@pytest.mark.integration
def test_wheel_imports_and_reads_runtime_resources(
    distributions: tuple[Path, Path],
    tmp_path: Path,
) -> None:
    wheel, _ = distributions
    install = tmp_path / 'site-packages'
    subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '--no-deps', '--target', install, wheel],
        capture_output=True,
        text=True,
        check=True,
    )
    script = f"""\
from importlib.resources import files
import allegrobridge
import allegrobridge.server.extensions
import allegrobridge._kernel

assert allegrobridge.__file__.startswith({str(install)!r})
assert allegrobridge.server.extensions.__file__.startswith({str(install)!r})
assert allegrobridge._kernel.__file__.startswith({str(install)!r})
for path in {sorted(_RUNTIME_FILES)!r}:
    package, resource = path.split('/', 1)
    assert files(package).joinpath(resource).is_file()
"""
    env = dict(os.environ)
    env['PYTHONPATH'] = str(install)
    subprocess.run(
        [sys.executable, '-c', script],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
