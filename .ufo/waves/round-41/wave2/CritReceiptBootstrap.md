# CritReceiptBootstrap — I2 seed at judged head

Seat: `CritReceiptBootstrap`, round-41 FALSIFY wave 2. Scope: compare the C1 suite at integrated judged-head candidate `ad7147532cb702b0d541d40499874552183d9132` with and without `--receipt-out`, inspect I2 bootstrap behavior, and test transcript stability. This is not final Y. No files outside this report and seat scratch were written; no mutating git/jj command was used; no tools installed.

## Finding

**The output transcript is byte-identical to the file written by `--receipt-out`, but this probe does not demonstrate a green receipt bootstrap or Y-only verification.** Both runs exited 1 (`closed=10/12 exit=1`), primarily because this candidate's live scratch scan sees three strays (`I6 payload=strays=3,read=fail,scanned=3`) and I2 cannot validate its receipt transcript (`cmp=0`). With `--receipt-out`, I2 advances from a missing-receipt shape to a seeded receipt shape (`receipt=1`, `payload-match=11/11`, `ancestor=1`, `diff-clean=1`) but remains red: `selftest-verdicts=8`, `summary=0`, `closed-line=0`, `cmp=0`, `i2-line=0`. The selftest's I1/I2/I3/I6 positives fail in this host/live-scratch condition; overall `selftest cases=12 failures=6`. These are reproduced outcomes at the requested integrated ref, not claims about the later final ref.

## Exact reproduced transcript facts

Commands executed with lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, `--export-ref ad7147532cb702b0d541d40499874552183d9132`, separate work directories under `/fast/scratch/hyaku/kasegi-r41/CritReceiptBootstrap/work`, and `--scratch-root /fast/scratch/hyaku/kasegi-r41/CritReceiptBootstrap`:

- Without `--receipt-out`: exit 1; header `export-ref=ad7147532cb702b0d541d40499874552183d9132`, `suite-sha256=3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd`, `run-utc=2026-10-27T11:35:28Z`; I2 was `receipt=0,sentinel=0,ref=,digest=0,time-basis=0,run-utc=0,not-future=0,header-lines=0,run-lines=0,selftest-lines=0,selftest-verdicts=0,summary=0,closed-line=0,payload-match=0/11,ancestor=0,diff-clean=0,diff-read=ok,i8-match=0,cmp=0,i2-line=0 closed=0`.
- With `--receipt-out <seat-scratch>/receipt.out`: exit 1; I2 became `receipt=1,sentinel=1,ref=ad7147532cb702b0d541d40499874552183d9132,digest=1,time-basis=1,run-utc=1,not-future=1,header-lines=5,run-lines=12,selftest-lines=12,selftest-verdicts=8,summary=0,closed-line=0,payload-match=11/11,ancestor=1,diff-clean=1,diff-read=ok,i8-match=1,cmp=0,i2-line=0 closed=0`.
- `cmp -s with-receipt.out receipt.out` returned 0; both were 2,481 bytes. Thus the file is byte-identical to the run's stdout, including its red results. This is evidence of output/file equality, not the frozen green receipt criterion.
- Both full transcripts showed I6 strays=3/read=fail/scanned=3, and both ended `selftest cases=12 failures=6` then `closed=10/12 exit=1`. Selftest case lines for I1, I2, I3, I6 had `positive=fail`; the other eight case lines passed.

The tool transcript was preserved during the probe in scratch, then scratch was removed before filing as required. No final Y run was performed.

## I2 bootstrap assessment and smallest safe correction

The source documents the seed/fixed-point design at `corpus/instruments/r41-closure.sh` lines 160-166; `receipt_source` lines 673-691 selects the committed export receipt if present, otherwise the canonical seed; `run_suite_report` lines 2041-2076 writes the assembled transcript and re-derives I2. Observed behavior is consistent with this bootstrap intent: `--receipt-out` lets I2 inspect the newly seeded output instead of reporting a completely absent receipt, while the no-output run cannot pass I2 when the export contains no committed receipt.

However, the output run does not establish successful I2 closure or transcript stability *for a green transcript*: its receipt is byte-stable against stdout, yet it is red and not a canonical accepted I2 receipt (`cmp=0`). This distinction matters for **depth:verifiability** and **coverage**. Smallest safe correction to the claim/evidence is to retain the bootstrap mechanism but require a clean-scratch probe with a path arrangement that satisfies I6, then demonstrate a successful 12/12 transcript generated at J, receipt bytes equal to stdout, and (after the receipt-only Y commit exists) a Y export run producing byte-identical output and `I2 ... cmp=1,i2-line=1 closed=1`. Do not characterize this candidate-ref run as proving the Y-only receipt contract. The frozen criterion itself requires the teed transcript equality; this probe only confirms equality for a failed transcript.

Scratch `/fast/scratch/hyaku/kasegi-r41/CritReceiptBootstrap/` was removed before filing. Disk guard was run before the probes and reported `/fast/scratch/hyaku` at 39% use, 492.1G free. No tools installed.
