# GitLab's ten remaining token families — the shapes S140 publishes

source: S140 — GitLab secret-detection rules, `rules/mit/gitlab/gitlab.toml` at commit 59ada1f4, lines 101, 160, 174, 190, 213, 229, 278, 341, 392 and 412 (capture `corpus/source-snapshots/round-94/S140.txt`, sha256 `f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`, 563 lines, example values structurally redacted, line numbering preserved); S146 — GitLab Docs, Deploy tokens, https://docs.gitlab.com/user/project/deploy_tokens/ (capture `corpus/source-snapshots/round-97/S146.txt:68-70`, 10,506 bytes / 238 lines / sha256 `a8e77bd6d351df2a5f8d8d5762e35bec7bb5be2b698fc0d4e2f5ee432f6145b5`)
verified-at: 2026-11-07 (both captures re-read at their pinned digests; the S140 live `/-/raw/` fetch answered HTTP 403 this round, so the committed capture is the citation base)
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B corpus/instruments/anchorcheck.py corpus/knowledge/gitlab-remaining-token-families.md && sed -n '101p;160p;174p;190p;213p;229p;278p;341p;392p;412p' corpus/source-snapshots/round-94/S140.txt | grep -c 'regex' && sed -n '68,70p' corpus/source-snapshots/round-97/S146.txt | grep -c 'deploy-token' && python3 -B corpus/instruments/capture-secret-scan.py --selftest >/dev/null && echo RECHECK-OK

## What this holds

GitLab's own secret-detection rules file publishes, beside the personal-access,
runner, deploy, workspace, agent and JWT forms the lane already holds, ten more
token families. Each is a fixed prefix plus an exact tail length, and one
(`glimt-`) is a lower-case-only alphabet as well. The rules file is the vendor's
machine-readable statement of what its own tokens look like; the documentation
page (S146) adds the HTTP username structure for the deploy-token URL form and
says the username can be customised.

| shape | prefix | tail | S140 line |
|---|---|---|---|
| `gitlab-runner-registration-token` | `GR1348941` | exactly 20 of `A-Za-z0-9_-`, no instance prefix | 101 |
| `gitlab-feed-token` | `feed_token=` | exactly 20 of `A-Za-z0-9_-` | 160 |
| `gitlab-oauth-app-secret` | `gloas-` | exactly 64 of `A-Za-z0-9_-`, no instance prefix | 174 |
| `gitlab-feed-token-v2` | `glft-` | exactly 20 of `A-Za-z0-9_-`, no instance prefix | 190 |
| `gitlab-kubernetes-agent-token` | `glagent-` (optional 1-20 instance prefix) | exactly 50 of `A-Za-z0-9_-` | 213 |
| `gitlab-incoming-email-token` | `glimt-` (optional 1-20 instance prefix) | 20-25 of `a-z0-9` only | 229 |
| `gitlab-scim-oauth-token` | `glsoat-` | exactly 20 of `A-Za-z0-9_-`, no instance prefix | 278 |
| `gitlab-deploy-token-in-url` | `gitlab+deploy-token-<digits>:` | exactly 20 of `A-Za-z0-9_-`, then `@` | 341 |
| `gitlab-feature-flags-client-token` | `glffct-` (optional 1-20 instance prefix) | exactly 20 of `A-Za-z0-9_-` | 392 |
| `gitlab-runner-controller-token` | `glrct-` (optional 1-20 instance prefix) | exactly 20 of `A-Za-z0-9_-` | 412 |

## The ten published rules, verbatim

Each quote is one line of `rules/mit/gitlab/gitlab.toml` at commit 59ada1f4,
reproduced exactly as the capture holds it (double-quoted TOML strings carry
`\\b`/`\\-`; triple-quoted strings carry `\b`/`\-`). Every quote is under 25
whitespace-separated words.

- S140:101 — `regex = "\\b(GR1348941[0-9a-zA-Z_\\-]{20})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)"`
- S140:160 — `regex = "\\b(feed_token=[0-9a-zA-Z_\\-]{20})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)"`
- S140:174 — `regex = "\\b(gloas-[0-9a-zA-Z_\\-]{64})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)"`
- S140:190 — `regex = "\\b(glft-[0-9a-zA-Z_\\-]{20})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)"`
- S140:213 — `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glagent-[0-9a-zA-Z_\-]{50})(?:[^0-9a-zA-Z_\-.]|\.[^0-9a-z]|\.$|$)'''`
- S140:229 — `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glimt-[0-9a-z]{20,25})(?:[^0-9a-zA-Z_\-]|$)'''`
- S140:278 — `regex = "\\b(glsoat-[0-9a-zA-Z_\\-]{20})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)"`
- S140:341 — `regex = '''gitlab\+deploy-token-[0-9]+:([0-9a-zA-Z_\-]{20})@'''`
- S140:392 — `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glffct-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''`
- S140:412 — `regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glrct-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''`

The landed matchers are `corpus/instruments/capture-secret-scan.py:289-309`.

## What the documentation adds, and what it does not

S146 states the deploy-token username structure in the HTTP authentication
framework: "The default username format is gitlab+deploy-token-{n}. You can specify a custom username when you create the deploy token." (S146:69-70, 18 words). It states no secret length and no alphabet, so the 20-character tail stays S140's ground (line 341).

S144 (round 96) states the prefix set and that the prefixes are standard
identifications; it states no lengths or tails either. A shape therefore needs
both sources for different reasons: the prefix from the documentation, the
length and alphabet from the rules file.

## Falsifiable rule

For each shape, a candidate that differs from the published length by one
character is not that shape: 19 or 21 characters fail the 20-length families,
63 or 65 fail `gloas-`, 49 or 51 fail the plain `glagent-` form, and an
upper-case tail fails `glimt-`. A reader can check this against the rules file's
own `{20}`/`{64}`/`{50}`/`{20,25}` quantifiers at the lines above, and against
the instrument's selftest cases (`gl-registration-short`, `gl-oauth-app-short`,
`gl-kubernetes-agent-short`, `gl-feed-token-v2-long`).

## Rejected over-generalizations

- **"The deploy-token URL form detects every deploy token."** Rejected: the
  shape matches the DEFAULT username `gitlab+deploy-token-<n>` only, and
  S146:70 says a custom username may be configured. A URL carrying a custom
  username is not detected, so the shape is a partial detector.
- **"A GitLab prefix is enough to detect its family."** Rejected: the plain
  `glagent-` form is 50 characters while the versioned `glagent-` form is a
  27-300 character head plus a dotted tail (S140:213 versus S140:358), and
  `glft-` is two different rules (S140:190 versus S140:512). A prefix-only
  matcher would either truncate a longer value or over-match a different rule.
- **"`GR1348941` takes an instance prefix like the other families."** Rejected:
  the registration-token rule has no optional `[a-zA-Z0-9]{1,20}-` group
  (S140:101), so `acme-GR1348941...` is not a hit under the published rule.

## Limits

- The path-dependent `glft-` form (`glft-` + 64 hex + `-` + 1-20 digits,
  S140:512), the bare `t1_` legacy partition token (S140:308) and the
  `/trigger/pipeline?...token=` URL form (S140:532) remain undetected and are
  named in the instrument's known-limits list.
- The rules file publishes shapes, not which of them are live on any instance;
  a hit is a shape match, never proof that the value is a working credential.
- Documentation only: this entry describes published patterns. It instructs no
  probing, scanning, logging in or submission against any host, and carries no
  credential material, session or private URL.
