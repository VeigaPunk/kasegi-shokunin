# SentinelShapes — round 97, attempt 1 (C2 attack surface)

Seat: leaf security review of the ten new GitLab shapes at
`a9a53608dce6aea07d298bb9d5133532078eb1dd`, read as an attacker who wants a
real token to pass unseen. Every payload below is synthetic; no credential
value appears in this report or in the receipts.

## Verdict

**C2 STANDS on its frozen predicate.** No finding re-scores K1-K6: the ten
boundary negatives still MISS, the selftest still passes 148, and the rev-mode
gate still reports `hits=0`. The frozen statement names each shape's body
grammar and length, not its right boundary, so the one MUST-FIX below is a
qualifier on the *implementation*, not a verdict change.

- **MUST-FIX 1** — five shapes use a right boundary narrower than the cited
  source: a real token followed by `_` or `-` is a MISS, while S140 lines
  101/160/174/190/278 detect it. One-character evasion, 10/10 payloads.
- **Routed** — six qualifiers (R-1…R-6), all source-faithful or declared-class
  except R-1/R-2, which are narrowings against S140 that no realistic left
  context reaches.
- **Not findings** — line wrap, 21/26-character overruns, uppercase tails,
  long instance prefixes, URL-query placement, JSON-value placement, markdown
  cells, curl/`git remote`/`.git/config`/log-line contexts: all behave as
  designed (HIT where they should, MISS where the grammar says so).

Axes walked: (a) false-negative classes per shape — depth:verifiability of the
security claim; (b) fidelity to the cited S140 rule text — coverage. Moves that
improved (a) without harming (b) were kept; the remediation in MF-1 was kept
because it improves (a) and *restores* (b) at zero cost to the boundary set.

## What was read

- `corpus/instruments/capture-secret-scan.py` at the landing, sha256
  `59909fc4d70819b1a67fa9eec36db2b054462770959828e4c3ff3ce164d2bd92`
  (matches the frozen `instrument_sha256`). Lines 284-303 hold the ten
  round-97 patterns; line 119 holds the `gitlab-pat` right-boundary
  declaration.
- `corpus/source-snapshots/round-94/S140.txt` lines 101, 160, 174, 190, 213,
  229, 278, 341, 392, 412 — the cited rule text.
- `.ufo/waves/round-97/claims.json` (C2 statement, K1-K6).
- `corpus/instruments/capture-secret-allow.tsv` — 28 lines; **no row names any
  of the ten new shapes**, so none of them has an allowlist escape hatch.

## The ten shapes as landed

| shape | landed pattern (after `_GL_LB`) | S140 line | S140 right boundary |
|---|---|---|---|
| `gitlab-runner-registration-token` | `GR1348941[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])` | 101 | `[[:punct:]]\|[[:space:]]\|[[:blank:]]\|$` |
| `gitlab-feed-token` | `feed_token=[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])` | 160 | same |
| `gitlab-oauth-app-secret` | `gloas-[A-Za-z0-9_-]{64}(?![A-Za-z0-9_-])` | 174 | same |
| `gitlab-feed-token-v2` | `glft-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])` | 190 | same |
| `gitlab-incoming-email-token` | `(?:[A-Za-z0-9]{1,20}-)?glimt-[a-z0-9]{20,25}(?![A-Za-z0-9_-])` | 229 | `[^0-9a-zA-Z_\-]\|$` |
| `gitlab-scim-oauth-token` | `glsoat-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])` | 278 | `[[:punct:]]\|…` |
| `gitlab-deploy-token-in-url` | `gitlab\+deploy-token-[0-9]+:[A-Za-z0-9_-]{20}@` | 341 | none (literal `@`) |
| `gitlab-feature-flags-client-token` | `(?:…)?glffct-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])` | 392 | `[^0-9a-zA-Z_\-]\|$` |
| `gitlab-runner-controller-token` | `(?:…)?glrct-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])` | 412 | `[^0-9a-zA-Z_\-]\|$` |
| `gitlab-kubernetes-agent-token` | `(?:…)?glagent-[A-Za-z0-9_-]{50}(?![A-Za-z0-9_-]\|\.[0-9a-z])` | 213 | `[^0-9a-zA-Z_\-.]\|\.[^0-9a-z]\|\.$\|$` |

ASCII `[[:punct:]]` is 0x21-0x2F, 0x3A-0x40, 0x5B-0x60, 0x7B-0x7E — so `-`
(0x2D) and `_` (0x5F) are both punctuation. The landed `(?![A-Za-z0-9_-])`
excludes exactly those two.

## Attack matrix

210 payloads: 10 shapes × 20 classes (+ the percent-encoded-separator variants).
Each was run through the landed `scan_bytes` and through a faithful translation
of the cited S140 regexes (POSIX classes expanded to ASCII). Full 210-row
output: `SentinelShapes-receipts/02-attack-matrix-vs-s140.txt`.

`scan` / `S140` below; `=` means both agree.

| class | REG | FEED | OAS | FTV2 | IMT | SCIM | DURL | FFCT | RCT | K8S |
|---|---|---|---|---|---|---|---|---|---|---|
| 00 plain control | HIT | HIT | HIT | HIT | HIT | HIT | HIT | HIT | HIT | HIT |
| 01 `&#x26` no semicolon | =MISS | =MISS | =MISS | =MISS | =MISS | =MISS | **MISS/HIT** | =MISS | =MISS | =MISS |
| 02 `\x26` | =MISS | =MISS | =MISS | =MISS | =MISS | =MISS | **MISS/HIT** | =MISS | =MISS | =MISS |
| 03 `%2526` double-encoded | =MISS | =MISS | =MISS | =MISS | =MISS | =MISS | **MISS/HIT** | =MISS | =MISS | =MISS |
| 04 `\u0026` | HIT/MISS | HIT/MISS | HIT/MISS | HIT/MISS | HIT/MISS | HIT/MISS | =HIT | HIT/MISS | HIT/MISS | HIT/MISS |
| 05 `%26` | HIT/MISS | HIT/MISS | HIT/MISS | HIT/MISS | HIT/MISS | HIT/MISS | =HIT | HIT/MISS | HIT/MISS | HIT/MISS |
| 06 `&#x26;` | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT |
| 07 line wrap | =MISS | =MISS | =MISS | =MISS | =MISS | =MISS | =MISS | =MISS | =MISS | =MISS |
| 08 alnum before | =MISS | =MISS | =MISS | =MISS | =MISS | =MISS | **MISS/HIT** | =MISS | =MISS | =MISS |
| 09 alnum after | =MISS | =MISS | =MISS | =MISS | =HIT | =MISS | n/a | =MISS | =MISS | =MISS |
| 10 trailing `_` | **MISS/HIT** | **MISS/HIT** | **MISS/HIT** | **MISS/HIT** | =MISS | **MISS/HIT** | n/a | =MISS | =MISS | =MISS |
| 11 trailing `-` | **MISS/HIT** | **MISS/HIT** | **MISS/HIT** | **MISS/HIT** | =MISS | **MISS/HIT** | n/a | =MISS | =MISS | =MISS |
| 12 trailing `.` | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | n/a | =HIT | =HIT | =HIT |
| 13 trailing `,` | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | n/a | =HIT | =HIT | =HIT |
| 14 trailing space | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | n/a | =HIT | =HIT | =HIT |
| 15 URL query | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT |
| 16 24-char prefix | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT |
| 17 EOF exact | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT |
| 18 pct separator | n/a | =MISS | =MISS | =MISS | =MISS | =MISS | =MISS | =MISS | =MISS | =MISS |
| 19 JSON value | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT |
| 20 markdown cell | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT | =HIT |

Bold = divergence from the cited source. 32 divergences total: 14 where the
landed instrument is **narrower** (real false negatives) and 18 where it is
**broader** (the documented escape-terminator extension).

CLI-layer confirmation (receipt `03-cli-layer.txt`): 80 files through
`--files`, `scanned=80 hits=62 files=62`, and the 18 misses are exactly
9 shapes × {trailing `_`, trailing `-`}. `gitlab-deploy-token-in-url` is exempt
because its literal `@` sits between the token and the suffix.

## MUST-FIX

### MF-1 — right boundary narrower than S140 on five shapes

**Shapes:** `gitlab-runner-registration-token` (L101),
`gitlab-feed-token` (L160), `gitlab-oauth-app-secret` (L174),
`gitlab-feed-token-v2` (L190), `gitlab-scim-oauth-token` (L278).

**Exploit path.** Append one byte, `_` or `-`, to the token in the capture.
The token is byte-identical and recoverable; the scanner never fires. The
cited source fires, because `[[:punct:]]` includes both bytes.

Exact payloads (all synthetic; `␠` = 0x20):

```
GR1348941A1b2C3d4E5f6G7h8I9j0_␠            landed MISS   S140 HIT
GR1348941A1b2C3d4E5f6G7h8I9j0-␠            landed MISS   S140 HIT
feed_token=A1b2C3d4E5f6G7h8I9j0_␠          landed MISS   S140 HIT
feed_token=A1b2C3d4E5f6G7h8I9j0-␠          landed MISS   S140 HIT
gloas-A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8S9t0U1v2W3x4Y5z6a7b8C9d0E1f2_␠  landed MISS  S140 HIT
gloas-A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8S9t0U1v2W3x4Y5z6a7b8C9d0E1f2-␠  landed MISS  S140 HIT
glft-A1b2C3d4E5f6G7h8I9j0_␠                landed MISS   S140 HIT
glft-A1b2C3d4E5f6G7h8I9j0-␠                landed MISS   S140 HIT
glsoat-A1b2C3d4E5f6G7h8I9j0_␠              landed MISS   S140 HIT
glsoat-A1b2C3d4E5f6G7h8I9j0-␠              landed MISS   S140 HIT
```

Why it is not merely adversarial: a token followed by `_` or `-` is an ordinary
capture shape (`feed_token=…_2` pagination suffix, `gloas-…-backup` in a
filename, a token glued to a slug). The attacker does not need to alter the
token, only the byte after it.

**Why it is undeclared.** The round-97 doc entries state the body grammar and
length and cite the S140 line; none states a right boundary. The lane's own
precedent for the same narrowing is explicit — line 119 says `gitlab-pat` is
"not followed by a letter, digit, `_` or `-`". The five round-97 entries carry
no such sentence, so the narrowing is invisible to a reader who trusts the
citation. The lane's own knowledge file makes the gap sharper:
`corpus/knowledge/gitlab-remaining-token-families.md:30` reproduces the source
line verbatim, `(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)`, while its
"Falsifiable rule" section tests only body length (19/21, 63/65, 49/51) and
never the terminator — so a reader of either document would conclude the
punctuation terminator is implemented.

**Smallest remediation (verified, receipt `05-remediation-check.txt`).**
Replace `(?![A-Za-z0-9_-])` with `(?![A-Za-z0-9])` on those five patterns only
(patched copy sha256 `af5885ac828786b0e744f7990a4b702b3c132e3d0d2aeaaa7235932ac08957f5`):

- `SELFTEST-RESULT pass cases=148` — rc 0, unchanged (all ten boundary
  negatives still MISS).
- 10/10 previously-missing payloads now HIT.
- 5/5 boundary negatives (`*-short`, `glft-` 21-char) still MISS — no
  regression, so K3 is untouched.

If the lane prefers to keep the stricter boundary, the alternative is to add
one sentence per shape to the doc block, matching line 119. Either way the
choice must be visible, because the current text implies source fidelity.

**Severity:** medium. Not exploitable against a token the attacker cannot
re-encode, but it is a one-byte false negative on 5 of the 10 new shapes and
the cited source catches it.

## Routed

### R-1 — `gitlab-deploy-token-in-url` left boundary narrower than S140
S140 line 341 has **no** left boundary (`gitlab\+deploy-token-…`); the landed
pattern prepends `_GL_LB`.
```
xgitlab+deploy-token-7:A1b2C3d4E5f6G7h8I9j0@gitlab.example␠   landed MISS  S140 HIT
q=a&#x26gitlab+deploy-token-7:A1b2C3d4E5f6G7h8I9j0@gitlab.example␠  MISS/HIT
q=a\x26gitlab+deploy-token-7:A1b2C3d4E5f6G7h8I9j0@gitlab.example␠  MISS/HIT
q=a%2526gitlab+deploy-token-7:A1b2C3d4E5f6G7h8I9j0@gitlab.example␠ MISS/HIT
```
Impact low: the realistic left context is `//`, `"` or a space, all of which
pass. The three escape forms are misses only because S140 has no boundary at
all there. Route: no action needed; note the divergence so a future reader does
not assume boundary parity.

### R-2 — `gitlab-deploy-token-in-url` requires literal `+`, `:` and `@`
```
https://gitlab+deploy-token-7:A1b2C3d4E5f6G7h8I9j0%40gitlab.com   MISS
https://gitlab%2Bdeploy-token-7:A1b2C3d4E5f6G7h8I9j0@gitlab.com   MISS
https://gitlab+deploy-token-7%3AA1b2C3d4E5f6G7h8I9j0@gitlab.com   MISS
```
The `%2B`/`%3A` cases are instances of the declared known limit "an encoded
prefix separator"; `%40` is the same class but is not named. S140 misses all
three too, so this is source-faithful. Route: extend the known-limits sentence
to name `%2B`, `%3A` and `%40` for this shape.

### R-3 — `gitlab-feed-token` is query-form only
```
{"feed_token":"A1b2C3d4E5f6G7h8I9j0"}   MISS
feed_token: A1b2C3d4E5f6G7h8I9j0        MISS
feed_token = A1b2C3d4E5f6G7h8I9j0       MISS
feed_token%3DA1b2C3d4E5f6G7h8I9j0       MISS
```
S140 requires the literal `feed_token=` too, and the frozen statement scopes
this shape to "the `feed_token=` query form", so this is faithful. Route: the
JSON/YAML encodings of the same value are a coverage gap for a future tranche,
not a defect here. `%3D` is the declared percent-encoded-`=` limit.

### R-4 — escape-terminator forms outside the declared set
```
q=a\U0026GR1348941A1b2C3d4E5f6G7h8I9j0␠   MISS   (uppercase U)
q=a\x26GR1348941A1b2C3d4E5f6G7h8I9j0␠     MISS
q=a\x3dGR1348941A1b2C3d4E5f6G7h8I9j0␠     MISS
q=a%2526GR1348941A1b2C3d4E5f6G7h8I9j0␠    MISS
q=a&#38GR1348941A1b2C3d4E5f6G7h8I9j0␠     MISS   (unterminated decimal entity)
```
All five are MISS in S140 as well (`\b` fails after a hex digit), so no
divergence. `_GL_LB` covers `\n`/`\t`/`\r`, `\uXXXX`, `%XX`, `&#NN;` and
`&#xNN;`; these five forms are outside that enumeration. Note the adjacent
forms that **do** work: `\u{26}` (HIT — `}` is punctuation), `%2D` before a
token (HIT), `&#45;` before a token (HIT). Route: the doc's phrase "the
escape-terminator left boundary" reads as complete; name the four uncovered
forms in the known-limits list.

### R-5 — `glagent-` 50-char token with a truncated version tail
```
glagent-A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8S9t0U1v2W3x4Y5z6.ab   MISS (both shapes)
glagent-A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8S9t0U1v2W3x4Y5z6.     HIT
glagent-A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8S9t0U1v2W3x4Y5z6.AB   HIT
glagent-…50….ab.cd1234567                                          HIT (as gitlab-agent-token-versioned)
```
The `\.[0-9a-z]` guard that keeps the 50-char pattern off the versioned form
also suppresses the plain token when the version tail is cut short. S140 line
213 behaves identically, so this is source-faithful. Route: declare it, or
accept it as part of the versioned-form ambiguity.

### R-6 — line-wrapped tokens (declared)
```
GR1348941A1b2C3d4E5<LF>f6G7h8I9j0␠   MISS
```
Already in the known-limits list ("values soft-wrapped across lines … are not
detected"). Confirmed as declared; no action.

## Confirmed correct (not findings)

- **Long instance prefix (24 chars):** `abcdefghijklmnopqrstuvwx-<token>` HITs
  for all ten. The `-` before the prefix is a valid left boundary, so a prefix
  longer than the grammar's 1-20 does not hide the token.
- **`glimt-` overruns:** 26 lower-case chars MISS (`{20,25}` is the rule's own
  grammar); 20 lower + uppercase tail MISS (the rule's alphabet is lower-case
  only). Both are faithful to S140 line 229.
- **21-character bodies:** `glft-` + 21 and `gitlab+deploy-token-7:` + 21 MISS.
  Correct — the grammar is exact-length.
- **Realistic contexts all HIT:** markdown bullet, `curl -d "token=…"`,
  `git remote -v` line, `.git/config` `url = https://gitlab+deploy-token-…@…`,
  JSON value, HTML `href` query, log line, markdown table cell, EOF.
- **Allowlist:** no row names any of the ten shapes, so none can be shadowed.

## Over-match direction (scanner broader than S140, by design)

`\u0026` and `%26` before a token produce a HIT where S140's `\b` does not
(the char before is a hex digit, so S140 sees no boundary). 18 payloads. This
is the documented escape-terminator extension and it does not create a live
false positive: the rev-mode run at the landing is
`scanned=3018 hits=0 files=0 allowed=27 unused_allow=0 rc=0` — identical to the
frozen K2 control, and zero `shape=gitlab` hits.

## Claim re-score

| limb | re-derived by this seat | effect of findings |
|---|---|---|
| K1 selftest ≥148 + sha pin | yes — `pass cases=148` rc 0; sha `59909fc4…` = pin | none |
| K2 allowlist gate | yes — `scanned=3018 hits=0 allowed=27 unused_allow=0 rc=0` | none |
| K3 ten positives / ten boundary negatives | boundary half yes — all ten still MISS on the landed and the patched instrument | none; MF-1's fix keeps all ten negatives at MISS |
| K4 base instrument 0/10 | not re-derived here | none (no shape removed) |
| K5 SCORECARD row | not re-derived here | none (no SCORECARD edit) |
| K6 round-86 aws-sts | not re-derived here | none (no AWS pattern touched) |

**No finding re-scores K1-K6.** MF-1 is a qualifier: the frozen C2 statement
fixes the body grammar and length, and every boundary negative in the K3 set is
a *short / long / uppercase / no-at* case, none of which the widening changes.

## Receipts

All commands run with cwd `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
`TMPDIR=/fast/scratch/hyaku/kasegi-r97/SentinelShapes`, scratch removed at
seat end. No tool installed or upgraded (nothing was needed).

| # | command | rc | observed |
|---|---|---|---|
| 1 | `sha256sum corpus/instruments/capture-secret-scan.py` | 0 | `59909fc4d70819b1a67fa9eec36db2b054462770959828e4c3ff3ce164d2bd92` = frozen pin |
| 2 | `awk 'NR==101\|\|NR==160\|\|NR==174\|\|NR==190\|\|NR==213\|\|NR==229\|\|NR==278\|\|NR==341\|\|NR==392\|\|NR==412' corpus/source-snapshots/round-94/S140.txt` | 0 | ten rule lines, quoted in "The ten shapes as landed" |
| 3 | `python3 -B $S/probe2.py` → `SentinelShapes-receipts/02-attack-matrix-vs-s140.txt` | 0 | 210 rows, 32 divergences (14 narrower, 18 broader) |
| 4 | `python3 -B $S/cli_probe.py $S/cap` → `…/03-cli-layer.txt` | 0 | `mode=files scanned=80 hits=62 files=62 allowed=0 unused_allow=25 rc=1`; 18 MISS rows |
| 5 | `python3 -B corpus/instruments/capture-secret-scan.py --selftest` → `…/04-selftest.txt` | 0 | 148 `SELFTEST` lines, 0 `FAIL`, `SELFTEST-RESULT pass cases=148` |
| 6 | `python3 -B $S/fixcheck.py $S` → `…/05-remediation-check.txt` | 0 | patched sha `af5885ac…`; `pass cases=148`; 10/10 misses→HIT; `PATCHED-NEGATIVES bad=0` |
| 7 | `python3 -B $S/edges.py` → `…/06-edge-probes.txt` | 0 | 35 edge/context rows, quoted above |
| 8 | `python3 -B corpus/instruments/capture-secret-scan.py --lane . --rev a9a53608…` → `…/07-rev-mode-fp-check.txt` | 0 | `mode=rev:a9a53608… scanned=3018 hits=0 files=0 allowed=27 unused_allow=0 rc=0` |
| 9 | `wc -l .ufo/waves/round-97/w1/SentinelShapes-receipts/*.txt` | 0 | 319 / 83 / 149 / 27 / 35 / 1 lines |
| 10 | `python3 -B corpus/instruments/capture-secret-scan.py --files .ufo/waves/round-97/w1/SentinelShapes-receipts/*.txt` | 1 then 0 | before redaction: `hits=9 files=1 rc=1`; after: `scanned=6 hits=0 files=0 allowed=0 unused_allow=25 rc=0` |

Read-only on git and jj: no `git add/commit/push/checkout/reset/stash`, no jj
mutation, no fixture repo created. Files written: this report and the seven
receipt files under `.ufo/waves/round-97/w1/SentinelShapes-receipts/`.

**Redaction.** `SentinelShapes-receipts/02-attack-matrix-vs-s140.txt` is a
capture path (`is_capture_path` true, because of the `-receipts` component),
so its synthetic bodies were replaced by `<fixture-64>` / `<fixture-50>` /
`<fixture-20>` / `<fixture-22>` markers per the round-97 convention (commit
b3c2aff), line count unchanged at 319. Before `e393e315…`, after `e676be62…`;
details in `SentinelShapes-receipts/00-redaction.txt`. This report is not a
capture path (`is_capture_path` false), so it keeps the exact payload bytes the
assignment asks for.
