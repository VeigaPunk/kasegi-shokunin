# DRAFT — corpus/lessons/round-76.md skeleton (ScribeLedger, not applied)
# Placement: NEW file corpus/lessons/round-76.md (no round-76 lesson exists at base; round-75.md is the last round file and is not edited). Every <FILL> is measured or decided at integration; M76-<FILL> rows are candidates until the wave's findings are captured. This header is not part of the text.
==========

# Round 76 — lesson (kasegi, attempt 1)

Round: kasegi r76, attempt 1. Frozen claims `.ufo/waves/round-76/claims.json` (freeze `5da54cd4451cbbb9e4b87e2f83475feb13c65c9e`; base `a788021675873a96e09e91aa033d8c26ac2fe212`; controls committed at the freeze). Wave `w1` (13 seats); receipts in `.ufo/waves/round-76/w1/`.

Claims: C1 (`depth:verifiability`, the recheck-cwd census counter `corpus/instruments/recheck-cwd-census.py`: a forged-relabel kill for neither-header files, a load-bearing case-6 RESULT limb, and a both-headers fixture classed as a normal entry; nominal score 4, per QUALITY R58) and C2 (`coverage`, frontier F54 on S111, the OSV.dev API overview; score held at 8, denominator operator-owned).

## Gate

Candidates considered this round:

- **S111 — the OSV.dev API overview `https://google.github.io/osv.dev/api/` — ADMITTED as F54 pending integration and the Q01 manifest repair** (one knowledge entry, `corpus/knowledge/osv-api-surface-and-limits.md`). Capture `corpus/source-snapshots/round-76/S111.txt`, sha256 `6f92e5b7…5581ab`, 48 lines, 1810 bytes; manifest `corpus/source-snapshots/round-76/manifest.json`, 13 quotes committed, anchors at capture lines 21-39. Located clauses: lines 21-36 (manifest Q01-Q11: API 1.0, OpenAPI download, six request types with three experimental, the rate-limit question and the no-limits answer). Lines 38-39 (Q12-Q13) are held ground from S108 and are cross-referenced only. Blocker, measured by the scribe: Q01 (`API (1.0)`, line 21) is 9 characters and fails the 12-character floor (`source-recheck.py` line 33; `--source S111` rc 2), so claim B5 is not met by the committed bytes; the quote count and the repair are an L1 or operator decision. The lead bullet at `corpus/SOURCES.md` line 175 is retired at integration.
- **Reject slot — <FILL: candidate name, the rule it fails, and where it is recorded>.**
- **Spot-check slot — <FILL: the non-author admit/reject check on the landed F54 entry, its verdict and its evidence path>.**

Admitted: S111 / F54 pending integration. Rejected or held: <FILL: the reject-slot candidates>.

## Mistakes

| id | class | evidence pointer | captured-by | fix | able to fail |
|---|---|---|---|---|---|
| M76-<FILL> | <FILL: from the wave's findings> | <FILL> | <FILL> | <FILL> | <FILL> |
| M76-<FILL> (candidate, scribe-found) | the drafting assignment for the knowledge-expected line said "append", while claim B2 requires `knowledge-expected.txt` to be `LC_ALL=C sort -c` clean; the row `corpus/knowledge/osv-api-surface-and-limits.md` sorts between `osv-affected-range-events.md` (line 67) and `osv-post-v1-query-contract.md` (line 68), so an end-of-file append breaks B2 | `.ufo/waves/round-76/w1/knowledge-expected-line-draft.md`; `.ufo/waves/round-76/w1/ScribeLedger-checks-r76.txt` T4 (append, rc 1) and T5 (insert, rc 0) | none yet | the draft specifies an insert at line 68; the L1 measures `LC_ALL=C sort -c` on the landed file | <FILL: yes if the landed file was appended and `sort -c` exits nonzero; the scribe's scratch simulation (T4) shows the failure> |
| M76-<FILL> (candidate, scribe-found) | the capture renders two endpoint names with an interior space (`POST /v1experimental/ determineversion`, S111.txt lines 8 and 46), while the frozen claim statement writes `POST /v1experimental/determineversion`; a row or entry that copies the claim's spelling would name a path the capture does not show | `corpus/source-snapshots/round-76/S111.txt` lines 8, 46; `.ufo/waves/round-76/claims.json` C2 statement | none yet | the entry quotes the path as its capture renders it, or cites line 32 for the endpoint's purpose, and states the interior space as a capture artefact; the per-endpoint contract is not claimed in round 76 | <FILL: yes, if the landed entry names the unspaced path without a note> |
| M76-<FILL> (candidate, scribe-found) | a frozen C2 clause (B5) names `source-recheck.py` as the check for "13 quotes anchor-located, exit 0", and the committed S111 manifest pins a quote (Q01, `API (1.0)`, 9 characters) that the same command rejects under its own 12-character floor; the same class as M75-2, a frozen clause whose named command cannot pass on the committed bytes | `corpus/source-snapshots/round-76/manifest.json` Q01; `corpus/instruments/source-recheck.py` line 33; `.ufo/waves/round-76/w1/ScribeLedger-checks-r76.txt` (source-recheck rc 2); `.ufo/waves/round-76/w1/ScribeEntry.md` § BLOCKER | none yet | the L1 or operator decides the repair before any seat scores (routed defect in § Routed defects) | yes: measured rc 2 on the committed bytes |

## Routed defects (not closed by round 76)

- **R76-<FILL> (C1 residual):** <FILL: any letter or mutant class the amended selftest does not kill, with its evidence path>.
- **R76-<FILL> (C2 residual):** <FILL: any clause or distinctness point the entry does not settle>.
- **R76-<FILL> (C2 B5 blocker, measured by ScribeLedger):** the committed S111 manifest's Q01 fails `MIN_QUOTE_CHARS = 12`; `source-recheck.py --manifest corpus/source-snapshots/round-76/manifest.json --source S111` exits 2 (`S111:Q01-api-version UNAVAILABLE reason=quote-too-short-to-be-evidence`), so the frozen B5 clause "13 quotes anchor-located, exit 0" is not met by the committed bytes. The version string `1.0` occurs on one capture line only (`grep -n '1\.0' S111.txt` → line 21), so no other located line keeps 13 quotes with a version ground of 12 characters or more. Options for the L1 or operator: (a) drop Q01 and record 12 quotes, which makes B5's "13" wording false as written; (b) keep 13 by re-pinning Q01 with a longer line-21 quote, which the capture does not allow; (c) an operator amendment of B5 before any seat scores. No predicate is rewritten here.
- **R76-<FILL> (operator, RC-8):** the census keeps exactly one `bash -c` call site (in `run_foreign`); RC-8 remains a pending operator decision and the exec surface is not expanded this round.

## Counters

| counter | before (base `a788021`, controls `5da54cd`) | after (landed tree) | command |
|---|---|---|---|
| recheck-cwd census selftest | `selftest cases=6 failures=0`, exit 0 | <FILL: `cases=8 failures=0`, exit <FILL>> | `TMPDIR=<scratch> python3 -B corpus/instruments/recheck-cwd-census.py --selftest` |
| census on the real tree | `RECHECK-CWD entries=91 noprefix=0 exit2_foreign=0 exit0_foreign=69 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0`, conformant, exit 0 | <FILL: byte-identical to base (A4); after C2 the entries/exit0 drift is entries=92 exit0_foreign=70 at the landed tree> | `python3 -B corpus/instruments/recheck-cwd-census.py --root <lane> --lane <lane>` from `/tmp` |
| registry rows | 110 | <FILL: 111> | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` |
| knowledge entries | 91 | <FILL: 92> | `ls corpus/knowledge/*.md \| wc -l` |
| frontier admitted | 53 (F01–F53); `FRONTIER-CENSUS rows=53 admitted=53 closed=53 problem-rows=0 registry=110`; `entries=56 pass=56` | <FILL: 54 (F01–F54); `entries=57 pass=57`> | `python3 corpus/instruments/frontier-recheck-count.py` |
| knowledge-expected | 93 lines / 91 rows, `LC_ALL=C sort -c` exit 0 | <FILL: 94 lines / 92 rows, exit 0> | `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt` |
| capture records | `records=89 bound=89 unbound=0`, exit 0 | <FILL: records=90 bound=90 unbound=0, exit 0> | `python3 corpus/instruments/capture-binding-check.py` |

## Counting commands

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
TMPDIR=/fast/scratch/hyaku/kasegi-r76/<L1>/tmp python3 -B corpus/instruments/recheck-cwd-census.py --selftest
cd /tmp && python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/recheck-cwd-census.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin
cd /tmp && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py --manifest /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-76/manifest.json --source S111
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-binding-check.py && python3 corpus/instruments/frontier-recheck-count.py
LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```
