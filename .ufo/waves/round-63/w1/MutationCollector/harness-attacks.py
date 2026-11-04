import hashlib,pathlib,subprocess,sys
S=pathlib.Path('/fast/scratch/hyaku/kasegi-r63/MutationCollector')
W=pathlib.Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-63/w1/MutationCollector')
H=S/'collector.py'; I=S/'figure-audit.py'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original=I.read_bytes(); before=sha(I)
print('axes=depth:verifiability; collector_copy=exact-proposed-bytes',flush=True)
print('collector_sha256='+sha(H)+' instrument_before_sha256='+before,flush=True)
(W/'collector-tested.py').write_bytes(H.read_bytes())
def run(name,instrument,work,mode='base',expected=0):
 cmd=[sys.executable,str(H),'--instrument',str(instrument),'--work',str(work),'--mode',mode]
 print('CASE '+name+' expected_exit='+str(expected)+' argv='+repr(cmd),flush=True)
 p=subprocess.run(cmd,cwd=S,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 sys.stdout.buffer.write(p.stdout);sys.stdout.buffer.flush()
 print('OBSERVED exit='+str(p.returncode)+' matches_expected='+str(p.returncode==expected),flush=True)
 return p.returncode
run('pristine',I,S/'normal',expected=0)
run('missing-instrument',S/'nonexistent.py',S/'missing-run',expected=2)
block=S/'blocked';block.write_text('sentinel\n')
run('unusable-work',I,block,expected=2)
under=S/'under';under.mkdir(exist_ok=True)
inside=under/'audit.py';inside.write_bytes(original)
run('instrument-under-work',inside,under,expected=2)
print('under_instrument_preserved='+str(inside.read_bytes()==original)+' unusable_sentinel='+repr(block.read_text()),flush=True)
try:
 I.write_bytes((W/'always-green.py').read_bytes())
 print('mutant=always-green audit_sha256='+sha(I),flush=True)
 run('always-green-fake-audit',I,S/'fake-run',mode='candidate',expected=1)
 # Same counterfeit result bytes, but every successful-looking result returns 7.
 I.write_bytes((W/'always-green.py').read_bytes()+b'raise SystemExit(7)\n')
 print('mutant=output-nonzero-mismatch audit_sha256='+sha(I),flush=True)
 run('nonzero-output-mismatch',I,S/'mismatch-run',mode='base',expected=1)
finally:
 I.write_bytes(original)
 print('restored_sha256='+sha(I)+' equals_before='+str(I.read_bytes()==original),flush=True)
 run('restored',I,S/'restored-run',expected=0)
