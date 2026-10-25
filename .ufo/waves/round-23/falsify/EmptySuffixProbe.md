# EmptySuffixProbe — round 23 falsify (C1 depth:verifiability)

Scoped executor probe. Read-only against landed bytes; the only write is this report.
Fixture drivers and their disposable roots live in `/tmp/kasegi-r23-falsify-EmptySuffixProbe-2`.

## Bytes and environment actually exercised

```text
sha256 resolve.py            ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9
sha256 mirror-containment-fixtures.json
                             5e61a33ed5fa530547aff197fad9380d86d5850374bbb4f2a8f99df44b5e76a9
python3 --version            3.14.8 (linux 7.2.11-arch1-1)
host roots                   /home/vgpnk/Projects/bounties ABSENT
                             /home/vgpnk/Projects/the-bounty-hunter ABSENT
```

Both digests match `.ufo/waves/round-23/c1-fixed.json`. No install or tool update was made.

Method: copy `corpus/instruments/resolve.py` unmodified into a per-case `tool/` directory under
a disposable root, run `python3 tool/resolve.py lane` with an isolated
`HOME`, `KASEGI_MIRROR=relocated/tbh` and a one-line `lane/SKILL.md`, then read the CLI's own
`citation-survival.tsv`. Populated-mirror cases materialise `relocated/tbh/README.md`,
`.../docs/note.md`, `.../ops/rank.mjs`.

```bash
python3 /tmp/kasegi-r23-falsify-EmptySuffixProbe-2/probe.py      # 16-case matrix
python3 /tmp/kasegi-r23-falsify-EmptySuffixProbe-2/probe2.py     # fixed vs c1-baseline bytes
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/mirror-containment-check.py           # committed matrix, no --json
python3 corpus/instruments/mirror-containment-check.py \
  --fixtures /tmp/kasegi-r23-falsify-EmptySuffixProbe-2/norow-fixtures.json
```

## Observed classes and exit codes (fixed bytes)

| citation (sole span) | fixture state | exit | TSV class (domain) |
|---|---|---|---|
| `` `~/Projects/bounties/` `` | mirror populated, HOME bounty root absent | 0 | **GONE** (bounty) |
| `` `~/Projects/bounties/` `` | `home/Projects/bounties/` exists (empty dir) | 0 | RESOLVES (bounty, `literal`) |
| `` `~/Projects/bounties` `` | mirror populated | 0 | **GONE** (bounty) |
| `` `/home/vgpnk/Projects/bounties/` `` | mirror populated | 0 | **GONE** (bounty) |
| `` `~/Projects/bounties/:12` `` | mirror populated | 0 | **GONE** (bounty) |
| `` `~/Projects/bounties:12` `` | mirror populated | 0 | **GONE** (bounty) |
| `` `~/Projects/bounties/.` `` | mirror populated | 0 | **GONE** — rewritten to `~/Projects/bounties/` by `rstrip(".,;:")` at `resolve.py:290` |
| `` `~/Projects/bounties/./` `` | mirror populated | 0 | **MIRROR-EQUIVALENT**, path `<mirror>/.` |
| `` `~/Projects/bounties/ops/../` `` | mirror populated (`ops/` exists) | 0 | **MIRROR-EQUIVALENT**, path `<mirror>/ops/..` |
| `` `~/Projects/bounties//` `` | mirror populated | 0 | GONE (suffix `"/"` → `join(mirror, "/") == "/"`) |
| `` `~/Projects/bounties//README.md` `` | `mirror/README.md` exists | 0 | **GONE** (see F4) |
| `` `~/Projects/bounties/README.md` `` | `mirror/README.md` exists | 0 | MIRROR-EQUIVALENT (control for F4) |
| `` `~/Projects/the-bounty-hunter/` `` | same mirror root | 0 | **RESOLVES** (other, path = mirror root) |
| root citation + `` `docs/note.md` `` | mirror populated | 0 | 2 rows: root GONE, `docs/note.md` MIRROR-EQUIVALENT |
| empty span (two adjacent backticks) as the only span | lane with `SKILL.md` only, no corpus | **1** | 0 data rows; header-only TSV; no `citation-survival.md` |
| `` ` ` `` whitespace-only span | empty corpus | **1** | same |
| `` `npm install` `` (non-path-like) | empty corpus | **1** | same |
| no span at all | empty corpus | **1** | same |
| `` `` `` + corpus `` `docs/note.md` `` | mirror populated | 0 | 1 row MIRROR-EQUIVALENT (crash is union-wide) |

Committed matrix replay: `cases=13 escape=6 controls=7 pass=13 fail=0`, exit 0, both digests as
above — i.e. the landed matrix reproduces without writing a receipt.

## Findings

### F1 — the `max()`-over-empty-rows crash is real, reachable from the assigned shape, and leaves a half-written census

Any lane whose `SKILL.md` + `corpus/**/*.md` yield **zero** path-like citations aborts after the
TSV header is written:

```text
Traceback (most recent call last):
  File ".../tool/resolve.py", line 582, in <module>
    sys.exit(main(sys.argv))
  File ".../tool/resolve.py", line 350, in main
    maxfiles = max(r["nfiles"] for r in rows)
ValueError: max() iterable argument is empty
```

Exact evidence: `resolve.py:350` (uncaught), exit code **1**, `citation-survival.tsv` present with
header and 0 data rows, `citation-survival.md` absent. Reachable by the assigned shape: `TOKEN`
at `resolve.py:90` requires ≥1 non-backtick character, so a `SKILL.md` whose only code span is
an empty pair of backticks produces no token at all; a one-space span is extracted but rejected by
`is_pathlike` (`resolve.py:126`). Only a path-like citation in **either** scope rescues the run
(empty span + corpus cite → exit 0, one row).

Correction to the inherited note: `CountMirror.md` cites `resolve.py:329`; the fixed working-tree
bytes put both `max()` calls at `:350-351`, so that line number no longer addresses the landed
file (21-line drift).

Falsifier: any of the four zero-row inputs exiting 0 (e.g. after `max(..., default=0)`), or the
crash occurring at a line other than `:350`.

### F2 — an empty-suffix bounty-root citation is GONE while two equivalent spellings of the same target are credited; that is a spelling artifact, not a containment decision

With the mirror root populated and `~/Projects/bounties` absent, the same mirror root is scored
three ways for the same lexical target:

- `~/Projects/bounties/` → **GONE**, via `resolve.py:231`
  `... if suffix else (None, None)` — the fallback is skipped when `bounty_suffix()` returned `""`.
- `~/Projects/bounties/./` → **MIRROR-EQUIVALENT**, path `<mirror>/.`, credited by the very same
  line pair `:231-232` because `suffix == "./"` is truthy and `under_mirror(realpath(<mirror>/.), mirror)` holds.
- `~/Projects/the-bounty-hunter/` → **RESOLVES** at the same mirror root, via `:240`
  `os.path.join(mirror_root, sfx) if sfx else mirror_root`.

`./` is no more confined than `""`; both realpath to the mirror root and both pass `under_mirror`.
So the empty-suffix GONE is not a soundness verdict, it is the consequence of not applying the
`sfx else mirror_root` substitution that the sibling branch applies. The same skip exists in the
baseline bytes (`.ufo/waves/round-23/c1-baseline-resolver.py:206-213`, `if rel else (None, None)`),
so C1 neither introduced nor removed it; there is no live verdict change because both host roots
are absent. Live relevance: `~/Projects/bounties` is the lane's 8th most-cited GONE row
(`corpus/instruments/citation-survival.md:237`, 12 files / 16 occurrences), and with a restored
mirror it would stay uncreditable while the mirror-root citation form would resolve.

Impact is liveness only, not escape: `suffix == ""` can only arise when `base` equals the bounty
root exactly (`resolve.py:207-211`), and every root variant I ran landed GONE or a
realpath-confined class. No empty-suffix escape exists in these fixtures.

Falsifier: a fix mapping `""` → `mirror_root` under `under_mirror` turning the root citation into
MIRROR-EQUIVALENT, or a demonstration that the bounty root and the mirror root must not be
equivalent (which would then have to explain why `./` and the canonical alias already are).

### F3 — the landed harness cannot express a passing `NO-ROW`, and the CountMirror report's matrix description does not match the committed bytes

`mirror-containment-check.py:84` seeds `actual = "NO-ROW"` and `:138` sets it when the citation is
absent, but `PASS` is assigned only at `:139`, after a successful TSV read; a zero-row CLI exits 1,
so `:117` returns early with `status = FAIL`. Reproduced on a scratch copy of the committed matrix
with one case `{"cite": "", "expect": "NO-ROW"}`:

```text
empty-citation-produces-no-row             control expect=NO-ROW           actual=NO-ROW           FAIL problems=cli-exit-1
cases=1 escape=0 controls=1 pass=0 fail=1
NOROW_EXIT=1
```

Consequence: a no-row case is unpassable until `resolve.py:350` is fixed, and 13/13 PASS is only
attainable because the committed matrix omits zero-row inputs.

Separately, `build/CountMirror.md` asserts “The committed JSON matrix has 15 IDs” and enumerates
an `empty-citation-produces-no-row` case plus `canonical-sibling-prefix-boundary`; the committed
file has **13** `"id"` entries (`grep -c '"id":' mirror-containment-fixtures.json` → `13`) and the
prefix-sibling case is named `bounty-prefix-sibling-confusion`. Coverage narrative ≠ landed bytes.

Falsifier: a zero-row case reporting PASS, or a 15-case matrix at the pinned digest.

### F4 — a double-slash suffix discards the mirror root and reads the host filesystem root (sound, but a false GONE and a host-absolute read)

`bounty_suffix` returns `base[len(root) + 1:]` without the `.lstrip("/")` that `mirror_suffix`
applies (`resolve.py:211` vs `:197`). So `~/Projects/bounties//README.md` yields suffix
`"/README.md"`, and `os.path.join(mirror_root, "/README.md")` is `"/README.md"`:

```text
- `~/Projects/bounties//README.md`   exit 0 -> GONE
- `~/Projects/bounties/README.md`    exit 0 -> MIRROR-EQUIVALENT  <mirror>/README.md
```

`under_mirror` rejects the root-absolute path, so containment holds; but the citation is a false
GONE while `mirror/README.md` exists, and the literal probe escapes the fixture's HOME/mirror
isolation into the real host root (host `/README.md` absent here, so GONE).

Falsifier: `//x` resolving against the mirror, or an argument that the absolute join cannot occur.

## What survived the attack

- Six escape cases still pin GONE and seven controls keep their classes, all with exit 0
  (`pass=13 fail=0`) on the exact resolver and matrix digests above.
- No bounty-root spelling I tried produced an out-of-mirror RESOLVES/MIRROR-EQUIVALENT: root and
  `:NN`-anchored forms are GONE; `./`, `ops/../` credit only `<mirror>`-prefixed realpaths.
- Root citations never lose their row when other citations exist (2-row case above).

## Scope limits

- One host, Python 3.14.8; no live mirror, bounties or the-bounty-hunter root, so no live-census
  movement is claimed. No network, credentials or account operations.
- Only the working-tree bytes at the pinned digests. The committed matrix and resolver were not
  edited; the harness was run without `--json`, so it wrote nothing into the lane tree.
- Fixture drivers are scratch (`/tmp/kasegi-r23-falsify-EmptySuffixProbe-2/probe.py`,
  `probe2.py`); this report is the only repo write.
- Detector classification only. No admission, scorecard or C1 adjudication claim is made here.
