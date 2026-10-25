# Round 29 wave-1 — R14 evidence economy

Axes: depth:verifiability (auditability), coverage (complete retained evidence). R14 requires receipts/digests in git, bulky fixture trees represented by content-addressed archives or reproducible `git archive` + named mutation scripts, and measurable committed-byte growth.

## Measurement

At the claims freeze `f28ff5d26b29270f93163117e7255e24f0b1d947`, `.ufo/waves/round-29/` contained **4 tracked files / 10,130 bytes** (`git ls-tree -r -l f28ff5d -- .ufo/waves/round-29/`). At dispatch HEAD `46e07f6`, it contained **7 tracked files / 213,718 bytes**: delta **+203,588 committed bytes** across the three additions `build-spec.py`, `wave1-dispatch.json`, and `wave1-spec.json` (2,078 lines). These are wave plan/dispatch evidence, not copied corpus data.

The working tree at measurement was **1.2 MiB / 112 files** under `.ufo/waves/round-29/`; this includes uncommitted seat receipts and temporary controls and is not a claim about committed growth. Largest subtrees: wave1 992 KiB, assimilation 244 KiB (fetch 208 KiB), receipts 216 KiB, `CritC2Kill-scratch` 120 KiB, `scoutcap-scratch` 68 KiB, and the `ExecCensusDry` scratch mirror 508 KiB before consolidation. Largest individual files in the remaining wave tree: `wave1/assimilation/fetch/S048-sibling.html` 94,208 B, `wave1-dispatch.json` 89,331 B, `wave1-spec.json` 63,435 B, `build-spec.py` 50,822 B, then `ExecCensusDry.mutations/SOURCES.md` 36,075 B. No other remaining single control/fixture tree exceeds the few-hundred-KiB threshold; the assimilation fetches are captured source evidence, not a duplicated corpus.

Round-29 production source captures are **1.2 MiB** under `corpus/source-snapshots/round-29/` (S043 1,220,741 B, S044 8,187 B, S045 14,575 B, manifest 3,806 B). These are the pinned source inputs explicitly required by frozen C2, not a scratch corpus copy; preserved.

## Consolidation performed

`wave1/ExecCensusDry/` was a 508 KiB, 42-file mirror of `corpus/SOURCES.md` plus every `corpus/knowledge/` file to test a proposed S043/S044/S045 append and F13 entry. The seat confirmed its census gate was complete and the tree was no longer needed; its report `ExecCensusDry.md` remains intact. I removed only that scratch mirror, after notifying/receiving confirmation from `ExecCensusDry-2`.

Preserved reconstructability without preserving the 508 KiB copy:

- `ExecCensusDry.mutations/SOURCES.md` and `ExecCensusDry.mutations/program-severity-ladders-and-reward-scales.md` are the two exact mutated files, verified byte-identical to their counterparts in the scratch mirror.
- `ExecCensusDry.digests.txt` records SHA-256 for all 42 paths. Aggregate digest of the sorted per-file hashes: `ad8e5a1e669d984844a207bdf80d21bd9e591b566ae47a4b37d6d95f827501ed`.
- `exec-census-dry.regenerate.sh` archives the base corpus subset from lane revision `46e07f6`, overlays the named mutation assets, and checks each digest. End-to-end regeneration produced 42 files byte-identical to the original mirror. A deliberately changed digest failed with exit 1 and named the mismatching path. No tool was installed or updated.

The removed scratch tree's bytes have not been substituted by a scratch copy elsewhere. The 42-file digest list plus two mutation assets retain content identity and allow reconstruction. Existing smaller control fixtures, receipts, source captures, and other seats' artifacts were preserved.

## Contract and tradeoff

Preserved: the census seat's proposed post-append state and its evidence remain inspectable/reconstructable; the seat's original decision receipt and frozen claims are untouched. Tradeoff: direct browsing of a ready-to-open corpus mirror is replaced by a regeneration step; this costs one local extraction but removes redundant corpus bytes while retaining exact hashes. No historical provenance was deleted.

Evidence commands/results: `du -sh .ufo/waves/round-29/` → 1.2M; `find .ufo/waves/round-29/ -type f | wc -l` → 112; `git ls-tree -r -l f28ff5d` / `46e07f6` measurements above; regeneration command and digest tamper test recorded above. These are observed current working-tree and committed revision values, not a prediction of final round commit growth.
