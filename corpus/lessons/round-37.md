
# Round 37 — kasegi

Lane: `kasegi-shokunin`. This lesson reports working-tree and receipt evidence, not a canonical
judge decision. Revisions: base `b56a41680cefd391868c1c370dc063c69d827e7d`; claims-freeze commit
`224df74db2a46d627ae1475a72ca48796bbd177c`; claims-erratum 1
`b362068195d5489aa94b31e6ec8f880c367e0ba0` (S054 capture URL corrected from the docs home page to the
SSVC overview tutorial, filed before any seat scored); r36 lane head
`c20300df516eb5575d8db2aaad1f0cf4913e7981` — cited here as the **anchor ancestor** of this round, not
as any round's final commit; round-37 final lane commit `⟨pending: L1 closure commit — a commit cannot
carry its own hash⟩`.

Shape: **one v2 wave**, `kasegi-r37-build`, **64 seats** — executor 18, scribe 12, reviewer 10,
critic 6, scout 6, mutation-tester 5, connector 3, sentinel 2, simplifier 2; adversarial seats
(reviewer + critic + mutation-tester + sentinel) 23/64 = 35.9 %. `.ufo/waves/round-37/wave1-dispatch.json`:
`schema=ufo-swarm-wave-dispatch-v1`, `counts={spawn: 64, resume: 0, total: 64}`,
`policy.maxLanes=128`; `wave1-spec.json` carries 64 `items`; `wave1.ready` names `l1: KasegiR37`.
Route: L1 inline spawn handoff, hyaku run 9. Axes owned: `depth:density`, `depth:verifiability`,
`coverage`; saturation line 9/10 per axis, window N=3; lowest non-retired axis
`depth:verifiability (4)`.

Receipt coverage at this seat's last read (2026-10-26T17:19Z): **50 of 64** spec names had filed a receipt under
`.ufo/waves/round-37/wave1/`; the seats this lesson still names as pending are listed in its receipt
(§ Pending). Every after-value below is either a receipt's own measured output quoted with its
digest/exit, or a read-only measurement by this seat over base bytes; anything else is named pending
with the seat that owns it.

## Frozen claims — before → after

| Claim | Axis | Before (frozen control at base) | After (frozen claim's declared state) |
|---|---|---|---|
| **C1** | depth:verifiability (4, held) | `corpus/instruments/r37-closure.sh` absent (`suite_missing=1`, `ls` exit 2); no `.ufo/waves/round-37/final-gates/all-gates.txt` (D1 open); `git ls-tree -r --name-only b56a4168 \| grep -c r36-fixtures` → `0` (D2 open); `SCORECARD.md` labels `Final lane commit: e666d902` (D4 open); `SKILL.md` row `r36-closure.sh` type cell `gate\|probe`, no exit-2 verdict (D5 open); `r36-closure.sh` carries `porcelain:-0` (D6 open); the structural-placeholder grep on `SCORECARD.md` → `0`, the angle-bracket lane-hash marker grep → `0`; `git status --porcelain` → `0`; scratch seat dirs `0` (`.ufo/waves/round-37/c1-controls/before.txt`) | suite present; `--export-ref` at the round-37 final head → `closed=14/14 exit=0`; `--selftest` → `cases=14 failures=0`; r36 base `cc692008` → `closed<14/14 exit=1`; r36 judged head `a23dc478` → `closed<14/14 exit=1`; E10 commits `all-gates.txt` with `suite-sha256=` header, 14 E-numbered payload lines, `closed=14/14 exit=0`, 14 `selftest case=` lines, `cases=14 failures=0`; D1–D6 closed |
| **C2** | coverage (7, held) | frontier 19; registry 53; `S054` rows 0; entries citing `source: S054` 0; knowledge 48; harness `entries=22 pass=22 exit=0`; `recheck-audit --quiet` `expected=48 … unexpected=0 exit=0`; `capture-binding-check` `records=43 bound=43 unbound=0`; census exit 0 (W04 S028/S029 only); `c2-controls/junk-f20.md` absent (`.ufo/waves/round-37/c2-controls/before.txt`, `census-before.txt`) | frontier 20 (F20 row); registry 54 (`S054`, tier A, mined, opened 2026-10-26); one entry cites `source: S054`; knowledge 49; harness `entries=23 pass=23 exit=0` incl. `PASS F20 … ids=S054`; `source-recheck S054` exit 0; `recheck-audit` `expected=49 … unexpected=0 exit=0`; capture `corpus/source-snapshots/round-37/S054.txt` + `manifest.json` committed and bound; junk twin rejected |
| depth:density | 9 | `SKILL.md` base lines byte-identical; `PROVINCE.md` unchanged | no move claimed; any `SKILL.md` change is the EOF-appended r37 registry block, existing rows byte-identical |

## Gate

### Admitted — F20 / S054 (SSVC overview tutorial, CERT/CC)

- **Row:** `corpus/SOURCES.md`, inserted immediately after the `| S053 |` row (base `:59`), so it becomes
  line 60 inside `## Registry` — `S054`, kind `docs`, tier `A`, status `mined`, recheck `90d`,
  `opened 2026-10-26`, `used-by
  corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`; `NF=13` / 11 cells, no
  cell carries a `|`; the source cell holds exactly one `https://` token equal to the manifest `url`
  (row draft `wave1/ScribeRowS054.md` §1–§3, row sha256 `ea4f1676…`; landing is the integrator's write).
- **URL:** `https://certcc.github.io/SSVC/tutorials/ssvc_overview/` — the claims-erratum-1 corrected
  literal (`claims.json` still prints the docs home page; the erratum is the operative one). Requested
  URL == effective URL, HTTP 200, `text/html; charset=utf-8`, 0 redirects, 143,053 served bytes →
  32,623 normalized bytes, 518 lines, sha256
  `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21`; raw-body sha256
  `9dba9f75…faec3f`; a conditional GET at `17:03:49Z` returned `304` with the same ETag
  (`wave1/ExecC2Capture.md` §1).
- **Access date:** `2026-10-26`; `fetched_utc` `2026-10-26T17:02:19Z` (strict UTC, equal to the served
  `Date` second).
- **Quotes (manifest pins, each ≤25 words, located, `occurrences=1`, `anchor=N-ok`):**
  - Q1 — 12 words, `S054.txt:259`: `SSVC categorizes vulnerabilities by priority based on risk that
    varies among stakeholders.` (definition)
  - Q2 — 14 words, `S054.txt:277`: `All decision points and decision outcomes (priority categories)
    must be explainable to the non-expert.` (decision-point/outcome rule)
  - Q3 — 17 words, `S054.txt:473`: `Unlike other vulnerability scoring systems, SSVC evaluates risk to
    a particular stakeholder without imposing a one-size-fits-all approach.` (distinctness)
  - Q4 — 5 words, `S054.txt:68`: `CISA BOD 26-04 Response Model` — **navigation entry only**: no body
    sentence about BOD 26-04 exists on this page, so the pin is recorded as a navigation-only mention
    and any BOD 26-04 prose must cite the dedicated page (`wave1/ExecC2Capture.md` §5).
- **Second pin set, also verified — recorded because two seats pinned different sentences.** A
  four-quote set (L247 22 words; L259 12 words; L277 25 words, carrying the page's own typo
  `decisions point values`; L367 19 words) passes `source-recheck` against its own scratch manifest
  with `occurrences=1` and anchors `247/259/277/367-ok` (`wave1/ExecC2QuoteOnce.md` §2,
  independently reproduced by `wave1/RevEntryF20.md` §1). Only the landed manifest is bound by
  `capture-binding-check`, so a grader reads the manifest's Q1–Q4; the entry may quote either set
  **only because both are true in the same 518-line capture bytes** — the entry's own quotes are not
  what `source-recheck` checks, which is a limit worth stating. The divergence is live, not academic:
  the drafted entry (`wave1/ScribeEntryF20.md` §2, `recheck:` comment) and the drafted frontier block
  (`wave1/ScribeFrontierAmendments.md` §1) both cite the second set, and the entry's comment asserts
  the recheck "prints … anchor=247-ok through … anchor=367-ok", which the landed manifest does not
  print. Landing must reconcile the comment with the manifest (or change the manifest) — the
  frozen C2 predicate names no quote set, so neither draft is authoritative over the other.
- **Bounds the capture imposes, recorded rather than smoothed:** `severity` and `exploitability` occur
  once each, in the L247 contrast sentence (41 words, over the pin budget); `CVSS` (6), `EPSS` (5) and
  `KEV` (1) occurrences are site navigation only; `Carnegie`/`Mellon` occur only in the footer
  copyright; `FIRST` occurs 0 times. The entry must source any CVSS/KEV/EPSS *definition* from
  S001/S002, S052 and S053, never from S054 (`wave1/ExecC2QuoteOnce.md` §5,
  `wave1/RevEntryF20.md` §2).
- **Entry draft and review:** the entry is drafted at 84 lines with `source: S054`, `verified-at:
  2026-10-26` and an executable `recheck:` line (`wave1/ScribeEntryF20.md` §2) but is **not landed**.
  The plan review passes Q1–Q6 with one open pitfall — the planned *example falsifiable rule* is not
  checkable against the pinned capture and needs a capture-grounded replacement
  (`wave1/RevEntryF20.md` §2 Q5, §4) — and the header's `recheck:` comment carries the pin-set
  mismatch recorded above. Landing (entry + certificate) is the integrator's write
  `⟨pending: entry file at the integrated head⟩`.
- **Recheck:** `python3 corpus/instruments/source-recheck.py --manifest
  corpus/source-snapshots/round-37/manifest.json --source S054` → `S054:sha256 OK`, Q1–Q4 each
  `OK occurrences=1 anchor=N-ok`, exit 0. On a scratch copy of the same bytes the capture seat
  observed exactly those lines; at the committed path this run is
  `⟨pending: ExecC2Harness / final-gates transcript at the integrated head⟩`.
- **Harness reading, with its measured caveat:** `frontier-recheck-count.py` needs no code change; on
  the base export it prints `entries=22 pass=22 exit=0` (`--selftest cases=6 failures=0`), and on a
  mirror carrying the planned data additions it prints `entries=23 pass=23 exit=0` with
  `PASS F20 knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md ids=S054 exit=0`
  (`wave1/ExecC2Harness.md` §2–§6). The counter is a **live-lane measurement, not an export
  measurement**: every row's `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` prefix makes
  `bash -c` re-check the lane even when the harness runs with its working directory inside the export —
  proven by corrupting only the export's S053 pin and watching F19 still `PASS`. So `entries=23 pass=23` must be produced
  after the F20 files are committed, and cannot be re-derived from an export alone.

### Rejected

- **`c2-controls/junk-f20.md` — the negative twin (fabricated SSVC claims).** Four invented sentences
  (a fixed remediation deadline; "replaces CVSS severity scoring"; "maintained by FIRST"; a 0–1
  exploitability score) each occur **0** times in both candidate captures, and `source-recheck.py`
  prints `MISMATCH reason=quote-not-found` per claim with `exit=1`. The rejection is
  **content-specific**: the same manifest ids/paths/sha with genuine sentences is `OK occurrences=1`
  ×4 `exit=0`; a one-word paraphrase of a true sentence (`stakeholder` → `organization`) is red;
  stitched genuine fragments are red; a fabricated claim carrying a valid anchor is red; `--source
  S055` gives `UNAVAILABLE reason=not-listed exit=2`; the twin reds against the home-page capture too.
  Component evidence: `wave1/ExecC2JunkControl.md` §2–§4 (twin body 991 bytes, sha256
  `22ec0dd9…cbb945`, delivered as content and landed by the integrator).
- **Standing refusals — seven staged package entries, no flip cleared.** Reasons and flip conditions
  are unchanged from the round-35 lesson (`corpus/lessons/round-35.md:155-169`):

  | staged entry | reason it stays refused | flip condition (still unmet) |
  |---|---|---|
  | `program-scope-rules-and-asset-boundaries.md` | 0 located quotes, no executable recheck, `ground: F09` collides with admitted lane F09 | a located quote + executable recheck + a non-colliding frontier id |
  | `claim-packaging-and-report-quality.md` | body cites S036 (BILISRC V1.7) in no lane row and no capture | an S036 row + capture |
  | `cn-crowdsourced-testing-roles-and-conduct.md` | H1 count 0; S081/S082 in no row/capture | an entry shape + the two rows |
  | `chinese-crowd-testing-national-standard-2026-10-23.md` | S077/S078/S079 unregistered; `ground: F24` is not a lane F-id | three rows + a real frontier id |
  | `chinese-criminal-thresholds-and-authorisation.md` | three PRC legal sources in no row/capture; staged ids collide with different lane rows | three rows + a renumber map |
  | `chinese-program-severity-instrument.md` | S047 (sse.com.cn) unregistered; anchor `newsType_6` → 0 in `round-32/S049.txt` | the row + a locatable anchor |
  | `program-severity-ladders-and-reward-scales.md` | same-name lane file differs (`6c05c98f…` vs `35de5f8b…`); S036 half unregistered | byte-identity or a supersedes row |

  Round-37 re-measurement (`wave1/ScoutStandingRefusals.md` §1–§2): package byte-identical to rounds
  35/36 (70 files, all mtime `2026-10-24 23:33:20 -0300`; `SOURCES.append.md` `4fe049cb…73eb`;
  0 files newer than `claims.json`), same reasons, **0 of 7 flip conditions triggered**. The
  `program-severity-ladders…` pair is still unequal (`6c05c98f…` lane vs `35de5f8b…` staged), and
  `newsType_6` is still absent from `round-32/S049.txt` (`newsType_21` → 1). No package ground exists
  for F18/F19/F20 (`ssvc|certcc|stakeholder-specific` → 0 files).
- **Quarantine slice — 7 kasegi rows, 0 adopted; the measured verdicts differ from the frozen
  wording.** From the read-only register
  `shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (rows 99, 100, 322–326),
  re-checked row by row on 2026-10-26 (`wave1/ScoutQuarantine.md` §1–§2):

  | id (staged) | register class | round-37 verdict | basis |
  |---|---|---|---|
  | S037 | `payload-absent` | **present-and-located, quote defective (stitched)** | page 200; title/status/dates present in separate cells; the contiguous quote with invented colons exists nowhere |
  | S054 | `payload-absent` | **present-and-located, quote defective (elided)** | IPA PDF 200; phrase present at １．（ア） with a parenthetical definition dropped from the quote |
  | S048 | unreachable | **unreachable as cited** (HTTP 404, deterministic; sibling ids return 200) | the claim is corroborated in S069 foreword d) and S070, not at the cited locator |
  | S065 | unreachable | **present-and-located** | 7.4 MB PDF 200; quote crosses a page break with the footer digit inside it |
  | S068 | unreachable | **present-and-located** | cited URL 403s to a browser UA; a later hop to `sec.cloudapps.cisco.com` serves the sentence verbatim |
  | S069 | unreachable | **present-and-located** | draft standard 200 with referer + `-k`; quote at §6.3.2, PDF p.25 |
  | S070 | unreachable | **present-and-located** | drafting note 200; quote at 1.2 制定背景, p.1 |

  **Divergence from the frozen claim text, recorded rather than smoothed.** The frozen non-claim
  wording reads "S037/S054 payload-absent; 5 unreachable prose-class"; the measured slice finds
  **0 fabrication-class, 1 unreachable (S048) and 6 present-and-located**, two of them with
  quote-form defects that must be corrected before any adoption. The register's class column is a
  candidate list, not a verdict (its own header says so), and the census-time failures behind the
  five "unreachable" rows were access problems (browser-UA block, referer + TLS leniency, a 7.4 MB
  PDF), not absent payloads. Nothing was adopted either way — adoption is the integrator's act, and
  these are package documents with no lane row.
  **Namespace warning, recorded because the id strings collide:** the quarantine **S054 is the
  staged IPA request PDF** (`shokuknow/merge/kasegi/SOURCES.append.md:30`), not the round-37 SSVC
  source; the quarantine **S037 is the GB/T 30279-2020 catalogue record**, while lane S037 is the
  Cybozu bug-bounty FAQ. The quarantine verdicts say nothing about the lane rows that share the
  numbers.

### Contested scope — none; adjacency is dense

`wave1/ExecSiblingSweep.md` sweeps the 20 sibling lanes (kasegi excluded) for `SSVC`,
`Stakeholder-Specific`, `CERT/CC`, `certcc.github.io`, `CERT Coordination Center`, `Vultron`, `VINCE`
and `vulnerability categoriz` over `corpus/`, `SKILL.md` and `PROVINCE.md`, then re-runs a whole-repo
superset with a strict boundary that does not match `JPCERT/CC`:

- **No sibling lane holds SSVC ground.** All 20 print `CLEAN` on the required surface; the whole-repo
  superset's only genuine payload is **kagi**'s retained round-28 probe
  `.ufo/waves/round-28/retained-probes/SrcCve202010735/nvd-api.json` (4 files) carrying
  `cve.metrics.ssvcV203` — CISA Coordinator, SSVC v2.0.3, `exploitation=none`, `automatable=no`,
  `technicalImpact=partial`. kagi rejected registering that row and never names SSVC; nothing is
  routed for absorption.
- **Ruled, not left silent** (`wave1/ConnSibling.md` Q1): the 20-lane sweep was re-run verbatim by
  the connector seat (20/20 `CLEAN`), the kagi probe payload and its four digests were re-verified,
  and the shokuknow doctrine grep returns **zero** SSVC rows and **zero** `certcc.github.io` matches;
  eight whole-repo false positives were classified as non-SSVC. The ruling is UNCONTESTED, and the
  correction of the capture URL (home → overview, same host and docs site) does not touch scope.
- **The nearest precedent is inside kasegi:** round-24 snapshot S004 is
  `https://certcc.github.io/certcc_disclosure_policy/` (manifest-bound), and SSVC is already named in
  four committed kasegi captures (S001/S003/S004/S008). S054's novelty is **page-level**
  (`…/SSVC/tutorials/ssvc_overview/`), never host-level or concept-level — read the admission as a
  frontier opening over adjacent ground, and the kagi `ssvcV203` payload as an unabsorbed lead, not a
  registry addition.

### Spot-check readiness (what a non-author can re-derive from committed bytes)

1. **Suite over an export, not the worktree.** `bash corpus/instruments/r37-closure.sh --export-ref` a named commit prints one E-numbered payload line per check plus `closed=K/14 exit=E`; a plain run refuses
   with exit 2. The suite exists as a draft only: sha256 `d4f65f0a…69d2`, 1,333 lines / 60,028 bytes,
   `bash -n` exit 0, and at the round-37 base it prints `closed=7/14 exit=1` (E2–E8 green at base; E1
   and E9–E14 open) (`wave1/ExecC1SuiteBuild.md`). Landing requirements from the export-mode seat: the
   digest must come from the **ref's blob** (`git cat-file blob "$REF":… | sha256sum`), the E10 gate
   must recompute it rather than trust the header, and the E9 status read must be rc-checked
   (`wave1/ExecC1ExportMode.md` G1/G2). The required reds are r36 base `cc692008` and r36 judged head
   `a23dc478`; at `a23dc478` the r36 suite prints `closed=8/9 exit=1` (E9 only, `head-match=0`) and
   the r37 E10–E14 stand-in prints `closed=0/5 exit=1` (`wave1/ExecC1BaseFail.md` /
   `ExecC1JudgedHeadFail.md`). The selftest bar is 14 case lines with `mutants=n/n`, `n≥1`, per-mutant
   detail lines naming the reopened limb, and one export positive-limb payload line per id; all three
   forgery shapes (summary-only, fake case lines, forged detail) are rejected
   (`wave1/RevC1Selftest.md` §1–§2). **The draft is not landing-ready as it stands:** the suite review
   demonstrates false-green paths in E1, E10, E12 and E14 (an E10 receipt whose payload lines all say
   `closed=0` but whose summary says `closed=14/14` passes; a stale label in a non-last round-37 block
   escapes E12; a status read split across lines escapes E14's per-line scan) and smaller
   strengthenings for E11/E13, with the required reds measured as r36 base `cc692008` → `closed=4/14
   exit=1` and r36 judged head `a23dc478` → `closed=7/14 exit=1` (E10–E14 all open there)
   (`wave1/RevC1Suite.md` §1, §3).
2. **The positive limb is committed, not asserted.** `.ufo/waves/round-37/final-gates/all-gates.txt`
   must carry the suite-digest header, the fourteen E payload lines, `closed=14/14 exit=0`, fourteen
   `selftest case=` lines and `cases=14 failures=0` — exactly the r36 gap
   (`corpus/lessons/round-36-verifier-spotcheck.md` §5 D1), where the gates file carried only the two
   reds. `⟨pending: wave1/ExecGateReviewPrep.md; file at the integrated head⟩`.
3. **C2 re-derives from the export.** Capture digest and Q1–Q4 pins, the registry row (one `https://`
   token == manifest `url`), `source-recheck S054` exit 0, `recheck-audit` `expected=49
   unexpected=0`, `capture-binding-check` exit 0, and the junk red all read from committed paths. The
   harness number is the exception (§ Gate, live-lane caveat).
4. **The readiness contract itself is committed.** `wave1/RevSpotCheckReadiness.md` enumerates what a
   fresh reviewer re-opens (capture, row, entry, harness, audit, census, the E10 receipt, the D1–D6
   baselines and their line cites) and re-confirms the live before-state; it is the checklist a
   non-author follows, and it also records that a reviewer reading the home-page URL is reading a
   superseded literal.
5. **Census and quiescence at filing.** `git status --porcelain` empty and no
   `/fast/scratch/hyaku/kasegi-r37/*` seat dirs; E9 fail-closed by shape (no `porcelain:-0`; no
   `2>/dev/null` swallowed status read). Measured hazard at probe time: a non-seat `l1prep/` directory
   in the round scratch root would turn E9 red if it survives to the final gate, and the r36 suite's
   *scratch* limb has one fail-open shape the frozen D6 wording does not name
   (`wave1/ExecQuiescenceProbe.md` §3).

## Assimilation: none adopted

Id-collision rerun (this seat, read-only, the guard's own 0–3-space extractor
`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`): lane `corpus/SOURCES.md` → **53** ids;
`shokuknow/merge/kasegi/SOURCES.append.md` → **94** ids (no duplicates on either side); `comm -12` →
**23** collisions: `S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046
S047 S048 S049 S050 S051 S052 S053`. Independently re-derived with the same result by
`wave1/ScoutIdCollisions.md` §2 and `wave1/ScribeAssimilationGate.md` §1 (three seats, identical
lists). Guard proof (`wave1/ScoutIdCollisions.md` §1): an indented-row fixture (`  | S002 |`) yields
`collisions=1`, while the column-zero-only pattern yields `collisions=0` on the same bytes — the
0–3-space tolerance is load-bearing; `round-35/assimilation/collide-check.sh` on the real inputs
prints `reg_ids=53 staged_ids=94 collisions=23`.

Two facts that keep the number honest:

- **The count is head-relative.** 23 at `b362068` (registry 53, no `S054`). Once the round's `S054`
  row lands the registry is 54 and the same guard reports **24** (`S031–S054`), because staged `S054`
  is the IPA 内閣府 request PDF — the same shape as r36's S053 prediction. The lesson must state the
  head it is read at, never carry the figure alone.
- **Register ids are package ids, not lane ids.** Register S037 is `openstd…GB/T 30279-2020` while
  lane S037 is the Cybozu bounty FAQ; register S048 is a `std.samr.gov.cn` plan record while lane S048
  is Microsoft MSVR (`wave1/ScribeAssimilationGate.md` §1). A quarantine verdict is therefore about
  the package document, and says nothing about the lane row that happens to share the number.

Quarantine slice verdicts: 7 rows, **0 adopted** — measured 0 fabrication-class, 1 unreachable
(S048), 6 present-and-located (S065, S068, S069, S070 clean; S037 and S054 located with quote-form
defects); see the Gate table and its divergence note. Standing refusals: 7 entries, no flip cleared
(package byte-identical, 0 of 7 flip conditions met; `wave1/ScoutStandingRefusals.md`).

## considerthese 2026-10-26 dispositions

Ledger: `corpus/considerthese-ledger.md` (new file; 18 rows over the 2026-10-24/25/26 files; landing
`⟨pending: wave1/ScribeConsiderthese.md §3 delivers the byte-exact block, sha256 `7c232983…`⟩`). Old →
new for the 2026-10-26 seven:

1. **Distance-to-next-score thresholds** — open. `score-gap.py` computed the r36 gap (`gap: 24 of 47
   rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`); `SCORECARD.md:309-321`
   still declares only the saturation line and `grep -c 'Threshold for 8' SCORECARD.md` → `0`.
2. **End-to-end domain task round** — open; `SHONEN.md:164-166` box 2 `[~]`, no new task.
3. **Quiescence gate before `complete`** — mined → landed r36 (QUALITY R28 + `r36-closure.sh:93-108`
   E9 limbs); round 37 hardens it (E14 fail-closed, E10 committed positive limb).
4. **Cap or externalise wave evidence** — open (operator-owned). Measured at HEAD: 7,266 tracked files,
   6,990 under `.ufo/` (96.2 %); 119,222,967 bytes total vs 113,443,672 `.ufo` (95.1 %); no release/LFS
   artefact committed.
5. **Land the owed F18 `PROVINCE.md` amendment** — mined → landed r36 (`PROVINCE.md:77`).
6. **Re-tune cadence and depth** — open (recorded, no change).
7. **Proposal-status ledger** — mined → landed r37: a ledger plus QUALITY **R31** (round-37
   append-only block), with the lesson recording old → new; the D6 class additionally adds QUALITY
   **R30**. **Conflict recorded, not resolved:** the frozen non-claim item names
   `corpus/considerthese-ledger.md` and `wave1/ScribeConsiderthese.md` drafts that new file (18 rows,
   sha256 `7c232983…`), while the delivered R31 row names the already-tracked
   `corpus/knowledge/considerthese-proposals-ledger.md` and its receipt reports the new path as absent
   (`wave1/ScribeQualityRows.md` F1, F5). Landing must make the row and the filed ledger cite one
   path; until then "R31 + ledger" is two drafts, not one artifact.

## Census

Before (measured at base, `.ufo/waves/round-37/census-before.txt`): `sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kasegi` → exit **0**, `W04 S028` + `W04 S029` only; rows **53**
(tier.A 50 / tier.B 1 / tier.C 2; mined 41 / queued 9 / rejected 3). After, on a faithful pre-state
mirror carrying the planned row **and** the entry: rows **54** (tier.A **51** / tier.B 1 / tier.C 2;
mined **42** / queued 9 / rejected 3), `validate` exit **0**, the same two W04 lines, **0** E-codes
(`wave1/ExecCensusReplay.md` §3–§4). The mirror's controls show the green is not vacuous: row without
entry → `E11 S054` exit 1; duplicate id → `E03`; same URL under a second id → `E04`; end-of-file
append → `E12 S054 row outside Registry section`.

After-state at the integrated head (real lane file, not the mirror):
`⟨pending: L1 integration census measurement⟩`.

## Mistakes

M37-1 … M37-5, minted this round from the round-36 spot-check's routed defects and the r36 scratch
incident. The table below is a summary of `wave1/ScribeMistakes.md` §2, which holds the full row text
and the derivation commands (§3–§5) and is the artifact to paste if verbatim rows are wanted; the r37
suite is absent at this head, so every green below is the frozen after-state, not a run this seat
observed.

| id | class | event | evidence | captured-by | fix | able to fail |
|---|---|---|---|---|---|---|
| M37-1 | evidence-record | Round-36 C1 committed only the negative limbs: `all-gates.txt` at the judged head carries the forged-selftest rejections and the two reds, no `suite-sha256=` header, no E-numbered payload line, no `closed=9/9`, no `selftest case=` line. The positive run existed only as prose in the SCORECARD "measured closure" line and the report erratum; two seats' scratch dirs were swept before the final gate run, so no stable transcript was available to commit. | `corpus/lessons/round-36-verifier-spotcheck.md` §2 C1 evidence gap / §5 D1; 28-line `all-gates.txt` at `a23dc478` | none (new) | E10 receipt check | base tree red vs final green |
| M37-2 | fail-open-gate | r36 E9 read the lane's status as `git … status --porcelain 2>/dev/null` piped to `count_lines`, then `porcelain=${porcelain:-0}` (`r36-closure.sh:465-466`): a failed status read scored 0 dirty lines, i.e. clean. Its runtime face: concurrent quiescence sweeps wiped `/fast/scratch/hyaku/kasegi-r36/*` mid-wave, so the limb's clean reading could be produced by deleting the evidence it reads. | suite sha256 `4db1ae70…b7c4` (894 lines) at `c20300df`: `grep -cF 'porcelain:-0'` → 1; `2>/dev/null` on the same limb | none (new) | E14 fail-closed shape + QUALITY R30 | `porcelain:-0` mutant red |
| M37-3 | stale-premise / label-drift | `corpus/lessons/round-36.md:3` and `SCORECARD.md:1492` name `e666d902…` as the round's "final lane commit" — an intermediate ancestor five commits below the round-36 tip `c20300df` and four below the judged head `a23dc478`. | measured at `a23dc478` and `HEAD`; `grep -cF 'Final lane commit: e666d902' SCORECARD.md` → 1; ancestry `a23dc478→c20300df→b56a416` all `anc=0` | R2 / R19 | E12 anchor-ancestor naming | stale-label fixture red |
| M37-4 | counter-discrimination | `SKILL.md:1111` registers `r36-closure.sh` with the literal type cell `gate\|probe` instead of a single choice, and its verdict map stops at `exit 0 only for K=9`: the suite's plain-run `exit 2` has no verdict, so `could-not-evaluate` is unrepresented. | measured at `c20300df` and `HEAD`: row `:1111`; `grep -cF 'gate\|probe' SKILL.md` → 6 rows; no `could-not-evaluate` in the row | R29 | E13 single-choice type + exit-2 verdict | `gate\|probe` fixture red |
| M37-5 | stale-premise | `LOG.md:1665` (round-36 C1 bullet) states the round landed `corpus/instruments/r36-fixtures/`; the directory is in no r36 tree and LOG is append-only, so the false statement stands as filed. | `git ls-tree -r --name-only` at any ref, piped to `grep -c r36-fixtures` → 0 at `c20300df`, `a23dc478` and `HEAD`; spot-check §5 D2 | R9 | E11 named correction entry | uncorrected LOG red |

## No-harm

`⟨pending: measurement at the integrated head⟩` — r36 discipline holds: `SKILL.md`/`PROVINCE.md` base
lines byte-identical (EOF appends only), `density.py` not re-run, no density move claimed; every claim
bit changes only on `corpus/` and `.ufo/waves/round-37/`.


## Integration resolutions (L1 addendum, appended 2026-10-26)

- F1 (two quote-pin sets): the landed manifest pins Q1=L259, Q2=L277, Q3=L473, Q4=L68 (navigation-only); the entry's `recheck:` comment and body quote set was aligned to the manifest pins; body quotes remain once-only-verified.
- F2 (quarantine verdicts): measured slice = 0 fabrication-class, 1 unreachable (S048), 6 present-and-located (S037/S054 located with quote-form defects; S065/S068/S069/S070 clean). Nothing adopted; the register's class column is a candidate list, not a verdict.
- F3 (ledger path): claims.json's `corpus/considerthese-ledger.md` shorthand resolves to the tracked `corpus/knowledge/considerthese-proposals-ledger.md` (round-30 home), extended this round with the 18-row disposition table and the re-pin note; R31 cites the tracked path.
- F4 (suite): the r37 suite was landed as built and self-tested by the wave (digest 0da98e37…). Review findings F10–F13 were assessed: E13's existential conforming-row reading is satisfied by the appended single-choice row placed last in the registry section; E14's shape greps plus E9's behavioral rc-gate (M1a/M1b measured) close the D6 class; continuation-split reintroduction (F11) is an accepted residual documented here, caught by M5 digest binding for any suite-byte change.
- F5 (E10 protocol): the gate receipt was generated from genuine suite runs at the F0 head, committed, and re-verified by the F2 head run (fixed-point protocol).
- F6 (harness): `entries=23 pass=23` is a live-lane measurement at the final head; mirror runs proved the binding only.
- F7 (quiescence): all seat dirs and l1prep/ removed before the final run.
- Erratum timestamp correction (R9): claims-erratum-1.md's filed stamp read 14:04Z from a local clock; UTC was 17:04Z (commit b3620681 at 2026-10-26T17:00Z; freeze 224df74d at 16:57Z).
- Id-collision count at the final head: registry 54 × staged 94 → 24 standing collisions (S031–S054); staged S054 is the IPA request PDF (different document), so no staged row is adopted.

## Pending-marker resolutions (round 38)

Appended 2026-10-26 by the round-38 scribe from committed bytes; the marked lines above stay byte-identical at `corpus/lessons/round-37.md:10,85,90,95,216,265,300,320` and this section edits nothing in place (append-only).

| line | what the marker deferred | resolved value | evidence pointer |
|---:|---|---|---|
| L10 | the round-37 final lane commit, deferred on the ground that a commit cannot contain its own hash | the round-37 lane tip `83975acc83df4bd8d5eaf463182ae615f2b64546` is the last round-37 lane commit; it adds only `.ufo/waves/round-37/kasegi-r37-build-results.json` (392 lines) to the head the round-37 report and verifier judged, `2387dcf6ccfefcfb703783387b9aade8fc82abfa`. The round-37 SHONEN lines still name `aa88877bf921d952137817b91ca76234b206da65` (the gates-receipt ancestor) as the "final lane head", and the round-37 SCORECARD section names `f3246559…` under `Final lane commit:` — both are the round-38 D-B/D-D correction targets (non-author grade: `.ufo/waves/round-38/wave1/RevPendingResolutions.md:48`, applied) | `corpus/lessons/round-37-verifier-spotcheck.md:8-10` (A and the tip); `2387dcf6:SHONEN.md:172,176`; `SCORECARD.md:1509` |
| L85 | landing of the 84-line F20 entry draft, described there as not landed | landed as `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` at `0acffc82`: 84 lines, `source: S054` on L3, `verified-at: 2026-10-26` on L4, executable `recheck:` on L6 — not byte-identical to the draft: L3 and L6 carry integration edits to the anchor/locator notes (non-author grade: `.ufo/waves/round-38/wave1/RevPendingResolutions.md:49`, applied) | `0acffc82:corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md:3-6`; `corpus/lessons/round-37-verifier-spotcheck.md:90` (`^source: S054` count 0→1) |
| L90 | existence of that entry file at the integrated head | present at `83975acc` with 84 lines (`git cat-file -e` exit 0; `git show … \| wc -l` → 84), and no round-37 commit after `0acffc82` touches it | tree `83975acc`; `git log 0acffc82..83975acc -- corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` → empty |
| L95 | the `source-recheck.py --source S054` transcript at a committed path and at the integrated head | the gates file holds no C2 limb (it carries E1–E14 only), so the committed run is the seat's mirror run — `S054:sha256 OK` plus Q1–Q3 at anchors 6/7/14, exit 0 — while at the integrated head the four landed manifest anchors re-derive over committed bytes by plain substring as 259/277/473/68 with `occurrences=1` each, and the entry's own recheck line reproduces the instrument run | `83975acc:.ufo/waves/round-37/wave1/ExecC2Harness.md:225-230`; `0acffc82:corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md:6`; `corpus/lessons/round-37-verifier-spotcheck.md:95` |
| L216 | the prep receipt and the integrated-head gates file carrying the suite digest, the fourteen payload lines and the selftest cases | `.ufo/waves/round-37/final-gates/all-gates.txt` is tracked and byte-identical from `aa88877b` to `83975acc`: 121 lines; `all-gates v1` (:1), `export-ref=9492c776…` (:2), `suite-sha256=0da98e37…` (:3, equal to `r37-closure.sh` at the judged head); 14 `payload=… closed=1` lines (:8-:21); `closed=14/14 exit=0` (:22); 14 `selftest case=` lines (:31-:113); `selftest cases=14 failures=0` (:114); the prep receipt is committed beside it | `83975acc:.ufo/waves/round-37/final-gates/all-gates.txt:1-5,22,114`; `83975acc:.ufo/waves/round-37/wave1/ExecGateReviewPrep.md:48-107`; `corpus/lessons/round-37-verifier-spotcheck.md:50-56` |
| L265 | the byte-exact considerthese block and its landing path | the block is committed byte-exact inside the seat receipt (9,184 bytes, sha256 `7c23298319a581720a5a66f63ea0b97ca65f2b9f3dd858bfd019fd86abc43706`); the path named there, `corpus/considerthese-ledger.md`, is in no round-37 tree, and the landing went instead to `corpus/knowledge/considerthese-proposals-ledger.md:37` as the heading `## Round-37 dispositions`, which holds no rows at the tip — the empty section routed as round-38 defect D-F and closed by the round-38 ledger deliverable | `83975acc:.ufo/waves/round-37/wave1/ScribeConsiderthese.md:56`; `0acffc82:corpus/knowledge/considerthese-proposals-ledger.md:37`; `git ls-tree -r --name-only 83975acc` → 0 rows for `corpus/considerthese-ledger.md` |
| L300 | the census after-state at the integrated head | exit 0 carrying `W04 S028` and `W04 S029` only (the two standing duplicate-URL warnings) and no E-codes; registry 53→54 with the S054 row | `corpus/lessons/round-37-verifier-spotcheck.md:98,142-143`; `83975acc:.ufo/waves/round-37/wave1/ExecCensusReplay.md:11-13,84-87` |
| L320 | the No-harm measurement at the integrated head | `git diff --numstat b56a4168 2387dcf6 -- . ':!.ufo'` gives zero deletions on every changed file — SKILL.md 2/0, SCORECARD.md 15/0, PROVINCE.md 74/0, corpus/README.md 56/0, corpus/SOURCES.md 1/0, LOG.md 17/0, SHONEN.md 9/0 — so the round's front-door edits are end-of-file appends only and no density move is claimed (the 74-line PROVINCE.md append is itself defect D-A, corrected this round) | `corpus/lessons/round-37-verifier-spotcheck.md:105-111`; re-measured in `.ufo/waves/round-38/wave1/ScribePendingResolutions.md` |
