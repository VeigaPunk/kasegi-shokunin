# DRAFT — SCORECARD.md append (scribe draft for the L1 integrator)

> **STATUS: SUPPLEMENT, not a replacement.** The L1 landed the round-66 SCORECARD section,
> the frozen claim (`.ufo/waves/round-66/claims.json`, frozen 2026-11-04T20:33:00Z) and the
> implementation commit `e8a865d` while this seat worked. **Do not write this draft as a
> file.** It is the scribe's independent record; the increments the L1 may still want are
> the **quantified** size-gating (numbers + mechanism), the **`--` separator
> operand-count** edge case, the **host-specificity** of the threshold, and the scribe's
> **independent base-vs-landed verification** on its own fixtures. Where the landed
> records already carry the substance, this draft is retained for the audit trail only.

**Draft only. Not in production.** No after-value that depends on a candidate run is
asserted by this seat; every such value reads `not yet measured` below, except where the
scribe observed it directly and says so. Nothing here decreases an earlier score.

---

## Round 66 — the cat SIGPIPE masking restriction (C1, depth:verifiability, nominal 4 held)

Frozen claims: not yet frozen in this draft. Base `b6db9e818d322726e39cb441f2179d34d4170275`;
proposed driver `not yet measured`. The C1 predicate in draft: on the committed-input
counter, the base gate's false green on `cat big.txt missing.txt | head -n 1` is replaced
by a stale reading with reason `derive-upstream-signal-13`, while the single-operand and
stdin-only `cat` SIGPIPE positives, the grep-no-match positive and the plain
`cat missing.txt | wc -l` stale case are preserved.

| Axis | Before | After | Score delta, command and evidence |
|---|---:|---:|---|
| depth:verifiability (lowest) | base public gate on `cat big.txt missing.txt \| head -n 1` → `FIG … derived=alpha ok`, `FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0`, rc 0 — a **false green**; native stages `[-13, 0]` with empty stderr, so the missing operand is never diagnosed; the same operand under a draining consumer reads `derive-upstream-exit-1 stale` | the scribe's own base-vs-landed check on independent fixtures: the two-operand cat SIGPIPE cases read `derive-upstream-signal-13 stale` under the landed gate (`e8a865d`) where the base read `ok`; the one-operand, stdin-only and grep-no-match positives stay `ok`; the pre-existing `cat missing.txt \| wc -l` stale is unchanged. The frozen counter's final measurement is the L1's to record — **not yet measured by this seat** | expected **4 → 4, delta 0, nominal per R58** (the citation-resolution metric is not moved). `python3 -B .ufo/waves/round-66/verify.py --revision … --work … --final`; evidence `w1/ScribeRound/receipts/base-false-green-r66.txt`, `receipts/native-statuses-r66.txt`, `receipts/landed-implementation-r66.txt` |
| coverage | `rows=44 admitted=44 closed=44 problem-rows=0 registry=98` (r65 close) | not yet measured | expected **8 → 8, delta 0.** One own-work registry row (S099, cat SIGPIPE masking diagnostic) is curation of local gate semantics, not new domain ground; the coverage denominator stays operator-owned |
| depth:density | 9 | 9 held | Not targeted or re-measured. No density credit asserted. |

**Residuals named, not claimed:** the exemption is bound to `cat`'s **decoded operand
count** (stdin-only or exactly one operand keeps it; two or more lose it), and a
conservative refusal for option-bearing forms is a legitimate reading that must be named
if adopted. Operand counting follows the decoded argv — a `--` separator is not an operand
and a second `--` is (measured: `cat -- -- missing.txt | head -n 1` with a 4 MiB file named
`--` is 30/30 false green at base, so the operand count there is two). The masking still
requires an early-closing consumer; a draining consumer already reads stale at base.
Single-operand `cat` that itself dies of SIGPIPE stays exempt by design. The
**size threshold is host-specific** (this host: ~512 KiB, the point where `cat`'s 512 KiB
`splice()` chunk stops fitting the 65 536-byte pipe), so it is a fixture property and not
a portable rule — the counter asserts the native stage status instead. The gate is not
pipefail, not a sandbox and not an authenticity check; grandchildren, shell wrappers,
PATH-shadowed binaries and exit-0 wrappers printing partial output stay out of scope. The
r65 seat-emulator finding (M65-5) stands: the documented probe set alone cannot reject a
semantic emulator. Source restoration and the operator-owned R67/R69 decisions remain open.

**Capabilities:** no new row. The existing derive-gate row is extended in place — the
SIGPIPE exemption becomes operand-count-bounded for `cat` — demonstration
`python3 -B .ufo/waves/round-66/verify.py --revision … --final` → not yet measured.

**Saturation:** line 9/10 per owned axis; the lowest non-retired axis remains
depth:verifiability 4, worked nominally this round. No retirement or split.

### Round-66 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 66 | depth:verifiability | a large-first-operand `cat` with a later missing operand reads `ok` at base (SIGPIPE -13 masks the undiagnosed error) | not yet measured (candidate not frozen) | `.ufo/waves/round-66/controls/red-before-mechanism.txt` (L1 base receipt); `w1/ScribeRound/receipts/base-false-green-r66.txt` (scribe's independent public-path reproduction); `corpus/instruments/figure-audit.py` at `86becbde…` |
| 66 | coverage | frontier 44 / registry 98 (pre-round) | not yet measured; S099 own-work row proposed, used-by `corpus/lessons/round-66.md` | `corpus/SOURCES.md`; `w1/ScribeRound/receipts/gate-quote-r66.txt` |
| 66 | calibration | six r65 routed defects carried in; M66-1 and M66-2 found in-round | all six addressed append-only in the round-66 records; M66-1/M66-2 recorded | `corpus/lessons/round-66.md` § Carry-in and § Mistakes (draft: `w1/ScribeRound/lesson-draft-round-66.md`) |

### Planned after round 66 (not frozen)

1. **depth:verifiability (4, lowest):** the next gate claim must select a distinct observed
   residual with a failing do-nothing control. Candidates named by this round: the
   single-operand SIGPIPE case that stays exempt by design; the held-out probe pair
   standardised into the probe collector (M65-5, still open); or the exit-0-wrapper
   partial-output class. Do not re-claim the cat multi-operand case.
2. **coverage (8):** the coverage denominator stays operator-owned. The Fuzzilli primary
   documents and the OpenSSF aggregate-score/API portion remain unopened leads; the
   extended pre-freeze screen and anchor-referent table run before any freeze (R80).
3. **calibration:** the size-gating finding (M66-1) should reach the counter design, not a
   new QUALITY criterion — R88 already states the governing rule and its check is what the
   r66 probe set implements.
