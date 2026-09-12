from __future__ import annotations
import hashlib,json,os,socket,sys,time,traceback,importlib.util,struct,random
from fractions import Fraction
from pathlib import Path
from shutil import copy2
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from allegrobridge import Allegro,SkillCode,Symbol
from allegrobridge.util import ASSETS_DIR
ROOT=Path(__file__).resolve().parent; SRC=ASSETS_DIR/'route'/'EL5_MIAN_FPC.brd'; LAYER='ETCH/TOP'; W=.15; NET_A='NFC_SWP'; NET_B='FINGER_SPI_MISO'
INITIAL_CY=[410.12490,410.124915,410.1249193400748,410.1249228400748,410.124930,410.124950]
LINE_Y=408.9071
REPEAT_SEED=20260912
REPEAT_LO=410.1249219650748; REPEAT_HI=410.12492207444984
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
 out=ROOT/'results'/'stage2-boundary-repeat'/f'run-{os.getpid()}-{time.time_ns()}'; out.mkdir(parents=True); snap=ROOT/'results'/'stage2-sweep-diag'/'run-63160-1789225091207869200'; helper=snap/'stage1_smoke.il'; drc=snap/'stage0_gate.il'; context=snap/'context_probe.il'; script=Path(__file__); [ (out/n).write_bytes(snapshot_source.read_bytes()) for n,snapshot_source in [('stage2_boundary_repeat.py',script),('stage1_smoke.il',helper),('stage0_gate.il',drc),('context_probe.il',context),('stage1_smoke.py',snap/'stage1_smoke.py'),('stage2_sweep_diag.il',snap/'stage2_sweep_diag.il'),('boundary_gate.py',ROOT/'boundary_gate.py')]]; os.chdir(out); rep={'status':'RUNNING','run_dir':str(out),'argv':sys.argv[:],'cwd':os.getcwd(),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'repeat_seed':REPEAT_SEED,'cases':[]}
 pending=[(f'lo-{i:02d}',REPEAT_LO,False) for i in range(5)]+[(f'hi-{i:02d}',REPEAT_HI,False) for i in range(5)]; random.Random(REPEAT_SEED).shuffle(pending); requested_bits=set(); state_by_fingerprint={}; duplicates=[]; samples=[]; stop_reason='REPEAT_INCOMPLETE'
 while pending and len(state_by_fingerprint)<60:
  label,y,cw=pending.pop(0)
  if bits(y) in requested_bits and False: continue
  requested_bits.add(bits(y))
  board=Path(copy2(SRC,out/f'{label}.brd')); p1=port(); os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']=str(out/label); Path(os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']).mkdir(); os.chdir(out/label); case={'label':label,'cy':wire(y),'line_y':wire(LINE_Y),'clockwise':cw,'arc_intent':{'start':[300,410],'end':[302.0001,410],'center':[301.00005,y],'width':.15},'creation':{},'drc':{}}; opened=None
  try:
   with Allegro.open(mode='cli',board=board,workspace_id=p1,timeout=300) as opened:
    ws,s=opened.workspace,opened.session; ws['load']((out/'stage1_smoke.il').resolve().as_posix()); ws['load']((out/'stage0_gate.il').resolve().as_posix()); ws['load']((out/'context_probe.il').resolve().as_posix()); ws['load']((out/'stage2_sweep_diag.il').resolve().as_posix()); spec=importlib.util.spec_from_file_location('stage1_smoke_snapshot',out/'stage1_smoke.py'); smoke=importlib.util.module_from_spec(spec); spec.loader.exec_module(smoke); s.drc(); pad='VIA_ALL_0103'; va=(300.,410.); vb=(300.,LINE_Y); ae=(302.0001,410.); ac=(301.00005,y); be=(302.,LINE_Y); objs=[{'name':'viaA','kind':'via','net':NET_A,'start':va,'end':None,'center':None,'cw':None,'command':viacmd(NET_A,pad,va)}, {'name':'arcA','kind':'arc','net':NET_A,'start':va,'end':ae,'center':ac,'cw':cw,'command':arccmd(va,ae,ac,cw)}, {'name':'viaB','kind':'via','net':NET_B,'start':vb,'end':None,'center':None,'cw':None,'command':viacmd(NET_B,pad,vb)}, {'name':'lineB','kind':'line','net':NET_B,'start':vb,'end':be,'center':None,'cw':None,'command':linecmd(NET_B,vb,be)}]
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
  except Exception: case['status']='INCOMPLETE'; case['traceback']=traceback.format_exc()
  case['process_poll']=None if opened is None else opened._runtime.process.poll()
  try:
   arc=next(o['dto'] for o in case['creation']['objects'] if o['name']=='arcA'); line=next(o['dto'] for o in case['creation']['objects'] if o['name']=='lineB')
   cy=Fraction.from_float(point(arc['center'])[1]); rr=Fraction.from_float(scalar(arc['radius'])); ly=Fraction.from_float(point(line['start'])[1]); wa=Fraction.from_float(scalar(arc['width'])); wl=Fraction.from_float(scalar(line['width'])); hw=(wa+wl)/2; clearance=cy-rr-ly-hw
   case['oracle']={'clearance_fraction':str(clearance),'clearance_decimal_display':format(float(clearance),'.17g'),'model':'actual committed cy - actual radius - actual line y - (actual arc width + actual line width)/2'}; samples.append((y,clearance,case.get('gate_verdict','AMBIGUOUS')))
  except Exception: case['oracle']={'status':'NOT_COMPUTED','error':traceback.format_exc()}
  fingerprint=hashlib.sha256(json.dumps([(o.get('name'),o.get('dto')) for o in case.get('creation',{}).get('objects',[])],sort_keys=True,default=repr).encode()).hexdigest(); case['geometry_fingerprint']=fingerprint
  if fingerprint in state_by_fingerprint and state_by_fingerprint[fingerprint].get('gate_verdict') != case.get('gate_verdict'): stop_reason='AMBIGUOUS_SAME_GEOMETRY_VERDICT'; pending.clear()
  elif fingerprint in state_by_fingerprint: duplicates.append({'label':label,'fingerprint':fingerprint})
  else: state_by_fingerprint[fingerprint]=case
  rep['cases'].append(case); (out/'cases.jsonl').open('a',encoding='utf8').write(json.dumps(case,default=repr)+chr(10)); (out/'manifest.json').write_text(json.dumps(rep,indent=2,default=repr),encoding='utf8')
  if False and len(samples)>=6:
   ordered=sorted((x for x in samples if x[2] in ('FLAGGED','CLEAN')),key=lambda z:z[1]); by_request=sorted(ordered,key=lambda z:z[0]); monotone=all(a[1]<=b[1] for a,b in zip(by_request,by_request[1:])); flags=[x for x in ordered if x[2]=='FLAGGED']; cleans=[x for x in ordered if x[2]=='CLEAN']; case.setdefault('adaptive',{})['request_cy_monotone']=monotone
   if not monotone: stop_reason='NONMONOTONE'; pending.clear()
   case.setdefault('adaptive',{})['clearance_order']=[{'cy':a,'clearance':str(b),'verdict':c} for a,b,c in ordered]
   if not monotone: pass
   elif flags and cleans:
    lo=max(flags,key=lambda z:z[1]); hi=min(cleans,key=lambda z:z[1])
    width=hi[1]-lo[1]
    case.setdefault('adaptive',{})['bracket']={'lo_cy':lo[0],'lo_clearance':str(lo[1]),'hi_cy':hi[0],'hi_clearance':str(hi[1]),'width':str(width)}
    if lo[1]>=hi[1]: stop_reason='NONMONOTONE'; pending.clear()
    elif width<Fraction(1,10000000): stop_reason='SEARCH_BRACKETED'; pending.clear()
    else:
     mid=(lo[0]+hi[0])/2
     if mid not in [x[1] for x in pending] and len(state_by_fingerprint)+len(pending)<60: pending.append((f'adaptive-{len(samples):03d}',float(mid),False)); case.setdefault('adaptive',{})['queued_midpoint']=float(mid)
  rep['adaptive']={'distinct_actual_fingerprints':len(state_by_fingerprint),'requested_bits':len(requested_bits),'duplicates':duplicates,'samples':len(samples),'pending':len(pending),'stop_reason':stop_reason,'stop':'bracket_width<1e-7 or 60 distinct actual geometries'}
 byfp={}
 for c in rep['cases']: byfp.setdefault(c.get('geometry_fingerprint'),set()).add(c.get('gate_verdict'))
 rep['repeat_validation']={'seed':REPEAT_SEED,'expected_each':5,'fingerprint_verdict_sets':{k:sorted(v) for k,v in byfp.items()},'ambiguous_same_geometry_verdict':any(len(v)>1 for v in byfp.values())}
 rep['status']='REPEAT_CAPTURED' if len(rep['cases'])==10 and all(c['status']=='CAPTURED' for c in rep['cases']) and not rep['repeat_validation']['ambiguous_same_geometry_verdict'] else 'AMBIGUOUS'; (out/'manifest.json').write_text(json.dumps(rep,indent=2,default=repr),encoding='utf8'); print(json.dumps({'status':rep['status'],'run_dir':str(out)})); return 0 if rep['status']=='REPEAT_CAPTURED' else 1
if __name__=='__main__': raise SystemExit(main())


















