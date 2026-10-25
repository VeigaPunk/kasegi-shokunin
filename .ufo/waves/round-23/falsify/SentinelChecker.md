# SentinelChecker — trust-boundary / failure-mode attack on `mirror-containment-check.py`

Round-23 FALSIFY wave, sentinel seat. Target: `corpus/instruments/mirror-containment-check.py`
and the matrix it consumes. Read-only on all production files; every mutation and side-effect
probe ran on `/tmp` copies. **This file was rewritten under me mid-seat (03:43–03:48), so this
report is organised as: current bytes first, then the disposition of the findings I filed against
the earlier bytes.** Nothing in the production tree was edited by me.

## Artifact identity (recomputed at each measurement, not taken from any receipt)

| revision | `mirror-containment-check.py` | `mirror-containment-fixtures.json` | `resolve.py` |
|---|---|---|---|
| R1 — analysed 03:37–03:40 (my first pass) | `1bc2db10dfbc59ef863e68afce475cd1d317da517137922804d7fc09cd46cecb` | `5e61a33ed5fa530547aff197fad9380d86d5850374bbb4f2a8f99df44b5e76a9` | `ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9` |
| **R2 — measured 03:44–03:50 (first pass on the rewrite)** | **`53742c8d9529dffb8c40c39b3448de7388b774b548d7831670598d5534bff5d1`** (12372 B) | `332a5fe9…` (23 cases) | `fce5b84b…` |
| **R3 — current at 03:52 (matrix/resolver moved again; checker byte-identical to R2)** | **`53742c8d…`** — unchanged | `d05b1e0cf62738ac8bf06497334c16a392089a5792ca9fd930f0cbf73e69b809` (10327 B, 24 cases) | `690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d` (28599 B) |
| **R4 — current at 03:53 (checker touched again)** | **`dddd55496b55eb49138613e3b7143834412cdb104b7f8f6b6e85210f3dd98f8a`** (12818 B) | `d05b1e0c…` | `690153ad…` |

R2's matrix had 23 cases (11 escape / 12 controls); R3/R4's has **24 (12 / 12)**, the new one being
`bounty-root-underscore-sibling` (escape, `GONE`). Between R2 and R4 the checker changed once more,
at 03:52:42: `diff` shows the entire delta is receipt metadata — `read_tsv` now also carries the
`method`/`domain` columns through to `record["method"]`/`record["domain"]` and `rows` values grew
from 2-tuples to 4-tuples. No guard, bound, wait or verdict path was touched. I therefore
re-verified the findings on R4 rather than inheriting them: default matrix 24/24 (`exit=0`), N1
carve-out waiver reproduced with `resolved_path=/etc/passwd`, N4 unrelated-in-root `RESOLVES`
reproduced. **Part 1 findings are properties of the bytes on disk now**; only the matrix and
resolver keep moving. R3 run on the current bytes:

```
$ cd /tmp/kasegi-r23-falsify-SentinelChecker/src3 && python3 mirror-containment-check.py --json ../receipt-r3.json
... 24 lines ...
cases=24 escape=12 controls=12 pass=24 fail=0 resolver_sha256=690153ad... matrix_sha256=d05b1e0c...
exit=0
```

`c1-fixed.json` keeps pace with each edit and at R4 pins all three: `checker_sha256=dddd5549…`,
`resolver_sha256=690153ad…`, `matrix_sha256=d05b1e0c…`, `generated_at=2026-10-25T06:52:43Z`
(= 03:52:43 local, i.e. the R4 edit), 24 ids in the same order, 24/24. Two transient states existed
earlier (`158a423c…` at 03:47 and `332a5fe9…` at 03:48, each briefly ahead of the receipt); I make
no claim about them. Because the receipt now pins the checker as well as the bytes it ran, the
R1-F7 provenance gap is closed *provided* the receipt is regenerated after every edit — which is
what happened here. Integration is still in flight, so treat the identity table as a timestamped
observation rather than a stable pin.

Scratch: `/tmp/kasegi-r23-falsify-SentinelChecker/` — R1 bytes in `src/`, **R2 bytes in `src2/`**,
R2 probes in `v2/`. All citations below are inlined as command+output; the tree is `/tmp` and not
durable. The two mutated copies of the checker are diff-verified and neither touches measured code
paths: `orphan/check-t3.py` (one line, `TIMEOUT_S = 120` → `2`) and `probe/check-copyprobe.py`
(one added 4-line `finally` block, used only in the R1 env probe). Interpreter: CPython 3.14
(`/usr/lib/python3.14`). No packages installed or updated (pacman paused host-wide; nothing needed).

R2 default-path reproduction:

```
$ cd /tmp/kasegi-r23-falsify-SentinelChecker/src2 && python3 mirror-containment-check.py --json ../receipt-current.json
bounty-parent-traversal                    escape  expect=GONE  actual=GONE  PASS
... 22 more ...
lane-relative-parent-internal-control      control expect=INTERNAL actual=INTERNAL PASS path_check=carve-out:path-outside-internal
cases=23 escape=11 controls=12 pass=23 fail=0 resolver_sha256=fce5b84b... matrix_sha256=332a5fe9...
exit=0
```

---

# Part 1 — live findings on the current checker (`dddd5549…`; guards identical in R2/R3/R4)

## N1 — MEDIUM — the new path audit is waivable by the same fixture data it guards (`path_tolerance: "carve-out"`)

**What changed and why it matters.** R2 added `path_verdict()` (`:140-152`): a non-GONE class must
name an existing path confined to `{MIRROR-EQUIVALENT: mirror, INTERNAL: lane, else: root}`
(`:149`), and `PASS` now requires `path_check == ""` — *or* `tolerated` (`:216-221`), where
`tolerated` is set whenever the **case itself** declares `"path_tolerance": "carve-out"`. The
waiver is unconditional: any verdict string, including `path-outside-mirror-equivalent`, is
accepted, and the case still counts as `PASS` in `totals.pass` and the exit code (`:301`).

**Evidence — a doctored case waives the audit for `/etc/passwd`:**

```
$ cat fixtures-carveout.json     # one case: expect MIRROR-EQUIVALENT + "path_tolerance": "carve-out"
$ python3 mirror-containment-check.py --resolver hostmirror/fake.py --fixtures fixtures-carveout.json --json rec-carveout.json
self-declared-carveout  control expect=MIRROR-EQUIVALENT actual=MIRROR-EQUIVALENT PASS path_check=carve-out:path-outside-mirror-equivalent
cases=1 escape=0 controls=1 pass=1 fail=0 ... exit=0
$ python3 -c "... rec-carveout.json ..."
status PASS | path_check carve-out:path-outside-mirror-equivalent | resolved_path /etc/passwd
```

The receipt and the printed line *do* keep the escape visible — that is a genuine improvement, and
the one legitimate use in the frozen matrix (`lane-relative-parent-internal-control`, whose
`../outside.md` really does leave the lane root) is honest. But `status`, `totals.pass` and `exit 0`
no longer imply the path audit passed, and the waiver is not restricted to the INTERNAL class or to
the specific `path-outside-internal` verdict.

**Impact.** The control half of the matrix remains conditionally self-auditing at the data layer:
adding one key to any future case silently converts a path failure into a pass. A reader who greps
`pass=23`/`exit 0` (the exact habit N3 rests on) sees nothing.

**Smallest remediation.** Restrict carve-out to `expect == "INTERNAL"` **and** to the exact
`path-outside-internal` verdict, require a per-case `carve_out_reason` string, and report
`totals["carve_outs"]` separately with exit 0 requiring the count to equal a pinned number
(currently 1) or 0.

## N2 — MEDIUM — a `setsid()` descendant converts the timeout into an unbounded hang (the killpg fix does not cover it)

**What changed.** R2 replaced `subprocess.run(timeout=…)` with `Popen(..., start_new_session=True)`
plus `os.killpg(proc.pid, SIGKILL)` on `TimeoutExpired` (`:185-196`) — the right direction — but the
kill targets only that one process group, and the follow-up `proc.communicate()` (`:196`) has **no
deadline**. Any descendant that leaves the group keeps the inherited stdout/stderr pipes open, so
the second `communicate()` waits forever.

**Evidence** (R2 checker, one-line `TIMEOUT_S = 2` scratch mutant; resolver forks, `os.setsid()`s,
then sleeps 600 s holding the pipes; external 20 s cap):

```
$ diff src2/mirror-containment-check.py orphan/check-t3.py
-TIMEOUT_S = 120
+TIMEOUT_S = 2
$ time timeout 20s python3 orphan/check-t3.py --resolver orphan-resolver-long.py --fixtures fixtures-orphan.json
real 0m20.001s
exit=124                      # the checker never returned: stuck in proc.communicate() at :196
$ cat orphan-descendant-proof.txt
holding the stdout pipe
```

For contrast, a descendant that stays in the group is handled correctly — the earlier probe with
`setsid` removed returned in 4.0 s with `problems=timeout`, i.e. the fix works exactly as far as the
process group reaches. This is a *new* failure mode in the sense that the stated mechanism
(`killpg`) is now the whole defence, and it is defeated by three lines.

**Impact.** A hung or hostile resolver — including a historical `git show` blob replayed via
`--resolver` — hangs the instrument indefinitely with no output, no receipt, and a live pipe holder.
The only bound is whatever the caller wraps around it; the file's own `TIMEOUT_S` docstring has no
force.

**Smallest remediation.** Give the second wait a deadline (`proc.communicate(timeout=5)`, then
`proc.kill()` and abandon the pipes), and/or write child stdout/stderr to files inside the case root
instead of pipes (`stdout=open(...,'wb')`) so a surviving holder cannot block the parent; optionally
walk `/proc/<pid>/task/*/children` and kill each new descendant after the group kill.

## N3 — MEDIUM — child output is still buffered without bound in the parent (`MAX_STDOUT_STORED` caps storage, not memory)

**What R2 changed.** `MAX_STDOUT_STORED = 400` (`:46`) truncates what is *recorded* (`:200,203,213`)
and `MAX_TSV_BYTES = 8 MiB` (`:47`) bounds the TSV read (`:123`). Neither bounds what is *read*:
`Popen(..., stdout=PIPE)` + `communicate()` (`:185-190`) still accumulates every byte in the parent.

**Evidence** (200 MiB of child stdout, R2 checker, `resource.getrusage(RUSAGE_CHILDREN)`):

```
checker exit: 1 | max child RSS KiB: 634200 delta 619.3 MiB
```

vs 617.9 MiB on R1 — unchanged within noise. 619 MiB of parent RSS for 200 MiB of child bytes; the
only ceiling remains 120 s of writing, i.e. multiple GiB on a fast pipe.

**Impact.** OOM of the checker mid-matrix; the receipt is written only after the loop (`:278-296`),
so the entire run's evidence is lost and the only signal is a killed process.

**Smallest remediation.** Redirect the child's stdout/stderr to files inside the case root and read
at most `MAX_STDOUT_STORED` bytes from them; that fixes N2 and N3 together.

## N4 — LOW-MEDIUM — `RESOLVES` is bound to the whole case root, so any in-root file satisfies the path audit

`path_verdict` binds `RESOLVES` to `root` (`:149`) — which contains the lane, the mirror, and every
planted file — while `MIRROR-EQUIVALENT` binds to `mirror` and `INTERNAL` to `lane`.

**Evidence** — a resolver that ignores the citation and reports `lane/SKILL.md`:

```
$ python3 mirror-containment-check.py --resolver hostmirror/lane-skill.py --fixtures fixtures-resolves-weak.json
resolves-satisfied-by-unrelated-in-root-file control expect=RESOLVES actual=RESOLVES PASS
cases=1 escape=0 controls=1 pass=1 fail=0 ... exit=0
```

(cite was `/no/such/tree/thing.md:1`). Out-of-root paths are still rejected —
`path-outside-resolves` on the same fixture with `/etc/passwd` — so the audit is not vacuous, just
satisfiable by an unrelated file for the largest class.

**Impact.** For `RESOLVES` controls the assertion proves "some file exists inside the case root",
not "the cited path resolved". `RESOLVES` is the joint-largest control class (4 of 12), alongside
`MIRROR-EQUIVALENT` (4), with `GONE` (2) and `INTERNAL` (2) behind them.

**Smallest remediation.** For `RESOLVES`, also require the class's own method/domain columns to
agree with the reported path (the resolver already emits them), or compare the reported path's
suffix to the citation's suffix.

## N5 — LOW — per-case containment is real but incomplete: two shape abuses still abort the whole run

The new `except Exception` (`:223`) does contain everything *inside* the case — my R1 crash vectors
(UTF-8 decode error, dangling symlink, bad path) now yield `problems=["case-error:…"]` and the
matrix continues (see P1 evidence). Two entry points sit outside it:

```
# fixtures with schema 1 + cases but no "defaults"
File ".../mirror-containment-check.py", line 254, in main
    defaults = matrix["defaults"]
KeyError: 'defaults'                                                              exit=1

# a non-dict case in the list (record is built from case.get() at :158-159, before the try at :223)
File ".../mirror-containment-check.py", line 159, in run_case
    "id": case.get("id", "unnamed"),
AttributeError: 'int' object has no attribute 'get'                               exit=1
```

**Impact.** A malformed matrix still loses every completed case and produces a traceback instead of
a receipt; `--json` is never written.

**Smallest remediation.** Validate `defaults` and each case's type/required keys in the existing
schema check (`:244-246`, next to the `schema`/`cases` test) and record `case-error` for anything
that fails.

## N6 — LOW — by design, unchanged: the selected resolver still runs unconfined, and its bytes still reach the receipt

R2 keeps the R1 trust model: `--resolver` bytes are executed with the lane user's full privilege;
env is replaced (6 keys, verified), there is no read/write barrier, and up to 400 bytes of
resolver-chosen stdout are stored in the receipt (`:200`). Verified on R2: a resolver that reports
`GONE` with an empty path and prints `/etc/hostname` back:

```
exfil-in-receipt  escape expect=GONE actual=GONE PASS        exit=0
status PASS | stored stdout len 341 | head: HOST-FILE-DISCLOSURE:plazir27plazir27...
```

The `<CASE>` root substitution (`:200,203,213`) is a genuine hygiene improvement over R1. What is
unchanged is that a passing receipt is evidence about bytes that ran with full user privilege and
that receipts can carry host data (now ≤400 B per field).

**Smallest remediation.** State the trust model in the docstring ("`--resolver` is executed
unconfined; do not pass bytes you would not run"), and drop `cli_stdout` from the receipt (keep it
in the console line only).

---

# Part 2 — disposition of the R1 findings (analysed bytes `1bc2db10…`)

Verified by replaying each R1 probe against R2 bytes, not by reading the diff.

| R1 finding | Severity then | Status on R2 | R2 evidence |
|---|---|---|---|
| **F1** fixture names joined without confinement → host write, `/tmp` write, host file unlink via symlink chain | HIGH | **FIXED** — `safe_path` (`:59-76`) rejects absolute/`..` and re-checks the resolved parent; `check_link_target` (`:78-87`) confines targets | `traversal-absolute` → `case-error:ValueError:unsafe-dir:'…/escape-dir'`; `symlink-chain-host-unlink` → `case-error:ValueError:escape-symlink-target:'…/hostdir'`; `symlink-target-absolute-host` → `…escape-symlink-target:'/etc/passwd'`; `escape-dir`/`escape-file.txt`/`/tmp/escape-rel.txt` absent; `hostdir/victim.txt` still `HOST-VICTIM` |
| **F2** unconfined resolver; stdout persisted verbatim | MEDIUM | **PARTIAL** — root substituted + capped at 400 B; still unconfined, still persisted (N6) | 341-byte disclosure in `rec-goneexfil.json`, `exit=0` |
| **F3** verdict self-reported, `resolved_path` never read | MEDIUM | **PARTIAL** — class *and* path now compared (`:120-152,221`); a `/etc/passwd` MIRROR-EQUIVALENT now fails | `mirror-control-host-path … FAIL path_check=path-outside-mirror-equivalent`; residues N1 and N4 |
| **F4** timeout kills only the direct child; descendants survive | MEDIUM | **PARTIAL** — `start_new_session` + `killpg` added, cooperative descendants now die; `setsid` descendants still hang the checker (N2) | `timeout 20s … exit=124` |
| **F5** unbounded child output in parent memory | MEDIUM | **NOT FIXED** — storage capped, memory not (N3) | 619.3 MiB delta |
| **F6** no per-case exception containment | LOW-MED | **MOSTLY FIXED** — `except Exception` per case; `defaults`/non-dict case still abort (N5) | R1's three crash vectors now record `case-error`; two shape abuses still `exit=1` with traceback |
| **F7** exit code + provenance weak; matrix hash from a second read (TOCTOU) | LOW | **FIXED** — `schema 2`, `checker_sha256`, `generated_at`, and `matrix_sha256 = sha256_bytes(fixtures_bytes)` from the parsed buffer (`:256-257,282`) | `rec-hostread.json`: `schema 2 … checker_sha256 53742c8d… … generated_at …`; residual: exit still `len(passed)==len(records)` (`:301`), so a 1-case matrix still exits 0 (verified in N1's run) |
| **F8** named missing bounds (no aggregate deadline, unbounded rmtree, whole-file fixture read) | INFO | **PARTIAL** — TSV capped at 8 MiB; aggregate deadline and rmtree still unbounded | by inspection |

## Guarantees that hold on R2 (each with its basis)

| Guarantee | Basis | Verification |
|---|---|---|
| G1 no fixture-supplied path reaches outside the case root | `safe_path` + `check_link_target`, applied before every mkdir/open/symlink/unlink (`:100-118`) | three escape fixtures → `case-error`, no host artifacts, victim intact |
| G2 child env is exactly 6 keys; parent env does not leak | fixed `env` dict (`:174-182`) | `KASEGI_SECRET=topsecret-abc123` absent; `env_keys` = 6 names (R1 probe, env block unchanged in R2) |
| G3 only `--resolver` bytes and `sys.executable` execute; fixture bytes are data | `Popen([sys.executable, copied, lane])` | R1 probe: `tool/sitecustomize.py` and `tool/usercustomize.py` supplied as fixture `files` never ran |
| G4 the matrix is not vacuous and controls are path-audited | fixture data + `path_verdict` | 23/23 on R2 and 24/24 on R3; `/etc/passwd` and out-of-root paths fail; R1 baseline `d6a3c3f1…` scored 7/13 |
| G5 the landed receipt describes the bytes on disk | receipt `resolver_sha256`/`matrix_sha256` vs measured | at R3: `690153ad…` and `d05b1e0c…` match, same 24 ids, 24/24 (R2 matched its own pair too, 23/23) |
| G6 escapes are pinned `GONE`, controls pin surviving classes | fixture data | `escape=12`, all `expect=GONE`; `controls=12`, one declared `path_tolerance` |

## Bounds the instrument still does not have

- Aggregate deadline: per-case `TIMEOUT_S = 120` (`:44`) only, N cases serial, N from fixtures.
- A deadline on the **second** `communicate()` after a timeout (`:196`) — N2.
- Any memory ceiling on captured output (`:185-190`) — N3.
- Case/`defaults` shape validation before the loop (`:158-159`, `:254`) — N5.
- Timeout on `shutil.rmtree(root, ignore_errors=True)` (`:225`) and partial-cleanup reporting.
- Any check that a passing `RESOLVES` path is *related* to the citation (`:149`) — N4.
- Any restriction on which verdicts a fixture may waive (`:216-219`) — N1.

## Scope limits

- Attacked the checker and the matrix; I did **not** audit `resolve.py`'s containment predicates
  (C1's `bounty_suffix`/`under_mirror`) or the C2 snapshot artifacts — sibling seats own those. The
  only production change I observed in `resolve.py` is that R2 is 77 diff lines from R1; I make no
  claim about its correctness beyond what the matrix shows.
- All probes ran against `/tmp` scratch: `/etc/hostname` was the only host file read, and the only
  host file I attempted to delete was one I created in scratch (`v2/hostdir/victim.txt`), which
  survived. `/tmp/escape-rel.txt` (created by the R1 probe) was removed after capture.
- Not exercised: read-only filesystems, `--json` aimed at a symlink/`/dev/full`, umask variants,
  non-CPython `sys.executable`, `TMPDIR`-set hosts, and a resolver that races the TSV read.
- The R2 findings rest on a *fixture/resolver I supply*; they are defects of the instrument's own
  guarantees, not claims that the frozen matrix or the current `resolve.py` is wrong.
- Read-only compliance: the only file I wrote is this report. No git/jj command was run, no lane or
  sibling-lane file touched, no install or host configuration performed.
- No admission, score, or claim-status movement is asserted.
