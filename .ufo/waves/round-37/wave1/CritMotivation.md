# CritMotivation — round 37, critic: do-nothing base control for C1 and C2

Seat: CritMotivation · role: critic · axes: depth:verifiability, coverage · milestone: round-37
Scope: run every C1 and C2 counter against untouched `git archive` exports and decide whether
either after-state is reachable by doing nothing; then decide whether either claim is a
re-scoring of held knowledge. Read-only on lane/fleet/shokuknow; no mutating git in the lane
(one scratch clone + one `mktemp` fixture under my own scratch dir). Only writes: this receipt
and `/fast/scratch/hyaku/kasegi-r37/CritMotivation/` (removed after this file was written).

| tag | ref | use |
|---|---|---|
| BASE | `b56a41680cefd391868c1c370dc063c69d827e7d` | round-37 base |
| FREEZE | `224df74db2a46d627ae1475a72ca48796bbd177c` | claims freeze |
| HEAD | `b362068195d5489aa94b31e6ec8f880c367e0ba0` | **the no-op control**: freeze + wave spec/plan/dispatch + claims-erratum-1 |
| R36BASE | `cc692008b0cfd58d18275aa6c4aed79620120799` | claim's required-red ref |
| R36HEAD | `a23dc4788aa7c98831eed6db953434034ce5ae8d` | claim's required-red ref |

Live state at measurement: lane HEAD = HEAD, `git status --porcelain` = 6–7 lines (all untracked
round-37 wave artifacts), 21 seat dirs under `/fast/scratch/hyaku/kasegi-r37`,
`git diff --stat BASE..HEAD -- corpus/` = **0 lines**. The round has committed *claims and
dispatch* and not one corpus byte.

## 1. Verdict

**Neither claim is reachable by a do-nothing run at BASE, and the round's own commits are the
do-nothing control: BASE and HEAD are counter-identical on all fourteen C2/C1 predicates.** Both
after-states are conjunctions whose leading limbs are absent at BASE. There is no path from
"commit the claims" to any target number.

Two calibration facts must ride with a `closed=14/14` / `entries=23 pass=23` receipt:

1. **Nine of C1's fourteen checks are pins, not round-37 work.** E1–E8 are already green at BASE
   (measured by executing the r36 suite on the BASE export); E9 is live-bound; only E10–E14 are
   round-37 limbs. `14/14 = 8 pins + E9 rewrite + 5 round-37 limbs`.
2. **The proposed C1 closure has two gameable limbs** (§5): E9's scratch root defaults to the
   *round-36* directory (a verbatim copy closes while 21 round-37 seat dirs exist), and E14's
   two grep-shape clauses are satisfiable without fixing D6 (demonstrated: a failing `git status`
   read still yields `E9 ... status-dirty=0 ... closed=1` and `closed=9/9 exit=0`).

C2 is a genuine surface move, not a re-scoring (§6). It is not *virgin* coverage either: SSVC is
already named in three committed captures (S003/S004/S008) that no row or entry has mined; the
claim's delta is the decision-point mechanism, and the entry must be written against that delta.

## 2. Method

Every number below comes from an export, never the dirty worktree:
`git -C {LANE} archive <ref> | tar -x -C /fast/scratch/hyaku/kasegi-r37/CritMotivation/<tag>`.
C2 counters run with `--root <export>` where the instrument accepts it. `recheck-audit.py` is
root-scoped: `--root` defaults to `os.getcwd()` and the `cdroot` strict limb compares a command's
`cd <path>` target to `--cdroot` (default `= root`). From the BASE export:

```
python3 corpus/instruments/recheck-audit.py --quiet                       -> strict pass=1/48
                                                                           cdroot_fail=47 ... exit=1
python3 corpus/instruments/recheck-audit.py --root <BASE> --cdroot {LANE} --quiet -> expected=48 exit=0
python3 corpus/instruments/recheck-audit.py --quiet        (in {LANE})    -> expected=48 exit=0
```

C2's counting command is therefore valid **only from the lane root**; a verifier running the
listed command inside an export gets `exit=1` on a claim that is not false. Fail-closed (no
silent green), but the receipt must name the root.

## 3. C1 — fourteen predicates at BASE

Suite limb: `bash corpus/instruments/r37-closure.sh --export-ref b56a416` →
`No such file or directory`, `RC=127`; `--selftest` unavailable; `.ufo/waves/round-37/final-gates/all-gates.txt`
absent. A do-nothing seat sits at **closed=0/14, no selftest, no receipt**.

| check | BASE evidence | verdict |
|---|---|---|
| E1 structural binding | `grep -cF 'filled by the L1' SCORECARD.md`=0; `grep -cF '<LANE_HASH>'`=0; r36 suite payload `round36-final-lane-commits=2,bound=2 closed=1` | **green at base (pin)** |
| E2 round-34 erratum | r36 payload `erratum-marker=1,erratum-row=1,erratum-mean=7 closed=1`; `corpus/lessons/round-34*.md` present | **green at base (pin)** |
| E3 registry rows | `SKILL.md:1110` `r35-defect-closure.sh`, `:1111` `r36-closure.sh`; r36 payload `registry-r35=1,registry-r36=1 closed=1` | **green at base (pin)** |
| E4 round-35 results tracked | `git ls-tree -r b56a416 | grep round-35/wave1-results.json` → 1 + `.provenance.md`; payload `tracked-ref=1,provenance-note=1 closed=1` | **green at base (pin)** |
| E5 claims-erratum-d5 | `.ufo/waves/round-35/claims-erratum-d5.md` present; payload `closed=1` | **green at base (pin)** |
| E6 L1Integration correction | `.ufo/waves/round-34/wave1/L1Integration.md`; payload `correction-round35=1 closed=1` | **green at base (pin)** |
| E7 QUALITY supersedes | `corpus/QUALITY.md:249` `supersedes R22`, `:250` `supersedes R23`; payload `supersedes-r22=1,supersedes-r23=1 closed=1` | **green at base (pin)** |
| E8 round-36 lesson correction | payload `m36-rows=4,names-corrected-line=3,stale-line=0 closed=1` | **green at base (pin)** |
| E9 quiescence | live-bound; at measurement `status-dirty=6–7, scratch-seat-dirs=0, head-match=0` → `closed=0`; D6 shape present (`r36-closure.sh:465` status read `2>/dev/null`, `:466` `porcelain=${porcelain:-0}`) | **open (D6), and see §5** |
| E10 all-gates receipt | `.ufo/waves/round-37/final-gates/` absent. R36HEAD's receipt has **0** `E<n> payload=` lines, **0** `selftest case=` lines, only `closed=0/9 exit=1` and `closed=3/9 exit=1` — D1 verbatim | **open** |
| E11 LOG correction | `grep -c round-37 LOG.md` = 0; the false path is live at `LOG.md:1665` ("Landed `corpus/instruments/r36-closure.sh` + `corpus/instruments/r36-fixtures/`"); `git ls-tree -r BASE | grep -c r36-fixtures` = 0 | **open (D2)** |
| E12 anchor-ancestor labels | `corpus/lessons/round-37*` = 0 files; SCORECARD's last section is `## Round 36` (L1406); `grep -c 'Final lane commit: e666d902' SCORECARD.md` = 1 (L1492, inside the round-36 block); `git merge-base --is-ancestor e666d902 BASE` → true | **open (D4)** |
| E13 registry row shape | `SKILL.md:1111` type cell = literal `gate\|probe`; verdict-map cell reads "exit 0 only for K=9" and carries **no** exit-2 → could-not-evaluate row | **open (D5)** |
| E14 fail-closed shape | `grep -cF 'porcelain:-0' r36-closure.sh` = 1; status read swallows stderr | **open (D6)** |

D1–D6 are open at BASE exactly as the claim's `before` says; E1–E8 are inherited corrections that
the suite must keep green (regression pins).

## 4. The do-nothing limb (this seat's core measurement)

### 4a. BASE vs HEAD — a metadata-only round moves nothing

| counter | BASE | HEAD | after target |
|---|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | **19** | **19** | 20 |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | **53** | **53** | 54 |
| `grep -rlE '^source: S054 ' corpus/knowledge \| wc -l` | **0** | **0** | 1 |
| `ls corpus/knowledge/*.md \| wc -l` | **48** | **48** | 49 |
| `frontier-recheck-count.py` | **entries=22 pass=22 exit=0** | **entries=22 pass=22 exit=0** | 23/23 |
| `source-recheck.py --source S054` | **exit=2** (`manifest UNAVAILABLE reason=missing-required-argument`; with the round-37 manifest path: `reason=missing`) | **exit=2** | exit 0 |
| `capture-binding-check.py` | **records=43 bound=43 unbound=0** | **records=43 bound=43 unbound=0** | 44 |
| `recheck-audit.py` (root-scoped) | **expected=48, pass=48, exit=0** | **expected=48, pass=48, exit=0** | 49 |
| `corpus/source-snapshots/round-37` | **absent** | **absent** | present + bound |
| `knowledge-expected.txt` | 50 lines = 2 comments + **48** entries | same | 49 entries |
| `r37-closure.sh` | **absent** | **absent** | `closed=14/14 exit=0` |
| `final-gates/all-gates.txt` | **absent** | **absent** | digest + 14 payload lines |
| `sources-census.sh validate --root … kasegi` | **exit=0**, W04 S028/S029 only | **exit=0**, same | exit 0 |
| `c2-controls/junk-f20.md` | absent | absent | rejected w/ receipt |

`git diff --name-only BASE..HEAD` = 8 paths, all `.ufo/waves/round-37/` claim/dispatch files
(`claims.json`, `claims-erratum-1.md`, `wave1-spec.json`, `wave1-plan.out`, `wave1-dispatch.json`,
`c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt`). **Zero corpus writes,
zero counter movement.** The claim's own `before` columns reproduce exactly; only `audit` needs
the root qualifier of §2.

Census and the binding *exit status* are already green at BASE (43/43); they are non-regression
pins. The discriminating C2 counters are the counts (43→44, 48→49, 19→20, 53→54) and presence.

### 4b. Sensitivity — the counters are live, and they fail closed

Measured in scratch copies of BASE:

- Delete F19's entry + row: frontier **19→18**, knowledge **48→47**, harness **22→21**,
  `recheck-audit` `expected=48 missing=1 unexpected=0 exit=1`. The counters respond to removal
  and the audit reds rather than silently accepting the loss.
- Add only a junk F20 row (`knowledge/does-not-exist.md`): `FAIL F20 … problems=missing-entry`,
  **entries=23 pass=22 exit=1**. The entry count is reachable by a row; the *pass* count is not.
- Add a prose-only entry with a correct `source: S054` declaration and a `recheck:` line pointing
  at the round-37 manifest: `problems=selection-not-cited-by-entry,manifest-unreadable`,
  **exit=1**. `frontier-recheck-count.py` rule B requires the named manifest to exist and list the
  id, rule D executes `source-recheck.py` (capture bytes), and the citation limb requires the body
  to cite the id outside the declaration/recheck lines. **`pass=23` therefore requires the capture
  + manifest + citation; no textual shortcut reaches it.**
- Rename-only C1: `cp r36-closure.sh r37-closure.sh` → `closed=8/9 exit=1`, `--selftest`
  `cases=9`. A relabel is worth 9 checks, not 14.

### 4c. `closed=14/14` cannot be reached by a copy, but *can* be reached by a copy plus two tricks

Both were executed against the real r36 suite, which is the template the round-37 suite inherits:

- **Wrong scratch root (silent, and it is live today).** `r36-closure.sh:128` sets
  `SCRATCH_ROOT=/fast/scratch/hyaku/kasegi-r36`. A verbatim copy therefore audits the *round-36*
  root: with a clean lane clone (`--lane <clone>` at BASE) it prints
  `E9 payload=status-dirty=0,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present closed=1`
  and `closed=9/9 exit=0` **while 21 round-37 seat dirs existed on disk at measurement** (r36
  root: 0 dirs). The
  payload prints `scratch-root=present` but not *which* root — a typo is visible, a valid-but-
  wrong round is not. This is exactly the claim's own kill shape: "any single E-check's committed
  fixture proves the check can pass while its defect is present".
- **Fail-open survives a grep-clean rewrite.** `E14` as frozen is two shape clauses
  (`grep -cF 'porcelain:-0'` → 0, no status-read `2>/dev/null`). Renaming the variable and keeping
  `${dirty:-0}` passes both greps and stays fail-open. Demonstrated end-to-end with a `git` shim
  that fails only `status` (repo otherwise clean, `head-match=1`):
  `E9 payload=status-dirty=0,...,closed=1` and `closed=9/9 exit=0` — **identical to the honest
  clean run**, despite `fatal: status read failed` on stderr and a non-zero status exit. D6 is
  real at BASE and is *observable*: with the same shim on the live lane the payload flips from
  `status-dirty=7` to `status-dirty=0`.

## 5. Re-scoring assessment

**C1 (held 4)** is not a re-scoring: the score does not move, the suite is absent at BASE, and
E10–E14 each require an artifact that cannot be produced by relabelling (a committed receipt with
a suite digest, a named LOG correction, a label change on a real section, a registry-row rewrite,
a code change). The claim discloses the carry-over. The risk is narrower and mechanical: the
*implementation* of E9/E14 can be surface-shaped (above), so a green `closed=14/14` would not by
itself prove D6 closed. That is a fixture defect in the proposed work, not a false claim.

**C2 (held 7)** is a surface move, not a re-scoring: frontier, registry, knowledge, capture and
audit all move, and no held row or entry covers SSVC. But SSVC is **not new to the corpus bytes**:
`corpus/source-snapshots/round-24/S003.txt:239` ("Suppliers should leverage risk assessment and
decision support systems such as Stakeholder-Specific Vulnerability Categorization (SSVC) to help
prioritize reports") and `:252` ("CISA uses SSVC to help prioritize the remediation of
vulnerabilities in FCEB agencies"), `S004.txt:9,21` (CERT/CC nav), `S008.txt:174`. None of those
rows mines it (`grep -rli ssvc corpus/knowledge` = 0, `SOURCES.md` has no SSVC row, `README.md`
has no F20). So the honest delta is **method, not name**: the decision-point/outcome structure.
The nearest neighbour is F18 (KEV: "exploitation-status-based prioritization"): both use
exploitation status as a prioritization input, so the entry must state what SSVC adds (stakeholder
-specific decision points × exposure × mission impact → outcome classes) or C2's coverage credit
partly double-counts F18's ground.

## 6. Impacted axes and smallest safe corrections

- **depth:verifiability (C1)** — three fixes before the suite is landed:
  1. `r37-closure.sh` must set `SCRATCH_ROOT=/fast/scratch/hyaku/kasegi-r37`, and E9's payload
     must print the **resolved scratch-root path** (not just `present|absent`), so a stale-round
     root is visible in the receipt.
  2. E14 needs a **behaviour limb**, not only two greps: ship a fixture with a `git` shim that
     fails `status` while `rev-parse --git-dir` succeeds, and require `E9 closed=0` with a named
     `status-read-failed` payload token. Without it a rename passes E14 and D6 stays open.
  3. The negative-control receipts (R36BASE `cc692008`, R36HEAD `a23dc47`) must keep the
     per-check `E<n> payload=` lines. E9 reds on those refs for `head-match=0` (it compares the
     live HEAD to `--export-ref`), so "E10–E14 open there" is true but not the whole cause; the
     receipt must attribute the limbs or the red is unattributable.
  4. Optional but cheap: pin E10's `suite-sha256` to the **export's** suite bytes (digest taken
     from `$TREE/corpus/instruments/r37-closure.sh`), so a post-gate edit of the worktree copy
     cannot satisfy the header.
- **coverage (C2)** — no harm to the axis; every discriminating counter is at its BASE value.
  Smallest safe correction: the knowledge entry's teaches line states the delta against F18/F19
  (exploitation-status input vs stakeholder-specific decision points) and cites the S054 capture
  for the mechanism only; the frontier row keeps `S054` as its sole source. Do not write the
  entry as "SSVC first appears here" — S003/S004/S008 already name it.
- **calibration (this seat)** — attribute `14/14 = 8 pins + E9 rewrite + 5 round-37 limbs`; keep
  `census exit 0` and `capture-binding exit 0` as pins, with the **counts** (43→44) as the
  discriminators.

## 7. Limits

- One read per counter; no kill judgment (that is CritC1Kill/CritC2Claim/CritC2Kill).
- `r37-closure.sh` is not landed, so E10–E14 are predicate measurements plus executed analogues
  against the r36 suite; where the analogue is the evidence it is labelled as such.
- The live lane was dirty during measurement (6–7 untracked wave files, 21 seat dirs), so E9's
  live red is wave-time state, not a BASE defect. The final-gates run must follow commit +
  cleanup; E9 cannot be green before that.
- Scratch `/fast/scratch/hyaku/kasegi-r37/CritMotivation/` (BASE, HEAD, R36HEAD exports, one
  scratch clone, one `mktemp` fixture, `TMPDIR`) removed after this receipt was written. No tool
  installs, so no tooling-ledger entry.

Report: `.ufo/waves/round-37/wave1/CritMotivation.md`
