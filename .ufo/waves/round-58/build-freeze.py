import copy,json,pathlib
p=pathlib.Path('.ufo/waves/round-58')
b={'schema':'kernel-report-training/v1','synthetic':True,'version':{'origin':'kernel.org','id':'6.12.1','recent_check':True},'description':'TRAINING ONLY: guest can read invented record despite owner-only policy.','conditions':{'config':'ordinary'},'reproducer':{'format':'source','trigger':'read-training-record','confirm':'access-granted','trace_id':'t1'},'traces':[{'id':'t1','version':'6.12.1','conditions':{'config':'ordinary'},'trigger':'read-training-record','observation':'access-granted','reproduced':True,'operation':'read-training-record','permitted':True,'production':True,'specimen':{'actor':'guest','owner':'owner','mode':'buggy'}}],'boundary_claim':{'operation':'read-training-record','permitted':False},'ai_assisted':True,'public_text':[{'kind':'summary','text':'Synthetic report only.'},{'kind':'availability','text':'Reproducer available on maintainer request.'}]}
cases=[]
def add(name, edits=(), evidence='corroborated-synthetic',boundary='supported-synthetic',disclosure='public-status-only',rc=0):
 d=copy.deepcopy(b)
 for path,value in edits:
  x=d
  for k in path[:-1]: x=x[k]
  if value=='__DELETE__': del x[path[-1]]
  else:x[path[-1]]=value
 cases.append({'id':name,'input':d,'expected':{'evidence':evidence,'boundary':boundary,'disclosure':disclosure},'exit':rc})
add('positive-ai')
for name,path,value in [('latest-mainline',['version','id'],'latest mainline'),('distro',['version','origin'],'distro'),('stale-check',['version','recent_check'],False),('empty-description',['description'],''),('binary-only',['reproducer','format'],'binary'),('no-trigger',['reproducer','trigger'],''),('no-confirm',['reproducer','confirm'],''),('missing-trace',['reproducer','trace_id'],'absent'),('wrong-version',['traces',0,'version'],'6.12.2'),('wrong-condition',['traces',0,'conditions'],{}),('wrong-trigger',['traces',0,'trigger'],'other'),('irrelevant-observation',['traces',0,'observation'],'crash'),('not-reproduced',['traces',0,'reproduced'],False),('forged-permission',['traces',0,'permitted'],False),('unknown-model',['traces',0,'specimen','mode'],'unknown'),('missing-specimen',['traces',0,'specimen'],'__DELETE__'),('fixed-trace-as-buggy',['traces',0,'specimen','mode'],'fixed')]:
 add(name,[(path,value)],'needs-evidence','unestablished')
add('fixed-valid-no-boundary',[(('traces',0,'specimen','mode'),'fixed'),(('traces',0,'observation'),'access-denied'),(('traces',0,'permitted'),False),(('reproducer','confirm'),'access-denied')],boundary='not-supported')
add('owner-legitimate',[(('traces',0,'specimen','actor'),'owner'),(('boundary_claim','permitted'),True)],boundary='not-supported')
add('owner-false-claim',[(('traces',0,'specimen','actor'),'owner')],boundary='unestablished')
add('wrong-boundary-operation',[(('boundary_claim','operation'),'write-record')],boundary='unestablished')
add('nonproduction',[(('traces',0,'production'),False)],boundary='not-supported')
add('public-leak',[(('public_text',),[{'kind':'reproducer','text':'INERT toy reproducer'}])],disclosure='withhold-reproducer')
add('missing-availability',[(('public_text',),[])],disclosure='needs-availability-statement')
add('non-ai',[(('ai_assisted',),False)],disclosure='not-assessed')
add('incomplete-and-public-leak',[(('traces',),[]),(('public_text',),[{'kind':'reproducer','text':'INERT'}])],evidence='needs-evidence',boundary='unestablished',disclosure='withhold-reproducer')
add('commit-id',[(('version','id'),'a'*40),(('traces',0,'version'),'a'*40)])
add('release-candidate',[(('version','id'),'6.13-rc2'),(('traces',0,'version'),'6.13-rc2')])
for name,edits in [('wrong-bool',[(('ai_assisted',),'true')]),('duplicate-id',[(('traces',),b['traces']*2)]),('wrong-conditions-type',[(('conditions',),[])]),('unknown-block-kind',[(('public_text',),[{'kind':'code','text':'x'}])]),('invalid-specimen-type',[(('traces',0,'specimen'),[])])]:
 add(name,edits,'invalid','unestablished','not-assessed',2)
add('not-synthetic',[(('synthetic',),False)],'invalid','unestablished','not-assessed',2)
(p/'fixtures.json').write_text(json.dumps(cases,indent=2)+'\n')
(p/'example.json').write_text(json.dumps(b,indent=2)+'\n')
print('frozen-candidate cases='+str(len(cases)))
