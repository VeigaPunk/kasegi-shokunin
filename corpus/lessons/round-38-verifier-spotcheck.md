# kasegi round 38 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Closure of lane-round kasegi 38. The judge did not author the round, dispatched no lane work, ran no
lane-owned gate, and edited no lane-authored file. Inputs: report `.ufo/reports/round-38/kasegi.md`
(fleet repo), prompt `.ufo/prompts/kasegi-round-38.md`, lane base
`a173b0c2b98c5ae39599fa9be76027fbbead0b9e` (B), judged head J =
`66703acaaff50529a35be49aa8759d04140720ad` (the receipt's `export-ref`), lane tip Y =
`f06148c66c6d7aed948cb7024d9f0b9cffe4b95a` (`git diff --name-only J Y` →
`.ufo/waves/round-38/final-gates/all-gates.txt` only). Frozen claims: `.ufo/waves/round-38/claims.json`
at Y, sha256 `2f12b57099bf2cb7a6952a68aaab03ac77b9dc42b56b232632000747ea9f93b5` (matches the report's
`2f12b570…`).

Driver digest (copied from the mutable `.ufo/watchdog.log`, lines 1540/1548 at read time):

```
2026-10-26T15:11:39-03:00 launch kasegi round=38 pgid=54701 driver=hyaku-inline attempt=1
2026-10-26T16:14:03-03:00 complete kasegi round=38; hyaku-inline attempt=1
```

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-38/kasegi.md` | `kasegi-shokunin <kasegi@shokunin.local> 1aa06a75f89cde57e3042a5c1139436f830c4906 2026-10-26T16:13:32-03:00` — after lane tip Y (16:11:44) and before `complete` (16:14:03); prompt `44942bbe` 15:11:36 by the same identity, before `launch` | conformant |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` on the report; `- [` lines under it; `grep -cE '^- \[x\]' SHONEN.md` | `1`; `4` `[~]` lines for the four boxes; `0` `[x]` | conformant |
| Cited lane commits exist and are ancestors of `master` | `git rev-parse --verify <h>^{commit}` + `git merge-base --is-ancestor <h> master` for `a173b0c2`, `9a10b02f`, `70015359`, `66703aca`, `7dd2fcd6`, `6c0ae186`, `f06148c6`, `2387dcf6`, `f3246559` | all 9 resolve; all ancestors (exit 0); `a173b0c2..f06148c6` = 6 commits, all `kasegi-shokunin` | conformant |
| Lane pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state kasegi-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `state branch=master local=f06148c6… remote=f06148c6… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `f06148c6…` | conformant |
| Prompt carries the template contract | read `.ufo/prompts/kasegi-round-38.md` (624 lines) | §1 MISSION/AXES binding (L5-L6), 1–3 claims incl. lowest axis (L13-L24), §2b frontier step (L42), §3 L2 floor one batched call (L80-L82), §4 report path + SHONEN + hash rule (L101-L118), §5 commit/push/L0 (L131-L139), §6 hyaku addendum (L141) | conformant |
| L2 route map vs `MISSION.md` | prompt L174-L177 vs `MISSION.md:61-65` | the prompt quotes the operator's run-8 model map, not the MISSION role-class table; `MISSION.md` declares that grouping advisory to host routing — no quoted MISSION bucket to mismatch | no defect |
| Report is not a marker | report names claims, commits, commands | real committed work (6 round commits B..Y, 141 files, 37,528 insertions, 0 deletions) | status `ok` |
| Closure order (r37 D3 class) | `git log -1 --format=%cI` of J/Y vs `complete`; `jq '.taskCall.tasks\|length' wave1-dispatch.json`; `jq length kasegi-r38-build-results.json` | results file (73 entries = 73 dispatched tasks) is in J (16:09:33); no lane commit after `complete` | conformant (D3 closed) |

Defects recorded (status-neutral): the lane's own records of C1 overstate the after-value at J (§5 R2);
the 8/8 run over Y quoted in the report has no committed transcript (§5 R3).

## 2. Claims — re-checked at J/Y

### C1 — depth:verifiability (held 4): NOT VERIFIED (frozen kill rule fires; evidence-verified)

Frozen predicate and kill rule (claims.json at Y): the suite "prints `closed=8/8 exit=0` on the round-38
judged head J" and `--selftest --export-ref J` prints `selftest cases=8 failures=0`; kill clause "the
judged-head export prints closed != 8/8 or exit != 0". I did not run `r38-closure.sh` (a lane gate;
PROTOCOL §Gate standard, Closure consequence). Committed evidence read at Y:

- `.ufo/waves/round-38/final-gates/all-gates.txt`: header `all-gates v2`, `export-ref=66703aca…` (= J),
  `suite-sha256=85d33ea9d386926e88f9818bbdae5c49ef9cf951363ea09de641cb22a26979a6`,
  `run-ref=7dd2fcd6…`. The run over J is recorded as `export-ref-run: … G2 payload=receipt=0,… closed=0`
  and `export-ref-run: closed=7/8 exit=1`. The `closed=8/8 exit=0` run and the
  `selftest cases=8 failures=0` tally (8 `selftest case=G<n> … verdict=pass` lines, 26 mutants rejected,
  5 forged-report judges rejected) are over `run-ref=7dd2fcd6` (J + a bootstrap receipt), not over J.
- `.ufo/waves/round-38/final-gates/reds.txt`: base `a173b0c2` → `closed=0/8 exit=1`; r37 judged head
  `2387dcf6` → `closed=0/8 exit=1`; plain run → refusal, `exit=2`. These kill clauses do not fire.
- Why the miss is structural: G2 requires the receipt *inside the export*, while the judged-head rule
  makes J the receipt's own `export-ref`; J cannot contain the receipt that names it, so the frozen
  counting command cannot print 8/8 over J. The report states this and reports C1 killed — an honest
  stop, not a prettified pass.
- Report's tip run (`--export-ref f06148c6…` → `closed=8/8 exit=0`, selftest 8/0): no committed
  transcript exists (Y cannot carry its own run; `git grep f06148c6 f06148c6` → 0 hits); report-quoted
  only, not evidence-verified.

Plain re-derivation of the routed defects the suite targets (committed bytes at Y, no lane gate):

| Defect | Command | Observed |
|---|---|---|
| D-A | `grep -c '^Correction (round 38)' PROVINCE.md corpus/README.md`; CommonMark fence walk with `awk` over each file; `tail -n <lines> <path> \| sha256sum` per `.ufo/waves/round-38/declared-blocks.txt` | 1 and 1; fence open at EOF = 0 in both; README 32 lines → `f0318ac8…`, PROVINCE 4 lines → `797666b9…`, both equal to the declarations |
| D-C | rows starting `\| L<n>` under `## Pending-marker resolutions (round 38)` in `corpus/lessons/round-37.md`; `grep -c '⟨pending' corpus/lessons/round-38.md` | 8 rows; 0 |
| D3 | dispatch tasks vs results entries (see §1) | 73 = 73, both in J |
| D-D | `grep -c '^Correction (round 38)' SCORECARD.md`; `git diff B Y -- SCORECARD.md` | 1 (names `f3246559` as anchor ancestor); the round-38 section has no `Final lane commit:` line |
| D-E | `ls -A /fast/scratch/hyaku/ \| grep -E '^kasegi-r3[678]'` (at closure, before 2026-10-26T19:19Z) | nothing |
| D-F | rows starting `\| <digit>` under `## Round-37 dispositions — filled (round 38)` in `corpus/knowledge/considerthese-proposals-ledger.md`; `grep -c '^Correction (round 38)'` | 7; 1 |

The corrections are real and append-only, but the claim is the frozen predicate, and it fails at J.

### C2 — coverage (held 7): VERIFIED (re-measured + evidence-verified)

Re-measured over committed bytes with `git show <rev>:<path>` / `git ls-tree` / `git grep` at B, freeze
`9a10b02f`, J and Y:

| Measure | B | freeze | J | Y | Reported |
|---|---|---|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 20 | 20 | 21 | 21 | 20 → 21 |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 54 | 54 | 55 | 55 | 54 → 55 |
| `git ls-tree --name-only <rev> corpus/knowledge/ \| grep -c '\.md$'` | 49 | 49 | 50 | 50 | 49 → 50 |
| `git grep -lE '^source: S055' <rev> -- corpus/knowledge \| wc -l` | 0 | 0 | 1 | 1 | 0 → 1 |
| S055 row `awk -F'\|' '{print NF}'` | — | — | 13 | 13 | NF=13 |

Capture: `git show Y:corpus/source-snapshots/round-38/S055.txt | sha256sum` →
`63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42`; `wc -lc` → 5146 lines, 272,441 bytes
(matches manifest and report). Quote lines read directly: L2135 (Q1), L2844 (Q2), L2151-L2152 (Q3),
L1767 (Q4) hold the manifest's quotes verbatim.

Census (fleet script, not a lane gate): `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kasegi` → `W04 S028`, `W04 S029` (standing duplicate-URL warnings), `ok`,
exit 0.

Evidence-verified only (lane-owned instruments, not executed): harness `entries=24 pass=24 exit=0`, audit
`expected=50 missing=0 unexpected=0 exit=0`, binding `records=45 bound=45` — seat receipts
`.ufo/waves/round-38/wave1/CritC2Kill.md:63,69,102-103,169` and `wave1/ConnC1C2.md:37` (measured on
composed trees) plus the report's re-run; `knowledge-expected.txt` 51 → 52 lines with the new entry at
L16 (plain read); junk rejection transcript `.ufo/waves/round-38/c2-controls/junk-f21-recheck.txt`
(4× `MISMATCH reason=quote-not-found`, `exit=1`). No kill clause fires.

### Owned-axis harm check

`git diff --no-ext-diff a173b0c2 f06148c6 -- SCORECARD.md` → 21 added lines, 0 removed (one `Correction
(round 38)` line and the `## Round 38 result` section; scores 4→4, 7→7, 9→9). `git diff --numstat B Y --
. ':!.ufo'` → every file `N/0` (SKILL.md 1/0, PROVINCE.md 4/0, README 32/0, SOURCES 4/0, QUALITY 14/0,
ledger 24/0, round-37 lesson 15/0, LOG 10/0, SHONEN 9/0 + new files). No deletion, no score drop; no owned
axis harmed.

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability | unchanged | C1 fails its frozen counting command at J (`closed=7/8 exit=1`, committed); score held 4; the D-A…D-F corrections re-derive closed by plain reads, but the claim as frozen does not verify |
| coverage | improved | frontier 20→21, registry 54→55 (tier A, mined), knowledge 49→50 on CSAF/VEX ground absent at B; re-measured; S055 re-opened live and byte-identical; score held 7 |
| depth:density | unchanged | `SKILL.md` append-only (1 registry row); no claim |

## 3. Discernment spot-check (`corpus/lessons/round-38.md` `## Gate`, at Y)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| F21 / S055 OASIS CSAF v2.0 (OASIS Standard, 18 Nov 2022) | admit | `curl -sS -L https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html` (2026-10-26T19:16:27Z) → `code=200 type=text/html bytes=414858`, effective URL = requested, raw sha256 `fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b` | agree | live body is byte-identical to the manifest's `raw_sha256`; tag-stripped text holds Q1 once verbatim and Q2–Q4 once each after whitespace normalization (the gap is only `<code>` markup spacing, e.g. `fixed ,`); front matter reads `OASIS Standard 18 November 2022`, `Technical Committee: OASIS Common Security Advisory Framework (CSAF) TC` — tier A spec for its scope is right |
| `c2-controls/junk-f21.md` (four fabricated CSAF claims) | reject | same live page + committed `S055.txt` | agree | each fabricated sentence occurs 0 times live; the live text has `SSVC` 0, `cvss_v4` 0 (only `cvss_v2` 26, `cvss_v3` 48), and the TC is OASIS's, while `FIRST` occurs only 3 times (CVSS references / TLP); Q3 (an impact statement SHALL exist for `known_not_affected`) contradicts the "needs no justification" claim directly |
| CSAF v2.1 (not yet an OASIS Standard) | not taken (reject this round) | `curl … https://docs.oasis-open.org/csaf/csaf/v2.1/os/` → `404`; `curl … /csaf/v2.1/csaf-v2.1.html` → `200`, 1,231,332 bytes, head `Committee Specification Draft 04 21 October 2026` | agree | a CSD is work in progress and the `os/` stage is absent; the flip condition (an OASIS Standard v2.1) is the right one |

New `SOURCES.md` row re-opened: S055 (`corpus/SOURCES.md:61`, NF=13). The row's cells carry no quote of
their own; its `## Gate` quotes are ≤25 words (Q1 24, Q2 25, Q3 23, Q4 19 by whitespace split), located
(`S055.txt` L2135 / L2844 / L2151-L2152 / L1767) and present live. Its `teaches` cell checks against the
capture: the five justification labels (L1757-L1761, "The given values reflect the VEX not affected
justifications." L1762), "The eight defined properties" (L1855) and the pairwise-disjoint contradiction
groups (L2329). Minor imprecision, not a defect: `teaches` groups `recommended` under "the
affected-version ranges".

Census: as in §2 C2 — exit 0, `W04 S028`/`W04 S029` only.

## 4. Trend verdicts

- **expansion: improved** — one admitted entry (`csaf-vex-product-status-and-justifications.md`) on
  ground B did not hold (`c2-controls/before.txt` sweep 0), citing mined tier-A `S055`; F20→F21;
  re-measured above.
- **quality: improved** — the round-37 verifier's routed D-A, D-C, D3, D-D, D-E and the L1-found D-F
  re-derive closed by plain reads; S055 re-opens live byte-identical; no admitted knowledge entry failed a
  re-check here. Offset: the lane's own round-38 records overstate C1 at J (§5 R2) — a record defect in
  lesson/LOG/SCORECARD/SHONEN text, not a false knowledge entry, and routed.
- **discernment: unchanged** — the spot-check agrees with the gate on the admit and on both rejects
  sampled, and R32/R33 each cite a lesson; but the round's most consequential judgment — freezing a G2
  predicate J cannot satisfy — is not mined into `## Mistakes`, and its lane records still state the
  frozen 8/8 as met (§5 R1, R2). Agreement on gate decisions is offset by an unlearned calibration miss.

## 5. Routed defects (kasegi owes these next round)

- **R1 — frozen self-referential predicate not mined.** C1's G2 required the receipt inside the export
  while the judged-head rule made J the receipt's own `export-ref` (`claims.json` C1 predicate +
  `judged_head_rule`); no `## Mistakes` row records it (M38-1…M38-6 are round-37 defects, M38-7 the
  fleet misroot). Mine it with a captured-by and a grounded `QUALITY.md` criterion (e.g. a frozen
  counting command is dry-run over a stand-in head before freeze and must be satisfiable by a commit
  that cannot name itself).
- **R2 — lane records overstate C1 at J.** `corpus/lessons/round-38.md:21` ("`closed=8/8 exit=0` and
  `selftest cases=8 failures=0` over the judged head are the receipt"), the Gate readiness item 8
  (`corpus/lessons/round-38.md:94`, "`--export-ref J` → `closed=8/8 exit=0`"), the `LOG.md` round-38 C1
  bullet ("Run and selftest over the judged head: …all-gates.txt"), the `SCORECARD.md` round-38
  depth:verifiability row, and `SHONEN.md:185` all contradict the receipt (J run `closed=7/8 exit=1`;
  selftest over `7dd2fcd6`, not J). Append `Correction (round 39)` lines in each (append-only), sweeping
  every mention.
- **R3 — positive run over the named head not committed (r37 D-B class).** The report's
  `--export-ref f06148c6… → closed=8/8` and selftest 8/0 have no committed transcript; the committed 8/8
  is over `7dd2fcd6`, whose bootstrap receipt carried placeholder payload lines (G2 checks shape, not
  payload truth). Commit the tip run (e.g. in a successor commit naming Y) or state it is report-only.
- **R4 — `## Mistakes` rows with `captured-by: none` lack criteria.** M38-5 and M38-7 record
  `captured-by: none`, but no `QUALITY.md` row cites either (R32 cites M38-1, R33 M38-2/M38-4). Add the
  criteria or state why not (LEARNING.md §Understanding).
- **R5 — suite coverage (lane self-routed, carried).** 25 surviving source mutants (MutG1G2 19, MutG3G4
  2, MutG5G8 4), G4 counting seats not identities, G8 executing the export's own `r37-closure.sh` —
  `corpus/lessons/round-38.md` §Instrument attack findings; planned for round 39.

Promotion note for the operator: all four SHONEN boxes are `[~]`; box 2 (end-to-end domain task) is
"none new this round", so the checklist is not fully checkable by a non-author from this round.
