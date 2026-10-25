# Scout Instrument Baseline — C1 do-nothing control reproduction (round 30, wave 1)

Scout seat: ScoutInstrumentBaseline (L2, leaf). Assignment: reproduce the four C1 before
probes (A1/A2/B1/B2) from `claims.json` C1 `counter_commands` against the lane working tree at
the claims-freeze commit, confirm every value in `.ufo/waves/round-30/c1-controls/before.txt`
still reproduces, and explain why each baseline behavior is a conformance gap for claim C1.

## 1. Working tree measured (bytes labeled)

- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- `git rev-parse HEAD` at measurement time: **002e92ce07ed398334ef7cd8ca08d3fd99631351**
  (commit "round-30: wave-1 spec + dispatch", the child of the claims-freeze commit
  3c5573541300ba0fd3d89372dda3d841172eaa3f). `git status --porcelain` shows only untracked
  wave dispatch artifacts (`.ufo/waves/round-30/{assimilation,kasegi-r30-build.ready*,
  plan.err,run.err,wave1/swarm-registry.json}`); no tracked file is modified.
- Instrument digests at measurement (sha256):
  - `corpus/instruments/frontier-recheck-count.py`
    `c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261` — byte-identical to the
    frozen baseline digest recorded in `before.txt` (line 3).
  - `corpus/instruments/source-recheck.py`
    `9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96` — byte-identical to the
    frozen baseline digest recorded in `before.txt` (line 4).
  - These also match the "Baseline bytes at base a94871315" digests quoted in `claims.json` C1
    `do_nothing_control`. So although HEAD has advanced from base a94871315 / freeze 3c55735 to
    the spec commit 002e92ce, the instrument bytes and the C1 control fixtures are unchanged
    from the frozen receipt; the probes below measure exactly the frozen baseline bytes.
- C1 fixture tree present and unchanged: `.ufo/waves/round-30/c1-controls/harness-root-a1/
  corpus/README.md` (F98 admitted row naming `knowledge/zz-missing.md`, absent),
  `harness-root-a2/` (two admitted rows F98/F97 both naming `knowledge/dup-entry.md`),
  `q9/manifest-b1.json` (id S043, path S045.txt), `q9/manifest-b2.json` (id S045, path B2.txt).
  Committed capture `a1.err` matches the A1 run below line-for-line.
- Tooling installs this seat: none (no tool installed/upgraded).

## 2. Probe runs (exact counter commands from claims.json C1), with stdout/stderr/exit

All commands run with `cwd = /home/vgpnk/Projects/shokunin/kasegi-shokunin`; stdout and stderr
captured separately; exit captured immediately after the process.

### Probe A1 — missing-entry fixture (`harness-root-a1`)
Command:
`python3 corpus/instruments/frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a1`
- exit = **1**
- stdout = (empty)
- stderr = uncaught `FileNotFoundError` traceback:
  - `File ".../frontier-recheck-count.py", line 65, in entry_contract` → `with open(full, encoding="utf-8") as fh:`
  - `FileNotFoundError: [Errno 2] No such file or directory: '.../harness-root-a1/corpus/knowledge/zz-missing.md'`
- No occurrence of the row id **F98** anywhere in stdout/stderr. **Matches `before.txt` lines 6–12.**

### Probe A2 — duplicate-target fixture (`harness-root-a2`)
Command:
`python3 corpus/instruments/frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a2`
- exit = **0**
- stdout:
  - `PASS     F98  knowledge/dup-entry.md                               ids=S003           exit=0   `
  - `PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0   `
  - `entries=2 pass=2 exit=0`
- stderr = (empty). **Matches `before.txt` lines 14–17 (pass=2 on duplicate target).**

### Probe B1 — stem-mismatch order (`q9/manifest-b1.json`)
Command:
`python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-30/c1-controls/q9/manifest-b1.json --source S043`
- exit = **0**
- stdout:
  - `S043:sha256 OK`
  - `S043:Q1 OK normalized=markup-whitespace occurrences=1`
- stderr = (empty). **Matches `before.txt` lines 19–21 (id S043 ≠ capture stem S045 passes).**

### Probe B2 — double-occurrence fixture (`q9/manifest-b2.json`)
Command:
`python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-30/c1-controls/q9/manifest-b2.json --source S045`
- exit = **0**
- stdout:
  - `S045:sha256 OK`
  - `S045:Q1 OK occurrences=2 anchor=MISSING`
- stderr = (empty). **Matches `before.txt` lines 23–24 (occurrences=2 anchor=MISSING passes).**

All four probes reproduce the frozen `before.txt` receipt exactly (exit codes, printed lines,
and stream placement). The C1 do-nothing control is confirmed: baseline is broken on all four
predicates.

## 3. Why each baseline behavior is a conformance gap for claim C1

C1's predicate sentence requires: A1 exit 1 naming the row (not a traceback); A2 exit 1 naming
the duplicate; B1 exit 1 `reason=stem-mismatch`; B2 exit 1 `reason=occurrence-not-unique`. The
baseline violates all four, so the claim's `kill_rule` is meaningful and the `do_nothing_control`
cannot meet the target.

### A1 — missing named-row error (harness crashes)
`entry_contract` (frontier-recheck-count.py:54–65) opens the entry file directly —
`open(full, ...)` — with no `isfile` gate. When a frontier row names an entry that does not
exist, the `FileNotFoundError` escapes `evaluate` → `main` → `sys.exit(main())` as an uncaught
traceback (exit 1 by accident of the interpreter's unhandled-exception exit code).
Gap vs predicate:
- The failure is an unhandled interpreter crash, not a controlled diagnostics path; the harness
  cannot distinguish "row names a missing entry" from an internal harness bug (both surface as a
  raw traceback).
- The traceback names only the file path, never the frontier row id (**F98** absent), so a
  verifier cannot tell which row is broken without parsing a path out of an exception; the
  predicate explicitly requires "a message naming the row".
- Exit 1 is conflated with the normal "some row failed recheck" exit, giving ambiguous signal.
This is exactly round-29 mistake M29-4 ("harness crashes with an uncaught FileNotFoundError on a
missing entry").

### A2 — duplicate target passes (double credit on one entry)
`main` (lines 154–168) iterates admitted rows and calls `evaluate` per `(frontier, entry)` pair;
there is no set of already-seen resolved entry realpaths anywhere (no dedup in `read_frontier`,
`main`, or `evaluate`). Two rows naming the same `knowledge/dup-entry.md` are each evaluated
fresh, both run the same recheck line against the same capture, both PASS.
Gap vs predicate:
- The predicate requires exit 1 naming the duplicate; baseline declares `entries=2 pass=2
  exit=0`, i.e. the harness reports full success on a registry that credits one entry file twice.
- Double credit inflates recheck coverage counts (N rows can point at one passing entry and
  report N/N pass) — precisely the count-inflation class the harness was built to prevent (its
  docstring: binds the recheck line to the entry it belongs to). It also lets one entry's passing
  capture mask a sibling row that was never independently verified.

### B1 — stem mismatch passes (id ≠ capture stem)
`load_manifest` (source-recheck.py:44–74) validates schema, id format, id uniqueness — but never
compares `record["id"]` to `Path(record["path"]).stem`. `check_source` (99–180) then reads
whatever capture the path names and verifies the record's sha256/quotes against it, regardless of
whether the capture's stem matches the record id. With `manifest-b1.json` (id S043, path
S045.txt) the quote is found in S045.txt and everything reports OK, exit 0.
Gap vs predicate:
- Predicate requires exit 1 `reason=stem-mismatch`; baseline lets a record borrow another
  source's capture file. A record id S043 can be verified against S045's bytes, so the quote
  check validates the wrong source's captured text — the Q9 "stem == id" binding (round-29
  M29-3) is not enforced, and the instrument can bless cross-source quote evidence.

### B2 — double-occurrence passes (un-anchored ambiguous quote)
`anchor_verdict` (77–96) reports ` anchor=MISSING` when a quote occurs more than once
(`occurrences > 1`) without a declared anchor, but `check_source` (164–179) treats that as a
pass: it prints `OK occurrences=2 anchor=MISSING` and only sets status 1 for `reason=quote-not-found`.
With `manifest-b2.json` the quote occurs twice in B2.txt, no anchor is declared, and the run
exits 0.
Gap vs predicate:
- Predicate requires exit 1 `reason=occurrence-not-unique`; baseline reports OK on ambiguous
  evidence. Under QUALITY Q9 a non-unique quote without a verified anchor does not uniquely pin
  the claim (two spots could match), so it must fail, not pass. This is the double-occurrence
  half of round-29 M29-3.

## 4. Scope notes / unknowns

- The A1 "pass pointing at an unrelated existing entry" half of M29-4 is in the C1 surface but
  has no dedicated counter/fixture probe; it is not separately exercised here (the A1 fixture
  exercises only the crash half). Still present by code reading: `entry_contract` resolves
  `entry_path` relative to root first, then falls back to `root/corpus/entry_path` with no check
  that the resolved file is the entry the README row intends.
- Real-corpus runs (harness on the full lane, real round-30 manifest rechecks) belong to C1's
  `kill_rule` final clause and were not in this seat's scope; nothing here touched the real
  corpus, live network, or any bounty target.
- No files were modified in the lane; this report is the only artifact written (plus transient
  /tmp capture files, removed after use).
