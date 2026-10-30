# Round 46 — Kasegi

Lane: `kasegi`; attempt 1 (L1 `KasegiR46`, which held the planner seat — the validator rejects a `planner` role, so none was dispatched). Round-open base: `914ca0b6956f01d87b2e252ffad06fe74ec5d9ba`. Frozen claims commit: `9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5` (`.ufo/waves/round-46/claims.json` sha256 `e56ebf872b6073964d98812608275f5799afc9ee2334d4aab1363c06e59cd740`, never edited; `freeze.txt`; counters v1 `r46-c1-gate.py` sha256 `b0c730c8…2294` and `r46-c2-gate.py` sha256 `0ee95857…c6f3`; capture `S073.txt` sha256 `66c96a61…1930`). Measurement basis: `.ufo/waves/round-46/controls/final-measure.txt` at lane commit `eb874bc86ad7a6cfec299088e5a2d7ec68cf61b7` (the documents of this lesson, `LOG.md`, `SCORECARD.md`, `SHONEN.md` and the SKILL/instrument registry rows are the commits after it).

Claims: C1 (`depth:verifiability`) gated `recheck:` lines 24 → ≤22 by re-grounding `claim-package-contract.md` and `claim-gates.md` onto committed bytes; C2 (`coverage`) frontier F28, GitHub private vulnerability reporting (reporter flow), source S073, entry `corpus/knowledge/github-private-vulnerability-reporting.md`. Neither is exploratory.

Frozen-tree readings (the spot-check item 5 / QUALITY R52 rule: before-value per start tree). Counters v1, run from the lane against a base export and the freeze export: C1 `c1-gate fixed=1/7 exit=1` at the base and at the freeze tree; C2 `c2-gate fixed=1/7 exit=1` at the base and `fixed=2/7 exit=1` at the freeze tree (the freeze commit already carries the S073 capture and manifest, so G4 reads green there). Both readings are stated; neither narrows the target.

## Mistakes

Round-45 spot-check disposition (`corpus/lessons/round-45-verifier-spotcheck.md` §6): item 1 is answered below as M46-2 (it did not reproduce); items 2–5 are answered in `## Routed defects`.

| ID | Class | Error | Evidence pointer | Captured by | Fix | Evidence the fix can fail |
|---|---|---|---|---|---|---|
| M46-1 | vacuous | The round-46 C1 counter v1 and C2 counter v1 were frozen with nine cheap controls and no mutant battery. Wave 1 and wave 2 found eleven trees that carry the defect and read 7/7 on v1: a recheck line `true  # r46-c1-gate.py --entry …`, a `cd ~/Projects/bounties && …` line, a planted anchor, a dropped restoration line, a tree-supplied line executed with the host environment, and six C2 filler or wrapping shapes (`--source S0730`, a junk table row, an emptied Limits section, a URL wrapped in another host, a citation range 1-589, a stray non-md file in `corpus/knowledge`). | `wave1/R46RevC1L3.md`, `wave1/R46RevC1L1.md`, `wave1/R46SentinelGate.md`, `wave1/R46MutC2a.md`, `wave1/R46MutC2b.md`, `wave1/R46MutC2c.md`; `controls/controls-v1.2.out.txt` | R48 (presence-only predicates; it existed and was not applied before the freeze) | Counters hardened to v1.2 (`counter-errata.md` E1, E2); selftests `r46-counters-selftest-c1.py` (76 cases) and `-c2.py` (137 cases); QUALITY R50 (a pre-freeze single-edit mutant battery, three mutants per limb, survivors closed or disclosed) | `controls/controls-v1.2.out.txt`: eleven controls print `v1 … GREEN` and `v1.1 … RED` (the file's `v1.1` label names the hardened counters; their sha256 prefixes `95f2eb79…` and `647bd5b7…` are v1.2); `controls/selftest-vs-frozen-v1.txt`: each selftest run with `--counter` set to the frozen v1 bytes prints `selftest cases=76 failures=40` (C1) and `selftest cases=137 failures=121` (C2). Two controls stay green and are disclosed, not hidden: `c1 hollow-rows` (claim cells rotated across rows: no mechanical limb reads claim text) and `c2 core-in-HTML-comment` (the control wraps one occurrence of the AI-assistance quote while a second live occurrence remains, so the defect is not present; wrapping both reads `c2-gate fixed=5/7`, G2 and G5 red). |
| M46-2 | stale-premise | Round-45 spot-check §6 item 1 read the report commit's AUTHOR stamp (19:30:06) as the time the report was filed and the lane commit's committer stamp (19:36:31) as later, and called it an ordering defect. The committer clocks and both reflogs show the lane commit existed first (committer 19:36:31 against the report commit's committer 19:37:42; reflog `2998baa HEAD@{19:36:31}`, `a1f7761b HEAD@{19:37:42}`); an amend or a jj rewrite keeps the author stamp and moves the committer stamp. The lane accepted the item as a defect and the first landing gate carried a `date-order-author` check; it failed the round-44 pair, the round-28 pair, the round-45 pair and a constructed honest amend alike, and passed only a report authored after landing. | `wave2/R46W2CritMistake.md` F1-F5; `corpus/lessons/round-45-verifier-spotcheck.md:22`, `:95`; `git -C /home/vgpnk/Projects/shokunin log --format='%h %aI %cI' -- .ufo/reports/round-45/kasegi.md` | none | The author-time check was removed; `r46-landing-gate.py` keeps the committer-clock `date-order`, ancestor, final-is-tip and quiescence checks; its selftest asserts the round-45 shape PASSES; QUALITY R51 (re-derive a routed defect from committed clocks before building a gate on it) | `r46-landing-gate.py --selftest` prints `selftest cases=30 failures=0`, including `post-honest-rewrite-author-earlier-than-cited-round45-shape` (must pass) beside `post-date-inversion-committer-and-author` (must fail); the withdrawn check's red-before is `wave2/R46W2CritMistake.md` F2-F4. The class is `stale-premise`, not `landing`: the premise (author time as filing time) was wrong. |
| M46-3 | scope | Wave-1 drafts and the integrated F28 entry and re-ground rows carried statements the sources do not make: a claimed contrast of AI-handling policy between the kernel page and GitHub's page (GitHub's page states no handling rule), a link count of three where the capture shows four, a fork called a "drafting step", an overclaim that the recheck line re-verifies every quote (it verifies the sha256 and eight pinned quotes), a `report.md` "heading" check the committed gate does not make (`claim-package-check.py:120` searches anywhere in the text), a secrets regex stated wider than the committed one, and rows citing an entry line the entry never wrote. The committed gate was also written from the entry, so its rows show that the entry's description is implemented, not that the lost `claim-check.mjs` behaved so. | `wave2/R46W2RevEntryRule.md` F-1…F-6, `R46W2RevEntryTable.md` findings 2-5, `R46W2RevEntryOverlap.md` rows 3, 4, 22, 24, `R46W2RevGroundContract1.md`/`3.md` (G18, G19-G21), `R46W2RevGroundGates2.md` (G17), `R46W2RevGroundGates3.md` (G24, G25) | Q3/Q4 (quote and attribution), and the re-ground rule of R52 once written | The entry, the row claims, the Re-ground intros and the registry text were corrected in the wave-2 integration; both Re-ground sections now say the committed gate derives from the entry and list what stays historical | the per-row side-by-side reviews are the evidence (`wave2/R46W2RevGround*.md`, three BROKEN rows named and then reworded); no counter limb can check this, which is the disclosed residual of M46-1 (`c1 hollow-rows` stays green). |

## Gate — frontier, source, and rejection

Candidates considered: GitHub private vulnerability reporting (L1 screen, `S073`); the Zero Day Initiative disclosure policy (`wave1/R46ScoutLeadZDI.md`, screened and left a lead); the OpenSSF vulnerability guide (404 at the L1's probe); `considerthese/2026-10-26.md` proposal 3 (`wave1/R46ScoutConsiderthese.md`); the `merge/kasegi/` package (`wave1/R46ScoutMerge.md`).

Admitted: F28, GitHub private vulnerability reporting (reporter flow), source S073 (tier A, kind docs, scope: GitHub's own statement of the reporter-side flow only), entry `corpus/knowledge/github-private-vulnerability-reporting.md`. README row `F28` and the `## Round-46 admission` block are at the end of `corpus/README.md`; capture `corpus/source-snapshots/round-46/S073.txt` (589 lines, 15568 bytes, sha256 `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930`) committed at freeze.

Rejected, with reason and flip: (1) the legacy docs URL `…/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability` as a separate source — HTTP 200 after one redirect to the S073 URL (`wave2/R46W2RevRegistry.md` H9); flip: the legacy URL serves a different document. (2) The ZDI policy as a round-46 row — screened, not written as a row (a lead is not a row; CORPUS rule 1): its 120-day deadline, 30/90-day patch-regression windows and "sole discretion" extension (`wave1/R46ScoutLeadZDI.md` §2, quotes located in that seat's own capture, sha256 `9dee8161…04e1`) overlap F02's timelines and the page names no start event for the 120 days; flip: a later round whose claim is the ZDI deadline rule, opened and cited by that round. (3) The `date-order-author` landing check — rejected after wave 2 (M46-2); flip: a clock that survives amends is found. (4) The author-time reading of §6 item 1 — see M46-2.

Assimilation: none. Id-collision guard run exactly as the prompt states against `merge/kasegi/SOURCES.append.md` (`wave1/R46ScoutMerge.md`): lane ids 72, staged ids 94, `comm -12` collisions 42, indented-row guard proved on a scratch `  | S002 |` fixture; the package's registry baseline (30 rows) is stale and no staged theme covers F28's ground; nothing appended, nothing written into `/home/vgpnk/Projects/shokuknow`.

considerthese: `considerthese/2026-10-26.md` proposal 3 ("Add a quiescence gate before `complete`", line 31) is adopted as `corpus/instruments/r46-landing-gate.py` (QUALITY R51; registry rows in `SKILL.md` and `corpus/instruments/README.md`). The ledger row (`corpus/knowledge/considerthese-proposals-ledger.md`, a section `## Round-46 dispositions`) is NOT appended this round: C2's G6 byte-pins the 62 base knowledge entries it does not exempt, and the ledger is one of them, so editing it would turn C2 red; the disposition is carried here and in the `LOG.md` entry and is appended in a later round together with a pin amendment. Proposal 2 (an end-to-end domain task) stays partially landed: the claim-checker landed in round 43 and round 46 re-grounded two lost-tree entries on it; SHONEN box 2 is still unexercised.

New source row S073 — URL `https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately`; access (UTC capture) `2026-10-28T22:56:49Z`, HTTP 200, `capture_url` equals the URL. Quote block, ≤25 words each, located by `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073` (`S073:sha256 OK`, `S073:Q1 OK` … `S073:Q8 OK`, exit 0):

- Q1 `S073.txt:560` (10 words): “Anyone can privately report a security vulnerability to repository maintainers.”
- Q2 `S073.txt:563` (6 words): “create a draft security advisory directly”
- Q3 `S073.txt:564` (13 words): “You can only report vulnerabilities privately for repositories where this feature is enabled.”
- Q4 `S073.txt:566` (18 words): “you need to initiate the reporting process by following the instructions in the security policy for the repository”
- Q5 `S073.txt:573` (14 words): “By default, you must provide a summary, details, proof of concept, and impact statement.”
- Q6 `S073.txt:574` (13 words): “Optionally, select I used AI assistance to find or write up this report.”
- Q7 `S073.txt:577` (20 words): “GitHub automatically adds the reporter of the vulnerability as a collaborator and as a credited user on the proposed advisory.”
- Q8 `S073.txt:578` (15 words): “only the repository maintainer can merge changes from that private fork into the parent repository”

Spot-check slots for the non-author closure (not filled by the lane): (1) re-open the S073 URL, locate Q1-Q8 in the live page or the capture (`wave2/R46W2ScoutLive.md` already re-fetched it: no drift, a lane seat); (2) F28 entry: does it state a rule a reporter can act on (the claim's kill rule); (3) run `r46-c1-gate.py` and `r46-c2-gate.py` on the tip export and the plain re-derivations in `counter-errata.md`; (4) read the 46 re-ground rows side by side against `claim-package-check.py` and the fixtures (the C1 verdict rests on this reading, not on the counter).

Census (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`): before `controls/sources-census-before.txt` — `W04 S028`, `W04 S029`, `W04 S072`, `kasegi ok`, exit 0; after (round end) the same three `W04` warnings and `kasegi ok`, exit 0; `capture-binding-check.py --root` `records=60 bound=60 unbound=0` (it read `records=60 bound=59 unbound=1` at the freeze tree, where the capture was committed before its SOURCES row: `wave1/R46CritCalibration.md` row 14; green once the S073 row landed).

## Status, recheck and used-by changes (old → new)

None on any pre-existing row: `diff <(git show 914ca0b:corpus/SOURCES.md) corpus/SOURCES.md` shows additive hunks only (the S073 row, one Search-log bullet, two Registry-changes bullets). The S072 / S070 pair (round-45 spot-check §6 item 4, `corpus/lessons/round-45-verifier-spotcheck.md:98`) is recorded in the `## Registry changes` bullet "Supersede-pair note": S072 supersedes S070, shares its canonical URL, and the census `W04 S072` warning is expected.

## Wave and result

Round shape: two waves, 97 seats (inside 64-128; no residual call). Wave 1: one v2 wave (`ufo-wave-policy-v2.json`), 64 seats — 17 scout, 15 scribe, 10 reviewer, 6 mutation-tester, 5 executor, 5 critic, 2 connector, 2 sentinel, 1 revenger, 1 simplifier (attack 21/64); `wave1-results.json` `seats=64`. Wave 2: one v1 wave (`ufo-wave-policy.json`), 33 seats — 12 reviewer, 9 mutation-tester, 6 critic, 3 executor, 1 scout, 1 sentinel, 1 connector (attack 27/33); `wave2-results.json`. Dead seats: none reported by the orchestrator; two seats outlived their siblings by tens of minutes (`R46MutC1b` in wave 1, `R46W2MutSelftestC1` in wave 2) and were asked by message to wrap up.

Wave 1 falsified counters v1 (every limb and gate had a green-with-defect tree) and supplied the drafts that landed: the two re-grounds, the F28 entry, the S073 row and notes, the selftests, the landing gate, the plain-measure script. Wave 2 falsified the integrated tree: counter survivors (v1.1 → v1.2), the entry and row defects (M46-3), a withdrawn landing check (M46-2), a registry text defect list and the cross-artifact consistency list, all repaired in the wave-2 integration commit `93140c1`.

## Routed defects (round-45 spot-check §6)

1. **Report/commit ordering (item 1).** Not reproduced by the committed clocks: M46-2. The gate was built anyway for the other half of the item's ask (cite the hash after `git ls-remote` shows it): `r46-landing-gate.py --pre-report` before the report, `--post-report` after; the report names the lane hash only after `ls-remote` prints it.
2. **Counter classification (item 2).** Decided inside the round, before closure: counter erratum, with the critic's objection and the partial-disagreement recorded (`counter-errata.md` Decision and E2: the E1 phrase "the sentence made literal" is withdrawn for L4, L6, L7, the token floor and every C2 change; a reader who reads the kill-rule parenthesis narrowly must read C1 as unverified on the frozen counter and rely on the plain re-derivations). Prose-predicate diff: `claims.json` is byte-identical to the freeze.
3. **Plain second measure per claim (item 3).** Every claim carries a `plain` list in `claims.json`; `corpus/instruments/r46-plain-measure.sh` and `controls/plain-rows.sh` run them with no python counter. Base → tip: gated lines 24 → 22 (`c1b`), `test -d ~/Projects` guarded lines 23 → 21, frontier rows 27 → 28, SOURCES rows 72 → 73, knowledge files 64 → 65, absence sweep 0 → 3 files (README, SOURCES, the entry); rows located by fixed-string search 25/25 and 21/21 (`final-measure.txt`).
4. **S072 / S070 pair (item 4).** Recorded in the `## Registry changes` section of `corpus/SOURCES.md` (see above).
5. **Per-held-axis next promotion limb (item 5).** `depth:verifiability` stays 4: limb 1 (zero gated rechecks) reads `gated=22` of 65, 22 to 0 remaining; limb 2 (the non-author 25/25 chains audit, `SCORECARD.md:331`) is untouched; the next claim targets the remaining 22 (the census `wave1/R46ScoutCensus1-8.md` classifies each entry as fully, partly or not re-groundable). `coverage` stays 8: the only written promotion heading is `### coverage, 7 → 8` (`SCORECARD.md:1547`); the ratio `(20 + F_admitted)/(20 + F_total)` stays 1.000 and 0/18 domain surfaces stay absent, so +1 frontier row is an expansion count, not a ratio move. No 8 → 9 criterion is written; this lesson does not invent one.

## Score and trend verdicts

Scores held: depth:verifiability 4, coverage 8, depth:density 9 (non-target guard: `density.py` byte-identical to base; SKILL.md mean 249.1 → 258.7 comes from the appended registry block and is not credited). Trends: expansion improved (F28 admitted; S073 mined; knowledge 64 → 65); quality improved (two counters falsified twice, each falsification changed committed bytes; two entries re-grounded with 46 rows read side by side by six reviewers; a withdrawn gate check; QUALITY R50-R52) with the C1 caveat in M46-3; discernment unchanged (the lane disagrees with one non-author spot-check item, §6 item 1, with a committed-clock reason; no non-author judgment of this round exists yet).

## SHONEN

All four boxes stay `[~]`; the round-46 evidence paragraph is in `SHONEN.md` (`## Round 46 evidence`).

## Attempt 2 (2026-10-29, L1 `KasegiR46`; re-dispatched round after the attempt-1 honest-stop)

Base `04af9bc92229232ea5cce8b32bfe59dd969eb26d` (the attempt-1 tip plus the closure-era stale-ready
removal); claims frozen at `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`
(`.ufo/waves/round-46/attempt2/claims.json` sha256 `ca73279f5464cf6395028c7e848b5d82bfec95794f03b7fd9b1a61cf000ca1d0`,
`freeze.txt`). C1 (`depth:verifiability`): the two attempt-1 counters reach full mutation coverage —
the frozen battery (`r46-mutbat.py` v1) at the base prints `uncaught=7` (c1) and `uncaught=13` (c2)
(`controls/mutbat-before.txt`), and the after-state is `uncaught=0` with every equivalent verdict
backed by a committed proof. C2 (`coverage`): frontier F29 = GitHub repository security advisories,
the maintainer-side advisory lifecycle (row S074, capture `corpus/source-snapshots/round-46-a2/S074.txt`,
sha256 `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`), 28 -> 29 admitted rows,
65 -> 66 entries, admission gate `r46-f29-gate.py` (R50 pre-freeze mutant receipt:
`controls/f29-r50-receipt.txt`, 21 mutants, 11 defect-tree flips, 9 disclosed). Neither claim is
exploratory. The attempt-1 counters `r46-c1-gate.py` / `r46-c2-gate.py` are not edited by the claims;
their amendments (v1.3 ledger exemption + junk-row conjunct) are errata E3 of this attempt
(`.ufo/waves/round-46/attempt2/counter-errata.md`), and the attempt-1 receipts stay reproducible at
their era export (`eb874bc` reads `fixed=7/7` under the v1.3 bytes).

## Mistakes (attempt 2)

| ID | Class | Error | Evidence pointer | Captured by | Fix | Evidence the fix can fail |
|---|---|---|---|---|---|---|
| M46-4 | unmeasured-coverage | The attempt-1 round shipped counters whose mutation coverage was asserted by controls and selftest tallies but never measured against a mutant battery; the attempt-2 battery measured 7 (c1) + 13 (c2) uncaught clause-level mutants on the day-old instruments, including an uncaught L6-control drop and an uncaught L2-equality relaxation. | `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt` (c1 `uncaught=7`, c2 `uncaught=13`, BATEXIT=1); mutants table `corpus/instruments/r46-mutbat.py` | QUALITY R50 (the author must run a single-edit mutant battery before the freeze; the attempt-1 round wrote R50 AFTER its freeze — the rule was mined but not yet mechanical) | `r46-mutbat.py` (committed, frozen before the wave) makes the battery the claim's counter: the after-state is `uncaught=0` with caught-or-committed-proof semantics; the extended selftests (83 + 147 cases) carry the dedicated cases | red-before: `controls/mutbat-before.txt`; a re-run of the v1 battery at the base still prints uncaught=7/13 (the battery's own do-nothing replay in `run-controls.sh`) |
| M46-5 | wrong-attack-class | The attempt-2 pre-freeze falsification of the new f29 gate ran only counter-mutants (R50) and no tree-level false-green probes; the wave-1 reviewers found seven tree-level false-greens the mutant pass could not see (indented duplicate frontier rows, entry-cell substring aliasing, recheck comment carrying shell text, redirector-wrapped URL, wrong-file locator, mid-line-comment core text, duplicated Registry section relayed green by the census). | `wave1/R46bRevF29H1.md` (F1, F3), `wave1/R46bRevF29H2H3.md` (F1, F3, F5), `wave1/R46bRevF29H4H5.md` (F2), `wave1/R46bRevF29H6H7.md` (F5, F6); the R50 receipt lists none of them | QUALITY R48 (limbs bind content and are graded by mutants that keep the marker and remove the content — i.e. TREE mutations) — R50 covers the counter side only; the tree side had no pre-freeze duty | gate v1.1 closes all seven (`counter-errata.md` E4: loose-indent parse + anywhere-count, exact entry cell, cadence-only comment tail, all-URLs-canonical, path-bound locator, mid-line comment strip, single-Registry-heading check) and QUALITY R53 (below) makes tree-level false-green probes a pre-freeze duty | the reviewer receipts quote each defect tree reading `fixed=7/7` on v1 and red on v1.1 (re-run at integration on the fixture builders) |
| M46-6 | stale-instrument-state | The attempt-1 C2 counter byte-pins its era state (28 frontier rows, 65 entries), so any later round's honest landing moves it red at the new tip; the attempt-1 report's open item (the considerthese ledger row) was blocked by that same pin for a full round. | attempt-1 `counter-errata.md` G6; this attempt's v1.3 reading at the tip (`5/7`: G1 28->29, G6 65->66 moved by THIS round's landing, recorded in `controls/final-measure.sh` output) | QUALITY R49's inverse: an instrument that pins era bytes needs its exemption story stated at freeze time, not discovered when a later round trips it | erratum E3 (ledger exemption with re-derived content pin; era-export receipts re-verified 7/7) and the report states the attempt-1 counter's tip reading as EXPECTED-MOVED, graded instead by `r46-f29-gate.py` | the era-export run (`final-measure.sh`) prints 7/7 under v1.3 bytes at `eb874bc` while the same bytes print 5/7 at the moved tip — the two lines are the fix's proof |

## Gate — frontier, source, and rejection (attempt 2)

Admitted: F29, GitHub repository security advisories — the maintainer-side advisory lifecycle
(draft advisory, temporary private fork, CVE request via GitHub as CNA with the 72-hour review
clock, the not-public and other-CNA boundaries, credit, publication visibility, the fix-version
duty), source S074 (tier A, kind docs, scope: GitHub's own statement of the maintainer-side flow
only; the reporter-side flow stays F28; advisory editing, the REST API and the Advisory Database
edit flow are out). URL
`https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories`
(served there after one redirect from the `about-repository-security-advisories` URL; the FINAL url
is the canonical one recorded in the manifest and row), access 2026-10-29T20:19:30Z, HTTP 200,
capture `corpus/source-snapshots/round-46-a2/S074.txt` (42 lines, 7087 bytes,
sha256 `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, manifest
`corpus/source-snapshots/round-46-a2/manifest.json` sha256 `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f`).
Entry `corpus/knowledge/github-repository-security-advisories.md` (45 located quotes,
`f29-gate` H5 `spans=45 located=45 failed=0 uncited=0 cores=5/5`).

Gate quotes (<= 25 words each, verified at their manifest anchors):
Q1 "Repository security advisories allow maintainers of public repositories to privately discuss and fix a security vulnerability in a project." (S074.txt:10);
Q2 "Privately collaborate to fix the vulnerability in a temporary private fork." (`S074.txt:13`);
Q3 "You can give credit to individuals who contributed to a security advisory." (S074.txt:17);
Q4 "GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers." (S074.txt:24);
Q5 "GitHub usually reviews the request within 72 hours." (S074.txt:25);
Q6 "Requesting a CVE identification number doesn't make your security advisory public." (S074.txt:25);
Q7 "GitHub cannot assign CVEs to your project if it is covered by another CNA." (S074.txt:26);
Q8 "Anyone can see the current version of the advisory data, as well as any advisory credits that the credited users have accepted." (S074.txt:31);
Q9 "you should add a fix version to a security advisory prior to publishing the advisory" (S074.txt:38).

Rejected, with reason and flip: (1) the GitHub Advisory Database as the F29 source — the database
row class was already screened and rejected in round 43 (S068, tier B REJECTED: it republishes
NVD's record; record-completeness defect), and the database is the publication target of F29, not
the lifecycle's first-party statement; flip: a first-party GitHub statement of the database's own
editing flow (a page the S074 capture names but does not hold) would be a new row. (2) The
repository-advisories REST API page — the S074 capture names it as a pointer only (S074.txt:16);
a leads entry, not an opened source this round; flip: opened + located quotes in a later round.
(3) The prior-attempt ZDI lead stays a lead (round-46 attempt-1 flip condition unchanged).

Status/recheck/used-by changes (old -> new): none on pre-existing rows — the SOURCES.md diff against
base `04af9bc9` is additive (S074 row + one Search-log bullet + two Registry-changes bullets);
`capture-binding-check.py --root` records=61 bound=61 unbound=0 (S074 binds its entry).

considerthese: the attempt-1 deferral is closed — the `## Round-46 dispositions` section is appended
to `corpus/knowledge/considerthese-proposals-ledger.md` (draft by ExecLedgerDraft, applied by the L1;
the v1.3 content-pin exemption is errata E3), closing the attempt-1 routed item.

Spot-check slots for the non-author closure (not filled by the lane): (1) re-open the S074 URL and
locate Q1-Q9 in the live page; (2) the F29 entry: does it state a decision rule a maintainer can act
on (the C2 kill rule); (3) run `r46-mutbat.py --root <tip export> --pure <914ca0b corpus export>
--work <scratch> --counter all` and read the three `uncaught=` values; (4) read the equivalence
proofs (`corpus/instruments/r46-mutant-equivalents/`) and try to falsify one; (5) re-run the
absence sweep at the base and tip exports (2 -> 4 files).

Census (attempt 2): before `controls/sources-census-before.txt` (exit 0, three W04 warnings);
after (round end) the same three warnings and `kasegi ok`, exit 0 (`controls/final-measure.txt`).

## Corrections (round 47)

- D5: the statement above that the S074 row landed with one Search-log and two Registry-changes bullets described bytes trapped inside drafting fences. Round 47 lands those three bullets verbatim as real section bullets in `corpus/SOURCES.md` and removes the instruction prose and fences. This is an explicit line-anchor migration: SOURCES.md lines below the deleted scaffold move; the old locations quoted in historical lessons remain historical, not current locators. Registry rows themselves retain their immutable cells.
- D6: the dropped findings in `.ufo/waves/round-46/attempt2/wave2/R46bW2RevEntryClaims.md`, `.ufo/waves/round-46/attempt2/wave2/R46bW2ConnW2.md` and `.ufo/waves/round-46/attempt2/wave1/R46bConnPatterns.md` identified the capture-chrome, source-order and fix-version-case errors. The F29 entry now distinguishes chrome from prose, states that the page puts the CVE request before the fix-version discussion, and distinguishes the two publish-without-fix cases from the qualified imminent-fix instruction to wait. Same-line replacements preserve its 145-line layout.
- D7: the original S074 capture and manifest remain byte-identical historical evidence. The current F29 entry instead cites S076, re-captured through the committed `capture-source.py --kind html` instrument. Its producing method is reproducible at the observed instants; this does not retroactively reproduce the original 42-line rendering or guarantee future server bytes.
- D8: S068 is one GHSA advisory entry, not the Advisory Database's documentation. The unopened repository-advisories REST-API page is now a Leads bullet. The old ZDI lead's proposed S074 was consumed; round 47 allocates S075 to the re-opened policy, without treating a suggested id as a reservation or automatically admitting new frontier ground.
- The round-46 `rejected-harmed` closure stands. These repairs neither rewrite its verdict nor convert its old receipts into measurements of the new tree.
- D5 exact section names: the bullets now live under `## Search log` and `## Registry changes` in SOURCES.md, outside any fence. The wave-2 integrated counter read 10/11 because the earlier correction used hyphenated prose labels; this clarification fixes that documentary mismatch without changing a frozen predicate.
- Wave-2 semantic sweep found additional inherited overclaims in the touched F29 entry: optional private-fork and CVE capabilities were made mandatory, fix-version exceptions were contradicted by the package rule, republication was contradicted by an absolute secrecy sentence, and publication-linked process timing was denied categorically. Round 47 corrects those sentences at stable line numbers; `.ufo/waves/round-47/w2/R47W2F29Claims.md` and `R47W2FixVersion.md` under that same wave directory record the evidence.
