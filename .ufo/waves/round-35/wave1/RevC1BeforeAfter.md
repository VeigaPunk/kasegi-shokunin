# RevC1BeforeAfter — round-35 wave 1 (leaf, independent C1 before→after verification)

Role: independent re-derivation of every C1 (depth:verifiability) counter from the frozen
`.ufo/waves/round-35/claims.json`, at the lane base and at the tip, compared against the frozen
before receipt (`.ufo/waves/round-35/c1-controls/before.txt`) and the claim's after-values.
I did not author any of the verified changes; this receipt is my only lane write.

- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- Lane base: `3266c9937b03062d9bbc2f436e20820115ed179c`
- Claims-freeze commit: `617496b9c6e92bc671e7e78b83df69a04470d0e9`
- Lane HEAD at seat start and at every measurement below: `da2d3c687f82a9814ee71c91c930cb733050d37c`
  (round-35 wave-1 spec + dispatch). The wave-1 outputs are in the **worktree, uncommitted**;
  `git status --porcelain` grew 12 → 13 → 17 entries while I measured — the wave was landing live.
- Measurement window: 2026-10-26T06:33Z–06:41Z (UTC stamp on every pass)
- Scratch: `/fast/scratch/hyaku/kasegi-r35/RevC1BeforeAfter/` (deleted before yield; this receipt
  written first). The suite's own selftest scratch was pointed into it via `KASEGI_SCRATCH`.
- Tools installed/upgraded: **none** (nothing needed; no pacman/uv/npx/cargo transaction ran).
- Frozen-claims integrity: `sha256sum .ufo/waves/round-35/claims.json` →
  `fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982` — equal to the freeze-blob
  digest recorded in `.ufo/waves/round-35/wave1/ExecBeforeReceipts.md` §2; the frozen claims are
  unmodified on my read.
- Coordination: one message to `ExecSelftestFixtures` (fixture-path expectation) after I observed
  `corpus/instruments/r35-fixtures/` holding only `README.md`; all seven fixture dirs landed at
  ~06:37Z during my verification (D1–D7 plus `clean`, `two-defect`, `fixtures.json`, `README.md`).

## Report

### 1. Method — three tree states, one command per counter

| state | tree | how obtained |
|---|---|---|
| before | base `3266c99` | `git archive 3266c99… \| tar -x -C $S/base` (6930 files, no `.git`) — every before-command run with cwd = that export |
| after (worktree) | lane worktree at HEAD `da2d3c6` + uncommitted wave-1 outputs | commands run from the lane root |
| after (post-commit) | simulated landed tree | worktree copied to `$S/postcommit` (`tar`, excluding `./.git`/`./.jj`), `git init` + `git add -A` + commit **inside scratch only**, then `r35-defect-closure.sh --root $S/postcommit` |

Every counter below was re-derived with its own command; nothing is accepted from another seat's
receipt without being re-run here. Read-only git only (`rev-parse`, `status`, `ls-files`,
`ls-tree`, `diff`, `show`, `archive`, `log`); the only `git init/add/commit` in this seat ran
inside my scratch simulation tree, never against the lane repository.

### 2. Before side — base export vs `c1-controls/before.txt`: 12/12 MATCH

Driver: `before-battery.sh` (scratch, reproduced in §10). Exact outputs (cwd = base export):

```
$ ls corpus/instruments/r35-defect-closure.sh
ls: cannot access 'corpus/instruments/r35-defect-closure.sh': No such file or directory
exit=2
$ grep -c 'filled by the L1' SCORECARD.md      → 1   exit=0   (line 1240)
$ grep -c 'the L1 fills this line' SCORECARD.md → 1  exit=0   (line 1129, second spelling)
$ grep -c '<LANE_HASH>' SCORECARD.md           → 0   exit=1
$ grep -c 'c1c6a5f' SCORECARD.md               → 0   exit=1
$ grep -c '201\.7' SCORECARD.md                → 2   exit=0   (lines 1003, 1145)
$ grep -c '201\.2' SCORECARD.md                → 0   exit=1
$ grep -cE '^\| depth:density \| 9 \| mean \*\*201\.7\*\*, 25 blocks, 710 path-citation instances' SCORECARD.md → 1 exit=0
$ grep -cE 'r-defect-closure\.sh|kill-rule-check\.py' SKILL.md → 0 exit=1
$ ls corpus/instruments/r-defect-closure.sh corpus/instruments/kill-rule-check.py → both exist, exit=0 (present-but-unregistered, exactly as D3 states)
$ ls .ufo/waves/round-34/wave1-results.json    → No such file or directory, exit=2
$ git ls-tree -r --name-only 3266c99… -- .ufo/waves/round-34/wave1-results.json | wc -l → 0
$ find .ufo/waves/round-34 -maxdepth 1 -name '*provenance*' -type f  → (none)
$ find . -name 'claims-erratum-d5.md' -type f                        → (none)
$ grep -c 'did not file a receipt (dead seat' .ufo/waves/round-34/wave1/L1Integration.md → 1 exit=0 (line 30)
$ grep -c 'Correction (round 35)' .ufo/waves/round-34/wave1/L1Integration.md → 0 exit=1
$ grep -c 'supersedes R22' corpus/QUALITY.md   → 0  exit=1   (hyphen spelling also 0)
$ grep -c 'supersedes R23' corpus/QUALITY.md   → 0  exit=1   (hyphen spelling also 0)
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md → 51 exit=0
```

| stored (`before.txt`) | my base re-derivation | verdict |
|---|---|---|
| suite absent, `ls_exit=2` | same message, exit 2 | MATCH |
| D1 `filled by the L1` = 1 | 1 (`:1240`) | MATCH |
| D1 c1c6a5f citations = 0 | 0 | MATCH |
| D2 stale `201.7` = 2 | 2 (`:1003`, `:1145`) | MATCH |
| D2 corrected `201.2` = 0 | 0 | MATCH |
| D3 registry rows = 0 | 0 (both greps) | MATCH |
| D4 results tracked = 0 | 0 (absent on disk; `ls-tree` 0) | MATCH |
| D4 provenance note = 0 | 0 | MATCH |
| D5 erratum present = 0 | 0 | MATCH |
| D6 dead-seat sentence = 1 | 1 (`:30`) | MATCH |
| D7 supersedes rows = `0 0` | `0 0` (both spellings) | MATCH |
| (shared) S-rows = 51 | 51 | MATCH |

Self-honesty note: my first battery wrapper piped `run … | wc -l` incorrectly and printed two
spurious `3`s for the D4-provenance and D5 find commands; re-run clean (above) both give 0,
matching `before.txt`. No stored value was accepted from the buggy runs.

### 3. After side — the five frozen `counting_commands`, three passes

| # | frozen command | @06:35Z | @06:38Z | final @06:38:41Z | frozen after-value |
|---|---|---|---|---|---|
| 1 | `bash corpus/instruments/r35-defect-closure.sh` | `closed=3/7 exit=1` | `closed=4/7 exit=1` | `closed=4/7 exit=1` | `closed=7/7 exit=0` |
| 2 | `… --selftest` | `cases=7 failures=7` (+`fixture-missing` ×7) | `cases=7 failures=3 control-failures=0` | `cases=7 failures=3 control-failures=0` | `cases=7 failures=0` |
| 3 | `grep -c 'filled by the L1' SCORECARD.md` | 0 (exit 1) | 0 | **0** ✓ | 0 |
| 4 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 51 | — | **52** ✓ (S052 landed mid-verification) | 52 |
| 5 | `git ls-files .ufo/waves/round-34/wave1-results.json \| wc -l` | 0 | 0 | 0 (untracked until the L1 commits) | 1 |

Final pass per-check lines (suite digest at this pass `cba8c95b7f026ae7aee50d1bd1914ddbdc694e81c6155b2e2e3812678f50ef63`, 760 lines):

```
D1 check=placeholders=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=0,provenance=1 open=1
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=4/7 exit=1
```

Fourth pass at 06:40:29Z (suite digest `d7ad84384eb4b3fa2f5737e0597cbc9cdf3ded1eac867f6131886b790d38a304`,
773 lines): plain again `closed=4/7 exit=1` — D1's payload gained a third clause,
`D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0` (the suite now also
encodes the kill rule's `<LANE_HASH>` check; D1 mutants 3/3); selftest unchanged at
`cases=7 failures=3 control-failures=0` with the same judge lines.

### 4. Per-defect after-values, verified in the worktree bytes

**D1 — MET.** `grep -c 'filled by the L1' SCORECARD.md` → 0; second spelling
`grep -c 'the L1 fills this line'` → 0 (both placeholder paragraphs rewritten in place — the
numstat's 15 SCORECARD deletions are exactly those two paragraphs, the round-34 R1 convention);
`grep -c '<LANE_HASH>'` → 0; `grep -c 'c1c6a5f'` → 3:

```
1130:`c1c6a5f826d2425446347173de527c42991b78b0`** (filled in round 35, D1). This section is written at the
1241:**Round-34 final lane commit: `c1c6a5f826d2425446347173de527c42991b78b0`** (filled in round 35, D1).
1259:paragraph's) were replaced with the round-34 final lane hash `c1c6a5f826d2425446347173de527c42991b78b0`
```

plus the appended correction paragraph at `SCORECARD.md:1258-1261` ("Correction (round 35): the two
lane-commit placeholder sentences above … Neither placeholder spelling occurs in this file any
more"). `git diff --numstat -- SCORECARD.md SKILL.md` → `33 15 SCORECARD.md`, `13 0 SKILL.md`.

**D2 — MET, and both limbs reproduced from the named blobs.** Erratum appended at
`SCORECARD.md:1246` ("Erratum (round 35): the round-34 depth:density row measured 0 changed
SKILL/PROVINCE lines and mean 201.7; … the measured density mean is 201.2 …"); `201.2` ×2
(`:1246`, `:1250`); the stale row's opening bytes remain verbatim (suite `row-bytes=1`; the row now
sits at `:1146`, one line lower after the D1 insertions). `201.7` count went 2 → 4: the two new
mentions are inside the appended erratum block itself (`:1246`, `:1248`), the stale rows untouched.
Reproduction with the unchanged instrument (`corpus/instruments/density.py`, two files):

```
base 3266c99:  SKILL.md ba5ebe5d…  PROVINCE.md b4bb5fee…  → mean dens **201.2**, 711 cites / 25 blocks
git show 206e510: SKILL.md b11b6085…  PROVINCE.md b57de5d9… → mean dens **201.7**, 710 cites / 25 blocks
```

Both blob digests equal the ones the erratum's measurement-state paragraph (`:1248-1252`) names.

**D3 — MET.** `grep -nE 'r-defect-closure|kill-rule-check' SKILL.md` → rows at `:1097`
(`| r-defect-closure.sh | gate\|probe | bash corpus/instruments/r-defect-closure.sh [--root DIR] …`) and
`:1098` (`| kill-rule-check.py | gate\|probe | … python3 corpus/instruments/kill-rule-check.py …`),
inside the Gates & probes registry (home `SKILL.md:977`), with pinned digests and re-verify
commands at `:1100-1104`. Count 4/4 (two rows + their context lines). SKILL.md is append-only
(13 insertions, 0 deletions).

**D4 — MET ON COMMIT (index clause pending by design).** Both files exist on disk:
`wave1-results.json` 312874 B, sha256 `3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4`
— byte-identical to the digest the round-34 verifier recorded at 06:23:46Z
(`round-34-verifier-spotcheck.md` §1) — and `wave1-results.json.provenance.md` 5639 B beside it
(filed by `ExecD4ResultsTrack` ~06:32Z; it documents the 3 min 48 s after-`complete` offset, the
identity check, and that `git ls-files` printed 0 at its filing). `git ls-files … | wc -l` → 0 at
every pass (untracked, unstaged, not ignored). The clause flips exactly at the L1's commit —
proved by the simulation in §6.

**D5 — MET** (landed between my 06:35Z and 06:38Z passes). `.ufo/waves/round-35/claims-erratum-d5.md`
exists (sha256 `e2e7202d3c0c88619de96c65211e839248e43c9eb13241afeed2bf64480917a6`), carries
`discriminating invocation` ×5 and `per-id occurrences` ×5, is explicitly an appended correction
that touches neither frozen claims.json, and restates both broken round-34 C2 clauses with
executable invocations (quote-comparison route with `MISMATCH reason=quote-not-found`, and the
per-id occurrences reading with the three fixture runs) plus a round-35 disclosure (§5) that does
not claim any round-35 after-state.

**D6 — NOT MET at final measurement (06:39:25Z).** `grep -c 'did not file a receipt (dead seat'
.ufo/waves/round-34/wave1/L1Integration.md` → 1 (`:30`, the file's digest is still the freeze
digest `5472f60a…`, i.e. untouched); `grep -c 'Correction (round 35)'` → 0.

**D7 — NOT MET at final measurement (06:39:25Z).** `grep -c 'supersedes R22' corpus/QUALITY.md` → 0,
`grep -c 'supersedes R23'` → 0 (hyphen spelling also 0/0); QUALITY.md digest is still the freeze
digest `807cc714…`. Per the dispatch, `ScribeQualityDraft` drafts the rows
(`| R26 | … supersedes R22`, `| R27 | … supersedes R23`) and `ExecClosureSuite`'s task carries the
D6/D7 check specs — neither fix had landed in the worktree when I last read.

### 5. Base-tree failure direction — verified

```
$ KASEGI_SCRATCH=$S/suite-scratch bash corpus/instruments/r35-defect-closure.sh --root $S/base
D1 check=placeholders=1,correction-c1c6a5f=0 open=1
D2 check=erratum-row=0,erratum-mean=0,row-bytes=1 open=1
D3 check=registry-r-defect-closure=0,registry-kill-rule=0 open=1
D4 check=tracked=0,provenance=0 open=1
D5 check=erratum-file=absent,discriminating-invocation=0,per-id-occurrences=0 open=1
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=0/7 exit=1
base_run_exit=1
```

Matches the claim's base clause (`closed=0/7`, exit 1) exactly — all seven open on the base
export, run by the tip suite via `--root`.

### 6. Post-commit simulation — the D4 commit-timing discriminator

Worktree copied to scratch, `git init` + `git add -A` + commit inside the scratch copy only, then:

```
$ bash corpus/instruments/r35-defect-closure.sh --root $S/postcommit
D1 check=placeholders=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=1,provenance=1 open=0        ← flips exactly at commit (was tracked=0)
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=5/7 exit=1
```

So on the bytes as they stood at ~06:36Z, committing alone closes D4 and D5; the residual gap to
`closed=7/7` is exactly D6 + D7 landing plus the commit itself.

### 7. Do-nothing control discrimination — verified

The selftest's judge rejects the committed fake suite
(`.ufo/waves/round-35/c1-controls/fake-suite.sh`, which prints a claimed `cases=7 failures=0` /
`closed=7/7 exit=0` while checking nothing):

```
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=short-report rejected=1
selftest judge=fake-suite rejected=1 path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0
selftest judge=fake-plain rejected=1 output=closed=7/7 exit=0
```

Fixture and control limbs at suite digest `cba8c95b…`: all seven fixtures rejected on their own
clause (`fixture=rejected`, reasons match each defect's `fix_re`); `control=clean closed=7/7
verdict=pass`; `control=two-defect closed=5/7 failed=D1,D2 verdict=pass`; per-clause mutants
killed for D1 (2/2), D2 (3/3), D3 (2/2), D4 (2/2), D5 (2/2); D6/D7 mutants read
`verdict=unexpected` only because those fixes are still open in the live bytes they are built
from (isolate_ok requires every other clause closed). `selftest cases=7 failures=3
control-failures=0`, and the suite correctly refuses to bless its own failing report
(`selftest problem=self-report status=1`).

**`report_ok` anchoring defect (found by `ExecSelftestFixtures`, independently reproduced here).**
At `cba8c95b…` the fixture-detail judgement anchored `reason=$(fix_re $id)` immediately after
`reason=`, but the D4 and D5 fixture payloads open with another clause
(`reason=tracked=0,provenance=0`; `reason=erratum-file=present,discriminating-invocation=2,per-id-occurrences=0`),
so at `failures=0` the judge would have rejected its own clean report and exited 1 with
`selftest problem=self-report` — keeping the frozen `--selftest … exit=0` after-value unreachable
even with every defect closed. Reproduced on the D4/D5 detail lines: anchored form 0/1 matches,
`reason=.*$(fix_re …)` form 1/1 for exactly those two ids. **The fix is already in the landed
bytes**: `corpus/instruments/r35-defect-closure.sh:487` at digest `d7ad8438…` reads
`grep -Eq "^selftest detail=$id fixture reason=.*$(fix_re "$id")"`. I have not observed the
`failures=0` path end-to-end (D6/D7 were still open at my last read), so the post-commit,
post-D6/D7 selftest run remains the L1's to take at the pinned final digest.

### 8. Findings for the L1

1. **[in-flight gap] D6 and D7 fixes had not landed at my final measurement (06:39:25Z).**
   `L1Integration.md` still carries the stale dead-seat sentence (`:30`, digest = freeze digest
   `5472f60a…`) with no `Correction (round 35)` note; `QUALITY.md` has 0 `supersedes R22`/`R23`
   rows (digest = freeze digest `807cc714…`). Until they land and the L1 commits, the frozen
   counter reads `closed=4/7 exit=1` — if the round closed in this state, the kill clause
   `` `closed` != 7/7 `` would trigger. Everything else C1 needs is in the worktree (D1/D2/D3/D5
   verified met; D4 met on commit per §6), so the remaining distance is exactly those two fixes
   plus the integration commit.
2. **[order-critical, by design] Both suite counters are commit-sensitive.** D4's live clause
   reads `git ls-files` (the index), so `closed=7/7 exit=0` and `--selftest cases=7 failures=0`
   are reachable **only on a committed tree** — on the uncommitted worktree D4's live limb fails
   and the selftest counts it (`cases=7 failures=3` at 06:38Z with D6/D7 also open). The L1 must
   run both counters **after** the integration commit, not before; running them first would
   record a false failure (the M35-1 landing-order class in mirror image).
3. **[process] The suite iterated throughout my verification — four digests observed.**
   `c748dd70…` (643 lines, ~06:36Z) → `cba8c95b…` (760 lines, 06:38Z; `fix_re` D4 `tracked=0` →
   `provenance=0`, D5 `erratum-file=absent` → `per-id-occurrences=0`; case lines gained
   `others=6/6`) → `d7ad8438…` (773 lines, 06:40Z; `report_ok`'s fixture-detail grep un-anchored
   to `reason=.*$(fix_re …)` — the §7 defect fix — and D1 gained the `lane-hash-markers` clause).
   Each iteration changed what the frozen counters measure against. Pin the final digest as the
   figure of record (round-28 convention: the receipt index, not a retyped digest) and re-run
   both counters at that pinned digest post-commit; a digest move is not a verdict move, but an
   unpinned one leaves the judge no canonical bytes.
4. **[hardening, non-blocking] The suite's D1 clause still covers two of three placeholder
   spellings.** At `d7ad8438…` D1 greps `filled by the L1` (placeholders) and `<LANE_HASH>`
   (lane-hash-markers, newly encoded this round) — but not the second prose spelling
   (`the L1 fills this line`, `SCORECARD.md:1129` at freeze — ExecBeforeReceipts finding 3).
   That spelling is also gone at tip (0), so the bytes are clean, but a future recurrence of it
   would pass the suite. The frozen kill rule names only `filled by the L1` and `<LANE_HASH>`,
   so this is hardening, not a kill.
5. **[shared counter trajectory] COUNT-4 (S-rows) read 51 at 06:35Z and 52 at 06:38:41Z** — the
   S052 row landed mid-verification (C2's lane). The frozen after-value 52 is met at my final
   measurement.
6. **[self-honesty] My first before-battery wrapper produced two spurious `3`s** (pipeline bound
   to the wrapper, not the find); re-run clean gives 0/0 matching `before.txt` (§2). No stored
   value was accepted from the buggy runs.

### 9. Digests at measurement time

```
fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982  .ufo/waves/round-35/claims.json   (= freeze blob)
51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7  SCORECARD.md                     (modified: D1+D2)
daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc  SKILL.md                         (modified: D3, append-only 13/0)
807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8  corpus/QUALITY.md                (= freeze digest; D7 pending)
5472f60ab33a2241e7051c071e1469ca89b2c874e571d93420499cd0998a0fd5  .ufo/waves/round-34/wave1/L1Integration.md  (= freeze digest; D6 pending)
3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4  .ufo/waves/round-34/wave1-results.json      (= round-34 verifier's digest)
e1c4430133adeb58b8d3b3af9edcb49739eacd3f40536dca529105c609e86c98  .ufo/waves/round-34/wave1-results.json.provenance.md
e2e7202d3c0c88619de96c65211e839248e43c9eb13241afeed2bf64480917a6  .ufo/waves/round-35/claims-erratum-d5.md
cba8c95b7f026ae7aee50d1bd1914ddbdc694e81c6155b2e2e3812678f50ef63  corpus/instruments/r35-defect-closure.sh    (760 ln at 06:38Z; then 5fb0da5e… 06:39:25Z, d7ad8438… 773 ln at 06:40Z — suite under active iteration, see finding 3)
```

Base-export digests for the before side (measured on the `git archive` extraction):
`SCORECARD.md` `efa646c8…`, `SKILL.md` `ba5ebe5d…`, `corpus/QUALITY.md` `807cc714…`,
`L1Integration.md` `5472f60a…` — the latter two equal to ExecBeforeReceipts §1's freeze digests,
so my before side measured the same committed bytes that receipt replayed.

### 10. Reproduction

Driver scripts (deleted with scratch; contents reproduced here in full in the receipt's spirit —
each is a labeled `run`/`runsh` wrapper around the exact commands quoted in §2–§3):
`before-battery.sh` (§2), `after-battery.sh` (§3 pass 1 + §4), `final-battery.sh` (§3 final pass),
plus `git archive 3266c99… | tar -x` (§2 tree) and the §6 tar-copy + `git init/add/commit`
simulation. Toolchain: git 2.56.0, GNU bash 5.3.20, GNU grep (builtin pi-uu-grep 0.2.0 shim
present; counts spot-checked against `/usr/bin/grep` behavior on the shared S-rows command in
ExecBeforeReceipts §6 — I used the same builtin throughout for consistency), Python 3.14.8,
GNU tar 1.35.

Scratch `/fast/scratch/hyaku/kasegi-r35/RevC1BeforeAfter/` is deleted immediately before yield;
this receipt was written to the wave dir first. No lane file other than this receipt was written
by this seat; no git/jj mutation was run against the lane repository.
