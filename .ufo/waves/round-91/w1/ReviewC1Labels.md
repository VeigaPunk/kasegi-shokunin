# ReviewC1Labels — round 91, attempt 1: non-author labels for the round-92 C1 tranche

Seat: ReviewC1Labels (leaf, review/attack). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Measured rev `8a1a00c639ba808a701d1f186aac9ebd0045deaa` (C1 landing). No lane file was edited; every
label is a routed proposal in the wave dir.

## 0. Deliverables

- `ReviewC1Labels-receipts/round92-labels.tsv` — 30 rows, header `line	key	label	fix	evidence`
  (5 columns, tab-separated, no tabs in fields).
- `ReviewC1Labels-receipts/gone-list.txt`, `list-gone-keys.py` — the GONE-token census and the script
  that produces it.
- `ReviewC1Labels-receipts/verify-labels.txt`, `verify-labels.py` — mechanical verification (PASS).
- `ReviewC1Labels-receipts/projected-reading.txt` — a fixture projection of a tranche built from these
  labels: 891/1880 -> 905/1877 (token-level edits; see §5).

## 1. Method and commands

The meter's measure mode over the frozen scope (`corpus/knowledge/*.md`) at the landing:

```
python3 -B .ufo/waves/round-91/c1/knowledge-meter.py --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --measure-rev 8a1a00c639ba808a701d1f186aac9ebd0045deaa --work $S
```

printed `KNOWLEDGE-METER rev=8a1a00c… rate=891/1880 pct=47.39 mirror_absent=True pinned=archive`
(`HOST rev abs_tokens=127 abs_nongone=23`). That equals the C1 frozen after-target, so the labels below
are applied to the post-C1 corpus.

The GONE population was produced the way the meter does — `git archive 8a1a00c…` into `$S`, import
`corpus/instruments/resolve.py` from that extract, walk `corpus/knowledge/*.md` with the resolver's own
`TOKEN`/`is_pathlike` rules, and `classify(tok, tree, mirror)[0] == "GONE"`:

```
python3 -B $S/list-gone-keys.py $S
```

filtered to bare keys matching `^<name>.md(:N[-M])?$` whose target file exists as
`corpus/knowledge/<name>.md` at the landing. Result: **20 distinct keys, 30 citing sites** (all of
`corpus/knowledge`; the mirror is absent, so relative tokens classify GONE). 4 sites are outside
`triage-thresholds.md` (`citation-bases.md:14` x2, `japanese-domestic-disclosure-workflow.md:7`,
`root-loss-2026-10-12.md:68`); the other 26 are in `triage-thresholds.md`. All 30 were labelled.

Label vocabulary used (per the seat spec):
- `CORRECT` — the bare key's own range already states the row's rule; the round-92 edit is a pure path
  qualification to `corpus/knowledge/<key>` (same `N-M`). Three such rows are mentions that must NOT be
  qualified (`No edit` in the fix column).
- `corpus/knowledge/<name>.md:N-M` — the key's range is wrong/absent and this range states the row's
  rule; the edit is `key` -> `N-M`.
- `content-repair` — the row's premise is stale, or support is split across non-contiguous ranges, or
  no range states it. Fix starts `Replace with — (` (drop the tie) or `Replace with <name>.md:N-M (`
  (repoint/reword). 4 dash, 6 named.

Verification (`verify-labels.py`): every `line` exists at the landing; every key occurs exactly once,
backticked, on its citing line; every named target file is `corpus/knowledge/<key-basename>` and its
anchor lies inside the entry; the labelled site set equals the independently re-derived GONE site set
(30/30); the only tracked non-`.ufo/` file with each target basename is `corpus/knowledge/<name>.md`
(meter M4's uniqueness premise). Output: `LABELS rows=30 distinct_sites=30 gone_sites=30
map_eligible=26` / `VERIFY PASS`.

## 2. Counts per label kind (30 sites)

| label kind | sites | names |
|---|---|---|
| `CORRECT` (pure qualification, incl. 3 mentions) | 10 | 177, cb14(claim-gates.md:3), jp7, 59, 90, 456, 458, 390, cb14(ops-invariants.md:18), root68 |
| canonical range (range change) | 10 | 445, 280, 281, 367, 86, 87, 146, 153, 154, 149 |
| `content-repair` | 10 | 249, 369, 370, 437, 58, 144, 155, 438, 152, 150 (named 6, dash 4) |

Per-key summary (all paths `corpus/knowledge/`):

| key | site(s) | label |
|---|---|---|
| `claim-gates.md:21-23` | 177 | CORRECT (partial: artifact-level confinement; package-root single `realpathSync(dir)` not restated) |
| `claim-gates.md:3` | citation-bases:14 | CORRECT, **no edit** (bare form is the counter-example the paragraph forbids) |
| `claim-gates.md:42-47` | 249 | content-repair -> `claim-gates.md:52-56` (stale "new / regex only" premise) |
| `claim-gates.md:5-6` | 445 | -> `claim-gates.md:57-61` |
| `claim-gates.md:71-74` | 280, 281 | -> `claim-gates.md:88-91` |
| `ev-model.md:15-16` | 367 | -> `ev-model.md:22-23` |
| `ev-model.md:22-23` | 369, 370 | content-repair `—` x2 (deadline / duration_p90 types not stated) |
| `intake-surface.md:71` | 86, 87 | -> `intake-surface.md:83-88` (partial: predicate/defaults not restated) |
| `intake-surface.md:75-76` | 437 | content-repair -> `intake-surface.md:89-90` (gloss "reward.min present on 48" is the conflation) |
| `japanese-domestic-disclosure-workflow.md` | jp7 | CORRECT, **no edit** (names the shokuknow staged entry, not a corpus citation) |
| `mission-control.md:13-46` | 458 | CORRECT |
| `mission-control.md:19-21` | 456 | CORRECT |
| `mission-control.md:20-21` | 58, 59, 90, 144 | 58/144 content-repair `—` (no `attempt(s)`/`MAX_ATTEMPTS` text in the entry); 59 CORRECT partial (filter bullet); 90 CORRECT (`freshness.live +1`) |
| `mission-control.md:36-38` | 146, 153, 154 | -> `:54-56` / `:54-55` (partial: window stated, UTC−3 formula not) / `:54-56` |
| `mission-control.md:37-38` | 155, 438 | content-repair -> `:56-57` x2 (stale SUPERSEDES / stale `openai-oauth/` gloss) |
| `mission-control.md:40-45` | 152 | content-repair -> `:61` (15-min window stated; 20000-char tail not) |
| `mission-control.md:42-46` | 149 | -> `:68-71` (partial: 30 s tick is L17) |
| `mission-control.md:43-46` | 150 | content-repair -> `:68-71` (entry lists 8 allowlist groups, not the row's 11) |
| `ops-invariants.md:18` | citation-bases:14, 390 | CORRECT no-edit (mention) / CORRECT (`BANNED` row) |
| `ufo-archive-2026.md:31` | root-loss:68 | CORRECT |

## 3. Routed defects (attack findings; qualifiers, never a re-score)

**F1 (medium) — stale SUPERSEDES / stale gloss survives at `triage-thresholds.md:155` and `:438`.**
Both cite `mission-control.md:37-38` (the sweep bullet). The entry at `:56-57` already writes
`openai-codex/gpt-6-astra:max` with "round-13 correction: … earlier text said `openai-oauth/`". So the
`:155` SUPERSEDES premise ("that entry writes `openai-oauth/`") and the `:438` gloss are false at the
landing. Same class as round-90 Finding 1; the r91 C1 tranche touched six other sites, so this class
remains unlabelled-in-lane. Re-runnable: `git show 8a1a00c:corpus/knowledge/mission-control.md | sed -n
'54,58p'` and `git show 8a1a00c:corpus/knowledge/triage-thresholds.md | sed -n '155p;438p'`.

**F2 (medium) — four MATCHES ties have no supporting text in the cited entry.** `:369` (`deadline`
date-time) and `:370` (`duration_p90`/`submission_buffer` number) cite `ev-model.md:22-23`, which pins
only `p_*` to [0,1] plus `as_of`/`sources`; `:58` and `:144` cite `mission-control.md:20-21`, and the
string `attempt` does not occur in that entry at all (grep returns nothing). `:58`/`:144` are multi-tie
cells, so the dash applies to the single token, keeping `SKILL.md:117`.

**F3 (medium) — nine wrong anchors, all with a correct range elsewhere.** `intake-surface.md:71`
(coverage/name drift) at `:86`, `:87`; `intake-surface.md:75-76` (name drift) at `:437`;
`claim-gates.md:71-74` (reviewer/hard-gate text) at `:280`, `:281`; `claim-gates.md:5-6` (the "OK only
when zero errors" line) at `:445`; `claim-gates.md:42-47` (secrets gate) at `:249`;
`ev-model.md:15-16` (formula block) at `:367`; `mission-control.md:36-38`/`:37-38` (sweep bullet) at
`:146`, `:153`, `:154`, `:155`, `:438`; `mission-control.md:40-45`/`:42-46`/`:43-46` (budget/P20-P21/
commit/finalize text) at `:152`, `:149`, `:150`. Each row's fix names the range that does state it.

**F4 (low) — three mentions must not be repointed.** `citation-bases.md:14` quotes `claim-gates.md:3`
and `ops-invariants.md:18` as the bare forms its own L13-16 forbids; `japanese-domestic-disclosure-
workflow.md:7` names the `~/Projects/shokuknow/merge/kasegi/` staged package entry (external, read-only),
not a line in this corpus. Qualifying these would break the doc/example; the TSV fixes say "No edit".

## 4. Implementation notes for the round-92 meter/map builder

1. `CORRECT` rows name a pure qualification `old "`key`" -> new "`corpus/knowledge/<key>`"`; the round-91
   meter's `expected_edit` returns `None` for a non-range, non-content-repair label, so a successor meter
   must either express this edit form or exclude CORRECT rows from the map/label set equality (M9/M10).
2. Rows `:58` and `:144` are multi-tie cells (`MATCHES: `SKILL.md:117`, `mission-control.md:20-21``).
   The round-91 `FIXDASH` pattern (`MATCHES: `key`` -> `—`) does not match them; the round-92 removal
   must drop just the named token and keep the sibling tie (and tidy the trailing separator).
3. Rows `:369`/`:370` are sole-tie cells; the whole cell becomes `—`, the FIXDASH form.
4. `mission-control.md:20-21` has four sites with three treatments (2 qualify, 2 drop) because four
   different rows make different claims; edits are per-site, so this is not a conflict, but the map must
   be built per `citing-file:line`, not per key.

## 5. Projection (informational, not a claim)

Applying these labels token-level to a scratch fixture of the landing tree (three `No edit` mentions
skipped, dashes tidied for the sole-tie rows) gives `891/1880 -> 905/1877` (`pct 47.39 -> 48.22`). The
delta is +14 numerator, -3 denominator: repaired keys that are cited at several sites collapse into
fewer distinct tokens, and the two `ev-model.md:22-23` dash rows remove that token. This is a projection
of *these labels*, not of the frozen C1 claim (which is judged only at `8a1a00c`).

## 6. Bounds observed

Scratch root `/fast/scratch/hyaku/kasegi-r91/ReviewC1Labels` (all `git archive` extracts, fixture repos
with asserted `rev-parse --show-toplevel`, and the projection lived there); it is deleted on exit.
Lane reads only (`git show`/`git archive`/`git ls-tree`/`git log`); no lane file, instrument, frozen
control or sibling lane was touched. No credential-shaped value was written to the wave dir; receipts
carry only sha-free text, line texts that contain none, and scanner-clean label prose. No tool was
installed.
