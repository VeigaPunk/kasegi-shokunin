# R47RevD7 — D7 fix-shape review

Axes: depth:verifiability; coverage. Recommendation only; no admission/integration performed.

## Findings by severity

### High — S074 rejection breaks the retained capture's binding

`R47ExecS074Flip.md:17-20` proposes `mined` → `rejected` while retaining the historical row/capture. `corpus/instruments/capture-binding-check.py:327-339` explicitly rejects a manifest record anchored to a rejected row (rule B3). The retained record is `corpus/source-snapshots/round-46-a2/manifest.json:5-18`.

Bounded probe copied the actual round-46-a2 and round-47 snapshot directories into an isolated fixture, supplied their three registry IDs, and changed only S074's status between arms. Do-nothing control: `records=3 bound=3 unbound=0`, `EXIT=0`. Rejection arm: `FAIL rule=rejected-row-anchor record=S074 row=S074 dir=round-46-a2`, `records=3 bound=2 unbound=1`, `EXIT=1`. Full argv/output: `.ufo/waves/round-47/w1/R47RevD7.receipts.txt`. Fixture S075/S076 rows are minimal bindings, not proposed production rows; the failure concerns S074 only.

Census success is not a counterargument: the flip seat's census receipt (`R47ExecS074Flip.md:22-28`) checks a different contract. The rule-2 successor does not require rejecting its predecessor (`/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`). Recommendation: preserve S074 as mined historical evidence, point used-by to the lesson that actually cites it, log that permitted cell change, and explicitly supersede current guidance via S076. Do not delete/rewrite the old pinned manifest or relax B3 merely to green this change. The executor was notified and acknowledged this integration blocker.

### Medium — proposed rejected row lacks required rejection semantics

The exact proposed row (`R47ExecS074Flip.md:10`) leaves `teaches` as positive maintainer advice despite status `rejected`. The contract requires rejected rows to read `REJECTED: <reason>; flip: <what would change the verdict>` (`CORPUS.md:101-104`). The report's external rejection explanation at line 20 does not populate that cell. Keeping the historical row mined resolves this as well as B3; editing teaches in place instead would violate append-only rule 2.

## Reproducibility and supersession evidence

- Two actual `capture-source.py --id S076 --url <canonical URL> --kind html --out <explicit seat scratch file>` executions returned HTTP 200, `fetched_bytes=582877 snapshot_bytes=19804`, SHA-256 `9bd8ab57dac9cc605355c60831f51e02b92f5e34990aa99a49566d207e6bbb38`, at 2026-10-30T11:43:48Z and 11:43:49Z. Both exit 0; both equal the manifest pin. This discriminates against merely reading the existing snapshot (the do-nothing capture control). Full receipts are preserved above.
- `source-recheck.py` on S076 returned `S076:sha256 OK` and all twelve Q1–Q12 OK, exit 0. S074 likewise returned SHA OK and all nine quotes OK, exit 0. Commands and full output: `.ufo/waves/round-47/w1/R47RevD7.history-receipts.txt`.
- Historical S074 and its manifest still hash respectively to `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039` and `46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f`, exactly the round-46 attempt-2 freeze pins (`.ufo/waves/round-46/attempt2/freeze.txt:6-7`). Keep them byte-identical. Local captured-evidence replay remains reproducible; S074's original reader-style producing method remains unimplemented, and S076 does not retroactively reproduce it.
- The available candidate successor in `.ufo/waves/round-47/w1/R47RevCounterC1.draft/attack-A/corpus/SOURCES.md:82` literally opens teaches with `supersedes S074 —`, satisfying the rule-2 prefix. Its capture path, hash, body 558–600 and twelve anchors agree with the checked manifest. This is a counter-review fixture, **not** final integration evidence. The named Registry seat confirmed it owns S075 only; final S076 diff was requested from R47SrD5Diff.
- The counter's check is weaker than rule 2: `r47-routed-defects.py:243` only checks `startswith("supersedes S074")`, not the required em dash. Check the actual final row, not merely L8 green.

## Residual risk and verification gaps

- The round-46 F29 gate is era-bound after the intended recapture: it requires the S074 provenance header/recheck (`r46-f29-gate.py:18-21,207-210`), old citation names, and mined S074/knowledge used-by (`:269-275`). Re-anchoring to S076 deliberately invalidates its current-tip reading; do not claim every r46-era gate stays green. Historical frozen-tree replay is distinct. I did not rerun the frozen era counter or full mutation battery.
- Successful capture reproduction applies to normalized text at the observed instants, not perpetual upstream stability, raw HTML byte identity, original fetch timestamp, or the entire manifest. `capture-source.py:73-97` prints status/count/digest/time but does not record final redirect URL or preserve raw HTML. Its own contract explicitly disclaims future byte stability (`:15-18`). The manifest's 'deterministic' wording must be read in that bounded sense.
- No final integrated row/diff existed at initial inspection; this review covers the available proposal and actual manifest, not a claimed integrated-tree pass. Census conformance is supported by the flip seat's bounded control, not independently rerun here. No C1/C2 full pass or mutant closure is claimed; the disclosed 34 pre-freeze survivors remain gaps.
- LSP unavailable: `read xd://lsp` returned `No such tool`; references/definition/diagnostics could not be run. Literal source inspection and scoped subprocess probes are not semantic-reference proof.
- Disk guard printed `/fast/scratch/hyaku 54% 375.3G` free (`/tmp 96.7G`, `/var/tmp 532.8G`) before its consumer enumeration timed out at 30s. Only small scoped fixtures followed. No installations, background jobs, delegation, git/jj mutations, or production edits. Seat scratch removed in Python `finally` after receipts were saved.

Self-evaluation: accuracy 4 (exact probe receipts; final diff unavailable), completeness 4 (all D7 questions covered; integrated verification remains L1's), clarity 4 (separates binding/census/local replay), actionability 4 (preserve historical mined row and pins), conciseness 4 (full receipts externalized); overall 4.0. Highest-impact remaining check: final-row rule-2 prefix plus integrated capture-binding audit after disposition is corrected.

## Delivered-diff addendum

After initial submission, R47SrD5Diff supplied `.ufo/waves/round-47/w1/R47SrD5Diff.draft/patched-SOURCES.md:82`. I read that exact S076 row: its teaches literally begins `supersedes S074 —`; the capture path/hash, prose 558–600, and twelve anchor numbers match the manifest and independently reproduced capture. Thus the actual delivered draft satisfies the supersession-prefix requirement, not just the earlier reviewer fixture. Integration is still unverified. The diff author confirms the rejected-S074/B3 conflict is preserved in their report for L1; both findings above remain actionable.

Report: .ufo/waves/round-47/w1/R47RevD7.md
