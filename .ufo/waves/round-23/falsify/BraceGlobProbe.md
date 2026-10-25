# BraceGlobProbe — round-23 falsify: brace / placeholder-glob expansion against C1

Seat: `L1Kasegi23.BraceGlobProbe-2` (leaf executor, read-only on the lane).
Target: § "Target" of the round-23 falsify dispatch — escape cases whose hit travels through
`{a,b}` brace expansion and through a `<...>` placeholder glob under the bounty, canonical-alias,
relative-mirror and relative-lane branches; replay on fixed and baseline bytes; report
expected-vs-actual class and whether realpath confinement holds on each hit.

Scratch (all writes confined here): `/tmp/kasegi-r23-falsify-BraceGlobProbe/`.
No production file, lane tree, git/jj state or sibling lane was written. `resolve.py` was never
executed against the lane repo, because it writes `corpus/instruments/citation-survival.tsv`
beside itself; every run below executes a byte-copied resolver inside a disposable fixture tree.

## Bytes under test (pinned; four artifacts were edited while this probe ran)

| artifact | as-of snapshot in scratch | sha256 |
|---|---|---|
| `corpus/instruments/resolve.py` (fixed) | `asof-resolve-fixed.py` | `8dd45bc8d9aedbb25247a64fbd6094a1b9e7b9a3b3facdb58001c59ef3868848` |
| `corpus/instruments/resolve.py` (superseded at 03:46:26; only change is that a *root-only* bounty suffix no longer maps to the mirror root, `resolve.py:237-243`) | `asof2-resolve-fixed.py` | `fce5b84be4cece914260f03a3a8b739dc1108381f97482bbfc7b22143810a4b0` |
| `.ufo/waves/round-23/c1-baseline-resolver.py` | `asof-resolve-baseline.py` | `d6a3c3f1a1d8e97d42d66a8aa3cb34530b7bc1c18b194e487ef8d580d869f903` |
| `corpus/instruments/mirror-containment-check.py` | `asof-checker-53742c8d.py` | `53742c8d9529dffb8c40c39b3448de7388b774b548d7831670598d5534bff5d1` |
| `corpus/instruments/mirror-containment-fixtures.json` (frozen matrix, 20 cases) | read in place | `4e39f65c7c1bdc7d6a390f0aeefe5fa88af67ea84659aa9ff36b84d271c2400b` |

Both resolver revisions were exercised: every case in all three matrices returns the same class on
`8dd45bc8…` and on `fce5b84b…` (`final-results-v3.json`, `final-results-v4.json`), and likewise
under both checker revisions. `c1-fixed.json` now names `fce5b84b…` and the frozen matrix
`4e39f65c…`. See "Drift" below: four artifacts were edited while this probe ran, so all evidence
here is tied to the byte copies listed above, not to the live paths.

## Matrices written (committed schema, accepted verbatim by `--fixtures`)

* `brace-glob-fixtures.json` — 17 cases, sha256 `28ef0f8bed7f1c0a8bbe3c4d59e3f95018c9f153b3d23aec6809cfbab4aeea0d`
  (7 escape, 10 control): brace/glob escapes through the bounty fallback, the relative-mirror
  fallback and the canonical-alias branch; brace/glob confined controls; a multi-match decoy pair;
  an absolute-path injection into the bounty suffix; and three direct-hit *parity* controls.
* `boundary-vacuum-fixtures.json` — 2 cases, sha256 `9ff92e2c5d0a9e32da0dedb98374a77b035e5715eb23442287c68ab81861e3f9`:
  the frozen traversal escape with and without the intermediate directory it walks through.
* `brace-empty-alt-fixtures.json` — 3 cases, sha256 `8ebd1a53922d96ea5acc6fae0461a344a80d8712f4a8db162d398ec0d0fc2f91`:
  the exact brace idiom cited at `SKILL.md:1000`, with an empty first alternative.

Replay command (per contract; each matrix × both byte-sets):

```
python3 corpus/instruments/mirror-containment-check.py \
  --fixtures /tmp/kasegi-r23-falsify-BraceGlobProbe/<matrix>.json \
  --resolver <resolver bytes>            # corpus/instruments/resolve.py | .ufo/.../c1-baseline-resolver.py
```

A second harness, `probe.py` / `final-probe.py`, rebuilds the same case trees and records the TSV
`method`, `domain`, `resolved_path` and a realpath-containment boolean per row
(`final-results-v3.json`), because the class column alone does not show whether a hit was
*confined* or merely *absent*.

## Results

`brace-glob-fixtures.json` — fixed **15/17**, baseline **12/17**.

| case (nature) | cite | fixed | baseline |
|---|---|---|---|
| `bounty-brace-direct-parity` (control) | ``~/Projects/bounties/{../outside.md,absent.md}:1`` | RESOLVES (brace) | RESOLVES (brace) |
| `bounty-brace-out-of-home-parity` (control) | ``~/Projects/bounties/{../../../escape-vault/leak.mjs,absent.mjs}:1`` | RESOLVES (brace) | RESOLVES (brace) |
| `bounty-glob-direct-symlink-parity` (control) | ``~/Projects/bounties/<name>.md:1`` | RESOLVES (glob) | RESOLVES (glob) |
| `bounty-fallback-brace-escape` (escape) | ``~/Projects/bounties/{../mirror-escape,keep}/note.md:1`` | **GONE** | MIRROR-EQUIVALENT ✗ |
| `bounty-fallback-glob-escape` (escape) | ``~/Projects/bounties/../<probe>/leak.md:1`` | **GONE** | MIRROR-EQUIVALENT ✗ |
| `bounty-fallback-glob-symlink-escape` (escape) | ``~/Projects/bounties/ops/<name>.mjs:1`` | **GONE** | MIRROR-EQUIVALENT ✗ |
| `relative-fallback-brace-escape` (escape) | ``{../../escape3,absent}/x.md:1`` | **GONE** | MIRROR-EQUIVALENT ✗ |
| `relative-fallback-glob-escape` (escape) | ``../../escape4/<name>.md:1`` | **GONE** | MIRROR-EQUIVALENT ✗ |
| `canonical-alias-brace-escape` (escape) | ``~/Projects/the-bounty-hunter/{../outside.md,absent.md}:1`` | **GONE** | GONE |
| `bounty-absolute-join-probe` (escape) | ``~/Projects/bounties//tmp/kasegi-r23-falsify-BraceGlobProbe/abs-probe.txt:1`` | **GONE** | GONE |
| `relative-brace-lane-escape-internal` (control) | ``{../root-escape,absent}/y.md:1`` | INTERNAL (brace) | INTERNAL (brace) |
| `bounty-fallback-brace-confined` (control) | ``~/Projects/bounties/ops/{absent,rank}.mjs:1`` | MIRROR-EQUIVALENT | MIRROR-EQUIVALENT |
| `bounty-fallback-glob-confined` (control) | ``~/Projects/bounties/ops/<name>.mjs:1`` | MIRROR-EQUIVALENT | MIRROR-EQUIVALENT |
| `relative-fallback-brace-confined` (control) | ``notes/{../moot.md,absent.md}:1`` | MIRROR-EQUIVALENT | MIRROR-EQUIVALENT |
| `relative-fallback-glob-confined` (control) | ``notes/<name>.md:1`` | MIRROR-EQUIVALENT | MIRROR-EQUIVALENT |
| `glob-multimatch-decoy-mask` (control) | ``~/Projects/bounties/sorted/<name>.mjs:1`` | **GONE** ✗ | MIRROR-EQUIVALENT (outside path) |
| `brace-multialt-decoy-mask` (control) | ``~/Projects/bounties/sorted/{a-lure,z-real}.mjs:1`` | **GONE** ✗ | MIRROR-EQUIVALENT (outside path) |

`boundary-vacuum-fixtures.json` — fixed **2/2**, baseline **2/2** (see F4).
`brace-empty-alt-fixtures.json` — fixed **0/3**, baseline **0/3** (see F2).

## Findings

### F1 — receipt/matrix consistency: stale for a five-minute window, then regenerated and now corroborated

At 03:45 the frozen matrix was **20 cases / `4e39f65c…`** while both wave receipts still pinned
**17 cases / `5c64e014…`**, so three cases (`brace-expansion-escape`, `glob-expansion-escape`,
`brace-expansion-confined-control`) had entered the matrix with no receipt covering them:

```
$ sha256sum corpus/instruments/mirror-containment-fixtures.json     # 03:45
4e39f65c7c1bdc7d6a390f0aeefe5fa88af67ea84659aa9ff36b84d271c2400b
$ python3 -c "import json;d=json.load(open('.ufo/waves/round-23/c1-fixed.json'));print(d['matrix_sha256'],d['totals'])"
5c64e0149f66d0261b561e271f0f5d4072b103f27ae4cea358d3e51cbed73e6e {'cases': 17, 'controls': 10, 'escape': 7, 'fail': 0, 'pass': 17}
```

At 03:47 both receipts were regenerated against `4e39f65c…`: fixed **20/20 pass, 0 fail**;
baseline **12/20 pass, 8 fail**. That baseline count is exactly what my independent replay of the
same 20-case matrix on the baseline bytes produced (`cases=20 escape=9 controls=11 pass=12 fail=8`,
all 8 failures `path_check=gone-with-path`), so the landed pair is now consistent and corroborated
from outside the L1's own runs. Standing guard, still falsifiable if the matrix is edited again:
`matrix_sha256` in both receipts must equal `sha256sum` of the frozen matrix and both must report
20 cases.

### F2 — the newly frozen `glob-expansion-escape` is non-discriminating: it passes on the knowingly-unsound baseline

```
$ python3 corpus/instruments/mirror-containment-check.py --fixtures corpus/instruments/mirror-containment-fixtures.json \
      --resolver .ufo/waves/round-23/c1-baseline-resolver.py
glob-expansion-escape                      escape  expect=GONE   actual=GONE   PASS
brace-expansion-escape                     escape  expect=GONE   actual=MIRROR-EQUIVALENT FAIL path_check=gone-with-path
```

The case materialises `relocated/outside-vault/x.md`, but its citation is
``~/Projects/bounties/<name>.md`` (fixtures.json, case `glob-expansion-escape`), whose two probes are
`<CASE>/home/Projects/bounties/*.md` and `<CASE>/relocated/tbh/*.md`. Neither pattern can match
`relocated/outside-vault/x.md`, and `home/Projects/bounties` does not exist in that case, so the
GONE is a *no-hit* GONE that any resolver produces. A fail-before/pass-after pair whose "before"
already passes carries no evidence that confinement works for globs.

The discriminating version I ran, with the outside file where the glob actually matches
(`bounty-fallback-glob-escape`: file at `relocated/probe/leak.md`, cite
``~/Projects/bounties/../<probe>/leak.md:1``), flips exactly as required: baseline
`MIRROR-EQUIVALENT` on `<CASE>/relocated/tbh/../probe/leak.md` (`path_check=gone-with-path`), fixed
`GONE`. Falsifiable: change the frozen case's file to `relocated/tbh/../outside-vault/x.md` (or move
the cite to include `../`) — the baseline must start failing it.

### F3 — realpath confinement holds for brace and glob hits on the mirror fallbacks (attacked, not breached)

All five brace/glob fallback escapes that the baseline credits outside the mirror are `GONE` on the
fixed bytes, and the probe confirms the mechanism is the containment predicate, not a missing file:

| case | baseline resolved path (credited) | realpath inside mirror? | fixed |
|---|---|---|---|
| `bounty-fallback-brace-escape` | `<CASE>/relocated/tbh/../mirror-escape/note.md` | no | GONE |
| `bounty-fallback-glob-escape` | `<CASE>/relocated/tbh/../probe/leak.md` | no | GONE |
| `bounty-fallback-glob-symlink-escape` | `<CASE>/relocated/tbh/ops/only.mjs` → `<CASE>/secret/sym.mjs` | no | GONE |
| `relative-fallback-brace-escape` | `<CASE>/relocated/tbh/../../escape3/x.md` | no | GONE |
| `relative-fallback-glob-escape` | `<CASE>/relocated/tbh/../../escape4/note.md` | no | GONE |

`under_mirror()` (`resolve.py:224-229`) is applied on both fallbacks (`resolve.py:241`, `:262`), and
it survives every expansion method I could construct: brace alt containing `..`, placeholder glob
before and after the traversal, glob match that is itself a symlink out, canonical-alias branch, and
empty-suffix (``~/Projects/bounties/``). The absolute-path injection
(`~/Projects/bounties//tmp/...`) is closed twice — by `lstrip("/")` in `bounty_suffix`
(`resolve.py:220`) and by `under_mirror` on the joined hit (probe: `join(mirror, suffix)` returned
`/tmp/kasegi-r23-falsify-BraceGlobProbe/abs-probe.txt`, exists, `under_mirror=False`).

### F4 — the frozen traversal escape is POSIX-fixture-sensitive; its escape is the *fallback*, not the direct hit

`boundary-vacuum-fixtures.json` replays the frozen cite
``~/Projects/bounties/../outside.md:1`` with identical bytes in the case root, twice:

* **without** `home/Projects/bounties` → **GONE** on both resolvers
* **with** `home/Projects/bounties` present → **RESOLVES** on both resolvers,
  `path=<CASE>/home/Projects/bounties/../outside.md`

POSIX cannot traverse a nonexistent component, so the GONE in the frozen `bounty-parent-traversal`
case is not produced by confinement at all; that case's fail-before/pass-after discrimination comes
entirely from its `relocated/outside.md` mirror-fallback hit. This is consistent with the now-frozen
controls `bounty-literal-present-traversal` and `bounty-literal-symlink-present`, which pin
`RESOLVES` for the direct branch. Not a defect — but the fixture pair is what makes the dependency
explicit, and every brace/glob *parity* case above reproduces the same class as those literal pins
(RESOLVES on both byte-sets, `method=brace` / `method=glob`), so expansion does not change the
direct-hit class.

### F5 — control preservation is incomplete: a valid confined match is suppressed when an escaping expansion sorts first

Fixed `GONE`, expected `MIRROR-EQUIVALENT`, verdict `missing-path`:

```
glob-multimatch-decoy-mask   control expect=MIRROR-EQUIVALENT actual=GONE FAIL verdict=missing-path
brace-multialt-decoy-mask    control expect=MIRROR-EQUIVALENT actual=GONE FAIL verdict=missing-path
```

Probe (`final-results-v3.json`, tree built by the same `build_case`):

```
globmatch <root>/relocated/tbh/sorted/a-lure.mjs  in_mirror=False real=<root>/secret/lure.mjs
globmatch <root>/relocated/tbh/sorted/z-real.mjs  in_mirror=True  real=<root>/relocated/tbh/sorted/z-real.mjs
exists_any(join)= ('glob', '<root>/relocated/tbh/sorted/a-lure.mjs')
classify= ('GONE', '', '', 'bounty')
```

Mechanism: `exists_any` (`resolve.py:179-195`) returns the **first existing** brace alternative
(`:186-187`) and only `matches[0]` of a sorted glob (`:192`); `classify` then applies `under_mirror`
to that single path and returns GONE when it fails (`resolve.py:240-242`) instead of trying the
remaining expansions. `z-real.mjs` is a genuine confined mirror byte; a sibling symlink that sorts
earlier masks it. The baseline "passes" the class only by crediting the escaping path — the current
checker flags it `path-outside-mirror-equivalent`, so baseline fails it too under the path column.
So C1's "preserve valid confined mirror controls" holds for **single-match** expansions (the four
controls above) and fails for multi-match ones. Falsifiable: iterating the expansion list and
crediting the first `under_mirror` hit flips both cases to MIRROR-EQUIVALENT without weakening any
escape case.

### F6 — an empty brace alternative silently disables the real file, on a live corpus citation

`SKILL.md:1000` cites ``~/Projects/bounties/ops/sighting{,-board,-dispatcher,-missions}.sh``.
`brace_expand` drops the empty alternative by design (`resolve.py:172`,
`# `{}` / `{,x}` empty alternative is not a resolvable expansion`), so `ops/sighting.sh` is never
probed:

```
brace_expand: [.../sighting-board.sh, .../sighting-dispatcher.sh, .../sighting-missions.sh]
sighting.sh exists at: True
exists_any: (None, None)
classify: ('GONE', '', '', 'bounty')
```

`brace-empty-alt-fixtures.json`: 0/3 on **both** resolvers (direct hit and mirror fallback, with the
file present at exactly the name the empty alternative denotes). Bash expands
`sighting{,-board}.sh` to `sighting.sh sighting-board.sh`, which is how the corpus line reads. This
is a detector false negative independent of C1 (identical baseline behaviour), and it depresses the
census numerator for a citation the lane actually ships. Falsifiable: keep the empty alternative
(`alt == ""` → also test the unsubstituted path) and the three cases must pass.

## Drift observed (the artifacts moved under this probe)

| time | artifact | sha256 | note |
|---|---|---|---|
| 03:27–03:38 | `resolve.py` | `ed9a9dae…` | matched `c1-fixed.json` when I started |
| 03:40:40 | `resolve.py` | `9e0b5751…` | `bounty_suffix` gained `lstrip("/")`, empty-suffix guard, `max(…, default=0)` |
| 03:42:37 | `resolve.py` | `8dd45bc8…` | current, equals my pinned snapshot |
| 03:28:25 | checker | `1bc2db10…` | class-only |
| 03:42:15 | checker | `fc9550f0…` | gained `resolved_path` + `path_verdict` |
| 03:43:0x | checker | `53742c8d…` | added `path_tolerance: carve-out` handling |
| 03:39→03:45 | fixtures | `5e61a33e…` → `5c64e014…` → `4e39f65c…` | 13 → 17 → 20 cases |
| 03:46:26 | `resolve.py` | `fce5b84b…` | root-only bounty suffix no longer maps to the mirror root; no probe case has an empty suffix, classes unchanged |
| 03:47 | `c1-fixed.json`, `c1-baseline.json` | — | both regenerated against `4e39f65c…` (20 cases); baseline 12/20 matches my independent replay exactly |

My matrices were re-run after each change; the fixed/baseline class per case is unchanged across
both resolver revisions and both checker revisions. The 17-case receipts I first read
(`5c64e014`, resolver `8dd45bc8`) were superseded at 03:47 by 20-case receipts
(`4e39f65c`, resolver `fce5b84b`); the numbers above are the superseded pair only where F1 says so.

## Scope limits

* Realpath cannot see **bind mounts / overlayfs** inside the mirror; that vector is untestable here
  (host package/service/mount operations are paused by the wave tooling rule) and is not covered by
  any case, including mine.
* `glob` through a magic component into `..` (`…/bounties/*/../outside.md`) returns `[]` on CPython
  **3.14.8**, so one direct-branch glob-traversal vector could not be exercised; that is a stdlib
  property, not a resolver property.
* F5 requires a citation with two or more existing expansions and at least one escaping — brace or
  placeholder forms, which `noise_flags` marks `synthetic` (71 such path-like tokens exist in
  `SKILL.md` + `corpus/**/*.md`; a scan with the resolver's own `TOKEN`/`is_pathlike` found them).
  None of the current corpus brace citations contains `..`, so F5 is not exploited by shipped text
  today.
* F6 is specific to the empty-alternative idiom; `~/Projects/bounties/{README.md,.gitignore}` and
  `ops/{claim-check,…}.mjs` (no empty alternative) are unaffected.
* I did not measure a live census delta: running `resolve.py` on the lane writes
  `citation-survival.tsv` into `corpus/instruments/`, which this seat may not do.
* Counts here are classification counts from copied-CLI replays; they establish detector behaviour
  only, not source availability, attribution, or any score movement.

## Reproduction

```
cd /tmp/kasegi-r23-falsify-BraceGlobProbe
python3 /tmp/kasegi-r23-falsify-BraceGlobProbe/final-probe.py     # pinned snapshot resolver/checker
# or, against live bytes:
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
for m in brace-glob-fixtures boundary-vacuum-fixtures brace-empty-alt-fixtures; do
  python3 corpus/instruments/mirror-containment-check.py \
    --fixtures /tmp/kasegi-r23-falsify-BraceGlobProbe/$m.json --resolver corpus/instruments/resolve.py
done
```

Raw evidence: `final-results-v3.json` and `final-results-v4.json` (per-case class, method,
`resolved_path` and realpath-containment booleans), `probe-results.json`, `receipt-fixed.json`,
`receipt-baseline.json`, and the as-of byte copies listed in the first table.
