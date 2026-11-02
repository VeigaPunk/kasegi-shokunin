import json,pathlib,hashlib,datetime,subprocess
p=pathlib.Path(__file__).parent;l=p.parent.parent/'lanes/kasegi';a=l/'.ufo/waves/round-60/first-answers.json'
o=json.loads((p/'private-oracle.json').read_text());ans=json.loads(a.read_text());cs=json.loads((p/'challenge.json').read_text());notes=[
'Active, open, all-stage automation are explicit; one death with higher consequences excluded plus temporarily continuing MEFs supports high HI. Immediate is row70, not severity-derived.',
'Local isolated exposure and bounded minor safety/nonessential disruption justify small/low despite same CVSS9.8 and same flaw as01. Explicit automation evidence is retained rather than contradicted by exposure intuition.',
'Well-known exploitation method independently meets PoC alternative even without program. Necessary nonautomatable delivery is explicit, not inferred from chosen practice. Marginal safety and MEF failure correctly produce medium.',
'Whole mission fails and recovery impaired, so HI very high even with minor safety. None follows an explicit negative review. Scheduled is correctly bounded to row3 with unreconciled prose conflict disclosed.',
'Effective timely restriction supports controlled. Automation remains unknown, while both compatible paths58/62 agree on out-of-cycle. No fictitious value was filled in.',
'Omitted exploitation section stays unknown; independent automation does not imply public PoC or wild activity. Complete rows20/44/68 disagree, supporting abstention.',
'Chosen manual stages do not establish necessary manual stages. A single automated final step does not establish all-four capability. Known PoC/open/high are retained; rows42/46 disagree.',
'Explicit actual supplier request and requested_model defeat generic deployer boilerplate. No supplier result is obtained from deployer labels; empty paths and mismatch are correct.',
'Unknown mission/safety are not inferred low from severity or silence. Official default assumptions are acknowledged but not mistaken for observed facts under the frozen evidence-only scope.',
'Firewall ownership/installation is not affected-instance access or effective interruption evidence. All three exposure values remain compatible and produce different outcomes. This directly exercises the prior shared-assumption lesson.',
'Multiple deaths establishes catastrophic safety, whose OR limb fixes very-high HI despite missing mission evidence. Unknown mission is retained and no mission-failure inference invented.'
]
results=[]
for c,e,x,n in zip(cs,o['cases'],ans,notes):
 vals=[x['inputs'][k]['value'] for k in ['exploitation','exposure','automatable','human_impact']]
 assert c['id']==e['id']==x['id'];assert e['priority']==x['priority'] and e['path_rows']==x['path_rows']
 if x['priority']!='model_mismatch':assert vals==e['inputs']
 for v in x['inputs'].values():assert all(t in c['scenario'] for t in v['evidence'])
 assert x['model_id']==o['model'] and x['model_binding']['inputs']==o['input_versions']
 results.append({'id':x['id'],'verdict':'pass','causal_review':n})
receipt={'reviewed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'/root/judge_kasegi_round60','author_commit':'a45efc84655fe8c64d803788e77868c954b6cbb0','answer_sha256':hashlib.sha256(a.read_bytes()).hexdigest(),'cases':results,'verdict':'All 11 first cases pass semantic/source/model/path review. C1 performance condition met; final admission still depends on conformance and no-harm closure.','limits':'Human judgment recorded here; Python verifies identity/excerpts/row parity only, never correctness of natural-language reasoning. 40 assessed input fields plus four withheld model-mismatch fields; not 44 independently assessed facts. No general accuracy estimate.'}
(p/'first-review.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['verdict'])
