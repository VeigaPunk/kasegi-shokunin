# SentinelCounter — W1 security review (kasegi round 74, attempt 1)

Seat: SentinelCounter (sentinel, leaf). Date: 2026-11-05. Scope: exec surface of the C1
amendment, path confinement/RC-8 status, R-NOSECRET lens on the trial package and the
frozen S109 disclosure, scratch hygiene. Reviewer made no edits to any lane file except
this report and the two receipts named in §3.4.

## Verdict summary

| Surface | Verdict |
|---|---|
| C1 amendment exec surface (kill rule (d)) | PASS — zero new exec sites; single `bash -c` call site preserved |
| RC-8 (`cd /` recheck value via `bash -c`) | UNCHANGED — neither expanded nor mitigated; still pending operator decision |
| Path confinement (fixtures) | PASS — every write resolves under the TMPDIR-honoring scratch; no new write path |
| R-NOSECRET lens (S109 + trial tree, 11 files) | CLEAN — 1 match, dispositioned benign false positive; nothing to redact |
| Security findings requiring action | NONE — L1 not messaged (nothing actionable) |

## 1. Exec surface

### 1.1 Original counter at freeze (847b53792d2d29d161cad7d21a33c89df9e52e8d)

```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 847b53792d2d29d161cad7d21a33c89df9e52e8d:corpus/instruments/recheck-cwd-census.py > $S/orig-counter.py   # exit 0, 162 lines
grep -nE 'bash -c|subprocess|Popen|os\.system|check_output|check_call|shell[[:space:]]*=[[:space:]]*True|shlex|os\.exec[^u]|[^a-z]exec\(|[^a-z]eval\(' $S/orig-counter.py   # exit 0
grep -nE 'system|popen|shell[[:space:]]*=|shlex|execv|execve|spawn|os\.exec|eval\(|exec\(|commands\.|pty' $S/orig-counter.py   # exit 1 (no match)
grep -c 'subprocess\.run' $S/orig-counter.py   # -> 1, exit 0
grep -c '"bash", "-c"' $S/orig-counter.py      # -> 1, exit 0
```

Hits: L9 docstring mention, L28 `import subprocess`, L51-52 the one call site,
L55 `subprocess.TimeoutExpired`. Exactly one exec site: `run_foreign` calls
`subprocess.run(["bash", "-c", value], cwd=scratch, env=env, stdin=DEVNULL,
capture_output=True, text=True, timeout=120)` — list argv (no `shell=True`), cwd is a
per-run `mkdtemp` under TMPDIR, child `TMPDIR` repointed into that scratch, 120 s timeout,
scratch removed in `finally`. This matches kill rule (d)'s baseline "run_foreign's single
call".

### 1.2 Patch review (.ufo/waves/round-74/w1/ExecC1Amend.patch)

7338 bytes; sha256 `f92c4b38b0d8d58462fbb7c281c64f3a597d624f9e49e0a1fdfb76028370ab55`
hashed at appearance (watcher check 15, 09:00:07Z) and re-hashed at report close —
identical (exit 0 both). Applied to a scratch copy for analysis only:

```
cp $S/orig-counter.py $S/tree/corpus/instruments/recheck-cwd-census.py   # exit 0
patch -d $S/tree -p1 --dry-run -i $W/ExecC1Amend.patch                   # exit 0 (applies clean)
patch -d $S/tree -p1 -i $W/ExecC1Amend.patch                             # exit 0
diff -u $S/orig-counter.py $S/tree/corpus/instruments/recheck-cwd-census.py | grep '^@@'
# -> exactly two hunks: @@ -20,7 +20,8 @@ (module docstring), @@ -97,38 +98,113 @@ (selftest)   # exit 0
grep -nE '<exec sweep as §1.1>' $S/tree/corpus/instruments/recheck-cwd-census.py   # exit 0, same 4-line shape (L9/29/52-53/56)
grep -c 'subprocess\.run' <amended>   # -> 1, exit 0
grep -c '"bash", "-c"' <amended>      # -> 1, exit 0
grep '^+' $W/ExecC1Amend.patch | grep -cE 'subprocess|bash|system|popen|shlex|exec|eval\(|spawn|pty'   # -> 0
```

Findings:

- **Zero new exec sites.** No added patch line even carries exec vocabulary (count 0).
  The amended file retains exactly one `subprocess.run` and one `"bash", "-c"` — the
  untouched `run_foreign`. Kill rule (d) holds. No SECURITY FINDING; L1 not messaged.
- The tempting shortcut was not taken: the new `result-main` case runs `main()`
  **in-process** (`capture(main, ["recheck-cwd-census.py", "--root", …, "--lane", …])`)
  rather than spawning `python3 … --selftest`. The `tmpdir-parent`/`scratch-cleanup`
  cases use a recording wrapper around `tempfile.mkdtemp`, restored in `finally`.
- Diff confinement proof: the only two hunks are the docstring and `selftest()`;
  `run_foreign`, `census`, and `main` are byte-untouched (124 changed lines total,
  all inside those hunks).

### 1.3 Non-blocking observations

- O1: the `tmpdir-parent` assertion tests `r["dir"].startswith(expected)`, so a TMPDIR
  *sibling* such as `"$TMPDIR-evil"` would satisfy the prefix test. Non-boundary: it is a
  selftest assertion, not a defense; allocation still goes through
  `mkdtemp(dir=TMPDIR-or-None)`. No action this round.
- O2: the selftest monkeypatch of `tempfile.mkdtemp` is process-local and restored in
  `finally` (amended L179/L183), including on exception paths. No exec surface.

## 2. Path confinement (RC-8 and fixture writes)

- `--root`/`--lane` (pre-existing behavior, confirmed unchanged): `main()` only abspaths
  `root`; `census()` globs `root/corpus/knowledge/*.md` and executes each first `recheck:`
  line via `run_foreign`. There is **no containment check** between root and lane, and the
  amendment adds none. Pointing `--root` at a foreign tree makes the instrument execute
  that tree's values — operator-chosen by construction (whoever passes `--root` chooses
  what is executed). The `startswith("cd %s && " % lane)` prefix test gates only the
  `noprefix` counter, not execution; it is a plain string compare with no security effect.
- RC-8: a recheck value such as `cd / && …` is repo-controlled text handed to `bash -c`
  with the invoking user's privileges; the child gets `TMPDIR` repointed into census
  scratch and a 120 s timeout, and nothing else restrains it. The census's own writes stay
  under TMPDIR; the executed value's writes are unbounded by design. The amendment
  **neither expands** (zero new sites, §1.2) **nor mitigates** (`run_foreign` byte-untouched,
  §1.2 hunks) this surface. claims.json notes record RC-8 as operator-pending, "routed
  around, not decided" — status confirmed: PENDING OPERATOR DECISION, unchanged.
- Fixture/write inventory on the amended file (write-path sweep, exit 0):
  `open(` L38 read-only; `mkdtemp` L47 (run_foreign, `dir=env_tmp` = TMPDIR-or-None) and
  L108 (selftest, `dir=os.environ.get("TMPDIR") or None`); `rmtree` L59, L209; selftest
  fixture writes L111 `open(..., "w")` under `kdir` under `fixture(name)` root under the
  single selftest scratch; `makedirs` L117 under the same scratch. Sweep pattern included
  `rename|shutil.(copy|move)|write_text|write_bytes|unlink|os.remove` — no matches.
  **No NEW file-writing path outside scratch.** PASS.

## 3. R-NOSECRET lens

### 3.1 Frozen disclosure S109

```
sha256sum corpus/source-snapshots/round-74/S109.txt
# -> c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486  == frozen value, exit 0
wc -l S109.txt   # -> 375 lines
```

Five pattern families (grep -niE; verbatim strings in
`SentinelCounter-lens-s109.txt`): private-key headers, `op://`,
bearer/authorization values, session-cookie shapes, plus a supplemental common-token
family (AKIA / aws_secret_access_key / gh[pousr]_ / github_pat_ / xox / AIza / x-api-key).
All five exit 1 (no match); hit file 0 lines. Lens ran on the byte-exact frozen capture.

### 3.2 Trial package (ExecTrial's output, .ufo/waves/round-74/w1/trial/)

Swept every file under `trial/` — 11 files × 5 families = 55 checks, **1 match**:

- `package/provenance.json:73` — `"method": "the claim-package-check R-NOSECRET pattern
  set (private-key header, op:// reference, bearer/authorization value, labelled
  credential, session cookie) applied to the captured evidence bytes before packaging;
  zero hits; no redaction performed"`.
- Disposition: **benign false positive** — the matched text is ExecTrial's own attestation
  quoting the pattern name itself, not a credential reference. Nothing to redact.

All other 54 checks clean (grep exit 1 each). Evidence identities: `disclosure-capture.txt`
= curl CVE-2023-38545 (SOCKS5 heap buffer overflow) project-overview capture (131 lines,
6446 B, sha256 `327bc909e01ee3dc78272c06d3d568b78e92e5b4c35c7e527394422d763b238b`);
`policy-capture.txt` = curl Vulnerability Disclosure Policy capture (221 lines, 19670 B).
Both are public documentation pages; no live-target testing involved. Note the trial's
disclosure capture is a different document from S109 (hashes differ; expected — separate
trial artifact).

### 3.3 Timing note

The `trial/package/` subtree landed mid-review (first listing showed only
`trial/evidence/`); the final sweep covers the full 11-file tree as listed in the receipt.

### 3.4 Receipts written next to this report

- `SentinelCounter-lens-s109.txt` — S109 target, patterns verbatim, 5/5 clean.
- `SentinelCounter-lens-trial.txt` — 11-file target list, patterns verbatim, 54/55 clean
  with the L73 disposition quoted.

## 4. Scratch hygiene

- Scratch root `/fast/scratch/hyaku/kasegi-r74/SentinelCounter` created 05:46 local
  (`mkdir -p`, exit 0). All analysis writes (orig/amended copies, patch tree, lens hit
  files) stayed inside it; the only wave-dir writes are this report and the two receipts.
- No tools installed (grep/patch/git/diff only); no pacman transactions; no PATH-directory
  writes; no fleet-root tracked-file writes; no mutating git/jj commands (only
  `git show` / `sha256sum` / `patch` into scratch).
- Scratch deleted before yield: `rm -rf -- $S` (exit 0), absence verified (`ls -d $S`
  fails, exit 2). Command log with per-command exits is embedded above; no checks were
  claimed without being run.

## 5. Security findings

None requiring action this round. RC-8 remains the standing operator decision (documented,
unchanged, out of this round's remediation scope per claims.json notes).
