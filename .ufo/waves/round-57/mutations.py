#!/usr/bin/env python3
# Execute prospective mutants against frozen answers. Exit 0 all killed, 1 survivor, 2 setup.
import datetime,hashlib,json,pathlib,subprocess,sys,tempfile
R=pathlib.Path(__file__).resolve().parents[3];engine=R/'corpus/instruments/osv-affectedness.py';harness=R/'corpus/instruments/osv-semantic-check.py'
src=engine.read_text();freeze=json.loads((R/'.ufo/waves/round-57/claims.json').read_text())
recordwide=" flat={k for a in osv.get('affected',[]) for r in a.get('ranges',[]) for e in r.get('events',[]) for k in e}\n if 'fixed' in flat and 'last_affected' in flat:raise Invalid('mixed-closures')\n entries=[]"
patches={
 'always-affected':("def evaluate(request):","def evaluate(request):\n return {'status':'affected','reason':'range-match'}"),
 'always-unaffected':("def evaluate(request):","def evaluate(request):\n return {'status':'unaffected','reason':'no-match'}"),
 'range-only':("if v in versions:","if False:"),
 'boundary-swap':("elif k=='fixed' and query>=n:","elif k=='fixed' and query>n:"),
 'recordwide-exclusion':(' entries=[]',recordwide),
 'wrong-package':("if identity(a.get('package'))!=target:continue","if False:continue"),
 'ecosystem-as-semver':("if r['type']!='SEMVER':","if r['type'] not in ('SEMVER','ECOSYSTEM'):"),
 'git-as-semver':("if r['type']!='SEMVER':","if r['type'] not in ('SEMVER','GIT'):"),
 'lexical-sort':("return tuple(int(x) for x in v.split('.'))","return tuple(x for x in v.split('.'))"),
 'limits-and':("not any(n is None or query<n for n in limits)","not all(n is None or query<n for n in limits)"),
 'unsorted-events':("for n,k in sorted(events):","for n,k in events:")}
print('run-utc='+datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'));print('engine-sha256='+hashlib.sha256(src.encode()).hexdigest())
assert set(patches)==set(freeze['mutants'])
failures=0
with tempfile.TemporaryDirectory(prefix='osv-mutants-') as td:
 for name,(old,new) in patches.items():
  assert src.count(old)==1,(name,src.count(old))
  mutated=src.replace(old,new);compile(mutated,name,'exec');f=pathlib.Path(td)/(name+'.py');f.write_text(mutated)
  p=subprocess.run([sys.executable,str(harness),'--engine',str(f)],text=True,capture_output=True)
  # Count actual status flips separately: reason-only changes never suffice.
  flips=[]
  for line in p.stdout.splitlines():
   if line.startswith('CASE '):
    _,id,rest=line.split(' ',2);d=json.loads(rest)
    if d['got'].get('status')!=d['want']['status']:flips.append(id)
  killed=p.returncode==1 and bool(flips);failures+=not killed
  print(f'MUTANT {name} exit={p.returncode} status-flips={len(flips)} cases={",".join(flips)} killed={killed}')
 # Model faithfully reconstructs the two erroneous sentences. Not historical code.
 model=src.replace(*patches['range-only']).replace(*patches['recordwide-exclusion'])
 f=pathlib.Path(td)/'legacy-reading-model.py';f.write_text(model)
 p=subprocess.run([sys.executable,str(harness),'--engine',str(f)],text=True,capture_output=True)
 print('BEFORE-MODEL constructed-from=README-F31-and-knowledge-Claim3 not-historical-executable=true')
 print(p.stdout,end='');print('before-model-exit='+str(p.returncode))
print(f'mutations={len(patches)} failures={failures}')
sys.exit(int(bool(failures)))
