# ScoutInstrumentInventory — r43 suite contract

Axes: depth:verifiability (the suite ExecSuiteSkeleton implements must be machine-gradable from this grammar), coverage (every r36–r42 convention and every hardcoded-`/tmp` writer).

Source of truth for the new checks is `.ufo/waves/round-43/claims.json` (read, not edited). Where the seat-prompt summary disagrees with that file, the file wins. Confidence: observed = read from a committed file or a command in Evidence; inferred = required so the frozen predicate stays gradable.

## 1. Exact shape r43-closure.sh must implement

Path: `corpus/instruments/r43-closure.sh`. Export mode only. Id prefix `K`. Nineteen checks. Sentinel `all-gates v3` (inferred: r41 restarted the five-line family at `v1`, r42 bumped to `v2` for 13 checks; 19 checks change the receipt length 33→45, so the sentinel bumps once. claims.json does not name the version. Do not reuse `all-gates v2`, or an r42 receipt pasted at the r43 path satisfies the sentinel limb.)

### 1.1 Arguments (keep r42 names)

```
r43-closure.sh --export-ref <hash> [--lane DIR] [--work DIR]
               [--scratch-root DIR] [--receipt-out PATH]
r43-closure.sh --selftest --export-ref <hash> [same options]
r43-closure.sh --export-ref <hash> ... --leaf
r43-closure.sh -h|--help
```

| flag | arity | behavior |
|---|---|---|
| `--export-ref` | value, required for every non-help invocation including `--selftest` | missing value → stderr `r43-closure: --export-ref needs a value`, exit 2. Absent → the two-line refusal below, exit 2. |
| `--lane` | value | default `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, overridable by `R43_LANE_DEFAULT` before the flag. Not a directory → one stdout line `ERROR ref-not-found lane=<path> ref=<token> closed=0 exit=1`, exit 1. |
| `--work` | value | extract root. Parent of `export/` must be outside the lane (claims.json; r42 does not enforce this — do not copy that gap). |
| `--scratch-root` | value | scratch for fixtures and the K9 nested run. |
| `--receipt-out` | value | write the receipt file (§1.4). Ignored when `--leaf`. |
| `--selftest` | flag | stdout is the graded block only (§1.5), not the run transcript. |
| `--leaf` | flag | nested depth-1. No further nesting, no receipt write, K9 and K10 take the deferred payloads in §1.6. |
| `-h`/`--help` | flag | comment header only, exit 0. |
| anything else | | stderr `r43-closure: unexpected argument <tok>`, usage on stderr, exit 2. |

Plain run (measured on r42, keep the shape with the r43 name), stderr, exit 2, before any scratch directory is created:

```
r43-closure: a plain run is refused (export mode only)
r43-closure: usage: r43-closure.sh --export-ref <hash> [options]
```

Resolve with `git -C "$LANE" rev-parse --verify --quiet "${EXPORT_REF}^{commit}"`. Empty → one stdout line, exit 1 (measured on r42):

```
ERROR ref-not-found ref=<token> closed=0 exit=1
```

Do not emit per-check `payload=ref-not-found` lines. That was r41. r42 replaced it with this single line, and the frozen kill rule only requires a distinct `ref-not-found` red plus exit 1.

Export, only after the ref resolves:

```
git -C <lane> archive <resolved> | tar -x -C <work>/export
```

`rm -rf` the export directory first. A failed archive prints `ERROR export-failed ref=<resolved> closed=0 exit=1` and exits 1 (r42 lines 89–91). Tree bytes are read from that export. Ref-scoped git reads (`rev-parse`, `cat-file`, `merge-base --is-ancestor`, `diff`, `log -1 --format=%ct`, `ls-tree`) stay read-only against the lane.

Scratch discipline (do not keep r42's fallback). r42 line 75 is `SCRATCH_ROOT="${TMPDIR:-/tmp}"`, which writes under literal `/tmp` when `TMPDIR` is unset. That is the §7 defect class. r43 must not contain that fallback. `--work` and `--scratch-root` are how the frozen counting commands invoke the suite; if either is missing, exit 2. Never default a write root to `/tmp`.

### 1.2 Run-mode stdout (not `--selftest`)

Five header lines, nineteen payload lines, one tally. No selftest lines on this stream. Trailing newline. Exit 0 only when all nineteen are closed, else 1.

```
all-gates v3
export-ref=<40 lowercase hex of the resolved ref>
suite-sha256=<64 hex of the export's corpus/instruments/r43-closure.sh, or none>
time-basis=ref-commit
run-utc=<YYYY-MM-DDTHH:MM:SSZ>
K1 payload=<cells> closed=0|1
...
K19 payload=<cells> closed=0|1
closed=<n>/19 exit=0|1
```

`run-utc` is `git log -1 --format=%ct` of the resolved ref, formatted UTC. Not the wall clock. `time-basis=ref-commit` is a fixed literal. `suite-sha256` is the export copy, so a tree that does not contain the script prints `none`.

The tally's exit field is `0` only when `n=19`, else `1`. The tally counts `closed=1` lines.

### 1.3 Payload line grammar

```
^K([1-9]|1[0-9]) payload=(.*) closed=([01])$
```

Cells are comma-separated `key=value` with no spaces. The K5 replay value contains commas (`outside=detected,inside=detected`); the payload is everything between `payload=` and ` closed=`. Do not split the replay cell on comma. The replay suffix is the tail after the literal `,replay=`, and only K1–K7 carry it.

Selftest payload-match compares the positive payload to the run payload with `,replay=...` stripped (r42 `run_selftest`, line 2083).

### 1.4 Receipt file (`--receipt-out`, not `--leaf`)

Byte transcript, 45 lines (`5 + 19 + 1 + 19 + 1`), newline-terminated:

1. the five header lines
2. K1..K19 payload lines
3. `closed=<n>/19 exit=<0|1>`
4. the nineteen graded selftest lines (§1.5) in id order
5. `selftest cases=19 failures=<k>`

K8's `lines=1` limb is this count. A summary-only body, a duplicate id, an extra line, or a selftest line missing `positive=` or `verdict=` is a stray (`no-stray=0`).

K8 is not in the deterministic re-derive set. At the judged head the receipt is absent, so K8 grades a synthesized canonical transcript and the frozen line says `source=canonical` / `receipt=(canonical)`. At Y the same check reads the committed file and the live payload says `source=committed`. Both can be `closed=1`. Do not require the K8 payload text at Y to equal the K8 line stored in the receipt. Deterministic set = K1–K7 and K9–K19 (r42 `DETERMINISTIC` excludes only J8).

### 1.5 Selftest stdout (`--selftest --export-ref`)

Nineteen graded lines then one summary. No `all-gates` header, no `K<n> payload=` lines, no `selftest detail=`, no `selftest judge=` (r36–r41 printed those; r42 stopped). Exit 0 iff failures=0, else 1.

```
selftest case=K<n> mutants=<ok>/<total> positive=pass|fail payload-match=0|1 verdict=pass|fail
selftest cases=19 failures=<k>
```

Regex (r42 `SELFTEST_RX`, id letter changed):

```
^selftest case=K(1[0-9]|[1-9]) mutants=(\d+)/(\d+) positive=(pass|fail) payload-match=([01]) verdict=(pass|fail)$
```

`verdict=pass` only when positive passed, payload-match is 1, total≥1 and ok=total. A line that is only `selftest cases=19 failures=0` does not satisfy a case. Field order is mutants, then positive, then payload-match, then verdict (r41/r42). Do not restore the r36–r39 order `positive=... mutants=... verdict=...`.

Established mutant widths to keep for the carried checks (committed r42 receipt):

| id | mutants |
|---|---|
| K1 | 1/1 |
| K2 | 1/1 |
| K3 | 3/3 |
| K4 | 2/2 |
| K5 | 2/2 |
| K6 | 2/2 |
| K7 | 2/2 |
| K8 | 6/6 |
| K9 | 3/3 |
| K10 | 2/2 |
| K11 | 1/1 |
| K12 | 2/2 |
| K13 | 2/2 |

K14–K19: at least one mutant each, built from the committed r42 narrative-defect bytes, rejected. The claim does not fix the width past that.

The six K8 forgeries (r42 `forgery_verdicts`) stay: forged payload value, flipped closed bit, forged tally, forged summary, `verdict=pass` flipped, `run-utc` replaced. `forged=6/6` in the payload.

### 1.6 K1–K13 payload cells (keep; rename J→K)

Copied from the committed green receipt `.ufo/waves/round-42/final-gates/all-gates.txt` lines 6–18. Value domains, not the round-42 numbers. Replay artifacts and their sha256 stay byte-for-byte (r42 `DEFEAT_ARTIFACTS`).

| id | family | artifact (sha256) | cells, in order |
|---|---|---|---|
| K1 | F-EVID | `.ufo/waves/round-41/wave2/RevC1Counters.md` `afe2c4d388d331035854d709072e3f62b9f87fa0f363e2170619789fb60a25d2` | `records,blocks,graded,evidence,missing,wrong-grade,per-record,union,replay` |
| K2 | F-TOKEN | `.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt` `6eef3338dc472e9033dc9131f5da630a6f23fea89ddda174f6819473593860af` | `boundary,truth-tokens,stated,mangled,truth-stated,token,replay` |
| K3 | F-TABLE | `.ufo/waves/round-41/wave2/MutSkillTablePipes.md` `41117cde4e2e30bb2969c056f00b8c9b4d379da9e7903a887fbd7867fb1fea7a` | `tables,rows,r42-rows,r40-rows,r40-split,bare,lead,replay` |
| K4 | F-DECL | `.ufo/waves/round-41/wave2/CritDeclarationCoverage.md` `0254bbe7b8b0b33bb6a8aa06b135813b8a11cc501bea1d81bed01e19da9141df` | `declared,valid,missing,escape,coverage,file,replay` |
| K5 | F-SCAN | `.ufo/waves/round-41/wave2/MutScratchTiming.md` `54fb821cd10d3c95a9bc4d3605b4fdce6da8611a057b6efcfd959f1c36fdae7e` | `family,strays,scanned,read,outside,outside-scanned,scope,replay` |
| K6 | F-BIND | `.ufo/waves/round-41/wave2/MutBindingExistence.md` `960e8da0580f1b4760112fb218d4620a55e5050576ce09fc7f3fef8c7808fb32` | `instrument,base,missing-path,url-mutated,digest-mutated,rule,replay` |
| K7 | F-FLIP | `.ufo/waves/round-41/wave2/MutFrontierParser.md` `faae26b19b0c04908fced285d3a8733b81125bccdfdad62f9dcc6f625ce4365c` | `instrument,base,status-flip,no-pass,rows,admitted,replay` |
| K8 | — | no defeat artifact | `receipt,source,sentinel,lines,ref,digest,time-basis,utc,ancestor,diff,run-lines,selftest-lines,verdicts,summary,closed-line,no-stray,payload-match,forged,payload-match,forged` |
| K9 | — | nested runs | `depth,base,r41,accept,cap` |
| K10 | — | synthetic canaries | `cases,isolated,canary,graded-lines,fixture` |
| K11 | — | — | `corrections,groups,dups,excused,unexcused,marker,marker-substantive,marker-appended,eof-closed,fenced` |
| K12 | — | — | `deleted,density,density-sha,diff-read,base` |
| K13 | — | — | `faithful,extra,missing,scratch-strays,scratch-read,markers,named` |

Cell value domains that are part of the grammar:

- K1 `per-record`: `SCORECARD.md=<ev>/<n>;LOG.md=<ev>/<n>;SHONEN.md=<ev>/<n>` (semicolons). `union` is an integer.
- K2 `boundary=<pass>/10`, `token=whole`. The ten probes are the r42 `BOUNDARY_PROBES` list (prefix/suffix traps on `closed=13/13`, `failures=6`, `cases=13`). Keep the probe list; the round-42 tally string inside the probes is the probe text, not the r43 tally.
- K3 `r40-split`, `bare`, `lead` are integers. Closed iff one r42 row, one r40 row, split=0, bare=0, lead=0.
- K4 `coverage=<hit>/11`, `file=present|absent`.
- K5 `family=kasegi-r4[0-9]*` (literal), `read=ok|fail`, `scope=materialized`. Replay detail is `outside=detected|missed,inside=detected|missed` with no extra comma escaping.
- K6 `instrument=present|absent`, `rule=reject`, the three mutant cells are 0|1, `base` is 0|1.
- K7 same shape; cells `status-flip`, `no-pass`, `rows`, `admitted`.
- K8 `source=committed|canonical`. `receipt` is the relative path or `(canonical)`. Every fact cell is 0|1. Then a second `payload-match=<m>/12` and a second `forged=<k>/6`. The duplicate keys are the r42 grammar (the fact list already emits `payload-match` and `forged` as 0|1, then the format string appends the fractions). Do not dedupe them. `m` counts the deterministic ids: 12 in r42 (13 minus J8) and 18 in r43 (19 minus K8). The fraction denominator therefore becomes 18. That is the one K8 cell whose denominator changes with N. The bool `payload-match=0|1` stays.
- K9 non-leaf: `depth=1,base=<0|1>,r41=<0|1>,accept=tree-red,cap=nested`. Nested refs stay r42's pair: base `5053a7f46de35784cff4b56756906e9014a38276`, r41 `1f7464612ac4c44e39886b82e812610d3c039b13`. Acceptance (`neg_accept`): child exit ≠ 0, tally in `0..18`, and at least two reds among K1, K2, K3, K4, K8, K11. Child argv: `--export-ref <ref> --lane <lane> --work <scratch>/work --scratch-root <scratch> --leaf`, with `R43_EXPORT`, `R43_WORK`, `R43_SCRATCH_ROOT`, `R43_REF`, `R43_RECEIPT_OUT`, `R43_LEAF` stripped from the environment and `TMPDIR` set to that scratch. Leaf payload, closed=0: `depth=leaf,base=deferred,r41=deferred,deferred=1,accept=tree-red`.
- K10 non-leaf: `cases=19,isolated=19,canary=0,graded-lines=19,fixture=synthetic` when every graded line matches the regex, each case is isolated, no canary leaked. Leaf, closed=0: `cases=0,isolated=0,canary=0,graded-lines=0,fixture=skipped`.
- K11 `eof-closed=<n>/3`, `fenced=0`.
- K12 `density-sha` is the first 12 hex of `corpus/instruments/density.py`; the pinned full sha stays `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710`. `diff-read=ok|fail`. `base` is the 8-hex of the deletion base (`5053a7f4` in r42). `deleted=0` is the closed limb.
- K13 `faithful=0|1`, `scratch-read=ok|fail`, `named=0|1`.

Replay polarity (do not normalize). The check stays closed only when the replay function's numeric rc is 1.

- K1, K2: rc is `0 if check_ok else 1`; detail `rejected` when the mutated fixture fails the check, else `accepted`. No substrate → rc 0, detail `no-substrate`.
- K3, K4: rc is `1` only when every sub-verdict rejected; detail `<ok>/<n>` or `no-substrate`.
- K5: rc is `1` only when both outside and inside strays are detected; detail `outside=detected|missed,inside=detected|missed`.
- K6, K7: rc is `1 if check_ok else 0` (opposite of K1); detail `rejected` when the check is ok, else `accepted`.

A missing or digest-mismatched artifact prints `replay=artifact-missing:<basename>` and forces the check open.

### 1.7 K14–K19 cells (inferred; the claim states predicates, not keys)

Same comma grammar, no `replay=` suffix. Each needs a mutant the selftest rejects. File names are the lane's names.

claims.json K14 says `SHENON.md`. That path does not exist (`ls` in Evidence). The record is `SHONEN.md`, which is also K1's `per-record` third field. Grading `SHENON.md` would make K14 blind to the defect it exists to see. Read `SHONEN.md`.

| id | closed when | cells |
|---|---|---|
| K14 | every `corrections=<n>` literal in `SCORECARD.md`, `LOG.md`, `SHONEN.md` equals the value re-derived on this export, or a committed `Correction (round 43)` line names that literal superseded | `files=3,literals=<n>,match=<n>,superseded=<n>,open=<n>` (`open=0` to close) |
| K15 | every sentence in `LOG.md` or `corpus/lessons/` that asserts a named `kasegi-rNN-*` wave was dispatched has `.ufo/waves/round-NN/<wave>-results.json`, or a `Correction (round 43)` line names it never-true | `sentences=<n>,bound=<n>,never-true=<n>,unbound=<n>` (`unbound=0` to close) |
| K16 | `corpus/lessons/round-42.md` `## Wave-2 falsification` promise is named unfulfilled by a `Correction (round 43)` line | `section=0\|1,named-unfulfilled=0\|1,open=0\|1` |
| K17 | every `closed=` / `failures=` literal in a `claims.json` `before` or `after` cell appears in the control receipt that cell cites, or a committed claims erratum names it superseded | `cells=<n>,in-receipt=<n>,erratum=<n>,open=<n>` |
| K18 | every `closed=` / `selftest cases=` value quoted in round-42 or round-43 lane records appears in a committed transcript under that round's `final-gates/` or `c1-controls/`, or the quoting line contains `report-only`, or a `Correction (round 43)` / claims-erratum line names it superseded | `quotes=<n>,in-transcript=<n>,report-only=<n>,superseded=<n>,open=<n>` |
| K19 | round-43 freeze `frozen_at_utc` is not earlier than the latest `measured-at=` in the two committed control receipts, and both receipts carry that line | `freeze=present\|absent,frozen_at=<utc\|absent>,latest-measured=<utc\|absent>,measured-lines=<n>,not-earlier=0\|1` |

K19 closes only when `not-earlier=1` and `measured-lines>=2`. It has no `open` cell.

### 1.8 Exits the claim requires, and the tally it forbids pre-declaring

| invocation | exit | stdout contains |
|---|---|---|
| no `--export-ref` | 2 | the two stderr lines in §1.1; no tally |
| `--export-ref` unresolvable | 1 | `ref-not-found` (the one-line form) |
| `--export-ref Y` with `--work` and `--scratch-root` | 0 | `closed=19/19 exit=0` and nineteen `K<n> payload=` lines |
| `--selftest --export-ref Y` with the same dirs | 0 | nineteen `verdict=pass` lines and `selftest cases=19 failures=0` |
| `--export-ref ab98fac9dce87130bc4f66de89e30650d63943dc` | 1 | `closed=<n>/19 exit=1` with K14–K19 each `closed=0` |
| `--export-ref 1f7464612ac4c44e39886b82e812610d3c039b13` | 1 | `closed=<n>/19 exit=1` |

claims.json predicate, not the seat summary: "the exact base figure is measured during integration and quoted in the report, never pre-declared." Do not hardcode `closed=13/19` and do not require that K1–K13 are all closed at base. The kill rule fires if any of K14–K19 is closed at base, or if either negative export prints `closed=19/19`. K8's canonical-receipt fallback (r42) can close K8 with no r43 receipt on disk; that is not permission to paint K14–K19 green at base.

Round-scoped constants that must move (the cell names do not): `ROUND=43`, receipt `.ufo/waves/round-43/final-gates/all-gates.txt`, declared-blocks `.ufo/waves/round-43/declared-blocks.txt`, suite path `corpus/instruments/r43-closure.sh`, env prefix `R43_`, sentinel `all-gates v3`. Replay artifact paths stay in round-40 and round-41.

## 2. Conventions r42 established that r43 must keep

Observed in `corpus/instruments/r42-closure.sh` and the 33-line receipt.

1. Export mode is the only run mode. Plain invocation exits 2 before mkdir.
2. Unresolvable ref is a one-line stdout red, exit 1, not a harness exit 2 and not a vacuous tally with empty payloads.
3. Five-line header: sentinel, `export-ref`, `suite-sha256`, `time-basis=ref-commit`, `run-utc` from the ref's committer instant.
4. One `payload=` line per check, then `closed=<n>/<N> exit=<0|1>`. Exit 0 only at N/N.
5. Run-mode stdout does not include selftest lines. `--selftest` stdout is only the graded lines plus the summary.
6. `--receipt-out` writes header + payload lines + closed line + graded lines + summary. Not written under `--leaf`.
7. Graded line field order `mutants=<ok>/<n> positive=pass|fail payload-match=0|1 verdict=pass|fail`. Summary `selftest cases=<N> failures=<k>`. No `detail=` / `judge=` lines.
8. A summary-only report is not a pass. `verdict=pass` requires `positive=pass` as well.
9. Payload cells are comma-separated `k=v` with no spaces. K1–K7 append `,replay=<basename>=<detail>` after digest-checking the committed defeat. K8–K13 have no replay suffix.
10. Payload-match ignores the `,replay=` tail.
11. K8 (was J8) excludes itself from deterministic re-derive, accepts a canonical transcript when the receipt is absent, and emits duplicate `payload-match` and `forged` keys (bool, then fraction).
12. `--leaf` is the depth cap: K9 deferred and closed=0, K10 `fixture=skipped` and closed=0, child does not nest, child does not write a receipt.
13. K9's nested negatives are `5053a7f4…` and `1f746461…`, judged by `neg_accept` (≥2 reds in K1, K2, K3, K4, K8, K11, nonzero exit, tally not N).
14. K12 still pins `density.py` to `ee803726a322…` and deletion-base `5053a7f4`.
15. Archive invocation is `git -C <lane> archive <resolved> | tar -x -C <export>` (r42 / the claim), not r38–r41's `tar -xf -`.
16. `set -uo pipefail`. Usage errors exit 2. Check failures exit 1.
17. Help is `-h|--help`, exit 0. r42's `sed -n '2,30p'` also prints `set -uo pipefail` because the comment ends at line 27 (measured). Do not keep that off-by range; stop the header comment before code.

Do not keep: the `${TMPDIR:-/tmp}` fallback; r42's failure to reject a `--work` inside the lane (the claim requires the work dir outside the lane).

## 3. all-gates header versions (observed)

| round | script constant | committed `final-gates/all-gates.txt` line 1 | header shape |
|---|---|---|---|
| r36 | none | no receipt | `E<n> payload=` then `closed=K/9`. Selftest has `detail=` and `judge=`. `mktemp -d -t` (honors `TMPDIR`). |
| r37 | `all-gates v1` | `all-gates v1` | 4 lines: sentinel, export-ref, suite-sha256, run-utc. No `time-basis`. Body has `== run ==`. 121 lines. |
| r38 | `all-gates v2` | `all-gates v2` | Not a clean transcript: line 4 is `run-ref=`, line 5 is a `#` comment, later lines are `export-ref-run:` prefixed. |
| r39 | script checks `all-gates v3` (lines 89, 686, 1133) | file line 1 is `all-gates v5` | Drift. Do not copy either side as the r43 sentinel. The script header's run preamble is `export-ref= mode=export lane= suite-sha256=` before the G lines, which is not the five-line family. |
| r40 | `all-gates v4` | `all-gates v4` | The five-line header begins here (`time-basis=ref-commit`). Receipt is header + H lines + `closed=10/10 exit=0` (16 lines). Selftest is not inside the receipt. |
| r41 | `all-gates v1` (family reset) | `all-gates v1` | Five-line header, then I lines, then graded selftest lines, then summary, then closed line. Graded-field order is the one r42 kept. Ref-not-found is per-check `payload=ref-not-found,...` plus `suite-ref-status=ref-not-found` — r42 replaced that. |
| r42 | `all-gates v2` | `all-gates v2` | 33 lines. Order: 5 header, 13 J lines, closed, 13 graded, summary. This is the shape r43 scales to 19. |

## 4. Hardcoded `/tmp` (scratch-discipline defect class)

Scan: every `*.py` and `*.sh` under `corpus/instruments/` (Evidence). No `mkdtemp(dir="/tmp")` and no unconditional `/tmp/<name>.XXXX`.

Writers that fall through to a literal `/tmp` when `TMPDIR` is unset — this is the defect class:

| file:line | mechanism | honors |
|---|---|---|
| `r42-closure.sh:75` | `SCRATCH_ROOT="${TMPDIR:-/tmp}"` then `mkdir` `$SCRATCH_ROOT/r42-<12>/` | `--scratch-root`, else `TMPDIR`, else `/tmp`. Not removed on exit. |
| `r-defect-closure.sh:461` | `mktemp -d "${TMPDIR:-/tmp}/rdc-r9.XXXXXX"` inside a check | `TMPDIR`, else `/tmp`. Removed before return. |
| `r-defect-closure.sh:750` | `base=${SCRATCH_ARG:-${HYAKU_SCRATCH:-${TMPDIR:-/tmp}}}` | `--scratch`, else `HYAKU_SCRATCH`, else `TMPDIR`, else `/tmp`. |
| `r35-defect-closure.sh:114` | `SCRATCH_BASE=${KASEGI_SCRATCH:-${TMPDIR:-/tmp}}` | `KASEGI_SCRATCH`, else `TMPDIR`, else `/tmp`. No `--scratch-root`. |

Not the defect class:

- r36–r41 `mktemp -d -t rNN-closure.XXXXXXXX` — `mktemp -t` uses `TMPDIR`. Comments at r36:217, r37:286, r38:258, r39:306, r40:292 say so. r41:359 is the same call without the comment.
- `frontier-recheck-count.py`, `capture-binding-check.py`, `kill-rule-check.py`: `--scratch`, else `$HYAKU_SCRATCH`, else `$TMPDIR`, else `/fast/scratch/hyaku` if it is a directory, else `tempfile.gettempdir()`. No literal `/tmp`.
- `anchorcheck.py:299`, `source-recheck.py:262`, `mirror-containment-check.py:161`, `resolve-dispatch-check.py:214`, `capture-source.py:60` and `:102`, `recheck-audit.py:201`, `limb-mutation-check.py:260`, `:599`, `:619`, `score-gap.py:462`: `tempfile` with no `dir=`, so they follow `TMPDIR` via Python's temp dir, not a hardcoded `/tmp`.
- `density.py:6-7`, `resolve.py:10` and `:43`: `/tmp/...` appears only in comments or classifier examples. Not writes.
- `recheck-audit.py:216`: the string `cd /tmp &&` is fixture text inside a case, not a directory the tool creates.

`citation-survival.tsv` cites historical `/tmp/kasegi-r1*` paths. It is a generated census, not an instrument that writes there.

## 5. Other committed instruments (argument names only)

Closure suites above are the contract. The rest, from their usage blocks:

| script | arguments | selftest line |
|---|---|---|
| `density.py` | `<file> [--label LABEL] [--debug]` | none |
| `resolve.py` | `<lane-root>` | none (census written next to the script) |
| `anchorcheck.py` | `<file.md>` or `--selftest` | `selftest cases=N failures=0` |
| `test_resolve.py` | unittest | temp under the script dir |
| `mirror-containment-check.py` | `[--resolver] [--fixtures] [--json]` | none |
| `resolve-dispatch-check.py` | `[--resolver] [--json]` | none |
| `capture-source.py` | `--id --url --out [--kind]` or `--selftest` | none in the usage block |
| `source-recheck.py` | `--manifest --source` | none |
| `frontier-recheck-count.py` | `[--root] [--json]` or `--selftest [--scratch]` | `selftest case=<name> exit=N want=N verdict=` |
| `capture-binding-check.py` | `[--root] [--selftest] [--scratch]` | same `exit/want/verdict` shape; summary-only is a failure |
| `kill-rule-check.py` | `[--instrument] [--fake] [--root] [--scratch] [--row-file] [--json] [--selftest]` | same shape; `CASE_FLOOR=19` |
| `recheck-audit.py` | audits `corpus/knowledge` | `--selftest` builds temp trees |
| `limb-mutation-check.py` | `--ledger [--root]` or `--selftest` (selftest rejects `--ledger`/`--root`) | internal fixtures |
| `score-gap.py` | `[--selftest]` | not a claim |
| `r-defect-closure.sh` | `[--root DIR] [--selftest] [--scratch DIR]` | `selftest case=R# live= fixture= control= verdict=` |
| `r35-defect-closure.sh` | `[--root DIR] [--selftest]` | `selftest case=D<i> live= fixture= mutants= others= verdict=` |

r43's graded line is the r42 line, not these `exit/want` or `live/fixture` lines.

## 6. Evidence

Lane base named by the freeze is `ab98fac9dce87130bc4f66de89e30650d63943dc`. These reads are the working tree at dispatch, which contains the committed r42 suite. Scratch `$S=/fast/scratch/hyaku/kasegi-r43/ScoutInstrumentInventory`, `TMPDIR=$S`. Removed before yield.

```
$ bash corpus/instruments/r42-closure.sh; echo plain_exit=$?
r42-closure: a plain run is refused (export mode only)
r42-closure: usage: r42-closure.sh --export-ref <hash> [options]
plain_exit=2

$ bash corpus/instruments/r42-closure.sh --export-ref deadbeefdeadbeefdeadbeefdeadbeefdeadbeef --work "$S/w" --scratch-root "$S"; echo dead_exit=$?
ERROR ref-not-found ref=deadbeefdeadbeefdeadbeefdeadbeefdeadbeef closed=0 exit=1
dead_exit=1

$ bash corpus/instruments/r42-closure.sh --export-ref; echo miss_exit=$?
r42-closure: --export-ref needs a value
miss_exit=2

$ bash corpus/instruments/r42-closure.sh --export-ref ab98fac9dce87130bc4f66de89e30650d63943dc --nope; echo unk_exit=$?
r42-closure: unexpected argument --nope
<usage text, then the line set -uo pipefail>
unk_exit=2

$ ls SHENON.md SHONEN.md
ls: cannot access '.../SHENON.md': No such file or directory
.../SHONEN.md
```

Receipt first lines: r37 `all-gates v1` then export-ref, suite-sha256, run-utc, blank, `== run ==` (121 lines). r38 `all-gates v2`, then export-ref, suite-sha256, `run-ref=`, a `#` comment. r39 line 1 `all-gates v5` while the script matches `all-gates v3`. r40 `all-gates v4` + `time-basis=ref-commit` + `H1 payload=suite=1,digest=1,registry=1,registry-in=skill closed=1` (16 lines). r41 `all-gates v1` + `I1 payload=records=3,lines=14,graded=3,evidence=3/3,missing=0 closed=1`. r42 33 lines; line 6 is `J1 payload=records=1,blocks=3,graded=1,evidence=3,missing=0,wrong-grade=0,per-record=SCORECARD.md=3/3;LOG.md=0;SHONEN.md=0,union=0,replay=RevC1Counters.md=rejected closed=1`; line 33 is `selftest cases=13 failures=0`.

`/tmp` scan: Python walk of `corpus/instruments/**/*.py` and `**/*.sh`, 61 hit lines, classified in §4. No instrument contains `mkdtemp(dir="/tmp")`.

Unresolved: the numeric base tally (`closed=<n>/19` at ab98fac9). claims.json says integration measures it. K8's denominator change 12→18 is inferred from `len(DETERMINISTIC)` once N=19. K14–K19 key names are inferred from the predicate; the predicates themselves are quoted from claims.json.
