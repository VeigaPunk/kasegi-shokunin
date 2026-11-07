# ReviewC2Scanner — C2 `capture-secret-scan`: instrument, allowlist, counter

Reviewer seat: ReviewC2Scanner (round 87, attempt 1). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
C2 landing `132e16c588a2424c06b5ca15ea01fce1ee9a396d` (base `cd1f568a6be2656b5f5dc479eb90ef99b91131b5`, freeze `afb13a88e6fbc8e2f8a0c11f9cfbfde77e90769e`).
No lane file edited, nothing committed, no counter or instrument modified. All receipts beside this file under
`.ufo/waves/round-87/w1/ReviewC2Scanner-receipts/`.

**Verdict: CHANGES-REQUESTED** (routed defects for round 88). The frozen predicate is not falsified — see *Verified*.

## Verified at the landing commit

- **P1 reproduced.** `python3 -B .ufo/waves/round-87/c2/capability-check.py --lane . --rev 132e16c5… --work <scratch> --instrument-sha256 b2bf9d65e0a2bea99003ea7fdb3aec237449abb4ccd301f45b3ce496d161c6d1 --gate-sha256 8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6`
  → `CAPABILITY-CHECK-RESULT pass rc=0`; K2 `sts_files=2 oracle=2`, K3 `scanned=1319,hits=0,files=0,allowed=18,unused_allow=0`, K4 `missing=none extra=none sts_allow_rc=2`, K5 `rows=1`
  (`ReviewC2Scanner-receipts/landing-counter.txt`).
- **P2 byte equality.** `capture-secret-scan.py` = `b2bf9d65…c6d1`, `capture-secret-allow.tsv` = `f9fbd7e7…fc82`, counter = `4fba0cbe…ead7`, gate = `8b6f8493…c8e6`; all equal `claims.json` "instruments" and the frozen `c2/candidate/` bytes (checked with `sha256sum` + `git show 132e16c5:…`).
- **Coupling is correct.** `gate_patterns()` imports `SECRET_PATTERNS` from `claim-package-check.py` at run time, so the scanner's shape set is not self-contained; K1 pins *both* shas and the frozen invocation passes both. A pin on the scanner alone would not bind behaviour — this is the right choice and it is exercised.
- **Allowlist: all 17 rows are genuinely non-secrets** (full audit below). `allowed=18` with 17 rows is explained: one row's matched bytes occur twice in `gone.json` (lines 9983 and 10001).
- **No stale or out-of-scope allowlist row** at the landing commit (`unused_allow=0`), and no in-scope hit other than the four allowlisted files (my own value-free census: 1319 in-scope blobs).
- **Detected** (fixtures, all in scratch): JSON `\u0026` escapes, lower-case header names, header/query name split across a line break (the `\s*` after `:` spans `\r\n`), NUL-separated binary, and a 33 MiB capture (no size cap exists in code; value at line 3844779 was reported).
- **Receipts hygiene**: my own `-receipts/` directory was scanned with the frozen instrument → `hits=0 rc=0`.

## Findings

### F1 (High) — the capture scope is not where this lane stores fetched third-party bytes

`is_capture_path()` (`corpus/instruments/capture-secret-scan.py:98-102`) matches only
(a) `corpus/source-snapshots/`, (b) a directory segment ending in `-receipts`, (c) a basename starting `live-`.
At the landing commit that is **1319 in-scope blobs vs 15331 out of scope**, and these out-of-scope paths hold fetched third-party bytes:

| out-of-scope path | what it holds |
|---|---|
| `corpus/practice/curl-ibb-h1-1997312/evidence/` | 6 files (S120–S123 snapshots + manifest) — `S122.txt` is the **redacted copy of the round-86 leaked HackerOne report**, i.e. the incident's own evidence directory |
| `corpus/practice/curl-h1-1913733/evidence/` | 5 files (S119–S121 + manifest) |
| `.ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312/` | candidate package + evidence copies |
| `.ufo/waves/{round-28/wave1/ScribeLessonGate,round-29/wave1/assimilation/fetch,round-30/wave1/fetch,round-31/wave1/ScoutMSVR-scratch,round-59/controls,round-68/w1/ScoutS102,round-73/w1/K73ScoutCapture,round-74/w1}/` | 15 tracked files that begin with an HTTP status line / `<!DOCTYPE html>` / `<html` |
| `.ufo/waves/<round>/w1/*.md` (seat reports written beside, not inside, `<seat>-receipts/`) | e.g. `.ufo/waves/round-86/w1/CriticClaims.md` |
| `.ufo/waves/**/receipts/` (no dash; ~20 dirs, ~1000 files, e.g. `round-67/w1/ExecMultiHeadDriver/receipts/{base,candidate}`) | seat outputs; the SCORECARD row says "seat receipts" are covered but only `<name>-receipts/` is |

Consequence: the r86 defect would be caught at its historical path (`-receipts/` + `live-`), but the *same bytes* committed under
`corpus/practice/<pkg>/evidence/` — which is exactly where the redacted copy lives now, and where every future practice package will put its captures —
are never read by `--rev`. `--files` can scan them, but nothing forces it and the SCORECARD row's `--rev master` demonstration implies total coverage.

Reproduce (fixture repo, one fake STS-shaped value per path; `--rev` reports only 4 of 12 paths):
`python3 -B .ufo/waves/round-87/w1/ReviewC2Scanner-receipts/regen-fixtures.py <scratch> <inst-dir>` → *scope battery* section of
`ReviewC2Scanner-receipts/fn-battery.txt`; inventory in `ReviewC2Scanner-receipts/capture-inventory.txt`.

### F2 (High) — detection misses structured-JSON, percent-encoded-name and non-text captures

Fixtures + actual output in `ReviewC2Scanner-receipts/fn-battery.txt` (`--files` mode, rc 1 = HIT, rc 0 = **missed**):

| fixture | result |
|---|---|
| HAR-style `{"name":"X-Amz-Security-Token","value":"<value>"}` (compact and pretty) | **clean** — both shapes require the value to follow the name through `=`/`:`; the `","` separator defeats both |
| parameter name percent-encoded (`X-Amz-Security-Token%3D<value>`, single and double-encoded URL) | **clean** |
| UTF-16LE capture (BOM) | **clean** |
| gzip-compressed response body | **clean** |
| base64-wrapped capture (`.b64` dump) | **clean** |
| JSON-escaped `/` inside the value with the first slash inside the first 20 chars | **clean** (see F7) |

Calibration: the lane currently tracks **0** `.har` files and `X-Amz-Security-Token%3D` appears only in the round-87 spec/dispatch files, so today's exposure is nil.
But the capability exists to screen captures fetched from arbitrary APIs, and the one real incident was a **JSON** capture; a JSON receipt that stores query parameters as name/value pairs (HAR, Playwright trace, most API redaction receipts) is the obvious next shape.

### F3 (Medium) — the counter never exercises `--files`, the mode the defect class needs

K1–K5 call the instrument only with `--selftest` and `--lane/--rev` (`capability-check.py:155,164,172,185,189`). The pre-commit mode documented in the instrument's own docstring ("run it on every capture before the commit") has **zero behavioural coverage**.

Demonstration: mutant A+D = `scan_files()` replaced by an always-clean stub **and** `selftest()` replaced by printing `SELFTEST-RESULT pass` (`ReviewC2Scanner-receipts/mutant-A-D.patch.b64`, decode with `base64 -d … | git apply` inside a `git clone --shared` of the lane).
`python3 -B .ufo/waves/round-87/c2/capability-check.py --lane <clone> --rev 1ba403e7… --work <scratch>` → **`CAPABILITY-CHECK-RESULT pass rc=0`, all five limbs pass** (`ReviewC2Scanner-receipts/counter-soundness.txt`).
The same instrument reports `hits=0 rc=0` on a capture that carries the live shape. Under the frozen invocation (with both sha pins) it fails **only** K1 on sha — i.e. the pin proves identity, never behaviour; nothing in K1–K5 distinguishes a working `--files` from an inert one.

### F4 (Medium-low) — header/JSON-key STS forms are attested only by the instrument's own selftest

K2's oracle is a `git grep` for the query-string form only (`capability-check.py:49`), and K4's plants contain only the query-string form (`PLANTS[corpus/source-snapshots/round-1/S001.txt]`).
Mutant B = the STS regex narrowed to the `=` form with its header/JSON selftest cases deleted (`mutant-B.patch.b64`) → **all five limbs pass, rc=0** without pins; with pins it fails only on sha.
Today the real instrument is still safe on header forms because the gate's generic `credential` shape happens to match `token: <value>` / `token": "<value>"` — but that is incidental redundancy the counter cannot see, and a future edit could remove one of the two branches and still pass.

### F5 (Medium-low) — allowlist rows are keyed to the literal path argument under `--files`

`scan_files()` passes the argument string through as the allow key, so a row written repo-relative only matches a repo-relative invocation
(`ReviewC2Scanner-receipts/fn-battery.txt`, *allowlist path form*):

- `--files .ufo/waves/round-87/w1/X-receipts/fp.json` from the repo root → `hits=0 rc=0`
- `--files ./.ufo/.../fp.json` → `hits=1 rc=1`
- `--files /abs/path/.ufo/.../fp.json` → `hits=1 rc=1`

Fails safe, but `find`, `xargs` with absolute paths, and editor integrations all produce the noisy form; a gate that cries wolf on already-adjudicated non-secrets invites the shortcut that caused M86-2.

### F6 (Low) — "one exact matched value" is approximate: binding is to the matched *bytes*, truncated

The docstring (`:32-37`) says a row binds one exact matched value. The digest is over the matched bytes, and the gate shapes truncate at the first character outside their class:

- S124 `authorization` rows (`9cb06f6f…`, `af714e42…`) bind the scheme token only (`AWS4-HMAC-SHA256`, 16 bytes). Demonstrated: an `authorization` header at that path with a **different** key id in the same scheme line is allowed (`hits=0 allowed=1`); it was still caught by `aws-access-key-id`, so defence in depth holds for AKIA/ASIA, but any non-AKIA credential in a SigV4 header at that path would pass on the `authorization` shape.
- `gone.json`/`hunt2.json` rows bind the lane-name prefix before the first `/`; a different value sharing that prefix is allowed (demonstrated: value `…-skeleton/v2` → `hits=0 allowed=1`).

Low risk (prefix must match 16+ chars) but the docstring's exactness claim should be corrected; the honest statement is "a row binds the exact matched byte string, which is a prefix of the value for values containing characters outside the shape's class".

### F7 (Low) — JSON `\/` escaping inside the value can defeat both shapes

If a writer escapes `/` inside the token value and the token's first `/` falls within the first 20 characters, both shapes stop short of the 16/20-char threshold: fixture `json escaped slash at char 10` → **clean**; at char >20 → hit (`fn-battery.txt`). Real STS tokens start with the fixed `IQoJb3JpZ2luX2Vj…` prefix and rarely carry `/` that early, so this is narrow.

### F8 (Low) — `--rev` never reads mode-120000 entries

`tree_blobs()` skips symlinks. For git a symlink blob holds only the target path, so nothing leaks from the link itself; but a capture committed as a symlink to an **in-repo, out-of-scope** path is never scanned (fixture: `corpus/source-snapshots/round-1/link.txt` → target `w/receipts/target.json` → neither read). Document it or resolve-and-scan.

## Allowlist audit — every row read in context at 132e16c5

Full resolution (row → matched line(s), matched-byte length, class) in `ReviewC2Scanner-receipts/allowlist-audit.txt`. No values recorded (hygiene).

| rows | path | shape | judgement |
|---|---|---|---|
| 13 | `.ufo/waves/round-85/w1/ExecC1Hunt-receipts/gone.json` | credential | **correct**: JSON key `token` holds a citation-hunt name (`…-skeleton/v1`, `custodian-receipts`, `submission-review`, engagement/cycle names). In context (lines 7305–10001) the key is a hunt-token field, not a credential. Reasons accurate |
| 1 | `…/hunt2.json` | credential | **correct**, same value as a gone.json row at a different path (path-bound, `:36-37` holds) |
| 1 | `corpus/source-snapshots/round-49/S078.txt` | credential | **correct**: CVE Services OpenAPI example, key `secret`, value `12345-abcde-67890` (line 4223, surrounded by `jdoe`/UUID example fields). Reason accurate |
| 2 | `corpus/source-snapshots/round-87/S124.txt` | authorization | **correct as a non-secret** (SigV4 doc example, lines 384/394; the key id is the documented `AKIAIOSFODNN7EXAMPLE`, which `ALLOWED_VALUES` already skips). Reason accurate; see F6 on binding breadth |

All 17 rows are consumed at the landing commit (`unused_allow=0`), none is out of scope, none is for a refused shape (`load_allow` refuses `aws-sts-session-token` rows, `:79-81`; K4 confirms exit 2).

## Counter soundness — can a lying instrument pass K1–K5?

- **Without the sha pins**: yes, twice (mutants A+D and B, both `rc=0`). K1's selftest check is a substring in output the instrument itself authors, and K2/K3/K4 use only `--rev`.
- **With the frozen invocation's pins**: substitution is blocked (sha), and K4's plant set does constrain real query-form detection plus exact-value allow semantics (the r87 control battery's forgeries fail K2/K3/K4 — reproduced shape in `controls/c2-controls-r87.txt`). Residual: the pins are computed from whatever landed, so the pin check is circular w.r.t. behaviour; K2–K4 are the only independent checks and they cover neither `--files` (F3) nor header/JSON forms (F4).
- K2's oracle is a literal `git grep` (`-E`, query form). At `252df0c9` it agrees with the instrument (2 files, both expected). A future capture-class binary blob containing the value would be hit by the instrument and missed by the oracle → K2 would fail on a correct instrument; nothing at the frozen rev triggers it.

## Residual risk and verification gaps

- Scope counts come from `git ls-tree` + the instrument's own `is_capture_path`; the fetched-body census is a literal first-line grep (not semantic proof of every third-party byte), and it cannot see credential shapes outside the instrument's six gate shapes + two AWS shapes.
- No live token was copied into scratch; K2 was re-run, not re-derived.
- Mutants were evaluated on a `git clone --shared` in scratch (they cannot exist at the frozen rev by construction); the frozen instrument's `--files` behaviour was exercised directly (F2/F5/F6 fixtures) and does work for text, repo-relative, unescaped captures.
- Not run: full `resolve.py` census (forbidden by the lane contract), live targets (refused by PROVINCE.md).

## Verdict

**CHANGES-REQUESTED.** The frozen C2 predicates hold (P1 `CAPABILITY-CHECK-RESULT pass rc=0`, P2 byte equality) and the allowlist is sound — nothing here re-scores the claim.
Round-88 routed defects, in priority order: **F1** widen `is_capture_path` to `corpus/practice/*/evidence/`, `…/fetch/`, `*-evidence/`, `receipts/` and wave-level `w1/*.md` (or require `--files` in the seat contract); **F2** add a structured name/value shape and a decoding step (gzip/UTF-16/base64) for captures; **F3** add a K6 limb that runs `--files` on a planted capture and requires a hit, plus a selftest that cannot pass by printing its own verdict; **F4** plant one header-form and one JSON-key-form value in K4; **F5** normalise `--files` paths to repo-relative before allow lookup; **F6** correct the docstring's exactness claim or bind rows to the full value.
