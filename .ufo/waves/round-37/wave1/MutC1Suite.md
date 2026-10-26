# MutC1Suite — one-limb mutation probes of the planned r37 closure suite

Round 37, wave 1, seat `MutC1Suite` (mutation-tester, leaf). Judged on depth:verifiability.
Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` at HEAD `b362068195d5489aa94b31e6ec8f880c367e0ba0`
(claims-freeze `224df74db2a46d627ae1475a72ca48796bbd177c`, base `b56a41680cefd391868c1c370dc063c69d827e7d`).

## Instrument under mutation

- The **planned r37 suite** (`corpus/instruments/r37-closure.sh`, checks E1–E14) exists in **no bytes
  anywhere yet**: the C1 before-control records `suite_missing=1` at base `b56a416`, and
  `git log --all -- corpus/instruments/r37-closure.sh` is empty at HEAD `b362068`. Design rows below are
  therefore stated as exact find/replace over the planned shapes named in the frozen claim, and **every
  limb that already exists in committed bytes is proven empirically on scratch copies of the committed
  r36 suite** `corpus/instruments/r36-closure.sh` (E9/E1/E3/E8 + digest reporting), sha256
  `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` (byte-identical via
  `git archive HEAD` — the suite's own export mechanism).
- The r36 suite's E9 status read is the D6 defect site, lines 465–466:
  `porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain 2>/dev/null | count_lines)` /
  `porcelain=${porcelain:-0}` — a failed status read maps to `status-dirty=0` (clean).

## Method

- Scratch bound at `/fast/scratch/hyaku/kasegi-r37/MutC1Suite/` (removed after this receipt; nothing
  under /tmp, no lane/fleet/source-tree writes except this receipt).
- **Fixture lane F**: `git init` inside scratch (toplevel verified equal to the fixture dir before any
  mutating git), populated with `git archive HEAD` of the real lane, then SCORECARD's two captured
  round-36 anchor hashes (`e666d902…`, `274fa9ae…`) re-bound to fixture commits in two passes
  (anchor names pass-1 commit `H1=9c95148c2a989bfc666facfa9c06aa353acf8e98`, an ancestor of export ref
  `H2=0035ddb96d7e2da0466dceb72df227d1add1d7be`). **Green baseline: pristine suite on F →
  `closed=9/9 exit=0`** (all nine E-lines closed, `suite-sha256=4db1ae70…`).
- **Poison lever** isolating exactly the D6 limb:
  `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=status.showUntrackedFiles GIT_CONFIG_VALUE_0=bogus` makes
  `git --no-optional-locks status --porcelain` fail (rc=128, `fatal: unable to parse
  'status.showuntrackedfiles'`) while `rev-parse --git-dir`, `--show-toplevel`, `rev-parse HEAD`,
  `cat-file`, `merge-base`, `ls-tree`, `ls-files` all still succeed — measured directly on the lane
  before use. Every other check stays green, so any verdict flip is attributable to E9 alone.
- Detector = the suite itself, run `--export-ref <fixture HEAD> --lane F --scratch-root <empty dir>
  --work <scratch dir>`; plus two scripted planned-shape detectors for E10 receipt clauses and the E12
  stale-label window. A baseline failure is reported as inconclusive, never as a kill.

## Mutation table

Verdicts: **KILLED** = the detector flips exactly as predicted; **SURVIVED** = no flip (coverage
finding). Expected flips are stated as closed 1→0 (or 0→1 where the mutant is a detector-weakening
reintroduction measured against a poisoned read).

| id | limb (planned r37 check) | target bytes | exact find → replace | expected flip | observed |
|----|--------------------------|--------------|----------------------|---------------|----------|
| M1a | E9 fail-closed (defect-live probe, no edit) | r36 lines 465–466 (already defective) | — (poisoned run on pristine) | E9 reads a failed status read as clean → `closed=9/9` despite rc=128 | **SURVIVED** — `E9 payload=status-dirty=0,… closed=1`, `closed=9/9 exit=0` under poison. The D6 defect is live in committed r36 bytes; r37's E9 rewrite + E14 shape grep must close it. |
| M1b | E9 rewrite (the planned fix) | r36 465–466 | find `  porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain 2>/dev/null \| count_lines)` + `  porcelain=${porcelain:-0}` → replace with `  if ! porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain); then` / `    printf 'status-dirty=read-failed'` / `    return 1` / `  fi` / `  porcelain=$(printf '%s\n' "$porcelain" \| grep -c . \|\| true)` | poison → E9 closed 1→0 | **KILLED** — `E9 payload=status-dirty=read-failed closed=0`, `closed=8/9 exit=1` (copy sha `b17935f430bda6e1eb01c74f0a015cb19c6ebc2486698a5bd3c1a18d7bad9b45`). Happy path preserved: clean-env run `closed=9/9 exit=0`. |
| M1c | E9 `porcelain:-0` reintroduced (verdict-bearing placement) | fixed copy | find the rc-gate block above → replace with `  porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain)` + `  porcelain=${porcelain:-0}` (gate removed) | poison → E9 flips back 0→1 (fail-open restored) | **KILLED** — `E9 payload=status-dirty=0,… closed=1`, `closed=9/9 exit=0` under poison (copy sha `910fe47d…`-class mutant `mut-gateoff`, sha below). Placement finding: with the rc gate left in place, a bare `porcelain=${porcelain:-0}` line is **dormant** (P3: still `closed=8/9`) yet statically greppable — E14 must be a shape check to catch dormant reintroductions too. |
| M1d | E9 status-read swallow reintroduced | fixed copy | find the rc-gate block → replace with `  porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain 2>/dev/null) \|\| true` + count line | poison → E9 flips back 0→1 | **KILLED** — `closed=9/9 exit=0` under poison (copy sha `09d5be5f9c0af1b7b20f0ee2f364bc41015d695f0abae4b198f6e20599eb7e55`). |
| M2 | E14 shape greps (planned) | five suite copies | greps `grep -cF 'porcelain:-0'` and status-read-lines containing `2>/dev/null` | pristine 1/1 (red by planned E14); fixed 0/0 (green); each reintroduction mutant fires its own grep | **KILLED** — census: pristine `1,1`; fixed `0,0`; mut-fallback `1,0`; mut-swallow `0,1`; mut-gateoff `1,0`. Weakened-pattern mutant `grep -cF 'porcelain:-0 '` (trailing space) → 0 hits on defect-bearing pristine bytes = **SURVIVED** statically; backstopped by M5 digest binding. |
| M3 | E3 registry section scoping (limb-c analog) | r36 `e3_registry_rows` | find `    /^## / { inreg = ($0 ~ /Gates & probes registry/); next }` + `    inreg && $0 ~ pat { n++ }` → replace with `    $0 ~ pat { n++ }` (file-wide count) | fixture with real row deleted + row-shaped line outside any `## ` section: pristine E3 1→0, mutant stays 1 | **KILLED PAIR** — fixture F3b: pristine `E3 payload=registry-r35-defect-closure=1,registry-r36-closure=0 closed=0` (`closed=8/9`); mutant `mut-e3scope` (sha `910fe47d5a7712a23168a761b102b4d5fdbefd797bd94a3ecf5ba2fde07801a1`) `E3 …=1 closed=1`, `closed=9/9 exit=0`. Section scoping is load-bearing. |
| M4 | E1 round-section boundary (limb-c analog) | r36 `e1_final_hashes` + `e1_has_round36` (2 sites) | find `Round[- ]?36([^0-9]|$)` → replace `Round[- ]?[0-9]+([^0-9]|$)` | fixture with ALL Round-36 headings renamed + bound `## Round 37 closure` block appended: pristine E1 1→0, mutant 0→1 | **KILLED PAIR** — Probe A pristine `E1 …round36-section=0… closed=0` (`closed=8/9`); Probe B `mut-anyround` (sha `7149ff6308297b815239fbe91ddde2dc9f71435c02595cac2d24ef28a9a33f50`) `E1 …section=1…bound=1 closed=1` (`closed=9/9`). |
| M5 | E10 digest binding (limb e) | r36 `suite_digest()` report header | no edit — equation check `printed suite-sha256 == sha256sum(executing bytes)` on pristine/fixed/mut-gateoff; receipt anchored to pristine digest vs mutated bytes | any one-byte suite mutation → planned E10 flips 1→0 | **KILLED (mechanism proven)** — MATCH ×3; a receipt carrying `suite-sha256=4db1ae70…` mismatches fixed bytes `b17935f4…` → E10 red. This is the backstop that catches E14-pattern-weakening and every other suite-byte mutant. |
| M6 | E1 placeholder limb (r36 bytes) | fixture SCORECARD | insert line `Evidence pending; filled by the L1 at closure.` after the anchor line | E1 closed 1→0 | **KILLED** — `E1 payload=placeholders=1,… closed=0`, `closed=8/9 exit=1`; reverted, tree restored. |
| M7 | E1 hash-binding limb (r36 bytes) | fixture SCORECARD | anchor hash `9c95148c…` → `f`×40 (unresolvable 40-hex) | E1 closed 1→0 (`bound=0`) | **KILLED** — `E1 payload=…,bound=0 closed=0`, `closed=8/9 exit=1`; reverted, tree restored. |
| M8 | E3 exact-basename presence limb (r36 bytes) | fixture SKILL.md | delete the single row `^\|\s*`?`r36-closure.sh``?\s*\|` | E3 closed 1→0 | **KILLED** — `E3 payload=…,registry-r36-closure=0 closed=0`, `closed=8/9 exit=1`; reverted, tree restored. |
| M9 | E8 stale-evidence limb (r36 bytes) | fixture `corpus/lessons/round-35.md` | append `The gate says source-recheck exit 0 on committed bytes.` | E8 closed 1→0 (`stale-line=1`) | **KILLED** — `E8 payload=…,stale-line=1,… closed=0`, `closed=8/9 exit=1`; reverted, tree restored. |
| B1 | E10 clause: digest header absent | planned-shape receipt fixture | delete line 1 `suite-sha256=…` | E10 1→0 | **KILLED** — `c1 header-absent` → `E10 closed=0`. |
| B2 | E10 clause: payload line trimmed away | receipt fixture | delete the `E7 payload=…` line | E10 1→0 | **KILLED** — `c3 payload-lines=13 want=14` → `closed=0`. |
| B3 | E10 clause: payload field emptied (line kept) | receipt fixture | `E7 payload=probe-field-7 closed=1` → `E7 payload= closed=1` | E10 1→0 | **SURVIVED under the naive clause** (`^E[0-9]+ payload=` still counts 14) — and also under a `payload=.+` "strengthening" (the tail ` closed=1` matches `.+`). **KILLED only by `payload=[^[:space:]]`** → `c7 nonempty-payload-lines=13` → `closed=0`. Coverage finding F3 below. |
| B4 | E10 clause: selftest case lines absent | receipt fixture | delete all 14 `selftest case=` lines | E10 1→0 | **KILLED** — `c5 selftest-case-lines=0 want=14` → `closed=0`. |
| B5 | E10 clause: selftest summary flipped | receipt fixture | `cases=14 failures=0` → `cases=14 failures=1` | E10 1→0 | **KILLED** — `c6 selftest-summary-absent` → `closed=0`. |
| B6 | E10 clause: digest mismatch | receipt fixture | header sha → `a`×64 | E10 1→0 | **KILLED** — `c2 digest-mismatch got=aaaa… want=b17935f4…` → `closed=0`. |
| T1 | E12 stale-label window (planned, exact vs weakened) | planned-shape detector (awk) | exact: window = last `^#{1,6} .*Round[- ]?37([^0-9]|$)` heading → next heading of ≤ level; weakened: last `Round[- ]?3[0-9]` heading → EOF | T1 (stale label inside round-37 section, clean round-38 after): exact 1→0; weakened stays 1 (miss) | exact `E12 closed=0 (stale label inside window lines 5-9)`; weakened `E12 closed=1 (window lines 10-12 clean)` — **miss confirmed (SURVIVED mutant class)**. |
| T2 | E12 boundary precision | same detectors | same | T2 (stale label only in round-38 section): exact stays 1 (no false positive) | exact `closed=1 (window lines 1-4 clean)` ✓; weakened `closed=0 (window lines 5-7)` — the drifted window **false-flags a legitimate future-round anchor line**. Boundary drift both misses and false-positives. |

## Key proof transcripts (trimmed)

```
# baseline (pristine, fixture F, clean env)
export-ref=0035ddb9… suite-sha256=4db1ae70…  deviation=non-default --lane  deviation=non-default --scratch-root
E1…E8 closed=1 … E9 payload=status-dirty=0,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present closed=1
closed=9/9 exit=0

# P1 pristine + poisoned status read  → defect live (D6)
E9 payload=status-dirty=0,… closed=1 / closed=9/9 exit=0        (status rc=128, swallowed)

# P2 fixed (planned E9 rewrite) + poison
E9 payload=status-dirty=read-failed closed=0 / closed=8/9 exit=1

# P3b gate-off + porcelain:-0 reintroduced + poison → flips back
E9 payload=status-dirty=0,… closed=1 / closed=9/9 exit=0
# P4 swallow reintroduced + poison → flips back
E9 payload=status-dirty=0,… closed=1 / closed=9/9 exit=0
# P5 fixed, clean env → happy path preserved
closed=9/9 exit=0

# E14 shape census (porcelain:-0, status-read 2>/dev/null)
pristine 1,1 · fixed 0,0 · mut-fallback 1,0 · mut-swallow 0,1 · mut-gateoff 1,0

# digest equation (limb e)
pristine MATCH · fixed MATCH · mut-gateoff MATCH  (printed suite-sha256 == sha256sum bytes)

# artifact mutants (pristine suite, fixture F)
M6 E1 placeholders=1 closed=0 · M7 E1 bound=0 closed=0 · M8 E3 registry-r36-closure=0 closed=0 · M9 E8 stale-line=1 closed=0  (each closed=8/9 exit=1)

# boundary probes
Probe C (no mutation): pristine E1 stays closed=1 with a bound hash under an appended `## Round 37 closure`
  heading while residual `### Round-36 move-log rows` exists above — scoping is heading-relative, not
  section-bounded (finding F4).
Probe A pristine: round36-section=0 → closed=8/9 · Probe B mut-anyround: section=1,bound=1 → closed=9/9

# E10 receipt clauses (planned-shape detector, fixture receipt)
control closed=1 · b1 c1 header-absent · b2 c3 13≠14 · b3 SURVIVED naive, killed by payload=[^[:space:]]
b4 c5 0≠14 · b5 c6 summary-absent · b6 c2 digest-mismatch

# E12 stale-label window (planned-shape detector)
T1 exact closed=0 (lines 5-9) · T1 weakened closed=1 (lines 10-12, MISSED)
T2 exact closed=1 (lines 1-4) · T2 weakened closed=0 (lines 5-7, FALSE FLAG)
```

## Findings (coverage, for the r37 suite author)

- **F1** — the r36 E9 fail-open is live in committed bytes: a failed `git status` read is reported as
  `status-dirty=0` and the suite still prints `closed=9/9 exit=0` (P1). The planned E9 rewrite kills it
  behaviorally (P2) and the planned E14 greps kill both reintroduction shapes statically (M2 census).
- **F2** — placement subtlety: under a fail-closed rc gate, a bare `porcelain=${porcelain:-0}` line is
  behaviorally dormant (P3 still red) but shape-detectable; the behaviorally-active reintroduction is
  gate removal (P3b). E14 must therefore keep **both** greps (`porcelain:-0` count AND status-read
  `2>/dev/null`/rc-swallow absence) — either alone leaves the other shape undetected.
- **F3** — the claim's E10 wording "fourteen `E<n> payload=` lines" is satisfiable with **empty payload
  fields** (B3 survived; even `payload=.+` survives because the ` closed=1` tail matches). The planned
  E10 must require `payload=[^[:space:]]` (non-empty first payload char), else a trimmed receipt passes.
- **F4** — E1's round-section scoping is heading-relative ("last matching heading"), so a bound hash
  appended under a later `## Round 37 closure` heading stays green as long as any residual Round-36
  heading exists above it (Probe C). The planned E12 stale-label check must extract the round-37
  section by **section boundaries** (heading level), not "last matching heading".
- **F5** — boundary drift cuts both ways (T1: miss; T2: false flag on a legitimate future-round anchor).
  The planned E12 needs the exact round-37 window; a `Round[- ]?3[0-9]`-class drift is detectably wrong
  in both directions.
- **F6** — digest binding (E10) is the meta-backstop: `printed suite-sha256 == sha256sum(executing
  bytes)` held on every copy tested, so ANY one-byte suite mutation (including E14-pattern weakening,
  M2's survived static case) flips a receipt-anchored E10. The r37 receipt must be written against the
  final suite bytes and E10 must re-verify the equation at gate time.

## Restoration evidence

- Pristine scratch copy sha256 before/after all runs: `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` (unchanged; equals lane file at start and end).
- Lane HEAD unchanged throughout: `b362068195d5489aa94b31e6ec8f880c367e0ba0`; no lane write by this seat (receipt below is the only one).
- Lane `git status --porcelain` at seat start: 6 untracked round-37 wave paths (`assimilation/`, `wave1-plan.err`, `wave1-run.err`, `wave1.ready`, `wave1.ready.partial`, `wave1/`). At receipt time: same set plus sibling churn not caused by this seat — ` M .ufo/waves/round-36/wave1/ScribeConsiderthese.md` (modified by its own seat) and `wave1.ready.dispatched` (replaced `wave1.ready.partial`). Porcelain hash at receipt time `6b8e9457e326202e102c2356595e3fd9bd86fbbe954f89c01a3582eb18fb995c`.
- Fixture F: every mutant was reverted in-fixture; final tree `cdd445b4b4537e814f1c5b26172008cecdd7b6bb` equals the baseline tree; `git status --porcelain` in F = 0 lines.
- Mutant copy sha256s (all under scratch, all removed with it): fixed `b17935f430bda6e1eb01c74f0a015cb19c6ebc2486698a5bd3c1a18d7bad9b45`, mut-fallback `9fd852ab049304a7c4c21e38377ed7f84ef716337c3017ce32e6b49524771e7b`, mut-swallow `09d5be5f9c0af1b7b20f0ee2f364bc41015d695f0abae4b198f6e20599eb7e55`, mut-gateoff `19f1e142b5450045c66218015508fc8d1e127f349c7f58e96e06d8d50bb40cce`, mut-e1sec `b75ecd092a194fb0247cf1ff09b26a25ad28de7ff750656178bb6060543abf29` (superseded by mut-anyround `7149ff6308297b815239fbe91ddde2dc9f71435c02595cac2d24ef28a9a33f50`), mut-e3scope `910fe47d5a7712a23168a761b102b4d5fdbefd797bd94a3ecf5ba2fde07801a1`.
- Fixture anchors: H1 `9c95148c2a989bfc666facfa9c06aa353acf8e98` (named by the re-anchored SCORECARD line), H2 `0035ddb96d7e2da0466dceb72df227d1add1d7be` (export ref = fixture HEAD).

## Limits

- The planned r37 suite does not exist in bytes yet (before-control `suite_missing=1`; absent from every
  tree at HEAD), so E10/E12/E14 rows are proven against planned-shape detectors and r36 analogs, not
  against the r37 bytes themselves. Once the suite lands, the table's find/replace strings apply
  verbatim as the regression probes.
- Full-suite runs against the REAL lane are environmentally red on E9 mid-wave (sibling receipts make
  the worktree dirty), so all suite runs used the fixture lane; the real-lane required reds (r36 base /
  judged-head exports) belong to the ExecC1BaseFail / ExecC1JudgedHeadFail seats and were not re-run here.
- No tools installed or upgraded (bash, coreutils, awk, grep, python3, git only); pacman untouched.
- Scratch dir `/fast/scratch/hyaku/kasegi-r37/MutC1Suite/` removed after this receipt was written.
