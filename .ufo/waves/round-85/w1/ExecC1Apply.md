# ExecC1Apply — round-85 C1 independent apply and score

Seat: ExecC1Apply (leaf, godspeed). Scratch `S=/fast/scratch/hyaku/kasegi-r85/ExecC1Apply` (deleted after receipts copied; `TMPDIR=$S` passed explicitly; `python3 -B` throughout; no lane-tree writes outside `w1/`; no test/lint/build run — parent owns the gate; no git/jj writes).

Axes: depth:verifiability (the scored meter itself), coverage.

## 1. Frozen instrument hashes vs claims.json instruments (P2)

Command: `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum .ufo/waves/round-85/c1/skill-meter.py .ufo/waves/round-85/c1/apply-map.py .ufo/waves/round-85/c1/repair-map.json`
Receipt: `ExecC1Apply-receipts/sha256.txt`

| file | sha256 | claims.json | match |
|---|---|---|---|
| `c1/skill-meter.py` | `89c5d47b4dc04df90129d5a3bd443bb877f22ba9f1565008daa7024557634ed6` | same | yes |
| `c1/apply-map.py` | `8eb22d7db99b820ab8209106f9db634bf5ef88aeb6dbb271e3ec514122b98c93` | same | yes |
| `c1/repair-map.json` | `b575f147835d55fcb810fe946825c0cfd36e51094341497e00f0d98db5ae1944` | same | yes |

## 2. Candidate generation (the file the L1 lands)

Commands:
```
git show bc722e540c93b48ff159454b65a0f9f4630db1ed:SKILL.md > $S/base.md
python3 -B .ufo/waves/round-85/c1/apply-map.py .ufo/waves/round-85/c1/repair-map.json $S/base.md .ufo/waves/round-85/w1/ExecC1Apply-SKILL.md
```
- base: 1251 lines; candidate: 1251 lines (line count unchanged).
- Candidate sha256: `7d082bfec14257351b39c145ea0db26cafbce3d6f263009c3eb1d0893c373552` (receipt `ExecC1Apply-receipts/candidate-sha.txt`).
- Base copy kept at `ExecC1Apply-receipts/base.md` for the L1 diff.

## 3. Frozen counting command, lane worktree (P1)

Command (exact claims.json C1, `--after` = candidate):
```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && TMPDIR=$S python3 -B .ufo/waves/round-85/c1/skill-meter.py --lane . --base $S/base.md --after .ufo/waves/round-85/w1/ExecC1Apply-SKILL.md --map .ufo/waves/round-85/c1/repair-map.json --target 167/732 --map-sha256 b575f147835d55fcb810fe946825c0cfd36e51094341497e00f0d98db5ae1944 --work $S/w
```
Output (receipt `ExecC1Apply-receipts/meter-lane.txt`), rc=0:
```
SKILL-METER base=158/741 after=167/732 target=167/732 mirror_absent=True
LIMB M1 pass after=167/732
LIMB M2 pass removed=18 keys=18 stray_removed=0 stray_added=0 unrepaired=0
LIMB M3 pass linecount_equal=True bad_lines=0 keys_hit=18
LIMB M4 pass bad=none
LIMB M5 pass sha256=b575f147835d55fcb810fe946825c0cfd36e51094341497e00f0d98db5ae1944
SKILL-METER-RESULT pass rc=0
```
Exactly as frozen: 158/741 -> 167/732, M1–M5 pass, rc 0. P1 holds in the `.git` lane worktree; P2 holds (§1); M3 machine form gives P3 (diff touches only repair-map-key lines, §6).

## 4. Re-run in freeze-clone and git-archive extract (host dependence)

Clone (read-only, detached at freeze 4a2d34f2…; `.git` present):
```
git clone --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin $S/clone
git -C $S/clone rev-parse --show-toplevel        # -> $S/clone
git -C $S/clone checkout -q --detach 4a2d34f203519a87078f21a896dc8679137ff675
# then skill-meter.py --lane $S/clone (same args)
```
Output (receipt `ExecC1Apply-receipts/meter-clone.txt`), rc=0 — identical to §3:
```
SKILL-METER base=158/741 after=167/732 target=167/732 mirror_absent=True
LIMB M1 pass after=167/732 / M2 pass / M3 pass (linecount_equal=True, keys_hit=18) / M4 pass / M5 pass
SKILL-METER-RESULT pass rc=0
```

git-archive extract (NO `.git`; `ls $S/extract/.git` → No such file or directory):
```
git archive 4a2d34f203519a87078f21a896dc8679137ff675 | tar -x -C $S/extract
# then skill-meter.py --lane $S/extract (same args)
```
Output (receipt `ExecC1Apply-receipts/meter-extract.txt`), rc=1:
```
SKILL-METER base=157/741 after=166/732 target=167/732 mirror_absent=True
LIMB M1 FAIL after=166/732
LIMB M2 pass removed=18 keys=18 stray_removed=0 stray_added=0 unrepaired=0
LIMB M3 pass linecount_equal=True bad_lines=0 keys_hit=18
LIMB M4 FAIL bad=S040-live.txt,S073.txt,S074.txt,capture-binding-check.py,capture-source.py,claim-package-check.py,entry29-fixed-bytes.md,frontier-recheck-count.py,kill-rule-check.py,limb-ledger.json,limb-mutation-check.py,r-defect-closure.sh,repo-git-state.md,resolve.py,score-gap.py,shonen-form.py,source-recheck.py,target-checkouts.md
LIMB M5 pass sha256=b575f147835d55fcb810fe946825c0cfd36e51094341497e00f0d98db5ae1944
SKILL-METER-RESULT fail rc=1
```
Recorded difference (as the spec predicted): without `.git`, the SKILL token `.git` classifies GONE, so base reads 157/741 (not 158/741) and after 166/732 (not 167/732); M4 additionally fails because the git-tracked check cannot run — all 18 map values list as bad. The meter must be read in a checkout with `.git` (census-of-record root) — confirmed, not merely asserted. This is a reproduced host-dependence, not a defect in the candidate; P1 is defined over the `.git` checkout.

## 5. Harm check — density (P4)

Usage line first: `density.py <SKILL.md> [--label LABEL]`.
Commands:
```
python3 -B corpus/instruments/density.py $S/base.md --label base
python3 -B corpus/instruments/density.py .ufo/waves/round-85/w1/ExecC1Apply-SKILL.md --label candidate
```
Receipts: `ExecC1Apply-receipts/density-base.txt`, `ExecC1Apply-receipts/density-cand.txt`.
- base: mean dens **273.2**, 932 path-citation instances, 38 blocks, 1251 lines.
- candidate: mean dens **273.2**, 932 path-citation instances, 38 blocks, 1251 lines.
- Per-block tables identical in both receipts. Candidate >= base (equal) → P4 holds; no depth:density harm. (`mirror_absent=True` in all meter runs; mirror roots absent as the claim states.)

## 6. Diff (receipt `ExecC1Apply-receipts/diff.txt`)

Command: `diff -u $S/base.md .ufo/waves/round-85/w1/ExecC1Apply-SKILL.md` (rc=1 = files differ, as expected).
- Line counts: both 1251.
- `diff | wc -l` = 64; `grep -c '^@@'` = 10 hunks; `grep -c '^[-+]'` on the unified diff = 36 (includes file/hunk headers).
- Every hunk is a backticked bare token replaced by its full lane path, in map order: e.g. `` `repo-git-state.md` `` → `` `corpus/knowledge/repo-git-state.md` ``, `` `S040-live.txt` ``-family snapshot names → `corpus/source-snapshots/…`, and the 14 instrument basenames → `corpus/instruments/…`. No other citation added/removed/changed (corroborated by M2 `stray_removed=0 stray_added=0` and M3 `bad_lines=0`).

## Files written by this seat

- `.ufo/waves/round-85/w1/ExecC1Apply-SKILL.md` — the candidate (L1 lands it as SKILL.md).
- `.ufo/waves/round-85/w1/ExecC1Apply.md` — this report.
- `.ufo/waves/round-85/w1/ExecC1Apply-receipts/` — `sha256.txt`, `meter-lane.txt`, `meter-clone.txt`, `meter-extract.txt`, `diff.txt`, `density-base.txt`, `density-cand.txt`, `base.md`, `candidate-sha.txt`, `clone.log`.

## Verdict for the L1

C1 predicates P1 (in a `.git` checkout), P2, P3 (M3 machine form), P4 all hold on the generated candidate; rc=0 with 167/732 exactly. The git-archive read (157/741 → 166/732, M1/M4 fail) reproduces the frozen host note and does not count against C1 — the counter must be run where `.git` exists. No routed defects. No tools installed. Scratch `$S` deleted before yield.

Checks the main agent should run at integration (not run by this seat per wave rules): the frozen counting command over the landing commit's SKILL.md in the census-of-record checkout; `git diff <freeze> <landing> -- SKILL.md` line-touch audit; density on the landed SKILL.md.
