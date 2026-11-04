PASS — all executed C1/C2 counters match frozen after-wants; C1 probe scratch argument relocated for seat isolation, so the frozen shared-path literal was not executed.

# ExecCounters: round 61 / w1

Axes: depth:verifiability and coverage. This is a counter execution report, not a sandbox claim or a SQLite reproduction.

## Scope, provenance, and literal-runnability

- Read `/home/vgpnk/.omp/agent/RULES.md` first. No tools installed or updated; no pacman transaction.
- Production changes: only this report. No lane git/jj mutations, commits, pushes, or fixture commits. The clone copied committed state only; a pre-existing production `corpus/SOURCES.md` modification was not imported.
- All counters ran once, concurrently, through `bash -c COMMAND`, with cwd `/fast/scratch/hyaku/kasegi-r61/ExecCounters/clone` and `TMPDIR=/fast/scratch/hyaku/kasegi-r61/ExecCounters/tmp`.
- Frozen claims identity: `git -C /fast/scratch/hyaku/kasegi-r61/ExecCounters/clone show 6f88f3a7f6b9689b49241e3f4a8e551c57a3f766:.ufo/waves/round-61/claims.json` exited 0; full text equals the clone's claims file.
- Clone setup: `mkdir -p /fast/scratch/hyaku/kasegi-r61/ExecCounters/tmp && export TMPDIR=/fast/scratch/hyaku/kasegi-r61/ExecCounters/tmp && git clone --no-hardlinks --quiet /home/vgpnk/Projects/shokunin/kasegi-shokunin /fast/scratch/hyaku/kasegi-r61/ExecCounters/clone && git -C /fast/scratch/hyaku/kasegi-r61/ExecCounters/clone rev-parse HEAD && git -C /fast/scratch/hyaku/kasegi-r61/ExecCounters/clone status --porcelain=v1 | wc -l` exited 0: implementation pin `13c8060b343e002339ffd72da37ff74514f82765`, dirty-line count 0. No checkout/reset was needed. An initial attempt failed before execution because its requested cwd did not yet exist; creation was retried from an existing cwd.
- Pin receipt: `git -C /fast/scratch/hyaku/kasegi-r61/ExecCounters/clone rev-parse --show-toplevel HEAD` exited 0 and printed the clone root and that exact pin.
- C1 command 1's frozen final argument is `/fast/scratch/hyaku/kasegi-r61/verify/probes`. It violates this seat's exclusive scratch boundary, so only that argument was replaced with `/fast/scratch/hyaku/kasegi-r61/ExecCounters/probes`. No frozen rules/claims were edited. Runner lines 15–20 accept either pathname but recursively delete/create it and trap-delete it; therefore literal execution of the shared-path command was intentionally withheld. The adapted command is observed runnable; shared-path availability is not claimed.
- Other nine counting commands ran literally, including the external census script. Relative operands are interpreted under the explicit absolute clone cwd above.

Digest command (exit 0):
```sh
sha256sum /fast/scratch/hyaku/kasegi-r61/ExecCounters/clone/corpus/instruments/figure-audit.py /fast/scratch/hyaku/kasegi-r61/ExecCounters/clone/corpus/instruments/figure-audit-mutbat.py /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
```
```text
051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9  figure-audit.py
f94393d981eeb93a05f6c57782b787faabfc56bfa5b4775f1c319f405fdd353c  figure-audit-mutbat.py
3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30  external sources-census.sh
```
Both instrument digests equal the frozen claims. External census code is not pinned by the lane commit; its digest is retained above.

## Before/after comparison

Before-values below are historical committed receipts, not a separately rerun base checkout. All after-values are fresh executions retained in full below.

| Predicate | Frozen before | Fresh after | Match after-want |
|---|---|---|---|
| C1 P1/P2/P3 | exit 1, markers 1 | each exit 2, markers 0, derive-not-read-only | yes |
| C1 P4 | refused | exit 2, markers 0 | yes |
| C1 P5/P6 | admitted, derived 35 | each exit 0, derived 35 | yes |
| C1 regression controls | derived 35 / 1 | exit 0, derived 35 / 1 | yes |
| C1 selftest | cases 20 | cases 24, failures 0, exit 0 | yes |
| C1 mutation battery | 2/2 | killed 3/3, survivors 0, controls pass, exit 0 | yes |
| C1 ledger | after-want 35/35 | figures 35, ok 35, stale 0, exit 0 | yes |
| C1 stale fixture | after-want exit 1 | figures 2, ok 0, stale 2, exit 1 | yes |
| C2 frontier | rows/admitted/closed 41, registry 93 | rows/admitted/closed 42, problems 0, registry 94, F42/S094 passes | yes |
| C2 entry checks | entries/pass 44 | entries/pass 45, exit 0 | yes |
| C2 binding | records/bound 76 | records/bound 77, unbound 0, exit 0 | yes |
| C2 S094 | seven after-want quotes | digest and Q1–Q7 OK, exit 0 | yes |
| C2 expected list | sorted after-want | no output, exit 0 | yes |
| C2 census | exit 0 after-want | exit 0; W04 warnings only | yes |

## Path:line evidence

All following absolute paths are retained production files at the implementation pin (the scratch clone has been deleted after capturing receipts).

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/c1-probe-run-r61.sh:15-20`: accepted scratch shape, destructive scratch setup, cleanup trap.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/c1-probe-run-r61.sh:43-54`: exact six probes and two controls.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/c1-probes-base-r61.txt:4-11`: historical before probe/control outcomes.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/do-nothing-c2-r61.txt:2`: historical frontier 41/41/41, registry 93.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/do-nothing-c2-r61.txt:88`: historical entries/pass 44.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/do-nothing-c2-r61.txt:128-129`: historical capture records/bound 76.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/c2-standin-r61.txt:44,89-90`: recorded F42/S094 and after entry tally; corroborated by fresh C2.1 below.
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:16-18,29-33`: warnings do not fail validation; W04 means same URL across scopes.

## Full fresh command receipts

Outputs below combine stdout/stderr without truncation. C1.5 exit 1 is the required red result, not an unexpected failure. Empty C2.4 output is explicitly noted.

### C1.1

```sh
bash .ufo/waves/round-61/controls/c1-probe-run-r61.sh corpus/instruments/figure-audit.py /fast/scratch/hyaku/kasegi-r61/ExecCounters/probes
```

Exit: 0

```text
instrument=/fast/scratch/hyaku/kasegi-r61/ExecCounters/clone/corpus/instruments/figure-audit.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:26:07Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/ExecCounters/probes/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
```

### C1.2

```sh
python3 corpus/instruments/figure-audit.py --selftest
```

Exit: 0

```text
selftest case=ok-ledger exit=0 want=0 verdict=pass
selftest case=stale-literal exit=1 want=1 verdict=pass
selftest case=derive-fails-fail-closed exit=1 want=1 verdict=pass
selftest case=token-boundary-34-vs-340 exit=1 want=1 verdict=pass
selftest case=unreadable-ledger-exit-2 exit=2 want=2 verdict=pass
selftest case=derive-not-read-only-refused exit=2 want=2 verdict=pass
selftest case=chain-semicolon-refused exit=2 want=2 verdict=pass
selftest case=chain-background-refused exit=2 want=2 verdict=pass
selftest case=chain-newline-refused exit=2 want=2 verdict=pass
selftest case=chain-cmdsubst-refused exit=2 want=2 verdict=pass
selftest case=pipe-to-shell-refused exit=2 want=2 verdict=pass
selftest case=redirect-refused exit=2 want=2 verdict=pass
selftest case=or-chain-refused exit=2 want=2 verdict=pass
selftest case=quoted-separator-admitted exit=0 want=0 verdict=pass
selftest case=escape-single-quote-refused exit=2 want=2 verdict=pass
selftest case=escape-double-quote-refused exit=2 want=2 verdict=pass
selftest case=sed-head-refused exit=2 want=2 verdict=pass
selftest case=awk-head-refused exit=2 want=2 verdict=pass
selftest case=sort-output-flag-refused exit=2 want=2 verdict=pass
selftest case=git-show-output-flag-refused exit=2 want=2 verdict=pass
selftest case=python-inside-admitted exit=0 want=0 verdict=pass
selftest case=python-traversal-refused exit=2 want=2 verdict=pass
selftest case=python-symlink-refused exit=2 want=2 verdict=pass
selftest case=python-absolute-refused exit=2 want=2 verdict=pass
selftest cases=24 failures=0
```

### C1.3

```sh
python3 corpus/instruments/figure-audit-mutbat.py
```

Exit: 0

```text
PRISTINE selftest_exit=0 last='selftest cases=24 failures=0'
CONTROL c-equivalent-trailing-space selftest_exit=0 must_not_be_killed=held last='selftest cases=24 failures=0'
MUT m4-drop-stale-literal-case sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=23 failures=1'
MUT m6-readonly-gate-off sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=24 failures=4'
MUT m7-python-confinement-off sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=24 failures=2'
mutbat killed=3/3 survivors=0 controls=pass
```

### C1.4

```sh
python3 corpus/instruments/figure-audit.py
```

Exit: 0

```text
FIG frontier-rows recorded=34 derived=34 ok
FIG registry-rows recorded=85 derived=85 ok
FIG knowledge-expected-entries recorded=72 derived=72 ok
FIG knowledge-files recorded=72 derived=72 ok
FIG capture-lines-s085 recorded=543 (filed; superseded by the r54 D53-2 correction) derived=542 ok
FIG capture-bytes-s085 recorded=7590 derived=7590 ok
FIG capture-lines-s086 recorded=731 derived=731 ok
FIG capture-sha256-s086 recorded=fa84a01753971589571c22597d5b7f65ed34dc373dfc466d2233437faf4dc81f derived=fa84a01753971589571c22597d5b7f65ed34dc373dfc466d2233437faf4dc81f ok
FIG frontier-rows-r54 recorded=35 derived=35 ok
FIG registry-rows-r54 recorded=86 derived=86 ok
FIG entries-r54 recorded=38 derived=38 ok
FIG knowledge-expected-r54 recorded=73 derived=73 ok
FIG knowledge-files-r54 recorded=73 derived=73 ok
FIG figure-audit-mentions-base-scorecard recorded=2 (the receipt's limb; the filed prose 0 superseded) derived=2 ok
FIG figure-audit-mentions-base-log recorded=0 derived=0 ok
FIG figure-audit-mentions-base-knowledge-expected recorded=0 derived=0 ok
FIG frontier-rows-r55 recorded=36 derived=36 ok
FIG registry-rows-r55 recorded=87 derived=87 ok
FIG entries-r55 recorded=39 derived=39 ok
FIG knowledge-expected-r55 recorded=74 derived=74 ok
FIG knowledge-files-r55 recorded=74 derived=74 ok
FIG census-fresh-literal-r55 recorded=stale (the receipt's printed limb; the filed prose ok superseded) derived=stale ok
FIG census-internal-r55-receipt recorded=1118 derived=1118 ok
FIG census-gone-r55-receipt recorded=3883 derived=3883 ok
FIG census-fixedpoint-internal-r55 recorded=1119 derived=1119 ok
FIG census-fixedpoint-gone-r55 recorded=3882 derived=3882 ok
FIG fail-entry-records recorded=33 (the class-check line; the trailer's 34 superseded) derived=33 ok
FIG frontier-rows-r56 recorded=37 derived=37 ok
FIG registry-rows-r56 recorded=88 derived=88 ok
FIG entries-r56 recorded=40 derived=40 ok
FIG knowledge-expected-r56 recorded=75 derived=75 ok
FIG knowledge-files-r56 recorded=75 derived=75 ok
FIG census-fresh-literal-r56 recorded=ok derived=ok ok
FIG census-internal-r56-receipt recorded=1130 derived=1130 ok
FIG census-gone-r56-receipt recorded=3915 derived=3915 ok
FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
```

### C1.5

```sh
python3 corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json
```

Exit: 1

```text
FIG d53-1-trailer recorded=34 derived=33 want=34 stale
FIG d53-2-lines recorded=543 derived=542 want=543 stale
FIGURE-AUDIT figures=2 ok=0 stale=2 exit=1
```

### C2.1

```sh
python3 corpus/instruments/frontier-recheck-count.py
```

Exit: 0

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
```

### C2.2

```sh
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-61/manifest.json --source S094
```

Exit: 0

```text
S094:sha256 OK
S094:Q1 OK occurrences=1 anchor=18-ok
S094:Q2 OK occurrences=1 anchor=25-ok
S094:Q3 OK occurrences=1 anchor=25-ok
S094:Q4 OK occurrences=1 anchor=112-ok
S094:Q5 OK occurrences=1 anchor=113-ok
S094:Q6 OK occurrences=1 anchor=118-ok
S094:Q7 OK occurrences=1 anchor=118-ok
```

### C2.3

```sh
python3 corpus/instruments/capture-binding-check.py
```

Exit: 0

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
```

### C2.4

```sh
LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt
```

Exit: 0

```text
(no output)
```

### C2.5

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md
```

Exit: 0

```text
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	W04	S076 duplicate url docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories across scopes
file	W04	S080 duplicate url ossf.github.io/osv-schema across scopes
file	W04	S085 duplicate url csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema across scopes
file	ok	/fast/scratch/hyaku/kasegi-r61/ExecCounters/clone/corpus/SOURCES.md
```

## Risks and limits

- All scoped numeric predicates match. The exact shared-path probe command remains unexecuted because it would write/delete outside the seat boundary; this is the sole command-literal qualification.
- C1 is only the named probe-set predicate. No universal shell confinement, sandbox, or write-prevention conclusion follows.
- C2 is a dated first-party account. Quote/binding/count success does not reproduce SQLite analysis or independently assess substantive novelty; those are outside this counting seat.
- Existing capture orphan `S040-live.txt` and census W04 warnings are retained verbatim, not suppressed; neither caused the assigned checks to fail.
- No unrelated checks or base reproduction were run. Historical before-values are explicitly distinguished from current runs.

## Cleanup

Executed after preserving receipts:

```sh
rm -rf -- /fast/scratch/hyaku/kasegi-r61/ExecCounters && test ! -e /fast/scratch/hyaku/kasegi-r61/ExecCounters && printf 'cleanup exit=0 scratch absent\n'
```

Exit 0; output: `cleanup exit=0 scratch absent`. No shared scratch was touched.
