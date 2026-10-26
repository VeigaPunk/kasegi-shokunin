# RevNoHarmDiff — round 39 wave 2 (falsify), no-harm verification receipt

Seat: RevNoHarmDiff (leaf, reviewer). Date: 2026-10-26.
Base `480b1a505a2dfc14a4f718d16d63808247214d0a`; claims freeze `dcd31701720a6a4929a32471a62011ed87103421`; lane tip (verified at run time) `5006097a84305267c9a3e8c1e1d560e60fe41d37`.
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Fleet: /home/vgpnk/Projects/shokunin.
I am not an author of the round-39 deliverables; attack posture on the no-harm controls only.

**Verdict: NO HARM FOUND.** The lane tree diff base→tip outside `.ufo` is additions-only (0 deletions on every file), all eight protected files are untouched on their base lines (pure appends), and the fleet root carries zero untracked files of any origin. One convention observation (SKILL.md instrument registration) is recorded below; it is not a base-line harm.

## Check 1 — lane diff numstat, zero deletions

Command: `git -C <lane> diff --numstat 480b1a50…d0a 5006097a…d37 -- ':!.ufo'` plus `awk '$2!=0'` over the same.

```
15	0	LOG.md
2	0	PROVINCE.md
49	0	SCORECARD.md
15	0	SHONEN.md
17	0	corpus/QUALITY.md
28	0	corpus/README.md
10	0	corpus/SOURCES.md
1	0	corpus/instruments/knowledge-expected.txt
1793	0	corpus/instruments/r39-closure.sh
144	0	corpus/knowledge/cisa-when-to-issue-vex.md
28	0	corpus/knowledge/considerthese-proposals-ledger.md
2	0	corpus/lessons/round-38.md
84	0	corpus/lessons/round-39.md
275	0	corpus/source-snapshots/round-39/S057.txt
74	0	corpus/source-snapshots/round-39/manifest.json
files_with_deletions=0
```

`git merge-base --is-ancestor` base tip → `YES ancestor`. `diff --name-status` shows only `M` and `A` (no D/R/T); `awk '$1=="-"'` over numstat shows no binary rows. Added lines per file are the first numstat column above (15 files, 2180 added lines total, 0 deleted).

## Check 2 — protected files, no modification of base lines

Per protected file: existence at base and tip via `git cat-file -e <commit>:<path>`, minus/plus lines via `grep -cE '^-[^-]'` / `grep -cE '^\+[^+]'` on `git diff base tip -- <path>`, numstat for the authoritative count.

```
SKILL.md        base=yes tip=yes numstat=(no diff)  plus_lines=0  minus_lines=0
PROVINCE.md     base=yes tip=yes numstat=2/0  plus_lines=1  minus_lines=0   (plus undercounts blank added lines; numstat authoritative)
corpus/README.md  base=yes tip=yes numstat=28/0 plus_lines=23 minus_lines=0
corpus/SOURCES.md base=yes tip=yes numstat=10/0 plus_lines=9  minus_lines=0
corpus/QUALITY.md base=yes tip=yes numstat=17/0 plus_lines=13 minus_lines=0
LOG.md          base=yes tip=yes numstat=15/0 plus_lines=11 minus_lines=0
SHONEN.md       base=yes tip=yes numstat=15/0 plus_lines=10 minus_lines=0
SCORECARD.md    base=yes tip=yes numstat=49/0 plus_lines=26 minus_lines=0
```

Hunk headers confirm appends after 3-line context with no removals: LOG `@@ -1700,3 +1700,18`, README `@@ -154,3 +154,5`, SCORECARD `@@ -1528,3 +1528,52`, SHONEN `@@ -185,3 +185,18`, QUALITY `@@ -290,3 +290,20`, PROVINCE `@@ -484,3 +484,31`, SOURCES `@@ -59,6 +59,10` and `@@ -120,3 +124,9`. The PROVINCE addition is the declared `[r39 Frontier amendment, appended 2026-10-26, end-of-file append per R6]` F22 block. SOURCES row insertions sit at the tail of the registry table and add S057 (mined) then S056/S058/S059 (rejected) plus 6 changelog lines; the appended changelog itself states S001–S055 cells untouched, and the 10/0 numstat corroborates. SKILL.md has zero diff this round — trivially no base-line modification.

## Check 3 — fleet root byte-clean of kasegi misroots

Command: `git -C /home/vgpnk/Projects/shokunin status --porcelain` → **empty output, exit 0** (untracked count 0). No kasegi-authored files anywhere at fleet root.

## Check 4 — corroborating state

- Lane working tree: `git status --porcelain` lists only wave machinery under `.ufo/waves/round-39/` (`wave2/`, `wave2-dispatch.json`, `kasegi-r39-falsify.ready`, `kasegi-r39-falsify.ready.dispatched`, `wave2-run.err`) — all inside the excluded `.ufo`, none in the source tree.
- E4 consistency: `git diff --name-only 46c66c2 5006097` = `.ufo/waves/round-39/final-gates/all-gates.txt` exactly — tip Y = J + receipt only, as the erratum defines.
- Frozen claims.json and claims-erratum-1.md read before checking; not edited.

## Observations (not harms; for the round's ledger)

1. **SKILL.md instrument registry carries no r39-closure.sh row.** The round adds `corpus/instruments/r39-closure.sh` (1793 lines) and names it in LOG/SCORECARD/SHONEN/QUALITY, but SKILL.md's instrument table ends at the r38 row (`grep -c 'r39-closure' SKILL.md` at tip → 0). Precedent is mixed (the r35 row notes "exact-basename registration round 36", i.e. deferred one round; r37/r38 rows registered in-round), so this may be intentional next-round registration — flagged, not scored as a defect by this seat.
2. SOURCES.md lists the newly mined S057 row above the rejected S056 row (ID order S057, S056, S058, S059). Counters are grep-based (E1: 59) so no measurement is affected.
3. Residual risk: this seat verified committed bytes and tree hygiene only; it did not re-run the C1 suite or C2 counters (other seats own those). Scratch ran under /fast (617G free, disk guard green).

## Tooling

No tools installed or upgraded (read-only git + coreutils sufficed). No pacman, no network fetches. Scratch `/fast/scratch/hyaku/kasegi-r39/RevNoHarmDiff` removed after this receipt was written; no other writes outside the permitted receipt path.
