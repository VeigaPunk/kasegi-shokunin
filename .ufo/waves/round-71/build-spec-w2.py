#!/usr/bin/env python3
"""Build the round-71 attempt-2 v1 wave spec (12 seats, band 8-16).

Wave w1 was dispatched by the dead attempt-1 L1 and its 10 surviving seat reports
are committed evidence. Four of its attack seats never reported (CriticC1, CriticC2,
MutationC1, SentinelGate). This wave re-attacks with fresh identities, re-verifies
both frozen claims at the lane tip, and drafts the round's missing artifacts.
"""
import json

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
TIP = "3cc8cd45cb6f8ca49a292f3b2647c5bddac71486"
FREEZE = "0e260a54b0a670cee2915237ac403d37164c749d"
GATE = "182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603"
DONO = "7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5"
BASE69 = "c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde"
COUNTER = "80020705e1ff8c3cd8b0d2d20485589d8f17b65e9d1aae9eb9af2f748dd61c0b"
S106 = "291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db"

CONTEXT = """# Goal
Kasegi round 71, attempt 2, ONE v1 wave: re-verify or falsify TWO claims frozen in attempt 1, and produce the round's missing artifacts. L1 `KasegiR71` is the planner seat (the validator rejects a `planner` role) and the sole integrator: you never commit, never push, never run a mutating git/jj command, and you write production files ONLY when your item names them. Otherwise you write your report file.

Lane repo {lane}, tip `{tip}`. Frozen claims `{freeze}` — read `{lane}/.ufo/waves/round-71/claims.json` and `{lane}/.ufo/waves/round-71/controls/pins-r71.txt` before anything else. Attempt-1 seat reports are committed at `{lane}/.ufo/waves/round-71/w1/` (10 of that wave's 14 seats reported; `CriticC1`, `CriticC2`, `MutationC1`, `SentinelGate` died — do not trust an absent verdict).

C1 (depth:verifiability) is a per-script python-head census in the derive gate `{lane}/corpus/instruments/figure-audit.py` (sha256 `{gate}`, selftest 106 cases): `PY_DENIED_ANY` (--out/--output/--selftest), `PY_HEAD_REFUSED` (frontier-recheck-count.py), `PY_DENIED_BY_SCRIPT` (per-script --root/--json/--url/--work/--scratch), and `PY_SCRIPT_CENSUS` (allowlist; a head it does not name is refused). Frozen counter `{lane}/.ufo/waves/round-71/controls/c1-probe-run-r71.py` (sha256 `{counter}`) over N1-N12 + R1-R8 + five whole-gate limbs. Committed controls: do-nothing gate (round-70 bytes, sha256 `{dono}`) `VERIFY measurements=25 failures=13` exit 1; r69 base gate (sha256 `{base69}`) `failures=14` exit 1; candidate `failures=0` exit 0.

C2 (coverage) is frontier F49 on S106 — TrendAI Zero Day Initiative's own About page (120-day standard coordination window; 30/60/90-day shortening for incomplete or problematic patches; escalation after 15 business days of vendor silence; full advisory after a patch vs a limited advisory when no fix arrives; validate -> formal monetary offer -> payment -> vendor coordination; credit or anonymity). Capture `{lane}/corpus/source-snapshots/round-71/S106.txt` (sha256 `{s106}`, 148 lines) with a 15-quote manifest; entry `{lane}/corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md`; registry row S106.

# Contract
- Read committed bytes with `git -C {lane} show <rev>:<path>`, or clone/shared-checkout into your own scratch. NEVER `git add/commit/checkout/reset/push` in the lane, and never a mutating `jj` command anywhere.
- Scratch: every clone, fixture, work dir and receipt lives under `/fast/scratch/hyaku/kasegi-r71/<SeatName>/` (NVMe). `mkdir -p` it, pass it explicitly (`TMPDIR=...`, `--work ...`), never write a citable receipt under `/tmp`. Delete your scratch tree before you yield (`trap 'rm -rf -- "$S"' EXIT`), after copying receipts into your report file.
- Any git fixture repo: `D=$(mktemp -d -p /fast/scratch/hyaku/kasegi-r71/<SeatName>) && git -C "$D" init -q`, every later git call names `-C "$D"`, and `git -C "$D" rev-parse --show-toplevel` must print `$D` before the first commit. Never commit with a throwaway identity anywhere else.
- Report file: the `Report:` trailer path is relative to `{lane}` — write it at `{lane}/<that path>`. Under 400 lines; measured commands and their observed output lines only, never a summary of a run you did not do. An unrun check has not passed; "could not reproduce" is a finding, not a failure of your seat.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; read `/home/vgpnk/.omp/agent/RULES.md` first (official channels, update-safety gate; record tool/version/channel/reason in your report). PACMAN GUARD (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/`npx`/an official binary in `~/.local/bin`, or report the need.
- An executor seat may spawn ONE read-only `labrat` probe for a falsifiable hypothesis; every other role is a leaf; no seat runs its own swarm.
- Never message `agent://all`. Findings go in your report file.
"""

ITEMS = []


def add(name, role, prompt):
    ITEMS.append({"name": name, "role": role, "prompt": prompt})


add("VerifyC1", "reviewer", """Independently reproduce C1's frozen predicate from COMMITTED bytes at the lane tip `{tip}` (not at the attempt-1 base).
(1) `S=/fast/scratch/hyaku/kasegi-r71/VerifyC1; mkdir -p $S; git -C {lane} clone --shared {lane} $S/clone; git -C $S/clone checkout {tip}`. Confirm `sha256sum $S/clone/corpus/instruments/figure-audit.py` = `{gate}` and `sha256sum $S/clone/.ufo/waves/round-71/controls/c1-probe-run-r71.py` = `{counter}`; both must equal `controls/pins-r71.txt`.
(2) Run the frozen counter three times on that clone, each with its own `--work` under `$S`:
  a. `python3 -B .ufo/waves/round-71/controls/c1-probe-run-r71.py --gate corpus/instruments/figure-audit.py --work $S/FINAL --mode candidate` -> expect `VERIFY measurements=25 failures=0`, exit 0.
  b. `--gate <export of the round-70 gate: git -C {lane} show 39cde8a:corpus/instruments/figure-audit.py written to $S/r70-gate.py> --work $S/DONO --mode donothing` -> expect `failures=13`, exit 1, and specifically `N8 ... marker_runs=1`.
  c. `--gate <r69 base gate: .ufo/waves/round-70/controls/base-gate-r70.py if it exists, else git show 656272cf:corpus/instruments/figure-audit.py> --work $S/BASE --mode base` -> expect `failures=14`, exit 1.
(3) Apply the claim's kill rule literally: report any MEASURE line whose values disagree with `claims.json`, any gate sha256 drift, and whether the do-nothing run still scores >=10 failures.
(4) Audit one thing the attempt-1 wave did not: R8's pipeline is `python3 corpus/instruments/capture-binding-check.py --root . | grep -c records=84`, but the tip's records count is 85. Measure what R8 actually returns at the tip (`direct_rc`, `gate_rc`, the pipeline's stdout) and state whether R8 is still a discriminating positive control or a vacuous row that passes on both sides. Quote the counter's `value_ok` logic.
Report: `C1: VERIFIED` / `C1: NOT VERIFIED <reason>`, the three VERIFY lines verbatim with exits, and the R8 finding with its numbers.""")

add("AttackC1", "critic", """Falsify C1's declared sentence, measured. It claims the gate refuses N1-N12 "while admitting every read-only derive in the enumerated set R1-R8 that the round-70 critic measured as over-refused, re-deriving each one's own value; a python head not in the census is refused (fail closed)".
(1) Over-refusal: read `corpus/instruments/figure-audit.py` at `{tip}` (`PY_DENIED_ANY`, `PY_HEAD_REFUSED`, `PY_DENIED_BY_SCRIPT`, `PY_SCRIPT_CENSUS`, `python_flags_ok`) and enumerate plausible read-only derives now refused. Run at least these directly and through the gate, on a shared clone: `frontier-recheck-count.py --root .` (head refused), `score-gap.py --root .`, `shonen-form.py --root .`, `limb-mutation-check.py --root .`, `citation-ground-check.py --json`, `gate-quote-audit.py --json`, `resolve.py .`, `claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar --json`. Report a table: command, direct exit/value, gate verdict, and whether the refusal is load-bearing or inert.
(2) Vacuous controls: measure the R8 row (see VerifyC1 §4) and say whether any other R row passes on both sides without comparing a nonempty value; name it with the code line.
(3) Under-refusal: which write/exec shapes stay reachable? Measure at least: a denied spelling before/after `--`; `python3 -m <mod>`; `python3 -c`; an env var changing a counter's behaviour (`TMPDIR`, `PYTHONPATH`); a counter's own write on a positional path (`python3 corpus/instruments/resolve.py <lane>` writes its census — measure whether it really writes and where); a head reached through a symlink; nested python invoked by an admitted counter.
(4) Verdict: does the declared sentence survive as written? Name every surviving counter-example with its command and observed rc/stderr, and give the smallest safe correction set for round 72 (do not edit the gate).
Report: `C1: VERIFIED` / `C1: NOT VERIFIED`, the over-refusal table, the vacuous-row finding, the reachable-class list, and the correction set.""")

add("MutateC1", "mutation-tester", """Mutation-test the gate's refusal rules, with focus on the eight per-script entries attempt-1's lesson calls unpinned (`V71-1`) and the two it calls equivalent (`V71-2`, `V71-3`).
(1) `S=/fast/scratch/hyaku/kasegi-r71/MutateC1; mkdir -p $S; git -C {lane} clone --shared {lane} $S/clone; git -C $S/clone checkout {tip}`. Copy the real `corpus/instruments/` tree into your scratch so the census-completeness case stays meaningful, and edit only the copy of `figure-audit.py` there (its basename must stay `figure-audit.py`).
(2) Build one-limb mutants, each removing exactly one rule: M1 `--selftest` from PY_DENIED_ANY; M2 `--output`; M3 the short `-o` arm; M4 the `PY_HEAD_REFUSED` entry; M5 `capture-source.py`'s `--url`; M6 the census allowlist check (no-op); M7 the global-deny regression (deny `--root`/`--json` to every head); M8 the eight unpinned entries V71-1 names, one mutant each (`citation-ground-check.py --json`, `gate-quote-audit.py --json`, `mirror-containment-check.py --json`, `resolve-dispatch-check.py --json`, `limb-mutation-check.py --root`, `r46-c1-gate.py --root`, `capture-source.py --work`, `capture-source.py --scratch`).
(3) For each mutant run `python3 <scratch>/corpus/instruments/figure-audit.py --selftest` and record `cases=`/`failures=`/exit. A mutant that stays `failures=0` is a SURVIVOR. For each survivor also run the frozen counter (`--mode candidate --gate <mutant>`) and report whether the round's own probe set kills it.
(4) Report the kill matrix and, per survivor, the smallest selftest case that would kill it (rule + expected rc).
Report: matrix (mutant, rule, selftest exit, cases, failures, counter verdict, killed/survived) and `MUTANTS killed=<n>/<m> survivors=<list>`.""")

add("SentinelC1", "sentinel", """Adversarial security review of the derive gate at `{tip}`: what does it still let a hostile or careless `derive:` string do?
(1) Read `tokenize`, `parse_derive`, `segment_ok`, `python_head_ok`, `python_flags_ok`, `run_derive` in `corpus/instruments/figure-audit.py`. Name the trust boundary: the gate decides admission, then something executes the string.
(2) Measure at least eight bypass attempts on a shared clone, each as a minimal ledger with one figure whose `derive` is the string; record the gate verdict, then what the gate-run process actually did (`marker_runs`, files written, child processes). Cover: (a) `python3 corpus/instruments/capture-source.py -- -o x`; (b) a `--url` spelling the deny list misses (`--ur`, `--u`, `–url` with an en dash); (c) `python3 -m http.server` / `python3 -m json.tool`; (d) a symlink inside `corpus/instruments/` pointing outside it; (e) `python3 corpus/instruments/figure-audit.py --selftest`; (f) `env PYTHONPATH=/x python3 corpus/instruments/gate-quote-audit.py --root .`; (g) `sort -T /tmp` / `sort --compress-program=sh` (round-68 class); (h) `git -c core.pager=sh show HEAD:corpus/SOURCES.md`; (i) two positive controls (`capture-binding-check.py --root .`, `claim-package-check.py <exemplar> --json`) that MUST stay admitted, so blanket refusal is not a gain.
(3) Verdict per attempt with the exact rc and stderr; then a severity-ordered residual list and whether any residual is a NEW regression this round (r70 -> r71) or an old one.
Report: the attempt table, `REGRESSIONS=<n>`, and the residual list with severities.""")

add("VerifyC2", "reviewer", """Re-measure C2's frozen after-values at the lane tip `{tip}` with your OWN plain counts (do not run a lane instrument for the counts; run the census only as the last line).
Run on a shared clone at `{tip}`: `grep -cE '^\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|' corpus/SOURCES.md` (expect 106); `ls corpus/knowledge/*.md | wc -l` (87); `grep -cE '^\\| F[0-9]+ \\|' corpus/README.md` (49); `wc -l < corpus/instruments/knowledge-expected.txt` (89); `grep -vc '^#' corpus/instruments/knowledge-expected.txt` (87); `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt` (exit 0); the summed `sources[]` length over `corpus/source-snapshots/**/manifest.json` (85 over 44 dirs); `python3 corpus/instruments/capture-binding-check.py` (`records=85 bound=85 unbound=0`, exit 0); `python3 corpus/instruments/frontier-recheck-count.py` (`FRONTIER-CENSUS rows=49 admitted=49 closed=49 problem-rows=0 registry=106` and `entries=52 pass=52 exit=0`); `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` (exit 0).
Then audit the claim's own artifacts: the S106 registry row (11 cells, tier A, status mined, opened 2026-11-05, `used-by` resolving to an existing file); F49 present in `corpus/README.md` naming both S106 and the entry path; the entry file citing S106 and each of its anchors resolving inside `corpus/source-snapshots/round-71/S106.txt`.
Note for the record: attempt-1's `ReviewC2` reported NOT VERIFIED at `4e33119` because the registry row landed later (`34faab9`). Confirm whether the tip now reproduces every frozen after-value, and if any value differs say which and by how much.
Report: `C2: VERIFIED` / `C2: NOT VERIFIED <reason>` plus the count table with one output line per command.""")

add("AttackC2", "critic", """Source-outrun audit of the F49 entry (criterion R108) — attempt-1's `CriticC2` died, so this is unrun.
(1) Read `corpus/source-snapshots/round-71/S106.txt` in full at `{tip}` and the 15 quotes in `corpus/source-snapshots/round-71/manifest.json`. Build two lists: what the page states, and what a reader would be tempted to attribute to it that it does not state. Test at least: (a) the 120-day window as an industry or coordinator norm rather than ZDI's own policy; (b) 30/60/90 read as a severity ladder rather than the incomplete/problematic-patch case; (c) "may escalate" read as a deadline guarantee; (d) the "no backlog" sentence read as applying to other programmes; (e) the page read as a severity taxonomy; (f) any statement about Microsoft or Pwn2Own as if the page said it; (g) a rebrand claim (TrendAI) the page does not support.
(2) Audit `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md` sentence by sentence against the anchors it cites (`S106.txt:N`); list every sentence that outruns its anchor, with entry line number, anchor, and the correction.
(3) Check the registry row S106 and the F49 frontier row in `corpus/README.md` for the same outruns (a frontier row is a claim too).
Report: `OUTRUNS=<n>` with the list (O1..On: entry line, anchor, quoted source line, correction), and `ENTRY HASH` before/after any correction you recommend (do not edit the entry yourself).""")

add("CountTip", "executor", """Produce the round's before -> after receipt at the lane tip, byte-exact and pasteable, plus the frontier-step censuses. You may write ONLY `{lane}/.ufo/waves/round-71/controls/attempt2-tip-counters.txt` — nothing else in the lane tree.
(1) Shared clone at `{tip}`; run each command once, with its exit code, writing the combined output to that receipt file:
  - `cat .ufo/waves/round-71/controls/c2-base-counters-r71.txt` (the BEFORE values)
  - `python3 corpus/instruments/frontier-recheck-count.py | head -2`
  - `python3 corpus/instruments/capture-binding-check.py | tail -1`
  - `wc -l < corpus/instruments/knowledge-expected.txt; grep -vc '^#' corpus/instruments/knowledge-expected.txt; LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt; echo $?`
  - `ls corpus/knowledge/*.md | wc -l; grep -cE '^\\| F[0-9]+ \\|' corpus/README.md; grep -cE '^\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|' corpus/SOURCES.md`
  - `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo $?`
  - `sha256sum corpus/instruments/figure-audit.py .ufo/waves/round-71/controls/c1-probe-run-r71.py` (compare against `controls/pins-r71.txt`)
  - the assimilation collision guard, exactly: `A=/fast/scratch/hyaku/kasegi-r71/CountTip/asim; mkdir -p $A; grep -oE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > $A/reg-ids; grep -oE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}' /home/vgpnk/Projects/shokunin/../../Projects/shokuknow/merge/kasegi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > $A/staged-ids; wc -l < $A/reg-ids; wc -l < $A/staged-ids; comm -12 $A/reg-ids $A/staged-ids | wc -l` (if `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` is absent, say so and report the shape instead).
  - the quarantine slice: `awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {{print $4, $5}}' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md | tee -a $A/quarantine-slice`; then for EACH row print the S-id and say whether the row carries an S-id cell (quarantine matrix integrity).
(2) The receipt must be plain text with one `# command` / output / `# exit=N` triad per command so the L1 can paste it into the report.
Report: the receipt path, its line count, and any command whose value differs from the frozen after-values.""")

add("DraftScorecard", "scribe", """Draft the SCORECARD.md round-71 section (the L1 integrates it; you write ONLY `{lane}/.ufo/waves/round-71/w2/ScorecardDraft.md`).
Read `{lane}/SCORECARD.md` (round-69 and round-70 sections are the shape to follow), `.ufo/waves/round-71/claims.json`, `.ufo/waves/round-71/controls/{c1-donothing-r71.txt,c1-base-r71.txt,c1-candidate-trial-r71.txt,c2-base-counters-r71.txt}`, and `corpus/lessons/round-71.md`.
Produce, in the lane's exact table shape:
- `## Round 71 — ...` heading naming C1 (per-script python-head census) and C2 (F49/S106 ZDI)
- the frozen-claims line (freeze `{freeze}`, base `4e33119e0167cac3fbfa15afb3f2f5b98a43cc60`, pins `controls/pins-r71.txt`, C1 implementation sha `{gate}`)
- the axis table rows: depth:verifiability before -> after with the counting command; coverage before -> after with the counting command; depth:density "not targeted, no credit"
- a `### Round-71 move log` table (round, axis, before, after, evidence)
- `**Capabilities:**` line (no new row; `derive-gate-chain-refusal` extended in place)
- `**Saturation:**` line (9/10 per owned axis; lowest non-retired axis depth:verifiability 4, worked nominally; no retirement/split/waiver)
- a `### Planned after round 71 (not frozen)` list with at least three concrete next items drawn from `corpus/lessons/round-71.md` § Routed defects (V71-1, V71-2, V71-3) and the next coverage ground.
Every number must be one you read from a committed receipt (name it) or one produced by a command you ran yourself; mark which is which. No placeholder text, no invented hash.
Report: the draft path, its line count, and a `RECEIPTS:` list of every receipt file each number came from.""")

add("DraftLog", "scribe", """Draft the `LOG.md` round-71 entry (the L1 appends it; you write ONLY `{lane}/.ufo/waves/round-71/w2/LogDraft.md`).
Read `{lane}/LOG.md`'s round-68/69/70 entries for the shape (a `## Round N — title` heading, then bullets: declared claims, pre-freeze controls, freeze, wave, implementation, measurements, C2 landing, routed defects, assimilation, capability/score posture).
Write the round-71 entry from committed evidence only: `.ufo/waves/round-71/claims.json`, `.ufo/waves/round-71/controls/*`, `corpus/lessons/round-71.md`, `corpus/README.md` F49 row, `corpus/SOURCES.md` S106 row, and `.ufo/waves/round-71/w1/*.md` (the ten attempt-1 seat reports).
It must record honestly: (a) attempt 1's wave spawned 14 seats and 4 attack seats died with no output (`CriticC1`, `CriticC2`, `MutationC1`, `SentinelGate`); (b) attempt 1's L1 died before filing a report, so the round is completed in attempt 2; (c) C2's registry row landed only in the late commit `34faab9`, which is why attempt-1 `ReviewC2` graded NOT VERIFIED at `4e33119`; (d) the lane tip at integration is `{tip}` and the round is not admitted until the non-author closure verifies it.
Report: the draft path, its line count, and the list of evidence pointers you used.""")

add("DraftReport", "scribe", """Draft the round report body (the L1 completes it; you write ONLY `{lane}/.ufo/waves/round-71/w2/ReportDraft.md`).
Read `/home/vgpnk/Projects/shokunin/.ufo/reports/round-70/kasegi.md` for the required shape and `/home/vgpnk/Projects/shokunin/.ufo/prompts/kasegi-round-71.md` section 4 for the section list. Draft, with real measured values only:
- **Work performed** — opens by naming the two declared claims and their axes, then one bullet per work item with an evidence pointer (path, command output line, or commit)
- **Landed changes** — each change tied to a LOG entry and the commit carrying it (commits: `0e260a5` freeze, `4e33119` C1 gate + S106 capture, `453275f` seat reports + entry + registry + README, `34faab9` registry row, `3cc8cd4` lesson)
- **Before -> after measurements** — one per claim with the frozen counting command and the commit measured
- **Sources & frontier** — SOURCES rows before -> after with the census command, rows added by tier, rows touched, frontier rows advanced, and `Assimilation: none` with the collision count
- **Trend verdicts** — one verdict each for expansion, quality, discernment
- **Stale-lane** — one line (respawn-per-round driver; no other mission of this lane is open)
- **Tooling** — record that no tool was installed this round unless a seat's report says otherwise
Leave `## SHONEN` for the L1. For every value you cannot verify from a committed receipt, write `L1 TO FILL` instead of a number.
Report: the draft path, its line count, and a `GAPS:` list of every place you left `L1 TO FILL` with why.""")

add("ScoutNext", "scout", """Reconnaissance for round 72 and the coverage frontier (read-only; no lane edits).
(1) Province fit of the round's C2 ground: read `{lane}/PROVINCE.md`, the F49 row and its neighbours in `{lane}/corpus/README.md`, and the registry rows S106 plus S003/S004/S005/S041/S043/S044/S045/S051/S095. Is the ZDI acquisition-programme ground distinct from each? Answer per row with the line you compared.
(2) Sibling ownership: `grep -l` the sibling lanes' `PROVINCE.md` under `/home/vgpnk/Projects/shokunin/*-shokunin/` for acquisition-programme / bug-bounty / disclosure-policy ground and report what each holds (read-only).
(3) Next-round leads: propose at least five candidate sources a bounty triager or VR analyst needs that the registry does NOT already hold — exact URL, the document/programme, the ground it adds, and whether it is out of province. Include at least two acquisition-programme primary sources and two region-specific ones.
(4) Check whether `corpus/README.md`'s `## Leads (unopened)` section is current (does it name only the Fuzzilli primary documentation?) and report the exact lines.
Report: per-row distinctness verdicts, the sibling scan, the five-lead list with province verdicts, and the leads-section state.""")

add("ConnectorTable", "connector", """Cross-source comparison table that makes F49's distinctness checkable by a reader (attempt-1's `ConnectorScope` wrote one; extend and verify it, do not trust it).
(1) From committed bytes only (`{lane}/corpus/knowledge/*.md`, `{lane}/corpus/SOURCES.md`, `{lane}/corpus/source-snapshots/`), build a table of every coordination-window statement the lane already holds: CISA (S003/S004/S005), ISO 29147/30111 and JPCERT (S041/S042), FIRST PSIRT (S098/S100/S101), CERT/CC phases (S095), GitHub advisory curation (S105), and ZDI (S106). Columns: party, window, shortening/escalation rule, who publishes, what happens on vendor refusal, and the entry file plus anchor that states it.
(2) Mark every cell where two sources genuinely disagree (not merely different scope) and every cell where the ZDI row is the only holder.
(3) Name any place where F49 duplicates an existing frontier row's ground, with the row id and the overlapping sentence; then `SCOPE CLEAR` or the overlap list.
(4) Check the attempt-1 table at `{lane}/.ufo/waves/round-71/w1/ConnectorScope.md` against your own build: list every cell it got wrong or unanchored.
Report: the table, the disagreement list, the duplicate list, and the corrections to `ConnectorScope.md`.""")


def subst(text):
    for k, v in (("lane", LANE), ("tip", TIP), ("freeze", FREEZE), ("gate", GATE),
                 ("dono", DONO), ("base69", BASE69), ("counter", COUNTER), ("s106", S106)):
        text = text.replace("{" + k + "}", v)
    return text


CONTEXT = subst(CONTEXT)
for _item in ITEMS:
    _item["prompt"] = subst(_item["prompt"])

spec = {
    "wave": "kasegi-r71-w2",
    "milestone": "round-71 attempt 2: re-verify/falsify C1 (per-script python-head census) and C2 (F49/S106 ZDI), run the attack seats attempt 1 lost, and draft the round's missing artifacts",
    "reportDir": ".ufo/waves/round-71/w2",
    "maxLanes": 16,
    "axes": ["depth:verifiability", "coverage"],
    "context": CONTEXT,
    "items": ITEMS,
}
path = "/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-71/w2-spec.json"
with open(path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(spec, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("wrote", path, "items", len(ITEMS))
