# SentinelC1 — round-77 w1 — C1 amendment exec-surface and guard audit (read-only)

Target: `.ufo/waves/round-77/c1-amended-reference.py` (sha256 `18bfc439…588a33`, frozen at 539a4387…)
Base: `corpus/instruments/recheck-cwd-census.py` at 2e53fc74 (git blob 80fcc2b8; sha256 `e666ae11…ab52a21a`, matches claims.json).
The freeze-tree instrument path is byte-identical to base (`git diff --stat 2e53fc74 539a4387 -- corpus/instruments/recheck-cwd-census.py` empty).
All runs used scratch `/fast/scratch/hyaku/kasegi-r77/SentinelC1/` with `TMPDIR` pointed inside it. No lane-tree write, no git mutation.

## (1) Exec surface — claim A5 — PASS
- `"bash", "-c"` pairs: reference 1 (c1-amended-reference.py:71), base 1 (recheck-cwd-census.py:70). Unchanged.
- `subprocess.run(` call sites: reference 1 (:71), base 1 (:70). Import at :39 only.
- The only execution path is `run_foreign` (:64-78): `census()` calls it once per first `recheck:` value. `census`, `main`, `selftest`, `first_recheck`, `has_restoration_recheck` contain no exec. The selftest executes values only indirectly through `census()`/`main()`.
- Grep for `os.system|Popen|os.spawn|os.exec|pty|sudo|pip|ssh`: zero hits in the reference.

## (2) Filesystem write sites — PASS
- :66 `tempfile.mkdtemp(prefix="recheck-cwd-", dir=env_tmp)`, `env_tmp = os.environ.get("TMPDIR") or None` (:85). Cleanup `shutil.rmtree` in finally at :78.
- :143 selftest `tempfile.mkdtemp(prefix="recheck-cwd-selftest-", dir=TMPDIR)`; cleanup in the outer finally at :341.
- :146-147 `open(..., "w")` in `write_entry`, :152 `os.makedirs(kdir)` in `fixture`. Both paths are under the selftest scratch.
- Patch/restore, case 3: `tempfile.mkdtemp = recording_mkdtemp` at :216, restored at :220 in `try/finally`. PASS.
- Patch/restore, case 8: `globals()["has_restoration_recheck"]` replaced at :298, restored at :302 in `try/finally`. PASS.
- `sys.stdout` swap in `capture` restored in finally (:159, :163). PASS.
- Read-only sites: `first_recheck` :48 and `has_restoration_recheck` :57 open for read only.
- Note (informational, not a finding): `tempfile.mkdtemp` with TMPDIR unset falls back to the tempfile default, not a hard-coded path. Docstring :24-25 says so.

## (3) Forbidden patterns — PASS
- Pattern `sysctl|pacman|curl|urllib|requests|socket|http|wget|os.system|eval(|exec(|/tmp|Popen|os.spawn|os.exec|pty|sudo|pip|ssh|mkdir`: one hit, c1-amended-reference.py:25, which is docstring prose ("no path is hard-coded under /tmp"). No code-level `/tmp` path.
- `DEFAULT_LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"` (:43) is a string constant used only as a prefix comparison (`prefix = "cd %s && " % lane`, :86). It is not read or written. Same in base.

## (4) Guard compliance — case-4 cleanup and both-headers fixture — PASS
- Empirical: `TMPDIR=<scratch>/tmp python3 -B c1-amended-reference.py --selftest` → rc 0, `selftest cases=12 failures=0`. Afterwards `find tmp -mindepth 1` is empty, so nothing survived. Receipt in `SentinelC1.receipts.txt`.
- Trace of both-headers (case 7, :267-284): fixture root is `scratch/case7`, and `b-both.md` holds `recheck: cd <root7> && touch <root7>/first-ran` plus `restoration-recheck: touch <root7>/restoration-ran`. The census executes only the first line, so `first-ran` is created inside `scratch/case7` and `restoration-ran` is never created (observed `first_ran=True restoration_ran=False`). Both files sit inside the selftest `scratch`, which the outer `finally` removes (:341). The restore-check is `shutil.rmtree`, not a per-file cleanup, so no leak.
- The case-6 restoration fixture likewise never runs its `restoration-recheck:` value (`marker_present=False`).
- Base do-nothing control: `base … --selftest` → `selftest cases=6 failures=0` rc 0, `TMPDIR` residue 0. Matches claims.json.

## (5) Scope — PASS
- `census(root, lane)` reads only `root/corpus/knowledge/*.md` (:82, glob at census). Writes happen only inside tempfile dirs. `main` default root is `"."` (:347) and `--root` is caller-supplied.
- No write to the lane tree from the counter or the selftest.
- Informational (inherited from base, unchanged by the amendment): census executes every first `recheck:` value from `corpus/knowledge/*.md` via `bash -c` with a copy of the full environment (:68-69, env copy) and a 120 s timeout (:44). The `cd <lane> && ` prefix is a naming convention. Nothing sandboxes writes, so a knowledge entry could touch lane files. Not an amendment regression, and A5 explicitly keeps this exec surface.

## Diff scope (A6, cross-check) — PASS (supporting)
- `git diff --no-index` base→reference hunks are at docstring :28-34 and inside `selftest()` only. `first_recheck`, `has_restoration_recheck`, `run_foreign`, `census`, `main` are byte-identical to base.
- Mode note: git records both base and reference as 100755 (`git ls-tree`), so no mode finding.

## Gate probes (scratch-only mutants of the frozen reference, outside the freeze bytes)
- Neutered closure `lambda out, ret: True` → `selftest case=gate-negpolarity FAIL neg_ok=True`, `selftest cases=12 failures=1`, rc 1. Gate catches it.
- Registration deleted → `gate-regs FAIL registered=[]`, `gate-consume FAIL no-registration`, `gate-negpolarity FAIL no-registration`, `failures=3`, rc 1. Gate catches it.
- Scratch mutant copies only; not written to the wave dir or lane.

## Findings
- No FINDING on exec surface, filesystem writes, forbidden patterns, cleanup, or scope.
- Informational only: the exec trust boundary of census (see (5)) is base-design, not introduced by this amendment.
- Tooling: none installed. Used only the host's `python3` and `git` (read-only).
