# R47ScoutS076Live — S076 live reopen

Axes: depth:verifiability (independent retrieval and byte equality); coverage (all twelve manifest quotations).

## Observed findings — high confidence

Two concurrent, independent executions from the lane cwd of:

```text
python3 corpus/instruments/capture-source.py --id S076 --url https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories --kind html --out /fast/scratch/hyaku/kasegi-r47/R47ScoutS076Live/live-{1,2}.txt
```

Both exited 0 with empty stderr and printed `status=200 fetched_bytes=582877 snapshot_bytes=19804 sha256=9bd8ab57dac9cc605355c60831f51e02b92f5e34990aa99a49566d207e6bbb38 utc=2026-10-30T11:42:43Z`. Each normalized capture has 610 lines. Full individual argv/stdout and comparison results: `.ufo/waves/round-47/w1/R47ScoutS076Live.draft/receipt.json`.

Both live normalized captures are byte-for-byte equal to each other and to `corpus/source-snapshots/round-47/S076.txt`; independently computed committed SHA-256 equals the supplied pin and manifest SHA-256 (`manifest.json:88`). The normalization/output contract is `capture-source.py:82-97`; command arguments are defined at lines 120-132.

Every quote was independently located by searching every line for the manifest's literal quotation, not by assuming its recorded anchor. Each quote has exactly one hit per capture. Manifest records: `corpus/source-snapshots/round-47/manifest.json:97-157`.

| Quote | Committed anchor | Live 1 | Live 2 | Drift |
|---|---:|---:|---:|---:|
| Q1 | 568 | 568 | 568 | 0 |
| Q2 | 571 | 571 | 571 | 0 |
| Q3 | 575 | 575 | 575 | 0 |
| Q4 | 582 | 582 | 582 | 0 |
| Q5 | 583 | 583 | 583 | 0 |
| Q6 | 583 | 583 | 583 | 0 |
| Q7 | 584 | 584 | 584 | 0 |
| Q8 | 589 | 589 | 589 | 0 |
| Q9 | 596 | 596 | 596 | 0 |
| Q10 | 598 | 598 | 598 | 0 |
| Q11 | 599 | 599 | 599 | 0 |
| Q12 | 600 | 600 | 600 | 0 |

Exact live evidence: `.ufo/waves/round-47/w1/R47ScoutS076Live.draft/live-1.txt` and `live-2.txt` at the table's line numbers; committed evidence: `corpus/source-snapshots/round-47/S076.txt` at those same lines. `committed-vs-live.diff` contains no diff hunks.

## Control and interpretation

Do-nothing control: existing committed S076 bytes and recorded anchors, with no retrieval. This control already contains all twelve quotations, so quote presence alone does not establish a live re-open. The distinguishing observations are two actual capture-source subprocess executions with HTTP 200 receipts, independent output paths, and byte comparisons after retrieval. The live results reproduce, rather than improve or modify, the control. No frozen C1/C2 counter was run; this is scoped provenance evidence, not a claim that either complete gate or mutant battery passes.

Inference: S076's normalized content and all twelve anchors were reproducible at the observed instant. This supports the superseding capture provenance; it does not establish perpetual stability.

## Limitations and operational record

- Same-second requests are not a longitudinal stability test; upstream/cache behavior and future page drift remain unknown.
- Compared normalized captured text, not archived raw HTML bytes. The instrument reports raw byte count but does not preserve raw response bytes or final redirect URL in its receipt.
- LSP device unavailable (`read xd://lsp` returned `No such tool`); literal source inspection only, not semantic reference proof. No exported contract was changed.
- Disk guard printed `/fast/scratch/hyaku 54% 376.3G`, `/tmp 25% 96.8G`, `/var/tmp 41% 532.8G`; its subsequent top-consumer enumeration timed out after 30 seconds. No heavy pass, clone, counter, or battery was run.
- No installs, commits, git/jj mutations, or production-file edits. Scratch was removed in a Python `finally` block; printed `scratch_removed=True` after copying evidence here.

Report: .ufo/waves/round-47/w1/R47ScoutS076Live.md
