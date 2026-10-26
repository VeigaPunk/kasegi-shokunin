# ScribeFrontierAmendments — round 37: the F20 frontier amendment blocks (PROVINCE.md + corpus/README.md)

Seat: `ScribeFrontierAmendments` (leaf, scribe; axis coverage). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(read-only for this seat except this receipt and `/fast/scratch/hyaku/kasegi-r37/ScribeFrontierAmendments/`).
Item: draft the two F20 (SSVC, source S054) frontier amendment blocks in the files' existing append-only style.
No lane, fleet, sibling-lane or source-tree file was written; no mutating git command was run.

## 1. State read (provenance of the draft)

| object | value |
|---|---|
| lane HEAD (`git rev-parse HEAD`) | `b362068195d5489aa94b31e6ec8f880c367e0ba0` |
| `PROVINCE.md` blob / file sha256 | `b6b6364556c656fd30d73c1796687715c29f8004` / `b0e91a611feadeeae38df7fd7fa55d8efe56039721cc35a024ca8af81108b5a9` |
| `corpus/README.md` blob / file sha256 | `18c09ce102cdb1e57be7c9adcaba1d53ac17706b` / `55c41374c101924170fb7d2e571ace348929292cba5a787315395b70177e0dca` |
| sizes at this head | `PROVINCE.md` 78 lines; `corpus/README.md` 398 lines; README ends `...stays outside it.\n\n` |
| working tree | clean except untracked `.ufo/waves/round-37/…` (`assimilation/`, `wave1/`, `wave1.ready*`, `wave1-*.err`) |
| style base | PROVINCE F18/F19 lines (77-78, `[r36 Frontier amendment, …]`); README round-35 section (370-398): `## Round-35 admission — coverage map row and Frontier F18`, two-column coverage-map table, six-column frontier table with the F18 row and the F19 row appended at 389, `[r35 amendment … 18/18 admitted]` at 391 |

Observed state gaps the round-37 block has to carry (measured, not changed):

- `grep -c '^## Round-36' corpus/README.md` → `0`; `grep -c '19/19' corpus/README.md` → `0`. Round 36
  appended the F19 row to the round-35 table but filed no round-36 section and no count line, so README's
  last count line still says 18/18. F19's round-36 admission is recorded outside README at
  `corpus/lessons/round-36.md:9` ("Frontier F19 … admitted 18→19") and `LOG.md:1661`; the frozen claim's
  mapping (`F19 r36`) and those records are why the r37 count line below names F19 at round 36. No
  existing line is rewritten (R9); if a standalone round-36 count line is wanted it must be another
  appended line, not an edit.
- `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → `19` at this head; the frozen C2 counter target is
  `20`, so exactly one row has to be added.
- Capture, entry, registry row and expected-list sync have NOT landed at this head
  (`corpus/knowledge/` has no `*ssvc*`; `corpus/source-snapshots/round-37/` absent; `SOURCES.md` has no
  S054 row). The block is a draft to append in the same integration state as those artifacts.
- Source basis measured by other seats (this seat made no network fetch and no re-measurement of their
  pins): `claims-erratum-1.md` — the C2 capture URL is corrected from the docs home
  `https://certcc.github.io/SSVC/` to the overview tutorial
  `https://certcc.github.io/SSVC/tutorials/ssvc_overview/`; `wave1/ExecC2QuoteOnce.md` — four
  ≤25-word quote pins on the overview snapshot sha256 `ff3f3b2c…fdce21` (518 lines, fetched
  2026-10-26T17:02:11Z), anchors L247 (severity/exploitability contrast), L259 (priority varies among
  stakeholders), L277 (decision-point series; page typo `decisions point values` quoted verbatim), L367
  (Exposure, per-system), §5: `Carnegie`/`Mellon` footer-only L505-L507, `CERT/CC` in body prose, `CVSS`
  6 / `EPSS` 5 / `KEV` 1 occurrences all in site navigation, `severity` and `exploitability` one
  occurrence each and undefined; `wave1/ExecManifestChecks.md` — capture-binding rules A/B5/C and the
  S054 record shape (`fetched_utc` strict UTC; one exact URL literal shared with the registry row).

## 2. Deliverable A — `PROVINCE.md` end-of-file block

Append verbatim (the leading blank line is part of the block; lines 1-78 stay byte-identical):

```text

[r37 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F20 — SSVC (Stakeholder-Specific Vulnerability Categorization) decision-point-based prioritization — admitted round 37; entry `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` (source S054)
```

| property | value |
|---|---|
| sha256 (block bytes) | `cdfe44e319094957ec583b7c3cd8212b882752b75682d9f1cf4d0b734f20f545` |
| bytes / lines | 295 / 2 |
| placement | after line 78 (`…(source S053)` + newline); result 80 lines |
| source of the F20 sentence | the round-37 frozen claim C2 wording (SSVC — Stakeholder-Specific Vulnerability Categorization, decision-point-based prioritization) and the item's mandated line text |

## 3. Deliverable B — `corpus/README.md` end-of-file block

Append verbatim at EOF. The file currently ends with a blank line (`...stays outside it.\n\n`), so the
block starts directly with `##` (no extra leading newline: the boundary stays a single blank line) and
ends with the file's terminal blank line. Lines 1-398 stay byte-identical; the result is 425 lines.

```text
## Round-37 admission — coverage map row and Frontier F20 (appended 2026-10-26)

The coverage map above is not edited in place (R6): the round-37 entry
`knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` (Frontier F20, source S054;
source basis: CERT/CC's SSVC "What is SSVC?" overview tutorial at
https://certcc.github.io/SSVC/tutorials/ssvc_overview/ — the overview page, not the docs home, per
`claims-erratum-1.md` and capture-binding rule B5 — captured 2026-10-26, status 200, under
`corpus/source-snapshots/round-37/`) is recorded here as an appended amendment so every existing
line keeps its number. The coverage-map row is appended here rather than inserted into the map, and
the F20 frontier row is listed here on the same table shape as the frontier above.

| Area | Entry | Source basis |
|---|---|---|
| Stakeholder-specific vulnerability categorization (round 37) | knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md | S054 — public primary, opened 2026-10-26 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F20 | SSVC (Stakeholder-Specific Vulnerability Categorization) — stakeholder-tailored, decision-point-based prioritization | admitted | knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md | S054 | Read a priority from one stakeholder's decision model, not a universal score: "A decision point itself is not representative of risk, but the series of decisions point values help a stakeholder determine how risky a vulnerability is" (S054.txt:277; the page's own typo "decisions point values" is quoted verbatim), and the inputs are per-system — Exposure asks how difficult it is for an attacker to access a system from the open Internet (S054.txt:367). Keep it distinct from CVSS severity, KEV status and EPSS likelihood: SSVC categorizes "by priority based on risk that varies among stakeholders" (S054.txt:259), and the page contrasts itself with systems that "rate on technical severity" (S054.txt:247) while naming no CVSS metric and defining neither severity nor exploitability in prose — CVSS, EPSS and KEV appear only in site navigation, so source those definitions from S001/S002, S052 and S053. Read "Carnegie Mellon" only as the site footer's owner statement, not as a methodology claim. |

[r37 amendment, appended 2026-10-26] The parenthetical above records the round-26 frontier state
and each later amendment paragraph states its own round; those are retained as history, not
rewritten (R9): at round 37 the frontier stands at **20/20 admitted** — F01-F08 at round 23, F09
at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30,
F15 at round 31, F16 at round 33, F17 at round 34, F18 at round 35, F19 at round 36, F20 at
round 37. The 0/18 sentence is untouched: the lost-domain denominator still holds 0 of 18
surfaces present, and the frontier count stays outside it.

```

| property | value |
|---|---|
| sha256 (block bytes) | `2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b` |
| bytes / lines | 2947 / 27 |
| row shape | six cells (id, topic, status, entry, sources, next), topic names SSVC as stakeholder-tailored decision-point prioritization, entry path `knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`, source `S054` |
| count line | `[r37 amendment, appended 2026-10-26]` naming `20/20 admitted` and F01-F08 r23, F09 r24, F10 r25, F11 r26, F12 r28, F13 r29, F14 r30, F15 r31, F16 r33, F17 r34, F18 r35, F19 r36, F20 r37; the 0/18 sentence is declared untouched |
| URL choice | overview tutorial page per `claims-erratum-1.md`; the paragraph says so and why (capture-binding B5) |

## 4. Validation on a scratch mirror (append, not edit)

Fixture: `git archive HEAD PROVINCE.md corpus` exported into
`/fast/scratch/hyaku/kasegi-r37/ScribeFrontierAmendments/mirror`, both blocks appended with Python to the
copies only. Measured on that mirror:

| check | command | observed |
|---|---|---|
| pure addition (PROVINCE) | `diff orig PROVINCE.md \| grep -c '^<'` | `0` (2 added lines) |
| pure addition (README) | `diff orig corpus/README.md \| grep -c '^<'` | `0` (27 added lines) |
| frontier row count | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `20` (target `20`) |
| row cells | pipe-split of the F20 line | 6 cells; next cell 155 words |
| section header | `grep -c '^## Round-37 admission' corpus/README.md` | `1` |
| count line | `grep -c 'frontier stands at \*\*20/20 admitted\*\*' corpus/README.md` | `1` |
| PROVINCE line | `grep -c '^\[r37 Frontier amendment' PROVINCE.md` | `1` |
| sizes | `wc -l` on the mirror | `PROVINCE.md` 80, `corpus/README.md` 425 |

Harness on the same mirror (`HYAKU_SCRATCH=<scratch> python3 corpus/instruments/frontier-recheck-count.py
--root <mirror>`, tail):

```text
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0
FAIL     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=-              exit=-    problems=missing-entry
entries=23 pass=22 exit=1
```

Reading, not over-claiming: the appended row is parsed and counted as the 23rd entry record (the frozen
`entries=23` target), and all 22 pre-existing entries still PASS, so the append perturbs nothing. The run
is red only through the harness's designed fail-closed `missing-entry` limb (docstring rule E) because the
entry file does not exist at this head; it is the row that the pending entry will bind when the C2
artifacts land. This receipt does not claim a green `entries=23 pass=23` for a state that does not exist.

## 5. Integration cautions

1. **Line pins are snapshot-bound.** `S054.txt:247`, `:259`, `:277`, `:367` in the README row are the
   ExecC2QuoteOnce anchors on the overview snapshot sha256 `ff3f3b2c…fdce21` (518 lines,
   fetched 2026-10-26T17:02:11Z). If the capture that lands has different bytes/line numbering, re-derive
   the three refs against the committed `S054.txt`; the quote texts are the stable part, the numbers are not.
2. **URL literal.** The paragraph's URL must equal the S054 registry row's single `https://` token and the
   manifest record's `url` byte-for-byte (capture-binding B4/B5). If integration lands the home page
   `https://certcc.github.io/SSVC/` instead, change the paragraph's URL and drop its "not the docs home"
   clause — but then the entry's load-bearing quotes have no capture basis (ExecC2QuoteOnce measured each
   of the four quotes 0 times on the home capture).
3. **Attribution stays narrow.** The row says `Carnegie Mellon` is only the site footer's owner statement
   because the methodology prose never claims authorship; `CERT/CC` is the body-prose publisher. Do not
   upgrade S054 into an authorship or endorsement claim.
4. **Vocabulary stays sourced elsewhere.** The row asserts S054 names no CVSS metric and defines neither
   severity nor exploitability (CVSS/EPSS/KEV occurrences are navigation only), so definitions for those
   systems belong to S001/S002, S052 and S053. Do not cite S054 for them.
5. **F19 count-line gap is recorded, not silently fixed.** The r37 line names F19 at round 36 from the
   r36 lesson/LOG and the frozen mapping while the r35 paragraph at line 391 keeps saying 18/18 (R9). An
   integrator wanting a standalone round-36 count line must append one; editing line 391 breaks the
   append-only discipline the C1 suite checks.
6. **Footer-only quote rule.** The row's longest quoted span is the 25-word Q3 sentence (the page's typo
   included). If the row's refs are re-derived, do not "fix" `decisions point values` — the capture
   contains the typo.
7. **Do not insert the row into the frontier table at line 201-219.** Every later admission in this file
   appends its own section/table at EOF so earlier line numbers hold (R6); the draft follows that.

## 6. Out of scope, tooling, cleanup

- Out of scope and untouched: entry file, capture `S054.txt`/`manifest.json`, S054 registry row,
  `knowledge-expected.txt`, harness/census/source-recheck instruments, LESSON/SCORECARD/LOG/SKILL.
- No mutating git command: `git rev-parse`, `git log`, `git show`, `git archive HEAD` (into scratch) only.
- No tool install or upgrade; no pacman; no network fetch by this seat. Interpreter `Python 3.14.8`;
  `git version 2.56.0` (both preinstalled).
- Scratch `/fast/scratch/hyaku/kasegi-r37/ScribeFrontierAmendments` (mirror + block files) removed after
  this receipt was written; the only retained artifact is this file at
  `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md`.
