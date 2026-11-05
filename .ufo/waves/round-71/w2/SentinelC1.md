# SentinelC1 — round-71 attempt 2: what the derive gate still lets a hostile derive do

Seat: sentinel (leaf, no dispatch). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, tip
`3cc8cd45cb6f8ca49a292f3b2647c5bddac71486`. Reviewed gate `corpus/instruments/figure-audit.py`
sha256 `182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603` (matches the frozen
C1 gate pin). Comparison gate: `git show 39cde8a:corpus/instruments/figure-audit.py` sha256
`7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5` (the round-70 bytes = r71
base, matching the do-nothing gate hash pinned in `claims.json` and the gate behind
`controls/c1-donothing-r71.txt`).
Host toolchain used by the gate's own `subprocess` resolution: python 3.14.8, GNU sort 9.12
(`python3 -c 'subprocess.run(["sort","--version"])'` → `sort (GNU coreutils) 9.12`; this shell also
has a bash builtin `sort` from uutils 0.8.0, which the gate never uses because it `execvp`s), git
2.56.0. No tool installs were needed.

## 1. Trust boundary

Decision point: `parse_derive(root, cmd)` → `tokenize` → per-stage `segment_ok` →
`python_head_ok`/`python_flags_ok`/`denied_flag`/`git_show_operands_ok`. It returns a plan of argv
lists. `run_derive(plan, root)` then `subprocess.Popen(argv, cwd=root, stdin=…, stdout=PIPE,
stderr=tempfile)` — no shell, same decoded argv, 300 s deadline, **first stage's stdin is the gate's
own stdin** (`stdin = None` unless `<` was parsed).

So the boundary is: *a lexical admission filter over the derive string*, then the program runs with
the gate's uid, cwd=root, PATH, environment and stdin. The gate sees argv tokens only. It does not
see file contents the program will read, the program's own option semantics beyond a hand-kept deny
table, absolute paths, the environment, PATH, stdin, or the program's children. Every residual below
is a consequence of that: the filter's knowledge is (a) a per-head name table, (b) a per-head option
name list, (c) a `--` separator model that only argparse honours.

Tokenizer/segment boundary, measured separately (candidate gate, one figure each):
`cat corpus/SOURCES.md; sh -c id` REFUSED rc 2, `cat corpus/SOURCES.md | sh` REFUSED rc 2,
`cat corpus/SOURCES.md > <abs>` REFUSED rc 2, `cat $HOME/…` REFUSED rc 2, ``cat `id` `` REFUSED rc 2,
`cat corpus/*.md` REFUSED rc 2, `cat ~/corpus/SOURCES.md` REFUSED rc 2 — all with
`reason=derive-not-read-only`. Controls admitted: `cat corpus/SOURCES.md && cat corpus/SOURCES.md |
wc -l` rc 1, and `cat < corpus/SOURCES.md | wc -l` rc 1 with `derived=262`. Also refused in the table
below: `python3 -m <module>`, `env VAR=x cmd`, git with a `-c` first option,
`--compress-program`/`--co`, `--output`/`--out`/`--selftest` before any `--`, and symlinks whose
realpath leaves `corpus/instruments/`.

## 2. Method

Shared clone at `$S/lane` (`git clone --no-hardlinks`, tip = the measured revision, `figure-audit.py`
sha256 re-verified in the clone). Harness `$S/probe.py`: for each attempt it writes a **minimal
ledger with exactly one figure** whose `derive` is the tested string, snapshots the clone tree
(relpath→sha256), runs
`python3 <gate> --ledger <ledger> --root <clone>` with `TMPDIR`/`HYAKU_SCRATCH` in scratch, then
records rc, the `FIG` line, the refusal line, every tree delta inside the root, and the recursive
listing (size-tagged) of watch dirs outside the root. Rows that write outside the root were run
under `strace -f -qq -e trace=execve,openat,unlink,unlinkat`. Every row was run twice: candidate gate,
then the round-70 gate (`$S/base70.py`), same ledger shape, same root. `ADMITTED` = the gate did not
refuse (rc ≠ 2 / no `derive-not-read-only`); `REFUSED` = rc 2 with that stderr line.

Scratch was `/fast/scratch/hyaku/kasegi-r71/SentinelC1/` and is deleted at hand-off; no citable
receipt was written under `/tmp` (the one `/tmp` row below creates sort temp files that GNU sort
unlinks itself, measured by strace).

## 3. Attempt table

`C` = candidate (r71), `B` = round-70 gate. `obs` = what the gate-run process actually did.

| # | derive (abbreviated) | C | rc | stderr | obs | B | class |
|---|---|---|---|---|---|---|---|
| 1 | `…capture-source.py -- <abs>/out/a1.txt` | ADMITTED | 1 | — | script `exit 2`; `out/a1.txt` absent | ADMITTED | old, inert |
| 2 | `…capture-source.py --ur file://…/secret.txt` | REFUSED | 2 | `UNAVAILABLE reason=derive-not-read-only id=b1-…` | nothing | REFUSED | holds |
| 3 | `…capture-source.py -u file://…/secret.txt` | ADMITTED | 1 | — | script `exit 2` (argparse: unknown `-u`), no fetch | ADMITTED | old, inert |
| 4 | `…capture-source.py –url file://…/secret.txt` (U+2013) | ADMITTED | 1 | — | script `exit 2`, no fetch | ADMITTED | old, inert |
| 5 | `…capture-source.py --id=x --url=… --out=…` | REFUSED | 2 | `…derive-not-read-only id=b4-…` | nothing | REFUSED | holds |
| 6 | `python3 -m http.server 8791` | REFUSED | 2 | `…derive-not-read-only id=c1-…` | nothing | REFUSED | holds |
| 7 | `python3 -m json.tool corpus/SOURCES.md` | REFUSED | 2 | `…derive-not-read-only id=c2-…` | nothing | REFUSED | holds |
| 8 | `…/ok.py` → symlink to `$S/outside-evil.py` | REFUSED | 2 | `…derive-not-read-only id=d1-…` | marker `mark/evil.mark` = 0 bytes | REFUSED | holds |
| 9 | same symlink + `--url … --out …/out/d2.txt` | REFUSED | 2 | `…id=d2-…` | no file, no marker | REFUSED | holds |
| 10 | `…/censusf.py` → symlink to `capture-source.py` | REFUSED | 2 | `…id=d3-…` | nothing (census fail-closed) | REFUSED | holds |
| 11 | `…figure-audit.py --selftest` | REFUSED | 2 | `…id=e1-selftest-direct` | nothing | **ADMITTED**, rc 1 | r71 fix |
| 12 | `…figure-audit.py -- --selftest` | ADMITTED | 1 | — | **ran the gate's own 106-case selftest**: stdout ends `selftest cases=106 failures=0 want=35 stale` | ADMITTED | old |
| 13 | `env PYTHONPATH=/x python3 …gate-quote-audit.py --root .` | REFUSED | 2 | `…id=f-env-pythonpath` | nothing | REFUSED | holds |
| 14 | `sort -T <abs td1> -S 1K < big.txt` | ADMITTED | 1 | — | **51,200** `openat(…/td1/sortXXXXXX, O_RDWR\|O_CREAT\|O_EXCL)` and 25,600 unlinks in strace | ADMITTED | old |
| 15 | `sort -T /tmp -S 1M < big.txt` (the literal spelling asked for) | ADMITTED | 1 | — | 46 `O_CREAT` opens in `/tmp` (`openat("/tmp/sortwqmXcK", O_CREAT…)`) and 23 unlinks | ADMITTED | old |
| 16 | `sort --compress-program=sh < big.txt` | REFUSED | 2 | `…id=g2-…` | nothing | REFUSED | holds |
| 17 | `sort --co=sh < big.txt` | REFUSED | 2 | `…id=g3-…` | nothing | REFUSED | holds |
| 18 | `sort --temporary-directory=<abs td2> -S 1K < big.txt` | ADMITTED | 1 | — | 51,200 `O_CREAT` opens in td2 (same class, different name) | ADMITTED | old |
| 19 | `git -c core.pager=sh show HEAD:corpus/SOURCES.md` | REFUSED | 2 | `…id=h-…` | nothing | REFUSED | holds |
| 20 | `…capture-binding-check.py --root .` | ADMITTED | 1 | — | ran, printed manifest counters (rc 1 only because `want` was the probe sentinel) | **REFUSED** | intended fix |
| 21 | `…claim-package-check.py …/exemplar --json` | ADMITTED | 1 | — | JSON on stdout (`{"exit": 0, "fail": 0, …}`) | **REFUSED** | intended fix |
| 22 | `…r47-f30-gate.py --root . --work <abs w2>` | ADMITTED | 1 | — | `derive-exit-1`; w2 still empty (head failed early) | **REFUSED** | **new** |
| 23 | `…r47-counters-selftest.py --base . --work <abs w3> --counter c1` | ADMITTED | 1 | — | **22,012 files written under `--work`** (a copy of the base tree incl. `.git`: 7,855 loose objects, `refs/heads/*` = `3cc8cd45…`); child `execve`: the derive itself | **REFUSED** | **new** |
| 24 | `cat <abs>/out/secret.txt` | ADMITTED | 1 | — | `FIG … derived=SECRET-STDIN-TOKEN-9f3a` (arbitrary read outside root, exfiltrated into the FIG line) | ADMITTED | old |
| 25 | `cat` (no operands) with a secret on the **gate's** stdin | ADMITTED | 1 | — | `FIG … derived=SECRET-STDIN-TOKEN-9f3a` (first stage inherits the gate's stdin) | ADMITTED | old |
| 26 | `…claim-package-check.py <dir> -- --selftest` | ADMITTED | 1 | — | `selftest: unknown argument '--'` exit 2 (inert) | ADMITTED | old, inert |
| 27 | `…claim-package-check.py -- --selftest` | ADMITTED | 1 | — | same, exit 2 (inert; the `--` reaches its dispatcher) | ADMITTED | old, inert |
| 28 | `…/ok.py` → symlink to `gate-quote-audit.py`, `--json <abs>/out/alias.json` | ADMITTED | 1 | — | **wrote `out/alias.json` (2,595 bytes)** — the per-script `--json` denial is gone under the alias | **REFUSED** | **new** |
| 29 | same alias, `--url file://…/secret.txt` | ADMITTED | 1 | — | script `exit 2` (no `--out`), no fetch | **REFUSED** | **new**, inert |
| 30 | `…gate-quote-audit.py --json <abs>/out/direct.json` (correct spelling) | REFUSED | 2 | `…id=o3-…` | no file | REFUSED | holds |
| 31 | `python3 -B …capture-binding-check.py --root .` | REFUSED | 2 | `…id=p1-…` | nothing | REFUSED | old, over-refusal |
| 32 | `…figure-audit.py -- --ledger <evil> --root .` (nested gate) | ADMITTED | 1 | — | `derive-exit-1`, no tree delta; the inner ledger is filtered by the same policy, so this adds no refused spelling (analysis, not a measured bypass) | ADMITTED | old |
| 33 | `…freeze-check.py --claims <abs>/claims-evil.json --tool-root <dir> --base <dir>` | ADMITTED | 1 | — | **`bash -c` executed the claims file's `counter_cmd`**: `mark/freeze.mark` = `pwned-from-claims` | ADMITTED (also without `--work`) | old, **critical** |

Row 33 on the round-70 gate, for the class: with `--work` → rc 2 `derive-not-read-only` (base denied
`--work` globally); **without** `--work` → rc 1, no refusal, marker written. So the shell-exec
capability is old and independent of row 23's regression.

## 4. REGRESSIONS=2

Both are consequences of the R71 mechanism (per-script option table + basename census), both
measured as refused-at-base70 → admitted-and-effective-at-candidate.

**R1 — `--work`/`--root`/`--scratch` are no longer refused globally, and the per-script table only
covers ten heads.** Base70 refused those three names for *every* head; candidate refuses them only
where `PY_DENIED_BY_SCRIPT` names the head. Static census of the census: **23 heads** re-admit at
least one base-denied flag (`capture-binding-check, citation-ground-check, freeze-check,
gate-quote-audit, kill-rule-check, r44-frontier-count, r44-routed-defects, r45-c2-gate,
r45-counters-selftest-c1, r45-routed-defects, r46-c1-gate, r46-c2-gate, r46-counters-selftest-c1,
r46-f29-gate, r46-landing-gate, r46-mutbat, r46-selftest-f29, r47-counters-selftest, r47-f30-gate,
r47-mutbat, r47-routed-defects, score-gap, shonen-shipped-fixture-check`). Measured effect: row 23
wrote 22,012 files to a directory of the ledger author's choosing (a byte copy of the lane,
including `.git`), rc 1, no refusal; base70 refused the same ledger with rc 2. `--work` is a write
root and, in `r46-mutbat`/`r47-mutbat`/`r47-counters-selftest`/`freeze-check`, a child-process
scratch root.

**R2 — the census is keyed on basename while containment is keyed on realpath, so an in-dir alias
under a `PY_SELFTEST_FIXTURE_HEADS` name restores the denied flags of the file it points at.**
Measured: `ok.py → gate-quote-audit.py`, derive `python3 corpus/instruments/ok.py --json
<abs>/out/alias.json` → candidate ADMITTED and wrote 2,595 bytes (row 28); base70 REFUSED
(`--json` was global). The fixture-name allowance exists because the gate's own `selftest()` writes
`ok.py/fail.py/exit1.py/kill.py/kill9.py/pipe.py/grep.py/link.py` into a temp root and runs the same
`parse_derive`; it is not scoped to that run. Prerequisite: create one file inside
`corpus/instruments/`. Note this is not only a symlink trick: any file with one of those eight names
is admitted with `denied = PY_DENIED_ANY` only.

## 5. Residuals, severity ordered

1. **CRITICAL (old) — an admitted head that runs its own data is a general `bash -c` primitive.**
   `freeze-check.py` is admitted with no denied option; `--claims PATH` supplies `counter_cmd`
   strings that the head renders and runs as `bash -c` in `--tool-root` (source line 73). Measured:
   row 33, marker written, rc 1, base70 admits it too (without `--work`). The derive string is
   innocuous — the payload is a JSON file the gate never opens. Exploit path: ledger figure 1's
   `derive` = `python3 corpus/instruments/freeze-check.py --claims <any attacker-authored json>
   --tool-root <dir> --base <dir>`; the author of a wave ledger normally also commits files, so
   "attacker-authored json" is not a barrier. Smallest remediation: add `freeze-check.py` to
   `PY_HEAD_REFUSED` (it has no read-only invocation) — it belongs there exactly as
   `frontier-recheck-count.py` does; `r46-c1-gate.py`'s `bash -c` on ledger commands (line 243) and
   `limb-mutation-check.py`'s `bash -c` (line 295) need the same audit before the census can claim
   fail-closed.
2. **HIGH (old) — `PY_DENIED_ANY` is unenforceable for heads that hand-parse argv.** `python_flags_ok`
   returns `True` at the first `--`, and the `--` is then dropped/misread by hand parsers.
   Measured: row 12 — `figure-audit.py -- --selftest` is admitted and the gate's own 106-case
   selftest runs (its stdout becomes the derived value); row 11 shows the same flag refused when
   spelled directly, so the denial is advisory. `claim-package-check.py -- --selftest` is inert only
   because its dispatcher rejects the leftover `--` (rows 26-27). Smallest remediation: refuse any
   `--` token in the python head's argv when the target is not argparse-verified — none of R1-R8
   needs one — or drop the early return and treat post-`--` tokens as operands for the deny check.
3. **MEDIUM-HIGH (new, R1) — arbitrary tree write via `--work`/`--root`** on 23 heads; measured
   22,012 files (row 23), including a copy of the lane's `.git`. Impact: write-amplification and
   disclosure (the lane's bytes land where the ledger author points) without any exec class.
   Smallest remediation: make the denied set a *union of base's global list minus an explicit
   per-head allowlist* — i.e. invert the table: deny `--work/--root/--scratch/--json/--url` unless
   the head is proven read-only for that flag (that is what R1-R8 actually exercise).
4. **MEDIUM (old, R2) — alias restores a denied flag** (row 28), and `--url` ingress is restored
   for capture-source-under-alias (row 29; one `--out` away, which `PY_DENIED_ANY` still denies).
   Requires one file inside `corpus/instruments/`. Smallest remediation: apply
   `PY_DENIED_BY_SCRIPT[basename(realpath(target))]` instead of the invoked basename, and scope
   `PY_SELFTEST_FIXTURE_HEADS` to `selftest()` (pass an explicit flag or check the root is the
   scratch temp root).
5. **MEDIUM (old) — `sort -T` / `--temporary-directory` write outside the root.** Rows 14/15/18:
   51,200 (and 46) `O_CREAT|O_EXCL` opens plus 25,600 (and 23) unlinks in a caller-chosen
   directory. The deny list names
   `-o`/`--output`/`--compress-program` only, so the temp-root redirection is a different name for
   the same write class. Impact: bounded file creation/removal (GNU sort unlinks its spills), no
   exec. Smallest remediation: add `-T`, `--temporary-directory` (and `-S` is harmless) to
   `DENIED_FLAGS["sort"]`.
6. **MEDIUM (old) — no read confinement, and the first stage inherits the gate's stdin.** Rows 24/25:
   `cat` with an absolute path outside root prints the file into the FIG line, and bare `cat` reads
   whatever the auditor had on stdin (both printed `SECRET-STDIN-TOKEN-9f3a`). Impact: a ledger
   author can exfiltrate any file the gate user can read into the audit output, and can hang a derive
   on a tty stdin until the 300 s deadline. Smallest remediation: `stdin=subprocess.DEVNULL` unless
   `< file` was parsed, and refuse absolute/`..` operands for the read-only heads (documented as a
   capability restriction, the same way `cat_sigpipe_exempt` already is).
7. **LOW (old) — the deny lists are ASCII-dash spelling-exact.** Rows 3/4: `-u` and `–url` are
   admitted (argparse then rejects them, so inert today); a hand-rolled parser could honour either.
   Rows 1/26/27: `-- <flag>` is admitted and inert for argparse heads. Smallest remediation: refuse
   any argv token whose first character is a dash-like codepoint (U+2010..U+2015, U+2212) for
   allow-listed heads.
8. **LOW (old, admission cost not security) — `python3 -B <script>` is refused** (row 31) because
   `parts[1]` must start with `corpus/instruments/`; any interpreter flag before the script refuses
   a legitimate derive. Worth naming because several lane counters are habitually invoked with `-B`.
9. **Note (old, unmeasured) — PATH is not pinned and argv[0] is PATH-resolved.** The strace showed
   `execve("python3")` candidates walked across eight PATH entries before one succeeded; the gate
   decides on the name, not the binary. Combined with `sort`/`git`/`cat` from PATH this is a
   boundary statement, not a measured exploit.

## 6. Coverage limits

33 table attempts (one figure each, every one replayed against the round-70 gate), plus the nine
tokenizer rows in §1 and four `freeze-check` gate variants. Not attempted: network egress through an
admitted head (none of R1-R8 needs it — `--url` is denied on capture-source and inert under alias
without `--out`); a `git` spelling that reaches a textconv or pager without `--textconv` (all
`-c`/`-p`/`--textconv` spellings and non-`rev:path` operands are refused; stdout is a pipe so a pager
would not start anyway); `r46-landing-gate.py --report/--work` writes (static: its `fx()` fixture
runner does `git add -A`/`git commit` only in selftest fixture lanes, lines 326-342, and `--selftest`
is refused for that head — its report/`--work` write path is unmeasured here); CPU-exhaustion sizing
for row 14 (the spill count is a function of `-S`).
Everything above is a measured command and its observed output; the class counts in R1 and in
residuals 1-2 are static enumerations over the committed census, named as such.
