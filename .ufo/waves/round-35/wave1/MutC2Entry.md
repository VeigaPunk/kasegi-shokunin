# MutC2Entry — round-35 wave-1 receipt (mutation test: F18 entry + harness binding)

Seat: MutC2Entry (mutation-tester, leaf). Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin.
Assignment: mutation-test the F18 entry + harness binding — four mutants, each must fail
source-recheck or the harness (exit != 0); the pristine entry must pass.

## Report

### Invariant under test and binding chain

- Claimed invariant (wave item, build-spec.py L538-542): mutants (1) drop the `source: S052`
  header line, (2) change a quote's wording (paraphrase), (3) point the anchor at the wrong line,
  (4) add an unregistered `--source` to the recheck line — each must fail source-recheck or the
  harness (exit != 0). Pristine must pass.
- Binding chain: entry `corpus/knowledge/cisa-kev-catalog.md` header `source: S052 — …` (L3) →
  `recheck:` line (L6) → manifest `corpus/source-snapshots/round-35/manifest.json` (record S052,
  sha256 pin `d69349e8…`) → capture `corpus/source-snapshots/round-35/S052.txt`.
- Detectors (the bounded behavioral detector, run on pristine, mutated and restored bytes):
  - `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052`
  - `python3 corpus/instruments/frontier-recheck-count.py --root <tree>`
  - plus, from the third revision on, the entry's own evidence-layer check FC-13 (anchor
    verification), measured to test the scribe's mitigation claim against my M3 finding.

### Byte-state provenance (the pristine target moved three times during this seat's run)

1. `f874c49b…` (87 lines) — first copy, an intermediate revision caught before the scribe's
   finalization notice.
2. `da81204b3fbca378aa311406fd3a46394759967ecc3445297335a7526c573acf` (88 lines, 13,308 B) —
   first final bytes per ScribeEntryF18's message; full probe run.
3. `0988866608c4a1818219e02bbb23cd1d7aeffb5768a73c411216a4cf821f5e74` (117 lines, 16,995 B) —
   steered bytes after an L1 steer (adds Claim 4b live-page quotes + FC-12); full probe re-run;
   every shared-point verdict matched the state-2 run.
4. `e3f233c0d5e5a1c5a876aa396b1c42e8265f5e3a4cd076837deac50af6de2730` (118 lines, 17,643 B) —
   current bytes; the only delta is **FC-13** (anchor verification), the scribe's response to this
   seat's M3 finding. **All verdicts below are on these bytes**; the mutation points (L3 header,
   L6 recheck, L14/L16/L22/L24 pinned quotes, L50 4b quote, manifest Q1-Q5) are byte-identical
   across states 2-4, and every re-measured verdict matched the earlier runs.

### Fixture (isolated scratch; live lane never written)

- Scratch root `/fast/scratch/hyaku/kasegi-r35/MutC2Entry/`: `pristine/` plus `mut1 mut2a mut2b
  mut3 mut4 mut2c`, each a `cp -a` of pristine. All detector runs executed inside scratch copies.
- **Adaptation A (documented, applied identically to every copy).** Every knowledge entry's
  `recheck:` line carries an absolute `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin` (46 of 47
  knowledge files carry that string). In each scratch copy that cd was rewritten to the copy's own
  root — otherwise the recheck line would read the LIVE lane's manifest and the manifest-side
  mutants (M2a/M3) would be invisible to the detector. The live lane bytes were never modified.
- **Adaptation B (retired).** In the state-2 run the live README still had 17 frontier rows, so the
  scratch README carried a stand-in F18 row. From the state-3 re-run on, the live F18 frontier row
  had landed (`corpus/README.md` L388, 18 frontier rows, sha256 `277f04ce…`), so the fresh corpus
  copy ships it and no stand-in is needed — the harness binds F18 natively.
- Scratch pristine digests (state 4): entry (cd-rewritten)
  `7ac99597e07b840d51faaa5c88e8ca4a5a571b52c92b7361ece2678a8ac5d1f1`; manifest
  `06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee` (byte-identical to the live
  manifest); capture `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826` (= the
  manifest's pin).

### Pristine baseline — PASS (required)

```
$ cd <scratch>/pristine && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
S052:sha256 OK
S052:Q1 OK occurrences=1 anchor=2-ok
S052:Q2 OK occurrences=1 anchor=3-ok
S052:Q3 OK normalized=markup-whitespace occurrences=1 anchor=4-ok
S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=15472-ok
S052:Q5 OK normalized=markup-whitespace occurrences=1 anchor=19165-ok
source-recheck exit=0

$ python3 corpus/instruments/frontier-recheck-count.py --root <scratch>/pristine
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
entries=21 pass=21 exit=0
harness exit=0

$ FC-13 (entry L100, run from the tree root)
anchors_ok 5 of 5   (exit 0)
```

(The other 20 admitted rows each printed `PASS … exit=0`; full output reproducible with the command.)
Matches the C2 after-state: entries=21 pass=21 exit=0 incl. `PASS F18 ids=S052`; source-recheck
every assertion `occurrences=1`, `sha256 OK`, exit 0; FC-13 `anchors_ok 5 of 5`.

### Mutants (each applied to its own copy; digests after mutation)

**M1 — drop the `source: S052` header line** (entry L3 deleted; entry 118 → 117 lines; mutated
entry digest `70fc83359ce1e59305bfb71ba84afa814fb4fca58101c5283c45b985f881a383`)

```
source-recheck: (six OK lines as pristine) exit=0        # reads only the manifest; cannot see the entry
FAIL     F18  knowledge/cisa-kev-catalog.md   ids=-   exit=-   problems=no-source-line
entries=21 pass=20 exit=1
harness exit=1          |  FC-13: anchors_ok 5 of 5 (reads the manifest; unaffected)
```

KILLED by the harness. Note: the kill rests on the single `no-source-line` limb — with
`declared=[]` the two directional rule-A limbs are skipped (their guards require a non-empty
declared set), and this entry declares S052 nowhere else (0 `- S052` evidence bullets; verified
`grep -cE '^[[:space:]]*[-*] S052'` → 0). The harness docstring names the shape where a dropped
header would NOT fire rule A (an entry that also declares the id via an evidence bullet) — F18 is
not that shape, so the kill holds for these bytes.

**M2a — manifest Q1 quote paraphrased** (manifest L14: `"CISA Catalog of Known Exploited
Vulnerabilities"` → `"CISA List of Known Exploited Vulnerabilities"` inside the `quote` field only;
mutated manifest digest `6e93d9a817354f78381b55fbadecd0783b90da974f2e94e63a49ab156151b2dd`)

```
S052:Q1 MISMATCH reason=quote-not-found
S052:Q2 OK occurrences=1 anchor=3-ok
S052:Q3 OK normalized=markup-whitespace occurrences=1 anchor=4-ok
S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=15472-ok
S052:Q5 OK normalized=markup-whitespace occurrences=1 anchor=19165-ok
source-recheck exit=1
FAIL     F18  knowledge/cisa-kev-catalog.md   ids=S052   exit=1   problems=recheck-exit-1
entries=21 pass=20 exit=1
harness exit=1          |  FC-13: anchors_ok 4 of 5 (the paraphrased quote no longer sits in Q1's anchor window — redundant catch)
```

KILLED by both detectors (and by FC-13).

**M2b — supplementary probe: the same paraphrase applied at the entry's rendered quote**
(entry L14 blockquote `> "title": "CISA Catalog of …" — L2` → `"CISA List of …"`;
manifest and capture pristine; mutated entry digest
`34012d3a29163434323b90b3745522848350b02b7a0ebdbcd5a47eda2e08fb42`)

```
source-recheck: (six OK lines as pristine) exit=0
PASS     F18  knowledge/cisa-kev-catalog.md   ids=S052   exit=0
entries=21 pass=21 exit=0
harness exit=0          |  FC-13: anchors_ok 5 of 5 (reads the manifest, not the entry render)
```

**SURVIVED at every automated layer** — coverage finding (see Findings).

**M3 — point the anchor at the wrong line** (manifest L33: Q4 `anchor` 15472 → 19165, i.e. pointed
at Q5's asserted location; mutated manifest digest
`3852616279771b8836b6ecc79738a499b2dd40b16b9cfe7c1e1ce9efe65b2441`)

```
S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=19165-BROKEN
source-recheck exit=0
PASS     F18  knowledge/cisa-kev-catalog.md   ids=S052   exit=0
entries=21 pass=21 exit=0
harness exit=0          |  FC-13: anchors_ok 4 of 5  ← caught at the entry's evidence layer
```

**SURVIVED per the assigned exit-code detectors** (source-recheck prints the broken-anchor note
but exits 0; the harness reads only the exit code) — **but now caught by the entry's own FC-13**
(`anchors_ok 4 of 5`), which the scribe added in response to this seat's state-2/3 M3 finding and
which I verified empirically on the mutated manifest. The instrument-level gap remains (see
Findings): neither instrument's exit code moves on a wrong anchor for an exactly-once quote.

**M4 — add an unregistered `--source` to the recheck line** (entry L6: `--source S052` →
`--source S052 --source S051`; S051 is registered in SOURCES.md but declared by neither the F18
entry nor the round-35 manifest; mutated entry digest
`7b1621e61e42a3c40cdac68c08aba9d6abbcaa6882e2393312ac69c2084c1a73`)

```
source-recheck: (six OK lines as pristine) exit=0        # the line never runs — the harness refuses it first
FAIL     F18  knowledge/cisa-kev-catalog.md   ids=S052   exit=-   problems=selection-not-declared-by-entry,selection-not-cited-by-entry,manifest-missing-ids
entries=21 pass=20 exit=1
harness exit=1          |  FC-13: anchors_ok 5 of 5 (unaffected)
```

KILLED by the harness (three limbs fire; the recheck line is never executed).

**M2c — supplementary probe on the steered bytes' new surface: a Claim 4b live-page quote
paraphrased** (entry L50: `"A Binding Operational Directive is a compulsory direction to federal,
executive branch, departments, and agencies"` → `"… a mandatory direction to …"`, attribution
`— page introduction, extraction L92` kept; manifest and capture pristine; mutated entry digest
`98c9b47861980a656d00dcdc959b19d162330d266a6b16a59519b0a1c9cb47eb`)

```
source-recheck: (six OK lines as pristine) exit=0
PASS     F18  knowledge/cisa-kev-catalog.md   ids=S052   exit=0
entries=21 pass=21 exit=0
harness exit=0          |  FC-13: anchors_ok 5 of 5 (4b quotes are not manifest assertions)
```

**SURVIVED at every automated layer** — disclosed-gap measurement, NOT counted against the pinned
tier: the entry itself discloses (Claim 4b provenance paragraph and `## Scope and limits`) that the
BOD 26-04 page is "not in the S052 capture and is not a registered source row, so these quotes are
a dated live-page claim, not a pinned-source claim", and ScribeEntryF18 flagged the same gap to
this seat. FC-12 re-checks the live page's own counts (`revoked 1 compulsory 1 three_days 1
evolves 1`), not the entry's quote fidelity, so a paraphrase there is caught only by manual
reading. Measured here so the gap is empirical, not assumed.

### Verdict summary

| mutant | mutation point | source-recheck | harness | FC-13 (entry layer) | verdict |
|---|---|---|---|---|---|
| M1 | entry L3 `source: S052` line dropped | exit 0 (entry invisible to it) | exit 1 `no-source-line` | 5 of 5 | killed |
| M2a | manifest Q1 quote paraphrased | exit 1 `quote-not-found` | exit 1 `recheck-exit-1` | 4 of 5 | killed |
| M2b* | entry L14 rendered pinned quote paraphrased | exit 0 | exit 0 | 5 of 5 | **SURVIVED** |
| M3 | manifest Q4 anchor → wrong line (19165) | exit 0 (`anchor=19165-BROKEN` note) | exit 0 | **4 of 5** | **SURVIVED per instruments**; caught at the entry's FC-13 layer |
| M4 | recheck line + `--source S051` | exit 0 (line not run) | exit 1 (3 problems) | 5 of 5 | killed |
| M2c* | entry L50 unpinned 4b quote paraphrased | exit 0 | exit 0 | 5 of 5 | **SURVIVED** (disclosed gap) |

\* supplementary probes at additional wording sites of assigned mutant 2 (the quote's wording
exists in the manifest assertion, the entry's pinned render, and — after the steer — the entry's
unpinned Claim 4b render; all three sites probed).

The assigned invariant ("each must fail source-recheck or the harness, exit != 0") holds for M1,
M2a and M4. It does NOT hold for M3 (per the two instruments; mitigated at the entry's FC-13
evidence layer, which is a manual check, not an instrument exit) nor for the entry-side variants
of M2 (M2b pinned render, M2c unpinned render). Surviving mutants = coverage findings for the L1
to weigh; per my role I changed no contract and no lane file.

### Findings (surviving mutants)

1. **M3 — the instruments' anchor pin is not enforced for exactly-once quotes; the entry's FC-13
   now covers the gap at the evidence layer.** In `corpus/instruments/source-recheck.py`,
   `check_source` makes a broken anchor fatal only when `occurrences > 1`
   (`if occurrences > 1 and anchor_verdict_result != "ok"`); for a unique quote a wrong anchor
   degrades to the printed note `anchor=N-BROKEN` on an `OK` line, exit 0. All five S052
   assertions are `occurrences=1` (pristine output above), so the round-35 manifest exercises no
   non-unique quote and the anchor limb is unexercised by S052 — contrast the round-34 S051
   manifest, which carried two `occurrences=2` quotes whose anchors are load-bearing
   (`corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`, "Scope and limits"). The C2
   kill rule ("source-recheck S052 exit != 0") therefore still does not catch a wrong-anchor
   mutant on this manifest. Mitigation landed this round at the entry layer: FC-13 (entry L100)
   verifies every manifest anchor against the capture and prints `anchors_ok K of 5` — measured
   `5 of 5` pristine, `4 of 5` on the M3 manifest (and on the M2a manifest). FC-13 is a manual
   entry check, not an instrument wired to an exit code, so the instrument-form gap stands for the
   instrument owner/L1 to weigh (ScribeEntryF18 reports it as a lane-instrument gap as well).
2. **M2b — entry↔manifest quote fidelity is unguarded by any automated layer (pinned tier).**
   Paraphrasing the entry's rendered quote (manifest and capture pristine) passes both instruments
   and FC-13: source-recheck verifies manifest↔capture only; the harness binds
   ids/manifest/exit-code, not quote text (its docstring states the scope: "a passing entry proves
   its pinned captures still hold its own assertions, not … that the quotes assert what the entry
   says they assert"); FC-13 reads the manifest, not the entry render. The guard that exists is
   the human reviewer procedure (RevEntryF18: re-open the capture and verify every quoted string
   exactly-once at its cited line with `grep -c`), not an automated gate.
3. **M2c — the Claim 4b live-page quotes sit outside every automated layer (disclosed).** The
   entry's own Scope section and the scribe's note disclose this; measured empirically here. A
   registry row + capture + manifest record for the BOD 26-04 page would close it; until then the
   provenance difference is labelled in the entry ("weaker than Claims 1–6").

### Restoration evidence

- The live lane was never written by this seat. The three files the mutants actually touch are
  byte-identical before and after the whole probe (hashed at probe start, after each re-sync, and
  at cleanup):
  entry `e3f233c0d5e5a1c5a876aa396b1c42e8265f5e3a4cd076837deac50af6de2730`,
  manifest `06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee`,
  capture `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`.
- `corpus/README.md` moved once during the seat's run, `876be9cc…` (368 lines, 17 frontier rows) →
  `277f04cedfb06f493ae5da636d665b490ac0e78b26ea282b0d0ef3a469d3ffa2` (396 lines, 18 frontier rows):
  a concurrent sibling append landed the live F18 frontier row
  (`## Round-35 admission — coverage map row and Frontier F18 (appended 2026-10-26)`, row at L388).
  Not a MutC2Entry write; stable from the state-3 re-probe on; no detector run wrote to it.
- The scratch pristine copy was never mutated; final re-runs on it after all mutants:
  source-recheck exit 0 (Q5 `anchor=19165-ok`), harness `entries=21 pass=21 exit=0`, FC-13
  `anchors_ok 5 of 5`.
- Mutant copies are disposable scratch and were deleted before yield.

### Tooling

- No tools installed or upgraded (python3 stdlib only was needed; pacman is paused host-wide and
  nothing was required).

### Scratch cleanup

- `/fast/scratch/hyaku/kasegi-r35/MutC2Entry` deleted before yield (verified absent at yield time).
