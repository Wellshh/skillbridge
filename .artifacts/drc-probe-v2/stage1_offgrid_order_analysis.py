from decimal import Decimal, localcontext
from fractions import Fraction
import json
import struct
from pathlib import Path

ROOT=Path(__file__).resolve().parent
RAW=ROOT/'results'/'stage1-offgrid-order'/'run-20260912-231222-629'/'manifest.json'
OUT=ROOT/'results'/'stage1-offgrid-order-analysis-v2'
def q(x): return Fraction.from_float(float(x['value']))
def d(x): return Decimal(x.numerator)/Decimal(x.denominator)
def p(a): return (q(a['x']),q(a['y'])) if isinstance(a,dict) else (q(a[0]),q(a[1]))
def dist(a,b):
    with localcontext() as c:
        c.prec=100
        return (d((a[0]-b[0])**2+(a[1]-b[1])**2)).sqrt()
def ulp(a,b):
    ia=struct.unpack('>Q',struct.pack('>d',float(a)))[0]; ib=struct.unpack('>Q',struct.pack('>d',float(b)))[0]; return abs(ia-ib)
def analyse(r):
    req=r['transaction_return']['request']; dto=r['requery']; s=p(req['start']); c0=p(req['center']); e0=p(req['end']); sd=p(dto['start']); ed=p(dto['end']); cdb=p(dto['center']); m=((sd[0]+ed[0])/2,(sd[1]+ed[1])/2); v=(ed[0]-sd[0],ed[1]-sd[1]); w=(c0[0]-m[0],c0[1]-m[1]); den=v[0]*v[0]+v[1]*v[1]; t=(w[0]*v[0]+w[1]*v[1])/den; proj=(c0[0]-t*v[0],c0[1]-t*v[1])
    with localcontext() as ctx:
        ctx.prec=100; rreq=(dist(s,c0)+dist(e0,c0))/Decimal(2); rq=(dist(sd,c0)+dist(ed,c0))/Decimal(2); rdb=(dist(sd,cdb)+dist(ed,cdb))/Decimal(2); db_r=d(q(dto['radius'])); perp=(-v[1],v[0]); plen=(d(v[0]*v[0]+v[1]*v[1])).sqrt(); sign=Decimal(1) if d(c0[0]-m[0])*d(perp[0])+d(c0[1]-m[1])*d(perp[1])>=0 else Decimal(-1)
        def recenter(rr):
            rem=(rr*rr-d(v[0]*v[0]+v[1]*v[1])/Decimal(4)).sqrt(); return (d(m[0])+sign*d(perp[0])/plen*rem,d(m[1])+sign*d(perp[1])/plen*rem)
        rc_req,rc_q=recenter(rreq),recenter(rq)
        models={'R_REQUEST_MEAN':format(rreq,'f'),'R_Q_ENDPOINT_MEAN':format(rq,'f'),'R_DB_ENDPOINT_CENTER_MEAN':format(rdb,'f'),'P_Q_CREQ':{'x':str(proj[0]),'y':str(proj[1])},'RDB_minus_models':{'request':format(db_r-rreq,'f'),'q_endpoint':format(db_r-rq,'f'),'db_endpoint_center':format(db_r-rdb,'f')},'RDB_model_float_ulp':{'request':ulp(db_r,rreq),'q_endpoint':ulp(db_r,rq),'db_endpoint_center':ulp(db_r,rdb)},'CDB_minus_PQ':{'x':format(d(cdb[0]-proj[0]),'f'),'y':format(d(cdb[1]-proj[1]),'f')},'CENTER_REQUEST_MEAN_ON_Q_CHORD':{'x':format(rc_req[0],'f'),'y':format(rc_req[1],'f')},'CENTER_Q_MEAN_RECENTER':{'x':format(rc_q[0],'f'),'y':format(rc_q[1],'f')},'CDB_minus_center_request_recenter':{'x':format(d(cdb[0])-rc_req[0],'f'),'y':format(d(cdb[1])-rc_req[1],'f')},'CDB_minus_center_q_recenter':{'x':format(d(cdb[0])-rc_q[0],'f'),'y':format(d(cdb[1])-rc_q[1],'f')},'radius_db':dto['radius']}
    pre=r['transaction_return']['pre_path']; pre_e=pre['endPoint']; pre_c=pre['arcCenter']; req_e=req['end']; req_c=req['center']; prepath_bits={'end_matches_request':pre_e[0]['bits']==req_e['x']['bits'] and pre_e[1]['bits']==req_e['y']['bits'],'center_matches_request':pre_c[0]['bits']==req_c['x']['bits'] and pre_c[1]['bits']==req_c['y']['bits']}
    return {'label':r['label'],'intent_fraction':r['intent_fraction'],'request':req,'pre_path':pre,'prepath_bits':prepath_bits,'committed':r['transaction_return']['committed'],'requery':dto,'models':models}
def main():
    m=json.loads(RAW.read_text()); rows=[analyse(r) for r in m['cases']]; OUT.mkdir(parents=True,exist_ok=False); out={'raw_manifest':str(RAW),'raw_status':m['status'],'raw_script_sha256':m['script_sha256'],'raw_helper_sha256':m['helper_sha256'],'case_count':len(rows),'reset_all_match':all(r['reset_fingerprint']['matches_initial'] for r in m['cases']),'baseline_hashes':sorted({r['initial_fingerprint']['sha256'] for r in m['cases']}),'sqrt_precision':'Decimal100 approximation','request_to_committed':'difference is allowed and recorded','cases':rows}; (OUT/'analysis.json').write_text(json.dumps(out,indent=2),encoding='utf8'); print(json.dumps({'out':str(OUT/'analysis.json'),'cases':len(rows)}))
if __name__=='__main__': main()
