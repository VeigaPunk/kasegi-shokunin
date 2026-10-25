# RevFrontierHarness — no-harm guard on the round-24 frontier recheck harness

Seat: `L1Kasegi25.RevFrontierHarness` (read-only). Round 25, wave 1, lane `kasegi-shokunin`.
Lane base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`.

Axes named: `depth:verifiability` (C1 — the 35 `recheck:` lines) and `coverage` (C2 — F10 frontier row).
The axis this seat adds is the *no-harm* constraint on both: the round-24 harness
`corpus/instruments/frontier-recheck-count.py` must still read 10/10 after the round lands.

---

## (a) Harness receipt and exit code

**Committed bytes (base revision, extracted with `git archive` into `/tmp/base25`):**

```
$ cd /tmp/base25 && python3 corpus/instruments/frontier-recheck-count.py --json /tmp/frc-base.json | tail -3
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0
entries=10 pass=10 exit=0
EXIT=0
```

**Live lane tree after the C1 seat rewrote all 35 `recheck:` lines** (30 tracked files modified,
`git status --porcelain` shows `M corpus/knowledge/*.md`; C1 audit at the same moment:
`lines=35 pass=35 fail_closed=23 failing_limbs={parse:0,cwd:0,paths:0} exit=0`):

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/frontier-recheck-count.py
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0
entries=10 pass=10 exit=0
HARNESS_EXIT=0
```

Receipt JSON (`--json /tmp/frc-live.json`, outside the lane because this seat is read-only):
`schema: kasegi-frontier-recheck-receipt-v1`, `entries: 10, pass: 10`, every record `problems: []`.
The base-revision receipt is `/tmp/frc-base.json` (same schema, `entries: 10, pass: 10`).

**Harness bytes are untouched by the round:**

```
c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261  corpus/instruments/frontier-recheck-count.py
c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261  /tmp/base25/corpus/instruments/frontier-recheck-count.py
```

## (b) Does the harness read the 35 lines? **Yes — 10 of them, and only through `corpus/README.md`.**

The harness never globs `corpus/knowledge/*.md`. It walks the frontier table and then each entry the
admitted rows name:

| step | code pointer | what it does |
|---|---|---|
| row discovery | `corpus/instruments/frontier-recheck-count.py:42` `read_frontier` + `:35` `FRONTIER_ROW` | parses `\| F## \| title \| status \| entry-cell \|` from `corpus/README.md` |
| admission filter | `:154` `admitted = [r for r in rows if r[2] == "admitted"]` | only `status == admitted` rows are evaluated (a `rejected`/staged row is invisible to the harness) |
| multi-entry cell | `:157-158` | splits `entry, entry` on comma — this is why F09 yields two records |
| `recheck:` extraction | `:54` `entry_contract` + `:37` `RECHECK_LINE = r"^recheck:\s*(.+)$"` | takes the **first** line starting at column 0 with `recheck:`, whole tail of the physical line |
| id extraction | `:38` `RECHECK_SOURCE = r"--source\s+(S\d{3,})"` | every `--source S###` anywhere in that tail (comments included) |
| manifest extraction | `:39` `RECHECK_MANIFEST = r"--manifest\s+(\S+)"` | **first** `--manifest <token>`; quotes stripped by `.strip("`'\"")` |
| manifest validation | `:85` `manifest_ids` | `os.path.join(root, manifest)`, must parse as JSON, `schema_version == 1`, `sources` list |
| execution | `:125` `subprocess.run(["bash","-c",recheck], cwd=root)` | runs the tail with **cwd = lane root**, exit code is the record's result |

The ten entries that are harness inputs (of the 35 lines):

```
knowledge/cvss-v4-severity-and-vector.md                     F01  S001, S002
knowledge/coordinated-disclosure-timelines.md                F02  S003, S004, S005
knowledge/authorization-safe-harbor-and-scope.md             F03  S006, S007, S008
knowledge/ai-assisted-finding-validation.md                  F04  S009, S010, S011, S012
knowledge/cwe-top25-2025-methodology.md                      F05  S013, S014, S015
knowledge/multiparty-vulnerability-coordination.md           F06  S018
knowledge/cna-assignment-and-vulnerability-rules.md          F07  S031
knowledge/cra-manufacturer-reporting-duties.md               F08  S029
knowledge/authorised-testing-rules-of-engagement.md          F09  S032
knowledge/statutory-authorization-and-unauthorized-access.md F09  S033, S034, S035
```

The other **25 lines are not harness inputs** — including all 23 `on-restoration …` lines and
`citation-bases.md`. Those are read only by the C1 audit
(`corpus/instruments/recheck-audit.py:41` `RECHECK_RE`, `:105` `glob("corpus/knowledge/*.md")`),
which is a different instrument with different limbs (`bash -n` parse, lane-root vs `/` exit+digest
equality, corpus-path existence).

### Does a `cd … && cmd # note` form still parse? **Yes — measured PASS.**

Fixture `/tmp/frhfix` (README row `F99 admitted → knowledge/x.md`, `corpus/instruments` and
`corpus/source-snapshots` symlinked to the lane, entry header `source: S001`):

| variant of the `recheck:` tail | harness verdict |
|---|---|
| `cd <lane> && python3 …/source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json --source S001 # note` | **PASS** exit 0, `manifest=corpus/source-snapshots/round-24/manifest.json`, `ids=[S001]` |
| `cd <lane> && …` (no note) | PASS exit 0 |
| `bash -c 'cd <lane> && …'` (whole command quoted) | PASS exit 0 |
| `recheck:` + leading spaces before `cd` | PASS exit 0 (`\s*` after the colon absorbs them) |
| `--manifest=corpus/…/manifest.json` (equals form) | **FAIL** `no-manifest` — `:39` requires whitespace |
| `--manifest $HOME/Projects/…/manifest.json` | **FAIL** `manifest-unreadable` — `:85` does not expand `$HOME`/`~` |
| note naming another source: `… --source S001 # see --source S999` | **FAIL** `manifest-missing-ids` — `:38` harvests ids from the note too |
| trailing backslash continuation | **FAIL** `recheck-exit-127` — `:37` captures one physical line only |

Why the note form is safe for the real rewrite: `#` is a shell comment inside `bash -c`, so the
execution is unchanged; the manifest token is still the first space-separated `--manifest` argument,
so `:39` captures the right path; the id set is unchanged because the notes carry no `--source`
token. The live C1 rewrite uses exactly this shape (`cd … && cmd  # on-restoration — …`) on the
23 fail-closed lines, and **none of the ten frontier lines carries a `#` at all**:

```
$ for f in <the ten>; do grep -m1 '^recheck:' corpus/knowledge/$f.md | grep -c '#'; done
cvss-v4-severity-and-vector 0 / coordinated-disclosure-timelines 0 / authorization-safe-harbor-and-scope 0 /
ai-assisted-finding-validation 0 / cwe-top25-2025-methodology 0 / multiparty-vulnerability-coordination 0 /
cna-assignment-and-vulnerability-rules 0 / cra-manufacturer-reporting-duties 0 /
authorised-testing-rules-of-engagement 0 / statutory-authorization-and-unauthorized-access 0
```

## (c) Verdict

**`fix is safe for the harness`** — for the C1 rewrite of the 35 `recheck:` lines. Measured:
`entries=10 pass=10 exit=0` on committed bytes `b49948f` *and* on the live tree after the rewrite;
the harness file hash is identical in both; the ten input lines changed only by the `cd <lane> &&`
prefix, which leaves the id set, the manifest token and the exit status untouched; the note form the
rewrite uses on the other 25 lines is parsed and executed correctly (fixture, PASS).

**One blocking precondition, on the C2 side, not on the harness.** F10's entry has already landed at
`corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` with

```
source: S036 … / S037 … / S038 … / S039 …
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py
         --manifest corpus/source-snapshots/round-25/manifest.json --source S036 … --source S039
```

and `corpus/source-snapshots/round-25/` currently holds only `S036.txt … S040.txt` — **no
`manifest.json`**. `corpus/README.md` has no `F10` row yet, so the harness still reports 10/10 today.
The moment an **admitted** F10 row is appended, the harness evaluates an 11th record; measured on a
fixture with the live entry text and a missing manifest:

```
FAIL     F10  knowledge/new.md   ids=S055   exit=-   problems=manifest-unreadable
entries=2 pass=1 exit=1        HARNESS EXIT 1
```

With a manifest present and valid (`schema_version: 1`, relative `path` inside the manifest directory,
64-hex `sha256`, `quotes` list with ≥12 normalized chars) the same entry passes end-to-end — the four
live command bodies were run against a fixture manifest built from the real captures and exited 0
(`S036..S039:sha256 OK`, `q1 OK occurrences=1`), and the harness then reported
`PASS F10 … exit=0 / entries=1 pass=1 exit=0`.

So: **the L1 must land `corpus/source-snapshots/round-25/manifest.json` in the same commit as (or
before) the admitted F10 README row.** If that manifest cannot be built, the F10 row must not be
appended — the harness would go from `entries=10 pass=10 exit=0` to `entries=11 pass=10 exit=1`, which
is a regression of the round-24 capability the round is supposed to preserve. The harness itself needs
no change to admit F10.

## Residual risks (measured, pre-existing, not introduced by this round)

1. **Row/entry atomicity.** An `admitted` row naming a missing entry file crashes the harness with an
   uncaught `FileNotFoundError` (traceback, exit 1) instead of emitting a FAIL record — `entry_contract`
   opens the path with no `isfile` guard. Verified on a fixture (`knowledge/ghost.md`).
2. **Exit laundering.** `… ; false | tail -1` scores PASS because `:125` takes the exit of the last
   pipeline element. A line can hide a failing recheck behind a pipe.
3. **Comment harvesting.** `:38`/`:39` scan the raw line, so a note that mentions `--source`/`--manifest`
   alters the contract check (measured FAILs above). Harmless today (no frontier line carries a note).
4. **Column-0 requirement.** Both `RECHECK_LINE` (`:37`) and the audit's `RECHECK_RE` (`:41`) anchor at
   column 0; indenting the key silently drops the line from both instruments. Not triggered by the rewrite.
5. The harness proves pinned-capture integrity only; it does not check cwd-independence or `bash -n` —
   those are the C1 audit's limbs, and the harness is not a substitute for it.

## Verification gaps

- The real `corpus/source-snapshots/round-25/manifest.json` was not built here (L1's artifact;
  contract documented by the `RevManifestShape` seat). My end-to-end F10 proof used a fixture manifest
  built from the real captures with my own quotes, not the entry's pinned quotes.
- The F10 README row had not landed at any check made by this seat (last check: both
  `vendor-disclosure-policies-as-corpus-objects.md` and `vendor-disclosure-policy-commitments-crosswalk.md`
  present, `corpus/README.md` still F01–F09 only, `corpus/source-snapshots/round-25/` still
  `S036.txt … S040.txt` with no `manifest.json`, harness re-run `entries=10 pass=10 exit=0`), so the
  11-record state was exercised only on fixtures.
- Tooling: nothing installed or upgraded for this seat.
