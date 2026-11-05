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
`b4afd8a0` measured from a shared clone (`controls/c2-after-counters-r70-clone.txt`,
`controls/census-after-r70.txt`). The frozen pin set keeps the pre-freeze working-tree receipt
(`controls/c2-after-counters-r70.txt`, sha256 `f20fd6e7…`) byte-identical; the clone re-measurement
is a separate file with the same values (see M70-5).

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
- **M70-5 — a frozen receipt was overwritten after the freeze.** `controls/c2-after-counters-r70.txt`
  was pinned at `e74ba6b5` (sha256 `f20fd6e7…`, the pre-freeze working-tree measurement) and then
  re-written with the shared-clone re-measurement before the evidence commit, so the pinned hash and
  the committed file disagreed (found by `ExecCountersC2` at the wave). The frozen bytes were
  restored from `15d4da87` and the clone measurement landed as its own file
  (`controls/c2-after-counters-r70-clone.txt`, sha256 `636b462d…`); the values are identical (diff is
  the header line and one added `malformed_rows` line). Class: evidence-integrity. Captured-by:
  `pins-r70.txt` (the pin itself was the detector, once a seat re-hashed the file). Fix: **R107**.
- **M70-6 — the new selftest cases are not single-limb isolated.** `ExecR103` measured the 10 new
  cases against one-limb mutants: 2/3/7/8/9 have exclusive killers, case 1 is a group limb, cases 4/5
  are group-only because every `--out` case also carries `--url`, case 6 (`--ou`) is pinned by the
  conjunction of the prefix rule and the `--url` denial, and case 10 pins `--` together with the
  `git show` operand rule. Three rule limbs (`--url` alone, `-o`, `--scratch`/`--work`) have no
  dedicated case at all. R103 is therefore only partly met by this round's cases. The claim's
  behaviour is unaffected (the refusals are redundant), but the *pin* is weaker than R103 asks.
  Routed as **V70-1** to the next gate change; not repaired this round because the selftest bytes are
  part of C1's frozen measured implementation (gate sha256 `7a8d52eb…`) and a post-measurement edit
  would invalidate the claim rather than strengthen it.
- **M70-7 — the entry's prose outran its own source.** `CriticC2` listed 21 outruns (O1–O21) in the
  F48 entry: the page never states a three-class count (it has three sub-headings under "several
  varieties"), the fix-version sentence's subject is "malware alerts", the CVSS maintainer rule is for
  GitHub-obtained CVEs (not imports), "always fully synchronized" was misquoted, and the community
  edit's author cell named the reviewing team instead of the submitter. Corrected in place with the
  README/SOURCES/manifest wording aligned; the correction is recorded as
  `controls/pins-r70-erratum-1.txt` with the old→new entry hash (`d479c495…` → `0775d2a4…`) and the
  re-measured C2 values (unchanged: the predicate counts rows, entries, records and files).
  Captured-by: `none` before the wave → **R108**. Fix: mark every generalization as the entry's
  reading or drop it, and apply a critic seat's outrun list before the round closes.
- **M70-8 — a pinned control receipt was captured mid-write.** The base/candidate/forgery control
  chain ran as one background job; the controls commit `15d4da87` and the freeze `e74ba6b5` were made
  while it was still writing `controls/c1-forgery-blanket-r70.txt`, so both commits carry a 10-line
  truncated blob (`fdbcc484…`) that lacks the `VERIFY … mode=forgery` line, while the pins line
  (`d74ba3f9…`) describes the completed 14-line file that only lands at `7f6e39a9`. Found by the
  wave's `ScribeRound` seat. The completed receipt now matches its pin byte-for-byte and the control
  was re-run to `controls/c1-forgery-blanket-r70-rerun.txt` (exit 1, `failures=4`, `diff` empty).
  Captured-by: `none` before the wave (the pin only detects a change if someone re-hashes it) →
  **R109**. Fix: never commit or pin while a background writer is still producing the receipts; wait
  for the writer's exit, then hash.

## Corrections (post-freeze, append-only)

- **F48 entry and its three summaries** — see M70-7 and `controls/pins-r70-erratum-1.txt`. The frozen
  pins file is untouched; the corrected entry hash and the re-run receipts live in the erratum.
- **Forgery control receipt** — see M70-8 and `controls/pins-r70-erratum-2.txt`. The freeze commit
  carried a mid-write truncated blob; the completed receipt matches its pin and the control re-runs to
  the same `failures=4` exit 1 (`controls/c1-forgery-blanket-r70-rerun.txt`).

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

## Routed defects (this round → next gate change)

- **V70-1 — selftest pin strength (R103).** `ExecR103` and `MutationC1` agree: cases 4/5 are group-only
  (`--out` cases also carry `--url`), case 6 is conjunction-pinned, case 10 pins `--` together with the
  `git show` operand rule, and four limbs have no dedicated case (`--url` alone, the short `-o`,
  `--scratch`, `--work`). `MutationC1` measured the missing cases that would kill each survivor and
  ranked them smallest-first (one `capture-source.py --ou` case without `--url`; a `-o`/`-oout.txt`
  case; `--scratch`/`--work`/`--url` cases; a `git show HEAD:g.txt -- HEAD:g.txt` case). Not applied
  after measurement: the selftest bytes are part of C1's frozen gate sha256 `7a8d52eb…`.
- **V70-2 — the short `-o` limb is implemented but unmeasured.** The claim's declared sentence includes
  a short `-o` refusal, but neither the frozen probe set (P1..P7) nor the selftest exercises it
  (`MutationC1` M5 survives the counter end to end). The claim is graded on its frozen predicate only;
  the `-o` behaviour is a code fact with no this-round receipt.
- **V70-3 — capability loss to state.** `SentinelGate` records that the gate can no longer derive a
  counter against a non-default root (`--root <fixture>`); every committed use invokes such counters
  directly rather than through the gate, so nothing breaks, but the loss is real and is recorded here
  rather than left implicit.

## Residuals (named, not claimed)

- `--fleet-root`, `--manifest`, `--ledger`, `--results` and every non-denied counter option remain
  admitted; a counter that writes on a positional path (`resolve.py <lane>`) remains open.
- Nested python: a counter that itself invokes `python3 corpus/instruments/... --root` is validated
  only at the first stage.
- `sort -T`/`TMPDIR` temp writes, environment variables, host-file reads, `git`/`python` head SIGPIPE
  masking, exit-0 partial-output producers and semantic emulators remain open from rounds 67–69.
- The score gap (`score-gap.py`) is not re-claimed this round; source restoration and the operator-owned
  R67/R69 decisions remain unanswered.
