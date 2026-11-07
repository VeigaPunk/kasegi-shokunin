# ReviewC1Sites — semantic review of the C1 landing (round-92 attempt 1, wave w1)

Scope: the 25 mapped (site, key) pairs of tranche 7 landed at cb1ef2b9856df79c530f3ff1374fa9691ff56233
(base 0628fd247914555838a42c02ba5d4ac08b7e095d, freeze 9e4f0d6830dcc9a30c6f524c48d074ec8979f040),
each row judged whole (main statement plus every gloss), plus the 2 EXCLUDED pairs and the 3 no-edit pairs.
Verdicts: `ReviewC1Sites-receipts/verdicts.tsv` (30 rows).

Method: `git show cb1ef2b:corpus/knowledge/<entry>` for every cited entry, read at the landed line
ranges; support confirmed by grep counts over the landed bytes. No re-scoring of the frozen meter —
the landing receipt (`.ufo/waves/round-92/l1/c1-landing-r92.txt`) is taken as the meter's record.

Tally on the 25 mapped pairs: **16 CORRECT, 7 UNCLEAR (partial), 2 WRONG**. EXCLUDED: 2 AGREE.
No-edit: 3 AGREE.

## HIGH — WRONG (2)

1. `corpus/knowledge/triage-thresholds.md:58` and `:144` — the two token drops leave a cell whose
   only tie is false. Landed cells: `MATCHES: SKILL.md:117` (line 58, attempts exhausted) and
   `MATCHES: SKILL.md:117` (line 144, `MAX_ATTEMPTS`). At cb1ef2b SKILL.md:117 is
   `` `[lost-tree] claims/hackerone-anthropic/honest-zero-claude-code/provenance.json:29` `` —
   a provenance-shape line. `MAX_ATTEMPTS` occurs 0 times in SKILL.md; the only attempts statement
   is SKILL.md:191 (`real termination is status-file TERMINAL + telemetry attempts()>=2`).
   The labels' instruction "keep `SKILL.md:117`" is the cause: dropping mission-control.md:20-21 was
   correct (`attempt` occurs 0 times in that entry), but the survivor does not support the row.
   Re-runnable:
   `git show cb1ef2b9856df79c530f3ff1374fa9691ff56233:SKILL.md | sed -n '117p;191p'`
   `git show cb1ef2b9856df79c530f3ff1374fa9691ff56233:SKILL.md | grep -c MAX_ATTEMPTS`  (0)
   Remediation for a later tranche: repoint the two cells to `SKILL.md:191` (or restore a correct
   corpus tie); the remaining-tie rule is not met as landed.

## MEDIUM — UNCLEAR / partial support (7)

2. `:86`, `:87` (repoint to `intake-surface.md:83-88`). The range gives the score terms and the
   14/50 program counts, but not the rows' predicates (`id ∈ fleets/priority.json priority[]`,
   `{v.program : v.verdict === 'continue'}`); the missing-file default `{priority:[]}` is absent and
   `docs/review-verdicts.jsonl` is named at :97, outside the range. `MATCHES` overstates.
3. `:59` — mission-control.md:21 states the filter only generally ("DONE never redispatches; live
   leases and mission-file presence filter the candidate set"). `readStatus` occurs 0 times in the
   entry, so `readStatus(id) exists AND state ∉ TERMINAL` is not restated.
4. `:152` — mission-control.md:61 states the <15 min window; the row's `20000`-char tail occurs
   0 times in the entry, yet the cell is a bare `MATCHES`.
5. `:153` — mission-control.md:54-55 states the UTC-3 12:00-22:00 window but not the row's modulo
   formula (`getUTCHours` 0 hits). The row's second tie `SKILL.md:14-15` is stale: `peak` occurs
   0 times in SKILL.md; the window text is SKILL.md:265-266.
6. `:150` — mission-control.md:69-70 lists 8 SYNC_PATHS groups; the row's 11 entries (adding
   `bounty-map`, `README.md`, `.gitignore`) are not stated.
7. `:177` — claim-gates.md:21-23 describes per-artifact `realpathSync` confinement inside realDir,
   not the row's package-root `realpathSync(dir)` "resolves the package once"; that behavior is not
   restated anywhere in the entry.

## LOW — row-gloss defects on otherwise-correct landings (2 rows, plus systemic)

8. `:390` — mapped tie is correct (ops-invariants.md:18 = `['cursor','opencode']`), but the row also
   cites `SKILL.md:525`, which at cb1ef2b is the parking-classifier text; BANNED is at SKILL.md:322.
9. `:90` — landed qualification is correct (mission-control.md:20: `freshness.live` +1), but the row's
   SUPERSEDES `SKILL.md:113-114,175-176` is stale: those lines are the round-14 provenance correction
   and the intake reward paragraph; the five-term score is now SKILL.md:182-185 and already includes
   `is_live(1)`.
10. Systemic (out of tranche 7, routed as a qualifier): triage-thresholds.md carries 30 bare
   `SKILL.md:N` refs; all five that appear in mapped rows are stale (117→191, 14-15→265-266,
   525→322). These are root-level refs the meter's M4/M5 never classify (HOST abs_tokens=127), so
   the 960/1944 rate cannot see them. A separate root-ref audit tranche is warranted.

## EXCLUDED pairs — 2 AGREE

- `:437` (`intake-surface.md:75-76`, excluded from the :89-90 repoint). AGREE. The cell quotes the
  superseded text `reward.min present on 48`, which sat at pre-round-13 intake-surface line 76 (the
  75-76 range is a faithful audit-time target; verified at 7483333^ and fb9ac8e). Repointing to :89-90
  under that quote would be false — :89-90 states the corrected "reward object on 48 but numeric
  `reward.min` on only 14".
- `:438` (`mission-control.md:37-38`, excluded from the :56-57 repoint). AGREE for the mechanical edit:
  :56-57 states `openai-codex/gpt-6-astra:max`, so repointing under the quoted
  `openai-oauth/gpt-6-astra:max` would make the quote false. **Residual defect** (not fixable by the
  mechanical token swap, so the exclusion is still right): the Supersedes target 37-38 is wrong even
  as a historical reference — the pre-correction text was at mission-control.md:52 (`d87f2fa`,
  `fc6d398`); :37-38 is the P20/P21 block. A correct repair rewrites the cell to
  `mission-control.md:52`, keeping the quote.

## No-edit pairs — 3 AGREE

- `citation-bases.md:14` / `claim-gates.md:3` and `/ ops-invariants.md:18`: the bare forms are the
  paragraph's counter-examples (L14 forbids them; L16 says a bare subdirectory cite classifies GONE).
  Qualifying them would destroy the example.
- `japanese-domestic-disclosure-workflow.md:7` / `japanese-domestic-disclosure-workflow.md`: the token
  names the staged package entry under `/home/vgpnk/Projects/shokuknow/merge/kasegi/` (read-only merge
  input), not a corpus/knowledge line citation.

## Residual risk / verification gaps

- I did not re-run `knowledge-meter.py`; the 947/1947 → 960/1944 pass is taken from the L1 landing
  receipt. My verdicts are prose-support judgments over the landed bytes; the meter's M-limbs are
  structural and cannot catch the two WRONG survivor ties.
- No LSP server exists for Markdown prose semantics (`lsp` is not mounted for this lane), so the
  caller/definition check was done by direct read of every cited entry at cb1ef2b and by counted
  greps; no grep result is presented as semantic proof beyond the cited lines.
- The 2 WRONG rows are confined to the `SKILL.md:117` survivor; no mapped `corpus/knowledge` anchor is
  out of range (M5 receipt), and no landed byte outside the 25 mapped lines changed (M3 receipt).
- Scratch `/fast/scratch/hyaku/kasegi-r92/ReviewC1Sites` was deleted.

## Files written

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-92/w1/ReviewC1Sites.md`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-92/w1/ReviewC1Sites-receipts/verdicts.tsv`
