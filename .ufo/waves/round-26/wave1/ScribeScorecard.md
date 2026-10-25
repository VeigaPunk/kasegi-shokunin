# ScribeScorecard — round 26 wave 1 (SCORECARD.md update)

- Seat: L1Kasegi26.ScribeScorecard (leaf scribe, SOLE OWNER of `SCORECARD.md` edits).
- Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Base revision `1b076fa7f2fb5e7dd9d87449514eba526043421b` (claims freeze commit).
- Report written: 2026-10-25 (UTC). No tools installed/updated (none needed; tooling directive record: none).

## 1. Behavior — what changed in SCORECARD.md

Sole owned file edited: `SCORECARD.md` (**+27 / -0**, per `git diff --stat`). Two appends, no historical section rewritten:

### (a) `## Planned` — r27 plan row supersedes executed r26 plans
Inserted after the historical "Round-22 planned for round 23" block (kept as history per house convention), lines 179–182:
- `**Round-26 planned for round 27** (supersedes the blocks above as the next plan; that text is kept as history). The round-26 plans were taken up as this round's frozen claims C1/C2 …` — marks the r26 plans executed, i.e. removed from planned status.
- Plan row 1, **depth:verifiability** (lowest non-retired, 4): continue instrument soundness on the routed debt named in round 25 (`anchorcheck.py` exit nonzero on unverifiable verdicts; `CITE` `~/Projects/bounties/` arm) — marked plan, not commit, no internal-citation credit.
- Plan row 2, **coverage** (7): continue the frontier from the open leads (`SOURCES.md` § Leads: ISO/IEC 29147/30111 standard records at iso.org), contingent on opening and clearing Q1–Q6, registering source rows first — marked plan, not commit.

### (b) New `## Round 26 — frozen claims C1/C2 (2026-10-25)` section (lines 567–578)
- **C1 depth:verifiability row** — evidence pointer set to `.ufo/waves/round-26/c1-receipt-index.txt`, last-change **26**, score **4 held** (gate conformance round; not a higher score). Before cell carries the frozen baseline from `claims.json` (registry row 0, selftest receipt lines 0, fix-control #3 hits excluding historical 1, deletion-fixture exit 0); After cell carries the claim targets.
- **C2 coverage row** — evidence pointer set to the F11 admission (`corpus/README.md` § Frontier), last-change **26**, score **7 held**. Sources-census state recorded as measured at scribe time (exit 1, findings listed), with round-end targets stated.
- **depth:density row** — no-harm guard: measured at scribe time (before the C1 registry-row edit to SKILL.md landed): mean 154.0, 652 path-citation instances, 19 blocks; `anchorcheck.py SKILL.md` `bad=0`, `LOST-RECORDED=306`, `PIN-BROKEN=0`, `OUTSIDE-BASE=0`, `BASE-ABSENT=0`, exit 0.

### (c) New `## Round-26 capabilities` section (lines 580–588)
- `source-capture-pdf` row — records the PDF capture path `capture-source.py --kind pdf` (pdftotext) as evidence, exercised on the round-26 S041 capture; evidence pointers: `corpus/instruments/capture-source.py` (`--kind pdf`), `corpus/source-snapshots/round-26/manifest.json` + `S041.txt` (sha256 `e18acbf9…`, 7 pinned quotes). First-working round 26 (flag predates, disclosed in-row).
- Saturation paragraph carried: "Planned round 27: see `## Planned` above."

## 2. Exact diff lines (git diff -- SCORECARD.md)

```
@@ -177,6 +177,10 @@ in the round-17 continuation below; source restoration remains operator-owned.
+**Round-26 planned for round 27** (supersedes the blocks above as the next plan; ...)
+1. **depth:verifiability** (lowest non-retired, 4) — ...
+2. **coverage** (7) — ...
+
@@ -559,3 +563,26 @@ C1 verifiability — make `anchorcheck.py` exit nonzero on unverifiable verdicts
+
+## Round 26 — frozen claims C1/C2 (2026-10-25)
+... (intro, table with C1/C2/density rows, capabilities table, saturation)
```
Full diff: 27 insertions, 0 deletions (verified `git diff --stat`). No other file written by this seat.

## 3. Exact counter commands used (all from lane root)

| # | Command | Output |
|---|---|---|
| 1 | `git diff --stat -- SCORECARD.md` | `SCORECARD.md \| 27 ++++++++++++++++++++`, 1 file changed |
| 2 | `git diff -- SCORECARD.md` | two hunks above (+27/-0) |
| 3 | `grep -n 'c1-receipt-index.txt' SCORECARD.md` | refs at new lines 180, 572, 576 (+ historical 524/557) |
| 4 | `grep -nE 'Round 26\|source-capture-pdf\|--kind pdf\|F11\|Round 27' SCORECARD.md` | all markers present (lines 180, 567, 577, 584) |
| 5 | `awk -F'\|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | **11** (F11 admitted; frozen before=10, target 11) |
| 6 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | **EXIT=1**; findings: W04 S028/S029 duplicate URL; E09 S040 `recheck=180d` URL/UA note; E09 S041 `recheck=180d` re-fetch w/ instrument UA (canonical anchor PDF); E11 S041 missing used-by `corpus/knowledge/iso-29147-and-30111-division-of-labour.md`; E11 S041 missing used-by `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` |
| 7 | `python3 corpus/instruments/density.py SKILL.md --label r26` | mean **154.0**, 652 path-citation instances, 19 blocks |
| 8 | `python3 corpus/instruments/anchorcheck.py SKILL.md` | `7 in-range/0 bad/7 distinct; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` |
| 9 | `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` | **1** (recheck-audit.py gate\|probe row at SKILL.md:981) |
| 10 | `grep -cE 'selftest cases=' .ufo/waves/round-26/c1-receipt-index.txt` | **1** (`selftest cases=14 failures=0 exit=0`, index line 4; `instrument_sha256=c3c19adc…` line 2) |
| 11 | `git status --porcelain` | SCORECARD.md modified; sibling artifacts present (see §5) |

## 4. Evidence pointers verified (read-only)

- `.ufo/waves/round-26/c1-receipt-index.txt` **exists** (created by ExecSkillRegistry during this wave): `instrument_sha256=c3c19adc…`, `selftest cases=14 failures=0 exit=0`, live audit `strict pass=37/37`, R25-2 crossreference note. C1 row pointer is real.
- `SKILL.md:981` carries the `recheck-audit.py | gate|probe` row (verdict map, `--selftest`, pinned path `c1-receipt-index.txt`, write scope, owner).
- `corpus/README.md` § Frontier now has **F11 admitted** (`ISO/IEC 29147/30111 division-of-labour meta | admitted | knowledge/iso-29147-and-30111-division-of-labour-2026-10-23.md, knowledge/iso-29147-divergence-and-clause-crosswalk-2026-10-23.md | S041`).
- `corpus/SOURCES.md:47` has S041 (JPCERT/CC 2026 P-guideline capture; canonical anchor PDF).
- `corpus/source-snapshots/round-26/` has `S041.txt` (2354 lines, PDF-extracted text incl. signature metadata) + `manifest.json` (S041 sha256 `e18acbf9…`, 7 pinned quotes) + `S040-live.txt`.
- **Not landed at scribe time:** the two F11 knowledge entries are not yet in live `corpus/knowledge/`; no corpus entry cites S041 yet (hence census E11, exit 1). These are sibling seats' remaining work; round-end targets are stated in the C2 row rather than asserted.

## 5. Concurrency / tool notes

- The `edit` tool initially rejected absolute-path edits to the lane SCORECARD.md, reporting the fleet-root `SCORECARD.md` hash (`#3ABA`; `/home/vgpnk/Projects/shokunin/SCORECARD.md` is the main-repo/protocol scorecard, outside my write scope). Re-issuing the same edits with the relative path `kasegi-shokunin/SCORECARD.md` applied cleanly (tags #3255 → #A6C9 → #870F → #8D24 → #D0DB). No fleet-root file was touched.
- Sibling work observed landing mid-scribe (read-only): F11 frontier row, S041 registry row/snapshot/manifest, `c1-receipt-index.txt`, `c1-controls/`, `c2-controls/`, SKILL.md registry-row edit (mtime 09:35). Density/anchorcheck were measured before the SKILL.md edit (disclosed in-row).
- No VCS writes performed (git only read-only: status/diff/log). No edits to `claims.json`, round-25 lessons, or round-25 receipts.

## 6. Out-of-scope

- Not touched: `corpus/README.md`, `corpus/SOURCES.md`, `SKILL.md`, `corpus/knowledge/*`, `claims.json`, `.ufo/waves/round-26/c1-receipt-index.txt`, any round-25 artifacts, fleet root, sibling lanes.
- Not run: C1 deletion-fixture and fix-control #3 counters (executor-owned); density/anchorcheck post-SKILL-edit re-run (final numbers belong to the round-end verification).
