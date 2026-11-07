# Round 85 — lesson (kasegi, attempt 1)

> DRAFT — not landed. The L1 owns every `<L1>` slot and lands the final text as
> `corpus/lessons/round-85.md`, the `## Round 85` LOG entry and the three
> `corpus/SOURCES.md` `## Registry changes` bullets. Nothing here was measured on
> a landing commit; the frozen control values below were read from the freeze
> receipts named in each pointer.

Read first: the r84 closure (`.ufo/reports/round-84/kasegi.md`), the r84 verifier spot-check
`corpus/lessons/round-84-verifier-spotcheck.md` (routed defects 1–6, whose item 3 requires a
`resolve.py`-read move or a recorded retire/split of depth:verifiability) and
`corpus/lessons/round-84.md`. Freeze `4a2d34f203519a87078f21a896dc8679137ff675` (base
`bc722e540c93b48ff159454b65a0f9f4630db1ed`); frozen claims, predicates, kill rules and executed
controls in `.ufo/waves/round-85/claims.json` and `.ufo/waves/round-85/controls/`. One v1 wave `w1`
of 12 seats; reports under `.ufo/waves/round-85/w1/`.

## Claims

- **C1 — depth:verifiability (lowest non-retired, 4; the claim reads the scored meter itself).**
  Repoint the 18 bare SKILL.md citations listed in `.ufo/waves/round-85/c1/repair-map.json` — each a
  basename that `corpus/instruments/resolve.py` classifies GONE on this host and that names exactly
  one tracked lane file outside `.ufo/` — to their full lane paths, so the resolve.py SKILL.md scope
  moves from **158/741 (21.32 %) to exactly 167/732 (22.81 %)** with no other SKILL.md citation
  added, removed or changed. Frozen limbs: M1 meter, M2 token set, M3 line diff, M4 binding, M5 map
  sha256 (`b575f147…b5ae1944`). The integer axis score is **not** claimed to move; the meter is.
  Candidate already generated: `.ufo/waves/round-85/w1/ExecC1Apply-SKILL.md` (1251 lines, same as
  base; sha256 `7d082bfec14257351b39c145ea0db26cafbce3d6f263009c3eb1d0893c373552`), 10 hunks, 18
  tokens replaced, M2 `stray_removed=0 stray_added=0`, density 273.2 → 273.2
  (`w1/ExecC1Apply.md` §2–§6).
- **C2 — coverage (8 held; the coverage denominator is operator-owned).** Build the six-file claim
  package `corpus/practice/curl-h1-1913733/` for disclosed HackerOne report 1913733 as a
  **retrospective practice package** (no submission, not claimable), priced from the platform record,
  the vendor advisory and the vendor's current policy plus the round-35 KEV capture; pass the r43
  gate and the frozen e2e counter; log it in LOG.md and cite it in SHONEN box 2; move S119–S121
  `queued` → `mined`. Pricing fields re-derived, not asserted: `severity=medium`,
  `reward-at-disclosure=2400 USD`, `platform-bounty-flag=false`, `reward-current-policy=none`,
  `cvss=not-set-by-vendor`, `kev=not-listed`, `cve=CVE-2023-28319` (derivation read from
  `.ufo/waves/round-85/c2/e2e-check.py:67-81`; the KEV capture holds 0 occurrences of the CVE).
  This is the round's sourced claim.

## Gate

### S119 — HackerOne disclosed report 1913733, JSON record (admitted, priced)

- **URL:** https://hackerone.com/reports/1913733.json (HTTP 200; final URL equal to the requested URL).
- **Access date:** 2026-11-07. Capture `corpus/source-snapshots/round-85/S119.txt` (sha256
  `9e4fb52e7e7572482fa29fc268dddbf7e249dd94c6850d2e383241ae14bc6105`, 5001 bytes, 1 line,
  `fetched_utc 2026-11-07T00:26:28Z`); manifest `corpus/source-snapshots/round-85/manifest.json`.
- **Located quote (7 words), S119.txt:1:** `"title":"CVE-2023-28319: UAF in SSH sha256 fingerprint
  check","state":"Closed","substate":"resolved","severity_rating":"medium"`. Also pinned on the same
  line: `"has_bounty?":false` and `"cve_ids":["CVE-2023-28319"]`.
- **Row change, old → new:** status `queued` → `mined`; used-by `—` →
  `corpus/practice/curl-h1-1913733`; every other cell byte-identical. Registry 121 → 121.
- **Pricing note (the reason this source is in the package):** the platform record's
  `has_bounty? false` is **not** "unpaid". The vendor advisory records a 2400 USD bug bounty for the
  same report (S120.txt:81) while the vendor's current policy says it offers none (S121.txt:43). The
  three are separate package fields (`platform-bounty-flag`, `reward-at-disclosure`,
  `reward-current-policy`) and may not be collapsed into one verdict.
- **Independent re-open:** `<L1>` (ScoutSources report, quote/live-byte re-check).

### S120 — Project curl security advisory, CVE-2023-28319 (admitted, priced)

- **URL:** https://curl.se/docs/CVE-2023-28319.html (HTTP 200; final URL equal).
- **Access date:** 2026-11-07. Capture `corpus/source-snapshots/round-85/S120.txt` (sha256
  `65d6b230ad58e86517b1b0faddd800d6bcb111ed05e21e22752246f4b0913690`, 3053 bytes, 101 lines,
  `fetched_utc 2026-11-07T00:26:29Z`).
- **Located quote (4 words), S120.txt:81:** `Bug bounty: 2400 USD`. Class and severity on adjacent
  pinned lines: `CWE-416: Use After Free` (:79), `Severity: Medium` (:80).
- **Row change, old → new:** status `queued` → `mined`; used-by `—` →
  `corpus/practice/curl-h1-1913733`. No other cell changed.
- **Independent re-open:** `<L1>` (ScoutSources).

### S121 — Project curl, Vulnerability Disclosure Policy (admitted, priced)

- **URL:** https://curl.se/dev/vuln-disclosure.html (HTTP 200; final URL equal).
- **Access date:** 2026-11-07. Capture `corpus/source-snapshots/round-85/S121.txt` (sha256
  `9e346a4e579769aa4ac207b9f088e7194fe543efa12a98cd73ea2d262304f102`, 19670 bytes, 221 lines,
  `fetched_utc 2026-11-07T00:26:30Z`).
- **Located quote (15 words), S121.txt:43:** `There is no bug bounty and the curl project never
  offers rewards for reported vulnerabilities.` Also pinned: the CVSS refusal (`We do not support
  CVSS as a method to grade security vulnerabilities`, :95) and the four-level ladder (`Low` :99,
  `Medium` :102, `High` :104, `Critical` :106).
- **Row change, old → new:** status `queued` → `mined`; used-by `—` →
  `corpus/practice/curl-h1-1913733`. No other cell changed.
- **Independent re-open:** `<L1>` (ScoutSources).

### Reused input (no row change)

- `corpus/source-snapshots/round-35/S052.txt` (CISA KEV, sha256
  `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`) is read only for the `kev`
  derivation: 0 occurrences of `CVE-2023-28319` → `not-listed`. S052's row is unchanged.

### Rejected / deferred this round

- `<L1>` — ScoutSources / ProbeKEV leads (quote must sit on one snapshot line; flip condition
  named).
- `<L1>` — deferred lead and the registry id it would take (registry stays 121 this round).
- `<L1>` — observation that is not a source (any live probe recorded in Limits only).

### considerthese and assimilation

- **considerthese:** `considerthese/2026-10-26.md` proposal 2 ("Run one end-to-end domain task
  round", § Self-improvement suggestions) is **adopted as C2**; it was carried into r85 by the r84
  connector (`w1/ConnectorOverlap.md` §3 in `.ufo/waves/round-84/`). SHONEN box 2 moves from `[ ]`
  to `[~]` at landing — never `[x]`, because no non-author verifier has checked the package.
- **Assimilation:** `<L1>` (pending L0). Receipts in
  `w1/ConnectorOverlap-receipts/assimilation/` show 91 staged-id collisions S031–S121 with guard
  collisions S001 and S052; the L0 question stays open.

## Mistakes

**M85-1 — class `census-root-dependence`.** The resolve.py census of record is read over a **git
checkout**, but the same bytes extracted with `git archive` read one citation lower: SKILL.md
**157/741** over the extract vs **158/741** over the worktree. The difference is one path-like token,
`.git`, cited at `SKILL.md:464` (`` `~/Projects/the-bounty-hunter` (excluding `.git`) ``): it
resolves against a checkout's `.git` directory and cannot resolve in an archive extract, which has
no `.git` (`git archive bc722e5 | tar -t | grep -c '^\.git/'` = 0). Receipt:
`w1/ScribeLesson-receipts/m85-check.txt` §M85-1; frozen base rerun header
`controls/census-of-record-base-r85.txt:1` ("extract has no .git … worktree root gives 158/741") vs
the frozen worktree control `controls/c1-controls-r85.txt:2` (`rate=158/741`). The same split was
reproduced independently on the candidate: `base=157/741 after=166/732`, M1 and M4 fail over the
extract (`w1/ExecC1Apply.md` §4). C1 already scopes P1 to the checkout (`claims.json` C1
`host_note`), so this is not a claim defect; it is a *reading* defect: a census receipt that prints
158/741 for an extract is wrong, and one that prints 157/741 for a checkout is wrong.
**Captured-by:** the base census rerun (`census-of-record-base-r85.txt`) against the frozen control.
**Fix:** every census receipt names its root class (`checkout` vs `archive-extract`) beside the rate;
`corpus/instruments/citation-survival.md` and the resolve.py docstring say that VCS-internal tokens
are checkout artifacts, not lane citations. Route `<L1>`.
**Check that can fail:**
`python3 -B .ufo/waves/round-85/c1/skill-meter.py --lane <checkout>` → `rate=158/741`;
`--lane <git-archive extract>` → `rate=157/741`. A change that makes both print 158 (e.g. resolve.py
exempting `.git` from the GONE class) fails the check and forces the recorded numbers to be
re-derived, not silently carried.

**M85-2 — class `claim-names-a-control-path-never-committed`.** The r84 freeze's `claims.json`
named `c1-candidate-r84.raw`; the committed file is `controls/c1-candidate-r84.txt` and no `.raw`
exists at either the freeze or the r84 landing
(`corpus/lessons/round-84-verifier-spotcheck.md:27` and `:97`). Re-measured read-only at
`7f76b7eb`: `git cat-file -e 7f76b7eb:.ufo/waves/round-84/controls/c1-candidate-r84.raw` → rc 128,
while `.txt` → rc 0; `7f76b7eb:.ufo/waves/round-84/claims.json` prints `c1-candidate-r84.raw`
(`w1/ScribeLesson-receipts/m85-check.txt` §M85-2 targeted). The same check on the r85 freeze
(`4a2d34f2`, controls as an explicit six-path list) names 6 and misses 0.
**Captured-by:** the r84 non-author spot-check (D-a).
**Fix:** a pre-freeze control-path check: extract every `controls/...` token from `claims.json`
(list entries verbatim; prose blocks by token regex `controls/[^ ;),]+`) and require
`git cat-file -e <freeze>:<path>`. Commit its receipt with the freeze. **Check that can fail:** on
r84's freeze the `.raw` token must fail; on r85's freeze all six must pass. A claims.json that
renames a control without committing the path fails before the claim is scored.

## Routed-defect disposition (r84 spot-check, defects 1–6)

| # | r84 routed defect | r85 disposition | pointer |
|---|---|---|---|
| 1 | D-b: C2 entry gate not runnable over a `git archive` extract | `<L1>` — whether the frozen C2 counter's E1 was measured over the landing extract or a checkout, stated as such | `claims.json` C2 P1; `<L1>` landing receipt |
| 2 | D-a: control named by an uncommitted path | answered in form by M85-2's check (candidate; landing decision `<L1>`) | M85-2 |
| 3 | depth:verifiability nominal since r70 — r85 must deliver a resolve.py-read move | answered by C1: the claim reads the scored meter's own SKILL.md scope and moves 158/741 → 167/732 (landing confirmation `<L1>`) | C1; `controls/c1-controls-r85.txt` |
| 4 | Carried C1 limits (MutC1Hunt survivors, MutCounter semantic survivors, F12 forgery class, ExecC1RealTree exit code) | attacked this round; findings `<L1>` | `w1/MutC1Counter.md`, `w1/CriticClaims.md` |
| 5 | P3 per-row MUTANT lines absent from the landing receipt | `<L1>` | `<L1>` landing receipt |
| 6 | SHONEN box 2 unset | answered by C2: box 2 `[~]`, evidence line names `corpus/practice/curl-h1-1913733`; never `[x]` | C2 P6 |

## Routed to round 86

- `<L1>` — from MutC1Counter / MutC2Counter / CriticClaims / ReviewC1Semantics / ReviewC2Package.
- `<L1>` — ScoutSources / ProbeKEV leads with their flip conditions.
- `<L1>` — QUALITY rule id (`R<L1>`) for M85-1/M85-2 and the check that shows it fails on the defect.

## Landing values

`<L1>` — every landing predicate value goes in the landing receipt the L1 commits
(`.ufo/waves/round-85/l1/…`), measured over the landing commit; C1's meter must be read in the
`.git` checkout (see M85-1), and the extract reading is disclosed beside it, not substituted.

---

# LOG.md draft — `## Round 85` entry

> L1: replace `<L1>` and land under the existing round headings, matching r83/r84 bullet style.

## Round 85 — C1 `<L1>`, C2 `<L1>`

- Read first: the r84 closure and `corpus/lessons/round-84-verifier-spotcheck.md` (routed defects
  1–6; item 3 requires a `resolve.py`-read move or a recorded retire/split). C1 is
  depth:verifiability, the lowest axis: the claim reads the scored meter itself, repointing 18 bare
  SKILL.md citations from the frozen repair map so the resolve.py SKILL.md scope moves **158/741 →
  167/732** (M1–M5). C2 is coverage: one end-to-end priced claim package,
  `corpus/practice/curl-h1-1913733/`, for disclosed HackerOne report 1913733 (curl
  CVE-2023-28319) on S119–S121, a retrospective practice package (no submission, not claimable).
- Controls executed and committed before scoring (freeze `4a2d34f2`), `.ufo/waves/round-85/controls/`:
  - C1 (`c1-controls-r85.txt`): do-nothing 158/741 fails; pad-with-resolving-cites 168/751, de-cite
    158/723, wrong-target 168/733 and partial 9/18 164/738 each fail; the frozen map's positive
    control gives 167/732 rc 0.
  - C2 (`c2-controls-r85.txt`): package absent (E1–E5 fail); r43 exemplar copied (E1 pass, E2/E3/E4/E5
    fail); positive pricing rc 0; the seven pricing forgeries (severity, reward-at-disclosure,
    platform flag, current policy, CVSS, KEV, CVE) and the forged quote each fail E3 or E4.
- Wave `w1`: one v1 wave of 12 seats (executor×3, reviewer×2, mutation-tester×2, critic×1, scout×2,
  scribe×1, connector×1); attack seats `<L1>`, dead seats `<L1>`; reports under
  `.ufo/waves/round-85/w1/`.
- C1 landing `<L1>`: P1–P4 hold over the landing commit (`<L1>` receipt). The meter is read in the
  `.git` checkout; over a `git archive` extract the same bytes read 157/741 → 166/732 (M1/M4 fail),
  disclosed as the census-root dependence M85-1 rather than substituted for the reading.
- C2 landing `<L1>`: P1–P6 hold (`<L1>` receipt); pricing at landing `severity=medium`,
  `reward-at-disclosure=2400 USD`, `platform-bounty-flag=false`, `reward-current-policy=none`,
  `cvss=not-set-by-vendor`, `kev=not-listed`, `cve=CVE-2023-28319`; SHONEN box 2 `[~]` with the
  package path in its evidence line.
- S119, S120 and S121 `queued` → `mined`, used-by → `corpus/practice/curl-h1-1913733`; registry stays
  121 (three Registry-changes bullets landed in `corpus/SOURCES.md`).
- Mistakes mined: M85-1 (`census-root-dependence`: 157/741 over an extract vs 158/741 over a
  checkout, one `.git` token) and M85-2 (`claim-names-a-control-path-never-committed`, from the r84
  spot-check D-a), in `corpus/lessons/round-85.md`; QUALITY `R<L1>`.
- Measured scores: depth:verifiability `<L1>` → `<L1>` (meter 158/741 → 167/732; the integer is
  `<L1>`); coverage `<L1>` → `<L1>` (held pending the operator denominator).
- Assimilation: `<L1>` (L0 pending). considerthese: proposal 2 adopted as C2 (one end-to-end domain
  task, SHONEN box 2).

---

# corpus/SOURCES.md draft — `## Registry changes` (three bullets, append only)

> L1: append under the existing `## Registry changes` list; the three rows already exist at the
> freeze, so these are cell changes, not row additions.

- S119 row status/used-by cells old → new: `queued` / `—` → `mined` /
  `corpus/practice/curl-h1-1913733` (R85 C2: the end-to-end priced package reads the platform
  record for severity, the `has_bounty?` flag and the CVE id; `has_bounty? false` is not read as
  unpaid). Every other S119 cell byte-identical; registry 121 → 121.
- S120 row status/used-by cells old → new: `queued` / `—` → `mined` /
  `corpus/practice/curl-h1-1913733` (R85 C2: the advisory supplies `Severity: Medium` at
  S120.txt:80 and the recorded `Bug bounty: 2400 USD` at :81, the `reward-at-disclosure` value).
  Every other S120 cell byte-identical.
- S121 row status/used-by cells old → new: `queued` / `—` → `mined` /
  `corpus/practice/curl-h1-1913733` (R85 C2: the policy supplies `reward-current-policy=none` from
  :43 and `cvss=not-set-by-vendor` from :95, and the four-level ladder at :99–:107). Every other
  S121 cell byte-identical; no other row's status, recheck or used-by cell changed this round.
