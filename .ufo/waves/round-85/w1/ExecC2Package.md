# ExecC2Package — C2 end-to-end priced claim package candidate (HackerOne 1913733 / CVE-2023-28319)

Seat: ExecC2Package. Candidate root: `.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733/`
(L1 copies it to `corpus/practice/curl-h1-1913733/` and re-runs ExecC2Package-build.sh there.)
Everything below is relative to the lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin/`.
Gate runs and receipts: `.ufo/waves/round-85/w1/ExecC2Package-receipts/`.
No fleet-repo, other-lane, or `.ufo/state` write was attempted; `corpus/`, LOG.md and SHONEN.md were left untouched for the L1.

## Files written

- `.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733/report.md`
- `.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733/claim_checklist.md`
- `.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733/evidence/manifest.json`
- `.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733/evidence/S119.txt` (byte copy of committed S119)
- `.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733/evidence/S120.txt` (byte copy of committed S120)
- `.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733/evidence/S121.txt` (byte copy of committed S121)
- `.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733/custodian-receipts.json`
- `.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733/provenance.json`
- `.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733/status.json`
- `.ufo/waves/round-85/w1/ExecC2Package.md` (this file)
- `.ufo/waves/round-85/w1/ExecC2Package-build.sh` (deterministic rebuild script; verified below)
- `.ufo/waves/round-85/w1/ExecC2Package-receipts/gate-final.txt`
- `.ufo/waves/round-85/w1/ExecC2Package-receipts/e2e-full.txt`
- `.ufo/waves/round-85/w1/ExecC2Package-receipts/e2e-pricing.txt`

## Behavior

- Candidate is a six-file claim package in the contract's shape, built only from committed snapshots S119/S120/S121 (round-85) read from `corpus/source-snapshots/`.
- Report prices the finding from those records (price-program curl, price-severity medium, price-reward-at-disclosure 2400 USD, price-platform-bounty-flag false, price-reward-current-policy none, price-cvss not-set-by-vendor, price-kev not-listed with catalogVersion 2026.10.23 from S052 line 3, price-cve CVE-2023-28319) plus four verbatim `> ` quotes and a short derivation disambiguating has_bounty? false vs the recorded 2400 USD payment.
- Evidence manifest lists three positive artifacts (S119/S120/S121 byte copies, digests equal the round-85 manifest records) with one same-digest redaction receipt per artifact (producer ExecC2Package, verifier KasegiR85).
- Custodian chain is exactly 2 decisions (capture-sources, build-practice-package) with matched_grant_id `kasegi-PROVINCE-documentation-only`, scope_signal `NO_SCOPE_OBJECTION`; head equals final decision digest equals `expected_head_sha256`.
- Status is PARKED, claimable false, finding_count 1, blocker `retrospective practice package: already disclosed and fixed upstream (CVE-2023-28319, curl 8.1.0); duplicate of HackerOne 1913733`; claim_review mirrors the exemplar (hard_gates, subchecks, reviewer identity `ReviewC2Package`, requested `@m_zfl`, resolved `PENDING-L1`, fallback false).
- Provenance pins remote `https://github.com/VeigaPunk/kasegi-shokunin.git` (actual `git remote get-url origin`) and commit `4a2d34f203519a87078f21a896dc8679137ff675`, policy_sha256 is the S121 digest, external_effects_performed is `[]`, resolved_model is `unrecorded` (allowed fallback; seat does not know its runtime model id to cite it honestly).
- Reproduction section is an isolated-lab outline only: no exploit payload, no live target was touched.

## Exact retained outputs (verbatim)

### (a) `python3 -B corpus/instruments/claim-package-check.py candidate`

```
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=3,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=3,receipts=3,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=2,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=6,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=3,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733 rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
gate exit=0
```

### (b) `python3 -B .ufo/waves/round-85/c2/e2e-check.py --lane <lane> --pkg candidate` (E5 FAIL is expected and owned by the L1 — candidate is outside corpus/practice and LOG.md/SHONEN.md are L1-owned)

```
LIMB E1 pass gate_rc=0
LIMB E2 pass bound=S119,S120
LIMB E3 pass section=True bad=none
LIMB E4 pass quotes=4 missing=0
LIMB E5 FAIL rel=.ufo/waves/round-85/w1/ExecC2Package-candidate/curl-h1-1913733 log=False shonen=False
E2E-RESULT fail limbs=5 rc=1
e2e exit=1
```

### (c) `python3 -B .ufo/waves/round-85/c2/e2e-check.py --lane <lane> --pricing-only candidate/report.md`

```
LIMB E3 pass section=True bad=none
LIMB E4 pass quotes=4 missing=0
E2E-RESULT pass limbs=2 rc=0
pricing exit=0
```

### (d) Build-script verification (`./ExecC2Package-build.sh $S/pkg` then full counter)

```
rebuilt 9e4fb52e7e7572482fa29fc268dddbf7e249dd94c6850d2e383241ae14bc6105 65d6b230ad58e86517b1b0faddd800d6bcb111ed05e21e22752246f4b0913690 9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102 5d306fb5ae79460d24223218e5d705641ff88cfafc3869ffd3f48c74e39e2bb2 89f0f18bc778faf53296327c88e8ae51b68b72dc405e0ab4d50e6b5d54cbe1cf
rebuilt at /fast/scratch/hyaku/kasegi-r85/ExecC2Package-verify/pkg
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=3,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=3,receipts=3,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=2,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=6,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=3,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=/fast/scratch/hyaku/kasegi-r85/ExecC2Package-verify/pkg rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
LIMB E1 pass gate_rc=0
LIMB E2 pass bound=S119,S120
LIMB E3 pass section=True bad=none
LIMB E4 pass quotes=4 missing=0
LIMB E5 FAIL rel=../../../../../fast/scratch/hyaku/kasegi-r85/ExecC2Package-verify/pkg log=False shonen=False
E2E-RESULT fail limbs=5 rc=1
e2e-ver exit=1
```
(`ExecC2Package-build.sh` takes an output root argument; rebuilding there reproduced identical digests 9e4f…/65d6…/9e34…/5d30…/89f0…. The L1 re-runs it at `corpus/practice/curl-h1-1913733/` and recomputes digests there; provenance command paths are path-agnostic, so digests are identical across locations.)

### (e) Digest table (final bytes, measured before yielding)

- `claim_checklist.md`  819732d0facf4a6e8dcf3f708230b2403502f57f7f3ba907e2ec2e0921684d7b
- `custodian-receipts.json`  6075c74aac1217b5f8195b16b968dd9e946d413c9f1da71b3d317f4708fd66b5
- `evidence/S119.txt`  9e4fb52e7e7572482fa29fc268dddbf7e249dd94c6850d2e383241ae14bc6105
- `evidence/S120.txt`  65d6b230ad58e86517b1b0faddd800d6bcb111ed05e21e22752246f4b0913690
- `evidence/S121.txt`  9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102
- `evidence/manifest.json`  89f0f18bc778faf53296327c88e8ae51b68b72dc405e0ab4d50e6b5d54cbe1cf
- `provenance.json`  bdae262189fba0a773e09600f65a809877794dee5759c91f58107d78135fe5f7
- `report.md`  5ef6fd7a11882bbe3251dbd5fb253ea7d2b6cfc9cf5b1affb287f9fa773b976d
- `status.json`  00f61d21a561d5069d0c307df66c1060cf4b6269db942e239a8e270859bc19cf

- status manifest_sha256  89f0f18bc778faf53296327c88e8ae51b68b72dc405e0ab4d50e6b5d54cbe1cf  (== sha256(evidence/manifest.json) == 89f0f18bc778faf53296327c88e8ae51b68b72dc405e0ab4d50e6b5d54cbe1cf)
- custodian head / manifest expected_head_sha256  5d306fb5ae79460d24223218e5d705641ff88cfafc3869ffd3f48c74e39e2bb2  (== final decision digest; head == expected_head: True)
- provenance policy_sha256 (= evidence/S121.txt)  9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102  (== S121 9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102)
- report 64-hex tokens (all in manifest): 65d6b230ad58e86517b1b0faddd800d6bcb111ed05e21e22752246f4b0913690, 9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102, 9e4fb52e7e7572482fa29fc268dddbf7e249dd94c6850d2e383241ae14bc6105
- KEV: `CVE-2023-28319` occurs 0 times in `corpus/source-snapshots/round-35/S052.txt` (catalogVersion `2026.10.23`, line 3)
- Custodian math re-verified: decision_sha256 = sha256(action|input_sha256|matched_grant_id|NO_SCOPE_OBJECTION) holds for both chain entries; second entry's input is the first entry's decision digest.

## Risks and blockers

- E5 cannot pass until the L1 copies the package into the lane tree and names its lane-relative path in LOG.md and SHONEN.md; this seat deliberately did not touch those files.
- reviewer resolved_model is PENDING-L1 by instruction; claimable stays false with a named blocker, so the gate does not require reviewer approval.
- provenance resolved_model is `unrecorded` because this seat does not know its own runtime model id to cite it honestly; the spec allows this fallback. The L1 can overwrite it.
- Mirror roots `~/Projects/bounties` and `~/Projects/the-bounty-hunter` are absent on this host per spec, so no cross-check against them was possible (spec says so).
- No network access was needed or used; no live target, portal, or vendor contact.
- No subagent was dispatched (seat is a leaf; a single-package build needed no labrat probe).
