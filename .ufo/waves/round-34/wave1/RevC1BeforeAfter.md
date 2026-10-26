# RevC1BeforeAfter — independent before→after verification of C1 (round 34)

Seat: reviewer, kasegi-shokunin round 34 wave 1 (id `RevC1BeforeAfter-2`). Mandate: re-derive
every C1 counter from `.ufo/waves/round-34/claims.json` with its own command at the tip and
compare against the frozen before receipt (`.ufo/waves/round-34/c1-controls/before.txt`) and the
claimed after-values. I did not author any of the changes. Lane base
`014ee2d7aa8c3c095ff57ae51097606a9906228c`; claims freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13`.

## Report

### 0. Method and timing

Three measurement passes, all commands run from the lane root
(`/home/vgpnk/Projects/shokunin/kasegi-shokunin`), exit codes captured with `echo "EXIT=$?"`:

- **Pass 1 (~05:26–05:31Z):** wave 1 still in flight — the C1 instruments did not exist at the
  tip yet (outputs in §2 pre-landing block). Working tree then had 4 modified files
  (SCORECARD.md, QUALITY.md, frontier-recheck-count.py, round-32 manifest).
- **Pass 2 (~05:33–05:36Z):** instruments landed mid-pass; suite measured `closed=8/9 exit=1`
  (R4 open), selftest `cases=9 failures=1` (same R4 limb), the other four counters already at
  after-values.
- **Pass 3 (final, stamped 2026-10-26T05:39:56Z, HEAD `206e5108f1190e61b3e2622d21cab8a5d921650c`,
  wave-1 work uncommitted in the working tree, 20 dirty/untracked paths):** all six counters at
  after-values. §2 quotes the final pass; §5 records the in-flight observations.

Before side re-derived from base bytes (`git show 014ee2d:<path>`), plus a full base-tree export
(`git archive 014ee2d | tar -x -C <scratch>/base-tree`) used for the plain-audit baseline, the
suite's base-tree run, and the kill-rule counter's base-bytes replay. Scratch:
`/fast/scratch/hyaku/kasegi-r34/RevC1BeforeAfter/` (removed before yield; this receipt first
copied into the wave dir).

### 1. Before side — frozen receipt vs my re-derivation at base `014ee2d`

| # | Frozen before-receipt value | My command at base | My result | Match |
|---|---|---|---|---|
| B1 | `r-defect-closure.sh` absent (`ls_exit=2`) | `git cat-file -e 014ee2d:corpus/instruments/r-defect-closure.sh` | `fatal: path … does not exist in '014ee2d'`, exit 128 (absent; different tool, same fact) | ✓ |
| B2 | capture-binding `--selftest` → `cases=11 failures=0` | base bytes copied to scratch, `python3 <scratch>/base-capture-binding-check.py --selftest` | `selftest cases=11 failures=0`, exit 0; the 11 case names identical to the pre-land tip output (incl. `url-matching-two-rows`) | ✓ |
| B3 | `<LANE_HASH>` count 2 | `git show 014ee2d:SCORECARD.md \| grep -c '<LANE_HASH>'` | `2` | ✓ |
| B4 | round-32 manifest `fetched_utc` = `2026-10-25T23:14:00-03:00` ×2 | `git show 014ee2d:corpus/source-snapshots/round-32/manifest.json \| grep -n fetched_utc` | lines 10 and 59: `"fetched_utc": "2026-10-25T23:14:00-03:00"` | ✓ |
| B5 | round-26 manifest `records= 1 paths= ['S041.txt']` (no S040 record) | python one-liner over `git show 014ee2d:…round-26/manifest.json` | `records= 1 paths= ['S041.txt']` | ✓ |
| B6 | QUALITY "exactly one" occurrences 1 | `git show 014ee2d:corpus/QUALITY.md \| grep -c 'exactly one'` | `1` | ✓ |
| B7 | round-33 lesson erratum marker `4` | `git show 014ee2d:corpus/lessons/round-33.md \| grep -c 'Erratum'` (capital E) | `4` (case-insensitive gives 8; before.txt does not record its command — the value reproduces only under the case-sensitive reading) | ✓ |
| B8 | plain-audit baseline (absent from the frozen before receipt; claims call it the "unchanged C1 instrument baseline") | base tree export; `python3 <scratch>/base-tree/corpus/instruments/capture-binding-check.py --root <scratch>/base-tree` | `AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2` then `records=40 bound=40 unbound=0`, exit 0 | ✓ (baseline 40/40/0 at base) |

**Verdict: the frozen before receipt is honest** — every value I re-derived matches; B8
supplements it with the one counter it omits.

### 2. After side — the six C1 counting commands at the tip (final pass, 05:39Z)

**Counter 1 — `bash corpus/instruments/r-defect-closure.sh`** → exit 0

```
R1 check=SCORECARD.md lane-hash-markers=0 + appended 'Correction (round 34)' naming 7963976e/014ee2d open=0
R2 check=SCORECARD.md round-33 'Erratum 2' per-id restatement + QUALITY.md R22 pre-freeze step open=0
R3 check=QUALITY.md appended round-34 note below R20 (per-id supersedes 'exactly one') open=0
R4 check=tightened kill rule recorded (selftest case= per case, cases>=11) + round-33 lesson R4 3-of-4 erratum open=0
R5 check=capture-binding-check.py url-matching-two-rows=0 cases=21 (>=11) open=0
R6 check=round-26 manifest binds S040-live.txt (record or orphan list) + purpose corrected open=0
R7 check=round-33 lesson appended R7 erratum (19->31, 23->22 characters, S050.txt:70) open=0
R8 check=round-32 manifest fetched_utc strict UTC (^YYYY-MM-DDTHH:MM:SSZ$), no '-' offset open=0
R9 check=capture-binding H4-H8 cases=9 + frontier rule A bidirectional (mirror=0 reverse=1) + junk=.ufo/waves/round-34/c2-controls/junk-f17.md open=0
closed=9/9 exit=0
```
Claim: `closed=9/9 exit=0` → **MATCH**.

**Counter 2 — `bash corpus/instruments/r-defect-closure.sh --selftest`** → exit 0

```
selftest case=R1 live=pass fixture=rejected verdict=pass
selftest case=R2 live=pass fixture=rejected verdict=pass
selftest case=R3 live=pass fixture=rejected verdict=pass
selftest case=R4 live=pass fixture=rejected verdict=pass
selftest case=R5 live=pass fixture=rejected verdict=pass
selftest case=R6 live=pass fixture=rejected verdict=pass
selftest case=R7 live=pass fixture=rejected verdict=pass
selftest case=R8 live=pass fixture=rejected verdict=pass
selftest case=R9 live=pass fixture=rejected verdict=pass
selftest cases=9 failures=0
```
Claim: `cases=9 failures=0` → **MATCH**. Each of the nine checks is shown able to fail on a
defect-bearing fixture copy (`fixture=rejected` for all nine).

**Counter 3 — `python3 corpus/instruments/capture-binding-check.py --selftest`** → exit 0

```
selftest case=clean-all-pass exit=0 want=0 verdict=pass
selftest case=missing-manifest-dir exit=1 want=1 verdict=pass
selftest case=record-without-url exit=1 want=1 verdict=pass
selftest case=shared-url-between-two-records exit=0 want=0 verdict=pass
selftest case=duplicate-id-rows exit=1 want=1 verdict=pass
selftest case=url-mismatch exit=1 want=1 verdict=pass
selftest case=no-row exit=1 want=1 verdict=pass
selftest case=shared-url-not-a-failure exit=0 want=0 verdict=pass
selftest case=round-32-record-without-fetched_utc exit=1 want=1 verdict=pass
selftest case=pre-round-32-record-without-archival exit=1 want=1 verdict=pass
selftest case=round-32-record-with-fetched_utc-passes exit=0 want=0 verdict=pass
selftest case=pre-round-32-archival-passes exit=0 want=0 verdict=pass
selftest case=fetched-utc-pending-rejected exit=1 want=1 verdict=pass
selftest case=fetched-utc-local-offset-rejected exit=1 want=1 verdict=pass
selftest case=per-file-orphan-detected exit=1 want=1 verdict=pass
selftest case=per-file-orphan-listed exit=0 want=0 verdict=pass
selftest case=nested-snapshot-dir exit=0 want=0 verdict=pass
selftest case=nested-snapshot-missing-manifest exit=1 want=1 verdict=pass
selftest case=dup-record-in-manifest exit=1 want=1 verdict=pass
selftest case=double-https-row exit=1 want=1 verdict=pass
selftest case=rejected-row-anchor exit=1 want=1 verdict=pass
selftest case=summary-only-selftest-rejected exit=1 want=1 verdict=pass
selftest case=complete-selftest-report-accepted exit=0 want=0 verdict=pass
selftest cases=23 failures=0
```
Claim: `selftest cases=N failures=0` with N≥19 → **MATCH** (N=23). All nine claim-named cases
present verbatim: `per-file-orphan-detected`, `per-file-orphan-listed`, `nested-snapshot-dir`,
`fetched-utc-pending-rejected`, `fetched-utc-local-offset-rejected`, `dup-record-in-manifest`,
`double-https-row`, `rejected-row-anchor`, `summary-only-selftest-rejected`. R5's rename landed:
`url-matching-two-rows` is gone, split into `shared-url-between-two-records` (control, want 0)
and `duplicate-id-rows` (dup-id fixture, want 1).

**Counter 4 — `python3 corpus/instruments/kill-rule-check.py`** → exit 0 (verdict lines quoted
verbatim; the full run additionally prints per-mutant patch/bytes/probe lines and six `GATE ok`
lines):

```
KILL-RULE instrument=corpus/instruments/capture-binding-check.py sha256=3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa bytes=40556 lines=892 floor=19 counter_sha256=1af15e592acc3ad794bba48b79e9a08c3462fd75dc358de7f2df720151045742
mutant=skip-selftest-summary killed=1
mutant=accept-record-without-url killed=1
mutant=per-file-binding-removal killed=1
controls=4 rejected=4
gates=6 failed=0
survivors=0
```
Claim: `survivors=0` → **MATCH**. This is a real mutant replay, not the do-nothing control: it
patches a copy of the landed instrument bytes (three exactly-once textual patches), probes each
mutant on a selftest-shape oracle plus two external fixture lanes, and rejects all four controls
(`CTL-noop` → `invalid:noop`, `CTL-nocompile` → `invalid:nocompile`, `CTL-equivalent` → witness
survivor, `CTL-fake-killrule` → `opaque`, `differs=1` against
`.ufo/waves/round-34/c1-controls/fake-killrule.py`).

**Counter 5 — `grep -c '<LANE_HASH>' SCORECARD.md`** → `0`, exit 1 (grep no-match).
Claim: 0 → **MATCH**. The appended correction is at `SCORECARD.md:1116-1119`: "Correction
(round 34): the two lane-hash placeholders above (R1) were replaced with the round-33 final hash
`7963976e60b2564860553c6ab4838128d5ca06ea` (lane tip `014ee2d7aa8c3c095ff57ae51097606a9906228c`
after the verifier spot-check commit)".

**Counter 6 — `python3 corpus/instruments/capture-binding-check.py`** (plain audit) → exit 0

```
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=41 bound=41 unbound=0
```
Claim literal: `records=40 bound=40 unbound=0 exit=0` → **DIFFERS on `records` (41 vs 40),
MATCHES on `bound`/`unbound`/exit** — and the difference is already ruled by the L1:
`.ufo/waves/round-34/claims-erratum-1.md` (filed pre-integration, untracked at measurement time)
rules the frozen literal "40" a snapshot-of-round-33 scope note and states the measured
after-state as `records=41 bound=41 unbound=0 exit=0` once S051's registry row lands. My
observation equals the ruled after-state exactly. The C1-invariance reading also holds: at base
the same audit printed 40/40/0 (§1 B8), and C1's own changes moved none of those 40 records —
the +1 is C2's S051 manifest record (`MANIFEST round-34 records=1 url_bound=1 fetched=1`).

### 3. Predicate demonstrations beyond the six counters

- **Suite fails on the base tree** (C1 predicate: "the suite fails on the base tree,
  `closed=0/9`"): `bash corpus/instruments/r-defect-closure.sh --root <scratch>/base-tree` →
  all nine checks `open=1`, `closed=0/9 exit=1`. R1 names `lane-hash-markers=2`, R5 names
  `url-matching-two-rows … (count=2)`, R8 names the non-UTC `fetched_utc`, R9 names all nine
  missing H4–H8 case names — the base state the frozen before receipt describes.
- **Suite determinism:** two consecutive runs byte-identical stdout (both sha256
  `7e8b6ff84cfa94b33a3385c6493c275fff74ea41756a5fbaad5470eccdd978ab`), both exit 0.
- **Kill-rule counter replayed against base bytes** (`--instrument
  <scratch>/base-tree/corpus/instruments/capture-binding-check.py`, base digest
  `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9`, 492 lines):
  `mutant=skip-selftest-summary killed=0` (the F-5 survivor the before receipt records),
  `mutant=per-file-binding-removal killed=0` (no per-file limb in base to remove),
  `mutant=accept-record-without-url killed=1` (killed even on base bytes by the tightened
  rule's external fixture oracle — the rule, not the instrument, is what changed for this
  mutant), `gates=6 failed=4` (base selftest has 11 cases < floor 19), `survivors=1`, exit 0.
  Same counter, both trees: base `survivors=1` → landed `survivors=0`. The before receipt's
  survivor story is reproduced by the landed instrument itself.
- **Frontier rule A bidirectionality (R9):** `python3 corpus/instruments/frontier-recheck-count.py
  --selftest` → `selftest cases=6 failures=0`, exit 0, with both directions pinned
  (`header-source-not-rechecked` want 1; `selection-not-declared` want 1; controls
  `bidirectional-holds`, `evidence-list-declares-selection` want 0). See §5 F3 for the
  mid-wave failure I caught and its fix.

### 4. Remaining C1 after-items, spot-verified (R1–R9 map)

| Defect | After-item | Evidence at tip | Verdict |
|---|---|---|---|
| R1 | 0 `<LANE_HASH>` + correction naming `7963976e`/`014ee2d` | counter 5 = 0; `SCORECARD.md:1116-1119`; suite R1 `open=0` | closed |
| R2 | Erratum 2 restating the per-id parenthetical + pre-freeze satisfiability step | `SCORECARD.md:1014-1027` ("Erratum 2, disclosed (round-34 append, round-25 form)"), `:1028-1035` ("Pre-freeze satisfiability step, recorded (QUALITY R22)"); `corpus/QUALITY.md:226` R22 row; suite R2 `open=0` | closed |
| R3 | Appended note below QUALITY R20 | `corpus/QUALITY.md:220-222` ("Note (round 34): R20's 'exactly one registry-row URL' reading is superseded by the C1 erratum-2 per-id reading…"); suite R3 `open=0` | closed |
| R4 | Tightened kill rule recorded + round-33 R4 erratum correcting the overstatement | `corpus/QUALITY.md:228` R24 row ("…one `selftest case=<name>` verdict line per case with cases>=11…"); `corpus/lessons/round-33.md:215` "## Erratum (round 34) — R4: 'all mutants killed' overstated; the frozen kill rule caught 3 of 4" (after the `:136` provenance anchor; 3-of-4 figure at `:225`, `:237`); counter 4 `survivors=0`; suite R4 `open=0` | closed |
| R5 | `url-matching-two-rows` renamed | counter 3 output (case gone; `shared-url-between-two-records` + `duplicate-id-rows` present); suite R5 `open=0` | closed |
| R6 | S040-live.txt manifest record or orphan listing + round-26 purpose corrected | `corpus/source-snapshots/round-26/manifest.json` now carries an `orphans` array (S040-live.txt with sha256 `b7f7b55f…`, row S040, both URLs, `fetched_utc 2026-10-25T12:34:27Z`) and a rewritten purpose ("accounts for exactly the two files committed in this directory"); audit prints `orphans=1 orphan=S040-live.txt`; suite R6 `open=0` | closed |
| R7 | Round-33 lesson R7 erratum (31/22 counts, S050.txt:70) | `corpus/lessons/round-33.md:140-213`; I independently re-derived the erratum's own numbers: the two quotes at lesson `:31`/`:32` measure 31 and 22 characters excluding the 「」 brackets (33/24 including), each occurs exactly once (`grep -cF` → 1) at `S049.txt:214` and `S050.txt:591`, and `sed -n '69,71p' S050.txt` shows the heading at L69 with the applicability sentence opening at L70 | closed (erratum's figures verified correct) |
| R8 | Round-32 manifest strict-UTC only | diff: both `fetched_utc` now `2026-10-26T04:16:06Z` / `2026-10-26T04:16:16Z`; suite R8 regex check `open=0` | closed |
| R9 | Rule A both directions + junk twin committed and rejected | harness selftest 6/6 (§3); junk twin committed at the freeze commit (`git ls-tree 29f606d …c2-controls/` → `junk-f17.md` blob `50f7a84c`); suite R9 `open=0`. The rejection limbs (source-recheck exit ≠ 0; non-author reviewer REFUSE) are C2 counters — cross-reference `RevC2BeforeAfter`'s receipt; not re-derived here | closed for C1's scope (rejection limbs deferred to the C2 seat) |

### 5. Findings

- **F1 — in-flight measurement window (resolved).** Pass 1 found the C1 state still at
  before-values at the tip: `r-defect-closure.sh` absent (exit 127), `kill-rule-check.py` absent
  (exit 2), capture-binding `--selftest cases=11` (base value), plain audit
  `FAIL rule=missing-manifest dir=round-34 … records=40 bound=40 unbound=0`, exit 1. Passes 2–3
  show the wave landing: instruments → suite 8/9 (R4 open) → 9/9. No defect in the final state;
  recorded so the L1 can order receipts against the landing timeline.
- **F2 — frozen counter-6 literal vs landed tree (already ruled).** Observed `records=41` vs the
  frozen literal `records=40`; explained and pre-ruled by
  `.ufo/waves/round-34/claims-erratum-1.md` (S051's round-34 record). Residual: at measurement
  time the erratum file was untracked and its promised disclosure "on every surface that reads
  the C1 counter" was not yet visible in SCORECARD/QUALITY/round-33.md (the round-34 SCORECARD
  section does not exist yet — it lands at integration). The L1 should land that disclosure with
  the integration commit.
- **F3 — frontier-recheck selftest failed mid-wave, fixed in-flight.** At ~05:33Z the modified
  `frontier-recheck-count.py` printed `selftest cases=4 failures=1`: case `extra-source-not-cited`
  expected `problems=selection-not-in-header-sources,selection-not-cited-by-entry` but only the
  first fired. Mechanism (read from the then-current bytes): `build_fixture` writes every
  recheck-selected id into the prose line (`Body cites S001, S002, S003.`) and `entry_contract`'s
  `cited` set scans the whole file including the `recheck:` line, so `selection-not-cited-by-entry`
  could never fire — the limb was vacuous as built. The landed state replaced the case set
  (6 cases, `selection-neither-declared-nor-mentioned` among them) and now prints
  `cases=6 failures=0`, exit 0. No action needed; recorded as caught-and-fixed in flight.
- **F4 — kill-rule-check bytes changed between my runs.** First run printed
  `counter_sha256=e1737783b1edea23e8966d3e5c9a95ac50644fd8130008b7704d253d0bbcd9f7`; both later
  runs print `counter_sha256=1af15e592acc3ad794bba48b79e9a08c3462fd75dc358de7f2df720151045742`
  (= the file's current sha256). Verdict structure identical across runs
  (`mutants=3 killed=3 survivors=0 invalid=0`, `controls=4 rejected=4`, `gates=6 failed=0`).
  In-flight edit by the author seat; final bytes stable across my last two runs.
- **F5 — stray untracked file at the lane root.** `selftest-baseline.txt` (1552 B, mtime
  2026-10-26 02:37:05 -0300 = 05:37:05Z) holds the landed capture-binding selftest's 23-case
  output. No instrument writes that filename (grep over `corpus/instruments/*.py *.sh` → no
  match), so it is a seat's manual capture left in the lane root instead of
  `/fast/scratch/hyaku/kasegi-r34/<seat>/` or the wave dir. Not deleted by me (not my file);
  the L1 should drop it or have its author relocate it before the integration commit.
- **F6 — suite R5's case-tuple count reads 21 vs the selftest's 23 printed cases.** The suite's
  R5 floor check greps `^\s*\("[a-z0-9-]+",` (21 hits) while the selftest prints 23 case lines;
  the delta is the counting regex, not missing cases (kill-rule-check's case-set equality
  23=23 binds the real set). Both floors clear; cosmetic, no action required.
- **F7 — before-receipt command provenance.** before.txt prints values without their commands;
  B7's `4` reproduces only as case-sensitive `grep -c 'Erratum'` (case-insensitive gives 8).
  Every value did reproduce; suggest the next freeze receipt records the command beside each
  value.

### 6. Verdict

C1's after-state is **verified at the tip** as of 2026-10-26T05:39:56Z: all six counting
commands reproduce the claimed after-values (counter 6 under the L1's round-34 erratum-1
reading), the suite fails 0/9-closed on the base tree and passes 9/9 at the tip with a
deterministic, self-testing implementation, and the kill-rule counter demonstrates the
before→after mutant story on real replayed bytes (base `survivors=1` → landed `survivors=0`).
Open items for the L1: F2's disclosure surfaces, F5's stray file. No C1 counter is red.

### 7. File digests (sha256, measured 05:39Z)

```
7aca98b344d4ca8718344cc09c63b67b2382fd327d579e6b6a2c713b351e08ab  corpus/instruments/r-defect-closure.sh
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py
1af15e592acc3ad794bba48b79e9a08c3462fd75dc358de7f2df720151045742  corpus/instruments/kill-rule-check.py
87b14892dfc42792056c7a9f09a0783e9d749d0478f376841c98bfc25e0a7c29  corpus/instruments/frontier-recheck-count.py
b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0  SCORECARD.md
2bb724fb65ef37e9c9af954cb932bb5e7f21c5576b726be55e1bf541012d1090  corpus/QUALITY.md
f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807  corpus/lessons/round-33.md
72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6  corpus/source-snapshots/round-32/manifest.json
33ac33c3caa6d43f3772b8cf8532b37cdb50f48db8ba667b5dd90645e8eacefa  corpus/source-snapshots/round-26/manifest.json
dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850  .ufo/waves/round-34/claims.json
```

### 8. Environment

- No tools installed or upgraded (stdlib python3 + coreutils only); tooling authorization unused.
- No git/jj mutations performed (read-only `git show`/`git archive`/`git status`/`git ls-tree`
  only); no writes outside the lane repo; scratch dir removed before yield.
