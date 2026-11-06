# ReviewRouted — round-80 w1: re-measurement of the round-79 spot-check routed defects

Seat: ReviewRouted (leaf reviewer). Every command below was re-run by this seat over the lane tree at its current bytes; no routed reason was transcribed as a verdict. Frozen r80 bytes verified before use (all three pins match):

| frozen byte | sha256 (measured) | pin |
|---|---|---|
| `.ufo/waves/round-80/c1/recheck-cwd-census.py` | `420151fdea1187aa308f63536216039746fc9d784f6096c36627b7513e505698` | matches prompt pin |
| `.ufo/waves/round-80/c1/mutbat.py` | `b47276d1f96795d8b430de0be195f26122ffa6d673fb4b25e88250d8fcb7d450` | matches `b47276d1…d450` |
| `.ufo/waves/round-80/c1/mutant-table.json` | `08d7f3cebc5b40dfb6a03a0ba5caa1f1aa848b3bbc3d9e0b6b969497098ea418` | matches `08d7f3ce…e418` |

No lane file outside `.ufo/waves/round-80/w1/` was written. No tools installed (nothing to record under the 2026-10-19 authorization).

## Item 1 — retract the round-79 Q12 correction (`corpus/lessons/round-79.md:37`)

Commands re-run by this seat:

1. `grep -n -i 'threading\|vary' corpus/knowledge/osv-post-v1-query-contract.md` — **one match, line 47**, whose tail reads: `The page size is not fixed: "The page size can vary slightly because of threading and may change in the future." (S108.txt:136).`
2. `git log --format=%h -S'vary slightly because of threading' -- corpus/knowledge/osv-post-v1-query-contract.md` → `6582d14`; `git show -s 6582d14` → `6582d14 2026-11-05 05:04:35 -0300 round-73: Q10 recheck cwd repair (11 lines) and F51 OSV.dev POST /v1/query contract on S108`.
3. Snapshot corroboration: `corpus/source-snapshots/round-73/S108.txt:136` ends `...The page size can vary slightly because of threading and may change in the future.`, and `corpus/source-snapshots/round-73/manifest.json:48` pins exactly that quote as `Q30-page-size-vary`, anchor 136. F51 has held the sentence since round 73.
4. The bullet under correction (`corpus/lessons/round-79.md:37`) claims `grep -n -i 'threading\|vary'` over the entry "finds no variance caveat" and that `:47` "holds the single-query pagination trigger". Both false as a pair: line 47 verbatim holds the trigger AND the caveat, both quoting S108.txt:136.
5. Third leg checked: the bullet says F54's `Not claimed` line "carries the same wrong cite". Measured `corpus/knowledge/osv-post-batch-query-contract.md:61`: it cites "ground F51 already holds at `...osv-post-v1-query-contract.md:21` and `...:47` (S108.txt:40,41,136)" — **correct**, because F51:47 does hold the caveat. The accusation is false.
6. The S112 sentence the bullet quotes exists: `corpus/source-snapshots/round-77/S112.txt:170` and `round-78/S112.txt:170` = `These numbers can vary slightly because of threading and the page size may change in the future.` (pinned `Q12-threading-variance`, anchor 170, in the round-77 manifest), directly following the `3,000 vulnerabilities` count at S112.txt:169.

**Verdict: AGREE with the closure.** The r78 reject reason ("restates ground F51 already holds at :47") is right. The r79 appended correction at `round-79.md:37` is wrong — false grep premise, false description of :47, false accusation against F54:61. The r78 verifier spot-check item 4 and its routed item 1 stay withdrawn.

**Exact appended-correction text for the L1** (append to `corpus/lessons/round-79.md`; never edit :37 in place):

> - **Appended correction — the round-79 appended correction above (the Q12 bullet) is retracted (appended here, never in place).** Re-measured this round: `grep -n -i 'threading\|vary' corpus/knowledge/osv-post-v1-query-contract.md` matches line 47, which holds both the single-query pagination trigger ("pagination will occur when there more than 1,000 vulnerabilities in the response, or when the query has exceeded 20 seconds.") and the variance caveat "The page size can vary slightly because of threading and may change in the future." — both quoting S108.txt:136; the sentence has been in F51 since round 73 (`git log --format=%h -S'vary slightly because of threading' -- corpus/knowledge/osv-post-v1-query-contract.md` → `6582d14`, the round-73 F51 commit; pinned there as `Q30-page-size-vary`, `corpus/source-snapshots/round-73/manifest.json:48`). The retracted bullet is wrong on all three of its measurements: the grep is not empty; `:47` is not only the pagination trigger; and F54's `Not claimed` line (`corpus/knowledge/osv-post-batch-query-contract.md:61`) does not carry a wrong cite — its `:47 (S108.txt:136)` reference is correct and needs no correction. The round-78 reject reason stands as written: the S112.txt:170 note restates ground F51 already holds at `:47`. The round-78 verifier spot-check item 4 and its routed item 1 remain withdrawn. The one surviving observation is successor-entry refinement only, not a defect: the S112.txt:170 note sits directly beside the querybatch counts it qualifies (S112.txt:169) and could be claimed by a future querybatch entry if that ground is ever re-opened.

## Item 2 — D1 line cite: `mutbat.py:41` → `:40`

Commands re-run by this seat:

1. `grep -n 'EXC_RE' .ufo/waves/round-79/c1/mutbat.py` →
   - line 40: `EXC_RE = re.compile(r"^selftest case=\S+ FAIL .*exception", re.M)` (definition)
   - line 62: `    if EXC_RE.search(out):` (use)
   - line 41 is blank (visible in the same output).
2. `grep -rn 'mutbat.py:41' corpus SCORECARD.md LOG.md` → exactly three hits, none in SCORECARD.md or LOG.md:
   - `corpus/QUALITY.md:581` (the R129 evidence cell)
   - `corpus/lessons/round-79-verifier-spotcheck.md:28` (the D1 statement itself — a correct report of the defect, not a stale cite)
   - `corpus/lessons/round-79.md:53` (M79-2 root cause)
3. Out of the L1's write scope, for the record: the fleet report `.ufo/reports/round-79/kasegi.md:25` also cites `c1/mutbat.py:41` (same off-by-one).

**Verdict: AGREE.** The committed r79 counter bytes define `EXC_RE` at line 40; every `mutbat.py:41` citation is off by one.

**Exact appended-correction text for the L1** (append to `corpus/lessons/round-79.md`; plus the appended note for the R129 evidence cell in `corpus/QUALITY.md`):

> - **Appended correction — line cite (appended here, never in place).** The r79 counter's classifier is defined at `.ufo/waves/round-79/c1/mutbat.py:40` (`EXC_RE = re.compile(r"^selftest case=\S+ FAIL .*exception", re.M)`; line 41 is blank; used at `:62`). Every citation of it as `mutbat.py:41` — `corpus/lessons/round-79.md:53` and the QUALITY R129 evidence cell — is off by one; read `:40` in each. This corrects the citation only; R129's requirement and the r79 NOT VERIFIED outcome are unchanged.
>
> (For the QUALITY R129 evidence cell, append: "*Correction (appended): the frozen classifier cited here as `.ufo/waves/round-79/c1/mutbat.py:41` is at `:40`; see the round-79 lesson's appended line-cite correction.*")

## Item 3 — C1 successor vs the frozen round-80 bytes

Commands re-run by this seat (over the frozen bytes; pins verified above):

1. Row census: `mutant-table.json` parses to **28 rows** (consistent with the frozen kill_rule, "Any of the 28 rows"); ids in file order:
   `K-M1 K-M2 K-M3 K-M4 K-M5 K-X1 K-X2a K-X2b K-M8 K-W1 K-W2 K-N1 K-P1 K-P2 K-G1 K-C1 K-NP K-CL K-T1 N10 N11 N21 N25 N26 N27 N30 T1 T2`
2. Survivor presence vs the routed item 3 list — **all nine present as literal frozen row ids**, each class `"assertion"` with a concrete real-gap expectation:
   - MutC1Hunt real-gap survivors: **N10 ✓ N11 ✓ N21 ✓ N25 ✓ N26 ✓ N27 ✓ N30 ✓** (e.g. N21 `exit_other bucket folded into exit1_foreign -> prefix-census FAIL`; N25 `only the first side log consulted -> gate-predicates FAIL`; N30 `foreign cwd inherited -> prefix-census FAIL (fresh-cwd entry exits 1)`).
   - ReviewEquiv half-B survivors: **T1 ✓ T2 ✓** (T1 gate-consume predicate argument neutered to a constant → gate-wiring FAIL F4; T2 RESULT limb ret conjunct neutered → gate-negpolarity FAIL).
3. "P7 as a code-literal check": frozen `claims.json` P7 reads: *"At the landing commit, over corpus/instruments/recheck-cwd-census.py: `grep -c 'subprocess.run('` = 1, `grep -c '\"bash\", \"-c\"'` = 1, `grep -cE \"[\\\"']/tmp\"` = 0."* — that is a code-literal check (three literal grep counts over the instrument source), which is what the carried item demanded. Measured over the frozen candidate bytes: **1, 1, 0** — P7's values hold at freeze.
4. Third leg of the carried item, confirmed in passing: the r80 counter keys exceptions on the dedicated marker — `mutbat.py:42` `EXC_RE = re.compile(r"^selftest case=\S+ FAIL exception=", re.M)` (header: "keys on the dedicated marker 'FAIL exception=' … never on a free-text substring of the detail"; counting rule at `:95` counts `EXCEPTION-KILL` only for rows classed `exception`), and P8's frozen selftest row T-KILL (an assertion FAIL whose detail mentions "exception") must score KILLED counted=yes. R129-keyed, as required.

**Verdict: AGREE — the carried routed item 3 is satisfied by the frozen bytes**: every listed survivor class is a frozen table row, and P7 is a code-literal check whose values hold. Nothing to correct; no appended text needed for this item. M77-3 (TMPDIR crash) remains open on the lane tree, as the routed item itself states; the frozen P7 `/tmp` literal (= 0) does not close it.

## Residual notes

- Row ids are non-contiguous by design (no K-M6/K-M7/K-M9+; K-M8 present). The 28-row census is the binding count and matches the kill_rule; no row is missing behind an id gap.
- The r80 counter's `EXC_RE` sits at its own line 42. No pin cites an r80 counter line, so there is no current off-by-one exposure — noted only to prevent a future `mutbat.py:41`-style transcription.
- S108's snapshot lives under `corpus/source-snapshots/round-73/` (the r79 spot-check cited `S108.txt:136` without the directory); this report names the directory in every snapshot cite.
