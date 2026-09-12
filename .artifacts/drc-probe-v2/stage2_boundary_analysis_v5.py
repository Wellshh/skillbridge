from __future__ import annotations
import json,struct
from decimal import Decimal,localcontext
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'results'/'stage2-boundary'/'analysis-v5'; OUT.mkdir(parents=True,exist_ok=True); B=ROOT/'results'/'stage2-boundary'/'run-33608-1789226631112365500'; R=ROOT/'results'/'stage2-boundary-repeat'/'run-73320-1789227627605277800'
def f(x):
 if isinstance(x,dict) and 'bits' in x:return struct.unpack('>d',bytes.fromhex(x['bits']))[0]
 if isinstance(x,dict) and 'value' in x:return f(x['value'])
 return float(x)
def q(x): return Fraction.from_float(f(x))
def p(x,i): return x[i] if isinstance(x,list) else x['xy'[i]]
def grid(x):
 u=q(x)*10000; n,r=divmod(u.numerator,u.denominator); return Fraction(n+(2*r>u.denominator or (2*r==u.denominator and n%2)),10000)
def load(d): return [json.loads(x) for x in (d/'cases.jsonl').read_text().splitlines() if x.strip()]
def calc(c):
 a=next(x['dto'] for x in c['creation']['objects'] if x['name']=='arcA'); l=next(x['dto'] for x in c['creation']['objects'] if x['name']=='lineB'); cy=q(p(a['center'],1)); ly=q(p(l['start'],1)); w=(q(a['width'])+q(l['width']))/2; dx=q(p(a['start'],0))-q(p(a['center'],0)); dy=q(p(a['start'],1))-cy; rr=q(a['radius']);
 api=q(c['settings']['spacing_line_line_numeric']['value']); nom=Fraction(3,50); full=cy-rr-ly-w; g=grid(p(a['center'],1))-grid(a['radius'])-grid(p(l['start'],1))-(grid(a['width'])+grid(l['width']))/2
 with localcontext() as z:
  z.prec=100; ds=Decimal(cy.numerator)/Decimal(cy.denominator)- (Decimal((dx*dx+dy*dy).numerator)/Decimal((dx*dx+dy*dy).denominator)).sqrt()-Decimal(ly.numerator)/Decimal(ly.denominator)-Decimal(w.numerator)/Decimal(w.denominator); ex=q(p(a['end'],0))-q(p(a['center'],0)); ey=q(p(a['end'],1))-cy; de=Decimal(cy.numerator)/Decimal(cy.denominator)-(Decimal((ex*ex+ey*ey).numerator)/Decimal((ex*ex+ey*ey).denominator)).sqrt()-Decimal(ly.numerator)/Decimal(ly.denominator)-Decimal(w.numerator)/Decimal(w.denominator); ad=Decimal(api.numerator)/Decimal(api.denominator); nd=Decimal(nom.numerator)/Decimal(nom.denominator); dsa=ds-ad; dsn=ds-nd; dea=de-ad; den=de-nd
 return {'FULL_B64_WIDTH':(full-api,full-nom),'GRID_NORMALIZED':(g-api,g-nom),'CENTER_FROM_START':(dsa,dsn),'CENTER_FROM_END':(dea,den)}
def main():
 out={'status':'OFFLINE_ANALYSIS_V5_PASS'}
 for name,d in [('boundary',load(B)),('repeat',load(R))]:
  rows=[(f(c['cy']),calc(c),c['gate_verdict']) for c in d]; out[name]={}
  for m in ('FULL_B64_WIDTH','GRID_NORMALIZED','CENTER_FROM_START','CENTER_FROM_END'):
   vals=[(x[1][m][0],x[2]) for x in rows]; ff=[x[0] for x in vals if x[1]=='FLAGGED']; cc=[x[0] for x in vals if x[1]=='CLEAN']; out[name][m]={'max_delta_FLAGGED':str(max(ff,default=0)),'min_delta_CLEAN':str(min(cc,default=0)),'width_or_status':'NON_SEPARATING' if ff and cc and max(ff)>=min(cc) else 'SEPARATING','samples':[{'cy':x[0],'delta_api':str(x[1][m][0]),'delta_nominal':str(x[1][m][1]),'verdict':x[2]} for x in rows]}
 (OUT/'analysis-v5.json').write_text(json.dumps(out,indent=2),encoding='utf8'); print(json.dumps({'status':out['status'],'path':str(OUT/'analysis-v5.json')}))
if __name__=='__main__': main()


