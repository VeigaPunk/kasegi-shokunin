# ExecForgeFixtures — round 40, wave 1 (executor)

## Item

Produce two minimal receipt fixtures for H5 (`a forged/tampered receipt — a recorded payload contradicting
the export, or a future-dated run-utc — is rejected`), plus `expected.txt` naming the verdict the suite MUST
print for each. Axes named up front: **depth:verifiability** (H5's discriminating power). `coverage` and
`depth:density` are untouched by this item. No lane file outside this seat's wave-dir deliverables was
written; no git/jj mutation was run.

## Deliverables (byte stats, measured)

| File | Lines | Bytes | sha256 |
|---|---|---|---|
| `ExecForgeFixtures.forged-payload.txt` | 33 | 1550 | `09388af91592e51f867de95cb755f2e822d6a15d43a5e9f69a64cb18cf281cef` |
| `ExecForgeFixtures.future-dated.txt` | 33 | 1528 | `2a1f2c77466edab3a728868e7fe378f07df9738115435a43bd4a395e584be9ee` |
| `ExecForgeFixtures.expected.txt` | 2 | 554 | `4bc9f96a7a70fced5db81e00b29c7a05b14f9bf9b0bf0f1066c8c0f5a5e8ff55` |

Both receipts are round-40-shaped transcripts (sentinel, `export-ref`, `suite-sha256`, `run-utc`,
`== run ==` with ten `H<n> payload=... closed=1` lines and `closed=10/10 exit=0`, `== selftest ==` with ten
graded `selftest case=H<n> positive=pass mutants=n/n verdict=pass` lines and `selftest cases=10 failures=0`).
No trailing whitespace or tabs (`grep -nP '[ \t]+$|\t'` → none).

Binding of both fixtures (immutable, already the frozen predicate's own red-control ref):

```
$ git -C <lane> log -1 --format='%H %cI %ct' 8371e7ac9f32cae5ed72f8c28205634603f836fa
8371e7ac9f32cae5ed72f8c28205634603f836fa 2026-10-26T17:55:17-03:00 1793048117
$ date -u -d '2026-10-26T17:55:17-03:00' +%Y-%m-%dT%H:%M:%SZ
2026-10-26T20:55:17Z
```

## The two violations

**(1) forged payload.** `H2 payload=corrections=4,files=4 closed=1` records four `Correction (round 40)`
lines across four files. Re-derived from the export of the receipt's own `export-ref`, on the same
`git archive | tar -x` path the suite uses:

```
$ git -C <lane> archive 8371e7ac9f32cae5ed72f8c28205634603f836fa | tar -xf - -C export
$ grep -Hc '^Correction (round 40)' export/SCORECARD.md export/LOG.md export/SHONEN.md export/corpus/lessons/round-39.md
export/SCORECARD.md:0
export/LOG.md:0
export/SHONEN.md:0
export/corpus/lessons/round-39.md:0
total=0 files-with=0
```

The claim (4 in 4) and the tree (0 in 0) cannot both hold; the value is absent from the export, which is
exactly the frozen example ("a check line claims a correction count that is absent from the export").

**(2) future-dated.** `run-utc=2027-01-01T00:00:00Z` against the export commit time of its own
`export-ref`:

```
$ date -u -d '2027-01-01T00:00:00Z' +%s        -> 1798761600
$ git -C <lane> log -1 --format='%ct' 8371e7ac -> 1793048117
```

`1798761600 > 1793048117` (2027-01-01T00:00:00Z vs 2026-10-26T20:55:17Z): the transcript is dated after the
tree it describes exists, so it cannot be that tree's run. Design note: the honest fixture sets
`run-utc` **equal** to the export commit time (the only instant inside the `ref_ct <= run-utc <= cont_ct`
window when `--contained-in` defaults to the export ref), so the date limb is satisfied by construction and
the two fixtures differ in exactly one limb each.

## Validation (commands + actual output)

Replicas were written in scratch (`$S/naive-shape.sh`, `$S/strict-h5.sh`) because
`corpus/instruments/r40-closure.sh` does not exist yet (checked: absent from the lane tree and from the
wave dir at 18:21; the `ExecSuiteBuild` wave-1 deliverable had not landed when this seat finished).

**Naive fix (shape-only, r39 G2 semantics with H ids: sentinel, ten `closed=1` run lines, `closed=10/10`,
ten graded case lines, summary — payload values never compared, `run-utc` never read). It accepts both:**

```
naive-shape ExecForgeFixtures.forged-payload.txt sentinel=1,run-lines=10,closed-lines=0,distinct-ids=10,closed-line=1,graded-cases=10,ungraded-cases=0,selftest-summary=1 accepted=1
naive-forged exit=0
naive-shape ExecForgeFixtures.future-dated.txt sentinel=1,run-lines=10,closed-lines=0,distinct-ids=10,closed-line=1,graded-cases=10,ungraded-cases=0,selftest-summary=1 accepted=1
naive-future exit=0
```

**H5 limb (named, recomputable fields: H2 `corrections=`/`files=` vs the export; `run-utc` vs the export
commit time). It rejects both, on different limbs, and accepts the honest control:**

```
H5 payload=xref=1,run-utc=2026-10-26T20:55:17Z,corrections=0(recorded=4),files=0(recorded=4),dated=ok closed=0
strict-forged exit=1
H5 payload=xref=1,run-utc=2027-01-01T00:00:00Z,corrections=0(recorded=0),files=0(recorded=0),dated=future closed=0
strict-future exit=1
--- control: future-dated fixture with line 4 restored to run-utc=2026-10-26T20:55:17Z
H5 payload=xref=1,run-utc=2026-10-26T20:55:17Z,corrections=0(recorded=0),files=0(recorded=0),dated=ok closed=1
control exit=0
```

Isolation is therefore real, not asserted: `forged-payload` fails only `corrections`/`files` (`dated=ok`);
`future-dated`'s recorded `corrections=0,files=0` *matches* the export, so its only failing limb is
`dated=future`; flipping that one line to the honest value yields an accepted receipt.

**Third-party code, not mine:** `ExecMistakesDraft.h5-replica.sh` (another seat's limb replica) run against
both fixtures prints the same split, plus `digest=1,xref=1` — the header is resolvable at the named ref under
the round-39 receipt checker, so the rejections below come from the payload/date limbs, not from a malformed
header (`declared=0` is that replica's r39-specific `G1 declared=` field, which only exists in round-39
receipts):

```
H5 payload=version=1,xref=1,digest=1,declared=0(recorded=none,export=2),run-utc=2026-10-26T20:55:17Z,dated=ok closed=0
replica-forged exit=1
H5 payload=version=1,xref=1,digest=1,declared=0(recorded=none,export=2),run-utc=2027-01-01T00:00:00Z,dated=future closed=0
replica-future exit=1
```

## Consumption contract (for the H5 graded case and L1 integration)

1. `forged-payload.txt`: assert the **payload limb** — recompute `^Correction (round 40)` count/files from
   the export at the receipt's `export-ref`, compare to `H2 payload=corrections=,files=`; expect mismatch
   (0 vs 4 / 0 vs 4) and the receipt **rejected** (`closed=0`; the run must not print `closed=10/10`).
   Verdict/reason are in `expected.txt`.
2. `future-dated.txt`: assert the **date limb** — `run-utc` (2027-01-01T00:00:00Z) vs the export commit
   time (2026-10-26T20:55:17Z); expect `future-dated` and the receipt **rejected** (`closed=0`). Its
   `H2 payload=corrections=0,files=0` is deliberately truthful at the named ref so the payload limb stays
   green and the date limb carries the rejection alone.
3. Both fixtures are *fabricated transcripts for a pre-round-40 ref* (no `r40-closure.sh` and no
   `Correction (round 40)` line exists at 8371e7ac), so any limb set that also checks suite presence/digest
   against `corpus/instruments/r40-closure.sh` will additionally red at that ref. The assertions above are
   limb-scoped for that reason; they do not claim the fixtures are otherwise-acceptable receipts.
4. **Rebinding rule if the H5 case wants them at J/Y instead:** replace header lines 2–4 (`export-ref`,
   `suite-sha256`, `run-utc`) and the run-context line's `export-ref=`/`suite-sha256=` with the J/Y values
   and keep the defect: for (1), set `H2 corrections=` to a count that is *not* the export's recomputed
   count (as delivered it is 4 vs 0, so no edit is needed at all at the named ref — only a rebind needs the
   value re-picked); for (2), keep `run-utc` later than the export commit time. The golden path that needs
   no rebind is the one-field mutation of the genuine receipt at Y:
   `sed -E 's/^(H2 payload=corrections=)[0-9]+/\1<n+1>/'` (payload) and
   `sed -E 's/^run-utc=.*/run-utc=2027-01-01T00:00:00Z/'` (date) — the wave-2 `CritReceiptForge` item does
   the same two mutations on the committed receipt.
5. Sentinel: line 1 is `all-gates v6` (the successor of the committed round-39 receipt's `all-gates v5`).
   The round-40 suite's sentinel token was not observable when this seat ran; if it differs, the fixtures
   are still rejected (the required verdict), and the limb-scoped assertions above are unaffected. The
   suite builder owns the token, not this seat.

## Risks / notes

- `suite-sha256` in both headers is `2856a210…`, the digest of the round-39 instrument resolvable at the
  named ref (confirmed: `sha256sum export/corpus/instruments/r39-closure.sh`). Deliberate: it makes the
  header well-formed for the only receipt checker that exists today while leaving the transcript visibly
  bound to the round-39 instrument — part of the fabrication (the R1 class), not the declared defect.
- The forged value `corrections=4,files=4` is permanently false at 8371e7ac (0). If L1 rebinds fixture (1)
  to Y without re-picking the value and the round happens to land exactly 4 correction lines in 4 files,
  the forgery would evaporate; the rebinding rule above exists for that case.
- No r40 suite bytes existed at run time, so no end-to-end `--selftest` evidence is claimed here. The H5
  limb was proven with two independent implementations (this seat's `strict-h5.sh` and another seat's
  `h5-replica.sh`) plus a shape-only negative control that accepts both fixtures.
- Tooling: nothing installed, upgraded or downloaded (no pacman, no network, no `uv`/`npx`).

## Scratch

`S=/fast/scratch/hyaku/kasegi-r40/ExecForgeFixtures` (export, replica scripts, control receipt) held all
work; deliverables were copied into `.ufo/waves/round-40/wave1/` first, then `$S` was removed at yield
(`rm -rf -- "$S"`). No scratch path survives.

Report: .ufo/waves/round-40/wave1/ExecForgeFixtures.md
