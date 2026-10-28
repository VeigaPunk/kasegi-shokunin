# CritClaims — attacks on the frozen round-42 claims (wave 1)

Seat: CritClaims (UFO-FSD critic, receipt-only). Base 5053a7f46de35784cff4b56756906e9014a38276, lane tip 0566bd6 at review time; claims.json sha `EF3B` (13,072 bytes) read in full including the untruncated C1/C2 predicate and kill-rule lines. No installs, no network, no writes outside scratch + this receipt. Scratch `/fast/scratch/hyaku/kasegi-r42/CritClaims` removed before yield.

Per-attack verdicts below: **A1 DEFENDED · A2 ROUTED (one wording hole + one kill-scope asymmetry) · A3 DEFENDED · A4 DEFENDED**.

## A1 — can a do-nothing control reach any after-state? DEFENDED

Both claims' after-states contain expansion atoms a do-nothing cannot reach; the only atoms already true are stationary no-harm guards, which is the correct use of a control.

C1 evidence (independently verified):
- `git cat-file -e 5053a7f:corpus/instruments/r42-closure.sh` → `fatal: path ... does not exist` — suite **absent at base**.
- `git cat-file -e HEAD:corpus/instruments/r42-closure.sh` → absent at lane tip 0566bd6 too (wave-1 suite still being built).
- A do-nothing therefore has no instrument that can print `closed=13/13` (control receipt records exit 127), no selftest lines, and no receipt — every after-atom unreachable.

C2 evidence (live re-verification against the working tree, matching `c2-controls/before.txt`):
- frontier rows 24 (`grep -cE '^\| F[0-9]+ \|' corpus/README.md` → 24), no S064+ rows, knowledge 60 (`ls corpus/knowledge/*.md | wc -l` → 60), `grep S064|S065` in SOURCES.md/README.md → 0 hits.
- `python3 corpus/instruments/frontier-recheck-count.py` → `entries=27 pass=27 exit=0` (F24 PASS present, no F25).
- `python3 corpus/instruments/capture-binding-check.py` → `records=55 bound=55 unbound=0` (pre-existing `orphan=S040-live.txt` noted — not a new W/E, unbound still 0).
- `python3 corpus/instruments/recheck-audit.py --quiet` → `expected=60 missing=0 unexpected=0 exit=0`.
- `census-before.txt` shows the only warnings are the two standing W04s (S028/S029), exit 0.
- Stationary atoms (do-nothing already "reaches" them): census exit 0, `unbound=0`, and **measure 1.000** — the formula `(20+F_ADM)/(20+F_TOT+QUEUED)` reads 44/44 = 1.000 at base and 45/45 = 1.000 after F25 (r41 lesson L85 documents the 44/44 reading). These are no-harm guards in the kill rule, not expansion gates; every delta atom (24→25, 63→64, 60→61, 27→28, 55→56, 60→61) is unreachable without work. Correctly designed: an after-state need not be all-delta; it needs at least one atom a do-nothing cannot reach, and both claims carry several.

One execution caveat (recorded, not relied on): my own re-run of `r41-closure.sh --export-ref 5053a7f` was killed at the 300 s shell cap with no output captured. The committed control transcript (`closed=8/12 exit=1`, I1/I3 alive) plus the suite-absence evidence stands on its own; wave-2 RevC1Counters is assigned to re-run it.

## A2 — C1 kill-rule self-consistency: ROUTED

**A2a — does replaying-to-rejection actually close a defect? DEFENDED.** The mechanism is coherent and a real fix for the r39-r41 failure mode it names. Per the frozen predicate + `ExecReplayHarness` spec in `wave1-dispatch.json`: `replay_defeat` reconstructs the mutated input state of each committed artifact and requires the CURRENT check limb to reject it (0 iff rejected). Because the kill clause is artifact-vs-current-bytes ("shows the CURRENT suite bytes accepting"), a replay limb makes the suite's own committed attack evidence self-falsifying forever — the exact mode that fired in r39-r41 ("committed fixtures showed checks passing while their named defects were present"). The pairing `positive=pass` + `mutants=<ok>/<n>` grading also blocks the cheap fixes: an always-red limb fails its positive, an always-green limb fails its mutants. The harness can't self-certify because the artifacts are committed bytes, not suite-generated fixtures. That is defect closure at artifact level plus a live falsification path — not mere regression bookkeeping.

**A2b — can an in-family escape evade the F-* enumeration? Partially YES → ROUTED.** Two defects in the enumeration itself:

1. **F-TOKEN boundary class is under-specified (wording hole, concrete escape).** The frozen text: "a `closed=<n>/<m>` or `failures=<k>` value is read only as a whole token bounded by non-digit, non-slash characters." Letters are non-digit non-slash. So `closed=13/13x` presents `13/13` as a whole token bounded on the right by `x` — a compliant J2 limb *must accept it*, yet `13/13x` is exactly the mangled-value class F-TOKEN exists to kill (the r41 defeat was `closed=10/100` — `RevC1Counters.md` r41: `mutant=mangled-value-token rejected=0`; the fix was meant to require whole-token reads). A suffix/digit-extension to the RIGHT is covered (digit), a `/` run is covered (slash), but letter-adjacency is not: `closed=13/13x`, `closed=13/13a`, `failures=0x1`. Whether a committed artifact showing `13/13x` accepted then *fires* the kill clause depends on calling it "in-family" (intent) vs literal-compliant (spec) — the enumeration's own wording admits it, so the strongest reading is that an attacker can land an in-family escape the freeze legitimises as out-of-family. Smallest safe correction: bound the token by `[0-9/]` complement i.e. *non-alphanumeric-non-slash*, or freeze one letter-adjacent mutant into J2's replay set.
2. **Kill-clause family coverage is narrower than the predicate's repair set (asymmetry, not contradiction).** The artifact-kill clause enumerates only F-EVID/F-TOKEN/F-TABLE/F-DECL/F-SCAN/F-BIND/F-FLIP (J1-J7). But the predicate also repairs J8 (F-RCPT receipt forgery), J9, J10, J11 (F-CORR duplicated Correction block), J12, J13 — and `claims.json`'s own design lesson concedes "new attack findings outside the seven families are routed defects, not kill clauses." Concretely: a committed artifact showing a forged-payload receipt accepted (F-RCPT escape) or a fresh duplicated Correction block accepted (F-CORR escape) does **not** kill the claim under the frozen text — those are routed defects only, even though both are named "repaired checks" in the same predicate. Consistent with the r39-r41 precedent, but the enumeration is narrower than "the routed queue it claims to close" (the r41 verifier §5 item 1 explicitly routed D-r41-1). Also note the wording tension "EVERY repaired check carries a REPLAY limb" (summary) vs kill clause "the committed replay limb of any J1-J7 check" — J8-J13 limbs' replay limbs are neither specified nor kill-covered.

Neither defect contradicts the kill rule (self-consistency holds: no clause is unsatisfiable or mutually exclusive), so this does not overturn the freeze — it is routed repair material: tighten the F-TOKEN boundary class, and decide explicitly whether F-RCPT/F-CORR escapes should be kill-level or stay routed.

## A3 — is C2's topic axis really coverage (new surface), not quality re-scoring? DEFENDED

- The after-state is pure expansion: frontier 24→25, registry 63→64, knowledge 60→61, harness 27→28, binding 55→56, audit 60→61. Nothing re-grades an existing row; quality/verifiability scoring is untouched (C1 holds 4, coverage holds 8 — no score re-derivation claimed).
- Measure formula stays native to the axis: `(20+F_ADM)/(20+F_TOT+QUEUED)` → 45/45 = 1.000 requires F_TOT=25 admitted with QUEUED=0 — the number rises only because a new topic exists.
- New-surface check I ran: `grep -rinE 'osv\.dev|cveawg|CVE Record Format|cvelistV5|CVE Services'` across `corpus/` → **zero lane coverage** of either lead-class document. "CVE Record" hits exist only as subject-matter *inside* held documents (CNA Rules S030/S031 prose, CWE-top25, CVD stage 4, EPSS) — none is the CVE Record Format spec itself; the KEV row (S052/F18) is a catalog feed, not a record-schema document. So both named lead-class candidates (OSV schema, CVE Record Format) are genuinely un-held and distinct documents — the "already covered" kill clause is a real constraint, not vacuous.
- D-r41-2 closure is structurally enforced: the kill clause requires a screened reject (reason + flip + URL + date + ≤25-word located quote), so the lead screen can't be a one-sided admit.
- F24/RFC 9116 correctly stays parked (open L0 scope question from r41 is unanswered at freeze) — the claim expands on a different lead instead of re-litigating the parked topic.
- Honest caveat (not a defect): the lead class "machine-readable vulnerability-data standard" is a class the lane already samples (F21 CSAF, F22 VEX guidance, F23 CycloneDX, F24 security.txt), so F25 is another topic in a populated class rather than a new surface *category* — still new surface by the lane's own frontier-row metric.

## A4 — are C1 and C2 causally separable? DEFENDED (with named guard couplings)

- Counting commands are orthogonal: C1 counts suite behaviour (export/selftest/refusal lines); C2 counts corpus tallies (rows, entries, harness, binding, audit, census). C2 never alters suite bytes; the new `r42-closure.sh` is not a SOURCES/README/knowledge/manifest object, so C1 never alters C2's tallies.
- C1's J6 replay runs capture-binding over *scratch* manifests and J7 replays status-flip mutants over copies — C2's real S064 manifest/row additions do not collide with the replay limbs.
- Named couplings that are shared-fate, not conflation (all consistent, but wave-2 should know they exist): **J12** spans "no tracked deletions in corpus paths" — a C2-side deletion would fire *both* claims (C2's kill rule carries the same clause); **J13** quiescence means every C2 artifact must be committed inside J before the receipt runs, so C1's receipt cannot certify until C2's work lands (sequencing dependency, not causal mixing); **J4** declared-blocks must cover C2's new round-42 artifact paths too.
- PROVINCE.md verified real and amendable: tracked at lane root, `r41 Frontier amendment` F24 block present at EOF matching the r38-r41 append convention the F25 amendment must follow.

## Routed items for the queue

- **R-CRIT-1 (F-TOKEN wording hole):** boundary class "non-digit, non-slash" admits `closed=13/13x`-class letter-adjacent mangled values. Probe candidates for wave-2: `closed=13/13x`, `failures=0x1`, `closed = 13/13` (separator spacing), `closed:13/13` (key separator). Smallest correction: bound by non-alphanumeric-non-slash, or add a letter-adjacent mutant to J2's committed replay set.
- **R-CRIT-2 (kill-scope asymmetry):** F-RCPT (J8) and F-CORR (J11) are predicate-named repairs outside the seven-family artifact-kill clause; escapes there route rather than kill. Decision item: extend the artifact clause to all repaired checks or record the intentional boundary.
- **R-CRIT-3 (replay-limb coverage wording):** "EVERY repaired check carries a REPLAY limb" vs kill clause "J1-J7" — J8-J13 replay limbs are unspecified; either specify them or narrow the summary wording.

## Provenance

Commands run (all read-only against the lane; cwd was my scratch or `-C`-flagged absolute paths): `git log --oneline -8`, `git status --porcelain`, `git cat-file -e` on r42 suite at base+HEAD, `grep -cE` frontier/SOURCES counts, `ls corpus/knowledge/*.md | wc -l`, `python3 corpus/instruments/frontier-recheck-count.py`, `capture-binding-check.py`, `recheck-audit.py --quiet`, `score-gap.py` (context), `find`/`git ls-files` for PROVINCE.md + declared-blocks, `grep` OSV/CVE-record overlap scans, `grep` r41-closure.sh selftest/replay structure + I3 defect lines (438-459, 973), `grep` wave1-spec replay-limb/attack-seat prompts, `bash r41-closure.sh --export-ref 5053a7f` (timed out 300 s — recorded, not relied on), `bash scripts/hyaku/disk-guard.sh status` (green: /fast/scratch 27%). Read: claims.json in full incl. raw lines 27-28 and 48-49; c1-controls/do-nothing.txt; c2-controls/before.txt; census-before.txt; corpus/lessons/round-41-verifier-spotcheck.md §5 (L125-155); `.ufo/waves/round-41/wave2/RevC1Counters.md` head; PROVINCE.md tail; sibling receipt RevRegistry.md for format. Tools installed: none.
