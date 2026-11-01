# Round 53 — the routed D1 equality-limb repair (C1), the NVD API 2.0 response schema (C2), and the routed D2 wording fix

Two declared claims, frozen in `.ufo/waves/round-53/claims.json` at base `e276dbf6255e0cea5e70456aada7e59e971f5853`
(freeze commit `23448a2`) before implementation: C1 on depth:verifiability (the lane's lowest non-retired axis, score 4 —
instrument repair: the recheck-audit expected-list equality limb's Windows separator artifact fixed POSIX-preserving, the
committed expected list synced with the two entries the round-52 closure routed, and a committed Windows-separator fixture
pinning the behavior red-before/green-after), C2 on coverage (frontier F34 = the NVD Vulnerability Data API 2.0 response
schema document on S085, re-opening the rejected S066 row under the unspent term of its own flip). The r52 closure's D2
observation (the erratum's "filed before the implementation" wording) landed as a routed non-claim one-line append-only
correction in its own commit (`d9710d2`). Host unchanged from rounds 50-52 (Windows workspace, `python` 3.13.15, `python3`
= Microsoft Store stub, no /home, no /fast). The carry-in was addressed first: the equality limb's base state was receipted
at the freeze (`expected=69 missing=69 unexpected=71` plus the selftest crash — `controls/c1-donothing-r53.txt`), the D2
base greps taken (1 filed / 0 marker — `controls/d2-base-greps-r53.txt`), and the S085 capture + extended pre-freeze
neighbor screen landed in the freeze commit itself.

## Mistakes

Sweep that found them (paste, per contract): the round's own receipt runs, each before the state it
concerns was committed — (a) the first frontier-counter run over the DRAFT F34 entry printed
`FRONTIER-FAIL F34 ... problems=missing-pass-line` twice and `entries=37 pass=3` where `pass=4` was
expected; (b) the first appended D2 erratum line QUOTED the phrase its frozen counter greps for,
moving `grep -c "Filed BEFORE the implementation commit"` from 1 to 2 against the frozen "stays 1",
caught by re-running the counter before committing; (c) the frozen C1/C2 after-literals were checked
against the landed receipts after the freeze and two disagreed — `total=14` vs the printed
`total=15`, and `34 inherited FAIL records` vs the 33 both cited controls printed — filed as
`claims-erratum-1.md` before the results landed; (d) reading the committed receipts back showed the
C2 counter-final footer had first been written with the draft-run's numbers (34) and was rewritten
from the landed run's captured raw output; and (e) the limb-mutation replay (`limb-mutation-check.py`)
reads `invalid:live-baseline` on every row here because its kill commands require a `python3` that
exists — disclosed host-bound, not fixed (see Limits).

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| declaration-shape leakage: prose list item starting with an S-id parses as a source declaration | first counter run over the draft entry: `FRONTIER-FAIL F34 ... problems=missing-pass-line`, `ids=S066,S085` (the Limits bullet "- S066 (the rejected row for this URL) ..." matched `frontier-recheck-count.py` EVIDENCE_LINE `^(?:[-*]|\\d+[.)])\\s+(S\\d{3,})\\b`), adding S066 to the declared set the recheck must cover; raw run quoted in `controls/c2-counter-final-r53.txt` landing note | the frontier counter's own limb A (header-sources-not-rechecked), working as designed — this is the same limb that the round-46 wave found seven false-greens with, here firing on the author's own draft | reworded the bullet so no list item begins with an S-id ("The rejected round-42 row for this URL (S066) stays byte-identical ..."); the counter then prints `FRONTIER-PASS F34 ids=S085` over the shipped bytes; entry-writing rule going forward: an entry's list items never begin with an S-id unless that source is declared and rechecked |
| self-referential quote in a correction breaks an unanchored whole-phrase counter | the first D2 append contained the verbatim phrase its frozen counter greps (`grep -c "Filed BEFORE the implementation commit"` → 2 against the frozen "stays 1"); caught by re-running the counter before committing (nothing was pushed) | the frozen D2 counter itself, run before commit | reworded the correction to refer to the sentence without quoting it ("the opening sentence claiming this erratum was filed before the implementation commit"); counts then read 1 filed / 1 marker as frozen; rule: a correction never quotes a counter's literal — refer, don't reproduce |
| frozen after-literals derived by arithmetic instead of dry-run (R25 applied only to the state literals) | C1: frozen `total=14` vs receipt `total=15` (the selftest's separately pre-written `target.md` missed: 13 cases + missing-line + target = 15); C2: frozen `34 inherited FAIL records` vs `entries=37 pass=4` = 33, the figure BOTH cited controls printed (do-nothing footer and final receipt) — the frozen sentence contradicted its own control in the R43 shape, after side | the receipts the frozen sentences themselves cite (read back after landing, before the results landed) | `claims-erratum-1.md` (freeze rev 1b) supersedes both literals with the controls' figures, filed before the SCORECARD/LOG results; next round: dry-run EVERY numeric literal in expect_after against a stand-in tree, not only the headline state figures |
| receipt composed before the run it describes (draft-run numbers left in a footer) | the first `c2-counter-final-r53.txt` build quoted the draft-run's `34` in its footer while the landed run printed 33 | re-reading the receipt against the captured raw output of the landed run (R39: a receipt is the unedited tee of one observed run) | receipt rebuilt from the landed run's raw output; the draft-run episode is recorded inside the receipt itself as the landing note |
| inherited, disclosed here: the limb-mutation replay is host-bound on this workspace | `python -I corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json` → every row `invalid:live-baseline` (kill commands run `python3 {inst}`; `python3` is the Store stub, exit 49, so the live baseline cannot reach the ledger's `live_exit: 0`) | the round-53 C1 receipt work, which wanted R17 replay evidence for the repaired limb | NOT fixed (out of D1's scope; the harness's ledger-validation rule requires the `python3` shape); disclosed beside the 67 host-bound recheck lines as operator-owned debt; the C1 kill rests on the semantic red/green pair instead: the pre-repair bytes fail the fixture's exact scenario (`controls/c1-fixture-red-r53.txt` driver: `missing=['corpus/knowledge/good.md'] unexpected=['corpus\\knowledge\\good.md']`) while the repaired selftest case reads exit=0 0/0, and the r31 ledger's RA-expect find tokens stay exactly-once so a future POSIX-host replay stays byte-valid |

## Gate

- S085 — https://csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema — access date 2026-11-01;
  fetched 2026-11-01T06:16:10Z, HTTP 200, 10394 raw bytes (the same count the r42 S066 screen
  recorded), sha256 4d1c4e7732e128750a00557b0f16e69f021d2d5d25e2f55dfe8a9d5faa9a44d2, capture
  `corpus/source-snapshots/round-53/S085.txt` (543 lines, 7590 bytes), manifest with 13 exactly-once
  assertions; command: `python corpus/instruments/source-recheck.py --manifest
  corpus/source-snapshots/round-53/manifest.json --source S085` → sha256 OK + 13 Q-OK lines, exit 0
  (`controls/s085-recheck-r53.txt`). Located quote (9 words by `wc -w`, R56): "Metric scores for a
  vulnerability as found on NVD." at S085.txt:96.
- Rejections this round: none — the round's source hunt opened exactly the deferred artifact
  (S085, mined); the two other planned-for-53 leads (OpenSSF Scorecard, CISA ADP list page) were
  NOT opened and are recorded as Leads in `corpus/SOURCES.md` (lead, not row — R64 does not apply
  to unopened surfaces).
- Extended pre-freeze screen (the r51-closure downstream-consumer sweep included):
  `controls/neighbor-screen-r53.txt` — the schema URL named only by the rejected S066 row and the
  r42 lesson records of that screen; mirror-field names only in F33's Limits disclaimer; zero
  consumers across corpus/source-snapshots/.

## Limits

- The equality limb's green is stated beside the audit's overall exit 1: the 67 host-bound recheck
  lines (cd into the old Linux lane root) and `cwd_fail=3` are operator-owned disclosed debt
  (L0 kasegi round-50/46 unanswered, routed around, no portability rewrite) — the round shows the
  limb green, not the whole audit.
- The limb-mutation replay stays host-bound (Mistakes, item 5): R17-style replay evidence for the
  repaired limb is replaced by the committed semantic red/green pair plus the preserved ledger find
  tokens; a future POSIX host must re-derive `live_exit` values if the selftest grows.
- The census figures moved for bookkeeping reasons only (two new corpus files): the score-bearing
  claims this round are instrument repair and frontier admission; neither is claimed as a
  citation-resolution move (R58 nominal labeling on C1; the coverage score's denominator is
  operator-owned).
- F34's external schema references (cvss-v2.0/v3.0/v3.1/v4.0.json, ssvc-v2.0.3.json,
  cve_affected_1.0.json) are not captured; nothing in the entry or the F34 row asserts their content.

## Census of record at this round's tip (quoted only from the final regeneration)

The round-52 tip read 209 files / 4912 distinct; the round-53 tip is quoted in SCORECARD from the
final regeneration over the truly final tree (the two new corpus files are the F34 entry and this
lesson); the gate receipt (`controls/c1-gate-final-r53.txt`, `CENSUS-FRESH=ok`) is measured after
the last corpus edit. Internal consistency of the quoted figures is checked at regeneration time.
