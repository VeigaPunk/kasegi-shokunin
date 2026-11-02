import json,pathlib,subprocess,sys
p=pathlib.Path(__file__).parent; cases=json.loads((p/'cases.json').read_text()); results=[]
for c in cases:
 f=p/'input.json';f.write_text(json.dumps(c['input']));r=subprocess.run([sys.executable,str(p/'candidate/corpus/instruments/kernel-report-assess.py'),str(f)],capture_output=True,text=True)
 try:o=json.loads(r.stdout)
 except ValueError:o={}
 bad=[]
 for k,want in c['expected'].items():
  got=r.returncode if k=='exit' else o.get(k)
  if want is not None and got not in (want if isinstance(want,list) else [want]):bad.append({'key':k,'expected':want,'got':got})
 results.append({'id':c['id'],'exit':r.returncode,'output':o,'stderr':r.stderr,'mismatches':bad});print(c['id'], 'FAIL' if bad else 'PASS',bad)
(p/'results.json').write_text(json.dumps(results,indent=2)+'\n');print('cases',len(results),'failed',sum(bool(r['mismatches']) for r in results))
