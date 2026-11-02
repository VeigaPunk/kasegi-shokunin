"""Actual lane/foreign replay and strict form check; not semantic grading."""
import pathlib,importlib.util,json,sys,subprocess,tempfile
root=pathlib.Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('audit',root/'corpus/instruments/recheck-audit.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
p=root/'corpus/knowledge/cwe-root-cause-assessment.md'
r=a.audit_entry(str(p),str(root),'/tmp');print(json.dumps(r,indent=2));assert r['pass_strict'] and r['lane_exit']==0 and r['foreign_exit']==0
# Missing/corrupted source controls use exact corrected manifests in disposable
# copy; no modification to source captures. Retained source checker must reject.
import shutil
with tempfile.TemporaryDirectory(prefix='k61-source-control-') as d:
 q=pathlib.Path(d);shutil.copytree(root/'corpus/source-snapshots/round-61-correction01',q/'capture');f=q/'capture/S102.txt';f.write_text(f.read_text()+'\ncorruption\n')
 cmd=[sys.executable,str(root/'corpus/instruments/source-recheck.py'),'--manifest',str(q/'capture/manifest.json'),'--source','S102']
 x=subprocess.run(cmd,capture_output=True,text=True);print('CORRUPT',x.returncode,x.stdout);assert x.returncode==1
 f.unlink();x=subprocess.run(cmd,capture_output=True,text=True);print('MISSING',x.returncode,x.stdout);assert x.returncode==2
print('OPERABILITY repaired=true strict=111111 lane=0 foreign=0 negative-controls=2')
