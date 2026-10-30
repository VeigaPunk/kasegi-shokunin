author: hyaku closure (non-author integrator, @m_zfl)
round: kasegi 49 · closed 2026-10-30 · lane tip `de94a3924b4cc14a7dafb08dc174cf93441e07ce` (branch `master`, `ls-remote` verified) · report `.ufo/reports/round-49/kasegi.md`

## 1. Step-1 conformance

| Check | Result |
|---|---|
| Report committed in fleet repo by lane identity | PASS — `kasegi-shokunin <kasegi@shokunin.local>`: `bdd65436` (file 12:57:56 -03), `7ca12c6f` (post-filing tip correction 13:17:12), `be0493c2` (erratum 13:20:42, appended after the filed bytes, names the text it withdraws) |
| `SHONEN` heading, one line per box | PASS — `grep -c '^## SHONEN'` = 1; four `[~]`/`[ ]` lines matching the four SHONEN.md boxes; no `[x]` written by the lane |
| Cited lane commits exist and are ancestors of the branch | PASS — all 7 (`1954022d`, `a71cd118`, `6d1aad3d`, `7bfafc50`, `a693fce0`, `b329b7b4`, `de94a392`) pass `git merge-base --is-ancestor <hash> master`; base `9b1662a` and round base `11c9818` also ancestors |
| No uncommitted round work; pushed | PASS — `jj-lane.sh state`: `branch=master local=de94a392… remote=de94a392… ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` empty; `ls-remote origin refs/heads/master` prints `de94a392…` |
| Dispatch prompt carries the template contract | PASS — round-level items (i) MISSION/AXES binding with 1–3 distinct-axis falsifiable claims incl. lowest non-retired axis, (ii) L2 floor ≥8 in one batched call (matches `MISSION.md` L53 "at least 8"), (iii) commit-then-push, (iv) push scope, (v) L0 side channel; all five child-lane items (report path/filename, commit-before-report, SHONEN heading, hash-citation rule, write scope). Prompt committed (`834221df`) before launch |
| Marker vs report | Real report: names committed work with checkable hashes; not a marker. Status `ok` |
| Dispatch/completion digest (from `.ufo/watchdog.log`, lines 2017/2028) | `2026-10-30T12:46:07-03:00 launch kasegi round=49 pgid=1579490 driver=hyaku-inline attempt=1` / `2026-10-30T13:17:10-03:00 complete kasegi round=49; hyaku-inline attempt=1` — both verified verbatim in the live log |

Frozen bytes re-verified by my own sha256 over committed bytes: counter C1 `988a5370…` and counter C2 `010897bc…` identical at freeze `1954022d` and tip `de94a392`; `claims.json` sha256 `c299aeaf…` as recorded in `freeze.txt`. No seat scored before the freeze; the wave never ran (below), so no post-freeze rule change is possible.

## 2. Claim re-checks

### C1 — depth:verifiability (lowest non-retired axis, score 4): VERIFIED (evidence-verified + re-measured)

Gate evidence (verified, not executed — §Gate standard): committed receipts at the measured tip — `controls/do-nothing.txt` (base `9b1662a`: `unresolved-class=68`, `class-lane-bare=57`, `class-fleet-relative=11`, `class-total=147`, `ledger-rows=0`, `exit=1`), `controls/c1-final.txt` (`unresolved-class=0`, `ledger-rows=68`, `rows-resolving=68`, `findings=0`, `class-total=79` = the 79 protected-file members kept as named debt, `C1_EXIT=0`), `freeze.txt` self-test tally `cases=10 failures=0 exit=0`.

My own measurements over committed bytes:
- `git show de94a392:corpus/instruments/citation-reground-ledger.md` → exactly **68** data rows; class split `lane-bare=57`, `fleet-relative=11` (parsed per row).
- 8-row random sample across both classes: every new token's file exists at the tip and the old token is absent from **every** listed site file (0 fails).
- Axis census receipts match the report: base (`citation-survival.md` at `1954022d`) SKILL 130/694 = 18.73 %, lane total 1071/4696 = 22.81 %; tip (`resolve-after.log` + `citation-survival.md`) SKILL 132/701 = 18.83 %, corpus 1090/4372 = 24.93 %, all 1115/4758 = **23.43 %**. Arithmetic re-derived: both percentages exact.
- The erratum (withdrawn isolated-repair sentence) is honest: no committed artifact claims that measurement; the C1 predicate never rested on it.
- Score honestly held at 4: the score-5 bar (`score-gap.py`: 22 gated rechecks on lost bases) is a different measurement, and the report says so rather than re-scoring.

### C2 — coverage (8): VERIFIED (evidence-verified + re-measured), one disclosed deviation accepted

Gate evidence: `controls/c2-final.txt` — `FRONTIER-CENSUS rows=30 admitted=30 closed=30 problem-rows=0 registry=79`, `entries=33 pass=33 exit=0`, `FRONTIER-PASS F30 ids=S078`, `C2_EXIT=0`.

My own measurements over committed bytes:
- `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → base **29** → tip **30**; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → base **77** → tip **79**. Both match the report.
- `corpus/knowledge/cve-services-publication-api.md` opens with the provenance trio (`source:` S078 + capture sha, `verified-at: 2026-10-30`, `recheck:` naming `source-recheck.py --manifest … --source S078`) and ground F30; F30 row appended in `corpus/README.md` coverage map; PROVINCE.md gained exactly one end-of-file F30 frontier amendment.
- Capture binding: `S078.txt` at tip hashes `1403e607…`, 282553 bytes, 8374 `wc -l` newlines — identical to the entry's declaration and `manifest.json` (`sha256`, `bytes`).
- `manifest.json` carries 8 quotes Q1–Q8, each with a numeric line anchor; Q2 at anchor 125 is byte-identical to capture line 125 ("Reserves CVE IDs for the organization provided in the short_name query parameter (accessible to CNAs and Secretariat)", 17 words).
- SOURCES.md diff base→tip: +S078 (tier A, mined, used-by the new entry), +S079 (tier C, REJECTED with reason+flip, used-by `—`), +1 round-49 search-log bullet, and one search-log line whose only change is a C1 re-ground (`kake-shokunin/…` → absolute fleet path). No registry `status`/`recheck`/`used-by` cell changed — "rows touched: none" holds.
- Disclosed deviation: frozen `expect_after` read `registry=78`, measured **79** — caused by rejected row S079 added after the freeze, outside the claim. The kill rule binds `rows=30 admitted=30 problem-rows=0` and the entry's own recheck — all hold. Accepted; the frozen predicate was not amended to match (correct discipline).
- `sources-census.sh validate --root … kasegi` (my run): **exit 0**, exactly the four pre-existing W04 duplicate-URL warnings (S028, S029, S072, S076), no new findings — matches the report's before/after claims.

## 3. Discernment spot-check (non-author, this round)

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S078 + F30 admit | admit (tier A, `spec`, first-party) | live fetch of `https://raw.githubusercontent.com/CVEProject/cve-services/master/api-docs/openapi.json` → HTTP 200, 282553 bytes, sha256 `1403e607…` **byte-identical** to the committed capture; `openapi: 3.0.2`, `info.version 2.8.8.1`; Q2 quote located at `S078.txt:125` (17 words, ≤25) | **agree** | First-party CVE Program OpenAPI document, capture reproducible today; the entry teaches the write path (reserve/publish/reject/ADP/converse as distinct endpoints with distinct actors), which F25 (record format) and F07 (numbering rules) do not hold — novelty argument checks out |
| S079 reject | rejected row with reason + flip | live fetch of `https://docs.bugcrowd.com/researchers/reporting-managing-submissions/reporting-a-bug/` → HTTP 200, **129264 bytes** (exactly the byte count the row records from round 48); title "Reporting a Bug | Bugcrowd Docs"; raw body contains **0** occurrences of "dispute"/"Dispute" — a JS docs shell, no first-party dispute-route content | **agree** | The rejection reason is reproduced by an independent fetch; the flip condition (a first-party capture documenting the report-and-dispute workflow) is the right unblock. Landing the opened-then-refused source as a rejected row closes the round-48 curation defect correctly |
| staged-package refusal (assimilation: none) | refuse `shokuknow/merge/kasegi/` | committed id-collision screen (mass id drift; package holds no citation-base or CVE Services ground) | **agree** | Append-only registry bars wholesale renumbering; refusal is the only conformant move |

R60–R64 verified present in `corpus/QUALITY.md`, each citing the round-49 lesson; the M48-4/M48-6 fixes and their self-test tallies are committed (`selftest cases=5/17 failures=0` recorded in the SKILL registry rows and receipts).

## 4. Per-axis verdicts and trend verdicts

| axis | verdict | evidence |
|---|---|---|
| depth:verifiability | **improved** | `unresolved-class` 68 → 0 with `ledger-rows=68 rows-resolving=68 findings=0` (receipts + my ledger/site re-measurements); axis census 22.81 % → 23.43 % lane total (re-derived); score honestly held at 4 with the score-5 gap named |
| coverage | **improved** | frontier 29 → 30 admitted (F30, registry-verified, S078 tier A, capture byte-identical on live re-open); registry 77 → 79; score honestly held at 8 (denominator is the operator-owned lost-root 18-surface set, per rounds 38–46 precedent) |
| depth:density | **unchanged** | non-target guard; score 9 held; proxy 270.1 → 267.1 mean over 36 → 37 blocks, disclosed. (SCORECARD's "SKILL.md was not edited this round" cell is wrong — defect 2 below) |

- **expansion: improved** — one new admitted `knowledge/` entry on coverage-map ground the lane did not hold, `source:` citing `mined` row S078 opened this round; frontier row 29 → 30; no capability row claimed. Re-verified by me end to end.
- **quality: unchanged** — no admitted entry re-verified, deepened or superseded; nothing failed a re-check. The round's M48-4/M48-6 closures and R60–R64 are curation/repair, outside the quality observable (report says the same).
- **discernment: improved** — round-48 closure routed defects became lesson-backed criteria (R60–R64) or landed fixes; and the outside spot-check that the round could not carry (wave undispatched) is now on record: this verifier agrees with the gate on the sampled admit (S078/F30) and reject (S079). Both limbs of `LEARNING.md`'s discernment test now hold.

**Admission:** both claims verify on their frozen predicates, re-derivable from committed bytes; no owned axis harmed (SCORECARD diff `11c9818 → de94a392` only appends round-49 sections; no score decreased). **Verdict: admitted.**

**Wave disposition (noted, status-neutral):** the 64-seat wave-1 spec (policy v2, validator-clean, 31 attack seats) was built and handed over via `wave1.ready` (13:02); the operator's wrap-up ruling released it UN-DISPATCHED — no seat spawned, no `wave1-results.json`, no WAVE-DONE. The round claims no falsification credit and no seat count; the only conformity cost is that the round's L2 floor was met in build, not in run — an operator decision, recorded here and in the round notes.

## 5. Routed defects the lane must fix next round

1. **Report evidence pointers misname the ledger (3×).** `.ufo/reports/round-49/kasegi.md` cites `corpus/instruments/citation-ground-ledger.md` three times; no commit ever contained that path (`git log --all` empty). The actual ledger is `corpus/instruments/citation-reground-ledger.md` (68 rows, verified). Fix: appended erratum naming the three lines; the frozen `claims.json` and all receipts use the correct name, so no claim is affected.
2. **SCORECARD round-49 `depth:density` row is false:** it reads "`SKILL.md` was not edited this round, so the density instrument's input bytes are unchanged", but SKILL.md gained the two registry rows plus the M48-6 disclosure (verified diff). The report discloses the edit and the 270.1 → 267.1 movement correctly. Fix: append-only correction entry.
3. **SCORECARD C2 cells quote `registry=78`** (the frozen expectation) while the committed final receipt reads 79 (S079 added post-freeze). The report discloses the cause; the SCORECARD text was left stale. Fix: append-only correction.
4. **SCORECARD "Planned for round 50" cites "the round-49 scout seat … its report (in the wave directory)"** — no seat ran (wave released undispatched) and `wave1/` holds only `swarm-registry.json`. Fix: correction naming the actual starting point.
5. **Evidence hygiene (minor, no routing needed beyond this note):** the report quotes `anchorcheck.py`, `density.py` and `recheck-audit.py` outputs without committed receipts; the claim-bearing receipts (freeze, do-nothing, c1/c2-final, census-end, resolve-after) are all committed. Next round: commit non-target-guard outputs as receipts too.
6. **Open L0 (operator/aggregator):** `kasegi | round-49` in `.ufo/l0-questions.md` — the 79 protected-file class members sit in `round-*-verifier-spotcheck.md` / `round-*-aggregator-*.md` files the lane may not edit; owner of the re-ground to be decided.

## 6. SHONEN observation for the operator (promotion is operator-owned)

Boxes 1, 3 and 4 look fully checkable by a non-author verifier (SKILL.md decision tables/checklists/citations with resolvable sources; two new instruments runnable with committed self-tests; PROVINCE accurate with one appended amendment). Box 2 (end-to-end domain task) remains open. This verifier checked none of the boxes and wrote no `[x]`; the lane's own marks stay `[~]`/`[ ]`.
