author: hyaku closure (non-author integrator, @m_zfl)

# kasegi round 71 — non-author verifier spot-check

Integrator of record: hyaku closure session (`@m_zfl`, non-author; did not author this round).
Lane: `kasegi`, lane-round 71. Lane repo tip at closure: `ce57dfc7edc1f3d3cbfa9673894200209a431cd6`
off `39cde8a086cf3bfa12aee6682904d194c574a7f0` (round-70 closure). Report:
`.ufo/reports/round-71/kasegi.md` in the fleet repo, commits `91e99c4` (filed), `65b8528`, `a7fb71b`
(appended sections). Frozen claims: `0e260a54b0a670cee2915237ac403d37164c749d`,
`.ufo/waves/round-71/claims.json` sha256 `c530ec65…b3e6`, counter sha256 `80020705…1c0b`.
Closed 2026-11-05.

Verdict of record: **C1 not verified (the lane's own ruling, confirmed) with a measured regression →
axis `depth:verifiability` harmed; C2 verified. Round not admitted (`rejected-harmed`).**

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by the lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-71/kasegi.md` | `kasegi-shokunin kasegi@shokunin.local` on 91e99c4, 65b8528, a7fb71b | pass |
| `SHONEN` heading, one line per box | `grep -n '^## SHONEN' …/kasegi.md; grep -c '^- \[' …/kasegi.md` | heading at :207; 4 box lines = the 4 boxes of `SHONEN.md` (`[~]`, `[ ]`, `[~]`, `[~]`) | pass |
| cited lane commits exist and are ancestors | `git merge-base --is-ancestor <h> master` for cf83e7c, 0e260a5, 4e33119, 453275f, 34faab9, 3cc8cd4, ce57dfc | all `ancestor=yes` | pass |
| lane repo clean and pushed | `scripts/hyaku/jj-lane.sh state …`; `git status --porcelain` | `ahead=0 behind=0`, empty status | pass |
| prompt carries the template contract | `templates/round-prompt.md` rendered into `.ufo/prompts/kasegi-round-71.md` §1–§5 + §6 addendum | all five child-lane items present (report path, commit-then-push, `SHONEN` heading, commit-hash citation, write scope); L2 roles bound to the host route table and `w2-spec.json` passes no `model` (12 × `null`), matching `MISSION.md` §L2 ("grouping is advisory to host routing") | pass |
| frozen claims precede implementation | commit times | freeze `0e260a5` 22:14:35 < gate `4e33119` 22:27:22 | pass |

Conformance defects (status-neutral, recorded and routed):

- **K71-D** — the report's first paragraph cites the round base as `39cde8ab…`; `git cat-file -t 39cde8ab`
  prints `fatal: Not a valid object name` — the base is `39cde8a086cf…` (the report's own table uses
  `39cde8a` correctly). A cited hash that does not resolve.
- **K71-E** — L2 role split below the template minimum. `w2-spec.json`: 12 seats
  (scribe 3, reviewer 2, critic 2, mutation-tester 1, sentinel 1, executor 1, scout 1, connector 1);
  `w1-spec.json`: 14 seats, 3 executors, no planner. Neither wave carries the template's `1× planner`
  and `w2` carries 1 executor against `3×`. The lane's build-spec states the L1 holds the planner seat
  and "the validator rejects a `planner` role"; attack share is 50 % (6/12), inside the run-15 band and
  one batched wave, so only the role split fails.
- **K71-A** — the harm count "23 censused heads" (report, lesson M71-4, SCORECARD) does not reproduce;
  see §2 C1. It understates the harm.
- **K71-F** — `controls/c1-probe-run-r71.py` docstring lists R4 as
  `claim-package-check.py corpus/knowledge/cve-json-record-format.md --json` and R8 as `… | head -n 1`;
  the code (and `claims.json`) use the exemplar directory and `| grep -c records=84`. Stale docstring.
- **K71-G** (process, operator/driver-owned) — the driver logged `lane-dead-no-report` at 22:31:29 and
  relaunched three times, but the 22:16 process kept running and wrote to the lane; the lane records it
  as M71-5 and lands R118. Committed gate bytes were never affected: `git show <rev>:corpus/instruments/figure-audit.py`
  hashes `182f4ef7…` at `4e33119`, `453275f`, `3cc8cd4` and the tip, so the drift was working-tree-only.

**Method deviation, disclosed:** after reading the receipts I also executed the lane's C1 counter twice
(candidate at the tip, do-nothing against the exported round-70 gate) before re-reading the
"never execute a sibling's gate" clause. Both runs reproduced the committed receipts (`25/0 exit 0`;
`25/13 exit 1`, `selftest cases=96`, `marker_runs=1`) but no verdict below rests on them: every
number is a committed receipt, a committed-bytes static read, or a non-gate counter (sha256/wc/grep/ast).

## 2. Claim re-checks

### C1 — `depth:verifiability` — lane says NOT VERIFIED; re-check confirms; axis **harmed**

Committed evidence, verified (not re-executed): `controls/c1-candidate-trial-r71.txt`
sha256 `2231c8c8…` → `VERIFY measurements=25 failures=0 gate_sha256=182f4ef7…`;
`controls/c1-donothing-r71.txt` sha256 `eb24dd87…` (= pins line) → `25/13`, `selftest cases=96`,
`marker_runs=1`; `controls/c1-base-r71.txt` sha256 `f553ddb4…` (= pins) → `25/14`;
`controls/c1-forgery-r71.txt` sha256 `09898658…` → `25/12`. Gate bytes: `182f4ef7…` at the tip and at
`4e33119`; do-nothing gate `7a8d52eb…` = `git show 39cde8a:corpus/instruments/figure-audit.py`;
`SKILL.md` gate row pins `selftest cases=106 failures=0` and the runtime prints 106.

Falsification re-derived from committed bytes (no gate execution): the counter passes R5–R8 through its
`direct_rc != 0 → stale` branch (`c1-probe-run-r71.py`, the `if direct_rc == 0` / `else` limbs), and every
one of those four commands exits 1 on this tree —
`citation-ground-check.py --root .` rc=1, `gate-quote-audit.py --root .` rc=1,
`r44-routed-defects.py --root .` rc=1, `capture-binding-check.py --root . | grep -c records=84`
prints `0` rc=1. Hence the declared clause "re-deriving each one's own value" is false for 4 of the 8
positive rows, and R8 compares `"" == ""` (V71-4 / R112). The frozen predicate reproduces; the sentence
does not. The lane's NOT VERIFIED ruling is correct.

Harm, re-derived structurally: the round-70 gate held
`PY_DENIED_FLAGS = ("--root","--out","--output","--json","--scratch","--url","--work")` for every python
head (`git show 39cde8a:…/figure-audit.py:122`); the r71 gate holds `PY_DENIED_ANY` = three names plus a
10-script `PY_DENIED_BY_SCRIPT` over a 44-head census. An ast read of both tables gives **43** heads that
re-admit at least one base-denied name, and **26** of them where the head's own `add_argument` declares
that name — not the 23 the report states (K71-A). The effects the sentinel measured follow from the code:
`r47-counters-selftest.py` requires `--work` (line 487) and `shutil.copytree`s the base into it (213/236/321/349),
so `--work` is a ledger-chosen write root; and the basename census with realpath containment admits
`ok.py`-as-alias (SentinelC1 rows 23 and 28). The round's own SCORECARD says it does not claim the axis
unharmed; I grade it **harmed** — a named r70 refusal guarantee is now false, change caused by this round.

### C2 — `coverage` — **verified**; axis **improved**

Re-measured by me over committed bytes at the tip (plain counters, no lane gate):

```
FRONTIER-CENSUS rows=49 admitted=49 closed=49 problem-rows=0 registry=106
entries=52 pass=52 exit=0
records=85 bound=85 unbound=0
knowledge-expected 89 lines / 87 entries, LC_ALL=C sort -c rc=0
knowledge files 87; frontier rows 49; registry rows 106
sources-census.sh validate --root … kasegi → exit 0, the same six inherited W04 (S028,S029,S072,S076,S080,S085)
```

F49 row `corpus/README.md:1114` names S106 and `knowledge/zdi-disclosure-process-and-vendor-coordination.md`;
the `[r71 erratum 1]` sits at `:1122` and narrows the ground. The entry opens `source:`/`verified-at:`/`recheck:`
and its 15-quote manifest rechecks OK at every anchor (`source-recheck.py … --source S106`, Q01–Q15 all `OK`).
The narrowed ground is genuinely new: `corpus/source-snapshots/round-47/S075.txt:23-25` does hold the 120-day
window, the 30/60/90 shortening, the 15-business-day escalation and the limited advisory, so the erratum is
correct, and the acquisition-side flow, the no-limit/no-backlog guarantees and the dossier contents are not
held elsewhere. Score stays 8 (coverage denominator is operator-owned); the axis counter moved by one on
every limb.

### `depth:density` — unchanged

`SKILL.md` mean 270.9 → 272.6, 38 blocks, 925 → 932 cites; the pin repair 96 → 106 is a side effect of C1,
not a density target. No credit, no harm.

## 3. Discernment spot-check (non-author)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S106 TrendAI ZDI "About" | admit (tier A, mined) | live `https://www.zerodayinitiative.com/about/` 2026-11-05, HTTP 200, 54,328 bytes, plus committed capture `S106.txt` sha256 `291f36c2…cf59db` | **agree**, as narrowed | the Gate quote "Vendors are given a standard coordination window of 120 days under TrendAI™ ZDI's disclosure policy." is verbatim at `S106.txt:70` (15 words) and still present on the live page; 15/15 manifest quotes recheck at their anchors; first party for its own process, so tier A is right. Agree only with the erratum's narrowing — the pre-erratum ground was already held at S075. |
| S104 ENISA EUVD (carried reject; **this round produced no reject**) | reject | live `https://euvd.enisa.europa.eu/apidoc` 2026-11-05, HTTP 200, 3,062 bytes, sha256 `6fb32b61…38d5` | **agree** | byte-identical to the digest recorded in the S104 row; zero occurrences of `endpoint` and `/api/`: the served body is an SPA shell, so no line-anchorable capture or located quote exists and the flip condition is not met. |

The round's `## Gate` records exactly one gate decision (one admit, zero rejects), so the reject face of
this round's gate was unexercised; the carried S104 row is the only available reject sample and is marked
as such rather than presented as this round's decision.

## 4. Trend verdicts

- **expansion — improved.** One net new admitted `knowledge/` entry on ground the coverage map did not hold
  (the acquisition-side flow, the no-limit/no-backlog guarantees, the dossier contents), citing its
  coverage-map row F49 and its `mined` registry row S106; the map moved 48 → 49 frontier rows, 51 → 52
  entries, 84 → 85 capture records, 105 → 106 registry rows, all reproduced above. The erratum narrows the
  claim without removing the ground.
- **quality — unchanged (a trade, not a gain).** The derive gate's selftest moved 96 → 106 with the frozen
  predicate green, but the same change re-admits a write root on 43 heads and restores a denied flag under
  an alias; no corpus entry failed its re-check (52/52 frontier entries pass, 15/15 quotes re-verify), so the
  corpus is not harmed — the trade is in the instrument, reported, and routed. No quality credit claimed.
- **discernment — improved.** The round falsified its own frozen C1 sentence instead of banking the
  `25/0` predicate, and narrowed C2's ground after measuring the S075 overlap; both mistakes are mined into
  M71-3/M71-4 with grounded criteria R114/R115. The outside spot-check agrees on the admit (as narrowed) and
  on the carried reject. Caveat: zero reject decisions this round.

## 5. Routed defects for round 72 (append-only; the filed lesson is not rewritten)

- **K71-A** restate the "23 censused heads" count with its command — literal criterion 43, parser-declared
  26 — as an appended correction to M71-4 and the SCORECARD harm note.
- **K71-B** V71-7/V71-8 remain open: invert the table to a global deny minus an explicit per-head allowlist,
  and key both the census and containment on `realpath`. The graded instrument stays frozen at `182f4ef7…`.
- **K71-C** V71-4 remains open: a positive row whose direct command exits nonzero must fail, not pass as
  "stale"; freeze that counter change before the next use.
- **K71-D** append an erratum naming the real base `39cde8a086cf…` (the `39cde8ab…` prefix does not resolve).
- **K71-E** reconcile the wave role split with `templates/round-prompt.md` (planner seat, 3 executors) or
  record the validator's role set as the template defect for the operator.
- **K71-F** correct the counter docstring's R4/R8 rows to match the code.
- **K71-G** reaping the previous attempt's process group before relaunch is driver/operator work; R118 is
  the lane-side half and is landed.
