# ExecControls — round-42 C2 junk twin control (kasegi-shokunin, wave 1)

Seat: ExecControls (executor). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Scope: the C2 junk twin control named in `.ufo/waves/round-42/claims.json` (claim C2,
kill rule: "a junk twin accepted (a mined-marked row without capture+entry+harness pass
— the O4 class)").

## What I built

A junk twin is fabricated on a scratch copy of the lane corpus and every named instrument
is run against the mutated copy. The fabricated twin is exactly the O4 class the C2 kill
rule names:

- a registry row `| S999 | ... | mined | ... |` whose `used-by` cell names a knowledge
  file that does not exist;
- an F25-lookalike frontier row `| F25 | ... | admitted | knowledge/junk-f25-osv-schema.md | S999 | ... |`
  naming an entry that does not exist;
- a snapshot manifest that *claims* S999 with no `url`, no `fetched_utc` and no capture
  bytes behind it;
- and no knowledge entry, no capture file, and no harness pass.

The arms are a monotone ladder (base → J1 → J2 → J3 → J4 → J5 → J6), each arm adding one
layer of fabrication, plus a live-tree replay (LIVE-J3) and one labelled probe (P5).

## Result: the twin is rejected by all three named instruments

| arm | what it adds | frontier-recheck-count.py | capture-binding-check.py | sources-census validate |
|---|---|---|---|---|
| base | pristine (positive control) | exit 0 `entries=27 pass=27` | exit 0 `records=55 bound=55 unbound=0` | exit 0, no E-code |
| J1 | registry row only | exit 0 | exit 0 | **exit 1** `E11 S999 missing used-by` |
| J2 | + F25 frontier row | **exit 1** `FAIL F25 ... problems=missing-entry` | exit 0 | **exit 1** `E11` |
| **J3** | **+ manifest claiming S999 (the full O4 twin)** | **exit 1** `entries=28 pass=27` | **exit 1** `records=56 bound=55 unbound=1` | **exit 1** `E11` |
| J4 | + fabricated entry file | **exit 1** `problems=no-recheck-line,no-source-selection,no-manifest` | **exit 1** `unbound=1` | exit 0 |
| J5 | J3 with `used-by` = em-dash (census limb blinded) | **exit 1** | **exit 1** `unbound=1` | exit 0 (W03 only) |
| J6 | J3 + entry carrying a `recheck:` line | **exit 1** `problems=recheck-exit-2` | **exit 1** `unbound=1` | exit 0 |
| LIVE-J3 | the same O4 twin on a copy of the **live** lane tree | **exit 1** | **exit 1** `unbound=1` | **exit 1** `E11` |

Every instrument's own exit status is the verdict, and every one of the three named
instruments reds on the twin independently — none of them is load-bearing alone:

- the **frontier harness** rejects it on two different limbs — `missing-entry` when the
  entry file is absent (J2/J3), and `recheck-exit-2` when a fabricated entry does carry a
  `recheck:` line (J6), and `no-recheck-line,no-source-selection,no-manifest` when the
  entry exists but declares nothing (J4);
- the **capture-binding check** rejects it on rule B (`FAIL rule=url-mismatch record=S999
  detail=absent`) and rule C (`FAIL rule=provenance-missing record=S999`), so `unbound=1`;
- the **census** rejects it on E11 (`S999 missing used-by corpus/knowledge/junk-f25-osv-schema.md`).

J5 is the sharpest arm for the conjunction claim: with the row's `used-by` cell set to the
em-dash the census's E11 limb cannot fire at all (it prints only `W03 S999 mined but
unused`), and the twin is *still* rejected by the frontier harness and the capture-binding
check, both exit 1.

The fourth C2 instrument, `recheck-audit.py --quiet`, adds a second independent rejection
on the arms that write a knowledge file: J4 and J6 read `expected=60 missing=0 unexpected=1
exit=1` (the fabricated entry is on disk but not on the expected list), while J3 and J5 read
`expected=60 missing=0 unexpected=0 exit=0` — the audit sees no entry at all there, so it
does not reject them. The twin is rejected by at least two of the four C2 instruments on
every O4-class arm.

## The counting-command ledger (why the twin is not a way to reach the after-state)

Measured on J3, against the C2 after-state targets in `claims.json`:

| C2 counting command | after-state target | twin reads | verdict |
|---|---|---|---|
| frontier rows `grep -cE '^\| F[0-9]+ \|'` | 25 | 25 | SATISFIED |
| registry rows `grep -cE S[0-9]{3,}` | 64 | 64 | SATISFIED |
| S064 mined rows (awk, status cell) | 1 | 0 | not satisfied |
| entries citing S064 | 1 | 0 | not satisfied |
| knowledge files | 61 | 60 | not satisfied |
| harness `frontier-recheck-count.py` | `entries=28 pass=28` | `entries=28 pass=27 exit=1` | REJECTED |
| capture binding `capture-binding-check.py` | `records=56 bound=56 unbound=0` | `records=56 bound=55 unbound=1` | REJECTED |
| recheck audit `recheck-audit.py --quiet` | `expected=61 missing=0 unexpected=0 exit=0` | `expected=60 missing=0 unexpected=0 exit=0` | not satisfied |
| census `sources-census.sh validate` | exit 0 | exit 1 (E11) | REJECTED |

The twin **satisfies the two raw row-count greps** — a verifier reading only
`grep -cE '^\| F[0-9]+ \|' corpus/README.md` and the registry-row grep would see the
after-state numbers 25 and 64 on a forged tree. It cannot satisfy the remaining seven.
The C2 after-state is therefore reachable only as a conjunction, never by row-count
arithmetic.

## The measure conjunct

The C2 after-state also names `measure 45/45 = 1.000`. The measure has two conjuncts
(the round-22/round-41 form: the frontier ratio, and the harness passing every admitted
entry). Measured on the arms, `measure: criterion met=no` on J2, J3, J4, J5, J6 and
LIVE-J3, and `yes` on base and J1 (J1 has no frontier row, so the ratio is unchanged).
The twin cannot reach 1.000 on the measure.

## Boundary observation (P5) — reported, not a defect claim

P5 is **not** the junk twin and is outside the O4 class: it carries a self-consistent
forged capture (forged bytes plus a manifest binding them with `url` + `fetched_utc` +
`sha256`), a knowledge entry, a `recheck:` line and the expected-list line. On P5 all
three instruments are green (`entries=28 pass=28`, `records=56 bound=56 unbound=0`, census
exit 0) and the measure reads `criterion met=yes`.

This is a **boundary of the local instrument guard, not a claim defect**: these instruments
verify internal binding and self-consistency, not upstream truth. It is reported because it
is the honest edge of what the control proves, and because it names where the lane's own
admission bar (a human/L2 review of the capture against the upstream document) does the
work the instruments cannot. The transcript labels P5 with a warning banner and marks it
`PROBE, OUTSIDE THE O4 CLASS` so it cannot be read as a junk-twin acceptance.

## Deliverables

| file | landable as | lines | sha256 |
|---|---|---|---|
| `.ufo/waves/round-42/wave1/ExecControls.junk-f25.txt` | `.ufo/waves/round-42/c2-controls/junk-f25.md` | 70 | `f48d2ba73645ddee898cbeddd74f9b95f29a7263aeba906e458e7431848cc8aa` |
| `.ufo/waves/round-42/wave1/ExecControls.junk-recheck.txt` | `.ufo/waves/round-42/c2-controls/junk-f25-recheck.txt` | 1225 | `a96084914a17ec586e56194f42f4afdf13a207efc6bae36f5928ce86b6e9806a` |
| `.ufo/waves/round-42/wave1/ExecControls.replay.sh` | the control's replay tool (not a corpus file; may be left in the wave dir) | 122 | `aee679cdc1af66fecbbfeda842d77e1959cdde0145b34409db01a7f935ec51cd` |

`ExecControls.replay.sh` rebuilds the twin from the lane tree in one command and re-runs
the three named instruments against it, so the control is reproducible without the
transcript:

    bash ExecControls.replay.sh <scratch-dir>

It prints the three instrument outputs with their exit codes and exits 0 when the twin is
rejected by all three (exit 1 when any instrument accepts it — the script is itself a
falsifier). Verified against the live lane tree.

The junk file carries the exact fabricated bytes (registry row, frontier row, manifest)
plus the per-instrument expected rejection, in the house style of
`.ufo/waves/round-38/c2-controls/junk-f21.md`. Both fabricated rows are indented four
spaces, so `grep -c '^|'` on the landed file returns 0 — the landed file cannot be
mistaken for a live table row by any column-0 `^\|` scan.

## Harm check on the landing

Landing `junk-f25.md` at `.ufo/waves/round-42/c2-controls/junk-f25.md` must not perturb
any instrument. Measured on a copy of the live lane tree: the frontier rows / registry rows
/ S064-mined / entries-citing-S064 / knowledge-files counters, the frontier harness, the
capture-binding check, the recheck audit and the census were run before and after the
landing, and **every output was byte-identical** (`VERDICT: instrument outputs
byte-identical before/after the landing = YES`).

## Commands actually run

- `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` — green before the
  heavy pass (root `/fast/scratch/hyaku` 27% used, 592.6G free).
- `git -C <lane> archive 5053a7f46de35784cff4b56756906e9014a38276 | tar -x -C <scratch>/master`
  — the claims' frozen base (the corpus at that commit is byte-identical to the freeze
  commit: `git diff --stat <base> HEAD -- corpus` is empty).
- `tar -C <lane> --exclude=.git --exclude=.jj -cf - . | tar -C <scratch>/master-live -xf -`
  — the live tree copy for the LIVE-J3 arm.
- Per arm: `python3 corpus/instruments/frontier-recheck-count.py`,
  `python3 corpus/instruments/capture-binding-check.py`,
  `python3 corpus/instruments/recheck-audit.py --quiet`,
  `python3 corpus/instruments/source-recheck.py --manifest <junk manifest> --source S999`,
  `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <arm> <arm>`,
  and every C2 counting command verbatim.
- `bash replay.sh <scratch>` — an independent one-shot rebuild of the twin from the lane
  tree; it reproduces the same three rejections and exits 0 (the twin rejected). Verified.

No mutating git/jj command was run anywhere; no lane file was written by this seat other
than the two deliverables and this receipt; `git status --porcelain -- corpus/` is empty.

## Risks / what the L1 should check

1. **The two raw row-count greps are satisfiable by the twin.** If any verifier reads
   `grep -cE '^\| F[0-9]+ \|' corpus/README.md` alone, a forged tree reads 25. The claim's
   conjunction catches it; a counter-only reading would not.
2. **P5 is green.** A self-consistent forgery (forged capture + manifest + entry + expected
   list) is not detected by the three local instruments. This is the instruments' documented
   limit, not a C2 defect — but it means the O4 class is rejected by binding/consistency
   checks, not by an upstream-truth check. The lane's own admission bar covers that.
3. **The census alone is not sufficient.** J4 and J5 show the census going green (exit 0)
   while the twin is still rejected by the other two instruments. The kill clause "a junk
   twin accepted" must be read against the conjunction, not against the census alone.
4. **The row ids are deliberately out of the claimed range.** The twin uses `S999` and an
   `F25`-shaped row so it cannot collide with the real S064/S065/S066 rows the round-42
   C2 work lands; `S999` is not a real lane id and is used nowhere else in the corpus.

## Blockers

None. Note for the L1: the lane HEAD moved during this seat (`0566bd6` → `27e18d2`,
claims erratum 1) and the jj export rewrites old commit objects, so `0566bd6` is no longer
resolvable by hash. The frozen base `5053a7f46de35784cff4b56756906e9014a38276` is still
a live object and is what the arms were cut from; the LIVE-J3 arm was cut from the live
working tree at run time, so the rejection is witnessed on both the frozen base and the
tree the L1 will land on.

## Scratch

`/fast/scratch/hyaku/kasegi-r42/ExecControls` — **removed** after the deliverables and this
receipt were copied into `.ufo/waves/round-42/wave1/` (verified: the path no longer
exists). All work copies, the nine arm trees, the frozen-base and live-tree masters, the
harm-check tree and the replay scratch lived under it (`TMPDIR` pointed there for every
instrument run). No scratch dir of this seat survives.

## Tooling

No tool was installed or upgraded by this seat; the control uses only the lane's committed
instruments, the fleet census script, Python 3.14.8 and GNU coreutils already present.
