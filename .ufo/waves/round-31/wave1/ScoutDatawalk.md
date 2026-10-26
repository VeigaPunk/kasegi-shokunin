# ScoutDatawalk receipt (round 31, planner data-walk)
Run in /home/vgpnk/Projects/shokunin/kasegi-shokunin, read-only. Quiescent-state caveat (bound 6): other seats were starting; no corpus/ byte differed from the freeze at run time (`git diff --stat b374feb 738a779 -- corpus` and `git diff --stat 738a779 master -- corpus` both empty; `git status` shows no modified path under corpus/).

## Observed facts
1. `git rev-parse master` -> `8a8916c7043bd873d191b30dd1744b241b91f4d9` (NOT 738a779). `git log`: 8a8916c "wave-1 spec, validated dispatch" -> 738a779 "freeze claims" -> b374feb. `git merge-base --is-ancestor 738a779 master` true. 738a779..master touches only .ufo/waves/round-31 files (spec/plan/dispatch), no corpus/ bytes. So frozen BEFORE values hold at master; master tip is freeze+1 (dispatch commit). Only modified tracked file: `.ufo/waves/round-31/build-spec.py` (+5 lines, uncommitted).
2. C1 counter/ledger absent: `ls corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json` -> both "No such file", ls_exit=2; `python3 corpus/instruments/limb-mutation-check.py --ledger ...` -> "can't open file", counter_exit=2. Matches c1-controls/before.txt.
3. `python3 corpus/instruments/recheck-audit.py --quiet`:
```
strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=19 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=43 total=43 pass=43 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=43 missing=0 unexpected=0 exit=0
audit_exit=0
```
   Committed expected-entry count: `grep -cvE '^\s*(#|$)' corpus/instruments/knowledge-expected.txt` = 43; `ls corpus/knowledge/*.md | wc -l` = 43.
4. `python3 corpus/instruments/source-recheck.py --selftest` -> 9 SELFTEST PASS lines (clean, corrupt, missing-source, missing-manifest, stem-mismatch, double-occurrence, double-occurrence-anchored, double-occurrence-out-of-range, double-occurrence-broken), `selftest cases=9 failures=0`, sr_selftest_exit=0.
5. `python3 corpus/instruments/frontier-recheck-count.py`: last lines `PASS F12 ... ids=S041,S042`, `PASS F13 ... ids=S043,S044,S045`, `PASS F14 ... ids=S041,S046,S047`, `entries=17 pass=17 exit=0`, harness_exit=0.
6. C2 counters (claims.json counter_commands, verbatim): `frontier_admitted=14`; entries citing S048 (`grep -lE '^source: S048 '`) = 0; S048 rows = 0; registry rows = 47; `source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048` -> `manifest UNAVAILABLE reason=missing`, recheck_exit=2. All equal c2-controls/before.txt.
7. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`: census_exit=0; findings exactly
```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```
8. Base instrument sha256 (equal claims.json do_nothing_control prefixes 3fc0d751 / 33602a9d / aa60b581):
```
3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1  corpus/instruments/recheck-audit.py
33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f  corpus/instruments/source-recheck.py
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
```
   These are the pre-mutation bytes; ExecRALimbs/ExecSRLimbs/ExecFRLimbs will change them (strengthening), so post-wave digests legitimately differ.

## claims.json predicates vs counter commands (inference from reading both)
- C1: the predicate's 13 limbs = 9+2+2 match the contract ids. Predicate says each control "must report as rejected or survivor"; the interface contract says `controls=3 rejected=3` where rejected = verdict equals `expect` (invalid:noop, invalid:nocompile, survivor). Consistent: the equivalent control's expected verdict is `survivor`, counted as rejected. Kill rule requires `strict pass=N/N` with N = committed expected-entry count: now 43=43; if ExecExpectedList adds the F15 entry the count becomes 44 (N moves with it, rule tolerates). C1 counter_commands run the three instruments but not the harness's F15; C2 harness line expects 18/18 after the entry lands, which also changes the recheck-audit `lines`/`expected` totals to 44 (inference: the audit lists each knowledge entry).
- C2: predicate 14->15, 1 entry, S048 once, 47->48, census 0, harness 18/18 with `PASS F15`, recheck exit 0 -- each has a matching counter command above; no mismatch found. Kill rule additionally bars new census findings beyond the two W04.
- Gap noted: C2's `grep -lE '^source: S048 '` requires entry `source:` lines to begin with `S048 ` followed by a space; an entry writing `source: S048, ...` or `source: S048` alone would count 0.

## Untracked entries (`git status --porcelain -uall`, 28 paths; tracked-modified: build-spec.py)
Inherited round-29/30 leftovers (routed defect 1, to be committed or discarded and named):
- .ufo/waves/round-29/kasegi-r29-build-results.json
- .ufo/waves/round-30/c1-controls/c1-after.txt
- .ufo/waves/round-30/kasegi-r30-build.ready
- .ufo/waves/round-30/kasegi-r30-build.ready.dispatched
- .ufo/waves/round-30/plan.err
- .ufo/waves/round-30/run.err
- .ufo/waves/round-30/wave1/ConnHarm.md
- .ufo/waves/round-30/wave1/CritMeta.md
- .ufo/waves/round-30/wave1/ExecControlC1.md
- .ufo/waves/round-30/wave1/RevC1Controls.md
- .ufo/waves/round-30/wave1/fetch-manifest.sha256
- .ufo/waves/round-30/wave1/fetch/s037.html
- .ufo/waves/round-30/wave1/fetch/s048.html
- .ufo/waves/round-30/wave1/fetch/s054.pdf
- .ufo/waves/round-30/wave1/fetch/s054.txt
- .ufo/waves/round-30/wave1/fetch/s065.pdf
- .ufo/waves/round-30/wave1/fetch/s065.txt
- .ufo/waves/round-30/wave1/fetch/s068.html
- .ufo/waves/round-30/wave1/mutant-b1/mutant-b1-source-recheck.py
- .ufo/waves/round-30/wave1/mutant-b1/mutant-b1.diff
- .ufo/waves/round-30/wave1/mutant-b1/source-recheck.py
Round-31 own (not leftovers):
- .ufo/waves/round-31/wave1.ready
- .ufo/waves/round-31/wave1.ready.dispatched
- .ufo/waves/round-31/wave1/ScoutMSVR-scratch/S048.txt
- .ufo/waves/round-31/wave1/ScoutMSVR-scratch/S048b.txt
- .ufo/waves/round-31/wave1/ScoutMSVR-scratch/raw.html
- .ufo/waves/round-31/wave1/ScoutMSVR.md
- .ufo/waves/round-31/wave1/swarm-registry.json
- .ufo/waves/round-31/wave2-items.py

## Gaps
- Master is 8a8916c, not the freeze commit; if a checker pins master==738a779 it fails, but corpus bytes are identical.
- Counters run pre-landing = PRE-STATE; none compared to any after column here.
