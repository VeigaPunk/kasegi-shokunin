# kasegi — round 71

Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (jj-colocated, branch `master`).
Lane tip at report: `<<TIP>>`. Round base (round-70 closure): `39cde8ab…`.
Claims freeze: `0e260a54b0a670cee2915237ac403d37164c749d`.
Report commit: filed through `fleet-commit.sh --as kasegi`; the lane commit it cites is `<<TIP>>`.

**Declared claims (2).** Both frozen before any implementation byte, in `.ufo/waves/round-71/claims.json`
(sha256 `c530ec65…`, pins `controls/pins-r71.txt`), with the pre-freeze do-nothing and base controls
committed in the same freeze commit.

1. **C1 — depth:verifiability (lowest non-retired axis, nominal 4 per R58).** The derive gate refuses the
   twelve enumerated python-head write/exec/ingress shapes N1–N12 while admitting the eight read-only
   derives R1–R8 the round-70 critic measured as over-refused — each re-deriving its own value — and
   fails closed on a python head its per-script census does not name. Before: the round-70 gate
   (sha256 `7a8d52eb…`) refused all eight read-only derives and still ran a root-supplied `recheck:`
   payload through `bash -c` with no option at all. After: gate sha256 `182f4ef7…`, selftest 106 cases.
2. **C2 — coverage (8 held).** Frontier F49 admitted on S106, TrendAI ZDI's own About page: the
   acquisition-programme disclosure process and vendor coordination. Before: 48 frontier rows, 105
   registry rows, 51 entries, 84 capture records, 86 knowledge files. After: 49 / 106 / 52 / 85 / 87.

**Verdicts this round.** **C1: NOT VERIFIED as declared** — its frozen predicate reproduces (25/0 exit 0) but the sentence's clause "re-deriving each one's own value" is false for R5-R8, and the per-script repair re-admits write flags on 23 heads (measured, `SentinelC1`); score 4 → 4, no improvement claimed, a trade reported. **C2: VERIFIED** on its declared content (F49 admitted on S106 with the entry, capture manifest and registry row) with its ground narrowed by erratum 1 (four of the five listed items were already held at S075); every C2 counter reproduces at the tip.

## Work performed

**Attempt 1 (inherited, spent the round's freeze and its build wave).** The attempt-1 L1 froze both claims,
implemented C1, landed C2 and spawned a 14-seat v1 wave, then died before filing a report
(`.ufo/watchdog.log`: `lane-dead-no-report kasegi round=71`, three attempts). Its work is committed and
was re-verified in this attempt rather than trusted: `0e260a5` (freeze + controls), `4e33119` (C1 gate,
S106 capture, entry, README F49, knowledge-expected), `453275f` (ten of the wave's fourteen seat reports,
registry row, PROVINCE, QUALITY R110), `34faab9` (late seat output: registry row S106), `3cc8cd4` (late
seat output: the lesson). Four of that wave's attack seats — `CriticC1`, `CriticC2`, `MutationC1`,
`SentinelGate` — died with no output, so the round arrived with no adversarial grading of either claim.

**Attempt 2 (this attempt) — one fresh v1 wave, 12 seats, plus the L1's own integration.**

- **Frozen-control completion.** The frozen `controls` list names a blanket-refusal forgery "to be produced
  at the wave"; attempt 1 never produced it. Produced here:
  `.ufo/waves/round-71/controls/c1-forgery-r71.txt` — `VERIFY measurements=25 failures=12`, exit 1, against
  the committed round-70 forgery gate (sha256 `126de75d…`), so blanket refusal is not a gain.
- **C1 re-verified at the tip, not at the freeze base** — seat `VerifyC1`: `VERIFY measurements=25
  failures=0` exit 0 at gate `182f4ef7…`; do-nothing gate `7a8d52eb…` 25/13 exit 1 (`N8 … marker_runs=1`);
  r69 base gate `c09b0fb1…` 25/14 exit 1. `C1: VERIFIED`. Evidence: `.ufo/waves/round-71/w2/VerifyC1.md`.
- **C1 falsification** — seat `AttackC1`: **`C1: NOT VERIFIED` as written.** The numeric predicate reproduces (`VERIFY measurements=25 failures=0`, exit 0), but the sentence's clause "re-deriving each one's own value" is false for four of the eight positive rows: R5-R8 exit nonzero when run directly, so the counter takes its stale-exit branch, the gate stamps `derived=UNAVAILABLE` and compares nothing (V71-6 / R116). Independent second finding: the fail-closed census is name-only — a file carrying a censused basename is admitted and executed against any `--root`. Evidence: `.ufo/waves/round-71/w2/AttackC1.md` § Verdict, §2, §3.
- **C1 mutation matrix** — seat `MutateC1`: `<<MUTATEC1>>`
- **C1 gate security review** — seat `SentinelC1`: **`REGRESSIONS=2`**, both consequences of the r71 mechanism and both measured refused-at-base → admitted-and-effective: (R1) `--root`/`--work`/`--scratch` are no longer refused globally and the per-script table covers only ten heads, so **23 censused heads re-admit at least one base-denied flag**; one ledger derive wrote **22,012 files** into a ledger-chosen directory (`rc=1`, no refusal) where the round-70 gate refused the same ledger with `rc=2`; (R2) the census is keyed on basename while containment is keyed on realpath, so an in-directory alias named after a selftest fixture restores the denied flags and **wrote 2,595 bytes**. Residuals include a CRITICAL older one (`freeze-check.py` is an admitted `bash -c` primitive via `--claims`) and a HIGH older one (`figure-audit.py -- --selftest` is admitted and runs the selftest). Evidence: `.ufo/waves/round-71/w2/SentinelC1.md` §4-§5.
- **C2 re-verified with plain counts at the tip** — seat `VerifyC2`: `C2: VERIFIED`, every frozen
  after-value reproduces (`rows=49 admitted=49 registry=106`, `entries=52 pass=52`, `records=85 bound=85
  unbound=0`, expected 89/87 sort-clean, 87 files, census exit 0). Attempt-1's `ReviewC2` had reported
  NOT VERIFIED at `4e33119` because the registry row landed later (`34faab9`) — M71-2 / R111.
  Evidence: `.ufo/waves/round-71/w2/VerifyC2.md`.
- **C2 outrun audit** — seat `AttackC2`: `OUTRUNS=8` (O1-O4 in the entry, O5-O6 in the binding registry and frontier rows, O7 in the manifest note, O8 in the row's date cell). All eight applied in-round (R108): the entry, `corpus/SOURCES.md:118`, the F49 row, the manifest note and the ground line corrected in place; entry `6f304a05…` → `d61e4f6f…` (262 lines), manifest `815566ac…` → `1e2f2d47…`, registry `1d4d4e74…` → `75c31bf1…`, README `85715e2f…` → `ac2a49dc…`; every C2 counter unchanged after the edits. Evidence: `.ufo/waves/round-71/w2/AttackC2.md` §2; `corpus/lessons/round-71.md` § Errata E71-1.
- **Round counters at the tip** — seat `CountTip`: receipt `.ufo/waves/round-71/controls/attempt2-tip-counters.txt` (170 lines) — every frozen C2 after-value reproduces at the tip, the pins match, the collision guard reads `reg-ids=106 staged-ids=94 collisions=76`, the 7-row quarantine slice carries S-ids, and the counter's three modes re-run 25/0, 25/13, 25/14 with the forgery at 12 failures.
- **C2 distinctness erratum (L1).** The frozen C2 sentence lists the 120-day window, the 30/60/90-day
  shortening, the 15-business-day escalation and the full-versus-limited advisory choice as F49's ground.
  `ScoutF49` measured all four already held from ZDI's own policy page S075 (`S075.txt:23-25`) in
  `corpus/knowledge/zdi-disclosure-policy.md`. Correction landed append-only as `corpus/README.md`
  `[r71 erratum 1]`: F49's ground is the acquisition-side flow (validate → severity → formal monetary offer
  → payment → vendor coordination → credit or anonymity), the no-limit/no-backlog guarantees, the dossier
  contents, and three measured wording divergences between S106 and S075 — the escalation publishes a
  *limited* advisory where S075 publishes a public one; S106's 120 days is stated unconditionally where
  S075 conditions it on a vendor response; S075's 15 business days starts after a 5+5-day acknowledgement
  ladder the About page does not name. The row, the entry and every counter are unchanged; M71-3 / R114.
- **C1 measurement gap routed (L1).** The frozen counter's R8 row is
  `capture-binding-check.py --root . | grep -c records=84`; the tip prints `records=85`, so the pipeline
  yields an empty value and `figure-audit.py:587` passes on `"" == ""`. R8 still proves the pipeline is
  *admitted*, but its value limb proves nothing. Measured: `grep -c records=84` → `0`, rc 1; counter line
  `R8-capture-binding-pipeline ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1`. Routed V71-4 / R112,
  independently confirmed by `VerifyC1` §4.
- **Stale pin repaired (L1).** `SKILL.md:1224` pinned `selftest cases=96` for a gate that prints 106.
  Corrected to 106 with an `[r71 current-execution amendment]` block; density measured no-harm
  (270.9 → 272.6 mean, 925 → 932 path cites, 38 blocks, `anchorcheck.py` exit 0, 0 `BAD`). Routed V71-5 /
  R113.
- **Lesson and criteria.** `corpus/lessons/round-71.md` gains M71-2 (after-state across two commits),
  M71-3 (ground already held) and V71-4/V71-5; `corpus/QUALITY.md` gains R111–R114.
- **Assimilation hand-check (L1).** Collisions re-derived at this attempt: 106 registry ids vs 94 staged,
  **76 colliding** (`.ufo/waves/round-71/assimilation/attempt2/collisions`). The 7-row quarantine slice is
  hand-checked row by row (`.ufo/waves/round-71/assimilation/attempt2/quarantine-verdicts.md`): 0 adopted,
  0 fabrication refusals, 7 unverifiable (payload absent / register prose class), 7 already held by the
  lane registry.
- **Seat drafts reviewed** — `DraftScorecard`, `DraftLog`, `DraftReport`: `<<DRAFTS>>`

### Wave outcome

**Attempt 2 wave `w2`: 12 seats, all roles on the host route table (no `model` passed).** Role mix:
2 reviewer, 2 critic, 1 mutation-tester, 1 sentinel, 1 executor, 3 scribe, 1 scout, 1 connector — attack
seats 6/12 = 50 %, one connector seat, no `planner` seat (the L1 holds the canonical planner seat; a
`planner` role is rejected by the validator). Report dir `.ufo/waves/round-71/w2`, dispatch
`w2-dispatch.json`, ready-file handoff `w2.ready` (`l1: KasegiR71`), dispatched 2026-11-04T23:56:40.
`<<WAVEOUTCOME>>`

**Attempt 1 wave `w1` (inherited, not re-run):** 14 seats, 10 reported, 4 dead (`CriticC1`, `CriticC2`,
`MutationC1`, `SentinelGate`) — no seat was replaced. Round seat total across both attempts: 26 spawned,
22 reported, 4 dead. Attempt 2's wave alone is 12 seats, inside the 8–16 band; attempt 1's is 14.

## Landed changes

| change | LOG entry | commit |
|---|---|---|
| Frozen claims + r71 controls (do-nothing, r69 base, candidate trial, C2 base, pins) | `## Round 71` bullet 2–3 | `0e260a5` |
| C1 per-script census in `corpus/instruments/figure-audit.py` (sha256 `182f4ef7…`, selftest 106) | bullet 4 | `4e33119` |
| C2: S106 capture + 15-quote manifest, entry, README F49, knowledge-expected, PROVINCE, QUALITY R110 | bullets 5 | `4e33119`, `453275f` |
| S106 registry row (105 → 106) | bullet 5 | `34faab9` |
| Ten attempt-1 seat reports + wave evidence | bullet 6 | `453275f` |
| `corpus/lessons/round-71.md` (M71-1, V71-1…V71-3, C1/C2 measurements) | bullet 7 | `3cc8cd4` |
| Attempt-2 wave evidence (`build-spec-w2.py`, `w2-spec.json`, `w2-dispatch.json`, `w2.ready`, seat reports), forgery receipt, attempt-start census, assimilation attempt-2 receipts | this report | `<<TIP>>` |
| M71-2/M71-3, V71-4/V71-5 in the lesson; QUALITY R111–R114; SCORECARD round-71 section; LOG round-71 entry; `SKILL.md` pin 96 → 106 + r71 amendment; `corpus/README.md` `[r71 erratum 1]` | this report | `<<TIP>>` |

## Before → after measurements

**C1 (depth:verifiability).** Frozen counting command:

```
python3 -B .ufo/waves/round-71/controls/c1-probe-run-r71.py --gate <gate exported from the measured revision> \
  --work /fast/scratch/hyaku/kasegi-r71/<seat>/FINAL --mode candidate
```

| run | before (round-70 gate `7a8d52eb…`, base at `39cde8a`) | after (r71 gate `182f4ef7…` at `4e33119`, re-run at tip `<<TIP>>`) |
|---|---|---|
| candidate | — | `VERIFY measurements=25 failures=0` exit 0 |
| do-nothing (r70 gate) | `VERIFY measurements=25 failures=13` exit 1, N8 `marker_runs=1`, R1–R8 `admitted=0` | same 25/13 exit 1 (the control is unchanged by design) |
| r69 base gate `c09b0fb1…` | `failures=14` exit 1, every N row admitted | same 25/14 exit 1 |
| blanket-refusal forgery `126de75d…` | not produced by attempt 1 | `failures=12` exit 1 (`controls/c1-forgery-r71.txt`) |
| selftest | 96 cases | 106 cases, `failures=0` |

Receipts: `controls/c1-donothing-r71.txt`, `controls/c1-base-r71.txt`, `controls/c1-candidate-trial-r71.txt`,
`controls/c1-forgery-r71.txt`. Score **4 → 4, delta 0, nominal per R58**: the axis counter `resolve.py`
reads citation resolution and this gate does not move it.

**C2 (coverage).** Frozen counting command:

```
python3 corpus/instruments/frontier-recheck-count.py; python3 corpus/instruments/capture-binding-check.py; \
wc -l < corpus/instruments/knowledge-expected.txt; grep -vc '^#' corpus/instruments/knowledge-expected.txt; \
LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt; ls corpus/knowledge/*.md | wc -l; \
grep -cE '^\| F[0-9]+ \|' corpus/README.md; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md; \
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```

| counter | before (`controls/c2-base-counters-r71.txt`, measured at `39cde8a`) | after (measured at `<<TIP>>`) |
|---|---|---|
| `FRONTIER-CENSUS` | `rows=48 admitted=48 closed=48 problem-rows=0 registry=105` | `rows=49 admitted=49 closed=49 problem-rows=0 registry=106` |
| frontier entries | `entries=51 pass=51 exit=0` | `entries=52 pass=52 exit=0` |
| capture binding | `records=84 bound=84 unbound=0` | `records=85 bound=85 unbound=0`, exit 0 |
| knowledge-expected | 88 lines / 86 entries, sort clean | 89 / 87, `sort -c` exit 0 |
| knowledge files / frontier rows / registry rows | 86 / 48 / 105 | 87 / 49 / 106 |
| sources census | exit 0, six inherited W04 | exit 0, the same six W04 |

Score **8 → 8, delta 0** (the coverage denominator is operator-owned). C2's distinctness erratum above
narrows the *ground* the row may claim without touching any counter.

## Sources & frontier

Census command (run at attempt start and at round end):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```

- **Attempt-start census** (`controls/census-attempt2-start.txt`): exit **0**, six inherited W04
  duplicate-scope warnings (S028, S029, S072, S076, S080, S085), `ok …/corpus/SOURCES.md`. Attempt 1 had
  already landed the round's row, so the attempt-start registry is 106.
- **Round-level before → after:** registry rows **105 → 106** (before from the committed round-70 base
  receipt `controls/c2-base-counters-r71.txt`, after measured at the tip).
- **Rows added by tier:** 1 row, tier **A** (S106, `mined`, opened 2026-11-05, recheck 180d, `used-by`
  `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md`).
- **Rows touched old → new:** S106 added; no existing row's cells changed (`git diff --numstat 39cde8a..TIP
  -- corpus/SOURCES.md` = `2 0`: the row and its Search-log bullet).
- **Frontier rows advanced:** F48 → F49 (S106), `entries 51 → 52`, `knowledge-expected 88/86 → 89/87`,
  `capture records 84 → 85`.
- **Round-end census:** exit **0**, same six inherited W04 warnings, `ok`.
- **Assimilation: none.** The staged `merge/kasegi` set collides with 76 of the lane's 106 registry ids
  (mass id drift; the round-70 L0 question is still the routing item), so nothing is adopted; the 7-row
  quarantine slice is hand-checked with a per-row verdict in
  `.ufo/waves/round-71/assimilation/attempt2/quarantine-verdicts.md`.
- **considerthese:** `considerthese/2026-10-26.md` exists and is operator-authored; its proposal 3
  (quiescence gate) is already carried as QUALITY R110. No new proposal is implemented this round.

## Trend verdicts

- **expansion — improved.** The corpus gains genuinely new ground: F49's acquisition-side flow (validate →
  severity → formal monetary offer → payment → vendor coordination → credit or anonymity), the
  no-limit/no-backlog guarantees and the dossier contents, with a 15-quote capture and an entry that
  anchors each statement. Registry 105 → 106, frontier 48 → 49, entries 51 → 52, capture records 84 → 85.
  The erratum narrows what the row may claim; it does not remove the ground.
- **quality — unchanged (a trade, not a gain).** The derive gate's refusal set moved from a global deny list to a per-script census (selftest 96 → 106) and the frozen predicate reproduces 25/0, but the declared sentence is false for four of eight positive rows and the same change re-admits `--root`/`--work`/`--scratch` on 23 heads, one measured 22,012-file write where the base refused, plus a fixture-name alias that restores denied flags (2,595 bytes). No quality credit is claimed; R115/R116 and V71-6…V71-10 carry the repairs.
- **discernment — improved.** Attempt 1's attack wave lost four of its six attack seats and produced no
  adversarial grade; this attempt re-attacked with fresh identities and produced two independent C1
  verdicts, a C2 outrun audit, a mutation matrix and a gate security review; the round also caught its own
  two accounting defects (R8's vacuous value limb; a C2 ground already held at S075) and narrowed them
  honestly instead of counting them as wins.

## Stale-lane

Respawn-per-round driver (`hyaku-inline`); this lane has no other open mission. Round 71 ran on this
Linux/omp host; no Windows-host receipt was re-declared.

## Tooling

No tool was installed or upgraded this round by the L1 or by any seat that reported; no `pacman`
transaction was attempted (the host-wide pause stands). Environment used: `python3 3.14.8`,
GNU coreutils `sort 9.12`, `git 2.56.0`, `jj 0.45.1`, `node`/`ufo-swarm-wave.mjs` for the wave spec.

## SHONEN

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SKILL.md:1224`
  (gate row, pin corrected 96 → 106) and the `[r71 current-execution amendment, 2026-11-05]` block;
  author-asserted, outside promotion verification remains required.
- [ ] At least one end-to-end domain task executed and logged in LOG.md — not claimed; no authorized
  end-to-end bounty task, former roots absent, live-target testing refused.
- [~] Instructions executable by an agent without oral context — this round's receipts are re-runnable
  commands (`controls/c1-probe-run-r71.py`, `controls/c1-forgery-r71.txt`,
  `controls/c1-candidate-trial-r71.txt`, `controls/attempt2-tip-counters.txt`); the standing caveat in
  `corpus/lessons/round-47-verifier-spotcheck.md` remains.
- [~] No cross-domain bleed (PROVINCE.md still accurate) — no PROVINCE change this round; both claims
  stay inside the lane's province (a derive gate over the lane's own instruments; an acquisition
  programme's own disclosure process), sibling scan `ConnectorScope` `SCOPE CLEAR`.
