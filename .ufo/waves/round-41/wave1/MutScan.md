# MutScan — round-41 wave-1 — I6 scan-limb mutant matrix (receipt-only item)

Seat: MutScan (mutation-tester, leaf). Attacked limb: the round-41 I6 scratch-scan
limb that sibling seat ExecI6Scan is building (`corpus/instruments/r41-closure.sh`
check I6: "scratch scan case/separator-insensitive, recursive, dot-inclusive,
fail-closed (T14 + CritKillRule)" — claims.json C1 predicate).

## Inputs read (all read-only)

- `.ufo/waves/round-41/claims.json` (C1 predicate + kill rule), `c1-controls/do-nothing.txt`,
  `c2-controls/before.txt`, `census-before.txt`.
- `corpus/instruments/r40-closure.sh` check_h6 (round-40 limb under attack).
- Round-40 wave-2 attack evidence: `wave2/RevC1Counters.defeats.txt` §D4 (T14:
  `Kasegi-R40-stray`/`kasegi_r40-stray` escaped with `rc=0 strays=0`),
  `wave2/CritKillRule.h6-escapes.sh` (escape matrix m2 dotfile, m3 uppercase,
  m4 U+2011 non-breaking hyphen, m5 nested, m6 ancestor symlink, m8 dangling,
  m9 unreadable, m10 regular file), `wave2/LabExportClean.md` §3–§4 (defects D1–D4),
  `wave2/MutH6H10.md`.
- ExecI6Scan's declared design from `.ufo/waves/round-41/wave1-spec.json` (its full
  prompt). **Its deliverable was NOT present in `wave1/` at write time** (seat still
  running per the live roster) — every kill verdict below is therefore graded against
  (a) its declared design/sandbox and (b) my empirical reference implementation of
  exactly that design. Verdicts marked `verify-at-land` should be re-checked against
  ExecI6Scan's transcript when it lands.

## The known 4 H6 survivors (identified from LabExportClean.md D4, as the spec requires)

LabExportClean §4: "D4 survivors M2/M5/M9/M10" — the four behavior-bearing points the
round-40 H6 selftest could not kill:

| known id | mutant | why it survived r40 |
|---|---|---|
| M2 | unreadable entry (`cd` fail) ignored | no fixture covered a non-directory/unreadable entry |
| M5 | `find -type d` only | same coverage hole (file stray `closed=1` on fixture I) |
| M9 | `read=fail` no longer reds | no fixture re-opened the read-state clause |
| M10 | `find` failure ignored (root mode 0311) | listable-failure root not in the fixture set |

Plus the round-40 routed escape classes (CritKillRule m2–m6; RevC1Counters T14/D4):
case-fold escape, separator escape (underscore and U+2011), dot-prefixed escape,
nested escape — these are what the round-41 design explicitly fixes ("any letter
case, ANY depth, INCLUDING dot-prefixed"). The matrix below is **beyond** those.

## Method

Built a reference honest limb `i6-ref.sh` implementing ExecI6Scan's declared design
verbatim (family `kasegi-r41*`|`kasegi_r41*` in any case **plus dot-prefixed name
variants**, recursive `find`, canonicalized `--work` exclusion by path containment,
fail-closed `read=fail` on any scan error), then generated 16 mutants from it by
exact single-point replacement (`gen-mutants.py`; every anchor asserted unique), and
ran one bounded detector (`mutscan-driver.sh`) over a 10-scenario sandbox matrix on
pristine and mutated bytes. The detector caught and I fixed two defects in my own
first reference limb (process-substitution `find` rc was un-propagatable; the family
pattern missed dot-prefixed NAMES because `fnmatch` anchors at string start — the
traversal is dot-inclusive but `.kasegi-r41-dot` does not match `-iname
'kasegi-r41*'`). Final baseline (pristine, deterministic across reruns):

```
== ref
declared            strays=5,read=ok  rc=1     (5 named strays + clean work dir)
clean               strays=0,read=ok  rc=0
decoy               strays=0,read=ok  rc=0     (akasegiXr41-decoy: NOT the family)
single-collision    strays=1,read=ok  rc=1     (only kasegi-r41-stray)
nested-work         strays=0,read=ok  rc=0     (work dir symlinked INSIDE root/kasegi-r41/)
empty               strays=1,read=ok  rc=1     (kasegi-r41-emptied counts)
symlink             strays=1,read=ok  rc=1     (kasegi-r41-link -> target-real, counted once, not followed)
nested-work-trailroot strays=0,read=ok rc=0    (root arg passed with trailing slash)
nested-locked       strays=0,read=fail rc=1    (container/locked-dir chmod 000 hides kasegi-r41-inner)
nested-work-rel     strays=0,read=ok  rc=0     (work arg passed as relative path)
```

Hashes: i6-ref.sh `e6d73553…`, gen-mutants.py `958c551b…`, mutscan-driver.sh
`4614d000…`, full detector transcript `detector-output.txt` `4cedef9b…` (kept in
scratch until yield; the verbatim per-mutant lines are quoted under each mutant).

## The matrix — 14 novel mutants + 1 known-survivor re-derivation + 1 race demonstration

Verdict column: does ExecI6Scan's **declared** design + sandbox kill it? Its sandbox:
`kasegi-r41-stray/`, `Kasegi_R41-stray/`, `kasegi_r41_stray/`,
`container/kasegi-r41-nested/`, `.kasegi-r41-dot/` + clean work dir (expect each to
red once, count 5; removal greens; work never reds; chmod-000 root → `read=fail`).

---

### MX1 — name-matching regex weakened to unanchored substring
Sketch: `\( -iname 'kasegi-r41*' -o -iname 'kasegi_r41*' -o -iname '.kasegi-r41*' -o -iname '.kasegi_r41*' \)` → `\( -iname '*kasegi*r41*' \)`.
Honest state broken: **false positives / count inflation**. Any scratch entry
containing both substrings in any position (`akasegiXr41-decoy`, `notkasegi-r41`,
`mykasegi_r41notes`) is counted; an honest seat whose root holds a non-family decoy
is red-flagged and the count-exact receipt payload is wrong.
Detector evidence: `decoy` scenario — ref `strays=0 rc=0` vs mx1 `strays=1 rc=1`.
ExecI6Scan declared design: **SURVIVES** — the declared sandbox has no negative
decoy, and all 5 named strays still match, so its transcript stays green. `verify-at-land`.
Recommendation: add a non-family decoy (`akasegiXr41-decoy`) and assert the exact count.

### MX2 — depth limit introduced
Sketch: `find "$realroot" ...` → `find "$realroot" -maxdepth 1 ...`.
Honest state broken: **nested leftovers invisible** — `container/kasegi-r41-nested/`
reads green.
Detector: `declared` — ref `strays=5` vs mx2 `strays=4`; also `nested-locked` flips
from honest `read=fail rc=1` to `strays=0,read=ok rc=0` (find never descends into the
locked container, so the error never surfaces — a second honest state broken).
ExecI6Scan design: **KILLED** — the sandbox contains `container/kasegi-r41-nested/`
and (per its prompt) counts 5.

### MX3 — dotfile traversal exclusion
Sketch: append `-not -path '*/.*'` before `-print`.
Honest state broken: **dot-prefixed leftovers invisible** (`.kasegi-r41-dot/`).
Detector: `declared` — ref 5 vs mx3 4.
ExecI6Scan design: **KILLED** — `.kasegi-r41-dot/` is one of its 5 named strays.

### MX15 — dot-prefixed NAME variants dropped from the family pattern (NEW; the subtle one)
Sketch: keep `-iname 'kasegi-r41*' -o -iname 'kasegi_r41*'`, silently drop the
`-o -iname '.kasegi-r41*' -o -iname '.kasegi_r41*'` alternatives.
Honest state broken: **dot-prefixed leftovers invisible** — same surface as MX3 but a
different mutation point: GNU find traverses dot-dirs by default, yet
`fnmatch(".kasegi-r41-dot", "kasegi-r41*", 0)` is false because the literal prefix
anchors at string start. My own first reference implementation had exactly this
defect; the detector caught it (ref `declared`=4 until fixed).
Detector: `declared` — fixed ref 5 vs mx15 4.
ExecI6Scan design: **KILLED iff** its implementation actually matches dot-prefixed
names (its sandbox names `.kasegi-r41-dot/`, so a faithful transcript kills it) — but
a naive `-iname 'kasegi-r41*' -o -iname 'kasegi_r41*'` implementation, which
satisfies the sandbox's *letter* only if it also treats the dot dir as matched, must
be checked. `verify-at-land`: this is the likeliest silent defect in a fresh limb.

### MX4a — work-dir exclusion reduced to path equality
Sketch: `case $realw in "$r"|"$r"/*) continue ;; esac` → `[ "$r" = "$realw" ] && continue`.
Honest state broken: **false red on the live default shape** — when `--work` sits
inside the family root (`/fast/scratch/hyaku/kasegi-r41/<seat>`, the standard seat
layout this very round uses), the family root entry contains the work dir but is not
*equal* to it, so the ancestor is counted and every honest run reds.
Detector: `nested-work` — ref `strays=0 rc=0` vs mx4a `strays=1 rc=1` (also
`nested-work-trailroot`, `nested-work-rel`).
ExecI6Scan design: **SURVIVES** — its declared sandbox places the work dir as a
sibling of the strays, so containment is never exercised. `verify-at-land`.
Recommendation: add a fixture with `--work` nested inside a `kasegi-r41/` dir and
assert green (this is the LabExportClean D1 kill-rule gap shape).

### MX4b — work-dir exclusion by basename prefix (`kasegi-r41` exactly)
Sketch: `case $realw in "$r"|"$r"/*) continue ;; esac` → `b=${e##*/}; case $b in kasegi-r41*) continue ;; esac`.
Honest state broken: **false green via prefix collision** — the canonical leftover
`kasegi-r41-stray/` (and any `kasegi-r41-*` sibling, plus `container/kasegi-r41-nested`)
shares the work dir's family prefix and is skipped. On a root whose only leftover is
`kasegi-r41-stray/`, the scan reads clean.
Detector: `single-collision` — ref `strays=1 rc=1` vs mx4b `strays=0 rc=0`; `declared`
— mx4b prints 3 (collision skips `kasegi-r41-stray` and `kasegi-r41-nested`);
`empty` — mx4b 0 (false green).
ExecI6Scan design: **KILLED iff the transcript asserts the exact count 5** (3≠5
detects it); a red/green-only assertion keeps it red at 3 and misses it, and the
isolated single-stray collision is not in the sandbox. Recommendation: assert exact
per-scenario counts and add the isolated `kasegi-r41-stray`-alone case.

### MX5 — case-fold forgotten
Sketch: `-iname` → `-name` (all four alternatives).
Honest state broken: **case-variant leftovers invisible** (`Kasegi_R41-stray/`,
`KASEGI-R41-…`).
Detector: `declared` — ref 5 vs mx5 4.
ExecI6Scan design: **KILLED** — `Kasegi_R41-stray/` is one of its 5. (This is the
round-40 T14/m3 escape class re-tested as a regression guard on the new limb.)

### MX6 — separator check single-alternative
Sketch: drop `-o -iname 'kasegi_r41*'` (or the dash alternative).
Honest state broken: **separator-variant leftovers invisible** (`kasegi_r41_stray/`
and `Kasegi_R41-stray/` both escaped in the detector — 5→3).
Detector: `declared` — ref 5 vs mx6 3.
ExecI6Scan design: **KILLED** — `kasegi_r41_stray/` is one of its 5.

### MX7 — `find -L` over-follow
Sketch: `find "$realroot"` → `find -L "$realroot"`.
Honest state broken: **root escape + over-count** — a family-named symlink
(`kasegi-r41-link -> target-real`) is followed out of the scratch root; entries
outside the root (`target-real/kasegi-r41-underneath`) get counted, and a symlink
loop or foreign tree can fail the scan or inflate the count.
Detector: `symlink` — ref `strays=1` vs mx7 `strays=2`.
ExecI6Scan design: **SURVIVES** — no symlink scenario in the declared sandbox.
`verify-at-land`. (The inverse `-type d` shape is known survivor M5, below.)

### MX8 — nested-unreadable fail-open (the NESTED shape of the known M10 family)
Sketch: `if ! out=$(find ...); then read=fail; fi` → `out=$(find ...)` (rc discarded).
Honest state broken: **silent partial scan** — a chmod-000 dir nested inside a
readable container (`container/locked-dir/kasegi-r41-inner`) hides its contents;
`find` exits 1, the mutant reports `strays=0,read=ok` green. Distinct from known M10
(which was proven at the ROOT): here the root is listable, so the failure mode only
fires mid-tree, which is exactly what a recursive r41 limb newly faces.
Detector: `nested-locked` — ref `strays=0,read=fail rc=1` vs mx8 `strays=0,read=ok rc=0`.
ExecI6Scan design: **SURVIVES** — its declared fail-closed proof is chmod-000 on the
ROOT, where both honest and mutant limbs red at the `cd` before `find` runs; the
nested shape is not exercised. `verify-at-land`. Recommendation: add a nested
chmod-000 fixture and assert `read=fail`.

### MX9 — scan-root trailing slash
Sketch: family-root skip built by textual concatenation:
`case $realw in "$r"|"$r"/*) continue ;; esac` → `case $r in "${root}/kasegi-r41") continue ;; esac`.
Honest state broken: **invocation-shape false red** — a root argument with a trailing
slash (`"$BASE/"`, the natural result of concatenation) makes the textual pattern
`${root}/kasegi-r41` expand to `.../root//kasegi-r41`, which never equals the
canonical path, so the work dir's own family root is counted and every honest run
reds.
Detector: `nested-work-trailroot` — ref `strays=0 rc=0` vs mx9 `strays=1 rc=1`
(with the trailing-slash root argument; `nested-work` without the slash stays green).
ExecI6Scan design: **SURVIVES** — the sandbox invokes the limb with a clean
mktemp-style path, no trailing slash, and the work dir as a sibling. `verify-at-land`.
Recommendation: invoke once with a trailing-slash root and with `--work` nested.

### MX10 — race: stray created mid-scan (TOCTOU)
Sketch: no single-line diff — the defect is the scan-then-file sequence itself: a
concurrent seat creates `kasegi-r41-late/` after the directory snapshot, before the
receipt is filed.
Honest state broken: **the verdict is a point-in-time snapshot, not the filing-time
state** — the receipt can certify a clean scratch that is dirty at file time.
Detector (deterministic demonstration, mx10-toctou):
`snapshot-strays=0 leftover-present-at-file-time=yes` — the snapshot found nothing;
the stray existed when the verdict was printed.
ExecI6Scan design: **SURVIVES by nature** — no bounded sequential transcript can kill
a scheduling race. This is a design observation, not an implementation bug: the
round-41 closure re-runs the live scan at Y verification, so a race survivor is
closed at the outer verification layer. The receipt should state the scan is
point-in-time (the r40 suite documented the same limit for H6).

### MX11 — `find -o` precedence (`-print` binds to the last alternative)
Sketch: drop the parentheses: `\( A -o B -o C -o D \) -print` → `A -o B -o C -o D -print`.
Honest state broken: **every family entry is matched but none is printed** — each
stray satisfies an earlier `-o` alternative, short-circuiting before the `-print`
side effect, so even the all-5-strays sandbox reads `strays=0` green. The classic
find precedence bug; the most damaging one-line mutation on this limb.
Detector: `declared` — ref `strays=5 rc=1` vs mx11 `strays=0,read=ok rc=0`.
ExecI6Scan design: **KILLED** — the red expectation on the 5-stray sandbox fires
(turns green), no count comparison needed.

### MX12 — work dir not canonicalized (raw string in the containment test)
Sketch: `realw=$( cd "$work" && pwd -P ) || …` → `realw=$work`.
Honest state broken: **false red on any non-canonical work argument** — relative
paths (`work`), `..` components, or symlinked work dirs break the containment
comparison, so the work dir's own family root is counted. This is the live default
shape for round 41: `--work /fast/scratch/hyaku/kasegi-r41/<seat>` passed through any
non-canonical spelling.
Detector: `nested-work` — ref green vs mx12 `strays=1 rc=1`; same for
`nested-work-trailroot` and `nested-work-rel`.
ExecI6Scan design: **SURVIVES** — the sandbox passes work as an absolute sibling path,
where raw-string containment coincidentally agrees. `verify-at-land`.
Recommendation: pass work once as a relative path and once through a symlink, assert green.

### MX13 — empty family entries exempted
Sketch: add `[ -n "$(ls -A "$e" 2>/dev/null)" ] || continue` before the counter.
Honest state broken: **emptied leftovers read green** — a seat that emptied its
scratch but left the directory entry (the r40-documented case: "an EMPTY one counts
too, because a seat that merely emptied its scratch still left the entry at filing")
is certified clean.
Detector: `empty` and `declared` (all 5 sandbox strays are empty dirs) — ref red vs
mx13 `strays=0,read=ok rc=0` on both; only the non-empty symlink target reds.
ExecI6Scan design: **KILLED iff its sandbox strays are created empty** (as its prompt
implies: `kasegi-r41-stray/` with no content) — the 5-stray scenario would read green
and fire the red expectation. If ExecI6Scan populates the strays, this SURVIVES and
needs a dedicated empty-dir fixture (round-40's selftest had one; carry it forward).

### MX14 — family glob dropped (exact names only)
Sketch: `-iname 'kasegi-r41*'` → `-iname 'kasegi-r41'` (all four alternatives).
Honest state broken: **all suffixed leftovers invisible** — every real leftover is
suffixed (`-stray`, `-nested`, `-seat`), so nothing ever matches except the bare
family root itself (which is excluded as the work container); the limb becomes a
no-op that greens any state.
Detector: `declared`/`single-collision`/`empty`/`symlink` all read `strays=0 rc=0`.
ExecI6Scan design: **KILLED** — the 5-stray sandbox turns green; red expectation fires.

### M5 (known survivor, re-derived on the new design) — `-type d` only
Sketch: append `-type d` before `-print`.
Honest state broken: **non-directory strays invisible** — a family-named symlink
(leftover link into another tree) is not counted; r40 proved this survived on a
regular-file stray (LabExportClean §4, fixture I).
Detector: `symlink` — ref `strays=1` vs m5 `strays=0 rc=0` (reproduces the known
survivor on the recursive r41 design).
ExecI6Scan design: **SURVIVES as declared** — its prompt requires covering "the 4 the
round-40 H6 selftest missed" (M2/M5/M9/M10), but its named sandbox contains only
directories, so unless its actual transcript adds a symlink/file stray fixture, M5
still survives. `verify-at-land` — the L1 should check ExecI6Scan's transcript for a
non-directory stray case.

## Verdict summary

| mutant | honest state broken | detector evidence (vs ref) | killed by ExecI6Scan's declared sandbox? |
|---|---|---|---|
| MX1 substring regex | false red on non-family decoy | decoy 0→1 | **NO** (no decoy in sandbox) |
| MX2 depth limit | nested leftover green | declared 5→4 | YES |
| MX3 dotfile traversal excl | dot leftover green | declared 5→4 | YES |
| MX15 dot-NAME variant dropped | dot leftover green | declared 5→4 | YES iff dot names actually matched (likely silent defect — verify) |
| MX4a equality-only exclusion | false red, work nested in family root | nested-work 0→1 | **NO** (sibling-only sandbox) |
| MX4b basename-prefix exclusion | false green on `kasegi-r41-stray` | single-collision 1→0 | partial: only under exact-count 5 (mutant prints 3) |
| MX5 case-fold forgotten | case-variant leftover green | declared 5→4 | YES |
| MX6 separator single-alternative | separator-variant leftover green | declared 5→3 | YES |
| MX7 find -L | root escape + over-count | symlink 1→2 | **NO** (no symlink scenario) |
| MX8 nested-unreadable swallowed | silent partial scan, green | nested-locked fail→ok | **NO** (chmod-000 ROOT only) |
| MX9 trailing-slash root | false red on natural invocation | trailroot 0→1 | **NO** (no trailing-slash invocation) |
| MX10 mid-scan race | snapshot ≠ filing state | toctou demo | **NO** (inherent; closed at live Y re-scan) |
| MX11 find -o precedence | everything green | declared 5→0 | YES (red expectation) |
| MX12 uncanonicalized work | false red, relative/symlink work | nested-work 0→1 | **NO** (absolute sibling work only) |
| MX13 empty-dir exemption | emptied leftover green | declared/empty →0 | YES iff sandbox strays are empty (verify) |
| MX14 exact names only | limb becomes a no-op | declared →0 | YES |
| M5 `-type d` (known) | symlink/file stray green | symlink 1→0 | **NO** as declared (no non-directory fixture) |

## Recommendations for ExecI6Scan's coverage table / the L1's land-check

Eight mutants SURVIVE ExecI6Scan's declared sandbox as written (MX1, MX4a, MX4b
partial, MX7, MX8, MX9, MX10, M5, plus MX15/MX13 conditional on implementation
choices). To close them, the limb's transcript should add six cheap fixtures to its
sandbox: (1) a non-family decoy asserting exact count; (2) `--work` nested inside a
`kasegi-r41/` dir (live shape) asserting green; (3) an isolated
`kasegi-r41-stray`-alone scenario asserting red with count 1; (4) a family-named
symlink and a family-named regular file asserting each counts once, and a `find -L`
advisory note; (5) a nested chmod-000 dir (root listable) asserting `read=fail`; (6)
trailing-slash root + relative/symlink `--work` invocations asserting green. MX10
cannot be fixture-killed; document the point-in-time limit and rely on the closure's
live re-scan at Y. Assertion strength matters throughout: per-scenario EXACT counts
(`strays=5`, `strays=1`), not red/green-only — MX4b, MX2, MX3, MX5, MX6, MX15 all
print a wrong-but-nonzero count that a red/green assertion accepts.

## Hygiene / restoration evidence

- Lane never written: all mutation lived in scratch copies under
  `/fast/scratch/hyaku/kasegi-r41/MutScan`; `git status --porcelain` in the lane shows
  only siblings' untracked wave-1 outputs; no mutating git/jj command run anywhere
  (read-only `status`/`hash-object` only). No lane/fleet/source-tree file edited; no
  PATH-dir write; no network fetch; no tool installed (nothing needed); no pacman.
- Baseline rerun determinism: pristine detector output identical across reruns
  (ref line `declared strays=5,read=ok rc=1` every run); detector transcript hash
  `4cedef9b025798fa69d482b2950c03d7e23044961320cbbbde0e376ab9539ad4`.
- The r40 committed suite `corpus/instruments/r40-closure.sh` was used read-only
  (git hash-object `3350fc21f622…`, consistent with the committed bytes quoted in the
  round-40 receipts).
- Scratch dir removed before yield (sandbox + mutants + detector all under
  `/fast/scratch/hyaku/kasegi-r41/MutScan`, deleted at exit).
