# RevClosureSuite — round 35, wave 1

Seat item: review `corpus/instruments/r35-defect-closure.sh` — exactly seven checks D1–D7; every
check `bash -n`-parseable, `cd`-prefixed, read-only; every check exits nonzero while its defect is
open (suite on a scratch copy of the base tree → `closed=0/7`; on the tip → `closed=7/7`);
`--selftest` genuinely runs each check against a broken fixture (`r35-fixtures/D1..D7`); no vacuous
`echo` check can pass the selftest. Verdict with evidence.

## Report

All commands below ran with the lane repo at working-copy state; the suite bytes were FROZEN by the
author (ExecClosureSuite) before the definitive battery and re-verified at each step. Scratch root
`/fast/scratch/hyaku/kasegi-r35/RevClosureSuite/` (deleted before yield; verified absent).

### 0. Bytes reviewed (frozen)

```
sha256sum corpus/instruments/r35-defect-closure.sh
→ d7ad84384eb4b3fa2f5737e0597cbc9cdf3ded1eac867f6131886b790d38a304  (773 lines, mode 755)
bash -n corpus/instruments/r35-defect-closure.sh && echo OK
→ bash-n-whole=OK   (exit 0)
grep -c '^check_d[0-9]()' corpus/instruments/r35-defect-closure.sh
→ 7
```

Freeze announced by the author with this exact sha256 + line count. Three pre-freeze digests were
observed while the author was still editing (58ca3115…/643 ln, cba8c95b…/761 ln, 5fb0da5e…/772 ln);
no verdict in this receipt is based on them. Fixture set at freeze:
`r35-fixtures/fixtures.json` `b9a07afa1bed7b15b1754e7defee87cdb6233806d0b94b80d8a0acb4529da113`,
`r35-fixtures/README.md` `9bcb39cb5315abe0cd20f39599e03519542f4ae9936f01b4b0e0e80140b272d2` — both
match the digests the author announced.

### 1. Exactly seven checks, arrays aligned

Source (frozen bytes): `CHECK_IDS=(D1 D2 D3 D4 D5 D6 D7)`,
`CHECK_FNS=(check_d1 check_d2 check_d3 check_d4 check_d5 check_d6 check_d7)` — aligned 1:1; the only
`check_d*()` definitions are the seven; `run_plain` iterates `CHECK_IDS` and prints one
`D<i> check=<payload> open=0|1` line per defect plus `closed=K/7 exit=0|1`.

### 2. `bash -n` per check

Each check block (marker `# --- D<i> ---` to the next `# ---` marker) extracted and parsed
standalone:

```
D1: bash-n=0   D2: bash-n=0   D3: bash-n=0   D4: bash-n=0
D5: bash-n=0   D6: bash-n=0   D7: bash-n=0   (all exit 0)
```

### 3. `cd`-prefixed

Every check's first filesystem action is the same shape (D1 shown; identical ×7):

```bash
check_d1() { # [ROOT]
  local root=${1:-$LANE_ROOT}
  ( cd "$root" || { printf 'root-unreadable'; exit 2; }
    ...
```

Measured: `cd-first=True` for all seven (first non-`local` statement starts `( cd "$root" ||`).
A `cd` failure prints `root-unreadable` and exits 2 (harness error, counted open by `run_plain`).

### 4. Read-only

Static: write-token scan (`>>`, `sed -i`, `tee`, `touch`, `rm -`, `mv`, `git init`, `git add`,
`cp -`, `mkdir`, `chmod`) over each of the seven check blocks → **none**. Every write token lives in
the scratch builders (`copy_live` cp -p, `filter_out` tmp+mv, `build_mutant` mkdir/sed -i/printf >>,
`materialize` cp -a/git init/git add -A) and the `run_selftest` RETURN trap `rm -rf` — all confined
to `scratch=$(mktemp -d "$SCRATCH_BASE/r35-closure.XXXXXX")`, `SCRATCH_BASE=${KASEGI_SCRATCH:-…}`.
The plain run's one git invocation is `git ls-files` (D4, an index read) — the frozen header states
exactly this ("Its one git invocation is `git ls-files` (an index read, no git mutation …)").

Dynamic proof — a tar copy of the lane working tree (`.git`/`.jj` excluded), snapshot before, plain
run + `--selftest` run on the copy, snapshot after:

```
before-snapshot=95d94292666e1f7807012072445732823aaf89fcf5cb1b728927cc951f7558cd files=7175
plain-on-copy exit=1   selftest-on-copy exit=1
after-snapshot=95d94292666e1f7807012072445732823aaf89fcf5cb1b728927cc951f7558cd files=7175
READ-ONLY=PROVEN tree-byte-identical
```

Scratch removal on exit verified: after every selftest run, `ls $S/suite-scratch` → empty (the
RETURN trap fired each time).

### 5. Base-tree run — every check exits nonzero while its defect is open

`git archive 3266c9937b03062d9bbc2f436e20820115ed179c | tar -x` into scratch, then:

```
bash corpus/instruments/r35-defect-closure.sh --root <scratch>/base
D1 check=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0 open=1
D2 check=erratum-row=0,erratum-mean=0,row-bytes=1 open=1
D3 check=registry-r-defect-closure=0,registry-kill-rule=0 open=1
D4 check=tracked=0,provenance=0 open=1
D5 check=erratum-file=absent,discriminating-invocation=0,per-id-occurrences=0 open=1
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=0/7 exit=1
base-run exit=1
```

Each check reads open on its own clause, cross-checked against the base bytes directly:
`filled by the L1`=1 / `c1c6a5f`=0 in base SCORECARD.md; `round-34 depth:density row`=0,
`201.2`=0, and the stale-row regex
`^\| depth:density \| 9 \| mean \*\*201\.7\*\*, 25 blocks, 710 path-citation instances` matches the
real base bytes (count 1 — the D2 `row-bytes` clause is pinned to genuine base bytes, not a
transcription); SKILL.md registry counts 0/0; `wave1-results.json` absent at base;
`.ufo/waves/round-35/` absent; L1Integration dead-seat sentence=1, correction=0; QUALITY
supersedes rows 0/0.

### 6. Tip run at receipt time (mid-flight state, digests pinned)

```
bash corpus/instruments/r35-defect-closure.sh
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=0,provenance=1 open=1
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=4/7 exit=1
tip-run exit=1
```

D4 open is the designed index read: `wave1-results.json` is still untracked in the working copy
(`git status`: `?? .ufo/waves/round-34/wave1-results.json`; provenance note present,
`tracked=0,provenance=1`) and closes only on the L1's commit. D6/D7 open because those fixes had
not landed at receipt time (`grep -c 'Correction (round 35)' …/L1Integration.md` → 0;
`grep -c 'supersedes R22' corpus/QUALITY.md` → 0). Input digests at run time: SCORECARD.md
`51337bf1…`, SKILL.md `daeff71b…`, corpus/QUALITY.md `807cc714…`,
`.ufo/waves/round-34/wave1/L1Integration.md` `5472f60a…`,
`.ufo/waves/round-35/claims-erratum-d5.md` `2f4fae0a…`, `wave1-results.json` `3afa3581…`,
`wave1-results.json.provenance.md` `e1c44301…` (full digests in §11).

### 7. Green path on a fully-fixed tree (the tip-equivalent reading)

Materialized `r35-fixtures/clean` by the fixture README's own construction
(`cp -a …/. && git init -q && git add -A`) and run:

```
bash corpus/instruments/r35-defect-closure.sh --root <scratch>/clean-mat
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0
D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=2,per-id-occurrences=1 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
clean-run exit=0
```

And the committed two-defect control `r35-fixtures/two-defect/D1D2` (same construction):

```
D1 open=1, D2 open=1, D3–D7 open=0 → closed=5/7 exit=1   (exactly D1+D2 fail)
two-defect-run exit=1
```

The suite is neither always-reject nor blind to which limb broke.

### 8. `--selftest` on the live tree — fail-closed direction

```
KASEGI_SCRATCH=<scratch>/suite-scratch bash corpus/instruments/r35-defect-closure.sh --selftest
selftest case=D1 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D2 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D3 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D4 live=fail  fixture=rejected mutants=2/2 others=6/6 verdict=fail
selftest case=D5 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D6 live=fail  fixture=rejected mutants=0/2 others=6/6 verdict=fail
selftest case=D7 live=fail  fixture=rejected mutants=0/2 others=6/6 verdict=fail
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=3 control-failures=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=short-report rejected=1
selftest judge=fake-suite rejected=1 path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0
selftest judge=fake-plain rejected=1 output=closed=7/7 exit=0
selftest problem=self-report status=1
selftest-live exit=1
```

Every fixture rejection names its own clause (detail lines quoted in the full run, e.g.
`selftest detail=D4 fixture reason=tracked=0,provenance=0`,
`selftest detail=D5 fixture reason=erratum-file=present,discriminating-invocation=2,per-id-occurrences=0`);
all mutants of the four closed checks isolate (`mutants=n/n`); the D6/D7 mutant legs read
`verdict=unexpected rc=1` — correct mid-flight behavior, not a defect: mutants are built from the
live bytes, where the correction/supersedes clauses are still open, so isolation is not yet
attributable; the fixture leg already rejects on the right clause. The judge rejected all four
forgery shapes and the committed do-nothing control (`.ufo/waves/round-35/c1-controls/fake-suite.sh`
`292aaac0…`, verified by reading it: prints `cases=7 failures=0` / `closed=7/7 exit=0`, performs no
check).

### 9. `--selftest` green path

Scratch copy of the frozen instrument with `LANE_ROOT=` repointed to the materialized `clean` tree
(that tree also carries the round-35 fake control at
`.ufo/waves/round-35/c1-controls/fake-suite.sh` so the judge's fake leg runs), `r35-fixtures`
symlinked beside the copy:

```
KASEGI_SCRATCH=<scratch>/suite-scratch bash <scratch>/green/r35-green.sh --selftest
selftest case=D1 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D2 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D3 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D4 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D5 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D6 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D7 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=short-report rejected=1
selftest judge=fake-suite rejected=1 path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0
selftest judge=fake-plain rejected=1 output=closed=7/7 exit=0
selftest judge=complete-report accepted=1
selftest-green exit=0
```

16/16 clause mutants isolated, both controls pass, the honest report is accepted by the suite's own
judge (this exercises the `reason=.*<clause>` form the fixture seat had fixed pre-freeze).

### 10. Vacuous-echo mutation battery — the discriminator

For each check: the check body replaced by its closed-payload `printf` + `exit 0` (a vacuous echo),
run as a scratch copy against the green tree with the real fixtures symlinked:

```
D1: case=D1 live=pass fixture=pass mutants=0/3 others=6/6 verdict=fail  → cases=7 failures=1 control-failures=1, exit 1
D2: case=D2 live=pass fixture=pass mutants=0/3 others=6/6 verdict=fail  → cases=7 failures=1 control-failures=1, exit 1
D3: case=D3 live=pass fixture=pass mutants=0/2 others=6/6 verdict=fail  → cases=7 failures=1 control-failures=0, exit 1
D4: case=D4 live=pass fixture=pass mutants=0/2 others=6/6 verdict=fail  → cases=7 failures=1 control-failures=0, exit 1
D5: case=D5 live=pass fixture=pass mutants=0/2 others=6/6 verdict=fail  → cases=7 failures=1 control-failures=0, exit 1
D6: case=D6 live=pass fixture=pass mutants=0/2 others=6/6 verdict=fail  → cases=7 failures=1 control-failures=0, exit 1
D7: case=D7 live=pass fixture=pass mutants=0/2 others=6/6 verdict=fail  → cases=7 failures=1 control-failures=0, exit 1
ALL-MUTATIONS-CAUGHT=True
```

A vacuous echo passes live but cannot pass the selftest: the fixture leg requires rejection
(`fixture=rejected` in `report_ok`'s case-line regex) and the mutant leg requires nonzero exit with
clause attribution. For D1/D2 the committed two-defect control adds a second layer
(`control-failures=1`: the control requires exactly D1+D2 to fail). Companions:

- always-exit-1 mutant (D1 body → open payload + `exit 1`): `case=D1 live=fail … verdict=fail`,
  `cases=7 failures=7 control-failures=1`, exit 1 — an always-failing check also poisons every
  `others=6/6` leg and the clean control.
- summary-only selftest body (`printf 'selftest cases=7 failures=0'; return 0`):
  `selftest problem=self-report cases=0 expected=7`, exit 1.
- summary-only plain body (`printf 'closed=7/7 exit=0'; return 0`):
  `suite problem=self-report plain-lines=0 expected=7`, exit 1.

### 11. Fixture inspection (limb states, measured from the committed trees)

| tree | D1 ph/cor | D2 er/mean/row | D3 rdc/krc | D4 res/prov/gitignore | D5 disc/occ | D6 stale/corr | D7 r22/r23 |
|---|---|---|---|---|---|---|---|
| D1/  | 1/0 (broken) | 1/1/1 | 1/1 | T/T/– | 2/1 | 0/1 | 1/1 |
| D2/  | 0/1 | 0/0/1 (broken) | 1/1 | T/T/– | 2/1 | 0/1 | 1/1 |
| D3/  | 0/1 | 1/1/1 | 0/0 (broken) | T/T/– | 2/1 | 0/1 | 1/1 |
| D4/  | 0/1 | 1/1/1 | 1/1 | T/F/ignores results path (broken) | 2/1 | 0/1 | 1/1 |
| D5/  | 0/1 | 1/1/1 | 1/1 | T/T/– | 2/0 (broken) | 0/1 | 1/1 |
| D6/  | 0/1 | 1/1/1 | 1/1 | T/T/– | 2/1 | 1/0 (broken) | 1/1 |
| D7/  | 0/1 | 1/1/1 | 1/1 | T/T/– | 2/1 | 0/1 | 0/0 (broken) |
| clean/ | 0/1 | 1/1/1 | 1/1 | T/T/– | 2/1 | 0/1 | 1/1 |
| two-defect/D1D2/ | 1/0 + 0/0/1 (both broken) | — | 1/1 | T/T/– | 2/1 | 0/1 | 1/1 |

Every broken limb is broken on its own clause; every other limb carries fixed content; `two-defect/`
is nested one level down so a `D?` glob never picks it up as a case (per `r35-fixtures/README.md`).
The fixture README honestly records its limits (pinned excerpts, not full-file copies; D2's
row-bytes is an exact-prefix grep; no fixture proves base bytes are not deleted — that stays a
git-diff reading on the lane).

### 12. Unplanned scratch-base demonstration

First selftest attempt ran with a nonexistent `KASEGI_SCRATCH` subdir:

```
mktemp: failed to create directory via template '…/r35-closure.XXXXXX': No such file or directory
selftest problem=scratch-base path=…
selftest judge=forged-summary rejected=1 … (all four forgery lines still printed)
selftest problem=self-report status=2
selftest-live exit=1
```

The harness-error path is fail-closed too (exit 2 → judge rejects the empty report → exit 1).

## Verdict

**The instrument meets every criterion in the seat item.** Exactly seven checks D1–D7
(§1); every check `bash -n`-parseable (§2), `cd`-prefixed (§3), read-only — proven dynamically by a
byte-identical 7175-file tree snapshot across plain + selftest runs, with scratch confined to
`KASEGI_SCRATCH` and removed on exit (§4); every check exits nonzero while its defect is open —
base-tree run `closed=0/7 exit=1` with each check open on its own clause (§5), and per-clause
mutants isolate the nonzero exit to the reopened clause (§8–§9); the tip-equivalent green reading
`closed=7/7 exit=0` measured on the materialized `clean` fixture and `closed=5/7 failed=D1,D2` on
the two-defect control (§7); `--selftest` genuinely runs each check against the committed broken
fixtures `r35-fixtures/D1..D7` — fixture rejections are clause-attributed, the other six checks must
pass on the same tree (`others=6/6`), and both committed controls are part of the selftest (§8–§9,
§11); **no vacuous `echo` check can pass the selftest** — proven by mutation for all seven checks
(`fixture=pass` → `verdict=fail`, exit 1), plus always-fail and summary-only forgeries rejected by
`report_ok`/`plain_report_ok`/the judge, and by the committed do-nothing control being rejected
(§10, §8).

## Findings

No blocking defect. Observations, in severity order:

1. **(low, residual — no action required this round)** D1 greps only the `filled by the L1` and
   `<LANE_HASH>` placeholder spellings. The round-34 spotcheck's D1 also named the other spelling
   ("**Final lane commit: the L1 fills this line in the closing commit.**", `SCORECARD.md:1129` at
   `c1c6a5f`); that spelling is not matched. Measured at the current tip: `grep -c 'fills this
   line' SCORECARD.md` → 0 — no live blind spot today, and the frozen claim's kill rule defines the
   contract this check implements (`filled by the L1` count 0 + `c1c6a5f` citation). If a future
   round reintroduces the other spelling, D1 passes while a placeholder remains — the
   spelling-brittle residue the spotcheck warned about (R1 class, recurs).
2. **(cosmetic)** `--root DIR` is silently ignored under `--selftest` (the selftest always measures
   `LANE_ROOT`). The usage text does not document the combination; no wrong output is possible
   because the selftest's report names what it measured.
3. **(note)** Default scratch base is `${KASEGI_SCRATCH:-${TMPDIR:-/tmp}}`; trees are small and
   removed on exit (trap verified, §4). My runs pinned `KASEGI_SCRATCH` under the seat scratch per
   the round rules.

## Residual risk / verification gaps

- The two live-tree green readings in claim C1 — `closed=7/7 exit=0` and `--selftest cases=7
  failures=0` on `LANE_ROOT` — were **not measurable at receipt time**: D4's tracked clause reads
  the git index and closes only on the L1's commit, and the D6/D7 fixes had not landed
  (`grep -c 'Correction (round 35)'` → 0, `grep -c 'supersedes R22'` → 0; digests in §6). The
  equivalent green path was measured on the materialized `clean` fixture with the same checks and
  the suite's own construction (§7, §9). The L1 should run the two counting commands on the landed
  tree before claiming C1 green.
- The instrument was frozen mid-wave; any revision re-baselines this review (the author committed
  to announcing new digests). Digest reviewed: `d7ad84384eb4b3fa2f5737e0597cbc9cdf3ded1eac867f6131886b790d38a304`.

## Provenance

| file | sha256 |
|---|---|
| corpus/instruments/r35-defect-closure.sh (reviewed, frozen) | d7ad84384eb4b3fa2f5737e0597cbc9cdf3ded1eac867f6131886b790d38a304 |
| corpus/instruments/r35-fixtures/fixtures.json | b9a07afa1bed7b15b1754e7defee87cdb6233806d0b94b80d8a0acb4529da113 |
| corpus/instruments/r35-fixtures/README.md | 9bcb39cb5315abe0cd20f39599e03519542f4ae9936f01b4b0e0e80140b272d2 |
| .ufo/waves/round-35/c1-controls/fake-suite.sh | 292aaac048c9cacff081c24b54fd71fc67a86d3c6ab6845398e0e2856c5be121 |
| SCORECARD.md (at tip run) | 51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7 |
| SKILL.md (at tip run) | daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc |
| corpus/QUALITY.md (at tip run) | 807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8 |
| .ufo/waves/round-34/wave1/L1Integration.md (at tip run) | 5472f60ab33a2241e7051c071e1469ca89b2c874e571d93420499cd0998a0fd5 |
| .ufo/waves/round-35/claims-erratum-d5.md (at tip run) | 2f4fae0a4ce0ed4120888ae0ed4340d43810c356bdd35609783fd08cdb2233e5 |
| .ufo/waves/round-34/wave1-results.json (at tip run) | 3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4 |
| .ufo/waves/round-34/wave1-results.json.provenance.md (at tip run) | e1c4430133adeb58b8d3b3af9edcb49739eacd3f40536dca529105c609e86c98 |

Base commit archived for §5: `3266c9937b03062d9bbc2f436e20820115ed179c` (claims-freeze
`617496b9c6e92bc671e7e78b83df69a04470d0e9`; working HEAD at dispatch `da2d3c687f82a9814ee71c91c930cb733050d37c`).
No tools were installed (none needed). No subagents spawned. Scratch
`/fast/scratch/hyaku/kasegi-r35/RevClosureSuite/` deleted after this receipt was written; verified
absent (`ls` exit 2) before yield.

---

# RE-BASELINE — re-cuts `a4f80067…` and final `0ae4b484…` (supersedes the digest in §0–§12)

The author re-cut the instrument twice after my first battery, both times announcing the digest.
§0–§12 remain the evidence record for `d7ad8438…`; this section re-baselines every criterion on the
final bytes. No check semantics changed in any revision (author's statement; verified by re-run).

## R0. Final bytes

```
sha256sum corpus/instruments/r35-defect-closure.sh
→ 0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f
wc -l → 834 ; tail -c 20 | od -c ends `U S " \n` → newline-terminated, 834 lines
bash -n → exit 0 ; grep -c '^check_d[0-9]()' → 7 ; mode 755
```

(Correction recorded: my first footnote claimed "no trailing newline" from a Python
`count('\n')+1`; the author's `od -c` disproved it and my own `tail -c 1` check confirms
`ends_with_newline=yes` — the +1 was my arithmetic error, not a file property. Quoting 834.)

Re-cut chain: `d7ad8438…` (773 ln) → `a4f80067…` (834 ln) → `0ae4b484…` (834 ln, final). Changes,
all traceable to review findings: (1) `--selftest` now honours `--root` — the live tree under test
is `RD_ROOT`, mutant builders copy from it (`copy_live` reads `$RD_ROOT/$rel`), and the fake-suite
probe looks in the tree under test first, then the lane control dirs (my observation 2 → fixed);
(2) D1's prose-placeholder residue is now a header paragraph "Documented limit (not a live blind
spot)" — measured 0 at base and tip, recorded not hidden (my observation 1 → documented);
(3) D5 gained a third mutant `-erratum-file` marked `cascade` (RevSelftestFixtures' finding);
(4) header miscount "sixteen mutants in all" corrected to seventeen — the clause table has 17
clauses (D1:3 D2:3 D3:2 D4:2 D5:3 D6:2 D7:2), every clause one mutant.

## R1. Static battery on the final bytes

All seven check blocks: `bash -n` exit 0, first FS action `( cd "$root" ||`, write-token scan none.
Mutant inventory counted from `mutant_specs`: D1 3, D2 3, D3 2, D4 2, D5 3 (one `cascade`), D6 2,
D7 2 — **17 total**, matching the corrected header.

## R2. Functional runs on the final bytes

```
--root <git archive 3266c99>  → closed=0/7 exit=1  (every check open on its own clause; payloads
identical to §5)
(no arg, live tip)            → closed=4/7 exit=1  (D4 tracked=0/provenance=1; D6
dead-seat-sentence=1/correction-round-35=0; D7 supersedes-R22=0/R23=0 — unchanged at receipt-update
time: grep 'Correction (round 35)' → 0, grep 'supersedes R22' → 0)
--root <materialized clean>   → closed=7/7 exit=0
--root <materialized two-defect/D1D2> → closed=5/7 exit=1, exactly D1+D2 open (own exit measured: 1)
```

## R3. `--selftest` green path — now the frozen CLI, no sed patch

```
KASEGI_SCRATCH=<scratch>/suite-scratch bash corpus/instruments/r35-defect-closure.sh \
  --root <materialized r35-fixtures/clean> --selftest
selftest case=D1 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D2 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D3 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D4 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest detail=D5 mutant=erratum-file reason=erratum-file=absent,discriminating-invocation=0,per-id-occurrences=0 cascade=1
selftest case=D5 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D6 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D7 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=short-report rejected=1
selftest judge=fake-suite rejected=1 path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0
selftest judge=fake-plain rejected=1 output=closed=7/7 exit=0
selftest judge=complete-report accepted=1
exit=0
```

17/17 mutants: 16 satisfy the closed-other-clauses rule (`isolate_ok`), 1 (D5 `-erratum-file`) is
the cascade probe credited on `erratum-file=absent`. The fake-suite probe fell back to the lane's
round-35 control (the clean tree carries no fake) — the fallback path works.

## R4. `--selftest` on the live tree (fail-closed direction, final bytes)

`cases=7 failures=3 control-failures=0`, exit 1, naming exactly D4/D6/D7 (live=fail,
fixture=rejected on the right clause); D1/D2/D3/D5 pass with mutants n/n isolated; both controls
pass; all five judge forgery lines rejected. (D6/D7 mutant legs still read `verdict=unexpected` —
correct mid-flight, resolves when their fixes land.)

## R5. Read-only proof on the final bytes

Tar copy of the lane working tree, snapshot → plain run + `--selftest` on the copy → snapshot:

```
before=57db26e4fb6ac21e44cada7ae975d5831a021598ee31ac6acd80b90706189af4 files=7198
plain exit=1 ; selftest exit=1
after=57db26e4fb6ac21e44cada7ae975d5831a021598ee31ac6acd80b90706189af4 files=7198
READ-ONLY=PROVEN tree-byte-identical
```

## R6. Vacuous-echo mutation battery on the final bytes — 10/10 caught

Same construction as §10 but with the frozen CLI (`--root <clean> --selftest`, no sed):

```
D1 vac: case=D1 live=pass fixture=pass mutants=0/3 others=6/6 verdict=fail → failures=1 control-failures=1, exit 1
D2 vac: case=D2 live=pass fixture=pass mutants=0/3 others=6/6 verdict=fail → failures=1 control-failures=1, exit 1
D3 vac: case=D3 live=pass fixture=pass mutants=0/2 others=6/6 verdict=fail → failures=1 control-failures=0, exit 1
D4 vac: case=D4 live=pass fixture=pass mutants=0/2 others=6/6 verdict=fail → failures=1 control-failures=0, exit 1
D5 vac: case=D5 live=pass fixture=pass mutants=0/3 others=6/6 verdict=fail → failures=1 control-failures=0, exit 1
D6 vac: case=D6 live=pass fixture=pass mutants=0/2 others=6/6 verdict=fail → failures=1 control-failures=0, exit 1
D7 vac: case=D7 live=pass fixture=pass mutants=0/2 others=6/6 verdict=fail → failures=1 control-failures=0, exit 1
D1 always-exit-1: case=D1 live=fail fixture=rejected mutants=0/3 verdict=fail → failures=7 control-failures=1, exit 1
selftest body → printf summary: selftest problem=self-report cases=0 expected=7, exit 1
plain body  → printf summary: suite problem=self-report plain-lines=0 expected=7, exit 1
ALL-MUTATIONS-CAUGHT=True
```

## R7. New finding on the final digest (filed to both owners)

`corpus/instruments/r35-fixtures/README.md` (revised to
`c7261c745e60812824a430574b42766a1e3f2193fea30c29e9e866e6e3547e55`; `fixtures.json` unchanged
`b9a07afa…`) Limits bullet still reads "**The `erratum-file=absent` clause has no fixture and no
mutant.** … the two D5 mutants … a suite change that stopped testing the erratum file's existence
would not be caught by this set." Stale on the "no mutant" half against the re-cut: `mutant_specs`
D5 carries `'-erratum-file' 'erratum-file' 'cascade'` and R3 credits it. The "no fixture" half
stays true (no committed fixture breaks that limb; the lane-level absent-file direction is the
base-tree run). Owner: ExecSelftestFixtures; cause: the suite re-cut landed after the README
revision. Severity: low (prose; the suite's own selftest proves the mutant exists). Messaged
ExecClosureSuite and ExecSelftestFixtures with this digest.

ExecSelftestFixtures (owner) fixed it: README now 86 lines, `6d99ba915272f9424f3d9fb9cc56fbfd6b2fb34c3c3c60c3037d991ef6562563`,
reworded to "**The `erratum-file=absent` clause has no fixture.** … The clause *is* covered by the
suite's own scratch mutant (D5 `-erratum-file`, printed with `cascade=1` …), so this set's gap is
the committed fixture only." — verified against the landed bytes (digest + text read back). The
owner also independently re-ran the final suite bytes (`--selftest` on a LANE_ROOT-redirected
scratch copy) → `cases=7 failures=0`, byte-identical report to their `a4f80067…` run — the re-cut
changed no verdict. **Finding closed.**

## R7b. Peer finding cross-referenced (verified by this seat, no action taken on the file)

SimplifierCleanup-3's YAGNI sweep found three dead assignments (shellcheck SC2034) in the
instrument: `open` (run_plain — declared `local … closed=0 open` at line 495, assigned 501/507,
never read: the printf branches use literal `open=0`/`open=1` strings), `oout` (others-loop, line
692, only `$?` consumed), `cout` (both control loops, lines 764/790, only `$?` consumed). Verified
against the final digest `0ae4b484…` by this seat (grep lines quoted above) — the trio is real,
non-blocking, style-class. Their 6-hunk patch (8 lines removed / 6 added) is inlined in
`.ufo/waves/round-35/wave1/SimplifierCleanup.md` §1.3, measured byte-identical on four paths
(green `--root clean --selftest`, base `3266c993`, live root, two-defect root); they also proved by
a 26-tree discrimination matrix (9 fixture trees + 17 clause mutants, all exact singletons) that no
two checks test the same fact and all 9 fixture trees are load-bearing. The instrument is
ExecClosureSuite's file — patch application is the author's/L1's call; this seat takes no action on
it. Does not change the R8 verdict.

## R8. Re-baseline verdict

**The final instrument `0ae4b484…` meets every criterion in the seat item** — same evidence shape
as §Verdict, now with: `--root` honoured by `--selftest` (green path = frozen CLI), the D1
prose-placeholder residue documented in the header, 17 mutants (16 isolate + 1 cascade) all
credited, and the vacuous-echo/always-fail/summary-only mutation battery 10/10 caught. Both of my
§Findings observations are dispositioned (2 → fixed in code; 1 → documented as a measured limit,
agreed to belong in the lesson as R1-class residue — the L1 owns that call).

Residual risk unchanged from §Residual risk: the two live-tree green readings in claim C1
(`closed=7/7 exit=0`, `--selftest cases=7 failures=0` on `LANE_ROOT`) remain unmeasurable at
receipt-update time (D4 closes on the L1's commit; D6/D7 fixes not landed — grep counts 0). The
green path is measured on the materialized `clean` fixture with the frozen CLI (R3). The L1 runs
the two counting commands on the landed tree before claiming C1 green.

## R9. Provenance (final)

| file | sha256 |
|---|---|
| corpus/instruments/r35-defect-closure.sh (FINAL, reviewed) | 0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f |
| corpus/instruments/r35-fixtures/fixtures.json (unchanged) | b9a07afa1bed7b15b1754e7defee87cdb6233806d0b94b80d8a0acb4529da113 |
| corpus/instruments/r35-fixtures/README.md (R7 finding FIXED by the owner; chain 9bcb39cb… → c7261c74… → 6d99ba91…) | 6d99ba915272f9424f3d9fb9cc56fbfd6b2fb34c3c3c60c3037d991ef6562563 |
| ExecClosureSuite receipt (re-filed by the author after my R7 finding was cross-referenced into their §10; earlier announced digest f8f99970c581eb89cccd77cb25f32b0f5d8956f03f855bd002e5cd3551b33367) | 0b0e0abefaf47fff8b668a701dde2d625d140ab605ce14d03313097badb44ee3 |

Scratch `/fast/scratch/hyaku/kasegi-r35/RevClosureSuite/` deleted again after this section was
written; verified absent before yield.
