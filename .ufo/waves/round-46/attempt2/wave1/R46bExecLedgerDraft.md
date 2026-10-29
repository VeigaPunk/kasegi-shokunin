VERDICT: DRAFT-READY

Seat: `R46bExecLedgerDraft` (executor, leaf). Lane `kasegi`, round 46 attempt 2. Lane HEAD at the time of the runs: `ee03806b6b54a2822045e96641a77fa76984b410` (frozen base `04af9bc92229232ea5cce8b32bfe59dd969eb26d`, freeze commit `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`). No commit, no push, no git/jj mutation, no edit to any tracked lane file; the only writes are my draft directory, this report, and a scratch tree that was removed on exit. Documentation only: no live target was probed, no credential, session URL or op:// reference appears below.

## 1. Built: the exact ledger append

**Deliverable:** `.ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/ledger-append.md` — 10146 bytes, 19 lines, the verbatim `## Round-46 dispositions (appended 2026-10-29, R6/R9)` section, one disposition paragraph per proposal (seven paragraphs, proposals 1–7 of `considerthese/2026-10-26.md`; `grep -c '^\*\*[0-9]\.'` → `7`), each with path:line or command+output evidence pointers, plus a closing scope note. It is an end-of-file append (R6/R9): it edits no earlier section and no `recheck:` line (`grep -n '^recheck:'` on the draft → no match), and it carries exactly one `##` heading.

**Source of the disposition.** The card's preferred input, `.ufo/waves/round-46/attempt2/wave1/R46bScoutLedger.md`, was absent when I ran (`ls: cannot access '.../R46bScoutLedger.md': No such file or directory`; the wave directory held only `swarm-registry.json` and other seats' drafts), so I derived it from the fallback sources named in the card plus the attempt-1 scout draft that is committed in the lane: `corpus/lessons/round-46.md:29` (the `## Gate — frontier, source, and rejection` section's `considerthese:` paragraph) and `corpus/knowledge/considerthese-proposals-ledger.md` (the existing sections), and `.ufo/waves/round-46/wave1/R46ScoutConsiderthese.md` (attempt-1 scout, read-only). If the scout's draft lands later, the L1 can diff it against mine; the seven proposal titles and numbering are taken verbatim from `considerthese/2026-10-26.md:29-35`.

**State of the target file, measured.** `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -n '^## ' corpus/knowledge/considerthese-proposals-ledger.md` ends at

```
134:## Round-42 dispositions (appended 2026-10-28, R6/R9)
```

and `wc -c corpus/knowledge/considerthese-proposals-ledger.md` → `30696 corpus/knowledge/considerthese-proposals-ledger.md`, `wc -l` → `146 corpus/knowledge/considerthese-proposals-ledger.md`, `grep -c '^## Round-46 dispositions' corpus/knowledge/considerthese-proposals-ledger.md` → `0`. The file therefore carries no round-46 section yet, and rounds 43, 44 and 45 filed none either: `grep -cE '^## Round-4[345] dispositions' corpus/knowledge/considerthese-proposals-ledger.md` → `0`.

## 2. Verification A — `r46-f29-gate.py` H6 stays green with the ledger grown

Scratch: `S=/fast/scratch/hyaku/kasegi-r46/R46bExecLedgerDraft` (removed on exit). Tree exported read-only with `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive HEAD corpus | tar -x -C "$S"` (65 knowledge entries, ledger 30696 bytes, `corpus/source-snapshots/round-46-a2/{S074.txt,manifest.json}` present).

**Fixture note (important for reading the numbers).** The F29 entry (`corpus/knowledge/github-repository-security-advisories.md`) is another seat's deliverable and is not landed in the lane, so H6 cannot be green without *a* file at that path. For the fixture only I added a size-only stand-in at that exact path (3655 bytes, a labelled placeholder with no claim, no quote, no source — scratch-only, never in the lane). Without it H6 reads `entry-bytes-ok=0`; with it H6's other limbs can be evaluated. H1/H2/H3/H5 stay red on this tree for a second, unrelated reason: the F29 README row, the S074 SOURCES row and the real entry are not landed either.

**Control (ledger unchanged, 66-entry tree):**

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py --root $S/base
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=source=0 verified-at=0 recheck=0 sections=0/4 full=0/4 table-rows=0 xrefs=0/0 anchored=0
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=spans=0 located=0 failed=0 uncited=0 cores=0/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=3/7 exit=1
```

**Test (the same tree with my append applied to the ledger):** `cat $DRAFT/ledger-append.md >> $S/append/corpus/knowledge/considerthese-proposals-ledger.md` (ledger 30696 → 40803 bytes, 146 → 165 lines), then

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py --root $S/append
gate H1 pass=0 read=rows=28 admitted=28 dup=0
gate H2 pass=0 read=source=0 verified-at=0 recheck=0 sections=0/4 full=0/4 table-rows=0 xrefs=0/0 anchored=0
gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=0
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=0 read=spans=0 located=0 failed=0 uncited=0 cores=0/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=3/7 exit=1
```

(The fixture applied the draft as first written, 10107 bytes; the shipped draft is 10146 bytes after one sentence in proposal 5 was corrected. The correction is 39 bytes inside a paragraph that H6 never reads — H6 grades the ledger's presence, name pin and size floor — so the verdict is unaffected; the shipped text was not re-fixtured because the difference is inside prose H6 does not read.)

H6's read line is byte-identical before and after the append: `knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0`. The append does not turn the attempt-2 counter's H6 limb red.

**Negative control (the limb really reads the ledger):** same tree with the ledger truncated to 1000 bytes,

```
$ python3 .../r46-f29-gate.py --root $S/shrink
gate H6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1 symlinks=0
f29-gate fixed=2/7 exit=1
```

`base-intact=0` — so H6 discriminates on the ledger's bytes/size, and the green result above is a measurement, not a vacuous pass. The mechanism is explicit in the counter: `corpus/instruments/r46-f29-gate.py:80` (`LEDGER = "considerthese-proposals-ledger.md"`), `:81` (`LEDGER_MIN_BYTES = 30696  # the ledger's byte size at the freeze tip; it may grow, never shrink`) and `:323` (`ledger_ok = os.path.getsize(os.path.join(d, LEDGER)) >= LEDGER_MIN_BYTES`); the ledger is excluded from H6's base-content pin, so growth is allowed.

## 3. Verification B — the census is unaffected, exit 0

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/base/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	/fast/scratch/hyaku/kasegi-r46/R46bExecLedgerDraft/base/corpus/SOURCES.md
census rc=0
```

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/append/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	/fast/scratch/hyaku/kasegi-r46/R46bExecLedgerDraft/append/corpus/SOURCES.md
census rc=0
```

Byte-identical apart from the path echoed in the `ok` line; exit 0 in both runs. The three `W04` warnings are the same ones the lane's own before-receipt carries (`controls/sources-census-before.txt`: `W04 S028`, `W04 S029`, `W04 S072`, `kasegi ok`). The append touches `corpus/knowledge/…` only, never `corpus/SOURCES.md`.

## 4. Risk measured — the append turns the attempt-1 counter's G6 red (the L1's amendment is a landing condition)

**Isolated on 65-entry trees** (no F29 stand-in, so the only variable is the ledger):

```
$ python3 .../corpus/instruments/r46-c2-gate.py --root $S/base65        # ledger 30696
gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1
c2-gate fixed=7/7 exit=0

$ python3 .../corpus/instruments/r46-c2-gate.py --root $S/append65      # ledger 40803 (my append)
gate G6 pass=0 read=knowledge=65 entries=65 nested-md=65 base-intact=0 entry-bytes-ok=1
c2-gate fixed=6/7 exit=1
```

The attempt-1 counter `corpus/instruments/r46-c2-gate.py` byte-pins the ledger inside its content pin (`:329` `def g6`, `:341` `base_ok = base_ok and (PINS["base-knowledge-content"] is None or cont == PINS["base-knowledge-content"])`, with `CONTENT_EXEMPT = {"claim-package-contract.md", "claim-gates.md"}` at `:71`), so growing the ledger turns G6 red. This is exactly the reason the attempt-1 lesson deferred the append (`corpus/lessons/round-46.md:29`: "C2's G6 byte-pins the 62 base knowledge entries it does not exempt, and the ledger is one of them, so editing it would turn C2 red").

**Why it matters for C1, not only for C2.** `corpus/instruments/r46-counters-selftest-c2.py:537` grades the counter on the live lane itself — `add(Case("ctl-committed-tip-direct", "control", direct=True, note="the counter run on --lane itself (the committed tip export): must read 7/7"))` — and `r46-mutbat.py:152` runs that selftest with the selftest's default `--lane` (the live lane, `r46-counters-selftest-c2.py:46` `LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"`), printing `mutbat counter=c2 BASELINE-DIRTY baseline_failures=<n>` when it fails. C1's kill rule reads "C1 fails if either battery summary at the final revision prints uncaught>0 or baseline_failures!=0". So the append is safe only together with the `r46-c2-gate.py` ledger-exemption amendment that the frozen claims' `frontier_step` already names ("considerthese ledger dispositions append (the attempt-1 routed item) lands this round together with the `r46-c2-gate.py` ledger-exemption amendment if the wave verifies it, else the deferral is carried"); without it, the deferral is carried again.

**The C1 consequence, demonstrated.** I re-ran the committed C2 selftest against a scratch copy of the lane with `--lane` pointed at the copy (read-only on the copy; the copy is a `git archive` export of lane HEAD). Control first, on the un-grown copy:

```
$ python3 .../corpus/instruments/r46-counters-selftest-c2.py --lane $S/base65 --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2
ok   control ctl-committed-tip-direct fixed=7/7 failing=[]
selftest cases=137 failures=0
selftest rc=0
```

Then on the same copy with my append applied (ledger 30696 → 40803 bytes):

```
$ python3 .../corpus/instruments/r46-counters-selftest-c2.py --lane $S/append65 --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2
FAIL control ctl-committed-tip-direct fixed=6/7 failing=['G6']  <- control-not-7/7 failing=['G6']
selftest cases=137 failures=1
selftest rc=1
```

One case flips, and it is exactly the committed-tip control: with the grown ledger the live-lane read is 6/7, so the selftest reports `failures=1`, and `r46-mutbat.py`'s baseline for that counter is then dirty (`mutbat counter=c2 BASELINE-DIRTY baseline_failures=1`), which C1's kill rule names. The append and the counter amendment therefore travel together; the append alone is not landable.

**Cross-seat check of the sibling's amendment draft** (`.ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/r46-c2-gate.py`, v1.3). The ledger half of that draft works — on my 65-entry trees it reads `gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1` with the ledger at 30696 **and** at 40803 bytes. But its G6 still requires `len(names)==65 and len(everything)==65 and nested==65` (`r46-c2-gate.py:350`) and its `base_like` (`:338`) excludes only the F28 entry, so the attempt-2 landing of the F29 entry (the 66th knowledge entry) also leaves G6 red:

```
$ python3 .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/r46-c2-gate.py --root $S/base    # 66 entries (F29 stand-in), ledger 30696
gate G6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1
c2-gate fixed=5/7 exit=1
$ python3 .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/r46-c2-gate.py --root $S/append  # 66 entries + ledger 40803
gate G6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1
c2-gate fixed=5/7 exit=1
```

So the amended attempt-1 counter needs, besides the ledger exemption, the F29 entry exempted from the base-names pin and the count raised to 66 — otherwise the C2 selftest's committed-tip control cannot read 7/7 on the final lane revision. I sent this to the owning seat (`agent://R46bExecGatePinAmend`). (The `gate G4 pass=0 read=exception-FileNotFoundError` that draft shows when run from the draft directory is a path artifact of `TOOL_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))` at `:61`, not a defect of the amendment; `corpus/instruments/source-recheck.py` resolves once the file is installed under `corpus/instruments/`.)

## 5. Evidence quoted inside the appended section (all measured by this seat)

- `python3 corpus/instruments/score-gap.py` → `gap: 22 of 65 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`.
- `python3 corpus/instruments/r46-landing-gate.py --selftest --work <scratch>` → `selftest cases=30 failures=0`.
- `python3 corpus/instruments/claim-package-selftest.py` → `selftest cases=10 failures=0` (the degenerate always-pass control is rejected by case 10).
- `git ls-tree --name-only HEAD corpus/instruments/ | grep -ic claim` → `2`; `git log --oneline -1 -- corpus/instruments/claim-package-check.py` → `5b4a850 round-43 C2: claim-package gate (8 rules) + selftest + exemplar + nine defect fixtures + S067 capture (CVE-2025-9086) + registry rows S067/S068 + entry + coverage-map note`.
- `git ls-tree -r --name-only HEAD | wc -l` → `9342`; `… | grep -c '^\.ufo/'` → `8861`; `git ls-tree -r -l HEAD | awk '{s+=$4} END {print s}'` → `151100680`; `git ls-tree -r --name-only HEAD | grep -c gitattributes` → `0`.
- `git ls-tree --name-only HEAD corpus/instruments/ | grep -c r46-landing-gate` → `1`.
- Anchors cited in the section: `SCORECARD.md:1532`, `SCORECARD.md:331`, `SCORECARD.md:1788`; `corpus/QUALITY.md:391` (R51); `SKILL.md:1163`, `corpus/instruments/README.md:1000`; `corpus/instruments/r46-landing-gate.py:113` and `:115`; `corpus/instruments/r41-closure.sh:1392-1405` (the bare-porcelain gap and `worktree_state()`); `PROVINCE.md:77` (F18) and `PROVINCE.md:171` (F28); `SHONEN.md:310` and `:311` (box 2, round-46 evidence); `corpus/lessons/round-46.md:29`; `corpus/instruments/r46-f29-gate.py:80`, `:81`, `:323`; `corpus/instruments/r46-c2-gate.py:329`, `:341`; `corpus/instruments/r46-counters-selftest-c2.py:537`.

## 6. Limitations

- The F29 entry is not in the lane, so the H6 fixture used a size-only stand-in at that path (see §2). H6's verdict is therefore a verdict about the ledger limb; H1/H2/H3/H5 were never exercised on a landed F29 tree and are another seat's and the L1's business.
- The append was applied to scratch copies, never to the live lane's tracked file (my seat may not edit tracked lane files); the live landing is the L1's integration step.
- The census was run with `--file` (the lane label in the output is `file`), not with `--root <fleet> kasegi`; the lane's own before/after receipts use the latter form.
- I did not run the mutation battery (`r46-mutbat.py`) — that is C1's own measurement and the L1's gate. My C1 consequence claim in §4 is derived from the committed battery/selftest sources (`r46-mutbat.py:152`, `r46-counters-selftest-c2.py:537`) plus the measured 6/7 and 5/7 readings above, not from a battery run at the final revision.
- The C2 selftest runs quoted in §4 were executed with `--lane` pointed at scratch copies of the lane (read-only on the copy), not against the live lane, whose ledger is not grown; the live-lane direct control therefore still reads 7/7 today. The `mutbat` summary line `BASELINE-DIRTY` itself is the battery's rendering of that failure (`r46-mutbat.py:152-156`), quoted from the committed source, not observed — I did not run the battery.
- The owning seat of the counter amendment (`R46bExecGatePinAmend`) independently reproduced my §4 readings in its own scratch and confirmed the same coupling ("my ledger exemption itself holds and discriminates … once the F29 entry and row are landed that control reads 5/7 -> selftest failures=1 -> mutbat prints BASELINE-DIRTY -> C1's kill rule (baseline_failures!=0) fires"), and keeps the 65-entry/28-row limb sentences unchanged, carrying the coupling as a risk for the L1. Its draft reads `c2-gate fixed=6/7` on my trees only because `TOOL_ROOT` resolves into the draft directory; from a tree-shaped copy under `corpus/instruments/` it reads 7/7.
- Rounds 43, 44 and 45 filed no ledger section; this section does not backfill them (their dispositions were not re-measured here).
- Shape note for the L1: the ledger's earlier round sections use a three-column table, while the card for this seat specifies one disposition paragraph per proposal; my section follows the card. Converting it to the table shape is a formatting decision for the L1 and does not change any status or pointer.
- Scratch `$S` was removed on exit; the receipts quoted above are this report's evidence, not `/tmp` paths.

## 7. Receipts and cleanup

Command receipts are in my draft directory, `.ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/`: `f29-gate-base.txt`, `f29-gate-append.txt`, `f29-gate-shrink.txt`, `census-base.txt`, `census-append.txt`, `c2-gate-base65.txt`, `c2-gate-append65.txt`, `c2-gate-v13-base65.txt`, `c2-gate-v13-append65.txt`, `c2-gate-v13-base66.txt`, `c2-gate-v13-append66.txt`, `selftest-c2-base65.txt`, `selftest-c2-append65.txt`, `selftests-instruments.txt`. The scratch tree `/fast/scratch/hyaku/kasegi-r46/R46bExecLedgerDraft` was removed on exit (`rm -rf -- "$S"`; `scratch exists? NO`). No tracked lane file was modified by this seat: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --stat` shows only `.ufo/waves/round-46/attempt2/build-wave2-spec.py` and `wave2-spec.json`, which are concurrent wave-2 preparations by other seats and not mine.

Tooling: no tool was installed or upgraded for this seat (none was needed); no pacman, uv, npm or cargo transaction was run.
