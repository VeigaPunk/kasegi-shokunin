# ExecC2Package — round-86 C2 package candidate (candidate written; blocked on frozen instrument conflict)

Seat: ExecC2Package. Axes: depth:verifiability, coverage. Candidate:
`.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/`
(mirror of `corpus/practice/curl-ibb-h1-1997312/`; L1 copies it).
Receipts: `.ufo/waves/round-86/w1/ExecC2Package-receipts/`
(`gate-final.txt`, `e2e-pricing.txt`, `e2e-full.txt`).

## Files written

- `.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/report.md`
- `.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/claim_checklist.md`
- `.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/evidence/manifest.json`
- `.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/evidence/S120.txt` (byte copy of `corpus/source-snapshots/round-85/S120.txt`)
- `.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/evidence/S121.txt` (byte copy of round-85 S121)
- `.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/evidence/S122.txt` (byte copy of round-86 S122)
- `.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/evidence/S123.txt` (byte copy of round-86 S123)
- `.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/custodian-receipts.json`
- `.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/provenance.json`
- `.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/status.json`
- `.ufo/waves/round-86/w1/ExecC2Package-candidate/DONE`
- `.ufo/waves/round-86/w1/ExecC2Package-receipts/gate-final.txt`
- `.ufo/waves/round-86/w1/ExecC2Package-receipts/e2e-pricing.txt`
- `.ufo/waves/round-86/w1/ExecC2Package-receipts/e2e-full.txt`
- `.ufo/waves/round-86/w1/ExecC2Package.md` (this report)

No `S<digits>.txt` written at the wave-dir root (C1 M4 hygiene); the only
snapshot copies are the two in-candidate evidence artifacts the spec
allows. Scratch under `/fast/scratch/hyaku/kasegi-r86/ExecC2Package/`
will be deleted at exit.

## Gate and counter outputs (verbatim)

`python3 -B corpus/instruments/claim-package-check.py
.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312`
(rc 1; receipt `gate-final.txt`):

```
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=4,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=2,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=3,commands=5,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=fail detail=hits=1,first=evidence/S122.txt,shape=credential
package=.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312 rules=8 pass=7 fail=1 verdict=DEFECT exit=1
```

`python3 -B .ufo/waves/round-86/c2/e2e-check.py --lane <lane>
--pricing-only .../report.md` (rc 0; receipt `e2e-pricing.txt`):

```
LIMB E0 pass heading=True url=True stray=none
LIMB E3 pass sections=1 dup=none bad=none
LIMB E4 pass quotes=6 short=0 missing=0 s123=4
E2E-RESULT pass limbs=3 rc=0
```

`python3 -B .ufo/waves/round-86/c2/e2e-check.py --lane <lane>
--pkg .../curl-ibb-h1-1997312` (rc 1; receipt `e2e-full.txt`):

```
LIMB E0 pass heading=True url=True stray=none
LIMB E1 FAIL gate_rc=1
LIMB E2 pass bound=S122,S123
LIMB E3 pass sections=1 dup=none bad=none
LIMB E4 pass quotes=6 short=0 missing=0 s123=4
LIMB E5 FAIL rel=.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312 log=False shonen=False
E2E-RESULT fail limbs=6 rc=1
```

## Blocker (measured, not assumed)

The frozen C2 requirement set is unsatisfiable as specified, and the
blocker is exact:

- The spec requires evidence artifacts `S122.txt`/`S123.txt`
  byte-identical to the committed snapshots (E2 binding, `bound=S122,S123`
  above confirms this holds).
- S122's JSON carries HackerOne's presigned `profile_picture_urls` for
  the team avatar. The presigned URL contains
  `X-Amz-Security-Token=<AWS session token>` (105 bytes, twice: the
  `small` and `medium` variants). The frozen gate's `credential`
  pattern (`\b(?:api[_-]?key|secret|token|password)...`,≥16 chars)
  matches `Token=<that value>` twice. I verified the hit by running
  `claim-package-check.py`'s own `SECRET_PATTERNS` over the committed
  S122 bytes: hits `credential` at offsets 1404 and 3507; S120, S121
  and S123 are clean (0 hits each). The value is an expired presigned-
  URL session token, not a program credential; the round-85 sibling
  S119 had no such URLs, so r85 did not face this.
- Consequences: any package holding the byte-identical S122 under
  `evidence/` fails R-NOSECRET (as shown: the *only* failing rule is
  R-NOSECRET, single hit on `evidence/S122.txt`). Any redaction of the
  artifact breaks E2 (bytes no longer equal the committed S122, and the
  artifact digest no longer equals the round-86 manifest digest). A
  symlink or external reference fails both R-FILES/R-MANIFEST and E2.
  There is no file shape satisfying E1 + E2 simultaneously. E5's failure
  is the expected pre-integration one (candidate outside `corpus/`, L1
  owns LOG.md/SHONEN.md).

The candidate was built to the spec anyway, with the overlap documented
in place: `report.md` §Evidence carries the same disclosure (byte-
identical artifact kept, token identified as an expired presigned-URL
session token, R-NOSECRET reachability noted). I did **not** redact
evidence silently (would break the manifest/evidence binding and the
round-85 F-1/F-2 lessons) and did **not** waive the F-2 lesson: the
Pricing derivation separates the 2400 USD vendor record (`Bug bounty:
2400 USD`, S120) from the payer (`internet-bug-bounty`, S122+S123),
states S122's `bounty_amount` is null, and states plainly that no
captured record shows the split of the 2400 USD between reporter and
project or a disbursement receipt.

## Pricing (machine lines, exactly as frozen-counted)

The candidate's `## Pricing` section carries exactly the nine
`price-<field>` lines (one each, `sections=1 dup=none bad=none`), six
`> ` quotes (all ≥20 chars and verbatim in the `{S120,S121,S122,S123}`
pool; four occur in S123), plus the derivation list keeping the fields
separate:

```
price-program: ibb
price-payer: internet-bug-bounty
price-severity: medium
price-reward-at-disclosure: 2400 USD
price-platform-bounty-flag: true
price-original-report: 1913733
price-reward-current-policy: ended 2026-01-31
price-kev: not-listed catalogVersion 2026.10.23
price-cve: CVE-2023-28319
```

E0 subject check: first line is a `# ` heading naming 1997312 and
CVE-2023-28319; the report names `https://hackerone.com/reports/1997312`
and no other `hackerone.com/reports/<N>` except 1913733 (verified:
`stray=none`).

Package kind: retrospective practice package; no submission, not
claimable, `state: PARKED`, `claimable: false`, `do_not_submit: true`,
`No submission performed` in `report.md` and `claim_checklist.md`.
Digests: manifest sha256 `9a130c1d56d4b7c87965f47ec3e1b15ff023fc7f6a1429f9ca58594564c5f367`
(the `status.json` `manifest_sha256` binding; gate R-STATUS pass
confirms it over the file bytes); head `00a88c5a05a3b7e673eaaaa921069527f485aa8cee10c206f35ffc3fc3587550`
(custodian formula `sha256(action|input_sha256|matched_grant_id|NO_SCOPE_OBJECTION)`,
recomputed; gate R-CUSTODIAN pass confirms); pin commit
`252df0c90c066d83d229e3107811a6bc05e8feed` (the freeze commit, current
lane HEAD), remote `https://github.com/VeigaPunk/kasegi-shokunin.git`;
policy sha256 is S121's digest
(`9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102`,
matching the r85 package's policy anchor).

## Provenance model honesty

`provenance.json` agents/transitions carry `requested_model: "@m_cru"`
(dispatch alias, per the wave spec) and `resolved_model:
"commandcode/stealth/crouton-alpha"` as served (my session file records
that model; no inference from branding). `KasegiR86` (L1) entries are
`PENDING-L1` because the integration transition has not happened yet;
the sealed reviewer's entries in `status.json` are likewise `PENDING-L1`.
L1 needs to fill those (round-85 F-4 class fix: no `unrecorded`
placeholders in the landed package). There is no invented fallback.

## What the L1 needs to decide (options, all outside this seat's scope)

1. Keep the byte-identical S122 and amend the frozen gate's
   `credential` shape (W05 strict-tokenlist fix — already routed by the
   lane for this exact pattern class; evidence
   `.ufo/waves/round-85/w1/ReviewC2Package.md` R-01/R-02 counter fixes
   and the S122 token evidence above suggest the gate fix lands here).
   After the gate amendment, R-NOSECRET passes on this candidate
   unchanged; E1 then passes and the full counter is `E1–E4 pass, E5
   expected FAIL` until landing.
2. Or re-capture S122 without the presigned avatar URLs (a new
   snapshot id; E2's manifest binding would then move, and the frozen
   round-86 manifest would change).
3. Or drop the S122 artifact and cite it by path+sha256 only (E2
   fails on that shape alone; not recommended — it silently weakens
   the evidence binding).

Whichever route, the L1 must not edit the frozen `c2/e2e-check.py`,
the gate, or the committed snapshots; routes 1/2 move the instrument
or the source set, not the evidence bytes.

## Self-review vs the round-85 review (F-1..F-8)

- F-1 (fabricated verifier): this candidate names `KasegiR86` as
  verifier with receipt wording `(pending L1 verification)` in every
  redaction receipt — deliberately not asserting a scan that has not
  run, unlike the r85 candidate. L1's real scan
  (`l1/redaction-scan-r86.txt`, r85 script pattern) closes it.
- F-2 (unsupported "paid"): all `paid*` strings are either the r85
  quote "No captured record shows who paid it" (round-85 package
  wording, carried verbatim in the §Scope note), S123's own "has paid
  the bounties for us" / "over 100,000 USD paid as rewards"
  (program totals, quoted), or the derivation's "who paid …" framing.
  No per-report disbursement is asserted; the split is stated as
  unsourced.
- F-3 (custodian grant): grant string
  `kasegi-PROVINCE.md:52-documentation-only` points at
  `PROVINCE.md:52` ("this corpus is documentation only" — verified by
  reading the line); both chain steps are labelled "producer
  attestation … no independent custodian decided" in
  `decision_kind`, as the fixed r85 package does.
- F-4 (models): resolved models recorded honestly for the producer;
  L1 entries pending (above), no `unrecorded` placeholder emitted.
- F-5 (KEV date): `price-kev` line and derivation both carry
  `catalogVersion 2026.10.23` plus "captured 2026-10-26 in round 35 and
  not re-fetched for this package".
- F-6 (verbatim scope): scope fragments are raw JSON fragments from
  S122 (checked present), not paraphrases; the `structured_scope`
  ceiling is described as a ceiling, not a rating.
- F-7 (pricing label): no `price-frequency` label; the derivation
  bullets are named by the field they price,
  `price-severity` first.
- F-8 (E5): expected FAIL shown with the candidate outside `corpus/`
  (receipt `e2e-full.txt`); E5 passes only after the L1 lands the
  package at `corpus/practice/curl-ibb-h1-1997312/` and names it in
  LOG.md/SHONEN.md.

## Risks and blockers

- **Blocker: frozen instrument conflict (see above)** — E1 cannot pass
  on this candidate until the credential-shape question is decided.
  Measure: `gate-final.txt` (all rules pass except R-NOSECRET/cdential
  on S122) + `e2e-full.txt` (E2 `bound=S122,S123`, E1 FAIL, E5 expected
  FAIL). Re-runnable:
  `python3 -B corpus/instruments/claim-package-check.py
  .ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312`.
- Reviewer `ReviewC2Package` review is `PENDING-L1` (this seat is the
  producer; self-review above is not a substitute for the independent
  review).
- `status.json` `finding_count: 1` with `claimable: false` mirrors the
  r85 package shape; the gate accepts (R-STATUS pass).
- Provenance `commands` in the candidate carry the recorded exit codes
  (`1` for the gate and full-counter runs, `0` for pricing-only,
  `2` for the non-existent `build-package-r86.sh` placeholder the L1
  must supply).
- Network: none used. Live-target testing: none (PROVINCE.md).
  Tooling: none installed. `git` read-only only (remote, HEAD, log).
  No `__pycache__` (all runs `python3 -B`). No writes outside the
  wave dir and scratch. Scratch deleted at exit.

## What main agent / L1 should run after the blocker is resolved

1. `python3 -B corpus/instruments/claim-package-check.py
   .ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312`
   (expect R-NOSECRET pass after the credential-shape decision).
2. `python3 -B .ufo/waves/round-86/c2/e2e-check.py --lane <lane>
   --pkg <candidate>` (expect E1–E4 pass, E5 FAIL pre-landing).
3. L1: copy to `corpus/practice/curl-ibb-h1-1997312/`, name the path in
   LOG.md and SHONEN.md, run the redaction scan, fill the PENDING-L1
   models, re-run 1–2 (expect all limbs pass).

Yield (structured, per seat protocol):

```json
{
  "files_written": [
    ".ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/report.md",
    ".ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/claim_checklist.md",
    ".ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/evidence/manifest.json",
    ".ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/evidence/S120.txt",
    ".ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/evidence/S121.txt",
    ".ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/evidence/S122.txt",
    ".ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/evidence/S123.txt",
    ".ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/custodian-receipts.json",
    ".ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/provenance.json",
    ".ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/status.json",
    ".ufo/waves/round-86/w1/ExecC2Package-candidate/DONE",
    ".ufo/waves/round-86/w1/ExecC2Package-receipts/gate-final.txt",
    ".ufo/waves/round-86/w1/ExecC2Package-receipts/e2e-pricing.txt",
    ".ufo/waves/round-86/w1/ExecC2Package-receipts/e2e-full.txt",
    ".ufo/waves/round-86/w1/ExecC2Package.md"
  ],
  "limbs": {
    "E0": "pass heading=True url=True stray=none",
    "E1": "FAIL gate_rc=1 (sole failing rule: R-NOSECRET credential shape on byte-identical S122)",
    "E2": "pass bound=S122,S123",
    "E3": "pass sections=1 dup=none bad=none",
    "E4": "pass quotes=6 short=0 missing=0 s123=4",
    "E5": "FAIL log=False shonen=False (expected pre-landing)"
  },
  "pricing": "price-program: ibb; price-payer: internet-bug-bounty; price-severity: medium; price-reward-at-disclosure: 2400 USD; price-platform-bounty-flag: true; price-original-report: 1913733; price-reward-current-policy: ended 2026-01-31; price-kev: not-listed catalogVersion 2026.10.23; price-cve: CVE-2023-28319",
  "blocker": "Frozen conflict: S122 byte-identical evidence (E2) necessarily trips the frozen gate's credential shape (R-NOSECRET, presigned-URL session token, 2 hits). No file shape satisfies E1+E2. Candidate documents the overlap in report.md §Evidence and status.json blockers; L1 instrument/source call required.",
  "risks": [
    "E5 pending L1 landing at corpus/practice/curl-ibb-h1-1997312 + LOG.md/SHONEN.md naming",
    "status.reviewer.resolved_model PENDING-L1; provenance KasegiR86 entries PENDING-L1",
    "provenance.commands records exit 2 for the not-yet-existing build-package-r86.sh placeholder",
    "ReviewC2Package independent review not yet run"
  ],
  "no_submission": true,
  "claimable": false,
  "scratch_deleted_at_exit": true
}
```
