# ExecRegressionC2 — round 34 wave1 receipt

Seat: **ExecRegressionC2** (executor, leaf of the L2 wave; lane `kasegi-shokunin`). Assignment:
**final C2 (coverage) regression at quiescent tip bytes** — run every C2 counting command from
`.ufo/waves/round-34/claims.json` verbatim, record the outputs, compare them to the claim's
`after` values, and report matches/mismatches. This seat authored no C2 change: it wrote no corpus
file, no instrument, no entry, no registry row and no SCORECARD/QUALITY text.

Method constraints honoured: read-only git plumbing only (`rev-parse`, `show`, `archive`, `status`,
`diff`, `ls-tree`); no `git add/commit/push`; no jj mutation; no write outside this receipt, its two
evidence appendices and `/fast/scratch/hyaku/kasegi-r34/ExecRegressionC2/`; no subagent dispatch; no
`agent://all`. Tools installed: none (Python 3 and coreutils/gawk from the host were sufficient).

## Report

### 1. Measurement state, quiescence and byte identity

| item | value |
|---|---|
| lane root | `/home/vgpnk/Projects/shokunin/kasegi-shokunin` |
| base | `014ee2d7aa8c3c095ff57ae51097606a9906228c` |
| claims-freeze | `29f606dbdd28aff6fd4573ab4b90788bbb90af13` |
| tip at every measure below | `206e5108f1190e61b3e2622d21cab8a5d921650c` (`206e510`) |
| frozen claims integrity | `sha256sum .ufo/waves/round-34/claims.json` → `dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850`; `git show 29f606dbdd28aff6fd4573ab4b90788bbb90af13:.ufo/waves/round-34/claims.json \| sha256sum` → same digest. The predicates compared below are the committed frozen bytes. |
| landing state | uncommitted in the working copy (the L1 commits). `git status --porcelain` at the final measure: 12 tracked `M` paths (`SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/README.md`, `corpus/instruments/capture-binding-check.py`, `corpus/instruments/frontier-recheck-count.py`, `corpus/lessons/round-29.md`, `corpus/lessons/round-33.md`, `corpus/source-snapshots/round-26/manifest.json`, `corpus/source-snapshots/round-32/manifest.json`, `.ufo/waves/round-33/wave1/ScribeReportDraft.md`) and 10 untracked paths (`kill-rule-check.py`, `r-defect-closure.sh`, the F17 entry, `corpus/source-snapshots/round-34/`, `selftest-baseline.txt`, the wave dirs). |

**Quiescence** was measured, not assumed. A surface watcher (git rev + `sha256sum` of
`corpus/README.md`, `corpus/SOURCES.md`, `SCORECARD.md`, `frontier-recheck-count.py`,
`source-recheck.py`, `knowledge/*.md` concatenation, `corpus/source-snapshots/round-34/*`,
`c2-controls/*`) polled every 10–20 s and required 5–6 consecutive identical polls:

```
QUIESCENT polls=22 rev=206e5108f1190e61b3e2622d21cab8a5d921650c surfaces=c9546f8f9e28a7bc20526ff09a716a2862ef00999daa0ae62ca4542e8f733815 at 2026-10-26T05:39:32Z
QUIESCENT polls=6 rev=206e5108f1190e61b3e2622d21cab8a5d921650c c2=58e932044aa27804fe9d3b96e9a4bdb688b713324cc81fc684b572b2b73e69c0 at 2026-10-26T05:43:44Z
poll=6 t=05:46:43Z rev=206e510 c2=5292cf954a44b73161e436f2626207fa5f3d5c65c965522de293a20a030801d3
QUIESCENT polls=6 rev=206e5108f1190e61b3e2622d21cab8a5d921650c c2=5292cf954a44b73161e436f2626207fa5f3d5c65c965522de293a20a030801d3 at 2026-10-26T05:46:50Z
QUIESCENT polls=6 rev=206e5108f1190e61b3e2622d21cab8a5d921650c c2=5292cf954a44b73161e436f2626207fa5f3d5c65c965522de293a20a030801d3 at 2026-10-26T05:48:22Z
```

Byte identity of the surfaces the seven counters read, at the final quiescent measure
(2026-10-26T05:46:50Z, full digest block in `ExecRegressionC2-battery-final.txt`):

```
876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29  corpus/README.md
4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6  corpus/SOURCES.md
b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0  SCORECARD.md
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  corpus/instruments/frontier-recheck-count.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe  corpus/source-snapshots/round-34/manifest.json
948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
S051_txt_sha256=4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5
knowledge_files=46
knowledge_digest=291b7da19cf97ca4eb80bc739527aa1db892e2919764171765408c7b26e381ab
junk_twin_sha256=2752a994265a1e284ebd236730d169d677e1923cfb7073cf79ad874d19bc4026
```

**Determinism and digest succession.** Four full batteries were run at four quiescent points
(`q1` 05:39:55Z, `q2` 05:42:16Z, `q3` 05:43:44Z, `q4` 05:46:50Z). Every counter section is
byte-identical across them (`diff` of the `C2 counter A` … `end label` block → only the `label=`
line differs), and the two back-to-back runs at one state (`q2`/`q2b`) differ only in `label=` and
`utc=`. Only the harness bytes moved while I measured, and the counter output did not move with
them:

| surface | q1 05:39:55Z | q2 05:42:16Z | q3 05:43:44Z | q4 05:46:50Z |
|---|---|---|---|---|
| `corpus/instruments/frontier-recheck-count.py` | `87b14892dfc4…` | `8a79010d557d…` | `8a79010d557d…` | `1be79af6…` |
| harness output | `entries=20 pass=20 exit=0` | same | same | same |

`ExecFrontierBidirectional`'s receipt names the earliest of those digests, `87b14892dfc4…`; the
final measured bytes are `1be79af60cb5…`, and the counter is green at both.

### 2. Before-control reproduction (proof the counters discriminate)

`git archive 014ee2d7aa8c3c095ff57ae51097606a9906228c | tar -x -C <scratch>/base` (6815 files)
then the same commands inside the extracted tree (`ExecRegressionC2-battery-base.txt`):

```
A=16          (grep -cE '^\| F[0-9]+ \|' corpus/README.md)
B=50          (grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md)
C=0  exit=1   (grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md)
D=0           (grep -lE '^source: S051 ' corpus/knowledge/*.md | wc -l)
knowledge_files=45
entries=19 pass=19 exit=0        (python3 corpus/instruments/frontier-recheck-count.py, base-tree run)
manifest UNAVAILABLE reason=missing / recheck_exit=2   (source-recheck --source S051)
census_exit=0  with kasegi W04 S028, kasegi W04 S029, kasegi ok
```

This reproduces the frozen before block in `.ufo/waves/round-34/c2-controls/before.txt` (committed
at the freeze commit) line for line — `frontier admitted 16`, `registry rows 50`, `S051 rows 0`,
`entries citing S051 0`, `harness entries=19 pass=19 exit=0`,
`manifest UNAVAILABLE reason=missing / recheck_exit=2`, `knowledge entries 45`, and the same two
W04 lines with `census_exit=0`. **Caveat disclosed:** the base-tree census run resolves the lane at
its canonical live path (`--root /home/vgpnk/Projects/shokunin kasegi`), so that census line is a
live-lane read, not a base-bytes read; the base registry row count is the counter-B value measured
on the extracted bytes (50), and the frozen `before.txt` carries the same three census lines.

### 3. Final C2 battery — every counting command from claims.json, verbatim

All commands ran from the lane root at the quiescent state of §1. Raw log:
`ExecRegressionC2-battery-final.txt`.

| # | command (verbatim) | measured output | exit | claim `after` | verdict |
|---|---|---|---|---|---|
| A | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `17` | 0 | frontier admitted 17 | **match** |
| B | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `51` | 0 | registry rows 51 | **match** |
| C | `grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md` | `1` | 0 | S051 row 1 | **match** |
| D | `grep -lE '^source: S051 ' corpus/knowledge/*.md \| wc -l` | `1` | 0 | entries citing S051 1 | **match** |
| E | `python3 corpus/instruments/frontier-recheck-count.py` | `PASS F17 … ids=S051 exit=0` + `entries=20 pass=20 exit=0` | 0 | entries/pass 20/20, `PASS F17` | **match** (literal-spacing note C2-R2) |
| F | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051` | `S051:sha256 OK` + 18 assertions `OK`, exit 0 | 0 | sha256 OK, exit 0 | **numeric match; wording mismatch C2-R1** |
| G | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `W04 S028`, `W04 S029`, `kasegi ok …/corpus/SOURCES.md` | 0 | exit 0, W04 S028/S029 only | **match** |

Supporting values from the same run: `entries_citing_s051=1`, `knowledge_files=46` (claim
`entries=46`), F17 row at `corpus/README.md:361` (`| F17 | Immunefi Vulnerability Severity
Classification System v2.2 — Web3/smart-contract bounty severity classification | admitted |
knowledge/immunefi-vscs-v2-2-smart-contract-severity.md | S051 | …`), S051 row at
`corpus/SOURCES.md:57` with `NF=13` and fields `kind=docs`, `tier=A`, `status=mined`,
`opened=2026-10-26`, `recheck=90d`, `used-by=corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`
— i.e. the claim's `tier A, status mined, opened 2026-10-26` holds. Census emits no `E` code, so
`E11` (used-by path missing) is clean.

Counter E in full (the one line the claim names):

```
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
entries=20 pass=20 exit=0
```

Counter F in full (18 assertions; `Q9` and `Q17` are the two occurrence-count exceptions of C2-R1):

```
S051:sha256 OK
S051:Q1 OK occurrences=1 anchor=46-ok      S051:Q11 OK occurrences=1 anchor=83-ok
S051:Q2 OK normalized=markup-whitespace occurrences=1
S051:Q3 OK occurrences=1 anchor=52-ok      S051:Q13 OK occurrences=1 anchor=92-ok
S051:Q4 OK occurrences=1 anchor=52-ok      S051:Q14 OK occurrences=1 anchor=94-ok
S051:Q5 OK normalized=markup-whitespace occurrences=1 anchor=53-ok
S051:Q6 OK normalized=markup-whitespace occurrences=1 anchor=55-ok
S051:Q7 OK occurrences=1 anchor=74-ok      S051:Q17 OK occurrences=2 anchor=96-ok
S051:Q8 OK occurrences=1 anchor=75-ok      S051:Q18 OK occurrences=1 anchor=99-ok
S051:Q9 OK occurrences=2 anchor=77-ok
S051:Q10 OK occurrences=1 anchor=79-ok     S051:Q12 OK occurrences=1 anchor=88-ok
S051:Q15 OK occurrences=1 anchor=90-ok     S051:Q16 OK occurrences=1 anchor=95-ok
source_recheck_s051_exit=0
```

### 4. Kill-rule probes on the landed bytes (not only at base)

Copy of the landed tree (`rsync -a --exclude .git --exclude .jj --exclude .ufo`, 202 files) with a
re-measured baseline `A=17 B=51 C=1 D=1 entries=20 pass=20 exit=0`; each mutant is a fresh copy of
that tree, and the instrument is invoked with `--root $PWD` inside the copy so the mutation cannot
touch the lane:

| mutant | edit | measured |
|---|---|---|
| m1 | delete the `F17` row from `corpus/README.md` (`removed_lines=1`) | `A=16`, `entries=19 pass=19 exit=0` → detected by counter A |
| m2 | delete the `S051` row from `corpus/SOURCES.md` (`removed_lines=1`) | `B=50`, `C=0` → detected by counters B and C |
| m3 | retype the entry's header id `source: S051 —` → `S052` | `D=0`; harness `FAIL F17 … ids=S052 exit=- problems=header-sources-not-rechecked,selection-not-declared-by-entry`, `entries=20 pass=19 exit=1` → detected by counters D and E |

**Junk-twin control** (`.ufo/waves/round-34/c2-controls/`, committed at `29f606d`;
`junk-f17.md` sha256 `2752a994…4026`):

```
python3 .ufo/waves/round-34/c2-controls/junk-checker.py
junk_twin h1=True source_line=True recheck_line=True
shape_counters=3/3
junk_checker_exit=0
```

so the twin passes every shape counter, as the frozen before states. The twin's own `recheck:` line,
run verbatim at the tip:

```
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
… S051:sha256 OK … 18 assertions OK …
twin_recheck_exit=0
```

i.e. the twin's written recheck command is byte-identical in effect to the real entry's and
**exits 0** — it re-verifies the manifest's assertions, never the twin's sentence. When the twin's
own sentence is asserted instead (scratch manifest carrying the capture + the twin's text),
`source-recheck.py` rejects it:

```
S051:sha256 OK
S051:J1 MISMATCH reason=quote-not-found
probe_exit=1
```

The twin's quoted fragment is also a real substring of the capture
(`corpus/source-snapshots/round-34/S051.txt:75` `- Direct theft of any user funds, whether at-rest or
in-motion, other than unclaimed yield`; `grep -c 'Direct theft of any user funds' S051.txt` → `1`),
so a substring-presence gate would not reject it either. See finding **C2-R3**.

### 5. Independent cross-checks (secondary, not C2 counters)

- `python3 corpus/instruments/source-recheck.py` (entry `recheck:` line) run from `cwd=/` → exit 0:
  the Q10 "runs from any cwd" clause holds; the line also passes `bash -n` (`bash_n_exit=0`).
- Entry contract spot check: `source: S051 — …` at line 3, `verified-at: 2026-10-26` at line 4,
  `ground: F17` at line 5, one `source: S051 ` header line; `grep -nE 'TODO|FIXME|<LANE_HASH>|TBD|XXX'`
  on the entry → no match (`exit=1`).
- `python3 corpus/instruments/capture-binding-check.py` → `MANIFEST round-34 records=1 url_bound=1
  fetched=1 archival=0`, `AUDIT records=41 with_url=41 … orphans=1 orphan=S040-live.txt`,
  `records=41 bound=41 unbound=0`, exit 0 — the S051 record raises the round-33 audit from 40 to
  41, exactly as `.ufo/waves/round-34/claims-erratum-1.md` rules.
- No receipt records a REFUSE verdict on the junk twin: the `REFUSE` hits in `wave1/*.md` are
  unrelated (standing assimilation refusals in `ScribeAssimilationGate.md:137-140` /
  `ScoutPackageThemes.md:11-14`, C1 row text in `RevC1BeforeAfter.md:206`, the real entry's
  "No criterion fails; no REFUSE grounds" in `RevEntryF17.md:152`). Two independent measures agree:
  `CritOverclaim.md:92-93` — "No reviewer REFUSE for `junk-f17.md` exists in `wave1/` at read
  time" — and `RevC2BeforeAfter.md:282-287` — "The non-author reviewer REFUSE record was not yet on
  disk at my final measure".

### 6. Findings (for the L1; this seat does not judge the round)

- **C2-R1 — C2 `after` wording "every assertion occurrences=1" is not what the capture check
  prints.** 16 of 18 S051 assertions print `occurrences=1`; `S051:Q9` prints
  `occurrences=2 anchor=77-ok` and `S051:Q17` prints `occurrences=2 anchor=96-ok`, both accepted
  under QUALITY Q9 ("exactly-once **or** carries an `anchor` line number the instrument verifies",
  `corpus/QUALITY.md:64`). The C2 kill rule (`source-recheck S051 exit != 0`) does **not** fire —
  exit is 0 — but the predicate text overstates the reading. The landed entry's own `recheck:` note
  already says "each `occurrences=1` or anchored (Q9/Q17)", so the entry and the claim disagree in
  words, not in outcome. A one-line erratum (the `claims-erratum-1.md` pattern) would align it.
- **C2-R2 — `PASS F17 ids=S051` is not a grep-able literal.** The harness prints
  `PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0`;
  `grep -c 'PASS F17 ids=S051'` on the output → `0`, `grep -cE 'F17.*ids=S051'` → `1`. The claims'
  `after` uses an ellipsis form; the C2 predicate and the wave context do not. Same defect as
  `ScoutDatawalk.md` F-4, measured independently here.
- **C2-R3 — the junk-twin rejection has no runnable landed form, and the kill-rule literal fires
  under a strict reading.** The twin's own `recheck:` line exits 0 (above), its quoted fragment is a
  genuine capture substring at `S051.txt:75`, and no committed instrument reads entry bodies
  (`grep -ln 'verified-at' corpus/instruments/*.py` → no match). What does reject the twin's own
  sentence is a scratch manifest that asserts it (`quote-not-found`, exit 1) — my probe, and the
  same result is recorded by `ExecHarnessAfter.md` §F-B (`junkman_exit=1`) and
  `ScoutDatawalk.md` F-1/F-1b. The frozen kill-rule clause "junk twin passes source-recheck" is
  literally true for the committed control, so C2's `after` item "source-recheck exit != 0 and
  non-author reviewer REFUSE on record" is **half demonstrated at my final measure**: the
  quote-binding demonstration exists (three seats), the reviewer-REFUSE record and a committed
  gate command do not. `corpus/instruments/r-defect-closure.sh` (C1) checks only that
  `junk-f17.md` exists (per `ScoutDatawalk.md` F-1b), so `closed=9/9` does not close this either.
  L1 adjudication needed: either add a committed gate (bind each entry's quoted sentence to the
  capture) or restate the clause as reviewer-only.
- **C2-R4 — mid-flight instrument regression I observed and reported (resolved before my final
  measure).** At 05:35Z the worktree `frontier-recheck-count.py` (`+152/-3` vs HEAD, rule A reverse
  direction `recheck_ids ⊆ header source: ids`) printed `entries=19 pass=14 exit=1` with F01–F05
  `problems=selection-not-in-header-sources`, while the same tree under HEAD instrument bytes
  printed `entries=19 pass=19 exit=0` (control: `git show HEAD:… > scratch/frc-head.py; python3
  scratch/frc-head.py --root $PWD`). Cause was structural — F01–F05 declare one header `source:`
  line while their rows select 2–4 ids and their recheck lines verify all row ids — so the reverse
  direction could not bind against header lines alone. I reported it to `ExecFrontierBidirectional`
  and `ExecRegressionC1-2`; the landed rule A binds `declared = header source: lines ∪ per-source
  evidence items`, and F01–F05 PASS at my final measure. **This is the exact class of defect the C2
  harness counter would have caught only after the fact**, and it is why the after-battery must run
  at quiescence: at 05:35Z a naive after-battery would have reported `pass=14` as a C2 mismatch.
- **C2-R5 — hygiene: stray untracked file in the lane root.** `selftest-baseline.txt` (1552 B,
  `git status` `??`, mtime 2026-10-26 02:37 local) sits in the lane root; its content is a
  capture-binding `--selftest` case log (`selftest case=clean-all-pass exit=0 want=0 verdict=pass`
  …). No committed artifact references it, no receipt claims it, and it is not under any assigned
  path — a seat's selftest output leaked out of scratch. It should not be swept into the round-34
  commit.

### 7. Limits and residual risk

- Every number above is measured on **uncommitted worktree bytes** at tip `206e510`; the digests in
  §1 name exactly the bytes. Post-integration the L1 should re-run the seven commands (they are
  cheap: the battery takes 1.5 s) — a commit that changes no bytes changes no counter, but a later
  scribe edit to `corpus/README.md`, `corpus/SOURCES.md` or the F17 entry can move A–E.
- The harness depends on rule A's `declared` set now including per-source evidence items
  (`- S002, "…"`); entries that declare sources only in body prose outside that shape would not
  bind. That boundary is C1's subject (`ExecFrontierBidirectional.md` §7 discloses the residual),
  and it is recorded here because counter E reads it.
- Counter G reads the live lane registry through `--root`; it is a live-tree verdict, not a
  frozen-bytes one.
- I did not run any build/lint/test suite (editing-wave policy) and did not re-verify C1's counters
  beyond the cross-checks in §5.

### 8. Scratch state

Scratch root `/fast/scratch/hyaku/kasegi-r34/ExecRegressionC2/` (base extraction, four batteries,
mutant copies, probe manifest, watcher logs) was removed before yield — `rm -rf` returned 0 and
`ls -d` on the path now prints `No such file or directory` (exit 2); the two evidence appendices
below were copied into the wave dir first. No work tree remains on disk.

### Evidence appendices

- `ExecRegressionC2-battery-final.txt` — the full `q4` battery (digests, all seven commands, exit
  codes, supporting probes) as measured at 2026-10-26T05:46:50Z
  (`sha256 51e548ec2becaa36bf3db9ea245483202de3da5c250cef8d4e481099d065275a`, 125 lines).
- `ExecRegressionC2-battery-base.txt` — the base-commit (`014ee2d`) before-battery
  (`sha256 d083370cff0925fb3803ce05eaa808fb0b0fa45fa3749c4afd7541f6ac23b7f8`, 19 lines).
