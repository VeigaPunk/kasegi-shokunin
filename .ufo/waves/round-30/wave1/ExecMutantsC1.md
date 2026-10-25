# ExecMutantsC1 — C1 mutant matrix (round 30, wave 1)

Seat: `ExecMutantsC1` (executor, L2 leaf). Role: after the instruments were updated, create
the four isolating mutants of the landed C1 instruments, run the frozen fixtures, and re-run the
four probes from the freeze-commit bytes as the do-nothing control.

Measured bytes (sha256), worktree at mutant-construction time (2026-10-25, ~18:52–18:55Z):

| instrument | sha256 | note |
|---|---|---|
| `corpus/instruments/frontier-recheck-count.py` | `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` | landed (fixed) bytes; poll observed the change from base `c8a62888…` at 18:50:40Z |
| `corpus/instruments/source-recheck.py` | `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f` | landed (fixed) bytes; poll observed `0b841d5d…` at 18:50:40Z, later settled at `33602a9d…` (M29-6 digest drift observed during the wave; mutants snapshot the settled bytes) |

Freeze-commit instrument bytes (`git show 3c5573541300ba0fd3d89372dda3d841172eaa3f:…`) are
byte-identical to the base digests in `.ufo/waves/round-30/c1-controls/before.txt`
(`c8a62888…` / `9fe6a4a0…`); copies preserved at `mutants/freeze-frontier-recheck-count.py` and
`mutants/freeze-source-recheck.py`.

## 1. Do-nothing control — four probes at freeze-commit bytes (none meet the targets)

Commands run with `cwd = /home/vgpnk/Projects/shokunin/kasegi-shokunin` against the freeze-byte
copies; stdout/stderr/exit recorded to `mutants/control-*.out|err`.

| probe | command | exit | output | meets target? |
|---|---|---|---|---|
| A1 | `mutants/freeze-frontier-recheck-count.py --root …/harness-root-a1` | 1 | uncaught `FileNotFoundError` traceback (`entry_contract` line 65 `open(full,…)`); **no F98 named-row marker** | NO — target needs named-row marker, not traceback |
| A2 | `mutants/freeze-frontier-recheck-count.py --root …/harness-root-a2` | 0 | `PASS F98 … / PASS F97 … / entries=2 pass=2 exit=0` | NO — target needs exit 1 naming duplicate |
| B1 | `mutants/freeze-source-recheck.py --manifest …/q9/manifest-b1.json --source S043` | 0 | `S043:sha256 OK / S043:Q1 OK normalized=markup-whitespace occurrences=1` | NO — stem mismatch passes |
| B2 | `mutants/freeze-source-recheck.py --manifest …/q9/manifest-b2.json --source S045` | 0 | `S045:sha256 OK / S045:Q1 OK occurrences=2 anchor=MISSING` | NO — double occurrence passes |

All four reproduce `.ufo/waves/round-30/c1-controls/before.txt` line-for-line. Control cannot
meet the targets (confirmed).

## 2. Landed (fixed) instrument reference — four counters at current digests

| probe | exit | key output |
|---|---|---|
| A1 | 1 | `FAIL F98 knowledge/zz-missing.md ids=- exit=- problems=missing-entry`; `entries=1 pass=0 exit=1` |
| A2 | 1 | `PASS F98 … / PASS F97 …` + `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md`; `entries=2 pass=2 exit=1` |
| B1 | 1 | `S043:manifest MISMATCH reason=stem-mismatch` |
| B2 | 1 | `S045:manifest MISMATCH reason=stem-mismatch` |

Kill-rule clauses are satisfied by the landed bytes (A1 names F98; A2 names the duplicate; B1
has `reason=stem-mismatch`; B2 exits 1 with a failure reason). **Observation:** on the committed
B2 fixture `manifest-b2.json` (id `S045`, path `B2.txt`), the B1 stem limb fires before the B2
occurrence limb, so the fixed B2 output is `reason=stem-mismatch`, not
`reason=occurrence-not-unique`. See §4.

## 3. Mutants — creation, digests, and fixture flip results

Each mutant is a byte-copy of the landed instrument with exactly one new limb removed (verified by
`diff`; see §5). All four pass `python3 -m py_compile`.

| mutant | source copy | removed limb | sha256 |
|---|---|---|---|
| `mutant-a1.py` | frontier-recheck-count.py | A1 named-row gate (`if not os.path.isfile(full): return None` → uncaught `open()`) | `013dd1e537a439e1cb19f2cf9b44141c84190d799f8e3d016cd6eec5f0cfd5b5` |
| `mutant-a2.py` | frontier-recheck-count.py | A2 duplicate-realpath detection + `DUPLICATE-ENTRY` print + fail_closed conjunct | `5028f09e2ee8cb9d46c615adc15c2b4f8d5c8fce96b0f31ddbcbaf45d287a7bb` |
| `mutant-b1.py` | source-recheck.py | B1 stem==id check (`reason=stem-mismatch`) | `99073b1134480a8ae43fdc7699f1ddf3edb434985a80a517b59cc7ca09ff82cf` |
| `mutant-b2.py` | source-recheck.py | B2 non-unique-without-anchor failure (`reason=occurrence-not-unique` etc.) | `e12c8c7561de752f40605f78f304904de4117dc0c4e7e448b3f3544c09117db0` |

Fixture runs (stdout/stderr recorded to `mutants/mutant-*.out|err`):

| mutant | fixture | exit | output | FLIP? |
|---|---|---|---|---|
| mutant-a1 | A1 (`harness-root-a1`) | 1 | uncaught `FileNotFoundError` traceback at `entry_contract` `open(full,…)`; **no F98 marker** | **YES** — named-row marker gone, reverted to traceback |
| mutant-a2 | A2 (`harness-root-a2`) | 0 | `PASS F98 … / PASS F97 … / entries=2 pass=2 exit=0` | **YES** — duplicate undetected, exit 0 |
| mutant-b1 | B1 (`manifest-b1.json`, S043) | 0 | `S043:sha256 OK / S043:Q1 OK normalized=markup-whitespace occurrences=1` | **YES** — stem mismatch passes |
| mutant-b2 | B2 (`manifest-b2.json`, S045) | **1** | `S045:manifest MISMATCH reason=stem-mismatch` | **NO on the committed fixture** — see §4 |

## 4. Finding — committed B2 fixture does not isolate the B2 occurrence limb (R10)

`manifest-b2.json` names id `S045` with path `B2.txt`; `Path("B2.txt").stem == "B2" != "S045"`,
so the B1 stem limb (which runs before quote checking) fails the record first. Removing the B2
occurrence limb alone therefore cannot flip that fixture — the mutant still exits 1 via
`reason=stem-mismatch`. The B2 fixture as committed exercises the stem limb, not the occurrence
limb.

Supplementary isolation control (scratch fixture `mutants/b2iso/`, inside the lane; same double-occurrence
capture bytes `55124b0e…`, but named `S045.txt` so the stem matches):

| instrument | exit | output |
|---|---|---|
| landed `source-recheck.py` | 1 | `S045:sha256 OK / S045:Q1 MISMATCH reason=occurrence-not-unique` |
| `mutant-b2.py` | 0 | `S045:sha256 OK / S045:Q1 OK occurrences=2 anchor=MISSING` |

So the B2 limb **is** load-bearing and fails closed exactly as claimed once the stem matches; the
flip is real but is masked on the frozen fixture by the earlier stem limb. Recommendation for the
wave: the committed B2 fixture should either (a) be replaced by a same-stem capture
(`S045.txt` with the repeated quote) so it isolates B2, or (b) remain as-is and the B2 counter
evidence carries the stem-mismatch reason, with the occurrence-limb isolation proven by the
supplementary fixture above. This is a fixture-isolation defect to record (R10 class), not an
instrument defect.

## 5. Mutant diffs (against the landed bytes) — each removes exactly one limb

- `mutant-a1.py`: `78,79d77` — removes `if not os.path.isfile(full): return None` only.
- `mutant-a2.py`: `203,214c203` — removes `seen_realpath` scan loop, `DUPLICATE-ENTRY` print,
  and `duplicate is not None or` conjunct; leaves `duplicate = None` for the JSON receipt branch.
- `mutant-b1.py`: `123,126d122` — removes the stem-check block only.
- `mutant-b2.py`: `190,200d189` — removes the occurrence-check block only.

## 6. Scope / safety / tooling

- Writes: only inside the lane — `mutants/` (freeze copies, control outputs, mutant files,
  `b2iso/` scratch) and this report. No `git`/`jj` mutation (only read-only `git show`), no
  writes to fleet root, siblings, `/home/vgpnk/Projects/shokuknow`, `.ufo/state`, or MANIFEST.
- No tool installed/upgraded (none needed; operator RULES read).
- No live network contact; fixtures are documentation-only.

## Evidence on disk

`mutants/{freeze-frontier-recheck-count.py, freeze-source-recheck.py, control-a1.{out,err},
control-a2.out, control-b1.out, control-b2.out, mutant-a1.py, mutant-a2.py, mutant-b1.py,
mutant-b2.py, mutant-a1.{out,err}, mutant-a2.out, mutant-b1.out, mutant-b2.out, b2iso/}`.
