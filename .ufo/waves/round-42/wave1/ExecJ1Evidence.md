# ExecJ1Evidence — round-42 wave 1 receipt (J1, family F-EVID)

Seat: `ExecJ1Evidence` (leaf executor). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Axes: depth:verifiability (primary), coverage. No score is claimed by this seat; the L1 integrates.

## 1. Deliverables

| file | sha256 | lines |
|---|---|---|
| `.ufo/waves/round-42/wave1/ExecJ1Evidence.sh` | `20d95cfbbe5f203dc3dbb4808eddf9a61508546904391f19249bf29a49382463` | 574 |
| `.ufo/waves/round-42/wave1/ExecJ1Evidence.transcript.txt` | `07705cb56d16037a00c8f3da113a7106c1d6ee8faa590d6045283c0271743f71` | 107 |

These supersede the first landing (`bd7cff78…` / 554 lines), which carried a latent
dynamic-scope bug in `j1_members` — see §7. The sha256 printed *inside* the transcript is the
sha256 of the landed `.sh`; re-hashing the copied file after the copy reproduces it exactly.

## 2. What J1 grades, and the defect it repairs

The round-41 limb I1 collected the firing evidence identifiers as a cross-record UNION
(`corpus/instruments/r41-closure.sh` lines 902–906: the `seen` accumulator spans `RECORDS`). Removing
the evidence names from one correction therefore left the aggregate at `evidence=3/3` and the limb
green. That is exactly the committed defeat recorded in
`.ufo/waves/round-41/wave2/CritC1KillRule.md` and `RevC1Counters.md` (finding 2).

J1 keeps I1's population and fixes the aggregation. Population of an audited block = the
**outside-fence** `Correction (round 41)` lines in SCORECARD.md, LOG.md, SHONEN.md that name the
audited claim (`C1`, whole token) and the round being corrected (`round 40` / `r40`). The verdict
phrase and the evidence identifiers are deliberately **not** part of the selection, so a correction
whose verdict was softened or whose evidence names were stripped stays in the population and is
graded. Every member is graded **on its own**:

- (a) it grades the overclaim **not verified** (`not verified` / `unverified` / `withdraw`, I1's
  vocabulary), and
- (b) it names **every** firing evidence identifier of the block, each as a **whole token**
  (boundary chars may not be a letter, digit or `_`, so `wave2/RevC1Counters.defeats.txt` names
  `RevC1Counters` while `RevC1CountersX` does not — the whole-token intent of claims-erratum-2 E6).

The evidence identifiers for round 41 are `RevC1Counters CritKillRule MutH6H10` — the three
committed round-40 wave-2 defeat artifacts the round-41 corrections cite. Every declared identifier
must **resolve** to a committed artifact under the export's `.ufo/waves/round-40/wave2/`
(`evidence-not-grounded` otherwise), so the declaration cannot drift from the repository. There is no
cross-record and no cross-correction set operation in the tally: `graded` and `evidence` count
passing members, and the check closes only when every member of every block of every record passes;
a record with no member in an audited block is `missing` and fails.

Payload: `J1 payload=records=<n>,rounds=<n>,lines=<members>,graded=<pass>/<members>,evidence=<pass>/<members>,missing=<n>,detail=<file:rN:graded/evidence/members;…>,fail=<file:line:rN:reason;…|none> closed=0|1`.
`check_j1` also sets `J1_PAYLOAD` and `J1_CLOSED`, so the suite can re-emit the line from values it
graded rather than from stdout. Exit 0 iff `closed=1`. All helpers are `j1_`-prefixed to avoid a
collision when sourced next to the suite's own helpers.

## 3. Evidence (commands and actual output)

Ref exercised: lane HEAD `514ff62d61ee9bc717a20a02a22c65ec0c5124ed` (the three claims-erratum commits
landed while this seat ran; the transcript records the exact ref it read). Export is read-only:
`git -C <lane> archive --format=tar <ref> | tar -xf - -C <scratch>`.

**Positive — lane HEAD export:**

```
$ source ExecJ1Evidence.sh; check_j1 "$E"
J1 payload=records=3,rounds=1,lines=4,graded=4/4,evidence=4/4,missing=0,detail=SCORECARD.md:r41:2/2/2;LOG.md:r41:1/1/1;SHONEN.md:r41:1/1/1,fail=none closed=1
rc=0
```

Members: SCORECARD.md:1602 and :1607 (the D-r41-1 duplicate pair — both graded, both pass),
LOG.md:1736, SHONEN.md:221.

**Committed defeat re-executed against the committed r41 I1 limb** (fixture = in every record the
first `Correction (round 41)` line is replaced by the round-41 selftest's own evidence-free
replacement, the `I1-evidence` mutant of `selftest_case_i1`):

```
clean  : records=3,lines=14,graded=3,evidence=3/3,missing=0         rc=0
mutant : records=3,lines=14,graded=3,evidence=3/3,missing=0         rc=0
```

The committed I1 limb accepts the committed defeat (identical payload, rc=0) — the defect is live in
the lane's own bytes, reproduced, not quoted.

**J1 over the same committed union mutant:**

```
J1 payload=records=3,rounds=1,lines=4,graded=4/4,evidence=1/4,missing=0,detail=SCORECARD.md:r41:2/1/2;LOG.md:r41:1/0/1;SHONEN.md:r41:1/0/1,fail=SCORECARD.md:1602:r41:evidence;LOG.md:1736:r41:evidence;SHONEN.md:221:r41:evidence closed=0
rc=1
round-41 union tally over the same tree (distinct ids in the qualified population): 3/3
```

Per-correction evidence `1/4`, closed=0, while the r41-style union tally still reads `3/3` on the
same bytes. That is the defect and the repair side by side.

**Per-record variants of the same defeat** (the replay library's `e1`/`e2`/`e3`: strip the evidence
names from every member line of one record, leaving the other records intact). Each is rejected while
the r41 union tally stays 3/3:

| case | record stripped | J1 result |
|---|---|---|
| e1 | SCORECARD.md (both duplicated member lines 1602, 1607) | `evidence=2/4 closed=0 rc=1`, `fail=SCORECARD.md:1602:r41:evidence;SCORECARD.md:1607:r41:evidence` |
| e2 | LOG.md (member 1736) | `evidence=3/4 closed=0 rc=1`, `fail=LOG.md:1736:r41:evidence` |
| e3 | SHONEN.md (member 221) | `evidence=3/4 closed=0 rc=1`, `fail=SHONEN.md:221:r41:evidence` |

**Fresh mutants (each rejected; the union tally never moves off 3/3):**

| mutant | construction | J1 result | union tally |
|---|---|---|---|
| M2 partial evidence | one member per record loses the `MutH6H10` citation (2 of 3 ids) | `evidence=1/4 closed=0` | 3/3 (committed r41 I1 also still `rc=0`) |
| M3 soft verdict | one member per record: `not verified on the frozen counter (NOT verified)` → `not confirmed on the frozen counter` | `graded=2/4 closed=0`, `fail=SCORECARD.md:1602:r41:verdict;SHONEN.md:221:r41:verdict` | 3/3 |
| M4 fenced member | first member of each record wrapped in a CommonMark fence | `lines=1,missing=2 closed=0` | — |
| M5 deleted block | LOG.md's whole `Correction (round 41)` block deleted | `lines=3,missing=1 closed=0` | — |
| M6 superstring id | `RevC1Counters` → `RevC1CountersX` (substring match would pass) | `evidence=1/4 closed=0`, mutated text `RevC1CountersX.defeats.txt` | 3/3 |

**Graded selftest over the landed bytes:**

```
selftest detail=J1 mutant=union union-evidence=3 rejected=1
selftest detail=J1 mutant=partial-evidence union-evidence=3 rejected=1
selftest detail=J1 mutant=soft-verdict union-evidence=3 rejected=1
selftest detail=J1 mutant=fenced union-evidence=3 rejected=1
selftest detail=J1 mutant=deleted-record union-evidence=3 rejected=1
selftest detail=J1 mutant=superstring union-evidence=3 rejected=1
selftest case=J1 mutants=6/6 positive=pass verdict=pass
selftest cases=1 failures=0
rc=0
```

**Fail-closed edges:** export root absent or empty argument → `fail=export-root-missing closed=0 rc=1`;
audited round with no declared table (`J1_ROUNDS=(99)`) → `fail=round-99:evidence-table-missing
closed=0 rc=1`; records-only fixture without the grounding artifacts →
`fail=round-41:evidence-not-grounded closed=0 rc=1`.

**Negative-control refs (observed, reported here rather than in the transcript):**

```
ref=5053a7f46de35784cff4b56756906e9014a38276 grounding_dir=present
J1 payload=records=3,rounds=1,lines=4,graded=4/4,evidence=4/4,missing=0,...,fail=none closed=1  rc=0
ref=1f7464612ac4c44e39886b82e812610d3c039b13 grounding_dir=present
J1 payload=records=3,rounds=1,lines=4,graded=4/4,evidence=4/4,missing=0,...,fail=none closed=1  rc=0
```

J1 is **green at base and at the round-41 judged head by construction**: the round-41 correction
blocks it audits already exist at both refs, and they already satisfy the per-correction rule. J1 is
therefore *not* a contributor to the base/r41-head `closed<13/13` negative control — the other twelve
checks must carry that (J3's r42 registry row, J8's Y receipt, J4's round-42 declared blocks, …). This
is stated so the integrator is not surprised by J1=1 in a base run.

## 4. Integration contract for the L1 / ExecSuiteCore

1. `source .ufo/waves/round-42/wave1/ExecJ1Evidence.sh` then `check_j1 "$EXPORT"`. The limb prints the
   finished `J1 payload=... closed=0|1` line and returns 0/1; the suite can emit that line directly or
   rebuild it from `J1_PAYLOAD`/`J1_CLOSED`. The limb writes nothing and reads only `$EXPORT`.
2. **Fixtures must carry `.ufo/waves/round-40/wave2/`** (the grounding artifacts). `j1_copy_tree SRC
   DST ROUND` copies them; a records-only fixture is correctly rejected as `evidence-not-grounded`.
   ExecReplayHarness materialisations for J1 must copy that directory too.
3. To audit the round-42 correction block as well (once ScribeCorrections' blocks land), set
   `J1_ROUNDS=(41 42)` and `J1_EVIDENCE_MAP[42]='<ids>'` where each id resolves under
   `.ufo/waves/round-41/wave2/`. Not enabled by default: at freeze time those blocks do not exist and
   the target ids are the L1's to declare.
4. Replay limb (required by claims-erratum-2 E8 for J1): `j1_selftest_export "$EXPORT" "$WORK"` prints
   the six `selftest detail=` lines, the graded `selftest case=J1 mutants=6/6 …` line and the
   `selftest cases=1 failures=<k>` summary; exit 0 only when the positive passes and all six mutants
   are rejected. The committed defeat it replays is I1's own `evidence-not-named` fixture.
5. Helpers are safe to drive directly: every round argument defaults to `${J1_ROUNDS[0]}`, so
   `j1_members FILE`, `j1_qualified FILE`, `j1_union_evidence FILE…` and the `j1_mutant_*` builders work
   without repeating the round, including under `set -u`. Only `check_j1`'s `$1` (the export root) is
   required.

## 5. Limits and risks (stated, not hidden)

- **Population is claim-token scoped.** A round-41 correction that corrects the overclaim without
  naming `C1` (e.g. SCORECARD.md:1603, which corrects "the `## Round 40 result` depth:verifiability
  row") is outside the population — the same selector r41's I1 used. Consequence: evidence cannot be
  offloaded into such a line, and deleting a record's whole member set is caught by `missing`.
- **Residual, out-of-family escape.** Adding a *new* fully compliant member while gutting the real one
  would satisfy J1. Records integrity (duplicated/undeclared correction blocks, declared-block
  equality) is J11's and J4's remit, not F-EVID's; J1 does not claim it.
- **D-r41-1 duplicate pair.** SCORECARD.md:1602 and :1607 are verbatim duplicates, so SCORECARD has
  two members; both are graded individually and both pass. J1 does not deduplicate (J11 owns the
  `Correction-dedup (round 42)` marker); it only refuses to let one copy carry the other's evidence.
- **Green at base / r41 head** (see §3) — J1 is a repair of the aggregation, not a negative control.
- No blocker. No installation or host change was needed; no pacman transaction was attempted.

## 6. Housekeeping

- Tooling: none installed or upgraded (no pacman, no `uv tool install`, no `npx`, no network fetch). The
  limb needs only bash, awk, grep, sed, find, cut, head.
- Disk guard read before the run: `/tmp` 5% used / 122.2 G free, `/var/tmp` 36% / 576.1 G, `/fast/scratch/hyaku`
  27% / 592.6 G — green.
- Scratch: `/fast/scratch/hyaku/kasegi-r42/ExecJ1Evidence` (first pass) and
  `/fast/scratch/hyaku/kasegi-r42/ExecJ1Evidence-verify` (post-fix cross-check of the replay library's
  `e1`–`e3` catalog) held every work copy (exports, mutants, transcript drivers); both removed before
  yield. No `/tmp` use, no fixture git repository, no mutating git command (only `git archive` /
  `rev-parse`, both read-only).
- Lane writes: the two deliverables above and this receipt only.

## 7. Change after the first landing (and why it matters)

The first landed limb (`bd7cff78…`) computed the prior round inside the same `local` statement as the
round argument:

    local file=$1 round=$2 prior=$((round - 1))

Bash expands every word of a `local` command before assigning any of them, so `prior` read the
**caller's** `round` through dynamic scope. Inside `check_j1` that happened to be the right value, so
the payloads were correct — but the helper aborted with `round: unbound variable` under `set -u` when
called with its own arguments from anywhere else (found by driving `j1_members` directly while
cross-checking ExecReplayHarness's `e1`–`e3` cases). The fix splits the assignments:

    local file=$1
    local round=${2:-${J1_ROUNDS[0]}}
    local prior=$((round - 1))

and every helper that takes a round now defaults it to `${J1_ROUNDS[0]}` instead of aborting when the
argument is omitted. Two consequences worth recording: the limb no longer depends on a caller variable
name for correctness (a rename inside `check_j1` could otherwise have silently changed the audited
prior round), and peers may drive the helpers directly. Behaviour on every case above is unchanged;
the graded selftest still reports `mutants=6/6 positive=pass failures=0`.
