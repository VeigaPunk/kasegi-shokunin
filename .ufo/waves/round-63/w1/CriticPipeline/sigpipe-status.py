import pathlib,subprocess,shutil,sys
S=pathlib.Path('/fast/scratch/hyaku/kasegi-r63/CriticPipeline')
if S.exists(): raise SystemExit('refusing existing scratch')
S.mkdir(parents=True)
try:
 argv=[sys.executable,'-c','import os,signal; signal.signal(signal.SIGPIPE,signal.SIG_DFL)\nwhile True: os.write(1,b"x\\n"*65536)']
 p=subprocess.Popen(argv,cwd=S,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 q=subprocess.Popen(['head','-n','1'],cwd=S,stdin=p.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 p.stdout.close()
 out,err=q.communicate(timeout=10);perr=p.communicate(timeout=10)[1]
 print('producer_argv='+repr(argv));print('consumer_argv='+repr(['head','-n','1']))
 print('producer_exit='+str(p.returncode));print('consumer_exit='+str(q.returncode))
 sys.stdout.flush();sys.stdout.buffer.write(out);sys.stdout.buffer.flush()
 sys.stderr.buffer.write(err+perr)
finally:
 shutil.rmtree(S)
