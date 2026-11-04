# SourceLedger — round 64 predata source-ledger report

Seat: SourceLedger (scribe, leaf). Axis: depth:verifiability. Nominal 4 held (R58). No production edits, no commits, no git mutations, no candidate scoring, no subagents. Output directory: `.ufo/waves/round-64/w1/SourceLedger/`. Scratch `/fast/scratch/hyaku/kasegi-r64/SourceLedger/` removed on exit after receipts were copied.

## Findings

1. **S097 own-work row and Gate drafted** (`SourceLedger/S097-row-draft.md`, `SourceLedger/lesson-gate-draft.md`). Located at committed base d74be00 (sha256 15bcb6c4…, identical to the r63 candidate): `Upstream exit1 and negative signal statuses remain` (L42–43), `if p.returncode > 1:` (L107), selftest controls L412 and L419. POSIX grep and cat EXIT STATUS quotes (fetched 2026-11-04) are recorded inside the Gate block as a spec companion row S098 for L1 to accept or reject. Quotes checked ≤25 words with `wc -w`.

2. **Wave expectation error (M64-4).** The prompt says base greens want0 for the missing-input probes except partial. Measured with the committed base instrument on own fixtures (`SourceLedger/base-probe-recon-r64.txt`, run-utc 2026-11-04T18:37:31Z): `ls missing | wc -l` and `sort missing | wc -l` are already **stale** at base with `derive-upstream-exit-2`. They are controls, not repairs. `cat`, `cat partial`, `cut`, `head`, `tail`, `sha256sum` are green at base as expected (partial green at 1). Candidate outcomes for the r64 rule are inference only, listed in `S097-row-draft.md`.

3. **Native exit values (GNU, absolute paths).** `SourceLedger/native-exit-absolute-paths-r64.txt` (run-utc 2026-11-04T18:38:06Z): cat/head/tail/cut/sha256sum/wc missing exit 1; ls/sort missing and `grep -e x missing` exit 2; grep no-match exit 1. POSIX defines only grep's 1 as no-match; cat's nonzero exit is specified only as `>0`, so the numeric 1 is a host value (`SourceLedger/subprocess-binary-identity-r64.txt`: GNU coreutils 9.12 and GNU grep 3.12 resolved by the instrument's own PATH lookup).

4. **Host hazard for probes (M64-6, self-caught).** In this persistent shell, bare `cat`, `grep`, `wc`, and other names resolve to wrapper functions (`command -v` prints a bare name). My first version and host-identity receipts were produced through them: `host-userland-identity-r64.txt` prints `uu 0.8.0` / `pi-uu-grep 0.2.0` and is **not** instrument identity; `native-exit-and-anchor-recon-r64.txt` used shell names and is superseded for native exits by the absolute-path receipt. Both kept as raw files, not used as evidence. Collector and mutation seats should use absolute binaries or `subprocess`.

5. **r63 missing-input closure (M63-7), mined.** Frozen `verify-r63.py` PATHS (8 entries) omits four ledger-declared receipts (`round-55/gate-final-r55.txt`, `round-56/df3-fixedpoint-r55tip.txt`, `round-53/c2-counter-final-r53.txt`, `round-56/gate-final-r56.txt`). All four exist at base (`git cat-file -e`), and the nonclaim supplemental reads ledger35/35 with them listed at INPUT 12–15. Static check: `verify-r64.py` PATHS lines 18–25 include them plus S086 and the collector. No dry run. Append-only correction text is in the lesson Gate draft.

6. **S096 placement (r63), mined.** S096's dated provenance is at `corpus/lessons/round-63.md:37` under the frozen-claim heading, not under `## Gate` (confirmed by the r63 closure at `round-63-verifier-spotcheck.md:15,79`). Restated append-only in the Gate draft; the S096 range 106–109 contains the verified line 107.

7. **Weak spot in the existing S094 trial.** `domain-qualification.py` checks phrases at hard-coded lines and its ARITHMETIC rows compute `index = column - 1`. Capture L51 names `SERIES_COLUMN_START` but its value is not in the capture (M64-5). The r63 domain ledger's four figures are count-only anchors (`grep -F … | wc -l`), so they do not say which line matched. Those are the weaknesses the trial proposal targets.

8. **Considerthese proposal 2 read.** `considerthese/2026-10-26.md:29-30` (end-to-end domain task: one disclosed report, six-file package, rebuilt claim checker). Mined only as a bounded trial, `SourceLedger/trial-proposal-r64.md`: located-line figures via `grep -n … | cut -d: -f1`, a negative ledger whose reason (not verdict) changes under the S097 rule, pre-registered kill rules, and explicit non-claims. Not a six-file package; SHONEN box 2 untouched.

## Sources and access (recorded inside the Gate draft)

- Own-work: `corpus/instruments/figure-audit.py` at d74be00, opened 2026-11-04 (`SourceLedger/committed-figure-audit-d74be00.py` copied from committed bytes).
- POSIX: pubs.opengroup.org grep and cat utility pages, fetched 2026-11-04 (edition Issue 7, 2018).
- S094: live Project Zero page read 2026-11-04 18:35Z; capture `corpus/source-snapshots/round-61/S094.txt` sha256 663ac16d… (matches the r64 qualification receipt's source digest).

## Gates and touched surfaces

- No gate or selftest of the candidate was executed. The base instrument was run once on own fixtures (copy in scratch, `probe-ledger.json` copied to output) to test the wave's expectations; that is recon, not verification of the production change.
- Writes: only `.ufo/waves/round-64/w1/SourceLedger.md` and `.ufo/waves/round-64/w1/SourceLedger/` files listed below. Nothing under `corpus/`, `LOG.md`, `SCORECARD.md`, `MANIFEST.json`, or sibling trees.
- No installs or updates; no tool, PATH, or ~/.local/bin changes. pacman not used.

Artifacts under `.ufo/waves/round-64/w1/SourceLedger/`:
- `S097-row-draft.md`: S097 row, S098 spec companion row, base vs candidate expectation table.
- `lesson-gate-draft.md`: Gate draft, S094 and POSIX quotes with access dates, append-only S096 and M63-7 corrections, M64-4..6 proposals.
- `trial-proposal-r64.md`: bounded disclosed-finding trial, figures, negative ledger, kill rules, non-claims.
- `committed-figure-audit-d74be00.py`: committed bytes copy (sha256 15bcb6c4…).
- `native-exit-absolute-paths-r64.txt`: absolute-binary native exits, run-utc 2026-11-04T18:38:06Z.
- `native-exit-and-anchor-recon-r64.txt`: superseded for native exits (shell names); anchor and word-count parts kept.
- `base-probe-recon-r64.txt`: committed base instrument on 10 own fixtures, run-utc 2026-11-04T18:37:31Z (its trailing tool-version lines came from shell wrappers; disregard).
- `subprocess-binary-identity-r64.txt`: subprocess-resolved binaries and GNU versions, run-utc 2026-11-04T18:37:56Z.
- `host-userland-identity-r64.txt`: superseded (wrapper names; not instrument identity).
- `s094-negative-phrase-counts-r64.txt`: phrase counts and line anchors in the S094 capture.
- `S094-committed-capture-d74be00.txt`: committed S094 capture copy (sha256 663ac16d…), the source of the anchor line numbers.
- `probe-ledger.json`: the ten-figure fixture ledger used for base recon.

## Out of scope

Coverage, source restoration, new knowledge entries, frontier, promotion, SHONEN box changes, exploitability, severity, bounty or submission, live-target testing, all-error/sandbox/signal guarantees, sibling or domain source trees, other seats' probes. No external domain coverage was added.

## Self-evaluation

Accuracy 4: every quoted line checked against committed bytes or the live page; the wave expectation error and my own wrapper contamination are disclosed. Completeness 4: S097 row, Gate, trial proposal, both corrections and the M64 rows drafted. Clarity 4: receipts separated from inference. Actionability 4: L1 has exact row, figures and kill rules; a candidate run is still needed. Conciseness 3: the artifact set is larger than the single file requested, but each piece is a draft L1 can accept or drop. Mean 3.8. The main caveat: the S097 candidate table is inference until L1 runs the candidate on committed bytes.

Report: .ufo/waves/round-64/w1/SourceLedger.md
