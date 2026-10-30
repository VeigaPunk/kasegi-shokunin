import pathlib, shutil, subprocess, json, os
S=pathlib.Path('/fast/scratch/hyaku/kasegi-r47/R47RevCounterC2')
L=pathlib.Path('/home/vgpnk/Projects/shokunin/kasegi-shokunin')
O=L/'.ufo/waves/round-47/w1/R47RevCounterC2.draft'
G=L/'corpus/instruments/r47-f30-gate.py'
E='corpus/knowledge/zdi-disclosure-policy.md'
try:
 S.mkdir(parents=True,exist_ok=True)
 os.environ['TMPDIR']=str(S)
 c=S/'control'; (c/'corpus').mkdir(parents=True)
 shutil.copytree(L/'corpus/knowledge',c/'corpus/knowledge')
 shutil.copytree(L/'corpus/source-snapshots/round-47',c/'corpus/source-snapshots/round-47')
 row='| F30 | ZDI broker disclosure timeline | admitted | `'+E+'` | S075 | Reopen policy before reliance. |'
 (c/'corpus/README.md').write_text((L/'corpus/README.md').read_text()+'\n'+row+'\n')
 src=(L/'corpus/SOURCES.md').read_text().split('## Paths')[0]
 src+='| S075 | ZDI disclosure policy — https://www.zerodayinitiative.com/advisories/disclosure_policy/ | docs | A | Broker acquisition disclosure timeline with deadlines and conditional exceptions | lines 20-27 of corpus/source-snapshots/round-47/S075.txt sha256 9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1 | Distinguish broker acquisition timelines from coordinator comparison and vendor intake | mined | 2026-10-30 | 90d | '+E+' |\n'
 (c/'corpus/SOURCES.md').write_text(src)
 entry='# ZDI disclosure policy\nsource: S075 — https://www.zerodayinitiative.com/advisories/disclosure_policy/ — capture\nverified-at: 2026-10-30\nrecheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-47/manifest.json --source S075\n\n'
 para='This policy describes a broker acquisition disclosure process rather than a universal rule for every coordinator or vendor. Retain the source conditions and avoid inventing a start event for the deadline. '
 entry+='## Scope and decision rule\n'+para+'See `S075.txt:24`.\n\n'
 entry+='| Rule label | Source words | Decision consequence |\n|---|---|---|\n'
 quotes=[('Deadline window','four months (120 days) to address the vulnerability',24),('Exploitation trigger','active exploitation is detected or imminent',25),('Rare extensions','granted only in rare circumstances',24),('Limited publication','publish a limited advisory including mitigation',24),('Unresponsive vendor','fifteen business days after the initial contact',23),('Regression window','vendors will be given a disclosure window of 60 days',25)]
 for label,q,n in quotes: entry+=f'| {label} | “{q}” (`S075.txt:{n}`) | Preserve source conditions |\n'
 entry+='\n## Overlap and novelty\n'+para+'Comparison remains at `corpus/knowledge/coordinated-disclosure-timelines.md:1`; vendor intake remains at `corpus/knowledge/vendor-third-party-finding-coordination.md:1`.\n\n'
 entry+='## Limits\n'+para+'The capture is the only evidence here (`S075.txt:24`). '+para*4+'\n\n'
 entry+='## Falsifiable package rule\n'+para+'Reject any package that claims a universal deadline from this broker policy (`S075.txt:24`).\n'
 (c/E).write_text(entry)
 outputs={}
 def run(name,tree):
  p=subprocess.run(['python3','-I',str(G),'--root',str(tree),'--work',str(S/name/'work')],capture_output=True,text=True,env=os.environ,timeout=40)
  text=f'COMMAND python3 -I {G} --root {tree} --work {S/name/"work"}\nEXIT {p.returncode}\n'+p.stdout+p.stderr
  print(name+'\n'+text,flush=True); (O/(name+'.txt')).write_text(text); outputs[name]={'exit':p.returncode,'stdout':p.stdout}
 run('do-nothing-control',c)
 for name in ['word-joiner-duplicate','hostile-recheck-comment']:
  t=S/name; shutil.copytree(c,t)
  if name=='word-joiner-duplicate':
   p=t/'corpus/README.md'; p.write_text(p.read_text()+'\n'+row.replace('F30','F\u206030')+'\n')
  else:
   p=t/E; p.write_text(p.read_text().replace('--source S075\n','--source S075 <!-- ; echo HOSTILE_TOKEN -->\n'))
  run(name,t)
 (O/'results.json').write_text(json.dumps(outputs,indent=2))
 (O/'control-entry.md').write_text(entry)
 (O/'mutations.txt').write_text('word-joiner-duplicate: append exact F30 row with id F\\u206030 (WORD JOINER); all other bytes control-identical.\nhostile-recheck-comment: append " <!-- ; echo HOSTILE_TOKEN -->" to canonical recheck line; all other bytes control-identical.\n')
finally:
 shutil.rmtree(S,ignore_errors=True)
