---
source: S142 — GitHub Docs, Refreshing user access tokens, https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/refreshing-user-access-tokens (capture corpus/source-snapshots/round-95/S142.txt, line 169); S143 (supersedes S141) — GitLab secret-detection rules, rules/mit/github/github.toml at commit 59ada1f4, line 72 (the 76-character length); S140 — GitLab secret-detection rules, rules/mit/gitlab/gitlab.toml at commit 59ada1f4, lines 429, 446, 463 (the `eyJ` three-segment forms)
verified-at: 38e7319f44a9fab2978b59ffd43faf207cf62b32
recheck: python3 -B corpus/instruments/capture-secret-scan.py --selftest | grep -E 'gh-refresh|gl-jwt' (14 cases) and `python3 -B corpus/instruments/capture-secret-scan.py --rev master`
---

# GitHub refresh tokens and the GitLab JWT token family

Two provider shapes the capture scanner can now express, each grounded in a
first-party or vendor rule file and each bounded by an explicit length floor.

## GitHub refresh token — `ghr_` plus 76 characters

GitHub states the prefix in its own documentation: the token exchange returns a
`refresh_token` and "The token starts with `ghr_`" (S142, capture line 169; the
sentence is 5 words and sits in the response-field table). The *length* is not
on that page; GitLab's machine-readable GitHub rule file gives it as
`ghr_[0-9a-zA-Z]{76}` (S143, line 72; superseding S141), and the same file's measurement table
records `ghr total= 80 tail= 76` (a round-94 wave receipt derived the same 76
from that file). This lane therefore implements `ghr_` + exactly 76
alphanumerics, right-bounded by `(?![A-Za-z0-9_])`.

The 36-character classic family is unchanged: `gh[pousr]_` + 36 alphanumerics
still fires as `github-token`, and a `ghr_` token of 36 characters keeps that
hit (S136/S137, rounds 92). The 76-character rule is a *separate* shape
(`github-refresh-token`) precisely because a 36-character matcher with a right
boundary cannot match a 76-character value: its lookahead fails at character 37.

Boundary facts, all mutation-tested in round 95:

- 75 characters is not a hit; 77 characters is not a hit (a 76-character
  matcher with a right boundary cannot consume a longer value).
- The left boundary is the escape family (`\uXXXX`, `\r`/`\n`/`\t`, `%XX`,
  `&#NN;`, `&#xNN;` and non-identifier characters), so a JSON-joined
  `"log":"line\nghr_…"` is a hit and a letter immediately before the prefix
  (`xghr_…`) is not.
- A word ending in the letters is not a hit; the prefix must be preceded by a
  boundary and followed by exactly 76 token characters.

## GitLab JWT family — `glcbt-`, `glsat-`, `gliamat-`

GitLab's rules file publishes three JWT-shaped tokens as one grammar
(S140 lines 429, 446, 463):

```
(?:[a-zA-Z0-9]{1,20}-)?glcbt-eyJ[0-9a-zA-Z_-]{10,1000}\.eyJ[0-9a-zA-Z_-]{10,1000}\.[0-9a-zA-Z_-]{20,1000}
(?:[a-zA-Z0-9]{1,20}-)?glsat-eyJ…  (same grammar)
gliamat-eyJ…                       (same grammar, no instance prefix)
```

Facts a reader can act on:

- The head is `eyJ` (base64 of `{"`), so a `glcbt-` string whose first segment
  does not start with `eyJ` is not a hit.
- The first two segments carry a 10-character floor; the signature segment
  carries a **20**-character floor. A 19-character third segment is not a hit.
- `glcbt-` and `glsat-` accept a 1–20-character instance prefix (`acme-glcbt-…`);
  `gliamat-` carries no prefix in the vendor rule, and this lane's matcher
  reaches a prefixed `gliamat-` only through its left boundary, which is a
  documented superset, not a vendor claim.
- The left boundary is the same escape family as the other GitLab shapes, so
  `\u0020`-prefixed and HTML-entity-separated contexts are hits.

## Why the prefix and the length are separate evidence

Credential detectors that key on the prefix alone under-detect: a 76-character
refresh token defeats a 36-character matcher, and a JWT segment floor is what
distinguishes a token from a placeholder such as `glcbt-eyJ<header>.<payload>.
<signature>`. Both new shapes are therefore tested against the vendor's own
published examples and against documentation placeholders in the instrument's
selftest (cases `gh-refresh-*`, `gl-jwt-*`), which grew 101 → 115 cases in
round 95.

## Falsification checklist

- `grep -c 'The token starts with ghr_' corpus/source-snapshots/round-95/S142.txt` → 1.
- `sed -n '72p' <S141 capture>` must print `regex = "ghr_[0-9a-zA-Z]{76}"` (the
  row records the file at commit 59ada1f4; the capture is not committed because
  the file lists published example values).
- `sed -n '429p;446p;463p' corpus/source-snapshots/round-94/S140.txt` must print
  the three `glcbt-`/`glsat-`/`gliamat-` rules.
- `python3 -B corpus/instruments/capture-secret-scan.py --selftest` prints
  `SELFTEST-RESULT pass cases=115`; the 14 new cases cover both families'
  positive, boundary and placeholder negatives.
- `python3 -B .ufo/waves/round-95/c2/capability-check.py --lane . --rev master
  --work <scratch> --instrument-sha256 <sha> --gate-sha256 <sha>` prints K1–K6 ok.

## Rejected claims

- **"The S142 page states the refresh token's length."** It does not: line 169
  states only the prefix. The length comes from S141's rule file; an entry that
  attributes 76 to the GitHub page would be false about its own source.
- **"`ghr_` is a 36-character shape like the other GitHub prefixes."** The
  classic family is 36; the refresh family is 76. Treating 76 as 36 would miss
  every real refresh token because the right boundary fails at character 37.
- **"The JWT family is one flat prefix rule."** The three-segment grammar with
  its 10/10/20 floors is what separates a token from a placeholder; a flat
  `glcbt-` prefix rule false-greens documentation prose.
