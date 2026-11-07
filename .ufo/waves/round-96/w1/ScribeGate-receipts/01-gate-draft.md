## Gate

Candidates considered this round:

1. **S144 — GitLab Docs, Security — Tokens** — ADMIT (`docs`, tier A, `mined`).
   URL `https://docs.gitlab.com/security/tokens/`; opened 2026-11-07 (HTTP 200,
   67,805 bytes fetched; committed capture
   `corpus/source-snapshots/round-96/S144.txt`, 17,591 bytes, 418 lines
   (`wc -l`; the round-96 manifest's `"lines": 419` is one high), sha256
   `d6e529275deb3ecf4ea2c3edaff2caa882760680cf23c1a134424e6acffdb83d`). Quote
   (20 words, `corpus/source-snapshots/round-96/S144.txt:346-347`): "With the
   exception of Personal Access tokens, these prefixes cannot be configured, as
   they are designed to be standard identifications." The "Token prefixes" table
   follows at `:348-395` and lists `glpat-`, `gloas-`, `gldt-`,
   `glrt-`/`glrtr-`, `glcbt-`, `glptt-`, `glft-`, `glimt-`, `glagent-`, `glwt-`,
   `glsoat-` and `glffct-`. The page states prefixes and no length or tail; the
   row's `teaches` cell says so, and the lengths and tails stay with S140.
2. **S145 — GitLab Docs, REST API authentication** — REJECT (`docs`, tier B,
   `rejected`). URL `https://docs.gitlab.com/api/rest/authentication/`; opened
   2026-11-07 (HTTP 200, 53,671 bytes; the fetch is a seat scratch file and is
   not committed, because a rejected row carries no capture). The
   authentication-methods and token sections were searched for `glpat`,
   `glptt`, `glrt`, `gldt`, `glagent` and `glwt`: 0 hits. The page writes a bare
   placeholder where a token would go (`Authorization: Bearer OAUTH-TOKEN`,
   scratch capture line 172), so it states no character set, length or tail and
   cannot ground a shape. Flip: the page gains a prefix or length table, or a
   section that states a token's character set.
3. **S140 — GitLab rules `rules/mit/gitlab/gitlab.toml` at commit 59ada1f4** —
   re-opened for the seven rules this round implements, no status change
   (`mined`). The rules are at capture lines 30, 51, 73, 136, 324, 358 and 375
   of `corpus/source-snapshots/round-94/S140.txt`; the capture redacts example
   values and preserves line numbering, so the line cites are stable.

Status / used-by changes this round, old → new:

- S144: (new row) → `mined`; used-by `—` → `corpus/instruments/capture-secret-scan.py, corpus/knowledge/gitlab-routable-and-versioned-token-forms.md`.
- S145: (new row) → `rejected`; used-by `—` (unchanged).
- S140: status `mined` (unchanged); used-by unchanged (`corpus/instruments/capture-secret-scan.py`).

Registry 143 → 145 rows: `git show d8a2bb0:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`
prints 143, and the same grep on the working tree prints 145. Census (the
script lives at the fleet root, not in the lane, so the command is run from
there):
`cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
prints `kasegi ok` rc 0 with the seven inherited W04 duplicate-URL warnings
(S028, S029, S072, S076, S080, S085, S143).

Spot-check result: pending the round-96 non-author closure.
