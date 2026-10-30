# Round 47 — Kasegi

L1 `KasegiR47a3`; base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`; claims frozen at `308a2cb2dc7bdce233461cc1ac49dd88e51c6193` in `.ufo/waves/round-47/claims.json`. C1 targets depth:verifiability (the lowest non-retired axis, score 4): the four lane-repo round-46 routed defects D5–D8, decomposed into eleven limbs. C2 targets coverage: the proposed F30 ZDI broker-policy admission. Neither is exploratory. A counter pass alone does not settle semantic admission or novelty.

## Mistakes

| ID | Class | Evidence | Captured-by | Fix and falsifiability |
|---|---|---|---|---|
| M47-1 | landing | `round-46-verifier-spotcheck.md` §8 D5: three intended bullets remained inside drafting fences in SOURCES.md; instruction prose was committed instead of integrated | QUALITY R48: content belongs in its real rendered section, not merely somewhere in the bytes | Land the three bullets in Search log/Registry changes and remove the scaffold. C1 L1/L2 read red on the base; the fenceleft and regbullet-missing probes in `controls/selftest-receipt.txt` remain red. |
| M47-2 | stale-premise | The same spot-check §8 D6: capture chrome called prose, entry order misattributed to the source, imminent-fix case incorrectly counted as permission to publish without a fix | Q3/Q4 and the source-vs-claim comparison duty | Same-line corrections and an appended round-46 erratum naming the dropped findings `R46bW2RevEntryClaims` and `R46bConnPatterns`; neither findings' existence nor a green counter proves the corrections true. The falsephrase1/orderfalse/threecases probes demonstrate red-before behavior. |
| M47-3 | attribution | The spot-check §8 D7: S074's 42-line capture has no committed producing recipe; the committed instrument instead produces 610 lines | QUALITY R49; source capture provenance | Preserve the old capture, re-capture the same document as S076 with `capture-source.py --kind html`, and supersede S074 without rewriting its immutable registry cells. Two captures yielded the same digest; `controls/capture-determinism.txt`. C1 L8 rejects altered manifest/anchor bytes; L9 rejects old or unlocated citations. |
| M47-4 | reference-drift | The spot-check §8 D8: S074 was consumed while the ZDI lead still proposed that id; the REST-API pointer lacked a Leads bullet; S068 was generalized beyond one advisory | CORPUS append-only ids and Q4 attribution | Record the id reservation disposition, the unopened REST-API lead and the S068 precision below. L10/L11 reject absent lead/precision fixtures. No source id is reserved by an unopened lead. |
| M47-5 | vacuous | Pre-freeze counter-source mutation battery: C1 35 mutants, 19 caught, 16 uncaught; C2 21 mutants, 3 caught, 18 uncaught. `.ufo/waves/round-47/controls/mutbat-receipt.txt` | QUALITY R50 | Disclose every survivor before freeze in the claims. These are selftest coverage gaps, not equivalence proofs. The 43-case tree-probe suite passes, but full mutation coverage is not claimed. A battery exit 1 is not a pass. |
| M47-6 | number-drift | Pre-freeze plain-count calibration found `grep -c 'to append'` = 2, not 3, and `grep -c 'S074.txt:'` = 54 matching lines, not the 59 occurrences | CORPUS: a count carries its command; QUALITY R2 | Corrected before freezing. The frozen claim distinguishes lines from occurrences and treats the surviving true phrase 'three cases that follow, only two' as contextual, not its kill rule. |

## Gate

Opened personally this round:

- S075 candidate: https://www.zerodayinitiative.com/advisories/disclosure_policy/ — access `2026-10-30T10:35:37Z`, HTTP 200; committed instrument capture `corpus/source-snapshots/round-47/S075.txt`, sha256 `9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1`. Same-instrument second capture was byte-identical. Scope: ZDI's own disclosure-policy text, not rewards, submission rules or advisories.
- S076 candidate superseding S074: https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories — access `2026-10-30T10:35:47Z`, HTTP 200; capture `corpus/source-snapshots/round-47/S076.txt`, sha256 `9bd8ab57dac9cc605355c60831f51e02b92f5e34990aa99a49566d207e6bbb38`. Same-instrument second capture was byte-identical. The old S074 capture remains historical evidence, not deleted.

Located Gate quotes (each ≤25 words):

- S075:23: “fifteen business days after the initial contact” — only the fallback public-advisory clock has this explicit trigger.
- S075:24: “four months (120 days) to address the vulnerability” — the vendor deadline; its start event is not named explicitly.
- S075:24: “sole discretion of TrendAI™ ZDI and will be granted only in rare circumstances” — no automatic extension entitlement.
- S075:25: “For critical-rated bugs where active exploitation is detected or imminent, the vendor will have 30 days” — one faulty-patch tier, not the ordinary deadline.
- S075:26: “In no cases will an acquired vulnerability be” — acquisition is explicitly mentioned; the remainder of this sentence rejects keeping it quiet.
- S076:582: “GitHub is a CVE Numbering Authority (CNA) and is authorized to assign CVE identification numbers.”
- S076:598: “wait to disclose the issue when the fix is ready” — the imminent-fix case is not permission to publish without a fix.

S075 novelty is contested, not proven by numbering: the prior round's `R46ScoutLeadZDI.md` recommended adding a coordinator case within F02 rather than a separate frontier topic. The proposed F30 must survive that overlap attack. The round-46 flip condition required a later round claiming the ZDI deadline rule and reopening the page; those procedural conditions are met, but they do not settle the independent coverage judgment.

ZDI id reservation precision (D8): the old lead's proposed S074 was consumed by F29. This round uses S075 for the opened ZDI candidate; this records the allocation without treating a lead as a durable reservation. Whether the candidate is mined or rejected follows its Gate decision, not the old proposal.

S068 precision (D8): S068 is **one GHSA advisory entry**, not the GitHub Advisory Database's documentation. The old lesson's 'database row class' statement overgeneralized an n=1 precedent. Rejection of the database as a source for the maintainer lifecycle can stand independently: a publication destination is not the lifecycle's first-party policy.

REST-API page: https://docs.github.com/en/rest/security-advisories/repository-security-advisories remains an unopened lead, not a source row. Rejected for this round's admission because its body has not been opened and grounded here; flip: open it in its own round, locate quotes and demonstrate new ground.

## Registry changes

Pre-existing registry cells are unchanged at freeze. S075/S076 captures are intentionally staged before their row decisions, so the pre-admission capture-binding receipt reports unbound captures; it is not a green round-end gate. Every later status/recheck/used-by change must be logged old→new here.

## Verification boundaries

No lane-dispatched seat is the non-author closure. Independent admit/reject sampling and promotion remain outside this lane. All SHONEN boxes remain `[~]`. The open L0 question about the 22 gated historical rechecks is routed around, not treated as answered.

## Live-tree versus frozen-tree replay

`.ufo/waves/round-47/w1/R47ExecGateReplay.md` independently reproduces C1 `fixed=0/11` and C2 `fixed=1/7` on the base export. Its current-working-tree C1 reads `2/11`, not the seat card's expected zero: this lesson was written after freeze, legitimately making L7/L11 true. That is integration progress, not a changed frozen before-value. The freeze commit has no round-47 lesson. The seat card's assertion about the moving working tree was stale; the committed base replay remains the baseline.

## Wave-1 additional mutation evidence

`.ufo/waves/round-47/w1/R47MutC1b.md`: six fresh counter-source mutants, two caught and four uncaught. Crafted pristine-versus-mutant witnesses distinguish the LESSON46 acceptance branch, body-window edge bounds, Leads section scoping and the S068 precision phrase. These are additional selftest-coverage gaps, not equivalent mutations. They do not replace or erase the pre-freeze 34 survivors. The seat reports its saved per-case stdout as authoritative where its receipt driver's `divergent_cases` parser failed on spaces in the `want=` field.

## Integration decisions — frozen claims are not rerolled

- **C1 is not fully verified.** Its frozen prose required S074 `mined→rejected`. `.ufo/waves/round-47/w1/R47RevD7.md` demonstrates that transition breaks capture-binding rule B3; it also leaves positive teaches text on a rejected row. The integrated repair keeps S074 mined, re-points its permitted used-by cell to the historical round-46 lesson and admits S076 as the reproducible successor. The harmful transition is not performed and the frozen target is not rewritten.
- **C2 is unmet.** `.ufo/waves/round-47/w1/R47CritNovelty.md` shows the proposed deadline rule instantiates existing F02. The policy entry is retained as an F02 coordinator case; no F30 frontier row is added. A newly numbered row would not prove coverage. The additional non-suppression detail is useful but is not substituted for the frozen claim.
- Wave-1 counterexamples (`R47RevCounterC1.md`, `R47RevCounterC2.md` under that wave directory) accept hidden/commented material and disguised rows. Counters remain byte-frozen as diagnostic evidence; no post-score hardening is presented as validation of their original predicates.

## Final Gate decisions

Admit S075's bounded policy facts as F02 enrichment and S076's reproducible capture for current F29 guidance. Reject F30 as independent frontier ground on the F02-overlap evidence; flip requires a future, independently scoped claim demonstrating an uncovered surface, not another row number. The REST-API page remains an unopened lead. The original S074 capture remains mined historical evidence, with its current-guidance role superseded. These are lane decisions, not the independent closure's admit/reject sampling.

Registry cells old→new: S074 used-by `corpus/knowledge/github-repository-security-advisories.md` → `corpus/lessons/round-46.md`; S074 status `mined` → `mined`, recheck `90d` → `90d` (unchanged). No other pre-existing status/recheck/used-by cell changes. New S075/S076 rows are docs/tier-A/mined and cite their opened captures. Old S074 anchor wording that calls every line prose is marked historical and corrected by the superseding row and this lesson; immutable cells are not rewritten.

M47-3 fix refinement: preserve historical mined capture bindings rather than reject the predecessor. The demonstrated B3 red-before arm remains in `.ufo/waves/round-47/w1/R47RevD7.receipts.txt`; R54 explicitly captures why a frozen harmful after-state must be reported unmet.
