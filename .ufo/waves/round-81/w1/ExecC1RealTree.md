# ExecC1RealTree — C1 P5/P6/P7 dry run on a scratch landing mirror (round 81, attempt 1, wave 1)

Freeze `7ad3118c86ee14fde433d73671cc407668533cec`; base `191e6ba8f872d08802d83b57cd7fcf4bfa122f0e`. Lane read-only throughout; all writes in the wave dir and scratch. No lane byte was edited; no git/jj writes.

Mirror construction (scratch `/fast/scratch/hyaku/kasegi-r81/ExecC1RealTree`, deleted before yield):

```
mkdir -p $S/m && git -C <lane> archive 7ad3118c… | tar -x -C $S/m
cp .ufo/waves/round-81/c1/recheck-cwd-census.py  $S/m/corpus/instruments/recheck-cwd-census.py
cp .ufo/waves/round-81/w1-input/osv-importfindings-record-quality-feedback.md  $S/m/corpus/knowledge/
```
Frozen-byte checks on the mirror: instrument sha256 `a3b58aa52ba0744199ee97e6bd837e62c499e3e6af03a2fc26f0e6e3746dbec0` (= frozen candidate); new entry sha256 `2895011e23b38deb04f634398072d70e88ce9dfe878bffe3d64d00af0c371940` (= w1-input copy). `ls $S/m/corpus/knowledge/*.md | wc -l` = **95**.

## P5 — MET on the landing analogue

The census reads only `<root>/corpus/knowledge/*.md` (`:116`, `:123`), and every entry's recheck value executes against the real lane through its own `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ` prefix, so the mirror root is read-set-exact for the landing tree. Two runs:

| run | command | RECHECK-CWD line | result | rc |
|---|---|---|---|---|
| A | `--root $S/m --lane $S/m` | `entries=95 noprefix=95 exit2_foreign=0 exit0_foreign=73 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0` | `nonconformant` | 1 |
| **B (P5 analogue)** | `--root $S/m --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin` | `entries=95 noprefix=0 exit2_foreign=0 exit0_foreign=73 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0` | **`conformant`** | **0** |

Run A is the control, not the analogue: the mirror's 94 tracked entries carry the real lane's `cd` prefix in frozen bytes, so `--lane <mirror>` counts all 95 as `noprefix` — exactly what "frozen bytes are never edited" predicts. Run B is the P5 analogue: `entries=95` = the landing tree's `ls corpus/knowledge/*.md | wc -l` (95, also measured in the real worktree), `noprefix=0 exit2_foreign=0 exit_other=0 norecheck=0 restoration_only=0`, `RECHECK-CWD-RESULT conformant`, rc 0. Exit buckets sum to 95 (73+22); the 22 `exit1_foreign` are the entries' recorded fail-closed lines, which the gate allows (only `exit2_foreign`/`exit_other` are required zero). The new entry is counted in the prefixed set and runs green: in run A it prints `ENTRY osv-importfindings-record-quality-feedback.md noprefix=1 foreign_exit=0`; in run B it is silent by design (prefixed passing entry without `--verbose`) while `entries` rises 94→95. Its frozen `recheck:` line (`:5`) is `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-81/manifest.json --source S115`.

Residual risk (names, not hides): the literal landing run uses `--root` = `--lane` = the real lane. The only difference is the root path string; the read set is identical (no tracked knowledge drift: `git diff --name-only -- corpus/knowledge` = 0 files; new entry bytes = w1-input bytes). If the L1 re-writes the entry's `recheck:` line at landing, P5 must be re-read from the landed bytes.

## P7 — MET on the candidate (= the bytes P2 pins at landing)

`grep -c 'subprocess.run('` = **1**; `grep -c '"bash", "-c"'` = **1** (both the single site at `:105`); `grep -cE "[\"']/tmp"` = **0**. The only `/tmp` occurrence in the file is prose at `:25` ("no path is hard-coded under /tmp"), unquoted, so the P7 regex does not see it. Temp paths come from `tempfile` under `TMPDIR`.

## P6 — replacement rows, single-hunk diff, verified by apply

At the freeze both anchored rows match exactly once and each contains exactly one `cases=15`:

- `SKILL.md:982` (`^\| recheck-cwd-census\.py \|` → 1 match; 10 pipes; 540 B row; file sha256 `6d5b4421a22b5982e2a10d1772cd8772ab75332c462ffa08a118f618acaba65c`, 156080 B / 1251 lines)
- `corpus/instruments/README.md:354` (`^\| `corpus/instruments/recheck-cwd-census\.py` \|` → 1 match; 4 pipes; 709 B row = 703 chars; file sha256 `bd0eb3bae16647b43dffa3d554706383f0186ae9cbc391fc47136c6ff51ff990`, 94062 B / 1054 lines)

Replacement is `selftest cases=15 failures=0` → `selftest cases=22 failures=0` inside those two rows and nothing else; the unified diff is `ExecC1RealTree-pins.txt` (6059 B, sha256 `ef04db7257cd7bba8100ca2a6eb4415c7534a4d4c009ff9aab6ee1d1785ffb9e`; two hunks: `a/SKILL.md` @@ -979,7 +979,7 @@ and `a/corpus/instruments/README.md` @@ -351,7 +351,7 @@). Verified on a scratch copy of the mirror with `patch -p1`: `patch_rc=0`; `patch -p1 --dry-run` against a scratch copy of the lane's current `SKILL.md` + `corpus/` (both byte-identical to the freeze files) checks both files cleanly, `dryrun_rc=0`; per file exactly **2** `+/-` lines (the one row); post-patch anchored rows still **1** each, `cases=22` **1** per file, `cases=15` **0** per file; patched files are byte-identical to the constructed replacement copies. Row widths, pipe counts and the escaped `\|` inside the verdict column are unchanged.

**No third row pins the count.** `grep -rn 'selftest cases=15' --include='*.md' --include='*.json' --include='*.txt'` over the freeze tree: 154 lines in 88 files — 143 lines / 81 files are frozen `.ufo/` wave history (round-26 `recheck-audit.py`, round-79/80 census artifacts, controls, claims). Outside `.ufo/`: 11 lines in 7 files — the two pin rows above, and 9 lines in five lesson records (`corpus/lessons/round-26.md` ×3 and `round-26-verifier-spotcheck.md` ×1, about round-26's `recheck-audit.py` count; `round-79.md` ×1; `round-80.md` ×3 and `round-80-verifier-spotcheck.md` ×1, round-80 landing records). None is a registry row; none binds the round-81 landing count. `SCORECARD.md:3027` and `LOG.md:2852,2864` likewise quote `cases=15` as round-79/80 ledger history.

## Step 5 — stale instrument README/SKILL prose

- Neither `SKILL.md` nor `corpus/instruments/README.md` describes the census selftest's *case list*; each mentions the instrument on exactly one line (the pin row replaced above). The `--selftest` prose blocks elsewhere in the README (`:267-328`, `:849-851`, `:936-942`, `:1026-1040`) belong to anchorcheck, capture-binding-check, frontier-recheck-count, kill-rule-check and census-freshness-check — they do not name this instrument and are not stale from this landing.
- Round-80 records that will *read* stale if quoted as current: `corpus/lessons/round-80.md:39,44`, `corpus/lessons/round-80-verifier-spotcheck.md:40`, `SCORECARD.md:3027`, `LOG.md:2864`. They are historical statements about round 80 and must not be edited; the L1 should add the round-81 row rather than rewrite them.
- Pre-existing staleness in the SKILL row's *pinned-value path* column: `.ufo/waves/round-75/controls/c1-after-r75.txt:9` says `selftest cases=6 failures=0`. That receipt was already stale at the base (15) and is untouched by this round; the claim does not ask for a third edit. Routed as a note: if the column is meant to pin the current count, it belongs to round 82, not to this landing.

## Verdict and files

P5 met on the analogue (conformant, entries=95, all required limbs zero, rc 0); P6 replacement diff verified by apply, exactly two rows, no third pin; P7 1/1/0. No instrument, registry, corpus or lane file was edited by this seat; the lane worktree changes visible at yield (`PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`, `knowledge-expected.txt`, the new entry, `.ufo/waves/round-81/assimilation/`) are concurrent writes by the L1/other seats and were not used as evidence. Findings above are routed notes, not verdict changes.

Files written:
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ExecC1RealTree.md`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ExecC1RealTree-pins.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ExecC1RealTree-receipts/p5-runA-lane-mirror.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ExecC1RealTree-receipts/p5-runB-lane-real.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ExecC1RealTree-receipts/mirror-state.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ExecC1RealTree-receipts/p6-freeze-rows.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ExecC1RealTree-receipts/p6-apply-and-check.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ExecC1RealTree-receipts/p7-greps.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ExecC1RealTree-receipts/pin-census.txt`

Tooling: no installs or upgrades (nothing needed).
