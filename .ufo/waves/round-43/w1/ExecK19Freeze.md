# ExecK19Freeze — kasegi round 43 (leaf executor)

**Assignment.** Deliver the K19 limb for `corpus/instruments/r43-closure.sh`: RD42-6 class, the freeze
record must not predate the evidence it freezes. Deliverable is a sourceable limb plus its transcript and
the exact freeze-record format; no suite, no C2, no other check was touched.

## Deliverables

| file | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-43/w1/ExecK19Freeze.sh` | 247 | `75f9552ec4958905b76c33f154ecaf0cdd099426d8bd0b321846167d8539e52f` |
| `.ufo/waves/round-43/w1/ExecK19Freeze.transcript.txt` | 332 | `b4c7e5682f522f15d00236daef3241b04082f73751611587e6eab11ddf6c3cc5` |
| `.ufo/waves/round-43/w1/ExecK19Freeze.freeze-format.txt` | 32 | `7981e242f9bb6566b580003184860bd5d08ca3068106ed90bd2e7e9ef1ac5a71` |

`ExecK19Freeze.sh` is the landable limb (the L1 drops its `check_k19` into the suite); the transcript and
format file are evidence/spec, not suite code.

## Review rounds (RevK19 attacked this limb twice; both rounds' findings were real and were fixed)

**Round 1** — limb `b9b6d387…` (209 lines):

| finding | change | evidence |
|---|---|---|
| claims with `round=42/44` or `lane=souji` and a regenerated digest passed | relation (0): `claims.round` is the JSON **integer** 43 and `claims.lane == "kasegi"`, folded into `order` | `m-round42`, `m-lane-souji` → `order=bad,sha=match closed=0` |
| `controls.c2 := controls.c1` collapsed the two controls into one file | (1) resolves both paths and requires two distinct real paths | `m-alias` (their construction: alias + label 16:32:23 + coherent digest) → red |
| a label after the containing commit (17:10:00Z) was accepted | optional relation (6): `check_k19 <export> [<commit-utc>]` bounds `frozen-at` by the export ref's committer instant | `m-future` with `16:37:11Z` → red |
| the receipt quoted a fabricated `bash -n: ok` line | transcript records the real `bash -n` result: 0 bytes, `rc=0` | transcript §E |

**Round 2** — limb `8e6b124f…` (243 lines); all five assigned classes behaved, two new defects found:

| finding | change | evidence |
|---|---|---|
| F7: `check_k19 <export> ""` silently disabled relation (6), contradicting the promised "unparseable bound is a red" | the argument count is passed into the check; **supplied but empty** is now `commit_bound_ok = False` → red, with the true `freeze=present` payload | transcript: `check_k19 $S/live ""` → `freeze=present,order=bad,sha=match closed=0`, rc 1 |
| F8: `claims.round = 43.0` (JSON float) passed `43 == 43.0` | identity uses `type(...) is int`, so `43.0` and `true` are refused | `m-round-float` → `order=bad,sha=match closed=0` |
| F9/F11 (residual): a coherent rewrite of claims+record+controls, and a shape-only `base` (40 zeros with matching claims), are accepted | inherent to an internal digest; **not** claimed as forgery-proof — stated under Risks | — |
| F10 (residual): relation (6) is caller-trusted: one-arg accepts a post-commit label, a lax bound (2030) passes | stated in integration constraint 1: the bound must be the Z-normalized committer instant of the graded ref; only that formula is correct | transcript shows the one-arg gap explicitly |
| F12 (integration): under `set -euo pipefail` a bare `check_k19` returning 1 aborts the caller | stated in integration constraint 2: call it in an `if`/`||` position or avoid `errexit` | — |

## Interface

Sourceable, silent at source time, defines exactly one function:

```
$ bash -c 'source .ufo/waves/round-43/w1/ExecK19Freeze.sh >/dev/null; declare -F | wc -l; declare -F check_k19'
1
check_k19
```

`check_k19 <export-root> [<commit-utc>]` prints exactly one line and returns its status:

```
K19 payload=freeze=<present|absent>,order=<ok|bad>,sha=<match|mismatch> closed=<0|1>
```

- return 0 when `closed=1`, return 1 when `closed=0` — it never `exit`s:
  `check_k19 $S/base 2026-10-28T16:27:52Z >/dev/null; echo survived-rc=$?` → `survived-rc=1`, then
  `caller-alive`.
- no argument / non-directory argument → `freeze=absent,order=bad,sha=mismatch closed=0`, rc 1.
- `<commit-utc>` optional; when **supplied** it must be ISO 8601 Z — empty or malformed is a red, never a
  skipped bound.
- runs under a caller's `set -u`; reads **only** bytes under the export root (no git call, no lane work-tree
  read), so `committed` is carried by the export itself.

## What K19 grades (all over the same export)

Paths: `claims = .ufo/waves/round-43/claims.json`, `freeze = .ufo/waves/round-43/freeze.txt`, and the two
control receipts named by `claims.controls.c1` / `.c2` (must be relative, resolve inside the export;
absolute paths and `..` escapes are refused).

0. the claims are this round's: `round` is the JSON integer 43 and `lane == "kasegi"`;
1. each control receipt carries **exactly one** `measured-at=<ISO-Z>` line that parses as
   `YYYY-MM-DDThh:mm:ssZ` (calendar-valid, second precision, literal `Z`), and the two controls are two
   distinct files;
2. `claims.frozen_at_utc` is not earlier than the latest of those measurements;
3. `claims.frozen_at_utc` equals the committed record's `frozen-at=` label;
4. the record is exactly four lines in the documented order (`frozen-at`, `measured-at-max`, `claims-sha256`,
   `base`) with valid `<iso-z>`/`<hex64>`/`<hex40>` shapes, `measured-at-max` equals the latest control
   measurement, and `base` equals `claims.base`;
5. `claims-sha256` is the SHA-256 of the `claims.json` bytes read from the same export;
6. when `<commit-utc>` is supplied, `frozen-at` is not later than that instant.

`closed=1` only when `freeze=present`, `order=ok`, `sha=match`. A malformed record (wrong line count, wrong
key order, non-ISO label) fails closed: `order=bad`, and with no parseable record `sha=mismatch`.

## Evidence (commands and their real output; full transcript in the deliverable)

Record and inputs, from the live lane commit `4cb6d4ae768481e1a14afbedc2d865a060ebacfd` export:

```
$ cat live/.ufo/waves/round-43/freeze.txt
frozen-at=2026-10-28T16:37:07Z
measured-at-max=2026-10-28T16:34:15Z
claims-sha256=a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630
base=ab98fac9dce87130bc4f66de89e30650d63943dc
$ sha256sum live/.ufo/waves/round-43/claims.json
a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630
$ grep -n '"lane"\|"round"\|"frozen_at_utc"\|"c1"\|"c2"' live/.ufo/waves/round-43/claims.json
2: "lane": "kasegi",
3: "round": 43,
6: "frozen_at_utc": "2026-10-28T16:37:07Z",
74:  "c1": ".ufo/waves/round-43/c1-controls/do-nothing.txt",
75:  "c2": ".ufo/waves/round-43/c2-controls/before.txt"
$ grep -n 'measured-at=' live/.../c1-controls/do-nothing.txt live/.../c2-controls/before.txt
…/c1-controls/do-nothing.txt:2:measured-at=2026-10-28T16:32:23Z
…/c2-controls/before.txt:2:measured-at=2026-10-28T16:34:15Z
```

Export/ref times (`date -u -d @$(git … show -s --format=%ct <ref>) +%Y-%m-%dT%H:%M:%SZ`):
`ab98fac9… 2026-10-28T16:27:52Z`, `4cb6d4a… 2026-10-28T16:37:11Z`.

```
$ check_k19 $S/base 2026-10-28T16:27:52Z; echo rc=$?      # no .ufo/waves/round-43 at base
K19 payload=freeze=absent,order=bad,sha=mismatch closed=0
rc=1
$ check_k19 $S/live; echo rc=$?
K19 payload=freeze=present,order=ok,sha=match closed=1
rc=0
$ check_k19 $S/live 2026-10-28T16:37:11Z; echo rc=$?
K19 payload=freeze=present,order=ok,sha=match closed=1
rc=0
```

Mutant trees (each a copy of the live `.ufo/waves/round-43` subtree under scratch with one edit; the exact
`diff -u` / `grep` / `stat` behind each is in transcript §D):

| mutant | edit | K19 line | rc |
|---|---|---|---|
| `m-early` | `frozen-at=2026-10-28T16:30:00Z` (< control max 16:34:15Z) | `order=bad,sha=match closed=0` | 1 |
| `m-late-baddigest` | label kept (`16:37:07Z`), `claims-sha256` first nibble `a→f` | `order=ok,sha=mismatch closed=0` | 1 |
| `m-dupe-measured` | c1 gains a second `measured-at=` line | `order=bad,sha=match closed=0` | 1 |
| `m-offset` | `frozen-at=2026-10-28T08:00:01-03:00` (r42 offset form) | `order=bad,sha=match closed=0` | 1 |
| `m-missing-line` | record loses its `base=` line | `order=bad,sha=mismatch closed=0` | 1 |
| `m-label-drift` | `frozen-at=2026-10-28T16:37:08Z` | `order=bad,sha=match closed=0` | 1 |
| `m-max-drift` | `measured-at-max=2026-10-28T16:34:16Z` | `order=bad,sha=match closed=0` | 1 |
| `m-badjson` | `claims.json` replaced by `{` | `order=bad,sha=mismatch closed=0` | 1 |
| `m-noclaims` | `claims.json` removed | `order=bad,sha=mismatch closed=0` | 1 |
| `m-round42` | `"round": 42`, digest regenerated | `order=bad,sha=match closed=0` | 1 |
| `m-round-float` | `"round": 43.0`, digest regenerated | `order=bad,sha=match closed=0` | 1 |
| `m-lane-souji` | `"lane": "souji"`, digest regenerated | `order=bad,sha=match closed=0` | 1 |
| `m-alias` | `"c2": …c1-controls/do-nothing.txt`, label and `measured-at-max` `16:32:23Z`, digest regenerated | `order=bad,sha=match closed=0` | 1 |
| `m-future` | label and `frozen_at_utc` `17:10:00Z`, digest regenerated, bound `16:37:11Z` | `order=bad,sha=match closed=0` | 1 |
| `m-future`, no bound | same tree, one-argument call | `order=ok,sha=match closed=1` | 0 |

Digest isolation holds: `m-early`/`m-dupe-measured`/`m-offset`/`m-label-drift`/`m-max-drift`/`m-round42`/
`m-round-float`/`m-lane-souji`/`m-alias`/`m-future` keep `sha=match` and fail on ordering/identity only;
`m-late-baddigest` keeps `order=ok` and fails on the digest only. Transcript tally: `red-cases=15
green-cases=3`.

Bound-edge behaviour (transcript §E):

```
$ check_k19 $S/live ""; echo rc=$?                    # supplied but empty
K19 payload=freeze=present,order=bad,sha=match closed=0
rc=1
$ check_k19 $S/live 2026-10-28T13:37:11-03:00; echo rc=$?   # offset form, not Z
K19 payload=freeze=present,order=bad,sha=match closed=0
rc=1
```

Syntax/contract, with the real `bash -n` result (it prints nothing):

```
$ bash -n .ufo/waves/round-43/w1/ExecK19Freeze.sh; echo rc=$?
rc=0
$ bash -n .ufo/waves/round-43/w1/ExecK19Freeze.sh 2>&1 | wc -c
0
```

## Integration constraints for the L1

1. **Call the two-argument form, with a Z-normalized instant.**
   `check_k19 "$EXPORT" "$COMMIT_UTC"` where
   `COMMIT_UTC=$(date -u -d "@$(git -C "$LANE" show -s --format=%ct "$EXPORT_REF")" +%Y-%m-%dT%H:%M:%SZ)`.
   `%cI` verbatim (offset form) and an empty value are both red by design. One argument still grades
   relations (0)–(5), but a forged future label (`m-future`) is accepted, as the transcript shows.
2. **Call it in an `if`/`||` position.** The limb returns 1 for a red; under `set -euo pipefail` a bare call
   would abort the suite and a `$(…)` capture would swallow the line.
3. **`claims.json` bytes are pinned by the record.** `freeze.txt` carries
   `claims-sha256=a4c03e1e…a6630` over the current `claims.json`. Any later edit to that file — including an
   appended `errata` entry — makes the digest mismatch and turns K19 red at Y. Either keep the claims bytes
   identical or regenerate line 3 of the record (a re-freeze must also keep `frozen-at` ≥ every control
   `measured-at` and ≤ the commit instant).
4. **`freeze.txt` shape is exact.** Four lines, `frozen-at`, `measured-at-max`, `claims-sha256`, `base`, in that
   order, no extra or blank lines, LF, trailing newline. The committed record satisfies it.
5. **K19 is red at base for the right reason**: base `ab98fac9` has no `.ufo/waves/round-43` at all, so the
   payload is `freeze=absent,…` — K19 is one of the six checks the base run must leave open.
6. A selftest case for K19: positive = live export (green); mutant = the same tree with `freeze.txt` rewritten
   to `m-early`'s label (`16:30:00Z`), or the claims of `m-round42`, both red; verdict pass.

## Not run here (out of scope, owned elsewhere)

- the full `r43-closure.sh` run/selftest at Y (instrument does not exist yet; `ExecSuiteSkeleton` owns it);
- the C2 claim-package gate and its fixtures;
- no mutating git/jj command was issued anywhere; exports used read-only `git archive` only, and no fixture
  repository was created (no throwaway git identity used).

## Tooling and scratch

- No install or upgrade was needed: `bash`, `python3`, `git`, `tar`, `sha256sum`, `diff`, `od`, `stat`, `cmp`,
  `date`, `wc` were already present. Nothing was written to any PATH directory or to the fleet root.
- Lane writes were confined to `.ufo/waves/round-43/w1/`; `git -C <lane> status --porcelain` shows only
  untracked `w1/` plus siblings' own files.
- Scratch `/fast/scratch/hyaku/kasegi-r43/ExecK19Freeze/` (two full exports + fourteen mutant subtrees) is
  removed before this seat yields; no scratch lives in `/tmp`, none in the lane.

## Risks

- **K19 is not forgery-proof.** The digest binds the record to the claims bytes; a coherent rewrite of
  claims+record+controls (RevK19's F9) and a shape-only `base` with matching claims (F11) pass. The check
  grades internal consistency and ordering, not history.
- Relation (6) is only as good as the caller's bound: one argument leaves the future-label class ungraded,
  and a wrong (e.g. far-future) bound weakens it (F10). The receipt names the one correct formula.
- The strict four-line record shape and exact key order are a deliberate lock; they are documented in
  `ExecK19Freeze.freeze-format.txt` and the committed record conforms.
- `freeze=absent` always carries `sha=mismatch` because an absent record cannot match a digest — fail-closed
  by design, and it is what the base run prints.
- Identity assertions are literal (`round == 43` integer, `lane == "kasegi"`). If the suite is ever reused for
  another round those constants must move with it — a stale round number turns K19 red, never green.
