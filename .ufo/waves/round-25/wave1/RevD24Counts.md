# D24-2 — the round-24 snapshot assertion count, re-derived from committed bytes

seat: `L1Kasegi25.RevD24Counts` (reviewer, READ-ONLY)
lane: `kasegi-shokunin`, base revision `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`
measured: 2026-10-25, against the committed blobs of `d3614a2` (`git show HEAD:` digests match
the worktree byte-for-byte; `git status --porcelain` is empty for both artefact paths below).
I made no production edit. My only output is this file.

## 1. The one number

**76 assertions over 19 records.**

`corpus/source-snapshots/round-24/manifest.json` carries 76 quote assertions:
S001–S015 = 50, S032–S035 = 26. The committed receipt
`.ufo/waves/round-24/c1-counterA-manifest-receipt.txt` has 95 lines, which are
19 `:sha256 OK` lines plus 76 quote lines.

Canonical phrasing (recommend using it verbatim everywhere, so nobody re-derives 95 as a
count of assertions):

> `corpus/source-snapshots/round-24/manifest.json`: 19 records, 76 assertions
> (receipt: 95 `OK` lines = 19 `:sha256` + 76 quote lines).

Committed-bytes proof (all commands run from
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`):

```
$ sha256sum corpus/source-snapshots/round-24/manifest.json
c94c0ae95e1e7df0bb2ea78e853b38c60edb5b5204eed1298351daa336ce8923  corpus/source-snapshots/round-24/manifest.json
$ git show HEAD:corpus/source-snapshots/round-24/manifest.json | sha256sum
c94c0ae95e1e7df0bb2ea78e853b38c60edb5b5204eed1298351daa336ce8923  -
$ sha256sum .ufo/waves/round-24/c1-counterA-manifest-receipt.txt
4d5358a70a4eabab115e21fadc4f752e3f1108b6d6a13a35b16c7058c728d7c7  .ufo/waves/round-24/c1-counterA-manifest-receipt.txt
$ git show HEAD:.ufo/waves/round-24/c1-counterA-manifest-receipt.txt | sha256sum
4d5358a70a4eabab115e21fadc4f752e3f1108b6d6a13a35b16c7058c728d7c7  -
$ git status --porcelain corpus/source-snapshots/round-24/ .ufo/waves/round-24/c1-counterA-manifest-receipt.txt
(empty)
```

## 2. Derivations

### (a) Sum of `len(s['quotes'])` over the manifest — 76

```
$ python3 -c "import json;d=json.load(open('corpus/source-snapshots/round-24/manifest.json'));print(sum(len(s['quotes']) for s in d['sources']))"
76
```

Per-source breakdown (same load):

```
[('S001',4),('S002',7),('S003',3),('S004',3),('S005',5),('S006',3),('S007',3),('S008',3),
 ('S009',2),('S010',3),('S011',2),('S012',3),('S013',4),('S014',4),('S015',1),
 ('S032',6),('S033',8),('S034',6),('S035',6)]
sources: 19   S001-S015: 50   S032-S035: 26
```

### (b) Receipt OK lines minus sha lines — 76

```
$ wc -l < .ufo/waves/round-24/c1-counterA-manifest-receipt.txt
95
$ grep -c ':sha256 OK$' .ufo/waves/round-24/c1-counterA-manifest-receipt.txt
19
$ grep -c '^S[0-9]*:Q' .ufo/waves/round-24/c1-counterA-manifest-receipt.txt
76
$ grep -vc ' OK' .ufo/waves/round-24/c1-counterA-manifest-receipt.txt
(no output; exit 1 — there is no line that is not an OK line)
```

95 − 19 = **76**. (This is the exact place the report's "95 OK lines" phrasing seeds the
confusion: 95 is the *total* OK lines, sha lines included.)

### (c) Fresh run of the committed instrument, compared to the committed receipt — 76

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json > /tmp/revd24.out 2>&1
exit=0   lines=95   sha=19   quote=76
$ cmp -s .ufo/waves/round-24/c1-counterA-manifest-receipt.txt /tmp/revd24.out && echo CMP_IDENTICAL
CMP_IDENTICAL
```

The receipt is not a stale transcription: re-running the committed instrument on the committed
manifest reproduces it byte-for-byte, exit 0.

### (d) `jq` over the same manifest — 76

```
$ jq '[.sources[].quotes[]]|length' corpus/source-snapshots/round-24/manifest.json
76
```

### (e) Literal quote-id occurrence count — 76

```
$ grep -c '"id": "Q' corpus/source-snapshots/round-24/manifest.json
76
```

### (f) Per-source cross-tab, receipt Q-lines vs manifest `len(quotes)` — 0 mismatches

```
sources in manifest 19   sources in receipt 19   sha lines 19
mismatches []
receipt quote total 76   manifest total 76
```

Four independent surfaces (JSON object count via Python, JSON object count via jq, literal id
count, instrument output) plus one cross-tab agree on **76**. No derivation yields 62 or 77 from
the committed bytes.

## 3. Where the two wrong numbers came from

### 77 — the wave-1 *candidate* manifest, not the landed one

`.ufo/waves/round-24/wave1/CaptureTool.md` measured a candidate manifest assembled outside the
lane, at `/tmp/r24-final`:

- `:184` — "Total 51 assertions over 15 snapshots" (its own table `:168-182` sums to 51:
  `4+7+3+3+5+3+3+3+2+3+2+3+4+4+2`), with **S015 = 2** in that table (`:182`).
- `:195` — "… 77 quote lines "OK count=1", 19 "…:sha256 OK" … exit=0"
- `:199` — "96 lines (19 sha256 + 77 quotes) exit=0"
- `:237` — "receipt should read `occurrences=1` for all 77 assertions"

51 + 26 = **77**, over 96 lines. The landed manifest carries **S015 = 1**, i.e. exactly one
assertion fewer: 50 + 26 = **76**, over 95 lines. The `77` in the lesson/scorecard/log is the
candidate's count copied forward; the candidate directory no longer exists (nothing under `/tmp`),
so 77 is unreachable from committed bytes.

### 62 — unreproducible; no committed or wave-1 artefact yields it

Tested candidates that do **not** equal 62: distinct quote text = 70, distinct `location` values =
30, `len(quotes)` = 76, records = 19, S001–S015 = 50, S001–S015 + S032 = 56. The only arithmetic
that reaches 62 with cited operands is 51 + 11: the candidate's 51 (`CaptureTool.md:184`) plus the
11-assertion S032-only set that `EntryRoE.md:111` ("`manifest.json` lists S032 with the 11
assertions below") and `:139` ("The entry's 11 assertions, in manifest form…") describe for the
fixture stage. **[INFERENCE]** — that is an intermediate draft count, not a measurement; no
artefact states 62, so 62 must be replaced, not explained.

## 4. Per-file table — which file says what

| path:line | value as it reads now | verdict |
|---|---|---|
| `corpus/instruments/README.md:178-184` (worktree, **uncommitted**, sha256 `3329202fcf16a40887eabecf7d7b754835ea0aa6c5362df0dfe2f9d0bdd6fe32`, mtime 2026-10-25 05:28:42 -0300) | "19 captured records, **76** assertions" + the counting command + "receipt's 95 `OK` lines are 19 `:sha256` plus these 76" | **correct**, already fixed by another seat during this run (I verified the inserted command prints `76`) |
| `corpus/instruments/README.md:174` at base `b49948f` (committed) | "19 captured records, **62**" | **wrong** — superseded by the worktree edit; the committed base still says 62 until the L1 commits |
| `corpus/lessons/round-24.md:77` | "`source-recheck.py` exits 0 over 19 records / **77** assertions." | **wrong** |
| `SCORECARD.md:510` (source-capture row, live evidence table) | "(19 records, **77** assertions, exit 0)" | **wrong** |
| `LOG.md:1213` (round-24 changelog entry) | "(19 captures, **77** assertions, `source-recheck.py` exit 0)" | **wrong**, but historical log → R9 says append, do not rewrite |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-24/kasegi.md:31-32` | "19 records, **76** assertions (S001–S015 plus S032–S035)" | **correct** (report is historical; stays) |
| `.ufo/reports/round-24/kasegi.md:34` | "(`c1-counterA-manifest-receipt.txt`, **95 OK lines**)" | correct but sha-inclusive; historical, stays |
| `.ufo/waves/round-24/wave1/CaptureTool.md:184,195,199,237` | 51 / 77 / 96 lines | candidate-stage record, historical, stays (it is the *evidence* for where 77 came from) |

No `corpus/knowledge/*.md` entry states an assertion count (checked: the only `assertion` hits at
`ai-assisted-finding-validation.md:8` and `ufo-workspaces.md:182` are unrelated prose).

`QUALITY.md:51` (R9) governs the disposition: *"A numerical erratum names its base and
changed-file scope; line pointers are re-opened against the cited revision. Append the correction
to historical lessons/logs rather than silently rewriting their filed assertions."*

## 5. Exact replacement text

### 5.1 `corpus/instruments/README.md` — already applied in the worktree; fallback block below

The sibling edit at `:178-184` is correct and verified. If that edit is dropped before landing,
replace committed lines **174-178** (base `b49948f`) with exactly these seven lines (this is
byte-identical in substance to what is in the worktree now; the command prints `76`):

```
- `corpus/source-snapshots/round-24/manifest.json` — 19 captured records, 76
  assertions: S001–S015 (the five round-22 Frontier entries) and S032–S035 (the
  round-24 F09 admissions). Every assertion was measured exactly-once in its own
  capture; the checker now prints `occurrences=N` and verifies a declared `anchor`
  line for non-unique quotes (QUALITY Q9). Count it from the lane root:
  `python3 -c "import json;d=json.load(open('corpus/source-snapshots/round-24/manifest.json'));print(sum(len(s['quotes']) for s in d['sources']))"`
  → `76`, and the round-24 receipt's 95 `OK` lines are 19 `:sha256` plus these 76.
```

(The 147-column command line is in family: `README.md` already carries a 599-column line at `:14`,
and splitting the command would break copy-paste.)

### 5.2 `corpus/lessons/round-24.md:77` — exact replacement sentence

Replace line 77 with exactly:

```
it was written; `source-recheck.py` exits 0 over 19 records / 76 assertions.
```

(76 columns, inside the file's 78–82-column wrap; lines 74–76 are unchanged.)

**R9-conformant alternative (recommended for a historical lesson).** Keep line 77 verbatim and
append after line 211 (file end), so the filed assertion stays and the correction is filed with its
base and changed-file scope:

```
## Erratum (filed round 25, D24-2)

`corpus/lessons/round-24.md:77` filed `19 records / 77 assertions` for
`corpus/source-snapshots/round-24/manifest.json`. Measured on the committed bytes at base
`b49948f`: **76** assertions over 19 records (S001–S015: 50, S032–S035: 26), and the
committed receipt is 95 `OK` lines = 19 `:sha256` + 76 quote lines. `77` is the wave-1
candidate manifest's count (`.ufo/waves/round-24/wave1/CaptureTool.md:184,195,199`:
51 + 26 = 77 over 96 lines); the landed manifest carries one fewer S015 assertion.
Count it: `python3 -c "import json;d=json.load(open('corpus/source-snapshots/round-24/manifest.json'));print(sum(len(s['quotes']) for s in d['sources']))"` → `76`.
Changed-file scope: this statement (`corpus/lessons/round-24.md:77`),
`corpus/instruments/README.md:174` (62 → 76), `SCORECARD.md:510`, `LOG.md:1213`.
```

### 5.3 `SCORECARD.md:510` — exact cell replacement

In the source-capture row, replace the substring

```
(19 records, 77 assertions, exit 0)
```

with

```
(19 records, 76 assertions, exit 0)
```

The row describes the *current* committed manifest rather than a past-revision measurement, so a
direct edit is appropriate (the round-23 erratum precedent at `SCORECARD.md:265` covers filed
measurements, not this pointer).

### 5.4 `LOG.md:1213` — historical; erratum unless the L1 rules LOG living

If LOG is treated as a living log, the exact replacement for the substring

```
(19 captures, 77 assertions, `source-recheck.py` exit 0)
```

is

```
(19 captures, 76 assertions, `source-recheck.py` exit 0)
```

Otherwise (R9 default) leave `:1213` verbatim and carry the erratum from §5.2 in the round-25 LOG
entry — one sentence is enough:

```
- **D24-2 erratum.** `LOG.md:1213` filed "77 assertions" for the round-24 manifest; the committed
  manifest at `d3614a2` holds 76 (S001–S015: 50, S032–S035: 26) and the receipt's 95 `OK` lines
  are 19 `:sha256` + 76 quote lines. 77 was the wave-1 candidate count (`CaptureTool.md:184,195,199`).
```

### 5.5 Round-24 report — no change

`.ufo/reports/round-24/kasegi.md:31-32` already says 76 and is historical. `:34`'s "95 OK lines"
is correct as a total; leave it, but never quote it as an assertion count (use §1's phrasing).

## 6. Out-of-scope observation (one line, for the L1 to route)

`/home/vgpnk/Projects/shokunin/.ufo/reports/round-24/kasegi.md:29` places `capture-log.txt` in
`kasegi-shokunin/corpus/source-snapshots/round-24/`; that path does not exist — the file is
`.ufo/waves/round-24/capture-log.txt` (3003 B, 2026-10-25 04:15). Evidence:
`ls corpus/source-snapshots/round-24/capture-log.txt` → "No such file or directory";
`ls -l .ufo/waves/round-24/capture-log.txt` → exists. Not D24-2; flagged only because it sits in
the same count/receipt paragraph.

## 7. Residual risk and verification gaps

- **Concurrent edits.** `corpus/instruments/README.md` was rewritten by another seat *while I was
  measuring*: base `b49948f:174` read `62`, an intermediate worktree state read `76` with the
  command inline at `:178-181`, and the state I verified last is `:178-184`, sha256
  `3329202f…`. Everything in §1–§3 was measured against the committed manifest and receipt, which
  were never touched (`git status` empty for both). Re-hash the README at landing; if it differs
  from `3329202f…`, use the §5.1 block.
- **77's provenance** rests on the wave-1 candidate report's own numbers; the candidate manifest
  (`/tmp/r24-final`) is gone, so I could not re-measure 77 directly. The landed-vs-candidate delta
  is pinned to one assertion (S015: 2 → 1), which reconciles 51+26=77/96 lines with 50+26=76/95
  lines exactly.
- **62's provenance is inference only** (§3); no artefact states it.
- I did not re-run the round-25 mutant/pristine copies under
  `.ufo/waves/round-25/wave1/mut-skip/` and `rev-independent/base-tree/` (out of scope; they
  carry the same 77 text at their own `round-24.md:77`).
- No tool installed or upgraded for this item.
