from __future__ import annotations
import argparse,hashlib,json,os,socket,sys,time,traceback,importlib.util
from fractions import Fraction
from pathlib import Path
from shutil import copy2
from allegrobridge import Allegro,SkillCode,Symbol
from allegrobridge.util import ASSETS_DIR
ROOT=Path(__file__).resolve().parent; SRC=ASSETS_DIR/'route'/'EL5_MIAN_FPC.brd'; LAYER='ETCH/TOP'; W=.15; NET_A='NFC_SWP'; NET_B='FINGER_SPI_MISO'
BASE={'arc_start':(300.0,410.0),'arc_end':(302.0001,410.0),'arc_center_x':301.00005,'line_start':(300.0,408.9071),'line_end':(302.0,408.9071),'width':0.15}
TRANSLATIONS=[(0,0),(-300,-300),(-600,-500)]
def exact_point(pt,t): return (Fraction.from_float(float(pt[0]))+t[0],Fraction.from_float(float(pt[1]))+t[1])
def translated_float(value, offset): return float(Fraction.from_float(float(value))+Fraction(offset))
def relative_point(pt,tx,ty): return [str(Fraction.from_float(float(pt[0]))-tx),str(Fraction.from_float(float(pt[1]))-ty)]
def cases_from_args(flag_cy,clean_cy):
 if flag_cy is None or clean_cy is None: raise SystemExit('--flag-cy and --clean-cy are required; values come from boundary evidence')
 out=[]
 for cy_label,cy in [('flag',flag_cy),('clean',clean_cy),('control',410.10)]:
  for tx,ty in TRANSLATIONS:
   out.append({'label':f'{cy_label}_T{tx}_{ty}','tx':tx,'ty':ty,'cy':cy})
 return out
CASES=[]
def bits(x):
 import struct; return struct.pack('>d',float(x)).hex()
def wire(x):
 x=float(x); s=format(x,'.17g'); return {'value':x,'%.17g':s if any(c in s for c in '.eE') else s+'.0','bits':bits(x)}
def js(v):
 if hasattr(v,'model_dump'): return js(v.model_dump(mode='python'))
 if isinstance(v,dict): return {str(k):js(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)): return [js(x) for x in v]
 if isinstance(v,float): return wire(v)
 return v
def fld(v,n): return v[n] if isinstance(v,dict) else v[v.index(n)+1]
def p(v): return (float(v.x),float(v.y)) if hasattr(v,'x') else tuple(float(x) for x in v)
def ep(n):
 st,en=fld(n,'start'),fld(n,'end'); return ((float(fld(st,'x')),float(fld(st,'y'))),(float(fld(en,'x')),float(fld(en,'y'))))
def sn(x):
 s=format(float(x),'.17g'); return s if any(c in s for c in '.eE') else s+'.0'
def port():
 with socket.socket() as s: s.bind(('localhost',0)); return str(s.getsockname()[1])
def linecmd(net,s,e): return f'__v2Stage1Create(\'line "{net}" "{LAYER}" nil {sn(s[0])}:{sn(s[1])} {sn(e[0])}:{sn(e[1])} {sn(W)} nil nil)'
def arccmd(s,e,c,cw): return f'__v2Stage1Create(\'arc "{NET_A}" "{LAYER}" nil {sn(s[0])}:{sn(s[1])} {sn(e[0])}:{sn(e[1])} {sn(W)} {"t" if cw else "nil"} {sn(c[0])}:{sn(c[1])})'
def viacmd(net,pad,xy): return f'__v2Stage1Create(\'via "{net}" "{LAYER}" "{pad}" {sn(xy[0])}:{sn(xy[1])} nil {sn(W)} nil nil)'
def raw(ws,name,*args):
 try:return {'ok':True,'value':js(ws[name](*args))}
 except Exception:return {'ok':False,'traceback':traceback.format_exc()}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--flag-cy',type=float,required=True); ap.add_argument('--clean-cy',type=float,required=True); cli=ap.parse_args(); global CASES; CASES=cases_from_args(cli.flag_cy,cli.clean_cy)
 os.environ.setdefault('CDSROOT',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('Sigrity_EDA_DIR',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('CDS_LIC_FILE','5280@localhost')
 out=ROOT/'results'/'stage3-translation'/f'run-{os.getpid()}-{time.time_ns()}'; out.mkdir(parents=True); snap=ROOT/'results'/'stage0-gate'/'run-37248-1789193361092813400'; diag_snap=ROOT/'results'/'stage2-sweep-diag'/'run-63160-1789225091207869200'; helper=snap/'stage1_smoke.il'; drc=snap/'stage0_gate.il'; context=snap/'context_probe.il'; boundary=ROOT/'boundary_gate.py'; diag=diag_snap/'stage2_sweep_diag.il'; script=Path(__file__); [ (out/n).write_bytes(snapshot_source.read_bytes()) for n,snapshot_source in [('stage3_translation.py',script),('stage1_smoke.il',helper),('stage0_gate.il',drc),('context_probe.il',context),('stage2_sweep_diag.il',diag),('stage1_smoke.py',snap/'stage1_smoke.py'),('boundary_gate.py',boundary)]]; os.chdir(out); rep={'status':'RUNNING','run_dir':str(out),'argv':sys.argv[:],'cwd':os.getcwd(),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'boundary_gate_sha256':hashlib.sha256(boundary.read_bytes()).hexdigest(),'cases':[]}
 for case_spec in CASES:
  label=case_spec['label']; tx,ty,cy=case_spec['tx'],case_spec['ty'],case_spec['cy']; y=translated_float(cy,ty); cw=False
  board=Path(copy2(SRC,out/f'{label}.brd')); p1=port(); os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']=str(out/label); Path(os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']).mkdir(); os.chdir(out/label); case={'label':label,'line_y':wire(translated_float(408.9071,ty)),'center_y':wire(translated_float(cy,ty)),'clockwise':cw,'translation':{'tx':case_spec['tx'],'ty':case_spec['ty']},'intent_fraction':{'arc_start':list(exact_point(BASE['arc_start'],(case_spec['tx'],case_spec['ty']))),'arc_end':list(exact_point(BASE['arc_end'],(case_spec['tx'],case_spec['ty']))),'line_start':list(exact_point(BASE['line_start'],(case_spec['tx'],case_spec['ty']))),'line_end':list(exact_point(BASE['line_end'],(case_spec['tx'],case_spec['ty']))),'center_x':str(Fraction.from_float(float(BASE['arc_center_x']))+case_spec['tx']),'center_y':str(Fraction.from_float(float(case_spec['cy']))+case_spec['ty'])},'arc_intent':{'start':[wire(translated_float(300,tx)),wire(translated_float(410,ty))],'end':[wire(translated_float(302.0001,tx)),wire(translated_float(410,ty))],'center':[wire(translated_float(301.00005,tx)),wire(translated_float(cy,ty))],'width':wire(.15)},'creation':{},'drc':{}}; opened=None
  try:
   with Allegro.open(mode='cli',board=board,workspace_id=p1,timeout=300) as opened:
    ws,s=opened.workspace,opened.session; ws['load']((out/'stage1_smoke.il').resolve().as_posix()); ws['load']((out/'stage0_gate.il').resolve().as_posix()); ws['load']((out/'context_probe.il').resolve().as_posix()); ws['load']((out/'stage2_sweep_diag.il').resolve().as_posix()); import_spec=importlib.util.spec_from_file_location('stage1_smoke_snapshot',out/'stage1_smoke.py'); smoke=importlib.util.module_from_spec(import_spec); import_spec.loader.exec_module(smoke); s.drc(); pad='VIA_ALL_0103'; va=(translated_float(300,tx),translated_float(410,ty)); ae=(translated_float(302.0001,tx),translated_float(410,ty)); ac=(translated_float(301.00005,tx),translated_float(cy,ty)); vb=(translated_float(300,tx),translated_float(408.9071,ty)); be=(translated_float(302.0,tx),translated_float(408.9071,ty)); objs=[{'name':'viaA','kind':'via','net':NET_A,'start':va,'end':None,'center':None,'cw':None,'command':viacmd(NET_A,pad,va)}, {'name':'arcA','kind':'arc','net':NET_A,'start':va,'end':ae,'center':ac,'cw':cw,'command':arccmd(va,ae,ac,cw)}, {'name':'viaB','kind':'via','net':NET_B,'start':vb,'end':None,'center':None,'cw':None,'command':viacmd(NET_B,pad,vb)}, {'name':'lineB','kind':'line','net':NET_B,'start':vb,'end':be,'center':None,'cw':None,'command':linecmd(NET_B,vb,be)}]
    targets=[]
    for obj in objs:
     name,kind,net,st,en,center,cw,cmd=obj['name'],obj['kind'],obj['net'],obj['start'],obj['end'],obj['center'],obj['cw'],obj['command']; rawv=ws.transaction(SkillCode(cmd)); s.refresh(); inp={'start':[wire(st[0]),wire(st[1])],'end':None,'width':wire(W),'center':None} if kind=='via' else {'start':[wire(st[0]),wire(st[1])],'end':[wire(en[0]),wire(en[1])],'width':wire(W),'center':None if center is None else [wire(center[0]),wire(center[1])]}; smoke.assert_echo_inputs(kind,rawv,inp); native=fld(rawv,'committed'); expected=ep(native) if kind!='via' else (float(fld(native,'x')),float(fld(native,'y'))); pool=s.vias(net=net,layer=LAYER) if kind=='via' else s.routes(net=net,layer=LAYER); hits=[r for r in pool if (p(r)==expected if kind=='via' else (r.obj_type==kind and p(r.start)==expected[0] and p(r.end)==expected[1]))];
     if len(hits)!=1: raise RuntimeError(f'{name} target count={len(hits)}')
     smoke.assert_requery_bits(kind,rawv,hits[0])
     actual_relative_fraction=({'point':relative_point(expected,tx,ty)} if kind=='via' else {'start':relative_point(expected[0],tx,ty),'end':relative_point(expected[1],tx,ty)})
     if kind=='arc':
      actual_relative_fraction['center']=relative_point(p(hits[0].center),tx,ty); actual_relative_fraction['radius']=str(Fraction.from_float(float(hits[0].radius))); actual_relative_fraction['length']=str(Fraction.from_float(float(hits[0].length))) if getattr(hits[0],'length',None) is not None else None
     case['creation'].setdefault('objects',[]).append({'name':name,'command':cmd,'return':js(rawv),'echo_assert':True,'requery_bits_assert':True,'actual_relative_fraction':actual_relative_fraction,'dto':js(hits[0])})
     if kind!='via': targets.append((net,hits[0]))
    case['process']={'pid':opened._runtime.process.pid,'port':p1,'cwd':os.getcwd(),'version':js(ws['axlVersion'](Symbol('fullVersion'))),'units_accuracy':js(ws['axlDBGetDesignUnits']())}; case['settings']={'drcEnable_before':raw(ws,'axlDBControl',Symbol('drcEnable')),'spacing_line_line_numeric':raw(ws,'axlCNSGetSpacing','', 'TOP', Symbol('line_line'), None),'spacing_line_line_string':raw(ws,'axlCNSGetSpacing','', 'TOP', Symbol('line_line'), True),'spacing_via_line':raw(ws,'axlCNSGetSpacing','', 'TOP', Symbol('via_line'), None),'waived_before':raw(ws,'axlDRCWaiveGetCount'),'master_after':raw(ws,'axlDBControl',Symbol('drcEnable')),'spacing_mode_all':raw(ws,'axlCNSSpacingModeGet',Symbol('all')),'design_mode_all':raw(ws,'axlCNSDesignModeGet',Symbol('all'))}
    case['creation']['context']=raw(ws,'__v2DrcContextPure',NET_A,NET_B); case['settings']['context']=case['creation']['context'];  case['drc']['item_calls']=[]
    for created in case['creation'].get('objects',[]):
     if created.get('name')=='arcA': case['creation']['arc_requery']=created.get('dto')
     if created.get('name')=='lineB': case['creation']['line_requery']=created.get('dto')
    for net,rline in targets:
     args=('route',net,None,rline.layer,rline.obj_type,rline.start,rline.end,float(rline.width),rline.radius,rline.is_clockwise,rline.center); case['drc']['item_calls'] += [{'net':net,'first':raw(ws,'__v2DrcItemCount',*args),'second':raw(ws,'__v2DrcItemCount',*args)}]
    case['drc']['fresh_diag_items']=[]
    for net,rline in targets:
     da=('route',net,None,rline.layer,rline.obj_type,rline.start,rline.end,float(rline.width),rline.radius,rline.is_clockwise,rline.center); case['drc']['fresh_diag_items'].append({'net':net,'first':raw(ws,'__v2DiagItem',*da),'second':raw(ws,'__v2DiagItem',*da)})
    case['drc']['snapshot_before']=raw(ws,'__v2DrcSnapshot'); case['drc']['snapshot_before_fresh1']=raw(ws,'__v2DiagSnapshot'); case['drc']['snapshot_before_fresh2']=raw(ws,'__v2DiagSnapshot'); case['drc']['full_update']=raw(ws,'axlDRCUpdate',True); case['drc']['snapshot_after']=raw(ws,'__v2DrcSnapshot'); case['drc']['snapshot_after_fresh1']=raw(ws,'__v2DiagSnapshot'); case['drc']['snapshot_after_fresh2']=raw(ws,'__v2DiagSnapshot'); case['settings']['master_after']=raw(ws,'axlDBControl',Symbol('drcEnable')); case['settings']['drcEnable_after']=case['settings']['master_after']; case['settings']['waived_after']=raw(ws,'axlDRCWaiveGetCount'); case['drc']['waived_after']=case['settings']['waived_after']; case['audit_view']={'schema':'B3-boundary-gate','creation':{'arc_requery':case['creation'].get('arc_requery'),'line_requery':case['creation'].get('line_requery')},'settings':case['settings'].copy(),'drc':dict(case['drc'])}; case['audit_view']['drc']['item_calls']=case['drc'].get('fresh_diag_items'); case['audit_view']['drc']['snapshot_before']=case['drc'].get('snapshot_before_fresh2'); case['audit_view']['drc']['snapshot_after']=case['drc'].get('snapshot_after_fresh2'); gate_spec=importlib.util.spec_from_file_location('boundary_gate_snapshot',out/'boundary_gate.py'); gate_mod=importlib.util.module_from_spec(gate_spec); gate_spec.loader.exec_module(gate_mod); case['audit_view']['gate_verdict'],case['audit_view']['gate_evidence']=gate_mod.gate(case['audit_view']); case['status']='CAPTURED' if len(case['creation'].get('objects',[]))==4 and case['drc'].get('snapshot_before',{}).get('ok') and case['drc'].get('snapshot_after',{}).get('ok') else 'INCOMPLETE'
  except Exception: case['status']='INCOMPLETE'; case['traceback']=traceback.format_exc()
  case['process_poll']=None if opened is None else opened._runtime.process.poll(); rep['cases'].append(case); (out/'cases.jsonl').open('a',encoding='utf8').write(json.dumps(case,default=repr)+chr(10)); (out/'manifest.json').write_text(json.dumps(rep,indent=2,default=repr),encoding='utf8')
 rep['status']='CAPTURED' if len(rep['cases'])==len(CASES) and all(c['status']=='CAPTURED' for c in rep['cases']) else 'INCOMPLETE'; (out/'manifest.json').write_text(json.dumps(rep,indent=2,default=repr),encoding='utf8'); print(json.dumps({'status':rep['status'],'run_dir':str(out)})); return 0 if rep['status']=='CAPTURED' else 1
if __name__=='__main__': raise SystemExit(main())


















