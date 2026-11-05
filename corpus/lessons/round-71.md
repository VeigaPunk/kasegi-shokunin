# Round 71 — the per-script python-head census (C1) and frontier F49 on S106, the TrendAI ZDI disclosure process (C2)

Round 71, attempt 1. Lane base `4e33119e0167cac3fbfa15afb3f2f5b98a43cc60`; frozen claims
`0e260a54b0a670cee2915237ac403d37164c749d` (`.ufo/waves/round-71/claims.json`, pins
`.ufo/waves/round-71/controls/pins-r71.txt`).

- **C1, depth:verifiability (4)** — the derive gate replaces the round-70 global python deny list with a
  per-script census: `PY_DENIED_ANY` (`--out`, `--output`, `--selftest`), `PY_HEAD_REFUSED`
  (`frontier-recheck-count.py`), `PY_DENIED_BY_SCRIPT` (per-script `--root`/`--json`/`--url`/`--work`/
  `--scratch`), and `PY_SCRIPT_CENSUS`, an allowlist that refuses a head it does not name. Gate
  `corpus/instruments/figure-audit.py` sha256
  `182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603`, selftest 106 cases / 0 failures.
- **C2, coverage (8)** — frontier F49 on S106, TrendAI Zero Day Initiative's own About page: its
  disclosure process and vendor-coordination statements (120-day standard window; 30/60/90-day shortening
  for incomplete or problematic patches; escalation after 15 business days of vendor silence; full
  advisory after a patch versus a limited advisory when no fix arrives; validate → formal monetary offer
  → payment → vendor coordination; credit or anonymity). Capture
  `corpus/source-snapshots/round-71/S106.txt` sha256
  `291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db` (148 lines, 15004 bytes) with a
  15-quote `manifest.json`.

## C1 - measured result

Three control VERIFY lines, from the committed receipts in `.ufo/waves/round-71/controls/`; the control
hashes equal the pin lines of `controls/pins-r71.txt`, checked against the committed blobs:

```
VERIFY measurements=25 failures=13 gate_sha256=7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5 mode=donothing   # controls/c1-donothing-r71.txt
VERIFY measurements=25 failures=14 gate_sha256=c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde mode=base         # controls/c1-base-r71.txt
VERIFY measurements=25 failures=0  gate_sha256=182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603 mode=candidate    # controls/c1-candidate-trial-r71.txt
```

Re-run by this seat on a `git clone --shared` checkout of `4e33119` (R106: a clone with an object store,
never a `git archive` export), scratch `/fast/scratch/hyaku/kasegi-r71/ScribeLesson/`:

```
candidate exit=0 : VERIFY measurements=25 failures=0  gate_sha256=182f4ef7… mode=candidate
donothing exit=1 : VERIFY measurements=25 failures=13 gate_sha256=7a8d52eb… mode=donothing
base     exit=1 : VERIFY measurements=25 failures=14 gate_sha256=c09b0fb1… mode=base
forgery  exit=1 : VERIFY measurements=25 failures=12 gate_sha256=126de75d… mode=forgery
```

The blanket-refusal forgery line is not a committed round-71 receipt; it is this seat's own control, run
against the committed round-70 forgery gate `.ufo/waves/round-70/controls/forgery-blanket-refusal-gate-r70.py`
(sha256 `126de75d…`): all eight read-only positives R1–R8 refused (`controls=8 failed=8`), `selftest
cases=86 failures=47`, exit 1.

Direction-by-direction reading of the three committed receipts (each `MEASURE` line quoted from them):

| limb | base (r69 `c09b0fb1`) | do-nothing (r70 `7a8d52eb`) | candidate (`182f4ef7`) |
|---|---|---|---|
| N1–N3 `--root` space/equals/abbrev | FAIL, `refused=0`, `marker_runs=1` | ok, `refused=1` | ok, `refused=1` |
| N4–N6 `--out` space/equals/abbrev | FAIL, `wrote=1` | ok, `wrote=0` | ok, `wrote=0` |
| N7 `--json` | FAIL, `refused=0`, `marker_runs=1`, `wrote=1` | ok | ok |
| N8 no-option head | FAIL, `marker_runs=1` | FAIL, `marker_runs=1` | ok, `refused=1` |
| N9 `--selftest` | FAIL | FAIL | ok, `refused=1` |
| N10 short `-o` | FAIL | ok | ok |
| N11 `--output` | FAIL | ok | ok |
| N12 head absent from the census | FAIL | FAIL | ok, `refused=1` |
| R1–R8 read-only positives | 8/8 admitted and exact | 8/8 **refused** (`admitted=0`) | 8/8 admitted and exact |
| selftest | 86 cases | 96 cases | **106 cases**, `failures=0` |
| mutbat | 5/5 killed | 5/5 killed | 5/5 killed |
| real ledger | `figures=35 ok=35 stale=0` | `figures=35 ok=35 stale=0` | `figures=35 ok=35 stale=0` |
| no-write-side-effect | FAIL, `marker_runs=5` | FAIL, `marker_runs=1` | ok, `marker_runs=0` |

The round-70 defect is visible in the middle column: the r70 gate refuses **all eight** R1–R8 read-only
derives (`admitted=0` in every row), which the r69 base gate admits and re-derives exactly —
`PY_DENIED_FLAGS` was one global name list, so `--root` (a read-only lane pointer on six instruments) and
`--json` (stdout-only in `claim-package-check.py:791`) were refused everywhere while the exec class
stayed reachable with **no option at all** (N8: `python3 corpus/instruments/frontier-recheck-count.py`,
`marker_runs=1`).

One-limb mutation audit of the new census (this seat's own mutants, one edit each of the committed gate
bytes, selftest run per mutant; R103 = one-limb-killed). Killed (`cases=106 failures=1` each): census
fail-closed check removed → `python-unknown-head-refused`; `PY_HEAD_REFUSED` entry removed →
`python-no-option-head-refused`; `PY_DENIED_ANY --selftest` removed → `python-selftest-refused`;
`PY_DENIED_ANY --output` removed → `python-output-long-refused`; `capture-source.py --url` removed →
`python-url-refused`; short `-o` arm removed → `python-short-o-refused`; `capture-source.py` deleted from
`PY_SCRIPT_CENSUS` → `python-census-covers-instruments`; a new instrument file absent from the census →
`python-census-covers-instruments`; and **the global deny list restored** (every script also denied
`--root`, `--json`) → `python-per-script-root-admitted`. That last one is the one that matters for this
round: the r70 shape (one list applied to every head) is killed by the r71 selftest, so the r70
over-refusal cannot silently return.

Two mutants are not killed. `PY_DENIED_ANY --out` removed → `cases=106 failures=0`, because the
`--output` entry's prefix coverage still refuses `--out` (equivalent mutant; the r70 `MutationC1`
`M1-out` finding repeats). And eight per-script denial entries have **no** one-limb-killed case: the
mutant's selftest stays `cases=106 failures=0` while the mutant is behaviour-changing — pristine gate
`rc=2 refused=1`, mutant gate `rc=1 refused=0` — for `citation-ground-check.py --json`,
`gate-quote-audit.py --json`, `mirror-containment-check.py --json`,
`resolve-dispatch-check.py --json`, `limb-mutation-check.py --root`, `r46-c1-gate.py --root`,
`capture-source.py --work`, `capture-source.py --scratch`. Two of these
(`citation-ground-check.py --json`, `limb-mutation-check.py --root`) also pass the frozen round-71
counter unchanged (`VERIFY measurements=25 failures=0` on the mutant gate), so neither the selftest nor
the committed probe set pins them.

## C2 - measured result

Counter table; the "before" column is the committed receipt
`.ufo/waves/round-71/controls/c2-base-counters-r71.txt` (measured at the round-70 base `39cde8a`), the
"after" column is re-measured by this seat on clones of the tips `453275f` and `34faab9` (identical
values at both):

| counter | before (`controls/c2-base-counters-r71.txt`) | after (measured at `453275f`/`34faab9`) |
|---|---|---|
| `FRONTIER-CENSUS` | `rows=48 admitted=48 registry=105` | `rows=49 admitted=49 closed=49 problem-rows=0 registry=106` |
| frontier entries | `entries=51 pass=51 exit=0` | `entries=52 pass=52 exit=0` |
| `capture-binding-check` | `records=84 bound=84 unbound=0` | `records=85 bound=85 unbound=0` (exit 0) |
| knowledge-expected lines / entries / sort | 88 / 86, exit 0 | 89 / 87, `LC_ALL=C sort -c` exit 0 |
| knowledge files / frontier rows / registry rows | 86 / 48 / 105 | 87 / 49 / 106 |
| `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit 0 | exit 0, six inherited W04 warnings |

Re-measured before values at base `39cde8a` (clone) agree with the committed receipt: `FRONTIER-CENSUS
rows=48 admitted=48 registry=105`, `entries=51 pass=51`, `records=84 bound=84 unbound=0` (capture exit 0),
knowledge-expected 88 lines / 86 entries, 86 knowledge files, 48 frontier rows, 105 registry rows.

S106 quote anchors, re-derived from the committed capture and manifest (all 15 manifest quotes are exact
substrings of the line their anchor names; `wc -w` on the quoted text, R56):

```
Q01-scope anchor= 28 wc_w= 7   Q02-acquisition anchor= 31 wc_w=13   Q03-guarantee anchor= 47 wc_w=19
Q04-validation anchor= 49 wc_w= 5   Q05-window anchor= 70 wc_w=15   Q06-shortened anchor= 70 wc_w=15
Q07-escalation anchor= 70 wc_w=25   Q08-limited anchor= 52 wc_w=19   Q09-full anchor= 51 wc_w=12
Q10-offer anchor= 60 wc_w=19   Q11-nobacklog anchor= 62 wc_w=19   Q12-credit anchor= 61 wc_w=16
Q13-dossier anchor= 69 wc_w=19   Q14-refusal anchor= 72 wc_w=18   Q15-nolimit anchor= 60 wc_w=13
```

## Gate

| row | URL | access date | located quote (≤25 words) |
|---|---|---|---|
| S106 (admitted, tier A, mined) | https://www.zerodayinitiative.com/about/ | 2026-11-05 (capture fetched 2026-11-05T01:27:03Z, HTTP 200; capture sha256 `291f36c2…cf59db`, 148 lines) | "Vendors are given a standard coordination window of 120 days under TrendAI™ ZDI's disclosure policy." (`S106.txt:70`, 15 words by `wc -w`) |
| rejected row this round | — | — | **No source was rejected this round.** The round opened exactly one candidate source (S106) and admitted it, so the registry moves 105 → 106 by one admitted row and no `rejected` row is owed (R102's arithmetic: before + admitted + rejected = 105 + 1 + 0 = 106, which the measured `registry=106` matches). No candidate was opened and refused, so R64's rejected-row rule has nothing to record; the rejected row S104 (ENISA EUVD, tier C) is carried unchanged from round 70 and is not re-opened here. |

## Mistakes

- **M71-1 — a global deny list applied where the flags are per-script.** The round-70 gate denied one
  name list (`--root`, `--out`, `--output`, `--json`, `--scratch`, `--url`, `--work`) to *every* python
  head, although `--root` is a read-only lane pointer on six instruments and `--json` is a stdout-only
  flag in `claim-package-check.py:791`; the frozen positive controls happened to spell none of the seven
  denied names, so `measurements=12 failures=0` was a property of the control set, not of the gate. The
  defect was caught only by an adversarial seat — `CriticC1`, `.ufo/waves/round-70/w1/CriticC1.md` —
  **after** the round-70 claim had already been frozen, and the round-70 lesson recorded it as "C1 is
  therefore NOT VERIFIED as declared", routing the correction as V70-5/V70-6 instead of repairing it in
  place. Captured-by: **none** before this round — the class was found by an adversarial seat, not by a
  criterion, so under R36 it earns a criterion row this round. The criteria that now carry it are
  **R103** (every refusal rule carries a selftest case that fails when that rule — or its scope — alone is
  removed; the r70 global shape is killed this round by `python-per-script-root-admitted`) and **R110**
  (the round ends only on a quiescent lane — measured now: `git status --porcelain` prints
  ` M corpus/SOURCES.md` at tip `453275f`, and after that bullet's commit `34faab9` only this lesson and
  this seat's report remain untracked, so R110 is satisfied only once the round's own artifacts are
  committed). Fix landed in r71:
  `PY_DENIED_BY_SCRIPT` per script, `PY_DENIED_ANY`, `PY_HEAD_REFUSED` and the fail-closed
  `PY_SCRIPT_CENSUS` allowlist in `corpus/instruments/figure-audit.py` (sha256 `182f4ef7…`), with ten
  new selftest cases and the `python-census-covers-instruments` completeness case.

## Routed defects

- **V71-1 — eight per-script denial entries are load-bearing but unpinned (R103).** The eight entries
  listed in the C1 section each change the gate's verdict when removed, yet no selftest case fails
  without them, and two of them (`citation-ground-check.py --json`, `limb-mutation-check.py --root`) also
  pass the frozen round-71 counter unchanged (`VERIFY measurements=25 failures=0`). Fix: one dedicated
  selftest case per entry, naming the script and the flag, so the R103 mutant set is killed by the
  selftest and not only by a mutation seat.
- **V71-2 — the `--out` / `--output` pair is one rule, not two.** Removing `--out` from `PY_DENIED_ANY`
  leaves the selftest green (`cases=106 failures=0`) because the `--output` entry's prefix coverage
  already refuses `--out`; the r70 `MutationC1` finding (`M1-out` equivalent) repeats. Fix: treat the
  pair as one rule in the mutation battery and say so in the gate's docstring, or split the entry so the
  `--out` limb has its own case.
- **V71-3 — the `frontier-recheck-count.py --json` entry is inert.** With `PY_HEAD_REFUSED` naming that
  head, removing its `--json` entry leaves the gate refusing the derive anyway (`rc=2 refused=1` before
  and after). Fix: drop the redundant entry or note that the head refusal covers it, so the census does
  not carry a rule no probe can distinguish.

## Residuals

- The claim is the enumerated probe set N1–N12 and R1–R8 on this host's PATH `python3` 3.14.8, GNU
  `sort` 9.12 and `git` 2.56.0 (the `HOST` line of each committed receipt). It is an enumerated option
  set plus a per-script census, **not** a sandbox.
- Positional arguments stay admitted: `python3 corpus/instruments/claim-package-check.py
  corpus/instruments/fixtures/claim-package/exemplar` is admitted (`rc=1 refused=0`), and `python3
  corpus/instruments/resolve.py .` is admitted and runs long (the probe timed out at 90 s without a
  refusal).
- Non-denied counter options stay admitted: `--results`, `--manifest`, `--fleet-root` all measured
  `rc=1 refused=0`. Operand forms stay admitted by construction: `python3 corpus/instruments/ok.py --
  --root` is admitted (`rc=1 refused=0`), and `python3 corpus/instruments/capture-source.py -- --out x` is
  admitted while `python3 corpus/instruments/capture-source.py --out x --` (denied flag *before* the
  separator) is refused (`rc=2 refused=1`).
- A relative head path that resolves back into the instrument directory is admitted
  (`corpus/instruments/../instruments/capture-binding-check.py` → `rc=1 refused=0`), while a path outside
  the directory is refused (`python3 ../ok.py` and `python3 /tmp/x/ok.py` → `rc=2 refused=1`).
- Spelled variants of the denied names are refused: `--url=file:///dev/null`, `'--url'
  file:///dev/null` and the bundled short `-ox.txt` all measured `rc=2 refused=1`; a head absent from the
  census is refused (`corpus/instruments/zzz.py` → `rc=2 refused=1`).
- Nested python, a counter's own writes on a positional path, `sort -T`/`TMPDIR` temp writes, environment
  variables, host-file reads and SIGPIPE masking stay open from rounds 67–70. On the C2 side,
  `capture-binding-check.py` at the capture commit `4e33119` alone prints `FAIL rule=no-row record=S106
  dir=round-71` and `records=85 bound=84 unbound=1` (exit 1) because the S106 registry row lands later in
  the same round; at tips `453275f`/`34faab9` it reads `records=85 bound=85 unbound=0` (exit 0).
