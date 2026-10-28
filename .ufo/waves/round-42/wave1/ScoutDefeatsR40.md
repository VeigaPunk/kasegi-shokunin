# ScoutDefeatsR40 — round-42 wave-1 receipt (defeat catalog, round-40 + round-39 wave-2)

Seat: `ScoutDefeatsR40` (scout, leaf — no subagents). Item: catalog every defeat committed in
`.ufo/waves/round-40/wave2/` (RevC1Counters.defeats.txt T2–T14, CritKillRule.md F1–F8,
CritKillRule.h6-escapes.sh, MutH6H10.md D2, MutH1H5.md) and `.ufo/waves/round-39/wave2/`
(CritG2Exploit.md, CritC1Kill.md); for each record defeat status, mutation class, and which
r41 (I1–I12) or r42 (J1–J13 / F-*) check should already reject it; flag UNMAPPED.
Axes: **depth:verifiability** (primary — this catalog is the replay source for the r42 J1–J7
REPLAY limbs), **coverage** (UNMAPPED items are candidate routed defects).

## Deliverable

`.ufo/waves/round-42/wave1/ScoutDefeatsR40.txt` — **94 lines**, sha256
`4436b50d3b245f5e88d63ee1703aa7a20628ce0c7f31c05af5d5c2a5bcf2e7dd`.
Catalog format: `ID | src file:lines | attacked limb | status | mutation class | r41 check | r42 check/family | mapping`.

## What was read (all evidence paths)

- `.ufo/waves/round-42/claims.json` (frozen C1/C2 predicates, kill rules, counting commands — full text)
- `round-40/wave2/`: `RevC1Counters.defeats.txt` (whole file), `RevC1Counters.md` (verdict/defect
  tables), `CritKillRule.md` (whole), `CritKillRule.h6-escapes.sh` (whole, incl. elided limb+matrix),
  `CritKillRule.pending-variants.md`, `MutH6H10.md` (whole), `MutH6H10.h7-reorder-receipt.txt`,
  `MutH1H5.md` (whole), `MutH1H5.h4-nodate.txt`
- `round-39/wave2/`: `CritG2Exploit.md` (whole), `CritC1Kill.md` (whole, 478 lines)
- `corpus/instruments/r41-closure.sh` — header I1–I12 semantics, `check_i3/i4/i5/i11`, `fence_awk`
  (CommonMark ≥3-run grammar), `pending_scan` (broad spelling class), `worktree_state`
  (ls-files -v + --untracked=all + --ignored), `i11_probe_f1..f8` bodies, `declared_blocks_check`
  (canon clause = the T7 fix), `EVIDENCE=(RevC1Counters CritKillRule MutH6H10)`
- `corpus/instruments/r40-closure.sh` header (H1–H10 lineage to r39 findings)
- `corpus/lessons/round-41-verifier-spotcheck.md` §5 (routed queue), LOG.md/SCORECARD.md/SHONEN.md
  line-anchored `Correction (round 41)` counts (8/3/3 — K3 class closed)
- `corpus/instruments/*.py` grep: no committed instrument re-grades Gate located-quote/date/≤25-word
  conjuncts (`source-recheck.py` grades manifest quote pins; `recheck-audit.py` has no quote/date limb;
  `kill-rule-check.py` is a capture-binding fixture driver)
- `corpus/instruments/r42-closure.sh`: does not exist yet at catalog time — r42 mappings are to the
  frozen J1–J13/family text, not committed bytes.

## Result

**32 distinct committed defeats cataloged; 26 cleanly MAPPED, 3 UNMAPPED, 4 PARTIAL** (plus one
selftest SURVIVOR, also unmapped — counted with UNMAPPED below).

### MAPPED (defeat → rejecting check, verified in r41-closure.sh source)

| class | defeats | r41 check | r42 check/family |
|---|---|---|---|
| substring tally values | T2 | I3 token boundary | J2 / F-TOKEN |
| fenced content counted | T3(ctrl), T4 | I3/I4 fence_match | J1 / F-EVID (+J3 rows) |
| out-of-export declared path | T7 | I5/I12 `canon` clause | J4 / F-DECL |
| receipt tree tamper | T8 T9 (controls) | I2 byte-equal rebuild | J8 |
| negative-control env forgery | T10 (ctrl), D2 | I10 killable predicate | J9 |
| scratch family scan | T14, F1–F6, h6-escapes m2–m6 | I6 + I11 probes f1–f6 | J5 / F-SCAN |
| mention-only registry row | T13 | I7 row-shape | J3 / F-TABLE |
| receipt grading shape-only | G2 f g h j k, a4/K1 | I2/I8/I9 (transcript+detail+isolation) | J8/J10 |
| receipt ref semantics | G2 e i (ctrl/defect), K1b | I2 ancestor+diff-clean, parent naming | J8 |
| false provenance | K5 | I2 run-utc = committer instant, not-future | J8 + kill_rule |
| section/anchor scoping | K3 | I1 (records authored line-anchored, verified) | J1 |
| pending-marker spellings | F7 | I11 probe_f7 via pending_scan | (see PARTIAL) |
| worktree-clean blindness | F8 | I11 probe_f8 via worktree_state | J13 (see PARTIAL) |
| undeclared appended tail | CritC1Kill e/K2 | I5/I12 declared_blocks_check | J4 / F-DECL |
| selftest window/spec gap | MutH6H10 F1 | seeding-at-J design (I2 contract) | judged_head_rule |
| replay limbs D1 | MutH6H10 D1 (cmp unguarded) | I9 isolation + I2 cmp | J10/J8 — replay `h7-reorder-receipt.txt` |

### UNMAPPED (no committed r41 limb and no named r42 J-check owns the class) — flagged

1. **T5** — H4 URL-colon location-token false positive (`s056=1` green on a quote block with no
   real location; `://…:7` inside the URL matched `:[0-9]+`). Mutation class: location-token
   regex fails to exclude URL spans.
2. **T6** — H4 25-word cap evaded by hyphen-joining (42 real words → 21 tokens). Mutation class:
   word-tokenization alphabet too narrow.
3. **MutH1H5 H4-survivor** — dropping the `date` conjunct is unkillable by the r40 selftest
   (fixture-set gap; probe `h4-nodate.txt` reds pristine rc=1, greens mutant rc=0). Mutation
   class: per-conjunct mutant coverage gap.

Root cause of all three: **the r40 check_h4 Gate-conjunct limb was retired at r41** — no r41 I-check
and no r42 J-check re-grades located-quote/access-date/≤25-word conjuncts, and C2's kill rule only
requires the Gate *text* to carry them. The committed replay artifacts (`h4-nodate.txt`,
`MutH1H5.md` probe transcript) have no committed check to execute against. If r42 keeps C2's Gate
recheck at verifier level only, this whole family is routed-defect material for wave 2.

### PARTIAL (mapped limb exists; named subclass residual open)

- **T11** — lying `--scratch-root`: I6 scans live, but the audited root still leaves no fingerprint
  in the receipt (the "unfalsifiable post-hoc" subclass; r42 J13's "bound to the exported ref by
  name" wording may close it — verify in the r42 suite once landed).
- **F7** — pending-marker spelling class is fixed in r41 (`pending_scan` inside I11), but the r42
  claims carry **no pending-marker clause** (not in J1–J13 text, not in the kill rule). Coverage
  depends entirely on whether the r42 suite inherits the limb.
- **F8** — worktree-clean blindness is fixed in r41 (`worktree_state`: flags+dirty+ignored), and
  r42 J13 ("no uncommitted lane changes") presumably inherits it — verify J13 runs
  `git ls-files -v` + `--untracked-files=all --ignored`, not plain `git status --porcelain`.
- **CritC1Kill f / K6** — duplicate `## Round N` heading hiding a `Final lane commit:` line: r41
  re-anchored everything to line-start `Correction` records; r42 J11 names duplicated *Correction
  blocks* verbatim — a duplicated `## Round N` heading is a different shape, not named.

### Controls confirmed (not defeats)

T1 (honest H2 values), T3 (4-backtick fence errs red), T8/T9 (post-receipt tree tamper reds H7),
T10 (forged-env H8 reds produce + re-run), h6-escapes m1/m7/m8/m9/m10, CritG2Exploit a–e,
CritC1Kill a1–a3, b (undersized tail), c (zero-task dispatch), d (r37 pin tamper).
T12 never existed in the committed artifact (numbering gap, not a missing defeat).

### Note for the J5 replay limb

`CritKillRule.h6-escapes.sh` is a byte-exact verbatim copy of the committed r40 `check_h6` driving
10 scenarios (m2–m6 = F3/F4/F1/F5 states). r42 J5's claims text names "the committed
MutScratchTiming probe" (the r41-era artifact); the r40-era equivalent is this file — either the
J5 replay limb names it directly or it must replay `i11_probe_f1..f6`-equivalent states.
A committed defeat that is not replayed is a kill clause (claims.json).

## Conduct

- Writes: `.ufo/waves/round-42/wave1/ScoutDefeatsR40.txt` (deliverable) and this receipt only.
- Reads: lane files listed above; all `git`/text reads non-mutating; no mutating git/jj anywhere;
  fleet root and `/home/vgpnk/Projects/shokuknow` untouched.
- Scratch: `S=/fast/scratch/hyaku/kasegi-r42/ScoutDefeatsR40/` created and removed at yield; no
  files were ever placed under it (all work was read+catalog; the deliverable/receipt were written
  directly to the wave dir). `ls` of the dir before removal confirms empty.
- Disk guard: green before heavy pass (`/fast/scratch/hyaku` 27%, 592.6G free).
- Tooling: none installed/upgraded; no pacman (paused), no network fetches.
- No lane file outside the wave dir was written; `git status --porcelain` delta = the two wave-1
  artifacts only (untracked).

Report: `.ufo/waves/round-42/wave1/ScoutDefeatsR40.md` (this file).
Deliverable: `.ufo/waves/round-42/wave1/ScoutDefeatsR40.txt` (94 lines, sha256
`4436b50d3b245f5e88d63ee1703aa7a20628ce0c7f31c05af5d5c2a5bcf2e7dd`).
