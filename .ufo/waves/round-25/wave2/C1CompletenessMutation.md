# C1CompletenessMutation — round 25 wave 2

Role: mutation-tester. Item: delete one recheck line and prove the completeness
rule fails; also test empty corpus/knowledge. Read-only scope; all mutations on
scratch copies under `/tmp/w2c1/`; production tree never touched (verified below).

Instrument of record: `corpus/instruments/recheck-audit.py`
sha256 `c3c19adcde927ac83460ad5a9855b5178935c1f5b8ec41291e8a4fd0ba2f6d7f`
(matches `c1-receipt-index.txt` line 3).

## Claim under attack

`claims.json` C1, with `counter_notes.counter_repair`: "strict limbs and
completeness rule added … A deleted recheck line therefore fails the audit
instead of silently shrinking the set" (recheck-audit.py:39-42).

Rule under test (file:line, instrument sha c3c19adc):
- `complete = len(entries) == total and total > 0` — recheck-audit.py:251
- `ok = passed == len(entries) and complete and strict_passed == total` — :252
- `total = len(glob.glob(os.path.join(root, "corpus/knowledge/*.md")))` — :243
- `collect()` at :153-159 counts only files whose `audit_entry()` returns a
  record, i.e. files containing a `recheck:` line (:101-102 returns None).

Baseline note: the working tree holds the post-C2 state (37 knowledge files,
two added this round), matching the "final tree 37/37" receipt, not the frozen
35-file surface. All probes use the final tree; `--cdroot
/home/vgpnk/Projects/shokunin/kasegi-shokunin` keeps strict limb (d) honest
while `--root` points at each scratch copy (recheck-audit.py:230-233).

## Baseline (pristine scratch copy)

```
cp -a $LANE/corpus /tmp/w2c1/baseline/
python3 corpus/instruments/recheck-audit.py --root /tmp/w2c1/baseline \
  --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin
```
Output: `strict pass=37/37 … lines=37 total=37 pass=37 fail-closed=23
parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`. **EXIT=0.** Baseline is
conclusive — a mutation that changes exit 0→1 is killed by the detector.

## Mutants

### M1 — delete the `recheck:` line of ev-model.md (the assigned attack)

```
grep -n '^recheck:' /tmp/w2c1/mut-line/corpus/knowledge/ev-model.md
# 60:recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && ...
sed -i '/^recheck:/d' /tmp/w2c1/mut-line/corpus/knowledge/ev-model.md
python3 corpus/instruments/recheck-audit.py --root /tmp/w2c1/mut-line \
  --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin   →  EXIT=1
strict pass=36/37 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=14 gated=22 broken=0
lines=36 total=37 pass=36 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
```

Every remaining line passes all six strict limbs, yet exit is 1: only the
completeness limb (`len(entries)=36 != total=37`, recheck-audit.py:251)
distinguishes this from a green run. **Verdict: KILLED** — the completeness
rule detects a deleted recheck line exactly as the wave-1 counter_notes claim.

### M2 — empty `corpus/knowledge/`

```
rm /tmp/w2c1/mut-empty/corpus/knowledge/*.md
python3 corpus/instruments/recheck-audit.py --root /tmp/w2c1/mut-empty ...  → EXIT=1
strict pass=0/0 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=0 gated=0 broken=0
lines=0 total=0 pass=0 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
```

`total=0` → `complete=False` via `total > 0` (recheck-audit.py:251) → `ok=False`
(:252). **Verdict: KILLED** — an empty corpus cannot reach exit 0; the rule
fails closed on the degenerate case. (A nonexistent `corpus/knowledge/` dir
glob-matches the same way, also exit 1.)

### M3 — delete the whole entry file ev-model.md (coverage probe)

```
rm /tmp/w2c1/mut-delfile/corpus/knowledge/ev-model.md   # 37 → 36 files
python3 corpus/instruments/recheck-audit.py --root /tmp/w2c1/mut-delfile ...  → EXIT=0
strict pass=36/36 … lines=36 total=36 pass=36 fail-closed=22 … exit=0
```

**Verdict: SURVIVED.** The completeness check compares recheck-line count to
the count of `*.md` files present (:251); removing an entire entry shrinks both
sides, so the audit self-consistently reports 36/36 exit 0. The rule catches a
deleted *line* but not a deleted *entry*. This does not void the wave-1 claim —
the frozen surface is "the `recheck:` line of every corpus/knowledge/*.md
entry", and a vanished file has no line to audit — but it is a real coverage
gap: entry deletion is the one mutation that silently shrinks the audited set
the completeness rule was added to protect. Smallest correction: hash or list
the expected `corpus/knowledge/*.md` set into the receipt (the instrument
already embeds `instrument_sha256`; a `knowledge_set_sha256` over sorted
basenames would pin the same surface).

### M4 — a directory named `zz-fake.md` inside corpus/knowledge/

```
mkdir /tmp/w2c1/mut-dir/corpus/knowledge/zz-fake.md     # total glob = 38
python3 corpus/instruments/recheck-audit.py --root /tmp/w2c1/mut-dir ...    → EXIT=1
Traceback (most recent call last):
  … recheck-audit.py:95, in audit_entry
    with open(path, encoding="utf-8") as handle:
IsADirectoryError: [Errno 21] Is a directory: '/tmp/w2c1/mut-dir/corpus/knowledge/zz-fake.md'
```

**Verdict: KILLED but uncleanly.** Exit is non-zero so the audit still fails
closed, but it crashes at `audit_entry` (recheck-audit.py:95) instead of
emitting a verdict line for the offending path. Cosmetic hardening only;
`*.md` glob at :155 matches directories.

## Restoration evidence

```
cp /tmp/w2c1/baseline/corpus/knowledge/ev-model.md \
   /tmp/w2c1/mut-line/corpus/knowledge/ev-model.md
sha256sum …/ev-model.md → 000fe7fbb93dada051006f44cbdada4944fb75bfc5e78fe1276c70d64fb7a364
  (identical for restored scratch file and $LANE/corpus/knowledge/ev-model.md)
re-audit → lines=37 total=37 pass=37 … exit=0   RESTORED_EXIT=0
```

Mutated bytes restored exactly; scratch copies only — `git status` shows
`corpus/knowledge/ev-model.md` already ` M` from wave-1's own round-25 edits
(1 insertion, 1 deletion vs commit b49948f), not from this probe. No production
files were written; no VCS touched.

## Verdict on the wave-1 result

Wave-1's completeness claim **holds as stated**: the rule at
recheck-audit.py:251-252 detects both a deleted recheck line and an empty
corpus/knowledge, exiting 1 in each case, and the 37/37 baseline is
reproducible on a byte-identical copy. One falsifiable correction to scope,
not to the score: the rule is a *line-count* completeness check — deleting an
entire `corpus/knowledge/*.md` entry still yields exit 0 (M3), and a `.md`
directory crashes the audit (M4). Neither changes lines=37 pass=37 on the
real tree.

## Commands and exits (verbatim)

| Probe | Command | Exit | Key output |
|---|---|---|---|
| Baseline | `python3 corpus/instruments/recheck-audit.py --root /tmp/w2c1/baseline --cdroot $LANE` | 0 | `lines=37 total=37 pass=37 … exit=0` |
| M1 delete line | same `--root /tmp/w2c1/mut-line` | 1 | `lines=36 total=37 pass=36 … exit=1` |
| M2 empty corpus | same `--root /tmp/w2c1/mut-empty` | 1 | `lines=0 total=0 pass=0 … exit=1` |
| M3 delete file | same `--root /tmp/w2c1/mut-delfile` | 0 | `lines=36 total=36 pass=36 … exit=0` |
| M4 md directory | same `--root /tmp/w2c1/mut-dir` | 1 | `IsADirectoryError` traceback at :95 |
| Restored | same `--root /tmp/w2c1/mut-line` after `cp` | 0 | `lines=37 total=37 pass=37 … exit=0` |

Scratch trees: `cp -a $LANE/corpus /tmp/w2c1/<mut>/corpus`. Runs from the lane
root with `--foreign` default `/`. Full logs at `/tmp/w2c1/*-run.txt` (ephemeral).

## Tool install/update record

None. Python 3.13.7 (`/usr/bin/python3`) and coreutils/bash already present; no
installs needed or performed.

Report: .ufo/waves/round-25/wave2/C1CompletenessMutation.md
