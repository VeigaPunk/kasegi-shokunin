# R46W2MutC2b — C2 counter v1.1 mutation battery, gates G4-G5

VERDICT: BROKEN

Scope: `corpus/instruments/r46-c2-gate.py` v1.1 (sha256 `b52fea3183a393fa2f5bb40879241034e9db0b45f7914244d9f3bed134958621`), limbs G4 (manifest / capture) and G5 (entry citations). Target tree: committed tip `5437afeaf9b642c267bba3c31f00ae701e49da68` (exported with `git archive`; the lane HEAD is `0d121a2`, a descendant that changes no targeted file: `cmp` of the five targeted files against the tip printed nothing). Counter and `source-recheck.py` (sha256 `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`) were run from the lane's `corpus/instruments/` with `--root <copy>`; neither was edited. Nothing was committed; the scratch copy is removed on exit.

The tip itself is not shown defective: the do-nothing control passes 7/7 and the raw-file oracle finds zero uncited curly, ASCII or single-curly quotes in the tip entry. The BROKEN verdict is about the instrument: twelve single-edit mutants were run and seven defects were not rejected (F1-F7 below). Survivors come first.

## How the battery ran

- Recipe (scratch, removed): for each mutant, copy the tip export, apply one edit, run `python3 corpus/instruments/r46-c2-gate.py --root <copy>`, print `mutant=<name> rejected=<0|1>` (rejected = counter exit != 0), the edit, a raw-file oracle, and every gate line.
- Entry mutants insert one block after line 25 of `corpus/knowledge/github-private-vulnerability-reporting.md` (line 25 is blank, line 26 is `## Overlap and novelty`; the assert on those two lines passed).
- Manifest mutants run in two modes: `graded` (the lane's pin `PINS["manifest.json"]` stays in force) and `repinned` (`R46_PINS_OVERRIDE` set to the mutated manifest's own sha256, the counter's documented selftest hook, to judge the G4 limbs without the pin). Repinned mode is an isolation device, not a grading mode.
- Oracle: a naive regex pass over the RAW entry file with no comment, fence or live-line stripping, and no counter code, so it reads what the counter hides.
- Command: `MUT_SCRATCH=<scratch> TMPDIR=<scratch>/tmp python3 recipe.py` (full output: 260 lines; sha256 `6861aad34b113cd78e4ba402ff683a1d8494f70caaf19f4bacb7e643c00d291d`).

Full run, summary line (exact): `SUMMARY runs=19 rejected=8 not-rejected=11` (the 11 not-rejected are 4 controls by design and 7 survivors).

## Findings: survivors (defect present, counter exits 0)

### F1 — fenced-looking line hides an uncited curly quote (G5, live-line handling). Survives.
Edit: after line 25 insert
```
    ```
The reporter may also state that “anyone can file a report by email to the maintainers.” This sentence has no citation.
    ```
```
Output (exact): `mutant=M01-fence-hides-uncited-curly-prose rejected=0`; `oracle(raw file ...): {'curly_uncited': 1, 'ascii4w_uncited': 0, 'single_curly4w': 0}`; `counter exit=0 fixed=7/7 failing=- target=G5 target-pass=1`; `gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5`.
Why: `live_lines()` (counter lines 114-126) treats a line whose `strip()` begins with ``` as a fence and drops everything until the next fence line, so the sentence is removed from `body` (line 284). CommonMark does not treat `    ```` (four spaces) as a fence. Rendered with the reference CommonMark implementation (`cmark`, `/usr/bin/cmark`, preinstalled, not changed), the sentence is ordinary paragraph text:
`<p>The reporter may also state that “anyone can file a report by email to the maintainers.” This sentence has no citation.` followed by a stray ```` ``` ```` in the same paragraph.

### F2 — an HTML comment opened in one fence and closed in another hides prose (G5, live-line handling). Survives.
Edit: after line 25 insert seven lines: ```` ```text ````, `<!--`, ```` ``` ````, the same uncited curly sentence as F1, ```` ```text ````, `-->`, ```` ``` ````.
Output (exact): `mutant=M02-comment-spans-fences-hides-prose rejected=0`; `oracle: {'curly_uncited': 1, ...}`; `gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5`.
Why: the comment regex `(?s)<!--.*?-->` (counter line 116) runs on the whole text before the line/fence pass, so it removes the prose between the `<!--` inside the first code fence and the `-->` inside the second. `cmark` renders the sentence as `<p>…</p>` between two `<pre><code class="language-text">` blocks, i.e. visible prose.

### F3 — ASCII quote of four or more words split across two lines is not held (G5, ASCII). Survives.
Edit: after line 25 insert
```
The reporter may say "anyone can file a
report with the maintainers" in the form.
```
Output (exact): `mutant=M03-multiline-ascii-quote-uncited rejected=0`; `oracle: {'curly_uncited': 0, 'ascii4w_uncited': 1, 'single_curly4w': 0}`; `gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5`.
Why: the ASCII regex (counter line 288) is `"([^"\n]{12,})"`, which cannot cross a newline, and the curly regex (line 286) is the only multi-line-capable one. `cmark` renders `<p>The reporter may say &quot;anyone can file a` / `report with the maintainers&quot; in the form.</p>`.

### F4 — ASCII quote of four words but under 12 characters is not held (G5, ASCII). Survives.
Edit: after line 25 insert `The reporter may say "is it so ok" in the summary.`
Output (exact): `mutant=M04-ascii-4word-under-12-chars-uncited rejected=0`; `oracle: {'curly_uncited': 0, 'ascii4w_uncited': 1, 'single_curly4w': 0}`; `gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5`.
Why: the same regex requires `{12,}` characters (line 288) while the errata states the rule as "an ASCII-quoted span of >= 4 words is held to the same cite-and-locate rule" (`.ufo/waves/round-46/counter-errata.md` line 36, row C2-E4). "is it so ok" is 4 words, 11 characters. The sentence and the code disagree.

### F5 — single curly quotes ‘…’ are never held (G5, curly). Survives. Reading-dependent.
Edit: after line 25 insert `The page calls the form ‘the private report form for maintainers’ in its heading.`
Output (exact): `mutant=M05-single-curly-quote-uncited rejected=0`; `oracle: {'curly_uncited': 0, 'ascii4w_uncited': 0, 'single_curly4w': 1}`; `gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5`.
Why: `allcurly` (line 286) matches only `“ ”` (U+201C/U+201D). The counter's own G5 description (docstring line 27) says "no curly quote is uncited". Read literally, a single curly quote is a curly quote. The counter cannot count `’` as a quote mark (it is the apostrophe), so this needs a decision, not a patch; flagged as a reading question, not a certain defect.

### F6 — G4 distinctness reads `sources[0]`, not S073 (G4, manifest distinctness). Survives under re-pin only.
Base: tip manifest plus a clean decoy record `{"id":"S000", ... 8 distinct quotes, anchors 1-8}` inserted at `sources[0]`. Edit: the S073 record's Q2 is replaced by a copy of Q1 (text "Anyone can privately report a security vulnerability to repository maintainers.", anchor 560).
Output (exact, repinned): `mutant=M11-dup-quote-behind-decoy-sources0/repinned rejected=0`; `oracle: {'s073_quotes': 8, 's073_distinct_texts': 7, ...}`; `gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0`.
Why: `qs = json.load(...)["sources"][0]["quotes"]` (counter line 272); distinctness (line 273) is evaluated on that list. `source-recheck --source S073` (line 266) verifies only S073, so the S073 duplicate is invisible to the check. Same edit with the decoy absent is rejected (M10, below), so the decoy is what hides it.
As graded (pin on): `mutant=M11-dup-quote-behind-decoy-sources0/graded rejected=1` with `gate G4 pass=0 read=manifest-not-the-pinned-bytes`. The as-graded pin is the only reason it is rejected.

### F7 — a frozen core carried only in a note field passes G4 (G4, manifest cores). Survives under re-pin only.
Edit: the S073 record's Q3 quote is replaced by the snapshot's `Private vulnerability reporting is separate from a repository’s SECURITY.md file.` (snapshot line 564), and the record gains `"note": "You can only report vulnerabilities privately for repositories where this feature is enabled."`.
Output (exact, repinned): `mutant=M12-core-moved-to-note-field/repinned rejected=0`; `oracle: {'s073_quotes': 8, 's073_distinct_texts': 8, 'cores_in_quote_records': 4, 'cores_anywhere_in_manifest': 5}`; `gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0`.
Why: the frozen-core check is `norm(c) not in norm(whole manifest text)` (counter lines 269-270), a substring test over the whole file, not over the quote records. As graded: `gate G4 pass=0 read=manifest-not-the-pinned-bytes` (rejected by the pin).

## Controls and rejections (limbs that do bite)

- C0 do-nothing (unmutated tip): `mutant=C0-do-nothing-tip rejected=0`, `c2-gate fixed=7/7 exit=0`, `gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5`. Oracle on the tip: all zeros; manifest `{'s073_quotes': 8, 's073_distinct_texts': 8, 'cores_in_quote_records': 5, 'cores_anywhere_in_manifest': 5}`.
- C1 legit edit (a 12-line cite `(`S073.txt:556-567`)`): accepted, `gate G5 pass=1 read=spans=22 located=22 failed=0 uncited=0 cores=5/5`. Shows the span limit is exactly 12 lines.
- C2 repinned tip and C3 decoy base without the duplicate: both `rejected=0`, 7/7. So the repin hook works, and a decoy alone is accepted (F6 needs the duplicate).
- M06 cite to nav line 550 (outside body 556-583): rejected. `gate G5 pass=0 read=spans=22 located=21 failed=1`. The block-level check shows `quote='Raise your quality score' lines=550-550 located=1 in_body=0`, so the one failure is the body bound (counter line 296).
- M07 cite `556-568` (13 lines): rejected, `located=1 in_body=1 span<=12=0`; the span limit (line 296, `b - a <= 11`) bites.
- M08 cited quote with a changed word: rejected, `located=0`.
- M09 uncited ASCII quote of 12+ characters and 4+ words: rejected, `gate G5 pass=0 read=spans=21 located=21 failed=0 uncited=1`. The straight-quote path does work when the quote is long enough.
- M10 duplicate (Q2 := copy of Q1, no decoy): rejected by both modes. Graded: `gate G4 pass=0 read=manifest-not-the-pinned-bytes`. Repinned: `gate G4 pass=0 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0` with `s073_distinct_texts: 7`, so distinctness is what rejects it.

Design note from the first attempt (not in the table): a duplicate of Q8 removed a frozen core, and a duplicate of Q2 with its original anchor (563) was rejected by source-recheck's `anchor=563-BROKEN` note, which G4 reads through `"BROKEN" not in out`. Both runs rejected for the wrong reason; the reported M10 copies Q1 with its anchor so only the distinctness limb is in play.

## Limitations

- Twelve mutants, not an exhaustive search. Only G4 and G5 were attacked; G1-G3, G6, G7 were not mutated (they read 1 on the tip).
- Repinned runs use `R46_PINS_OVERRIDE`, which the counter documents as "selftests only". It is used here only to isolate limbs; as graded the pin rejects every manifest edit, so F6 and F7 are conditional on a future re-pin of the manifest. Whether a re-pin is likely is not assessed here; the as-graded tree is not exposed.
- F5 depends on reading "no curly quote is uncited" as including ‘ ’. I did not change the counter.
- Two-edit mutants: F7 changes Q3's text and adds a note key (one defect, two byte edits). F6's base is the tip plus a decoy record; the single mutant edit is the Q2 copy. Both disclosed.
- The raw oracle is a naive regex, not an independent Markdown parser. Rendering evidence (`cmark`, reference CommonMark) was taken for F1-F3 only; F4 and F5 are plain text lines.
- `source-recheck.py` and `S073.txt` were not mutated: the snapshot is bound through the manifest's `sha256`, which the pin covers.
- No tool was installed or upgraded; `cmark` is the preinstalled `/usr/bin/cmark`.

## Suggested falsification fixes (for the L1 to decide; not applied)

1. Live-line pass: treat a fence as a fence only when the marker is at column 0-3 (CommonMark), and strip HTML comments line-by-line inside live text, not across fences.
2. Quote regex: hold ASCII quotes of 4+ words regardless of length, and allow the match across newlines (match the same way as curly quotes).
3. Distinctness and cores: read the record whose `id == "S073"`; check frozen cores against the `quote` fields of that record, not the whole manifest text.
4. Decide and write down whether single curly quotes are quotes; if yes, handle the apostrophe ambiguity explicitly.
