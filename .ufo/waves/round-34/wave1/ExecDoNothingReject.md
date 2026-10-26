# ExecDoNothingReject — round 34, wave 1

| field | value |
|---|---|
| seat | ExecDoNothingReject (L2 leaf, executor) |
| round / lane | kasegi-shokunin round 34 |
| lane base | `014ee2d7aa8c3c095ff57ae51097606a9906228c` |
| claims freeze | `29f606dbdd28aff6fd4573ab4b90788bbb90af13` |
| assignment | demonstrate the do-nothing controls (C1 fake suite, C1 fake kill-rule runner, C2 shape-only junk twin) are rejected by the real instruments |
| measured at (UTC) | final evidence run at stability gate `2026-10-26T05:55:07Z` on the instrument bytes below (pre/post hashes identical); earlier runs at `2026-10-26T05:45:14Z` and `2026-10-26T05:51:41Z` on the previous instrument digests produced identical verdicts (see F6) |
| scratch | `/fast/scratch/hyaku/kasegi-r34/ExecDoNothingReject/` (removed before yielding; every quote below is the transcript, not a scratch path) |
| lane writes | this receipt only |
| installs | none (no pacman/uv/npm transaction run) |

## Artifacts under test — digests at the measured state

```
2a635bf575c38e04b028dd26ecbeff73c3b909add892ab727c2ab6b1c821dcfc  corpus/instruments/r-defect-closure.sh          (742 lines)
c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61  corpus/instruments/kill-rule-check.py           (881 lines)
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py     (892 lines, 40556 B)
d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe  corpus/source-snapshots/round-34/manifest.json
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  corpus/source-snapshots/round-34/S051.txt       (175 lines, 8502 B)
948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
899416e3ffaced532009646bbc6b5c0c0a48825e67858fca0b2b200fa19900db  .ufo/waves/round-34/c1-controls/fake-suite.sh   (10 lines)
7ca5d4fa97c6dadcb8f8b63a8f86f12a75d41335fdded8e46b1475a6cbb3b1af  .ufo/waves/round-34/c1-controls/fake-killrule.py (8 lines)
2752a994265a1e284ebd236730d169d677e1923cfb7073cf79ad874d19bc4026  .ufo/waves/round-34/c2-controls/junk-f17.md
c8438b4da19145efa7594dd576be0eba270fad3d27c378b5b6f99c1b6b0d8e1a  .ufo/waves/round-34/c2-controls/junk-checker.py
```

The same five mutable artifacts were hashed before and after the run block; the two hash prints are byte-identical (`HASHES (pre-run)` vs `HASHES (post-run)` in §Report). The five artifacts held that digest through the stability gate:

```
STABILITY stable_rounds=3 at 2026-10-26T05:55:07Z
```

(gate: the five artifacts were hashed every 30 s and three identical consecutive samples were required before any command below ran; every command whose output is quoted is shown verbatim in its section, and the pre/post hash prints bracket the run block).

## Report

### 1. Real closure suite vs `c1-controls/fake-suite.sh`

Command / output (verbatim; exit status after each block):

```
$ bash corpus/instruments/r-defect-closure.sh --selftest
selftest case=R1 live=pass fixture=rejected control=absent verdict=pass
selftest case=R2 live=pass fixture=rejected control=absent verdict=pass
selftest case=R3 live=pass fixture=rejected control=absent verdict=pass
selftest case=R4 live=pass fixture=rejected control=absent verdict=pass
selftest case=R5 live=pass fixture=rejected control=absent verdict=pass
selftest case=R6 live=pass fixture=rejected control=absent verdict=pass
selftest case=R7 live=pass fixture=rejected control=absent verdict=pass
selftest case=R8 live=pass fixture=rejected control=pass verdict=pass
selftest case=R9 live=pass fixture=rejected control=absent verdict=pass
selftest cases=9 failures=0
exit=0
```

```
$ bash corpus/instruments/r-defect-closure.sh
R1 check=SCORECARD.md lane-hash-markers=0 + appended 'Correction (round 34)' naming 7963976e/014ee2d open=0
R2 check=SCORECARD.md round-33 'Erratum 2' per-id restatement + QUALITY.md R22 pre-freeze step open=0
R3 check=QUALITY.md appended round-34 note below R20 (per-id supersedes 'exactly one') open=0
R4 check=tightened kill rule recorded (R24 row: kill rule + one 'selftest case=' line per case) + round-33 lesson R4 3-of-4 erratum open=0
R5 check=capture-binding-check.py url-matching-two-rows=0 cases=21 (>=11) open=0
R6 check=round-26 manifest binds S040-live.txt (record or orphan list) + purpose corrected open=0
R7 check=round-33 lesson appended R7 erratum (19->31, 23->22 characters, S050.txt:70) open=0
R8 check=round-32 manifest fetched_utc is a real strict-UTC instant (date-T time Z, zero offset), no '-' offset open=0
R9 check=capture-binding H4-H8 cases=9 + frontier rule A bidirectional (mirror=0 reverse=1) + junk=.ufo/waves/round-34/c2-controls/junk-f17.md open=0
closed=9/9 exit=0
exit=0
```

The same suite on the **base tree** (extracted read-only with `git cat-file -e 014ee2d…^{commit}` exit 0 and `git archive 014ee2d7aa8c3c095ff57ae51097606a9906228c | tar -x -C "$S/base"`, `archive_exit=0`; the extract carries 21 entries under `corpus/instruments/` and neither closure instrument):

```
$ bash corpus/instruments/r-defect-closure.sh --root /fast/scratch/hyaku/kasegi-r34/ExecDoNothingReject/base
R1 check=SCORECARD.md lane-hash-markers=2 open=1
R2 check=no 'Erratum 2' block in SCORECARD.md open=1
R3 check=no appended 'Note (round 34)' below R20 open=1
R4 check=tightened kill-rule requirement not recorded (QUALITY R24 row or a SCORECARD paragraph: kill rule + one 'selftest case=' line per case) open=1
R5 check=misnamed selftest case 'url-matching-two-rows' still present (count=2) open=1
R6 check=round-26 manifest has no S040-live.txt record and no orphan list open=1
R7 check=round-33 lesson has no appended R7 erratum open=1
R8 check=round-32 manifest carries a fetched_utc that is not a strict-UTC instant open=1
R9 check=capture-binding H4-H8 cases missing: per-file-orphan-detected per-file-orphan-listed nested-snapshot-dir fetched-utc-pending-rejected fetched-utc-local-offset-rejected dup-record-in-manifest double-https-row rejected-row-anchor summary-only-selftest-rejected open=1
closed=0/9 exit=1
exit=1
```

The do-nothing control:

```
$ cat .ufo/waves/round-34/c1-controls/fake-suite.sh        # 10 lines, no check table
#!/usr/bin/env bash
# Do-nothing control for C1: prints the claimed after-state without performing
# any check. The real suite must distinguish itself: its --selftest must run
# nine real checks each shown able to fail on a defect-bearing fixture copy.
if [ "${1:-}" = "--selftest" ]; then
  echo "cases=9 failures=0"
else
  echo "closed=9/9 exit=0"
fi
exit 0

$ bash .ufo/waves/round-34/c1-controls/fake-suite.sh --selftest
cases=9 failures=0
exit=0

$ bash .ufo/waves/round-34/c1-controls/fake-suite.sh
closed=9/9 exit=0
exit=0
```

**Comparison — the fake cannot satisfy the real suite's discriminator.**

1. **Output shape.** The fake's `--selftest` is *one* line, `cases=9 failures=0`, and it prints **0** `selftest case=` lines; the real suite prints **9** case lines plus the summary, and the case-line schema carries the outcome of a *fixture run* (`live=pass fixture=rejected control=absent verdict=pass`, with R8's positive control accepted as `control=pass`), not a constant:

```
fake_selftest_case_lines=0
fake_selftest_lines=1
real_selftest_case_lines=9
```

2. **The rule the lines encode** (`corpus/instruments/r-defect-closure.sh:12-21` and the discriminator paragraph `:24-36`): "For each check: run it on the live tree (must pass) and on a scratch fixture copy of only the files that check reads, with that one defect reintroduced (must fail). Where a check has a positive control (R8: the `+00:00` and fractional-second stamps rule C accepts) that fixture must be accepted too. Prints one `selftest case=R# live=... fixture=... control=... verdict=...` line per check plus `selftest cases=9 failures=0`; exit 0 only when every live run passes, every broken fixture is rejected and every control is accepted." The discriminator paragraph then states: "this suite prints exactly nine `selftest case=R# live=... fixture=... verdict=...` lines, produced by running each check twice (live tree + broken fixture), and a case counts as a pass only if the live run exits 0 AND the broken-fixture run exits non-zero. A summary line alone cannot satisfy that: the fake suite has no case table, so it cannot emit a case line, and it cannot exhibit a check that fails on a defect-bearing tree." The implementation is `run_selftest()` (the runner tail of `r-defect-closure.sh`): it calls `run_check_once "$RD_ROOT"`, calls `build_broken_fixture "$id"` (re-introducing exactly that one defect), calls `run_check_once "$scratch/$id"`, and prints `verdict=fail problems=...` when the live run is open or the broken fixture is accepted. A print-only script has no check functions, no fixture builder and no second run, so it cannot produce a passing case line; the fake's `case=0` count is the direct evidence.

3. **Same bytes, opposite verdicts.** The fake accepts any tree by construction (it has no `--root` argument; its plain line is the constant `closed=9/9 exit=0`). On the identical base bytes `014ee2d` the real suite reads `closed=0/9 exit=1` while the fake reads `closed=9/9 exit=0`; on the landed tree both read 9/9. The fake therefore cannot distinguish a defect-bearing tree from a repaired one — it is an unfalsifiable printer, and its claimed after-state is reproducible on the frozen base where all nine defects are open (`c1-controls/before.txt` records the same base facts: `ls_exit=2` for the suite, `lane-hash`=2, `url-matching-two-rows` present).

4. **The summary-only rule is also implemented in the instrument it gates.** `capture-binding-check.py --selftest` runs the forged-report cases (`judge_selftest_report`, `capture-binding-check.py:756-805`; "A report that prints only the summary is a failure, not a pass"):

```
$ python3 corpus/instruments/capture-binding-check.py --selftest | grep -E 'summary-only-selftest-rejected|^selftest cases='
selftest case=summary-only-selftest-rejected exit=1 want=1 verdict=pass
selftest cases=23 failures=0
exit=0
```

Applying that judge function (imported from the real instrument, read-only) to the fake suite's exact stdout:

```
fake --selftest raw: 'cases=9 failures=0\n'
fake lines=1 case_lines=0
real lines=10 case_lines=9 summary='selftest cases=9 failures=0'
judge_selftest_report(fake, R1..R9) ->
   summary-only-report
   case-line-count case=R1 count=0
   case-line-count case=R2 count=0
   case-line-count case=R3 count=0
   case-line-count case=R4 count=0
   case-line-count case=R5 count=0
   case-line-count case=R6 count=0
   case-line-count case=R7 count=0
   case-line-count case=R8 count=0
   case-line-count case=R9 count=0
   summary-line-count count=0
```

(Scope note: this judge's case-line regex is `capture-binding`'s own schema (`exit=`/`want=`), so it is quoted here as the implemented statement of the summary-only rule and applied to the fake; the real suite's nine lines use its own `live=`/`fixture=` schema and are judged by `run_selftest()` itself, item 2 above.)

### 2. Real survivor counter vs `c1-controls/fake-killrule.py`

```
$ python3 corpus/instruments/kill-rule-check.py
KILL-RULE instrument=corpus/instruments/capture-binding-check.py sha256=3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa bytes=40556 lines=892 floor=19 counter_sha256=c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61
probe selftest-shape pristine=pass exit=0
probe record-without-url pristine=pass exit=1
probe per-file-orphan pristine=pass exit=1
probe unnamed-record-id pristine=pass exit=1
probe stale-orphan-declaration pristine=pass exit=1
probe malformed-fetched-utc pristine=pass exit=1
probe punctuated-url-cell pristine=pass exit=0
probe malformed-orphan-declaration pristine=pass exit=2
probe nested-legacy-round pristine=pass exit=0
pristine selftest cases=23 case-lines=23 floor=19 floor_met=1
mutant-patch name=skip-selftest-summary patch_sha256=c457083e5d99f9f0 find_sha256=e6262244cffa1e1e find_count=1 status=ok
mutant-bytes name=skip-selftest-summary pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=b9d40dbee7521dbd
mutant-probe name=skip-selftest-summary probe=selftest-shape pristine=pass mutant=fail exit=0 reasons=summary-only;case-set-mismatch
mutant-probe name=skip-selftest-summary probe=record-without-url pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=per-file-orphan pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=punctuated-url-cell pristine=pass mutant=pass exit=0
mutant-probe name=skip-selftest-summary probe=malformed-orphan-declaration pristine=pass mutant=pass exit=2
mutant-probe name=skip-selftest-summary probe=nested-legacy-round pristine=pass mutant=pass exit=0
mutant=skip-selftest-summary killed=1
mutant-patch name=accept-record-without-url patch_sha256=83cbd622ad2fd1e2 find_sha256=cbf461982c746e9d find_count=1 status=ok
mutant-bytes name=accept-record-without-url pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=5897a1f044bcbf3f
mutant-probe name=accept-record-without-url probe=selftest-shape pristine=pass mutant=fail exit=1 reasons=exit=1;failures=1;case-verdict
mutant-probe name=accept-record-without-url probe=record-without-url pristine=pass mutant=fail exit=0 reasons=exit=0 want=1;missing='detail=absent';missing='unbound=1'
mutant-probe name=accept-record-without-url probe=per-file-orphan pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=punctuated-url-cell pristine=pass mutant=pass exit=0
mutant-probe name=accept-record-without-url probe=malformed-orphan-declaration pristine=pass mutant=pass exit=2
mutant-probe name=accept-record-without-url probe=nested-legacy-round pristine=pass mutant=pass exit=0
mutant=accept-record-without-url killed=1
mutant-patch name=per-file-binding-removal patch_sha256=f872ef12408d9162 find_sha256=f1a44079b9477ef2 find_count=1 status=ok
mutant-bytes name=per-file-binding-removal pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=616ce9dd0637a23b
mutant-probe name=per-file-binding-removal probe=selftest-shape pristine=pass mutant=fail exit=1 reasons=exit=1;failures=2;case-verdict
mutant-probe name=per-file-binding-removal probe=record-without-url pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=per-file-orphan pristine=pass mutant=fail exit=0 reasons=exit=0 want=1;missing='rule=orphan-capture';missing='orphans=1 orphan=S009.txt'
mutant-probe name=per-file-binding-removal probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=punctuated-url-cell pristine=pass mutant=pass exit=0
mutant-probe name=per-file-binding-removal probe=malformed-orphan-declaration pristine=pass mutant=pass exit=2
mutant-probe name=per-file-binding-removal probe=nested-legacy-round pristine=pass mutant=pass exit=0
mutant=per-file-binding-removal killed=1
control=CTL-noop verdict=invalid:noop expect=invalid:noop ok=1
control=CTL-nocompile verdict=invalid:nocompile expect=invalid:nocompile ok=1
control=CTL-equivalent verdict=survivor expect=survivor ok=1 witness_survivors=1 witness_exit=1
control=CTL-fake-killrule verdict=opaque expect=opaque ok=1 fake=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-34/c1-controls/fake-killrule.py fake_exit=0 fake_mutant_lines=0 fake_patch_digests=0 fake_mutants_line=0 fake_survivors=0 real_mutant_lines=3 witness_survivors=1 differs=1 stable=1
controls=4 rejected=4
GATE ok name=named-rows
GATE ok name=pristine-selftest
GATE ok name=pristine-fixtures
GATE ok name=pristine-determinism
GATE ok name=rows-valid
GATE ok name=controls
GATE ok name=survivors-zero
mutants=3 killed=3 survivors=0 invalid=0
gates=7 failed=0
survivors=0
exit=0
```

Fake runner:

```
$ cat .ufo/waves/round-34/c1-controls/fake-killrule.py     # 8 lines
#!/usr/bin/env python3
"""Do-nothing control for C1's survivor-mutant counter.

Prints the claimed after-state (survivors=0) without replaying any mutant.
The real kill-rule-check.py must replay each mutant against the landed
instrument bytes and print the actual survivor count.
"""
print("survivors=0")

$ python3 .ufo/waves/round-34/c1-controls/fake-killrule.py
survivors=0
exit=0
```

**Difference, measured by the real instrument itself.** The real runner replays three textual mutants over a *copy* of the landed `capture-binding-check.py` bytes, each exactly-once (`find_count=1`), records pre/post digests (`pristine_sha256=3d9e5e0ddbaaccf9` → `mutant_sha256=…`) and probes each mutant against five behaviour probes; it proves its post-state per mutant (`mutant=… killed=1`) and only then prints `survivors=0`. The fake prints the same summary line with `fake_mutant_lines=0 fake_patch_digests=0 fake_mutants_line=0`, i.e. no replay at all. The runner's own control block rejects it rather than accepting the coincidence of the summary string:

```
control=CTL-fake-killrule verdict=opaque expect=opaque ok=1 … fake_exit=0 fake_mutant_lines=0 fake_patch_digests=0 fake_mutants_line=0 fake_survivors=0 real_mutant_lines=3 witness_survivors=1 differs=1 stable=1
```

`differs=1` is computed from the absence of mutant lines/digests in the fake's output *and* the presence of a live witness (`witness_survivors=1`, `witness_exit=1`, i.e. the equivalent-patch control is correctly a survivor). A fake that emitted a fabricated `mutants=` line would also fail that predicate (`kill-rule-check.py:39-52` documents the control). Hand-invoking the fake and the real runner on the same bytes yields `survivors=0` twice, so the summary line alone is not evidence — the discriminator is the replay record, and the real tool refuses the fake on exactly that ground (`verdict=opaque`).

### 3. Real S051 recheck vs the C2 shape-only junk twin

Real pinned entry:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
S051:sha256 OK
S051:Q1 OK occurrences=1 anchor=46-ok
S051:Q10 OK occurrences=1 anchor=79-ok
S051:Q11 OK occurrences=1 anchor=83-ok
S051:Q12 OK occurrences=1 anchor=88-ok
S051:Q13 OK occurrences=1 anchor=92-ok
S051:Q14 OK occurrences=1 anchor=94-ok
S051:Q15 OK occurrences=1 anchor=90-ok
S051:Q16 OK occurrences=1 anchor=95-ok
S051:Q17 OK occurrences=2 anchor=96-ok
S051:Q18 OK occurrences=1 anchor=99-ok
S051:Q2 OK normalized=markup-whitespace occurrences=1
S051:Q3 OK occurrences=1 anchor=52-ok
S051:Q4 OK occurrences=1 anchor=52-ok
S051:Q5 OK normalized=markup-whitespace occurrences=1 anchor=53-ok
S051:Q6 OK normalized=markup-whitespace occurrences=1 anchor=55-ok
S051:Q7 OK occurrences=1 anchor=74-ok
S051:Q8 OK occurrences=1 anchor=75-ok
S051:Q9 OK occurrences=2 anchor=77-ok
exit=0
```

The junk twin's fabrication, adjudicated against the *same pinned capture bytes*: three scratch variants of the round-34 manifest were built by appending one `JUNK1` assertion to the real `S051` record (same `path`, same `sha256`; `S051.txt` copied beside the manifest so the instrument resolves it the same way). The build recorded the raw occurrence count of each string in `S051.txt`:

```
{
 "junk-sentence": { "quote": "Critical includes \"Direct theft of any user funds\"", "raw_occurrences_in_capture": 0 },
 "junk-clause":   { "quote": "five severity levels for smart-contract exploits",     "raw_occurrences_in_capture": 0 },
 "junk-fragment": { "quote": "Direct theft of any user funds",                        "raw_occurrences_in_capture": 1 }
}
```

`junk-sentence` (the sentence `c2-controls/junk-f17.md:15-16` asserts) — full output:

```
$ python3 corpus/instruments/source-recheck.py --manifest $S/junk-sentence.json --source S051
S051:sha256 OK
S051:JUNK1 MISMATCH reason=quote-not-found
S051:Q1 OK occurrences=1 anchor=46-ok
S051:Q10 OK occurrences=1 anchor=79-ok
S051:Q11 OK occurrences=1 anchor=83-ok
S051:Q12 OK occurrences=1 anchor=88-ok
S051:Q13 OK occurrences=1 anchor=92-ok
S051:Q14 OK occurrences=1 anchor=94-ok
S051:Q15 OK occurrences=1 anchor=90-ok
S051:Q16 OK occurrences=1 anchor=95-ok
S051:Q17 OK occurrences=2 anchor=96-ok
S051:Q18 OK occurrences=1 anchor=99-ok
S051:Q2 OK normalized=markup-whitespace occurrences=1
S051:Q3 OK occurrences=1 anchor=52-ok
S051:Q4 OK occurrences=1 anchor=52-ok
S051:Q5 OK normalized=markup-whitespace occurrences=1 anchor=53-ok
S051:Q6 OK normalized=markup-whitespace occurrences=1 anchor=55-ok
S051:Q7 OK occurrences=1 anchor=74-ok
S051:Q8 OK occurrences=1 anchor=75-ok
S051:Q9 OK occurrences=2 anchor=77-ok
exit=1
```

`junk-clause` and `junk-fragment` — the only delta from the real run in each is the `JUNK1` line (verified by diff; every one of the 18 real assertions is unchanged and still `OK`):

```
--- diff real vs junk-sentence ---
1a2
> S051:JUNK1 MISMATCH reason=quote-not-found
(exit=1)
--- diff real vs junk-clause ---
1a2
> S051:JUNK1 MISMATCH reason=quote-not-found
(exit=1)
--- diff real vs junk-fragment ---
1a2
> S051:JUNK1 OK occurrences=1
(exit=0)
```

Shape-only control on the same file:

```
$ python3 .ufo/waves/round-34/c2-controls/junk-checker.py
junk_twin h1=True source_line=True recheck_line=True
shape_counters=3/3
exit=0
```

**Comparison.** The shape counter (H1 header, `source:` line citing S051, `recheck:` line) accepts the junk twin 3/3 without reading capture bytes; the real gate rejects the junk twin's *asserted sentence* at the first byte comparison (`JUNK1 MISMATCH reason=quote-not-found`, exit 1) while the real entry's 18 assertions pass on the identical pinned bytes (`exit=0`). The fake's `shape_counters=3/3` is blind to exactly that distinction, which is why the claim's admission gate is the quote check, not the shape counters.

**Honest limit measured on this control (see F1 below):** `junk-fragment` — the bare noun phrase the junk twin puts inside quotation marks — **does** occur once in the landed capture (`S051.txt:75`, `raw_occurrences_in_capture: 1`) and passes (`S051:JUNK1 OK occurrences=1`, exit 0). The rejection above rests on the twin's *sentence* and *clause*, not on that fragment.

### Findings for the L1 (no artifacts edited by this seat)

- **F1 — `c2-controls/junk-f17.md:18` states a false claim about its own fixture.** It says `[FABRICATED — no capture holds this quote; the admission gate must reject this entry]`, but the quoted fragment `Direct theft of any user funds` occurs once in the landed capture at `corpus/source-snapshots/round-34/S051.txt:75` (measured, `raw_occurrences_in_capture: 1`). The twin is still rejected because its sentence `Critical includes "Direct theft of any user funds"` and its clause `five severity levels for smart-contract exploits` do not occur (`reason=quote-not-found`, exit 1), but the file's own explanation is wrong at fragment level, and a reviewer who tests only the quoted fragment would read exit 0. Suggested correction (append-only, L1-owned): restate the twin's fabricated assertion as the sentence that source-recheck actually rejects, or add the measured fragment occurrence and say plainly that the rejection is "paraphrase asserted as a quote", not "string absent from the capture".
- **F2 — transient selftest crash observed mid-wave, absent at final bytes.** At suite digest `ba729460…` (02:35 local) `--selftest` printed a summary line `selftest cases=9 failures=9` and then `corpus/instruments/r-defect-closure.sh: line 1: scratch: unbound variable` (exit 1) because the EXIT trap referenced a function-local `scratch` under `set -u`. At the first measured digest `0beafed2…` line 620 expands the path at trap-install time (`trap 'rm -rf -- '"$scratch"'' EXIT`); the construct survives at the final digest `2a635bf5…` on line 683, and `--selftest` exits 0 with no such line. Recorded so a reviewer does not mistake the earlier transcript for a defect of the landed bytes; the landed bytes were re-run clean.
- **F3 — the round-34 manifest churned during the wave; the capture did not.** Three distinct manifest digests were recorded while waiting (`72bac252…` → `3e726d84…` → `d5077f81…`); `S051.txt` stayed `4fd8ed98…` throughout and `source-recheck --source S051` exited 0 at each invocation. All numbers quoted here are from the stable `d5077f81…` state, hashed before and after the run block. If a reviewer replays against a different manifest digest, the `Q9` occurrence/anchor figures (`occurrences=2 anchor=77-ok`) are the cells most likely to differ.
- **F4 — R5 undercounts the instrument's case table by two, and the numbers name different measurements.** The closure suite's R5 line says `cases=21`; `kill-rule-check.py` says `pristine selftest cases=23 case-lines=23`; `capture-binding-check.py --selftest` prints `selftest cases=23 failures=0`. The instrument's `CASES` table (`capture-binding-check.py:662-738`) holds 21 entries — measured `sed -n '662,738p' … | grep -cE '^\s+\("'` → `21` — and `REPORT_CASES` (`:806-810`) adds 2, so `--selftest` reports 23. R5's grep `^[[:space:]]*\("[a-z0-9-]+",` (`r-defect-closure.sh:250-256`) counts 21 over the whole file only because it takes the 19 underscore-free `CASES` names plus the 2 `REPORT_CASES`; it misses the two `CASES` names containing `_` (`round-32-record-without-fetched_utc` at `:692`, `round-32-record-with-fetched_utc-passes` at `:698`). R5's floor is `>=11`, so no kill-rule is tripped and the frozen claim's `N>=19` is met at 23; but R5 would be tighter (and would track the claim) if it read the instrument's own summary line or widened the character class.
- **F5 — base-tree replay confirms the frozen before-state.** `--root` on the `014ee2d` extract reads `lane-hash-markers=2`, `url-matching-two-rows count=2`, all nine `open=1`, `closed=0/9 exit=1` — matching `c1-controls/before.txt` (`2`, `2`, `selftest cases=11`, `ls_exit=2`), so the suite's nine checks are load-bearing in both directions (open on base, closed at tip).

- **F6 — both closure instruments were revised during the wave; every verdict reproduced on each revision.** The suite moved `0beafed2…` (665 lines) → `357a7e49…` (688) → `2a635bf5…` (742), and the survivor counter moved `7a20e724…` (793) → `c279d952…` (881; three added probes — `punctuated-url-cell`, `malformed-orphan-declaration`, `nested-legacy-round` — a `named-rows` gate, and reworded R8 descriptions). The suite revision additionally added a per-case `control=` field (R8's `+00:00`/fractional-second positive control is accepted as `control=pass`; the other eight checks have no positive control and print `control=absent`). Each of the three evidence runs (stability gates `05:45:14Z`, `05:51:41Z`, `05:55:07Z`) reproduced every verdict: `selftest cases=9 failures=0` exit 0, `closed=9/9` exit 0, base `closed=0/9` exit 1, `mutants=3 killed=3 survivors=0` exit 0, `controls=4 rejected=4`, `gates=7 failed=0`, source-recheck `exit=0`; transcript diffs between runs are confined to digest lines, the R8 wording, the added probe/gate lines and the `control=` field. The digests quoted above are the last measured ones; the suite is owned by ExecRDefectClosureSuite and may be revised after this measurement — the kill rule (`cases=9 failures=0` exit 0, `closed=9/9` exit 0) held at all three digests.
- **F7 — stray untracked file at the lane root, not authored by this seat.** `selftest-baseline.txt` (1552 B, mtime 2026-10-26 02:37 local) sits untracked at the lane root and contains `capture-binding-check` `selftest case=…` output — evidently a seat's accidental redirect. This seat's only lane write is this receipt; the L1 should sweep the file or have its author remove it. It does not affect any of the three demonstrations.

### Scope, cleanup, tooling

- Lane writes: this receipt only. No `git add/commit/push`, no `jj` mutation; the only git commands run were read-only (`git cat-file -e`, `git archive` into scratch). No write to `/home/vgpnk/Projects/shokunin`, `/home/vgpnk/Projects/shokuknow`, `bounties`, or any sibling lane.
- Scratch (`/fast/scratch/hyaku/kasegi-r34/ExecDoNothingReject/`, including the four scratch manifests, the copied `S051.txt`, the base-tree extract and the driver) was removed with `rm -rf` before yielding; no scratch tree is left on disk.
- No installs or upgrades were performed (pacman transactions untouched; no `uv`/`npm`/binary install).
- Verdict scope: the do-nothing controls are rejected by the landed instruments on the measured digests. This seat does not judge C1/C2 soundness as a whole; the L1 integrates and the critics review.
