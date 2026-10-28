VERDICT: BROKEN

# R46MutC1a — C1 mutation test of corpus/instruments/r46-c1-gate.py (limbs L1–L3)

Scope: read-only mutation probe. Counter not edited; nothing committed; no git mutation; no shared file touched. Scratch removed on exit.
Result: the counter rejects all four controls and accepts **6 of 10** single-edit mutants whose defect is present. The survivors are in the recheck-line shape (L3, with L1/L2 consequences) and in the row-to-claim link that the counter cannot judge.

## Setup (re-run by me)

- Counter under test: `corpus/instruments/r46-c1-gate.py`, sha256 `b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294` — equals `c1-gate-sha256` in `.ufo/waves/round-46/freeze.txt`.
- BASE = copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure` (+ the frozen counter copied in as the tree's own tool).
- GOOD = BASE + the same counter + `corpus/source-snapshots/round-46/` copied from the lane, + hand-built `## Re-ground (round 46)` sections (7 rows each, anchors in `corpus/instruments/claim-package-check.py`, `corpus/instruments/claim-package-selftest.py`) in `corpus/knowledge/claim-gates.md` and `corpus/knowledge/claim-package-contract.md`, each recheck line replaced by `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<entry>`.
- Every counter run: `HOME` = scratch home that mirrors only the host facts the rechecks assert (`~/Projects/ufo-fsd-alpha` exists, `~/Projects/bounties` absent). Without the `ufo-fsd-alpha` fixture the base read was `gated=25`, because `root-loss-2026-10-12.md` ends `test -e ~/Projects/ufo-fsd-alpha`; with it the base read matches the frozen control.
- Mutant command: `python3 <tree>/corpus/instruments/r46-c1-gate.py --root <tree> --baseline <BASE> --work <scratch>` (the mutant tree's own copy). `rejected=1` iff exit ≠ 0.

## Controls (re-run)

```
== control A: do-nothing (tree = baseline = pure base export)
gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64
gate L2 pass=0 read=base-gated=24 regrounded=0
gate L3 pass=0 read=recheck-lines-clean=0
gate L4 pass=0 read=entry-mode-green=0
gate L5 pass=0 read=append-only=0
gate L6 pass=0 read=mutants=0 survivors=none
gate L7 pass=1 read=still-gated=24 changed=none
c1-gate fixed=1/7 exit=1
== control B: clean hand-built tree (no mutation)
gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-clean=2
gate L4 pass=1 read=entry-mode-green=2
gate L5 pass=1 read=append-only=2
gate L6 pass=1 read=mutants=13 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
clean verbatim recheck exits (cd rewritten to tree) CG=[0] CP=[0]
```

The do-nothing read (`fixed=1/7 exit=1`, `gated=24`) and the clean read (`fixed=7/7 exit=0`) agree with the frozen expectations (`expect_before` / `expect_after`).

## Survivors (defect present, counter says fixed=7/7 exit=0)

Each survivor is one edit to the `claim-gates.md` re-ground of GOOD. Every survivor's counter output is the same as clean (all seven gates pass, `mutants=13 survivors=none`).

**S1. `soft-or-true` (L3 recheck shape; L1 gated count).** Edit: the recheck line gets ` || true` appended, so the line always exits 0 and is classed `executes`.
- Result: `mutant=soft-or-true rejected=0`, `c1-gate fixed=7/7 exit=0`.
- Witness: verbatim recheck exit with rows intact `[0]`; with the first row token blanked `[0]` (the gate call can no longer fail).
- Why the counter misses it: `classify` (counter lines 160–168) classes any `rc == 0` as `executes`; L3 (lines 184–189) only does substring tests on the raw line (`"r46-c1-gate.py" in ln`, `"--entry corpus/knowledge/%s" % e in ln`) and a `~/`/`$HOME`/`/home/` regex on the cd-stripped line; L4 (line 192) runs the counter's own bytes, not the recheck line.

**S2. `comment-shape` (L3 recheck shape).** Edit: the whole recheck line becomes `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && true  # r46-c1-gate.py --entry corpus/knowledge/claim-gates.md`. The gate call is inside a shell comment; the substrings L3 looks for are still present.
- Result: `mutant=comment-shape rejected=0`, `fixed=7/7 exit=0`.
- Witness: verbatim exit with rows intact `[0]`; with the first row token blanked `[0]`.

**S3. `cd-tilde` (L3 recheck shape; cd target never checked).** Edit: `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin` → `cd ~/Projects/shokunin/kasegi-shokunin` in the claim-gates recheck line.
- Result: `mutant=cd-tilde rejected=0`, `fixed=7/7 exit=0`.
- Witness: verbatim line with cd rewritten to the tree `[0]`; the same line run as written, isolated HOME `(1)`; run as written with the real HOME `(1)` — the cd lands in the live lane and the counter's entry mode runs there against the lane's own (un-re-grounded) `claim-gates.md` (read-only).
- The counter never runs the `cd` (`CD_RE.sub` at counter line 163), so the line is scored `executes` while it fails as written. The lane's own strict audit catches this (see cross-check).

**S4. `abs-counter-path` (L3 recheck shape; portability).** Edit: `python3 corpus/instruments/r46-c1-gate.py` → `python3 /fast/scratch/hyaku/kasegi-r46/R46MutC1a/good/corpus/instruments/r46-c1-gate.py` in the claim-gates recheck line (the path lies outside the tree).
- Result: `mutant=abs-counter-path rejected=0`, `fixed=7/7 exit=0`.
- Witness: gate path lies outside the mutant tree `True`; verbatim exits `[0]` intact, `[1]` with the first row blanked (the gate still works; the defect is the non-repo-relative path).
- L3's HOME regex (counter line 62, `HOME_RE`) bans only `~/`, `$HOME`, `${HOME}`, `/home/`; any other absolute path passes.

**S5. `stale-base-line` (L5 excludes recheck lines; L1/L2/L3 read the first recheck line only).** Edit: the BASE claim-gates line `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-gates.md  # on-restoration …` is kept, placed after the new recheck line.
- Result: `mutant=stale-base-line rejected=0`, `fixed=7/7 exit=0`.
- Witness: verbatim exits `[0, 1]` intact (the second, stale line is gated); `[1, 1]` with the first row blanked.
- `recheck_line` (counter lines 78–83) returns the first match; L5 (lines 198–199) drops every `RECHECK_RE` line before comparing; `recheck-audit.py` audit_entry (lines 112–116) also breaks at the first match.
- The claim's own plain check disagrees with the counter: `grep -lE '^recheck:.*test -d ~/Projects/' corpus/knowledge/*.md | wc -l` printed `base: 23`, `good: 21`, `mut/stale-base-line: 22` (target ≤21).

**S6. `claim-mismatch` (row-to-claim link; semantic, by design of the counter).** Edit: G3's claim cell `Hard gates are written_scope, authorization, evidence_integrity, no_duplicate_or_prior_submission` → `Custodian receipts must name a matched_grant_id on every action`. Anchor `claim-package-check.py:124-126` and token `evidence_integrity` unchanged.
- Result: `mutant=claim-mismatch rejected=0`, `fixed=7/7 exit=0`.
- Witness: anchored lines 124–126 are `'written_scope',`, `'authorization',`, `'evidence_integrity',`, which do not support the new claim. Blanking the token still turns the entry red (L6 holds), so the counter sees a load-bearing row attached to the wrong claim.
- The freeze kill-rule already routes this to a non-author reading ("the rows are the semantic check the counter cannot make"); it is recorded here as a survivor so the 7/7 read is not taken as semantic support.

## Controls (must be rejected; all were)

- `soft-unrelated-entry`: `claim-anatomy-sample.md` (a still-gated entry, not re-grounded) gets ` || true` before its comment. `mutant=soft-unrelated-entry rejected=1`, `fixed=3/7 exit=1`, `gate L3 pass=0 read=bad=claim-anatomy-sample.md`. Contrast: the same edit on a re-grounded entry (S1) survives. This shows L3 does gate softening on unrelated entries and not on re-grounded ones.
- `single-reground`: claim-package-contract reverted to BASE bytes. `mutant=single-reground rejected=1`, `fixed=5/7 exit=1`, `failed_limbs=L1,L2`, `gate L2 pass=0 read=base-gated=24 regrounded=1 claim-gates.md`.
- `recheck-deleted`: claim-gates new recheck line deleted. `mutant=recheck-deleted rejected=1`, `fixed=0/7 exit=1`, all seven gates `exception-KeyError`.
- `broken-line`: claim-gates recheck gets an unbalanced double quote. `mutant=broken-line rejected=1`, `fixed=6/7 exit=1`, `gate L1 pass=0 read=gated=22 broken=1 lines=64/base=64`.

## Summary as printed by the recipe

```
mutant=abs-counter-path rejected=0 fixed=7/7 category=survivor
mutant=cd-tilde rejected=0 fixed=7/7 category=survivor
mutant=claim-mismatch rejected=0 fixed=7/7 category=survivor
mutant=comment-shape rejected=0 fixed=7/7 category=survivor
mutant=soft-or-true rejected=0 fixed=7/7 category=survivor
mutant=stale-base-line rejected=0 fixed=7/7 category=survivor
mutant=broken-line rejected=1 fixed=6/7 category=control
mutant=recheck-deleted rejected=1 fixed=0/7 category=control
mutant=single-reground rejected=1 fixed=5/7 category=control
mutant=soft-unrelated-entry rejected=1 fixed=3/7 category=control
```

## Cross-check: the lane's strict recheck audit (static predicates, recheck-audit.py limbs d–f)

`cmp` shows the lane's `corpus/instruments/recheck-audit.py` equals the base copy. I imported it without running any recheck line and evaluated its own regexes and limb expressions (`CD_RE` line 87, `cdroot` line 137, `instrument` line 140, `own` line 147) on each mutant's claim-gates line:

```
GOOD             recheck_lines=1 cd_target=/home/vgpnk/Projects/shokunin/kasegi-shokunin cdroot_vs_lane=True instrument=True own=True
soft-or-true     recheck_lines=1 cd_target=/home/vgpnk/Projects/shokunin/kasegi-shokunin cdroot_vs_lane=True instrument=True own=True
comment-shape    recheck_lines=1 cd_target=/home/vgpnk/Projects/shokunin/kasegi-shokunin cdroot_vs_lane=True instrument=False own=True
cd-tilde         recheck_lines=1 cd_target=~/Projects/shokunin/kasegi-shokunin cdroot_vs_lane=False instrument=True own=True
stale-base-line  recheck_lines=2 cd_target=/home/vgpnk/Projects/shokunin/kasegi-shokunin cdroot_vs_lane=True instrument=True own=True
abs-counter-path recheck_lines=1 cd_target=/home/vgpnk/Projects/shokunin/kasegi-shokunin cdroot_vs_lane=True instrument=True own=True
claim-mismatch   recheck_lines=1 cd_target=/home/vgpnk/Projects/shokunin/kasegi-shokunin cdroot_vs_lane=True instrument=True own=True
```

So `cd-tilde` (cdroot) and `comment-shape` (instrument) are caught by the audit's strict limbs and not by the counter. `soft-or-true`, `stale-base-line` (first-match only), `abs-counter-path` and `claim-mismatch` pass the audit's strict limbs too. The gap is therefore in the counter, and in part in the audit's first-match reading.

## Routed defects (not applied; the counter is not edited here)

1. L3 should judge the recheck line by running it. The line must exit 0 with rows intact and non-zero with one token blanked (the witness above), and it should reject trailing `||`, `;`, and anything after a `#`. A substring test cannot do this.
2. L3/L5 should require exactly one `^recheck:` line per entry (or count all of them). Today the counter reads the first, L5 ignores all, and the claim's plain grep still sees the stale one.
3. The cd target should be checked (equal to the audited root, not `~`), since the counter strips it before every run (counter line 163).
4. The semantic row-to-claim link stays a non-author reading (kill_rule); no counter change can close S6.

## Limitations

- Mutation run on my own hand-built GOOD fixture, not on the lane's committed tree. The GOOD rows were checked only against the anchor lines I read (`claim-package-check.py` 91–98, 101–114, 120–126, 305, 460; `claim-package-selftest.py` 77); their semantic support is not judged here.
- HOME is an isolated scratch directory; the `~`-cd witness was also run with the real HOME, which resolves the cd into the live lane (read-only: the counter's entry mode, which exited 1 because the lane's claim-gates has no re-ground section yet). No lane file was written.
- Lane HEAD is `323d1f5…`, not the freeze commit `9f23aab…`. I did not check out or change anything; the counter bytes match the freeze sha.
- Recipe, scratch fixtures and run output lived under `/fast/scratch/hyaku/kasegi-r46/`, removed on exit. The mutant definitions above are the exact edits; the recipe itself is not committed.
- Only the L1–L3 mutation surface was probed; L4–L7 were exercised only as far as the mutants touched them.
