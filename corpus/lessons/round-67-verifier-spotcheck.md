# Round-67 verifier spot-check — kasegi

author: hyaku closure (non-author integrator, @m_zfl)

Round: kasegi r67 · base `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0` · final lane hash
`f167ee104d001791f7f444cda8a25c3866e0e28c` · measured implementation
`c40f0bc8ae95627b60b6f6e893ea00d7b1fd7146` · report `.ufo/reports/round-67/kasegi.md` (fleet commit
`414d7a45891e29252d1ca0bf90e6220eaedc4925`, commit date 2026-11-04 18:19:36 -0300, by
`kasegi-shokunin`) · prompt `.ufo/prompts/kasegi-round-67.md` (824 lines, 17:48 dispatch).

Driver digest (copied from `.ufo/watchdog.log`, mutable):

```
2026-11-04T17:48:59-03:00 launch kasegi round=67 pgid=3615195 driver=hyaku-inline attempt=1
2026-11-04T18:20:16-03:00 complete kasegi round=67; hyaku-inline attempt=1
```

## Conformance (step 1)

- **Attribution.** `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-67/kasegi.md` →
  `kasegi-shokunin <kasegi@shokunin.local> 414d7a45891e29252d1ca0bf90e6220eaedc4925 2026-11-04
  18:19:36 -0300`. The report lands after the lane's final commit (`f167ee10`, 18:19:12) and cites
  that hash as the final lane state. All six lane commits carry the lane identity
  (`kasegi-shokunin <kasegi@shokunin.local>` as both author and committer); none touches
  `.ufo/state/` or `.ufo/watchdog.log`.
- **SHONEN heading.** `grep -c '^## SHONEN'` = 1; four box lines (`[~]`, `[ ]`, `[~]`, `[~]`), one
  per box in `SHONEN.md` (4 boxes, `grep -c '^- \['` = 4). No `[x]` was written by this non-author,
  and the report writes none.
- **Ancestry.** Base plus all six cited commits exist and
  `git -C kasegi-shokunin merge-base --is-ancestor <h> refs/heads/master` = yes for each (the repo is
  jj-colocated and git HEAD is detached, so ancestry was tested against the branch ref, never
  `@{u}`): `8e2a8fe8`, `7ae95a06`, `b3082060`, `e59c564e`, `c40f0bc8`, `73e6a0c0`, `f167ee10`.
- **Lane state.** `scripts/hyaku/jj-lane.sh state kasegi-shokunin` →
  `branch=master local=f167ee104d00 remote=f167ee104d00 ahead=0 behind=0 head=detached tracked=0
  untracked=0`; `git status --porcelain` empty; `git ls-remote origin refs/heads/master` prints
  `f167ee104d001791f7f444cda8a25c3866e0e28c`. No uncommitted round work.
- **Prompt fidelity.** `templates/round-prompt.md` (140 lines) renders byte-identically to the
  dispatch's l.1–140 after the macro substitutions (the only diff is the working-dir substitution,
  which the dispatch carries correctly as `kasegi-shokunin`); the §6 hyaku addendum starts at
  l.141 and is appended, not substituted. All ten contract items are present: mission/axes binding
  (l.3), L2 ≥8 in one batched AgentSwarm call (l.82), report path and filename (l.101), Work
  performed opening on the declared claims (l.104), commit-hash citation rule (l.107), per-claim
  counting command and measured commit (l.109), Sources & frontier (l.111), trend verdicts (l.116),
  `## SHONEN` one line per box (l.118), commit-then-push ordering (l.133), push scope (l.135), L0
  side channel (l.138). The quoted L2 route map (run-15 restore: reviewer/critic/executor/
  mutation-tester/sentinel `@m_zfl`, every other role `@m_flash`) does not contradict
  `MISSION.md` §L2: that section holds advisory role-class buckets and delegates the actual route to
  the operator's global host table, and the prompt passes no model parameter.
- **Marker check.** Substantive report, not a marker: two declared claims, six landed commits each
  tied to an existing `LOG.md` round-67 bullet (l.2696–2708), committed receipts under
  `.ufo/waves/round-67/`, and a checkable commit-hash citation. Status `ok`.
- **Report contract.** Sections appear in the required order (Work performed → Landed changes →
  Before → after measurements → Sources & frontier → Trend verdicts → SHONEN); the frontier step is
  present (two opened rows, census before→after, ten `## Mistakes` rows, C2 as the sourced claim);
  the wave is one v1 call of 12 seats (`w1-dispatch.json` `counts.spawn=12`, `taskCall` present,
  `resumeSends` empty), 5 of 12 attack seats (41.7 %), one connector seat, no residual call.

## Claim re-checks

C1 is a **gate claim**, so per PROTOCOL §Gate standard ("Closure consequence") its committed
evidence was verified and the lane's gate was **never executed**. C2 is countable and was
**re-measured** by this reviewer with the frozen manual census commands over committed bytes.

### C1 — depth:verifiability, 4 → 4, delta 0, nominal R58

Frozen predicate (`.ufo/waves/round-67/claims.json`): `VERIFY measurements=12 failures=0 and process
exit0 on the exact committed-input counter at the measured revision.`

```
$ git show <rev>:<path> | sha256sum                 # committed bytes, not the worktree
corpus/instruments/figure-audit.py @8e2a8fe8   51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac
corpus/instruments/figure-audit.py @c40f0bc8   8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247
corpus/instruments/figure-audit.py @f167ee10   8147350c… (worktree identical)
w1/ExecMultiHeadDriver/verify.py  @f167ee10   07dfa36c2ec0a26e40034675a746c5f49e02988f0ee2b36fea1f6f6f79210bdd
w1/MutationMultiHead/multihead-mutbat.py @c40f0bc8 and @f167ee10   ea31d43929529de60602fecdbbb72a0723012288fce0d195fc7bdca6c200ac01
corpus/instruments/figure-audit-ledger.json   28ad7fefedf0d911ea8afec3c3f1278c4001f682edec583266b82ed8e81a753b (35 figures)
```

`controls/driver-pins.json` pins those same values (`driver 07dfa36c`, `controls` battery
`ea31d439`, probes `d56a1437`, `measured.gate_sha256 8147350c`, base gate `51f299af`,
`tree_inputs` ledger `28ad7fef`), so the receipt's `RESULT controls-pins PASS pinned=14` is a
committed-bytes check, not a self-report. The final receipt is unchanged between the measured
revision and the tip (`git log -- <receipt>` = one commit, `73e6a0c0`; its own line names
`revision=c40f0bc8ae95`).

```
$ .ufo/waves/round-67/controls/final-verification-r67.txt   (committed at 73e6a0c0)
RESULT driver-self-pin PASS running=07dfa36c… pinned=07dfa36c… committed-at-controls=07dfa36c… mode=final
RESULT controls-pins PASS pinned=14 problems=none
RESULT probes-base-paired PASS mode=base probes=20 rc=0
RESULT probes-measured PASS mode=candidate probes=20 rc=0 face-recorded=P10=rc1/derive-upstream-signal-13,…
RESULT shape-identity PASS shapes=20 … P9/P10/P11 stale derive-upstream-signal-13 …
RESULT selftest PASS cases=73 failures=0 want=73 exit=0 kind=candidate
RESULT mutbat-existing PASS killed=5/5 survivors=0 invalid=0 controls=pass
RESULT multihead-mutbat PASS killed=7/7 survivors=0 equivalents=3 invalid_rejected=0 failures=0
RESULT real-ledger PASS want='FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0'
RESULT red-wrong-want PASS   RESULT identity-guards PASS head=c40f0bc8ae95 gate=8147350c… base=51f299af…
VERIFY measurements=12 failures=0 revision=c40f0bc8ae95627b60b6f6e893ea00d7b1fd7146 mode=final
```

Before-state, read as committed receipts (not re-run):

```
$ .ufo/waves/round-67/controls/donothing-multihead-r67.txt
GATE sha256=51f299af… 
NATIVE P9 stages=[-13, 0] derive=cut -f1 -d: big.txt missing.txt | head -n 1
NATIVE P10 stages=[-13, 0] derive=wc -l big.txt missing.txt | head -n 1
NATIVE P11 stages=[-13, 0] derive=grep x xlines.txt missing.txt | head -n 1
FIG P9 … ok   FIG P10 … ok   FIG P11 … ok
NOWORK-VERDICT gate=corpus/instruments/figure-audit.py green_on_masked=P9,P10,P11,P12,P13,P14
$ .ufo/waves/round-67/controls/critic-s3s4-confirm-r67.txt
NATIVE S3 cut-mid--   [[-13, 0] ×5]      FIG S3 … ok
NATIVE S4 grep-mid--  [[-13, 0] ×5]      FIG S4 … ok
NATIVE S6 cut-no--    [[1, 0] ×5]        FIG S6 … stale
$ w1/ExecMultiHeadDriver/driver-base-r67.txt
RESULT selftest PASS cases=67 failures=0 want=67 exit=0 kind=base
RESULT multihead-mutbat FAIL … killed=0/7 … invalid_rejected=10 failures=5
$ w1/ExecMultiHeadProbes/probes-output-base.txt       PROBES probes=20 failures=0 mode=base instrument=51f299af…
$ w1/ExecMultiHeadProbes/probes-output-candidate-vs-base.txt  PROBES probes=20 failures=5 mode=candidate instrument=51f299af…
$ w1/ExecMultiHeadGate/selftest-base-graft-r67.out     selftest cases=73 failures=5   (the five repair shapes; the sixth new case is a positive control)
```

Static delta (`git diff 8e2a8fe8 f167ee10 -- corpus/instruments/figure-audit.py` = 117 insertions,
23 deletions): `EXPECTED_CASES` 67 → 73 (67 + 4 multi-head + 2 end-of-options), a new
`sigpipe_input_count()` that splits the decoded argv at the FIRST `--` anywhere, skips grep's
pattern as a required non-file argument, counts every post-separator token and treats option values
as operands (conservative), applied only to `READ_ONLY_HEADS` with `cat` keeping round-66's rule
byte-identically and unknown heads (`git`, `python`) keeping the old benign rule. The seven-limb
battery that kills 7/7 is the same digest the pin names, so the post-freeze Erratum-2 battery edit
is measured, not orphaned. The reviewer's own table names the conservative refusals (detached
option values, `grep -e x -- f`) and the wave names the residuals; the claim's finite scope is
honest.

Verdict: **claim verified** (predicate met on the frozen counter; before/after reproduced from
committed receipts; the measured production instrument equals the pinned candidate digest; no
post-measurement change to gate, probes, battery, pins or receipt).

### C2 — coverage, 8 → 8, score held

```
$ git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
99  ->  101
$ awk … tier histogram     A=89 B=5 C=5   ->   A=91 B=5 C=5
$ awk … status histogram   mined=81 rejected=18  ->  mined=83 rejected=18
$ awk … malformed rows (NF!=13)   0     duplicate ids   (none)     enum/tier-inflation   (none)
$ awk … mined rows whose used-by paths do not exist   (none)
$ git ls-tree -r --name-only <rev> corpus/knowledge/ | wc -l     82  ->  83
$ git show <rev>:corpus/README.md | grep -oE '^\|[[:space:]]*F[0-9]+' | sort -u | wc -l   44 -> 45
   (raw rows 46 -> 47: F02 and F29 each appear twice in the append-only admission sections)
```

```
$ python3 corpus/instruments/frontier-recheck-count.py     entries=48 pass=48 exit=0
$ python3 corpus/instruments/capture-binding-check.py      records=81 bound=81 unbound=0 exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-67/manifest.json --source S100   exit=0
$ python3 corpus/instruments/source-recheck.py … --source S101                                                          exit=0
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi W04 S028 … / S029 … / S072 … / S076 … / S080 … / S085 …   kasegi ok …/corpus/SOURCES.md   exit=0
```

The six `W04` warnings are byte-identical to `controls/census-before.txt` and `census-after.txt`;
none names S100/S101. Snapshot digests re-measured: `S100.txt` `cf834a65…` (478 lines, 59068 bytes),
`S101.txt` `a55e315f…` (768 lines, 58889 bytes), both matching the rows and the manifest. The new
entry opens with its provenance trio, cites S100/S101 with URL + anchor, and the README carries the
F45 row (l.1063). `git diff --numstat` over the corpus shows pure additions: SOURCES +6/-0,
README +21/-0, QUALITY +16/-0, knowledge-expected +1/-0, LOG +13/-0, SKILL +2/-0, SCORECARD
+31/-0, PROVINCE unchanged; the only deletions in the whole round are the 23 replaced lines in the
gate. Registry 99→101, knowledge 82→83, frontier 44→45, entries 47→48, capture 79→81 all reproduce.

**One numeric defect:** the entry header and the SOURCES bullet say `54/54 OK (S100 44, S101 10)` /
`54 pinned quotes`, while the landed manifest pins **58** (S100 48, S101 10) and the instrument
prints 58 quote-level `OK` lines (60 lines including the two sha256 lines). The scribe seat caught
this before landing (`w1/ScribeF45/NOTES.md:211-213`); it was landed unfixed. Routed as V67-1.

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability (lowest, 4) | **improved** | The frozen counter moved from a base that reads `ok` on the three two-operand SIGPIPE pipelines and both mid-argv `--` shapes to a candidate that reads `stale` on all five, with `VERIFY measurements=12 failures=0` at the pinned gate `8147350c`, selftest 67→73, and the five other measurements green. The nominal R58 score is held at 4 because the metric R58 scores (citation resolution / source availability) is not read by this gate — `delta 0` is reported, not hidden. |
| coverage (8) | **improved** | F45 admitted on ground the coverage map did not hold (S098 carries zero "Maturity Level" occurrences), with registry 99→101, knowledge 82→83, frontier 44→45, capture records 79→81, census exit 0 and 58/58 pinned quotes. The score is held at 8 by the lane's saturation convention; the report's wording "saturated under the lane's saturation line" is loose (line 9, score 8) but the held score is explicit. |
| depth:density (9) | **unchanged** | Not targeted, not re-measured; no density credit claimed or taken; the SKILL delta is one appended current-execution amendment. |

No owned axis is harmed: `SCORECARD.md` is a pure append (31/0), `PROVINCE.md` is byte-identical to
base, no knowledge entry was superseded or deleted, and `SHONEN.md` carries no new mark.

## Discernment spot-check (non-author)

| # | Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|---|
| 1 | S100 admit (FIRST PSIRT Maturity HTML page) | admit, tier A docs, mined | `https://www.first.org/standards/frameworks/psirts/psirt_maturity_document` fetched 2026-11-04 (HTTP 200, 82978 bytes); committed `S100.txt` L224; row `corpus/SOURCES.md:112` | **agree** | The located quote "in this document is intended to describe a profile of a product security team" (14 words) appears verbatim in the live page's text and at `S100.txt:224`; the snapshot digest matches the row and the manifest; the anchor carries lines and a revision, not a homepage. |
| 2 | S101 admit (same document's PDF companion) | admit, tier A docs, mined | `https://www.first.org/standards/frameworks/psirts/FIRST_PSIRT_Maturity_Document.pdf` fetched 2026-11-04 (HTTP 200, 644190 bytes, sha256 `f217c446…` reproduces exactly); committed `S101.txt:8`; row `corpus/SOURCES.md:113` | **agree** | The raw digest reproduces byte-for-byte and the cover notice "believes are best practices. These descriptions are for informational purposes only" (12 words) sits at L8, which the HTML rendering does not carry; admitting the PDF for that notice (not as a second document) is the right scope. |
| 3 | Reject the round-65 lead's raw-HTML digest `334aeb01…` as an anchor | reject, retire the lead | same URL fetched 4× on 2026-11-04; `grep -c 334aeb01 corpus/SOURCES.md` = 2 (the historical lead line at `:246` and the retirement bullet at `:252`), no `S###` row | **agree** | Today's raw digest is `fce2d830…` ≠ `334aeb01…`, the CSP `nonce=` differs per response, and a 82978-byte body with a response-scoped nonce cannot anchor a claim; the decision is right. Caveat recorded: four back-to-back fetches returned one identical digest/nonce (CDN caching), so the lesson's "six fetches give six raw digests" needs spaced fetches to reproduce — the mechanism, not the verdict. |
| 4 | Reject the per-level service-area listings as text claims | reject (PNG artwork) | `S100.txt` L225–L227 (Figure-1 caption then "Getting Started - Operational Foundations"); `controls/c2-entry-verification-r67.txt` "figure labels absent 0" | **agree** | The caption is text, but the box labels are not: the snapshot jumps from the caption to the next section, and the entry-verification receipt measures 0 figure-label hits. Refusing to cite a PNG's labels as text is correct. |
| 5 | New registry rows S100/S101 | row written as claimed | `corpus/SOURCES.md:112-113` | **agree** | Both rows are well-formed 11-column rows (`malformed=0`), tier A / kind docs / status mined / `opened=2026-11-04` / `recheck=180d` / `used-by=corpus/knowledge/first-psirt-maturity-document.md` (path exists), ids are the next unused and unique, and the `## Gate` quotes are 14 and 12 words (≤25) with line locations. |

## Trend verdicts

- **Expansion — improved.** F45 admitted with an 18-row attributed claim table on ground the lane did
  not hold; two new tier-A rows (registry 99→101), one new knowledge entry (82→83), frontier 44→45,
  capture records 79→81 — all re-measured above.
- **Quality — unchanged.** No knowledge entry was superseded, re-admitted or re-verified;
  `corpus/knowledge/` gains one new file and modifies none. The gate repair is an instrument
  correction, not a corpus entry. QUALITY gains R93–R100 from this round's mistakes, which is the
  discernment instrument rather than a quality move by itself.
- **Discernment — improved.** The wave's attack seats found the mid-argv `--` hole, the flaky native
  face and three counter defects **before** the freeze (M67-1..M67-4), and the round's own errata
  were filed with both receipts preserved (M67-5..M67-10). This non-author spot-check agrees with
  both sampled admits and both sampled rejects, and the sample's one disagreement-shaped finding
  (the stale quote count) was already captured by a seat as a conflict and is routed below rather
  than left unlearned. Outside admission/promotion remains owed.

## Routed defects and notes

1. **V67-1 (lane, minor, evidence standard).** `corpus/knowledge/first-psirt-maturity-document.md:11`
   and `corpus/SOURCES.md:250` say `54/54 OK (S100 44, S101 10)` / `54 pinned quotes`; the landed
   manifest pins 58 (S100 48, S101 10) and `source-recheck.py` prints 58 quote-level OK lines. The
   scribe flagged it (`w1/ScribeF45/NOTES.md:211-213`) and it landed unfixed. Fix as an appended
   correction naming the superseded text (append-only), with the counting command.
2. **V67-2 (lane, minor, citation base).** `corpus/README.md:1050` carries a backticked bare
   `knowledge/first-psirt-maturity-document.md`; the lane's own `citation-ground-check.py --root .`
   exits 1 and lists it as `finding class-lane-bare … corpus/README.md:1050` (findings=11). Add the
   `corpus/` prefix and the `citation-reground-ledger.md` row in the next round.
3. **V67-3 (lane, minor, anchor).** Entry C15 (`:29`) ends the Level-3 capability-area list at
   `S100.txt:463`; L463 is `Train development teams`, an item under the L462 `Training & Education`
   heading, so the area list should end at L462 (the quote at L463 is correct as a quote).
4. **V67-4 (lane, minor, receipt prose).** `controls/driver-pins.json`'s `note` still names driver
   `61d5a048` and battery `e6d54540` while the pinned dict values are `07dfa36c` and `ea31d439`
   (the note describes the pre-erratum state; the dict — and the receipt's self-pin — are correct).
5. **V67-5 (inherited, not introduced by r67).** `recheck-audit.py` exits 1 at base and tip with the
   same 9 `cwd_fail` (73/82 → 74/83; the new entry passes), and `citation-ground-check.py` exits 1
   with 10 inherited findings besides V67-2. Standing routed items; the round neither fixed nor
   introduced them.
6. **V67-6 (fleet/operator, unchanged).** `.ufo/state/kasegi.round` still reads `17` (stale legacy
   watchdog state, already recorded as V66-4); the MANIFEST closure ledger is the round authority
   and the report, lesson, LOG and SCORECARD all say 67.
7. **Operator note (promotion, operator-owned).** SHONEN boxes 1, 3 and 4 are `[~]`
   author-asserted but checkable by a non-author against committed bytes; box 2 stays `[ ]` (no
   authorized end-to-end domain task). No box was marked here; promotion is operator-owned.

No lane-authored file was edited by this reviewer; this file is the only artifact written.
