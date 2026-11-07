# MutC2Counter — round-94 C2 counter mutation probe

**Seat:** mutation tester, leaf (no delegation). **Lane:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin` — read-only; no git/jj mutation was made in the lane. All mutation work happened in `/fast/scratch/hyaku/kasegi-r94/MutC2Counter`, which was removed at the end (`10-restoration.txt`).

**State probed.** C2 landing `996460861d4130ddb2da6b7554e905d3e47504a3` (freeze `96b5033f4dfa8d6605c13e0c9aad458be3cd7df3`, C1 landing `d51220aeb4a538b7b211bb2629e83210669cd56d`), on a fresh clone whose `git rev-parse --show-toplevel` was asserted equal to the clone directory before the first forgery commit. Pins re-measured at the landing:

| object | sha256 |
|---|---|
| `.ufo/waves/round-94/c2/capability-check.py` (frozen counter) | `7619ea9464c53a84b5f9c3f409ffbf3482754ee35648d0632486fca55fb1d076` |
| `corpus/instruments/capture-secret-scan.py` (candidate) | `22ba32d145f90f7759caf16d3ee524eb1779153d3f2a33611675a93a4667beaf` |
| `corpus/instruments/claim-package-check.py` (gate) | `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` |
| `.ufo/waves/round-94/c2/candidate-row.txt` | `4f10e273f3c27e5b43cec77b280071d13284c3c475e976ac160bb674ca4beed8` |

**Protocol.** Seven mutants, each committed on top of the landing in its own fresh clone of the pristine clone. Every clone's `rev-parse --show-toplevel` was asserted before the first commit, and every mutant's `--selftest` was run and had to exit 0 before the commit, so the unpinned runs exercise the detector, not a broken selftest. The frozen counter then ran as

```
python3 -B .ufo/waves/round-94/c2/capability-check.py --lane <clone> --rev HEAD --work <scratch> \
    --gate-sha256 8b6f84… [--instrument-sha256 22ba32…] --seed {1,9191}
```

`pinned` = both frozen sha256 pins; `unpinned` = gate pin only (the instrument pin omitted). Thirty-two runs plus one default-seed baseline; every stdout is committed under `MutC2Counter-receipts/runs/`.

## Baseline (re-derived here, not copied from the freeze)

| run | result | key limb values |
|---|---|---|
| pinned, seed 1 (nonce `bc0d93a0`) | pass rc 0 | all K1–K9 pass; K3 `scanned=2224 hits=0 allowed=24 unused_allow=0`; K4 `missing=none extra=none files_ok=True`; K9 `prev_hits=39 lost=none prev_caught_new=none`; K7 `missing=none extra=none`; K8 `clauses=61 failing=none`; K5 `rows=1` |
| pinned, seed 9191 (nonce `3a69ac7f`) | pass rc 0 | same, `seed=9191` |
| unpinned, seeds 1 and 9191 | pass rc 0 | identical limb values |
| pinned, printed run-time seed `1745964395` (nonce `cf4de1ca`) | pass rc 0 | same; completes P1's three-seed clause |

P2 holds (instrument and gate shas above). P3 holds: the landing commit changes exactly `SCORECARD.md` and `corpus/instruments/capture-secret-scan.py`, and line 307 of `SCORECARD.md` at the landing is byte-identical to `candidate-row.txt` (`diff` rc 0). P4's required line `C2-CONTROLS-RESULT pass controls=10` is printed by the frozen receipt with all ten `CONTROL … PASS`; the enumeration of those ten is wrong (defect D2 below).

## Mutants

`unpinned` is the detector-level verdict; `pinned` adds K1, whose instrument pin rejects every byte change. All runs at seeds 1 and 9191 produced the same limb set.

| # | mutant (smallest behaviour-bearing change) | expected detector | observed, unpinned (both seeds) | pinned | verdict |
|---|---|---|---|---|---|
| F1 | `scan_rev()` (line 311) scans only paths shaped `corpus/source-snapshots/r[0-9a-f]{8}/[0-9a-f]{12}\.(txt\|json)` — a detector keyed on the relocated plant shape | K4 exactness and K7 (generated paths are not that shape) | rc 1; FAIL K2,K3,K4,K9,K7,K8 (K1 pass). K2 `rc=0 sts_files=0`; K3 `scanned=0 unused_allow=23`; K4 `missing=23 extra=0`; K9 `lost=21`; K7 `missing=17 extra=0`; K8 17 clauses | +K1 | **KILLED** |
| F2 | `main()` returns the clean summary when `--lane`/`--files` contains the counter's work-dir prefix `c2check-` | K4/K7 (their repositories live under `c2check-*`), K9 | rc 1; FAIL K4,K9,K7,K8; **K2 and K3 pass**. K4 `missing=44 extra=0`; K9 `lost=39`; K7 `missing=17 extra=0`; K8 35 clauses | +K1 | **KILLED** |
| F3 | drop the round-91 `cloudfront-signed-cookie-signature` shape and its 7 selftest cases (selftest stays green) | K4, K9 (planted old shape), K7, K8 | rc 1; FAIL K4,K9,K7,K8. K4 `missing=4`; K9 `lost=4`; K7 `missing=2`; K8 4 clauses | +K1 | **KILLED** |
| F4 | `gldt-[A-Za-z0-9_-]+` (any length) and its 2 length negatives deleted | K4 exactness (19/21-character negatives), K7 generated negative | rc 1; FAIL K4,K7,K8. K4 `extra=2`; K7 `extra=1` (`live-n17`); K8 2 clauses; K9 pass | +K1 | **KILLED** |
| F5 | `glpat-[A-Za-z0-9_-]{3,}` (any 3+ tail) and its 4 length negatives deleted | K3 (real receipts), K4 exactness, K7 generated negatives | rc 1; FAIL K3,K4,K7,K8. K3 `hits=15 files=15`; K4 `extra=3`; K7 `extra=3`; K8 3 clauses; K9 pass | +K1 | **KILLED** |
| F6 | `patterns()` mines `b"0123456789abcdefghij"` from `open(__file__)` and adds it as a `gitlab-pat` pattern (11 contradicting selftest cases deleted so K1 stays green) | K3 and K4 shape exactness; K7 shows run-time values defeat literals | rc 1; FAIL K3,K4,K8. K3 `hits=5 files=5`; K4 `extra=10` (the runner/deploy plants now also report `gitlab-pat`); K8 3 clauses; **K7 and K9 pass** | +K1 | **KILLED** |
| F7 | `gate_patterns()` drops the gate's old `session-cookie` shape | none exists for an unplanted shape | **rc 0; all nine limbs pass** — K3 clean, K4 `missing=none extra=none`, K9 `lost=none`, K7 clean, K8 61/0, K5 rows=1 | K1 only (pin) | **SURVIVOR** |

Notes that matter for the claim:

- F1 is the relocation probe. The relocated shape carries no shape information (the 12-hex basename is `sha256(nonce|path)[:12]`, counter lines 503–524), so a detector that gates on that shape finds only the source-snapshot plants and loses every practice-evidence and `-receipts` plant: K4 `missing=23`, K9 `lost=21`, K7 `missing=17`. The statement's M93-4 clause ("a path-shape-keyed detector finds nothing") is re-derived.
- F2 is sharper than the shipped `F2-harness-gated` control: gating on `__file__` (the shipped control) also suppresses K2/K3; gating on the fixture lane path passes K2 and K3 and is still caught by K4, K7, K8, K9. The harness prefix therefore leaks, but cannot be exploited without losing the fixture limbs.
- F3 isolates K9: because the shape is planted, K9's `lost` set is non-empty (4 pairs) and K4/K7/K8 fail independently.
- F6 measured the actual own-source content: the instrument's source contains only its *selftest* fixtures, never a K4 plant literal (the K4 literals live in the counter, not the instrument). Using them as a table corrupts the selftest (11 cases had to be deleted) and still fails K3/K4/K8; K7 and K9 pass, which is why the run-time-generated fixtures are the anti-literal detector.
- F5's 15 K3 hits are pre-existing receipt files under `.ufo/waves/round-92/` and `round-93/` that contain short `glpat-` fragments; the clean-scan limb catches the relaxation before the fixture limbs do.

## K9: can a scanner lose an old shape and still pass?

**Yes, when no plant exercises the shape — and K9 cannot see it; no, when the shape is planted.** The mechanism is explicit in the counter:

```python
new94 = {(relocate(p0[0], nonce), p0[1]) for p0 in ROUND94_SHAPES}   # line 643
lost = phits - hits                                                   # line 644
caught_new = phits & new94                                            # line 645
ok = rcp == 1 and not lost and not caught_new
```

`phits` and `hits` are both measured over the same K4 plant repository. K9 is a relative regression check on *planted* hits; it is not a shape-coverage check.

- Planted old shape: F3 drops `cloudfront-signed-cookie-signature`; K9 prints `lost=` four pairs (two `…/evidence/…json`, two `source-snapshots/r…/*.txt`, one `w/…-receipts/live-…txt`) and fails, as do K4, K7 and K8.
- Unplanted old shape: F7 drops the gate's `session-cookie` shape (`gate_patterns()`, line 231). The counter passes rc 0 at both seeds with `K4 missing=none extra=none`, `K9 lost=none`, `K7` clean. A micro-probe proves the loss is real: on a one-line fixture `w/x-receipts/live-s.txt` = `session-cookie: abcdefghijklmnopqrstuvwxyz`,
  - pristine candidate: `HIT shape=session-cookie … rc=1`
  - round-93 landing instrument (`9225954a…`): `HIT shape=session-cookie … rc=1`
  - F7 instrument: `hits=0 … rc=0`

So the frozen fixture certifies the six *planted* shapes and loses the other gate shapes silently. `op-ref`, `bearer`, `authorization` and `session-cookie` all have zero occurrences in the counter's `PLANTS` and `generated()` texts (`05-unplanted-gate-shapes.txt`), and the instrument's selftest covers only the gate's `private-key` shape.

## Routed defects (no claim re-score)

- **D1 (coverage, new this probe).** Four of the six gate `SECRET_PATTERNS` shapes have no K4 plant and no K7 generated case. A regression that drops `op-ref`, `bearer`, `authorization` or `session-cookie` from the scanner passes K1–K9 (F7, both seeds, rc 0). Round 95 could add one plant per gate shape, or a K4 limb that derives the expected shape set from `gate_patterns()` instead of a hand-written expectation table. This does not contradict the frozen C2 statement (it claims the three GitLab shapes and the retained earlier shapes, not a gate-shape-set invariant), so C2 is not re-scored.
- **D2 (claim-package prose, from P4).** P4's parenthetical — repeated in `claims.json`'s `controls` field — names “the S140-allowlist-removed control”, but the executed receipt contains no such control; its tenth control is `tampered-instrument`. The required line `C2-CONTROLS-RESULT pass controls=10` and every executed control hold, so this is a description defect, not a limb failure (`02-frozen-controls.txt`).

## Verdict

STANDS — C2 P1/P2/P3 and P4's required result line were re-derived here on a fresh clone at `996460861d4130ddb2da6b7554e905d3e47504a3` (pinned baseline rc 0 at seeds 1, 9191 and the printed run-time seed `1745964395`; K1–K9 pass), and six of seven forged detectors are killed unpinned by the frozen counter (F1 K2/K3/K4/K7/K8/K9; F2 K4/K7/K8/K9; F3 K4/K7/K8/K9; F4 K4/K7/K8; F5 K3/K4/K7/K8; F6 K3/K4/K8), with the pinned runs additionally killed by K1's sha256 pin. The one SURVIVOR (F7, the unplanted gate shape `session-cookie`) and the P4 enumeration defect are routed as D1/D2; neither re-scores a frozen claim limb and no claim was narrowed, re-labelled or edited.

## Receipts

Directory: `.ufo/waves/round-94/w1/MutC2Counter-receipts/`. Every cited command's output is stored there; scratch (`/fast/scratch/hyaku/kasegi-r94/MutC2Counter`) was deleted after the copies.

| receipt | command | observed |
|---|---|---|
| `00-environment-and-pins.txt` | `sha256sum` on instrument, gate, counter, candidate, row; `git rev-parse HEAD`; `diff` landed row vs `candidate-row.txt` | rc 0; four pins as above; clone toplevel = clone dir; `row_diff_rc=0` |
| `01-p3-landing-pathset.txt` | `git show --name-status 9964608…`; `git show --stat` | rc 0; exactly `M SCORECARD.md`, `M corpus/instruments/capture-secret-scan.py` (2 files, +47/−14) |
| `02-frozen-controls.txt` | `grep -n '^CONTROL\|^C2-CONTROLS' .ufo/waves/round-94/controls/c2-controls-r94.txt`; `grep -c s140` | rc 0; 12 grep lines (header + 10 `CONTROL…PASS` + result); `s140` occurrences 0 |
| `03-k9probe.log` | `python3 k9probe.py` over the one-line `session-cookie` fixture with pristine / F7 / round-93 instruments | rc 0; 14 lines: `HIT … rc=1`, `hits=0 … rc=0`, `HIT … rc=1` |
| `04-k9probe-fixture.txt` | `git -C <fixture> log --stat`; `cat` of the one-line fixture | rc 0; fixture toplevel = fixture dir |
| `05-unplanted-gate-shapes.txt` | `grep -c` for `op://`, `Bearer`, `session-cookie`, `authorization=`, `BEGIN` in the counter | rc 0; counts `0,0,0,0,1` (only `private-key` planted) |
| `06-matrix.tsv` | aggregated matrix from `driver.py` (case × mode × seed × rc × failed limbs × K4/K7/K9 details) | 33 lines (header + 32 runs) |
| `07-driver.log` | `python3 driver.py` (8 cases; 32 counter runs, 6 concurrent) | rc 0; 40 lines; 6/7 mutants rejected, F7 rc 0 |
| `08-patches.txt` | `git diff HEAD~1 -- corpus/instruments/capture-secret-scan.py` per mutant | 7 patches, anchors asserted unique at apply time |
| `09-mutant-summary.txt` | parser over `results.json`: per-run limb statuses and missing/extra/lost/failing counts | 34 lines; the counts quoted in the mutant table |
| `10-restoration.txt` | lane `git rev-parse HEAD`, `sha256sum`, `git status --porcelain` before cleanup; `test ! -e $S` after `rm -rf` | HEAD `99646086…`; instrument `22ba32d1…`; counter `7619ea94…`; gate `8b6f8493…`; `dirty_count=0` for instrument/gate/c2; scratch absent |
| `runs/` (56 files) | raw stdout of every counter run (baseline pinned/unpinned × seeds 1, 9191, plus the printed-seed baseline), every mutant run (pinned/unpinned × 2 seeds), every `--selftest` preflight, and every patch/meta | each run's `LIMB` lines and `CAPABILITY-CHECK-RESULT` are the source of the table above |

Baseline runs cited: `runs/baseline.pinned.1.txt` (11 lines, rc 0), `runs/baseline.pinned.9191.txt` (11 lines, rc 0), `runs/baseline.pinned.default.txt` (11 lines, rc 0, printed seed `1745964395`). Mutant runs cited: `runs/{F1…F7}.{pinned,unpinned}.{1,9191}.txt`.
