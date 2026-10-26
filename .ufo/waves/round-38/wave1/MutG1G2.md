# MutG1G2 — round-38 mutation test of r38-closure.sh limbs G1 and G2

Seat: MutG1G2 (leaf, no subagents). Item: mutation-test the G1 and G2 limbs of
`corpus/instruments/r38-closure.sh`; per limb apply one-limb source mutations
(delete condition / invert / widen regex / fail-closed read → default), run each
mutant against (a) a base `a173b0c2` export and (b) the suite's own `--selftest`;
a surviving mutant is a coverage finding naming the limb and the missing fixture.

## 1. Deliverable tracking (the file moved three times during this run)

The executor's deliverable was revised while this seat ran. All three versions
were captured; the campaign below is authoritative against the final bytes.

| ver | wave1 sha256 (prefix) | bytes | lines | captured (UTC) |
|---|---|---|---|---|
| v1 | `85d33ea9d386926e` | 61159 | 1473 | 18:46 check 3 |
| v2 | `7883c37cd3249a12` | 74707 | 1716 | ~19:05 |
| v3 | `09d46673a75b5047` | 77726 | 1767 | ~19:20, stable through filing |

Wait protocol: deliverable absent at checks 1–2 (18:36:04Z, 18:41:10Z), present at
check 3 (18:46:12Z). No fallback implementation was needed.

v1→v2: G1 gained the outside-fence correction rule, a second fuller CommonMark
walk (tilde, closing-run length), lane-relative declaration paths, and the
declaration-must-cover-correction rule; G2 gained no-`closed=0`-lines, real-pass
case claims, `cat-file -t` commit check, `--name-status` rename-off diff, and
cross-run payload key-set binding. v2→v3: `check_g1`, `g1_declared`,
`g1_cm_walk`, `g1_fixture`, `selftest_case_G1` byte-identical (G1 results
transfer; re-verified by regenerating all G1 mutants against v3 anyway);
`check_g2` gained header-block-scoped counts and a per-commit history limb
(`history=`, every commit in `export-ref..REF` only A/M/R rows) with a new
`history-added-then-removed` fixture; `g2_fixture` unchanged.

Observation for the L1 (not my item): the lane's untracked
`corpus/instruments/r38-closure.sh` is the **stale v1 bytes** (`85d33ea9…`,
1473 lines) while wave1 carries v3 (`09d46673…`, 1767 lines) — landing the lane
copy as-is would commit the two-revisions-older suite.

## 2. Pristine baselines (v3, sha256 `09d46673a75b50479bb2b7e184b370d08554ad6a7e21ff6f63c67edca640be42`)

- plain run → `r38-closure: refusing to run against the live worktree…`, **exit 2** ✓
- `--export-ref a173b0c2b98c5ae39599fa9be76027fbbead0b9e` → **`closed=0/8 exit=1`**;
  `G1 payload=province-correction=0,readme-correction=0,province-fence=closed,readme-fence=open,declared-blocks=0,declared-ok=0 closed=0`;
  `G2 payload=receipt=0,…,crossrun=0,history=0 closed=0` — G1 and G2 red at base ✓
- `--selftest --export-ref 7001535` → `selftest cases=8 failures=8`;
  `case=G1 positive=fail mutants=6/6`, `case=G2 positive=fail mutants=12/12`,
  all negative fixtures `rejected=1` ✓

Detector note: the claims run `--selftest --export-ref <J>`; J does not exist yet
(the receipt is unlanded), and the selftest positives run against the export of
the given ref, so at any pre-landing ref positives fail by design. Detector (b)
is therefore **differential at a fixed ref (7001535)**: a mutant is killed-by-(b)
iff its G1/G2 selftest case/detail blocks differ from pristine's (a negative
fixture flipping to `rejected=0`, or a lost/changed detail). Detector (a) is the
base export: a mutant is killed-by-(a) iff a base-red G1/G2 limb flips to green
in the payload/verdict. To make "survived" independent of the pre-landing ref,
every surviving mutant was additionally run against the suite's own **green
fixture tree** (`g1_fixture`/`g2_fixture` + live key-set file, the exact positive
the selftest runs at J): all 19 survivors print rc=0 there, i.e. they would also
survive at a green J. Controls: pristine rc=0 on both green trees; killed invert
controls (M3-G1-05, M3-G2-05) rc=1.

## 3. Mutant table (v3 bytes; 28 one-limb mutants)

Find/replace are exact source substrings; each mutant differs from pristine by
exactly one line (verified; line numbers refer to v3). "no delta" = byte-identical
G1/G2 base lines and selftest blocks vs pristine.

| id | limb | mutation (find → replace) | base a173b0c2 run | selftest run | verdict |
|---|---|---|---|---|---|
| M3-G1-01 | province-fence | delete `&& [ "$pf" = closed ]` from check_g1 chain (L456) | no delta | no delta | **SURVIVED** |
| M3-G1-02 | readme-fence | delete `&& [ "$rf" = closed ]` (L456) | no delta | no delta | **SURVIVED** |
| M3-G1-03 | correction wording | drop `&& line ~ /(^|[^[:alnum:]_])misplaced([^[:alnum:]_]|$)/` from g1_cm_walk count (L378) | no delta | no delta | **SURVIVED** |
| M3-G1-04 | declared-blocks missing-file read | `printf '0 0'` → `printf '2 1'` in g1_declared (L391) | G1 payload `declared-blocks=0,declared-ok=0` → `2,1` (base limb turns green) | positive payload flips | KILLED (a+b) |
| M3-G1-05 | declared-ok | `[ "$dok" -eq 1 ]` → `-eq 0` (L457) | no delta | dotdot fixture accepted (`declaration-path-escapes-export rejected=0`, mutants 5/6) | KILLED (b) |
| M3-G1-06 | valid-count | delete `&& [ "$valid" -ge 2 ]` (L457) | no delta | no delta | **SURVIVED** |
| M3-G1-07 | lane-relative path | `case $path in /*|*..*)` → `in ZZZNEVERZZZ)` in g1_declared (L402) | no delta | no delta | **SURVIVED** |
| M3-G1-08 | declaration-covers-correction | `[ "${got:-0}" -ge 1 ] \|\| { bad=1; continue; } ;;` → `: ;;` (L415) | no delta | no delta | **SURVIVED** |
| M3-G1-09 | outside-fence counting | `if (!open && index(…))` → `if (index(…))` in g1_cm_walk (L376) | no delta | cfence fixture accepted (`correction-inside-fence rejected=0`, 5/6) | KILLED (b) |
| M3-G1-10 | readme-correction | delete `&& [ "$rcor" -ge 1 ]` (L456) | no delta | no delta | **SURVIVED** |
| M3-G2-01 | ancestor | delete `&& [ "$ancestor" -eq 1 ]` (L572) | no delta | no delta | **SURVIVED** |
| M3-G2-02 | diff-clean | delete `&& [ "$diffclean" -eq 1 ]` (L573) | no delta | no delta | **SURVIVED** |
| M3-G2-03 | closed-line | `grep -cE '^closed=8/8 exit=0$'` → `'^closed=8/8'` (L513) | no delta | no delta | **SURVIVED** |
| M3-G2-04 | receipt existence | `if [ -f "$p" ]` → `if [ -e . ]` (L479) | G2 payload `receipt=0` → `1` | positive payload flips | KILLED (a+b) |
| M3-G2-05 | digest | `= "$(suite_digest)"` → `!=` (L506) | no delta | digest-mismatch accepted (`digest-match=1`, 11/12) | KILLED (b) |
| M3-G2-06 | 8-distinct-closed=1 lines | `[ "$n" -eq 8 ] && [ "$got" -eq 8 ] && runlines=1` → `runlines=1` (L510) | no delta | no delta | **SURVIVED** |
| M3-G2-07 | zero-closed=0 lines | `[ "$n" -eq 0 ] \|\| runlines=0` → `:` (L512) | no delta | closed0 fixture accepted (11/12) | KILLED (b) |
| M3-G2-08 | real-pass case claims | `for g in G1 G2 … G8; do` → `for g in; do` (L522) | no delta | casefail fixture accepted (11/12) | KILLED (b) |
| M3-G2-09 | crossrun | delete `&& [ "$cross" -eq 1 ]` (L576) | no delta | keydrift fixture accepted (11/12) | KILLED (b) |
| M3-G2-10 | selftest-summary | delete `&& [ "$stsum" -eq 1 ]` (L574) | no delta | no delta | **SURVIVED** |
| M3-G2-11 | scorecard-ref | delete `&& [ "$scref" -eq 1 ]` (L575) | no delta | no delta | **SURVIVED** |
| M3-G2-12 | shonen-ref | delete `&& [ "$shonenref" -eq 1 ]` (L575) | no delta | no delta | **SURVIVED** |
| M3-G2-13 | head-token-zero | delete `&& [ "$headtok" -eq 0 ]` (L575) | no delta | both headline fixtures accepted (10/12) | KILLED (b) |
| M3-G2-14 | export-ref-is-commit | `[ "$(git … cat-file -t …)" = commit ]` → `[ -n "$(…)" ]` (L491) | no delta | no delta | **SURVIVED** |
| M3-G2-15 | name-status A/M-only | drop `&& { [ "$st" = A ] \|\| [ "$st" = M ]; }` (L500) | no delta | no delta | **SURVIVED** |
| M3-G2-16 | export-ref-present | delete `[ -n "$xref" ] &&` (L572) | no delta | no delta | **SURVIVED** |
| M3-G2-17 | per-commit history (v3 new) | delete `&& [ "$hist" -eq 1 ]` (L576) | no delta | no delta | **SURVIVED** |
| M3-G2-18 | header-scoped export-ref count (v3) | `printf '%s\n' "$hdr" \| grep -cE …` → file-wide `grep -cE … "$p"` (L~495) | no delta | no delta | **SURVIVED** |

**Totals: 9 killed, 19 survived.** Every survivor verified rc=0 on the suite's own
green fixture tree, so none of them is an artifact of the pre-landing ref.

Earlier campaigns (same method, superseded bytes): v1 19 mutants → 6 killed
(M-G1-2 readme-fence, M-G1-4, M-G2-4, M-G2-5, M-G2-7 sentinel, M-G2-10 headtok),
13 survived; v2 26 mutants → 9 killed, 16 survived (same survivor set as v3 minus
the two v3-only limbs). One v1→v2 **regression** worth flagging: v1's
`readme-fence-open` fixture isolated the readme-fence limb (deleting the conjunct
was killed); v2/v2's fence-aware `g1_cm_walk` makes that fixture co-fault
`readme-correction=0`, so the kill disappeared.

## 4. Findings (survivors → limb + missing fixture)

**F-A — the four repo-based G2 history fixtures are vacuous (suite fixture bug,
strongest finding).** `g2_fixture` begins with `mut_reset "$d"` (`rm -rf`), and
`selftest_case_G2` calls `g2_fixture "$repo" …` **after** `git init`, destroying
the fixture repo's `.git`. Every subsequent `git add/commit/checkout` fails
(stderr suppressed), `c1/ref/side` stay empty, and the receipt is written with an
empty `export-ref=` line. Proof against the v3-pristine control, reproducing the
selftest's own steps:

```
is-repo=fatal: not a git repository (or any parent up to mount point /)
receipt-head=all-gates v2|export-ref=|suite-sha256=09d46673…|
payload=receipt=1,sentinel=1,export-ref=0,ancestor=0,diff-clean=0,…,crossrun=0,history=0
```

The check therefore rejects via `[ -n "$xref" ]` (`export-ref=0`) — never via the
limbs the fixtures exist to exercise. That is why five mutants survive:
M3-G2-01 (ancestor), M3-G2-02 (diff-clean), M3-G2-14 (export-ref-is-commit),
M3-G2-15 (name-status A/M-only), M3-G2-16 (export-ref-present) — and the v3-new
M3-G2-17 (per-commit history): its `history-added-then-removed` fixture is
repo-based and inherits the same wipe. Pristine's `mutants=12/12` for G2 counts
five vacuous rejections. Missing fixture: `g2_fixture` must not wipe an
initialized repo (reset only before init, or add a no-reset write path); then a
real side-branch commit exercises `ancestor=0`, a real post-receipt commit
exercises `diff-clean=0`, an annotated tag exercises the `cat-file -t` limb, a
`git mv` receipt exercises the A/M rows, and a commit that adds-then-removes a
file inside `export-ref..REF` exercises `history=0`.

**F-B — G1 fence/correction fixtures co-fault two limbs each.** With
`ropen=yes` (or `tilde=yes`), the unclosed fence opens *before* the README
correction line, so the fence-aware correction count also drops:
`payload=province-correction=1,readme-correction=0,…,readme-fence=open`. Deleting
either the fence conjunct (M3-G1-02) or the readme-correction conjunct
(M3-G1-10) leaves the other rejecting → both survive. Likewise no fixture ever
opens the **province** fence (`cfence` opens and closes; `ropen`/`tilde` are
README-only) → M3-G1-01 survives. Missing fixtures: a `pfence=yes` knob and
fence-open knobs that open *after* the correction line (so the correction stays
outside fences and only the fence limb faults).

**F-C — unkillable / unexercised G1 declared-blocks limbs.**
- M3-G1-06 (`valid -ge 2` deleted) survives **by construction**: `dok=1` requires
  `have_p ∧ have_r`, which implies ≥2 valid rows — the conjunct is logically
  redundant; no single-fault fixture can isolate it. Either drop it or make it
  meaningful (e.g. require ≥2 declarations per front door).
- M3-G1-07 (lane-relative path check deleted) survives because the `dotdot`
  fixture never places the escape target: `../PROVINCE.md` fails the plain
  `[ -f "$tree/$path" ]` existence test anyway. The limb is load-bearing — with a
  sibling file placed outside the export tree, the **mutant accepts a
  declaration that binds bytes outside the export**
  (`scenario=dotdot-esc mutant=M3-G1-07 rc=0 payload=…,declared-blocks=3,declared-ok=1`
  vs pristine rc=1 `declared-ok=0`). Missing fixture: the dotdot fixture must
  create the sibling (`$MUT/PROVINCE.md` with matching tail bytes) so the
  existence test passes and only the lane-relative limb faults.
- M3-G1-08 (declaration-must-cover-correction deleted) survives: no fixture
  declares a tail without a `Correction (round 38)` line (e.g. declaring only the
  comment line). Missing fixture: a `shortdecl=yes` knob declaring 1 line.
- M3-G1-03 (dropping the `misplaced` word requirement) survives: no fixture
  carries an outside-fence correction line that lacks `misplaced` or names the
  wrong range. Missing fixture: a `pcor=weak` knob.

**F-D — G2 receipt-shape limbs with no negative fixture.** M3-G2-03 (widening
`closed=8/8 exit=0` to `closed=8/8` accepts an `exit=1` receipt), M3-G2-06
(deleting the 8-distinct-`closed=1`-lines sub-limb — a receipt with 7 run lines
or a duplicate id passes; the `closed0` fixture only covers the zero-`closed=0`
half), M3-G2-10 (`stsum`), M3-G2-11/M3-G2-12 (`scref`/`shonenref` — the
`g2_fixture` knobs exist but `selftest_case_G2` never uses them), M3-G2-18
(reverting v3's header-scoped export-ref count — no fixture duplicates
`export-ref=` inside the run section). Missing fixtures: receipt variants with
`closed=8/8 exit=1`, 7 run lines, `selftest cases=8 failures=1`, `scref=no`,
`shonenref=no`, and a second `export-ref=` line after `== run ==`.

## 5. Method, environment, restoration

- Suite copies, mutants, exports, fixture repos: all under
  `S=/fast/scratch/hyaku/kasegi-r38/MutG1G2` (`TMPDIR=$S`; every suite run used
  `--work` under `$S`). Detector runs: 2 × 28 mutants + baselines + green-tree
  runs; each mutant verified `bash -n` clean and exactly one line different from
  pristine (asserted at generation).
- Restoration: after all mutants, pristine v3 re-runs are byte-identical to the
  baselines (base export diff empty; selftest G1/G2 blocks diff empty);
  `r38-pristine-v3.sh` sha256 `09d46673a75b50479bb2b7e184b370d08554ad6a7e21ff6f63c67edca640be42`
  equals the wave1 deliverable at filing. The lane repo was never written by
  this seat (git status shows only the concurrent round-38 landing by others;
  this receipt is my first and only lane write).
- Git mutations: none by this seat. Fixture `git init/commit` steps ran only
  inside scratch copies driven by the suite's own fixture code (toplevel
  asserted by the suite; reproduced in my debug driver under `$S`).
- Tooling: nothing installed or upgraded (bash/git/awk/python3 sufficient). No
  network fetches. No pacman. Scratch dir removed before yield.
