VERDICT: BROKEN

Seat R46RevC2G5 — attack on C2 gate G5 (`def g5`, corpus/instruments/r46-c2-gate.py, lines 255-276). Read-only; no lane file edited; all fixtures under /fast/scratch/hyaku/kasegi-r46/R46RevC2G5 (removed on exit).

Counter identity: `sha256sum corpus/instruments/r46-c2-gate.py` printed `0ee958578b5923706178081a94dae471682f02f74492bb4a3b54a118c12ec3f6`, equal to freeze.txt `c2-gate-sha256`. S073.txt printed `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930` (matches PINS). S073.txt is 589 lines.

## Finding 1 (BROKEN): G5 passes an entry whose only content is five cores cited to the whole capture

G5 has no range-width check: `window = norm(" ".join(snap[max(a - 1, 0):b]))` takes `a` and `b` straight from the citation. A citation of `S073.txt:1-589` makes the window the entire 589-line capture, navigation included, so any <=25-word substring of the capture counts as located.

Recipe (cheapest tree, three files; the entry is 358 bytes, one line):
- `corpus/README.md`: `| F28 | GitHub private vulnerability reporting | admitted | knowledge/github-private-vulnerability-reporting.md | S073 | probe |`
- `corpus/source-snapshots/round-46/S073.txt`: copied unchanged from the freeze commit.
- `corpus/knowledge/github-private-vulnerability-reporting.md`: the five frozen cores, each cited to 1-589:
  `“only report vulnerabilities privately for repositories where this feature is enabled” (S073.txt:1-589) “summary, details, proof of concept, and impact statement” (S073.txt:1-589) “I used AI assistance” (S073.txt:1-589) “credited user on the proposed advisory” (S073.txt:1-589) “only the repository maintainer can merge” (S073.txt:1-589)`

Command: `python3 corpus/instruments/r46-c2-gate.py --root /fast/scratch/hyaku/kasegi-r46/R46RevC2G5/cheap`
Printed (G5 line): `gate G5 pass=1 read=spans=5 located=5 failed=0 uncited=0 cores=5/5`
Direct call `m.g5(root)` printed: `(True, 'spans=5 located=5 failed=0 uncited=0 cores=5/5')`

Five spans is the fewest that cover the five cores in my reading of the source lines (564, 573, 574, 577, 578): no pair of cores falls within one 25-word contiguous passage. This is reasoned from the line text, not exhaustively tested.

Full-tree demonstration (freeze tree + F28 row + S073 row inserted after S072 in the Registry + an entry with the four-section shape, a 6-row table and two in-range xrefs; `/fast/scratch/hyaku/kasegi-r46/R46RevC2G5/fC-wide`): the five cores cited to `S073.txt:1-589`, everything else identical. Printed:
- `gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md`
- `gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=6 xrefs=2/2`
- `gate G3 pass=1 read=row-S073=ok`
- `gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0`
- `gate G5 pass=1 read=spans=5 located=5 failed=0 uncited=0 cores=5/5`
- `gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1`
- `gate G7 pass=1 read=census-rc=0 ok-line=1`
- `c2-gate fixed=7/7 exit=0`

So the whole counter grades a wide-range entry as complete. The C2 kill rule's control list (do-nothing, junk-row, fabricated-quote, uncited-filler) has no wide-range entry, so none of the frozen controls catches this.

## Finding 2: G5 can fail alone (discrimination shown)

Same full tree as fA-honest (precise cites 564/573/574/577/578), with the enablement core replaced by an uncorroborated quote `“private reporting is enabled by default on every public repository” (S073.txt:564)` (`fB-fabricated`):
- `gate G5 pass=0 read=spans=5 located=4 failed=1 uncited=0 cores=4/5`
- every other gate `pass=1` (G1, G2, G3, G4, G6, G7 as printed in Finding 1; G2 `sections=4/4 table-rows=6 xrefs=2/2`)
- `c2-gate fixed=6/7 exit=1`

Honest precise-cite control (`fA-honest`): `gate G5 pass=1 read=spans=5 located=5 failed=0 uncited=0 cores=5/5`, `c2-gate fixed=7/7 exit=0`.

Answer: yes, G5 can be the single red gate (fB). Its failure comes from the located check, not from the structure gates. The freeze control `c2 fabricated-quote` was not a G5-alone case (G2 was also red there: `sections=1/4`).

## Finding 3: additional constructions that pass G5 (each a direct `g5` call on a 3-file tree: README, S073.txt, entry)

| # | Construction | G5 output |
|---|---|---|
| a | five cores, precise cites, nothing else | `(True, 'spans=5 located=5 failed=0 uncited=0 cores=5/5')` |
| b | navigation text cited to nav lines (`“Report privately” (S073.txt:12)`, `“Configure vulnerability reporting” (S073.txt:278)`, `“Create repository advisory” (S073.txt:284)`) plus the five cores; the nav text is used as support | `(True, 'spans=8 located=8 failed=0 uncited=0 cores=5/5')` |
| c | stitched prose: "they gain “credited user on the proposed advisory” (S073.txt:577) only after “only the repository maintainer can merge” (S073.txt:578) and …", contradicted by S073.txt:577 ("automatically adds the reporter ... on submit") | `(True, 'spans=5 located=5 failed=0 uncited=0 cores=5/5')` |
| d | straight-quoted, uncited claim `"GitHub notifies your Security team by e-mail within one hour"` beside the five cored spans (the gate reads only curly quotes) | `(True, 'spans=5 located=5 failed=0 uncited=0 cores=5/5')` |
| e | unclosed curly quote `“a bounty on every submission, uncited, with the closing quote missing.` after the five cored spans | `(True, 'spans=5 located=5 failed=0 uncited=0 cores=5/5')` |
| f | wide-range cores (Finding 1) | `(True, 'spans=5 located=5 failed=0 uncited=0 cores=5/5')` |

Discriminating controls, same harness, all red as intended:
- wrong range (five cores cited `S073.txt:1-10`): `(False, 'spans=5 located=0 failed=5 uncited=0 cores=0/5')`
- fabricated core (`... can merge and publish the advisory`): `(False, 'spans=5 located=4 failed=1 uncited=0 cores=4/5')`
- closed uncited curly quote beside the five cores: `(False, 'spans=5 located=5 failed=0 uncited=1 cores=5/5')`
- freeze do-nothing (freeze tree, no F28 row): `gate G5 pass=0 read=F28-rows=0`; counter `c2-gate fixed=2/7 exit=1` (G4 and G7 green at freeze, as claims.json states).

Note on construction (b): my first draft put a citation after a word rather than directly after the closing quote. G5 printed `uncited=2` and failed it. That was my construction error, and the gate handled it correctly. The corrected version is row (b).

## Finding 4: what the gate cannot see (not counted as G5 bugs)

- Stitching (c) and nav-as-support (b) are semantic; G5 cannot measure them. The C2 kill rule places that check on the non-author closure. The wide-range form in Finding 1 is different: it is a gate defect, because the "every curly quote located" limb is meant to bind each quote to its cited lines.
- Straight quotes (d) and unclosed curly quotes (e): the regex `“([^”]+)”` and the `allcurly`/`spans` counts ignore them. These are literal-spec holes.
- Code reading (not exercised): `body = txt(root, p)` at line 259 uses the raw entry, not `live_lines()`, so quotes inside an HTML comment or fenced code block are counted. I did not build a fixture for this.

## Limitations

- Full-tree fixtures use my own placeholder prose for the F28 entry and a placeholder S073 row. They are scratch fixtures for testing the gates, not drafts for the lane. The G5 results depend only on the README F28 cell, the entry's curly-quote spans, and the committed S073.txt. The other gates were checked only as far as the fixture satisfies them.
- The real F28 entry and S073 row do not exist at freeze, so this is not a grade of the lane's entry.
- Constructions were chosen to reach the stated defect classes; I did not run an exhaustive search over quote-regex edge cases.
- Lane state: `git status --short` in the lane printed 36 lines, all from other seats' writes. This seat ran no mutating git or index command and wrote no lane file other than this report.

## Recommendation (for the L1; not implemented)

Bound the cited range (e.g. `b - a <= 3`, or require the located text to fall within a small window of the snapshot). Apply the same curly/straight and paired-quote checks to straight quotes and unclosed curly quotes. The stitching and nav-as-support classes stay with the non-author closure.
