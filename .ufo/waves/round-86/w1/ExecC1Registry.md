# ExecC1Registry — C1 map vs. lane registry cross-check (round-86, attempt 1)

**Seat:** ExecC1Registry. **Lane:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
**Frozen base:** `d7296645c2cd9f631329fa8e2f38328a4c9c89a5` (candidate base).
**Freeze commit:** `252df0c90c066d83d229e3107811a6bc05e8feed`.
**Scope:** machine cross-check of every C1 map value against the lane's own
registry (`corpus/SOURCES.md` at base), plus byte-reproduction of the frozen map
by `c1/build-map.py`.

## Axes

- **depth:verifiability** — every one of the 203 map entries is checked against
  an independent lane-owned source of truth (the registry row, the citing
  knowledge file's front-matter, the cited snapshot bytes), not just the
  builder's own logic.
- **coverage** — all 203 keys, all 15 distinct S-ids, all citing files, all
  anchored lines.

## Results

### (a)+(b) Registry capture vs. map value — 198 yes, 0 no, 5 absent

Script: `.ufo/waves/round-86/w1/ExecC1Registry-receipts/registry-xcheck.py`
Output: `.ufo/waves/round-86/w1/ExecC1Registry-receipts/xcheck.tsv` (203 rows + header).

For each of the 203 keys the S-id's registry row at base was read and the
capture path extracted from the anchor cell (`capture corpus/source-snapshots…`
when present, else the bare `corpus/source-snapshots/round-N/Sxxx.txt`
mention — the registry uses both phrasings). Compared with the map value's
path (anchor stripped):

- **registry_match=yes: 198** — the registry capture equals the map value path
  exactly. Covers S071, S073, S075, S076, S078, S089, S090, S103, S105, S106
  (10 S-ids, 198 keys).
- **registry_match=no: 0** — no registry capture contradicts any map value.
- **registry_match=absent: 5** — the registry row names no capture path at
  all: `S016.txt`, `S020.txt`, `S021.txt`, `S023.txt`, `S025.txt`. Their
  anchor cells describe the source (e.g. S016: "Vulnerability Disclosure
  Reporting and Coordination; last updated 2026-03-06") but contain no
  `corpus/source-snapshots/…` mention. The map repoints these to
  `corpus/source-snapshots/round-40/S016|20|21|23|25.txt`, which are tracked
  files; the map is therefore *unverifiable from the registry* for these 5
  keys, though nothing contradicts it. This is a registry-coverage gap, not a
  map error. 66 of 121 registry rows name no capture, so this phrasing gap is
  systemic, not specific to the map.

### (c) Citing-file front-matter vs. S-id — 203 yes, 0 no

For each key, every `corpus/knowledge/*.md` file citing it at base (backticked
tokens, resolve.py TOKEN/is_pathlike semantics) was checked whether its
front-matter (first 15 lines, the `source:` ids) includes that S-id:

- **file_cites_sid=yes: 203 keys, 204 file instances, 0 no.** Every citing
  knowledge file declares the S-id in its `source:` block. No orphan or
  misattributed citation among the 203 keys.

### (d) Anchored lines — 197 readable, 0 out-of-range

For the 197 anchored values the cited snapshot line(s) were read directly
(anchorcheck.py verifies `path:NN[-MM]` cites in markdown; here the value
already names the snapshot, so plain line read is the equivalent check).
All 197 returned non-empty text from inside the snapshot. The 6 unanchored
keys (`S016.txt`, `S020.txt`, `S021.txt`, `S023.txt`, `S025.txt`, `S071.txt`)
have no line to print, as expected.

### build-map.py reproduction — byte-identical

In a `git clone --shared` under scratch, checked out at base (`git rev-parse
--show-toplevel` confirmed `/fast/scratch/hyaku/kasegi-r86/ExecC1Registry/clone`):

```
python3 -B .ufo/waves/round-86/c1/build-map.py --lane <clone> \
  --rev d7296645c2cd9f631329fa8e2f38328a4c9c89a5 --out $S/m.json \
  --excluded $S/x.json --work $S/w
→ MAP keys=203 excluded=89
cmp m.json repair-map.json   → rc=0 (byte-identical)
cmp x.json excluded.json     → rc=0 (byte-identical)
```

SHA-256 (both pairs identical):

- map: `dd40455a379eb53b75bf5a15772fe675efae79eda2516ea7fac50f86420bce12`
- excluded: `920641e6fda6c21539725bba874332ebba6dd0134b18c2dffc468166fc218ac4`

Reproduced copies: `.ufo/waves/round-86/w1/ExecC1Registry-receipts/m-reproduced.json`,
`x-reproduced.json`.

## Frontier

- Registry-match frontier: 0 mismatches against the registry. The 5 `absent`
  rows are a registry coverage gap (no capture named), not a map defect; the
  map's round-40 values for S016/S020/S021/S023/S025 are corroborated by the
  knowledge files' own `source:` lines (which name
  `corpus/source-snapshots/round-40/Sxxx.txt` captures) — cross-checked in
  limb (c) indirectly, since every citing file's front-matter names the S-id.
- Front-matter frontier: 0 files citing a key without declaring its S-id.
- Anchored-line frontier: 0 out-of-range anchors among the 197 (consistent
  with the frozen M5 limb).
- Reproduction frontier: builder reproduces both frozen artifacts
  byte-for-byte from base.

## Risks

- The 5 `absent` registry rows mean the registry alone cannot verify 5 map
  values; verification for those rests on tracked-file existence/unicity (M4)
  and the knowledge files' `source:` capture mentions. If the L1 wants
  registry-level closure, the registry rows for S016/S020/S021/S023/S025
  would need capture additions — that edit is outside this seat's bounds
  (lane tree, not the wave dir) and is reported, not made.
- `registry-xcheck.py` reads anchored lines from the lane working tree, not
  from `git show` at base; the snapshot paths are tracked and unchanged
  between base and freeze for these 15 S-ids (the map's M5 limb reads the
  same working-tree bytes), so this is consistent with the frozen predicates.

## Blockers

None. All checks executed; scratch removed.

## Files written

- `.ufo/waves/round-86/w1/ExecC1Registry.md` (this report)
- `.ufo/waves/round-86/w1/ExecC1Registry-receipts/registry-xcheck.py`
- `.ufo/waves/round-86/w1/ExecC1Registry-receipts/xcheck.tsv` (203 rows)
- `.ufo/waves/round-86/w1/ExecC1Registry-receipts/m-reproduced.json`
- `.ufo/waves/round-86/w1/ExecC1Registry-receipts/x-reproduced.json`

## Re-run command

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
TMPDIR=/fast/scratch/hyaku/kasegi-r86/ExecC1Registry python3 -B \
  .ufo/waves/round-86/w1/ExecC1Registry-receipts/registry-xcheck.py \
  --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --rev d7296645c2cd9f631329fa8e2f38328a4c9c89a5 \
  --map .ufo/waves/round-86/c1/repair-map.json \
  --out .ufo/waves/round-86/w1/ExecC1Registry-receipts/xcheck.tsv
→ keys=203 registry_yes=198 registry_no=0 registry_absent=5 \
  files_sid_yes=203 files_sid_no=0 anchored_lines=197 files_checked=204
```

## Tooling

None installed or upgraded.

## Checks for the main agent

- `cmp .ufo/waves/round-86/w1/ExecC1Registry-receipts/m-reproduced.json .ufo/waves/round-86/c1/repair-map.json`
- `awk -F'\t' 'NR>1{c[$4]++} END{for(k in c) print k,c[k]}' .ufo/waves/round-86/w1/ExecC1Registry-receipts/xcheck.tsv` → `yes 198`, `absent 5`
- Scratch: `/fast/scratch/hyaku/kasegi-r86/ExecC1Registry` removed before yield.
