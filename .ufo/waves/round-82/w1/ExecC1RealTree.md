# ExecC1RealTree — C1 real-tree predicates (round 82, attempt 1)

Seat: ExecC1RealTree (leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Freeze commit: `b9589300810a477f4d6794bfabc24b22fb50b846` (base `1a50638e`).
Scratch: `/fast/scratch/hyaku/kasegi-r82/ExecC1RealTree` (TMPDIR passed explicitly; deleted at exit).
No lane file, instrument, corpus file or git state was modified. No tool installs were needed.

Frozen bytes verified before any run (sha256, all four match the freeze):

```
81677e9dc030ed59d2e3481c8b1c2bc8d083e6805cc06fbb25052a685773e050  .ufo/waves/round-82/c1/recheck-cwd-census.py
a7d4db43cdc8b2948af9c8c5f1baee827979fbb3d7dac0f39ecd46fad60ac55c  .ufo/waves/round-82/c1/mutbat.py
045edc07c9edb24cb401b241e512745cc81e4d0f36eea26e5362b49e7cc5f26a  .ufo/waves/round-82/c1/mutant-table.json
52cc6be5aa9d72c9d0644c1d97e252b215d792e5c00445417aa477d004d53908  .ufo/waves/round-82/controls/c1-forgeries-r82.py
```

Tree state at run time (read-only observation): the worktree is mid-integration and dirty —
`corpus/instruments/recheck-cwd-census.py` is already byte-identical to the frozen candidate
(81677e9d), `SKILL.md` and `corpus/instruments/README.md` already carry the P7 replacement,
`corpus/knowledge/` holds 96 entries including the untracked C2 draft
`osv-high-quality-record-import-bar.md`. So P5/P6/P7 below were evaluated on the **integrated
worktree**, not on the freeze commit's 95-entry tree. Nothing was written to it.

The tree kept moving while this seat ran: `git diff --stat` grew from 4 to 9 modified files
(`PROVINCE.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`,
`corpus/instruments/knowledge-expected.txt` appeared) — concurrent integration by other seats,
not this seat. The stability control is the scratch copy: P5 and P6 reproduce byte-identically
over a frozen copy of `corpus/knowledge` (96 files), and the two P7 rows' worktree sha256 in the
pins file still match the live files (`SKILL.md` 818d0a45, `README.md` c3b18ce6).

## P5 — census on the real tree: HOLDS

```
$ TMPDIR=$S python3 -B .ufo/waves/round-82/c1/recheck-cwd-census.py --root $LANE --lane $LANE
RECHECK-CWD entries=96 noprefix=0 exit2_foreign=0 exit0_foreign=74 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0
RECHECK-CWD-RESULT conformant
rc=0
```

- `exit0_foreign + exit1_foreign = 74 + 22 = 96 = entries` ✔
- `entries = 96` equals `ls corpus/knowledge/*.md | wc -l = 96` ✔
- `noprefix=0 exit2_foreign=0 exit_other=0 norecheck=0 restoration_only=0` ✔
- `RECHECK-CWD-RESULT conformant`, exit 0 ✔

Reproduced identically over an exact scratch copy of `corpus/knowledge` (`--root $S/tree`,
`--lane` unchanged, 96 files), so the numbers are not a race against the in-flight tree:
same line, same rc 0. Receipts: `ExecC1RealTree-receipts/p5-lane.txt`,
`.../p5-scratchcopy.txt`.

## P6 — J1 applied once: HOLDS (nonconformant, rc 1)

Row J1 from the frozen table: anchor `        counts["entries"] += 1\n` (occurs exactly once
in the candidate), replacement appends `if name.startswith("osv-"): continue`. Applied once
with a literal `str.replace(..., 1)`; mutated file sha256
`b29a9034f003fecc46eb26bb6d148f528c6498b5fa972213f1577f0da7edd86d`.

```
$ TMPDIR=$S python3 -B $S/j/recheck-cwd-census.py --root $LANE --lane $LANE
RECHECK-CWD entries=96 noprefix=0 exit2_foreign=0 exit0_foreign=67 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0
RECHECK-CWD-RESULT nonconformant
rc=1
```

`67 + 22 = 89 != 96`: the seven `osv-*.md` entries are counted then skipped, so the bucket sum
limb fires. Every other limb is still zero, so the kill is attributable to the bucket sum alone.

### r81 baseline of the same edit (r81 instrument, same tree)

```
$ TMPDIR=$S python3 -B .ufo/waves/round-81/w1/CriticClaims-receipts/candidate-junkedit.py --root $LANE --lane $LANE
RECHECK-CWD entries=96 noprefix=0 exit2_foreign=0 exit0_foreign=67 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0
RECHECK-CWD-RESULT conformant
rc=0
```

The r81 instrument prints the **same 89 != 96 shortfall** and still exits 0, because its
conformance expression is only the four limbs (`noprefix`, `exit2_foreign`, `norecheck`,
`restoration_only`; `candidate-junkedit.py:737-740`). This is the r81 routed defect 3
reproduced on the round-82 tree, and it is closed by `conform_ok()` in the candidate. The r81
junkedit file is byte-for-byte the r81 candidate plus the same J1 edit
(`candidate-junkedit.py:125-127`).

## P4 — forgery controls: HOLDS, all six lines match the frozen P4 text

```
$ TMPDIR=$S python3 -B .ufo/waves/round-82/controls/c1-forgeries-r82.py --lane $LANE --work $S/f
FORGERY F6-selfdiff counter=r81 forgery_sha256=5950fee4... rc=0 verdicts={"KILLED": 60, "NEUTRAL-OK": 3} ... baseline=ok rows=63 killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3
FORGERY F6-selfdiff counter=r82 forgery_sha256=5950fee4... rc=1 verdicts={"KILLED": 60, "NEUTRAL-OK": 3} ... baseline=ok rows=63 killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=broken decoy_hidden=59/60
FORGERY F7-wsnorm   counter=r81 forgery_sha256=342f4c61... rc=0 verdicts={"KILLED": 60, "NEUTRAL-OK": 3} ... killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3
FORGERY F7-wsnorm   counter=r82 forgery_sha256=342f4c61... rc=1 verdicts={"KILLED": 60, "NEUTRAL-OK": 3} ... killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=broken decoy_hidden=59/60
FORGERY F8-astembed counter=r81 forgery_sha256=b37e7da6... rc=0 verdicts={"KILLED": 60, "NEUTRAL-OK": 3} ... killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3
FORGERY F8-astembed counter=r82 forgery_sha256=b37e7da6... rc=0 verdicts={"KILLED": 60, "NEUTRAL-OK": 3} ... killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=59/60
rc=0
```

Per-line comparison with P4 in `claims.json` (full lines in
`ExecC1RealTree-receipts/p4-forgeries.txt`):

| line | required by P4 | observed | match |
|---|---|---|---|
| F6 r81 | rc 0, `killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3` | rc 0, exactly that | yes |
| F6 r82 | rc 1, `decoy=broken` | rc 1, `decoy=broken decoy_hidden=59/60` | yes |
| F7 r81 | rc 0, kill line | rc 0, exactly that | yes |
| F7 r82 | rc 1, `decoy=broken` | rc 1, `decoy=broken decoy_hidden=59/60` | yes |
| F8 r81 | rc 0 | rc 0 | yes |
| F8 r82 | rc 0 (recorded limit) | rc 0, `decoy=ok decoy_hidden=59/60` | yes |

Note worth carrying: the **kill tally is identical** for F6/F7 under both counters
(`killed=60 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3`). Only the decoy limb
separates r81 from r82, i.e. the r81 defect 2 closure rests entirely on the counter-owned
decoy limb, exactly as claimed. F8 stays rc 0 under both counters — the declared limit, not a
pass condition.

## P8 analogue — HOLDS (1 / 1 / 0)

```
grep -c 'subprocess.run('      -> 1
grep -cF '"bash", "-c"'        -> 1
grep -cE "[\"']/tmp"           -> 0
```

## P7 — pins and dry-run proof (no lane edit)

Pins: `.ufo/waves/round-82/w1/ExecC1RealTree-pins.txt` — per file the freeze-commit row
(contains `cases=22` exactly once), the replacement row (`cases=22` -> `cases=24`, nothing
else), and the current worktree row.

- `SKILL.md` line 982, pattern `^\| recheck-cwd-census\.py \|`
- `corpus/instruments/README.md` line 354, pattern ``^\| `corpus/instruments/recheck-cwd-census\.py` \|``

Dry run on scratch copies of the freeze-commit bytes
(`git show b958930:SKILL.md`, `:corpus/instruments/README.md` -> `$S/base-*.md` ->
`$S/p7/*.md`, `sed -i 's/cases=22/cases=24/'`):

```
base   SKILL  cases=22: 1  cases=24: 0      README cases=22: 1  cases=24: 0
sed    SKILL  cases=24: 1  cases=22: 0      README cases=24: 1  cases=22: 0
sed row vs current worktree row: SKILL identical, README identical (diff empty)
whole-file diff base -> worktree: 2 changed lines per file = exactly one row each
```

So the substitution is provably one token and nothing else, and the worktree rows already
equal the replacement byte-for-byte (an in-flight seat has applied it; uncommitted). At the
freeze commit both rows contain `cases=22` and no `cases=24`, as P7's base clause states.
Receipt: `ExecC1RealTree-receipts/p7-dryrun.txt`.

## Findings routed to round 83 (advisory; no verdict change, no predicate edit)

1. **Registry prose understates the landed gate.** The `SKILL.md` row's conformance cell and
   the `README.md` row's prose still list only `noprefix/exit2_foreign/norecheck/
   restoration_only`; the r82 `conform_ok()` also requires the six buckets to sum to `entries`.
   P7 pins only the `cases=` token, so this is not a P7 failure — but an operator reading the
   registry would not learn that a bucket shortfall is now nonconformant.
2. **P6's real-tree kill is environment-dependent.** J1 skips entries whose name starts with
   `osv-`; the tree currently has 7 such entries (one of them C2's new draft), so the sum
   shortfall is 7. With zero `osv-*` entries J1 would be a no-op on the real tree and P6 would
   print conformant. It holds today; the dependency is worth stating in the claim's texture.
3. **`exit1_foreign=22` is the documented fail-closed set, and the README prose is looser than
   the code.** The 22 entries (e.g. `claim-anatomy-sample.md`, `mission-ledger.md`) exit 1
   because their external base (`~/Projects/bounties`, `~/Projects/the-bounty-hunter`) has been
   absent since 2026-09-28; the instrument docstring calls this "fail-closed ... by design" and
   conformance only refuses exit 2. The README row says each value "must exit 0 from a foreign
   cwd", which the code does not enforce. Pre-existing (same prose at the freeze commit), not a
   P5/P7 failure.
4. **P5's `entries=96` is the landing-tree number, not the freeze-tree number.** At the freeze
   commit `corpus/knowledge/` held 95 files; the 96th is C2's untracked draft. The predicate is
   self-consistent either way (`entries` vs `ls | wc -l`), but the recorded 96 must not be read
   as a freeze-time fact.

## Scope

Ran only the named commands (P5 census, P6 J1 mutation + r81 baseline, P4 forgery driver, P8
greps, P7 sed dry-run) plus one read-only `--verbose` diagnostic run of the same census to
characterise the 22 exit-1 entries. No selftest, no mutbat run, no lane gate suite. No lane
file, corpus file, instrument, registry, git or jj state was touched; no subagents, no
background jobs beyond the single forgery-driver run that outlived the 60 s shell window.
