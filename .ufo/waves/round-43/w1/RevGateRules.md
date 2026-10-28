# RevGateRules — rule-by-rule review of the claim-package gate (round 43, C2)

Seat: RevGateRules (reviewer, leaf). Round 43, base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Reviewed 2026-10-28 16:38–16:54 UTC. Host python3 3.14.8, uid 1000 (non-root).
Contract under review: `corpus/knowledge/claim-package-contract.md` (authoritative) with
`corpus/knowledge/claim-gates.md` as the byte-level derivation.

## 0. Artefacts reviewed (pinned by sha256; the seats were still editing)

| file (in `.ufo/waves/round-43/w1/`) | sha256 at review | note |
|---|---|---|
| `ExecGateCore.claim-package-check.py` | `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` | self-contained gate; **does not import the three modules** |
| `ExecGateManifest.rules.py` | `e8131998f246684a9876d4a18769e544379a70146bf72f817bf929811b18a81b` | stable across my pass |
| `ExecGateChain.rules.py` | `6f0f1c42082652cdfd8ea6172ee96ab2e8450aca2fc20397e051adffa102c542` | stable |
| `ExecGateProvReport.rules.py` | `97003db342b713d20a159690e289c1b3aaeb7091a9a07531a44a6d1d80dc3aa5` | **changed mid-review** (was `3085969c…`, below) |
| `ExecGateCore.rules.txt` | `59875e76d88eb63b379bd18e4508fc2e70ea38bda4cdc0ade9b4bf1a63073da1` | the rule table the core claims |
| `ExecGateSelftest.selftest.py` | `04951ca0e72050725fc01a16ba1e42d7a52bd29bb0ae653b164a39ed39b57b17` | integration-tested, §3 |
| `ExecExemplarPackage.*`, `ExecGateFixtures.defect-*` | n/a (assembled in scratch) | rerun against the gate, §1 |

`ExecGateProvReport.rules.py` revision drift during the review, verified by replaying the two
byte sets over identical packages (`oldprov.py`):

```
== old bytes 3085969c:
extra-symlink-outside   pass files=8 hits=0 skipped=0 classes=none
nosecret-unreadable     pass files=8 hits=0 skipped=1 classes=none
nosecret-oversize       pass files=8 hits=0 skipped=1 classes=none
== current bytes 97003db3:
extra-symlink-outside   fail files=8 hits=0 symlinks=1 ... fail=symlink-entry
nosecret-unreadable     fail ... fail=unreadable-file
nosecret-oversize       fail ... fail=oversize-file
```

Two revisions landed while I reviewed. `ExecGateProvReport.rules.py` fixed its own R-NOSECRET
fail-open (above). The core was then revised (`bdb50a82…` → `8b6f8493…`, an internal rename to
`_GateFail`/`_gate_token`) and the selftest with it (`bc34fff5…` → `04951ca0…`); I re-ran the
whole matrix against the revised bytes: the 48 decisive variants produced byte-identical
verdicts (`diff` of the two transcripts is empty), the 92-variant module/core diff is unchanged
(73/19/9), the exemplar is still 8/8, the nine fixtures still fail one rule each, and
`--selftest` still prints `selftest cases=10 failures=0`. Every verdict below is pinned to the
hashes above, i.e. the current bytes. The gate's remaining holes are in §6.

Method (scratch only, `S=/fast/scratch/hyaku/kasegi-r43/RevGateRules`, disk guard checked):
`matrix.py` builds a full six-file package that BOTH implementations accept (`base`), applies
exactly ONE delta per variant, and runs the gate; `drive.py` runs the three modules over the same
directory; `dual.py` runs the gate and the three modules over the SAME bytes and diffs.
92 single-delta variants (plus the shared base) × 2 implementations. Nothing outside `S`
was written.

## 1. Accept case — independently reproduced, not taken from a transcript

Assembled the exemplar from the delivered parts (`report.md`, `claim_checklist.md`,
`custodian-receipts.json`, `provenance.json`, `status.json`, `evidence/manifest.json`,
four evidence artifacts) and ran the gate:

```
$ python3 .ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py ex
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=ex rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
exit=0
```

The nine shipped defect fixtures fail on exactly their own rule and no other, one failing rule
each (`python3 <gate> <fixture>`): defect-1 `missing=1,bad=0` (R-FILES);
defect-2 `artifacts=4,digest-bad=1` (R-MANIFEST); defect-3 `positive=0` (R-MANIFEST);
defect-4 `escape=1` (R-MANIFEST); defect-5 `redactions=empty` (R-REDACT);
defect-6 `chain=3,head=mismatch` (R-CUSTODIAN); defect-7 `reviewer=not-distinct` (R-STATUS);
defect-8 `marker=absent` (R-REPORT); defect-9 `hits=1,…,shape=credential` (R-NOSECRET).
All nine `verdict=DEFECT exit=1`.

## 2. CLI contract of the core (measured)

```
no-args exit=2              missing-dir exit=2        extra-arg exit=2
good exit=0                 selftest-absent exit=2    -W error::DeprecationWarning exit=0
$ gate /nonexistent-pkg            -> package=/nonexistent-pkg verdict=ERROR exit=2
$ gate /nonexistent-pkg --json     -> {"exit": 2, "rules": null, "verdict": "ERROR", ...}
$ gate <file>                      -> verdict=ERROR exit=2
```

Eight `RULE` lines in the frozen order, comma-separated `detail=` tokens, summary
`… verdict=… exit=N`, text mode identical to `--json` field content. Containment held on every
probe: `../` artifact (`escape=1`), absolute artifact (`escape=1`), symlink artifact
(`escape=1`), `evidence/` as a symlink (`R-MANIFEST detail=symlink`, overall DEFECT). A symlinked
package root is resolved via `realpath` and accepted — a legitimate reading of "under the package
dir it is given".

## 3. `--selftest` integration (tested end-to-end in scratch)

Landing names matter. `selftest_dispatch` uses `globals()['run_selftest']` or the companion
`<gate dir>/claim-package-selftest.py` (`$CLAIM_PACKAGE_SELFTEST` overrides). With the companion
named exactly that and `fixtures/claim-package/` beside the gate:

```
$ TMPDIR=$S/st/tmp python3 st/claim-package-check.py --selftest
selftest case=1 class=defect fixture=defect-1-missing-file expected=R-FILES observed=R-FILES verdict=pass
… nine defect cases, each expected==observed …
selftest case=10 class=degenerate fixture=always-pass expected=reject observed=rejected-9/9 verdict=pass
selftest cases=10 failures=0
exit=0
```

Mis-named companion (`claim-package-check.selftest.py`) or no companion:
`selftest module=… verdict=missing exit=2`. So `ExecGateSelftest.selftest.py` MUST land as
`corpus/instruments/claim-package-selftest.py` or the C2 selftest counting command cannot pass.
Verified that a stub companion's exit code propagates (0→0, 1→1).

## 4. Rule by rule

Contract quotes are from `claim-package-contract.md`; line numbers are from `claim-gates.md`.

### R-FILES
- Accepts: six contract files present, regular, non-symlink, non-empty; the four JSON files parse
  to objects (`base` → `files=6,missing=0,bad=0`).
- Must reject: a missing contract file (contract table lists exactly six); a symlinked or
  non-regular file is not a file the package owns (claim-gates blanket symlink ban, L104-105);
  unparsable JSON must fail closed (R30).
- Rejects (run): `files-missing-status` → `missing=1,bad=0`; `files-report-is-dir` →
  `missing=0,bad=1`; `files-empty` (six 0-byte files) → `missing=0,bad=6`; each of the four JSON
  files chmod 000 → `bad=1` (a chmod-000 `report.md`/`claim_checklist.md` stays a regular
  non-empty file here and is caught downstream by R-NOSECRET).
- Fail-closed: yes — a truncated/invalid-UTF-8 manifest is `bad=1`, not a pass.
- Module divergence: `ExecGateManifest.rules.py:184 rule_files` checks existence only; it passes
  six 0-byte files (`files-empty`: module R-FILES=pass) and never parses JSON.
- Contract key unread: the file's *content* — see §7, F3.

### R-MANIFEST
- Accepts: `schema_version == evidence-manifest/v1`; numeric `sequence`; 64-hex
  `expected_head_sha256`; non-empty `artifacts[]` with unique relative `path`, 64-hex `sha256`
  RECOMPUTED from `evidence/<path>` bytes, `polarity ∈ {positive,negative}`, ≥1 positive;
  confinement.
- Must reject (contract: "Per-artifact sha256 … ≥1 positive … paths are relative to `evidence/`,
  must stay inside the package, no symlink traversal"; claim-gates L39 `sequence` number).
- Rejects (run, core): `man-schema` → `schema=evidence-manifest/v2`;
  `man-digest-wrong` → `digest-bad=1`; **`man-digest-trusted`** (bytes changed after the digest was
  written) → `digest-bad=1`, i.e. the digest is recomputed, never trusted; `man-negative-only` →
  `positive=0`; `man-polarity-bad` → `polarity-bad=1`; `man-path-dotdot|escape|absolute|symlink-inside`
  → `escape=1` each; `man-artifacts-empty` → `artifacts=none`; `man-head-absent|head-not-hex` →
  `expected_head=bad`; `man-duplicate-path` → `digest-bad=1` (plus R-REDACT
  `missing=2`); `man-truncated|invalid-utf8` → `parse:evidence_manifest.json`;
  `man-empty-object` → `schema=absent`; `man-list` → `manifest:not-object`.
- Fail-closed: yes.
- Extra-contract requirement: `sequence` is enforced (`man-no-sequence` → `sequence=not-number`)
  although the contract's manifest row never mentions it (it is claim-gates L39) and
  `rules.txt` does not mark it `[convention]`, unlike the conventions it does mark. Same bytes:
  modules pass, core fails — a contract-conformant manifest is rejected by the landing gate.

### R-REDACT
- Accepts: non-empty `redactions[]`, exactly one receipt per artifact, receipt
  `artifact_sha256 == scanned_artifact_sha256 == artifact.sha256`, non-empty distinct
  producer/verifier.
- Must reject: `redactions: []` ("never claim-ready"), digest mismatch, missing/same identity,
  a receipt bound to no artifact.
- Rejects (run): `red-empty|red-missing-key|red-not-list` → `redactions=empty`;
  `red-producer-eq-verifier` and `red-empty-verifier` → `identity=1`;
  `red-scanned-mismatch` → `digest-mismatch=1`; `red-digest-mismatch` and `red-uncovered` →
  `missing=1`; `red-unbound` → `unbound=1`; `red-two-for-one` (two receipts for one artifact) →
  `unbound=1` — the core enforces the contract's "one … per artifact", the module accepts ≥1.
- Fail-closed: yes (truncated manifest → `parse:…`).

### R-CUSTODIAN
- Accepts: non-empty `chain` (or `decisions`); per decision non-empty `action`, 64-hex
  `input_sha256`/`decision_sha256`, non-empty `matched_grant_id`, `scope_signal` exactly
  `NO_SCOPE_OBJECTION`; `head_sha256 == last decision == manifest.expected_head_sha256`.
- Must reject: empty chain; any other signal (`HARD_STOP` included); empty grant; broken head.
- Rejects (run): `cus-empty-chain|chain-string|empty-object` → `chain=empty`;
  `cus-scope-signal` → `signal-bad=1`; `cus-grant-empty` → `grant-miss=1`;
  `cus-head-mismatch` → `head=mismatch`; `cus-manifest-head-mismatch` →
  `head-manifest=mismatch`; `cus-no-input-sha` → `digest-bad=2`; `cus-truncated` →
  `parse:custodian-receipts.json`.
- Fail-closed: yes.
- Module defect: `ExecGateChain.rules.py:191` requires non-empty *strings* only. A chain whose
  `input_sha256`/`decision_sha256` are `"zz"`/`"not-a-digest"` (and whose head/manifest head are
  the same non-digest string) passes the module 8/8 — the "three-way digest binding" degenerates
  to string equality (`cus-decision-not-hex`, `cus-input-sha-junk`: modules WELL-FORMED, core
  DEFECT). claim-gates L74-93 requires `/^[a-f0-9]{64}$/i`.

### R-PROVENANCE
- Accepts: `agents[]` each with non-empty `transition` + `requested_model` + `resolved_model`;
  `commands[]` with `command` and integer `exit_code`; `pin.remote` + 7–64-hex `pin.commit`;
  64-hex `policy_sha256`; `external_effects_performed == []`; `secrets_attestation` as a
  non-empty string or `{"no_secrets": true}`.
- Must reject (contract row): missing models, command without exit code, missing pin, empty
  effects list violated, absent attestation.
- Rejects (run): `pro-external-effects` → `external_effects_performed=not-empty`;
  `pro-no-pin` → `pin=absent`; `pro-pin-no-commit` → `pin=commit`; `pro-no-exit-code` →
  `commands=1,commands-bad=2`; `pro-no-policy` → `policy_sha256=bad`;
  `pro-no-secrets-attestation` → `secrets_attestation=absent`; `pro-no-agents` → `agents=empty`;
  `pro-no-transition-field` → `agents=1,agents-bad=1`; `pro-truncated|invalid-utf8` →
  `parse:provenance.json`; `pro-empty-object` → `agents=empty`.
- Fail-closed: yes.
- Coverage: this rule reads every key its contract row states (as do R-MANIFEST and
  R-CUSTODIAN; R-STATUS and R-REPORT are the two with stated-but-unread contract keys). Key NAMES are
  lane conventions (`transition`, `command`, `exit_code`, `secrets_attestation`) — `claim-gates`
  uses `cmd`/`exit`; the module accepts those aliases, the core does not. Those conventions are
  not marked `[convention]` in `rules.txt` except the attestation object shape.

### R-STATUS
- Accepts: 64-hex `manifest_sha256` equal to sha256 of the current manifest bytes; `claim_review`
  with `hard_gates`, `subchecks` and a `reviewer` (identity, requested/resolved model, boolean
  fallback, identity distinct from every manifest producer/verifier); `claimable true` ⇒ all four
  named hard gates and both subchecks exactly `PASS` and `finding_count` int ≥1;
  `claimable false` ⇒ a named blocker.
- Must reject: the 12 mutations below.
- Rejects (run): `sta-manifest-sha` → `manifest_sha256=mismatch`;
  `sta-reviewer-is-producer` → `reviewer=not-distinct`; `sta-reviewer-empty` →
  `reviewer:identity`; `sta-no-requested-model` → `reviewer:requested_model`;
  `sta-fallback-not-bool` → `reviewer:fallback`; `sta-hard-gates-absent|sta-empty-object` →
  `missing:…`; **`sta-partial-hard-gates`** (only `written_scope` and `no_secrets` present) →
  `gates-missing=4` — the four contract gate names are enforced, which the module does not do
  (same bytes: module passes); `sta-claimable-true-gate-fail` → `gates-not-pass=1`;
  `sta-claimable-true-finding-zero` → `finding_count=bad`; `sta-claimable-false-no-blocker` →
  `blocker=none`; `sta-truncated` → `parse:status.json`.
- Fail-closed: yes.
- **Contract keys this rule does not read** (all proven accepted, `exit=0`):
  `state` (`"SUBMITTED"` passes), `do_not_submit: true` + `no_submission_performed: false` pass
  alongside `claimable: true`, `claim_review.outcome`/`claim_ready` absent and pass,
  `claimability_blocker`/`resume_condition` absent and pass.
- `rules.txt` states these are out of scope because "the lost tool never machine-checked
  `status.state`". `claim-gates.md` L118 says the opposite: "`state === 'DONE'` (anything else
  fails, incl. SUBMITTED)". The scope note understates the reference tool (F6).

### R-REPORT
- Accepts: `/scope\s+excerpt/i`, the exact literal `No submission performed`, ≥1 `https://` URL,
  and every whole 64-hex token bound to an `artifacts[].sha256`.
- Must reject: missing excerpt heading, missing marker, no URL, a cited digest absent from the
  manifest.
- Rejects (run): `rep-no-marker` → `marker=absent`; `rep-no-scope-excerpt` →
  `scope-excerpt=absent`; `rep-no-url` → `url=absent`; `rep-cites-foreign-digest` →
  `cited=2,unbound=1`; `rep-empty` → `scope-excerpt=absent`; `rep-truncated-mid-marker` →
  `marker=absent`.
- Fail-closed: yes (`unreadable` for a chmod-000 report; empty report fails).
- **Accepted defects**: `rep-no-citation` (no content sha256 anywhere) → `cited=0,unbound=0`,
  `exit=0`, although the contract states the excerpt carries "content sha256". `rep-bare-prose`
  (URL + heading + marker + one digest; no title, program name, vuln class, repro, impact,
  affected asset, fix, disclosure timeline) → `exit=0`.
- Module divergence: the module requires ≥1 citation (`rep-no-citation` fails there) and accepts a
  citation that is only `expected_head_sha256` (core rejects: "every artifact sha256 it cites").

### R-NOSECRET
- Accepts: package text with no secret shape.
- Must reject: private-key header, `op://`, bearer/authorization value, labelled credential,
  session cookie, per `rules.txt`; plus a symlink entry, a file >5 MiB and any unreadable file.
- Rejects (run, core): `sec-private-key|op-ref|bearer|hex-token` → `hits=1,…,shape=…`;
  `extra-symlink-outside` and `extra-dir-symlink-outside` → `symlinks=1`;
  `nosecret-unreadable` → `unreadable:leak.txt`; `nosecret-oversize` → `oversize=1`.
- Fail-closed: **yes for files, no for directories.** `nosecret-locked-dir` — a `chmod 000`
  subdirectory containing an `-----BEGIN OPENSSH PRIVATE KEY-----` file — is reported
  `files-scanned=ok,symlinks=0,oversize=0,hits=0`, package `WELL-FORMED exit=0`. Cause:
  `ExecGateCore.claim-package-check.py:656` `os.walk(pkg.root, followlinks=False)` with the
  default `onerror=None` silently drops an unreadable subtree; the `except OSError: continue` on
  `lstat` at :666 has the same effect for an entry it cannot stat.
- **Accepted defect on a declared class**: `sec-cookie` (`"Cookie: sessionid=<32 hex>"` in
  provenance) → `exit=0`. The core pattern (line 141) is
  `\bsession[_-]?cookie\b` and needs a key literally named `session_cookie`; a standard
  `Cookie: sessionid=…` header is not matched. The sibling module (current bytes) DOES catch it
  (`hits=1,…,shape=session-cookie`) — the core is weaker than its own module here.

## 5. Fails-closed (R30) matrix — truncated/corrupt input per rule

Builder variants: each JSON truncated to half its bytes, one JSON replaced with invalid UTF-8,
plus six `chmod 000` required files. All runs on the core.

| corrupt input | R-FILES | R-MANIFEST | R-REDACT | R-CUSTODIAN | R-PROVENANCE | R-STATUS | R-REPORT | R-NOSECRET |
|---|---|---|---|---|---|---|---|---|
| manifest truncated | fail `bad=1` | fail `parse:…` | fail | fail | pass (does not read it) | fail | fail | pass |
| manifest invalid UTF-8 | fail `bad=1` | fail `parse:…` | fail | fail | pass | fail | fail | pass |
| custodian truncated | fail `bad=1` | pass | pass | fail `parse:…` | pass | pass | pass | pass |
| status truncated | fail `bad=1` | pass | pass | pass | pass | fail `parse:…` | pass | pass |
| provenance truncated | fail `bad=1` | pass | pass | pass | fail `parse:…` | pass | pass | pass |
| report chmod 000 | pass | pass | pass | pass | pass | pass | fail `unreadable` | fail |
| claim_checklist chmod 000 | pass | pass | pass | pass | pass | pass | pass | fail `unreadable:…` |

`chmod 000` on each JSON file in turn: R-FILES fails `bad=1`; the owning rule fails `unreadable`;
R-REDACT/R-CUSTODIAN/R-STATUS also fail when the unreadable file is the manifest (they read it);
R-REPORT fails `unreadable` only when the unreadable file is the manifest (it reads no other
JSON file);
R-NOSECRET fails `unreadable:<rel>` in every case, which is what catches the file no other rule
reads (`claim_checklist.md`).

No truncated, corrupt, non-UTF-8 or unreadable **file** yields a pass from the rule that reads it.
The single R30 hole is the unreadable **directory** (§4 R-NOSECRET, F1).

## 6. Findings by severity

**F1 (High) — R-NOSECRET cannot see inside an unreadable directory.** A package carrying
`locked/leak.txt` = private key, with `locked/` mode 000, is `WELL-FORMED exit=0`
(`nosecret-locked-dir`). `ExecGateCore.claim-package-check.py:656` walks with `onerror=None`.
Fix shape: pass an `onerror` that raises `_GateFail`, or pre-`scandir` with an explicit
error check.
Both implementations share the hole, so no shipped fixture covers it.

**F2 (High) — `claimable: true` is accepted alongside the contract's own no-submission guards.**
`sta-state-submitted` (`state:"SUBMITTED"`) and `sta-do-not-submit`
(`do_not_submit:true`, `no_submission_performed:false`, `claimable:true`, all six gates PASS) are
both `WELL-FORMED exit=0`. The contract's status semantics define the state enum and its guards;
claim-gates makes `state === 'DONE'` (L118, "anything else fails, incl. SUBMITTED") and
`do_not_submit` (status-gate not-claimable triggers) hard failures. The gate's `claimable` verdict is the bit
a claim-ready consumer would read, so this is the gate's own subject matter, not prose.

**F3 (Med) — `claim_checklist.md` content is never read.** `chk-no-marker` (no `OPERATOR-GATED`)
is `WELL-FORMED exit=0`; the only occurrence of the filename in the gate is the `SIX_FILES`
tuple. The contract's checklist row states the marker and "names residual gates";
claim-gates L32 makes it a marker gate. The shipped exemplar carries `OPERATOR-GATED`, so the
gate's accept case demonstrates content it never requires.

**F4 (Med) — R-REPORT does not require the excerpt's content sha256.** `rep-no-citation`
(`cited=0`) is `WELL-FORMED`; the contract's report row states "Scope excerpt = verbatim policy
text + URL + observed_at + content sha256". `rep-bare-prose` shows that everything else the row
states (title, program, vuln class, repro, impact, affected asset, fix, disclosure timeline,
observed_at) is also unread — deliberately (prose is not a gate), but then the row's one machine
checkable element should be required, as the sibling module does.

**F5 (Med) — the declared "session cookie" class is not actually matched by the gate.**
`sec-cookie` (`Cookie: sessionid=<32 hex>`) is `WELL-FORMED`; the module matches it. The gate's
pattern needs a literal `session_cookie` key. A receipt that claims "session cookies" are scanned
is over-broad as measured.

**F6 (Med) — `rules.txt` misstates the reference tool's scope.** It asserts `status.state` was
"never machine-checked by the lost tool"; `claim-gates.md` L118 records
`state === 'DONE'` as a gate that fails on SUBMITTED. The declared scope therefore omits a check
both source documents require, and F2's acceptance of `SUBMITTED` follows from it.

**F7 (Low) — `sequence` is an unmarked extra requirement.** `man-no-sequence` fails
`sequence=not-number` on the core while the modules pass the same bytes; the authoritative
contract's manifest row does not list `sequence`. Either mark it `[convention]` (it is
claim-gates L39) or drop it; as shipped, a contract-conformant manifest is rejected.

**F8 (Med, integration) — the three rule modules are a second implementation with
verdict-flipping divergences.** 92 single-delta variants run through both implementations
(plus the base, which both accept): 73 agree; 19 differ in at least one rule; 9 differ in the
bottom line (7 packages the modules pass and the core rejects, 2 the core
passes and the modules reject).

```
cus-decision-not-hex   modules WELL-FORMED  core DEFECT   (R-MANIFEST, R-CUSTODIAN)
cus-input-sha-junk     modules WELL-FORMED  core DEFECT   (R-MANIFEST, R-CUSTODIAN)
man-duplicate-path     modules WELL-FORMED  core DEFECT   (R-MANIFEST, R-REDACT)
man-head-not-hex       modules WELL-FORMED  core DEFECT   (R-MANIFEST, R-CUSTODIAN)
red-two-for-one        modules WELL-FORMED  core DEFECT   (R-REDACT)
rep-cites-head-digest  modules WELL-FORMED  core DEFECT   (R-REPORT)
sta-partial-hard-gates modules WELL-FORMED  core DEFECT   (R-STATUS)
files-empty            modules R-FILES=pass core R-FILES=fail (same bottom line, DEFECT both)
rep-no-citation        modules DEFECT       core WELL-FORMED (R-REPORT)
sec-cookie             modules DEFECT       core WELL-FORMED (R-NOSECRET)
```

The gate is self-contained and does not import them, so this is not a runtime defect — but any
sibling artefact, fixture, selftest or QA lane that exercises a *module* instead of the gate gets a
different answer on 9 of 92 packages. The modules must either be deleted or declared
non-authoritative in the receipt/knowledge entry.

**F9 (Low) — mislabelled detail tokens.** A missing artifact path reports `escape=1`
(`man-artifact-missing-file`), and a symlinked required file reports `missing=1`
(`files-report-symlink-out`, and the `evidence/`-symlink probe `missing=1,bad=0`). Fail-closed is unaffected, but a
receipt quoting these tokens attributes the wrong cause.

**F10 (Low) — module CLI divergence on a missing package dir.** `Manifest` and `ProvReport` print
`package=… verdict=ERROR exit=2`; `Chain` prints two fail lines and exits 1. The core implements
the required exit 2, so this only bites a direct invocation of the module.

**F11 (Low, landing) — `--selftest` depends on one exact filename.**
`corpus/instruments/claim-package-selftest.py` (or a pasted `run_selftest`); any other name prints
`selftest module=… verdict=missing exit=2`. `ExecGateSelftest.selftest.py` is a different name.

## 7. Keys the contract states that no rule reads

| contract statement | keys | read by | evidence |
|---|---|---|---|
| report.md row: Title; program; vuln class; repro steps; impact; affected asset; suggested fix; disclosure timeline; `observed_at` | those fields | nothing | `rep-bare-prose` exit 0 |
| report.md row: Scope excerpt "content sha256" | the digest | optional only | `rep-no-citation` exit 0 (core) |
| claim_checklist.md row: `OPERATOR-GATED`; residual gates | marker, list | nothing | `chk-no-marker` exit 0 |
| status semantics: `state` enum | `state` | nothing | `sta-state-submitted` exit 0 |
| status semantics: DONE requires reviewer `APPROVED` + `claim_ready:true` | `claim_review.outcome`, `claim_review.claim_ready` | nothing | base lacks both, exit 0 |
| status semantics: `do_not_submit` / `no_submission_performed` | both | nothing | `sta-do-not-submit` exit 0 |
| status semantics: `claimability_blocker` / `resume_condition` | both | `claimability_blocker` only as a blocker string when `claimable:false`; `resume_condition` never | base lacks both, exit 0 |
| status semantics: `verdict` | `verdict` | only as a blocker string | base lacks it, exit 0 |
| status semantics: hard-gate names | `written_scope`, `authorization`, `evidence_integrity`, `no_duplicate_or_prior_submission` | read as a required SET | `sta-partial-hard-gates` → `gates-missing=4` |
| status semantics: subchecks | `no_secrets`, `operator_attribution` | read as a required SET | same run |
| provenance row / custodian row | every key in the row | read | §4 |
| manifest row | every key in the row | read | §4 |
| claim-gates-only, not contract: reviewer role `kx-reviewer`, `status.severity`/`reward` | — | nothing (declared out of scope in `rules.txt`) | `sta-role-not-reviewer` exit 0 |

`state` and `do_not_submit` are hard gates in claim-gates as well as contract statements
(F2/F6); `no_submission_performed` is a contract guard only. The rest are prose or
reviewer/runbook concerns that the gate should name as out of scope rather than leave silent.

## 8. Residual risk and verification gaps

- Accept-case basis: my synthetic base is contract-derived; the gate's `WELL-FORMED` on it does
  not validate the exemplar's provenance or the S067 capture (out of scope — ExecSourceCapture /
  RevGateFixtures).
- The seats were still editing: `ExecGateProvReport.rules.py`, `ExecGateCore.claim-package-check.py`
  and `ExecGateSelftest.selftest.py` each changed under me once; §0 records both revisions and the
  re-run that showed identical verdicts. `ExecGateManifest.rules.py` and `ExecGateChain.rules.py`
  held their hashes throughout. Any later edit invalidates the pinned verdicts.
- Not exercised: an artifact >5 MiB (I tested an *extra* file >5 MiB → `oversize=1`; the artifact
  path would hit the same branch), non-UTF-8 bytes inside `report.md` (decoded with
  `errors='replace'` by design), FIFOs/device nodes, very long paths, concurrent mutation during
  a run, and `--selftest` from the landed repo path (not landed at review time). No performance
  claim is made.
- `--json` shape is verified for pass and for the ERROR path, not for a DEFECT package.

## 9. Tooling and scratch

No tool installed or upgraded; no package manager invoked. Scratch
`/fast/scratch/hyaku/kasegi-r43/RevGateRules` (disk guard: `/fast/scratch/hyaku` 25% used) held
the fixture builder, the two drivers, the 92 built variants plus the exemplar assembly and the
fixture copies, and the transcripts; it is removed before
this receipt is yielded. Nothing outside the wave `w1/` directory and that scratch dir was
written; no git/jj mutation was run; the fleet root and `shokuknow` were read-only.
