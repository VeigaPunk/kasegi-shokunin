# R44W2Crit07 — append-only attack (round 44, wave 2, falsify)

seat: R44W2Crit07 (critic, read-only) · lane: kasegi · base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` · tree under attack `8063547d0ce647d6f9eafc3c8d0a502616685218`

## Item

For every file this round touched, diff the frozen base `5ab3a60` against commit `8063547` and report any modification of pre-existing lines — a rewrite is a defect, an append is not. Give the diffstat per file.

## Method

1. `git diff --name-status 5ab3a60 8063547` — 112 changed paths: 10 `M`, 102 `A`, 0 `D`, 0 `R`, 0 mode/type changes (`git diff --summary` shows only `create mode` lines).
2. Per-file `git diff --numstat 5ab3a60 8063547 -- <file>` and deletion count `git diff 5ab3a60 8063547 -- <file> | grep -c '^-[^-]'`.
3. Independent check that does **not** rely on git's diff alignment: for each touched file, walk the head blob and confirm every base line is preserved verbatim and in order (insert-only subsequence). All 11 files pass.
4. Byte-level EOF checks (`git show <rev>:<file> | tail -c 8 | od -c`) for the trailing-newline question (routed defect 6).
5. Counter re-runs and rewrite mutants against exported trees (`git archive` of both revs into scratch).

## Result — per-file diffstat (base `5ab3a60` → head `8063547`)

| file | diffstat | deletions | shape |
|---|---|---|---|
| `LOG.md` | 23+/0− | 0 | tail append (`@@ -1963,0 +1964,23 @@`) |
| `SCORECARD.md` | 17+/0− | 0 | tail append (`@@ -1689,0 +1690,17 @@`) |
| `SHONEN.md` | 11+/0− | 0 | tail append (`@@ -292,0 +293,11 @@`) |
| `SKILL.md` | 10+/0− | 0 | tail append (`@@ -1134,0 +1135,10 @@`) |
| `PROVINCE.md` | 2+/0− | 0 | tail append (`@@ -165,0 +166,2 @@`) |
| `corpus/README.md` | 20+/0− | 0 | tail append (`@@ -612,0 +613,20 @@`) |
| `corpus/SOURCES.md` | 7+/0− | 0 | **4 hunks — 3 mid-file insertions** (see F2) |
| `corpus/instruments/README.md` | 16+/0− | 0 | tail append (`@@ -977,0 +978,16 @@`) |
| `corpus/lessons/round-43.md` | 10+/0− | 0 | tail append (`@@ -165,0 +166,10 @@`) |
| `corpus/lessons/round-44.md` | NEW, 152+/0− | n/a | new file; no pre-existing lines exist |
| `corpus/instruments/knowledge-expected.txt` *(not in the seat's list — see F1)* | 1+/0− | 0 | tail append |

**Verdict on the named item: the append-only discipline HOLDS at the committed tip.** Zero deletions across all 112 changed paths; every base line of every touched file is preserved verbatim and in order. I found **no modification of any pre-existing line** and could not falsify the item's core claim.

## Findings

### F1 — the seat's enumerated file list omits a touched file (coverage)

The item names ten files; the round also modified `corpus/instruments/knowledge-expected.txt` (`git diff --name-status 5ab3a60 8063547 | grep '^M'` → 10 entries, nine of them in the list). The omitted file is insert-only (+1/0−, the new `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` line), so no defect — but the list itself is incomplete.

### F2 — `corpus/SOURCES.md` is not a tail append; three mid-file insertions

Hunks: `@@ -74,0 +75,2 @@` (S069/S070 rows inserted into the registry table after S068, before `## Paths`), `@@ -83,0 +86 @@` (S069 bullet appended at the end of the `## Paths` list), `@@ -101,0 +105,2 @@` (round-44 sweep bullet appended at the end of the `## Search log` list), `@@ -147,0 +153,2 @@` (change-log entry at EOF). No pre-existing line was touched; the registry rows must sit inside the table in id order, so mid-file insertion there is required, not a rewrite. A naive "append-only = single tail hunk" check would mis-flag this file; the correct criterion (no pre-existing line modified) holds. Minor: the new Paths bullet sits directly against the `## Search log` heading with no blank line — the base already had that shape (`- Exploitation likelihood…` → `## Search log`), so nothing new was broken.

### F3 — routed defect 6's lost byte is restored, append-only

Base `5ab3a60` `SHONEN.md` ends `` `[~]`.\n `` (the byte lost in round 43's `0a24364d`); head `8063547` ends `` `[~]`.\n\n `` — identical to the pre-loss tail at `ab98fac9` (`` `[~]`.\n\n ``). The restoration is an append: the base's last content line is preserved verbatim (subsequence check) and the trailing blank line is new content at EOF. `r44-routed-defects.py` limb D6 (`data.endswith(b"\n\n")`) is satisfied.

### F4 — the C1 counter does not grade append-only globally (evidence-discipline gap)

The counter's docstring claims: *"Append-only is enforced where the protocol demands it: a correction must sit AFTER the text it corrects, and the corrected text must still be there."* Enforcement is limb-local only — D1 (round-43 row still carries `13/19`, correction sits after it) and D3 (the original `29-character prefix` sentences still present). No limb or selftest case grades the append-only property of the other touched files, and the selftest's 11 cases contain no rewrite mutant.

Four mutants built from the committed head tree, each an in-place rewrite/deletion of pre-existing lines, all still grade `fixed=8 unresolved=0 exit=0`:

| mutant | pre-existing content destroyed | counter result |
|---|---|---|
| M-A | `corpus/README.md` round-43 line `ratio is unchanged: 25/25 admitted` rewritten in place to `26/26` | `fixed=8 unresolved=0 exit=0` |
| M-B | pre-existing `SKILL.md` line 2 (`description: Domain specialist — bounty & security research…`) deleted | `fixed=8 unresolved=0 exit=0` |
| M-C | `corpus/SOURCES.md` S067 row's status cell rewritten `mined` → `rejected` in place | `fixed=8 unresolved=0 exit=0` |
| M-D | pre-existing `SCORECARD.md` round-43 `coverage` move-log row deleted | `fixed=8 unresolved=0 exit=0` |

So C1's after-claim *"all eight have append-only fixes"* is **true of the committed tree** (this audit) but is **not proven by the committed counter** — it is an ungraded property that happened to hold. This is a coverage gap in the counter, not a false claim about the tree.

### F5 — the committed tip's SCORECARD.md round-44 record is stale against its own commit

At `8063547`, `SCORECARD.md`'s appended `## Round-44 capability disposition` rows record `4 held; C1 unverified, no delta` and `8 held; C2 unverified, no delta`, citing `.ufo/waves/round-44/controls/r44-counter-trial-disposition.txt` (the *rejected* draft counter's disposition). The same commit lands the fail-closed `corpus/instruments/r44-routed-defects.py`, which I re-ran against an export of that very tree: `routed-defects total=8 fixed=8 unresolved=0 exit=0` (and `--baseline` replay `fixed=0 unresolved=8` at `5ab3a60`; selftest `cases=11 failures=0`). `LOG.md` (committed) carries both the attempt-1 and attempt-2 records; `SCORECARD.md` carries only attempt 1. The attempt-2 move-log rows exist only as an **uncommitted working-tree edit** (`git status --porcelain` → ` M SCORECARD.md`), and that edit cites an **untracked** control `.ufo/waves/round-44/controls/c1-counter-at-commit-A.txt`. A reader at the committed tip sees a report-level record that contradicts the instruments committed in the same tree.

### F6 — the frozen C2 counter string is defective (disclosed in-tree)

`grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md` (the frozen counter in `.ufo/waves/round-44/claims.json` C2) prints **0 at the frozen base and 0 at the after tree** — the frontier table's status is its third cell. The committed `SCORECARD.md` block and the substitute counter's docstring both disclose this; `corpus/instruments/r44-frontier-count.py` measures the same declared predicate table-aware: base `frontier rows=25 admitted=25 … verdict=SHORT exit=1`, head `frontier rows=26 admitted=26 exit=0`. C2's kill rule ("a do-nothing replay cannot reach F26") holds under the substitute, but the frozen counter string itself can never reach F26 in either world.

## Verification of the appended C2 evidence (spot-check)

`corpus/source-snapshots/round-44/S069.txt` sha256 `0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2`, 45,681 bytes — matches the S069 row's pin and `manifest.json`. Manifest quote anchors resolve within wrapped-line windows: Q1→61-62, Q2→62-63, Q3→70-72, Q4→76-77, Q5→10-11 (the S069 row's "Q5 lines 9–11" is a superset locator; the quote starts at line 10).

## Limitations

- Read-only seat: I did not re-open the S069 source live; the digest and quote anchors are verified against the committed capture only.
- The uncommitted `SCORECARD.md` working-tree edit is in-flight L1 work; I audited the committed tip `8063547` only and made no edits anywhere.
- I did not audit the wave1/wave2 seat transcripts (out of this item's scope).
- F4's mutants show the counter's blind spot; they do not show the committed tree violates append-only — it does not.

## Tooling

None installed or updated; pacman was not invoked.

## Scratch

`/fast/scratch/hyaku/kasegi-r44/R44W2Crit07` — removed before yield.
