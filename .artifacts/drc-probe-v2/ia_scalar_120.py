from __future__ import annotations
import hashlib, json, os, socket, struct, sys, time
from pathlib import Path
from fractions import Fraction
from shutil import copy2
from allegrobridge import Allegro, SkillCode, Symbol
from allegrobridge.util import ASSETS_DIR
sys.path.insert(0, str(Path(__file__).resolve().parent))
import stage1_smoke as smoke

ROOT=Path(__file__).resolve().parent
LAYER='ETCH/TOP'; NET='NFC_SWP'; WIDTH=0.15
PIPE=['299.90005','299.90015','299.90025','299.90045000000003','-300.09995','-300.09985','-300.09905000000003','-300.09885']
VALUES=[(f'pipeline_{i}',Fraction(s),float(s),Fraction('300') if not s.startswith('-') else Fraction('-300')) for i,s in enumerate(PIPE)]
for T in (Fraction('300'),Fraction('-300')):
  for bi,b in enumerate((Fraction('0.03125'),Fraction('0.09375'))):
    H=T+b; f=float(H)
    VALUES += [(f'next_{T}_{bi}_{side}',H,x,T) for side,x in (('minus',__import__('math').nextafter(f,-__import__('math').inf)),('center',f),('plus',__import__('math').nextafter(f,__import__('math').inf)))]
ROLES=('line_x','line_y','via_x','via_y','arc_x','arc_y')

def bits(x): return struct.pack('>d',float(x)).hex()
def wire(x):
    x=float(x); s=format(x,'.17g')
    if all(c not in s for c in '.eE'): s += '.0'
    return {'value':x,'%.17g':s,'bits':bits(x)}
def p(v):
    if hasattr(v,'location'): v=v.location
    return (float(v.x),float(v.y)) if hasattr(v,'x') else (float(v[0]),float(v[1]))
def js(v):
    if hasattr(v,'model_dump'): return js(v.model_dump(mode='python'))
    if isinstance(v,dict): return {str(k):js(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)): return [js(x) for x in v]
    if isinstance(v,float): return wire(v)
    return v
def fld(v,n): return v[n] if isinstance(v,dict) else v[v.index(n)+1]
def sn(x):
    s=format(float(x),'.17g'); return s if any(c in s for c in '.eE') else s+'.0'
def point17(x,y): return {'x':wire(x),'y':wire(y)}
def call(kind, value):
    H,x,T=value; v=float(x)
    if kind=='line_x': return 'line',(v,-600.0),(float(T+1),-599.0),None,None
    if kind=='line_y': return 'line',(-1000.0,v),(-999.0,float(T+1)),None,None
    if kind=='via_x': return 'via',(v,-600.0),None,None,None
    if kind=='via_y': return 'via',(-1000.0,v),None,None,None
    if kind=='arc_x': return 'arc',(v,-600.0),(float(T+1),-599.0),(float(T)+.5,-599.25),None
    if kind=='arc_y': return 'arc',(-1000.0,v),(-999.0,float(T+1)),(-999.25,float(T)+.5),None
    v=float(value)
    if kind=='line_x': return 'line',(v,200.0),(1.0,200.0),None
    if kind=='line_y': return 'line',(300.0,v),(301.0,1.0),None
    if kind=='arc_x': return 'arc',(v,350.0),(1.0,351.0),(0.5,350.75)
    if kind=='arc_y': return 'arc',(350.0,v),(351.0,1.0),(350.75,0.5)
    return 'via',(v,400.0) if kind=='via_x' else (400.0,v),None,None
def cmd(kind, a,b,c,pad,direction='nil'):
    if kind=='via': return f"__v2Stage1Create('via \"{NET}\" \"{LAYER}\" \"{pad}\" {sn(a[0])}:{sn(a[1])} nil {sn(WIDTH)} nil nil)"
    k,s,e,center=kind,a,b,c
    ce='nil' if center is None else sn(center[0])+':'+sn(center[1])
    return f"__v2Stage1Create('{k} \"{NET}\" \"{LAYER}\" nil {sn(s[0])}:{sn(s[1])} {sn(e[0])}:{sn(e[1])} {sn(WIDTH)} {direction} {ce})"
def main():
    os.environ.setdefault('CDSROOT',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('Sigrity_EDA_DIR',r'D:\Cadence\Cadence_SPB_17.2-2016'); os.environ.setdefault('CDS_LIC_FILE','5280@localhost')
    out=ROOT/'results'/'ia-scalar-120'/f'run-{os.getpid()}-{time.time_ns()}'; out.mkdir(parents=True)
    source=ASSETS_DIR/'route'/'EL5_MIAN_FPC.brd'; board=Path(copy2(source,out/'EL5_MIAN_FPC.brd'))
    helper=ROOT/'stage1_smoke.il'; (out/'stage1_smoke.il').write_bytes(helper.read_bytes()); (out/'ia_scalar_120.py').write_bytes(Path(__file__).read_bytes()); (out/'stage1_smoke.py').write_bytes((ROOT/'stage1_smoke.py').read_bytes())
    with socket.socket() as s: s.bind(('localhost',0)); port=str(s.getsockname()[1])
    os.environ['ALLEGROBRIDGE_LOG_DIRECTORY']=str(out)
    report={'status':'RUNNING','run_dir':str(out),'board':str(board),'port':port,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),'cases':[]}
    os.chdir(out); report['cwd']=os.getcwd(); report['argv']=sys.argv[:]
    (out/'manifest.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    opened=None
    try:
      with Allegro.open(mode='cli',board=board,workspace_id=port,timeout=300.0) as opened:
        ws,session=opened.workspace,opened.session; report['pid']=opened._runtime.process.pid; report['version']=js(ws['axlVersion'](Symbol('fullVersion'))); report['units_accuracy']=js(ws['axlDBGetDesignUnits']())
        snapshot_helper=out/'stage1_smoke.il'; ws['load'](snapshot_helper.resolve().as_posix()); vias0=session.vias(); pad=__import__('collections').Counter(v.padstack for v in vias0).most_common(1)[0][0]
        for i,(label,H,x,T) in enumerate(VALUES):
          for role in ROLES:
            kind='via' if role.startswith('via') else ('line' if role.startswith('line') else 'arc')
            v=(H,x,T); k,a,b,c,direction=call(role,v); before=len(session.routes(net=None,layer=LAYER))+len(session.vias(net=None,layer=LAYER)); rec={'index':i*6+ROLES.index(role),'label':label,'role':role,'kind':kind,'intent_H':str(H),'actual_input':wire(x),'translation_T':str(T),'input':{'start':[wire(a[0]),wire(a[1])],'end':None if b is None else [wire(b[0]),wire(b[1])],'center':None if c is None else [wire(c[0]),wire(c[1])]}}
            try:
              command=cmd('via',a,None,None,pad) if kind=='via' else cmd(kind,a,b,c,pad,'t' if direction else 'nil'); rec['command']=command
              inputs={'start':[wire(a[0]),wire(a[1])],'end':None if kind=='via' else [wire(b[0]),wire(b[1])],'width':wire(WIDTH),'center':None if kind!='arc' else [wire(c[0]),wire(c[1])]}
              raw=ws.transaction(SkillCode(command)); result=js(raw); smoke.assert_echo_inputs(kind,raw,inputs)
              session.refresh(); rec['transaction_return']=result; rec['after_count']=len(session.routes(net=None,layer=LAYER))+len(session.vias(net=None,layer=LAYER)); rec['count_changed']=rec['after_count']==before+1
              rec['requery_kind']=kind
              if kind=='via':
                rows=session.vias(net=None,layer=LAYER); native=fld(raw,'committed'); expected=(float(fld(native,'x')),float(fld(native,'y'))); hit=[r for r in rows if p(r)==expected]
              else:
                rows=session.routes(net=None,layer=LAYER); native=fld(raw,'committed'); st=fld(native,'start'); en=fld(native,'end'); expected=((float(fld(st,'x')),float(fld(st,'y'))),(float(fld(en,'x')),float(fld(en,'y')))); hit=[r for r in rows if r.obj_type==kind and p(r.start)==expected[0] and p(r.end)==expected[1]]
              rec['requery_count']=len(rows); rec['requery_match_count']=len(hit); rec['requery']=js(hit[0]) if len(hit)==1 else None
              if len(hit)!=1: raise RuntimeError(f'requery expected one row, got {len(hit)}')
              smoke.assert_requery_bits(kind,raw,hit[0]); rec['status']='PASS' if rec['count_changed'] else 'FAILED'
            except Exception as e: rec['status']='FAILED'; rec['error']=repr(e)
            report['cases'].append(rec); (out/'cases.jsonl').open('a',encoding='utf-8').write(json.dumps(rec,default=repr)+'\n')
            ws['axlOpenDesignForBatch'](board.resolve().as_posix(),'wf'); session.refresh()
            (out/'manifest.json').write_text(json.dumps(report,indent=2,default=repr),encoding='utf-8')
        report['status']='PASS' if len(report['cases'])==len(VALUES)*len(ROLES) and all(x['status']=='PASS' for x in report['cases']) else 'FAILED'
    except Exception as e: report['status']='FAILED'; report['error']=repr(e)
    report['owned_process_poll_after_context']=None if opened is None else opened._runtime.process.poll(); (out/'manifest.json').write_text(json.dumps(report,indent=2,default=repr),encoding='utf-8'); print(json.dumps({'status':report['status'],'run_dir':str(out),'cases':len(report['cases']),'port':port,'pid':report.get('pid')})); return 0 if report['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
