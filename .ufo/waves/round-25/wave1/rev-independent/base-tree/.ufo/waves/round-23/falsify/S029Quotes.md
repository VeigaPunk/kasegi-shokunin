# S029 quote exactness — falsify report

Seat: `L1Kasegi23.S029Quotes-2` (leaf, read-only). Target: `corpus/knowledge/cra-manufacturer-reporting-duties.md` against
`corpus/source-snapshots/round-23/S029.txt`. All statements below were reproduced from bytes in this session; no L1
claim is adopted as evidence.

## Method (read-only; no production write, no git/jj mutation)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/source-snapshots/round-23/S029.txt
# 82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c  corpus/source-snapshots/round-23/S029.txt
python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-23/manifest.json --source S029
# S029:sha256 OK + OK for art14-2a / art14-2b / art14-2c / art14-4c / art71-article-14-start /
#          art71-general-application ; EXIT=0
```
Digest equals the manifest pin for S029 (`manifest.json`, sources[id=S029].sha256). Quote presence was decided by
Python `in` on the decoded UTF-8 text (byte-substring semantics) and independently by `grep -F -n -o`; the two agreed
on every string below. Snapshot is 146 lines / 19900 bytes.

## Six "Exact located quotes" (entry lines 45-50)

Each entry quote was extracted mechanically from between the U+201C/U+201D delimiters, not retyped.

| # | Entry line | Attributed to | S029 line(s) | Occurrences | Word count | Verdict |
|---|---|---|---|---|---|---|
| 1 | 45 | Article 14(2)(a) | 10 (and 20) | 2 | 10 | exact substring |
| 2 | 46 | Article 14(2)(b) | 12 | 1 | 13 | exact substring |
| 3 | 47 | Article 14(2)(c) | 14 | 1 | 13 | exact substring |
| 4 | 48 | Article 14(4)(c) | 24 | 1 | 13 | exact substring |
| 5 | 49 | Article 71 | 124 | 1 | 8 | exact substring |
| 6 | 50 | Article 71 | 122 | 1 | 8 | exact substring |

Evidence lines (verbatim, from `grep -n -F -o`):
- `10:within 24 hours of the manufacturer becoming aware of it` and `20:` same string (Article 14(4)(a)).
- `12:within 72 hours of the manufacturer becoming aware of the actively exploited vulnerability`
- `14:no later than 14 days after a corrective or mitigating measure is available`
- `24:within one month after the submission of the incident notification under point (b)`
- `124:Article 14 shall apply from 11 September 2026`
- `122:This Regulation shall apply from 11 December 2027.`

All quotes are <= 25 words (max 13), satisfying the table's own stated bound. Attribution check: each quote is
contained in the syntactic unit it names — Article 14(2)(a) at :10 (prefix `(a)an early warning notification of an
actively exploited vulnerability, without undue delay and in any event `), 14(2)(b) at :12, 14(2)(c) at :14,
14(4)(c) at :24, Article 71 at :124 / :122. Entry table and manifest carry the identical six strings in identical
order (set equality, `entry-only: []`, `manifest-only: []`).

## Article 71 application sentence

```
                  entry line 50 (od -c): |   A r t i c l e   7 1   |     342 200 234  T h i s ... 2 0 2 7 . 342 200 235
S029:122       : 2.This Regulation shall apply from 11 December 2027.
```

The quoted sentence `This Regulation shall apply from 11 December 2027.` is a byte-exact substring of S029:122,
terminal period included (the `od` dump shows `2027 .` immediately before the closing U+201D). The adjacent
`However, Article 14 shall apply from 11 September 2026 and Chapter IV (Articles 35 to 51) shall apply from 11 June
2026.` sits at S029:124 and supplies quote 5. Entry prose (lines 15-16) matches the excerpt: Article 14 2026-09-11 is
earlier than general application 2027-12-11. No other date in the entry conflicts with the four dates present in the
excerpt (`11 December 2025` :52 delegated acts, `11 December 2027` :122, `11 September 2026` and `11 June 2026` :124,
signature `23 October 2024` :128).

## Are any *other* entry quotes paraphrases rather than substrings?

Strict answer for quotes presented as source text: **no.** The entry contains exactly nine U+201C…U+201D spans.

- Seven are source quotes and all are substrings: line 23 `without undue delay` (snapshot lines 10, 12, 20, 22, 68,
  94) plus the six table rows above.
- Two are not substrings, and both are correctly *not* presented as S029 text:
  - line 55 `14 days after awareness` — a hypothetical worksheet label the entry instructs the reader to reject.
  - line 64 `CRA requires every researcher to publish a vulnerability within\n24 hours, and therefore authorizes
    testing.` — the "Rejected" strawman, explicitly labelled `Rejected:`.
  Both return `inset=False` against S029, which is the desired result: neither is asserted as captured wording.

### Secondary finding (labelling, not a false quote)

The unquoted summary column `Clock in official text` (entry rows 29-34, header at 27) is paraphrase in every cell. Five
probes built from that column's own wording return `inset=False` against S029; a sixth, snapshot-side control
(`unlawful or malicious acts`, S029:20) confirms the tool reports positives correctly:

| Probe | In S029? | Official wording it compresses |
|---|---|---|
| `Without undue delay; within 24 hours of awareness` | no | `without undue delay and in any event within 24 hours of the manufacturer becoming aware of it` (:10, :20) |
| `Without undue delay; within 72 hours of awareness, unless relevant information already provided` | no | `without undue delay and in any event within 72 hours of the manufacturer becoming aware of ...`, `unless the relevant information has already been provided` (:12, :22) |
| `No later than 14 days after a corrective or mitigating measure is available, unless relevant information already provided` | no | `... unless the relevant information has already been provided` (:14) |
| `Within one month after submission of the incident notification under (b), unless relevant information already provided` | no | `within one month after the submission of the incident notification under point (b)`, `unless the relevant information has already been provided` (:24) |
| `unless relevant information already provided` | no | `unless the relevant information has already been provided` (:12, :14, :22, :24) |
| `unlawful or malicious acts` | yes (:20) | snapshot-side positivity control, not a string from the entry column |

The column drops `in any event`, the awareness subject (`of the manufacturer becoming aware of it`), and the articles
(`the ... has already been`). This is a summary column without quotation marks, so it does not violate the exact-quote
contract; but its header names the official text, so a verifier that extends substring checking to that column fails
5/5 of its checked cells. Flagged as fidelity risk, not as a falsified quote.

## Falsifiable findings

1. **Falsified-if-not-true, currently holds:** all six strings in the entry's `Exact located quotes` table are
   byte-exact substrings of the pinned S029 bytes, in the article each row names, and the set is identical to the
   manifest's S029 assertion set. Falsifier: any one quote returning `inset=False`, or a manifest/entry string
   mismatch.
2. **Article 71 general-application sentence:** entry line 50 and S029:122 both read `This Regulation shall apply
   from 11 December 2027.` with the terminal period inside the quotation. Falsifier: period absent from the captured
   line, or entry text differing in any character.
3. **Paraphrase question:** zero entry quotes presented as S029 text are paraphrase-only; the only non-substring
   quoted spans (entry lines 55, 64) are the hypothetical worksheet label and the rejected claim, both explicitly
   framed as non-source. Falsifier: any table-row or inline quote that fails substring lookup above.
4. **Ambiguity note (not a defect):** quote 1 occurs twice (:10 and :20) because Article 14(4)(a) repeats the 24-hour
   wording for severe incidents. The entry's 14(2)(a) attribution is correct, but a bare substring check cannot
   distinguish the two tracks — an entry that cited only the substring to prove track separation would overclaim.

## Scope limits

- Read-only: no production file, lane tree, manifest, git/jj index or state was modified; the only write is this
  report. No installs or upgrades were needed, so none were performed.
- I verified captured-byte containment and article attribution, not substantive legal correctness, and not whether
  the paraphrase column is acceptable editorial style for a verifiability-graded entry (that is a grading judgment,
  not a byte fact).
- The pin certifies the local excerpt only; upstream freshness was not re-fetched. The excerpt is a partial OJ
  capture (Articles 14-17 and 71), so absence of a phrase proves nothing about the rest of the Regulation.
- The header claim `OJ 20.11.2024` is not present in the captured bytes (`20.11.2024` and `20 November 2024` both
  count 0); it is carried only by the ELI URL, so it is outside what this snapshot can verify.
- The `Clock in official text` probe table is my construction, not a check the repo's own instruments run.
