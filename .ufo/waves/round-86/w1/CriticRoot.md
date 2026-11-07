# CriticRoot — attack on C1 root-independence (round-86, attempt 1)

Hypothesis under test: *C1's knowledge-meter reading at freeze+map is root-independent
except for the one token `../MISSION.md:49-56`.*

Verdict: **FALSIFIED as literally stated** (two further tokens differ at a root without a
`.git` directory), **CONFIRMED inside the frozen root class** (two independent
`git clone --shared` checkouts: 0 differing tokens, 398/1721 -> 596/1716, M1-M6 pass, rc 0).
P1 holds at the C1 landing commit `fdb5f4a` (verified); it fails at the later lane HEAD
`e73c1f9` for an integration reason unrelated to the root — see §Integration state.
The invariant is *not* "root-independent" but "a checkout whose `.git` is a directory and
whose parent holds no `MISSION.md`".

## Roots and exact commands

All at freeze 252df0c90c066d83d229e3107811a6bc05e8feed, base d7296645c2cd9f631329fa8e2f38328a4c9c89a5,
map `.ufo/waves/round-86/c1/repair-map.json` sha256 `dd40455a379eb53b75bf5a15772fe675efae79eda2516ea7fac50f86420bce12`.
`git diff --stat d729664 252df0c -- corpus/knowledge` is empty: freeze knowledge bytes == base bytes.

R1 (frozen root class) — `git clone -q --shared <lane> $S/clone`; HEAD 252df0c; map applied in the
clone worktree with the frozen `apply-map.py`. Full frozen counting command shape:
`python3 -B .ufo/waves/round-86/c1/knowledge-meter.py --lane $S/clone --base-rev d729664 --map
$S/clone/.ufo/waves/round-86/c1/repair-map.json --target 596/1716 --map-sha256 dd4045... --work $S/w`
-> `base=398/1721 after=596/1716 target=596/1716 keys=203`, M1-M6 pass, `rc=0` (receipt `meter-clone.txt`).

R1b (second checkout, P1 path shape) — `git clone -q --shared <lane> $S/verify/land`, map applied,
same command -> identical line, M1-M6 pass, rc 0 (`meter-verifyland.txt`).

R2 (archive, no `.git`) — `git -C <lane> archive 252df0c | tar -x -C $S/arch`: every tracked file at
freeze, token set identical (1721 base / 1716 after). `--base-rev` needs git, so both scopes were
classified with the frozen meter's own functions via importlib (`knowledge-meter.py`:
`load_resolve` / `scope_files_tree` / `classify_scope` / `rate`; dumper copied to
`receipts/dump.py`) with `lane=$S/arch`:
- after: `scope_files_tree($S/arch)` after `apply-map.py --root $S/arch`;
- base: `git show d729664:corpus/knowledge/*` exported to a plain dir (git only reads the lane).
Variants: `mkdir $S/arch/.git` (empty dir) and `$S/arch-file` with `.git` as a regular file
(worktree-style marker).

R3 (lane checkout, fleet root) — read-only, `--measure-rev 252df0c` only; the map was **not** applied
there. After-scope for the lane classified from base+map bytes built in scratch (byte-identical to
the lane working tree at 22:12; see §Integration state) with `lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

Control (fleet geometry) — `git clone --shared` into `$S/lane-mission/land` with a `MISSION.md` in its
parent; map applied; full command -> `base=399/1721 after=597/1716`, M1 FAIL, M2-M6 pass, rc 1
(`meter-fleet-geometry.txt`). This shows `MISSION.md` is the only parent-directory lever and that the
exact target is a root fingerprint, not a map property.

## Rates

| root | `.git` | parent `MISSION.md` | base | after | vs R1 tokens |
|---|---|---|---|---|---|
| R1 clone $S/clone | directory | no | 398/1721 | **596/1716** | — |
| R1b clone $S/verify/land | directory | no | 398/1721 | **596/1716** | none (base and after) |
| R2 archive (no `.git`) | absent | no | 396/1721 | 594/1716 | `.git`, `.git/` |
| R2 archive + empty `.git` dir | directory | no | 398/1721 | 596/1716 | none |
| R2 archive + `.git` regular file | file | no | 397/1721 | 595/1716 | `.git/` |
| R3 lane checkout (freeze+map scope) | directory | **yes** (`../MISSION.md`) | 399/1721 | 597/1716 | `../MISSION.md:49-56` |
| control, fleet geometry (freeze+map scope) | directory | yes | 399/1721 | 597/1716 (M1 FAIL) | same |

Every root has 98 knowledge files and exactly the same token sets (1721 base / 1716 after), so all
deltas are class-level, not extraction loss. `mirror_absent=True` at every root (`KASEGI_MIRROR`
unset; both `MIRROR_CANDIDATES` absent), so the mirror dimension does not vary.

## Token-level diff (exact)

- R1 vs R3, base **and** after: `../MISSION.md:49-56` GONE -> INTERNAL (cited
  `corpus/knowledge/source-tree-loss-2026-09-28.md:315`). Only difference.
- R1 vs R2 (no `.git`), base and after: `.git` and `.git/` INTERNAL -> GONE. Both are path-like to
  `resolve.py` (`git` is in `EXTS`; `.git/` ends in `/`). Cited at
  `corpus/knowledge/ops-invariants.md:124`, `root-loss-2026-10-12.md:18`,
  `source-tree-loss-2026-09-28.md:77` (`.git/`), `:120`, `:218`, `:251`; these are VCS-state
  citations that resolve on the existence of the checkout marker, not on corpus content.
- R1 vs R2 + `.git` **directory**: no differing tokens — the archive delta is exactly the marker.
- R1 vs R2 + `.git` **file**: `.git/` only (`os.path.exists("<lane>/.git/")` is false for a file).
- R1 vs R1b: no differing tokens (base and after).
Receipt: `receipts/token-diffs.json`.

## Impact on the claim

- Impacted axis: depth:verifiability (C1). Not coverage; no C2 interaction.
- P1/P2 unaffected: instrument bytes at HEAD match `claims.json` (meter `03df491b...`, applier
  `2a11c1c6...`, builder `222f92e6...`, map `dd40455a...`, resolve `db5e0767...`); the verbatim frozen
  command gives the exact frozen line, M1-M6 pass, rc 0 at two independent clone roots and at the
  C1 landing commit `fdb5f4a`; at `e73c1f9` it fails for a token-set reason - see §Integration state.
- No map key, limb, target, or measuring root changed; no identity change; no duplicate authority.

## Smallest safe correction

1. This round (documentation only; P2 freezes instrument bytes): record the full root fingerprint —
   the reading is invariant across checkouts with `.git` **as a directory** and no `MISSION.md` in the
   parent; a `.git`-less tree reads 594/1716 (`.git`, `.git/` differ), a `.git`-file tree 595/1716
   (`.git/`), a fleet-positioned tree 597/1716 (`../MISSION.md:49-56`).
2. Next round (not now): have the meter fail closed (`rc 2`) unless `os.path.isdir(<lane>/.git)`.
   Today's docstring precondition "a checkout that has .git" is satisfied by a `git worktree`
   (`.git` file) which reads 595/1716; a verifier using one would see M1 FAIL and could misattribute
   it to the map. Do not change the frozen instrument this round.

## Integration state moved during this review (not part of the root verdict)

At 22:12, when the root measurements ran, HEAD was the freeze commit `252df0c` and the working tree's
`corpus/knowledge` was byte-identical to base+map (14 ` M` files, `diff -r` empty); the lane base
reading was reproducible only with `--measure-rev` (399/1721), and `apply-map` is idempotent
(`APPLY files_changed=0` on a second run).

By 22:16 the lane had landed and then amended C1:

- `fdb5f4a` "C1 landing - frozen 203-key snapshot repoint map applied to corpus/knowledge": the frozen
  command **passes** there exactly — `base=398/1721 after=596/1716 target=596/1716 keys=203`, M1-M6
  pass, rc 0 (`meter-landing-fdb5f4a.txt`).
- `e73c1f9` "revert 4 C1 repoints that rewrote a quoted round-40 manifest path field
  (ReviewC1Semantics Finding 1)": the reverted keys are `S020.txt`, `S021.txt`, `S023.txt`,
  `S025.txt`, each the `path` field of a quoted round-40 manifest record in
  `corpus/knowledge/cisa-bod-20-01-vdp-minimums.md`, `cisa-cvd-program-stages.md`,
  `cve-bench-agent-exploitation-benchmark.md`,
  `doj-vdp-framework-scope-and-authorization.md` (`landing-state.txt`).
- At `e73c1f9` the frozen command prints `base=398/1721 after=596/1720 target=596/1716 keys=203`,
  **M1 FAIL** (596/1720), **M2 FAIL** (`unrepaired=4`), **M3 FAIL** (`bad_lines=4`), M4/M5/M6 pass,
  rc 1 (`meter-head-e73c1f9.txt`). The token set grows back by exactly the 4 bare keys
  (1716 + 4 = 1720): each reverted line keeps the already-present full-path pin token and re-adds a
  bare `S0xx.txt` token, GONE at every root measured here.

Consequence: if `e73c1f9` is the landing commit, P1 is false and C1 fails under its own kill rule —
for a token-set reason, not a root effect. The frozen M3 requires exactly the mechanical key->value
replacement on those 4 quoted manifest `path` fields, so the frozen target 596/1716 is reachable only
by making the quoted records state a path the manifest does not contain; ReviewC1Semantics Finding 1
and the frozen target are mutually exclusive under the frozen bytes. The L1 must either land
`fdb5f4a` (accepting the 4 rewritten quotes) or record C1 as failed; the map, target, limbs and
measuring root cannot be adjusted after the freeze.

Re-runnable, for `<commit>` in {`fdb5f4a`, `e73c1f9`}:
`S=<scratch>; git clone -q --shared <lane> $S/land && git -C $S/land checkout -q <commit> &&
python3 -B $S/land/.ufo/waves/round-86/c1/knowledge-meter.py --lane $S/land --base-rev
d7296645c2cd9f631329fa8e2f38328a4c9c89a5 --map $S/land/.ufo/waves/round-86/c1/repair-map.json
--target 596/1716 --map-sha256 dd40455a379eb53b75bf5a15772fe675efae79eda2516ea7fac50f86420bce12
--work $S/w`

## Wave hygiene, adjacent (not a C1 finding)

The staged C2 candidate directory already holds snapshot copies
`w1/ExecC2Package-candidate/curl-ibb-h1-1997312/evidence/S120-S123.txt`. None of them collides with
this round's 203 map keys (key prefixes 016, 020, 021, 023, 025, 071, 073, 075, 076, 078, 089, 090,
103, 105, 106; no S052 and no S120-S123), so M4/P1 are unaffected if w1 is committed as-is. They do
add tracked duplicates of snapshot basenames (S120/S121 are already duplicated at freeze by
`corpus/practice/curl-h1-1913733/evidence/` and round-85 wave receipts), which would block any future
map that keys those names; decide before committing the candidate payload.

## What I did not run
No full `resolve.py` lane census; no write to the lane outside `w1/` (no map application at the lane);
no git/jj writes anywhere (clones/archives only in scratch; `rev-parse --show-toplevel` asserted for
all three clones, receipt `clone-toplevels.txt`; the two landing-commit meter runs used fresh
scratch clones, read-only w.r.t. the lane); no network; no tool installs.

## Files written
- `.ufo/waves/round-86/w1/CriticRoot.md` (this file)
- `.ufo/waves/round-86/w1/CriticRoot-receipts/`: `meter-clone.txt`, `meter-verifyland.txt`,
  `meter-fleet-geometry.txt`, `root-rates.txt`, `token-diffs.json`, `lane-tree-state.txt`,
  `clone-toplevels.txt`, `landing-state.txt`, `meter-landing-fdb5f4a.txt`, `meter-head-e73c1f9.txt`,
  `dump.py`
Scratch `/fast/scratch/hyaku/kasegi-r86/CriticRoot` and `/fast/scratch/hyaku/kasegi-r86/CriticRoot2`
deleted after copying receipts.
