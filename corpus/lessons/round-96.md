author: kasegi (round 96, attempt 1)

# Round 96 — lesson

Lane: kasegi. Round 96, attempt 1. Base `d8a2bb0a2bdc2f6337ea2f849a1a557297067ad6`;
freeze `804e7bc344df0808c880815dde077c28be5db18a`; C1 landing
`3c0581e2616df7a10af494a785b479d5e5293749`; C2 landing
`7ef1d365eb523a83b2567342a6c0f585ab028ab0`.

## Gate

Candidates considered this round:

1. **S144 — GitLab Docs, Security — Tokens** — ADMIT (`docs`, tier A, `mined`).
   Opened 2026-11-07, HTTP 200, 67,805 bytes fetched, 17,591 bytes / 418 lines
   committed as `corpus/source-snapshots/round-96/S144.txt` (sha256
   `d6e529275deb3ecf4ea2c3edaff2caa882760680cf23c1a134424e6acffdb83d`).
   URL: `https://docs.gitlab.com/security/tokens/`. Quote (20 words, capture
   lines 346-347): "With the exception of Personal Access tokens, these
   prefixes cannot be configured, as they are designed to be standard
   identifications." The "Token prefixes" table follows at lines 348-395 and
   lists `glpat-`, `gloas-`, `gldt-`, `glrt-`/`glrtr-`, `glcbt-`, `glptt-`,
   `glft-`, `glimt-`, `glagent-`, `glwt-`, `glsoat-`, `glffct-`. The page
   states prefixes, never lengths or tails, and the row says so.
2. **S145 — GitLab Docs, REST API authentication** — REJECT (kept `rejected`,
   tier B). Opened 2026-11-07, HTTP 200, 53,671 bytes. URL:
   `https://docs.gitlab.com/api/rest/authentication/`. The authentication-methods
   and token sections were read and searched for `glpat`, `glptt`, `glrt`,
   `gldt`, `glagent`, `glwt`: 0 hits. Reason: it names authentication methods
   but states no token prefix, length or tail, so it cannot ground a shape.
   Flip: the page adds a prefix or length table, or a section that states a
   token's character set.
3. **S140 — GitLab rules `rules/mit/gitlab/gitlab.toml` at commit 59ada1f4** —
   re-opened from its committed capture for the seven rules this round
   implements (lines 30, 51, 73, 136, 324, 358, 375). The L1's own `/-/raw/`
   fetch answered HTTP 403 (a Cloudflare challenge page, receipt
   `.ufo/waves/round-96/l1/s140-live-fetch-r96.txt`); the wave's ScoutSources
   re-fetched the same pinned URL and got HTTP 200, 20,228 bytes, sha256
   `14854f71f81f2400ac33a950cd70850cbdc80c319e4bdb0445bff6dbc36a11b5`, equal to
   the round-94 manifest's raw digest
   (`.ufo/waves/round-96/w1/ScoutSources-receipts/R1-s140-live.txt`), so the
   source is live-verified this round and the capture's line numbers are the
   citation base. The row's status (`mined`), recheck and used-by are unchanged.

Status / used-by changes this round, old → new:

- S144: (new row) → `mined`; used-by `—` → `corpus/instruments/capture-secret-scan.py, corpus/knowledge/gitlab-routable-and-versioned-token-forms.md`.
- S145: (new row) → `rejected`; used-by `—` (unchanged).
- S140: status `mined` (unchanged), used-by unchanged (`corpus/instruments/capture-secret-scan.py`).

Registry 143 → 145 rows: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`
prints 143 at the base and 145 in the working tree. Census:
`cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`
prints `kasegi ok` rc 0 with the seven inherited W04 duplicate-URL warnings
(S028, S029, S072, S076, S080, S085, S143).

Spot-check result: pending the round-96 non-author closure.

## Mistakes

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M96-1 | harness-crash | the first control run died with `TypeError: 'NoneType' object is not iterable` at `record()` (`declared=None` for the rc-2 control); no receipt was written | none — the harness's own error path was never exercised before the fixture set was trusted | `.ufo/waves/round-96/controls/c1-controls-r96.py` defaults `declared` to `[]` and skips the attribution check; the receipt is written on every path. The first run after the fix printed `C1-CONTROLS-RESULT pass controls=12` |
| M96-2 | fixture-shape | the `snapshot-missing-only` fixture put the kind word `range` in the label column and the path in the fix column; the counter read `kinds=...unknown=1` and the fixture failed M9/M10 as well as M4/M5 | the harness's attribution check (declared `M4,M5`, observed `M4,M5,M9,M10`) | a range label carries the path in BOTH the label and fix columns, as the round-95 label set does; re-run prints `CONTROL snapshot-missing-only rc=1 want=1 PASS limbs=M4,M5` |
| M96-3 | fixture-shape | the first `unlabelled-only` fixture appended a second map row on the same (site, key) as row 1, so M3 reported `dup_rows=1` and the fixture failed M3 as well as M9/M10 | the harness's attribution check (declared `M9,M10`, observed `M3,M9`) | a fixture that must isolate M10 uses a site no other row names (line 89, a no-op row); re-run prints `CONTROL unlabelled-only rc=1 want=1 PASS limbs=M10,M9` |
| M96-4 | fixture-shape | the first C2 plant table named `p6.txt` while the plant map wrote `p6.html`; K3 printed `missing=[('…-p6.txt', 'gitlab-workspace-token-versioned')] extra=[('…-p6.html', …)]` | K3's exact-set comparison | the plant spec and the file map are one table in `.ufo/waves/round-96/c2/capability-check.py`; the re-run prints `K3 ok hits=7 missing=none extra=none` |
| M96-5 | successor-constant | the first round-96 counter run read 16 labels (`M10 labelled=16`) and failed M9/M10: the copied counter still carried `LABELS_PATH = ".ufo/waves/round-95/c1/labels.tsv"` | the counter's own M10 label count | a successor counter's path constants are part of its identity; the first run must print a label count equal to the frozen label set (5). The landed counter reads `.ufo/waves/round-96/c1/labels.tsv` and prints `labelled=5` |
| M96-6 | measurement-base | the round-95 report's meter reading (1008/1994) is not the round-96 base: the knowledge scope grew by the round-95 entry, so the base reads 1030/2027 | the round-96 first measurement (`KNOWLEDGE-METER rev=d8a2bb0a rate=1030/2027`) | every round re-measures its own base at its own base revision; the claim's `--base-target` is that reading, never the previous round's |
| M96-7 | fixture-shape | the `row-old-absent-only` fixture picked the pointer `(L1819)`, which DOES occur on `iso-29147-divergence-and-clause-crosswalk.md:36`; the fixture therefore fails M3 via `bad_lines`, not via `old_not_once`, and the round-95 mutant `s01_old_absent_accepted` survives | MutC1Counter's rebuilt-mutant campaign (6 killed, 4 survived; `s01` survived with `no control verdict differs from baseline`) | an absent-old fixture must name a pointer that does not occur on its line (a synthetic `(L9999)` with a valid range is enough); routed to round 97 with the `s05` and `m06` gaps |

## Wave findings (13-seat v1 wave, round-96 w1)

All 13 seats settled, 0 dead. C1 STANDS on P1–P4 (CriticClaimsC1; ExecC1Indep AGREE with an
independent census reproducing 1030/2027 → 1032/2028 and a byte-identical map application;
ReviewC1Sites 5/5 CORRECT with an empty round-97 label set). C2 STANDS (CriticClaimsC2 at three
seeds; ExecC2Probe 21 positives exact and 21 boundary negatives clean; ReviewC2Scanner APPROVE;
SentinelShapes 0 MUST-FIX, 7 routed). NO HARM on all four CriticHarm checks. MutC1Counter: 6 of
the 10 round-95 survivors killed, 4 survive (m06, s01, s03 equivalent, s05) — the two
attribution-only kills (s06, s09) are the attribution limb working. MutC2Counter: 8 of 14
scanner mutants killed, 6 survive. ScoutSources live-verified S140 (HTTP 200, digest equal to
the round-94 manifest), confirmed S144 is the page this round already holds, and proposed one
reject. ScribeGate drafted the Gate/Mistakes/entry and routed F1–F7; F1–F4 were repaired in
`6299582b`, F5/F6 answered by committed receipts. ConnectorOverlap: no sibling overlap, no
`considerthese/` proposal touching either claim. Routed to round 97: the m06/s01/s05 fixture
gaps, the four surviving scanner mutants, SentinelShapes R1/R2, ReviewC2Scanner F1–F4, the
scratch-rev receipt header, and the missing machine receipt for the pre-freeze repairs.
