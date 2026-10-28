# ExecJ4Decl — round 42 wave 1, J4 / family F-DECL

Seat: `ExecJ4Decl` (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Round base `5053a7f46de35784cff4b56756906e9014a38276`; ref exercised for the
transcript `514ff62d61ee9bc717a20a02a22c65ec0c5124ed` (the lane HEAD as I read it,
not a judged head — the L1 names J and Y). No lane, fleet-root, sibling-lane or
source-tree file was written; no mutating git/jj command was run; no tool was
installed; no network fetch was made.

## Deliverables (landable bytes; validation evidence is below, not inside them)

| deliverable | lines | sha256 |
|---|---|---|
| `ExecJ4Decl.sh` (sourceable limb `check_j4`) | 806 | `ff5b811f1972a1b170e35114349c9bcbb4589d4cba32f9eddf19502236a0c98b` |
| `ExecJ4Decl.declared-blocks.txt` (regenerated declarations) | 324 | `dd73e00e41e187ed4a1ecb6906008b64e9603c3692b1035b4318e3ee37ab2d65` |
| `ExecJ4Decl.transcript.txt` (17 sections, every line a real command output) | 139 | `5ba210f46ffecd3869cc3327ec0f30aa35321efe79451dfdbe90a4a5c4c7170a` |

## What J4 grades (four clauses, one validator over the export)

`check_j4 TREE REF` prints `declared=..,valid=..,pinned=..,dyn=..,malformed=..,paths=..,canon=..,symlink=..,nul=..,diff-read=..,changed=..,changed-undeclared=..,changed-symlink=..,reads=..,reads-undeclared=..,literals=..,literal-undeclared=..,ledger=..,file=..`
and returns 0 only when every clause holds. `j4_line TREE REF` wraps it in the
suite grammar `J4 payload=... closed=0|1`.

1. **Declaration validity.** Every pinned record binds real bytes and binds them
   to the *changed region*: `tail -n <lines>` must hash to the declared digest;
   when the path changed since the base ref the diff's add count must equal
   `<lines>`, deletions must be 0, the base blob must be a byte PREFIX of the
   graded file (an append, not an in-place edit), and the appended bytes must
   equal the bound region byte for byte. The checker does not trust the record —
   it recomputes the binding with the same `j4_pin` the generator used and
   requires equality. Unchanged paths and non-append changes are pinned to the
   WHOLE file (strictly stronger than a tail binding).
2. **Containment.** Every declared path is lane-relative, has no `.`/`..`/empty
   component and no absolute prefix, has no symlink in ANY component, and its
   `realpath -m` resolves UNDER the export root. Symlink escape, `..` escape and
   absolute paths are each rejected (measured below).
3. **Coverage** — the CritDeclarationCoverage closure. Every path changed
   between the base ref and the graded ref must be declared (a changed symlink is
   counted in `changed-symlink` instead: a symlink can never be declared, so
   requiring it would make the check unsatisfiable); every path read through the
   guarded accessor `j4_read` is declared (read ledger); every lane-relative
   artifact path the exported suite names literally and that exists in the export
   is declared.
4. **Non-vacuity.** An empty or missing declaration file is red.

Format of `.ufo/waves/round-42/declared-blocks.txt` — **always three
whitespace-separated fields**, so the round-41 grammar and any reader using
`awk 'NF>=3 {print $1}'` sees every declared path:

```
<path> <lines> <sha256>    pinned (see clause 1)
<path> dyn unpinned        declared, not hashed — exactly three paths use it:
                           the declaration file itself, the suite file (its
                           bytes are pinned by the receipt's suite-sha256,
                           graded by J8) and the receipt (it does not exist
                           until the run that writes it)
```

Delivered file: 324 records, 321 pinned, 3 `dyn unpinned`. Determinism was
measured: two regenerations of the same ref are byte-identical.

## Routed defects this closes

**T7 (declared path read outside the export through a symlink).** The committed
byte transcript is `.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt` lines
22-25 (section `## D2  H9 symlink out-of-export read (T7)`): `numstat: 1 0 pwn`
/ `rc=0 payload=declared=1,valid=1,tail=1,pure=1,paths=1,diff-read=ok`. Section 5
of the transcript reproduces that shape exactly — `pwn` is a symlink to a file
outside the export and the declared digest *is* the digest of those outside
bytes, so the old digest clause passes — and J4 rejects it with
`paths=0,canon=0,symlink=1`, exit 1. Section 6 additionally replaces an
already-declared real path (`corpus/README.md`) with a symlink to `/etc/hostname`
and gets the same rejection.

**CritDeclarationCoverage (declarations were a validated subset, not a
completeness assertion).** `declared_blocks_check` (r41-closure.sh:1054-1115)
never enumerated `BASE..REF`; `check_i5` (1118-1125) only ran it. J4 adds the
changed-path-set clause, so an undeclared changed path is a defect rather than an
unvisited path. Section 10 removes one changed path (`census-before.txt`) from
the declaration set and the check prints `changed=12,changed-undeclared=1`,
exit 1.

Also closed, because they are the same family: an **unchanged** undeclared path
that the suite reads (ConnWave2Seed item 92, DECL-READ-UNDECLARED) is rejected by
the literal clause — section 15 measures `literals=2,literal-undeclared=1`,
exit 1, and exit 0 after the path is declared; and an **undeclared read through
the accessor** is rejected twice over — `j4_read` refuses it (exit 3,
`j4_read: undeclared path ...`) and the ledger clause reds the run
(`reads-undeclared=1`), section 7.

## Retained evidence (exact, from `ExecJ4Decl.transcript.txt`)

Green over the judged export (section 4):

```
declared=324,valid=324,pinned=321,dyn=3,malformed=0,paths=1,canon=1,symlink=0,nul=0,
diff-read=ok,changed=12,changed-undeclared=0,changed-symlink=0,reads=0,reads-undeclared=0,
literals=0,literal-undeclared=0,ledger=ok,file=present        [exit=0]
```

Rejections, each a one-line payload and its exit code:

| § | probe | discriminating fields | exit |
|---|---|---|---|
| 5 | T7: declared `pwn` is a symlink to outside bytes whose digest `557c6d0a…` equals the declaration | `paths=0,canon=0,symlink=1` | 1 |
| 6 | declared `corpus/README.md` replaced by `-> /etc/hostname` | `paths=0,canon=0,symlink=1` | 1 |
| 7 | `j4_read` of an undeclared path, then the ledger records that read | `reads=1,reads-undeclared=1` (and `j4_read` exit 3) | 1 |
| 8 | declaration `../outside-fixture.md 1 …` | `paths=0,canon=0` | 1 |
| 9 | declaration `/etc/hostname 1 …` | `paths=0` (digest would match) | 1 |
| 10 | one changed path removed from the declaration set | `changed-undeclared=1` | 1 |
| 11 | `corpus/README.md 1 000…0` (tampered pin) | `valid=324 < declared=325` | 1 |
| 12 | empty declaration file | `declared=0,changed-undeclared=12` | 1 |
| 13 | base export / r41 judged-head export | `file=missing` | 1 / 1 |
| 15 | suite literal `considerthese/2026-10-26.md` undeclared, then declared | `literal-undeclared=1` then `0` | 1 then 0 |

Additional measured properties:

* **Y transition (section 14):** the declaration generated for the judged tree
  still validates after the receipt is added (`changed=12` unchanged,
  exit 0) — the receipt is `dyn unpinned`, so `Y = J + receipt` cannot invalidate
  a pin.
* **Non-vacuity and negative controls (sections 12-13):** empty declaration red;
  base and the round-41 judged head are red because no round-42 declaration file
  exists there — so J4 contributes a real red to `closed<13/13 exit=1` at both
  negative refs, and cannot be green vacuously.
* **Suite grammar (section 16):** `j4_line` prints
  `J4 payload=... closed=1` on the green export and `closed=0` on the tampered
  one.
* **Edge cases** were exercised on a throwaway repo (asserted
  `git rev-parse --show-toplevel` == the fixture dir before committing): a new
  file, an append with no trailing newline, an in-place edit with a deletion, a
  normal append, and a committed symlink (`changed-symlink=1`). All resolve to a
  binding the checker accepts; the fixture run is
  `declared=8,valid=8,changed-undeclared=0,exit=0`.
* **The lane was not written to:** `git -C <lane> status --porcelain | grep -c
  ExecJ4Decl` → `0` (section 17).

## Integration contract for the L1 (the ordering matters)

1. Land everything the round carries **except** `.ufo/waves/round-42/declared-blocks.txt`
   — the r42 suite, the C2 corpus bytes, the wave receipts. J4's literal and
   changed-path clauses read the suite *from the export*, so the suite must be in
   the tree before the declaration is generated.
2. Generate the declaration for the tree you are about to commit. Either
   * after committing that tree as `J0`:
     `bash ExecJ4Decl.sh --regen <lane> 5053a7f46de35784cff4b56756906e9014a38276 J0 .ufo/waves/round-42/declared-blocks.txt`
   * or in the working tree (`git add -A` first, so no stray untracked file is
     declared): `bash ExecJ4Decl.sh --regen-work <lane> 5053a7f… .ufo/waves/round-42/declared-blocks.txt`
   `--regen` validates nothing about its own output; run `--check` on the export
   of the commit before landing the receipt.
3. Land the generated file and commit `J`. Re-run step 2 if any further file
   lands: a landing after generation is an undeclared changed path by design.
4. Wire the limb into `corpus/instruments/r42-closure.sh`: source it, set `LANE`
   and `WORK`, and emit `j4_line "$tree" "$ref"`. Reads of export artifacts
   **should** go through `j4_read` — that is what makes the read ledger
   authoritative; the literal and changed-path clauses already catch a named or a
   changed artifact, and `j4_read` catches a path built at runtime from a
   computed name.

Environment knobs (documented in the limb header, inert unless set):
`R42_DECLARED`, `R42_READ_LEDGER`, `J4_BASE`, `LANE`, `J4_DISABLE_LITERAL`.

## Risks and limits

* **The delivered declaration file is generated for `514ff62`, not for the judged
  head.** It is the landable output of `--regen` for the tree I could read; the
  L1 must regenerate at `J` (step 2). Landed unchanged after further changes it
  will red J4 — correctly, but it must not be shipped stale.
* **Documented limit.** The literal clause reads only path-like literals of the
  exported suite file that exist as regular files in the export. A path built at
  runtime from a computed name is invisible to it; it is covered by the
  changed-path clause (if the artifact changed) and by the `j4_read` ledger (if
  the suite routes the read). The clause set is deliberately layered, and this
  hole is stated rather than hidden.
* **`changed-symlink` counts rather than reds.** A symlink changed in the round
  is exempt from the declaration requirement because a declared symlink is always
  rejected by clause 2; the exemption is reported in the payload so it is
  visible. If the L1 prefers a hard red there, it is a one-line change
  (`changed-symlink` added to the exit condition).
* **The limb sets `set -uo pipefail` at load** (the lane's suite convention,
  r41-closure.sh line 1). A host script that sources it without already running
  under `-u` inherits that.
* **Performance:** the changed-path, ledger and literal clauses each re-read the
  declaration file per lookup; a 324-record file and ~350 lookups take a couple
  of seconds, measured in the transcript.
* No blocker: every clause has a measured green and a measured red.

## Scratch

`/fast/scratch/hyaku/kasegi-r42/ExecJ4Decl/` was removed after the deliverables
were copied into this wave directory.

Report: .ufo/waves/round-42/wave1/ExecJ4Decl.md
