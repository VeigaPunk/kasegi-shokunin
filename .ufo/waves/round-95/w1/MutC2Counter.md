# MutC2Counter — round-95 C2 gate: mutation test of `capability-check.py`

Seat: MutC2Counter (leaf, mutation tester). Lane: `kasegi-shokunin`. Scratch:
`/fast/scratch/hyaku/kasegi-r95/MutC2Counter` (created at seat start, removed by the seat's
`EXIT` trap; no seat artifact outlives it). Tool installs: none. No mutating git/jj command
was issued against the lane; every mutation lived in a scratch clone.

## Target and pins (re-hashed at the seat)

| object | sha256 |
|---|---|
| gate `.ufo/waves/round-95/c2/capability-check.py` | `9011e1b474d74a376b35301af562e70f4a6235c09798d15f429b70f0144fddf6` |
| mutated object: `corpus/instruments/capture-secret-scan.py` at `38e7319f44a9fab2978b59ffd43faf207cf62b32` | `66edd66143ec62f6e40c864817a97383916d7ff67e5ab384e130b65c44516707` |
| gate pin in `claims.json` (`gate_sha256`) | `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` |

All three equal `claims.json` (`22-target-hashes.txt`). The landed working-tree instrument and
the landing blob are byte-identical (`00b-`, `21-`).

## Method

- Nine forgery instruments. Each is the landed scanner bytes plus **exactly one** behavioural
  defect, compiled, committed on top of the C2 landing in a scratch clone; each commit changes
  one file only (`03-forgery-revs.txt`).
- where a defect would make the instrument's own selftest fail, the selftest expectations were
  flipped to match the defect, so every forgery still prints `SELFTEST-RESULT pass cases=115`
  rc 0 (`02-forgery-selftests.txt`). The mutant therefore cannot be refused by K1's selftest
  clause; only the digest pin and K2–K6 can refuse it.
- Each forgery was run twice by the gate: (a) **pinned**, with the claim's
  `--instrument-sha256` and `--gate-sha256`; (b) **unpinned**, with both pins omitted, which
  exposes the behavioural residue. Fixed seeds: 95000 baseline; 95101–95109 per forgery.
- Controls: real lane at `38e7319` pinned → `pass rc=0` (`00-`); the unmodified scratch clone
  at `38e7319` pinned → `pass rc=0` with identical limb text (`04-`). A forgery failure is
  therefore attributable to the forgery, not to the clone.

## Verdict

8 of 9 forgeries are killed; `F6-fixture-literals` **survives K2–K6** when
the digest pin is not supplied and the gate prints `CAPABILITY-CHECK-RESULT pass rc=0`
(`17-F6-fixture-literals-unpinned.txt`). A survivor is a routed gate gap for round 96 — no
target narrowing and no re-wording is claimed here. With the claim's pins every forgery is
refused at K1 on `inst_sha`, but a caller-supplied digest authenticates bytes, not correctness:
a wave that lands a defective instrument and re-pins to its digest would also pass K1.

## Killed / survived

| forgery | defect | pinned: failing limbs | unpinned: failing limbs |
|---|---|---|---|
| F1 always-clean | `report()` suppresses every recorded hit; scanned/allowed/unused counters stay true | K1 `inst_sha=b21920d0…`; K3 `hits=0 missing=6`; K6 `rc=0 shapes=none` | K3, K6 |
| F2 plant-path-drops | skips every match whose basename has the gate's nonce-plant shape `[a-z0-9]{12}-[a-z]\d?\.[a-z]+` | K1 `inst_sha=9bad2ae2…`; K3 `hits=0 missing=6` | K3 |
| F2b plant-path-injects | emits both new shapes on every plant-shaped basename | K1 `inst_sha=3995ba1a…`; K3 `hits=24 missing=none`, 18 extras over 12 files | K3 |
| F3 drops gh-refresh | deletes the `github-refresh-token` pattern; selftest cases flipped to `set()` | K1 `inst_sha=7b8a6727…`; K2 `allowed=24 unused_allow=1`; K3 `hits=4 missing=2` | K2, K3 |
| F4 accepts 74–78 | `_GH_REFRESH` `{76}` → `{74,78}`; selftest 75/77 cases flipped | K1 `inst_sha=77bde7bd…`; K3 `hits=8 extra=n1,n2` | K3 |
| F5 any glcbt- prefix | new-family branch accepts `glcbt-/glsat-/gliamat-` + any 10-char run, no `eyJ` structure | K1 `inst_sha=13ede72b…`; K2 `hits=1` on `.ufo/waves/round-94/w1/SentinelShapes-receipts/08-unlisted-classes.txt:75`; K3 `hits=8 extra=n3,n4` | K2, K3 |
| **F6 fixture-literals** | for the two new shapes, reports a match only when the matched bytes are one of 10 known literals (the four plant constants plus the `acme-`-prefixed form p5 produces, the allow row's value, four selftest values) | K1 only: `inst_sha=61f088a9…` vs pin `66edd661…`; K2–K6 all `ok` | **none — `pass rc=0`** |
| F7 worktree-not-rev | `scan_rev` walks the checkout instead of reading `rev` blobs; `--rev` ignored | K1 `inst_sha=959c36b8…`; K6 `rc=0 shapes=none` | K6 |
| F8 allow-accepts-anything | any non-empty allowlist accepts every match | K1 `inst_sha=34ef6004…`; K3 `hits=0 missing=6`; K6 `rc=0 shapes=none` | K3, K6 |

Baseline and clone control, both `CAPABILITY-CHECK-RESULT pass rc=0`: K1 `inst_sha=pin-ok
gate_sha=pin-ok selftest=pass cases=115`; K2 `scanned=2477 hits=0 allowed=26 unused_allow=0`;
K3 `hits=6 missing=none extra=none`; K4 `base_new_shape_hits=0 old_shapes_missing=none`;
K5 `rows=1 last=87`; K6 `rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential`.

## The survivor, and why it survives

`F6-fixture-literals` is a general-looking scanner whose two new patterns fire only on values
it has memorised. It passes every behavioural limb:

- **K3** — the six expected positives are built from the gate's module constants (`GH76`,
  `JWT_CLCBT`, `JWT_GLSAT`, `JWT_GLIAMAT`, and the `GJ1`–`GJ3` segments), plus the
  `acme-`-prefixed form p5 produces. They
  are in the literal set, so `hits=6 missing=none extra=none`; the six negatives produce no
  match under the real patterns at all (structure, boundary or length), so the set filter is
  never consulted for them.
- **K2** — the one allowlisted `ghr_` value from the round-94 receipt is readable in the same
  commit, so adding it keeps `hits=0 allowed=26 unused_allow=0`. Nothing else in the 2477-file
  clean scan is allowed to fire.
- **K4** — imports the **base** instrument's patterns, so it measures the base, never the
  candidate's generality.
- **K5** — reads `SCORECARD.md`, untouched.
- **K6** — leaves the AWS shapes generic, so the history run still reports
  `aws-sts-session-token`.
- **K1's selftest clause** — the forgery carries its own selftest and reports `cases=115` pass.

Root cause: `build_plants` randomises the plant **paths** from the run-time seed and says so
("every path is nonce-derived so a path-keyed detector cannot know it"), but the plant
**values** are module constants (`PLANT_SPEC` bodies, `GH76`, `GJ*`, `JWT_*`). A path-keyed
detector cannot know the nonce; a **value**-keyed detector does not need it. The same holds for
the single allow row and for the HISTORY_REV positive, both readable in the repo.

Routed remedy for round 96 (finding only, not applied): derive the plant values from the same
run-time seed — e.g. a random 76-character alnum body after `ghr_`, random `eyJ`-shaped
segments with the fixed prefixes — and require at least one positive whose value exists
nowhere in the repository, the gate source or the allowlist. Then a literal-keyed forgery fails
K3 on `missing`, as F1 and F8 do.

## Limb coverage notes (routed, not verdict changes)

- **K2 has two-sided power over real corpus text.** F3 shows the allow row is a canary: dropping
  the GitHub-refresh pattern leaves `allowed=24 unused_allow=1` on the clean run, before K3 is
  consulted. F5 shows the reverse: an over-broad GitLab-JWT pattern produces a false positive on
  `SentinelShapes-receipts/08-unlisted-classes.txt:75` (`20-f5-lane-hit.txt`).
- **K2 cannot see a wildcard allowlist.** F8's clean-run counters are numerically identical to
  the truth (`scanned=2477 hits=0 allowed=26 unused_allow=0`); only K3 and K6 refuse it.
- **K3's nonce names defeat path-keyed evasion, not value-keyed.** F2 and F2b are killed by K3
  exactly because the HIT set must equal `PLANT_EXPECT`; F6 shows the same limb is blind to a
  detector that knows the values.
- **K6 is the only limb that binds "read the commit, not the checkout".** F7 passes K2, K3, K4,
  K5 and dies solely on K6 (`rc=0 shapes=none`).
- **K1's pin is caller-supplied.** The gate compares the landed bytes with a digest argument; it
  cannot distinguish the frozen digest from a digest chosen to match a forgery.

## Restoration

The lane was never written. Read-only probes before/after (`00b-`, `21-`) are identical:
`lane_head=43cc15e8d807a06baf9d2dd789bb121364944169`; `wt_inst_sha256=66edd661…`;
`wt_gate_sha256=8b6f8493…`; `wt_allow_sha256=ab4e8f2c…`; `rev_inst_sha256=66edd661…`;
`rev_gate_sha256=8b6f8493…` (diff of the two probe sets: `LANE-UNCHANGED`). The lane head read
`d050e286` early in the seat and `43cc15e8` at the first integrity probe; this seat issued no
mutating git command against the lane.

The scratch clone was restored to the landing: `clone_head=38e7319f44a9fab2978b59ffd43faf207cf62b32`,
`clone_wt_inst_sha256=66edd661…` (pristine bytes), `clone_worktree_clean_files=0`. The nine
forgery commits exist only in the disposable clone (revs in `03-forgery-revs.txt`) and are
removed with the scratch at seat exit; the receipt preserves the base sha, each forgery sha and
the mutation semantics so round 96 can rebuild the survivor.

## Receipts

All under `.ufo/waves/round-95/w1/MutC2Counter-receipts/`.

| receipt | command | observed |
|---|---|---|
| `00-baseline-pinned.txt` | gate on real lane `--rev 38e7319 --seed 95000` with both pins | `CAPABILITY-CHECK-RESULT pass rc=0`; K1–K6 ok; `elapsed=31.55 s`; `rc=0` |
| `00b-lane-integrity-before.txt` | `rev-parse HEAD` + five `sha256sum` probes on the lane | head `43cc15e8…`; inst `66edd661…`; gate `8b6f8493…`; allow `ab4e8f2c…`; rev blobs identical |
| `01-forgery-build.txt` | `python3 -B build-forgeries.py` (scratch) | `rc=0`; `pristine_sha=66edd661…`; `literal_set_size=10`; nine `FORGERY … sha=…` lines |
| `02-forgery-selftests.txt` | `<forgery> --selftest` × 9 | every forgery `rc=0 :: SELFTEST-RESULT pass cases=115` |
| `03-forgery-revs.txt` | `git -C lane checkout --detach 38e7319` + one-file commit × 9, toplevel asserted each time | nine `REV <name> <rev> files=[corpus/instruments/capture-secret-scan.py]`; `restored_head=38e7319…` |
| `04-clone-pristine-pinned.txt` | gate on the unmodified clone, both pins | `pass rc=0`; limb text identical to the baseline |
| `11-…F1…-pinned/-unpinned.txt` | gate per forgery, both modes | as tabulated; unpinned `K3 FAIL hits=0 missing=6`, `K6 FAIL rc=0` |
| `12-…F2…` | as above | `K3 FAIL hits=0 missing=6`; K6 ok |
| `13-…F2b…` | as above | `K3 FAIL hits=24 missing=none`; 18 extras over 12 files |
| `14-…F3…` | as above | `K2 FAIL allowed=24 unused_allow=1`; `K3 FAIL hits=4 missing=2` |
| `15-…F4…` | as above | `K3 FAIL hits=8 extra=n1,n2` |
| `16-…F5…` | as above | `K2 FAIL hits=1`; `K3 FAIL hits=8 extra=n3,n4` |
| `17-…F6…` | as above | pinned: `K1 FAIL inst_sha=61f088a9…`, K2–K6 ok; unpinned: `CAPABILITY-CHECK-RESULT pass rc=0` |
| `18-…F7…` | as above | `K6 FAIL rc=0 shapes=none` |
| `19-…F8…` | as above | `K3 FAIL hits=0 missing=6`; `K6 FAIL rc=0` |
| `20-f5-lane-hit.txt` | forged F5 instrument `--lane lane --rev <f5>` | one `HIT shape=gitlab-jwt-token path=.ufo/waves/round-94/w1/SentinelShapes-receipts/08-unlisted-classes.txt line=75`; `allowed=26 unused_allow=0 rc=1` |
| `21-integrity-after.txt` | same probes as `00b` plus clone restoration | identical lane values; `clone_head=38e7319…`; `clone_wt_inst_sha256=66edd661…`; `clone_worktree_clean_files=0` |
| `22-target-hashes.txt` | `sha256sum` of gate/candidate/landed files + claim pins | all three equal `claims.json` |
