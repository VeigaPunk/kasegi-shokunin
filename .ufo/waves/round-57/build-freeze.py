# Author expected fixtures, before implementation. Not an evaluator. Exit 0 success.
import json, pathlib, hashlib, datetime, subprocess
P=pathlib.Path('.ufo/waves/round-57'); P.mkdir(exist_ok=True)
pkg={'ecosystem':'npm','name':'training-only'}
def r(events,typ='SEMVER',**kw): return dict(type=typ,events=events,**kw)
def a(ranges=None,versions=None,package=None):
 d={'package':package or pkg}
 if ranges is not None:d['ranges']=ranges
 if versions is not None:d['versions']=versions
 return d
cases=[]
def c(id,version,entries,status,reason):
 cases.append(dict(id=id,request={'package':pkg,'version':version,'osv':{'affected':entries}},expected={'status':status,'reason':reason},exit={'affected':0,'unaffected':0,'unsupported':2,'invalid':3}[status]))
I={'introduced':'1.0.0'}; F={'fixed':'2.0.0'}; L={'last_affected':'2.0.0'}
base=[a([r([I,F])])]
for id,v,st in [('below','0.9.9','unaffected'),('introduced','1.0.0','affected'),('inside','1.9.9','affected'),('fixed','2.0.0','unaffected'),('above','2.0.1','unaffected')]:c(id,v,base,st,'range-match' if st=='affected' else 'no-match')
for id,v,st in [('last-at','2.0.0','affected'),('last-above','2.0.1','unaffected')]:c(id,v,[a([r([I,L])])],st,'range-match' if st=='affected' else 'no-match')
c('explicit-only','release-foo',[a(versions=['release-foo'])],'affected','explicit-match')
c('explicit-miss','release-bar',[a(versions=['release-foo'])],'unaffected','no-match')
c('explicit-overrides-fixed','2.0.0',[a([r([I,F])],['2.0.0'])],'affected','explicit-match')
c('range-or-versions','1.5.0',[a([r([I,F])],['9.0.0'])],'affected','range-match')
c('separate-arrays','3.0.0',[a([r([I,F]),r([{'introduced':'3.0.0'},{'last_affected':'4.0.0'}])])],'affected','range-match')
c('separate-packages','1.5.0',[a([r([I,F])]),a([r([I,L])],package={'ecosystem':'npm','name':'other'})],'affected','range-match')
c('mixed-same-array','1.5.0',[a([r([I,F,L])])],'invalid','mixed-closures')
c('wrong-package','1.5.0',[a([r([I,F])],['1.5.0'],{'ecosystem':'npm','name':'other'})],'unaffected','no-match')
c('wrong-ecosystem','1.5.0',[a([r([I,F])],['1.5.0'],{'ecosystem':'PyPI','name':'training-only'})],'unaffected','no-match')
c('empty-record','1.5.0',[],'unaffected','no-match')
c('open-zero','0.0.0',[a([r([{'introduced':'0'}])])],'affected','range-match')
c('unsorted','1.5.0',[a([r([F,I])])],'affected','range-match')
reopen=[a([r([{'introduced':'3.0.0'},F,{'fixed':'4.0.0'},I])])]
c('reintroduced','3.2.0',reopen,'affected','range-match')
c('gap','2.5.0',reopen,'unaffected','no-match')
c('numeric-not-lexical','1.10.0',[a([r([{'introduced':'1.9.0'},{'fixed':'1.11.0'}])])],'affected','range-match')
for id,v,st in [('limit-below','1.5.0','affected'),('limit-at','2.0.0','unaffected')]:c(id,v,[a([r([I,{'limit':'2.0.0'}])])],st,'range-match' if st=='affected' else 'no-match')
c('multiple-limits-or','2.5.0',[a([r([I,{'limit':'2.0.0'},{'limit':'3.0.0'}])])],'affected','range-match')
c('star-limit','200.0.0',[a([r([I,{'limit':'*'}])])],'affected','range-match')
for typ in ['ECOSYSTEM','GIT']:
 rr=r([I,F],typ,**({'repo':'https://example.invalid/training.git'} if typ=='GIT' else {}))
 c(typ.lower()+'-unsupported','1.5.0',[a([rr],['1.0.0'])],'unsupported','range-type')
 c(typ.lower()+'-explicit','1.5.0',[a([rr],['1.5.0'])],'affected','explicit-match')
c('unsupported-plus-positive','1.5.0',[a([r([I,F],'ECOSYSTEM'),r([I,F])])],'affected','range-match')
c('unsupported-plus-negative','2.5.0',[a([r([I,F],'ECOSYSTEM'),r([I,F])])],'unsupported','range-type')
for id,v in [('prerelease-query','1.5.0-alpha'),('build-query','1.5.0+meta'),('leading-zero-query','01.5.0')]:c(id,v,base,'unsupported','version-domain')
c('prerelease-event','1.5.0',[a([r([{'introduced':'1.0.0-alpha'},F])])],'unsupported','version-domain')
c('missing-introduced','1.5.0',[a([r([F])])],'invalid','missing-introduced')
c('two-verbs','1.5.0',[a([r([{'introduced':'1.0.0','fixed':'2.0.0'}])])],'invalid','event-shape')
c('unknown-verb','1.5.0',[a([r([I,{'patched':'2.0.0'}])])],'invalid','event-shape')
c('git-no-repo','1.5.0',[a([r([I,F],'GIT')])],'invalid','missing-repo')
raw=(json.dumps(cases,indent=2)+'\n').encode();(P/'fixtures.json').write_bytes(raw)
claims={'round':57,'base':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'claims':[{'id':'C1','axis':'depth:verifiability','type':'bounded domain capability; nominal legacy metric','score_before':4,'score_after':4,'claim':'Discriminate OSV explicit versions OR range membership and per-events-array fixed/last_affected exclusion on frozen synthetic cases. Correct all owned prose mentions append-only. No general ecosystem or Git comparator.','before':'No executable OSV evaluator; committed README F31 excludes versions and knowledge Claim 3 wrongly scopes exclusion record-wide. Reconstructed mistaken reading is a negative model, not a historical executable.','after':'Every frozen expected status/reason/exit passes; each declared semantic mutant fails at least one targeted case; original source opens and census clean; no prior corpus bytes rewritten.','kill_rule':'Any frozen case mismatch, missing before demonstration, surviving declared mutant, omitted correction, unsupported range classified as unaffected, or harm to existing gate attributable to this change prevents verification.'}],'domain':'package identity is exact ecosystem/name pair; input is affectedness fragment, not whole-record JSON Schema validator; explicit versions compare exact nonempty strings; SEMVER ranges support only canonical unsigned x.y.z release triples, introduced 0 and limit *; prerelease/build/other types unsupported unless another OR limb proves affected. Structural invalidity in matching entries is checked before evaluation; unknown nonmatching packages ignored. Ties with different event kinds at identical release are unsupported rather than invented ordering.','fixtures_sha256':hashlib.sha256(raw).hexdigest(),'expected_cases':len(cases),'mutants':['always-affected','always-unaffected','range-only','boundary-swap','recordwide-exclusion','wrong-package','ecosystem-as-semver','git-as-semver','lexical-sort','limits-and','unsorted-events'],'measurement':'python3 corpus/instruments/osv-semantic-check.py --engine corpus/instruments/osv-affectedness.py','admission':'pending independent non-author review'}
(P/'claims.json').write_text(json.dumps(claims,indent=2)+'\n')
print('fixture-count='+str(len(cases)))
