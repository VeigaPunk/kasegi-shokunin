# R44Mutant3 — mutation that fools hash-prefix numeral verification; exact expected kill

## Verdict

**KILLED.** Five single-substitution mutants of a candidate hash-prefix numeral
limb were each (a) shown to be *fooled* — they print `verdict=pass`, exit 0, on a
claim whose stated numeral is wrong — and (b) *killed* by the lane's own committed
mutation harness (`limb-mutation-check.py`): `limbs=5 killed=5 survivors=0`,
`controls=3 rejected=3`, exit 0. The exact kill is reproduced below.

## Grounded numerals (committed bytes, identical at frozen base `5ab3a60` and HEAD `6631401`)

- `corpus/lessons/round-43.md` sha256 `ba118cea2c98128fe7cd78144fe5d43ac3e91a85829d8c533f16f31ecd163e48`
  at **both** revisions — defect 3 is untouched (also confirmed by `git diff`
  on the two `character prefix` lines at `:90` and `:101`).
- `printf '%s' c6ae07c6a541e0e96d0040afb6 | wc -c` → **26**; `printf '%s' c6ae07c6a541e0e96d0040afb62b45dd37711300 | wc -c` → **40**.
- The documented off-by-one: `printf '%s\n' c6ae07c6a541e0e96d0040afb6 | wc -c` → **27** (the `\n` is counted);
  R44Review3 flagged the same trap. This is the realistic source of a *plausibly-correct* wrong numeral.
- `grep -c 'wc -c' corpus/lessons/round-43.md` → **0** — the numeral carries no counting command (defect 3's second half).
- No `corpus/instruments/r44-*` or numeral limb exists at HEAD — so "hash-prefix
  numeral verification" is **absent** at base/HEAD; absence is not verification.

## What the numeral limb must do (the contract the mutant attacks)

A claim `<N>-character prefix` binds to the hex token inside the **quoted span**
the claim annotates (the lesson's claim quotes `"Fixed-in: …commit/<token>"`);
the numeral must equal `len(token)` counted **without a trailing line feed**;
and a claim with no bound token must **fail closed**. Anything looser is foolable.

## Mutants designed and probed (each a one-point change in the scratch copy `numeral_limb.py` sha `56332aa4…`)

| id | mutation (smallest behavior-bearing point) | wrong numeral that fools it | data proof (mutant output) |
|---|---|---|---|
| m1-newline-measure | `return len(token)` → `return len(token) + 1` | **27** (newline-inclusive count) | `stated=27 measured=27 verdict=pass`, exit 0 on `claim-27-newline.md` |
| m2-unquoted-nearest | `bind()` takes nearest hex run, ignoring quote marks | **29** decoy placed next to the claim | `token=c6ae07c6a541e0e96d0040afb62b4 measured=29 verdict=pass`, exit 0 on `claim-29-exists.md` |
| m3-exists-length | `stated != measure(token)` → `stated not in {measure(t) for t in hex_runs(block_text)}` | **29** if *any* block token is 29 | `measured=26 verdict=pass`, exit 0 on `claim-29-exists.md` (and `claim-40-firsttoken.md`: ∃ 40-hex ⇒ pass) |
| m4-unbound-pass | `…"FAIL","UNBOUND"` → `…"pass","UNBOUND"` | **any** numeral with no quotable token | `verdict=pass rule=UNBOUND` on an unquoted claim |
| m5-first-token | `bind()` returns `hex_runs(block_text)[0]` | **40** when the full hash precedes the claim | `token=c6ae07c6a541e0e96d0040afb62b45dd37711300 measured=40 verdict=pass`, exit 0 on `claim-40-firsttoken.md` |

The sharpest fool is **m2/m3**: an adjacent *decoy prefix* of the claimed length
(`c6ae07c6a541e0e96d0040afb62b4`, the first 29 hex of the real 40-hex hash, so it
even passes an ancestor check) launders a wrong numeral through any binder that
does not anchor to the quoted span.

## Exact expected kill (observed, not inferred)

Pristine limb on the committed lesson:

```
claim line=90 stated=29 token=c6ae07c6a541e0e96d0040afb6 measured=26 verdict=FAIL rule=NUMERAL
claim line=101 stated=29 token=- measured=- verdict=FAIL rule=UNBOUND
claims=2 pass=0 fail=2 closed=0        exit=1
```

Each mutant's selftest fixture that must fail:

| mutant | killing fixture line | summary/exit |
|---|---|---|
| m1 | `selftest correct-26 verdict=fail … got=FAIL/NUMERAL` (and `stated-27… got=pass`, `full-hash-40`) | `cases=7 failures=3`, exit 1 |
| m2 | `selftest decoy-adjacent-prefix verdict=fail … got=pass/-` | `cases=7 failures=1`, exit 1 |
| m3 | `selftest paragraph-first-token verdict=fail … got=pass/-` | `cases=7 failures=1`, exit 1 |
| m4 | `selftest decoy-adjacent-prefix … got=pass/UNBOUND`, `unbound-claim … got=pass/UNBOUND` | `cases=7 failures=2`, exit 1 |
| m5 | `selftest paragraph-first-token … got=pass/-`, `decoy-adjacent-prefix … got=FAIL/NUMERAL` | `cases=7 failures=2`, exit 1 |

Committed-harness run over a scratch probe lane
(`TMPDIR=$HYAKU_SCRATCH… python3 corpus/instruments/limb-mutation-check.py
 --ledger probe-ledger.json --root probe-lane`):

```
guard cases=3 failures=0
LIMB PN-newline     live=0/y mutant=1/n verdict=killed
LIMB PN-unquoted    live=0/y mutant=1/n verdict=killed
LIMB PN-exists      live=0/y mutant=1/n verdict=killed
LIMB PN-unbound     live=0/y mutant=1/n verdict=killed
LIMB PN-firsttoken  live=0/y mutant=1/n verdict=killed
CONTROL CTL-noop      verdict=invalid:noop      expected=invalid:noop      ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor         expected=survivor          ok=y
limbs=5 killed=5 survivors=0
controls=3 rejected=3
exit=0
```

In-place probe (mutate → detect → restore):
pristine `56332aa4ddcdb2e4b34828071077319e19de67eafb67b18c1bea6eeaf4c80038`
→ mutant `a2216427762ce6d18e5e194f8341ea5014943d4cd4da84ca5a1828b0fefdeb1e`
(exit 1, `cases=7 failures=1`) → restored **`56332aa4…`** byte-exact, exit 0,
`cases=7 failures=0`.

## Do-nothing discrimination

The control states no r44 correction/counter exists at `5ab3a60`. Measured: the
lesson bytes are identical base↔HEAD, no `r44-*` instrument exists, and the limb
is **red** on both (`exit=1`). A do-nothing replay therefore produces the open
defect (red), never `closed=1`; and since no verifier exists at all, "verified"
cannot be claimed by absence. The five fooling mutants are the specific ways a
*too-weak* r44 numeral limb could be written; the fixture set above is what kills
each.

## Limitations

- `numeral_limb.py` is a scratch probe, not a committed lane instrument; the
  `corpus/instruments/r44-routed-defects.py` counter named in C1 did not exist at
  HEAD. Verdicts are probe-level kills under the lane's committed harness, not a
  landed-gate result. The exact ledger rows are included so L1 can bind them.
- The quoted-span binding is a design choice matching the lesson's own quote
  discipline; a different correct binding is possible but must still (i) anchor
  to the referenced token, not an ∃/nearest-anywhere rule, and (ii) fail closed
  on unbound claims.
- m3's fooling depends on a block-level ∃ rule; a per-claim ∃ (same sentence)
  would need the decoy inside that sentence — still foolable, same fix.

## Scope compliance

- Scratch: `/fast/scratch/hyaku/kasegi-r44/R44Mutant3/` (default `HYAKU_SCRATCH`
  was empty; used the documented default root). Deleted on exit.
- No edits outside this report path and scratch; no git/jj mutation, no commits,
  no tool installs (none needed: python3 + bash).
- No verdict inflation: the mutant is *killed* because a properly-written limb
  plus the committed harness kills it; the finding is a coverage design
  requirement for the r44 counter, not a claim that the lane gate exists.
