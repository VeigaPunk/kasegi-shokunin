# K72ScribeLesson: round-72 lesson and mistake mining (draft, attempt 1)

Seat: scribe (leaf). Draft only; nothing was written into the lane. The L1 (`KasegiR72`) copies the
four drafted sections (`## Mistakes`, `## Gate`, `## Routed defects`, `## Residuals`) into
`corpus/lessons/round-72.md` after integration. Section 1 is working notes for the Mistakes section.

## 0. What was run, and what was not

Commands run by this seat, with observed output:

- `S=/fast/scratch/hyaku/kasegi-r72/K72ScribeLesson; mkdir -p "$S"`, then
  `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show a34ce4c:corpus/instruments/figure-audit.py > "$S/base-gate.py"`
  (read-only git; output redirected into my scratch only).
- `sha256sum "$S/base-gate.py" <lane>/corpus/instruments/figure-audit.py <lane>/corpus/instruments/derive-head-census.py` →
  `182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603` (base),
  `b146c81a29437aef2d4e91576782a2829570ac12f13888cad099d6081d1fefdc` (candidate, working tree, uncommitted),
  `255fd4072dfe8e2a6bf53d5fcc0f92d2af486d40711d03c4573a4017ccd8db52` (census counter). All three equal the pins in the spec.
- `git -C <lane> cat-file -t a34ce4c` → `commit`; `git -C <lane> show a34ce4c:corpus/instruments/derive-head-census.py | sha256sum` →
  `255fd4072dfe8e2a6bf53d5fcc0f92d2af486d40711d03c4573a4017ccd8db52  -` (matches the counter pin).
- `sha256sum corpus/source-snapshots/round-72/S107.txt; wc -l ...` → `0b944ea123efa204f1c0539c7d9d8f0367c25741210290681099fb6429254652`, `1176`.
- Reads (`read` tool, line ranges): round-71 spot-check 1-153; round-71 sentinel `SentinelC1.md` §§1-6 (rows 1-33 and §4-§5);
  round-71 and round-72 `claims.json`; both `controls/` receipts; `figure-audit.py` candidate and base; `derive-head-census.py`;
  `corpus/source-snapshots/round-72/S107.txt` (1-300) and `manifest.json`; `corpus/README.md:1108-1128`; `w1-spec.json`.
- The `grep` tool did not resolve the `/fast/scratch` path (`Path not found`); the base gate was read with `read` instead.

Not run by this seat: the candidate gate, the census counter, and any mutant or probe. The kill matrix (K72Mutate), the
attack verdict (K72AttackCensus), the candidate probe (K72ExecProbe) and the S107 fetch (K72ScoutCapture) were still running
when this draft was written. Every value this draft attributes to those seats is marked **pending** and is not claimed here.

Scratch `/fast/scratch/hyaku/kasegi-r72/K72ScribeLesson/` holds only the base-gate copy; it is removed at hand-off.

## 1. Mining notes: round-71 sources behind R1 and R2

Source lines relied on (file:line, verbatim or trimmed with `…`):

- Spot-check `corpus/lessons/round-71-verifier-spotcheck.md`
  - `:13-14` "Verdict of record: **C1 not verified (the lane's own ruling, confirmed) with a measured regression → axis `depth:verifiability` harmed; C2 verified.**"
  - `:38-39` "**K71-A** — the harm count "23 censused heads" (report, lesson M71-4, SCORECARD) does not reproduce;"
  - `:66-68` "the counter passes R5–R8 through its `direct_rc != 0 → stale` branch … every one of those four commands exits 1 on this tree"
  - `:71-73` "the declared clause "re-deriving each one's own value" is false for 4 of the 8 positive rows, and R8 compares `"" == ""`"
  - `:77-80` "the r71 gate holds `PY_DENIED_ANY` = three names plus a 10-script `PY_DENIED_BY_SCRIPT` over a 44-head census. An ast read … gives **43** heads that re-admit at least one base-denied name, and **26** of them where the head's own `add_argument` declares that name — not the 23 the report states (K71-A)."
  - `:83-84` "a named r70 refusal guarantee is now false, change caused by this round."
- Sentinel `.ufo/waves/round-71/w2/SentinelC1.md`
  - `:85` row 23: "**22,012 files written under `--work`** (a copy of the base tree incl. `.git` …)"
  - `:90` row 28: "**wrote `out/alias.json` (2,595 bytes)** — the per-script `--json` denial is gone under the alias"
  - `:106-108` R1 "`--work`/`--root`/`--scratch` are no longer refused globally, and the per-script table only covers ten heads. Static census of the census: **23 heads** re-admit at least one base-denied flag"
  - `:119-121` R2 "the census is keyed on basename while containment is keyed on realpath, so an in-dir alias under a `PY_SELFTEST_FIXTURE_HEADS` name restores the denied flags of the file it points at."
- Round-71 frozen claims `.ufo/waves/round-71/claims.json`
  - `:14` declared: "… a python head not in the census is refused (fail closed)." (here "census" means the head allowlist `PY_SCRIPT_CENSUS`, not a write-class counter.)
  - `:19-51` probe_set: N1-N12 and R1-R8 (every row names a real instrument, none is a symlink or a `--work` head); `:49` whole_gate "no-write-side-effect: fixture trees byte-identical, marker_runs=0".
  - `:58` scope: "non-denied options … stay open and the lesson names them."
- Do-nothing census receipt `.ufo/waves/round-72/controls/c1-census-donothing-r72.txt`
  - `:4` "base gate sha256: 182f4ef7…"; `:8-26` 19 `READMITTED-ROW` lines; `:27` "CENSUS heads=45 write_class_pairs=5 READMITTED=19"; `:28` "ALIAS-PROBE verdict=admitted rc=1"; `:30` "CENSUS-RESULT defect"; `:31` "EXIT=1".

Class of R1. The round-70 gate refused `--root/--out/--output/--json/--scratch/--url/--work` for every python head. The round-71
gate kept three names global and moved the rest into a 10-entry per-script table. Every head absent from that table therefore
inherited *allow*. The round-71 predicate checked the enumerated rows (N1-N12, R1-R8, `claims.json:19-51`) and not the
population, so the lost guarantee was never a predicate row. The spot-check and sentinel both record that the change caused the
loss (spot-check `:83-84`).

Class of R2. The head policy was looked up by `os.path.basename(parts[1])`, the spelling in the derive string, while containment
used `realpath` (base `figure-audit.py:493` and `:501-505`). An in-directory symlink with a fixture name therefore took the
policy of the name and the file of its target. The round-71 probe set contained no alias row.

Three different counts are in circulation for "the heads that re-admit a write-class flag". They use three predicates and must not
be merged:

| source | count | predicate |
|---|---|---|
| sentinel `:108` | 23 heads | names re-admit at least one *base-70* denied flag (the 7-name list) by static census of the round-71 tables |
| spot-check `:77-80` | 43 heads, 26 declared | 43: r71 tables lack at least one base-denied name; 26: of those, the head's `add_argument` declares that name (ast read; "a 44-head census") |
| census receipt `:8-27` | 19 pairs (15 `--work`, 4 `--scratch`) | `WRITE_CLASS = (--out,--output,--work,--scratch,--url)` (census `:40`) declared and not denied by the r71 gate |

The 19 count is a receipt (base control). Its `READMITTED-ROW` lines are 15 `--work` (`:10, :13-26`) and 4 `--scratch` (`:8, :9, :11, :12`).
The candidate's own comment at `figure-audit.py:144-146` says "18 `--work` heads and one `--scratch` head" (routed, section 4).

## 2. Mistakes (round 72)

Field shape: class · evidence pointer · captured-by · fix · able to fail. "Able to fail" lists a red value measured by a receipt and
a green value (pending where the green run is not in hand).

| id | class | evidence pointer | captured-by | fix | able to fail |
|---|---|---|---|---|---|
| M72-1 | **unmeasured narrowing**: a repair changed the default for the whole python-head population (deny-everywhere became deny-where-listed); the frozen predicate measured only the enumerated rows the change was built for, so the base guarantee was never a predicate row | census receipt `.ufo/waves/round-72/controls/c1-census-donothing-r72.txt:8-27` (19 READMITTED-ROW lines, `:27` READMITTED=19); sentinel `.ufo/waves/round-71/w2/SentinelC1.md:106-117` (R1) and `:85` (row 23, 22,012 files written under `--work`); spot-check `corpus/lessons/round-71-verifier-spotcheck.md:83-84`; r71 predicate `.ufo/waves/round-71/claims.json:19-51` (no census row) | **none** at round 71: the frozen round-71 predicate did not contain a write-class census row (claims `:19-51`, `:49`) | Round 72 C1: the write-class census (`corpus/instruments/derive-head-census.py`) and global denial of `--work` and `--scratch` in the candidate, `figure-audit.py:147` `PY_DENIED_ANY = ("--out", "--output", "--selftest", "--work", "--scratch")` (base `figure-audit.py:143` lacked both). Sanity: `EXPECTED_CASES` 106 → 110 (`:226`). | Red: base receipt `:27` `READMITTED=19`, `:30` `CENSUS-RESULT defect`, `:31` `EXIT=1`. Green: **pending**, candidate run with predicate `READMITTED=0`. K72Mutate kill matrix (`.ufo/waves/round-72/w1/K72Mutate.md`, M1 drop `--work`, M2 drop `--scratch`): **pending**. |
| M72-2 | **identity by spelling**: the policy key was the basename of the derive's argv spelling; containment used the realpath of the same token, so the two keys could name different files | base `figure-audit.py:493` `script = os.path.basename(parts[1]…)`, `:501-505` realpath only for containment; sentinel `SentinelC1.md:119-127` (R2) and `:90` (row 28, `out/alias.json` 2,595 B written under `ok.py`→`gate-quote-audit.py`) and `:91` (row 29); census receipt `:28` `ALIAS-PROBE verdict=admitted rc=1` (base) | **none**: the round-71 probe set (`claims.json:20-43`) used real names only; no alias row | Candidate keys the policy on the realpath basename: `figure-audit.py:500-504` (`target = realpath(...)`, `script = os.path.basename(target)`), denial built from it at `:509`. Census ALIAS-PROBE (`derive-head-census.py:115-136`). Residual of the same class: section 5 item 4. | Red: base `:28` `verdict=admitted rc=1`. Green: **pending**, candidate ALIAS-PROBE `verdict=refused rc=2 reason=derive-not-read-only` (the frozen predicate). |
| M72-3 | **count quoted without its predicate**: "23 censused heads" was reported as the harm figure; the same phrase names three different sets (section 1 table) | spot-check `:38-39` (K71-A), `:77-80` (43/26), `:142-143`; sentinel `:108` (23) and `:151-152` (residual 3, "23 heads") | **none** (no round-71 row or criterion covers a harm-count predicate) | This lesson states each count with its predicate (section 1). The spot-check correction ("restate … with its command") is routed, not landed (section 4, K71-A). | Red: the sentence "23 censused heads" with no predicate, as at spot-check `:38`. Green: this table, each row carrying its predicate and receipt. Not re-measured by this seat; the 43/26 figures are the spot-check's ast read. |
| M72-4 | **a counter whose negative branch passes**: a positive row whose direct command exits nonzero is reported as "stale" and passes | spot-check `:66-68` (`direct_rc != 0 → stale` branch of `.ufo/waves/round-71/controls/c1-probe-run-r71.py`); `:71-73` (R8 compares `"" == ""`) | **none** | Not fixed by round 72 (K71-C, section 4). Freeze the counter change before the next use. | Red: the spot-check's four rows R5-R8 exiting 1 yet passing (`:66-68`, read from bytes; not re-run here). Green: **not measured**. |

Mistakes not captured by this round's C1 or C2: M72-3 and M72-4 (routed, section 4). M72-1 and M72-2 are captured by C1.

## 3. Gate (round-72 lesson, C2 source S107)

- URL: https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html
- Access date: 2026-11-05 (`corpus/source-snapshots/round-72/manifest.json:3` "Opened 2026-11-05"; `:15` `fetched_utc` `2026-11-05T03:49:50Z`; `:10` HTTP 200).
- Capture: `corpus/source-snapshots/round-72/S107.txt`, sha256 `0b944ea123efa204f1c0539c7d9d8f0367c25741210290681099fb6429254652`, 1176 lines (measured by this seat).
- Located quote (line 33 of the capture, 12 words):
  "The REST API for creating, changing, and getting the details of bugs."

## 4. Routed defects

Each item names the evidence and the next owner. None is closed by round 72 unless the L1 says so.

- **R-1 · the `--json` and `--root` write-class gap (census blind spot).** The counter's `WRITE_CLASS` is `("--out","--output","--work","--scratch","--url")` (`derive-head-census.py:40`), so it never counts `--json` or `--root`. The base gate denied both globally; the candidate denies them only per script (candidate `figure-audit.py:156-168`; the global tuple at `:147` has neither). A head that declares `--json` or `--root` and is absent from the per-script table is therefore admitted and not counted. Owner: K72AttackCensus (spec item 3). Round 72 does not change the frozen `WRITE_CLASS`; the gap is routed to the next round.
- **R-2 · `freeze-check.py` runs `bash -c` on claims-supplied commands.** Sentinel row 33 `SentinelC1.md:95` (marker `pwned-from-claims`), residual 1 `:131-142`, and the candidate's `PY_HEAD_REFUSED` still lists only `frontier-recheck-count.py` (`figure-audit.py:149-152`). The sentinel also names `r46-c1-gate.py` (line 243) and `limb-mutation-check.py` (line 295) for the same audit. Round 72 excludes it (`claims.json:64`, "NOT repaired this round; it is routed"). Owner: next round; the sentinel's smallest fix is adding `freeze-check.py` to `PY_HEAD_REFUSED`.
- **R-3 · `sort -T` / `--temporary-directory` create and unlink files outside the root.** Sentinel rows 14 `:76` (51,200 `O_CREAT|O_EXCL` opens in `td1`), 15 `:77` (46 opens in `/tmp`), 18 `:80` (51,200 in `td2`); residual 5 `:163-169`. The sentinel's fix is adding `-T` and `--temporary-directory` to `DENIED_FLAGS["sort"]`. Not in the round-72 claims; the candidate's non-python tables were not re-read by this seat. Owner: next round.
- **R-4 · the round-71 harm report says "23 censused heads".** Correct figure under the spot-check's predicate is 43 (any base-denied name) and 26 (declared), spot-check `:77-80`, with the 19-pair write-class census count (receipt `:27`) and the sentinel's 23 as different predicates (section 1). The spot-check asks for an appended correction to M71-4 and the SCORECARD harm note (`:142-143`). Owner: L1 (filing). Section 2 M72-3 carries the correction in this lesson.

Other round-71 spot-check defects that round 72 does not fix (spot-check section 5, `:140-153`):

- **K71-B** (`:144-145`) invert the table to global-deny-minus-allowlist. Round 72 keys on realpath (M72-2) but keeps the per-script table for `--json`, `--root`, `--url`. Open.
- **K71-C** (`:146-147`) a positive row whose direct command exits nonzero must fail, not pass as "stale" (M72-4). Open; `c1-probe-run-r71.py` is not changed by round 72.
- **K71-D** (`:148`, also `:29-31`) append an erratum naming the real base `39cde8a086cf…`. Open.
- **K71-E** (`:149-150`) reconcile the wave role split with `templates/round-prompt.md`. Round 72's `w1-spec.json` has 11 items with roles executor×3 (`:14, :19, :24`), mutation-tester (`:29`), reviewer×2 (`:34, :39`), critic (`:44`), scout (`:49`), scribe×2 (`:54, :59`), connector (`:64`), and no planner item (the Goal names the L1 as the planner). Open.
- **K71-F** (`:151`) correct the counter docstring R4/R8 rows to match the code. Open.
- **K71-G** (`:152-153`) reap the previous attempt's process group before relaunch: driver/operator work. Open.

Defects found by this seat in the round-72 bytes (not in the spot-check):

- **R-5 · candidate comment misstates the split.** `figure-audit.py:144-146` says the round-71 table "re-admitted 18 `--work` heads and one `--scratch` head". The census receipt has 15 `--work` (`c1-census-donothing-r72.txt:10, :13-26`) and 4 `--scratch` (`:8, :9, :11, :12`); both sum to 19. A comment-only edit changes the candidate's sha256 (`b146c81a…`) and therefore the frozen pin. Owner: L1 decides whether to correct it before commit.
- **R-6 · fixture-name allowance is still keyed on the name.** `figure-audit.py:222-224` (`PY_SELFTEST_FIXTURE_HEADS`) and `:507` admit a head by basename; `:509` then gives it `PY_DENIED_ANY` plus `PY_DENIED_BY_SCRIPT.get(name, ())`, which is empty for `ok.py` and the other seven names. The realpath fix covers symlinks, not a regular file named `ok.py` inside `corpus/instruments/`. [INFERENCE from committed bytes; not measured by this seat.] Owner: K72ExecProbe and K72AttackCensus to measure; next round to scope the allowance to `selftest()`, as the sentinel's residual 4 (`:157-162`) suggests.

## 5. Residuals

Each line: residual · one-line reason it stays open.

1. `freeze-check.py` `bash -c` exec (R-2) · not in the round-72 claims (`claims.json:64`); needs its own head-refusal change and a row in the census.
2. `sort -T` temp-directory writes (R-3) · outside C1's write-class set; no census row exists for `sort`.
3. `--json` and `--root` not in `WRITE_CLASS` (R-1) · the frozen counter excludes them; changing the frozen set is a next-round decision.
4. Fixture-name allowance by basename (R-6) · the realpath fix covers symlinks only; a regular file named `ok.py` is admitted with `PY_DENIED_ANY` only (inference, unmeasured).
5. Per-script default-allow for `--json`, `--root`, `--url` (K71-B) · inversion to global-deny-minus-allowlist is a larger repair than this round's claims.
6. Positive row exit-nonzero reads as "stale" (K71-C, M72-4) · `c1-probe-run-r71.py` is frozen and not changed by round 72.
7. Probe-doc drift in `c1-probe-run-r71.py` (K71-F) · docstring-only; no measured effect on verdicts.
8. Missing erratum for the base prefix `39cde8a…` (K71-D) · an L1 filing action, not a gate change.
9. Wave role split (K71-E) · needs the template decision; `w1-spec.json` has no planner item by design of this wave.
10. Driver relaunch with a live prior process (K71-G) · operator/driver work; R118 is the lane-side half.
11. Harm-count predicates (R-4, M72-3) · three predicates (23, 43/26, 19) remain in the record until the L1 files the spot-check correction.
12. Argparse abbreviations and dash-spelling (sentinel residual 7, `:177-181`) · C1 claims the enumerated spellings only; K72AttackCensus item 4 is the only measurement pending.
13. Stdin inheritance, absolute-path reads (sentinel residual 6, `:170-176`) · read confinement is not in C1's claims.
14. `-- --selftest` admission (sentinel residual 2, `:143-150`) · outside the frozen set (`claims.json:63`, V71-9/V71-10).
15. Unpinned PATH and argv[0] resolution (sentinel residual 9, `:185-188`) · a host boundary statement, unmeasured.
16. Green values for M72-1 and M72-2 · pending the candidate census run and the K72Mutate matrix; this draft does not claim them.
17. `captured-by` criterion for M72-1 and M72-2 · no `corpus/QUALITY.md` row is appended by this draft; the frozen C1 census row is the captured rule. The L1 decides whether a QUALITY row is also needed.

## 6. Which claims each section supports

- Section 0 (run log) supports the byte pins for C1 and C2 (candidate `b146c81a…`, census `255fd407…`, base `182f4ef7…`, S107 `0b944ea1…`, 1176 lines). It supports no outcome claim.
- Section 1 (mining notes) supports C1 by naming the mechanism that the C1 repair addresses (default-allow and basename keying). It supports no measured claim by itself.
- Section 2 (`## Mistakes`): M72-1 supports C1 (write-class census and global `--work`/`--scratch` denial). M72-2 supports C1 (ALIAS-PROBE, realpath keying). M72-3 and M72-4 support no round-72 claim; they are routed mistakes.
- Section 3 (`## Gate`) supports C2 (S107 access date, URL, located quote).
- Section 4 (`## Routed defects`) supports no frozen claim. It records the frozen non-claims (`claims.json:63-64`) and the round-71 defects not repaired.
- Section 5 (`## Residuals`) supports the scope limits of C1 and C2 and the non-claims. It does not support a pass on any claim.
