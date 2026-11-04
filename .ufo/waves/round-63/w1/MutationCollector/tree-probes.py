import hashlib,json,pathlib,subprocess,sys
L=pathlib.Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin')
S=pathlib.Path('/fast/scratch/hyaku/kasegi-r63/MutationCollector')
S.mkdir(parents=True,exist_ok=True)
source=subprocess.check_output(['git','-C',str(L),'show','fdccc6da803965234c1eff5a0fee38b97e6621c1:corpus/instruments/figure-audit.py'])
audit=S/'figure-audit.py'; audit.write_bytes(source)
root=S/'tree'; (root/'corpus/instruments').mkdir(parents=True,exist_ok=True)
(root/'present.txt').write_text('present\n')
(root/'corpus/instruments/fail.py').write_text('raise SystemExit(7)\n')
prose=root/'claim.md'; prose.write_text('Upstream positive exit>1 errors must be stale. grep no-match exit1 counting and existing final-stage behavior retained.\n')
sha=lambda b:hashlib.sha256(b).hexdigest()
print('axes=depth:verifiability; isolation=own-scratch; base=fdccc6da803965234c1eff5a0fee38b97e6621c1',flush=True)
print('audit_sha256='+sha(source)+' prose_sha256='+sha(prose.read_bytes()),flush=True)
# All four named error classes plus three independently varied tree shapes.
cases=[('cat-missing','cat missing.txt | wc -l',1),('grep-invalid',"grep '[' present.txt | wc -l",1),('git-bad-ref','git show refs/heads/MutationCollector-nonexistent:path | wc -l',1),('python-exit7','python3 corpus/instruments/fail.py | wc -l',1),('cat-middle','cat present.txt | cat missing.txt | wc -l',1),('grep-middle',"cat present.txt | grep '[' | wc -l",1),('python-error-and-group','python3 corpus/instruments/fail.py | wc -l && wc -l < empty.txt',1),('grep-no-match',"grep absent present.txt | wc -l",0),('final-error',"cat present.txt | grep '['",1)]
(root/'empty.txt').write_text('')
for name,derive,want_exit in cases:
    ledger=root/(name+'.json')
    want='0\n0' if name=='python-error-and-group' else '0'
    ledger.write_text(json.dumps({'figures':[{'id':name,'record':'claim.md:1','recorded':want,'derive':derive,'want':want}]}))
    cmd=[sys.executable,str(audit),'--ledger',str(ledger),'--root',str(root)]
    print('CASE '+name+' expected_exit='+str(want_exit)+' argv='+json.dumps(cmd)+' derive='+json.dumps(derive),flush=True)
    p=subprocess.run(cmd,cwd=S,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    sys.stdout.buffer.write(p.stdout);sys.stdout.buffer.flush()
    print('OBSERVED exit='+str(p.returncode)+' matches_expected='+str(p.returncode==want_exit),flush=True)
print('audit_after_sha256='+sha(audit.read_bytes())+' prose_after_sha256='+sha(prose.read_bytes()),flush=True)
