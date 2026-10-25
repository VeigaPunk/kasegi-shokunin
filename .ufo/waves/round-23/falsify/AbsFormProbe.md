# AbsFormProbe — absolute `/home/vgpnk/Projects/bounties…` citation forms vs the C1 containment evidence

Seat: `L1Kasegi23.AbsFormProbe-2` (leaf, falsify wave). Target question: build scratch fixtures for
citations spelled `/home/vgpnk/Projects/bounties/...`, the same path with a `../` escape, and
`/home/vgpnk/Projects/bounties-legacy/...` with a mirror decoy, then report fixed-vs-baseline classes
and whether the absolute form is covered by the same boundary and confinement as the tilde form.

Class-level only. This report does not judge admission, score movement, or C2. No lane or production
file was modified; only this report was written. No package was installed (nothing to record under the
tooling directive).

## 0. The artifacts changed three times during this probe

Everything below is measured on the **final** generation; §7 keeps the earlier observations that the
drift superseded, so a reader can tell what is still true.

| when (-0300) | resolve.py | matrix | checker | note |
|---|---|---|---|---|
| 03:28 | `ed9a9dae…` | `5e61a33e…` (13 cases) | old (class-only) | the `c1-fixed.json` I was handed |
| 03:40:40 | `9e0b5751…` | `5e61a33e…` | old | `bounty_suffix` gained `.lstrip("/")` |
| 03:42:37 | `8dd45bc8…` | `5e61a33e…` | old | literal branch documented as CARVE-OUT |
| 03:43:01 | `8dd45bc8…` | `5c64e014…` (17 cases) | `53742c8d…` (+path_verdict, carve-out) | receipts regenerated |

Final bytes:

```
resolve.py                      8dd45bc8d9aedbb25247a64fbd6094a1b9e7b9a3b3facdb58001c59ef3868848
mirror-containment-fixtures.json 5c64e0149f66d0261b561e271f0f5d4072b103f27ae4cea358d3e51cbed73e6e
mirror-containment-check.py     53742c8d9529dffb8c40c39b3448de7388b774b548d7831670598d5534bff5d1
c1-baseline-resolver.py         d6a3c3f1a1d8e97d42d66a8aa3cb34530b7bc1c18b194e487ef8d580d869f903
```

I re-derived, not quoted: with the current matrix, fixed is `cases=17 escape=7 controls=10 pass=17
fail=0`, baseline is `pass=10 fail=7` (all seven escapes `MIRROR-EQUIVALENT`), and `c1-fixed.json` /
`c1-baseline.json` (both mtime 03:43) now pin `resolver 8dd45bc8… / matrix 5c64e014…` consistently.
Earlier in the probe the same pair pinning `ed9a9dae… / 5e61a33e…` was stale; that no longer holds.

Current matrix composition: 11 `~/…` cites, 4 relative, **2 absolute** (`absolute-bounty-fallback-control`
→ `MIRROR-EQUIVALENT`, `absolute-prefix-sibling-confusion` → `GONE`), plus two literal-branch
carve-out controls (`bounty-literal-present-traversal`, `bounty-literal-symlink-present` → `RESOLVES`).

Host state relevant to every absolute case (read-only):
`/home/vgpnk/Projects/bounties`, `…/bounties-legacy`, `…/outside.md`,
`…/the-bounty-hunter`, `…/origin-work/the-bounty-hunter` are all **ABSENT**.

## 1. Method

`/tmp/kasegi-r23-falsify-AbsFormProbe/runner.py` materialises a case tree
(`home/Projects`, `lane`, `relocated/tbh`, plus per-case `dirs`/`files`/`symlinks` with `@ROOT@`
substitution), writes the cite into `lane/SKILL.md`, copies the selected resolver bytes to
`<case>/tool/resolve.py`, runs the real CLI with `HOME=<case>/home`,
`KASEGI_MIRROR=<case>/relocated/tbh`, cwd `<case>/tool`, then reads
`<case>/tool/citation-survival.tsv` (the CLI writes the TSV next to itself, so cases stay isolated)
and reports `class`, `domain`, `method`, `resolved_path`.

Three variants:
- `fixed` / `baseline` — landed bytes, unmodified (fixed = `8dd45bc8…` at run time).
- `*-abshome` — the *same* bytes with **only** the literal prefix at `resolve.py:97` rewritten to
  `<case>/home/Projects/bounties`, which is how the absolute-home tree becomes plantable and isolated.
  Diff is exactly one line:
  ```
  @@ -97 +97 @@
  -BOUNTY_PREFIXES = ("~/Projects/bounties", "/home/vgpnk/Projects/bounties")
  +BOUNTY_PREFIXES = ("~/Projects/bounties", "/tmp/…/work/<case>/home/Projects/bounties")
  ```
- `*-realhome` — landed bytes with `HOME=/home/vgpnk` (production-equivalent `expanduser`).

Case matrix: `/tmp/kasegi-r23-falsify-AbsFormProbe/cases.json`. Raw outputs:
`out-main.json`, `out-abshome.json`, `out-realhome.json`, `out-mutantC.json`.

Because the frozen checker sets `HOME` to a disposable directory, the tilde form follows the fixture
and the absolute form does not: `/home/vgpnk/...` ignores `HOME`. That asymmetry is the subject of
F1 and F4. The `-abshome` variant is the minimum change that makes an absolute-form case expressible
(the frozen schema has no such substitution).

## 2. Classes: fixed vs baseline (final bytes)

| # | cite | planted decoy | fixed | baseline |
|---|---|---|---|---|
| m1 | `~/Projects/bounties/../outside.md:1` | `relocated/outside.md` (= frozen `bounty-parent-traversal`) | GONE (bounty) | MIRROR-EQUIVALENT (bounty) |
| m2 | `~/Projects/bounties/evil.mjs:1` | mirror symlink → `secret/outside.mjs` (= frozen `bounty-fallback-symlink-escape`) | GONE (bounty) | MIRROR-EQUIVALENT (bounty) |
| m3 | `~/Projects/bounties-legacy/README.md:1` | `relocated/tbh/-legacy/README.md` (= frozen `bounty-prefix-sibling-confusion`) | GONE (**other**) | MIRROR-EQUIVALENT (bounty) |
| m4 | `~/Projects/bounties/ops/rank.mjs:1` | `relocated/tbh/ops/rank.mjs` (= frozen `confined-bounty-fallback-control`) | MIRROR-EQUIVALENT | MIRROR-EQUIVALENT |
| **m5** | `/home/vgpnk/Projects/bounties/../outside.md:1` | `relocated/outside.md` | **GONE (bounty)** | **MIRROR-EQUIVALENT** |
| m6 | `/home/vgpnk/Projects/bounties/../shokunin/kasegi-shokunin/SKILL.md:1` | none (lexical target exists, sha `f74a9f33…`) | GONE (bounty) | GONE (bounty) |
| **m7** | `/home/vgpnk/Projects/bounties/evil.mjs:1` | mirror symlink → `secret/outside.mjs` | **GONE (bounty)** | **MIRROR-EQUIVALENT** |
| **m8** | `/home/vgpnk/Projects/bounties-legacy/README.md:1` | `relocated/tbh/-legacy/README.md` | **GONE (other)** | **MIRROR-EQUIVALENT** |
| m9 | `~/Projects/bounties/../outside.md:1` | `home/Projects/outside.md`, bounty root **absent** | GONE (bounty) | GONE (bounty) |
| **m9b** | `~/Projects/bounties/../outside.md:1` | root **present**, `home/Projects/outside.md` present | **RESOLVES** (path `<root>/home/Projects/bounties/../outside.md`) | **RESOLVES** |
| **m10** | `~/Projects/bounties/evil.mjs:1` | literal symlink `home/Projects/bounties/evil.mjs` → `secret/outside.mjs` | **RESOLVES** | **RESOLVES** |
| m11 | `~/Projects/bounties//ops/rank.mjs:1` | `relocated/tbh/ops/rank.mjs` | MIRROR-EQUIVALENT | MIRROR-EQUIVALENT |
| m12 | `/home/vgpnk/Projects/bounties//ops/rank.mjs:1` | `relocated/tbh/ops/rank.mjs` | MIRROR-EQUIVALENT | MIRROR-EQUIVALENT |
| m13 | `../outside-vault/secret.mjs:1` | decoys at **both** `<root>/outside-vault/` and `<root>/relocated/outside-vault/` | INTERNAL (rel) | INTERNAL (rel) |
| **m14** | `/home/vgpnk/Projects/the-bounty-hunter/../../outside.md:1` | `outside.md` | **GONE (other)** | **GONE (other)** |
| **m15** | `/home/vgpnk/Projects/the-bounty-hunter/server.py:1` | `relocated/tbh/server.py` | **GONE (other)** | **GONE (other)** |
| m15-realhome | same, `HOME=/home/vgpnk` | same | **RESOLVES** (`<root>/relocated/tbh/server.py`) | **RESOLVES** |
| **m18** | `~/Projects/bounties/docs/x.md:1` | mirror **directory** symlink `docs` → `secret` | **GONE (bounty)** | **MIRROR-EQUIVALENT** |
| m19 | `docs/x.md:1` | same directory symlink | GONE (rel) | MIRROR-EQUIVALENT |

abshome variant (absolute form, isolated home, one-line constant rewrite):

| # | cite | planted | fixed-abshome | baseline-abshome |
|---|---|---|---|---|
| d1 | `<case>/home/Projects/bounties/../outside.md` | root present, `home/Projects/outside.md` | **RESOLVES** | **RESOLVES** |
| d2 | same | `relocated/outside.md` | **GONE** | **MIRROR-EQUIVALENT** |
| d3 | `<case>/home/Projects/bounties-legacy/README.md` | `relocated/tbh/-legacy/README.md` | **GONE (other)** | **MIRROR-EQUIVALENT** |
| d4 | same | literal `home/Projects/bounties-legacy/README.md` | RESOLVES (other) | RESOLVES (bounty) |
| d5 | `<case>/home/Projects/bounties/evil.mjs` | literal symlink → `secret/outside.mjs` | **RESOLVES** | **RESOLVES** |

## 3. Direct answer to the assigned question

For the **bounty prefix**, the absolute spelling gets the same boundary and confinement as the tilde
spelling, and the mirror fallback is confined identically:

- same boundary: `BOUNTY_PREFIXES` (`resolve.py:97`) lists the absolute spelling, `bounty_suffix`
  (`:201-215`) iterates both, and `bounty-literal-symlink-present` / `absolute-prefix-sibling-confusion`
  are the pinned consequences. m8 + d3 reproduce the sibling rejection on absolute bytes: fixed
  `GONE (domain=other)`, baseline `MIRROR-EQUIVALENT (domain=bounty)`.
- same fallback confinement: m5 (`../` + mirror-adjacent decoy) fixed `GONE` / baseline
  `MIRROR-EQUIVALENT`; m7 (symlink) identical; d2 reproduces it isolated.

For the **canonical mirror alias**, no: the absolute spelling is not in the registry at all, so the
absolute arm is asymmetric and cannot be pinned by the matrix (F1). For the **literal branch**, the
absolute form is not confined either — but that is now an explicitly documented carve-out (F4), and on
this host the absolute literal path does not exist, so the carve-out is unreachable there.

## 4. Findings

### F1 (primary). Absolute canonical-mirror citations are outside the registry, so the absolute form is only half-covered and cannot be expressed as a matrix case.

`MIRROR_CANDIDATES` (`resolve.py:106`) is tilde-only and `mirror_suffix` (`:187-199`) compares against
the tilde spelling and `os.path.expanduser()` of it — the *current* `HOME`. It never contains the
literal `/home/vgpnk` spelling, while `BOUNTY_PREFIXES` (`:97`) does contain its literal spelling. The
result is an asymmetry inside one classifier:

```
$ HOME=/tmp/…/fakehome python3 -c "<import resolve.py; print registries>"
BOUNTY_PREFIXES   = ('~/Projects/bounties', '/home/vgpnk/Projects/bounties')
MIRROR_CANDIDATES = ('~/Projects/the-bounty-hunter', '~/Projects/origin-work/the-bounty-hunter')
/home/vgpnk/Projects/bounties/x.md                bounty='x.md'   mirror=None
/home/vgpnk/Projects/the-bounty-hunter/server.py  bounty=None     mirror=None
```

Consequences, measured:

1. `/home/vgpnk/Projects/the-bounty-hunter/server.py:1` with `relocated/tbh/server.py` present is
   **GONE (other)** on *both* byte sets under `HOME=<case>/home` (m15) and **RESOLVES** on both under
   `HOME=/home/vgpnk` (m15-realhome). The absolute canonical cite is not treated as an alias in the
   harness; it degrades to a plain other-root literal.
2. It follows that the frozen matrix cannot express the absolute form of its own canonical-alias
   controls. I added the two cases verbatim to a scratch copy of the matrix
   (`/tmp/…/matrix-abs.json`, 17+3 cases) and ran the real checker:
   ```
   === fixed (8dd45bc8…) ===
   abs-canonical-alias-confined-control  control expect=RESOLVES  actual=GONE  FAIL path_check=missing-path
   abs-canonical-alias-escape            control expect=GONE      actual=GONE  PASS
   === baseline (d6a3c3f1…) ===   same two verdicts
   === mutantA (confinement removed, a0cb729a…) ===   same two verdicts
   ```
   The confined control fails on **every** byte set including a mutant with confinement deleted — so
   the failure is a harness property, not a resolver property; and the escape control passes on all
   three, including the mutant, so it is **vacuous**: it is GONE because the alias never matched, not
   because `under_mirror` rejected anything. A matrix extended this way would either report a resolver
   regression that does not exist or add a pin with no discriminating power.

Impact on current numbers: none observable. The live corpus contains exactly **one** distinct
absolute-form citation, `/home/vgpnk/Projects/bounties` (in `SKILL.md:9` and `corpus/README.md:4`),
classified `GONE, domain=bounty`; there are **zero** absolute canonical-mirror cites. The defect is
latent: it would surface the moment a citation is written as `/home/vgpnk/Projects/the-bounty-hunter/...`
(a form the lessons and round-5 record use in prose, see `corpus/lessons/round-5-…:11`), or as soon as
the lane is resolved with a `HOME` other than `/home/vgpnk`.

### F2. The absolute arm gained two cases but still has no `../` escape; that case is cheap and does discriminate.

The current matrix pins an absolute fallback control (non-`..`) and an absolute prefix-sibling escape,
but no absolute parent-traversal escape. I added one to the scratch matrix and ran the real checker:

```
abs-bounty-parent-traversal  escape expect=GONE
  fixed    (8dd45bc8…) → GONE              PASS
  baseline (d6a3c3f1…) → MIRROR-EQUIVALENT FAIL path_check=gone-with-path
  mutantA  (a0cb729a…) → MIRROR-EQUIVALENT FAIL path_check=gone-with-path
```

So the missing case is available in the existing schema (its decoy is mirror-side, no host write
needed) and it is sensitive to both the round-23 fix and the confinement mutation. Its absence is a
gap in the absolute-form evidence, and the code path it exercises (`suffix` from `BOUNTY_PREFIXES[1]`
with a `..` segment) is distinct from the two absolute cases already present.

### F3. The policy text promises `/home/<u>/Projects/bounties`; the code implements only `/home/vgpnk`.

Docstring (`resolve.py:26-31`) reads "`~/Projects/bounties` (or /home/<u>/Projects/bounties; root-only or
a `/`-delimited descendant…)". Measured with `HOME=/tmp/…/fakehome`:

```
bounty_suffix('/home/vgpnk/Projects/bounties/x.md') = 'x.md'
bounty_suffix('/home/other/Projects/bounties/x.md') = None
```

The `<u>` generalisation does not exist: the absolute side is a hardcoded user, so on any host whose
account is not `vgpnk` the absolute bounty spelling is not a bounty citation and falls to the generic
other-root literal. Falsifiable doc/impl mismatch; latent here (the lane runs as `vgpnk`, and the only
absolute corpus cite is for `vgpnk`). A `/home/<u>` implementation would also make the absolute form
`HOME`-parametric and therefore fixture-expressible without the constant rewrite F1 needs.

### F4. The literal branch is a documented carve-out, not a confinement gap — but the escape pins are conditional on an unenforced host premise.

`classify` still tests the literal path first in the bounty domain (`:228 m, p = exists_any(base)` →
`RESOLVES`) before any mirror join; `under_mirror` applies only to the fallback (`:232`). On the final
bytes this is declared (docstring `:30-33`, "CARVE-OUT: literal existence is reported as written") and
pinned by two controls whose notes say so. I confirm the behaviour independently:

- m9b: same cite as frozen `bounty-parent-traversal`, but with `home/Projects/bounties` present and
  `home/Projects/outside.md` planted → `RESOLVES`, `resolved_path`
  `<root>/home/Projects/bounties/../outside.md` (realpath `<root>/home/Projects/outside.md`, outside
  the selected mirror). Same on baseline.
- m10 / d5: symlink at the literal bounty path pointing outside the mirror → `RESOLVES`, path
  `<root>/home/Projects/bounties/evil.mjs`.
- The frozen escape version of the same cite is GONE only because `defaults.dirs` omits
  `home/Projects/bounties` and `os.path.exists` walks the filesystem instead of normalising lexically:
  ```
  target exists  : True            # home/Projects/outside.md
  traversal path : <root>/home/Projects/bounties/../outside.md
  os.path.exists : False           # intermediate bounties/ absent => ENOENT
  after mkdir bounties: True ; realpath → <root>/home/Projects/outside.md
  ```
- Mutation check on the final matrix: deleting that literal branch (sha `71701ff9…`) leaves the
  *current* matrix at `pass=17 fail=0`, while m9b/m10 flip `RESOLVES → GONE`. The two carve-out
  controls restore visibility in principle, but they are controls, so they pass on baseline too
  (baseline `pass=10` includes both) and cannot discriminate.
- Premise enforcement: `absolute-bounty-fallback-control`'s note admits the dependency ("requires
  `/home/vgpnk/Projects/bounties/ops/rank.mjs` to stay absent on the run host"), and `grep` over the
  checker finds no host/premise check (`host|premise` → no match; the only tolerance is
  `path_tolerance: carve-out` on `lane-relative-parent-internal-control`). If the premise breaks, the
  case fails as if the resolver regressed: d4 shows the absolute sibling spelling becoming `RESOLVES`
  once the literal exists. The receipt cannot distinguish "resolver changed" from "host changed".

None of this contradicts C1 as worded ("mirror fallback paths cannot credit …"); it bounds what the
`escape 7/7` line means. On this host the carve-out is unreachable for the absolute form (the literal
tree is absent) and reachable only for the tilde form.

### F5. The relative escape pin is lane-branch-shadowed, and unlike the internal control it has no carve-out tolerance.

m13 plants decoys at both candidate bases for `../outside-vault/secret.mjs`; the lane branch hits
first, so both byte sets return `INTERNAL` (`<root>/lane/../outside-vault/secret.mjs`), not GONE. The
frozen case is GONE only because its decoy sits at `relocated/outside-vault/…` and no lane-level
`outside-vault/` exists. That matches C1's explicit preservation of lane-relative semantics, and the
new checker records exactly this class for `lane-relative-parent-internal-control`
(`path_check=carve-out:path-outside-internal`) — but `relative-mirror-fallback-escape` has no
tolerance, so a legitimate INTERNAL there would be reported as a failure. Placement-conditional pin,
not a resolver defect.

### F6. Confinement covers symlinked directories; the matrix only exercises file-level symlinks.

m18 (`~/Projects/bounties/docs/x.md`, with `relocated/tbh/docs` → `<root>/secret`) is `GONE` on fixed
vs `MIRROR-EQUIVALENT` on baseline; m19 is the relative equivalent. `under_mirror`'s
`realpath`+`commonpath` handles directory symlinks; adding m18 to the matrix would be a discriminating
escape pin in the current schema (mirror-side decoy, no host write).

## 5. Suggested additions (not applied)

Three cases, scratch-verified through the real checker with the current matrix as base
(`matrix-abs.json` → 20 cases; run outputs in `receipt-abs-{fixed,baseline,mutantA}.json`):

```json
{"id": "abs-bounty-parent-traversal", "nature": "escape",
 "cite": "/home/vgpnk/Projects/bounties/../outside.md:1",
 "files": {"relocated/outside.md": "escaped file outside the selected mirror\n"},
 "note": "absolute arm, '../' segment; literal prefix must stay absent on the host",
 "expect": "GONE"},
{"id": "bounty-dir-symlink-escape", "nature": "escape",
 "cite": "~/Projects/bounties/docs/x.md:1",
 "dirs": ["relocated/tbh", "secret"],
 "files": {"secret/x.md": "directory symlink target outside the selected mirror\n"},
 "symlinks": {"relocated/tbh/docs": "@ROOT@/secret"}, "expect": "GONE"}
```
Both discriminate: fixed PASS, baseline FAIL (MIRROR-EQUIVALENT). Only after F1/F3 are addressed
(make `MIRROR_CANDIDATES` carry the literal absolute spelling, or make the case schema substitute the
absolute home) should an absolute canonical-alias case be added — as shown in F1, it currently fails
on all byte sets and the escape form is vacuous.

## 6. Scope limits

- Read-only on the lane: only this report was written. All trees, mutants, receipts, and the extended
  matrix live in `/tmp/kasegi-r23-falsify-AbsFormProbe`; the sole resolver mutation is the one-line
  `BOUNTY_PREFIXES` rewrite for `-abshome`, diffed in §1 (mutants A/B/C are additionally hashed in
  §7 and never touch the lane).
- No write to `/home/vgpnk/Projects/bounties` or `/home/vgpnk/Projects/outside.md` was attempted or is
  possible under lane bounds; the absolute literal branch is therefore demonstrated through the tilde
  form (m9b/m10) and the constant-rewrite variant (d1/d5).
- Class evidence is primary, as in the frozen matrix; `domain`/`method`/`resolved_path` are quoted
  where they change the reading. I do not judge whether `RESOLVES` of a `..` path is acceptable policy —
  the final bytes document it as a carve-out and I treat that as the claim's boundary.
- One host (`/home/vgpnk`, Linux), one Python, no network, no live-target traffic. No C2 artifact was
  probed. The artifacts moved three times while I measured; §7 records what each generation showed.

## 7. Superseded observations (kept for the record)

- **`//` separator false GONE at `ed9a9dae…`.** At the bytes pinned by the `c1-fixed.json` I was
  handed, `bounty_suffix` returned a leading-slash suffix, so `os.path.join(mirror_root, "/ops/rank.mjs")`
  discarded the mirror root:
  ```
  # ed9a9dae…, HOME=<case>/home
  bounty_suffix('~/Projects/bounties//ops/rank.mjs')        = '/ops/rank.mjs'
  bounty_suffix('/home/vgpnk/Projects/bounties//ops/rank.mjs') = '/ops/rank.mjs'
  mirror_suffix('~/Projects/the-bounty-hunter//server.py')   = 'server.py'   # already lstripped
  ```
  m11/m12 then classified fixed `GONE` vs baseline `MIRROR-EQUIVALENT` — a confined mirror hit
  rejected, contradicting `bounty_suffix`'s docstring ("the boundary matches mirror_suffix()'s").
  `9e0b5751…` added `.lstrip("/")` at `:211`; on the final bytes m11/m12 are `MIRROR-EQUIVALENT` on both
  byte sets. No live cite uses `//`, so no census number moved.
- **Matrix without absolute cases / without literal carve-out (13 cases, `5e61a33e…`).** At that
  generation every one of the 13 cites was tilde or relative, and the matrix kept `pass=13 fail=0`
  with the bounty literal branch deleted (mutant C, `02757bd4…` at the time), while m9b/m10 flipped
  `RESOLVES → GONE`. The current matrix (`5c64e014…`) closes both holes with two absolute cases and
  two carve-out controls; F1/F2 above describe what is still missing at that generation.
- **Mutant sensitivity of the current matrix** (mutants rebuilt from `8dd45bc8…`):
  ```
  A-no-confinement     a0cb729a…  fail=6   # 5 escapes + canonical-alias-escape-control
  B-prefix-sibling     91fb48cf…  fail=1   # bounty-prefix-sibling-confusion
  C-no-literal-branch  71701ff9…  fail=0   # carve-out controls are non-discriminating by design
  ```
  So the current `escape 7/7` does pin confinement and the root boundary; it does not pin the literal
  branch, which is why that branch is documented as a carve-out rather than tested.
