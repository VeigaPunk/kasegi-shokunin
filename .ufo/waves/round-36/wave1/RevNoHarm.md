# RevNoHarm — planned round-36 write set vs base (no-harm review)

Seat: `RevNoHarm` (reviewer, leaf — no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `cc692008b0cfd58d18275aa6c4aed79620120799`; claims freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`
(= lane HEAD at my read; the freeze commit changed exactly 4 files, 97 insertions, all new files under
`.ufo/waves/round-36/` — `c1-controls/before.txt` +9, `c2-controls/before.txt` +9, `census-before.txt` +3,
`claims.json` +76 — so base and freeze corpus bytes are identical). Judged axis: depth:verifiability.
Review state bound to **2026-10-26T15:56Z** (60 receipts in the wave dir); the wave was still landing, so
every receipt-digest statement below carries its observation instant.

Writes made by this seat: this receipt only, plus scratch under `/fast/scratch/hyaku/kasegi-r36/RevNoHarm/`
(removed before yield). No lane, fleet, sibling-lane or source-tree file edited; no mutating git/jj command
(read-only `rev-parse/log/show/diff/status/ls-tree/ls-files/archive/merge-base/cat-file` only); no tool
installed (nothing needed; pacman untouched). No LSP server exists for this corpus (markdown) — verification
is by `git archive` exports, digest-bound extraction and simulated landings, per the item.

## 1. Method

1. **Base export.** `git -C <lane> archive cc692008… | tar -x -C <scratch>/base` — the review base is the
   exported tree, not the worktree (the worktree holds only untracked round-36 wave artifacts; verified
   `git status --porcelain` = 9 entries, all `?? .ufo/waves/round-36/*`).
2. **Proposed writes extracted verbatim from seat receipts** under `.ufo/waves/round-36/wave1/`, each
   single-line insert extracted by its unique line prefix and digest-cross-checked: my extraction of the
   three ScribeRowS053 lines reproduces ExecC2Harness's published `post1` `corpus/SOURCES.md` digest
   `a2c4828f…4d3544d6` exactly (byte-identical extraction, independently computed).
3. **Simulated landings.** Each proposed write applied to the base export in scratch; `diff base proposed`
   must be pure additions (`<` lines = 0). SOURCES.md simulated both with and without the correction line.
4. **Anchor arithmetic.** Every existing `path:NN` citation into each touched file was enumerated over the
   base export and classified: stays-valid (EOF-append targets), shifts (SOURCES.md mid-file insertions),
   or already-stale (pre-existing trail).
5. **Baseline instruments re-run on the base export**: `density.py SKILL.md` → mean **220.9**, 26 blocks,
   742 path-citation instances, exit 0 (independently reproduced; matches `ScribeScorecard` §3 and
   `ExecInstrumentsSynopsis` §4.8). `anchorcheck.py` was deliberately NOT re-run from the scratch copy: the
   instrument resolves lane-relative cites against the lane root, so a scratch run manufactures false
   `BASE-ABSENT` failures (the hazard round-35's `ExecNoHarmFinal` §F6 documented); its in-lane baseline
   (16 in-range / 0 bad, exit 0) is cited from `ExecInstrumentsSynopsis` §4, whose SKILL.md bytes equal
   base bytes (`daeff71b…`, verified by me at both commits).

## 2. Inventory of the proposed write set

| # | target | base state (measured) | proposed write | producing receipt | shape | verdict |
|---|---|---|---|---|---|---|
| 1 | `corpus/knowledge/epss-exploit-prediction-scoring.md` | absent (`ls` exit 2) | new entry — final bytes 263 lines / 17,374 B, sha256 `36df1b1f…` (ExecC2QuoteOnce's PASS binds these; see D1) | `ScribeEntryF19.md` §6 fence | new file | PASS (D1) |
| 2 | `corpus/SOURCES.md` | 112 lines, 52 registry rows, S052 `:58`, `## Paths` `:60`, `## Search log` `:67`, CISA bullet `:79`, `## Leads` `:81`, `## Registry changes` `:87`, S043 change-cell `:94` | 4 single-line insertions: S053 row after `:58`; Paths study line inside `## Paths`; F19 sweep bullet inside `## Search log`; S052-bullet correction after the CISA bullet | `ScribeRowS053.md` §1.1–1.3; `ScribeSOURCSCorrection.md` §1 | simulated `+4/−0` (with correction), `+3/−0` (without) | PASS (§4, D3) |
| 3 | `corpus/lessons/round-36.md` | absent | new lesson — landed fence 404 lines / 36,315 B, sha256 `540af067…` (the receipt binds exactly these bytes after its 12:54:21Z re-pin; see D9) | `ScribeGateLesson.md` fence | new file | PASS (D3; D9 resolved) |
| 4 | `SCORECARD.md` | 1404 lines, last heading `## Round 35` `:1284` | `## Round 36` section appended at EOF | `ScribeScorecard.md` §2 | EOF append | PASS |
| 5 | `PROVINCE.md` | 75 lines, F16 `:74`, F17 `:75`, F18/F19 counts 0/0 | two one-line frontier amendments (F18, F19) at EOF in the `:74`/`:75` form | L1-authored (no seat drafts the exact lines; `ScribeShonen` §6 + `ScribeConsiderthese` #5 fix the shape) | EOF append | PASS structurally; bytes unverifiable pre-landing (§7) |
| 6 | `SHONEN.md` | 160 lines | four box-evidence blocks + measurement-state paragraph | `ScribeShonen.md` §3–§7 | simulated `+98/−0` at EOF | PASS (D5) |
| 7 | `LOG.md` | 1659 lines, last heading `## Round 35` `:1651` | `## Round 36` entry at EOF | `ScribeLOG.md` §7 | EOF append | PASS |
| 8 | `corpus/QUALITY.md` | 250 lines / 33,731 B (sha `d4f83bb1…`), R22 `:226`, R23 `:227`, R26 `:249`, R27 `:250` | R28 + R29 rows + intro block appended after `:250` | `ScribeQualityRows.md` §1 | EOF append | PASS |
| 9 | `SKILL.md` | 1104 lines, Gates & probes registry `:977`, per-round addition sections `:1037–:1104` | `## Round-36 Gates & probes registry addition` at EOF with exact-basename rows `r35-defect-closure.sh` AND `r36-closure.sh` (E3) | L1-authored (no seat drafts the rows; shape per the round-29/30/31/33/35 sections) | EOF append | PASS structurally; bytes unverifiable pre-landing (§7) |
| 10 | `corpus/instruments/r36-closure.sh` | absent | new suite — frozen digest `4db1ae70…` (894 lines / 39,022 B); the landed receipt's verbatim fence hashes to exactly that (verified by me) | `ExecC1SuiteBuild.md` :348 fence | new file | PASS as file; evidence re-binding owed (D2) |
| 11 | `corpus/instruments/r36-fixtures/` + generator | absent | per-limb red/green fixtures | `ExecC1Fixtures.md` | new files | PASS |
| 12 | `corpus/source-snapshots/round-36/{S053.txt,manifest.json}` | absent | capture 244 lines / 8,448 B (sha `4ec61c59b0e9…`), manifest 3,566 B (sha `f9590c2b…`) | `ExecC2Capture.md` §2–§3 | new files | PASS |
| 13 | `.ufo/waves/round-36/c2-controls/junk-f19.md` | absent | junk twin 1,889 B (sha `ea078f05…`), outside the `corpus/knowledge/` glob | `ExecC2JunkControl.md` §2 | new file | PASS |
| 14 | `corpus/instruments/knowledge-expected.txt` | 49 lines / 47 entry rows (sha `d2e99ca6…`) | entry inserted at its SORTED position (after `cwe-top25-2025-methodology.md`, before `ev-model.md`), once | `ExecC2Harness.md` §1.1 | sorted insert `+1/−0` | PASS |
| 15 | `corpus/README.md` | 396 lines, 18 F-rows, F18 row `:388` | round-36 admission section at EOF carrying the `| F19 |` row (or, in ExecC2Harness's derived test form, one row after the F18 row) | L1-authored (`ExecC2Harness` §5 F1 derives a test row; no seat drafts the section) | EOF append (or +1 mid-table) | PASS structurally; bytes unverifiable pre-landing (§7) |
| 16 | `.ufo/waves/round-35/wave1-results.json.provenance.md` | absent (the round-34 note exists; E4 needs the round-35 one) | new provenance note beside the round-35 results file (E4 limb) | L1 landing item (`ScribeGateLesson` §4.4) | new file | PASS |
| 17 | optional standalone E9 gate | absent | 320-line bash draft (sha `ecd3bb82…`), landing optional | `ExecQuiescenceProbe.md` | new file if landed | PASS |

Everything else the wave produces (wave receipts, `wave1-results.json`, assimilation artifacts) is new-file
or receipt-only and touches no pre-existing line. A landing-language grep over the 60 landed receipts
proposed writes to existing files in `ScribeRowS053`, `ScribeQualityRows`, `ScribeScorecard`; direct reads
add `ScribeSOURCSCorrection`, `ScribeShonen`, `ScribeLOG` — all reviewed above, and no other receipt
proposes one.

## 3. Deletions / rewrites of existing lines

Simulated landings diffed against the base export:

| file | simulated diff | `<` (deleted) | `>` (added) |
|---|---|---|---|
| `corpus/SOURCES.md` (row+paths+bullet+correction, canonical order) | 4 insertions | **0** | 4 |
| `corpus/SOURCES.md` (ExecC2Harness post1 order) | 3 insertions | **0** | 3 |
| `SHONEN.md` (§3–§7 blocks at EOF) | 5 blocks | **0** | 98 |
| all EOF-append targets (`SCORECARD`, `LOG`, `QUALITY`, `PROVINCE`, `SKILL`, `README`) | append-only by construction | **0** | N/A |

No seat draft proposes a deletion, a cell rewrite, or an in-place edit of any existing line. Spot-verified
negatives: `ScribeSOURCSCorrection` explicitly never edits `:79` (the correction is a new line; the old
bullet is byte-intact in my simulated landing); `ScribeQualityRows` names R22/R23/R26/R27 as untouched and
adds neither `supersedes` literal (E7's counts stay 1/1); `ScribeScorecard`'s block contains no placeholder
literal and no angle-bracket token (E1-safe); `ScribeShonen`'s blocks contain neither E1 literal (measured
on the extracted bytes) and keep all four boxes `[~]` (no promotion rewrite); the lesson fence contains
neither E1 literal (measured on the landed fence bytes).

## 4. R6 line-anchor preservation (mid-file insertions: SOURCES.md; knowledge-expected.txt is line-safe)

`corpus/QUALITY.md:40` (R6): an edit to a file other files cite by line number keeps every existing line at
its number (append at end, or same-line suffix). Of the nine touched existing files, seven take EOF-only
appends (`SCORECARD`, `PROVINCE`, `SHONEN`, `LOG`, `QUALITY`, `SKILL`, `README`) → every existing line keeps
its number by construction; `knowledge-expected.txt` takes one sorted mid-file insert and has zero
line-number citations in the tree (line-safe); `corpus/SOURCES.md` takes four mid-file
insertions (the registry row cannot go elsewhere without tripping census E12 — the ruling recorded in
`corpus/lessons/round-31.md:107`), so line numbers ≥ 59 shift. Cumulative shift table, measured on my
simulated landing (canonical order: row → Paths line → F19 bullet → correction; the correction and F19
bullet may swap — every EXISTING anchor below is identical under either order because both new lines sit
above them):

| anchor (base `b47f2cd`) | base line | after landing |
|---|---|---|
| `## Paths` | 60 | 61 |
| `## Search log` | 67 | 69 |
| CISA sweep bullet (cited unqualified as `:79` by `corpus/lessons/round-35.md:271`) | 79 | **81** |
| S052-bullet correction (new) / F19 sweep bullet (new) | — | 82 / 83 (or 83 / 82) |
| `## Leads (unopened)` | 81 | 85 |
| `## Registry changes` | 87 | 91 |
| S043 change-cell line (cited as `:83` by `round-29.md:214`, `round-29-verifier-spotcheck.md:74`) | 94 | **98** |
| S052 row-added note | 108 | 112 |
| round-35 "superseded" / "scope correction" lines | 111 / 112 | 115 / 116 |

Exposure classification over the whole base tree:

- **Stays valid**: every citation into the EOF-append targets — `SCORECARD.md` `:331/:502/:813/:1145/:1263-1281/:1269/:1271/:1284`, `QUALITY.md` `:95/:249-250`, `README.md:159`, `SOURCES.md` `:46/:54/:55-56/:57/:58` (all below the `:59` insertion point). Verified by tree-wide grep of the citation tokens.
- **Goes stale this round (known M31-3/M33-3 anchor-drift class; record, never rewrite)**: `corpus/lessons/round-35.md:271`'s unqualified `corpus/SOURCES.md:79` → +2 stale after landing. The correction line itself base-qualifies its `:79` pointer (`b47f2cd`), so it stays R9-resolvable.
- **Already stale at base, deepens +11 → +15**: the `SOURCES.md:83` trail (`round-29.md:214`, `round-29-verifier-spotcheck.md:74`; actual line `:94` at base → `:98` after landing). Pre-existing routed debt (M31-3/M33-3); round-36 does not create it and must not chase it with rewrites (R9).
- **Pre-existing, not round-36's**: `corpus/lessons/round-35.md` cites `corpus/SOURCES.md:255` — PAST-EOF at base (the file is 112 lines). Noted so it is not attributed to this round's insertions.
- **Nothing cites `SOURCES.md:111`/`:112`** — verified by tree-wide grep (only unrelated `:111` hits in other files), confirming `ScribeSOURCSCorrection`'s claim.

## 5. Core-text edits

None found. Specifically: no existing SOURCES row or cell is edited (the 52 base ids are an exact prefix of
the proposed 53, in order; the S053 row is 11 cells / NF 13, no embedded `|`, id/kind/tier/status/opened/
recheck/used-by exactly per the frozen C2 predicate — all measured on my simulated landing, registry count
52→53); no QUALITY row is edited; no SKILL core body line is touched (the registry addition is a new EOF
section, the established round-29/30/31/33/35 shape); SHONEN boxes stay `[~]` with evidence appended
(round-35 landed shape was `+23/−0`); LOG/SCORECARD take new `## Round 36` sections at EOF; entry, lesson,
instruments, capture, manifest, junk twin and the E4 note are new files. The frontier count moves 18→19
exactly via the new F19 row (counting command verified placement-independent).

## 6. Findings

**D1 (must-fix at landing — digest drift, already repaired mid-wave; land the repaired bytes).** The F19
entry's 12:41Z composition carried the capture digest as `4ec61c59b0a9aedf…` (drift at hex 11: `b0a` vs the
true `b0e`) in four places. The 12:43Z revision fixed it; after the peer-review round the FINAL entry bytes
are 263 lines / 17,374 B, sha256 `36df1b1f…` (verified by my extraction of the current
`---BEGIN ENTRY---` fence; `ExecC2QuoteOnce`'s PASS binds exactly these bytes per `ScribeGateLesson` §4.8b).
The manifest's record `sha256` field is the true `b0e` digest (verified by parsing the manifest fence in
`ExecC2Capture.md`), so entry-vs-manifest-vs-row are consistent only in the current bytes. Stale references
to pre-revision bytes the L1 must disregard: `ExecC2Harness.md` F2 and its §1.1 entry row (17,267 B /
262 lines / `27a4d42a…` — measured before the fix), and `ScribeEntryF19.md` §1's own "262 lines / 17,251
bytes" header. The wrong digest string survives by design only inside record sections that quote it as the
error (`ScribeGateLesson` §4.3 counts 3 full wrong strings in `wave1/`); any later grep for the bad digest
must exempt record sections.

**D2 (evidence re-binding owed at landing).** The suite digest moved repeatedly under peer attack (lineage
`1019d64d` 710 → `9fbdee69` 780 → `dc5208fa` 774 → `76273416` 817 → **`4db1ae70` 894**, the frozen
revision). The landed `ExecC1SuiteBuild.md` now carries the `4db1ae70` verbatim text — I extracted the
`:348` fence and hashed it to exactly `4db1ae70c76afd28…adb7c4` (894 lines / 39,022 B), so the canonical
bytes ARE in a durable artifact. Residual: most C1 evidence receipts were measured on `76273416`
(`ExecC1BaseFail` negative arms 0/9 and 4/9; `ExecC1ExportMode` PASS incl. the `--no-optional-locks`
lane-write fix; `ExecC1Fixtures` matrix) and are being revised to `4db1ae70` (revised mtimes 12:53–12:54Z
at my read); `RevC1Suite` (12:49Z) and `CritC1Export` (12:45Z) still bound older digests at my read. The L1
must land bytes hashing to the receipt's CURRENT frozen digest and confirm at closure that the negative
arms, export-mode discipline and fixture matrix are bound to the landed digest (the seats announced each
move; re-runs were in flight). Note: the suite's own text necessarily contains the literals `filled by the
L1` / `<LANE_HASH>` (it greps for them); E1's grep is SCORECARD-scoped, so no self-trip — verified against
the frozen claim's counting commands.

**D3 (should-fix in the lesson draft).** The landed lesson fence (Gate → standing-refusals table) cites
`corpus/SOURCES.md:76-77` unqualified (S081/S082 refusal prose — verified present at those base lines).
Those lines shift to `:78-79` under the planned insertions, so the citation is born stale (M31-3 class) in
the round's own lesson. Repair at composition: base-qualify the pointer (`at base b47f2cd`) or cite the
post-landing numbers. Everything else the lesson cites into existing files stays valid (`QUALITY.md:249-250`,
`:227`, `SCORECARD.md:1271` — all EOF-append-safe).

**D4 (record, do not rewrite).** `corpus/lessons/round-35.md:271`'s unqualified `:79` goes +2 stale and the
`:83` trail deepens +11 → +15 (§4). The lesson's `## No-harm` section defers to `wave1/RevNoHarm.md` and
`ExecRegressionBase` (`ScribeGateLesson` :406) — this receipt's §4 table IS the recording; the landed lesson
should cite it explicitly so the M31-3-class deepening is recorded in-lane. No lesson file may be rewritten
to chase the drift (R9).

**D5 (integration note).** `ScribeShonen.md` §2 rule 1 says the box drafts "append under the existing four
`[~]` items" while its §11 says they "append cleanly after `SHONEN.md:160`". The verbatim drafts (box-title
line + evidence paragraph, ×4) fit the EOF append; an in-box insertion would need the repeated title lines
stripped. Both are zero-deletion; the L1 picks one and measures once. If the EOF shape is used, the 13 `⟨…⟩`
slots must be filled or their clauses dropped at landing (unfilled slots would be a new placeholder defect
of the class E1 polices in SCORECARD — and E1 does not read SHONEN.md, so nothing automated would catch
them).

**D6 (cosmetic, pick one).** ExecC2Harness's post1 places the Paths line after the section's trailing blank
(directly above `## Search log`) and the F19 bullet directly above `## Leads`; my canonical variant places
both before the trailing blank, matching how the existing bullets sit. Both are pure insertions (digests
`a2c4828f…` vs `d31ce458…`/`6e85c8a4…`); no counter or anchor depends on the choice.

**D7 (out of my axis, corroborated; for RevClaimsFreeze).** `.ufo/waves/round-36/c2-controls/before.txt`
records `"junk_present": "1"` while claims.json C2 `before` says "junk-f19 absent (control not yet built)"
and the file does not exist at the freeze. `ScribeGateLesson` §4.1 independently flags the key as unbacked.
No no-harm impact; the freeze reviewer should pin its meaning.

**D8 (cross-ref, C1 soundness — resolved at the final digest).** ExecC1Fixtures measured E8b/E8d survivors
at `76273416` and re-measured at `4db1ae70`: **no frozen-limb survivor remains** (clause mutants 10/14; the
residual E5b/E5c/E6b/E8b/E8d are the documented limits beyond the frozen wording, recorded in the suite's
documented-limits block). Also from ExecC1ExportMode: the pre-fix suite wrote `.git/index.lock` under the
lane via plain `git status`; the frozen digest carries `git --no-optional-locks` with 0 write syscalls
traced under the lane — the instrument's lane-write discipline is verified at the frozen digest.

**D9 (resolved at the 12:54:21Z revision).** The first landed `ScribeGateLesson.md` bound its lesson block
as sha256 `87fda89e…` / 399 lines / 35,810 B (:37, repeated at :676) with §6.4 printing a third variant
(35,701 B), while its own `---BEGIN LESSON---` fence measured 404 lines / 36,315 B — the post-SimplReport-fix
revision, digest never re-pinned. The 12:54:21Z revision re-pinned correctly: the receipt now binds
sha256 `540af0671e0d1e0f…e3d62` / 404 lines / 36,315 B, which matches the current fence bytes exactly
(verified by my re-hash after the revision). Residual for the L1: trivial — hash the fence it lands against
the receipt's binding at integration, as for every other landed artifact.

## 7. Verification gaps (honest limits)

- **L1-authored appends are not byte-reviewable pre-landing**: the PROVINCE F18/F19 lines, the SKILL.md
  round-36 Gates & probes section, the README round-36 admission section, and the E4 provenance note exist
  (at my read) only as shapes specified in other receipts. My PASS for them is structural (target anchors
  verified: PROVINCE ends `:75`, SKILL `:1104`, README `:396`; no live citation into any line an EOF append
  moves; the F19-row count is placement-independent). The L1 must run the post-landing trio on the
  integrated bytes: `git diff --numstat <base> -- <files>` (deletions must be 0), `anchorcheck.py SKILL.md`
  (0 bad, exit 0), `density.py SKILL.md` (mean move disclosed; precedent r35: 201.2 → 220.9 disclosed).
- **The wave was still landing at my 15:56Z bound** (60 receipts; several C1 receipts mid-revision to
  `4db1ae70`). Every digest statement here carries its observation instant; the L1 re-checks drift at
  landing. Receipts still binding pre-`4db1ae70` digests at my read: `RevC1Suite` (`76273416`),
  `CritC1Export` (`ff616adc`), `ScribeReportDraft.md:114` / `SimplC1.md:8` (`ff616adc` mentions).
- **Post-landing E9 quiescence** (clean worktree, zero seat scratch dirs) is red by construction mid-wave
  (49 seat dirs at my read) and only meaningful at closure.

## 8. Verdict

**PASS with conditions.** Every seat-drafted write to an existing file is a pure insertion or EOF append —
zero deleted lines, zero rewritten lines, zero core-text edits across the whole proposed set (measured on
simulated landings, not inferred). Line-anchor preservation per R6 holds for every EOF-append target by
construction and is fully tabulated for the one mid-file-insertion file (`corpus/SOURCES.md`, §4). The
conditions are: D1 (land the repaired entry bytes `36df1b1f…`), D2 (land suite bytes hashing to the
receipt's frozen digest `4db1ae70…` and re-bind the evidence chain), D3 (fix the lesson's born-stale
`:76-77` citation), D4 (record the anchor shifts in the lesson via this receipt's §4), plus the §7
post-landing measurements (D9 resolved mid-review). No defect in the proposed set deletes, rewrites, or
re-anchors any existing line.

Report: .ufo/waves/round-36/wave1/RevNoHarm.md
