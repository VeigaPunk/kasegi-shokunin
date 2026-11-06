# ConnectorOverlap — kasegi round 80, attempt 1 (w1)

Read-only seat. No lane, instrument, corpus or frozen byte edited; no tool installed; no subagent.
Scratch `/fast/scratch/hyaku/kasegi-r80/ConnectorOverlap` (removed before yield); every probe
below ran with `TMPDIR` set there and wrote only under it.

Ground: freeze commit `4ab5458`. At scan time the working tree already carried an in-flight
landing (`M PROVINCE.md`, `M corpus/README.md`, `M corpus/instruments/recheck-cwd-census.py`,
`?? corpus/knowledge/osv-ubuntu-binary-to-source-mapping.md`). Every frozen-byte statement below
is measured at HEAD `4ab5458` or on files `git diff --stat` shows unmodified
(`corpus/instruments/source-recheck.py`, `corpus/source-snapshots/round-80/`).

---

## 1. C2 — sibling-lane overlap and PROVINCE ownership

Scan (read-only, kasegi skipped):

```
for r in $(ls -d /home/vgpnk/Projects/shokunin/*-shokunin | grep -v kasegi); do
  grep -rn -e 'binary-to-source' -e 'binary_to_source' -e 'ubuntu' -e 'osv.dev' \
          -e 'OSV.dev' -e 'source package' "$r/corpus/knowledge"
  grep -rin 'osv' "$r/corpus/knowledge"          # case-insensitive sweep
  grep -in  'osv' "$r/PROVINCE.md"               # ownership sweep
done
```

Complete hit list (18 sibling lanes have `corpus/knowledge/`), each classified:

| path:line | matched term | why it is not the same ground |
|---|---|---|
| `kaidoku-shokunin/corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:22` | `ubuntu` | GCC `.comment` banner `GCC: (Ubuntu 13.3.0-6ubuntu2~24.04.1)` |
| `kaidoku-shokunin/corpus/knowledge/2026-10-13-r2-jq-shadow-verdict.md:100` | `ubuntu` | `bugs.launchpad.net/ubuntu/+source/glibc` URL |
| `kaidoku-shokunin/corpus/knowledge/2026-10-13-r3-node-addons.md:8` | `ubuntu` | same GCC banner |
| `kengaku-shokunin/corpus/knowledge/tb2-constraints-scheduling-grader.md:303` | `ubuntu` | `FROM ubuntu:24.04` Dockerfile, never pulled |
| `kengaku-shokunin/corpus/knowledge/tb2-db-wal-recovery-grader.md:264,267` | `ubuntu` | `FROM ubuntu:24.04`; `packages.ubuntu.com` HTTP 500 note |
| `kengaku-shokunin/corpus/knowledge/tb2-git-leak-recovery-grader.md:266,268,329` | `ubuntu` | `ubuntu:24.04` container, apt git |
| `kengaku-shokunin/corpus/knowledge/tb2-polyglot-c-py-grader.md:5,71` | `ubuntu` | image recipe `ubuntu:24.04` |
| `mori-shokunin/corpus/knowledge/pid-probe-conclusion-r44.md:3,6` | `ubuntu` | `manpages.ubuntu.com` proc(5) |
| `kotodama-shokunin/corpus/knowledge/linguistics/syntax-typology.md:11,32` | `OSV` | **word order** Object–Subject–Verb, not OSV.dev (the false-positive trap of this scan) |

Result:

- **0 of 18 sibling lanes hold an entry on OSV.dev or on any OSV endpoint.** No sibling entry
  states the binary-to-source mapping, the Ubuntu source-indexing rule, the 1000-name bound or the
  empty-object result.
- **0 sibling `PROVINCE.md` mention OSV** (`grep -in 'osv'` over all sibling PROVINCE files →
  no output). C2 has no cross-lane overlap.

kasegi ownership, cited from `PROVINCE.md` at freeze `4ab5458`:

- `PROVINCE.md:219` **F51** — OSV.dev POST `/v1/query` contract; scope limit: "the query
  endpoint's request and response contract only — … not the other endpoints".
- `PROVINCE.md:225` **F54** — POST `/v1/querybatch`; scope limit: "not the single-query POST
  /v1/query contract (F51) …".
- `PROVINCE.md:227` **F55** — POST `/v1experimental/determineversion`; scope limit names F51,
  F54, F31 and "the case-sensitivity line (:64, held by F51)".

So the lane owns OSV ground **endpoint by endpoint**, and each admitted frontier's scope limit
explicitly hands the sibling endpoints to future frontiers. F56's six clauses therefore cannot
overlap F51/F54/F55 by those frontiers' own wording. The mechanism is visible in the entry:
`corpus/knowledge/osv-post-v1-query-contract.md:75` lists "the other endpoints in the page's
navigation … They are listed, not described" — that Limits bullet is the queue F56 walks, and
F56 is the third walk (F54, F55, F56). `PROVINCE.md:229` (F56) exists only in the working tree,
not in HEAD.

Residue after F56, named for round 81 (not claimed here): `GET /v1experimental/importfindings`
and `GET /v1/vulns/{id}` — `corpus/source-snapshots/round-76/S111.txt:7,29,45`,
`corpus/lessons/round-79.md:78`. No snapshot of either endpoint page exists yet.

---

## 2. C1 — instruments carrying the R129-forbidden pattern

Literal grep: `grep -n 'exception' corpus/instruments/*mutbat*.py` → **0 hits** in all three
mutbat instruments (`figure-audit-mutbat.py`, `r46-mutbat.py`, `r47-mutbat.py`). None classifies
by free text; each grades structurally:

- `figure-audit-mutbat.py:105-109` — `valid = rc in (0,1) and last.startswith("selftest cases=")`,
  `killed = int(rc == 1)`.
- `r46-mutbat.py:280-282` — parses `^gate (H\d) pass=(\d) ` numeric fields.
- `r47-mutbat.py:168-192` — failures count from `run_selftest` exit.

The literal R129 defect survives only in frozen r79 evidence (`.ufo/waves/round-79/c1/mutbat.py:40`
`EXC_RE`), not in any live mutbat.

The **shape** R129 forbids — a verdict decided by a free-text substring of a child's output rather
than a dedicated marker — survives in registered instruments (registry rows `SKILL.md:1156,1163,
1172,1173,1185,1226`). Routed candidates:

| # | site | pattern | status |
|---|---|---|---|
| R80-CONN-A | `corpus/instruments/source-recheck.py:196-215` (+`:110`) | unique-quote pass is exit-0 regardless of `anchor=N-BROKEN` / `anchor=OUT-OF-RANGE`; `anchor=N-ok` holds for a 4-line window | **live on C2's B0/B5 path** |
| R80-CONN-B | `corpus/instruments/r46-c2-gate.py:326` | `"BROKEN" not in out and distinct` as the anchor gate | registered, historical round |
| R80-CONN-C | `r45-c2-gate.py:252`, `r46-f29-gate.py:299`, `r45-routed-defects.py:200` | `"S071/S072/S073:sha256 OK" in out`, `oks >= N` | registered, historical |
| R80-CONN-D | `corpus/instruments/figure-audit.py:698,701` | `any("reason=%s stale" % r in out …)` decides pass | current, not an r80 predicate |
| R80-CONN-E | `corpus/instruments/capture-binding-check.py:988-990` | `line not in stdout`, `"FAIL " in stdout` (report verifier; summary-only reports already fail) | current, not an r80 predicate |

Not a defect: `claim-package-check.py:636` `NO_SUBMISSION not in text` (sentinel presence, not a
verdict over a child's output).

Ranking: R80-CONN-A is the only one on round 80's critical path; B/C are historical but still
registered commands; D/E are current but out of scope for this round.

---

## 3. Cross-claim pattern — the shared freeze-time dry run, and the missing C2 control

**Shared move.** Both claims' verdicts rest on an R126 freeze-time dry run over frozen bytes. C1
rebuilt its dry run so the counter *can print its own target*: `controls/c1-mutbat-selftest-r80.txt`
runs the same counter under the r79 classifier and it FAILs (`T-KILL → EXCEPTION-KILL counted=no`);
`controls/c1-forgery-r80.txt` (selftest replaced by a print stub) shows `survived=28 rc1`.

**C2's dry run lacks that property.** Executed read-only probes — scratch copy of the frozen
manifest and snapshot, frozen instrument, no lane write:

```
$ cp corpus/source-snapshots/round-80/S114.txt $S/probe/   # sha256 unchanged
$ python3 -c '... anchor Q01 25->24, Q04 38->999 ...'      # $S/probe/perturb.json
$ TMPDIR=$S python3 -B corpus/instruments/source-recheck.py --manifest $S/probe/perturb.json --source S114
S114:sha256 OK
S114:Q01-purpose OK occurrences=1 anchor=24-ok
S114:Q02-source-indexing OK occurrences=1 anchor=35-ok
S114:Q03-scanner-use OK occurrences=1 anchor=35-ok
S114:Q04-ecosystem-forms OK occurrences=1 anchor=OUT-OF-RANGE
S114:Q05-binary-names-limit OK occurrences=1 anchor=39-ok
S114:Q07-unmapped-empty-object OK occurrences=1 anchor=58-ok
rc=0

$ ... anchor Q01 25->26 ...                                  # one line late
S114:Q01-purpose OK occurrences=1 anchor=26-BROKEN
rc=0
```

Cause, in the frozen instrument: `source-recheck.py:110`
`window = " ".join(raw_lines[max(0, anchor - 1):anchor + 3])` — a **4-line window**, so
`anchor=N-ok` holds for any N in [L-3, L]; and `:190-203` makes the anchor fatal only when
`occurrences > 1`. All six frozen quotes occur once.

Content is sound — measured independently: `exact_hits` in `S114.txt` equal the declared anchors
for all six (25, 35, 35, 38, 39, 58), `occurrences=1` each, 73 snapshot lines. **No verdict change.**

**Would any control in `controls/` catch a C2 freeze defect of the r79 C1 kind? No.**

- `c2-prerecheck-r80.txt` is a positive-only run; `grep -rn 'BROKEN\|anchor=' controls/*.txt` over
  the round-80 controls returns only the six `anchor=…-ok` lines. Its second section
  ("exact-line containment + word counts") is where exactness is actually measured, and that
  section is generated by an uncommitted inline script, not an instrument.
- `c2-donothing-counters-r80.txt` reads counter values at base; `census-start-r80.txt` is the W04
  validator, positive.
- There is no C2 analogue of `c1-forgery-r80.txt` (instrument replaced by a stub) and none of
  `c1-mutbat-selftest-r80.txt` (instrument run under a known-bad rule).

So a manifest whose anchors sit 1–3 lines early yields `rc=0` and byte-different but still
"anchor=N-ok" notes; an anchor one line late yields `rc=0` with a `-BROKEN` note. Only a human
comparing the note's number to the manifest/actual line separates them — exactly r79's K-T1 shape,
transposed from the counter's classifier into the C2 receipt. Historical regression:
`r46-c2-gate.py:326` gated this same instrument with `"BROKEN" not in out and distinct`; the r80
B0 predicate drops that limb. The draft's receipt line
(`.ufo/waves/round-80/w1-input/osv-ubuntu-binary-to-source-mapping.md:86`) already states "the six
anchors are the exact lines the quotes occupy" while citing that exit-0 control.

Frozen instrument self-test, for the record (read-only, lane bytes):
`TMPDIR=$S python3 -B corpus/instruments/source-recheck.py --selftest` → `selftest cases=10
failures=0`, rc 0; its broken/out-of-range anchor cases all run on the **double-occurrence**
capture, none on a unique quote — the gap above.

---

## 4. Proposed move (one, bounded)

At the C2 landing, make the anchor receipt two-polarity **without editing any frozen byte**, and
route the instrument fix to round 81:

(a) **Landing receipt.** Record (i) `grep -n` of each frozen quote in
`corpus/source-snapshots/round-80/S114.txt` (all six exact: 25/35/35/38/39/58) as the source of
the "exact lines" statement, and (ii) the negative run of the frozen instrument against a scratch
copy of the frozen manifest with one anchor shifted by +1, showing `anchor=26-BROKEN` and rc 0.
The receipt then states that exactness comes from the direct grep, not from the recheck exit code.

(b) **r81 counter route.** `source-recheck.py --selftest` gains one case — "unique quote on a wrong
anchor → MISMATCH, exit 1" — and the anchor window narrows to the exact line (or gains an
exit-bearing exact-line mode), so B0-style predicates cite an exit code instead of a note.

**Affected axes.** depth:verifiability improves (C2's anchor claim acquires a failing mode; C1
untouched; no frozen byte, row, table or score changes). coverage unchanged — no entry added, no
row re-scored; the residue in §1 is r81 material.

**Risks.**
1. If the L1 keeps draft `:86`'s wording while citing only the rc-0 control, the entry's receipt
   overstates its evidence — the r79 K-T1 class; a routed defect, never a verdict change.
2. C2's claims pin no sha256 for `source-recheck.py` (`corpus/instruments/README.md:477` pins a
   revision pair; the r80 byte is unpinned), so an instrument edit during landing could green B0
   vacuously — the exact hole `c1-forgery-r80.txt` exists to close on the C1 side.
3. Narrowing the window may flip anchors that currently rely on it; the six round-80 anchors do
   not (all exact), but the change must be measured lane-wide before landing.
4. The negative receipt is landing evidence only; it cannot change the frozen manifest, the
   snapshot, the claims or the score.

**Verification.**
- `grep -rn -e 'binary-to-source' -e 'ubuntu' -e 'osv'` over the 18 sibling `corpus/knowledge`
  trees and sibling `PROVINCE.md` → only the classified hits in §1.
- `git show HEAD:PROVINCE.md | grep -n 'F51 —\|F54 —\|F55 —'` → 219, 225, 227; F56 absent at HEAD.
- The two perturbed-manifest runs in §3 (exact commands and outputs) → rc 0 with
  `anchor=24-ok`, `anchor=26-BROKEN`, `anchor=OUT-OF-RANGE`.
- Independent exact-line measurement → six `exact_hits` equal to declared anchors, `occ=1` each.
- `python3 -B corpus/instruments/source-recheck.py --selftest` → `cases=10 failures=0`, rc 0; no
  unique-quote-broken-anchor case exists.

## Files written

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-80/w1/ConnectorOverlap.md`
