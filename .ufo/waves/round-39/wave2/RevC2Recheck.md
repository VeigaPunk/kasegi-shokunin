# RevC2Recheck — round 39 wave 2 (falsify), C2 counter re-run receipt

Seat: RevC2Recheck (attack seat, leaf; no subagents). Item: re-run the full C2 counter
set on the integrated lane tree and compare to the frozen after-values; any mismatch
is a kill finding. I did not author any deliverable under attack.

Lane state at measurement: HEAD `5006097a84305267c9a3e8c1e1d560e60fe41d37` (receipt
commit Y); J = `46c66c2` (content head J2); `git diff --name-only 46c66c2 5006097` =
`.ufo/waves/round-39/final-gates/all-gates.txt` (the receipt only), matching erratum
E4. Working tree: 5 untracked wave-2 runtime entries (`kasegi-r39-falsify.ready`,
`.ready.dispatched`, `wave2-dispatch.json`, `wave2-run.err`, `wave2/`); **zero tracked
modifications**. Claims freeze `dcd3170` and base `480b1a5` are ancestors of HEAD.

## Verdict: NO KILL — every frozen C2 after-value reproduces; controls verified

## 1. The frozen counter set (run from the lane root, TMPDIR bound to my scratch)

| # | frozen after-value | command | measured output | match |
|---|---|---|---|---|
| 1 | frontier 22 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `22` (exit 0) | YES |
| 2 | registry 59 (E1) | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `59` (exit 0) | YES |
| 3 | S057 row NF=13 | `awk -F'|' '/^\| *S057 *\|/{print NF}' corpus/SOURCES.md` | `awkNF=13` | YES |
| 4 | entry cites S057 | `grep -rlE '^source: S057' corpus/knowledge \| wc -l` | `1` | YES |
| 5 | knowledge 51 | `ls corpus/knowledge/*.md \| wc -l` | `51` | YES |
| 6 | harness 25/25 exit 0 | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=25 pass=25 exit=0` | YES |
| 7 | source-recheck S057 exit 0 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057` | 5 OK lines, `EXIT=0` | YES |
| 8 | binding 46/46 | `python3 corpus/instruments/capture-binding-check.py` | `records=46 bound=46 unbound=0`, `EXIT=0` | YES |
| 9 | audit expected=51 | `python3 corpus/instruments/recheck-audit.py --quiet` | `expect=present expected=51 missing=0 unexpected=0 exit=0` | YES |
| 10 | census exit 0, W04 S028/S029 only | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit 0, exactly two W04 lines | YES |
| 11 | junk-f22 4x MISMATCH exit 1 | source-recheck over committed `junk-manifest.json` + committed `S057.txt` (staged in my scratch) | 4x `MISMATCH reason=quote-not-found`, `EXIT=1` | YES |

As-frozen note: the registry counting command in `claims.json` says `-> 58`; erratum
E1 supersedes it (`registry != 58` reads `!= 59`, four appended rows S056–S059). I
measured 59; the fleet census independently agrees (`kasegi rows 59`; status.mined 44
+ queued 9 + rejected 6 = 59).

### Verbatim outputs

Counter 6 (harness) — 25 PASS lines, tail:
```
PASS     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055           exit=0
PASS     F22  knowledge/cisa-when-to-issue-vex.md                  ids=S057           exit=0
entries=25 pass=25 exit=0
EXIT=0
```
22 frontier rows → 25 entries: F09, F10, F11 each carry two entries; F-id sequence
F01..F22 has 22 distinct ids, no duplicate and no gap (`uniq -c` audit clean).

Counter 7 (positive source-recheck):
```
S057:sha256 OK
S057:Q1 OK normalized=markup-whitespace occurrences=1 anchor=12-ok
S057:Q2 OK normalized=markup-whitespace occurrences=1 anchor=132-ok
S057:Q3 OK normalized=markup-whitespace occurrences=1 anchor=136-ok
S057:Q4 OK normalized=markup-whitespace occurrences=1 anchor=184-ok
EXIT=0
```

Counter 8 (binding):
```
MANIFEST round-39 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=46 with_url=46 with_fetched_utc=8 with_archival=38 snapshot_dirs=15 manifest_dirs=15 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=46 bound=46 unbound=0
EXIT=0
```
(`orphan=S040-live.txt` is the pre-existing declared orphan, unchanged from base; it
does not enter the counts.)

Counter 9 (audit, --quiet):
```
strict pass=51/51 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=27 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=51 total=51 pass=51 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=51 missing=0 unexpected=0 exit=0
EXIT=0
```

Counter 10 (census):
```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
EXIT=0
```
Exactly the two pre-existing W04 codes; no new W/E code (the same two W04s fire at
base — see §4).

Counter 11 (junk-f22 negative twin; committed `junk-manifest.json` sha256
`9dafce36…` staged beside committed `S057.txt` in my scratch, so the manifest's
relative `path: S057.txt` resolves to the real capture):
```
S057:sha256 OK
S057:J1 MISMATCH reason=quote-not-found
S057:J2 MISMATCH reason=quote-not-found
S057:J3 MISMATCH reason=quote-not-found
S057:J4 MISMATCH reason=quote-not-found
EXIT=1
```
4x MISMATCH, exit 1 — the junk twin is rejected, matching the committed transcript
`.ufo/waves/round-39/c2-controls/junk-f22-recheck.txt` line for line.

## 2. Row-level content bindings (erratum E5 item 9)

- **S057 row** (`corpus/SOURCES.md`): awk NF=13 (census convention); cells: kind=`docs`,
  tier=`A`, status=`mined`, opened=`2026-10-26`, recheck=`180d`,
  used-by=`corpus/knowledge/cisa-when-to-issue-vex.md`; the source cell carries exactly
  one `https://` token, `https://www.cisa.gov/resources-tools/resources/when-issue-vex-information`
  (1 occurrence in the row).
- **F22 frontier row** (`corpus/README.md`): `| F22 | VEX issuance, lifecycle and
  inheritance guidance (CISA When to Issue VEX Information) | admitted |
  knowledge/cisa-when-to-issue-vex.md | S057 | …` — names the entry and source S057.
- **Rejected rows**: S056, S058, S059 each `status=[ rejected ]` with a `flip:` token
  and a reason in `teaches` (census W02 thin-teaches did not fire).
- **Entry** `corpus/knowledge/cisa-when-to-issue-vex.md`: 144 lines, tracked at HEAD;
  header trio `source: S057 — …` / `verified-at: 2026-10-26 …` / `recheck: cd … && python3 corpus/instruments/source-recheck.py …` plus `ground: F22`; body far exceeds
  10 lines beyond the provenance trio (10 claims, falsifiable rule, FC-1..FC-6, 8
  rejected over-generalizations, honest limits). Q1–Q6 spot-check: header trio present
  (Q1); sole support is tier-A S057 opened in the admitting round (Q2); quotes carry
  line locations (Q3); "CISA guidance, not a standard" + "Lane reading, not a quote"
  labels (Q4); falsifiable rule + rejected over-generalizations (Q5); documentation-only
  (Q6).
- **Capture committed and bound**: `git ls-files` lists
  `corpus/source-snapshots/round-39/S057.txt` and `manifest.json`; HEAD bytes ==
  working-tree bytes; S057.txt sha256 `11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f`
  == manifest pin; manifest.json sha256 `432f2205b368acb39d620bb85fe81c0fd6ccb345dd0878661478085ac1ce6659`
  == the seat-manifest sha recorded in the committed junk-f22-recheck.txt; 275 lines /
  17971 bytes as the entry and manifest state.

## 3. Independent upstream verification (attack-grade, beyond the frozen set)

- **Re-fetch** of the manifest's `capture_url`
  `https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf`
  with `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`: HTTP **200**, **235270**
  bytes, fetched **2026-10-26T20:16:29Z**; sha256
  `cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99` — byte-identical
  to the manifest's `raw_sha256`. The upstream document has not changed since the
  19:30:55Z capture.
- **Re-derivation** of the committed capture from the freshly fetched PDF
  (`pdftotext -enc UTF-8` + the instrument's `collapse()`: CRLF→LF, space/tab/NBSP
  runs collapsed, trim, blank lines dropped, final newline):
  `derived_bytes=17971 derived_sha256=11c8d6d6…` vs committed
  `committed_bytes=17971 committed_sha256=11c8d6d6…` → **BYTE-IDENTICAL**. The full
  chain live-PDF → pdftotext → collapse → committed S057.txt reproduces exactly.
- **Line-citation spot-check** of the entry against the capture: L12-14 (business
  decision), L79-81 ("not determined by a strict protocol"), L132-138
  (under_investigation lifecycle + timestamp reaffirmation), L184-191 (inheritance
  caution + two-label allowance + re-introduction exception), L219-227 (open source,
  absence-of-VEX), L170 ("VEX users choose the most appropriate tools for their
  ecosystems.") — every cited span sits on its declared lines.
- **Instrument bytes**: `source-recheck.py` sha256 `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`
  == the pin in the committed junk-f22-recheck.txt, so the bytes I executed are the
  bytes wave 1 recorded. Instruments changed base→HEAD: only
  `corpus/instruments/knowledge-expected.txt` (50→51 entries) and the new
  `r39-closure.sh` — no existing instrument was modified.

## 4. Do-nothing controls: before-state reproduced over the base export

`git archive 480b1a505a2dfc14a4f718d16d63808247214d0a` extracted to my scratch; grep
counters run on the export bytes; the three instruments run with `--root <export>`
(after re-targeting the exported entries' `cd <lane>` prefixes to the export dir so
every executed input is base bytes). All match `.ufo/waves/round-39/c2-controls/before.txt`:

| counter | base measured | before.txt frozen | HEAD measured |
|---|---|---|---|
| frontier rows | 21 | 21 | 22 |
| registry rows | 55 | 55 | 59 |
| S057 citations | 0 | 0 | 1 |
| knowledge files | 50 | 50 | 51 |
| harness | `entries=24 pass=24 exit=0` | same | `entries=25 pass=25 exit=0` |
| binding | `records=45 bound=45 unbound=0` | same | `records=46 bound=46 unbound=0` |
| audit | `expect=present expected=50 missing=0 unexpected=0 exit=0` | same | `expected=51 missing=0 unexpected=0 exit=0` |
| census (base `validate --file`) | exit 0, same two W04s | — | exit 0, same two W04s |

Every counter moves between base and HEAD in the claimed direction and magnitude —
the C2 counters are non-vacuous under the E5 semantics, and the before-controls are
honest.

## 5. Kill-rule sweep (C2)

frontier rows = 22 ✓; S057 row present, NF=13 ✓; S056/S058/S059 present as rejected
rows with flip ✓; entry present and Q1–Q6 spot-pass ✓; harness 25/25 exit 0 ✓;
source-recheck S057 exit 0 ✓; binding 46/46 ✓; audit expected=51 missing=0
unexpected=0 ✓; census exit 0 with no new W/E code ✓; junk-f22 rejected (exit 1) ✓;
capture + manifest committed and bound ✓. **No kill finding.**

## 6. Residual risk / verification gaps

- I spot-checked 6 of the entry's ~22 declared line ranges by eye plus the 4
  manifest-pinned quotes through the instrument; the remaining FC-1 spans were not
  individually re-derived (the instrument's anchor verification and my byte-exact
  capture re-derivation bound this risk).
- The base-export instrument runs execute the exported entries' recheck lines against
  base bytes only because I re-targeted the `cd` prefix in my scratch copy; the grep
  counters at base are byte-exact from `git archive` without modification.
- The census `multi_row_url=2` and `orphan=S040-live.txt` are pre-existing facts,
  identical at base and HEAD; not C2-relevant.

## 7. Tooling and environment record

- No tool installed or upgraded. `pdftotext` (poppler 26.08.0) already present at
  `/usr/bin/pdftotext`; system `curl` used for the one network fetch (recorded in §3).
  No pacman run. Scratch `/fast/scratch/hyaku/kasegi-r39/RevC2Recheck/` removed before
  yield; only this receipt was written in the lane tree.

Report: .ufo/waves/round-39/wave2/RevC2Recheck.md
