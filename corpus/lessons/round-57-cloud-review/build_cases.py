import json, pathlib, hashlib, datetime
out=pathlib.Path(__file__).parent
P={'ecosystem':'npm','name':'review-kit'}
def rng(*events,typ='SEMVER',**kw): return dict(type=typ,events=list(events),**kw)
def ent(ranges=None,versions=None,package=None):
 d={'package':package or P.copy()}
 if ranges is not None:d['ranges']=ranges
 if versions is not None:d['versions']=versions
 return d
cases=[]
def add(id,v,expected,affected,reason,pkg=None):
 cases.append(dict(id=id,package=pkg or P.copy(),version=v,expected=expected,reason=reason,osv={'schema_version':'1.7.0','id':'OSV-2026-REVIEW','modified':'2026-11-02T00:00:00Z','affected':affected}))
R=lambda *e:rng(*e)
base=R({'introduced':'2.3.4'},{'fixed':'3.0.0'})
for id,v,e in [('introduced-inclusive','2.3.4','affected'),('below-introduced','2.3.3','not_affected'),('fixed-exclusive','3.0.0','not_affected'),('inside-range','2.9.9','affected')]:add(id,v,e,[ent([base])],'Evaluation endpoint predicates')
for v,e in [('7.1.4','affected'),('7.1.5','not_affected')]:add('last-'+v,v,e,[ent([R({'introduced':'0'},{'last_affected':'7.1.4'})])],'last_affected inclusive')
add('numeric-not-lexical','2.10.0','affected',[ent([R({'introduced':'2.9.0'},{'fixed':'2.11.0'})])],'Numeric SemVer ordering')
add('zero-sentinel','0.0.0','affected',[ent([R({'introduced':'0'})])],'introduced zero sorts before all versions')
add('star-limit','90.0.0','affected',[ent([R({'introduced':'0'},{'limit':'*'})])],'unbounded limit')
add('limit-exclusive','4.0.0','not_affected',[ent([R({'introduced':'0'},{'limit':'4.0.0'})])],'strict BeforeLimits')
add('multiple-limit-or','5.0.0','affected',[ent([R({'introduced':'0'},{'limit':'4.0.0'},{'limit':'6.0.0'})])],'BeforeLimits existential, not minimum limit')
add('star-dominates-limit','8.0.0','affected',[ent([R({'introduced':'0'},{'limit':'4.0.0'},{'limit':'*'})])],'BeforeLimits existential')
add('sort-events','4.0.0','affected',[ent([R({'fixed':'5.0.0'},{'introduced':'3.0.0'})])],'sort required, storage order optional')
for v,e in [('2.0.0','not_affected'),('3.0.0','affected'),('4.0.0','not_affected')]:add('reintroduced-'+v,v,e,[ent([R({'fixed':'4.0.0'},{'introduced':'1.0.0'},{'introduced':'3.0.0'},{'fixed':'2.0.0'})])],'sorted disjoint intervals')
add('multiple-range-or','9.0.0','affected',[ent([base,R({'introduced':'9.0.0'})])],'ranges OR')
add('multi-affected-or','9.0.0','affected',[ent([base]),ent(None,['9.0.0'])],'affected entries OR')
add('versions-override-fixed','3.0.0','affected',[ent([base],['3.0.0'])],'exact membership OR range')
add('exact-only-opaque','release-red','affected',[ent(None,['release-red'])],'explicit string equality does not need SemVer')
add('exact-only-absence','release-blue','not_affected',[ent(None,['release-red'])],'explicit-only nonmembership')
for typ in ['ECOSYSTEM','GIT']:
 r=rng({'introduced':'0'},typ=typ,**({'repo':'https://example.org/repo.git'} if typ=='GIT' else {}))
 for yes in [True,False]: add(typ+'-explicit-'+str(yes),'2.3.4','affected' if yes else 'could_not_evaluate',[ent([r],['2.3.4'] if yes else ['0.1.0'])],'unsupported range not false; exact matching membership proves true')
add('unsupported-plus-supported-true','2.3.4','affected',[ent([rng({'introduced':'0'},typ='ECOSYSTEM'),base],['0.1.0'])],'known true OR unknown true')
add('unsupported-plus-supported-false','5.0.0','could_not_evaluate',[ent([rng({'introduced':'0'},typ='ECOSYSTEM'),base],['0.1.0'])],'known false OR unknown unknown')
for version in ['2.3.4-alpha','2.3.4+build.9']:
 add('query-unsupported-'+version,version,'could_not_evaluate',[ent([base])],'bounded evaluator excludes query prerelease/build')
 add('query-explicit-'+version,version,'affected',[ent([base],[version])],'exact membership proves true')
add('boundary-prerelease','2.3.4','could_not_evaluate',[ent([R({'introduced':'2.3.4-alpha'},{'fixed':'3.0.0'})])],'bounded evaluator excludes boundary prerelease')
add('boundary-build','2.3.4','could_not_evaluate',[ent([R({'introduced':'2.3.4+build.1'},{'fixed':'3.0.0'})])],'bounded evaluator excludes boundary build')
add('wrong-package-name','2.3.4','not_affected',[ent([base],['2.3.4'],{'ecosystem':'npm','name':'other-kit'})],'package identity filters')
add('wrong-ecosystem','2.3.4','not_affected',[ent([base],['2.3.4'],{'ecosystem':'PyPI','name':'review-kit'})],'ecosystem identity filters')
add('wrong-package-unsupported','2.3.4','not_affected',[ent([rng({'introduced':'0'},typ='ECOSYSTEM')],['1.0.0'],{'ecosystem':'npm','name':'other-kit'})],'irrelevant unknown does not contaminate target')
for id,r in [('missing-introduced',R({'fixed':'3.0.0'})),('multi-event-key',R({'introduced':'1.0.0','fixed':'3.0.0'})),('mixed-last-fixed',R({'introduced':'0'},{'fixed':'2.0.0'},{'last_affected':'3.0.0'})),('empty-events',R()),('event-not-string',R({'introduced':0})),('unknown-event',R({'introduced':'0'},{'banana':'4.0.0'})),('unknown-range-type',rng({'introduced':'0'},typ='MAGIC'))]:add(id,'2.3.4','invalid',[ent([r])],'OSV Requirements or shape invalid, not unsupported semantics')
add('invalid-versions-scalar','2.3.4','invalid',[ent(None,'2.3.4')],'versions must array')
add('invalid-versions-member','2.3.4','invalid',[ent(None,[2])],'versions members strings')
add('invalid-ranges-object','2.3.4','invalid',[ent(base)],'ranges must array')
add('invalid-affected-member','2.3.4','invalid',[None],'affected member object')
blob=(json.dumps(cases,indent=2,sort_keys=True)+'\n').encode();(out/'cases.json').write_bytes(blob)
manifest={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':len(cases),'sha256':hashlib.sha256(blob).hexdigest(),'source':'https://ossf.github.io/osv-schema/','source_sections':['Evaluation','affected[].ranges[].events Requirements','Special values'],'independence':'No author candidate or expected fixtures inspected before this freeze. Abstract verdict labels to be mapped to documented CLI after parent supplies candidate hash.'}
(out/'FREEZE.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest))
