VERDICT: BROKEN

# R45SentinelCounters: security review of the round-45 counters

Scope: `corpus/instruments/r45-routed-defects.py` (C1, sha256 82004c70…f04ee),
`corpus/instruments/r45-c2-gate.py` (C2, sha256 5e079616…30082),
`.ufo/waves/round-45/controls/freeze-controls.py` (sha256 79e45b98…7a37e),
plus the instruments they execute: `corpus/instruments/source-recheck.py` (fd2e01e8…c003) and
`corpus/instruments/r44-frontier-count.py` (bb4753a7…abd90). All read-only; `git status --short` on the three
counter files prints nothing (unchanged, not committed). Scratch was
`/fast/scratch/hyaku/kasegi-r45/R45SentinelCounters` (TMPDIR set to `$S/tmp`), removed on exit. No tools installed.
Base export: `git archive dc5bb8c6e31efc4a6650819df85e79b72fd64bcd | tar -x`, 8932 files.

Bottom line: a PASS from either counter is not evidence that the claimed defect was fixed. The counters execute
the tree's own instruments with the grader's privileges and full environment, so a tree can forge GREEN limbs
(finding 1), can forge the provenance of the S071 capture (finding 2), and can satisfy C1 R2 with paths outside
`--root` (finding 3). The frozen controls (freeze-controls, 5/5 RED) do not exercise any of these.

## Findings (severity-ranked)

### 1. HIGH: tree-controlled instruments are executed; a GREEN limb can be forged by editing them
Where: C1 `limb_r1` source-recheck run (`r45-routed-defects.py:123`), `limb_r3` r44 run (`:189`), `limb_r4`
freeze-check run (`:214`, `:219`); C2 `g4` source-recheck run (`r45-c2-gate.py:160`). All resolve
`os.path.join(root, "corpus/instruments/...")`, i.e. the candidate tree, not the tool root. The claims file confirms
the invocation shape: `claims.json:14` `python3 {tool}/corpus/instruments/r45-routed-defects.py --root {tree} --baseline {base}`.

Evidence (fixture = frozen base + lane round-45 snapshots):
- A1 genuine snapshot, real instrument: `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`
- A2 S071.txt edited (one line appended), real instrument: `gate G4 pass=0 read=recheck-rc=1 quotes-ok=0 frozen-cores-missing=0`
- A3 same edited tree, `corpus/instruments/source-recheck.py` replaced by a 6-line stub that prints `S071:sha256 OK` and five `S071:Qn OK` lines:
  `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`
- The stub ran with the grader's identity and environment (probe file written by the stub):
  `uid=1000 marker=probe-marker-7731 argv=['--manifest', '.../manifest.json', '--source', 'S071'] cwd=.../instr-fab`
  (marker = a dummy variable set on the counter's environment; it reached the tree code).
- R3: the real `r44-frontier-count.py` has no `--selftest` flag. Direct run:
  `r44-frontier-count.py: error: unrecognized arguments: --selftest --work ...` (exit 2; `--help` lists only `--root --expect --ids`).
  Real-instrument C1 run on a fixture with the R3 registry rows: `limb R3 fixed=0 read=selftest-rc=2-tokens=None`.
  Replacing the tree's `r44-frontier-count.py` with `print("selftest cases=8 failures=0")`:
  `limb R3 fixed=1 read=selftest-cases=8`.
  So R3 is unsatisfiable by the committed instrument; the only route to GREEN is editing or stubbing tree code.

Acceptability for a read-only gate: executing code from the object under test is acceptable only if the instrument
bytes come from the trusted tool root. The current design has the candidate tree choose the instrument, so a PASS
says nothing about what the instrument checked. Honest limitation to record: even after the fix below, the counters
run lane-side code over tree-supplied data; the tree still controls every data-side input.
Smallest remediation: resolve every instrument from `os.path.dirname(os.path.abspath(__file__))` (C1 and C2),
run with `[sys.executable, "-I", ...]`, and pin the instrument sha256s (or add a freeze-controls control "instrument
replaced in tree" that must be RED; A3 would currently be GREEN). R3 then needs a lane-side change that is committed.

### 2. MEDIUM: the S071 capture is not pinned; a resealed, edited snapshot passes G4
Where: `g4` (`r45-c2-gate.py:156-166`) reads `corpus/source-snapshots/round-45/manifest.json` from the tree;
`g3`/`g5` hash and read the tree's `S071.txt` (`:143`, `:174`). No counter compares S071 or S072 against the
frozen sha256 `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40` (lane `manifest.json`, S071 entry).
Evidence: I appended a sentinel line to line 1 of S071.txt and re-pinned the S071 `sha256` in the tree's manifest.json:
`gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`.
(G5 reported `F27-rows=0` only because that fixture had no F27 row.)
G3 is [INFERENCE]: it compares the tree's snapshot sha to the tree's SOURCES.md anchor (`:143-152`), so a tree that
re-pins both passes G3 too; I did not build a SOURCES.md S071 row to run it.
Honest limitation: `source-recheck.py:8-9` already says it "verifies captured bytes, not current upstream". Nothing in
the counters ties the capture to the URL or to the frozen sha; that link exists only in the lane reviewers' heads.
Remediation: compare the snapshot sha256 to constants pinned in the counter (or claims.json) before any quote check.

### 3. MEDIUM: C1 R2 accepts `enforced-by:` paths outside `--root`
Where: `limb_r2`, `r45-routed-defects.py:172-177`: `os.path.join(root, p.split(" ")[0])` with `os.path.exists`.
`os.path.join` returns an absolute `p` unchanged and does not contain `..`.
Evidence: fixture with QUALITY.md rows R47/R48/R49 citing `/etc/hostname`, `../../../../../../../../../../etc/hostname`, `/etc/passwd`
(`enforced-by:` cells, lane's grounded-in cell kept): `limb R2 fixed=1 read=criteria=3`.
Discriminator, same rows with `corpus/instruments/nothing.py` (the freeze-controls marker-only path):
`limb R2 fixed=0 read=R47-enforced-by-missing-corpus/instruments/nothing.py`.
So the marker-only control only proves "nothing.py is absent"; any existing host file satisfies R2.
Remediation: reject absolute paths and any path whose `realpath` leaves `root`; require the named file to be under
`corpus/instruments/` and to exist in the tree.

### 4. LOW-MEDIUM: reads outside `--root` via symlinks; a per-bit located-quote oracle over host files
Where: C2 `g5` opens `corpus/source-snapshots/round-45/S071.txt` directly (`r45-c2-gate.py:174`), `g3` at `:143`,
`g2`/`g5` read the entry through `corpus/knowledge/*.md` (`:125`, `:173`). `source-recheck.py:156-162` contains the
capture, but only relative to the manifest's own directory.
Evidence (fixture: S071.txt is a symlink to /etc/passwd; entry quotes `“root:x:0:0::/root:/usr/bin/bash”` and `“root:x:0:0::/root:/usr/bin/zsh”` with `(`S071.txt:1`)`):
`gate G5 pass=0 read=spans=2 located=1 failed=1 cores=0/4`
The first guess matched line 1 of the host file and the second did not. Repeating this reads the host file one guess at a time.
Containment is also inconsistent: C2 G4 with the symlinked S071.txt printed
`S071:source UNAVAILABLE reason=outside-manifest-directory` (recheck-rc=2), but G5 still read it.
The manifest directory itself may be a symlink outside the tree: with `corpus/source-snapshots/round-45` -> an external
copy of the lane snapshots, `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`.
Severity is LOW-MEDIUM because finding 1 already gives the tree code execution; it becomes an independent leak only
once instruments are pinned. Remediation: one containment helper (`realpath` under `root`, no symlinked components)
used by every read.

### 5. LOW: tree text echoed raw to the operator's terminal
`r45-routed-defects.py:176-177` prints the tree-controlled `p` unescaped. Evidence (enforced-by `/nonexistent/` + `\x1b[2J\x1b]0;SENTINEL\x07`):
`limb R2 fixed=0 read=R47-enforced-by-missing-/nonexistent/\x1b[2J\x1b]0;SENTINEL\x07` (raw ESC bytes in output).
Remediation: `repr()` or `ascii()` the echoed string.

### 6. LOW: full environment inherited by tree code
`r45-routed-defects.py:71-78` builds `env = dict(os.environ)`; `r45-c2-gate.py:77-82` calls `subprocess.run` without `env`,
so both inherit everything. The stub in finding 1 received the marker variable. Any credential in the operator's environment
reaches tree-controlled code. Remediation: pass a minimal env (PATH, LANG, TMPDIR) and `-I`.

### 7. LOW: freeze-controls writes through symlinks in a crafted base export
Where: `freeze-controls.py:21` `shutil.copytree(..., symlinks=True)` preserves symlinks; `append()` (`:24-26`) and the
`open(..., "w")` calls (`:80`, `:90`) follow them. Evidence: base copy with `SKILL.md` -> `$S/outside/SKILL.md`
(outside `--work`); after `freeze-controls.py --base-export <copy> --lane <lane> --work <work>` the target had
`first: 'outside-original'`, grew to 9 lines and contained the appended `Round-45 Gates & probes registry addition` block
(`appended block present: True`). The work dir kept the symlink.
Exposure: the frozen base has no symlinks outside `.ufo/` (`git ls-tree -r dc5bb8c6…` filtered to `120000` outside `.ufo/`: 0 lines),
so this needs a crafted `--base-export`. Remediation: `symlinks=False` (copy target content) or refuse symlinks in the base export.

### 8. LOW: quadratic-cost regex in C2 G5 (self-DoS, no gate timeout)
`r45-c2-gate.py:175` `“([^”]+)”` scans to end of file for each unmatched `“`. Wall time for an entry of n unmatched `“`:
n=5000 0.31s, n=10000 0.49s, n=20000 1.22s, n=40000 3.66s (includes ~0.25s interpreter startup; roughly quadratic).
Remediation: bound the span length (`[^”\n]{1,400}`) or split-based parsing.

### 9. LOW/INFO: TMPDIR is only nominally honoured
The counters create no temp files (no `tempfile` import in either counter; `source-recheck.py` uses `tempfile` only in
`selftest()`, `:262`). Their docstrings claim "Honors TMPDIR" (`r45-routed-defects.py:38`, `r45-c2-gate.py:29`), which is vacuous.
The one reachable temp use is the instrument's selftest, which the counters do not call. When TMPDIR is unusable it silently
falls back: with `TMPDIR=$S/does-not-exist`, `tempfile.gettempdir()` printed `/tmp` and `source-recheck.py --selftest` returned
`selftest cases=10 failures=0` (rc 0). Remediation: drop the claim or check `TMPDIR` explicitly.

### 10. INFO: C2 G7 depends on a fleet-root file outside the frozen commit
`r45-c2-gate.py:46` defaults `SOURCES_CENSUS` to `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (exists, 35466 bytes, mtime Oct 19),
run via `bash` (`:198`). Overriding it with a file containing `exit 1` gave `gate G7 pass=0 read=census-rc=1`. A tree cannot change it; the
environment can. Record as a limitation: the C2 do-nothing result depends on that file. `CENSUS` in `r45-routed-defects.py:55` is unused (dead code).

## Checked and holding
- Command/argument injection: no `shell=True`, `os.system` or `popen` in either counter or the instruments they call
  (grep over the five files returned only list-form `subprocess.run`/`Popen` lines). Every argv element is a list item;
  the `--root`-derived values passed to children are absolute (`os.path.abspath`, `os.path.join(root, ...)` with a leading `/`), so none can be read as an option.
- Path containment inside `source-recheck.py`: `load_manifest` and `check_source` use `resolve(strict=True)` plus `commonpath`
  (`:52-54`, `:156-162`). Demonstrated: `reason=outside-manifest-directory` for a symlinked snapshot (see finding 4).
- Writes by the counters: a tree with 8978 files was hashed before and after running both counters:
  `tree files: 8978 changed: 0 added: 0`. The counters write nothing.
- Frozen controls reproduce: `controls total=5 red=5 green=0` (do-nothing base C1 `fixed=0`, C2 `fixed=1/7`; junk row `4/7`; fabricated quote `5/7`).
  Limitation: none of these controls swaps an instrument, uses an absolute `enforced-by:` path, or re-pins a resealed snapshot, so findings 1-4 are all GREEN under the present control set (A3, the `/etc/hostname` R2 rows and the resealed G4 each pass).

## Recommended control additions (advice; not a predicate change)
- instrument-stub-in-tree (C1 and C2): expect RED. Currently GREEN (finding 1, A3 and B2).
- enforced-by-outside-root (C1 R2): expect RED. Currently GREEN (finding 3).
- resealed-snapshot (C2 G4): expect RED once the sha pin of finding 2 exists.

## Limitations
- Fixtures are my own, built from the frozen base plus lane round-45 snapshots; I did not run them on other hosts.
- G3 and the SOURCES.md re-pin path are [INFERENCE] from code (`r45-c2-gate.py:143-152`); not run.
- I did not build F27 or the C1 repairs (outside this item). Observation: `corpus/instruments/freeze-check.py` exists neither in the base nor in the lane (`ls`/`git ls-tree` empty), so C1 R4 reports `freeze-check-absent` on every tree.
- Attacks in findings 1-4 assume a candidate tree authored by a seat; they do not model the host-level attacker.
- I removed the scratch directory on exit; the fixtures are not kept as evidence. Commands are listed above for re-run.
