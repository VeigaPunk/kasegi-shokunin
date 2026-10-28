VERDICT: INFO

# R45Simplifier — YAGNI pass over frozen round-45 instruments (advice only, no edits)

Scope: `corpus/instruments/r45-routed-defects.py` (C1, 272 lines), `corpus/instruments/r45-c2-gate.py` (C2, 227 lines), `.ufo/waves/round-45/controls/freeze-controls.py` (109 lines), plus `claims.json` wording. Base rev `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd` exported read-only to scratch. No file in the lane, git index or fleet was touched. Scratch removed on exit.

Line numbers below are for the lane files as committed at the frozen base (the instruments are untracked in the working tree; the same bytes were read).

## 0. Reproduction of the frozen controls (before judging anything)

Command: `python3 .ufo/waves/round-45/controls/freeze-controls.py --base-export $SCR/base --lane $LANE --work $SCR/work` (PYTHONDONTWRITEBYTECODE=1)

Output:
```
control do-nothing-base counter=C1 routed-defects total=5 fixed=0 unresolved=5 exit=1 expect=RED got=RED
control do-nothing-base counter=C2 c2-gate fixed=1/7 exit=1 expect=RED got=RED
control c1-marker-only counter=C1 routed-defects total=5 fixed=0 unresolved=5 exit=1 expect=RED got=RED
control c2-junk-row counter=C2 c2-gate fixed=4/7 exit=1 expect=RED got=RED
control c2-fabricated-quote counter=C2 c2-gate fixed=5/7 exit=1 expect=RED got=RED
controls total=5 red=5 green=0
```
This matches `controls/freeze-controls.txt` line for line. Controls are RED as recorded.

Per-limb reads (run directly on each control tree) show what each control actually trips:

- C1 do-nothing base: `limb R1 fixed=0 read=row-S072=absent`, `R2 ... quality-not-append-only-or-unchanged`, `R3 ... selftest-rc=2-tokens=None`, `R4 ... freeze-check-absent`, `R5 ... refiled-absent`.
- C1 marker-only: `R1 row-S072=absent`, `R2 R47-enforced-by-missing-corpus/instruments/nothing.py`, `R3 selftest-rc=2-tokens=None`, `R4 freeze-check-absent`, `R5 invocation-absent`.
  -> Positive: all five limbs go red for five different reasons. This control discriminates.
- C2 do-nothing base: `gate G1 pass=0 read=rows=26 admitted=26 dup=0`, `G2 F27-rows=0`, `G3 row-S071=absent-or-malformed`, `G4 manifest-absent`, `G5 F27-rows=0`, `G6 knowledge=63`, `G7 pass=1 read=census-rc=0`.
- C2 junk-row: `G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/junk-entry.md`, `G2 pass=1`, `G3 pass=0`, `G4 pass=0 read=manifest-absent`, `G5 pass=0 read=spans=0 located=0 failed=0 cores=0/4`, `G6 pass=1 read=knowledge=64`, `G7 pass=1`.
- C2 fabricated-quote: `G1 pass=1`, `G2 pass=1`, `G3 pass=0 read=row-S071=absent-or-malformed`, `G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`, `G5 pass=0 read=spans=4 located=0 failed=4 cores=0/4`, `G6 pass=1`, `G7 pass=1`.

## 1. Defects in the counter logic (verified by execution)

### 1a. C2 G1 raises IndexError instead of returning a named reason (reachable)
- Attacked: `r45-c2-gate.py:115` `f27 = [r for r in rows if r[0] == "F27"][0]`, which runs after `entry_path()` has already returned `None` for a missing F27.
- Command: fixture = frozen base + one appended row `| F28 | placeholder | admitted | ... |` (27 rows, 27 admitted, no F27), call `g1()`.
- Output: `TEST-A G1 (27 admitted, no F27): (False, 'exception-IndexError: list index out of range')`
- Verdict stays fail-closed (main's `except Exception` at `r45-c2-gate.py:217-218` catches it), but the read token is an exception, not `F27-entry-missing`.
- Advice: test `p is None` (or F27 presence) before indexing at line 115. Behaviour-neutral for the verdict; only the read token changes.

### 1b. C2 G1 line 116 has a dead condition
- Attacked: `r45-c2-gate.py:116` `if f27[2] != "admitted" or p is None:`
- Reasoning (no execution needed): line 116 is reached only when `len(rows) == 27` and `adm == 27` (line 110 counts `r[2] == "admitted"`) and `dup == 0`. Then every row, F27 included, has `r[2] == "admitted"`, so `f27[2] != "admitted"` is always False.
- Advice: drop the `f27[2] != "admitted"` clause; keep `p is None`.

### 1c. C2 `frontier()` returns a second value nobody reads
- Attacked: `r45-c2-gate.py:85` signature and `:91` `return rows, t`. Callers `:95` and `:108` both discard it with `rows, _`.
- Advice: return `rows` only. `t` is dead.

### 1d. C1 `CENSUS` constant is dead
- Attacked: `r45-routed-defects.py:55`. Grep of the file shows this is the only occurrence of `CENSUS`; no C1 limb calls the census script (the census is only used by C2 G7, `r45-c2-gate.py:198`).
- Advice: delete line 55.

### 1e. C1 `run()` parameters never used
- Attacked: `r45-routed-defects.py:71` `env_extra: dict | None = None` and `:73` `env.update(env_extra or {})`, plus the `env = dict(os.environ)` copy at `:72`. Every call site (`:123`, `:189`, `:214`, `:219`) passes only `(cmd, root)`. `subprocess.run` inherits `os.environ` when `env` is omitted.
- Advice: remove `env_extra` and the env copy (`:72-73`, `:75` `env=env`). Keep `timeout` only if L1 wants it; it is never overridden.

### 1f. C1 R2 `or q == qb` clause is redundant for the verdict
- Attacked: `r45-routed-defects.py:153` `... or not q.startswith(qb) or q == qb:`
- Command: `limb_r2(BASE, BASE)` (original) vs same with ` or q == qb:` removed.
- Output: original `(False, 'quality-not-append-only-or-unchanged')`; mutant `(False, 'round-45-heading!=1')`.
- Advice: clause only changes the read token. Drop it or keep it for message clarity; verdict is identical.

### 1g. C1 R4 `os.path.exists(fc)` pre-check is redundant for the verdict
- Attacked: `r45-routed-defects.py:212-213`.
- Command: `limb_r4(BASE, BASE)` original vs with the 2-line pre-check removed.
- Output: original `(False, 'freeze-check-absent')`; mutant `(False, 'selftest-rc=2-tokens=None')`.
- Advice: same as 1f; `run()` already fails closed on a missing script. Drop or keep for the message.

### 1h. Duplicated token regex
- Attacked: `r45-routed-defects.py:112` and `:137`, both `r"(?<![0-9])10[ ,]?029(?![0-9])"`.
- Advice: hoist to one module constant (cosmetic; avoids the two copies drifting).

## 2. Conditions that do not discriminate

### 2a. C2 G6 (knowledge count == 64) is satisfied by any added .md file
- Attacked: `r45-c2-gate.py:192-194`.
- Evidence: the junk-row control (which adds only `junk-entry.md`, no sources) prints `G6 pass=1 read=knowledge=64`. G1 (`:107-118`) and G2 (`:121-129`) also pass on the junk tree (`G1 pass=1 ... entry=corpus/knowledge/junk-entry.md`, `G2 source=1 verified-at=1 recheck=1`).
- Advice: G6 is a structural count, not a content check. It is not wrong to keep (the claim wording says "64 total"), but it adds no evidence beyond G2/G5. Note it in the claim, not as a discriminator.

### 2b. C2 G4 `"BROKEN" not in out` is probably redundant with `rc == 0`
- Attacked: `r45-c2-gate.py:165`.
- Evidence: `source-recheck.py:17` documents a broken anchor as "(exit 1)"; `source-recheck.py:392` returns `0 if failed == 0 else 1`.
- Limitation: I did not build a broken-anchor fixture to exercise this. Treat as "likely redundant on the documented contract", not verified.

### 2c. C2 G2 `len(h) > 10` is an undocumented magic constant
- Attacked: `r45-c2-gate.py:128` `ok_r = any(h.startswith("recheck:") and len(h) > 10 for h in head)`.
- Effect: a bare `recheck:` (8 chars) and `recheck: x` (9 chars) fail; `recheck: ab` (11 chars) passes. The claim says only "a `recheck:` line".
- Advice: either document the threshold or drop it. Dropping it would accept a bare `recheck:`, so that is a predicate decision for L1, not a simplification. I am not proposing it.

### 2d. C2 G3 keeps the last matching S071 row and never checks duplicates
- Attacked: `r45-c2-gate.py:139` `row = c` inside a loop (last match wins). G1 does check duplicate F-ids (`:111`); G3 does not check duplicate S071 rows.
- Advice: inconsistency, not a complexity problem. Noted for L1.

### 2e. freeze-controls fabricated-quote control is not isolated to G5
- Attacked: `freeze-controls.py:85-97` (c2-fabricated-quote tree). The control has no S071 row, so G3 fails too.
- Evidence: `G3 pass=0 read=row-S071=absent-or-malformed` alongside `G5 pass=0 read=spans=4 located=0 failed=4 cores=0/4`.
- Advice: the RED verdict is correct, but the control does not prove G5 is the discriminating limb. Adding the genuine S071 row to this control would isolate G5. This strengthens the control; it does not widen any predicate.

### 2f. C2 secondary command duplicates G1 on the same predicate
- Attacked: `claims.json` C2 `secondary` (`r44-frontier-count.py --root {tree} --expect 27`).
- Command: `python3 corpus/instruments/r44-frontier-count.py --root $BASE --expect 27`
- Output: `frontier rows=26 admitted=26` / `frontier expected=27 admitted=26 verdict=SHORT exit=1`. This matches the claim's base expectation.
- It measures the same thing as G1 lines 108-113, but via independent code. Keep it as a cross-check if L1 wants independence; drop it if not. It is not a discriminator beyond G1.

### 2g. freeze-controls printed counts are misnamed
- Attacked: `freeze-controls.py:99` `bad = 0`, `:101` `got = ...`, `:102` `bad += 1 if got != "RED" else 0`, `:104` `red=len(rows) - bad green=bad`.
- `bad` counts controls the counter wrongly accepted. Rename to `accepted` or `green` so the code matches the printed `green=`.

### 2h. freeze-controls unused import
- Attacked: `freeze-controls.py:12` `import argparse, os, re, shutil, subprocess, sys`.
- Command: grep `\bre\.` over the file returns no matches. `re` is unused. Remove it.

## 3. Conditions too complex to verify by eye

- `r45-c2-gate.py:175` span extraction: `re.findall(r"“([^”]+)”\s*\(`?S071\.txt:(\d+)(?:-(\d+))?`?", body)`. Nested optional backticks, optional range, optional parentheses, and the silent-skip effect in 4 below. A reviewer cannot tell by eye which citation shapes are counted.
- `r45-c2-gate.py:165` G4 is a five-term conjunction including the `"BROKEN" not in out` string test (see 2b).
- `r45-routed-defects.py:197` R3 SKILL section extraction: `re.search(r"^## Round-45 Gates & probes registry addition.*?(?=^## |\Z)", ..., re.M | re.S)`. A lookahead with `re.S` is harder to verify than splitting on `## `.
- `r45-routed-defects.py:236` R5 invocation: `re.search(r"--root \S+ --selftest --work \S+", t)`. The order of arguments in a receipt is pinned by this regex.
- `r45-routed-defects.py:136-137` R1 correction-line predicate: a list comprehension combining `startswith`, a substring test and the lookaround token regex.

Advice for these: leave the predicates alone in this round (kill-rule forbids post-scoring predicate changes). Document the shapes in the docstring if L1 wants them readable.

## 4. Silent-drop hole in C2 G5 (verified) and claim-wording mismatch

- Attacked: `r45-c2-gate.py:175-182`. Only curly quotes followed by the exact citation shape `(`S071.txt:N[-M]`)` enter `spans`. Quotes in any other shape are not counted as failed; they are not counted at all.
- Fixture: genuine S071 snapshot copied from the lane; the four frozen cores each located at their real lines (`304-311`, `89-96`, `33-40`, `35-42`); entry = those four real spans plus one fabricated quote cited as ``“embargoes last forever for every reporter” — `S071.txt:310` `` (no parentheses).
- Output: `TEST-B 4 real + 1 fabricated, unmatched citation shape: (True, 'spans=4 located=4 failed=0 cores=4/4')`
- Same tree with the fabricated quote moved to the matching shape `(`S071.txt:310`)`: `TEST-B2 ...: (False, 'spans=5 located=4 failed=1 cores=4/4')`
- Real 4-span tree: `TEST-B3 ...: (True, 'spans=4 located=4 failed=0 cores=4/4')`
- Consequence: G5 goes green on a fabricated quote as long as four genuine cited quotes are present and the fabricated one uses another shape.
- Claim wording: `claims.json` C2 `after` says "one new knowledge entry ... whose curly quotes are each located in snapshot lines". G5 only checks curly quotes that carry the citation shape. The claim is broader than the counter.
- Advice (no widening proposed): either narrow the C2 `after` wording to "each cited curly quote" (claim-side, consistent with the counter), or L1 decides whether the counter must count every curly quote. That second option is a predicate change and is L1's call, not mine.

## 5. Claim-wording and provenance observations

- `freeze.txt` records `claims-sha256: bbe40503281c90eb9d70f469d7bac10125b285758ca9675be9894ce6c12c6206`. Command: `sha256` of `.ufo/waves/round-45/claims.json` gives the same value, so the record is currently correct.
- No counter checks it. `r45-routed-defects.py:210-222` (R4) replays `claims` from the candidate tree (`:219`, `root/.ufo/waves/round-45/claims.json`) and checks only the output token `freeze-check claims=2 base_ok=2`. A seat that edits `claims.json` in its own tree would be replayed against its edited copy with no sha comparison. The freeze protection is therefore a human record, not a counter. Advice: L1 should keep the sha check in the freeze step, not in the counter.
- G7 and the dead C1 constant (1d) both point at `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, outside the lane tree, and this path is not pinned in `freeze.txt`. The validate subcommand exists in that script (grep `validate` shows the mode list at `sources-census.sh:12` and `:68`). The verdict of C2 G7 therefore depends on a fleet-root file. Advice: note the dependency in the freeze record or make the path lane-relative.
- C1 R3 `selftest` precondition: `r44-frontier-count.py` has no `--selftest` flag at base. Command `python3 .../r44-frontier-count.py --root $BASE --selftest` prints `r44-frontier-count.py: error: unrecognized arguments: --selftest` and exits 2. This is expected (the lane must add it), recorded so nobody reads the red as a counter bug.

## 6. What is not simplifiable (checked, keep)

- C1 marker-only control: five limbs go red for five different reasons (section 0). Keep.
- C2 G5 `failed == 0` and `len(cores) == len(CORES)` (`:187`) and `nq and` (`:182`): each removes a verdict-changing case. Keep.
- C2 `entry_path` `p is None` guards (`:123`, `:151`, `:171`): reachable when F27 is absent and needed to avoid a TypeError in `p not in row[10]`. Keep.
- C1 R1 `not les_b` (`r45-routed-defects.py:133`, `if not les.startswith(les_b) or not les_b:`): reachable only if the base lesson file is missing; it is a guard, not dead.

## Limitations

- No real final lane tree exists yet (F27 and C1 repairs are not built). All verdict-changing observations use synthetic fixtures derived from the frozen base plus the committed round-45 snapshots.
- `source-recheck.py` broken-anchor contract (2b) is inferred from its docstring; not exercised.
- I did not run a per-condition mutation sweep of R1's ten sub-predicates (out of this YAGNI scope).
- I read, but did not audit, `sources-census.sh`; only its `validate` mode name was confirmed by grep.
- Nothing was committed, staged or written outside this report. Scratch was removed on exit.
