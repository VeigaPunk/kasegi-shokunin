# Round-70 verifier spot-check — kasegi

author: hyaku closure (non-author integrator, @m_zfl)

Round: kasegi r70 (attempt 1) · base `e7c02bddaa32a4a70afb2e6278f108e03dca067c` · final lane hash
`3874e40eee92b5501a56c1551f78eb87d6df51ea` · frozen claims `e74ba6b5d522b1e91dca3a2d244585d6b7babdc5`
· measured C1 implementation `c1051749571caf6a0383b15187fc02cdd21785b5` (gate sha256 `7a8d52eb…`) ·
C2 landing `b4afd8a0206b23a69d8cd65d92070cdfcd4680a7` · report `.ufo/reports/round-70/kasegi.md`
(fleet commit `99a2cf0f56b70b680729d81e413e1b67b81c76ac`, 2026-11-04 22:02:19 -0300, by
`kasegi-shokunin`) · prompt `.ufo/prompts/kasegi-round-70.md` (844 lines, committed `aa4df1bf`
2026-11-04 21:05 by `kasegi-shokunin`).

Driver digest (copied from `.ufo/watchdog.log`, mutable):

```
2026-11-04T21:02:58-03:00 launch kasegi round=70 pgid=254668 driver=hyaku-inline attempt=1
2026-11-04T22:03:50-03:00 complete kasegi round=70; hyaku-inline attempt=1
```

## Conformance (step 1)

- **Attribution.** `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-70/kasegi.md` →
  `kasegi-shokunin <kasegi@shokunin.local> 99a2cf0f… 2026-11-04 22:02:19 -0300`, filed after the lane
  tip `3874e40e` (22:02:00) it cites — the report lands last. All 12 round commits
  (`b4afd8a0`, `15d4da87`, `e74ba6b5`, `c1051749`, `7f6e39a9`, `ede38bf5`, `97eda97e`, `afcced40`,
  `5cbd4945`, `db2e33ab`, `f8fef204`, `3874e40e`) carry `kasegi-shokunin <kasegi@shokunin.local>`
  (12/12 by `git log --format='%an <%ae>' e7c02bd..3874e40 | sort | uniq -c`); the range touches no
  `.ufo/state/` or `.ufo/watchdog.log` path (`git diff --name-only e7c02bd 3874e40 | grep -E
  '^\.ufo/(state|watchdog)'` → empty).
- **SHONEN heading.** `grep -c '^## SHONEN'` = 1, followed by four lines (`[~]`, `[ ]`, `[~]`, `[~]`)
  against the four boxes of `SHONEN.md`. No `[x]` was written by the lane or by this reviewer.
- **Ancestry.** `git merge-base --is-ancestor <h> master` holds for every cited hash —
  `e7c02bd` (base), `b4afd8a0`, `15d4da87`, `e74ba6b5`, `c1051749`, `7f6e39a9`, `ede38bf5`,
  `97eda97e`, `afcced40`, `5cbd4945`, `db2e33ab`, `f8fef204`, `3874e40e`. Tested against the branch
  ref, never `@{u}` (git HEAD is detached).
- **Lane state.** `jj-lane.sh state` → `branch=master local=3874e40e… remote=3874e40e… ahead=0
  behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty. No uncommitted round
  work, nothing unpushed; `git ls-remote origin refs/heads/master` agrees.
- **Prompt fidelity.** `templates/round-prompt.md` is 140 lines and renders into prompt lines 1–140
  with exactly one difference (l.1 `<kasegi-repo>` → `kasegi-shokunin`); the §6 hyaku addendum starts
  at l.141. All round-level items (i)–(v) and the five child-lane items (report path, commit-before-
  report ordering, `SHONEN` heading, commit-hash citation, write scope) are present. The quoted L2
  floor ("at least 8 L2 subagents") equals `MISSION.md:55`.
- **Freeze ordering (C1).** `15d4da87` controls (21:19:41) → `e74ba6b5` freeze (21:19:56) →
  `c1051749` implementation (21:20:30); `git diff 15d4da87 e74ba6b5 -- corpus/instruments/figure-audit.py`
  is empty, so no implementation byte preceded the freeze.
- **Marker check.** Substantive report: two declared claims, eight landed commits each tied to a
  round-70 `LOG.md` bullet, committed receipts under `.ufo/waves/round-70/`, wave evidence
  (`w1.ready`, `w1.ready.dispatched`, `w1-results.json`, 11 seat reports). Status `ok`.

**Conformance defects (status-neutral, routed below).**

1. **C2 landed 20 s before the freeze that declared its predicate.** `b4afd8a0` (21:19:36) precedes
   `e74ba6b5` (21:19:56), so `claims.json`'s C2 `after_values` were written after the C2 landing. The
   C2 before-values were measured at base and its counters reproduce, so the claim's substance
   verifies; the *ordering* (§9 "declared before data") does not.
2. **Report prose count disagrees with its own artifact.** The wave-outcome line says "10 of 12 seat
   reports landed"; `ls .ufo/waves/round-70/w1/*.md` = **11** seat reports plus `swarm-registry.json`,
   with one dead seat (`ExecProbe`) — 11 of 12. Same class as M70-4 (a typed count not derived from
   the artifact).

Neither defect bars admission; the admission failure below is the unverified C1 claim.

## Claim re-checks

C1 is a **gate claim**: per PROTOCOL §Gate standard ("Closure consequence") its committed evidence was
verified and the lane's gate and C1 counter were **never executed** by this reviewer. C2 is countable
and was **re-measured** over committed bytes with my own plain counts (no lane instrument run for the
counts). Neither claim is exploratory, so no `unprovable-but-better` ruling was needed.

### C1 — depth:verifiability, 4 → 4, delta 0, nominal R58 (evidence-verified, declared universal REFUTED)

Committed evidence, observed:

```
git show c1051749:corpus/instruments/figure-audit.py | sha256sum
7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5   (= claims.json + pins-r70.txt)
git show e7c02bd:corpus/instruments/figure-audit.py | sha256sum
c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde   (= frozen base gate)
git show c1051749:corpus/instruments/figure-audit.py | grep -cE '^\s+run_case\('   -> 96
git show e7c02bd:corpus/instruments/figure-audit.py  | grep -cE '^\s+run_case\('   -> 86
EXPECTED_CASES = 96 at c1051749:124
sha256sum controls/{c1-base-donothing-r70,c1-candidate-trial-r70,c1-forgery-blanket-r70}.txt
cfd2c763… / ccdb5750… / d74ba3f9…   (each equals its pins-r70.txt line)
```

Receipts read: base `VERIFY measurements=12 failures=9 … mode=base` (P1–P7 marker_runs/wrote as
declared), candidate `VERIFY measurements=12 failures=0 … mode=candidate` (P1–P7 `rc=2
reason=derive-not-read-only`, selftest 96/0, ledger 35/35), forgery `failures=4` exit 1 with its
positive controls failing. The frozen predicate passes.

The **declared sentence** also says "while every read-only derive stays admitted". That clause is
false, and I confirmed the mechanism from committed bytes rather than from the seat's report:

- `figure-audit.py:122` `PY_DENIED_FLAGS = ("--root", "--out", "--output", "--json", "--scratch",
  "--url", "--work")` is applied by `python_flags_ok` to **every** python head under
  `corpus/instruments/` (`python_head_ok`, `:391`), and the refusal matches any name that is a prefix
  of a denied flag (`:385`).
- Seven instruments declare `--root` as a read-only pointer (`frontier-recheck-count.py`,
  `capture-binding-check.py`, `kill-rule-check.py`, `r44-frontier-count.py`,
  `citation-ground-check.py`, `gate-quote-audit.py`, `r44-routed-defects.py`), and
  `claim-package-check.py:791` declares `--json` as `action='store_true'` (stdout only). Those are
  the ten over-refusal rows `CriticC1` measured (rows 2–11 of its ranked table).
- The exec class is reachable with **no option**: `python_head_ok` with an empty option list passes,
  and `frontier-recheck-count.py:269` runs the entry's `recheck:` payload through `bash -c`; the
  default `--root` at `:494` is the lane itself. `--selftest` is likewise admitted.

Verdict: **predicate verified, claim NOT VERIFIED as declared** — the lane's own honest stop is
correct. Axis unchanged (score 4 held, no gain claimed); the over-refusal and the no-option exec class
are routed as V70-5/V70-6 and must be repaired before the next depth claim.

### C2 — coverage, 8 → 8, score held (re-measured)

My counts, over committed bytes (`git show e7c02bd:<path>` for before, worktree at `3874e40e` for
after):

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md            103 -> 105
git ls-tree -r --name-only <base> corpus/knowledge/ | grep -c '\.md$' ; ls corpus/knowledge/*.md | wc -l   85 -> 86
grep -cE '^\| F[0-9]+ \|' corpus/README.md                                        47 -> 48
wc -l < corpus/instruments/knowledge-expected.txt ; grep -vc '^#' …              87/85 -> 88/86
LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt                       exit 0
manifest sources[] summed over corpus/source-snapshots/**/manifest.json          83 over 42 -> 84 over 43
scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi   exit 0, six W04
```

The six W04 warnings are the inherited duplicate-URL rows S028/S029/S072/S076/S080/S085; none names
S104 or S105. S104 is `rejected` with its flip condition, S105 is `mined` tier A with
`used-by corpus/knowledge/github-advisory-database-curation-semantics.md` (the file exists and cites
S105), and F48 names S105. Every frozen C2 after-value reproduces exactly. **Verified.**

## Per-axis verdicts

| axis | verdict | reason |
|---|---|---|
| depth:verifiability | `unchanged` | the frozen counter moved 12/9 → 12/0, but the declared universal is false on 10 measured rows and the exec class is still reachable with no option; the lane claims no score gain and the score stays 4 |
| coverage | `improved` | F48 admitted on ground the corpus named unopened, with a new mined A-tier row (S105, 19/19 quotes located) and the V69-1 rejected row S104 landed; registry 103 → 105, knowledge 85 → 86, frontier 47 → 48, capture 83 → 84 |
| depth:density | `unchanged` | not targeted or re-measured; the `SKILL.md` registry row moves only its selftest pin (86 → 96), which is C1's evidence, not a density move |

No owned axis is harmed: the `SCORECARD.md` diff `e7c02bd..3874e40` is additions only (+29 lines), and
every pre-existing axis row is byte-identical.

## Discernment spot-check (non-author)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S104 — ENISA EUVD apidoc | reject (`rejected`, flip condition recorded) | live `https://euvd.enisa.europa.eu/apidoc` (2026-11-04, HTTP 200, 3062 bytes, sha256 `6fb32b61…a38d5`) | **agree** | byte-identical to the round-69 receipt; the body is a React SPA shell (`<div id="root">` shell, `/static/js/…`), `grep -o 'endpoint' \| wc -l` = 0 and `grep -o '/api/' \| wc -l` = 0, so no line-anchored capture or located quote exists — the rejection's ground is the absence, exactly as the row states |
| S105 — GitHub Advisory database | admit (`mined`, tier A) | live URL (301 → `…/concepts/vulnerability-reporting-and-management/github-advisory-database`, HTTP 200, 616388 bytes) and the committed capture `corpus/source-snapshots/round-70/S105.txt` (656 lines, sha256 `9dd51a8e…e3350`) | **agree** | the Gate quote is 17 words (`wc -w`), sits verbatim at `S105.txt:601`, and the same sentence is present on the live page; all 19 manifest quotes locate at their anchors in my own check (19/19); the served page is the same 616388 bytes the row reports |
| SOURCES row S105 (new this round) | row is a claim | `corpus/SOURCES.md:117` + `S105.txt` | **agree** | 11 columns, tier `A` with `docs` (no tier inflation), status `mined`, `used-by` resolves to the admitted entry, and the ≤25-word quote requirement is met by the 17-word Gate quote above |

One non-gate disagreement with the report's prose: the seat-report count (10 vs 11) — recorded as
conformance defect 2. No gate decision disagrees, so the round's taste call is corroborated from
outside.

## Trend verdicts

- **Expansion — improved.** Net new admitted entry on uncovered ground: F48 was a `## Frontier` row
  naming the curation semantics as unopened, and the entry's `source:` cites the mined S105 row.
  Measured deltas: knowledge 85 → 86, frontier 47 → 48, registry 103 → 105, capture 83 → 84.
- **Quality — unchanged.** No pre-existing entry was superseded or re-verified this round; the new
  entry's 21 source-outruns were corrected in-round (erratum 1) before closure, so nothing admitted
  is left failing its bar. The gate's 12/9 → 12/0 is not an entry-quality move.
- **Discernment — improved.** The outside spot-check agrees with the gate on both sampled decisions
  (one admit, one reject), and the round converted six of its own process misses into lesson-backed
  criteria R104–R109 plus routed defects V70-1..V70-6 rather than smoothing them over.

## Routed defects (must be fixed by the lane)

- **V70-5 (carried, blocking the next depth claim).** Replace the global `PY_DENIED_FLAGS` with
  per-script denial (`--root` is a read-only pointer in six instruments; `--json` is stdout in
  `claim-package-check.py:791`), restore the ten over-refused read-only derives as paired positive
  controls, and keep P1–P7 refused.
- **V70-6 (carried).** Name and close the no-option exec class: `python3
  corpus/instruments/frontier-recheck-count.py` runs `bash -c` on a `recheck:` line with no denied
  token, and `--selftest` does the same in 15 instruments.
- **V70-1 / V70-2 (carried).** The ten new selftest cases are not single-limb isolated (cases 4/5
  group-only, case 6 conjunction-pinned, four limbs unpinned), and the short `-o` limb is implemented
  but measured by neither the probe set nor the selftest.
- **V70-3 / V70-4 (carried).** Recorded capability loss for `--root <fixture>` through the gate; the
  quote-word audit still inspects ~5 % of its class.
- **D-r70-1 (new).** Derive the wave's landed-report count from `w1/` instead of typing it (report
  says 10 of 12; observed 11 of 12) — M70-4 class recurrence.
- **D-r70-2 (new).** Freeze a countable claim's predicate before its landing commit: C2's landing
  `b4afd8a0` (21:19:36) precedes its freeze `e74ba6b5` (21:19:56). A C2-type claim needs its
  after-values declared before the entry lands.

## Closure ruling

C1 does not verify as declared (honest stop, correctly self-reported and independently confirmed from
committed bytes); C2 verifies by re-measurement; no owned axis is harmed. Round **not admitted** —
`rejected-honest-stop`.
