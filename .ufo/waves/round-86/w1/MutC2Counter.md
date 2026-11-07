# MutC2Counter — mutation probe of the frozen C2 counter

Seat: MutC2Counter (mutation-tester, leaf). Kasegi round 86, attempt 1, wave w1.
Probed bytes: `.ufo/waves/round-86/c2/e2e-check.py`
sha256 `b4a97e095da1d869a0e8c0b82f758ba8d517ae2d10cf72e48e7fc4962578a834`
(freeze commit `252df0c90c066d83d229e3107811a6bc05e8feed`, base `d7296645…`).
Gate under test (`corpus/instruments/claim-package-check.py`) sha256
`8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6`;
frozen control script sha256 `ab4e3914…`; S122 `ceb01841…`, S123 `22a7d5be…`.

## Method and integrity

- **39 single-point mutants** were generated from one copy of the frozen
  counter. Every anchor is a unique substring (`count == 1` asserted); each
  mutant changes exactly one behaviour-bearing expression. Mutant sha256s are
  in `MutC2Counter-receipts/mutation-results.json`.
- **Detector = the freeze's own control set.** `controls/c2-controls-r86.sh` was
  copied into scratch and patched on exactly two lines: the `C=` command and the
  printed counter sha, so the script can target `$COUNTER`. Every fixture it
  builds (`b3`, exemplar copy, 18 pricing reports) is byte-identical to the
  freeze's. The pristine counter over this reconstruction reproduces
  `controls/c2-controls-r86.txt` at verdict level **23/23 controls**
  (`compare-controls.txt`, `verdict-mismatches=0`). The only textual drift is
  the `donothing` E5 detail (`shonen=True`, because the live `SHONEN.md` now
  names the C2 package path) — the same limb verdict, FAIL.
- **Kill criterion** (the spec's, same as round 85): at least one control
  changes its `(rc, per-limb pass/FAIL)` signature. A change in printed detail
  tokens with the same verdicts is recorded as `detail-only`, not as a kill.
- **27 probes** (`probe-matrix.txt`): each survivor is paired with a scratch-lane
  probe whose pristine verdict differs from the mutant's. Lane fixtures live
  under `$S` (snapshots copied from the committed bytes, gate copied, a golden
  package built from those snapshots). All 27 distinguish pristine from mutant.
- Sibling-seat note (not mine, not edited): `ExecC2Package-candidate/…/evidence/`
  already holds `S120.txt`–`S123.txt`. Those basenames are not among the 203
  frozen C1 map keys (`repair-map.json` checked), so C1's M4 uniqueness limb is
  unaffected by them; the four snapshots cited here are cited by lane path and
  sha256, not copied.
- Writes: scratch `/fast/scratch/hyaku/kasegi-r86/MutC2Counter/` (removed on
  exit) and this wave dir. Frozen counter, gate, controls, S122/S123 and the
  round-86 manifest hashes are unchanged before/after
  (`hashes-after.txt`). No git/jj write; lane tree untouched.

## Result: 15 killed / 39 (38.5 %), 24 survivors

| # | mutant | single point | verdict | killed by (frozen control) |
|---|--------|--------------|---------|----------------------------|
| 1 | `e0_head_no_subject` | E0 heading drops `SUBJECT in first` | **killed** | b3-url-added, wrong-subject-heading |
| 2 | `e0_head_no_cve` | E0 heading drops `want["cve"] in first` | survived | — |
| 3 | `e0_head_no_hash_prefix` | E0 heading drops `startswith("# ")` | survived | — |
| 4 | `e0_url_always_true` | E0 `url_ok = True` | survived (detail-only) | — |
| 5 | `e0_no_stray_check` | E0 `stray = []` | **killed** | stray-report-url |
| 6 | `e3_no_dup_check` | E3 `ok` drops `not dup` | **killed** | duplicate-key |
| 7 | `e3_dup_never_detected` | E3 never records a repeat | **killed** | duplicate-key |
| 8 | `e3_sections_ge1` | E3 `len(heads) == 1` → `>= 1` | **killed** | two-pricing-sections |
| 9 | `e4_min_quote_10` | `MIN_QUOTE = 10` | survived | — |
| 10 | `e4_min_quote_1` | `MIN_QUOTE = 1` | survived (detail-only) | — |
| 11 | `e4_no_short_check` | E4 drops `not short` | **killed** | short-quotes |
| 12 | `e4_no_s123_requirement` | E4 drops `bool(from_s123)` | **killed** | no-s123-quote, r85-package |
| 13 | `e4_s123_taken_from_s120` | E4 S123 pool → S120 pool | **killed** | no-s123-quote, r85-package |
| 14 | `program_hardwired_curl` | `program` hardwired to `curl` | **killed** | positive-pricing, forged-program |
| 15 | `payer_drop_handle_conjunction` | payer = PAYER_LINE only | survived | — |
| 16 | `payer_drop_s123_conjunction` | payer = handle only | survived | — |
| 17 | `policy_drop_end_line` | policy = S121 clause only | survived | — |
| 18 | `policy_drop_s121_conjunction` | policy = END_LINE only | survived | — |
| 19 | `severity_drop_s120_agreement` | severity from S122 alone | survived | — |
| 20 | `flag_truthy_not_strict_true` | `is True` → truthy | survived | — |
| 21 | `original_report_drop_s120_corroboration` | original id without S120 check | survived | — |
| 22 | `reward_regex_digits_only` | `Bug bounty: (\d+)` | **killed** | positive-pricing + 7 forgeries |
| 23 | `kev_always_not_listed` | `count == 0` → `>= 0` | survived | — |
| 24 | `kev_reverse_prefix` | prefix predicate reversed | **killed** | positive-pricing, forged-kev |
| 25 | `cve_lowercased` | `cve` lowercased | **killed** | positive-pricing + all forgeries |
| 26 | `e2_drop_manifest_digest` | E2 drops `h == rec[sid]` | survived | — |
| 27 | `e2_drop_byte_equality` | E2 drops `b == snap` | survived | — |
| 28 | `e2_drop_recorded_artifact_digest` | E2 drops package-recorded digest | survived | — |
| 29 | `e2_follow_symlinks` | E2 drops the symlink skip | survived | — |
| 30 | `e2_found_subset` | `found == {…}` → `found <= {…}` | **killed** | r85-package, exemplar-copy |
| 31 | `e2_require_third_source` | E2 demands S120 too | **killed** (over-strict) | b3 × 2 |
| 32 | `reward_case_insensitive` | reward compared case-folded | survived | — |
| 33 | `e1_drop_verdict_check` | E1 keeps rc only | survived | — |
| 34 | `e1_drop_rc_check` | E1 keeps verdict string only | survived | — |
| 35 | `e4_quotes_not_normalized` | E4 quotes not whitespace-collapsed | survived | — |
| 36 | `e4_pool_includes_kev` | E4 pool += S052 (KEV) | survived | — |
| 37 | `severity_case_sensitive` | severity compared case-sensitively | survived | — |
| 38 | `e5_or_instead_of_and` | E5 `and` → `or` | **killed** | donothing |
| 39 | `allok_skips_e1` | overall verdict ignores E1 | survived | — |

No mutant is equivalent: each of the 24 survivors has a probe that flips it
(`probe-matrix.txt`). Two survivors change a printed detail without changing a
verdict (`e0_url_always_true`: exemplar E0 `url=False→True`; `e4_min_quote_1`:
short-quotes `short=2→1`); the control set asserts no detail token, so these
would pass unnoticed even at the detail level.

## Survivors — one killing control each

`P:` = probe id in `probe-matrix.txt` / re-run by `mutate-harness-r86.py`;
the flip is the pristine verdict → the mutant verdict on the listed limb.

| survivor | P: probe | flip (pristine → mutant) | expected limb |
|---|---|---|---|
| `e0_head_no_cve` | `p_e0_head_no_cve` | E0 FAIL → pass (heading names 1997312 but CVE-2025-9086) | E0 |
| `e0_head_no_hash_prefix` | `p_e0_no_hash_prefix` | E0 FAIL → pass (line 1 has no `# `) | E0 |
| `e0_url_always_true` | `p_e0_url_missing` | E0 FAIL → pass (no 1997312 URL in report) | E0 |
| `e4_min_quote_10` | `p_e4_min10_16char_quote` | E4 FAIL → pass (a 16-char quote) | E4 |
| `e4_min_quote_1` | `p_e4_min1_16char_quote` | E4 FAIL → pass (a 16-char quote) | E4 |
| `payer_drop_handle_conjunction` | `p_payer_no_handle` | E3 FAIL → pass (S122 handle `curl`, PAYER_LINE present) | E3 payer |
| `payer_drop_s123_conjunction` | `p_payer_no_s123` | E3 FAIL → pass (S123 without the payer sentence) | E3 payer |
| `policy_drop_end_line` | `p_policy_no_endline` | E3 FAIL → pass (S123 without END_LINE) | E3 policy |
| `policy_drop_s121_conjunction` | `p_policy_no_s121` | E3 FAIL → pass (S121 without "There is no bug bounty") | E3 policy |
| `severity_drop_s120_agreement` | `p_severity_no_s120` | E3 FAIL → pass (S120 `Severity: High`) | E3 severity |
| `flag_truthy_not_strict_true` | `p_flag_truthy` | E3 FAIL → pass (`has_bounty? = 1` not `true`) | E3 flag |
| `original_report_drop_s120_corroboration` | `p_original_no_corroboration` | E3 FAIL → pass (S120 without the Original-report line) | E3 original-report |
| `kev_always_not_listed` | `p_kev_always_not_listed` | E3 FAIL → pass (S052 lists the CVE) | E3 kev |
| `e2_drop_manifest_digest` | `p_e2_no_manifest_binding` | E2 FAIL → pass (lane manifest lies about S122) | E2 |
| `e2_drop_byte_equality` | `p_e2_drop_byte_equality` | E2 FAIL → pass (evidence bytes differ, hashes agree) | E2 |
| `e2_drop_recorded_artifact_digest` | `p_e2_lying_recorded_digest` | E2 FAIL → pass (package records `f…f`, bytes true) | E2 |
| `e2_follow_symlinks` | `p_e2_symlink_evidence` | E2 FAIL → pass (`evidence/S122.txt` is a symlink) | E2 |
| `reward_case_insensitive` | `p_reward_case` | E3 FAIL → pass (`2400 usd`) | E3 reward |
| `e1_drop_rc_check` | `p_e1_rc0_bad` | E1 FAIL → pass (gate prints DEFECT, exits 0) | E1 |
| `e1_drop_verdict_check` | `p_e1_rc3_good` | E1 FAIL → pass (gate prints WELL-FORMED, exits 3) | E1 |
| `e4_quotes_not_normalized` | `p_e4_ws_quote` | E4 pass → FAIL (quote with a double space) | E4 |
| `e4_pool_includes_kev` | `p_e4_kev_quote` | E4 FAIL → pass (an S052-only quote) | E4 |
| `severity_case_sensitive` | `p_severity_case` | E3 pass → FAIL (`price-severity: Medium`) | E3 severity |
| `allok_skips_e1` | `p_allok_only_e1_fails` | `E2E-RESULT fail` → `pass` (gate absent, E0/E2–E5 pass) | overall |

## Does the r86 hardening close the r85 survivors?

Round 85 measured 6/20 killed. This run measures 15/39 (38.5 %); the control set
also grew from 11 to 23 controls, so the ratios are not directly comparable —
the class-by-class answer is:

| r85 survivor class | r86 counterpart mutant | r86 verdict |
|---|---|---|
| `e5_or` (E5 `and`→`or`) | `e5_or_instead_of_and` | **closed** (killed) |
| `e2_one_source` | `e2_found_subset` | **closed** (killed via the r85-package/exemplar E2 FAIL→pass) |
| `e1_rc_only` | `e1_drop_rc_check` | open |
| `e1_verdict_only` | `e1_drop_verdict_check` | open |
| `e2_drop_recorded_sha` | `e2_drop_recorded_artifact_digest` | open |
| `e2_drop_manifest_binding` | `e2_drop_manifest_digest` | open |
| `e2_symlink_evidence` | `e2_follow_symlinks` | open |
| `sev_ignore_s120` | `severity_drop_s120_agreement` | open |
| `reward_case_insensitive` | `reward_case_insensitive` | open |
| `e4_threshold_1` | `e4_min_quote_10` / `_1` | open (threshold class moved to length) |
| `e4_raw_no_norm` | `e4_quotes_not_normalized` | open |
| `e4_pool_includes_kev` | `e4_pool_includes_kev` | open |
| `allok_ignores_e1` | `allok_skips_e1` | open |

So the named hardening closed **2 of 13** r85 survivors (E5 conjunction, E2
subset). The four clauses r86 *added* are themselves only partly covered:

- E0: changed heading-subject check and stray check are live; the `# ` prefix,
  the CVE-in-heading check and URL presence are not (3 mutants survive).
  `url_ok` changes a detail token in the exemplar control but no verdict.
- Duplicate keys (2 mutants) and the single-section check: live.
- `MIN_QUOTE`: not tested at its boundary — a 16-character quote accepted by
  `MIN_QUOTE=10` and by `MIN_QUOTE=1` is rejected only because the frozen
  short-quotes fixture uses 0- and 1-character quotes. Quote normalization and
  the S052-free pool are untested (r85's `e4_raw_no_norm` /
  `e4_pool_includes_kev` defects persist through the rewrite).

## Routed defect 1 — `R86-C2-MUT-1`: the control set still has no success-path negatives

24 of 39 single-point mutants leave every frozen control's verdict identical.
The missing control shapes are exactly the ones the r85 probe suite named, minus
E5: a gate with `(verdict, rc)` disagreement, a package with a lying recorded
digest, a lying lane manifest, a symlinked artifact, a package where only E1
fails, a lane where only one of LOG/SHONEN names the package, a policy/payer
conjunction, a `has_bounty?` that is truthy but not `true`, a S052-listed CVE,
a short-but-≥10 quote, a double-space quote and a case-varied pricing value.

Route: adopt the 27 probes in `MutC2Counter-receipts/mutate-harness-r86.py`
(`probe_cases`, run by `main`) as a pre-freeze control
(`controls/c2-probes-r86.py` after L1 integration) and require all 27 to
distinguish before freeze. No frozen byte changes; this adds a control.

Reproduce (lane reads only; writes under `$S`):

```bash
S=/fast/scratch/hyaku/kasegi-r86/MutC2Counter
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
TMPDIR=$S python3 -B .ufo/waves/round-86/w1/MutC2Counter-receipts/mutate-harness-r86.py
# -> {"n_mutants": 39, "killed": 15, "survived": 24}; every probe distinguishes=True
python3 -B .ufo/waves/round-86/w1/MutC2Counter-receipts/compare-controls.py \
  .ufo/waves/round-86/controls/c2-controls-r86.txt "$S/out/controls-pristine.txt"
# -> verdict-mismatches=0
```

## Routed defect 2 — `R86-C2-MUT-2`: limbs E1 and E2 are jointly unsatisfiable on the frozen S122 bytes

E2 requires evidence bytes byte-identical to
`corpus/source-snapshots/round-86/S122.txt`; E1 requires the r43 gate to exit 0
with `verdict=WELL-FORMED`. The gate scans every package file (R-NOSECRET), and
S122's own bytes carry a pre-signed S3 query string:

```
X-Amz-Security-Token=[redacted-r86]
```

`SECRET_PATTERNS['credential']` matches `…Token=<16+ chars>`. A package that
satisfies every other gate rule still fails E1 on that byte sequence:
`golden-package-gate.txt` → `R-NOSECRET verdict=fail
detail=hits=1,first=evidence/S122.txt,shape=credential`, 7/8 rules pass,
`verdict=DEFECT exit=1`. The golden package (built only from the committed
snapshots) passes E0, E2, E3, E4 and E5 and fails only E1
(`golden-package-counter.txt`):

```
LIMB E0 pass heading=True url=True stray=none
LIMB E1 FAIL gate_rc=1
LIMB E2 pass bound=S122,S123
LIMB E3 pass sections=1 dup=none bad=none
LIMB E4 pass quotes=3 short=0 missing=0 s123=2
LIMB E5 pass rel=corpus/practice/pkg log=True shonen=True
E2E-RESULT fail limbs=6 rc=1
```

No artifact layout avoids this: E2 skips symlinks and requires the exact bytes;
the gate scans hardlinks, subdirectories and every regular file under 5 MiB
(oversize counts as a failure). The C2 contract as frozen therefore cannot be
satisfied by any package, and the four failing package controls in the freeze
(`donothing`, `r85-package`, `exemplar-copy`, `b3`) cannot be joined by a
passing one. This is a freeze-blocking contract defect, not a counter
loosening; the L1 (or the C2 designer) must decide between a documented gate
allowance for public-capture pre-signed URLs, a redacted S122 capture with a
new manifest digest, or an E1 clause that does not require R-NOSECRET to pass on
capture bytes. MutC2Counter does not rank those options.

Reproduce:

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
bash .ufo/waves/round-86/w1/MutC2Counter-receipts/satisfiability-probe.sh \
  /fast/scratch/hyaku/kasegi-r86/MutC2Counter/satisfy
# -> R-NOSECRET verdict=fail detail=hits=1,first=evidence/S122.txt,shape=credential
```

## Files written

- `.ufo/waves/round-86/w1/MutC2Counter.md` (this report)
- `.ufo/waves/round-86/w1/MutC2Counter-receipts/mutate-harness-r86.py`
- `.ufo/waves/round-86/w1/MutC2Counter-receipts/compare-controls.py`
- `.ufo/waves/round-86/w1/MutC2Counter-receipts/satisfiability-probe.sh`
- `.ufo/waves/round-86/w1/MutC2Counter-receipts/mutation-results.json`
- `.ufo/waves/round-86/w1/MutC2Counter-receipts/mutation-matrix.txt`
- `.ufo/waves/round-86/w1/MutC2Counter-receipts/probe-matrix.txt`
- `.ufo/waves/round-86/w1/MutC2Counter-receipts/controls-pristine.txt`
- `.ufo/waves/round-86/w1/MutC2Counter-receipts/compare-controls.txt`
- `.ufo/waves/round-86/w1/MutC2Counter-receipts/satisfiability.txt`
- `.ufo/waves/round-86/w1/MutC2Counter-receipts/golden-package-gate.txt`
- `.ufo/waves/round-86/w1/MutC2Counter-receipts/golden-package-counter.txt`
- `.ufo/waves/round-86/w1/MutC2Counter-receipts/hashes-after.txt`
- `.ufo/waves/round-86/w1/MutC2Counter-receipts/probe-*-{pristine,mutant}.txt`
  (p_e5_one_doc, p_e2_symlink_evidence, p_e1_rc0_bad, p_payer_no_handle,
  p_e4_min10_16char_quote)

No tools were installed or upgraded for this seat.
