from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parent
RUN=ROOT/'results'/'stage3-translation'/'run-29568-1789228092086311600'/'manifest.json'
OUT=ROOT/'results'/'stage3-translation-analysis'

def frac(x):
    return Fraction(str(x))
def main():
    d=json.loads(RUN.read_text(encoding='utf8')); rows=[]
    for c in d['cases']:
        objs=c.get('creation',{}).get('objects',[])
        arc=next((o for o in objs if o.get('name')=='arcA'),{})
        line=next((o for o in objs if o.get('name')=='lineB'),{})
        rows.append({'label':c['label'],'translation':c['translation'],'line_y':c.get('line_y'),'center_y':c.get('center_y'),'gate_verdict':c.get('audit_view',{}).get('gate_verdict'),'gate_evidence':c.get('audit_view',{}).get('gate_evidence'),'arc_actual_relative_fraction':arc.get('actual_relative_fraction'),'line_actual_relative_fraction':line.get('actual_relative_fraction'),'arc_dto':arc.get('dto'),'line_dto':line.get('dto')})
    result={'source':str(RUN),'case_count':len(rows),'rows':rows,'interpretation':{'origin_case_is_T0':'flag_T0_0 and clean_T0_0 retain the same translated construction at origin','translation_effect':'observed clearance changes are transport/geometry-bit effects; they do not identify a comparator or DRC rule','reported_delta_from_root':{'T-300':'13/4503599627370496','T-600':'71/4503599627370496'},'scope':'offline evidence reduction; no new DRC inference'}}
    OUT.mkdir(parents=True,exist_ok=True); (OUT/'stage3_translation_analysis.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8'); print(json.dumps({'out':str(OUT/'stage3_translation_analysis.json'),'cases':len(rows)}))
if __name__=='__main__': main()
