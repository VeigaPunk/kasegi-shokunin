from pathlib import Path
import json,hashlib
w=Path('.ufo/waves/round-59'); p=Path('corpus/source-snapshots/round-59/S092.txt')
quotes=[(478,'prior'),(502,'other than the attacker'),(548,'coherent function'),(527,'Only an increase in access'),(589,'direct, serious impact')]
s={'id':'S092','url':'https://www.first.org/cvss/v4.0/specification-document','capture_url':'https://www.first.org/cvss/v4.0/specification-document','fetched_utc':'2026-11-02T21:17:19Z','http':{'status':200},'kind':'html','path':'S092.txt','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'quotes':[{'id':'Q'+str(i+1),'anchor':n,'quote':q} for i,(n,q) in enumerate(quotes)]}
p.with_name('manifest.json').write_text(json.dumps({'schema_version':1,'sources':[s]},indent=2)+'\n')
def append(p,s):
 with Path(p).open('a') as f:f.write(s)
source=Path('corpus/SOURCES.md');text=source.read_text(); marker='| S091 |'; lines=text.splitlines(True); i=next(i for i,l in enumerate(lines) if l.startswith(marker));lines.insert(i+1,'| S092 | FIRST CVSS v4.0 specification — https://www.first.org/cvss/v4.0/specification-document | spec | A | PR/UI and subsequent-system impact evidence assessment, not scenario truth | Document v1.2 Base Metrics PR/UI, Impact Metrics, Tables 7/9/11; capture 2026-11-02 | Distinguish prerequisite authority, another human, system boundary and supported additional impact; deepens F01 | mined | 2026-11-02 | on-release | corpus/knowledge/cvss-v4-evidence-assessment.md |\n');source.write_text(''.join(lines))
append(source,'\nRound-59 bounded search (2026-11-02): opened one official specification, screened one, included its metric-definition scope (S092), rejected using that same source to establish fictional scenario truth or bounty entitlement. No secondary summaries needed; stop at operative PR/UI/impact clauses. No old status/recheck/used-by cells changed.\n')
Path('corpus/knowledge/cvss-v4-evidence-assessment.md').write_text('''# CVSS v4 evidence assessment, not vector transcription
source: S092 — https://www.first.org/cvss/v4.0/specification-document — document v1.2, PR/UI, Impact Metrics, Tables 7/9/11
verified-at: 2026-11-02
recheck: cd /workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-59/manifest.json --source S092

## Decision procedure
Treat a scenario as assumed training evidence, not proof of a real finding. Record
what the attacker could do before, what changes after, and whose actions enable it.
For PR, distinguish required prior authority from resulting privilege gain. Do not
translate every login into L: examine self-service and nonunique-default credentials.
For UI, distinguish attacker actions, ordinary victim participation, and deliberate
special actions or protection overrides. Explain why the action is necessary.

Draw the functional/policy boundary before assigning subsequent impact; an exclusive
support component may be part of the vulnerable system. Name additional loss in each
CIA dimension separately. N needs supported absence, not silence. H need not mean
all data: limited loss with direct serious consequence can qualify. If evidence cannot
discriminate values, answer insufficient and name the missing fact; this is not a CVSS
vector value. Do not abstain on established metrics because another metric is unknown.

## Located source support
All quotes together are 15 words: PR line478 “prior”; UI line502 “other than the attacker”;
boundary line548 “coherent function”; impact line527 “Only an increase in access”;
SC Table7 line589 “direct, serious impact”. The manifest pins exact capture bytes/anchors.

## Rejected inference and limits
An attacker ends with administrator control: PR:H does not follow. A second host or
company is named: subsequent impact does not follow. A complete-looking partial vector
does not establish full score, reward, authorization or actual exploitability. Source
recheck verifies captured wording, not current online freshness or analyst correctness.

Assessment workflow: `.ufo/waves/round-59/CONTRACT.md`. Independent scenarios and first
answers will remain in that wave's dossier; a human independent judge must evaluate
causal reasons, not merely compare enums. This documentation-only exercise deepens F01;
no target testing, scanner, automatic natural-language classifier or total CVSS calculator.
''')
append('SKILL.md','''
## Round-59 CVSS v4 evidence judgment

Trigger: explaining PR/UI and subsequent-system impact from scenario evidence.
Anti-trigger: computing a full score, target testing, claiming rewards or validating a
real vulnerability. S092 and `corpus/knowledge/cvss-v4-evidence-assessment.md` deepen F01.

| Question | Evidence discipline / error pattern |
|---|---|
| What authority existed before exploitation? | Do not substitute authority gained afterward; inspect self-service/default-credential qualifications |
| Must someone besides the attacker act? | Distinguish ordinary rendering from a specific conscious action or protection override |
| Is an affected component truly a subsequent system? | State coherent function/policy boundary and exclusive-support relationship; host count is not the rule |
| What additional CIA loss is supported? | Judge each dimension separately, including limited but directly serious loss; do not invent a chain |
| Facts omitted? | Name the missing fact; insufficient is workflow uncertainty, not a vector token or N |

Checklist: mark exact scenario fragments, state before/after authority, draw boundary,
separate necessary victim actions, justify each selected metric against source anchor,
name unsupported conclusions. Replay by independently assessing the prose cases under
`.ufo/waves/round-59/CONTRACT.md`, then compare reasons with the independent review.
This is a human-assessment dossier, not a classifier or schema-validity gate. A matching
label with invented evidence fails. No full score/vector or bounty conclusion follows.
''')
append('corpus/README.md','''
## Round-59 F01 deepening — evidence before metric labels

`knowledge/cvss-v4-evidence-assessment.md` (S092) adds PR/UI and subsequent-system impact
judgment to the existing F01 nomenclature overview. No new frontier id or recovered
root surface. Independent prose-scenario assessment, not automatic scoring or reward.
''')
p=Path('corpus/instruments/knowledge-expected.txt');ls=p.read_text().splitlines();ls.append('corpus/knowledge/cvss-v4-evidence-assessment.md');p.write_text('\n'.join(sorted(ls))+'\n')
