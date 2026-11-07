# ReviewC2Scanner — round-99 C2 landing review

Seat: `ReviewC2Scanner` (leaf; no subagent dispatch). Lane: `kasegi-shokunin`.
Reviewed state: C2 landing `a3db47e71fe292c03b00ba11f38cccbec45d3966` (the redaction
addendum) over `7f89004692fbf1b8b15ba1fa03f5372667ee355c` (the pattern change), base
`b9411a6b530e486180cf14c72fccc46668dcf5ee`. Scratch
`/fast/scratch/hyaku/kasegi-r99/ReviewC2Scanner` (removed before yield).

Sources checked:
- S140 `corpus/source-snapshots/round-94/S140.txt:547-551` — `id = "gitlab_session_cookie"`,
  `keywords = ["_gitlab_session"]`, `regex = '''(?:cell-[0-9]+-)?[0-9a-f]{64}'''`,
  `assignmentContext.keywordGroup = '''_gitlab_session(?:_geo_[0-9a-f]{64})?'''`,
  `assignmentContext.keywordGroupType = "raw"`.
- S148 — **no `corpus/source-snapshots/round-98/` directory exists** (`ls` → No such file or
  directory), so the row quote was used: `corpus/SOURCES.md:160`, "64 hexadecimal characters
  with an optional `cell-<ID>-` prefix".
- S150 — `corpus/SOURCES.md:162`, "`assignmentContext` expands a rule to
  `<keyword>.{0,8}[:=].{0,8}<value>`, and `keywordGroupType raw` injects the keyword group
  verbatim".

## What the landing changes

`git diff --stat b9411a6 a3db47e -- corpus/instruments/capture-secret-scan.py` →
`1 file changed, 38 insertions(+), 6 deletions(-)`; `git diff … | grep '^@@'` → three hunks
only (`@@ -186,11 +186,17 @@` docstring, `@@ -310,7 +316,7 @@` the one pattern line,
`@@ -632,6 +638,32 @@` the case list). Every removed line is docstring prose or the old
pattern line:

```
-        _GL_LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?[\s\"'=:;]+"
```

The landing pattern (`corpus/instruments/capture-secret-scan.py:318-320`):

```python
("gitlab-session-cookie", re.compile(
    _GL_LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?[^\n]{0,8}[:=][^\n]{0,8}"
    rb"(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])")),
```

`_GL_LB` is `corpus/instruments/capture-secret-scan.py:286`
(`(?<![A-Za-z0-9_])` plus escape-context alternatives). Instrument sha256 at the landing:
`git show a3db47e:corpus/instruments/capture-secret-scan.py | sha256sum` →
`8b338726f931ab0b3f2333d48a200017d36ae0dddac5f3b86fb2c581f2ca110a` (equals the claim pin and
the working tree). Ancestry: `git merge-base --is-ancestor 7f89004 a3db47e` → `ANCESTOR-OK`.

## Checks

### 1. Window vs the S150 generator, element by element

Model used: `re.compile(rb'_gitlab_session(?:_geo_[0-9a-f]{64})?.{0,8}[:=].{0,8}(?:cell-[0-9]+-)?[0-9a-f]{64}')`
(Python `.` without DOTALL ≡ Go RE2 `.` without `(?s)`; both exclude `\n`).

| element | generator | instrument | observed |
|---|---|---|---|
| gap bounds | `.{0,8}` both sides | `[^\n]{0,8}` both sides | equal; `n-gap-9` (9 spaces) misses in both |
| operator class | `[:=]` | `[:=]` | equal; `=>`, `,=`, `\|=`, `+=`, `(=`, ` ( = ) ` all hit via gap absorption + `=` |
| newline refusal | `.` excludes `\n` | `[^\n]` | equal; `n-gap-newline` (`=\n` + H) misses in both |
| left boundary | none in the quoted generator | `_GL_LB` = `(?<![A-Za-z0-9_])` + escape alternatives | **narrower** — see F4 |
| optional `cell-<N>-` | `(?:cell-[0-9]+-)?` | `(?:cell-[0-9]+-)?` | equal; `cell-7-`+64/65 hit, `cell-abc-` misses in both |
| 64-hex alphabet | `[0-9a-f]{64}` | `[0-9a-f]{64}` | equal; upper-case and 63-hex misses in both |
| right boundary | none | `(?![0-9a-f])` | **narrower** — see F5 |

Evidence for the table (all run at the landing bytes):

```
x_gitlab_session=        pure_gen=True inst=False
__gitlab_session=        pure_gen=True inst=False
cr_gap                   pure_gen=True inst=True
tab_gap                  pure_gen=True inst=True
pct20                    pure_gen=True inst=True
cell-7-64                pure_gen=True inst=True
cell-7-65                pure_gen=True inst=True
cell-7-66                pure_gen=True inst=False
geo                      pure_gen=True inst=True
newline_gap              pure_gen=False inst=False
gap9                     pure_gen=False inst=False
```

Fuzz over 120,000 generated payloads (18-byte separator alphabet incl. `\n`, `\r`, `%`, hex
digits, `_`, `-`; random gap lengths 0-10, operator variants, cell-prefix variants):

```
divergence classes: {'right-boundary': 88, 'other': 0}
```

i.e. every ASCII divergence is the pre-existing `(?![0-9a-f])` boundary, not a new one.

Non-ASCII gap (the one new divergence class, documented as bytes):

```
gap 4 x e-acute (bytes=8):  gen=True  inst=True
gap 8 x e-acute (bytes=16): gen=True  inst=False
gap 9 x e-acute (bytes=18): gen=False inst=False
```

The docstring already says "up to 8 non-newline **bytes**"
(`corpus/instruments/capture-secret-scan.py:193-194`) and the knowledge entry says "a gap
wider than eight bytes" (`corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md:77-82`),
so the byte/rune difference is disclosed, not silent.

### 2. The twelve MUST-FIX payloads and the ten negatives

The probe's twelve `MUSTFIX` payloads (`corpus/instruments/capture-secret-scan.py:645-656`,
`.ufo/waves/round-99/c2/session-cookie-probe.py:26-39`) were replayed against the generator
model: `MUSTFIX gen hits: 12 /12`. The ten negatives: nine are generator misses; the tenth,
`n-left-word` (`x_gitlab_session=` + H), **is a generator hit** (F4).

Probe runs (probe sha256 `79b2235d94295129fbc6c404a6d7005772099dd9489e446df875488d3fef6904`,
equals the claim pin):

```
base b9411a6 : PROBE-RESULT mustfix_hit=0/12  negatives_extra=2 negatives=10 instrument_sha256=b7804b7d…
landing      : PROBE-RESULT mustfix_hit=12/12 negatives_extra=0 negatives=10 instrument_sha256=8b338726…
round-98 e2caf4a1: PROBE-RESULT mustfix_hit=0/12 negatives_extra=2 negatives=10 instrument_sha256=45f8d226…
```

The two base extras are `n-gap-9` and `n-gap-newline` — the round-98 class `[\s"'=:;]+`
crossed nine spaces and a newline; the landing fixes both. The committed
`.ufo/waves/round-99/controls/c2-probe-candidate-r99.txt` reproduces line-for-line.

### 3. Selftest and no earlier shape regressed

```
BASE    (b9411a6): SELFTEST-RESULT pass cases=170
LANDING (a3db47e): SELFTEST-RESULT pass cases=192
```

Case-name diff base→landing: 22 additions (`gl-session-ck-*`), **zero removals**. The full
file diff removes only the docstring block and the old pattern line (listed above), so no
pre-existing case payload or expectation changed. The 22 new cases are the twelve positives
plus ten negatives at `corpus/instruments/capture-secret-scan.py:645-669`.

### 4. K4 — the lane's own scan

```
rev 7f89004 (pre-redaction): HIT … body-sweep.txt line=10; final-checks.txt line=15;
  matrix-run.txt line=5; matrix.tsv line=306
  CAPTURE-SECRET-SCAN mode=rev:7f89004692fbf1b8b15ba1fa03f5372667ee355c scanned=3485
  hits=4 files=4 allowed=27 unused_allow=0 rc=1
rev a3db47e (landing): CAPTURE-SECRET-SCAN mode=rev:a3db47e71fe292c03b00ba11f38cccbec45d3966
  scanned=3485 hits=0 files=0 allowed=27 unused_allow=0 rc=0
```

Both reproduce `.ufo/waves/round-99/controls/c2-landing-r99.txt` exactly. The widened window
introduced no hit anywhere in the lane except the four receipts, and the addendum removes them.

### 5. The redaction

`git diff a3db47e^ a3db47e -- .ufo/waves/round-98/w1/SentinelShapes-receipts/`: 57 changed
lines, 57 `[session-cookie-fixture-redacted-r99]` markers, one per line, no line with two
markers; pre and post files have identical line counts (asserted per file). Redacted value
lengths: `{64: 35, 65: 9, 66: 11, 67: 1, 68: 1}`. The instrument's `findall` over the
pre-redaction files returns 8 + 12 + 18 + 19 = **57**, so the redaction set is exactly the
instrument's match set. 26 synthetic 64+ hex runs remain in the committed receipts (bare
values and the `cell-7-` 66/67-hex lines); none is a scanner hit (K4 hits=0) and all are the
sentinel's synthetic `0123456789abcdef…` fixture, not a credential.

Control digests, verified:

```
before = sha256 of the whole pre-redaction file  → matches all four rows exactly
after  = sha256 of the whole file with ONLY that row's line redacted → matches all four rows
```

Example (body-sweep line 10): `before=b84a39d9…` equals
`git show a3db47e^:…/body-sweep.txt | sha256sum`; `after=dfffcff9…` equals the digest of the
pre file with only line 10's value replaced. The committed final file digest is
`6b8c8833…`, which is not what the row's `after` states — see F1.

## Findings

**F1 (low — documentation/evidence clarity).** `.ufo/waves/round-99/controls/redaction-r99.txt:4-7`
states `before=`/`after=` digests without stating the convention. `before` is the whole
pre-redaction file and `after` is the whole file with **only that row's line** redacted (a
per-line intermediate state), not the committed final file. Verified: all four `before`
digests match the pre-redaction blobs; all four `after` digests match the per-line
reconstruction; none of the four `after` digests matches the committed file
(`body-sweep` committed `6b8c8833…` vs `after=dfffcff9…`; `final-checks` `95a1ea3e…` vs
`4d6e27ca…`; `matrix-run` `f085df54…` vs `f5a44d45…`; `matrix.tsv` `d2954f70…` vs
`a26004e9…`). A verifier checking the committed bytes sees a mismatch. Fix: state the
per-line convention in the control, or add the four final-file digests. Not a correctness
defect — the redaction itself is surgical and complete relative to the instrument's matches.

**F2 (low — documentation).** The commit message (and the Goal text) says "53 synthetic
64-hex session values". Observed: 57 redacted values, of which 35 are exactly 64 hex and 22
are 65-68 hex (`{64: 35, 65: 9, 66: 11, 67: 1, 68: 1}`), and 57 markers. The `53` is not
reproducible from the committed diff. Fix the count (57 values / 57 markers) in the receipt
or the wave summary.

**F3 (informational — disclosed).** The byte-quantified gap is narrower than the generator's
rune-quantified `.{0,8}` for non-ASCII separators: `_gitlab_session` + 8 × `é` (16 bytes) +
`=` + H is a generator hit and an instrument miss. Both the docstring
(`capture-secret-scan.py:193-194`, "bytes") and the knowledge entry
(`gitlab-iam-ci-build-and-session-token-shapes.md:77-82`) state the byte unit. No action
required; keep the wording.

**F4 (informational — deliberate, documented).** `_GL_LB` refuses `x_gitlab_session=` and
`__gitlab_session=`, which the literal S150 generator matches (verified:
`pure_gen=True inst=False`). The knowledge entry documents this as a deliberate miss
("The instrument keeps a left boundary (`_GL_LB`) that S140's raw keyword group does not
have, so a prefixed name (`x_gitlab_session=`) is a deliberate miss (the round-98 sentinel's
Q1: S140 over-detects there)"). Consequence: the probe's `n-left-word` is a
*convention* negative, not an S140 negative; the claim's "no boundary negative" is true
under the instrument's convention. Pre-existing, not a regression.

**F5 (low — pre-existing, disclosed in the claim statement, undocumented in the docstring).**
`(?![0-9a-f])` is narrower than S140's boundary-less value regex: 73+ hex runs and
`cell-7-` + 66 hex are generator hits and instrument misses (`hex 73: gen=True inst=False`;
`cell-7-66: pure_gen=True inst=False`). 64-72 hex runs hit in both (the gap absorbs the
leading hex). The claim statement includes the boundary; the docstring
(`capture-secret-scan.py:189-199`) does not state it. Real session values are exactly 64
lower-case hex, so the narrowing cannot miss a real value; add one clause to the docstring
for symmetry with the other rules.

## Residual risk and verification gaps

- S150 was reviewed from the committed `corpus/SOURCES.md:162` quote, not a live fetch; the
  MR's "Generated Regex" block itself was not re-read. The generator model is a Python
  reconstruction of Go's default `.` (no `(?s)`); no Go toolchain was run against the rules
  repo. If the generated regex carries `(?s)`, the newline refusal would be narrower than
  the generator — the committed quote does not show `(?s)`.
- S148 has no round-98 snapshot; the row quote was used. It says "64 hexadecimal characters"
  without a case, while S140's regex is lower-case `[0-9a-f]`; the instrument follows S140,
  and the upper-case negative is justified by S140.
- The 26 residual synthetic 64+ hex runs in the receipts are not scanner hits and are the
  sentinel's synthetic fixture; they are not a credential leak, but the receipts are not
  value-free.
- The widened window was not exercised against a live GitLab rules corpus; coverage evidence
  is the 12 sentinel payloads, the 22 selftest cases and the lane-wide scan.

## Verdicts

VERDICT: window-vs-S140/S148/S150 APPROVE — the landing pattern is the generator's
`<keyword>.{0,8}[:=].{0,8}<value>` with Go's newline-excluding `.` made explicit as `[^\n]`,
the same `[:=]`, the same optional `cell-[0-9]+-` and the same `[0-9a-f]{64}`; the two
narrowings (left `_GL_LB`, right `(?![0-9a-f])`) are pre-existing/documented and cannot miss
a real 64-hex session value; 120,000-payload fuzz found no other ASCII divergence.

VERDICT: no-earlier-shape-regression APPROVE — only the `gitlab-session-cookie` pattern line
changed; selftest 170 → 192 with 22 additions and zero removals; the base probe's two false
positives (`n-gap-9`, `n-gap-newline`) are fixed; the lane-wide scan at the pre-redaction
revision shows the four receipt hits and nothing else, and the landing revision scans clean.

VERDICT: C2-landing APPROVE — K1 (192), K2 (12/12, 0 extras), K3 (0/12 at `e2caf4a1`), K4
(hits=0 at `a3db47e`; hits=4/files=4 at `7f89004`) all reproduce; F1 and F2 are
documentation-only (state the per-line digest convention; correct 53 → 57); F3/F4/F5 are
disclosed or pre-existing conventions.
