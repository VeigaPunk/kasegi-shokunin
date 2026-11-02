#!/usr/bin/env python3
import importlib.util,json,pathlib,subprocess,sys,tempfile
root=pathlib.Path(__file__).resolve().parents[3]
engine=root/'corpus/instruments/kernel-report-assess.py';src=engine.read_text()
mutants={
'field-presence':("evidence='needs-evidence' if issues else 'corroborated-synthetic'","evidence='corroborated-synthetic'"),
'ignore-version-binding':("if trace['version']!=v['id']:","if False:"),
'ignore-condition-binding':("if trace['conditions']!=d['conditions']:","if False:"),
'trust-claimed-replay':("result=replay(trace.get('specimen'))","result={'permitted':trace['permitted'],'expected_permitted':c['permitted'],'observation':trace['observation'],'operation':trace['operation']}"),
'ignore-boundary-authority':("c['permitted']!=result['expected_permitted']","False"),
'ai-blanket-reject':("boundary='unestablished'","evidence='needs-evidence' if d['ai_assisted'] else evidence\n boundary='unestablished'"),
'allow-public-reproducer':("elif any(b['kind']=='reproducer' and b['text'].strip() for b in d['public_text']):","elif False:"),
'always-positive':("evidence='needs-evidence' if issues else 'corroborated-synthetic'","issues=[];evidence='corroborated-synthetic'")}
failed=0
with tempfile.TemporaryDirectory(prefix='kasegi-r58-mut-') as td:
 for name,(old,new) in mutants.items():
  if src.count(old)!=1:raise SystemExit('nonunique mutation anchor '+name)
  p=pathlib.Path(td)/'mutant.py';p.write_text(src.replace(old,new))
  r=subprocess.run([sys.executable,str(root/'corpus/instruments/kernel-report-check.py'),'--engine',str(p)],capture_output=True,text=True)
  flips=[]
  for line in r.stdout.splitlines():
   if line.startswith('{'):
    d=json.loads(line)
    if not d['ok'] and d['got'] and d['exit'] in [0,2] and d['got']!=d['want']:flips.append(d['case'])
  killed=r.returncode==1 and bool(flips);failed+=not killed
  print(json.dumps({'mutant':name,'exit':r.returncode,'semantic_flips':flips,'killed':killed}))
print('MUTATIONS total=%d survivors=%d'%(len(mutants),failed));sys.exit(int(bool(failed)))
