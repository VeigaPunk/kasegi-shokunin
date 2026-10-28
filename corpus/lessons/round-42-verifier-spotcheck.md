# kasegi round-42 verifier spot-check — non-author, hyaku closure

author: hyaku closure (non-author integrator, @m_zfl)
lane: kasegi-shokunin · round 42 · attempt 3 (report commit `68abb231311df19ea2f531c171eb9aec5bae56ae`)
revisions: base `5053a7f46de35784cff4b56756906e9014a38276`; judged head J `4c40ef21cced6ebed592e5622996ab41996e2da9`;
verification ref Y `b2c49ea5e7bc214e91c2b0bede5d4eaed4968572` (lane HEAD = remote `master`); round-41 judged head
`1f7464612ac4c44e39886b82e812610d3c039b13`. Date: 2026-10-28.

This seat is the non-author integrator. It did not write the round's claims, instruments, corpus rows or report.
It re-measured every in-force claim target against committed bytes, ran the falsification pass this round never
dispatched (wave 2 was rendered, validated and handed off but **never taken**: no `.ready.dispatched` marker, no
`wave2-results.json`, zero seats), and wrote only this file.

**Gate-execution disclosure.** PROTOCOL §Gate standard says the integrator verifies a gate's committed evidence and
does not execute a sibling's gate. Because this round has no adversarial wave, the closure assignment requires the
falsification pass to be carried here, so the frozen suite was executed **in export mode only** — `--export-ref`
extracts a git ref into a private work dir outside the lane (`/tmp/kasegi-r42-judge/*`), and no lane byte is
written (`git -C … status --porcelain` empty before and after). Every C1 figure below is a re-run, not a quoted
receipt line; the committed receipt was separately byte-checked against the re-run.

## 1. Step-1 conformance

| Item | Check | Result |
|---|---|---|
| report path/name | `.ufo/reports/round-42/kasegi.md` | pass |
| report attribution | `git log --format='%an %ae %cn %ce %H' -- <report>` | `kasegi-shokunin kasegi@shokunin.local` author and committer, `68abb231` — pass |
| report commit inside window | launch attempt 3 `11:09:11-03`, complete `12:22:31-03`; report authored `12:20:56-03`, committed `12:21:17-03` | pass |
| cited lane commits exist and are ancestors | 16 hashes, `git merge-base --is-ancestor <c> master` | 16/16 ancestors — pass |
| lane clean and pushed | `jj-lane.sh state` → `ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` empty | pass |
| `## SHONEN` heading | `grep -c '^## SHONEN'` = 1, four `[~]` lines = the four SHONEN.md boxes | pass (no `[x]`) |
| trend verdicts | expansion / quality / discernment present, evidence pointers | pass |
| Sources & frontier section | census before/after, rows 63→66, F25 advance | pass |
| prompt contract | `.ufo/prompts/kasegi-round-42.md` carries report path, report-commit rule, SHONEN duty, write scope, commit-hash rule | pass |
| round shape | two v1 waves **declared**; wave 1 `kasegi-r42-build` 64 seats dispatched (`.ready.dispatched` present, `kasegi-r42-build-results.json` 64 results = the 64 `wave1-dispatch.json` names, no duplicates, no empty outputs); wave 2 `kasegi-r42-falsify` 36 seats rendered/validated (`.ready` 175 B, `wave2-dispatch.json` `counts.spawn=36`, 36 `taskCall.tasks`) but **undispatched** | **conformance finding (RD42-7)**: executed round = 64 seats (band floor met, ceiling untouched); the report states this correctly, but two committed narrative files assert the opposite (RD42-2, RD42-3) |

Contamination check (all 17 `round-42` commits): author and committer are `kasegi-shokunin <kasegi@shokunin.local>`
in every commit; committer timestamp ≥ author timestamp in every commit; committer times fall inside
`07:42:02-03 → 12:22:31-03` on 2026-10-28. One timestamp-hygiene exception, RD42-6: `0566bd6`'s **author** time
(`2026-10-27T10:06:29-03`) is inherited from its parent `5053a7f` (the round-41 closure commit) and precedes the
dispatch window by 21.6 h while its committer time (`08:00:01-03`) is inside; identity is kasegi throughout, so
this is a jj author-date inheritance artifact, not a foreign actor.

## 2. Claims — independent re-check

### C1 — depth:verifiability (4 → held 4), frozen reading with erratum 4 on the implementation

| # | Command (lane root; private `--work` under `/tmp/kasegi-r42-judge/`) | Observed |
|---|---|---|
| 1 | `bash corpus/instruments/r42-closure.sh` | `r42-closure: a plain run is refused (export mode only)` — **exit 2** |
| 2 | `… --export-ref b2c49ea5e7bc214e91c2b0bede5d4eaed4968572` | **`closed=13/13 exit=0`**, J1–J13 payloads byte-identical to the committed receipt |
| 3 | `… --selftest --export-ref b2c49ea5…` | thirteen `selftest case=J1..J13 … positive=pass payload-match=1 verdict=pass` lines, **`selftest cases=13 failures=0`**, exit 0 |
| 4 | `… --export-ref 5053a7f46de35784cff4b56756906e9014a38276` | `closed=5/13 exit=1` |
| 5 | `… --export-ref 1f7464612ac4c44e39886b82e812610d3c039b13` | `closed=4/13 exit=1` |
| 6 | `… --export-ref deadbeef…` | `ERROR ref-not-found ref=deadbeef… closed=0 exit=1` — exit 1 (distinct red) |
| 7 | `git show J:…/r42-closure.sh \| sha256sum` vs `Y:` and the receipt's `suite-sha256=` | all three `fca5ae62379e01232a523bbf318872dbb358cdf534ce65a42dfe7ef8df7f6d6b` |
| 8 | `git diff --stat J Y` | one path: the receipt, 33 lines (J+receipt only = Y) |
| 9 | receipt `run-utc=2026-10-28T15:12:46Z` vs commit Y `15:15:28Z` | run precedes its containing commit — pass (kill-rule clause satisfied) |

Replay limbs at Y (same run): `J1 …Replay=RevC1Counters.md=rejected` · `J2 …RevC1Counters.defeats.txt=rejected` ·
`J3 …MutSkillTablePipes.md=3/3` · `J4 …CritDeclarationCoverage.md=2/2` · `J5 …MutScratchTiming.md=outside=detected,
inside=detected` · `J6 …MutBindingExistence.md=rejected` · `J7 …MutFrontierParser.md=rejected`. J8 at Y: `receipt=…/all-gates.txt,source=committed,…,payload-match=12/12,forged=6/6
closed=1`.

Inherited-state numbers in the report/erratum 4 reproduce, with a receipt-granularity caveat (RD42-5): the pre-repair
instrument at `de09313` prints `closed=10/13 exit=1` and `selftest cases=13 failures=3` (re-run from that ref's own
suite bytes), but the committed red transcript `final-gates/all-gates.pre-repair.txt` is the **earlier** `d238e36`
state, `closed=9/13 exit=1`, `selftest cases=13 failures=4`.

Erratum 4 is an **implementation** repair inside the frozen predicate: predicate, five counting commands, kill rule,
targets and scores are unchanged in `claims.json`; E-R1..E-R5 each replace a false-pass or structurally-impossible
pass with the check its own predicate sentence describes. Reading applied: **frozen predicate, amended
implementation** (erratum 4 disclosed and committed before J).

### C2 — coverage (8 → held 8), frozen reading with erratum 1 (rejects add registry rows)

Measured at Y in the lane worktree; before-column re-derived from a `git archive` of base into `/tmp/kasegi-base`
(the lane worktree was never checked out at base).

| # | Command | Base | Y |
|---|---|---|---|
| 1 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 24 | **25** |
| 2 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 63 | **66** |
| 3 | `awk -F'\|' '/^\|[[:space:]]*S064[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); if(s=="mined") n++} END{print n+0}'` | 0 | **1** |
| 4 | `grep -rlE '^source: S064' corpus/knowledge \| wc -l` | 0 | **1** |
| 5 | `ls corpus/knowledge/*.md \| wc -l` | 60 | **61** |
| 6 | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=27 pass=27 exit=0` | **`entries=28 pass=28 exit=0`**, `PASS F25 ids=S064` |
| 7 | `python3 corpus/instruments/capture-binding-check.py` | `records=55 bound=55 unbound=0` | **`records=56 bound=56 unbound=0`** |
| 8 | `python3 corpus/instruments/recheck-audit.py --quiet` | `expected=60 missing=0 unexpected=0` (exit 1 at base: 59 strict cwd failures on absent instruments) | **`expected=61 missing=0 unexpected=0 exit=0`**, `strict pass=61/61` |
| 9 | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit 0 (`W04 S028`, `W04 S029`) | exit 0 (same two warnings, `ok`) |
| 10 | measure `awk …` over `corpus/README.md` | `44/44 = 1.000` | **`45/45 = 1.000`** |
| 11 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-42/manifest.json --source S064` | — | `S064:sha256 OK` + `Q1..Q4 OK occurrences=1 anchor=…-ok`, exit 0 |

Registry status cells: `S064=mined`, `S065=rejected`, `S066=rejected`. F25 row points at
`knowledge/cve-json-record-format.md`/`S064`; `PROVINCE.md:165` carries the `[r42 Frontier amendment]`. The capture is
3,545 lines / 84,520 B / `b90a51f7b356e7683483d9ac0753e3eb06fe3ab53806a57fdd4bf129b2f141fa`, matching the row, the
entry and the report. Junk-twin control: `.ufo/waves/round-42/wave1/ExecControls.md` records the O4 twin rejected at
every instrument independently (harness `entries=28 pass=27`, binding `unbound=1`, census `E11 S999`), so C2's
"a junk twin control is rejected" clause is evidenced.

## 3. Falsification pass — the missing wave 2

Ten attacks were run by this seat against a throwaway clone (`/tmp/kasegi-forge`, never pushed; each attack is one
commit on a branch from Y, graded by the frozen suite in export mode beside the pristine Y baseline). The suite's
own thirteen selftest cases plus the lane's 64-seat wave 1 cover the same surface synthetically; these attacks are
the tree-level pass the undispatched wave 2 owed.

| # | Attack (family) | Expected | Observed at the attacked ref | Killed? |
|---|---|---|---|---|
| a1 | receipt `J3 … rows=73` forged to `rows=99` (F-RCPT) | J8 payload comparison reds | `J3 … rows=73` recomputed; `J8 … payload-match=11/12 closed=0`; `closed=12/13 exit=1` | yes |
| a2 | receipt `selftest cases=13 failures=0` forged to `failures=1` (F-RCPT) | J8 summary fact reds | `J8 … summary=0 closed=0`; `closed=12/13 exit=1` | yes |
| a3 | receipt `export-ref` set to an unresolvable hash (F-RCPT) | ref/ancestor/diff facts red | `J8 … utc=0 ancestor=0 diff=0 closed=0`; `closed=12/13 exit=1` | yes |
| a4 | duplicate a `Correction (round 39)` block verbatim (F-CORR) | J11 unexcused duplicate | `J11 … corrections=35 groups=5 dups=5 excused=3 unexcused=2 closed=0`; `closed=11/13` | yes |
| a5 | `corpus/instruments/density.py` one-byte edit (J12 guard) | density digest reds | `J12 … density=0 density-sha=e5cbfb96d313 closed=0`; `closed=11/13` | yes |
| a6 | `declared-blocks.txt` gains `../escape` (F-DECL) | J4 escape | `J4 … declared=470 valid=469 escape=1 closed=0`; `closed=11/13` | yes |
| a7 | strip the evidence ids from a `Correction (round 42)` line (F-EVID) | J1 missing/union | `J1 … evidence=2 missing=1 … union=1 closed=0`; `closed=11/13` | yes |
| a8 | F25 row status `admitted`→`rejected` (F-FLIP) | J7 base instrumentation reds | `J7 … base=0 rows=25 admitted=24 closed=0`; `closed=11/13`; the C2 harness independently reports `FAIL F25 … status-not-admitted`, `entries=28 pass=27 exit=1` | yes |
| b1 | `check_j1`'s `ok` arm forced `True` in the suite (arm mutant) | J1 selftest mutant survives→case fails | `selftest case=J1 mutants=0/1 … verdict=fail`; `selftest cases=13 failures=2` (J1 and the J8 meta-case), exit 1 | yes |
| b2 | suite exit arm forced to `0` (never returns 1) | negative-control case fails | `selftest case=J9 positive=fail verdict=fail`; `failures=2` (J9 and J8), exit 1 | yes |

Incidental, and correct: a run whose export ref differs from J by *anything* other than the receipt reds J8's `diff`
fact (observed while driving b1/b2 before the driver copy was swapped) — the receipt is bound to its own tree, not
just to its own bytes.

Coverage honesty: this is a leaf seat with no subagent dispatch. Ten attacks were run; the remaining wave-2 plan
items (live-tree J2 mangled-tally and J6 manifest-mutation variants, J13 quiescence drift, C2 census adversarial rows)
were **not** run here and are carried as r43 attack material (RD42-7). No in-family (F-EVID / F-TOKEN / F-TABLE /
F-DECL / F-SCAN / F-BIND / F-FLIP) escape was found; the C1 kill rule is not triggered.

## 4. Axis verdicts

| Axis | Before → after (lane) | Verifier verdict | Reading | Evidence |
|---|---|---|---|---|
| depth:verifiability | 4 → 4 (held) | **met** | frozen predicate; erratum 4 = implementation repair, disclosed | C1 rows 1–9 above; 10/10 falsification attacks killed |
| coverage | 8 → 8 (held) | **met** | frozen predicate; erratum 1 adds reject rows to the registry count | C2 rows 1–11 above; junk twin rejected |
| depth:density | 9 → 9 | **unchanged (no harm)** | no-harm guard only | `density.py` sha256 identical at base and Y (`ee803726a322…`); `git diff --diff-filter=D` base→Y = 0 paths; J12 `deleted=0 density=1` |

Saturation stays 9/10 per owned axis, window N=3; the lowest non-retired axis remains depth:verifiability (4), which
this round measured but did not raise — the report claims no increase and the verifier confirms no increase is
claimed anywhere.

## 5. Discernment spot-check (LEARNING.md) — admits and rejects re-opened

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| F25 / S064 (CVE Record Format) | admit | capture `corpus/source-snapshots/round-42/S064.txt` L5, L3466, L3510 + `source-recheck.py` | **agree** | L5 = `"cve-schema specifies the CVE JSON record format. This is the blueprint for a rich set of JSON data…"` (18 words, the gate's quoted span); L3466 and L3510 verbatim; capture digest and 3,545/84,520-byte shape match the row; Q1–Q4 `occurrences=1 anchor=…-ok`, exit 0 |
| S065 (OSV schema) | reject | live `https://ossf.github.io/osv-schema/` L298–299 | **agree** | quote "This document defines a standard interchange format for describing vulnerabilities in open source packages." served verbatim at the cited Purpose paragraph (14 words); page is v1.9.2, 2026-10-13, as recorded; the stated reason (family already adjacent via kaidoku S015; normative artifact is HTML describing a schema published elsewhere) holds against the page itself |
| S066 (NVD API 2.0 schema) | reject | live `https://csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema` L96 | **agree** | `"description": "Metric scores for a vulnerability as found on NVD."` at line 96 exactly as cited (9 words); the document is an NVD response schema, so the "derived projection" reason is sound |
| S064 registry row / `SOURCES.md:70` | new row | `corpus/SOURCES.md` cells + manifest record | **agree** | status `mined`, kind spec, tier A, open date 2026-10-28, used-by the entry; manifest record bound (`records=56 bound=56`) |

No item was "could not re-open": the admit was checked against committed bytes and its executable recheck, both
rejects against the live first-party pages at the cited line numbers. No contradiction was found between a recorded
decision and its source; the reject reasons are honest (they name a criterion and a flip, not a generic preference).

## 6. Trend verdicts

- **expansion — improved.** F25 is a document class the lane did not hold (CVE Record Format schema), admitted with
  row + province amendment + entry + capture; registry 63→66, knowledge 60→61. Every delta atom is unreachable by the
  do-nothing control (`c2-controls/before.txt` re-derived above; base harness/binding/audit red at base).
- **quality — improved.** The C1 instrument moved from an inherited red (10/13, three selftest failures at `de09313`;
  9/13, four failures at the preserved `d238e36` transcript) to `closed=13/13`, `selftest cases=13 failures=0`, with
  four real defects mined as M42-3..M42-5 and the red transcript kept rather than overwritten. Ten independent
  tree-level attacks and two arm mutants were killed by the landed bytes in this spot-check.
- **discernment — improved.** The round read the three prior rejections, reused attempts 1–2 only after
  re-verification, kept predicate and implementation in separate records (errata 1–4, no target moved), preserved
  the stale red, and rejected two live-verified candidates with named criteria and flips. Its claim artifact matches
  measurement. Counter-evidence is confined to narrative hygiene — LOG.md and the lesson assert a wave-2 dispatch
  that never happened (RD42-2, RD42-3) — which is routed, not a claim overclaim.

## 7. Routed defects (owner: kasegi-shokunin; next round)

| id | Class | Pointer | What is wrong | Required next-round action |
|---|---|---|---|---|
| RD42-1 | stale number (append-only file) | `SCORECARD.md:1634` | says "the r42 suite at Y prints `J11 payload=corrections=33,…`"; the Y receipt (`final-gates/all-gates.txt:16`) and an independent Y run print `corrections=34` (the correction line itself raised the count) | appended `Correction (round 43)` naming the superseded cell; do not rewrite 1634 |
| RD42-2 | never-true narrative | `LOG.md:1804` | "wave 2 `kasegi-r42-falsify` 36 seats dispatched against the repaired head; dead seats counted from `wave2-results.json`" — no `.ready.dispatched`, no results file, zero seats | appended LOG correction in r43; the round total is 64 |
| RD42-3 | never-true narrative | `corpus/lessons/round-42.md:11,16` | "wave 2 dispatched 36 seats; the round total is 100" / "36 seats, 32 attack roles" — wave 2 was handed off, not taken | correct in the r43 lesson/QUALITY record |
| RD42-4 | placeholder section in a committed record | `corpus/lessons/round-42.md:52` | `## Wave-2 falsification` promises per-claim verdicts, attack tallies and per-family replay status "when the round-42 falsify wave reports"; no such report exists | replace with the non-dispatch record + the r43 attack plan, or delete the promise |
| RD42-5 | receipt granularity | report §Work performed / `claims-erratum-4.md` | quotes `closed=10/13`, `failures=3` at `de09313`; the only committed red transcript is `all-gates.pre-repair.txt` at `d238e36` = `9/13`, `failures=4` (both reproduced by this seat) | commit the `de09313` transcript, or cite the `d238e36` values where that transcript is the pointer |
| RD42-6 | timestamp hygiene | `claims.json` `frozen_at_utc`; commit `0566bd6` | freeze label `2026-10-28T12:05:00Z` is 65 min after its containing commit (`11:00:01Z`), disclosed by erratum 3 (real mtime `10:51:52Z`); `0566bd6`'s author date is inherited from parent `5053a7f` and predates dispatch by 21.6 h | record the erratum-3 freeze time wherever the freeze is cited; no claim depends on it |
| RD42-7 | conformance (undispatched wave) | `.ufo/waves/round-42/` | two v1 waves declared; wave 2 (36 seats, 31–32 attack roles) validated but never taken. Status-neutral, but it leaves the round's falsification on the instruments alone (carried here) | r43 opens with the wave-2 plan's unexecuted items (live J2/J6/J13 tree-level mutations, census adversarial rows) and counts wave 2 only when `<wave>-results.json` exists |

Non-defects noted for the record: the wave-1 attack share is stated as 21/64 = 32.8 % (reviewer+critic+mutation-tester);
counting `sentinel` as an attack role gives 23/64 = 35.9 %. Both clear the ≥25 % floor, so the reported share is a
conservative lower bound, not an error. `ExecControls.junk-f25.txt` is a control fixture under `.ufo/waves/` and is
correctly never landed in `corpus/` (harness counts unaffected).

## 8. Verdict

Both in-force claims verify at Y under their frozen predicates (C1 with erratum 4's disclosed implementation repair,
C2 with erratum 1's reject rows), no owned axis is harmed, and the falsification pass finds no in-family escape.
`admitted: true`. Seven routed defects, all narrative/timestamp hygiene or the undispatched wave; none touches a
claim's measurement. The round's own admission does not depend on them, and the next round must clear them before
adding new claims.
