# ExecC2Instruments — round-41 wave 1 (kasegi C2) — seat receipt

Seat: ExecC2Instruments · 2026-10-27 · dispatched by L1 KasegiR41 (hyaku run 10, run-10
fresh-start round).
Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (the only lane repo).
Fleet root `/home/vgpnk/Projects/shokunin` and `/home/vgpnk/Projects/shokuknow` were read
only; nothing was written there. `/home/vgpnk/Projects/shokuknow`'s campaign tools were
never run.

Deliverable: `.ufo/waves/round-41/wave1/ExecC2Instruments.txt` — 404 lines, 20613 bytes,
sha256 `bd043f293ad15f741f4bcdfb5e26cadc4310b89b353990ade86f79bb88229de1`. It contains the
post-integration instrument runbook (exact ordered command list with expected outputs), the
measured base-tree baseline outputs, the base→after delta table, the measured integration
order, and the falsification-probe table. It is the landable bytes for the L1; this receipt
carries the evidence and the notes.

## Base-hash correction (received from the L1 mid-seat)

The dispatched prompt and the frozen `claims.json` carry a **38-character** base literal
`5b29ea1439450b712581edf5f0bf98dfb262ab`, which is not a valid SHA-1 and resolves to no
object:

```
$ git -C …/kasegi-shokunin cat-file -t 5b29ea1439450b712581edf5f0bf98dfb262ab
fatal: Not a valid object name 5b29ea1439450b712581edf5f0bf98dfb262ab
```

The real base commit is the 40-character `5b29ea1439450b712581edf5f0f0bf98dfb262ab`
(`5b29ea1 round-40 verifier spot-check (integrator, hyaku): non-author admit/reject`). The
L1 confirmed this in-band and pointed at `.ufo/waves/round-41/wave1/CORRECTIONS-L1.md` +
the live `claims.json`. Every base-tree run below uses the 40-char hash.

**Carry-forward risk for the L1.** The frozen `claims.json` still carries the 38-char
literal in its `base` field and in the C1 predicate's counting command
(`bash corpus/instruments/r41-closure.sh --export-ref 5b29ea1439450b712581edf5f0bf98dfb262ab`).
That literal resolves to nothing, and the closure-script shape makes the failure hard:

```
$ git -C …/kasegi-shokunin rev-parse --verify --quiet "5b29ea1439450b712581edf5f0bf98dfb262ab^{commit}"
rc=1                       # no output: the object does not exist
$ git -C …/kasegi-shokunin rev-parse --verify --quiet "5b29ea1439450b712581edf5f0f0bf98dfb262ab^{commit}"
5b29ea1439450b712581edf5f0f0bf98dfb262ab
rc=0
```

`corpus/instruments/r40-closure.sh` (the shape the round-41 suite follows) resolves the ref
at `:312` with `git -C "$LANE" rev-parse --verify --quiet "${want}^{commit}"` and dies at
`:313` with `cannot resolve export ref in $LANE: $want` when that fails; and its receipt
parser at `:379` matches `^export-ref=[0-9a-f]{40}$` — a 40-hex requirement, so a 38-char
literal is not merely unresolvable but also unrecordable in the receipt the suite tees. The
base negative control therefore cannot produce its expected red as the claim is currently
worded. The C1 seat should either resolve the export ref leniently (abbrev/prefix match) or
the L1 should correct the literal in the live claims before the C1 gate runs. This seat did
not edit `claims.json` (fleet-owned, L1-landed).

## What was run, and what it showed

### 1. CLI shapes (task item 1)

Read from `--help` at the base tree; recorded in the runbook §1. All four are stdlib-only
Python 3, no network, no writes outside their own scratch dir.

- `source-recheck.py --manifest <path> --source S### [--selftest]` — both args required for a
  lane check; with neither, exit 2 `manifest UNAVAILABLE reason=missing-required-argument`.
- `capture-binding-check.py [--root DIR] [--selftest] [--scratch DIR]`
- `frontier-recheck-count.py [--root DIR] [--json PATH] [--selftest] [--scratch DIR]`
- `recheck-audit.py [--root DIR] [--foreign DIR] [--cdroot DIR] [--expect PATH] [--json PATH] [--selftest] [--quiet]`

### 2. Baseline on the current base tree (task item 2)

All against base `5b29ea1439450b712581edf5f0f0bf98dfb262ab`. The corpus bytes at base and
at lane HEAD `b3b08b2` are identical (`git diff base..HEAD -- corpus` is empty), so these
are also the HEAD numbers.

| gate | measured | exit |
|---|---|---|
| `frontier-recheck-count.py` | `entries=26 pass=26 exit=0` (F01–F23, no F24) | 0 |
| `capture-binding-check.py` | `records=54 bound=54 unbound=0` (16 manifest dirs) | 0 |
| `recheck-audit.py --quiet` | `strict pass=59/59`, `lines=59 total=59 pass=59 fail-closed=24`, `expect=present expected=59 missing=0 unexpected=0 exit=0` | 0 |
| `source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source S060` | `S060:sha256 OK` + 3 quote lines `anchor=N-ok` | 0 |
| `source-recheck.py --manifest corpus/source-snapshots/round-41/manifest.json --source S063` | `manifest UNAVAILABLE reason=missing` | 2 |
| `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `W04 S028`, `W04 S029`, `kasegi ok` | 0 |

Base-tree counters: frontier 23, admitted 23, registry 62, S063 rows 0, entries citing S063
0, knowledge files 59, queued 0, r22 measure `43/43`.

The claim's expected baseline is confirmed exactly: `entries=26 pass=26`, `records=54`,
`expected=59`.

### 3. F24 stand-in mirror, full chain green (task item 3)

Mirror built at `/fast/scratch/hyaku/kasegi-r41/ExecC2Instruments/mirror` by
`git -C <lane> archive b3b08b2 | tar -x` (read-only git; no mutating git or jj command was
run anywhere), with the round-40 F23 artefacts placed under the F24 names. **The stand-in
lives only in scratch and is not landable bytes**: the capture is a byte copy of
`corpus/source-snapshots/round-40/S060.txt` (sha256 `d68626222139e8399bd421bbf023c030e6cace071cacbfc8abe659c629ce6779`,
4889 bytes, 111 lines) renamed to `S063.txt`, with the manifest record's
`url`/`capture_url` set to `https://www.rfc-editor.org/rfc/rfc9116.txt` so binding rule B5's
byte-equality comparison holds. The real RFC 9116 capture replaces it at landing.

Full-chain result on the mirror — every C2 after-state reached:

```
PASS     F24  knowledge/rfc-9116-security-txt.md                   ids=S063           exit=0
entries=27 pass=27 exit=0
MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=55 with_url=55 with_fetched_utc=17 with_archival=38 snapshot_dirs=17 manifest_dirs=17 missing_manifest=0 multi_row_url=3 orphans=1 orphan=S040-live.txt
records=55 bound=55 unbound=0
strict pass=60/60 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=36 gated=24 broken=0
lines=60 total=60 pass=60 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=60 missing=0 unexpected=0 exit=0
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	…/corpus/SOURCES.md
```

Counters on the mirror: frontier 24, admitted 24, registry 63, S063 mined 1, entries citing
S063 1, knowledge files 60, queued 0, measure `44/44`. Every value the C2 claim names is
reached, and the census carries only the standing W04 S028/S029 warnings — no new W/E code.

Note the `executes=35 → 36` delta against the base's `executes=35`: the new entry's recheck
line exits 0 (it is `executes`, not `gated`), while `gated` stays at 24.

### 4. Integration order (measured, not asserted)

Seven fresh extractions, each adding exactly one artefact, all four gates plus the measure
run at each step (runbook §5). The binding constraints this exposes:

- **registry row ↔ knowledge entry are a pair.** The registry row alone (step 2) leaves the
  census red with `E11 S063 missing used-by corpus/knowledge/rfc-9116-security-txt.md` —
  the census resolves the `used-by` cell against the tree on disk. The entry alone (step 3)
  leaves the audit red with `unexpected=corpus/knowledge/rfc-9116-security-txt.md` — the
  expected-list does not name it. Both must land together (or in one commit).
- **the expected-list row must land with the entry** (step 3→4).
- **the manifest record must land with the registry row** (step 1→2): capture + manifest
  alone leave `capture-binding-check.py` red with `FAIL rule=no-row record=S063 dir=round-41`.
- **the README F24 frontier row is what moves the harness and the measure** (step 5): the
  harness reaches `entries=27 pass=27` and the measure reaches `44/44` only then.

Working order: capture + manifest → registry row → knowledge entry → knowledge-expected.txt
row → README coverage-map row + F24 frontier row → PROVINCE.md F24 amendment. Landing all
six in one commit satisfies every gate simultaneously, which is what the L1 should do.

### 5. Falsification probes (runbook §6)

Seven probes against scratch copies of the mirror, one mutation each; every probe red at the
named gate:

| probe | mutation | observed |
|---|---|---|
| A | delete the S063 registry row | binding `FAIL rule=no-row record=S063 dir=round-41`, `records=55 bound=54 unbound=1`, exit 1 |
| B | empty `sources` in the round-41 manifest | `source-recheck` exit 2 `missing-sources`; frontier `FAIL F24 … problems=manifest-missing-ids`, `entries=27 pass=26 exit=1` |
| C | remove the new row from `knowledge-expected.txt` | audit `expected=59 … unexpected=1 exit=1`, exit 1 |
| D | append one byte to the capture | `S063:sha256 MISMATCH expected=d6862622…6779 actual=e32faaf8…4341`, exit 1 |
| E | S063 status cell → `queued` | census **exit 0** (it does not reject `queued`); measure moves to `44/45` |
| F | S063 tier cell → `Z` | census `E06 S063 tier=Z`, exit 1 |
| G | F24 frontier status cell → `queued` | frontier harness **stays green** at `entries=26 pass=26 exit=0`; measure moves to `43/44` |

**Two gaps worth the L1's attention.** Probes E and G show that neither the census nor the
frontier harness rejects a `queued` row: the census accepts a queued registry row, and the
frontier harness simply drops a non-admitted frontier row and stays green. The r22 measure
(§2 step 7) is the only gate that holds the C2 after-state together against both. A lander
who verifies only the four instruments and the census would miss a `queued` F24/S063 row and
still report a green chain. The measure is cheap and already in the runbook; it should be
run at every integration point, not only at the end.

## Tooling

No tools installed or upgraded. Everything used was already present: `git` (read-only
`archive`/`log`/`diff`/`cat-file`/`rev-parse`), `python3` (stdlib), `bash`, `gawk`, `tar`,
`grep`/`awk`/`sed` via the read/grep/bash tools. The host's pacman transactions are paused
fleet-wide and were not touched.

## Network fetches

None. The F24 stand-in reuses the round-40 F23 capture bytes already committed in the lane;
no URL was fetched. Therefore there is no HTTP status / byte count / UTC fetch time to
record for a fetch.

## Write scope

Exactly two lane paths written, both under `.ufo/waves/round-41/wave1/`:

- `ExecC2Instruments.md` (this receipt)
- `ExecC2Instruments.txt` (the deliverable)

No lane file, no fleet-root file, no sibling lane repo, and no source tree was edited.
`claims.json`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `SHONEN.md`, `PROVINCE.md`,
`corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/instruments/` and
`MANIFEST.json` were read only. No mutating git or jj command was run anywhere.

## Scratch hygiene

`S=/fast/scratch/hyaku/kasegi-r41/ExecC2Instruments` — all scratch (mirror, order ladder,
probe copies, evidence files, the two driver scripts) lived under it and it was removed
before this receipt was written. `TMPDIR` was set explicitly to `$S` for every instrument
run; no run relied on an inherited `TMPDIR`. The disk guard was green before the heavy
pass (`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`).

## Risks / notes for the L1

1. **The 38-char base literal in `claims.json`** (above) is a live blocker for the C1
   base negative control if `r41-closure.sh` resolves `--export-ref` strictly through git.
2. **The `queued`-row gaps** (probes E, G) — run the measure at every integration point.
3. **The census's `E11` used-by rule** means the S063 registry row and the new knowledge
   entry must land together; a single-commit landing of the whole C2 set avoids the
   transient reds.
4. **`recheck-audit.py --selftest` prints no `selftest cases=N failures=F` summary line** —
   unlike the other three. A receipt that quotes a `cases=17` summary for it would be
   fabricated; the runbook states the real shape (17 `selftest <case> … ok` lines over 18
   printed lines, including a `completeness` sanity line that is not a case).
5. **`frontier-recheck-count.py` counts entries, not frontier rows.** `entries=27` is 27
   admitted *entry files* across 24 frontier rows (F09, F10 and F11 each name two entries:
   24 rows + 3 extra entries = 27, measured); a checker that expects
   `entries == frontier rows` will mis-read 27 against 24. The runbook states both numbers.
6. The census roster resolves lanes from the fleet `shokunin.conf`; a mirror run needs a
   copy of that conf at the mirror root, or `--root <mirror>` finds no lanes.
7. `recheck-audit.py` on a mirror needs the recheck lines' `cd` target rewritten to the
   mirror (round-40 `MutEntries.md` §B1 precedent) or `--cdroot` pointed at the live lane;
   otherwise the audit measures the live lane and the mirror is not measured at all
   (measured: an unadapted mirror run reports `lines=59 total=59 … exit=1` with
   `--cdroot <mirror>`, and exit 0 against the live lane).
