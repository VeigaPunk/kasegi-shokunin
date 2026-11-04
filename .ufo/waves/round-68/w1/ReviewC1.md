# ReviewC1 — round 68 C1 independent reproduction

**Verdict: VERIFIED (frozen predicate reproduces from committed bytes, 8/8, exit 0) — with FINDINGS: the refusal is spelling-exact, and the same program-execution classes still run through the abbreviated spellings `--compress-prog`/`--compress` and through default textconv on `git show <commit>`. These findings sit outside the eight frozen measurements, so they don't defeat the frozen predicate. They do contradict the target's prose claim that the gate "executes neither named program". L1 adjudicates.**

Raw receipts: `.ufo/waves/round-68/w1/ReviewC1/` (candidate.txt, base.txt, selftest.txt, ledger.txt, mutbat.txt, adversarial.txt, adv.py, adv2.py).
Scratch: `/fast/scratch/hyaku/kasegi-r68/ReviewC1/` (removed before yield). Every input byte came from `git archive 82b3b7d…`. The working tree supplied only the real ledger/root and the mutbat script. The seat spec names those, and the counter itself reads them from `--lane`.

## 1. Export and pins
```
S=/fast/scratch/hyaku/kasegi-r68/ReviewC1; mkdir -p $S/export $S/final $S/base
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 82b3b7d4704e914eb224e7bb24e57aa9cbd8603f corpus/instruments .ufo/waves/round-68/controls | tar -x -C $S/export
sha256sum $S/export/corpus/instruments/figure-audit.py $S/export/.ufo/waves/round-68/controls/*.py
10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8  .../export/corpus/instruments/figure-audit.py
8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247  .../export/.ufo/waves/round-68/controls/base-gate-d0f48405.py
785e38fd1393f345226fbd34e3a2310eed597bb7b95997478066db158c496b4b  .../export/.ufo/waves/round-68/controls/c1-probe-run-r68.py
```
- Gate = pin `10c87100…` ✔. Base gate = pin `8147350c…` ✔. **The counter bytes equal the pin `785e38fd…`** ✔. The working-tree copies of the counter and the gate hash to the same values.
- `git rev-parse HEAD` = `82b3b7d4704e914eb224e7bb24e57aa9cbd8603f`. `git diff --stat 82b3b7d HEAD -- corpus/instruments .ufo/waves/round-68/controls` printed nothing.

## 2. Frozen counter, candidate (all nine lines)
```
cd $S && TMPDIR=$S python3 -B $S/export/.ufo/waves/round-68/controls/c1-probe-run-r68.py --gate $S/export/corpus/instruments/figure-audit.py --work /fast/scratch/hyaku/kasegi-r68/ReviewC1/final --mode candidate
MEASURE sort-compress-refused ok rc=2 marker_runs=0
MEASURE git-textconv-refused ok rc=2 marker_runs=0
MEASURE read-only-controls-admitted ok controls=5 failed=0
MEASURE selftest ok selftest cases=77 failures=0 rc=0
MEASURE mutbat ok rc=0 mutbat killed=5/5 survivors=0 invalid=0 controls=pass
MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 rc=0
MEASURE red-fixture ok rc=1
MEASURE no-write-side-effect ok fixture_changed=0 marker_runs=0
VERIFY measurements=8 failures=0 gate_sha256=10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8 mode=candidate
exit=0
```
These lines match the committed `controls/c1-candidate-trial-r68.txt` byte for byte (compared visually, all 9 lines).

## 3. Frozen counter, base (do-nothing control)
```
python3 -B .../c1-probe-run-r68.py --gate $S/export/.ufo/waves/round-68/controls/base-gate-d0f48405.py --work $S/base --mode base
MEASURE sort-compress-refused FAIL rc=1 marker_runs=18288
MEASURE git-textconv-refused FAIL rc=1 marker_runs=1
MEASURE selftest FAIL selftest cases=73 failures=0 rc=0
MEASURE no-write-side-effect FAIL fixture_changed=0 marker_runs=18289
VERIFY measurements=8 failures=4 gate_sha256=8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247 mode=base
exit=1
```
The other four measurements read `ok` (full output is in `ReviewC1/base.txt`). The lines match the committed `controls/c1-base-donothing-r68.txt` exactly.

## 4. Independent re-derivation (without the counter)
```
G=$S/export/corpus/instruments/figure-audit.py
python3 -B $G --selftest                      -> selftest cases=77 failures=0   (exit=0)
python3 -B $G --ledger /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit-ledger.json --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
                                              -> FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0   (exit=0)
python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit-mutbat.py --instrument $G
                                              -> mutbat killed=5/5 survivors=0 invalid=0 controls=pass   (exit=0)
```
All four new selftest cases pass:
```
selftest case=sort-compress-program-refused exit=2 want=2 verdict=pass
selftest case=sort-compress-program-space-refused exit=2 want=2 verdict=pass
selftest case=sort-compress-program-quoted-refused exit=2 want=2 verdict=pass
selftest case=git-show-textconv-refused exit=2 want=2 verdict=pass
```

## 5. Findings (adversarial probes beyond the frozen measurements)
These probes ran on the exported candidate gate, using the counter's own `build_fixture`/`probe` imported read-only. The script is in `ReviewC1/adv.py` and `adv2.py`, and the output is in `ReviewC1/adversarial.txt`. Host tools: `/usr/bin/sort` is `sort (GNU coreutils) 9.12`; git is `2.56.0`.

`denied_flag()` (figure-audit.py:301-311) matches only `tok == flag` or `tok.startswith(flag + "=")`. GNU getopt_long accepts any unambiguous prefix of a long option.

**F1 (HIGH): the program-execution class is still reachable through sort by abbreviation.**
```
ADV rc=1 comp_runs=18288 tc_runs=0 derive='sort --compress-prog=$W/compressor.sh -S 1K big.txt | head -n 1'
ADV rc=1 comp_runs=18288 tc_runs=0 derive='sort --compress=$W/compressor.sh -S 1K big.txt | head -n 1'
ADV rc=1 comp_runs=18288 tc_runs=0 derive='sort --compress $W/compressor.sh -S 1K big.txt | head -n 1'
```
The gate admits all three at parse time, and the compressor really runs 18288 times each, the same count as the base. The target's "executes neither named program" holds only for the three exact spellings that the measurements test.

**F2 (HIGH): textconv runs without `--textconv`.** `git show <commit>` (a patch, not a blob) applies textconv by default. The gate admits it and the config-declared driver runs:
```
ADV rc=1 comp_runs=0 tc_runs=1 derive='git show HEAD | wc -l'
```
So the git half of the repair is flag-shaped and doesn't close the class. Counter control 5 (`git show HEAD:big.txt`) does not catch this, because blob display does not apply textconv by default. Precondition: the repo config must declare the driver, while `.gitattributes` is in tracked bytes.

**F3 (MEDIUM, existed before this repair; a write class): sort `--output` by abbreviation.**
```
ADV rc=1 written_exists=True derive='sort --outp=written.txt big.txt'
```
The gate admitted the derive, and sort created `fixture/written.txt`. The round-60 refusal of `-o/--output` has the same prefix hole.

**Negative results:** git's own abbreviations are refused by git itself, so neither ran a program:
```
ADV rc=1 tc_runs=0 derive='git show --textc HEAD:big.txt'  reason=derive-upstream-exit-128
ADV rc=1 derive='git show --ext-d HEAD | wc -l'            reason=derive-upstream-exit-128
```
The exact spellings `git show --textconv` and `--ext-diff` are refused at parse time (rc=2, `reason=derive-not-read-only`).

## 6. Residual risk and verification gaps
- The frozen predicate is VERIFIED, but measurements 1 and 2 test one exact spelling each, and measurement 8 inherits that limit. F1 and F2 show that the instrument move is narrower than the target's prose. A sound fix would be one of these: prefix-match long flags (any `tok` with `len>=3` that is a prefix of a denied long flag, plus its `=` form), and for git show refuse unless `--no-textconv`/`--no-ext-diff` is present; or allow-list the flags instead of deny-listing them. That's an L1/next-round decision, and I didn't change anything.
- I didn't probe other getopt-sensitive heads (`grep`, `ls`, `cut`, `git cat-file --textconv`/`--filters`), sort's `--files0-from`, or `--random-source`. Per the docstring, `git cat-file` is on the allow-list, and `git cat-file --textconv`/`--filters` are a likely analogue of F2. **Not run, unverified.**
- No tools were installed or upgraded.
