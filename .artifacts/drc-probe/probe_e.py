# Probe E: DRC marker-set semantics across the P0 chain (extends Probe D).
# Probe D compared marker COUNTS only (129 == 129); it never compared the
# marker SET.  This probe closes that gap and produces byte-level save controls
# for the parallel raw-file line:
#   E1  marker-set bit identity across save/reopen (S1_PRE -> S1_POST ->
#       S2_PERSISTED): are persisted markers verbatim (bit-exact keys) or
#       re-derived (float noise, display-equivalent)?
#   E2  update idempotence (update x2) + persisted-vs-regenerated set equality.
#   E3  targeted drc.check global side effects: full-set diff around each
#       targeted check, in-session (S1, live markers) and post-reopen (S2,
#       persisted markers).
#   E4  delete/recreate marker attribution: which markers vanish at delete
#       (multiset diff + figure attribution to the deleted cell) and are the
#       recreated markers bit-identical?
#   E5  save determinism controls: fe_F1a/fe_F1 = two zero-op saves in one
#       session; fe_F2b = reopened state saved BEFORE any update; fe_F2 =
#       post-update; fe_F3 = second-generation reopen+save.  Byte-diff tables
#       written to logs/probe_e.fdiff.*.txt for the raw-file line (they decode,
#       we only hash/compare).
#   E6  (optional, gated on bit-clean set identity) waiver round-trip via raw
#       axlDRCWaive: waive -> waived count -> set diff -> unwaive.  Single
#       attempt; any failure -> NOT_TESTED (no retry, per probe discipline).
#
# Marker identity key (dbid-free): (name, category, source, layer, expected,
# actual, location bits, bbox bits, sorted object refs, sorted figure keys) --
# every float through orc.bits.  Comparison is two-tier: Tier-1 strict
# multiset (Counter); Tier-2 (only on mismatch) coarse-key pairing
# (name/category/layer/trunc4-location/objects) with per-field diff reporting
# to distinguish "verbatim persistence" from "re-derived + display-equal".
#
# Reuses probe_d (pd) harness: open_verified/wait_ready/sha256, snap/snap_compare,
# check_cell/verdict_snapshot/verdict_compare, plan_cell/create_pair, TRACK and
# RESULTS module dicts, _sync_state/_summary.  probe_d.py stays frozen (it is
# the committed run5 evidence script); this file duplicates its phase flows
# with mset snapshot points inserted.
from __future__ import annotations

import os

os.environ.setdefault('CDSROOT', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('Sigrity_EDA_DIR', r'D:\Cadence\Cadence_SPB_17.2-2016')
os.environ.setdefault('CDS_LIC_FILE', '5280@localhost')

import pickle
import subprocess
import sys
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
from shutil import copy2
from tempfile import mkdtemp

import arc_oracle as orc
import probe_c as pc
import probe_d as pd
from scan_window import CX_NAT, CY_OFF, EX, SX
from allegrobridge.client.api.geometry import ArcTo, BBox, Point
from allegrobridge.util import ASSETS_DIR

HERE = Path(__file__).resolve().parent
LOGS = HERE / 'logs'


def _pid_alive_safe(pid: int) -> bool:
    """Encoding-safe tasklist probe (monkey-patched over pd._pid_alive):
    localized tasklist output (GBK on this host) can crash utf-8 text-mode
    decoding inside subprocess reader threads, yielding stdout=None."""
    try:
        p = subprocess.run(['tasklist', '/FI', f'PID eq {pid}'],
                           capture_output=True)
        raw = p.stdout or b''
        out = raw.decode('utf-8', 'ignore') + raw.decode('gbk', 'ignore')
    except Exception:
        return False
    return str(pid) in out


pd._pid_alive = _pid_alive_safe   # probe_d functions resolve it at call time

# positional field names of the marker key tuple (diagnostics only)
KEY_FIELDS = ('name', 'category', 'source', 'layer', 'expected', 'actual',
              'location', 'bbox_ll', 'bbox_ur', 'objects', 'figures')


# --------------------------------------------------------------------------
# marker-set canonicalization
# --------------------------------------------------------------------------

def _bitsf(v) -> str:
    return '' if v is None else orc.bits(float(v))


def _pt(v):
    """Point -> (bits, bits); None -> ('', '')."""
    if v is None:
        return ('', '')
    return (_bitsf(v[0]), _bitsf(v[1]))


def _obj_key(o):
    return (getattr(o, 'kind', ''), getattr(o, 'refdes', None),
            getattr(o, 'name', None), getattr(o, 'number', None))


def _ref_key(r):
    return '' if r is None else (getattr(r, 'kind', ''),
                                 getattr(r, 'refdes', None),
                                 getattr(r, 'name', None),
                                 getattr(r, 'number', None))


def _fig_key(f):
    return (f.obj_type or '', f.layer or '',
            (f.net.name if f.net is not None else ''),
            _pt(getattr(f, 'location', None)), _pt(f.start), _pt(f.end),
            _pt(f.center), _bitsf(f.radius), _bitsf(f.width),
            '' if f.is_clockwise is None else bool(f.is_clockwise),
            _ref_key(f.reference))


def _marker_key(m):
    objs = tuple(sorted(_obj_key(o) for o in (m.objects or [])))
    figs = tuple(sorted(_fig_key(f) for f in (m.figures or [])))
    return (m.name, m.category, m.source, m.layer, m.expected, m.actual,
            _pt(m.location), _pt(m.bbox[0] if m.bbox is not None else None),
            _pt(m.bbox[1] if m.bbox is not None else None), objs, figs)


def _coarse_key(full):
    """Coarse pairing key: name/category/layer + trunc4 location + objects
    (float-free, display-level identity)."""
    loc = full[6]
    trunc = tuple('' if b == '' else ('%.4f' % _bits_to_float(b))
                  for b in loc)
    return (full[0], full[1], full[3], trunc, full[9])


def _bits_to_float(bits: str) -> float:
    import struct
    return struct.unpack('>d', bytes.fromhex(bits))[0]


def mset(session, stage: str) -> dict:
    """Full projected marker multiset snapshot (picklable plain structures)."""
    rows = session.drc()
    ordered = []
    pairs = []
    for m in rows:
        fk = _marker_key(m)
        ordered.append(fk)
        pairs.append((fk, _coarse_key(fk)))
    counter = Counter(ordered)
    hist = Counter(k[0] for k in ordered)
    top = ', '.join(f'{n}x{k!r}' for k, n in hist.most_common(6))
    print(f'MSET {stage}: total={len(ordered)} distinct={len(counter)} '
          f'names=[{top}]', flush=True)
    return dict(total=len(ordered), distinct=len(counter),
                counter=counter, pairs=pairs, ordered=ordered)


def mset_compare(tag: str, a: dict, b: dict) -> int:
    """Tier-1 strict multiset compare; Tier-2 coarse pairing + per-field diff
    only on mismatch.  Returns Tier-1 mismatch count."""
    ca, cb = a['counter'], b['counter']
    diff = (ca - cb) + (cb - ca)
    n = sum(diff.values())
    print(f'MSETDIFF {tag}: mismatches={n} '
          f'(a_total={a["total"]} b_total={b["total"]})', flush=True)
    if n == 0:
        stable = a['ordered'] == b['ordered']
        print(f'MSETORDER {tag}: order_stable={stable}', flush=True)
        return 0
    ma: defaultdict = defaultdict(list)
    mb: defaultdict = defaultdict(list)
    for fk, ck in a['pairs']:
        ma[ck].append(fk)
    for fk, ck in b['pairs']:
        mb[ck].append(fk)
    fields = Counter()
    samples = []
    unpaired = 0
    for ck in sorted(set(ma) | set(mb), key=repr):
        la, lb = sorted(ma.get(ck, []), key=repr), sorted(mb.get(ck, []),
                                                          key=repr)
        for i in range(max(len(la), len(lb))):
            ka = la[i] if i < len(la) else None
            kb = lb[i] if i < len(lb) else None
            if ka is None or kb is None:
                unpaired += 1
                continue
            for fname, va, vb in zip(KEY_FIELDS, ka, kb):
                if va != vb:
                    fields[fname] += 1
                    if len(samples) < 8:
                        samples.append((ck[0], fname, va, vb))
    print(f'MSETDIFF {tag}: tier2 field_diffs={dict(fields)} '
          f'unpaired={unpaired}', flush=True)
    for s in samples:
        print(f'MSETFIELD {tag}: marker={s[0]!r} field={s[1]} '
              f'a={s[2]!r} b={s[3]!r}', flush=True)
    # unpaired samples: coarse keys with no counterpart on the other side
    ca_keys = {ck for _, ck in a['pairs']}
    cb_keys = {ck for _, ck in b['pairs']}
    for side, keys, pairs in (('A', ca_keys - cb_keys, a['pairs']),
                              ('B', cb_keys - ca_keys, b['pairs'])):
        shown = 0
        for fk, ck in pairs:
            if ck in keys and shown < 6:
                loc = tuple('' if x == '' else ('%.4f' % _bits_to_float(x))
                            for x in fk[6])
                print(f'MSETUNPAIRED {tag} {side}: name={fk[0]!r} '
                      f'expected={fk[4]!r} actual={fk[5]!r} loc={loc} '
                      f'objs={fk[9]}', flush=True)
                shown += 1
    return n


def check_delta(session, drc, tag_key: str, stage: str, marker_name: str):
    """E3: full-set diff around one targeted check."""
    before = mset(session, f'{stage}_PRE')
    v = pd.check_cell(session, drc, tag_key, stage, marker_name)
    after = mset(session, f'{stage}_POST')
    d = sum(((before['counter'] - after['counter'])
             + (after['counter'] - before['counter'])).values())
    print(f'CHECK_DELTA {stage} {tag_key}: verdict={v[0]} '
          f'markers_changed={d}', flush=True)
    return v, d


def fdiff(tag: str, pa: Path, pb: Path, cap: int = 12) -> None:
    """Byte-range diff of two probe-owned files; summary to stdout, full table
    to logs/probe_e.fdiff.<tag>.txt (handoff artifact for the raw-file line)."""
    a = pa.read_bytes()
    b = pb.read_bytes()
    ranges = []
    start = None
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            if start is None:
                start = i
        elif start is not None:
            ranges.append((start, i - 1))
            start = None
    if start is not None:
        ranges.append((start, min(len(a), len(b)) - 1))
    n_bytes = sum(e - s + 1 for s, e in ranges)
    print(f'FDIFF {tag}: size_a={len(a)} size_b={len(b)} '
          f'size_equal={len(a) == len(b)} diff_bytes={n_bytes} '
          f'ranges={len(ranges)} first_offset='
          f'{ranges[0][0] if ranges else None}', flush=True)
    for s, e in ranges[:cap]:
        print(f'FDIFF {tag}: range [{s}, {e}]', flush=True)
    if ranges[cap:]:
        print(f'FDIFF {tag}: ... {len(ranges) - cap} more ranges '
              f'(full table in logs/probe_e.fdiff.{tag}.txt)', flush=True)
    LOGS.mkdir(exist_ok=True)
    with open(LOGS / f'probe_e.fdiff.{tag}.txt', 'w',
              encoding='ascii', errors='replace') as fh:
        fh.write(f'# {tag}: {pa} vs {pb}\n')
        fh.write(f'# size_a={len(a)} size_b={len(b)} diff_bytes={n_bytes} '
                 f'ranges={len(ranges)}\n')
        for s, e in ranges:
            fh.write(f'[{s}, {e}]\n')


# --------------------------------------------------------------------------
# STAGE 4 (E4): delete-recreate with marker-set attribution
# --------------------------------------------------------------------------

def stage4_delete_recreate_e(session, drc, padstack, ws, marker_name):
    tag = 'P1_UPPER'
    info = pd.TRACK[tag]
    orig_com = info['com']
    v_before = pd.check_cell(session, drc, tag, 'DEL_PRECHECK', marker_name)
    pd.marker_count(drc, 'DEL_BEFORE')
    m_del0 = mset(session, 'DEL0_BEFORE')
    S, E = info['S'], info['E']
    y0 = S[1]
    bx0, by0 = min(S[0], E[0]) - 0.15, y0 - 1.0
    bx1, by1 = max(S[0], E[0]) + 0.15, y0 + 0.15
    box = f'list({bx0!r}:{by0!r} {bx1!r}:{by1!r})'
    deleted = False
    for filt in ('arcs', 'clines'):
        try:
            ws['evalstring'](
                f'axlSetFindFilter(?enabled list("noall" "{filt}") '
                f'?onButtons list("noall" "{filt}"))')
            sel_ok = ws['evalstring'](f'axlSingleSelectBox({box})')
            n_raw = ws['evalstring']('length(axlGetSelSet())')
            try:
                n = int(n_raw)
            except (TypeError, ValueError):
                n = -1
            print(f'DELETE_SELECT filter={filt}: sel_ok={sel_ok!r} '
                  f'selset_count={n_raw!r}', flush=True)
            if n == 1:
                res = ws['evalstring'](
                    'if(axlDeleteObject(axlGetSelSet()) 1 0)')
                print(f'DELETE_RESULT filter={filt}: {res!r}', flush=True)
                deleted = (res == 1)
                break
        except Exception as exc:
            print(f'DELETE_SELECT_FAILED filter={filt}: {exc!r}', flush=True)
    session.refresh()
    if not deleted:
        print('STAGE4: SKIP (delete canary unavailable)', flush=True)
        pd.RESULTS['DELETE_RECREATE'] = 'SKIPPED'
        return
    row = pd.find_row(session, info)
    print(f'DELETE_VERIFY: row_present_after_delete={row is not None}',
          flush=True)
    if row is not None:
        pd.RESULTS['DELETE_RECREATE'] = 'ABORTED_STILL_PRESENT'
        return
    m_del1 = mset(session, 'DEL1_AFTER_DELETE')
    removed = m_del0['counter'] - m_del1['counter']
    # figure-start bits of the deleted upper arc AND its lower partner
    # (both cell endpoints are tracked, so attribution is exact)
    p1_s_bits = (_bitsf(S[0]), _bitsf(S[1]))
    lower_S = pd.TRACK['P1_LOWER']['S']
    p1_l_bits = (_bitsf(lower_S[0]), _bitsf(lower_S[1]))

    def refs_p1(full_key):
        # fig key layout: (obj_type, layer, net, location, start, end, ...)
        for fig in full_key[10]:
            netname, start = fig[2], fig[4]
            if netname == pc.NET_A and start == p1_s_bits:
                return True
            if netname == pc.NET_B and start == p1_l_bits:
                return True
        return False

    attr = {k: refs_p1(k) for k in removed}
    for k, cnt in removed.items():
        print(f'DEL_REMOVED x{cnt}: name={k[0]!r} actual={k[5]!r} '
              f'refs_P1_cell={attr[k]}', flush=True)
    print(f'DEL_MARKER_REMOVED: keys={len(removed)} '
          f'instances={sum(removed.values())} '
          f'all_attributed_to_P1={all(attr.values()) if attr else None}',
          flush=True)
    rows = session.routes.create(
        info['net'],
        [info['S'], ArcTo(end=info['E'], center=info['req_C'],
                          clockwise=info['cw'])],
        pc.LAYER, pc.WIDTH)
    arcs = [r for r in rows if r.obj_type == 'arc']
    if not arcs:
        print('RECREATE: NO ARC ROW', flush=True)
        pd.RESULTS['DELETE_RECREATE'] = 'RECREATE_FAILED'
        return
    r2 = arcs[0]
    new_com = dict(cx=float(r2.center.x), cy=float(r2.center.y),
                   r=float(r2.radius), length=float(r2.length),
                   cw=r2.is_clockwise)
    same = all(orc.bits(new_com[k]) == orc.bits(orig_com[k])
               for k in ('cx', 'cy', 'r', 'length')) \
        and new_com['cw'] == orig_com['cw']
    print(f'RECREATE_BITS: identical={same}', flush=True)
    pd.TRACK[tag]['com'] = new_com
    m_del2 = mset(session, 'DEL2_AFTER_RECREATE')
    added = m_del2['counter'] - m_del1['counter']
    for k, cnt in added.items():
        print(f'DEL_ADDED x{cnt}: name={k[0]!r} actual={k[5]!r}', flush=True)
    restored = (removed == added)
    print(f'DEL_MARKER_RESTORED_BIT_EXACT: {restored}', flush=True)
    pd.RESULTS['DEL_MARKERS'] = (f'removed={sum(removed.values())} '
                                 f'added={sum(added.values())} '
                                 f'restored_bit_exact={restored} '
                                 f'all_attributed={all(attr.values()) if attr else None}')
    v_after = pd.check_cell(session, drc, tag, 'DEL_POSTRECREATE',
                            marker_name)
    pd.marker_count(drc, 'DEL_AFTER_RECREATE')
    pd.RESULTS['DELETE_RECREATE'] = (f'bits_identical={same} '
                                     f'verdict_stable={v_before == v_after}')


# --------------------------------------------------------------------------
# phases
# --------------------------------------------------------------------------

def run_e1(work: Path) -> dict:
    board = copy2(ASSETS_DIR / 'route' / 'EL5_MIAN_FPC.brd', work)
    f1a = work / 'probe_e_F1a.brd'
    f1 = work / 'probe_e_F1.brd'
    f2b = work / 'probe_e_F2b.brd'
    f2 = work / 'probe_e_F2.brd'
    f3 = work / 'probe_e_F3.brd'
    os.environ['ALLEGROBRIDGE_LOG_DIRECTORY'] = work.as_posix()
    print(f'WORKDIR {work}', flush=True)
    print(f'BOARD_COPY_SHA256_START {pd.sha256(board)}', flush=True)
    ports = [pd._free_port() for _ in range(3)]
    print(f'PORTS {ports}', flush=True)
    state = dict(work=work, board=Path(board), f1a=f1a, f1=f1, f2b=f2b,
                 f2=f2, f3=f3, ports=ports, marker_name=None,
                 s1_pre=None, v1_pre=None, m1_pre=None, m1_post=None)

    with pd.open_verified(board, ports[0], 'S1') as allegro:
        session = allegro.session
        ws = session.workspace
        drc = session.drc
        padstack = Counter(v.padstack
                           for v in session.vias()).most_common(1)[0][0]
        print('PADSTACK:', padstack, flush=True)
        pd.marker_count(drc, 'BASELINE')
        mset(session, 'BASELINE')

        # ---- STAGE 0: rule learning (identical to probe_d) --------------
        print('STAGE0: rule learning (natural arc y0=390 + tight line)',
              flush=True)
        cy_nat = 390.0 + CY_OFF
        s0_arc = pc.create_arc_net(session, padstack, pc.NET_A, (SX, 390.0),
                                   (EX, 390.0), (CX_NAT, cy_nat), False,
                                   'STAGE0_ARC')
        if s0_arc is None or s0_arc.center is None:
            print('STAGE0: ARC CREATION FAILED - ABORT', flush=True)
            return pd._sync_state(state)
        p1 = Decimal(float(s0_arc.center.y)) - Decimal(float(s0_arc.radius))
        L_dec = pc.floor_grid(p1 - pc.W_TOTAL - pc.NOMINAL_TIGHT)
        pc.create_line(session, padstack, float(L_dec), 'STAGE0_LINE')
        found = pc.run_drc(drc, s0_arc, 'STAGE0', None)
        if not found:
            print('STAGE0: NO SPACING MARKER - cannot learn R; ABORT',
                  flush=True)
            return pd._sync_state(state)
        if len(found) > 1:
            pref = [t for t in found
                    if t[0].lower() == 'line to line spacing']
            if pref:
                found = pref
        marker_name, expected, actual, _ = found[0]
        R_dec = Decimal(pc._quantity(expected))
        delta_dec = pc.floor_grid(R_dec + 2 * Decimal(pc.R_NAT_F)
                                  + pc.W_TOTAL - 2 * pc.CY_OFF_DEC)
        print(f'STAGE0: marker_name={marker_name!r} R={R_dec} DELTA={delta_dec}',
              flush=True)
        pd.marker_count(drc, 'STAGE0_END')

        def plan(y0, win, cy1_override=None):
            p = pd.plan_cell(y0, R_dec, delta_dec, win[0], win[1], win[2],
                             cy1_override=cy1_override)
            if p is not None:
                p['R_dec'] = R_dec
            return p

        # ---- STAGE 1 with E3 side-effect measurement ---------------------
        print('STAGE1: P1 violation cell y0=410', flush=True)
        plan_p1 = plan(410, pd.DELTA_WIN)
        if plan_p1 is None:
            print('STAGE1: EPS_SCAN_FAILED - ABORT', flush=True)
            return pd._sync_state(state)
        pd.create_pair(session, drc, padstack, 'P1', plan_p1, marker_name)
        mset(session, 'P1_AFTER_CREATE')
        h1, d1 = check_delta(session, drc, 'P1_UPPER', 'P1_CHECK1',
                             marker_name)
        h2, d2 = check_delta(session, drc, 'P1_UPPER', 'P1_CHECK2',
                             marker_name)
        h3 = pd.check_cell(session, drc, 'P1_UPPER', 'P1_CHECK3',
                           marker_name)
        pd.RESULTS['REPEAT_STABLE'] = (h1 == h2 == h3)
        pd.RESULTS['CHECK_SIDE_EFFECT_S1_P1'] = [d1, d2]
        print(f'REPEAT_STABLE: {h1 == h2 == h3}', flush=True)
        try:
            upd = drc.update()
            print(f'UPDATE: markers_returned={len(upd)}', flush=True)
        except Exception as exc:
            print(f'UPDATE: FAILED {exc!r}', flush=True)
        mset(session, 'P1_AFTER_UPDATE')
        h4 = pd.check_cell(session, drc, 'P1_UPPER', 'P1_CHECK4_AFTER_UPDATE',
                           marker_name)
        pd.RESULTS['UPDATE_VERDICT_STABLE'] = (h4 == h1)

        print('STAGE1: P2 clean cell y0=430', flush=True)
        plan_p2 = plan(430, pd.MARGIN_WIN)
        if plan_p2 is not None:
            pd.create_pair(session, drc, padstack, 'P2', plan_p2, marker_name)
            mset(session, 'P2_AFTER_CREATE')
            g1, d3 = check_delta(session, drc, 'P2_UPPER', 'P2_CHECK1',
                                 marker_name)
            g2 = pd.check_cell(session, drc, 'P2_UPPER', 'P2_CHECK2',
                               marker_name)
            pd.RESULTS['CLEAN_REPEAT_STABLE'] = (
                g1 == g2 == ('clean', None, None))
            pd.RESULTS['CHECK_SIDE_EFFECT_S1_P2'] = [d3]
        h5 = pd.check_cell(session, drc, 'P1_UPPER', 'P1_CHECK5_AFTER_P2',
                           marker_name)
        pd.RESULTS['FAR_OBJECT_STABLE'] = (h5 == h1)

        # ---- STAGE 2: order swap (identical to probe_d) ------------------
        print('STAGE2: order swap', flush=True)
        va = vb = None
        plan_a = plan(450, pd.DELTA_WIN)
        plan_b = plan(470, pd.DELTA_WIN)
        if plan_a is not None and plan_b is not None:
            pd.create_pair(session, drc, padstack, 'ORD_A', plan_a,
                           marker_name, lower_first=False)
            va = pd.check_cell(session, drc, 'ORD_A_UPPER', 'ORD_A_CHECK',
                               marker_name)
            pd.create_pair(session, drc, padstack, 'ORD_B', plan_b,
                           marker_name, lower_first=True)
            vb = pd.check_cell(session, drc, 'ORD_B_UPPER', 'ORD_B_CHECK',
                               marker_name)
            cyA = pd.TRACK['ORD_A_UPPER']['com']['cy']
            cyB = pd.TRACK['ORD_B_UPPER']['com']['cy']
            rA = pd.TRACK['ORD_A_UPPER']['com']['r']
            rB = pd.TRACK['ORD_B_UPPER']['com']['r']
            print(f'ORDER_SWAP: dcy(committed)-20='
                  f'{Decimal(cyB) - Decimal(cyA) - 20} '
                  f'dr={Decimal(rB) - Decimal(rA)}', flush=True)
            pd.RESULTS['ORDER_SWAP_CONSISTENT'] = (
                va[0] == vb[0] == 'FLAGGED' and va[1] == vb[1])
        else:
            pd.RESULTS['ORDER_SWAP_CONSISTENT'] = 'SCAN_FAILED'

        # ---- STAGE 3: equivalent representation --------------------------
        print('STAGE3: forward y0=490 vs reversed y0=510', flush=True)
        vf = vr = None
        plan_f = plan(490, pd.DELTA_WIN)
        if plan_f is not None:
            pd.create_pair(session, drc, padstack, 'FWD', plan_f, marker_name)
            vf = pd.check_cell(session, drc, 'FWD_UPPER', 'FWD_CHECK',
                               marker_name)
            cy1_rev = float(Decimal(pd.TRACK['FWD_UPPER']['com']['cy'])
                            + Decimal(20))
            plan_r = plan(510, pd.DELTA_WIN, cy1_override=cy1_rev)
            if plan_r is not None:
                pd.create_pair(session, drc, padstack, 'REV', plan_r,
                               marker_name, reverse_upper=True)
                vr = pd.check_cell(session, drc, 'REV_UPPER', 'REV_CHECK',
                                   marker_name)
                fC = pd.TRACK['FWD_UPPER']['com']
                rC = pd.TRACK['REV_UPPER']['com']
                print(f'REVERSED_EQUIV: dcx='
                      f'{Decimal(rC["cx"]) - Decimal(fC["cx"])} '
                      f'dcy-20={Decimal(rC["cy"]) - Decimal(fC["cy"]) - 20} '
                      f'dr={Decimal(rC["r"]) - Decimal(fC["r"])}', flush=True)
                pd.RESULTS['REVERSED_EQUIVALENT'] = (
                    vf[0] == vr[0] and vf[1] == vr[1]
                    and orc.bits(rC['r']) == orc.bits(fC['r']))
            else:
                pd.RESULTS['REVERSED_EQUIVALENT'] = 'SCAN_FAILED'
        else:
            pd.RESULTS['REVERSED_EQUIVALENT'] = 'SCAN_FAILED'

        # ---- STAGE 4 (E4): delete-recreate with attribution --------------
        print('STAGE4: delete-recreate P1 upper (with marker attribution)',
              flush=True)
        stage4_delete_recreate_e(session, drc, padstack, ws, marker_name)

        # ---- STAGE 5a (E5): snapshots, zero-op double save ---------------
        print('STAGE5: snapshots + zero-op double save (F1a, F1)', flush=True)
        s1_pre = pd.snap(session, 'S1_PRE')
        v1_pre = pd.verdict_snapshot(session, drc, 'S1_PRE_CHECK', marker_name)
        m1_pre = mset(session, 'S1_PRE')
        try:
            save1a = ws['axlSaveDesign'](design=f1a.as_posix(),
                                         no_confirm=True)
            print(f'SAVE F1a: result={save1a!r} '
                  f'size={f1a.stat().st_size if f1a.exists() else None}',
                  flush=True)
            save1 = ws['axlSaveDesign'](design=f1.as_posix(), no_confirm=True)
            print(f'SAVE F1: result={save1!r} '
                  f'size={f1.stat().st_size if f1.exists() else None}',
                  flush=True)
        except Exception as exc:
            print(f'SAVE F1a/F1: FAILED {exc!r}', flush=True)
        pd.RESULTS['SAVE_F1'] = 'OK' if f1.exists() else 'FAILED'
        if f1a.exists() and f1.exists():
            h_a, h_b = pd.sha256(f1a), pd.sha256(f1)
            print(f'F1A_SHA256 {h_a}', flush=True)
            print(f'F1_SHA256 {h_b}', flush=True)
            pd.RESULTS['F1A_EQ_F1'] = (h_a == h_b
                                       and f1a.stat().st_size
                                       == f1.stat().st_size)
            print(f'F1A_EQ_F1: {pd.RESULTS["F1A_EQ_F1"]}', flush=True)
        session.refresh()          # axlSaveDesign cleared all dbid handles
        s1_post = pd.snap(session, 'S1_POST')
        pd.RESULTS['BITS_S1_POST_SAVE'] = pd.snap_compare('S1_SAVE_INMEMORY',
                                                          s1_pre, s1_post)
        v1_post = pd.verdict_snapshot(session, drc, 'S1_POST_CHECK',
                                      marker_name)
        pd.verdict_compare('S1_SAVE_INMEMORY', v1_pre, v1_post, pd.VTAGS)
        m1_post = mset(session, 'S1_POST')
        pd.RESULTS['MSETDIFF_S1_POST_VS_PRE'] = mset_compare(
            'S1_POST_VS_PRE', m1_post, m1_pre)

    state.update(marker_name=marker_name, s1_pre=s1_pre, v1_pre=v1_pre,
                 m1_pre=m1_pre, m1_post=m1_post)
    return pd._sync_state(state)


def run_e2(state: dict) -> None:
    f1, f2b, f2 = state['f1'], state['f2b'], state['f2']
    m1_post, v1_pre = state['m1_post'], state['v1_pre']
    marker_name = state['marker_name']
    if not f1.exists():
        print('E2: SKIP (F1 missing)', flush=True)
        pd._sync_state(state)
        return
    with pd.open_verified(f1, pd._free_port(), 'S2') as allegro2:
        session2 = allegro2.session
        ws2 = session2.workspace
        drc2 = session2.drc
        print('E2: opened F1', flush=True)
        m2_persist = mset(session2, 'S2_PERSISTED')
        pd.RESULTS['MSETDIFF_S2_PERSISTED_VS_S1_POST'] = mset_compare(
            'S2_PERSISTED_VS_S1_POST', m2_persist, m1_post)
        # E5: save the reopened state BEFORE any check/update (pure persistence)
        try:
            save2b = ws2['axlSaveDesign'](design=f2b.as_posix(),
                                          no_confirm=True)
            print(f'SAVE F2b: result={save2b!r} '
                  f'size={f2b.stat().st_size if f2b.exists() else None}',
                  flush=True)
            print(f'F2B_SHA256 {pd.sha256(f2b)}', flush=True)
        except Exception as exc:
            print(f'SAVE F2b: FAILED {exc!r}', flush=True)
        # E3 on persisted markers
        v2, d_s2 = check_delta(session2, drc2, 'P1_UPPER', 'S2_CHECK',
                               marker_name)
        pd.RESULTS['CHECK_SIDE_EFFECT_S2_P1'] = [d_s2]
        v2_all = pd.verdict_snapshot(session2, drc2, 'S2_CHECK_ALL',
                                     marker_name)
        bad2 = pd.verdict_compare('S2_REOPEN', v1_pre, v2_all, pd.VTAGS)
        pd.RESULTS['VERDICTS_S2_STABLE'] = not bad2
        # E2: update x2
        try:
            upd2 = drc2.update()
            print(f'S2_UPDATE1: markers_returned={len(upd2)}', flush=True)
            m2_u1 = mset(session2, 'S2_AFTER_UPDATE1')
            pd.RESULTS['PERSISTED_VS_REGENERATED'] = mset_compare(
                'S2_PERSISTED_VS_REGENERATED', m2_persist, m2_u1)
            upd3 = drc2.update()
            print(f'S2_UPDATE2: markers_returned={len(upd3)}', flush=True)
            m2_u2 = mset(session2, 'S2_AFTER_UPDATE2')
            pd.RESULTS['UPDATE_IDEMPOTENT'] = mset_compare(
                'S2_UPDATE_IDEMPOTENT', m2_u1, m2_u2) == 0
            print(f'UPDATE_IDEMPOTENT: {pd.RESULTS["UPDATE_IDEMPOTENT"]}',
                  flush=True)
            print(f'PERSISTED_VS_REGENERATED_MISMATCHES='
                  f'{pd.RESULTS["PERSISTED_VS_REGENERATED"]}', flush=True)
            # convergence probe: does a third update shift fewer markers?
            upd4 = drc2.update()
            print(f'S2_UPDATE3: markers_returned={len(upd4)}', flush=True)
            m2_u3 = mset(session2, 'S2_AFTER_UPDATE3')
            pd.RESULTS['UPDATE3_MISMATCHES'] = mset_compare(
                'S2_UPDATE2_VS_UPDATE3', m2_u2, m2_u3)
        except Exception as exc:
            print(f'S2_UPDATE: FAILED {exc!r}', flush=True)
        try:
            save2 = ws2['axlSaveDesign'](design=f2.as_posix(), no_confirm=True)
            print(f'SAVE F2: result={save2!r} '
                  f'size={f2.stat().st_size if f2.exists() else None}',
                  flush=True)
            print(f'F2_SHA256 {pd.sha256(f2)}', flush=True)
        except Exception as exc:
            print(f'SAVE F2: FAILED {exc!r}', flush=True)
        if f2b.exists() and f1.exists():
            fdiff('F2B_VS_F1', f2b, f1)
        if f2.exists() and f2b.exists():
            fdiff('F2_VS_F2B', f2, f2b)
    state['m2_persist'] = m2_persist
    pd._sync_state(state)


def run_e3(state: dict) -> None:
    f2b, f3 = state['f2b'], state['f3']
    m2_persist, m1_post, v1_pre = (state.get('m2_persist'),
                                   state.get('m1_post'), state.get('v1_pre'))
    marker_name = state.get('marker_name')
    if not f2b.exists() or m2_persist is None:
        print('E3: SKIP (F2b or m2_persist missing - E2 did not complete)',
              flush=True)
        pd._sync_state(state)
        return
    with pd.open_verified(f2b, pd._free_port(), 'S3') as allegro3:
        session3 = allegro3.session
        ws3 = session3.workspace
        drc3 = session3.drc
        print('E3: opened F2b (pure persistence: reopen WITHOUT regeneration)',
              flush=True)
        m3 = mset(session3, 'S3_PERSISTED')
        pd.RESULTS['MSETDIFF_S3_F2B_VS_S2_PERSISTED'] = mset_compare(
            'S3_F2B_VS_S2_PERSISTED', m3, m2_persist)
        pd.RESULTS['MSETDIFF_S3_F2B_VS_S1_POST'] = mset_compare(
            'S3_F2B_VS_S1_POST', m3, m1_post)
        v3 = pd.verdict_snapshot(session3, drc3, 'S3_CHECK', marker_name,
                                 tags=('P1_UPPER', 'REV_UPPER'))
        pd.verdict_compare('S3_F2B_REOPEN', v1_pre, v3,
                           ('P1_UPPER', 'REV_UPPER'))
        try:
            save3 = ws3['axlSaveDesign'](design=f3.as_posix(), no_confirm=True)
            print(f'SAVE F3: result={save3!r} '
                  f'size={f3.stat().st_size if f3.exists() else None}',
                  flush=True)
            print(f'F3_SHA256 {pd.sha256(f3)}', flush=True)
        except Exception as exc:
            print(f'SAVE F3: FAILED {exc!r}', flush=True)
        if f3.exists():
            fdiff('F3_VS_F2B', f3, f2b)
        # ---- E6 (gated, single attempt) ---------------------------------
        gate = (pd.RESULTS.get('MSETDIFF_S2_PERSISTED_VS_S1_POST') == 0
                and pd.RESULTS.get('MSETDIFF_S3_F2B_VS_S2_PERSISTED') == 0)
        if not gate:
            print('E6: SKIPPED (set identity not bit-clean)', flush=True)
            pd.RESULTS['E6_WAIVER'] = 'SKIPPED (set identity not bit-clean)'
        else:
            try:
                payload = ('errset.string=catch(car(axlDBGetDesign()->drcs) '
                           'errset.errset)')
                handle = ws3['evalstring'](payload)
                print(f'E6: marker handle -> {handle!r}', flush=True)
                if handle is None:
                    raise RuntimeError('design->drcs empty / no handle')
                w = ws3['axlDRCWaive'](True, handle, 'probe-e')
                cnt = ws3['evalstring']('axlDRCWaiveGetCount()')
                m3w = mset(session3, 'E6_AFTER_WAIVE')
                print(f'E6: waive={w!r} waived_count={cnt!r} '
                      f'markers_after={m3w["total"]}', flush=True)
                uw = ws3['axlDRCWaive'](False, handle)
                cnt2 = ws3['evalstring']('axlDRCWaiveGetCount()')
                print(f'E6: unwaive={uw!r} waived_count_after={cnt2!r}',
                      flush=True)
                pd.RESULTS['E6_WAIVER'] = (f'waive={w!r} count={cnt!r} '
                                           f'markers_after_waive='
                                           f'{m3w["total"]} unwaive={uw!r} '
                                           f'count_after={cnt2!r}')
            except Exception as exc:
                print(f'E6: NOT_TESTED {exc!r}', flush=True)
                pd.RESULTS['E6_WAIVER'] = f'NOT_TESTED {exc!r}'
    pd._sync_state(state)


# --------------------------------------------------------------------------
# main / selftest / phase dispatch
# --------------------------------------------------------------------------

def _selftest() -> None:
    from types import SimpleNamespace as NS

    def mk(actual='0.0599 MM', dy=0.0, name='Line to Line Spacing'):
        return NS(name=name, category='NET SPACING CONSTRAINTS',
                  source='Constraint', layer='ETCH/TOP',
                  expected='0.06 MM', actual=actual,
                  location=Point(300.0, 410.0 + dy),
                  bbox=BBox(ll=Point(299.9, 409.0), ur=Point(302.1, 411.0)),
                  objects=[NS(kind='net', refdes=None, name='NFC_SWP',
                              number=None)],
                  figures=[NS(obj_type='arc', layer='ETCH/TOP',
                              net=NS(kind='net', refdes=None, name='NFC_SWP',
                                     number=None),
                              location=None,
                              start=Point(300.0, 410.0),
                              end=Point(302.0001, 410.0),
                              center=Point(301.00005, 410.12498067),
                              radius=1.007829435159368, width=0.15,
                              is_clockwise=None, reference=None)])

    class Session:
        def __init__(self, rows):
            self._rows = rows

        def drc(self):
            return self._rows

    a = mset(Session([mk(), mk('0.06 MM')]), 'T1')
    b = mset(Session([mk('0.06 MM'), mk()]), 'T1B')
    n = mset_compare('SELFTEST_IDENTICAL', a, b)
    print(f'SELFTEST identical_multiset: mismatches={n} (expect 0)',
          flush=True)
    c = mset(Session([mk(dy=1e-9), mk('0.06 MM')]), 'T2')
    n2 = mset_compare('SELFTEST_SUBGRID_LOCATION', a, c)
    print(f'SELFTEST subgrid_location: mismatches={n2} (expect >0, '
          f'tier2 pairs by coarse key, field=location)', flush=True)
    d = mset(Session([mk(actual='0.0598 MM'), mk('0.06 MM')]), 'T3')
    n3 = mset_compare('SELFTEST_ACTUAL_STRING', a, d)
    print(f'SELFTEST actual_string: mismatches={n3} (expect >0, '
          f'field=actual)', flush=True)
    cnt = a['counter']
    single = cnt - Counter([a['ordered'][0]])
    print(f'SELFTEST duplicates: total={a["total"]} after_remove_one='
          f'{sum(single.values())} (expect 2 -> 1)', flush=True)
    print('SELFTEST DONE', flush=True)


def main() -> None:
    if '--selftest' in sys.argv:
        _selftest()
        return
    argv = sys.argv[1:]
    if '--phase' in argv:
        i = argv.index('--phase')
        phase = argv[i + 1]
        if phase == 'e1':
            work = Path(mkdtemp(prefix='drc-probe-e-'))
            state = run_e1(work)
            sf = work / 'probe_e_state.pkl'
            with open(sf, 'wb') as fh:
                pickle.dump(state, fh, protocol=4)
            print(f'STATE_FILE {sf}', flush=True)
            pd._summary()
            return
        sf = Path(argv[i + 2])
        with open(sf, 'rb') as fh:
            state = pickle.load(fh)
        pd.TRACK.clear()
        pd.TRACK.update(state['TRACK'])
        pd.RESULTS.clear()
        pd.RESULTS.update(state['RESULTS'])
        if phase == 'e2':
            run_e2(state)
        elif phase == 'e3':
            run_e3(state)
        else:
            raise SystemExit(f'unknown phase {phase!r}')
        with open(sf, 'wb') as fh:
            pickle.dump(state, fh, protocol=4)
        pd._summary()
        return
    # Legacy single-process path (kept for the record): in-process reopen
    # after S1's terminate-close hits the empty-design refusal (see probe_d
    # header).  Use run_e_chain.sh instead.
    work = Path(mkdtemp(prefix='drc-probe-e-'))
    state = run_e1(work)
    run_e2(state)
    run_e3(state)
    pd._summary()


if __name__ == '__main__':
    main()
