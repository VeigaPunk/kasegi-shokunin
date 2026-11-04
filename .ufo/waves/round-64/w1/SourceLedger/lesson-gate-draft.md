# Round 64 — draft `## Gate` block (SourceLedger proposal; L1 applies or rejects)

Not applied to `corpus/lessons/round-64.md`. Every located quote below was read from committed bytes or a live page on 2026-11-04 and is ≤25 words (counted with `wc -w`, receipt `native-exit-and-anchor-recon-r64.txt`).

## Gate

**S097 — own-work/A, opened 2026-11-04.** Committed base `d74be00a82c8c2962a0b78442c5daea3af0adaae`, `corpus/instruments/figure-audit.py` (sha256 `15bcb6c4fbaaa23c2b85e480dff9b9af52e43442de64661f222d8868dd73b997`). Located: L42–L43 “Upstream exit1 and negative signal statuses remain” / “ignored, preserving grep|wc zero-count derives”; L107 “if p.returncode > 1:”. Receipts: `base-probe-recon-r64.txt` (run-utc 2026-11-04T18:37:31Z) shows `ls` and `sort` missing already stale at base with derive-upstream-exit-2, not green. Scope: local instrument rule only.

**S098 candidate (spec; L1 registration decision) — POSIX, fetched 2026-11-04.** `pubs.opengroup.org/onlinepubs/9699919799/utilities/grep.html`, EXIT STATUS: “No lines were selected.” (exit 1); “An error occurred.” (exit >1). `…/utilities/cat.html`, EXIT STATUS: “All input files were output successfully.” (0); “An error occurred.” (>0, numeric value unspecified). Teaches: grep exit1 is a defined no-match; cat exit1 is a host value, not a spec value. Edition read: Issue 7, 2018; a newer edition link exists and was not used.

**S094 — domain (publisher account), reopened 2026-11-04 18:35Z via live reader and pinned capture.** Live: “we found this issue before it appeared in an official release, so SQLite users were not impacted.” (capture `corpus/source-snapshots/round-61/S094.txt:18`). Conclusion: “However, we want to reiterate that these are highly experimental results.” (capture L118). Attribution stays with the publisher; no reproduction.

**Correction, append-only (r63 S096 placement).** S096's dated provenance sat at `corpus/lessons/round-63.md:37`, under “Frozen claim and integrated evidence”, not under `## Gate`. The r63 closure recorded this at `round-63-verifier-spotcheck.md:15,79`. Restated here; the filed lesson is not rewritten. Verified at base by `grep -n -F 'if p.returncode > 1:'` → line 107 (inside the S096 citation range 106–109).

**Correction, append-only (r63 missing-input closure, M63-7).** The frozen `.ufo/waves/round-63/controls/verify-r63.py` PATHS list has eight entries and omits four ledger-declared receipts: `round-55/controls/gate-final-r55.txt`, `round-56/controls/df3-fixedpoint-r55tip.txt`, `round-53/controls/c2-counter-final-r53.txt`, `round-56/controls/gate-final-r56.txt`. All four exist at base (`git cat-file -e`). The nonclaim supplemental (`supplemental-verification-r63.txt`, run-utc 2026-11-04T18:15:39Z, revision 204a627b…) lists them at INPUT lines 12–15 and reads ledger35/35. Static check only: `verify-r64.py` PATHS (lines 18–25) now contains them, plus S086 and the collector; no dry run performed here.

## Mistakes (proposed rows; L1 assigns captured-by and dispositions)

| id | class | evidence | captured-by | fix / disposition |
|---|---|---|---|---|
| M64-4 | stale-premise | `base-probe-recon-r64.txt` (ls, sort rows, exit2 → derive-upstream-exit-2 at base) | L1 to assign | Wave-prompt expectation "base greens want0" is wrong for `ls` and `sort`; they are base-stale controls. Expected table restated in S097-row-draft.md. |
| M64-5 | unlocated-constant | `.ufo/waves/round-64/domain-qualification.py` ARITHMETIC rows compute `index = column - 1`; capture L51 names `SERIES_COLUMN_START` but no value appears in the capture (grep count of the name = 1, value absent) | L1 to assign | Those four rows assert a Python-derived index, not a located source value. Replace or anchor before any trial claim uses them. |
| M64-6 | receipt-identity | my first version receipt used shell names, which the persistent shell resolves to wrapper functions (printed `uu 0.8.0`, `pi-uu-grep 0.2.0`) | self-caught by SourceLedger | Superseded by `subprocess-binary-identity-r64.txt` (GNU coreutils 9.12, GNU grep 3.12 at /usr/bin) and `native-exit-absolute-paths-r64.txt`. Earlier raw files kept, not used as identity evidence. |

## Assimilation and retained boundaries (proposed text)

Assimilation: none. considerthese `2026-10-26.md:30` (proposal 2) is mined only as a bounded disclosed-finding qualification design (see `trial-proposal-r64.md`), not a six-file claim package; SHONEN box 2 stays unchecked. No candidate scoring before L1 freezes; the S097 candidate expectations above are inference, not measurements.
