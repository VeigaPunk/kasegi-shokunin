# ReviewC1Sites — C1 site truth, round 95 w1

Seat: leaf reviewer. Base `9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10`; freeze
`347519f21524d2bc13eb6c91cf3550930a4265b3`; C1 landing
`53ec479d71d25cf5be052db794a548a5904564b8`; map `.ufo/waves/round-95/c1/repair-map.tsv`
(sha256 `8545eba2c39a1fed66b5d6eba59de973c182208aa8b06d28013417821359beb6`).

Method: (1) reconstruct the landing from the base plus the map — every row's `old`
must occur on its line at the base and every `new` must occur on its line at the
landing; the reconstructed files must equal the landing bytes exactly. Result:
`rows_applied=16 files_exact=2/2`, both files byte-identical (`reconstruct.txt`).
`git show --name-status 53ec479` lists only the two corpus files (14 insertions,
14 deletions), so no unlisted edit rides the landing. (2) For each NEW text, read
the committed bytes of the anchor it cites at the landing and test the asserted
facts, not the label's premise. (3) Re-derive the residual sites with the lane's
own resolver (`corpus/instruments/resolve.py`) against a scratch fixture.

## Verdict

**C1 site truth: 14/16 CORRECT, 2/16 PARTIAL, 0/16 WRONG.** The sixteen edits are
byte-exact at their sites. The two PARTIALs (`triage-thresholds.md:88`, first
part, and `:90`) cite `SKILL.md:182-184` for a correction whose asserted predicate
completes on line 185; exact one-line fixes are in the round-96 label set. The C1
frozen predicate (P1 meter, P2 counter hash, P3 path set) is **not re-scored by
this seat**; on the site-truth limb of the C1 statement ("whose new text is true
of the anchor they cite") the claim does **not fully stand as written** — it is
qualified by those two PARTIALs, not failed at the predicate. The four exact-cell
rewrites (`89`, `356`, `434`, `435`), the `396` and `436` repoints, the five S041
token repairs, and **three** of the five part repairs (`88` second part, `433`
both parts) re-derive CORRECT; the other two part repairs are the PARTIALs. One
bare backticked S041 capture citation survives on the edited line 13 (GONE under
the lane resolver) and is routed with an exact round-96 label.

## The sixteen rows

Quotes are the committed lines at the landing; full lines are in the receipts.
`182-184` means `SKILL.md` lines 182-184, etc.

| # | site | key | new anchor | cited bytes (quoted) | verdict |
|---|---|---|---|---|---|
| 1 | `triage-thresholds.md:89` | `SKILL.md:175` | `SKILL.md:182-184` | `184: …> reward.min×1000 > is_live(1) (round-13 correction: earlier` | **CORRECT** — 182-184 writes the current queue tail `reward.min×1000`; the earlier form is historical (pre-round-13 `7483333^:SKILL.md:176` reads `curated-EV(1e12) > reward.min — EV orders`), so "the earlier text wrote `reward.min`" is true of the superseded summary. |
| 2 | `triage-thresholds.md:356` | `SKILL.md:522` | `SKILL.md:999` | 999: ``- `~/Projects/bounties/bounty-map/schema.json` — program record schema (draft-07, fail-closed `additionalProperties:false`)`` | **CORRECT** — 999 is the program-record schema bullet; SKILL.md states no key list (`official_url` 0 hits, `source_kind` only the census sentence at 177). `[lost-base] schema.json:6` is not host-checkable (marked; see gaps). |
| 3 | `triage-thresholds.md:434` | `SKILL.md:175` | `SKILL.md:182-184` | 184: ``> reward.min×1000 > is_live(1)` (round-13 correction: earlier`` | **CORRECT** — 182-184 writes `reward.min×1000`; the earlier text's `reward.min` is the superseded form (same history as row 1). |
| 4 | `triage-thresholds.md:435` | `SKILL.md:10-11` | `[lost-base] fleet-dispatch.mjs:10`, `SKILL.md:182-184` | 182-184: five-term order ``priority(9e12) > continue(2e12) > curated(1e12, boolean on non-empty ev_inputs) > …`` | **CORRECT** — `curated` is third, behind `priority` and `continue`; `EV ordering` occurs **0** times in SKILL.md, so dropping the `SKILL.md:10-11` token is right; the `[lost-base]` comment is not host-checkable (marked). |
| 5 | `triage-thresholds.md:90` | `SKILL.md:113-114,175-176` | `SKILL.md:182-184,255-257` | 184: `…(round-13 correction: earlier`; 185: ``text omitted `is_live(1)`) — exactly 1024…``; 256: ``terms; `curated` is a boolean on non-empty `ev_inputs`, never an EV`` | **PARTIAL** — the curated half is fully inside 255-257, but the cell's assertion "earlier text omitted `is_live(1)`" completes on **185**, outside both cited ranges. Exact defect: the is_live-omission predicate is one line past the range; fix `182-184,255-257` → `182-185,255-257`. |
| 6 | `triage-thresholds.md:88` | `SKILL.md:113-114` | `SKILL.md:182-184` | 184: `…(round-13 correction: earlier`; 185: ``text omitted `is_live(1)`)`` | **PARTIAL** — same one-line shortfall: 182-184 carries the five-term expression and the correction's opening, but the asserted omission completes on 185. Fix `182-184` → `182-185`. |
| 7 | `triage-thresholds.md:88` | `SKILL.md:175-176` | `SKILL.md:255-257` | 256-257: ``terms; `curated` is a boolean on non-empty `ev_inputs`, never an EV / magnitude)`` | **CORRECT** — 255-257 states the curated-boolean correction exactly. |
| 8 | `triage-thresholds.md:433` | `SKILL.md:113-114` | `SKILL.md:182-184` and `SKILL.md:255-257` | `255: curated(1e12) > reward.min×1000 > is_live(1) (round-13 correction: five`; `256: terms; curated is a boolean on non-empty ev_inputs, never an EV` | **CORRECT** — the compound citation's second anchor (255-257) supplies the five-term correction ("round-13 correction: five terms"); 182-184 cuts the note at "earlier", but the pair carries the correction the cell asserts. Note the 182-184 half alone would be one line short. |
| 9 | `triage-thresholds.md:433` | `SKILL.md:175-176` | `SKILL.md:255-257` | 255-257: `round-13 correction: five terms; curated … never an EV magnitude` | **CORRECT** — 255-257 carries the correction; both lines are queue summaries. |
| 10 | `triage-thresholds.md:396` | `SKILL.md:245-247` | `SKILL.md:335-338` | `335-338: gitMutationBlocker / (fail-closed on rebase/merge/cherry-pick or non-main HEAD) is absent from / the mirror — 0 hits repo-wide; it existed only in the lost tree` | **CORRECT** — 335-338 states the fail-closed gitMutationBlocker rule; the marker list stays sourced by `ops-invariants.md:24`, which the cell also cites. Old 245-247 was the mission-ledger paragraph. |
| 11 | `triage-thresholds.md:436` | `corpus/knowledge/mission-control.md:21-23` | `corpus/knowledge/mission-control.md:21-27` | `23-27: Round-13 correction: the "negative-EV dispatches carry an ev_note" claim is dead code — ev_note (fleet-dispatch.mjs:204) fires only when ev_inputs.adjusted_ev is a negative number, which can never exist (schema additionalProperties:false, 0/1088 records); every mission_dispatched line logs adjusted_ev:"unknown".` | **CORRECT** — 21-27 carries the dead-`ev_note` substance; the old 21-23 stopped at "carry an". |
| 12 | `crosswalk.md:13` | `S041.txt:1868-1870` | `corpus/source-snapshots/round-30/S041.txt:1868-1870` | 1868: `P ガイドラインでは、ベンダに脆弱性公開ポリシーの策定を求めていません`; 1869-1870: `が、ISO/IEC 29147:2014 では、…その一 / 部を公開することを求めています。` | **CORRECT** (token) — the cited range is in range (file 2354 lines) and carries the divergence sentence. Same line 13 still carries a bare `S041.txt:1680-1681` (GONE); routed below. |
| 13 | `crosswalk.md:34` | `S041.txt:1792-1867` | `corpus/source-snapshots/round-30/S041.txt:1792-1867` | 1792: `(2) 脆弱性公開ポリシー`; 1867: `（出所：ISO/IEC 29147:2014 を元に作成）` | **CORRECT** — 1792-1867 is the clause-6 reproduction (English + Japanese), in range. Adjacent bullet pointers at line 36 are off by one for d)/e) (pre-existing; routed). |
| 14 | `crosswalk.md:43` | `S041.txt:1996-2079` | `corpus/source-snapshots/round-30/S041.txt:1996-2079` | 1996: `参考 1 ISO/IEC 29147:2014 と情報セキュリティ早期警戒パートナーシップガ`; 2079: `文献目録`; 2080: `55` | **CORRECT** — 1996-2079 is the 参考1 table through its last row (page number 55 starts 2080), in range of 2354 lines; the print-page claim p.53-54 holds (page markers 1994=`53`, 2080=`55`). |
| 15 | `crosswalk.md:54` | `S041.txt:1868` | `corpus/source-snapshots/round-30/S041.txt:1868` | 1868: `P ガイドラインでは、ベンダに脆弱性公開ポリシーの策定を求めていません` | **CORRECT** — the quoted sentence is on 1868. |
| 16 | `crosswalk.md:64` | `S041.txt` | `corpus/source-snapshots/round-30/S041.txt` | file exists at landing: 2354 lines, sha256 `e18acbf9…` | **CORRECT** — the file is committed at round-30 and byte-identical to the round-26 capture (`e18acbf9…` both); the fetch instant 2026-10-25T12:34:17Z is recorded in `.ufo/waves/round-26/wave1/ExecCaptureS041.md:17`, the log the sentence names. |

## Findings (severity order)

**F1 — MEDIUM — a bare backticked capture citation survives on the edited line.**
`crosswalk.md:13` carries two backticked S041 citations; the map repaired
`S041.txt:1868-1870` but the same line still reads
``(§3, `S041.txt:1680-1681`)``. `corpus/instruments/resolve.py` classifies the bare
token **GONE** and `corpus/source-snapshots/round-30/S041.txt:1680-1681`
**INTERNAL, 1680-1681 in range of 2354** (`resolver-s041.txt`). The range content
is true (1680-1681: `これらの国際標準は、…大きな矛盾や不整合はありません` — no
major contradiction), so this is a pure path-qualification miss of exactly the
class the wave repaired five of. Round-96 label row 3.

**F2 — MEDIUM-LOW — two PARTIAL cells cite `SKILL.md:182-184` for a correction
that completes on 185.**
Committed bytes: 184 ends `…(round-13 correction: earlier`; 185 begins
``text omitted `is_live(1)`) — exactly 1024…``. The cells (`triage:88` first part,
`triage:90`) assert the omission; their cited range stops one line short. Exact
fixes in round-96 label rows 1-2 (extend to `182-185`). This is inherited from the
round-94 label's evidence, which merged 184-185 into the 182-184 quote; the C1
meter cannot see it (it checks map/label tokens, not line truth). Round-96 labels
1-2.

**F3 — MEDIUM-LOW — crosswalk line 36 d)/e) minimum-element pointers are off by
one.**
The entry reads `d) information useful when submitting a possible vulnerability
report (L1832-1834), e) out-of-scope services (L1835), f) how submitted reports
are tracked (L1835)`. Committed S041: 1832-1833 = d), **1834 = e)**, **1835 = f)**
(`1832 d) Information that would be useful when submitting a`; `1833 possible
vulnerability report`; `1834 e) Out-of-scope services`; `1835 f) How submitted
reports are tracked`). d) overruns by one line and e) points at f). Pre-existing
(the landing changed only the path on line 34, not lines 36-37), but it lies
inside the range edited at line 34 and misleads a reader checking the six minimum
elements. Round-96 label rows 4-5.

**F4 — LOW — six plain-text table locations remain unqualified.**
`crosswalk.md:23-28` (the quoted-record table) writes `S041.txt:1868`,
`:1869-1870`, `:1916`, `:1813`, `:1856`, `:1851` without a path and without
backticks. All six are content-true (verified against the capture); because they
are plain text, `resolve.py` does not extract them as citations. Not labelled;
qualifying them with `corpus/source-snapshots/round-30/` would make the entry
uniform if it is next touched.

**F5 — LOW / residual risk — the entry now names two committed copies of S041.**
The front matter and the recheck command use `corpus/source-snapshots/round-26/S041.txt`;
the five new citations use round-30. Both are committed and byte-identical
(`e18acbf9…`); the round-30 manifest declares S041 self-contained (its
`archival_note` says "fetch instant not recorded", while the round-26 capture
receipt records 2026-10-25T12:34:17Z — the Limits sentence correctly points to the
round-26 log). Not a defect; worth a note so a future recheck does not treat the
two paths as different captures.

## Residual risk

- The two PARTIALs are one-line range shortfalls, not factual inversions; the
  cited lines still carry the corrected expression and the correction's opening.
  If the lane's standard accepts a range that includes the correction's opening
  clause, rows 5-6 read CORRECT and the site result is 16/16; the byte split is
  stated above so the L1 can apply its standard.
- The C1 meter (`knowledge-meter.py`) and its predicate are another seat's limb;
  nothing here re-runs or re-scores it. The landed files are exactly base+map, so
  the meter's input at 53ec479 is the map-applied text.
- Round-96 text edits change lengths; a successor meter/label set must re-pin the
  map sha after landing, as round 95 did.
- The six plain table locations and the round-26/round-30 dual naming are
  human-facing only; neither moves a resolver count.

## Verification gaps

- `[lost-base]` tokens: `schema.json:6` (row 2) and `fleet-dispatch.mjs:10/11`
  (rows 4, 11) cannot be checked on this host. A full-object history search
  (`git rev-list --all --objects | grep -i fleet-dispatch`) finds no captured
  copy of either source in the lane repo; the lane's `[lost-base]` convention
  (QUALITY R1) covers them, so they are recorded, not verified, and nothing here
  falsifies them.
- The round-30 S041 copy has no fetch instant of its own; the instant is the
  round-26 capture's (same bytes). The entry's sentence names the round-26 log,
  so the sentence is true of the bytes.
- This seat did not re-run the C1 counter/controls (MutC1Counter, ExecC1Indep,
  CriticClaimsC1) or the C2 scanner/controls (ReviewC2Scanner, MutC2Counter,
  SentinelShapes, ExecC2Probe). No resume path exists in this wave, so the
  `resume_continuity_v1` check is not applicable.

## Round-96 label set

`ReviewC1Sites-receipts/round96-labels.tsv` — 5 rows, same 5-column schema as
`.ufo/waves/round-95/c1/labels.tsv`; each re-derived by the committed-byte checks
in `## Receipts`:

1. `triage-thresholds.md:88` — `SKILL.md:182-184` → `SKILL.md:182-185` (F2).
2. `triage-thresholds.md:90` — `SKILL.md:182-184,255-257` → `182-185,255-257` (F2).
3. `crosswalk.md:13` — `S041.txt:1680-1681` → `corpus/source-snapshots/round-30/S041.txt:1680-1681` (F1).
4. `crosswalk.md:36` — d) `(L1832-1834)` → `(L1832-1833)` (F3).
5. `crosswalk.md:36` — e) `(L1835)` → `(L1834)` (F3).

## Receipts

All under `.ufo/waves/round-95/w1/ReviewC1Sites-receipts/`; commands run from the
lane root, read-only on git/jj.

- `git show --stat --format='%H%n%s' 53ec479` — observed: 2 files changed,
  14 insertions(+), 14 deletions(-), only the two corpus files. rc 0.
  Receipt: `landing-and-capture.txt`, `pins.txt`.
- `sha256sum .ufo/waves/round-95/c1/{repair-map.tsv,labels.tsv,knowledge-meter.py}`
  — observed: `8545eba2…`, `cf739497…`, `c0799f4c…` (match the frozen pins). rc 0.
  Receipt: `pins.txt`.
- `python3 site-check.py` — observed: `map_rows=16 cols_set=[4]`,
  `exact_sites=16/16`. rc 0. Receipt: `site-check.txt`.
- `python3 reconstruct.py` — observed: `rows_applied=16 files_exact=2/2`,
  both files EXACT against the landing. rc 0. Receipt: `reconstruct.txt`.
- `git show 53ec479:SKILL.md` piped through `awk` for 182-186 — observed: 184
  ends `(round-13 correction: earlier`; 185 begins `text omitted `` `is_live(1)`
  ``)`; lengths 75/69/72/74/71. rc 0. Receipt: `anchors-wrap.txt`.
- `git show 53ec479:SKILL.md` piped through `awk` for 254-257 — observed:
  255-257 completes the five-term + curated-boolean correction. rc 0.
  Receipt: `anchors-wrap.txt`.
- `git show 53ec479:SKILL.md` piped through `awk` at 999 — observed: the
  program-record schema bullet. rc 0. Receipt: `anchors-skill.txt`.
- `git show 53ec479:SKILL.md` piped through `awk` for 335-338 — observed: the
  gitMutationBlocker fail-closed rule. rc 0. Receipt: `anchors-skill.txt`.
- `git show 53ec479:corpus/knowledge/mission-control.md` piped through `awk` for
  19-27 — observed: 23-27 = the dead-`ev_note` correction. rc 0.
  Receipt: `anchors-wrap.txt`.
- counts loop: `git show 53ec479:SKILL.md | grep -cF <term>` — observed:
  `EV ordering=0`, `curated-EV=0`, `official_url=0`, `source_kind=1`,
  `five-termed=1`, `reward.min×1000=2`; zero-count greps rc 1 by design.
  Receipt: `skill-historical.txt`.
- `git show 7483333^:SKILL.md` piped through `awk` for 113-114, 175-176 —
  observed: 114 `…> reward.min×1000` (buildQueue), 176
  `curated-EV(1e12) > reward.min`. rc 0. Receipt: `skill-historical.txt`.
- `git log --oneline -S'reward.min' -- SKILL.md` — observed: round-13
  `7483333` rewrote it (plus round-11 `fb9ac8e`). rc 0.
  Receipt: `skill-historical.txt`.
- `git show 53ec479:…/round-30/S041.txt` piped through `awk` for 1680-1681,
  1810-1815, 1832-1836, 1849-1852, 1854-1857, 1866-1871, 1912-1917, 1790-1795,
  1865-1868, 1995-1999, 2076-2081 — observed: every cited line quoted in
  `## The sixteen rows`. rc 0. Receipt: `s041-anchors.txt`.
- `python3 backtick-scan.py` — observed: 8 backticked S041 spans at landing,
  7 path-qualified, **1 bare** (line 13); 6 plain-text locations (lines 23-28).
  rc 0. Receipt: `s041-backtick-scan.txt`.
- scratch fixture + `python3 corpus/instruments/resolve.py <fixture>` —
  observed: `S041.txt:1680-1681 GONE`; the qualified path `INTERNAL`, 2354
  lines, `in range`. rc 0. Receipt: `resolver-s041.txt`.
- `git cat-file -p 53ec479:…/round-{26,30}/S041.txt | sha256sum` — observed:
  both `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`. rc 0.
  Receipt: `landing-and-capture.txt`.
- `git show 53ec479:…/round-30/manifest.json` (S041 entry) — observed:
  `S041.txt pre-round-32 capture; fetch instant not recorded`, same sha. rc 0.
  Receipt: `landing-and-capture.txt`.
- `grep -n 'utc=2026-10-25T12:34:17Z' .ufo/waves/round-26/wave1/ExecCaptureS041.md`
  — observed: line 17 records the fetch instant. rc 0.
  Receipt: `landing-and-capture.txt`.
- `git rev-list --all --objects | … | grep -i fleet-dispatch` — observed:
  empty (no captured source in lane history); grep rc 1.
  Receipt: `landing-and-capture.txt`, `skill-historical.txt`.
- `git rev-list --all --objects | … | grep -i bounty-map/schema` — observed:
  empty (no captured schema in lane history); grep rc 1.
  Receipt: `skill-historical.txt`.
- `python3` label re-derivation over the landing lines — observed: each
  round-96 label's `key` occurs exactly once on its cited landing line
  (`88`/`90`/`13`/`36`; `36` twice), all `OK`. rc 0.
  Receipt: `round96-label-checks.txt`.

Every command above returned rc 0 except the two history searches (empty, grep
rc 1) and the zero-count greps (`EV ordering`=0, `curated-EV`=0, `official_url`=0,
each grep rc 1 by design). `git status --porcelain` shows this seat's writes only
under the untracked `.ufo/waves/round-95/w1/` report/receipt paths; no tracked
file was modified by this seat.

No credential values are quoted anywhere in this report or the receipts.
