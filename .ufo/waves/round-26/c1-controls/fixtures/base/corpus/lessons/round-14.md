# Round 14 — lesson: measurement bars, three-way derivation, and generated-file truth

Round: 14 (depth axis-move; thin-cohort per-item citation repair + claim-anatomy
sampling push 3.6%→10.7%). Evidence: `LOG.md` round-14 entry, `SCORECARD.md`
depth row, `/tmp/kasegi-r14/*` (10 L2 reports + density instrument + selection
script). What generalizes:

## 1. A density/citation metric is form-sensitive — fix the bar BEFORE editing

Identical section content measured 86.0 (80-col wrapped prose), 97.2 (88-col),
973.3 (single-line-row table) with the same locked script
(`/tmp/kasegi-r14/density.py`). Two consequences, both now rules:

- **Bar = pre-edit file mean of the same run** (r14: 102.5), never the
  post-edit mean: a successful repair inflates the mean it must clear
  (142.5 after) — a circular bar that can fail honest work. Compare each
  block to its own BEFORE.
- **Hold rendering form constant** across before/after, or the measurement
  measures wrapping, not knowledge. The r14 integration kept the repo's
  ~76-col prose idiom and still cleared the bar (106.6 / 108.4); the
  executor's table-form variant (973.3) was preserved in
  `/tmp/kasegi-r14/section-only.md` but not shipped — metric-gaming a proxy
  is not the goal, per-item verifiable anchors are.
- Mechanical reflow corrupts census tokens: textwrap(78) severs `path:NN`
  spans and mints fake numerics (`20260915` from a split date). Rewrap by
  hand keeping every `path:line` intact per physical line; lint with
  backtick parity (`perl -ne 'print if tr/`// % 2'` — fence lines and
  deliberate multi-line code spans excepted).

## 2. Three-way derivation caught what every single auditor missed

- The **critic** falsified the 2026-09-05 severity decree as "nonexistent" —
  it grepped only `docs/`; the decree lives at `fleets/claimer-mission.md:29`.
  Rejected on L1's own grep + executor's verbatim + revenger's git timeline
  (b3b1b7e3 wrap-fixes 19:54 −03:00 → 2ef530c6 decree 20:56 −03:00).
- Both **executors** failed to locate the I8 definition ("no I8 in the
  domain tree") — it is at `fleets/mission-template.md:20` ("I8: never
  manufacture a finding"); L1's targeted grep found it in seconds.
- The **scout** mis-mapped one playbook anchor (`claim_checklist.md:31` vs
  the real `:19-20`) — L1's own sed adjudicated.
- Rule: an L2 falsification is a CLAIM, not a verdict. L1 must re-derive any
  claim that would delete or rewrite existing skill content, with its own
  read of the primary source, before integrating. Concordance across
  independent derivations (scout × executor × critic × revenger × L1) is what
  made the 3 real falsifications safe to repair in place.

## 3. Generated files carry two truths: the stale bytes and the live regen

`docs/claim-ready-index.md` on disk has 11 queue rows and a 2026-09-06
generated-stamp; the r10/r13-audited "12 queued" is the LIVE-regeneration
count (the 12th, intigriti-yahoo, went DONE+claimable after the stamp).
Neither number is wrong; citing one without the generator as-of is. Any
count sourced from a generated artifact gets: (a) the file's generated stamp,
(b) the row count of the bytes actually read, (c) the live-regen delta if
known. SKILL `:115` now models this.

## 4. "Read-only" surroundings still move — read the append-only log first

The domain tree gained 2 telemetry lines (`freshness_check` 23:32:22Z,
judge-lane `reroute_drill` 23:32:32Z) and one mtime-only touch
(`docs/claim-ready-index.md`, bytes unchanged HEAD==worktree) mid-round,
actor [UNVERIFIED]: no cron/timer/process match; an attached `ufo_sighting`
tmux hosts a separate live agent session; the two L2s alive that minute
attest read-only. Second occurrence after r13 (check-freshness +1, `.git`
touches). Practice: at round start AND before final measurement, snapshot
`wc -l ledger/telemetry.jsonl` + `find -newermt <round-start>` over the
domain tree; diffs during the round are either yours (forbidden) or
disclosed-with-[UNVERIFIED]-actor. Never revert an external append (revert =
second mutation); stamp as-of values instead.

## 5. Sampling with a preserved deterministic script turns "sampled" into a
##    reproducible claim

`select20.sh` (universe → exclusion → strata → even-index stride) re-runs
byte-identically; L1 re-ran it as acceptance (universe=280 eligible=263
selected=20). The ~3.6% "sampled" hedge that sat unowned since round 7/8 is
now 10.7% WITH a rule anyone can re-execute and a deviation taxonomy (D1-D13)
that annotates every contract claim with its real attestation strength
(the full status.json contract holds in 20/280 packages — 92.9% deviate).
Lesson: a sample without a preserved selection rule is a hedge; with one,
it is a census increment.

## 6. Subagent lifecycle hazard: despawn second-yields overwrite scratch

ExecutorAntipatterns' and ExecutorChecklist's post-DESPAWN yields rewrote
their `/tmp/kasegi-r14/draft-*.md` files AFTER L1 had integrated the first
verified yields (prose draft → table-form variant). No harm this round (L1
integrates from its own read + first yields), but: snapshot a scratch
deliverable (`cp draft.md draft.md.integrated`) at integration time if later
dispute resolution may need the exact bytes that were integrated.
