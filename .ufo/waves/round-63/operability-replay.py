"""Actual documented command replay and corrupt/missing controls; not semantic grader."""
import pathlib,importlib.util,json,subprocess,tempfile,shutil,sys
root=pathlib.Path(__file__).resolve().parents[3]
s=importlib.util.spec_from_file_location('audit',root/'corpus/instruments/recheck-audit.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
r=a.audit_entry(str(root/'corpus/knowledge/cna-causal-counting.md'),str(root),'/tmp');print(json.dumps(r,indent=2));assert r['pass_strict'] and r['lane_exit']==r['foreign_exit']==0 and r['lane_output_sha256']==r['foreign_output_sha256']
with tempfile.TemporaryDirectory(prefix='k63-source-control-') as d:
 p=pathlib.Path(d)/'capture';shutil.copytree(root/'corpus/source-snapshots/round-63',p);f=p/'S110.txt';f.write_bytes(f.read_bytes()+b'\ncorruption\n')
 cmd=[sys.executable,str(root/'corpus/instruments/source-recheck.py'),'--manifest',str(p/'manifest.json'),'--source','S110']
 for name,want in [('CORRUPT',1),('MISSING',2)]:
  if name=='MISSING':f.unlink()
  x=subprocess.run(cmd,capture_output=True,text=True);print(name,x.returncode,x.stdout);assert x.returncode==want
print('OPERABILITY strict=111111 lane=0 foreign=0 negative-controls=2')
