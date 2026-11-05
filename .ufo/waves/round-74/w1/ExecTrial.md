# ExecTrial — round-74 w1 — end-to-end claim-package trial (SHONEN box 2)

Seat: ExecTrial (wave-1 leaf executor). Item: the round's non-claim end-to-end
domain trial — one public disclosed report → six-file claim package →
claim-package-check.py 8/8 WELL-FORMED → pricing note through F13/F17/F18
(mined from considerthese/2026-10-26.md `## Self-improvement suggestions`
item 2; routed defect R73-V5). Not scored as a claim per claims.json
`non_claim_work[0]`; no commits, no pushes, no git mutations performed.

## Result

**Gate verdict WELL-FORMED, 8/8 rules pass, exit 0, on the first full gate run.**
Package at `.ufo/waves/round-74/w1/trial/package/`; receipts recorded below.

## Disclosure chosen

Project curl Security Advisory **CVE-2023-38545**, "SOCKS5 heap buffer overflow"
(https://curl.se/docs/CVE-2023-38545.html, published 2023-10-11, H1 report
2187833): plain public vendor documentation, no auth wall, complete repro
conditions, severity and reward language on the page. Program policy ground:
curl's own Vulnerability Disclosure Policy
(https://curl.se/dev/vuln-disclosure.html), captured with the same tool — the
assignment's primary scope-excerpt route, not the fallback.

The first candidate (HackerOne report 315615, Imagetragick) was abandoned: the
fetch returned HTTP 404 (recorded below, exit 1); no fallback-loop beyond one
candidate switch.

## Deliverables (all under .ufo/waves/round-74/w1/)

| Path | What |
|---|---|
| `trial/evidence/disclosure-capture.txt` | mandated TRIAL1 capture of the advisory (HTTP 200; 13940 fetched bytes; 6446 snapshot bytes; sha256 `327bc909e01ee3dc78272c06d3d568b78e92e5b4c35c7e527394422d763b238b`; fetched 2026-11-05T08:54:46Z) |
| `trial/evidence/policy-capture.txt` | TRIAL1-POLICY capture of the program policy page (HTTP 200; 26500 fetched bytes; 19670 snapshot bytes; sha256 `9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102`; fetched 2026-11-05T08:55:15Z) |
| `trial/package/report.md` | title; program + official URL; `## Scope excerpt` (verbatim policy text with URL + observed_at + content sha256); vuln class (CWE-122); repro steps (isolated-lab, no secrets); impact tied to the policy's own High-band language; affected asset; suggested fix; disclosure timeline; literal `No submission performed` |
| `trial/package/claim_checklist.md` | per-program intake steps from the captured policy (HackerOne private handling for HIGH/CRITICAL, GitHub public route for LOW/MEDIUM, CNA self-assignment, publish-after-handling); carries `OPERATOR-GATED`; residual gates named |
| `trial/package/evidence/manifest.json` | `evidence-manifest/v1`; 3 positive artifacts (disclosure capture, policy capture, verbatim excerpt `source-excerpt.txt`), each sha256 recomputed from bytes; redaction receipt per artifact with distinct producer/verifier; `expected_head_sha256` |
| `trial/package/evidence/disclosure-capture.txt`, `policy-capture.txt` | byte-identical copies of the two captures (post-copy sha256sum re-verified: `327bc9…`, `9e346a…`) |
| `trial/package/custodian-receipts.json` | 3-step decision chain (scope-triage, evidence-freeze, manifest-attest); every action carries nonempty `matched_grant_id` = the program policy's intake section `curl-vuln-disclosure-policy#Vulnerability-Handling-Report` and `scope_signal` exactly `NO_SCOPE_OBJECTION`; `head_sha256` = final decision digest = manifest `expected_head_sha256` = `e0b6fa97a937fb7eb47345000873b2ff01ccecc82a272d9c9920776d73e71b52` |
| `trial/package/provenance.json` | agents with requested `lane-routing(operator table)` / resolved `zai/glm-5.3-flash` per transition; commands with exit codes incl. the capture commands; pin `https://github.com/VeigaPunk/kasegi-shokunin.git` @ `847b53792d2d29d161cad7d21a33c89df9e52e8d`; `policy_sha256` = `6f445bc3389a9c577beff03b5003f967f55819e6b3dbcbb5dbc0faeba73269e1` (sha256 of claim-package-contract.md); `external_effects_performed: []`; secrets attestation present, affirmative |
| `trial/package/status.json` | `manifest_sha256` `1672f0b71b0bd121b20f9aff0096d759967ff92d58a61cfaec34d906037d9192` over the manifest bytes; hard_gates: written_scope PASS, **authorization FAIL — "no authorized program engagement; documentation-only trial"** (by design), evidence_integrity PASS, no_duplicate_or_prior_submission PASS; subchecks no_secrets PASS, operator_attribution PASS; reviewer `KasegiR74-L1-integrator` (requested/resolved models, `fallback: false`), distinct from every manifest producer/verifier identity; `claimable: false`, blocker `operator-gated: no authorized live program`, resume `operator authorizes a program engagement`; state BLOCKED |
| `trial/gate-run.txt`, `trial/gate-run.json` | full gate transcripts (both modes) |
| `trial/pricing-note.md` | the finding priced through F13/F17/F18 per each entry's own criteria |

## Gate evidence (commands + exits)

| # | Command (cwd = lane root unless noted) | Exit |
|---|---|---|
| 1 | `mkdir -p /fast/scratch/hyaku/kasegi-r74/ExecTrial` | 0 |
| 2 | `python3 corpus/instruments/capture-source.py --id TRIAL1 --url https://hackerone.com/reports/315615 --out .ufo/waves/round-74/w1/trial/evidence/disclosure-capture.txt --kind html` | **1** (HTTP 404 traceback; candidate discarded) |
| 3 | `python3 corpus/instruments/capture-source.py --id TRIAL1 --url https://curl.se/docs/CVE-2023-38545.html --out .ufo/waves/round-74/w1/trial/evidence/disclosure-capture.txt --kind html` → `TRIAL1 status=200 … sha256=327bc909…3b238b utc=2026-11-05T08:54:46Z` | 0 |
| 4 | `python3 corpus/instruments/capture-source.py --id TRIAL1-POLICY --url https://curl.se/dev/vuln-disclosure.html --out .ufo/waves/round-74/w1/trial/evidence/policy-capture.txt --kind html` → `TRIAL1-POLICY status=200 … sha256=9e346a4e…f102 utc=2026-11-05T08:55:15Z` | 0 |
| 5 | `sha256sum disclosure-capture.txt policy-capture.txt corpus/knowledge/claim-package-contract.md` | 0 |
| 6 | pre-packaging secret scan with the gate's own `SECRET_PATTERNS` (module loaded via importlib from `claim-package-check.py`) over both captures → `disclosure-capture.txt bytes=6446 hits=0 []`, `policy-capture.txt bytes=19670 hits=0 []` | 0 |
| 7 | package build (eval python; first attempt exit 1 `NameError: manifest`, fixed and rerun 0) | 0 |
| 8 | `cp trial/evidence/{disclosure-capture,policy-capture}.txt trial/package/evidence/ && sha256sum …` (digests identical) | 0 |
| 9 | `python3 corpus/instruments/claim-package-check.py .ufo/waves/round-74/w1/trial/package` | **0** |
| 10 | `python3 corpus/instruments/claim-package-check.py .ufo/waves/round-74/w1/trial/package --json` | **0** |
| 11 | `grep -c '38545' corpus/source-snapshots/round-35/S052.txt` → `0` (exit 1 = no match, intended); `grep -ci 'curl' corpus/source-snapshots/round-35/S052.txt` → `0` (exit 1) | 1 / 1 |
| 12 | `grep -c 'CWE-122' corpus/knowledge/program-severity-ladders-and-reward-scales.md` → `0` (exit 1) | 1 |
| 13 | `rm -rf -- /fast/scratch/hyaku/kasegi-r74/ExecTrial && test ! -e …` → `scratch removed` | 0 |

Gate transcript (step 9, verbatim; also `trial/gate-run.txt`):

```
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=3,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=3,receipts=3,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=5,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=3,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=…/trial/package rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
```

`--json` (step 10): `{"exit": 0, "fail": 0, …, "pass": 8, …, "verdict": "WELL-FORMED"}` — full line in `trial/gate-run.json`.

## Pricing summary (full detail in trial/pricing-note.md)

- **F13** (`program-severity-ladders-and-reward-scales.md`): advisory's "Severity: High" aligns at the label level with VRT P2 "High" (entry l.27) on Bugcrowd's suggested P1–P5 baseline (entry l.22), with the override caveat (entry l.32); the entry's crosswalk holds no CWE-122 node (grep 0/exit 1). Entry l.12's own rule (labels / policy / reward not interchangeable) is exactly this package's shape: High label, no-project-bounty policy (policy L43), 4660 USD platform-recorded reward (advisory L108).
- **F17** (`immunefi-vscs-v2-2-smart-contract-severity.md`): no VSCS level claimable — the demonstrated impact does not reach the held Websites-and-Apps Critical bullet "Execute arbitrary system commands" (entry l.58), Smart Contracts is excluded by the asset-class rule (entry l.56), and the entry is classification-only with no payout vocabulary (entry l.80).
- **F18** (`cisa-kev-catalog.md`): CVE-2023-38545 absent from the pinned feed (1,756 records, catalogVersion 2026.10.23, entry l.18; greps 0/exit 1); KEV is not a payout ladder (entry l.82). No KEV-adjacency asserted.

## R-NOSECRET discipline

The gate's six secret shapes (private-key header, `op://` reference, bearer,
authorization, labelled credential, session cookie) were run over the captured
evidence **before** packaging (step 6) and over the whole package tree at gate
time (R-NOSECRET hits=0). The captured advisory and policy pages carry no
token, cookie or session material; **zero redactions were needed** (receipts
record `removed: []` with scanned digest = artifact digest per artifact).

## Bounds compliance

- No git/jj mutation anywhere; only read-only `git remote -v` / `rev-parse HEAD` were used (remote `https://github.com/VeigaPunk/kasegi-shokunin.git`, HEAD `a5e814a1679626b6d9fb9ba3f1a6483ed4f4b68c`; the provenance pin carries the round freeze commit `847b5379…` per the seat spec).
- Writes confined to the assigned wave paths (`…round-74/w1/trial/**`, this report) and the scratch root; lane working tree otherwise untouched.
- HTTP GETs only: two documentation pages used (advisory, policy) plus one 404 probe of a candidate disclosure; no login walls hit, no port scans, no exploitation, no credential material anywhere.
- Scratch root `/fast/scratch/hyaku/kasegi-r74/ExecTrial/` deleted before yield (step 13, verified absent). Only `/tmp` use: none (TMPDIR pointed at scratch for the capture runs; the tool wrote no temp files on the html path).
- No tool installs were needed or performed; no pacman transactions.

## Risks / notes for the L1

1. **Reviewer independence is nominal**: `KasegiR74-L1-integrator` is a distinct identity per spec, but the reviewer is the same physical seat; status.json names this as a residual gate. The verifier identity in the receipts (`capture-source-sha256-crosscheck`) likewise describes an instrumented pass, not a second party.
2. **Policy-vs-advisory reward tension is an observation, not a defect**: the project policy states no project bounty (L43) while the advisory records a 4660 USD bounty (L108); the package attributes the reward to the intake platform only as far as the two artifacts show (the IBB linkage itself is not in the captured bytes and is not asserted).
3. The package's provenance command list contains the failed candidate capture (exit 1) for honesty; the exemplar fixture package (curl CVE-2025-9086) was used as the shape model, and this trial deliberately uses a different disclosure of the same program.
4. The gate has no enforcement of `status.severity`/`reward` (contract round-13 boundary note); those carry no figures here for that reason — pricing lives in `trial/pricing-note.md`.
