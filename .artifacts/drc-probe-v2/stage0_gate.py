from __future__ import annotations
import hashlib,json,os,socket,struct,sys,time,traceback
from pathlib import Path
from shutil import copy2
from allegrobridge import Allegro,SkillCode,Symbol
from allegrobridge.util import ASSETS_DIR
ROOT=Path(__file__).resolve().parent; SRC=ASSETS_DIR/'route'/'EL5_MIAN_FPC.brd'; LAYER='ETCH/TOP'; WA=0.15; A='NFC_SWP'; B='FINGER_SPI_MISO'
def bits(x): return struct.pack('>d',float(x)).hex()
def wire(x):
 x=float(x); s=format(x,'.17g'); return {'value':x,'%.17g':s if any(c in s for c in '.eE') else s+'.0','bits':bits(x)}
def js(v):
 if hasattr(v,'model_dump'): return js(v.model_dump(mode='python'))
 if isinstance(v,dict): return {str(k):js(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)): return [js(x) for x in v]
 if isinstance(v,float): return wire(v)
 return v
def fld(v,n): return v[n] if isinstance(v,dict) else v[v.index(n)+1]
def pt(v): return (float(v.x),float(v.y)) if hasattr(v,'x') else tuple(float(x) for x in v)
def port():
 with socket.socket() as s: s.bind(('localhost',0)); return str(s.getsockname()[1])
def raw(ws,name,*args):
 try:return {'ok':True,'value':js(ws[name](*args))}
 except Exception:return {'ok':False,'traceback':traceback.format_exc()}
def sn(x):
 s=format(float(x),'.17g'); return s if any(c in s for c in '.eE') else s+'.0'
def linecmd(net,s,e): return f'__v2Stage1Create(\'line "{net}" "{LAYER}" nil {sn(s[0])}:{sn(s[1])} {sn(e[0])}:{sn(e[1])} {sn(WA)} nil nil)'
def viacmd(net,xy,pad): return f'__v2Stage1Create(\'via "{net}" "{LAYER}" "{pad}" {sn(xy[0])}:{sn(xy[1])} nil {sn(WA)} nil nil)'
def routehit(session,net,s,e): return [r for r in session.routes(net=net,layer=LAYER) if r.obj_type=='line' and pt(r.start)==s and pt(r.end)==e]
def viahit(session,net,xy): return [v for v in session.vias(net=net,layer=LAYER) if pt(v)==xy]
def main():
 os.environ.setdefault('CDSROOT',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('Sigrity_EDA_DIR',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('CDS_LIC_FILE','5280@localhost')
 root=ROOT/'results'/'stage0-gate'; out=root/f'run-{os.getpid()}-{time.time_ns()}'; out.mkdir(parents=True)
 helper=ROOT/'stage1_smoke.il'; drc=ROOT/'stage0_gate.il'; (out/'stage0_gate.py').write_bytes(Path(__file__).read_bytes()); (out/'stage1_smoke.il').write_bytes(helper.read_bytes()); (out/'stage0_gate.il').write_bytes(drc.read_bytes()); (out/'context_probe.il').write_bytes((ROOT/'context_probe.il').read_bytes()); (out/'stage1_smoke.py').write_bytes((ROOT/'stage1_smoke.py').read_bytes()); os.chdir(out)
 rep={'status':'RUNNING','run_dir':str(out),'argv':sys.argv[:],'cwd':os.getcwd(),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),'drc_helper_sha256':hashlib.sha256(drc.read_bytes()).hexdigest(),'cases':[]}
 (out/'manifest.json').write_text(json.dumps(rep,indent=2))
 for label,sep in [('POS_NOMINAL_VIOLATION',0.19),('CLEAR_NOMINAL',0.35)]:
  case={'label':label,'sep':wire(sep),'intended_copper_gap':wire(sep-WA),'creation':{},'drc':{},'settings':{}}; board=Path(copy2(SRC,out/f'{label}.brd')); p1=port(); wd=out/label; wd.mkdir(); os.chdir(wd); os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']=str(wd); opened=None
  try:
   with Allegro.open(mode='cli',board=board,workspace_id=p1,timeout=300) as opened:
    ws,s=opened.workspace,opened.session; case['process']={'pid':opened._runtime.process.pid,'port':p1,'cwd':os.getcwd(),'version':js(ws['axlVersion'](Symbol('fullVersion'))),'units_accuracy':js(ws['axlDBGetDesignUnits']())}; ws['load']((out/'stage1_smoke.il').resolve().as_posix()); ws['load']((out/'stage0_gate.il').resolve().as_posix()); ws['load']((out/'context_probe.il').resolve().as_posix()); case['drc']['session_drc_init']=js(s.drc()); case['settings']['native_context']=raw(ws,'__v2DrcContextPure',A,B)
    vias=s.vias(); pad=sorted([v.padstack for v in vias])[0]; va=(-622.,-70.); vb=(-608.,-70.+sep); ea=(-610.,-70.); eb=(-620.,-70.+sep)
    objs=[('via',A,va,None,viacmd(A,va,pad)),('line',A,va,ea,linecmd(A,va,ea)),('via',B,vb,None,viacmd(B,vb,pad)),('line',B,vb,eb,linecmd(B,vb,eb))]
    natives=[]; line_targets=[]
    for kind,net,st,en,cmd in objs:
     rawv=ws.transaction(SkillCode(cmd)); natives.append((kind,net,st,en,rawv)); rec={'kind':kind,'net':net,'command':cmd,'return':js(rawv)}; s.refresh()
     if kind=='via': hit=viahit(s,net,st); inputs={'start':[wire(st[0]),wire(st[1])],'end':None,'width':wire(WA),'center':None};
     else: hit=routehit(s,net,st,en); inputs={'start':[wire(st[0]),wire(st[1])],'end':[wire(en[0]),wire(en[1])],'width':wire(WA),'center':None}
     import stage1_smoke as smoke; smoke.assert_echo_inputs(kind,rawv,inputs); rec['echo_assert']=True; rec['hit_count']=len(hit); rec['dto']=js(hit[0]) if len(hit)==1 else None; 
     if len(hit)!=1: raise RuntimeError(f'{kind} {net} unique hit={len(hit)}')
     if kind=='line': line_targets.append((net,hit[0]))
     smoke.assert_requery_bits(kind,rawv,hit[0]); rec['requery_bits_assert']=True; case['creation'].setdefault('objects',[]).append(rec)
    case['settings']['drcEnable_before']=raw(ws,'axlDBControl',Symbol('drcEnable')); case['settings']['drc_count_before']=raw(ws,'axlDRCGetCount'); case['settings']['waived_before']=raw(ws,'axlDRCWaiveGetCount'); case['settings']['spacing_default']=raw(ws,'axlCNSGetSpacing','DEFAULT','TOP',None,True); case['settings']['spacing_line_line_default']=raw(ws,'axlCNSGetSpacing','', 'TOP', Symbol('line_line'), None); case['settings']['spacing_line_line_all']=raw(ws,'axlCNSGetSpacing','', 'TOP', Symbol('line_line'), True); case['settings']['spacing_mode_all']=raw(ws,'axlCNSSpacingModeGet',Symbol('all')); case['settings']['design_mode_all']=raw(ws,'axlCNSDesignModeGet',Symbol('all'))
    case['drc']['snapshot_before']=raw(ws,'__v2DrcSnapshot'); case['drc']['item_calls']=[]
    for net,rline in line_targets:
     args=('route',net,None,LAYER,'line',pt(rline.start),pt(rline.end),float(rline.width),None,rline.is_clockwise,None); call1=raw(ws,'__v2DrcItemCount',*args); call2=raw(ws,'__v2DrcItemCount',*args); case['drc']['item_calls'].append({'net':net,'first':call1,'second':call2})
    case['drc']['full_update']=raw(ws,'axlDRCUpdate',True); case['drc']['snapshot_after']=raw(ws,'__v2DrcSnapshot'); case['drc']['count_after']=raw(ws,'axlDRCGetCount'); case['drc']['waived_after']=raw(ws,'axlDRCWaiveGetCount'); case['settings']['drcEnable_after']=raw(ws,'axlDBControl',Symbol('drcEnable')); case['status']='RAW_CAPTURED' if all(x.get('first',{}).get('ok') and x.get('second',{}).get('ok') and isinstance(x.get('first',{}).get('value'),dict) and x['first']['value'].get('resolved') is True and isinstance(x['first']['value'].get('count'),int) and isinstance(x['first']['value'].get('markers'),list) and x['first']['value'].get('count') == x.get('second',{}).get('value',{}).get('count') for x in case['drc'].get('item_calls',[])) and case['drc'].get('snapshot_before',{}).get('ok') and case['drc'].get('snapshot_after',{}).get('ok') and case['settings'].get('native_context',{}).get('ok') else 'INCOMPLETE'
  except Exception: case['status']='FAILED'; case['traceback']=traceback.format_exc()
  case['process_poll']=None if opened is None else opened._runtime.process.poll(); rep['cases'].append(case); (out/'cases.jsonl').open('a',encoding='utf-8').write(json.dumps(case,default=repr)+'\n'); (out/'manifest.json').write_text(json.dumps(rep,indent=2,default=repr),encoding='utf-8')
 rep['status']='COMPLETE_RAW' if len(rep['cases'])==2 and all(c['status']=='RAW_CAPTURED' for c in rep['cases']) else 'INCOMPLETE'; (out/'manifest.json').write_text(json.dumps(rep,indent=2,default=repr),encoding='utf-8'); print(json.dumps({'status':rep['status'],'run_dir':str(out),'cases':len(rep['cases'])})); return 0 if rep['status']=='COMPLETE_RAW' else 1
if __name__=='__main__': raise SystemExit(main())





















