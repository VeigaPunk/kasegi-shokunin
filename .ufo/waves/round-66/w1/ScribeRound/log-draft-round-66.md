# DRAFT — LOG.md append (scribe draft for the L1 integrator)

> **STATUS: SUPPLEMENT, not a replacement.** The L1 landed a nine-bullet round-66 LOG
> section while this seat worked. **Do not write this draft as a file.** It is the
> scribe's independent record; the increments the L1 may still want are the **quantified**
> size-gating with its mechanism and the flaky band, the **`--` separator operand-count**
> edge case, the **host-specificity** of the threshold, and the scribe's **independent
> base-vs-landed verification**. Where the landed LOG already carries the substance (the
> six r65 corrections, the S099 curation), this draft is the scribe's independent
> verification of it against committed bytes and is retained for the audit trail.

**Draft only. Not in production.** Numeric values that depend on a candidate run are
written as `not yet measured`. The bullet wording follows the file's own convention (`- `
bullets under a `## Round NN (YYYY-MM-DD) — …` heading), and — per the r65 verifier's
routed defect 1 — bullets are cited by **index**, never as "bolts".

---

## Round 66 (2026-11-04) — cat SIGPIPE masking, predata construction (scribe draft, continued)

- The base false green is reproduced on the **public path** by the scribe independently of
  the L1's own receipt: from a scratch clone of the lane at base
  `b6db9e818d322726e39cb441f2179d34d4170275`, the committed production gate
  (`corpus/instruments/figure-audit.py`, sha256 `86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef`)
  run against a 4 MiB first operand and a deliberately absent second operand prints
  `FIG miss-head recorded=alpha derived=alpha ok`,
  `FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0`, rc 0. The native stages behind that green
  are `cat` killed by SIGPIPE (-13) and `head` exit 0 with **empty stderr** — the missing
  operand is never diagnosed, while the untruncated run reports
  `cat: missing.txt: No such file or directory` and exit 1. Receipts
  `.ufo/waves/round-66/w1/ScribeRound/receipts/base-false-green-r66.txt` and
  `.../native-statuses-r66.txt`.
- **The false green is size-gated and its edge is a race.** Measured 100 repetitions per
  first-operand size with stderr categorised: 393 216 B and 520 000 B → the base already
  reads stale in 100/100 (no false green to detect); 524 288 B → 95/100 false green;
  528 000 B → 90/100; 540 000 B and above, including 1 MiB and 4 MiB → 100/100 false green.
  Mechanism, traced: `cat` moves the file into the pipe with `splice()` in 512 KiB chunks,
  `head` reads one 8 192-byte chunk and exits, and the next `splice` returns `EPIPE`.
  Consequence for the counter: a short fixture is **vacuous** for this class (the base is
  already stale, so an unmodified gate passes it), a fixture inside the 512-528 KiB band is
  **flaky**, and the threshold is host-specific, so the counter asserts the **native stage
  status** rather than a size threshold. Receipt
  `.../ScribeRound/receipts/threshold-band-r66.txt`.
- Operand counting follows the **decoded argv**, not the raw string: a `--` separator is not
  an operand and a second `--` is. Measured `cat -- -- missing.txt | head -n 1` with a 4 MiB
  file literally named `--` → 30/30 false green at base, so the operand count there is two,
  not one. A conservative refusal for option-bearing forms is a legitimate reading and
  must be named in the claim if adopted, not silently applied.
- **Correction, append-only, of the six defects the round-65 verifier routed to the lane.**
  The filed round-65 report is not rewritten and no round-65 number is restated as if it
  had been re-measured. (1) The Landed-changes table's commit→LOG ties said "LOG bolts
  1–12"; `LOG.md`'s Round 65 section has **10 bullets** and the string `bolt` appears
  **nowhere** in `LOG.md` — bullet indices are cited instead. (2) Two round commits were
  missing from that table (`git rev-list --count a283189…a3357329` = 15, table named 13):
  **`1929a47`** (widen the S098 body range, M65-9) and **`6824522`** (re-record the
  final-tip receipt) — both exist in the lane and are ancestors of the tip. (3) The "exact
  final driver" label was wrong for the receipt it cited: the before-block's
  `controls/driver-base-donothing-finaldrv-r65.txt` records the erratum-1 driver
  **`5aa842ab…`**, whereas the same-result base receipt from the final driver is
  `controls/driver-base-donothing-r65.txt`, driver sha256 **`7f27c4d2…`**, 8/3, with
  `GUARD driver-self-pin PASS` — that one is cited. (4) "Final tip" was not the lane tip:
  the tip receipt names revision **`03a23921`** while the lane tip is `a3357329`, two
  receipt-only commits later (`6824522`, `a3357329`; `git diff 03a23921 a3357329` touches
  only three receipt files) — the revision is named as measured and the delta is stated.
  (5) The base receipts record **no exit code**: `controls/driver-base-donothing*.txt` end
  at `VERIFY measurements=8 failures=3 revision=a283189…` with no line recording the
  **driver's own** exit status (the sub-result `exit=` values that are present are cited
  as such; the candidate receipt `controls/final-verification-tip-r65.txt` does end with a
  bare `exit=0`), so the filed report's "exit 1" was never captured; it is **not invented
  here**, the round-65
  receipts are described as recording the driver's own exit code as absent, and every
  round-66 receipt captures the exit status of its run. (6) The helper-count phrasing: the
  sentinel receipt records
  `marker lines=121900 (two gate runs appended; ~60950 program invocations per run)`, so
  the figure is **121 900 across two runs**, ~60 950 per run, not one run.
- Source curation: S099 admitted as own-work/A, opened 2026-11-04, scoped only to this
  lane's local cat-SIGPIPE exemption and the later-input masking case. Located quote (4
  words by `wc -w`, 2026-11-04): `return status != -signal.SIGPIPE` at L91 of
  `corpus/instruments/figure-audit.py` at base `b6db9e8…` (sha256 `86becbde…`), inside
  `upstream_stale` L83-L94, whose call site L129-L131 passes only `argv[0]` and therefore
  cannot see how many operands `cat` was given. Receipt
  `.../ScribeRound/receipts/gate-quote-r66.txt`. Assimilation: none — no
  `merge/kasegi/MERGE-REPORT.md` is present on this host, and `considerthese` proposal 2
  remains domain-task-open.
- Calibration: the round-66 lesson records M66-1 (an exemption's masking probe needs a
  fixture that reaches the masking) and M66-2 (a status label is not the error it hides).
  **No new QUALITY criterion is added**: R88 already states the governing rule ("an
  exemption class in a gate is probed for the error it can mask … and the probe set carries
  at least one control where that status hides a real failure") and R88's check is what the
  r66 probe set implements; the size-gating finding is a counter-design constraint and a
  residual, not a portable rule.
- Coverage 8 and density 9 are held, not re-measured. S099 is own-work curation, not new
  domain ground. The gate is not pipefail, not a sandbox and not an authenticity check;
  grandchildren, shell wrappers, PATH-shadowed binaries and exit-0 wrappers printing
  partial output remain out of scope, and the r65 seat-emulator finding (M65-5) stands.
- **No SHONEN box 2 credit.** Box 2 (end-to-end domain task) stays `[ ]`: no authorized
  end-to-end domain task was executed and the documentation-only claim does not close
  `considerthese` proposal 2. Boxes 1, 3 and 4 are as in round 65; promotion is
  operator-owned and no box was marked here.
