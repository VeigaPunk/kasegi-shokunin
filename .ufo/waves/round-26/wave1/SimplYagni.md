# SimplYagni — YAGNI audit of wave-1 drafts (round 26, wave 1)

Seat: `L1Kasegi26.SimplYagni` (simplifier, read-only). UTC access date: 2026-10-25.
Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (base `1b076fa7`).
Outputs: this report + checklist `.ufo/waves/round-26/wave1/x1-yagni.txt`.
No production edits; no tools installed.

## What was scanned
All wave-1 drafts, scanned after they landed:
- `corpus/knowledge/iso-29147-and-30111-division-of-labour.md`, `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md`
- `corpus/lessons/round-26.md`
- `corpus/SOURCES.md` (S041 append + S040 recheck-cell update + Registry-changes note)
- `corpus/README.md` (F11 row + denominator) and `SCORECARD.md` (r26 result + r27 plans)
- `SKILL.md` (`## Gates & probes registry` row)
- `corpus/instruments/knowledge-expected.txt`
- `.ufo/waves/round-26/c1-receipt-index.txt`, `c1-instrument-digest.txt`, `c1-live.json`, controls, wave1 reports

## Findings (four categories; measured where stated)

### 1. Dead/stale referents (R) — 4 blockers
1. **README F11 entry cell cites staged-package filenames** (`knowledge/iso-29147-and-30111-division-of-labour-2026-10-23.md`, `knowledge/iso-29147-divergence-and-clause-crosswalk-2026-10-23.md`) that do not exist in the lane; the scribes created undated names per the spec. Measured: `frontier-recheck-count.py` exits 1 with `FileNotFoundError` (after both entries landed). The same dead names are repeated in the SCORECARD C2 row.
2. **SOURCES S040/S041 recheck cells carry prose after the cadence** (`180d — …`). Measured: `sources-census.sh validate` exits 1 with `E09` on both rows — the C2 kill-rule limb "census exit = 0 at round end" is unsatisfied at compose.
3. **knowledge-expected.txt is stale** (37 entries vs 39 in the tree). Measured with the landed instrument: default expected-list audit exits 1, `unexpected=2` (the two F11 entries). The committed list must be regenerated after the entries landed.
4. **c1-receipt-index.txt was written before the instrument change landed** (pins pre-change digest `c3c19adc…`, `selftest cases=14`; landed instrument `3fc0d751…`, 15 cases, selftest exit 0). C1(b) requires the receipt at the instrument's own digest — regenerate; the lesson already records this (M26-1).

### 2. Duplication (D) — no load-bearing duplicates worth deleting
- The two knowledge entries are near-minimal for their Q-bars; the shared capture fingerprint repeated across entries/lesson/scorecard/LOG is provenance, not padding.
- SCORECARD r27 planned rows restate round-25 planned text (anchorcheck debt) — acceptable carry-forward; optional to compress to a pointer.
- The receipt index has identical `instrument_sha256`/`base_sha256_control` lines today (they coincide only because the instrument was unchanged at write time) and bare `EXIT=0` lines without commands — cosmetic; tidy while regenerating (BL-4).
- Lesson Appendix repeats counters from Overview/Fixes — house format (R2), keep.

### 3. Placeholders / empty sections (P) — none found
Every scanned draft is non-empty and substantive. No stub tables, no "TBD", no empty blocks. The only "placeholder"-like text (SCORECARD r27 plan rows) is explicitly marked plan-not-commit and is allowed by the assignment.

### 4. Over-wide claims (W) — none found beyond the receipts
- The lesson's kill-rule status and counter table match independent measurements by this seat: C1 (a)=1, (b)=1 (line present; digest caveat above), (c)=0, (d)=exit 1; C2 awk=11, grep=3, census=1.
- The C2 frozen grep overmatches S040 (before=1, not 0) and counts shells — the lesson discloses this (M26-4) and does not overclaim.
- Entry quotes verified against captures: S041.txt lines 1667-1678/1868-1916 etc.; S039.txt:497-499 and S040.txt:58 spot-checked verbatim. No claim exceeds the quoted record.

### 5. Dead pattern reuse (R) — none
Drafts use lane ids (S041/S040) and current instruments (`source-recheck.py`, `recheck-audit.py`, `frontier-recheck-count.py`). Staged-package F19/F20 grounds and dated filenames were dropped in the entries (only documented in re-ground notes). No references to retired instruments.

## Suggestions (also in x1-yagni.txt)
1. README F11 entry cell → actual filenames (also SCORECARD C2 row). Keeps awk=11; harness recovers (entries=14 pass=14).
2. SOURCES: `180d` cadence-only cells; R25-5 URL/UA prose stays in `## Registry changes` note (add S041 line). Census → exit 0.
3. Regenerate knowledge-expected.txt via `git ls-files corpus/knowledge/*.md | sort` (39 entries). Live audit turns green.
4. Regenerate c1-receipt-index.txt / c1-instrument-digest.txt / c1-live.json at the landed digest with `selftest cases=15 failures=0` and a live 39-entry audit; keep the base-digest control.
5. (Optional) Add the F11 coverage-map row for pattern parity with F01–F10.

## Tradeoffs
- The expected-list gate makes the audit red on ANY list/tree drift (including legitimate additions) until the list is regenerated — that is the intended C1(d) leverage; the cost is a mandatory post-entry regeneration step each round (recorded by e2 as a risk).
- Moving the URL/UA note out of the recheck cell keeps the census grammar while preserving the R25-5 record in the Registry-changes note; the note is not machine-checked, so the record moves to documentation authority.
- Fixing the F11 row names only changes referents, not counts; it unblocks the frontier harness, which is the substantive per-entry check.

## Evidence (measured this seat)
- `grep -cE '^\| [^|]+\| gate\|probe ' SKILL.md` → 1
- `grep -cE 'selftest cases=' .ufo/waves/round-26/c1-receipt-index.txt` → 1 (line present; index digest stale vs `sha256sum corpus/instruments/recheck-audit.py` = `3fc0d751…`)
- restated fix-control grep (excluding round-24.md:77) → 0
- `python3 corpus/instruments/recheck-audit.py --selftest` → exit 0, 15 cases
- `python3 corpus/instruments/recheck-audit.py --json …` (default expect) → exit 1, `unexpected` = both F11 entries
- `python3 corpus/instruments/frontier-recheck-count.py` → exit 1, FileNotFoundError on staged name
- `sources-census.sh validate --root … kasegi` → exit 1, E09 S040 + E09 S041 (E11 cleared once entries landed)
- `awk … corpus/README.md` → 11; `grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md | wc -l` → 3
