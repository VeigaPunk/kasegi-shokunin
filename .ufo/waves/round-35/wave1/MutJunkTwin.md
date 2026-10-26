# MutJunkTwin — round 35, wave 1 (mutation probes: D5 erratum check + junk-twin admission gate)

Seat: MutJunkTwin (UFO-FSD mutation tester). Scope: challenge the C1 D5 clause check and the
C2 junk-twin rejection with forged fixtures built entirely under
`/fast/scratch/hyaku/kasegi-r35/MutJunkTwin/` (deleted before yield; see §Cleanup). The lane
repo was never written except this receipt; no `git`/`jj` command touched it; no tool was
installed (bash + python3 already present, nothing recorded per the 2026-10-19 tooling rule).

## Report

### Environment and input digests (sha256, measured 2026-10-26T06:49–06:50Z)

```
eee0bb579844ad9d02777fb4cd241e726d0bb0630679bc41aa534d7f5d0951e6  .ufo/waves/round-35/claims-erratum-d5.md
0abec3591e4a2dc5195b23b1c2c920f66052327b7f971aa578af76c3459dc176  .ufo/waves/round-35/c2-controls/junk-f18.md
06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee  corpus/source-snapshots/round-35/manifest.json
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt
0988866608c4a1818219e02bbb23cd1d7aeffb5768a73c411216a4cf821f5e74  corpus/knowledge/cisa-kev-catalog.md
a4f80067183e8512d5e7f39a789c7b51437f357acb05cd77d481a4d9c7cc35ad  corpus/instruments/r35-defect-closure.sh
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  corpus/instruments/frontier-recheck-count.py
```

### Green baselines (pristine bytes, lane root)

`bash corpus/instruments/r35-defect-closure.sh` (working tree, mid-flight — see §Observation):

```
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=0,provenance=1 open=1
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=4/7 exit=1
```

`python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052`
→ five `OK` lines (`Q1..Q5`, each `occurrences=1` with anchors `2/3/4/15472/19165-ok`), `exit=0`.

`python3 corpus/instruments/frontier-recheck-count.py` (06:50:18Z) →
`entries=21 pass=21 exit=0`, including `PASS F18 knowledge/cisa-kev-catalog.md ids=S052 exit=0`.

**Observation (point-in-time, not a verdict):** at probe time the live suite read `closed=4/7`
because D4 (results file not yet git-tracked), D6 and D7 were still open in the working tree —
consistent with sibling seats mid-landing. D5 itself was green at baseline (`present,5,5`,
`open=0`), which is the clause under probe. Not judged; recorded as measured.

---

### Probe 1 — forged `claims-erratum-d5.md` missing one required literal

- **Mutant.** Scratch snapshots of exactly the seven check inputs (SCORECARD.md, SKILL.md,
  `claims-erratum-d5.md`, round-34 `wave1-results.json` + provenance note, round-34
  `L1Integration.md`, `corpus/QUALITY.md`), frozen at probe time so sibling landings cannot
  move them mid-probe. In the mutant snapshots the erratum copy — same relative filename
  `.ufo/waves/round-35/claims-erratum-d5.md` — has one required literal dropped line-wise with
  the suite's own `filter_out` semantics (`grep -v -F`): mutA drops `per-id occurrences`,
  mutB drops `discriminating invocation`. The live file was never modified.
- **Expected detector.** `bash corpus/instruments/r35-defect-closure.sh --root <tree>` — the
  suite's `check_d5` (probe-time bytes `a4f80067…`; D5 block at `:188-199` there, `:218-228`
  in the current tree — semantics unchanged) must read
  `open=1` on each mutant with the payload naming the dropped clause, and `open=0` on pristine
  and restored bytes (red-before for the check).
- **Output.**

```
P1-baseline pristine snapshot : D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0 | closed=4/7 exit=1
P1-mutA  minus per-id-occurrences: D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=0 open=1 | closed=3/7 exit=1
P1-mutB  minus discriminating-invocation: D5 check=erratum-file=present,discriminating-invocation=0,per-id-occurrences=5 open=1 | closed=3/7 exit=1
P1-restored mutA              : D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0 | closed=4/7 exit=1
```

  (`closed=4/7` baseline and `3/7` mutants differ only by D5; D4 reads constant `tracked=0`
  in the snapshot by construction — no git repo in scratch — and D6/D7 carry the frozen
  mid-flight bytes, identical in all four runs, so the delta is attributable to D5 alone.)
- **Verdict.** KILLED. The check is red-before for both clauses independently; each omission
  flips exactly its own payload field and the summary `closed` count.
- **Restoration evidence.** mutA's erratum re-copied from live bytes:
  `restored==live: True (sha256 eee0bb579844ad9d02777fb4cd241e726d0bb0630679bc41aa534d7f5d0951e6)`;
  live file hashed before and after the whole probe: identical
  (`eee0bb57…` → `eee0bb57…`, `unchanged=True`). The lane erratum was never opened for write.

---

### Probe 2 — junk-twin F18 candidate whose only quote is REAL (present in S052.txt)

- **Mutant.** Two forged twins (shape copied from `.ufo/waves/round-35/c2-controls/junk-f18.md`:
  fixture banner, `source: S052 — <feed URL>`, `verified-at: 2026-10-26`, the entry-identical
  relative `recheck:` line, one quoted sentence) built in scratch:
  `junk-f18-real-prose.md` (sha256 `6b2be9bdb115fcab1c8435055ab1cf1262175a03a4dcb6769bbe904621a052f2`)
  quotes the real capture sentence `"Arista VeloCloud Orchestrator SQL Injection Vulnerability"`
  (normalized occurrences in the committed capture = **1**, first at L11; not one of manifest
  Q1–Q5) and cites S052 in prose; `junk-f18-real-bare.md` (sha256
  `e92813d38184848d2e0a74e4ce376aaef83483fda14c33c96f196db05596a04c`) is identical minus the
  prose citation.
- **Expected detector.** Per the claimed invariant: the twin is not the drafted entry, so it
  must not be admitted, and `source-recheck` on a twin not listed in the manifest must exit != 0.
- **Output.** From the lane root unless stated (`<S>` = scratch root):

```
P2a  source-recheck --manifest corpus/source-snapshots/round-35/manifest.json --source junk-f18-real
     -> junk-f18-real:source UNAVAILABLE reason=not-listed            [exit=2]
P2b  source-recheck --manifest <S>/junk-f18-real-prose.md --source S052
     -> manifest UNAVAILABLE reason=unreadable-or-invalid             [exit=2]
P2c  control, --manifest /dev/null  -> manifest UNAVAILABLE reason=unreadable-or-invalid [exit=2]
P2d  scratch manifest with twin appended as a second S052 record
     -> manifest UNAVAILABLE reason=duplicate-source-id               [exit=2]
P2e  scratch manifest registering the twin under a new id S053
     -> S053:manifest MISMATCH reason=stem-mismatch                   [exit=1]
P2f  CONTROL: scratch manifest pinning the real sentence inside the S052 record
     (path S052.txt, sha256 d69349e8…)
     -> S052:sha256 OK / S052:J1 OK occurrences=1                     [exit=0]
P2g  harness with a forged F18 Frontier row naming the prose-cited twin (scratch root)
     -> PASS F18 knowledge/junk-f18-real.md ids=S052 exit=0 ; entries=1 pass=1 exit=0
P2h  same with the bare twin (no prose citation)
     -> FAIL problems=selection-not-cited-by-entry ; entries=1 pass=0 exit=1
```

- **Verdict.** KILLED on the committed tree — no executable route admits the twin: it is not
  the drafted entry (`corpus/knowledge/cisa-kev-catalog.md` holds the F18 row and prose; the
  live harness counts it, `PASS F18 … ids=S052`), it is `not-listed` in the manifest (exit 2),
  cannot be registered (duplicate id → exit 2; new id → B1 `stem-mismatch` → exit 1, so the
  manifest namespace is 1:1 with capture stems), and pointing `--manifest` at the twin file is
  non-discriminating (P2b ≡ P2c, exit 2 for any non-JSON — the erratum's §2 reading, re-measured
  for round 35).
- **Coverage findings (attributability, not contract changes).**
  1. The quote comparator is twin-blind: the twin's REAL sentence passes it outright (P2f
     `occurrences=1`, exit 0). For a real-sentence twin, `reason=quote-not-found` can never
     fire; rejection rides entirely on the admission binding (no Frontier row, no manifest
     route), not on quote absence. This is `.ufo/waves/round-35/claims-erratum-d5.md` §6's
     mixed-control warning, now measured for round 35: future twins must carry only absent
     sentences or the control loses its discriminating reason.
  2. The harness binding itself cannot reject a twin once a Frontier row names it: P2g admits
     the prose-cited real-sentence twin (`pass=1`). Only the bare shape trips a binding limb
     (P2h `selection-not-cited-by-entry`; the committed `junk-f18.md` is bare, so it would be
     caught there too). The committed rejection therefore rests on the Frontier admission
     process — "not the drafted entry", no row, non-author reviewer REFUSE — exactly as
     erratum §3 states; the instruments verify the manifest half, the row/admission half is
     process, not code.
- **Restoration evidence.** Everything ran on scratch copies or read-only live paths; nothing
  outside this receipt was written into the lane. Cleanup-time re-hash:
  **unchanged by this seat** — `claims-erratum-d5.md` (`eee0bb57…`), `manifest.json`
  (`06bfcc71…`), `S052.txt` (`d69349e8…`), `c2-controls/junk-f18.md` (`0abec359…`),
  `source-recheck.py` (`fd2e01e8…`), `frontier-recheck-count.py` (`1be79af6…`). **Moved during
  the wave by sibling seats, not by this probe** — `corpus/README.md` and
  `corpus/knowledge/cisa-kev-catalog.md` re-hashed differently at cleanup (concurrent
  landings; my runs against them were read-only, and the probe-2/3 detectors used frozen
  copies), and `r35-defect-closure.sh` moved `a4f80067…` → `0ae4b484…` between my baseline
  runs and cleanup (Probe 1 ran at `a4f80067…`; its `check_d5` clause semantics are identical
  in the current bytes — same three payload fields, same literals, now at `:218-228`).

---

### Probe 3 — junk twin with an absent/fabricated sentence

- **Mutant.** `junk-f35-fake.md` (sha256
  `b3b913a52bea0eddcc37f5f8d69e8452256058607b08fed18066595786878ecc`), same shape, only quote
  `"Every catalog entry carries a CVSS v4 base score that CISA recomputes weekly from exploit
  intelligence."` — normalized occurrences in the committed capture = **0** (and raw
  substring count 0).
- **Expected detector.** The erratum §3 discriminating invocation: a scratch manifest pinning
  that sentence inside the S052 record (path `S052.txt`, capture sha256) must print
  `MISMATCH reason=quote-not-found` and exit != 0, against the P2f real-sentence control at exit 0.
- **Output.**

```
P3a  source-recheck --manifest <committed manifest> --source junk-f35-fake
     -> junk-f35-fake:source UNAVAILABLE reason=not-listed            [exit=2]
P3b  scratch manifest pinning the fabricated sentence vs the committed capture
     -> S052:sha256 OK / S052:J1 MISMATCH reason=quote-not-found      [exit=1]
```

- **Verdict.** KILLED. The fabricated twin is rejected on both named routes: not listed
  (exit 2) and, via the discriminating invocation, `quote-not-found` (exit 1) while the
  identical invocation on the real sentence exits 0 — the pair is the discriminating
  comparison the frozen kill rule keys on.
- **Restoration evidence.** Scratch-only; no lane bytes changed by this seat (evidence in
  §Restoration evidence, cleanup re-check below).

---

### Files forged (all deleted with the scratch tree)

`junk-f18-real-prose.md`, `junk-f18-real-bare.md`, `junk-f35-fake.md`, scratch manifests
`dup.json`, `wrongstem.json`, `realquote.json`, `fakequote.json`, harness roots `rootA`/`rootB`
(forged F18 rows), and the seven-input probe-1 snapshots `lane/pristine|mutA|mutB`. Full
command transcripts: `probe1.txt`, `probe23.txt` under the scratch `out/` (quoted above in full).

### Cleanup

Scratch `/fast/scratch/hyaku/kasegi-r35/MutJunkTwin/` removed before yield; removal verified
(`test -d` → exit 1). No defect: no seat tree left on disk.
