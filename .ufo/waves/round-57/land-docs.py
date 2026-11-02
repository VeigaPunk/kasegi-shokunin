# Append declared round-57 corrections; preserve legacy bytes. Exit 0 success.
import pathlib,json,hashlib
R=pathlib.Path('.'); W=R/'.ufo/waves/round-57'; cap=W/'controls/S089.txt'
D=R/'corpus/source-snapshots/round-57';D.mkdir(exist_ok=True);(D/'S089.txt').write_bytes(cap.read_bytes())
quotes=[('Q1',760,'Entries in the events array may be “last_affected” or “fixed” events, but not both.'),('Q2',825,'if IncludedInVersions(v, affected.versions) || IncludedInRanges(v, affected.ranges)')]
manifest={'schema_version':1,'sources':[{'id':'S089','url':'https://ossf.github.io/osv-schema/','capture_url':'https://ossf.github.io/osv-schema/','fetched_utc':'2026-11-02T20:03:16Z','http':{'status':200},'kind':'html','path':'S089.txt','sha256':hashlib.sha256(cap.read_bytes()).hexdigest(),'quotes':[{'id':i,'anchor':a,'quote':q} for i,a,q in quotes]}]}
(D/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
blocks={
'corpus/knowledge/osv-affected-range-events.md':'''\n## Correction (round 57, 2026-11-02) — evaluation union and exclusion scope

Supersedes Claim 2's implication that events alone decide affectedness and Claim 3's
sentence beginning `A record may carry` at original line 60; preserves the historical bytes.
Correction source: S089, https://ossf.github.io/osv-schema/, Evaluation and Requirements,
version 1.9.2, independently reopened 2026-11-02; captured at
`corpus/source-snapshots/round-57/S089.txt` lines 760-761 and 819-856.
Correction verified-at: 2026-11-02.
Correction recheck (from lane root): `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-57/manifest.json --source S089`.

For the matching package, explicit version membership OR any range membership establishes
affectedness. Excluding a version from a range does not cancel its explicit membership.
The fixed/last_affected prohibition is per events array, not per record, package, or all ranges.
Boundary decisions differ: fixed excludes its boundary; last_affected includes its boundary.
Absent explicit limits means no upper limit; the old Claim 2 wording `still bounded` must
not be read as a finite bound. Event values and explicit versions have distinct comparison roles.
Located source quotes are recorded once in `corpus/lessons/round-57.md` Gate, Q1/Q2.

Operational check: `python3 corpus/instruments/osv-semantic-check.py` exercises frozen
synthetic inputs, including explicit-only and explicit-overrides-fixed, separate-arrays
versus mixed-same-array, wrong-package, boundaries, and unsupported comparators.
`osv-affectedness.py` is a deliberately bounded teaching implementation, NOT a scanner:
exact ecosystem/name identity; exact explicit-version strings; numeric-release-only SEMVER
x.y.z without leading zeros (plus introduced 0 / limit *). Prereleases/build metadata,
ECOSYSTEM and GIT range comparison are unsupported, not inferred unaffected. Another
supported true OR limb may still establish affectedness. Structural errors in matching
entries are rejected before evaluation; conflicting equal-version event kinds are unsupported.
This extra validation is local admission policy, not the specification's evaluation pseudocode.
It neither validates the full OSV schema nor establishes deployment exposure, exploitability,
withdrawal handling, normalized package equivalence, or authorization to test a real target.

Gate rejection: a universal comparator and a range-only classifier are refused. Flip requires
an independently sourced comparator and new frozen semantic controls, not a type-name cast.
''',
'corpus/README.md':'''\n## Correction (round 57, 2026-11-02) — F31 affectedness

Supersedes F31's original line 743 instruction `not from the versions list`: use explicit
version membership OR range membership for the matching package. Its `still bounded`
wording means no finite ceiling when the implicit limit is infinity. The knowledge entry's
round-57 correction supersedes its record-wide fixed/last_affected exclusion; the exclusion
is per events array. Source S089 (fresh Evaluation/Requirements reading), with runnable
semantic controls at `corpus/instruments/osv-semantic-check.py`. F31 is deepened, not a new
frontier row; F01-F37 and their historical admission records remain unchanged. This is a
bounded teaching evaluator, not a general vulnerability scanner or an ecosystem comparator.
''',
'PROVINCE.md':'''\n## Round-57 cloud surface annotation (2026-11-02)

Current writable lane: `/workspace/scratch/e2fdad13233f/shokunin-training/lanes/kasegi`.
Fleet contract: `/workspace/scratch/e2fdad13233f/shokunin-training/shokunin` (read-only to lane).
Historical lost domain roots remain unavailable; this is not recovery or a denominator re-scope.
F31 is deepened by bounded synthetic OSV affectedness evaluation on S089, not expanded to a
service/API, scanner, live target, general ecosystem comparator, or Git-graph engine. The
round-57 named correction in its existing knowledge entry governs over the earlier summary.
''',
'SKILL.md':'''\n## Round-57 OSV affectedness decision table and gate registry (2026-11-02)

Trigger: interpreting an OSV affectedness fragment. Anti-trigger: real-target scanning or
submission. S089 grounds the correction in `corpus/knowledge/osv-affected-range-events.md`
(round-57 correction); research method remains chousa-owned, secrets remain kagi-owned.

| Input situation | Decision |
|---|---|
| Exact package and explicit version match | Affected, even when all supported ranges exclude it |
| A supported range includes the version | Affected even when explicit versions do not list it |
| All relevant limbs known false | Unaffected within this fragment only, not a deployment safety assertion |
| No true limb and an unsupported comparator | Could-not-evaluate; never silently unaffected |
| Same events array contains fixed and last_affected | Invalid; different arrays may independently use each |
| A release equals fixed / last_affected | Excluded / included respectively |

Checklist: identify exact ecosystem/name; validate matching-entry shapes; apply the OR;
keep unsupported distinct from false; preserve the reason and exit; never elevate this
synthetic result to exploitation, target authorization, full-schema validation or deployment exposure.
Numeric-release-only SEMVER means canonical x.y.z triples, introduced 0 and limit * only.
No prerelease/build ordering, ECOSYSTEM comparator, Git traversal, purl normalization or
withdrawal handling. Conflicting equal-version event kinds are unsupported. Local structural
validation precedes evaluation, including explicit membership; this is a scoped admission rule.

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| osv-affectedness.py | probe | `python3 corpus/instruments/osv-affectedness.py < fragment.json` | 0 determinate, NOT clean/safe; 2 unsupported could-not-evaluate; 3 invalid could-not-evaluate; 64 usage could-not-evaluate | paired harness below exercises actual CLI | .ufo/waves/round-57/fixtures.json | read stdin only | kasegi |
| osv-semantic-check.py | gate | `python3 corpus/instruments/osv-semantic-check.py` | 0 clean; 1 failed; 2 could-not-evaluate; 64 usage could-not-evaluate | `python3 corpus/instruments/osv-semantic-check.py --selftest` (five CLI-output controls) | .ufo/waves/round-57/claims.json and fixtures.json (digest pinned) | read-only; selftest temporary fixtures removed | kasegi |

Mutation demonstration: `python3 .ufo/waves/round-57/mutations.py` checks actual status flips,
not keyword matches. The erroneous-reading model is reconstructed from the two filed prose
defects; it is explicitly NOT a claim that an earlier executable existed.
'''}
# Pre-landing declaration protects front-door appends from receipt contamination.
(W/'append-declarations.json').write_text(json.dumps({p:{'base_bytes':len((R/p).read_bytes()),'base_sha256':hashlib.sha256((R/p).read_bytes()).hexdigest(),'append_lines':b.count('\n'),'append_sha256':hashlib.sha256(b.encode()).hexdigest()} for p,b in blocks.items()},indent=2)+'\n')
for p,b in blocks.items():
 with (R/p).open('a') as f:f.write(b)
row='| S089 | OpenSSF OSV specification — https://ossf.github.io/osv-schema/ | spec | A | Matching-package affectedness union and per-events-array closure exclusion | Evaluation and Requirements; version 1.9.2; round-57 capture lines 760-761 and 819-856 | supersedes S080 — explicit versions OR ranges determine affectedness; fixed/last_affected exclusion is local to each events array, not the record | mined | 2026-11-02 | 90d | corpus/knowledge/osv-affected-range-events.md, corpus/lessons/round-57.md |\n'
p=R/'corpus/SOURCES.md';s=p.read_text();lines=s.splitlines(keepends=True);i=next(i for i,x in enumerate(lines) if x.startswith('| S088 |'));lines.insert(i+1,row);p.write_text(''.join(lines))
with p.open('a') as f:f.write('\n- Round-57 semantic correction search: identified/screened/included one official source, excluded zero source documents; OSV Evaluation and Requirements reopened 2026-11-02. S089 is the scoped supersession, no old row cells changed. Rejected candidate inference: range-only/record-wide interpretation and general comparator support, not the source itself. Stop: exact rule and discriminating synthetic cases established; no target queries.\n')
print('declared-appends='+str(len(blocks)));print('quote-words='+str(sum(len(q.split()) for _,_,q in quotes)))
