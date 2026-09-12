from __future__ import annotations
import json,struct
from decimal import Decimal,localcontext
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'results'/'stage2-boundary'/'analysis-v3'; OUT.mkdir(parents=True,exist_ok=True)
B=ROOT/'results'/'stage2-boundary'/'run-33608-1789226631112365500'; R=ROOT/'results'/'stage2-boundary-repeat'/'run-73320-1789227627605277800'
def f(x):
 if isinstance(x,dict) and 'bits' in x:return struct.unpack('>d',bytes.fromhex(x['bits']))[0]
 if isinstance(x,dict) and 'value' in x:return f(x['value'])
 return float(x)
def p(x,i): return x[i] if isinstance(x,list) else x['xy'[i]]
def q(x): return Fraction.from_float(f(x))
def load(d): return [json.loads(x) for x in (d/'cases.jsonl').read_text().splitlines() if x.strip()]
def calc(c):
 a=next(x['dto'] for x in c['creation']['objects'] if x['name']=='arcA'); l=next(x['dto'] for x in c['creation']['objects'] if x['name']=='lineB'); cy=q(p(a['center'],1)); ly=q(p(l['start'],1)); w=(q(a['width'])+q(l['width']))/2; dx=q(p(a['start'],0))-q(p(a['center'],0)); dy=q(p(a['start'],1))-q(p(a['center'],1)); ex=q(p(a['end'],0))-q(p(a['center'],0)); ey=q(p(a['end'],1))-q(p(a['center'],1));
 with localcontext() as z:
  z.prec=100; rs=(Decimal(dx.numerator*dx.denominator and (dx*dx).numerator)/Decimal((dx*dx).denominator)+Decimal((dy*dy).numerator)/Decimal((dy*dy).denominator)).sqrt(); re=(Decimal((ex*ex).numerator)/Decimal((ex*ex).denominator)+Decimal((ey*ey).numerator)/Decimal((ey*ey).denominator)).sqrt(); cys=Decimal(cy.numerator)/Decimal(cy.denominator); lys=Decimal(ly.numerator)/Decimal(ly.denominator); h=Decimal(w.numerator)/Decimal(w.denominator); start=cys-rs-lys-h; end=cys-re-lys-h
 return {'FULL_B64_WIDTH':cy-q(a['radius'])-ly-w,'GRID_NORMALIZED':q(round(f(p(a['center'],1)),4))-q(round(f(a['radius']),4))-q(round(f(p(l['start'],1)),4))- (q(round(f(a['width']),4))+q(round(f(l['width']),4)))/2,'CENTER_FROM_START':str(start),'CENTER_FROM_END':str(end)}
def main():
 out={};
 for name,data in [('boundary',load(B)),('repeat',load(R))]:
  rows=[(f(c['cy']),calc(c),c['gate_verdict'],c['geometry_fingerprint']) for c in data]; out[name]={}
  for m in ('FULL_B64_WIDTH','GRID_NORMALIZED','CENTER_FROM_START','CENTER_FROM_END'):
   vals=[x for x in rows if x[2] in ('FLAGGED','CLEAN')]; nums=[(Decimal(str(x[1][m])) if isinstance(x[1][m],str) else Decimal(x[1][m].numerator)/Decimal(x[1][m].denominator),x) for x in vals]; ff=[x for x in nums if x[1][2]=='FLAGGED']; cc=[x for x in nums if x[1][2]=='CLEAN']; out[name][m]={'max_delta_FLAGGED':str(max((x[0] for x in ff),default=Decimal(0))),'min_delta_CLEAN':str(min((x[0] for x in cc),default=Decimal(0))),'width_or_status':('NON_SEPARATING' if ff and cc and max(x[0] for x in ff)>=min(x[0] for x in cc) else str(min((x[0] for x in cc),default=Decimal(0))-max((x[0] for x in ff),default=Decimal(0)) ))}
 out['status']='OFFLINE_ANALYSIS_V3_PASS'; (OUT/'analysis-v3.json').write_text(json.dumps(out,indent=2),encoding='utf8'); print(json.dumps({'status':out['status'],'path':str(OUT/'analysis-v3.json')}))
if __name__=='__main__': main()
