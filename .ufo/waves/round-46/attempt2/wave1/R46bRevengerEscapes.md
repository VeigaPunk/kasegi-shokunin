VERDICT: HOLDS

# R46bRevengerEscapes — replay of the round-46 counter-falsification campaign against the current tip

Seat: leaf revenger, read-only on the lane. Question: do the three cheapest defect trees from the attempt-1 falsification campaign (reports `wave1/R46RevC1L3.md`, `wave1/R46SentinelGate.md`, `wave1/R46MutC2a.md..c`, all recorded against counter **v1**) still read RED under the counters now committed at the attempt-2 tip (**v1.2**)? A defect tree reading green now would mean the hardening regressed. No tree reads green. No regression found on the replayed surface.

## 0. Counter identity at the current tip

The prior reports ran v1 bytes (`r46-c1-gate.py` sha256 `b0c730c8…`, `r46-c2-gate.py` sha256 `0ee95857…` per `.ufo/waves/round-46/counter-errata.md:2`); the tip carries v1.2 (hardened via errata E1-E12, each row citing the wave-1/wave-2 report that forced it). Verified:

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
ee03806b6b54a2822045e96641a77fa76984b410
$ sha256sum corpus/instruments/r46-c1-gate.py corpus/instruments/r46-c2-gate.py
95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7  corpus/instruments/r46-c1-gate.py
647bd5b7b62685519d8d396bf2d02eca7ad0bb440dd5c4041beabfaa45ea2909  corpus/instruments/r46-c2-gate.py
$ git show 04af9bc9…:corpus/instruments/r46-c1-gate.py | sha256sum
95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7  -      # (c2 likewise 647bd5b7…)
$ git show fe0f56b7…:corpus/instruments/r46-c2-gate.py | sha256sum
647bd5b7b62685519d8d396bf2d02eca7ad0bb440dd5c4041beabfaa45ea2909  -      # (c1 likewise 95f2eb79…)
$ git status --porcelain -- corpus/instruments/r46-c1-gate.py corpus/instruments/r46-c2-gate.py
(clean)
```

Base 04af9bc, freeze fe0f56b and HEAD ee03806 carry byte-identical v1.2 counters. Every counter invocation below ran the lane's committed v1.2 bytes with `TMPDIR` set explicitly to the scratch tmp dir.

## 1. The three cheapest defect trees (each a single edit on the base export)

All trees were built from `git -C <lane> archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus | tar -x -C $S/base` (scratch `/fast/scratch/hyaku/kasegi-r46/R46bRevengerEscapes/`), then one edit per tree. Because attempt-1's landing is committed at 04af9bc, the original seats' hand-built fixtures (F28 row + S073 row + entry) are already present as real lane bytes — each replay is strictly cheaper than the original construction.

| tree | defect (source, verbatim edit) | v1 recorded verdict |
|---|---|---|
| T1 | `wave1/R46RevC1L3.md` Finding 1 ("cheapest tree", 1 line): `corpus/knowledge/claim-gates.md:125` → `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && true  # r46-c1-gate.py --entry corpus/knowledge/claim-gates.md` | `gate L3 pass=1 read=recheck-lines-clean=1` with the defect present (limb survivor; overall was 2/7 RED) |
| T2 | `wave1/R46MutC2a.md` S1 (1 token): F28 entry line 5 `--source S073` → `--source S0730` | full GREEN: `c2-gate fixed=7/7 exit=0` (survivor) |
| T3 | `wave1/R46MutC2c.md` S1 (1 file create): `corpus/knowledge/scratch-notes.txt` = `stray non-md file` | limb survivor: `gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1` |

Selection note: these three are the cheapest of the campaign (one edit each on the committed base) and span both counters and three distinct hardening mechanisms — C1-E1 (L3 exact form) + C1-E6 (allow-list) for T1, C2-E1/E8 (G2 exact recheck) for T2, C2-E5/E12 (G6 directory pin) for T3.

## 2. Finding 1 — T1 still RED; the attacked L3 limb flipped green → red (C1)

Like-for-like run uses the same baseline the original experiment used (round-15 base 914ca0b). First verified the shared export: `diff -rq <(git archive 914ca0b… corpus) /fast/scratch/hyaku/kasegi-r46/L1/pure2/corpus` → `PURE2-IS-914ca0b-CORPUS` (read-only, unedited).

```
$ TMPDIR=$S/tmp python3 <lane>/corpus/instruments/r46-c1-gate.py --root $S/t1 --baseline /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work $S/work-t1b
gate L1 pass=0 read=gated=22 broken=1 lines=65/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=0 read=bad=claim-gates.md
gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2
gate L5 pass=1 read=append-only-restoration-kept=2
gate L6 pass=1 read=mutants=46 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=5/7 exit=1
```

Two v1.2 mechanisms fire where v1 read green: L3 (C1-E1) names the defective entry (`bad=claim-gates.md`; v1 printed `gate L3 pass=1` on the same single edit), and L1 (C1-E6) reports `broken=1` — the `true` segment is outside the allow-list (`r46-c1-gate.py:82-88`), so the line was parsed but never executed (classify marks it broken at `:237-238` before any run). At the attempt-2 baseline the same tree reads RED as well:

```
$ TMPDIR=$S/tmp python3 <lane>/corpus/instruments/r46-c1-gate.py --root $S/t1 --baseline $S/base --work $S/work-t1
gate L1 pass=0 read=gated=22 broken=1 lines=65/base=65
gate L2 pass=0 read=base-gated=22 regrounded=0
...
c1-gate fixed=1/7 exit=1
```

## 3. Finding 2 — T2 flipped full-green → RED on exactly G2 (C2)

```
$ TMPDIR=$S/tmp python3 <lane>/corpus/instruments/r46-c2-gate.py --root $S/t2
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
gate G2 pass=0 read=source=1 verified-at=1 recheck=0 sections=4/4 full=4/4 anchored=1 table-rows=8 xrefs=4/4
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=1 read=spans=27 located=27 failed=0 uncited=0 cores=5/5
gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=6/7 exit=1
```

Pre-v1.2 the identical edit read `c2-gate fixed=7/7 exit=0` (R46MutC2a.md S1: `gate G2 pass=1 …`; `--source S0730` satisfied the substring test). v1.2's G2 requires the exact recheck form (docstring lines 13-15), so the survivor is closed: `recheck=0`, gate red, counter RED.

## 4. Finding 3 — T3 flipped the G6 limb green → RED (C2)

```
$ TMPDIR=$S/tmp python3 <lane>/corpus/instruments/r46-c2-gate.py --root $S/t3
gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 anchored=1 table-rows=8 xrefs=4/4
gate G3 pass=1 read=row-S073=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
gate G5 pass=1 read=spans=27 located=27 failed=0 uncited=0 cores=5/5
gate G6 pass=0 read=knowledge=65 entries=66 nested-md=65 base-intact=0 entry-bytes-ok=1
gate G7 pass=1 read=census-rc=0 ok-line=1
c2-gate fixed=6/7 exit=1
```

Pre-v1.2 G6 passed with the stray non-md file present (`os.listdir` was `.md`-filtered). v1.2 G6 (`r46-c2-gate.py:329-346`) hashes **all** names and requires `len(everything) == 65`: `entries=66 base-intact=0`, gate red, counter RED.

## 5. Controls (discrimination)

- C2 do-nothing on the honest 04af9bc tree (unedited export): `c2-gate fixed=7/7 exit=0` — the counter accepts the honest landed tree, and each single-edit defect above flips exactly its targeted gate to red. Do-nothing green vs defect red is the discrimination; note the honest tree reads green *because* attempt-1's F28 work is committed at 04af9bc (a green control tree is not a defect tree and not a regression).
- C1 do-nothing on the honest 04af9bc tree vs the 914ca0b baseline: `c1-gate fixed=7/7 exit=0` (all seven limbs, `L6 mutants=46 survivors=none`) — v1.2 still accepts the honest re-ground, so T1's limb flips are attributable to the defect, not the baseline.
- C1 literal do-nothing semantics at the attempt-2 base (`--root <04af9bc export> --baseline <same export>`): `gate L2 pass=0 read=base-gated=22 regrounded=0`, `c1-gate fixed=2/7 exit=1` — self-comparison is not the fixed state, by design (R=∅; L3-L6 vacuous). All three C1 readings (2/7 self, 7/7 honest-vs-914ca0b, 5/7 defect) are distinct and explained.

## 6. Answer to the seat question

No rebuilt defect tree reads green at the current tip. The three cheapest v1-era falsifications are closed by v1.2 exactly where the errata say they were closed (C1-E1/E6, C2-E1/E8, C2-E5/E12), and the honest tree still grades green on both counters. The prior hardening has not regressed on this surface.

## Limitations

- Only the three cheapest trees were rebuilt, per the item. SentinelGate's constructions (S1 hostile-exec, S2 absolute-anchor write, S3 timeout orphan, S4-S7) need outside-tree victims, marker files or 185 s runs and were not replayed; the C1-E6 allow-list was exercised here only via T1's non-allow-listed `true` segment (`broken=1`, never executed), not by a hostile payload.
- T1's comparison to the v1 record is limb-level: the original Finding-1 tree lacked the (now committed) re-ground sections, so its L4-L6 were red where mine pass; the attacked limb L3 is the comparable datum (v1 `pass=1` → v1.2 `pass=0 bad=claim-gates.md`), and the overall verdict was RED in both eras.
- The c1 counter resolves instruments to its own lane (`TOOL_LANE`, C1-E6/E7), so L4's per-entry invocations executed the live lane's gate bytes against scratch trees; the lane was not modified by them.
- The 914ca0b-baseline c1 runs left L3-L6 vacuous when run with `--baseline` = the 04af9bc tree itself (R=∅); the limb-level replay required the pre-round baseline (pure2, byte-verified, read-only).
- Exhaustiveness: the five source reports contain ~40 constructions; this replay covers the three cheapest, not the set.
- Tooling: no installs or upgrades (pacman transactions are paused host-wide; none needed). Git usage read-only (`rev-parse`, `status`, `show`, `archive`); no commit, push, index or shared-file write; the fleet repo, sibling lanes, `.ufo/state` and `~/Projects/shokuknow` untouched. Scratch `/fast/scratch/hyaku/kasegi-r46/R46bRevengerEscapes/` (export, four trees, work dirs, tmp) removed after this report was written; the receipts are the quoted outputs above.
