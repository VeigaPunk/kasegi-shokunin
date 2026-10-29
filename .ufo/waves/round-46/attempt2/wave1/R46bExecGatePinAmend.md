VERDICT: DRAFT-READY

# R46bExecGatePinAmend — the r46-c2-gate.py v1.3 ledger exemption (round 46, attempt 2, lane kasegi)

Seat scope: build the v1.3 amendment of the attempt-1 C2 counter that exempts
`considerthese-proposals-ledger.md` from the byte pin (name pinned, size may grow never shrink), mirror it in the
C2 selftest's synthetic-tree builder, and prove the four named checks. Drafts only; nothing committed, nothing in
the committed instrument paths touched.

## 1. What was built (two complete files, in my draft directory only)

| file | path | sha256 |
|---|---|---|
| v1.3 gate | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/r46-c2-gate.py` | `7d6d604d056136127bd2738199b544526d4d2bd32936708f79696cb239837dbb` |
| v1.3 selftest | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/r46-counters-selftest-c2.py` | `37a723c0952af8523f17e79e949e2e3670783dc126dc1f35047d653b9c73814a` |

Committed originals (untouched): `corpus/instruments/r46-c2-gate.py` sha256 `647bd5b7b62685519d8d396bf2d02eca7ad0bb440dd5c4041beabfaa45ea2909`,
`corpus/instruments/r46-counters-selftest-c2.py` sha256 `ff7104cfc891007160c6e474bf1f3b00a9e0b25e6ca9aed96559ea648c2b688f`.

### 1.1 The gate amendment (`r46-c2-gate.py` draft, five edits, nothing else touched)

- **draft:2** — version line `v1.2` -> `v1.3 (attempt-2 erratum E3: the considerthese ledger joins the content-exempt set — its name stays pinned, its bytes may grow never shrink; v1.2's hardening (errata E1 and E2 …) is unchanged; v1 sha256 0ee95857… unchanged)`. The id `E3` is the one the L1's own attempt-2 errata log already reserves for this amendment (`.ufo/waves/round-46/attempt2/counter-errata.md`, section "E3 — r46-c2-gate.py v1.2 -> v1.3 ledger exemption"); my first draft wrote `C2-E7`, which collides with the attempt-1 errata's `C2-E7` (`r46-c2-gate.py:78`, the v1.1 -> v1.2 G1 clause), and the label was corrected before the final run.
- **draft:34-38** — the G6 limb sentence: `61 of them are pinned byte for byte, and three entries are exempt from the byte pin (names pinned, size may grow never shrink): the two entries claim C1 re-grounds, and the considerthese ledger, which the round-46 attempt-2 wave appends the dispositions to.`
- **draft:69** — `PINS["base-knowledge-content"]` `5e0796fd3617f7626880950a5b25d1818f58eff58a12dec99ce7a0f3836b8f47` -> `2c4ccfb65fdb5b727a3bc0c2465f6091b535663abd81126b81e76fdaae83a9a7`
  (the pin is re-derived because the exempt set grew by one file: it is the sha256 of
  `"\n".join("%s %s" % (name, sha256(bytes)) for name in base_like if name not in CONTENT_EXEMPT)` over the 61
  non-exempt base entries — `base_like` = the 64 base names minus the F28 entry).
- **draft:74** — `CONTENT_EXEMPT = {"claim-package-contract.md", "claim-gates.md", "considerthese-proposals-ledger.md"}`
- **draft:75** — `EXEMPT_BASE_SIZE = {'claim-gates.md': 6742, 'claim-package-contract.md': 5169, 'considerthese-proposals-ledger.md': 30696}`
  — the shape of the two C1 entries mirrored: a floor in bytes, so the ledger may grow never shrink.
- **draft:340** — the `g6()` comment updated to name the three exempt entries.

The `30696` floor is the ledger's own byte size at the freeze tip, i.e. the value `r46-f29-gate.py:80-81` already uses
for the same file (`LEDGER = "considerthese-proposals-ledger.md"`, `LEDGER_MIN_BYTES = 30696  # the ledger's byte size at the freeze tip; it may grow, never shrink`):

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && for r in 04af9bc92229232ea5cce8b32bfe59dd969eb26d fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4 ee03806b6b54a2822045e96641a77fa76984b410; do echo "== $r"; git cat-file -s "$r:corpus/knowledge/considerthese-proposals-ledger.md"; done
== 04af9bc92229232ea5cce8b32bfe59dd969eb26d
30696
== fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4
30696
== ee03806b6b54a2822045e96641a77fa76984b410
30696
```

The two C1 floors are the same kind of number: the pure base export's own byte size for those entries
(`claim-gates.md` 6742, `claim-package-contract.md` 5169 in `/fast/scratch/hyaku/kasegi-r46/L1/pure2`).

### 1.2 The matching change in the selftest's synthetic-tree builder (`r46-counters-selftest-c2.py` draft, five edits, no case added or removed)

- **draft:2, 16-20** — docstring: the counter under test is v1.3; "The base's three content-exempt entries (the two C1 entries and the considerthese ledger) are the BASE bytes; `land_c1` swaps in the lane's current bytes for all three".
- **draft:62-63** — new constants `LEDGER = "considerthese-proposals-ledger.md"` and `EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}` (the builder's mirror of the counter's `CONTENT_EXEMPT`).
- **draft:310-315** — the two knowledge files a delete/rename mutant may touch (`spare`, `spare2`) now exclude `EXEMPT_ENTRIES`, not only `C1_ENTRIES`: a byte change to a content-exempt entry must never be expected to trip G6's byte pin.
- **draft:357-359** — `land_c1` now copies the lane's current bytes for all three exempt entries (the ledger is the file the attempt-2 wave appends the dispositions to), and **draft:361-362** keeps the "the lane's bytes differ from the base's" non-vacuity assertion scoped to the two claim entries (the ledger is currently byte-identical to the base, so the assertion would fail on it).

**No expectation, case, or counter-output was changed** — the case count is unchanged at 137.

## 2. The four named checks (commands and printed output)

### (1) The v1.3 gate on the LIVE lane still prints `c2-gate fixed=7/7 exit=0`

The draft was run from a tree-shaped copy so that the counter's `TOOL_ROOT` (draft:61 -> `corpus/instruments/source-recheck.py`) resolves; the draft bytes and the run bytes are identical (sha256 `10c3d816…` in both).

```
$ mkdir -p $S/v13 && git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive HEAD corpus/instruments | tar -x -C $S/v13
$ cp .../R46bExecGatePinAmend.draft/r46-c2-gate.py $S/v13/corpus/instruments/r46-c2-gate.py
$ TMPDIR=$S/tmp python3 $S/v13/corpus/instruments/r46-c2-gate.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 anchored=1 table-rows=8 xrefs=4/4
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=1 read=spans=27 located=27 failed=0 uncited=0 cores=5/5
gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=7/7 exit=0
exit=0
```

### (2) The v1.3 selftest still prints `selftest cases=137 failures=0`

```
$ HYAKU_SCRATCH=$S TMPDIR=$S/tmp python3 .../R46bExecGatePinAmend.draft/r46-counters-selftest-c2.py \
    --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 \
    --counter $S/v13/corpus/instruments/r46-c2-gate.py
…
ok   control ctl-complete-tree fixed=7/7 failing=[]
ok   mutant  mut-fabricated-quote fixed=6/7 failing=['G5']
…
selftest cases=137 failures=0
exit=0
```

### (3) A scratch tree where the ledger is REPLACED by a shrunk file still reads G6 red

The tree is a lane-HEAD `corpus` export with `corpus/knowledge/considerthese-proposals-ledger.md` replaced by a 16-byte file.

```
$ TMPDIR=$S/tmp python3 $S/v13/corpus/instruments/r46-c2-gate.py --root $S/shrunk
gate G6 pass=0 read=symlinks=0 exempt-entries-not-shrunk=0
…
c2-gate fixed=6/7 exit=1
exit=1
```

The read token is the non-shrink guard itself (`exempt-entries-not-shrunk=0`), not the byte pin — the ledger's bytes
are no longer pinned, but it may not be gutted. The same tree under the old v1.2 bytes reads
`gate G6 pass=0 read=knowledge=65 entries=65 nested-md=65 base-intact=0 entry-bytes-ok=1` / `c2-gate fixed=6/7 exit=1`
(a different reason: the content pin).

### (4) The v1.2 gate at the freeze-era export still reads 7/7

```
$ mkdir -p $S/v12 && git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive eb874bc86ad7a6cfec299088e5a2d7ec68cf61b7 corpus/instruments | tar -x -C $S/v12
$ sha256sum $S/v12/corpus/instruments/r46-c2-gate.py /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-c2-gate.py
647bd5b7b62685519d8d396bf2d02eca7ad0bb440dd5c4041beabfaa45ea2909  $S/v12/corpus/instruments/r46-c2-gate.py
647bd5b7b62685519d8d396bf2d02eca7ad0bb440dd5c4041beabfaa45ea2909  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-c2-gate.py

$ TMPDIR=$S/tmp python3 $S/v12/corpus/instruments/r46-c2-gate.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
…
gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=7/7 exit=0
exit=0
```

The receipts' historical basis is intact: the bytes at `eb874bc` are byte-identical to the committed v1.2 counter, and
that counter still reads 7/7 on the live lane. (`source-recheck.py` in both exports is sha256 `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`, the pin at draft:68.)

## 3. Discrimination against a do-nothing control

The amendment is not a no-op: on a tree whose ledger GREW (30696 -> 30753 bytes, the shape of the attempt-2
dispositions append), v1.3 stays green while the old v1.2 bytes go red on G6.

```
$ TMPDIR=$S/tmp python3 $S/v13/corpus/instruments/r46-c2-gate.py --root $S/grown
gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
c2-gate fixed=7/7 exit=0

$ TMPDIR=$S/tmp python3 $S/v12/corpus/instruments/r46-c2-gate.py --root $S/grown
gate G6 pass=0 read=knowledge=65 entries=65 nested-md=65 base-intact=0 entry-bytes-ok=1
c2-gate fixed=6/7 exit=1
```

Selftest controls (all four runs against the same `--pure /fast/scratch/hyaku/kasegi-r46/L1/pure2`):

| selftest | counter | printed |
|---|---|---|
| committed v1.2 (baseline) | committed v1.2 | `selftest cases=137 failures=0` |
| committed v1.2 (unmodified) | draft v1.3 | `selftest cases=137 failures=0` |
| draft v1.3 | draft v1.3 | `selftest cases=137 failures=0` |
| draft v1.3 with `--do-nothing-control` | stub that always prints 7/7 | `selftest cases=137 failures=118` |

The do-nothing control grades 118 of the 137 cases as failures (`FAIL mutant mut-fabricated-quote fixed=7/7 failing=[]  <- ACCEPTED-targeted-gate-passes=['G5']; tree read 7/7`), so the suite is not vacuous and the 137/0 result is a measurement, not an artefact.

Receipts (quoted output, not paraphrased): `.ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/receipts/`
(`gate-*.txt`, `selftest-*.txt`).

## 4. Findings for the L1 (not acted on — outside this seat's item)

**F1 (HIGH, pre-existing, not caused by this amendment): the attempt-1 C2 counter cannot read 7/7 once the F29 wave lands.**
Reproduced on scratch trees built from the lane-HEAD export:

```
$ TMPDIR=$S/tmp python3 $S/v13/corpus/instruments/r46-c2-gate.py --root $S/f29      # 66th entry added, rows still 28
gate G6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1
c2-gate fixed=6/7 exit=1

$ TMPDIR=$S/tmp python3 $S/v13/corpus/instruments/r46-c2-gate.py --root $S/f29row   # + the F29 frontier row
gate G1 pass=0 read=rows=29 admitted=29 dup=0
gate G6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1
c2-gate fixed=5/7 exit=1
```

G1 (`r46-c2-gate.py:181` in the v1.3 draft, `:178` in the committed v1.2) demands exactly 28 frontier rows and G6
(`:350` / `:347`) exactly 65 knowledge entries, and the base-names pin covers all 64 non-F28 names, so the F29 entry
breaks the names pin as well. The ledger exemption does
not and cannot fix this; it only removes the ledger append as a second, avoidable cause. Widening G1/G6 to the
attempt-2 shape changes counter limb sentences, so it is a counter erratum for the L1 to decide — this seat did not do
it.

**F2 (HIGH, consequence of F1): the C1 claim's kill rule can fire through the battery baseline.**
`corpus/instruments/r46-mutbat.py:97-107` runs the C2 selftest from the tree **without `--lane`**, so the selftest's
default `--lane` is the live lane and the case `ctl-committed-tip-direct`
(`r46-counters-selftest-c2.py:537` committed / `:540` in the v1.3 draft, "the counter run on --lane itself … must read 7/7")
grades the live lane. Once the
F29 entry and row are landed, that control reads 5/7 -> `failures=1` -> `r46-mutbat.py:152-154` prints
`BASELINE-DIRTY` -> C1's kill rule (`baseline_failures!=0`) fires. The same holds for the v1.3 selftest draft: the
synthetic trees are unaffected (they are built from `--pure`, 64 base entries + the F28 entry), only the direct control
is coupled to the live lane. The L1 owns the fix (fold the F29 shape into the attempt-1 counter as a logged erratum,
or re-base that control); this seat did not widen it.

**F3 (integration note): the `CONTENT_EXEMPT` edit and the `base-knowledge-content` pin edit are atomic.** Landing
the exemption without the re-derived pin value (or the other way round) makes G6 read `base-intact=0` on every tree.
Both edits are in the same draft file; they must land together.

**F4 (overlap): two seats are editing the same selftest file.** `R46bExecSelftestC2` extends
`r46-counters-selftest-c2.py` with the C1 claim's new cases; my draft also edits it (section 1.2). I messaged that
peer with the exact five edits and the rule "never pick a content-exempt file as a G6 byte-pin mutant target".

**F5 (running artifact, not a defect): `gate G4 pass=0 read=exception-FileNotFoundError` when the draft is run from
the draft directory.** `r46-c2-gate.py:61` in the v1.3 draft (`:58` in the committed v1.2) derives `TOOL_ROOT` from the
script's own path, so `corpus/instruments/source-recheck.py`
does not resolve from `.ufo/waves/round-46/attempt2/wave1/…`. Every number quoted in this report was produced from a
tree-shaped copy under `corpus/instruments/` (draft bytes == run bytes, sha256 checked). Once the L1 installs the file
at `corpus/instruments/r46-c2-gate.py`, G4 resolves as it does for the committed v1.2.

**F6 (one-line divergence from the L1's errata text, for the L1's ruling): the G6 limb SENTENCE is edited in the
draft, although the attempt-2 errata log's E3 section says "G6's sentence … is unaffected".**
The rule is untouched (the names pin, the byte pin over the non-exempt entries, the non-shrink floors); what changed
is the sentence's own arithmetic: it said "62 of them are pinned byte for byte, and the two entries claim C1 re-grounds
are exempt", while the v1.3 code pins 61 files and exempts three (the two claim entries plus the ledger). Leaving the
sentence as it was would make the docstring misstate the code, which is the opposite of the attempt-1 errata's own
rule ("each docstring edit is the sentence made literal, not a new requirement"). If the L1 prefers the sentence
untouched, the revert is the single edit at draft:34-38 and the code is unaffected; this seat did not decide it.

## 5. Limitations

- No tool was installed or upgraded for this seat (no `pacman`, `uv tool install`, `cargo`, `npm -g` transaction was
  run), so there is no tool/version/channel/reason line to record; the checks used the stock `python3` (stdlib only)
  and read-only `git archive`/`git cat-file`/`git log`.
- Nothing was committed, pushed, or mutated in git/jj. This seat wrote exactly two paths: the draft directory
  `.ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/` (two files plus `receipts/`) and this report.
  `git status --porcelain` in the lane also lists other seats' work (`.ufo/waves/round-46/attempt2/build-wave2-spec.py`,
  `.ufo/waves/round-46/attempt2/wave2-spec.json` modified; `attempt2/counter-errata.md`, `attempt2/wave1/`,
  `attempt2/wave2/`, `a2w1.ready.dispatched`, `attempt2/controls/final-measure.sh` untracked) — none of it is mine.
- The four checks were run against the live lane **as it stands now** (28 frontier rows, 65 knowledge entries). After
  the F29 landing the live lane is a different tree, and check (1) will no longer read 7/7 for the reason in F1 —
  that is a property of the attempt-1 counter's frozen limb sentences, not of this amendment.
- The v1.3 files are drafts in a wave draft directory; the committed instrument paths
  (`corpus/instruments/r46-c2-gate.py`, `corpus/instruments/r46-counters-selftest-c2.py`) and the frozen
  `.ufo/waves/round-46/attempt2/claims.json` were read only, never written. Integrating this draft needs the logged
  counter erratum (the attempt-2 errata log already has the `E3` section for it, `.ufo/waves/round-46/attempt2/counter-errata.md`);
  this seat did not write that log — it read it, and aligned the draft's docstring label with it.
- The scratch root `/fast/scratch/hyaku/kasegi-r46/R46bExecGatePinAmend/` was removed after the receipts were copied
  into the draft directory; the pure export `/fast/scratch/hyaku/kasegi-r46/L1/pure2` was read, never edited.
