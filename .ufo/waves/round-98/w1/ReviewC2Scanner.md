# ReviewC2Scanner — C2 landing `e2caf4a1`, capture-secret-scan round-98 shapes

Seat: ReviewC2Scanner (leaf, read-only). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Reviewed revision: `e2caf4a1561b544a6ea684b0bcfa975f7e7f6061` (C2 landing). Base for diffs:
`2133f5bd993aaf34efad795d5e0b588485401fb2`; round-97 instrument at `a9a53608`.
Instrument under test: `corpus/instruments/capture-secret-scan.py`,
sha256 `45f8d226b65e5bf16b9323bfc246c2748319713af5740a608838d6a6eb6f9f0e` — equals the
frozen pin in `.ufo/waves/round-98/claims.json` (receipt `instrument-sha256.txt`).
Sources: `corpus/source-snapshots/round-94/S140.txt` lines 291-294, 478-481, 495-498, 547-551.

Method: `git archive` extracts of the landing, base and round-97 revisions under my scratch
(`/fast/scratch/hyaku/kasegi-r98/ReviewC2Scanner`, removed after the receipts were copied);
no clone, no work tree, no mutating git call. Every comparison below is a differential run of
the landing regexes against reference regexes transcribed character-for-character from S140's
own `regex =` lines, with POSIX `[[:punct:]]`/`[[:space:]]`/`[[:blank:]]` translated to their
ASCII ranges (blank is a subset of space, so the class is punct ∪ space ∪ EOL).
No tool was installed; Python 3 stdlib only. The receipt scripts embed the scratch extract path
they ran against; to re-run, re-extract the three revisions with `git archive` and point the
`importlib` path in `oracle.py` / `fuzz.py` / `session-matrix.py` / `nine-payloads.py` at the
extract.

## Verdict summary

The four new grammars are exact, the five widenings move in the right direction and fix the
round-97 defect, and no earlier shape regressed. Two defects block a clean APPROVE: the claim
(and three documents) assert an equality between `(?![A-Za-z0-9])` and S140's class that is
false on 156 byte values, and the C2 docstring introduced a new `SyntaxWarning` that base and
round-97 do not have. Both are one-line/documentation fixes; no regex behaviour needs to change.

**REQUEST-CHANGES** (F1, F2 blocking; F3, F4 documentation). No K limb fails on anything I
could reproduce.

---

## What I verified as correct

### 1. The four new shapes, character by character

| shape | S140 line | grammar check | boundary check |
|---|---|---|---|
| `gitlab-ci-build-token` | 293 | `glcbt-` ✓, prefix `[A-Za-z0-9]{1,5}` ✓ (0 and 6 refused, 1-5 accepted), literal `_` ✓ (missing `_` refused), tail `[A-Za-z0-9_-]{20}` ✓ (19/21 refused) | `(?![A-Za-z0-9])` — superset of S140's class, F1 |
| `gitlab-iam-refresh-token` | 480 | `gliamrt-` ✓, `[A-Za-z0-9_-]{43}` ✓ (42/44 refused), `\.` ✓ (no-dot refused), `[A-Za-z0-9_-]{43}` ✓ | `(?![A-Za-z0-9_-])` ≡ S140's `[^0-9a-zA-Z_\-]\|$` exactly: 0 diffs over all 256 bytes |
| `gitlab-iam-authorization-code` | 497 | `gliamac-` + 43 + `.` + 43 ✓ | same, exact |
| `gitlab-session-cookie` | 549-551 | context `_gitlab_session` ✓, optional `_geo_`+64 hex ✓, separator required ✓, optional `cell-<N>-` ✓, 64 lower-case hex ✓ (63/65 and upper-case refused) | S140 has no right boundary; ours adds `(?![0-9a-f])` — narrowing, see O1 |

Receipts: `oracle-sweep.txt` (256-byte right-boundary sweep + 256-byte left-boundary sweep +
exact-length matrix), `fuzz.txt` (40 000 random bodies per shape), `session-matrix.txt`.

Left boundary: `_GL_LB` (`capture-secret-scan.py:278`) vs S140's `\b` — **0 diffs over all 256
single-byte prefixes** for all eight shapes. The escape-terminator alternatives in `_GL_LB`
(`\n`, `\uXXXX`, `%XX`, `&#..;`) are a deliberate pre-existing widening from rounds 96/97, not a
round-98 change.

### 2. The five widened shapes

`gitlab-runner-registration-token`, `gitlab-feed-token`, `gitlab-oauth-app-secret`,
`gitlab-feed-token-v2`, `gitlab-scim-oauth-token` each changed exactly one token:
`(?![A-Za-z0-9_-])` → `(?![A-Za-z0-9])` (`capture-secret-scan.py:312,314,316,318,322`).
Verified direction: `_` and `-` after the token now HIT (the round-97 defect), alphanumerics
still REFUSE, space/newline still HIT — all matching S140's class on those characters
(`oracle-sweep.txt` §widening direction). The round-97 instrument at `a9a53608` reports **none**
of the nine payloads; the landing reports exactly one shape per payload (`nine-payloads.txt`).

### 3. No earlier shape regressed

- Selftest: landing `SELFTEST-RESULT pass cases=170` rc 0; base `2133f5b` and round-97 `a9a53608`
  both `pass cases=148` rc 0 (`selftest-landing.txt`, `selftest-base.txt`, `selftest-r97.txt`).
- Case list: **0 removed**, 22 added, 148 + 22 = 170 (`case-diff.txt`). The selftest asserts
  `got == want` on the full hit set, so every base case still produces its exact shape set.
- Pattern table: 4 added, 0 removed, exactly 5 changed — and each change is only the right
  boundary class; no other shape's regex was touched (`pattern-diff.txt`).
- K2 independently replayed at the landing: `scanned=3280 hits=0 files=0 allowed=27
  unused_allow=0 rc=0` (`k2-scan.txt`).
- Gate plants are grammar-generated, not copied from the selftest: `PLANT_SPEC` uses
  `gen(r, ALNUM, r.randint(1,5))`, `ALNUMU`, `HEX` (`capability-check.py:65-67,140-175`).

---

## Findings

### F1 (blocking, low severity) — `(?![A-Za-z0-9])` is not S140's class; it is a strict superset, and the claim says it is S140's class

`claims.json` C2 statement: "the five round-97 shapes … now use S140's own punct/space/EOL
boundary `(?![A-Za-z0-9])`". That identification is false.

S140's class is `(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)` = ASCII punctuation ∪ ASCII
whitespace ∪ EOL. `(?![A-Za-z0-9])` additionally accepts every non-ASCII byte and every
non-whitespace C0 control plus DEL.

Evidence (256-byte right-boundary sweep, `oracle-sweep.txt`):

```
gitlab-ci-build-token                    diffs=156 {'ours-only': (156, ['0x00','0x01',...])}
gitlab-runner-registration-token         diffs=156 {'ours-only': (156, ...)}
gitlab-feed-token                        diffs=156 {'ours-only': (156, ...)}
gitlab-oauth-app-secret                  diffs=156 {'ours-only': (156, ...)}
gitlab-feed-token-v2                     diffs=156 {'ours-only': (156, ...)}
gitlab-scim-oauth-token                  diffs=156 {'ours-only': (156, ...)}
gitlab-iam-refresh-token                 diffs=0
gitlab-iam-authorization-code            diffs=0
```

156 = 0x00-0x08 (9) + 0x0E-0x1F (18) + 0x7F (1) + 0x80-0xFF (128). All differences are
"ours-only" — the implementation is a superset, never narrower. The 40 000-body fuzz shows the
same and nothing else (`fuzz.txt`), e.g.
`[gitlab-ci-build-token-fixture-redacted-r98]é` → ours True, S140 False; `GR1348941…\x04` → ours True, S140
False.

The same false equality is repeated in three committed places:
- `corpus/instruments/capture-secret-scan.py:178-180` — "with the rule's own punct/space/EOL
  right boundary (S140 line 294)";
- `corpus/instruments/capture-secret-scan.py:298-300` — "S140's own right boundary for the five
  round-97 shapes";
- `SCORECARD.md:307` — "plus S140's own punct/space/EOL right boundary for the five round-97
  shapes".

Impact: no secret S140 would catch is missed (superset), and the extra hits are real tokens
followed directly by a non-ASCII or control byte — which is *desirable* for a pre-commit secret
gate (S140's ASCII-only class misses `GR1348941…です`). So the regex should be **kept**; what is
wrong is the statement that it is S140's class. A verifier testing the claim's equality finds it
false, which is exactly the failure mode the round's verifiability axis is meant to prevent.

Fix (no behaviour change): record an erratum as C1 did, and reword the three sites to
"`(?![A-Za-z0-9])`, a superset of S140's punct/space/EOL class: it also accepts a non-ASCII or
non-whitespace control byte after the token, so it never refuses a token S140 would report".

### F2 (blocking, low-medium severity) — new `SyntaxWarning` at `capture-secret-scan.py:184`

The C2 docstring line

```
184:                         (S140 line 480), right boundary `[^0-9a-zA-Z_\-]`/EOL.
```

is a non-raw string containing `\-`. Compiling with warnings promoted (`syntax-warning.txt`):

```
landing/.../capture-secret-scan.py SYNTAXWARNING-AS-ERROR: "\-" is an invalid escape sequence. ... line 184
base/.../capture-secret-scan.py clean
r97/.../capture-secret-scan.py clean
```

Every invocation prints it to stderr, and so does every importer — `capture-source.py:102,120`
loads this module for the pre-commit intake gate. The warning's own text says the sequence "will
not work in the future": a later Python makes this a `SyntaxError`, which would take the intake
gate down. No current gate catches it (`py_compile` used by `kill-rule-check.py:513` and
`limb-mutation-check.py:324` accepts warnings), so only a reviewer sees it.

Fix: make the docstring raw (`r"""`) or write `\\-`. One character.

### F3 (documentation, low severity) — the knowledge entry's stated limit contradicts the instrument

`corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md:65-67`:

> "The session-cookie rule is context-bound … so a cookie value separated from its name by a
> line break is out of scope — the rule's own context window is the same line."

The instrument's separator is `[\s\"'=:;]+` (`capture-secret-scan.py:309`), and `\s` includes
`\n`. Verified: `_gitlab_session\n<64 hex>` **hits** (`session-matrix.txt`, `newline-only
got=True`). So the entry declares out of scope exactly what the instrument matches. Either the
entry is wrong about S140's context window or the instrument over-matches; as committed, the two
C2 artifacts disagree. This also means the separator does not require an assignment operator —
whitespace alone suffices — which is broader than an "assignment context" ([INFERENCE]: the
snapshot defines only `keywordGroup`/`keywordGroupType`, not the window semantics, so I cannot
prove S140 rejects it).

Fix: either require an assignment operator (e.g. `[\s"'=:;]*[=:][\s"'=:;]*`) or correct the
entry's limit to say the instrument accepts a line break.

### F4 (documentation, trivial) — wrong S140 line citation for the ci-build boundary

`capture-secret-scan.py:180` cites "S140 line 294" for the boundary. In the snapshot,
`293` is the whole regex *including* `(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)` and `294` is
`tags = ["gitlab", "client_side_sd"]` (`s140-lines.txt`). The boundary is on 293.

Fix: cite 293 (the claim's `S140:291-294` block citation is fine).

---

## Observations (not findings)

- **O1 — session-cookie right boundary is narrower than S140.** S140's regex has no boundary;
  ours adds `(?![0-9a-f])` (`capture-secret-scan.py:310`). A 65-hex value is refused by ours and
  matched by S140 (`session-matrix.txt`: "S140 regex … on 65-hex value: True / landing: False").
  This enforces the claim's "exactly 64" and only refuses values that are not valid cookies.
  Keep, but it is an undocumented deviation from S140's regex.
- **O2 — `\u003d`-escaped separator is not matched** (`escaped-json-u003d got=False`). Not a
  proven miss: the JSON form `"_gitlab_session":"<value>"` does match, and `\u003d` between key
  and value is not a form S140 is documented (in this snapshot) to accept.
- **O3 — `[[:blank:]]` in S140's class is redundant** (subset of `[[:space:]]`); no behaviour
  follows from it.
- **O4 — no ci-build/JWT double report** on the tested forms: `glcbt-eyJ…` reports only
  `gitlab-jwt-token`; `glcbt-Ab3_…` only `gitlab-ci-build-token` (`nine-payloads.txt`).

## Residual risk / verification gaps

- The S140 `examples` values are structurally redacted in the snapshot, so the four new shapes
  were checked against the grammar, not against a published example value.
- `assignmentContext` window semantics are not defined anywhere in the corpus (grep over
  `corpus/source-snapshots/` finds only S140:550-551), so F3's "S140 would reject a line break"
  half is [INFERENCE]; the entry-vs-instrument contradiction is observed fact.
- The gate's ten "boundary negatives" (`capability-check.py:159-175`) are length/grammar
  negatives; none exercises a non-ASCII or control boundary, which is why F1 is invisible to K3.
  A boundary negative of that kind would be the regression test for F1.
- I did not run the capability gate (K3-K7); that is R62Reviewer's seat. K1/K2 I reproduced
  independently.

## VERDICT lines

VERDICT: C2 four new shapes (grammar: alphabet, exact length, separator) — PASS. `glcbt-` 1-5 + `_` + 20; `gliamrt-`/`gliamac-` 43 + `.` + 43; `_gitlab_session` context + separator + optional `cell-<N>-` + 64 lower hex; all exact against S140:293/480/497/549-551.

VERDICT: C2 four new shapes (right boundary) — PASS for the two IAM shapes (`(?![A-Za-z0-9_-])` ≡ S140's class, 0/256 diffs); DEVIATION for ci-build (`(?![A-Za-z0-9])` is a 156-byte superset of S140's class, F1).

VERDICT: C2 five widened boundaries — PASS in direction (token + `_`/`-` now hits, alnum still refuses, r97 misses all five); the claim's "S140's own punct/space/EOL" is false as an equality (F1), though the superset never loses a hit.

VERDICT: C2 no earlier shape regressed — PASS. Selftest 148 → 170, 0 cases removed, 22 added, all pass at the landing; 4 shapes added, 0 removed, exactly 5 regexes changed (boundary only); K2 replay hits=0 allowed=27 unused_allow=0.

VERDICT: C2 landing `e2caf4a1` — REQUEST-CHANGES. Blocking: F1 (claim/docstring/SCORECARD assert an equality with S140's class that is false; keep the regex, record the erratum and reword three sites) and F2 (new `SyntaxWarning` at `capture-secret-scan.py:184`, absent at base and round-97; one-character fix). Also fix F3 (knowledge entry's line-break limit contradicts the instrument) and F4 (S140 line citation 294 → 293). No regex behaviour change is requested; with the erratum plus the two one-line doc fixes this flips to APPROVE.
