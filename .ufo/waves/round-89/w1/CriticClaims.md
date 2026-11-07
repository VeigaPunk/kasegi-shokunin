# CriticClaims — round 89 attempt 1: C1 and C2 falsified on their frozen predicates

Judged only on the frozen predicates in `.ufo/waves/round-89/claims.json`, at the landing
commits. Everything below is a routed defect or qualifier; nothing re-scores either claim.

## Verdicts

- **C1 — VERIFIED** at `eb5f0df8eaceca617465e493c710e8626e9aa618`. P1 `pass rc=0` (M1, M2,
  M3, M4, M9, M5, M7, M6; `base=777/1798 after=785/1797 target=785/1797 mirror_absent=True`);
  P2 15/15 pins equal at the landing; P3 `changed=1 outside=0 verdict=PASS`. The kill rule
  ("any of P1–P3 false") did not fire. Qualifiers C1-F1, C1-F2; wording notes C1-F3/C1-F4.
- **C2 — VERIFIED** at `c61c55868e6d28653f57413bac6a6de5a398d11f`. P1 `pass rc=0` (K1–K8) at
  seeds 8989 and 1; P2 scanner `95f24a54…` and allowlist `76245bba…` byte-equal, SCORECARD row
  byte-equal (`d3e840aa…`, last cell `87`); P3 `changed=3 outside=0 verdict=PASS`. The kill rule
  did not fire. Routed defects C2-F1, C2-F2, C2-F4; qualifiers C2-F3, C2-F5.

Both landing commits' parents are the previous commit (`eb5f0df ← 94573d2`, `c61c558 ← eb5f0df`),
and `claims.json` (`084b57a0…`) was committed in the freeze `94573d2` and is byte-identical at
`eb5f0df`, `c61c558`, `50e2632` and in the working tree: the predicates were frozen before either
landing.

## Environment / method

Lane clone `git clone --shared` in scratch, checked out at the landing; `python3 -B`; `TMPDIR`
inside the scratch root; no writes in the lane; no git writes outside the scratch clone; no
network. The counter/map/labels/candidate bytes were sha256-checked against `claims.json` before
use. `mirror_absent=True` in both counters, as the receipts claim.

## C1 — evidence

```
$ knowledge-meter.py --lane <scratch clone@eb5f0df8> --base-rev 090a46f89932324787e00ca20b1007f893934c9a \
    --after-rev eb5f0df8eaceca617465e493c710e8626e9aa618 \
    --map .ufo/waves/round-89/c1/repair-map.json --labels .ufo/waves/round-89/c1/labels.tsv \
    --target 785/1797 --map-sha256 c29f4c2186ed13495a9b03866f2412c6da5b95f7425b93f7dd1675a986d0e2ec \
    --labels-sha256 8aed5bded717a92df78943ea41332bd3a46b90858ec1396bc797eec85644050d --work <scratch>
KNOWLEDGE-METER base=777/1798 after=785/1797 target=785/1797 keys=9 mirror_absent=True
LIMB M1 pass … M2 pass … M3 pass … M4 pass … M9 pass … M5 pass … M7 pass … M6 pass
KNOWLEDGE-METER-RESULT pass rc=0
```

- P2: all 15 pinned paths at `eb5f0df8` equal their pins (`CriticClaims-receipts/c1-p2.txt`).
- P3: `git diff --name-only --no-renames 94573d2 eb5f0df` = `corpus/knowledge/triage-thresholds.md`
  only; `LANDING-SCOPE from=94573d25 to=eb5f0df8 changed=1 outside=0 verdict=PASS exit=0`.
- Do-nothing re-run: `after=777/1798`, M1/M2/M3 FAIL; the re-run block is byte-identical to
  `controls/c1-controls-r89.txt` lines 2–10 (`DONOTHING_BLOCK_SAME`).
- Prefix-only forgery re-run independently: `after=784/1796`; M9 unbound on the five WRONG keys;
  M1 FAIL. A cheap forgery does not meet the target (`c1-prefix-forgery.txt`).
- Semantic spot-checks, independent of the counter (the counter binds pairs, not meaning):
  all five re-anchor targets are the review's corrected lines and carry the claimed content —
  `claim-gates.md` L35 = the `decision_sha256` regex; L36–37 = the three-way
  `manifest.expected_head_sha256` binding; L78–80 = the not-claimable heuristics; L81–85 = the
  prior-submission guard plus the global duplicate scan; `claim-package-contract.md` L52–53 = the
  four hard gates. The two review-CORRECT sites (rows 223, 224) still cite
  `corpus/knowledge/claim-gates.md:35-36`; only row 225 moved to `:36-37`, so the global
  bare-token replace did **not** corrupt the correct sites. The four prefix targets are correct
  (L10–11 six required files; L15 the `provenance.json` row; L9–16 the six-file table; L17–25 the
  shared-constants table).
- Control provenance: `controls/c1-controls-r89.txt` at the freeze is byte-identical to the
  working-tree copy (`SAME`); the script clones **base**, applies the frozen map and commits in
  the clone, so the positive control's 785/1797 is a pre-landing result, not read back from the
  landing.

### C1-F1 — QUALIFIER: the clause "777/1798 at base" has no counter limb

**Counterexample.** M1 asserts only the *after* rate:
`limbs.append(("M1", (an, am) == (tn, tm), …))` (knowledge-meter.py). `bn, bm` are printed and then
unused, and `mirror_absent` is printed but never asserted. A run whose base reading drifts (a
resolve.py classification change, or the mirror becoming present so some GONE tokens earn a mirror
credit) while `after` still equals `785/1797` prints `KNOWLEDGE-METER-RESULT pass rc=0`.
**Evidence.** `CriticClaims-receipts/c1-p1.txt` (base printed, no base limb in the source above).
**Impacted axis.** depth:verifiability (the frozen number 777/1798 is evidence-by-observation only).
**Smallest correction.** Add `--base-target 777/1798` and
`limbs.append(("M1b", (bn, bm) == (tbn, tbm), …))`; optionally a `--require-mirror-absent` limb.

### C1-F2 — QUALIFIER: the R140 exclusion is sound, but it is load-bearing and must be recorded

**Assessment.** QUALITY R140 scopes itself to "a citation-repoint map whose keys were selected by a
lexical content proxy"; this map's nine keys were selected by the non-author review and all nine are
labelled (a census, not a sample), so R140's 15-key floor has no object — the criterion's purpose
(no unlabelled proxy-selected target) is met by full labelling. The exclusion is therefore sound as
written.
**Counterexample to any "R140 passes" reading.** R140's own checker cannot express this:
`python3 -B .ufo/waves/round-88/l1/r140-check.py --map .ufo/waves/round-89/c1/repair-map.json
--labels .ufo/waves/round-89/c1/labels.tsv` exits 2 (`R140 error reason=ValueError exit=2`) on the
four-column labels, and under R140's two-column vocabulary the same rows would report five `WRONG`.
**Impacted axis.** depth:verifiability (a future reader who assumes R140 was checked will mis-read
the closure).
**Smallest correction.** Repeat the exception in `corpus/lessons/round-89.md`/LOG at integration:
"R140 scoped out — 9/9 non-author census; r140-check.py cannot parse the four-column labels." No
change to the map or counter.

### C1-F3 — note (no defect): "5 re-anchors of the round-88 WRONG keys"

The r88 review labels six keys WRONG; the sixth (`japanese-domestic-disclosure-workflow.md`) has no
supported in-lane target and was already reverted at r88 integration (`corpus/knowledge/
japanese-domestic-disclosure-workflow.md:7` cites the upstream root, not a lane path). The claim's
parenthetical enumerates exactly the five re-anchored keys and the routed-defect disposition says
"restricted to the 9 keys a non-author named a supported target for", so the statement is exact as
written; only a reader dropping the parenthetical could read it as "all WRONG keys". Belt-and-braces
wording: "5 of the 6 WRONG keys".

### C1-F4 — note (no defect): the label class token `WRONG` is overloaded

`labels.tsv` class `WRONG` names the r88 pair's defect ("the r88 repoint was reverted; the review
names the correct line range"), and M9 enforces a *differing* value anchor for WRONG and an *equal*
anchor for FN. In R140's vocabulary the same token means "wrong target", so a reader who skips the
labels header sees "5 WRONG keys in a 9-key map". The header defines both classes; keep it.

## C2 — evidence

```
$ capability-check.py --lane . --rev c61c55868e6d28653f57413bac6a6de5a398d11f --work <scratch> \
    --instrument-sha256 95f24a541db8b3d6693315a03de28d0b6de0fb0b6e53a68471265382114d20ec \
    --gate-sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6 --seed 8989
CAPABILITY-CHECK rev=c61c5586… instrument_present=True seed=8989
LIMB K1 pass … K2 pass … K3 pass (scanned=1530,hits=0,allowed=20,unused_allow=0) … K4 pass …
LIMB K6 pass (base_hits=11, new_caught_by_base=none) … K7 pass … K8 pass (clauses=10) … K5 pass
CAPABILITY-CHECK-RESULT pass rc=0
```
Seed `1` reproduces every limb (`c2-p1.txt`). P2: scanner and allowlist shas equal; the
`## Capabilities` row at the landing is byte-equal to `c2/candidate/scorecard-row.txt`
(`d3e840aa…`, last cell `87`). P3: diff `eb5f0df → c61c558` = `SCORECARD.md`,
`corpus/instruments/capture-secret-scan.py`, `corpus/instruments/capture-secret-allow.tsv` exactly;
`LANDING-SCOPE … changed=3 outside=0 verdict=PASS`. The frozen C2 do-nothing control re-runs
byte-identically (`c2-donothing.txt`): K1, K4, K5, K7, K8 FAIL, K6 passes by construction.

### C2-F1 — DEFECT (counter): the `%26` half of the azure clause has no limb

**Counterexample.** Delete `|(?<=%26)` from `_LB` in a scratch clone, commit, run the counter
without pins: **`CAPABILITY-CHECK-RESULT pass rc=0`** (mutant `no26`, `c2-mutants.txt`). The landed
bytes *do* implement it: a probe with `…?a=1%26sig=<44 chars>&sv=2022-11-02` prints
`HIT shape=azure-sas-signature` (`c2-probe.txt`). So the capability is right and the counter cannot
see its loss — exactly the r88 F1/M88-2 shape recurring on the same clause family.
**Impacted axis.** coverage (a false-negative surface left unpinned).
**Smallest correction.** One K4 plant (start after `%26`, `sv` after a `&`), one `CLAUSES` row, one
K7 generated negative with the companion parameter removed.

### C2-F2 — DEFECT (counter): the "up to 20 other parameters between" clause has no limb

**Counterexample.** `_CF_PARAM … {0,20}?` → `{0,1}?` still passes every limb (mutant `win1`). No
plant has 2–20 intervening parameters and no negative has 21. The landed value is correct: probes
show 20 intervening parameters → HIT, 21 → no HIT (`c2-probe.txt`).
**Impacted axis.** coverage (the window is a stated false-negative limit).
**Smallest correction.** A 20-parameter positive and a 21-parameter negative plant, plus the
`CLAUSES` rows.

### C2-F3 — QUALIFIER: the exact precision bounds are unpinned

**Counterexample.** Three mutants pass all limbs: `{40,}` → `{13,}` (`floor13`), `{8,32}` → `{8,64}`
(`kpi64`), `{8,32}` → `{1,32}` (`kpi1`). The frozen `cffloor` control only pins the floor above 12
(S013's signature is exactly 12 characters). Probes confirm the landed bounds are the stated ones:
Signature 39 → no HIT, 40 → HIT; Key-Pair-Id 7 → no HIT, 8 → HIT, 32 → HIT, 33 → no HIT.
**Impacted axis.** coverage-adjacent precision (not the coverage edge).
**Smallest correction (only if the bounds are meant to be frozen):** boundary plants 39/40, 7/8,
32/33 and a `CLAUSES` row for the widths.

### C2-F4 — DEFECT (frozen claim text): the `clauses` field overstates K8

`claims.json` says "c2/capability-check.py CLAUSES (K8) maps every statement clause to a plant".
K8 verifies a hand-authored 10-entry list against K4; it does not derive the list from the
statement, and five statement sub-clauses are absent from it (`%26`; the 20-parameter window; the
40-character floor; the 8 and 32 Key-Pair-Id bounds). This is the M88-2 shape in weakened form:
"every clause" holds only for the clauses someone remembered to list.
**Bounded by what is bound.** The clauses that *are* bound: case-sensitivity fails two limbs when
made insensitive (`(?i)` → K1 selftest FAIL, K7 extra `live-n2`), the `\u0026` separator fails
K1/K4/K7/K8 when dropped, the X-Amz left boundary has the frozen `cfdash` control, and either
order, the doc placeholder, Signature-without-Key-Pair-Id and the capture-scope negative each have
K4/K7 plants.
**Impacted axis.** coverage (instrument credibility), not the predicate (P1 says K1–K8 pass and it
does).
**Smallest correction.** Reword the field to "maps the 10 named clauses", or extend `CLAUSES` with
C2-F1..F3's plants; do not read the frozen field as clause-complete.

### C2-F5 — QUALIFIER: S128/S130 are still `queued` after the C2 landing

At `c61c5586` both rows read `status=queued`, `used-by=—`, while the landed instrument's docstring
cites S128 lines 13, 70–78, 202–211 and S130 lines 14, 66, 75–84 (all five lines exist with the
cited content). The r88 precedent set S126/S127 to `mined` with a used-by at the landing
(`corpus/SOURCES.md` line 312). P3's exact three-path set forbids the landing from touching
`corpus/SOURCES.md`, so the update belongs to the integration commit, not the landing.
**Impacted axis.** coverage/provenance (a used source that the registry does not credit).
**Smallest correction.** Integration commit: set both rows `mined` and
`used-by=corpus/instruments/capture-secret-scan.py`.

### C2-F6 — VERIFIED clause: the allowlist rows are genuinely digest-bound

sha256 of the 209-byte match in **each** snapshot is `f8d573cb…` — equal to the allowlist digest in
both rows — and the match contains the literal `EXAMPLE` and the documented key-pair id
`K2JCJMDEHXQW5F`. Both rows are used (`allowed=20`, `unused_allow=0`), so the two doc-example rows
are load-bearing, not stale. Not a finding.

### C2-F7 — VERIFIED clause: this is coverage, not quality

The addition is a provider shape the base instrument cannot match: the base scanner at `090a46f`
flags none of the three round-89 probe files, and K6 reports `new_caught_by_base=none`. That matches
the r88 capability-extension precedent on the coverage axis; the unbound clauses above are the
precision/limit bounds, not the coverage edge.

## Controls and ordering (attacked)

- **Pre-freeze controls.** `controls/c1-controls-r89.txt`, `c2-controls-r89.txt`,
  `c2-controls-r89-first-run.txt`, `capture-scan-r89.txt`, `census-start-r89.txt` are committed in
  the freeze `94573d2` and are byte-identical to the working-tree copies. The landings are its
  children. `claims.json` is in the freeze and unchanged. The C1 do-nothing and prefix-forgery
  blocks reproduce exactly; the C2 do-nothing block reproduces exactly. The first-run C2 file is
  disclosed as a transcription and explains two pre-freeze fixes (K7 plant path moved into the
  capture scope; literal control widened) — the rerun file is raw and reproduces.
- **Do-nothing.** C1: M1/M2/M3 FAIL at `777/1798`. C2: K1/K4/K5/K7/K8 FAIL, K6 passes by
  construction. Neither target is reachable by doing nothing.
- **Cheap forgery.** C1 prefix-only: 784/1796 + M9 FAIL. C2 literal-only: fails K7 (frozen
  control); shape-minus-`%26` or shape-with-1-parameter: **passes** (C2-F1/F2) — the one remaining
  forgery surface.

## Hygiene (this round's subject)

- No credential-shaped value appears in this report or in any receipt: all receipts carry sha256
  digests, paths and the scanner's HIT/summary lines only.
- `capture-secret-scan.py --files <12 receipt files> --allow /dev/null` → `hits=0 rc=0`.
- `… --files $(find .ufo/waves/round-89/w1 -type f) --allow /dev/null` → `hits=0 files=0 rc=0`
  in every run (45 files before this report; 63 files with this report and its 12 receipts).
  This report itself scans `hits=0`.
- The whole round-89 wave directory scans to **7 hits in 2 files**, all inside the frozen
  instruments' own fixture literals (`c2/candidate/capture-secret-scan.py` and
  `c2/capability-check.py`: `private-key`, `credential`, `aws-access-key-id`,
  `aws-sts-session-token`). That is inherent to an instrument that plants fixtures and is why the
  contract forbids copying them into `w1/`; the L1's pre-commit scan should expect those two paths.

## Files written

- `.ufo/waves/round-89/w1/CriticClaims.md` (this report)
- `.ufo/waves/round-89/w1/CriticClaims-receipts/`: `c1-p1.txt`, `c1-p2.txt`, `c1-p3.txt`,
  `c1-donothing.txt`, `c1-prefix-forgery.txt`, `c2-p1.txt`, `c2-p2.txt`, `c2-p3.txt`,
  `c2-donothing.txt`, `c2-probe.txt`, `c2-mutants.txt`, `wave-scan.txt`

Scratch root `/fast/scratch/hyaku/kasegi-r89/CriticClaims/` (lane clones, mutant clone, fixtures,
probe files) was removed after the receipts were copied; nothing was written to the lane tree
outside the two paths above.
