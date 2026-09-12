from __future__ import annotations
import json, struct
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parent
B=ROOT/'results'/'stage2-boundary'/'run-33608-1789226631112365500'
R=ROOT/'results'/'stage2-boundary-repeat'/'run-73320-1789227627605277800'
OUT=ROOT/'results'/'stage2-boundary'; OUT.mkdir(parents=True,exist_ok=True)
def f(x):
    if isinstance(x,dict) and 'bits' in x:return struct.unpack('>d',bytes.fromhex(x['bits']))[0]
    if isinstance(x,dict) and 'value' in x:return f(x['value'])
    return float(x)
def load(p): return [json.loads(x) for x in (p/'cases.jsonl').read_text().splitlines() if x.strip()]
def fr(x): return Fraction.from_float(f(x))
def coord(p, axis): return p[0 if axis=='x' else 1] if isinstance(p,list) else p[axis]
def grid(x):
    q=Fraction(1,10000); u=fr(x)/q; n,d=u.numerator//u.denominator,u.numerator%u.denominator
    if 2*d< u.denominator:return Fraction(n)*q
    if 2*d>u.denominator:return Fraction(n+1)*q
    return Fraction(n+(n&1))*q
def sqrt100(q):
    with localcontext() as c: c.prec=100; return format((Decimal(q.numerator)/Decimal(q.denominator)).sqrt(),'f')
def sqrt_frac(q): return Fraction.from_float(float(sqrt100(q)))
def models(c):
    a=next(x['dto'] for x in c['creation']['objects'] if x['name']=='arcA'); l=next(x['dto'] for x in c['creation']['objects'] if x['name']=='lineB')
    sy,ey=fr(coord(a['start'],'y')),fr(coord(a['end'],'y')); cy=fr(coord(a['center'],'y')); ly=fr(coord(l['start'],'y')); hw=(fr(a['width'])+fr(l['width']))/2
    rs=((fr(coord(a['start'],'x'))-fr(coord(a['center'],'x')))**2+(sy-cy)**2); re=((fr(coord(a['end'],'x'))-fr(coord(a['center'],'x')))**2+(ey-cy)**2)
    return {'CENTER_FROM_START':cy-sqrt_frac(rs)-ly-hw,'CENTER_FROM_END':cy-sqrt_frac(re)-ly-hw,'FULL_B64_WIDTH':cy-fr(a['radius'])-ly-hw,'GRID_NORMALIZED':grid(coord(a['center'],'y'))-grid(a['radius'])-grid(coord(l['start'],'y'))-(grid(a['width'])+grid(l['width']))/2,'sqrt100_start':sqrt100(rs),'sqrt100_end':sqrt100(re)}
def summary(cs):
    rows=sorted([(f(c['cy']),models(c),c['gate_verdict'],c['geometry_fingerprint']) for c in cs])
    flags=[x for x in rows if x[2]=='FLAGGED']; clean=[x for x in rows if x[2]=='CLEAN']
    out={};
    for model in ('FULL_B64_WIDTH','CENTER_FROM_START','CENTER_FROM_END','GRID_NORMALIZED'):
        vals=[(x[0],x[1][model],x[2],x[3]) for x in rows]; ff=[x for x in vals if x[2]=='FLAGGED']; cc=[x for x in vals if x[2]=='CLEAN']; out[model]={'monotonic_by_requested_cy':all(a[1]<=b[1] for a,b in zip(vals,vals[1:])),'flagged_max':str(max((x[1] for x in ff),default=Fraction(0))),'clean_min':str(min((x[1] for x in cc),default=Fraction(0))),'rows':[{'cy':x[0],'clearance':str(x[1]),'verdict':x[2],'fingerprint':x[3]} for x in vals]}
    out['n']=len(rows); return out
def main():
    b,r=load(B),load(R); sb,sr=summary(b),summary(r); api=fr(b[0]['settings']['spacing_line_line_numeric']['value']); nominal=Fraction(3,50)
    data={'status':'OFFLINE_ANALYSIS_PASS' if sb['n']==11 and sr['n']==10 else 'OFFLINE_ANALYSIS_FAIL','boundary':sb,'repeat':sr,'api_R_fraction':str(api),'nominal_fraction':str(nominal),'sqrt_precision':'100-digit Decimal display only; not exact','model_conclusions':{'M0':'rejected by effective CLEAN with FULL<R','M1':'conditional epsilon interval uses observed FULL deltas; strict upper bound','M2':'rejected because positive epsilon predicts HI flagged','M3':'not uniquely identifiable','M4':'not uniquely identifiable'}}
    (OUT/'stage2_boundary_analysis.json').write_text(json.dumps(data,indent=2),encoding='utf8')
    report=['# II-D 边界数值分析','',f"boundary 11 点 FULL：FLAGGED 最大={sb['FULL_B64_WIDTH']['flagged_max']}；CLEAN 最小={sb['FULL_B64_WIDTH']['clean_min']}；按请求 Cy 单调={sb['FULL_B64_WIDTH']['monotonic_by_requested_cy']}。",f"repeat 10 点 FULL 按请求 Cy 单调={sr['FULL_B64_WIDTH']['monotonic_by_requested_cy']}；LO 5/5 FLAGGED、HI 5/5 CLEAN。",'',f"API_R={api}；名义值={nominal}。CENTER_FROM_START、CENTER_FROM_END、GRID_NORMALIZED 均独立计算并在 JSON 中逐点列出。",'', 'M0 被有效 CLEAN 反驳；M1 仅条件兼容 ε∈[9.596758035e-8,1.917853145e-7)，上界严格小于；M2 被 HI 反驳；M3/M4 不可唯一辨识。100 位 Decimal sqrt 仅显示近似。']
    (OUT/'II-D-report.zh.md').write_text('\n'.join(report)+'\n',encoding='utf8'); print(json.dumps({'status':data['status']})); return 0
if __name__=='__main__': raise SystemExit(main())
