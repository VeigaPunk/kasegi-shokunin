# ScoutDatawalk — kasegi round 30, wave 1 (hyaku run 7 inline spawn)

Seat: `ScoutDatawalk-3` (leaf L2 data-walk; no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write scope).
Lane base: `a94871315cafa368f79c17d8c62d71fddd967986`. Claims-freeze: `3c5573541300ba0fd3d89372dda3d841172eaa3f`.
Measured at lane HEAD `002e92c` (wave-1 spec + dispatch) on 2026-10-25, working tree.
Model: `inception/mercury-3` (operator route; no model passed). Tool installs: none required (no install performed).

## 1. Frozen counters run from the lane root; BEFORE values hold at the freeze commit

Commit identity checks (read-only git):
- `git -C <lane> cat-file -t 3c557354…` → `commit`; `cat-file -t a94871315…` → `commit`.
- `git -C <lane> merge-base --is-ancestor a94871315… 3c557354…` → exit **0** (base is ancestor of freeze).
- `git -C <lane> log --oneline` round-30 commits: `218abb0` (round-29 leftover resolution), `3c55735` (claims freeze + before receipts), `002e92c` (wave-1 spec + dispatch = HEAD).

Freeze-commit receipts are byte-identical to the worktree copies (`git show 3c557354…:<path> | cmp -s - <path>` → exit 0 for all):
- `.ufo/waves/round-30/c1-controls/before.txt`, `.ufo/waves/round-30/c2-controls/before.txt`,
  `.ufo/waves/round-30/census-before.txt`, `.ufo/waves/round-30/claims.json`.

Instrument digests at the freeze commit (`git show 3c557354…:corpus/instruments/<f> | sha256sum`) and in the worktree:

| instrument | sha256 at freeze | sha256 worktree |
|---|---|---|
| `corpus/instruments/frontier-recheck-count.py` | `c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261` | identical |
| `corpus/instruments/source-recheck.py` | `9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96` | identical |

Both digests match the committed `c1-controls/before.txt` instrument-digest block.

C1 counters run verbatim from claims.json (from the lane root):

- A1 (frontier harness, missing-row fixture): exit **1**, uncaught `FileNotFoundError` traceback naming
  `.../harness-root-a1/corpus/knowledge/zz-missing.md`, **no named-row marker** → identical to `c1-controls/before.txt` (a1_exit=1, FileNotFoundError traceback, no named-row marker).
- A2 (duplicate-target fixture): `PASS F98 … exit=0`, `PASS F97 … exit=0`, `entries=2 pass=2 exit=0`, exit **0** → identical (a2_exit=0, pass=2 on duplicate target).
- B1 (stem-mismatch manifest): `S043:sha256 OK`, `S043:Q1 OK normalized=markup-whitespace occurrences=1`, exit **0** → identical (b1_exit=0; stem mismatch passes).
- B2 (double-occurrence manifest): `S045:sha256 OK`, `S045:Q1 OK occurrences=2 anchor=MISSING`, exit **0** → identical (b2_exit=0).

C2 counters run verbatim from claims.json:

| # | counter | measured | before receipt |
|---|---|---|---|
| 1 | frontier admitted (`awk … corpus/README.md`) | **13** | 13 |
| 2 | entries citing `source: S04[6-7]` | **0** | 0 |
| 3 | registry rows `S04[6-7]` (`grep -cE …`) | **0** (grep exit 1 = no match, expected) | 0 |
| 4 | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit **0**; `kasegi W04 S028 …`, `kasegi W04 S029 …`, `kasegi ok …/corpus/SOURCES.md` | census_exit=0, W04 S028/S029 only |
| 5 | `frontier-recheck-count.py` on the real corpus | `entries=16 pass=16 exit=0` (F01–F13 all PASS), exit **0** | harness entries=16 pass=16 exit=0 |
| 6 | per-id source-recheck on round-30 manifest | `manifest UNAVAILABLE reason=missing`, **recheck_exit=2** | not recorded in before receipt (post-landing counter; round-30 captures absent pre-landing) |

Result: every C1/C2 counter measured against the working tree reproduces the committed before record byte-for-byte where the before receipt records it. Counter C2-6 is the only one not recorded in `c2-controls/before.txt`; it fails closed (`reason=missing`, exit 2) because `corpus/source-snapshots/round-30/` does not exist yet — the expected pre-implementation state.

## 2. Porcelain state — no pre-existing production drift

`git -C <lane> status --porcelain` at measurement time (exit 0):

```
?? .ufo/waves/round-30/assimilation/
?? .ufo/waves/round-30/kasegi-r30-build.ready
?? .ufo/waves/round-30/kasegi-r30-build.ready.dispatched
?? .ufo/waves/round-30/plan.err
?? .ufo/waves/round-30/run.err
?? .ufo/waves/round-30/wave1/swarm-registry.json
```

- Zero tracked modifications/deletions/additions across the whole lane (no `M`/`D`/`A` lines) — production files (`corpus/*`, `SKILL.md`, `SCORECARD.md`, instruments) are unmodified; instrument worktree hashes equal the base/freeze hashes (§1).
- The six untracked paths are all round-30 wave-owned dispatch artifacts (`plan.err`/`run.err`, ready markers, `wave1/swarm-registry.json`, `assimilation/` quarantine roster slice).
- No drift beyond the wave's own files. (Note: `218abb0` committed the round-29 leftover resolution the round-29 verifier spot-check routed — killtry-lab deletions + S069 fetch — so those leftovers are no longer worktree drift.)

## 3. Round-30 claims target the lowest non-retired axis + a second distinct axis

Per `claims.json` (frozen) and `SCORECARD.md`:
- `lowest_non_retired_axis: "depth:verifiability (4)"` — matches SCORECARD: depth:verifiability **4** (held r19/r22/continuation; lowest of density 9, coverage 7, verifiability 4).
- **C1** → `depth:verifiability`, `score_before: 4` (instrument conformance for frontier-recheck-count.py + source-recheck.py; M29-4/M29-3).
- **C2** → `coverage`, `score_before: 7` (frontier F14 assimilation; S046/S047 this-round rows + S041).
- density (9) is not claimed this round; no axis retired (SCORECARD "Retired: None"). C1/C2 are the two distinct axes: verifiability 4 (lowest non-retired) and coverage 7.

## 4. No earlier round-30 attempt artifacts

- Freeze-commit tree (`git ls-tree -r 3c557354… -- .ufo/waves/round-30`) contains exactly: `claims.json`, `c1-controls/before.txt` + `a1.out`/`a1.err` (recorded before-run outputs) + C1 fixture tree (`harness-root-a1`, `harness-root-a2`, `q9/manifest-b1.json`, `q9/manifest-b2.json`, `q9/B2.txt`, `q9/S045.txt`), `c2-controls/before.txt`, `census-before.txt`. No wave/attempt artifacts at freeze (no dispatch dir, no wave1, no attempt-2, no killtry).
- Tracked at HEAD adds only dispatch artifacts: `plan.out`, `run.out`, `wave1-dispatch.json`, `wave1-spec.json`, `wave1/build-spec.py`.
- Untracked adds only dispatch artifacts (§2) — `assimilation/quarantine-slice` is the merge-package roster slice (S037/S054/S048/S065/S068/S069/S070), not an attempt artifact.
- Git history shows no earlier round-30 attempt commit: the only round-30 commits are `218abb0` (leftover resolution), `3c55735` (freeze), `002e92c` (dispatch). `claims.json` records `"attempt": 1`.
- Verdict: no earlier round-30 attempt artifacts exist; only the committed freeze files (plus this wave's own dispatch artifacts).

## Scope compliance

No write outside the lane working tree; no git/jj mutation (read-only git only); no live contact target; no packetman transaction; no install.
