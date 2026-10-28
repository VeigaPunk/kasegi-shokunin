VERDICT: BROKEN

# R45W2MutC2G5: mutation test of C2 gate G5 (r45-c2-gate.py v1.1)

Target: export of lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (round base dc5bb8c6e31efc4a6650819df85e79b72fd64bcd), extracted with `git archive | tar -x` into scratch. The counter bytes were not changed; every copy reports `counter-sha=639a038a99bd` (sha256 prefix of corpus/instruments/r45-c2-gate.py). Each mutant edits only the F27 entry `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` in a fresh copy of the export's `corpus/`. SOURCES/manifest/snapshot pins (G3, G4) are untouched in every mutant, so these survivors are not byte forgeries.

Method: scratch recipe applies one edit per mutant, runs `python3 corpus/instruments/r45-c2-gate.py --root <copy>` from the copy, and sets rejected=1 on non-zero exit. The failing gate is recorded per mutant so that a kill is attributed to G5 and not to another gate.

Command run: `R45_VERBOSE=1 python3 recipe.py` (exit 0). Printed lines, verbatim (the entry-sha and bytes fields are omitted here):

```
P26=(26 words) 'will not be processed. Note that a time-dependent version such as "latest mainline" is not acceptable. A stable identifier such as a commit ID or an'
P25=(25 words) 'will not be processed. Note that a time-dependent version such as "latest mainline" is not acceptable. A stable identifier such as a commit ID or'
mutant=C0-do-nothing-tip rejected=0
  exit=0 failing-gates=none G5-read=[spans=24 located=24 failed=0 uncited=0 cores=4/4] counter-sha=639a038a99bd
mutant=C1-benign-25-word-located rejected=0
  exit=0 failing-gates=none G5-read=[spans=25 located=25 failed=0 uncited=0 cores=4/4] counter-sha=639a038a99bd
mutant=M01-misquote-located-span rejected=1
  exit=1 failing-gates=G5 G5-read=[spans=24 located=23 failed=1 uncited=0 cores=3/4] counter-sha=639a038a99bd
mutant=M02-wrong-window-citation rejected=1
  exit=1 failing-gates=G5 G5-read=[spans=24 located=23 failed=1 uncited=0 cores=4/4] counter-sha=639a038a99bd
mutant=M03-citation-range-past-eof rejected=0
  exit=0 failing-gates=none G5-read=[spans=24 located=24 failed=0 uncited=0 cores=4/4] counter-sha=639a038a99bd
mutant=M04-midword-fragment-quote rejected=0
  exit=0 failing-gates=none G5-read=[spans=25 located=25 failed=0 uncited=0 cores=4/4] counter-sha=639a038a99bd
mutant=M05-26-word-single-span rejected=1
  exit=1 failing-gates=G5 G5-read=[spans=25 located=24 failed=1 uncited=0 cores=4/4] counter-sha=639a038a99bd
mutant=M06-26-word-split-into-two-spans rejected=0
  exit=0 failing-gates=none G5-read=[spans=26 located=26 failed=0 uncited=0 cores=4/4] counter-sha=639a038a99bd
mutant=M07-core-quote-dropped rejected=1
  exit=1 failing-gates=G5 G5-read=[spans=23 located=23 failed=0 uncited=0 cores=3/4] counter-sha=639a038a99bd
mutant=M08-core-quote-hidden-in-html-comment rejected=0
  exit=0 failing-gates=none G5-read=[spans=24 located=24 failed=0 uncited=0 cores=4/4] counter-sha=639a038a99bd
mutant=M09-uncited-curly-quote rejected=1
  exit=1 failing-gates=G5 G5-read=[spans=24 located=24 failed=0 uncited=1 cores=4/4] counter-sha=639a038a99bd
mutant=M10-uncited-straight-quote rejected=0
  exit=0 failing-gates=none G5-read=[spans=24 located=24 failed=0 uncited=0 cores=4/4] counter-sha=639a038a99bd
mutant=M11-dangling-open-curly-at-eof rejected=0
  exit=0 failing-gates=none G5-read=[spans=24 located=24 failed=0 uncited=0 cores=4/4] counter-sha=639a038a99bd
mutant=M12-citation-separator-not-paren rejected=1
  exit=1 failing-gates=G5 G5-read=[spans=23 located=23 failed=0 uncited=1 cores=4/4] counter-sha=639a038a99bd
```

Result: 6 of 12 mutants survive (G5 green while the defect is present). The 6 that are killed fail only G5. Both controls stay green: the do-nothing tip (C0) and a benign 25-word located span (C1). Survivors are listed first.

## Survivors

### F1. The 25-word rule is applied per span, so one 26-word passage passes split into two cited spans (M06)
- Attacked: `r45-c2-gate.py:252` `if len(nq.split()) <= 25 and nq and nq in window`. The check runs per regex match (line 245), not per contiguous passage, and nothing aggregates adjacent citations to the same window.
- Exact edit: in entry line 50, replace `- Documentation only.` (the only occurrence) with `- Documentation only. The page says “will not be processed. Note that a time-dependent version such as "latest mainline"” (`S071.txt:21-27`) and “is not acceptable. A stable identifier such as a commit ID or an” (`S071.txt:21-27`).`
- Output: `mutant=M06-26-word-split-into-two-spans rejected=0`, `G5-read=[spans=26 located=26 failed=0 uncited=0 cores=4/4]`.
- Discrimination: the same 26 words in one span (M05) are rejected with `located=24 failed=1`. C1 with 25 words in one span is accepted. The 25-word boundary holds per span; splitting defeats it. The probe output `split spans: [(13, '21', '27', 'will not be processed. Note that a time-'), (13, '21', '27', 'is not acceptable. A stable identifier s')]` confirms each half is cited to `S071.txt:21-27` and is 13 words.

### F2. Citation windows are open-ended: an out-of-range end passes, and a wrong-line citation is masked (M03, S2)
- Attacked: `r45-c2-gate.py:250` `window = norm(" ".join(snap[max(a - 1, 0):b]))`. Python slicing clips `b` at EOF silently. There is no check that `b <= len(snap)`, and no check that the window is tight around the quote.
- M03 exact edit: entry line 21, `(`S071.txt:41-43`)` becomes `(`S071.txt:41-99999`)`. Output: `mutant=M03-citation-range-past-eof rejected=0`, `G5-read=[spans=24 located=24 failed=0 uncited=0 cores=4/4]`. The snapshot has 372 lines (probe output `snapshot-lines=372`), so 99999 cites lines that do not exist.
- S2 (wrong line, open end): entry line 24 quotes “Once a robust fix has been developed, the release process starts”. Its true location is `S071.txt:305` (probe output: `S071 line 305 = 'Once a robust fix has been developed, the release process starts.  Fixes'`). Citing it as `(`S071.txt:41-99999`)` gives `rejected=0`. The control S1, the same quote cited as `(`S071.txt:41-43`)`, gives `rejected=1` with `located=23 failed=1`. An open end turns a wrong citation into a pass.

### F3. Core quotes are accepted from inside an HTML comment (M08)
- Attacked: `r45-c2-gate.py:242` `body = txt(root, p)` scans the raw body. G1 and G2 read through `live_lines()` (lines 108-118, used at lines 124 and 133), which strips `<!-- -->` and fences. G5 does not.
- Exact edit: entry line 20, `“Binary-only executables are not accepted” (`S071.txt:39-40`)` becomes `<!-- “Binary-only executables are not accepted” (`S071.txt:39-40`) -->`. The visible table row then has no kernel-text quote.
- Output: `mutant=M08-core-quote-hidden-in-html-comment rejected=0`, `G5-read=[spans=24 located=24 failed=0 uncited=0 cores=4/4]`.
- Probe output: `M08 live_lines contains core: False` and `M08 raw body contains core: True`. The visible row after the edit: `| May the reproducer be a binary? |  | ... A binary-only file fails the field. |` (kernel-text cell empty).

### F4. An uncited verbatim quote in ASCII quotes is not counted (M10)
- Attacked: `r45-c2-gate.py:244` `allcurly = re.findall("\u201c([^\u201d]+)\u201d", body)`. Only U+201C/U+201D are counted. The tip has zero straight quotes (probe output `tip counts: open“=24 close”=24 straight"=0`).
- Exact edit: entry line 50, `- Documentation only.` becomes `- Documentation only. The page says "a reproducer is always required".`
- Output: `mutant=M10-uncited-straight-quote rejected=0`, `G5-read=[... uncited=0 ...]`. The same sentence in curly quotes (M09) is rejected with `uncited=1`.

### F5. A dangling opening curly quote with no closing quote is invisible (M11)
- Attacked: `allcurly` (line 244) needs a closing ”. The tip has 24 “ and 24 ”.
- Exact edit: append `\nThe page also says “a reproducer is always required.\n` at end of file (after entry line 60).
- Output: `mutant=M11-dangling-open-curly-at-eof rejected=0`, `G5-read=[spans=24 located=24 failed=0 uncited=0 cores=4/4]`.
- Limitation: I tested only the EOF position. [INFERENCE] A stray “ earlier in the file would pair with a later ” and fail G5 as a swallowed span, so the escape is specific to a final unpaired quote. That inference is from reading the regex and was not run.

### F6. The located check is raw substring, so a mid-word fragment passes as a quotation (M04)
- Attacked: `r45-c2-gate.py:252` `nq in window`. There is no token-boundary check.
- Exact edit: entry line 50, `- Documentation only.` becomes `- Documentation only. The quote “absolutely necessary in any security bug rep” (`S071.txt:17-18`) is a fragment.`
- Output: `mutant=M04-midword-fragment-quote rejected=0`, `G5-read=[spans=25 located=25 failed=0 uncited=0 cores=4/4]`. The fragment “rep” is a truncation of “report”, and it is counted as located.

## Killed (G5 is the only failing gate)
- M01 (entry line 25): `up to 7 calendar days` changed to `up to 14 calendar days`. `failed=1 cores=3/4`.
- M02 (entry line 11): citation `S071.txt:17-18` changed to `S071.txt:200-201`. `located=23 failed=1`.
- M05 (entry line 50): the 26-word passage in one span. `located=24 failed=1`.
- M07 (entry line 20): core-bearing quote replaced by unquoted prose. `cores=3/4`.
- M09 (entry line 50): uncited curly quote added. `uncited=1`.
- M12 (entry line 11): `”` followed by `, see `S071.txt:17-18`` (no parenthesis). `uncited=1`.

## Limitations
- Single-edit mutants only, applied to the F27 entry in a copy of the export's `corpus/` (8.4 MB). Combinations and other entries were not tested.
- Gates G1-G4 and G6 were not attacked (out of scope). G4 ran `source-recheck.py` from the copy. G7 ran the counter's constant fleet census path, `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <copy>`, read-only. I did not read that script.
- Severity: F3, F5 and F1 are gaps against the gate's own predicates (cores in the entry, every curly span, the 25-word rule). F2, F4 and F6 depend on whether the contract reads "located in lines N..M", "uncited" and "a quotation" strictly. A stricter reader would treat them as defects; a looser one as intended.
- Not tested: CRLF or non-UTF-8 entries, and quotes that span an `S071.txt` line range with markup inside the span.
- One accidental malformed edit hit my scratch copy of the recipe script and was fixed by rewriting the file. The lane was not touched.
- Nothing installed or upgraded. No git or jj mutation. Scratch removed on exit.

## Suggested predicate hardening (not applied; the L1 decides)
- Aggregate adjacent spans citing the same window before the 25-word check (F1).
- Reject `b > len(snap)` and require the located window to be bounded, e.g. at most the cited span plus a fixed slack (F2).
- Run G5 on `live_lines(body)` (F3).
- Count straight and single-curly quotes in the uncited check, and fail on any unbalanced quote mark (F4, F5).
- Match on word boundaries, e.g. `re.search(r"(?<!\w)" + re.escape(nq) + r"(?!\w)", window)` (F6).
