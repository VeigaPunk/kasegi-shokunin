# MutC1Hunt — round-83 C1 mutant hunt (depth:verifiability, coverage)

Round 83, attempt 1 — one v1 wave of 13 seats. Seat: MutC1Hunt (mutation tester, leaf).

Frozen inputs (read-only; no lane byte was modified):

| file | sha256 |
|---|---|
| `.ufo/waves/round-83/c1/recheck-cwd-census.py` | `343b21e46d4107fd81456840b7547b514283541bbe6fc2fface1da1adece08c9` |
| `.ufo/waves/round-83/c1/mutbat.py` | `2f7c49d44bb1f21e8286d1a8b54d4c57bccc0be990fd7946a57813db0d81cb7d` |
| `.ufo/waves/round-83/c1/mutant-table.json` | `5b1d99f59cede6cffa36d554ce7e8256bf1eba1cb84a9591bfbb9f7f386b6f44` |
| `w1/MutC1Hunt-rows.json` (this hunt) | `733aa5ff700ec6ee7f805f42d830be7e705ce164c78df960524cfec284e954e7` |

## Method

One 21-row table (20 non-neutral single mutants + 1 neutral control), built beyond the 67-row
frozen table, covering the four assigned areas: `conform_ok`, the `census()` verbose path,
the `main()` argument parser, and the production targets of the three round-83 checks
(bucket-other, bucket-over, main-verbose) including the canonical `RECHECK-CWD` summary that
reports `exit_other`. Every row is a single string replacement on bytes copied from the
frozen candidate; the candidate itself was only ever read.

Counter invocation (exactly as tasked, one battery per nonce, `~29 s` each):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
TMPDIR=/fast/scratch/hyaku/kasegi-r83/MutC1Hunt \
python3 -B .ufo/waves/round-83/c1/mutbat.py \
  --target .ufo/waves/round-83/c1/recheck-cwd-census.py \
  --table /fast/scratch/hyaku/kasegi-r83/MutC1Hunt/rows.json \
  --expect-cases 27 --work /fast/scratch/hyaku/kasegi-r83/MutC1Hunt/w
```

Run 1 (random nonce `aedc7c3fff2b42ff`, D3 row `MUT-AP-verbose-as-lane`) and run 2
(`--seed 00000000000000b2`, D3 row `MUT-SUM-swap-exit1-other`) produced **identical
verdicts**: `baseline=ok rows=21 killed=8 survived=12 miskilled=0 dirty=0 notderived=0
neutral_ok=1/1 decoy=ok decoy_hidden=20/20 target_sha256=343b21e4…`, counter exit 1. The
non-zero exit is the finding (survivors), not a counter fault: no MISKILLED, DIRTY or
NOT-DERIVED row occurred, the baseline was clean (`selftest cases=27 failures=0`), and all
three keyed decoys (D1, D2 unparse/rename + D3 single-anchor comment) passed on both nonces.
Receipts: `MutC1Hunt-receipts/mutbat-run1.out`, `mutbat-run2.out`.

## Verdicts (all 21 rows)

`failed_cases` is what the counter observed on the mutant's own selftest; a survivor is
`rc=0 selftest cases=27 failures=0` (clean run, no assertion fired).

| # | row | area | transform (one line) | verdict | observed |
|---|---|---|---|---|---|
| 1 | MUT-CF-noprefix-ge | conform_ok | `noprefix == 0` → `>= 0` | **SURVIVED** | rc=0, 27/0 |
| 2 | MUT-CF-noprefix-ne1 | conform_ok | `noprefix == 0` → `!= 1` | **SURVIVED** | rc=0, 27/0 |
| 3 | MUT-CF-exit2-ge | conform_ok | `exit2_foreign == 0` → `>= 0` | KILLED | conform-limbs |
| 4 | MUT-CF-norecheck-ge | conform_ok | `norecheck == 0` → `>= 0` | KILLED | conform-limbs |
| 5 | MUT-CF-restoration-ge | conform_ok | `restoration_only == 0` → `>= 0` | KILLED | gate-consume |
| 6 | MUT-BO-le | conform_ok | bucket equality → `<= entries` | KILLED | bucket-over,bucket-sum |
| 7 | MUT-BO-plus-one | conform_ok | bucket equality → `<= entries + 1` | KILLED | bucket-over,bucket-sum |
| 8 | MUT-EO-double | census exit_other | `exit_other += 1` twice | KILLED | bucket-other,prefix-census,timeout-bucket |
| 9 | MUT-EO-exit7-as-exit1 | census exit codes | `elif code == 1:` → `code in (1, 7)` | KILLED | bucket-other,prefix-census |
| 10 | MUT-MV-verbose-only-noprefix | census verbose | `verbose or noprefix` → `verbose and noprefix or noprefix` | KILLED | main-verbose |
| 11 | MUT-MV-drop-noprefix-pass | census verbose | prefix-less **passing** entries lose ENTRY | **SURVIVED** | rc=0, 27/0 |
| 12 | MUT-MV-extra-nonzero | census verbose | `code == 2` → `code != 0` (default mode widens) | **SURVIVED** | rc=0, 27/0 |
| 13 | MUT-MV-timeout-label | census ENTRY format | `foreign_exit=%d` prints `timeout` for code<0 | **SURVIVED** | rc=0, 27/0 |
| 14 | MUT-AP-root-no-value | main parser | drop `i + 1 < len(argv)` on `--root` | **SURVIVED** | rc=0, 27/0 |
| 15 | MUT-AP-lane-no-value | main parser | drop `i + 1 < len(argv)` on `--lane` | **SURVIVED** | rc=0, 27/0 |
| 16 | MUT-AP-verbose-as-lane | main parser | `--verbose` accepted by the `--lane` branch | **SURVIVED** | rc=0, 27/0 |
| 17 | MUT-AP-root-no-abspath | main parser | `census(os.path.abspath(root), …)` → `census(root, …)` | **SURVIVED** | rc=0, 27/0 |
| 18 | MUT-AP-selftest-last | main parser | `"--selftest" in argv` → `argv[-1] == "--selftest"` | **SURVIVED** | rc=0, 27/0 |
| 19 | MUT-SUM-swap-exit1-other | summary / bucket-other | print exit_other value under the exit1 label | **SURVIVED** | rc=0, 27/0 |
| 20 | MUT-SUM-other-as-norecheck | summary / bucket-other | print `norecheck` in the exit_other slot | **SURVIVED** | rc=0, 27/0 |
| 21 | MUT-NEU-comment | neutral control | trailing comment on `i = 1` | NEUTRAL-OK | rc=0, 27/0 |

Per-row selftest transcripts: `MutC1Hunt-receipts/selftest-out/<row>.out`.

## Survivors: mutant / expected detector / observed / verdict

All 12 survivors change observable behaviour; none is an equivalence. The only
semantics-preserving transform in the table is the neutral control (#21, NEUTRAL-OK).
Witness pairs are reproduced by `MutC1Hunt-repro.py` (12/12 pairs differ, exit 0); raw
outputs in `MutC1Hunt-receipts/witness.txt` and `witness.json`.

**#1 MUT-CF-noprefix-ge / #2 MUT-CF-noprefix-ne1 — noprefix conformance limb has no
isolating fixture. SEVERE.**
Expected detector: `conform-limbs` (or a new case) over a tree whose *only* defect is a
prefix-less entry. Observed: `--root one --lane one` over one `recheck: true` entry →
pristine `rc=1 RECHECK-CWD-RESULT nonconformant`; both mutants `rc=0 … conformant`. #2 needs
two prefix-less entries (`noprefix=2`) because `!= 1` still rejects a single one. Every
nonconformant fixture in the selftest fails the noprefix limb *together with* exit2/norecheck/
restoration, so the limb can be deleted or mis-bounded and all 27 cases stay green. The
round-83 G1–G4 additions do not touch this limb.

**#19 MUT-SUM-swap-exit1-other / #20 MUT-SUM-other-as-norecheck — the canonical
`RECHECK-CWD` summary is never parsed. SEVERE (silent misreport).**
Expected detector: a case that reads the summary fields, not the returned dict. Observed on
`--root mix --lane mix` (exit1_foreign=2, exit_other=1): pristine
`… exit1_foreign=2 exit_other=1 …`; #19 prints `exit1_foreign=1 exit_other=2`; #20 prints
`exit_other=0`. `bucket-other`/`bucket-sum` assert the *dict* (`got23["exit_other"] == 1`),
and no case matches `RECHECK-CWD entries=`, so the printed numbers can lie while the counter
still exits conformant.

**#11 MUT-MV-drop-noprefix-pass — default-mode ENTRY for prefix-less *passing* entries is
unasserted. MEDIUM.**
Expected detector: `output-lines`. It asserts `ENTRY b-relative.md … foreign_exit=2` (a
prefix-less *exit-2* entry) but never `c-bare-pass.md` (prefix-less, exit 0), although the
round-81 docstring promises ENTRY for a prefix-less entry. Observed: `--root one --lane one`
(default) → pristine prints `ENTRY c-bare.md noprefix=1 foreign_exit=0`; mutant prints no
ENTRY line (summary unchanged).

**#14 MUT-AP-root-no-value / #15 MUT-AP-lane-no-value — parser value guards untested.
MEDIUM.**
Expected detector: `usage-guards`. It tests only `--bogus`; a trailing `--root`/`--lane` is
never passed. Observed: `./cand --root` → pristine `rc=2`, stderr `usage: …`; mutant
`rc=1`, `Traceback … IndexError` on `argv[i + 1]`. Same for `--lane`. A harness that probes
with a missing value gets a crash instead of the documented exit 2.

**#16 MUT-AP-verbose-as-lane — flag/order misparse untested. MEDIUM.**
Expected detector: `usage-guards`/`main-verbose` with a non-final flag. Observed:
`./cand --verbose --root mix --lane mix` → pristine `rc=0` with ENTRY lines for every entry;
mutant consumes `--root` as the lane value, then rejects `mix` with `rc=2 usage:`. Every
fixture passes `--verbose` last, so the guarded branch hides the bug.

**#17 MUT-AP-root-no-abspath — `os.path.abspath` on `--root` is unpinned. LOW.**
Expected detector: `usage-guards` (it only uses absolute fixture roots). Observed from
`cwd=fx`: `--root nosuch --lane nosuch` → pristine
`recheck-cwd: no corpus/knowledge under /fast/scratch/…/fx/nosuch`; mutant prints the
relative `… under nosuch` (both rc=1). Only the message path differs.

**#18 MUT-AP-selftest-last — `--selftest` position sensitivity. LOW (battery is blind by
construction: `mutbat` always invokes `--selftest` as the last/only argument).**
Expected detector: `usage-guards` with `["--selftest", "--verbose"]`. Observed: pristine
`rc=0 selftest cases=27 failures=0`; mutant `rc=2 usage:`.

**#12 MUT-MV-extra-nonzero — contract-silent output widening. LOW (no action required
unless the output set is meant to be exact).** Default mode gains
`ENTRY q1-exit1.md noprefix=0 foreign_exit=1`, `…q2…`, `…r-exit7.md … foreign_exit=7` on
`mix`; the written contract only requires silence for a prefixed *passing* entry, so this is
permitted-but-unpinned output.

**#13 MUT-MV-timeout-label — contract-silent render change. LOW (cosmetic).** With
`TIMEOUT=1` and `--verbose` over a hanging entry: pristine `foreign_exit=-1`; mutant
`foreign_exit=timeout`. No case emits an ENTRY line with a negative code, so the rendering is
free.

## Routed gaps (re-runnable)

Reproducer (rebuilds fixtures + the 12 mutant copies in a temp dir; reads only the frozen
candidate and `MutC1Hunt-rows.json`):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
TMPDIR=/fast/scratch/hyaku/kasegi-r83/MutC1Hunt \
python3 -B .ufo/waves/round-83/w1/MutC1Hunt-repro.py
```

- **G-1 (SEVERE, #1/#2):** add a noprefix-only conformance limb: a tree with one prefix-less
  passing entry (`recheck: true`) must yield `rc=1` / `RECHECK-CWD-RESULT nonconformant`, and
  a two-entry (`noprefix=2`) variant must also fail (pins `== 0`, not `!= 1`).
- **G-2 (SEVERE, #19/#20):** assert the exact `RECHECK-CWD entries=… exit1_foreign=… exit_other=…`
  field values (or parse the line) on a fixture with `exit1_foreign=2 exit_other=1`; the dict
  assertions cannot see a misprinted summary.
- **G-3 (MEDIUM, #11):** assert `ENTRY c-bare.md noprefix=1 foreign_exit=0` in default mode over
  a one-entry prefix-less fixture (the passing counterpart of `b-relative.md`).
- **G-4 (MEDIUM, #14/#15):** `main(["…", "--root"])` and `main(["…", "--lane"])` must return 2
  with the usage line on stderr, empty stdout and no traceback.
- **G-5 (MEDIUM, #16):** `main(["…", "--verbose", "--root", R, "--lane", L])` must be verbose
  (ENTRY for a prefixed passing entry) and exit 0; also pins that `--verbose` is order-free.
- **G-6 (LOW, #17):** a relative `--root` without `corpus/knowledge` must report the absolute
  path (`os.path.abspath`) in the SystemExit message.
- **G-7 (LOW, #18):** either assert `--selftest` wins regardless of position, or invoke the
  battery with a trailing argument so the position cannot regress unnoticed.
- **G-8 (LOW, #12/#13):** decide the output contract: pin the exact ENTRY set for a mixed tree
  (kills #12) and a negative-code ENTRY rendering (kills #13), or record both as allowed.
  Until then the battery cannot distinguish them from a defect.

## Counter health / kill-rule evidence

- Baseline clean on both runs: `selftest cases=27 failures=0`, rc 0, no FAIL line, no
  traceback (`mutbat-run*.out`, `baseline=ok`).
- Decoys: D1/D2 keyed per run plus D3 single-anchor comment; `decoy=ok decoy_hidden=20/20` on
  both nonces, with different D3 rows chosen (`MUT-AP-verbose-as-lane`, then
  `MUT-SUM-swap-exit1-other`), so the 12 survivors are not decoy artifacts and the keyed
  nonce is doing its job.
- Kill rule sane: the 8 KILLED rows each fail a declared kill case (`conform-limbs` ×2,
  `gate-consume`, `bucket-over`+`bucket-sum` ×2, `bucket-other`+`prefix-census` ×3); no
  MISKILLED, no DIRTY, no NOT-DERIVED.
- Neutral control NEUTRAL-OK; no equivalence transform other than the neutral was needed.

## Restoration evidence

- The frozen candidate was never written: sha256 `343b21e4…` before run 1 and after run 2;
  `mutbat` reports the same `target_sha256`; each mutant ran from a copy under
  `/fast/scratch/hyaku/kasegi-r83/MutC1Hunt/` that the counter removed.
- `git status --porcelain .ufo/waves/round-83/c1/` shows no modification of the frozen C1
  bytes (the only untracked entry is `w1/`).
- Scratch `/fast/scratch/hyaku/kasegi-r83/MutC1Hunt/` is deleted before this seat yields;
  nothing cited here lives only there (all receipts copied below).
- Tooling: no installs; python3 stdlib only; no pacman transaction (host-wide pause
  respected).

## Files written

- `.ufo/waves/round-83/w1/MutC1Hunt.md` (this report)
- `.ufo/waves/round-83/w1/MutC1Hunt-rows.json` (21-row table; 20 non-neutral + neutral)
- `.ufo/waves/round-83/w1/MutC1Hunt-repro.py` (12-gap reproducer)
- `.ufo/waves/round-83/w1/MutC1Hunt-receipts/mutbat-run1.out`
- `.ufo/waves/round-83/w1/MutC1Hunt-receipts/mutbat-run2.out`
- `.ufo/waves/round-83/w1/MutC1Hunt-receipts/witness.txt`
- `.ufo/waves/round-83/w1/MutC1Hunt-receipts/witness.json`
- `.ufo/waves/round-83/w1/MutC1Hunt-receipts/repro.out`
- `.ufo/waves/round-83/w1/MutC1Hunt-receipts/sha256.txt`
- `.ufo/waves/round-83/w1/MutC1Hunt-receipts/selftest-out/<row>.out` (21 per-row selftest transcripts)
