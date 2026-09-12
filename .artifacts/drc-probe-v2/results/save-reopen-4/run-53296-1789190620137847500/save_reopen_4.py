from __future__ import annotations
import hashlib,json,os,socket,sys,time
from pathlib import Path
from shutil import copy2
from allegrobridge import Allegro,SkillCode,Symbol
from allegrobridge.util import ASSETS_DIR
ROOT=Path(__file__).resolve().parent; SRC=ASSETS_DIR/'route'/'EL5_MIAN_FPC.brd'; LAYER='ETCH/TOP'
CASES=['d0_s1_b1','d0_s1_b4','d3_s2_b1','d3_s2_b4']
def bits(x):
 import struct; return struct.pack('>d',float(x)).hex()
def p(v):
 if hasattr(v,'location'): v=v.location
 return (float(v.x),float(v.y)) if hasattr(v,'x') else (float(v[0]),float(v[1]))
def wire(x):
 x=float(x);s=format(x,'.17g');s=s if any(c in s for c in '.eE') else s+'.0';return {'value':x,'%.17g':s,'bits':bits(x)}
def js(v):
 if hasattr(v,'model_dump'): return js(v.model_dump(mode='python'))
 if isinstance(v,dict): return {str(k):js(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)): return [js(x) for x in v]
 if isinstance(v,float): return wire(v)
 return v
def fld(v,n): return v[n] if isinstance(v,dict) else v[v.index(n)+1]
def main():
 os.environ.setdefault('CDSROOT',r'D:\Cadence\Cadence_SPB_17.2-2016');os.environ.setdefault('Sigrity_EDA_DIR',r'D:\Cadence\Cadence_SPB_17.2-2016');os.environ.setdefault('CDS_LIC_FILE','5280@localhost')
 srcjson=ROOT/'results'/'ib-center-40'/'run-66284-1789189802536493400'/'cases.jsonl'; rows={json.loads(x)['label']:json.loads(x) for x in srcjson.read_text(encoding='utf-8').splitlines() if json.loads(x)['label'] in CASES}
 out=ROOT/'results'/'save-reopen-4'/f'run-{os.getpid()}-{time.time_ns()}';out.mkdir(parents=True);(out/'save_reopen_4.py').write_bytes(Path(__file__).read_bytes());(out/'stage1_smoke.il').write_bytes((ROOT/'stage1_smoke.il').read_bytes());(out/'stage1_smoke.py').write_bytes((ROOT/'stage1_smoke.py').read_bytes())
 report={'status':'RUNNING','run_dir':str(out),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'cases':[],'argv':sys.argv[:],'cwd':str(out)};os.chdir(out);outer=ROOT/'save_reopen_outer_stdout.log';
 for label in CASES:
  r=rows[label]; case={'label':label,'command':r['command'],'intent_H':r.get('H'),'creation':{},'save':{},'reopen':{}}; board=Path(copy2(SRC,out/f'{label}-initial.brd'));saved=out/f'{label}-saved.brd';
  def port():
   with socket.socket() as s:s.bind(('localhost',0));return str(s.getsockname()[1])
  p1=port();os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']=str(out/f'{label}-p1');Path(os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']).mkdir()
  try:
   with Allegro.open(mode='cli',board=board,workspace_id=p1,timeout=300.0) as op:
    ws,session=op.workspace,op.session;case['creation'].update({'pid':op._runtime.process.pid,'port':p1,'version':js(ws['axlVersion'](Symbol('fullVersion'))),'units_accuracy':js(ws['axlDBGetDesignUnits']())});ws['load']((out/'stage1_smoke.il').resolve().as_posix());before=len(session.routes(net=None,layer=LAYER));raw=ws.transaction(SkillCode(r['command']));session.refresh();case['creation']['transaction_return']=js(raw);case['creation']['before_routes']=before;case['creation']['after_routes']=len(session.routes(net=None,layer=LAYER));
    result=fld(raw,'committed');st=fld(result,'start');en=fld(result,'end');exp=((float(fld(st,'x')),float(fld(st,'y'))),(float(fld(en,'x')),float(fld(en,'y'))));hits=[x for x in session.routes(net=None,layer=LAYER) if x.obj_type=='arc' and p(x.start)==exp[0] and p(x.end)==exp[1]];case['creation']['requery_count']=len(hits);case['creation']['requery']=js(hits[0]) if len(hits)==1 else None;case['creation']['valid']=len(hits)==1
    saved_result=ws['axlSaveDesign'](design=saved.resolve().as_posix(),noMru=True,noConfirm=True);case['save']={'return':js(saved_result),'exists':saved.exists(),'sha256':hashlib.sha256(saved.read_bytes()).hexdigest() if saved.exists() else None,'source_hash_unchanged':hashlib.sha256(SRC.read_bytes()).hexdigest()==report['source_sha256']};case['save']['ok']=bool(saved_result) and saved.exists()
  except Exception as e:case['creation']['error']=repr(e)
  p2=port();os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']=str(out/f'{label}-p2');Path(os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']).mkdir()
  if saved.exists():
   try:
    with Allegro.open(mode='cli',board=saved,workspace_id=p2,timeout=300.0) as op2:
     ws2,s2=op2.workspace,op2.session;case['reopen'].update({'pid':op2._runtime.process.pid,'port':p2,'version':js(ws2['axlVersion'](Symbol('fullVersion'))),'units_accuracy':js(ws2['axlDBGetDesignUnits']())});rs=[x for x in s2.routes(net=None,layer=LAYER) if x.obj_type=='arc'];case['reopen']['routes_count']=len(rs);case['reopen']['matches']=[js(x) for x in rs if x.start is not None];case['reopen']['ok']=len(rs)>0
   except Exception as e:case['reopen']['error']=repr(e)
  case['status']='PASS' if case['creation'].get('valid') and case['save'].get('ok') and case['reopen'].get('ok') else 'FAILED';report['cases'].append(case);(out/'cases.jsonl').open('a',encoding='utf-8').write(json.dumps(case,default=repr)+'\n');(out/'manifest.json').write_text(json.dumps(report,indent=2,default=repr),encoding='utf-8')
 report['status']='PASS' if len(report['cases'])==4 and all(x['status']=='PASS' for x in report['cases']) else 'FAILED';(out/'manifest.json').write_text(json.dumps(report,indent=2,default=repr),encoding='utf-8');print(json.dumps({'status':report['status'],'run_dir':str(out),'cases':len(report['cases'])}));return 0 if report['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
