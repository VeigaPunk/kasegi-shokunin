# CritC2Kill — kill-rule attack on C2 (round 28, wave 1)

Seat: CritC2Kill (leaf, coverage axis). Ran 2026-10-25 (UTC). Scratch: `.ufo/waves/round-28/wave1/CritC2Kill/lab/` (logs kept; bulky corpus-tree fixtures pruned per R14 — regen commands below). No production file touched; no claim edited.

**State attacked.** Not PRE-STATE: the C2 build had already landed when this seat ran. Live counters re-measured first, all green — awk=12, entries-citing-S042=1, S042-row grep=1, census exit 0 rows 42 (pre-existing W04 S028/S029 only), harness `entries=15 pass=15 exit=0`. Pre-state extracts (`git show c9f8b115:…`, read-only) used for the forgery baselines. This receipt therefore attacks the **kill rules' discrimination**, not the landed bytes; the landed bytes pass every check proposed below as correction.

## Attempt 1 — frontier awk to 12 by editing an EXISTING row's status: NO PURCHASE (killed)

- Pre-state (base c9f8b115) frontier table: F01–F11, every row already `admitted` (`a1-flip.txt`: 11 rows, statuses F01=admitted … F11=admitted; zero non-admitted rows printed). There is no status to flip up; any edit only decreases the count — tested: F01 `admitted`→`parked` gives awk=10 (`a1-dup.txt`).
- Adjacent forgery that DOES work: appending a byte-copy of the F01 row → awk=**12** with no F12 admitted (`a1-dup.txt`). It also inflates the harness: duplicate row → `entries=15 pass=15 exit=0` with only **14 distinct entry files** (chain run, `live-vs-gaps.txt`: `chain entries=15 distinct=14`, F-id multiset F01×2). The awk counts lines, not ids; the harness counts row cells, not distinct entries.
- Strongest combined form (attempt 1+2+3 chain, `a-chain.txt`): duplicate-F01 README + 3-line stub + appended column-zero S042 row on the pre-state registry → **all four counters green** (12 / 1 / 1 + census exit 0 rows 42 / 15-15-0) with zero capture work, no round-28 manifest, no real entry.
- Caught by: **no executable counter**. Only the kill-rule sentence "a source row appended without an admitted entry citing it" kills it, and only interpretively — the stub is named by no admitted F-row, so it is not an "admitted entry"; nothing mechanical detects that.

## Attempt 2 — entries-citing-S042 = 1 with a Q1-failing stub: succeeds against counter 2 alone; harness kills it only when the stub is the admitted entry

- `grep -lE '^source: S042 '` matches a 3-line stub (`zz-stub-s042.md`): count **1**, no verified-at, no recheck, no quotes, no falsifiable rule (`a-chain.txt`). Counter 2 is Q1-blind by construction.
- If the F12 row names that stub, the harness fails it: `FAIL F12 … problems=no-recheck-line,no-source-selection,no-manifest`, `entries=15 pass=14 exit=1` → kill rule "harness pass < entries" fires (`a2a.out`, `a2-stubs.txt`).
- If NO row names it (chain above), no counter ever reads the file.
- Sharper survivor (`a2b.out`): a **header-complete, contentless** stub (6 header lines, empty body, recheck line copied against the real round-28 manifest) passes `entries=15 pass=15 exit=0` while failing Q1's exact-anchor, Q3 (no verbatim quotes), Q5 (no falsifiable rule). Q1/Q3/Q5 are enforced by the record bar and review, not by any frozen counter — a tradeoff to record, not a lane defect.

## Attempt 3 — census exit 0 with a malformed appended row: blind spot real, documented, NOT reachable to forge C2

Rows inserted INSIDE the Registry section of full scratch corpus copies (`a3-indent2.txt`):
- Malformed row (10 fields) at column 0 → `E01 S099 fields=10`, exit **1**, rows=43. At 1–3 spaces → same E01, exit **1** (parser accepts 0–3; confirmed). Kill rule "census exit != 0" fires.
- Same row indented **4 or 8 spaces → invisible**: validate exit **0**, census rows stays 42, no finding (`j4`, `j8`). A valid-shaped `S043` row at 4 spaces is equally invisible (`jhid`: rows=42, no finding, claim grep=0). This is the script's documented CommonMark rule ("4 or more spaces are indented code and ignored", sources-census.sh:40-42) — a fleet-instrument tradeoff, not a kasegi bug.
- Reachability: **cannot forge any C2 after-value.** The S042 row must match `^\|[[:space:]]*S042…` (column zero) AND be census-counted in rows=42; an indented row is invisible to both. The blind spot only lets garbage hide (a false-clean "census exit 0") or plants a row-shaped duplicate authority invisible to E03/E11. Live registry and README have **zero** 4+-space row-shaped lines (`live-vs-gaps.txt`: 0/0).

## Attempt 4 — harness 15/15 with the recheck pointing at the wrong manifest (R12): two variants KILLED, two SURVIVE — the real defect

Scratch corpora, only the F12 entry's recheck line rewritten (`a4-wrongmanifest.txt`):
- Old manifest (round-26, lists S041 only) with `--source S041 --source S042` → `FAIL manifest-missing-ids`, exit 1. **Killed** (R12's "the named manifest must list them" holds).
- Right manifest, `--source S041` only vs declared S041+S042 → `FAIL header-sources-not-rechecked`, exit 1. **Killed** (ids-differ clause holds).
- **Survivor 4c**: byte-identical manifest+captures duplicated to `corpus/source-snapshots/round-28-alt/` → `PASS entries=15 pass=15 exit=0`, receipt `manifest=corpus/source-snapshots/round-28-alt/manifest.json`. No kill-rule clause fires: ids equal the declared set, the manifest lists them, quotes are exactly-once in the duplicate too. The frozen predicate names `corpus/source-snapshots/round-28/manifest.json`; **no counter and no kill rule binds the path** — duplicate pinning authority is unconstrained.
- **Survivor 4d**: manifest+captures copied OUTSIDE the repo, `--manifest /tmp/critc2-outside/manifest.json` (absolute) → `PASS 15/15`. The harness imposes no containment on the manifest argument, so the pinned captures need not live under `corpus/` nor in git at all; R14's "receipts and digests in git" is prose-only here. False-provenance class.
- Live bytes NOT implicated: F12 receipt record `manifest=corpus/source-snapshots/round-28/manifest.json` (relative), entries=15 distinct=15 (`live-vs-gaps.txt`).

## Incidental (no kill impact)

A frontier row whose entry cell names a nonexistent file crashes the harness with an unhandled `FileNotFoundError` traceback, exit 1 (`crash.out`) — fail-closed, but not the documented clean `exit 2` read-error receipt.

## Verdict for the judge

- Attempts 1 (as literally posed), 4a, 4b: killed by existing rules; attempt 3: documented tradeoff, unreachable for C2.
- **Counterexamples that survive every executable counter**: (i) the duplicate-frontier-row chain reaching all four after-values with zero work (`a-chain.txt`), killed only by interpreting "admitted entry"; (ii) wrong-path / outside-repo manifest passing 15/15 (`w4c`, `w4d`). Both are fixable counter-discrimination defects, not grounds to reject the landed C2 — the landed bytes pass all corrections below.
- Smallest safe corrections for the L1 (appended receipts/lesson; claims.json stays frozen per R9):
  1. From the harness JSON receipt: assert `len(entries)==len(distinct entry paths)==15`; assert the single F12 record's `manifest == 'corpus/source-snapshots/round-28/manifest.json'` (relative, not `/`-leading).
  2. `awk -F'|' '$2 ~ /^ *F[0-9]+ /{gsub(/ /,"",$2); print $2}' corpus/README.md | sort | uniq -d` prints nothing (F-id uniqueness).
  3. `diff <(grep -lE '^source: S042 ' corpus/knowledge/*.md) <(echo corpus/knowledge/japanese-domestic-disclosure-workflow.md)` (counter-2 file is the admitted entry).
  4. `grep -cE '^ {4,}\|' corpus/SOURCES.md corpus/README.md` → 0 0 (hidden-row sweep).

## Evidence index (all under `.ufo/waves/round-28/wave1/CritC2Kill/lab/`)

`a1-flip.txt`, `a1-dup.txt`, `a-chain.txt`, `a2-stubs.txt`, `a2a.out`, `a2b.out`, `a3-indent.txt`, `a3-indent2.txt`, `j{0,3,4,8,hid}.out`, `a4-wrongmanifest.txt`, `w4{a,b,c,d}.out`, `crash.out`, `live-vs-gaps.txt`, fixtures `zz-stub-s042.md`, `zz-stub2-s042.md`, `dup-README.md`, `flip-README.md`, `pre-README.md`, `pre-SOURCES.md` (base-revision extracts). Regen: duplicate full `corpus/` into a scratch dir per variant, apply the described one-line mutations (dup F01 row / stub entry / indented registry row / rewritten recheck line), run `python3 corpus/instruments/frontier-recheck-count.py --root <scratch>` and `scripts/sources-census.sh validate --today 2026-10-25 <scratch>`; census runs used explicit-dir mode, same parser and file bytes as the frozen `--root` invocation.
