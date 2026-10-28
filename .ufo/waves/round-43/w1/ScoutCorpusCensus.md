# ScoutCorpusCensus — kasegi round 43

Axes: coverage (C2 before-counters and the after-delta), depth:verifiability (each counter that must not move has a named command that goes red if it does).

Measured 2026-10-28T16:41:31Z on the worktree of HEAD `4cb6d4ae768481e1a14afbedc2d865a060ebacfd`. That commit is the freeze commit, one ahead of base `ab98fac9dce87130bc4f66de89e30650d63943dc`, and it does not touch `corpus/`. Corpus bytes below are the base bytes. No tool was installed. Instruments were run read-only (`PYTHONDONTWRITEBYTECODE=1`); none was given `--json` or `--selftest`.

## Tree identity

```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
4cb6d4ae768481e1a14afbedc2d865a060ebacfd

git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse --verify ab98fac9dce87130bc4f66de89e30650d63943dc^{commit}
ab98fac9dce87130bc4f66de89e30650d63943dc

git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --name-only ab98fac9dce87130bc4f66de89e30650d63943dc HEAD -- corpus | wc -l
0
```

`git diff --stat` on `corpus` between those two commits is empty. Agrees with `.ufo/waves/round-43/c2-controls/before.txt` (registry 66, knowledge 61, capture 56/56/0, recheck expected 61, frontier entries 28 pass 28, census exit 0) and with `.ufo/waves/round-43/census-before.txt` (the two W04 lines plus `kasegi ok`, exit 0).

## Registry rows and status histogram

Section `## Registry` of `corpus/SOURCES.md` is lines 3–73 (next heading `## Paths` at line 74). Every registry-shaped line is inside that section. `bad_nf=0` (every row splits to 13 awk fields, 11 cells).

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
66
```

Status cell (column 8), same 66 rows:

```
mined=54 rejected=12 queued=0
```

Rejected ids: S022 S024 S026 S027 S028 S056 S058 S059 S061 S062 S065 S066. No queued id. Id span S001–S066, 66 unique, no duplicate id.

`S067` onwards, registry rows: 0.

```
grep -cE '^\|[[:space:]]*S06[7-9][[:space:]]*\|' corpus/SOURCES.md
0
grep -cE '^\|[[:space:]]*S0(6[7-9]|[7-9][0-9])[[:space:]]*\|' corpus/SOURCES.md
0
```

(`grep -c` exits 1 when the count is 0. That is grep, not a census failure. The printed count is 0. `id_max` from the section parse is S066.)

Tier histogram from census mode (below): A=61 B=3 C=2, invalid=0.

Claim-package gate, still absent (C2 before):

```
ls corpus/instruments/claim-package-check.py
ls: cannot access 'corpus/instruments/claim-package-check.py': No such file or directory
ls -d corpus/instruments/fixtures/claim-package
ls: cannot access 'corpus/instruments/fixtures/claim-package': No such file or directory
find corpus/instruments -name '*claim-package*' | wc -l
0
```

## Frontier rows and admitted count

`corpus/README.md` has 25 lines matching `^\| F<n> \|`. 25 unique ids F01–F25, every status cell `admitted`, no duplicate id. Three rows name two knowledge files, so the harness counts 28 entry cells: F09 (`authorised-testing-rules-of-engagement.md`, `statutory-authorization-and-unauthorized-access.md`), F10 (`vendor-disclosure-policies-as-corpus-objects.md`, `vendor-disclosure-policy-commitments-crosswalk.md`), F11 (`iso-29147-and-30111-division-of-labour.md`, `iso-29147-divergence-and-clause-crosswalk.md`). 25 + 3 = 28.

```
PYTHONDONTWRITEBYTECODE=1 python3 corpus/instruments/frontier-recheck-count.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
```

exit 0. stdout:

```
FRONTIER-CENSUS rows=25 admitted=25 closed=25 problem-rows=0 registry=66
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
entries=28 pass=28 exit=0
```

stderr empty.

## Queued rows

Registry status `queued`: 0 of 66. Frontier status `queued`: 0 of 25. Census mode prints a lane status key only when the count is non-zero, so `kasegi status.queued` is absent and the zero is the fleet line `FLEET status.queued 0`.

## Knowledge files

```
ls corpus/knowledge/*.md | wc -l
61
```

## Entries per source id, S060+

Denominator is a header line `^source: S<id>` (the same shape as C2's `grep -rlE '^source: S067'`). Prose mentions are listed separately and are not that counter.

| id | registry status | header entries | header file | other knowledge files mentioning the id |
|---|---|---|---|---|
| S060 | mined | 1 | cyclonedx-analysis-subtree.md | cve-json-record-format.md (comparison table, not a `source:` line) |
| S061 | rejected | 0 | — | — |
| S062 | rejected | 0 | — | — |
| S063 | mined | 1 | rfc-9116-security-txt.md | — |
| S064 | mined | 1 | cve-json-record-format.md | — |
| S065 | rejected | 0 | — | — |
| S066 | rejected | 0 | — | — |
| S067 | no row | 0 | — | no `S067` token anywhere under `corpus/` (`grep -l` exit 1) |

```
grep -rlE '^source: S067' corpus/knowledge | wc -l
0
```

The token `S068` already occurs, and it is not a registry row and not a `source:` header. `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:113` says "staged S068, not this lane's S040". The same token is in `corpus/lessons/round-24.md` through `round-40.md` (14 lesson files). A future row numbered S068 would collide with that prose; it would not be the first occurrence of the string.

## capture-binding-check.py

```
PYTHONDONTWRITEBYTECODE=1 python3 corpus/instruments/capture-binding-check.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
```

exit 0. stderr empty. stdout:

```
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
AUDIT records=56 with_url=56 with_fetched_utc=18 with_archival=38 snapshot_dirs=18 manifest_dirs=18 missing_manifest=0 multi_row_url=3 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=56 bound=56 unbound=0
```

## recheck-audit.py --quiet

```
PYTHONDONTWRITEBYTECODE=1 python3 corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
```

exit 0. stderr empty. stdout:

```
strict pass=61/61 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=37 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=61 total=61 pass=61 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=61 missing=0 unexpected=0 exit=0
```

## source-recheck.py availability

Path `corpus/instruments/source-recheck.py`, tracked, mode `0644` (not directly executable; the invocation is `python3`), 17275 bytes. `ast.parse` ok. `--help` exit 0. No arguments exit 2, stdout `manifest UNAVAILABLE reason=missing-required-argument`.

```
python3 corpus/instruments/source-recheck.py --help
usage: source-recheck.py [-h] [--manifest MANIFEST] [--source SOURCE]
                         [--selftest]
...
help_exit=0

python3 corpus/instruments/source-recheck.py
manifest UNAVAILABLE reason=missing-required-argument
noargs_exit=2
```

## sources-census.sh

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi
```

exit 0. stderr empty. stdout:

```
kasegi	rows	66
kasegi	tier.A	61
kasegi	tier.B	3
kasegi	tier.C	2
kasegi	status.mined	54
kasegi	status.rejected	12
FLEET	rows	66
FLEET	tier.A	61
FLEET	tier.B	3
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	0
FLEET	status.mined	54
FLEET	status.rejected	12
FLEET	status.invalid	0
FLEET	missing	0
```

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```

exit 0. stderr empty. stdout (byte-identical to `.ufo/waves/round-43/census-before.txt` lines 1–3):

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```

W04 does not change the exit (script header: warnings never change status).

## Tracked footprint, `.ufo/` vs total

`git ls-tree -r -l <rev>`, blob sizes, paths under `.ufo/` vs the rest. Untracked wave files are not in these counts.

| rev | files | bytes | .ufo files | .ufo bytes | other files | other bytes | .ufo file share | .ufo byte share |
|---|---|---|---|---|---|---|---|---|
| HEAD 4cb6d4ae | 8451 | 139644593 | 8124 | 132012188 | 327 | 7632405 | 0.961306 | 0.945344 |
| base ab98fac9 | 8442 | 139341514 | 8115 | 131709109 | 327 | 7632405 | 0.961265 | 0.945225 |

HEAD adds 9 tracked paths, all under `.ufo/waves/round-43/`, and deletes none: `build-w1-spec.py`, `c1-controls/do-nothing.txt`, `c2-controls/before.txt`, `census-before.txt`, `claims.json`, `freeze.txt`, `w1-dispatch.json`, `w1-run.err`, `w1-spec.json`. Non-`.ufo` file count and byte count are identical at base and HEAD, which is the corpus-identity check in byte form.

## What C2's after-state moves, and what must stay

Frozen claim C2 (`claims.json`, counting_commands and the after line) moves only these counters. The "after" column is the claim's own target, not a measurement.

| counter | measured now | C2 after | moves? |
|---|---|---|---|
| registry rows `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | 66 | >=68 | yes |
| status mined / rejected | 54 / 12 | 55 / 13 if the add is exactly one mined row (S067) and one reject row | yes |
| `^source: S067` knowledge files | 0 | 1 | yes |
| `corpus/knowledge/*.md` | 61 | 62 | yes, exactly one file |
| capture `records` / `bound` | 56 / 56 | 57 / 57 | yes |
| recheck-audit `expected` | 61 | 62 | yes |
| `claim-package-check.py` and `fixtures/claim-package/` | absent | present | yes |
| SCORECARD capability row `claim-package-gate` | not in this census | enters | yes (named by the claim, not counted here) |

Counters that must stay identical, each with the command that is the no-harm guard. A guard fails closed: the named output changes, or the diff is non-empty.

1. Frontier row set and entry-cell count. Stay `FRONTIER-CENSUS rows=25 admitted=25 closed=25 problem-rows=0` and `entries=28 pass=28 exit=0`. Guard: `python3 corpus/instruments/frontier-recheck-count.py --root <lane>`. The claim's own counting line says no frontier row changes. A new `| F<n> |` row, a second entry cell, or a status flip moves `rows=` or `entries=` or turns a `FRONTIER-PASS` into `FRONTIER-FAIL`.

2. Queued registry rows. Stay 0. Guard: `sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi` still prints `FLEET status.queued 0` and does not print a `kasegi status.queued` line with a positive count. C2's added rows are one mined and one rejected, not a queued row.

3. Census validate exit. Stay 0. Guard: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` exits 0. The two existing W04 lines (S028, S029) may remain; a new W04 does not fail this guard, an E-code does. This is also the claim's kill rule `census exit!=0`.

4. Capture `unbound`. Stay 0 while `records` and `bound` go 56 to 57. Guard: `capture-binding-check.py` prints `unbound=0`. Same run must still print `missing_manifest=0`, `digest_unpinned=0`, and `orphans=1 orphan=S040-live.txt` (the declared orphan is not a binding count and must not be dropped or joined by a second orphan). `snapshot_dirs` and `manifest_dirs` may go 18 to 19 with the new capture; those two are not frozen.

5. Header entry counts for S060–S066. Stay S060=1, S061=0, S062=0, S063=1, S064=1, S065=0, S066=0, and the header file for each mined id stays the file named above. Guard, per id: `grep -rlE '^source: S0NN\b' corpus/knowledge`. The claim's new entry cites S067 only. A second `source:` line for S060, S063, or S064 in that new file fails this guard. Prose mentions (S060 inside `cve-json-record-format.md`, staged-S068 prose) are not this counter.

6. The existing 61 knowledge files. The count goes 61 to 62 by addition of one file, not by replacement. Guard: `python3 corpus/instruments/recheck-audit.py --quiet` prints `missing=0 unexpected=0` against an expected list that is today's 61 names plus that one new file (`expected=62`). A deleted or renamed pre-existing file prints `missing=`. `fail-closed=24` and `gated=24` are today's reading; the claim does not freeze them, so they are not this guard. `strict pass` should become 62/62 only if the new line is strict-clean; that is a change, not an identity.

7. `source-recheck.py` stays the checker the frontier and the knowledge lines call. Stay: tracked path present, `python3 corpus/instruments/source-recheck.py --help` exit 0, no-argument exit 2 with `manifest UNAVAILABLE reason=missing-required-argument`. Guard: those two exits, plus `git diff --diff-filter=D --name-only <base> <Y> -- corpus/instruments/source-recheck.py` empty.

8. No tracked deletion under `corpus/`. Guard: `git diff --diff-filter=D --name-only ab98fac9dce87130bc4f66de89e30650d63943dc <Y> -- corpus` prints nothing. This is the claim's kill rule "a tracked deletion in corpus/". Addition of the gate, the exemplar, the nine defect fixtures, the knowledge file, and the registry rows is the move; deletion is not.

9. `.ufo/` tracked set does not shrink. Byte identity will not hold at Y: the judged-head rule says Y adds `.ufo/waves/round-43/final-gates/all-gates.txt`, and J carries the round's other files. Guard is no deletion, not equal bytes: `git diff --diff-filter=D --name-only ab98fac9dce87130bc4f66de89e30650d63943dc <Y> -- .ufo` prints nothing. Baseline to compare against is the HEAD row above (8451 files, 139644593 bytes, of which `.ufo/` is 8124 files and 132012188 bytes).

Not frozen, so not given an identity guard: tier counts (a new row has a tier), `with_fetched_utc` / `with_archival` (they follow how the new capture is recorded), `multi_row_url=3` (a new row that repeats an existing URL would move it; the claim does not forbid that), and `fail-closed`.

## Confidence and gaps

High on every number above: each one is the stdout of the command in this file, run at the named commits. Not measured: the bytes of the not-yet-written S067 row, which reject id C2 will pick, and whether that new knowledge file's `source:` line cites anything besides S067. Those are the after-state, and the guards above are how to see them miss.
