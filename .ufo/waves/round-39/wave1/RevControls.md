# RevControls — round-39 frozen-controls verification (receipt-only, no deliverables)

Seat: RevControls-2 (leaf) · 2026-10-26 · Lane: kasegi-shokunin
Item: verify the frozen controls are honest and match the base measurements; verdict controls-conformant / defect-named.
Scratch: /fast/scratch/hyaku/kasegi-r39/RevControls-2 (removed before yield). Disk guard at start: green (/fast/scratch/hyaku 25% use). No tools installed (pdftotext/pdfinfo/curl already present; pacman never touched).

## Method / provenance

- Base export: `git -C <lane> archive 480b1a505a2dfc14a4f718d16d63808247214d0a | tar -x -C $S/base` (both base and freeze commit dcd3170 exist as commits; `git cat-file -t` = commit).
- `git diff --stat 480b1a5 HEAD -- corpus/` is EMPTY and `cmp $S/base/corpus/SOURCES.md <lane>/corpus/SOURCES.md` passes: corpus bytes at tip d65d823 are identical to base (base..HEAD adds only 12 `.ufo/waves/round-39/*` files, 2396 insertions). So instrument runs inside the real lane reproduce base measurements exactly.
- Controls read: claims.json, c1-controls/before.txt, c2-controls/before.txt, census-before.txt, c2-controls/junk-f22.md — all present at dcd3170+.

## C2 before-values re-run (expected = c2-controls/before.txt)

| # | Command (at base) | Expected | Got | Verdict |
|---|---|---|---|---|
| 1 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 21 | 21 | match |
| 2 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 55 | 55 | match |
| 3 | `grep -rlE '^source: S057' corpus/knowledge \| wc -l` | 0 | 0 (also `grep -c S057 corpus/SOURCES.md` = 0) | match |
| 4 | `python3 corpus/instruments/frontier-recheck-count.py` | entries=24 pass=24 exit=0 | entries=24 pass=24 exit=0; last PASS line `F21 knowledge/csaf-vex-product-status-and-justifications.md ids=S055` identical | match |
| 5 | `python3 corpus/instruments/capture-binding-check.py` | records=45 bound=45 unbound=0 | AUDIT line byte-identical incl. `multi_row_url=2 orphans=1 orphan=S040-live.txt`; records=45 bound=45 unbound=0 | match |
| 6 | `python3 corpus/instruments/recheck-audit.py --quiet` | expect=present expected=50 missing=0 unexpected=0 exit=0 | in-lane run: `strict pass=50/50 cdroot_fail=0`, `expected=50 missing=0 unexpected=0 exit=0`; `--selftest` exit=0 | match |
| 7 | `ls corpus/knowledge/*.md \| wc -l` | 50 | 50 | match |
| 8 | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | W04 S028 + W04 S029 only, ok, exit=0 | all three lines byte-identical to census-before.txt, exit=0 | match |

Note on #6 (investigated, not a defect): run from a `.git`-less `git archive` export the audit prints `strict pass=1/50 cdroot_fail=49 … exit=1` while still reporting `expected=50 missing=0 unexpected=0`. Cause is documented instrument behavior — `--cdroot` "defaults to --root", and the corpus recheck lines `cd` into the absolute lane root, which an archive export cannot satisfy. Re-run in the real lane (corpus == base bytes) reproduces before.txt exactly. `--selftest` exits 0.

C1 before spot-check: `corpus/instruments/r39-closure.sh` absent at base (`ls` exit 2) — matches before.txt line 1.

## Junk twin vs live CISA When-to-Issue text

Fetches (curl -sS -L --max-time 90 -A kasegi-shokunin/1.0):
- Page https://www.cisa.gov/resources-tools/resources/when-issue-vex-information → HTTP 200, 54453 bytes, 2026-10-26T19:32:38Z; `<title>When to Issue VEX Information | CISA</title>`.
- PDF https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf → HTTP 200, 235270 bytes, application/pdf, 2026-10-26T19:34:07Z. pdfinfo: Title "When to Issue VEX Information", 9 pages, created 2023-11-02; text header TLP:CLEAR, "Publication date: November 2023". pdftotext -layout: 400 lines / 19718 bytes.

Full-claim greps on whitespace-joined live text — ALL 0 hits, as required:
- `mandates a strict protocol` = 0 (claim 1)
- `must never be changed` = 0 (claim 2)
- `defines the five not-affected justification labels` = 0 (claim 3)
- `exploitation-likelihood` = 0, `is mandatory` = 0, `requires every VEX statement` = 0 (claim 4)

The doc's own wording actively refutes each junk claim (verified in context):
- L129–130: "The decisions and timing around providing VEX information are primarily business decisions and are not determined by a strict protocol." (the contiguous grep `strict protocol` = 0 only because pdftotext wraps the line; joined-text shows the words solely inside this negation — "not determined by a strict protocol" = 1 hit).
- Labels: `component_not_present` and `vulnerable_code_not_present` hit once each, only in the inheritance passage L291–295 ("a VEX status of 'not_affected' with justification 'component_not_present' or 'vulnerable_code_not_present' could be inherited downstream…") — exactly the citation junk-f22.md itself anticipates ("cites them only in the inheritance discussion"); the other three labels (`vulnerable_code_not_in_execute_path`, `vulnerable_code_cannot_be_controlled_by_adversary`, `inline_mitigations_already_exist`) = 0 hits, so the doc does not define the five labels.
- L190–192: "VEX does not specifically describe threat or the degree to which a vulnerability is being exploited, however, such information could be included in the 'action_statement' field." — optional, not mandatory ("could be included in the" = 1 hit).
- Positive anchors confirming the live text is the genuine document: "When to Issue" ×3, "business decision" ×2, "not_affected" ×3, "reaffirm" ×1, "action_statement" ×2.

## Verdict

**Controls conformant.** Every C2 before-value (frontier 21, registry 55, S057 0, knowledge 50, harness 24/24 exit=0, binding 45/45, audit expected=50 exit=0, census W04 S028/S029-only exit=0) reproduces from the base tree, and every junk-f22 claim is genuinely absent from the live CISA document. No defect named.

Residual risk / verification gaps:
- C1 before.txt lines R2/R3/R4/R5 (R2 correction grep counts over lessons/LOG/SCORECARD/SHONEN, R3 transcript absence, R4 criteria counts, R5 25 surviving r38 mutants) are historical records I did not independently re-execute (r38-suite mutant run out of item scope); the checkable absence claim (r39-closure.sh) is verified.
- Junk absence is proven against the canonical live PDF fetched 2026-10-26; the committed capture `corpus/source-snapshots/round-39/S057.txt` was not yet in the tree at verification time (wave1 in flight), so capture-vs-claims rejection (source-recheck MISMATCH ×4) remains the Sentinel seat's check, not duplicated here.
