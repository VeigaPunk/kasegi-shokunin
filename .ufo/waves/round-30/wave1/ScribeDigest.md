# Round 30 wave 1 — instrument digest and evidence report

**Axes:** depth:verifiability (C1; frozen score 4) and coverage (C2; frozen score 7). This report records locally observed bytes and commands; it does not alter frozen claims or determine their canonical judgment.

## Behavior and gates

C1 targets the frontier recheck harness's named fail-closed missing-entry result (A1), rejection of duplicate entry realpaths (A2), source/capture stem identity (B1), and rejection of repeated quotes lacking a verified anchor (B2). The landed harness handles A1 and A2 as specified. The source checker enforces B1 and repeated-occurrence anchoring. The committed B2 fixture is not an isolating counterexample: it uses id `S045` with path `B2.txt`, so B1 fires first. Therefore its exit 1 is not evidence that the occurrence limb ran; the mutant report confirms the B2 mutant does not flip on this frozen fixture. Separate clean B2 fixtures/selftests do exercise the occurrence limb, but that does not make the frozen counter isolating. This distinction is material to the C1 kill rule.

C2's F14 knowledge entry, S046/S047 registry rows, and round-30 manifest eventually landed. Final local reruns measured 14 admitted frontier rows; one file cites S046/S047; 2 S046/S047 registry rows and 47 total registry rows; sources census exit 0; harness 17/17 exit 0; rechecks for S046, S047, S041 all exit 0. S047's repeated quotes are anchored and verified (Q1 3 occurrences, anchor 123; Q3 2, anchor 130). The report's `ExecHarnessAfter.md` records the all-present run and digests. Current final artifact SHA-256s are listed below.

## Digest ledger

| Stage | `frontier-recheck-count.py` SHA-256 | `source-recheck.py` SHA-256 | Evidence / qualification |
|---|---|---|---|
| Freeze — claims commit `3c5573541300ba0fd3d89372dda3d841172eaa3f` | `c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261` | `9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96` | Independently obtained with read-only `git show <commit>:<path> | sha256sum`; equals C1 before receipt. Frozen bytes both reproduced as control copies. |
| Implementation, first observed changed bytes, 2026-10-25 18:50:40Z | `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` | `0b841d5ddb80f96f0e802eec1e67a0b9ba0606609282d8991759db72ac71a243` | `c1-controls/mutants/digest-poll.log`; frontier implementation had changed. |
| Implementation, later poll, 2026-10-25 18:51:26Z | `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` | `2c893aa86b028494fee7934e875c61298f3e4d316e454b4d01b4793c6e267cdc` | Direct `sha256sum` on current working-tree instruments. Source checker had changed again. |
| Settled implementation / final landed working-tree bytes (18:52–18:55Z evidence) | `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` | `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f` | Matches `ExecMutantsC1.md`, `ExecHarnessAfter.md`; current final `sha256sum` rechecked these exact digests. No later changes observed. |

**Drift finding (M29-6 class):** the source instrument changed across measured implementation polls (`0b841d5d…` → `2c893aa8…` → settled `33602a9d…`) while the frontier digest remained stable after its first change. The settled digest is the one cited by the final harness-after receipt and the mutation evidence. The intermediate source digest `2c893aa8…` is not the receipt's final subject digest; do not treat it as landed/final. `ExecMutantsC1.md` explicitly records the intermediate `0b841d5d…` then settled digest. No evidence found that `ExecHarnessAfter.md`'s settled digests mismatch its cited files.

## Commands exercised and observed outcomes

1. Freeze blobs: `git show 3c5573541300ba0fd3d89372dda3d841172eaa3f:corpus/instruments/frontier-recheck-count.py | sha256sum` and equivalent `source-recheck.py`; observed freeze digests above. Read-only only.
2. Final C1 controls, each run from lane root:
   - `python3 corpus/instruments/frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a1` → exit 1; stdout `FAIL F98 ... problems=missing-entry`, `entries=1 pass=0 exit=1`; stderr empty.
   - same `--root .../harness-root-a2` → exit 1; stdout names `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md`, `entries=2 pass=2 exit=1`; stderr empty.
   - `python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-30/c1-controls/q9/manifest-b1.json --source S043` → exit 1, `reason=stem-mismatch`.
   - same manifest-b2.json `--source S045` → exit 1, **also `reason=stem-mismatch`**, not occurrence-not-unique. See B2 isolation finding above.
3. Final full harness: `python3 corpus/instruments/frontier-recheck-count.py` → `entries=17 pass=17 exit=0`, F14 PASS with ids S041/S046/S047.
4. Round-30 source rechecks, separately: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-30/manifest.json --source S046` → exit 0; S047 → exit 0; S041 → exit 0. S047 repeated quotes reported with verified anchors.
5. `python3 corpus/instruments/source-recheck.py --selftest` → 9 cases, 0 failures, exit 0; includes stem mismatch, repeated quote missing anchor, valid anchor, out-of-range and broken anchor.
6. Base-pass preservation: ran each registered source id in manifests rounds 23–29 against its corresponding manifest through `source-recheck.py --source <id>`; all 34 invocations returned exit 0. The per-id set was S018/S029/S030/S031; S001–S015, S032–S035; S036–S040; S041; S041/S042; S043/S044/S045. (S041 appears in more than one manifest.)
7. Final C2 counters: `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` → 14; `grep -lE '^source: S04[6-7] ' corpus/knowledge/*.md | wc -l` → 1; `grep -cE '^\\|[[:space:]]*S04[6-7][[:space:]]*\\|' corpus/SOURCES.md` → 2; total-row equivalent with `S[0-9]{3,}` → 47; `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0 (W04 duplicate-URL warnings S028/S029, then `kasegi ok`).

## Findings and limits

- **C1 A1/A2/B1 behavior:** observed on settled bytes and freeze controls. Mutation report says A1, A2, B1 mutants flip as expected. **C1 B2 kill-rule discrimination is not met by its frozen fixture:** the B2 mutant does not flip on that fixture because B1 masks it. The supplementary same-stem fixture and selftest establish B2 behavior, but do not repair frozen counter discrimination. The frozen kill rule only asks B2 output to have a failure reason, which the unrelated stem mismatch satisfies; report this limitation to canonical judge rather than upgrading the B2 counter claim.
- **C1 real corpus/no-regression:** final full harness and 34 prior registered source-rechecks passed; round-30 source rechecks pass. These are observed working-tree runs. No claim of an integration-commit hash or post-commit byte binding is made here.
- **C2:** final measured values satisfy the listed numeric/exit predicates at the inspected working-tree state. No live bounty target was contacted; all verification was local to captured documentation and fixtures.
- At an earlier snapshot, `ExecPostCommitRecheck.md` correctly recorded pending F14/manifest failures. Those are stale in-progress measurements, not final-state behavior: `ExecHarnessAfter.md` records polls until all prerequisites appeared and a successful final rerun. The current recheck run independently confirmed that later state.
- No package files under `/home/vgpnk/Projects/shokuknow` were written. Tool install/upgrade: none. No build/lint/test suite was run; only assigned instrument/counter checks and selftest were exercised.

## Touched surfaces and provenance

This scribe wrote only `.ufo/waves/round-30/wave1/ScribeDigest.md`. Product/corpus changes were made by other seats; evidence is sourced from frozen claims and before receipts, `ScoutDatawalk.md`, `ExecImplFrontierHarness.md`, `ExecImplSourceRecheck.md` and its diff, `ExecMutantsC1.md`, `ExecHarnessAfter.md`, `ExecCensusAfter.md`, `ExecRegistryAppend.md`, `ExecReadmeF14.md`, `RevClaimsOverall.md`, `CritC1Kill.md`, and direct local command outputs listed above. Read-only package source observed at `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` had SHA-256 `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb`; that path and the adjacent merge report/register remained read-only.

**Out of scope:** editing frozen claims, changing production code, committing/pushing, modifying lane git/jj state, contacting bounty targets, package/fleet/sibling writes, broader design changes, and claiming a canonical C1/C2 verdict.