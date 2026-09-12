"""I-B off-grid arc ordering probe (source only; runtime is separately authorized)."""
from __future__ import annotations
import hashlib, json, os, socket, struct, sys, time, traceback
from fractions import Fraction
from pathlib import Path
from shutil import copy2
from allegrobridge import Allegro, SkillCode, Symbol
from allegrobridge.util import ASSETS_DIR

ROOT=Path(__file__).resolve().parent; SNAP=ROOT/'results'/'ib-alpha-36'/'run-11788-1789189996641797000'
LAYER='ETCH/TOP'; NET='NFC_SWP'; W=.15; S=(Fraction(-620),Fraction(-70)); DELTA=(Fraction(49,1000000),Fraction(19,1000000))
DIRS=((Fraction(1),Fraction(0)),(Fraction(0),Fraction(1)),(Fraction(1),Fraction(1)),(Fraction(7,10),Fraction(11,10)))
VALUES=[(f'd{di}_s{scale}_sign{sign}',d,scale,sign) for di,d in enumerate(DIRS) for scale in (1,2) for sign in (-1,1)]
def bits(x): return struct.pack('>d',float(x)).hex()
def wire(x):
 f=float(x); s=format(f,'.17g'); return {'value':f,'%.17g':s if any(c in s for c in '.eE') else s+'.0','bits':bits(f)}
def js(x):
 if hasattr(x,'model_dump'): return js(x.model_dump(mode='python'))
 if isinstance(x,dict): return {str(k):js(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)): return [js(v) for v in x]
 if isinstance(x,float): return wire(x)
 return x
def fld(x,n): return x[n] if isinstance(x,dict) else x[x.index(n)+1]
def pt(x): return (float(x.x),float(x.y)) if hasattr(x,'x') else (float(x[0]),float(x[1]))
def sn(x):
 s=format(float(x),'.17g'); return s if any(c in s for c in '.eE') else s+'.0'
def fingerprint(session):
 rows=[js(x) for x in session.routes(net=None,layer=LAYER)]+[js(x) for x in session.vias(net=None,layer=LAYER)]
 payload=json.dumps(rows,sort_keys=True,separators=(',',':')); return {'sha256':hashlib.sha256(payload.encode()).hexdigest(),'count':len(rows),'rows':rows}
def cmd(a,e,c): return f"__v2Stage1Create('arc \"{NET}\" \"{LAYER}\" nil {sn(a[0])}:{sn(a[1])} {sn(e[0])}:{sn(e[1])} {sn(W)} nil {sn(c[0])}:{sn(c[1])})"
def intent(d,scale,sign):
 dx,dy=d[0]*scale,d[1]*scale; e=(S[0]+dx+sign*DELTA[0],S[1]+dy+sign*DELTA[1]); v=(e[0]-S[0],e[1]-S[1]); m=((S[0]+e[0])/2,(S[1]+e[1])/2); c=(m[0]+Fraction(3,8)*(-v[1]),m[1]+Fraction(3,8)*v[0]); return e,c
def main():
 ap=__import__('argparse').ArgumentParser(); ap.add_argument('--run-dir',type=Path,required=True); base=ap.parse_args().run_dir.resolve(); base.mkdir(parents=True,exist_ok=False); os.chdir(base)
 source=ASSETS_DIR/'route'/'EL5_MIAN_FPC.brd'; board=Path(copy2(source,base/'EL5_MIAN_FPC.brd')); helper=SNAP/'stage1_smoke.il'; helper_py=SNAP/'stage1_smoke.py'; copy2(helper,base/'stage1_smoke.il'); copy2(helper_py,base/'stage1_smoke.py'); copy2(Path(__file__),base/'stage1_offgrid_order.py')
 with socket.socket() as s: s.bind(('localhost',0)); port=str(s.getsockname()[1])
 os.environ.setdefault('CDSROOT',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('Sigrity_EDA_DIR',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('CDS_LIC_FILE','5280@localhost'); os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']=str(base/'bridge-logs'); (base/'bridge-logs').mkdir()
 rep={'status':'RUNNING','run_dir':str(base),'argv':sys.argv,'cwd':str(base),'board_sha256':hashlib.sha256(board.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256((base/'stage1_smoke.il').read_bytes()).hexdigest(),'helper_py_sha256':hashlib.sha256((base/'stage1_smoke.py').read_bytes()).hexdigest(),'cases':[]}
 opened=None
 try:
  with Allegro.open(mode='cli',board=board,workspace_id=port,timeout=300.0) as op:
   opened=op; ws,session=op.workspace,op.session; rep['process']={'pid':op._runtime.process.pid,'port':port,'version':js(ws['axlVersion'](Symbol('fullVersion'))),'units_accuracy':js(ws['axlDBGetDesignUnits']())}; ws['load']((base/'stage1_smoke.il').as_posix()); spec=__import__('importlib.util').util.spec_from_file_location('smoke',base/'stage1_smoke.py'); smoke=__import__('importlib.util').util.module_from_spec(spec); spec.loader.exec_module(smoke); session.drc(); session.refresh()
   baseline=fingerprint(session)
   for i,(label,d,scale,sign) in enumerate(VALUES):
    e,c=intent(d,scale,sign); rec={'index':i,'label':label,'intent_fraction':{'direction':[str(d[0]),str(d[1])],'scale':scale,'sign':sign,'start':[str(x) for x in S],'end':[str(x) for x in e],'center':[str(x) for x in c]},'input':{'start':[wire(x) for x in S],'end':[wire(x) for x in e],'center':[wire(x) for x in c],'width':wire(W)},'initial_fingerprint':{'sha256':baseline['sha256'],'count':baseline['count']}}
    try:
     command=cmd(S,e,c); rec['command']=command; raw=ws.transaction(SkillCode(command)); rec['transaction_return']=js(raw); inputs={'start':[wire(x) for x in S],'end':[wire(x) for x in e],'center':[wire(x) for x in c],'width':wire(W)}; smoke.assert_request_wire(command,inputs); smoke.assert_echo_inputs('arc',raw,inputs); session.refresh(); n=fld(raw,'committed'); st,en=fld(n,'start'),fld(n,'end'); actual_net=fld(n,'net'); hits=[r for r in session.routes(net=None,layer=LAYER) if r.net==actual_net and r.obj_type=='arc' and pt(r.start)==(float(fld(st,'x')),float(fld(st,'y'))) and pt(r.end)==(float(fld(en,'x')),float(fld(en,'y')))]; rec['committed_net']=actual_net; rec['requery_count']=len(hits); rec['requery']=js(hits[0]) if len(hits)==1 else None; 
     if len(hits)!=1: raise RuntimeError(f'requery expected one row, got {len(hits)}')
     smoke.assert_requery_bits('arc',raw,hits[0]); rec['status']='PASS'
    except Exception as exc: rec['status']='FAILED'; rec['error']=repr(exc); rec['traceback']=traceback.format_exc()
    rep['cases'].append(rec); ws['axlOpenDesignForBatch'](board.as_posix(),'wf'); session.refresh(); after_reset=fingerprint(session); rec['reset_fingerprint']={'sha256':after_reset['sha256'],'count':after_reset['count'],'matches_initial':after_reset['sha256']==baseline['sha256'] and after_reset['count']==baseline['count']}; (base/'cases.jsonl').open('a',encoding='utf8').write(json.dumps(rec)+'\n')
 except Exception as exc: rep['error']=repr(exc); rep['traceback']=traceback.format_exc()
 rep['process_poll_after_context']=None if opened is None else opened._runtime.process.poll(); rep['status']='PASS' if len(rep['cases'])==16 and all(c['status']=='PASS' for c in rep['cases']) else 'FAILED'; (base/'manifest.json').write_text(json.dumps(rep,indent=2),encoding='utf8'); return 0 if rep['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
