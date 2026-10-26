# ExecAncestry — r36 commit ancestry facts and the anchor-ancestor wording

Round 37, claim C1 (`depth:verifiability`), seat ExecAncestry (leaf executor). Item: establish the r36 commit
ancestry facts that C1's E12 (D4 anchor-ancestor label) and the round report need. **Receipt only** — no lane file
was created or edited by this seat.

Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, read at `HEAD` = `b362068195d5489aa94b31e6ec8f880c367e0ba0`
(`master` = `origin/master` = that hash at read time). Every command below is read-only
(`log`/`rev-parse`/`cat-file`/`rev-list`/`merge-base`/`diff`/`show`/`grep`); no mutating git command was run.

## Verdict

| question | answer | proof |
|---|---|---|
| r36 **lane final head** | `c20300df516eb5575d8db2aaad1f0cf4913e7981` — author `kasegi-shokunin`, 2026-10-26 13:41:37 -0300; it is the branch tip at closure and the last lane-authored commit of the round | spot-check §header states "Branch tip at closure: `c20300df…`"; its `state` row reads `branch=master local=c20300df… remote=c20300df… ahead=0 behind=0` |
| r36 **judged head** | `a23dc4788aa7c98831eed6db953434034ce5ae8d` (= `A`), 13:00:31; one commit below the lane head | spot-check §header: "judged head `a23dc478…` (A)" |
| **is `e666d902` the lane final head?** | **No — intermediate ancestor.** 5 commits below `c20300df`, 4 below `a23dc478`; direct *parent* of `2c26a97e`, the commit that wrote the `Final lane commit: e666d902…` line | `merge-base --is-ancestor` both directions; `rev-list --count`; `-S` pickaxe |
| r36 **base** (`B`) | `cc692008b0cfd58d18275aa6c4aed79620120799` (round-30 salvage commit; last commit before r36 work) | spot-check §header: "lane base `cc692008…` (B)" |
| **integrator spot-check** vs lane | `b56a4168` is **not** a lane commit: author/committer `protocol-shokunin`, +164 lines in exactly one file (`corpus/lessons/round-36-verifier-spotcheck.md`), landed after the lane head; it is the **r37 base** | `git show --stat b56a416`; parent of `224df74` |

## Chain (linear — `git rev-list --merges cc692008..b362068` → `0`)

Parent map, verified with `git rev-list --parents -n1 <commit>`:

```
cc692008 -> b47f2cdf -> caa31462 -> e666d902 -> 2c26a97e -> e9c57c43 -> 274fa9ae -> a23dc478 -> c20300df
                                                                                                   |
                                                                    b56a4168 (protocol-shokunin) --+
                                                                       |
                                                            224df74d -> f3246559 -> b3620681
```

| commit | author | author time | committer time | role |
|---|---|---|---|---|
| `cc692008b0cfd58d18275aa6c4aed79620120799` | kasegi-shokunin | 2026-10-26 09:05:45 -0300 | 09:05:46 | **r36 base (B)**; round-30 orchestrator salvage (pre-round) |
| `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` | kasegi-shokunin | 12:33:20 | 12:33:20 | **r36 claims-freeze** + before controls |
| `caa314625ad7991e8104de32402f381854f7e100` | kasegi-shokunin | 12:55:32 | 12:55:32 | r36 integration (r36 suite, F19/S053, drafts) |
| `e666d902337a49dcbfc77880939874f39c6f477b` | kasegi-shokunin | 12:57:10 | 12:57:10 | r36 **wave evidence** (spec/dispatch/ready, receipts 60/64) — **intermediate ancestor**, mislabelled "final lane commit" |
| `2c26a97ec3897a7c9885e6a8c62d356f37aa42f8` | kasegi-shokunin | 12:57:49 | 12:57:49 | r36 "E1 Final lane commit line, E4 provenance note, lesson hash" — **the commit that wrote the false label** |
| `e9c57c43729a354d7d027d467228028b439b7402` | kasegi-shokunin | 12:57:49 | 12:59:15 | r36 late seat receipt updates |
| `274fa9ae908db5800013778098f4d426281b46e2` | kasegi-shokunin | 12:59:56 | 12:59:56 | r36 late receipt updates (Gate/Simpl); named "final lane head" in `SCORECARD.md:1494` — same stale-label class |
| `a23dc4788aa7c98831eed6db953434034ce5ae8d` | kasegi-shokunin | 13:00:31 | 13:00:31 | **r36 judged head (A)** — final gate receipts + measured closure |
| `c20300df516eb5575d8db2aaad1f0cf4913e7981` | kasegi-shokunin | 13:41:37 | 13:42:03 | **r36 LANE FINAL HEAD** — WAVE-DONE integration, results 64/64, late receipts 64/64 |
| `b56a41680cefd391868c1c370dc063c69d827e7d` | **protocol-shokunin** | 13:47:37 | 13:47:37 | **r36 integrator spot-check** (non-author, hyaku), +1 file/164 lines; **r37 base** |
| `224df74db2a46d627ae1475a72ca48796bbd177c` | kasegi-shokunin | 13:47:37 | 13:57:07 | **r37 claims-freeze** + before controls |
| `f3246559bed2fd085dde860e00247ce394f02bad` | kasegi-shokunin | 13:59:17 | 13:59:17 | r37 wave evidence (spec/plan/dispatch, 64 seats v2) |
| `b362068195d5489aa94b31e6ec8f880c367e0ba0` | kasegi-shokunin | 14:00:19 | 14:00:19 | r37 claims-erratum-1 (tip at read) |

## Ancestry proof (exact outputs)

```
$ git merge-base --is-ancestor <a> <b>            # exit 0 = ancestor
cc692008 ancestor-of b47f2cdf -> exit=0
b47f2cdf ancestor-of e666d902 -> exit=0
e666d902 ancestor-of a23dc478 -> exit=0
a23dc478 ancestor-of c20300df -> exit=0
c20300df ancestor-of b56a4168 -> exit=0
b56a4168 ancestor-of b3620681 -> exit=0
e666d902 ancestor-of c20300df -> exit=0
e666d902 ancestor-of b56a4168 -> exit=0

# strictness: the lane head is NOT behind the anchor
c20300df ancestor-of e666d902 -> exit=1   (and `rev-list --count c20300df..e666d902` = 0)

$ git rev-list --count <a>..<b>
count(e666d902..c20300df) = 5      # 2c26a97e, e9c57c43, 274fa9ae, a23dc478, c20300df
count(a23dc478..c20300df) = 1
count(e666d902..a23dc478) = 4
count(c20300df..b56a4168) = 1

$ git rev-list --merges cc692008..b3620681 | wc -l   -> 0      # linear, no merge topology tricks
$ git rev-parse --verify --quiet <prefix>^{commit}   -> resolves uniquely for c20300df, e666d902, a23dc478, b56a416, 224df74
$ git log --format='%h %an %s' c20300df..b3620681    -> b56a416 (protocol-shokunin), 224df74, f324655, b362068 (r37 lane)
$ git diff --name-only a23dc478 c20300df | grep -vc '^\.ufo/waves/round-36/'  -> 0   # judged head and lane head differ only in wave evidence
```

No commit after `c20300df` inside r36 is lane-authored: the next commit is the `protocol-shokunin` spot-check, then the
r37 claims-freeze. So `c20300df` is the r36 lane final head by authorship, by topology, and by the spot-check's own
`state` reading (`local=c20300df… remote=c20300df… ahead=0`).

## How the false label arose (provenance, pickaxe)

```
$ git log --format='%h %ci %s' -S 'Final lane commit: e666d902' -- SCORECARD.md
2c26a97 2026-10-26 12:57:49 -0300 round-36: E1 Final lane commit line, E4 provenance note, lesson hash
$ git log --format='%h %ci %s' -S 'final lane commit `e666d902' -- corpus/lessons/round-36.md
2c26a97 2026-10-26 12:57:49 -0300 round-36: E1 Final lane commit line, E4 provenance note, lesson hash
$ git rev-list --parents -n1 2c26a97
2c26a97ec3897a7c9885e6a8c62d356f37aa42f8 e666d902337a49dcbfc77880939874f39c6f477b
```

The label was filled at `2c26a97e` with **its own parent**. A closing commit must be a descendant of the commit that
writes the line (here `2c26a97e` itself, then `e9c57c43`, `274fa9ae`, `a23dc478`, `c20300df`), so the label was
structurally impossible to be true at write time. Both sites still carry it at the r37 base:

- `corpus/lessons/round-36.md:3` — "final lane commit `e666d902337a49dcbfc77880939874f39c6f477b` (filled at closure)"
- `SCORECARD.md:1492` — `Final lane commit: e666d902337a49dcbfc77880939874f39c6f477b`
- second, same-class label: `SCORECARD.md:1494` — "Measured at the final lane head `274fa9ae908db5800013778098f4d426281b46e2`"

Routed defect D4 (`corpus/lessons/round-36-verifier-spotcheck.md:154-156`) names exactly this: "`corpus/lessons/round-36.md:3`
and `SCORECARD.md`'s `Final lane commit: e666d902…` name an intermediate ancestor, not the round's final head
(`a23dc478`, then `c20300df`). Label it as the anchor ancestor."

## Why E12's label is the only check that can catch this (measured, not inferred)

The committed r36 suite binds hashes by **ancestry only** (`corpus/instruments/r36-closure.sh:54-59`, `e1_final_hashes`
at 254-275): inside the last `Round[- ]36` block, every 40-hex on a `[Ff]inal lane commit` line or the four lines after
it must `cat-file -e` and be **an ancestor of the export ref**. An intermediate ancestor satisfies that by construction.
Reproducing the committed function on today's `SCORECARD.md`:

```
1492: e666d902337a49dcbfc77880939874f39c6f477b
1494: 274fa9ae908db5800013778098f4d426281b46e2
```

Both are bound (`bound == total`) — which is exactly why the false label survived E1 in round 36. Two consequences for
round 37's E12/E1 split:

1. E12's `anchor ancestor` label is load-bearing; an ancestry-only E1 can never distinguish anchor from final.
2. Any 40-hex within 4 lines after a `Final lane commit` line in the round-37 block enters E1's binding set. All lane
   hashes above are ancestors of any r37 head (`merge-base --is-ancestor <h> <r37 head>` → 0; a commit is its own
   ancestor, verified exit 0 on `b362068..b362068`), but a **non-lane** 40-hex there (e.g. a fleet-repo commit) fails
   `cat-file -e` in `$LANE`. A 64-hex sha256 is safe: the split is on non-hex runs, so it is never read as 40-hex.

State at read: `grep -c "Round 37" SCORECARD.md` → `0`; running the same block-scanner with `Round[- ]?37` prints
`start=0` (1494 lines). So the round-37 E1-analog is red (`total=0` → `closed<14/14`) until the section lands at closure.

## Exact recommended wording

**A. `corpus/lessons/round-37.md` line 3 (mirrors the r36 shape; `anchor ancestor` and the hash on the same line):**

```
Lane: `kasegi-shokunin`. Base `b56a41680cefd391868c1c370dc063c69d827e7d` (round-36 integrator spot-check, author `protocol-shokunin`, 2026-10-26 13:47:37 -0300); claims-freeze `224df74db2a46d627ae1475a72ca48796bbd177c`; anchor ancestor: `c20300df516eb5575d8db2aaad1f0cf4913e7981` (round-36 LANE head, author `kasegi-shokunin`, 2026-10-26 13:41:37 -0300); final lane commit `<r37 head>` (filled at closure).
```

**B. `SCORECARD.md` `## Round 37 …` section (append at EOF; carries the round-37 `Final lane commit:` line the E1-analog needs):**

```
**Measured commits.** before = claims-freeze `224df74db2a46d627ae1475a72ca48796bbd177c`; after = `Final lane commit: <r37 head>` (filled at closure).
anchor ancestor: `c20300df516eb5575d8db2aaad1f0cf4913e7981` — the round-36 LANE head (author `kasegi-shokunin`, 2026-10-26 13:41:37 -0300), one commit below this round's base `b56a4168`.
```

Optional correction sentence, only if wanted inside the round-37 section (keeps the stale compound out):

```
The round-36 closing label named `e666d902337a49dcbfc77880939874f39c6f477b`, an intermediate ancestor five commits below the lane head — not a closing commit.
```

**C. `## Mistakes` M37-3 evidence cell** (the row already exists in the item spec; this is the falsifiable evidence to
fill into it):

```
`git merge-base --is-ancestor e666d902 c20300df` -> 0 and the reverse -> 1; `git rev-list --count e666d902..c20300df` -> 5; label introduced at `2c26a97e`, whose parent is `e666d902`.
```

**Hard constraints on the wording** (each is a false-red if violated):

- Never write the literal `Final lane commit: e666d902` anywhere inside the round-37 SCORECARD section — not even in a
  correction sentence. Refer to it as "the round-36 closing label named `e666d902…`". The base file already carries that
  literal at `SCORECARD.md:1492` inside the **round-36** block; E12's stale-label clause is satisfiable only when scoped.
- Do not quote M37-3's row text into the SCORECARD section (it contains "final lane commit" + `e666d902` on one line);
  reference it by id.
- Leave no placeholder token: `<r37 head>` above, `<LANE_HASH>`, or `filled by the L1` must all be replaced/absent at the
  final export (r36's E1 greps the latter two).
- The round-37 block must be the last `Round[- ]37` heading block, and `Final lane commit:` there must name the actual
  r37 head at closure; E1-analog needs `total >= 1` bound hash.

## Files changed

This receipt only: `.ufo/waves/round-37/wave1/ExecAncestry.md`. No lane file, no fleet file, no sibling repo.

## Risks / open items for the L1

1. **E12 scoping is mandatory.** If the E12 stale-label grep is not scoped to the round-37 block (delimiter
   `awk '/^#{1,4} .*Round[- ]?37/'`), it will match `SCORECARD.md:1492` in the round-36 block and the check becomes
   permanently red on every export — including the final lane head. Recommended predicate: count `Final lane commit:
   e666d902` and `anchor ancestor` only between the last `Round[- ]37` heading and EOF.
2. **Two stale labels, one routed.** `SCORECARD.md:1494` names `274fa9ae` "the final lane head" (same class as D4, not
   routed by the spot-check). Round 37 should not repeat it; correcting the r36 block is optional and outside E12's scope.
3. **E1 cannot see label drift.** Keeping r36 semantics (ancestry-only) is per the frozen claim; requiring the
   `Final lane commit:` hash to *equal* the export ref would be a stronger check but is a claim change — not done here.
4. **Scratch observation (E9's domain, not mine):** 18 seat dirs existed under `/fast/scratch/hyaku/kasegi-r37` at read
   time; they must all be gone at closure. This seat's own dir was created empty and removed at yield.

## Tooling

No installs, no upgrades (pacman untouched — host-wide pause respected); read-only git and coreutils only.

## Scratch

`/fast/scratch/hyaku/kasegi-r37/ExecAncestry` — created with `mkdir -p`, held no files, removed at yield
(`rm -rf`); absence verified.
