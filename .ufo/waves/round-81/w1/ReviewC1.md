# ReviewC1 — round-81 C1 adversarial review (recheck-cwd successor + r81 counter)

Seat: ReviewC1-6 (reviewer, leaf). Scope: diff corpus vs candidate, the seven new checks,
the r81 counter (mutbat.py), build-table.py, the frozen 59-row table, r80 routing docs
(MutC1Hunt.md, ReviewC1.md), verdict/clean_pass forgery reasoning. Frozen bytes read only;
no lane file outside the wave dir written.

Frozen-hash check (all match claims.json): candidate `a3b58aa5…dbec0`; mutbat `fa96223b…43b4`;
table `abcc834eb21102f11a11cc91b7482f68957f988ea91e68e803a82251a216d095`;
r80 candidate `420151fd…5698`; r80 table read for (e). P1/P3/P8 executed once each over the
frozen bytes; receipts in `ReviewC1-receipts/`.

## Executed

- **P1**: `TMPDIR=<scratch> python3 -B <candidate> --selftest` → rc 0, `selftest cases=22
  failures=0`, 0 stderr bytes, wall 1.25 s (p1-selftest.out).
- **P3**: full battery → rc 0, 66 s, `MUTBAT target_sha256=a3b58aa5… baseline=ok rows=59
  killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3`; 59 MUTANT lines:
  55 KILLED + 1 EXCEPTION-KILL (K-M3, counted=yes) + 3 NEUTRAL-OK (p3-battery.out).
- **P8**: `mutbat --selftest` → rc 0, `mutbat selftest ok`, T-MIS counted=no, T-NEUBAD
  NEUTRAL-BROKEN, both toy forgeries exit 1 (p8-mutbat-selftest.out).
- **Table provenance**: `build-table.py` regen over the candidate is JSON-identical to the
  frozen table (regen-table.json); every anchor occurs exactly once (`not_unique=[]`).
- **Survivor-vs-row comparison (d)**: for 24 of the 26 MutC1Hunt-sourced new rows,
  `r80candidate.replace(anchor, replacement)` equals the routed survivor file byte-for-byte
  (survivors/S01…S43.py); M1/M2 match the ReviewC1.md:19/26 descriptions exactly
  (`isdir`→`exists`, `return -1`→`return 0`). Five rows differ textually but equivalently
  (m2 below). One row differs in substance: **S07 — see Major 1**.
- **Orphan check (c)**: 11 process samples over ~52 s around the runs: every in-flight
  `sleep 30` had etimes ≤ 1 s and a distinct live parent (concurrent seats running the same
  battery); none persisted past the 1 s timeout kill (orphan-sleep-sample.txt). The
  `exec sleep 30` child is killed by `subprocess.run`'s timeout; the timeout-bucket case
  costs ~1 s of the 1.25 s selftest.

## Findings

### Blocker
None. P1, P3, P8 hold on the frozen bytes; the table regenerates identically; all 28 old
rows' kill_cases equal the case names after `->` in their frozen r80 `expect` prose (K-M4
and K-M8 name two checks each — both listed, no mismatch, (e) clean).

### Major
- **S07 row kills a different transform than the routed survivor it is named after; the
  routed survivor is still open.** The frozen row (mutant-table.json:355-357,
  build-table.py:51) mutates the census site:
  `def census(root, lane, verbose=False):` → `verbose=True` (candidate census.py:115). The
  routed r80 survivor (MutC1Hunt.md:74 "S07 | verbose defaults to True") instead mutated
  **main()**'s default — survivors/S07.py:100 census default is still `False`, :557 reads
  `root, lane, verbose = ".", DEFAULT_LANE, True`. Falsified: applying the survivor's
  actual transform to the r81 candidate (`…DEFAULT_LANE, False` → `…True`, candidate
  census.py:718) and running `--selftest` exits **0** with `selftest cases=22 failures=0`
  (S07-routed-transform-selftest.out, mutant in receipts). The output-lines check's
  negative limb only inspects direct `census()` captures (`_t1`, census.py:593-604); no
  assertion observes a main()-driven verbose run, so verbose-by-default through the CLI
  remains unasserted. Impact: none on the verdict (P3 passes; the frozen row itself is a
  valid kill of the previously-unasserted census-site default — S07 verdict=KILLED
  counted=yes), but build-table.py:7's "the round-80 routed real-gap survivors" and the
  C1 statement's "including 28 round-80 routed survivors the landed r80 bytes let
  through" (claims.json:16) are inaccurate for S07: 27 of 28 rows kill the routed
  transform; row S07 kills a same-line, different-site mutant while the routed transform
  survives the successor selftest. Route: correct the row's `expect` provenance wording at
  the next freeze opportunity and carry the main-site verbose default as an open r82 gap.

### Minor
- **m1 — 10 of the 36 routed r80 real-gap survivors have no frozen row and no r81 check**:
  S03 (unsorted glob), S06 (DEFAULT_LANE), S18 (consumed() arity), S24 (selftest scratch
  cleanup), S29 (summary format), S32 (leftover limb), S33 (capture stdout restore), S36
  (F0 fallback), S38 (tmpdir-parent None-parent limb), H27 (fresh-cwd fixture
  neutralisation) — MutC1Hunt.md:113-131 themes vs the 26 ids the table takes. The claim
  does not assert these closed; they remain routed r82 defects (not executed here; absence
  is from the table id set).
- **m2 — five rows' replacement is textually different from the survivor bytes but
  behaviourally equivalent on the selftest** (same site, same mechanism, all KILLED in P3):
  S19/S20 (survivor deletes the print; row writes `pass`), S21 (survivor `if False:` keeps
  the print; row `…or code == 2:` + `pass`), S14 (parenthesization only), S39 (survivor
  passes `os.path.abspath(root)` as lane; row passes `root` — identical because main
  already abspaths root and all fixtures use absolute roots). Provenance note only.
- **m3 — P3 alone cannot certify real assertions (f).** verdict() (mutbat.py:82-93) counts
  any rc≠0, no-Traceback run whose FAIL lines name a kill case; clean_pass (mutbat.py:77)
  only pins the pristine run. A forgery whose kill signal is a semantic self-check — e.g. a
  hash of an alpha-renamed, comment-stripped AST — would pass the baseline, pass all three
  neutrals (NT1/NT3 are comment-only, NT2 is a local rename; only comment-insensitive pins
  are excluded), and emit case-matched FAIL lines for all 56 assertion mutants. Among the
  five committed forgery shapes none survives: F1/F3/F5 miskilled or neutral-broken, F2
  neutral_ok=1/3 (its body-after-sentinel hash tolerates NT1 only), F4 baseline=bad
  (controls/c1-forgeries-r81.txt). So: no, a target cannot pass P3 with a byte pin or any
  committed stub shape — the neutral rows are the pin-breaker — but P3 can in principle be
  passed without real assertions by a neutral-immune semantic pin; only P2 (byte pin at
  landing) closes that residuum. P3 is correctly claimed as tally-independence, not
  assertion-existence.
- **m4 — build-table.py:16 `OLD` is a cwd-relative path**: the builder only runs from the
  lane root (FileNotFoundError from the fleet root). Cosmetic; the frozen table is already
  generated and regen-identical.
- **m5 — run_selftest merges stderr into the parsed text** (mutbat.py:58-67): a mutant
  printing a fake `selftest case=… FAIL` line on stderr influences verdicts. Theoretical
  only (the merge is what catches tracebacks); no known exploit shape.

## (a)–(f) verdicts

- **(a)** All seven new checks assert their comment's contract with exact count/line
  equality and are each the declared kill case of ≥1 frozen row (prefix-literal S01/S02;
  conform-limbs S04/S05/S37; tmpdir-file M1; timeout-bucket M2; tmpdir-unset S25;
  usage-guards S30/S31/S39; output-lines S07/S19/S20/S21/S22) — non-vacuous: P3 shows every
  such row KILLED counted=yes on exactly that check. Only weakness: output-lines pins
  verbosity on the census() path, not main() (Major 1).
- **(b)** Every state-touching new check restores in `finally` on all paths: case 16 TMPDIR
  + sys.stderr (census.py:517-531), case 17 TIMEOUT (:541-546), case 18 TMPDIR (:553-561),
  case 19 sys.stderr (:569-574); stdout only via capture(), which restores in its own
  finally. Clean.
- **(c)** Timeout-bucket wall ≈1 s (P1 total 1.25 s); `exec sleep 30` killed at the 1 s
  timeout, no orphan (52 s of process sampling; before/after pgrep deltas were concurrent
  seats' in-flight runs).
- **(d)** 27/26-S-rows + M1/M2 derive exactly; S07 does not (Major 1); five equivalent-text
  variants noted (m2).
- **(e)** No mismatch: all 28 old rows' kill_cases = the `->`-named checks in the frozen
  r80 expect prose.
- **(f)** Answered in m3: byte pins and all five committed forgeries are rejected by the
  r81 tally alone; a semantic (alpha-renaming-robust) self-pin is the theoretical P3 pass
  without real assertions — closed at landing only by P2.

## Verification gaps
P4 not re-run (committed receipt read and found consistent; ~10 min runtime). The ten m1
survivors were not re-run against the successor (absence established from the frozen table).
No tools installed; commands run: diff, sha256sum, python3 -B (candidate selftest, mutbat
battery+selftest, build-table regen, survivor-comparison and mutant-falsification scripts),
grep -n, ps/pgrep sampling. Scratch /fast/scratch/hyaku/kasegi-r81/ReviewC1 deleted after
receipts were copied.
