# Scratch epsilon-ladder probe: how does Allegro's DRC compare spacing to the
# rule near the threshold?  Disposable board copy, owned Allegro process.
# Isolated new etch gets NO net assignment (documented, probe-verified), so each
# test line starts on a net-assigned via; cross-net pairs make the net spacing
# rule (Line to Line Spacing) fire and let drc.check(route) find the target.
from __future__ import annotations

import os

os.environ.setdefault('CDSROOT', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('Sigrity_EDA_DIR', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('CDS_LIC_FILE', '5280@localhost')

from collections import Counter
from pathlib import Path
from shutil import copy2
from socket import socket
from tempfile import mkdtemp

from allegrobridge import Allegro
from allegrobridge.util import ASSETS_DIR

NET_A = 'NFC_SWP'
NET_B = 'FINGER_SPI_MISO'
LAYER = 'ETCH/TOP'
WIDTH = 0.15          # mm
LENGTH = 2.0          # mm
X0, Y0 = 300.0, 300.0 # far outside the board outline; empty region
LINE_SPACING_NAME = 'line to line spacing'

# Stage-2 deltas from the rule R (edge spacing = R + delta), mm.
DELTAS = [0.02, 0.005, 0.002, 0.001, 5e-4, 1e-4, 5e-5, 1e-6, 1e-9,
          0.0,
          -1e-9, -1e-6, -5e-5, -1e-4, -5e-4, -1e-3, -1.5e-3, -2e-3, -5e-3, -0.02]


def _quantity(text: str) -> float:
    """Parse Allegro's pre-formatted '0.15 MM' quantity strings."""
    return float(text.split()[0])


def _is_line_spacing(marker) -> bool:
    return marker.name.lower() == LINE_SPACING_NAME


def _make_pair(session, y_a: float, y_b: float, padstack: str):
    """Two horizontal lines, each anchored on its own net-assigned via."""
    session.vias.create(padstack, at=(X0, y_a), net=NET_A)
    session.vias.create(padstack, at=(X0 + LENGTH, y_b), net=NET_B)
    a = session.routes.create(NET_A, [(X0, y_a), (X0 + LENGTH, y_a)], LAYER, WIDTH)
    b = session.routes.create(NET_B, [(X0, y_b), (X0 + LENGTH, y_b)], LAYER, WIDTH)
    return a, b


def _report(tag: str, ra, rb, markers) -> list:
    spacing = [m for m in markers if _is_line_spacing(m)]
    other = [m for m in markers if not _is_line_spacing(m)]
    verdict = 'FLAGGED' if spacing else 'clean'
    actual = repr(spacing[0].actual) if spacing else ''
    expected = repr(spacing[0].expected) if spacing else ''
    print(f'{tag}: {verdict} expected={expected} actual={actual}', flush=True)
    print(f'   net_a={ra.net!r} net_b={rb.net!r}', flush=True)
    print(f'   committed_a: ({ra.start.x!r},{ra.start.y!r})->({ra.end.x!r},{ra.end.y!r}) w={ra.width!r}',
          flush=True)
    print(f'   committed_b: ({rb.start.x!r},{rb.start.y!r})->({rb.end.x!r},{rb.end.y!r}) w={rb.width!r}',
          flush=True)
    y_a = (ra.start.y + ra.end.y) / 2.0
    y_b = (rb.start.y + rb.end.y) / 2.0
    w_a = (ra.width.x + ra.width.y) / 2.0 if hasattr(ra.width, 'x') else float(ra.width)
    w_b = (rb.width.x + rb.width.y) / 2.0 if hasattr(rb.width, 'x') else float(rb.width)
    edge = abs(y_b - y_a) - (w_a + w_b) / 2.0
    print(f'   python_edge={edge!r} rounded4={round(edge, 4)!r}', flush=True)
    if spacing:
        for figure in spacing[0].figures:
            print('   FIGURE:', figure.obj_type, figure.layer, 'net=', figure.net,
                  'start=', figure.start, 'end=', figure.end, 'w=', figure.width,
                  flush=True)
    for marker in other:
        print('   OTHER:', marker.category, '|', marker.name,
              '| expected=', repr(marker.expected), '| actual=', repr(marker.actual),
              flush=True)
    return spacing


def main() -> None:
    work = Path(mkdtemp(prefix='drc-probe-ladder-'))
    board = copy2(ASSETS_DIR / 'route' / 'EL5_MIAN_FPC.brd', work)
    os.environ['ALLEGROBRIDGE_LOG_DIRECTORY'] = work.as_posix()
    with socket() as listener:
        listener.bind(('localhost', 0))
        port = str(listener.getsockname()[1])

    with Allegro.open(mode='cli', board=board, workspace_id=port, timeout=300.0) as allegro:
        session = allegro.session
        drc = session.drc

        existing = session.vias()
        padstacks = Counter(v.padstack for v in existing)
        print('EXISTING_VIAS:', len(existing), 'PADSTACKS:', padstacks.most_common(5),
              flush=True)
        padstack = padstacks.most_common(1)[0][0]

        # --- grid probe: fractional coords reveal DB grid rounding on commit
        g = session.routes.create(
            NET_A, [(X0, Y0 + 80.0), (X0 + 1.23456789, Y0 + 80.0004567)], LAYER, WIDTH)
        print('GRID_PROBE committed:',
              f'({g[0].start.x!r},{g[0].start.y!r})->({g[0].end.x!r},{g[0].end.y!r})',
              'net=', repr(g[0].net), 'w=', repr(g[0].width), flush=True)

        # --- stage 1: tight cross-net pair (edge 0.01 mm) to learn the rule R
        rows_a, rows_b = _make_pair(session, Y0, Y0 + 0.01 + WIDTH, padstack)
        ra, rb = rows_a[0], rows_b[0]
        spacing = _report('STAGE1', ra, rb, drc.check(ra))
        if not spacing:
            print('STAGE1: no line-to-line spacing marker - aborting ladder', flush=True)
            return
        rule = _quantity(spacing[0].expected)
        print('RULE_R:', repr(rule), flush=True)

        # --- stage 2: ladder of pairs straddling R, each 4 mm apart vertically
        base_y = Y0 + 5.0
        for index, delta in enumerate(DELTAS):
            y_a = base_y + index * 4.0
            y_b = y_a + rule + delta + WIDTH
            rows_a, rows_b = _make_pair(session, y_a, y_b, padstack)
            _report(f'LADDER delta={delta!r} target_t={rule + delta!r}',
                    rows_a[0], rows_b[0], drc.check(rows_a[0]))

        print('TOTAL_MARKERS:', len(drc()), flush=True)


if __name__ == '__main__':
    main()
