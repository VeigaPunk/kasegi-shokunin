# MutCaptureBindingLimbs — round-34 wave1 seat receipt

Seat: MutCaptureBindingLimbs (mutation-tester, leaf of the L2 wave, hyaku run 8).
Assignment: mutation-test the landed `corpus/instruments/capture-binding-check.py` — for each of the
10 NEW selftest cases build a one-limb mutant that removes/disables that case's guard, run `--selftest`
against each mutant copy, and show the selftest run changes; controls (no-op, non-compiling,
semantically equivalent) must NOT be treated as kills. Every mutant an exact-once find/replace over the
instrument bytes in a scratch copy.

## Report

### 1. Scope and method

- Target bytes: `corpus/instruments/capture-binding-check.py`, landed digest
  `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` (892 lines), measured with
  `sha256sum` on the lane file and on my scratch copy — identical, and identical to the figure pinned
  mid-wave by the author seat ExecCaptureBindingHarden (peer message: "Bytes are final for this wave").
  The lane instrument was never opened for write by this seat; every mutant is a scratch copy under
  `/fast/scratch/hyaku/kasegi-r34/MutCaptureBindingLimbs/`.
- Method: for each assigned case, one exact-once find/replace over the pristine bytes disabling that
  case's guard limb, then `python3 <mutant>.py --selftest --scratch <dir>` on the mutant copy.
- Classification rule (declared before runs):
  - `KILLED` — the target case's verdict flips `pass`→`fail` (or its line vanishes while `failures>0`);
  - `SURVIVED` — mutant stdout byte-identical to baseline and same exit code;
  - `INCONCLUSIVE` — crash without a selftest report (e.g. syntax error);
  - controls are never kills: a no-op/equivalent control must reproduce baseline exactly, a
    non-compiling control must crash without a report.
- Every find string was asserted to occur **exactly once** in the pristine bytes before replacement
  (the driver raises `FIND-COUNT` on any other count; no assertion fired across all 16 probes).
- Runs: three driver executions. Run 1 = pilot (11 probes). Run 2 added the surgical `M03b` but
  invalidated its supplementary probe through an index bug in my driver (`M09AB` referenced
  `MUTANTS[8]/[9]`, which shifted after the `M03b` insert, so that probe applied the M08+M09a limbs
  instead of M09a+M09b); run 2 is discarded for the supplementary probe only — its other probes matched
  run 1 exactly. Run 3 (the record) fixed the lookup by id. Baseline stdout sha256 was identical in all
  three runs and equals the author seat's independent figure `ca3759d1…` (§2).

### 2. Baseline (pristine bytes)

```
$ /usr/bin/python3 pristine/capture-binding-check.py --selftest --scratch .../st/base
rc=0
selftest cases=23 failures=0
baseline_stdout_sha256=ca3759d1c4a047ec1a27f4d6bc8b64df4d6e21a29b74ef9904ccbe91be3a3a51
```

Full baseline stdout (24 lines, all `verdict=pass`):

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

The stdout digest matches ExecCaptureBindingHarden's independent measurement
(`ca3759d1c4a047ec1a27f4d6bc8b64df4d6e21a29b74ef9904ccbe91be3a3a51`) — the selftest is
deterministic across seats and across my three runs. Baseline passing, so no probe is
inconclusive-by-baseline.

### 3. Controls (must NOT be kills) — all three behaved as required

| id | patch (exact-once find/replace) | rc | selftest | verdict |
|---|---|---|---|---|
| C-nop | line 167 comment extended: `…exemption is closed` → `…exemption is closed [control C-nop: comment-only edit]` | 0 | `selftest cases=23 failures=0` | **not a kill** — stdout byte-identical to baseline |
| C-syntax | line 158 `SCHEMA_VERSION = 1` → `SCHEMA_VERSION = = 1  # control C-syntax: deliberate syntax error` | 1 | no report | **not a kill** — `SyntaxError`, crash without a report (inconclusive by construction) |
| C-equiv | line 461 `return 0 if not failures else 1` → `return 1 if failures else 0  # control C-equiv: equivalent rewrite` | 0 | `selftest cases=23 failures=0` | **not a kill** — stdout byte-identical to baseline |

C-syntax stderr head: `File ".../mutants/C-syntax.py", line 158` / `SCHEMA_VERSION = = 1 …` / `^`.
C-equiv is a true semantic-equivalence control (`failures` is a list; `0 if not failures else 1` ≡
`1 if failures else 0`), and it reproduces baseline byte-for-byte — the detector does not reward
non-behavioral edits. Control digests: C-nop `9bd1a43ab662871b95ebe9f23d728a4a129a097590c1bb1db64d0346064345bc`,
C-syntax `7b85f1ae2d2aad68100253a8625e84507b3be8be008e79f0373ee8e5d3fa1a1b`,
C-equiv `5684da03ea92af300bded79e087894ae56f11cf582d4f40135604313c5cc3cae`.

### 4. Mutants — one-limb, exact-once find/replace, `--selftest` per mutant copy

Summary (line numbers are pristine-file lines, confirmed by each diff's `@@` header):

| id | target case | guard limb disabled (file:line) | rc | selftest | verdict | collateral kills |
|---|---|---|---|---|---|---|
| M01 | per-file-orphan-detected | orphan-capture failure emission (`:442`) | 1 | `cases=23 failures=1` | **KILLED** | — |
| M02 | per-file-orphan-listed | declared-orphan acceptance (`:441`) | 1 | `cases=23 failures=1` | **KILLED** | — |
| M03 | nested-snapshot-dir | os.walk descent (`:236`) — blunt | 1 | `cases=23 failures=21` | **KILLED** | all 20 other fixture cases |
| M03b | nested-snapshot-dir | composed nested naming (`:237`) — surgical | 1 | `cases=23 failures=2` | **KILLED** | nested-snapshot-missing-manifest |
| M04 | fetched-utc-pending-rejected | pending classifier (`:254`) | 1 | `cases=23 failures=1` | **KILLED** | — |
| M05 | fetched-utc-local-offset-rejected | offset classifier (`:263`) | 1 | `cases=23 failures=1` | **KILLED** | — |
| M06 | dup-record-in-manifest | duplicate_records scan (`:430`) | 1 | `cases=23 failures=1` | **KILLED** | — |
| M07 | double-https-row | row-level double-https scan (`:365`) | 1 | `cases=23 failures=1` | **KILLED** | — |
| M08 | rejected-row-anchor | rejected-row guard (`:294`) | 1 | `cases=23 failures=1` | **KILLED** | — |
| M09a | summary-only-selftest-rejected | `summary-only-report` limb (`:767`) | 0 | `cases=23 failures=0` | **SURVIVED** | — |
| M09b | summary-only-selftest-rejected | case-line-count limb (`:778`) | 0 | `cases=23 failures=0` | **SURVIVED** | — |
| M10 | shared-url-between-two-records | `multi_row_url` counting (`:402`) | 1 | `cases=23 failures=2` | **KILLED** | shared-url-not-a-failure |
| M09ab | summary-only-selftest-rejected | **supplementary two-limb** (M09a+M09b together) | 1 | `cases=23 failures=1` | **KILLED** | — |

Per-mutant evidence (diff, then the changed run; full logs were in scratch, deleted after extraction —
the quoted lines below are the complete changed portion of each report):

**M01** — sha256 `c6640fb99cc86b374b872d7a9e01b42d42c8cdc6d23dcbe6b7042b0af92aa0c7`
```diff
@@ -442 +442 @@
-                failures.append("FAIL rule=orphan-capture file=%s dir=%s" % (capture, name))
+                pass  # MUTANT M01 per-file-orphan-detected: orphan-capture guard disabled
```
`selftest case=per-file-orphan-detected exit=0 want=1 verdict=fail` — problems:
`exit=0 want=1`; `missing='FAIL rule=orphan-capture file=S009.txt dir=round-30'`. The guard's fixture
now **passes** the checker:
```
MANIFEST round-30 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=1 with_url=1 with_fetched_utc=1 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=1 orphan=S009.txt
records=1 bound=1 unbound=0
```
The undeclared capture is still *listed* (`orphans=1 orphan=S009.txt`) but no longer *fails* — the
listing-only shape the case exists to forbid.

**M02** — sha256 `316773bd4c876681b5be664c4083b2963f7be905c244fd54e1ac00e303300252`
```diff
@@ -441 +441 @@
-            if capture not in declared:
+            if True:  # MUTANT M02 per-file-orphan-listed: declared-orphan acceptance disabled
```
`selftest case=per-file-orphan-listed exit=1 want=0 verdict=fail` — problems: `exit=1 want=0`;
`unexpected-FAIL-line`. Fixture stdout now carries `FAIL rule=orphan-capture file=S009.txt
dir=round-30` for a *declared* orphan — the over-strict direction, exactly the limb the README's
round-34 section calls "a real limb".

**M03** (blunt) — sha256 `b0eded8e02085c198307fc6c6f557b197d878fad6653f46884843e6c04bb096a`
```diff
@@ -236 +236 @@
-        dirnames.sort()
+        dirnames.sort(); dirnames.clear()  # MUTANT M03 nested-snapshot-dir: os.walk descent disabled
```
`selftest case=nested-snapshot-dir exit=0 want=0 verdict=fail` — problems: all four expected lines
missing (`MANIFEST round-30 …`, `MANIFEST round-30/inner …`, `snapshot_dirs=2 manifest_dirs=2
missing_manifest=0`, `records=2 bound=2 unbound=0`); fixture stdout collapses to
`AUDIT records=0 … snapshot_dirs=0 manifest_dirs=0 …` / `records=0 bound=0 unbound=0`.
Collateral: **all 20 other fixture cases fail** (`failures=21`) — the walk limb is shared by every
fixture case, so this mutant proves the limb load-bearing but attributes nothing narrowly. The two
report-verifier cases still pass (they do not run fixtures).

**M03b** (surgical, added so the nested case has an attributable kill) — sha256
`b57e843876778d6cf61d31adc59d19ed2314a80e38efb115bbfa78ea315e1f8b`
```diff
@@ -237 +237 @@
-        relname = os.path.relpath(dirpath, base)
+        relname = os.path.basename(dirpath)  # MUTANT M03b nested-snapshot-dir: composed nested naming disabled
```
`selftest case=nested-snapshot-dir exit=0 want=0 verdict=fail` — problem:
`missing='MANIFEST round-30/inner records=1 url_bound=1 fetched=1 archival=0'`; fixture stdout shows
the nested dir audited under the bare name `MANIFEST inner records=1 url_bound=1 fetched=1 archival=0`
— the composed `<parent>/<child>` naming is the limb this case pins. Collateral: only
`nested-snapshot-missing-manifest` (`missing='FAIL rule=missing-manifest dir=round-31/inner'`), the
one other case that names a nested directory.

**M04** — sha256 `033988ce40e63b7fd98dfe87ab3064ee00138dd6417e0831b512c8778ae628be`
```diff
@@ -254 +254 @@
-    if text.lower() in PENDING_VALUES:
+    if False and text.lower() in PENDING_VALUES:  # MUTANT M04 fetched-utc-pending-rejected: pending classifier disabled
```
`selftest case=fetched-utc-pending-rejected exit=1 want=1 verdict=fail` — problem:
`missing='FAIL rule=fetched-utc record=S001 dir=round-32 detail=pending'`; fixture stdout shows the
record still rejected but with the wrong label: `FAIL rule=fetched-utc record=S001 dir=round-32
detail=malformed`. The case pins the `detail=pending` classification specifically.

**M05** — sha256 `03ae53eccc6b3fa6ccecdfacc179db92e924872ed08558f019abf3700de983f5`
```diff
@@ -263 +263 @@
-    if OFFSET_STAMP_RE.match(text):
+    if False and OFFSET_STAMP_RE.match(text):  # MUTANT M05 fetched-utc-local-offset-rejected: offset classifier disabled
```
`selftest case=fetched-utc-local-offset-rejected exit=1 want=1 verdict=fail` — problem:
`missing='FAIL rule=fetched-utc record=S001 dir=round-32 detail=local-offset'`; fixture stdout shows
`detail=malformed` instead. Same shape as M04: rejection survives, the discriminating label dies.

**M06** — sha256 `0e51832f22cd86be7c29bb80f1e318e339e8ffdd245bae8472672ec56f88a8c4`
```diff
@@ -430 +430 @@
-        for field, value, count in duplicate_records(records):
+        for field, value, count in ():  # MUTANT M06 dup-record-in-manifest: duplicate_records scan disabled
```
`selftest case=dup-record-in-manifest exit=0 want=1 verdict=fail` — problems: `exit=0 want=1`;
both expected lines missing (`FAIL rule=dup-record field=id value=S001 count=2 dir=round-30`,
`FAIL rule=dup-record field=path value=S001.txt count=2 dir=round-30`). Fixture stdout:
`MANIFEST round-30 records=3 url_bound=3 fetched=3 archival=0` / `records=3 bound=3 unbound=0` —
the duplicated manifest now passes with its inflated record count, and note `records=`/`bound=`
did not move even in the pristine failure (rule D fails without moving the counts, as documented).

**M07** — sha256 `429d6fcc93148dc716ef6096b693522c8a0de7786f6769fd2552aa7e7166e807`
```diff
@@ -365 +365 @@
-    for row_id, count in double_https_rows(rows_by_id):
+    for row_id, count in ():  # MUTANT M07 double-https-row: row-level double-https scan disabled
```
`selftest case=double-https-row exit=1 want=1 verdict=fail` — problem:
`missing='FAIL rule=double-https-row row=S001 n=2'`. The second guard limb
(`FAIL rule=url-ambiguous record=S001 row=S001 tokens=2 dir=round-30`) still fires from
`bind_record`, so the fixture still exits 1 — the case is killed by the missing row-level line, which
is the limb this case names. (One-limb-per-case as assigned; the `url-ambiguous` limb inside
`bind_record` is a second, unprobed guard for the same case.)

**M08** — sha256 `fc6903eb99118117254ac0c73fa3ee103dd43d4ea195f011d558a51c1a12b2fd`
```diff
@@ -294 +294 @@
-    if status == STATUS_REJECTED:
+    if False and status == STATUS_REJECTED:  # MUTANT M08 rejected-row-anchor: rejected-row guard disabled
```
`selftest case=rejected-row-anchor exit=0 want=1 verdict=fail` — problems: `exit=0 want=1`;
`missing='FAIL rule=rejected-row-anchor record=S026 row=S026 dir=round-30'`;
`missing='records=1 bound=0 unbound=1'`. Fixture stdout: `MANIFEST round-30 records=1 url_bound=1
fetched=1 archival=0` / `records=1 bound=1 unbound=0` — the capture anchored to a refused row now
binds cleanly.

**M09a** — sha256 `287f9fbb60dd1f459b67e313921397f3aa46961ddc39e0e483a6377b60b49f0e` — **SURVIVED**
```diff
@@ -767 +767 @@
-    if not case_lines:
+    if False and case_lines:  # MUTANT M09a summary-only-selftest-rejected: summary-only limb disabled
```
rc=0, `selftest cases=23 failures=0`, stdout byte-identical to baseline.

**M09b** — sha256 `95bd405c1fa9e3016d51e0959ddc414b2d2d4639b78afa5030c413bb38d973dd` — **SURVIVED**
```diff
@@ -778 +778 @@
-        if seen.get(name, 0) != 1:
+        if False and seen.get(name, 0) != 1:  # MUTANT M09b summary-only-selftest-rejected: case-line-count limb disabled
```
rc=0, `selftest cases=23 failures=0`, stdout byte-identical to baseline.

**M10** — sha256 `f97dffd9a3383332618e8545e0061c6caa0e798a02a9c3b41b603a4500c0e0be`
```diff
@@ -402 +402 @@
-                if url_row_count(cells, url) > 1:
+                if False and url_row_count(cells, url) > 1:  # MUTANT M10 shared-url-between-two-records: multi_row_url counting disabled
```
`selftest case=shared-url-between-two-records exit=0 want=0 verdict=fail` — problem:
`missing='multi_row_url=2'` (the AUDIT line now reads `multi_row_url=0`); exit stays 0 and both
records still bind — the case pins the informational `multi_row_url` count that makes the shared-URL
shape *audited* rather than silently ignored. Collateral: `shared-url-not-a-failure`
(`missing='multi_row_url=1'`), the one other case asserting that count.

**M09ab** (supplementary two-limb: M09a + M09b together; not one of the assigned one-limb probes) —
sha256 `b8f2491e4b0dc7c7b66284a425ecf141cea6f1c207b2ff0d72e7b9a036b0abef`
```diff
@@ -767 +767 @@
-    if not case_lines:
+    if False and case_lines:  # MUTANT M09a summary-only-selftest-rejected: summary-only limb disabled
@@ -778 +778 @@
-        if seen.get(name, 0) != 1:
+        if False and seen.get(name, 0) != 1:  # MUTANT M09b summary-only-selftest-rejected: case-line-count limb disabled
```
`selftest case=summary-only-selftest-rejected exit=0 want=1 verdict=fail` — problem:
`selftest problem=report-verifier case=summary-only-selftest-rejected problems=[]` — the forged
summary-only report (`selftest cases=23 failures=0` with no case lines) is now **accepted**
(observed exit 0, want 1), i.e. the guard's fixture passes. `complete-selftest-report-accepted`
still passes; summary `selftest cases=23 failures=1`, exit 1.

### 5. Findings

- **F1 — 9 of the 10 assigned cases are load-bearing against one-limb mutants.** Ten one-limb kills
  across the nine fixture cases (nested-snapshot-dir killed twice: blunt M03 on the walk limb,
  surgical M03b on the composed-naming limb). In every kill the delta is exactly the predicted one:
  either the guard's fixture passes (M01, M06, M08, M09ab), the discriminating `detail=` label dies
  while rejection survives (M04, M05), a pinned output line vanishes (M02, M03, M03b, M07, M10), or
  the exit flips (M02, M06, M08).
- **F2 — `summary-only-selftest-rejected` is defense-in-depth, not single-limb killable.** Both
  one-limb probes (M09a on the `summary-only-report` limb, M09b on the case-line-count limb) survive
  with byte-identical output: an empty `case_lines` already produces N `case-line-count` problems, so
  neither limb is individually load-bearing and neither survival counts as a kill. The two-limb
  M09ab is killed — the aggregate guard is load-bearing at depth 2. ExecCaptureBindingHarden
  (concurring by peer message): "a surviving one-limb mutant there is an equivalent mutant, not a
  kill, and you should not count it" — recorded as survived/equivalent-mutant class, attributed.
- **F3 — collateral honesty.** M03's walk limb is shared by all fixture cases (20 collateral kills);
  M03b narrows this to the one sibling nested case; M10's `multi_row_url` limb is shared by the two
  shared-URL cases (1 collateral). No mutant produced a verdict flip anywhere without a case-level
  FAIL line, and no A/D failure moved `records=`/`bound=` in any observed run — the README's
  "exit is the verdict, counts don't move" contract held in every fixture stdout quoted above.
- **F4 — peer-attributed coverage candidates (observed by ExecCaptureBindingHarden, relayed here,
  NOT probed by this seat — outside my assigned 10-case list):** (a) the case-line-count limb is
  unpinned by any *rejection* case — no case feeds an incomplete report (forged_complete minus one
  case line, or one duplicated); their round-35 candidate is `incomplete-selftest-report-rejected`
  feeding `forged_complete(expected)` minus one line, expected exit 1; (b) no case pins
  `detail=malformed` (calendar-invalid stamp) or the legacy-round present-but-invalid branch — both
  live in `classify_fetched`/`provenance_ok` but only `pending`/`local-offset` on modern rounds are
  pinned. My M04/M05 kills show exactly this shape of gap would matter: the labels are the
  discriminating part.
- **F5 — no defect filed against the instrument.** All kills are kills; the two survivals are
  equivalent-mutant class with a named depth-2 kill; controls behaved. The claimed invariant ("each
  of the ten new cases is load-bearing") holds for the nine fixture cases against one-limb mutants
  and for the report-verifier case against a two-limb mutant; the one-limb survival there is
  reported as a coverage characterization, not a contract change.

### 6. Restoration evidence

- The lane instrument was never written by this seat (mutants are scratch copies only). Digest
  before the work, after the work, and of the pristine scratch copy — all identical:
```
$ sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  (measured at session start, mid-run, and after scratch deletion)
```
- `pristine_matches_lane=True`, `lane_unchanged=True` (driver-recorded, run 3).
- Scratch tree deleted before yielding:
```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r34/MutCaptureBindingLimbs && echo "rm_exit=$?" && test ! -e /fast/scratch/hyaku/kasegi-r34/MutCaptureBindingLimbs && echo "scratch_absent=yes"
rm_exit=0
scratch_absent=yes
```
  My seat directory is gone; sibling seat directories under `/fast/scratch/hyaku/kasegi-r34/` were
  not touched. No scratch tree remains on disk for this seat — no defect to report on that count.

### 7. Tooling

No tools installed or upgraded (system `python3` 3.14.8 at `/usr/bin/python3`, coreutils
`sha256sum`; the operator tooling authorization was read and nothing needed installing — pacman
stayed untouched, per the host-wide pause).

### 8. Command record (verbatim forms)

```
python3 /fast/scratch/hyaku/kasegi-r34/MutCaptureBindingLimbs/mutate.py          # driver: baseline + 12 one-limb mutants + M09ab + 3 controls
python3 <copy>.py --selftest --scratch /fast/scratch/hyaku/kasegi-r34/MutCaptureBindingLimbs/st/<id>   # per-probe form
python3 /fast/scratch/hyaku/kasegi-r34/MutCaptureBindingLimbs/print_evidence.py  # evidence extraction from results.json
rm -rf -- /fast/scratch/hyaku/kasegi-r34/MutCaptureBindingLimbs                  # cleanup (verified absent after)
```

Driver: exact-once assertion per find string (`text.count(find) == 1` before replace), unified diff
per mutant, byte-identical stdout comparison for the SURVIVED class, per-probe rc/stdout/stderr logs.
The driver and all logs were scratch-local and deleted with the tree; this receipt quotes the
complete changed portions before deletion.
