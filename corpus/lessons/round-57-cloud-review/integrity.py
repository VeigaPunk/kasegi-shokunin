import pathlib,subprocess,json,hashlib,datetime,importlib.util
root=pathlib.Path(__file__).parent;repo='shokunin-training/lanes/kasegi';base='eae1d614542e8d30d77e9f4e8b9dea6a11aad138';freeze='2b08aaef5bed38f84227328ea64daad4451d8b07';ref='9b1028c00656d2693f4accc513e14c4c180a2f27'
def git(*args):return subprocess.check_output(['git','-C',repo,*args])
print('run_utc='+datetime.datetime.now(datetime.timezone.utc).isoformat())
for a,b in [(base,freeze),(freeze,ref)]:print('ancestry',a,b,subprocess.run(['git','-C',repo,'merge-base','--is-ancestor',a,b]).returncode)
for f in ['.ufo/waves/round-57/claims.json','.ufo/waves/round-57/fixtures.json','corpus/instruments/osv-semantic-check.py','.ufo/waves/round-57/freeze-record.json']:print('freeze-bytes-preserved',f,git('show',freeze+':'+f)==git('show',ref+':'+f))
fr=json.loads(git('show',freeze+':.ufo/waves/round-57/freeze-record.json'));cl=git('show',freeze+':.ufo/waves/round-57/claims.json');print('freeze-claims-digest',hashlib.sha256(cl).hexdigest()==fr['claims-sha256']);print('freeze-harness-digest',hashlib.sha256(git('show',freeze+':corpus/instruments/osv-semantic-check.py')).hexdigest()==fr['harness-sha256'])
print('freeze-clock',fr['frozen-at'],git('show','-s','--format=%cI',freeze).decode().strip())
changed=git('diff','--name-only',base,ref).decode().splitlines()
for f in changed:
 try:old=git('show',base+':'+f)
 except subprocess.CalledProcessError:continue
 new=git('show',ref+':'+f)
 if f=='corpus/SOURCES.md':
  it=iter(new.splitlines());valid=all(any(x==y for y in it) for x in old.splitlines());print('old-source-lines-retained',valid)
 else:print('prefix-preserved',f,new.startswith(old))
for f in ['density.py','source-recheck.py','capture-binding-check.py','figure-audit.py','frontier-recheck-count.py']:
 p='corpus/instruments/'+f;print('retained-engine-identical',f,git('show',base+':'+p)==git('show',ref+':'+p))
spec=importlib.util.spec_from_file_location('density',root/'export/corpus/instruments/density.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
old=mod.split_blocks(git('show',base+':SKILL.md').decode().splitlines(True));new=mod.split_blocks(git('show',ref+':SKILL.md').decode().splitlines(True));print('density-oldblocks-identical',old==new[:len(old)])
for label,blocks in [('base',old),('candidate',new)]:print('density',label,'blocks',len(blocks),'mean',round(sum(mod.census_block(x[1])['dens'] for x in blocks)/len(blocks),1))
print('density-new-block',mod.census_block(new[-1][1])['dens'])
