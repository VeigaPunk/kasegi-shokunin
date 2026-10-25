## Live run on the real map — measurement 1 (before the real F11 row landed)

Measured at the start of this seat's session, when the working-tree
`corpus/README.md` still had exactly 10 admitted frontier rows (F01–F10).

Command: `python3 corpus/instruments/frontier-recheck-count.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --json .ufo/waves/round-26/wave1/e8-live-receipt.json`

- Exit: **0**.
- Per-row records: F01 1, F02 1, F03 1, F04 1, F05 1, F06 1, F07 1, F08 1,
  F09 2, F10 2 → 12 records; all 12 PASS (each printed line carries its frontier
  id, header `source:` ids and `exit=0`). Full stdout in `e8-live-receipt.json`
  and `e8-frontier-sim.txt`.
- Summary line: `entries=12 pass=12 exit=0`.

## Live run on the real map — measurement 2 (AFTER the real F11 row landed)

During the same session the real `corpus/README.md` gained an uncommitted F11
row (scribe w4 / C2 adoption work in flight; verified NOT to be this seat's
placeholder — `grep -c 'PLACEHOLDER frontier row' corpus/README.md` = 0):

```
| F11 | ISO/IEC 29147/30111 division-of-labour meta | admitted | knowledge/iso-29147-and-30111-division-of-labour-2026-10-23.md, knowledge/iso-29147-divergence-and-clause-crosswalk-2026-10-23.md | S041 | ... |
```

Re-run of the identical command against the live root:

- Exit: **1** — uncaught traceback (`FileNotFoundError` at
  `frontier-recheck-count.py:65` for
  `corpus/knowledge/iso-29147-and-30111-division-of-labour-2026-10-23.md`),
  no summary line, no JSON receipt written. Verbatim output in
  `e8-live-after-f11.txt` / `e8-live-receipt-after-f11.json` (receipt absent
  because the crash precedes the `--json` dump).
- The two F11 entry files currently exist ONLY in the read-only assimilation
  package (`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/`),
  not in `corpus/knowledge/` (verified: no `iso-29147*` file anywhere in the
  lane, including `.ufo/waves/round-26/`).

This is the live manifestation of the simulation-B hazard: the F11 row is
admitted before its entry files are landed, so the instrument breaks with a
traceback instead of reporting a clean verdict.

## How the instrument counts entries per frontier row

The instrument is pure-read over `corpus/README.md` plus per-entry geometry:

1. `read_frontier(root)` parses `<root>/corpus/README.md` line-by-line with
   `FRONTIER_ROW = ^\|\s*(F\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`?([^|`]+?)`?\s*\|`
   capturing `(id, topic, status, entry_cell)` in README order.
2. `main()` selects only rows whose status cell is exactly `admitted`.
3. Each admitted row's entry cell (4th column) is split on `,`; every part is one
   entry path resolved relative to `<root>/corpus/` (e.g. `knowledge/foo.md`).
4. Each entry is evaluated against the R12 contract: the `recheck:` line must be a
   `source-recheck.py` invocation with `--manifest` and `--source` ids that
   (A) cover the entry's own header `source:` ids, (B) are all listed by a
   schema-valid manifest, (C) are cited by the entry body; only then is the line
   executed from the lane root and its exit code is the entry's result. PASS = no
   problems and exit 0.
5. The summary line prints `entries=<total records across admitted rows>
   pass=<N> exit=<0 iff N==records and records nonempty, else 1>`; exit 2 on
   harness/read error.

So the per-row contribution is exactly 1 record per comma-separated entry path in
an admitted row's entry cell. Rows with multiple entries (F09, F10 today) add one
record per entry; non-admitted rows (any status other than `admitted`) contribute
nothing.

## Simulation A (assigned) — future F11 row as a copy of an existing admitted row

Scratch: `.ufo/waves/round-26/wave1/e8-scratch/` = byte-copy of the lane's
`corpus/` + one inserted row. Verified by `diff` that the ONLY difference from
the real `corpus/README.md` is the inserted line:

```
| F11 | PLACEHOLDER frontier row — temporary copy of F10 for frontier-recheck-count simulation | admitted | knowledge/vendor-disclosure-policies-as-corpus-objects.md, knowledge/vendor-disclosure-policy-commitments-crosswalk.md | S036, S037, S038, S039, S040 | PLACEHOLDER next cell — not a real admission. |
```

Run against the scratch root. Results:

| metric | before (live) | after (scratch A) |
|---|---|---|
| entries | 12 | **14** |
| pass | 12 | **14** |
| exit | 0 | **0** |

The two new records are the F11 copies of F10's entries, both PASS. All 12
pre-existing records remain PASS. **Verdict: an admitted F11 row whose entry
files exist integrates cleanly — the instrument reads it, counts 1 record per
entry path (2 for a two-entry row), and exits 0; no code change needed.**

## Simulation B (probe) — F11 admitted before its entry file exists

Same scratch, except F11's entry cell names `knowledge/f11-placeholder-theme.md`
(a file that does not exist). Run exits **1 with an uncaught traceback**
(`FileNotFoundError` at `frontier-recheck-count.py:65`, raised from
`entry_contract` via `evaluate` → `main`), prints **no summary line**, and writes
**no JSON receipt** (the crash precedes the `--json` dump). Verbatim traceback in
`e8-scratch-b-run.txt` and `e8-frontier-sim.txt`.

**Integration hazard:** if the future F11 row is admitted before its knowledge
entry file(s) are landed — or the entry path is mistyped — this instrument breaks
with a traceback instead of reporting a per-row FAIL or harness exit 2. For C2
adoption, land the entry file(s) first, then admit the F11 row; a defensive
improvement would resolve the entry path inside `evaluate()` and emit an
`entry-file-missing` FAIL problem rather than raising.

## Simulation C (probe) — F11 present but not yet admitted (status `staged`)

Same F11 row with status cell `staged`. Run exits **0**; output is identical to
the live run (`entries=12 pass=12 exit=0`). A not-yet-admitted F11 row is ignored
by the admitted filter and adds 0 records — no break.

## Evidence retained (all under `.ufo/waves/round-26/wave1/`)

- `e8-live-receipt.json` — measurement 1 JSON receipt (12 records, 12 pass,
  exit 0).
- `e8-live-after-f11.txt` — measurement 2 stdout with verbatim `FileNotFoundError`
  traceback (no JSON written because the crash precedes the `--json` dump).
- `e8-scratch-run.txt`, `e8-scratch-receipt.json` — simulation A stdout + JSON
  (14 records, 14 pass, exit 0).
- `e8-scratch-b-run.txt` — simulation B stdout with verbatim `FileNotFoundError`
  traceback (no JSON produced).
- `e8-scratch-c-run.txt`, `e8-scratch-c-receipt.json` — simulation C stdout + JSON
  (12 records, 12 pass, exit 0).
- `e8-frontier-sim.txt` — consolidated simulation outputs receipt (both live
  measurements, before/after counts, exits, per-row counts, the three variants,
  and the diff proof of the single-line scratch mutation).
- Scratch corpus trees were removed after capture; the only README change in every
  variant was the one F11 row.

## Files changed by this seat

- `.ufo/waves/round-26/wave1/ExecFrontierSim.md` (this report).
- `.ufo/waves/round-26/wave1/e8-frontier-sim.txt` (simulation outputs).
- Scratch trees under `wave1/` (created and removed for the simulation).
No real corpus file, no claims file, no lesson, and no instrument was modified.

## Risks / blockers

- None blocking this seat's deliverable. The milestone finding is **live**:
  measurement 2 shows the real F11 row was admitted in `corpus/README.md`
  before its two knowledge entry files exist, so `frontier-recheck-count.py`
  currently crashes on the live map (exit 1, `FileNotFoundError`, no summary).
  The instrument integrates the F11 row correctly once those entry files exist
  (proven by simulation A: 14/14, exit 0). Recommended C2 ordering: land
  `knowledge/iso-29147-and-30111-division-of-labour-2026-10-23.md` and
  `knowledge/iso-29147-divergence-and-clause-crosswalk-2026-10-23.md` (from the
  assimilation package) before the row stays admitted; optionally harden the
  instrument to report an `entry-file-missing` FAIL instead of raising.
