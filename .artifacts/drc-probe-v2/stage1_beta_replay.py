"""I-B same-canonical beta replay source; runtime is separately reviewed."""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, socket, struct, sys, traceback
from pathlib import Path
from shutil import copy2
from allegrobridge import Allegro, SkillCode, Symbol
from allegrobridge.util import ASSETS_DIR

ROOT=Path(__file__).resolve().parent; SNAP=ROOT/'results'/'stage2-sweep-diag'/'run-63160-1789225091207869200'
SRC=ASSETS_DIR/'route'/'EL5_MIAN_FPC.brd'; LAYER='ETCH/TOP'; A='NFC_SWP'; B='FINGER_SPI_MISO'; PAD='VIA_ALL_0103'; W=.15; S=(-620.,-70.); E=(-619.,-70.)
CASES=(('minus',-.00001,-70.46,True),('plus',.00001,-70.46,True),('positive',-.00001,-70.44,False))
def bits(x): return struct.pack('>d',float(x)).hex()
def wire(x):
 f=float(x); t=format(f,'.17g'); return {'value':f,'%.17g':t if any(c in t for c in '.eE') else t+'.0','bits':bits(f)}
def js(x):
 if hasattr(x,'model_dump'): return js(x.model_dump(mode='python'))
 if isinstance(x,dict): return {str(k):js(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)): return [js(v) for v in x]
 if isinstance(x,float): return wire(x)
 return x
def fld(x,n): return x[n] if isinstance(x,dict) else x[x.index(n)+1]
def pt(x): return (float(x.x),float(x.y)) if hasattr(x,'x') else (float(x[0]),float(x[1]))
def sn(x):
 t=format(float(x),'.17g'); return t if any(c in t for c in '.eE') else t+'.0'
def ss(x): return '"'+x.replace('"','\\"')+'"'
def via(net,p): return f"__v2Stage1Create('via {ss(net)} {ss(LAYER)} {ss(PAD)} {sn(p[0])}:{sn(p[1])} nil {sn(W)} nil nil)"
def arc(beta):
 c=(S[0]+.5+beta,S[1]+.375); return f"__v2Stage1Create('arc {ss(A)} {ss(LAYER)} nil {sn(S[0])}:{sn(S[1])} {sn(E[0])}:{sn(E[1])} {sn(W)} nil {sn(c[0])}:{sn(c[1])})"
def line(y): return f"__v2Stage1Create('line {ss(B)} {ss(LAYER)} nil -620.0:{sn(y)} -619.0:{sn(y)} {sn(W)} nil nil)"
def raw(ws,n,*a):
 try:return {'ok':True,'value':js(ws[n](*a))}
 except Exception:return {'ok':False,'traceback':traceback.format_exc()}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--run-dir',type=Path,required=True); base=ap.parse_args().run_dir.resolve(); base.mkdir(parents=True,exist_ok=False); os.chdir(base)
 for n in ('stage1_smoke.py','stage1_smoke.il','stage0_gate.il','context_probe.il','stage2_sweep_diag.il'):
  copy2(SNAP/n,base/n)
 copy2(Path(__file__),base/'stage1_beta_replay.py');
 with socket.socket() as s:s.bind(('localhost',0)); port=str(s.getsockname()[1])
 os.environ.setdefault('CDSROOT',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('Sigrity_EDA_DIR',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('CDS_LIC_FILE','5280@localhost'); os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']=str(base/'bridge-logs'); (base/'bridge-logs').mkdir()
 rep={'status':'RUNNING','run_dir':str(base),'argv':sys.argv,'cwd':str(base),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'cases':[]}; opened=None
 try:
  with Allegro.open(mode='cli',board=Path(copy2(SRC,base/'working.brd')),workspace_id=port,timeout=300.) as op:
   opened=op; ws,se=op.workspace,op.session; rep['process']={'pid':op._runtime.process.pid,'port':port,'version':js(ws['axlVersion'](Symbol('fullVersion'))),'units_accuracy':js(ws['axlDBGetDesignUnits']())}
   for n in ('stage1_smoke.il','stage0_gate.il','context_probe.il','stage2_sweep_diag.il'): ws['load']((base/n).as_posix())
   se.drc(); spec=importlib.util.spec_from_file_location('smoke',base/'stage1_smoke.py'); smoke=importlib.util.module_from_spec(spec); spec.loader.exec_module(smoke)
   for label,beta,y,save in CASES:
    rec={'label':label,'beta':wire(beta),'line_y':wire(y),'objects':[],'drc':{}}; arc_dto=via_dto=None
    try:
     specs=(('viaA',via(A,S),A,'via',S),('arcA',arc(beta),A,'arc',S),('lineB',line(y),B,'line',(-620.,y)),('viaB',via(B,(-620.,y)),B,'via',(-620.,y)))
     for name,cmd,net,kind,xy in specs:
      ret=ws.transaction(SkillCode(cmd)); se.refresh(); n=fld(ret,'committed'); smoke.assert_echo_inputs(kind,ret,{'start':[wire(xy[0]),wire(xy[1])],'end':None if kind=='via' else [wire(E[0]),wire(E[1])],'width':wire(W),'center':None if kind!='arc' else [wire(S[0]+.5+beta),wire(S[1]+.375)]}); pool=se.vias(net=None,layer=LAYER) if kind=='via' else se.routes(net=None,layer=LAYER); hits=[r for r in pool if r.net==fld(n,'net') and ((kind=='via' and pt(r)==(float(fld(n,'x')),float(fld(n,'y')))) or (kind!='via' and r.obj_type==kind and pt(r.start)==(float(fld(n,'start')['x']['value']),float(fld(n,'start')['y']['value'])) and pt(r.end)==(float(fld(n,'end')['x']['value']),float(fld(n,'end')['y']['value']))))];
      if len(hits)!=1: raise RuntimeError(f'{name} requery={len(hits)}')
      smoke.assert_requery_bits(kind,ret,hits[0]); rec['objects'].append({'name':name,'command':cmd,'return':js(ret),'dto':js(hits[0])}); arc_dto=hits[0] if kind=='arc' else arc_dto; via_dto=hits[0] if name=='viaB' else via_dto
     args=('route',A,None,LAYER,'arc',arc_dto.start,arc_dto.end,float(arc_dto.width),arc_dto.radius,arc_dto.is_clockwise,arc_dto.center); rec['drc']={'diag1':raw(ws,'__v2DiagItem',*args),'diag2':raw(ws,'__v2DiagItem',*args),'snapshot1':raw(ws,'__v2DiagSnapshot'),'update':raw(ws,'axlDRCUpdate',True),'snapshot2':raw(ws,'__v2DiagSnapshot'),'context':raw(ws,'__v2DrcContextPure',A,B),'spacing':raw(ws,'axlCNSGetSpacing','', 'TOP', Symbol('via_line'), None),'waived':raw(ws,'axlDRCWaiveGetCount')}
     if save:
      saved=base/(label+'.brd'); rec['save']={'return':js(ws['axlSaveDesign'](design=saved.as_posix(),noMru=True,noConfirm=True)),'path':str(saved),'exists':saved.exists()}; se.refresh(); rec['post_save_query']=[js(x) for x in se.routes(net=None,layer=LAYER) if x.obj_type=='arc'];
      with Allegro.open(mode='cli',board=saved,workspace_id=str(int(port)+1),timeout=300.) as op2: op2.session.refresh(); rec['reopen_query']=[js(x) for x in op2.session.routes(net=None,layer=LAYER) if x.obj_type=='arc']; rec['reopen_drc']=raw(op2.workspace,'__v2DiagSnapshot')
     rec['status']='CAPTURED'
    except Exception: rec['status']='INCOMPLETE'; rec['error']=repr(sys.exc_info()[1]); rec['traceback']=traceback.format_exc()
    rep['cases'].append(rec); (base/'manifest.json').write_text(json.dumps(rep,indent=2),encoding='utf8')
 except Exception: rep['error']=repr(sys.exc_info()[1]); rep['traceback']=traceback.format_exc()
 rep['process_poll_after_context']=None if opened is None else opened._runtime.process.poll(); rep['status']='CAPTURED' if len(rep['cases'])==3 and all(x['status']=='CAPTURED' for x in rep['cases']) else 'INCOMPLETE'; (base/'manifest.json').write_text(json.dumps(rep,indent=2),encoding='utf8'); return 0 if rep['status']=='CAPTURED' else 1
if __name__=='__main__': raise SystemExit(main())
