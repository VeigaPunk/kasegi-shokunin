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

## Wave findings (13-seat v1 wave, round-95 w1)

Verdicts, all re-derived by non-author seats from the frozen revs:

- **C1** — CriticClaimsC1: STANDS (M0 1007/1998, M1 1008/1994, M3–M6, M9 16/16, M10
  excluded=0, `after_rev=53ec479d`); ExecC1Indep: AGREE (independent implementation,
  exact changed-line set 14 lines/16 rows, meter reproduced, delta −4 tokens/+1
  resolved, pins equal); ReviewC1Sites: **14/16 CORRECT, 2 PARTIAL, 0 WRONG** —
  `triage-thresholds.md:88` (first part) and `:90` cite `SKILL.md:182-184` for a
  predicate completed on line 185; exact round-96 labels written
  (`ReviewC1Sites-receipts/round96-labels.tsv`).
- **C2** — CriticClaimsC2: STANDS at seeds 77031/913457/20261107; SentinelShapes:
  STANDS, 0 MUST-FIX; ExecC2Probe: PASS (independent fixtures); ReviewC2Scanner:
  claim STANDS, **REQUEST-CHANGES** on one routed defect.
- **Harm** — CriticHarm: NO HARM on SKILL.md identity, untouched citations, shape
  coverage and allowlist scope; three routed defects, none re-scoring.
- **Gate gaps** — MutC2Counter: 8/9 forgeries killed, `F6-fixture-literals`
  survives when the digest pin is not supplied; MutC1Counter: see its report.
- **Sources** — ScoutSources: AGREE on all three anchors, every live re-fetch
  byte-identical; six routed items, the sharpest being that C2's frozen statement
  names S141 while the landed citation is S143 (the correction row).
- **Scope** — ConnectorOverlap: no sibling lane implements either shape family, the
  `part`-edit counter or a markdown citation meter; `considerthese/` holds no
  unimplemented proposal touching either claim.

Routed to round 96 (no claim re-scored):

1. `corpus/instruments/capture-secret-scan.py` "Known limits" still lists the three
   GitLab JWT forms as undetected and the "Shapes." block documents neither new
   shape (ReviewC2Scanner finding 1; SentinelShapes R1; CriticHarm D1; ScribeGate).
   Not fixed here because the landed instrument's sha256 is C2's frozen pin.
2. One bare `S041.txt:1680-1681` citation survives at
   `iso-29147-divergence-and-clause-crosswalk.md:13` (CriticHarm D2; ReviewC1Sites).
3. The two C1 PARTIALs above (round-96 labels exist).
4. `MutC2Counter` survivor F6 (fixture-literal forger) when `--instrument-sha256` is
   absent: the gate authenticates bytes, not correctness.
5. `citation-survival.tsv` census drift (CriticHarm D3) — stale at base too; the
   freshness gate is not run by a lane round.
6. ScoutSources R1–R6: S142 has no manifest/digest row, S141→S143 re-tier needs the
   GitHub REST docs capture unblocked (intake refuses it for the new shape), the
   S140 "line numbering preserved" wording needs a qualifier.
