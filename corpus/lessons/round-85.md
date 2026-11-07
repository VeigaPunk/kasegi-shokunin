# Round 85 — lesson (kasegi, attempt 1)

Read first: the r84 closure (admitted), `corpus/lessons/round-84-verifier-spotcheck.md` (routed defects 1–6; item 3 asks for a `resolve.py`-read move or a recorded retire/split of depth:verifiability) and `corpus/lessons/round-84.md`. Freeze `4a2d34f203519a87078f21a896dc8679137ff675` (base `bc722e540c93b48ff159454b65a0f9f4630db1ed`). The frozen claims, predicates, kill rules and executed controls are in `.ufo/waves/round-85/claims.json` and `.ufo/waves/round-85/controls/`. One v1 wave `w1` ran 12 seats with 0 dead; the reports are under `.ufo/waves/round-85/w1/`.

## Claims

- **C1 — depth:verifiability (lowest axis, score 4; the claim reads the scored meter itself).** The frozen map `.ufo/waves/round-85/c1/repair-map.json` repoints 18 bare SKILL.md citations to their full lane paths. Each is a basename that `resolve.py` classifies GONE on this host and that names exactly one tracked lane file outside `.ufo/`. The resolve.py SKILL.md scope moves from 158/741 (21.32 %) to 167/732 (22.81 %). No other SKILL.md citation is added, removed or changed (limbs M1–M5 of `.ufo/waves/round-85/c1/skill-meter.py`).
  - CriticClaims A1 sets the qualifier: this is an internal-citation repoint. External RESOLVES stay at 4/741, so the score is held at 4.
  - ReviewC1Semantics read all 19 occurrences and judged all 18 CORRECT (`w1/ReviewC1Semantics.md` §1).
- **C2 — coverage, held at 8; claim type capability acquisition `priced-claim-package`.** This is the first end-to-end domain task logged for SHONEN box 2, from considerthese/2026-10-26.md proposal 2.
  - It builds the six-file practice package `corpus/practice/curl-h1-1913733/` for disclosed HackerOne report 1913733 (curl, CVE-2023-28319).
  - The package is priced from S119, S120 and S121 and from the round-35 KEV capture S052.
  - It is the round's sourced claim.

## Gate

### S119 — HackerOne report 1913733, JSON record (admitted, used by the package)

- **URL:** https://hackerone.com/reports/1913733.json, HTTP 200. Final URL unchanged.
- **Accessed:** 2026-11-07.
- **Capture:** `corpus/source-snapshots/round-85/S119.txt`, sha256 `9e4fb52e7e7572482fa29fc268dddbf7e249dd94c6850d2e383241ae14bc6105`, 5001 bytes, 1 line.
- **Located quote, S119.txt:1:** `"severity_rating":"medium"`. Also on that line: `"has_bounty?":false` and `"cve_ids":["CVE-2023-28319"]`.
- **Row change (old → new):** status `queued` (freeze `4a2d34f2`) → `mined`; used-by `—` → `corpus/practice/curl-h1-1913733/report.md`.

### S120 — curl advisory CVE-2023-28319 (admitted)

- **URL:** https://curl.se/docs/CVE-2023-28319.html, HTTP 200.
- **Accessed:** 2026-11-07.
- **Capture:** `corpus/source-snapshots/round-85/S120.txt`, sha256 `65d6b230ad58e86517b1b0faddd800d6bcb111ed05e21e22752246f4b0913690`.
- **Located quote, S120.txt:81:** "Bug bounty: 2400 USD". Also pinned: :80 "Severity: Medium" and :83 the original-report link.
- **Row change (old → new):** status `queued` → `mined`; used-by `—` → `corpus/practice/curl-h1-1913733/report.md`.

### S121 — curl vulnerability-disclosure policy (admitted)

- **URL:** https://curl.se/dev/vuln-disclosure.html, HTTP 200. It was requested as `/docs/bugbounty.html`, which answers 301 to this URL.
- **Accessed:** 2026-11-07.
- **Capture:** `corpus/source-snapshots/round-85/S121.txt`, sha256 `9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102`.
- **Located quote, S121.txt:43:** "There is no bug bounty and the curl project never offers rewards for reported vulnerabilities." Also pinned: :95 the CVSS refusal and :103 the Medium rung of the four-level ladder.
- **Row change (old → new):** status `queued` → `mined`; used-by `—` → `corpus/practice/curl-h1-1913733/report.md`.

Registry: 118 → 121. No other row's status, recheck or used-by cell changed.

**Independent re-open.** ScoutSources re-fetched all three pages live and found all 12 manifest quotes, once each, on their anchor lines (`w1/ScoutSources.md` §1). ProbeKEV checked the CVE against KEV:

- The S052 capture (catalogVersion 2026.10.23) has 0 hits for CVE-2023-28319.
- The live feed (catalogVersion 2026.11.06, 1769 entries) also has 0 hits.
- Verdict HOLDS (`w1/ProbeKEV.md`).

**The pricing lesson.** The three records answer different questions, so they are not netted into one price:

- S119 `has_bounty?` false is the platform team's flag.
- S121 "no bug bounty" is the vendor's policy today.
- S120 "Bug bounty: 2400 USD" is the vendor's 2023 record.

ScoutSources lead (a) found who paid: HackerOne IBB report 1997312. Lead (b) found the end of curl's paid bounty: 2026-01-31, announced on daniel.haxx.se on 2026-01-26. Both stay leads and are not registered this round.

### Rejected or deferred this round

- **Deferred (not rejected):** IBB report https://hackerone.com/reports/1997312.json and the post https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/.
  - They were opened by ScoutSources with HTTP 200 (§2–3).
  - Reason: no claim this round rests on them, and CORPUS rule 4 says no row without an entry that uses it.
  - Flip condition: a round-86 package field cites the payer or the bounty end date.
- **Rejected as package evidence:** the CVSS figures third parties published for this CVE (NVD/MITRE records, ScoutSources §5).
  - Reason: S121:95 says the vendor sets no CVSS. A third-party score would price the finding on a ladder the program refuses.
  - Flip condition: a program whose own policy prices by CVSS.

### considerthese and assimilation

- **considerthese:** `considerthese/2026-10-26.md` proposal 2's open half, one end-to-end task, is adopted as C2. The lane holds no other unimplemented proposal it owns (`w1/ConnectorOverlap.md` §2).
- **Assimilation: none.** The staged-id collision check gives lane 121 ids, staged 94 ids and 91 collisions. The guard was proven on an indented scratch row, where it finds 2 collisions (`w1/ConnectorOverlap.md` §3 and `w1/ConnectorOverlap-receipts/assimilation/`). The r77 L0 question is still open.

## Mistakes

**M85-1 — class `gate-not-run-after-edit`.**

- **What happened:** Round 84 corrected the SHONEN evidence pointers (CriticTrend 1–2). The box-1 pointer it wrote, `corpus/lessons/round-47-verifier-spotcheck.md:94 (…)`, is not in the canonical pointer form. The lane's own registered gate `corpus/instruments/shonen-form.py` went from `canonical=1 SF-CLEAN` at `a089ff3d` to `canonical=0 finding=SF-POINTER exit=1` at `c91c944f`. It stayed broken through `bc722e54`. Nobody ran the gate (`.ufo/waves/round-85/l1/r136-check-r85.txt`).
- **Captured-by:** none. The gate existed, but no rule required running it when SHONEN.md changes.
- **Fix:** QUALITY R136. This round restores the canonical form for box 1, and the gate prints `exit=0` on the landing.
- **Shown able to fail:** the same check prints `exit=1` on the r84 bytes.

**M85-2 — class `counter-binds-fields-not-subject`.**

- **What happened:** The frozen C2 counter `e2e-check.py` passes a wrong-subject package. CriticClaims B3 took the r43 CVE-2025-9086 exemplar, added S119/S120 copies and a correct 1913733 pricing block, and got `E2E-RESULT pass rc=0` (`w1/CriticClaims-receipts/`).
- **Further gaps found:**
  - E4 accepts empty or one-letter quotes; E3 is first-wins on duplicate keys (ReviewC2Package R-01/R-02, CriticClaims B4/B5).
  - MutC2Counter: 6 of 20 mutants killed, 13 survived, 1 equivalent.
  - MutC1Counter: the frozen controls kill 4 of 20 mutants of the C1 counter. The limbs overlap, so the conjunction still rejects every control, but no single limb is self-protecting.
- **Captured-by:** none. R134 covers lexical limbs that score entry rule text, not subject binding.
- **Fix:** not yet a fix, so it is routed. The round-86 counter adds subject binding (the body names the CVE and report URL in `price-cve`), a minimum quote length, duplicate-key rejection and one Pricing section. It also carries the named-limb assertions C8–C10 from MutC1Counter.
- **How this round compensates:** C2's subject evidence is ReviewC2Package's independent read of the package, not E1–E5.

**M85-3 — class `census-root-dependence`.**

- **What happened:** resolve.py over a `git archive` extract gives SKILL 157/741. Over a checkout it gives 158/741, because the SKILL token `.git` exists only in a checkout (`.ufo/waves/round-85/controls/census-of-record-base-r85.txt` against `controls/c1-controls-r85.txt`).
- **Captured-by:** none.
- **Fix:** the claim pins a checkout with `.git`, and the landing receipt measures over a `git clone --shared` of the landing commit (`l1/landing-r85.sh`).
- **Shown able to fail:** the extract run gives 157, the clone run gives 158.

## Routed-defect disposition (r84 spot-check, defects 1–6)

| # | r84 routed defect | r85 disposition |
|---|---|---|
| 1 | D-b: B8 not measured over the extract | Carried; no entry gate runs this round. The r85 landing receipt measures over a clone of the landing commit. |
| 2 | D-a: control named by a path that was never committed | Answered: `claims.json` names every control by its committed path. |
| 3 | depth:verifiability nominal since r70 | Answered: C1 moves the resolve.py SKILL meter, 158/741 → 167/732. The qualifier is "internal-citation repoint". |
| 4 | Carried C1 limits (MutC1Hunt 22, MutCounter 5, A1, exit 1/2) | Carried; that instrument was not touched this round. |
| 5 | Per-row MUTANT lines not committed | Not applicable to r85; the r85 counters print every limb line into committed receipts. |
| 6 | SHONEN box 2 still `[ ]` | Answered: box 2 is `[~]` with the package pointer, and non-author verification is pending. |

## Routed to round 86

- **Census of record:** `corpus/instruments/citation-survival.md` still states 132/701, which is r57-era. The full resolve.py rerun on the C1 landing gives 167/732 (`l1/census-of-record-c1-r85.txt`). The census is not regenerated this round, because `figure-audit-ledger.json` pins r56 census figures and a regeneration must move them in the same round (CriticClaims D1).
- **ExecC1Hunt:** 31 more SKILL tokens across 19 distinct files are candidates (`w1/ExecC1Hunt-r86-candidates.json`).
- **e2e counter amendment:** see M85-2.
- **Leads:** IBB 1997312 (who paid) and the 2026-01-26 end-of-bounty post.
