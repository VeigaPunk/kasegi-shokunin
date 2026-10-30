# R47CritErrata — era-bound F29 gate and report errata

Axes: **depth:verifiability**, **coverage**. Scope: read-only criticism; no integration, judgment, runtime dispatch, git mutation, installs, or production edits.

## Counterexample and finding

**An unexplained red historical gate remains a closure trap.** Correctly re-grounding F29 from S074 to S076 necessarily violates the old gate's source identity, recheck path and citation grammar. This happens even without adding F30. Merely saying “old instruments are era-bound” or correcting D1–D4 does not identify these D7-driven failures; merely explaining the F30 count increases also misses them.

Exact evidence, relative to lane root unless prefixed `fleet:`:

- `corpus/instruments/r46-f29-gate.py:202-240`: H2 requires `source: S074`, the round-46-a2 S074 recheck, S074 table citations and S074 anchors in the decision/package sections.
- `corpus/instruments/r46-f29-gate.py:303-329`: H5 recognizes only `S074.txt` citation suffixes and requires five located live cores. S076 quotes do not satisfy that grammar.
- Frozen intended repair `corpus/instruments/entry29-fixed-bytes.md:3-5,11-21` changes source/recheck/citations to S076. Thus H2/H5 reject the honest repair by construction. This is a predicate-level counterexample, **not an executed fixture**.
- The independent F30 change also violates H1's exactly-29 count (`r46-f29-gate.py:175-181`) and H6's exactly-66/name/content pins (`:332-352`). H6 also pins the other entries, so later unrelated honest growth is not generally exempt.
- H3 is not automatically exempt: it still requires S074 status `mined` and its original capture anchors (`:243-275`). If integration changes those S074 cells, its resulting red must be explained separately. H4 should still check the preserved original S074 manifest/capture (`:278-300`); unexplained failure there is not justified by D7.
- `corpus/lessons/round-46.md:96` already names M46-6 and demands an exemption story rather than discovering it after a later landing. The new C2 instrument does declare its F29-content exemption at freeze (`corpus/instruments/r47-f30-gate.py:53-62`), but this does **not** amend the old F29 gate or its receipts.

### Do-nothing discrimination

Named control: **unchanged round-46 receipted tree**, not a stub and not a tree with the new entry. `.ufo/waves/round-46/attempt2/controls/final-measure.txt:1,20-29` stamps revision `c8641e7a5a5859a62c55a0d2012efe6f5b0a9c7e` and records H1–H7 all green, `f29-gate fixed=7/7 exit=0`; H2 has `source=1 recheck=1 table-rows=19 anchored=1`, H5 `spans=45 located=45 failed=0 uncited=0 cores=5/5`. The closure independently established equivalent production bytes at judged revision `4cdcf7bdea8bea06705de752a2796d4e3aab0242` (`corpus/lessons/round-46-verifier-spotcheck.md:45-47`). Original entry `corpus/knowledge/github-repository-security-advisories.md:3-5,11-21` still shows the S074 identity at inspection. Keeping that identity avoids the H2/H5 mismatch but leaves D7 unresolved; replacing it with the frozen S076 entry repairs provenance while making those old predicates false. Therefore old-gate green is not a safe acceptance condition for this repair.

The control receipt was **read, not rerun**. No full battery or other executable check was run by this seat. No scratch was created.

## Exhaustive report sentence inventory for this change

Report is `fleet:.ufo/reports/round-46/kasegi.md` (82 lines). Numbers below refer to that file. Historical counts are not false merely because the corpus grows; the problem is reading unqualified “tip”, “after”, “every”, or executable examples as current. Preserve filed text and append an explicit naming erratum.

| Lines | Sentence or clause a round-47 reader could misread | Required qualification/correction |
|---|---|---|
| 3 | “both claims verify on their frozen counters … no owned axis harmed” | Round-46-era claim evidence only; not a live round-47 gate result or a current admission ruling. Closure §9 later records rejected-harmed. |
| 5 | “final lane hash … pre-report landing gate … reads 4/4 … at the same hash” | Historical hash only; D4 says the claimed gate transcript was not committed. Do not promote it to a fresh receipt. |
| 11 | “the two attempt-1 claim counters reach full mutation coverage”; “After: uncaught=0 on both” | Frozen round-46 battery/tree result only, not all later counters or round-47 mutation coverage. |
| 12 | “C2 … row S074, capture … S074.txt”; 28→29, 65→66, 73→74; excluded flows | F29 admission-era source/counts; current provenance becomes S076. Scope exclusions remain valid. |
| 13 | “C2 rests on S074 … opened … by the L1 … nine located quotes; source-recheck.py exit 0” | Original quote-integrity evidence, not evidence of a committed capture-producing recipe. D7 explicitly found that recipe absent. |
| 17 | “21 mutants (3 per limb H1-H7), 11 defect-tree flips … tally 11+10=21 stands” | Already corrected by the later round-46 lesson; cannot be republished as a reliable current receipt. |
| 19 | “gate v1.1 closing seven tree-level false-greens” | Seven identified classes closed at that era, not an assurance that corrected future F29 trees satisfy it. |
| 21 | “f29 selftest's 28-row precondition fixed to accept the landed 29-row README”; ledger floor/proofs | Era-specific fixes/proofs, not support for a future 30-row/67-entry tree or S076 identity. |
| 24 | “M46-6 … fix = errata E3 + the expected-moved selftest case” | That fixed the prior-attempt counter's transition only; it does not implement a general exemption for r46-f29-gate.py. |
| 45 | Entire C1 “After (landed tree …)” and selftest/result sentence | Results belong to receipted round-46 bytes, not the round-47 tree; do not inherit uncaught=0. |
| 46 | Entire C2 “After (tip 4cdcf7bd): fixed=7/7 …”; secondary `--expect 29`; plain counts; S074 recheck, binding 61/61, audit 66, harness 32/32, census | All are explicitly historical measurements. Neither the 7/7 nor H5 45/45 describes S076-reanchored entry bytes. Running the same commands at the new tip is a different experiment. |
| 47 | “attempt-1 C1 counter reads 7/7 at the tip”; old C2 5/7 “expected-moved, graded by r46-f29-gate.py”; “shows appends … only” | No-harm at the old tip only. The claimed replacement gate itself becomes era-bound. Append-only-hunks wording was already false (D3), not merely historical. |
| 51 | “SOURCES.md rows before→after: 73→74” | Round-46 delta only; not current registry size. |
| 55 | “same three warnings … no new warning: the S074 URL is unique” | Historical census only; S076 intentionally shares S074's URL, so uniqueness cannot be repeated as current. |
| 57 | “Rows touched old→new: none (additive hunks only … one Search-log bullet + two Registry-changes bullets)”; “C2 cites S074”; S068/REST/ZDI rejects | D5 bullets were fenced, not landed; S074 becomes historical provenance; S068 is n=1, REST lead was unrecorded, ZDI reservation must be resolved. This is not cured by merely changing a date. |
| 65 | “expansion: improved … S074 mined … SOURCES 73→74, knowledge 65→66 …” | Historical expansion assessment; current source identity/counts must be separately stated. |
| 66 | “quality: improved … 20 uncaught to 0 … all closed … every fix … logged erratum” | The closure addendum superseded quality to harmed for unmarked D5–D8. Do not reuse this sentence as current trend authority. |
| 67 | “no non-author admit/reject judgment of S074 exists yet”; “integration defects now fixed and receipted” | Closure now exists and leaves D5–D8 routed. Scope this absence to filing time; it is not current. |
| 79 | “F29 entry with 45 located quotes … No non-author verifier yet” | Original S074-based H5 reading, not a live S076 validation; later closure exists. |
| 80 | “S074 live re-open with zero drift against the pinned capture” | Do not equate located live text with byte-reproducible capture production; D7 found a provenance gap, not changed page content. |
| 81 | “every counting command runs … prints its reading … all uncaught=0 … final-measure.txt (exit 0 …) … r46-f29-gate.py --root . = 7/7. No non-author verifier yet.” | Most dangerous bare live-root assertion. It must be named verbatim in the erratum and restricted to the old receipted revision. All listed aggregate outputs and verifier absence are historical. |
| 82 | “No non-author verifier yet” | Filing-time absence only; closure followed. The F29/F28/CNA scope distinction itself is not withdrawn. |

Unchanged historical landing tables, seat counts, assimilation, tooling and task-execution status are not made stale by D7/F30. Existing D1/D2/D3/D4 errata remain independently necessary; this review does not replace them.

## Exact proposed append-only errata wording

The following text can be appended to the round-47 lesson and quoted in the round-47 report. It deliberately does not invent integrated-tip outputs:

> **Erratum — round-46 attempt-2 F29 receipts are era-bound, not live-root promises.** In the filed round-46 report `.ufo/reports/round-46/kasegi.md:3,11-13,19,21,24,45-47,51,55,57,65-67,79-82`, “tip”, “after”, the aggregate counts/selftest/battery results, and the bare statement “`r46-f29-gate.py --root .` = 7/7” refer only to the round-46 receipted production bytes at `c8641e7a5a5859a62c55a0d2012efe6f5b0a9c7e`, independently found equivalent outside `.ufo/waves` to judged tip `4cdcf7bdea8bea06705de752a2796d4e3aab0242`. The authoritative historical F29 receipt is `.ufo/waves/round-46/attempt2/controls/final-measure.txt:1,20-29`: `f29-gate fixed=7/7 exit=0`, H5 `spans=45 located=45 failed=0 uncited=0 cores=5/5`. It does not describe round-47 bytes and does not promise that rerunning that command on the present root is green.
>
> Round 47's D7 repair changes F29's current supporting source/recheck/citations from S074 to the superseding reproducible capture S076; the old S074 capture/manifest and their original quote-integrity receipt remain historical evidence, not a reproducible capture recipe. The old gate hard-codes S074 in H2 and H5, so the S076 repair is expected to make those limbs red even without F30. F30's 30th frontier row and 67th entry additionally exceed H1/H6's round-46 counts/name pins. The old gate is retained unmodified for historical replay, not used as the round-47 acceptance gate. E3 and its prior expected-moved case do not grant a blanket exemption to every old instrument or every red limb. Any other observed failure must be individually explained, not waived as era drift.
>
> The round-47 acceptance instruments are the frozen `corpus/instruments/r47-routed-defects.py` for D5–D8 and `corpus/instruments/r47-f30-gate.py` for F30. Their outputs, the integrated revision and the old F29 gate's full seven-limb output must be receipted separately; this erratum supplies no unrun result. The pre-freeze round-47 battery disclosed C1 16 and C2 18 survivors, not zero uncaught; round-46 mutation/selftest receipts cannot establish round-47 completeness.
>
> Separately, the report's “one Search-log bullet + two Registry-changes bullets” (`:57`, also lesson `round-46.md:135-137`) described fenced drafting bytes, not landed bullets; D5 corrects their placement. Its S068 “row class” statement overgeneralized one GHSA row, the REST-API lead lacked a corpus bullet, and the ZDI id reservation was consumed; D8 corrects these records. “No non-author verifier yet” was true only when filed. The later closure addendum superseded “quality: improved” with quality harmed, and its reconciliation records round 46 as rejected-harmed pending an operator ruling (`corpus/lessons/round-46-verifier-spotcheck.md:217-241`). Repairing these defects now does not retroactively change that ruling or manufacture an admission.

## Smallest safe correction and receipt requirements

1. Append the naming erratum above (do not rewrite old receipts, soften the old gate, retain a misleading S074 live identity, or suppress nonzero exit codes).
2. At integration, L1 records the final revision, exact old instrument bytes, command and explicit `--work` scratch path, all seven old-gate lines, summary and actual exit code. Classify each red limb with its changed tree predicate. Pair it with the two round-47 gate receipts and a plain source/citation/count derivation. A generic prose waiver without this receipt leaves the closure trap open.
3. Preserve the historical do-nothing receipt and S074 evidence. Historical replay is a separate era export with era-matching instruments, never a claim about the new root. Do not run the full battery for this erratum.
4. Keep any canonical admission/trade decision with its owner; correcting explanatory provenance does not authorize this critic to judge it.

**Limitations:** No integrated round-47 tree exists in the frozen evidence reviewed here; final red-limb set/summary is not measured by this seat. This is static predicate falsification plus inspection of committed historical receipts, not a fresh gate, battery, live-source or selftest run. No scratch or tools were installed/created. The requested findings file is the only seat write.

Self-evaluation: accuracy 4/5 (final-tip output intentionally unmeasured); completeness 4/5 (full 82-line report inventory, but integration receipt remains L1-owned); clarity 4/5 (long inventory is required to enumerate every affected sentence); actionability 4/5 (exact erratum supplied, final output must still be inserted from real receipts); conciseness 4/5 (historical inventory dominates). Overall 4.0/5. Highest-impact improvement is the bounded integrated-tree receipt, not an invented expected total.
