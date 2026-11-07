# CriticClaimsC1 — round-99 C1 attack report

Seat: `CriticClaimsC1` (critic, read-only attacker). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `b9411a6b530e486180cf14c72fccc46668dcf5ee`, freeze `6195db307c1cb101eba1d268f8cbfc1578d2caf7`, C2 landing
`a3db47e71fe292c03b00ba11f38cccbec45d3966`, C1 landing `35e3ab6041ff8690b00d831f27b93d08101fd16a`.
Scratch `S=/fast/scratch/hyaku/kasegi-r99/CriticClaimsC1`. No tools installed; no subagent dispatched.
Receipts: `.ufo/waves/round-99/w1/CriticClaimsC1-receipts/`.

Instrument under attack: `corpus/instruments/census-at-rev.py`, sha256
`6d68d9555b9be5a75bfefb27ee8cf531bc97dd540c954cc2da56581e6a68f041` (verified as the C1 landing blob:
`git show 35e3ab6:corpus/instruments/census-at-rev.py | sha256sum` → `6d68d955…`; same as the worktree file).
Counter: `.ufo/waves/round-99/c1/tamper.py`, sha256 `1d0810a2a7a9b5179fba482df782f1ee98547d3a638b6b2ca09925dfbb5be220`.
Census of record (committed blob): sha256 `211818db7ed71ae2eebfe7fa02890faab7302915c66fc9929be9a44e984859e3`.

## P1 — the 12-class tamper harness

Command (at the landing; the worktree instrument is byte-identical to the landing blob):

```
python3 -B .ufo/waves/round-99/c1/tamper.py --lane . \
  --rev a3db47e71fe292c03b00ba11f38cccbec45d3966 \
  --alt-rev b9411a6b530e486180cf14c72fccc46668dcf5ee \
  --instrument corpus/instruments/census-at-rev.py --work $S/R1/w
```

(The run used `--lane /home/vgpnk/Projects/shokunin/kasegi-shokunin`; `.` from the lane root is equivalent.)

Observed (full output in `-receipts/p1-tamper-candidate.txt`):

```
TAMPER T01-pinned-edited        rc=1 PASS reason=header-sha-mismatch
TAMPER T02-measured-at-repointed rc=1 PASS reason=header-sha-mismatch
TAMPER T03-measured-at-short    rc=1 PASS reason=no-measured-at
TAMPER T04-measured-at-missing  rc=1 PASS reason=no-measured-at
TAMPER T05-body-edited          rc=1 PASS reason=body-sha-mismatch
TAMPER T06-host-line-removed    rc=1 PASS reason=no-host-inclusive
TAMPER T07-host-line-edited     rc=1 PASS reason=header-sha-mismatch
TAMPER T08-body-from-other-rev  rc=1 PASS reason=body-sha-mismatch
TAMPER T09-poisoned-cache       rc=1 PASS reason=pinned-mismatch
TAMPER T10-pinned-from-host     rc=1 PASS reason=header-sha-mismatch
TAMPER T11-host-owned-edited    rc=1 PASS reason=header-sha-mismatch
TAMPER T12-body-truncated       rc=1 PASS reason=body-sha-mismatch
TAMPER-RESULT killed=12 total=12 evaluated=12 instrument_sha256=6d68d9555b9be5a75bfefb27ee8cf531bc97dd540c954cc2da56581e6a68f041 rc=0
```

Base instrument (`git show e2d3de7b847f8e9bac72a5bc4dea455ea051cf1a:corpus/instruments/census-at-rev.py`,
sha256 `66383371211bf4b801df608d5e20c23e2b51457717fcb1b76de471b8feb62502`; `-receipts/p1-tamper-base.txt`):

```
TAMPER T01..T04, T10 killed; T05 T06 T07 T08 T09 T11 T12 accepted (rc=0)
TAMPER-RESULT killed=5 total=12 evaluated=12 instrument_sha256=66383371211bf4b801df608d5e20c23e2b51457717fcb1b76de471b8feb62502 rc=0
```

**P1 STANDS.** 12/12 at the landing, 5/12 on the round-98 instrument, exact shas as pinned. The five classes the
round-98 instrument already rejected (T01–T04, T10) are still rejected; no regression.

## P2 — layout equality

Committed census checked in a clean work dir (`-receipts/p2-layouts.txt`):

```
CENSUS-CHECK pass rev=a3db47e71fe292c03b00ba11f38cccbec45d3966 skill=162/732 corpus=2569/7624 lane=2607/8026 host_owned=76 confined=1
rc=0
```

Same census with `MISSION.md` and `.ufo/waves/shokunin12h-20261014-p1-repair/members/KasegiGateRepair.md`
in the **work dir** (the round-98 scratch parent), `--work $S/R2/dirtywork`:

```
CENSUS-CHECK pass rev=a3db47e71fe292c03b00ba11f38cccbec45d3966 skill=162/732 corpus=2569/7624 lane=2607/8026 host_owned=76 confined=1
rc=0
```

Same files placed in the **extract's private parent** `<work>/extract-a3db47e71fe2/`, `--work $S/R2/dirtyparent`:

```
CENSUS-CHECK fail reason=body-mismatch rc=1
--rev in the same layout: CENSUS rev=a3db47e… skill=162/732 corpus=2569/7624 lane=2607/8026 host_owned=76 confined=3
```

Two `../` citations (`../MISSION.md:49-56`, `../.ufo/waves/…/members/Kasegi*.md`) move GONE→INTERNAL in
resolve.py's raw output; the instrument reclassifies both as HOST-OWNED (`confined=3`), so the **pinned triple stays
2607/8026**, but the **body** changes (GONE 5342→5340, INTERNAL 2608→2610) and `--check` fails `body-mismatch`.
The statement's "one whose parent carries `MISSION.md` and `.ufo/…/KasegiGateRepair.md`" is therefore true only if
"parent" means the work dir / work parent; the natural reading in the round-98 context (the extract's parent) does
not pass. The docstring's "the body is layout-stable" (lines 8–10) is an overclaim for that layout.

**P2 STANDS for the control's layout** (clean and dirty work-dir both pass with the identical triple). The
extract-parent reading is a wording/limitation finding, not a P2 failure under the recorded control.

## P3 — measured-at ancestor, no scratch paths

```
git merge-base --is-ancestor a3db47e71fe292c03b00ba11f38cccbec45d3966 HEAD   → ancestor rc=0
grep -c 'fast/scratch' committed-census.md                                   → 0 (grep rc=1)
grep -c 'tree-a3db47e71fe2' committed-census.md                              → 0 (grep rc=1)
```

`-receipts/p3-p4.txt`. **P3 STANDS.**

## P4 — time and peak RSS

`/usr/bin/time -v … --check committed-census.md --work <fresh>`:

```
CENSUS-CHECK pass rev=a3db47e… skill=162/732 corpus=2569/7624 lane=2607/8026 host_owned=76 confined=1
Elapsed (wall clock) time: 0:08.99      Maximum resident set size: 514764 kbytes
```

Earlier runs on the same command: 3.79 s / 513492 KB; the P2 clean run: 2.23 s / 512980 KB (control receipt).
Wall time varies with host load; the predicate is <60 s and <1 GiB. **P4 STANDS.**

## Statement limbs verified outside P1–P4

- **Confinement.** The tsv has 2608 INTERNAL rows; the pinned numerator is 2607. The reclassified row is
  `citation='../'`, `resolved='<extract>/../'` → `realpath` is the extract's parent, outside the extract →
  HOST-OWNED, denominator unchanged (8026). A second `..` row
  (`corpus/instruments/../instruments/capture-binding-check.py`) resolves *inside* the extract and stays INTERNAL.
  Code: `walkout()` at `census-at-rev.py:103`, reclassification at `:152`. `confined=1` is printed by
  `--write`/`--check` but is **not recorded in the census** (the body still says INTERNAL 2608; see residual 6).
- **Confined HOME.** `measure()` sets `env["HOME"] = home_dir(work)` (`:124`); resolve.py uses
  `os.path.expanduser` (`resolve.py:124,130,189`), so the mirror root is
  `<confined-home>/Projects/the-bounty-hunter` (ABSENT) and the host-inclusive line is 165/732, 2645/7624, 2683/8026.
  The host itself has no `~/Projects/the-bounty-hunter` (`ls` rc=2), so the mirror absence is not solely the
  confinement's doing; the confinement is what prevents `~/Projects/**` globs.
- **Digests.** Header-sha over the five lines, body-sha over the body; `--check` compares both, then re-measures
  and compares the body (`:337`), pinned (`:326`), host (`:331`), host-owned (`:334`).
- **Cache bypass.** Poisoning `<work>/cache/<rev>-<inst12>.json` and re-checking the committed census still
  prints `CENSUS-CHECK pass` (`-receipts/statement-cache-bypass.txt`). T09 confirms the reverse direction.
- **measured-at.** Regex requires exactly 40 hex (`:289`); ancestor check at `:239`; a non-ancestor dangling commit
  in a fixture clone gives `CENSUS-CHECK fail reason=measured-at-not-ancestor rc=1`.
- **`--write` refusal.** Fixture clone (`git clone --shared`, `rev-parse --show-toplevel` asserted = fixture dir):
  `CENSUS-WRITE error reason=rev-not-ancestor rc=2` for a dangling commit; `bad-revision rc=2` for a short rev
  (`-receipts/statement-not-ancestor.txt`).

## Attacks the twelve classes do not cover

### (a) Body permutation — STANDS

Swap two body table rows; leave `body-sha256` → `CENSUS-CHECK fail reason=body-sha-mismatch rc=1`. Recompute
`body-sha256` over the permutation → `CENSUS-CHECK fail reason=body-mismatch rc=1`. The digest is over the whole
body and the check also compares the body to the freshly measured body, so a permutation is killed twice
(`-receipts/attack-a-permutation.txt`).

### (b) measured-at ancestor whose rates coincide — STANDS

Repoint `measured-at` a3db47e→b9411a6b (rates differ), recompute header-sha → `pinned-mismatch` with both lines
printed. Repoint 29cd305→35e3ab6, whose bodies differ **only** in the `Lane root: … (measured from the git-archive
extract of <rev>)` line, recompute header-sha → `body-mismatch` (the Lane root line is the binding). A census that
coincides with another revision's rates is still a correct reading of the named revision, and the check re-measures
it (`-receipts/attack-b-ancestor.txt`).

### (c) Two `--write`s at different revisions into one path, warm cache — STANDS

Write a3db47e then b9411a6b into the same path with the same work dir: the cache key is `rev + "-" + inst12`, so
the second write measures b9411a6b and the file carries `measured-at: b9411a6b…` and 2607/8022; `--check` passes.
Poisoning the cache for a3db47e and then `--write --rev a3db47e` emits a census with `SKILL 1/2 …`; `--check`
rejects it `pinned-mismatch` (fail-closed). No wrong census is accepted by the warm cache
(`-receipts/attack-c-double-write.txt`).

### (d) Symlinked extract parent — parent STANDS, tree DOES-NOT-STAND

- **Parent symlink** `<work>/extract-a3db47e71fe2 → <scratch target>`: the write extracts the rev's tree under the
  target, body has no scratch paths, `--check` passes and a **fresh** work-dir check also passes with the correct
  2607/8026 (`-receipts/attack-d-symlink-and-extract.txt`). Harmless.
- **Tree symlink** `<work>/extract-a3db47e71fe2/tree → <scratch copy of the b9411a6b tree>`:
  `CENSUS-WRITE ok rev=a3db47e… skill=162/732 lane=2607/8022` — the census claims a3db47e but carries the other
  tree's rates; `--check` with the same work dir prints `CENSUS-CHECK pass … lane=2607/8022 rc=0`; a fresh work-dir
  check prints `pinned-mismatch rc=1`. The target's `corpus/instruments/citation-survival.md` is rewritten by
  resolve.py (`Lane root: …/RD/w/extract-a3db47e71fe2/tree`), i.e. `--write`/`--check` are **not read-only** with
  respect to the extract path. **DOES-NOT-STAND** for the tree variant.

### (e) Pre-seeded extract, no symlink — DOES-NOT-STAND

Seed `<work>/extract-a3db47e71fe2/tree` from `git archive b9411a6b`, then `--write --rev a3db47e…`:

```
CENSUS-WRITE ok rev=a3db47e71fe292c03b00ba11f38cccbec45d3966 skill=162/732 lane=2607/8022 host_owned=76 confined=1
measured-at: a3db47e71fe292c03b00ba11f38cccbec45d3966
pinned rate … lane 2607/8022 = 32.50%
--check (same work dir): CENSUS-CHECK pass … lane=2607/8022 rc=0
--check (fresh work dir): CENSUS-CHECK fail reason=pinned-mismatch rc=1
```

`extract()` early-returns when `<work>/extract-<rev12>/tree/corpus/instruments/resolve.py` exists (`:79`) and never
verifies the tree against the revision. This is the same shape as T09 (poisoned cache) but one level lower: the
check bypasses the cache (`cache_ok=False`) yet reuses the extract. **DOES-NOT-STAND**: a wrong census is accepted
when the census is generated in the poisoned work dir and checked there. A fresh work dir rejects it, so the
guarantee is "a census generated in a pristine work dir is verifiable", not "a census is a reading of the named
revision".

### (f) `home:` line rewritten — DOES-NOT-STAND (false provenance accepted)

Rewrite `home: confined (empty Projects tree; no host roots)` to
`home: real (host roots; the host Projects tree was globbed)` and recompute `header-sha256`; body untouched:

```
CENSUS-CHECK pass rev=a3db47e… skill=162/732 corpus=2569/7624 lane=2607/8026 host_owned=76 confined=1
rc=0
```

`check()` binds `hdr[1]` (the `home:` line) only through the header digest and never compares it to `HOME_LINE`
(the comparisons are `hdr[2]`, `hdr[3]`, `hdr[4]`, `:326/:331/:334`). The numbers are still the confined numbers, so
this is a provenance lie rather than a numeric one, but the record can claim a measurement mode the check never
used (`-receipts/finding-home-line.txt`).

### (g) `--home real` is advertised but does not exist — doc defect

Docstring line 17: "`--home real` restores the host reading for an ad-hoc host-inclusive number". argparse defines
only `--lane --rev --work --write --check`; the flag is rejected:

```
census-at-rev.py: error: unrecognized arguments: --home real   rc=2
```

### (h) Latent: confinement is syntactic (`..` only)

The reclassification fires only for `klass == "INTERNAL" and walkout(cit)` (`:152`). A citation with no `..` that
resolves outside the extract stays INTERNAL. The tree contains 58 committed symlinks, **6 of them absolute**
(`.ufo/waves/round-25/assimilation/rows/validate/corpus/knowledge`, the three round-28 `schema{2,3,4}` copies, and
two round-29 `CritC2Kill-scratch` links → the live lane's `corpus/knowledge` / `corpus/instruments`); `tar.extractall(..., filter="fully_trusted")` preserves them. At this
revision no citation goes through them: of 77 rows resolving outside the extract, 76 have no `..` and are all
`RESOLVES` (already out of the pinned numerator), and the one `..` row is the confined `../`. So the hole is latent,
not exercised — but a future citation through one of those symlinks would be an INTERNAL row reading the live lane,
and the instrument's comment ("a committed absolute symlink under .ufo/ … is outside the resolver's scope") is an
assumption, not an enforcement.

### (i) Residual: the record does not name the confined count

The body says `INTERNAL | 2608`, the pinned numerator is 2607; the one-row gap is the confined `../` row. The
census of record never states `confined: 1` (only the `--write`/`--check` stdout does). A reader cannot reconcile
2608 vs 2607 from the record alone.

## Incident disclosure (my write, restored)

The (d) tree-symlink test was first run with `tree → /home/vgpnk/Projects/shokunin/kasegi-shokunin` (the lane
itself). `measure()` runs `resolve.py` with `root = d`, and resolve.py writes `<root>/corpus/instruments/
citation-survival.md` and `.tsv`; the lane's census and tsv were therefore overwritten at 19:27:37 (worktree census
then had `Lane root: /fast/scratch/…/D2/w/extract-a3db47e71fe2/tree`, `337 files`, `8041` citations; `git status`
showed `M` for both). I restored both tracked files from HEAD at 19:30/19:31 with
`git show HEAD:corpus/instruments/citation-survival.{md,tsv} > <lane>/…`; current shas are
`211818db…` (md) and `0099820f…` (tsv), both equal to `git show HEAD:…`, and
`git status --porcelain corpus/instruments/` is empty (`-receipts/incident-clobber-restore.txt`). Peers
`ExecC1Indep-13` and `CriticHarm-13` flagged the dirty tree; both were answered. The (d)/(e) receipts were re-run
against scratch copies only. This is itself evidence for the finding: an unverified `tree` path is a write
primitive against its target, and `--check` is not read-only.

## Impacted axes

- **depth:verifiability (C1).** P1–P4 hold as written. The tamper-evidence is incomplete: two uncovered classes
  (poisoned extract / symlinked tree; `home:` provenance line) are accepted, and the body is layout-stable only if
  the extract's private parent is not contaminated. The 12/12 score is real but is not evidence of completeness.
- **coverage (C2).** Not in this seat's scope; no observation.

## Smallest safe corrections

1. `extract()` (`:74-101`): reject a `tree` that is a symlink or whose `realpath` is not under `realpath(work)`;
   when `cache_ok=False` (i.e. `--check`), always re-extract instead of reusing. This closes (d)-tree and (e) with
   a few lines and no format change.
2. `check()`: compare `hdr[1]` to `HOME_LINE` (`home-mismatch`), and add the confined count to the record (a sixth
   header line or a body note) so 2608 vs 2607 is explained.
3. Remove the `--home real` sentence from the docstring, or implement the flag (if implemented, the census must
   record the mode and `check` must reject a mismatch).
4. Add T13 (poisoned extract) and T14 (home-line rewrite) to the harness; optionally reclassify by resolved path
   rather than `..` syntax to close (h).
5. Keep `--check` from writing the cache (`:200-202` writes even when `cache_ok=False`), or document that it needs a
   writable work dir; a read-only work dir currently yields `resolve-rc1 rc=2`.

## Verdict

VERDICT: P1 STANDS — `killed=12 total=12 evaluated=12 instrument_sha256=6d68d955…` at the landing and `killed=5 total=12 instrument_sha256=66383371…` on the round-98 instrument, both reproduced.
VERDICT: P2 STANDS — clean and dirty work-dir layouts both print `CENSUS-CHECK pass` with the identical 162/732, 2569/7624, 2607/8026 triple; the extract-parent reading of "dirty parent" fails `body-mismatch` (pinned triple stable), so the statement's wording is ambiguous but the recorded control is reproduced.
VERDICT: P3 STANDS — `merge-base --is-ancestor` rc=0, `grep -c 'fast/scratch'` = 0, `grep -c 'tree-<rev12>'` = 0.
VERDICT: P4 STANDS — 8.99 s / 514764 KB (also 3.79 s / 513492 KB), under 60 s and 1 GiB.
VERDICT: (a) body permutation STANDS — killed by `body-sha-mismatch` and, with the digest recomputed, by `body-mismatch`.
VERDICT: (b) ancestor with coinciding rates STANDS — `pinned-mismatch` when rates differ; `body-mismatch` when only the Lane root line differs.
VERDICT: (c) double `--write` with a warm cache STANDS — the second write is correct; a poisoned-cache write is rejected `pinned-mismatch`.
VERDICT: (d) symlinked extract parent STANDS for the parent alone (pass, fresh check pass); DOES-NOT-STAND for a symlinked extract tree (check accepts a wrong census and resolve.py writes through the target).
VERDICT: (e) pre-seeded extract DOES-NOT-STAND — `--check` accepts a census measured from another revision when the work dir is reused.
VERDICT: (f) `home:` line rewrite DOES-NOT-STAND — `--check` accepts a false provenance line when `header-sha256` is recomputed.
VERDICT: C1 overall — the frozen kill rule is not triggered (P1–P4 hold; no round-98-rejected class regressed), but the "tamper-evident" goal is incomplete by two uncovered classes; the extract-reuse hole is a fixable defect (correction 1), not a tradeoff that requires rejecting the claim.
