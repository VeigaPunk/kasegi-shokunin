# Round 44 — Kasegi

Lane: `kasegi`; attempt 1. Round-open base: `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`. Frozen claims/wave commit: `66314015122b9aa32dc40f2f1815df56624c26d1`. Frozen claims are `.ufo/waves/round-44/claims.json`; they were not edited. C1 targets eight routed R43 defects on `depth:verifiability`; C2 targets a sourced frontier entry on `coverage`.

## Wave and result

One V2 wave (66 seats): 20 reviewers, 12 critics, 8 mutation-testers, 8 executors, 8 scouts, 5 scribes, 3 connectors, 1 revenger, and 1 simplifier. `KasegiR44` was L1 and held the planner seat; the round dispatched no separate planner seat. WAVE-DONE reported all 66 settled. `wave1-results.json` has 66 nonempty outputs; its schema has no explicit status field. Attack roles (reviewer + critic + mutation-tester) were 40/66, 60.6%. One wave, no residual call.

## Mistakes

| ID | Error | Captured by | Correction / disposition | Evidence that the correction can fail closed |
|---|---|---|---|---|
| M44-1 | The prompt's literal census invocation used the wrong root and exited 2 (`config-not-found`). | Invocation error receipt | Re-ran with the fleet root and lane name. | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` returns the two known W04 warnings, `kasegi ok`, exit 0; a missing root is still an error. Receipts: `controls/census-invocation-error.txt`, `controls/sources-census-after.txt`. |
| M44-2 | A cadence prefix placed before the F26 recheck command made the command non-executable (exit 127). | R44Scribe5 and Q5 gate review | Moved cadence after the command in the entry's `recheck:` line. | `frontier-recheck-count.py` now reports `entries=29 pass=29 exit=0`; receipt `controls/frontier-recheck-after.txt`. |
| M44-3 | Frozen C2's F-row counter assumes `admitted` is the second table cell; the control uses a different, double-escaped regex. | R44Review10, R44Critic11, R44Connector1 | Frozen claims/control bytes left unchanged. C2 is unverified; do not substitute the correct diagnostic. | The exact frozen command prints 0 in base and after; see `controls/c2-frozen-counter-replay.txt`. Correct table-aware diagnostic is separately recorded in `controls/c2-counter-audit.txt`. |
| M44-4 | Draft C1 counter accepted marker-only evidence and reported all 8 fixed with no repairs. | R44Critic1, R44Critic3, R44Critic4 | Removed the draft counter from production paths; its selftest receipt is not accepted as verification. C1 remains unverified. | `controls/r44-counter-trial-disposition.txt` documents the false-green construction; the counter trial's selftest is retained only as rejected evidence. |
| M44-5 | Initial F26 draft omitted the Q5 scope quote and did not distinguish its ground from prior general rules. | R44Scribe5 and R44Critic11 | Added Q5, the customer-IP-range rule, safe local reproduction boundary, and an explicit rejected overgeneralization; manifest and entry now cover Q1–Q5. | `source-recheck.py --manifest corpus/source-snapshots/round-44/manifest.json --source S069` passes Q1–Q5 (`controls/S069-source-recheck.txt`); frontier harness passes 29/29. |
| M44-6 | First C1 correction mislocated `closed=13/19` as the before-cell and treated prose markers as proof. | R44Critic2 | Append-only erratum now says the token is in the after-cell, the before-cell is `12/13`, and a current committed suite run at export `ab98fac9` yields `12/19`, not `13/19`. | The exact run and K17/K18 scope findings are in `wave1/R44Critic2.md:21-93`; the frozen C1 claim remains unverified. |

## Gate — frontier, source, and rejection

F26 admits only the program-specific Cloud VRP boundary, not a general authorization rule. S069 is the official Google Cloud VRP rules page, `https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules`; S070 is the general rules-directory page, `https://bughunters.google.com/about/rules/about-this-section`, rejected because its accessible body is a JavaScript shell and its metadata is only a directory welcome. The S070 rejection has a flip condition in `corpus/SOURCES.md`.

S069 was fetched 2026-10-28T18:53:38Z via the official article API (`capture_url` and `http.final_url` in the manifest); the canonical program page remains the `url` in the registry. The preserved API response is `.ufo/waves/round-44/source-recon/S069.txt`; reconstruct the pinned body with:

```sh
jq -r '.body' .ufo/waves/round-44/source-recon/S069.txt > corpus/source-snapshots/round-44/S069.txt
```

The pinned body is 45,681 bytes / 1,132 lines, SHA-256 `0932279ccba89ac0bcf5db080e910c855c9457b3e7c6b4b6038a684edf0974f2`. The manifest records the transformation inputs and Q1–Q5. A later live fetch returned formatting differences; the digest identifies the dated pin, not a claim of byte-stable live responses.

Located rules:

- Q1 (S069.txt:61): “The Google Cloud VRP scope is strictly limited to Google-owned infrastructure and services.”
- Q2 (S069.txt:62–63): customer-resource testing is prohibited.
- Q3 (S069.txt:70–72): a report is ineligible for a reward if finding or verifying it involved testing/accessing customer resources.
- Q4 (S069.txt:76–77): finding a Google-owned asset inside a customer IP block during a broad scan is still unauthorized testing within customer space.
- Q5 (S069.txt:10–11): a product or web service handling reasonably sensitive user data is intended to be in scope.

The knowledge entry preserves the Cloud VRP-specific limits, distinguishes scope from permission, and records the safe local-reproduction path for unsafe multi-tenant cases. Its novel ground is the customer IP-range boundary and non-live multi-tenant reproduction, not the general distinctions already in F03/F09/F13/F01. The rejected overgeneralization is explicit: a Google-owned asset inside a customer IP range is not thereby authorized. No target testing or submission was performed.

SOURCES rows moved 68→70: S069 (tier A, mined) and S070 (tier C, rejected); no pre-existing status/recheck/used-by cell changed. Frontier rows 25→26; knowledge files 62→63. Auxiliary gate results: source recheck Q1–Q5 pass; capture binding `records=58 bound=58 unbound=0`; recheck audit `63/63`; frontier recheck `entries=29 pass=29`; census `W04 S028`, `W04 S029`, `kasegi ok`, exit 0. These validate the pinned record and corpus shape, not the frozen C2 claim.

## C1 — depth:verifiability

Do-nothing baseline recorded eight routed defects and no round-44 correction. C1's frozen after-state is not certified: the draft counter accepted a marker-only tree and was withdrawn. `controls/r44-counter-trial-disposition.txt` explains why the apparent selftest pass is not evidence. R44Critic2 also found that the 13/19 literal is in the C1 after-cell (the before-cell says 12/13); the current committed `r43-closure.sh` run against export `ab98fac9` reports `closed=12/19 exit=1`, with K8 and K14–K19 open. The run is a seat report, not a committed `final-gates` receipt at that base. K17 skips after-cells, and K18 already treats the token as superseded from the defect prescription itself, so adding prose cannot establish closure. C1 remains unverified; no score increase.

Append-only documentation corrections include the 26-character digest-prefix correction, L1/planner and L2-floor fields in the round report, a registry correction based on dispatch names, removal of the untracked round-43 temp, restoration of SHONEN's trailing blank line, a corrected SKILL registry pointer, and the distinct missing-path measurement (`bash` at the `ab98fac9` export exits 127; the cited `ls` exits 2). These corrections are recorded in `claims-erratum-6.md`, `SCORECARD.md`, the controls, and this lesson. They are not represented as a verified 0/8 counter result. The round-43 emitter/registry issue and false-green counter scope remain unverified.

## C2 — coverage

The new F26/S069 row and entry are present in the worktree and passed their pinned-source/frontier checks. But the frozen C2 counter `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md` reads 0 at base and after because the status is the third cell. The frozen control's regex is not the same counter. The separate table-aware diagnostic yields frontier 25→26, SOURCES 68→70, knowledge 62→63; it does not replace the frozen predicate. No nonauthor admit/reject spot-check was available: the 66 seats were within the lane. C2 remains unverified; no score increase.

## Assimilation and open questions

Assimilation: none. The Kasegi merge packet was inspected read-only; no candidate fits the frozen C1/C2 scope. No `considerthese/2026-10-26.md` proposal was adopted because none matched the frozen claims. No other source was imported. Open L0 questions: none newly raised. Existing RFC 9116 cross-lane question remains parked and unchanged.

## Score and trend verdicts

Scores held: depth:verifiability 4, coverage 8, depth:density 9. Neither frozen claim is admitted; no score delta. Expansion improved (one new frontier/knowledge entry); source-quality gates pass for the pinned S069 entry, but the round's coverage claim is not certified; discernment unchanged (no nonauthor spot-check). Saturation unchanged; the lowest non-retired axis remains depth:verifiability at 4.

## SHONEN

- `[~]` Registry pointer correction: `SKILL.md` Gates & probes registry section and `wave1/R44Critic7.md`; not independently signed off.
- `[~]` End-to-end domain task: not exercised this round; no user submission or target testing (`LOG.md`, Round 44).
- `[~]` Executable instructions: the S069 pinned-source recheck and corpus checks are recorded in the round-44 controls; no nonauthor verifier.
- `[~]` Cross-domain boundary: F26 is limited to Google Cloud VRP, with source-specific limits; sibling sweep `wave1/R44Scout8.md` found no second holding. No `[x]` box.

## Attempt 2 — L1 `KasegiR44a2`: the two claims measured

The frozen claims file `.ufo/waves/round-44/claims.json` is unchanged: C1 is
still the eight routed round-43 defects and C2 is still the sourced frontier
entry. This attempt lands the repairs the attempt-1 wave only drafted, and
measures both claims with committed instruments.

### C1 — depth:verifiability (measured)

`corpus/instruments/r44-routed-defects.py` is the committed read-only counter.
One limb per routed defect of `corpus/lessons/round-43-verifier-spotcheck.md`
§6; every limb binds a committed artifact (a file that must exist and the
content that must be inside it), so a tree carrying only prose markers is
rejected. Measured against the frozen base export (`5ab3a60`, no round-44
repair present) the counter prints `routed-defects total=8 fixed=0 unresolved=8
exit=1`; against the round-44 tree it prints `routed-defects total=8 fixed=8
unresolved=0 exit=0` (receipts `controls/c1-counter-baseline.txt` and
`controls/c1-counter-after.txt`). Its own selftest builds eleven mutants — one
per limb plus the always-pass case — and prints `selftest cases=11 failures=0`:
every mutant keeps the prose marker and drops the artifact the limb binds to.

The eight repairs, all append-only: (1) the `closed=13/19` literal is
superseded by an appended `SCORECARD.md` correction that cites the erratum;
(2) the erratum `.ufo/waves/round-43/claims-erratum-6.md` is committed and
matched by K17's own `claims-erratum*` escape — the mechanism is K17's escape,
not a widened K18; (3) the lesson numeral is corrected to 26 characters with
its counting command; (4) the planner=L1 mapping and the L2-floor/residual
lines are recorded in `LOG.md`, cross-checked against the committed wave
results file; (5) the aborted-write leftover is gone, the lane-owned emitter
`corpus/instruments/wave-registry.py` refuses to emit an empty `names=`, and
the export-ref sidecar annotates the receipt that lacked it; (6) `SHONEN.md`'s
final empty line is restored; (7) the registry rows for the two round-43
instruments are appended to `corpus/instruments/README.md` and the pointer is
corrected by append; (8) the `127` and the control's `exit=2` are separated in
the erratum, and the `127` is backed by a committed measurement receipt.

### C2 — coverage (measured with a disclosed counter correction)

The frozen C2 counter string reads `0` at the base and `0` after the
admission: the frontier table's status is its third cell, so the frozen regex
measures nothing and cannot separate the two worlds
(`controls/c2-frontier-counter.txt` replays it verbatim). The counter is
defective, not the target: the declared predicate is the number of frontier
rows whose status cell is `admitted` and the declared target is 26, and both
are unchanged. `corpus/instruments/r44-frontier-count.py` measures that
predicate table-aware — 25 at the frozen base (`--expect 26` → exit 1, so a
do-nothing control cannot reach the target) and 26 at the round-44 tree (exit
0). SOURCES rows 68 → 70 (S069 `mined`, S070 `rejected`) and knowledge entries
62 → 63 carry the same movement; the source census exits 0. The non-author
admit/reject spot-check is outside the lane's authority; the packet
`.ufo/waves/round-44/nonauthor-spotcheck-packet.md` is filed for the closure.

### Mistakes

| ID | Error | Captured by | Correction / disposition | Evidence that the correction can fail closed |
|---|---|---|---|---|
| M44-7 | The attempt-1 C1 counter accepted a marker-only tree: a prose correction with no committed artifact behind it made the counter print `fixed=8 unresolved=0`. | R44Critic1's marker-only export, R44Critic3 and R44Critic4's false-positive findings (`.ufo/waves/round-44/controls/r44-counter-trial-disposition.txt`) | The draft counter was withdrawn and replaced by `corpus/instruments/r44-routed-defects.py`, in which every limb binds a committed artifact and a content token inside it; the selftest keeps the marker and removes the artifact. | Eleven graded mutants, one per limb plus the always-pass case: `selftest cases=11 failures=0`, every mutant rejected (`controls/c1-counter-after.txt`). |
| M44-8 | The frozen C2 counter string reads `0` in both the base and the after tree, so the frozen predicate was unmeasurable. | The freeze rule that a counter must be re-derived on a do-nothing control before data, and attempt-1 seat findings (`controls/c2-frozen-counter-replay.txt`; `wave1/R44Critic11.md`) | The counter was corrected to measure the same declared predicate table-aware; the target value (26) and the frozen predicate sentence are unchanged, and the frozen string stays recorded verbatim in the claims file and in the report. | The corrected counter is red at the frozen base (`frontier rows=25 admitted=25`, `--expect 26` → exit 1) and green only at the round-44 tree (`frontier rows=26 admitted=26`, exit 0). |

### Gate — admit and reject from this round's source set

- **Admit — S069, tier A, `mined`.** `https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules`, opened 2026-10-28 by this lane; located quote (≤25 words): "The Google Cloud VRP scope is strictly limited to Google-owned infrastructure and services." (`corpus/source-snapshots/round-44/S069.txt:61`). Admitted as F26, cited by `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`.
- **Reject — S070, tier C, `rejected`.** `https://bughunters.google.com/about/rules/about-this-section`, opened 2026-10-28; the accessible body is a JavaScript shell and the metadata is a directory welcome with no quotable rule. Flip condition: a readable, dated copy of the rules directory that carries a quotable rule text. No knowledge entry cites it; the row stays in the registry with its reason.

### Frontier step

Census before and after: `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kasegi` → `W04 S028`, `W04 S029`, `kasegi ok`,
exit 0 at both ends of the round (receipts `controls/sources-census-before.txt`
and `controls/sources-census-after.txt`; the attempt-1 wrong-root invocation
and its exit 2 stay as `controls/census-invocation-error.txt`). Sourced claim:
C2 rests on the S069 row opened this round. Registry rows 68 → 70 (one tier-A
`mined` admit, one tier-C reject); no pre-existing row's status, recheck or
used-by cell changed.

### Attempt-2 score and trend verdicts

Scores held: depth:verifiability 4, coverage 8, depth:density 9. Both claims
are now measured, but no score increase is claimed: the lane's scorecard keeps
its own saturation window, and the judge rules on admission. Expansion
improved (F26, S069, S070 and the two new instruments landed); quality
improved (both claims carry a committed counter and a red-before control);
discernment is unprovable-but-better in-lane only — the admit/reject
spot-check is prepared but the adjudication belongs to the non-author closure.

## Attempt 2, wave 2 — the falsify wave and what it changed

Wave 2 (one v1 wave, 40 seats: 14 reviewer, 8 critic, 6 mutation-tester,
5 executor, 3 scout, 3 connector, 1 revenger; attack share 28/40 = 70 %)
attacked the committed tree `8063547` (attempt 2's first landing). Round total:
66 + 40 = 106 seats, inside the 64–128 band. All 40 seats settled with
non-empty output; reports under `.ufo/waves/round-44/wave2/`.

### What the wave falsified, and what changed because of it

| Finding | Seat | What changed |
|---|---|---|
| The v1 counter graded a strongest-marker-only tree `fixed=8 unresolved=0` — every bound artifact had been fabricated with plausible content and no repair performed. | `wave2/R44W2Exec05.md` | The v2 counter pins the stable artifacts by sha256 (`PINS` in `corpus/instruments/r44-routed-defects.py`): a fabricated tree must reproduce the genuine bytes, i.e. do the work. A `FABRICATED-ARTIFACTS` mutant is now graded in the selftest and must be rejected. |
| Presence-only predicates accepted denials (D4), filename mentions instead of registry rows (D7), a nonfunctional emitter stub and fabricated seat names (D5), a token-only receipt (D8), a rewritten row that kept its token (D1), and D3's history check was satisfied by the correction's own quotation. | `wave2/R44W2Rev09.md` | v2 requires the affirmative `planner=L1` token and rejects denials; line-anchored README table rows plus the preserved original SHONEN bullet with the correction after it; the emitter must carry its refusal logic and the registry's `names=` list must EQUAL the committed results file's seat names; D8 digest-pins the receipt; D1 pins the row's measured cell; D3 counts only the original occurrences before the correction. |
| The K17-escape mechanism claim was wrong in substance: the `closed=13/19` token sits in the round-43 claims.json AFTER-cell, K17 skips after-cells, so its `claims-erratum*` escape never fires for that token; K18 treats the token as superseded from the spot-check's own prescription; neither check was widened. The same commit was self-contradictory (the erratum says K17 skips after-cells while the lesson asserted the K17 mechanism). | `wave2/R44W2Rev02.md`, `wave2/R44W2Revenger01.md` (D2 verdict: letter only, mechanism void) | This correction is the mechanism statement of record; limb D2 requires the lesson to carry `K17`, `after-cell` and `K18`, applies K17's own same-paragraph predicate shape to the erratum, and requires K17's wildcard glob to be able to match the erratum file. The check that sees the literal is this counter's D2 limb. |
| The round-44 export-ref sidecar carried `export-ref=ab98fac9…` — the round-43 measurement base — while the paired run receipt `.ufo/waves/round-43/final-gates/r42-at-de09313-run.txt:2` carries `export-ref=de09313e8edb98280b19767d0094bb2dd8031d73`. | `wave2/R44W2Rev09.md` | The sidecar was corrected to the run receipt's value and limb D5 now requires the sidecar's export-ref to EQUAL the paired run receipt's, so this error class is graded. |
| The stale round-43 registry (`names=` empty at `.ufo/waves/round-43/w1-REGISTRY.txt:7`) was still the only committed registry of that round; the v1 counter checked only the new one. | `wave2/R44W2Conn01.md` | `controls/round43-registry-names.txt` records the stale field as superseded (the round-43 file stays byte-identical); limb D5 requires that note. |
| `r44-frontier-count.py` would have counted a duplicated frontier row twice. | `wave2/R44W2Rev10.md` | Duplicate frontier ids are now a `DEFECT` verdict with exit 1. |
| The SCORECARD prose said "eleven marker-only mutants"; the v1 battery was ten mutants plus one positive (eleven cases). | `wave2/R44W2Crit01.md` (numeral-slip finding) | Corrected wording in the SCORECARD round-44 append: nineteen mutants plus one positive = twenty graded cases in v2. |

Not changed, with reasons: Crit01's "the report-owed sections are unfiled" is
the normal order — the report is filed last, after the lane lands; Exec01's
`recheck-audit` exit 1 was a run-context artifact (the audit ran against an
export whose recheck lines `cd` into the live lane path; the committed receipt
`controls/recheck-audit-after.txt` is 63/63 on the lane root); Rev12's Q5
locator drift (manifest anchor `:10`, entry `:10-11`, registry `:9-11`) keeps
the quote inside every cited range and is recorded here rather than rewritten;
Conn03's CLI adjacency with kaidoku's `routed-defects.py` is a distinct
basename (`r44-routed-defects.py`) and no shared receipt path.

### Mistakes (added by the falsify wave)

| ID | Error | Captured by | Correction / disposition | Evidence that the correction can fail closed |
|---|---|---|---|---|
| M44-9 | The attempt-2 export-ref sidecar stated the wrong export (`ab98fac9…`, the round-43 measurement base) for a round-42 receipt whose paired run receipt says `de09313…`. | R44W2Rev09's contradiction finding against `.ufo/waves/round-43/final-gates/r42-at-de09313-run.txt:2` | The sidecar was corrected and limb D5 now requires the sidecar's export-ref to equal the paired run receipt's, digest-pinned. | A `D5-wrong-export-ref` mutant (any other 40-hex value) is rejected by the digest pin and the equality check; see the v2 selftest receipt. |
| M44-10 | The v1 counter accepted a fully fabricated evidence tree (`fixed=8 unresolved=0` with no repair performed) and several presence-only predicates accepted denials, stubs and rewrites. | R44W2Exec05, R44W2Rev09, R44W2Rev02, R44W2Revenger01 | The v2 counter pins the stable artifacts by sha256, requires the affirmative tokens, the refusal logic, the names equality, the line-anchored rows and the ordering checks, and grades a `FABRICATED-ARTIFACTS` mutant. | The v2 selftest: twenty graded cases (nineteen mutants plus one positive), `selftest cases=20 failures=0`; the baseline export still grades `unresolved=8`. |

### D2 — the mechanism statement of record

The `closed=13/19` token sits in the AFTER-cell of the round-43
`.ufo/waves/round-43/claims.json` C1 (`claims.json:41`); K17 grades before-cell
tokens only and skips after-cells, so K17's `claims-erratum*` escape covers a
BEFORE-cell occurrence and never fires for this token (R44W2Rev02 measured
identical K17 payloads with and without the erratum). K18 treats the token as
superseded because the spot-check's own §6.1 prescribes the supersession — a
marker-bound coverage, not a fail-closed one. No check was widened. The
committed check that sees the literal is this round's counter limb D2, which
applies K17's same-paragraph predicate shape (literal + superseded vocabulary
in one paragraph) to the erratum file and requires the escape's wildcard glob
to be able to match it.

Correction (round 45, appended 2026-10-28): the S070 reject reason above (`## Gate` and the S070 row) was wrong: the S070 body is readable through the article API (`https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section`, HTTP 200, 10029 chars; re-measured by the round-45 scribe on 2026-10-28 from the API JSON `body` field; pinned as `corpus/source-snapshots/round-45/S072.txt`, sha256 `364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025`, which carries one extra trailing newline, 10030 characters), so the JavaScript-shell reason does not hold. The true reason is "overview, no program-specific rule beyond S069 Q5": the directory's Cloud VRP row says "Security issues affecting any Google Cloud product or web service that handles reasonably sensitive user data" (`corpus/source-snapshots/round-45/S072.txt:148`, located across the line break at 149), which restates S069 Q5 and adds no customer-resource rule. The S070 row stays byte-identical as history; the superseding row is S072 (status `rejected`, teaches `supersedes S070`).
