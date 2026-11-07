author: kasegi (round 95, attempt 1)

# Round 95 — lesson

Lane: kasegi. Round 95, attempt 1. Base `9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10`;
freeze `347519f21524d2bc13eb6c91cf3550930a4265b3`; C1 landing
`53ec479d71d25cf5be052db794a548a5904564b8`; C2 landing
`38e7319f44a9fab2978b59ffd43faf207cf62b32`.

## Gate

Candidates considered this round:

1. **S142 — GitHub Docs, Refreshing user access tokens** — ADMIT (`docs`, tier A,
   `mined`). Opened 2026-11-07. Quote (5 words,
   `corpus/source-snapshots/round-95/S142.txt:169`): "The token starts with
   `ghr_`". The page grounds the prefix and nothing else; it states no length,
   and the entry says so.
2. **S143 — GitLab `rules/mit/github/github.toml` at commit 59ada1f4 (a
   correction row superseding S141)** — ADMIT (`code`, tier B, `mined`). Opened
   2026-11-07. Quote (line 72, committed at
   `.ufo/waves/round-94/w1/ScoutGitLabRules-receipts/08-github-rules-file.txt:16`):
   `regex = "ghr_[0-9a-zA-Z]{76}"`. Tier B because the file is GitLab's copy of
   GitHub's shapes; it is the only non-superseded row that states the
   76-character length, so the entry carries it as tier B and names the tier.
3. **S141 — the same file as a cited row** — REJECT (kept `rejected`). Its
   `teaches` cell is already the rejection record and CORPUS rule 2 does not
   allow rewriting it; the length is carried by the S143 correction row instead.
   Flip: none needed — the supersession is the fix.
4. **S140 re-open (GitLab `gitlab.toml`)** — ADMIT as the already-mined row it
   is; re-opened this round for the three JWT rules
   (`corpus/source-snapshots/round-94/S140.txt:429`,
   `corpus/source-snapshots/round-94/S140.txt:446`,
   `corpus/source-snapshots/round-94/S140.txt:463` keywords;
   `corpus/source-snapshots/round-94/S140.txt:430`,
   `corpus/source-snapshots/round-94/S140.txt:447`,
   `corpus/source-snapshots/round-94/S140.txt:464` regexes). No status change.

Status / used-by changes this round, old → new:

- S142: (new row) → `mined`; used-by `—` → `corpus/instruments/capture-secret-scan.py, corpus/knowledge/github-refresh-tokens-and-gitlab-jwt-tokens.md`.
- S143: (new correction row) → `mined`; used-by `—` → the same two paths.
- S141: status unchanged (`rejected`), used-by unchanged (`—`), superseded by S143.
- S140: status unchanged (`mined`), used-by unchanged (`corpus/instruments/capture-secret-scan.py`).

Registry 141 → 143 rows: `git show 9ef0126:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`
prints 141, and the working tree prints 143 by the same command. Census:
`bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
prints `kasegi ok` rc 0 with the six inherited W04 duplicate-URL warnings plus
the S143 supersession duplicate (S141/S143 share the URL by design).

Spot-check result: pending the round-95 non-author closure.

## Mistakes

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M95-1 | reproducibility | round-94 `.ufo/waves/round-94/controls/c1-controls-r94.py` ~line 145 `git clone -q --shared LANE`; `.ufo/waves/round-94/w1/CriticClaimsC1-receipts/controls-rerun-landing.txt:60,117` print `CONTROL m5-cell-repair-before-r93 rc=1 want=0 FAIL` and `C1-CONTROLS-RESULT fail controls=12`; `controls-pinned-lane-r94.txt:60,117` print `rc=0 want=0 PASS` and `pass controls=12` | CriticClaimsC1's P4 reproduction limb (the wave critic re-ran the frozen controls after the landing); no freeze-time rule required the fixture's source revision to be immutable | every round-95 fixture clones the pinned base; `.ufo/waves/round-95/l1/c1-controls-postlanding-r95.txt` prints `C1-CONTROLS-RESULT pass controls=15` |
| M95-2 | frozen-control | `corpus/lessons/round-94-verifier-spotcheck.md` §2 C2: the frozen P4 names `s140-allow-rows-removed`; the receipt's tenth control is `tampered-instrument` | CriticClaimsC2 and ReviewC2Scanner (two independent seats) | the round-95 `claims.json` control field is a verbatim copy of the receipt's `CONTROL` lines, and all 15 controls were re-run after the landing |
| M95-3 | key-collision | the first round-95 label set wrote two `cell-repair` rows on line 88; `.ufo/waves/round-95/controls/c1-controls-r95.txt:139-149` prints `CONTROL two-cells-one-line rc=1 want=1 PASS limb=True` and its M3 line prints `bad_lines=1 old_not_once=0 dup_rows=1` | the counter's own M3 composition check | the successor counter's `part` kind allows two disjoint substring edits per cell; the `two-cells-one-line` control keeps the failure reproducible |

## Wave findings

Pending the round-95 w1 wave closure and the non-author spot-check.
