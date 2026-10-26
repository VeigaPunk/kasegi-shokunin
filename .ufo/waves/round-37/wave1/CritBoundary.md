# CritBoundary — boundary conditions of the C2 counters (round 37)

Seat: CritBoundary (critic, leaf — no subagent dispatch used).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (the only lane repo; no writes outside this receipt and the scratch dir).
Base commit `b56a41680cefd391868c1c370dc063c69d827e7d`; claims-freeze commit `224df74db2a46d627ae1475a72ca48796bbd177c`; lane HEAD observed while working: `b362068195d5489aa94b31e6ec8f880c367e0ba0`.
Axes: coverage (primary), depth:verifiability (the counters' fail-closed shape).

Scope of this receipt: the six assigned boundary classes — empty/malformed frontier rows, `S054` row with `NF!=13`, capture with zero lines or a wrong sha256, the frontier harness on a tree missing the F20 entry, census over an indented `S054` row, and the audit with a 49th unexpected file — plus the two adjacent boundaries each probe exposed. Every verdict below is an executed transcript from scratch mirrors, never a reading of the source alone.

**Head note.** `corpus/instruments/r37-closure.sh` is absent at the HEAD I observed (`ls` → No such file or directory), so the C1 E10–E14 checks are not probeable from this seat; every row below concerns the committed C2-era counters (`frontier-recheck-count.py`, `recheck-audit.py`, `source-recheck.py`, `capture-binding-check.py`, fleet `scripts/sources-census.sh`).

## 0. Baselines re-measured before probing (lane root, read-only)

```text
python3 corpus/instruments/frontier-recheck-count.py        -> entries=22 pass=22 exit=0
python3 corpus/instruments/recheck-audit.py --quiet          -> strict pass=48/48 ... expect=present expected=48 missing=0 unexpected=0 exit=0
python3 corpus/instruments/capture-binding-check.py          -> records=43 bound=43 unbound=0 exit=0
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
                                                             -> kasegi W04 S028, kasegi W04 S029, kasegi ok ... exit=0
census row count on the base registry mirror                 -> rows=53
```

These are the pre-states the frozen C2 claim measures against (22/22, 48/48+expected 48, 43/43, 53 rows, census exit 0).

Fixtures were built from `git archive b56a4168…` (`$S/export`), never from a mutated lane: every README mirror is `export/corpus/README.md` plus one appended/inserted row; every `SOURCES.md` mirror is `export/corpus/SOURCES.md` with the `S054` row inserted immediately before `## Paths` (line 61) unless a variant says otherwise; `corpus/knowledge` is a symlink farm to the lane (read-only) plus the one stub used-by file where a row had to satisfy E11; capture fixtures are byte files + `manifest.json` written in scratch. `S = /fast/scratch/hyaku/kasegi-r37/CritBoundary`.

## 1. Boundary test table

`FC` = fails closed (red or exit≠0 on the hollow input). `FO` = fails open (green while the target state is not actually present). `DIV` = two counters disagree about the same bytes.

| # | boundary | counter | prediction | observed | verdict |
|---|---|---|---|---|---|
| 1 | F20 row with an **empty entry cell** (`\| F20 \| … \| admitted \|  \| S054 \| next \|`) on an otherwise-passing tree | harness | red | row unmatched by `FRONTIER_ROW`; `entries=22 pass=22 exit=0` | **FO** (row invisible; only the claim literal `23` catches it) |
| 2 | F20 row with a whitespace-only entry cell, a backticks-only cell (`` ` ` ``), a 3-cell truncated row, or an **empty status cell** | harness | red | each: `entries=22 pass=22 exit=0` | **FO** |
| 3 | F20 row indented 2 spaces, entry cell naming an existing file | harness | red | `FRONTIER_ROW` is `^\|`-anchored; `entries=22 pass=22 exit=0` | **FO** |
| 4 | F20 row present, entry file **absent** | harness | red | `FAIL F20 knowledge/ssvc-…md ids=- exit=- problems=missing-entry`; `entries=23 pass=22 exit=1` | **FC** (named row+path, no traceback) |
| 5 | F20 entry cell names a **directory** (`knowledge`) | harness | red | `problems=missing-entry`; `entries=23 pass=22 exit=1` | **FC** |
| 6 | harness where **every** row is malformed (zero parsed rows) | harness | red | `entries=0 pass=0 exit=1` (`not records` limb) | **FC** (total collapse only) |
| 7 | `S054` row **`NF=12`** (used-by column dropped) inside `## Registry` | census | E01, red | `file E01 S054 fields=10`; validate exit=1 | **FC** |
| 8 | `S054` row **`NF=14`** (extra `\|` inside teaches) inside `## Registry` | census | E01, red | `file E01 S054 fields=12`; validate exit=1 | **FC** |
| 9 | `S054` row **appended at EOF** (after `## Registry changes`, outside `## Registry`) | census | red | `file E12 S054 row outside Registry section`; exit=1; census `rows=53` (row not counted) | **FC** |
| 10 | `S054` row **indented 2 spaces** (otherwise valid) | census + binding | agree → red | census: exit=0, `rows=54`, W04 S028/S029 only; binding: `FAIL rule=no-row record=S054`, `records=44 bound=43 unbound=1 exit=1` | **DIV** — census parses 0–3 leading spaces, binding's `ROW_RE` is column-0; net **FC** via binding |
| 11 | `S054` row **indented 4 spaces** | census + binding | red | census: exit=0, `rows=53`, no finding (skipped as code before E12); binding: `no-row`, exit=1 | **DIV** — census alone **FO**; net **FC** via binding |
| 12 | capture **0 bytes** (or a single `\n`) with the matching empty/short sha256 and a real quote | source-recheck + binding | red | source-recheck: `S054:sha256 OK` then `Q1 MISMATCH reason=quote-not-found`, exit=1; binding: `records=44 bound=44 unbound=0 exit=0` | **FC** via source-recheck; binding blind to an empty capture |
| 13 | capture **wrong sha256** (declared ≠ bytes, incl. 64×`0`) | source-recheck | red | `S054:sha256 MISMATCH expected=… actual=…`, exit=1 | **FC** |
| 14 | manifest `sha256` **malformed / uppercase** (`NOTAHASH`, `A…A`) | source-recheck | red | `UNAVAILABLE reason=invalid-sha256` (exit 2) | **FC** |
| 15 | manifest **declares `lines: 0`** over a real capture whose sha256 matches | source-recheck (whole chain) | red | `S054:sha256 OK` + `Q1 OK occurrences=1 anchor=1-ok`, exit=0 | **FO** — no instrument reads `lines`/`fetched_bytes`; only the byte digest binds |
| 16 | harness tree **missing the F20 row entirely** | harness | red | `entries=22 pass=22 exit=0` | **FO** (identical signature to rows 1–3) |
| 17 | audit with a **49th knowledge file** carrying a valid `recheck:` line | audit | red | `strict pass=49/49`, `lines=49 total=49`, `expect=present expected=48 … unexpected=1 exit=1` | **FC** |
| 18 | audit with a **49th file with no `recheck:` line** | audit | red | `lines=48 total=49`, `complete=False`, `unexpected=1`, exit=1 (two limbs) | **FC** |
| 19 | audit with a 49th file while the **expected list is absent** (`--expect <missing path>`, or the committed `knowledge-expected.txt` removed) | audit | red | `expect=absent expected=0 missing=0 unexpected=0 exit=0` with 49 entries audited | **FO** |
| 20 | 49th knowledge path that is a **directory** named `*.md` | audit | red | uncaught `IsADirectoryError` traceback, exit=1 | **FC** by status, not by named verdict |

Count: 20 boundaries — 13 fail closed (rows 4–9, 12–14, 17, 18, 20), 6 fail open at the counter that owns the boundary (rows 1–3, 15, 16, 19), and 2 divergent-parser rows (10, 11) that are net fail-closed only because a second counter disagrees with census.

## 2. Row-by-row evidence and the smallest safe correction

### Rows 1–3, 6, 16 — the harness cannot see a row it does not parse

`read_frontier` keeps only lines matching

```python
FRONTIER_ROW = re.compile(r"^\|\s*(F\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`?([^|`]+?)`?\s*\|")
```

and keeps only rows whose status cell is exactly `admitted`. Four independent shapes therefore leave the denominator without a single problem line:

- empty or whitespace-only entry cell (group 4 requires ≥1 non-`|`/non-backtick char);
- backticks-only entry cell;
- a row truncated before the 4th pipe;
- status cell empty or `admitted (r37)` (the cell must equal `admitted`);
- any row indented by ≥1 space (`^|` anchor);
- no F20 row at all — indistinguishable from the above.

Executed, on a mirror of the base `corpus/README.md` whose other 22 entries all pass:

```text
empty entry cell             entries=22 pass=22 exit=0
whitespace-only entry cell   entries=22 pass=22 exit=0
backticks-only entry cell    entries=22 pass=22 exit=0
3-cell truncated row         entries=22 pass=22 exit=0
empty status cell            entries=22 pass=22 exit=0
2-space-indented row         entries=22 pass=22 exit=0
```

The instrument *is* fail-closed against total collapse (`entries=0 pass=0 exit=1`) and against a resolved-but-unusable row:

```text
FAIL     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=-  exit=-  problems=missing-entry
entries=23 pass=22 exit=1
```

(absent file and directory-as-entry both produce that line; `entry_contract` returns `None` and the caller prints the row id and path, never a traceback).

**Assessment.** This is not a fixable defect in the frozen instrument — it is the counter's contract: the harness counts what it can parse, so a shape it cannot parse leaves the set instead of reddening it. The only discriminator between “F20 row malformed” and “F20 row absent” and “F20 admitted” is the printed integer.

**Smallest safe correction.** None to the instrument this round. The C2 counting command must quote the whole summary line `entries=23 pass=23 exit=0` (and the `PASS F20 … ids=S054` line) rather than the exit status alone; the frozen claim already names `entries=23`, so a malformed row surfaces as `22`. Rewriting the harness to compare admitted rows against parsed rows is an instrument change and belongs to a later round, not to this cutover.

### Rows 7–8 — census rejects `NF!=13` at the field count, and stops validating that row

`awk -F'|'` sees `NF=13` for an 11-cell row. A dropped used-by column and an embedded `|` both red the registry:

```text
file	E01	S054 fields=10        (validate exit=1)
file	E01	S054 fields=12        (validate exit=1)
```

The `next` after E01 means the malformed row's kind/tier/status/opened/recheck cells are not checked — a malformed row produces exactly one finding, which is enough for the exit status.

**Smallest safe correction.** None; this is the contract. (A row appended at EOF is a different failure, row 9.)

### Row 9 — E12 makes the append position load-bearing

`S054` appended after the last section (the R6-shaped end-of-file append that other corpus files use) is *not* a registry row to the census:

```text
file	E12	S054 row outside Registry section       (validate exit=1)
file	rows	53                                      (row not counted)
```

Inserted before `## Paths` (line 61), the same bytes give:

```text
file	W04	S028 duplicate url …
file	W04	S029 duplicate url …
file	ok	<mirror>/corpus/SOURCES.md              (validate exit=0)
file	rows	54
```

**Smallest safe correction (integration rule).** The `S054` row must land *inside* the `## Registry` table (after `S053`, which is line 59, before the blank line and `## Paths` at line 61). Appending at EOF satisfies none of the C2 row claims and turns census red.

### Rows 10–11 — census and binding disagree about indentation

Same two bytes, two answers:

```text
S054 row indented 2 spaces, otherwise valid
  census  validate --file -> file ok, exit 0; census rows=54; only W04 S028/S029
  binding --root mirror   -> FAIL rule=no-row record=S054 dir=round-37
                             records=44 bound=43 unbound=1 exit=1

S054 row indented 4 spaces
  census  validate --file -> file ok, exit 0; census rows=53  (no E01/E12: skipped as code)
  binding --root mirror   -> FAIL rule=no-row record=S054 ; records=44 bound=43 unbound=1 exit=1
```

`capture-binding-check.py` uses `ROW_RE = re.compile(r"^\|\s*(S\d{3,})\s*\|")` (column 0) while `sources-census.sh` deliberately accepts 0–3 leading spaces; the frontier harness is column-0 like binding. So an indented row is *claim-satisfying for census* and *unbound for binding* at the same time.

**Assessment.** Net fail-closed for the C2 claim as frozen, because binding's `unbound=0` target is one of the claim's literals. But the census line alone (`exit 0`, W04 only, `rows=54`) cannot distinguish an indented row from a correctly placed one — and at 4 spaces census is fully silent while `rows` drops back to 53.

**Smallest safe correction.** Land the row at column 0. If indentation is ever intended, the two parsers must be unified in a later round; do not “fix” it by relaxing binding now (that would remove the only limb that catches the 4-space case).

### Rows 12–14 — a hollow capture is caught by source-recheck, not by binding

A zero-byte capture with the empty-string digest, a valid URL, provenance and a real quote:

```text
binding --root mirror   -> records=44 bound=44 unbound=0 exit=0     (blind)
source-recheck --source S054 -> S054:sha256 OK
                                S054:Q1 MISMATCH reason=quote-not-found   exit=1
```

Wrong digest and malformed digest:

```text
sha256 64×'0' vs content -> S054:sha256 MISMATCH expected=000… actual=a992…  exit=1
sha256 "NOTAHASH"        -> UNAVAILABLE reason=invalid-sha256                 exit=2
sha256 64×'A' (uppercase)-> UNAVAILABLE reason=invalid-sha256                 exit=2
```

**Assessment.** Binding proves *provenance and URL*, not *content*; the content limb is the entry's own `recheck:` line (and therefore the harness, which executes it). A zero-line capture is fail-closed only through that path, and only because the manifest's quotes must be found in the bytes.

**Smallest safe correction.** None; keep the S054 `recheck:` line in the entry and keep the entry's recheck ids equal to the declared set, because that line is what makes `bound=44` mean “bound to a capture that still holds the entry's quotes”.

### Row 15 — the manifest's `lines` (and `fetched_bytes`) are unenforced

A manifest that declares `"lines": 0` over a real, digest-matching capture passes:

```text
S054:sha256 OK
S054:Q1 OK occurrences=1 anchor=1-ok        exit=0
```

`grep -n 'lines' corpus/instruments/*.py` shows no instrument reading `sources[].lines` (the only `lines` keys are `recheck-audit`'s own receipt counters). The same is true of `fetched_bytes`/`snapshot_bytes`: no counter consumes them.

**Assessment.** Fail-open, but bounded: the C2 claim's capture is bound by sha256 (checked) and by the entry's quotes (checked), so a false line count cannot make a hollow capture pass; it can only make a *provenance note* wrong. Treat the manifest's line/byte counts as documentation, never as measured evidence.

**Smallest safe correction.** None this round. Do not let any receipt claim “lines verified”; write “sha256 verified, line count recorded”.

### Row 19 — the audit's expected-list equality is opt-in by file presence

With a 49th good entry and the committed list present, the audit is correctly red (`unexpected=1`, exit=1 — rows 17–18). With the same tree and the list *absent*, both by `--expect <nonexistent>` and by deleting `corpus/instruments/knowledge-expected.txt`:

```text
lines=49 total=49 pass=49 … exit=0
expect=absent expected=0 missing=0 unexpected=0 exit=0
```

The code drops the check silently: `elif not os.path.exists(expect_path): expect_path = None` and `expect_ok = not expect_active or (…)`.

**Assessment.** This is the one place where a *hollow* 49th entry can be green. It is reachable only by the caller composing the command, not by the base tree (the list is committed at base and the default path resolves), so the frozen counting command `python3 corpus/instruments/recheck-audit.py --quiet` is safe as written. But `know-expected.txt`-deleted is indistinguishable from `expect=absent` in the receipt.

**Smallest safe correction.** Quote the `expect=present expected=49 missing=0 unexpected=0` line in the C2 measurement, and do not pass `--expect` at all (the default path is the committed list). A later round could make an explicitly-passed-but-missing `--expect` an error; changing it now is an instrument rewrite outside this cutover.

### Row 20 — a directory named `*.md` reds the audit by crashing

```text
Traceback (most recent call last):
  …
IsADirectoryError: [Errno 21] Is a directory: '…/corpus/knowledge/unexpected.md'
exit=1
```

Fail-closed by exit status, but the receipt carries no named verdict for it. Not reachable from the planned integration (a file is written, not a directory); recorded for completeness only.

## 3. Cross-counter safety net

The counters are not redundant: each hollow state below is caught by exactly one limb, and greens everywhere else.

| hollow state | caught by | green elsewhere |
|---|---|---|
| F20 row malformed / absent / indented | the claim's literal `entries=23` (harness stays green at 22/22) | harness exit 0, census (never reads README) |
| F20 row present, entry missing/unusable | harness `missing-entry` (exit 1) | — |
| `S054` row NF≠13 / outside Registry | census E01 / E12 | binding (a NF≠13 row still parses on `\|`: `records=44 bound=44 unbound=0 exit=0`; see note) |
| `S054` row indented ≥1 space | binding `no-row` | census green at 0–3 spaces; fully silent at ≥4 |
| capture empty / digest mismatch | source-recheck (entry recheck line → harness) | binding green (`bound=44`) |
| fake `lines` in the manifest | nothing | every counter green |
| 49th knowledge entry | audit `unexpected=` (list present) | audit green when the list is absent |
| 49th entry without a recheck line | audit `complete=False` + `unexpected=` | — |

Note on the NF≠13 row: `capture-binding-check` splits on `|` and takes `parts[1]`/`parts[STATUS_COLUMN]`, so a row with 10 or 12 cells still parses as a row and can still bind a record (the URL sits in the same cell in both mutants). The census is the only counter that enforces columnarity — which is why the row must be validated by `sources-census.sh`, not only by binding.

## 4. What the integration must actually print

For the frozen C2 claim to be *measured* rather than merely plausible, the after-state transcript must contain, verbatim:

1. `PASS     F20  knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054` and `entries=23 pass=23 exit=0` — not just exit 0 (a 22/22 run is green and one row short).
2. `file	rows	54` from census with only `W04 S028`/`W04 S029`, from a row placed at column 0 inside `## Registry` (lines 3–60), never at EOF.
3. `records=44 bound=44 unbound=0` (43 base + S054) — an indented or mis-placed row prints `bound=43 unbound=1`.
4. `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054` → exit 0 with `S054:sha256 OK` and four `OK occurrences=1` lines — this, not binding, is what says the capture has content.
5. `expect=present expected=49 missing=0 unexpected=0` — with the default expected path (no `--expect` override), because the list-absent form is green.
6. Do not cite the manifest's `lines`/`fetched_bytes` as verified; they are unenforced documentation.

## 5. Limits of this receipt

- The probes ran against the base export (`b56a4168`) and the live instruments at `b3620681`; the final round-37 lane head does not exist yet, and `r37-closure.sh` is not committed at the head I observed, so no C1 E-check boundary is claimed here.
- The census mirror reuses the base registry (53 rows) so `rows=54` is the expected after-value; the real after-state must also survive E11, which this receipt satisfied with a stub used-by file — the landed entry file is the real used-by target.
- `frontier-recheck-count` was driven with `--root <mirror>` while the entries' `recheck:` lines `cd` to the real lane (their absolute lane path). That is the instrument's documented execution model (the line is executed from the audited root; the `cd` is part of the line), and the only thing a mirror changes is which `README.md` and which entry files the row contract is read from — which is exactly the row-shape input under test.
- The harness runs for rows 1–6 were each ~5 s; no counter was run with `--json` on a mutated tree except where quoted.

## 6. Scope, tooling, scratch

- Writes: this receipt only. All fixtures and transcripts under `/fast/scratch/hyaku/kasegi-r37/CritBoundary/` (removed after this receipt landed). No lane repo, fleet repo, sibling lane, shokuknow or `~/Projects/*` file was written; no mutating git/jj command was run (only `git archive`, `rev-parse`, `status`, `ls`, `grep`).
- No tools installed or upgraded; no pacman invocation (transactions paused host-wide). `python3`, `bash`, `awk`/`gawk` from the host sufficed.
- Scratch was bound explicitly (`S=/fast/scratch/hyaku/kasegi-r37/CritBoundary; mkdir -p "$S"`) and never relied on an inherited `TMPDIR`.
