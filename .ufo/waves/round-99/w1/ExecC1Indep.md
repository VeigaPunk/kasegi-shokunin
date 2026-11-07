# ExecC1Indep — independent re-derivation of C1 (kasegi round-99, wave 1)

Seat: read-only attacker/verifier, leaf. Axes worked: depth:verifiability (primary), coverage (incident hygiene).
Scratch: /fast/scratch/hyaku/kasegi-r99/ExecC1Indep (removed before yield). Receipts: `.ufo/waves/round-99/w1/ExecC1Indep-receipts/` (9 files). No lane file written by this seat; no commits/pushes; no tools installed (stdlib python3 sufficient).

## 0. Pins verified

`sha256sum` (receipt `shas.txt`): lane `corpus/instruments/census-at-rev.py` = `6d68d955…f041` (claim pin ✓); `.ufo/waves/round-99/c1/tamper.py` = `1d0810a2…e220` (claim counter pin ✓); round-98 instrument materialized via `git show e2d3de7b847f8e9bac72a5bc4dea455ea051cf1a:corpus/instruments/census-at-rev.py` = `66383371…2502` (do-nothing pin ✓). All four wave commits resolve (`git rev-parse --verify <rev>^{commit}`).

## 1. Independent census — AGREE (exact)

Method: own extractor+classifier (`mycensus.py`) over `git archive a3db47e71fe292c03b00ba11f38cccbec45d3966 | tar -x` into private scratch; the lane instrument was never imported or called for these numbers. Scope `SKILL.md` + `corpus/**/*.md` excluding `corpus/instruments/citation-survival.md` (373 files scanned, 336 contributing — matches the census body). INTERNAL = lane-relative BASE resolving inside the extract (literal/brace/`<...>`→glob ladder); a `..`-walk-out INTERNAL resolving outside the extract leaves the numerator, stays in the denominator.

```
$ python3 -B mycensus.py $S/extract          (receipt mycensus-output.txt)
pinned: SKILL 162/732 = 22.13% | corpus 2569/7624 = 33.70% | lane 2607/8026 = 32.48%
distinct=8026 occurrences=16587
walk-out INTERNAL excluded (HOST-OWNED): 1 ['../']
```

Comparison with the pinned line (`corpus/instruments/citation-survival.md:7` at HEAD/35e3ab6): all six numbers and all three percentages identical; distinct 8026 and occurrences 16587 identical; contributing files 336 identical; walk-out exclusion 1 = the lone `../` citation = the census `confined 1`.

Delta forensics (kept as evidence, not hidden — first run printed corpus 7622 / lane 8024):
- My initial −2 denominator was MY extractor's divergence: resolve.py's `is_pathlike` re-normalizes in-predicate (`t = tok.strip().rstrip(".,;:")` again), so a span like `` `resolve.py .` `` yields key `resolve.py ` and still counts. My `pathlike()` applied the space rule to the once-normalized token. Fixed to the pinned rule; numbers became exact.
- Identity note (count- and numerator-neutral): two in-scope backticked citations contain literal TABs (`corpus/SOURCES.md:263` → `file\tW04\tS072 duplicate url … scopes`; `corpus/lessons/round-43.md:50` → `kasegi\tok\t/home/…/SOURCES.md`). resolve.py counts each as one GONE citation (distinct 8026); census-at-rev's TSV re-parse splits each NF=10 row into a fragment row whose "class" is a data value (`W04`, `ok`). True rows and fragments are both non-INTERNAL and corpus-scoped, so the pinned numerator and both denominators are unaffected (receipt `delta-analysis.txt`).
- `host_owned=76` decomposition: instrument RESOLVES rows = 76; my informational absolute/~ ladder resolves 73 of them; the extra 3 are `~/Projects`, `~/Projects/`, `~/Projects/**`, which RESOLVE under the instrument's confined HOME because `home_dir()` creates `<work>/home/Projects` (census-at-rev.py:63-66) — exactly the "empty Projects tree" the census header discloses (receipt `delta-analysis.txt`).

## 2. Lane `census-at-rev.py --check` — PASS, both layouts

Against the committed census blob copied to scratch (`git show HEAD:corpus/instruments/citation-survival.md`, sha `211818db…959e3`, byte-equal to 35e3ab6's blob; see §4 for why not the worktree file):

```
clean:  CENSUS-CHECK pass rev=a3db47e71fe292c03b00ba11f38cccbec45d3966 skill=162/732 corpus=2569/7624 lane=2607/8026 host_owned=76 confined=1   rc=0
dirty:  identical output, rc=0   (work parent carries MISSION.md and .ufo/waves/shokunin12h-20261014-p1-repair/members/KasegiGateRepair.md)
```
Receipts `check-clean.txt`, `check-dirty-layout.txt`. Cache-bypass is exercised inside the harness: T09-poisoned-cache (poisoned under both key schemes, census edited to agree, digests recomputed) is killed with `reason=pinned-mismatch` (receipt `tamper-candidate.txt`).

## 3. Tamper harness — PASS, both limbs

```
$ cd <lane> && python3 -B .ufo/waves/round-99/c1/tamper.py --lane . --rev a3db47e71fe292c03b00ba11f38cccbec45d3966 \
    --alt-rev b9411a6b530e486180cf14c72fccc46668dcf5ee --instrument corpus/instruments/census-at-rev.py --work $S/tamper-cand2
TAMPER-RESULT killed=12 total=12 evaluated=12 instrument_sha256=6d68d9555b9be5a75bfefb27ee8cf531bc97dd540c954cc2da56581e6a68f041 rc=0

same with --instrument $S/r98-census-at-rev.py:
TAMPER-RESULT killed=5 total=12 evaluated=12 instrument_sha256=66383371211bf4b801df608d5e20c23e2b51457717fcb1b76de471b8feb62502 rc=0
```
Per-case reasons in receipts `tamper-candidate.txt` / `tamper-round98-instrument.txt`; the round-98 instrument accepts T11-host-owned-edited and T12-body-truncated (`CENSUS-CHECK pass … corpus=2570/7624 lane=2608/8026`), matching the claim's do-nothing analysis.

## 4. Mid-wave incident: lane census clobber + restore (verified, not mine)

Between ~19:27 and 19:30 the worktree files `corpus/instruments/citation-survival.{md,tsv}` were overwritten by a foreign run: the md became a raw resolve.py output naming `/fast/scratch/hyaku/kasegi-r99/CriticClaimsC1/D2/w/extract-a3db47e71fe2/tree` as `Lane root:` with different totals (8041/16627, 337 files) and no round-99 header; my first `--check` attempts therefore failed `reason=no-measured-at`. Overwrite mtimes `19:27:37` (tsv .207, md .315). CriticClaimsC1-7 acknowledged (their D2 symlink test pointed resolve.py's extract root at the lane), restored both files at mtime `19:30:03`, and disclosed in CriticClaimsC1.md. Post-restore I verified: `git status --porcelain corpus/instruments/` empty; md sha `211818db…` and tsv sha `0099820f…` both equal to `git show HEAD:…`. Evidence: receipt `clobber-evidence.txt`. All my lane-side readings were taken against the committed blob in scratch, so no verdict depends on the clobbered interval. Note for the fleet: a `--write`/`--check` whose extract `tree` is a symlink to the lane turns the read-only lane into a write target — worth a lane-side guard (reporting only; out of my scope to fix).

Also independently corroborated the claim's motivation: my first direct `resolve.py` invocation ran with the real HOME and hung past 300 s on the `~/Projects` recursive glob (job killed) — the exact earlyoom hazard C1's confined HOME eliminates; rerun confined finished in ~4 s.

## 5. Bounds

Read-only in the lane throughout (rev-parse/show/status/diff/archive/merge-base only). Writes: this report, the receipts dir, and scratch. Scratch removed before yield. No peer orchestration; one coordination message to CriticClaimsC1-7 (incident).

VERDICT: C1 independent census AGREE — my own extractor over the a3db47e extract reproduces SKILL 162/732 = 22.13%, corpus 2569/7624 = 33.70%, lane 2607/8026 = 32.48%, distinct 8026, occurrences 16587, contributing files 336, and the single `../` HOST-OWNED exclusion (confined 1), all exact.
VERDICT: C1 census --check PASS — clean and contaminated work layouts both rc=0 with the identical pinned triple (host_owned=76, confined=1) against the committed census blob sha 211818db; cache poisoning (T09) does not vouch.
VERDICT: C1 tamper harness PASS — killed=12/12 evaluated=12 with the pinned candidate instrument (sha 6d68d955) and killed=5/12 with the round-98 instrument (sha 66383371), rc=0 both, at rev a3db47e / alt b9411a6 as pinned.
VERDICT: C1 host-owned/confined support AGREE — 76 = 73 genuinely resolving absolute/~ citations + 3 `~/Projects*` roots resolved by the instrument's own empty confined Projects tree; confined=1 is the lone `../` INTERNAL walk-out; the two TAB-embedded citations shift TSV row identity but not any pinned count.
