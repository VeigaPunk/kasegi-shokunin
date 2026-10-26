# RevShonenFinal — wave-2 falsify receipt: SHONEN.md round-39 box lines

Seat: RevShonenFinal (reviewer, leaf, attack seat; I did not author any deliverable under review).
Item: review the final SHONEN.md round-39 lines — exactly four box lines, all `[~]`, resolvable
evidence pointers to committed artifacts, no `[x]`, lines match the observed tree state (no
overclaim), and the report's SHONEN section mirrors them.
Judged axis: depth:verifiability. Review window: 2026-10-26T20:05Z–20:24Z.
Tree reviewed: lane HEAD `5006097a84305267c9a3e8c1e1d560e60fe41d37` (= verification ref Y; J =
`46c66c268502abd1b2c342fc71bf88ccf721845b` per the receipt's `export-ref=`; `git diff --name-only
J HEAD` = `.ufo/waves/round-39/final-gates/all-gates.txt` only — the judged-head rule holds).
SHONEN.md blob at HEAD: `7788d1d65bb0785d5609098c5d65ecd3d5a3ed85` (202 lines), unchanged under me
during the window. Frozen inputs read first: `claims.json` + `claims-erratum-1.md` (E1/E2/E4/E5).

## Verdict per property

| Property | Verdict | Note |
|---|---|---|
| Exactly four box lines | PASS | `- [~]` box lines at SHONEN.md:193, :195, :197, :199; the round-39 section (after the `Correction (round 39)` block at :190) ends at the :202 trailer; no other round-39 box lines exist (all earlier `- [~]` lines carry round 34–38 evidence labels). |
| All `[~]`, no `[x]` | PASS | All four are `[~]`; `grep -n '\[x\]' SHONEN.md` → no match file-wide (rc=1). |
| Pointers resolve to committed artifacts | PARTIAL | Every pointer resolves except box 1's primary referent: the `r39-closure.sh` registry row in SKILL.md **does not exist** (F1). Box 3's `all-gates.txt` resolves but is a curated composite with an impossible timestamp (F2). |
| Lines match observed tree state | **FAIL (box 1)** | Box 1 clause 1 is false on the tree (F1). Boxes 2, 3, 4 verified clause-by-clause (§ What holds). |
| Report's SHONEN section mirrors them | PENDING + draft defect | The round-39 report is **not filed** (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/kasegi.md` absent; 11 sibling lanes filed there, kasegi not). The L1's staged draft `kasegi-r39-l1/report-final.md` §SHONEN mirrors all four boxes substantively in one compressed paragraph (the r38 report used four per-box bullets), but it **repeats box 1's false registry-row claim** ("box 1 registry row r39-closure.sh") — F1 propagates into the report draft (F5). |

## Findings

### F1 — HIGH: box 1 claims a SKILL.md registry row that does not exist (overclaim; M39-2 class recurring in round 39's own box)

Box 1 (SHONEN.md:193-194) asserts: "Gates & probes registry gains the `r39-closure.sh` row
(single-choice gate, verdict map incl. exit 2) appended at EOF; every base line byte-identical".

Observed tree:

- `git -C <lane> rev-parse 480b1a50…:SKILL.md HEAD:SKILL.md` → both `ed22d61d4035f8756cf1a14701478385f079c3c1` — SKILL.md is **byte-identical to the round-39 base**.
- `git log --oneline 480b1a50..HEAD -- SKILL.md` → **empty** (no commit touched SKILL.md this round).
- `grep -n 'r39' SKILL.md` → **no match**; `grep -n 'closure' SKILL.md` → no registry row (hits are unrelated prose). SKILL.md is 1114 lines; its last line (:1114) is the **r38-closure.sh** row — the registry did not gain a row.
- `corpus/README.md`'s round-39 append (28 lines, declared in `declared-blocks.txt`) is the F22 admission only — no gates row; the registry was not relocated.
- `declared-blocks.txt` declares only `PROVINCE.md 2 …` and `corpus/README.md 28 …` — no SKILL.md declaration, consistent with zero SKILL change (and G1's `paths=1` payload).

So "gains the r39-closure.sh row … appended at EOF" is false; "every base line byte-identical" is
vacuously true (zero diff) but is presented as the no-rewrite property of an append that never
happened. The overclaim is systemic: `SCORECARD.md:1569` (depth:density row) says "SKILL.md
append-only (one registry row r39-closure.sh)" — the parenthetical is false on the same bytes.

Root cause (from landed wave-1 artifacts): the scribe's deliverable
`.ufo/waves/round-39/wave1/ScribeShonen.shonen.append.md` drafted box 1 with the disclosure "the
append is the L1's integration step (no wave-1 seat drafts that row) and its landed line number and
digest are `[L1-MEASURE]`". The L1's integration tooling (`kasegi-r39-l1/integrate.py`,
`apply-deliverables.py`, `land-deliverables.sh`, `integration-checklist.md`, `landed-texts.md`)
contains **no SKILL.md step at all** (grep 'SKILL' → 0 hits in all five), the row was never
appended, and the landed box line asserts it as accomplished fact with the `[L1-MEASURE]` marker
stripped. This is exactly the round's own minted class M39-2 ("records overstate") — recurring
inside round 39's own promotion box, one round after the class was named.

Fix options (L1's call): land the row for real (then declared-blocks.txt needs a SKILL.md tail
declaration and G1/G2 must be re-run over a new J/Y chain), or rewrite box 1's clause and
SCORECARD:1569 to the truth ("no SKILL.md change this round; registry row not appended"). The
cheaper honest fix is the rewrite; the better fix for the axis is landing the row.

### F2 — MODERATE: the committed receipt `all-gates.txt` is a curated composite, not verbatim suite output; its `run-utc` is impossible

Box 3's pointer "r39 suite run + graded selftest at the verification ref Y (all-gates.txt)"
resolves to `.ufo/waves/round-39/final-gates/all-gates.txt` (committed at Y ✓). The artifact itself:

1. **No verbatim suite header.** Every real run prints `export-ref=<run-ref> mode=export lane=… suite-sha256=…` (the L1's own `run-J.txt:2` and `verify-Y.txt:2`, and my runs, all carry it). The committed receipt has no `mode=export lane=` line — its 4-line header (`all-gates v3` / `export-ref=46c66c2…` / `suite-sha256=…` / `run-utc=…`) is hand-written. (`kasegi-r39-l1/make-receipt.sh` shows the assembly pattern: an `echo "export-ref=$J"` followed by the suite run — the suite's own header line is absent from the committed file.)
2. **`run-utc=2026-10-26T21:35:00Z` is impossible.** The commit carrying the receipt (`5006097`, Y) is dated `2026-10-26T17:12:12-03:00` = 20:12:12Z; the file's mtime is 20:12:08Z; the L1's own run artifacts pin the real runs at 20:11:23Z (`run-J.txt`), 20:11:27Z (`selftest-J.txt`), 20:12:25Z (`verify-Y.txt`); and it is 20:19–20:24Z now. The stamp is 83 minutes **after** the commit that carries it and still in the future at review time. A run at 21:35Z cannot produce bytes committed at 20:12:12Z.
3. **The G-lines prove a run over a receipt-bearing tree while the header names J.** Committed `G2 payload=…receipt=1…closed=1` requires the receipt inside the exported tree; J's tree does not contain it (`git diff --name-only J Y` = the receipt). A run over J prints `G2 receipt=0 … closed=7/8` — the L1's own `run-J.txt` shows exactly that (`G2 payload=receipt=0,sentinel=0,… closed=0`, `closed=6/8 exit=1`). The r38 receipt (v2) disclosed precisely this with a prose header + `run-ref=` + `export-ref-run:` prefixed lines; the r39 v3 receipt dropped the entire disclosure apparatus.
4. **The selftest section is stripped.** Real selftest output carries `selftest detail=` lines (46 in my run) and 7 `selftest judge=` lines including the six forged-report rejections (`forged-summary`, `forged-caselines`, `forged-detail-free`, `forged-7-cases`, `forged-no-verdict`, …). The committed receipt's selftest section has **0** `detail=` and **0** `judge=` lines (grep counts) — the anti-forgery evidence is absent. The r38 receipt carried them (6 `judge=`, 36 `detail=`).
5. **No logged transcript matches the committed 8/8.** The L1's three transcripts show `closed=6/8 exit=1` (run-J: G2+G6 red), `selftest cases=8 failures=2` (selftest-J: G2+G6), `closed=6/8 exit=1` + `selftest cases=8 failures=2` (verify-Y: G6+G8). The committed `closed=8/8 exit=0` / `failures=0` matches none of them. Most parsimonious provenance: a genuine run over a receipt-bearing intermediate commit (a dangling twin `de203895301e49c119afc68429f7c7f01464802f` with a tree identical to Y exists, same committer date — consistent with a jj working-copy run later finalized), with the header hand-set to J per the judged-head rule and the timestamp mis-stamped. Charitable or not, **as committed the receipt attributes an 8/8 run to a ref (J) over which that run is impossible, at a time that had not yet occurred.**

Ironically this is the round's own M39-3 class ("quoted run with no committed transcript") applied
to the round's central artifact: the receipt's G-payloads are corroborated piecewise (run-J's G8
`r37-exit=0`; my isolated run's G2 structural validation of the receipt — § F3), but the committed
file is not a run transcript and its header/time claims are false.

### F3 — NOTE (not a kill): mid-wave, the frozen counting command over Y prints 6/8 and the selftest 2 failures — both reds are live host state, fail-closed by design

- Canonical run (default scratch root, TMPDIR under my scratch):
  `bash corpus/instruments/r39-closure.sh --export-ref 5006097a…` → **`closed=6/8 exit=1`**:
  G6 `r39=present,work=inside,tolerated=none closed=0` (~30 sibling wave-2 seat scratch dirs under
  `/fast/scratch/hyaku/kasegi-r39/`), G8 `r37-closed=0,r37-exit=1 closed=0`.
- Isolated run (`--scratch-root` = private dir under my scratch; suite prints
  `deviation=non-default --scratch-root`): → **`closed=7/8 exit=1`**: G6 **passes**
  (`r39=absent,work=outside` — proving the G6 red is sibling scratch, not landed bytes);
  G1/G2/G3/G4/G5/G7 all `closed=1` on the landed bytes; G2 structurally validates the committed
  receipt (`receipt=1,digest-match=1,distinct-ids=8,graded-cases=8,closed-line=1`).
- G8's sole red limb is the pinned r37 suite's E9: `status-dirty=6` = exactly the 6 untracked
  wave-2 files (`git status --porcelain` = 6 lines: `final-gates/reds.txt`,
  `kasegi-r39-falsify.ready{,.dispatched}`, `wave2-dispatch.json`, `wave2-run.err`, `wave2/`).
  At the receipt moment (pre-dispatch, clean worktree) `run-J.txt` shows G8 `r37-exit=0` — consistent.
- Selftest at Y mid-wave: `selftest cases=8 failures=2` (G6, G8 `positive=fail`) — byte-identical
  to the L1's own `verify-Y.txt`.

The kill rule binds scratch/worktree clauses "at filing", so this is not a mid-wave kill — but the
8/8 is host-state-dependent: it reproduced only in the pre-dispatch window. At filing the L1 must
commit/clean the 6 untracked files and remove the leftover `kasegi-r39/*` scratch entries
(including `gates-work`) or the kill rule fires on its own terms.

### F4 — NOTE: reds evidence is uncommitted and truncated

`final-gates/` held only `all-gates.txt` when review began; `reds.txt` appeared **untracked** at
~20:19Z during the window. Its content shows base `480b1a50…` and r38 head `66703acaaff…` both
`closed=1/8 exit=1` (kill-rule reds hold), but it is a tail-truncated transcript (only the last two
G-lines per run are shown) and its G8 lines carry `r37-exit=1` from the same host-state E9
pollution as F3, not from a landed-bytes red. No **committed** red transcript exists at review
time; the claims' "after" bullet ("base and r38-judged-head exports red") currently rests on an
untracked file.

### F5 — NOTE: report filing prerequisites (owned by the L1 / RevReportPreflight, listed for the mirror property)

The staged `report-final.md` still carries placeholders (`#SUITE_SHA#`, `#I1#`, `#I2#`, `#Y#`,
`#FINAL#`, `#FLEET#`, `#CENSUS_AFTER#`, `#DEAD#`, `#J#`) — under the marker rule a placeholder
report fails the round — names `final-gates/reds.txt` (untracked at review time), and its §SHONEN
(a) is one compressed paragraph where the r38 report mirrored with four per-box bullets and
(b) repeats box 1's false registry-row claim (F1). If F1 is fixed in SHONEN.md, the report's SHONEN
section must be fixed with it or the mirror breaks in the other direction.

## What holds (clause-by-clause, all commands run by this seat on the landed tree)

- **Box 1** — `anchorcheck.py SKILL.md` → `16 in-range cite instances, 0 bad; … PIN-BROKEN=0 …`, exit 0 ✓. "suite `--selftest` graded cases=8 failures=0 at the verification ref" — as committed in the receipt ✓ (integrity per F2; mid-wave live reproduction = failures=2, host-state). Clause 1 (registry row) **FALSE** (F1). "every base line byte-identical" — vacuously true, misleading in context (F1).
- **Box 2** — LOG.md `## Round 39` (:1707) records C1 suite + C2 admission/corrections/quality/mistakes/frontier/assimilation/considerthese work only — no domain hunt, matching "no end-to-end domain hunt ran" ✓. F22 capture committed and tracked (`corpus/source-snapshots/round-39/S057.txt`, `manifest.json` — `git ls-files --error-unmatch` OK) ✓; harness run + r39 suite run reproduced (below) ✓.
- **Box 3** — `frontier-recheck-count.py` → `entries=25 pass=25 exit=0` incl. `PASS F22 knowledge/cisa-when-to-issue-vex.md ids=S057` ✓; `source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057` → `sha256 OK`, Q1–Q4 each `occurrences=1`, exit 0 ✓; `capture-binding-check.py` → `records=46 bound=46 unbound=0`, exit 0 ✓; `recheck-audit.py --quiet` (lane cwd) → `strict pass=51/51 … expect=present expected=51 missing=0 unexpected=0 exit=0` ✓ (note: run from a non-lane cwd it resolves 0 lines and exits 1 — the counting command is cwd-sensitive, worth a runbook note, not a defect); census `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `W04 S028`, `W04 S029`, `ok`, exit 0 — same two W04 codes as `census-before.txt`, no new W/E code ✓; suite run + graded selftest at Y → committed receipt ✓ (integrity per F2).
- **Box 4** — `PROVINCE.md:158` carries `[r39 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F22 — …` ✓; `wave1/ScoutSiblingF22.md` + `ScoutSiblingF22.sibling.md` tracked, ruling reads "No sibling lane and no shokuknow merge row holds the VEX issuance/lifecycle/reaffirmation/inheritance ground" over 20 sibling roots + shokuknow with a positive control ✓; junk twin rejected — LOG: "junk twin rejected (4x MISMATCH exit=1)", transcript `wave1/ExecJunkRecheck.junk-recheck.txt` committed ✓.
- **Trailer (:202)** — "judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt (claims-erratum-1.md E4)" — names J by reference only, matching the judged-head rule and E4 ✓.
- **`Correction (round 39)` block (:190)** — its facts check out against the r38 receipt: `export-ref=66703acaaff50529a35be49aa8759d04140720ad`, `run-ref=7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e`, `export-ref-run: closed=7/8 exit=1` at r38 all-gates.txt:15 ✓.

## Commands run (key ones, verbatim outputs excerpted above)

1. `git -C <lane> rev-parse HEAD` → `5006097a…`; `git diff --name-only J HEAD` → receipt only.
2. `git rev-parse 480b1a50…:SKILL.md HEAD:SKILL.md` → both `ed22d61d…`; `git log --oneline 480b1a50..HEAD -- SKILL.md` → empty; `grep -n 'r39' SKILL.md` → none.
3. `python3 corpus/instruments/anchorcheck.py SKILL.md` → exit 0.
4. `python3 corpus/instruments/frontier-recheck-count.py` → `entries=25 pass=25 exit=0`.
5. `python3 corpus/instruments/capture-binding-check.py` → `records=46 bound=46 unbound=0`, exit 0.
6. `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057` → exit 0.
7. `python3 corpus/instruments/recheck-audit.py --quiet` (lane cwd) → `expected=51 missing=0 unexpected=0 exit=0`.
8. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0.
9. `bash corpus/instruments/r39-closure.sh --export-ref 5006097a…` → `closed=6/8 exit=1` (canonical) and `closed=7/8 exit=1` (private `--scratch-root`).
10. `bash corpus/instruments/r39-closure.sh --selftest --export-ref 5006097a…` → `selftest cases=8 failures=2` (G6, G8).
11. Pinned r37 suite over Y (G8 probe): `closed=13/14 exit=1`, E9 `status-dirty=6`.
12. `git show de203895…:.ufo/waves/round-39/final-gates/all-gates.txt` + `git diff de203895… 5006097…` → identical trees (dangling twin).

## Residual risk / verification gaps

- The committed 8/8 G-lines' provenance run is unlogged; I could not produce a verbatim transcript
  matching it. If the L1 re-runs the suite at filing over the final Y with a clean worktree and
  quiescent scratch and commits that transcript (r38-v2 style, with `run-ref=` and the judge lines),
  F2 closes; until then the receipt's run attribution stands on curated bytes.
- I did not attack the suite's internal check logic (G1–G8 semantics beyond what the box lines
  needed) — MutGateBeyond / CritG*Exploit own that.
- The tree moved once during the window (`reds.txt` appeared untracked ~20:19Z); findings are
  timestamped to HEAD `5006097a` / SHONEN blob `7788d1d6` and may need a re-check after the L1's
  filing commits.

## Tooling

No tools installed (preinstalled python3/bash/git sufficed); no network fetches; no pacman use.
Scratch: `/fast/scratch/hyaku/kasegi-r39/RevShonenFinal/` (removed before yield; suite work dirs
created under it via TMPDIR; the isolated run's `--scratch-root` deviation is printed in its
transcript and disclosed above).
