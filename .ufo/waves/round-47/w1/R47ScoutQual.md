# R47ScoutQual — pre-freeze duty audit

Axes: depth:verifiability; coverage. Scope: documentary audit of frozen controls, not a rerun, counter repair, semantic approval, or closure verdict.

## Evidence provenance and method

All paths below are relative to the lane root. `C/` abbreviates `.ufo/waves/round-47/controls/`; `Q` means `corpus/QUALITY.md`; `E46` means `.ufo/waves/round-46/counter-errata.md`.

Observed read-only command, lane cwd:

```
git ls-tree -r --name-only 308a2cb2dc7bdce233461cc1ac49dd88e51c6193 -- .ufo/waves/round-47/controls/ .ufo/waves/round-47/claims.json .ufo/waves/round-47/freeze.txt
```

Printed the claims, freeze record, and all eleven control files inventoried below. `git diff --exit-code 308a2cb2dc7bdce233461cc1ac49dd88e51c6193 -- .ufo/waves/round-47/controls/ .ufo/waves/round-47/claims.json .ufo/waves/round-47/freeze.txt corpus/QUALITY.md .ufo/waves/round-46/counter-errata.md` printed nothing and exited successfully. Thus the line citations to those working files describe freeze-committed bytes, not newly generated seat receipts.

No LSP device is mounted in the `xd://` inventory. This is a literal document/receipt audit; source-text references below are not represented as semantic definition/reference proof. No counters, battery, or fixture builders were executed. No tools installed. No scratch created, hence no scratch remains.

## Checklist: what already had to hold at freeze

| Duty and controlling evidence | Frozen evidence | Finding |
|---|---|---|
| **R47: replay each frozen counter on the cheapest do-nothing tree; match its complete declared before line; do this before data/seats.** `Q:380`. | Claims `:16` and `:40` declare the lines. `C/c1-base.txt:12-13` prints `routed-defects total=11 fixed=0 unresolved=11 exit=1`, `EXIT=1`. `C/c2-base.txt:8-9` prints `f30-gate fixed=1/7 exit=1`, `EXIT=1`. `C/freeze-check.txt:1-4` records both `verdict=ok`, `base_ok=2 exit=0`. `C/freeze-controls.txt:1` identifies those as do-nothing controls. | **Receipt-supported for before-value discrimination.** Neither base reads the after-value. `freeze.txt:2` asserts before-seat ordering, but the receipts do not independently timestamp the runs; see timing gap below. |
| **R48: every artifact limb binds content, not merely a heading/file/word; use marker-retaining negative worlds; surviving false-green is a limb defect.** `Q:381`. | `C/selftest-receipt.txt:1-44` supplies positive fixtures plus 41 negative cases. Examples: bad SHA `:2`, thin correction `:19`, fabricated quote `:30`, duplicate rows `:25,29`, duplicate registry heading `:35`. | **Partial evidence, not a universal content-binding certification.** Several cases simply remove required material. The receipt is evidence only for its named attacks, not for denial/stub/comment variants absent from it. |
| **R49: admission/rejection capture-method parity; a contradicted reject needs a superseding row and appended correction; independent review remains necessary.** `Q:382`. | `C/capture-determinism.txt:1-4` records two matching captures each for S075 and S076 using `capture-source.py`. `C/capture-binding-before.txt:24-29` explicitly reads `bound=61 unbound=2`, no-row S075/S076, exit 1. `C/freeze-controls.txt:5` discloses staged capture-before-registry state. | **Capture reproducibility recorded; parity review not demonstrated by these receipts.** No receipt independently compares admitting/rejecting methods and reasons or certifies a supersedes+lesson correction. These are still substantive review/landing duties; do not label binding green. |
| **R50: pre-freeze single-edit counter-mutant battery, at least three per limb; every survivor closed or disclosed as a mechanical limit in the claim.** `Q:390`. | `C/mutbat-receipt.txt:1-36` gives C1 L1-L11: 35 total (L2/L8 four each, every other limb three), 19 caught, 16 uncaught, equivalent 0, baseline_failures 0, exit 1. `:37-58` gives C2 H1-H7: three each, 21 total, 3 caught, 18 uncaught, equivalent 0, baseline_failures 0, exit 1. Claims `:18,:41` disclose those limits and point to all IDs. `freeze.txt:3` acknowledges 34 survivors. | **Count/run/disclosure supported; no mutation pass.** This satisfies the disclosure alternative, not elimination of survivors. Receipt output alone does not prove edit atomicity; source text `corpus/instruments/r47-mutbat.py:16-18,129-140` describes/asserts one occurrence and writes one replacement. |
| **R51: re-derive each routed defect from committed bytes/clocks before constructing its gate; an honest comparator must distinguish a timestamp defect if a clock gate is involved.** `Q:391`. | Claims `:12` names base-byte locations; `C/c1-base.txt:1-11` records all eleven unresolved limb readings. | **Partial only:** these are the gate's own readings, not independent plain re-derivations of D5-D8. No control receipt supplies a byte-by-byte independent derivation for every defect. No R47 claim introduces a timestamp-order gate; do not import the withdrawn author-clock test as a requirement. E46 `:85-87` records why it was withdrawn. |
| **R52: each claim has an independent plain second measurement over committed bytes, with before-values explicitly tied to both start trees (base and freeze).** `Q:392`; E46 `:45-58,:99-119`. | Claims `:19-28` and `:43-49` list commands and base expectations. Claims `:29,:50` distinguish aggregate freeze-counter readings (C1 unchanged; C2 2/7 versus base 1/7). `C/sources-census-before.txt:1-4` and `C/sources-census-attempt3.txt:1-5` preserve census output only. | **Gap:** no committed per-tree plain-measure transcript for either claim; base expectations are annotations, and aggregate Python-counter freeze readings are not per-measure plain values. `source-recheck.py` at claims `:27` is an additional check, not a grep/wc/awk substitute. C2's grep at `:47` counts matching files whereas its annotation calls the base 0 “policy-bearing files”; the receipt set does not establish that interpretation. |
| **R52 re-ground-specific safeguards:** keep restoration recheck verbatim; anchors per current claim across >=2 files; distinguish historical claims/reimplementation; identify independent row reader. `Q:392`; E46 `:21-24,:42,:93-97`. | No R47 claim is a new un-gating/re-ground of the lost-tool entries. `C/recheck-audit-before.txt:1-5` records executes=44, gated=22, broken=0, 66 entries, exit 0. | **Not a new R47 implementation duty unless integration changes those entries/rechecks.** The unchanged gated count is not evidence they were re-grounded or that semantic row faithfulness passed. The plain-second-measure duty above remains applicable to both claims. |
| **R53: BOTH attack classes before freeze; tree-level false-green probes per limb; every such probe red at frozen bytes; fixture builders committed beside counter.** `Q:393`. | `C/selftest-receipt.txt:1,:21` establishes positive fixture greens; `:2-20,:22-43` are 41 targeted reds; `:44-45` says 43 cases, failures=0, exit 0. `freeze.txt:6` pins `r47-counters-selftest.py`; `:7` pins mutant harness. Per-limb mapping below. | **Per-limb execution/targeted red receipts supported. Strict marker-retention coverage remains partial.** The fixture source removes recheck/rows/lesson for some cases (`r47-counters-selftest.py:249-250,268,274-275,411`), so do not equate “one red per limb” with every required marker-preserving false-green attack. No receipt here explicitly names C1 marker-only-fix and false-phrases-commented worlds from the C1 kill rule. |
| **Era-bound instrument exemption story at freeze, not discovered after honest landing.** `corpus/lessons/round-46.md:96` (M46-6); E46 `:37,:83,:96` shows content-pin exemptions and changed pass sets must be explicit. | No file in the eleven committed controls names the R47 era-export/new-tip contrast, replacement gate, or exemptions. `freeze.txt:4-8` pins new instruments only. | **Gap:** no frozen exemption story/paired readings in this control set. Need explicit treatment of `r46-f29-gate.py` (S074/42-line/manifest/entry-era state versus S076 repair) and r46-c1/c2 v1.3 era pins, ledger/F29 entry exceptions, era export versus new-tip expected-moved readings, and which current counter replaces them. This scope is also explicit in the errata scribe card, `.ufo/waves/round-47/build-wave1-spec.py:86` (dispatch instruction, not freeze evidence). |

### R53 per-limb receipt map

All references in this table are to `C/selftest-receipt.txt`; they certify only the named fixture/expected limb-red condition.

| Limb | Receipt lines / example |
|---|---|
| L1 | 18, s1left |
| L2 | 5,17, fenceleft / regbullet-missing |
| L3 | 8,19, nocorrection / thin-correction |
| L4 | 4, falsephrase1 |
| L5 | 16, orderfalse |
| L6 | 9,20, noforbid / threecases |
| L7 | 12, nonames |
| L8 | 2,6,14, badsha76 / maninert / norow76 |
| L9 | 3,7,15, badspan / nocite / oldcite |
| L10 | 10, nolead |
| L11 | 11,13, nolesson47 / noprecision |
| H1 | 25,29,36, duprow / ghostrow / rowstatus |
| H2 | 23,34,39, badxref / norecheck / thinsect |
| H3 | 22,38,40, badloc / thinscope / tierc |
| H4 | 24,27,32,41, capflip / fewquotes / manws / toolmut |
| H5 | 28,30,31,42,43, fewspans / junkquote / longquote / unlocated / widespan |
| H6 | 26,33, entryrename / nestedmd |
| H7 | 35,37, regdup / symlink |

### Ordering evidence limitation (R47 explicitly imports R44)

`Q:380` delegates before-seat ordering to the freeze record. `Q:370` requires a `frozen-at` UTC instant bounded by latest control `measured-at` and containing commit, plus claims hash equality. `freeze.txt:1-12` contains a before-seat assertion, file hashes, and base but no `frozen-at`; claims `:1-7` have no freeze timestamp. Except capture timestamps (`C/capture-determinism.txt:4`), the inspected controls have no `measured-at` timestamps. Observed: files are committed at the stated freeze and claims hash is listed at freeze `:12`. Unresolved: independent clock corroboration of pre-freeze execution. Committed presence is not a substitute for the required timestamp envelope.

## Complete frozen control inventory

- `C/c1-base.txt:1-13`: eleven unresolved limb readings and declared C1 before-line/exit.
- `C/c2-base.txt:1-9`: seven limb readings and declared C2 before-line/exit.
- `C/freeze-check.txt:1-4`: two do-nothing before-value matches, overall exit 0.
- `C/freeze-controls.txt:1-5`: index to do-nothing/tree/mutation/determinism receipts; discloses survivors and unbound staged captures, not additional execution evidence.
- `C/mutbat-receipt.txt:1-58`: all mutant IDs/results, C1/C2 totals; both battery exits 1, not a pass.
- `C/selftest-receipt.txt:1-45`: two positive fixtures and 41 targeted-negative results, 43 total, failures 0.
- `C/capture-determinism.txt:1-4`: capture command shape, matching double-fetch hashes for both sources, HTTP 200 and timestamps; not independent live-semantic review.
- `C/capture-binding-before.txt:24-29`: round-47 records unbound to registry, two explicit failures, exit 1.
- `C/recheck-audit-before.txt:1-5`: executes 44/gated 22/broken 0; total 66, exit 0; no separately labelled base-vs-freeze pair.
- `C/sources-census-before.txt:1-4`: three W04 warnings and ok path, no explicit exit trailer.
- `C/sources-census-attempt3.txt:1-5`: same warning classes and ok path, explicit exit 0.

## Closure roadmap / limits

Keep the recorded do-nothing discriminator and the 43-case receipt; do not convert the two mutation `exit=1` summaries into a pass or call the 34 survivors equivalent. At closure distinguish frozen evidence from later repairs: obtain per-tree plain values (not just commands or Python aggregate values), explicit era-bound historical/live gate readings and exceptions, and marker-preserving worlds missing from the frozen receipt set. Separately review semantic capture provenance, each corrected sentence, genuine section placement, F30 novelty and live quote location: claims `:18,:41` explicitly reserve semantic duties.

Confidence: high for committed receipt contents/counts and the named missing artifacts; moderate for sufficiency of R48/R53 adversarial coverage because no probes were rerun and this seat did not attempt exhaustive falsification. This report does not repair or retroactively certify pre-freeze ordering. Permanent claim/counter changes remain the L1's decision, not this scout's.

Self-evaluation: accuracy 4/5 (line-grounded; timing remains uncorroborated), completeness 4/5 (all eleven receipts inventoried; no dynamic/exhaustive attack claims), clarity 4/5 (abbreviations defined; checklist necessarily dense), actionability 4/5 (specific missing evidence named; no integration authority), conciseness 4/5 (full per-limb map adds length). Overall 4.0/5. Highest-impact evidence improvements are per-tree plain transcripts and freeze-time era/ordering corroboration. A user should read these scores as a scope statement, not a quality-gate pass.
