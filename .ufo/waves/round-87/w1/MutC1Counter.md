# MutC1Counter — mutation test of the frozen r87 C1 counter

Seat: `MutC1Counter` (mutation-tester). Target: `.ufo/waves/round-87/c1/knowledge-meter.py`
(sha256 `949f0625f02bbd2fcc05a9d7ddddc7e622137f5935f06d1a27be252e3fe927be`, unchanged before
and after this seat). Base `cd1f568a6be2656b5f5dc479eb90ef99b91131b5`; map
`.ufo/waves/round-87/c1/repair-map.json` sha256 `7db928c77efe2f594c0fcbc26174b79db1f60f7a1d244055b679512c778f1eaa`;
target `678/1719`. Every run is a `git clone --shared` of the lane at `cd1f568a` under scratch,
with `python3 -B`. No lane file was written; no frozen byte was edited.

Result: **28 single-point mutants, 19 killed, 9 survived (all mutation-equivalent or
unreachable, with proofs below).** The frozen battery alone kills 7; 12 more die under the
11 limb-isolating controls this seat built (`MutC1Counter-controls-ext.sh`).
**Routed defect RD-1: of the counter's 7 limbs, the frozen battery isolates exactly one (M6).**

## 1. Baseline validity (detector first)

`MutC1Counter-score-frozen.py` re-implements `controls/c1-controls-r87.sh` (same seven trees,
same four derived maps, same targets, same expectations) and builds its own trees. On the
pristine counter it reproduces `controls/c1-controls-r87.txt` **limb-for-limb, all 8 controls,
zero drift** (`MutC1Counter-frozen-battery.txt`):

| control | expected | observed | fail limbs |
|---|---|---|---|
| do-nothing | fail | fail rc=1 | M1,M2,M3 |
| positive | pass | pass rc=0 | — |
| partial (half applied, frozen map scored) | fail | fail rc=1 | M1,M2,M3 |
| pad (+2 resolving cites) | fail | fail rc=1 | M1,M2,M3 |
| ufo-copy (one key → `.ufo` fixture copy) | fail | fail rc=1 | M4,M5 |
| S041-forge (ambiguous 3-capture key) | fail | fail rc=1 | M1,M4,M5 |
| quoted-forge (S020 re-added) | fail | fail rc=1 | M1,M7 |
| map-sha (wrong sha) | fail | fail rc=1 | M6 |

So the measured discrimination below is against a detector that is itself correct on the
frozen bytes.

### Limb isolation of the frozen battery (the structural result)

| limb | isolated by the frozen battery? | note |
|---|---|---|
| M1 | no | always co-fails with M2,M3 (do-nothing/partial/pad) or with M4/M7 (forges) |
| M2 | no | same three controls as M1 |
| M3 | no | same three controls as M1 |
| M4 | no | always co-fails with M5 (`M5 = not m5bad and not m4bad`) |
| M5 | no | cannot fail without M4; ufo/S041 print `M5 FAIL out_of_range=none` |
| M6 | **yes** | map-sha fails M6 and nothing else |
| M7 | no | quoted-forge also fails M1 |

Consequence (QUALITY R13 "each limb shown load-bearing by an isolating fixture"): 6 of 7
limbs have no isolating fixture in the frozen battery. RD-1.

## 2. Mutant matrix

`mutants` column is the exact single substitution (`MutC1Counter-mutants.tsv`, one row per
mutant; each matched exactly once in the frozen source). "frozen" = verdict under the 8 frozen
controls; "ext" = the control that kills it (`MutC1Counter-controls-ext.sh`).

| id | single-point mutation | limb | frozen | ext killer |
|---|---|---|---|---|
| M01 | `bybase` fill: `if p.startswith("corpus/source-snapshots/"):` → `if True:` | M4 | **killed** (positive) | — |
| M02 | same line → `if p.startswith("corpus/"):` | M4 | survived | dup-basename |
| M03 | `bybase.get(name) == [path]` → `path in bybase.get(name, [])` | M4 | survived | s041-own-rate |
| M04 | drop `path.startswith("corpus/source-snapshots/")` | M4 | survived | *equivalent* (proof §3) |
| M05 | drop ` and bcls.get(k) == "GONE"` | M4 | survived | not-gone (`KASEGI_MIRROR`) |
| M06 | drop `and R.classify(v, lane, mirror)[0] == "INTERNAL"` | M4 | survived | nofile-own-rate |
| M07 | `QUOTED = frozenset({S020,S021,S023,S025})` → `frozenset()` | M7 | survived | quoted-key |
| M08 | `q_moved = sorted(...)` → `q_moved = []` | M7 | survived | *equivalent* (proof §3) |
| M09 | `q_in_map = sorted(...)` → `q_in_map = []` | M7 | survived | *equivalent* (proof §3) |
| M10 | `added <= vals` → `added == vals` | M2 | **killed** (positive) | — |
| M11 | `removed == keys` → `keys <= removed` | M2 | survived | *equivalent* (proof §3) |
| M12 | drop ` and added <= vals` | M2 | survived | *equivalent* (proof §3) |
| M13 | verify replace-all → `replace(..., 1)` | M3 | survived | dup-key-line |
| M14 | `hit == keys` → `hit <= keys` | M3 | survived | *equivalent* (proof §3) |
| M15 | `if len(bl) != len(al):` → `if False:` | M3 | survived | appended-line |
| M16 | `same_files = set(bfiles) == set(afiles)` → `True` | M3 | survived | extra-file |
| M17 | `1 <= lo_i <= hi_i <= nlines` → `... <= nlines + 1` | M5 | survived | range-out |
| M18 | same → `... < nlines` | M5 | survived | range-edge |
| M19 | `not m5bad and not m4bad` → `not m5bad` | M5 | survived | *equivalent* (proof §3) |
| M20 | M1 `(an, am) == (tn, tm)` → `an >= tn` | M1 | survived | target-degenerate |
| M21 | M1 verdict → `True` | M1 | survived | target-degenerate |
| M22 | `if a.map_sha256:` → `if False:` | M6 | **killed** (map-sha) | — |
| M23 | `got == a.map_sha256.lower()` → `!=` | M6 | **killed** (positive, map-sha) | — |
| M24 | exit: `return 0 if allok else 1` → inverted | exit | **killed** (all 8) | — |
| M25 | `allok = all(...)` → `allok = True` | exit | **killed** (7 of 8) | — |
| M26 | `if c != "GONE"` → `if c == "INTERNAL"` | M1 | **killed** (positive) | — |
| M27 | scope filter `p.count("/") == 2` → `>= 2` | scope | survived | *unreachable* (§3) |
| M28 | `not m4bad and bool(tracked)` → `not m4bad` | M4 | survived | *unreachable* (§3) |

Raw per-mutant output (8 controls × 28 mutants, with limb sets and drift): 
`MutC1Counter-frozen-matrix.txt`.

## 3. The 9 survivors are equivalent or unreachable — not coverage escapes

Each is proven, not assumed, and the proof names the limb that carries its duty.

- **M04** — `bybase` is filled only from tracked paths under `corpus/source-snapshots/`
  (`m4` builds `bybase` with that prefix, and `git ls-files` evidence: no tracked `corpus/`
  file outside `corpus/source-snapshots/` carries an `S###.txt` basename). So
  `bybase.get(name) == [path]` already implies both `startswith("corpus/source-snapshots/")`
  and `endswith("/" + name)`. Dropping either clause cannot change any verdict on any tree.
  *Qualifier:* the r87 docstring/r87 change is credited to the scope test, but the scope is
  actually enforced by the `bybase` construction; the two prefix tests are decoration.
- **M08 / M09** — the two M7 clauses are mutually redundant. Measured: on the quoted-key
  fixture, M08 still fails M7 through `q_in_map`, M09 still fails through `q_moved`. Killing
  one alone is impossible because (a) a QUOTED token that moves without being a map key
  requires a knowledge edit, which M3 rejects line-by-line; and (b) a map key that is not
  GONE at base is rejected by M4's GONE clause, so `q_moved` can never be the only detector
  while `q_in_map` exists.
- **M11 / M12** — implied by M3. M3 requires `after[line] == base[line]` with every backticked
  map key replaced by its value; that transform makes *removed == keys* and *added ⊆ vals*
  arithmetic identities. No tree can violate one without violating M3 first.
- **M14** — implied by M2. `removed` (token-set diff) and `hit` (textual scan) are both
  produced from the same backtick token regex over the same two texts, so `removed == keys`
  forces `hit == keys`.
- **M19** — cosmetic. `not m4bad` only suppresses M5's line when M4 already failed; M5's own
  content is `m5bad`, which cannot be non-empty when M4 failed on the same key. Verdicts are
  identical on all 8 controls (measured drift: ufo/S041 lose the M5 line, rc unchanged).
- **M27** — unreachable: `git ls-tree --name-only REV corpus/knowledge/` is non-recursive, so
  a nested knowledge file never enters `bfiles`; `corpus/knowledge/` holds 98 `.md` files, all
  direct children. **M28** — unreachable: `tracked` is empty only in a repo with zero tracked
  files (every control tree has 16,650).

Residual risk if a future scope breaks the premises: M04 needs a `corpus/` duplicate basename
(control **dup-basename** was built for exactly that shape and kills M02), M27 needs a
recursive listing, M28 needs an empty repo. None is a live escape.

## 4. Killed by the extended controls (12) — the isolating fixtures that were missing

`bash .ufo/waves/round-87/w1/MutC1Counter-receipts/MutC1Counter-controls-ext.sh <SCRATCH>`
(`MutC1Counter-controls-ext.txt`; pristine fails the named limbs, the mutant then passes).

| control | tree / map / target | pristine fail set | kills |
|---|---|---|---|
| target-degenerate | positive tree, frozen map, `--target 596/1720` | M1 | M20, M21 |
| s041-own-rate | S041-forge tree, forged map, `--target 679/1719` | M4,M5 | M03 |
| nofile-own-rate | positive tree minus `corpus/source-snapshots/round-25/S040.txt`, `--target 677/1719` | M4,M5 | M06 |
| extra-file | positive tree + uncited `corpus/knowledge/extra.md` | M3 | M16 |
| appended-line | positive tree + one prose line (no backticks) | M3 | M15 |
| range-out | fixture, 3-line snapshot, citation `S102.txt:4` | M5 | M17 |
| range-edge | fixture, 3-line snapshot, citation `S102.txt:3` (=EOF) | pass | M18 |
| dup-basename | fixture + tracked `corpus/sources/S102.txt` copy | pass | M02 |
| not-gone | fixture + `KASEGI_MIRROR` holding `S102.txt` (bare key resolves) | M4,M5 | M05 |
| quoted-key | fixture citing `` `S020.txt` `` (QUOTED) with its own target | M7 | M07 |
| dup-key-line | fixture, same key twice on one base line | pass | M13 |

## 5. Routed defects (re-runnable; the claim itself is not re-scored)

- **RD-1 (coverage, primary).** The frozen battery isolates only M6; M1/M2/M3 always co-fail,
  M4/M5 always co-fail, M7 never fails alone (sources: `controls/c1-controls-r87.txt`; §1).
  Consequence: 21 of 28 mutants survive it, including trivial ones (`allok` → True is caught,
  but `M1 := True`, `QUOTED := ∅`, `same_files := True`, `nlines + 1` all survive).
  Fix: add the 11 controls above to the next freeze's battery. Every row is measured, not
  proposed.
- **RD-2 (masking).** Forge controls in the frozen battery score the forged tree against the
  *frozen* target, so the forged map's own rate trips M1 and hides the limb under test:
  `S041-forge` fails M1 as well as M4 (measured). Fix: pass the forged tree's own rate as
  `--target` (controls `s041-own-rate`, `nofile-own-rate`) — this is what turns M03/M06 from
  survivors into kills.
- **RD-3 (qualifier, M7).** All three M7 mutants survive the frozen battery. `QUOTED := ∅` is
  invisible because M1 is exact; the two sub-clauses are each other's alibi. M7 is a redundant
  tripwire, not an independently verified limb — R13's "load-bearing" claim does not hold for
  it until `quoted-key` is added.
- **RD-4 (qualifier, misleading line).** `M5 = not m5bad and not m4bad` makes the frozen
  receipt print `LIMB M5 FAIL out_of_range=none` on ufo-copy and S041-forge — a range failure
  that does not exist. Readers of the freeze receipt can misattribute an anchor-range defect
  to those trees.
- **RD-5 (qualifier, aggregation).** `rate()` counts every class except GONE, while
  `resolve.py`'s own numerator is `RESOLVES + MIRROR-EQUIVALENT + INTERNAL` (resolve.py:457).
  Measured base scope: 1124 GONE, 574 INTERNAL, 22 RESOLVES → 596 either way, so the readings
  agree today (M26, `!= GONE` → `== INTERNAL`, is killed by the positive control only because
  of those 22 RESOLVES). An OTHER-class citation entering the knowledge scope would make the
  counter's rate exceed the resolver's; the claim's "reads resolve.py's own classification" is
  exact for the per-token classes but the aggregation is the counter's.
- **RD-6 (qualifier, dead clause).** `bcls.get(k) == "GONE"` is unfalsifiable on this host:
  every frozen run prints `mirror_absent=True` (`MIRROR_ROOT=~/Projects/the-bounty-hunter`
  does not exist) and every bare `S<digits>.txt` classifies GONE. It was only exercised by the
  `not-gone` fixture with `KASEGI_MIRROR` set. The claim's "GONE at base" therefore rides on
  an absent mirror, not on a measured resolution.

## 6. Restoration and hygiene

- Frozen counter sha256 before **and** after every run:
  `949f0625f02bbd2fcc05a9d7ddddc7e622137f5935f06d1a27be252e3fe927be`; map unchanged
  `7db928c7…8f1eaa`. No mutant was ever written over the frozen path — mutations live only in
  scratch; "restored bytes" is therefore the frozen file's own unchanged hash (printed at the
  head and tail of `MutC1Counter-controls-ext.txt`).
- Receipts carry sha256 digests, paths and limb lines only; fixtures use `aa/bb/cc` and
  `line1..3` byte content. No credential-shaped value was written at all: no
  `X-Amz-Security-Token`, no `AKIA`/`ASIA` key id (not even the AWS documentation example),
  no private-key header, no `token=`/`secret:` value. Scanned with
  `grep -REn 'X-Amz-Security-Token|AKIA|ASIA[A-Z0-9]{12,}|BEGIN .*PRIVATE KEY|token=…|secret:…'`
  over this directory: no matches.
- No lane file written outside `.ufo/waves/round-87/w1/MutC1Counter*`; scratch
  `/fast/scratch/hyaku/kasegi-r87/MutC1Counter` deleted on exit. Frozen `c1/`, `c2/`,
  `controls/` bytes, `corpus/` and the instruments were read-only; `corpus/instruments/__pycache__`
  predates this seat (mtime 2026-11-04) and was not rewritten.
- Tooling: none installed or upgraded.

## 7. Files written

- `.ufo/waves/round-87/w1/MutC1Counter.md` (this report)
- `.ufo/waves/round-87/w1/MutC1Counter-receipts/MutC1Counter-score-frozen.py` (self-building frozen-battery harness)
- `.ufo/waves/round-87/w1/MutC1Counter-receipts/MutC1Counter-frozen-battery.txt` (pristine, reproduces the frozen txt)
- `.ufo/waves/round-87/w1/MutC1Counter-receipts/MutC1Counter-frozen-matrix.txt` (28 mutants × 8 controls, raw)
- `.ufo/waves/round-87/w1/MutC1Counter-receipts/MutC1Counter-controls-ext.sh` (11 limb-isolating controls)
- `.ufo/waves/round-87/w1/MutC1Counter-receipts/MutC1Counter-controls-ext.txt` (their measured output)
- `.ufo/waves/round-87/w1/MutC1Counter-receipts/MutC1Counter-mutants.tsv` (the 28 exact single-point substitutions)
- `.ufo/waves/round-87/w1/MutC1Counter-receipts/MutC1Counter-mkmut.py` (table → mutant generator)

Verifier: `python3 -B .ufo/waves/round-87/w1/MutC1Counter-receipts/MutC1Counter-score-frozen.py .ufo/waves/round-87/c1/knowledge-meter.py <scratch>`
must print 8/8 expected verdicts with no drift; then
`bash .ufo/waves/round-87/w1/MutC1Counter-receipts/MutC1Counter-controls-ext.sh <scratch>`
must reproduce §4 line for line.
