# SentinelChecker — trust-boundary / failure-mode attack on `mirror-containment-check.py`

Round-23 FALSIFY wave, sentinel seat. Target: `corpus/instruments/mirror-containment-check.py` only
(plus the frozen matrix it consumes). Read-only on all production files; every mutation and
side-effect probe ran on `/tmp` copies.

## Artifact identity (recomputed, not taken from any receipt)

| artifact | sha256 |
|---|---|
| `corpus/instruments/mirror-containment-check.py` (under test) | `1bc2db10dfbc59ef863e68afce475cd1d317da517137922804d7fc09cd46cecb` |
| `corpus/instruments/mirror-containment-fixtures.json` | `5e61a33ed5fa530547aff197fad9380d86d5850374bbb4f2a8f99df44b5e76a9` |
| `corpus/instruments/resolve.py` | `ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9` |

Scratch: `/tmp/kasegi-r23-falsify-SentinelChecker/` (256 K, present at write time with the three
shas above). It is `/tmp` and therefore **not durable**: every observable this report relies on is
inlined below as the exact command plus its output, so no finding depends on that tree surviving a
`/tmp` sweep. (For the same reason I assert nothing about the separate round-35 wave's scratch
tree, which was relocated to `scratch-evidence/` and partly re-created/deleted again between ~03:43
and ~03:46; this report cites no wave scratch path.) Interpreter seen in tracebacks:
`/usr/lib/python3.14` (CPython 3.14). No packages installed or updated (pacman paused host-wide;
nothing was needed).

**Derived bytes I created (rebuild ≠ evidence).** Nothing here was rebuilt from a transcript; these
are the exact files that produced the inlined outputs, pinned so a later reader can tell a
substitution from the original. All are *derived* (doctored fixtures and resolver stubs), not
authoritative sources — the authoritative bytes are the three production files above. Note the
fixtures embed `$S` absolute paths, so their hashes are path-dependent: they pin these bytes at
this path only.

| scratch artifact | bytes | sha256 |
|---|---|---|
| `receipt-baseline.json` | 8140 | `ce24314b904d1a13449270fe6333453039944471b37e48fc5a73c67705ed5056` |
| `fixtures-traversal.json` | 890 | `48814c3a4df21a48187f19fedb3a62407d67d2e67ebf2c02ea1412662ac877e0` |
| `exfil/fake-resolver.py` | 508 | `c48a1dfd5d593f5304fd9d5c94549f75c9e1d541ff624e22fd4d778760cbfbb2` |
| `fixtures-hostread.json` | 393 | `cff417c60a70526817c8e144bc86f5f97ff32f28ef565067333ff237e2f5556a` |
| `receipt-hostread.json` | 869 | `0479015f05bf3f9c7fa097562c2f1fb84ed37dc984656eddd3a5c3ae22ee4792` |
| `table/table-resolver.py` | 1426 | `0cd5e54d59bedf2526e12cec0d0905a99d0a1718293823eadae5c4b344f92dab` |
| `receipt-table.json` | 5445 | `d612ba29b88889a80c518bba44383b553220cb911a1b1f942a59e44a2842c3ed` |
| `hostmirror/fake.py` | 364 | `da6936387b3d928e11e3db97cacea46156327a4e98ca688f703400af5c52a36d` |
| `fixtures-hostmirror.json` | 312 | `fd15e90830855cbd1966f531e014cc6e5519a2d1a9e239ae17a4516a1595d9e0` |
| `orphan/check-t3.py` | 8286 | `3e151e2223818398fbd29731cde74145ee0af2eb7f30ad1eb1576bfb45f81b6a` |
| `orphan/orphan-resolver.py` | 270 | `3443e00817ea41a137a998b33e47157443b3f7bcfae2e71c58047a187d484a9d` |
| `fixtures-orphan.json` | 359 | `b0bf41293c57003ab6734b4a7669112a2c810339be536364f0b335c3de84e467` |
| `bomb/stdout-bomb.py` | 84 | `e54afaefe79474606a9ab174478bc25f5a8cae0d6e43634f97e5ded4dd305ce9` |
| `fixtures-bomb.json` | 364 | `8ac27738c5f5dfd86e55747ed092abca4244df85decdbe10cfdd70ab0b8eb22b` |
| `utf8/bad-utf8-resolver.py` | 78 | `6b87d89f80141dd4030e6a4c938205996e9a42dce25921a74fe75cc038d51aed` |
| `probe/probe-resolver.py` | 557 | `3b8b567cae71853d8cade4debc92ab868511581f58ed1e9d3fe411e1b51a50a6` |
| `probe/check-copyprobe.py` | 8494 | `d50e580e1a5e822f76d1be60d2718933c823fdb5004dc3a7e1533148eb9b992a` |
| `fixtures-probe.json` | 679 | `c315ba21091e798fcae046c5da59e498560b4dff48310cb1519b9d63fec0987e` |

Two artifacts are mutated copies of the checker under test, both verified by diff, and neither
touches the measured code paths:

- `orphan/check-t3.py` — exactly one line (`TIMEOUT_S = 120` → `2`), so F4's timeout behaviour is
  produced by production logic at a shorter clock, not by rewritten logic;
- `probe/check-copyprobe.py` — one added 4-line block in the existing `finally` that copies
  `tool/probe.json` out before `rmtree` (the manifest above records `probe/probe-resolver.py`'s
  readings); `build_case`, the env dict and the run path are byte-identical to production.

Every other artifact's *behaviour* is fully quoted in its finding, so a reader can reconstruct it
without the tree and still check the claim against the inlined output.

Default-path reproduction (production bytes, unmodified, copied to scratch):

```
$ cd /tmp/kasegi-r23-falsify-SentinelChecker/src && time python3 mirror-containment-check.py --json ../receipt-baseline.json
... 13 lines ...
cases=13 escape=6 controls=7 pass=13 fail=0 resolver_sha256=ed9a9dae... matrix_sha256=5e61a33e...
real 0m0.232s
exit=0
totals {'cases':13,'controls':7,'escape':6,'fail':0,'pass':13}
```

So the happy path reproduces 13/13 here in 0.23 s, and the receipt's two hashes match the
production bytes above. Everything below is about what that number does and does not buy.

---

## F1 — HIGH — fixture data is joined to the temp root with no confinement: arbitrary host file write, truncate and delete

**Guarantee it breaks.** The only thing making "writes stay in the temp root" true is
`os.path.join(root, rel)` on data that currently happens to be relative. There is no
`commonpath`/`realpath` check, no rejection of absolute names, no rejection of `..` segments
(`corpus/instruments/mirror-containment-check.py:49-64,70-74`). `defaults` is merged into every
case (`:49,53,57`), so one poisoned `defaults.files` entry escapes for all 13 cases.

**Exploit path.** The instrument advertises `--fixtures PATH` (`:149`) and its purpose is to replay
"a frozen matrix" that contributors may propose changes to. A doctored or PR-substituted matrix
executes these paths as data:

1. absolute `dirs`/`files` keys → `os.makedirs` / `open(...,"w")` at that absolute path (`:51,71-74`);
2. `../…` keys → the same, one level above the `mkdtemp` root;
3. two ordered `symlinks` entries — `"esc": "/any/host/dir"` then `"esc/victim.txt": …` — make
   `os.path.lexists()`/`os.remove()` act **through** the first link (`:59-64`), deleting a real
   host file outside the root and then planting a symlink in its place.

**Evidence** (doctored matrix in scratch; `$S=/tmp/kasegi-r23-falsify-SentinelChecker`):

```
$ ls -l "$S/victimdir/"          # before: -rw-r--r-- victim.txt "host victim file"
$ cd "$S/src" && python3 mirror-containment-check.py --fixtures "$S/fixtures-traversal.json"; echo exit=$?
exit=0
$ ls -ld "$S/escape-dir" "$S/escape-file.txt" /tmp/escape-rel.txt
drwxr-xr-x 2 vgpnk vgpnk  6 ... /tmp/kasegi-r23-falsify-SentinelChecker/escape-dir
-rw-r--r-- 1 vgpnk vgpnk 33 ... /tmp/kasegi-r23-falsify-SentinelChecker/escape-file.txt
-rw-r--r-- 1 vgpnk vgpnk 44 ... /tmp/escape-rel.txt          # from the "../escape-rel.txt" key
$ ls -l "$S/victimdir/"
lrwxrwxrwx 1 vgpnk vgpnk 43 ... victim.txt -> /tmp/kasegi-r23-c1-wyvaht1f/does-not-matter
$ cat "$S/victimdir/victim.txt"
cat: .../victim.txt: No such file or directory
```

The absolute keys wrote two artifacts outside the `mkdtemp` root, the `../` key wrote directly into
`/tmp`, and the host file named by the symlink chain was **unlinked and replaced**. In a real run
the same shape reaches `~/.bashrc`, `~/.config/…`, or any corpus file the lane user can write,
including this repo.

**Impact.** Data-to-arbitrary-write/delete as the invoking user, for an artifact whose entire job
is to consume an externally editable JSON file. It also gives a reviewer no way to tell a benign
matrix edit from a destructive one without reading every `files`/`dirs`/`symlinks` key.

**Smallest remediation.** In `build_case`/`write_file`, resolve each name against the root and
refuse unless `os.path.commonpath((root, os.path.realpath(joined))) == os.path.realpath(root)`,
plus refuse absolute names and `..` segments before creating anything; create symlinks after
validating their *names* the same way, and never `os.remove` a path whose parent resolves outside
the root. (The frozen shipped matrix passes such a guard — see G4.)

---

## F2 — MEDIUM — the selected resolver runs with no confinement at all, and its stdout is persisted verbatim into the receipt

**Guarantee it rests on.** Only the env dict at `:96-103` plus `cwd=tool`. That is process
*environment* substitution, not a filesystem boundary: no user namespace, no seccomp, no chroot,
no read/write barrier. The docstring's "executed once per matrix case with an isolated HOME,
KASEGI_MIRROR and lane root" (`:5-7`) reads stronger than the code delivers.

**Evidence — env is genuinely replaced (this part holds):**

```
$ KASEGI_SECRET=topsecret-abc123 python3 check-copyprobe.py --resolver probe-resolver.py ... 
{"cwd":"/tmp/kasegi-r23-c1-wjp50hp4/tool","home":"/tmp/kasegi-r23-c1-wjp50hp4/home",
 "mirror":"/tmp/kasegi-r23-c1-wjp50hp4/relocated/tbh","secret_leak":"<absent>","tmpdir":"<absent>",
 "env_keys":["HOME","KASEGI_MIRROR","LANG","LC_ALL","PATH","PYTHONDONTWRITEBYTECODE"]}
```

**Evidence — host read is unbounded and lands in the receipt:**

```
$ python3 mirror-containment-check.py --resolver "$S/exfil/fake-resolver.py" --fixtures fixtures-hostread.json --json receipt-hostread.json
host-read-through-selected-resolver  control expect=RESOLVES actual=RESOLVES PASS
exit=0
$ python3 -c "... receipt-hostread.json ..."
class= RESOLVES
stdout= HOST-FILE-DISCLOSURE:plazir27          # /etc/hostname content
```

Two things follow: (a) the resolver reads anything the lane user can read, which is expected for
`--resolver` but is not disclosed as the actual trust model; (b) `record["cli_stdout"]`
(`:113`) copies child-controlled bytes into the receipt unconditionally, so any secret or host data
the resolver prints is persisted into the wave artifact. `PATH` is also inherited (`:99`) and
`TMPDIR` is unset, so a resolver's `tempfile` writes land in host `/tmp`, outside the case root.

**Impact.** A passing receipt is evidence about *bytes that ran with full user privilege*, not about
a contained run; and receipts can silently carry host data.

**Smallest remediation.** Retract the "isolated" wording to "HOME/KASEGI_MIRROR are redirected";
stop recording `cli_stdout` (or keep ≤200 bytes and strip), and set `PATH=/usr/bin:/bin` explicitly
rather than inheriting it.

---

## F3 — MEDIUM — the verdict is the resolver's own self-report; `resolved_path` is never inspected

**Guarantee it rests on.** `record["actual"] = classes.get(case["cite"], "NO-ROW")` where
`classes` maps the TSV's `citation` column to its `class` column (`:122-138`). Only two columns are
read (`:126-127`); `resolved_path` is never compared to the case root or to the mirror.

**Evidence A — a lookup table with zero containment logic scores 13/13, exit 0.** A 25-line
resolver that reads the cite from `lane/SKILL.md`, maps it through a dict, and writes
`<cite>\t<class>\t/fabricated\t1`:

```
$ python3 mirror-containment-check.py --resolver "$S/table/table-resolver.py" --json receipt-table.json
cases=13 escape=6 controls=7 pass=13 fail=0 resolver_sha256=0cd5e54d... matrix_sha256=5e61a33e...
exit=0
totals {'cases':13,'controls':7,'escape':6,'fail':0,'pass':13}
```

**Evidence B — a MIRROR-EQUIVALENT control passes while reporting a host path:**

```
resolver writes: ~/Projects/bounties/ops/rank.mjs:1 \t MIRROR-EQUIVALENT \t /etc/passwd \t 1
$ python3 mirror-containment-check.py --resolver "$S/hostmirror/fake.py" --fixtures fixtures-hostmirror.json
mirror-control-host-path  control expect=MIRROR-EQUIVALENT actual=MIRROR-EQUIVALENT PASS
exit=0
```

**Impact.** "13/13 under the frozen matrix" is a statement about classification strings emitted by
those bytes. It does not demonstrate either C1 predicate (`bounty_suffix` exact-root boundary,
`under_mirror` realpath confinement) and it cannot detect a resolver that credits a path outside the
selected mirror, because the harness never looks at the credited path. This is the fabricated-
readiness class of defect if 13/13 is cited as containment proof on its own.

**Smallest remediation.** For cases whose expectation is `RESOLVES`/`MIRROR-EQUIVALENT`, assert
that the reported `resolved_path` is a realpath-confined descendant of the case's mirror root (the
checker already knows `root`, `home`, `mirror`); report `problems=["path-outside-mirror"]` otherwise.
That converts the control half of the matrix into an oracle the checker computes itself.

---

## F4 — MEDIUM — timeout kills only the direct child; descendants survive and keep writing after the run returns

**Guarantee it rests on.** `subprocess.run(..., timeout=TIMEOUT_S)` with no `start_new_session` /
process group. `TimeoutExpired` is handled (`:109-111`), the direct child is killed, and the temp
root is removed in `finally` (`:141-142`) — but nothing kills the resolver's children, and nothing
stops them writing by absolute path after `rmtree`.

**Evidence** (scratch copy differs from production by one line — `TIMEOUT_S = 120` → `2`; diff
shown, `$S/orphan/check-t3.py`). Resolver forks an orphan that sleeps 4 s and writes a marker:

```
$ diff -u src/mirror-containment-check.py orphan/check-t3.py
-TIMEOUT_S = 120
+TIMEOUT_S = 2
$ time python3 check-t3.py --resolver orphan/orphan-resolver.py --fixtures fixtures-orphan.json
orphan  control expect=GONE actual=NO-ROW FAIL problems=timeout
real 0m2.043s
exit=1
$ sleep 5; cat "$S/orphan-descendant-proof.txt"
descendant survived the checker's timeout
```

**Impact.** A slow or hung resolver leaks processes that outlive the matrix run and can write
anywhere afterwards; repeated CI invocations accumulate them. No cleanup step can observe them,
because the record says `problems=timeout` and the root is already gone.

**Smallest remediation.** `subprocess.Popen(..., start_new_session=True)` and on timeout
`os.killpg(proc.pid, SIGKILL)` (then reap); or `process_group=0` on 3.11+ with the same killpg.

---

## F5 — MEDIUM — no bound on child output or on the TSV: memory grows with resolver-controlled bytes

**Guarantee it rests on.** `capture_output=True, text=True` (`:107`) buffers the child's entire
stdout/stderr in the checker, and the TSV is read line-by-line into a dict with no row/size cap
(`:123-136`). `TIMEOUT_S` bounds wall time, not bytes.

**Evidence.** Resolver writes 200 MiB to stdout; parent (checker) peak RSS delta measured with
`resource.getrusage(RUSAGE_CHILDREN)`:

```
$ python3 -c "... subprocess.run([sys.executable,'mirror-containment-check.py', '--resolver', stdout-bomb.py, ...])
checker exit: 1
max child RSS KiB: 632780 delta KiB: 632780 = 617.9 MiB
```

618 MiB of parent RSS for 200 MiB of child bytes (~3×: byte buffer + decoded str). The only ceiling
is 120 s of writing, i.e. multiple GiB on a fast pipe. Fixtures and resolver files are also read
whole (`:155,164`).

**Impact.** OOM of the checker mid-matrix; because the receipt is written only after the loop
(`:191-209`), the entire run's evidence is lost, and there is nothing in the record that says why.

**Smallest remediation.** Cap captured bytes (read incrementally, `problems=["stdout-overflow"]`
past N MiB), cap TSV rows/bytes, and reject a fixtures/resolver file above a size limit before
reading it.

---

## F6 — LOW-MEDIUM — no per-case exception containment: one malformed case or one odd child byte stream aborts the whole matrix, receipt lost

**Guarantee it rests on.** The only `except` around the child is `TimeoutExpired` (`:109`); the only
`except` around the TSV is the header `ValueError` (`:128`). `build_case` has no guard at all, and
`main`'s loop (`:174`) has none either. `finally` does clean the temp root, so this is not a leak —
it is total loss of results.

**Evidence (three independent aborts, all exit 1, `--json` never written):**

```
# 1) child emits a non-UTF-8 byte
File "/usr/lib/python3.14/subprocess.py", line 1099, in _translate_newlines
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
exit=1 ; receipt-utf8.json: No such file or directory

# 2) fixtures symlink whose target directory does not exist (legal fixture, dangling link)
File ".../mirror-containment-check.py", line 61, in build_case
FileExistsError: [Errno 17] File exists: '/tmp/kasegi-r23-c1-p1ckzygn/esc'

# 3) fixtures with schema 1 + cases but no "defaults"
File ".../mirror-containment-check.py", line 169, in main
KeyError: 'defaults'
exit=1
```

**Impact.** A single hostile or merely sloppy case turns 12 completed cases into zero evidence, and
the exit status cannot distinguish "matrix failed" from "instrument crashed". `case["cite"]`/`id`/
`expect`/`nature` are also unvalidated (a case with `nature:"escape2"` would be counted in
`cases`/`pass` but in neither `escapes` nor `controls` at `:184-185`).

**Smallest remediation.** Wrap the body of `run_case` (and the `defaults = matrix["defaults"]` read)
in `try/except Exception as exc: record["problems"].append("crash-"+type(exc).__name__)`;
validate each case's required keys and `nature ∈ {escape,control}` before the loop; write the
receipt even when some records failed.

---

## F7 — LOW — the exit code and the matrix hash are weaker provenance than they look

**Guarantee it rests on.** `return 0 if len(passed) == len(records) else 1` (`:211`): success means
"every case this file contained agreed", with no requirement that there are 13 cases, 6 escapes, or
7 controls, and no comparison of `matrix_sha256` against any expected value.

**Evidence.** A one-case doctored matrix exits 0 (both F2 and F3 runs above: `cases=1 ... pass=1`,
`exit=0`). The receipt (`:192-206`) carries `resolver`/`resolver_sha256`, `matrix`/`matrix_sha256`,
`cases`, `totals` — and nothing else: no checker sha256, no `sys.version`, no start/finish
timestamp, no per-case resolver sha. A hand-written 13/13 receipt is byte-shape identical to a
generated one; the landed `c1-fixed.json` is only distinguishable by re-running.

**Second, small defect in the same block:** `matrix_sha256` is computed by `sha256_file(args.fixtures)`
(`:171`, a *second* open of the path) while the executed matrix came from the buffer read at `:155`.
Those are different reads; `TOCTOU` between them means the recorded hash need not describe the bytes
that were executed. The resolver path does not have this defect — `:170` hashes the same in-memory
buffer it copies at `:95`.

**Impact.** "exit 0 / 13 of 13" is not self-authenticating; and the matrix hash is not strictly
bound to the parsed matrix.

**Smallest remediation.** Hash the buffer read at `:155` (`hashlib.sha256(raw).hexdigest()`), record
`checker_sha256`, `sys.version` and `started/finished` timestamps, and make exit 0 additionally
require `escape == 6 and controls == 7` for the frozen matrix id (or fail loudly when the case
inventory does not match the expected one).

---

## F8 — INFO — bounds the file names and does not have

- **Per-case only:** `TIMEOUT_S = 120` (`:33`); no aggregate deadline. N cases × 120 s, N taken
  from the fixtures list (`:174`, unbounded length, serial).
- **Cleanup:** `shutil.rmtree(root, ignore_errors=True)` (`:142`) — no timeout; a resolver that
  fills the root within its 120 s makes cleanup unbounded, and `ignore_errors` hides partial
  cleanup. (In my runs no root leaked: the one `/tmp/kasegi-r23-c1-*` visible mid-experiment was a
  concurrently running sibling case's root and was gone on the next read — I am **not** claiming a
  temp-root leak.)
- **Sizes:** fixtures and resolver read whole (`:155,164`); TSV rows unbounded (F5).
- **Receipt:** `open(args.json,"w")` with no parent creation and no atomic replace (`:207`), written
  only after the last case (F6).

---

## Guarantees that do hold (verified, with the confinement they rest on)

| # | Guarantee | Rests on | Verification |
|---|---|---|---|
| G1 | Child env is exactly the 6-key dict; parent env does not leak | `:96-103` replaces `env` wholesale | `KASEGI_SECRET=topsecret-abc123` absent in child; `env_keys` = 6 names |
| G2 | No fixture bytes are executed; the only executed bytes are `--resolver` content and `sys.executable` | `:93-108`; fixture data is only written to files | `tool/sitecustomize.py` and `tool/usercustomize.py` supplied as `files` keys — `/tmp/.../sitecustomize-proof.txt` and `usercustomize-proof.txt` were **not** created |
| G3 | Working tree stays inside `mkdtemp` for the *shipped* matrix, and `finally` removes the root even on crash | `:78` (0700 mkdtemp) + relative-only fixture names | default run left no `/tmp/kasegi-r23-c1-*`; crash runs also cleaned |
| G4 | The frozen matrix contains no absolute names, no `..` segments, and every symlink target is `@ROOT@`-prefixed | script audit of every `dirs`/`files`/`symlinks` key | `unsafe entries: none`, 13 cases |
| G5 | Escapes are pinned `GONE` and the 6/7 split is real | fixture data, not checker logic | `Counter({'control': 7, 'escape': 6})`, all six escape ids `expect=GONE` |
| G6 | Landed `c1-fixed.json` is content-bound to the production bytes | its `resolver_sha256`/`matrix_sha256` equal the independently measured shas above | `ed9a9dae…` / `5e61a33e…`, totals 13/13; `c1-baseline.json` `d6a3c3f1…`, 7/13 |

**Net reading for C1's evidence.** The landed receipt is honestly bound to the production
`resolve.py` bytes, and the matrix is not vacuous (a do-nothing baseline scores 7/13). What it does
**not** establish is containment: F3 shows the verdict is self-reported and path-blind, so the
receipt's 13/13 must be read as "these sha-pinned bytes classified these 13 cites as expected", with
the containment predicates carrying the argument from source review (`bounty_suffix` exact-root
boundary, `under_mirror` realpath check), not from this instrument.

## Scope limits

- Attacked `mirror-containment-check.py` and the frozen matrix only. I did **not** audit
  `resolve.py`'s two containment predicates, the fixture matrix's semantic adequacy, or the C2
  snapshot/quote artifacts — sibling seats own those; my mutation of the checker is one scratch line
  (`TIMEOUT_S`) and is shown as a diff.
- Hostile resolver is in scope *as a trust boundary question*, not as an intrusion: all probes ran
  against `/tmp` scratch, `/etc/hostname` was the only host file touched (read), and the deleted
  file was one I created in scratch (`$S/victimdir/victim.txt`).
- Not exercised: read-only filesystems, `--json` aimed at a symlink/`/dev/full`, umask variants,
  in-place mutation of fixtures *during* the 0.23 s run (F7's TOCTOU is by inspection, not a
  demonstrated race), `TMPDIR`-set host, and behaviour under a non-CPython `sys.executable`.
- Read-only compliance: the single file written by me is this report. No git/jj command was run, no
  lane or sibling-lane file was touched, no install or host configuration was performed. Scratch
  `/tmp/kasegi-r23-falsify-SentinelChecker/` (256 K) existed at write time but is not durable (see
  the header); the report is self-contained because each finding inlines its command and output.
  The one artifact my traversal probe dropped directly in `/tmp` (`/tmp/escape-rel.txt`) was removed
  after capture.
- No admission, score, or claim-status movement is asserted here.
