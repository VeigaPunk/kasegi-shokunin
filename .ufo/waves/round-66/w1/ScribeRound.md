# ScribeRound — scoped findings (kasegi round 66, wave 1)

Seat: **ScribeRound** (leaf scribe; no subagent dispatch). Lane:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Round evidence:
`.ufo/waves/round-66`. Base `b6db9e818d322726e39cb441f2179d34d4170275`.

**Status of the round when I finished: the claim is frozen and the repair is landed.**
While this seat worked the L1 landed `corpus/lessons/round-66.md`, the round-66 LOG
section, the S099 registry row, the frozen claim (`.ufo/waves/round-66/claims.json`,
frozen 2026-11-04T20:33:00Z) and the implementation commit `e8a865d`. **I hold no admission
authority and admit nothing.** My four drafts are therefore positioned as **supplements
with named increments**, not as files to write over the landed records; each carries a
status banner saying so. No production file was created or modified by this seat; no
commit, push, publish or deploy was performed; no git index or jj state was touched.

## What I produced

All writes are under my seat directory and my seat report only:

| file | what it is |
|---|---|
| `.ufo/waves/round-66/w1/ScribeRound/lesson-draft-round-66.md` | **supplement** to the landed `corpus/lessons/round-66.md`: Gate (S099 own-work, quote/date/location), measured-result table, Mistakes M66-1/M66-2, carry-in of the six r65 routed defects, the scribe's independent check of the landed implementation, residuals |
| `.ufo/waves/round-66/w1/ScribeRound/scorecard-draft-round-66.md` | **supplement** to the landed round-66 SCORECARD section: before/after table, residuals, capabilities, saturation, move log, planned-after |
| `.ufo/waves/round-66/w1/ScribeRound/log-draft-round-66.md` | **supplement** to the landed nine-bullet round-66 LOG section, in the file's own `- ` bullet convention |
| `.ufo/waves/round-66/w1/ScribeRound/r65-correction-draft.md` | append-only correction of the six r65 routed defects: what the filed report says, what the committed bytes show, what r66 cites instead — the scribe's independent verification of the substance the landed lesson already carries |
| `.ufo/waves/round-66/w1/ScribeRound/receipts/base-false-green-r66.txt` | base public-path reproduction of the false green, with hashes and rc |
| `.ufo/waves/round-66/w1/ScribeRound/receipts/native-statuses-r66.txt` | independent native pipeline statuses for the six probe shapes |
| `.ufo/waves/round-66/w1/ScribeRound/receipts/size-gating-r66.txt` | size ladder + mechanism trace (corrected, absolute fixture paths) |
| `.ufo/waves/round-66/w1/ScribeRound/receipts/threshold-band-r66.txt` | fine threshold ladder, the `--` operand form, mechanism, and the counter-design constraints |
| `.ufo/waves/round-66/w1/ScribeRound/receipts/gate-quote-r66.txt` | S099 Gate evidence: quote, word count, date, location, id check |
| `.ufo/waves/round-66/w1/ScribeRound/receipts/landed-implementation-r66.txt` | the scribe's independent base-vs-landed check of the shipped repair on its own fixtures |

Scratch `/fast/scratch/hyaku/kasegi-r66/ScribeRound/` (one shared clone) is deleted before
this report; the durable receipts above are the copy.

**Note on four of my receipts already in the lane's history.** The L1 committed four files
from my seat directory in `0d5aef2` / `6102c0e` (`base-false-green-r66.txt`,
`gate-quote-r66.txt`, `native-statuses-r66.txt`, `size-gating-r66.txt`) — the durable
evidence I produced, landed by the integrator. Two of those four I have since **corrected
in place** as working-tree modifications (not committed, because this seat does not touch
the git index): `native-statuses-r66.txt` (the `cat < big.txt` row previously read
`rcs=[0, 0]` with empty output, because that harness left `cat`'s stdin unattached; it now
correctly reads `rcs=[-13, 0]` with `out=b'alpha\n'`, matching the gate's own
`cat < big.txt` input redirection) and `base-false-green-r66.txt` (a clarifying note that
the gate resolves ledger paths against `--root`, so the relative fixture names in that
receipt are correct there). **The L1 should re-commit those two corrections.** The
superseded `native-statuses` values are not cited anywhere in the drafts; the landed
records' own numbers are unaffected, since that receipt is evidence, not a claim input.

**Checked the shipped repair independently, on my own fixtures.** After the L1 landed the
implementation (commit `e8a865d`, gate sha256 `51f299af…`, byte-identical to the frozen
candidate), I ran the base tree and the landed tree side by side over ledgers I built
myself in scratch. The landed gate turns exactly the two two-operand `cat` SIGPIPE cases
from the base's green `ok` into `derive-upstream-signal-13 stale`, and leaves the
one-operand case, the stdin-only case, the grep no-match positive and the pre-existing
`cat missing.txt | wc -l` stale unchanged. On the operand-count edge cases it refuses
`cat -- -- missing.txt` (the second `--` is a real operand, so the count is two) and
`cat -n big.txt` (option-bearing, conservatively refused), while `cat -- big.txt` (one
operand after a separator) and `cat - < big.txt` (stdin via `-`) stay benign. That matches
the frozen scope in `claims.json`. This is my observation on my own fixtures — **not an
admission** and not a substitute for the frozen counter's final measurement. Receipt:
`receipts/landed-implementation-r66.txt`.

## Behavior

**Reproduced the base false green on the public path, independently of the L1.** From a
scratch clone of the lane checked out at base, the **committed production gate**
(`corpus/instruments/figure-audit.py`, sha256 `86becbde…`) run against a 4 MiB first
operand and a deliberately absent second operand prints:

```
FIG miss-head recorded=alpha derived=alpha ok
FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0
[rc=0]
```

The native stages behind that green are `cat` killed by **SIGPIPE (-13)** and `head` exit
0 with **empty stderr** — the missing operand is never diagnosed. The untruncated run
reports `cat: missing.txt: No such file or directory` and exit 1. The same missing operand
under a draining consumer (`cat missing.txt | wc -l`) already reads
`derive-upstream-exit-1 stale` at base. This confirms M65-7 on the public path and
matches the L1's own `controls/red-before-mechanism.txt` on the same bytes.

**Mined M65-7 with R88 and found a counter-design constraint the other receipts do not
state.** R88 requires the probe set to carry a control where the benign status hides a
real failure. I probed for the *error the exemption masks* and found the masking is
**size-gated**, with a **flaky band** at the edge (100 reps per size, stderr categorised
so "never diagnosed" and "diagnosed it" are never conflated):

| first operand bytes | base outcome (100 reps) | false green |
|---:|---|---:|
| 393 216 | stale (missing.txt diagnostic) | 0/100 |
| 520 000 | stale (missing.txt diagnostic) | 0/100 |
| 524 288 | **mixed** | 95/100 |
| 528 000 | **mixed** | 90/100 |
| 540 000 | false green | 100/100 |
| 589 824 / 1 048 576 / 4 194 304 | false green | 100/100 |

Mechanism, traced with `strace`: `cat` moves the file into the pipe with `splice()` in
**512 KiB** chunks; `head` reads one **8 192-byte** chunk and exits; the next `splice`
returns `EPIPE`. Below the chunk size the whole operand fits, `cat` finishes, reports the
missing operand and exits 1 — the base is already stale and there is no false green to
detect. Host parameters: pipe capacity 65 536 bytes, `pipe-max-size` 1 048 576.

Three consequences for the counter, stated as constraints:

1. **A short fixture is vacuous for this class.** Below ~512 KiB the base reads stale, so
   an unmodified gate passes the probe — a counter built on a short file cannot
   discriminate. (The L1's own LOG bullet already records that small-file behavior
   differs; this puts a number on it.)
2. **A fixture inside the 512-528 KiB band is flaky.** Repeated runs of the same committed
   bytes disagree, so a single-run counter placed there is not reproducible.
3. **The threshold is host-specific, not a portable constant** — it is a function of the
   pipe capacity and `cat`'s chunk size on this machine. A counter must therefore assert
   the **native stage status** (`native0=-13`), which the r66 probe set already records,
   rather than encoding a size threshold.

The r66 probe set's 4 MiB operand (`BIG_TARGET = 4 * 1024 * 1024`) sits 8× above the
measured edge and is deterministic here (200/200 native, 40/40 gate-level), so this
constraint **does not invalidate the probe set**; it sharpens the fixture-size rationale
and the residual wording.

**Checked the operand-counting edge the claim depends on.** The claim binds the exemption
to `cat`'s decoded operand count, so the separator form matters. Measured
`cat -- -- missing.txt | head -n 1` with a 4 MiB file literally named `--`: **30/30 false
green at base** — the second `--` is a real operand, so the operand count there is **two**,
not one. A `--` separator is not an operand; a second `--` is.

**Named the six r65 routed defects as an append-only correction**, each with the filed
claim, the committed bytes, and what r66 cites instead:

1. **LOG bullets, not "bolts".** `LOG.md`'s Round 65 section has **10 bullets**
   (`awk 'NR>2667 && /^- /'` = 10) and the string `bolt` occurs **nowhere** in `LOG.md`
   (`grep -c 'bolt' LOG.md` = 0). The filed table also cites a nonexistent "bolt 12".
2. **Omitted commits `1929a47` and `6824522`.** `git rev-list --count a283189…a3357329` =
   **15**; the filed table names 13. Both commits exist and are ancestors of the tip
   (`1929a47` = widen the S098 body range, M65-9; `6824522` = re-record the final-tip
   receipt).
3. **The final-driver base receipt is `7f27c4d2…`, not `5aa842ab…`.** The filed before
   block cites the `base-finaldrv2` workdir, whose receipt
   (`controls/driver-base-donothing-finaldrv-r65.txt`) records the **erratum-1** driver
   `5aa842abdceac676ff8c0a1b90f641bbad93a9505161f192dde85b1a1d06aaaf`. The same-result
   base receipt from the **final** driver is
   `controls/driver-base-donothing-r65.txt` — `driver_sha256=7f27c4d2…`,
   `GUARD driver-self-pin PASS`, 8/3 — and `sha256sum verify-r65.py` = `7f27c4d2…` =
   `driver.sha256`, so the counter identity is checkable.
4. **Measured revision `03a23921`, not the lane tip `a3357329`.** Two receipt-only commits
   later; `git diff 03a23921 a3357329` touches exactly three receipt files
   (`census-after-r65.txt`, `final-verification-tip-r65.txt`, `fresh-clone-r65.txt`), so
   the verdict is unaffected. The revision is named as measured and the delta stated.
5. **The base receipts record no exit code for the driver itself.** They end at
   `VERIFY measurements=8 failures=3 revision=a283189…`. They *do* carry `exit=` values
   for individual sub-results (probe audit exits, selftest, ledger, collector-selfcheck),
   but no line records the **driver's own process exit status** — which is what the filed
   report's "exit 1" asserts. The candidate receipt
   `controls/final-verification-tip-r65.txt` *does* end with a bare `exit=0`. **That exit
   status was never captured and is not invented here.**
6. **Helper count `121900` spans two runs.** The sentinel receipt records
   `marker lines=121900 (two gate runs appended; ~60950 program invocations per run)`, so
   the figure is **121 900 across two runs**, ~60 950 per run — not one run.

**Prepared the S099 own-work Gate row with quote, date and location**, as required.
Located quote (4 words by `wc -w`, opened 2026-11-04): `return status != -signal.SIGPIPE`
at **L91** of `corpus/instruments/figure-audit.py` at base `b6db9e8…` (sha256
`86becbde…`), inside `upstream_stale` (**L83-L94**), whose docstring documents the
exemption at **L86-L88** and whose call site (**L129-L131**) passes only `argv[0]` — the
head name — and therefore cannot see how many operands `cat` was given. The row is scoped
only to the local exemption and the later-input masking case; it is not external security
policy and not general error detection. Evidence:
`receipts/gate-quote-r66.txt`.

**Kept blank numbers out of the drafts.** Every after-value that depends on a candidate
run reads `not yet measured`; no placeholder zeros, no empty cells. **No SHONEN box 2
credit**: box 2 stays `[ ]`, the documentation-only claim does not close `considerthese`
proposal 2, and no box was marked.

## Gates I ran, and what they did **not** cover

- Only the checks my item required: a public-path reproduction of the base false green,
  native status capture for the six probe shapes, the size ladder and its mechanism, the
  `--` operand form, the S099 Gate quote/id check, the six r65 defect verifications, and
  — after the L1 landed the repair — a base-vs-landed comparison on my own fixtures. No
  general build, lint or test sweep was run, and I did not run the round's frozen counter
  or mutation battery — those are the L1's and the executor seats'.
- Every receipt records command, base/input hashes, observed stdout and rc. Nothing is
  reported as passing that I did not observe passing.
- **One measurement of mine was wrong and I corrected it.** My first size-ladder harness
  wrote fixtures under a relative name while `cat` ran with a different cwd, so the
  measured fixture was not the one opened; the receipt would have shown "stale" for
  sizes that actually produce the false green. I found this by capturing `cat`'s stderr
  and classifying it, re-ran the whole ladder with absolute paths, and the regenerated
  `receipts/size-gating-r66.txt` and `receipts/threshold-band-r66.txt` are the corrected
  ones. The superseded intermediate numbers are not cited anywhere in the drafts.
- **A correction I initially overstated, and fixed.** My first draft of correction 5 said
  the base receipts contain no `exit=` line at all. They contain `exit=` for individual
  sub-results; what is missing is the **driver's own** exit status. The drafts now say
  exactly that, and the distinction is checked against the committed bytes.

## Touched surfaces

**Read-only:** the lane's production tree (`corpus/instruments/figure-audit.py`,
`corpus/instruments/figure-audit-ledger.json`, `corpus/SOURCES.md`, `corpus/QUALITY.md`,
`corpus/lessons/round-65.md`, `corpus/lessons/round-65-verifier-spotcheck.md`, `LOG.md`,
`SCORECARD.md`, `SHONEN.md`), the r65 wave evidence, and the filed fleet report
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-65/kasegi.md`.

**Written:** only `.ufo/waves/round-66/w1/ScribeRound/` and this report. Scratch under
`/fast/scratch/hyaku/kasegi-r66/ScribeRound/`, deleted before yielding. Four of my
receipts were subsequently committed by the L1 (`0d5aef2`, `6102c0e`); my two subsequent
in-place corrections to them are uncommitted working-tree modifications, since this seat
does not touch the git index.

**Not touched:** any production file, any sibling seat's directory, the fleet root's
tracked files, `~/.local/bin` or any PATH directory, the git index, any jj state, any
commit, push, publish or deploy.

**Tooling:** no install was needed; the tools used were already present — `python3`
3.14.8, `git` 2.56.0, `strace` (system package), `awk`/`grep`/`sha256sum` (coreutils).
**No pacman transaction was performed** — the operator's pacman pause is observed.

**Scratch hygiene:** one shared clone (`/fast/scratch/hyaku/kasegi-r66/ScribeRound/clone`,
`--no-hardlinks` from the lane), checked out at base; `git rev-parse --show-toplevel`
asserted before any git operation in it; `TMPDIR` was not needed because all fixtures
were written under the scratch work directory by absolute path.

## Out of scope for this seat

- Admission, freezing and integration of C1 — L1's.
- The candidate gate, the probe collector's correctness, the driver's committed-input
  discipline and the mutation battery — the executor and mutation-tester seats'.
- Any coverage/knowledge/frontier claim: this round holds coverage 8 and density 9, and
  the only registry row is the own-work S099.
- Any QUALITY criterion. R88 already states the governing rule and its check is what the
  r66 probe set implements; the size-gating finding is a counter-design constraint and a
  residual, not a portable rule, so adding a criterion would duplicate R88 without
  adding a discriminating test.
- The r65 verdicts themselves, and the filed r65 report's text.

## Findings for the L1

**Already carried by the landed records — the scribe's independent verification only.**
The landed `corpus/lessons/round-66.md` and the round-66 LOG section already state the
six r65 corrections (items 1-6) in substance, the S099 curation, and M66-1/M66-2 (the
exemption-masking class and the vacuous-short-fixture class). I verified each of those
against the committed bytes; the verification is in `r65-correction-draft.md` and the
receipts. The increments below are the ones the landed records do **not** carry.

1. **The size-gating result is a constraint on the counter, not on the candidate.** The
   4 MiB probe fixture is safe (8× above the measured edge, 200/200 native, 40/40
   gate-level). The landed M66-2 names the class; the **numbers and the mechanism** are
   new: the edge sits between 520 000 B (0/100 false green) and 540 000 B (100/100), with
   a genuinely **flaky band at 524 288-528 000 B** (95/100 and 90/100). The mechanism is
   `cat`'s 512 KiB `splice()` chunk against this host's 65 536-byte pipe, with `head`
   reading one 8 192-byte chunk and exiting. State it so a later shrink of the fixture
   does not silently make the probe vacuous.
2. **The threshold is host-specific, not a portable constant.** It is a function of the
   pipe capacity and `cat`'s build on the measuring machine. The counter must assert the
   **native stage status** (`native0=-13`) rather than a size threshold — the r66 probe
   set already records `native0`, and this should be why that recording is retained.
3. **The `--` separator operand-count edge case is worth keeping as a residual.** The
   landed `cat_sigpipe_exempt` handles it correctly (a leading `--` is stripped; a second
   `--` is a real operand, so the count is two → stale), and I verified that behaviour
   end-to-end. But the *reason* it is right — that the second `--` is a real operand —
   is not stated in the landed records, and it is the kind of detail a future edit to the
   exemption could get wrong silently.
4. **The conservative refusal is already named in the frozen scope**, so no correction is
   needed: `claims.json` says "Multi-input and option-bearing cat SIGPIPE is conservatively
   stale even with existing inputs; no claim every newly stale input failed." My
   independent check confirms `cat -n big.txt` is stale under the landed gate and
   `cat -- big.txt` / `cat - < big.txt` stay benign, which is that scope exactly.
5. **S099's Gate evidence is complete** (quote 4 words, date 2026-11-04, location L83-L94
   / L91 at base `b6db9e8…`, sha256 `86becbde…`) and the landed row carries it. One id
   note, stated with its limits: the r65 staged-ids artifact lists `S099` among the
   unadopted package band, but that band carries **no reservation declaration in
   `corpus/SOURCES.md`** (0 hits for `S100`/`S199`/`S032–S099`), and **68 staged-band ids
   are already adopted** as registry rows — including this lane's own S096, S097 and S098
   own-work rows and the S099 row itself. The lane's established practice is therefore
   the contiguous next unused id, and S099 follows it; this is a note, **not an
   objection**, and it needs no reconciliation. The landed lesson reaches the same
   conclusion independently ("staged ids reserve nothing in this moving registry"). I did
   not touch the registry.

## Known limits of this report

- Every claim here is a **draft or a supplement**; nothing is admitted by this seat, and
  the landed records were not written by me.
- The frozen counter was never run by me, so the round's final after-state is **not
  asserted** by this seat; where the drafts state an after-value it is either marked
  `not yet measured` or is explicitly the scribe's own base-vs-landed observation on the
  scribe's own fixtures.
- The size-gating numbers are **this host's**: a different host's pipe capacity or
  `cat` build would move the edge. The receipts state the host parameters so the numbers
  are re-derivable rather than portable.
- The false-green classification rests on `cat`'s stderr being empty in the masked case and
  naming the missing operand in the honest case. That discriminator is used consistently
  in every measurement above, and the receipts show the categorised counts.
- The claim was frozen and the repair landed **during** this seat's work, so my drafts
  were written against a moving target. Where the landed records had already covered the
  substance, I kept the draft for the audit trail and marked it as a supplement rather
  than presenting it as new content — so a reader must not double-count the lesson's
  Mistakes rows or the LOG's bullets.
