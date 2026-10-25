# EmptySuffixProbe — round 23 falsify (C1 depth:verifiability)

Scoped executor probe. Read-only against the landed bytes; the only repo write is this report.
Fixture drivers live in `/tmp/kasegi-r23-falsify-EmptySuffixProbe-2/drivers/` (see §Provenance).

## 0. The artifact changed under the wave — every claim here names its digest

The landed C1 bytes were rewritten while this seat was measuring them (files owned by the
integration lane, not by this seat). Three resolver digests were observed within ~8 minutes:

| rev | resolver sha256 | matrix sha256 (cases) | status |
|---|---|---|---|
| R1 | `ed9a9dae10024bbb…` | `5e61a33ed5fa5305…` (13) | read at 03:38, matches the original `c1-fixed.json` |
| R-mid | `8dd45bc8d9aedbb2…` | `4e39f65c7c1bdc7d…` (20) | observed in `mirror-containment-check.py` stdout at 03:46 while the receipts were being refreshed; not on disk now |
| **R2** | **`fce5b84be4cece91…`** | **`4e39f65c7c1bdc7d…` (20)** | current working tree; `resolve.py` mtime 03:46:26 |

Current digests, all re-hashed after the runs below:

```text
resolve.py                               fce5b84be4cece914260f03a3a8b739dc1108381f97482bbfc7b22143810a4b0
mirror-containment-check.py              53742c8d9529dffb8c40c39b3448de7388b774b548d7831670598d5534bff5d1
mirror-containment-fixtures.json         4e39f65c7c1bdc7d6a390f0aeefe5fa88af67ea84659aa9ff36b84d271c2400b
c1-baseline-resolver.py                  d6a3c3f1a1d8e97d42d66a8aa3cb34530b7bc1c18b194e487ef8d580d869f903
c1-fixed.json (file)                     21b852128dbcc16fa295a878d7def10d15d04c0e71200fb5ca666bfa41f88f28
```

All numbers below are R2 unless labelled R1. The matrix grew 13 → 20 cases (9 escape / 11
controls); `c1-fixed.json` now pins the R2 digests and reports `pass=20 fail=0`.

Environment: linux 7.2.11-arch1-1, Python 3.14.8; host `~/Projects/bounties` and
`~/Projects/the-bounty-hunter` both ABSENT. No tool install or update was made.

## 1. Method

`drivers/snapshot_probe.py` snapshots `resolve.py` **once**, records its sha256 before and after
the batch, copies the snapshot into a per-case `tool/` directory, and runs
`python3 tool/resolve.py lane` with an isolated `HOME`, `KASEGI_MIRROR=relocated/tbh` and a
one-line `lane/SKILL.md`; it reads the CLI's own `citation-survival.tsv`. The populated-mirror
cases materialise `relocated/tbh/{README.md,docs/note.md,ops/rank.mjs}`.

```bash
python3 /tmp/kasegi-r23-falsify-EmptySuffixProbe-2/drivers/snapshot_probe.py   # R2, digest-pinned
python3 /tmp/kasegi-r23-falsify-EmptySuffixProbe-2/drivers/probe2.py            # R2 fixed vs baseline
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/mirror-containment-check.py                          # committed matrix, no --json
python3 /tmp/kasegi-r23-falsify-EmptySuffixProbe-2/drivers/norow.py
python3 corpus/instruments/mirror-containment-check.py \
  --fixtures /tmp/kasegi-r23-falsify-EmptySuffixProbe-2/norow-fixtures.json
```

`sha_before == sha_after == fce5b84b…`, `drift False`, so the batch below is one revision.

## 2. R2 results — empty-suffix bounty-root citations

| citation (sole span) | fixture state | exit | class (domain) | path column |
|---|---|---|---|---|
| `` `~/Projects/bounties/` `` | mirror populated, literal root absent | 0 | **GONE** (bounty) | empty |
| `` `~/Projects/bounties` `` | same | 0 | **GONE** (bounty) | empty |
| `` `~/Projects/bounties/:12` `` | same | 0 | **GONE** (bounty) | empty |
| `` `/home/vgpnk/Projects/bounties/` `` | same | 0 | **GONE** (bounty) | empty |
| `` `~/Projects/bounties/` `` | `home/Projects/bounties/` exists (empty dir) | 0 | RESOLVES (bounty) | `<CASE>/home/Projects/bounties/` |
| `` `~/Projects/bounties/./` `` | mirror populated | 0 | **MIRROR-EQUIVALENT** (bounty) | `<CASE>/relocated/tbh/.` |
| `` `~/Projects/bounties/ops/../` `` | mirror populated (`ops/` exists) | 0 | **MIRROR-EQUIVALENT** (bounty) | `<CASE>/relocated/tbh/ops/..` |
| `` `~/Projects/bounties//` `` | mirror populated | 0 | **GONE** (bounty) | empty |
| `` `~/Projects/bounties//README.md` `` | `mirror/README.md` exists | 0 | MIRROR-EQUIVALENT (bounty) | `<CASE>/relocated/tbh/README.md` |
| `` `~/Projects/bounties/README.md` `` | `mirror/README.md` exists | 0 | MIRROR-EQUIVALENT (bounty) | `<CASE>/relocated/tbh/README.md` |
| `` `~/Projects/the-bounty-hunter/` `` | same mirror root | 0 | RESOLVES (other) | `<CASE>/relocated/tbh` |
| `` `~/Projects/the-bounty-hunter` `` | same mirror root | 0 | RESOLVES (other) | `<CASE>/relocated/tbh` |

Zero-row inputs (R2): a `SKILL.md` whose only span is an empty backtick pair, a whitespace-only
span, a non-path-like span (`npm install`), or no span at all → **exit 0**, both
`citation-survival.tsv` (header only) and `citation-survival.md` written. An empty span plus one
corpus citation yields the corpus row (`docs/note.md` MIRROR-EQUIVALENT), exit 0.

Containment spot checks (R2): `` `~/Projects/bounties/../outside.md:1` `` with the target outside
the mirror → GONE; `` `../outside-vault/secret.mjs:1` `` with the target outside the mirror → GONE.

Committed matrix replay on R2: `cases=20 escape=9 controls=11 pass=20 fail=0`, checker exit 0,
`resolver_sha256=fce5b84b…`, `matrix_sha256=4e39f65c…`.

Fixed-vs-baseline, digest-pinned, same citations: current fixed (`fce5b84b`) and current baseline
(`d6a3c3f1`) agree on every root form — root variants GONE, `./` MIRROR-EQUIVALENT, mirror root
RESOLVES, confined fallback MIRROR-EQUIVALENT.

## 3. Findings

### F1 — the `max()`-over-empty-rows crash was real in R1 and is fixed in R2

R1 (`ed9a9dae`, line 350) aborted on a zero-row lane:
`ValueError: max() iterable argument is empty`, exit **1**, header-only TSV, no `.md`.
R2 replaces both reductions with `max((…), default=0)` at `resolve.py:362-363`; the four zero-row
inputs above now exit **0** and both artifacts are written. Reproduced from the current bytes,
not inferred from source.

Scope note: the crash is gone, but the checker still cannot record a *passing* zero-row case —
see F3.

### F2 — a bounty-root citation is GONE while equivalent spellings of the same target are credited (persists in R2; pre-existing, not a C1 delta)

With the mirror root populated and `~/Projects/bounties` absent, one lexical target is scored two
ways:

- `~/Projects/bounties/` (also exactly, `:12`, and the absolute form) → **GONE**, because
  `resolve.py:243` skips the fallback entirely: `... if suffix else (None, None)`.
- `~/Projects/bounties/./` → **MIRROR-EQUIVALENT** with path `<mirror>/.`, and
  `~/Projects/bounties/ops/../` → **MIRROR-EQUIVALENT** with path `<mirror>/ops/..` — both through
  the same `:243-244` pair, because their suffix is truthy and `under_mirror(realpath(<mirror>/./), mirror)`
  holds.
- `~/Projects/the-bounty-hunter/` → **RESOLVES** at the same root through `:252`
  (`... if sfx else mirror_root`).

R2 adds a comment at `classify` declaring this intentional: “Root-only bounty citations keep their
pre-r23 verdict (no mirror mapping)”. That statement is factually correct — the `d6a3c3f1` baseline
also returns GONE for these roots — so this is **not** a C1 regression and not an escape: `""` can
only arise when the text after the bounty root is empty or slashes only (`bounty_suffix`,
`:210-221`), and every root form I ran was GONE or realpath-confined to the mirror. What it does falsify is the claim that the
verdict is a property of the citation target: two spellings that realpath to the same directory
differ, and `~/Projects/bounties//` (suffix `""` after `.lstrip("/")`) is GONE while
`~/Projects/bounties//README.md` resolves. Impact is liveness only: the lane's 8th most-cited GONE
row is `~/Projects/bounties` (12 files / 16 occurrences, `corpus/instruments/citation-survival.md:237`),
and a restored mirror would not change it, while `~/Projects/bounties/./` would be credited.

Observation, same branch: `exists_any` uses `os.path.exists`, so a root citation whose literal
target is an empty *directory* classifies RESOLVES (`<CASE>/home/Projects/bounties/`), i.e. a
directory counts as evidence.

Falsifier: a fix mapping `""` → `mirror_root` under `under_mirror` (root becomes
MIRROR-EQUIVALENT), or a documented rule establishing why `./` and the canonical alias may be
credited but the bare root may not.

### F3 — the harness cannot express a passing `NO-ROW` case in either revision

R2 `path_verdict` (`mirror-containment-check.py:140-153`) returns `missing-path` whenever
`expect != "GONE"` and the path column is empty, and `PASS` requires `path_check == ""`
(`:221-222`). A correct zero-row classification therefore always FAILs. Reproduced on a scratch
one-case matrix (`{"cite": "", "expect": "NO-ROW"}`) against the current bytes:

```text
empty-citation-produces-no-row   control expect=NO-ROW  actual=NO-ROW  FAIL path_check=missing-path
cases=1 escape=0 controls=1 pass=0 fail=1
resolver_sha256=fce5b84be4cece914260f03a3a8b739dc1108381f97482bbfc7b22143810a4b0
NOROW_EXIT=1
```

In R1 the same case failed earlier, as `problems=cli-exit-1` (the CLI crashed). The failure moved
with the fix; the inexpressibility did not. Consequence: a `NO-ROW` expectation cannot be pinned as
a regression test until `path_verdict` accepts a canonical zero-row outcome.

Falsifier: the same scratch matrix reporting PASS.

### F4 — the R1 double-slash false GONE is fixed in R2

R1 returned suffix `"/README.md"` without stripping, so `os.path.join(mirror, "/README.md")` became
`/README.md` and the probe read the host filesystem root while `mirror/README.md` existed. R2's
`bounty_suffix` applies `.lstrip("/")` (`:220`), and
`` `~/Projects/bounties//README.md` `` now yields MIRROR-EQUIVALENT with
`<CASE>/relocated/tbh/README.md`, identical to the single-slash form.

### F5 — the refreshed matrix pins a class/path mismatch as a declared carve-out, and still omits both shapes assigned here

`mirror-containment-fixtures.json:110-118` marks `lane-relative-parent-internal-control` with
`"path_tolerance": "carve-out"`; the R2 receipts record
`path_check = "carve-out:path-outside-internal"` for it — the case is pinned with its class
(`INTERNAL`) while its resolved path lies outside the lane root the checker bounds `INTERNAL` to,
and the mismatch is retained rather than suppressed. That is a deliberate, visible carve-out (the
receipt keeps the string), not a silent pass.

Remaining coverage gap, stated plainly: the committed 20-case matrix contains **no** root-only
bounty citation and **no** zero-row input, so the two shapes this seat attacked are exercised only
by the scratch drivers above. Also, in `c1-baseline.json`, `glob-expansion-escape` is PASS on the
baseline (`actual=GONE`), so 8 of the 9 declared escapes change verdict between baseline and fix,
not 9.

Falsifier: a committed matrix case covering either shape, or a receipt whose carve-out string is
absent while the class still passes.

## 4. What survived

- R2 committed matrix: 20/20 PASS, checker exit 0, digests as pinned.
- Both escape shapes I re-ran (bounty-parent traversal, relative parent traversal) are GONE.
- Root citations never escape: GONE or a class whose path is `realpath`-confined to the mirror.
- Zero-row lanes no longer crash the CLI.

## 5. Provenance, scratch and drivers

The originally cited `/tmp/.../probe.py` deleted itself: its `shutil.rmtree(BASE)` targeted the
directory containing the script. It has been rebuilt with the driver directory disjoint from the
case root and its sha pinned below. A rebuild is not evidence, so the R1 numbers quoted in §F1/F4
are the transcript output of the run that produced them, and the durable R2 evidence is
`drivers/snapshot.out.json`:

```text
snapshot_probe.py   d9ed55ef8b56ab875c5cfe903d20f1ea9fec97ca9c52edaf1e72aa79aac2e69a
probe.py            faca38bcb57b5cf732e0e4e9e39840d52bd17287b52f52f25eccec22e3fc29f0
norow.py            a0ce6419a6c0e8c450d8718291325fffd89e541aaf1386bb36d457d70d40b9f2
snapshot.out.json   e092c2c9e5a7f15bf3407961ece55fbc34a6e266a911a278a2a230c5eced42f4
```

Scratch is a convenience copy; the tables above are the durable evidence locus.

## 6. Scope limits

- One host, Python 3.14.8, no live mirror/bounties/the-bounty-hunter root; no network, credentials
  or account operations; no live-census movement claimed.
- Measured only the digests named in §0. The resolver, matrix, checker and receipts were not
  edited; the checker ran without `--json`, so nothing was written into the lane tree.
- Detector classification only. No admission, scorecard or C1 adjudication claim.
- The R2 artifact set changed at 03:43-03:46, i.e. after this seat's first measurements; F1 and F4
  are explicitly revision-relative.
