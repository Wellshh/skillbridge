from __future__ import annotations
import copy, importlib.util, json, struct
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parent
RUN=ROOT/'results'/'stage3-translation'/'run-29568-1789228092086311600'/'manifest.json'
REOPEN=ROOT/'results'/'stage1-beta-reopen'/'run-52936-1789229074638350500'/'manifest.json'
GATE=RUN.parent/'boundary_gate.py'
BOUNDARY_CASES=ROOT/'results'/'stage2-boundary'/'run-33608-1789226631112365500'/'cases.jsonl'
OUT=ROOT/'results'/'stage3-translation-analysis'

def F(x):
    if isinstance(x,dict) and 'bits' in x: return Fraction.from_float(struct.unpack('>d',bytes.fromhex(x['bits']))[0])
    if isinstance(x,dict) and 'value' in x: return F(x['value'])
    return Fraction.from_float(float(x))
def net(dto):
    n=dto.get('net'); return n.get('name') if isinstance(n,dict) else n
def coord(p,axis):
    if isinstance(p,dict): return p[axis]
    return p[0 if axis=='x' else 1]
def objmap(c): return {x.get('name'):x for x in c.get('creation',{}).get('objects',[])}
def clearance(c):
    o=objmap(c); a=o['arcA']['dto']; l=o['lineB']['dto']; cy=F(coord(a['center'],'y')); r=F(a['radius']); ly=F(coord(l['start'],'y')); w=(F(a['width'])+F(l['width']))/2
    return cy-r-ly-w
def gate_check(c):
    try:
        s=importlib.util.spec_from_file_location('bg',GATE); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
        v,e=m.gate(c['audit_view'] if 'audit_view' in c else c); return {'verdict':v,'evidence':e}
    except Exception as e: return {'verdict':'ERROR','error':repr(e)}
def main():
    d=json.loads(RUN.read_text()); cases=d['cases']; groups={}
    boundary_by_bits={}
    for line in BOUNDARY_CASES.read_text().splitlines():
        q=json.loads(line); b=q.get('cy',{}).get('bits') if isinstance(q.get('cy'),dict) else None
        if b in ('4079a1ffae2ca8c6','4079a1ffae4a04f8'): boundary_by_bits[b]=q
    for c in cases: groups.setdefault(c['label'].split('_T')[0],{})[c['translation']['tx'],c['translation']['ty']]=c
    rows=[]
    for c in cases:
        rel={x['name']:x.get('actual_relative_fraction') for x in c.get('creation',{}).get('objects',[])}
        boundary_match=None
        if c['translation']=={'tx':0,'ty':0} and c['label'].startswith(('flag_','clean_')):
            b=boundary_by_bits.get(c.get('center_y',{}).get('bits')); bo=objmap(b) if b else {}; boundary_match={'boundary_case':b.get('label') if b else None,'center_bits_equal':bool(b),'object_names_equal':set(objmap(c))==set(bo),'dto_equal':bool(b) and all(objmap(c)[n].get('dto')==bo[n].get('dto') for n in objmap(c))}
        rows.append({'label':c['label'],'translation':c['translation'],'center_y_bits':c.get('center_y',{}).get('bits'),'line_y_bits':c.get('line_y',{}).get('bits'),'full_clearance_fraction':str(clearance(c)),'full_clearance_decimal':str(float(clearance(c))),'stored_gate':c.get('audit_view',{}).get('gate_verdict'),'recomputed_gate':gate_check(c),'relative_fraction':rel,'boundary_match':boundary_match})
    deltas=[]
    for g,items in groups.items():
        base=items[(0,0)]; bm=objmap(base)
        for t,c in items.items():
            cm=objmap(c); diffs={}
            for name in bm:
                b= bm[name].get('actual_relative_fraction') or {}; q=cm[name].get('actual_relative_fraction') or {}; fd={}
                for k in set(b)|set(q):
                    if b.get(k)!=q.get(k): fd[k]={'base':b.get(k),'translated':q.get(k)}
                diffs[name]={'relative_fraction_equal':not fd,'relative_fraction_diff':fd,'dto_bits_equal':bm[name].get('dto')==cm[name].get('dto')}
            deltas.append({'group':g,'translation':{'tx':t[0],'ty':t[1]},'clearance_delta_from_T0_fraction':str(clearance(c)-clearance(base)),'objects':diffs})
    reopen=json.loads(REOPEN.read_text()); reopen_rows=[]
    for c in reopen['cases']:
        rr=c.get('reopen',{}); objs=rr.get('objects',[]); gd={'settings':c.get('settings',{}),'drc':c.get('drc',{}),'creation':{'arc_requery':next((x.get('after_dto') for x in objs if x.get('name')=='arcA'),None),'line_requery':next((x.get('after_dto') for x in objs if x.get('name')=='lineB'),None)}}
        reopen_rows.append({'label':c['label'],'status':c.get('status'),'stored_gate_verdict':c.get('gate_verdict'),'recomputed_gate':gate_check(gd),'all_unique':rr.get('all_unique'),'all_fields_equal':rr.get('all_fields_equal'),'objects':objs})
    t0={r['label'].split('_T')[0]:r.get('boundary_match') for r in rows if r['translation']=={'tx':0,'ty':0} and r['label'].startswith(('flag_','clean_'))}
    out={'source':str(RUN),'cases':rows,'translation_deltas':deltas,'reopen_source':str(REOPEN),'reopen_cases':reopen_rows,'conclusions':{'T0_boundary_match':t0,'transport_effect_is_not_comparator_inference':True,'scope':'bits-to-Fraction offline audit; no new DRC/epsilon claim'}}
    OUT.mkdir(parents=True,exist_ok=True); (OUT/'stage3_translation_analysis_v2.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8'); print(json.dumps({'cases':len(rows),'reopen_cases':len(reopen_rows),'out':str(OUT/'stage3_translation_analysis_v2.json')}))
if __name__=='__main__': main()
