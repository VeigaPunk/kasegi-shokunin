source: S140 — GitLab secret-detection rules, `rules/mit/gitlab/gitlab.toml` at commit 59ada1f4, capture lines 30, 51, 73, 136, 324, 358 and 375 (capture `corpus/source-snapshots/round-94/S140.txt`, example values structurally redacted, line numbering preserved); S144 — GitLab Docs, Security — Tokens, https://docs.gitlab.com/security/tokens/ (capture `corpus/source-snapshots/round-96/S144.txt:346-347`, 17,591 bytes / 418 lines (`wc -l`) / sha256 `d6e529275deb3ecf4ea2c3edaff2caa882760680cf23c1a134424e6acffdb83d`)
verified-at: 7ef1d365eb523a83b2567342a6c0f585ab028ab0
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B corpus/instruments/anchorcheck.py corpus/knowledge/gitlab-routable-and-versioned-token-forms.md && sed -n '346p' corpus/source-snapshots/round-96/S144.txt | grep -q 'these prefixes cannot be configured' && test "$(sed -n '30p;51p;73p;136p;324p;358p;375p' corpus/source-snapshots/round-94/S140.txt | grep -c 'regex')" = 7 && python3 -B corpus/instruments/capture-secret-scan.py --selftest >/dev/null && echo RECHECK-OK

# GitLab routable and versioned-routable token forms, and the pipeline trigger token

Seven GitLab token shapes the capture scanner could not express before round 96.
All seven are rules in GitLab's own secret-detection ruleset (S140); the prefix
set they share is stated first-party in GitLab's documentation (S144).

## Why the plain shape misses the family

The round-94 scanner matched `glpat-` plus exactly 20 characters and required
the next byte to be outside `[A-Za-z0-9_-]`
(`corpus/instruments/capture-secret-scan.py:255`). A routable token continues
past those 20 characters, so that right boundary refuses it: the 21st character
is still alphanumeric. Every versioned form behaves the same way. A shape that
knows only the 20-character prefix therefore reports nothing for the whole
family, which is why these forms were a named limit in the instrument's
docstring until round 96.

## The two tails

S140 publishes two suffixed tails, one dot apart:

| tail | S140 grammar | shape of the suffix |
|---|---|---|
| routable | `\.[0-9a-z]{2}[0-9a-z]{7}` | a 2-character route then a 7-character check |
| versioned-routable | `\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7}` | a version, then a route, then the check |

Both tails are lower-case (`[0-9a-z]`) while the head is mixed-case
(`[A-Za-z0-9_-]`), so an upper-case character after the first dot is not a
match. The head is `{27,300}` characters, not the plain token's 20.

## The seven shapes

| shape | head | tail | S140 line |
|---|---|---|---|
| `gitlab-pat-versioned` | `glpat-`, optional instance prefix | versioned | 51 |
| `gitlab-pat-routable` | `glpat-`, optional instance prefix | routable | 30 |
| `gitlab-runner-auth-token-versioned` | `glrt-`/`glrtr-` | versioned | 136 |
| `gitlab-deploy-token-versioned` | `gldt-`, optional instance prefix | versioned | 324 |
| `gitlab-agent-token-versioned` | `glagent-`, optional instance prefix | versioned | 358 |
| `gitlab-workspace-token-versioned` | `glwt-`, optional instance prefix | versioned | 375 |
| `gitlab-pipeline-trigger-token` | `glptt-`, optional instance prefix | none: exactly 20 or exactly 40 characters | 73 |

The landed matchers are the two tail fragments at
`corpus/instruments/capture-secret-scan.py:242-243` and the seven patterns at
`corpus/instruments/capture-secret-scan.py:247-254`.

The order in which they are tried matters only for reporting. A versioned token
cannot match the routable pattern, because after the 2-character route comes a
dot rather than the 7-character check; a routable token cannot match the
versioned pattern, because there is no second dot. A plain 20-character token
matches neither, because both heads require at least 27 characters.

## Boundaries the scanner enforces

- **Left**: the escape-terminator family
  (`corpus/instruments/capture-secret-scan.py:237`): the match may not be
  preceded by a letter, digit or `_`, and may follow `\t`/`\r`/`\n`, `\uXXXX`,
  `%XX`, `&#NN;` or `&#xNN;`.
- **Right**: `(?![A-Za-z0-9_])` after the tail, so a longer alphanumeric run is
  not truncated into a hit. The `glptt-` shape uses `(?![A-Za-z0-9_-])`, which
  also refuses a trailing `-`.
- **Instance prefix**: `(?:[A-Za-z0-9]{1,20}-)?`
  (`corpus/instruments/capture-secret-scan.py:238`) on the shapes whose rule
  publishes one.

## The instance prefix on the runner versioned shape

S140 line 136 publishes the optional instance prefix on the runner versioned
rule as well (`(?:[a-zA-Z0-9]{1,20}-)?` before `glrtr?-`). The landed matcher
does not consume it (`corpus/instruments/capture-secret-scan.py:249`), so a
custom-prefixed runner token matches from `glrtr-` onward rather than from the
prefix. That shortens the matched span and cannot cause a miss: the left
boundary accepts the hyphen that precedes `glrtr-`
(`corpus/instruments/capture-secret-scan.py:237`).

## Why the prefix set is stable

GitLab states that "With the exception of Personal Access tokens, these
prefixes cannot be configured, as they are designed to be standard
identifications" (`corpus/source-snapshots/round-96/S144.txt:346-347`). The
prefix table on the same page lists `glpat-`, `gloas-`, `gldt-`,
`glrt-`/`glrtr-`, `glcbt-`, `glptt-`, `glft-`, `glimt-`, `glagent-`, `glwt-`,
`glsoat-` and `glffct-` (`corpus/source-snapshots/round-96/S144.txt:348-395`).
A shape keyed on a prefix therefore stays meaningful across instances. Only the
lengths and tails need the rules file, because the documentation page states
none.

## Known limits that remain

Taken from the instrument's own list
(`corpus/instruments/capture-secret-scan.py:159-175`):

- The other GitLab families: `glft-` (20), `glimt-` (20-25 lower-case),
  `glsoat-` (20), `glffct-` (20), `gloas-` (64) and `glrct-` (20), at S140
  lines 190, 229, 278, 392, 174 and 412.
- The runner registration token (`GR1348941` + 20, S140 line 101), the
  `feed_token=` query form (S140 line 160), the `gitlab+deploy-token-N:` URL
  form (S140 line 341), the bare `t1_`-prefixed runner token (S140 line 308)
  and the `/trigger/pipeline?...token=` URL form (S140 line 532).
- An encoded prefix separator (`glpat%2D`), a value soft-wrapped across lines,
  and gzip/UTF-16/base64-wrapped captures are not detected.
- `glptt-` accepts exactly 20 or exactly 40 characters as published; an
  intermediate length is deliberately not a hit.
