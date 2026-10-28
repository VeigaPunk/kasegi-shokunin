# R44Mutant5 — path/deletion mutant against cleanup of the inherited aborted tmp

seat: R44Mutant5 (mutation-tester, leaf) · round 44 · lane `kasegi-shokunin`
item: *Design a path/deletion mutant that falsely passes cleanup of the inherited aborted tmp.*
lane HEAD at probe: `66314015122b9aa32dc40f2f1815df56624c26d1` ("round-44: freeze claims and validated wave"); frozen base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`.
mode: read-only on the lane. No lane file was created, modified or deleted; the only lane write is this report. No git/jj/index mutation, no commit, no push. Scratch under `/fast/scratch/hyaku/kasegi-r44/R44Mutant5/`, deleted on exit (see §9).
tools installed/updated: **none** (no install was needed; nothing added to any PATH directory).

Subject = routed defect **R43-5c** (`corpus/lessons/round-43-verifier-spotcheck.md:105`, restated at `:20`): the untracked aborted write
`.ufo/waves/round-43/final-gates/all-gates.at-Y.txt.tmp` (2137 B) must be gone, deleted "through the lane helper".

## 1. Measured subject facts (read-only, at HEAD 6631401)

| fact | command | observed |
|---|---|---|
| subject path is **untracked** | `git ls-tree -r HEAD .ufo/waves/round-43/final-gates/` | exactly 4 blobs (`all-gates.at-Y.txt`, `all-gates.txt`, `r42-at-de09313-run.txt`, `r42-at-de09313-selftest.txt`); no `.tmp` |
| subject path is **absent** from the work tree now | `test -e .ufo/waves/round-43/final-gates/all-gates.at-Y.txt.tmp`; `git status --porcelain -- <path>` | rc=1; porcelain empty (agrees with `R44Review5.md:7`) |
| `.ufo` **is** tracked, so exports carry wave evidence | `git ls-tree -r --name-only HEAD .ufo \| wc -l` | `8391` |
| but an export can **never** carry the subject | `git archive HEAD .ufo/waves/round-43/final-gates/ \| tar -t` | 8 entries = 4 dirs + the same 4 tracked files; **no `.tmp`** |
| no cleanup gate exists at HEAD (do-nothing state) | `git ls-tree -r --name-only HEAD corpus/instruments \| grep -iE 'k20\|tmp-leftover\|r44'` | rc=1, no match |
| the "lane helper" has **no deletion verb** | `grep -nE '^  (init\|commit\|recover\|push\|state\|clean\|delete\|rm)\)' scripts/hyaku/jj-lane.sh` | `init/commit/recover/push/state` only; its `rm -f` at `jj-lane.sh:529,570` removes only its own changes file, and `:461` says "never deletes the file" |

The load-bearing consequence: **the round-43 suite passes `<export-root>` to every limb** (`corpus/instruments/r43-limbs/k19-freeze.sh:5,10-12`; `k18-transcript.sh:9`). An aborted *untracked* write is invisible to `git archive` by construction, so a gate that reuses the suite's root convention cannot see the artefact it claims to grade — and cannot go red when the artefact is restored. That is the mutant's lever.

## 2. Candidate pristine gate (authored for this probe — not landed lane code)

`.ufo`-style limb `k20-tmp-leftover.sh`, sourceable `check_k20 <lane-root>`, one-line payload
`K20 payload=leftover=<present|absent>,root=<worktree|other> closed=<0|1>`, exit 0/1/2, read-only (deletion is an executor act, not the gate's). Contract:

1. root must exist (usage → 2);
2. root must be a **work tree** (`[ -d "$root/.git" ]`); a non-work-tree root is refused with `closed=0`, because an export cannot prove work-tree cleanup;
3. the target is the exact basename `all-gates.at-Y.txt.tmp` under `.ufo/waves/round-43/final-gates/`, **anchored** at `$root` (cwd-independent);
4. present → `closed=0`; absent → `closed=1`.

Pristine sha256 `090c556d00a67f18e941472a4947d01636326b5e8d5e6efdf434ecdb61629058`.

## 3. Mutants (each a minimal byte change; diffs verbatim)

| id | concept | one-line change | sha256 |
|---|---|---|---|
| **M1** | root-provenance path mutant: drop the work-tree guard, so an **export** root is accepted as a work tree (and, if the gate self-deletes, `rm` lands on the export copy) | removes 4 lines (`if [ ! -d "$root/.git" ]; then … fi`) | `5f78e058373f929073ff8476ace090d9f1701c624511f7efbf2f1ac998a571a1` |
| **M2** | path-visibility oracle mutant: ask git for the path with `--untracked-files=no`, so the *untracked* subject is structurally invisible | `[ -e "$root/$target" ]` → `[ -n "$(git -C "$root" status --porcelain --untracked-files=no -- "$target" 2>/dev/null)" ]` | `9cac6bac6f321a2e84da668f8f242ce89b18d044ab634be04f4e7fec7fad83b7` |
| **M3** | unanchored-path mutant: use the target relative to **cwd** instead of `$root` | `[ -e "$root/$target" ]` → `[ -e "$target" ]` | `1a216decb01f76feef6ddc80c1e42839c448afa166e9cf763ec288946f5ed1f3` |

Fixture: `fx/` = git repo holding the four committed `final-gates` files extracted with `git show HEAD:<path>` (byte-identical to the lane) **plus** the untracked subject reconstructed to the reported size, `2137` bytes, sha256 `ea189506088ffe36019399596a20d6d09a7a54e1d15447da35fa34b814a11592` (content is a placeholder — the original bytes were never committed and are unrecoverable, §8). `fx-export/` = `git -C fx archive HEAD | tar -x` → 4 files, no `.tmp`.

## 4. Detector matrix — same bounded detector (the limb's exit code + payload line), pristine vs mutated vs restored

```
== pristine ==
P1  k20-tmp-leftover root=fx         cwd=<fx>  rc=1 | K20 payload=leftover=present,root=worktree closed=0
P2  k20-tmp-leftover root=fx-export  cwd=<fx>  rc=1 | K20 payload=leftover=absent,root=other closed=0
P4  k20-tmp-leftover root=fx         cwd=/     rc=1 | K20 payload=leftover=present,root=worktree closed=0
== M1 export-root ==
M1a m1-export-root   root=fx-export  cwd=<fx>  rc=0 | K20 payload=leftover=absent,root=worktree closed=1
M1b m1-export-root   root=fx         cwd=<fx>  rc=1 | K20 payload=leftover=present,root=worktree closed=0
== M2 untracked-no oracle ==
M2a m2-untracked-no  root=fx         cwd=<fx>  rc=0 | K20 payload=leftover=absent,root=worktree closed=1
== M3 unanchored ==
M3a m3-unanchored    root=fx         cwd=/     rc=0 | K20 payload=leftover=absent,root=worktree closed=1
M3b m3-unanchored    root=fx         cwd=<fx>  rc=1 | K20 payload=leftover=present,root=worktree closed=0
== clean work tree (leftover moved aside, all limbs) ==
k20-tmp-leftover rc=0 | K20 payload=leftover=absent,root=worktree closed=1
m1-export-root   rc=0 | K20 payload=leftover=absent,root=worktree closed=1
m2-untracked-no  rc=0 | K20 payload=leftover=absent,root=worktree closed=1
== restore ==
restored-leftover sha256: ea189506088ffe36019399596a20d6d09a7a54e1d15447da35fa34b814a11592
P1-restored rc=1 | K20 payload=leftover=present,root=worktree closed=0
```

| mutant | expected detector behaviour (pristine) | mutant output | verdict |
|---|---|---|---|
| **M1** | export root → `closed=0` (refuse provenance); **P2** shows this | `closed=1` on an export while the subject is present in the corresponding work tree (**M1a**) | **survived** — false pass of cleanup |
| **M2** | work tree with untracked subject → `closed=0` (**P1**) | `closed=1` with the subject present (**M2a**) | **survived** — false pass of cleanup |
| **M3** | subject present, any cwd → `closed=0` (**P1**, **P4**) | `closed=1` from any cwd ≠ lane root (**M3a**); still red from the root (**M3b**) | **survived**, conditionally (cwd ≠ root) |
| pristine, clean tree | `closed=1` | `closed=1` | green reachable — the gate is not a degenerate always-red control |

Deletion facet (M1's second half): `rm -f "$fx-export/.ufo/waves/round-43/final-gates/all-gates.at-Y.txt.tmp"` → `rm-rc=0`, `export-target-exists: no`, **`worktree-leftover-exists: yes`**, sha unchanged. A gate that "deletes then verifies" against the export root therefore deletes a scratch copy, leaves the inherited 2137-B artefact in place, and prints `closed=1`. On the real lane: `M1-on-lane-export rc=0 | K20 payload=leftover=absent,root=worktree closed=1` against an extraction of `HEAD` that contains **0** `*.tmp` — i.e. the token is green no matter what the work tree holds.

Also observed, and part of the false pass rather than a side note: **M1 certifies provenance it never checked** — it prints `root=worktree` for an export (M1a). A reader of the payload cannot tell the green came from a root that cannot hold the artefact.

## 5. Restoration evidence

- The pristine limb was never mutated in place: mutants are copies. Pristine sha256 before and after the whole probe is identical — `090c556d…` (see §3 and the closing `sha256sum` in §4 run log). Post-restore re-run of the red-before case: `P1-restored rc=1 … closed=0` (red again).
- The fixture subject was moved aside and moved back, not rewritten: `restored-leftover sha256: ea189506…`, `bytes=2137`.
- Diffs are exactly one concept each (§3); no other bytes changed.

## 6. Do-nothing discrimination

- Do-nothing (frozen base `5ab3a60`, and HEAD `6631401`) has **no K20 limb at all** (§1, `grep` rc=1) and its control states no cleanup mechanism — it cannot print `K20 … closed=1`, so it cannot satisfy C1's after-state. It also cannot *manufacture* a green token.
- The mutant is **strictly worse than do-nothing** for C1: it produces a green, provenance-labelled token (`closed=1`, `root=worktree`) while the frozen defect persists. `claims.json:12` demands "at least one red-before control per changed gate"; under M1 the red-before control is **vacuous** whenever it is run in the suite's established `<export-root>` harness, because restoring an untracked file cannot change an export. The only thing that separates mutant from do-nothing is a leftover-present run against a **work tree** root (P1) — which is exactly the control an export-rooted implementation omits.
- Observed at HEAD: the real lane work tree is currently clean (`test -e` rc=1), so *today* every variant is green for the right reason — the discrimination is only demonstrable after restoring the artefact, which is why the reconstructed fixture is the probe's instrument.

## 7. Findings handed to C1 integration (no contract change implied)

1. A cleanup gate for R43-5c must be **work-tree-rooted and must refuse a non-work-tree root** (`root=other → closed=0`); reusing the r43 suite's `<export-root>` argument makes it blind by construction (M1) — the export listing in §1 is the proof, not an inference.
2. The red-before control must **restore the artefact in a work tree** (or a fixture copy of one) and show `closed=0`; an export-based red-before is unsatisfiable and will pass a gate that cannot fail.
3. Any oracle must see **untracked** paths (`-e`/`lstat`, or `git status` without `--untracked-files=no`): the subject is untracked by definition, so a trackedness oracle (M2) is green forever.
4. Paths must be anchored at the resolved root (M3); the lane's own receipts are run from several cwds, so a cwd-relative gate reports clean from anywhere but the lane root.
5. `delete the leftover through the lane helper` (`round-43-verifier-spotcheck.md:105`) has **no executable helper verb** — `scripts/hyaku/jj-lane.sh` exposes only `init|commit|recover|push|state`. Either the helper gains a delete verb or the deletion is a plain `rm` with a recorded receipt; a `deleted-by=lane-helper` token would otherwise be unbacked.
6. If the gate self-deletes, delete and verify must target the **same work-tree path**; deleting at the export root and verifying there is a self-consistent no-op (§4 deletion facet).

## 8. Limitations

- The pristine gate is **my candidate design**, not landed lane code: at HEAD `6631401` no r44/K20 limb exists (§1). The mutants are therefore designed against the *expected* detector shape for R43-5c; they show which shapes are undiscriminating, not that a specific committed gate is broken.
- The fixture subject's **content** is a placeholder padded to the reported 2137 B; the original aborted write was untracked and its bytes were never committed, so no content can be recovered. Only path, size and untracked status are faithful (size from `round-43-verifier-spotcheck.md:20,105`).
- The fixture is a minimal repo (4 files), not a full lane clone; the export/untracked asymmetry it exhibits is a git property, verified additionally on the real lane's own archive (§1, §4).
- I did not run the r43 suite, did not execute any lane gate, and did not evaluate whether the integrator will choose an export- or work-tree-rooted gate; no verdict is offered on C1 or C2 as a whole.
- M3's survival is cwd-conditional (red from the lane root, green elsewhere); it is reported as such rather than as an unconditional false pass.

## 9. Scratch cleanup

Scratch root `/fast/scratch/hyaku/kasegi-r44/R44Mutant5/` (`fx/`, `fx-export/`, `lane-export/`, `limbs/`, `out/matrix.txt`) deleted on exit; deletion result recorded in the seat's final return. Nothing under `/tmp`, nothing in the fleet root, nothing in `~/.local/bin`, nothing in the lane except this report.
