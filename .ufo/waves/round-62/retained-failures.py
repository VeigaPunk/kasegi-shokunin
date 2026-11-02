"""Compare actual per-entry legacy recheck behavior; red totals do not hide new red."""
import pathlib,subprocess,tempfile,importlib.util,json,tarfile,io
root=pathlib.Path(__file__).resolve().parents[3];base='f282e44e17c20d4587977412398a8a5136ae1524'
s=importlib.util.spec_from_file_location('audit',root/'corpus/instruments/recheck-audit.py');a=importlib.util.module_from_spec(s);s.loader.exec_module(a)
with tempfile.TemporaryDirectory(prefix='k62-base-') as d:
 p=pathlib.Path(d);raw=subprocess.check_output(['git','-C',str(root),'archive',base,'corpus']);tarfile.open(fileobj=io.BytesIO(raw)).extractall(p,filter='data')
 bad=[];n=0
 for old in sorted((p/'corpus/knowledge').glob('*.md')):
  new=root/'corpus/knowledge'/old.name
  # Context is explicitly the real lane for both historical documented commands.
  b=a.audit_entry(str(old),str(root),'/tmp');c=a.audit_entry(str(new),str(root),'/tmp')
  keys=['command','limbs','strict','missing_paths','cd_target','lane_exit','foreign_exit','class','pass','pass_strict']
  changed=[k for k in keys if b.get(k)!=c.get(k)]
  print('LEGACY',old.name,'before='+str(b.get('class')),'after='+str(c.get('class')),'changed='+','.join(changed));n+=1
  if changed:bad.append(old.name)
 print('LEGACY-COMPARE entries='+str(n)+' changed='+str(len(bad)));assert not bad,bad
