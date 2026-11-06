# ScribeLesson — round-80 w1 scoped findings

Seat: `ScribeLesson` (scribe; leaf). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, freeze `4ab545865f747fca8456370b5927fe51236fe579`, base `58905f2bbc52db6b1634566cc1be9c92cdddebfb`. Drafting only: no lane file outside `.ufo/waves/round-80/w1/` was written; no counter/gate run; no installs.

**Deliverable:** `.ufo/waves/round-80/w1/lesson-round-80.md` — the round-80 lesson draft for the L1 to integrate into `corpus/lessons/round-80.md`. Sections in the required order (`## Gate`, `## Mistakes`, `## Sources`, `## Learning`), plus a header paragraph stating **one v1 wave of 12 seats** (counted from `w1-spec.json` `items`).

## What the draft states, and on what evidence

- **C1** — frozen bytes re-hashed by this seat (candidate `420151fd…5698`, counter `b47276d1…d450`, table `08d7f3ce…e418`, builder `e0a8c714…0ef3`); table composition measured (28 rows, 27 `assertion` / 1 `exception`, the exception row `K-M3`); the eight predicates one line each; the seven executed controls with their MUTBAT/selftest/P4/P7/P5 lines quoted verbatim from `controls/*.txt`. Target-state values are attributed to seat receipts (`w1/ExecC1Battery.md` for P1/P3/P4/P7/P8; `w1/ExecC1RealTree.md` for P5/P6 on a scratch landing mirror; `w1/MutClassifier.md` for an independent re-run of P3), never to this seat.
- **C2** — S114 access record (URL, 2026-11-06, HTTP 200 per manifest, sha256 `e1ccfb9b…88d2`, 73 lines, 2365 bytes, measured); the six located quotes with line and word count re-measured by plain containment (all `occ=1`, on the declared line 25/35/35/38/39/58, words 11/16/14/9/12/20); admits (six clauses) and rejects with held-ground cites verified by reading (`F51:75`, `F54:19`, `:33`, `:58`, `:41`, `:60`); the S114 row's old cells measured at the freeze commit (`queued` / `—`), new cells quoted as target (worktree reads `mined` / the entry path uncommitted).
- **Mistakes** — M80-1 `routed-reason-transcribed-unmeasured` and M80-2 `line-cite-off-by-one`, each with the command re-run by this seat and its output quoted, `captured-by: none`, a fix with a show-able-to-fail pair. The two appended corrections for `corpus/lessons/round-79.md` are drafted in a fenced block (never in place).
- **Sources** — S114 row before/after, rows added: 1, tier A `docs`; clauses by pin and line; unpinned lines and why; distinctness as recorded by the pre-freeze control; access record.
- **Learning** — expansion / quality / discernment / verifiability, each on measured or receipted facts.

## Status of the two claims as the draft records it

- **C1:** all five predicates assigned to the battery (P1, P3, P4, P7, P8) are met on the frozen candidate by seat receipt; P2 is uncommitted (worktree instrument already hashes `420151fd…5698`); P5/P6 are met on a scratch mirror; landing-commit confirmation and the L1 verdict are **PENDING-L1**.
- **C2:** B0 passes pre-freeze; the worktree shows the integrated state (94 `.md`, 114 registry rows, `knowledge-expected.txt` 96/94, entry byte-identical to `w1-input` sha256 `5b176aa5…c8d8`, S114 `mined`); B1–B7 at the landing commit and the L1 verdict are **PENDING-L1**.

## Findings (routed / for the L1; no verdict changes)

1. **The pre-freeze control set has no candidate full-battery run.** `controls/` holds base, r79-candidate, print-stub forgery and the counter selftest, but not the candidate's own 28-row run; `killed=28/28` exists as the claim's `measured_after_target`, as P3, and (post-freeze) as the battery seat's two runs and the classifier seat's re-run. Recorded in the draft as a fact about the control set, not as a predicate failure.
2. **Classifier carve-out (round-81 routed defect).** `MutClassifier` measured that an assertion-class transform which trips either `exception=` detail branch (`recheck-cwd-census.py:523`, `:532`) scores `EXCEPTION-KILL counted=no` (and lands in `dirty`) — shown with two single-transform probes on the frozen counter. The frozen 28-row table is immune (only `K-M3` emits `exception=`, and it is classed `exception`), so P3 holds as written; the defect is that a row's `class` is read from the observed FAIL shape rather than from the transform's mechanism. Drafted in § Gate C1 and § Learning.
3. **P5 does not discriminate base from candidate on the landing mirror** — `ExecC1RealTree` measured bucket-identical census output for both instruments (`entries=94`, `exit0=72`, `exit1=22`), and a scratch `--lane` yields `noprefix=94` because every recheck prefix is lane-absolute. Recorded as an observation with the claim's shape (the move is the kill set, the TMPDIR refusal and the selftest), not as a defect.
4. **M80-1/M80-2 criteria exist only uncommitted.** `corpus/QUALITY.md:587` (R130) and `:588` (R131) are present in the worktree and absent at the freeze commit (`git show 4ab5458:corpus/QUALITY.md` has neither); both cite `corpus/lessons/round-80.md` § Mistakes M80-1/M80-2, which is the file the L1 will create from this draft. The draft names them with that status and marks their landing **PENDING-L1**.
5. **The two round-79 appended corrections are already drafted in the worktree** (`corpus/lessons/round-79.md`, +5 uncommitted lines) and match `ReviewRouted.md`'s supplied text in substance. The draft reproduces them so the L1 can confirm the wording or drop the duplicate.

## Touched surfaces

- Written: `.ufo/waves/round-80/w1/lesson-round-80.md`, `.ufo/waves/round-80/w1/ScribeLesson.md`.
- Scratch `/fast/scratch/hyaku/kasegi-r80/ScribeLesson/` created and removed before this report; nothing else written. Read-only reads of lane bytes, `git show`/`git grep`/`git diff`/`git status`/`git log`; no git or jj writes.

## Limits

- Seat receipts (`ExecC1Battery.md`, `ExecC1RealTree.md`, `MutClassifier.md`, `ReviewRouted.md`) were read at draft time and may change before WAVE-DONE; the L1 re-reads the final files. Values from them are labelled *receipt*, not *measured*.
- HTTP 200 / raw 18769 bytes / `fetched_utc` are manifest records; the live page was not re-fetched, and the r79 lead's 404 path form was not re-probed — both **PENDING-L1**.
- No landing commit exists at draft time; every "at the landing commit" predicate is **PENDING-L1**.
