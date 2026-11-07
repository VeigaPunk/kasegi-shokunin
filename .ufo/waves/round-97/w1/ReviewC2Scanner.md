# Round-97 w1 — ReviewC2Scanner

Seat: `ReviewC2Scanner` (leaf). Lane: kasegi. Base `b06af5e07efbd961a8449f7de6b57eeea62c6bd3`,
freeze `daf7fc6a627d615178c27594110e956e592e4cd9`, C1 landing `75a471809cba265c8981ece1c0ed29c7895d9308`,
C2 landing `a9a53608dce6aea07d298bb9d5133532078eb1dd`.

Instrument under review: `corpus/instruments/capture-secret-scan.py` at the C2 landing,
sha256 `59909fc4d70819b1a67fa9eec36db2b054462770959828e4c3ff3ce164d2bd92` — equals the frozen
`instrument_sha256` pin. Base instrument `71876619a62875049a5526a03806aa740e3ead122aacdc1499fe153be3048ac9`.
Source of truth: S140 = `corpus/source-snapshots/round-94/S140.txt` (GitLab `gitlab.toml` @ `59ada1f4`),
sha256 `f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`.

## Verdict

**APPROVE.**

Every clause of the frozen C2 statement is implemented at the landing, and every K limb re-derives
at the landing with the pinned shas. The four boundary deviations below are routed findings (F1–F2
qualifiers, F3–F4 informational): none of them re-scores the claim (K1–K6 pass), and none produces a miss
on a token form the statement names. F5 (four undetected S140 rules missing from the known-limits list)
and F6 (provenance) are routed for the L1, not verdict changes.

## What I re-derived

| Clause (frozen statement) | Landing | Evidence |
|---|---|---|
| ten new shapes exist, named exactly | lines 284–303, ten entries | `06-s140-lines.txt` |
| `gitlab-runner-registration-token` `GR1348941`+exactly 20, **no prefix** | line 285, no `_GL_PREFIX`; `group(0)` starts at `GR1348941` | `09-clause-probes.txt` |
| `gitlab-feed-token` `feed_token=`+exactly 20 | line 287 | 19→no, 20→yes, 21→no |
| `gitlab-oauth-app-secret` `gloas-`+exactly 64, **no prefix** | line 289 | 63→no, 64→yes, 65→no |
| `gitlab-feed-token-v2` `glft-`+exactly 20, **no prefix** | line 291 | 19→no, 20→yes, 21→no |
| `gitlab-incoming-email-token` optional 1–20 prefix + `glimt-` + 20–25 **lower-case** | line 293: `_GL_PREFIX` + `[a-z0-9]{20,25}` | 19→no, 20/22/25→yes, 26→no, upper-case tail→no |
| `gitlab-scim-oauth-token` `glsoat-`+exactly 20, **no prefix** | line 295 | 19→no, 20→yes, 21→no |
| `gitlab-deploy-token-in-url` literal + 1+ digits + `:` + exactly 20 + `@` | line 297: `[0-9]+` and a literal `@` | no digits→no, no `@`→no, 19/21→no |
| `gitlab-feature-flags-client-token` optional prefix + `glffct-`+exactly 20 | line 299 | 19→no, 20→yes, `acme-` included in `group(0)` |
| `gitlab-runner-controller-token` optional prefix + `glrct-`+exactly 20 | line 301 | 19→no, 20→yes, `acme-` included in `group(0)` |
| `gitlab-kubernetes-agent-token` optional prefix + `glagent-`+exactly 50, **rule's own right boundary** | line 303: `(?![A-Za-z0-9_-]|\.[0-9a-z])` | 49→no, 50→yes, 51→no; `.ab`→no, `.AB`→yes, `.`→yes, `.0`→no, `._`→yes, `-`→no |
| no new shape fires on a plain 20-char token of the same family | `gloas-`+20→none, `glagent-`+20→none | `09-clause-probes.txt` |
| selftest 128 → 148 | base 128, landing 148, rc=0 | `02`, `03` |
| known-limits list keeps only the three named GitLab items | lines 189–193 name exactly `glft-` 64-hex (S140:512), `t1_` (S140:308), `/trigger/pipeline` (S140:532) | `06-s140-lines.txt` |
| landing repairs the round-96 receipt literals | 19 files / 152 markers under `.ufo/waves/round-96/w1/**-receipts/` at the landing | `13-redaction-and-base-limits.txt` |

Predicate re-derivation at the landing (`05-capability-check.txt`, seed 4242):

```
LIMB K1 ok inst_sha=pin-ok gate_sha=pin-ok selftest=pass cases=148
LIMB K2 ok rc=0 scanned=3018 hits=0 allowed=27 unused_allow=0
LIMB K3 ok rc=1 hits=10 missing=none extra=none
LIMB K4 ok base_new_shape_hits=0 old_shapes_missing=none
LIMB K5 ok rows=1 last=87 named=True
LIMB K6 ok rc=1 shapes=aws-access-key-id,aws-sts-session-token,credential
CAPABILITY-CHECK-RESULT pass rc=0
```

Independent `--rev` run at the landing: `scanned=3018 hits=0 files=0 allowed=27 unused_allow=0 rc=0`.
The base instrument on the same revision also reports `hits=0 allowed=27`, so the ten new shapes add no
hit to the real corpus (no new false positive) — `04-rev-landing.txt`.

Independent adversarial plant repo (nonce `04cjvrpevejp`, 10 positives + 24 negatives, `--files`):
`hits=10`, `MISSING []`, `EXTRA []`, `EXACT True` — `08-plant-probe.txt`. The 24 negatives include the
same-family short forms (`gloas-`+20, `glagent-`+20), the `glft-` 64-hex known limit, `.ab`/`.0`/`-`
after a 50-char `glagent-`, upper-case variants, and 21-char over-length forms.

Differential against S140's published regexes (POSIX classes expanded verbatim, 63,288 generated
cases: left × prefix × length × right per family) — `07-differential.txt`:

```
CASES 63288
DISAGREE 2192
cont-right:narrower      130
escape-left:broader     1935
escape-left:narrower      20
nonascii-right:broader    65
OTHER:narrower            42
```

The `escape-left:narrower` bucket is not an escape-left effect: its 20 cases are `&#38;`/`&#x26;` left bytes
with a `_`/`-` right byte, i.e. the same right-boundary narrowing as `cont-right:narrower` (F2). The
`OTHER` bucket is entirely F1.

No collision was observed: no new shape fires on another new shape's plant, and no old shape fires on any
new plant (the plant probe's `EXACT True` covers every shape in `patterns()`, not only the ten).

## Findings

### F1 — `gitlab-deploy-token-in-url` adds a left boundary S140 line 341 does not have (narrower) — [qualifier, low]

- Landing line 297: `_GL_LB + rb"gitlab\+deploy-token-[0-9]+:[A-Za-z0-9_-]{20}@"`.
- S140 line 341: `regex = '''gitlab\+deploy-token-[0-9]+:([0-9a-zA-Z_\-]{20})@'''` — **no `\b`**.
- Observable: of 24 left bytes, exactly the four word bytes disagree (`x`, `_`, `9`, `Z`): S140 matches,
  the scanner does not (`12-deploy-url-left.txt`, `07-differential.txt` OTHER bucket, 42 cases).
- Practical impact: none observed. Every URL-authority position for this form is preceded by `:`, `/`,
  `@`, or start-of-input, all of which the scanner accepts. The docstring at lines 164–166 does not
  disclose the added boundary.
- Suggested repair (not required by the frozen predicate): drop `_GL_LB` from line 297, matching S140
  exactly, or state the added left boundary in the docstring.

### F2 — the five "simple" shapes narrow S140's right boundary, rejecting `_` and `-` — [qualifier, low]

- Landing lines 285, 287, 289, 291, 295: `(?![A-Za-z0-9_-])`.
- S140 lines 101, 160, 174, 190, 278: `(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)`. POSIX `[[:punct:]]`
  includes `_` and `-`, so S140 terminates a 20/64-char token on either; the scanner continues the token
  and refuses.
- Observable: `GR1348941<20>_`, `feed_token=<20>-`, `gloas-<64>-`, `glft-<20>-`, `glsoat-<20>_` — S140
  hits, scanner misses (130 `cont-right:narrower` cases plus the 20 `escape-left:narrower` cases, which
  are the same effect after an `&#38;`/`&#x26;` left byte — 150 total, `07-differential.txt`).
- This is the lane's uniform token-continuation rule for the non-versioned GitLab shapes (round-93..96
  `gitlab-pat`, `gitlab-runner-auth-token`, `gitlab-deploy-token`, `gitlab-jwt-token` and
  `gitlab-pipeline-trigger-token` all end with the same `(?![A-Za-z0-9_-])`), and it prevents a truncated
  match on a longer token whose 21st byte is `_` or `-`. It does not affect the `glft-` 64-hex known
  limit: S140's own 20-character rule also refuses a 64-hex tail, because the 21st byte is alphanumeric.
  No realistic 20-character token is followed by `_`/`-` in prose.
- Not a round-97 regression; inherited convention.

### F3 — `_GL_LB` is broader than S140's `\b` in escape-terminated contexts (broader) — [informational]

- Landing line 264 (`_GL_LB`), applied at lines 285–303.
- S140 lines 101/160/174/190/213/229/278/392/412 use `\b`; line 341 uses none.
- Observable: `\u0026GR1348941<20>`, `%26glft-<20>`, `\ngloas-<64>`, `&#38;…` — scanner hits, S140 misses
  (1,935 cases, `07-differential.txt`).
- Documented convention since round 93 (lines 89–92: "a preceding escape terminator of the forms `\\t`,
  `\\r`, `\\n`, `\\uXXXX`, `%XX`, `&#NN;` or `&#xXX;` is allowed"), deliberate for JSON-escaped captures.
  Not a round-97 change and not a false positive on the real corpus (`--rev` hits=0 over 3,018 capture
  files).

### F4 — a non-ASCII byte after the token widens the five simple shapes (broader) — [informational]

- Landing lines 285/287/289/291/295 vs S140's POSIX classes: S140's `[[:punct:]]`/`[[:space:]]` cover
  ASCII only, so a following `\xc3` (first byte of a UTF-8 sequence) is not a terminator for S140 but is
  for the scanner (65 cases, `07-differential.txt`).
- Marginal; no observed false positive.

### F5 — four S140 GitLab rules remain undetected and are not in the known-limits list — [qualifier, medium]

The landing's known-limits paragraph (lines 189–193) names only the `glft-` path-dependent form, the `t1_`
legacy partition and the `/trigger/pipeline` URL form. Four further S140 GitLab rules have no scanner
shape and no limit entry (`11-uncovered-rules.txt`):

| S140 | rule id | regex | landing scanner |
|---|---|---|---|
| 293 | `gitlab_ci_build_token` | `\b(glcbt-[0-9a-zA-Z]{1,5}_[0-9a-zA-Z_\-]{20})(?:[[:punct:]]|[[:space:]]|$)` | `[]` — `gitlab-jwt-token` covers only the `glcbt-eyJ…` JWT form |
| 480 | `gitlab_iam_refresh_token` | `\b(gliamrt-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:…)` | `[]` |
| 497 | `gitlab_iam_authorization_code` | `\b(gliamac-[0-9a-zA-Z_\-]{43}\.[0-9a-zA-Z_\-]{43})(?:…)` | `[]` |
| 549 | `gitlab_session_cookie` | `(?:cell-[0-9]+-)?[0-9a-f]{64}` (`_gitlab_session` context) | `[]` |

This is pre-existing: the base instrument at `b06af5e0` names none of them either (grep count 0), so it is
not a round-97 regression and it does not re-score K1–K6. It does mean the statement's "keeps only …"
reads as the complete remaining GitLab gap when it is not. Suggested repair: add the four rule ids to the
known-limits paragraph, or take them as a round-98 lead.

### F6 — provenance of the tenth family — [informational]

The claim's surface says "the ten remaining GitLab families the round-96 known-limits list named". The
round-96 list named nine GitLab families (six prefixes + registration + `feed_token=` + deploy-token URL)
plus the two path-dependent forms it kept. The tenth, the plain `glagent-` 50 form (S140:213), is the
round-96 spot-check's routed defect 1 — which the surface itself parenthesises. No scanner effect.

## Residual risk

- F1's narrowing is invisible to the frozen predicate: K3's plant for the deploy-token URL starts with
  `https://`, i.e. preceded by `/`. A future plant that prefixes the literal with a word byte would expose
  it.
- F2's narrowing means a 20-character token immediately followed by `_` or `-` is missed where S140 would
  report it (e.g. `glft-<20>-backup`). No published S140 example takes that shape, and the narrowing is
  what prevents a truncated match on a longer token; the two properties cannot both hold with one regex.
- F5's four rules are real GitLab credential shapes (CI build token, IAM refresh/authorization codes,
  session cookie) and are undetected in captures today.

## Verification gaps

- The S140 example arrays are structurally redacted in the snapshot, so no published example value could
  be replayed through the scanner; the differential uses generated boundary matrices instead.
- K3's plant set is the frozen harness's ten positives + ten negatives; my independent probe widens the
  negatives to 24 but still cannot cover every left/right byte (the 63,288-case differential does).
- The `--rev` clean run depends on the round-97 redaction; I verified the marker counts (19 files / 152
  markers) but did not re-run the redaction generator.

## Receipts

All under `.ufo/waves/round-97/w1/ReviewC2Scanner-receipts/`; every cited output is the command's own
stdout/stderr.

| File | Command | Observed |
|---|---|---|
| `01-sha-and-diff.txt` | `sha256sum` + `git show <rev>:<path> \| sha256sum` + `git diff --stat` | landing `59909fc4…` = pin; base `71876619…`; 77 insertions / 5 deletions; allowlist unchanged |
| `02-selftest-landing.txt` | `python3 -B corpus/instruments/capture-secret-scan.py --selftest` | `SELFTEST-RESULT pass cases=148`, rc=0 |
| `03-selftest-base.txt` | same, three files extracted at `b06af5e0` | `SELFTEST-RESULT pass cases=128`, rc=0 |
| `04-rev-landing.txt` | `--lane <lane> --rev a9a53608 --allow corpus/instruments/capture-secret-allow.tsv` (landing and base instruments) | both `scanned=3018 hits=0 files=0 allowed=27 unused_allow=0 rc=0` |
| `05-capability-check.txt` | `.ufo/waves/round-97/c2/capability-check.py … --seed 4242` | K1–K6 ok, `CAPABILITY-CHECK-RESULT pass rc=0` |
| `06-s140-lines.txt` | `sed -n` over S140 lines 101/160/174/190/213/229/278/341/392/412/308/512/532 + landing lines 283–304, 189–193 | the ten published regexes and the ten landing patterns |
| `07-differential.txt` | generated 63,288-case matrix, S140-translated regexes vs `GITLAB_PATTERNS` | `CASES 63288 DISAGREE 2192`; classes as tabulated |
| `08-plant-probe.txt` | nonce plant repo, 10 positives + 24 negatives, `--files` | `hits=10`, `MISSING []`, `EXTRA []`, `EXACT True` |
| `09-clause-probes.txt` | per-clause length/prefix/right-boundary probes | as tabulated above |
| `10-scorecard-row.txt` | `git show <landing>:SCORECARD.md` filtered to the capability row | `ROWS 1`, last cell `87`, all ten ids named |
| `11-uncovered-rules.txt` | S140 lines 291/478/495/547 + 293/480/497/549, scanner probe | four rules → `[]`; base names none |
| `12-deploy-url-left.txt` | 24-byte left sweep, S140:341 vs landing line 297 | `DIFF` on `x`, `_`, `9`, `Z` only |
| `13-redaction-and-base-limits.txt` | `git show --name-only b3c2aff`, `git grep -c` at the landing, base known-limits | 19 files / 152 markers; base list text |

Scratch `/fast/scratch/hyaku/kasegi-r97/ReviewC2Scanner` removed at seat end. No tool installed or
upgraded; no pacman transaction; no git/jj mutation in the lane.
