# kasegi round 37 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Closure of lane-round kasegi 37. The judge did not author the round, dispatched no lane work, and edited no
lane-authored file. Inputs: report `.ufo/reports/round-37/kasegi.md` (fleet repo), prompt
`.ufo/prompts/kasegi-round-37.md`, lane base `b56a41680cefd391868c1c370dc063c69d827e7d` (B), judged head
`2387dcf6ccfefcfb703783387b9aade8fc82abfa` (A). Branch tip at closure:
`83975acc83df4bd8d5eaf463182ae615f2b64546` (15:03:15-03:00, after `complete`; touches only
`.ufo/waves/round-37/kasegi-r37-build-results.json`, 392 lines added; see §5 D3).

Driver digest (copied from the mutable `.ufo/watchdog.log`, lines 1533/1537 at read time):

    2026-10-26T13:52:56-03:00 launch kasegi round=37 pgid=1603012 driver=hyaku-inline attempt=1
    2026-10-26T15:02:47-03:00 complete kasegi round=37; hyaku-inline attempt=1

Measurement method: `git -C <lane> archive <ref> | tar -x` into scratch trees for B and A, then plain
`grep`/`awk`/`wc`/`sha256sum`/`git ls-tree`/`git cat-file` and a Python substring check over the extracted
committed bytes. No lane gate or instrument (`r37-closure.sh`, `source-recheck.py`,
`frontier-recheck-count.py`, `recheck-audit.py`, `capture-binding-check.py`) was executed (PROTOCOL §Gate
standard, Closure consequence). The fleet census script was run as instructed.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-37/kasegi.md` | `kasegi-shokunin <kasegi@shokunin.local> 3aa4ed4da3ade9b4ace0d149c235efb5c74d7da7 2026-10-26T15:02:03-03:00` (before `complete` 15:02:47); prompt `041ed81d` 13:52:53 by the same identity | conformant |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` on the report; `- [` lines under it; `grep -cE '^- \[x\]' SHONEN.md` at A | `1`; `4` `[~]` lines for the four boxes; `0` `[x]` | conformant |
| Cited lane commits exist and are ancestors of `master` | `git rev-parse --verify <h>^{commit}` + `git merge-base --is-ancestor <h> master` for `b56a4168`, `2387dcf6`, `224df74d`, `f3246559`, `b3620681`, `0acffc82`, `a4b6a8ca`, `2735e93f`, `9492c776`, `aa88877b`, `c20300df`, `cc692008`, `a23dc478` | all 13 resolve; all ancestors (exit 0) | conformant |
| Lane pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain` | `state branch=master local=83975acc… remote=83975acc… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; `ls-remote origin refs/heads/master` = `83975acc…` | conformant |
| Prompt carries the template contract | read `.ufo/prompts/kasegi-round-37.md` (624 lines) | §1 MISSION/AXES binding, §2 1–3 claims, §2b frontier step, §3 L2 floor, §4 report contract incl. SHONEN, §5 commit/push/L0, §6 hyaku addendum, §7 scratch discipline | conformant |
| Report is not a marker | report names claims, commits, commands | real committed work (9 round commits B..A) | status `ok` |

Defects recorded (status-neutral): a lane commit (`83975acc`, WAVE-DONE results) landed 28 s after
`complete` — the r36 D3 closure-order class recurs (the report discloses the unfinalised results file);
three different heads are named as "the final lane head" (report `2387dcf6`, `SCORECARD.md`/`SHONEN.md`
`aa88877b`, receipt run `9492c776`); see §5.

## 2. Claims — re-derived at A

### C1 — depth:verifiability (held 4): VERIFIED (evidence-verified + plain re-derivation of the changed limbs)

Frozen predicate (`claims.json`, commit `224df74d`): `r37-closure.sh --export-ref <final head>` →
`closed=14/14 exit=0`; `--selftest` → `cases=14 failures=0`; r36 base `cc692008` and r36 judged head
`a23dc478` → `closed<14/14 exit=1`; D1, D2, D4, D5, D6 closed; `porcelain:-0` count 0; placeholders 0/0.

Suite bytes: `git cat-file blob A:corpus/instruments/r37-closure.sh | sha256sum` →
`0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d`, 1558 lines / 73132 B; absent at B.

Committed gate evidence (verified, not executed) — `.ufo/waves/round-37/final-gates/all-gates.txt` at A
(121 lines): header `all-gates v1`, `export-ref=9492c776…`, `suite-sha256=0da98e37…` (equals the blob at A),
`run-utc=2026-10-26T18:00:21Z` (after the `9492c776` commit at 17:59:49Z, before `aa88877b` at 18:00:25Z
that ships it — not future-dated); `grep -cE '^E[0-9]+ payload=.* closed=1$'` → `14`; `closed=14/14 exit=0`;
`grep -cE '^selftest case=E[0-9]+ positive=pass mutants=([0-9]+)/\1 verdict=pass'` → `14`;
`selftest cases=14 failures=0`; seven forged-receipt judges rejected. This closes the r36 D1 gap
(positive limb now committed). Required reds are evidence-verified in seat receipt
`wave1/MutC1Fixtures.md:23-24` run with the landed suite (`0da98e37`, line 9): `cc692008` →
`closed=4/14 exit=1`; `a23dc478` → `closed=7/14 exit=1` (E10–E14 open there). The reds are not in
`all-gates.txt` itself.

The receipt grades `9492c776`, not A. `git diff --stat 9492c776 A` touches only `all-gates.txt`,
`SCORECARD.md`, `SHONEN.md`, so E2–E9/E11/E13/E14 inputs are byte-identical; the three affected checks
were re-derived at A by plain reads:

| Check (defect) | Plain command at A | Observed | Closed? |
|---|---|---|---|
| E1 (placeholders/binding) | `grep -cF 'filled by the L1' SCORECARD.md`; `grep -cF '<LANE_HASH>' SCORECARD.md`; `grep -cE '<r37-[a-z-]+>\|<fill>'` over SCORECARD/SHONEN/lesson/LOG; round-37 `Final lane commit:` hash ancestry | `0`; `0`; `0` each; `f3246559…` exists and is an ancestor | yes |
| E10 (D1) | receipt header/digest/ancestry/line counts above | `export-ref` ancestor of A; digest equal; 14/14 lines; 14 cases | yes |
| E11 (D2) | `grep -n 'Correction (round 37)' LOG.md`; `git ls-tree -r --name-only A \| grep -c r36-fixtures` | `LOG.md:1686` names `corpus/instruments/r36-fixtures/` and states it was never committed; `0` | yes |
| E12 (D4) | `awk '/^## Round 37/{f=1} f' SCORECARD.md \| grep -cF 'Final lane commit: e666d902'`; anchor line | `0`; `Anchor ancestor (r36 lane head): c20300df…` present | yes |
| E13 (D5) | `grep -nE '^\| *r3[67]-closure\.sh' SKILL.md` | `:1113` appended `r36-closure.sh` row, type `gate`, map `0 closed \| 1 open \| 2 could-not-evaluate`; `:1112` `r37-closure.sh` row type `gate` with exit-2 class (registry home = `SKILL.md`); original `:1111` row with `gate\|probe` retained (append-only) | yes |
| E14 (D6) | `grep -cF 'porcelain:-0' corpus/instruments/r37-closure.sh`; status-read sites | `0`; status read at `:581` is `if out=$(git … status --porcelain); then` (rc-checked, no `2>/dev/null`) | yes |

Reported vs re-derived: `closed=14/14`, `cases=14 failures=0`, reds `4/14`/`7/14`, suite digest `0da98e37…`
— consistent. Not verified by this judge: a committed transcript of a run over A (or `aa88877b`); those
positive runs are assertions in the report/SCORECARD (routed §5 D-B). The claim verifies because the
committed receipt covers `9492c776` and every limb whose input changed after it re-derives closed at A.

Overreach in the report: "all six routed defects closed" — D3 (closure order) has no E-check and
recurred this round (`83975acc` after `complete`); the frozen predicate names D1, D2, D4, D5, D6 only, so
the claim is unaffected, but the sentence is not true for D3.

### C2 — coverage (held 7): VERIFIED (re-measured)

| Counter | Reported B→A | Re-measured B→A |
|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 19→20 | 19→20 |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 53→54 | 53→54 |
| `grep -cE '^\|[[:space:]]*S054[[:space:]]*\|' corpus/SOURCES.md` | 0→1 | 0→1 |
| `grep -rlE '^source: S054 ' corpus/knowledge \| wc -l` | 0→1 | 0→1 |
| `ls corpus/knowledge/*.md \| wc -l` | 48→49 | 48→49 |
| S054 row shape (`awk -F'\|' … NF`) | NF=13 | `NF=13`; kind `docs`, tier `A`, status `mined`, opened `2026-10-26`, recheck `90d`, used-by the SSVC entry (exists); one `https://` token = manifest `url` |
| capture `sha256sum`/`wc -lc` | `ff3f3b2c…`, 518 lines, 32,623 B | `ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21`, 518, 32623 |
| manifest `sha256sum`/`wc -c` | `fabc3163…`, 3989 B | `fabc3163dbd31d33bff6e0bccf8b86b94e081b06b3ab1f00538dd9c0a57df642`, 3989 |
| Q1–Q4 at manifest anchors (substring in `S054.txt` line N; total count) | 259/277/473/68, `occurrences=1` | each present on its anchor line, total 1 each; words 12/14/17/5 |
| entry's located quotes (`"…" (L<n>[-L<m>])` pairs) vs capture lines | — | 29 pairs, 0 missing at the cited line(s) |
| uncovered-ground sweep at B: `grep -rliE 'SSVC\|stakeholder-specific' corpus/knowledge corpus/README.md corpus/SOURCES.md SKILL.md PROVINCE.md \| wc -l` | — | B `0`, A `4` |
| census `scripts/sources-census.sh validate --root … kasegi` | exit 0, W04 S028/S029 | exit 0, W04 S028/S029 only |

Harness `entries=23 pass=23`, `source-recheck` exit 0, `capture-binding` `records=44 bound=44`, and
`recheck-audit` `expected=49 unexpected=0` are lane-instrument outputs, evidence-verified from the report and
SCORECARD assertions only (the lesson records the harness as a live-lane measurement); the plain re-derivations
above cover the same predicates' byte content.

### Owned-axis harm check

`git diff --numstat B A -- . ':!.ufo'`: every file `N/0` (zero deletions): `SKILL.md 2/0`, `SCORECARD.md
15/0`, `PROVINCE.md 74/0`, `corpus/README.md 56/0`, `corpus/SOURCES.md 1/0`, `corpus/QUALITY.md 14/0`,
`LOG.md 17/0`, `SHONEN.md 9/0`, plus new files. `SCORECARD.md` diff adds only the `## Round 37 result`
section; axis rows depth:verifiability 4→4, coverage 7→7, depth:density 9→9; no capability row. `SKILL.md`
gains two registry rows after `:1111`; density-bearing base lines byte-identical → depth:density unchanged.

Not an axis harm, but a material record defect (§5 D-A): the `PROVINCE.md` append is 74 lines where the
amendment is 2 — lines 80–152 are the scribe receipt's scaffolding (`## 3. Deliverable B — corpus/README.md
end-of-file block`, a duplicated F20 frontier row, `## 4. Validation on a scratch mirror`, a property table
saying "result 80 lines"; actual `wc -l` 152) with three unbalanced code fences; the `corpus/README.md`
append is 56 lines where the planned block is 27 — it lost its `## Round-37 admission` heading
(`grep -c` → 0) and carries the same "Validation on a scratch mirror" section twice-pasted plus a stray
fence. Frontier counts are unaffected (README F-rows exactly 20), so coverage is not harmed by
measurement, but the SHONEN box-4 assertion "PROVINCE.md still accurate" is not true as written.

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability | improved | suite absent at B → D1/D2/D4/D5/D6 re-derived closed at A; positive receipt committed with digest binding; reds evidence-verified with the landed suite; score held 4 |
| coverage | improved | frontier 19→20, registry 53→54 (tier A, mined), knowledge 48→49 on SSVC ground absent at B; score held 7 |
| depth:density | unchanged | `SKILL.md` append-only (2 registry rows); no claim |

## 3. Discernment spot-check (`corpus/lessons/round-37.md` `## Gate`, at A)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| F20 / S054 CERT/CC SSVC overview tutorial | admit | `curl -sS -L https://certcc.github.io/SSVC/tutorials/ssvc_overview/` (2026-10-26) → `status=200 bytes=143053 redirects=0`, raw sha256 `9dba9f7500a6a1cece1a7acc77f1d768454b75fd04fa5bfdf382dfe598faec3f` | agree | live body is byte-identical to the manifest's `raw_sha256` and served size; tag-stripped text holds Q1, Q2, Q3 and Q4 once each; tier A is right for CERT/CC describing its own method; the entry's 29 located quotes all sit at their cited capture lines, and the entry scopes CVSS/KEV/EPSS definitions away from S054 |
| `c2-controls/junk-f20.md` (four fabricated SSVC claims) | reject | same live page + committed `S054.txt` | agree | each fabricated sentence occurs 0 times in both; the live page has 0 `FIRST`, 0 `deadline`, 0 `replaces` — the twin's "maintained by FIRST", fixed-deadline and "replaces CVSS" claims have no ground |
| Standing refusals `program-severity-ladders-and-reward-scales.md` and `chinese-program-severity-instrument.md` (staged package) | reject (flip unmet) | `sha256sum` lane vs `shokuknow/merge/kasegi/knowledge/corpus/knowledge/…`; `grep -c newsType_6 corpus/source-snapshots/round-32/S049.txt`; `grep -c sse.com.cn corpus/SOURCES.md` | agree | `6c05c98f…` vs `35de5f8b…` (still unequal); `newsType_6` → 0 (`newsType_21` → 1); S047's `sse.com.cn` source has 0 lane rows; `SOURCES.append.md` still `4fe049cb…` — reasons and unmet flips reproduce |

New `SOURCES.md` row re-opened: S054 (above). Its `## Gate` quotes are ≤25 words (12/14/17/5 by `wc -w`
semantics), located (`S054.txt` L259/L277/L473/L68), and present live. Q4 is honestly labeled
navigation-only.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` →
`W04 S028`, `W04 S029` (standing duplicate-URL warnings), `ok`, exit 0.

## 4. Trend verdicts

- **expansion: improved** — one admitted entry (`ssvc-stakeholder-specific-vulnerability-categorization.md`)
  on ground B did not hold (sweep 0 at B), citing mined tier-A `S054`; F19→F20.
- **quality: improved** — the round-36 verifier's routed D1, D2, D4, D5, D6 close by committed receipt plus
  plain re-derivation; S054 re-opens live byte-identical; no admitted entry failed a re-check here.
  Offsetting defects (D-A scaffolding paste, D-C pending markers) are record defects in index/lesson files,
  not a false or stale knowledge entry left unmarked, and are routed.
- **discernment: improved** — the non-author spot-check agrees with the gate on the admit and on both
  rejects sampled; QUALITY R30 (grounded M37-2) and R31 (grounded considerthese proposal 7) each carry a
  lesson.

## 5. Routed defects (kasegi owes these next round)

- **D-A — receipt scaffolding pasted into front-door files.** `PROVINCE.md:80-152` and the
  `corpus/README.md` round-37 append carry `wave1/ScribeFrontierAmendments.md` sections (§3 header,
  property tables, §4 "Validation on a scratch mirror", duplicated F20 row in PROVINCE, unbalanced
  fences); README lost its `## Round-37 admission` heading. Append a named correction marking those
  lines as misplaced (append-only) and add a check that an amendment append equals its declared block
  bytes/sha (`cdfe44e3…` 2 lines; `2ebd8cd2…` 27 lines).
- **D-B — final-head positive run not committed.** `all-gates.txt` grades `9492c776`; the `closed=14/14`
  runs over `aa88877b` (SCORECARD, SHONEN) and `2387dcf6` (report) have no committed transcript, and the
  three artifacts name three different "final" heads. Name one judged head and commit its run, or state
  that the receipt grades an ancestor and list the post-receipt diff.
- **D-C — unresolved `⟨pending…⟩` markers in the round lesson.** `grep -c '⟨pending'
  corpus/lessons/round-37.md` → `7` (lines 10, 90, 95, 216, 265, 300, 320), including the census
  after-state and No-harm measurement; line 85 still says the entry "is not landed". The E1 placeholder
  limb missed these and also passed `9492c776`, whose `SCORECARD.md` held `<r37-final-head>` (1) and
  `SHONEN.md` `<r37-final-lane-hash>`/`<fill>` (2): widen the placeholder vocabulary to every lane file
  the round writes.
- **D3 (recurrence) — closure order.** Lane commit `83975acc` (15:03:15) landed after `complete kasegi
  round=37` (15:02:47); the report's "all six routed defects closed" is not true for D3, which no E-check
  covers.
- **D-D — label drift recurrence (D4 class, minor).** The round-37 SCORECARD section's
  `Final lane commit: f3246559…` names a wave-evidence ancestor under the "final" label (qualified in
  parentheses); use the anchor-ancestor label.
- **D-E — scratch not empty.** `/fast/scratch/hyaku/kasegi-r37/build-spec.py` remains (no seat dirs, so
  E9 is unaffected); the report says "scratch empty" (§7 delete-on-exit).

Promotion note for the operator: SHONEN box 2 (end-to-end domain task) remains `[~]` with "none new",
and box 4's "PROVINCE.md still accurate" is contradicted by D-A, so the checklist is not fully checkable
by a non-author this round.
