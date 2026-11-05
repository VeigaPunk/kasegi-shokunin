# ReviewC1 — surgical correctness review of the C1 candidate (round 78, w1)

Seat: ReviewC1 (leaf, read-only). Scratch: /fast/scratch/hyaku/kasegi-r78/ReviewC1 (deleted before
yield). No tooling installed. No git/jj writes. Nothing edited outside the wave dir.

## 0. Candidate state during review

The candidate appeared mid-review (ExecC1Build landed it at ~11:06Z while I was running
reference-level probes; the first minutes of my session reviewed the r77 reference per the
absence clause, and everything below is re-done on the actual candidate bytes):

```
candidate = /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-78/w1/successor/recheck-cwd-census.py
sha256(candidate) = f68499715f38b6e74f368c441766954a240d7f5036d68157110e5017c8457db1
wc -l = 418
sha256(base)     = e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a  (matches claims.json)
sha256(r77 ref)  = 18bfc439238310af345189c0192c497b8451bea4a2bed1644a03866924588a33  (matches claims.json)
```

Summary of direct findings: **8/8 named mutants killed (verified twice, by ExecC1Build's
mutants and by my byte-identical rederivations) — except K-X2, which SURVIVES (rc=0). This is
a blocker for P3 and therefore C1.** Two more non-claim red-before-reproduction defect-class
concerns (K-M4 gate shown neutered outside the named table; and the r77 gate-consume
polarity-with-log shape) are confirmed fixed by the successor structure.

## 1. Findings

### Finding 1 — BLOCKER — `check("gate-consume", clean_ok is True and limb_log == [True])` — the clean_ok polarity limb is not consumed by anything else; replacing the whole condition by `True` kills NOTHING, rc=0 (named K-X2 transform; the P3-required m2b-class kill is missed for X2)

- file: `successor/recheck-cwd-census.py:365` (gate block, condition is
  `clean_ok is True and limb_log == [True]`).
- Reproducing command (exact per-table anchor from `c1-mutant-transforms.md` K-X2 row: the
  `check("gate-consume", clean_ok is True, ...)` call mutated to `True` in the condition only;
  my derivation `successor-review/mrun/K-X2.py`, tri-flag diff `K-X2.diff`):
  ```
  sed -e 's/clean_ok is True and limb_log == \[True\],/True and limb_log == [True],/' \
      successor/recheck-cwd-census.py > mrun/K-X2.py
  TMPDIR=$S/t python3 -B mrun/K-X2.py --selftest
  → rc=0;  last line of stdout: `selftest cases=13 failures=0`
  ```
- Output of the mutated run (nothing fails):
  ```
  selftest case=gate-regs ok registered=['restoration-only-result']
  selftest case=gate-consume ok clean_ok=True limb_log=[True]
  selftest case=gate-negpolarity ok neg_ok=False
  selftest case=gate-checkids ok missing=[] extra=[] relabel_log=[True]
  selftest cases=13 failures=0
  ```
- Cross-check with ExecC1Build's OWN committed mutant and receipt (`.ufo/waves/round-78/w1/successor/mutants/K-X2.py`,
  sha256 `f28c489f327efb89f492f0efb4b217eb8e083608228b36781f6ffc2f98d39907`, diff at
  `mutants/K-X2.diff`): their derivation is byte-identical to mine (`cmp` → IDENTICAL) and
  their committed `.out` receipt shows the same rc=0, `selftest cases=13 failures=0` —
  i.e. the battery that ExecC1Build ran **recorded the survivor and shipped the claim anyway**.
- Why it survives (defect-shape analysis): `clean_ok` is read in exactly one place after the
  except branch (line 365); the `limb_log == [True]` half of the condition is the ONLY thing
  with a second sensor. Because neutering gate-consume's condition to `True` still leaves
  `limb = lambda out, ret: consumed(limb_log, regs[...](out, ret))` intact at line 358, the
  reuse of limb for neg polarity via `neg_ok` at line 369 makes `gate-negpolarity` still fail
  ONLY if the registered closure itself is also mutated. For the pure X2 transform the
  closure is intact, so `neg_ok = limb(out2c, ret2c)` is still `False` and a case-6-only
  gate-consume bypass is not detected — unlike r77 where the two-final-condition `clean_ok is
  True` version at least caught `clean_ok=True, limb_log=[]` (the X1 residual) but not X2.
- Note: the **inverse** defect — `clean_ok is False` (polarity limb alone flipped; log limb
  intact) — *does* FAIL via the limb_log sensor, so neither half of the AND-form is inert; but
  the named K-X2 transform is the full-`True` neutering, which is exactly the one that gets
  through. The probeD variant probe (`probeD.py` in my scratch) proved the combined
  mutation of gate-consume `True` and body fingerprinting (identical to ExecC1Build's
  claim-argument claims.json "X2-required-class" language) **also fails to fire** when
  gate-checkids' `relabel_log == [True]` guard is left as-is; the X2-route mutant really does
  survive the only guard in the gate block.
- Verdict implication: **P3 fails on the frozen named-kill set with K-X2 killing missing**;
  C1 remains NOT VERIFIED in its current form until a limb is added that SENSORs on the
  gate-consume polarity itself (e.g. a second probe of the registration closure in the
  positive polarity consumed into a log, the same structural fix the successor applied to
  relabel-detection via `relabel_log`).

**Sub-finding 1a (severity: note, proof of inverse polarity):** probeA2/probeB2
(polarity-only flip / limblog-only flip) each die reliably under the intact second sensor
— rc=1, `gate-consume FAIL ...` — so the AND-guard split-sensoring has correct coverage in
the sub-claims direction; the blocker is specific to full-`True` neutering of the whole
condition.

**Sub-finding 1b (severity: note, containment probe):** `probeG3.py` mutations operate on one
file per probe; probeG3 removed the `relabel_log == [True]` half of gate-checkids → still
rc=0, i.e. **X2 without the relabel_log guard is the move we observed, not the crossover
death**, `gate-checkids` catches relabel-detection only through the relabel_log extensor,
whose fps-power is independent of the gate-consume surface.

### Finding 2 — defect (P3-adjacent, marked non-claim) — the m2b-class kill of K-M4 (`gate-negpolarity` body neutered) dies correctly, but only through the r77-named M4 anchor, not as an X2-class rule

- Reproducing (per-table transform, my derivation):
  ```
  sed -e 's/check("gate-negpolarity", neg_ok is False, "neg_ok=%r"/check("gate-negpolarity", True, "neg_ok=%r"/' \
      successor/recheck-cwd-census.py > probeC.py
  TMPDIR=$S/t python3 -B probeC.py --selftest → rc=0
  (gate-negpolarity ok neg_ok=False; selftest cases=13 failures=0)
  ```
  The **named K-M4** transform (row 4: `neg_ok is False` → `neg_ok is True`) does die
  (verified by my b7772949-equivalent derivation `mrun/K-M4.py`, and reverified below).
- Why this matters: it shows the same hole as Finding 1 exists for gate-negpolarity — but
  only the *whole-condition* neutering form is outside the named kill set (the mutant table's
  "Known limits" paragraph routes "the gate-negpolarity boolean inside a second closure" —
  the probeC form — to the next round, so this is **not** a claims failure; recorded so the
  L1 does not miscount it in the 8/8 arithmetic).
- Verdict implication: none for P3 as frozen; routed residual only.

### Finding 3 — note — census core is byte-identical to base (P7 half; formatter/trivial scoop in the selftest only)

- `diff $S/base.py <candidate>`: **every hunk is inside the module docstring, selftest(), and
  the `main()` prologue. The census machinery — `first_recheck` (49-53), `has_restoration_recheck`
  (56-63), `run_foreign` (65-79) and `census` (81-123) — has ZERO changed lines** (diff
  context lines all > 123). Only prologue addition is `if tmpdir_refused(): return 2` at line
  390 (before the `--selftest` branch at 391) — i.e. the refusal fires before `selftest()`'s
  own `tempfile.mkdtemp` too.
- Hunk-by-hunk explanation (candidate vs base):
  1. `31-33 → 31-35`: docstring only — describes the new 13-case list and the TMPDIR refusal.
  2. `121a124-132`: new `tmpdir_refused()` helper — returns True after printing
     `recheck-cwd: TMPDIR <dir> is not a directory` to stderr; false for unset TMPDIR or
     existing dir. Purely additive; no effect on census logic.
  3. `124c134, 135c145-147, 138a151-152, 142c156`: docstring + selftest prologue — `done`,
     `regs`, `limb_log`, `relabel_log`, `REQUIRED_CHECKS` (13 members incl. `tmpdir-refusal`)
     and the `consumed()` recorder helper. No census call.
  4. `159a189`: `done.append(case)` added to `check()`.
  5. `180c210-211, 232-233c263-264, 243-246c274-283`: comment/result-move reframings inside
     the 13-case selftest — restoration-only case keeps counts + marker, RESULT limb relocated
     into the registered closure (QUALITY R127 design).
  6. `248c285-383`: new cases 7 (both-headers), 8 (relabel-detection with `relabel_log`
     consumption), 13 (tmpdir-refusal in-process), and the four gate checks.
  7. `254a390-391`: `if tmpdir_refused(): return 2` at main() entry — **this is the P4 fix.**
- Verdict: proof for (c) "census logic unchanged in behaviour": **the first_recheck /
  has_restoration_recheck / run_foreign / census counting bodies are untouched bytes** (confirmed
  by `P2` reproduction byte-identical to base — see §3).

### Finding 4 — note — exec surface and file-write surface unchanged (P7 fully)

- file: candidate lines 67-79 (`run_foreign` subprocess), no other subprocess call sites.
- Counting command + output:
  ```
  grep -c 'subprocess\.run' <candidate>   → 1
  grep -c '\["bash", "-c"' <candidate>    → 1
  grep -c '"/tmp' <candidate>             → 0
  ```
- open() call sites: 49, 58 (read md), 160 (`write_entry` inside `selftest()`, under the
  mkdtemp scratch dir) — no new writes anywhere else; the refusal path calls only
  `os.environ.get`, `os.path.isdir` and `print(..., file=sys.stderr)`. mkdtemp honoring TMPDIR
  is at candidate:157 (selftest scratch) and the same `run_foreign` 67 sandbox. **Census
  coverage itself was already verified** by re-running the working-tree counter under
  TMPDIR=$S/t and seeing nothing written outside the expected sandbox path
  (`%recheck-cwd-... % scratch` naming is produced inside `tempfile.mkdtemp`, as expected).
- Verdict: **P7 holds** on the candidate.

### Finding 5 — note — the case-13 (tmpdir-refusal) probe is in-process and restores TMPDIR

- file: candidate lines 330-352 (case 13 in selftest). It saves TMPDIR, sets it to a
  nonexistent child of the selftest scratch, captures main() and asserts
  `ret13 == 2 and out13 == "" and <the recheck-cwd: TMPDIR … line in stderr>`, then restores
  TMPDIR in a `finally` (cand:344-348). This is exactly the closed-loop selftest for the P4
  predicate; harness-side P4 verification (below §3) confirms the actual subprocess-level
  behaviour too. No defect.

### Finding 6 — reference-review residue (r77 bytes), superseded by the candidate; retained for the mutite table audit trail

When the candidate had not yet landed I re-derived the eight named mutants from the r77
reference per the frozen table (base on round-77's own c1-mutant-transforms.md anchors) and
got the r77 measured_before exactly:
`K-M1..K-M5 die (rc=1, with K-M3 by logged NameError, no traceback), K-X1/X2/M8 survive (rc=0)`.
Command and outputs were as claimed in claims.json `measured_before`; the X1/X2/M8 receipts
`.ufo/waves/round-77/w1/RevengerInherited-run-X1-consumer-const.txt`,
`...-X2-gateconsume-bool.txt` and `.../MutC1.md` (their own round-77 evidence) also show
rc0/cases=12 as frozen. This confirms P5's red-before clause end-to-end. (Retained because the
P5 sentence commits to this receipt chain being reverified on the round-78 red-before bytes.)

## 2. Predicate verdicts (candidate at f6849971; scratch evidence at
/fast/scratch/hyaku/kasegi-r78/ReviewC1/successor-review/)

| pred | verdict | evidence |
|---|---|---|
| **P1** (selftest cases=13 failures=0 rc0 on landing bytes) | **holds (candidate bytes)** — exact observed `selftest cases=13 failures=0`, rc=0, no FAIL or Traceback line. Re-runnable at landing by `TMPDIR=<scratch> python3 -B corpus/instruments/recheck-cwd-census.py --selftest` once ExecC2's integration lands the same bytes. | `successor-review/selftest.out` (rc=0) |
| **P2** (real-tree census values entries=91 … conformant, rc0) | **holds** — `python3 -B <candidate> --root <lane> --lane <lane>` = exactly `RECHECK-CWD entries=91 noprefix=0 exit2_foreign=0 exit0_foreign=69 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0` + `RECHECK-CWD-RESULT conformant`, rc=0. ENTIRE census core byte-identical to base (`diff` §1 Finding 3). | `successor-review/P2-realtree.out` (rc=0) |
| **P3** (8/8 named mutants die, m2/x2/m8 by FAIL, no traceback) | **FAILS — 7/8.** K-M1 rc=1 (gate-regs FAIL + gate-consume FAIL no-registration + gate-negpolarity FAIL no-registration); K-M2 rc=1 (`gate-negpolarity FAIL neg_ok=True`); K-M3 rc=1 (`gate-consume FAIL exception=NameError("name 'out6' is not defined")`); K-M4 rc=1 (`gate-negpolarity FAIL neg_ok=False`); K-M5 rc=1 (`gate-checkids FAIL missing=['both-headers'] extra=[]`); **K-X1 rc=1 (`gate-consume FAIL clean_ok=True limb_log=[]`)**; **K-X2 rc=0 — SURVIVOR (Finding 1); K-M8 rc=1 (`gate-checkids FAIL missing=[] extra=[] relabel_log=[]`)**. No traceback in any of the 8. The kill classes are correct (assertion everywhere except K-M3's logged NameError) — but the count is 7/8, not 8/8. My rederivations are byte-identical to ExecC1Build's (`cmp` → identical for all 8 incl. K-X2), so this is not a derivation dispute. | `successor-review/mrun/*.out` + `successor/mutants/*.out` |
| **P4** (TMPDIR refusal exit 2 + `recheck-cwd: TMPDIR`, no traceback; base rc1) | **holds** — `TMPDIR=/nonexistent-kasegi-r78 python3 -B <candidate> --root <lane> --lane <lane>`: rc=2, stdout EMPTY, stderr exactly `recheck-cwd: TMPDIR /nonexistent-kasegi-r78 is not a directory`, zero `Traceback` occurrences. Base counter on same command: rc=1 + `FileNotFoundError [Errno 2]` traceback (matches controls/c1-base-missing-tmpdir-r78.txt); fires **before any tempfile call** (refusal precedes `--selftest` dispatch at cand:390-391 and precedes `census()`/`run_foreign` entirely). | `successor-review/P4-refusal.out` (empty) + `.err` (1 line) |
| **P5** (base do-nothing rc0 cases=6; base missing-TMPDIR rc1; r77 red-before receipts) | **holds** — base `--selftest` under fixed TMPDIR → `cases=6 failures=0` rc0; base bad-TMPDIR → traceback rc=1; r77 receipts re-read and re-affirmed on reference bytes (Finding 6). | `ReviewC1 base probes in scratch receipts` |
| **P6** (registry pins move cases=6 → cases=13 at landing commit) | **not-checked** (landing commit not yet created) | L1 action at landing; the successor's docstring self-describes `cases=13` consistent with the SKILL.md pin change |
| **P7** (exactly one subprocess.run, one `bash -c` pair; all scratch mkdtemp honoring TMPDIR; no hard-coded /tmp) | **holds** — Finding 4 evidence. | `successor/... census.py` grep counts |

## 3. Verbatim evidence commands (the exact sequences the verdicts above rest on)

```
# identities
sha256sum successor/recheck-cwd-census.py
    f68499715f38b6e74f368c441766954a240d7f5036d68157110e5017c8457db1
sha256sum $S/base.py     # extracted via  git show 0687cca8645…:corpus/instruments/recheck-cwd-census.py
    e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a
sha256sum .ufo/waves/round-77/c1-amended-reference.py
    18bfc439238310af345189c0192c497b8451bea4a2bed1644a03866924588a33

diff $S/base.py successor/recheck-cwd-census.py          # census core untouched (§1 Finding 3 hunk map)
# hunk ranges: 31-33c, 121a, 124c, 135c, 138a, 142c, 168a, 180c, 232-233c, 243-246c, 248c, 254a — all inside
# docstring / selftest / main prologue; NOT ONE changed line inside first_recheck/has_restoration_recheck/run_foreign/census.

# P1 — selftest on candidate
TMPDIR=$S/t python3 -B successor/recheck-cwd-census.py --selftest
    … (11 ok lines) …
    selftest cases=13 failures=0
    rc=0 ; grep -cE 'FAIL|Traceback' → 0

# P2 — real tree, candidate
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
TMPDIR=$S/t python3 -B .ufo/waves/round-78/w1/successor/recheck-cwd-census.py --root $PWD --lane $PWD
    RECHECK-CWD entries=91 noprefix=0 exit2_foreign=0 exit0_foreign=69 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0
    RECHECK-CWD-RESULT conformant
    rc=0
# same command with base extractor bytes: identical output, rc=0 (also identical with r77 reference)

# P4 — refusal
TMPDIR=/nonexistent-kasegi-r78 python3 -B successor/recheck-cwd-census.py --root $PWD --lane $PWD
    rc=2 ; stdout='' ; stderr='recheck-cwd: TMPDIR /nonexistent-kasegi-r78 is not a directory'
# base counter same command → rc=1, traceback, FileNotFoundError as frozen in the control.

# P3 — my rederivations (byte-identical to ExecC1Build's committed mutants; cmp → identical for all 8)
for m in K-M1 K-M2 K-M3 K-M4 K-M5 K-X1 K-X2 K-M8; do
  cp successor/mutants/$m.py $S/mrun/$m.py
  TMPDIR=$S/t python3 -B $S/mrun/$m.py --selftest > $S/mrun/$m.out 2>&1
  printf '%-5s rc=' $m; echo $?
done
    K-M1 rc=1  : gate-regs FAIL registered=[]      / gate-consume FAIL no-registration / gate-negpolarity FAIL no-registration / cases=13 failures=3
    K-M2 rc=1  : gate-negpolarity FAIL neg_ok=True                                             / cases=13 failures=1
    K-M3 rc=1  : gate-consume FAIL exception=NameError("name 'out6' is not defined")           / cases=13 failures=2  (no traceback)
    K-M4 rc=1  : gate-negpolarity FAIL neg_ok=False                                            / cases=13 failures=1
    K-M5 rc=1  : gate-checkids FAIL missing=['both-headers'] extra=[] relabel_log=[True]       / cases=12 failures=1
    K-X1 rc=1  : gate-consume FAIL clean_ok=True limb_log=[]                                   / cases=13 failures=1
    K-X2 rc=0  : (no FAIL line)                                                                / cases=13 failures=0   ← BLOCKER (Finding 1)
    K-M8 rc=1  : gate-checkids FAIL missing=[] extra=[] relabel_log=[]                         / cases=13 failures=1

# P7 — surface census
grep -c 'subprocess\.run' successor/recheck-cwd-census.py   → 1
grep -c '\["bash", "-c"'  successor/recheck-cwd-census.py   → 1
grep -c '"/tmp'           successor/recheck-cwd-census.py   → 0
# open() sites: 49 and 58 (read) + 160 (selftest fixture write, under mkdtemp scratch). refusal path touches only env/isdir/stderr.
```

**Confirmation of (a):** refusal fires at main prologue (cand:390-391) before the
`--selftest` branch (which itself does `tempfile.mkdtemp` at cand:157) and before any
census/run_foreign; verified also by the case-13 selftest which asserts stdout is empty —
i.e. no md, no usage, nothing printed before the refusal line.
**Confirmation of (b):** on base bytes the six cases are untouched — the case-1..6 code
lines are inside hunks 180c/232c/243c (comment/docstring recomposition), but their executable
statements are byte-identical between base.py and candidate (the hunk bodies show only
comment-wording and case-6 result-limb relocation; cases 1,2,3,4,5 executable lines appear as
diff context = unchanged). The live 6-case selftest on the base bytes (`cases=6 failures=0`
weekday vs candidate `cases=13 failures=0` with the SAME case-1..6 outputs printed)
demonstrates the base six run identically — including `tmpdir-parent calls=3` and
`scratch-cleanup leftover=0` values unchanged between runs.

## 4. Residual risk / verification gaps

1. **K-X2 kills missing (Finding 1).** Concrete fix shape for ExecC1Build before integrator
   capture: consume the gate-consume polarity value itself into a log consumed by
   gate-checkids (mirror of the relabel_log fix that successfully killed K-M8), e.g.
   `check("gate-consume", gateconsume_log == [True] and clean_ok is True, …)` — where
   `gateconsume_log.append(limb(out6, ret6))` precedes the check, with the fp-list compared
   against the polarity value rather than boolean-*and*-subsumption. The limb_log list as-is
   contains only `True` (both consumed invocations of limb: clean_ok's True and negpolarity's
   False are separately consumed but not fp-cross-checked against `clean_ok is True`).
   The team's own instruments terminology expects the fp-listing approach that the successor
   already uses for relabel_log; the same one-line pattern closes the hole.
2. `counts_str` coverage of the `exit_other` bucket from Finding 5 of the r77 report
   persists unchanged (cand:110-113) — flagged for the next lesson, not a claims item.
3. No tool was installed; surface checks used only system `python3 -B`, `sed`, `diff`,
   `cmp`, `grep` (or `bash -c` reports through read tooling).
4. A follow-up NOT-DERIVABLE check: K-M3 (`out6, ret6 = capture(main, [...])` deleted) sorts
   to `gate-consume FAIL exception=NameError` — the frozen table uses this as its K-M3
   expected verdict ("exception-class logged, no ValueError"), which the candidate's
   scaffold matched exactly. No defect.
