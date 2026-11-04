# ExecCatDriver — round-66 C1 committed-input driver (proposed, not frozen)

Seat: ExecCatDriver (executor, leaf). Base `b6db9e818d322726e39cb441f2179d34d4170275`; controls
commit observed `1957407e22331c73aafe944da2b37c182f13583a` (round-66 start). Scope: one file,
`.ufo/waves/round-66/w1/ExecCatDriver/verify.py`, plus this report. No production, fleet, sibling,
git-index or commit writes. No subagents. No pins frozen.

## What was built

`verify.py --revision REV --controls-revision CREV --work DIR [--candidate PATH | --final]
[--cat-mutbat REL] [--base-rev REV] [--source-repo PATH] [--pins-path REL] [--probes-path REL]
[--timeout SEC] [--print-inputs]`

- Controls (probe battery, pin manifest, optional cat-limb battery) are read as bytes with
  `git show CREV:path`. The worktree is never a control source.
- Measured tree: one scratch shared clone (`git clone --shared --no-checkout` from the source), checked
  out at the full REV with `checkout -f --detach` and `clean -q -f -d -x`. HEAD is asserted.
- Paired base gate: `git show BASE:corpus/instruments/figure-audit.py`, bytes saved, digest pinned.
- `--candidate` overlays the measured gate for a trial only. Its digest is recorded and labelled
  unpinned. `--final` refuses `--candidate`, requires `--cat-mutbat`, and requires source = lane.
- Work path must sit under `/fast/scratch/hyaku/kasegi-r66/` and outside the lane.
- Children run in their own session and are killed as a process group on timeout (r65 killed only the
  parent). Each child writes a receipt with its argv, cwd, input sha256s, combined output and `[exit=N]`
  (r65 base receipts had no exit line; defect fixed). `receipts/index.json` lists every receipt digest.
- Integer and exact-line checks replace r65's substring and string-compare checks (r65 compared
  `m.group(6) >= "1"` as strings and used substring `check_lines`). Pins are required; an empty pin set
  no longer passes vacuously (r65 `if not pins: bad = []`).
- Revision is named by full sha in every output line (r65 spotcheck defect 4 concerned the tip vs measured
  revision; the driver prints the measured revision only).

## Measurements (11 default, 12 with `--cat-mutbat`)

Printed in this order as `RESULT <name> PASS|FAIL <note>`, then `VERIFY measurements=N failures=F
revision=REV mode=...`:

1. `driver-self-pin`: running digest == manifest `driver_sha256`; final also requires the driver committed at CREV.
2. `controls-pins`: every manifest `controls` entry, including the probe battery, matches committed bytes at CREV.
3. `ledger-closure`: committed inputs each ledger derive reads, resolved by object id (`commit:path`),
   written to `receipts/closure.tsv`. Unresolved `REV:PATH` tokens fail. Pinned against
   `measured.closure_sha256`, `closure_entries`, `ledger_sha256` when `measured.revision == REV`.
4. `probes-base-paired`: `probes.py --mode base` on the BASE gate bytes.
5. `probes-measured`: `probes.py --mode candidate` on the measured gate.
6. `shape-identity`: the driver runs the measured gate itself on driver-owned single-figure ledgers
   for the eight shapes (P1–P8, fixtures `big`/`small` built under work), under two figure-ID spellings
   (probe ID and a held-out ID). It requires the same rc, verdict and reason across spellings, equal to the
   driver's expectation table, and derived=want on ok lines. Native stage0 premise is checked with
   `subprocess` pipelines (no shell).
7. `selftest`: `gate --selftest` exit 0 with `selftest cases=<pin> failures=0`.
8. `mutbat-existing`: `corpus/instruments/figure-audit-mutbat.py --instrument GATE` exact summary line from pins.
9. `real-ledger`: `gate --ledger corpus/instruments/figure-audit-ledger.json --root .` exact
   `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0` from pins.
10. `red-wrong-want`: driver-built fixture, one wrong-want red (rc 1) and one right-want control (ok).
11. `cat-mutbat` (only with `--cat-mutbat REL`): the L1 cat battery read from CREV, pinned in `controls`,
    run as `--instrument GATE --collector PROBES --work DIR`, exact line `expected.<kind>.cat_mutbat_summary`
    (L1 reports `CAT-MUTBAT killed=3/3 survivors=0 equivalents_held=1 invalid_rejected=1 failures=0`).
12. `identity-guards` (always last): HEAD == REV; tree status unchanged by the run; dirty set equals
    the candidate path only in candidate mode; gate bytes == committed bytes at REV in non-candidate modes;
    base digest == `base_gate_sha256`; `measured.gate_sha256` == tree gate when pinned for REV; final requires
    `measured.revision == REV`; the controls revision must descend from REV (`merge-base --is-ancestor`).

Exit: 0 all pass, 1 any FAIL, 2 setup (`VERIFY-SETUP reason=...`, no verdict).

## Manifest schema the driver expects (`controls/driver-pins.json` at CREV, L1 to set)

```
{ "base": "<BASE full sha>",
  "base_gate_sha256": "<sha of gate at BASE>",
  "driver_sha256": "<sha of verify.py>",
  "controls": { "<probes path>": "<sha>", "<cat-mutbat path if used>": "<sha>" },
  "measured": { "revision": "<REV>", "gate_sha256": "<committed gate at REV>",
                "ledger_sha256": "...", "closure_sha256": "...", "closure_entries": N },
  "expected": { "ledger_summary": "FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0",
                "base":      { "selftest_cases": N, "mutbat_summary": "..." },
                "candidate": { "selftest_cases": N, "mutbat_summary": "...", "cat_mutbat_summary": "..." } } }
```

`--print-inputs` prints the digests (driver, controls, base, measured gate, ledger, mutbat, closure) as JSON
for constructing that manifest without writing it.

## Construction evidence (what was actually run)

Tool versions: Python 3.14.8, git 2.56.0. No install performed (no pacman, uv or npm used).

```
python3 -c "ast.parse(verify.py)"                                           -> syntax ok, rc 0
python3 -B verify.py --revision b6db9e8 --controls-revision 1957407 --work <scratch>/work-nopins --cat-mutbat x
    -> VERIFY-SETUP reason=pin manifest .ufo/waves/round-66/controls/driver-pins.json absent at controls revision 1957407e..., rc 2
python3 -B verify.py ... --work /tmp/x                                       -> VERIFY-SETUP work outside scratch, rc 2
python3 -B verify.py ... --final (no --cat-mutbat)                           -> VERIFY-SETUP --final requires --cat-mutbat, rc 2
python3 -B verify.py ... --final --candidate /etc/hostname --cat-mutbat a.py -> VERIFY-SETUP --final refuses --candidate, rc 2
```

Base facts observed (read-only, lane, not driver output): base gate `86becbde…`, `EXPECTED_CASES = 63`,
ledger 35 figures, `figure-audit-mutbat.py` 5 mutants; base is the r65-landed gate, so the SIGPIPE
exemption is present at base.

NOT done: no end-to-end measurement run. Reason: no committed controls revision with a pin manifest exists
yet (L1 owns pins), probes.py and the cat battery are still being revised by ExecCatProbes/CriticCat, and
freezing pins now would freeze the attacked collector (CriticC ID-oracle, collector 1d28ca24). Expected
values in `expected` must come from a base trial and the final candidate, not from this report.

## Attacks and what the driver does about them

- CriticCat ID-keyed no-work oracle (passes the collector 8/0 at 1d28ca24): the collector alone is not
  authority. `shape-identity` runs the gate itself under two IDs and fails spelling-dependent verdicts.
  The held-out-ID rename of P1 (CriticCat identity-counter) would flip `probes-measured` and
  `shape-identity` for an ID-keyed oracle.
- A text-keyed oracle that answers correctly for the eight driver shapes is NOT caught by
  `shape-identity`. It is caught by identity in final mode (`gate-not-committed-bytes`,
  `measured-gate-pin`) and by `cat-mutbat` / `selftest` / `mutbat-existing` only if they fail it.
  In candidate mode the candidate is unpinned by design and must not be read as a claim.
- No broad sandbox claim: the driver executes the gate, selftest and batteries; the gate is not confined.

## Residual defects / open items

1. `shape-identity` uses driver-owned derives identical in text to probes; a derive-text-keyed oracle is only
   defeated by the pinned gate bytes, not by the driver's own behavioural check. Recommend a held-out derive
   variant (e.g. `cat big.txt missing.txt | head -n 2`) in the final battery, to be coordinated with CriticCat.
2. `ledger-closure` is a heuristic token enumeration over shlex tokens; it is complete only for the tokens the
   gate actually reads for this ledger. The gate's own run is the ground truth; closure is a pin, not a proof.
3. Expected values (selftest case count, mutbat and cat summaries) are pinned from measured runs, so the
   pin itself is only as good as the base trial that produced it. Must be labelled as such in the claim.
4. `shape-identity` runs 16 gate invocations on 4 MiB fixtures; runtime not measured here.
5. No `--json` output; `RESULT` lines are the only machine surface, matching r65.
6. Measurement count is 11, or 12 with `--cat-mutbat`; the docstring states both.

## Suggested checks for the main agent after pins are set (not run by this seat)

```
python3 -B .../verify.py --revision <BASE> --controls-revision <CREV> --work /fast/scratch/hyaku/kasegi-r66/L1/base-trial --cat-mutbat <REL>
python3 -B .../verify.py --revision <BASE> --controls-revision <CREV> --work .../base-do-nothing --candidate <base gate copy> --cat-mutbat <REL>
python3 -B .../verify.py --revision <REV> --controls-revision <CREV> --work .../final --final --cat-mutbat <REL>
```
Expected: base trial fails `probes-measured`, `shape-identity` and `cat-mutbat` (predicate and cat limb), all
other measurements pass; final passes all 12. Forged-control trial: change one `controls` digest in a fixture
manifest and expect `controls-pins` FAIL.

## Scratch

`/fast/scratch/hyaku/kasegi-r66/ExecCatDriver` holds no durable receipts (construction checks failed before
any work directory was created). Removed before yield.
