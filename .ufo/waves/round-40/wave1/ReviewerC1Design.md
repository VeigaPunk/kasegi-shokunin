# ReviewerC1Design — round 40, wave 1 (design attack on frozen C1, pre-build)

Seat: `ReviewerC1Design` (leaf reviewer; no subagents, no lane edits). Item: attack the frozen
C1 design BEFORE the suite is final — verify that the proposed H5 (payload re-derivation), H6
(sibling scan) and H7 (teed deterministic receipt) semantics actually close the round-39 attack
classes, list remaining blinded spots, deliver a checklist the suite must satisfy.

I authored none of the bytes under attack: claims.json C1 is frozen at
`5e985b74075dd3813a63d7750966bf8abf693465`, the suite `corpus/instruments/r40-closure.sh` does
not exist yet (verified: `ls` → No such file or directory; c1-controls/before.txt agrees). The
round-39 attack files I re-read are the L1's and ExecSuiteBuild's. No conflict of interest.

Inputs read in full: `.ufo/waves/round-40/claims.json` (C1 predicate, kill rule, counting
commands, judged_head_rule), `.ufo/waves/round-39/wave2/CritG2Exploit.md` (F1–F5),
`.ufo/waves/round-39/wave2/CritC1Kill.md` (K1–K6, attempts a1–f),
`corpus/lessons/round-39-verifier-spotcheck.md` (R1–R7, §1–§5),
`.ufo/waves/round-40/c1-controls/before.txt`. Peer coordination: read the in-flight sibling
deliverable `.ufo/waves/round-40/wave1/CritC1AntiSuite.txt` (T1–T11) to divide scope — it
enumerates forgeries; this seat verifies the DESIGN semantics and names what neither the frozen
text nor T1–T11 states.

Axes: depth:verifiability (primary). coverage and depth:density untouched.

## Verdict

The H5/H6/H7 semantics CAN close the r39 attack classes, but only under a receipt-identity
model the frozen text does not state, and two attack classes (K2 undeclared added tail; K3
anchoring) are not closed by the frozen H9/H2 wording as written. Ten findings; D1 and D2 are
design-level defects that would surface only after the suite is built.

## Findings (by severity)

### D1 — DESIGN: the committed receipt cannot certify the ref it is committed at; H5/H7 are only self-consistent if the receipt is the tee of the run over its RECORDED ref (J), and the frozen text never says so
A run's transcript cannot validate a receipt that does not exist yet: if the receipt recorded
`export-ref=Y`, the receipt-validation limb would read the receipt from Y's export — but those
bytes do not exist when the producing run starts (fixpoint regress, same shape as r39 K1b).
The only consistent model: the receipt records `export-ref=J` (= judged head, no receipt in
that tree, per judged_head_rule `git diff --name-only J Y` = the receipt path), H7's "re-run
over J reproduces it byte-identically" matches, and the Y counting run is a fresh tally whose
output is never compared to the receipt. Consequences the builder must implement (checklist
§0): the receipt-validation limb is two-mode switched on receipt presence at `--export-ref`
(absent → `receipt=0` green, present → full validation); payload re-derivation runs over a
SECOND archive of the recorded ref; structural limbs bind recorded→passed ref (ancestor,
receipt-absent-at-recorded-ref, diff = exactly the receipt path). Without this model stated,
ExecSuiteBuild will hit the regress mid-build and improvise one — or worse, make the J-run
tee red (closed=9/10) and the round's own receipt self-falsifying.
Evidence: claims.json judged_head_rule; r39 spotcheck §1 verified exactly this shape at J/Y
(`export-ref=ee5ae5e1` = J, receipt absent at J, run-utc ≤ Y commit).

### D2 — DESIGN: H5's "recorded payload contradicting the export" is undefined about WHICH export; field-shape grading (the r39 G2 flaw) survives unless re-derivation is exact-string over the recorded-ref archive
The frozen predicate says "a recorded payload contradicting the export" — if the Y counting
run re-derives over Y and compares to a receipt recorded at J, honest receipts red on any
limb sensitive to the receipt's own existence. If re-derivation compares only field presence
or shapes, CritG2Exploit F2 (forged payload values pass) is reopened verbatim. Required
semantics (checklist §0.3, §1.1): re-derive over the recorded ref's archive; compare each
recorded `H<n> payload=` and `selftest detail=` value as an exact string; recount closed from
re-derived limbs and require equality with both printed tallies; unknown payload ids, missing,
extra or duplicated lines red. Note the honest division of labor (checklist §0.5): no single
in-suite limb proves the receipt is a true tee; that closure is H7's re-run — the suite header
must say so, or a payload field will eventually claim it.

### D3 — GAP: H9 as frozen checks only declared⇒exact; the K2 attack (undeclared added tail) passes it
The frozen predicate: "declared blocks equal the added lines with zero deletions for every
declared path". CritC1Kill K2 measured the reverse direction failing at r39: 271 added files
undeclared, fixture (e) appended 40 invented lines to the round-39 lesson and printed 8/8. The
frozen wording does not require every added path to be declared. Required: enumerate
`git diff --numstat base <ref>` paths with added>0, minus declared-blocks.txt itself and the
receipt path, and require each declared (checklist §4.6b). CritC1AntiSuite T10 does not cover
this direction either (its `cases=blocks-nonexistent` is declared-but-not-added, the inverse).

### D4 — GAP: H2's correction count can be satisfied by value-free or unanchored lines (K3/K6 recur)
The frozen H2 says "Correction (round 40) lines naming final r39 receipt values ... count >= 1
each". r39 K3 measured the anchoring trap (`^Correction` missed LOG.md's bullet) and K6 the
last-section scoping trap; the frozen text fixes neither the anchor pattern nor requires the
VALUES on the matched line, and "naming the final values" is checkable text the suite must
implement literally (`closed=7/8`, `exit=1`, `failures=1` substrings on the matched line).
Checklist §4.2.

### D5 — HAZARD (measured): reused `--work` overlay defeats export-mode isolation and flips H8 green
```
$ git archive HEAD | tar -x -C $W        # $W pre-planted with corpus/instruments/r40-closure.sh
$ cat $W/corpus/instruments/r40-closure.sh
PLANTED                                   # survives: tar overlays, never deletes
$ git ls-tree -r --name-only HEAD
corpus/suite.sh                           # tracked members only — planted file is foreign
```
A check that tests suite presence by listing the work tree would pass H1 at the base ref —
exactly the H8 kill. Closure: fresh empty extraction dir, refuse non-empty `--work`, plus a
canonical extracted-tree digest compared against the ref's tree before any limb runs (measured
discriminating: clean digest `b44c2bb6…` ≠ planted `3b4b8c49…`). Checklist §5.2–5.3.

### D6 — HAZARD (measured): committed symlinks escape the export through `git archive | tar -x`
```
$ ln -s /etc/passwd corpus/escape-abs; git add; git commit
$ git archive HEAD | tar -t | grep escape
corpus/escape-abs
$ tar -x; head -1 work/corpus/escape-abs
root:x:0:0::/root:/usr/bin/bash            # read left the work dir; host file reached
```
A relative-target variant (`../../../../../../etc/passwd`) is also extracted faithfully and
resolves outside the work dir (depth-dependent — a deeper extraction path reaches the root).
Any content limb that reads through export paths without a symlink guard can be pointed at
host or live-lane bytes. Closure: refuse symlink members (or validate canonicalized targets),
refuse `.git`/absolute/`..` members (checklist §5.3; ENDORSES AntiSuite T6 and adds the
post-extract enforcement point and measured evidence).

### D7 — HAZARD (measured): an unguarded tee launders a dead run into a clean receipt
```
$ false | tee f; echo $?   -> 0        # without pipefail
$ set -o pipefail; false | tee f; echo $? -> 1
```
If the caller's tee status is what survives, a suite that dies mid-run produces a truncated
receipt and exit 0. Closure: `set -o pipefail`, stderr merged, suite-printed final `exit=<n>`
line, transcripts missing that line red (checklist §3.1).

### D8 — H7 needs an explicit normalization rule or it is unsatisfiable as worded
"Re-run reproduces it byte-identically, run-utc printed by the run" is self-contradictory
unless byte-identity is defined as: identical argv, exactly one differing line, and that line
is `run-utc=`. Two or more differing lines red. The remaining injection class (rewrite run-utc
post-run) is closed by bracketing (run-utc ∈ [run-start, run-end], all printed by the run) and
by the K5 anchor `run-utc <= committer date of the receipt's containing commit` (implementable:
`git log -1 --format=%cI`, graded via pinned-date fixtures). Checklist §1.3, §3.2.
Premise measured: two `git archive HEAD | sha256sum` of one commit are byte-identical.

### D9 — H6 is only quiescence-safe if the scan covers the scratch PARENT, exempts exactly the work chain, and the selftest never plants live-root strays
The R4 survivor `kasegi-r39-l1` lived at parent level, not inside `kasegi-r39/` — the frozen
text's `kasegi-r39*/r40` pattern is right but the scanned ROOT is unstated; during the wave the
round's own mandated scratch root (`…/hyaku/kasegi-r40/`, all seats' dirs) matches the pattern,
so the counting run is green only at filing quiescence, with the sole exemption being the
passed `--work` chain. Graded H6 cases must plant strays under an isolated `--scratch-root`
only; unreadable roots red (`read=fail`); strays listed LC_ALL=C-sorted in the payload (F3
observability). The H6 payload is host state: byte-identity (H7) holds under the kill rule's
precondition and drift reds both consistently — document, do not relax (checklist §2, §2.6).

### D10 — Graded-case false-pass trap: every rejection case must assert its sabotage precondition and its named red needle
r39's fixtures were sound, but the class is live: a fixture builder that silently no-ops (git
add fails, tamper misses the file) yields a suite-green output that the case would grade as
pass. Each rejection case asserts the tamper is provably in place before invoking the suite and
grades only on the named red payload field (never exit code alone — F3). Checklist §1.4, §6.1.

### Verification of H5/H6/H7 semantics vs the r39 attack classes (summary)

| Class | Closed by | Verdict |
|---|---|---|
| G2Exploit F2 forged payload values | H5 exact-string re-derivation over recorded-ref archive (D2) | closes IF D2 semantics implemented; shape-only grading does NOT close |
| G2Exploit F4 indented 9th case line | H5 grammar counts `^[[:space:]]*selftest case=` | closes (checklist §1.2) |
| G2Exploit F5 / CritC1Kill K1b self-naming export-ref, circular head | H5 structural limbs: receipt-absent-at-recorded-ref, diff(recorded,passed)=receipt-only, ancestor | closes in validation mode (checklist §0.4) |
| CritC1Kill K1 detail-free receipt (R3) | H5 judge standard on receipt block + H7 byte-identity tee | closes (a hand-written receipt cannot byte-match a fresh run modulo run-utc) |
| R1 / K5 future-dated run-utc | H7 single clock + bracketing + commit-date anchor | closes (checklist §1.3) |
| CritC1Kill K2 undeclared added tail | nothing in frozen H9 wording | NOT closed — D3 fix required |
| CritC1Kill K3 correction anchoring | nothing in frozen H2 text | NOT closed — D4 fix required |
| CritC1Kill K6 last-section scoping | nothing in frozen H2/H4 text | NOT closed — checklist §4.2/§4.4 require all-section scans |
| G6 / R4 scratch sibling | H6 parent-root prefix scan + work-chain exemption + fail-closed | closes under filing quiescence (D9) |
| Export-reuse stale state | not enumerated in H1–H10 | closed only by harness guards (D5) |
| Symlink/relative-path escape | not enumerated in H1–H10 | closed only by harness guards (D6) |
| Check reads working tree instead of export | not enumerated per-limb | closed only by per-limb dual-state graded cases (checklist §0.6, ENDORSES T7) |
| Receipt copied from a different ref | H7 byte-identity (judge-side) + H5 payload/structural mismatch in-suite | closes; in-suite detection is partial by construction (D1/D2), full closure is the H7 re-run command |

## Residual risk and verification gaps

- The suite does not exist yet; nothing here is a run of r40-closure.sh. All probe evidence is
  from scratch fixtures (D5–D8), not lane instruments. ExecSuiteBuild's selftest and the L1's
  counting commands are the actual verification surface; this receipt pins the semantics they
  must implement.
- I did not re-run the r39 suite or its mutants (they are r39 evidence, already committed);
  findings rest on the committed r39 attack receipts plus fresh fixture probes.
- Whether an eleventh check (harness guards as a named limb) requires a claims erratum is a
  judge ruling; checklist §6.1 carries the AntiSuite freeze-gap note (T6 folded into H5, never
  a silent count change).
- The two-mode receipt-validation limb (D1) is my design resolution, derived from
  judged_head_rule + the H7 re-run wording; if the L1 prefers a different resolution (e.g.
  receipt certifies Y with a two-phase commit), the counting commands must change with it —
  the current counting command set is only consistent with the D1 model.

## Tooling

None installed or upgraded (no pacman; no uv/npx needed; no network fetches — nothing in scope
required one, so no HTTP status/bytes/UTC to record).

## Scratch

`/fast/scratch/hyaku/kasegi-r40/ReviewerC1Design` (fixture repos with toplevel asserted
`git rev-parse --show-toplevel` = fixture dir; inline `-c user.email/-c user.name` identities
used inside fixtures only; no mutating git command in any real repo) — removed after copying
deliverable + receipt into the wave dir.

Report: .ufo/waves/round-40/wave1/ReviewerC1Design.md
