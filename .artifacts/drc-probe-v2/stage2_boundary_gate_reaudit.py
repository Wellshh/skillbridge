import json,hashlib,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parent; B=ROOT/'results'/'stage2-boundary'/'run-33608-1789226631112365500'; R=ROOT/'results'/'stage2-boundary-repeat'/'run-73320-1789227627605277800'; OUT=ROOT/'results'/'stage2-boundary'/'gate-reaudit'; OUT.mkdir(parents=True,exist_ok=True)
sp=importlib.util.spec_from_file_location('bg',B/'boundary_gate.py'); bg=importlib.util.module_from_spec(sp); sp.loader.exec_module(bg)
def load(d): return [json.loads(x) for x in (d/'cases.jsonl').read_text().splitlines() if x.strip()]
def audit(c):
    objs=c['creation']['objects']; gd={'settings':dict(c['settings'],context=c['creation']['context'],drcEnable_after=c['settings']['master_after']),'drc':dict(c['drc'],waived_after=c['settings']['waived_after']),'creation':{'arc_requery':next(o['dto'] for o in objs if o['name']=='arcA'),'line_requery':next(o['dto'] for o in objs if o['name']=='lineB')}}
    return bg.gate(gd)
def main():
    b,r=load(B),load(R); rows=[]
    for c in b+r:
        v,e=audit(c); rows.append({'label':c['label'] if 'label' in c else c['tag'],'cy_bits':c.get('cy',{}).get('bits'),'gate_reaudit':v,'gate_evidence':e,'raw_verdict':c.get('gate_verdict'),'match':v==c.get('gate_verdict'),'geometry_sha256':hashlib.sha256(json.dumps([(o.get('name'),o.get('dto')) for o in c['creation']['objects']],sort_keys=True,default=repr).encode()).hexdigest(),'pid':c.get('process',{}).get('pid'),'port':c.get('process',{}).get('port'),'poll':c.get('process_poll')})
    groups={}
    for x in rows[11:]: groups.setdefault((x['cy_bits'],x['gate_reaudit']),[]).append(x)
    repeat_ok=len(rows)==21 and len(groups)==2 and all(len(v)==5 and len({x['geometry_sha256'] for x in v})==1 and len({x['gate_reaudit'] for x in v})==1 for v in groups.values()) and len({x['pid'] for x in rows[11:]})==10 and len({x['port'] for x in rows[11:]})==10 and all(x['poll'] is not None for x in rows[11:])
    result={'status':'GATE_REAUDIT_PASS' if len(rows)==21 and all(x['match'] for x in rows) and repeat_ok else 'GATE_REAUDIT_FAIL','boundary_manifest_sha256':hashlib.sha256((B/'manifest.json').read_bytes()).hexdigest(),'repeat_manifest_sha256':hashlib.sha256((R/'manifest.json').read_bytes()).hexdigest(),'boundary_gate_sha256':hashlib.sha256((B/'boundary_gate.py').read_bytes()).hexdigest(),'repeat_group_check':repeat_ok,'cases':rows}
    (OUT/'audit.json').write_text(json.dumps(result,indent=2),encoding='utf8'); print(json.dumps({'status':result['status'],'path':str(OUT/'audit.json')})); return 0 if result['status']=='GATE_REAUDIT_PASS' else 1
if __name__=='__main__': raise SystemExit(main())
