VERDICT: BROKEN

Scope: C1 limb L1 of corpus/instruments/r46-c1-gate.py (`gated <= 22`, `broken = 0`, `lines >= base lines`), attacked alone and inside the aggregate counter. Recipe below reads `gate L1 pass=1` with no entry re-grounded.

Provenance of inputs (all read-only):
- counter sha256 `b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294` = `c1-gate-sha256` in .ufo/waves/round-46/freeze.txt (matches).
- base tree: `/fast/scratch/hyaku/kasegi-r46/L1/pure` (copied to scratch `base/`; used as both base and do-nothing tree).
- scratch: `/fast/scratch/hyaku/kasegi-r46/R46RevC1L1/` (removed on exit). No git mutation, no lane file touched.

## Finding 1 (BROKEN): two one-token edits pass L1 with no re-grounding

Recipe (tree `tA`, diff vs pure base, only these two lines differ):
```
corpus/knowledge/claim-gates.md:125
-recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-gates.md  # on-restoration ...
+recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d . && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-gates.md  # on-restoration ...
corpus/knowledge/claim-package-contract.md:68
-recheck: ... test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-package-contract.md  ...
+recheck: ... test -d . && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-package-contract.md  ...
```
No `## Re-ground (round 46)` section, no row, no other byte changed (`diff -rq tree tA`: only the two entries differ).

Command: `python3 corpus/instruments/r46-c1-gate.py --root <tA> --baseline <base> --work $TMPDIR`
Output (verbatim):
```
gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=0 read=bad=claim-gates.md,claim-package-contract.md
gate L4 pass=0 read=bad=claim-gates.md,claim-package-contract.md
gate L5 pass=0 read=bad=claim-gates.md,claim-package-contract.md
gate L6 pass=0 read=mutants=0 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=3/7 exit=1
```
Standalone L1 predicate (same `classify` the counter calls): `tA gated=22 broken=0 lines=64 base_lines=64 L1=True`.

This tree is the same construction as the frozen control `c1 marker-only` in .ufo/waves/round-46/controls/freeze-controls.txt (which also grades `fixed=3/7`), so the aggregate kill holds for this attack, but the limb itself does not: L1 passes on it alone. L2 also passes on it (L2 counts exit-code flips, not re-grounding); only L3-L5 catch it.

Why it works: `classify` runs the recheck line with its `cd` stripped and only checks exit status. Entry text is never read. `test -d .` succeeds, and anchorcheck then exits 0 because the two entries have nothing to check:
```
$ bash -c "test -d . && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-gates.md"   (cwd=tA)
== corpus/knowledge/claim-gates.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
rc=0
$ ... claim-package-contract.md
LOST-RECORDED md:50 [lost-tree] claims/hackerone-hyatt/ingestion-20260914/status.json:14 (not checked)
rc=0
```
Under the real HOME the original lines fail closed: `test -d ~/Projects/bounties && ...` gives rc=1, and `ls -d ~/Projects/bounties` prints `ls: cannot access '/home/vgpnk/Projects/bounties': No such file or directory`.
So the two intended entries' current rechecks verify zero live anchors, which is a second defect for C1: gate-passing does not mean anchors were checked.

## Finding 2 (BROKEN, same limb): shadow line passes L1, base line kept byte-identical

Tree `tB`: insert `recheck: true` above the BASE recheck line in both entries (`PUT <125`, `PUT <68`). `recheck_line()` returns the first match, so the original line is still in the file, byte-identical and append-only.
- `tB gated=22 broken=0 lines=64/base=64 L1=True` (standalone)
- aggregate: `gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64`, `c1-gate fixed=3/7 exit=1` (L3-L5 fail on the same two entries).

## Finding 3 (BROKEN, zero tree edits): host HOME flips L1

The recheck lines use `~/Projects/...`, and the counter runs them with inherited env. I created empty `$HOME/Projects/{bounties,the-bounty-hunter,origin-work,ufo-fsd-alpha}` in a scratch fakehome and ran the unmodified pure tree:
```
HOME=<scratch>/fakehome python3 corpus/instruments/r46-c1-gate.py --root <pure> --baseline <base>
gate L1 pass=1 read=gated=3 broken=0 lines=64/base=64
gate L2 pass=0 read=base-gated=3 regrounded=0
...
c1-gate fixed=2/7 exit=1
```
The baseline is also read under the same HOME (`base-gated=3`), so L2 fails. Still gated: citation-bases.md, repo-git-state.md, root-loss-2026-10-12.md. L1 measures host directory state, not committed bytes; the on-restoration case in the entries is the same mechanism. Real HOME: `gate L1 pass=0 read=gated=24` (do-nothing, see Finding 4).

## Finding 4: L1 can fail alone (load-bearing as a count, not as a re-ground test)

- Do-nothing (pure base as tree and baseline): `gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64`; full `c1-gate fixed=1/7 exit=1` (matches freeze reading).
- One edit only (`tA1`: claim-gates token edit, package-contract untouched): `gate L1 pass=0 read=gated=23 broken=0 lines=64/base=64`; standalone `tA1 ... L1=False`.
So L1 does fail when the count is wrong, but it cannot distinguish a count flip from a re-ground. Its load-bearing content is exit-status counting.

## Finding 5: constructions that fail L1 (checked)

- tC, delete both gated recheck lines: standalone `gated=22 broken=0 lines=62 base_lines=64 L1=False`. Aggregate: every limb `exception-KeyError`, `c1-gate fixed=0/7 exit=1` (L3 indexes `ct[e]` for removed entries; the exception discards L1 too).
- tD, replace both with unparsable `recheck: test -d ~/Projects/bounties && if then`: `gate L1 pass=0 read=gated=22 broken=2 lines=64/base=64`; standalone `broken=2 ... L1=False`; aggregate `fixed=2/7`.
- tE, move both entries to corpus/archive-moved/: standalone `lines=62 ... L1=False`; aggregate `exception-KeyError` (fixed=0/7).
- tF, move both out and add two filler entries (`recheck: true`, filler-alpha.md, filler-beta.md) to keep lines=64: standalone `gated=22 broken=0 lines=64/base=64 L1=True`, so padding passes L1 alone. Aggregate still reads `exception-KeyError` on all seven (fail-closed), so tF is not a full-counter pass; it is a pass of the L1 predicate only.

## Constructions tried (9)
1 do-nothing (fail L1) | 2 one token edit tA1 (fail) | 3 two token edits `~/Projects/bounties`->`.` (PASS, Finding 1) | 4 shadow `recheck: true` above base lines (PASS, Finding 2) | 5 delete both gated lines (fail) | 6 unparsable replacement (fail) | 7 move both entries out (fail) | 8 move out + 2 filler entries (PASS on L1 predicate, aggregate exception) | 9 HOME env with empty Projects dirs, zero tree edits (PASS, Finding 3).
Distinct constructions that pass the L1 predicate: 4 (3, 4, 8, 9).

## Assessment
- L1 alone does not hold: the cheapest tree (two one-token edits, Finding 1) and the zero-edit host-state route (Finding 3) both read L1 pass=1 with no entry re-grounded.
- The aggregate counter does catch the tree attacks (3/7 and 3/7), via L3-L5, which the frozen `c1 marker-only` control already grades red. So C1's kill rule (fixed=7/7) is not violated by these recipes; the failure is in the limb's own predicate and in L2's exit-flip counting.
- Suggested for the lane (not applied, I wrote no tree files): bind L1 to committed bytes (e.g. also require the re-ground section per entry, or count only gated lines whose recheck was changed to a re-ground line), and make the two intended rechecks check at least one live anchor so a pass means something.

## Limitations
- Only the two intended entries and the gate's aggregate reading were attacked; I did not search for further full-counter (7/7) bypasses beyond the constructions above.
- Finding 3 used empty fake project dirs; I did not test a real restored ~/Projects/bounties.
- The pure base export was used as provided at /fast/scratch/hyaku/kasegi-r46/L1/pure; I did not re-hash it against rev 914ca0b6. Lane HEAD is 323d1f5 (not the base); I did not rely on it.
- All runs in scratch with TMPDIR set explicitly; HOME was overridden only in the child process of the counter runs in Finding 3. The scratch directory is removed on exit.
