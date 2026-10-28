# ExecJ7Flip — F-FLIP: frontier-recheck-count.py must never drop a frontier row

Seat: ExecJ7Flip (round 42, wave 1, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `5053a7f46de35784cff4b56756906e9014a38276`). No mutating git/jj anywhere; the fleet root,
`shokuknow` and every other lane were read-only to this seat.

## 1. The defect, grounded

Round-41 falsify result `MutC2Chain` (`agent: mutation-tester`,
`.ufo/waves/round-41/kasegi-r41-falsify-results.json`, results[5]):

```
mutant:            "F24 row status admitted→explored in scratch mirror"
expected_detector: "frontier-recheck-count.py must fail F24"
output:            "entries=26 pass=26 exit=0; F24 absent from output"
verdict:           "survived (coverage finding). Baselines: frontier 27/27; ..."
```

The instrument built its record set from `rows if status == "admitted"` only. Flipping one row's
status cell removed that row from the denominator, so the count self-consistently greened
(`26/26 exit 0`). Nothing compared `entries=` against the README row count; nothing required an
explicit `PASS F<n>` per row; nothing bound a row's cited id to the registry.

Reproduced on the lane's current committed instrument before the patch, against the scratch
mirrors built in `$S/cases` (see §4):

```
status-queued    -> entries=26 pass=26 exit=0     (row vanished; defect)
status-explored  -> entries=26 pass=26 exit=0     (the exact r41 mutant shape; defect)
cites-S999       -> entries=27 pass=27 exit=0     (row cites an unregistered id; silent)
no-recheck       -> entries=27 pass=26 exit=1     (record limb already rejected this one)
```

## 2. Deliverable

`.ufo/waves/round-42/wave1/ExecJ7Flip.frontier-recheck-count.py` — the whole patched instrument,
to be landed over `corpus/instruments/frontier-recheck-count.py`.

- lines: 566
- sha256: `010897bc8614c3ef3bb008eb4cdbb6c79f01a7c0afa280bc902e709dda9f1bd6`
- stdlib only, same shebang, same default `--root` derivation (`dirname^3(__file__)`, i.e. correct
  once landed in `corpus/instruments/`; the wave-1 copy needs an explicit `--root`).

What the patch adds (rule G — the frontier census):

1. `FRONTIER_SOURCES` / `REGISTRY_ROW` regexes; `read_frontier_sources(root)` (each README row's
   `sources` cell ids) and `read_registry_ids(root)` (`corpus/SOURCES.md` ids, or `None` when the
   root carries no registry — a miniature fixture lane).
2. `frontier_row_record(fid, entry, problems, declared_ids)` — the synthetic FAIL record a
   non-admitted row contributes, one per entry cell, so `entries=` counts the raw row set and can
   never shrink under a status flip.
3. `frontier_census(rows, records, registry, sources)` — enumerates **every** `| F<n> |` row and
   fails the run when a row's status is not `admitted` (`status-not-admitted`), when an admitted
   row owns no PASS record (`missing-pass-line`), or when an id it binds — its README `sources`
   cell plus the ids its entries declare/evidence — has no registry row
   (`source-id-absent:<id>`). Prints `FRONTIER-CENSUS rows=N admitted=N closed=N problem-rows=N
   registry=N|absent`, then one `FRONTIER-PASS <id> ids=<ids>` / `FRONTIER-FAIL <id>
   status=<status> ids=<ids> problems=<...>` line per row, **before** the per-entry records.
4. `main()` iterates all rows (not just admitted ones), prints the census, then the records in the
   exact pre-existing `%-8s %-4s %-52s ids=%-14s exit=%-4s` shape, and ORs `census_failed` into
   `fail_closed` after the untouched duplicate-entry block. `entries=` / `pass=` / the final
   `exit=` summary line keep their position (last line) and meaning.
5. `--json` receipt: one additive key `frontier_census` (`rows`, `admitted`, `closed`,
   `problem_rows`, `registry`, `failures`); `schema` unchanged, so existing readers are unaffected.

Committed instrument-quality apparatus is untouched: both `limb-ledger.json` `find` strings for
this instrument still occur exactly once (`FR-missing-entry`, `FR-duplicate-entry`), and the six
`--selftest` cases are unchanged in number and wording.

## 3. Base green (proved)

```
$ python3 .ufo/waves/round-42/wave1/ExecJ7Flip.frontier-recheck-count.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
FRONTIER-CENSUS rows=24 admitted=24 closed=24 problem-rows=0 registry=63
FRONTIER-PASS F01 ids=S001,S002
...
FRONTIER-PASS F24 ids=S063
PASS     F24  knowledge/rfc-9116-security-txt.md                   ids=S063           exit=0
entries=27 pass=27 exit=0
```

`entries=27 pass=27 exit=0` at base exactly as the item requires (24 frontier rows, 27 entry cells),
`rows=24 admitted=24 closed=24 problem-rows=0 registry=63` — every row admitted, every row with a
PASS line, every bound id (cell ∪ entry) registered, nothing dropped.

```
$ python3 .ufo/waves/round-42/wave1/ExecJ7Flip.frontier-recheck-count.py --selftest --scratch $S/st3
selftest case=bidirectional-holds exit=0 want=0 verdict=pass
selftest case=selection-not-declared exit=1 want=1 verdict=pass
selftest case=header-source-not-rechecked exit=1 want=1 verdict=pass
selftest case=evidence-list-declares-selection exit=0 want=0 verdict=pass
selftest case=evidence-declared-not-rechecked exit=1 want=1 verdict=pass
selftest case=selection-neither-declared-nor-mentioned exit=1 want=1 verdict=pass
selftest cases=6 failures=0
exit=0
```

Also proved at the lane location with the default root (`cd $S/lane && python3
corpus/instruments/frontier-recheck-count.py` → `entries=27 pass=27 exit=0`, exit 0), and the JSON
receipt carries `frontier_census = {admitted: 24, closed: 24, failures: [], problem_rows: 0,
registry: 63, rows: 24}`.

## 4. Rejected runs (the required three, plus the r41 replay)

Scratch mirrors are full copies of the lane `corpus/` with one mutation each; the entries' own
`recheck:` lines `cd` to the real lane, so a mutation isolates exactly one limb. Transcript
deliverable: `.ufo/waves/round-42/wave1/ExecJ7Flip.transcript.txt`
(322 lines, sha256 `193b29ba6798c6552d4166229ed9ca14791a251fab1c807e1ddc2a787842d864`) — real
`$ command` / output / `exit=` triples, regenerated by `$S/make_transcript.py` against the
delivered path.

| case | mutation | census line | summary | exit |
|---|---|---|---|---|
| a `status-queued` | F24 status cell `admitted`→`queued` | `FRONTIER-FAIL F24 status=queued ids=S063 problems=status-not-admitted` | `entries=27 pass=26 exit=1` | 1 |
| r41 replay `status-explored` | F24 status cell `admitted`→`explored` (the MutC2Chain mutant) | `FRONTIER-FAIL F24 status=explored ids=S063 problems=status-not-admitted` | `entries=27 pass=26 exit=1` | 1 |
| b `no-recheck` | `recheck:` line deleted from F24's entry (`grep -c '^recheck:'` 1→0) | `FRONTIER-FAIL F24 status=admitted ids=S063 problems=missing-pass-line` + record `problems=no-recheck-line,no-source-selection,no-manifest` | `entries=27 pass=26 exit=1` | 1 |
| c `cites-S999` | F24 `sources` cell `S063`→`S999` | `FRONTIER-FAIL F24 status=admitted ids=S063,S999 problems=source-id-absent:S999` | `entries=27 pass=27 exit=1` | 1 |

Case (c) is the sharp one: every entry still rechecks clean, so `entries=27 pass=27` self-
consistently greens — **only** the census sees that the row is bound to an id the registry does not
declare, and exits 1. In all four cases the flipped/lost row still occupies its entry cells, so the
denominator stays 27 instead of silently shrinking to 26.

Multi-cell row check (F09 governs two entries): flipping its status cell to `queued` yields two
synthetic FAIL records and keeps the denominator —

```
$ python3 .../ExecJ7Flip.frontier-recheck-count.py --root $S/cases/two-cell-flip
FRONTIER-CENSUS rows=24 admitted=23 closed=23 problem-rows=1 registry=63
FRONTIER-FAIL F09 status=queued ids=S032,S033,S034,S035 problems=status-not-admitted
FAIL     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032,S033,S034,S035 exit=-    problems=status-not-admitted
FAIL     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S032,S033,S034,S035 exit=-    problems=status-not-admitted
entries=27 pass=25 exit=1
```

(the census also reports the row's bound set as cell ∪ each entry's declared ids, so a flipped row
keeps its citations visible instead of losing them).

## 5. No harm (measured, not argued)

**(i) Committed limb ledger, replayed against the patched bytes.** `corpus/` copied to `$S/lane`,
patched instrument dropped in, ledger run unchanged:

```
$ cd $S/lane && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json --root $S/lane
guard cases=3 failures=0
LIMB FR-missing-entry   live=1/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
LIMB RA-* (9: parse, cwd, paths, cdroot, instrument, own, completeness, expect-missing,
           expect-unexpected) killed; LIMB SR-* (2) killed
CONTROL CTL-noop verdict=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
ledger_exit=0
```

`FR-missing-entry` is still killed by signal and `FR-duplicate-entry` still by exit 0 on the
mutant, exactly as the ledger notes require (the ledger `find` strings sit in untouched code).

**(ii) The consumer script that executes this counter.** `r-defect-closure.sh --root $S/lane`
(with SCORECARD.md and the round-34 `junk-f17.md` twin the check requires) is fully green:

```
R9 check=capture-binding H4-H8 cases=9 + frontier rule A bidirectional (mirror=0 reverse=1) + junk=.ufo/waves/round-34/c2-controls/junk-f17.md open=0
closed=9/9 exit=0
```

R9 builds a four-column `| F99 | ... | admitted | entry |` fixture row and asserts mirror exit 0 /
reverse exit 1; the census reads no `sources` cell there (four columns), finds no registry in that
fixture root (`registry=absent`), and leaves both exit codes exactly as they were.

**(iii) r42 C1 compatibility.** The planned C2 after-state runs the counter expecting
`entries=28 pass=28 exit=0` incl. `PASS F25`. The census only ever adds lines *before* the record
lines; `entries=`/`pass=`/`exit=` stay on the final line in the same format, so a grep for
`^entries=(\d+) pass=(\d+) exit=0$` and a grep for `PASS F25` both still work — provided F25's
README row has status `admitted`, its entry's recheck passes, and the id its row/entry binds
(S064) has a `corpus/SOURCES.md` row, which is exactly what C2 undertakes.

## 6. Landing obligations for the L1 (not mine to write)

The patch changes the instrument's bytes and output, so these documents must be amended in the
same landing (each is outside this seat's write scope):

- `corpus/instruments/README.md:460` — the digest table row pins
  `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893`… `(unchanged)`; replace with
  `010897bc8614c3ef3bb008eb4cdbb6c79f01a7c0afa280bc902e709dda9f1bd6`.
- `corpus/instruments/README.md:175` — the counter's description (add rule G / the census lines
  and the three row-failure problems), plus a round-42 amendment section; `:441` ("needed no edit")
  now refers to round 34 only and should say so.
- Any r41/r42 suite assertion that captures the full counter transcript: the record lines are
  byte-identical, but `FRONTIER-*` lines now precede them.
- `limb-ledger.json` needs no edit (both find strings and both signals are preserved, §5i); if the
  suite wants the new row-level edge covered by the quality apparatus rather than by this
  transcript, the natural home is an r42-closure J-check (a status-flipped row → exit 1 with
  `status-not-admitted`), not a ledger limb.

## 7. Risks / limits (stated, not papered over)

- The registry limb is **not decidable** in a root without `corpus/SOURCES.md`; there the census
  reports `registry=absent` and skips it. Every real lane root has one (base: `registry=63`).
- Row binding is cell + declared/evidence ids. Re-key detection (row id re-pointed to another
  entry) is still only caught by the existing duplicate-entry limb, as CriitCriticalRule noted; the
  census does not add a re-key check, and I did not widen scope to one.
- The six `--selftest` cases were deliberately not extended: `MutC1Candidate` recorded the ledger's
  "positive=pass" graded contract as defective, the suite edge belongs to r42-closure.sh's graded
  J-cases, and adding cases would have moved a number other seats may pin. The new limbs are proved
  by the replayed transcript (§4) instead. If the L1 prefers self-test coverage, the census edge is
  addable as a seventh case (`missing-pass-line` + `registry=absent`).
- `entries=` counts entry cells, not rows (27 at base); the row count is now explicit and auditable
  in `FRONTIER-CENSUS rows=24`.

## 8. Scratch, tooling, guard

- Scratch `S=/fast/scratch/hyaku/kasegi-r42/ExecJ7Flip` (work copy, `cases/*` mirrors, `lane/`
  replay lane, `make_transcript.py`, transcript/ledger logs) — removed after the deliverables were
  copied into the wave dir.
- `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` before the heavy passes:
  `/tmp 5%`, `/var/tmp 36%`, `/fast/scratch/hyaku 33%` — green.
- No tool installed or upgraded; no pacman call; no network fetch; no service touched; scratch-only
  `git`-free work (no fixture repo needed).
