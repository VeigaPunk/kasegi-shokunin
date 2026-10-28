# MutScan — J5 scan mutant matrix (round 42 wave 1, receipt-only)

Scope: propose the J5 (family F-SCAN) scratch-scan mutant matrix beyond r41's
known mutants, one detection mechanism per state. Empirical basis: the
committed r41 scanner was exercised read-only over planted fixture trees;
observed payloads below pin which classes escape today and which already die.

## Inputs read

- `.ufo/waves/round-42/claims.json` (frozen; J5 = F-SCAN: "covers `kasegi-r4[0-9]*`
  prefixes and an outside-configured-root stray under a seat-named dir is
  detected — the committed MutScratchTiming probe must be rejected on replay,
  evaluated inside the suite's own scratch root, never host-global state").
- `corpus/instruments/r41-closure.sh` — `family_name`/`family_match` (L596-606),
  `chain_clean` (L612-628), `scan_scratch` (L636-667), `check_i6` (L1128-1148),
  committed probes `i11_probe_f1..f6` (L1415-1463).
- `.ufo/waves/round-41/wave2/MutScratchTiming.md` (outside-root escape),
  `RevScanOwnership.md` (F1-F8 expected reds), `MutAncestorGuard.md`.
- wave1-spec ExecJ5Scan prompt (two-root design: live root + materialized
  fixture root; parent-of-root enumeration; never hardcoded host path).
- `corpus/lessons/round-41-verifier-spotcheck.md` §5 (routed queue).

## What "r41's 4 known" are

r41's committed stray-shape selftest fixtures (I11 replay probes F1-F4):
nested-under-container family stray, family stray beside a dirty own-container
chain, dot-prefixed family dir, case/separator variants. `i11_probe_f5` adds
the symlink-to-ancestor (r40 F5) state and `f6` the missing-root fail-closed
state. I6's own selftest detail lines were `family-stray`,
`nested-family-stray`, `dot-prefixed-stray`, `case-separator-stray`,
`unreadable-scratch-root` (MutScratchTiming.md L15) — four stray shapes plus
one fail-closed probe. Everything below is beyond those.

## Method (detector exercised)

Sourced the committed suite (`BASH_SOURCE` guard makes it importable; sha256
`3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd`, identical
to the bytes MutScratchTiming recorded) and called `scan_scratch ROOT WORK`
plus `family_match`/`family_name` over ~45 fixture trees under
`/fast/scratch/hyaku/kasegi-r42/MutScan/`. Verbatim observed outputs:

```
C1 in-root kasegi-r41-stray                  -> strays=1,read=ok,scanned=1   (control: dies)
M1 ../kasegi-r41-outside vs root             -> strays=0,read=ok,scanned=0   ESCAPE
M2 root/kasegi-r39|r40|r42|r50               -> strays=0,read=ok,scanned=0   ESCAPE (4x)
   (first probe run: kasegi-r{39,50,100,5}-seat all missed too; only the
    literal own-round anchor kasegi-r41* matches)
M3a kasegi-r41/hidden/OtherSeat              -> strays=1,read=ok,scanned=1   dies
M3b misc/kasegi-r41-seat (nonfam parent)     -> strays=1,read=ok,scanned=1   dies
M3c fam-ancestor chain w/ violator           -> strays=1,read=ok,scanned=1   dies
M3d work/kasegi-r99-plant                    -> strays=0,read=ok,scanned=0   exempt (policy)
M3e fam-ancestor clean chain (control)       -> strays=0,read=ok,scanned=1   tolerated, correct
M4a .kasegi-r41-seat / M4b ..kasegi-r41      -> strays=1                     dies
M4c .x/.kasegi-r41 (hidden parent)           -> strays=1                     dies
M4d .kasegi-r41/work ancestor (control)      -> strays=0,scanned=1           tolerated, correct
M5a KASEGI-R41-SEAT / M5b kasegi_r41_seat    -> strays=1                     dies
M5c kasegi<U+2010>r41 / M5d 'kasegi - r41'   -> strays=1                     dies
M6a ' kasegi-r41' (leading space)            -> strays=0,read=ok,scanned=0   ESCAPE
M6b --kasegi-r41                             -> strays=0,read=ok,scanned=0   ESCAPE
M6c .-kasegi-r41                             -> strays=0,read=ok,scanned=0   ESCAPE
M7a link -> outside-root dir                 -> strays=1                     dies
M7b link -> /etc                             -> strays=1                     dies
M7c link -> inside work                      -> strays=0,read=ok,scanned=1   ESCAPE (entry-level stray exempted by target)
M7d link -> ancestor of work                 -> strays=1                     dies (r40 F5 limb holds)
M7e dangling link                            -> strays=1,read=fail           dies (fail-closed)
M7f link -> root (work descendant)           -> strays=1                     dies
M7g link->sib w/ fam file inside             -> strays=1 (link counted; inner file invisible) dies
M8a regular file / M8b fifo                  -> strays=1,read=fail           dies (via read=fail conflation)
M9a kasegi,kasegi-r,kasegi-rx,foo,kasegi-r41x,kasegi-r41seat -> strays=0  (see M9b note)
M9c kasegi-r4 + kasegi-r41-4                 -> strays=1,scanned=1           kasegi-r4 silently NOT counted
M9b 'kasegi-r41.' trailing dot               -> strays=1                     dies
M10a work==root, stray inside                -> strays=0,read=ok,scanned=1   VACUOUS-PASS config
M10b missing work                            -> strays=0,read=ok,scanned=0   (no work to exempt)
M11 unreadable hide/kasegi-r41               -> strays=0,read=fail,scanned=0 dies via read=fail; stray masked
M7h root=symlink, in-root stray              -> strays=0,read=ok,scanned=0   VACUOUS (find -P won't descend a link arg)
M7i root=dangling link                       -> strays=0,read=fail           fail-closed, correct
M12 'kasegi-r41<LF>seat'                     -> strays=1,read=fail,scanned=1 dies via read=fail (record split)
M13 'kasegi-r41<TAB>seat'                    -> strays=1                     dies (tab is a separator)
M14 kasegi-r-41                              -> strays=0,read=ok,scanned=0   ESCAPE
M16 family sibling next to chain parent      -> strays=1                     dies (chain_clean)
M17 a/kasegi-r41-mid/b/kasegi-r41-deep       -> strays=2                     dies
M18 non-family + other-lane name (souji-r32) -> strays=0                     correct negative control
unit ' kasegi-r41'  family_name -> '-kasegi-r41'  match rc=1                 (root cause of M6)
unit '--kasegi-r41' family_name -> '-kasegi-r41'  match rc=1
unit '.-kasegi-r41' family_name -> '-kasegi-r41'  match rc=1
unit 'kasegi-r41x'  family_name -> 'kasegi-r41x'  match rc=1                 (r41 tight tail)
unit 'kasegi-r-41'  family_name -> 'kasegi-r-41'  match rc=1
```

## J5 mutant matrix

Eight classes. For each: planted fixture shape(s), the r41 baseline behavior
observed above, the detection mechanism J5 requires, and the expected J5
payload. All fixtures live under a materialized fixture root beneath `--work`;
no row touches host-global state.

### S1 — outside-configured-root stray (the routed defect; MutScratchTiming replay)

Shapes: `PARENT/kasegi-r42-outside` where `PARENT=$(dirname realroot)`;
`PARENT/.kasegi-r41` (dot+outside); `PARENT/kasegi-r50` (sibling+outside).
Baseline: `strays=0,scanned=0` — unobserved, r41 enumerates only `$root`.
Mechanism REQUIRED: a second enumeration pass over `dirname(realroot)` (one
level only), classifying names with the same family matcher, exempting only
`realroot` itself and any entry on the `--work` ancestor chain. Bounded: never
recurse into siblings, never read the host `/fast/scratch` — the limb scans
the fixture parent the selftest materialized, and in run mode the parent of
the caller-supplied `--scratch-root`.
Expected: `parent-strays>=1` and `closed=0`; pair with a negative control
(only `realroot` and non-family entries in the parent -> green).

### S2 — sibling-round prefixes (literal-anchor mutant; my seat's named rows)

Shapes: `$root/kasegi-r39`, `$root/kasegi-r50`, `$root/kasegi-r100`,
`$root/kasegi-r5`, `$root/kasegi-r42/SeatX` (own-round seed of the r42
family), `$root/kasegi-r41/SeatX` (prior round), `$root/kasegi-r42/OtherSeat`
(the spec's planted examples).
Baseline: every non-`r41` round missed (`strays=0,scanned=0`, M2 x4 + probe1
x5); r41's matcher is the literal `kasegi-r41|kasegi-r41-*`.
Mechanism REQUIRED: normalize `family_name`, then match the round-family
CLASS `^kasegi-r-?[0-9]+` (lowercase, separators collapsed), never the literal
own-round string and never the `kasegi-r4[0-9]` decade glob — the glob
under-matches `kasegi-r39`/`r5`/`r100` (seat spec's `kasegi-r3*`/`kasegi-r5*`
rows) while over-matching `kasegi-r42x` (which is fine: loose tail flags
suspect residue, see S5 controls). Own-round entries remain strays unless
they are `realwork`, inside it, or tolerated chain ancestors — matching is by
name family, not by "other round = ignore".
Expected: one stray per planted sibling dir; `scanned` reflects planted count.

### S3 — nested seat dirs

Shapes: `$root/kasegi-r42/hidden/OtherSeat`; `$root/misc/kasegi-r42-seat`
(non-family intermediate); `$root/a/kasegi-r42-mid/b/kasegi-r42-deep`;
chain violator `$root/kasegi-r42/{work,hidden/SeatB}` with `--work` inside
the container; in-`--work` plant `$root/work/kasegi-r99`.
Baseline: arbitrary-depth and non-family-parent strays die (M3a/b, M17);
chain violators die via `chain_clean` (M3c); in-work entries are exempt
(M3d) — that is the r41 contract, needed so the suite's own materialized
fixture under `--work` is not self-incriminating.
Mechanism REQUIRED: unbounded-depth recursive enumeration (no depth cap) +
per-entry family classification + `chain_clean` retained verbatim for the
ancestor exemption. Policy row: in-work family plants stay exempt by design;
the matrix asserts the exemption is scoped to `realwork` only (a `realwork`
that equals `realroot` must fail closed — see C1 config class below).
Expected: strays = number of family entries outside the work chain.

### S4 — dot-prefixed strays (sibling-hardened)

Shapes: `$root/.kasegi-r42`, `$root/..kasegi-r42`, `$root/.kasegi-r39-seat`
(dot+sibling — r41's dot fixture was own-round only), `$root/.x/.kasegi-r42`;
control `.kasegi-r42-cont/work` as `--work` ancestor.
Baseline: own-round dot entries die (M4a/b/c); a `.kasegi-r4x` sibling would
miss under the literal anchor (compounds S2); dot-ancestor tolerated
correctly (M4d).
Mechanism REQUIRED: dot-inclusive enumeration (the `find` listing already is;
a `for $root/*` glob or `ls` without `-A` is a fail) + strip leading dots
BEFORE family matching + ancestor tolerance applied to the normalized name
(dot-prefixed work-chain containers must not be condemned, else the check
condemns a legitimate hidden seat dir).
Expected: dot-prefixed sibling strays counted; dot-ancestor control green.

### S5 — case/separator variants of SIBLING prefixes (+ three new normalization escapes)

Shapes: `KASEGI-R42-SEAT`, `Kasegi_R50_Seat`, `kasegi<U+2010>r39` (non-ASCII
hyphen), `kasegi - r42`; NEW escapes found this probe: `' kasegi-r42'`
(leading space), `--kasegi-r42`, `.-kasegi-r42` — normalization strips
leading dots but not a collapsed leading separator, so `family_name` yields
`-kasegi-r42` and the match fails (unit probes above); `kasegi-r-41`
(separator inside the digits) and `kasegi-r42x`/`kasegi-r41seat` (no
separator tail) — missed by r41's tight `kasegi-rN|kasegi-rN-*` case.
Baseline: M5a-e die (own-round); M6a/b/c, M14, `kasegi-r41x` all escape.
Mechanism REQUIRED: normalize = lowercase + collapse every non-`[a-z0-9]`
run to one `-` (byte-wise, so UTF-8 separators collapse) + strip BOTH
leading and trailing separators after collapse (fixes M6) + family ERE
`^kasegi-r-?[0-9]+` (loose tail; catches `r-41`, `r42x`, `r41seat`). Matched
against SIBLING rounds, not own-round literal.
Expected: every shape above a stray; negative controls `kasegi`, `kasegi-r`,
`kasegi-rx`, `kasegi-abc`, other-lane `souji-r32` must NOT match.

### S6 — symlinks pointing outside the suite scratch (and the inside-work exemption hole)

Shapes: `$root/kasegi-r42-link -> $PARENT/out` (target outside root);
`-> /etc` (host-global target — planted as a literal link in the fixture,
the check only stats it); `-> ancestor of work` (r40 F5 shape); `-> root`
with work a descendant (M7f); dangling `-> gone` (M7e); link->sibling-family
(M7g); NEW: `$root/kasegi-r42-link -> inside realwork` — entry path outside
work but resolved target inside (M7c escapes r41).
Baseline: outside/ancestor/root/dangling all die (M7a/b/d/e/f — the F5 limb
holds); inside-work target exempted (M7c) — a family-named entry exists at
entry level yet is pardoned by its target.
Mechanism REQUIRED: resolve every family-named entry (`cd e && pwd -P`);
resolution failure -> stray+fail (dangling, loop, non-dir). Exemption by
ENTRY lexical path inside `realwork`, not by resolved target: a family-named
symlink outside `realwork` is a stray wherever it points; only a family
entry INSIDE `realwork` may be exempt. Ancestor case unchanged: tolerated
only if real dir + `chain_clean` (F5 replay). Root-boundary rule: any
resolved target outside `realroot` that is not `realwork`-related is a stray.
Expected: M7c-class mutant red (`strays>=1`), F5 replay red, all outside
links red.

### C1 — configuration mutants (not name shapes; each is a vacuous-pass risk)

- `work == realroot`: r41 exempts everything -> `strays=0` with a planted
  stray (M10a). Mechanism: precondition `realwork != realroot`; degenerate
  equality fails closed (report `config=degenerate`, `closed=0`).
- `--scratch-root` given through a symlink: `find -P` does not descend a
  link-valued root arg -> `scanned=0` vacuous green (M7h). Mechanism: the
  check canonicalizes the root itself (`cd root && pwd -P`) BEFORE
  enumerating — `check_i6` already does this; `scan_scratch` must never be
  called on an uncanonicalized root. Dangling root -> `read=fail` already
  correct (M7i).
- missing/absent `--work`: scan must still evaluate strays against the
  declared work path, never skip exemption silently (M10b benign only
  because no entries existed).
- enumeration errors: unreadable non-family parent dir yields `read=fail`
  but `strays=0,scanned=0` (M11) — safe (closed=0) yet the payload masks a
  hidden family dir. Mechanism: carry a `hidden=<n>` or per-entry
  `inaccessible` count in the payload so the payload does not claim an
  unscanned region is clean.
- newline in a family name splits `find -print` records (M12 dies via
  read=fail but the entry is miscounted). Mechanism: `find -print0` +
  `read -d ''` makes enumeration record-safe.
- payload fidelity: `scanned` counts only family-matched entries, so an
  escaped class reports `scanned=0` and the payload cannot distinguish
  "empty root" from "matcher missed". Mechanism: report `entries=<n>` (all
  entries visited) alongside `scanned`; a suite run over a non-empty root
  showing `scanned=0,entries=0` is suspicious, `entries>0` is honest.

### R1 — replay limb requirement (frozen kill rule)

Every shape above is a selftest case over a materialized fixture root under
`--work`; additionally the committed MutScratchTiming probe is replayed: the
selftest re-creates its outside-configured-root stray beside a fixture root
(deterministic bytes — NOT `/tmp/kasegi_r41_outside_probe` host state) and
requires rejection. This keeps J5 deterministic and inside the suite's own
scratch root, satisfying "never host-global state".

## Boundary notes for ExecJ5Scan / ExecSuiteCore

- J5 (leftover sweep, F-SCAN) vs J13 (quiescence at receipt time): the same
  matcher/enumeration serves both; J13 adds only the at-receipt timing and
  the ref-name binding. One shared scan implementation avoids the r41
  dual-ownership drift RevScanOwnership flagged; if two call sites exist,
  both must call the same function.
- Do not weaken the work-exemption: the suite's own export dir and the
  selftest's materialized fixture root live under `--work` and MUST remain
  exempt (M3e/M4d semantics), or J5 condemns itself.
- Suggested payload: `J5 payload=strays=<n>,parent-strays=<n>,entries=<n>,scanned=<n>,read=ok|fail[,config=degenerate] closed=0|1`.

## Hygiene / ledger

- Scratch: `/fast/scratch/hyaku/kasegi-r42/MutScan/` (fixtures `fix`, `fix2`,
  `fix3`, probes `probe.sh/out`, `probe2.sh/out`, `probe3.sh/out`); removed
  via `rm -rf` before yield. No writes outside that dir except this receipt.
- Disk guard `status` ran green before the probe battery.
- Suite bytes unmutated (source-only harness; sha256 before/after
  `3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd`).
- Tools installed: none. Network fetches: none. Git/jj mutations: none.
- Deliverables: none (receipt-only item). This file is the report.
