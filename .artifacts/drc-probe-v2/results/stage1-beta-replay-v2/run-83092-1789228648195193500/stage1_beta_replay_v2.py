from __future__ import annotations
import hashlib,json,os,socket,sys,time,traceback,importlib.util,struct
from fractions import Fraction
from pathlib import Path
from shutil import copy2
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from allegrobridge import Allegro,SkillCode,Symbol
from allegrobridge.util import ASSETS_DIR
ROOT=Path(__file__).resolve().parent; SRC=ASSETS_DIR/'route'/'EL5_MIAN_FPC.brd'; LAYER='ETCH/TOP'; W=.15; NET_A='NFC_SWP'; NET_B='FINGER_SPI_MISO'
LINE_Y=-70.46
def bits(x):
 import struct; return struct.pack('>d',float(x)).hex()
def scalar(x):
 if isinstance(x,dict) and 'bits' in x: return struct.unpack('>d',bytes.fromhex(x['bits']))[0]
 if isinstance(x,dict) and 'value' in x: return scalar(x['value'])
 return float(x)
def point(x):
 if isinstance(x,dict): return (scalar(x['x']),scalar(x['y']))
 return (scalar(x[0]),scalar(x[1]))
def signature(dto):
 if not isinstance(dto,dict) or dto.get('obj_type') not in ('arc','line') or not dto.get('start') or not dto.get('end') or not dto.get('width'): return None
 return (dto.get('obj_type'),dto.get('net',{}).get('name') if isinstance(dto.get('net'),dict) else dto.get('net'),dto.get('layer'),tuple(bits(v) for v in point(dto['start'])),tuple(bits(v) for v in point(dto['end'])),tuple(bits(v) for v in point(dto['center'])) if dto.get('center') else None,bits(scalar(dto['width'])),bits(scalar(dto['radius'])) if dto.get('radius') is not None else None,None if dto.get('is_clockwise') is False else dto.get('is_clockwise'))
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
def saved_matches(session,obj):
 dto=obj['dto']; kind=dto.get('obj_type','via'); net=dto.get('net')
 if kind=='via':
  xy=(scalar(dto['x']),scalar(dto['y'])); pool=session.vias(net=net,layer=LAYER)
  return [r for r in pool if p(r)==xy]
 expected=(point(dto['start']),point(dto['end'])); pool=session.routes(net=net,layer=LAYER)
 return [r for r in pool if getattr(r,'obj_type',None)==kind and p(r.start)==expected[0] and p(r.end)==expected[1]]
def port():
 with socket.socket() as s: s.bind(('localhost',0)); return str(s.getsockname()[1])
def linecmd(net,s,e): return f'__v2Stage1Create(\'line "{net}" "{LAYER}" nil {sn(s[0])}:{sn(s[1])} {sn(e[0])}:{sn(e[1])} {sn(W)} nil nil)'
def arccmd(s,e,c,cw): return f'__v2Stage1Create(\'arc "{NET_A}" "{LAYER}" nil {sn(s[0])}:{sn(s[1])} {sn(e[0])}:{sn(e[1])} {sn(W)} {"t" if cw else "nil"} {sn(c[0])}:{sn(c[1])})'
def viacmd(net,pad,xy): return f'__v2Stage1Create(\'via "{net}" "{LAYER}" "{pad}" {sn(xy[0])}:{sn(xy[1])} nil {sn(W)} nil nil)'
def raw(ws,name,*args):
 try:return {'ok':True,'value':js(ws[name](*args))}
 except Exception:return {'ok':False,'traceback':traceback.format_exc()}
def main():
 os.environ.setdefault('CDSROOT',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('Sigrity_EDA_DIR',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('CDS_LIC_FILE','5280@localhost')
 out=ROOT/'results'/'stage1-beta-replay-v2'/f'run-{os.getpid()}-{time.time_ns()}'; out.mkdir(parents=True); snap=ROOT/'results'/'stage2-sweep-diag'/'run-63160-1789225091207869200'; helper=snap/'stage1_smoke.il'; drc=snap/'stage0_gate.il'; context=snap/'context_probe.il'; script=Path(__file__); [ (out/n).write_bytes(snapshot_source.read_bytes()) for n,snapshot_source in [('stage1_beta_replay_v2.py',script),('stage1_smoke.il',helper),('stage0_gate.il',drc),('context_probe.il',context),('stage1_smoke.py',snap/'stage1_smoke.py'),('stage2_sweep_diag.il',snap/'stage2_sweep_diag.il'),('boundary_gate.py',ROOT/'boundary_gate.py')]]; os.chdir(out); rep={'status':'RUNNING','run_dir':str(out),'argv':sys.argv[:],'cwd':os.getcwd(),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest() ,'cases':[]}
 for label,y,cw in [('minus',-69.62501,False),('plus',-69.62499,False),('positive',-69.62501,False)]:
  board=Path(copy2(SRC,out/f'{label}.brd')); p1=port(); os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']=str(out/label); Path(os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']).mkdir(); os.chdir(out/label); line_y = -70.44 if label == 'positive' else LINE_Y; va=(-620.,-70.); vb=(-620.,line_y); ae=(-619.,-70.); ac=(-619.5 + (0.00001 if label == 'plus' else -0.00001),-69.625); be=(-619.,line_y); case={'label':label,'beta':wire(0.00001 if label == 'plus' else -0.00001),'cy':wire(-69.625),'line_y':wire(line_y),'clockwise':cw,'arc_intent':{'start':list(va),'end':list(ae),'center':list(ac),'width':.15},'creation':{},'drc':{}}; opened=None
  try:
   with Allegro.open(mode='cli',board=board,workspace_id=p1,timeout=300) as opened:
    ws,s=opened.workspace,opened.session; ws['load']((out/'stage1_smoke.il').resolve().as_posix()); ws['load']((out/'stage0_gate.il').resolve().as_posix()); ws['load']((out/'context_probe.il').resolve().as_posix()); ws['load']((out/'stage2_sweep_diag.il').resolve().as_posix()); spec=importlib.util.spec_from_file_location('stage1_smoke_snapshot',out/'stage1_smoke.py'); smoke=importlib.util.module_from_spec(spec); spec.loader.exec_module(smoke); s.drc(); pad='VIA_ALL_0103'; line_y = -70.44 if label == 'positive' else LINE_Y; va=(-620.,-70.); vb=(-620.,line_y); ae=(-619.,-70.); ac=(-619.5 + (0.00001 if label == 'plus' else -0.00001),-69.625); be=(-619.,line_y); objs=[{'name':'viaA','kind':'via','net':NET_A,'start':va,'end':None,'center':None,'cw':None,'command':viacmd(NET_A,pad,va)}, {'name':'arcA','kind':'arc','net':NET_A,'start':va,'end':ae,'center':ac,'cw':cw,'command':arccmd(va,ae,ac,cw)}, {'name':'viaB','kind':'via','net':NET_B,'start':vb,'end':None,'center':None,'cw':None,'command':viacmd(NET_B,pad,vb)}, {'name':'lineB','kind':'line','net':NET_B,'start':vb,'end':be,'center':None,'cw':None,'command':linecmd(NET_B,vb,be)}]
    targets=[]
    for obj in objs:
     name,kind,net,st,en,center,cw,cmd=obj['name'],obj['kind'],obj['net'],obj['start'],obj['end'],obj['center'],obj['cw'],obj['command']; rawv=ws.transaction(SkillCode(cmd)); s.refresh(); inp={'start':[wire(st[0]),wire(st[1])],'end':None,'width':wire(W),'center':None} if kind=='via' else {'start':[wire(st[0]),wire(st[1])],'end':[wire(en[0]),wire(en[1])],'width':wire(W),'center':None if center is None else [wire(center[0]),wire(center[1])]}; smoke.assert_echo_inputs(kind,rawv,inp); native=fld(rawv,'committed'); expected=ep(native) if kind!='via' else (float(fld(native,'x')),float(fld(native,'y'))); pool=s.vias(net=net,layer=LAYER) if kind=='via' else s.routes(net=net,layer=LAYER); hits=[r for r in pool if (p(r)==expected if kind=='via' else (r.obj_type==kind and p(r.start)==expected[0] and p(r.end)==expected[1]))];
     if len(hits)!=1: raise RuntimeError(f'{name} target count={len(hits)}')
     smoke.assert_requery_bits(kind,rawv,hits[0])
     case['creation'].setdefault('objects',[]).append({'name':name,'command':cmd,'return':js(rawv),'echo_assert':True,'requery_bits_assert':True,'dto':js(hits[0])})
     if kind!='via': targets.append((net,hits[0]))
    case['process']={'pid':opened._runtime.process.pid,'port':p1,'cwd':os.getcwd(),'version':js(ws['axlVersion'](Symbol('fullVersion'))),'units_accuracy':js(ws['axlDBGetDesignUnits']())}; case['settings']={'drcEnable_before':raw(ws,'axlDBControl',Symbol('drcEnable')),'spacing_line_line_numeric':raw(ws,'axlCNSGetSpacing','', 'TOP', Symbol('line_line')),'spacing_line_line_string':raw(ws,'axlCNSGetSpacing','', 'TOP', Symbol('line_line'), True),'spacing_via_line':raw(ws,'axlCNSGetSpacing','', 'TOP', Symbol('via_line')),'waived_before':raw(ws,'axlDRCWaiveGetCount'),'master_after':raw(ws,'axlDBControl',Symbol('drcEnable')),'spacing_mode_all':raw(ws,'axlCNSSpacingModeGet',Symbol('all')),'design_mode_all':raw(ws,'axlCNSDesignModeGet',Symbol('all'))}
    case['creation']['context']=raw(ws,'__v2DrcContextPure',NET_A,NET_B); case['drc']['item_calls']=[]
    for net,rline in targets:
     args=('route',net,None,rline.layer,rline.obj_type,rline.start,rline.end,float(rline.width),rline.radius,rline.is_clockwise,rline.center); first=raw(ws,'__v2DiagItem',*args); second=raw(ws,'__v2DiagItem',*args); case['drc']['item_calls'] += [{'net':net,'first':first,'second':second,'repeat_equal':first==second}]
    case['drc']['snapshot_before']=raw(ws,'__v2DiagSnapshot'); case['drc']['full_update']=raw(ws,'axlDRCUpdate',True); case['drc']['snapshot_after']=raw(ws,'__v2DiagSnapshot'); case['settings']['master_after']=raw(ws,'axlDBControl',Symbol('drcEnable')); case['settings']['drcEnable_after']=case['settings']['master_after']; case['settings']['waived_after']=raw(ws,'axlDRCWaiveGetCount'); case['drc']['waived_after']=case['settings']['waived_after']; case['settings']['context']=case['creation']['context']; gate_spec=importlib.util.spec_from_file_location('boundary_gate_snapshot',out/'boundary_gate.py'); gate_mod=importlib.util.module_from_spec(gate_spec); gate_spec.loader.exec_module(gate_mod); gd={'settings':case['settings'],'drc':case['drc'],'creation':{'arc_requery':next(o['dto'] for o in case['creation']['objects'] if o['name']=='arcA'),'line_requery':next(o['dto'] for o in case['creation']['objects'] if o['name']=='lineB')}}; case['gate_verdict'],case['gate_evidence']=gate_mod.gate(gd); case['status']='CAPTURED' if case['gate_verdict'] in ('FLAGGED','CLEAN') else 'INCOMPLETE'
    if label in ('minus','plus') and case['status']=='CAPTURED':
     saved=out/f'{label}-saved.brd'; save_ret=ws['axlSaveDesign'](design=saved.resolve().as_posix(),noMru=True,noConfirm=True); s.refresh(); after=[]
     for obj in case['creation']['objects']:
      hits=saved_matches(s,obj)
      if len(hits)!=1: raise RuntimeError(f'{obj["name"]} saved target count={len(hits)}')
      dto=js(hits[0]); before=obj['dto']; after.append({'name':obj['name'],'before_dto':before,'after_dto':dto,'count':len(hits),'all_fields_equal':before==dto})
     case['save']={'path':str(saved),'return':js(save_ret),'exists':saved.exists(),'sha256':hashlib.sha256(saved.read_bytes()).hexdigest() if saved.exists() else None,'objects':after,'all_objects_unique':len(after)==4,'all_fields_equal':all(x['all_fields_equal'] for x in after)}
  except Exception: case['status']='INCOMPLETE'; case['traceback']=traceback.format_exc()
  case['process_poll']=None if opened is None else opened._runtime.process.poll()
  try:
   arc=next(o['dto'] for o in case['creation']['objects'] if o['name']=='arcA'); line=next(o['dto'] for o in case['creation']['objects'] if o['name']=='lineB')
   cy=Fraction.from_float(point(arc['center'])[1]); rr=Fraction.from_float(scalar(arc['radius'])); ly=Fraction.from_float(point(line['start'])[1]); wa=Fraction.from_float(scalar(arc['width'])); wl=Fraction.from_float(scalar(line['width'])); hw=(wa+wl)/2; clearance=cy-rr-ly-hw
   case['oracle']={'clearance_fraction':str(clearance),'clearance_decimal_display':format(float(clearance),'.17g'),'model':'actual committed cy - actual radius - actual line y - (actual arc width + actual line width)/2'}
  except Exception: case['oracle']={'status':'NOT_COMPUTED','error':traceback.format_exc()}
  rep['cases'].append(case); (out/'cases.jsonl').open('a',encoding='utf8').write(json.dumps(case,default=repr)+chr(10)); (out/'manifest.json').write_text(json.dumps(rep,indent=2,default=repr),encoding='utf8')
 rep['status']='CAPTURED' if len(rep['cases'])==3 and all(x['status']=='CAPTURED' for x in rep['cases']) else 'INCOMPLETE'; (out/'manifest.json').write_text(json.dumps(rep,indent=2,default=repr),encoding='utf8'); print(json.dumps({'status':rep['status'],'run_dir':str(out)})); return 0 if rep['status']=='CAPTURED' else 1
if __name__=='__main__': raise SystemExit(main())





















