# Round 47 — counter errata and era-bound instruments

Seat: R47SrErrata (scribe, wave 1). Axes: **depth:verifiability**, **coverage**.
Destination after L1 integration: `.ufo/waves/round-47/counter-errata.md`.
All evidence paths below are relative to the kasegi lane. This is an evidence-backed draft, not a receipt of the integrated round-47 tip. No counters, batteries, live fetches or product checks were executed by this seat.

## 1. Era statement (M46-6)

A past gate's green receipt describes its measured tree, not an invariant of every future tree. Do not weaken an old gate until it accepts a new era, delete the historical receipt, or treat an expected era mismatch as proof that the new repair is wrong. Equally, “expected-moved” excuses only identified obsolete requirements; it does not excuse an unexplained failure of a current requirement.

Authority: `corpus/lessons/round-46.md:96` (M46-6): “an instrument that pins era bytes needs its exemption story stated at freeze time, not discovered when a later round trips it”. The same row records the decisive contrast: v1.3 C2 was green at `eb874bc` but `5/7` at the round-46a2 tip.

### r46-f29-gate.py — round-46a2 F29 admission, not round-47 acceptance

Historical reproducibility tree: export of round-46a2 tip **`4cdcf7bdea8bea06705de752a2796d4e3aab0242`**. Preserve the historical instrument and snapshots there. The historical run in `.ufo/waves/round-46/attempt2/controls/final-measure.txt:20-29` printed `f29-gate fixed=7/7 exit=0`; its do-nothing base run at :10-19 printed `fixed=1/7 exit=1`. The receipt self-stamps `c8641e7a…` (:1), not `4cdcf7bd`; `corpus/lessons/round-46-verifier-spotcheck.md:45-47` records that the lane bytes outside `.ufo/waves` were identical through the judged tip. This is historical receipt plus recorded equivalence, not a fresh replay by this seat.

Why era-bound:

- `corpus/instruments/r46-f29-gate.py:74-88` hard-codes the round-46-a2 S074 manifest/capture, body `1..42`, snapshot length 42, capture sha256 `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`, and manifest sha256 `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f`.
- H1 requires exactly 29 admitted frontier rows (:180-199); H2 requires S074 provenance/recheck and S074-cited content (:18-27, :91-94, :217-238); H5 recognizes `S074.txt` citations (:309-310). H6 requires exactly 66 knowledge files and the era names/content pins (:340-350).
- D7 deliberately re-anchors the F29 entry to **S076**, whose committed-instrument capture is 610 lines with body **558..600** and `supersedes_capture_of: S074` (`corpus/source-snapshots/round-47/manifest.json:78-96`). Round-47 C1 requires zero old S074 citations; C2 requires 30 rows and 67 entries (`.ufo/waves/round-47/claims.json:13,24,37,44-46`). These cannot satisfy the old S074-only citation and 29/66 era requirements.

**At the repaired round-47 tip, the old F29 gate is expected to read red BY DESIGN.** [INFERENCE from the cited predicates and intended landing, not an executed final reading.] In particular H1/H2/H5/H6 have obsolete requirements. Do not predict every other limb's final result: S074 retention, row edits and other changes need their own reading. Merely keeping S074 snapshot bytes does not keep the repaired entry eligible for the old gate. A round-46 `7/7` must therefore be captioned “historical, round-46a2 era export”, never “passes at the current round-47 tip”.

### r46-c1 / r46-c2 — preserve the actual exemption and version history

**Assignment wording requiring correction:** “r46-c1/c2-gate v1.3 content pins”. The inspected C1 header actually says **v1.2** (`corpus/instruments/r46-c1-gate.py:2`); C2 says **v1.3** (`r46-c2-gate.py:2-4`). C1 does not have C2's global knowledge-directory content pin. Do not silently describe both as v1.3 or claim both necessarily turn red at round 47.

- **C1:** round-46a2 export `4cdcf7bd…`, baseline export `914ca0b6956f01d87b2e252ffad06fe74ec5d9ba`. The historical run printed `c1-gate fixed=7/7 exit=0`, while baseline against itself printed `fixed=1/7 exit=1` (`attempt2/controls/final-measure.txt:41-61`). Its re-grounded-entry anchors must remain byte-identical to baseline, and still-gated entries remain byte-identical (`r46-c1-gate.py:28-36`). These are the actual preservation constraints. Whether a round-47 edit invalidates them is not measured here; no general automatic-red claim is made. Retain the historical baseline when reproducing this historical measurement.
- **C2 v1.3:** at the **round-46a2 export `4cdcf7bd…` its reproducible result is already `5/7 exit=1`, not `7/7`**. Historical receipt `attempt2/controls/final-measure.txt:74-84` identifies G1 (28→29 rows) and G6 (65→66 entries). The green era is the earlier **`eb874bc` export with v1.3 counter bytes**, explicitly receipted at :62-73. The newer instrument bytes matter: the record states they were the only difference in that earlier era fixture. Do not promise `7/7` from untouched older counter bytes, or from the round-46a2 tree.
- The v1.3 ledger amendment exempted `considerthese-proposals-ledger.md` **content**, retained its name pin and minimum 30,696 bytes, and re-derived the digest over 61 non-exempt files. The two C1-re-grounded files were already content-exempt. Exact record: `.ufo/waves/round-46/attempt2/counter-errata.md:47-58`; implementation: `r46-c2-gate.py:35-38,74-75,367-378`. This was not a blanket future-edit exemption.
- Round-47 F30's corresponding exemption story was declared at freeze: the ledger remains exempt with a 40,843-byte floor; the F29 entry name stays pinned but its content is exempt to allow C1's in-place S076 re-grounding. The F29 content exemption does **not** impose a never-shrink byte floor; C1 separately requires the 145-line repair. Evidence: `r47-f30-gate.py:54-62,97-99,360-362` and frozen C1 `claims.json:13`. The other 64 pre-existing entries remain content-pinned. This new exemption does not retrospectively rewrite r46 gates.

## 2. Round-47 H4 erratum: five distinct anchors, not seven

**Conflict verbatim:** the F30 docstring says “>= 7 distinct anchors” (`corpus/instruments/r47-f30-gate.py:43-46`), while its implementation says `len({q["anchor"] for q in qs}) >= 5` (:313).

The operational H4 distinct-anchor floor is **5**, decided at freeze, disclosed here; it is not a post-score relaxation to make a failing tip green. Freeze record `.ufo/waves/round-47/freeze.txt:5,9-10` pins the gate, manifest and S075 capture; the frozen gate digest recorded there is `563d52b827acf3afe269a0079f76ba7b208cefed69c14ff24ea47b86030e6b3b`. This seat read the checked-in implementation and freeze record, but did not independently compare a freeze-commit blob or hash bytes.

Plain re-derivation independent of H4: `corpus/source-snapshots/round-47/manifest.json:20-74` declares body **20..27** (eight lines), ten distinct quote texts and anchors **21, 23, 24, 24, 24, 24, 25, 25, 25, 26**. Their distinct set is **{21,23,24,25,26}**, count **5**. Five is the maximum represented by these frozen ten quote records, not a mathematical maximum for arbitrary quotes from an eight-line document. It would be misleading to assert that any eight-line body can have at most five anchors. The retained floor rejects anchor collapse without requiring invented additional manifest locations.

H4 still requires the pinned manifest and recheck tool, source-recheck success, sha256 OK, >=8 OK quote records, pairwise-distinct quote texts equal in number to OK records, and all five frozen cores (:296-317). “Five anchors” is not “five quotes”, and it is not the complete F30 admission predicate. The docstring discrepancy remains an explicit textual defect; this seat does not edit the frozen instrument. Any L1 documentation correction must preserve this disclosed provenance and be logged, not claimed as an unchanged historical file.

## 3. New-tip re-derivation route (commands supplied, NOT RUN)

Use the frozen round-47 instruments against explicit tree exports, not the era-bound round-46 admission counter. Set `TOOL` to the freeze export, `TREE` to the integrated candidate, `BASE` to export of `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`, and `WORK` to an explicitly owned scratch directory. For this seat any export/work directory would have to be below `/fast/scratch/hyaku/kasegi-r47/R47SrErrata/`; no scratch was created.

```sh
python3 "$TOOL/corpus/instruments/r47-routed-defects.py" --root "$TREE" --baseline "$BASE"
# target: routed-defects total=11 fixed=11 unresolved=0 exit=0
python3 "$TOOL/corpus/instruments/r47-f30-gate.py" --root "$TREE" --work "$WORK"
# target: f30-gate fixed=7/7 exit=0
```

Independent plain second measures, from the candidate lane root (expected values are targets, not observed results of this seat):

```sh
grep -c 'to append' corpus/SOURCES.md                       # 2 -> 0
grep -c '```' corpus/SOURCES.md                            # 4 -> 0
grep -c 'all 42 lines are body prose' corpus/knowledge/github-repository-security-advisories.md # 1 -> 0
grep -c 'S074.txt:' corpus/knowledge/github-repository-security-advisories.md # 54 lines/59 instances -> 0
wc -l corpus/knowledge/github-repository-security-advisories.md # 145 -> 145
grep -c 'supersedes S074' corpus/SOURCES.md                 # 0 -> 1
grep -c 'docs.github.com/en/rest/security-advisories' corpus/SOURCES.md # 0 -> 1
grep -cE '^\| F[0-9]+ \|' corpus/README.md                 # 29 -> 30
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md # 74 -> 76
find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l      # 66 -> 67
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-47/manifest.json --source S076
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-47/manifest.json --source S075
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$PWD/corpus/SOURCES.md"
```

A zero-match `grep -c` prints 0 and exits 1; that is expected, not a harness failure. Count measures alone cannot establish semantic truth. Read SOURCES' rendered Search log/Registry changes to confirm the original three bullets really landed outside fences. Read the repaired F29 sentences against S076 body 558..600 (CVE request before fix-version discussion; only two cases permit no fix-version; not “all 42 lines are body prose”). Locate every quoted span against its own cited range, rejecting chrome, and read the REST-API lead/ZDI reservation/S068 precision notes. For C2 locate each quotation in S075 body 20..27, check F02/F15 distinction, researcher actionability and the rejected generalization, and reopen the live policy for the independent closure. The broad ZDI mention count is contextual only: old advisory-index mentions do not prove policy coverage (`claims.json:36,47`). The companion plain-measure script is another seat's draft, not an artifact this seat has executed or certified.

## 4. Controls, limits and handoff

Do-nothing control: **base `fc8e0af…`**, not a partially landed freeze tree. Existing receipts `.ufo/waves/round-47/controls/c1-base.txt:1-13` print `routed-defects total=11 fixed=0 unresolved=11 exit=1`; `c2-base.txt:1-9` prints `f30-gate fixed=1/7 exit=1`. `freeze-check.txt:1-4` records both before-values accepted (`claims=2 base_ok=2 exit=0`). At freeze C1 still has zero fixes; F30 is only `2/7` because capture H4 now exists, not because F30 was admitted (`claims.json:29,50`). Thus capture availability alone does not beat the admission control. Replay current candidate and base with the same frozen tools to discriminate them; no new replay is claimed here.

Known mechanical limits remain **C1 35 mutants/19 caught/16 uncaught; C2 21/3/18, baseline_failures=0**. The 34 survivors are disclosed gaps, not equivalent and not closed (`claims.json:18,41`; `controls/freeze-controls.txt:1-5`). The 43-case tree selftest is an existing receipt, not a run by this seat. Historical round-46 `uncaught=0` findings do not transfer to round 47. No gate score establishes source truth, novelty, closure or promotion by itself.

Touched surfaces: only this report and owned empty `w1/R47SrErrata.draft/`. No product/instrument edits, git/jj mutation, commits, installs, background jobs, delegation or runtime invocations for probes. No scratch directory was created, so none remains to remove. Out of scope: L1 integration/commit, final-tip measurement, wave-2 attacks, live-source closure, fleet/sibling/adoption changes.

Self-evaluation (not a gate): accuracy 4 (freeze hash not independently recomputed); completeness 4 (final-tip execution is intentionally absent); clarity 4 (historical version corrections require context); actionability 4 (explicit export/work prerequisites must be supplied by the integrator); conciseness 4 (detail retained for auditable provenance). Mean 4.0. Highest-impact improvements belong to integration: bind actual candidate revision and record its receipts, then resolve the docstring conflict without disguising the frozen five-anchor implementation. A reader should agree these limits are explicit rather than claimed passes.

### Integration receipt requirement and stale-report pointer

Companion critic inventory: `w1/R47CritErrata.md:24-72` enumerates the historical report sentences and supplies append-only naming errata. In particular, the filed report's bare “`r46-f29-gate.py --root .` = 7/7” must be restricted to the historical measured revision, not left as a current-root promise. This is a sibling finding, not an independently inspected fleet-report assertion by this seat. Its recorded later rejected-harmed ruling is not reversed by these proposed repairs.

At integration, the L1 should record the actual candidate revision, exact old gate bytes, explicit scratch `--work`, all seven old F29 limb lines, summary and actual exit code alongside both new gate receipts. D7 alone invalidates H2/H5; F30 independently invalidates H1/H6. Classify any additional red limb separately (especially S074 H3/H4); do not replace that bounded receipt with a generic era waiver. None of these prospective checks has passed merely because this draft names it.
