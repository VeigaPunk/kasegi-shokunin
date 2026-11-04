PASS — C2 frozen predicate reproduced at implementation pin; one low-severity stale cross-reference remains (recommendation only, not admission).

## Scope and provenance
Axes: depth:verifiability and coverage. Reviewed only C2/F42/S094. No C1 checks, delegation, live exploit or network reproduction. Rules were read first alongside frozen claims. No tools installed or updated.

Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin
Implementation: 13c8060b343e002339ffd72da37ff74514f82765
Base: c33d24ddd11abf1ebdea0dccf7327e9069dd9104
Claims freeze: 6f88f3a7f6b9689b49241e3f4a8e551c57a3f766
Scratch: /fast/scratch/hyaku/kasegi-r61/ReviewC2/

`git -C /fast/scratch/hyaku/kasegi-r61/ReviewC2/clone show 6f88f3a7f6b9689b49241e3f4a8e551c57a3f766:.ufo/waves/round-61/claims.json` exited 0; returned bytes equal the pinned claims file.

## Findings by severity

LOW — The existing tracker entry now contains a stale present-tense exclusivity claim. /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/google-big-sleep-findings-tracker.md:61-63 says the 2024-10 post is in no admitted source row. This cutover adds that post as S094 at /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md:102 and admits F42 at /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md:1019. Qualify the old sentence historically or link S094; no registry id/URL change is needed. This does not falsify C2's frozen counting or distinct-ground predicate.

No medium/high C2 defect observed. All required after values and base values reproduced.

## Ground and invariants

- /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/project-zero-big-sleep-sqlite-variant-analysis.md:10,14 preserves first-party attribution, publication date, same-day fix and pre-release/no-user-impact qualification. Captured support: /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-61/S094.txt:13-18.
- Entry :20-22 preserves recent-commit seeding, manual filtering, commit-message/diff input and HEAD review; capture :24-25 supports it. No unseeded-discovery success-rate claim.
- Entry :26-28 preserves missing generate_series, unaffected old harness, the team's CLI AFL run, 150 CPU-hours and experimental/target-specific-fuzzer caveat; capture :112-118 supports it. No universal saturation or agent-superiority claim is admitted. The source's saturation speculation at :115 is not promoted into a lane fact.
- Entry :34 distinguishes held ground. Compared actual entries: /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/ai-assisted-finding-validation.md:6-25 (principles/validation), /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/google-big-sleep-findings-tracker.md:19-66 (tracker/disclosure/fields), and /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md:12-34 (V8 production/re-discovery comparison). F42 adds a separate dated SQLite case rather than recounting these surfaces.
- Parsed Markdown registry lines with `^\| (S\d+) \|.*$`: base rows=93, implementation rows=94; changed old full rows=[]; added=['S094']. Full old-row equality is stronger than old id/URL invariance. Git diff likewise only adds S094 and a blank line.
- SHA256 of S094.txt independently computed with hashlib: 663ac16df13b7c93c2d9848265854625c46e8f59d0c39a5bbb4d68bf6573e804, matching frozen source_digest.
- Expected new entry occurs at /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/knowledge-expected.txt:62; sort check below passed.

## Exact setup and execution

Initial setup command (exit 0):
```sh
mkdir -p /fast/scratch/hyaku/kasegi-r61/ReviewC2/tmp && git clone --no-local -q /home/vgpnk/Projects/shokunin/kasegi-shokunin /fast/scratch/hyaku/kasegi-r61/ReviewC2/clone && git -C /fast/scratch/hyaku/kasegi-r61/ReviewC2/clone checkout -q 13c8060b343e002339ffd72da37ff74514f82765 && git -C /fast/scratch/hyaku/kasegi-r61/ReviewC2/clone rev-parse HEAD
```
Output: 13c8060b343e002339ffd72da37ff74514f82765.
An earlier invocation selected a nonexistent scratch cwd and failed before execution (tool supplied no numeric exit). Procedural deviations: initial clone/checkout omitted TMPDIR and pre-checkout top-level assertion; all assigned probes and archive/export subsequently used the seat TMPDIR. Only the named scratch clone was checked out; lane git state was not mutated.

Export, executed via Python subprocess (both exit 0):
```sh
git -C /fast/scratch/hyaku/kasegi-r61/ReviewC2/clone archive c33d24ddd11abf1ebdea0dccf7327e9069dd9104
# stdout bytes passed directly as stdin to:
tar -x -C /fast/scratch/hyaku/kasegi-r61/ReviewC2/base
```
For export and every probe, environment was inherited plus TMPDIR=/fast/scratch/hyaku/kasegi-r61/ReviewC2/tmp and PYTHONDONTWRITEBYTECODE=1. Probe subprocesses used shell=True and explicit cwd as below; independent checks ran concurrently. Commands below are exact frozen commands, including their relative arguments; absolute execution roots are specified explicitly.

### implementation: cwd=/fast/scratch/hyaku/kasegi-r61/ReviewC2/clone

```sh
python3 corpus/instruments/frontier-recheck-count.py
```
```text
FRONTIER-CENSUS rows=42 admitted=42 closed=42 problem-rows=0 registry=94
FRONTIER-PASS F01 ids=S001,S002
FRONTIER-PASS F02 ids=S003,S004,S005
FRONTIER-PASS F03 ids=S006,S007,S008
FRONTIER-PASS F04 ids=S009,S010,S011,S012
FRONTIER-PASS F05 ids=S013,S014,S015
FRONTIER-PASS F06 ids=S018
FRONTIER-PASS F07 ids=S031
FRONTIER-PASS F08 ids=S029
FRONTIER-PASS F09 ids=S032,S033,S034,S035
FRONTIER-PASS F10 ids=S036,S037,S038,S039,S040
FRONTIER-PASS F11 ids=S041
FRONTIER-PASS F12 ids=S041,S042
FRONTIER-PASS F13 ids=S043,S044,S045
FRONTIER-PASS F14 ids=S041,S046,S047
FRONTIER-PASS F15 ids=S048
FRONTIER-PASS F16 ids=S049,S050
FRONTIER-PASS F17 ids=S051
FRONTIER-PASS F18 ids=S052
FRONTIER-PASS F19 ids=S053
FRONTIER-PASS F20 ids=S054
FRONTIER-PASS F21 ids=S055
FRONTIER-PASS F22 ids=S057
FRONTIER-PASS F23 ids=S060
FRONTIER-PASS F24 ids=S063
FRONTIER-PASS F25 ids=S064
FRONTIER-PASS F26 ids=S069
FRONTIER-PASS F27 ids=S071
FRONTIER-PASS F28 ids=S073
FRONTIER-PASS F29 ids=S074,S076
FRONTIER-PASS F30 ids=S078
FRONTIER-PASS F31 ids=S080
FRONTIER-PASS F32 ids=S081
FRONTIER-PASS F33 ids=S083
FRONTIER-PASS F34 ids=S085
FRONTIER-PASS F35 ids=S086
FRONTIER-PASS F36 ids=S087
FRONTIER-PASS F37 ids=S088
FRONTIER-PASS F38 ids=S089,S090
FRONTIER-PASS F39 ids=S091
FRONTIER-PASS F40 ids=S092
FRONTIER-PASS F41 ids=S093
FRONTIER-PASS F42 ids=S094
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0   
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0   
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0   
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0   
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0   
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0   
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0   
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0   
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0   
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0   
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0   
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0   
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0   
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0   
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0   
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0   
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0   
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0   
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0   
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0   
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0   
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0   
PASS     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=0   
PASS     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055           exit=0   
PASS     F22  knowledge/cisa-when-to-issue-vex.md                  ids=S057           exit=0   
PASS     F23  knowledge/cyclonedx-analysis-subtree.md              ids=S060           exit=0   
PASS     F24  knowledge/rfc-9116-security-txt.md                   ids=S063           exit=0   
PASS     F25  knowledge/cve-json-record-format.md                  ids=S064           exit=0   
PASS     F26  corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md ids=S069           exit=0   
PASS     F27  corpus/knowledge/linux-kernel-security-bugs-reporting-process.md ids=S071           exit=0   
PASS     F28  corpus/knowledge/github-private-vulnerability-reporting.md ids=S073           exit=0   
PASS     F29  corpus/knowledge/github-repository-security-advisories.md ids=S076           exit=0   
PASS     F30  corpus/knowledge/cve-services-publication-api.md     ids=S078           exit=0   
PASS     F31  corpus/knowledge/osv-affected-range-events.md        ids=S080           exit=0   
PASS     F32  corpus/knowledge/cisa-vulnrichment-adp-enrichment.md ids=S081           exit=0   
PASS     F33  knowledge/nvd-api-2.0-retrieval-interface.md         ids=S083           exit=0   
PASS     F34  knowledge/nvd-api-2.0-response-schema.md             ids=S085           exit=0   
PASS     F35  knowledge/openssf-scorecard-checks.md                ids=S086           exit=0   
PASS     F36  knowledge/github-repository-security-advisories-rest-api.md ids=S087           exit=0   
PASS     F37  knowledge/cisa-vulnrichment-record-list.md           ids=S088           exit=0   
PASS     F38  knowledge/iso-29147-30111-standard-records.md        ids=S089,S090      exit=0   
PASS     F39  knowledge/aisi-autonomous-cyber-capability-progress-rate.md ids=S091           exit=0   
PASS     F40  knowledge/google-big-sleep-findings-tracker.md       ids=S092           exit=0   
PASS     F41  knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md ids=S093           exit=0   
PASS     F42  knowledge/project-zero-big-sleep-sqlite-variant-analysis.md ids=S094           exit=0   
entries=45 pass=45 exit=0
exit=0
```

### implementation: cwd=/fast/scratch/hyaku/kasegi-r61/ReviewC2/clone

```sh
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-61/manifest.json --source S094
```
```text
S094:sha256 OK
S094:Q1 OK occurrences=1 anchor=18-ok
S094:Q2 OK occurrences=1 anchor=25-ok
S094:Q3 OK occurrences=1 anchor=25-ok
S094:Q4 OK occurrences=1 anchor=112-ok
S094:Q5 OK occurrences=1 anchor=113-ok
S094:Q6 OK occurrences=1 anchor=118-ok
S094:Q7 OK occurrences=1 anchor=118-ok
exit=0
```

### implementation: cwd=/fast/scratch/hyaku/kasegi-r61/ReviewC2/clone

```sh
python3 corpus/instruments/capture-binding-check.py
```
```text
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-35 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-36 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-37 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-38 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-39 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-40 records=8 url_bound=8 fetched=8 archival=0
MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-42 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-43 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-44 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-45 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-46 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-46-a2 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-47 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-49 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-50 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-51 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-52 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-53 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-54 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-55 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-56 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-57 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-58 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-59 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-60 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-61 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=77 with_url=77 with_fetched_utc=39 with_archival=38 snapshot_dirs=37 manifest_dirs=37 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=77 bound=77 unbound=0
exit=0
```

### implementation: cwd=/fast/scratch/hyaku/kasegi-r61/ReviewC2/clone

```sh
LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt
```
```text
exit=0
```

### implementation: cwd=/fast/scratch/hyaku/kasegi-r61/ReviewC2/clone

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md
```
```text
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	W04	S076 duplicate url docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories across scopes
file	W04	S080 duplicate url ossf.github.io/osv-schema across scopes
file	W04	S085 duplicate url csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema across scopes
file	ok	/fast/scratch/hyaku/kasegi-r61/ReviewC2/clone/corpus/SOURCES.md
exit=0
```

### base: cwd=/fast/scratch/hyaku/kasegi-r61/ReviewC2/base

```sh
python3 corpus/instruments/frontier-recheck-count.py
```
```text
FRONTIER-CENSUS rows=41 admitted=41 closed=41 problem-rows=0 registry=93
FRONTIER-PASS F01 ids=S001,S002
FRONTIER-PASS F02 ids=S003,S004,S005
FRONTIER-PASS F03 ids=S006,S007,S008
FRONTIER-PASS F04 ids=S009,S010,S011,S012
FRONTIER-PASS F05 ids=S013,S014,S015
FRONTIER-PASS F06 ids=S018
FRONTIER-PASS F07 ids=S031
FRONTIER-PASS F08 ids=S029
FRONTIER-PASS F09 ids=S032,S033,S034,S035
FRONTIER-PASS F10 ids=S036,S037,S038,S039,S040
FRONTIER-PASS F11 ids=S041
FRONTIER-PASS F12 ids=S041,S042
FRONTIER-PASS F13 ids=S043,S044,S045
FRONTIER-PASS F14 ids=S041,S046,S047
FRONTIER-PASS F15 ids=S048
FRONTIER-PASS F16 ids=S049,S050
FRONTIER-PASS F17 ids=S051
FRONTIER-PASS F18 ids=S052
FRONTIER-PASS F19 ids=S053
FRONTIER-PASS F20 ids=S054
FRONTIER-PASS F21 ids=S055
FRONTIER-PASS F22 ids=S057
FRONTIER-PASS F23 ids=S060
FRONTIER-PASS F24 ids=S063
FRONTIER-PASS F25 ids=S064
FRONTIER-PASS F26 ids=S069
FRONTIER-PASS F27 ids=S071
FRONTIER-PASS F28 ids=S073
FRONTIER-PASS F29 ids=S074,S076
FRONTIER-PASS F30 ids=S078
FRONTIER-PASS F31 ids=S080
FRONTIER-PASS F32 ids=S081
FRONTIER-PASS F33 ids=S083
FRONTIER-PASS F34 ids=S085
FRONTIER-PASS F35 ids=S086
FRONTIER-PASS F36 ids=S087
FRONTIER-PASS F37 ids=S088
FRONTIER-PASS F38 ids=S089,S090
FRONTIER-PASS F39 ids=S091
FRONTIER-PASS F40 ids=S092
FRONTIER-PASS F41 ids=S093
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0   
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0   
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0   
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0   
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0   
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0   
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0   
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0   
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0   
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0   
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0   
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0   
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0   
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0   
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0   
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0   
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0   
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0   
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0   
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0   
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0   
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0   
PASS     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054           exit=0   
PASS     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055           exit=0   
PASS     F22  knowledge/cisa-when-to-issue-vex.md                  ids=S057           exit=0   
PASS     F23  knowledge/cyclonedx-analysis-subtree.md              ids=S060           exit=0   
PASS     F24  knowledge/rfc-9116-security-txt.md                   ids=S063           exit=0   
PASS     F25  knowledge/cve-json-record-format.md                  ids=S064           exit=0   
PASS     F26  corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md ids=S069           exit=0   
PASS     F27  corpus/knowledge/linux-kernel-security-bugs-reporting-process.md ids=S071           exit=0   
PASS     F28  corpus/knowledge/github-private-vulnerability-reporting.md ids=S073           exit=0   
PASS     F29  corpus/knowledge/github-repository-security-advisories.md ids=S076           exit=0   
PASS     F30  corpus/knowledge/cve-services-publication-api.md     ids=S078           exit=0   
PASS     F31  corpus/knowledge/osv-affected-range-events.md        ids=S080           exit=0   
PASS     F32  corpus/knowledge/cisa-vulnrichment-adp-enrichment.md ids=S081           exit=0   
PASS     F33  knowledge/nvd-api-2.0-retrieval-interface.md         ids=S083           exit=0   
PASS     F34  knowledge/nvd-api-2.0-response-schema.md             ids=S085           exit=0   
PASS     F35  knowledge/openssf-scorecard-checks.md                ids=S086           exit=0   
PASS     F36  knowledge/github-repository-security-advisories-rest-api.md ids=S087           exit=0   
PASS     F37  knowledge/cisa-vulnrichment-record-list.md           ids=S088           exit=0   
PASS     F38  knowledge/iso-29147-30111-standard-records.md        ids=S089,S090      exit=0   
PASS     F39  knowledge/aisi-autonomous-cyber-capability-progress-rate.md ids=S091           exit=0   
PASS     F40  knowledge/google-big-sleep-findings-tracker.md       ids=S092           exit=0   
PASS     F41  knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md ids=S093           exit=0   
entries=44 pass=44 exit=0
exit=0
```

### base: cwd=/fast/scratch/hyaku/kasegi-r61/ReviewC2/base

```sh
python3 corpus/instruments/capture-binding-check.py
```
```text
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-35 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-36 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-37 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-38 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-39 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-40 records=8 url_bound=8 fetched=8 archival=0
MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-42 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-43 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-44 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-45 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-46 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-46-a2 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-47 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-49 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-50 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-51 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-52 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-53 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-54 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-55 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-56 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-57 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-58 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-59 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-60 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=76 with_url=76 with_fetched_utc=38 with_archival=38 snapshot_dirs=36 manifest_dirs=36 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=76 bound=76 unbound=0
exit=0
```

## Receipt comparison and residual risks

The base frontier output and base capture-binding output each matched verbatim as substrings of /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/do-nothing-c2-r61.txt. Thus the do-nothing comparison is an actual exported-base replay, not a repeated assertion. Implementation matches rows=42/admitted=42/closed=42/problem-rows=0/registry=94, F42=S094, entries=45/pass=45 and captures=77/bound=77/unbound=0. All seven quotes occur once at the expected anchors, sort is clean, and census exits 0.

Existing census W04 duplicate-URL warnings and capture orphan S040-live.txt remain visible; they are not new failures or suppressed outputs. Capture checks verify pinned text, not live freshness, the original experiment or independent SQLite reproduction. The frontier wrapper also runs pre-existing recheck commands, some with hard-coded lane cwd; consequently overall old-entry PASS lines are not proof of fully isolated old-source validation. The new F42 recheck is relative and was separately executed directly against the pinned clone. Base structural counts and registry invariance were additionally obtained from the exported base files themselves.

Semantic tooling gap: reading xd://lsp returned “No such tool”; no LSP device/server was available for status/references/definition/diagnostics. Text reads and registry parsing were fallback evidence, not semantic caller proof. No runtime/rerouting/resume implementation changes occur in this C2 source-admission scope, so those generic reviewer axes are inapplicable.

All raw assigned command receipts are preserved above in this report. Scratch deletion is recorded below after removal.

Cleanup executed: `rm -rf -- /fast/scratch/hyaku/kasegi-r61/ReviewC2 && test ! -e /fast/scratch/hyaku/kasegi-r61/ReviewC2`; exit 0, no output. Scratch is removed. No commits or pushes.
