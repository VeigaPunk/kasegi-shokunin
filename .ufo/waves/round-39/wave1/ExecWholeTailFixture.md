# ExecWholeTailFixture — G1' whole-tail fixture pack (round 39)

- Seat: `ExecWholeTailFixture`, executor (leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
- Axis: `depth:verifiability` (C1). Milestone: round-39.
- Base: `480b1a505a2dfc14a4f718d16d63808247214d0a`; claims freeze `dcd31701720a6a4929a32471a62011ed87103421`.
- Item: five synthetic export trees that pin the r39 G1 check (whole-tail declarations),
  with the exact expected `G1 payload=... closed=` line for each, and a README mapping
  fixture → verdict.
- Tools installed/upgraded: none (git 2.56.0, bash 5.3.20, python 3.13, GNU coreutils/grep/awk
  present; pacman not touched).
- Disk guard before work: green — `root 3% used, 125.2G free; /fast/scratch/hyaku 24% used, 610.7G free`.

## Deliverable

Path: `.ufo/waves/round-39/wave1/ExecWholeTailFixture.fixtures/` (42 files, 184 KB, no nested `.git`).

| file | lines | sha256 |
|---|---|---|
| `README.md` | 243 | `1e381548b22852fcde4cdc5b9e96d39a68a3a684c8abc6b6d2a35240d63fbdfc` |
| `g1-check.sh` | 231 | `f56e2d02591df9cdc246b056dc4757ca759f1e123ff3ead89dddc744bb1b7e86` |

Tree digest over the sorted `sha256sum` listing of all 42 files:
`8d8defea785891b4c7363443cae2e0263ccdfc1e73b85d28d1e273a9b91769a4`.

The pack is data plus one reference model:

- `<fixture>/base/` — pre-change front doors (commit 1 of the fixture repo).
- `<fixture>/head/` — the export tree the r39 commit would ship, carrying
  `.ufo/waves/round-39/declared-blocks.txt` (commit 2).
- `<fixture>/export/` — the same head bytes as `git archive` extracts them.
- `g1-check.sh` — reference implementation of the G1' model; builds the fixture repo in
  `--work` (asserts `git rev-parse --show-toplevel` equals that repo), exports the head,
  prints `export-sync=<0|1>` then the payload line; exit 0 only on `closed=1`.
- `README.md` — fixture-to-verdict map, the clause-by-clause model, the payload contract,
  the fence-walk probes and the clause-isolation mutants.

## Expected lines (verified, not authored)

Each line below is the actual stdout of
`bash g1-check.sh --fixture <fixture> --work <dir outside the lane>`, run from the landed
path `.ufo/waves/round-39/wave1/ExecWholeTailFixture.fixtures/`.

| fixture | clause pinned | expected line | verdict |
|---|---|---|---|
| `01-full-tail-green` | declared lines == added lines, fences closed, correction outside | `G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=1,pending-paths=0,tail=PROVINCE.md:3:3,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=0 closed=1` | GREEN |
| `02-partial-tail-red` | declared lines < added lines | `G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=0,pending-paths=0,tail=PROVINCE.md:2:3,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=0 closed=0` | RED |
| `03-inside-fence-correction-red` | `Correction (round 39)` inside an open fence | `G1 payload=province-correction=0,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=1,pending-paths=0,tail=PROVINCE.md:3:3,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=1 closed=0` | RED |
| `04-tilde-fence-green` | `~~~` fence closing a door the r38 walk calls OPEN | `G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=1,pending-paths=0,tail=PROVINCE.md:5:5,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=0 closed=1` | GREEN |
| `05-outside-path-red` | declared path not inside the export | `G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=0,pending-paths=1,tail=PROVINCE.md:3:3,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=0 closed=0` | RED |

`04` under the round-38 backtick-only walk is the documented false RED:

```
G1 payload=province-correction=0,readme-correction=1,province-fence=open,readme-fence=closed,declared-blocks=2,declared-ok=1,pending-paths=0,tail=PROVINCE.md:5:5,corpus/README.md:4:4,fence-model=backtick,corrections-inside=1 closed=0
```

(exit 1): the old walk ignores `~~~text`, opens on the literal ```` ```bash ```` line inside
the tilde block, finds no backtick closer, and wrongly rejects a closed door.

## Evidence

### Matrix from the landed pack

```
$ cd .ufo/waves/round-39/wave1/ExecWholeTailFixture.fixtures
$ for f in [0-9]*/; do f=${f%/}; out=$(bash g1-check.sh --fixture "$f" --work "$S/landed-w" 2>&1); rc=$?; ...
```

```
01-full-tail-green
export-sync=1
G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=1,pending-paths=0,tail=PROVINCE.md:3:3,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=0 closed=1
rc=0
02-partial-tail-red
export-sync=1
G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=0,pending-paths=0,tail=PROVINCE.md:2:3,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=0 closed=0
rc=1
03-inside-fence-correction-red
export-sync=1
G1 payload=province-correction=0,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=1,pending-paths=0,tail=PROVINCE.md:3:3,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=1 closed=0
rc=1
04-tilde-fence-green
export-sync=1
G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=1,pending-paths=0,tail=PROVINCE.md:5:5,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=0 closed=1
rc=0
05-outside-path-red
export-sync=1
G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=0,pending-paths=1,tail=PROVINCE.md:3:3,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=0 closed=0
rc=1
```

The README's five expected lines and its `04` old-model line were re-derived from the
document as a mechanical check (read the fenced `G1 payload=` line under each `###`
heading, run that fixture, compare string and exit status):

```
blocks: 5
PASS 01-full-tail-green
PASS 02-partial-tail-red
PASS 03-inside-fence-correction-red
PASS 04-tilde-fence-green
PASS 05-outside-path-red
PASS 04-old-model
ALL PASS
```

### Clause isolation (mutants of `01-full-tail-green`, built in scratch)

| mutant | change | output |
|---|---|---|
| `M1-hash-flip` | README declaration hash → 64 zeros | `...declared-blocks=1,declared-ok=0,...tail=corpus/README.md:0:4... closed=0` (rc 1) |
| `M2-no-correction` | `Correction (round 39)` → `Correcting (round 39)`, declaration re-hashed | `province-correction=0,...declared-blocks=2,declared-ok=1... closed=0` (rc 1) |
| `M3-door-undeclared` | README declaration line deleted | `...declared-blocks=1,declared-ok=0,...tail=corpus/README.md:0:4... closed=0` (rc 1) |

Exact `M1`/`M2` lines:

```
G1 payload=province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=1,declared-ok=0,pending-paths=0,tail=PROVINCE.md:3:3,corpus/README.md:0:4,fence-model=backtick+tilde,corrections-inside=0 closed=0
G1 payload=province-correction=0,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=1,pending-paths=0,tail=PROVINCE.md:3:3,corpus/README.md:4:4,fence-model=backtick+tilde,corrections-inside=0 closed=0
```

`M2` leaves `declared-ok=1`, so the correction limb is graded on its own rather than
riding on the byte binding.

### Fence-walk probes (`g1-check.sh --walk FILE`)

```
U1-longer-closer.md                      fence-model=backtick+tilde state=closed outside=0 inside=0 rc=0
U2-four-space-indent.md                  fence-model=backtick+tilde state=closed outside=0 inside=0 rc=0
U3-tilde-with-backtick-content.md        fence-model=backtick+tilde state=closed outside=0 inside=0 rc=0
U4-unclosed-backtick.md                  fence-model=backtick+tilde state=open outside=0 inside=0 rc=1
U5-closer-trailing-text.md               fence-model=backtick+tilde state=open outside=0 inside=0 rc=1
U6-char-mismatch.md                      fence-model=backtick+tilde state=open outside=0 inside=0 rc=1
U7-correction-outside-vs-inside.md       fence-model=backtick+tilde state=closed outside=1 inside=1 rc=0
```

Old model on the same tilde content: `--fence-model backtick` on `U3` prints
`fence-model=backtick state=open outside=0 inside=0` (rc 1), and on the `04` export door
prints `fence-model=backtick state=open outside=0 inside=1` (rc 1) against
`fence-model=backtick+tilde state=closed outside=1 inside=0` (rc 0) for the r39 model —
the same door, opposite verdicts, decided only by the fence model.

### Fixture integrity

- `head/` ↔ `export/` byte equality, every fixture: `equal` (5/5). A fixture edited without
  regenerating `export/` also fails the runtime `export-sync=1` guard.
- Pack digest before and after a full matrix run: `8d8defea…769a4` both times — the checker
  writes nothing into the fixture.
- Default work dir path (`TMPDIR` bound to scratch): one run, then
  `find "$TMPDIR" -mindepth 1 -maxdepth 1 | wc -l` → `0` (the `mktemp -d` is removed).
- `bash -n g1-check.sh` → `syntax ok`; `g1-check.sh --walk README.md` →
  `fence-model=backtick+tilde state=closed outside=0 inside=2` (the document's own fences
  balance; the two inside counts are the quoted tails it displays).

## Suite-integration notes (for the r39 author)

- Payload key order is fixed and one key per clause, so a mutant reopens one limb:
  `province-correction,readme-correction,province-fence,readme-fence,declared-blocks,
  declared-ok,pending-paths,tail,fence-model,corrections-inside`, then
  ` closed=<0|1>`. Closed = both corrections ≥1, both fences `closed`,
  `declared-ok=1`, `pending-paths=0`, `declared-blocks≥2`, `export-sync=1`.
- Selftest limb: call `g1-check.sh` on the exported fixture and require the exact line and
  exit status, or inline the model and build the fixture repo the same way. The diff base
  for clause 3 must be the fixture's `base/`, not the lane's round-39 base.
- The graded run must use `fence-model=backtick+tilde`; `--fence-model backtick` exists only
  to reproduce the r38 false RED and must never satisfy a graded case.
- `declared-blocks` counts declarations that pass shape, path existence and byte binding;
  a declaration failing only the added-line count leaves `declared-blocks` intact and sets
  `declared-ok=0` (see `02`). `05` keeps both door declarations valid and isolates
  `pending-paths=1`.

## Risks and limits

- The r39 claim states the correction clause as a fence-exclusion count with no required
  token, so the fixtures use plain `Correction (round 39): …` text. If the landed check adds
  a token requirement (as r38 required `L79-L152` / `misplaced`), the fixtures' correction
  lines must gain that token; the count/fence behaviour they pin is unchanged.
- The fixture corrections are synthetic prose, not the real round-39 front-door corrections;
  they grade the check, not the lane's own correction text.
- `g1-check.sh` is a reference model, not the landed instrument: the suite must reproduce
  its verdicts, and `01`/`04` acceptance plus `02`/`03`/`05` rejection is the acceptance
  contract for the G1 case line.
- The fence walk follows the contract's spelling (up to three leading spaces, info string,
  same-character closer with a run ≥ the opener and blanks only). It does not model
  indented-code-block interplay beyond that, or block quotes/list indentation.
- Fixtures carry no nested git repo by design, so landing them inside the lane cannot create
  a gitlink; the fixture repo is built in `--work` at run time.

## Scratch and cleanliness

- Scratch root `/fast/scratch/hyaku/kasegi-r39/ExecWholeTailFixture/` was used for the build,
  the mutant sweep, the fence probes and the work dirs; it is removed before this receipt
  is reported (verified absent).
- No write outside `.ufo/waves/round-39/wave1/…` in the lane, no fleet-root write, no
  mutating git command in any repo (the only commits were in the throwaway fixture repo
  under scratch, with `git rev-parse --show-toplevel` asserted first).

## Manifest (sha256, landed pack)

```
9851dc920b63e45da764eda7d0da94d5d438bdec3f1cc57c2ca1e86b1816ac8c  01-full-tail-green/base/corpus/README.md
704b9c1a096a1d7d6406de3a770a25157c37efb53a720d042a4b5f81b784eb8b  01-full-tail-green/base/PROVINCE.md
6b14719ec9c149fffa16ac4b57c4d535596d2342c204528aafdac9c567fc9efa  01-full-tail-green/export/corpus/README.md
bf5c685f35d3dde56a51cbb2199c940f428af13d801506c9bc9651f2a526efee  01-full-tail-green/export/PROVINCE.md
014a002d709a74a92a12e80b080ad3c09d2cae1fc0baea9cb8a6118c46bb6977  01-full-tail-green/export/.ufo/waves/round-39/declared-blocks.txt
6b14719ec9c149fffa16ac4b57c4d535596d2342c204528aafdac9c567fc9efa  01-full-tail-green/head/corpus/README.md
bf5c685f35d3dde56a51cbb2199c940f428af13d801506c9bc9651f2a526efee  01-full-tail-green/head/PROVINCE.md
014a002d709a74a92a12e80b080ad3c09d2cae1fc0baea9cb8a6118c46bb6977  01-full-tail-green/head/.ufo/waves/round-39/declared-blocks.txt
9851dc920b63e45da764eda7d0da94d5d438bdec3f1cc57c2ca1e86b1816ac8c  02-partial-tail-red/base/corpus/README.md
704b9c1a096a1d7d6406de3a770a25157c37efb53a720d042a4b5f81b784eb8b  02-partial-tail-red/base/PROVINCE.md
6b14719ec9c149fffa16ac4b57c4d535596d2342c204528aafdac9c567fc9efa  02-partial-tail-red/export/corpus/README.md
bf5c685f35d3dde56a51cbb2199c940f428af13d801506c9bc9651f2a526efee  02-partial-tail-red/export/PROVINCE.md
93c89fca3a0a1665c5b854f5a56cfbe6f96cb4aa9adc34b6c418965771750b62  02-partial-tail-red/export/.ufo/waves/round-39/declared-blocks.txt
6b14719ec9c149fffa16ac4b57c4d535596d2342c204528aafdac9c567fc9efa  02-partial-tail-red/head/corpus/README.md
bf5c685f35d3dde56a51cbb2199c940f428af13d801506c9bc9651f2a526efee  02-partial-tail-red/head/PROVINCE.md
93c89fca3a0a1665c5b854f5a56cfbe6f96cb4aa9adc34b6c418965771750b62  02-partial-tail-red/head/.ufo/waves/round-39/declared-blocks.txt
9851dc920b63e45da764eda7d0da94d5d438bdec3f1cc57c2ca1e86b1816ac8c  03-inside-fence-correction-red/base/corpus/README.md
704b9c1a096a1d7d6406de3a770a25157c37efb53a720d042a4b5f81b784eb8b  03-inside-fence-correction-red/base/PROVINCE.md
6b14719ec9c149fffa16ac4b57c4d535596d2342c204528aafdac9c567fc9efa  03-inside-fence-correction-red/export/corpus/README.md
ab025d1559a888c03f58bcc617f5bd31204cfb826033c3459d5ea197b216957e  03-inside-fence-correction-red/export/PROVINCE.md
ec6d036375c1bc3c07379f3c7fa5700700e5b16f2bbb34c1dd430cf9464953e2  03-inside-fence-correction-red/export/.ufo/waves/round-39/declared-blocks.txt
6b14719ec9c149fffa16ac4b57c4d535596d2342c204528aafdac9c567fc9efa  03-inside-fence-correction-red/head/corpus/README.md
ab025d1559a888c03f58bcc617f5bd31204cfb826033c3459d5ea197b216957e  03-inside-fence-correction-red/head/PROVINCE.md
ec6d036375c1bc3c07379f3c7fa5700700e5b16f2bbb34c1dd430cf9464953e2  03-inside-fence-correction-red/head/.ufo/waves/round-39/declared-blocks.txt
9851dc920b63e45da764eda7d0da94d5d438bdec3f1cc57c2ca1e86b1816ac8c  04-tilde-fence-green/base/corpus/README.md
704b9c1a096a1d7d6406de3a770a25157c37efb53a720d042a4b5f81b784eb8b  04-tilde-fence-green/base/PROVINCE.md
6b14719ec9c149fffa16ac4b57c4d535596d2342c204528aafdac9c567fc9efa  04-tilde-fence-green/export/corpus/README.md
3255e369b2b33125b46f10f7fc63e0c25a26a4ef5ee2d46d448dbc09411d4894  04-tilde-fence-green/export/PROVINCE.md
220b3609139bfda6afeec2f327fd2b3fb0b915bae5a4500c41fb448c4a3b1d31  04-tilde-fence-green/export/.ufo/waves/round-39/declared-blocks.txt
6b14719ec9c149fffa16ac4b57c4d535596d2342c204528aafdac9c567fc9efa  04-tilde-fence-green/head/corpus/README.md
3255e369b2b33125b46f10f7fc63e0c25a26a4ef5ee2d46d448dbc09411d4894  04-tilde-fence-green/head/PROVINCE.md
220b3609139bfda6afeec2f327fd2b3fb0b915bae5a4500c41fb448c4a3b1d31  04-tilde-fence-green/head/.ufo/waves/round-39/declared-blocks.txt
9851dc920b63e45da764eda7d0da94d5d438bdec3f1cc57c2ca1e86b1816ac8c  05-outside-path-red/base/corpus/README.md
704b9c1a096a1d7d6406de3a770a25157c37efb53a720d042a4b5f81b784eb8b  05-outside-path-red/base/PROVINCE.md
6b14719ec9c149fffa16ac4b57c4d535596d2342c204528aafdac9c567fc9efa  05-outside-path-red/export/corpus/README.md
bf5c685f35d3dde56a51cbb2199c940f428af13d801506c9bc9651f2a526efee  05-outside-path-red/export/PROVINCE.md
f70e1dc16da6833424a5c2d804ef0ffe1be9c7456f0755696f03bad9adde24d0  05-outside-path-red/export/.ufo/waves/round-39/declared-blocks.txt
6b14719ec9c149fffa16ac4b57c4d535596d2342c204528aafdac9c567fc9efa  05-outside-path-red/head/corpus/README.md
bf5c685f35d3dde56a51cbb2199c940f428af13d801506c9bc9651f2a526efee  05-outside-path-red/head/PROVINCE.md
f70e1dc16da6833424a5c2d804ef0ffe1be9c7456f0755696f03bad9adde24d0  05-outside-path-red/head/.ufo/waves/round-39/declared-blocks.txt
f56e2d02591df9cdc246b056dc4757ca759f1e123ff3ead89dddc744bb1b7e86  g1-check.sh
1e381548b22852fcde4cdc5b9e96d39a68a3a684c8abc6b6d2a35240d63fbdfc  README.md
```

## Blockers

None. All five fixtures plus the reference model and README are landed at the deliverable
path; the only open item is the suite author adopting the payload contract above.
