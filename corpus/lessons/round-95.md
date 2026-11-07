# Round 95 — lesson

Lane: kasegi. Round 95, attempt 1. Base `9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10`;
freeze `347519f21524d2bc13eb6c91cf3550930a4265b3`; C1 landing
`53ec479d71d25cf5be052db794a548a5904564b8`; C2 landing
`38e7319f44a9fab2978b59ffd43faf207cf62b32`.

## Gate

Candidates considered this round:

1. **S142 — GitHub Docs, Refreshing user access tokens** — ADMIT (`docs`, tier A,
   `mined`). Opened 2026-11-07. Quote (5 words, capture line 169): "The token
   starts with `ghr_`". The page grounds the prefix and nothing else; it states
   no length, and the entry says so.
2. **S143 — GitLab `rules/mit/github/github.toml` at commit 59ada1f4 (a
   correction row superseding S141)** — ADMIT (`code`, tier B, `mined`). Opened
   2026-11-07. Quote (line 72): `regex = "ghr_[0-9a-zA-Z]{76}"`. Tier B because
   the file is GitLab's copy of GitHub's shapes; it is the only opened source
   that states the 76-character length, so the entry carries it as tier B and
   names the tier.
3. **S141 — the same file as a cited row** — REJECT (kept `rejected`). Its
   `teaches` cell is already the rejection record and CORPUS rule 2 does not
   allow rewriting it; the length is carried by the S143 correction row instead.
   Flip: none needed — the supersession is the fix.
4. **S140 re-open (GitLab `gitlab.toml`)** — ADMIT as the already-mined row it
   is; re-opened this round for the three JWT rules (lines 429, 446, 463). No
   status change.

Status / used-by changes this round, old → new:

- S142: (new row) → `mined`; used-by `—` → `corpus/instruments/capture-secret-scan.py, corpus/knowledge/github-refresh-tokens-and-gitlab-jwt-tokens.md`.
- S143: (new correction row) → `mined`; used-by `—` → the same two paths.
- S141: status unchanged (`rejected`), used-by unchanged (`—`), superseded by S143.
- S140: status unchanged (`mined`), used-by unchanged.

Registry 141 → 143 rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`);
`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
prints `kasegi ok` rc 0 with the six inherited W04 duplicate-URL warnings plus the
S143 supersession duplicate (S141/S143 share the URL by design).

Spot-check result: pending the round-95 non-author closure.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| A frozen predicate named a control that the round's own redaction had made impossible (round-94 P4, mined here) | `corpus/lessons/round-94-verifier-spotcheck.md` §2 C2: the frozen P4 names `s140-allow-rows-removed`, the receipt's tenth control is `tampered-instrument` | none — the freeze-time control list was hand-copied into `claims.json` and never re-derived from the executed receipt | the round-95 `claims.json` control field is a verbatim copy of the receipt's `CONTROL` lines, and C1's reproduction limb is re-run after the landing |
| A control fixture cloned the mutable live lane, so its reception flipped after the landing (round-94 defect 1) | round-94 `c1-controls-r94.py` ~line 145 `git clone -q --shared LANE`; the r94 spot-check's `controls-rerun-landing.txt` prints 11/12 | the control harness had no pinned base; no rule required the fixture's source to be immutable | every round-95 fixture clones the pinned base commit; the post-landing re-run is committed (`.ufo/waves/round-95/l1/c1-controls-postlanding-r95.txt`) and prints 15/15 |
| A cell with two citation keys cannot be mapped by two whole-cell replacements (same line, same old string) | the first round-95 label set wrote two `cell-repair` rows on line 88; the counter's M3 reported `old_not_once` | the counter's own composition check (M3) caught it before any landing | the successor counter gained a `part` kind: two disjoint substring edits per cell, each carrying its own key; the `two-cells-one-line` control keeps the failure reproducible |
