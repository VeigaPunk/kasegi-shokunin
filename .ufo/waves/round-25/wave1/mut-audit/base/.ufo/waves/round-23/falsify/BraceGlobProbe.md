# BraceGlobProbe — round-23 falsify: brace / placeholder-glob expansion against C1

Seat: `L1Kasegi23.BraceGlobProbe-2` (leaf executor, read-only on the lane).
Target (dispatch § "Target"): escape cases whose hit travels through `{a,b}` brace expansion and
through a `<...>` placeholder glob under the bounty, canonical-alias, relative-mirror and
relative-lane branches — replayed on fixed and baseline bytes, reporting expected-vs-actual class
and whether realpath confinement holds on each hit.

Scratch (all writes confined here): `/tmp/kasegi-r23-falsify-BraceGlobProbe/`.
No production file, lane tree, git/jj state or sibling lane was written. `resolve.py` was never
executed against the lane repo, because it writes `corpus/instruments/citation-survival.tsv` beside
itself; every run executes a byte-copied resolver inside a disposable fixture tree.

## Bytes under test (pinned; four artifacts were edited while this probe ran)

| artifact | as-of snapshot in scratch | sha256 |
|---|---|---|
| `corpus/instruments/resolve.py` (fixed, superseded 03:46:26) | `asof-resolve-fixed.py` | `8dd45bc8d9aedbb25247a64fbd6094a1b9e7b9a3b3facdb58001c59ef3868848` |
| `corpus/instruments/resolve.py` (fixed, final) | `asof2-resolve-fixed.py` | `fce5b84be4cece914260f03a3a8b739dc1108381f97482bbfc7b22143810a4b0` |
| `.ufo/waves/round-23/c1-baseline-resolver.py` | `asof-resolve-baseline.py` | `d6a3c3f1a1d8e97d42d66a8aa3cb34530b7bc1c18b194e487ef8d580d869f903` |
| `corpus/instruments/mirror-containment-check.py` (final) | `asof-checker-53742c8d.py` | `53742c8d9529dffb8c40c39b3448de7388b774b548d7831670598d5534bff5d1` |
| `corpus/instruments/mirror-containment-fixtures.json` (frozen matrix, 23 cases) | read in place | `332a5fe95b94207cdf25caf29d52b394f81701b4fe441b92e47ab3ac100005e3` |

Every case in all three matrices returns the **same class** on resolver `8dd45bc8…` and on
`fce5b84b…`, and under checker `fc9550f0…` and `53742c8d…` (`final-results-v3.json`,
`final-results-v4.json`). The two resolver revisions differ only in that a root-only bounty suffix
no longer maps to the mirror root (`resolve.py:237-243`); no probe case has an empty suffix, so the
change is class-neutral here.

## Matrices written (committed schema, accepted verbatim by `--fixtures`)

* `brace-glob-fixtures.json` — 17 cases, sha256 `28ef0f8bed7f1c0a8bbe3c4d59e3f95018c9f153b3d23aec6809cfbab4aeea0d`
  (7 escape, 10 control): brace/glob escapes through the bounty fallback, the relative-mirror
  fallback and the canonical-alias branch; brace/glob confined controls; a multi-match decoy pair;
  an absolute-path injection into the bounty suffix; and three direct-hit *parity* controls.
* `boundary-vacuum-fixtures.json` — 2 cases, sha256 `9ff92e2c5d0a9e32da0dedb98374a77b035e5715eb23442287c68ab81861e3f9`:
  the frozen traversal escape with and without the intermediate directory it walks through.
* `brace-empty-alt-fixtures.json` — 3 cases, sha256 `8ebd1a53922d96ea5acc6fae0461a344a80d8712f4a8db162d398ec0d0fc2f91`:
  the exact brace idiom cited at `SKILL.md:1000`, with an empty first alternative.

Replay command (each matrix × both byte-sets):

```
python3 corpus/instruments/mirror-containment-check.py \
  --fixtures /tmp/kasegi-r23-falsify-BraceGlobProbe/<matrix>.json \
  --resolver <resolver bytes>   # corpus/instruments/resolve.py | .ufo/.../c1-baseline-resolver.py
```

`probe.py` / `final-probe.py` additionally record the TSV `method`, `domain`, `resolved_path` and a
realpath-containment boolean per row (`final-results-v3.json`, `final-results-v4.json`), because the
class column alone does not show whether a hit was *confined* or merely *absent*.

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

`boundary-vacuum-fixtures.json` — fixed **2/2**, baseline **2/2** (F4).
`brace-empty-alt-fixtures.json` — fixed **0/3**, baseline **0/3** (F2).

## Findings (live against `fce5b84b…`)

### F1 — control preservation is incomplete: a valid confined match is suppressed when an escaping expansion sorts first

```
glob-multimatch-decoy-mask   control expect=MIRROR-EQUIVALENT actual=GONE FAIL verdict=missing-path
brace-multialt-decoy-mask    control expect=MIRROR-EQUIVALENT actual=GONE FAIL verdict=missing-path
```

Probe rows (`final-results-v4.json`; trees built by the instrument's own `build_case`):

```
globmatch <root>/relocated/tbh/sorted/a-lure.mjs  in_mirror=False real=<root>/secret/lure.mjs
globmatch <root>/relocated/tbh/sorted/z-real.mjs  in_mirror=True  real=<root>/relocated/tbh/sorted/z-real.mjs
exists_any(join)= ('glob', '<root>/relocated/tbh/sorted/a-lure.mjs')
classify= ('GONE', '', '', 'bounty')
```

Mechanism: `exists_any` returns the **first existing** brace alternative (`resolve.py:187`, inside `exists_any` at `:179`) and only `matches[0]` of a sorted glob (`resolve.py:192`); `classify`
then applies `under_mirror` to that single path and returns GONE when it fails
(`resolve.py:243-246`) instead of trying the remaining expansions. `z-real.mjs` is a genuine
confined mirror byte; a sibling symlink that sorts earlier masks it. The baseline "passes" the class
only by crediting the escaping path — the checker flags that row `path-outside-mirror-equivalent`,
so the baseline fails the case too under the path column. C1's "preserve valid confined mirror
controls" therefore holds for **single-match** expansions (the four confined controls above) and
fails for multi-match ones.

Falsifiable: iterate the expansion list and credit the first `under_mirror` hit — both cases flip to
MIRROR-EQUIVALENT with no escape case weakening.

### F2 — an empty brace alternative silently disables the real file, on a live corpus citation

`SKILL.md:1000` cites ``~/Projects/bounties/ops/sighting{,-board,-dispatcher,-missions}.sh``.
`brace_expand` drops the empty alternative by design (`resolve.py:172`,
`# `{}` / `{,x}` empty alternative is not a resolvable expansion`), so `ops/sighting.sh` is never
probed even when it is the file that exists:

```
brace_expand: [.../sighting-board.sh, .../sighting-dispatcher.sh, .../sighting-missions.sh]
sighting.sh exists at: True
exists_any: (None, None)
classify: ('GONE', '', '', 'bounty')
```

`brace-empty-alt-fixtures.json` is **0/3 on both resolvers** — direct hit and mirror fallback, with
the file present at exactly the name the empty alternative denotes. Bash expands
`sighting{,-board}.sh` to `sighting.sh sighting-board.sh`, which is how the corpus line reads, so
this is a detector false negative independent of C1 (identical baseline behaviour) that depresses
the census numerator for a citation the lane ships.

Falsifiable: also test the unsubstituted path when an alternative is empty — the three cases pass,
and no existing case changes.

### F3 — realpath confinement holds for brace and glob hits on the mirror fallbacks (attacked, not breached)

All five brace/glob fallback escapes that the baseline credits outside the mirror are GONE on the
fixed bytes, and the probe shows the mechanism is the containment predicate, not a missing file:

| case | baseline credited path | realpath inside mirror? | fixed |
|---|---|---|---|
| `bounty-fallback-brace-escape` | `<CASE>/relocated/tbh/../mirror-escape/note.md` | no | GONE |
| `bounty-fallback-glob-escape` | `<CASE>/relocated/tbh/../probe/leak.md` | no | GONE |
| `bounty-fallback-glob-symlink-escape` | `<CASE>/relocated/tbh/ops/only.mjs` → `<CASE>/secret/sym.mjs` | no | GONE |
| `relative-fallback-brace-escape` | `<CASE>/relocated/tbh/../../escape3/x.md` | no | GONE |
| `relative-fallback-glob-escape` | `<CASE>/relocated/tbh/../../escape4/note.md` | no | GONE |

`under_mirror()` (`resolve.py:224-229`) is applied on the bounty fallback (`:244`), the
canonical-alias branch (`:253`) and the relative-mirror fallback (`:265`), and it survives every
expansion method I could construct: brace alt containing `..`, placeholder glob before *and* after
the traversal, glob match that is itself a symlink out, alias branch, and root-only suffix. The
absolute-path injection (`~/Projects/bounties//tmp/...`) is closed twice — by `lstrip("/")` in
`bounty_suffix` (`resolve.py:220`) and by `under_mirror` on the joined hit (probe:
`join(mirror, suffix)` returned `/tmp/kasegi-r23-falsify-BraceGlobProbe/abs-probe.txt`, exists,
`under_mirror=False`).

### F4 — expansion does not change the direct-bounty-hit class; the frozen traversal pin is POSIX-fixture-sensitive

The three parity controls reproduce exactly the class the frozen matrix pins for the literal forms
`bounty-literal-present-traversal` and `bounty-literal-symlink-present` — RESOLVES on both byte-sets,
with `method=brace` / `method=glob` — so expansion neither launders nor blocks a direct hit.

`boundary-vacuum-fixtures.json` replays ``~/Projects/bounties/../outside.md:1`` with identical case
bytes twice: **without** `home/Projects/bounties` → GONE on both resolvers; **with** it present →
RESOLVES on both, `path=<CASE>/home/Projects/bounties/../outside.md`. POSIX cannot traverse a
nonexistent component, so the frozen `bounty-parent-traversal` GONE is not produced by confinement;
that case's fail-before/pass-after discrimination comes entirely from its `relocated/outside.md`
mirror-fallback hit. The pair documents a proof obligation that the new
`absolute-parent-traversal` case had to state explicitly ("host-dependent: requires
/home/vgpnk/Projects/outside-vault to stay absent on the run host") while the relative spelling's
dependence on `~/Projects/bounties` staying absent is not stated in its note.

## Verification of two gaps I measured earlier in this probe (both closed while I worked)

* **Stale receipts.** At 03:45 the frozen matrix was 20 cases / `4e39f65c…` while both receipts
  pinned 17 cases / `5c64e014…`. At 03:47 both were regenerated against `4e39f65c…`
  (fixed 20/20, baseline 12/20 — the baseline count matches my independent replay exactly). At
  03:48 the matrix grew to 23 cases / `332a5fe9…` and both receipts were regenerated again
  (fixed 23/23, baseline 12/23 — again matching my replay of the same matrix).
* **Non-discriminating glob escape.** At `4e39f65c…` the case `glob-expansion-escape` cited
  ``~/Projects/bounties/<name>.md`` with the only outside file at `relocated/outside-vault/x.md`;
  neither probe pattern could match it, and the case **passed on the knowingly-unsound baseline**
  — a fail-before/pass-after pair whose "before" already passed proves nothing. At `332a5fe9…` the
  case cites ``~/Projects/bounties/<name>/../../outside-vault/x.md`` and the baseline now fails it
  (`MIRROR-EQUIVALENT`, `path_check=gone-with-path`); the fixture's own note records the reason
  ("a bare `<name>.md` glob cannot cross `/` and would pass on baseline too, so it is not used
  here"). My discriminating variant (`bounty-fallback-glob-escape`) behaves the same way.

Neither is an open defect at write time; both are recorded because the verification standard they
test — the receipt digest must equal the frozen matrix, and every escape case must fail on the
baseline — is the one that makes the pair evidence.

## Drift observed (the artifacts moved under this probe)

| time | artifact | sha256 | note |
|---|---|---|---|
| 03:27–03:38 | `resolve.py` | `ed9a9dae…` | matched the then-current `c1-fixed.json` |
| 03:40:40 | `resolve.py` | `9e0b5751…` | `bounty_suffix` gained `lstrip("/")`, empty-suffix guard, `max(…, default=0)` |
| 03:42:37 | `resolve.py` | `8dd45bc8…` | `asof-resolve-fixed.py` |
| 03:46:26 | `resolve.py` | `fce5b84b…` | root-only bounty suffix no longer maps to the mirror root |
| 03:28:25 | checker | `1bc2db10…` | class-only |
| 03:42:15 | checker | `fc9550f0…` | gained `resolved_path` + `path_verdict` |
| 03:43:0x | checker | `53742c8d…` | added `path_tolerance: carve-out` handling |
| 03:39→03:48 | fixtures | `5e61a33e…` → `5c64e014…` → `4e39f65c…` → `332a5fe9…` | 13 → 17 → 20 → 23 cases |
| 03:47, 03:48 | `c1-fixed.json`, `c1-baseline.json` | — | regenerated at 20 and again at 23 cases |

My matrices were re-run after each change; per-case classes are unchanged across both resolver and
both checker revisions. Numbers quoted against `5c64e014`/`4e39f65c` above are marked as belonging
to those revisions only.

## Scope limits

* Realpath cannot see **bind mounts / overlayfs** inside the mirror; untestable here (host
  package/service/mount operations are paused by the wave tooling rule) and uncovered by any case.
* `glob` through a magic component into `..` (`…/bounties/*/../outside.md`) returns `[]` on CPython
  **3.14.8**, so that one direct-branch glob-traversal spelling could not be exercised; that is a
  stdlib property, not a resolver property.
* F1 needs a citation with two or more existing expansions and at least one escaping — brace or
  placeholder forms, which `noise_flags` marks `synthetic`. A scan with the resolver's own
  `TOKEN`/`is_pathlike` over `SKILL.md` + `corpus/**/*.md` (66 files) finds 71 such path-like
  tokens, many in the bounty domain (e.g. `ops/{claim-check,…}.mjs`), but none containing `..`, so
  F1 is not exploited by shipped text today.
* F2 is specific to the empty-alternative idiom; `~/Projects/bounties/{README.md,.gitignore}` and
  `ops/{claim-check,…}.mjs` (no empty alternative) are unaffected.
* No live census delta was measured: running `resolve.py` on the lane writes
  `citation-survival.tsv` into `corpus/instruments/`, which this seat may not do.
* Counts are classification counts from copied-CLI replays; they establish detector behaviour only,
  not source availability, attribution, or score movement.

## Reproduction

```
cd /tmp/kasegi-r23-falsify-BraceGlobProbe
python3 final-probe.py        # pinned snapshot resolver + checker; writes final-results-v3.json
# live bytes, per matrix:
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
for m in brace-glob-fixtures boundary-vacuum-fixtures brace-empty-alt-fixtures; do
  python3 corpus/instruments/mirror-containment-check.py \
    --fixtures /tmp/kasegi-r23-falsify-BraceGlobProbe/$m.json --resolver corpus/instruments/resolve.py
done
```

Raw evidence: `final-results-v3.json` and `final-results-v4.json` (per-case class, method,
`resolved_path`, realpath-containment booleans), `probe-results.json`, the three matrices, and the
as-of byte copies listed in the first table. The wave receipts themselves live at
`.ufo/waves/round-23/c1-{fixed,baseline}.json`.
