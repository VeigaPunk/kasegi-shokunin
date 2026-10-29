VERDICT: BROKEN

# R46MutC1b — C1 mutation test of r46-c1-gate.py limbs L4 (per-entry mode on its own bytes) and L5 (append-only)

Scope: frozen counter `corpus/instruments/r46-c1-gate.py`, sha256 `b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294`
(matches freeze record `c1-gate-sha256`; extracted from freeze commit 9f23aab with `git archive`, read-only). The committed
`S073.txt` (sha256 `66c96a61…1930`, matches freeze) was used as a re-ground anchor. Nothing committed, nothing under the lane
or the pure export was written. Scratch recipe (`mutate_c1.py`, `verify_c1.py`) removed on exit; its edit list is reproduced below.

## Harness

- Base: copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure` (unmodified).
- Hand-built satisfied tree: pure copy + frozen counter at `corpus/instruments/r46-c1-gate.py` + committed round-46 snapshot;
  `claim-package-contract.md` re-grounded with 6 rows (5 anchors into `corpus/instruments/claim-package-check.py`, 1 into
  `S073.txt:131`, token `private`); `claim-gates.md` re-grounded with 6 rows (5 into `claim-package-check.py`, 1 into `S073.txt:564`).
  Each recheck line is `cd <lane> && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<entry>.md`.
- Invoked tool (L4 SELF and the aggregate) = frozen copy outside the tree. Tree copy = frozen (honest) or one-edit mutant (tampered).
- `rejected=1` iff the aggregate exits non-zero. `targeted` = which of L4/L5 print `pass=0`.
- Run: `python3 mutate_c1.py` (full matrix, 95 counter runs, wall 615.9 s), output `run3.txt` (scratch, deleted). Quoted lines below are verbatim.

## Controls (discriminate)

```
mutant=control-satisfied-unmutated rejected=0 targeted=none failing=none exit=0 mode=honest
mutant=control-pure-base-do-nothing rejected=1 targeted=L4,L5 failing=L1,L2,L3,L4,L5,L6 exit=1 mode=honest
mutant=clean-tree/c1-no-token-length-floor rejected=0 targeted=none failing=none exit=0 mode=tampered-tree-copy
mutant=clean-tree/c2-no-two-files-rule rejected=0 targeted=none failing=none exit=0 mode=tampered-tree-copy
mutant=clean-tree/c3-range-bound-99 rejected=0 targeted=none failing=none exit=0 mode=tampered-tree-copy
mutant=clean-tree/c4-no-unique-id-rule rejected=0 targeted=none failing=none exit=0 mode=tampered-tree-copy
```
The satisfied tree is green (exit 0) and the pure base is red, so the harness discriminates. The pure base's L4/L5 failures are
the empty-R guard (`bool(reg) and …`, code lines 195 and 202), not a per-entry check. The four weakened counters are green on the
clean tree, so each is visible only through a fixture.

## SURVIVORS — defect present, counter exits 0 (L4/L5 accept)

S1. `m09-indented-hidden-row` (L4). Edit: append to `claim-package-contract.md`
`  | G7 | an unlisted claim | `corpus/instruments/claim-package-check.py:2` | `this token is not in the file` |` (2 leading spaces).
Printed: `mutant=m09-indented-hidden-row rejected=0 targeted=none failing=none exit=0 mode=honest`.
Cause: `section_rows` (`corpus/instruments/r46-c1-gate.py:96`) matches `^\|\s*G\d+\s*\|` at column 0, so the indented row is never
counted or checked (rows stays at 6). A 2-space indent is still inside GFM's tolerance for table rows [INFERENCE: not rendered].
Effect: an unverified claim row can sit in the re-ground section with no limb noticing.

S2. `m10-anchor-parent-symlink` (L4). Edit: `corpus/source-snapshots/round-46` directory renamed to `round-46-real`, and
`round-46` replaced by a relative symlink to it. Printed: `mutant=m10-anchor-parent-symlink rejected=0 targeted=none failing=none exit=0 mode=honest`.
Cause: `islink` checks only the leaf (`:113`, `os.path.islink(fp)`); the realpath test (`:113`) only confirms the target is in-root.
The contract says "a regular non-symlink file"; a symlinked ancestor is not rejected. Here the target stays in-tree, so the harm is bounded;
the severe variant is S5.

S3. `m11-stale-recheck-kept` (L5). Edit: in `claim-gates.md`, the base gated line
`recheck: cd … && test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py …` is kept as a second `recheck:` line below the new gate line.
Printed: `mutant=m11-stale-recheck-kept rejected=0 targeted=none failing=none exit=0 mode=honest`.
Cause: `recheck_line` returns the first match only (`:78-83`); L5 drops every `recheck:` line from its comparison (`:198-199`);
L3 reads the first line only (`:187`). A live gated `~/` line can persist unseen beside a re-ground.

S4. `m14-base-lf-to-cr` (L5, low severity). Edit: the LF after the historical line `verified-at: 2026-09-28` in `claim-gates.md`
rewritten to CR (a byte change to historical text). Printed: `mutant=m14-base-lf-to-cr rejected=0 targeted=none failing=none exit=0 mode=honest`.
Cause: the counter opens files in text mode (`:72`) and compares lines (`:200`), so append-only is enforced at line level after
universal-newline normalisation, not at byte prefix. Historical bytes can change without tripping L5.

S5. `m17-self-anchor-via-symlink-dir` (L4; the aggregate rejects it only through L6, not L4). Edit: symlink
`corpus/source-snapshots/knowledge-alias -> ../knowledge`; the `claim-package-contract.md` G1 anchor becomes
`corpus/source-snapshots/knowledge-alias/claim-package-contract.md:<line of verified-at>` with token `verified-at: 2026-09-28`
(the entry's own line). Printed: `mutant=m17-self-anchor-via-symlink-dir rejected=1 targeted=none failing=L6 exit=1 mode=honest`.
L4 passes (`targeted=none`), so L4 accepts the entry as its own anchor. The rejection comes from L6, and I did NOT inspect why L6
fails (not verified). Cause for L4: the self check is a string comparison (`rel == entry_rel`, `:110`), not a realpath comparison, so an
alias to the entry passes. This contradicts the docstring rule "never the entry itself".

Survivors appear in every tampered-counter combination too (S1–S4 × c1–c4 print `rejected=0`; e.g. `c1-no-token-length-floor+m09-indented-hidden-row rejected=0 … exit=0`).
The counter tampers do not cover these four defects.

## Findings — L4 bite only where its own bytes disagree with the tree copy

Tampered tree copy (the tree's own counter weakened, invoked tool frozen), paired with the defect that exactly one fixture
exercises. L4 rejects each:

```
mutant=c1-no-token-length-floor+m15-short-token rejected=1 targeted=L4 failing=L4 exit=1 mode=tampered-tree-copy
mutant=c2-no-two-files-rule+m07-single-anchor-file rejected=1 targeted=L4 failing=L4 exit=1 mode=tampered-tree-copy
mutant=c3-range-bound-99+m06-range-41-lines rejected=1 targeted=L4 failing=L4 exit=1 mode=tampered-tree-copy
mutant=c4-no-unique-id-rule+m16-duplicate-row-id rejected=1 targeted=L4 failing=L4 exit=1 mode=tampered-tree-copy
```

Structural observation: a per-entry defect (m01, m02, m03, m05, m06, m07, m08, m15, m16) makes the entry's own recheck exit non-zero.
The aggregate then classifies the entry as gated, it leaves R, and L4 never checks it. These mutants are rejected by the accounting limbs
(`failing=L1,L2,L7`, e.g. `mutant=m07-single-anchor-file rejected=1 targeted=none failing=L1,L2,L7 exit=1 mode=honest`), not by L4.
L4 is the independent detector only when the tree's copy is tampered and the invoked tool is frozen (the four lines above).
Inverse case (`invoked-c*` runs: invoked tool tampered, tree copy frozen) is rejected by L1/L2/L7 only, e.g.
`mutant=invoked-c2-no-two-files-rule+m07-single-anchor-file rejected=1 targeted=none failing=L1,L2,L7 exit=1 mode=tampered-invoked-tool`.

m04 (anchored file replaced by symlink) fails L4 and L5 via the empty-R guard (`failing=L1..L7`). The reason is inferred from the code (`:195`, `:202`), not verified.

## Full honest results (tree copy frozen, invoked frozen)

```
mutant=m01-token-not-in-lines rejected=1 targeted=none failing=L1,L2,L7 exit=1
mutant=m02-range-past-eof rejected=1 targeted=none failing=L1,L2,L7 exit=1
mutant=m03-anchor-is-entry rejected=1 targeted=none failing=L1,L2,L7 exit=1
mutant=m04-anchor-leaf-symlink rejected=1 targeted=L4,L5 failing=L1,L2,L3,L4,L5,L6,L7 exit=1
mutant=m05-anchor-dotdot rejected=1 targeted=none failing=L1,L2,L7 exit=1
mutant=m06-range-41-lines rejected=1 targeted=none failing=L1,L2,L7 exit=1
mutant=m07-single-anchor-file rejected=1 targeted=none failing=L1,L2,L7 exit=1
mutant=m08-section-duplicated rejected=1 targeted=none failing=L1,L2,L7 exit=1
mutant=m12-base-body-edit rejected=1 targeted=L5 failing=L5 exit=1
mutant=m13-base-line-deleted rejected=1 targeted=L5 failing=L5 exit=1
mutant=m15-short-token rejected=1 targeted=none failing=L1,L2,L7 exit=1
mutant=m16-duplicate-row-id rejected=1 targeted=none failing=L1,L2,L7 exit=1
mutant=m17-self-anchor-via-symlink-dir rejected=1 targeted=none failing=L6 exit=1
```

## Edit list (scratch recipe; the recipe is not committed)

Tree-side (one edit each, against the satisfied tree):
m01 CG G3 token `def rule_redact(pkg):` → `def rule_redact(pkg, strict):`; m02 CG G6 anchor `S073.txt:564` → `:580-600` (file 589 lines);
m03 CPC G5 anchor → the entry itself `:1`; m04 `claim-package-check.py` → symlink to a byte-identical `claim-package-check.src.py`;
m05 CPC G2 anchor path `…/instruments/../instruments/…:101`; m06 CG G1 anchor `:275` → `:275-315` (41 lines);
m07 CPC G6 anchor `S073.txt:131` → `claim-package-check.py:78` (token `private` on both); m08 second `## Re-ground (round 46)` header appended to CG;
m09 indented row appended to CPC (see S1); m10 parent directory → symlink (see S2); m11 base recheck line kept (see S3); m12 `verified-at: 2026-09-28` → `2026-09-29` in CG;
m13 base `source: [lost-tree] …` line deleted from CG; m14 LF → CR (see S4); m15 CPC G2 token `SIX_FILES = (` → `SIX_`; m16 CG row id G4 → G2;
m17 alias symlink + self-anchor row (see S5).
Counter-side (one edit to the tree copy): c1 `if len(tok) < 6 or …` → `if a < 1 or …`; c2 remove ` and len(files) >= 2`;
c3 `b - a > 39` → `b - a > 99`; c4 remove ` and len(set(ids)) == len(ids)`.

## Limitations and unrun checks

- Not run: the reason L6 fails for m17 (not inspected); the rendered GFM behaviour of S1; L6/L7/L1 defects beyond what the matrix hit; counter branches not in the edit list (e.g. `break` on headings, `CD_RE` stripping).
- Single run, deterministic inputs. Re-ground claim texts are fixture wording, not semantic checks of real entries.
- An earlier run of the same recipe (before the rewrite) applied counter edits only to a clean tree; its counter-side survivors were trivially green and are superseded. A second rerun aborted on a pure-export digest assertion before printing; the rewritten recipe reports that digest instead.
- The pure export `L1/pure/corpus/instruments/__pycache__/recheck-audit.cpython-314.pyc` appeared after my first run. This recipe never runs with cwd=pure and never imports `recheck-audit`, so the file was not written by this seat (the source of the write is unknown to me). Digest excluding `__pycache__`: `pure-export-changed-outside-pycache=0` (run3).
- Out-of-scope observation, code reading only [INFERENCE, not run]: `CD_RE` (`:61`) strips a `cd <path> &&` prefix, including `cd ~/…`, before L3's `HOME_RE` test (`:187`). A recheck of the form `cd ~/Projects/bounties && python3 …` would pass L3's no-`~/` rule.
- Installs/upgrades: none (system python3 3.14.8 used as-is).
- Scratch: removed on exit; no commit, push, index or git mutation.
