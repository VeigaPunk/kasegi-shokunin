# ExecCensusAfter — round-35 C2 census after-state (quiescent tip bytes)

Seat: `ExecCensusAfter` (leaf of the L2 wave; sole writer of this receipt).
Round: kasegi-shokunin round 35, hyaku run 8. Lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Lane base `3266c9937b03062d9bbc2f436e20820115ed179c`; claims-freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`.

Writes: this receipt only. Every command below is **read-only** over the lane
(`sources-census.sh validate` writes nothing without `--out`; the instruments read only; `git archive`,
`git rev-parse`, `git ls-files`, `git status` are reads). No `git add/commit/push` and no `jj` mutation was run.
No tool installs or upgrades were needed (nothing installed; tooling authorization recorded as unused).

## Report

### 1. Where these bytes are — read this before quoting any number

Measured on the **working copy on top of commit `87f6b95`**, not on a landing commit (the L1 commits; this seat
does not). The lane's commit graph moved during the wave, so every number below is bound to its instant:

| instant (UTC) | `git rev-parse HEAD` | what the vessel was |
|---|---|---|
| 06:44:51–06:44:57 | `da2d3c687f82a9814ee71c91c930cb733050d37c` | round-35 wave-1 spec + dispatch (pass 1) |
| 06:58:42–06:58:43 | `aa6ad99bb90c4fe30dc5c326adf2f82d8ec84b1b` | round-35 L1 integration — C1 D4/D6/D7 (pass 2) |
| **07:12:31–07:12:33** | **`87f6b95ec67dffb007c69ef07d9a9962d75e89b0`** | **round-35 verifier spot-check (integrator, hyaku) (pass 3, definitive)** |
| 07:13:17–07:14:57 | `87f6b95` (unchanged, 6 polls) | retained quiescence trace (§2) |

`git log --format='%h %cd %s' --date=iso-strict -6` at 07:12:5xZ:

```
87f6b95 2026-10-26T04:08:04-03:00 round-35 verifier spot-check (integrator, hyaku): non-author admit/reject
48e6053 2026-10-26T04:04:55-03:00 round-35: scorecard + SHONEN late seat appends
bb2dc8c 2026-10-26T04:04:46-03:00 round-35: receipt finalization — ExecDoNothingReject updated receipt, ExecD1Markers receipt fix
5a25337 2026-10-26T04:02:21-03:00 round-35: commit wave leftovers — S052 capture (named >1MiB), SKILL registry, controls, ready markers, receipts
8ce6fb4 2026-10-26T04:01:12-03:00 round-35: D1 closure fix — scorecard closing-commit wording
0aee0ef 2026-10-26T04:00:05-03:00 round-35: integration — lesson, scorecard, SHONEN, LOG, wave receipts, assimilation artifacts
```

At the definitive pass the lane still carried uncommitted bytes above `87f6b95`, none of them a C2 input:

```
 M .ufo/waves/round-35/wave1/ScribeLesson.md      M .ufo/waves/round-35/wave1/ScribeReportDraft.md
 M SHONEN.md                                      M corpus/lessons/round-35.md
?? .ufo/waves/round-35/wave1/ExecRegressionC1.md  ?? .ufo/waves/round-35/wave1/ScribeScorecard.md
?? .ufo/waves/round-35/wave1/ScribeShonen.md      ?? .ufo/waves/round-35/wave1/SentScopeFinal.md
```

`corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/cisa-kev-catalog.md`,
`corpus/source-snapshots/round-35/…` and `corpus/instruments/r35-defect-closure.sh` are clean against `HEAD`
(absent from `git status --short`), i.e. the C2 row, the F18 row/entry and the capture are **committed** bytes.
The §7 digest table is the bookend set: identical digests after the L1's commit ⇒ identical verdicts.

### 2. Quiescence predicate and the evidence it fired

Pass 1 predicate (poll every 20 s, three consecutive byte-identical polls required): `rows>=52`,
`S052 rows>=1`, `README F rows>=18`, `knowledge entries citing 'source: S052'>=1`,
`corpus/source-snapshots/round-35/manifest.json` present, `corpus/instruments/r35-defect-closure.sh` present,
and a stable sha256 set over `SOURCES.md`, `README.md`, `SCORECARD.md`, `QUALITY.md`,
`corpus/knowledge/**`, `corpus/source-snapshots/round-35/**`, `corpus/instruments/**`.
Fired at **06:44:51Z**. Verbatim tail of that log (the `stable=` field is printed *before* the poll's own
comparison is applied, so the break fires on the poll that prints `stable=2` with a third identical digest):

```
06:41:31Z poll=29 rows=52 s052=1 front=18 citing=1 know=47 manifest=1 suite=1 dig=4d3132639cd4347d1c6a6621245a0d0cf62ed307e6313f631e7aa5a615ffcc5f stable=0
06:41:51Z poll=30 rows=52 s052=1 front=18 citing=1 know=47 manifest=1 suite=1 dig=4d3132639cd4347d1c6a6621245a0d0cf62ed307e6313f631e7aa5a615ffcc5f stable=0
06:42:11Z poll=31 … dig=4d3132639cd4347d1c6a6621245a0d0cf62ed307e6313f631e7aa5a615ffcc5f stable=1
06:42:31Z poll=32 … dig=ef6fccb8fc59182e549285acdd70f791935ac3d060d0ba433ef948ff6e05d38f stable=2
06:42:51Z poll=33 … dig=2b15cff35daf59d449e68eae69c87724a55dbf0217bb68eca6d0c0dd5f585353 stable=0
06:43:11Z poll=34 … dig=fc0e3e49a6e764ac49fce1bb5d7b3eebec3bea045f7a059c1d898ad2aceb3986 stable=0
06:43:31Z poll=35 … dig=fff13ff06443f9be38d712c867e74f42fe5118277fbffdd490cd9ff82f697af1 stable=0
06:43:51Z poll=36 … dig=e064f7e263550ce0999698f1cbe4c670c620d3f80f61c3311cf6b6b7a5159bdf stable=0
06:44:11Z poll=37 … dig=e064f7e263550ce0999698f1cbe4c670c620d3f80f61c3311cf6b6b7a5159bdf stable=0
06:44:31Z poll=38 … dig=e064f7e263550ce0999698f1cbe4c670c620d3f80f61c3311cf6b6b7a5159bdf stable=1
06:44:51Z poll=39 … dig=e064f7e263550ce0999698f1cbe4c670c620d3f80f61c3311cf6b6b7a5159bdf stable=2
QUIESCENT at 2026-10-26T06:44:51Z polls=39 dig=e064f7e263550ce0999698f1cbe4c670c620d3f80f61c3311cf6b6b7a5159bdf
```

The surfaces were still moving until poll 36 (`dig` changed at posts 32, 33, 34, 35, 36); polls 37/38/39 are the
three identical ones that satisfied the predicate.

Pass 2 waited for the C1 closure suite to reach `closed=7/7` **and** three stable polls over
`SCORECARD.md`, `SKILL.md`, `QUALITY.md`, `SOURCES.md`, `README.md`, `r35-defect-closure.sh`,
`kill-rule-check.py`, the F18 entry, the round-35 manifest, `claims-erratum-d5.md` and the round-34 results pair.
Pass 3 repeated that over 11 C2/C1 surfaces plus `corpus/source-snapshots/round-35/S052.txt` and added
`no file under .ufo/waves/round-35 touched in the last 120 s`; it ended after **782 s / ~39 polls, well before its
2400 s cap**, and its meta block records `newest-in-wave-120s=0` with 64 wave-1 receipts on disk.

Retained trace after the definitive pass (this replaces pass 3's poll log — see §10.1, the scratch tree was
deleted by something outside this seat mid-run, so the pass-3 log itself is gone):

```
07:13:17Z poll=1 rows=52 front=18 fresh60=0 head=87f6b95 dig=bbc53efc…
07:13:37Z poll=2 rows=52 front=18 fresh60=0 head=87f6b95 dig=bbc53efc…
07:13:57Z poll=3 rows=52 front=18 fresh60=0 head=87f6b95 dig=bbc53efc…
07:14:17Z poll=4 rows=52 front=18 fresh60=0 head=87f6b95 dig=bbc53efc…
07:14:37Z poll=5 rows=52 front=18 fresh60=0 head=87f6b95 dig=bbc53efc…
07:14:57Z poll=6 rows=52 front=18 fresh60=0 head=87f6b95 dig=bbc53efc…
```

Six identical digest polls over 100 s, zero wave files touched in any 60 s window, HEAD unchanged.

### 3. A1 — round-end census (`sources-census.sh validate`), definitive pass

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

- exit **0**; one registry (`…/kasegi-shokunin/corpus/SOURCES.md`), lane verdict line `kasegi ok`.
- **W04 only, and only S028/S029** — byte-identical to `.ufo/waves/round-35/census-before.txt` (same two lines,
  same exit 0). No E-code. Per the script header, `W` codes never change a clean lane's status.
- Byte-identical in all three passes (06:44:51Z / 06:58:42Z / 07:12:31Z).

### 4. A2–A9 — the contract commands (verbatim from `.ufo/waves/round-23/falsify/RegistryR8.md:143-168`)

Run from the lane root; every one re-run in each of the three passes with identical output (the only
inter-pass `diff` lines were the meta timestamps, §7). Exit codes were captured per command, so no pipeline exit
is misattributed.

| # | command | output | exit | frozen C2 expectation | verdict |
|---|---|---|---|---|---|
| A2 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `52` | 0 | registry rows **52** | **match** |
| A3 | `awk -F'\|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md` | `0` | 0 | malformed **0** | **match** |
| A4 | tier histogram (`$5`) | `A=49 B=1 C=2 ` | 0 | (not frozen; sums to 52) | consistent |
| A5 | status histogram (`$9`) | `mined=40 queued=9 rejected=3 ` | 0 | (not frozen; sums to 52) | consistent |
| A6 | duplicate ids (`uniq -d`) | *(empty, 0 bytes)* | 0 | empty | **match** |
| A7 | enum violations + tier inflation | *(empty, 0 bytes)* | 0 | empty | **match** |
| A8 | mined rows whose `used-by` paths do not exist | *(empty, 0 bytes)* | 0 | empty | **match** |
| A9 | independent count of rows whose `used-by` cell is not `—` | `40` | 0 | (not frozen; equals `mined=40`) | consistent |

Sum checks: `49+1+2 = 52` rows and `40+9+3 = 52` statuses. A9 is the cross-check that the A8 walk is not
vacuous: all 40 `mined` rows carry a non-`—` used-by cell and all 40 paths exist on disk.

### 5. B1–B6 — the registry/frontier cells the frozen C2 claim names

| # | command | output | exit |
|---|---|---|---|
| B1 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `18` | 0 |
| B1b | `awk` status tally over the same `F<n>` rows | `admitted=18` | 0 |
| B2 | `grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md` | `1` | 0 |
| B3 | `grep -lE '^source: S052 ' corpus/knowledge/*.md \| wc -l` | `1` | 0 |
| B4 | `ls corpus/knowledge/*.md \| wc -l` | `47` | 0 |

B1 = 18 **admitted** rows (no queued/rejected frontier rows), i.e. frontier admitted 17 → 18 against the frozen
C2 `before` cell (`.ufo/waves/round-35/claims.json` → `claims[1].before[0]: "frontier_admitted=17"`; note that
round-35's `census-before.txt` records only the two W04 lines and no frontier tally, so the 17 is taken from the
freeze, not from that file). Registry 51 → 52 against the same `before` cell (`registry rows=51`).

S052 row, field by field (`-F'|'`, `f2`=id … `f12`=used-by):

```
f2=[S052]
f3=[CISA Catalog of Known Exploited Vulnerabilities (KEV catalog JSON feed) — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json]
f4=[dataset]  f5=[A]  f9=[mined]  f10=[2026-10-26]  f11=[90d]
f8=[CISA's catalog states exploitation status per record, with a dateAdded to dueDate remediation clock and a knownRansomwareCampaignUse label, and carries no severity or CVSS score, so a KEV listing is a prioritization signal that a severity score cannot supply]
f12=[corpus/knowledge/cisa-kev-catalog.md]
```

i.e. tier **A**, kind **dataset**, status **mined**, opened **2026-10-26**, recheck cadence 90d, used-by the
entry — the frozen C2 cell ("row S052, tier A, status mined, opened 2026-10-26") holds by measurement.

Frontier row F18 (`corpus/README.md:388`, quoted in part): `| F18 | CISA Known Exploited Vulnerabilities
catalog — exploitation-status-based prioritization distinct from CVSS severity | admitted |
knowledge/cisa-kev-catalog.md | S052 | Keep the catalog's remediation clock attached to the directive that binds
it: BOD 26-04 supersedes the revoked BOD 22-01 and uses KEV status as one of four risk-priority factors … KEV
listing is an exploitation-status signal, not a severity score — the feed carries no severity field (12 keys x
1756 records, cvss 0). |`

Citing entry `corpus/knowledge/cisa-kev-catalog.md` (117 lines, sha256
`e9de994dbe1940adb894420d566386500e4e29d69d8e6a5244ff2172c71d9761`), lines 3–6:

```
source: S052 — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json — capture corpus/source-snapshots/round-35/S052.txt (27,870 lines; sha256 d69349e8…8826): title L2, catalogVersion L3, …
verified-at: 2026-10-26
ground: F18
recheck: cd …/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052   # five assertions (Q1-Q5) at anchors 2, 3, 4, 15472 and 19165, each `occurrences=1` with `sha256 OK`; …
```

`grep -lE '^source: S052 '` hits exactly this one file, so the citation is single-sourced.

### 6. C — the two C2 runtime re-checks

**C1 `frontier-recheck-count.py --root .`** — 21 `PASS` lines, exit 0:

```
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
entries=21 pass=21 exit=0
harness_exit=0
```

21 entries over 18 admitted rows (F09/F10/F11 each carry two entries). `grep -E 'PASS *F18'` returns exactly
the one line above with `ids=S052`, `grep_exit=0`.

**C2 `source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052`** — 6 lines,
exit 0:

```
S052:sha256 OK
S052:Q1 OK occurrences=1 anchor=2-ok
S052:Q2 OK occurrences=1 anchor=3-ok
S052:Q3 OK normalized=markup-whitespace occurrences=1 anchor=4-ok
S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=15472-ok
S052:Q5 OK normalized=markup-whitespace occurrences=1 anchor=19165-ok
recheck_exit=0
```

Assertion census on that output: `grep -c '^S052:Q'` = **5**; `occurrences=1` = **5**; `occurrences=2` = **0**;
`grep -cE 'MISMATCH|FAIL'` = **0**. So the frozen sentence "every assertion occurrences=1, sha256 OK, exit 0" is
**literally true at these bytes** — the round-34 D5 wording problem (Q9/Q17 `occurrences=2`) does not recur, and
the entry itself states the count ("five assertions (Q1-Q5)").

Manifest binding (`corpus/source-snapshots/round-35/manifest.json`, sha256
`06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee`): one source `S052`, `path=S052.txt`,
`sha256=d69349e8…8826` (equal to `corpus/source-snapshots/round-35/S052.txt`), `url` =
`https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`, `fetched_utc=2026-10-26T06:32:40Z`
(strict UTC, `Z`, no local offset), quotes Q1–Q5 at anchors 2/3/4/15472/19165. The manifest `url` byte-equals the
S052 registry row's `https://` token.

### 7. D — C1 cross-checks (measured here; the C1 seat owns the claim)

Cheap, read-only, and they use the same quiescent bytes, so they are reported rather than left to inference.
**Pass 1 is the interesting column**: at 06:44:51Z two limbs were still open.

| # | measurement | 06:44:51Z | 06:58:42Z | 07:12:31Z |
|---|---|---|---|---|
| D1 | `bash corpus/instruments/r35-defect-closure.sh` | `closed=4/7 exit=1` (D6, D7 open) | `closed=7/7 exit=0` | `closed=7/7 exit=0` |
| D1b | same, `--root` = `git archive 3266c99` extraction | — | — | `closed=0/7 exit=1` (`base_suite_exit=1`) |
| D2 | `--selftest` (run between 07:00Z and 07:12Z, `KASEGI_SCRATCH` under this seat's scratch) | — | — | `selftest cases=7 failures=0`, exit 0 |
| D3 | `grep -c 'filled by the L1' SCORECARD.md` | 0 (exit 1: no match) | 0 | 0 |
| D3b | `grep -c '<LANE_HASH>' SCORECARD.md` | 0 | 0 | 0 |
| D4 | `git ls-files .ufo/waves/round-34/wave1-results.json \| wc -l` | 0 (untracked, provenance note beside it) | 1 | 1 |
| D5 | `claims-erratum-d5.md` present | present (`ls` count 1; untracked at that instant) | yes (13086 B, sha `eee0bb57…`) | yes (sha `eee0bb57…`) |
| D6 | `supersedes R22` / `supersedes R23` rows in `QUALITY.md` | 0 / 0 (suite D7 open) | 1 / 1 | 1 / 1 |

Full suite line set at 07:12:31Z (each `open=0` = defect closed):

```
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=4 open=0
D2 check=erratum-row=1,erratum-mean=6,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
```

**Base-tree discriminator** (the C1 kill rule's "fails on the base tree" limb), run from the lane instrument
against an extraction of lane base `3266c99`:

```
base_extract=AGENTS.md considerthese corpus LOG.md plans PROVINCE.md README.md SCORECARD.md SHONEN.md SKILL.md
D1 check=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0 open=1
D2 check=erratum-row=0,erratum-mean=0,row-bytes=1 open=1
D3 check=registry-r-defect-closure=0,registry-kill-rule=0 open=1
D4 check=tracked=0,provenance=0 open=1
D5 check=erratum-file=absent,discriminating-invocation=0,per-id-occurrences=0 open=1
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=0/7 exit=1
```

Each check therefore flips on the bytes that carry its defect — the suite is a discriminator, not a constant.

**Selftest** (7 case lines, 24 detail lines, exit 0; scratch forced under this seat's scratch via
`KASEGI_SCRATCH`):

```
selftest case=D1 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D2 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D3 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D4 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D5 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D6 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D7 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=short-report rejected=1
selftest judge=fake-suite rejected=1 path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0
selftest judge=fake-plain rejected=1 output=closed=7/7 exit=0
selftest judge=complete-report accepted=1
selftest_exit=0
```

17 clause mutants across the seven checks (3+3+2+2+3+2+2), each rejected with `others=6/6`, so a rejection is
attributable to the reopened clause. The do-nothing twin (`.ufo/waves/round-35/c1-controls/fake-suite.sh`, which
prints `closed=7/7 exit=0` / `cases=7 failures=0` while checking nothing) is rejected by the judge.

Marker re-read at 07:12:55Z: `201.7` occurrences in `SCORECARD.md` = 5, `201.2` = 6, `c1c6a5f` = 4 — the D1/D2
corrections are appended rows rather than edits of the filed rows, as `QUALITY` R19 requires.

### 8. E — the junk F18 twin, measured three ways (read-only)

```
E1 file:      .ufo/waves/round-35/c2-controls/junk-f18.md 1164 B sha256 0abec3591e4a2dc5195b23b1c2c920f66052327b7f971aa578af76c3459dc176
E2 in round-35 manifest:  grep -c 'junk-f18' corpus/source-snapshots/round-35/manifest.json -> 0
E3 in frontier table:     grep -c 'junk-f18' corpus/README.md -> 0
E4 in knowledge dir:      ls corpus/knowledge/ | grep -c 'junk' -> 0
E5 fabricated strings in the pinned capture (grep -oF | wc -l over corpus/source-snapshots/round-35/S052.txt):
   "five exploited vulnerabilities to the catalog every Tuesday" -> 0
   "scores each entry with a CVSS v4 vector rather than a due-date" -> 0
```

`E5`'s second form, the **discriminating invocation** the round-34 erratum restates (a manifest whose assertion
is the twin's own sentence, sha256-pinned to the committed capture), run here for F18:

```
### twin assertions (expect MISMATCH quote-not-found, exit != 0) ###
S052:sha256 OK
S052:J1 MISMATCH reason=quote-not-found
S052:J2 MISMATCH reason=quote-not-found
twin_probe_exit=1
### control assertion the capture holds (expect OK, exit 0) ###
S052:sha256 OK
S052:C1 OK occurrences=1 anchor=3-ok
control_probe_exit=0
```

So the twin is rejected on evidence, not on shape: its sentences are absent from the pinned bytes and the same
invocation shape accepts a sentence the capture holds.

**Boundary recorded, not fixed** (the round-34 §8.2 finding recurs; the L1 owns the wording): the twin's own
`recheck:` line is `source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052` —
byte-for-byte the invocation that exits 0 for the admitted entry. Executing the twin's own line therefore
**does not** reject it, and C2's `kill_rule` clause "junk twin passes source-recheck or is admitted", read
literally against that line, is satisfied. The clause is satisfiable only under the erratum's restatement
(`.ufo/waves/round-35/claims-erratum-d5.md:77-79`: "the twin is rejected only by a discriminating invocation that
pins the twin's own fabricated quote against the committed capture … the comparison, not the twin's `recheck:`
line, is the gate"), which this section measures. The remaining half — a non-author reviewer receipt naming the
twin as refused — is a receipt requirement, not a checker line; this seat did not grade it.

### 9. Frozen C2 cell vs measured bytes

| frozen C2 cell | measured at 07:12:31Z | verdict |
|---|---|---|
| Frontier F18 admitted 17 → 18 | `18` rows, `admitted=18` | match |
| registry row S052, tier A, mined, opened 2026-10-26 | 1 row, `f5=A f9=mined f10=2026-10-26` | match |
| registry 51 → 52 | `52` | match |
| one knowledge entry citing `source: S052` | `1` (47 entries total) | match |
| harness `entries=21 pass=21 exit=0`, incl. `PASS F18 ids=S052` | exactly that, exit 0 | match |
| source-recheck S052 exit 0, every assertion `occurrences=1`, sha256 OK | 5 assertions, 5×`occurrences=1`, `sha256 OK`, exit 0 | match |
| census exit 0, W04 S028/S029 only | exactly that, exit 0 | match |
| junk twin rejected by the admission gate | absent from manifest/table/knowledge; fabricated strings 0/0; discriminating probe `MISMATCH`×2 exit 1; **its own `recheck:` line exits 0** | match under the erratum's restatement only (§8) |

No C2 counting command disagrees with the freeze. The one wording boundary is §8's, and it is the same one the
round-34 verifier routed as D5.

### 10. Determinism, hygiene, and what this seat does not establish

**10.1 Scratch hygiene — an external deletion, reported as a fact.** Scratch root
`/fast/scratch/hyaku/kasegi-r35/ExecCensusAfter/` held `battery.sh`, `wait2.sh`, `final2.sh`, `trace.sh`,
`twin-probe.sh`, `wait.log`, `wait2.log`, `run1.txt`, `run2.txt`, `run-diff.txt`, `dig-before.txt`,
`dig-after.txt`, `dig2-before.txt`, `dig2-after.txt`, `selftest.txt`, `base-tree/`, `suite-scratch/`.
At ~07:12Z, **during pass 3**, the whole tree was deleted by something outside this seat: pass 3's own
`wait3.log` writes began failing with `No such file or directory` at line 29, and `selftest.txt`, `run1.txt`,
`run2.txt`, `wait.log` were gone while the script continued to run and re-created `base-tree/` and its outputs.
Nothing of the lane was touched. Every figure above was already transcribed into this receipt from the read
outputs; the pass-3 poll-by-poll log is the one artifact lost, and §2's 100-second retained trace (re-run on the
same bytes, same digest `bbc53efc…`, same HEAD) stands in its place. This seat's directory was removed with
`rm -rf --` after this file was written.

**10.2 Determinism.** Pass 1 ran the full battery twice; the two transcripts differ in exactly one hunk —
the meta timestamp line (`2026-10-26T06:44:51Z` vs `2026-10-26T06:44:54Z`, `diff` reported `2c2`, i.e. one
changed line; `run_diff_lines=4` counts the two header/marker lines plus both sides). Input digest
sets were sha256'd immediately before and after each pass: `DIGESTS_STABLE=yes`, `DIGESTS_STABLE_run2=yes`,
`SAME_INPUTS_as_run1=yes`.

**10.3 Digest bookends** (schema: `path | pass1 06:44:51Z | pass2 06:58:42Z | pass3 07:12:31Z`):

| path | pass 1 (06:44:51Z) | pass 2 (06:58:42Z) | pass 3 (07:12:31Z) |
|---|---|---|---|
| `corpus/SOURCES.md` | `0f95a132a69e` | `0f95a132a69e` | `0f95a132a69e` |
| `corpus/README.md` | `277f04cedfb0` | `277f04cedfb0` | `277f04cedfb0` |
| `SCORECARD.md` | `51337bf1fd5d` | `51337bf1fd5d` | `ed6e931f795c` |
| `corpus/QUALITY.md` | `807cc714d015` | `d4f83bb1206f` | `d4f83bb1206f` |
| `SKILL.md` | (not in pass-1 digest set) | `daeff71be4d0` | `daeff71be4d0` |
| `corpus/knowledge/cisa-kev-catalog.md` | `0988866608c4` | `e9de994dbe19` | `e9de994dbe19` |
| `corpus/source-snapshots/round-35/manifest.json` | `06bfcc71e6df` | `06bfcc71e6df` | `06bfcc71e6df` |
| `corpus/source-snapshots/round-35/S052.txt` | (not in pass-1/2 set) | (not in pass-2 set) | `d69349e86c5c` |
| `corpus/instruments/r35-defect-closure.sh` | `a4f80067183e` | `0ae4b4848b10` | `0ae4b4848b10` |
| `corpus/instruments/kill-rule-check.py` | `c279d952cba5` | `c279d952cba5` | `c279d952cba5` |
| `corpus/instruments/frontier-recheck-count.py` | `1be79af60cb5` | `1be79af60cb5` | `1be79af60cb5` |
| `corpus/instruments/source-recheck.py` | `fd2e01e88c8c` | `fd2e01e88c8c` | `fd2e01e88c8c` |
| `corpus/lessons/round-35.md` | — | — | `af6e2c99cf83` (uncommitted at that instant) |
| `.ufo/waves/round-35/claims-erratum-d5.md` | — | `eee0bb579844` | `eee0bb579844` |
| `.ufo/waves/round-34/wave1-results.json` | — | — | `3afa3581afb1` (tracked) |

Digests are 12-hex prefixes of the full sha256sum values printed by the runs; full values are reproducible by
re-running `sha256sum` on the listed paths at the §1 commit plus the §1 uncommitted set.


Both C2 surfaces (`SOURCES.md`, `README.md`) are byte-identical across all three instants, i.e. across two L1
commits and 28 minutes — the C2 counters are not a transient. Every surface that moved is a C1/scribe surface
(`SCORECARD.md` at pass 3, the F18 entry body and `r35-defect-closure.sh` between pass 1 and pass 2), and the
entry move did not disturb §6's verdict (recheck exit 0 at both digests).

**10.4 Tooling.** Nothing installed or upgraded this seat; no `pacman`, `uv`, `npx`, `cargo` or network fetch was
run. Instruments used were the committed lane ones plus the fleet `scripts/sources-census.sh` (read-only).

**10.5 What this receipt does not establish.** Not a commit-pinned measurement (§1: working-copy bytes on top of
`87f6b95`); re-run §3–§6 after the L1's final commit and compare with §10.3 — identical digests ⇒ identical
verdicts. Not a fleet-wide census: `--root` is the fleet root but the lane list is `kasegi` only (3 output lines,
one registry). W04 is a warning, not a failure, and is carried from earlier rounds. A8 proves mined `used-by`
paths exist, not that each target cites the row (`capture-binding-check.py`/`source-recheck.py` territory,
measured by other seats). D1b's base extraction is `git archive 3266c99`, which contains no `.ufo/waves/round-34`
tree, so D4's tracking limb reads 0 there by construction as well as by defect — the other six limbs flip on
their own bytes. This seat does not judge the round; it reports the after-state numbers, the §8 wording
boundary, and the replayable commands.

### 11. Post-receipt replay (same bytes, 07:18:51Z)

Re-ran the load-bearing commands after this receipt was written, to prove it still describes live bytes:

```
$ date -u +%Y-%m-%dT%H:%M:%SZ ; git rev-parse --short HEAD
2026-10-26T07:18:51Z
87f6b95
$ sha256sum corpus/SOURCES.md corpus/README.md
0f95a132a69e…  corpus/SOURCES.md      (== §10.3, unchanged since 06:44:51Z)
277f04cedfb0…  corpus/README.md       (== §10.3, unchanged since 06:44:51Z)
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 52
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md -> 18
$ bash corpus/instruments/r35-defect-closure.sh | tail -1 -> closed=7/7 exit=0
```

HEAD unchanged (`87f6b95`), both C2 surfaces at the §10.3 digests, census exit 0 with the same two W04 lines,
registry 52, frontier 18, closure suite 7/7. The receipt describes the live tree.
