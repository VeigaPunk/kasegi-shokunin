# kasegi round 35 — lesson

Revisions: base `3266c9937b03062d9bbc2f436e20820115ed179c`; claims-freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`; wave-1 spec/dispatch `da2d3c687f82a9814ee71c91c930cb733050d37c`; integration commit `aa6ad99bb90c4fe30dc5c326adf2f82d8ec84b1b`; final lane tip named in the round report. Shape: one v2 wave `kasegi-r35-build`, 64 seats (executor 18, scribe 12, reviewer 10, scout 6, mutation-tester 5, critic 5, connector 4, sentinel 2, simplifier 2; attack share 20/64 = 31.2 %; m_flash roles 39/64 = 60.9 %). Answering model per seat receipts: `inception/mercury-3` (config route table; never a model from a seat).

## Frozen claims — before → after

Frozen in `.ufo/waves/round-35/claims.json` (sha256 `fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982`). Before-controls replayed on `git archive 617496b9` by `ExecBeforeReceipts.md` — every stored value MATCH.

**C1 depth:verifiability (4, held) — D1–D7 closure suite.** Before: `r35-defect-closure.sh` absent (ls_exit=2); D1 `filled by the L1`=1; D2 `201.7`×2, `201.2`=0; D3 SKILL registry 0; D4 results untracked; D5 erratum absent; D6 dead-seat sentence present; D7 supersedes-R22/R23=0. After (landed bytes): suite `closed=7/7 exit=0`, `--selftest cases=7 failures=0`, base tree `closed=0/7 exit=1`; D1 0/3; D2 erratum present (`201.2` ×2, row bytes untouched); D3 registry 4/4; D4 tracked=1 + provenance note (`aa6ad99`); D5 erratum present (`discriminating invocation` ×5, `per-id occurrences` ×5); D6 sentence 0 + `Correction (round 35)`; D7 `supersedes R22/R23` 1/1. Counter: `bash corpus/instruments/r35-defect-closure.sh`; selftest discriminated (fake suite/plain/complete reports; 4 forged judges rejected).

**C2 coverage (7, held) — F18 CISA KEV admitted.** Before: frontier 17, registry 51, S052 0, entries citing S052 0, harness 20/20, knowledge 46. After: frontier 18 (`corpus/README.md:388`), registry 52 (`S052` at `corpus/SOURCES.md:58`), S052 row 1, entries citing S052 1 (`corpus/knowledge/cisa-kev-catalog.md`), harness `entries=21 pass=21 exit=0` incl. `PASS F18 ids=S052`, source-recheck S052 all 5 assertions occurrences=1/sha256 OK/exit 0, census exit 0 (W04 S028/S029 only), knowledge 47. Capture: `corpus/source-snapshots/round-35/S052.txt` (JSON feed, 1479694 B, 27870 lines, sha256 `d69349e86c…8826`, fetched_utc `2026-10-26T06:32:40Z`); manifest `06bfcc71e6df…`; live re-open 0 differing lines.

## Gate

- **Admitted — F18 / S052**: capture + manifest + registry row + entry, all landed this round; source-recheck exit 0 on committed bytes; live re-open byte-identical. URL `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`; access date 2026-10-26. Note: the root `.json` endpoint 404s (recorded in the search log); the feed is linked from the catalog page. Captured quotes: header/record lines (anchors 2/3/4/15472/19165), each ≤25 words, exactly-once.
- **RevEntryF18 REFUSE→repair→ADMIT**: intermediate bytes refused on Q2 (Claim 4b asserted directive force from a live page with no registry row/capture); repaired by demoting that content to a labelled Scope note (`:89`, "a live-page note, not an admitted claim (Q2)"); final bytes ADMIT. Adding a directive-page row would have moved registry 52→53 and broken the frozen C2 literal `registry rows != 52` — recorded as the repair constraint, not a defect.
- **Rejected — standing assimilation refusals** (all re-confirmed, flips unmet): `program-scope-rules-and-asset-boundaries` (quotes/location), `claim-packaging-and-report-quality` (BILISRC unregistered), `cn-crowdsourced-testing-roles-and-conduct` (no H1; S081/S082 unregistered), `chinese-crowd-testing-national-standard-2026-10-23` (S077/S078/S079 unregistered), `chinese-criminal-thresholds-and-authorisation` (S044–S046 id collision), `chinese-program-severity-instrument` (anchor absent from capture), `program-severity-ladders-and-reward-scales` (same-name lane entry differs — overwrite hazard).
- **Quarantine slice — 7 rows re-derived (S-id on every line)**: S065/S068/S069/S070 `present-and-located` (S068 is already lane S040 — duplicate, nothing to adopt; S069/S070 need a recorded transport exception), S037/S054 `prose-class-unverifiable`, S048 `unreachable` (404); **adopted 0**. Fetch verdicts are UA/TLS-dependent — pinned to `capture-source.py:32` UA; round-34's 403/0-byte verdicts for S068–S070 were invocation artifacts (erratum-class note, disposition unchanged).
- **Id collisions**: `reg_ids=52 staged_ids=94 collisions=22 S031..S052` (post-C2; 21 before S052 landed); guard proven load-bearing (indented S031 row caught by 0–3-space pattern, missed by column-0-only); adopt by document, never by number (staged S052 = CNNVD weekly, lane S052 = CISA KEV).

## Mistakes

- **M35-1 — D4: wave writes landed after the `complete` line** (`.ufo/waves/round-34/wave1-results.json` untracked at round-34 closure). Class: landing/closure-order. Evidence: spotcheck D4; `git ls-files` 0 at base. Captured-by: R4's landed-means-committed reading was not applied to the results file. Fix: committed with provenance note (`aa6ad99`); quiesce before final commit.
- **M35-2 — the KEV capture URL in the frozen wave spec 404ed** (root `.json` → 404); the seat discovered the official feed one path over and captured it; the L1 steered the row/entry/search-log to the feed URL. Class: source-URL drift. Captured-by: seat honesty (three-UA 404 reproduction), not a check. Fix: search-log records both endpoints; future fetch prompts resolve the canonical path first.
- **M35-3 — BOD 22-01 is revoked, superseded by BOD 26-04**; the entry must not present 22-01 as current (Page L208 "Revoked"; 340 records name 22-01 vs 139 name 26-04). Class: currency drift. Captured-by: ScoutKEVLive live open. Fix: entry cites BOD 26-04 in the labelled note; a row+capture for the directive page is the minimal next-round repair (registry 52→53 requires a claim erratum).
- **M35-4 — instrument gaps recorded by MutC2Entry**: (i) a manifest anchor retarget is not fatal while `occurrences=1`; (ii) paraphrased entry quotes pass source-recheck and the harness (nothing compares entry text to the manifest). Class: instrument blind spots. Captured-by: mutation seats. Fix: harness-level quote-binding (routed to instrument owner; not landed this round).
- **M35-5 — draft-time suite `cases=7 failures=0` was unreachable until the L1 landed D4/D6/D7**; the three failures were the fail-closed behaviour (order dependency). Class: dependency ordering. Captured-by: ExecDoNothingReject. Fix: landed; suite reads `closed=7/7`, `cases=7 failures=0`.

## considerthese

Proposal 2 (2026-10-25.md) mined → QUALITY `R26` (distance-to-next-score reporting; score-gap read-only; `score-gap.py` prints threshold `SCORECARD.md:331` and `gap: 24 of 47 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`). Other proposals unchanged: 1 (already R14), 3 (bounty-craft E2E — not attempted this round), 4 (status ledger — not mined), 5 (already R15), 6 (already R23).

## Census before → after

Before (census-before.txt): exit 0, W04 S028/S029 only. After: exit 0, W04 S028/S029 only (rows 52, tier A 49 / B 1 / C 2, malformed 0, dups empty, enum/tier-inflation empty, missing used-by empty).

## No-harm

`density.py SKILL.md` valid 201.2 baseline held (no density claim); `anchorcheck.py SKILL.md` 0 bad, `LOST-RECORDED=306`, `PIN-BROKEN=0`, exit 0. Numstat: `SKILL.md` +13/0 (registry rows), `corpus/README.md` +28/0, `corpus/SOURCES.md` +5/0, `corpus/QUALITY.md` +21/0 (supersession block), `PROVINCE.md`/`LOG.md` 0 changed; `SCORECARD.md` carries 15 deletions, all within the round-34 region the placeholder substitution replaces (D1). No misroot writes; no fleet-root strays.

## Open items / unverified

- Final `wave1-results.json` for round 35 is written by the dispatcher after the wave settles; the report cites the receipts; seat counts/dead seats from results when the dispatcher finalizes (1 seat's receipt was completed live via messages before the results file landed).
- Score-gap instrument digest drift: `score-gap.py` now `57584fda…` vs registered `855869bf97…` (F6) — R9 forbids rewriting; routed as a dated observation.
- R23's narrowed disposition limb and R26's dual-purpose row recorded (ScribeQualityDraft F3/F5) — L1 decisions noted, no bar change.
- BOD 26-04 row+capture repair (next round).
