# CriticClaimsC2 — round-98 C2 attack (capture-secret-scan)

Seat: CriticClaimsC2 (leaf; no subagent dispatch). Scope: C2 only — the frozen predicate
K1–K7 at the C2 landing `e2caf4a1561b544a6ea684b0bcfa975f7e7f6061`. Read-only: no lane
commit, push, or mutating git/jj in the lane; the only writes are this report and its
`-receipts/` directory. Scratch `/fast/scratch/hyaku/kasegi-r98/CriticClaimsC2` (removed
before yield; receipts copied first). No tools installed or upgraded (host `python3` and
`git` only).

Frozen pins re-checked by extraction, not by trust:

```
$ git show e2caf4a1:corpus/instruments/capture-secret-scan.py | sha256sum
45f8d226b65e5bf16b9323bfc246c2748319713af5740a608838d6a6eb6f9f0e   (frozen 45f8d2…)
$ git show e2caf4a1:corpus/instruments/claim-package-check.py | sha256sum
8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6   (frozen 8b6f84…)
```

## 1. Landing re-run at two independent seeds

The frozen command with my own `--seed` (the frozen command omits `--seed`, so the gate
takes a run-time seed; the pre-freeze control used 20261107):

```
python3 -B .ufo/waves/round-98/c2/capability-check.py --lane . \
  --rev e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 --work <scratch> \
  --instrument-sha256 45f8d226b65e5bf16b9323bfc246c2748319713af5740a608838d6a6eb6f9f0e \
  --gate-sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6 \
  --seed 777001
```

Observed (seed 777001; seed 424242 is identical except the `seed=` field):

```
CAPABILITY-CHECK-REV rev=e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 seed=777001
LIMB K1 ok inst_sha=pin-ok gate_sha=pin-ok selftest=pass cases=170
LIMB K2 ok rc=0 scanned=3280 hits=0 allowed=27 unused_allow=0
LIMB K3 ok rc=1 hits=9 missing=none extra=none
LIMB K4 ok base_new_shape_hits=0 old_shapes_missing=none
LIMB K7 ok base_widened_hits=0 landing_widened_hits=5 missing=none
LIMB K5 ok rows=1 last=87 named=True
LIMB K6 ok rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential
CAPABILITY-CHECK-RESULT pass rc=0
RC=0
```

Seed 424242: `CAPABILITY-CHECK-REV … seed=424242`, the same seven `LIMB … ok` lines,
`CAPABILITY-CHECK-RESULT pass rc=0`. Both runs took ~68 s.

Independent checks of the counts the claim names:

```
$ python3 -B base/capture-secret-scan.py --selftest | tail -1
SELFTEST-RESULT pass cases=148
$ python3 -B land/capture-secret-scan.py --selftest | tail -1
SELFTEST-RESULT pass cases=170
```

The 22-case delta is exactly the 22 round-98 selftest cases (5 ci-build, 5 iam,
6 session-cookie, 6 widened-boundary). The allowlist has 25 data rows; K2's `allowed=27`
is 27 allowed matches across those rows (at least one row matches more than once), and
`unused_allow=0`.
The SCORECARD row (line 307) names all nine round-98 ids once and its last cell is `87`.

## 2. Independence claim: a literal-locked matcher

Hypothesis under test: K3's plants are the instrument's own selftest literals in disguise.
I built nine patterns from `re.escape` of the instrument's selftest positive literals
(`glcbt-Ab3_` + `k`*20, `gliamrt-` + `A`*43 + `.` + `B`*43, `gliamac-` + …, the session
cookie `_gitlab_session=` + `0a`*32, and the five widened literals) and ran them over the
gate's own plants, rebuilt with `gate.build_plants(work, seed)` (seeds 777001 and 424242;
nonces `cykwdgzx30x5` and `8qw9tcxni0y1`).

Observed, both seeds:

```
VARIANT V1-literal-locked K3=FAIL hits=0
  missing=[all nine (path, shape) positives] extra=none
  PROBE selftest-literal  b'[gitlab-ci-build-token-fixture-redacted-r98] end' correct=[gitlab-ci-build-token] variant=[gitlab-ci-build-token] same
  PROBE plant-p1          b'[gitlab-ci-build-token-fixture-redacted-r98] end' correct=[gitlab-ci-build-token] variant=none DIVERGES
```

The literal-locked matcher matches its own selftest literal and none of the nine plants:
K3 FAIL, 0/9. **The independence claim holds** — the plants are generated from the rule
grammar, not copied from the selftest.

## 3. Session-cookie context: does n10 kill a context-dropped matcher?

Variant V2 replaces only the session-cookie rule with
`(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])` (the `_gitlab_session` context removed). Over
the same plants:

```
VARIANT V2-session-nocontext K3=FAIL hits=10
  extra=[(<nonce>-n10.txt, gitlab-session-cookie)] missing=none
  SELFTEST rc=1 fail cases=170 fails=5
  PROBE bare-64-hex b'x=' + b'0a'*32 -> correct=none variant=[gitlab-session-cookie] DIVERGES
```

**n10 kills the coarse context drop**: the bare 64-hex negative is a hit, K3 fails. The
selftest also catches it five times (the bare 64-hex regex fires on the GCS signatures).

A narrower drop keeps `_gitlab_session` but discards the `_geo_`/`cell-<N>-` structure
(V3: `_gitlab_session[\s"'=:;]+[0-9a-f]{64}(?![0-9a-f])`):

```
VARIANT V3-session-keyword-only K3=PASS hits=9 missing=none extra=none
  SELFTEST rc=1 fail cases=170 fails=2
  SELFTEST-FAIL gl-session-cookie-cell FAIL got=none
  SELFTEST-FAIL gl-session-cookie-geo  FAIL got=none
```

K3 alone is passable by V3; K1's selftest is what catches it. The session-cookie limb is
real only as K3 + K1 together.

## 4. Limb-by-limb: which limbs are real, which are passable

Matrix over the gate's plants (seed 777001; seed 424242 identical). `K1` is the selftest
behavioural part of K1 (the sha256 pin is not exercised by these variants); `K3`/`K7` are
the gate's own checks; `full gate` is the gate with `--instrument-sha256` omitted.

| variant | what is wrong | K1 selftest | K3 | K7 | full gate (no pin) |
|---|---|---|---|---|---|
| V0 landing | none | pass 170 | pass 9/9 | pass | pass (with pin) |
| V1 literal-locked | only selftest literals | n/a (partial list) | **FAIL 0/9** | n/a | n/a |
| V2 session no context | any 64 hex | FAIL 5 | **FAIL extra n10** | pass | n/a |
| V3 session keyword-only | no `_geo_`/`cell-` | FAIL 2 | **PASS** | pass | n/a |
| V4 ci-build strict boundary | `(?![A-Za-z0-9_-])` | pass 170 | **PASS** | **PASS** | **PASS** |
| V5 ci-build zero prefix | `{0,5}` | pass 170 | **PASS** | **PASS** | **PASS** |
| V6 iam second 43+ | `{43,}` | pass 170 | **PASS** | **PASS** | **PASS** |
| V7 all five no boundary | no lookahead | FAIL 1 | **FAIL extra n5,n8** | pass | n/a |
| V7b feed/oauth/scim no boundary | no lookahead on 3 | **PASS 170** | **PASS** | **PASS** | **FAIL (K2 rc=1 hits=4)** |
| V8 all five strict | round-97 boundary | FAIL 6 | **FAIL 5 missing** | **FAIL** | n/a |
| V9 do-nothing (round-97) | no new shapes | FAIL 12 | **FAIL 0/9** | **FAIL** | n/a |

Reading the table:

- **Real limbs.** K3 kills literal-locking (V1), the coarse context drop (V2), the
  no-boundary variant for the two shapes whose negatives are 21 chars (V7), the old strict
  boundary (V8), and the do-nothing instrument (V9). K7 kills the old strict boundary (V8)
  and the no-widening instrument (V9). K1's selftest kills V2, V3, V7, V8, V9.
- **Passable limbs.** V4, V5 and V6 pass K1's selftest, K3, K7 and the full behavioural
  gate. V7b passes K1, K3 and K7 but the full gate catches it on K2. Each is a wrong
  instrument against the claim's statement:
  - **V4** keeps the round-97 strict right boundary on `gitlab-ci-build-token`; the claim
    says `(?![A-Za-z0-9])`. Probes: `glcbt-Ab3_` + 20 chars + `_x`/`-x` are hits under the
    landing instrument and misses under V4. No K3 plant or selftest case has a ci-build
    token followed by `_`/`-`.
  - **V5** accepts a zero-length ci-build prefix (`glcbt-_` + 20); the claim says 1–5. No
    K3 negative and no selftest case has a zero prefix.
  - **V6** accepts a 44-character second iam segment; the claim says exactly 43. No K3
    negative and no selftest case has a 44-character second segment (`gl-iam-auth-code-44`
    is 44 in the *first* segment, which the exact-43 first segment already rejects).
  - **V7b** drops the right boundary on `gitlab-feed-token`, `gitlab-oauth-app-secret` and
    `gitlab-scim-oauth-token`; their K3 negatives n6/n7/n9 are too *short* (19/63/19), and
    the selftest's only too-long negative is `gl-feed-token-v2-long` (21). Probes:
    `feed_token=` + 21, `gloas-` + 65, `glsoat-` + 21 are hits under V7b and misses under
    the landing instrument. **K2 catches V7b**: on the landing tree the no-boundary
    instrument reports 4 hits (21/65-character over-long round-97 fixtures and a
    filename-like `glsoat-no-left-boundary-nopin` string), so the boundary for these three
    shapes is bound by K2 even though K3's negatives are short.

## 5. Full-gate counterexample (pin omitted)

To test whether the gate as a whole — not just K3 — accepts a wrong instrument, I made a
`git clone --shared` fixture at `$S/lane`, checked out the landing, replaced only the
instrument with V4/V5/V6, and committed each on a branch. Host guard: `git -C $S/lane
rev-parse --show-toplevel` printed `$S/lane` before the first commit. The gate was run with
the frozen command minus `--instrument-sha256`/`--gate-sha256` (the pin is the only limb
that rejects a wrong instrument by identity):

```
python3 -B .ufo/waves/round-98/c2/capability-check.py --lane $S/lane \
  --rev <3a6fc107…|0ed19605…|ded7d22d…> --work <scratch>
```

Observed:

```
# V4, fixture commit 3a6fc1079d11252d1d55a78cd5c1b6459cc86b9b
CAPABILITY-CHECK-REV rev=3a6fc1079d11252d1d55a78cd5c1b6459cc86b9b seed=1542001404
LIMB K1 ok selftest=pass cases=170
LIMB K2 ok rc=0 scanned=3280 hits=0 allowed=27 unused_allow=0
LIMB K3 ok rc=1 hits=9 missing=none extra=none
LIMB K4 ok base_new_shape_hits=0 old_shapes_missing=none
LIMB K7 ok base_widened_hits=0 landing_widened_hits=5 missing=none
LIMB K5 ok rows=1 last=87 named=True
LIMB K6 ok rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential
CAPABILITY-CHECK-RESULT pass rc=0

# V5, fixture commit 0ed19605e1b3e4d2567571024346f72db6f7310e
CAPABILITY-CHECK-REV rev=0ed19605e1b3e4d2567571024346f72db6f7310e seed=28517191
LIMB K1 ok selftest=pass cases=170
LIMB K2 ok rc=0 scanned=3280 hits=0 allowed=27 unused_allow=0
LIMB K3 ok rc=1 hits=9 missing=none extra=none
LIMB K4 ok base_new_shape_hits=0 old_shapes_missing=none
LIMB K7 ok base_widened_hits=0 landing_widened_hits=5 missing=none
LIMB K5 ok rows=1 last=87 named=True
LIMB K6 ok rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential
CAPABILITY-CHECK-RESULT pass rc=0

# V6, fixture commit ded7d22da44d90856fcd9e5f07acf251732f331b
CAPABILITY-CHECK-REV rev=ded7d22da44d90856fcd9e5f07acf251732f331b seed=174071834
LIMB K1 ok selftest=pass cases=170
LIMB K2 ok rc=0 scanned=3280 hits=0 allowed=27 unused_allow=0
LIMB K3 ok rc=1 hits=9 missing=none extra=none
LIMB K4 ok base_new_shape_hits=0 old_shapes_missing=none
LIMB K7 ok base_widened_hits=0 landing_widened_hits=5 missing=none
LIMB K5 ok rows=1 last=87 named=True
LIMB K6 ok rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential
CAPABILITY-CHECK-RESULT pass rc=0
```

All three wrong instruments pass the entire behavioural gate. The frozen command *does*
pass the pins, and the pins match the landing bytes, so the landed artifact is the one the
claim describes; the counterexample is that the gate's K2–K7 do not bind the exact
grammar. The sha256 pin (K1) is the only limb that distinguishes V4/V5/V6 from the landing
instrument.

V7b is the counterpoint that shows K2 is not vacuous: the same full-gate command at
fixture commit `b939b52f81bc3642158d0f2bce8e534699caa18d` (no boundary on
feed-token/oauth-app-secret/scim-oauth-token) fails K2 with `rc=1 hits=4`, all four in
round-97 receipts (`ExecC2Probe-receipts/fixture-bytes.txt` lines 11/17/35 and
`MutC2Counter-receipts/09-receipt-index.txt` line 38). K2 therefore binds those three
boundaries; V4/V5/V6 remain the full-gate counterexamples.

## 6. Statement-fidelity caveats (not kills)

1. **The five widened shapes' boundary is not S140's literal boundary.** S140's rules for
   the five (`gitlab_runner_registration_token`, `gitlab_feed_token`,
   `gitlab_oauth_app_secret`, `gitlab_feed_token_v2`, `gitlab_scim_oauth_token`) end in
   `(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)` (S140 snapshot regex lines 101, 160, 174,
   190, 278). The landing instrument ends them in `(?![A-Za-z0-9])`
   (`capture-secret-scan.py:311-322`). The two agree on the `_`/`-` widening (both are
   punct) but differ on non-ASCII and control bytes: probes `GR1348941` + 20 + `é`
   (UTF-8) and `GR1348941` + 20 + NUL are hits under the instrument and would not be hits
   under S140's boundary. The claim's sentence "now use S140's own punct/space/EOL right
   boundary" is therefore a superset, not the literal rule; the difference is
   over-reporting only (no miss), and the counter does not bind it.
2. **The session-cookie separator is the instrument's own class.** `[\s"'=:;]+` matches
   `=`, space, `:`, quotes and `;`, but not `%3D`, `&` or `+`. Probes:
   `_gitlab_session%3D<64hex>` and `_gitlab_session&x=<64hex>` are misses; S140's
   assignmentContext is a keyword-group mechanism, not a separator, so a URL-encoded
   cookie header could be a miss against S140. The claim says "separator" without a class;
   K3's p4 only exercises `=`.
3. **K4's "misses none of the earlier shapes" is a pattern-name set check**, not a
   behavioural check (`base_shapes = {name for name, _ in mod.patterns()}`). A base
   instrument with the right names and wrong regexes would pass that half of K4.
4. **K6 checks one shape**; an instrument that over-reports on the round-86 freeze is not
   bound.
5. **K2 is a clean-scan regression check**; a literal-locked or otherwise wrong instrument
   that reports nothing on the landing tree passes it (V1 would pass K2 if it were the
   whole instrument).

## 7. Verdict

- The frozen K1–K7 all pass at `e2caf4a1` at seeds 777001 and 424242; the pins match; the
  selftest is 170 (base 148); K3's nine positives are exact and the ten negatives silent.
- The independence claim holds: a literal-locked matcher scores 0/9 and K3 fails.
- n10 kills the coarse context drop; the keyword-only drop passes K3 but fails the selftest.
- The gate's behavioural limbs are passable by V4/V5/V6; V7b is caught by K2 (4 hits). The
  sha256 pin (K1) is the only limb that binds the exact grammar for the full-gate
  counterexamples. This is a **counter-coverage defect, not a claim
  defect**: the pinned bytes implement the claim's grammar (read at
  `capture-secret-scan.py:302-322`), and the probes above show the landing instrument
  accepts `glcbt-…_x`, rejects `glcbt-_…`, rejects a 44-character second iam segment, and
  accepts `GR1348941…_x`; the gate simply does not test those clauses.
- Smallest safe correction for the next gate: add the missing plants/negatives that
  the full gate does not bind — (a) ci-build token + `_`/`-` positive and zero-prefix
  negative, (b) 44-character second iam segment negative — and state the
  boundary/separator fidelity limits in the claim or the knowledge entry. The
  feed-token/oauth/scim too-long negatives (c) are already bound by K2 through the
  round-97 receipts; adding them to K3 would be redundancy, not a new kill.

VERDICT: C2 K1–K7 PASS at e2caf4a1 at seeds 777001 and 424242 — no kill condition met; claim verified with the §6 boundary/separator wording caveat.
VERDICT: K3 independence claim HOLDS — literal-locked matcher 0/9, K3 FAIL.
VERDICT: n10 KILLS the context-dropped session-cookie matcher — K3 FAIL with an extra hit on the bare 64-hex negative.
VERDICT: K3 is passable by V4/V5/V6/V7b; the full gate is passable by V4/V5/V6 (V7b fails K2 with 4 hits); K1's sha256 pin is the only limb that binds the exact grammar for those three — counter-coverage defect, not a claim defect.
VERDICT: the five widened shapes' boundary is a superset of S140's literal punct/space/EOL boundary (non-ASCII/control only); the claim's sentence is imprecise but the `_`/`-` widening is faithful.
