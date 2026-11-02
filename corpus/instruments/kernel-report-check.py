#!/usr/bin/env python3
"""Frozen synthetic assessment decision gate. 0 clean; 1 mismatch; 2 unavailable/tampered."""
import argparse,hashlib,json,pathlib,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[2]
WAVE=ROOT/'.ufo/waves/round-58'
def run(engine, cases):
 failures=0
 with tempfile.TemporaryDirectory(prefix='kasegi-report-') as td:
  for c in cases:
   p=pathlib.Path(td)/'input.json';p.write_text(json.dumps(c['input']))
   r=subprocess.run([sys.executable,str(engine),str(p)],capture_output=True,text=True,timeout=10)
   try: out=json.loads(r.stdout); got={k:out.get(k) for k in c['expected']}
   except (ValueError,AttributeError):got={}
   ok=r.returncode==c['exit'] and got==c['expected']
   failures+=not ok
   print(json.dumps({'case':c['id'],'ok':ok,'exit':r.returncode,'got':got,'want':c['expected'],'stderr':r.stderr}))
 print('REPORT-CHECK cases=%d failures=%d'%(len(cases),failures))
 return int(bool(failures))
def main():
 a=argparse.ArgumentParser();a.add_argument('--engine',default=str(ROOT/'corpus/instruments/kernel-report-assess.py'));a.add_argument('--selftest',action='store_true');x=a.parse_args()
 try:
  raw=(WAVE/'fixtures.json').read_bytes();pin=json.loads((WAVE/'freeze.json').read_text())
  if hashlib.sha256(raw).hexdigest()!=pin['fixtures_sha256']:raise ValueError('snapshot_tampered')
  cases=json.loads(raw)
  if x.selftest:
   # Actual CLI substitutes, not helper-only assertion tests.
   failed=0
   with tempfile.TemporaryDirectory(prefix='kasegi-report-gate-') as td:
    for label,body in [('always-positive',"import json;print("+repr(json.dumps(cases[0]['expected']))+")"),('always-incomplete',"print('{\"evidence\":\"needs-evidence\",\"boundary\":\"unestablished\",\"disclosure\":\"public-status-only\"}')"),('empty-output','pass'),('wrong-exit',"print("+repr(json.dumps(cases[0]['expected']))+");raise SystemExit(2)")]:
     p=pathlib.Path(td)/'stub.py';p.write_text(body)
     rc=run(p,cases);print('CONTROL '+label+' rejected='+str(rc==1));failed+=rc!=1
   print('SELFTEST controls=4 failures='+str(failed));return int(bool(failed))
  if not pathlib.Path(x.engine).is_file():raise ValueError('engine-unavailable')
  return run(pathlib.Path(x.engine),cases)
 except (OSError,ValueError,subprocess.TimeoutExpired) as e:
  print('REPORT-CHECK could-not-evaluate '+str(e));return 2
if __name__=='__main__':sys.exit(main())
