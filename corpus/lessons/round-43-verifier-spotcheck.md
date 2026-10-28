# round-43 verifier spot-check — kasegi (non-author)

author: hyaku closure (non-author integrator, @m_zfl)

- lane-round: **kasegi 43**; base `ab98fac9dce87130bc4f66de89e30650d63943dc`; judged head **J** `3634ec948a9ee78cb13ba86ef60871216391636a`; receipt **Y** `fdc20ad6a0c50ec425bf728861dba360d4c84861`; lane tip `dbd2e106e35ac5ad14ea80f4c634d3fbf11853fb` (branch `master`, `ahead=0`, `behind=0`).
- report: `.ufo/reports/round-43/kasegi.md`, commit `fdf719a92d8d305d5465f8087c5af90a8900a172`, author `kasegi-shokunin <kasegi@shokunin.local>`.
- dispatch digest (copied from the mutable log; this digest, not the live log, is the pointer):
  - `2026-10-28T13:29:27-03:00 launch kasegi round=43 pgid=3638835 driver=hyaku-inline attempt=1`
  - `2026-10-28T15:14:29-03:00 complete kasegi round=43; hyaku-inline attempt=1`
- method: read-only re-derivation over **committed bytes** (`git show`/`git grep`/`git ls-tree`/`sha256sum`/`wc`/`jq`/`awk` plus one live HTTP re-open per source). The lane's gates were **not executed** — PROTOCOL §Gate standard (Closure consequence) has the integrator verify a gate's committed evidence, never run a sibling's gate. Six read-only reviewer/critic seats ran in parallel against the same revisions; their commands are folded into the rows below.

## 1. Conformance (step 1)

| item | result | command / observed |
|---|---|---|
| report committed by the lane identity | **ok** | `git log --format='%an %ae %H' -- .ufo/reports/round-43/kasegi.md` → `kasegi-shokunin kasegi@shokunin.local fdf719a9…` |
| `SHONEN` heading, one line per box | **ok** | `grep -c '^## SHONEN'` → `1`; four `- [~] …` lines, each with a resolvable pointer (no `[x]`, `grep -c '^- \[x\]'` → `0`) |
| report sections in order | **ok** | `grep -n '^## '` → Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN, then Mistakes / Open / Stale-lane / Tooling |
| every cited lane commit exists and is an ancestor | **ok** | 12/12: `4cb6d4ae 5b4a8503 a6c1d462 ffe197d1 9e6800ea 6c360f4c 0a24364d f2dee6c0 2448a7d2 2fccc781 3634ec94 fdc20ad6` — each `git merge-base --is-ancestor <full> master` → true |
| lane repo has no uncommitted round work | **defect (minor)** | `jj-lane.sh state` → `local=dbd2e106 remote=dbd2e106 ahead=0 behind=0`; `git status --porcelain` → one untracked leftover `.ufo/waves/round-43/final-gates/all-gates.at-Y.txt.tmp` (2137 B). Nothing tracked is dirty; the `.tmp` is an aborted-write leftover, not round work. |
| prompt carries the template contract | **ok** | sections 1–5 of `.ufo/prompts/kasegi-round-43.md` diff against `templates/round-prompt.md` (rendered with the lane substitutions) with **one** hunk — the `<{{LANE}}-repo>` → `kasegi-shokunin` substitution. Round-level items (i)–(v) and all five child-lane items are present; §3's L2 floor (`≥8 in ONE batched call`) matches `MISSION.md` §L2 concurrency, whose role-class route table is advisory to host routing (the addendum's run-11 alias map is the operator's label, not a second floor). |
| marker test | **not a marker** | the report names twelve real commits, per-claim counting commands, controls and receipts → a real report |

Additional conformance defects, all status-neutral:

- the report carries **no planner=L1 mapping** and **no L2-floor / residual-call record**, which `scripts/hyaku/lane-addendum.md:233-241` and the wave bullet make mandatory (`grep -ci planner` → `0`; `grep -ciE 'residual|L2 floor'` → `0`);
- `.ufo/waves/round-43/w1-REGISTRY.txt:7` reads `names=` with zero names while the same file asserts `seats=73` (the seat set is attested only by `w1-dispatch.json .registry.members` and `w1.ready.dispatched`, both 73);
- `SHONEN.md` lost its final empty line (`git diff --stat ab98fac9 dbd2e106 -- SHONEN.md` → `9 +-`; base tail `…\n\n`, tip `…\n`) in the `0a24364d` restore-and-reappend; no box changed;
- `.ufo/waves/round-43/final-gates/r42-at-de09313-selftest.txt` carries no `export-ref`/`de09313` token, so the RD42-5 transcript pair is only half self-identifying (the run file does name it);
- the report's SHONEN bullet says "the two new instruments are registered in `corpus/instruments/README.md`"; `git grep` there → 0 hits (the gate is registered in `corpus/README.md`'s round-43 note; `r43-closure.sh` in neither).

## 2. Per-claim re-check

### C1 — `depth:verifiability` (score 4, held)

| re-check | command | observed | verdict |
|---|---|---|---|
| before: suite absent at base | `git ls-tree ab98fac9 corpus/instruments/r43-closure.sh` | empty (and `git cat-file -e` → rc 128) | agree |
| after: suite present at tip | `git ls-tree dbd2e106 corpus/instruments/r43-closure.sh` | `100755 blob 97038e41…` | agree |
| six new limbs | `git ls-tree -r --name-only dbd2e106 corpus/instruments/r43-limbs/` | `k14-corrections.sh … k19-freeze.sh` (6) | agree |
| suite digest binds the receipts | `git show dbd2e106:corpus/instruments/r43-closure.sh \| sha256sum` | `a832908e15f49de89066d8168a833d3ffa0f5fad432ba1c2b5a813ba45bef168` = `suite-sha256=` in both `all-gates.txt` and `all-gates.at-Y.txt` | agree |
| after: 19/19 at Y | `grep -c 'payload=' .ufo/waves/round-43/final-gates/all-gates.at-Y.txt`; `grep -oE 'K[0-9]+ payload='` | 19 payload lines, ids `K1…K19` sequential; `closed=19/19 exit=0`; `export-ref=fdc20ad6…` | agree |
| selftest tally | `grep -c 'selftest case='`; `grep -o 'verdict=[a-z]*'` | 19 case lines, 19 × `verdict=pass`; `selftest cases=19 failures=0` | agree |
| receipt is the J-run tee, K8 open by construction | `grep -nE 'export-ref=\|closed=\|payload-match=\|forged=' .ufo/waves/round-43/final-gates/all-gates.txt` | `export-ref=3634ec94…`; `closed=18/19 exit=1`; one `closed=0`, on K8; K8 payload `payload-match=18/18,forged=3/3` | agree |
| the transcript is exactly one commit after the receipt | `git diff --stat fdc20ad6 dbd2e106`; `git rev-list --parents -n 3 dbd2e106` | `1 file changed, 45 insertions(+)` = `all-gates.at-Y.txt`; chain `dbd2e106 ← fdc20ad6 ← 3634ec94` | agree |
| base-red limb is transcript-backed **per limb** | `git grep -n 'K1[4-9] payload=' .ufo/waves/round-43/w1/ExecK1*.transcript.txt` | K14 `stale=1 … closed=0`; K15 `unbacked=3 … closed=0`; K16 `promises=1,unresolved=1 … closed=0`; K19 `freeze=absent,order=bad … closed=0` at `ab98fac9`; limb shas equal the tip limbs (`4a4945b0 14a195b1 d7c33c9e 37a513ed 3551a0fc 75f9552e`) | agree |
| the composite `closed=13/19` base tally | `git grep -n '13/19' dbd2e106 -- .ufo/waves/round-43` | only draft-run sources: `ExecCarryChecks.transcript.txt` (`payload=limb=absent`), `CritBaselineEscape.md` (`payload=stub`); committed seats derive 12/19 or 11/19; **no committed run of `a832908e…` at `ab98fac9`** | **disagree (defect, see §6)** |

C1 verdict: **verifies as measured.** The after-state (`closed=19/19 exit=0` at Y, `selftest cases=19 failures=0`, receipt `18/19` with K8 as the disclosed self-reference) reproduces from committed bytes and the digests bind; the base-red requirement is backed per limb. The composite `13/19` figure is an unbacked summary of a measurement that is otherwise established.

### C2 — `coverage` (score 8, held; capability acquisition)

| re-check | command | observed | verdict |
|---|---|---|---|
| before: gate and fixtures absent at base | `git cat-file -e ab98fac9:corpus/instruments/claim-package-check.py` (and fixtures dir) | rc 128 / 0 files | agree |
| after: present at tip | `git ls-tree -r dbd2e106 -- corpus/instruments/fixtures/claim-package/` | 108 files: 9 `defect-*` dirs + `exemplar/` carrying the six contract files (`claim_checklist.md`, `custodian-receipts.json`, `provenance.json`, `report.md`, `status.json`, `evidence/manifest.json`) | agree |
| gate digest binds the green run | `git show dbd2e106:corpus/instruments/claim-package-check.py \| sha256sum` | `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` = the digest `ExecEntryGateRecheck.transcript.txt` measured at HEAD `5b4a8503` | agree |
| eight rules | `git show dbd2e106:…/claim-package-check.py \| grep -oE 'R-[A-Z]+' \| sort -u` | `R-CUSTODIAN R-FILES R-MANIFEST R-NOSECRET R-PROVENANCE R-REDACT R-REPORT R-STATUS` (8) | agree |
| exemplar green + selftest green | `ExecEntryGateRecheck.transcript.txt` §3–§5 | at `5b4a8503`: `selftest cases=10 failures=0`; `package=… rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`; `exit=0` from three cwds; mutant (forced-pass R-REPORT) → `exit=1`, `cases=10 failures=1` | agree (measured at `5b4a8503`) |
| the green run transfers to the tip | `git diff --name-only 5b4a8503 dbd2e106 -- corpus/instruments/claim-package-check.py corpus/instruments/claim-package-selftest.py corpus/instruments/fixtures/claim-package corpus/knowledge/claim-package-gate.md` | **empty** — gate, companion and fixtures byte-identical; entry `f53109d8…` identical | agree |
| fix shown able to fail | `tail -15 .ufo/waves/round-43/w1/ExecGateSelftest.transcript.txt`; `CritC2DoNothing.md` §1–§2 | red-before ends `selftest cases=10 failures=9` / `exit=1`; critic receipt: nine fixtures each `pass=7 fail=1 verdict=DEFECT exit=1` on their own rule, always-pass stand-in `observed=rejected-9/9` | agree |
| registry / knowledge / binding | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`; `ls corpus/knowledge/*.md \| wc -l`; `grep -rlE '^source: S067' corpus/knowledge \| wc -l` | 68 (66 at base); 62 (61 at base); 1 | agree |
| capture binding `records=57` | `python3` over `corpus/source-snapshots/**/manifest.json` (plain read, instrument not executed) | 19 manifest dirs, **57** records (18/56 at base); `git diff --name-status ab98fac9 dbd2e106 -- corpus/source-snapshots/` → only `round-43/S067.txt` + `manifest.json` added, so the 56 base-bound records are untouched; the new record hand-checked: path resolves, `sha256 7e35413a…` matches the file, `bytes 10455` matches the live fetch, `lines 109` | agree (re-derived) |
| audit `expected=62` | `git show dbd2e106:corpus/instruments/knowledge-expected.txt \| grep -v '^#' \| sort` vs `git ls-tree -r --name-only dbd2e106 corpus/knowledge/ \| grep '\.md$' \| sort` | `diff` → identical, 62 lines each | agree (re-derived) |
| frontier harness `entries=28 pass=28` | `git diff ab98fac9 dbd2e106 -- corpus/README.md`; `grep -cE '^\|[[:space:]]*F[0-9]+'` | 25 F rows at base **and** tip, 25 `admitted`; README append-only (12+/0−); no frontier entry references the round-43 manifest (`grep -c` → 0) → harness inputs unchanged, verdict invariant | agree (invariance, not re-executed) |
| census | `scripts/sources-census.sh validate --root … kasegi` | `W04 S028`, `W04 S029`, `ok`, **exit 0** — identical to `census-before.txt` | agree |
| SOURCES append-only | `git diff --numstat ab98fac9 dbd2e106 -- corpus/SOURCES.md` | `3 0` — three added lines, **zero** removed; no pre-existing row's status/recheck/used-by cell changed | agree |

C2 verdict: **verifies.** Five of the report's quoted tokens reproduce at the tip by plain measurement, three by invariance/byte-identity from a pre-tip green run whose inputs did not move.

## 3. Per-axis verdicts

| axis | before | after | verdict | evidence |
|---|---|---|---|---|
| `depth:verifiability` | 4 (r42 row: held, `closed=13/13`; six routed narrative defects ungraded) | 4 held — suite extended 13 → 19 checks, six new narrative-evidence checks red at base and green at Y, `selftest cases=19 failures=0` | **unchanged** | the score is held and no score move is claimed; the increment is graded under the quality trend (same reading the r40–r42 closures gave this axis). No regression: all 13 carried checks still replay their committed defeats |
| `coverage` | 8 (registry 66, knowledge 61, binding 56, frontier 25) | 8 held — registry 68 (S067 `mined`, S068 `rejected` + flip), knowledge 62, binding 57, a new executable gate over a surface that was documentation-only, capability row enters | **improved** | registry/knowledge/capability movement re-derived above; frontier ratio deliberately unchanged (25/25) and recorded as such |
| `depth:density` | 9 | 9 held | **unchanged** | `corpus/instruments/density.py` byte-identical at base and tip (`ee803726…`); no density claim made; no harm |

No axis is **harmed**: `SKILL.md` and `PROVINCE.md` are byte-identical base→tip (`git diff` → 0 lines; blobs `073a7b61…`, `63d791a2…`); no deleted files (`git diff --diff-filter=D` → empty); `LOG.md` (157+/0−), `corpus/QUALITY.md` (18+/0−), `corpus/README.md` (12+/0−) and `SCORECARD.md` (29+/0−) are append-only.

## 4. Discernment spot-check (LEARNING.md — checked from outside)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S067 — curl security advisory CVE-2025-9086 | **admit** (tier A `docs`, `mined`) | live `https://curl.se/docs/CVE-2025-9086.html` (HTTP 200, 10455 B) **and** the committed capture `corpus/source-snapshots/round-43/S067.txt` (sha256 `7e35413a…`, 109 lines, 3822 B) | **agree** | all seven located quotes exist verbatim on the re-opened page and sit at exactly L69/L82/L83/L88/L89/L97/L103 of the capture; the capture digest is pinned in the row's anchor cell with fetch time and per-fact line locators; the row is not a bare homepage |
| S068 — GHSA-v676-f8gm-92r9 | **reject** (tier B, reason + flip) | live `https://github.com/advisories/GHSA-v676-f8gm-92r9` (HTTP 200, 141796 B — the lane's "not byte-stable, 141794–141796" holds) | **agree** | every reject ground reproduces: `Unreviewed`, `High severity` 7.5 against the vendor's `Low`, `No package listed`, affected **and** patched versions `Unknown`, `No known source code`, published by the NVD. The flip condition is falsifiable (status becomes `Reviewed`; or the curl package with per-version ranges / commit `c6ae07c6…`) |
| S067 quote discipline | ≤25-word quotes | same two sources; `awk '{print NF}'` over the seven quotes | **agree (with one numeric slip)** | counts 8/3/2/8/9/2/19 — none over 25 and the lane's stated counts are exact. **But** the lesson calls the fix pointer a "29-character prefix" (L90, L101) where the measured prefix is **26** chars (`c6ae07c6a541e0e96d0040afb6`); the full 40-char hash `c6ae07c6a541e0e96d0040afb62b45dd37711300` is real (curl's JSON sibling) |
| S067/S068 not double-counted | rows touched old→new: none | `git diff ab98fac9 dbd2e106 -- corpus/SOURCES.md` | **agree** | 3 added lines, 0 removed; the 66 pre-existing rows keep every cell |
| degenerate-control rejection (gate taste) | nine defect fixtures + always-pass stand-in rejected | `CritC2DoNothing.md` §1–§2, `ExecGateSelftest.transcript.txt` | **agree** | the lane's own critic proves the gate discriminates (each fixture fails exactly its own rule) and that a stand-in printing the target line is rejected 9/9 |

## 5. Trend verdicts

- **expansion — improved.** Registry 66 → 68 with one tier-A `mined` row opened this round and one recorded reject carrying its flip; knowledge 61 → 62; and a capability (`claim-package-gate`) admitted to the SCORECARD repertoire with a working demonstration — `AXES.md` §Capabilities counts a capability admission as an expansion observable. Frontier deliberately unchanged (25/25), and the round says so.
- **quality — improved.** Six routed narrative/hygiene defect classes (RD42-1/-2/-3/-4/-5/-6/-8) are now machine-graded by K14–K19, each red at base and each rejecting a mutant built from the committed defeat bytes; the missing `de09313` transcript is committed so the one unbacked quote is bound; `corpus/QUALITY.md` gains R43–R46 with the lesson behind each. No admitted knowledge entry fails a re-check. Caveat carried into §6: one new composite figure in the lane's own records (`closed=13/19`) is not graded by any check and is not backed by a run of the landed suite.
- **discernment — improved.** The outside spot-check agrees with the gate on both sampled decisions (one admit, one reject) after re-opening both sources live; the gate rejects nine deliberate defects and a degenerate always-pass control; and the round reports its own C1 receipt as 18 of 19 with K8 open rather than dressing the self-reference as a pass. The one disagreement it did produce is a prose numeral (§6), not a gate decision.

## 6. Routed defects — the lane must fix these in round 44

Each lands as an appended correction or a new lesson row, never as an in-place rewrite (PROTOCOL §Evidence standard; `CORPUS.md` corrections clause).

1. **`closed=13/19` is unbacked (highest priority).** `SCORECARD.md`'s round-43 move-log row and `.ufo/waves/round-43/claims.json` C1 `before` state the base export prints `closed=13/19 exit=1 with exactly K14-K19 open`. No committed run of the landed suite (`a832908e…`) at `ab98fac9` exists; the figure comes from a stub/draft suite (`CritBaselineEscape.md` "produced with the six stubs", `ExecCarryChecks.transcript.txt` `payload=limb=absent`), while committed seats derive 12/19 or 11/19. Append a `Correction (round 43)` naming the literal superseded by the per-limb base result (six per-limb transcripts, all red), or commit a base run of the landed suite.
2. **No check can see defect 1.** `k18-transcript.sh` excludes `SCORECARD.md` as a quote source and K17's escape reads only `claims-erratum*.md`, which never names `13/19`. Close it by adding the missing erratum paragraph (K17's existing escape then covers it) rather than widening K18 — and say which.
3. **Lesson numeral wrong.** `corpus/lessons/round-43.md` L90 and L101 call the fix pointer a "29-character prefix"; it is **26** characters (`c6ae07c6a541e0e96d0040afb6`), full hash `c6ae07c6a541e0e96d0040afb62b45dd37711300`. A numeric claim needs its counting command; append a correction.
4. **Report omissions against the wave contract.** The report records neither the planner=L1 mapping (`lane-addendum.md:238`) nor the L2-floor/residual-call line; both are mandatory report content. Record them next round (and in the next round's report shape).
5. **Wave-evidence hygiene.** `.ufo/waves/round-43/w1-REGISTRY.txt:7` is `names=` empty while asserting `seats=73`; `final-gates/r42-at-de09313-selftest.txt` names no `export-ref`; `final-gates/all-gates.at-Y.txt.tmp` is an untracked aborted-write leftover (2137 B) still in the tree. Fix the emitter and delete the leftover through the lane helper.
6. **`SHONEN.md` lost one base byte** (final empty line) in the `0a24364d` restore-and-reappend; `git diff ab98fac9 dbd2e106 -- SHONEN.md` → `9 +-`. Restore the blank line when the file is next appended.
7. **Report pointer retarget.** The SHONEN bullet says both new instruments are registered in `corpus/instruments/README.md`; `git grep` there → 0 hits. Retarget the pointer or append the two rows.
8. **Before-cell token.** `claims.json` C1 `before` and the report's C1 cell say the base suite run exits `127`, citing `c1-controls/do-nothing.txt`, which prints `exit=2` for its `ls` (§A). 127 is the shell's not-found code for running the missing script, not a value the cited control prints; either measure it (run the absent path) or cite the control's own token.

## 7. Note for the operator (promotion is operator-owned)

All four `SHONEN.md` boxes are stated `[~]` with resolvable pointers, and — as a non-author — I could check three of them mechanically (box 1 by `density.py`/`anchorcheck.py` receipts and the byte-unchanged `SKILL.md`; box 3 by the two instruments' documented CLIs and committed exit-0 runs; box 4 by the byte-unchanged `PROVINCE.md` plus the sibling-overlap ruling). Box 2 is the one that cannot be checked: the round's package is `claimable:false` with operator gates open and no submission was performed, so it stays an asserted `[~]`. Writing `[x]` is not this role's act; the record says so rather than implying a pass.
