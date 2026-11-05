# Round 70 — python-head write/exec/ingress option refusal (C1) and the GitHub Advisory Database curation semantics F48 (C2)

Round 70, attempt 1. Lane base `e7c02bddaa32a4a70afb2e6278f108e03dca067c` (round-69 verifier
spot-check tip). Two claims, both frozen in `.ufo/waves/round-70/claims.json` (freeze
`e74ba6b5d522b1e91dca3a2d244585d6b7babdc5`, pins `.ufo/waves/round-70/controls/pins-r70.txt`):

- **C1, depth:verifiability (lowest non-retired, 4, nominal per R58)** — the derive gate refuses the
  python head's measured write/exec/ingress long options by name and by any unique argparse
  abbreviation. Implementation `c1051749571caf6a0383b15187fc02cdd21785b5`, gate sha256
  `7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5`, selftest pin 86 → 96.
- **C2, coverage (8)** — frontier F48 on S105 (GitHub Advisory Database curation semantics) plus the
  rejected-row debt V69-1 landed as S104 (ENISA EUVD API documentation). Landing
  `b4afd8a0206b23a69d8cd65d92070cdfcd4680a7`.

## C1 — measured result

Counting command (frozen):

```
python3 -B .ufo/waves/round-70/controls/c1-probe-run-r70.py \
  --gate <gate exported from the measured revision> \
  --work /fast/scratch/hyaku/kasegi-r70/L1/FINAL --mode candidate
```

| limb | before (base gate `c09b0fb1…`) | after (`7a8d52eb…` at `c1051749`) |
|---|---|---|
| P1 `--root .` | admitted, recheck payload ran through `bash -c` (marker_runs=1) | rc=2 `derive-not-read-only`, marker_runs=0 |
| P2 `--root=.` | admitted, payload ran | refused |
| P3 `--ro .` (argparse abbreviation) | admitted, payload ran | refused |
| P4 `--out ABS` | admitted, wrote `outside/p4.txt` | refused, wrote=0 |
| P5 `--out=ABS` | admitted, wrote | refused |
| P6 `--ou ABS` | admitted, wrote | refused |
| P7 `--json ABS` | admitted, wrote the receipt and ran the payload | refused, wrote=0, marker_runs=0 |
| 8 read-only controls | 8/8 admitted and exact | 8/8 admitted and exact |
| selftest | 86/0 | 96/0 |
| mutbat | 5/5 | 5/5 |
| real ledger | 35/35 | 35/35 |
| write side effect | FAIL (marker_runs=4) | ok (0) |
| **VERIFY** | **measurements=12 failures=9 exit 1** | **measurements=12 failures=0 exit 0** |

Receipts: `controls/c1-base-donothing-r70.txt` (base, live lane root),
`controls/c1-base-donothing-r70-clone.txt` (base, shared clone — the paired closure),
`controls/final-verification-r70.txt` (candidate, shared clone at `c1051749`, exit 0),
`controls/c1-candidate-trial-r70.txt` (pre-freeze candidate trial, byte-identical gate),
`controls/c1-forgery-blanket-r70.txt` (blanket-refusal forgery rejected: controls 8/8 fail,
selftest 47 failures, exit 1).

**Scope, stated exactly.** The claim is the enumerated probe set P1..P7 on this host's PATH python3
3.14.8, `/usr/bin/sort` GNU coreutils 9.12 and git 2.56.0. The new rule is an enumerated option set,
not a sandbox: positional arguments (`resolve.py <lane-repo>`, `limb-mutation-check.py <path>`),
non-denied options (`--results`, `--manifest`, `--ledger`, `--fleet-root`), a counter's own writes on
a positional path, and the `--` operand boundary stay open. Options after a `--` separator are
operands by construction and remain admitted (`python3 corpus/instruments/ok.py -- --root` is a
positive control).

## C2 — measured result

```
frontier: FRONTIER-CENSUS rows=48 admitted=48 closed=48 problem-rows=0 registry=105 ; entries=51 pass=51 exit=0
capture:  records=84 bound=84 unbound=0
knowledge-expected: 88 lines / 86 entries, LC_ALL=C sort -c exit 0
knowledge files: 86 ; frontier rows: 48 ; registry rows: 105 ; malformed rows: 0
sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi -> exit 0 (six inherited W04 warnings)
```

Before (`controls/c2-base-counters-r70.txt`, base `e7c02bd`): rows=47, registry=103, entries=50,
records=83, expected 87/85, knowledge files 85. After is the committed landing
`b4afd8a0` measured from a shared clone (`controls/c2-after-counters-r70.txt`,
`controls/census-after-r70.txt`).

## Gate — the two rows written this round

| row | URL | access date | located quote (≤25 words) |
|---|---|---|---|
| S104 (rejected) | https://euvd.enisa.europa.eu/apidoc | 2026-11-05 (re-fetch; byte-identical to the round-69 receipt: 3062 bytes, sha256 `6fb32b61…a38d5`) | The static body contains no `endpoint` and no `/api/` occurrence (0 and 0), so no line-anchored capture exists — the rejection's ground is the absence, not a sentence. |
| S105 (mined, tier A) | https://docs.github.com/en/code-security/security-advisories/global-security-advisories/about-the-github-advisory-database | 2026-11-05T00:14:43Z (capture sha256 `9dd51a8e…e3350`, 656 lines) | "Unreviewed advisories are published automatically into the GitHub Advisory Database, directly from the National Vulnerability Database feed." (`S105.txt:601`, 18 words) |

Flip conditions recorded in the rows: S104 flips on a statically served or line-anchorable rendering
of the same API reference; S105's recheck is 180d.

## Mistakes

- **M70-1 — table edit replaced a row instead of inserting one.** The README frontier edit for F48
  was written as a whole-row replacement and deleted the F47 row; it was restored by the next edit
  and the committed diff shows F47 intact, but the intermediate working-tree state was a deleted row.
  Class: record-integrity, edit-shape. Evidence: `git -C … diff e7c02bd b4afd8a0 -- corpus/README.md`
  shows one insertion block and no deletion of F47; the intermediate state is the round's own
  transcript. Captured-by: `none` before this round → **R104**. Fix: count the table's rows
  (`grep -cE '^\| F[0-9]+ \|'`) after every table edit; the count must be before+1.
- **M70-2 — snapshot directory created before its manifest.** `corpus/source-snapshots/round-70/`
  existed with `S105.txt` and no `manifest.json` while the C2 base counters ran, so
  `capture-binding-check.py` printed `FAIL rule=missing-manifest dir=round-70` and the base receipt
  was polluted. The directory was moved to scratch, the base counters re-measured clean, and the
  capture landed with its manifest in one commit. Captured-by: capture-binding-check rule A (it did
  catch it). Fix: **R105**.
- **M70-3 — a `git archive` export is not a committed-input closure for this counter.** The first
  final run used a `git archive` export of `c1051749`; the ledger derives are `git show
  <rev>:<path>`, so `real-ledger` read `figures=35 ok=11 stale=24` and the run exited 1. Re-run on a
  `git clone --shared` checkout of the same revision: 12/0 exit 0. Both receipts are committed
  (`controls/final-verification-r70-archive-export-failed.txt`, `controls/final-verification-r70.txt`)
  and the claim is graded on the clone. Captured-by: R34/R65 ("complete transitive local input
  closure") — the rule existed, the round applied it late. Fix: **R106**.
- **M70-4 — a prose count drifted from the artifact.** The entry's recheck comment said 17 pinned
  quotes while the manifest carried 19; corrected before the landing commit, so the committed bytes
  agree. Captured-by: `source-recheck.py` line count (`S105:Q19-credit OK`). Fix: derive the count
  from the manifest, never type it.

## Disposition of the round-69 routed defects

- **V69-1 (EUVD rejected row owed)** — landed as S104 with a 2026-11-05 re-fetch that reproduces the
  round-69 digest; the C2 registry count includes it (`103 + 1 admitted + 1 rejected = 105`), which is
  the form R102 requires.
- **V69-2 (two unpinned `git show` limbs)** — pinned as `git-show-no-operand-refused` and
  `git-show-separator-refused`; the selftest pin moves 86 → 96.
- **V69-3 (class attack lost to a provider outage)** — this round dispatched six attack seats
  (two reviewers, two critics, a mutation-tester and a sentinel) against the same gate; their outcome
  is recorded in the round report and in `## Wave outcome` below.

## Assimilation

`Assimilation: none`. The staged package `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`
carries 94 ids of which **73 collide** with the lane's 103-row registry (`assimilation/collisions`),
i.e. mass id drift that a read-only check cannot repair; per the contract's drift rule nothing is
adopted and an L0 question is filed. The quarantine slice re-derived this round has 7 rows
(`assimilation/quarantine-slice`), five of them the register's unchecked "could not be fetched" family
and two `payload-absent`; with adoption closed they carry no verdict this round beyond that
classification.

## Trends

- **Expansion — improved.** F48 admitted on ground F47 explicitly left unopened, with a new mined A-tier
  row (S105, 19 located quotes) and a rejected row (S104) that closes a contract debt: registry
  103 → 105, knowledge 85 → 86, frontier 47 → 48, capture 83 → 84, census exit 0.
- **Quality — improved.** The measured gate refuses seven shapes the base gate executed or wrote on
  (`12/9` → `12/0`), the blanket-refusal forgery is rejected by the positive controls, the selftest
  pin rises 86 → 96 with the pin re-derived from bytes, and three round defects become R104–R106.
- **Discernment — improved.** The round's own three process misses (M70-1..M70-3) were found from
  committed receipts and converted into criteria rather than left standing; V69-1/V69-2 are closed and
  V69-3 is answered by a six-seat attack wave.

## Wave outcome

One v1 wave, 12 seats (band 8–16), attack share 6/12, one connector, one scout, one scribe; the L1
held the planner seat. Seat results, dead seats and their error text are recorded in the round report
from `.ufo/waves/round-70/w1-results.json`; the wave's findings are folded into this lesson's
residuals and into the report's verdicts.

## Residuals (named, not claimed)

- `--fleet-root`, `--manifest`, `--ledger`, `--results` and every non-denied counter option remain
  admitted; a counter that writes on a positional path (`resolve.py <lane>`) remains open.
- Nested python: a counter that itself invokes `python3 corpus/instruments/... --root` is validated
  only at the first stage.
- `sort -T`/`TMPDIR` temp writes, environment variables, host-file reads, `git`/`python` head SIGPIPE
  masking, exit-0 partial-output producers and semantic emulators remain open from rounds 67–69.
- The score gap (`score-gap.py`) is not re-claimed this round; source restoration and the operator-owned
  R67/R69 decisions remain unanswered.
