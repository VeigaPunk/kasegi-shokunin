import hashlib,json,pathlib,shlex,shutil,subprocess,sys
L=pathlib.Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin')
W=L/'.ufo/waves/round-63/w1/CriticPipeline'
S=pathlib.Path('/fast/scratch/hyaku/kasegi-r63/CriticPipeline')
BASE='fdccc6da803965234c1eff5a0fee38b97e6621c1'
probes=[
 ('cat-missing','cat missing.txt | wc -l','0',1),
 ('grep-invalid',"grep '[' good.txt | wc -l",'0',1),
 ('git-missing-ref','git show critic-r63-nonexistent-ref | wc -l','0',1),
 ('python-exit7','python3 corpus/instruments/fail.py | wc -l','0',1),
 ('midstage-exit7','cat good.txt | python3 corpus/instruments/fail.py | wc -l','0',1),
 ('error-before-and','python3 corpus/instruments/fail.py | wc -l && cat tail.txt','0\nTAIL',1),
 ('cat-before-and','cat missing.txt | wc -l && cat tail.txt','0\nTAIL',1),
 ('grep-no-match',"grep absent good.txt | wc -l",'0',0),
 ('grep-no-match-and',"grep absent good.txt | wc -l && cat tail.txt",'0\nTAIL',0),
 ('final-exit7','cat good.txt | python3 corpus/instruments/fail.py','0',1),
 ('final-exit1','grep absent good.txt','0',1),
 ('sigpipe','python3 corpus/instruments/sigpipe.py | head -n 1','x',0),
]
if S.exists(): raise SystemExit('scratch already exists; refusing overwrite')
S.mkdir(parents=True)
try:
 code=subprocess.check_output(['git','-C',str(L),'show',BASE+':corpus/instruments/figure-audit.py'])
 instrument=S/'figure-audit.py';instrument.write_bytes(code)
 (W/'baseline-figure-audit.py').write_bytes(code)
 root=S/'root';(root/'corpus/instruments').mkdir(parents=True)
 (root/'.git').write_text('gitdir: '+str(L/'.git')+'\n')
 (root/'good.txt').write_text('one\n');(root/'tail.txt').write_text('TAIL\n')
 (root/'corpus/instruments/fail.py').write_text('raise SystemExit(7)\n')
 (root/'corpus/instruments/sigpipe.py').write_text('import os,signal\nsignal.signal(signal.SIGPIPE,signal.SIG_DFL)\nwhile True: os.write(1,b"x\\n"*65536)\n')
 print('axis=depth:verifiability nominal score4 held')
 print('base='+BASE+' sha256='+hashlib.sha256(code).hexdigest())
 results=[]
 for name,derive,want,desired in probes:
  ledger=root/'ledger.json';ledger.write_text(json.dumps({'figures':[{'id':name,'record':'scratch-probe','recorded':want,'derive':derive,'want':want}]}))
  argv=[sys.executable,str(instrument),'--root',str(root),'--ledger',str(ledger)]
  r=subprocess.run(argv,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
  (W/(name+'.stdout')).write_bytes(r.stdout);(W/(name+'.stderr')).write_bytes(r.stderr)
  row={'probe':name,'derive':derive,'want':want,'desired_bounded_exit':desired,'observed_exit':r.returncode,'argv':argv,'cwd':str(root),'stdout':r.stdout.decode(),'stderr':r.stderr.decode()}
  results.append(row);print(json.dumps(row,sort_keys=True))
 # Direct argv statuses isolate exit1 from exit>1 and preserve unedited bytes.
 for name,argv in [('cat-status',['cat','missing.txt']),('grep-invalid-status',['grep','[','good.txt']),('git-ref-status',['git','show','critic-r63-nonexistent-ref']),('python-status',[sys.executable,'corpus/instruments/fail.py'])]:
  r=subprocess.run(argv,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
  (W/(name+'.stdout')).write_bytes(r.stdout);(W/(name+'.stderr')).write_bytes(r.stderr)
  print(json.dumps({'direct':name,'argv':argv,'cwd':str(root),'exit':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode()},sort_keys=True))
 (W/'results.json').write_text(json.dumps(results,indent=2)+'\n')
finally:
 shutil.rmtree(S)
 print('scratch_removed='+str(not S.exists()))
