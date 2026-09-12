from __future__ import annotations
import contextlib, hashlib, json, os, socket, struct, sys, time, traceback
from pathlib import Path
from shutil import copy2
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from allegrobridge import Allegro, SkillCode, Symbol
from allegrobridge.util import ASSETS_DIR

ROOT = Path(__file__).resolve().parent
SRC = ASSETS_DIR / 'route' / 'EL5_MIAN_FPC.brd'
APPROVED = ROOT / 'results' / 'stage0-gate' / 'run-37248-1789193361092813400'
HELPER = APPROVED / 'stage1_smoke.il'
DRC_HELPER = APPROVED / 'stage0_gate.il'
CONTEXT = APPROVED / 'context_probe.il'
SMOKE = APPROVED / 'stage1_smoke.py'
LAYER = 'ETCH/TOP'; PAD = 'VIA_ALL_0103'; ARC_NET = 'NFC_SWP'; LINE_NET = 'FINGER_SPI_MISO'; W = 0.15
CASES = [
 ('FLIP_LO', (300.0,410.0), (302.0001,410.0), (301.00005,410.1249193400748), (300.0,408.9071), (302.0,408.9071), False),
 ('FLIP_HI', (300.0,420.0), (302.0001,420.0), (301.00005,420.1249228400748), (300.0,418.9071), (302.0,418.9071), False),
 ('GRID_EQ', (300.0,460.0), (302.0,460.0), (301.0,460.75), (300.0,459.29), (302.0,459.29), False),
]

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def bits(x): return struct.pack('>d', float(x)).hex()
def wire(x):
 x=float(x); s=format(x,'.17g'); return {'value':x,'%.17g':s if any(c in s for c in '.eE') else s+'.0','bits':bits(x)}
def pure(v):
 if hasattr(v,'model_dump') and callable(v.model_dump): return pure(v.model_dump(mode='python'))
 if isinstance(v,dict): return {str(k):pure(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)): return [pure(x) for x in v]
 if isinstance(v,float): return wire(v)
 return v
def pt(v): return (float(v.x),float(v.y)) if hasattr(v,'x') else (float(v[0]),float(v[1]))
def port():
 with socket.socket() as s: s.bind(('localhost',0)); return str(s.getsockname()[1])
def raw(ws,name,*args):
 try: return {'ok':True,'value':pure(ws[name](*args))}
 except Exception: return {'ok':False,'error':traceback.format_exc()}
def n(x):
 s=format(float(x),'.17g'); return s if any(c in s for c in '.eE') else s+'.0'
def via_cmd(net,pad,p): return f'__v2Stage1Create(\'via "{net}" "{LAYER}" "{pad}" {n(p[0])}:{n(p[1])} nil {n(W)} nil nil)'
def line_cmd(net,s,e): return f'__v2Stage1Create(\'line "{net}" "{LAYER}" nil {n(s[0])}:{n(s[1])} {n(e[0])}:{n(e[1])} {n(W)} nil nil)'
def arc_cmd(s,e,c): return f'__v2Stage1Create(\'arc "{ARC_NET}" "{LAYER}" "{PAD}" {n(s[0])}:{n(s[1])} {n(e[0])}:{n(e[1])} {n(W)} nil {n(c[0])}:{n(c[1])})'
def marker_dict(v):
 if isinstance(v,dict): return v
 if isinstance(v,list):
  out={}; i=0
  while i+1<len(v):
   if isinstance(v[i],str): out[v[i]]=v[i+1]
   i+=2
  return out
 return {}
def matching_markers(raw_value):
 seq=raw_value.get('markers') if isinstance(raw_value,dict) else None
 out=[]
 for x in seq or []:
  if isinstance(x,dict): out.append(x.get('data',x))
  elif isinstance(x,list):
   d=marker_dict(x); out.append(d.get('data',d))
 return out
def scalar(v): return float(v.get('value')) if isinstance(v,dict) and 'value' in v else float(v)
def point_value(v):
 f=marker_dict(v); return (scalar(f.get('x')),scalar(f.get('y')))
def same_point(v, expected):
 try: return bits(scalar(marker_dict(v).get('x'))) == bits(expected[0]) and bits(scalar(marker_dict(v).get('y'))) == bits(expected[1])
 except (TypeError,ValueError): return False
def dto_point_bits(v):
 try: return (bits(pt(v)[0]),bits(pt(v)[1]))
 except (TypeError,ValueError,AttributeError): return None
def unique_rows(rows, obj_type, net, start, end, center=None):
 out=[]
 for r in rows:
  if getattr(r,'obj_type',None)!=obj_type or getattr(r,'net',None)!=net or getattr(r,'layer',None)!=LAYER: continue
  if dto_point_bits(getattr(r,'start',None)) != tuple(bits(x) for x in start): continue
  if dto_point_bits(getattr(r,'end',None)) != tuple(bits(x) for x in end): continue
  if center is not None and dto_point_bits(getattr(r,'center',None)) != tuple(bits(x) for x in center): continue
  out.append(r)
 return out
def committed_point(d, name):
 p=marker_dict(d.get(name)); return (scalar(p.get('x')),scalar(p.get('y')))
def figures_match(m, S, E, C, LS, LE, arc_radius, expected_cw):
 fs=m.get('figures',[]) if isinstance(m,dict) else []
 route_fs=[marker_dict(f) for f in fs if isinstance(f,(dict,list)) and marker_dict(f).get('obj_type') in ('arc','line')]
 if len(route_fs)!=2: return False
 line_ok=arc_ok=False
 for f in route_fs:
  net=marker_dict(f.get('net'))
  w=f.get('width')
  if f.get('obj_type')=='line' and net.get('name')==LINE_NET and f.get('layer')==LAYER:
   line_ok=same_point(f.get('start'),LS) and same_point(f.get('end'),LE) and bits(scalar(w))==bits(W)
  if f.get('obj_type')=='arc' and net.get('name')==ARC_NET and f.get('layer')==LAYER:
   arc_ok=same_point(f.get('start'),S) and same_point(f.get('end'),E) and same_point(f.get('center'),C) and bits(scalar(w))==bits(W) and f.get('radius') is not None and bits(scalar(f.get('radius'))) == bits(arc_radius) and f.get('is_clockwise') == (expected_cw if expected_cw else None)
 return line_ok and arc_ok
def main():
 os.environ.setdefault('CDSROOT',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('Sigrity_EDA_DIR',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('CDS_LIC_FILE','5280@localhost')
 out=ROOT/'results'/'stage0-b-replay'/f'run-{os.getpid()}-{time.time_ns()}'; out.mkdir(parents=True)
 for p in (HELPER,DRC_HELPER,CONTEXT,SMOKE):
  if not p.is_file(): raise FileNotFoundError(p)
 (out/'stage1_smoke.il').write_bytes(HELPER.read_bytes()); (out/'stage0_gate.il').write_bytes(DRC_HELPER.read_bytes()); (out/'context_probe.il').write_bytes(CONTEXT.read_bytes()); (out/'stage1_smoke.py').write_bytes(SMOKE.read_bytes())
 (out/'stage0_b_replay.py').write_bytes(Path(__file__).read_bytes())
 report={'status':'RUNNING','run_dir':out.as_posix(),'source_sha256':sha(SRC),'script_sha256':sha(Path(__file__)),'helper_sha256':sha(HELPER),'drc_helper_sha256':sha(DRC_HELPER),'context_sha256':sha(CONTEXT),'cases':[]}
 (out/'manifest.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 old=os.getcwd()
 try:
  for tag,S,E,C,LS,LE,cw in CASES:
   case={'tag':tag,'request':{'arc':{'start':list(map(wire,S)),'end':list(map(wire,E)),'center':list(map(wire,C)),'width':wire(W),'clockwise':cw},'line':{'start':list(map(wire,LS)),'end':list(map(wire,LE)),'width':wire(W)},'via_anchors':{'arc':list(map(wire,S)),'line':list(map(wire,LS))}},'commands':{},'settings':{},'drc':{}}
   board=Path(copy2(SRC,out/f'{tag}.brd')); wd=out/tag; wd.mkdir(); os.chdir(wd); os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']=wd.as_posix(); opened=None; p1=port()
   try:
    with Allegro.open(mode='cli',board=board,workspace_id=p1,timeout=300) as opened:
     ws,s=opened.workspace,opened.session; proc=opened._runtime.process; case['process']={'pid':proc.pid,'port':p1,'cwd':os.getcwd(),'board_sha256':sha(board),'argv':pure(getattr(proc,'args',None)),'version':pure(getattr(proc,'version',None))}
     ws['load']((out/'stage1_smoke.il').resolve().as_posix()); ws['load']((out/'stage0_gate.il').resolve().as_posix()); ws['load']((out/'context_probe.il').resolve().as_posix()); sys.path.insert(0,str(out)); import stage1_smoke as smoke
     case['settings']['drc_init']=pure(s.drc())
     case['settings']['units_accuracy']=raw(ws,'axlDBGetDesignUnits'); case['settings']['drcEnable_before']=raw(ws,'axlDBControl',Symbol('drcEnable')); case['settings']['spacing_mode_all']=raw(ws,'axlCNSSpacingModeGet',Symbol('all')); case['settings']['design_mode_all']=raw(ws,'axlCNSDesignModeGet',Symbol('all')); case['settings']['waived_before']=raw(ws,'axlDRCWaiveGetCount'); case['settings']['spacing_default']=raw(ws,'axlCNSGetSpacing','DEFAULT','TOP',None,True); case['settings']['spacing_line_line_numeric']=raw(ws,'axlCNSGetSpacing','', 'TOP', Symbol('line_line')); case['settings']['spacing_line_line_string']=raw(ws,'axlCNSGetSpacing','', 'TOP', Symbol('line_line'), True); case['settings']['context']=raw(ws,'__v2DrcContextPure',ARC_NET,LINE_NET)
     for net,p,cmd in [(ARC_NET,S,via_cmd(ARC_NET,PAD,S)),(LINE_NET,LS,via_cmd(LINE_NET,PAD,LS))]:
      ret=ws.transaction(SkillCode(cmd)); case['commands'][f'via_{net}']={'wire':cmd,'return':pure(ret),'before_call':True}; s.refresh()
      case.setdefault('_via_native',[]).append(ret)
     ac=arc_cmd(S,E,C); lc=line_cmd(LINE_NET,LS,LE); case['commands']['arc']={'wire':ac,'before_call':True}; case['commands']['line']={'wire':lc,'before_call':True}; ar=ws.transaction(SkillCode(ac)); case['commands']['arc']['return']=pure(ar); s.refresh(); lr=ws.transaction(SkillCode(lc)); case['commands']['line']['return']=pure(lr); s.refresh()
     arc_comm=marker_dict(pure(ar).get('committed')); line_comm=marker_dict(pure(lr).get('committed'))
     actual_S,actual_E,actual_C=committed_point(arc_comm,'start'),committed_point(arc_comm,'end'),committed_point(arc_comm,'center'); actual_LS,actual_LE=committed_point(line_comm,'start'),committed_point(line_comm,'end'); actual_radius=scalar(arc_comm.get('radius'))
     arc_rows=unique_rows(s.routes(net=ARC_NET,layer=LAYER),'arc',ARC_NET,actual_S,actual_E,actual_C); line_rows=unique_rows(s.routes(net=LINE_NET,layer=LAYER),'line',LINE_NET,actual_LS,actual_LE)
     if len(arc_rows)!=1 or len(line_rows)!=1: raise RuntimeError(f'unique target rows arc={len(arc_rows)} line={len(line_rows)}')
     all_vias=[v for v in s.vias(layer=LAYER) if getattr(v,'net',None) in (ARC_NET,LINE_NET)]
     via_rows=[]
     for net,p in ((ARC_NET,S),(LINE_NET,LS)):
      vr=[v for v in all_vias if v.net==net and dto_point_bits(v)==tuple(bits(x) for x in p) and v.padstack==PAD]
      if len(vr)!=1: raise RuntimeError(f'unique via row {net}={len(vr)}')
      via_rows.append(vr[0])
     arc_row,line_row=arc_rows[0],line_rows[0]; case['creation']={'arc_requery':pure(arc_row),'line_requery':pure(line_row),'via_requery':pure(via_rows)}
     inputs_arc={'start':[wire(S[0]),wire(S[1])],'end':[wire(E[0]),wire(E[1])],'center':[wire(C[0]),wire(C[1])],'width':wire(W)}; inputs_line={'start':[wire(LS[0]),wire(LS[1])],'end':[wire(LE[0]),wire(LE[1])],'center':None,'width':wire(W)}
     smoke.assert_request_wire(ac,inputs_arc); smoke.assert_echo_inputs('arc',ar,inputs_arc); smoke.assert_requery_bits('arc',ar,arc_row); smoke.assert_request_wire(lc,inputs_line); smoke.assert_echo_inputs('line',lr,inputs_line); smoke.assert_requery_bits('line',lr,line_row)
     for (net,p),cmd,ret,row in zip(((ARC_NET,S),(LINE_NET,LS)),(via_cmd(ARC_NET,PAD,S),via_cmd(LINE_NET,PAD,LS)),case['_via_native'],via_rows):
      vi={'start':[wire(p[0]),wire(p[1])],'width':wire(W)}; smoke.assert_request_wire(cmd,vi); smoke.assert_echo_inputs('via',ret,vi); smoke.assert_requery_bits('via',ret,row)
     case['creation']['echo_requery_assert']=True; del case['_via_native']
     case['drc']['snapshot_before']=raw(ws,'__v2DrcSnapshot'); case['drc']['item_calls']=[]
     for net,route in [(ARC_NET,arc_row),(LINE_NET,line_row)]:
      args=('route',net,None,LAYER,route.obj_type,pt(route.start),pt(route.end),float(route.width),float(route.radius) if route.obj_type=='arc' else None,route.is_clockwise,pt(route.center) if route.obj_type=='arc' else None)
      a=raw(ws,'__v2DrcItemCount',*args); b=raw(ws,'__v2DrcItemCount',*args); case['drc']['item_calls'].append({'net':net,'args':pure(args),'first':a,'second':b,'repeat_equal':a==b,'marker_identity_first': [figures_match(marker_dict(x),pt(arc_row.start),pt(arc_row.end),pt(arc_row.center),pt(line_row.start),pt(line_row.end),float(arc_row.radius),bool(arc_row.is_clockwise)) for x in matching_markers(a.get('value',{}))]})
     case['drc']['full_update']=raw(ws,'axlDRCUpdate',True); case['drc']['snapshot_after']=raw(ws,'__v2DrcSnapshot'); case['drc']['waived_after']=raw(ws,'axlDRCWaiveGetCount'); case['settings']['drcEnable_after']=raw(ws,'axlDBControl',Symbol('drcEnable')); case['drc']['all_markers_after']=pure(s.drc())
     valid=all(x['first'].get('ok') and x['second'].get('ok') and x['first'].get('value',{}).get('resolved') is True and isinstance(x['first'].get('value',{}).get('count'),int) and x['first']['value'].get('count')==x['second'].get('value',{}).get('count') and x['repeat_equal'] for x in case['drc']['item_calls'])
     case['drc']['full_snapshot_ok']=case['drc']['snapshot_before'].get('ok') and case['drc']['snapshot_after'].get('ok') and case['drc']['full_update'].get('ok')
     case['drc']['target_identity_observed']=[any(x['marker_identity_first']) for x in case['drc']['item_calls']]
     case['clean_gate']='NOT_EVALUATED_BY_REPLAY'
     case['status']='RAW_CAPTURED' if valid and case['drc']['full_snapshot_ok'] else 'INCOMPLETE'
   except Exception: case['status']='FAILED'; case['error']=traceback.format_exc()
   finally:
    case['process_poll']=None if opened is None else opened._runtime.process.poll(); report['cases'].append(case); (out/'cases.jsonl').open('a',encoding='utf-8').write(json.dumps(case,default=repr)+'\n'); (out/'manifest.json').write_text(json.dumps(report,indent=2,default=repr),encoding='utf-8'); os.chdir(out)
  report['status']='COMPLETE_RAW' if len(report['cases'])==3 and all(c['status']=='RAW_CAPTURED' for c in report['cases']) else 'INCOMPLETE'
 finally: os.chdir(old)
 (out/'manifest.json').write_text(json.dumps(report,indent=2,default=repr),encoding='utf-8'); print(json.dumps({'status':report['status'],'run_dir':out.as_posix(),'cases':len(report['cases'])})); return 0 if report['status']=='COMPLETE_RAW' else 1
if __name__=='__main__': raise SystemExit(main())
