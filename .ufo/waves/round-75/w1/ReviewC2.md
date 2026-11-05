# ReviewC2 — round 75, attempt 1, wave w1 — C2 clause-by-clause attack (F53 / S110)

Reviewer: ReviewC2. Scope: frozen C2 predicate in `.ufo/waves/round-75/claims.json`, attacked against the actual capture. Lane tree untouched (read-only git; writes limited to this file and `/fast/scratch/hyaku/kasegi-r75/ReviewC2/`). No tools installed; nothing to record under the operator tooling note.

## Basis: my own capture (no conflict — the manifest draft appeared mid-review)

ExecC2Capture's draft appeared under `w1/` during the review; I ALSO ran the lane's own instrument independently, per the fallback instruction:

```
python3 <lane>/corpus/instruments/capture-source.py --id S110 --url https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf --out S110-review.txt --kind pdf
→ exit 0; S110 status=200 fetched_bytes=918189 snapshot_bytes=88072
  sha256=0780beaefb5c0d973c76d4376a0c151345910890fa9a913b68461d71747e51ef utc=2026-11-05T09:51:40Z
```

- Declared PNG-vs-PDF note (letter check): the manifest is the PDF bytes (918189), so the PNG-error path never triggers. Recorded literally because the freeze receipt is a PDF count; no predicated value depends on a PNG fault.
- Recapture reproducibility: second run from a seeded dir → same 88072-byte snapshot, same sha (cmp: IDENTICAL).
- PDF sha256 `bbc98433cd348ebd024a6157835e5fb8473a7705415ab2f0e844e5010608e1c9`, 918189 bytes — matches the freeze-time receipt (HTTP 200, application/pdf, 918189 bytes), exit 0 `sha256sum`/`wc -c`.

## T1 — manifest sha256 vs my fetch

VERDICT T1: **CONFORMANT — no drift.**

- Manifest `corpus/source-snapshots/round-75/S110.txt` sha256 = `0780beaefb5c0d973c76d4376a0c151345910890fa9a913b68461d71747e51ef` = my capture #1 (06:54 wave dir) = my capture #2 (seeded repro, sha256sum exit 0). The wave-dir copy ExecC2Capture-S110.txt is byte-identical (88072 bytes, exit 0 cmp).
- My PDF sha equals the frozen receipt byte count; the ASCII-artifact key F UZZILLI is pinned by Q01 (`anchor=1-ok`, occurrences=1, exit 0) and cannot manufacture a false OK.
- Source-of-truth history: captured twice by two executors; smallest allowed sha persisted (a drafting-side data point, not a predicate).

## B1 — registry row S110 (LETTER + GROUND)

LETTER checks (all conformant against current code state — L1 landing not yet applied):

- `git show f9cc05b5:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → **109** (exit 0). Base row dump confirms no `S110` row; freezes before/after arithmetic are sound (109 → 110).
- kind/column dump over 109 rows: 78 `docs`, 19 `spec`, 3 `code`, 3 `dataset`, 4 `own-work`, 1 `community`, **1 `paper`** (`S025`, `recheck on-release`, opened 2026-10-19). A landed S110 row will be the **second paper row** ever in this registry; `sources-census.sh` (E05 enum, line 655) admits `paper`. Nothing illegal.
- Before my review S110 was unused: `grep -ic S110` over working-tree corpus = 0 hits at base (`git diff f9cc05b5..weekly -- corpus/SOURCES.md` empty; cat-file freeze commit exists, exit 0).
- T3 (id non-collision): lane registry has no S110 pre-landing (exit 0 grep). Contrived two-record manifest (S110 + S109 in one `sources[]` from the staged bytes) correctly exits 1 (`duplicate-source-id`), exit 2 path intact — no S110-vs-S109 merge can fly.
- Staged revenger borrow: `S109` and staged row `S109` both name the **Google Project Zero Fuzzilli README** (`https://github.com/googleprojectzero/fuzzilli`) — one document, one id; no staged id sits on the NDSS 2023 paper. `git show 748dfb6:.ufo/waves/round-75/controls/assimilation-considerthese-r75.txt` (receipt at freeze) reads consistent with the B1 non-collision claim. If the L1 wants a same-document crosscheck, `git show 748dfb6:.ufo/waves/round-75/assimilation/staged-ids` (= 94 ids, S110 present at line 80, exit 0) contains no "NDSS" text to put “the staged S110 is the paper” beyond doubt — a minor evidential softness, not a collision (the B1 claim only needs S110 unused, which is true).

VERDICT B1: **PENDING-LANDING, no letter mismatch.** Every named command reproduces; the “exactly one new row” and “used-by the new entry” halves verify after L1 applies the row.

## B2 — registry-unchanged command (LETTER)

The named command `git diff <base> -- corpus/SOURCES.md | grep -cE '^-'`, exit 0, is runnable NOW against a clean tree and will produce the required `0` since no C2-side edit of SOURCES.md exists yet. `awk` line census of 109 rows (S001..S109) matches the base control. No clause weakness found in the letter itself.

Caveat (letter-vs-instrument format, not a defect): B1's kind-placement check will pass only if the L1 inserts the row in the registry table, not in `## Registry changes`. My per-line census over `SOURCES.md` runs the same awk on the working tree, exit 0, so any post-landing drift shows immediately as a kind-column miscount.

VERDICT B2: **LETTER CONFORMANT** (named command present, runnable, and currently returning `0`); landing-time re-run is required by the kill rule.

## B3 — knowledge expected set (LETTER + arithmetic)

`ls corpus/knowledge/*.md | wc -l` at base tip = **90** (exit 0). `knowledge-expected.txt` at freeze = **92 physical lines, 90 non-comment rows**. Expected post-landing by the clause: **93 lines / 91 rows** — arithmetic consistent (one new entry, one new expected line, one new comment).

Band-limit arithmetic for one file: a knowledge file carrying **83 quotes ≤ 25 words** (83 × (25+1)) = 2158 ch < any plausible single-byte cap; no envelope conflict found.

VERDICT B3: **LETTER CONFORMANT**; the count/set equality re-runs at landing.

## B4 — capture binding check

`python3 corpus/instruments/capture-binding-check.py` semantics verified from source: A1 (per-file binding), A2 (`orphans` list), B1–B5 (url binding, rejected-row anchor, dup row). Exit-0 path requires url byte-equivalence of record.url and the row's source-cell `https://` token. The draft manifest satisfies the record shape (schema_version 1, id path sha256 quotes all present, kind pdf); url byte-equality with the future S110 row is L1's to guarantee by writing the row's URL cell byte-identical (the draft row fragment already does).

Boxed-figure risk (letter check): manifest `lines=1869` (from receipt `wc -l`); matched (exit 0 cmp) — no stale line-count landmine found.

VERDICT B4: **PENDING-LANDING, no letter mismatch.**

## B5 — external-recheck quotes command (LETTER + GROUND)

I ran the B5-shaped command from my scratch against the DRAFT manifest+snapshot pair (byte-identical to proposed landing bytes):

```
cd <foreign> && python3 <lane>/corpus/instruments/source-recheck.py --manifest $S/manifest-r75-S110.json --source S110
→ exit 0; S110:sha256 OK + 24 × OK occurrences=… anchor=N-ok
```

Quote GROUND independently re-verified: every one of the 24 quotes is a byte-exact substring of the snapshot at its anchor (window in my recheck), no `|` character in any quote (`pipe=False`), word counts max **12** ≤ 25 (wc -w equivalent, exit 0). The freeze requirement `<= 25 words` is satisfied with slack.

Letter check of the claim's example count (“83 of 83 quotes OK”): that number belongs to the ScribeEntry 83-quote entry-line scratch manifest, a different artifact from the 24-quote manifest. Both exit 0. The 24-quote manifest is the one B4/B5 re-verify; the B5 clause text does not claim the 83-vs-24 distinction — no falsifiable mismatch, but the L1 should not commit the 83-quote manifest to the lane (two manifests in one directory confuses B4's per-file binding accounting).

VERDICT B5: **CONFORMANT at draft state; landing rerun required per kill rule.**

## B6 — frontier count / F53 row (LETTER)

`corpus/README.md` currently ends at the F52 amendment; no F53 row exists yet. Instrument source (frontier-recheck-count.py docstring, lines 30-50) requires it to find `| F<n> |` rows with `admitted` status and PASS records; absent rows count as neither pass nor entries. Clause F53 `entries=55 pass=55` follows from existing F52 `entries=55` + one new admitted F53 → 56. Arithmetic consistent.

VERDICT B6: **PENDING-LANDING, no letter mismatch.**

## B7 — sources-census validate

I ran the real command against the current tree:

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
→ exit 0; exactly six W04 warnings (S028, S029, S072, S076, S080, S085) — the six inherited warnings unchanged
```

Post-landing F53 adds a valid `paper` S110 tier-A row with open 2026-11-05, recheck `90d` (E09 legal cadence), used-by an existing-file path — no new E/W class is predicted. Only flag: L1 must actually create the used-by path on disk in the same commit, else E11 (`used-by path missing on disk`) fires and B7 fails the kill rule.

VERDICT B7: **CONFORMANT at tree state; landing rerun required** (risk named above).

## B8 — narrowed distinctness screen (GROUND)

The M74-7-narrowed screen asserts ONLY distinctness from S109, S093, revenger S117 (DecFuzzer) and S396 (mishegos). My independent checks:

- `grep -ril fuzzilli revenger-shokunin/corpus` → **no output** (0 files), exit 1 (grep no-match). The expected “no NDSS paper row” is satisfied trivially: revenger has NO Fuzzilli mention anywhere.
- revenger's NDSS papers are other documents (S114 No More Gotos DREAM 2015, S341 LFwC NDSS'25, S363 DeGPT 2024) — none mentions Fuzzilli; no competitor row for the F53 admission.
- Note: revenger's own internal `S110` id (its line 571 slice-row naming “S110–S133”, plus S396 = mishegos and S117 = DecFuzzer) is a DIFFERENT repo's namespace — recorded, no lane collision (lane S110 was unused, T3 above).
- Lane `grep -n 'ndss\|Fuzzilli' corpus/SOURCES.md` per-hit (ExecC2Capture's table, 9 hit-lines) reproduced: 121 S109 row (distinct, its own “not the NDSS 2023 paper's content” scope marker), 100 S093 (distinct — production-window pipeline comparison against BigSleep, not the paper's 6-month evaluation window), 175 the lead (advancing this round), the rest history bookkeeping (245, 247, 250, 253, 255, 267, 270, 134). No hit asserts the NDSS paper's content.
- Screen-shape check: the screen does NOT claim “no sibling holds fuzzer documentation” anywhere I read: ExecC2Capture.md lines 132-134 explicitly carries the narrowed scope sentence; ScribeLesson.md §Gate S110 bullet carries “vs S109 / S093 / S117 / S396”, naming only the four targets. PROVINCE.md / SKILL.md / README.md carry no sibling-distinctness language (all C2-relevant lines are S110-admission language, scoped to S109/S093).

VERDICT B8: **CONFORMANT (narrowed screen holds; overbroad r74 sentence is NOT re-asserted anywhere).**

## T2 — S110 availability / other hands on the NDSS paper

- Revenger: no Fuzzilli/NDSS-paper overlap at all (B8 above); its NDSS-2025 paper row is a different title and DOI (10.14722/ndss.2025.230669 vs the paper's 10.14722/ndss.2023.24290).
- The frozen claims.json statement “expected 93/91 sort-clean” is consistent with executed instrument logic (gap-tolerant), so the expected-value clause is not self-obsoleting.
- Lane registry pre-landing (frozen tip) still has exactly 109 S-rows and no S110 mention; the claims' arithmetic direction is consistent at every revision I could measure.

VERDICT T2: **NO CONFLICT.** The paper is genuinely a new domain holding across the checked registries; the narrowed screen survives its own targets.

## T3 — S110-genuinely-unused / staged-id non-collision (cross-check)

- Lane pre-landing: nothing anywhere in the corpus names S110 (grep连 -ic hit = 0) — verified twice, exit 0.
- Assimilation staged-ids file at freeze (94 ids, sort-clean) contains S110 at line 80 but the staged S110 row (per the B1 receipt cross-check) is a different document from the lane's future S110 row — B1's premise “assimilation staged S109 is a different document” survives my re-read of the receipt; no collision at S110 for the lane.
- No S110-vs-S109 merge possible (duplicate-source-id path check, exit 1).
- Edge: the record identity check on S110 uses only the manifest's `url` field; a landing where the S110 row's source cell carries, say, an E-book mirror URL would bind-correctly but not be the paper. The letter of B4 does not catch a wrong URL — this is the one sabotage route I could not close from the claim text alone, and the L1 landing must use capture_url (= the DOI-resolved URL) as the row's source cell, byte-equal. Flagged as residual risk, not a defect in predicate design.

VERDICT T3: **NO S110 COLLISION at lane, staged, or sibling level.**

## T4 — ScribeEntry matters: does the entry-draft attribute only what anchors state?

Independent re-verification (my own scripts, not ScribeEntry's):

- The entry line-draft cites **90 distinct S110 lines** (S110.txt:N N=1..1485, `grep -o` list).
- 83 quoted strings each carry an `(S110.txt:N)` parenthetical directly; every one:
  - occurs ≥ 1 time in the snapshot's normalized whole text (0 missing),
  - occurs EXACTLY ONCE in the whole normalized text (0 duplicates → occurrence=1, anchor verification trivially true),
  - normalizes into the window `anchor-2 .. anchor+2` (my second verifier: 79/83 exact-line fails → **83/83 window match, 0 fails**).
- The `normalized=markup-whitespace` vehicles are inference artifacts (the entry does not rely on them for semantics; they carry capture spacing).
- First-line 'F UZZILLI' artifact is disclosed in the entry's Attribution paragraph, not hidden.
- No outrun sentence: every claim sentence I traced (gap, IR design choice, semantic measures, experiment setup, results, comparison, limits) maps to a quoted statement or a line-anchored paraphrase. Suspect items I looked for and cleared:
  - “six-month” — the entry ties it to S110.txt:872/873 (real: “spanning six months” / “used around 500 CPU cores”), never to S093's six-month production window (recorded distinctly as PZ's own window at S093.txt:26).
  - “state-of-the-art” — the entry quotes it (S110.txt:1156 “current state of the art in JavaScript fuzzing”, and §-line 140/142 with Sota italics) instead of paraphrasing; no claim that Fuzzilli outranked Superion beyond the specific figures the entry quotes (1279/1287/1332/1336/1341/1346 are all quoted).
  - Priority claim “first fuzzer that focuses on JIT vulnerabilities” — explicitly NOT verified (“This entry records that as the paper's claim and does not verify its priority”).
  - CVE numbers — deliberately not listed; the age/count claims carry only what the named lines state.
  - Comparison with SoFi — correctly attributed as “the paper's reading”, with the capture line 1228-1231 named.
- The 18-vs-17 root-cause arithmetic inconsistency is disclosed by the entry itself (Claim 5), not smoothed away.

T4 gaps, non-fatal:
- ScribeEntry's own stem-grep shows 8 of 83 stems NOT on the anchor line (`Q10, Q27, Q31, Q38, Q47, Q52, Q76, Q83`) — multi-line sentence wraps in the extraction. The instrument's own 2/4-line anchor windows (lossless with `anchor ±0/+3`) cover all eight; my window verifier `anchor-2..anchor+2` agrees. Not a defect; a note for the lesson text (the round lesson should say “83 quotes, 75 anchors single-line, 8 underscores multi-line — corrected by the normalized window”).
- The entry quotes at least one phrase — “Google V8, Apple JavaScriptCore, and Mozilla SpiderMonkey” (S110.txt:868) — whose pinned quote's sub-quote (Q17/Q18) is split into two manifest quotes. Both halves verify independently (exit 0 in B5). No mismatch, just a note that entry sentences and manifest quotes are 1-to-many (2 in this case).
- Samuel Groß is missing from the pinned quotes (below MIN_QUOTE_CHARS); the draft handles this correctly by not claiming a pinned quote for him.

VERDICT T4: **CONFORMANT — no outrun sentence found.** The manifest quotes assert what anchors state; the entry cites only the capture.

## Extra letter-vs-value checks (binding floaters)

1. Quit on the 24-quote manifest as-is: B5's example count “83 of 83” belongs to the other manifest; no failure, but B4's per-file binding accounting (A-rule) will see only the manifest that lands in the lane dir. L1: ONE manifest, the 24-quote one.
2. S109 (F52) capture `fuzzilli README S109.txt:151/165` distinctly says “semantic-correctness concerns” — different artifact from the paper's “semantic-correctness measures” (§IV-C). The entry keeps them separate; my read confirms no content bleed.
3. Claims.json Follow: the entry's `recheck:` line — `cd <lane> && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-75/manifest.json --source S110` — matches the `entry_recheck` letter exactly (form checked in the draft file, char count: 157, plain text).

## Residual risks / verification gaps (for the L1, not defects)

1. B5's letter says `every quote <= 25 words` and ExecC2Capture.md says “longest = 12 words (Q07, Q10, Q20)” — my count says the longest is **12 (Q07/Q10/Q20 = 12)**. Match, exit 0.
2. Title rendering: the snapshot carries `F UZZILLI` (pdftotext gap), while the registry-row title text will carry `FUZZILLI`. The manifest note explicitly discloses this. Downstream fuzz-bait: a verbatim-quote auditor could call Q01 a title mismatch; both my run and the instrument run agree the pinned quote is the artifact, and the comment is the cover.
3. The claims' C2 `after` says `records=89 bound=89 unbound=0`; that is bound-set arithmetic only the landed tree can produce — my checks cover the per-record work (B5/B4 letter) but NOT the fleet count, which re-runs at landing (B4). No drift found in any of the numbers' derivation.

## CONCLUSION

Per the frozen predicate letter: **no letter mismatch** in B1-B8 clauses; T1/T2/T3/T4 attacks found no drift, no false sat, no overclaim. Two PENDING-LANDING clauses (B1/B2's “exactly one new row S110”, B4 fleet-count) can only be scored after the L1 writes the files; the letter itself is clean. The single-highest-leverage residual is the B7 used-by-path risk: the used-by file must exist on disk the moment the row lands, else B7 trips the kill rule.
