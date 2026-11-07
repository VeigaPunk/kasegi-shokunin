# ExecC2Counter — round-97 w1, independent re-derivation of C2's gate numbers

Seat: ExecC2Counter (leaf). Lane: kasegi-shokunin. All work at lane HEAD a9a53608dce6aea07d298bb9d5133532078eb1dd (the C2 landing). No files edited outside this report, this seat's receipts dir, and scratch /fast/scratch/hyaku/kasegi-r97/ExecC2Counter (trap-removed). No tools installed (none needed).

## Verdict

AGREE on all four items — every C2 gate number re-derived independently and matching the frozen pins/values:

1. Gate at three own seeds — **AGREE** (pass rc=0 at seeds 9701, 20261107, 555555; all six limbs ok, detail lines identical to each other and to the frozen controls receipt's seed-4242 run).
2. K1 selftest AST count — **AGREE** (cases=137 + paths=8 + checks=3 = 148 = printed cases=148; committed instrument bytes == candidate scanner, both sha256 59909fc4d70819b1a67fa9eec36db2b054462770959828e4c3ff3ce164d2bd92).
3. K5 SCORECARD row — **AGREE** (exactly 1 `capture-secret-scan` row in the whole file; 4 cells; last cell "First-working round" = `87`; all ten round-97 shape ids present in the "What it can now do" cell, missing=none).
4. K6 at the round-86 freeze — **AGREE** (252df0c90c066d83d229e3107811a6bc05e8feed is "round-86: freeze claims C1 … and C2 …" and an ancestor of the round-97 freeze daf7fc6a; the landed scanner over that rev reports exactly three shapes: `aws-access-key-id`, `aws-sts-session-token`, `credential`; aws-sts-session-token present → no shape lost).

Routed observation (qualifier, not a verdict change; my items' numbers are unaffected): the dispatch/goal text (make-wave-r97.py line 49, mirrored in w1-dispatch.json and w1-spec.json) says "the pre-freeze K1-K6 pass at the scratch candidate **72fa2fa1**", but the frozen claims.json C2 `controls` field and the committed receipt .ufo/waves/round-97/l1/c2-candidate-r97.txt both name scratch candidate **659e320f8ec95e02cb82bb8d2f52a894fa190a80** (seed 4242). One of the two frozen texts is stale; L1 may wish to route/correct the wave-spec narrative.

## Item detail

### Item 1 — frozen gate re-run at three own seeds
Command template per claims.json C2 `command`, at rev a9a5360, pins `--instrument-sha256 59909fc4…bd92` / `--gate-sha256 8b6f8493…c8e6`, scratch work dirs under $S. All three runs:

```
CAPABILITY-CHECK-REV rev=a9a53608dce6aea07d298bb9d5133532078eb1dd seed=<9701|20261107|555555>
LIMB K1 ok inst_sha=pin-ok gate_sha=pin-ok selftest=pass cases=148
LIMB K2 ok rc=0 scanned=3018 hits=0 allowed=27 unused_allow=0
LIMB K3 ok rc=1 hits=10 missing=none extra=none
LIMB K4 ok base_new_shape_hits=0 old_shapes_missing=none
LIMB K5 ok rows=1 last=87 named=True
LIMB K6 ok rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential
CAPABILITY-CHECK-RESULT pass rc=0
```

Every limb line equals the frozen controls receipt (`…/l1/c2-candidate-r97.txt`, seed 4242): K2 scanned=3018 hits=0 allowed=27 unused_allow=0; K3 hits=10 missing=none extra=none; K6 same three shapes. Seed independence of the nonce-derived plant repo holds (run-time nonce differs per seed; HIT set still equals the ten positives exactly).

### Item 2 — K1 selftest count by AST
Parsed `git show a9a5360:corpus/instruments/capture-secret-scan.py` (byte-identical to .ufo/waves/round-97/c2/candidate-scanner.py; both sha256 59909fc4…bd92, matching the frozen instrument pin; gate script sha256 1d87da67…e597 matches counter_sha256). AST over `selftest()`: `cases` list = 137 (name, data, want) triples, `paths` = 8 scope triples, `checks` = 3 allowlist triples; sum 148 = the `SELFTEST-RESULT pass cases=148` the gate's K1 observed (selftest requires >= 148). No double-counted or starred elements.

### Item 3 — K5 SCORECARD cell split
`git show a9a5360:SCORECARD.md`: rows matching `capture-secret-scan` at line start = **1** (whole file, not just the `## Capabilities` section). Cells = 4 against header ["Capability", "What it can now do", "Evidence pointer", "First-working round"]. Last cell = `87`. Cell[1] "What it can now do" (3416 chars) contains all ten ids: gitlab-runner-registration-token, gitlab-feed-token, gitlab-oauth-app-secret, gitlab-feed-token-v2, gitlab-incoming-email-token, gitlab-scim-oauth-token, gitlab-deploy-token-in-url, gitlab-feature-flags-client-token, gitlab-runner-controller-token, gitlab-kubernetes-agent-token; no other cell is required to and none of the ten is missing there.

### Item 4 — K6 at the round-86 freeze
252df0c90c066d83d229e3107811a6bc05e8feed subject: "round-86: freeze claims C1 (knowledge-scope snapshot repoint 398/1721->596/1716) and C2 (subject-bound IBB 1997312 package), controls executed, S122/S123 queued"; `git merge-base --is-ancestor` vs round-97 freeze daf7fc6a → rc 0. Ran the landed scanner extracted from a9a5360 (with its pinned claim-package-check.py gate and allowlist) over `--rev 252df0c9`: scanned=1074, 6 HIT lines across 2 capture paths — .ufo/waves/round-85/w1/ScoutSources-receipts/live-LEAD-hackerone-ibb-1997312.json line 1 and corpus/source-snapshots/round-86/S122.txt line 1 — shapes exactly {credential, aws-sts-session-token, aws-access-key-id}; rc=1; allowed=16 unused_allow=10 (unused rows bind paths that post-date round 86; reported, not an error; K6 predicate needs only rc=1 + aws-sts-session-token reported). Matches the gate's K6 limb at every seed and the frozen receipt.

## Receipts

All under .ufo/waves/round-97/w1/ExecC2Counter-receipts/ (lane-relative):

- gate-seed9701.txt — `python3 -B .ufo/waves/round-97/c2/capability-check.py --lane <lane> --rev a9a5360… --work $S/work-9701 --instrument-sha256 59909fc4… --gate-sha256 8b6f8493… --seed 9701` → 8 lines as quoted above, CAPABILITY-CHECK-RESULT pass rc=0 (observed; wall ~56s).
- gate-seed20261107.txt — same, --seed 20261107 → pass rc=0, identical limb lines.
- gate-seed555555.txt — same, --seed 555555 → pass rc=0, identical limb lines.
- ast-k5-derivation.txt — eval(Python) AST count over the committed instrument + SCORECARD row cell split → committed==candidate bytes True; cases=137 paths=8 checks=3 sum=148 delta=+0 MATCH; k5_rows=1; last cell '87' MATCH; cell[1] round97_ids=10, missing=none.
- k6-round86-shapes.txt — extracted landed scanner (rev a9a5360 files) run `--rev 252df0c9…` → 6 HIT lines (paths+shapes only, no values), `CAPTURE-SECRET-SCAN mode=rev:252df0c9… scanned=1074 hits=6 files=2 allowed=16 unused_allow=10 rc=1`.
- k6-freeze-identity.txt — `git show -s 252df0c9…` subject line; merge-base --is-ancestor vs daf7fc6a rc=0; sha256sum of candidate-scanner.py (59909fc4…bd92) and capability-check.py (1d87da67…e597).

Pin checks observed before running: instrument_sha256 (claims.json) == sha256(candidate-scanner.py) == sha256(git show a9a5360:corpus/instruments/capture-secret-scan.py) = 59909fc4…bd92; counter_sha256 == sha256(capability-check.py) = 1d87da67…e597; the gate verified its own gate_sha pin (8b6f8493…c8e6, claim-package-check.py at the landing) → `gate_sha=pin-ok` in every K1 line.

No credential values appear in any receipt (scanner output prints shape/path/line only). rc values: every cited command's observed rc is stated above; all commands exited as reported, none suppressed.
