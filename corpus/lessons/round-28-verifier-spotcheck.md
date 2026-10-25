# Round-28 verifier spot-check — kasegi

author: hyaku closure (non-author integrator, @m_kfc)

Fresh non-author closure judge for lane-round kasegi 28. Report:
`.ufo/reports/round-28/kasegi.md`; lane HEAD before `261a6651b7e52c58e9ad0ceaef6f3bd0bf2d904f`,
after `32f694b38e02b3dccbc696ba7ea1e52a928101cf`.

## Conformance (step 1)

- Report committed by lane identity: `git log --format='%an %H' -- .ufo/reports/round-28/kasegi.md`
  → `kasegi-shokunin 361c31bdbb0908c78165696d159a98f3af327987 round-28: kasegi report`. OK.
- Report carries `## SHONEN` heading with one line per box (4 `[~]` lines, each with a resolvable
  pointer). OK.
- Cited lane commits exist and are ancestors of the branch ref `master` (jj-colocated repo, git HEAD
  detached — tested against the branch ref, never `@{u}`):
  `261a6651…`, `32f694b38…`, `1265fe111…`, `c9f8b115…`, `94f387cb…` → all `ANCESTOR-ok`. OK.
- Lane pushed and clean: `jj-lane.sh state` → `local=32f694b38… remote=32f694b38… ahead=0 behind=0`
  (tracked=0 untracked=0); `git status --porcelain` empty. OK.
- Prompt carries the template contract (round-level items + five child-lane items: report path/name,
  commit-before-report, SHONEN heading, commit-hash citation, write scope). OK.
- Report is a real report (named work, committed hashes, evidence pointers), not a marker. Status `ok`.

## Claims re-check (step 2)

All plain measurements over committed bytes; gate/self-test evidence verified as committed evidence
(self-test tally, frozen-run verdict, revision measured), not re-executed.

**C1 — depth:verifiability (score held 4).**
- Before, at freeze commit `c9f8b115…` (re-derived from committed bytes): `anchorcheck.py` sha256
  `c2a9e6c6…ef748` (matches report); no `selftest` string in the file (0 hits); SOURCES rows 41;
  frontier admitted 11; S042 rows 0; knowledge files citing `source: S042` 0.
- After, at `32f694b38…`: instrument sha256 `23818c1204c38ee8d1bb0c6d449dd0ffb3c9181271f14fb3d7aab25a73ee7396`
  (recomputed via `git show 32f694b38…:corpus/instruments/anchorcheck.py | sha256sum` → matches report
  and `c1-receipt-index.txt`). Committed receipt `c1-receipt-index.txt` records: bad-fixture exit=1;
  BOUNTIES-ABSENT lines=1; `selftest cases=9 failures=0` exit 0; SKILL.md exit 0, bad=0,
  LOST-RECORDED=306. `post-commit-recheck.txt` re-confirms all four at revision `1265fe111…`.
- Gate evidence verified: self-test tally (9 cases, 0 failures, receipt line) and frozen-run verdict at
  the measured revision (receipt pins instrument sha256; my recomputed hash matches). `GIT_DIR`
  isolation defect (M28-13) has recorded before/after reproduction in erratum 2. Do-nothing control
  receipts committed under `.ufo/waves/round-28/c1-controls/` (bad-fixture-before, bounties-fixture-
  before, selftest-before, skill-before, instrument-digest-before).
- Erratum 1/3 correctly scoped the false `corpus_disclosure` prediction: four provenance trailers are
  unbackticked, `TOK` is backtick-only; sweep of backticked anchored bounties tokens over the
  Markdown input surface → 0 (I re-checked `grep -c` of S043+ rows and F20 → 0). No verdict-class
  movement.
- Verdict: **improved** (depth:verifiability), measured + evidence-verified.

**C2 — coverage (score held 7).**
- Before (c9f8b115…): frontier admitted 11, entries citing S042 0, registry 41 rows, harness 14/14.
- After (32f694b38…): frontier admitted 12 (`awk` over `corpus/README.md` → 12); entries citing S042 1
  (`japanese-domestic-disclosure-workflow.md`); S042 rows 1; census exit 0 (W04 S028/S029 only);
  harness `entries=15 pass=15 exit=0` (committed run). I re-derived all of these directly from
  committed bytes.
- Capture pins: S041 sha256 `e18acbf9…` and S042 `b432ec1656…` match the committed captures; S041
  round-28 capture is byte-identical to the committed round-26 capture (`cmp` → IDENTICAL). Manifest
  has 12 quote assertions (6+6), all `occurrences=1`, path stems match ids — verified by my own
  script over committed bytes. S042 Q1 quote (「JPCERT/CC は…連絡します。」) found verbatim at
  `S042.txt:145`, exactly once, 2 whitespace-words (≤25). S042 row: tier A, mined, opened
  2026-10-25, used-by exactly the F12 entry; S041 used-by old→new logged.
- Verdict: **improved** (coverage), measured.

No owned axis harmed: `git diff 261a6651… 32f694b38… -- SCORECARD.md` is append-only (143 added
lines; scores held: depth 4, coverage 7, density 9); SKILL.md no-harm run exit 0/bad=0/LOST=306
unchanged; density 150.3→160.2 disclosed as measurement change, not claimed.

## Discernment spot-check (step 3)

From `corpus/lessons/round-28.md` §Gate. Sample: 1 admit (S042/F12), 2 rejects.

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S042 + F12 entry | admit | `corpus/source-snapshots/round-28/S042.txt` (sha256 pin verified; URL `https://www.ipa.go.jp/security/todokede/vuln/process.html`); manifest quote assertions all exactly-once; Q1 located at L145 | agree | source opens and is verifiably captured; row is tier A/mined with used-by exactly the admitted entry; quote is inline, located, ≤25 words; entry recheck resolves both ids |
| `chinese-criminal-thresholds-and-authorisation.md` | reject (re-confirmed) | staged package `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/chinese-criminal-thresholds-and-authorisation.md` (file exists; quote at lines 47–48 present verbatim) | agree | sources S044/S045/S046 are not lane registry rows (lane registry ends at S042: grep for S04[3-9] rows → 0); `ground: F12` is package F-space, not lane F12; no located quote/capture anchors; recheck is prose — refusal sound |
| `vendor-third-party-finding-coordination-2026-10-23.md` | reject (new) | staged package same dir (file exists; `ground: F20` at line 7 verbatim; "MSVR learns …" at line 16) | agree | F20 absent from lane README (grep `| F20 ` → 0); source S080 not a lane row; claim restated with no located quote — refusal sound |

Both rejects are grounded in measured, re-openable facts; the admit is pinned and re-verifiable.
No disagreement.

## Trend verdicts

- **expansion — improved**: F12 admitted on ground absent from F01–F11, sourced by mined S042 (new
  A-tier row) + S041; registry 41→42; frontier advanced F12.
- **quality — improved**: anchorcheck fail-closed + nine selftest cases incl. the reproduced `GIT_DIR`
  isolation fix; F12 re-grounded on pinned captures with 12 exactly-once quote assertions; expected-list
  debt closed (40/42, audit exit 0).
- **discernment — improved**: the outside non-author spot-check (this file) agrees with the gate's
  admit and rejects; the round's own report graded `unchanged` because the outside check was owed —
  it now lands and agrees, so the calibration evidence is positive.

## Routed defects for round 29

1. **M28-3**: frozen C1 counter (d)'s `sed` limb for `bad=` is malformed — fix the counter or
   append a claims correction; a frozen counter whose command cannot emit its value is not a
   reproducible measurement.
2. **M28-1**: PRE-STATE receipts (seven) — dispatch counters after their subject lands.
3. **M28-6**: SKILL.md R6 row append shifted line numbers (1032→1035) and left a stale
   `resolve-dispatch-fixtures.json:159,161` pointer to `SKILL.md:1000` — decide R6 carve-out and
   re-anchor.
4. **M28-8**: C2 Q9 stem check is not instrumented (hand-run receipts) — promote `check_q9.py`.
5. **M28-5**: `frontier-recheck-count.py` crashes on an absent entry — fail with a named row.
6. **M28-12**: receipt digests drifted behind bytes (e.g. `ScribeReadmeC2` 243 vs landed 245 lines)
   — re-hash production files immediately before commit.
