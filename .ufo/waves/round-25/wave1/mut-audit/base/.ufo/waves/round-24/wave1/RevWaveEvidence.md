# RevWaveEvidence — round-24 wave evidence (claims, counter-A before, baseline resolver)

Seat: read-only reviewer. No production file, lane git state or sibling repo was modified.
No tool was installed. All runs below are read-only (`source-recheck.py`,
`resolve-dispatch-check.py` with `--json` omitted).

## Findings (severity order)

### H1 — The declared freeze time is provably false; nothing else in the artifact set orders claims before receipts

`claims.json` declares `"frozen_at_utc": "2026-10-25T00:00:00Z"`. Its own inode:

```
$ stat -c '%n inode=%i mtime=%y ctime=%z' .ufo/waves/round-24/claims.json
... mtime=2026-10-25 04:09:47.804761115 -0300 ctime=2026-10-25 04:09:47.804761115 -0300
$ date -u -d '2026-10-25 04:09:47.804761115 -0300' +%FT%TZ
2026-10-25T07:09:47Z
```

`ctime == mtime` rules out a later `utimensat`/`touch -d` backdate (either would push
ctime to the tamper time), and a `cp -p` copy would leave ctime > mtime. So the inode was
created/written at **07:09:47Z**, i.e. the file did not exist at the declared
00:00:00Z — seven hours earlier. The one field that would have bound the claim to a
pre-collection moment is therefore a label, not evidence.

Relative order of file *writes* does exist and does favour the claim
(claims 07:09:47.805 → baseline copy 07:09:55.734 → counter-A receipt 07:09:56.021,
all `-0300`), but write order is not run order: a writer can run the counter, author the
claim, then 8 s later paste the captured stdout into the receipt. That is exactly the
shape of this artifact set.

What would actually prove ordering (none present):
1. `claims.json` committed as a git object **whose commit is an ancestor of** the commit
   that contains the receipts (committer date + object hash chain), or
2. the receipt carrying `sha256(claims.json)` plus its own argv, cwd, UTC stamp and the
   `sha256` of the manifest it read, so a reader can prove the counter ran *under* the
   frozen claim, or
3. an append-only, sequence-numbered log holding both.

Present receipt: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/c1-counterA-before.txt`
is 282 bytes, 8 lines of `name <code>` — no claim id, no command, no cwd, no timestamp,
no `sha256` of claims or manifest. It cannot bind itself to any claim.

### H2 — Counter A reaches the after-target (8/8 exit 0) from any wrong cwd, with zero captures

`claims.json` runs the recheck lines through `bash -c "$r"` where `$r` comes from

```
r=$(grep -m1 '^recheck: ' corpus/knowledge/$f.md | sed 's/^recheck: //')
```

`corpus/knowledge/...` is relative. Away from the lane root the grep fails, `$r` is empty,
and **`bash -c ""` exits 0**, so every entry scores a pass:

```
$ mkdir -p /tmp/rwe-elsewhere && cd /tmp/rwe-elsewhere
$ for f in cvss-v4-severity-and-vector coordinated-disclosure-timelines ... cra-manufacturer-reporting-duties; do
    r=$(grep -m1 '^recheck: ' corpus/knowledge/$f.md | sed 's/^recheck: //'); bash -c "$r" >/dev/null 2>&1; echo "$f $?"; done
cvss-v4-severity-and-vector 0
... all eight 0 ...
$ bash -c ""; echo "rc=$?"
rc=0
```

That is 8/8 — the C1 after-target — achieved by standing in the wrong directory, i.e. the
counter is gameable without adding a single capture. The same hole reverses for the
"before": the five unanchored recheck lines are *also* cwd-dependent in the other
direction, and CPython's missing-script exit code is 2:

```
$ cd /tmp && python3 corpus/instruments/source-recheck.py --manifest ... --source S001 >/dev/null 2>&1; echo $?
2
$ ... 2>&1 | tail -1
python3: can't open file '/tmp/corpus/instruments/source-recheck.py': [Errno 2] No such file or directory
```

`source-recheck.py` exits 2 for `reason=not-listed` **and** for invalid-path,
invalid-sha256, missing-quotes, missing, unreadable, not-utf8, manifest-missing and
invalid-source-id (13 `return 2` sites, `corpus/instruments/source-recheck.py:81-161`).
With `>/dev/null 2>&1` the receipt cannot tell "defect present" from "command never ran".

**Answer to Q4: yes, cwd decides the score, and the counter MUST run from the lane root.
`claims.json` does not say so** — `grep -niE 'cwd|working directory|lane root|cd '` over
`claims.json` returns no match (rc=1), and neither the receipt nor `wave1-spec.json`
states a cwd. Of the eight recheck lines, F01–F05 (`cvss-v4…`, `coordinated-disclosure…`,
`authorization-safe-harbor…`, `ai-assisted-finding-validation`, `cwe-top25-2025…`) are
bare-relative; F06–F08 (`multiparty…`, `cna-assignment…`, `cra-manufacturer…`) carry
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`, which is why only the last three
survive a foreign cwd.

Minimal fix: anchor the counter for real —
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 99` as the first statement, read
the row with `grep -m1 '^recheck: ' "corpus/knowledge/$f.md" || { echo "$f NOROW"; continue; }`,
and fail on empty `$r` (`[ -n "$r" ] || { echo "$f EMPTY"; continue; }`) — then a missing
file can never be scored as a pass.

### H3 — The round-24 evidence is not committed, so the C1 kill rule cannot be satisfied as written

```
$ git -C .../kasegi-shokunin status --porcelain
 M corpus/instruments/citation-survival.md
 M corpus/instruments/citation-survival.tsv
 M corpus/instruments/resolve.py
?? .ufo/waves/round-24/
?? corpus/instruments/resolve-dispatch-check.py
?? corpus/instruments/resolve-dispatch-fixtures.json
$ git ls-files '.ufo/waves/round-24*' | wc -l
0
$ git ls-files '.ufo/waves/round-23*' | wc -l
104
```

Zero round-24 files are tracked (round 23 has 104), and both counter-B instruments are
untracked. C1's `kill_rule` requires "either counter is not reproducible from committed
bytes by one command" → C1 is not claimed. Either commit `claims.json`, both receipts, the
baseline copy and both counter-B instruments before scoring, or rewrite the rule to say
"tracked bytes" and accept that the receipts are mutable working-tree files. Nothing in
`.gitignore` excludes them (`git check-ignore` rc=1) — they are simply uncommitted.

### M1 — Q2 verified: the baseline byte-copy genuinely is the r23 final resolver

```
$ sha256sum .ufo/waves/round-24/c1-baseline-resolver.py
690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d
$ git show c2480b143120364728b40397926ffcf30a7309c8:corpus/instruments/resolve.py | sha256sum   # master tip, r23 verifier commit
690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d
$ git show d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a:corpus/instruments/resolve.py | sha256sum   # claimed base
690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d
```

Same digest at `master` (`c2480b1`), at the claimed base (`d0a3f6a`, confirmed an ancestor
of master via `git merge-base --is-ancestor`), at the working tree when sampled, and in
the copy. Behavioural confirmation — the copy fails exactly the four liveness cases and the
patched tree passes all eight:

```
$ python3 corpus/instruments/resolve-dispatch-check.py --resolver .ufo/waves/round-24/c1-baseline-resolver.py --fixtures corpus/instruments/resolve-dispatch-fixtures.json
resolver_sha256=690153ad... ; cases=8 pass=4 exit=1
$ python3 corpus/instruments/resolve-dispatch-check.py --resolver corpus/instruments/resolve.py --fixtures corpus/instruments/resolve-dispatch-fixtures.json
resolver_sha256=035f8844... ; cases=8 pass=8 exit=0
```

Timing supports "before": at my first sample the tree still hashed `690153…`; the tree copy
became `035f8844…` at `mtime=2026-10-25 04:14:32 -0300` (07:14:32Z), ~4m36s *after* the
receipt at 07:09:56Z. The baseline copy is a genuine pre-edit byte-copy, not a copy of the
patched file.

### M2 — Q3: the before receipt matches routed defect 1 at the exit-code level, not at the reason level

F01–F05 map to the first five filenames in `corpus/README.md:198-202`; the receipt lists
them in the claim's order with `2,2,2,2,2,0,0,0`. Re-running the exact counter at the lane
root is byte-identical:

```
$ diff <(re-run) .ufo/waves/round-24/c1-counterA-before.txt && echo BYTE_IDENTICAL
BYTE_IDENTICAL
$ sha256sum .ufo/waves/round-24/c1-counterA-before.txt
c5154b2d64332bc786ec3ac183c24c3c4d4e37e87c8fd7818afd58ca3e5f4ce8
```

"not-listed" is directly evidenced only for the first id of the first chain:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S001
S001:source UNAVAILABLE reason=not-listed      rc=2
```

and the manifest provably holds none of S001–S015 (4 records total, min `S018`, max `S031`,
`sha256 e06aa3cd…`), so every cited id is absent and the label holds. Two caveats a scorer
must not paper over:
- the receipt records **no reason string**, and exit 2 is overloaded (H2);
- the recheck lines are `&&`-chains, so only the first absent id per entry is observable —
  a later `present-but-mismatched` source (exit 1) would be masked behind an earlier
  exit 2. The receipt therefore proves "each of these five entries fails, first failure =
  absent id", not "S001…S015 are each not-listed".
Precise wording, and the strongest form the evidence supports: *F01–F05 exit 2, with the
first cited id per entry confirmed `not-listed` against a manifest whose id set is
S018–S031*.

### L1 — Counter B has no before receipt, and its instrument post-dates the freeze

`ls .ufo/waves/round-24/*counter*` returns only `c1-counterA-before.txt`. Counter B's
`before_expected` ("4/8, exit 1 on frozen baseline resolver bytes") is asserted with no
committed record; the only two files that exist are the baseline bytes and the checker,
and the checker is untracked with `mtime=2026-10-25 04:14`, four minutes after the claim
was written. I ran it read-only and it reproduces the claim exactly (M1), but that run is
this reviewer's, not the wave's. A `c1-counterB-before.txt` should be written from the
baseline copy before the tree patch is scored.

### L2 — Matrix FAIL rows print `expect == actual`

```
FAIL  glob-dangling-first-match  expect=INTERNAL  actual=INTERNAL  method=glob  path=<CASE>/lane/refs/a-lure.md
```
No `problems=` text is printed, because the verdict is on the resolved *path*
(`mirror-containment-check.py`), not the class. A saved receipt cannot localise the failure
without re-reading the checker. Print the expected path (or the failing component) on FAIL.

## Residual risk / verification gaps

- Could not verify any claim about *when the counter first ran*: no run log, no shell
  history for the L1 seat, no signed artifact. H1 is therefore "the declared freeze time is
  false and no substitute binder exists", not "the claim was authored after the receipt" —
  the latter remains UNVERIFIED in either direction.
- The 07:09:47Z → 07:09:56Z write ordering, plus the `resolve.py` tree patch at 07:14:32Z,
  are consistent with an honest pre-edit state; they do not prove one.
- Live lane-tree edits observed during this review (`resolve.py` patched, `citation-survival.tsv`
  cut from 1480 lines to 81 bytes at 04:14:44 -0300) are the integrator's state, not mine; I
  did not evaluate them. They do mean counter A's *before* cannot be re-derived from the
  working tree any more — only the preserved baseline copy and the receipt carry it, which
  makes H3 (commit them) load-bearing rather than cosmetic.
- Nothing here evaluates C2, the Q1–Q6 gates, or the F09 entries.
