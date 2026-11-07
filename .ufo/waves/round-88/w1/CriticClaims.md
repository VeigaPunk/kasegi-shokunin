# Round 88 — CriticClaims (hostile closure review of the two frozen claims)

Seat: CriticClaims (attack). Base `6beead9148945fa695cf3139e8fc9d8e91cc5fd0`; freeze
`7f2ebebf7588ead4f4248478f18b989983e94b69`; C1 landing `fd33e1bfe26ad9af13c138feb87c9f222be957cb`;
C2 landing `b43dc2154bc09470da2209fb626021da3af3593e` (`landing.json`). Lane tip = `master` = the C2 landing.

Every measurement below was re-run by this seat on `git clone --shared` checkouts under
`/fast/scratch/hyaku/kasegi-r88/CriticClaims` (deleted after the run), never on the lane working tree, and
never over uncommitted bytes except where a receipt says so explicitly. The two clones used for P1 reported an
empty `git status --porcelain`. Receipts: `CriticClaims-receipts/` — each receipt names its command.
No lane file outside `.ufo/waves/round-88/w1/` was written.

## 0. Verdicts

| Claim | Verdict | Basis (re-run by this seat) |
|---|---|---|
| **C1** depth:verifiability | **VERIFIED** | P1 `KNOWLEDGE-METER-RESULT pass rc=0` (703/1754 → 742/1743, M1–M6/M8) on a pristine clone of `fd33e1bf`; P2 15/15 pins at both landings; P3 `changed=8 outside=0 verdict=PASS` |
| **C2** coverage | **VERIFIED** | P1 `CAPABILITY-CHECK-RESULT pass rc=0` (K1–K6) at `b43dc215`; P2 both instrument files byte-equal, SCORECARD row equal; P3 `changed=2 outside=0 verdict=PASS` |

All findings below are qualifiers and routed defects; none falsifies a frozen predicate, and none is a re-score.

## 1. (e) P1–P3 exactly as frozen

| Claim | Predicate | Re-run result | Receipt |
|---|---|---|---|
| C1 | P1 counter on a clone of the landing | `pass rc=0`; base 703/1754, after 742/1743, keys=50; M2 removed=50, M3 bad_lines=0, M4 bad=none, M8 no_shared_identifier=none, M5 none, M6 map sha `5a7314…7960` | `c1-p1-meter.txt` |
| C1 | P2 pins of all 15 `instruments` entries | 15/15 at `fd33e1bf` **and** 15/15 at `b43dc215` | `p2-pins-p3-scope.txt` |
| C1 | P3 scope | `LANDING-SCOPE from=7f2ebebf to=fd33e1bf changed=8 outside=0 verdict=PASS` (diff = 8 `corpus/knowledge/` files) | `p2-pins-p3-scope.txt` |
| C2 | P1 counter at the landing | K1 pass (`selftest_rc=0`, instrument sha `d73495…5417`, gate sha `8b6f84…c8e6`); K2 pass (`sts_files=2 oracle=2`); K3 pass (`scanned=1414,hits=0,allowed=18,unused_allow=0`); K4 pass (`missing=none extra=none sts_allow_rc=2 files_rc=1 files_hits=1`); K6 pass (`base_hits=6 new_caught_by_base=none`); K5 pass (`rows=1`) | `c2-p1-counter.txt` |
| C2 | P2 byte equality + row | scanner `d73495…5417` equal, allowlist `f9fbd7…afc82` equal, SCORECARD row equal (1 row) | `c2-p2-bytes.txt` |
| C2 | P3 scope | `from=fd33e1bf to=b43dc215 changed=2 outside=0 verdict=PASS` (SCORECARD.md + the scanner; the allowlist did not change) | `p2-pins-p3-scope.txt` |

Negative control on the scope tool: `from=to=freeze` gives `changed=0 … verdict=FAIL`, so P3 cannot pass
vacuously on an empty diff (`p2-pins-p3-scope.txt`).

## 2. (a) Can a do-nothing or cheaper control meet either predicate?

**C1 — do-nothing fails, and the honest work has no cheaper form.**
- base as after: `M1 FAIL 703/1754`, M2/M3 FAIL, rc=1 (`do-nothing-controls.txt`).
- The frozen half-map control is `722/1748` FAIL (re-read from `controls/c1-controls-r88.txt`).
- There is no cheaper *honest* path: M6 fixes the map bytes, M3 forces the landed text to be exactly that map
  applied verbatim, and M2 forces the set of removed tokens to equal the map keys. With the map fixed and M3
  fixing every line, the landing content has no remaining degree of freedom. A key swap also cannot preserve
  `742/1743`: with the recorded split of 39 new values and 11 pre-existing ones, swapping a mapped key for a
  forged one gives 742/1744 (new→new), 741/1743 (new→pre-existing), 743/1745 (pre-existing→new) or 742/1744
  (pre-existing→pre-existing) — the returned bare token always costs a denominator slot, so no 50-key variant
  lands on the target.
- **But the predicate as written is cheaper to satisfy than the claim reads:** I built a landing commit that
  carries 1 of the 8 repointed files (the other 7 left uncommitted in the clone's working tree) and got
  `KNOWLEDGE-METER-RESULT pass rc=0` **and** `LANDING-SCOPE … changed=1 outside=0 verdict=PASS`
  (`c1-p1-not-commit-bound.txt`). P1 reads the clone's working tree (`scope_files_tree`), not the commit, and
  P3 only reasons about the path list.

**C2 — do-nothing fails; the behavioural limbs are fixture-bound.**
- base as landing: K1 (sha), K4 (5 missing entries), K5 FAIL, rc=1 (`do-nothing-controls.txt`).
- I built a "scanner" whose two new shapes match **only** the literal fixture values that the candidate's own
  selftest and the counter's plant constants already contain (two mechanical substitutions: the GCS hex class
  and the Azure `_SIG` body; the `sv`-context wrapper untouched so the `sig`-without-`sv` negative stays
  silent). It passes **K1–K6**, `CAPABILITY-CHECK-RESULT pass rc=0`, instrument sha `d0433f6b…a076`
  (`c2-fixture-literal-mutant.txt`). Under the frozen P1 command it fails only K1, i.e. only the sha pin.
- Reading: K1's selftest is self-authored and K4's plant set is frozen, so no limb measures generality. C2's
  capability evidence is P2's byte equality plus a reading of the regex; the eight frozen mutants only cover
  over-detection and fixture misses, not under-generalisation.

## 3. (b) C1 — honest as an internal repoint, and what M8 actually proves

**Honest, and the accounting is exact.**
- Domain completeness (my independent enumeration through `resolve.collect` at base): **104** in-scope GONE
  sibling-entry citations = **50** mapped + **54** drift-excluded, residue **0**; the other 5 exclusions
  (3 not-a-knowledge-entry, 2 basename-not-unique) are outside the domain by construction
  (`c1-completeness.txt`). The per-entry counts also match the statement exactly (claim-gates 19,
  ops-invariants 10, mission-control 7, claim-package-contract 5, 9 entries ×1).
- The value is **forced by the key** (`<name>.md` → `corpus/knowledge/<name>.md` + the key's own anchor), and
  M4 enforces it (`bybase == [path]`, `INTERNAL`, key GONE at base). A repoint therefore cannot misdirect a
  citation to a different entry — a genuine structural strength, and it matches the lane's own LANE rule in
  `corpus/knowledge/citation-bases.md`.
- The score is declared held at 4, not moved. Correct and not inflated.
- Wording nit: **13 of the 50 keys are whole-entry** (no anchor), so M8 does not apply to them at all; the
  statement's "anchor in range, and every citing line sharing an identifier with the cited range" reads as if
  all 50 were anchored.

**M8 is a keyword-overlap test, not a content test.**
- Selectivity, measured on the 37 anchored keys: the share of *disjoint* ranges (≤5 lines) in the same entry
  that also pass M8 has **median 15 %**; three keys accept a majority — `claim-gates.md:24` 64 %,
  `mission-control.md:43-46` 61 %, `claim-gates.md:31` 56 % (`c1-m8-selectivity.txt`).
- For **22 of the 50 citing lines**, every shared identifier also appears in ≥8 knowledge entries (three in
  40+: `claim`, `manifest`, `sha256`). The asymmetry explains it: the citing side draws identifiers only from
  backticked/quoted spans and drops path-like spans, while the target side accepts **any** 5+ character word
  in the range.
- **A concrete admitted mis-anchor:** the "decision digest" row (the `decision_sha256` regex rule) is cited at
  `claim-gates.md:34`, but that rule is on **:35**; line 34 carries the `matched_grant_id` clause and the tail
  of the scope-signal sentence. M8 passes on the single word `decision`; the row's own specific identifier is
  absent from the cited line. The repoint makes this citation resolve and count toward the meter
  (`c1-m8-mis-anchor.txt`).
- Consequence: **resolving ≠ correct.** The 742/1743 move includes at least one citation a reader following it
  would find does not state the rule it is cited for. This does not falsify P1 — M8 is declared a "proxy" —
  but the word "content" in the limb's name overstates what it tests.

## 4. (c) C2 — real capability, and how far the sourcing goes

**Real, small, not bookkeeping.**
- Code delta (read): two compiled shapes, one scope clause, docstring. Base vs landed candidate on the *same*
  tree: `scanned=1405` vs `scanned=1414` — the +9 are `corpus/practice/<pkg>/evidence/` files, so the scope
  clause admits 9 real files (`c2-scope-delta.txt`). Candidate and base both `hits=0` on that tree.
- Base misses all 5 round-88 plant entries (`K6 new_caught_by_base=none`); the frozen mutants for
  over-detection fail as their receipts say (extra S005 / extra S007, re-read from
  `controls/c2-controls-r88.txt`), so K4 discriminates in that direction.
- Pre-freeze capture hygiene check: 3 captures scanned by both instruments, 0 hits
  (`controls/capture-scan-r88.txt`) — a hygiene check, not a discriminator.

**The sourced status holds only for the shape, not for its parameters.** All four manifest quotes re-locate
verbatim at their declared anchors (`sourcing-quotes.txt`): S126:424, S126:487, S127:404, S127:605.
- Sourced by S126: the parameter name and that anyone holding an active signed URL can use it. **Not sourced:**
  the 64-hex rule (S126 states no length).
- Sourced by S127: that `sig` is an HMAC-SHA256 encoded in Base64, and that a service-SAS URI carries `sv` and
  `sig`. **Not sourced:** the 40-character threshold, "either order", the `&amp;`/JSON-unicode separators, and
  the practice-evidence scope (which comes from the r87 routed defect, not from either capture).
- **Neither capture contains a positive the instrument can detect.** S126's one example signature is
  soft-wrapped across the capture's lines (and the candidate's own selftest `gcs-doc-wrapped` asserts the
  miss); S127's example carries a placeholder. The instrument's positives are its own synthetic fixtures —
  which is exactly why the fixture-literal mutant passes (§2).
- Measured false negatives beyond the docstring's "Known limits": soft line wrapping, a JSON-escaped slash
  inside the value, a base64url alphabet, and more than 20 parameters between `sv` and `sig`
  (`c2-scanner-limits.txt`).
- Precision note: the pattern has no host anchor, so it also fires on an account SAS, a user-delegation SAS,
  or any URL carrying `sv`+`sig` — wider than the SOURCES row's "service SAS on Azure Storage only".

## 5. (d) Separability — content-independent both ways

- The landed candidate scans the **C1 landing** and the **C2 landing** to the identical summary
  (`scanned=1414 hits=0`): C1's 8 knowledge files are not capture-class paths, so C2 cannot see them.
- The C1 meter on a clone of the **C2 landing** still reads 742/1743: C2 touches no knowledge file.
- C2's P3 names the C1 landing only as its `from` rev — a declared graph edge, not a content dependency.
- Receipt: `separability.txt`. Either claim could be judged without the other's substance.

## 6. Qualifiers (not re-scores)

1. **C1 internal repoint, score held at 4** — declared; corroborated.
2. **M8 is lexical** — median 15 % selectivity, 3/37 keys >50 %, 22/50 citing lines on generic words; one
   demonstrated admitted mis-anchor (`claim-gates.md:34`, rule on :35). Resolving citations are not thereby
   correct citations.
3. **C1 P1 is not commit-bound** — it reads the working tree; demonstrated pass with 7 of 8 files uncommitted.
   The actual landing is clean (porcelain empty), so the verdict stands, but the procedure must assert
   cleanliness or read committed blobs.
4. **The literal P1 command needs an explicit checkout** — `git clone --shared` checks out `master`, not the
   named landing. Benign this round only because `master` is the C2 landing and C2 left the knowledge scope
   untouched (meter still 742/1743 there).
5. **C1 scope saturation** — 55 distinct eligible bare sibling-entry citations in the same form remain GONE
   outside `corpus/knowledge/` (lessons dominate), and the lane's older authority
   `corpus/instruments/citation-ground-check.py` stays at 58 lane-bare → 58, unmoved (`c1-scope-outside.txt`,
   `citation-ground-crosscheck.txt`). The two counters measure disjoint classes; neither subsumes the other.
6. **C2's K1/K4 are fixture-bound** — a fixture-literal detector passes K1–K6; generality is carried by P2's
   byte pin plus reading, not by the behavioural limbs.
7. **C2 sourcing is shape-level** — thresholds, ordering, separators and the scope clause are engineering, not
   sourced; neither capture has a detectable positive.
8. **C2's P2 allowlist clause is vacuous** — the allowlist is byte-identical at base, r87 and the C2 landing,
   so "lands byte-equal" holds trivially for it.
9. **SCORECARD reproduction is weaker than the claim** — the published counting command omits
   `--instrument-sha256` / `--gate-sha256`, so it reproduces a check that a mutated instrument also passes.
10. **Two small sourcing errata**: the S127 SOURCES row's anchor `601` points at the revocation paragraph, not
    the signature table (638-639) or the example (603-605); the S127 HMAC quote is 29 words (the ≤25-word gate
    rule is written for the round lesson's Gate record, which does not exist — see D8).
11. **Dispositions 4 and 5 in `claims.json` point at `corpus/lessons/round-88.md`, which does not exist** in
    the tree (0 files, 0 tracked, no history). The disposition is unbacked as of the landing commits.

## 7. Routed defects (re-runnable)

**D1 — C1 P1 does not bind the commit.** Run the meter only on a pristine clone and record
`git status --porcelain` as empty in the receipt, or make the counter read `git show <rev>:<path>`.
Repro: `c1-p1-not-commit-bound.txt` (clone at the freeze, apply the map, commit 1 of 8 files, meter →
pass; scope check → PASS).

**D2 — M8 admits unrelated anchors on a single common word.** Next tranche: require ≥2 shared identifiers, or
one shared identifier with corpus frequency ≤3, or a shared identifier inside the target range's backticked
spans; then re-anchor the admitted keys that fail the stricter test. Repro: `c1-m8-selectivity.txt`,
`c1-m8-mis-anchor.txt`.

**D3 — C1 tranche scope.** 55 eligible bare sibling-entry citations remain outside `corpus/knowledge/`
(lessons, instruments, README, QUALITY, SOURCES); extend the map/meter or state the knowledge-only rule.
Repro: `c1-scope-outside.txt`.

**D4 — C2 counter cannot see under-generalisation.** Add a limb that generates a fresh signature value per run
(seeded RNG) and requires a hit, so a fixture-literal detector fails. Repro: `c2-fixture-literal-mutant.txt`
(mutant passes K1–K6 today).

**D5 — C2 known-limits list is incomplete.** Document soft line wrapping, JSON-escaped slashes inside the
value, base64url alphabets, and the 20-parameter window between `sv` and `sig`. Repro:
`c2-scanner-limits.txt`.

**D6 — C2 statement granularity.** Split "sourced" (parameter names and semantics) from "engineering"
(thresholds, ordering, separators, practice-evidence scope). Repro: `sourcing-quotes.txt`.

**D7 — SCORECARD row.** Put both sha pins in the row's counting command so the published reproduction equals
the claim's P1.

**D8 — S127 row erratum (low).** Anchor `601` → the signature table / example region (603-605, 638-639);
and if the ≤25-word rule is applied to manifest quotes, the 29-word HMAC quote needs trimming. Same class as
the r87 D-1 erratum.

**D9 — Unbacked dispositions (low).** `claims.json` dispositions 4 and 5 cite `corpus/lessons/round-88.md`,
which does not exist; commit the lesson or re-point the disposition.

## 8. Receipts (`CriticClaims-receipts/`)

`c1-p1-meter.txt` · `p2-pins-p3-scope.txt` · `c2-p1-counter.txt` · `c2-p2-bytes.txt` ·
`c1-m8-selectivity.txt` · `c1-m8-mis-anchor.txt` · `c1-completeness.txt` · `c1-p1-not-commit-bound.txt` ·
`c1-scope-outside.txt` · `citation-ground-crosscheck.txt` · `c2-fixture-literal-mutant.txt` ·
`c2-scanner-limits.txt` · `c2-scope-delta.txt` · `sourcing-quotes.txt` · `separability.txt` ·
`do-nothing-controls.txt`

## 9. Hygiene

No credential-shaped value was written into the wave dir: fixtures, mutants and planted repositories stayed in
scratch, and the receipts carry counts, paths, shapes, sha256 digests and source line numbers only. The mutant
receipt describes its two substitutions instead of reproducing fixture values. No scanner, counter or capture
snapshot was copied into the wave dir. No git/jj write in the lane (fixture commits only, inside `clone --shared`
checkouts with `-C` and asserted toplevels). No network access, no pacman, nothing installed.
