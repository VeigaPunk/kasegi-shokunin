source: S140 — GitLab secret-detection rules, `rules/mit/gitlab/gitlab.toml` at commit 59ada1f4, lines 30, 51, 73, 136, 324, 358 and 375 (capture `corpus/source-snapshots/round-94/S140.txt`, example values structurally redacted, line numbering preserved); S144 — GitLab Docs, Security — Tokens, https://docs.gitlab.com/security/tokens/ (capture `corpus/source-snapshots/round-96/S144.txt:346-347`, 17,591 bytes / 418 lines / sha256 `d6e529275deb3ecf4ea2c3edaff2caa882760680cf23c1a134424e6acffdb83d`)
verified-at: 7ef1d365eb523a83b2567342a6c0f585ab028ab0
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B corpus/instruments/anchorcheck.py corpus/knowledge/gitlab-routable-and-versioned-token-forms.md && sed -n '346p' corpus/source-snapshots/round-96/S144.txt | grep -q 'these prefixes cannot be configured' && sed -n '30p;51p;73p;136p;324p;358p;375p' corpus/source-snapshots/round-94/S140.txt | grep -c 'regex' && python3 -B corpus/instruments/capture-secret-scan.py --selftest >/dev/null && echo RECHECK-OK

# GitLab routable and versioned-routable token forms, and the pipeline trigger token

Seven GitLab token shapes the scanner could not express before round 96. Each is
a **published** rule in GitLab's own secret-detection ruleset (S140), and the
prefix set itself is a first-party statement in GitLab's documentation (S144).

## Why the plain shape misses them

The round-94 scanner matched `glpat-` + exactly 20 characters and required the
next character to be outside `[A-Za-z0-9_-]`
(`corpus/instruments/capture-secret-scan.py:255`). A *routable* token
continues past those 20 characters, so the right boundary refuses it: the
token's 21st character is alphanumeric. The same is true of every versioned
form. A shape that only knows the 20-character prefix therefore reports nothing
for the whole family — which is why these forms were a named limit in the
instrument's docstring until round 96.

## The two tails

S140 publishes two suffixed tails, and the difference is one dot:

| tail | S140 rule | meaning |
|---|---|---|
| routable | `.` + 2 lower-case alphanumerics + 7 (`\.[0-9a-z]{2}[0-9a-z]{7}`) | the token carries a 2-character route and a 7-character check |
| versioned-routable | `.` + 2 + `.` + 2 + 7 (`\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7}`) | the route is split into a version and a route |

Both tails are **lower-case** (`[0-9a-z]`) while the head is mixed-case
(`[A-Za-z0-9_-]`), so an upper-case character after the first dot is not a
match. The head floor is 27 characters (S140's `{27,300}`), not the plain
token's 20.

## The seven shapes

| shape | head | tail | S140 line |
|---|---|---|---|
| `gitlab-pat-versioned` | `glpat-` (optional 1-20 character instance prefix) | versioned | 51 |
| `gitlab-pat-routable` | `glpat-` (same prefix) | routable | 30 |
| `gitlab-runner-auth-token-versioned` | `glrt-`/`glrtr-` (S140 publishes an instance prefix; the landed matcher omits it and relies on the left boundary, which is equivalent because a prefix always ends with `-`) | versioned | 136 |
| `gitlab-deploy-token-versioned` | `gldt-` (instance prefix) | versioned | 324 |
| `gitlab-agent-token-versioned` | `glagent-` (instance prefix) | versioned | 358 |
| `gitlab-workspace-token-versioned` | `glwt-` (instance prefix) | versioned | 375 |
| `gitlab-pipeline-trigger-token` | `glptt-` (instance prefix) | none: exactly 20 or exactly 40 characters | 73 |

The landed matchers are
`corpus/instruments/capture-secret-scan.py:242-243` (the two tail fragments) and
`corpus/instruments/capture-secret-scan.py:247-254` (the seven patterns).

The order matters only for reporting: a versioned token cannot match the
routable pattern (after the 2-character route comes a dot, not the 7-character
check), and a routable token cannot match the versioned pattern (there is no
second dot). A plain 20-character token matches neither, because both heads
require at least 27 characters.

## Why the prefix set is stable

GitLab states that, "With the exception of Personal Access tokens, these
prefixes cannot be configured, as they are designed to be standard
identifications" (`corpus/source-snapshots/round-96/S144.txt:346-347`). The
prefix table on the same page lists `glpat-`, `gldt-`, `glrt-`/`glrtr-`,
`glcbt-`, `glptt-`, `glft-`, `glimt-`, `glagent-`, `glwt-`, `glsoas-`,
`glsoat-` and `glffct-` (`corpus/source-snapshots/round-96/S144.txt:348-395`).
A shape keyed on a prefix therefore stays meaningful across instances; only the
*lengths and tails* need the rules file, because the documentation page states
none.

## Boundaries the scanner enforces

- **Left**: the escape-terminator family (`corpus/instruments/capture-secret-scan.py:237`):
  not preceded by a letter, digit or `_`, or preceded by `\t`/`\r`/`\n`,
  `\uXXXX`, `%XX`, `&#NN;` or `&#xNN;`.
- **Right**: `(?![A-Za-z0-9_])` after the tail, so a longer alphanumeric run is
  not truncated into a hit.
- **Instance prefix**: `(?:[A-Za-z0-9]{1,20}-)?` where S140 publishes one
  (`corpus/instruments/capture-secret-scan.py:238`). The runner versioned rule
  publishes one as well; the landed matcher omits it and relies on the left
  boundary, which starts the match at `glrt-`/`glrtr-` instead of the prefix.
  Detection is the same for a prefix ending in `-` (and wider for a prefix
  longer than 20 characters, which the published rule would refuse); only the
  reported hit position differs.

## Known limits that remain

- The other GitLab families are still undetected: the plain `glagent-`
  50-character form (S140 line 213 — only the versioned `glagent-` form is
  detected), `glft-` (feed, 20), `glimt-`
  (incoming mail, 20-25 lower-case), `glsoat-` (SCIM, 20), `glffct-` (feature
  flags, 20), `gloas-` (OAuth application secret, 64), `glrct-` (20), the
  runner registration token (`GR1348941` + 20, S140 line 101), the
  `feed_token=` query form (S140 line 160), the `gitlab+deploy-token-N:` URL
  form (S140 line 341), the bare `t1_`-prefixed runner token (S140 line 308)
  and the `/trigger/pipeline?...token=` URL form (S140 line 532).
- A routable token whose head is split across a line wrap is not detected; the
  shapes are single-line by construction.
- The `glptt-` shape accepts exactly 20 or exactly 40 characters as published;
  an intermediate length is deliberately not a hit.
