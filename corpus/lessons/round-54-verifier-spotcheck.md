author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

# kasegi round 54 — non-author closure spot-check

Closed against lane tip `5108584aab38a1919992c46d0224f6ec1cb59363` (branch `master`), base
`32782bd6b564f80454af853b38868603a4140e79`. Verdict: **both claims verify, admitted=true, no axis
harmed**. Two status-neutral conformance defects found (DF-1, DF-2 below); they do not bar
admission. All commands below were run by the closure judge at the lane tip unless noted.

## 1. Step-1 conformance

| Check | Result |
|---|---|
| Report committed in fleet repo by lane identity | PASS — `git log --format='%an %ae %H' -1 -- .ufo/reports/round-54/kasegi.md` → `kasegi-shokunin kasegi@shokunin.local 3dce3dc1d5e2bae232821b80560a3a2e965a8094` |
| `SHONEN` heading in report | PASS — `## SHONEN` with one line per box: `[~]` box 1, `[ ]` box 2, `[~]` box 3, `[~]` box 4. No `[x]` written by the author (non-author gate preserved). SHONEN.md itself untouched in the range. |
| Cited lane commits exist and are ancestors of master | PASS — `git merge-base --is-ancestor` ok for `37fc40e`, `cfdf059`, `c9df68e`, `ff5a1bf`, `739215a`, `5108584aab38` |
| Branch tip pushed | PASS — local `refs/heads/master` = `5108584aab38a1919992c46d0224f6ec1cb59363` = `git ls-remote origin refs/heads/master` |
| Round work inside `32782bd6b564..5108584aab38` | PASS — exactly the six cited commits; every cited work item traces to one of them |
| Lane commit identity | PASS — all six round commits authored `kasegi-shokunin <kasegi@shokunin.local>` |
| Report is a real report, not a marker | PASS — substantive work, evidence pointers, commit hashes throughout |

## 2. Claim C1 — depth:verifiability 4 held, capability acquisition `move-log-figure-audit` (RE-MEASURED by the closure judge)

Every predicate was re-run live at the tip; all reproduce.

| Predicate | Committed receipt | Judge re-run | Match |
|---|---|---|---|
| `python corpus/instruments/figure-audit.py --selftest` | `controls/c1-selftest-r54.txt`: `cases=5 failures=0`, EXIT=0 | `cases=5 failures=0`, SELFTEST-EXIT=0 (incl. token-boundary 34-vs-340 and unreadable-ledger exit 2) | YES |
| Red control over the two r53 literals AS FILED (`--ledger .ufo/waves/round-54/controls/red-d53-ledger.json`) | `controls/c1-red-d53literals-r54.txt`: 2 stale (34→33, 543→542), EXIT=1 | `FIGURE-AUDIT figures=2 ok=0 stale=2 exit=1`, RED-EXIT=1 — **the routed D53 number-drift class is machine-catchable** | YES |
| Green audit at lane root | `controls/c1-green-lane-r54.txt`: `figures=9 ok=9 stale=0 exit=0` | `FIGURE-AUDIT figures=9 ok=9 stale=0 exit=0`, GREEN-EXIT=0 (ledger entries 1–6 rev-pinned to 32782bd; 7–8 read the freeze capture; 9 re-runs the live counter) | YES |
| Do-nothing at base: instrument absent | `controls/c1-donothing-r54.txt`: `git cat-file -e` exit 128 | judge re-run: `fatal: path … exists on disk, but not in '32782bd'`, CATFILE-EXIT=128 | YES |
| Freeze integrity | `freeze.txt` pins `claims-sha256=f2dd143e…` | `sha256sum .ufo/waves/round-54/claims.json` → `f2dd143e63d0cc458c09c4e35480fd200c24c8611d0c6584a8a37252064236c9` | YES |

The instrument itself was read by the judge: whole-value comparison (never substring), fail-closed
on nonzero derive exit or empty stdout, read-only allow-list on derive heads, exit codes
0/1/2 as declared. Score HELD at 4 with the non-moving metric named (R58 nominal labeling) —
honest labeling, no score inflation.

### DF-1 (defect, status-neutral — number drift in report/freeze prose, contradicted by the lane's own receipt)

The report ("exit 128 and **0 mentions** in base SCORECARD/LOG/knowledge-expected") and the frozen
C1 sentence ("'figure-audit' appears **0 times in the base SCORECARD.md**") contradict the committed
do-nothing receipt they cite: `git show 32782bd:SCORECARD.md | grep -c 'figure-audit'` prints **2**
(SCORECARD.md:2102 and :2158 — the r52-planned / r53-routed "figure-audit sibling" text, i.e. the
defect routing that demanded this instrument, not a pre-existing capability). LOG.md and
knowledge-expected.txt are indeed 0. The substantive do-nothing claim (capability absent at base)
verifies; the prose count is wrong in two filed artifacts. Ironic class: this is exactly the
D53 number-drift family the round machine-catchable. Route: next round's report carries the
erratum; optionally a figure-audit ledger entry pinning the do-nothing receipt's mention counts.

## 3. Claim C2 — coverage 8 held, frontier F34 → F35 on S086 (RE-MEASURED; source re-opened LIVE by the closure judge)

| Predicate | Committed receipt | Judge re-run | Match |
|---|---|---|---|
| 14 exactly-once assertions + capture digest | `controls/s086-recheck-r54.txt`: sha256 OK + Q1–Q14 `occurrences=1 anchor=N-ok`, EXIT=0 | judge re-run `python corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-54/manifest.json --source S086` → identical 15 OK lines, RECHECK-EXIT=0 | YES |
| **Live re-open of the source** | manifest: fetched 2026-11-01T08:17:52Z, HTTP 200, sha256 `fa84a017…` | judge `curl` of `https://raw.githubusercontent.com/ossf/scorecard/main/docs/checks.md` → **HTTP 200, sha256 `fa84a01753971589571c22597d5b7f65ed34dc373dfc466d2233437faf4dc81f`, 731 lines, 46441 bytes — byte-identical to the committed capture** | YES |
| Two byte-identical opens claim | Gate/entry/claims assert two opens this round, both sha `fa84a017…` | the *recorded* open is receipt- and pin-backed and the judge's independent re-open is byte-identical (a third open, same sha); the *first* open's sha is lane-attested with no separate committed receipt — verified to the extent checkable, noted, not a defect | YES (with note) |
| Capture binding 68 → 69 | `controls/capture-binding-r54.txt`: `records=69 bound=69 unbound=0`, EXIT=0, `multi_row_url=7` | judge re-run: `AUDIT records=69 with_url=69 … multi_row_url=7 …`, `records=69 bound=69 unbound=0`, BINDING-EXIT=0; before-value 68 = the receipt's own per-round sum (68 + round-54's 1) | YES |
| Counter before→after | do-nothing (base export): `rows=34 admitted=34 closed=4 problem-rows=30 registry=85`, `entries=37 pass=4`, 0 F35 lines, 33 FAIL records → final: `rows=35 admitted=35 closed=5 problem-rows=30 registry=86`, `FRONTIER-PASS F35 ids=S086`, `entries=38 pass=5`, FAIL 33 | judge re-run at tip: line-identical to the final receipt (`rows=35 … registry=86`, F35 PASS, `entries=38 pass=5`, 33 FAIL records = 38−5 invariant); counter exit 1 is the standing disclosed host-bound class, unchanged | YES |
| Plain counts | report: registry 85→86, knowledge 72→73, knowledge-expected 72→73 | judge: `grep -cE '^\|…S[0-9]{3,}…\|'` → 85 at base, 86 at tip; `grep -c '^corpus/knowledge/' knowledge-expected.txt` → 72→73; `ls corpus/knowledge/*.md | wc -l` → 72→73; SOURCES diff +3/−0, README +26/−0, PROVINCE +2/−0 (pure appends) | YES |
| Entry quality | `corpus/knowledge/openssf-scorecard-checks.md` | provenance trio present (source/verified-at/recheck); 4 falsifiable rules each with located quotes and rejected over-generalizations; distinctness vs F24/F17/F31/F18 argued from the neighbor screen; honest Limits (aggregate/weights/publisher/Prox unasserted; moving `main` pinned by sha) | YES |

Neighbor screen (pre-freeze, at base): receipt present in the freeze commit; the 'scorecard' hits it
shows are SCORECARD.md-filename strings and the OSV entry's foundation naming — no held README/
PROVINCE row, no snapshot consumer; only S086.txt + manifest.json landed under
`corpus/source-snapshots/round-54/` (diff-tree verified). First admission of the recorded lead:
PASS.

## 4. Routed D53 corrections (carry-in, non-claim) — both defects closed, no filed byte edited

- The judge ran the corrections file's own closure check verbatim from the lane root →
  `d53-corrections=closed`, exit 0 (both superseded literals named; receipt sha `be69ece7…`,
  capture sha `4d1c4e77…`, r53-manifest sha `eb6ffa60…` all verified against the live files).
- No filed byte edited: `git diff-tree -r 32782bd6b564 5108584aab38` over `.ufo/waves/round-53/`,
  `corpus/source-snapshots/round-53/`, and `corpus/knowledge/nvd-api-2.0-response-schema.md` is
  EMPTY; the SOURCES diff is +3/−0 (the new S086 row only); the nvd entry sha is byte-identical
  base→tip (`15eb2d05…`).
- Filed literals confirmed at base, each exactly once: manifest `"lines": 543` ×1, S085 row
  "543 lines" ×1, F34 header "543 lines" ×1, receipt "34 inherited" ×1; measured 542/33 confirmed
  by the closure check and the C1 red control.
- D53-3 (prompt-template L2-embed omission) is operator-side and standing: the L0 row exists
  (`.ufo/l0-questions.md` line 246, kasegi | round-54), non-blocking, correctly never treated as
  answered.

### DF-2 (defect, status-neutral — cited evidence pointer does not resolve)

`d53-base-greps-r54.txt` is cited by the corrections file (its header AND D53-2's disposition),
the LOG round-54 entry, the SCORECARD round-54 section, and the report's landed-changes table
(cfdf059: "… + `d53-base-greps-r54.txt`") — but it was **never committed**: absent at `cfdf059`,
at the freeze, at the tip, and in `git log --all -- <path>`. The substance survives independent of
the missing file: all four pins it carried re-derive true from base bytes (judge-verified:
SOURCES@base `06c92e6a…`, nvd entry@base `15eb2d05…` = tip, manifest `eb6ffa60…` and capture
`4d1c4e77…` pinned by the closure check), and the four filed literals each appear exactly once at
base. Route: commit the before-state receipt (or a regenerated equivalent naming the same pins)
in round 55 so every citation resolves; an evidence pointer must resolve at closure time.

## 5. Discernment spot-check (non-author)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| Admit S086 — OpenSSF Scorecard check documentation (the round's only new row) | admit | Live URL re-fetched by the judge: HTTP 200, sha `fa84a017…` byte-identical to the committed capture; `source-recheck --source S086` exit 0 (14/14 exactly-once at pinned anchors); Gate quote at S086.txt:415 re-read: "week during the previous 90 days, the project receives the highest score." = 12 words by `wc -w`, inside the ≤25-word rule | **agree** | First-party generated documentation (tier A docs is the right scope); entry grounded, falsifiable, with rejected over-generalizations; distinctness screen held (only one capture landed) |
| Reject-side: Gate records "Rejections this round: none — the bounded hunt opened exactly the recorded lead" | disposition | Base SOURCES.md:140 shows the CISA ADP list page as "not opened this round; lead, not row"; registry delta is exactly +1 row (S086); `corpus/source-snapshots/round-54/` contains only S086.txt + manifest.json | **agree** | The none-reject disposition is honest: one bounded hunt, one opened source, no unopened surface rowed; the hunt trail (round-53 SCORECARD planned-for-53) resolves |

Newly written SOURCES.md row re-opened (duty): S086 — done above, including the located quote.
Fleet census (the operator-side validator, run by the judge):
`bash scripts/sources-census.sh validate --root <fleet root> kasegi` → **exit 0**, the same 6
informational W04 duplicate-URL rows the report discloses (S028/S029/S072/S076/S080/S085). The
E01 catch-and-fix re-derives: the S086 row at `ff5a1bf` carries 12 fields, at the tip 11 — the
sixth Mistakes row is grounded.

## 6. Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| depth:verifiability | **improved** | C1 capability acquisition verifies end-to-end (selftest 5/0, red 2-stale exit 1, green 9/9 — all judge re-run); the repertoire gains `move-log-figure-audit`; score honestly HELD at 4 (nominal, R58) |
| depth:density | **unchanged** | SKILL.md untouched in the range (diff empty; non-target guard held); density 9 assertion stands outside this round |
| coverage | **improved** | F35 admitted on a live first-party source; frontier 34→35, registry 85→86, knowledge 72→73 — all judge re-derived; score honestly HELD at 8 (operator-owned denominator, disclosed) |
| calibration | **improved** (verdict-only row) | Six Mistakes rows with class/captured-by/fix; three own-catches landed before their data; the E01 12→11 fix re-derived by the judge; corrections landed append-only with byte pins (closure check exit 0); DF-1's prose drift is the one new number-drift instance and is itself of the class the round now machine-catches |

No owned axis harmed: the SCORECARD diff contains only the round-54 section (holds, verdict rows,
move log, capabilities row, planned-for-55); no score decreased; no entry failed a re-check.

## 7. Trend verdicts (closure judge, evidence-checked)

- **expansion: improved** — frontier 34→35 (F35 admitted on a first-party source the judge
  re-opened live, byte-identical), registry 85→86, knowledge 72→73; the F35 entry's `used-by`
  binding holds (S086 status `mined`, cites the entry).
- **quality: improved** — no admitted entry failed a re-check (F31–F35 all PASS in the judge's
  counter run; S086 recheck exit 0); the new instrument carries selftest+red+green, all reproduced;
  the one new defect class (registry row shape) was caught by the round-end gate and mined the
  same round (E01 12→11, judge re-derived).
- **discernment: improved** — the carry-in landed append-only with byte pins and a runnable closure
  check (exit 0); own-catches documented pre-data with receipts; the judge's spot-check agrees with
  the Gate on the admit and on the none-reject disposition.

## 8. Notes for the operator / next round

- Standing, unchanged, operator-owned (L0 kasegi round-50/46 + round-54 row): the 30 problem-rows /
  33 host-bound FAIL entry records behind the counter's exit 1; the 67 `cd /home/...` recheck
  lines; D53-3 prompt-template L2-embed omission. All disclosed; routed around, never treated as
  answered.
- SHONEN.md: all four boxes carry author marks only (`[~]`×3, `[ ]`×1) — correct form; box 2
  (end-to-end domain task) remains open and is only checkable by a non-author promotion review.
  No `[x]` written anywhere; the judge did not write SHONEN.md.
- Defects for the lane's round 55: DF-2 (commit the missing `d53-base-greps-r54.txt` or an
  equivalent naming the same pins) and DF-1 (erratum for the "0 mentions in base SCORECARD" prose;
  receipt says 2). Both status-neutral; neither bars this round's admission.
- The capture-binding before-value (68) rests on the receipt's own per-round summation, not a
  dedicated base receipt — fine, but a one-line base run in a future receipt would close it
  completely.
