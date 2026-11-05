# CriticClaims — round 78 attempt 1, wave 1 (frozen at 2d81fe84, base 0687cca8)

Seat: adversarial falsification of the two frozen claims (read-only). Scratch
`/fast/scratch/hyaku/kasegi-r78/CriticClaims` (deleted before yield). No lane,
corpus, SKILL, PROVINCE or instrument bytes touched; no git/jj writes; no tools
installed. All commands below ran over committed bytes at the freeze (lane tip ==
2d81fe84) or over scratch copies.

## Part A — the six assigned questions

**1. Is C1 a depth:verifiability move, or gate-hardening dressed as one? Can it verify at all?**
It is gate/instrument-hardening in the lowest-axis slot, and the lane's own rules make that
conformant, not dressed. QUALITY.md:415 (R58) explicitly provides the "nominal" label with the
score held and the non-moving metric named; C1's `axis_score` field does exactly that ("the
scored resolve.py census is not read by this counter"). Precedent is long: SCORECARD r22
(`:331`), r23 (`:407`) and r47-class rows all read "depth:verifiability 4 → 4 … Improved, score
held" for instrument-soundness moves. What a reader sees if the score does not move: a
SCORECARD row "4 → 4 (nominal; named non-moving metric: resolve.py citation-survival census)"
next to the measured gate deltas (named-kill 5/8 → 8/8; TMPDIR traceback rc1 → exit 2 refusal)
— indistinguishable in shape from the accepted r22/r23 rows. The claim verifies through P1–P7,
all mechanically checkable at the landing commit; I confirmed the base-side halves of P2, P4,
P5, P7 myself (Part C). So: conformant and verifiable **in structure**, with one material
verification risk (objection 1) that makes the frozen text mislead the successor author exactly
the way round 77 failed.

**2. Is C2 a new claim or a narrowed re-declaration of rejected r77 C2? Cherry-picking?**
New claim, and the narrowing is the r77 gate's own prescribed successor shape, not
cherry-picking. corpus/lessons/round-77.md:13 (closure flip line): "a successor that claims
only the batch-specific clauses (Q01–Q06, Q09–Q11, Q13) and cites Q07/Q08/Q12 as held."
SCORECARD `:2957` (r77) records the rejection reason verbatim. Round 78 goes further and drops
Q04/Q05/Q06 — justified: those quotes are pointer sentences, not ground ("The parameters are
the same as those in POST /v1/query…", "Instructions are available for handling pagination for
querybatch requests.", S112.txt:28–30 region), so they "pass" only as cross-references; the
claim names them as not-claimed. Clauses that pass only because they are cross-references:
**Q04 (parameters pointer), Q05 (instructions pointer), Q06 (item-rules pointer)** — all three
excluded by the claim itself. Against F51 (osv-post-v1-query-contract.md, S108) the claimed
seven are genuinely batch-specific: Q01/Q02 (batch definition, ids+modified-only return shape),
Q03 (input-matched ordering), Q09 (per-query partial tokens), Q11 (3,000 total) have no F51
counterpart; Q10 and Q13 carry new per-query substance but share concepts with F51 Claim 5
(the 1,000 number, S108:136; the next-request token rule, S108:144) and must be swept per
clause (objection 4). B6 byte-greps at base: all seven quotes absent from corpus/knowledge/*.md
(0 hits each, verified).

**3. Does either claim harm an axis?**
None found. The counter has no other callers (`grep -rln recheck-cwd corpus/instruments/*.py
scripts/*.sh` minus itself → none), so the exit-2 refusal breaks no consumer; the real-tree
census expected line is unchanged by C1 (re-run matches control byte-for-byte); density is not
touched; coverage's held-score-on-admission shape is accepted practice (SCORECARD `:2909`, r75:
"8 (held; F53 admitted; the denominator is operator-owned)"). The SKILL.md/README pin moves are
R113 obligations, not depth-census inputs (R58 names the non-moving metric).

**4. Are the do-nothing controls real? Could a do-nothing reach the target?**
Real and substantive; I re-ran them. c1-donothing-selftest-r78.txt reproduces exactly (base
`selftest cases=6 failures=0`, rc0); c1-base-missing-tmpdir-r78.txt reproduces (FileNotFoundError
traceback, rc1); c1-base-realtree-census-r78.txt reproduces (`entries=91 … conformant`, rc0,
exit0_foreign=69 exit1_foreign=22). C2 side re-measured live: `FRONTIER-CENSUS rows=53
admitted=53 closed=53 problem-rows=0 registry=112`, `entries=56 pass=56 exit=0`, knowledge=91,
expected 93 lines/91 .md rows (sort -c clean, set-equal), capture-binding `records=92 bound=92
unbound=0` rc0. A do-nothing cannot reach either target: C1's target needs cases=13 + 8/8 named
kills + the refusal (base: cases=6, traceback, no refusal); C2's needs rows=54 admitted=54,
knowledge 92, S112 mined (base: 53/91/queued). Two receipt-hygiene defects: objection 5.

**5. Does C2 risk the 'no universal clauses' admission criteria (claims.json wording)?**
The phrase does not exist: `grep -c universal .ufo/waves/round-78/claims.json` → 0, and the
corpus protocol has no such wording. The operative rules are QUALITY.md:17 (Q4
anti-universalization) and the B6 distinctness machinery. Real Q4-shaped risk: Q10/Q11 claim
the 1,000/3,000 thresholds while their on-page qualifier (S112.txt:170, "These numbers can vary
slightly because of threading…", held in F51 from S108:136) is unclaimed — an entry stating the
thresholds as crisp rules without the page's own caveat makes OSV's contract crisper than the
page states it (objection 4). Q03's "will be guaranteed to match the input" must stay
attributed to OSV's page, which the entry form (attribution section) enforces by convention.

**6. Does the frontier step hold (S112 opened 2026-11-05 live)?**
Holds. SOURCES.md:124: S112 tier A, status queued, opened 2026-11-05, snapshot sha256 pinned.
S112.txt sha256 = f3ca0465…0907, byte-identical to round-77's capture (verified). My live
re-open on 2026-11-05: HTTP 200, 30406 bytes — exactly the manifest's recorded raw-page size —
and all seven quotes present in the live text after tag-strip/entity/whitespace normalization.
F54 is the genuine next frontier id (F53 last admitted; census rows=53). The F54 row itself is
unfrozen (objection 7).

## Part B — numbered objections

**1. HIGH — C1 P3: the X2 and K-M8 kills as specified are observationally impossible; the
mechanism that can produce them is named nowhere.**
Evidence: I re-derived all three r77 survivors from the reference bytes
(`.ufo/waves/round-77/c1-amended-reference.py`, sha 18bfc439… verified) and each prints
`selftest cases=12 failures=0`, rc0, no FAIL — X1 (`clean_ok = True`), X2 (gate-consume
condition → `True`), K-M8 (relabel expr → `True`). All three mutations leave every other
assertion's observable state identical: the conditions are pure reads of already-correct state
(`got8u`/`got8p`/`out6`/`ret6` unchanged), `gate-checkids` compares only the id set
(MutC1.md:46), and the kill rule's NOT-DERIVED clause forces the successor to keep the anchor
lines verbatim — which forecloses restructuring the consumption into the conditions. Therefore
no state-reading assertion can fail under X2/K-M8; the only in-process mechanisms that work are
(a) an evaluation/invocation witness carried inside the condition or the limb (kills X1; kills
K-M2 robustly), and (b) a source-pinned check asserting the literal condition text in
`__file__` (kills X2 and K-M8). Neither is named in claims.json P3 or c1-mutant-transforms.md,
and the table's expected-verdict cells are unsatisfiable as written: X2's "an assertion FAIL on
a case-6 polarity check" cannot happen (a case-6 polarity check evaluates correct state under
X2), and K-M8's "FAIL in relabel-detection or gate-checkids" cannot happen (relabel prints ok;
ids unchanged). The r77 routed suggestion (MutC1.md:58: gate-checkids "requires each check's
detail or verdict to be consumed") is also insufficient — under X2/K-M8 verdict and detail are
the correct values. Smallest safe correction (allowed pre-scoring; the freeze's own rule freezes
the table only "after any seat has scored"): amend c1-mutant-transforms.md to name the
mechanism — e.g. a source-pin gate check `all(pin in open(__file__).read() for pin in
PINNED_CONDITIONS)` over the three anchored condition strings, plus a limb call-counter for
X1 — and rewrite the X2/K-M8 expected-verdict cells to that site. Without it, the most natural
successor (r77 shape + TMPDIR case) fails P3 exactly as round 77 did.

**2. MEDIUM — C1 P6 is overbroad and mechanically self-failing.**
P6 says "SKILL.md and corpus/instruments/README.md rows pinning 'selftest cases=6' move to
'cases=13'". README.md also pins `selftest cases=6` for two other instruments (:851
frontier-recheck-count, :887 kill-rule-check) which must stay 6; SKILL.md:1151 pins cases=61.
The kill rule is mechanical ("Any of P1–P7 false … = NOT VERIFIED"), so a literal verifier
greps, finds unmoved `cases=6` rows, and fails C1; an executor following P6 literally corrupts
two other instruments' pins against R113. Smallest correction: P6 names the two recheck-cwd rows
(SKILL.md:982, README.md:354).

**3. MEDIUM — C2's "claims ONLY those seven clauses" is enforced by no predicate.**
B0–B7 check the seven quotes, the census, the registry, the binding and the byte-absence of the
seven quotes elsewhere; nothing pins the entry's bytes or its claimed-clause set. An entry that
additionally claims Q12 (or Q07/Q08) passes every B-predicate: B6 greps only the seven claimed
quotes, and Q12's sentence exists in no other knowledge file. The kill rule freezes the quotes
but not the entry. Smallest correction: add a predicate that the entry's claimed-clause markers
enumerate exactly {Q01,Q02,Q03,Q09,Q10,Q11,Q13} (or pin the entry sha256 in the round lesson at
landing).

**4. MEDIUM — C2 claims the thresholds without their on-page qualifier (QUALITY Q4 pressure).**
Q10/Q11 are claimed; S112.txt:170 ("These numbers can vary slightly because of threading and
the page size may change in the future.") is not, on the grounds that F51 holds its v1/query
form (S108:136). The batch page's own thresholds are therefore entered without the caveat the
page itself attaches to them. Smallest correction: require the entry, inside the threshold
clauses, to cite the qualifier (S112:170 as the page's sentence, or F51 Claim 5 as held ground),
and require the R125 per-clause sweep verdicts for Q10 and Q13 (partial F51-Claim-5 overlap:
1,000 number; next-request token rule) to be recorded, as B6 already contemplates.

**5. LOW — control receipts do not carry what claims.json cites them for.**
c2-donothing-counters-r78.txt contains no `FRONTIER-CENSUS` line — it is a filtered excerpt
(three `PASS F5x` lines + `entries=56 pass=56`) — while claims.json's control description and
B3's before-state cite "FRONTIER-CENSUS rows=53 admitted=53 registry=112" from it. The line is
real (I re-ran the instrument), but the receipt cannot evidence it. Relatedly, the
c1-donothing receipt's tmpdir-parent case shows scratch dirs created inside the committed
controls directory itself (TMPDIR set to `.ufo/waves/round-78/controls/` when the receipt was
generated; leftover=0, so nothing persisted). Smallest correction: regenerate the C2 receipt
with full output; generate receipts with TMPDIR in scratch.

**6. LOW — C1 statement enumeration is arithmetically wrong.**
"The selftest grows to thirteen cases: the six base cases, the twelve-check r77 gate set, and a
TMPDIR-refusal case" reads 6+12+1=19; the twelve include the six (reference prints
`selftest cases=12 failures=0` with the six base cases inside), so 12+1=13 — P1's number is
right, the enumeration is not. Frozen-text noise; no correction needed beyond awareness.

**7. LOW — the F54 frontier row is unfrozen.**
B3 needs `rows=54 admitted=54`, which requires a new corpus/README.md frontier row; no F54 row
exists anywhere at freeze (grep over corpus/README.md, PROVINCE.md → none), and no draft text
is pinned in the wave dir. The row's wording is the admission's visible claim surface and is
authored at landing. Smallest correction: draft the F54 row in the wave dir (F53-row shape,
README.md:1187) before the landing.

**8. LOW — P5's "round-78 red-before bytes" is ambiguous and uncommitted at freeze.**
The red-before receipts that exist are round-77 artifacts (RevengerInherited-run-X1/X2 .txt,
MutC1.md — all present and consistent with my re-derivations); no round-78 red-before re-run is
committed in the wave dir, and no round-78 candidate bytes exist to re-run against. Smallest
correction: P5 names `.ufo/waves/round-77/c1-amended-reference.py` as the red-before bytes.

**9. LOW — C2 motivation cites a dangling pointer.**
"(round-77 planned-after item 2 …)" resolves nowhere: grep over corpus/lessons/round-77.md, the
fleet report (.ufo/reports/round-77/kasegi.md) and the round-77 wave dir finds no planned-after
items. The substantive anchors exist (round-77.md:13 flip line; :51 R-77-C; SCORECARD :2957),
so this is a provenance-label defect, not a substance gap. Note the r78 narrowing additionally
diverges from the flip line by dropping Q04/Q05/Q06 — a justified improvement (pointers, not
ground), but the divergence deserves its one-line justification in the lesson, which the claim
statement already supplies.

**10. LOW — the new TMPDIR-refusal limb ships with no named mutant or red-before.**
The eight-mutant set covers the case-6 RESULT limb and gate machinery only; a refusal-neutering
transform (condition → pass) is unnamed, so the 13th case's kill power is asserted, not
demonstrated. Smallest correction: add one refusal-mutant to the table pre-scoring, or route it
in the lesson's known-limits paragraph.

Positive verifications worth recording: all eight transform anchors are present verbatim in the
reference bytes today (regs statement, K-M2 body, K-M3 case-6 line, K-M4 negpolarity check,
K-M5 both-headers call, X1 line, X2 check, K-M8 expr) — derivability holds if the landing
preserves them; P7's surface holds on base bytes (exactly 1 `subprocess.run`, 1 `bash -c`, no
`/tmp` literals); the r77 `cases=12` pin indeed never landed (no occurrence in SKILL.md/
instruments README); B2 mechanics clean; capture-binding already binds the round-78 manifest at
the freeze commit.

## Part C — verdicts

**C1 (depth:verifiability): weak as frozen — one amendment from sound.**
Red-before is honest (I reproduced all three survivors), the controls are real, the axis shape
is R58-conformant with long precedent, and P1/P2/P4/P5/P7 are mechanically verifiable. But P3
as frozen directs the successor toward impossible kill sites for X2/K-M8 and names no workable
mechanism — the same failure mode that sank round 77 — and P6 is literally self-failing. The
one change that makes it sound: amend c1-mutant-transforms.md (pre-scoring) to name the kill
mechanism (source-pin gate check over the three anchored condition strings + limb call-counter)
and fix the X2/K-M8 expected-verdict cells, and scope P6 to SKILL.md:982 + README.md:354.

**C2 (coverage): sound.**
New claim, not a re-declaration: the claimed seven are the r77 gate's prescribed residue plus a
justified further exclusion of three pointer quotes; all seven are located on their declared
lines (prerecheck receipt + my snapshot reads), byte-absent from every other knowledge entry,
batch-specific against F51, and the source is live-verified today (HTTP 200, byte-size match,
7/7 quotes). The held-score shape matches accepted r75 practice. Harden, do not reject: add the
entry clause-set predicate (objection 3) and the threshold-qualifier requirement (objection 4);
note the F54-row draft (objection 7) for the L1.

No routed-defect edits made by this seat; the report is the deliverable. Files written:
`.ufo/waves/round-78/w1/CriticClaims.md` (this file) only.
