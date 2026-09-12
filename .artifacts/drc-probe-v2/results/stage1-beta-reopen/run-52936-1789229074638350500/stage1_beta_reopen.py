from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, socket, struct, sys, time, traceback
from pathlib import Path
from shutil import copy2
from allegrobridge import Allegro, Symbol
from allegrobridge.util import ASSETS_DIR

ROOT=Path(__file__).resolve().parent; LAYER='ETCH/TOP'
def bits(x): return struct.pack('>d',float(x)).hex()
def scalar(x):
 if isinstance(x,dict) and 'bits' in x: return struct.unpack('>d',bytes.fromhex(x['bits']))[0]
 if isinstance(x,dict) and 'value' in x: return scalar(x['value'])
 return float(x)
def point(x): return (scalar(x['x']),scalar(x['y'])) if isinstance(x,dict) else (scalar(x[0]),scalar(x[1]))
def js(x):
 if hasattr(x,'model_dump'): return js(x.model_dump(mode='python'))
 if isinstance(x,dict): return {str(k):js(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)): return [js(v) for v in x]
 if isinstance(x,float):
  s=format(x,'.17g'); return {'value':x,'bits':bits(x),'%.17g':s if any(c in s for c in '.eE') else s+'.0'}
 return x
def fld(x,n): return x[n] if isinstance(x,dict) else x[x.index(n)+1]
def p(x): return (float(x.x),float(x.y)) if hasattr(x,'x') else tuple(float(v) for v in x)
def port():
 with socket.socket() as s: s.bind(('localhost',0)); return str(s.getsockname()[1])
def raw(ws,name,*args):
 try: return {'ok':True,'value':js(ws[name](*args))}
 except Exception: return {'ok':False,'traceback':traceback.format_exc()}
def unique(session,obj):
 dto=obj['dto']; net=dto.get('net'); net=net.get('name') if isinstance(net,dict) else net; kind=dto.get('obj_type','via')
 if kind=='via':
  xy=(scalar(dto['x']),scalar(dto['y'])); return [v for v in session.vias(net=net,layer=LAYER) if p(v)==xy]
 st,en=point(dto['start']),point(dto['end']); return [r for r in session.routes(net=net,layer=LAYER) if getattr(r,'obj_type',None)==kind and p(r.start)==st and p(r.end)==en]
def main():
 os.environ.setdefault('CDSROOT',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('Sigrity_EDA_DIR',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('CDS_LIC_FILE','5280@localhost')
 ap=argparse.ArgumentParser(); ap.add_argument('--manifest',required=True); a=ap.parse_args(); mp=Path(a.manifest).resolve(); src=json.loads(mp.read_text(encoding='utf8')); base=mp.parent
 out=ROOT/'results'/'stage1-beta-reopen'/f'run-{os.getpid()}-{time.time_ns()}'; out.mkdir(parents=True); snap=ROOT/'results'/'stage2-sweep-diag'/'run-63160-1789225091207869200'; files=[('stage1_beta_reopen.py',Path(__file__)),('stage1_smoke.il',snap/'stage1_smoke.il'),('stage0_gate.il',snap/'stage0_gate.il'),('context_probe.il',snap/'context_probe.il'),('stage2_sweep_diag.il',snap/'stage2_sweep_diag.il'),('stage1_smoke.py',snap/'stage1_smoke.py'),('boundary_gate.py',ROOT/'boundary_gate.py')]; [ (out/n).write_bytes(q.read_bytes()) for n,q in files]; os.chdir(out)
 rep={'status':'RUNNING','run_dir':str(out),'argv':sys.argv[:],'cwd':os.getcwd(),'input_manifest':str(mp),'cases':[]}
 for source_case in src.get('cases',[]):
  label=source_case.get('label')
  if label not in ('minus','plus'): continue
  save=source_case.get('save',{}); saved=Path(save.get('path','')); row={'label':label,'saved_path':str(saved),'saved_exists':saved.is_file(),'saved_hash':hashlib.sha256(saved.read_bytes()).hexdigest() if saved.is_file() else None,'reopen':{},'drc':{}}; opened=None
  try:
   if label not in ('minus','plus') or not saved.exists(): raise RuntimeError('missing requested minus/plus saved board')
   board=Path(copy2(saved,out/f'{label}.brd')); row['copy_hash']=hashlib.sha256(board.read_bytes()).hexdigest(); p1=port(); cdir=out/label; cdir.mkdir(); os.chdir(cdir); os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']=str(cdir)
   with Allegro.open(mode='cli',board=board,workspace_id=p1,timeout=300) as opened:
    ws,s=opened.workspace,opened.session
    for f in ('stage1_smoke.il','stage0_gate.il','context_probe.il','stage2_sweep_diag.il'): ws['load']((out/f).resolve().as_posix())
    spec=importlib.util.spec_from_file_location('smoke_snapshot',out/'stage1_smoke.py'); smoke=importlib.util.module_from_spec(spec); spec.loader.exec_module(smoke); s.drc()
    row['process']={'pid':opened._runtime.process.pid,'port':p1,'cwd':os.getcwd(),'version':js(ws['axlVersion'](Symbol('fullVersion'))),'units_accuracy':js(ws['axlDBGetDesignUnits']())}
    after=[]; targets=[]; expected_saved={x.get('name'):x.get('after_dto') for x in save.get('objects',[])}
    for obj in source_case.get('creation',{}).get('objects',[]):
     hits=unique(s,obj); rec={'name':obj.get('name'),'count':len(hits),'before_dto':expected_saved.get(obj.get('name'),obj.get('dto')),'after_dto':js(hits[0]) if len(hits)==1 else None,'all_fields_equal':len(hits)==1 and expected_saved.get(obj.get('name'),obj.get('dto'))==js(hits[0])}; after.append(rec)
     if len(hits)!=1: raise RuntimeError(f"{obj.get('name')} unique count={len(hits)}")
     if getattr(hits[0],'obj_type',None) in ('arc','line'): targets.append((getattr(hits[0],'net',None),hits[0]))
    row['reopen']={'objects':after,'all_unique':len(after)==4,'all_fields_equal':all(x['all_fields_equal'] for x in after)}
    row['settings']={'context':raw(ws,'__v2DrcContextPure','NFC_SWP','FINGER_SPI_MISO'),'drcEnable_before':raw(ws,'axlDBControl',Symbol('drcEnable')),'waived_before':raw(ws,'axlDRCWaiveGetCount'),'spacing_line_line_numeric':raw(ws,'axlCNSGetSpacing','', 'TOP', Symbol('line_line'), None),'spacing_line_line_string':raw(ws,'axlCNSGetSpacing','', 'TOP', Symbol('line_line'), True),'spacing_mode_all':raw(ws,'axlCNSSpacingModeGet',Symbol('all')),'design_mode_all':raw(ws,'axlCNSDesignModeGet',Symbol('all'))}
    row['drc']['item_calls']=[]
    for net,r in targets:
     args=('route',net,None,r.layer,r.obj_type,r.start,r.end,float(r.width),r.radius,r.is_clockwise,r.center); row['drc']['item_calls'].append({'net':net,'first':raw(ws,'__v2DiagItem',*args),'second':raw(ws,'__v2DiagItem',*args)})
    row['drc']['snapshot_before']=raw(ws,'__v2DiagSnapshot'); row['drc']['full_update']=raw(ws,'axlDRCUpdate',True); row['drc']['snapshot_after']=raw(ws,'__v2DiagSnapshot'); row['settings']['drcEnable_after']=raw(ws,'axlDBControl',Symbol('drcEnable')); row['settings']['waived_after']=raw(ws,'axlDRCWaiveGetCount'); row['drc']['waived_after']=row['settings']['waived_after']
    gate_spec=importlib.util.spec_from_file_location('boundary_gate_snapshot',out/'boundary_gate.py'); gm=importlib.util.module_from_spec(gate_spec); gate_spec.loader.exec_module(gm); gd={'settings':row['settings'],'drc':row['drc'],'creation':{'arc_requery':next(x['after_dto'] for x in after if x['name']=='arcA'),'line_requery':next(x['after_dto'] for x in after if x['name']=='lineB')}}; row['gate_verdict'],row['gate_evidence']=gm.gate(gd); row['status']='CAPTURED' if row['gate_verdict'] in ('FLAGGED','CLEAN') else 'INCOMPLETE'
  except Exception: row['status']='INCOMPLETE'; row['traceback']=traceback.format_exc()
  row['process_poll']=None if opened is None else opened._runtime.process.poll(); rep['cases'].append(row); (out/'cases.jsonl').open('a',encoding='utf8').write(json.dumps(row,default=repr)+chr(10)); (out/'manifest.json').write_text(json.dumps(rep,indent=2,default=repr),encoding='utf8')
 rep['status']='CAPTURED' if len(rep['cases'])==2 and all(x['status']=='CAPTURED' for x in rep['cases']) else 'INCOMPLETE'; (out/'manifest.json').write_text(json.dumps(rep,indent=2,default=repr),encoding='utf8'); print(json.dumps({'status':rep['status'],'run_dir':str(out)})); return 0 if rep['status']=='CAPTURED' else 1
if __name__=='__main__': raise SystemExit(main())
