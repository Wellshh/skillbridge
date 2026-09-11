# diag_y700.py - why did vias.create at (300.0, 700.0) fail with
# VIA_CREATE_FAILED: "VIA_ALL_0103" in probe_c run b2gigon2b?
#
# Phase 6 anchors at x=300, y=390..680 all created OK in the same run, so the
# failure is position-dependent.  This diagnostic:
#   1) inventories pre-existing objects (vias/pins/components/shapes/routes)
#      around the probe region on a FRESH disposable board copy;
#   2) attempts via creation at candidate positions to map the blocked region.
#
# Owned headless Allegro, unique port, disposable copy.  No production changes.
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
XMIN, XMAX = 288.0, 314.0
YMIN, YMAX = 580.0, 800.0


def _loc(obj):
    p = getattr(obj, 'location', None)
    if p is None:
        return None
    return (float(p.x), float(p.y))


def _in(pt, xmin=XMIN, xmax=XMAX, ymin=YMIN, ymax=YMAX):
    return pt is not None and xmin <= pt[0] <= xmax and ymin <= pt[1] <= ymax


def seg_in(row):
    try:
        s = (float(row.start.x), float(row.start.y))
        e = (float(row.end.x), float(row.end.y))
    except Exception:
        return False
    return _in(s) or _in(e)


def bbox_coords(bb):
    """Best-effort (x0, y0, x1, y1) from an unknown BBox shape."""
    for a, b in (('min', 'max'), ('lower_left', 'upper_right')):
        lo, hi = getattr(bb, a, None), getattr(bb, b, None)
        if lo is not None and hi is not None:
            try:
                return (float(lo.x), float(lo.y), float(hi.x), float(hi.y))
            except Exception:
                pass
    try:
        return (float(bb[0]), float(bb[1]), float(bb[2]), float(bb[3]))
    except Exception:
        return None


def main() -> None:
    work = Path(mkdtemp(prefix='drc-diag-y700-'))
    board = copy2(ASSETS_DIR / 'route' / 'EL5_MIAN_FPC.brd', work)
    os.environ['ALLEGROBRIDGE_LOG_DIRECTORY'] = work.as_posix()
    with socket() as listener:
        listener.bind(('localhost', 0))
        port = str(listener.getsockname()[1])

    with Allegro.open(mode='cli', board=board, workspace_id=port,
                      timeout=300.0) as allegro:
        session = allegro.session
        all_vias = session.vias()
        padstack = Counter(v.padstack for v in all_vias).most_common(1)[0][0]
        print('PADSTACK:', padstack, flush=True)

        print(f'--- inventory x[{XMIN},{XMAX}] y[{YMIN},{YMAX}] ---', flush=True)
        hits = [(v, _loc(v)) for v in all_vias]
        hits = [(v, p) for v, p in hits if _in(p)]
        print(f'VIAS in region: {len(hits)} / {len(all_vias)}', flush=True)
        for v, p in hits[:80]:
            print(f'   VIA net={v.net!r} padstack={v.padstack!r} '
                  f'at=({p[0]!r},{p[1]!r})', flush=True)

        pins = session.pins()
        ph = [(n, _loc(n)) for n in pins]
        ph = [(n, p) for n, p in ph if _in(p)]
        print(f'PINS in region: {len(ph)} / {len(pins)}', flush=True)
        for n, p in ph[:120]:
            print(f'   PIN refdes={n.refdes!r} num={n.number!r} net={n.net!r} '
                  f'pad={n.padstack!r} at=({p[0]!r},{p[1]!r})', flush=True)

        comps = session.components()
        ch = [(c, _loc(c)) for c in comps]
        ch = [(c, p) for c, p in ch
              if p is not None and XMIN - 8 <= p[0] <= XMAX + 8
              and YMIN - 8 <= p[1] <= YMAX + 8]
        print(f'COMPONENTS near region: {len(ch)} / {len(comps)}', flush=True)
        for c, p in ch[:60]:
            ident = getattr(c, 'refdes', None) or getattr(c, 'name', '?')
            print(f'   COMP {ident!r} at=({p[0]!r},{p[1]!r})', flush=True)

        shapes = session.shapes()
        sh = []
        for s in shapes:
            b = bbox_coords(getattr(s, 'bbox', None))
            if b is None:
                continue
            if b[2] >= XMIN and b[0] <= XMAX and b[3] >= YMIN and b[1] <= YMAX:
                sh.append((s, b))
        print(f'SHAPES overlapping region: {len(sh)} / {len(shapes)}',
              flush=True)
        for s, b in sh[:40]:
            print(f'   SHAPE net={s.net!r} layer={s.layer!r} '
                  f'dyn={s.dynamic!r} bbox={b!r}', flush=True)

        routes = session.routes()
        rh = [r for r in routes if seg_in(r)]
        print(f'ROUTE segments in region: {len(rh)} / {len(routes)}',
              flush=True)
        for r in rh[:120]:
            print(f'   ROUTE net={r.net!r} layer={r.layer!r} '
                  f'type={r.obj_type!r} '
                  f'start=({float(r.start.x)!r},{float(r.start.y)!r}) '
                  f'end=({float(r.end.x)!r},{float(r.end.y)!r})', flush=True)

        print('--- creation trials (fresh copy, net=NET_A) ---', flush=True)
        trials = [(300.0, y) for y in (685.0, 690.0, 695.0, 698.0, 700.0,
                                       702.0, 705.0, 710.0, 720.0, 730.0,
                                       740.0, 750.0)]
        trials += [(x, 700.0) for x in (292.0, 296.0, 298.0, 302.0, 304.0,
                                        308.0)]
        trials += [(300.0, y) for y in (480.0, 500.0, 520.0, 540.0, 560.0)]
        for x, y in trials:
            try:
                session.vias.create(padstack, at=(x, y), net=NET_A)
                print(f'CREATE ({x!r},{y!r}) OK', flush=True)
            except Exception as exc:
                print(f'CREATE ({x!r},{y!r}) FAILED {str(exc)[:180]}',
                      flush=True)
        print('DIAG_DONE', flush=True)


if __name__ == '__main__':
    main()
