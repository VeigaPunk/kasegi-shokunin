VERDICT: INFO

# R46Simplifier: YAGNI pass over the frozen round-46 instruments

Scope: `corpus/instruments/r46-c1-gate.py`, `corpus/instruments/r46-c2-gate.py`, `.ufo/waves/round-46/controls/freeze-controls.py`, frozen at 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5. Advice only. No lane file was edited, nothing was committed or staged, no git mutation ran. The only write is this file. No limb is proposed to widen and no control to weaken.

Line numbers below refer to the frozen bytes. Experiments ran in a scratch root that is removed on exit. Fixture and variant outputs are quoted from my runs; the scratch paths are not citable.

## 0. Frozen bytes and the controls re-run

Command: `sha256sum` of the working copy versus `git show 9f23aab…:<path> | sha256sum` (read-only).

```
corpus/instruments/r46-c1-gate.py worktree=b0c730c834b4d7c6 freeze=b0c730c834b4d7c6
corpus/instruments/r46-c2-gate.py worktree=0ee958578b592370 freeze=0ee958578b592370
.ufo/waves/round-46/controls/freeze-controls.py worktree=6560c0f209a3e17c freeze=6560c0f209a3e17c
```

Command: `python3 .ufo/waves/round-46/controls/freeze-controls.py --lane <lane> --base 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba --work <scratch>/controls/work`
Result: exit 0. Output diffed line for line against `controls/freeze-controls.txt` is identical. Last line: `controls total=9 red=9 green=0`.

## 1. Safe deletions (dead code; no reading changes on any frozen control)

Each item below is either unreachable or inactive at freeze. Removing it does not change any printed reading. After the deletion, re-run freeze-controls.py and expect identical output. Any difference means the deletion was wrong.

**S1. `r46-c2-gate.py:66-67`, the `R46_PINS_OVERRIDE` hook.**
- Evidence: `grep -rn "R46_PINS_OVERRIDE" --include=*.py --include=*.md --include=*.txt --include=*.json` in the lane prints only lines 66 and 67. There is no caller and no selftest.
- The comment says a null value disables one pin. So when the variable is set, the hook can switch off a pinned limb (e.g. `base-knowledge-content`, line 289). It is a latent weakening route with no user. Deleting it tightens the counter and changes no reading.

**S2. `r46-c2-gate.py:61`, `"F28-row": None`.**
- Evidence: `grep -n 'F28-row'` finds only line 61 and the message string at line 178. The key is never read.

**S3. `r46-c2-gate.py:176-178`, the raw-row check, including `or (False)`.**
- Line 177 `if len(raw) != 1 or (False):` is the leftover of a removed pin. `(False)` is always false.
- The check is also unreachable as a verdict. The raw count is taken from `live_lines(README)` with `^\| F28 \|`, the same source and regex that `frontier()` (lines 130-131) uses. By the `r[0]` split in line 132, `r[0] == "F28"` holds exactly for those lines. `entry_path()` (line 151) already requires exactly one F28 row. The check runs only after `entry_path` returned a path (lines 172-175).
- Fuzz (my run): 400 random READMEs drawn from 10 F28-like line variants (duplicates, extra spaces, `F028`, fenced, commented). In the 122 cases where `entry_path`'s F28 count was 1, the raw count was 1 in all 122.

**S4. `r46-c2-gate.py:174`, `f27[2] != "admitted"`.**
- Line 170 already fails unless `adm == 28 == len(rows)`. `adm` counts rows whose third cell is `admitted`. So every row is admitted, F28 included.

**S5. Inactive pin branches, `r46-c2-gate.py:59, 187-188` (`PINS["entry"]`) and `60, 217-218` (`PINS["S073-row"]`).**
- Both pins are `None` at freeze (lines 59-60). The branches run only with S1 active. These are the "pins used to be" remnants. Delete with S1.

**S6. Dead return values and variables.**
- `r46-c2-gate.py:133` returns `(rows, t)`. Every caller discards `t` (`rows, _ =` at lines 149 and 166).
- `r46-c2-gate.py:282`, `p, why = entry_path(root)` in g6; `why` is never read.

**S7. `r46-c1-gate.py:126`, the abs/rel conditional in `entry_mode`.**
- `os.path.join(root, entry)` already returns an absolute path for an absolute `entry`. So the single call covers both branches.
- Command (my run):
```
A relpath corpus/knowledge/a.md same= True -> corpus/knowledge/a.md
A relpath /x/root/corpus/knowledge/a.md same= True -> corpus/knowledge/a.md
A relpath /y/a.md same= True -> ../../y/a.md
A relpath corpus/instruments/b.md same= True -> corpus/instruments/b.md
```

**S8. `r46-c1-gate.py:136, 139, 212`, the `if r` / `r[0] if r else "?"` guards.**
- `section_rows` (lines 96-97) appends only lists built from a line that matched `^\|\s*G\d+\s*\|`. Such a list is never empty, so the guards are always true.

**S9. `r46-c1-gate.py:143`, the `bool(rows) and` prefix.**
- `len(rows) >= MIN_ROWS` with `MIN_ROWS = 6` (line 56) already implies non-empty.

**S10. `r46-c1-gate.py:182`, the conjunct `len(gt) == len(gb) - len(reg)`.**
- Given `not (gt - gb)`, the equality always holds, because `reg = gb - gt`. This is the only added check on that line.
- Command (my run, all pairs of subsets of a 4-element universe):
```
B L2 pairs 256 disagreements with conjunct removed: 0
```

## 2. Looked unused, but reachable or load-bearing: keep

**K1. `r46-c1-gate.py:212`, the unparsed-row branch that appends `"...:unparsed"` to `survivors`.**
- Not unused. It is reached when a regrounded entry (recheck non-gated, so the entry is in R) has a row that is not a four-cell row.
- It is the only L6 red for that input, because the mutant count still reaches 12 with six valid rows per entry.
- Fixture (my run): two entries with recheck `cd <lane> && true`, six valid two-file rows plus one three-cell row `| G7 | claim | \`corpus/instruments/r46-c1-gate.py:55\` |`.
  - With the label (current counter): `gate L6 pass=0 read=mutants=12 survivors=claim-gates.md:G7:unparsed,claim-package-contract.md:G7:unparsed`, then `c1-gate fixed=4/7 exit=1`.
  - Label removed (`survivors.append` replaced by `pass`): `gate L6 pass=1 read=mutants=12 survivors=none`, then `c1-gate fixed=5/7 exit=1`.
- Removing it would turn L6 green on malformed rows. That is widening, so keep it. Frozen controls never reach it: the label-removed variant re-runs freeze-controls.txt identically (see section 3, last note).

**K2. `r46-c1-gate.py:189, 195, 202, 235`, the `bool(reg) and` guards in L3, L4, L5, L6.**
- Without them, an empty R passes vacuously. The do-nothing control shows the guard working: `freeze-controls.txt:4` reads `gate L3 pass=0 read=recheck-lines-clean=0`, and `freeze-controls.txt:6` reads `gate L5 pass=0 read=append-only=0`.

**K3. `r46-c1-gate.py:110`, the clause `or rel == entry_rel`.**
- None of the seven limbs can reach it. L3, L4 and L6 always pass `corpus/knowledge/<e>` (lines 187, 192, 230).
- It is live for a direct `--entry` on a file under `corpus/instruments/` or `corpus/source-snapshots/`. Fixture (my run): an entry whose rows anchor to itself.
  - Current counter: `reground entry=selfent.md rows=6 ok=3 files=1 exit=1`, with rows G1-G3 `ok=0 read=anchor-dir-or-self`.
  - Clause removed: `reground entry=selfent.md rows=6 ok=6 files=2 exit=0`.
- Keep it, or restrict direct `--entry` to `corpus/knowledge/` as a separate decision. Removing the clause alone would widen direct mode.

**K4. `r46-c2-gate.py:251`, `"BROKEN" not in out`.**
- Reachable. `source-recheck.py:108-114` and `:201-203` print `anchor=N-BROKEN` on an `OK` line for a unique quote with a declared bad anchor, and the exit code stays 0.
- Command (my run): copied round-46 S073 manifest with quote 1's anchor set to 1, then `python3 -I corpus/instruments/source-recheck.py --manifest <copy> --source S073`:
```
rc 0
S073:sha256 OK
S073:Q1 OK occurrences=1 anchor=1-BROKEN
...
BROKEN in output: True
```
- Without this clause, G4 would pass with a broken anchor.

**K5. `r46-c2-gate.py:290`, `sized` (entry ≥ 3000 bytes).**
- It does not discriminate the control it seems built for. `freeze-controls.txt:87` (uncited-filler, 4200 bytes of filler) reads `gate G6 pass=1 read=... entry-bytes-ok=1`.
- It is the only reason G6 is red in junk-row and fabricated-quote (`freeze-controls.txt:67, 77`: `base-names-intact=1 entry-bytes-ok=0`).
- Removing it widens G6. Keep it, but know it is a bare magic number with weak motivation.

**K6. `r46-c2-gate.py:294-297`, G7 (census validate).**
- Green in every C2 reading, including do-nothing (`freeze-controls.txt:58, 68, 78, 88`). It discriminates nothing among the controls. It is a claimed condition ("census exit 0"), so it stays.

## 3. Verdict-adjacent: needs an L1 decision (counter errata rule applies)

The claims' kill rule says a limb sentence may not change after a seat has scored. Anything below that changes a verdict-bearing line must go in `counter-errata.md` with a plain re-derivation.

**D1. `r46-c1-gate.py:223-228`, the L6 fallback for tokens that match only after normalisation.**
- The `if tok in raw` test at line 221 uses the raw backticked token. A double-space token is not literally in the file, so the fallback blanks the entire anchored range. That is broader than "blanking that row's token", which the L6 limb sentence in the counter docstring (`r46-c1-gate.py:34-35`) and the claims C1 "after" text specify.
- Fixture with double-space tokens (`TARGET_GATED  =  22` against the file's `TARGET_GATED = 22`), two anchor files, all rows valid:
  - Current counter: `gate L6 pass=1 read=mutants=12 survivors=none`, then `c1-gate fixed=7/7 exit=0`.
  - Fallback replaced by `pass` (literal token blank only): `gate L6 pass=0 read=mutants=12 survivors=claim-gates.md:G1,...,claim-package-contract.md:G6`, then `c1-gate fixed=6/7 exit=1`.
- On the frozen controls the literal variant re-runs identically to freeze-controls.txt (my run). So the fallback is not exercised by any control. It is a leniency the frozen sentence does not state. Options for L1: keep and document it, or tighten to the literal reading. Either is a decision, not a YAGNI deletion.
- Note for K1 and D1 together: the label-removed variant (K1) and the literal-token variant (D1) each re-ran `freeze-controls.py` with `C1` pointed at the variant; both outputs were identical to `freeze-controls.txt` (exit 0, `identical-to-record: True`). So neither the unparsed label nor the fallback is reached by a frozen control.

**D2. `r46-c2-gate.py:195`, `tbl = len([...]) - 2`.**
- The `-2` offset (for the header and separator) makes an entry with no table read `table-rows=-2` (`freeze-controls.txt:63, 73, 83`). It also counts any line that starts with three pipe-delimited cells.
- Hole, command (my run) on `c2.live_lines` plus the same expression:
```
T1 real 3-col table, 6 rows -> 6
T2 no table -> -2
T3 same + one stray 3-cell prose line -> 7
T4 real table, 6 rows of 2 cells -> -2
T5 table rows inside a fenced block -> -2
```
- So G2's "table-rows >= 6" can be met by 5 real rows plus one stray line. This is a discrimination weakness, not dead code. A fix that counts only real table rows (excluding header and separator by pattern) tightens G2. The frozen controls have no tables, so their verdicts should not change, but the printed read changes from `-2` to `0`. Verify with a full freeze-controls re-run before landing.

**D3. `r46-c2-gate.py:70-83`, duplicated core lists.**
- `CORES` and `MANIFEST_CORES` encode the same five sentences. Each `CORES` pattern is a substring of its manifest sentence. Command (my run): `re.search(core, man)` for each pair gives `True` five times.
- A single list of substrings, `re.escape`d, would remove the duplication. Verdict-neutral in principle; confirm with the freeze-controls re-run.

## 4. Too complex to verify by eye (advice only)

- **C1 L6, lines 203-236.** Three paths from one mutation loop: token blank (221-222), range blank fallback (223-228, D1), unparsed label (211-212, K1). Plus a per-row temp copy of the corpus and per-row subprocess. A reviewer cannot tell which path a row took without running it. A comment naming the three outcomes would help. No logic change needed.
- **C1 L3, line 187 with `HOME_RE` (line 62).** The `cd` prefix is stripped by `CD_RE` (line 61) before `HOME_RE` is applied, and `HOME_RE` also matches `/home/`. The check is a substring test for the script name and the `--entry` path. It does not prove the line runs this file. Acceptable, but needs the reader to know the strip rule.
- **C2 G5, lines 274-275.** `uncited = len(allcurly) - len(spans)` is a difference of two `findall` counts. It is correct only because `spans` is a subsequence of `allcurly` matches. I did not fuzz that property.
- **C2 G2, line 195.** See D2.

## 5. Control-side observations (no widening proposed)

- `freeze-controls.py:113-114` writes the S073 row itself. G3 is therefore green in all three C2 controls by construction (`freeze-controls.txt:64, 74, 84`). Only the absent-row do-nothing (`freeze-controls.txt:54`) exercises G3. A control with a wrong tier or used-by would make G3 falsifiable. This is a strengthening suggestion for L1.
- `c1-one-file` (`freeze-controls.py:76-82`) is the only control that exercises the two-file rule at line 143. Keep.
- `freeze-controls.txt` matches the re-run exactly. No stale record.

## 6. Limitations

- Lines 176-178 and 282 are dead by argument plus the 122-case fuzz. I did not prove unreachability by exhaustive search.
- The L6 fallback (D1) and the `-2` offset (D2) are judgement calls about the claim wording, not defects the controls can see.
- I did not run the full C1 aggregate on the lane tip (F28 is not yet landed). All measurements are on fixtures built from the base export plus the frozen counter bytes.
- Nothing was installed or upgraded. No lane file was touched.
