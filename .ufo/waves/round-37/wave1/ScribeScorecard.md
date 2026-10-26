# ScribeScorecard — round-37 SCORECARD.md section draft

seat: `ScribeScorecard` (scribe, leaf — no subagent dispatch)
issue: draft the round-37 `SCORECARD.md` section: `## Round 37 result` block, axes table
(depth:verifiability held 4 with the r37 suite commands; coverage held 7 with counters;
depth:density unchanged, no move claimed), measured commits (before = claims-freeze `224df74d`;
after = the r37 final head) with the anchor-ancestor convention, counting-commands block,
capabilities-table check, a Planned line for round 38, and the `Final lane commit:` line.
lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` — read-only for this seat except this receipt.
writes: this receipt only. No lane byte, fleet byte, or source tree touched; no mutating git/jj
command (read-only `log/show/diff/status/rev-parse/ls-tree/ls-files/cat-file/merge-base` only);
no tool installed or upgraded.

## 1. Behavior

Read the round-34/35/36 sections (`SCORECARD.md:1121-1262`, `:1263-1404`, `:1406-1494`), the frozen
claims (`.ufo/waves/round-37/claims.json`, blob `570c1d2c…` at freeze commit `224df74d…` — matches
the working file), the frozen controls (`.ufo/waves/round-37/{c1-controls/before.txt,c2-controls/before.txt,census-before.txt}`),
the appended erratum (`.ufo/waves/round-37/claims-erratum-1.md`, commit `b362068…`), and the
round-36 verifier spot-check §5 (`corpus/lessons/round-36-verifier-spotcheck.md:142-164`, D1-D6).
Measured the before surface myself on the base/freeze bytes with read-only commands, then drafted
the block in the lane's established shape. Every after-cell is the frozen contract's expected
state, labelled as such, because `corpus/instruments/r37-closure.sh` does not exist at this read
(and this seat does not build it). The `Final lane commit:` hash cannot exist at draft time (a
commit cannot cite itself); the block therefore carries the substitution token `R37_FINAL_HEAD` and
the anchor-ancestor convention, with the binding rule stated in §3.

## 2. Drafted block (append at EOF; lands after `SCORECARD.md:1494`)

Every paragraph is self-contained; the block contains no angle-bracket placeholder, no
`filled by the L1` literal, no `<LANE_HASH>` marker, and no intermediate-ancestor label. Pipes
inside table cells are escaped in the block source as `\|`.

````markdown
## Round 37 result — frozen claims C1/C2 (2026-10-26)

Frozen before dispatch in `.ufo/waves/round-37/claims.json` (sha256 `570c1d2c…`, `frozen_at_utc`
`2026-10-26T16:30:00Z`, attempt 1; base `b56a41680cefd391868c1c370dc063c69d827e7d`, claims-freeze
commit `224df74db2a46d627ae1475a72ca48796bbd177c`), together with the frozen before controls
`.ufo/waves/round-37/c1-controls/before.txt` (`63670cf5…`), `c2-controls/before.txt` (`fd849486…`)
and `census-before.txt` (`ada01b8e…`, exit 0, `W04 S028` + `W04 S029` only). One appended erratum
(`claims-erratum-1.md`, commit `b362068…`) corrects the C2 S054 capture URL to the SSVC overview
tutorial page; no other frozen literal changes. Receipts land under `.ufo/waves/round-37/`
(`c1-controls/`, `c2-controls/`, `census-before.txt`, `assimilation/`, `final-gates/`, `wave1/`);
`wave1-spec.json` dispatches 64 items. The last round heading at this round's base is round 36, so
every before-cell is the frozen control measured at this round's base bytes. The round-37 subject is
closure of the six routed defects D1-D6 of the round-36 verifier spot-check (§5) in a fourteen-check
closure suite (C1), and frontier F20 / SSVC — Stakeholder-Specific Vulnerability Categorization (C2).

| Axis | Before (frozen control, base `b56a416…`) | After (held) | Evidence and reds |
|---|---|---|---|
| depth:verifiability | 4 — `corpus/instruments/r37-closure.sh` absent (`ls_exit=2`, `suite_missing=1`); D1-D6 open: no `.ufo/waves/round-37/final-gates/all-gates.txt`; the round-36 C1 bullet names an absent `corpus/instruments/r36-fixtures/` path (`git ls-tree … \| grep -c r36-fixtures` = 0); the round-36 lesson labels an intermediate ancestor as final; `SKILL.md`'s `r36-closure.sh` registry row type cell is the literal `gate\|probe` and its verdict map has no exit-2 row; `r36-closure.sh` maps a failed status read to 0 dirty lines (`porcelain:-0`). Placeholder greps 0 / 0; `worktree_clean=0`; `scratch_leftovers=0` (all four at the freeze). | held 4 — `bash corpus/instruments/r37-closure.sh --export-ref "$R37_FINAL_HEAD"` → `closed=14/14 exit=0`; `--selftest` → `cases=14 failures=0`; `.ufo/waves/round-37/final-gates/all-gates.txt` carries a `suite-sha256=` header equal to the suite bytes' digest, fourteen `E1`–`E14` `payload=` lines, `closed=14/14 exit=0`, fourteen `selftest case=` lines and `cases=14 failures=0`; E10-E14 close D1, D2, D4, D5 and D6; D3 (closure-order recurrence) is carried as the round-37 lesson's mistake rows, not as an E-check; E9 is fail-closed by shape (`grep -cF 'porcelain:-0' corpus/instruments/r37-closure.sh` = 0, no status-read `2>/dev/null` swallow); placeholder greps 0 / 0. | `corpus/instruments/r37-closure.sh`; `.ufo/waves/round-37/final-gates/all-gates.txt`; `.ufo/waves/round-37/wave1/{ExecC1SuiteBuild,ExecC1ExportMode,ExecC1BaseFail,ExecC1JudgedHeadFail,ExecQuiescenceProbe}.md`. **Reds:** r36 base `cc692008b0cfd58d18275aa6c4aed79620120799` → `closed<14/14 exit=1` (E10-E14 open there); r36 judged head `a23dc4788aa7c98831eed6db953434034ce5ae8d` → `closed<14/14 exit=1` (E10-E14 open there). |
| coverage | 7 — frontier admitted **19**; registry rows **53**; `S054` rows **0**; entries citing `source: S054` **0**; `corpus/knowledge/*.md` **48**; harness `entries=22 pass=22 exit=0`; capture `records=43 bound=43 unbound=0`; `recheck-audit --quiet` `expected=48 pass=48`, exit 0; census exit 0 (`W04 S028`, `W04 S029`); junk twin absent. | held 7 — frontier admitted **20** (`F20` row); registry rows **54** (the `S054` row: tier A, `mined`, opened 2026-10-26); entries citing `source: S054` **1**; knowledge entries **49**; harness `entries=23 pass=23 exit=0` including `PASS F20 … ids=S054`; `source-recheck S054` exit 0 against the round-37 manifest; capture `corpus/source-snapshots/round-37/S054.txt` + `manifest.json` (URL per `claims-erratum-1`, strict-UTC `fetched_utc`) committed and bound (`records=44 bound=44 unbound=0`); `recheck-audit --quiet` `expected=49 unexpected=0`, exit 0; census exit 0 (`W04 S028`, `W04 S029`); junk twin `.ufo/waves/round-37/c2-controls/junk-f20.md` rejected. | `corpus/README.md` F20 row; `corpus/SOURCES.md` S054 row; `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`; `corpus/source-snapshots/round-37/{S054.txt,manifest.json}`; `.ufo/waves/round-37/wave1/{ExecC2Capture,ExecC2Harness,ExecC2QuoteOnce,ExecC2JunkControl,ExecManifestChecks,ExecCensusReplay,ExecExpectedListSync}.md`. |
| depth:density | 9 — mean **225.3**, 27 blocks, 751 path-citation instances (`SKILL.md` `2ddb1bc7…`, 1111 lines; `PROVINCE.md` `b0e91a61…`, 78 lines), committed `density.py` (`ee803726…`). | 9, unchanged — **no move claimed.** The round's only `SKILL.md` change is the D5 registry-row repair (single-choice type cell and the exit-2 → `could-not-evaluate` verdict row); no reflow of an existing block is claimed. | `corpus/instruments/density.py` (same digest and definition); the post-round census is recorded at closure; no density-bearing byte is read by `r37-closure.sh`. |

**Verdict state.** Every after-cell above is the frozen contract's expected state at this draft:
at this seat's read `r37-closure.sh` is absent, the harness prints `entries=22 pass=22 exit=0`, and
the three coverage counters print 19 / 53 / 48. The commands that decide the verdicts, one per line,
so closure appends verdict lines instead of rewriting the table:

    bash corpus/instruments/r37-closure.sh --export-ref "$R37_FINAL_HEAD"      -> closed=14/14 exit=0
    bash corpus/instruments/r37-closure.sh --export-ref cc692008b0cfd58d18275aa6c4aed79620120799 -> closed<14/14 exit=1
    bash corpus/instruments/r37-closure.sh --export-ref a23dc4788aa7c98831eed6db953434034ce5ae8d -> closed<14/14 exit=1
    bash corpus/instruments/r37-closure.sh --selftest                          -> cases=14 failures=0 exit=0
    test "$(head -1 .ufo/waves/round-37/final-gates/all-gates.txt | sed 's/^suite-sha256=//')" = "$(sha256sum corpus/instruments/r37-closure.sh | cut -d' ' -f1)" -> exit 0
    grep -c '^E[0-9]* payload=' .ufo/waves/round-37/final-gates/all-gates.txt  -> 14
    grep -c '^selftest case=' .ufo/waves/round-37/final-gates/all-gates.txt    -> 14
    grep -c 'closed=14/14 exit=0' .ufo/waves/round-37/final-gates/all-gates.txt -> 1
    grep -c 'cases=14 failures=0' .ufo/waves/round-37/final-gates/all-gates.txt -> 1
    grep -cF 'porcelain:-0' corpus/instruments/r37-closure.sh                  -> 0
    grep -cE '^\| F[0-9]+ \|' corpus/README.md                                 -> 20
    grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md       -> 54
    grep -rlE '^source: S054 ' corpus/knowledge | wc -l                        -> 1
    python3 corpus/instruments/frontier-recheck-count.py                       -> entries=23 pass=23 exit=0
    python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054 -> exit 0
    python3 corpus/instruments/capture-binding-check.py                        -> records=44 bound=44 unbound=0 exit 0
    python3 corpus/instruments/recheck-audit.py --quiet                        -> strict pass=49/49 expected=49 missing=0 unexpected=0 exit=0
    ls corpus/knowledge/*.md | wc -l                                           -> 49

**Measured commits.** Before = claims-freeze commit `224df74db2a46d627ae1475a72ca48796bbd177c`,
whose `.ufo/waves/round-37/claims.json` blob digests `570c1d2c…`, on base
`b56a41680cefd391868c1c370dc063c69d827e7d`; after = `R37_FINAL_HEAD`, the round-37 final lane head;
**anchor ancestor: `c20300df516eb5575d8db2aaad1f0cf4913e7981`** (round-36 lane head). The
anchor-ancestor convention is stated once here and once in the closing paragraph: the round-36 head
is the ancestor this round measures from, and no intermediate commit is labelled final in this
section.

**Measurement state (values re-read at this draft).** `SCORECARD.md` 1494 lines (`1e2788c6…`);
`SKILL.md` `2ddb1bc7…` (1111 lines, mean 225.3 / 27 blocks / 751 cites); `PROVINCE.md` `b0e91a61…`
(78 lines); `corpus/README.md` `55c41374…` (398 lines, 19 F-rows); `corpus/SOURCES.md` `2ff7818a…`
(117 lines, 53 rows); `corpus/QUALITY.md` `cfd0187a…` (264 lines, R22/R23 supersession rows
present); `corpus/instruments/r36-closure.sh` `4db1ae70…` (the D5/D6 target); `density.py`
`ee803726…`. The frozen control's audit reads `expected=48`; the after value is `expected=49`. The
wave-1 integration commit, the `r37-closure.sh` digest and line count, and the final lane-commit
value are recorded at closure: this draft asserts none of them.

**Capabilities: no row enters this round.** `r37-closure.sh` is a closure counter — it demonstrates
fourteen named checks closed on an exported head — not a new thing the lane can do to the domain.
The master `## Capabilities` table and the round-33 row are unchanged, and the capability window is
not restarted (last entry round 33).

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. No capability entry enters this
round, so the capability window does not restart. The lowest non-retired axis remains
**depth:verifiability (4)**; with C1 held 4 by design, that obligation stays active after this round.

**Planned round 38.** Re-freeze C1/C2 on the bytes after this round's final lane head; the lowest
non-retired axis stays depth:verifiability (4, held), so the depth obligation carries into the next
freeze; the open `considerthese/2026-10-26.md` proposal-1 saturation-thresholds plank and the
proposal-7 spend (`QUALITY` R31 + `corpus/considerthese-ledger.md`) carry forward; the next Frontier
admission with its capture, entry and harness trio is the round's coverage candidate.

**Anchor ancestor: `c20300df516eb5575d8db2aaad1f0cf4913e7981`** (round-36 lane head).
**Final lane commit: `R37_FINAL_HEAD`**.
````

## 3. Integration substitution (for the L1, not part of the block)

1. Replace `R37_FINAL_HEAD` (two occurrences: the `--export-ref` command in the verdict paragraph
   and the closing `Final lane commit:` line) with the 40-hex round-37 final lane head. The value
   must satisfy both E1 limbs on the exported ref: `git cat-file -e "<h>^{commit}"` and
   `git merge-base --is-ancestor "<h>" "<export-ref>"`. A real ancestor of the export ref is
   sufficient and is the only thing the suite can bind; a token, a 64-hex digest, or a side-branch
   commit is red.
2. Keep the `anchor ancestor:` label on `c20300df516eb5575d8db2aaad1f0cf4913e7981` and do **not**
   add a `Final lane commit:` label to any intermediate commit in this section (E12: the stale
   intermediate-ancestor literal must not appear inside the round-37 section). The round-36
   section's stale line at `SCORECARD.md:1492` is outside this section's scope; relabel it only if
   you also keep E12's round-37-section grep clean.
3. Heading is `## Round 37 result — frozen claims C1/C2 (2026-10-26)`; append after
   `SCORECARD.md:1494` so the round-36 section stays closed above it.
4. Do not copy the draft's "expected state" sentences into a measured-verdict claim without running
   the commands; the closure appends the measured lines (prior rounds' form).

## 4. Before-column measurements (mine, read-only, base `b56a416` / freeze `224df74d`)

| surface | command | value |
|---|---|---|
| suite presence | `ls corpus/instruments/r37-closure.sh` | exit 2 (`suite_missing=1`) |
| D1 | `ls .ufo/waves/round-37/final-gates/all-gates.txt` | exit 2 (no receipt) |
| D2 | `git ls-tree -r --name-only b56a416 \| grep -c r36-fixtures` | 0 |
| D5 type cell | `grep -cF 'gate\|probe' SKILL.md` | 6 (the `r36-closure.sh` row is `SKILL.md:1111`; the r35 row is `:1110`) |
| D5 verdict map | `grep -nE '^\| \`?r36-closure\.sh\`?[[:space:]]*\|' SKILL.md` | one row, no exit-2 → `could-not-evaluate` clause |
| D6 | `grep -n 'porcelain:-0' corpus/instruments/r36-closure.sh` | `:466` (`porcelain=${porcelain:-0}`) |
| placeholders | `grep -c 'filled by the L1' SCORECARD.md` · `grep -c '<LANE_HASH>' SCORECARD.md` | 0 · 0 |
| frontier | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 19 (last F19) |
| registry | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 53 |
| S054 rows / citing entries | same grep for `S054` · `grep -rlE '^source: S054 ' corpus/knowledge \| wc -l` | 0 · 0 |
| knowledge | `ls corpus/knowledge/*.md \| wc -l` | 48 |
| harness | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=22 pass=22 exit=0` |
| capture binding | `python3 corpus/instruments/capture-binding-check.py` | `records=43 bound=43 unbound=0`, `with_fetched_utc=5`, exit 0 |
| audit | `python3 corpus/instruments/recheck-audit.py --quiet` | `strict pass=48/48 expected=48 unexpected=0 exit=0` |
| round-37 capture dir / junk twin | `ls corpus/source-snapshots/round-37` · `ls .ufo/waves/round-37/c2-controls/` | absent · `before.txt` only |
| density | `python3 corpus/instruments/density.py SKILL.md` | mean 225.3, 27 blocks, 751 cites, exit 0 |

Digests measured: `claims.json` `570c1d2c…` (identical at `224df74d`), `c1-controls/before.txt`
`63670cf5…`, `c2-controls/before.txt` `fd849486…`, `census-before.txt` `ada01b8e…`, `SCORECARD.md`
`1e2788c6…` (1494 lines), `SKILL.md` `2ddb1bc7…` (1111 lines), `PROVINCE.md` `b0e91a61…` (78
lines), `corpus/README.md` `55c41374…`, `corpus/SOURCES.md` `2ff7818a…`, `corpus/QUALITY.md`
`cfd0187a…`, `r36-closure.sh` `4db1ae70…`, `density.py` `ee803726…`. Commit existence/ancestry
checked: `224df74d`, `b56a416`, `cc692008`, `a23dc478`, `c20300df`, `b362068` all present; `c20300df`
and `b56a416` are ancestors of current HEAD `b362068`. The frozen control's `worktree_clean=0` and
`scratch_leftovers=0` were measured at freeze; at this draft the live wave's own untracked receipts
(6 paths) and live seat scratch dirs exist, so E9 is a closure-time check, not a draft claim.

## 5. Findings (reported, not filed as failures)

- **F1 — final head cannot be self-cited.** The `Final lane commit:` value is the one datum that
  cannot exist when the block is written; the draft uses `R37_FINAL_HEAD` with the E1 binding rule
  in §3. The r36 failure was not the placeholder but the label: the filled value named an
  intermediate ancestor (spot-check D4). Labelling `c20300df` as `anchor ancestor` and naming only
  the measured r37 head keeps that class closed. If the closing commit itself is declared the final
  head, record it in the next round (the round-33/34 pattern) rather than mislabelling an earlier
  commit.
- **F2 — after-cells are contract, not measurement.** `r37-closure.sh` and
  `final-gates/all-gates.txt` are absent at this read, so the 14/14, 23/23 and 49/49 values are
  frozen expectations. The commands block is the deciding surface; closure appends measured lines.
- **F3 — C2 URL erratum supersedes the frozen literal.** `claims.json` still spells the SSVC docs
  home page; `claims-erratum-1.md` (commit `b362068`, filed before scoring) corrects the row,
  manifest and capture URL to the overview tutorial page
  (`https://certcc.github.io/SSVC/tutorials/ssvc_overview/`). The block says "per `claims-erratum-1`"
  rather than reprinting a URL the capture must match exactly.
- **F4 — density baseline is 225.3, not the round-36 landed 220.9.** The round-36 landed number was
  measured before its own closure appended the round-36 registry block; the r37 base bytes measure
  mean 225.3 / 27 blocks / 751 cites at `SKILL.md` 1111 lines (`2ddb1bc7…`). The score stays 9 and
  no move is claimed; the D5 repair edits one registry row in place, so a closure re-census on the
  same committed `density.py` is the no-harm guard.
- **F5 — the round-36 stale label remains at `SCORECARD.md:1492`.** E12 scopes the stale literal to
  the round-37 section; the draft therefore relabels only through the anchor-ancestor convention and
  leaves the round-36 bytes alone. The round-37 lesson (not this seat's file) must carry the same
  correction for the lesson limb.
- **F6 — capture stamp and expected-list coupling.** `capture-binding-check.py` reads
  `with_fetched_utc=5` at base; the S054 record must add a strict-UTC `fetched_utc` (6) and bind, and
  `knowledge-expected.txt` must move 48 → 49 or `recheck-audit` reports `unexpected=1`.
- **F7 — D5 is row-scoped, not file-global.** `grep -cF 'gate\|probe' SKILL.md` is 6 at base; the
  claim targets the `r36-closure.sh` row only. A global scrub would rewrite unrelated registry rows
  and is not required.
- **F8 — E10 digest equality is exact.** The all-gates header must equal `sha256sum
  corpus/instruments/r37-closure.sh` on the exported bytes, not a 64-hex digest pasted from the lane
  working tree; the commands block tests the equality directly.

## 6. Out-of-scope / not done

- No `SCORECARD.md`, lesson, LOG, SKILL or corpus edit: this seat's only lane write is this receipt;
  the block above is text for the L1's integration commit.
- No suite run, no export of any ref, no harness run against round-37 bytes beyond the read-only
  counters in §4 (re-running absent counters would not decorate a draft).
- No score change proposed; C1/C2 stay `held` until the deciding commands run on the final head.
- No tool installs or upgrades; no `pacman`.

## 7. Scratch

`/fast/scratch/hyaku/kasegi-r37/ScribeScorecard/` created for the extracted spec, then removed
before yield; every other read was `git show`/`git ls-tree`/`git status` or a read-only counter run
against the lane with `PYTHONDONTWRITEBYTECODE=1`.

Report: .ufo/waves/round-37/wave1/ScribeScorecard.md
