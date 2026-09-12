import hashlib,json,os,socket,sys,time,traceback
from pathlib import Path
from shutil import copy2
from allegrobridge import Allegro,Symbol
from allegrobridge.util import ASSETS_DIR
ROOT=Path(__file__).resolve().parent; SRC=ASSETS_DIR/'route'/'EL5_MIAN_FPC.brd'
def js(v):
 if hasattr(v,'model_dump'): return js(v.model_dump(mode='python'))
 if isinstance(v,dict): return {str(k):js(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)): return [js(x) for x in v]
 return v
def main():
 os.environ.setdefault('CDSROOT',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('Sigrity_EDA_DIR',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('CDS_LIC_FILE','5280@localhost')
 out=ROOT/'results'/'context-probe'/f'run-{os.getpid()}-{time.time_ns()}'; out.mkdir(parents=True); board=Path(copy2(SRC,out/'board.brd')); helper=ROOT/'context_probe.il'; (out/'context_probe.py').write_bytes(Path(__file__).read_bytes()); (out/'context_probe.il').write_bytes(helper.read_bytes()); port=str((lambda s:(s.bind(('localhost',0)),s.getsockname()[1],s.close()))(socket.socket())[1]); os.chdir(out); os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']=str(out)
 rep={'run_dir':str(out),'argv':sys.argv[:],'cwd':os.getcwd(),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest()}
 try:
  with Allegro.open(mode='cli',board=board,workspace_id=port,timeout=300) as op:
   ws=op.workspace; rep['process']={'pid':op._runtime.process.pid,'port':port,'version':js(ws['axlVersion'](Symbol('fullVersion')))}; ws['load'](helper.resolve().as_posix()); v=js(ws['__v2DrcContextPure']('NFC_SWP','FINGER_SPI_MISO')); rep['context']=v; rep['valid']=isinstance(v,dict) and all(k in v for k in ('netA','netB','classTables')) and v.get('netA',{}).get('found') is True and v.get('netB',{}).get('found') is True
 except Exception: rep['error']=traceback.format_exc(); rep['valid']=False
 rep['process_poll']=op._runtime.process.poll() if 'op' in locals() else None; rep['status']='PASS' if rep.get('valid') else 'INCOMPLETE'; (out/'manifest.json').write_text(json.dumps(rep,indent=2,default=repr),encoding='utf8'); print(json.dumps({'status':rep['status'],'run_dir':str(out)})); return 0 if rep['valid'] else 1
if __name__=='__main__': raise SystemExit(main())

