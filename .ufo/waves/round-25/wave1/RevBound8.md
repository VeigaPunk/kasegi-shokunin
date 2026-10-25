# RevBound8 — D24-3: what was actually measured about the bound-64→8 brace mutant

Seat: reviewer (read-only on the lane). Round 25, wave 1. Lane base
`b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. Every number below was run by me on
2026-10-25 against the bytes named, from the lane root; nothing is copied from the
lane's own prose unless marked *evidence-verified*.

**Verdict in one line:** the figure `8/8` is **true** but was **never measured on the
landed bytes** in round 24 — the only round-24 mutant receipt scores the *baseline*
and returns **4/8**; the seat that would have scored the landed bytes never spawned.
I re-measured it now on the landed bytes: **8/8 and 24/24**, so the sentence can be
made true by fixing its provenance, not its number.

---

## 1. The evidence chain, as it exists

1. `.ufo/waves/round-24/c1-control-baseline.txt` — `cases=8 pass=4 exit=1`,
   `sha256 resolver=690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d`
   (the round-23 baseline bytes).
2. `.ufo/waves/round-24/c1-fixed.txt` — `cases=8 pass=8 exit=0`,
   `sha256 resolver=db5e0767c60ce00ea6c9cfb4ddd3e159e9a86525e5c8417c4a0a73e2e6d45667`
   (the landed bytes; `sha256sum corpus/instruments/resolve.py` today = same hash).
   Both receipts carry `matrix=fef0f02d…` and `checker=acbb6870…`: one detector on
   both sides.
3. `.ufo/waves/round-24/wave1/ResolverAttack.md:151` (M4 `mut-m4-bound8.py`, mutant
   sha `25c5584e…`) — the **only** bound-8 receipt in the round. Its header states the
   resolver under attack is `.ufo/waves/round-24/c1-baseline-resolver.py` sha
   `690153ad…`. Row 151: counter-B **`4/8, identical receipt`**, round-23 containment
   **`24/24`**, probe delta `many10/{a01…a09,zzz}/f.md`: `INTERNAL` → **`GONE`**.
   So the one measured bound-8 mutant was scored **on the baseline base, and it scored
   the baseline's own 4/8**.
4. `.ufo/waves/round-24/wave2-spec.json` `items[3]` = `T4MatrixMutants`
   (mutation-tester, "Mutate the landed `…/resolve.py` in /tmp copies and score each
   mutant on BOTH matrices… (a) `brace_expand` bound 64→8") — the seat that would have
   produced the landed-base receipt. It **never ran**: `.ufo/waves/round-24/wave2/`
   contains only `swarm-registry.json` (35 members, `agentId: null` for all, 0 seat
   reports) and `wave2-refusal-{1,2,3,4}.json` each record
   `"host_error": "Background job limit reached (100)"`, `"spawned": 0`.
5. **No committed file records any mutant of `db5e0767…`.** `grep -rn db5e0767` over
   `.ufo/waves/round-24/wave1/*.md` → **0 hits**. The only lane files naming
   `db5e0767` are `c1-fixed.{txt,json}` and `c1-containment-regression.{txt,json}`, and
   all three score the **real** bytes, not a mutant.
6. Structural reason the `8/8` is true by construction: I enumerated every brace group
   in both fixture files. Dispatch max **4** alternatives
   (`{validate,registry-check,reroute-drill,check-freshness}`); containment max **2**
   real alternatives (`{ops,missing}`, `{../outside.md,missing.md}`). A bound of 8
   never binds on either matrix, so a bound-8 mutant cannot lose a case.

**Conclusion for (a) of the acceptance:** at round-24 write time the `8/8` was an
**inference** from "no case exceeds four alternatives", carried into four documents as
if it were a receipt; the receipt that exists says `4/8` on a different byte base.

---

## 2. Acceptance (a) — artefact | claim | measured or inferred

| # | artefact (current worktree) | claim as written | measured or inferred |
|---|---|---|---|
| 1 | `.ufo/waves/round-24/c1-control-baseline.txt` | baseline `690153ad…`: `cases=8 pass=4 exit=1` | **MEASURED** — re-ran today, `4/8 exit=1`, same `matrix=fef0f02d…`, same `checker=acbb6870…` |
| 2 | `.ufo/waves/round-24/c1-fixed.txt` | landed `db5e0767…`: `cases=8 pass=8 exit=0` | **MEASURED** — re-ran today, `8/8 exit=0`, `resolver_sha256=db5e0767…` |
| 3 | `.ufo/waves/round-24/c1-containment-regression.txt` | landed `db5e0767…`: `cases=24 pass=24 fail=0` | **MEASURED** — re-ran today, `24/24 exit=0`, `matrix_sha256=d05b1e0c…` |
| 4 | `.ufo/waves/round-24/wave1/ResolverAttack.md:151` (M4, mutant `25c5584e…`) | bound 64→8: counter-B `4/8, identical receipt`; containment `24/24`; `many10` INTERNAL→GONE | **MEASURED — on the BASELINE base `690153ad…`, not on the landed bytes.** The only bound-8 receipt the round owns |
| 5 | `.ufo/waves/round-24/wave2-spec.json` `items[3]` (`T4MatrixMutants`, mutant (a)) | "score each mutant on BOTH matrices" against the **landed** `resolve.py` | **NOT RUN** — 4 dispatch refusals, `spawned: 0`, registry `agentId: null`, `wave2/` holds 0 seat reports |
| 6 | any committed lane file | a mutant of `db5e0767…` scoring `8/8` | **ABSENT** — 0 hits for `db5e0767` in `wave1/*.md`; the three `db5e0767` receipts score the real bytes |
| 7 | `corpus/instruments/README.md:159-160` (round-24 text, now superseded by a concurrent sibling edit) | "a mutant that lowers … bound to 8 scores `8/8` here and `24/24` … while flipping real verdicts" | **INFERRED** at write time |
| 8 | `SCORECARD.md:499-501` | "scores `8/8` on the dispatch matrix and `24/24` … while flipping real verdicts (`ResolverAttack` receipt, wave 1)" | **INFERRED**, and **misattributed**: the cited receipt says `4/8` |
| 9 | `corpus/QUALITY.md:65` (R11 grounded-in cell) | "bound-64→8 **8/8 and 24/24 unchanged**" | **INFERRED**; "unchanged" is true only of containment (baseline is 24/24); dispatch baseline is 4/8, so 8/8 is not "unchanged" |
| 10 | `corpus/lessons/round-24.md:186` (M24-4 evidence) | "scores **8/8** on the dispatch matrix and **24/24** on the containment matrix while flipping real verdicts" | **INFERRED** |
| 11 | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-24/kasegi.md:159` and `:227` | "bound-64→8 brace mutant scores 8/8 and 24/24 (R11)" | **INFERRED** (fleet-repo historical report) |
| 12 | **this report, §3** (new, round 25) | mutant `88122e10…` = landed bytes with `64`→`8`: dispatch `8/8 exit=0`, containment `24/24 exit=0`, `many10` INTERNAL→GONE | **MEASURED NOW** (commands and digests in §3) |
| 13 | `corpus/instruments/resolve-dispatch-fixtures.json`, `mirror-containment-fixtures.json` | "no case has more than four brace alternatives" | **MEASURED** — max alternatives dispatch **4**, containment **2** |
| 14 | `README.md:157`, `SCORECARD.md:503`, `QUALITY.md:65` | degenerate `always-INTERNAL` scores `0/8` | **MISLABELLED** — the measured artefact `LivenessMatrix.md:103,107,201` names it `always-RESOLVES` `0/8`. Not D24-3, but in the same sentences (see §6) |
| 15 | lane corpus / `SKILL.md` | (unstated) reach of the bound in real citations | **MEASURED** — the largest real brace group in the lane is **7** alternatives (`SKILL.md:993`, `corpus/knowledge/source-tree-loss-2026-09-28.md:118`), so a bound of 8 truncates **no** real lane citation; the flip is latent, not live |

---

## 3. Acceptance (b) — the fresh measurement

Scratch only, no lane write: `/tmp/kasegi-r25-bound8/`. Mutant = a copy of the landed
`corpus/instruments/resolve.py` (sha `db5e0767…`, confirmed by `sha256sum` today) with
exactly two tokens changed at `resolve.py:182` and `:184`:

```
<         if len(out) > 64:            >         if len(out) > 8:
<     return sorted(out)[:64]          >     return sorted(out)[:8]
```

Mutant sha256 `88122e10e94cb74eefcd39841061ca128317bb7d0a81733f1cdb7d51c2234285`.

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ python3 corpus/instruments/resolve-dispatch-check.py --resolver corpus/instruments/resolve.py --json /tmp/kasegi-r25-bound8/dispatch-landed.json
cases=8 pass=8 exit=0
sha256 resolver=db5e0767c60ce00ea6c9cfb4ddd3e159e9a86525e5c8417c4a0a73e2e6d45667 matrix=fef0f02d6d64cfb68702d245ecd156b6bb7eea95115c2a94216a10f8f9414c8c checker=acbb687094f0fedb3517c744f0bcda68a4edd96ec760087e667fc70c6a0569e1

$ python3 corpus/instruments/resolve-dispatch-check.py --resolver /tmp/kasegi-r25-bound8/mut-bound8.py --json /tmp/kasegi-r25-bound8/dispatch-mut8.json
cases=8 pass=8 exit=0
sha256 resolver=88122e10e94cb74eefcd39841061ca128317bb7d0a81733f1cdb7d51c2234285 matrix=fef0f02d6d64cfb68702d245ecd156b6bb7eea95115c2a94216a10f8f9414c8c checker=acbb687094f0fedb3517c744f0bcda68a4edd96ec760087e667fc70c6a0569e1

$ python3 corpus/instruments/mirror-containment-check.py --resolver corpus/instruments/resolve.py --json /tmp/kasegi-r25-bound8/contain-landed.json
cases=24 escape=12 controls=12 pass=24 fail=0 resolver_sha256=db5e0767… matrix_sha256=d05b1e0cf62738ac8bf06497334c16a392089a5792ca9fd930f0cbf73e69b809

$ python3 corpus/instruments/mirror-containment-check.py --resolver /tmp/kasegi-r25-bound8/mut-bound8.py --json /tmp/kasegi-r25-bound8/contain-mut8.json
cases=24 escape=12 controls=12 pass=24 fail=0 resolver_sha256=88122e10… matrix_sha256=d05b1e0cf62738ac8bf06497334c16a392089a5792ca9fd930f0cbf73e69b809
```

Verdict flip, by importing `classify()` from each copy against an isolated fixture
(`/tmp/kasegi-r25-bound8/lane`, `MIRROR_ROOT` set to an absent dir; 10-alternative and
65-alternative citations whose only on-disk member is the last alternative):

```
landed(dB5e)       many10(10 alts)  -> INTERNAL method=brace      path=…/lane/many10/zzz/f.md
landed(dB5e)       many65(65 alts)  -> GONE     method=
mut8(88122e)       many10(10 alts)  -> GONE     method=
mut8(88122e)       many65(65 alts)  -> GONE     method=
baseline(690153)   many10(10 alts)  -> INTERNAL method=brace      path=…/lane/many10/zzz/f.md
baseline(690153)   many65(65 alts)  -> GONE     method=
```

So on the landed bytes the mutant **flips a real behaviour** (`many10` INTERNAL→GONE)
and **passes both matrices unchanged** — the coverage finding is real, and it is now
measured rather than argued. The `many65` GONE is a **pre-existing** bound defect on
the landed bytes that round 24 did not introduce and did not fix.

Reproduce the whole thing deterministically from committed bytes: copy
`corpus/instruments/resolve.py`, apply the two-token diff above, run the two commands
with `--resolver`. No fixture, matrix or checker change is involved (`matrix` and
`checker` digests are identical across all four runs).

---

## 4. Acceptance (b) — the corrected sentence (29 words)

> Bound-64→8: baseline bytes `690153ad…` 4/8, identical receipt, 24/24; landed
> `db5e0767…` re-measured (round 25, mutant `88122e10…`) 8/8 and 24/24, flipping a
> 10-alternative citation INTERNAL→GONE. No lane citation exceeds 7 alternatives.

It is true at every site listed in §5, survives `anchorcheck`-style checking (both
resolver hashes are real and named above), and drops the two false load-bearing bits:
that `8/8` was a round-24 receipt, and that `ResolverAttack` supports it.

If a shorter form is needed for a table cell:

> bound-64→8: 4/8 on baseline `690153ad…` (measured, `ResolverAttack.md:151`); 8/8 and
> 24/24 on landed `db5e0767…` (round-25 re-measurement, mutant `88122e10…`).

---

## 5. Acceptance (c) — exact places to change, and what stays

Line numbers are the **current worktree** at lane base `b49948f` plus round-25 wave-1
edits already on disk. Re-grep the anchor phrase before editing: a sibling seat is
editing `corpus/instruments/README.md` right now (§6.1).

### Change (lane-owned, round-25 work)

| # | file:line | current text (anchor) | change |
|---|---|---|---|
| 1 | `SCORECARD.md:499-501` | "64-combination bound to 8 scores `8/8` on the dispatch matrix and `24/24` on the containment matrix while flipping real verdicts (`ResolverAttack` receipt, wave 1)" | replace with the §4 sentence. The `(`ResolverAttack` receipt, wave 1)` attribution **must go**: that receipt says `4/8`. Keep `SCORECARD.md:498` ("Known blind spot (R11, published not hidden)") and `:502-503` |
| 2 | `corpus/QUALITY.md:65` (R11, `grounded in` cell) | "bound-64→8 **8/8 and 24/24 unchanged**" | replace with the §4 sentence. The criterion column ("A matrix that a bound-8 brace mutant passes identically to the real fix proves the matrix does not exercise that bound") is **correct as written** and stays |
| 3 | `corpus/lessons/round-24.md:186` (M24-4 evidence) | "scores **8/8** on the dispatch matrix and **24/24** on the containment matrix while flipping real verdicts" | replace with the §4 sentence; `:188` "Captured-by: **R10** … **Fix: R11**" stays |
| 4 | `corpus/instruments/README.md:158-164` | sibling's live text: "…that mutant scores 4/8 with an identical receipt and 24/24 on the round-23 containment matrix (`ResolverAttack.md:151`); no lane file records it against the landed `db5e0767…` bytes, so 8/8 there is an inference, not a receipt." | **Now stale in one clause only**: a measurement of the landed bytes exists (this report, §3). Replace the final clause with the §4 sentence's landed half, or keep the clause and cite `.ufo/waves/round-25/wave1/RevBound8.md §3` as the receipt. Do **not** revert the rest of the sibling's rewrite — it is correct |

Optional, so the lane owns a durable receipt rather than a `/tmp` run cited by a
report: commit the two-token mutant (or just its sha `88122e10…` plus the diff) and a
`--json` receipt under `.ufo/waves/round-25/`, then point `README.md` at it. The
deterministic reproduction in §3 makes this a nice-to-have, not a requirement.

### Stays — historical, do not edit

| file | why |
|---|---|
| `.ufo/waves/round-24/c1-control-baseline.txt`, `c1-fixed.txt`, `c1-containment-regression.{txt,json}` | receipts of record; all three reproduce byte-for-byte today (§3) |
| `.ufo/waves/round-24/wave1/ResolverAttack.md:151` | the round-24 wave-1 receipt; it is the **correct** evidence for the `4/8` half and the source of D24-3. Correcting it would destroy the only honest measurement |
| `.ufo/waves/round-24/wave2-spec.json` `items[3]`, `wave2-refusal-{1..4}.json`, `wave2/swarm-registry.json` | the record that the landed-base seat never spawned; load-bearing for this finding |
| `corpus/lessons/round-24-verifier-spotcheck.md:178,206` | round-24 verifier spot-check — operator-protected, and its D24-3 text is accurate |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-24/kasegi.md:159,227` | round-24 report as filed, in the fleet repo (outside lane write scope). The correction belongs in the round-25 lesson/report, not by rewriting a filed report |

---

## 6. Secondary findings in the same sentences (L1's call, not D24-3)

### 6.1 `corpus/instruments/README.md` is being edited concurrently

`git status --porcelain` shows `M corpus/instruments/README.md` and the R11 paragraph
now reads differently from base (it already says "baseline … 4/8 … inference, not a
receipt"). A sibling seat owns that edit. Whoever lands §5 row 4 must coordinate with
that seat; my §5 wording is written to merge into the sibling's text rather than
replace it.

### 6.2 `always-INTERNAL 0/8` is the wrong name for the measured degenerate

`README.md:157`, `SCORECARD.md:503` and `QUALITY.md:65` call the second degenerate
`always-INTERNAL`; the artefact that measured it — `.ufo/waves/round-24/wave1/LivenessMatrix.md:103,107,201`
— says `always-RESOLVES 0/8` ("fails C2 with `gone-with-path`"). An always-INTERNAL
resolver would fail only C2/C4 and could not score 0/8. If L1 is editing these exact
lines for D24-3, fix the name in the same pass; it is a one-word change per site with
the measurement already on disk.

### 6.3 `QUALITY.md:65` "unchanged" is directionally wrong for dispatch

The word "unchanged" is defensible only for containment (24/24 before and after). On
dispatch the baseline is 4/8, so a bound-8 mutant scoring 8/8 *improves*; the claim
that matters is "indistinguishable from the real fix", which §4's sentence states
without the false symmetry.

---

## 7. Residual risk and what this does not establish

- **Not established:** that the round-24 *fix* introduced the bound defect. It did not
  — `many65` is GONE on the baseline too (§3), so the bound is inherited. The round-24
  sentence's implicit "the matrix cannot see a defect the fix left behind" is true; a
  reading of "the fix has a bound bug" would also be true and is **not** what was
  written.
- **Not established:** that the bound matters for the lane's own numbers. The largest
  real brace group is 7 alternatives (§2 row 15), so a bound of 8 changes no lane
  citation's class today; the matrix blindness is a **latent** instrument gap, which is
  exactly what R11 is for.
- **My measurement is a `/tmp` run reported here, not a committed receipt.** It is
  reproducible from committed bytes by a two-token diff (§3) and the checker digests
  are unchanged, so the risk is bookkeeping, not truth. §5's optional step removes it.
- **Not run:** `T4MatrixMutants`' other five mutants ((b)–(f)). They are out of D24-3
  scope and remain unmeasured for the landed bytes; if the lane wants them, the wave-2
  spec text is intact and now demonstrably runnable from a `/tmp` copy.
- **Tooling:** nothing installed or upgraded this seat (Python 3.14 stdlib only,
  `git`/`sha256sum`/`sed`). No pacman transaction attempted (host-wide pause honoured).
- **Lane writes:** none. The only file I created is this report; all scratch lives in
  `/tmp/kasegi-r25-bound8/`. `git status` deltas other than this report belong to other
  seats.
