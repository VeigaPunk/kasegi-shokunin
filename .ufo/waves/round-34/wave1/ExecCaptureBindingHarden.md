# ExecCaptureBindingHarden — round 34, C1 capture-binding hardening

Seat: `ExecCaptureBindingHarden` (leaf executor, wave 1). Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `014ee2d7aa8c3c095ff57ae51097606a9906228c`,
claims-freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13`. No commit, no jj/git mutation,
no write outside the lane. Scratch `/fast/scratch/hyaku/kasegi-r34/ExecCaptureBindingHarden`
(created, used, removed — proof at the end).

Assignment executed: the eight-item hardening of `corpus/instruments/capture-binding-check.py`
(strict-UTC, per-file orphan binding, nested snapshot dirs, dup records, double-`https://` row,
rejected-row anchor, the R5 case rename, and the summary-only selftest rejection), all in one
landing, plus the instrument doc it invalidates.

## Report

### 1. Files written

| path | change | before | after |
|---|---|---|---|
| `corpus/instruments/capture-binding-check.py` | whole-file rewrite of `check()`/`load_registry()`/`snapshot_dirs()`/`provenance_ok()`/`bind_record()`, new rules, new selftest runner + report verifier, 12 new cases | `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9`, 492 lines | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa`, 892 lines |
| `corpus/instruments/README.md` | appended `## Round-34 hardening …` section (appended at EOF; nothing above moved) | `15dd603ec3cb47fa9dc181f2010790a858c437dedc2184ffcd1fe0eae40139ba`, 656 lines | `161654c1b83b160a4aa290f524d6ec6897e09c51faf7e491a60c06791b65d404`, 761 lines |
| `.ufo/waves/round-34/wave1/ExecCaptureBindingHarden.md` | this receipt | — | — |

Base-bytes proof that the pre-edit digest is the lane base, not a sibling's edit:
`git show 014ee2d7…:corpus/instruments/capture-binding-check.py` → sha256
`b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9`, 492 lines, `show_exit=0`.

### 2. Selftest — 23 cases, 0 failures, exit 0, deterministic

```
$ python3 corpus/instruments/capture-binding-check.py --selftest ; echo "selftest_exit=$?"
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
selftest_exit=0
```

`N=23 ≥ 19` (frozen C1 predicate satisfied; was 11). Line counts: 24 stdout lines = 23
`selftest case=` lines + 1 summary (`grep -c '^selftest case='` → `23`). Determinism: two
consecutive runs byte-identical,
`sha256(stdout) = ca3759d1c4a047ec1a27f4d6bc8b64df4d6e21a29b74ef9904ccbe91be3a3a51`,
`selftest_exit_1=0 selftest_exit_2=0`.

The 11 pre-existing cases survive under their old names except `url-matching-two-rows`
(item 7): that name now builds a two-record shared-URL fixture and asserts
`multi_row_url=2` at exit 0, and the duplicate-id fixture it used to carry is
`duplicate-id-rows`, so the name matches the content (R5 closed at the case level).

### 3. Live audit — real corpus, unchanged per-record binding

```
$ python3 corpus/instruments/capture-binding-check.py ; echo "binding_exit=$?"
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=0 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
FAIL rule=no-row record=S051 dir=round-34
records=41 bound=40 unbound=1
binding_exit=1
```

13 stdout lines, `sha256 = 56f08a92037cc2520dc89f23f4acd0fdffc4a9331796e7cfbff7c534263a6038`,
identical on two consecutive runs (`audit_identical`).

Every rule the hardening adds is measured **clean** on the live tree; the one FAIL line is
not a capture defect:

- `orphans=1 orphan=S040-live.txt` and **no** `rule=orphan-capture` line: round-26 declares
  the file under the `orphans` key agreed with `ExecS040Orphan` (manifest sha256
  `33ac33c3caa6d43f3772b8cf8532b37cdb50f48db8ba667b5dd90645e8eacefa`). Declared, named,
  unbound, exit-neutral, `records=1` unchanged — R6's listing form.
- `grep -c 'detail=local-offset'` → 0; round-32 measures `fetched=2` with strict stamps
  (`2026-10-26T04:16:06Z`, `2026-10-26T04:16:16Z`) — R8's shape.
- `grep -c 'rule=double-https-row'` → 0 (all 50 registry rows carry exactly one `https://`
  token), `grep -c 'rule=rejected-row-anchor'` → 0, `grep -c 'rule=dup-record'` → 0,
  `missing_manifest=0` over ten snapshot dirs (the recursive walk finds no nested dir today).
- `FAIL rule=no-row record=S051 dir=round-34` is a **C2 sibling in flight**: round-34 landed
  its `sources` record before `corpus/SOURCES.md` gained `| S051 |`
  (`grep -cE '^\|…S051…\|' corpus/SOURCES.md` → `0`, registry rows → `50`). When that row
  lands, the same bytes print `records=41 bound=41 unbound=0`, `binding_exit=0`.

**Finding for the L1 (claim text, not the counter):** C1's frozen counting command says
`python3 corpus/instruments/capture-binding-check.py -> records=40 bound=40 unbound=0 exit=0
(unchanged C1 instrument baseline)`. That literal is no longer reachable — round-34's S051
capture record makes `records=41` — and it was already stale in intent once any round adds a
capture. The predicate that holds is `bound = records` (0 unbound) at exit 0; the README
section records that reading. I did not edit the frozen claims.

### 4. Discrimination — the round-33 bytes pass, the landed bytes reject

Nine fixture shapes built once with the instrument's own builders, then each `--root` run
through both byte sets (round-33 `b4182665…` vs landed `3d9e5e0…`):

```
case                         | old exit  old summary              | new exit  new summary
fetched-utc-pending          | 0         records=1 bound=1 unbound=0 | 1         records=1 bound=0 unbound=1
   new FAIL lines: ['FAIL rule=fetched-utc record=S001 dir=round-32 detail=pending']
fetched-utc-local-offset     | 0         records=1 bound=1 unbound=0 | 1         records=1 bound=0 unbound=1
   new FAIL lines: ['FAIL rule=fetched-utc record=S001 dir=round-32 detail=local-offset']
per-file-orphan-undeclared   | 0         records=1 bound=1 unbound=0 | 1         records=1 bound=1 unbound=0
   new FAIL lines: ['FAIL rule=orphan-capture file=S009.txt dir=round-30']
per-file-orphan-declared     | 0         records=1 bound=1 unbound=0 | 0         records=1 bound=1 unbound=0
nested-snapshot-dir          | 0         records=1 bound=1 unbound=0 | 0         records=2 bound=2 unbound=0
nested-missing-manifest      | 0         records=1 bound=1 unbound=0 | 1         records=1 bound=1 unbound=0
   new FAIL lines: ['FAIL rule=missing-manifest dir=round-31/inner']
dup-record-in-manifest       | 0         records=3 bound=3 unbound=0 | 1         records=3 bound=3 unbound=0
   new FAIL lines: ['FAIL rule=dup-record field=id value=S001 count=2 dir=round-30', 'FAIL rule=dup-record field=path value=S001.txt count=2 dir=round-30']
double-https-row             | 0         records=1 bound=1 unbound=0 | 1         records=1 bound=0 unbound=1
   new FAIL lines: ['FAIL rule=double-https-row row=S001 n=2', 'FAIL rule=url-ambiguous record=S001 row=S001 tokens=2 dir=round-30']
rejected-row-anchor          | 0         records=1 bound=1 unbound=0 | 1         records=1 bound=0 unbound=1
   new FAIL lines: ['FAIL rule=rejected-row-anchor record=S026 row=S026 dir=round-30']
clean-control                | 0         records=2 bound=2 unbound=0 | 0         records=2 bound=2 unbound=0
```

`nested-snapshot-dir` is the silent-undercount case: the old bytes exit 0 while reading
`records=1` of the 2 recorded captures, i.e. the nested dir was invisible, not failed.
`clean-control` and `per-file-orphan-declared` show the hardening is not an always-fail limb.

Summary-only report, fed to the landed report checker vs. the round-33 bytes:

```
new judge_selftest_report(summary-only) -> ['summary-only-report', 'case-line-count case=a count=0', 'case-line-count case=b count=0', 'summary-cases=23 want=2']
new judge_selftest_report(complete)     -> []
old bytes carry a case-line requirement: False
```

So the round-33 F-5 shape (print the summary, run no case) is rejected by the landed bytes
via a required `verdict=` line per case, and the checker is proven two-sided by the
`complete-selftest-report-accepted` control.

### 5. Exit-2 paths (measured, not assumed)

```
$ … capture-binding-check.py --root p1        # empty root
UNAVAILABLE reason=no-snapshot-tree …/p1
exit=2

$ … capture-binding-check.py --root p2        # snapshot tree, no SOURCES.md
UNAVAILABLE reason=read-error [Errno 2] No such file or directory: '…/p2/corpus/SOURCES.md'
exit=2

$ … capture-binding-check.py --root p3        # malformed manifest JSON
UNAVAILABLE reason=manifest-JSONDecodeError …/p3/corpus/source-snapshots/round-30/manifest.json
exit=2

$ … capture-binding-check.py --root p4        # orphans: ["S009.txt"]  (bare string)
UNAVAILABLE reason=manifest-shape …/p4/corpus/source-snapshots/round-30/manifest.json orphans
new_exit=2
$ … old/capture-binding-check.py --root p4    # round-33 bytes: the key was invisible
MANIFEST round-30 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=1 … multi_row_url=0
records=1 bound=1 unbound=0
old_exit=0
```

The malformed-declaration path is new this round and is the reason the `orphans` schema was
fixed with `ExecS040Orphan` before either side wrote bytes. Their entry carries
`sha256`/`row`/`row_url`/`captured_url`/`fetched_utc` as extra keys; the validator reads only
`path` and `reason`, and the round-26 `purpose` text states those extra fields are
informational to this checker, not asserted by it — I am not claiming otherwise.

### 6. Rule implementation, quoted by symbol

- `classify_fetched` — one strict-UTC regex (`(?:Z|\+00:00)\Z`) plus
  `datetime.datetime(*groups)` calendar validation, so `2026-13-01T00:00:00Z` is
  `malformed`, `2026-10-25T23:14:00-03:00` is `local-offset`, `pending` is `pending`.
- `provenance_ok` — returns `(ok, has_fetched, has_archival, detail)`; `has_fetched` counts
  only strict stamps, so `MANIFEST … fetched=` no longer counts a placeholder; a
  present-but-invalid value fails in legacy rounds too.
- `bind_record` — order `no-row` → `dup-id` → `rejected-row-anchor` → `url-mismatch
  detail=absent` → `url-ambiguous` (row with >1 token) → `url-mismatch`; the status comes
  from column 8 of the row (`STATUS_COLUMN = 7` after the leading-empty split).
- `snapshot_dirs` — `os.walk` with `dirnames.sort()`, relpath naming (`round-30/inner`),
  parents before children; a dir is a snapshot dir iff it holds `manifest.json` or one of
  its own files.
- `orphan_paths` / `capture_files` / `duplicate_records` — declaration validation (None on
  malformed → exit 2), direct-file listing excluding `manifest.json`, and the `id`/`path`
  duplicate scan.
- `judge_selftest_report` — `summary-only-report`, per-case line count, `verdict=pass`,
  `exit == want`, summary `cases`/`failures` cross-check; run on forged inputs by the two
  `REPORT_CASES`.

### 7. Docs follow the change

`corpus/instruments/README.md` gains an appended round-34 section: the new rule table with
every failure name, the selftest report contract and the 23 case names, the old-vs-new
discrimination matrix above, the live-tree block and the in-flight S051 explanation, and an
explicit supersession note — the round-33 section's targets (`b4182665…`, `selftest cases=11`,
the AUDIT line drawn without `orphans=`/`orphan=`, the lenient two-token branch, "a
`rejected` … row's URL binds a record exactly like a `mined` row's") now describe the
round-33 bytes, not this file. Appended at EOF per the lane convention; no line above moved.

Not mine to edit, flagged instead: `SCORECARD.md`'s capability row still says "run an
11-case `--selftest`" (`ScribeScorecard`), and the frozen C1 counting command's literal
`records=40` (§3).

### 8. Risks and limits carried forward (measured, not hidden)

- **Rule A binds by file name, not content.** A capture copied from the wrong document but
  named by a record passes; only `source-recheck.py` sha/quote pins catch that. Recorded in
  the docstring's known limits.
- **Rule A is one-directional by assignment.** A record naming a file that is absent is not
  a rule here (the round-34 item scopes this instrument to capture-file coverage;
  `source-recheck.py` fails closed on a missing capture). Named in the docstring so a future
  reviewer does not read `orphans=0` as "every record's capture exists".
- **A declared orphan is exit-neutral by design.** The claim's own closure wording ("a
  manifest record or orphan listing") requires it; the listing is visible (`orphan=<file>`,
  `orphans=N`) but a reader who greps only for exit 0 learns nothing about it. The AUDIT
  token is the reading.
- **The `orphans` declaration is trusted, not hashed.** Extra fields are passthrough; a
  declaration could name a file whose bytes then change. The file is still covered by the
  dir-level manifest presence and by `source-recheck.py` where a record exists.
- **Live gate is red until a sibling lands.** `binding_exit=1` on `rule=no-row record=S051`
  is the C2 registry append, not this instrument; the C1 arm's exit-0 state is
  `records=41 bound=41 unbound=0` after that row. Do not "fix" it by dropping the record.

### 9. Scratch cleanup

Work tree `/fast/scratch/hyaku/kasegi-r34/ExecCaptureBindingHarden` (fixtures, the round-33
byte copy at `old/capture-binding-check.py`, the `discriminate.py` harness, the four exit-2
probe roots, captured stdout) was removed after this receipt was written; removal verified
in the same shell (`test -e … || echo removed`) — see the run block in §10.

### 10. Tooling

No install or upgrade was needed or performed this seat (python3 stdlib only; `git show` read
only). No pacman, no `uv tool`, no network fetch.

## Commands run (verbatim, in order, with exit codes)

```
git show 014ee2d7aa8c3c095ff57ae51097606a9906228c:corpus/instruments/capture-binding-check.py   -> show_exit=0 (492 lines, b4182665…)
python3 corpus/instruments/capture-binding-check.py --selftest                                   -> selftest cases=23 failures=0, selftest_exit=0 (run 1)
python3 corpus/instruments/capture-binding-check.py --selftest                                   -> selftest cases=23 failures=0, selftest_exit=0 (run 2, byte-identical)
python3 corpus/instruments/capture-binding-check.py                                              -> records=41 bound=40 unbound=1, binding_exit=1 (S051 row unappended)
python3 corpus/instruments/capture-binding-check.py                                              -> identical stdout, sha256 56f08a92…
python3 /fast/scratch/hyaku/kasegi-r34/ExecCaptureBindingHarden/discriminate.py                  -> discriminate_exit=0 (matrix in §4)
python3 corpus/instruments/capture-binding-check.py --root p1|p2|p3|p4                           -> exit 2 each (§5)
python3 /fast/scratch/hyaku/kasegi-r34/ExecCaptureBindingHarden/old/capture-binding-check.py --root p4 -> old_exit=0
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md                             -> 50
grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md                                   -> 0
sha256sum corpus/instruments/capture-binding-check.py                                            -> 3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa (892 lines)
sha256sum corpus/instruments/README.md                                                           -> 161654c1b83b160a4aa290f524d6ec6897e09c51faf7e491a60c06791b65d404 (761 lines)
sha256sum corpus/source-snapshots/round-26/manifest.json                                         -> 33ac33c3caa6d43f3772b8cf8532b37cdb50f48db8ba667b5dd90645e8eacefa
sha256sum corpus/source-snapshots/round-32/manifest.json                                         -> 72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6
```

## Verdict for the L1

C1's capture-binding arm is landed and measured: `selftest cases=23 failures=0` exit 0
(N≥19, every required case name present: `per-file-orphan-detected`, `per-file-orphan-listed`,
`nested-snapshot-dir`, `fetched-utc-pending-rejected`, `fetched-utc-local-offset-rejected`,
`dup-record-in-manifest`, `double-https-row`, `rejected-row-anchor`,
`summary-only-selftest-rejected`), with the round-33 bytes demonstrably passing seven of the
nine mutant shapes the landed bytes reject. `records=40 bound=40 unbound=0 exit=0` cannot be
the C1 target any more — the tree measures `records=41` and the honest predicate is
`bound=records` at exit 0, gated on the C2 S051 registry row that is still unappended
(`rule=no-row record=S051`). I did not edit the frozen claims; the correction is the L1's.

## Addendum (same seat, later in the wave) — the S051 row landed, live gate is green

The C2 registry append landed after §3 was written. Nothing in my instrument changed; the
same bytes `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` now measure:

```
$ grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md ; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
1
51
$ python3 corpus/instruments/capture-binding-check.py ; echo "binding_exit=$?"
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=41 bound=41 unbound=0
binding_exit=0
```

So the capture-binding arm of C1 is green on the landed tree: `records=41 bound=41
unbound=0` (`bound=records`, the invariant that replaces the frozen literal 40),
`binding_exit=0`, no `FAIL` line, `orphans=1 orphan=S040-live.txt` (declared, exit-neutral),
`multi_row_url=2` (the erratum-1 informational pair), `missing_manifest=0` over ten
snapshot dirs. The §3 block stays as the timestamped in-flight measurement; this addendum
is the closed one. `corpus/instruments/README.md` carries the matching addendum and its
before/after digest moved to `161654c1…` → the digest at the time of this note (re-read
after the append, not retyped).

Because the README gained a second append, its digest after this addendum is not
`161654c1b83b160a4aa290f524d6ec6897e09c51faf7e491a60c06791b65d404` any more; measure it
with `sha256sum corpus/instruments/README.md` at integration rather than quoting §1. The
instrument digest `3d9e5e0…` is unaffected and remains the pinned mutant target for
`RevKillRule` / `ExecKillRuleCheck`.

## Peer finding recorded (MutCaptureBindingLimbs, relayed not adopted) — the report-verifier limb is thinner than §4 reads

`MutCaptureBindingLimbs` read the landed `judge_selftest_report` and flagged that
`summary-only-report` is redundant with the `case-line-count` loop for the forged
summary-only report: an empty `case_lines` already yields one `case-line-count` problem per
expected name, so a one-limb mutant deleting the `summary-only-report` append leaves the
function non-empty and `summary-only-selftest-rejected` still passes. I re-read the code and
agree — it is an explicit diagnostic (one word naming the forged shape), not a load-bearing
limb, and such a survivor is an equivalent mutant rather than a kill.

The consequence is a real gap the 23 landed cases do not close: **nothing pins the
case-line-count limb itself.** `complete-selftest-report-accepted` only proves acceptance, so
a mutant that deletes the count loop survives unless a fixture requires rejection of an
*incomplete* report. Round-35 candidate, with the shape already in the selftest:
`incomplete-selftest-report-rejected` feeding `forged_complete(expected)` minus one case
line, expected exit 1 (and a duplicated-case-line variant for the same limb).

Not landed here, deliberately: the instrument bytes `3d9e5e0d…` are pinned mid-wave by
`MutCaptureBindingLimbs`, `RevKillRule` and `ExecKillRuleCheck`, an extra case moves N from
23, and the frozen C1 predicate names N≥19 with a fixed case list that does not include it.
Recording beats a unilateral late edit that invalidates three peers' baselines for a limb
the claim does not name. The same gap is stated in the docstring's known limits? No — it is
not; that is what this section is for, and the L1 can route it.

Also relayed by that peer, for consistency: `detail=malformed` (calendar-invalid stamp) and
the legacy "present-but-invalid `fetched_utc` still fails" branch are implemented
(`classify_fetched`, `provenance_ok`) but **not** pinned by any case — the cases pin
`pending` and `local-offset` on modern rounds only. Same class of finding: live code, no
fixture. Both are candidates for round 35, not silent claims of coverage.

## Digests at close of seat

```
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py   (892 lines, unchanged since §1)
65ab717c03864f127a97bc3c0e3e596f58ac2914827c4be8d4ac5cd506a70ddc  corpus/instruments/README.md                 (781 lines; §1 recorded 161654c1… at 761 lines, before the green-gate addendum)
ee18150b146a9251be9a3a57df3cea1a2c14a4efcb52df670a8fea0c5b6e34e3  this receipt, before this section was appended
```

Scratch `/fast/scratch/hyaku/kasegi-r34/ExecCaptureBindingHarden` removed and verified
absent before this append (`scratch removed: …`).

## Peer-measured confirmation (MutCaptureBindingLimbs, their run — cited, not mine)

Their mutant run on the pinned bytes reports the limb split exactly as analysed above, and
I record it here because it is the kill-rule evidence for this instrument's report verifier:
`M09a` and `M09b` (one limb each: the `summary-only-report` append; the case-line-count
loop) **SURVIVED** — byte-identical stdout, `rc=0`, `cases=23 failures=0` — while the
two-limb probe `M09ab` (both disabled) was **KILLED** with the forged report accepted
(`selftest case=summary-only-selftest-rejected exit=0 want=1 verdict=fail`,
`problems=[]`). I did not run these; the numbers are theirs, from
`/fast/scratch/hyaku/kasegi-r34/MutCaptureBindingLimbs/`, and their receipt is the source.
The reading is unambiguous: the report verifier is one effectively-single-limb check for
the summary-only shape, so a one-limb mutant there is equivalent rather than killed, and the
missing incomplete-report fixture (§Peer finding) is the same weakness seen from the other
side.

Final instrument digest unchanged: `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa`.
`corpus/instruments/README.md` moved after my appends because sibling seats append their own
round-34 sections to the same file (measured `65ab717c…` at 781 lines right after mine, then
`1f32dd08…`); my two sections are intact under `## Round-34 hardening …` and its
`### Addendum …`, and the instrument digest is what the pins rest on.

## Critic finding verified (CritC1Kill, relayed) — two vacuity routes, neither landed this wave

`CritC1Kill` reported two vacuity routes on the pinned bytes. I reproduced both from my own
fixtures (fresh scratch tree, `--root` per fixture) rather than taking them on report; both
are real and both are recorded here as routed defects, not as fixed code.

### (a) Degenerate orphans: per-file coverage with zero records — CONFIRMED, vacuous pass

Fixture: `round-30` with three capture files and `"sources": []`, all three declared under
`orphans` with a reason. Measured on `3d9e5e0…`:

```
MANIFEST round-30 records=0 url_bound=0 fetched=0 archival=0
AUDIT records=0 with_url=0 with_fetched_utc=0 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=3 orphan=A1.txt orphan=A2.txt orphan=A3.txt
records=0 bound=0 unbound=0
exit=0
```

A directory holding captures and zero documented records exits 0: rule A's per-file check is
satisfied by declarations alone, and rule C has no record to examine, so `bound=records`
holds vacuously. This is exactly the class the instrument exists to refuse (an unauditable
capture directory), and it is my landing's hole, not the critic's.

Proposed fix (NOT landed): rule A3 — `FAIL rule=no-records dir=<d> captures=<n>` when a
manifest directory holds at least one capture and `len(records) == 0`, plus selftest case
`all-captures-orphaned-rejected` (this exact fixture, expected exit 1). Two lines in
`check()` and one case; N moves 23 → 24. Not landed because three peers (`RevKillRule`,
`MutCaptureBindingLimbs`, `ExecKillRuleCheck`) pinned `3d9e5e0d…` mid-wave as their mutant
target, an edit moves N and their baseline stdout digest, and the frozen C1 case list does
not name this case. It needs an L1 order, then one edit and a re-notify to all three.

### (b) `fetched_utc` is a shape check, not a provenance tie — CONFIRMED as a limit, not a bug

Measured: `2026-10-25T04:16:06Z` (wrong day), `2026-01-01T00:00:00Z` (far past) → `bound=1`,
exit 0; `2026-02-30T00:00:00Z` → `detail=malformed` exit 1; `2026-10-25Tgarbage-not-a-timeZ`
→ `detail=malformed` exit 1. So rule C's boundary is exactly what the docstring says it is:
ISO-8601 syntax plus real calendar fields, no claim that the instant is the true fetch time.
The instrument cannot close that with a clock: `now()` would break the byte-identical
determinism the lane requires of every instrument, and a round→window table would be an
invented rule that flags legitimate re-captures. The honest defences remain the manifest
`purpose` text, `source-recheck.py`'s sha/quote pins and a live re-fetch — which is what the
round-32 records actually rely on. Recorded as a known limit, and `CritC1Kill`'s stronger
formulation (reject future/out-of-round instants) is a round-35 design question, not a patch
this seat may invent.

### (c) The R8 closure check is weaker than rule C — CONFIRMED, and it is not my file

`CritC1Kill` is right that `r-defect-closure.sh`'s R8 accepts what rule C rejects:
`2026-10-25Tgarbage-not-a-timeZ` passes R8 while `capture-binding-check.py` fails it
(`detail=malformed`, exit 1, measured above). R8 belongs to `ExecRDefectClosureSuite`; I
relayed the cross-check to that seat. My instrument's own verdict on that string is the
stronger one, so the fix direction is to make R8 delegate to rule C rather than parse the
stamp a second time.

## Round-35 design note accepted from the critic (clock-free provenance tie)

`CritC1Kill` withdrew the future/out-of-round variant as a wave fix (a hidden round→window
policy would flag legitimate re-captures and a `now()` comparison would break the
byte-identical determinism every instrument in this lane owes) and proposed the clock-free
form instead, which I accept as the right round-35 shape:

- **receipt-as-data tie:** a record's `fetched_utc` must appear verbatim in a named receipt
  the manifest cites (a manifest-level `receipt` key pointing at a committed file), so the
  instant is checked against a second committed artefact rather than against the wall clock;
- **`fetched-utc-fabricated-no-receipt` case:** a stamp that no cited receipt carries is a
  failure, which pins the tie the way `fetched-utc-pending-rejected` pins the placeholder.

That keeps the instrument deterministic, adds the provenance link rule C cannot make alone,
and needs no new clock. Not landed here (post-freeze, moves N); recorded so the L1 can order
it in one edit next round instead of re-deriving the design.

Both of the critic's corrections (§3–4 of `.ufo/waves/round-34/wave1/CritC1Kill.md`) and my
reproductions above agree on the state of C1: two recoverable instrument gaps (degenerate
orphans, report-verifier limb), one stated limit (instant is a shape check), one sibling
defect (R8 weaker than rule C), and no blocker for the held-4 claim.

## R8 resolution reviewed (ExecRDefectClosureSuite's landed check) — one residual gap, measured

The suite landed a stricter local R8 (`corpus/instruments/r-defect-closure.sh` sha256
`357a7e4923bf784cd513dfaa94258d4cb6d5dfc1cbb677b36accbab86a05bc2d`, 688 lines): the frozen
`^[0-9]{4}-[0-9]{2}-[0-9]{2}T.*Z$` floor plus a real `datetime.fromisoformat` instant at
zero offset, no clock, no delegation of the exit status to the whole-corpus audit. That
closes the `2026-10-25Tgarbage-not-a-timeZ` false positive I measured, and I checked the
landed behaviour rather than the claim:

```
$ bash corpus/instruments/r-defect-closure.sh --root <fixture with fetched_utc="2026-10-26T04:16:06+00:00"> | grep -E '^R8|closed='
R8 check=round-32 manifest carries a fetched_utc that is not a strict-UTC instant open=1
closed=0/9 exit=1
$ bash corpus/instruments/r-defect-closure.sh --root <same fixture, fetched_utc="2026-10-26T04:16:06Z"> | grep -E '^R8|closed='
R8 check=round-32 manifest fetched_utc is a real strict-UTC instant (date-T time Z, zero offset), no '-' offset open=0
closed=1/9 exit=1
```

Residual gap: R8 now rejects a **`+00:00`-suffixed** stamp — `shaped` requires a literal
`Z`, and the separate `offset` guard `[+-][0-9]{2}:?[0-9]{2}` also matches `+00:00` — while
rule C accepts both by assignment item 1 ("`Z` or `+00:00`") and the frozen kill rule reads
"non-UTC `fetched_utc`". A legitimate `+00:00` capture would therefore leave R8 open at
`closed=8/9` on a manifest that rule C passes at exit 0: the two instruments now disagree on
one value class, and the suite's "the strike only removes false positives" holds for the
garbage string but not for this one. One-line fix, either side: allow the `+00:00`
alternative in `shaped` and exempt it in the `offset` guard (or normalise `+00:00` → `Z`
before matching). Not my file, reported not patched; my instrument keeps the assigned
contract.

The suite's own note that `closed=9/9` is not evidence against the degenerate-orphan route
matches mine: that route is routed to the L1, not covered by R1–R9.

## R8 residual closed — verified, so the previous section reads "patched", not "routed-not-patched"

`ExecRDefectClosureSuite` normalised the suffix and pinned the boundary in its own selftest.
I verified the landed bytes rather than the announcement
(`corpus/instruments/r-defect-closure.sh` sha256
`2a635bf575c38e04b028dd26ecbeff73c3b909add892ab727c2ab6b1c821dcfc`, 742 lines):

```
2026-10-26T04:16:06+00:00        -> R8 open=0 (accepted)
2026-10-26T04:16:16.500Z         -> R8 open=0 (accepted)
2026-10-26T04:16:16-03:00        -> R8 open=1 (rejected)
2026-10-25Tgarbage-not-a-timeZ   -> R8 open=1 (rejected)
```

So R8's accept set is now rule C's (`Z`, `+00:00`, fractional seconds) and it still rejects
non-zero offsets and non-instants — the divergence recorded above is gone, in the direction
that keeps both limbs honest. Live suite: `closed=9/9 exit=0`; `--selftest` prints
`selftest case=R8 live=pass fixture=rejected control=pass verdict=pass` and
`selftest cases=9 failures=0`, exit 0. The positive-control fixture is the `+00:00` value I
measured, so the gap cannot silently return without a failing case.

The degenerate-orphan route remains the one open instrument gap in this area: it is not
covered by R1–R9 (`closed=9/9` is not evidence about it) and not landed in rule A, as stated
above and in the suite's own §11 item 7.
