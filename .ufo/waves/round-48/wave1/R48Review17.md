# R48Review17 — Directory pointer acceptance attack (kasegi round 48, wave 1)

- Seat: `R48Review17`, reviewer, leaf member (no subagent dispatch). Date: 2026-10-30.
- Scope: attack the frozen counter's evidence-pointer acceptance — evidence pointing at a **directory** rather than a file must be rejected `SF-POINTER`. Author-side form only, never promotion or semantic truth. No production edits, no commit/push, no target testing, no tool installs (none needed).
- Report path: `.ufo/waves/round-48/wave1/R48Review17.md` (relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, as written here).
- Read `/home/vgpnk/.omp/agent/RULES.md` first: tooling directive noted; no installs performed, no pacman transactions initiated.

## Frozen references

- Freeze commit cited by tasking: `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` — confirmed in the lane repo: `git cat-file -t` → `commit`; `git log --oneline -1` → `3546f70 round-48: freeze canonical checklist restoration and controls` (read-only invocations).
- `.ufo/waves/round-48/freeze.txt`: `frozen-at: 2026-10-30T14:30:48.968093Z`, `claims-sha256: b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345` — matches observed `sha256sum` of `.ufo/waves/round-48/claims.json`.
- Counter bytes (frozen): `corpus/instruments/shonen-form.py`, sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` (read-only every run; hash identical before and after, see Restoration evidence).
- Measured checklist: production `SHONEN.md` sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0` — the landed round-48 candidate; grades `shonen-form canonical=1 finding=SF-CLEAN exit=0` against the production root (observed this session, command below).
- Interpreter: Python 3.14.8 (host `python3`).
- Pointer logic under attack (frozen source, verbatim): the evidence line's first token (split on `' — '`) is rejected `SF-POINTER` when empty, absolute, containing `..`, non-normalized (`token != Path(token).as_posix()`), resolving outside `--root`, or failing `resolved.is_file()`.

## Method

Scratch: `/fast/scratch/hyaku/kasegi-r48/R48Review17/` (explicitly created; removed on exit — receipt below). No `/tmp` clones.

- `pristine.md` = byte copy of production `SHONEN.md` (sha256 `b1352168…`, verified after `cp -p`). Box 1's evidence line in these bytes: `      Evidence: SKILL.md — Author assertion; outside promotion verification remains required.` (appears exactly once; boxes 2–4 keep the candidate's own pointers).
- Fixture root `root/` = isolated tree under scratch containing every pointer target the four boxes use (`SKILL.md`, `LOG.md`, `PROVINCE.md`, `corpus/lessons/round-47-verifier-spotcheck.md`) plus the attack surface: `corpus/` and `corpus/lessons/` directories, symlinks (`dirlink→corpus`, `filelink→LOG.md`, `outlink→/etc/passwd`, `brokenlink→MISSING.md`), a fifo `fifo0`, a chmod-000 `secret.txt`, a literal backslash file `weird\name.txt`. First battery attempt missed three box targets and every case failed on box 3/4 instead of box 1 — caught by the positive control, fixture corrected before any verdict was recorded. Isolation discipline: each mutant changes exactly one line (box 1's evidence) except the named all-four case; the driver asserted single-line diffs.
- Driver `probe_dir_pointer.py` (scratch fixture, reproduced behavior in the tables below): builds each mutant, runs the frozen counter as `python3 corpus/instruments/shonen-form.py --root <fixture-root> --file <mutant>`, records expected vs observed `finding`/`exit`.

## Battery — expected vs observed (fixture root)

All 28 cases; expected derived by hand from the frozen source, recorded before the runs.

| # | case | box-1 evidence token (after `Evidence: `) | expected | observed | verdict |
|---|---|---|---|---|---|
| 1 | file-positive | `LOG.md — …` | SF-CLEAN/0 | SF-CLEAN/0 | PASS |
| 2 | **dir-bare** | `corpus — note` | **SF-POINTER/1** | **SF-POINTER/1** | **PASS — seat attack** |
| 3 | dir-trailing-slash | `corpus/ — note` | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 4 | dir-nested | `corpus/lessons — note` | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 5 | dir-dot | `. — note` | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 6 | dir-dotdot-tail | `corpus/.. — note` | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 7 | no-note-dir | `corpus` (no note) | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 8 | dir-symlink | `dirlink — note` (symlink→dir) | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 9 | dir-all-four | all four boxes → `corpus — note` | SF-POINTER/1 | SF-POINTER/1 | PASS (uniform per-box) |
| 10 | missing-file | `MISSING.md — note` | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 11 | absolute | `/etc/passwd — note` | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 12 | dotdot | `../LOG.md — note` | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 13 | dot-prefix | `./LOG.md — note` | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 14 | double-slash | `corpus//lessons — note` | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 15 | inside-dotdot | `corpus/../LOG.md — note` | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 16 | file-dot-tail | `LOG.md/. — note` | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 17 | empty-token | ` — note` (empty token) | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 18 | whitespace-token | `   — note` | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 19 | outside-symlink | `outlink — note` (→/etc/passwd) | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 20 | broken-symlink | `brokenlink — note` (dangling) | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 21 | fifo | `fifo0 — note` | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 22 | name-too-long | 300×`a` | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 23 | backslash-missing | `corpus\lessons — note` (absent) | SF-POINTER/1 | SF-POINTER/1 | PASS |
| 24 | file-symlink | `filelink — note` (→LOG.md) | SF-CLEAN/0 | SF-CLEAN/0 | PASS (documented acceptance) |
| 25 | backslash-existing | `weird\name.txt — note` (POSIX literal) | SF-CLEAN/0 | SF-CLEAN/0 | PASS (documented acceptance) |
| 26 | perm-denied-file | `secret.txt — note` (chmod 000) | SF-CLEAN/0 | SF-CLEAN/0 | PASS (existence/type only) |
| 27 | note-mentions-dir | `LOG.md — see corpus/ for history` | SF-CLEAN/0 | SF-CLEAN/0 | PASS (dir in free note text) |
| 28 | nul-in-token | `LO␀G.md — note` | robustness probe | crash, see below | recorded |

Driver summary (run 1 of 3): `total=28 pass=28 fail=0`.

Exemplar commands (fixture root), exactly as executed:

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py \
    --root /fast/scratch/hyaku/kasegi-r48/R48Review17/root \
    --file /fast/scratch/hyaku/kasegi-r48/R48Review17/mutants/pristine.md
shonen-form canonical=1 finding=SF-CLEAN exit=0        # positive control vs fixture root

$ python3 …/shonen-form.py --root …/R48Review17/root --file …/mutants/dir-bare.md
shonen-form canonical=0 finding=SF-POINTER exit=1      # the seat attack

$ python3 …/shonen-form.py --root …/R48Review17/root --file …/mutants/dir-all-four.md
shonen-form canonical=0 finding=SF-POINTER exit=1      # all four boxes → dir
```

## Production-root cross-check

Same frozen counter, `--root /home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only; the counter only `stat()`s pointer tokens under root):

```
$ python3 …/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --file …/mutants/dir-bare.md            → shonen-form canonical=0 finding=SF-POINTER exit=1
$ python3 … --file …/mutants/dir-trailing-slash.md → shonen-form canonical=0 finding=SF-POINTER exit=1
$ python3 … --file …/mutants/dir-nested.md         → shonen-form canonical=0 finding=SF-POINTER exit=1
$ python3 … --file …/mutants/file-positive.md      → shonen-form canonical=1 finding=SF-CLEAN exit=0
$ python3 … --file /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md
                                                  → shonen-form canonical=1 finding=SF-CLEAN exit=0
```

`corpus/` and `corpus/lessons/` are real directories in the production tree; both bare and shaped directory pointers are rejected exactly as in the fixture.

## Determinism

The full battery ran three times (runs 1–3, plus two production-root spot checks). Runs 2 and 3 outputs are byte-identical (`diff run2.txt run3.txt` → empty; driver exit 0 both times). Every mutant's sha256 was stable across all three runs (driver-recorded hashes re-verified against the final on-disk bytes: drift `none`). The counter is read-only; no observed run wrote anything.

## Verdict

- **Seat attack defeated by the frozen counter.** Every directory-pointer shape — bare, trailing slash, nested, `.`, `..`-carrying, note-less, symlink-to-dir, and all-four-boxes — grades `canonical=0 finding=SF-POINTER exit=1`, deterministically, on both the isolated fixture root and the production tree. Expected = observed on all 28 cases. The frozen predicate's claim "evidence pointer existence is checked, not semantic truth" holds mechanically: `resolved.is_file()` admits only regular files (and symlinks to them), and never a directory.
- No false greens found anywhere on the pointer frontier; no false reds against legitimate file pointers.
- This is author-side form verification only; nothing here speaks to promotion or evidence truth.

## Observations (recorded, not fixed — counter bytes frozen)

1. **NUL robustness gap (case 28).** A NUL byte inside the pointer token crashes the counter before grading: stderr `ValueError: lstat: embedded null character in path` (raised from `Path.resolve()`), stdout empty — the frozen one-line output contract is not produced; process exit 1 via uncaught exception. A crash is not a graded verdict: per the lane's gate vocabulary this is at best a `could-not-evaluate`-shaped outcome delivered as a traceback, and a SHONEN.md carrying NUL would be rejected by side effect rather than by `SF-POINTER`. Reported as a defeat of the frozen output contract, per seat rules left untouched.
2. **SF-POINTER class coarseness.** All 23 distinct rejection causes collapse to the single finding `SF-POINTER` (normalization, escape, nonexistent, directory, fifo, dangling symlink are indistinguishable in the output). Sensitivity is total; diagnostic precision is per-class only. Same coarseness class as the sibling `SF-BOX` observation (R48Probe16).
3. **Documented acceptances** (consistent with the frozen source, kept clean): symlink to a regular file inside root; POSIX literal backslash filename; chmod-000 file (existence/type checked, not readability); a directory path mentioned inside the free note text after the first token (only the first token is the pointer, per the frozen comment "optional explanatory text").

## Restoration evidence

Production lane files unchanged (sha256 identical before and after every run):

| File | sha256 before | sha256 after |
|---|---|---|
| `SHONEN.md` | `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0` | same |
| `corpus/instruments/shonen-form.py` | `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` | same |
| `.ufo/waves/round-48/claims.json` | `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345` | same |

`git status --porcelain` in the lane root after the runs shows only sibling-authored untracked wave-1 reports (and this report once written); nothing tracked was modified. No git/jj index or state was read mutatively or written; no files outside this report and the (now removed) scratch dir were created, modified, or deleted.

Scratch removal (receipts embedded above first, then removal per seat spec):

```
$ rm -rf /fast/scratch/hyaku/kasegi-r48/R48Review17
$ ls /fast/scratch/hyaku/kasegi-r48/
KasegiR48a2  R48Review08  l1-novelty
```

Only my own `R48Review17` directory was removed; sibling scratch dirs were left untouched.

## Notes

- Round-47 verifier routes R1/R2 were not consulted: this seat's oracle is fully defined by the seat spec plus the frozen counter; no verifier-route input was needed.
- No build/lint blanket verification was run; only the assigned bounded probe executed.
- No delegation, no background jobs, no tool installs.
