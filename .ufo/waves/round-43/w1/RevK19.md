# RevK19 — attacks on the K19 freeze-record limb (reviewer, kasegi round 43)

Seat: reviewer, receipt-only. Three revisions of ExecK19Freeze were attacked; fixtures lived under
`/fast/scratch/hyaku/kasegi-r43/RevK19/` (removed before yield) and no lane file was written except
this receipt.

| revision | limb | lines | sha256 | state |
|---|---|---|---|---|
| R1 | `.ufo/waves/round-43/w1/ExecK19Freeze.sh` | 209 | `b9b6d387d9bdd8b799045b71f9d5b7871eb1b9e64f479ef7d5a3be43277940d2` | superseded |
| R2 | same path | 243 | `8e6b124feb975469e0837de4a3998ccf6a940543a19bfae93b9ec73d5165d7f2` | superseded |
| **R3 (under review)** | same path | 247 | `75f9552ec4958905b76c33f154ecaf0cdd099426d8bd0b321846167d8539e52f` | current |

R3 evidence, measured against the bytes: limb 247 lines / `75f9552e…`, transcript 332 /`b4c7e568…`,
format 32 / `7981e242…`, receipt 218 / `8069075c…`. The transcript carries 18 graded
`expected=` lines and closes `red-cases=15 green-cases=3`; its `bash -n` block records `rc=0` and `0`
bytes, which is the real (empty) output.

Frozen predicate under test (claims.json C1, K19 clause): *"the round-43 freeze record's
`frozen_at_utc` is not earlier than the latest `measured-at=` timestamp in the two committed control
receipts and the receipts carry that line."*

## 1. Method

```
$ git -C <lane> archive 4cb6d4ae… | tar -x -C $S/exp-head     # claims freeze commit
$ git -C <lane> archive ab98fac9… | tar -x -C $S/exp-base     # base control
$ git -C <lane> archive 1f7464612… | tar -x -C $S/exp-r41     # round-41 judged head
$ . .ufo/waves/round-43/w1/ExecK19Freeze.sh
$ check_k19 <export-root> [<commit-utc>]; echo rc=$?
```

59 mutated fixture roots (full copies of the head export, one byte-level edit each), the 3 real
exports, and 20 argument probes (true one-arg, supplied empty, whitespace, offset, garbage, a 2030
bound, and two 3-argument calls). `limb-sha=75f9552e…` printed by the driver.

## 2. The five assigned classes at R3

```
one-arg:HEAD   rc=0 [K19 payload=freeze=present,order=ok,sha=match closed=1]
one-arg:BASE   rc=1 [K19 payload=freeze=absent,order=bad,sha=mismatch closed=0]
one-arg:R41    rc=1 [K19 payload=freeze=absent,order=bad,sha=mismatch closed=0]
```

**2.1 Right label, forged claims digest — CLOSED.**

```
V01-forged-digest          rc=1 [K19 payload=freeze=present,order=ok,sha=mismatch closed=0]
W05-digest-63hex           rc=1 [K19 payload=freeze=present,order=ok,sha=mismatch closed=0]
W06-digest-space           rc=1 [K19 payload=freeze=present,order=ok,sha=mismatch closed=0]
V21-order-ok-digest-forged rc=1 [K19 payload=freeze=present,order=ok,sha=mismatch closed=0]
```
Digest over the `claims.json` bytes of the same export; the head export's claims.json is
`a4c03e1e…a6630`, exactly the record's line 3.

**2.2 Control receipt with two `measured-at` lines — CLOSED.**

```
V02-two-measured-at  rc=1 [K19 payload=freeze=present,order=bad,sha=match closed=0]
V10-quoted-dup       rc=1 [K19 payload=freeze=present,order=bad,sha=match closed=0]
```

**2.3 Control receipt with an unparseable timestamp — CLOSED.**

```
V03-unparseable-ts  (no Z)        order=bad,sha=match closed=0  rc=1
V03b-invalid-date   (2026-02-30)  order=bad,sha=match closed=0  rc=1
V03c-offset-ts      (+00:00)      order=bad,sha=match closed=0  rc=1
V15-bad-date-control (month 13)   order=bad,sha=match closed=0  rc=1
```

**2.4 Freeze label exactly equal to the control timestamp — CLOSED at the boundary.**

```
V04-label-eq-max      rc=0 [K19 payload=freeze=present,order=ok,sha=match closed=1]
V04b-label-eq-earlier rc=1 [K19 payload=freeze=present,order=bad,sha=match closed=0]
```
Equality with the latest measurement is accepted ("not earlier than"); equality with the earlier
control is red. The residual is the self-asserted timestamps (5.3), not the comparison.

**2.5 Freeze record for the wrong round — CLOSED; identity is now type-strict.**

```
V05-wrong-round-42    [order=bad,sha=match closed=0]   V05b-wrong-round-44  [order=bad,sha=match closed=0]
V05c-wrong-round-base [order=bad,sha=match closed=0]   X02-lane-souji       [order=bad,sha=match closed=0]
X03-round-41-coherent [order=bad,sha=match closed=0]   Y01-round-string     [order=bad,sha=match closed=0]
Y03-lane-case         [order=bad,sha=match closed=0]   Y02-round-float      [order=bad,sha=match closed=0]
Z01-round-true        [order=bad,sha=match closed=0]   Z02-round-43-5       [order=bad,sha=match closed=0]
Z03-round-list        [order=bad,sha=match closed=0]
```
All eleven are red; `claims.round` is now `type(...) is int` so `43.0`, `true` and `[43]` are refused,
closing R2's F8.

## 3. Further classes at R3

**3.1 Control-set aliasing — CLOSED for paths (bytes-level copy is the rewrite family).**

```
W01-controls-both-c1 [order=bad,sha=match closed=0]   X04-controls-both-c2 [order=bad,sha=match closed=0]
Y04-alias-symlink    [order=bad,sha=match closed=0]   Y05-alias-spelling    [order=bad,sha=match closed=0]
W02-controls-swapped rc=0 [order=ok,sha=match closed=1]     (same two files, names swapped)
Y06-copied-receipt   rc=0 [order=ok,sha=match closed=1]     (c2 bytes := c1 bytes; deletes the c2 evidence)
```

**3.2 Relation (6) and the second argument — F7 fixed.**

```
head-bound-Z          rc=0 [freeze=present,order=ok,sha=match closed=1]   (16:37:11Z)
head-bound-equal      rc=0 [freeze=present,order=ok,sha=match closed=1]   (== label 16:37:07Z)
head-bound-1s-early   rc=1 [freeze=present,order=bad,sha=match closed=0]
head-bound-EMPTY      rc=1 [freeze=present,order=bad,sha=match closed=0]  <-- R2's F7, fixed
X01-bound-EMPTY       rc=1 [freeze=present,order=bad,sha=match closed=0]  (forged future label)
head-bound-space      rc=1 [freeze=present,order=bad,sha=match closed=0]
head-bound-offset     rc=1 [freeze=present,order=bad,sha=match closed=0]  (%cI verbatim)
head-bound-garbage    rc=1 [freeze=present,order=bad,sha=match closed=0]
X01-bound-real        rc=1 [freeze=present,order=bad,sha=match closed=0]  (17:10Z label)
base-bound-Z          rc=1 [freeze=absent,order=bad,sha=mismatch closed=0]
head-3arg-Z-junk      rc=0 [freeze=present,order=ok,sha=match closed=1]   (extra arg ignored)
head-3arg-empty-empty rc=1 [freeze=present,order=bad,sha=match closed=0]
head-bound-2030       rc=0 [freeze=present,order=ok,sha=match closed=1]   (lax bound accepted)
```
A true one-argument call is unchanged and still grades relations (0)-(5):
`check_k19 <head>` → `closed=1`; `check_k19 <X01>` → `closed=1` (post-commit label ungraded).
The transcript discloses both (`m-future` without the bound → `closed=1`) and records the empty and
offset cases in its §E.

**3.3 Whole-record co-rewrite — OPEN by construction.**

```
V06-consistent-rewrite rc=0 [freeze=present,order=ok,sha=match closed=1]
W15-post-freeze-edit   rc=0 [freeze=present,order=ok,sha=match closed=1]
```
The digest binds `freeze.txt` to `claims.json` and nothing else; both are committed together. The
executor now states this under Risks and no longer implies forgery-proofness.

**3.4 Grammar / containment / fail-closed — all behave.**

```
V07-five-lines       order=bad,sha=mismatch   V08-reordered      order=bad,sha=mismatch
W07-value-equals     order=bad,sha=mismatch   W09-crlf-freeze    order=bad,sha=mismatch
V11-absolute-control order=bad,sha=match      W03-dotdot-inside  order=bad,sha=match
W04-control-is-dir   order=bad,sha=match      V12-short-base     order=bad,sha=match
V13-base-mismatch    order=bad,sha=match      V14-stated-max-wrong order=bad,sha=match
V16-label-before     order=bad,sha=match      V17-claims-not-json order=bad,sha=match
V18-control-missing  order=bad,sha=match      V19-freeze-absent  freeze=absent
V20-claims-absent    order=bad,sha=mismatch   V22-clock-rollback order=bad,sha=match
V23-symlink-escape   order=bad,sha=match      V24-claims-symlink  order=bad,sha=mismatch
(all closed=0, rc=1)  W08-trailing-blank closed=1 (one blank line tolerated)
W14-base-zeros closed=1 (base shape-only)   X05-extra-control-key closed=1 (unknown key ignored)
```
V16 is the round-42 defeat mutant the claim's kill rule names (label earlier than the controls):
rejected. V23/V24 confirm realpath containment refuses reads outside the export.

**3.5 Contract at R3.** One line per call (`green-lines=1`, `red-lines=1`), status equals `closed`,
sourcing is silent and defines one function (`source-bytes=0`; `declare -F | wc -l` → 1; `check_k19`),
no argument and a file argument → `freeze=absent,order=bad,sha=mismatch closed=0` rc 1, and three runs
(one-arg, bounded, empty-bound) leave the export byte-identical (recursive digest
`6b992d3a…a7ad7f` before and after).

## 4. Findings at R3

No new defect was found in R3. F7 and F8 are fixed and verified; the residuals are unchanged and now
disclosed by the executor.

- **F7 (closed at R3) empty second argument** — `check_k19 <head> ""` is now
  `freeze=present,order=bad,sha=match closed=0` (rc 1), and the forged-future tree with an empty bound
  is red too. Verified against the transcript's §E.
- **F8 (closed at R3) non-integer round** — `43.0`, `true`, `[43]` all red.
- **F9 (residual, medium) coherent rewrite** — V06, W15, Y06 accepted; inherent to an internal digest.
- **F10 (residual, medium) the bound is caller-trusted** — one-arg accepts the post-commit label and a
  2030 bound is green. The receipt's integration constraint 1 gives the one correct Z-normalized
  formula (`date -u -d "@$(git show -s --format=%ct "$REF")" +%Y-%m-%dT%H:%M:%SZ`).
- **F11 (residual, low) `base` existence unproven** — W14 green (shape only).
- **F12 (integration, low) errexit** — a bare `check_k19` returning 1 aborts an `errexit` caller
  (measured: `before`, the K19 line, no `after`, rc 1). The suite must call it in `if`/`||`.
- **F13 (informational)** uppercase digest of the same 256 bits red (V09); a receipt quoting its own
  `measured-at=` line twice red (V10) — per the documented format.
- **F14 (integration note, not a defect) argument shape.** Because a *supplied but empty* second
  argument is now red, a suite that always passes a variable must guarantee it is non-empty, and a
  suite that wants relations (0)-(5) must pass literally one argument. Measured both ways: true
  one-arg head `closed=1`; two args with an empty second `closed=0`.

## 5. Disposition of all reported findings

| finding | revision | state at R3 | evidence |
|---|---|---|---|
| F1 wrong round/lane accepted | R1 | fixed (R2) + type-strict (R3) | V05/V05b/V05c/X02/X03/Y01/Y02/Z01 red |
| F2 control aliasing accepted | R1 | fixed (R2) | W01/X04/Y04/Y05 red |
| F3 post-commit label accepted | R1 | fixed only in the two-arg form | X01 one-arg green, X01 bound red |
| F4 fabricated `bash -n: ok` | R1 | fixed (R2) | transcript `rc=0` / `0` bytes; my R3 run: 0 bytes, rc 0 |
| F7 empty bound silently ignored | R2 | fixed (R3) | head-EMPTY and X01-EMPTY red |
| F8 round 43.0 accepted | R2 | fixed (R3) | Y02/Z01/Z02/Z03 red |
| F9 rewrite family | R2 | accepted as inherent, disclosed | V06/W15/Y06 green |
| F10 caller-trusted bound | R2 | disclosed, integration constraint 1 | 2030 bound green; `%cI` red |
| F11 base shape-only | R2 | accepted as inherent, disclosed | W14 green |
| F12 errexit | R2 | disclosed, integration constraint 2 | bare call aborts the caller |

## 6. Which forgery classes remain

1. **Whole-record co-rewrite** (claims + digest + label), including the bytes-level control copy:
   V06, W15, Y06 — inherent; the limb is not a forgery defence and is no longer described as one.
2. **Relation (6) rests on the caller** — a lax or mis-derived bound passes (2030), and the one-arg
   form leaves post-commit labels ungraded (F10).
3. **`base` existence** unproven (F11).

Closed at R3: forged digest; measured-at count != 1; unparseable/offset/calendar-invalid stamps;
label equality boundary; wrong round/lane and every non-integer round type; path-level control aliasing
(alias, symlink, `./`); record grammar (line count, order, `=`, CRLF); missing record/claims/control;
symlink escape; base/ref mismatch; label before the controls (the RD42-6 mutant); empty/whitespace/
unparseable caller bound.

## 7. Verification gaps

- `corpus/instruments/r43-closure.sh` still does not exist, so suite wiring, the K19 selftest case,
  base `closed=13/19` and Y `closed=19/19` are unverified here.
- J/Y do not exist. Measurements pin limb sha `75f9552e…`. If the suite calls the one-argument form,
  F10 stays open in the shipped instrument; if it passes a second argument it must use the receipt's
  Z-normalized formula or K19 turns red at an honest Y (F14).
- K17's independent claims.json binding was not inspected (outside this item).
- **Advance check after the C2 + corrections landings** (measured at `5b4a850` and again at the newest
  head `a6c1d46`, two commits past the freeze): the four K19 inputs are byte-identical to `4cb6d4a`
  (`git diff 4cb6d4a..HEAD -- .ufo/waves/round-43/{claims.json,freeze.txt,c1-controls,c2-controls}`
  yields 0 lines), the claims digest still equals the record's line 3 (`a4c03e1e…a6630`), and an export
  of `a6c1d46` with the receipt's own bound formula —
  `COMMIT_UTC=$(date -u -d "@$(git show -s --format=%ct HEAD)" +%Y-%m-%dT%H:%M:%SZ)` = `17:01:00Z` —
  prints `K19 payload=freeze=present,order=ok,sha=match closed=1` (rc 0), while the base export prints
  `K19 payload=freeze=absent,order=bad,sha=mismatch closed=0` (rc 1). Content-only landings do not
  disturb K19; the only open item is that `r43-closure.sh` itself still does not exist.
- Transcript fidelity otherwise holds: declared shas/line counts match the bytes, `bash -n` records its
  real (empty) output, the 18 `expected=` lines support `red-cases=15 green-cases=3`, and the format
  file's record block is byte-identical to the committed `freeze.txt` (4 lines, LF, one trailing
  newline).

## 8. Housekeeping

- No tool installed or upgraded (bash, python3, git, tar, sha256sum, od, diff present); no pacman;
  nothing written to a PATH directory, the fleet root, or any lane path other than this receipt.
- Read-only git only (`log`, `archive`, `rev-parse`, `show`, `status`); no fixture repository and no
  throwaway git identity.
- Disk guard checked before the export pass (`/fast/scratch/hyaku` 26% used, 598.6G free); scratch
  `/fast/scratch/hyaku/kasegi-r43/RevK19/` removed before yield.
