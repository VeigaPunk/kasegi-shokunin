author: RevKillRule
round: kasegi 34 — hyaku run 8, leaf reviewer (L2 wave 1)
lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin
lane base: 014ee2d7aa8c3c095ff57ae51097606a9906228c · claims freeze 29f606dbdd28aff6fd4573ab4b90788bbb90af13
date: 2026-10-26
claim touched: C1 depth:verifiability — review of the survivor-mutant counter `corpus/instruments/kill-rule-check.py`
role: review only. I edited no instrument and no corpus file; my only lane writes are this receipt and two
stray scratch files that I self-caught and removed (§8). All fixtures and copies lived under
`/fast/scratch/hyaku/kasegi-r34/RevKillRule/` (removed before yield, §9). No tool installs were needed
(stdlib-only work); no VCS commands beyond read-only `git log`/`git status`/`git show`/`git diff`.

# Round 34 — RevKillRule

## Report

### Verdict

**PASS.** Every criterion in the seat item holds on the frozen counter bytes
`c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61` (43138 B, 881 lines) against the
landed instrument bytes `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` (40556 B,
892 lines), and each criterion was verified **independently of the counter's own replay** (my own patch
application, `py_compile`, and probe runs). Per-criterion evidence in §1–§7; residual observations
(explicitly disclosed limits, not defects) in §7; the wave's generation churn and one self-caught
defect of mine in §8.

### 1. The claim's counting command — `survivors=0`, exit 0, deterministic

`python3 corpus/instruments/kill-rule-check.py` (cwd = lane root, `HYAKU_SCRATCH=/fast/scratch/hyaku/kasegi-r34/RevKillRule`),
run twice; both runs exit 0 and are byte-identical; stdout sha256
`85d80cb2c8c6cbf237bba0941617b7ad9904db6fbaabac0d5e7066b9f3bb9027` — equal to the digest
`ExecKillRuleCheck.md` §3 quotes for the frozen generation. The run prints, in order:

- Header binding both byte sets: `KILL-RULE instrument=corpus/instruments/capture-binding-check.py
  sha256=3d9e5e0d… bytes=40556 lines=892 floor=19 counter_sha256=c279d952…` — the instrument digest is
  measured at run time, not hardcoded (verified: pointing `--instrument` at the round-33 bytes
  `b4182665…` prints that digest instead and fails loudly, §6).
- Nine `probe <name> pristine=pass` lines (shape gate + 8 external fixtures), then
  `pristine selftest cases=23 case-lines=23 floor=19 floor_met=1` (the frozen C1 conjunct N>=19 met).
- Exactly one `mutant=<name> killed=0|1` line per named mutant — three lines, all `killed=1`.
- `control=…` lines for all four controls, then `controls=4 rejected=4`.
- Seven `GATE ok` lines (`named-rows`, `pristine-selftest`, `pristine-fixtures`,
  `pristine-determinism`, `rows-valid`, `controls`, `survivors-zero`), then
  `mutants=3 killed=3 survivors=0 invalid=0`, `gates=7 failed=0`, `survivors=0`.

Exit rule verified in both directions: green run exit 0; a deliberately surviving `--row-file` row
prints `mutants=4 killed=3 survivors=1` and exits 1 (§6); a missing instrument exits 2
(`UNAVAILABLE reason=instrument …`).

### 2. Exactly-once textual patches over the landed bytes (independent count)

I extracted the three rows from the counter's own `MUTANTS` list (imported unmodified from the landed
file) and counted occurrences of each `find` in the **landed instrument bytes** with
`bytes.count` — not via the counter:

| mutant | find span (landed bytes, 1-based) | find_count | limb the span sits in |
|---|---|---|---|
| `skip-selftest-summary` | `capture-binding-check.py:822-823` (`base = scratch_base(scratch_arg)` / `os.makedirs(base, exist_ok=True)`, the entry of `def selftest`) | 1 | selftest section |
| `accept-record-without-url` | `:297-299` (`url = record.get("url")` + the `detail=absent` return inside `def bind_record`) | 1 | rule B url-required limb |
| `per-file-binding-removal` | `:440-442` (`orphans.append((name, capture))` + the `rule=orphan-capture` failure append inside `def check`) | 1 | rule A per-file orphan detection |

Each patch is one contiguous `find`/`replace` pair (single strings, applied with one
`bytes.replace(find, replace, 1)`); the counter enforces `find_count==1` per row at run time
(`status=invalid:find-count` otherwise) and additionally pins each named row by digest
(`ROW_PINS`, `find` and `find\0replace` sha256) — I recomputed all six pin digests from the rows and
they match (`battery3` §1, all PASS), so a substituted named patch is `invalid:anchor-mismatch`
(demonstrated in §6).

### 3. Each mutant still compiles

Applied each patch to a copy of the landed bytes and ran `py_compile.compile(..., doraise=True)`:
all three compile (PASS ×3). The two control shapes behave as declared: the `CTL-nocompile` patch
(`def parse_round(dirname):` → `def parse_round(dirname)`) fails `py_compile` with a SyntaxError
(PASS), and the `CTL-noop` patch (`SCHEMA_VERSION = 1` → itself, exactly-once at `:96`) leaves the
bytes unchanged (`invalid:noop`, PASS).

### 4. Each mutant flips the relevant limb (independent replay, not the counter's)

I ran each mutated copy myself against probe fixtures I built from the landed instrument's own
fixture shape (`probes.py` in my scratch), and compared with the pristine baseline I pinned first:

- Pristine baseline (landed bytes): url-less fixture → exit 1,
  `FAIL rule=url-mismatch record=S002 detail=absent dir=round-30`, `records=2 bound=1 unbound=1`;
  orphan fixture → exit 1, `FAIL rule=orphan-capture file=S009.txt dir=round-30`,
  `orphans=1 orphan=S009.txt`; `--selftest` → exit 0, 23 `selftest case=` lines,
  `selftest cases=23 failures=0`.
- `skip-selftest-summary` → `--selftest` prints exactly `selftest cases=0 failures=0`, exit 0, **zero**
  `selftest case=` lines (the case loop is short-circuited: the patch prepends
  `print("selftest cases=0 failures=0", file=out); return 0` at `selftest()`'s entry). The round-33
  F-5 shape, now rejected by the shape gate (`summary-only;case-set-mismatch`). **Flipped.**
- `accept-record-without-url` → url-less fixture: exit **0**, `MANIFEST round-30 records=2
  url_bound=2 fetched=1 archival=1`, `records=2 bound=2 unbound=0` — the absent-url record binds
  (exactly the output the executor spec predicts for this mutant). Isolation: the orphan fixture
  still exits 1 with `rule=orphan-capture` (rule A untouched), and the mutant's own `--selftest`
  fails (`cases=23 failures=1`). **Flipped.**
- `per-file-binding-removal` → orphan fixture: exit **0**, no `FAIL` line, and the AUDIT orphan
  token is gone (`orphans=0`, no `orphan=S009.txt`) — the mutant neither lists nor fails the
  undeclared capture (its note says exactly this). Isolation: the url-less fixture still exits 1
  with `detail=absent` (rule B untouched), and its own `--selftest` fails (`cases=23 failures=2`).
  **Flipped.**

The counter's own replay agrees and adds the cross-check I could not do by hand: each mutant is
`killed_by` the probes named above **and** passes the seven non-target probes (e.g.
`accept-record-without-url` passes `per-file-orphan`, `unnamed-record-id`, `stale-orphan-declaration`,
`malformed-fetched-utc`, `punctuated-url-cell`, `malformed-orphan-declaration`, `nested-legacy-round`)
— the flips are limb-isolated, not whole-program breakage.

### 5. Output contract: one line per mutant, `survivors=K`, honest aggregates

- One `mutant=<name> killed=0|1` line per mutant: verified (3 lines, byte-exact grammar
  `mutant=%s killed=%d`).
- Summary `survivors=K`: verified (`survivors=0` green; `survivors=1` red via `--row-file`, §6).
- `killed` semantics as documented: "a probe the pristine bytes pass is failed by the mutant"
  (R17-compatible; a no-op/equivalent patch is a `survivor`, never relabelled).
- Invalid rows are never kills and never survivors: `invalid:*` rows print `mutant-invalid`, count in
  `invalid=`, fail the `rows-valid` gate, and force exit 1 (verified with a tampered counter copy,
  §6).
- `--selftest` (verdict arithmetic only): `selftest cases=3 failures=0`, exit 0, on the frozen bytes.

### 6. Controls rejected — all four, plus the two deeper rejections

- `CTL-noop` → `verdict=invalid:noop expect=invalid:noop ok=1` — a no-op patch is **not** a kill.
- `CTL-nocompile` → `verdict=invalid:nocompile … ok=1` — a non-compiling patch is **not** a kill.
- `CTL-equivalent` → `verdict=survivor … ok=1 witness_survivors=1 witness_exit=1` — the comment-only
  patch proves the counter can report survivors>0 and exit 1 (not an always-zero printer). I verified
  the patch is comment-only, compiles, changes bytes, and that no probe sees it.
- `CTL-fake-killrule` → `verdict=opaque expect=opaque ok=1 … fake_mutant_lines=0 … real_mutant_lines=3
  witness_survivors=1 differs=1 stable=1` — the committed fake is bound by path (newest
  `.ufo/waves/round-*/c1-controls/fake-killrule.py`, resolvable with `--fake`), and the control fails
  (`ok=0`, gate fail, exit 1) if the fake is missing (`absent`) or if it ever printed a full evidence
  span (`evidential`).
- Deeper rejection 1 — **evidential fake**: I forged a fake that prints the real tool's full line
  shape (3 `mutant=` lines, 3 `patch_sha256=` tokens, one `mutants=` line, `survivors=0`) without
  replaying anything; the counter prints `verdict=evidential expect=opaque ok=0`, fails the
  `controls` gate, and exits 1. Shape-mimicry alone does not pass the control.
- Deeper rejection 2 — **row substitution**: a tampered copy of the counter (one named row's
  `replace` altered) run against the landed instrument prints
  `status=invalid:anchor-mismatch detail=find-or-patch-digest`, `mutants=3 killed=2 survivors=0
  invalid=1`, `GATE fail name=rows-valid`, exit 1 — no false green. `--row-file` reusing a named
  row's name is rejected at parse: `UNAVAILABLE reason=row-file …: row 0 reuses the name
  'skip-selftest-summary'`, exit 2.
- Red aggregate through the public CLI: `--row-file` with a comment-only survivor row prints
  `mutant=comment-only-survivor killed=0`, `mutants=4 killed=3 survivors=1`, exit 1.

### 7. The fake runner does not satisfy the output contract — three independent ways

1. **Structurally**: `.ufo/waves/round-34/c1-controls/fake-killrule.py` (sha256
   `7ca5d4fa97c6dadcb8f8b63a8f86f12a75d41335fdded8e46b1475a6cbb3b1af`, 305 B) prints exactly
   `survivors=0` and nothing else — no `mutant=` line (the contract requires one per mutant), no
   patch digests, no `mutants=`/`gates=` lines, no header binding any instrument bytes.
2. **By the counter's control**: `CTL-fake-killrule verdict=opaque … differs=1 ok=1` — the counter
   explicitly measures the fake's span against its own output contract and records both differences
   (evidence span absent; `survivors=0` printed on a witness run where the real evaluator prints
   `survivors=1`/exit 1).
3. **By the negative control**: a hypothetical fake that DID print the full evidence span is
   `evidential` → `ok=0` → gate fail → exit 1 (§6), so the control is not satisfiable by output
   mimicry either; and the real tool's stdout sha256 (`85d80cb2…`) is a committed, reproducible
   value the fake cannot produce (it replays nothing).

### 8. Generation trail during the wave, and one self-caught defect

The counter was hardened four times while seats attacked it live; the executor's receipt
(`.ufo/waves/round-34/wave1/ExecKillRuleCheck.md` §0) now carries the full table. My measurements per
generation: `e33a300f…` (3 probes — main run + battery, all green); `c51ac05a…` (6 probes — main run +
batteries, all green); `7a20e724…` (declared frozen by the executor, then edited again — my battery2
determinism check failed **only** because its two runs straddled that rewrite; the executor names this
premature freeze as their own defect in §0); final `c279d952…` — one clean pass, digest stable across
a 4-minute watch (8 samples, 30 s apart, identical from t=60 s), all batteries green. Every
generation kept the same three named rows (identical mutant sha256s `b9d40dbe…`, `5897a1f0…`,
`616ce9dd…` throughout) — the churn strengthened the oracle (new probes, `ROW_PINS`, `named-rows`
gate), it never relabelled a survivor.

**Self-caught defect (mine):** my first baseline capture wrote `selftest-baseline.txt` into the lane
root (and aimed a second redirect at the fleet root, where no file materialized — swept
`/home/vgpnk/Projects`, `/tmp`, `/fast/scratch/hyaku`: absent). The lane-root stray is removed
(`rm -v` → "removed …"; `git status --short | grep baseline-plain` → no match). Scratch-discipline
defect, fixed before yield; no lane content was modified by it.

### 9. Residual observations (disclosed limits, not defects)

- The probe set is a bounded oracle: a mutant that keeps every asserted contract line intact
  survives by construction (docstring "Limits"; README "Known limits"). The three named mutants are
  the claim's subject; the instrument's other hardened limbs (strict-UTC, dup-record, double-https,
  rejected-anchor, nested) are guarded by its own 23-case selftest but have no committed kill-rule
  mutants — a future round could widen `MUTANTS` the same way attack seats did this round via
  `--row-file`.
- There is no module-level `invalid:import` gate (limb-mutation-check.py has one): a sabotage patch
  that crashes the instrument would fail every probe and be counted `killed`. The docstring discloses
  this ("not a claim that the mutated limb is the only cause"); it does not affect the three named
  mutants, each of which I verified flips its limb while leaving the other probes passing.
- The counter cannot defend its own summary line against an edit to its own bytes; it prints
  `counter_sha256` for exactly this binding (verified: my two runs bind `c279d952…`).

### 10. Commands (all cwd = lane root unless stated; `HYAKU_SCRATCH=/fast/scratch/hyaku/kasegi-r34/RevKillRule`)

| command | exit | result digest / key output |
|---|---|---|
| `python3 corpus/instruments/kill-rule-check.py --json …/kr-final.json` | 0 | stdout sha256 `85d80cb2…`; `survivors=0` |
| `python3 corpus/instruments/kill-rule-check.py --scratch …` (2nd run) | 0 | byte-identical to run 1 (`cmp` silent) |
| `python3 corpus/instruments/kill-rule-check.py --selftest` | 0 | `selftest cases=3 failures=0` |
| `python3 corpus/instruments/kill-rule-check.py --fake .ufo/waves/round-34/c1-controls/fake-killrule.py` | 0 | `CTL-fake-killrule … ok=1 differs=1` |
| `python3 corpus/instruments/kill-rule-check.py --fake …/evidential-fake.py` (my forgery) | 1 | `verdict=evidential ok=0`, `GATE fail name=controls` |
| `python3 corpus/instruments/kill-rule-check.py --row-file …/survivor-row.json` | 1 | `mutants=4 killed=3 survivors=1` |
| `python3 corpus/instruments/kill-rule-check.py --row-file …/reuse-named.json` | 2 | `UNAVAILABLE reason=row-file … reuses the name` |
| `python3 corpus/instruments/kill-rule-check.py --instrument /nonexistent` | 2 | `UNAVAILABLE reason=instrument` |
| `python3 corpus/instruments/kill-rule-check.py --instrument …/cb-round33.py` (29f606d bytes) | 1 | `pristine selftest-refused reasons=cases=11<floor=19`, `GATE fail name=pristine-selftest` — loud, no silent zero |
| tampered counter copy + explicit `--fake` | 1 | `invalid:anchor-mismatch`, `GATE fail name=rows-valid` only |
| my `battery.py` / `battery2.py` / `battery3.py` (scratch) | 0 / 0 / 0 | 20 + 10 + 9 PASS, 0 FAIL |
| `sha256sum corpus/instruments/{capture-binding-check,kill-rule-check}.py` | 0 | `3d9e5e0d…` / `c279d952…` |

Instrument bytes unchanged by every run I made (`3d9e5e0d…` before and after; counter reads them
read-only into scratch copies). No `kill-rule-*` scratch leftovers after any run (the counter's
`mkdtemp` is removed in `finally`).

### Scratch

`/fast/scratch/hyaku/kasegi-r34/RevKillRule/` removed before yield (verified absent). No tool
installs or upgrades (stdlib-only). Lane writes: this receipt only, plus the §8 strays now removed.
