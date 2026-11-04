# Round 65 — signal-fail-closed derive gate (depth:verifiability) and F44, the FIRST PSIRT services catalogue (coverage)

Lane `kasegi`; attempt 1; base `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`. Frozen claims
`.ufo/waves/round-65/claims.json` (freeze `57cb8dec1cd3a688b0f8a23f5b6b434656592577`); counter erratum
`.ufo/waves/round-65/claims-erratum-1.md` (commit `a333d8ef7183a9d8bb969c6ec5c29b8db01f7481`); implementation
`1c36d724c91cdd8585219798ea7cf60bb4f24b5b`; final run `controls/final-verification-r65.txt`
(`VERIFY measurements=8 failures=0`, exit 0).

## Gate — S098 (FIRST PSIRT Services Framework v1.1)

- **URL:** https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1 (HTTP 200, no redirect on the canonical path).
- **Access date:** 2026-11-04 (`capture-source.py` `fetched_utc` 2026-11-04T19:26:27Z; independent fetches at 19:26:42Z, 19:26:49Z and 19:26:52Z produced the same snapshot).
- **Capture:** `corpus/source-snapshots/round-65/S098.txt`, 170137 bytes, 1573 lines,
  sha256 `cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2`; manifest
  `corpus/source-snapshots/round-65/manifest.json` (18 anchored quotes). Fetch 229255 raw bytes;
  HTTP `Last-Modified: Mon, 26 Jan 2026 14:43:46 GMT` (`w1/ReviewC2Base/source-check.md`); the page body
  states no publication date. The trailing-slash URL redirects to `…_framework_v1-1`, different raw bytes,
  identical normalized text.
- **Located quotes (≤25 words each, verbatim at the anchor):**
  1. "PSIRT Services Framework 1.1" (L1, 4 words).
  2. "The Services Frameworks are high level documents detailing possible services that computer incident response teams (CSIRTs)" (L219, 16 words).
  3. "when defining an initial service catalogue for new teams" (L219, 9 words).
  4. "Service Areas regroup services related to a common aspect." (L229, 9 words).
  5. "For a PSIRT the main scenario is the intake of reports affecting" (L681, 12 words).
  6. "Vulnerability reports will be investigated by the PSIRT which is therefore easy to target through a malicious submission." (L713, 18 words).
  7. "sometimes called Quality gate and/or bug bars, are used to establish minimum acceptable levels of security quality" (L853, 17 words).
  8. "Provide clear expectations to engineers and finders alike on what constitutes a vulnerability." (L857, 13 words).
  9. "that some functions be bypassed such as qualification and triage to move directly to root cause analysis" (L875, 17 words).
  10. "The test environment should be isolated, to avoid malicious activities" (L918, 10 words).
  11. "Acknowledge receipt of vulnerability report from third-party finder." (L1203, 8 words).
  12. "When a security remediation is released there should be appropriate disclosures to ensure that stakeholders" (L1231, 15 words).
- **Admit:** the whole S098 row, scoped to the service catalogue and its intake/qualification/reproduction/
  disclosure services (entry `corpus/knowledge/first-psirt-services-framework.md`, frontier F44).
- **Reject:** "established finders skip the whole process" as an attribution to L875 — the line names
  *qualification and triage* only and routes the report into root cause analysis and remediation
  development; intake, reproduction and disclosure remain. Also rejected: "the framework is a compliance
  standard" (L219 says *possible services*; no normative "shall" or certification is claimed).
- **Quarantine slice:** not re-adopted this round. The 7 kasegi rows of the campaign's absent-defect
  register were hand-checked in round 24 (`corpus/lessons/round-24.md` § Quarantine) and again in round 26
  (`wave1/quarantine-verdicts.txt`); this round only re-derived the slice and the id-collision state
  (`.ufo/waves/round-65/assimilation/id-collision-check.txt`: registry 98, staged 94, collisions 68 —
  every staged id S031–S098 is already adopted).
- **Assimilation: none.** `merge/kasegi/MERGE-REPORT.md` read; no package entry was adopted because the
  round's two claim slots are the gate and F44, and the package's remaining unadopted surface is
  doctrine/duplicate of held rows. `considerthese/2026-10-26.md` proposal 2 remains domain-task-open
  (documentation-only review is not the six-file task); proposals 1 and 3 stay landed.

## Measured result

| Axis | Before | After | Verdict / counter |
|---|---|---|---|
| depth:verifiability (lowest) | `VERIFY measurements=8 failures=3` exit 1 at base (probes-candidate, selftest, mutbat-candidate FAIL); base gate reads SIGTERM and SIGKILL upstream producers `ok` (`controls/do-nothing-signal-base-r65.txt`); final-stage signal prints `derive-exit--15` | `VERIFY measurements=8 failures=0` exit 0 at `1c36d724`; signals stale with named reasons; selftest 63/0; mutbat 4/4; ledger 35/35 | **4 → 4, delta 0 — nominal per QUALITY R58** (the citation-resolution metric is untouched). `python3 -B .ufo/waves/round-65/verify-r65.py --revision 1c36d724… --work … --final` |
| coverage | frontier `rows=43 admitted=43 closed=43 registry=97`, `entries=46 pass=46`, capture `records=78 bound=78`, expected 83 lines / 81 paths, knowledge 81; S098 absent | `rows=44 admitted=44 closed=44 problem-rows=0 registry=98`, `FRONTIER-PASS F44 ids=S098`, `entries=47 pass=47`, `records=79 bound=79`, expected 84 / 82, knowledge 82; census exit 0 | **8 → 8, delta 0** — the coverage denominator is operator-owned; the moved measure is the frontier count. `python3 corpus/instruments/frontier-recheck-count.py` |
| depth:density | 9 | 9 held; not re-measured | SKILL changes are registry facts plus one execution amendment; no density claim. |

C1's own capture of the false-green class, beyond the probe set: a producer that writes one line and
then dies by SIGKILL makes the base gate print `derived=1 ok` (a *partial* output matching the want) and
the landed gate print `derive-upstream-signal-9 stale` — `controls/partial-output-truncation-r65.txt`.
That closes the r64 routed defect 1 class with observed output instead of a code-read claim.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M65-1 | spec claims an unmeasured base behaviour | the dispatched item text said P3 (final-stage signal) "reads ok at base"; the seat's `w1/ExecSignalProbes/probes-base.txt` shows `P3 audit_exit=1 verdict=stale reason=derive-exit--15`, so the base defect for P3 is the malformed label, not a false green | the seat's base receipt, before the freeze (`probes-base.txt`, `PROBES probes=6 failures=1`) | R84: a base model stated in a seat spec is measured before dispatch; the frozen predicate now says P1/P2 are the false greens and P3's base defect is the label |
| M65-2 | counter's base reference follows the tree under test | the first final-mode run printed `VERIFY measurements=8 failures=2` (`controls/final-verification-pre-erratum-r65.txt`): `probes-base` and `mutbat-base-limb-absent` read the landed gate as the base | the final-mode run itself | erratum 1: base gate read at `claims.json` `base`; the 8/3 before-state and 8/0 after-state unchanged |
| M65-3 | pin scope leaks into a base trial | the base trial with pinned inputs counted the candidate gate hash and read a fourth, spurious failure | the same base trial receipt | erratum 1: a base trial reports `gate-pin=base-tree` and still checks the other four pins |
| M65-4 | a phrase-absence screen ignores navigation boilerplate | the first downstream sweep reported 3 capture hits for "PSIRT Services Framework"; all three are FIRST site navigation at line 201 of S001, S002 and S053 | the same screen (`controls/prefreeze-screen-r65.txt`, adjudication block) | R85: classify nav/boilerplate hits before reporting presence or absence |
| M65-5 | a probe set alone cannot reject a semantic emulator | seat MutationC1's emulator passes 6/6 of the documented probes and is rejected only by a held-out pair (`w1/MutationC1.md` §5) | the independent mutation seat | named open in the claim's residuals and in the round-66 plan; the held-out pair is the control to standardise |
| M65-6 | two independent drivers under one claim | seat ExecDriver authored its own 8-measurement driver (`w1/ExecDriver/verify-r65.py`, base `failures=6`) while the L1 froze a different one; only one counter may back C1 | the wave's results file (both artifacts exist) | the frozen driver is the claim's counter; the seat's driver is corroborating predata only, named as such in the report |
| M65-7 | an exemption can mask an unrelated error | the SIGPIPE exemption makes `cat big.txt missing.txt | head -n 1` read green while `cat missing.txt | wc -l` reads stale — the same missing operand, hidden by the pipe closing before the error is reported (`w1/CriticC1.md` § H1; `w1/CriticC1/receipts/q2-missing-input-contrast.txt`) | seat CriticC1, before any final measurement | R88: an exemption's masking path is probed and named in the claim's residuals; the r66 plan carries the single-operand restriction |
| M65-8 | a counter trusts the mutable worktree | the driver read the probe/battery/candidate from the worktree and hashed worktree bytes; `--work` was unguarded and children had no timeout | seats CriticC1 (§ D2) and SentinelScope (S-02, S-03, S-08), before the final measured run | erratum 2 (`155737d0863fc4463998f060b58d1c7510f5f96d`): inputs materialised from their adding commits, work guard, 900 s child timeout; R89 |
| M65-9 | a declared capture body range ends inside an annex | the manifest declared `body_lines [216,1450]`, which stops inside Annex 2 (L1448-1466) and excludes the Glossary (L1498-1536) that carries the capture's only maturity definition (L1510); navigation resumes at L1537 | seat EntryS098 (`w1/EntryS098/manifest-assertions-proposal.json` note; `gate.md` § Finding for the L1) | widened to [216,1536] in the manifest and the entry header; R90 |
| M65-10 | the L1's own appended entry sentence overreached its source | the maturity bullet said "only maturity statement" and "no assessment method"; L675 states a measurement method (availability and efficiency of the services prescribed in a service area), so two negatives were false while the cited grep only supported "no maturity levels" | seat EntryS098's post-append audit (`w1/EntryS098.md`; graded form `w1/EntryS098/claim-table.md` C-24–C-26; the bullet was corrected to "only maturity definition" and the L675 sentence quoted) | R91: an entry edited after its claim table is re-audited sentence by sentence before the commit; the overreaching negatives were the same failure mode as M65-9 on the claim axis |

## Carry-in — round-64 routed defects

1. **Truncated-input arm unreceipted:** the r64 handoff's `could-not-evaluate exit2` arm does not exist in
   the landed r64 bytes (`grep -c 'could-not' corpus/instruments/figure-audit.py` = 0 at `a283189`); the
   claim is withdrawn as code-read only, and the class it named is now fail-closed with a receipt
   (`controls/partial-output-truncation-r65.txt`). Closed.
2. **Gate wording pointer:** appended to `corpus/lessons/round-64.md` § Gate (append-only). Closed.
3. **Lesson shape:** this round's Mistakes rows are all under `## Mistakes`. Closed.
4. **Unreceipted route claim:** dropped. No seat route is asserted in this lesson; the wave's captured
   routes are not re-derivable from the artifacts, so the report makes no route claim.
5. **Hygiene:** the four inherited untracked `w1.ready.dispatched` markers (r57–r60) were committed in
   `462ed24a7f64744a474101842e1c7e89a71198e4`. Closed.
6. **Not lane debt** (orchestrator restart accounting): unchanged; no action.

## Wave record

One v1 wave, 12 seats (`w1-spec.json`, validated under `ufo-wave-policy.json`, band 8–16), L1 holds the
planner seat. Roles: 4 executor, 1 scribe, 1 scout, 1 connector, 2 reviewer, 1 critic, 1 mutation-tester,
1 sentinel = attack 5/12 (42 %). Verdicts and the dead-seat record are appended below when the wave
settles.

## Residuals and open

- Signal detection covers direct child stages only: grandchildren, shell wrappers, PATH-shadowed binaries
  and exit-0 wrappers that print partial output stay out of scope (named, not claimed).
- SIGPIPE on a non-final stage stays benign by documented rule and is pinned by its own selftest case.
- The gate is not pipefail, not a sandbox and not an authenticity check.
- Lost-base source restoration and the operator-owned R67/R69 decisions remain open; the metric gap stays
  22 of 82 rechecks gated on a lost base (`recheck-audit.py`).
- F44's cardinalities (6/28/84) are counted headings of this page; the capture is a fetched instance, not
  an edition statement.
