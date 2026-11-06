# ReviewC2 — C2 F55 entry review (round 79, attempt 1)

Scope: `.ufo/waves/round-79/w1/c2/` draft (ScribeEntry) against S113 and the frozen C2 predicate B0–B7 in `.ufo/waves/round-79/claims.json`. Read-only. No lane file edited; scratch removed before yield.

## Verdict

- **Blockers (a frozen B-predicate or the kill rule fails): 0.**
- Major: 2. Minor: 2. Nit: 1.
- Draft bytes and the landed bytes in the lane tree are identical (see Landed-state note).

## Mechanical checks (evidence)

| Check | Result |
|---|---|
| B0: `source-recheck.py --manifest …round-79/manifest.json --source S113` | `S113:sha256 OK`, eight `OK occurrences=1 anchor=<n>-ok` lines (25, 41, 41, 55, 61, 62, 66, 85), rc0 |
| Quote placement: each of the 8 pinned quotes | byte-substring, exactly 1 occurrence, on its manifest anchor line; S113 sha256 `f4bce053…8ebf`, 127 lines (wc -l; 128 split fields), 5669 bytes |
| Every double-quoted span in the entry | all 8 pinned quotes plus the two S113 quotes in the Attribution lines are on-line; the one non-S113 span (entry L79) is F51's own sentence, byte-exact in `osv-post-v1-query-contract.md:75` |
| Gate word counts (`wc -w`) | 19, 18, 12, 22, 14, 7, 11, 14 — match the table exactly |
| Limits greps on S113 (six patterns) | all print nothing, rc1 |
| B1: SOURCES S113 row diff vs base | only status `queued`→`mined` and used-by `—`→path change (13 cells each); registry rows = 113 |
| B2: knowledge-expected | 95 lines, 93 `.md` rows, `LC_ALL=C sort -c` clean, set equals `corpus/knowledge/*.md`; git diff = one added line (`osv-determineversion-…md`) |
| B3 (scratch copy of landed tree): frontier census | `FRONTIER-CENSUS rows=55 admitted=55 closed=55 problem-rows=0 registry=113`, `FRONTIER-PASS F55 ids=S113` |
| B4: capture-binding-check (scratch copy) | `records=93 bound=93 unbound=0` |
| B5: recheck line | exactly the B0 command behind `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ` |
| B6 literal: 8 pinned quotes over `corpus/knowledge/*.md` excluding the new entry | 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 |
| README F55 row shape | 6 cells, same 8-field split as F54 row |
| Not-claimed list | matches claims.json C2 (:37, :39, :64, sample values); F51 :31 does hold the case-sensitivity sentence (`S108.txt:53`), so the "held by F51" premise is true |
| Entry structure vs F54 (QUALITY) | same heading set (Attribution / Claims / Distinctness / Not claimed / Gate / Limits), same frontmatter keys |

Not run by me: B7 (`sources-census.sh validate`) — a fleet-root validator, left to the L1 post-landing.

## Findings

### 1. MAJOR — Claim 2 misstates S113.txt:41 (over-generalization)
- Location: entry L21 (`Membership in the identifiable list is a property of that project integration, not of the language the library is written in (S113.txt:41).`)
- Evidence: S113.txt:41 names the set as "the C/C++ projects integrated into the OSS-Fuzz project" — the language is a membership condition, not an irrelevant one. The sentence says the opposite.
- Fix: state that membership requires both the C/C++ language and OSS-Fuzz integration, as the page's single sentence does. Keep the Falsifiable rule (L23), which is correct.
- Kill-rule impact: none (mechanical predicates pass); this is a claim-beyond-quote defect.

### 2. MAJOR — Claim 7 grounds on an unpinned list the entry's own Limits disclaims
- Location: entry L61 (`…so the scope is the listed extensions and not the whole directory (S113.txt:66).` with `(the list at S113.txt:67-72)`) versus entry L117 (`the extension list itself (S113.txt:67-72) … this entry grounds no clause on them`).
- Evidence: the frozen manifest pins only Q09 (S113.txt:66) and frozen C2 says the eight pinned quotes are the only clause grounds. L61 uses the unpinned list as the scope ground; L117 says it grounds nothing on it. Self-contradiction.
- Fix: rewrite L61 to rest the scope on the quote text alone ("every file with the following extensions", S113.txt:66) and cite the list only as a location in Limits, or delete the parenthetical.

### 3. MINOR — Distinctness subject sweep is narrower than R114
- Location: entry L75–83. Only `grep -rli 'determineversion\|indexer'` is recorded (L82).
- Evidence: R114 requires the sweep by subject (OSV.dev / OSS-Fuzz) with a per-hit verdict. `grep -rli OSV corpus/knowledge/` returns 6 files (fuzzilli-js-engine-fuzzing-framework, github-advisory-database-curation-semantics, openssf-scorecard-checks, osv-affected-range-events, osv-post-batch-query-contract, osv-post-v1-query-contract). `grep -rli oss-fuzz corpus/knowledge/` returns project-zero-big-sleep-sqlite-variant-analysis.md:26 (OSS-Fuzz harness configuration, not the identifiable set). ScoutDistinct.md records the fuzz-form sweep (L119–135) but the entry records no per-hit verdict for these.
- Fix: add one Distinctness bullet with both greps and a verdict per hit (F51/F54/F31 already covered; the other three OSV files and the big-sleep hit need a verdict line).
- Not a B-predicate: B6 literal count is 0/8 and the per-clause paraphrase is recorded in the lesson (lesson L62).

### 4. MINOR — Unmarked inferences inside falsifiable rules
- L31: "because S113.txt:41 states that the database does not represent all C/C++ packages" — reasonable inference; label `[INFERENCE]` or phrase as the rule's reading.
- L55: "even though hex is how digest tooling commonly prints the same hash" — not on the page and not sourced. Remove or mark `[INFERENCE]`.
- L69: "its order is closeness rather than input position" — contrast inferred from "sorted by how close"; state as the reading, not as a page clause.

### 5. NIT — Clause labels collide with campaign claim IDs
- Gate table (L94–103) labels clauses `C1 purpose` … `C8 closeness order`. In this round C1 and C2 are the campaign's claim IDs (recheck census; F55). Rename to `cl1`–`cl8` or `clause 1`–`clause 8`.

## Checked and clean
- All eight pinned quotes: once each, on anchor line, B0 rc0.
- Limits greps print nothing; Not-claimed list equals claims.json C2.
- F51 :31 holds the case-sensitivity sentence (S108.txt:53) — the frozen note is accurate.
- F51 :11/:19/:29/:37/:45/:53/:75, F54 :11/:19/:27/:35/:43, F31 :21/:33 — cited lines match their claim headings.
- R119: round-79 lesson `## Gate` has explicit reject lines (lesson L30 block). R125: admitted entries inspected; per-clause held-ground recorded (lesson L62).

## Landed-state note
While reviewing, the lane tree already held the landed files: `corpus/knowledge/osv-determineversion-cc-library-versioning.md` (untracked), `corpus/README.md` (+14 lines), `corpus/SOURCES.md` (S113 row), `corpus/instruments/knowledge-expected.txt`, `PROVINCE.md` (+1 line). Diffed against the wave draft: entry, F55 README row, S113 row and knowledge-expected are byte-identical. My first B3 probe showed rows=56 with F55 duplicated only because I had inserted the row onto the already-landed README in my scratch copy; the re-run on an unmodified scratch copy of the landed corpus gives rows=55 PASS. The duplicate was my probe's, not a lane defect.

## Verification gaps
- B7 (`sources-census.sh validate`) not run; L1 post-landing.
- Findings 1–2 are text corrections; after fixing, rerun B0 and the Limits greps (they touch only the entry prose, not the quotes).

## Tooling
No tools installed or upgraded.
