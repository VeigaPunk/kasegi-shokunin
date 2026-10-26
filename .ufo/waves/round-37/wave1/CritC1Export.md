# CritC1Export — export-mode integrity attack list (r37 suite)

Round 37, wave 1, seat `CritC1Export`. Judged on `depth:verifiability` (C1). Adversarial review only:
nothing here is a judgment, admission, edit, integration or ship decision. Receipt only; no lane, fleet,
or source-tree writes.

## Instrument under attack

`corpus/instruments/r37-closure.sh` is **not committed** at lane HEAD
`b362068195d5489aa94b31e6ec8f880c367e0ba0` (`git ls-files corpus/instruments/r37-closure.sh` → 0 lines;
`ls` → "No such file or directory"). The only bytes available are the in-flight build in
`ExecC1SuiteBuild`'s scratch. Two snapshots were taken and every attack re-run on the second:

| snapshot | sha256 | lines | taken (UTC) |
|---|---|---|---|
| v1 | `358444d6b8eeb998ed6d5668951d73268af441fea77dd79c9a600012d45f8d9c` | 1329 | 17:08 |
| v2 | `d4f65f0a6c1d557b6fe233b402e0d30362d65c8d2ef5f34d28a8cb7c71bf69d2` | 1333 | 17:15 |

`diff v1 v2` = 10 changed lines, all inside `check_e9`'s payload display (`dirty_disp`, `skip=''`); no
export-mode, digest, containment or quiescence *logic* changed. Every finding below is measured on **v2**;
the v1 observations cited are marked as such and are unaffected by that diff.

Fixtures were built only under `/fast/scratch/hyaku/kasegi-r37/CritC1Export/` with
`git init` in a `mktemp -d` under scratch, each verified `rev-parse --show-toplevel` == physical fixture
path. Lane access was read-only git (`rev-parse`, `ls-tree`, `ls-files`, `cat-file`, `archive`, `status`).
Tool versions: git 2.56.0, GNU tar 1.35. No tools installed or upgraded. Lane HEAD and status unchanged
throughout (`git status --porcelain | sha256sum` → `6b8e9457e326202e102c2356595e3fd9bd86fbbe954f89c01a3582eb18fb995c`,
HEAD `b362068…`).

Lane fact that shapes the whole review: the export tree is **not** a leaf-only tree. `git ls-tree -r HEAD`
carries 58 mode-`120000` entries (6743×100644, 465×100755, 58×120000); 6 of the 58 have **absolute**
targets into the live lane, e.g.
`.ufo/waves/round-25/assimilation/rows/validate/corpus/knowledge -> /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge`,
and 52 are relative (one such, `.ufo/waves/round-31/wave1/ExecCensusDry/validate/corpus/knowledge/ai-assisted-finding-validation.md
-> ../../../../../../../../corpus/knowledge/…`, resolves back to `<export>/corpus/knowledge/…`). A blanket
"no symlinks in the export" guard is therefore impossible; any seal must be scoped to the paths the checks read.

## Attack list

Severity is the false-green it buys; likelihood is for this lane and this campaign.

### A1 — a check reads through a committed symlink, outside the export root — OPEN, severity high

- Exploit sketch: commit the file a check greps as a symlink whose target is outside the export (absolute,
  or enough `../` to climb out). `check_e5`, `check_e12`, `check_e14`, `check_e10`, `check_e6`, `check_e8`
  all use `[ -f … ]`/`-s`/`grep`, which follow symlinks; nothing `lstat`s the path or consults the
  `git ls-tree` mode.
- Observed (v1, fixture `fa` 120000 entry): `.ufo/waves/round-35/claims-erratum-d5.md` committed as
  `120000 -> <scratch>/decoy-d5.md` (a file outside the repo) →
  `E5 payload=claims-erratum-d5=1 closed=1`, `closed=2/14 exit=1`.
- Likelihood: MEDIUM. The house habit is to commit symlinks into wave dirs (58 already tracked, 6 pointing
  at the live lane), so a new evidence path committed as a link is not exotic; and the 6 absolute links mean
  any future recursive check under `.ufo/waves/**` reads the **live lane**, not the named ref.
- Guard now: none.
- Smallest safe correction: in `check_e1…e14`, before reading, reject `-L` on each exact path read
  (`SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/lessons/round-3{5,6,7}.md`, `LOG.md`,
  `.ufo/waves/round-35/claims-erratum-d5.md`, `.ufo/waves/round-35/wave1-results.json.provenance.md`,
  `.ufo/waves/round-34/wave1/L1Integration.md`, `.ufo/waves/round-37/final-gates/all-gates.txt`,
  `corpus/instruments/r37-closure.sh`), or one pre-check that walks exactly that list and prints
  `symlinked=1` as a red limb. Do **not** use a blanket `find -type l` (see lane fact above).

### A2 — the gate's own transcript (`all-gates.txt`) read from a symlink target — OPEN, severity high

- Exploit sketch: commit `.ufo/waves/round-37/final-gates/all-gates.txt` as a symlink to any file outside
  the export, carrying the digest the executing suite prints.
- Observed (v2, fixture `fa2`, `git ls-tree` `120000 … all-gates.txt`):
  `E10 payload=all-gates=1,digest-match=1,e-payload-lines=14,closed-line=1,selftest-case-lines=14,selftest-summary=1 closed=1`.
  E10 certifies a transcript that is not in the export at all.
- Likelihood: MEDIUM (same reason as A1); this is the single most damaging green because E10 is the
  evidence-of-evidence limb for C1.
- Guard now: none.
- Smallest safe correction: `[ ! -L "$p" ] && [ -f "$p" ]` in `check_e10` (and the E5/E12/E14 equivalents),
  plus the A1 path list.

### A3 — E10's digest is self-referential, not bound to the named head's blob — OPEN, severity high (kill-rule class)

- Exploit sketch: run any *modified* suite whose transcript header names its own digest. `check_e10`
  compares the transcript's `suite-sha256` to `suite_digest()` (`r37-v2.sh:194-200`, called at `:596`),
  which hashes `SELF` — the bytes being interpreted — never the ref's blob
  (`git cat-file blob "$REF_RESOLVED":corpus/instruments/r37-closure.sh`). So a transcript can be produced
  by, and validated with, bytes that are not the ones committed at the head the run names.
- Observed (v2, fixture `fe`): committed blob
  `d4f65f0a6c1d557b6fe233b402e0d30362d65c8d2ef5f34d28a8cb7c71bf69d2`; transcript header
  `suite-sha256=92752de967f26142fc4789807903905b80ee3e6a7b5804d438aed67e64b97518` (one-byte-mutant copy);
  run of the mutant → `E10 payload=…,digest-match=1,… closed=1`. The frozen claim's E10 reading
  ("sha == digest of the suite bytes") is not what the check tests.
- Corroborating shape: `grep -cF '$Format' r37-v2.sh` → 0 and no `cat-file blob` anywhere in the suite;
  `selftest_case_E10` mutates the digest to all-zeros and truncates counts, but never tests
  "transcript digest ≠ committed blob digest while == executing digest", so the mutation set cannot catch it.
- Likelihood: HIGH that an independent verifier recomputing from the ref blob disagrees; a one-byte edit to
  the in-flight suite (this wave is editing it live) already produces the disagreement while E10 stays green.
- Guard now: none.
- Smallest safe correction: in `check_e10`,
  `blob=$(git -C "$LANE" cat-file blob "$ref:corpus/instruments/r37-closure.sh" | sha256sum)`; require
  `got == blob` **and** `got == $(suite_digest)`; die 2 if the blob cannot be read. Add the corresponding
  `st_neg E10 digest-names-other-suite` mutant (transcript = executing digest, ≠ blob digest) so
  `--selftest cases=14` proves the binding.

### A4 — `--lane` pointed at a subdirectory defeats the `--work` containment guard — OPEN, severity low-medium

- Exploit sketch: `--lane <repo>/sub` normalises `LANE` to the subdirectory, but `git archive` then exports
  that subtree as a root and `--work <repo>/probe` is no longer "inside the lane", so the suite creates and
  extracts inside the repository.
- Observed (v2): `--lane fb/sub --work fb/probe --export-ref HEAD` → run proceeded
  (`export-ref=081cdf8f…`, `closed=0/14 exit=1`) and `fb/probe` exists; `git status` stays clean because the
  leftover is an empty untracked directory. With no `SCORECARD.md` in the subtree the guard fires
  (`r37-closure: export has no SCORECARD.md …`, exit 2) but **after** `mkdir` — `probe` remains, 0 entries.
- Control still green: `--lane fb --work fb/probe` → `--work must be outside the lane …`, exit 2, no
  directory created; `--lane fb --work <symlink-to-fb>/w` → refused with the physical path, no directory.
- Likelihood: LOW (caller error), but it voids the "outside the lane" invariant the suite advertises, and the
  empty-dir residue is invisible to the E9 status limb.
- Guard now: partial (`realpath -m` + physical re-check against `$LANE` only; `r37-v2.sh:251-262`).
- Smallest safe correction: derive `LANE_TOP=$(git -C "$LANE" rev-parse --show-toplevel)` and compare
  `--work` against `LANE_TOP` (or refuse a `--lane` whose toplevel ≠ the normalized lane), before `mkdir`.

### A5 — TMPDIR inheritance can place the auto work dir inside a repository — OPEN, severity medium

- Exploit sketch: `WORK=$(mktemp -d -t r37-closure.XXXXXXXX)` (`r37-v2.sh:266`) honours `TMPDIR`
  uncritically; the `--work` containment check is never applied to the auto path.
- Observed (v2, fixture `fb2`): `cd fb2; TMPDIR=fb2/tmpx4 suite --export-ref HEAD` →
  `tar -xf - -C …/fb2/tmpx4/r37-closure.J2Ox5MC9/export` — extraction happened **inside** the repo. A
  relative `TMPDIR=reltmp` resolves against the caller's cwd, so running from a lane directory does the same
  in the lane. Exit was 1 (E9 red), but the writes had already landed. E9 counts only `SCRATCH_ROOT`
  children, so this residue is invisible to it.
- Likelihood: LOW-MEDIUM (needs `TMPDIR` set to an in-repo path; seats do set `TMPDIR`).
- Guard now: none.
- Smallest safe correction: after `mktemp`, `WORK=$( cd "$WORK" && pwd -P )` and apply the A4 `LANE_TOP`
  containment test (die 2); print `work=<physical>` in the header so the path is auditable.

### A6 — work-dir reuse with stale bytes — GUARDED (measured), keep

- Exploit sketch: pre-seed a reused `--work` with `export/.ufo/waves/round-37/final-gates/all-gates.txt`
  (forged, correct digest), `export/STALE-MARKER`, `mut/leftover/`, or make `export` a symlink to a
  directory of forged evidence.
- Observed (v2): seeded `all-gates.txt` + `STALE-MARKER` + `mut/leftover` → `E10 payload=all-gates=0,… closed=0`,
  `closed=0/14 exit=1`; after exit `stale-marker=no export-dir=no mut-dir=no work-entries=0`. Symlinked
  `export/` target: `target-kept=yes`, link gone, no export dir left. `rm -rf -- "$EXPORT" "$MUT"` +
  `mkdir` before extraction (`:273-274`) is the guard; stale bytes cannot satisfy a check.
- Residual: the work dir root itself is never cleaned; `--selftest` report files under `$WORK` are
  re-truncated each run (`>` at `:1217-1250`), so they cannot go stale either.

### A7 — two runs sharing one `--work` clobber each other's export — OPEN, severity high

- Exploit sketch: `rm -rf -- "$WORK/export"` and extraction are unconditional; there is no lock and no
  per-run subdirectory. A second run (rerun driver, a gate re-run, or a human retry) against the same
  `--work` mid-flight deletes the first run's export and substitutes its own ref's bytes.
- Observed (v2, instrumented copies with `sleep` after extraction only to widen the natural window;
  repos `r1` (has `.ufo/waves/round-35/claims-erratum-d5.md`) and `r2` (does not), same `--work`):
  run A (`--lane r1`) reported `E5 payload=claims-erratum-d5=0 closed=0` where its solo control reports
  `claims-erratum-d5=1 closed=1` — A judged r2's export. Run B then died
  `r37-closure: export has no SCORECARD.md (not a lane tree): da2cfebc…`, exit 2, because A's cleanup had
  removed B's export. Both runs clean the shared dirs on exit (`work entries after: 0`).
- Likelihood: MEDIUM in this campaign — the wave has a rerun driver and gate reruns; any overlapping
  invocation with a reused `--work` is a false-provenance source (a report about ref X computed from ref Y).
- Guard now: none.
- Smallest safe correction: own a private subdirectory per run (`WORK_RUN=$(mktemp -d "$WORK/run.XXXXXXXX")`
  when `--work` is given, or `flock` a lock file under `$WORK` and die 2 on contention), and keep
  `export/`, `mut/` under the private dir.

### A8 — status read and the rest of the gate are not atomic (TOCTOU) — OPEN by design, severity low

- Exploit sketch: E9's `git status --porcelain` is a point sample (`:560`); whatever dirties the lane after
  that read is invisible, and the summary line still says `closed=14/14 exit=0`.
- Observed (v2, fixture `frace2`, a writer creating `dirty.txt` 1.2 s into the run while an instrumented
  copy's E9 sleeps after its status read): `E9 payload=status-read=ok,status-dirty=0,…,closed=1` and
  `repo-dirty-at-exit: ?? dirty.txt`. The instrument only widens the natural window.
- Likelihood: MEDIUM that the sample is stale by the time the gate is filed (the transcript is committed by
  a later commit), severity LOW because the residue is visible to the next reader.
- Guard now: none; the claim is a point sample, so this is a depth limit, not a contradiction.
- Smallest safe correction: take a second sample after the summary (or print `status-final=` from a re-read)
  and require both clean; keep `--no-optional-locks` (measured: no `index.lock`).

### A9 — E9's self-exclusion launders a leftover seat dir — OPEN, severity medium

- Exploit sketch: E9 counts `find "$sroot" -mindepth 1 -maxdepth 1 -type d` but skips its own `$WORK`
  (`:570`, `:578`). Run the gate with `--work <scratch-root>/<leftover>` and the leftover is excluded from
  the count while it remains on disk after the run.
- Observed (v2, fixture `e9only2`, root containing `SeatLeftover/` with junk):
  control (`--work` outside the root) → `scratch-seat-dirs=1 closed=0`; laundered (`--work …/SeatLeftover`)
  → `scratch-seat-dirs=0 … closed=1`, `leftover-after=yes`. Same effect for the gate's own work dir when it
  lives under the default `SCRATCH_ROOT=/fast/scratch/hyaku/kasegi-r37`: the run reports "no seat dirs" and
  leaves exactly one behind.
- Also measured in the same run: `-type d` misses a symlinked seat dir and anything nested below depth 1
  (counted 2 for `LeftoverSeat/ nest/sub/ SymlinkedSeat->…`).
- Likelihood: MEDIUM for the default-root case, LOW for deliberate laundering.
- Guard now: partial (self-exclusion is intentional, and needed, only when `--work` is *outside* the root).
- Smallest safe correction: exclude `$WORK` only when it is not a direct child of `$sroot`; and have the
  gate either run with `--work` outside the scratch root or delete its work dir before the quiescence claim.

### A10 — tar path traversal — GUARDED by git and GNU tar, keep (do not rely on it silently)

- Exploit sketch: a tree member that climbs out (`..`, absolute path), or a symlink entry followed by a child.
- Observed: `git mktree` *does* accept a `..` entry (exit 0), so the tree can exist; but
  `git archive` refuses it — `error: invalid path '..'`, exit 128 — and the suite's
  `git archive … | tar -xf -` fails closed (`pipefail` → `die`). A handcrafted tar with `../escaped.txt`
  plus `link/through.txt` is refused by GNU tar 1.35: `Removing leading '../' … Member name contains '..'`,
  `link/through.txt: Cannot open: Not a directory`, exit 2; nothing landed outside. A gitlink (160000)
  exports as an empty `sub/` directory only.
- Guard now: external tool defaults plus `pipefail`. Not the suite's own property.
- Smallest safe correction (cheap hardening, no behaviour change on valid trees): validate the member list
  before extraction, `git archive … | tar -t | grep -E '(^/|(^|/)\.\.(/|$))'` must be empty, and extract
  with `--no-same-owner --no-overwrite-dir`.

### A11 — `.gitattributes` `export-ignore` / `export-subst` rewrite or drop the export — mostly fail-closed, contingent hole

- `export-ignore` on `SCORECARD.md`: `git archive` drops it → `export has no SCORECARD.md (not a lane tree)`, exit 2.
  `export-ignore` on a required file drops it → that check is red (`E5 payload=claims-erratum-d5=0 closed=0`
  measured). Every closing limb is a presence requirement, so `export-ignore` cannot turn red into green.
- `export-subst`: exported bytes ≠ committed bytes. Measured (v1 fixture `fg`): committed blob
  `75a2a912…`, exported copy `d9be830c…`, `$Format:%H$` replaced by the commit hash in the export. Contingent:
  neither snapshot contains `$Format` (`grep -cF '$Format'` → 0), so it is inert today. It becomes a hole the
  day a `$Format` string lands in `SCORECARD.md`, a lesson, or the suite itself (E14 reads the exported
  bytes; E10 reads the exported transcript).
- Likelihood: LOW. Smallest safe correction: with A3's blob-bound digest, compare the committed blob to the
  exported copy for the files checks read (`export-subst` mismatch → red); no `.gitattributes` handling needed.

### A12 — ambient environment: TMPDIR/PATH are inherited, not pinned — OPEN, severity low

- Exploit sketch: the suite resolves `git`, `tar`, `sha256sum`, `awk`, `grep`, `find`, `realpath`, `mktemp`
  from the caller's `PATH`, and honours `TMPDIR` (A5). A seat or wrapper that prepends a scratch `bin/`
  executes different bytes than the verifier assumes, with no trace in the report.
- Likelihood: LOW (all observed `PATH`s are normal), severity moderate if it happens (silent tool substitution).
- Guard now: none.
- Smallest safe correction: set a fixed `PATH=/usr/bin:/bin` at the top of the suite (and/or absolute tool
  paths), and record `tool=$(command -v git) $(git --version)` in the header.

## Smallest safe correction set — land before the suite commit (ordered)

1. **E10 blob binding (A3).** Replace `want=$(suite_digest)` with a recompute of
   `git -C "$LANE" cat-file blob "$ref:corpus/instruments/r37-closure.sh"`; require header == blob == SELF;
   die 2 if unreadable; add the `digest-names-other-suite` selftest mutant.
2. **Seal the read paths (A1, A2).** Per-path `[ ! -L ]` on the ~12 files the checks read, with a red
   `symlinked=1` payload token; no blanket `find -type l` (58 legit links, 6 absolute into the live lane).
3. **Containment by toplevel (A4, A5).** Compare `--work` and the resolved auto work dir against
   `git rev-parse --show-toplevel`, before `mkdir`; print the physical work path in the header.
4. **Private work dir / lock (A7).** Per-run subdir under `--work` (or `flock`), so concurrent runs cannot
   clobber `export/`.
5. **Quiescence honesty (A8, A9).** Re-read status after the summary; exclude `$WORK` from the seat-dir count
   only when it is outside `$sroot`.
6. **Extraction hardening (A10, A12).** Pre-validate `tar -t` member names; `--no-same-owner
   --no-overwrite-dir`; fixed `PATH`.

## Not defects — tradeoffs the judge should read as depth limits, not regressions

- **E1 accepts any ancestor** (`git merge-base --is-ancestor "$h" "$ref"`). Necessary: the section cannot
  name its own commit. Consequence: a "Final lane commit: <old ancestor>" line closes E1, which is the D4
  *shape*; only the literal `Final lane commit: e666d902` is banned (E12). The D4 class survives with a
  different hash.
- **E12 is a spot-ban**, not a shape check: `c20300df` + `anchor ancestor` present, `e666d902` absent. A
  second "Final lane commit: <ancestor>" line in the round-37 section is green on both E1 and E12.
- **E14 is a spelling check** on the committed bytes (`status --porcelain` sites without `2>/dev/null` or
  `|| true`, marker present). It cannot prove runtime fail-closedness. The runtime was measured green here:
  fixture with `chmod 000 .git/index` → `git status` rc 128 →
  `E9 payload=status-read=failed,status-dirty=0,… closed=0`, suite exit 1 (fail-closed behaviour confirmed;
  v2's `dirty_disp='?'` display change is consistent with it).
- **E9's own-work exclusion** is required for a work dir under the scratch root; A9 is the operational
  consequence, not a logic bug.

## Required reds — not this seat's to exercise

The frozen C1 required-reds (`--export-ref cc692008…` and `a23dc478…` → `closed<14/14 exit=1`) and the
`closed=14/14` final-head run are the scheduler's/gate's to measure. Note they cannot be measured against the
committed suite until `corpus/instruments/r37-closure.sh` exists at lane HEAD; the findings above bind to the
in-flight bytes and must be re-attacked on the committed blob (A3 is precisely the check that would catch a
mismatch between the committed blob and the bytes that produced the transcript).

## Risks / blockers

- Instrument not committed (see above): the verdict of this review is against `d4f65f0a…`; the suite seat is
  still editing, so re-run A1/A2/A3/A7 against the committed blob before the gate.
- No blockers for this receipt; no lane/fleet/source-tree writes; scratch dir removed after write.
