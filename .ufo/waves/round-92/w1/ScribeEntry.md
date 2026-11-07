# ScribeEntry — round 92, wave 1, attempt 1

**Seat:** ScribeEntry (leaf, non-author). **Assignment:** draft the `corpus/knowledge/` entry *GitHub prefixed tokens in captured evidence* as a candidate in the wave directory; the L1 decides admission. **Scope guard:** no `corpus/` edit, no SCORECARD/SOURCES/LOG edit, no instrument edit, no git/jj write, no network, no delegation, no background job.

## Verdict

Delivered. One candidate knowledge entry at `.ufo/waves/round-92/w1/candidate-knowledge-github-prefixed-tokens.md` (299 lines, 39,014 bytes, sha256 `4f639a18498b0f7b83b9fbebc9c70ceedcfb3184394f695c2253b9b3dc17ccee`), every fact anchored to S136/S137 (`corpus/source-snapshots/round-92/`) or to the landed scanner at `58c0c115`; 17 block quotes all verbatim and ≤25 words; seven check blocks (FC-1, FC-1b, FC-2 … FC-6) run with measured output pasted.

## Behavior — what the entry says

- **Claim 1** prefix rule (`S136.txt:158`), the blog's three-letter-prefix design and `_` separator (`S137.txt:156`, `:162`), the five classic prefixes (`S137.txt:157-161`; `S136.txt:161-167`) and the sixth, fine-grained prefix (`S136.txt:163`) as a limit rather than a covered case. GitHub's 0.5% expectation is read as a prefix-only floor (`S137.txt:164`).
- **Claim 2** 30 base62 positions (`S137.txt:173`) + 6-character checksum (`S137.txt:167`) = 36 after the prefix; 4 + 36 = 40 (`S136.txt:160`); length unchanged (`S137.txt:174`); offline checksum ≠ liveness.
- **Claim 3** stateless `ghs_APPID_JWT` rollout from 2026-04-27 (`S136.txt:160`); the scanner's branch: `ghs_` + 1–20 digits + `_` + three dotted base64url segments of 10+ (`capture-secret-scan.py:157`, `:160-161`), left boundary shared (`:156`).
- **Claim 4** why a capture holding one is treated as a live grant: the token is entered where a password would be (`S136.txt:150`) and GitHub's remedy is a reset by the holder (`S137.txt:177`), not expiry; neither page states a lifetime, so the rule is explicitly treat-as-live, not measured-live.
- **Claim 5** what the landed scanner detects and where (`:14-21`, `:81-94`, `:156-162`, `:198-203`, output at `:114-119`/`:256-268`, selftest `:341-355`).
- **Claim 6** a placeholder-free Known-limits list drawn **only** from the docstring: fine-grained `github_pat_` (`:95-96`), values split across lines and wrapped/encoded captures (`:100-102`), percent-encoded prefix bytes (docstring's percent limit at `:97-99`, marked as the entry's reading); plus the three shape boundaries the selftest pins (`:87-89`, `:348-355`).
- **Claim 7** operator checklist: scan with `--files` before the first commit (`:19-21`); digest-bound allowlist rows only (`:105-112`, `:168-183`, `:214-221`, refused rows exit 2 at `:179-181`, `aws-sts-session-token` never allowed at `:164`); never print a value (`:114-119`); on a hit reset with the owner then redact with a pre-redaction digest (model `corpus/source-snapshots/round-86/manifest.json:47-54`); read a clean run as a shape statement.
- Shape followed from `corpus/knowledge/cloud-signed-cookies-and-user-bound-sas.md`: H1, then `source:` / `verified-at:` / `recheck:` as three consecutive lines (Q1), Attribution, numbered Claims, "How a researcher uses this", Falsifiable rule + FC-n checks with measured output, Rejected over-generalizations, Honest limit.

## Gates (measured, receipts in `ScribeEntry-receipts/checks.txt`)

| gate | command | result |
|---|---|---|
| quote anchors, assigned `--rev` form | `quote-anchor-check.py --lane <lane> --rev 58c0c115 …candidate…` | `QUOTE-ANCHOR checked=0 bad=0 cites=0 out_of_range=0` rc 0 — **vacuous**, see finding F2 |
| quote anchors, landed-tree form | `git archive 58c0c115 \| tar -x -C $T`, candidate copied in, same tool `--lane $T` | `QUOTE-ANCHOR checked=17 bad=0 cites=81 out_of_range=0` rc 0 |
| 25-word cap | inline counter over `^> "…" — \`PATH:N\`` | `QUOTE-WORDS quotes=17 bad=0` rc 0 (widest = `S137.txt:156` at exactly 25) |
| capture digests + manifest | `sha256sum`; `source-recheck.py --source S136/S137` | `f0edd23c8d6d…`, `e4aaf2280203…`; 7 `OK` lines, both rc 0 |
| captures clean | `capture-secret-scan.py --files S136 S137` | `scanned=2 hits=0 files=0 allowed=0 unused_allow=19 rc=0` |
| shape load-bearing (FC-3) | landed vs `0628fd24` instrument, 3 scratch fixtures | landed 3× `hits=1 rc=1`; base 3× `hits=0 rc=0` |
| selftest (FC-4) | `--selftest \| grep '^SELFTEST gh-\|^SELFTEST-RESULT'` | 15 lines (6 hits, 9 `none`), `SELFTEST-RESULT pass cases=68` |
| limits (FC-5) | 8 scratch fixtures against the landed instrument | 7 clean (`github_pat_`, 35, 37, `GHP_`, bare, doc placeholder, percent-encoded); `K-4seg` hits |
| instrument identity (FC-6) | `git show <rev>:…certificate… \| sha256sum`, `grep -c github-token` at base | `04666f67…` / `89e283c6…` / `0` |
| hygiene of the candidate | `capture-secret-scan.py --files <candidate> <receipt>` | `scanned=2 hits=0 … rc=0`; a broad `grep -E 'gh[pousr]_[A-Za-z0-9]{20,}\|github_pat_[A-Za-z0-9_]{20,}\|ghs_[0-9]{1,20}_[A-Za-z0-9_-]{10,}'` on the candidate exits 1 |
| recheck line | `bash -n` and `bash -c` from `/tmp` | parse ok, rc 0 (Q10 / R33 shape: one command, `cd <lane-root> &&` prefix) |

Quality criteria Q1–Q6 are met as far as a candidate can: Q1 three header lines with anchors and a runnable recheck; Q2 both sources tier A, opened this round; Q3 17 verbatim quotes ≤25 words with line anchors; Q4 vendor positions attributed and the scanner's choices labelled as lane design; Q5 falsifiable rules + 8 rejected over-generalizations; Q6 documentation only, no credential material (scan clean).

## Touched surfaces

- Written (only these): `.ufo/waves/round-92/w1/candidate-knowledge-github-prefixed-tokens.md`, `.ufo/waves/round-92/w1/ScribeEntry-receipts/checks.txt` (sha256 `5362e42c799e57fbb69217e7f2db80040eaa0601438cd8d65c1ab2216a5f6910`).
- Read-only: `corpus/source-snapshots/round-92/{S136,S137,S138}.txt`, `manifest.json`, `corpus/instruments/{capture-secret-scan,claim-package-check,source-recheck}.py` (working tree and via `git show`), `corpus/knowledge/cloud-signed-cookies-and-user-bound-sas.md`, `corpus/SOURCES.md:148-150`, `corpus/QUALITY.md`, `.ufo/waves/round-92/{claims.json,l1/quote-anchor-r92.txt}`, `git log`.
- Nothing under `corpus/`, `.ufo/state/`, `templates/`, `scripts/`, the frozen `c1/ c2/ controls/ l1/` bytes, or any instrument was modified. No git/jj writes.
- Scratch `/fast/scratch/hyaku/kasegi-r92/ScribeEntry` (extracted instruments, a `git archive` of `58c0c115`, fixtures) **deleted before yield**. No `__pycache__` written (`python3 -B` throughout); no pacman/uv/npx/install of any kind (no tool change to report).

## Findings — routed, never re-scoring

**F1 (C2 qualifier, over-match).** The stateless branch carries no right boundary. Bytes: `_GH_LB + rb"(?:gh[pousr]_[A-Za-z0-9]{36}(?![A-Za-z0-9_])|ghs_[0-9]{1,20}_" + _JWT_SEG + rb"\." + _JWT_SEG + rb"\." + _JWT_SEG + rb")"` (`corpus/instruments/capture-secret-scan.py:160-161`): the classic alternative ends with a negative lookahead, the stateless alternative does not. Re-runnable: write `ghs_123456_` + three 10+-char base64url segments + `.ZZZZZZZZZZ` to a scratch file and run `python3 -B corpus/instruments/capture-secret-scan.py --files <file>` → `HIT shape=github-token … hits=1 rc=1` (receipt §7, `K-4seg`). Effect is a widening only (it cannot hide a token); it can flag a longer dotted string on its first three segments. The entry records it in Claim 3 and rejected over-generalization 6; the predicate set (K1–K8) does not test it.

**F2 (method, for the L1's receipt).** The assigned command form `quote-anchor-check.py --rev <rev> <candidate>` prints `checked=0 bad=0 cites=0` for a wave-dir candidate, because the tool loads the **entry** with `git show REV:ENTRY`; an uncommitted candidate is absent at the rev, so no line is inspected and the run is vacuous rather than passing. The non-vacuous equivalent is `git archive <rev> | tar -x -C $T`, copy the candidate into `$T`, then `--lane $T` (receipt §2; `checked=17 bad=0 cites=81`). This does not affect the L1's own `--rev` run over committed entries (`.ufo/waves/round-92/l1/quote-anchor-r92.txt`), only candidates. Suggested for the next round: have the tool read the entry from the working tree when it is absent at `--rev`, or accept an explicit `--entry-from-worktree`.

**F3 (coverage gap, C2-shaped).** Neither the capture scan nor the gate reaches a bare prefixed token outside capture-class paths. `is_capture_path` (`corpus/instruments/capture-secret-scan.py:198-203`) excludes `corpus/knowledge/` and `corpus/lessons/`; the gate's `SECRET_PATTERNS` are keyed by an adjacent parameter name (`corpus/instruments/claim-package-check.py:135-142`), and `capture-secret-scan` adds `github-token` only to its own tuple (`:158-162`, `:194-195`), not to the imported gate tuple. So a token pasted into a knowledge entry or a lesson has no detector at all. Re-runnable: paste a synthetic 36-base62 tail after `ghp_` into a scratch file under a non-capture path and run `--rev` → `hits=0`; run the gate's `R-NOSECRET` on the same file → `hits=0`. The entry states the fact (Claim 5, rejected 8); a shape change is out of this seat's scope.

**F4 (source unbounded field).** The application-id bound in the stateless branch (`[0-9]{1,20}`, `:160`) is a lane choice with no source behind it: S136 writes the placeholder `ghs_APPID_JWT` and says only that the format is stateless (`corpus/source-snapshots/round-92/S136.txt:160`). Neither opened source states an app-id digit count, so the 20-digit cap is unsourced (unlike the 1–20 bound's companion, the 36 base62 characters, which S137 gives). The entry states the bound as the instrument's clause, not as a vendor fact.

**F5 (docstring/branch asymmetry, cosmetic).** The docstring admits the stateless form by `ghs_<APPID>_<JWT>` (`:90-92`) while the regex requires digits for the app id (`:160`); a real app-id that is not purely numeric would read clean. No source settles whether an app id can be non-numeric, so this is recorded as a qualifier, not a defect claim.

## Conflicts, verbatim

1. **Prefix spelling.** S137 (design, 2021, updated 2023): `ghp for GitHub personal access tokens` … `Thus, we are adding a separator: _.` (`corpus/source-snapshots/round-92/S137.txt:157`, `:162`). S136 (current docs): the table cells read `Personal access token (classic)ghp_Managing your personal access tokens` (`corpus/source-snapshots/round-92/S136.txt:162`). No contradiction: the blog states the design in two sentences, the docs the joined form in one table cell. The entry cites both and says so.
2. **Length.** S136: `If your application expects or relies on installation tokens being exactly 40 characters long, it may not handle this new token format correctly.` (`S136.txt:160`). S137: `all without changing the token length` (`S137.txt:174`). The 40-character statement is scoped to installation tokens before the stateless rollout; the entry reads 40 as the classic length (4 + 36) and names the stateless form as the exception, exactly as S136 does.
3. **`github_pat_` in the prefix list vs in the known limits.** S136 lists it in the same table as the five (`S136.txt:163`); the instrument's docstring lists it as a limit (`capture-secret-scan.py:95-96`). Not a contradiction of fact — a documented prefix the shape does not match — and the entry states it in both places.

## Out of scope / not claimed

- No admission: the entry is a candidate; `corpus/knowledge/` is untouched and the L1 decides.
- No registry work: `corpus/SOURCES.md:148-149` stay `queued` with `used-by —`; the L1's integration step owns the status change.
- No SCORECARD/SKILL/PROVINCE/LOG edit; no citation of the round-92 capability row (I did not open it, so did not cite it).
- No re-scoring of C1 or C2: I ran neither `knowledge-meter.py` nor `capability-check.py`, made no resolve census, and state no score. Every instrument fact in the entry is about `capture-secret-scan.py` at `58c0c115`.
- No network request: all sources are pinned captures; the entry's fixtures are generated in scratch and deleted; receipts carry digests and `HIT`/summary lines only, never fixture bytes.
- One process deviation to disclose: six scanner line-anchor repairs were applied with a small in-place Python replacement instead of the `edit` tool. Result verified by the quote-anchor run (`bad=0`); no other file was affected.

## Artifacts

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-92/w1/candidate-knowledge-github-prefixed-tokens.md`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-92/w1/ScribeEntry-receipts/checks.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-92/w1/ScribeEntry.md` (this report)
