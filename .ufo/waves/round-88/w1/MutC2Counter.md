# MutC2Counter — round-88 C2 counter mutation sweep

Seat: attack/mutation tester. Target: the frozen C2 counter
`.ufo/waves/round-88/c2/capability-check.py`
(sha256 `7bf648df5c72bf2e89bbafb1dad1447fc7b45b5ad4caa18c3382368ddf75ecdc`, unchanged after the sweep).
Base `6beead9148945fa695cf3139e8fc9d8e91cc5fd0`, C2 landing `b43dc2154bc09470da2209fb626021da3af3593e`.
Frozen control suite: `.ufo/waves/round-88/controls/c2-controls-r88.sh` +
`c2-controls-r88.txt` (sha256 `190510998cc1…` / `5aa9cdcd1df2…`).

No claim is re-scored. Everything below is a kill-power measurement of the counter and,
where the counter survives, a routed defect plus the control that is missing.

## 1. Method

24 single-point mutants, each applied to a **scratch copy** of the counter (one textual
replacement, occurrence count asserted to be 1, sha256 recorded). Detector = the 13 controls
that `c2-controls-r88.sh` actually executes, rebuilt in scratch exactly as the script builds
them (`git clone --shared` of the lane at the base, candidate/mutant instrument copied to
`corpus/instruments/`, SCORECARD row applied or dropped, one fixture commit with an asserted
toplevel) and run against pristine and mutant bytes. A mutant is **killed** when a control's
verdict (`CAPABILITY-CHECK-RESULT pass|fail` + exit code) differs from the pristine run of the
same control; limb-vector flips are recorded separately because they show detection without a
verdict flip.

Baseline reproduction: **13/13** controls reproduce the frozen receipt, verdict *and* limb
vector (receipt `survey.txt` §A).

Reproducibility defect found on the way (routed, not a kill): `c2-controls-r88.sh`'s `r87`
control is built from the **lane working tree** `corpus/instruments/capture-secret-scan.py`,
which the C2 landing replaced with the new instrument. Run after the landing, that control
degenerates into a second `pos` — my first sweep printed `r87 … CAPABILITY-CHECK-RESULT pass
rc=0`. Reproduced correctly here from the base blob:

    git -C . show 6beead9148945fa695cf3139e8fc9d8e91cc5fd0:corpus/instruments/capture-secret-scan.py > $S/base-instrument.py   # sha256 b2bf9d65e0a2…

with that instrument the control fails K4 (`rc=1`, `missing=…S004…, …E1…, …E2…, live-c.json`),
as the frozen receipt says.

## 2. Results (24 mutants)

| # | mutant | point | class | killing control(s) |
|---|---|---|---|---|
| 1 | K4-drop-new-union | union of expected sets → legacy set only | killed | pos (wrongsha, norow) |
| 2 | K4-spurious-expected | adds a S003 / aws-access-key-id pair to PLANT_EXPECT | killed | pos (wrongsha, norow) |
| 3 | K4-plant-remove-gcs-fixture | renames the S004 fixture key (plant set) | killed | pos (wrongsha, norow) |
| 4 | K4-subset-hits | `hits == set(PLANT_EXPECT)` → `hits <= …` | **limb-only** | noscope, nogcs, nojsonsep flip the K4 line |
| 5 | K4-files-always-true | `fok = rc3 == 1 and fhits == {…}` → `fok = True` | killed | filesclean |
| 6 | K4-files-subset | `fhits == {…}` → `(f1,azure) in fhits` | **equivalent** | none (see §3.2) |
| 7 | K4-stsallow-rc-ge1 | `rc2 == 2` → `rc2 >= 1` | killed | stsallow |
| 8 | K4-drop-rc1 | drops `rc == 1` from K4 | **missing control** | *rc-zero-fixture-only* (designed) |
| 9 | K5-last-cell-any | drops `rows[0][-1] == "87"` | **missing control** | *row-wrong-round* |
| 10 | K5-needle-any | `all(needles)` → `any(needles)` | **missing control** | *row-gcs-only* |
| 11 | K5-needle-drop-azure | drops the azure needle | **missing control** | *row-no-azure* |
| 12 | K5-len-ge | `len(rows) == 1` → `>= 1` | **missing control** | *row-duplicated* |
| 13 | K6-base-rev-candidate | base instrument read at `rev` instead of `BASE_REV` | killed | pos |
| 14 | K6-drop-base-rc | drops `rcb == 1` | **unkillable** | none possible (§3.3) |
| 15 | K6-drop-caught | drops `not caught` | **unkillable** | none possible (§3.3) |
| 16 | K2-drop-oracle-expected | drops `oracle == HISTORY_EXPECTED` | **unkillable** | none possible (§3.3) |
| 17 | K2-len-compare | `sts == oracle` → `len(sts) == len(oracle)` | **missing control** | *sts-path-misattributed* |
| 18 | K3-drop-hits0 | drops `summ[1] == 0` | **equivalent** | §3.2 |
| 19 | K3-drop-unused | drops `summ[4] == 0` | **missing control** | *stale-allow-row* |
| 20 | K3-drop-allowed | drops `summ[3] >= 1` | **equivalent** | §3.2 |
| 21 | K1-drop-gate-sha | drops the `--gate-sha256` pin | **missing control** | *gate-pin-wrong* |
| 22 | K1-drop-selftest | drops `rc == 0 and "SELFTEST-RESULT pass"` | **missing control** | *selftest-red* |
| 23 | RESULT-any | `all(ok …)` → `any(ok …)` | killed | 12 of 13 controls (all but `pos`) |
| 24 | RESULT-rc0 | `return 0 if allok else 1` → `return 0` | killed | 12 of 13 controls (all but `pos`) |

Totals: **killed 17/24** (8 by the frozen controls, 9 only by a designed control),
**detected-but-not-verdict-killed 1**, **equivalent 3**, **structurally unkillable 3**.

Per-mutant/per-control verdicts and every mutation spec: receipt `survey.txt` §B–§D.
Designed controls, pristine vs mutant limbs: receipt `designed-controls.txt`.

## 3. Survivors

### 3.1 Killable, but the frozen suite has no control (9 + 1)

Each was killed by a control I built that varies only the control tree / counter args, exactly
as `c2-controls-r88.sh` does. All are cheap; each failed the pristine counter on exactly one
limb and passed under the mutant.

| designed control | build (single change vs the `pos` tree) | kills |
|---|---|---|
| rc-zero-fixture-only | instrument's `scan_rev` returns 0 when the scanned lane's basename starts with `plant-` (prints the same HIT lines/summary) | K4-drop-rc1 |
| row-wrong-round | candidate row with last cell `86` | K5-last-cell-any |
| row-gcs-only | candidate row with `azure-sas-signature` and `corpus/practice/*/evidence/` removed | K5-needle-any |
| row-no-azure | candidate row with `azure-sas-signature` removed | K5-needle-drop-azure |
| row-duplicated | candidate row emitted twice (two `## Capabilities` rows) | K5-len-ge |
| gate-pin-wrong | `pos` tree, `--gate-sha256 0*64` | K1-drop-gate-sha |
| selftest-red | instrument selftest returns 1 while printing the same cases | K1-drop-selftest |
| stale-allow-row | candidate allowlist + one well-formed row for a non-existent path | K3-drop-unused |
| sts-path-misattributed | instrument appends `.x` to reported `aws-sts-session-token` paths under `.ufo/` | K2-len-compare |

Missing control for #4 (K4-subset-hits), not demonstrated: an instrument that **misses exactly
one planted pair while `--selftest` stays green** — e.g. raise the GCS hex floor above the
planted S004 length while the selftest's own positive sample stays longer. #4 is *detected*:
`noscope`, `nogcs`, `nojsonsep` each flip K4 from pass to FAIL under it, but none can flip the
verdict, because every frozen instrument mutant that disables a detection also fails
`--selftest`, so K1 fails in the same control. That coupling is structural for K1 against K4:
no frozen control can produce a *K4-only* verdict flip. Worth stating in the r89 control
notes.

### 3.2 Equivalent mutants (no control needed — the invariant is enforced elsewhere)

- **K4-files-subset.** Proof (`designed-controls.txt`, control `files-placeholder-flagged`):
  an instrument that also flags the doc placeholder `sig=<signature>` makes the pristine K4
  line read `extra=…S006…|azure-sas-signature … files_hits=2 files_ok=False`; under the mutant
  the same control reads `files_ok=True` but K4 **still FAILs** on `extra=…S006…`. The rev-mode
  direction (`hits <= set(PLANT_EXPECT)`) keeps exactness, and `rc3 == 1` already forces a
  non-empty `--files` hit set, so the subset form cannot admit anything the exact form rejects
  without a mode-dependent instrument. (That control's instrument also fails its own selftest,
  so K1 is FAIL in both runs — the same K1/K4 coupling as above; the argument rests on the K4
  line alone, which is identical apart from `files_ok`.)
- **K3-drop-hits0.** `not hits` (parsed HIT lines) enforces the same invariant: control
  `lane-extra-credential` (one in-scope tree file with a synthetic sig value beside `sv=`)
  fails K3 for both pristine and mutant (`summary=… hits=1` upstream, K3 FAIL in both).
- **K3-drop-allowed.** With the landing tree, an empty allowlist produces `hits=4`, so
  `summ[3] >= 1` is never the sole failing clause (control `empty-allowlist`: pristine and
  mutant both `LIMB K3 FAIL … allowed=0,unused_allow=0`, hits>0).

### 3.3 Structurally unkillable in this harness

- **K6-drop-base-rc** / **K6-drop-caught.** K6 reads the base instrument blob at the constant
  `BASE_REV` and scans the plant repo built from the constant `PLANTS`; controls vary only the
  candidate tree, so neither `rcb` nor `caught` can move. The det line still prints
  `base_rc`/`new_caught_by_base`, so a reader sees the values the limb no longer checks — but
  no verdict can see them. Only a counter-side fixture change (out of scope for controls)
  would exercise them.
- **K2-drop-oracle-expected.** `oracle` is `git grep` over the frozen `HISTORY_REV`; no control
  tree can alter git history at that revision, and a tree that cannot reach it produces a read
  error (`rc=2`) that fails identically under the mutant. The clause is a self-consistency pin
  against a rewritten object store, not a measurable guard.

## 4. Findings routed (defects/qualifiers, not re-scores)

**D1 — the frozen r87 control is not re-runnable after the landing.** §1 above.
A re-run of `c2-controls-r88.sh` now yields `r87 pass rc=0` (a duplicate of `pos`), which
silently drops one of the 13 detectors. Re-runnable evidence: `bash .ufo/waves/round-88/controls/c2-controls-r88.sh <scratch>`
and read the `control r87` block. Fix for r89: build that control from
`git show 6beead91:corpus/instruments/capture-secret-scan.py`, not from the working tree.

**D2 — `azure-sas-signature` misses escaped-separator URLs whose anchored param is not the
first query param.** The claim text says "either order, `&`/`&amp;`/`\u0026` separators"; the
pattern is `(?i)(?<![A-Za-z0-9_])(?:sv=…_PARAM_SEP sig=…|sig=…_PARAM_SEP sv=…)`, and the
lookbehind rejects the match when the preceding byte is `6` — the last byte of `\u0026`. So
`sv=`-first (or `sig=`-mid-query) JSON-escaped URLs are missed; plain `&` and `&amp;` work in
every position. Measured on the landed candidate (values built in memory, never written):

    python3 -B - <<'PY'
    import os, subprocess, sys, tempfile
    d = tempfile.mkdtemp(dir=os.environ["S"]); Q = "Q" * 44
    f = {"esc_sv_first.json": '{"u":"https://a.blob.core.windows.net/c/b.txt?sp=r\\u0026sv=2022-11-02\\u0026sig=%s"}' % Q,
         "esc_sig_first.json": '{"u":"https://a.blob.core.windows.net/c/b.txt?sig=%s\\u0026sv=2022-11-02"}' % Q,
         "amp_sv_first.json": '{"u":"https://a.blob.core.windows.net/c/b.txt?sp=r&sv=2022-11-02&sig=%s"}' % Q}
    for n, t in sorted(f.items()):
        p = os.path.join(d, n); open(p, "w").write(t)
        r = subprocess.run([sys.executable, "-B",
            "corpus/instruments/capture-secret-scan.py", "--files", p], capture_output=True, text=True)
        print(n, "rc=%d" % r.returncode, [l.split(" path=")[0] for l in r.stdout.splitlines() if l.startswith("HIT ")])
    PY

gives `esc_sv_first rc=0 []`, `esc_sig_first rc=1 [...]`, `amp_sv_first rc=1 [...]`; the base
instrument misses all three and `&amp;` variants hit. K4's plant set only exercises the
`sig=`-first escaped case (`w/z-receipts/live-c.json`), so the frozen predicate cannot see the
gap. Routed for r89: either relax the lookbehind for escaped separators or add the
`sv`-first-escaped case to the plant set (then K4 fails until the pattern is fixed).

**D3 — K6's novelty is 3 shapes + 2 scope.** Of the 5 `NEW_EXPECT` pairs, two
(`corpus/practice/p/evidence/E2.json` with `aws-sts-session-token` and with `credential`) are
shapes the **base** instrument already has: run beside the base gate with `--files` on that
path, the base instrument reports both hits; at `--lane/--rev` it reports nothing, because it
lacks the practice-evidence scope. So the frozen K6 detection line `new_caught_by_base=none`
is true but conflates shape novelty with scope novelty, and the `not caught` guard can never
fire for those pairs. Not a defect in the claim (C2 says "two new edge classes … plus the
practice-evidence scope"), but the r89 counter should split K6 into a shape limb and a scope
limb, or annotate which `NEW_EXPECT` pairs are scope-borne.

**Note on what the frozen suite does cover well** (do not regress it): K4's expected-set
exactness in both directions (pos / spurious / union-drop / fixture-removal), the `--files`
blindness limb (filesclean), the STS-allowlist refusal (stsallow), the always-clean instrument
(alwaysclean), the aggregation and exit code of the result line, the pin limbs (wrongsha), the
row presence limb (norow), and K6's base-instrument *source* (K6-base-rev-candidate → pos).

## 5. Restoration / integrity evidence

- Frozen counter sha256 before and after the 24-mutant sweep:
  `7bf648df5c72bf2e89bbafb1dad1447fc7b45b5ad4caa18c3382368ddf75ecdc` (identical). Mutants
  existed only as scratch copies; every control tree was a `git clone --shared` under
  `/fast/scratch/hyaku/kasegi-r88/MutC2Counter/` (deleted before yield).
- No write to the lane outside `.ufo/waves/round-88/w1/`; git use was read-only
  (`clone --shared`, `show`, `grep`, `rev-parse`). No fixture repo was created in the lane.
- All fixtures (planted credential values, synthetic `sig=` values, the doc-placeholder
  instrument) live only in scratch; receipts carry sha256 digests, LIMB/summary lines and
  paths, never fixture bytes. The landed scanner over the three receipts:
  `CAPTURE-SECRET-SCAN mode=files scanned=3 hits=0 files=0 allowed=0 unused_allow=17 rc=0`.
- Tooling installed: none (existing git 2.56.0 and python3 sufficed).

## 6. Files written

- `.ufo/waves/round-88/w1/MutC2Counter.md` (this report)
- `.ufo/waves/round-88/w1/MutC2Counter-receipts/survey.txt` — baseline 13/13, 24-mutant table,
  mutation specs, per-control verdict matrix, restoration digests
- `.ufo/waves/round-88/w1/MutC2Counter-receipts/designed-controls.txt` — the 10 designed
  controls: build spec, pristine limbs, mutant limbs, killed
- `.ufo/waves/round-88/w1/MutC2Counter-receipts/equivalence-and-probes.txt` — equivalence
  proofs, shape/scope probe, `\u0026` boundary probe, r87 reproducibility note
