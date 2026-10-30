# R48Review18 — C1 frozen counter probe (depth:verifiability)

Seat: R48Review18 (reviewer, godspeed, leaf, no subagent dispatch). Claim: `C1` in
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/claims.json`, frozen at
`3546f7089c224ac6c8adc68208b1e648bbf3e6a5`. Verdict: **the frozen predicate holds on every
kill-rule class I could construct; one fail-closed defect (D61) and four scope limits are
routed below. No counter bytes were changed.**

## Read and verified inputs

- Rules: `/home/vgpnk/.omp/agent/RULES.md` (tooling directive only; no install was needed).
- Frozen counter: `corpus/instruments/shonen-form.py`, sha256
  `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`. Its only commit is the
  freeze `3546f70`; HEAD carries the same bytes, so no post-freeze amendment exists.
- Kill-rule archive: the drifted SHONEN.md with sha256
  `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` is retained at blob
  `29c02f9:SHONEN.md` (round-47 tip) and at base `903d47e:SHONEN.md`, verified by
  `git show <c>:SHONEN.md | sha256sum` (read-only). Drift shape: 52 `^- [~]` lines, 0 `[x]`, 356 lines,
  which matches the round-47 R1 route figure exactly.
- Protocol source: `controls/protocol-source.txt` L446 (seed diff modulo `<name>`; marks confined to
  box character plus one indented evidence line per box) and L453-463 (verbatim seed block).
- Round-47 verifier routes: `corpus/lessons/round-47-verifier-spotcheck.md:85` (R1, SHONEN canonical-form
  drift) and `:86` (R2, plain-target phrasing). Relevance is stated under Routed findings.
- Live lane tree (read-only run of the frozen counter with the frozen command):
  `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin`
  → expected `shonen-form canonical=1 finding=SF-CLEAN exit=0`; observed identical, exit 0. The live
  SHONEN.md sha256 is `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`, unchanged
  across the seat.

## Probe 1 — 64 distinct bounded fixtures through the frozen counter

Every fixture is a scratch tree
`/fast/scratch/hyaku/kasegi-r48/R48Review18/fx/<id>/` with evidence files `SKILL.md`, `LOG.md`,
`PROVINCE.md`, `corpus/lessons/round-47-verifier-spotcheck.md`, and the candidate `SHONEN.md`.
Command for every row (fixture root substituted):
`python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /fast/scratch/hyaku/kasegi-r48/R48Review18/fx/<id>`

Result: **62 MATCH, 2 MISMATCH** (B08 is an expectation error; D61 is a real defect, see below).

| id | group | expected finding/exit | observed finding/exit | probe |
|---|---|---|---|---|
| A01 | control | SF-CLEAN/0 | SF-CLEAN/0 | live lane SHONEN.md bytes |
| A02 | control | SF-PREAMBLE/1 | SF-PREAMBLE/1 | drifted blob 29c02f9 (do-nothing) |
| A03 | candidate | SF-CLEAN/0 | SF-CLEAN/0 | canonical-candidate, all `[~]` LOG.md |
| A04 | seed | SF-CLEAN/0 | SF-CLEAN/0 | verbatim seed, all `[ ]`, no evidence |
| B05 | structure | SF-PREAMBLE/1 | SF-PREAMBLE/1 | title hyphen for em dash |
| B06 | structure | SF-PREAMBLE/1 | SF-PREAMBLE/1 | title names another lane |
| B07 | structure | SF-PREAMBLE/1 | SF-PREAMBLE/1 | no blank after title |
| B08 | structure | SF-PREAMBLE/1 | **SF-BOX/1** | extra blank before first box — **expectation error**: extra blank occupies box-1 slot; SF-BOX is code-correct |
| B09 | structure | SF-PREAMBLE/1 | SF-PREAMBLE/1 | sentence reworded |
| B10 | structure | SF-PREAMBLE/1 | SF-PREAMBLE/1 | UTF-8 BOM |
| B11 | newline | SF-NEWLINE/1 | SF-NEWLINE/1 | CRLF throughout |
| B12 | newline | SF-NEWLINE/1 | SF-NEWLINE/1 | lone CR mid-word |
| B13 | newline | SF-NEWLINE/1 | SF-NEWLINE/1 | final newline removed |
| B14 | newline | SF-NEWLINE/1 | SF-NEWLINE/1 | empty file |
| B15 | hidden | SF-TRAILING/1 | SF-TRAILING/1 | canonical block duplicated |
| B16 | hidden | SF-TRAILING/1 | SF-TRAILING/1 | hidden HTML comment after block |
| B17 | hidden | SF-TRAILING/1 | SF-TRAILING/1 | extra blank line at end |
| B18 | hidden | SF-PREAMBLE/1 | SF-PREAMBLE/1 | opening `<!--` wrapper |
| B19 | hidden | SF-PREAMBLE/1 | SF-PREAMBLE/1 | code-fence wrapper |
| B20 | structure | SF-MISSING-BOX/1 | SF-MISSING-BOX/1 | three boxes only |
| B21 | structure | SF-TRAILING/1 | SF-TRAILING/1 | fifth box appended |
| B22 | structure | SF-BOX/1 | SF-BOX/1 | boxes 1/2 swapped |
| B23 | label | SF-BOX/1 | SF-BOX/1 | `sourcesx` typo |
| B24 | label | SF-BOX/1 | SF-BOX/1 | two spaces after mark |
| B25 | label | SF-BOX/1 | SF-BOX/1 | box indented two spaces |
| B26 | structure | SF-PREAMBLE/1 | SF-PREAMBLE/1 | en dash in title |
| B27 | newline | SF-NEWLINE/1 | SF-NEWLINE/1 | NUL after final newline |
| B28 | separator | SF-EVIDENCE/1 | SF-EVIDENCE/1 | U+2028 inside box-2 label |
| B29 | separator | SF-BOX/1 | SF-BOX/1 | form feed at evidence line end |
| B30 | label | SF-BOX/1 | SF-BOX/1 | trailing space on label |
| C31 | marks | SF-VERIFIER/1 | SF-VERIFIER/1 | `[x]` with valid pointer |
| C32 | marks | SF-EVIDENCE/1 | SF-EVIDENCE/1 | `[x]` without pointer |
| C33 | marks | SF-BOX/1 | SF-BOX/1 | `[X]` uppercase |
| C34 | marks | SF-BOX/1 | SF-BOX/1 | `[?]` |
| C35 | marks | SF-EVIDENCE/1 | SF-EVIDENCE/1 | `[~]` without evidence |
| C36 | marks | SF-CLEAN/0 | SF-CLEAN/0 | `[ ]` with valid pointers |
| C37 | marks | SF-POINTER/1 | SF-POINTER/1 | `[ ]` with missing pointer |
| C38 | marks | SF-EVIDENCE/1 | SF-EVIDENCE/1 | evidence indented five spaces |
| C39 | marks | SF-EVIDENCE/1 | SF-EVIDENCE/1 | `Evidence:LOG.md` no space |
| C40 | marks | SF-VERIFIER/1 | SF-VERIFIER/1 | `[x]` on box 4 |
| D41 | pointer | SF-POINTER/1 | SF-POINTER/1 | `../README.md`, decoy exists one level up |
| D42 | pointer | SF-POINTER/1 | SF-POINTER/1 | absolute `/etc/hosts` (exists) |
| D43 | pointer | SF-POINTER/1 | SF-POINTER/1 | missing `NOPE.md` |
| D44 | pointer | SF-POINTER/1 | SF-POINTER/1 | directory `corpus` |
| D45 | pointer | SF-POINTER/1 | SF-POINTER/1 | `./LOG.md` |
| D46 | pointer | SF-POINTER/1 | SF-POINTER/1 | `corpus//lessons/...` |
| D47 | pointer | SF-POINTER/1 | SF-POINTER/1 | `LOG.md/` |
| D48 | pointer | SF-POINTER/1 | SF-POINTER/1 | `corpus/../LOG.md` |
| D49 | pointer | SF-POINTER/1 | SF-POINTER/1 | in-root symlink escaping root |
| D50 | pointer | SF-CLEAN/0 | SF-CLEAN/0 | in-root symlink to in-root file |
| D51 | pointer | SF-CLEAN/0 | SF-CLEAN/0 | explanation with several em dashes |
| D52 | pointer | SF-POINTER/1 | SF-POINTER/1 | `--` in place of em dash |
| D53 | pointer | SF-CLEAN/0 | SF-CLEAN/0 | filename with a space, file present |
| D54 | pointer | SF-CLEAN/0 | SF-CLEAN/0 | `.git/config` pointer (limit, see below) |
| D55 | pointer | SF-CLEAN/0 | SF-CLEAN/0 | zero-byte evidence file (limit) |
| D56 | pointer | SF-CLEAN/0 | SF-CLEAN/0 | self-pointer to SHONEN.md (limit) |
| D57 | pointer | SF-POINTER/1 | SF-POINTER/1 | FIFO as pointer, no hang |
| D58 | pointer | SF-POINTER/1 | SF-POINTER/1 | absolute path inside root |
| D59 | pointer | SF-POINTER/1 | SF-POINTER/1 | `~/LOG.md` |
| D60 | pointer | SF-POINTER/1 | SF-POINTER/1 | 300-char name: returns POINTER, not unreadable |
| D61 | pointer | SF-POINTER/1 | **NO-FINDING-LINE/1** | embedded NUL in token — **defect**, see below |
| D62 | pointer | SF-POINTER/1 | SF-POINTER/1 | empty token before em dash |
| D63 | pointer | SF-POINTER/1 | SF-POINTER/1 | trailing NBSP |
| D64 | pointer | SF-POINTER/1 | SF-POINTER/1 | trailing tab before em dash |

Receipts: the driver and TSV exist only in scratch (removed on exit). The full TSV row for D61 is
`obs=NO-FINDING-LINE/1 stdout='' stderr_last='ValueError: lstat: embedded null character in path'`.

## Probe 2 — kill-rule and do-nothing controls

- Do-nothing (A02): the drifted blob returns `SF-PREAMBLE exit=1`, matching the claim's
  `expect_before` exactly.
- Candidate (A03, A04, A01): canonical clean forms return `SF-CLEAN exit=0`.
- Hidden / commented / duplicate checklists (B15–B19): all rejected (`SF-TRAILING` or `SF-PREAMBLE`);
  none passes. This satisfies the kill rule's hidden/commented/duplicate clause.
- Historical bytes (kill rule): `29c02f9` and `903d47e` both hash to `596122c0…`; the archive
  requirement is satisfied by git history.

## Probe 3 — mutant kill matrix (scratch copies; production checker untouched)

Eight single-point mutants of the checker, each run against the 64 fixtures. Discriminating kills only
(baseline B08/D61 mismatches excluded from attribution):

| mutant | killed by |
|---|---|
| M1 no trailing check | B15, B16, B17, B21 |
| M2 no `..` guard | D48 (D41 still rejected by containment — defense in depth) |
| M3 no root-containment | D49 |
| M4 accept `[x]` | C31, C40 |
| M5 no newline check | B11, B12, B13, B14, B27 |
| M6 no absolute guard | D58 (D42 still rejected by containment) |
| M7 no evidence for `[~]` | C32, C35, C38, C39, B28 |
| M8 no preamble check | A02, B05, B06, B07, B09, B10, B18, B19, B26 |

Verdict: **8/8 KILLED; 0 SURVIVED.** The frozen checker is not trivially weakened by any single
guard removal, and the checker sha stayed `0ab32a2c…` throughout.

## Probe 4 — traversal / absolute pointer, no target access

- D41 (`../README.md`, decoy present at the fixture's parent) and D42 (`/etc/hosts`) both return
  `SF-POINTER exit=1`, as expected.
- `strace -f -e trace=file` on each: **0** lines mention `README.md` or `/etc/hosts`. The checker rejects
  both before any filesystem access to the target; no file contents were read.

## Routed defects and limits (frozen; reported, not fixed)

1. **D61 — fail-closed crash path (defect, low).** A NUL byte inside an evidence pointer token raises an
   uncaught `ValueError` from `lstat` (the `try` catches only `OSError`/`UnicodeError`). Exit 1 is
   correct in direction; the finding line is missing, so an output-matching driver sees
   `NO-FINDING-LINE`, not `SF-POINTER`. It cannot produce a false pass. Route: counter-errata candidate;
   the frozen bytes are not edited here.
2. **Scope limit — `[x]` always rejected.** Stated in the claim (`mechanical_limits`); the protocol's
   `[x] <verifier-id>` form is therefore unreachable by this counter. Scoped, not a defeat.
3. **Scope limit — pointers into `.git/` accepted (D54), zero-byte evidence accepted (D55), self-pointer
   accepted (D56).** Form-only by the claim's own terms (existence, not truth). Noted for reviewers.
4. **Generalisation gap — hard-coded lane name.** The preamble expects the literal `kasegi-shokunin`, while
   the protocol seed uses `<name>`. Correct for this lane; another lane's SHONEN.md would be rejected
   without editing the counter.
5. **R1 (round-47 route, drift):** the drifted file carried 52 `- [~]` lines; the live file now carries
   4 boxes, each with one evidence line, which satisfies the protocol's "marks confined + one evidence line
   per box" shape as the counter reads it. R1's as-of / `test -e` discipline applies to liveness sentences;
   none are asserted in the live SHONEN evidence text beyond pointer existence, which the counter checks.
6. **R2 (round-47 route, plain targets):** the claim's `after`/`expect` targets are plain
   substrings (`shonen-form canonical=1 finding=SF-CLEAN exit=0`). They are satisfied only by the counter's
   single output line in practice, but R2 asks that future frozen targets be line-anchored (for example
   `^shonen-form canonical=1 finding=SF-CLEAN exit=0$`). Routed as a note for the next freeze; not
   changed here.

## Not done / boundaries

- No production file, fleet file, sibling lane, git/jj index or state was modified. Git use was limited to
  read-only `show`, `cat-file`, `rev-parse`, `log`.
- No package installs or upgrades; no pacman transactions; `strace` was already present at `/usr/bin/strace`
  and was used, not installed.
- No delegation, no background jobs, no commit/push.
- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Review18/` was created for this seat and removed on exit after
  these receipts were captured above.

## Checks the main agent should run

- The frozen counter command against the live lane root: expected `shonen-form canonical=1 finding=SF-CLEAN exit=0`
  (observed by this seat; re-run only if the lane tree moved after commit `3d7e042`).
- Recompute `sha256sum corpus/instruments/shonen-form.py`; expected `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`.
