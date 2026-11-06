# ReviewRouted — round-80 spot-check routed defects, re-measured (round 81, attempt 1)

Lane: kasegi. Frozen base `191e6ba8f872d08802d83b57cd7fcf4bfa122f0e`; HEAD at inspection `7ad3118c86ee14fde433d73671cc407668533cec` (freeze). Worktree carries uncommitted round-81 landing edits (`PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/knowledge-expected.txt`, `.ufo/waves/round-81/assimilation/`); none of them touches `corpus/lessons/round-80.md` (`git diff 7629cc56 7ad3118c -- corpus/lessons/round-80.md` is empty). Nothing in the lane tree was edited. No `git` write, no install.

Source of defects: `corpus/lessons/round-80-verifier-spotcheck.md` § Routed defects (items 1–3) and `corpus/lessons/round-80.md` § Mistakes / Appended corrections (CriticClaims (c) P6, (f)1 P3 — from `.ufo/waves/round-80/w1/CriticClaims.md`).

## Verdict summary

| # | defect | verdict | one-line basis |
|---|---|---|---|
| 1 | stale `osv-post-batch-query-contract.md:19` cite (ordering sentence is `:21`) | **still-open** | cites persist in `round-80.md` (:88, :160, :162, :169) and in `corpus/knowledge/osv-determineversion-cc-library-versioning.md:80`; r81 freeze does not touch them |
| 2 | "Six admits and four rejects" vs three reject bullets | **still-open** | Gate lists 3 bullets (:68–70); "four" holds only under a span rule the lesson never states |
| 3 | counter independence: forgeries reach killed=28 | **closed-by-r81** | `c1-forgeries-r81.txt` + my F1 re-run: r80 counter KILLED 56 rc0; r81 counter MISKILLED 56 rc1; `mutbat.py` never compares a byte pin |
| 4a | CriticClaims (c) P6 decoy (`grep -c` phrase in prose) | **closed-by-r81** | r81 P6 is line-anchored on the registry rows (`^\| recheck-cwd-census\.py \|`, ``^\| `corpus/instruments/recheck-cwd-census\.py` \|``) |
| 4b | CriticClaims (f)1 P3 ellipsis (`target_sha256=420151fd...5698`) | **closed-by-r81** | r81 P3 quotes no digest; it asserts the line ending `baseline=ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3` (the counter's own format, `mutbat.py:168–170`) |

Closures are on frozen bytes. Landing-commit re-checks (P4, P6 at the landing commit, P3 at the landing commit) stay with the L1.

---

## Defect 1 — stale `:19` cite

Commands run (verbatim, cwd lane):

```
grep -rn 'batch-query-contract\.md:19' --include=*.md . | grep -v '/\.ufo/'
grep -rln 'batch-query-contract\.md:19' --include=*.md . | grep -v '/\.ufo/' | wc -l   -> 3
grep -n -i 'guaranteed' corpus/knowledge/osv-post-batch-query-contract.md
  19:## Claim 2 — the response ordering is guaranteed to match the input
  21:"The response ordering will be guaranteed to match the input." (S112.txt:24). ...
  73:| C3 ordering | Q03-ordering | S112.txt:24 | 10 | "The response ordering will be guaranteed to match the input." |
```

`:19` is the section heading; the ordering sentence is `:21`. Confirmed.

Every stale cite (full scan of `*.md`, excluding `.ufo/`; QUALITY.md, SCORECARD.md, LOG.md, corpus/README.md contain **none**):

| file:line | text | status |
|---|---|---|
| `corpus/lessons/round-80.md:88` | full path `osv-post-batch-query-contract.md:19` (rule-shape held by F54) | **stale** — should be `:21` |
| `corpus/lessons/round-80.md:160` | full path `osv-post-batch-query-contract.md:19` | **stale** — should be `:21` |
| `corpus/lessons/round-80.md:162` | short form `F54 holds the input-matched ordering rule-shape (:19, measured)` | **stale** — short form of the same cite; not in the spot-check's list |
| `corpus/lessons/round-80.md:169` | short form `` `:58` ordering -> F54:19 `` | **stale** — short form; not in the spot-check's list |
| `corpus/lessons/round-80.md:14` | "F54 cite `:19` heading → `:21` sentence" | not stale — it records the old cite as a correction of ReviewC2 F-1 |
| `corpus/lessons/round-80-verifier-spotcheck.md:101` | describes the defect | not stale — defect report |
| `corpus/knowledge/osv-determineversion-cc-library-versioning.md:80` | full path `osv-post-batch-query-contract.md:19` ("input-matched ordering guarantee") | **stale** — knowledge entry, outside the lesson; route to round 82 (the other four cites on that line, :11 :27 :35 :43, are heading lines and correct as heading cites) |

Correction to the spot-check's own count: it says the lesson cites `:19` "three times (lines 88, 160, 162)". Measured: full-path cites are 88 and 160 only; 162 and 169 are short forms. The appended correction must name all four lesson lines.

Verdict: **still-open**. `git diff 7629cc56 7ad3118c -- corpus/lessons/round-80.md` is empty and `round-80.md` is not in the r81 claims' landing set, so no r81 artifact closes it. The fix is an appended correction (never in place).

### Appended-correction text for `corpus/lessons/round-80.md` (append at end of file; do not edit lines in place)

```
## Appended corrections (round 81, 2026-11-06; never in place)

- **Correction to lines 88, 160, 162 and 169 (F54 ordering cite).** The ordering sentence
  "The response ordering will be guaranteed to match the input." is at
  `corpus/knowledge/osv-post-batch-query-contract.md:21`; line 19 is the heading
  "## Claim 2 — the response ordering is guaranteed to match the input". Lines 88 and 160 carry the
  full path with `:19`; lines 162 and 169 carry the short form (`:19`, `F54:19`) for the same cite.
  Measured by `grep -n guaranteed corpus/knowledge/osv-post-batch-query-contract.md` (prints 19, 21, 73).
  Read `:21` wherever this lesson says `:19`. Routed from `corpus/lessons/round-80-verifier-spotcheck.md`
  item 1 (the spot-check's list of three lines omitted 169 and counted 162 as a full-path cite);
  re-measured in `.ufo/waves/round-81/w1/ReviewRouted.md` defect 1. Also stale, outside this lesson:
  `corpus/knowledge/osv-determineversion-cc-library-versioning.md:80` — routed to round 82.
```

---

## Defect 2 — reject count

Commands run:

```
grep -n -i 'reject' corpus/lessons/round-80.md
  14, 15 (routed text), 66 ("Rejected, with reasons" header: "all three are unpinned"), 169 ("Six admits and four rejects")
sed -n '20,94p' corpus/lessons/round-80.md | grep -n '^- \*\*S114\|^- \*\*The payload'
  -> bullets at lines 68, 69, 70 of that window = file lines 87, 88, 89 (measured):
     68 S114.txt:33 experimental status
     69 S114.txt:58, leading ordering clause
     70 payload skeleton (S114.txt:41-46) and samples (S114.txt:48-72)
```

State of the lesson:
- § Gate, "Rejected, with reasons": header says **"all three"**, lists **3 bullets**.
- § Learning, Discernment (:169): "**Six admits and four rejects**" and names `:33`, `:58`, "skeleton and samples" (three groups).
- Admits: 6 (cl1–cl6 table rows; equals the six manifest pins Q01, Q02, Q03, Q04, Q05, Q07). Confirmed.

**True count, by two rules:**
- Bullet rule (one per "Rejected" bullet): **3**.
- Span rule (one per unpinned S-file span; a bullet covering two spans counts two): `:33`, `:58` leading ordering clause, `:41-46` skeleton, `:48-72` samples = **4**.

The lesson's "four" matches the span rule, but the lesson never states a rule, and it says "all three" in § Gate. The two sections disagree on the same count. Note also that line `:58` is one line with two spans: the empty-object half is an admit (cl6), the leading ordering half is a reject. Counting lines instead of spans gives 3 rejects and 6 admits from 7 distinct clause-spans, which is why the lesson's sentence needs a stated rule.

**Proposed counting rule (for the appended correction):** a reject is one unpinned S-file span named under "Rejected, with reasons", split at span boundaries (a bullet naming two spans counts two); an admit is one manifest-pinned quote (one § Gate clause-table row). Under this rule: admits **6**, rejects **4**; § Gate's "all three" becomes "three bullets, four spans".

Verdict: **still-open**. Fix is an appended correction.

### Appended-correction text for `corpus/lessons/round-80.md` (append at end of file; the same block as defect 1 — one heading, two bullets)

```
- **Correction to line 169 (Discernment) and line 66 ("all three") — reject count.** The Learning sentence
  "Six admits and four rejects" and the Gate header "all three are unpinned" count different things.
  Counting rule used by this lesson, stated now: an admit is one manifest-pinned quote (one clause-table
  row: six, Q01 Q02 Q03 Q04 Q05 Q07); a reject is one unpinned S-file span named under "Rejected, with
  reasons", split at span boundaries. The rejected spans are S114.txt:33, S114.txt:58 (leading ordering
  clause), S114.txt:41-46 (skeleton) and S114.txt:48-72 (samples): **four rejects in three bullets**.
  Line 66's "all three" counts bullets, not spans. Routed from `corpus/lessons/round-80-verifier-spotcheck.md`
  item 2; re-measured in `.ufo/waves/round-81/w1/ReviewRouted.md` defect 2.
```

---

## Defect 3 — counter independence (forgeries reach killed=28)

Evidence (all re-measured by me):

1. Control receipt `.ufo/waves/round-81/controls/c1-forgeries-r81.txt` — F1 line pair (verbatim):
   - `FORGERY F1-location counter=r80 forgery_sha256=bc552edb…33f6 rc=0 verdicts={"KILLED": 56} … baseline=ok rows=56 killed=56 …`
   - `FORGERY F1-location counter=r81 forgery_sha256=bc552edb…33f6 rc=1 verdicts={"MISKILLED": 56, "NEUTRAL-BROKEN": 3} … rows=59 killed=0 survived=0 miskilled=56 … neutral_ok=0/3`
2. **My re-run of F1** (`.ufo/waves/round-81/w1/ReviewRouted-receipts/f1_rerun.py`, output `f1-rerun-r80.txt` / `f1-rerun-r81.txt`). It imports the frozen driver's own `forge()` and runs the frozen counters on the frozen 56-row and 59-row tables; the forgery sha256 matches the control (`bc552edb…33f6`). Results:
   - r80 counter, 56 non-neutral rows: `rc=0 verdicts={"KILLED": 56} … killed=56 survived=0 dirty=0 notderived=0`
   - r81 counter, 59-row table: `rc=1 verdicts={"MISKILLED": 56, "NEUTRAL-BROKEN": 3} … killed=0 miskilled=56 … neutral_ok=0/3`
3. The r81 tally rejects F1 without a byte pin. `grep -n sha .ufo/waves/round-81/c1/mutbat.py` finds only `:122` (`sha = hashlib.sha256(src.encode…)`, computed) and `:168` (the value printed in the summary line). No comparison of that digest to any constant exists. The per-row verdict is `MISKILLED` because FAIL lines appear on non-kill cases (`mutbat.py` verdict table, docstring lines 24–33; rule at `:90`), and the exit is `0 if fails == 0 else 1` (`:199`).
4. Both routes to rc1 are tally-based: `MISKILLED` 56 (the forgery's FAILs land on the wrong cases) and `NEUTRAL-BROKEN` 3 (the forgery breaks the moved-copy neutral rows). Either alone gives rc1.

Caveat, stated not scored: the forgery driver guards on the file's location (`basename(dirname) != "instruments"`), so the r81 tally's rejection of F1 is also caused by the moved copy breaking. That is the design: a location guard is a limb that must be killed by a case-matched row. The tally catches it without any hash.

Verdict: **closed-by-r81** on frozen bytes. The L1's landing re-check is P4 at the landing commit (`c1-forgeries-r81.py --lane … --work …`); this seat did not run it at landing.

---

## Defect 4a — CriticClaims (c) P6 decoy

r80 P6 (`claims.json` at `.ufo/waves/round-80/claims.json`): `grep -c` of the phrase `recheck-cwd-census.py --selftest -> selftest cases=15 failures=0` in `SKILL.md`, which CriticClaims showed matches prose as well as the row (decoy yields `1` and `1` while both rows read `cases=6`; `p6-decoy.txt`).

r81 P6 (frozen `.ufo/waves/round-81/claims.json`): "the SKILL.md registry row matching `^\| recheck-cwd-census\.py \|` and the `corpus/instruments/README.md` row matching `^\| \`corpus/instruments/recheck-cwd-census\.py\` \|` each contain 'selftest cases=22 failures=0' and no 'cases=15'".

Measured:
- Base `191e6ba8` and freeze `7ad3118c`, anchored patterns: `grep -cE '^\| recheck-cwd-census\.py \|' SKILL.md` = 1; ``grep -cE '^\| `corpus/instruments/recheck-cwd-census\.py` \|' corpus/instruments/README.md`` = 1. Both anchored rows contain `cases=15` at base (`grep -E … | grep -o 'cases=15'` = 1 each), so the r81 P6 "base: both rows contain cases=15" is correct, where the r80 wording "base: cases=6" was not.
- A prose decoy cannot satisfy a line-start anchor on `| recheck-cwd-census.py |`. The decoy shape the CriticClaims used (a phrase in prose) is excluded.

Residual, minor (not verdict-changing): P6 says "the row matching" and does not say "exactly one row". A second anchored row would pass. R113's own check (`grep -rn 'selftest cases='`) covers that case; the L1 can run it at landing.

Verdict: **closed-by-r81**.

---

## Defect 4b — CriticClaims (f)1 P3 ellipsis

r80 P3 wrote `target_sha256=420151fd...5698` with an ellipsis, which the counter's full 64-hex digest cannot match literally (CriticClaims (f)1).

r81 P3 (frozen): "… prints a line ending 'baseline=ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3' and exits 0". It quotes no digest, so there is no ellipsis. The counter's summary line is built at `mutbat.py:168–170`, and the candidate control (`c1-candidate-r81.txt`) prints `MUTBAT target_sha256=a3b58aa52ba0744199ee97e6bd837e62c499e3e6af03a2fc26f0e6e3746dbec0 baseline=ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3`, whose tail is the quoted string.

Verdict: **closed-by-r81**.

---

## Verification gaps and routed items

- Landing-commit re-runs (P1–P8 at the landing commit, P4 forgery driver, P6 rows at landing) were not run by this seat, per the seat's scope. L1 owns them.
- Routed to round 82 (not verdict-changing): `corpus/knowledge/osv-determineversion-cc-library-versioning.md:80` carries the stale `:19` cite (entry is outside this lesson).
- Routed (already in CriticClaims (f)2, not re-measured here): B7 depends on unfrozen sibling bytes (`sources-census.sh` walks the fleet root).
- Routed to L1 (cheap): the round-81 landing report should cite the defect-1 and defect-2 corrections in one appended block, not in place.

## Tooling

No installs, no upgrades. `python3` (stdlib only) for `f1_rerun.py`; `grep`/`sed`/`sha256sum` for the rest.

## Receipts

- `.ufo/waves/round-81/w1/ReviewRouted-receipts/f1_rerun.py` (the re-run driver)
- `.ufo/waves/round-81/w1/ReviewRouted-receipts/f1-rerun-r80.txt`
- `.ufo/waves/round-81/w1/ReviewRouted-receipts/f1-rerun-r81.txt`
