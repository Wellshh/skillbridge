"""Offline Stage0 gate audit for the accepted B3 replay evidence.

This consumes immutable raw replay JSON and deliberately returns AMBIGUOUS when
any evidence field is missing; it never infers CLEAN from an empty lookup.
"""
from __future__ import annotations
import json, struct, copy
from pathlib import Path

ROOT=Path(__file__).resolve().parent
RUN=ROOT/'results'/'stage0-b-replay'/'run-36900-1789223446873968800'
OUT=ROOT/'results'/'stage2-boundary'/'boundary_gate.json'

def scalar(v):
    if isinstance(v,dict) and 'bits' in v: return struct.unpack('>d',bytes.fromhex(v['bits']))[0]
    if isinstance(v,dict) and 'value' in v: return scalar(v['value'])
    return float(v)
def point(v):
    return (scalar(v['x']),scalar(v['y'])) if isinstance(v,dict) else (scalar(v[0]),scalar(v[1]))
def sig(f):
    if not isinstance(f,dict) or f.get('obj_type') not in ('arc','line') or not f.get('start') or not f.get('end') or not f.get('width'): return None
    net=f.get('net'); net=net.get('name') if isinstance(net,dict) else net
    return (f['obj_type'],net,f.get('layer'),tuple(struct.pack('>d',x).hex() for x in point(f['start'])),tuple(struct.pack('>d',x).hex() for x in point(f['end'])),tuple(struct.pack('>d',x).hex() for x in point(f['center'])) if f.get('center') else None,struct.pack('>d',scalar(f['width'])).hex(),struct.pack('>d',scalar(f['radius'])).hex() if f.get('radius') is not None else None,None if f.get('is_clockwise') is False else f.get('is_clockwise'))
def val(x): return x.get('value') if isinstance(x,dict) else None
def atom(x):
    while isinstance(x,list) and len(x)==1: x=x[0]
    return x
def gate(c):
    settings=c.get('settings',{}); d=c.get('drc',{}); ctx=settings.get('context',{}).get('value',{}); objs=c.get('creation',{})
    arc,line=objs.get('arc_requery'),objs.get('line_requery'); targets={sig(arc),sig(line)} if arc and line else set(); reasons=[]; groups=[]
    if len(targets)!=2 or None in targets: reasons.append('target signatures incomplete')
    if not (settings.get('drcEnable_before',{}).get('value') is True and settings.get('drcEnable_after',{}).get('value') is True): reasons.append('master drcEnable not true before/after')
    if settings.get('waived_before',{}).get('value')!=0 or d.get('waived_after',{}).get('value')!=0: reasons.append('waive count not zero before/after')
    mode=val(settings.get('spacing_mode_all',{})); mode_pairs={(atom(x[0]),atom(x[1])) for x in (mode or []) if isinstance(x,list) and len(x)==2};
    if ('line_line','on') not in mode_pairs: reasons.append('line_line mode not explicitly on')
    if ctx.get('netA',{}).get('name')!='NFC_SWP' or ctx.get('netB',{}).get('name')!='FINGER_SPI_MISO' or ctx.get('netA',{}).get('found') is not True or ctx.get('netB',{}).get('found') is not True: reasons.append('context net lookup incomplete')
    if any(ctx.get(k,{}).get(z,'missing') is not None for k in ('netA','netB') for z in ('directClass','hierClass')): reasons.append('unexpected net class override')
    tables=ctx.get('classTables',{})
    if any(k not in tables for k in ('netclass','classClass','classRegion','classClassRegion')): reasons.append('classTables incomplete')
    if any(tables.get(k) is not None for k in ('netclass','classClass','classRegion','classClassRegion')): reasons.append('unexpected class/region override')
    if not all(settings.get(k,{}).get('ok') for k in ('spacing_line_line_numeric','spacing_line_line_string')): reasons.append('numeric/string rule read failed')
    elif scalar(settings['spacing_line_line_numeric']['value']) != scalar(0.06) or settings['spacing_line_line_string'].get('value') != '0.06 MM': reasons.append('numeric/string rule mismatch')
    def group(ms):
        pairs=0
        for m in ms or []:
            md=m.get('data',{}); fs=md.get('figures',[]); route={sig(f) for f in fs if sig(f) is not None}
            if not all(md.get(k) for k in ('name','category','source','actual','expected','layer')) or not fs: reasons.append('incomplete marker fields')
            if route==targets and len(fs)==2 and md.get('name')=='Line to Line Spacing' and md.get('category')=='NET SPACING CONSTRAINTS' and md.get('source')=='DEFAULT' and md.get('expected')=='0.06 MM' and m.get('waived') is None: pairs+=1
            elif route==targets: reasons.append('target pair wrong rule metadata or extra figure')
        return pairs
    if len(d.get('item_calls',[]))!=2: reasons.append('expected two item calls')
    for x in d.get('item_calls',[]):
        a,b=x.get('first',{}),x.get('second',{}); av,bv=a.get('value',{}),b.get('value',{}); ms=av.get('markers',[])
        if not (a.get('ok') and b.get('ok') and av.get('resolved') is True and bv.get('resolved') is True and isinstance(av.get('count'),int) and av.get('count')==len(ms) and bv.get('count')==len(bv.get('markers',[])) and av.get('count')==bv.get('count') and a==b): reasons.append('count/list/repeat gate failed')
        groups += [group(ms),group(bv.get('markers',[]))]
    for k in ('snapshot_before','snapshot_after'):
        s=d.get(k,{}); v=s.get('value',{}); 
        if not (s.get('ok') and isinstance(v.get('count'),int) and v.get('count')==len(v.get('markers',[]))): reasons.append(k+' incomplete')
        groups.append(group(v.get('markers',[])))
    if not d.get('full_update',{}).get('ok'): reasons.append('full update missing')
    present=[x>0 for x in groups]
    if len(groups)!=6 or len(set(present))!=1: reasons.append('six group pair existence mismatch')
    return ('AMBIGUOUS' if reasons else ('FLAGGED' if present[0] else 'CLEAN')), {'reasons':reasons,'target_signatures':len(targets),'group_pair_counts':groups,'group_pair_present':present}

def main():
    cases=[json.loads(x) for x in (RUN/'cases.jsonl').read_text(encoding='utf8').splitlines() if x.strip()]
    verdicts=[]
    for c in cases:
        v,e=gate(c); verdicts.append({'tag':c.get('tag'),'verdict':v,'evidence':e})
    base=cases[0]; negatives=[]
    for label,mutate in [('delete_item_calls',lambda x:x['drc'].__setitem__('item_calls',[])),('blank_snapshot_marker',lambda x:x['drc']['snapshot_after']['value']['markers'][0]['data'].__setitem__('name',None)),('delete_class_table',lambda x:x['settings']['context']['value']['classTables'].__delitem__('netclass')),('wrong_string_rule',lambda x:x['settings']['spacing_line_line_string'].__setitem__('value','0.15 MM')),('remove_snapshot_pair',lambda x:(x['drc']['snapshot_after']['value'].__setitem__('markers',[]),x['drc']['snapshot_after']['value'].__setitem__('count',0)))]:
        q=copy.deepcopy(base); mutate(q); v,_=gate(q); negatives.append({'mutation':label,'verdict':v})
    result={'status':'OFFLINE_GATE_PASS' if [x['verdict'] for x in verdicts]==['FLAGGED','CLEAN','CLEAN'] and all(x['verdict']=='AMBIGUOUS' for x in negatives) else 'OFFLINE_GATE_FAIL','source':str(RUN),'cases':verdicts,'negative_derived_checks':negatives}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,indent=2),encoding='utf8'); print(json.dumps(result,indent=2)); return 0 if result['status']=='OFFLINE_GATE_PASS' else 1
if __name__=='__main__': raise SystemExit(main())
