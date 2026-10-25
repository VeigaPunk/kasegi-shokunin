# ExecReceiptCanonC2 — round-28 wave 1 (coverage / C2 canonical receipt block)

Seat: `ExecReceiptCanonC2` (executor, axes=coverage). Read-only on production: no production
file was edited. The single deliverable is the canonical **C2 receipt block** draft plus the
re-runnable emitter that produces it from executed observations.

- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `c9f8b115a098c65356e4b3b6048af45a37ab8395`.
- Collection window: 2026-10-25T17:22:41Z → 17:27:56Z (UTC).
- State: **POST-STATE** — every frozen C2 after value was reached and measured (the F12 entry
  landed between 17:25:48Z and 17:26:24Z, after the registry and README appends).

## Files written (all non-production)

| Path | Role |
|---|---|
| `.ufo/waves/round-28/receipts/ExecReceiptCanonC2.txt` | canonical C2 block draft + ledger + findings |
| `.ufo/waves/round-28/wave1/ExecReceiptCanonC2.md` | this report |
| `.ufo/waves/round-28/wave1/ExecReceiptCanonC2/emit-c2-block.sh` | emitter of record (self-verifying, fail-closed) |
| `.ufo/waves/round-28/wave1/ExecReceiptCanonC2/emitter-run-poststate.txt` | the 33-line block, verbatim |

No `c1-receipt-index.txt` or any canonical file was created under `.ufo/waves/round-28/` root —
verified: the root listing still holds only `census-before.txt` (defect 4 preserved). No VCS write,
no subagent, no background job, no tool install (python3 + coreutils sufficed).

## The canonical block

33 lines, emitted at 17:27:13Z, embedded byte-identically in the receipt (`diff` exit 0 against
the saved run):

```
frontier_admitted_before=11   -> frontier_admitted_after=12
entries_citing_S042_before=0  -> entries_citing_S042_after=1
sources_rows_before=41        -> sources_rows_after=42 ; s042_rows_after=1
census_exit_after=0           (census_findings=W04:2 E11:0)
frontier_harness_before=entries=14 pass=14 exit=0
frontier_harness_after=entries=15 pass=15 exit=0 (pass_lines=15 harness_exit=0)
manifest_sha256=e62ddad133ffc19ebc66822c0fcb3b48ed4993c101f05262302acc58714f291d
manifest_path_stem_ok=True pairs=S041->S041.txt S042->S042.txt
s041_capture_sha256=e18acbf9…f5ab47   s042_capture_sha256=b432ec16…c96966
s041_recapture_vs_round26=IDENTICAL
source_recheck_S041_exit=0            source_recheck_S042_exit=0
q9_assertions=unique=12 anchored_ok=0 bad=0 total_pinned=12
entry_header_and_recheck=declared=S041,S042 recheck=S041,S042 equal=True recheck_lines=1
c2_after_reached=yes
```

Each line is followed by a `# source:` pointer naming its instrument or receipt. The emitter
exits 0 only when all seven after conditions hold; an earlier run at 17:25:41Z (entry absent) did
exit 1 with `entries_citing_S042_after=0`, `census_exit_after=1` and a `FileNotFoundError`
harness line — the fail-closed path was exercised, not assumed.

## Cross-block constraint (why this block is safe to append to the C1 index)

C1's counter (c) greps the ONE canonical file for exactly one `selftest cases=` line and exactly
one `instrument_sha256=[0-9a-f]{64}` match. Measured on the emitted block:
`grep -cE 'selftest cases='` → **0**; `grep -oE 'instrument_sha256=[0-9a-f]{64}' | wc -l` → **0**.
`manifest_sha256=` occurs once and is a distinct token, so it cannot collide.

## Two limbs no instrument tests, measured here

1. **Q9 stem == id**: `source-recheck.py` checks a relative path, its sha256 and the quotes, but
   never the path stem (`source-recheck.py:116-150`). Measured independently: `stem_ok=True` for
   both records; carried as `manifest_path_stem_ok=True` in the block.
2. **Recheck id equality**: the frontier harness tests `declared ⊆ recheck` and `recheck ⊆ cited`,
   not equality, which is what C2's predicate states. Measured from the entry bytes:
   `declared=S041,S042 recheck=S041,S042 equal=True recheck_lines=1`. The line is also
   cwd-independent: `bash -n` exit 0 and a run from `/` exited 0.

## Grounded findings (reported, not patched — no ownership)

- **F-1** `frontier-recheck-count.py` raises an uncaught `FileNotFoundError` and prints no
  `entries=` line when an admitted row names an absent entry (reproduced mid-wave at 17:25:07Z,
  `harness_exit=1`). A partial landing is therefore indistinguishable from an instrument error,
  and the canonical index cannot record `entries=15 pass=14`.
- **F-2** the census is entry-order-sensitive: with README+SOURCES+manifest landed and the entry
  absent it exited 1 on `E11 S041/S042 missing used-by …`; after the entry landed it exited 0
  with only the pre-existing `W04` S028/S029 duplicate-URL warnings. Assembly must run after the
  entry lands.
- **F-3** Q9's stem-equals-id limb has no gate (see above).
- **F-4** the harness's `entries=` counts admitted **rows**, not frontier ids (F09/F10/F11 carry
  two rows each), so `entries=15` is rows+1 while `frontier_admitted=12` is ids.
- **F-5** `source-recheck.py`'s `MIN_QUOTE_CHARS=12` fired mid-build on ExecManifest's first
  digest `fa1f366f…` (`S042:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence`); the landed
  digest `e62ddad1…` pins the step body line. Re-verified 12/12 `OK occurrences=1`, `bad=0`.

## Drift and re-run

A re-run at 17:27:56Z differed from the saved 17:27:13Z run only in `measured_utc` — no value
moved. The L1 must still re-run at the final landed digest, because `manifest_sha256`,
`entry_header_and_recheck` and the three append-count lines can change if a scribe edits after
this seat:

```
bash .ufo/waves/round-28/wave1/ExecReceiptCanonC2/emit-c2-block.sh ; echo "emit_exit=$?"
# require emit_exit=0 and last line `c2_after_reached=yes`; then paste the 33 lines verbatim.
```

Then re-check the two C1-side greps on the assembled file (both must stay 1).

`claims-erratum-1.md` (appended by the L1) supersedes only C1's `corpus_disclosure` annotation; it
moves no C2 counter, so no line in the block changes. C2's predicate never referenced the bounties
arm that the erratum corrects.

## Risks / blockers

None blocking. Residual risk is staleness, not correctness: the embedded block is valid for the
tree as of 17:27:13Z and is explicitly marked for re-take. No credential, session or private URL
material was read or written.
