# R47ConnCross — numerical consistency recon

Axes: **depth:verifiability; coverage**. Findings/proposal only: no judgment, admission, integration, or production changes.

## One bounded proposed move

Use the table below as a **definition-qualified measurement ledger** for the report: every number carries its tree (base/freeze/working/synthetic/final), counted unit, command, and observed-versus-target status. This combines the scorecard's attribution split with the reviewers' control distinctions. It improves verifiability without reducing coverage or changing either frozen claim. Do not substitute a synthetic green or a current working-tree reading for a historical measurement.

Second-order effects: runtime reads remain the same frozen counters; contract predicates/axes stay unchanged; substrate accounting names strict roles instead of inferred adversarial intent; verification keeps independent plain counts and semantic review separate from mechanical gates. Risk: copying this ledger after concurrent integration makes receipts stale. Bind final values to L1's measured tree, not to this report's inspection time.

## Executed base control

Read-only `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8 corpus` extracted under `/fast/scratch/hyaku/kasegi-r47/R47ConnCross/base`; no checkout/index/commit operation. Let `L` be the lane root, `B` that export, `S` the seat scratch root. Executed:

```text
python3 L/corpus/instruments/r47-routed-defects.py --root B --work S/r47-routed-defects.py --baseline B
L1=0 scaffold-phrases=4
L2=0 fence-markers=4,search-log-bullet-absent,s074-row-bullet-absent,capture-note-bullet-absent
L3=0 corrections-section-absent
L4=0 false-phrases=2
L5=0 order-phrase-still-present
L6=0 two-cases-absent
L7=0 dropped-findings-unnamed
L8=0 row-S076=absent-or-duplicated hits=0
L9=0 old-citations=59
L10=0 rest-api-lead-bullet-absent
L11=0 round-47-lesson-absent
routed-defects total=11 fixed=0 unresolved=11 exit=1
process_exit=1; stderr empty

python3 L/corpus/instruments/r47-f30-gate.py --root B --work S/r47-f30-gate.py
H1=0 rows=29 admitted=29 dup=0
H2=0 entry-absent zdi-named=
H3=0 row-S075=absent-or-malformed-or-not-registry-only hits=0
H4=0 manifest-absent
H5=0 entry-absent zdi-named=
H6=0 entry-absent zdi-named=
H7=1 census-rc=0 ok-line=1
f30-gate fixed=1/7 exit=1
process_exit=1; stderr empty
```

These reproduce the named do-nothing controls `controls/c1-base.txt` and `controls/c2-base.txt` (`controls/freeze-controls.txt:1`). Neither reaches the claimed after-value. Plain base counts independently computed with Python `re.findall`, `splitlines`, `str.count`, and immediate-directory `Path.glob('*.md')`:

```text
frontier_rows=29 registry_rows=74 knowledge_entries=66
F29_lines=145 to_append_matching_lines=2 fence_matching_lines=4
S074_citation_matching_lines=54 S074_citation_instances=59
three_cases_matching_lines=2
```

## Single report-number ledger

Paths are lane-relative; `W` = `.ufo/waves/round-47/w1/`, `C` = `.ufo/waves/round-47/controls/`. Commands below are source/reproduction commands; only the two base counter calls and plain base counts above were newly exercised here. After-values are **targets**, not accomplished results.

| Quantity / definition | Source command or exact evidence | Base / other observed state | Expected round-end / reporting constraint |
|---|---|---|---|
| C1 fixed limbs, unresolved, exit | `python3 L/corpus/instruments/r47-routed-defects.py --root TREE --baseline B --work OWN_SCRATCH` | **0/11**, unresolved **11**, exit **1**, newly observed | **11/11**, unresolved **0**, exit **0** |
| Routed defect groups, not limbs | `claims.json:12-13`; counter doc :9-30 | **4** groups D5–D8 | **4** groups closed only with semantic review; not “11 defects” |
| C2 fixed gates / exit | `python3 L/corpus/instruments/r47-f30-gate.py --root TREE --work OWN_SCRATCH` | **1/7**, exit **1**, newly observed; freeze **2/7** per claims :50 | **7/7**, exit **0** |
| Frontier rows / admitted | `grep -cE '^\| F[0-9]+ \|' corpus/README.md`; gate H1 status parse | **29/29**, newly observed | **30/30**; exactly one F30 |
| SOURCES registry rows | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | **74**, newly observed | **76** = +1 S075/C2 +1 S076/C1; not 75 |
| Knowledge immediate `.md` files | `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` | **66**, newly observed | **67**; gate also rejects extra/nested/symlink files |
| Coverage ratio | claims :37; `W/R47SrRegistry.md:66-71` | `(20+29)/(20+29)` = **1.000** | `(20+30)/(20+30)` = **1.000**, not ratio improvement |
| Lost-domain coverage | `W/R47SrRegistry.md:70-71` | **0/18** carried, not newly measured | **0/18**, distinct denominator |
| Scaffold phrase types / to-append lines / fence-marker lines | C1 L1/L2; claims :20-21 | **4 / 2 / 4**; last two newly plain-counted | **0 / 0 / 0** |
| Original bullets rendered in real sections | C1 L2; `W/R47ScoutScaffold.md:33-58,80` | **3** payload bullets physically present but fenced; **0** recognized landed | **3** byte-verbatim landed; not three newly authored bullets |
| F29 false-sentence classes | claims :12; C1 L4–L6 | **3** classes, including prose assertions at two entry locations | **0** false classes; plain “three cases” token is not a kill rule |
| F29 line count | `wc -l corpus/knowledge/github-repository-security-advisories.md` | **145**, newly observed | **145** |
| Old citation matching lines versus occurrences | `grep -c 'S074.txt:' ENTRY` versus Python `text.count('S074.txt:')` | **54 lines / 59 occurrences**, newly observed | **0 / 0**; neither equals number of quoted spans |
| F29 corrected quote inventory | `W/R47ScoutEntrySpans.md:7-11,25-31` | absent S076 cites at base; draft **47 occurrences / 29 unique**, max **22 words**, source spans **1 line** | Re-measure integrated bytes; **47** is draft-specific, not frozen target |
| S074 versus S076 capture size | claims :12; `W/R47ScoutS076Live.md:13` | S074 **42 lines**; S076 absent at base, freeze **610 lines / 19804 bytes** | Preserve historical 42-line capture; use reproducible 610-line successor |
| S075 capture size / body / quote records | `wc -l`, `wc -c`, manifest quote-array length; `W/R47ScoutZdiLive.md:7-26` | absent at base; freeze **60 lines / 4701 bytes**, body **20–27**, **10 quotes** | Same pinned bytes and **10** records; not ten distinct source lines |
| S076 body / quote records | manifest; `W/R47ScoutS076Live.md:19-32` | absent at base; freeze body **558–600**, **12 quotes** | Same pin; numerical body interval includes labeled chrome |
| Live-capture repetitions / drift | `capture-source.py --kind html`, twice per URL; `W/R47ExecManif.md:5-8` | no new execution by this seat; peer reports **2 per URL / 4 total**, normalized drift **0** | Temporal observation only; not raw-HTML stability |
| Census exit / duplicate warnings | `sources-census.sh validate --file TREE/corpus/SOURCES.md`; `W/R47ScoutRegistry.md:13-24` | **exit 0, 3 W04**, no E04 | Target **exit 0, 4 W04**, no E04; entry must exist to avoid E11 |
| Capture-binding whole-corpus totals | `capture-binding-check.py --root TREE`; `W/R47ScoutRegistry.md:15-16,76-79,131-133` | freeze-containing control **63 records / 61 bound / 2 unbound** (NOT historical base) | Intended no unbound records; proposed S074 rejection instead yields **63/62/1**, exit **1** |
| Capture-binding isolated totals | `W/R47RevD7.md:9-13` + receipts | synthetic control **3/3/0**, exit **0** | rejection arm **3/2/1**, exit **1**; do not compare denominator 3 to whole corpus 63 |
| Pre-freeze mutation coverage C1 | `C/mutbat-receipt.txt:36`; claims :18 | **35 total / 19 caught / 16 uncaught**, baseline failures **0**, exit **1** | Remains disclosed; no uncaught=0 claim |
| Pre-freeze mutation coverage C2 | `C/mutbat-receipt.txt:58`; claims :41 | **21 / 3 / 18**, baseline failures **0**, exit **1** | Remains disclosed; total survivors **34**, total mutants **56**, caught **22** |
| Tree-probe selftest | `C/selftest-receipt.txt:44-45`; `W/R47ScoutQual.md:24,30,69` | **43 cases / 0 failures / exit 0**, includes **2 positive +41 negative** | Separate from mutation coverage; not rerun here |
| Recheck audit counts | `W/R47ExecState.md:53-68` | peer current tree **66/66**, executes **44**, gated **22**, broken **0** | New entry implies **67** total if all preserved; final audit unrun here; no reduction of gated=22 evidenced |
| Scores / saturation | `W/R47SrScorecard.md:19-21,39`; claims :13 | carried scores **4/8/9**, saturation line **9/10**, window **3** | Held, not promotion; score-5 criterion still requires **0 gated + non-author 25/25** |
| Density guard | `density.py SKILL.md`; `W/R47ExecDensity.md:5-7` | peer base/current **275.1**, **1173 lines**, **34 blocks** | No density credit; final value contingent on integrated bytes |
| Assimilation inventory/collisions | `W/R47ScoutMerge.md:37-44`; `W/R47ExecMergeGuard.md:6` | current registry **74**, staged IDs **94**, collisions **44** = S031–S074 | Not **42**; no assimilation/admission implied |
| Round-47 wave-1 planned seats and strict attack share | JSON query on `wave1-spec.json`: `.items|group_by(.role)`; select reviewer/critic/mutation-tester | cached plan **64**; reviewers **12**, critics **8**, mutation-testers **6** | **26/64 = 40.6%**; planned share, not completed/usable seat share; wave 2 unmeasured |
| Round-47 other planned role counts | same JSON query, observed here | scouts **11**, scribes **12**, executors **8**, sentinels **3**, connectors **2**, revenger **1**, simplifier **1** | Builder header's scouts **10** / executors **9** is stale (`build-wave1-spec.py:4`) |
| Round-46 attack-share correction | local current-round assignment cache `build-wave1-spec.py:92` | historical broader **27/64 = 42.2%** | Required strict correction **24/64 = 37.5%**; not round-47's 26/64 |

## Contradictions / integration hazards

1. **Not a conflict:** SOURCES **74→76** is the frozen combined round delta (`claims.json:45`; scorecard :20,28; lesson :67). C2 alone adds one row; it cannot justify saying the complete round ends at 75. No present inspected draft asserted combined 74→75.
2. **Tree identity mismatch:** `W/R47ExecGateReplay.md:57,77` reports working C1 **2/11**, whereas `claims.json:29` and scorecard :27 refer to freeze **0/11**. Existing lesson content explains L7/L11 passing. Do not call current working bytes the freeze tree. Historical base replay here is genuinely 0/11.
3. **Binding conflict, not score averaging:** frozen C1 after-text demands S074 rejected; `W/R47RevD7.md:9-17` and registry probe show rejecting its retained manifest anchor fails B3. Census may still pass. This seat does not select a contract change or silently change the target; L1 must explicitly resolve the incompatible requirements before claiming no harm.
4. **Used-by drafts disagree:** `W/R47SrLesson.draft/round-47.md:61` says historical used-by unchanged; `W/R47ExecS074Flip.md:18` and claims :13 require `corpus/lessons/round-46.md`. The final report must state the actual cells and disposition, not blend them.
5. **Chrome is inside the numerical body interval:** `W/R47ExecManif.md:8` says 558–600 are policy prose while immediately listing chrome within them. `W/R47ScoutEntrySpans.md:9` identifies **one** correctly located chrome quote (559). Lesson :15's “fails on ... a chrome ... span” is stricter than the actual location gate and conflicts with the reviewed correction that explicitly quotes chrome. Numeric in-range is not prose classification. Reviewer :9 in `R47RevD6.md` separately disputes :566's classification.
6. **Historical 42 vs current 44 collisions:** lesson :50 explicitly labels 42 historical, so it need not be rewritten as 44; the report's current assimilation figure must use the two agreeing current receipts. Builder critic card :143's 42 is stale as a current figure.
7. **Control naming differs:** C2 reviewer `W/R47RevCounterC2.md:25-29` calls a synthetic green tree “do-nothing-control” (**7/7**). It is not the round's historical do-nothing base (**1/7**). Name the former “unmutated positive fixture” in report summaries. C1 comment/fence attacks also grade **11/11** (`R47RevCounterC1.md:7-9`), so mechanical final green alone cannot establish semantic closure.
8. **Grounding-quote count conflict:** registry :25 labels Q10 grounding **23 words**, while entry-Q reviewer :25 labels Q10 **20 whitespace words**. This seat independently counted the displayed Q10 with `len(text.split())` and got **20**; no evidence explains 23. Correct the draft's count or explicitly supply its alternative tokenizer rather than presenting both as the same measure. The eight lesson Gate quotes, ten manifest quotes, ten F30 table quotes, twelve S076 manifest quotes, and 47 F29 quote occurrences are separate sets.

## Coverage boundary and verification handoff

Inspection cutoff: 27 top-level reports plus the F30 and lesson draft visible in the final inventory, including all their relevant numerical statements through ranged reads/searches. Synthetic attack trees/control entries were treated as fixtures, not proposed corpus totals. `R47SrReport.md`, `R47SrReadme.md`, and `R47SrD5Diff.md` were not in that inventory; no claim to have reviewed unpublished or later-arriving drafts. Reconcile those against this ledger at integration. This is bounded wave-1 recon, not final round census or wave-2 completion.

L1 verification: run both frozen counters and plain counts on the named final tree; separately run capture binding, census, and recheck audit; bind attack share to the actual chosen denominator and report wave 2 separately. Preserve mutation survivors and comment/ghost-row findings even if counters turn green. No full battery was run here.

Hygiene: scratch removed in Python `finally` after all measurements. Disk guard printed scratch **375.6G free**, /tmp **96.7G**, /var/tmp **532.8G**; consumer-list phase timed out at 30 seconds and harness auto-backgrounded it despite synchronous parameters. No deliberate background job, delegation, tool install/update, git/jj mutation, or production write. Only this report and own draft receipts are written.

Self-evaluation: accuracy 4/5 (new base receipts; final values unobserved); completeness 4/5 (explicit cutoff excludes unpublished drafts); clarity 4/5 (many units require separate rows); actionability 4/5 (reproduction commands supplied, integration L1-owned); conciseness 4/5 (ledger length necessary for D1 accounting). Mean 4.0. Highest-impact improvement is binding final report numbers to integrated receipts; user should not mistake targets for results.

Report: .ufo/waves/round-47/w1/R47ConnCross.md
