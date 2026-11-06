# ExecC1RealTree — C1 P5/P6 dry run on a scratch landing mirror (round 80, attempt 1, wave 1 of 1)

Seat: leaf. No user-visible claim score is asserted here; this is a dry run of claim C1 predicates P5 and P6
against a scratch mirror of the landing tree. Frozen bytes were used unmodified.

Scratch: `S=/fast/scratch/hyaku/kasegi-r80/ExecC1RealTree` (deleted before yield; `TMPDIR` passed explicitly
under `$S` for every run; no counter/gate output under `/tmp`).

## Setup (commands and evidence)

1. `mkdir -p $S/tree && git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 4ab545865f747fca8456370b5927fe51236fe579 | tar -x -C $S/tree`
   → `ARCHIVE_OK`; top level: `AGENTS.md LOG.md PROVINCE.md README.md SCORECARD.md SHONEN.md SKILL.md c2-controls cited-lines.txt considerthese corpus plans`
2. `cp .ufo/waves/round-80/c1/recheck-cwd-census.py $S/tree/corpus/instruments/recheck-cwd-census.py`
   → `sha256sum` = `420151fdea1187aa308f63536216039746fc9d784f6096c36627b7513e505698` (matches the frozen candidate).
3. `cp .ufo/waves/round-80/w1-input/osv-ubuntu-binary-to-source-mapping.md $S/tree/corpus/knowledge/`
   → `ls $S/tree/corpus/knowledge/*.md | wc -l` = **94**.
4. Mirror carries `corpus/source-snapshots/round-80/{S114.txt,manifest.json,swarm-registry.json}` from the freeze commit.

Lane working-tree state observed (not modified by this seat): `M corpus/lessons/round-79.md`, untracked
`.ufo/waves/round-80/{w1,w1-input,w1-dispatch.json,w1-spec.json,w1.ready,w1.ready.dispatched}`.
`git diff 4ab5458 -- SKILL.md corpus/instruments/README.md corpus/SOURCES.md corpus/instruments/knowledge-expected.txt` is empty,
so the lane worktree pin rows equal the freeze-commit rows.

## P5 — census on the landing mirror

Command (run from `$S/tree`):

```
TMPDIR=$S/t1 python3 -B $S/tree/corpus/instruments/recheck-cwd-census.py \
  --root $S/tree --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin
```

Output:

```
RECHECK-CWD entries=94 noprefix=0 exit2_foreign=0 exit0_foreign=72 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0
RECHECK-CWD-RESULT conformant
rc=0
```

`entries=94` == `ls $S/tree/corpus/knowledge/*.md | wc -l` = 94; `noprefix=0 exit2_foreign=0 exit_other=0 norecheck=0
restoration_only=0`; RESULT conformant; rc 0. **P5 = met** on the mirror.

Cross-check against the committed pre-freeze control (`controls/c1-p5-realtree-prefreeze-r80.txt`, base tree,
entries=93): `exit0_foreign` 71→72, `exit1_foreign` 22→22. The one added entry is the C2 entry and it exits 0
from a foreign cwd through its `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …` recheck line — evidence
bearing on C2 B5, recorded here only as an observation.

### Observation (not a claim, not a finding against P5)

Same census with `--lane $S/tree` (scratch prefix):

```
RECHECK-CWD entries=94 noprefix=94 exit2_foreign=0 exit0_foreign=72 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0
RECHECK-CWD-RESULT nonconformant
rc=1
```

All 94 entries (including the new one) carry an absolute `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …`
prefix, so a scratch `--lane` mismatches every prefix while the executed foreign-cwd results are unchanged
(exit0=72, exit1=22). This is the census doing what it says (prefix is compared against `--lane`); P5's own
command passes the real lane, so the predicate is unaffected. The `cd <lane> &&` entries are lane-absolute by
design, which means the census cannot be pointed at a relocated clone without noprefix=94 — worth knowing for
round 81, not a verdict change.

## Base-instrument comparison over the same mirror (bucket by bucket)

`git show 58905f2bbc52db6b1634566cc1be9c92cdddebfb:corpus/instruments/recheck-cwd-census.py > $S/base-instrument.py`
(sha256 `e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a`), then:

```
TMPDIR=$S/t3 python3 -B $S/base-instrument.py --root $S/tree --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin
RECHECK-CWD entries=94 noprefix=0 exit2_foreign=0 exit0_foreign=72 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0
RECHECK-CWD-RESULT conformant
rc=0
```

| bucket | base 58905f2 | candidate 420151fd |
|---|---|---|
| entries | 94 | 94 |
| noprefix | 0 | 0 |
| exit2_foreign | 0 | 0 |
| exit0_foreign | 72 | 72 |
| exit1_foreign | 22 | 22 |
| exit_other | 0 | 0 |
| norecheck | 0 | 0 |
| restoration_only | 0 | 0 |
| RESULT / rc | conformant / 0 | conformant / 0 |

No bucket difference on this tree. The two instruments are coextensive on census arithmetic over the landing
mirror, which is consistent with the claim's own shape: the candidate's move is the counter/kill set, the TMPDIR
refusal and the selftest cases (P1–P3, P4, P8), none of which this P5/P6 dry run exercises. Stated plainly:
this dry run gives no evidence that the base instrument would fail P5 on the landing tree — P5 alone does not
separate base from candidate, and the claim does not ask it to.

## P6 — pin rows

Current rows at freeze `4ab5458` (identical in the lane worktree):

- `SKILL.md:982` — `… python3 corpus/instruments/recheck-cwd-census.py --selftest -> `selftest cases=6 failures=0`, exit 0 | .ufo/waves/round-75/controls/c1-after-r75.txt | corpus/ read-only + TMPDIR scratch | kasegi |`
- `corpus/instruments/README.md:354` — `… ; `--selftest` → `selftest cases=6 failures=0`, exit 0 |`

Replacement text (one token per row, `cases=6` → `cases=15`; full rows in
`.ufo/waves/round-80/w1/ExecC1RealTree-pins.txt`). Applied to scratch copies of `SKILL.md` and
`corpus/instruments/README.md` inside `$S/tree`, then:

```
grep -c 'recheck-cwd-census.py --selftest -> `selftest cases=15 failures=0`' SKILL.md            -> 1
grep -c '`--selftest` → `selftest cases=15 failures=0`' corpus/instruments/README.md             -> 1
```

Base counts on the same patterns with `cases=6`: `SKILL.md` 1, `README.md` 1.

One-substitution check: `git diff --no-index --word-diff=porcelain <freeze bytes> <scratch bytes>` prints exactly

```
-cases=6
+cases=15
```

for each file and nothing else. **P6 = met** on the mirror.

Untouched by design: `SKILL.md:1151` (r44-frontier-count), `README.md:851`, `README.md:887`, `README.md:995`
(other instruments' own `cases=` pins). Only the two recheck-cwd-census rows above change.

## Verdicts

- **P5 = met** — entries=94 equals the `.md` listing count at the mirror, all five zero buckets hold, RESULT
  conformant, rc 0, and the added C2 entry executes 0 from a foreign cwd.
- **P6 = met** — both `grep -c` = 1 with `cases=15` (base 1 each with `cases=6`), exactly one token changed per row.

## Risks / notes for the L1

1. P5 is count-based, so it cannot see a name-set mismatch; the executed-bucket shift (exit0_foreign 71→72)
   is the only direct evidence that the C2 entry itself conforms.
2. Base and candidate instruments are bucket-identical on the landing mirror; if a future round wants P5 to
   discriminate base from candidate it needs a row (e.g. a relocated-clone/`--lane` case), which under the
   frozen table would be a round-81 routed defect.
3. Lane-relative `cd <lane> &&` recheck prefixes make the census unusable against a relocated clone
   (noprefix=all) — observation carried to round 81.
4. Frozen bytes (candidate, counter, table, builder, manifest, snapshot, claims) were read-only throughout; no
   lane file, corpus file, instrument, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, fleet file or
   sibling lane was written. No git/jj writes; only `git archive` / `git show` / `git diff` reads.
5. No tool installs; no pacman transactions; no host sysctl touched; scratch deleted before yield.

## Files written

- `.ufo/waves/round-80/w1/ExecC1RealTree.md` (this report)
- `.ufo/waves/round-80/w1/ExecC1RealTree-pins.txt` (P6 replacement text, both rows)
