# RevC1Control — C1 counter A do-nothing control (round 24)

Seat: reviewer. Scope: C1 counter A only (frontier `recheck:` exit codes), do-nothing
control plus every cheap route to 8/8 that creates no capture. Counter B (resolve
dispatch) not run — out of item.

## Verdict, stated plainly

1. **The do-nothing control is correct: 3/8, exactly as `claims.json` predicts.** It is
   reproducible from committed bytes by the claim's own command, on both the `/tmp`
   export and the live lane working tree, with no write to either.
2. **The after-target 8/8 is reachable with zero new capture bytes, by four independent
   routes.** Counter A reads only the exit status of a command the entry authors about
   itself; it never checks that the command names the entry's own sources. Rewriting the
   five `recheck:` lines alone produced `8/8` four different ways. **So `8/8` on counter A
   is not, by itself, receipt that C1 was done.** This is a measurement defect in the
   target, not a defect in `source-recheck.py`.
3. The strict kill-rule clause ("met by the do-nothing control receipt") is **not**
   triggered: unchanged entries + unchanged manifest stays at 3/8. What fails is the
   target's validity, not its reproducibility.
4. Counter A's own command is **not errexit-safe** and **discards every diagnostic** it
   produces. Details in findings 2 and 3.

## Provenance of the bytes

```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse master
c2480b143120364728b40397926ffcf30a7309c8      # lane tip (round-23 spot-check commit)

git archive c2480b14… | tar -x -C /tmp/kasegi-r24-RevC1Control-export
sha256 /tmp/kasegi-r24-RevC1Control-export/corpus/source-snapshots/round-23/manifest.json
e06aa3cdf65f316e6718342ed5dc03e289fd0132149f22c632225f3fbed0eeba
```

Manifest used for the whole control (unchanged throughout, except where an attempt
explicitly says otherwise): **`e06aa3cdf65f316e6718342ed5dc03e289fd0132149f22c632225f3fbed0eeba`**,
records `S018, S029, S030, S031`. At the baseline export no `S001`–`S015` capture existed
anywhere in the lane (`find . -name 'S0[01][0-9].txt'` returned only
`./corpus/source-snapshots/round-23/S018.txt`). Writer seats landed
`corpus/source-snapshots/round-24/S001.txt … S015.txt` at 04:15 mid-seat — see the closing
section; it does not change any measurement above, all of which were taken on the export.

## Baseline: the exact counter command from claims.json

Command, verbatim from `claims.json` `counter_A.command`, cwd = repo root:

```sh
for f in cvss-v4-severity-and-vector coordinated-disclosure-timelines authorization-safe-harbor-and-scope ai-assisted-finding-validation cwe-top25-2025-methodology multiparty-vulnerability-coordination cna-assignment-and-vulnerability-rules cra-manufacturer-reporting-duties; do r=$(grep -m1 '^recheck: ' corpus/knowledge/$f.md | sed 's/^recheck: //'); bash -c "$r" >/dev/null 2>&1; echo "$f $?"; done
```

Output, identical in `/tmp/kasegi-r24-RevC1Control-export` and in the lane working tree:

```
cvss-v4-severity-and-vector 2
coordinated-disclosure-timelines 2
authorization-safe-harbor-and-scope 2
ai-assisted-finding-validation 2
cwe-top25-2025-methodology 2
multiparty-vulnerability-coordination 0
cna-assignment-and-vulnerability-rules 0
cra-manufacturer-reporting-duties 0
```

**3/8 exit 0.** Matches `counter_A.before_expected` exactly.

### stderr of the five failures: empty, every one

Re-running each entry's `recheck:` line with both streams captured:

```
cvss-v4-severity-and-vector            CODE=2  STDOUT: S001:source UNAVAILABLE reason=not-listed   STDERR: []
coordinated-disclosure-timelines       CODE=2  STDOUT: S003:source UNAVAILABLE reason=not-listed   STDERR: []
authorization-safe-harbor-and-scope    CODE=2  STDOUT: S006:source UNAVAILABLE reason=not-listed   STDERR: []
ai-assisted-finding-validation         CODE=2  STDOUT: S009:source UNAVAILABLE reason=not-listed   STDERR: []
cwe-top25-2025-methodology             CODE=2  STDOUT: S013:source UNAVAILABLE reason=not-listed   STDERR: []
```

The three passing entries print `S018|S031|S029:sha256 OK` plus per-quote `OK` lines and
also write nothing to stderr.

## Finding 1 (major) — 8/8 without creating any capture

Every attempt below changed **only** the five failing entries' `recheck:` lines inside a
throwaway copy of the export. No file was added under `corpus/source-snapshots/`, the
manifest stayed byte-identical (`e06aa3cd…`) unless stated. Each attempt is a control
that must fail; all four pass.

| # | attempt | `recheck:` line used for F01–F05 | counter A | hardened probe |
|---|---------|----------------------------------|-----------|----------------|
| A3 | point at the existing manifest, drop `--source` | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json` | **8/8** | 3/8 |
| A4 | cross-entry credit: every failing entry "verifies" F06's capture | `… --manifest …/round-23/manifest.json --source S018` | **8/8** | 3/8 |
| A5 | degenerate | `true` | **8/8** | 3/8 |
| A6 | instrument selftest as the evidence | `python3 corpus/instruments/source-recheck.py --selftest` | **8/8** | 3/8 |

A3 is the decisive one because it is *not* obviously degenerate: it runs the real
instrument against a real committed manifest containing real captures, and the whole
manifest verifies clean (`RC=0`, 36 `OK` lines = 4 digests + 32 quotes). It simply verifies **no source the five
entries cite**. The gap is structural: `recheck()` filters with
`record["id"] == source_id` and treats `--source` as optional, so an entry that omits it
verifies whatever the manifest happens to hold.

A4 is the same gap in its other direction: the entry can name an id that is not its own.
`corpus/README.md` rows 198–205 already carry the correct id set per entry
(`S001,S002` / `S003,S004,S005` / … / `S031` / `S029`), so the binding is available in the
repo and nothing checks it.

### Manifest-side route: an id the manifest does not capture

Manifest shaped (scratch dir, no capture added) to list `S001` bound to the already
committed `S018.txt` bytes:

```json
{"id":"S001","path":"S018.txt","sha256":<sha of S018.txt>,
 "quotes":[{"id":"cvss-vector-string","quote":" "}]}
```

`python3 …/source-recheck.py --manifest forged-permissive.json --source S001`
→ `RC=0`, `S001:sha256 OK`, `S001:cvss-vector-string OK`.
forged manifest sha256 `599354b154e33a72c64f3cac64afcbf81347dbc46d7d160d75f9d0707911d07e`.

The instrument validates a record only against itself: digest of *some* file plus a quote
found in *that* file. A one-space quote satisfies it. With the entry's real assertion in
the record instead, it fails closed as expected — `RC=1`,
`S001:cvss-vector-string MISMATCH reason=quote-not-found`, forged manifest sha256
`cdff9e71064a972fccd596df30862444836a439fa820d325565e73299ac00724`.

So the counter cannot tell a capture of S001 from any committed file relabelled S001.
Manifest `purpose` already declares the quote-to-location ceiling; it does **not** declare
that the id-to-file binding is equally self-declared.

## Finding 2 (major) — the counter destroys its own diagnostics, and hides 10 of 15 ids

`>/dev/null 2>&1` discards both streams, and `source-recheck.py` writes every diagnostic
to **stdout** (`emit(..., out)`), never to stderr. Therefore the claim's receipt is an
exit code with no reason attached: `2` cannot be told apart from *not-listed*,
*manifest missing*, *invalid-sha256*, *missing-quotes*, *outside-manifest-directory*, or
*dangling capture symlink* without re-running something the claim does not specify.

Also, the per-entry chains short-circuit. Five entries cite 15 ids; the `&&` chain stops
at the first failure, so today's receipt probes only 5 of them. Individually:

```
S001 … S015 — all 15:  RC=2  "<id>:source UNAVAILABLE reason=not-listed"
```

(S002, S004, S005, S007, S008, S010–S012, S014, S015 are never reached by the claim
command.)

## Finding 3 (minor) — the claim's command is not errexit-safe

With `set -e` / `bash -e` in force (the default in this harness's shell, and in most CI),
the same command produces **zero rows and exit 2**: the first non-zero `bash -c "$r"`
aborts the loop before the `echo`. Measured: `flags=none RC=0 rows=8`; `flags=(-e) RC=2
rows=0`. "Reproducible … by one command" therefore holds only under a non-errexit shell,
which the claim does not pin.

## What does hold (probed, all fail closed)

| probe | result |
|-------|--------|
| `--source s001` / `S1` / `S01` / `S001x` | `RC=2 … reason=not-listed` — exact string match, no prefix/case/glob alias |
| `--source 'S0*'` / `--source ''` | `RC=2 manifest:selection … reason=invalid-source-id` |
| manifest path is a dangling symlink | `RC=2 manifest UNAVAILABLE reason=missing` |
| record path escapes manifest dir (`../S018-copy.txt`, file exists) | `RC=2 … reason=outside-manifest-directory` |
| record `sha256` not 64 lowercase hex | `RC=2 … reason=invalid-sha256` |
| record with empty `quotes` | `RC=2 … reason=missing-quotes` |
| capture path is a dangling symlink | `RC=2 … reason=missing` |
| correct digest, quote absent from bytes | `RC=1 … MISMATCH reason=quote-not-found` |

The `--source` alias route named in the item **does not exist**; that attempt is
correctly refused. The three routes that succeed are id-dropping, id-substitution and
manifest relabelling.

## Recommendation — harden the counter before accepting 8/8

Keep the instrument; add the binding check the predicate already names. Probe
(`/tmp/kasegi-r24-RevC1Control-hardcheck.py`, 60 lines, sha256
`42f6cdf1c0793fc4a585813f2486b9e54e88b42cd76876b735e9e40b99ba9403`) reads
`corpus/README.md` frontier rows, and per entry requires:

1. the `recheck:` line's set of `--source <ID>` values **equals** the README source column;
2. every such id is listed exactly once in the manifest;
3. each record's `path` stem equals its id (`S001` → `S001.txt`) — kills relabelling;
4. every quote is a real assertion (≥8 chars, ≥2 tokens);
5. the command then exits 0.

Measured on the same trees:

| tree | counter A | hardened |
|------|-----------|----------|
| do-nothing export (`e06aa3cd…`) | 3/8 | **3/8** (baseline preserved) |
| A3 id-dropped | 8/8 | **3/8** |
| A4 cross-entry `--source S018` | 8/8 | **3/8** |
| A5 `true` | 8/8 | **3/8** |
| A6 `--selftest` | 8/8 | **3/8** |
| a7: F01 names S001+S002, `S001.txt`/`S002.txt` created | 4/8 | **4/8** (PASS path reachable; forged manifest sha256 `8f0d3ac141ba9a81c507328254cb65d8ddcdbec25a5f844b72a383f8c4320a0d`) |

The hardened rule set agrees with the plain counter on the do-nothing baseline, refuses
all four no-capture routes, and is satisfiable — the a7 probe shows the PASS path
executing end to end once one capture file per id exists. It cannot prove `S001.txt` holds CVSS text rather than a copy of `S018.txt`;
that residual is the ceiling the manifest `purpose` already declares, and it must stay
declared rather than claimed.

Consequence for the round: shipping F01–F05 captures with `--source` ids and a manifest
record per id is what moves the axis. Rewriting five `recheck:` lines is not, and after
this control the two are indistinguishable under counter A as frozen.

## Working-tree movement observed mid-seat (not part of the control)

At 04:15 (after every measurement above was taken on the export) writer seats added
`corpus/source-snapshots/round-24/S001.txt … S015.txt` (S001 67354 B, S015 5696 B) and
modified `corpus/instruments/resolve.py`. **No `round-24/manifest.json` exists yet**, and no
entry's `recheck:` line changed (`git diff --name-only -- corpus/knowledge` → 0 files).

Re-running the exact counter command on the live lane tree after that:

```
cvss-v4-severity-and-vector 2
coordinated-disclosure-timelines 2
authorization-safe-harbor-and-scope 2
ai-assisted-finding-validation 2
cwe-top25-2025-methodology 2
multiparty-vulnerability-coordination 0
cna-assignment-and-vulnerability-rules 0
cra-manufacturer-reporting-duties 0
```

still **3/8**, with
`corpus/source-snapshots/round-23/manifest.json` = `e06aa3cd…` unchanged. Two facts for the
planner: (a) landing the capture bytes alone moves the counter by zero — the manifest record
and the entry's `--source` line are what the counter actually reads, consistent with
finding 1; (b) the id-dropping, cross-entry and `true` routes will each read 8/8 the moment
the five lines are rewritten, whether or not those new files are the right bytes. A
hardened counter as above is therefore a precondition for accepting this round's 8/8, and
its path-stem rule is already satisfiable against `round-24/`.

This run also confirms committed bytes (`master` = `c2480b1…`, `d0a3f6a…` present) are
pinned; the movement is working-tree only.

## Residual risk and gaps

- **Counter B not run** (item boundary). Nothing here bears on resolve.py brace/glob
  liveness.
- **UNVERIFIED:** whether the round-23 `S030` record (captured, no entry cites it) was
  meant to be superseded by `S031`; it does not affect counter A because no recheck line
  selects `S030`.
- **UNVERIFIED:** upstream authenticity of `S018/S029/S031` bytes — by design, the
  instrument verifies captured bytes only.
- No tool installed or upgraded. Scratch trees: `/tmp/kasegi-r24-RevC1Control-*`; the lane,
  `/home/vgpnk/Projects/shokuknow` and git/jj state were not modified. This report is the
  only file written in the lane.
