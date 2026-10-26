# ReviewerNoHarm — receipt (round 40, wave 1)

Seat: ReviewerNoHarm (leaf reviewer, no subagent dispatch). Item: independently reproduce the
base no-harm measurements at the claims freeze 5e985b74075dd3813a63d7750966bf8abf693465 and
compare with ExecH10NoHarmBase. No lane edits made; all commands read-only.

- Deliverable: `.ufo/waves/round-40/wave1/ReviewerNoHarm.txt` — 45 lines, 3171 bytes,
  sha256 `307ed9570afbc89fa5f67656723a346d74dfb89f009d09f2d25c1edaf9fb11a2`.
- Run window: 2026-10-26T21:14Z–21:19Z (UTC).
- Scratch: `/fast/scratch/hyaku/kasegi-r40/ReviewerNoHarm/` — removed before yield.

## 1. Preconditions verified

- Lane HEAD at run time = `5e985b74075dd3813a63d7750966bf8abf693465` (the freeze commit itself);
  `git rev-parse 5e985b7^` = `a7af2ce63bce153757d39bf66b366a96caf30c13` (freeze parent = base).
- `git status --porcelain` in the lane: only untracked `.ufo/waves/round-40/` wave-dispatch
  files; zero modifications to tracked files. Therefore the working tree is byte-identical to
  the freeze commit for every tracked path, and running the instruments in place measures the
  frozen bytes. Confirmed by sha256 (base = freeze = worktree for all four relevant files):

| file | sha256 (identical at base/freeze/worktree) |
|---|---|
| SKILL.md | `ce6689c554f2e33b6d7b79a53fde387b7f7e7140ace1ade6e9f4670548b242f4` |
| PROVINCE.md | `4d42eed1afa00ff0dafcfea235e2f48c3b607fd67cdbe1d489504f1a098a155c` |
| corpus/instruments/density.py | `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710` |
| corpus/instruments/anchorcheck.py | `d0f35f8ccdcf995b78ea1403732fa90e12708b79bda21793002f7315b0e2a912` |

- Frozen claims read first (`.ufo/waves/round-40/claims.json`); not edited. H10 limb under
  test: SKILL/PROVINCE append-only, density instrument unchanged, no deleted paths.
- Disk guard green before work: `/fast/scratch/hyaku` 26% used, 601.6G free.

## 2. Measurement 1 — density census

Command (cwd = lane repo; instrument and target read-only):
`python3 corpus/instruments/density.py SKILL.md --label SKILL` → exit 0.

Actual output (header + summary lines):

```
# Density census — SKILL (1115 lines, 27 blocks)
# ev = path-cites + concrete-tbl-rows + numerics + signatures; dens = ev*100/nb
...27 per-block rows...
| | **mean dens** | | | | | | | | **232.9** |

Total path-citation instances: 771 across 27 blocks.
```

Reproduced values: file-lines=1115, blocks=27, mean-dens=232.9, path-cite-instances=771, exit 0.

## 3. Measurement 2 — anchorcheck

Command: `python3 corpus/instruments/anchorcheck.py SKILL.md` → exit 0.

Actual summary line (first line of output):

```
== /home/vgpnk/Projects/shokunin/kasegi-shokunin/SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
```

Reproduced values: in-range=16, bad=0, distinct=16, lost-recorded=306, pin-broken=0,
origin=0, outside-base=0, base-absent=0, exit 0. All fail classes zero — fail-closed exit
rule (r28) satisfied; the 306 LOST-RECORDED cites are recorded-not-fail by design.

## 4. Measurement 3 — SKILL/PROVINCE numstat

Command:
`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --numstat a7af2ce63bce153757d39bf66b366a96caf30c13 5e985b74075dd3813a63d7750966bf8abf693465 -- SKILL.md PROVINCE.md`

Actual output: **empty**, exit 0. Zero added/removed lines in SKILL.md and PROVINCE.md
between base and freeze — both files untouched (append-only guard trivially holds at freeze).

## 5. Measurement 4 — full name-status base→freeze

Command:
`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --name-status a7af2ce63bce153757d39bf66b366a96caf30c13 5e985b74075dd3813a63d7750966bf8abf693465`

Actual output (verbatim, exit 0):

```
A	.ufo/waves/round-40/c1-controls/before.txt
A	.ufo/waves/round-40/c2-controls/before.txt
A	.ufo/waves/round-40/c2-controls/junk-decisions.md
A	.ufo/waves/round-40/census-before.txt
A	.ufo/waves/round-40/claims.json
```

Changed paths: exactly 5, all `A` (added), zero `M`/`D`/`R`. Every added path is a
`.ufo/waves/round-40/` control/claims file. Cross-check numstat per path:
11 / 10 / 20 / 5 / 71 added lines = 117 added, 0 deleted.

Corroboration: `git diff --numstat base freeze -- corpus/instruments/` is empty — the
density instrument (and anchorcheck) are unchanged between base and freeze, so the
measurements in §2–§3 were produced by the same instrument bytes the base round used.

## 6. Comparison with ExecH10NoHarmBase

Peer artifact: `.ufo/waves/round-40/wave1/ExecH10NoHarmBase.txt` (landed before my run).

| quantity | ReviewerNoHarm (this seat) | ExecH10NoHarmBase | agree |
|---|---|---|---|
| density file-lines | 1115 | 1115 | ✓ |
| density blocks | 27 | 27 | ✓ |
| density mean-dens | 232.9 | 232.9 | ✓ |
| density path-cite-instances | 771 | 771 | ✓ |
| anchorcheck in-range | 16 | 16 | ✓ |
| anchorcheck bad | 0 | 0 | ✓ |
| anchorcheck distinct | 16 | 16 | ✓ |
| anchorcheck lost-recorded | 306 | 306 | ✓ |
| anchorcheck pin-broken / origin / outside-base / base-absent | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | ✓ |
| SKILL/PROVINCE numstat lines | 0 | 0 | ✓ |
| added-files / deleted-paths | 5 / 0 | 5 / 0 | ✓ |
| added-lines total | 117 (11/10/20/5/71) | 117 (11/10/20/5/71) | ✓ |
| SKILL.md sha256 | ce6689c5…4242f4 | ce6689c5…4242f4 | ✓ |
| PROVINCE.md sha256 | 4d42eed1…98a155c | 4d42eed1…98a155c | ✓ |
| density.py sha256 | ee803726…9f54710 | ee803726…9f54710 | ✓ |
| freeze parent = base | yes | yes | ✓ |

**Result: full agreement on every reproduced value; zero differences.** Both seats used the
same four measurement commands on the same frozen bytes; my run additionally confirmed the
freeze commit is HEAD and the tracked tree is clean, so neither seat's numbers could have
drifted from the frozen state.

## 7. Verdict

The base no-harm measurements reproduce exactly and independently: at the claims freeze,
SKILL.md and PROVINCE.md are untouched, the density instrument is unchanged, no path was
deleted or modified, and the only five changes base→freeze are the round-40 control/claims
files. The H10 base limb (no-harm guard at freeze) is confirmed by two independent seats.

Residual risk / gaps: none for the base limb. This seat did not re-measure the working tree
after later wave commits (out of item scope); the H10 working-tree limb remains
ExecH10NoHarmBase's and the closer's to check at filing time.

## 8. Tooling & compliance notes

- No tools installed or upgraded (none needed); no pacman use; no host service touched.
- No mutating git/jj command anywhere; only `rev-parse`, `status`, `ls-tree`, `show`,
  `diff` (all read-only). No writes outside my receipt, my deliverable, and my scratch.
- Scratch dir `/fast/scratch/hyaku/kasegi-r40/ReviewerNoHarm/` removed before yield.
