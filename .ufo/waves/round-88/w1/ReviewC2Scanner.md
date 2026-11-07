# ReviewC2Scanner — round 88 attempt 1, C2 code review

Seat: ReviewC2Scanner (leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `6beead91`, freeze `7f2ebebf`, C1 landing `fd33e1bf`, C2 landing `b43dc215` (`landing.json`).
Reviewed bytes: `corpus/instruments/capture-secret-scan.py` at `b43dc215`, sha256
`d73495364f90f78fa5ee6ad28b83fce772a349a5339d240b21db4d5d04425417` (equals the frozen candidate pin);
allowlist `f9fbd7e7…`, SCORECARD row byte-equal to `c2/candidate/scorecard-row.txt`; landing diff = SCORECARD.md +
instrument only (allowlist unchanged, also byte-equal to its pin).

Method: read the landing diff, S126/S127, and the frozen counter; extracted the landing instrument with
`git show` into scratch and ran it with `--files` over generated fixtures; reproduced K1–K6 over a scratch
`git clone --shared` of the lane at the landing and again over a one-line lookbehind mutant. No fixture bytes
and no matched values are stored: fixtures are generated, receipts carry digests and shape names only.

## Frozen predicates (not re-scored)

P1–P3 hold at `b43dc215`: `l1/c2-landing-r88.txt` prints `CAPABILITY-CHECK-RESULT pass rc=0`, P2 byte-equal
(all three pins), P3 `changed=2 outside=0 verdict=PASS`; I reproduced the same counter pass on an independent
scratch clone (`ReviewC2Scanner-receipts/counter-landing-clone.txt`). Everything below is a routed
defect/qualifier for round 89, **not** a re-score of C2.

## Verdict: CHANGES-REQUESTED (routed to r89)

The extension works for the shapes the counter plants, and the scope predicate is correct, but the frozen
statement's Azure separator clause ("**either order, &/&amp;/\u0026 separators**") is false for
`\u0026`-escaped captures in the parameter order the source itself documents, and the instrument's own
docstring restates that clause. Fix in r89; the frozen predicates are unaffected.

## (a)/(b) survey — claim-implied behaviour on the landing bytes

* GCS: a contiguous single-line `X-Goog-Signature` of 64+ hex is detected in query, header (`:`), and
  JSON-key form, in lower and upper case; 63 hex is not; a percent-encoded parameter name is not (named
  limit); a line-wrapped value is not (F3, and the selftest asserts the miss); a Base64 value is not (S126
  shows hex only); the parameter name has no left boundary (F5).
* Azure: `sig=` beside `sv=YYYY-MM-DD` in one query is detected in either order with `&` and `&amp;`; with
  `\u0026` only when the starting parameter is the first one (F1); `%26` is never recognised (F6). The
  40-char floor admits 40/43/44-char values, raw and with `=`, `%3D`, `%2B`, `%2F` (a real Base64 HMAC-SHA256
  is 44 chars and hits). Intervening parameter *values* may contain `:`, `,`, and percent-encoded `%3A`,
  `%2F`, `%3D` (verified hit); parameter *names* must be 2–6 letters, at most 20 between the pair (F4).
  A non-Azure `sv=<date>&sig=<40 alnum>` hits (residual risk below).

## Findings

### F1 — High: `azure-sas-signature` misses `\u0026`-escaped SAS whenever the match-start parameter is not the first query parameter

At `b43dc215` (instrument lines 86–87):

```
rb"(?i)(?<![A-Za-z0-9_])(?:" + _SV + _PARAM + _SEP + _SIG + rb"|" + _SIG + _PARAM + _SEP + _SV + rb")"
```

The match must *start* at `sv=` or `sig=`, and the negative lookbehind rejects a start preceded by a word
character. `\u0026` ends in `6`, which is a word character: any `sv=`/`sig=` preceded by a `\u0026` escape cannot
start a match. `&` (ends `&`) and `&amp;` (ends `;`) are unaffected, so only the JSON-escaped form is broken,
and only when the starting parameter is not the first one (a `?` before it passes).

Consequence: the SAS URL printed in **S127:605** — `sp, st, se, sip, spr, sv, sr, sig` (sv is the sixth
parameter) — is missed entirely when a capture stores it JSON-escaped, which is the exact capture shape the
claim's `\u0026` clause promises to cover. Second failing order: `?sp=r\u0026sig=…\u0026sv=…`.

Evidence (`repro-review-c2.py`, run saved in `repro-output.txt`):

| case | observed | statement implies |
|---|---|---|
| `az_doc_order_u0026_f1` | `shapes=none` | `azure-sas-signature` |
| `az_sig_first_u0026_mid_f1` | `shapes=none` | `azure-sas-signature` |
| `az_sv_first_u0026_first_param_hit` | hit | hit |
| `az_sig_first_u0026_first_param_hit` | hit | hit |
| `az_doc_order_amp_hit`, `az_doc_order_ampamp_hit`, `az_sig_first_amp_mid_hit` | hit | hit |

Re-runnable:

```
python3 -B .ufo/waves/round-88/w1/ReviewC2Scanner-receipts/repro-review-c2.py /fast/scratch/hyaku/kasegi-r88/rc2 --only u0026
```

Fixture description: the S127:605 query string with every `&` replaced by the six-byte `\u0026` escape and the
44-character generated Base64 signature (digest `9fec33eb9033bce4`); and the same signature first, `\u0026`,
`sv=2022-11-02` last (digest `cbf3ed0b7493a80d`). The control case with raw `&` hits.

Fix direction: let the match start after a `\u0026` (and `%26`) escape, e.g. add those alternatives to the
lookbehind; `ReviewC2Scanner-receipts/fix-lookbehind.patch` is an illustrative one-line change that detects
both fixtures (`fix-detect-output.txt`), leaves the r86 oracle and K3 clean (hits=0), and still passes K1–K6
(`counter-fix-clone.txt`).

### F2 — Medium: the counter cannot see F1; K1/K4 avoid the failing position and K6 is candidate-independent

* K4's Azure plants: `corpus/practice/p/evidence/E1.txt` is sv-first with raw `&`; `w/z-receipts/live-c.json`
  is sig-first with `\u0026` but **sig is the first query parameter** (`?sig=`), so the lookbehind passes.
* The instrument selftest's `azure-json-escaped` is also sv-first; `azure-html-amp` is sv-first.
* Demonstrated: the landing (`counter-landing-clone.txt`, rev `b43dc215`) and the lookbehind mutant
  (`counter-fix-clone.txt`, rev `0fc7cd69`) both print `CAPABILITY-CHECK-RESULT pass rc=0`. A mutant that
  supports `\u0026` only in first-parameter position is indistinguishable from the landing and from the fix.
* The claimed 64-hex GCS floor is held by the sha pin, not by behaviour: K1's short case is 32 hex and K4's
  doc-wrapped run is 12 hex, so any threshold in 33..128 passes K1–K6 (the `gcs-threshold-12` control only
  catches ≤12).
* GCS colon/header form and Azure sig-first `&amp;` are exercised by the selftest only; K4 plants neither.
* K6 reads the fixed `BASE_REV` instrument bytes, so it is evidence about the base, not a discriminator for
  the candidate (claims.json says so; recorded so K6 is not over-read as coverage proof for the candidate).

Counter reproduction (F2, both runs print `CAPABILITY-CHECK-RESULT pass rc=0`):

```
S=/fast/scratch/hyaku/kasegi-r88/rc2
git clone --shared -q /home/vgpnk/Projects/shokunin/kasegi-shokunin "$S/clone"
git -C "$S/clone" checkout -q --detach b43dc2154bc09470da2209fb626021da3af3593e
python3 -B .ufo/waves/round-88/c2/capability-check.py --lane "$S/clone" --rev HEAD --work "$S/w1"
git -C "$S/clone" apply .ufo/waves/round-88/w1/ReviewC2Scanner-receipts/fix-lookbehind.patch
git -C "$S/clone" -c user.name=fixture -c user.email=fixture@invalid commit -qam mutant
python3 -B .ufo/waves/round-88/c2/capability-check.py --lane "$S/clone" --rev HEAD --work "$S/w2"
```

### F3 — Medium (documentation, security gate): "Known limits" omits the limits that matter for this round

The shape paragraph (instrument lines 37–42) and docstring restate the claim's `\u0026` clause, which F1
falsifies. The `Known limits` block (lines 43–45) names only GCS V2/CloudFront, percent-encoded parameter
names, and gzip/UTF-16/base64-wrapped captures. Unnamed, all verified below: the `\u0026`/`%26` position
interaction (F1, F6), the 20-parameter window and 2–6-letter parameter-name alphabet (F4), line-wrapped GCS
values (the selftest `gcs-doc-wrapped` asserts the miss, and S126:466–474's own example is wrapped), Base64
`X-Goog-Signature` values, a percent-encoded `=`, and the missing left boundary on the GCS parameter name (F5).

### F4 — Low: Azure matching is narrower than "in the same query"

`_SEP`/`_PARAM` (lines 79–80) allow at most 20 intervening parameters whose names are 2–6 ASCII letters
followed by `=`. `az_21_params_miss` (21 letter-named parameters between sv and sig) and `az_longname_between_miss`
(`x-ms-version=…` between them) are missed; `az_20_params_hit` hits. Real Azure-generated SAS queries stay
inside both bounds (all SAS parameter names are ≤6 letters), so the risk is captures/proxies that append
parameters before `sig`. The claim says only "in the same query".

### F5 — Low: GCS parameter has no left boundary

`X-Goog-Signature` matches inside a longer name: `Not-X-Goog-Signature=<128 hex>` hits
(`gcs_prefixed_name_fp`). False-positive surface only; the right side needs no boundary because a 64-hex
prefix of a longer run is still the signature.

### F6 — Low: `%26` separators are not recognised at all

`_SEP` is `&amp;|&|\u0026` (line 79); `az_sv_first_pct26_miss` does not match even with sv first. `%26` is not
in the claim's separator list and is not named as a limit. Fix alongside F1 if double-encoded captures are in
scope.

## (c) `corpus/practice/<pkg>/evidence/` scope — correct

`is_capture_path` (lines 124–129): `len(parts) >= 5 and parts[:2] == ["corpus", "practice"] and parts[3] == "evidence"`.
Verified: nested subdirectories under `evidence/` match; `corpus/practice/evidence/x.txt` does not;
`corpus/practice/<pkg>/report.md` does not; `evidenceX/` does not; `Evidence/` does not (case-sensitive);
the prefix is anchored at the path start (`.ufo/…/corpus/practice/…` is not matched by this clause).
The landing tree holds 9 files under two `evidence/` directories and K3 scans them (1414 files, hits=0,
allowed=18, unused_allow=0).

Adjacent note for the round's credential-hygiene rule: a seat report at
`.ufo/waves/round-88/w1/<seat>.md` is **not** capture-class under `--rev` (only `-receipts/` subtrees and
`live-*` files are), while `<seat>-receipts/` files are; `--files` covers everything named. A commit-time
scan of wave reports therefore needs `--files`, or the wave dir needs a scope clause.

## (d) Docstring honesty

Accurate: the two new shapes, their sources (S126:423–424/487–488, S127:402–404/605/638–639), the three named
limits, and the output contract ("never prints a matched value" — confirmed). Not honest enough: the
`\u0026`/either-order sentence overstates behaviour (F1), and the unnamed limits in F3 (line-wrap, window,
alphabet, `%26`, Base64 signature, no left boundary).

## (e) Do K4/K6 bind the new shapes?

Partly. K4 binds, with independent planted bytes: GCS query form (128 hex, `S004`), Azure sv-first with raw
`&` plus the practice-evidence scope (`E1`), STS token inside practice evidence (`E2`), Azure sig-first with
`\u0026` in first-parameter position (`live-c.json`), STS allowlist row refused (exit 2), `--files` with an
Azure hit against a documentation placeholder, and the negatives (non-capture `corpus/knowledge`, no-`sv`
SAS, placeholder, doc-wrapped GCS). It does **not** bind: `\u0026`/`%26` after a non-first parameter (F1/F6),
`&amp;` in sig-first order, the GCS colon form, the exact 64-hex floor, or the 20-parameter/name-alphabet
bounds. K6 binds nothing about the candidate by construction. See F2.

## Residual risks

* The 40-char floor admits non-Azure `sv=<date>&sig=<40 alnum>` (`az_nonazure_sv_sig_fp`); low, and the pair
  `sv=<date>`+`sig=` is distinctive.
* `NEVER_ALLOWED` still contains only `aws-sts-session-token`, so a digest-bound allowlist row can whitelist a
  live GCS/Azure signature. These are bearer credentials (S126:423–424; S127's only revocation is key
  rotation). Consider extending the policy in r89.
* The GCS hex restriction is example-derived: S126 prose names neither the encoding nor the length (the
  example at S126:466–474 is 512 hex, line-wrapped); the 64+ floor is a heuristic that also matches an RSA
  signature prefix.
* ReDoS: measured ~1.3 s/MB worst case on adversarial `&param=` chains (no catastrophic backtracking).

## Verification gaps

* `&amp;`, the GCS colon form, and the long-form GCS JSON key are exercised only by the instrument's own
  selftest (K1); no K4 plant repeats them.
* No live-target testing, no lane writes, no fleet census; findings are fixture-based on the frozen bytes.

## Files written

* `.ufo/waves/round-88/w1/ReviewC2Scanner.md` (this report)
* `.ufo/waves/round-88/w1/ReviewC2Scanner-receipts/repro-review-c2.py` (re-runnable fixtures)
* `.ufo/waves/round-88/w1/ReviewC2Scanner-receipts/repro-output.txt`
* `.ufo/waves/round-88/w1/ReviewC2Scanner-receipts/counter-landing-clone.txt`
* `.ufo/waves/round-88/w1/ReviewC2Scanner-receipts/counter-fix-clone.txt`
* `.ufo/waves/round-88/w1/ReviewC2Scanner-receipts/fix-lookbehind.patch`
* `.ufo/waves/round-88/w1/ReviewC2Scanner-receipts/fix-detect-output.txt`
