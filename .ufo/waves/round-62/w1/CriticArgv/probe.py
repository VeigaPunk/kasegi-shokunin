import concurrent.futures, hashlib, json, os, pathlib, subprocess, sys
S=pathlib.Path('/fast/scratch/hyaku/kasegi-r62/CriticArgv')
W=pathlib.Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-62/w1/CriticArgv')
instruments={'base':S/'corpus/instruments/figure-audit.py','candidate':W.parent/'ExecArgv/figure-audit.py'}
cases={
'inside':'python3 corpus/instruments/ok.py',
'whole-quoted-inside':'python3 "corpus/instruments/ok.py"',
'quoted-space-inside':'python3 corpus/instruments/"ok space.py"',
'normalized-inside':'python3 corpus/instruments/../instruments/ok.py',
'prefix-refusal':'python3 outside.py',
'absolute-refusal':'python3 {root}/outside.py',
'traversal-refusal':'python3 corpus/instruments/../../outside.py',
'boundary-refusal':'python3 corpus/instruments/../instruments-evil/outside.py',
'quoted-traversal':'python3 corpus/instruments/"../../outside.py"',
'single-quoted-traversal':"python3 corpus/instruments/'../../outside.py'",
'escaped-traversal':r'python3 corpus/instruments/\..\/\..\/outside.py',
'quoted-boundary':'python3 corpus/instruments/"../instruments-evil/outside.py"',
'symlink-refusal':'python3 corpus/instruments/link.py',
'quoted-symlink':'python3 corpus/instruments/"link.py"',
'variable-traversal':'python3 corpus/instruments/$ESC/outside.py',
'quoted-variable':'python3 corpus/instruments/"$ESC"/outside.py',
'brace-traversal':'python3 corpus/instruments/{../../outside.py,ok.py}',
'glob-symlink':'python3 corpus/instruments/link*.py',
'command-substitution':'cat $(cat data.txt)',
'python-option':'python3 -c "print(35)"',
'sort-quoted-write':"sort '--output=MARK' data.txt",
'sort-escaped-write':r'sort -\oMARK data.txt',
'sort-short-write':'sort -oMARK data.txt',
'sort-abbrev-residual':'sort --out=MARK data.txt',
'sort-cluster-residual':'sort -noMARK data.txt',
'pipe-control':'cat data.txt | wc -l',
'and-control':'cat data.txt && cat data.txt',
'pipe-escape':'cat data.txt | python3 corpus/instruments/"../../outside.py"',
'and-escape':'cat data.txt && python3 corpus/instruments/"../../outside.py"',
'pipe-denied':'cat data.txt | touch MARK',
'and-denied':'cat data.txt && touch MARK',
'quoted-operators':'python3 corpus/instruments/argv.py "a|b" "c&&d"',
'escaped-operators':r'python3 corpus/instruments/argv.py a\|b c\&\&d',
'input-control':'wc -l < data.txt',
'failed-pipeline-residual':'cat missing.txt | wc -l',
}
marker="from pathlib import Path\nPath('MARK').write_text('harmless\\n')\nprint(35)\n"
def probe(item):
 label,instr,name,text=item
 r=S/'fixtures'/(label+'-'+name); d=r/'corpus/instruments'; d.mkdir(parents=True)
 (r/'outside.py').write_text(marker); e=r/'corpus/instruments-evil';e.mkdir();(e/'outside.py').write_text(marker)
 (d/'ok.py').write_text('print(35)\n');(d/'ok space.py').write_text('print(35)\n')
 (d/'argv.py').write_text('import sys\nprint(repr(sys.argv[1:]))\n')
 (d/'link.py').symlink_to(r/'outside.py');(r/'data.txt').write_text('35\n')
 cmd=text.replace('{root}',str(r)); want='35'
 if name in ('pipe-control','input-control'):want='1'
 elif name=='and-control':want='35\n35'
 elif name=='and-escape':want='35\n35'
 elif name in ('quoted-operators','escaped-operators'):want="['a|b', 'c&&d']"
 elif name=='failed-pipeline-residual':want='0'
 ledger=r/'ledger.json'; ledger.write_text(json.dumps({'figures':[{'id':name,'record':'scratch','recorded':want,'derive':cmd,'want':want}]}))
 argv=[sys.executable,str(instr),'--ledger',str(ledger),'--root',str(r)]
 p=subprocess.run(argv,cwd=r,env=dict(os.environ,TMPDIR=str(S),PYTHONDONTWRITEBYTECODE='1',ESC='../..'),capture_output=True,text=True,timeout=15)
 return dict(revision=label,case=name,derive=cmd,argv=argv,exit=p.returncode,markers=int((r/'MARK').exists()),stdout=p.stdout.strip(),stderr=p.stderr.strip())
items=[(label,instr,name,text) for label,instr in instruments.items() for name,text in cases.items()]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(probe,items))
receipt={'digests':{k:hashlib.sha256(v.read_bytes()).hexdigest() for k,v in instruments.items()},'results':results}
(W/'receipts.json').write_text(json.dumps(receipt,indent=2)+'\n')
for name in cases:
 a,b=[x for x in results if x['case']==name]
 print(f"{name}: base={a['exit']}/{a['markers']} candidate={b['exit']}/{b['markers']}")
print('digests='+json.dumps(receipt['digests']))
