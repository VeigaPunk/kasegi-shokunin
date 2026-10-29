VERDICT: DRAFT-READY

Seat R46bScoutLedger, round 46 attempt 2, wave 1. Scope: the considerthese-proposals ledger, its round-46 disposition coupling, and the two counter gates that pin/exempt it. Read-only seat: the only bytes written are this report; no lane file was edited, no git/jj mutation anywhere, nothing installed (no tool install was needed).

# Finding 1 — the ledger is content-pinned by r46-c2-gate.py G6 (prior round's finding HOLDS)

Pin location, quoted verbatim from the worktree file `corpus/instruments/r46-c2-gate.py` (byte-identical to the freeze export of `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`; worktree == export sha256 `647bd5b7b62685519d8d396bf2d02eca7ad0bb440dd5c4041beabfaa45ea2909`; header declares "round-46 C2 counter (coverage), v1.2"; last commit `93140c1 round-46: wave-2 fixes (counters v1.2, …)`):

- `:71` — `CONTENT_EXEMPT = {"claim-package-contract.md", "claim-gates.md"}`

  The ledger is absent from this set, so it is one of the pinned names. The G6 docstring `:32-35`: "`find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` == 65, … and the other 64 names are the round-45 tip's; 62 of them are pinned byte for byte, and the two entries claim C1 re-grounds are exempt from the byte pin (names pinned, size may grow never shrink)". Arithmetic: 65 names − 1 entry path (`github-private-vulnerability-reporting.md`, from G1) − 2 exempt = 62 pinned; the ledger is among them. The digest enforced is `PINS["base-knowledge-content"]` at `:66` = `5e0796fd3617f7626880950a5b25d1818f58eff58a12dec99ce7a0f3836b8f47`, computed at `:338` over `base_like` names minus `CONTENT_EXEMPT`.

Commands and printed output (scratch `/fast/scratch/hyaku/kasegi-r46/R46bScoutLedger`, removed; tree exported with `git -C <lane> archive fe0f56b… corpus | tar -x -C $S/freeze`; TMPDIR set explicitly):

1. Do-nothing control — `TMPDIR=$S/tmp python3 $S/freeze/corpus/instruments/r46-c2-gate.py --root $S/freeze`:
   ```
   gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
   c2-gate fixed=7/7 exit=0
   ```
   (all seven gates pass on the unmodified freeze export — a stronger baseline than expected, since attempt 1's integrated tree is the attempt-2 base).
2. Mutant 1 (the lesson's exact feared edit) — appended `\n## Round-46 dispositions (probe — not a landing)\n\nProbe paragraph.\n` to the ledger (30696 → 30766 bytes), same command against `$S/mut1`:
   ```
   gate G6 pass=0 read=knowledge=65 entries=65 nested-md=65 base-intact=0 entry-bytes-ok=1
   c2-gate fixed=6/7 exit=1
   ```
   Only G6 flipped: the pin is load-bearing, exactly as `corpus/lessons/round-46.md:29` states ("editing it would turn C2 red").
3. Exemption contrast — appending one probe line to exempt `claim-package-contract.md` (`$S/mut2`): `c2-gate fixed=7/7 exit=0`, `gate G6 pass=1 … base-intact=1`. The CONTENT_EXEMPT path is the mechanism that keeps edits green.
4. Shrink guard — `truncate -s 100` on exempt `claim-gates.md` (6742 → 100 bytes, `$S/mut3`):
   ```
   gate G6 pass=0 read=symlinks=0 exempt-entries-not-shrunk=0
   c2-gate fixed=6/7 exit=1
   ```
   Grow-never-shrink is enforced for exempt names via `EXEMPT_BASE_SIZE` at `:72` = `{'claim-gates.md': 6742, 'claim-package-contract.md': 5169}`.

# Finding 2 — the F29 gate exempts the ledger by name, non-shrink (HOLDS)

Quoted verbatim from `corpus/instruments/r46-f29-gate.py` (v1; worktree == freeze export sha256 `a1091e246a51c1c1e710a18c6e8c9ba0cd4004069233a452ba446048de6fb8cd`, matching `f29-gate-sha256-v1` in `freeze.txt`):

- `:42-46` (H6 docstring): "…64 of them are pinned byte for byte — the considerthese ledger is exempt from the content pin (its name is pinned, its size may grow never shrink, so the ledger dispositions append does not couple with this claim)."
- `:80-81`: `LEDGER = "considerthese-proposals-ledger.md"` / `LEDGER_MIN_BYTES = 30696  # the ledger's byte size at the freeze tip; it may grow, never shrink`
- `h6()` `:311-330` excludes the ledger from the content hash (`if n != LEDGER`) and folds `ledger_ok = os.path.getsize(...) >= LEDGER_MIN_BYTES` into `base_ok`.

Measured: the ledger is 30696 bytes (exact match with the floor), sha256 `07994f484814de9f088de7cf1433c79917e92d38cff15d21ec9f57606f0c7205`, git blob `13ed71c8dca6f33d471d2708a0b8bf735c09a586` identical at `fe0f56b`, HEAD and worktree. `grep -c '^## Round-46 dispositions'` on it → `0` (the section does not exist yet; the append would be the first).

Commands and printed output (do-nothing control + ledger-specific mutants, positive tree built by the committed fixture `.ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode positive --dir $S/f29pos`, gate run `TMPDIR=$S/tmp python3 …/r46-f29-gate.py --root <tree> --work $S/tmp`):

1. Do-nothing control — unmodified positive tree: `f29-gate fixed=7/7 exit=0` with `gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0`.
2. Mutant 4 (append) — `\n## Round-46 dispositions (probe)\n\nProbe paragraph.\n` added (30696 → 30748 bytes): still `f29-gate fixed=7/7 exit=0`, H6 green. The append does not couple with the F29 claim.
3. Mutant 5 (shrink) — `truncate -s 30695` (one byte below the floor): `gate H6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1 symlinks=0`, `f29-gate fixed=6/7 exit=1`.

Cross-reference `controls/f29-r50-receipt.txt`: rows 16–17 of its mutant table already show H6 can fail (`nestedmd` → H6a flip, `entrymutant` pin-dropped → H6b flip); the two mutants above add the ledger-specific grow/shrink pair the receipt does not carry.

# Finding 3 — the coupling, and what the v1.3 amendment must touch

The two gates disagree by construction: H6 already tolerates the append (grow-allowed), G6 does not (byte-pinned). So the `## Round-46 dispositions` append couples with a CONTENT_EXEMPT amendment to the C2 counter — the lesson's own words: "the disposition is carried here and in the `LOG.md` entry and is appended in a later round together with a pin amendment" (`corpus/lessons/round-46.md:29`). The counters and frozen claims are read-only during the wave; the amendment lands only at L1 integration as a logged erratum.

It must touch `corpus/instruments/r46-c2-gate.py` in three places:

1. `:71` — add `"considerthese-proposals-ledger.md"` to the `CONTENT_EXEMPT` set literal (the named amendment).
2. `:72` — add `'considerthese-proposals-ledger.md': 30696` to `EXEMPT_BASE_SIZE`, so the grow-never-shrink guard covers the ledger and mirrors H6's `LEDGER_MIN_BYTES` contract. Without it the ledger would be unpinned and unguarded (a gutted ledger would read green — mutant 3's class).
3. `:66` — replace `PINS["base-knowledge-content"]` value `5e0796fd3617f7626880950a5b25d1818f58eff58a12dec99ce7a0f3836b8f47` with the 61-name digest `2c4ccfb65fdb5b727a3bc0c2465f6091b535663abd81126b81e76fdaae83a9a7`: exempting the ledger removes its `name sha` line from the hashed join (62 → 61 pinned names). I reproduced the committed digest byte-exactly with the same join over the freeze export (recomputed `5e0796fd…` == committed value), so the replacement value above is the expected one; recompute at integration if any other pinned byte moved.

# Draft — `## Round-46 dispositions` section text to append (end-of-file append, R6/R9)

```markdown
## Round-46 dispositions (appended 2026-10-29, R6/R9)

The seven proposals are those of `considerthese/2026-10-26.md` (`## Self-improvement suggestions`, :29-35). Statuses are documentary, measured at the round-46 attempt-2 freeze `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`, where this ledger's blob (`13ed71c8`) is byte-identical to the worktree. The round's considerthese record is `corpus/lessons/round-46.md:29`; it names proposals 2 and 3, and the other five are rejected for this round with the reasons below.

**1. Make "distance to next score" explicit** (`considerthese/2026-10-26.md:29`) — rejected this round, unchanged. The round-46 lesson records no landing for it (`corpus/lessons/round-46.md:29` names proposals 2 and 3 only) and the frozen attempt-2 claims (counter mutation coverage; the F29 admission) name no score-model work. The landed disposition stands: the r31 measurement (`corpus/instruments/score-gap.py`) and the r39 criteria (SCORECARD §Saturation); the last filed measure is this ledger's round-42 section, `gap: 24 of 61 rechecks still gated on a lost base` at round-43 base `ab98fac9`.

**2. Run one end-to-end domain task round** (`considerthese/2026-10-26.md:30`) — partially landed; the round-46 move is the C1 re-ground. The claim checker landed in round 43 (`corpus/lessons/round-43.md:139-147`: the gate prints `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0` on the committed exemplar and `selftest cases=10 failures=0`; landed pointer `corpus/instruments/claim-package-check.py` plus `corpus/knowledge/claim-package-gate.md`). Round 46 re-grounded the two lost-tree entries the package rests on — `corpus/knowledge/claim-package-contract.md` and `corpus/knowledge/claim-gates.md`, the two CONTENT_EXEMPT names at `corpus/instruments/r46-c2-gate.py:71` ("the claim-checker landed in round 43 and round 46 re-grounded two lost-tree entries on it", `corpus/lessons/round-46.md:29`). The remainder stays open: SHONEN box 2 is still unexercised (`corpus/lessons/round-46.md:29`).

**3. Add a quiescence gate before `complete`** (`considerthese/2026-10-26.md:31`) — adopted (mined) this round: implemented as `corpus/instruments/r46-landing-gate.py` (QUALITY R51; registry rows in `SKILL.md` and `corpus/instruments/README.md`), per `corpus/lessons/round-46.md:29`; the routed-defect disposition reshaped it into the `--pre-report`/`--post-report` pair (`corpus/lessons/round-46.md`, `## Routed defects` item 1, after M46-2 withdrew the author-time check).

**4. Cap or externalise wave evidence** (`considerthese/2026-10-26.md:32`) — rejected this round, unchanged, operator-owned. The round-46 lesson records no landing (`corpus/lessons/round-46.md:29`) and the claims name no release/LFS/prune work; the last filed measure is this ledger's round-42 section (8,442 tracked files, 8,115 under `.ufo/`, 96.1 %, at round-43 base `ab98fac9`).

**5. Land the owed F18 `PROVINCE.md` amendment** (`considerthese/2026-10-26.md:33`) — rejected this round as already resolved: landed r36 and marked resolved-landed by the round-39 section (`PROVINCE.md:77`, the `[r36 Frontier amendment …] F18` line); the round-46 lesson records no further change.

**6. Re-tune my own cadence and depth** (`considerthese/2026-10-26.md:34`) — rejected this round, unchanged, operator-owned. The round-46 lesson records no landing (`corpus/lessons/round-46.md:29`); `considerthese/` still holds one file per day with none after `2026-10-26.md`, and no second daily run, per-round digest section or weekly read-only cloud pass is claimed.

**7. Keep a proposal-status ledger** (`considerthese/2026-10-26.md:35`) — the round-46 disposition is this section, deferred to land with its pin amendment: the round does not append the ledger section in-round because "C2's G6 byte-pins the 62 base knowledge entries it does not exempt, and the ledger is one of them, so editing it would turn C2 red; the disposition is carried here and in the `LOG.md` entry and is appended in a later round together with a pin amendment" (`corpus/lessons/round-46.md:29`). This section is that append; the amendment it couples with adds `"considerthese-proposals-ledger.md"` to `CONTENT_EXEMPT` at `corpus/instruments/r46-c2-gate.py:71`, with the non-shrink base size (30696 bytes, this file's size at the freeze tip) at `:72` and the recomputed `base-knowledge-content` pin at `:66`, logged as a counter erratum at integration.

Scope: statuses are documentary; `adopted`/`mined` means a cited lane record names the landing (`corpus/lessons/round-46.md:29`, `corpus/lessons/round-43.md:139-147`) and no completeness re-measurement is claimed. This section is an end-of-file append (R6/R9): every section above, including the round-42 scope note, is unedited. The append keeps G6 of `corpus/instruments/r46-c2-gate.py` green only together with the amendment named in proposal 7's paragraph; H6 of `corpus/instruments/r46-f29-gate.py` already tolerates it (name pinned, non-shrink at `LEDGER_MIN_BYTES = 30696`, `:80-81`). This section is documentation-only, asserts no score move, and gives no instruction to probe, scan, log in to, or submit against any target.
```

# Limitations

- All gate runs executed the freeze-export copies of the counters (`$S/freeze/corpus/instruments/…`), byte-identical to the worktree files (sha256 quoted above) — the lane worktree itself was never a `--root` and was never modified.
- The predicted `:66` replacement digest `2c4ccfb6…` is exact for the freeze-tip bytes of the other 61 pinned names; it must be recomputed at integration if any of those bytes moved (the round's own gates pin them, so it should hold).
- The F29 positive tree is the L1's committed synthetic fixture, not the integrated round tree (the `github-repository-security-advisories.md` entry lands at integration); H6's ledger logic is identical either way, and the fixture embeds the real 66-entry knowledge dir including the 30696-byte ledger.
- Mutation coverage here is 5 targeted mutants + 2 do-nothing baselines aimed at the ledger coupling only — not the full battery; the full `uncaught=0` battery is the C1 claim's business (`r46-mutbat.py`, not run by this seat).
- `claims.json`, the counters, the S074 capture/manifest and every lane file were only read; read-only git (`ls-tree`, `log --oneline`, `status --porcelain`, `rev-parse`, `archive`) was used. No pacman/uv/npm install was performed, so there is nothing to record under the tooling authorization.
- The drafted heading carries the file's `(appended 2026-10-29, R6/R9)` suffix per the round-40/41/42 convention; the lesson names the section by prefix (`## Round-46 dispositions`), which the suffixed heading still satisfies for the `^## Round-46 dispositions` greps earlier rounds used.
