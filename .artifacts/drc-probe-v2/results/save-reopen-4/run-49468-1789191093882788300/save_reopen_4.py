from __future__ import annotations
import hashlib,json,os,socket,sys,time
from pathlib import Path
from shutil import copy2
from allegrobridge import Allegro,SkillCode,Symbol
from allegrobridge.util import ASSETS_DIR
import traceback
ROOT=Path(__file__).resolve().parent; SRC=ASSETS_DIR/'route'/'EL5_MIAN_FPC.brd'; LAYER='ETCH/TOP'
CASES=['d0_s1_b1','d0_s1_b4','d3_s2_b1','d3_s2_b4']
import stage1_smoke as smoke
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
def port():
 with socket.socket() as s: s.bind(("localhost",0)); return str(s.getsockname()[1])
def endpoint_pair(native):
 st,en=fld(native,"start"),fld(native,"end"); return ((float(fld(st,"x")),float(fld(st,"y"))),(float(fld(en,"x")),float(fld(en,"y"))))
def target(session,exp):
 return [r for r in session.routes(net=None,layer=LAYER) if getattr(r,"obj_type",None)=="arc" and p(r.start)==exp[0] and p(r.end)==exp[1]]
def append(out,rec):
 with (out/"cases.jsonl").open("a",encoding="utf-8") as f: f.write(json.dumps(rec,default=repr)+"\n")

def main():
    os.environ.setdefault("CDSROOT", r"D:\Cadence\Cadence_SPB_17.2-2016")
    os.environ.setdefault("Sigrity_EDA_DIR", r"D:\Cadence\Cadence_SPB_17.2-2016")
    os.environ.setdefault("CDS_LIC_FILE", "5280@localhost")
    srcjson = ROOT / "results" / "ib-center-40" / "run-66284-1789189802536493400" / "cases.jsonl"
    rows = {}
    for line in srcjson.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("label") in CASES: rows[row["label"]] = row
    out = ROOT / "results" / "save-reopen-4" / f"run-{os.getpid()}-{time.time_ns()}"
    out.mkdir(parents=True)
    helper = ROOT / "stage1_smoke.il"
    (out / "save_reopen_4.py").write_bytes(Path(__file__).read_bytes())
    (out / "stage1_smoke.il").write_bytes(helper.read_bytes())
    (out / "stage1_smoke.py").write_bytes((ROOT / "stage1_smoke.py").read_bytes())
    source_hash = hashlib.sha256(SRC.read_bytes()).hexdigest()
    report = {"status":"RUNNING", "run_dir":str(out), "source_sha256":source_hash,
              "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "helper_sha256":hashlib.sha256(helper.read_bytes()).hexdigest(), "cases":[],
              "argv":sys.argv[:], "cwd":str(out), "dependency_snapshots":["save_reopen_4.py","stage1_smoke.py","stage1_smoke.il"]}
    os.chdir(out); (out / "manifest.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    for label in CASES:
        row=rows[label]; case={"label":label,"command":row["command"],"intent_H":row.get("H"),"creation":{},"save":{},"reopen":{}}
        board=Path(copy2(SRC,out/f"{label}-initial.brd")); saved=out/f"{label}-saved.brd"; expected=None
        p1=port(); p1dir=out/f"{label}-p1"; p1dir.mkdir(); os.chdir(p1dir); os.environ["ALLEGROBRIDGE_LOG_DIRECTORY"]=str(p1dir); opened1=None
        try:
            with Allegro.open(mode="cli",board=board,workspace_id=p1,timeout=300.0) as opened1:
                ws,session=opened1.workspace,opened1.session
                case["creation"].update({"pid":opened1._runtime.process.pid,"port":p1,"version":js(ws["axlVersion"](Symbol("fullVersion"))),"units_accuracy":js(ws["axlDBGetDesignUnits"]())})
                ws["load"]((out/"stage1_smoke.il").resolve().as_posix())
                raw=ws.transaction(SkillCode(row["command"])); case["creation"]["transaction_return"]=js(raw)
                inputs=dict(row["input"]); inputs["width"]=wire(0.15); smoke.assert_echo_inputs("arc",raw,inputs); case["creation"]["echo_assert"]=True; session.refresh()
                expected=endpoint_pair(fld(raw,"committed")); hits=target(session,expected)
                case["creation"]["requery_count"]=len(hits); case["creation"]["requery_all_target_dto"]=[js(x) for x in hits]
                if len(hits)!=1: raise RuntimeError(f"creation endpoint target count={len(hits)}")
                smoke.assert_requery_bits("arc",raw,hits[0]); case["creation"].update({"requery_bits_assert":True,"dto":js(hits[0]),"valid":True})
                saved_result=ws["axlSaveDesign"](design=saved.resolve().as_posix(),noMru=True,noConfirm=True)
                case["save"].update({"return":js(saved_result),"exists":saved.exists(),"sha256":hashlib.sha256(saved.read_bytes()).hexdigest() if saved.exists() else None,"source_hash_unchanged":hashlib.sha256(SRC.read_bytes()).hexdigest()==source_hash})
                case["save"]["ok"]=bool(saved_result) and saved.exists(); session.refresh(); post=target(session,expected)
                case["save"]["fresh_requery_count"]=len(post); case["save"]["fresh_requery_all_target_dto"]=[js(x) for x in post]
                if len(post)==1:
                    case["save"]["fresh_dto"]=js(post[0]); case["save"]["observable_state"]="STABLE" if case["creation"]["dto"]==case["save"]["fresh_dto"] else "CHANGED"
                else: case["save"]["observable_state"]="AMBIGUOUS"; case["save"]["post_unique"] = False
        except Exception: case["creation"].setdefault("valid",False); case["creation"]["traceback"]=traceback.format_exc()
        case["creation"]["process_poll"]=None if opened1 is None else opened1._runtime.process.poll()
        if saved.exists() and expected is not None:
            p2=port(); p2dir=out/f"{label}-p2"; p2dir.mkdir(); os.chdir(p2dir); os.environ["ALLEGROBRIDGE_LOG_DIRECTORY"]=str(p2dir); opened2=None
            try:
                with Allegro.open(mode="cli",board=saved,workspace_id=p2,timeout=300.0) as opened2:
                    ws2,session2=opened2.workspace,opened2.session
                    case["reopen"].update({"pid":opened2._runtime.process.pid,"port":p2,"version":js(ws2["axlVersion"](Symbol("fullVersion"))),"units_accuracy":js(ws2["axlDBGetDesignUnits"]())}); session2.refresh(); matches=target(session2,expected)
                    arcs=[js(x) for x in session2.routes(net=None,layer=LAYER) if getattr(x,"obj_type",None)=="arc"]
                    case["reopen"].update({"routes_count":len(arcs),"all_arc_dto":arcs,"target_match_count":len(matches),"target_dto":js(matches[0]) if len(matches)==1 else None,"ok":len(matches)==1})
                    if len(matches)==1: case["reopen"]["observable_state"]="STABLE" if case["save"].get("fresh_dto")==case["reopen"]["target_dto"] else "CHANGED"
            except Exception: case["reopen"]["ok"]=False; case["reopen"]["traceback"]=traceback.format_exc()
            case["reopen"]["process_poll"]=None if opened2 is None else opened2._runtime.process.poll()
        case["status"]="PASS" if case["creation"].get("valid") and case["save"].get("ok") and case["reopen"].get("ok") else "FAILED"; report["cases"].append(case); append(out,case); (out/"manifest.json").write_text(json.dumps(report,indent=2,default=repr),encoding="utf-8")
    report["status"]="PASS" if len(report["cases"])==4 and all(x["status"]=="PASS" for x in report["cases"]) else "FAILED"; (out/"manifest.json").write_text(json.dumps(report,indent=2,default=repr),encoding="utf-8"); print(json.dumps({"status":report["status"],"run_dir":str(out),"cases":len(report["cases"])})); return 0 if report["status"]=="PASS" else 1
if __name__=='__main__': raise SystemExit(main())






