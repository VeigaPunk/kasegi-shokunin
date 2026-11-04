# DRAFT — corpus/lessons/round-66.md (append-only, scribe draft)

> **STATUS: SUPPLEMENT, not a replacement.** While this seat worked, the L1 landed
> `corpus/lessons/round-66.md` (and the round-66 LOG section, the S099 registry row, the
> frozen `.ufo/waves/round-66/claims.json`, and the implementation commit `e8a865d`).
> **This draft is therefore NOT a file to write.** It is the scribe's independent record
> and the source of the *append-only increments* the L1 may still land:
> - the **quantified** size-gating and the mixed/flaky band (the landed M66-2 names the
>   vacuous-short-fixture class but not the numbers or the mechanism);
> - the **`--` separator operand-count** edge case;
> - the **host-specificity** of the threshold;
> - the scribe's **independent check of the landed implementation** on its own fixtures;
> - the r65 routed-defect corrections, which the landed lesson already covers in substance
>   — this draft is the scribe's independent verification of each against committed bytes.
>
> Sections below that the landed lesson already carries are retained for the audit trail
> and are marked. Nothing in this draft overwrites the landed bytes.

**This is a draft for the L1 integrator. It is not in production.** Nothing here has been
admitted by this seat. Every numeric value that depends on a candidate run is written as
`not yet measured`, per the seat contract ("Keep blank numerical values out of production;
drafts may say not yet measured").

Lane `kasegi`; base `b6db9e818d322726e39cb441f2179d34d4170275`. One intended claim:
**C1 — depth:verifiability** (lowest non-retired axis, nominal 4 held under QUALITY R58).
Coverage 8 and density 9 are not targeted and not re-measured.

## Gate

S099 admitted as own-work/A, personally opened 2026-11-04, scoped only to this lane's local
cat-SIGPIPE exemption and the later-input masking case; not external security policy and
not general error detection.

- **Source (own-work repo artifact):** `corpus/instruments/figure-audit.py` at base
  `b6db9e818d322726e39cb441f2179d34d4170275`, sha256
  `86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef`.
- **Located quote (4 words by `wc -w`, 2026-11-04):** `return status != -signal.SIGPIPE`
  at L91 of that file, inside `upstream_stale` (L83-L94).
- **Location:** `upstream_stale` L83-L94; the exemption decision L90-L91; the docstring
  that documents the exemption L86-L88 ("SIGPIPE (-13) on a non-final stage is benign by
  documented rule"); the call site L129-L131, which passes only `argv[0]` (the head name)
  and therefore cannot see how many operands `cat` was given.
- **Execution source:** `.ufo/waves/round-66/controls/red-before-mechanism.txt` at
  `1957407e22331c73aafe944da2b37c182f13583a` — the L1's own base receipt for this class;
  the scribe's independent reproduction is `w1/ScribeRound/receipts/base-false-green-r66.txt`
  (gate sha256 `86becbde…`, the same bytes).
- **Anchor for the masked error:** `cat: missing.txt: No such file or directory` on stderr
  in the untruncated run, against the empty stderr of the truncated run.

**Admit:** the S099 row, scoped to the local exemption's semantics.

**Reject (kept as a rejection, not a silent row):** that the exemption's masking is a
general error-detection defect, that it is a pipefail/sandbox property, or that the
restriction generalises to any command other than `cat`. The gate is not pipefail, not a
sandbox and not an authenticity check; the sibling residual classes (grandchildren, shell
wrappers, PATH-shadowed binaries, exit-0 wrappers that print partial output) are untouched
and out of scope.

**Reject (bounded counter-example recorded as a residual, not a claim):** that the
restriction closes the masking class for *every* consumer. The masking needs a consumer
that closes the pipe early; `cat missing.txt | wc -l` already reads stale at base
(`derive-upstream-exit-1`) because `wc` drains the pipe, so the two-operand `cat` is stale
at base in that shape. The C1 class is the early-closing consumer.

**Assimilation: none.** `merge/kasegi/MERGE-REPORT.md` is not present on this host
(`find / -maxdepth 6 -name MERGE-REPORT.md` returned nothing), so no package row is read
and no package entry is adopted. `considerthese/2026-10-26.md` proposal 2 remains
domain-task-open; the documentation-only work in this round does not complete its six-file
task and earns **no SHONEN box 2 credit**. Promotion stays operator-owned.

## Measured result

| Axis | Before | After | Verdict / counter |
|---|---|---|---|
| depth:verifiability (lowest) | base gate: `cat big.txt missing.txt \| head -n 1` reads `derived=alpha ok`, `FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0`, rc 0 — a false green; the same missing operand under a draining consumer (`cat missing.txt \| wc -l`) reads `derive-upstream-exit-1 stale` | not yet measured (candidate not frozen) | expected **4 → 4, delta 0, nominal per R58** (the citation-resolution metric is untouched). `python3 -B .ufo/waves/round-66/verify.py --revision … --work … --final` |
| coverage | `rows=44 admitted=44 closed=44 problem-rows=0 registry=98` (r65) | not yet measured | **8 → 8, delta 0.** One own-work registry row (S099) is curation, not new domain ground; the coverage denominator is operator-owned. |
| depth:density | 9 | 9 held | Not targeted or re-measured. No density credit asserted. |

### The base false green, as the scribe measured it

Reproduced on the **public path** (the committed production gate, not a copy of it), from a
scratch clone of the lane checked out at base, with a 4 MiB first operand and a
deliberately absent second operand:

```
$ python3 -B corpus/instruments/figure-audit.py --ledger …/ledger.json --root …/work
FIG miss-head recorded=alpha derived=alpha ok
FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0
[rc=0]
```

The native stages behind that green are `cat` killed by **SIGPIPE (-13)** and `head` exit 0,
with **empty stderr** — the missing operand was never diagnosed. The untruncated run
reports `cat: missing.txt: No such file or directory` and exit 1. Full receipts:
`w1/ScribeRound/receipts/base-false-green-r66.txt` and `receipts/native-statuses-r66.txt`.

### A finding that changes how the counter must be built

**The false green is size-gated, and the gate edge is a genuine race.** Measured on this
host (Linux 7.2.11-arch1-1, pipe capacity 65 536 bytes, `pipe-max-size` 1 048 576), 100
repetitions per size, with stderr categorised so that "cat never reached the missing
operand" and "cat reported it" are never conflated:

| first operand bytes | base outcome (100 reps) | false green |
|---:|---|---:|
| 393 216 | stale (missing.txt diagnostic) | 0/100 |
| 520 000 | stale (missing.txt diagnostic) | 0/100 |
| 524 288 | **mixed** | 95/100 |
| 528 000 | **mixed** | 90/100 |
| 540 000 | false green | 100/100 |
| 589 824 | false green | 100/100 |
| 1 048 576 | false green | 100/100 |
| 4 194 304 | false green | 100/100 |

Mechanism (traced): `cat` moves the file into the pipe with `splice()` in **512 KiB
chunks**; `head` reads one 8 192-byte chunk and exits; the next `splice` returns `EPIPE`.
Below the chunk size the whole operand fits, `cat` finishes, reports the missing operand
and exits 1 — the base is already stale and there is no false green to detect.

Three consequences, stated as counter-design constraints:

1. **A short fixture is vacuous for this class.** Below ~512 KiB the base reads stale, so a
   probe built on a short file cannot discriminate candidate from base: an unmodified gate
   passes it. The L1's own round-66 LOG bullet already records this ("Small-file behavior
   is different, so a short fixture is vacuous for this class"); the scribe's measurement
   puts a number on it.
2. **A fixture inside the 512-528 KiB band is flaky.** Repeated runs of the same committed
   bytes disagree (95/100, then 90/100, then 100/100 as size rises). A single-run counter
   placed there is not reproducible.
3. **The threshold is host-specific, not a portable constant.** It is a function of the
   pipe capacity and `cat`'s chunk size on this machine. A counter must therefore assert
   the **native stage status** (`native0=-13`), not a size threshold — which is what the
   r66 probe set already records.

**No new knowledge, no new criterion, no new source row beyond S099.** The size-gating is
a property of the host and the fixture, recorded here as a counter-design constraint and
as a residual. It is not a QUALITY criterion: R88 already states the governing rule ("an
exemption class in a gate is probed for the error it can mask … and the probe set carries
at least one control where that status hides a real failure"), and R88's check is what the
r66 probe set implements. Adding a criterion here would duplicate R88 without adding a
discriminating test.

## Mistakes

| id | class | evidence | captured-by | fix / disposition |
|---|---|---|---|---|
| M66-1 | an exemption's masking probe needs a fixture that reaches the masking | the base false green needs a first operand above `cat`'s 512 KiB splice chunk; at 524 288 bytes the outcome is a race (95/100), below 520 000 it never masks at all (0/100); a short fixture makes the base already stale, so an unmodified gate passes the probe | seat ScribeRound, from the public path at base (`w1/ScribeRound/receipts/threshold-band-r66.txt`) | the counter asserts the native stage status and uses a 4 MiB operand; the size threshold is named as host-specific in the claim's residuals, not as a portable rule. R88's control is the governing criterion; no new criterion is added |
| M66-2 | a status label is not the error it hides | `cat` killed by SIGPIPE (-13) and `cat` reporting the missing operand both leave the gate reading `ok` on the truncated shape; only stderr separates "never diagnosed the error" from "diagnosed it" | seat ScribeRound (`receipts/native-statuses-r66.txt`, `receipts/threshold-band-r66.txt`) | every scribe measurement categorises stderr, so a false green and an honest stale are never counted as the same outcome |

## Carry-in — round-65 routed defects (append-only; each is corrected in the r66 records)

These are the six defects the round-65 verifier routed to the lane. Each correction below
is **append-only**: nothing in the filed round-65 report is rewritten, and no round-65
number is restated as if it had been re-measured.

1. **Commit→LOG ties must cite bullets, not "bolts".** The filed report's Landed-changes
   table says "LOG bolts 1–12" / "LOG bolt 12". `LOG.md`'s Round 65 section has **10
   bullets** (`awk 'NR>2667 && /^- /' LOG.md` counts 10) and the string `bolt` occurs
   **nowhere** in `LOG.md` (`grep -c 'bolt' LOG.md` = 0). Correction: cite bullet indices
   ("§ Round 65 bullet 4"), not "bolt" labels.
2. **Two round commits were missing from the Landed-changes table.** `git rev-list --count
   a283189…a3357329` = **15** commits; the table named 13. The unlisted are **`1929a47`**
   (widen the S098 body range — M65-9) and **`6824522`** (re-record the final-tip receipt).
   Both exist in the lane and both are ancestors of the tip. Correction: the round-66
   Landed-changes table lists all 15.
3. **The "exact final driver" label was wrong for the receipt it cited.** The report's
   before-block cites the `base-finaldrv2` workdir, whose receipt
   (`controls/driver-base-donothing-finaldrv-r65.txt`) records the erratum-1 driver
   **`5aa842ab…`**. A same-result base receipt from the *final* driver exists:
   `controls/driver-base-donothing-r65.txt`, driver sha256 **`7f27c4d2…`**, 8/3, with
   `GUARD driver-self-pin PASS`. Correction: cite the `7f27c4d2…` receipt.
4. **"Final tip" was not the lane tip.** The tip receipt names revision **`03a23921`**;
   the lane tip is `a3357329`, two receipt-only commits later
   (`6824522`, `a3357329`; `git diff 03a23921 a3357329` touches only three receipt
   files). Correction: name the revision as measured and state the delta.
5. **Base receipts record no exit code for the driver itself — and still do not.** The
   filed report claims the base ran "exit 1", but the three
   `controls/driver-base-donothing*.txt` receipts end at
   `VERIFY measurements=8 failures=3 revision=a283189…`. They do carry `exit=` values for
   individual sub-results (the probe audit exits, the selftest, the ledger, the
   collector-selfcheck), but **no line records the driver's own process exit status**,
   which is what the report's "exit 1" asserts — the candidate receipt
   `controls/final-verification-tip-r65.txt` *does* end with a bare `exit=0`. That exit
   status was never captured and is **not invented here**: the round-66 receipts must
   capture the exit code of every run, and the round-65 receipts are described as
   recording the driver's own exit code as absent.
6. **Helper-count phrasing.** `w1/SentinelScope/07-parser-sort-compress-exec.txt` records
   `marker lines=121900 (two gate runs appended; ~60950 program invocations per run)`.
   The filed report's "executed a helper 121900 times" reads as one run. Correction:
   **121 900 across two runs**, ~60 950 per run.

## The scribe's independent check of the landed implementation

The L1 landed the repair at commit `e8a865d` (gate sha256
`51f299aff8d9ec8ddc23201e78a4dce7338833bc7c409a37bd19bc8da6b4eeac`, byte-identical to the
frozen candidate). Against the **scribe's own** fixtures and ledgers — built independently
of the round's probe collector, in the scratch work directory, on the same base tree —
the landed gate and the base gate differ exactly where the frozen scope says they should:

| probe shape | base | landed |
|---|---|---|
| `cat big.txt missing.txt \| head -n 1` (two operands, later missing) | `derived=alpha ok` | `derive-upstream-signal-13 stale` |
| `cat big.txt other.txt \| head -n 1` (two operands, both existing) | `derived=alpha ok` | `derive-upstream-signal-13 stale` |
| `cat big.txt \| head -n 1` (one operand) | `derived=alpha ok` | `derived=alpha ok` |
| `cat < big.txt \| head -n 1` (stdin only) | `derived=alpha ok` | `derived=alpha ok` |
| `cat missing.txt \| wc -l` (pre-existing stale) | `derive-upstream-exit-1 stale` | `derive-upstream-exit-1 stale` |
| `grep absent big.txt \| wc -l` (no-match positive) | `derived=0 ok` | `derived=0 ok` |

Operand-count edge cases: `cat -- -- missing.txt` (the second `--` is a **real operand**,
so the count is two) → landed `derive-upstream-signal-13 stale`; `cat -- big.txt` (one
operand after a separator) → landed `ok`; `cat -n big.txt` (option-bearing, conservatively
refused) → landed `derive-upstream-signal-13 stale`; `cat - < big.txt` (stdin via `-`) →
landed `ok`.

This matches the frozen scope in `.ufo/waves/round-66/claims.json` ("decoded stdin-only/one
operand with optional leading `--` stays benign. Multi-input and option-bearing cat
SIGPIPE is conservatively stale even with existing inputs; no claim every newly stale
input failed. Non-cat SIGPIPE rule unchanged."). It is the scribe's independent
observation on its own fixtures, **not an admission** and not a substitute for the frozen
counter's final measurement. Receipt:
`w1/ScribeRound/receipts/landed-implementation-r66.txt`.

## Residuals and open

- The restriction binds the **exemption to `cat`'s decoded operand count**. `cat` with
  stdin-only or exactly one operand keeps the exemption; two or more operands lose it.
  Conservative refusal for option-bearing forms is a legitimate reading and must be
  **named** in the claim if adopted, not silently applied.
- Operand counting must follow the **decoded argv**, not the raw string: a `--`
  separator is not an operand, and a second `--` is a real operand. The scribe measured
  `cat -- -- missing.txt | head -n 1` with a 4 MiB file literally named `--`: 30/30
  false green at base, i.e. the operand count there is **two**, not one.
- The masking still needs an early-closing consumer. A draining consumer (`wc`) already
  reads stale at base. The class is not closed for every consumer shape.
- The size threshold is **host-specific** (this host: ~512 KiB). It is a fixture property,
  not a portable constant; the counter must assert native stage status instead.
- Single-operand `cat` that dies of SIGPIPE stays exempt by design, so a *single* operand
  that is itself unreadable in a way that also produces SIGPIPE is not covered by C1.
- Depth:coverage 8 and depth:density 9 are held, not re-measured. The gate is not
  pipefail, not a sandbox and not an authenticity check. Grandchildren, shell wrappers,
  PATH-shadowed binaries and exit-0 wrappers printing partial output remain out of scope
  (the r65 residuals, unchanged).
- The r65 seat-emulator finding (M65-5) stands: the documented probe set alone cannot
  reject a semantic emulator.
- **No SHONEN box 2 credit.** Box 2 (end-to-end domain task) stays `[ ]`: no authorized
  end-to-end domain task was executed in this round, and the documentation-only claim
  does not close `considerthese` proposal 2. Boxes 1, 3 and 4 remain as in round 65.
- Promotion is operator-owned. No box was marked; no MANIFEST or registry edit was made by
  this seat.
