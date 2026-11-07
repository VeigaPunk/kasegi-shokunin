# SentinelShapes — kasegi round 96, attempt 1, wave w1

Seat: adversarial security review of the seven GitLab shapes landed at
`7ef1d365eb523a83b2567342a6c0f585ab028ab0` (`gitlab-pat-routable`,
`gitlab-pat-versioned`, `gitlab-runner-auth-token-versioned`,
`gitlab-deploy-token-versioned`, `gitlab-agent-token-versioned`,
`gitlab-workspace-token-versioned`, `gitlab-pipeline-trigger-token`), read as an
attacker who wants a real token to pass unseen.

Read-only seat: no lane file was edited by this seat except this report and its
receipts directory. Every probe value is synthetic (repeated letters `A`–`H`);
no real credential appears in this report or in any receipt. The exact bytes are
given as compositions (`glpat-` + `A`×28 + …) so the report is reconstructible
without storing a shape-complete literal; receipt 07 carries the sha256 of every
payload.

## Verdict

**C2 STANDS.** The landed instrument is byte-identical to the frozen candidate
(sha256 `71876619…8ac9`), the gate is the frozen `8b6f8493…c8e6`, the selftest is
128 (base 115), and K1–K6 all pass at the landing at seed `20261107`. Across 214
probes the scanner's detection language is a strict superset of S140's seven
published regexes: **0 cases exist where S140 hits and the scanner misses**; the
8 parity differences are all the scanner being wider (the round-93 `%XX`
escape boundary). **0 MUST-FIX. 8 routed findings**, the highest-value ones
being R1 (an encoded `.` in a routable/versioned tail is undetected and
undocumented) and R8 (S140's plain `glagent-` 50-character rule is undetected
and the round-96 known-limits edit no longer names it). **No finding re-scores
K1–K6.**

## What I re-derived (not re-read)

| Limb | Observed | Receipt |
|---|---|---|
| instrument pin | `7ef1d36:corpus/instruments/capture-secret-scan.py` sha256 `71876619…8ac9` = claims.json `instrument_sha256` = `c2/candidate-scanner.py` | 06 |
| gate pin | `7ef1d36:corpus/instruments/claim-package-check.py` sha256 `8b6f8493…c8e6` = claims.json `gate_sha256` | 06 |
| counter pin | `c2/capability-check.py` sha256 `989a443f…247c` = claims.json `counter_sha256` | 06 |
| selftest | landed `SELFTEST-RESULT pass cases=128` rc 0; base `d8a2bb0` `cases=115` rc 0 | 04, 05 |
| K1–K6 at the landing | `CAPABILITY-CHECK-RESULT pass rc=0`, seed `20261107`: K1 pin-ok/cases=128; K2 `scanned=2744 hits=0 allowed=27 unused_allow=0`; K3 `hits=7 missing=none extra=none`; K4 `base_new_shape_hits=0 old_shapes_missing=none`; K5 `rows=1 last=87 named=True`; K6 `rc=1` with `aws-sts-session-token` | 03 |
| SCORECARD row | exactly one `capture-secret-scan` row; names all seven shapes and S140 lines 30/51/136/324/358/375; first-working-round cell `87` | 08 #10 |
| known-limits drop | the six detected families are absent from the `Known limits:` paragraph; only `glrt-` inside the `t1_` legacy-partition limit and `glpat%2D` in the encoded-prefix limit remain | 08 #9 |

## The seven shapes and their synthetic tokens (exact composition)

| shape | S140 regex line | synthetic token | bytes |
|---|---|---|---|
| `gitlab-pat-versioned` | 51 | `glpat-` + `A`×28 + `.de.fg1234567` | 47 |
| `gitlab-pat-routable` | 30 | `glpat-` + `B`×28 + `.defg12345` | 44 |
| `gitlab-runner-auth-token-versioned` | 136 | `glrtr-` + `C`×30 + `.ab.cd1234567` | 49 |
| `gitlab-deploy-token-versioned` | 324 | `gldt-` + `D`×30 + `.ab.cd1234567` | 48 |
| `gitlab-agent-token-versioned` | 358 | `glagent-` + `E`×30 + `.ab.cd1234567` | 51 |
| `gitlab-workspace-token-versioned` | 375 | `glwt-` + `F`×30 + `.ab.cd1234567` | 48 |
| `gitlab-pipeline-trigger-token` | 73 | `glptt-` + `G`×40 (and `glptt-` + `H`×20) | 46 / 26 |

S140's own regexes are transcribed in receipt 12; the head class
`[0-9a-zA-Z_\-]{27,300}`, the tails `\.[0-9a-z]{2}[0-9a-z]{7}` /
`\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7}`, the `glptt` alternation
`(?:[0-9a-zA-Z_\-]{20}|[0-9a-zA-Z_\-]{40})(?:[^0-9a-zA-Z_\-]|$)`, and the optional
`(?:[a-zA-Z0-9]{1,20}-)?` prefix are all matched by the landed code.

## Bypass classes — result matrix

Each cell is the landed scanner's verdict for that shape on the class payload.
`H` = HIT (the expected shape fires), `M` = MISS, `·` = class does not apply
(no `.` in the token). Full 214-row transcript: receipt 01; compact matrix:
receipt 13.

| class (transform applied to the token) | pat-v | pat-r | run-v | dep-v | agt-v | ws-v | pt-40 | pt-20 |
|---|---|---|---|---|---|---|---|---|
| baseline `t ` + tok + ` end` | H | H | H | H | H | H | H | H |
| A1 `q=a&#x26` + tok (no semicolon) | M | M | M | M | M | M | M | M |
| A1c `q=a&#x26;` + tok (control) | H | H | H | H | H | H | H | H |
| A2 `q=a\x26` + tok (literal backslash-x-2-6) | M | M | M | M | M | M | M | M |
| A3 `q=a&#38` + tok (decimal, no semicolon) | M | M | M | M | M | M | M | M |
| A3c `q=a&#38;` + tok (control) | H | H | H | H | H | H | H | H |
| A4 `q=a%2526` + tok (double-encoded `&`) | M | M | M | M | M | M | M | M |
| A4c `q=a&amp;amp;` + tok (control) | H | H | H | H | H | H | H | H |
| B `\n` inside the token body | M | M | M | M | M | M | M | M |
| B `\r\n` inside the token body | M | M | M | M | M | M | M | M |
| B `\`+`\n` continuation inside the body | M | M | M | M | M | M | M | M |
| C `x` + tok (left alnum run) | M | M | M | M | M | M | M | M |
| C tok + `Z` (right alnum run) | M | M | M | M | M | M | M | M |
| C `x` + tok + `Z` | M | M | M | M | M | M | M | M |
| C `_` + tok | M | M | M | M | M | M | M | M |
| D tok + `_` | M | M | M | M | M | M | M | M |
| D tok + `-` (control) | H | H | H | H | H | H | M | M |
| E `https://h/p?token=` + tok + `&x=1` | H | H | H | H | H | H | H | H |
| E `https://h/p?token%3D` + tok | H | H | H | H | H | H | H | H |
| E `https://h/p?t=` + tok + `#f` | H | H | H | H | H | H | H | H |
| G 20×`R` + `-` + tok (control) | H | H | H | H | H | H | H | H |
| G 21×`P` + `-` + tok | H | H | H | H | H | H | H | H |
| G 30×`Q` + `-` + tok | H | H | H | H | H | H | H | H |
| F `.` → `%2E` | M | M | M | M | M | M | · | · |
| F `.` → `%2e` | M | M | M | M | M | M | · | · |
| F `.` → `\u002e` | M | M | M | M | M | M | · | · |
| F `.` → `&#46;` | M | M | M | M | M | M | · | · |
| F `.` → `&#x2e;` | M | M | M | M | M | M | · | · |

Totals: 214 probes, 86 HIT / 128 MISS. The CLI `--files` run over one file per
probe agrees with `scan_bytes` on all 214 (`CLI_DISAGREEMENTS=0`), so the matrix
is the shipped executable's behaviour, not a library artefact.

## Per-class detail (exact bytes, exploit path, verdict)

### A — escape contexts the left boundary does not cover

`_GL_LB` is `(?<![A-Za-z0-9_])` plus the escape alternatives
`(?<=\\[ntr])`, `(?<=\\u[0-9A-Fa-f]{4})`, `(?<=%[0-9A-Fa-f]{2})`,
`(?<=&#[0-9]{2};)`, `(?<=&#[xX][0-9A-Fa-f]{2};)`. The alternatives are an
allowlist; any escape whose **last byte is alphanumeric** and which is not one of
those five forms leaves a word byte immediately before `glpat-`, so the primary
lookbehind fails and no alternative matches.

| exact bytes before the token | scanner | S140 | why |
|---|---|---|---|
| `q=a&#x26;` | HIT | HIT | `;` is non-word; the entity alternative is redundant |
| `q=a&#38;` | HIT | HIT | same |
| `q=a&amp;amp;` | HIT | HIT | `;` is non-word |
| `q=a\u0026` | HIT | MISS | `\uXXXX` alternative (scanner wider) |
| `q=a%26` | HIT | MISS | `%XX` alternative (scanner wider) |
| `q=a%3D` | HIT | MISS | `%XX` alternative (scanner wider) |
| `q=a&#x26` (no semicolon) | **MISS** | MISS | last byte `6` is word; HTML5 decodes this in text content |
| `q=a&#38` (no semicolon) | **MISS** | MISS | last byte `8` is word; HTML5 decodes this in text content |
| `q=a\x26` (C-style) | **MISS** | MISS | no `\xXX` alternative; valid JS string escape |
| `q=a%2526` (double-encoded `&`) | **MISS** | MISS | last two bytes `26` are alnum; no alternative |

`&#x26`/`&#38` without the semicolon are decoded by an HTML5 parser in **text
content** (the missing-semicolon parse error does not stop the decode); in an
attribute value they are not decoded when the next character is alphanumeric, so
the realistic exploit is a captured HTML page's text, not an attribute.
`\x26` is a valid JavaScript string escape. `%2526` is a double-encoded `&`
(one decode → `%26`, two → `&`). All four are source-faithful misses (S140's
`\b` fails identically); the general class is already routed in round 93
(`SentinelEscape` a19–a25: `%253A`, `%2520`, `\x20`, `%u0020`, octal, `\f`,
`\b`). This seat adds the no-semicolon entity sub-case. Routed as R2.

### B — token split across a line wrap

`t ` + `glpat-` + `A`×10 + `\n` + `A`×18 + `.de.fg1234567` + ` end` → MISS for
all seven shapes; the same with `\r\n` and with `\`+`\n` (a shell/Dockerfile
continuation) → MISS. `scan_bytes` runs `finditer` over the whole blob, but the
head class cannot contain a newline, so a split token is invisible. S140 misses
identically. The docstring's known limits already say "values soft-wrapped
across lines"; a `\`-continuation is a *syntactic join* (the shell/Dockerfile
produces the concatenated value), so the phrase under-describes that sub-case.
Routed as R3 (documentation wording, not a code defect).

### C — token embedded in a longer alphanumeric run

`x` + tok, tok + `Z`, `x` + tok + `Z`, `_` + tok → MISS for all seven. This is
the `\b`/`(?<![A-Za-z0-9_])` guard working as designed and is S140-faithful.
It is not a practical bypass: a server would receive the extended value, not the
token. Qualifier only (R4).

### D — trailing `_`

tok + `_` → MISS for all seven (`_` is in the excluded class); tok + `-` → HIT
for the six dotted shapes, MISS for `glptt` (its terminator is
`(?![A-Za-z0-9_-])`, which excludes `-`). Both are S140-faithful: the versioned
rules use `\b` (a trailing `-` is a boundary, a trailing `_` is not), the
`glptt` rule uses `(?:[^0-9a-zA-Z_\-]|$)`. A trailing `_` is not a valid token,
so this is a qualifier (R5); the `glptt` asymmetry is R6.

### E — token inside a URL query

`?token=` + tok + `&x=1` → HIT; `?token%3D` + tok → HIT; `?t=` + tok + `#f` →
HIT. The `=`, `&`, `#` and `%` are all non-word, so the left boundary holds.
The `%3D` form is **wider than S140** (S140's `\b` sees the `D` as a word byte
and misses); this is the round-93 escape-boundary extension doing its job. No
finding.

### F — percent-encoded `.` separator (highest-value routed finding)

`glpat-` + `A`×28 + `%2Ede%2Efg1234567` → MISS; likewise `%2e`, `\u002e`,
`&#46;`, `&#x2e;`. The tail patterns require a literal `\.`, and the plain
`gitlab-pat` shape cannot rescue the value because its head is exactly 20
characters and a routable/versioned head is at least 27 (any head ≥ 21 defeats
the 20-character shape). A real routable/versioned token placed
in a URL with its dots percent-encoded is decoded by the server to the valid
token, so a HAR/HTML/log capture of that URL passes the gate unseen. S140 uses
a literal `\.` too, so this is source-faithful and not a regression; but the
round-96 shapes are the **first** to depend on a literal `.` separator, and the
docstring's known limits name only an encoded *prefix* separator
(`gh%5Fp_`, `glpat%2D`) — a reader would not infer an encoded *tail* separator.
Routed as R1.

### G — custom instance prefix longer than 20 characters

`P`×21 + `-` + tok and `Q`×30 + `-` + tok → HIT for all seven. The optional
prefix group fails at >20 characters, but the match then starts at `glpat-` /
`glrtr-` / … because the preceding `-` is non-word; the span excludes the long
prefix (21-char probe: span 22–69). The 20-character control also hits with the
prefix included. No finding; this class is covered.

## S140 parity (is the landing a narrowing of the source?)

214 probes × the seven S140 regexes compiled from the snapshot (receipt 12):

- **0** payloads where S140 matches and the landed scanner does not.
- **8** payloads where the scanner matches and S140 does not — all the
  `?token%3D` + tok form, i.e. the scanner's `%XX` escape boundary is wider
  than S140's `\b`. Widening, not narrowing.
- Structural confirmation: the scanner's left boundary is `\b` plus five escape
  alternatives (superset); its right boundaries are `(?![A-Za-z0-9_])` for the
  versioned/routable forms (identical to `\b` after a word byte) and
  `(?![A-Za-z0-9_-])` for `glptt` (identical to S140's
  `(?:[^0-9a-zA-Z_\-]|$)`); head/tail classes and quantifiers are identical.
  The one difference is that `gitlab-runner-auth-token-versioned` omits the
  optional `(?:[a-zA-Z0-9]{1,20}-)?` prefix that S140 line 136 carries; detection
  is unaffected (a prefixed `glrtr-` still matches from `glrtr-`), only the span
  differs (R7).

This parity is scoped to the **seven claimed rules**. S140 has an eighth rule
in the `glagent-` family — `gitlab_kubernetes_agent_token` (line 213, plain
`glagent-` + exactly 50, with a special right boundary
`(?:[^0-9a-zA-Z_\-.]|\.[^0-9a-z]|\.$|$)`) — which the landing does not
implement and which the round-96 known-limits edit no longer names. It is a
**narrowing against S140** (scanner MISS, S140 HIT on the same payload) and is
routed as R8 (receipt 14).

## MUST-FIX

**None.** Each candidate failed to contradict a frozen clause or the source:

1. **K1–K6 all pass at the landing** (seed `20261107`, receipt 03): K1
   pin-ok/cases=128, K2 hits=0/allowed=27/unused_allow=0, K3 7/7 exact with no
   extra, K4 base 0 new shapes and no old shape missing, K5 one row/last=87/all
   seven named, K6 `aws-sts-session-token` present. No finding touches a limb.
2. **The instrument is the frozen candidate** (sha256 `71876619…8ac9`), so the
   pre-freeze control at `b31227ca` binds the landed bytes; the gate is the
   frozen `8b6f8493…c8e6`.
3. **No narrowing of the seven claimed rules**: 0/214 probes where the source's
   seven regexes hit and the scanner misses; the 8 differences are all wider.
   A bypass class that S140 also misses is a source-inherited limit, not a
   landing defect. (The eighth S140 rule, plain `glagent-` line 213, is outside
   the claim and is R8.)
4. **No boundary negative fires**: K3's six negatives produce no hit, and the
   clean tree is `hits=0`. The statement's shape/length/selftest clauses are true
   as written; the known-limits clause "keeps the rest" is qualified by R8 (the
   plain `glagent-` form is no longer named).

## Routed findings

All docstring remediations below change the instrument's sha256, which K1 pins;
they cannot be applied to the landed file without a re-freeze and are therefore
next-round work, not landing fixes. The regex changes are likewise future-round
work (the kill rule forbids widening a boundary after data).

### R1 (routed, medium) — encoded tail `.` separator is undetected and undocumented

- **Exploit path.** A real routable/versioned token is placed in a URL with its
  dots percent-encoded: `…?private_token=glpat-` + `A`×28 + `%2Ede%2Efg1234567`.
  The server percent-decodes `%2E` to `.` and accepts the token; the captured
  HAR/HTML/log stores the encoded form; `capture-secret-scan` reports nothing.
  The same holds for `%2e`, `\u002e` (JSON string escape), `&#46;`/`&#x2e;`
  (HTML entities).
- **Evidence.** Receipt 01, F rows: 6/6 dotted shapes MISS on all five encodings;
  receipt 02, spans `-` for the same payloads; the plain `gitlab-pat` shape
  cannot rescue them (its head is exactly 20, and any routable/versioned head is
  ≥ 27, so the 21st character defeats the lookahead).
- **Impact.** A real token passes a pre-commit gate. Medium: the attacker must
  control the URL encoding in the captured artifact, but that is exactly the
  HAR/HTML case the scanner exists for.
- **Smallest remediation.** Extend the known-limits sentence that already names
  the encoded prefix separator to also name the encoded **tail** separator
  (`%2E`/`%2e`/`\u002e`/`&#46;`). Do **not** widen the regex now: the kill rule
  forbids widening a boundary after data, and a widening would change the
  instrument pin and require a re-freeze. A future round that widens should add
  selftest cases for `%2E` and `%2e` plus a boundary negative.

### R2 (routed, medium-low; carried from round 93 a19–a25) — escape terminators whose last byte is alphanumeric

- **Exploit path.** `q=a&#x26` + tok (no semicolon) in captured HTML text
  content; `q=a\x26` + tok in a captured JS bundle; `q=a%2526` + tok in a
  double-encoded URL. All decode to `&` before the token, and all MISS.
- **Evidence.** Receipt 01, A1/A2/A3/A4 rows: 8/8 MISS each; the semicolon
  controls (`&#x26;`, `&#38;`, `&amp;amp;`) HIT. Receipt 02 confirms the
  no-semicolon entity and `\x26` misses.
- **Impact.** A real token in a captured HTML/JS artifact passes. The general
  class is already routed (round-93 `SentinelEscape` a19–a25); `%2526` is
  arguably covered by the documented "a whole URL percent-encoded inside
  another URL's query" limit.
- **Smallest remediation.** Add the no-semicolon entity and `\xNN` forms to the
  known-limits list. A regex fix (lookbehind for `&#x?[0-9A-Fa-f]{1,7}` and
  `\\x[0-9A-Fa-f]{2}`) is a future-round widening, not now.

### R3 (routed, low; documented limit, wording) — line-split token

- **Exploit path.** A token split by `\`+`\n` in a captured shell script or
  Dockerfile (the shell joins the continuation, so the file contains a valid
  token); or by a raw `\n`/`\r\n` in a log.
- **Evidence.** Receipt 01, B rows: 8/8 MISS for `\n`, `\r\n`, `\`+`\n`.
- **Impact.** Low: the artifact must split the value, and the known limits
  already say "values soft-wrapped across lines". A `\`-continuation is a
  syntactic join, not a display wrap, so the phrase under-describes it.
- **Smallest remediation.** Say "split by a line break or a `\`-continuation" in
  the known-limits sentence.

### R4 (routed, low) — token embedded in a longer alphanumeric run

- **Exploit path.** `x` + tok or tok + `Z`; the server would receive the
  extended value, not the token, so this is not a practical bypass.
- **Evidence.** Receipt 01, C rows: 8/8 MISS; S140 `\b` misses identically.
- **Impact.** None beyond the shape guard's intended false-negative cost.
- **Smallest remediation.** None; qualifier only.

### R5 (routed, low) — trailing `_`

- **Exploit path.** tok + `_`; the value is not the token.
- **Evidence.** Receipt 01, D row: 8/8 MISS; S140 `\b`/`[^…]` misses identically.
- **Impact.** None; qualifier only.
- **Smallest remediation.** None.

### R6 (routed, low) — `glptt` right-boundary asymmetry

- **Exploit path.** `glptt-` + `G`×40 + `-` MISSes while the six dotted shapes
  accept a trailing `-`. A 41-character value is not the 40-character token, so
  this is not a bypass.
- **Evidence.** Receipt 01, D control row: `glptt` M, the six dotted shapes H;
  receipt 02, `glptt-40 trailing hyphen` MISS.
- **Impact.** None; faithful to S140 line 73's `(?:[^0-9a-zA-Z_\-]|$)`.
- **Smallest remediation.** None; qualifier only.

### R7 (routed, low; consistency) — runner pattern omits the optional instance prefix

- **Exploit path.** None for detection: `ACME-glrtr-` + 30 + tail still matches
  from `glrtr-` because the preceding `-` is non-word.
- **Evidence.** Receipt 02: `runner glrt- (no r)` span 0–48; `prefixed 21-char
  glpat- versioned` span 22–69 (prefix excluded); the runner pattern at
  `capture-secret-scan.py:249` is `_GL_LB + rb"glrtr?-" + _GJ_VER` with no
  `_GL_PREFIX`, while S140 line 136 has `(?:[a-zA-Z0-9]{1,20}-)?`.
- **Impact.** The match span excludes a custom prefix for this one shape, unlike
  the other five; a future allowlist row authored over S140's span (with prefix)
  would not bind. No current allowlist row exists for the new shapes.
- **Smallest remediation.** Add `_GL_PREFIX` to the runner pattern in the next
  round; changing it now would break the frozen instrument pin and require a
  re-freeze.

### R8 (routed, medium) — S140's plain `glagent-` 50-character rule is undetected and no longer named as a limit

- **Exploit path.** A plain Kubernetes agent token — `glagent-` + exactly 50
  `[A-Za-z0-9_-]`, S140 line 213 `gitlab_kubernetes_agent_token`, with the
  special right boundary `(?:[^0-9a-zA-Z_\-.]|\.[^0-9a-z]|\.$|$)` — passes
  unseen. The landed scanner implements only the **versioned** `glagent-` form
  (line 358); there is no plain `glagent-` shape. The round-96 known-limits edit
  removed `glagent-` from the "remaining GitLab prefixes" sentence, so the
  docstring no longer names this limit even though it still applies.
- **Evidence.** Receipt 14: `glagent-` + 50×`X` + space → scanner `MISS`,
  S140:213 `HIT`; the same with `.Z` and with `.` at EOF; 49 and 51 characters
  miss in both. Receipt 12 line 213 carries the rule text.
- **Impact.** Medium: a real plain agent token passes the pre-commit gate, and
  a reader of the known-limits list would conclude the `glagent-` family is
  fully covered. This is the one place where the landing is **narrower** than
  S140, but it is outside the seven claimed rules, so it does not re-score
  K1–K6.
- **Smallest remediation.** Restore the plain `glagent-` 50-character form to
  the `Known limits:` paragraph (a docstring edit; no regex change now). A
  future round that adds the shape should transcribe S140 line 213's special
  right boundary and add selftests for 49/50/51 plus the `.Z` and `.`-at-EOF
  cases.

## Does any finding re-score K1–K6?

**No.** K1–K6 were re-derived at the landing (receipt 03): every limb is `ok`,
and the instrument/gate/counter hashes equal the frozen pins. The probes live
only in seat scratch and never enter the lane tree; they are outside the K3 plant
repository and outside the K2 clean tree, so they cannot change a limb. The
parity result (0/214 narrowing on the seven claimed rules) means no finding
contradicts the tested clauses; R8 qualifies the known-limits "keeps the rest"
clause (the plain `glagent-` form is no longer named) but touches no K limb, and
the six K3 boundary negatives still produce no hit. The findings are routed
defects/qualifiers for a later round, not verdict changes.

## Scope and limits of this review

- C1 (tranche 11 labels, prose-pointer M4, attribution fixtures) is outside this
  seat's surface; I did not audit it and did not touch its files.
- I did not test the intake gate (`capture-source.py`) end-to-end, base64/gzip/
  UTF-16-wrapped captures (documented limits), or the lane's own tree beyond the
  K2 limb the capability check runs.
- The probe matrix uses one payload per (shape, class); the supplementary probes
  (receipt 02) cover the length/case/prefix edges the matrix does not: head 27
  and 300 hit, 301 misses; routable head 26 misses; EOF hits; `glrt-` and
  `glrtr-t2_` hit; uppercase `GLPAT-` misses (lowercase literal, S140-faithful).
- The lane's working tree carries an uncommitted edit to
  `corpus/knowledge/gitlab-routable-and-versioned-token-forms.md` made by a
  sibling seat (it records the same plain-`glagent-` limit as R8 and clarifies
  the runner prefix). This seat did not touch it; R8 is re-derived from S140
  line 213 and receipt 14, not from that edit.

## Receipts

Directory: `.ufo/waves/round-96/w1/SentinelShapes-receipts/`.

| # | file | content |
|---|---|---|
| 01 | `01-attack-matrix.txt` | 214-row HIT/MISS table (shape, class, scanner, S140, parity, CLI) |
| 02 | `02-supplementary.txt` | 31 boundary probes with match spans |
| 03 | `03-capability-check.txt` | `CAPABILITY-CHECK-RESULT pass` and K1–K6 lines at seed `20261107` |
| 04 | `04-selftest-landed.txt` | landed `SELFTEST-RESULT pass cases=128` |
| 05 | `05-selftest-base.txt` | base `d8a2bb0` `SELFTEST-RESULT pass cases=115` |
| 06 | `06-pins.txt` | instrument/gate/counter/base sha256 |
| 07 | `07-payload-digests.txt` | sha256 and length of every probe payload |
| 08 | `08-commands.txt` | every command, observed rc/lines |
| 09 | `09-hygiene-scan.txt` | `--files` re-scan of this directory and the report: hits=0 |
| 10 | `10-driver-attack.py` | the 214-probe driver |
| 11 | `11-driver-supp.py` | the supplementary driver |
| 12 | `12-s140-lines.txt` | the seven S140 rule blocks with line numbers (examples elided) |
| 13 | `13-matrix.md` | compact class × shape matrix |
| 14 | `14-plain-glagent.txt` | S140 line 213 plain `glagent-` 50: scanner MISS, S140 HIT (R8) |

All receipts were re-scanned with the landed instrument after capture; no
shape-complete literal is stored, and no real credential appears anywhere.
