from pathlib import Path
import json,hashlib
root=Path('corpus/source-snapshots/round-60')
urls={'S094':'https://certcc.github.io/SSVC/howto/deployer_tree/','S095':'https://certcc.github.io/SSVC/reference/decision_points/mission_impact/','S096':'https://certcc.github.io/SSVC/reference/decision_points/safety_impact/'}
qs={'S094':[(514,'ssvc:DT_DP:1.0.0'),(216,'priority of deploying a patch')],'S095':[(201,'ssvc:MI:2.0.0'),(211,'essential functions continue for a time')],'S096':[(205,'ssvc:SI:2.0.1'),(221,'Multiple loss of life')]}
times={'S094':'21:45:58','S095':'21:46:33','S096':'21:46:36'}
sources=[]
for s in urls:
 sources.append({'id':s,'url':urls[s],'capture_url':urls[s],'fetched_utc':f'2026-11-02T{times[s]}Z','http':{'status':200},'kind':'html','path':s+'.txt','sha256':hashlib.sha256((root/(s+'.txt')).read_bytes()).hexdigest(),'quotes':[{'id':f'Q{i+1}','anchor':a,'quote':q} for i,(a,q) in enumerate(qs[s])]})
(root/'manifest.json').write_text(json.dumps({'schema_version':1,'sources':sources},indent=2)+'\n')
p=Path('corpus/SOURCES.md'); t=p.read_text(); line=next(x for x in t.splitlines() if x.startswith('| S093 |'))
rows='''
| S094 | CERT/CC Deployer Decision Model — https://certcc.github.io/SSVC/howto/deployer_tree/ | docs | A | Pinned example deployer prioritization table and input interpretation | DT_DP1.0.0 Table of Values; capture 2026-11-02 S094.txt:514,880 onward | Deepens F20 from overview to exact stakeholder-specific paths; table/prose discrepancy explicitly retained | mined | 2026-11-02 | on-release | corpus/knowledge/ssvc-deployer-assessment.md |
| S095 | CERT/CC Mission Impact — https://certcc.github.io/SSVC/reference/decision_points/mission_impact/ | docs | A | MI2.0.0 categories feeding Human Impact, not observed target facts | MI2.0.0 heading and definitions; capture 2026-11-02 S095.txt:201,211 | Distinguish crippled supporting functions from essential-function and whole-mission failure | mined | 2026-11-02 | on-release | corpus/knowledge/ssvc-deployer-assessment.md |
| S096 | CERT/CC Safety Impact — https://certcc.github.io/SSVC/reference/decision_points/safety_impact/ | docs | A | SI2.0.1 definitions feeding Human Impact | SI2.0.1 heading and catastrophic definition; capture 2026-11-02 S096.txt:205,221 | Safety covers multiple forms of harm; distinguish supported critical/catastrophic effects from omissions | mined | 2026-11-02 | on-release | corpus/knowledge/ssvc-deployer-assessment.md |
| S097 | CERT/CC Deployer Decision Model, rejected universal use — https://certcc.github.io/SSVC/howto/deployer_tree/ | docs | A | Deployer patch priority only, not supplier/CISA decisions or universal risk | DT_DP1.0.0; S094 capture 2026-11-02 line216 | REJECTED: table identity is deployer patch priority, not a universal or CISA model; flip: separately pinned appropriate stakeholder model and facts | rejected | 2026-11-02 | on-release | — |'''
p.write_text(t.replace(line,line+rows,1))
