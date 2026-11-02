#!/usr/bin/env python3
"""Read-only replay of frozen independent cases. Exit0 match,1 mismatch,2 setup error.
Uses committed original engine and isolated temporary runner; retains filed receipts.
"""
import pathlib,hashlib,json,subprocess,sys,tempfile,shutil
p=pathlib.Path(__file__).resolve().parent;repo=p.parents[2]
try:
 cases=(p/'cases.json').read_bytes()
 assert hashlib.sha256(cases).hexdigest()=='c7a7195db72b3fa9cab349be9b218de5d89f260052b03075dfc0e8fcec31a103'
 engine=subprocess.check_output(['git','-C',str(repo),'show','ee0e72d9f08b7bb4681126676c723c9cc9208361:corpus/instruments/kernel-report-assess.py'])
 with tempfile.TemporaryDirectory(prefix='kasegi58-review-') as t:
  q=pathlib.Path(t);(q/'cases.json').write_bytes(cases);shutil.copyfile(p/'run.py',q/'run.py');e=q/'candidate/corpus/instruments/kernel-report-assess.py';e.parent.mkdir(parents=True);e.write_bytes(engine)
  r=subprocess.run([sys.executable,'-B',str(q/'run.py')],capture_output=True,text=True);print(r.stdout,end='');print(r.stderr,end='',file=sys.stderr)
  if r.returncode:raise RuntimeError('runner_failed')
  results=json.loads((q/'results.json').read_text());assert len(results)==30
  raise SystemExit(1 if any(x['mismatches'] for x in results) else 0)
except (AssertionError,OSError,ValueError,RuntimeError,subprocess.SubprocessError) as e:
 print('setup_error:',type(e).__name__,file=sys.stderr);raise SystemExit(2)
