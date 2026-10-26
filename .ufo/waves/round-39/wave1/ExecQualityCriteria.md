# ExecQualityCriteria — round-39 QUALITY.md append block

Seat: ExecQualityCriteria (leaf executor), round 39, dispatched via `wave1-dispatch.json` (hyaku run 9).
Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only lane). Base `480b1a505a2dfc14a4f718d16d63808247214d0a`,
claims-freeze `dcd31701720a6a4929a32471a62011ed87103421`. Read first: `claims.json` (authoritative), `c1-controls/before.txt`,
`c2-controls/before.txt`, `census-before.txt`.

Axes named: **depth:verifiability** (the block's three rows all bind a claim to a runnable limb: R34 frozen-command
satisfiability, R35 transcript binding, R36 captured-by closure), **depth:density** (the block adds three rows to a
front-door ledger without touching one existing line — R6 form), **coverage** (untouched; no row claims it).

## 1. Deliverable (byte-exact, landable)

Path: `.ufo/waves/round-39/wave1/ExecQualityCriteria.quality.append.md`
Lines: **16** — Bytes: **6850** — sha256: **`a89eaa2de29dde8068ba4ab2b41ab9b9c2f0d17c718cdaa622ec7738742b368d`**

Contents (structure only; the bytes are the deliverable): one leading blank line, the heading
`## Round-39 additions — frozen-command satisfiability, transcript binding and captured-by closure (append-only)`,
the R6 preamble paragraph, blank, `| id | criterion | grounded in |`, `|---|---|---|`, and exactly three rows
`| R34 | … | … |`, `| R35 | … | … |`, `| R36 | … | … |`. No validation text, no tables, no headings beyond the block
heading (round-37 D-A discipline).

## 2. R6 measurement on the pre-landing file

Commands, actual output (2026-10-26T19:2xZ, read-only):

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && wc -l corpus/QUALITY.md
292 corpus/QUALITY.md
$ wc -c corpus/QUALITY.md
46569 corpus/QUALITY.md
$ head -c 46569 corpus/QUALITY.md | sha256sum
f2c2948da7676c4c6d9b6096768a9c48bc51b536d7ac030a83149204034a6237  -
$ git status --porcelain | grep -c QUALITY
0
```

The preamble in the deliverable carries exactly these figures (`46569` bytes, sha256 `f2c2948d…`, `wc -l` → `292`).
Row line numbers verified untouched-by-construction:

```
$ grep -nE '^\| R(22|23|26|27|28|29|30|31|32|33) \|' corpus/QUALITY.md | cut -c1-40
226:| R22 | A frozen claim predicate is
227:| R23 | A lane records an event-driv
249:| R26 | A round reports the distance
250:| R27 | A lane records an event-driv
263:| R28 | A round's claims rest on com
264:| R29 | An instrument is registered
277:| R30 | A gate's failure path is fai
278:| R31 | A considerthese proposal tha
291:| R32 | A front-door append (PROVINC
292:| R33 | Closure order: the judged he
```

Spec-vs-measured discrepancy recorded, not silently adopted: the item spec said "45.5KB/288 lines"; measured now
`46569` bytes (45.5KB, matches) and **292** lines (spec figure stale by 4 lines — the r38 block landed 3 table rows plus
heading/preamble after line 278). The deliverable and preamble carry the measured 292. The preamble also carries the
R19 landing rule verbatim in shape ("The landing commit re-runs both commands immediately before writing: a byte figure
measured at draft time is a stale premise under R19 if an earlier append in the same round moved it"), so the L1 must
re-measure before landing if any earlier round-39 append (e.g. a corrections block) moves the file.

## 3. Validation of the append (scratch mirror, before scratch removal)

Applied the deliverable to a scratch copy of `corpus/QUALITY.md` and checked the post-state:

```
prefix-identical: True orig-bytes: 46569 new-bytes: 53419
orig sha: f2c2948da7676c4c6d9b6096768a9c48bc51b536d7ac030a83149204034a6237
fence openers at: [110, 137, 148, 177, 204] | open at EOF: None
304 pipes 4 ticks 0 odd-ticks False
305 pipes 4 ticks 0 odd-ticks False
306 pipes 4 ticks 54 odd-ticks False
307 pipes 4 ticks 56 odd-ticks False
308 pipes 4 ticks 50 odd-ticks False
rows: 3
scaffolding markers: []
```

`prefix-identical: True` is the R6 invariant (`new.startswith(orig)` on the raw bytes, so every pre-existing byte keeps
its offset and its line number). Fence walk = CommonMark model (backtick and `~~~` openers, closer must match type and
length with an empty info string); the new block opens no fence and the file ends **CLOSED**. Each row line carries
exactly 4 pipes (3 columns) and an even backtick count (every code span closed). Post-append file = 308 lines =
292 + 16.

## 4. Row grounding — each row cites its lesson row id and committed evidence

### R34 — frozen counting command dry-run over a stand-in head (M39-1, verifier R1)

Committed evidence, actual reads:

```
$ sed -n '2p;8p;15p;17p;26p' .ufo/waves/round-38/final-gates/all-gates.txt
export-ref=66703acaaff50529a35be49aa8759d04140720ad
export-ref-run: G2 payload=receipt=0,sentinel=0,export-ref=0,ancestor=0,diff-clean=0,digest-match=0,run-lines=0,closed-line=0,selftest-lines=0,selftest-summary=0,scorecard-ref=1,shonen-ref=1,head-token-lines=0 closed=0
export-ref-run: closed=7/8 exit=1
run-header: export-ref=7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e mode=export …
closed=8/8 exit=0
$ grep -n "receipt=\|all-gates\|ancestor" corpus/instruments/r38-closure.sh | head
409:    local p=.ufo/waves/round-38/final-gates/all-gates.txt
411:    local file=0 sentinel=0 xref='' xsha='' ancestor=0 diffclean=0 digest=0
471:    [ "$file" -eq 1 ] && [ "$sentinel" -eq 1 ] && [ -n "$xref" ] && [ "$ancestor" -eq 1 ] \
$ git ls-files corpus/instruments/r39-closure.sh | wc -l
0
```

Mechanism: `r38-closure.sh:411` seeds `file=0` from the receipt's presence in the export and `:471` demands
`file -eq 1`, so an export that cannot contain the receipt it names is red — measured as `closed=7/8 exit=1` over J
(`all-gates.txt:15`). The 8/8 in the same receipt is over `run-ref=7dd2fcd6` (J + bootstrap receipt, `:17`, `:26`).
Routed by `corpus/lessons/round-38-verifier-spotcheck.md:155-160` (R1). The row's criterion is the spot-check's own
suggested shape, made executable: the round-39 G2 grades a receipt *in the export* whose `export-ref=` is
ancestor-or-equal of the export commit with a receipt-only diff (`claims.json` C1 G2), so the satisfiable run is over
the stand-in (head + receipt) and a limb red only because the named head cannot hold its own receipt is an
unsatisfiable freeze. Before-state honestly stated: the r39 instrument is untracked at draft head, so the row claims no
run of its own and claims the committed r38 receipt instead.

### R35 — every quoted export-ref result has a transcript or `report-only` (M39-3, verifier R3)

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin grep -c f06148c6 f06148c6 -- .
<no output>
grep-exit=1
$ grep -c 7dd2fcd6 .ufo/waves/round-38/final-gates/all-gates.txt
3
$ grep -c f06148c6 .ufo/waves/round-38/final-gates/all-gates.txt
0
$ grep -n f06148c6 /home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md | cut -c1-260
3:Lane tip at filing: `f06148c66c6d7aed948cb7024d9f0b9cffe4b95a` …
31:- `f06148c6` — receipt fix: the quoted run header collided with the receipt's `export-ref=` anchor …
37:- `bash corpus/instruments/r38-closure.sh --export-ref f06148c66c6d7aed948cb7024d9f0b9cffe4b95a` (tip = J + receipt only) → `closed=8/8 exit=0`, every G line `closed=1`; `--selftest --export-ref f06148c6…` → `selftest cases=8 failures=0` (8 case lines
$ sed -n '94p' corpus/lessons/round-38.md | cut -c1-200
8. **C1 receipts at the judged head.** `bash corpus/instruments/r38-closure.sh` plain → exit 2; `--export-ref J` → `closed=8/8 exit=0`; `--selftest --export-ref J` → `selftest cases=8 failures=0`; …
```

The tip run is report-only in fact (no committed line at `f06148c6` names `f06148c6`; the committed 8/8 transcript is
over `7dd2fcd6`), and the lane's own `corpus/lessons/round-38.md:94` quotes a J result the committed receipt
contradicts (`all-gates.txt:15`). Routed by `corpus/lessons/round-38-verifier-spotcheck.md:168-171` (R3). The row
states the binding: transcript under the round's `final-gates/` in the judged head, or the label.

### R36 — `captured-by: none` gets a criterion in the same round (M39-4, verifier R4)

```
$ for t in M38-1 M38-2 M38-4 M38-5 M38-7 M39-1 M39-3; do printf '%s %s\n' "$t" "$(grep -c "$t" corpus/QUALITY.md)"; done
M38-1 1
M38-2 1
M38-4 1
M38-5 0
M38-7 0
M39-1 0
M39-3 0
```

Row cells read from `corpus/lessons/round-38.md:287` (M38-5, captured-by `none — R31 requires a disposition per touched
proposal, but no check reads a row count, so an empty section reads exactly like a filled one`) and `:289` (M38-7,
captured-by `none — the wave context forbade fleet writes and required absolute paths, but nothing enforced it inside a
seat's own fixture driver`). R32 (`QUALITY.md:291`) cites M38-1 and R33 (`:292`) cites M38-2/M38-4 — the gap is exactly
where R32/R33 stop, and the measured `0`s are the before-state. Routed by
`corpus/lessons/round-38-verifier-spotcheck.md:172-174` (R4). This block closes the class in the round that mints it:
R36 cites M38-5/M38-7, R34 cites M39-1, R35 cites M39-3.

## 5. Landing instruction for the L1

1. Re-run `wc -c corpus/QUALITY.md` and `head -c <bytes> corpus/QUALITY.md | sha256sum` and `wc -l corpus/QUALITY.md`
   immediately before landing. If the figures still read `46569` / `f2c2948d…` / `292`, append the deliverable bytes
   verbatim. If an earlier round-39 append moved them, the R6 preamble must be re-derived (update byte count, digest and
   the `wc -l` figure, and re-number the "not edited" list) — that is an edit to the preamble only, never to rows R22–R33.
2. Append, do not rewrite: `cat .ufo/waves/round-39/wave1/ExecQualityCriteria.quality.append.md >> corpus/QUALITY.md`,
   then check `head -c <old-bytes> corpus/QUALITY.md | sha256sum` still reads the pre-append digest.
3. Cross-check with the suite's G-limbs: this block is the ruled text the round-39 lesson's M39-1/M39-3/M39-4 point at;
   `corpus/lessons/round-39.md` must cite R34/R35/R36 by id in the fix column for those rows (that is the lesson seat's
   deliverable, not mine).

## 6. Risks / notes

- **R34 vs the frozen C1 wording.** `claims.json` C1 says the suite "prints `closed=8/8 exit=0` on the round-39 judged
  head J" while its G2 requires the receipt inside the export and the judged-head rule says J excludes the receipt. As
  written, a run literally over J yields `G2 receipt=0 → closed=7/8`, exactly the r38 shape. R34's criterion states the
  satisfiable form (grade over the stand-in, or name the stand-in), so the landing must ensure the receipt's own
  transcript is produced over the stand-in and the records do not claim the run over J. I did not run
  `r39-closure.sh` (absent at base) and did not judge the claim — this is a wording hazard for the L1/verifier, recorded
  here as evidence, not as a lane edit.
- **Stale spec line count** (288 vs measured 292) — preamble uses measured; see §2.
- **Concurrent appends.** `corpus/QUALITY.md` was unmodified in the worktree at my measurement
  (`git status --porcelain | grep -c QUALITY` → 0). If another seat's deliverable also appends to QUALITY.md, the last
  appender owns the final R6 figures; two appends with one preamble each is the r38 shape and is fine as long as each
  preamble is re-measured at its own landing.
- No blockers.

## 7. Tooling and scratch

- No tool installed or upgraded (nothing needed; all work was read + `sha256sum`/`grep`/`sed` + a Python fence/pipe
  check).
- Scratch `S=/fast/scratch/hyaku/kasegi-r39/ExecQualityCriteria` created with `mkdir -p`, held `q.md` (prefix mirror) and
  `m39.txt` (the M39 spec text, folded for reading). Removed with `rm -rf -- "$S"`; verified after removal:
  `ls -d /fast/scratch/hyaku/kasegi-r39/ExecQualityCriteria` → `No such file or directory`. Sibling seat dirs under
  `kasegi-r39/` are theirs, untouched.
- Disk guard at start `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → `/fast/scratch/hyaku 24%
  use 614.6G free` (green).
- Writes made: this receipt, the deliverable, and scratch only. No git mutation, no fleet-root write, no PATH-directory
  write, no `MANIFEST.json`/`templates/`/`scripts/`/`.ufo/state/` touch. Read-only reads of the fleet report
  `.ufo/reports/round-38/kasegi.md` are cited above.
