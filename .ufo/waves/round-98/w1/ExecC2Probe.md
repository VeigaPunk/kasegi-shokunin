# ExecC2Probe — independent nine-shape probe of the C2 landing

Seat: ExecC2Probe (read-only attacker/verifier, round-98 w1, KasegiR98 wave). 2026-11-07.
Target: `corpus/instruments/capture-secret-scan.py` at the C2 landing `e2caf4a1561b544a6ea684b0bcfa975f7e7f6061`; before-state `a9a53608`.

## Environment and tooling

- python3 3.14.8, git 2.56.0 (system). **No tools installed or upgraded; no pacman transaction touched** (host-wide pause respected). Scratch `S=/fast/scratch/hyaku/kasegi-r98/ExecC2Probe`, removed before this report was finalized; receipts were copied out first.
- Both instrument revisions extracted with `git show REV:corpus/instruments/capture-secret-scan.py` into `$S/landed/` and `$S/r97/` (zero clones, zero mirrors, no lane writes). The gate module `claim-package-check.py` was extracted beside each copy at the SAME revision, because `patterns()` imports `SECRET_PATTERNS` from the file beside the script (`capture-secret-scan.py:493-499`, `gate_patterns()`).
- No `--allow` was passed and no `capture-secret-allow.tsv` was placed beside the copies, so both runs scanned with an empty allowlist (`allowed=0 unused_allow=0` in both summary lines). The lane does carry `corpus/instruments/capture-secret-allow.tsv`; the allow key is `(path, shape, sha256)` and every fixture path is nonce-derived, so no allow row could have collided either way.
- Sanity: `git diff --stat e2caf4a1 HEAD -- corpus/instruments/capture-secret-scan.py` is **empty** — the C1 landing (HEAD `e2d3de7b`) did not touch the instrument, so the extracted landing bytes are the bytes the wave's tree carries.
- Selftests, run by me on the extracted copies: landing `SELFTEST-RESULT pass cases=170` (rc 0), r97 `SELFTEST-RESULT pass cases=148` (rc 0) — the frozen 148 → 170 step reproduced independently (receipts `selftest-landed.out`, `selftest-r97.out`).

## Method

My own fixture generator (`gen.py`, not the gate's; receipts carry it in full):

- 43 fixtures in a scratch git repo (`$S/fx`, HEAD `09840277dda9e2696cf246a0a30c5e0816ff2ed0`, 43 files, `git rev-parse --show-toplevel` asserted equal to the repo dir before the first commit, `git status --porcelain` asserted clean after).
- Nonce-derived paths (`c98/<4-byte-hex>-<family>-<variant>.txt`).
- **22 positives** — note: the seat brief says "21 positives (four new shapes x 3 variants, five widened shapes x 2 boundary variants)"; that arithmetic is 22, and I built all 22 named variants rather than dropping one.
- **21 boundary negatives** (15 family-specific + 6 cross-shape), plus an **8-file edge annex** (`edges.py`, repo `$S/fx-edge`) probing the exact boundary semantics.
- Every plant value is generated from its rule's own grammar (`[A-Za-z0-9]`, `[A-Za-z0-9_-]`, `[0-9a-f]`) with a deterministic per-fixture seed (`sha256("ExecC2Probe|<family>|<variant>")[:12]`) — **never copied from the instrument's selftest**, whose `b"A"*43`-style literals my values share no alphabet-run with.
- Every value is scrubbed against a 32-entry marker list (all `gl*` prefixes, `GR1348941`, `feed_token`, `_gitlab_session`, `eyJ`, `AKIA`/`ASIA`, `gh[pousr]_`, `op://`, `bearer`; `FORBIDDEN.json`) so that any hit outside the expected set is instrument behaviour, not generator noise. Context lines avoid every gate keyword (`(?i)\b(token|secret|password|api[_-]?key)\b\s*[:=]`, `bearer`, `authorization`, `session[_-]?cookie`) — note `feed_token=` is safe against the gate's `\btoken\b` because `_`/`t` are both word chars, so no boundary exists.
- Expected sets were hand-derived from the grammar, then compared against observed `HIT shape=... path=... line=...` output of `--files` runs. Per the wave's structural-redaction convention (R146; the landing itself redacted the round-94 receipt's fixture literal), fixture bytes are not reproduced in receipts; receipts carry the generators, seeds, sha256 of every fixture, and both raw scan outputs, so every file is byte-exact regenerable.

## Results at the C2 landing (`e2caf4a1`)

`CAPTURE-SECRET-SCAN mode=files scanned=43 hits=23 files=23 allowed=0 unused_allow=0 rc=1` — **zero misses, zero extra hits** (`SUMMARY ok=43 miss-files=0 extra-files=0`; full matrix in receipts `landed.out`):

- **Four new shapes, 12/12 positives**, each hitting exactly its one shape:
  - `gitlab-ci-build-token` (rule at `capture-secret-scan.py:302-303`): `glcbt-<4 alnum>_<20 word>`; `glcbt-<1>_<20>`; `glcbt-<5>_<20>_x` (its own `(?![A-Za-z0-9])` boundary accepting a trailing `_` before a letter).
  - `gitlab-iam-refresh-token` (`:304-305`): `<43 word>.<43 word>` plain, JSON value, and trailing `.more` (punct right side hits, per `(?![A-Za-z0-9_-])`).
  - `gitlab-iam-authorization-code` (`:306-307`): `;`-terminated, `_`/`-`-containing segments, bare EOL — all hit.
  - `gitlab-session-cookie` (`:308-310`): `Cookie: _gitlab_session=<64 lc hex>; Path=/`, quoted `cell-42-` form, and the `_geo_<64hex>=<64hex>` form — all hit.
- **Five widened boundaries, 10/10 positives** (`:311-321`; old `(?![A-Za-z0-9_-])` → new `(?![A-Za-z0-9])`): `GR1348941…`, `feed_token=…`, `gloas-…`, `glft-…`, `glsoat-…` each followed by `_x` and by `-x` now hit their single shape — exactly the SentinelShapes MUST-FIX 1 class.
- **21/21 negatives silent** at both revisions: `glcbt-` 6-char prefix (backtracking cannot place `_`), 19-char payload, 21-alnum no-underscore; iam 42/44 segments, no-dot 86-mer, `_x` after a full token (the new iam pair kept the word-strict right boundary — the punct widening was scoped to the five round-97 shapes only, as the diff states); session 63-hex, no separator, uppercase hex, `gitlab_session=` without the leading `_`, `_geo_<64>=<63>`, `cell-` without digits; runner-registration + `a`, feed-token 19, `gloas-`+`9`, `glft-`+`A`, `glsoat-` 19, `feed_token` without `=`; cross-shape `gliamrt-<43>_<43>`.
- **Cross-shape containment**: `glcbt-eyJ…` hits `gitlab-jwt-token` only — the new ci-build rule does not claim JWT-shaped strings ({1,5} alnum then `_` cannot consume `eyJ.`).

## Before-state (`a9a53608`) over the same 43 files

`CAPTURE-SECRET-SCAN mode=files scanned=43 hits=1 files=1 … rc=1` — r97 misses **all 22 nine-shape positives**:

- all four new shapes (rules absent; nothing else claims the strings): 12/12 missed;
- all five widened shapes at `_x`/`-x` (the old `(?![A-Za-z0-9_-])` right boundary refuses a real token followed by `_` or `-`): 10/10 missed.

The single r97 hit is the deliberate pre-existing-family control (`gitlab-jwt-token` on the `glcbt-eyJ…` file), plus the two edge files whose right sides are legal under the old boundary too (below). This is the measured gap the landing closes.

## Edge annex (8 files, both revisions)

`EDGE-SUMMARY pass files=8` (receipts `landed-edge.out`, `r97-edge.out`):

1. `_gitlab_session=<64hex>_x` → **hit** at the landing: the session rule's right boundary is hex-strict (`(?![0-9a-f])`), so `_` after the value still hits — consistent with S140's class as implemented, and deliberately unlike the five widened shapes.
2. `_gitlab_session\n<64hex>` → **hit**: `[\s"'\=:;]+` spans a newline, so the keyword line and the value line are one match (reported at the keyword's line). S140-faithful as coded; noted as FP surface, not a defect.
3. `glcbt-<4>_<21 alnum>` → silent: a 21st alphanumeric payload char refuses; only `_`/`-`/punct/EOL pass.
4. `glcbt-<5>_<20>-` → hit: trailing `-` passes the ci-build boundary.
5. `gliamrt-<43>.<43>_x` → silent: the four new rules did not receive the boundary widening.
6. `-GR1348941…` (hyphen directly before the token, EOL after) → hit at BOTH revisions: the shared `_GL_LB` (`capture-secret-scan.py:284`) accepts any non-`[A-Za-z0-9_]` char — including `-` — before a token; behaviour inherited, not new.
7. `_gitlab_session=<65 hex>` → silent.
8. `gloas-<64>.more` → hit at both revisions (dot was always legal on the right).

## Observations (non-blocking)

- `python3 landed/capture-secret-scan.py --selftest` emits `SyntaxWarning: "\-" is an invalid escape sequence` at `capture-secret-scan.py:184` — the new docstring line `(S140 line 480), right boundary `[^0-9a-zA-Z_\-]`/EOL.` sits in a non-raw docstring. Cosmetic (stderr only, zero effect on matching; the r97 copy does not warn). A one-byte fix (`\-` → `\\-` or a raw docstring) if anyone cares.
- The landing's diff and my probe agree line-for-line: new rules at `:302-310`, widened at `:311-321`, selftest cases `:613-637`.

## Verdicts

VERDICT: C2 four new S140 shapes (gitlab-ci-build-token, gitlab-iam-refresh-token, gitlab-iam-authorization-code, gitlab-session-cookie) at e2caf4a1 — CONFIRMED: 12/12 grammar-derived positives hit exactly their one shape, 15/15 crafted family negatives and all cross-shape negatives stay silent, 0 extra hits.
VERDICT: C2 five widened right boundaries at e2caf4a1 — CONFIRMED: 10/10 `token_x`/`token-x` positives now hit; alnum/digit/uppercase suffixes and length violations still refuse; the widening is correctly scoped to exactly the five round-97 shapes.
VERDICT: before-state a9a53608 — CONFIRMED: misses 22/22 nine-shape positives over identical files (hits=1, the pre-existing jwt family on a deliberate cross file); this is the measured before of the frozen 148 → 170 step (selftests independently reproduced: 148 and 170, both pass).
VERDICT: false-positive safety of the landing — CONFIRMED: 0 unexpected shapes across 43 + 8 files at the landing (29 total hits, every one hand-expected).
