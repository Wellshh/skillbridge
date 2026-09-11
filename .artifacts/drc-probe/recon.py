# Scratch recon probe for DRC precision investigation (not part of the suite).
from __future__ import annotations

import os

os.environ.setdefault('CDSROOT', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('Sigrity_EDA_DIR', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('CDS_LIC_FILE', '5280@localhost')

from pathlib import Path
from shutil import copy2
from socket import socket
from tempfile import mkdtemp

from allegrobridge import Allegro
from allegrobridge.util import ASSETS_DIR

work = Path(mkdtemp(prefix='drc-probe-recon-'))
board = copy2(ASSETS_DIR / 'route' / 'EL5_MIAN_FPC.brd', work)
os.environ['ALLEGROBRIDGE_LOG_DIRECTORY'] = work.as_posix()
with socket() as listener:
    listener.bind(('localhost', 0))
    port = str(listener.getsockname()[1])

_GETTERS = (
    '(errset (axlGetParam "paramDesign")->designUnits)',
    '(errset (axlGetParam "paramDesign")->accuracy)',
    '(errset (axlDBChangeDesignUnits nil nil))',
    '(errset (axlDBGetDesign (axlDBGetDesign))->bBox)',
)


def main() -> None:
    with Allegro.open(mode='cli', board=board, workspace_id=port, timeout=300.0) as allegro:
        session = allegro.session
        ws = allegro.workspace
        print('BOARD:', session.board(), flush=True)
        markers = session.drc()
        print('DRC_COUNT:', len(markers), flush=True)
        for marker in markers[:6]:
            print('MARKER:', marker.name, '|', marker.category, '|', marker.source,
                  '| expected=', repr(marker.expected), '| actual=', repr(marker.actual),
                  '| layer=', marker.layer, '| loc=', marker.location, flush=True)
            for figure in marker.figures:
                print('   FIGURE:', figure, flush=True)
        by_category: dict[str, int] = {}
        for marker in markers:
            key = marker.category + '/' + marker.name
            by_category[key] = by_category.get(key, 0) + 1
        print('CATEGORIES:', sorted(by_category.items()), flush=True)
        spacing = [m for m in markers if 'space' in (m.category + m.name).lower()]
        print('SPACING_COUNT:', len(spacing), flush=True)
        for marker in spacing[:8]:
            print('SPACING:', marker.name, '| expected=', repr(marker.expected),
                  '| actual=', repr(marker.actual), '| source=', marker.source,
                  '| layer=', marker.layer, flush=True)
            for figure in marker.figures:
                print('   FIGURE:', figure, flush=True)
        for expr in _GETTERS:
            try:
                print('EXPR:', expr, '=>', ws['evalstring'](expr), flush=True)
            except Exception as error:
                print('EXPR:', expr, 'RAISED', type(error).__name__, str(error)[:160],
                      flush=True)


if __name__ == '__main__':
    main()
