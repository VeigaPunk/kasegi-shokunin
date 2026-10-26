# ExecH9DeclaredBlocks — H9 declared-block validator (+ F23 example blocks)

Seat: leaf executor, wave 1, round 40 (kasegi-shokunin). Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` at base
`a7af2ce63bce153757d39bf66b366a96caf30c13`, claims freeze
`5e985b74075dd3813a63d7750966bf8abf693465`. Disk guard green at start
(`/fast/scratch/hyaku 26% use, 597.4G free`). No tool installs; no mutating git
anywhere; no writes outside this seat's wave-1 files and its scratch.

## Deliverables

| file | lines | bytes | sha256 |
|---|---|---|---|
| `ExecH9DeclaredBlocks.validator.sh` | 402 | 15338 | `59d5b19ff94c3ec057396d241ef498627f6cf782ec1577b37dc87782f971012d` |
| `ExecH9DeclaredBlocks.province.txt` | 2 | 324 | `c445324c0f6d197f4c1b94f9509f86e3afd2af467d294dcb5bcac4e15c177408` |
| `ExecH9DeclaredBlocks.readme.txt` | 28 | 2734 | `d6a9f3c1306525f91ddad82afc96e47b77043208ce42a115a0290db43cc9e15b` |
| `ExecH9DeclaredBlocks.examples-declared.txt` | 2 | 164 | `80e1cfd663aba822b3c4ec6953417eb45dba9a62bfd0638567c43055c472aafc` |

All four are byte-exact landable text: no headings, notes or validation tables
inside them. The two block files are byte-identical copies (`cmp` clean) of the
landed `ScribeF23.province.txt` / `ScribeF23.readme-row.txt` — the exact bytes
that get appended to `PROVINCE.md` and `corpus/README.md` — and
`examples-declared.txt` is the matching `declared-blocks.txt` body for **those
bytes only**. This seat's first draft (F23 wording written before the scribe's
text landed) was superseded and is not shipped.

## What the validator checks (one clause per declared line)

Interface (`bash declared-blocks-validate.sh -h` prints the same text):

```
bash declared-blocks-validate.sh --declared FILE --base REF --ref REF
     [--lane DIR] [--export DIR]
bash declared-blocks-validate.sh --selftest
```

- `--declared` — the `declared-blocks.txt` to grade (blank lines and `#` lines
  skipped; exactly three blank-free fields per line otherwise).
- `--base` / `--ref` — refs used for the numstat limb; both must resolve in the
  lane or the run is a setup error.
- `--lane` — defaults to `$DECL_LANE`, else the round's lane repo
  (`/home/vgpnk/Projects/shokunin/kasegi-shokunin`), which is exactly the repo
  the H9 text names.
- `--export` — an existing `git archive <ref>` extraction. When omitted the
  translator extracts `git archive --format=tar <ref>` once into
  `mktemp -d "${TMPDIR:-/tmp}/declared-blocks.XXXXXXXX"` and removes it on exit.

Output (one graded line per declaration, then a summary):

```
decl head mode=<export|extract> ref=<ref> base=<base> lane=<dir> export=<dir>
decl path=<p> lines=<n> tail=<pass|fail> safe=<pass|fail> diff=<pass|fail> added=<n|-> deleted=<n|-> verdict=<pass|fail> reason=<clause|->
decl summary declared=<k> pass=<k> fail=<k> exit=<0|1>
```

Exit status: `0` = at least one declaration graded and all passed; `1` = any
declaration failed (including `declared=0`); `2` = setup error
(missing/unreadable declared file, unknown or missing ref, missing/empty export,
unknown argument). A suite that gets `2` must render the limb red, not skip it.

Clauses, in evaluation order (`reason=` names the first one that fails):

| clause | test | `reason=` |
|---|---|---|
| parse | three fields, `lines` a positive integer, `sha` 64 lowercase hex, path declared once | `malformed-line`, `malformed-hash`, `duplicate-path` |
| (b) path shape | no `/` root, no empty/`.`/`..` component | `unsafe-path` |
| (b) existence | `-e` and `-f` under the export root | `absent`, `not-a-file` |
| (b) containment | `realpath -m` of the export path stays under `realpath -m` of the export root — a committed symlink cannot carry the read outside the tree | `unsafe-path` |
| (a) whole tail | `tail -n <lines> <path> | sha256sum` equals `<sha256>`; `<lines>` may not exceed the file's own line count (else `tail -n` silently clips to a shorter tail) | `tail-mismatch`, `lines-exceed-file` |
| (c) pure append | `git --no-optional-locks -C <lane> diff --numstat <base> <ref> -- <path>` yields exactly one record with `added == <lines>` and `deleted == 0` | `diff-mismatch`, `diff-EMPTY`, `diff-ERR`, `diff-MULTI`, `diff-BIN` |

`diff-EMPTY` is the case where the path is not in the diff at all (declared
block not added between base and ref); `diff-BIN` is a binary counter pair.
Every git read uses `--no-optional-locks`; nothing under the lane, the export
or any tracked tree is written.

`--selftest` builds one throwaway fixture under `mktemp -d` (git toplevel
asserted equal to the fixture dir before the first commit), exports the ref, and
grades one good declaration file plus eleven defective ones; each defective one
must be rejected for its named clause.

## Runs (commands and actual output)

### 1. Syntax and selftest

```
$ bash -n ExecH9DeclaredBlocks.validator.sh && echo syntax-ok
syntax-ok
$ TMPDIR=$S bash ExecH9DeclaredBlocks.validator.sh --selftest
selftest detail=limb=positive rc=0 declared=2 pass=2 fail=0 exit=0
selftest detail=limb=mutant-m_tail rejected reason=tail-mismatch
selftest detail=limb=mutant-m_partial rejected reason=diff-mismatch
selftest detail=limb=mutant-m_deleted rejected reason=diff-mismatch
selftest detail=limb=mutant-m_unsafe rejected reason=unsafe-path
selftest detail=limb=mutant-m_absolute rejected reason=unsafe-path
selftest detail=limb=mutant-m_absent rejected reason=absent
selftest detail=limb=mutant-m_malformed rejected reason=malformed-line
selftest detail=limb=mutant-m_duplicate rejected reason=duplicate-path
selftest detail=limb=mutant-m_exceed rejected reason=lines-exceed-file
selftest detail=limb=mutant-m_symlink rejected reason=unsafe-path
selftest detail=limb=mutant-m_empty rejected reason=declared-0
selftest case=declared-blocks positive=pass mutants=11/11 verdict=pass
selftest cases=1 failures=0
RC=0
```

Mutant meanings: `m_tail` wrong digest for a correct tail; `m_partial` the
round-38 G1-H1 attack — the *suffix* (2 of 3 appended lines) hashed correctly,
rejected because `added=3 != 2`; `m_deleted` a ref commit that appends 3 lines
and deletes 1 (net `added=3 deleted=1`) with the tail hashed correctly;
`m_unsafe` `../outside.md`; `m_absolute` `/etc/passwd`; `m_absent` a path not in
the export; `m_malformed` two fields; `m_duplicate` the same path twice;
`m_exceed` `lines=99` on a 1-line file (correct digest of the clipped tail);
`m_symlink` a committed symlink to a file outside the export whose bytes hash to
the declared digest; `m_empty` an empty declared file (`declared=0` must be red).

Two selftest bugs were found and fixed by these runs: `awk 'END{…}' -- FILE`
silently produced an empty count on this host (every declaration then read
`lines-exceed-file`), and the duplicate limb matched only the first failing
reason on the line, so a rejected duplicate was scored as not rejected. Both
fixes are in the delivered bytes; the run above is the post-fix run.

### 2. Real lane, extract mode, positive

Declared body = the two files the freeze commit `5e985b7` added wholesale
(pure additions, so added==lines and deleted==0):

```
$ cat real/added.txt
.ufo/waves/round-40/claims.json 71 33a4602d3669aab178907082421fc72c3f2e938a06d902696ff4cb86cba2953f
.ufo/waves/round-40/c1-controls/before.txt 11 bde5ccec8961b3a5d6be3eb5145e9d384dfd809a4b4c082c56bd60bfd3ef937a
$ bash ExecH9DeclaredBlocks.validator.sh --declared real/added.txt \
    --base a7af2ce63bce153757d39bf66b366a96caf30c13 --ref 5e985b74075dd3813a63d7750966bf8abf693465
decl head mode=extract ref=5e985b74075dd3813a63d7750966bf8abf693465 base=a7af2ce63bce153757d39bf66b366a96caf30c13 lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin export=/fast/scratch/hyaku/kasegi-r40/ExecH9DeclaredBlocks/declared-blocks.c4d4FLqC/export
decl path=.ufo/waves/round-40/claims.json lines=71 tail=pass safe=pass diff=pass added=71 deleted=0 verdict=pass reason=-
decl path=.ufo/waves/round-40/c1-controls/before.txt lines=11 tail=pass safe=pass diff=pass added=11 deleted=0 verdict=pass reason=-
decl summary declared=2 pass=2 fail=0 exit=0
RC=0
```

The work dir named in `decl head` was removed on exit (`ls -d declared-blocks.*`
after the runs: `none`).

### 3. Real lane, export mode, positive

```
$ git --no-optional-locks -C "$LANE" archive --format=tar 5e985b7 | tar -x -C lane-export
$ bash ExecH9DeclaredBlocks.validator.sh --declared real/added.txt \
    --base a7af2ce63bce153757d39bf66b366a96caf30c13 --ref 5e985b74075dd3813a63d7750966bf8abf693465 \
    --export "$PWD/lane-export"
decl head mode=export ref=5e985b74075dd3813a63d7750966bf8abf693465 base=a7af2ce63bce153757d39bf66b366a96caf30c13 lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin export=/fast/scratch/hyaku/kasegi-r40/ExecH9DeclaredBlocks/lane-export
decl path=.ufo/waves/round-40/claims.json lines=71 tail=pass safe=pass diff=pass added=71 deleted=0 verdict=pass reason=-
decl path=.ufo/waves/round-40/c1-controls/before.txt lines=11 tail=pass safe=pass diff=pass added=11 deleted=0 verdict=pass reason=-
decl summary declared=2 pass=2 fail=0 exit=0
RC=0
```

### 4. Real lane, negative — declared tail that was not added between base and ref

```
$ P2=$(tail -n 2 PROVINCE.md | sha256sum | cut -d' ' -f1)   # fa2dd99f2791e022305fe1ee759a53ba514d7d4ef2e89a597cae8a41fe70d3d7
$ bash ExecH9DeclaredBlocks.validator.sh --declared real/province-not-added.txt \
    --base a7af2ce63bce153757d39bf66b366a96caf30c13 --ref 5e985b74075dd3813a63d7750966bf8abf693465
decl path=PROVINCE.md lines=2 tail=pass safe=fail diff=fail added=- deleted=- verdict=fail reason=diff-EMPTY
decl summary declared=1 pass=0 fail=1 exit=1
RC=1
```

### 5. Real lane, negative — tampered digest

```
$ bash ExecH9DeclaredBlocks.validator.sh --declared real/tampered.txt \
    --base a7af2ce63bce153757d39bf66b366a96caf30c13 --ref 5e985b74075dd3813a63d7750966bf8abf693465
decl path=.ufo/waves/round-40/claims.json lines=71 tail=fail safe=fail diff=fail added=- deleted=- verdict=fail reason=tail-mismatch
decl summary declared=1 pass=0 fail=1 exit=1
RC=1
```

### 6. Setup errors (exit 2, never a silent pass)

```
$ bash ExecH9DeclaredBlocks.validator.sh --base a7af2ce --ref 5e985b7
decl error missing --declared FILE
RC=2
$ bash ExecH9DeclaredBlocks.validator.sh --declared real/added.txt --base deadbeef --ref 5e985b7
decl error ref-not-in-lane: deadbeef
RC=2
$ bash ExecH9DeclaredBlocks.validator.sh --frobnicate
decl error unknown-argument: --frobnicate
RC=2
```

## Example blocks and their end-to-end proof

The block bytes are ScribeF23-2's landed text, copied byte-for-byte
(`cmp ExecH9DeclaredBlocks.province.txt ScribeF23.province.txt` clean,
`cmp ExecH9DeclaredBlocks.readme.txt ScribeF23.readme-row.txt` clean) so the
declarations the L1 needs are already derived from the final bytes.

`ExecH9DeclaredBlocks.province.txt` — 2 lines, 324 bytes: the separator blank
line and

```
[r40 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F23 — CycloneDX v1.7 vulnerabilities[].analysis (six analysis states, nine not-affected justifications, a repeatable response array and a per-version status) — admitted round 40; entry corpus/knowledge/cyclonedx-analysis-subtree.md (source S060)
```

`ExecH9DeclaredBlocks.readme.txt` — 28 lines, 2734 bytes: heading, paragraph,
coverage-map row, F23 frontier row (6 cells, one `| F23 |` row) and the
`[r40 amendment]` count line naming `23/23 admitted`; coverage rows carry 3
cells and no cell contains a `|`.

`ExecH9DeclaredBlocks.examples-declared.txt`:

```
PROVINCE.md 2 c445324c0f6d197f4c1b94f9509f86e3afd2af467d294dcb5bcac4e15c177408
corpus/README.md 28 d6a9f3c1306525f91ddad82afc96e47b77043208ce42a115a0290db43cc9e15b
```

The digests are real for the delivered bytes (`sha256sum` of each file above,
and each file is exactly `tail -n <lines>` after appending it to a file ending
in `\n`). Proof: a fixture git repo whose base commit is the content of
`git archive a7af2ce` (so `diff --numstat` reports what the lane will report),
the two files appended unchanged, a second commit, `git archive` of that commit,
and the validator run over it:

```
$ git -C "$L" archive --format=tar a7af2ce63bce153757d39bf66b366a96caf30c13 | tar -x -C "$D"
$ git -C "$D" init -q      # toplevel == realpath "$D": asserted
$ git -C "$D" diff --numstat <base> <ref> -- PROVINCE.md corpus/README.md
2	0	PROVINCE.md
28	0	corpus/README.md
$ bash ExecH9DeclaredBlocks.validator.sh \
    --declared ExecH9DeclaredBlocks.examples-declared.txt \
    --base ef3f7b6eb35fcd4092bc5201e2b30c9cf4af07c5 --ref a1dd28038647d05b97e01502cfbbe408b08f53d1 \
    --lane "$D" --export "$D.export"
decl head mode=export ref=a1dd28038647d05b97e01502cfbbe408b08f53d1 base=ef3f7b6eb35fcd4092bc5201e2b30c9cf4af07c5 lane=/fast/scratch/hyaku/kasegi-r40/ExecH9DeclaredBlocks/examples-fixture export=/fast/scratch/hyaku/kasegi-r40/ExecH9DeclaredBlocks/examples-fixture.export
decl path=PROVINCE.md lines=2 tail=pass safe=pass diff=pass added=2 deleted=0 verdict=pass reason=-
decl path=corpus/README.md lines=28 tail=pass safe=pass diff=pass added=28 deleted=0 verdict=pass reason=-
decl summary declared=2 pass=2 fail=0 exit=0
RC=0
```

Fixture surface after the append (matches the scribe's measured shape):

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md            -> 23
$ grep -c '^## Round-40 admission' corpus/README.md     -> 1
$ grep -c '^\[r40 Frontier amendment' PROVINCE.md        -> 1
$ wc -l PROVINCE.md corpus/README.md                    -> 160 / 542   (158+2, 514+28)
```

Suffix-only attack on the same 2-line block (declare the amendment line alone,
digest correct for `tail -n 1`) is rejected, so H9 cannot be satisfied by a
suffix of the append:

```
$ bash ExecH9DeclaredBlocks.validator.sh --declared partial.txt \
    --base ef3f7b6eb35fcd4092bc5201e2b30c9cf4af07c5 --ref a1dd28038647d05b97e01502cfbbe408b08f53d1 \
    --lane "$D" --export "$D.export"
decl path=PROVINCE.md lines=1 tail=pass safe=fail diff=fail added=2 deleted=0 verdict=fail reason=diff-mismatch
decl summary declared=1 pass=0 fail=1 exit=1
RC=1
```

Against the freeze commit, where the blocks are not yet landed, the same
declarations are red — they are only valid once the blocks are in the tree:

```
$ bash ExecH9DeclaredBlocks.validator.sh --declared ExecH9DeclaredBlocks.examples-declared.txt \
    --base a7af2ce63bce153757d39bf66b366a96caf30c13 --ref 5e985b74075dd3813a63d7750966bf8abf693465
decl path=PROVINCE.md lines=2 tail=fail safe=fail diff=fail added=- deleted=- verdict=fail reason=tail-mismatch
decl path=corpus/README.md lines=28 tail=fail safe=fail diff=fail added=- deleted=- verdict=fail reason=tail-mismatch
decl summary declared=2 pass=0 fail=2 exit=1
RC=1
```

## Integration notes for the L1 / H9

- Landing name: the suite's H9 limb can call this file directly, e.g.
  `bash "$R40_DIR/../instruments/declared-blocks-validate.sh" --declared
  "$tree/.ufo/waves/round-40/declared-blocks.txt" --base <base> --ref <ref>
  --export "$tree"`; the limb is green only when the summary carries
  `declared>=1`, `fail=0` and `exit=0` **and** the exit status is 0. Treat exit 2
  as red.
- Reconciliation status: done against ScribeF23-2's landed text (entry
  `corpus/knowledge/cyclonedx-analysis-subtree.md`, source `S060`), which is why
  the example files were refreshed to those bytes. If the L1 edits either block
  further, **both** `<lines>`/`<sha256>` in `examples-declared.txt` must be
  re-derived (`tail -n <lines> <path> | sha256sum`) — the delivered digests are
  only valid for the delivered bytes, and the `added == <lines>` clause is what
  catches a stale declaration.
- The fixture base is a re-commit of the `a7af2ce` tree, so its numstat line
  counts equal what the lane reports once the same bytes are appended to the
  same base content; if integration appends anything else to either front door
  in the same commit (any further correction line), the declared block grows and
  the declaration must be updated — that is exactly what the `added == <lines>`
  clause will catch.
- `declared-blocks.txt` is not created by this seat: the L1 owns
  `.ufo/waves/round-40/declared-blocks.txt` (H1's "suite+registry row present"
  and H9's declaration file are integration artefacts).

## No-harm / cleanup

- Writes: only the four deliverable files above plus this receipt in
  `.ufo/waves/round-40/wave1/`, and files under
  `/fast/scratch/hyaku/kasegi-r40/ExecH9DeclaredBlocks/` (removed before yield).
  The scribe's `ScribeF23.*` files were read and copied, never modified.
- Read-only elsewhere: `git --no-optional-locks rev-parse/archive/diff` against
  the lane, `git archive` piped to `tar -x` into scratch, and reads of
  `PROVINCE.md` / `corpus/README.md`. No `git add/commit/checkout/reset/stash`,
  no `jj`, no pacman, no writes to `~/.local/bin` or any PATH directory, no
  edits to `MANIFEST.json`, `templates/`, fleet `scripts/`, `.ufo/state/`.
- Fixture discipline: every fixture repo was created with
  `mktemp -d` + `git init -q` under this seat's scratch, and
  `git rev-parse --show-toplevel` was asserted equal to the fixture dir before
  the first commit; commits used inline `-c user.name/-c user.email`.
- Scratch: `/fast/scratch/hyaku/kasegi-r40/ExecH9DeclaredBlocks/` is removed
  before yield (receipt and deliverables were copied into the wave dir first),
  so no `kasegi-r40` scratch entry survives this seat (re-created for the
  refreshed-bytes run, then removed again). No `declared-blocks.*` work dir
  survived any run (checked after each).
- Lane worktree untouched by this seat: `git status --porcelain` lists only the
  round-40 wave scaffolding that predates this seat plus the untracked wave-1
  directory.

## Risks

- The validator is new code with no committed caller yet; its own evidence is
  the selftest (11/11 mutants rejected, positive accepted) plus the real-lane
  runs above. It has not been run inside `r40-closure.sh` (H9 is that seat's
  build), so the suite's own H9 grading line is unverified here.
- `realpath -m` and `tail -n` are GNU coreutils on this host; on a host without
  them the containment/whole-tail limbs degrade to `unsafe-path`/`tail-mismatch`
  (fail-closed), never to a false pass.
- A declared path containing whitespace is unsupported by the three-field line
  format; such a line is rejected as `malformed-line` rather than silently
  mis-parsed.
