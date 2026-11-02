#!/usr/bin/env python3
# Frozen OSV decision harness. Read-only inputs; selftest uses deleted temp trees.
# Exit 0 all expected decisions match; 1 mismatch; 2 unreadable/tampered input; 64 usage.
import argparse,datetime,hashlib,json,pathlib,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[2]
WAVE=ROOT/'.ufo/waves/round-57'
class Parser(argparse.ArgumentParser):
 def error(self,message): self.exit(64,message+'\n')
def battery(engine,fixtures,verbose=True):
 failures=0
 for case in fixtures:
  p=subprocess.run([sys.executable,str(engine)],input=json.dumps(case['request']),text=True,capture_output=True,timeout=5)
  try: got=json.loads(p.stdout)
  except ValueError: got={'status':'unreadable-output'}
  ok=got==case['expected'] and p.returncode==case['exit']
  failures+=not ok
  if verbose:print('CASE '+case['id']+' '+json.dumps({'got':got,'exit':p.returncode,'want':case['expected'],'want_exit':case['exit'],'ok':ok},sort_keys=True))
 print(f'OSV-CHECK cases={len(fixtures)} failures={failures}')
 return int(bool(failures))
def selftest(fixtures):
 failures=0
 with tempfile.TemporaryDirectory(prefix='osv-harness-') as td:
  for kind in ['clean','wrong-status','wrong-reason','wrong-exit','malformed-output']:
   p=pathlib.Path(td)/'standin.py'
   # Deliberate lookup stand-in proves only harness attainability, never evaluator capability.
   source='import json,sys\nx=json.load(sys.stdin)\nrows='+repr(fixtures)+'\nr=next(r for r in rows if r["request"]==x)\ny=dict(r["expected"])\ncode=r["exit"]\n'
   source+= {'clean':'','wrong-status':'y["status"]="fabricated"\n','wrong-reason':'y["reason"]="fabricated"\n','wrong-exit':'code=99\n','malformed-output':'print("bad-json");sys.exit(0)\n'}[kind]
   p.write_text(source+'print(json.dumps(y));sys.exit(code)\n')
   rc=battery(p,fixtures,False);want=0 if kind=='clean' else 1
   ok=rc==want;failures+=not ok
   print(f'selftest case={kind} finding=OSV-CHECK exit={rc} want={want} ok={ok}')
 print(f'selftest cases=5 failures={failures}')
 return int(bool(failures))
def main():
 p=Parser();p.add_argument('--engine',type=pathlib.Path,default=ROOT/'corpus/instruments/osv-affectedness.py');p.add_argument('--selftest',action='store_true');args=p.parse_args()
 print('run-utc='+datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
 try:
  raw=(WAVE/'fixtures.json').read_bytes();claims=json.loads((WAVE/'claims.json').read_text())
  if hashlib.sha256(raw).hexdigest()!=claims['fixtures_sha256']:print('OSV-INPUT snapshot_tampered');return 2
  fixtures=json.loads(raw)
  if not fixtures or len(fixtures)!=claims['expected_cases']:print('OSV-INPUT fixture-shape');return 2
  if args.selftest:return selftest(fixtures)
  if not args.engine.is_file():print('OSV-INPUT missing-engine');return 2
  return battery(args.engine,fixtures)
 except (OSError,ValueError,KeyError,TypeError,subprocess.TimeoutExpired) as e:print('OSV-INPUT '+type(e).__name__);return 2
if __name__=='__main__':sys.exit(main())
