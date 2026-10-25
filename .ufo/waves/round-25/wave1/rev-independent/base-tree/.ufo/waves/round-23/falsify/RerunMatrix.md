# RerunMatrix — C1 mirror-containment matrix: replay determinism vs committed receipt

Seat: `L1Kasegi23.RerunMatrix-2` (falsify wave, round 23). Read-only on the repo.
Scratch: `/tmp/kasegi-r23-falsify-RerunMatrix/`. No repo file, index, lane, or sibling lane was written.
No install, no update this run.

## Assignment executed

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  && python3 corpus/instruments/mirror-containment-check.py \
       --json /tmp/kasegi-r23-falsify-RerunMatrix/runA.json      # exit 0
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  && python3 corpus/instruments/mirror-containment-check.py \
       --json /tmp/kasegi-r23-falsify-RerunMatrix/runB.json      # exit 0
```
Plus three extra identical passes (`run_extra1..3.json`, all exit 0) to widen the determinism sample.

Input bytes at run time (mine, independently hashed):

| file | sha256 |
|---|---|
| `corpus/instruments/resolve.py` | `ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9` |
| `corpus/instruments/mirror-containment-fixtures.json` | `5e61a33ed5fa530547aff197fad9380d86d5850374bbb4f2a8f99df44b5e76a9` |
| `corpus/instruments/mirror-containment-check.py` | `1bc2db10dfbc59ef863e68afce475cd1d317da517137922804d7fc09cd46cecb` |
| `.ufo/waves/round-23/c1-fixed.json` (committed) | `550a863b9c3c167e1b0015825f8c1aa92a385fded751c19cd40a9ac00657b777` |

## Agreement with the committed receipt

All five of my receipts report, identically and identically to `c1-fixed.json`:

```
cases=13 escape=6 controls=7 pass=13 fail=0
resolver_sha256=ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9
matrix_sha256=5e61a33ed5fa530547aff197fad9380d86d5850374bbb4f2a8f99df44b5e76a9
```

Field-level comparison (A, B, committed; every case, every key except `cli_stdout`):

```
non-cli_stdout field diffs across A/B/committed: []
```

Case-by-case class, from my run A (equals B, extra1-3, and the committed receipt):

| id | nature | expect | actual | status | rows | cli_exit |
|---|---|---|---|---|---|---|
| bounty-parent-traversal | escape | GONE | GONE | PASS | 1 | 0 |
| bounty-parent-traversal-vault | escape | GONE | GONE | PASS | 1 | 0 |
| relative-mirror-fallback-escape | escape | GONE | GONE | PASS | 1 | 0 |
| bounty-fallback-symlink-escape | escape | GONE | GONE | PASS | 1 | 0 |
| relative-fallback-symlink-escape | escape | GONE | GONE | PASS | 1 | 0 |
| bounty-prefix-sibling-confusion | escape | GONE | GONE | PASS | 1 | 0 |
| confined-bounty-fallback-control | control | MIRROR-EQUIVALENT | MIRROR-EQUIVALENT | PASS | 1 | 0 |
| confined-relative-fallback-control | control | MIRROR-EQUIVALENT | MIRROR-EQUIVALENT | PASS | 1 | 0 |
| missing-bounty-target-control | control | GONE | GONE | PASS | 1 | 0 |
| lane-relative-parent-internal-control | control | INTERNAL | INTERNAL | PASS | 1 | 0 |
| literal-prefix-sibling-control | control | RESOLVES | RESOLVES | PASS | 1 | 0 |
| canonical-alias-confined-control | control | RESOLVES | RESOLVES | PASS | 1 | 0 |
| canonical-alias-escape-control | control | GONE | GONE | PASS | 1 | 0 |

Top-level `schema`/`resolver`/`matrix`/`resolver_sha256`/`matrix_sha256`/`totals` are identical
across A, B and committed; `resolver_sha256` and `matrix_sha256` match the working-tree bytes I
hashed above, so the committed receipt is consistent with the bytes it names.
**No class, totals, hash, or ordering divergence exists between my runs and the committed receipt.**

## Byte identity — the answer is NO, and the cause is receipt noise

```
0e90c6d5… runA.json          520c0e2f… runB.json
28e295e8… run_extra1.json    b85e0b6b… run_extra2.json   e07e16a7… run_extra3.json
550a863b… c1-fixed.json
cmp runA.json runB.json  → differ: char 253, line 7   (65 of 65 case records differ)
```

Normalising only `/tmp/kasegi-r23-c1-[A-Za-z0-9_]+` to a placeholder makes A == B == committed
exactly (deep JSON equality, `sort_keys=True`, all 13 cases / all fields): see
`normalized_equal A==B: True`, `normalized_equal A==COMMIT: True`. So five independent runs and the
committed artifact differ in exactly one thing: the ephemeral `mkdtemp` token embedded in
`cli_stdout`.

## Findings

> **Read the generation banner first.** F1–F3 below were measured on the generation-1 bytes
> (`resolve.py` `ed9a9dae…`, fixtures `5e61a33e…` / 13 cases, checker `1bc2db10…` schema 1,
> `c1-fixed.json` `550a863b…`). Those bytes were replaced in place while this seat was running;
> F1 and F2 are **closed** by the landed checker and F3 survives. Current-state findings are
> F4–F7 in "Generation 2/3" at the end of this report. Nothing below was retracted: each finding
> is true of the exact bytes it names.

### F1 — LOW (verifiability): the receipt is not byte-reproducible; `cli_stdout` carries an ephemeral path that nothing asserts

`corpus/instruments/mirror-containment-check.py:113` records the CLI's stdout verbatim
(`record["cli_stdout"] = (proc.stdout or "").strip()`), and the CLI prints its own scratch output
paths at `corpus/instruments/resolve.py:577` (`sys.stdout.write("wrote %s\nwrote %s\n" % (tsv, md))`).
Those paths come from `tempfile.mkdtemp(prefix="kasegi-r23-c1-")`
(`mirror-containment-check.py`, `run_case`), so every run and every receipt stores a fresh random
token. 65/65 case records across my five runs differ from the committed receipt — and from each
other — on this field alone (evidence: `1c8723…`-class raw sha divergence plus the `cmp`/`diff`
output above; `diff -u runA.json runB.json` shows 13 hunks, each only the `/tmp/kasegi-r23-c1-XXXX/tool/`
token).

Impact: any cross-seat or post-hoc check of the form "does the replayed receipt equal the committed
receipt" fails on identical inputs and identical semantics. It also means the committed receipt
cannot be authenticated by byte equality alone; it must be normalised first, which I had to do.
`cli_stdout` is never asserted anywhere in the checker, so its embedded paths are pure noise with a
reproducibility cost. Fix: either drop `cli_stdout` from the receipt, or record it with the case
root masked (the checker already knows `root`).

### F2 — MEDIUM (verifiability of the path-confinement half of C1): the matrix asserts the `class` label only; `resolved_path` is never read, so a falsified path still passes 13/13

The checker parses exactly two TSV columns and asserts one value:
`mirror-containment-check.py:126-127` (`i_cite`, `i_cls`), `:136` (`classes[cols[i_cite]] = cols[i_cls]`),
`:138-140` (`record["actual"] == case["expect"]` → PASS). `resolved_path` — the column that carries
the actual confinement evidence — is present in the CLI's own output
(`resolve.py:329`, row writer `:330-334`) and is never inspected.

Demonstrated in scratch: I copied `resolve.py` to `/tmp/…/mut_path.py` and changed only the emitted
path cell to a nonexistent literal (line 334, `r["path"]` → `"/MUTATED/nonexistent"`), leaving every
class computation untouched.

```
python3 corpus/instruments/mirror-containment-check.py \
  --resolver /tmp/kasegi-r23-falsify-RerunMatrix/mut_path.py \
  --json /tmp/kasegi-r23-falsify-RerunMatrix/mut_path_receipt.json
→ cases=13 escape=6 controls=7 pass=13 fail=0   exit 0   mut_path_receipt.json = 1c872353…
```

A control mutation of the same file, forcing `class` to `GONE` (line 334 only), is caught:

```
mut_class.py → cases=13 escape=6 controls=7 pass=8 fail=5   (pentad of non-GONE controls flips)
```

So the harness is sensitive to the class boundary and blind to the path. Concretely: C1's
`under_mirror()` realpath confinement (`resolve.py:215-220`) is attested only by `resolve.py`'s own
class assignment. The matrix proves the *labels* move correctly (escape 6/6 to GONE, controls 7/7
retained); it does not independently prove that the file behind a `MIRROR-EQUIVALENT` or `RESOLVES`
row lies inside the mirror. The checker's docstring already says it "measures the detector's
classification only", so this is a gap in the evidence chain, not a contradiction of its own scope —
but a reader who takes the PASS as path-confinement evidence is over-reading it. Cheapest close:
assert `resolved_path` for the two `MIRROR-EQUIVALENT` controls is `realpath`-inside the case mirror
root, and for the escapes that no resolved path exists.

Supplementary, non-vacuousness evidence (my own runs, independent of the checker's own delete logic
— `independent_probe.py` imports `build_case`, keeps the tree, and runs fixed and baseline bytes on
the same tree):

```
bounty-parent-traversal          escape expect=GONE fixed=GONE baseline=MIRROR-EQUIVALENT planted_outside=[('relocated/outside.md', True)]
bounty-parent-traversal-vault    escape expect=GONE fixed=GONE baseline=MIRROR-EQUIVALENT planted_outside=[('relocated/outside-vault/secret.mjs', True)]
relative-mirror-fallback-escape  escape expect=GONE fixed=GONE baseline=MIRROR-EQUIVALENT planted_outside=[('relocated/outside-vault/secret.mjs', True)]
bounty-fallback-symlink-escape   escape expect=GONE fixed=GONE baseline=MIRROR-EQUIVALENT planted_outside=[('secret/outside.mjs', True)]
relative-fallback-symlink-escape escape expect=GONE fixed=GONE baseline=MIRROR-EQUIVALENT planted_outside=[('secret/second.md', True)]
bounty-prefix-sibling-confusion  escape expect=GONE fixed=GONE baseline=MIRROR-EQUIVALENT planted_outside=[]   # decoy at relocated/tbh/-legacy/README.md
...
fixed_mismatches=[]
harness_discriminates(escape fixed!=baseline)=[all six escape ids]
```

For five escape cases the escaped target **exists on disk** and is outside the mirror root, and the
fixed bytes still return GONE while the baseline bytes return MIRROR-EQUIVALENT on the same tree —
so the six escape pins are decided by the boundary/confinement logic, not by a missing file. For
`bounty-prefix-sibling-confusion` the planted decoy lives at `relocated/tbh/-legacy/README.md`; the
baseline startswith mapping reaches it (`MIRROR-EQUIVALENT`), the fixed `bounty_suffix()` root
boundary (`resolve.py:201-213`) does not (`GONE`).

### F3 — INFORMATIONAL (latent, inert today): class lookup collapses duplicate citation rows

`mirror-containment-check.py:136` writes into a dict keyed by citation, and `:137` reports
`len(classes)` as `rows`, so two conflicting rows for one citation would silently keep the last and
still count as one row. Inert for this frozen matrix: every case's lane holds exactly one citation,
and all 78 CLI stdouts I collected (6 receipts × 13 cases) report `distinct=1` — 0 anomalies. Worth
knowing before any future case plants two citations for the same string.

## Verified positives (my reproductions, not restatements of the L1 claim)

- Five consecutive replays of the frozen matrix against the landed working-tree bytes produce
  identical classes, identical totals (13/13 pass, 6 escape, 7 control), and identical
  `resolver_sha256` / `matrix_sha256`; nothing flaked.
- The committed receipt's two hash fields match the bytes I hashed myself, so the artifact is
  self-consistent with what it names.
- The harness runs no writes into the repo: `git status --porcelain` after all runs shows only the
  pre-existing ` M LOG.md` (present before my first command); `ls -d /tmp/kasegi-r23-c1-* | wc -l`
  is `0`, i.e. every case root was cleaned up.
- `TMPDIR=/nonexistent-tmpdir …` still yields 13/13 and exit 0 (`tmpdir_receipt.json`), so the
  tempdir fallback does not silently degrade the matrix — negative result, no finding.

## Residual risk and scope limits

- I measured only the C1 detector matrix (`mirror-containment-check.py` + its fixtures, committed
  and baseline receipts). C2 (F06-F08 coverage), source snapshots, docs rows, and QUALITY gates were
  not in my slice and are untouched by this report.
- My determinism claim covers 5 runs on this host. It does not establish reproducibility across
  hosts, filesystems with different symlink semantics, or with `KASEGI_MIRROR` pointing at a
  non-`relocated/tbh` layout.
- The F2 path-blindness mutation is label-preserving and exists only in `/tmp`; it demonstrates an
  assertion gap, not a defect in the landed `resolve.py`, whose `under_mirror()` gate
  (`:215-220`) does apply on the class-assignment path.
- Overlap note: the baseline-vs-fixed discrimination above is corroborating context for my matrix
  slice; the dedicated baseline and mutation seats own the authoritative mutation analysis.
- No admission, verdict, or score movement is claimed here. Classes in this report are the
  instrument's own output, reproduced by me.

## Evidence durability (append-only note, added after the round-35 scratch-sweep notice)

The peer notice that `.ufo/waves/round-35/scratch/` was removed by an external sweep at ~03:45 does
**not** dangle any reference in this report. My scratch is `/tmp/kasegi-r23-falsify-RerunMatrix/`,
not under `.ufo/`; `grep -n "round-35" RerunMatrix.md` returns nothing; and re-checked at 03:46 all
eight receipts, both mutant resolvers (`mut_path.py`, `mut_class.py`), `independent_probe.py`, and
the retained `probe/` tree (13 materialised cases + `probe.json`) were still present. Round-23
evidence was not in the swept tree.

That precedent is why the raw hashes of every artifact this report rests on are recorded here. If
`/tmp` evidence is ever removed, the receipts are reconstructible with the commands above — but they
must then be verified **semantically**, not by raw sha, because F1 guarantees the raw bytes differ
per run. Rebuild check: mask `/tmp/kasegi-r23-c1-[A-Za-z0-9_]+` → `<SCRATCH>` in every `cli_stdout`
/ `cli_stderr`, then deep-JSON compare with `sort_keys=True`. Under that normalisation A, B,
extra1-3 and the committed receipt are equal; the expected outcomes are `mut_path` → 13 pass / 0
fail, `mut_class` → 8 pass / 5 fail, `tmpdir` → 13 pass / 0 fail.

| artifact (in `/tmp/kasegi-r23-falsify-RerunMatrix/`) | sha256 |
|---|---|
| `runA.json` | `0e90c6d597f1310ed31a511d5c8434b56a108e52c1b7faf1f4facf1fb6f42d10` |
| `runB.json` | `520c0e2f1a4c9840a9ae32660a8f6dd7108395b126cde76eb6143944841a9fab` |
| `run_extra1.json` | `28e295e8e6e9e441f3d0ade11b730ce6dfbc0f2cd82aa1e26497a2a97de7d7bc` |
| `run_extra2.json` | `b85e0b6b9e745219cb5d7a109e93433fe865f5f70553437739e9caafa487c34d` |
| `run_extra3.json` | `e07e16a754d24f0b1c9410c46d0a5baf17971cea517321f969442affcaea5f59` |
| `mut_path_receipt.json` | `1c872353180ac62538a9056a329fbc4f613c637a9bc5dad6a18577f10070cfc3` |
| `mut_class_receipt.json` | `44512c8932fb453944af96ce417700bdc3ffd4fbdb0b5ba44ef38fcc1ed01e0c` |
| `tmpdir_receipt.json` | `21a5436dbe4d09369aa529b43f3443e24a7e954a67525463fa3f13ae4505bf94` |
| `probe/probe.json` | `b28bd5d680caca29b4863f6ae6494b9e867263b2f8cb1760d2f952ab91cccfd0` |
| committed `.ufo/waves/round-23/c1-fixed.json` (in-repo, not scratch) | `550a863b9c3c167e1b0015825f8c1aa92a385fded751c19cd40a9ac00657b777` |

## Generation 2/3 — the subject was replaced in place while this seat ran (append-only)

Everything above is true of generation-1 bytes. While this seat was finishing, sibling seats landed a
different `resolve.py`, a different matrix and a schema-2 checker, and regenerated both receipts. I
observed the following transitions with my own hashes (`sha256sum`, local clock, `generated_at` in
UTC = local + 3h):

| observed at (local) | `resolve.py` | fixtures (cases) | checker | `c1-fixed.json` |
|---|---|---|---|---|
| 03:28 (gen 1, the bytes above) | `ed9a9dae…` | `5e61a33e…` (13) | `1bc2db10…` (schema 1) | `550a863b…` (13/13) |
| 03:46:26 | `fce5b84b…` | `4e39f65c…` (20) | `53742c8d…` (schema 2) | `21b85212…` (20/20) |
| 03:47:58 | `fce5b84b…` | `158a423c…` (22) | `53742c8d…` | `0ec4dafb…` (22/22) |
| 03:48:29 | `fce5b84b…` | `332a5fe9…` (23) | `53742c8d…` | `c8041b9d…` (23/23) |

At 03:50 the tree was stable on that last generation (fixtures `332a5fe9…`, `resolve.py`
`fce5b84b…`, checker `53742c8d…`, `c1-fixed.json` `c8041b9d…`), which is the state every gen-2/3
number below describes; a later move would only be a further generation.

`c1-baseline.json` moved with it (`46bda70f…` 13 cases → `8ad926ed…` 20 → `ea11b651…` 22; at the
22-case generation it recorded 13 pass / 9 fail, all nine escape ids resurrected to
`MIRROR-EQUIVALENT`).

### Pinned replay of the current generation (determinism answer for gen 2/3)

Running against the live tree is not stable: my first gen-2/3 pair used fixtures `4e39f65c…` (20
cases) and by the post-run checksum the fixture file had already moved on (`sha256sum -c` →
`corpus/instruments/mirror-containment-fixtures.json: FAILED`, while both runs had recorded
`matrix_sha256=4e39f65c…`). So I pinned a snapshot and replayed that:

```
mkdir -p /tmp/kasegi-r23-falsify-RerunMatrix/snap
cp corpus/instruments/resolve.py corpus/instruments/mirror-containment-fixtures.json \
   corpus/instruments/mirror-containment-check.py .ufo/waves/round-23/c1-fixed.json \
   /tmp/kasegi-r23-falsify-RerunMatrix/snap/
cd /tmp/kasegi-r23-falsify-RerunMatrix/snap
python3 mirror-containment-check.py --resolver resolve.py \
  --fixtures mirror-containment-fixtures.json --json ../snap_runA.json    # exit 0
python3 mirror-containment-check.py --resolver resolve.py \
  --fixtures mirror-containment-fixtures.json --json ../snap_runB.json    # exit 0
```

Snapshot bytes: `resolve.py` `fce5b84be4cece91…`, fixtures `332a5fe95b94207c…`,
checker `53742c8d9529dffb…`. Both runs: `cases=23 escape=11 controls=12 pass=23 fail=0`.

- **My two pinned runs are byte-identical**: `snap_runA.json` and `snap_runB.json` are both
  `e3196d020037f56640a0c4f1d9353d80b12847da517bf39a822222bfad36c4a6` (`cmp` → equal).
- **Against the committed receipt for the same matrix** (`c8041b9d…`, 23 cases, matrix
  `332a5fe9…`, generated 06:48:29Z): every case field is identical —
  `field diffs vs my pinned snapshot run: []` — and the only top-level differences are
  `generated_at` (mine 06:48:41Z) and the snapshot's own `resolver`/`matrix` **paths**; the
  `resolver_sha256`, `matrix_sha256`, `checker_sha256`, `schema` and `totals` all match.
- Against the preceding committed receipt (`0ec4dafb…`, 22 cases, matrix `158a423c…`), the 22
  shared cases agree on every field except the per-case `matrix` id, which necessarily changed with
  the matrix; `absolute-parent-traversal` is present only in mine.
- Raw byte equality with the committed receipt never holds, for two structural reasons: the
  perpetual `generated_at` (F4) and the absolute `resolver`/`matrix` paths, which point into the
  snapshot in my run.

### F4 — LOW (current): `generated_at` makes any receipt non-byte-comparable to a committed one

`generated_at` is stamped per receipt (UTC, second resolution), so a replay can never be
byte-identical to a committed receipt even when every measured field agrees. Evidence: `diff -u
snap_runA.json snap/c1-fixed-latest.json` yields exactly three changed lines — `generated_at`
(06:48:41Z vs 06:48:29Z), `matrix`, `resolver` — with all 23 case records untouched. Any audit that
asserts byte equality between a replayed and a committed receipt must exclude `generated_at` (and
should normalise the two path fields); with gen-1 bytes it additionally had to exclude `cli_stdout`
(F1), which gen 2 no longer needs.

### F5 — MEDIUM (current): three matrix cases pass only because host paths are absent; the harness cannot isolate an absolute citation

`corpus/instruments/mirror-containment-fixtures.json` now carries three cases whose citation is an
absolute host path, and whose own `note` fields admit the dependence:

- `absolute-bounty-fallback-control` — `/home/vgpnk/Projects/bounties/ops/rank.mjs:1`, expect
  `MIRROR-EQUIVALENT`, note: "Host-dependent: requires … to stay absent on the run host (verified
  2026-10-25)";
- `absolute-prefix-sibling-confusion` — `/home/vgpnk/Projects/bounties-legacy/README.md:1`, expect
  `GONE`, note: "the literal must be absent on the host for this to stay a confusion case";
- `absolute-parent-traversal` — `/home/vgpnk/Projects/bounties/../outside-vault/secret.mjs:1`,
  expect `GONE`, note: "Host-dependent".

The checker isolates `HOME`, `KASEGI_MIRROR` and the lane root
(`mirror-containment-check.py`, the per-case `env` dict), but an absolute citation never consults
`HOME`. Demonstrated in scratch by copying the matrix, repointing only that case's `cite` at a file
that exists on this host, and replaying:

```
cp -> /tmp/kasegi-r23-falsify-RerunMatrix/host_probe_fixtures.json   # absolute case cite = /etc/hostname:1
python3 corpus/instruments/mirror-containment-check.py \
  --fixtures /tmp/kasegi-r23-falsify-RerunMatrix/host_probe_fixtures.json \
  --json /tmp/kasegi-r23-falsify-RerunMatrix/host_probe_receipt.json
→ probe case: expect GONE, actual RESOLVES, path_check "gone-with-path",
  resolved_path "/etc/hostname", status FAIL;  totals pass=19 fail=1
```

So the matrix is not self-contained for absolute forms: today all three host paths are absent
(`ls` on `/home/vgpnk/Projects/bounties`, `…/bounties-legacy`, `…/outside-vault` → all "No such file
or directory", 03:48), which is the only reason those three cases pass. A host where any of them
exists flips the case, and the pass/fail carries no signal about `resolve.py`. Fix: make the
absolute prefix a fixture-declared, per-case substituted root (like `@ROOT@` for symlinks) so the
citation is absolute but inside the case root.

### F6 — LOW (current): the sole carve-out grants PASS to an `INTERNAL` control whose path is outside the lane

`lane-relative-parent-internal-control` PASSes with `path_check: "carve-out:path-outside-internal"`
and `resolved_path: "<CASE>/lane/../outside.md"` (i.e. `<CASE>/outside.md`, outside the lane root).
`path_verdict()` binds `INTERNAL` to the lane root and would report `path-outside-internal`; the
fixture declares `path_tolerance: "carve-out"` (the only case that does), and `run_case` then accepts
the record while prefixing the verdict `carve-out:` — visible, never suppressed. Effect: the
`controls` total counts a control whose path does not corroborate its own class name. The class
itself is the frozen pre-round-23 lane-first semantics (`resolve.py` classifies the lane branch
before the mirror fallback), so this is a naming/verification mismatch worth stating, not a
regression: a reader must not treat `controls 12/12` as "12 path-verified controls".

### F7 — MEDIUM (process, current): "the committed receipt" had no stable referent inside one falsify window

`c1-fixed.json` took four values in ~20 minutes (`550a863b…` → `21b85212…` → `0ec4dafb…` →
`c8041b9d…`) and the fixtures three (`5e61a33e…` → `4e39f65c…` → `158a423c…` → `332a5fe9…`). During
one of my replay pairs the fixture file changed under a running checker (the `sha256sum -c` failure
quoted above), and at snapshot time the committed receipt (`0ec4dafb…`, 22 cases) lagged the fixture
file (`332a5fe9…`, 23 cases) by the not-yet-landed `absolute-parent-traversal`. Consequences for any
seat doing this same comparison: (i) a divergence can be landing churn, not a defect — pin the
receipt hash and the matrix hash together before reporting one; (ii) a receipt that lags the
fixtures is not evidence of a mismatch, only of unfinished landing; (iii) the only durable
comparison is replay-vs-receipt **for the same `matrix_sha256`**, which is what the table above
does.

### Generation-2/3 positives I reproduced

- Two pinned replays of the current generation are byte-identical, so the gen-1 non-determinism
  (F1) is gone: the checker now masks the case root in `cli_stdout`
  (`record["cli_stdout"] = (stdout or "").strip().replace(root, "<CASE>")`), which is exactly the
  fix F1 asked for.
- F2 is closed: the checker now reads the `resolved_path` column (`read_tsv` → `{citation: (class,
  resolved_path)}`) and `path_verdict()` requires a non-`GONE` class to name an existing path
  confined to the root that class implies, and `GONE` to carry no path. A path-falsifying resolver
  would now fail on the two `MIRROR-EQUIVALENT` controls instead of passing 13/13.
- F3 survives unchanged in gen 2: `read_tsv()` still stores rows in a dict keyed by citation, so a
  duplicate citation row keeps only the last and is counted once.
- All 23 current cases pass on the landed bytes and the baseline receipt resurrects all eleven
  escape ids, so the escape pins remain non-vacuous at the larger matrix size.

### New artifacts (in `/tmp/kasegi-r23-falsify-RerunMatrix/`)

| artifact | sha256 |
|---|---|
| `snap_runA.json` = `snap_runB.json` | `e3196d020037f56640a0c4f1d9353d80b12847da517bf39a822222bfad36c4a6` |
| `snap/mirror-containment-fixtures.json` | `332a5fe95b94207cdf25caf29d52b394f81701b4fe441b92e47ab3ac100005e3` |
| `snap/mirror-containment-check.py` | `53742c8d9529dffb8c40c39b3448de7388b774b548d7831670598d5534bff5d1` |
| `snap/resolve.py` | `fce5b84be4cece914260f03a3a8b739dc1108381f97482bbfc7b22143810a4b0` |
| `snap/c1-fixed.json` (22-case generation) | `0ec4dafb8bbca7d13b3c99e572b512eabbb3e6af0727893919ed241ade1134ff` |
| `snap/c1-fixed-latest.json` (23-case generation) | `c8041b9d49fafc3c5400cda7f73acba0b85c6ee54250fac17678d38eda6ebbf7` |
| `gen2_runA.json` = `gen2_runB.json` (20-case generation) | `dea0f57b0fff056f3bd0fd45d1c9fbf5eeaa18ea2ce52011159b54cef7ce7c5c` |
| `host_probe_receipt.json` (absolute-cite probe) | `500d1d92ea09ac9589e30274f7ac636d1df2cd2680ef01bdecb6d20e19277cbf` |
