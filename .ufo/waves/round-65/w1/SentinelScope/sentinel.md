# SentinelScope — Kasegi round 65 w1 security and write-scope review

**Seat:** SentinelScope-21 (leaf; no subagent dispatch, no commits, no production edits).
**Scope:** every candidate this round proposes to land, read-only, plus the write-scope and
fail-closed behaviour of its fixtures. Reviewed at the byte level that landed.
**Verdict:** `FINDINGS` — no critical; three high (one inherited parser exec path, two in the
landed L1 driver's write-scope/provenance); the C1 predicate itself is sound and its four
positive/negative cases verify independently.

## 1. What was reviewed (sha256, observed)

| artifact | sha256 | state during review |
|---|---|---|
| `w1/ExecSignalGate/figure-audit.py` (candidate) | `86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef` | landed byte-identical as `corpus/instruments/figure-audit.py` (commit `1c36d72`) |
| `w1/ExecSignalProbes/c1-signal-probes.py` | `855af8dfca4c4fe48bd7eda93705789cff46aa00c25760f03fb66bca81a3adf2` | matches frozen copy `c1-signal-probes-r65.py` and claims pin |
| `w1/ExecSignalMutants/signal-mutbat.py` (final bytes) | `5050d853523d396aff7bb31004883d08e86a8fc9d66748a76bae2bc7ba0d47aa` | matches frozen copy `signal-mutbat-r65.py` and claims pin; receipts (16:31:32) post-date script (16:31:03) |
| `w1/ExecDriver/verify-r65.py` (seat deliverable) | `064404510b71825016b71a8db0d7a341ee17e6317cc5758ac0a3b9c89d754a60` | **not** the landed driver |
| `.ufo/waves/round-65/verify-r65.py` (landed driver, L1) | `5aa842abdceac676ff8c0a1b90f641bbad93a9505161f192dde85b1a1d06aaaf` | frozen `driver_sha256` is `533a6d4f…` (superseded by erratum 1); same bytes at `a333d8e` and at final HEAD `2f6017f` |
| base gate at `a283189` (extracted with `git show`) | `8d92eaa0a1f248eb1fb8ae4d0d098c2a11d8d0674fa1eff6cefdb771e2e917e9` | base state used for all "before" claims |

The lane moved during the review: HEAD was `a283189` at start; L1 landed `1c36d72` (gate ->
`86becbde`, F44/S098 content), froze at `57cb8dec`, committed the driver erratum as
`a333d8e`, and closed with `2f6017f`. All reviewed hashes above were re-checked at `2f6017f`
and are unchanged. That is the L1 integrator's authority. At handoff the worktree also showed
integration edits by L1 (`SCORECARD.md`, `corpus/lessons/round-65.md`, `SKILL.md`,
`w1/ReviewC2Base/*`); none was written by this seat. **This seat edited no production
file**; its only writes are `.ufo/waves/round-65/w1/SentinelScope/*` and this report
(untracked).

## 2. Per-script security table

| script | writes outside declared work dir? | executes untrusted input? | credentials / env secrets? | lane files at import/run? | verdict |
|---|---|---|---|---|---|
| gate `86becbde` | No. Selftest fixtures only under `$HYAKU_SCRATCH` else system temp (`figure-audit.py:363`), removed by `rmtree` of its own `mkdtemp` (`:410`). | Ledger `derive` is validated argv, no shell. **But the allow-list admits exec/write flags** (`sort --compress-program`, `-T`; `git cat-file --filters`) — S-01. | None. | None at import or run. | FINDINGS (S-01 inherited; no C1-introduced defect) |
| probe collector `855af8` | Only under `--work`, but **`--work` is unguarded** (`:275`; writes `:149,:155,:161`) — S-04. Receipts use a `--work` inside the lane artifact tree (S-10). | Executes `--instrument` by design; probe pipelines are self-authored argv, no shell. | None (no `os.environ` reads). | None at import; run-time only under `--work`. | FINDINGS (S-04, S-09, S-10) |
| mutant battery `5050d85` | Only under `--work`, but **unguarded**, and it `rmtree`s `work/fixture` (`:144,:198-199`) — S-05. | Executes the instrument and single-site-derived mutants, `timeout=180`, no shell. | None. | None at import; run-time only under `--work`. | FINDINGS (S-05) |
| w1 driver `0644045` | No. `--work` must be under `/fast/scratch/hyaku/kasegi-r65` and depth ≥ 2 (`:106-107`); tempdir inside it. | Runs committed/candidate scripts by design; **full ambient env passed** (`:191`) — S-06. | No reads; child env inheritance (S-06). | None at import; only under `--work` (tar/symlink caveat S-11). | FINDINGS (S-06, S-11) |
| landed driver `5aa842ab` | **No guard**: `--work` is `abspath` + `makedirs` (`:122,:137-140`), then `git clone --shared` + `git checkout --force` into it (`:82,:95`) — S-02. | Runs **worktree** collector/battery/candidate/pins, not revision bytes — S-03. | No reads; full ambient env, no timeout (`:59-60`) — S-08. | None at import; run-time under `--work`, but `--work .` from the lane writes the lane (S-02). | FINDINGS (S-02, S-03, S-07, S-08, S-12, S-13, S-14) |

No script contains `shell=True`, `os.system`, `eval`/`exec`, network calls, credential-file
reads, or import-time side effects (scanner receipt `08-scan.txt`; the single scanner hit,
gate `:215` "tokens" in a docstring, is a false positive).

## 3. Findings

### High

**S-01 — ledger `derive` can execute an arbitrary configured program through an allow-listed head.**
`corpus/instruments/figure-audit.py:67-73` (`DENIED_FLAGS`), `:216-245` (`denied_flag`, `segment_ok`).
The comment claims flags that "write a file or execute a configured command" are refused, but only
`sort -o/--output` and `git show --output/--ext-diff` are listed. `sort -S 1K
--compress-program=<path>` and `sort -T <dir>` are admitted and executed. Reproduced end-to-end
with a scratch ledger: the gate exited 0 and ran the named script ~60,950 times
(receipt `07-parser-sort-compress-exec.txt`; `sort --compress-program` invokes the program on
every spill). `git cat-file --filters/--textconv` and `git show --textconv` are likewise admitted
and execute configured filters. The module docstring does say "NOT a sandbox", but the
deny-list comment asserts the opposite for this class, and a foreign ledger is exactly the
untrusted input the parser is supposed to contain.
*One-line fix:* extend `DENIED_FLAGS` with `("sort", ("--compress-program", "-T",
"--temporary-directory"))` and `("git cat-file", ("--filters", "--textconv"))`,
`("git show", (..., "--textconv"))`, or reject every flag not explicitly allow-listed.
*Classification: pre-existing, inherited by the landed gate; the C1 diff does not touch it.*

**S-02 — landed driver has no `--work` ownership guard; `--work .` writes a clone and receipts into the lane.**
`.ufo/waves/round-65/verify-r65.py:122-126,:137-140` (`os.path.abspath` + `makedirs`), `:82`
(`git clone --shared <lane> <work>/repo`), `:95` (`git checkout -q --force`), `:141-143`
(receipts). From the lane root, `--work .` (or any lane path) creates a nested Git repo, checks
out the measured tree into it, and writes `receipts/` inside the protected tree. The seat's own
driver has exactly this guard (`w1/ExecDriver/verify-r65.py:106-107`, verified: `/tmp` and a
lane path both exit 2 `work-not-owned`). I did not execute the lane-path case on the landed
driver (it would write); the absence of any `WORK_FLOOR`/`is_relative_to` check is the finding.
*One-line fix:* port the w1 guard (`work.is_relative_to("/fast/scratch/hyaku/kasegi-r65")` and
depth ≥ 2) before `makedirs`/`export_tree`.

**S-03 — landed driver reads the round's scripts and pins from the mutable worktree, not from `--revision`, and never verifies its own bytes.**
`.ufo/waves/round-65/verify-r65.py:41-44` (`WAVE` paths for collector/mutbat/candidate/claims),
`:118`, `:237-247` (measurement 8 pins and `seen` hashes all from the worktree), `:51-57`
(`sha256` of worktree files). `driver_sha256` in `claims.json` is never checked against the
running driver. Evidence: the "final" receipt at revision `1c36d72` prints driver
`5aa842ab…`, while `1c36d72` contains `533a6d4f…`; erratum 1 explicitly supersedes the pin with
a byte string rather than a revision. A post-freeze edit of `c1-signal-probes-r65.py` +
`claims.json` (neither is pinned by anything the driver reads from the revision) passes all eight
measurements. My own `--final` run at `a333d8e` is 8/0 (receipt `10-l1-driver-final.txt`) and
shows the same property.
*One-line fix:* read `COLLECTOR`, `MUTBAT`, `CANDIDATE_FROZEN`, `CLAIMS` and the pins via
`git show <revision>:<path>` (or export them with the archive), and compare
`sha256(Path(__file__))` with `claims.json.driver_sha256` before measuring.

### Medium

**S-04 — probe collector has no work-dir guard.**
`w1/ExecSignalProbes/c1-signal-probes.py:275` (`work = os.path.abspath(args.work)`), writes at
`:149` (`os.makedirs(root/corpus/instruments)`), `:155` (`g.txt`), `:161-167` (ledgers), `:285`
(selfcheck stub). `--work <lane>` creates `g.txt` and `corpus/instruments/{kill,sigkill,
bigwriter}.py` in the lane; pointed at `corpus/instruments` it creates helper scripts in the
production instrument directory. r64's collector enforced a scratch prefix and depth.
*One-line fix:* require `work` under `/fast/scratch/hyaku/kasegi-r65` with ≥ 2 relative parts
before any write.

**S-05 — mutant battery has no work-dir guard and rmtrees a derived path.**
`w1/ExecSignalMutants/signal-mutbat.py:198-199` (`abspath` + `makedirs`), `:144`
(`shutil.rmtree(work/fixture)`), `:149-157` (fixtures/ledger), `:249,:279` (mutant copies).
`--work <lane>` removes `<lane>/fixture` and creates fixtures, `base/`, `mut/` in the lane.
*One-line fix:* same ownership guard before `makedirs`/`rmtree`.

**S-06 — w1 driver passes the full ambient environment to every child.**
`w1/ExecDriver/verify-r65.py:191` (`env = dict(os.environ, ...)`). The candidate instrument is
by definition the object under audit; giving it the operator's full environment exposes any
exported tokens/keys it cares to read. The driver's own docstring says "not a sandbox", but the
environment is separable from sandboxing.
*One-line fix:* build the child env from an allow-list (`PATH`, `LANG`, `LC_ALL`, `TMPDIR`,
`HYAKU_SCRATCH`, `PYTHONDONTWRITEBYTECODE`, `GIT_*`).

**S-07 — landed driver's eight measurements are not the wave's enumerated eight.**
`.ufo/waves/round-65/verify-r65.py:178-233,:255` implements `probes-base`,
`probes-candidate`, `selftest`, `mutbat-candidate`, `mutbat-base-limb-absent`, `real-ledger`,
`collector-selfcheck`, `input-hashes`. The wave contract names `collector-base`,
`candidate-collector`, `collector-selfcheck`, `selftest`, `old-mutbat`,
`signal-mutbat-and-equivalents`, `collector-forgeries`, `real-ledger`. `old-mutbat` (the
pre-existing five-mutant regression) and `collector-forgeries` (forged-receipt and
always-green counterfeit rejection) are absent, and the frozen after-state receipt therefore
does not include them; the seat driver `0644045` does implement both.
*One-line fix:* add the two missing measurements or freeze the seat driver's measurement set.

**S-08 — landed driver's `run()` has no timeout, no temp isolation, and inherits the full env.**
`.ufo/waves/round-65/verify-r65.py:59-60`: `subprocess.run(argv, cwd=cwd, ...)` with default
`env` and no `timeout`; nothing sets `TMPDIR`/`HYAKU_SCRATCH`, so the gate's `--selftest`
fixtures land in the system temp directory rather than `--work`, and a hung instrument hangs the
final verification. The w1 driver sets `TMPDIR`/`HYAKU_SCRATCH` under `--work` and uses
`timeout=600`.
*One-line fix:* allow-listed env + `TMPDIR`/`HYAKU_SCRATCH` under `--work` + `timeout=`.

### Low

**S-09 — probe collector's native replay has no timeout/cleanup.**
`c1-signal-probes.py:188-205`: `procs[-1].communicate()` and `p.wait()` without timeout; an
exception during setup leaks children.
*One-line fix:* `communicate(timeout=60)` / `wait(timeout=60)` with kill-and-wait in `finally`.

**S-10 — probe fixtures live inside the lane artifact tree, not the mandated scratch.**
Receipts (`probes-base.txt` header) show `root=<lane>/.ufo/waves/round-65/w1/
ExecSignalProbes/work/root`; the wave rule is scratch exactly
`/fast/scratch/hyaku/kasegi-r65/<seat>/`. Re-running the collector mutates the lane working
tree and leaves helper `.py` files untracked there.
*One-line fix:* run with `--work /fast/scratch/hyaku/kasegi-r65/ExecSignalProbes/work`; keep
only receipts in the lane.

**S-11 — w1 driver's tar extraction followed by `write_bytes` is symlink-unsafe.**
`w1/ExecDriver/verify-r65.py:174` (`tar -xf`), `:180` (`instrument.write_bytes(candidate)`),
`:188` (`(root/".git").write_text`). GNU tar blocks `..` members, but a committed symlink at
`corpus/instruments/figure-audit.py` (or `.git`) makes the later write follow the link outside
`root`; the candidate bytes then land at the link target.
*One-line fix:* extract with a Python tar filter rejecting symlinks/absolute names, or `lstat`
+ `unlink` each target before writing.

**S-12 — landed driver refuses `--final --candidate` as a measurement failure, not a setup error.**
`.ufo/waves/round-65/verify-r65.py:132-134` prints `RESULT construction-override FAIL` and
`VERIFY … failures=1`, exit 1; r64's driver (and the seat driver) raise `ValueError` -> exit 2.
*One-line fix:* `raise SystemExit("verify-r65: final-refuses-construction-override")` (exit 2).

**S-13 — landed driver's `--print-inputs` performs the clone and force checkout.**
`.ufo/waves/round-65/verify-r65.py:122-126` calls `export_tree` (clone + `checkout --force`)
before printing hashes; combined with S-02, a lane `--work` makes a "print" mode write the lane.
*One-line fix:* read inputs with `git show <revision>:<path>` in print mode, or apply the S-02
guard first.

**S-14 — landed driver has no structural candidate-absent fail-closed branch.**
Without `--candidate`/`--final` it runs the tree's gate as the instrument; at the base revision
that fails 3/8 (`probes-candidate`, `selftest`, `mutbat-candidate`; receipt
`controls/driver-base-donothing-finaldrv-r65.txt`), so no silent pass was observed, but a
limb-bearing tree in this mode passes all eight without `--final`. The seat driver fails
`selftest`/`signal-mutbat-and-equivalents` closed explicitly (`candidate-overlay-absent`,
verified: 6 failures, exit 1).
*One-line fix:* add the explicit `if not args.candidate and not args.final: conclude(..., False,
"candidate-overlay-absent")` branches used by the seat driver.

### Info

**S-15 — gate selftest temp fallback.** `figure-audit.py:363` uses `$HYAKU_SCRATCH` else the
system temp directory; `:410` removes only its own `mkdtemp`. Inherited; the driver pins both
`TMPDIR` and `HYAKU_SCRATCH` under `--work` (w1 driver) but the landed driver does not (S-08).

**S-16 — `signal.SIGPIPE` is POSIX-only.** `figure-audit.py:90`; on a non-POSIX host the lookup
raises and the instrument exits nonzero (fail-closed). No action on this Linux lane.

**S-17 — w1 driver imports the collector in-process.** `verify-r65.py:327-329`
(`importlib` + `exec_module`) for the forgery measurement. Trust boundary is the committed tree;
the collector's module top level is constants only.

**S-18 — landed driver compares the invalid-control count as a string.**
`.ufo/waves/round-65/verify-r65.py:209` (`m.group(6) >= "1"`); correct for "1", wrong ordering
for multi-digit values. Use `int(m.group(6)) >= 1`.

**S-19 — landed receipt's driver bytes vs measured revision.** The 8/0 receipt at `1c36d72`
prints driver `5aa842ab`; that revision contains `533a6d4f`. Erratum 1 documents the
supersession, but the receipt itself does not name the driver's revision (S-03 root cause).

## 4. Probe fixtures and fail-closed checks (explicit)

- **Helper containment — PASS.** `build_fixtures` writes only
  `<work>/root/g.txt` and `<work>/root/corpus/instruments/{kill,sigkill,bigwriter}.py`;
  the observed tree contains exactly `work/root/...`, `work/ledgers/P1..P6.json`,
  `work/stub-figure-audit.py`. No `/tmp` literal and no absolute-path literal in the collector
  (scan receipt `08-scan.txt`). Caveat S-10: that `work` is inside the lane artifact dir.
- **Signals are real, not simulated — PASS.** Receipts print `NATIVE P1 stage=0 rc=-15`,
  `P2 stage=0 rc=-9`, `P3 stage=1 rc=-15`, `P4 stage=0 rc=-13`, `P6 stage=0 rc=1`; my
  independent oracle reproduces the same stage statuses and the candidate reasons
  `derive-upstream-signal-15`, `derive-upstream-signal-9`, `derive-signal-15`, with
  P4/P5/P6 ok (`02-oracle-candidate.txt`). `bigwriter` correctly resets `SIGPIPE` to `SIG_DFL`;
  without that Python would exit 1/120 and the benign-SIGPIPE limb would be untested.
- **Base false green — PASS.** On base gate `8d92eaa0`, P1/P2 are `ok` (swallowed signals),
  P3 is `stale reason=derive-exit--15` (the malformed label), P4/P5/P6 ok
  (`03-oracle-base.txt`). The collector's assigned base model expects all six ok, so its base
  run is `PROBES probes=6 failures=1` exit 1 (`04-collector-base.txt`); the landed driver pins
  exactly that (`PROBES_BASE_SUMMARY`, `verify-r65.py:44`) and checks the P3 line separately.
- **Fail-closed without a candidate — PASS (w1 driver) / PASS-in-effect (landed driver).**
  w1 driver, no `--candidate`: `RESULT selftest FAIL candidate-overlay-absent`,
  `RESULT signal-mutbat-and-equivalents FAIL candidate-overlay-absent`,
  `VERIFY measurements=8 failures=6`, exit 1 (`05-driver-w1-failclosed.txt`). Guards:
  `--final --candidate` and `--work /tmp|/<lane>` all exit 2
  (`06-driver-w1-guards.txt`). Landed driver at base: 3 failures, exit 1, no silent pass
  (L1 receipt), but no explicit branch (S-14).
- **Convergence of the reviewed bytes — PASS.** Landed production gate `86becbde` =
  candidate; landed collector `855af8` and battery `5050d85` = frozen copies = claims pins;
  my `--selftest` on the landed gate is `cases=63 failures=0` exit 0 with no leftovers in
  `HYAKU_SCRATCH` (`01-gate-selftest.txt`); the landed driver's `--final` at `a333d8e` is
  8/0 exit 0 (`10-l1-driver-final.txt`).

## 5. Severity counts

FINDINGS critical=0 high=3 medium=5 low=6 info=5

**Verdict: FINDINGS.** No critical. The three highs are (S-01) an inherited, reproducible
configured-program execution path through a ledger `derive`, and (S-02/S-03) the landed L1
driver's missing `--work` guard and worktree-only provenance (with the erratum making the frozen
`driver_sha256` unenforced). None is introduced by the C1 signal diff itself: the landed gate
is byte-identical to the reviewed candidate, fails closed on SIGTERM/SIGKILL/SIGPIPE exactly as
specified, and its fail-closed probe set is independently reproduced.

## 6. Commands actually run (abbreviated; full receipts in `w1/SentinelScope/`)

- `git -C <lane> show a283189:corpus/instruments/figure-audit.py > <scratch>/base-gate-a283189.py`
- `HYAKU_SCRATCH=<scratch>/hk python3 -B <lane>/corpus/instruments/figure-audit.py --selftest`
- `python3 <scratch>/oracle.py --instrument <candidate|base-gate> --work <scratch>/fix-* --label *`
- `python3 -B <collector> --instrument <base-gate> --work <scratch>/cb-base2 --mode base`
- `python3 -B <w1 driver> --revision a283189… --work <scratch>/driver-final` (and `--candidate`,
  `--final --candidate`, `/tmp` and lane `--work` guard probes)
- `python3 -B <landed driver> --revision a333d8e… --work <scratch>/l1-final --final`
- `python3 -B <landed gate> --ledger <scratch>/parse-gap/p-compress.json --root <scratch>/parse-gap`
  (`sort -S 1K --compress-program=corpus/instruments/mark.sh …`; marker script invoked)
- `python3 <scratch>/scan.py <five scripts>` (AST scan for writes, shell, env, import-time I/O)
