# ScribeEntryC2 — round 28 wave 1 — F12 entry

Seat: ScribeEntryC2 (leaf, no dispatch). Item: draft the F12 entry
`corpus/knowledge/japanese-domestic-disclosure-workflow.md`, re-grounded on this round's captures.
Owned production file: that entry, and nothing else.

## Behavior

Landed `corpus/knowledge/japanese-domestic-disclosure-workflow.md` — 103 lines, 18544 bytes,
sha256 `a22d2321e39fd0e547d8ae480eb566648520e59281e69e057aab5ab8502413a6`.

- Q1 trio present directly under the H1: two `source:` lines (S041, S042, each with URL, section
  anchor and capture path), `verified-at: 2026-10-25`, one `recheck:` line, plus a `ground: F12` line
  in the F11 sibling's shape.
- Body: the 10-step software-product path, 起算日 as the disclosure-clock anchor (definition,
  two-way relay, 45-day 目安, the four considerations, the change clause, the five call-off grounds),
  the one-year withdrawal rule stated precisely as withdrawal of the 情報非開示依頼 and not of the
  report, the 7-step web-application path with what it lacks, the 8-step self-report path, and a
  "Why it matters" paragraph naming 起算日 as the transferable artefact and mapping it onto F02's
  trigger/interval/extension rule.
- Q4: every position is attributed — IPA for the intake process page, JPCERT/CC for the guideline —
  and the "Japanese standard" over-generalization is rejected explicitly.
- Q5: three falsifiable rules (trigger, scope, withdrawal) and four rejected over-generalizations.
- Q6: documentation-only; no probing, no credential material, no private URLs.
- Every load-bearing claim carries a ≤70-character verbatim quote with `S041.txt:LINE` or
  `S042.txt:LINE`; 30 quotes in the quoted-record table, 29 exactly-once, the one duplicate
  ("「画面キャプチャ」、", L344 and L929) bound by its line number and disclosed in Limits.

## Gates (measured after landing, on the landed bytes)

| check | command | observed |
|---|---|---|
| Q10 parse | `bash -n -c "<recheck line>"` | exit 0 |
| Q10 cwd | run from `/` and from lane root | identical sha256 `59bc2f5f…`, both exit 0 |
| Q9/R12 | `source-recheck.py --source S041`, `--source S042` | S041 Q1-Q6 OK occurrences=1; S042 Q1-Q6 OK occurrences=1 |
| recheck-audit | `python3 corpus/instruments/recheck-audit.py` | entry row `frozen=111 strict=111111 lane=0 foreign=0 executes PASS` |
| C2 counter 4 | `python3 corpus/instruments/frontier-recheck-count.py` | `PASS F12 … ids=S041,S042 exit=0`; `entries=15 pass=15 exit=0` |
| C2 counter 3 | `sources-census.sh validate --root … kasegi` | `census_exit=0`, only the pre-existing W04 S028/S029 |
| quote re-location | script over the entry's 30 table rows | 30/30 present on the cited line; 29 exactly-once |

## Touched surfaces

- `corpus/knowledge/japanese-domestic-disclosure-workflow.md` (new; the seat's only production write)
- `.ufo/waves/round-28/receipts/ScribeEntryC2.txt` (receipt: quote list + line anchors + runs)
- `.ufo/waves/round-28/wave1/ScribeEntryC2.md` (this report)
- `.ufo/waves/round-28/wave1/ScribeEntryC2/` (scratch: independent captures, audit json, expected-list copy)

No other lane file written. No VCS command run. No tool installed (pacman is paused host-wide anyway).

## Out-of-scope item handed to L1

`corpus/instruments/knowledge-expected.txt` is not in the ownership map, so this seat did not write it.
After the entry landed, `recheck-audit` reports `expected=39 missing=0 unexpected=1 exit=1` with
`unexpected=corpus/knowledge/japanese-domestic-disclosure-workflow.md` — the round-27 carry-forward 4
drift, now caused by this entry's existence. The minimal one-line append was **validated on a copy**
(`--expect .ufo/waves/round-28/wave1/ScribeEntryC2/expected-copy.txt`):
`lines=40 total=40 pass=40 … expect=present expected=40 missing=0 unexpected=0 exit=0`.

```sh
sed -i '/^corpus\/knowledge\/iso-29147-divergence-and-clause-crosswalk\.md$/a corpus/knowledge/japanese-domestic-disclosure-workflow.md' corpus/instruments/knowledge-expected.txt
python3 corpus/instruments/recheck-audit.py   # expected 40/40, exit 0
```

(`ev-model.md` sits out of C-order in the committed list — a pre-existing artifact that set equality
ignores; the append above leaves both it and every comment untouched.)

## Findings

1. **The staged draft's web path was wrong: seven steps, not six.** S042.txt:162-182 numbers
   1 届出の受付 … 7 統計情報の公表, and 図４ (S041.txt:1331) is the detailed flow. The entry follows
   the captures and records the correction in Limits; ExecCaptureS042 reported the same mismatch
   independently. The self-report path (not in the assignment) is eight steps (S042.txt:184-200) and
   is included because it completes the page's three flows.
2. **`source-recheck.py --source` is single-valued** (`corpus/instruments/source-recheck.py:275`), so the
   literal form in the assignment (`--source S041 --source S042` on one invocation) re-derives only S042
   — measured: that invocation printed only `S042:` lines. The landed line chains two invocations;
   ExecRecheckAuditR28 measured the same chain green on all six strict limbs from `/` and from the lane
   root. Entry declares the deviation in Limits.
3. **The 45-day figure is software-product-scoped, not programme-wide.** `45 日` occurs twice in the
   capture (S041.txt:648, 786), both in chapter Ⅳ; chapter Ⅴ (S041.txt:856-1150) has none, and the web
   path has no 起算日 step at all (S042.txt:162-182; 図４ has no 起算日の連絡, 図３ has four).
4. **S041's round-28 re-capture is byte-identical to round-26** (`e18acbf9…`), so F11's line anchors
   into round-26/S041.txt still resolve in round-28/S041.txt — worth knowing before anyone treats the
   re-capture as a changed source.
5. **CERT/CC's interval and this one are both 45 days** — recorded as a coincidence with an explicit
   "neither capture links them; keep the records separate" note, so a later F02 cross-walk cannot
   merge two different policies on a matching number.

## Artifacts

- `corpus/knowledge/japanese-domestic-disclosure-workflow.md` (deliverable)
- `.ufo/waves/round-28/receipts/ScribeEntryC2.txt` (quote list with line anchors, run log, open item)
- `.ufo/waves/round-28/wave1/ScribeEntryC2/recheck-audit.json`
- `.ufo/waves/round-28/wave1/ScribeEntryC2/expected-copy.txt` (validated remedy copy)
- `.ufo/waves/round-28/wave1/ScribeEntryC2/scratch/S041.txt`, `…/S042.txt` (independent captures, same
  sha256 as the production captures)

Nothing here is committed; the L1 commits through the lane helper.
