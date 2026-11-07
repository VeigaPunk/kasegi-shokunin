# Round 84 — lesson (kasegi, attempt 1)

Read first: the r83 closure (admitted) and `corpus/lessons/round-83-verifier-spotcheck.md` (routed defects 1–8). Freeze `7f76b7eb690cd6e75e7f3e7729cedcb15611b34b` (base `a089ff3d601b4d53a5515e52720ba27e5ec72c3d`); frozen claims, predicates, kill rules and do-nothing controls in `.ufo/waves/round-84/claims.json`; controls executed and committed in the freeze (`.ufo/waves/round-84/controls/`). One v1 wave `w1` of 12 seats; reports under `.ufo/waves/round-84/w1/`.

## Claims

- **C1 — depth:verifiability (nominal per R58, 4 held).** Land the recheck-cwd successor `e5f2e4bd…` (six new checks: noprefix-only, summary-fields, entry-bare-pass, argv-values, verbose-order, entry-set) that kills all 76 non-neutral rows of a 79-row table, including the twelve r83 MutC1Hunt survivors H01–H12 that the landed r83 bytes and a check-name stub both let survive; and an r84 counter whose selftest fails three counter mutants (M09, M10, M12) that the r83 selftest passes. Not claimed: the F8/F12/F13 forgery class.
- **C2 — coverage (8 held).** Admit Frontier F60, `corpus/knowledge/osv-gcs-data-dump-layout.md`, on six pinned export-layout clauses of S118 (OSV.dev Data sources page); FRONTIER-CENSUS rows 59 → 60, knowledge 97 → 98, S118 `queued` → `mined`; the r83 entry gate passes unchanged. This is the round's sourced claim.

Axis-label disclosure (CriticTrend, `.ufo/waves/round-84/w1/CriticTrend.md` § C1): the scored depth:verifiability meter (`resolve.py`, `anchorcheck.py`) does not read the census instrument, so C1 is gate hardening with no meter move; the frozen claim already says so (`axis_score`), and the lowest-axis obligation has been carried by nominal moves since r70. Routed to round 85: either a `resolve.py`-read move or a recorded retirement/split of depth:verifiability.

## Gate

### S118 — OSV.dev, Data sources (admitted, F60)

- **URL:** https://google.github.io/osv.dev/data/ (HTTP 200; final URL equal to the requested URL).
- **Access date:** 2026-11-06; capture `corpus/source-snapshots/round-84/S118.txt` (sha256 `e824a73545bedd0abae5f84cd120a5c73e482d7e935bc1534a08a1e1adfa5359`, 129 lines, 5820 snapshot bytes from a 27419-byte page), `fetched_utc 2026-11-06T23:34:49Z`; manifest `corpus/source-snapshots/round-84/manifest.json` (six quotes).
- **Located quote (17 words), S118.txt:102:** "This bucket contains a zip file with all vulnerabilities across all ecosystems (including withdrawn records) at gs://osv-vulnerabilities/all.zip."
- **Row changes, old → new:** S118 added `queued` with used-by `—` in the freeze `7f76b7eb`; at landing status `queued` → `mined`, used-by `—` → `corpus/knowledge/osv-gcs-data-dump-layout.md`. Registry 117 → 118. No other row's status, recheck or used-by cell changed.
- **Independent re-open:** ScoutSource re-fetched the page and the upstream `docs/data.md`: all six quotes occur once at their pinned lines and the upstream wording is identical on those lines (`.ufo/waves/round-84/w1/ScoutSource.md` §1–2).
- **Distinctness, disclosed:** Claim 4 (per-ecosystem modified_id.csv rows omit the directory prefix) is a second-source pin of a fact F59's cited FAQ range also carries (S117.txt:99; ReviewC2 M2). It counts as one clause of a new entry on a new page, not as new ground on its own.

### Rejected / deferred this round

- **Reject:** the r83 hand-off quote for the OSV data-quality initiatives post ("Thereafter, we will begin gating record imports…"), because it spans snapshot lines 59–60 and a pinned quote must sit on one line (ScoutSource §4 lead 1). Flip condition: a one-line quote; ScoutSource offers a 12-word sentence on line 46. The post stays an unopened registry lead.
- **Deferred lead:** OSV.dev GET /v1/vulns/{id} reference page (ScoutSource §4 lead 2); not registered this round.
- **Not a source:** the live bucket listing ScoutSource probed (30 colon-suffixed directories still served, frozen at 2024-10). It is recorded in F60's Limits as a reason not to over-read Claim 6, never as evidence for a claim.

### considerthese and assimilation

- **considerthese:** ConnectorOverlap read `considerthese/2026-10-26.md` and found one still-unimplemented proposal that fits the round: proposal 2's remaining half, run one end-to-end domain task and log it (SHONEN box 2), through `corpus/instruments/claim-package-check.py` (`.ufo/waves/round-84/w1/ConnectorOverlap.md` §3). Not adopted this round; it is the round-85 candidate. SHONEN box 2 stays `[ ]`.
- **Assimilation: none.** The staged-id collision check (0–3-space pattern, guard proven on an indented S118 fixture) gives 88 collisions, S031..S118 (`.ufo/waves/round-84/w1/ConnectorOverlap-receipts/assimilation/`). The r77 L0 question is still open.

## Mistakes

**M84-1 — class `rule-paraphrase-drifts-from-quote-vocabulary`.** The L1's first F60 draft had two falsifiable rules (Claims 1 and 4) that the r83 G6 tie limb scored `untied=2`, `ENTRY-GATE-RESULT fail`, rc 1 (`.ufo/waves/round-84/controls/c2-draft-v0-r84.txt`). Claim 1's rule spoke of "advisories" and "entries" where the quote says "vulnerabilities" and "records"; that is a real drift, and the rewrite names the quote's own objects. Claim 4's v0 rule was sound, and G6 failed it only because the five-letter stem cut keeps `file` and `files` apart. **Captured-by:** G6 for the first case. R134 already says a lexical limb is a heuristic, so the v1 pass (`untied=0`, `controls/c2-prefreeze-r84.txt`) is not cited as rule quality. ReviewC2 read all six landed rules for content and found one overreach, M84-2. **Fix:** run the gate before freeze and have a non-author review every rule. The gate step is shown able to fail (v0, rc 1) and pass (v1, rc 0).

**M84-2 — class `rule-consequence-contradicts-own-limits`.** The draft Claim 5 rule said a script looking for a release-suffixed dump directory "finds nothing". Two things contradict it. The page does not say that (S118.txt:121, :123). The entry's own Limits bullet calls the deleted-or-unrefreshed question unknown. CriticClaims B5 and ReviewC2 M1 caught it (`.ufo/waves/round-84/w1/CriticClaims-receipts/c2-claim5-limits-conflict.txt`). ScoutSource's live probe found the suffixed directories present and frozen (§3.4). **Captured-by: none.** G5 and G6 check shape and vocabulary, and no criterion compared a rule's consequence with the entry's Limits. **Fix:** QUALITY R135 and the rewritten Claim 5 rule. R135's check is shown able to fail and pass in `.ufo/waves/round-84/l1/r135-check-r84.txt`: it prints 1 on the draft rule and 0 on the landed entry. Over the other 97 entries it prints one hit, `osv-determineversion-cc-library-versioning.md:31`, which a reviewer read as a rule that rejects an absence inference, not an overreach. The grep is a pointer for that review, not a verdict.

## Routed-defect disposition (r83 spot-check, defects 1–8)

| # | r83 routed defect | r84 disposition | pointer |
|---|---|---|---|
| 1 | F12/F13 pass the r83 counter | carried, not claimed; CriticClaims A1 reproduced a table-lookup forgery of the same class under the r84 counter. P2/P3's `target_sha256` pin is the identity limb, and the counter itself does not defend against this class | `w1/CriticClaims.md` A1; `claims.json` C1 statement |
| 2 | P3 read only the MUTBAT summary | answered: P3 binds `target_sha256` and counts the counter's own per-row lines (76 counted, 12 H rows KILLED). CriticClaims A2: a target cannot inject those lines. MutCounter: the per-row limb detects no mutant that the summary limb misses | `claims.json` P3; `w1/MutCounter.md` §2 |
| 3 | `extra` limb not in the counter selftest (M09) | answered: r84_limbs extra/dup/decoy_line; M09/M10/M12 pass under r83 and fail under r84 | `controls/c1-counter-mutants-r84.txt` |
| 4 | G6 is lexical | carried; the r83 gate is reused unchanged and M84-1 shows its false-positive side again | M84-1 |
| 5 | MutEntryGate survivors; MutC1Hunt r83 gaps | MutC1Hunt half answered (H01–H12, six checks); MutEntryGate carried | `c1/mutant-table.json` |
| 6 | `comment_lines` f-string (latent) | carried | — |
| 7 | landing receipt measured over a pre-commit worktree | answered: `l1/landing-r84.sh` extracts the named landing commit with `git archive` and runs every predicate on the extract | `.ufo/waves/round-84/l1/L1-landing-r84.txt` header |
| 8 | r82 carry-overs | carried behind rows 4, 5 and 7 | `corpus/lessons/round-83.md` |

## Routed to round 85

- MutC1Hunt r84: 22 survivors over the frozen candidate (`w1/MutC1Hunt.md`), led by the summary-fields slots its fixture holds at zero (X09/X10/X18), exit-1 missing from entry-set (X11), no subprocess end-to-end CLI test (X13/X14), conform_ok limb coupling (X21) and five unasserted selftest restores (X01–X05).
- MutCounter r84 (these ids are the seat's own M01–M16, not the M09/M10/M12 of the C1 control): 7 of 16 counter mutants pass the selftest (M01, M08, M09, M10, M12, M13, M16); M14 passes only by its printed line, and its rc 1 fails P4. The seat counts 5 that survive the meaning of P3, P4 and P5 together. One of those is M13, `r84_ok` forced to True, so the new limbs are not self-protecting (`w1/MutCounter.md` §1).
- ExecC1RealTree: a malformed or unreadable `--root` exits 1 rather than the docstring's exit 2 (`w1/ExecC1RealTree.md` § Routed defects).
- CriticTrend: depth:verifiability label. Either a `resolve.py`-read move or a recorded retirement/split. The six SCORECARD "Planned round 84" items that were not delivered are listed in SCORECARD § Round 84 rather than rewritten in place.
- Leads: the data-quality initiatives post (one-line quote) and GET /v1/vulns/{id}.
- considerthese proposal 2: one end-to-end claim-package task.

## Landing values

Every landing predicate value is in `.ufo/waves/round-84/l1/L1-landing-r84.txt`, measured over a `git archive` extract of the landing commit that receipt names.
