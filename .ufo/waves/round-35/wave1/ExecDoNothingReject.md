# ExecDoNothingReject — round 35, wave 1

| field | value |
|---|---|
| seat | ExecDoNothingReject (L2 leaf, executor) |
| round / lane | kasegi-shokunin round 35 |
| lane base | `3266c9937b03062d9bbc2f436e20820115ed179c` |
| claims freeze | `617496b9c6e92bc671e7e78b83df69a04470d0e9` |
| assignment | demonstrate the do-nothing controls (C1 fake suite, C2 shape-only junk twin) are rejected by the real instruments |
| measured at (UTC) | wave evidence block `2026-10-26T06:58:47Z` → `2026-10-26T06:58:51Z` (pre/post hashes byte-identical); D1 recurrence observed `07:00:35Z` and post-fix state `07:01:28Z`; committed-bytes replay on lane head `5a253372d7ccda2fd7829932489481218c3b0efb` at `07:04Z` (see §4) |
| scratch | `/fast/scratch/hyaku/kasegi-r35/ExecDoNothingReject/` (removed before yielding; every path quoted below is the transcript) |
| lane writes | `.ufo/waves/round-35/c1-controls/fake-suite.sh` (authored), `.ufo/waves/round-35/c2-controls/junk-f18.md` (authored), this receipt |
| installs | none (no pacman/uv/npm/`~/.local/bin` transaction) |

## Artifacts under test — digests at the measured state (`sha256sum`, `wc -l`)

```
0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f  corpus/instruments/r35-defect-closure.sh              (834 lines)
b9a07afa1bed7b15b1754e7defee87cdb6233806d0b94b80d8a0acb4529da113  corpus/instruments/r35-fixtures/fixtures.json
6d99ba915272f9424f3d9fb9cc56fbfd6b2fb34c3c3c60c3037d991ef6562563  corpus/instruments/r35-fixtures/README.md
06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee  corpus/source-snapshots/round-35/manifest.json           (1 record: S052, Q1-Q5)
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt                (1479694 B, 27870 lines)
e9de994dbe1940adb894420d566386500e4e29d69d8e6a5244ff2172c71d9761  corpus/knowledge/cisa-kev-catalog.md
292aaac048c9cacff081c24b54fd71fc67a86d3c6ab6845398e0e2856c5be121  .ufo/waves/round-35/c1-controls/fake-suite.sh            (10 lines)  ← this seat
0abec3591e4a2dc5195b23b1c2c920f66052327b7f971aa578af76c3459dc176  .ufo/waves/round-35/c2-controls/junk-f18.md              (23 lines)  ← this seat
```

Check targets at the post-fix state (`07:01:31Z`, after the D1 recurrence in §F7 was corrected):

```
085cffd60be1ad2fac07736e4bbe5c25fb06cace5bdda8707d75352e2575aaaa  SCORECARD.md
daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc  SKILL.md
d4f83bb1206f5084e998d9449c9bef5af06674c325fb66709fe5fbec9d6e2b69  corpus/QUALITY.md
76f190a003931aee3bfbab7fec10aa657c0d64584d0cc0c7fd88b02b3679dc2d  .ufo/waves/round-34/wave1/L1Integration.md
eee0bb579844ad9d02777fb4cd241e726d0bb0630679bc41aa534d7f5d0951e6  .ufo/waves/round-35/claims-erratum-d5.md
```

The block opened with `=== HASHES (pre-run) 2026-10-26T06:58:47Z ===` and closed with
`=== HASHES (post-run) 2026-10-26T06:58:51Z ===`; the two listings are byte-identical, so every
number below was produced on the digests above. Nothing in this seat's write set changed during
the block.

## Report

### 1. Real closure suite vs `.ufo/waves/round-35/c1-controls/fake-suite.sh`

**1a. Real suite on the live tree** — `closed=7/7 exit=0`:

```
$ bash corpus/instruments/r35-defect-closure.sh
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
live_exit=0
```

**1b. Real suite on the claims-freeze tree** (`git archive 617496b9 | tar -x -C "$S/base617"`,
`archive_exit=0`; `ls "$S/base617/corpus/instruments/r35-defect-closure.sh"` → `No such file`
`ls_exit=2`, so the base export carries no suite) — `closed=0/7 exit=1`:

```
$ bash corpus/instruments/r35-defect-closure.sh --root $S/base617
D1 check=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0 open=1
D2 check=erratum-row=0,erratum-mean=0,row-bytes=1 open=1
D3 check=registry-r-defect-closure=0,registry-kill-rule=0 open=1
D4 check=tracked=0,provenance=0 open=1
D5 check=erratum-file=absent,discriminating-invocation=0,per-id-occurrences=0 open=1
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=0/7 exit=1
base_exit=1
```

**1c. Real suite `--selftest`** — `cases=7 failures=0`, exit 0, with one `selftest case=D<i>` line
per defect and 17 clause-mutant detail lines (D1 3, D2 3, D5 3, D3/D4/D6/D7 2 each):

```
$ bash corpus/instruments/r35-defect-closure.sh --selftest
selftest detail=D1 fixture reason=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0
selftest detail=D1 mutant=placeholders reason=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=3
selftest detail=D1 mutant=lane-hash-markers reason=placeholders=0,lane-hash-markers=1,correction-c1c6a5f=3
selftest detail=D1 mutant=correction-c1c6a5f reason=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=0
selftest case=D1 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest detail=D2 fixture reason=erratum-row=0,erratum-mean=0,row-bytes=1
selftest detail=D2 mutant=erratum-row reason=erratum-row=0,erratum-mean=1,row-bytes=1
selftest detail=D2 mutant=erratum-mean reason=erratum-row=1,erratum-mean=0,row-bytes=1
selftest detail=D2 mutant=row-bytes reason=erratum-row=1,erratum-mean=2,row-bytes=0
selftest case=D2 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest detail=D3 fixture reason=registry-r-defect-closure=0,registry-kill-rule=0
selftest detail=D3 mutant=registry-r-defect-closure reason=registry-r-defect-closure=0,registry-kill-rule=1
selftest detail=D3 mutant=registry-kill-rule reason=registry-r-defect-closure=1,registry-kill-rule=0
selftest case=D3 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest detail=D4 fixture reason=tracked=0,provenance=0
selftest detail=D4 mutant=tracked reason=tracked=0,provenance=1
selftest detail=D4 mutant=provenance reason=tracked=1,provenance=0
selftest case=D4 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest detail=D5 fixture reason=erratum-file=present,discriminating-invocation=2,per-id-occurrences=0
selftest detail=D5 mutant=erratum-file reason=erratum-file=absent,discriminating-invocation=0,per-id-occurrences=0 cascade=1
selftest detail=D5 mutant=discriminating-invocation reason=erratum-file=present,discriminating-invocation=0,per-id-occurrences=5
selftest detail=D5 mutant=per-id-occurrences reason=erratum-file=present,discriminating-invocation=5,per-id-occurrences=0
selftest case=D5 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest detail=D6 fixture reason=dead-seat-sentence=1,correction-round-35=0
selftest detail=D6 mutant=dead-seat-sentence reason=dead-seat-sentence=1,correction-round-35=1
selftest detail=D6 mutant=correction-round-35 reason=dead-seat-sentence=0,correction-round-35=0
selftest case=D6 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest detail=D7 fixture reason=supersedes-R22=0,supersedes-R23=0
selftest detail=D7 mutant=supersedes-R22 reason=supersedes-R22=0,supersedes-R23=1
selftest detail=D7 mutant=supersedes-R23 reason=supersedes-R22=1,supersedes-R23=0
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

The two `selftest control=` lines are the suite's own positive/negative controls on the judgement
itself: `control=clean` (a report from a fully closed tree is accepted) and `control=two-defect`
(a report from a tree with D1/D2 open is read as `closed=5/7 failed=D1,D2`), so `report_ok` is not
a constant and the seven live runs are load-bearing in both directions.

**1d. The fake suite** — summary-only, by construction:

```
$ cat .ufo/waves/round-35/c1-controls/fake-suite.sh        # 10 lines, no check table
#!/usr/bin/env bash
# Do-nothing control for C1: prints the claimed after-state without performing
# any check. The real suite must distinguish itself: its --selftest must run
# seven real checks each shown able to fail on a defect-bearing fixture copy.
if [ "${1:-}" = "--selftest" ]; then
  echo "cases=7 failures=0"
else
  echo "closed=7/7 exit=0"
fi
exit 0

$ bash .ufo/waves/round-35/c1-controls/fake-suite.sh
closed=7/7 exit=0
fake_plain_exit=0
$ bash .ufo/waves/round-35/c1-controls/fake-suite.sh --selftest
cases=7 failures=0
fake_selftest_exit=0
fake_case_lines=0
fake_total_lines=1
```

**1e. The real suite's own judge applied to the fake, outside the suite.** `report_ok()` /
`plain_report_ok()` / `fix_re()` / `CHECK_IDS` were extracted **verbatim** from the measured suite
bytes (`corpus/instruments/r35-defect-closure.sh`, extraction at run time inside the block:
`extracted 45 lines`) and applied to the fake's captured stdout:

```
$ bash apply.sh judge-lib.sh fake-selftest.txt selftest
judge=selftest accepted=0 report=…/judge/fake-selftest.txt
judge_selftest_exit=1
$ bash apply.sh judge-lib.sh fake-plain.txt plain
judge=plain accepted=0 report=…/judge/fake-plain.txt
judge_plain_exit=1
```

Inside the suite the same judgement runs by name — `selftest judge=fake-suite rejected=1
path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0` and `selftest
judge=fake-plain rejected=1 output=closed=7/7 exit=0` (§1c), with no `problem=judge … accepted`
line.

**Comparison — why the fake cannot satisfy the discriminator.** The discriminator is the suite's
own `report_ok` (`r35-defect-closure.sh:522-547` at the measured digest): a pass needs exactly seven
`^selftest case=D[1-7] live=pass fixture=rejected mutants=n/n others=6/6 verdict=pass$` lines with
distinct ids `D1..D7`; for each id a `selftest detail=D<i> fixture reason=…` line whose payload
contains that defect's own clause regex (`fix_re`: D1 `placeholders=[1-9]`, D2 `erratum-row=0`, D3
`registry-r-defect-closure=0`, D4 `tracked=0`, D5 `erratum-file=absent`, D6
`dead-seat-sentence=[1-9]`, D7 `supersedes-R22=0`); at least one
`selftest detail=D<i> mutant=… reason=…` line per id; and the case line's `mutants=n/n` count equal
to that id's mutant-detail count. `plain_report_ok` applies the same rule to the plain run (seven
named `D<i> check=… open=0|1` lines plus a `closed=K/7` summary agreeing with the open counts).

1. **Shape.** The fake's `--selftest` is one line; the real run is 7 case lines + 17 mutant detail
   lines + 7 fixture detail lines + 2 control lines + 6 judge lines + a summary —
   `fake_case_lines=0` vs `real_case_lines=7`.
2. **No line it can print suffices.** The case-line schema is a *result record*: `mutants=n/n` is
   cross-checked against the detail lines it claims, and the fixture payload must match that
   defect's clause semantics. A summary-only fake fails at the first predicate (`lines == 7`
   → 0); a fake that emitted seven constant case lines still fails on the missing fixture/mutant
   detail lines and the `mutants=n/n` ↔ detail-count equality — which is exactly what the suite
   demonstrates with its `forged-caselines` forgery (`selftest judge=forged-caselines rejected=1`).
3. **Same bytes, opposite verdicts, and the fake cannot even be aimed.** The fake has no argument
   parsing, so it ignores `--root`:

```
$ bash .ufo/waves/round-35/c1-controls/fake-suite.sh --root $S/base617
closed=7/7 exit=0
fake_root_exit=0
$ bash .ufo/waves/round-35/c1-controls/fake-suite.sh --selftest --root $S/base617
cases=7 failures=0
exit=0
```

   On the identical base-tree bytes (§1b) the real suite reads `closed=0/7 exit=1` while the fake
   reads `closed=7/7 exit=0`; on the landed tree both read 7/7. The fake therefore reports the
   after-state on a tree where all seven defects are open — it is an unfalsifiable printer, which
   is why the frozen base comment in `c1-controls/before.txt` (`ls_exit=2`, `filled by the L1` = 1,
   `201.7` = 2, `supersedes R22/R23` = 0 0) is the load-bearing negative, not the fake's string.

### 2. C2 counters on a do-nothing tree (`git archive 617496b9`, no F18 work)

```
=== 2a. C2 counters on base617 (do-nothing) ===
frontier_admitted=17
registry_rows=51
S052_rows=0
entries_citing_S052=0
knowledge_entries=46
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
entries=20 pass=20 exit=0
base_harness_exit=0
manifest UNAVAILABLE reason=missing
base_recheck_exit=2
```

Cell for cell this matches `c2-controls/before.txt` (17 / 51 / 0 / 0 / `entries=20 pass=20 exit=0` /
`manifest UNAVAILABLE reason=missing`, `recheck_exit=2` / 46), so the frozen before-state is
reproducible from the freeze commit alone and the do-nothing tree misses every C2 after-value.

Live tree, same commands, for contrast:

```
=== 2b. C2 counters on the live tree (contrast) ===
frontier_admitted=18
registry_rows=52
S052_rows=1
entries_citing_S052=1
knowledge_entries=47
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
entries=21 pass=21 exit=0
live_harness_exit=0
```

Separately run on the live tree: `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kasegi` → exit 0, output naming only
`kasegi W04 S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq
across scopes`, `kasegi W04 S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across
scopes`, `kasegi ok …/corpus/SOURCES.md`.

### 3. Real S052 recheck vs the junk twin's fabricated quote

**3a. Real pinned entry** — `exit 0`, every assertion `occurrences=1` and anchored:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
S052:sha256 OK
S052:Q1 OK occurrences=1 anchor=2-ok
S052:Q2 OK occurrences=1 anchor=3-ok
S052:Q3 OK normalized=markup-whitespace occurrences=1 anchor=4-ok
S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=15472-ok
S052:Q5 OK normalized=markup-whitespace occurrences=1 anchor=19165-ok
real_recheck_exit=0
```

**3b. The twin's assertions, adjudicated against the same pinned bytes.** Two scratch manifests were
built from the real one (same `path`, same `sha256`, `S052.txt` copied beside it), each carrying
**only** one of the twin's asserted strings as `JUNK1`; the driver first measures each string's raw
and normalized occurrence count in `S052.txt`:

```
twin=.ufo/waves/round-35/c2-controls/junk-f18.md
capture=S052.txt sha256=d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826
real_record_quotes=['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
asserted_strings:
  raw=0 normalized=0  'five exploited vulnerabilities to the catalog every Tuesday'
  raw=0 normalized=0  'scores each entry with a CVSS v4 vector rather than a\ndue-date'

--- junk twin assertion junk-1 (quote='five exploited vulnerabilities to the catalog every Tuesday') ---
S052:sha256 OK
S052:JUNK1 MISMATCH reason=quote-not-found
exit=1

--- junk twin assertion junk-2 (quote='scores each entry with a CVSS v4 vector rather than a\ndue-date') ---
S052:sha256 OK
S052:JUNK1 MISMATCH reason=quote-not-found
exit=1
```

The `S052:sha256 OK` line in both runs is the control inside the control: the scratch manifest
points at the *real* capture bytes, so the `MISMATCH` is a quote-level rejection on authentic bytes,
not a missing-file artefact.

**3c. Two further negatives on the same instrument:**

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S999
S999:source UNAVAILABLE reason=not-listed
unknown_source_exit=2

$ python3 corpus/instruments/source-recheck.py --manifest $S/sha-swap/manifest.json --source S052
S052:sha256 MISMATCH expected=0000000000000000000000000000000000000000000000000000000000000000 actual=d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826
sha_swap_exit=1
```

**3d. What a shape gate cannot see.** The same twin satisfies every shape counter:

```
shape_h1=1 shape_source=1 shape_recheck=1 shape_verified_at=1
```

i.e. H1 header, a `source: S052 —` line, a `recheck:` line and a `verified-at:` line, 4/4 — while
the real gate rejects its asserted content (`reason=quote-not-found`, exit 1) and the registry has no
row for it (`S052_rows=0` in the twin: `grep -c '^| S052' .ufo/waves/round-35/c2-controls/junk-f18.md`
→ 0). The rejection therefore rests on capture bytes and the manifest record, not on shape.

### 4. Committed-bytes replay (does the measurement survive the commit?)

Measured after the L1 committed the wave (`5a253372d7ccda2fd7829932489481218c3b0efb`) — first on a
`git archive` export, then on a clone of the same commit:

```
$ git archive 5a253372… | tar -x -C $S/head5a25          # export_ok
$ ls $S/head5a25/corpus/source-snapshots/round-35/
S052.txt
manifest.json
$ ls $S/head5a25/.ufo/waves/round-35/c1-controls/ $S/head5a25/.ufo/waves/round-35/c2-controls/
before.txt  fake-suite.sh
before.txt  junk-f18.md
$ python3 $S/head5a25/corpus/instruments/source-recheck.py \
      --manifest $S/head5a25/corpus/source-snapshots/round-35/manifest.json --source S052
S052:sha256 OK … (six OK lines) …
head_recheck_exit=0
```

```
$ bash $S/head5a25/corpus/instruments/r35-defect-closure.sh --root $S/head5a25
D1 … open=0   D2 … open=0   D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=0,provenance=1 open=1
D5 … open=0   D6 … open=0   D7 … open=0
closed=6/7 exit=1
```

`D4 tracked=0` is the export artefact, not a defect: `check_d4` reads `git ls-files`, and an archive
carries no index. On a clone of the same commit both predicates reproduce exactly:

```
$ git clone -q <lane> $S/clone5a25 && git -C $S/clone5a25 checkout -q 5a253372…
checked out 5a25337
$ bash corpus/instruments/r35-defect-closure.sh --root $S/clone5a25 | tail -1
closed=7/7 exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
… S052:Q5 OK normalized=markup-whitespace occurrences=1 anchor=19165-ok
clone_recheck_exit=0
```

C2 cells on the same export: `frontier=18 rows=52 s052=1 citing=1`,
`PASS F18 knowledge/cisa-kev-catalog.md ids=S052`, `entries=21 pass=21 exit=0`.

The worktree at the time of this replay carried ` M .ufo/waves/round-35/wave1/ExecD1Markers.md`
(another seat's post-commit write, not this seat's file and not mine to revert).

## Findings for the L1 (no artifacts edited by this seat outside its write set)

- **F1 — the twin's own `recheck:` line passes; the discriminating invocation is the scratch-manifest
  run in §3b.** Running the twin's line verbatim (`python3 corpus/instruments/source-recheck.py
  --manifest corpus/source-snapshots/round-35/manifest.json --source S052`) prints the six `OK`
  lines and `twin_own_recheck_exit=0`, because that line cites the *real* record. This is the same
  wording hazard round-34's D5 recorded, and it is why the frozen C2 claim's "junk twin is rejected
  by the admission gate" must be read with §3b's invocation attached (the erratum file
  `.ufo/waves/round-35/claims-erratum-d5.md` carries `discriminating-invocation` = 5 at the measured
  digest). No wording change is needed in the twin: it asserts nothing about itself and its two
  quoted strings measured `raw=0 normalized=0` (round-34's twin, by contrast, carried one fragment
  that really occurred).
- **F2 — the fake is unfalsifiable on any tree and cannot be aimed at one.** It prints
  `closed=7/7 exit=0` even with `--root $S/base617`, where the real suite reads `closed=0/7 exit=1`
  (§1e item 3). That is the strongest single demonstration that the suite's number is a measurement
  and the fake's is a constant.
- **F3 — the fake-suite judgement degrades silently if the control file is removed.**
  `r35-defect-closure.sh:593-612` (measured digest) selects the first existing candidate among
  `.ufo/waves/round-35/c1-controls/fake-suite.sh` and
  `.ufo/waves/round-34/c1-controls/fake-suite.sh`; if neither exists it prints `selftest
  judge=fake-suite absent=1` and **continues**, so `--selftest` still exits 0 with the rejection
  evidence gone. Since this seat authored the first candidate, a cleanup pass that deletes it
  downgrades §1c's line to `absent=1`. Recommendation for the suite owner (not this seat's file):
  treat `absent=1` as a failure, or keep the fixture and record the reason in
  `corpus/instruments/r35-fixtures/README.md`.
- **F4 — count correction: 17 clause mutants, not 15.** `ExecClosureSuite`'s message to this seat
  described "fifteen clause mutants"; the measured report carries `grep -cE '^selftest detail=D[1-7]
  mutant='` → `17` (three each for D1/D2/D5, two each for D3/D4/D6/D7), and
  `grep -oE 'mutants=[0-9]+/[0-9]+' | sort | uniq -c` → `4 mutants=2/2`, `3 mutants=3/3`. The claim
  documents do not quote a mutant count, so nothing frozen is contradicted; the prose figure is the
  one to fix wherever it was repeated.
- **F5 — the suite was revised during the wave; this receipt pins the final bytes.**
  `58ca3115…` (643 lines, seen at `06:35:24Z`) → `0ae4b484…` (834 lines, the digest every number
  above was measured on). At the intermediate tree state `06:56:47Z` the same final bytes read
  `closed=4/7 exit=1` with `D4 tracked=0`, `D6 correction-round-35=0`, `D7 supersedes-R22=0`; at
  `06:58:35Z` all three closed (D4 needed the L1's index action, which no seat may perform). A
  reviewer replaying against a different suite digest, or before those three land, will not see
  `cases=7 failures=0`; that is tree state, not a suite defect.
- **F6 — the C2 counters are tree-state snapshots.** `entries_citing_S052=1` and
  `knowledge_entries=47` were measured at `cisa-kev-catalog.md` = `e9de994d…`; if a scribe revises
  that entry, the harness line changes but the §2a do-nothing cells cannot.
- **F7 — D1 reopened after the first green measurement, by the round-35 scorecard's own closing
  sentence.** Timeline on unchanged suite bytes (`0ae4b484…`):

  | UTC | live tree | cause |
  |---|---|---|
  | `06:56:47Z` | `closed=4/7 exit=1` — `D4 tracked=0`, `D6 correction-round-35=0`, `D7 supersedes-R22=0` | D4/D6/D7 not yet landed; D4 needs the L1's index action |
  | `06:58:47Z` | `closed=7/7 exit=0`, `--selftest cases=7 failures=0` | the measured evidence state for §1–§3 |
  | `07:00:35Z` | `closed=6/7 exit=1` — `D1 check=placeholders=1,… open=1` | `SCORECARD.md:1271` (written `07:00:01Z`, digest `04365925…`): `… ; final lane commit filled by the L1 in the closing commit.` |
  | `07:01:28Z` | `closed=7/7 exit=0` | the sentence was reworded (SCORECARD.md `085cffd6…`); D1 `placeholders=0` |

  The C1 immutability claim is therefore state-dependent within the wave: the same suite digest gave
  two different verdicts eight minutes apart, and the reopen was a *prose* edit in a file no C1
  defects D2/D4–D7 touch. This seat reported it to the L1, which committed the fix (`8ce6fb4f`) —
  recorded here as the measured sequence, not as a judgement of C1.
- **F8 — D1's matcher is a literal substring, so any sentence that names who fills the closing
  commit reopens it.** `check_d1` uses `grep -c -F -- 'filled by the L1'` (`r35-defect-closure.sh:164`).
  The defect it targets is an *unfilled placeholder line*, but the check forbids the phrase anywhere
  in `SCORECARD.md`, including a measurement-state sentence that merely describes the commit
  process. That is the round-34 D1 class ("widen the R1 check to placeholder prose") implemented
  one step too literally: the scribe's natural wording re-mints the defect. Options for the suite
  owner: match the placeholder *form* (`final lane commit.*filled by the L1`, or a line whose only
  content is the placeholder), or require the scorecard's closing commit to be a hash citation.
  Not this seat's file, so recorded only.
- **F9 — wave writes landed after the L1's first push, and they mattered.** On `8ce6fb4f`,
  `git status --porcelain` listed `M .ufo/waves/round-35/build-spec.py`, `M SKILL.md`, and untracked
  `corpus/source-snapshots/round-35/S052.txt`, `c1-controls/fake-suite.sh`, `c2-controls/junk-f18.md`,
  `wave1.ready`, `wave1.ready.dispatched`, `wave1/ExecDoNothingReject.md`, `wave1/ScribeLesson.md`.
  Two of those were load-bearing, proven on a `git archive 8ce6fb4f` export: (a) `source-recheck
  --source S052` read `S052:source UNAVAILABLE reason=missing`, exit 2 — C2's frozen exit-0
  predicate did not reproduce from the commit; (b) the suite read `closed=5/7 exit=1` with
  `D3 registry-r-defect-closure=0,registry-kill-rule=0` — the registry rows lived only in the
  uncommitted `SKILL.md`. The L1 committed the pending set as `5a253372…`, after which §4's replay
  reproduces both predicates. The residual worktree modification at the time of that replay was
  ` M .ufo/waves/round-35/wave1/ExecD1Markers.md`.
- **F10 — the closure suite is not replayable from a `git archive`; only from a clone.** `check_d4`
  reads `git ls-files`, so an archive export always reports `tracked=0` and the suite reads
  `closed=6/7 exit=1` on a tree whose every defect is closed (§4, both sides measured). No header
  line states this; line 67 mentions "git-free export" only for D2's append-only reading. A
  non-author following the claim's "run the suite and read `closed=7/7`" will fail on an archive.
  Recommendation for the suite owner: state the replay recipe (`git clone` / a worktree, not
  `git archive`) in the suite header and in `corpus/instruments/r35-fixtures/README.md`, or let D4
  fall back to a committed tracked-file manifest when no index is present.

## Scope, cleanup, tooling

- Lane writes: the two control fixtures named above and this receipt. No `git add/commit/push`, no
  `jj` mutation; every git command run was read-only (`git archive` of `617496b9` / `8ce6fb4f` /
  `5a253372` into scratch, `git clone <lane>` into scratch, `git status`, `git log`, `git show`,
  `git cat-file -e`, `git check-ignore`). No write to `/home/vgpnk/Projects/shokunin`,
  `/home/vgpnk/Projects/shokuknow`, `bounties`, or any sibling lane. One read-only
  `scripts/sources-census.sh validate` run (it writes nothing into the fleet root).
- Scratch `/fast/scratch/hyaku/kasegi-r35/ExecDoNothingReject/` contained the base export, the four
  scratch manifests, the judge extraction/wrapper, the twin driver and `suite-scratch`; it was
  `rm -rf`'d before yielding. No scratch tree is left on disk.
- No installs or upgrades (pacman transactions untouched; no `uv`/`npm`/binary install).
- Verdict scope: the do-nothing controls are rejected by the landed instruments on the digests
  above, and the C2 do-nothing tree misses every after-value. This seat does not judge C1/C2
  soundness as a whole; the L1 integrates and the critics review.
