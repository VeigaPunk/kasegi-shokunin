from pathlib import Path
import subprocess,json,shutil,hashlib
r=Path('/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi'); a=Path(__file__).resolve().parent
entry=r/'corpus/knowledge/vex-evidence-assessment.md';t=entry.read_text(); cmd=next(l.removeprefix('recheck: ') for l in t.splitlines() if l.startswith('recheck: ')); out=[]
for cwd in [r,Path('/tmp')]:
 p=subprocess.run(['bash','-c',cmd],cwd=cwd,capture_output=True,text=True);out.append({'cwd':str(cwd),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
for mode in ['corrupt','missing']:
 d=a/mode;d.mkdir(exist_ok=True);m=r/'corpus/source-snapshots/round-62/manifest.json';shutil.copy(m,d/'manifest.json');s=r/'corpus/source-snapshots/round-62/S108.txt'
 if mode=='corrupt':(d/'S108.txt').write_bytes(s.read_bytes()+b'\ncorruption\n')
 p=subprocess.run(['python3',str(r/'corpus/instruments/source-recheck.py'),'--manifest',str(d/'manifest.json'),'--source','S108'],cwd='/tmp',capture_output=True,text=True);out.append({'mode':mode,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
(a/'entry-operability.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
