# ExecC1Indep — independent re-derivation of round-95 C1 (no lane counter)

Seat: ExecC1Indep, round 95 attempt 1, wave 1. Date: 2026-11-07.
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Base 9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10, C1 landing 53ec479d71d25cf5be052db794a548a5904564b8.

## Verdict

AGREE — C1 stands. I re-derived every limb myself from `git show` of the two pinned revs, without running or importing the lane's counter:

1. **Changed lines, computed independently.** The landing changes exactly 14 physical lines across the two corpus/knowledge files, carrying the 16 map rows (lines 88 and 433 each carry two rows):
   - `corpus/knowledge/triage-thresholds.md` (488 lines before and after): 88 (2 rows), 89, 90, 356, 396, 433 (2 rows), 434, 435, 436.
   - `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` (68 lines before and after): 13, 34, 43, 54, 64.
   My computed changed-set equals the map's site set for both files; no other line differs.
2. **Composition.** Every landing line equals its base line with its map old->new replacement(s) applied in map order (`str.replace` semantics, 2 rows composed sequentially on 88 and 433). All 16 rows: `old_missing=0`, `composed==after: True`.
3. **S041 capture targets at the landing.** `corpus/source-snapshots/round-30/S041.txt` exists (2354 lines); ranges 1868-1870, 1792-1867, 1996-2079, 1868 are all inside it; the bare-name row's target file exists.
4. **Anchor ranges inside their files at the landing.** SKILL.md = 1251 lines: 182-184, 255-257, 999, 335-338 all inside (first lines quoted in receipt 04 match the labels' content claims: 182-184 is the five-term dispatch ordering, 255-257 the curated/reward.min×1000/is_live correction, 335-338 carries `gitMutationBlocker`). `corpus/knowledge/mission-control.md` = 171 lines: 21-27 inside.
5. **Meter reproduced with my own implementation** of the pinned census classify (density.py path-like extraction; bounty/mirror/relative domains; literal/brace/glob existence), scoped to `corpus/knowledge/*.md` with lane_root = full extracted tree, over both revs: **base = 1007/1998, after = 1008/1994** — equal to the claim.
   - Categories counted as resolved: every non-GONE class (RESOLVES + INTERNAL + MIRROR-EQUIVALENT).
   - base: RESOLVES=23, MIRROR-EQUIVALENT=0, INTERNAL=984, GONE=991.
   - after: RESOLVES=23, MIRROR-EQUIVALENT=0, INTERNAL=985, GONE=986.
   - Delta: 12 unique tokens removed (the 5 bare `S041.txt*` tokens, all GONE at base, plus 7 INTERNAL tokens `SKILL.md:10-11`, `:113-114`, `:175`, `:175-176`, `:245-247`, `:522`, `mission-control.md:21-23`), 8 added (all INTERNAL: the 4 repointed SKILL/mission-control anchors + 4 `corpus/source-snapshots/round-30/S041.txt*` paths). No token changed class. Net: −4 tokens, +1 resolved — exactly the claim's movement.
   - Host context: KASEGI_MIRROR unset and neither mirror candidate directory exists, so `mirror_absent=True` on both readings — the same context the frozen controls printed.
6. **Pins.** repair-map.tsv sha256 8545eba2c39a1fed66b5d6eba59de973c182208aa8b06d28013417821359beb6, labels.tsv cf73949702a569385e0c68390177f454f050f101659edc5ad89410973f0379d0, knowledge-meter.py c0799f4c52441671b722ccdaa51b579a71c1e3f3c51074d062c7952606878db8 (blobs at the landing) — all equal the claims.json pins.

Routed observations (qualifiers, not verdict changes):

- `.ufo/waves/round-95/controls/c1-controls-r95.txt` recorded the pre-freeze candidate landing `after_rev=4ef12a2fc6797ab7fe9a9163a916e82800495142`, which is not an object in this repo (it was the pinned fixture clone's rev; `git cat-file -t` fails: "bad object"). The actual landing 53ec479d reproduces the identical readings (1007/1998 -> 1008/1994) under my own implementation, so the numbers hold; a post-landing controls re-run will print `after_rev=53ec479d…`, and that after_rev difference from the frozen receipt text is expected, not a control failure.
- 53ec479d is the combined wave commit (also carries the C2 instrument changes, claims.json, controls, make-wave script). C1's corpus/knowledge delta is confined to exactly the two named files (`git diff --name-only base..landing -- corpus/knowledge/` lists only those two; no round-30 snapshot change).

No tool installs or upgrades were performed (none needed). No git/jj mutation anywhere; fixture-free, read-only on the lane.

## Receipts

All under `.ufo/waves/round-95/w1/ExecC1Indep-receipts/` (written by `rederive-c1.py`, the implementation kept as evidence; run with `TMPDIR=$S` in seat scratch, scratch removed after):

- `01-commits.txt` — `git log -1 --format=%H %s <base>` (rc 0, subject "round-94 verifier spot-check…"); same for landing (rc 0, subject "round-95 C1: tranche 10 …"); `git diff --stat base landing -- corpus/knowledge/ corpus/source-snapshots/round-30/` → "2 files changed, 14 insertions(+), 14 deletions(-)"; `git diff --name-only base landing -- corpus/knowledge/` → the two files (rc 0).
- `02-pins.txt` — sha256 of the three committed blobs at the landing (rc 0; values above, all match claims.json).
- `03-changed-lines-and-map.txt` — 16 rows / 14 site lines; per-file changed-line list computed from `git show` blobs vs map sites (`changed-set==map-sites: True` twice); per-line `rows=… old_missing=0 composed==after: True` for all 14 lines (rc 0).
- `04-s041-and-anchors.txt` — capture exists=True lines=2354, 4 ranged rows inside, bare row file exists (5/5 True); SKILL.md lines=1251 with 182-184/255-257/999/335-338 inside (4/4 True, first-line quotes); mission-control.md lines=171, 21-27 inside (True) (rc 0).
- `05-meter-repro.txt` — `MY-METER base=1007/1998 after=1008/1994`; `MY-MIRROR … mirror_absent=True/True`; `MY-CATS base RESOLVES=23 MIRROR-EQUIVALENT=0 INTERNAL=984 GONE=991`; `MY-CATS after RESOLVES=23 MIRROR-EQUIVALENT=0 INTERNAL=985 GONE=986`; `MY-DELTA tokens_removed=12 added=8 class_changed=0` with the full token lists; `MY-CHECK base==1007/1998: True ; after==1008/1994: True` (rc 0).
- Extra (not a file): `git cat-file -t 4ef12a2fc6797ab7fe9a9163a916e82800495142` → "fatal: bad object" (candidate landing absent from this repo; see routed observation).
