# ScoutSources — round 99, attempt 1 — source reconnaissance

Lane: kasegi. Base `b9411a6b530e486180cf14c72fccc46668dcf5ee`; freeze
`6195db307c1cb101eba1d268f8cbfc1578d2caf7`; C2 landing
`a3db47e71fe292c03b00ba11f38cccbec45d3966`; C1 landing
`35e3ab6041ff8690b00d831f27b93d08101fd16a`.

Seat role: leaf source-recon seat (no subagents dispatched, per the seat spec).
Scratch: `/fast/scratch/hyaku/kasegi-r99/ScoutSources`, removed on exit.
Receipts: `.ufo/waves/round-99/w1/ScoutSources-receipts/`.

Tools installed this round: **none**. No `pacman` transaction (host-wide pacman
transactions are paused); no `uv tool`/`npx`/binary install was needed — every
check below runs on `curl`, `python3` and `git` already present. Nothing was
mutated in the lane repo, a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`
or `MANIFEST.json`; the only writes are this report and its `-receipts/`
directory.

---

## Summary of findings

Three findings, in descending order of severity for the two judged axes
(`depth:verifiability`, `coverage`):

| # | Finding | Axis | Severity |
|---|---|---|---|
| **F1** | The corpus implements the **superseded** upstream separator window. `S140`'s own pinned commit (`59ada1f4`, 2026-11-03) carries `assignmentOperand = `[="' :>\],\t.()\\?|]{1,10}``, **not** the MR !151 form `.{0,8}[:=].{0,8}`. Eleven separator characters that upstream accepts are refused by the corpus scanner. | coverage | **HIGH** |
| **F2** | The `S150` row's anchor digest `aa60d7af…` is **not reproducible**: the MR HTML page is nonce-bound and yields a different sha256 on every fetch. It violates corpus rule **R100** by name. | depth:verifiability | **HIGH** |
| **F3** | The `S140` row's `anchor`/`teaches` cells cite "lines 4, 114, 255" of the **upstream file**; those numbers are the **snapshot's** line numbers. The upstream file's own lines 4/114/255 hold different text (the snapshot's 82 example lines were collapsed, shifting every later line by up to 29). | depth:verifiability | MEDIUM |

---

## F1 — the corpus implements a superseded upstream separator window (coverage, HIGH)

### Observed

**The pinned upstream commit already carries a different window than MR !151.**

`corpus/source-snapshots/round-94/manifest.json` names the pinned commit
`59ada1f4ca53d5a69fafb9cb0f10bb893720ce39`. Fetching the generator source at
**that same commit** (via the commit-pinned API raw URL, byte-stable across
three fetches, receipt `upstream-window-evolution-r99.txt`):

```
$ curl -sS -L -o g.go "https://gitlab.com/api/v4/projects/gitlab-org%2F…/repository/files/pkg%2Frules%2Fassignment_regex.go/raw?ref=59ada1f4ca53d5a69fafb9cb0f10bb893720ce39"
fetch1 status=200 bytes=9776 91519731800ab8d96a00a03fff44e72c
fetch2 status=200 bytes=9776 91519731800ab8d96a00a03fff44e72c
fetch3 status=200 bytes=9776 91519731800ab8d96a00a03fff44e72c

$ awk 'NR>=26&&NR<=30' g.go
27		// assignmentOperand specifies the possible delimiters, used between the LHS and RHS variables in an assignment.
28		assignmentOperand = `[="' :>\],\t.()\\?|]{1,10}`
29		terminalRegex     = `(?:\\['"rn]|['"\x60; \s]|</|$)`
```

At the **MR's own merge sha** (`c9c39249…`, merged 2025-09-29) the constant is
the other form:

```
33		assignmentOperand = `.{0,8}[:=].{0,8}`
```

**Upstream changed it between the MR and the pinned commit.** The file's commit
history (receipt `upstream-window-evolution-r99.txt`):

```
2026-03-03  237a115a  Add support for defining multiple keyword groups
2025-12-01  9239cf69  Include whitespace character at the terminal regex
2025-11-25  1eb45282  Update assignment regex pattern     <-- the window changed here
2025-10-01  25371f29  Add support for Auth0, AWS and Azure patterns
2025-09-30  9dd97a9c  Remove dedicated optional char from keyword group
2025-09-29  fb5f0ff4  Assignment Regex Implementation    <-- MR !151 lands
```

`1eb45282` (2025-11-25) is an ancestor of the pinned `59ada1f4` (2026-11-03) —
`/api/v4/…/repository/compare?from=1eb45282&to=59ada1f4…` returns 47 commits
and a diff line `assignmentOperand = `[="' :>\],\t.()\\?|]{1,10}``.

**The corpus scanner implements the old window.** `corpus/instruments/capture-secret-scan.py:318-320`:

```python
    ("gitlab-session-cookie", re.compile(
        _GL_LB + rb"_gitlab_session(?:_geo_[0-9a-f]{64})?[^\n]{0,8}[:=][^\n]{0,8}"
        rb"(?:cell-[0-9]+-)?[0-9a-f]{64}(?![0-9a-f])")),
```

That is a faithful transcription of MR !151's `.{0,8}[:=].{0,8}` — and it is
exactly what the corpus cites (`S150`'s `teaches` cell: "`assignmentContext`
expands a rule to `<keyword>.{0,8}[:=].{0,8}<value>`").

**Measured gap.** Testing 13 separator characters against the corpus pattern
and against the upstream-at-`59ada1f4` window (receipt
`upstream-window-evolution-r99.txt`):

```
sep        corpus scanner   upstream@59ada1f4    gap
space      False            True                 GAP
dquote     False            True                 GAP
apos       False            True                 GAP
gt         False            True                 GAP
rbracket   False            True                 GAP
comma      False            True                 GAP
tab        False            True                 GAP
dot        False            True                 GAP
lparen     False            True                 GAP
question   False            True                 GAP
pipe       False            True                 GAP
colon      True             True
eq         True             True

GAPS: ['space','dquote','apos','gt','rbracket','comma','tab','dot','lparen','question','pipe'] (11)
```

The corpus scanner agrees with the MR !151 window on all 13 separators
(`corpus-vs-MR151-window disagreements: NONE`) — so the round-99 C2 work is
*internally* correct against the source it cited. The defect is that **the
source it cited is superseded at the commit the corpus itself pins for the
same feature.** A session cookie separated by a space, quote, comma, pipe or
bracket is what upstream detects today and the corpus misses.

Note the direction of the mistake is safe-fail (the corpus misses values upstream
would catch) — but it is a **coverage** miss on the round's own headline
capability, and the corpus's own `S150` `teaches` cell asserts the narrower
window as *the* rule: "a separator model narrower than that window misses real
values." By that sentence's own logic the corpus's own model is now too narrow.

### Inference

The corpus cites the **MR description** (a proposal that was merged and then
superseded) rather than the **generator implementation at the pinned commit**.
The MR page's "Generated Regex" block is a *sample* of one rule
(`API_SECRET_KEY`/`api_secret_key`/…), and the constant it shows was the
implementation's value at merge time only.

### Recommended actions (not taken — this seat is read-only)

1. **Add a new source row** for the generator implementation at the pinned
   commit — `pkg/rules/assignment_regex.go` at `59ada1f4`, byte-stable
   (9,776 bytes, sha256 `91519731800ab8d96a00a03fff44e72c…`), capture-able via
   the same API raw URL pattern that already serves `S140` and `S148`. This is
   the same URL family the corpus already trusts; it is a **new source**, not a
   correction to `S150`, because `S150` (the MR description) is a different
   document from the generator source. Tier: `code`, tier B (same class as
   `S150`/`S140`).
2. **Re-ground the scanner's separator model** on the upstream-at-`59ada1f4`
   window `[="' :>\],\t.()\\?|]{1,10}` (or a superset), and re-run the
   twelve MUST-FIX + ten boundary-negative sentinel battery. The corpus's
   `S150` `teaches` cell would then need the erratum that the MR form was the
   merge-time value and the pinned-commit value is the wider class.
3. This is a **coverage** correction, not a **verifiability** one: it does not
   weaken any tamper-evidence claim.

---

## F2 — `S150`'s anchor digest is not reproducible (depth:verifiability, HIGH)

### Observed

`corpus/SOURCES.md:162` (`S150` row) `anchor` cell:

> The MR description's "Generated Regex" block and its `keywordGroupType` enum
> sentence (HTTP 200, 128,120 bytes, sha256
> `aa60d7af465cad03b64259362dfa862a8d5c3176ebc2e6b5909a38daddea11e8`, opened
> 2026-11-07)

Re-fetching that exact URL today (receipt `s150-refetch-r99.txt`):

```
URL: https://gitlab.com/gitlab-org/security-products/secret-detection/secret-detection-rules/-/merge_requests/151
fetch1 status=200 bytes=128120  ff150c0bc071b8717a5cac7b3a3a2a39eb42fee4c9f9056887ea5caa1e1aaae4
fetch2 status=200 bytes=128120  7d28f2e38c69591530c385aacec7f557d1f25173bc81f058a2aed67549de5eb4
```

Two fetches, **same byte length (128,120)**, **different sha256**. The digest
also varies with the user agent:

```
UA=curl/8.0                          -> 9d5f3b7d965a3643
UA=Mozilla/5.0 (X11; Linux x86_64)   -> 8ab80f2d6959dd58
UA=kasegi-shokunin/1.0 (doc capture) -> 6fd15f6238c7d59e
UA=gitlab-source-capture/1.0          -> 24683a87f24ea700
recorded in SOURCES.md S150 anchor cell: aa60d7af465cad03
```

Across this seat's eight fetches of the URL (default curl ×2, three further
UAs, the instrument's own UA ×3), **no fetch produced `aa60d7af…`**. The
cause is visible in the diff between two fetches: a per-response CSP
`<script nonce="…">` value, a per-response `X-CSRF-Token`, a per-response
snowplow `correlation_id`, and a per-response `context_generated_at` timestamp.
The MR's *content* is constant; the *envelope* is not.

This is precisely the defect the corpus already named and already has a
precedent for. `corpus/QUALITY.md:518` (R100):

> **R100** | A source row's anchor digest is the normalized snapshot digest or
> a byte-stable artifact's digest; a raw response digest that varies between
> fetches of the same page is recorded as a nonce-bound instance digest and
> never carried into a row. | M67-8: the round-65 lead pinned the FIRST
> maturity page's raw HTML digest `334aeb01…`, which six fetches could not
> reproduce (per-response CSP nonce, identical 82978-byte length, one
> normalized digest); the lead is retired as S100/S101 with the correction
> stated in `corpus/SOURCES.md`.

The S100/S101 precedent (`corpus/SOURCES.md:151-152`) is the **correct
pattern**: `S100`'s anchor cell carries the **snapshot** digest
(`cf834a65…`, `corpus/source-snapshots/round-67/S100.txt`) and explicitly
states *"the raw HTML carries a per-response CSP nonce so only the snapshot
digest is stable."*

`S150` carries the raw response digest and has **no capture snapshot** — there
is no `corpus/source-snapshots/round-99/` directory and no `S150.txt`
anywhere under `corpus/source-snapshots/`:

```
$ find corpus/source-snapshots -iname "*S150*"
(no output)
$ grep -rln "S150" corpus/source-snapshots/
(no output)
```

So `S150` is the only round-93-and-later row in the registry with a live-URL
anchor, no capture, and a non-reproducible digest.

### The MR content itself does check out

The two located quotes are present and verbatim (MR description extracted from
the `data-noteable-data` attribute, and from the API JSON — byte-identical
descriptions, confirmed `HTML desc == API desc: True`):

- "Generated Regex:" block —
  `(?:API_SECRET_KEY|api_secret_key|apiSecretKey|SECERT_KEY|secret_key|secretKey).{0,8}[:=].{0,8}([a-z]{32})\b`
- `keywordGroupType` enum sentence —
  *"Indicates whether to inject `keywordGroup` directly as provided, or generate
  multiple case variant combinations"* (MR description, item 2 of the schema
  list)

Both are ≤25 words and are correctly located. The `teaches` cell's paraphrase
("`assignmentContext` expands a rule to `<keyword>.{0,8}[:=].{0,8}<value>`,
and `keywordGroupType raw` injects the keyword group verbatim") is accurate as
a statement **about MR !151**. It is not accurate as a statement about
upstream today — see F1.

### The byte-stable alternative already exists

The GitLab **API** endpoint for the same MR is byte-stable (receipt
`s150-refetch-r99.txt`):

```
api fetch1 status=200 bytes=10184  5e3c498482f742f84b7ba04972d61a96e4b853807a07b8da628e7aa36475abf2
api fetch2 status=200 bytes=10184  5e3c498482f742f84b7ba04972d61a96e4b853807a07b8da628e7aa36475abf2
description sha256: 3d35fbcd8be0cafc41655f4f808d6ac9b21c33e15c7d294dfdd86d6d4afba986 (3826 bytes)
state: merged  merged_at: 2025-09-29T11:34:55.310Z  sha: c9c3924931732522c172d1987521749d33641e1b
```

This is the same capture method the corpus already uses for `S140` and `S148`
(`/api/v4/projects/…/repository/files/…/raw?ref=…`), and the same URL family
the corpus's own `S148` row cites.

### Recommended actions (not taken)

1. Capture the MR description into `corpus/source-snapshots/round-99/S150.txt`
   with a `manifest.json` (per **R20**: a capture snapshot directory ships its
   `manifest.json` in the same round and commit), and change `S150`'s
   `anchor` cell to carry the **snapshot** digest, naming the nonce as the
   reason the raw digest is not carried — the `S100` wording pattern.
2. Alternatively (or additionally) cite the API JSON digest
   `5e3c4984…`, which reproduces exactly. Whichever is chosen, the row must
   not carry `aa60d7af…`.
3. This is a `depth:verifiability` correction and does **not** touch the
   round-99 C1 tamper-evidence claim, nor the C2 scan semantics.

---

## F3 — `S140`'s anchor cell cites snapshot line numbers under the upstream file's name (depth:verifiability, MEDIUM)

### Observed

`corpus/SOURCES.md:152` (`S140` row) `anchor` cell reads:

> file `rules/mit/gitlab/gitlab.toml` at commit 59ada1f4ca53d5a69fafb9cb0f10bb893720ce39;
> **snapshot lines 4, 114, 255** (and 30, 51, 136, 324 for the routable forms
> kept as limits)

The word "snapshot" appears once, after "file … at commit …". A verifier who
reads the row as "these are lines 4/114/255 of the upstream file at that
commit" gets the wrong text. Upstream (receipt `s140-line-drift-r99.txt`):

```
raw 4    regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glpat-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''   <- matches
raw 114  pushProtection = true                                                             <- does NOT match
raw 255  name = "GitLab"                                                                  <- does NOT match
```

The snapshot's own lines do match the row's citations:

```
snap 4    regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glpat-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''
snap 114  regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glrtr?-(?:t[1-3]_)?[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''
snap 255  regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?gldt-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''
```

**Cause:** the snapshot replaced the 82 `examples`/`negativeExamples` array
element lines with one marker line each and dropped every blank line, so
line numbers drift monotonically. Measured drift for all 30 rules
(receipt `s140-line-drift-r99.txt`): 0 at `gitlab_personal_access_token`,
growing to **29** at `gitlab_session_cookie`.

**This also affects the round-99 citations.** The knowledge entry
`corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md:3` cites
"lines 291-294, 478-481, 495-498 and 547-551" and the round-99 lesson
`corpus/lessons/round-99.md:31` cites "lines 547-551". Those are snapshot
lines; upstream they are different rules:

```
--- the corpus cites 'S140:547-551' for the session-cookie block ---
snapshot 547: id = "gitlab_session_cookie"
snapshot 548: keywords = ["_gitlab_session"]
snapshot 549: regex = '''(?:cell-[0-9]+-)?[0-9a-f]{64}'''
snapshot 550: assignmentContext.keywordGroup = '''_gitlab_session(?:_geo_[0-9a-f]{64})?'''
snapshot 551: assignmentContext.keywordGroupType = "raw"
--- what upstream raw 547-551 actually holds ---
raw      547: tags = ["gitlab", "gitlab_blocking"]
raw      548: type = "token"
raw      549: maturity = "stable"
raw      550: [rules.vendor]
raw      551: name = "GitLab"
--- upstream raw 576-580 (the true upstream session-cookie block) ---
raw      576: id = "gitlab_session_cookie"
raw      577: keywords = ["_gitlab_session"]
raw      578: regex = '''(?:cell-[0-9]+-)?[0-9a-f]{64}'''
raw      579: assignmentContext.keywordGroup = '''_gitlab_session(?:_geo_[0-9a-f]{64})?'''
raw      580: assignmentContext.keywordGroupType = "raw"
```

Upstream 547-551 is the **tail of `gitlab_pipeline_trigger_token_in_url`**;
upstream 576-580 is the session-cookie block. The manifest's own `quotes`
anchors (`4`, `114`, `255`) are snapshot anchors and are internally consistent
— the drift is between *upstream* and *snapshot*, and the row's cell names the
upstream file while quoting snapshot numbers.

### Also worth noting

The `S140` row's `anchor` cell says "capture corpus/source-snapshots/round-94/S140.txt",
which is correct and re-verifiable: the committed capture's digest matches the
round-94 manifest exactly (`f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`,
563 lines) and the pinned upstream raw still reproduces the manifest's raw digest
(`14854f71f81f2400ac33a950cd70850cbdc80c319e4bdb0445bff6dbc36a11b5`, 20,228
bytes — byte-identical to `main` today, receipt `s140-s148-refetch-r99.txt`).
The `/-/raw/` URL (the row's own URL) answers **HTTP 403** (Cloudflare
"just a moment" challenge, 6,078 bytes, sha256
`bd29de2819ac75d2b953791bc016b01ff77ed9bf24ffa726a724315a16c5c19b`) — the
round-99 lesson's statement that the live `/-/raw/` fetch 403s is **confirmed**.

### Recommended actions (not taken)

1. Make the coordinate system explicit in the `S140` row's `anchor` cell
   (e.g. "capture lines 4/114/255 — upstream lines 4/119/268"), or cite the
   upstream coordinates for the upstream file. Same for
   `corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md:3` and
   `corpus/lessons/round-99.md:26`.
2. Consider recording the drift table (rule id → raw line / snapshot line) in
   the round-94 manifest so a verifier can map either coordinate system.

---

## Item 3 — is a new row warranted for the round-99 finding?

**Yes — one new row is warranted, and it is not the one the corpus added.**

The round-99 finding is *the separator window that upstream's assignment-context
generator uses*. The corpus grounded that window on the **MR !151 description**
(`S150`), which is a merged-then-superseded proposal. The generator
**implementation** at the corpus's own pinned commit is a distinct, byte-stable,
machine-readable source that states the window as a Go constant — and states a
**different** window. That is new ground, so a new row is warranted:

- **Candidate row `S151`**: GitLab secret-detection rules,
  `pkg/rules/assignment_regex.go` at commit
  `59ada1f4ca53d5a69fafb9cb0f10bb893720ce39` —
  `https://gitlab.com/api/v4/projects/gitlab-org%2Fsecurity-products%2Fsecret-detection%2Fsecret-detection-rules/repository/files/pkg%2Frules%2Fassignment_regex.go/raw?ref=59ada1f4ca53d5a69fafb9cb0f10bb893720ce39`
  — kind `code`, tier B, status `mined`.
- Located quote (line 28, 9,776 bytes, sha256
  `91519731800ab8d96a00a03fff44e72c…`, byte-stable across three fetches):
  *"assignmentOperand specifies the possible delimiters, used between the LHS and RHS variables in an assignment."*
- Teaches: the assignment-context separator is the **character class**
  `[="' :>\],\t.()\\?|]{1,10}` at the pinned commit — not the merge-time
  `.{0,8}[:=].{0,8}`.

The corpus's own lesson already rejected one candidate new row as a duplicate
(`corpus/lessons/round-99.md:43`, the round-98 sentinel's MR quote). That
rejection is **correct** — the sentinel's quote is the same MR page, and
`S150` now carries the URL. The generator source file is a **different
document** at a **different URL**, so it does not duplicate `S150`.

### Does S148's prose state the separator, or only the value shape?

**Only the value shape.** `S148`'s capture is byte-stable and reproduces
exactly (two fetches, 1,028 bytes, sha256
`b50856e4413c392ffe47fd0f212d5dd22067d52db710a7a8f93a11e9182ac319`, matching
the row's recorded digest). Its full text:

```
5  A GitLab session cookie was identified. The `_gitlab_session` cookie identifies a signed-in browser session.
6  The value is a 64-character hexadecimal session ID, with an optional `cell-<ID>-` prefix.
```

Line 6 states the **length (64) and alphabet (hex)** and the optional
`cell-<ID>-` prefix. It says nothing about a separator, an assignment context,
or a delimiter window — `grep -c "separator\|assignment" ` over the 23-line
capture returns 0 for those terms, and the only `:`/`=` occurrences are inside
URLs and headings.

**Consequence:** the separator window is grounded **only** by `S150` (the MR)
and, correctly, by the rules file's own `assignmentContext` block
(`S140` snapshot lines 549-551 / upstream 578-580) — which names the
`keywordGroup` and `keywordGroupType` but **not** the separator. This is
precisely why `S150`/`S151` matters and why the corpus cannot ground the
separator from `S148` or from `S140` alone.

---

## Item 4 — the remaining S140 rules the scanner does not cover

`S140`'s pinned file publishes **30** `[[rules]]` entries; the scanner carries
**25** `gitlab-*` patterns (`capture-secret-scan.py:293-346`). Empirical
coverage test, one synthetic non-published value per rule, against the real
scanner's `patterns()` (receipt `s140-30-rule-coverage-r99.txt`):

### Not covered by any `gitlab-*` pattern (2 rules)

| Rule id | Upstream line | S140 snapshot line | Shape |
|---|---|---|---|
| `gitlab_runner_auth_token_legacy_partition` | 321 | 306 | `t[1-3]_` + exactly 20 of `[1-9a-km-zA-HJ-NP-Z_-]`, at line start or after a non-`[0-9a-zA-Z_\-\r\n]` char. **No `glrt-` prefix.** |
| `gitlab_feed_token_path_dependent` | 539 | 512 | optional `[a-zA-Z0-9]{1,20}-` + `glft-` + exactly 64 lowercase hex + `-` + 1-20 digits. |

Both are **already documented** as known limits — the scanner's docstring
(`capture-secret-scan.py:211-216`: *"the path-dependent feed-token form
(`glft-` + 64 hex + `-` + 1-20 digits, S140 line 512), the `t1_`-prefixed
runner token without `glrt-` (S140 line 308)"*) and
`corpus/knowledge/gitlab-remaining-token-families.md:87-89`. So these are
**known, documented gaps**, not round-99 regressions. (Both citations resolve
correctly against the *snapshot*; upstream they are lines 541 and 323.)

### Covered only by the generic gate pattern (1 rule)

| Rule id | Upstream line | S140 snapshot line | Shape | Hits |
|---|---|---|---|---|
| `gitlab_pipeline_trigger_token_in_url` | 558 | 530 | `/trigger/pipeline?` + up to 10 `key=value&` pairs + `token=` + 30 lowercase hex | generic `credential` (`claim-package-check.py:140`), not a `gitlab-*` pattern |

Also already documented as a known limit (`capture-secret-scan.py:215-216`,
`gitlab-remaining-token-families.md:89`).

### The 27 rules the scanner covers with a `gitlab-*` pattern

`gitlab_personal_access_token`, `…_routable`, `…_routable_versioned`,
`gitlab_pipeline_trigger_token`, `gitlab_runner_registration_token`,
`gitlab_runner_auth_token`, `…_routable`, `gitlab_feed_token`,
`gitlab_oauth_app_secret`, `gitlab_feed_token_v2`,
`gitlab_kubernetes_agent_token`, `gitlab_incoming_email_token`,
`gitlab_deploy_token`, `gitlab_scim_oauth_token`, `gitlab_ci_build_token`,
`gitlab_deploy_token_routable`, `gitlab_deploy_token_in_url`,
`gitlab_kubernetes_agent_token_routable`, `gitlab_workspace_token`,
`gitlab_feature_flags_client_token`, `gitlab_runner_controller_token`,
`gitlab_ci_build_token_jwt`, `gitlab_stateless_access_token`,
`gitlab_iam_access_token`, `gitlab_iam_refresh_token`,
`gitlab_iam_authorization_code`, `gitlab_session_cookie`.

### The round-99 delta is entirely inside `gitlab_session_cookie`

The only rule whose coverage changed this round is `gitlab_session_cookie`
(upstream 576 / snapshot 547). Before round 99 the scanner had no separator at
all; it now has the MR !151 window. The 11-character gap of **F1** sits inside
that same rule and is the one place where the corpus is behind upstream.

---

## Citations, with URL + date + located quote (≤25 words each)

| # | Source | URL | Date | Quote (located) |
|---|---|---|---|---|
| Q1 | MR !151 description, "Generated Regex" block | `https://gitlab.com/gitlab-org/security-products/secret-detection/secret-detection-rules/-/merge_requests/151` | 2026-11-07 (fetched) | `(?:API_SECRET_KEY\|api_secret_key\|apiSecretKey\|SECERT_KEY\|secret_key\|secretKey).{0,8}[:=].{0,8}([a-z]{32})\b` |
| Q2 | MR !151 description, `keywordGroupType` enum sentence | same URL | 2026-11-07 | "Indicates whether to inject `keywordGroup` directly as provided, or generate multiple case variant combinations" |
| Q3 | Generator implementation at the pinned commit | `…/repository/files/pkg%2Frules%2Fassignment_regex.go/raw?ref=59ada1f4…` | 2026-11-07 | "assignmentOperand specifies the possible delimiters, used between the LHS and RHS variables in an assignment." |
| Q4 | Generator implementation, the constant itself | same URL | 2026-11-07 | `assignmentOperand = `[="' :>\],\t.()\\?|]{1,10}`` |
| Q5 | Generator implementation at the MR merge sha | `…/raw?ref=c9c39249…` | 2026-11-07 | `assignmentOperand = `.{0,8}[:=].{0,8}`` |
| Q6 | S140 rules file, session-cookie rule | `…/repository/files/rules%2Fmit%2Fgitlab%2Fgitlab.toml/raw?ref=59ada1f4…` | 2026-11-07 | `assignmentContext.keywordGroup = '''_gitlab_session(?:_geo_[0-9a-f]{64})?'''` |
| Q7 | S148 rule prose, session cookie | `…/repository/files/rules%2Fmit%2Fgitlab%2Fgitlab_session_cookie.md/raw?ref=59ada1f4…` | 2026-11-07 | "The value is a 64-character hexadecimal session ID, with an optional `cell-<ID>-` prefix." |
| Q8 | S140 rules file, legacy partition rule | same as Q6 | 2026-11-07 | `regex = '''(?:(?m:^)\|[^0-9a-zA-Z_\-\r\n])(t[1-3]_[1-9a-km-zA-HJ-NP-Z_\-]{20})(?:[^0-9a-zA-Z_\-]\|$)'''` |
| Q9 | S140 rules file, path-dependent feed token | same as Q6 | 2026-11-07 | `regex = '''\b(?:[a-zA-Z0-9]{1,20}-)?glft-[0-9a-f]{64}-[0-9]{1,20}\b'''` |
| Q10 | S140 rules file, pipeline trigger in URL | same as Q6 | 2026-11-07 | `regex = '''/trigger/pipeline\?(?:[0-9a-zA-Z_.%\[\]=-]{1,100}&){0,10}token=([0-9a-f]{30})\b'''` |

---

## Registry census — unchanged

```
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
kasegi	W04	S076 duplicate url docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories across scopes
kasegi	W04	S080 duplicate url ossf.github.io/osv-schema across scopes
kasegi	W04	S085 duplicate url csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema across scopes
kasegi	W04	S143 duplicate url gitlab.com/gitlab-org/security-products/secret-detection/secret-detection-rules/-/blob/59ada1f4ca53d5a69fafb9cb0f10bb893720ce39/rules/mit/github/github.toml across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
rc=0
```

The seven inherited W04 warnings (S028, S029, S072, S076, S080, S085, S143)
are unchanged; the registry holds 150 rows.

---

## Claims this seat checked, and their status

| Claim | Status | Evidence |
|---|---|---|
| S150 MR page is live at HTTP 200, 128,120 bytes | **CONFIRMED** | receipt `s150-refetch-r99.txt`, 8 fetches all HTTP 200 / 128,120 bytes |
| S150's anchor digest `aa60d7af…` is the MR page's digest | **REFUTED** | 8 fetches, 8 distinct digests, none `aa60d7af…`; per-response CSP nonce / CSRF token / correlation id / timestamp |
| S150's "Generated Regex" block states `.{0,8}[:=].{0,8}` | **CONFIRMED** | Q1; present verbatim in both the HTML page and the API JSON (descriptions byte-identical) |
| S150's `keywordGroupType` enum sentence exists as quoted | **CONFIRMED** | Q2; the quoted clause is verbatim |
| S140's live `/-/raw/` fetch answers 403 (Cloudflare) | **CONFIRMED** | receipt `s140-s148-refetch-r99.txt`: HTTP 403, 6,078 bytes, "Just a moment…" |
| S140's commit-pinned API raw reproduces the manifest's raw digest | **CONFIRMED** | `14854f71…`, 20,228 bytes — identical to the round-94 manifest; byte-identical to `main` today |
| S148's capture digest `b50856e4…` reproduces | **CONFIRMED** | two fetches, both 1,028 bytes, both `b50856e4…` |
| S148's prose states the separator | **REFUTED** | Q7: only length + alphabet + optional `cell-<ID>-` prefix; no separator/delimitor term in 23 lines |
| S140 publishes 30 rules | **CONFIRMED** | 30 `id = ` entries in the pinned raw file |
| The scanner's separator model matches upstream at the pinned commit | **REFUTED** | 11 separator characters accepted upstream, refused by the scanner (F1) |
| The scanner's separator model matches upstream at the MR merge sha | **CONFIRMED** | corpus == MR !151 window on all 13 separators tested |
| The 2 uncovered S140 rules are undocumented | **REFUTED** | both are in `capture-secret-scan.py:211-216` and `gitlab-remaining-token-families.md:87-89` |

---

## VERDICT lines

- **F1 (upstream separator window superseded; 11-char coverage gap):** VERDICT: **NOT STANDS** — the corpus implements MR !151's `.{0,8}[:=].{0,8}`, while its own pinned commit `59ada1f4` carries `[="' :>\],\t.()\\?|]{1,10}`; 11 separator characters upstream accepts are refused. A new row for `pkg/rules/assignment_regex.go` at `59ada1f4` is warranted, and the scanner's window must be re-grounded on it.
- **F2 (S150 anchor digest not reproducible):** VERDICT: **NOT STANDS** — `aa60d7af…` was not reproduced by any of 8 fetches (identical 128,120-byte length, per-response nonce/CSRF/correlation-id/timestamp); the row violates corpus rule R100 by name and has no capture snapshot, unlike every other round-93+ row. The API JSON digest `5e3c4984…` reproduces exactly and is the correct anchor.
- **F3 (S140 anchor cell cites snapshot lines under the upstream file's name):** VERDICT: **NOT STANDS** — upstream lines 4/114/255 do not hold the quoted regexes (upstream 114 = `pushProtection = true`, upstream 255 = `name = "GitLab"`); the drift reaches 29 lines by `gitlab_session_cookie` (upstream 576-580 vs snapshot 547-551). The row's citations are correct against the capture and wrong against the upstream file it names.
- **Item 3 (new row warranted for the round-99 finding):** VERDICT: **YES** — a new row for the generator implementation at the pinned commit (`pkg/rules/assignment_regex.go`, 9,776 bytes, sha256 `91519731800ab8d96a00a03fff44e72c…`, byte-stable over three fetches) is new ground and does not duplicate S150; the lesson's rejection of the sentinel's MR quote as a duplicate is correct.
- **Item 3 (does S148's prose state the separator?):** VERDICT: **NO — value shape only.** S148 states "The value is a 64-character hexadecimal session ID, with an optional `cell-<ID>-` prefix." and nothing about a separator; the separator is groundable only from S150 (and, correctly, from the new implementation row).
- **Item 4 (remaining S140 rules the scanner does not cover):** VERDICT: **2 undocumented-shape gaps + 1 generic-only hit.** `gitlab_runner_auth_token_legacy_partition` (bare `t1_`/`t2_`/`t3_` + 20 chars, upstream 321 / snapshot 306) and `gitlab_feed_token_path_dependent` (`glft-` + 64 hex + `-` + 1-20 digits, upstream 539 / snapshot 512) have no `gitlab-*` pattern; `gitlab_pipeline_trigger_token_in_url` (upstream 558 / snapshot 530) hits only the generic `credential` gate shape. All three are already named as known limits in the instrument docstring and in `gitlab-remaining-token-families.md`; the other 27 of S140's 30 rules are covered by a `gitlab-*` pattern.
- **Round-99 C2 separator window as implemented (against its own cited source, MR !151):** VERDICT: **STANDS** — the corpus pattern equals the MR !151 window on all 13 separator characters tested; the defect is the source choice (F1), not the transcription.
- **Round-99 C2 twelve MUST-FIX / ten boundary-negative probe and the 170 → 192 selftest:** VERDICT: **NOT RE-RUN BY THIS SEAT** — the probe is C2's own control (`.ufo/waves/round-99/controls/c2-probe-candidate-r99.txt`, `c2-landing-r99.txt`); this seat verified sources only, and the scanner's behaviour was exercised directly for the F1 gap test and the 30-rule coverage test (receipts `upstream-window-evolution-r99.txt`, `s140-30-rule-coverage-r99.txt`).
- **Round-99 C1 tamper-evident census:** VERDICT: **NOT IN SCOPE FOR THIS SEAT** — source reconnaissance only; no claim made or refuted about `corpus/instruments/census-at-rev.py` or the 12-class harness.
- **Registry census `kasegi ok` rc 0 with seven inherited W04 warnings:** VERDICT: **CONFIRMED** — observed output above.
