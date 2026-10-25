# AbsFormProbe — absolute `/home/vgpnk/Projects/bounties…` forms, and the frozen C1 matrix

Seat: `L1Kasegi23.AbsFormProbe-2` (leaf, falsify wave). Assigned question: build scratch fixtures for
citations spelled `/home/vgpnk/Projects/bounties/...`, the same path with a `../` escape, and
`/home/vgpnk/Projects/bounties-legacy/...` with a mirror decoy; report fixed-vs-baseline classes and
whether the absolute form is covered by the same boundary and confinement as the tilde form.

Class-level only: no admission, no score movement, no C2 claim. Only this report was written in the
lane; everything else lives in `/tmp/kasegi-r23-falsify-AbsFormProbe`. No package was installed
(nothing to record under the tooling directive).

## 0. Anchor and churn

The artifacts were edited four times by concurrent seats while I probed. Every number in §2–§5 was
re-measured on the generation below; the earlier generations are kept in §7 so a reader can tell which
claim each one supports.

Anchor (final measurement, `2026-10-25 03:46:52 -0300`):

```
resolve.py                         fce5b84be4cece914260f03a3a8b739dc1108381f97482bbfc7b22143810a4b0
mirror-containment-fixtures.json   4e39f65c7c1bdc7d6a390f0aeefe5fa88af67ea84659aa9ff36b84d271c2400b
mirror-containment-check.py       53742c8d9529dffb8c40c39b3448de7388b774b548d7831670598d5534bff5d1
c1-baseline-resolver.py           d6a3c3f1a1d8e97d42d66a8aa3cb34530b7bc1c18b194e487ef8d580d869f903
```

| when | resolve.py | matrix | checker | note |
|---|---|---|---|---|
| 03:28 | `ed9a9dae…` | `5e61a33e…` 13 cases | old (class-only) | generation I was handed |
| 03:40:40 | `9e0b5751…` | `5e61a33e…` | old | `bounty_suffix` gained `.lstrip("/")` |
| 03:42:37 | `8dd45bc8…` | `5e61a33e…` | old | literal branch documented as CARVE-OUT |
| 03:43:01 | `8dd45bc8…` | `5c64e014…` 17 cases | `53742c8d…` | +absolute cases, +carve-out controls, +`path_verdict`; receipts regenerated |
| 03:43:38 | `8dd45bc8…` | `4e39f65c…` 20 cases | `53742c8d…` | +brace/glob expansion cases |
| 03:46:26 | `fce5b84b…` | `4e39f65c…` | `53742c8d…` | current |

**Receipt drift, verified now:** `c1-fixed.json` and `c1-baseline.json` both record
`resolver 8dd45bc8… / matrix 5c64e014…` (17 cases) while the tree is `fce5b84b… / 4e39f65c…` (20
cases). They were consistent when written at 03:43 and are stale at 03:46. Neither pins the brace/glob
cases. This is a seal-time regeneration item, not a resolver defect.

Current matrix: 20 cases, 9 `escape`, 11 `control`; 13 `~/…` cites, 4 relative, **2 absolute**
(`absolute-bounty-fallback-control` → `MIRROR-EQUIVALENT`, `absolute-prefix-sibling-confusion` →
`GONE`), plus 2 literal-branch carve-out controls and 2 brace/1 glob expansion cases. Host state
(read-only): `/home/vgpnk/Projects/{bounties,bounties-legacy,outside.md,the-bounty-hunter,origin-work/the-bounty-hunter}`
are all **ABSENT**.

Re-derived totals (not quoted): fixed `cases=20 escape=9 controls=11 pass=20 fail=0`; baseline
`pass=12 fail=8` (5 mirror escapes, both prefix-sibling escapes, `brace-expansion-escape`,
`absolute-prefix-sibling-confusion`; `glob-expansion-escape` **passes** on baseline — see F1).

## 1. Method

`/tmp/kasegi-r23-falsify-AbsFormProbe/runner.py` materialises a case tree
(`home/Projects`, `lane`, `relocated/tbh`, per-case `dirs`/`files`/`symlinks` with `@ROOT@`
substitution), writes the cite into `lane/SKILL.md`, copies the selected resolver bytes to
`<case>/tool/resolve.py`, runs the real CLI with `HOME=<case>/home`,
`KASEGI_MIRROR=<case>/relocated/tbh`, cwd `<case>/tool`, and reads
`<case>/tool/citation-survival.tsv` (written next to the script, so cases stay isolated), reporting
`class`, `domain`, `method`, `resolved_path`.

Variants: `fixed` (= anchor bytes), `baseline` (`c1-baseline-resolver.py`), `*-realhome`
(`HOME=/home/vgpnk`), and `*-abshome` — the same bytes with **only** the literal prefix at
`resolve.py:97` rewritten to `<case>/home/Projects/bounties`, which is the minimum change that makes an
absolute-form case plantable and isolated (the frozen schema has no `HOME` substitution; setting
`HOME` does not affect an absolute cite). Diff is exactly one line:

```
@@ -97 +97 @@
-BOUNTY_PREFIXES = ("~/Projects/bounties", "/home/vgpnk/Projects/bounties")
+BOUNTY_PREFIXES = ("~/Projects/bounties", "/tmp/…/work/<case>/home/Projects/bounties")
```

Case sets: `cases.json` (m-series / d-series), `matrix-abs2.json` (current matrix + 4 probe cases),
`matrix-glob.json` (current matrix + 2 probe cases). Raw outputs `out-*.json`, checker receipts
`receipt-*.json` in the same directory. Mutants are rebuilt from the anchor bytes and hashed in §4/§7.

## 2. Classes: fixed vs baseline (anchor bytes)

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
| **m9b** | `~/Projects/bounties/../outside.md:1` | root **present**, target present | **RESOLVES** (`<root>/home/Projects/bounties/../outside.md`) | **RESOLVES** |
| **m10** | `~/Projects/bounties/evil.mjs:1` | literal symlink → `secret/outside.mjs` | **RESOLVES** | **RESOLVES** |
| m11 | `~/Projects/bounties//ops/rank.mjs:1` | `relocated/tbh/ops/rank.mjs` | MIRROR-EQUIVALENT | MIRROR-EQUIVALENT |
| m12 | `/home/vgpnk/Projects/bounties//ops/rank.mjs:1` | `relocated/tbh/ops/rank.mjs` | MIRROR-EQUIVALENT | MIRROR-EQUIVALENT |
| m13 | `../outside-vault/secret.mjs:1` | decoys at **both** candidate bases | INTERNAL (rel) | INTERNAL (rel) |
| **m14** | `/home/vgpnk/Projects/the-bounty-hunter/../../outside.md:1` | `outside.md` | **GONE (other)** | **GONE (other)** |
| **m15** | `/home/vgpnk/Projects/the-bounty-hunter/server.py:1` | `relocated/tbh/server.py` | **GONE (other)** | **GONE (other)** |
| m15-realhome | same, `HOME=/home/vgpnk` | same | **RESOLVES** (`<root>/relocated/tbh/server.py`) | **RESOLVES** |
| **m18** | `~/Projects/bounties/docs/x.md:1` | mirror **directory** symlink `docs` → `secret` | **GONE (bounty)** | **MIRROR-EQUIVALENT** |
| m19 | `docs/x.md:1` | same directory symlink | GONE (rel) | MIRROR-EQUIVALENT |

abshome variant (absolute form, isolated home, one-line constant rewrite):

| # | cite | planted | fixed-abshome | baseline-abshome |
|---|---|---|---|---|
| d1 | `<case>/home/Projects/bounties/../outside.md` | root present, target present | **RESOLVES** | **RESOLVES** |
| d2 | same | `relocated/outside.md` | **GONE** | **MIRROR-EQUIVALENT** |
| d3 | `<case>/home/Projects/bounties-legacy/README.md` | `relocated/tbh/-legacy/README.md` | **GONE (other)** | **MIRROR-EQUIVALENT** |
| d4 | same | literal sibling README | RESOLVES (other) | RESOLVES (bounty) |
| d5 | `<case>/home/Projects/bounties/evil.mjs` | literal symlink → `secret/outside.mjs` | **RESOLVES** | **RESOLVES** |

## 3. Answer to the assigned question

**Bounty prefix — yes, same boundary and same fallback confinement.** `BOUNTY_PREFIXES`
(`resolve.py:97`) carries the absolute spelling, `bounty_suffix` (`:201-215`) iterates both spellings,
and the absolute arm is now pinned by two matrix cases. Measured independently: m8/d3 (absolute prefix
sibling) fixed `GONE`, baseline `MIRROR-EQUIVALENT`; m5 (absolute `../` + mirror-adjacent decoy) fixed
`GONE`, baseline `MIRROR-EQUIVALENT`; m7 (absolute symlink escape) identical.

**Canonical mirror alias — no.** The absolute spelling is not in `MIRROR_CANDIDATES`, so an absolute
canonical cite is not an alias at all outside `HOME=/home/vgpnk` (F2), and the matrix cannot express
that case without failing for harness reasons.

**Literal branch — same (unconfined) treatment, now a declared carve-out.** The literal path is tested
before the mirror join for both spellings (`:228` then `:232`), so a `..` path or an outside-pointing
symlink reachable at the literal path is reported `RESOLVES`. The anchor bytes document this
(`:30-33`, "CARVE-OUT") and pin it with two controls; mutation now detects its removal (F4).

## 4. Findings

### F1 (primary, new). `glob-expansion-escape` cannot fail: its decoy is unreachable, and the confined control its note points to is a *brace* case.

Frozen case (`matrix 4e39f65c…`): cite `~/Projects/bounties/<name>.md:1`, `dirs:
["relocated/outside-vault"]`, `files: {"relocated/outside-vault/x.md": …}`, note "Placeholder rewrite
matches only outside the mirror through a relative hop; a confined glob match is the control below."

The classifier's glob path is `exists_any(os.path.join(mirror_root, suffix))` →
`PLACEHOLDER.sub("*", <mirror>/<name>.md)` = `<mirror>/*.md`. A bare `*` cannot cross `/` and there is
no `..` in the cite, so `<mirror>/*.md` can never see `relocated/outside-vault/x.md`. Measured through
the real checker with three byte sets:

```
glob-expansion-escape  escape expect=GONE
  fixed     (fce5b84b…) → GONE  PASS
  baseline  (d6a3c3f1…) → GONE  PASS
  mutant A  (9363fa94…, all three under_mirror checks deleted) → GONE  PASS
```

So the case passes on the do-nothing control, on the fixed bytes, and on a mutant with confinement
removed: it pins nothing. It is also the only escape case that baseline passes (baseline
`pass=12 fail=8`, and this is not among the eight).

The note's promised control does not exist: the only confined expansion control in the matrix is
`brace-expansion-confined-control` (`~/Projects/bounties/{ops,missing}/rank.mjs`), which exercises
`brace_expand`, not the placeholder/glob branch. There is no glob control at all.

The intent is achievable and discriminating — a hop in the cite is required. Scratch probe through
the same checker (`matrix-glob.json`, 22 cases):

```
probe-glob-hop-escape  escape expect=GONE
  cite "~/Projects/bounties/<name>/../../outside-vault/x.md:1",
  dirs ["relocated/tbh/sub"], files {"relocated/outside-vault/x.md": …}
  fixed    → GONE              PASS
  baseline → MIRROR-EQUIVALENT FAIL path_check=gone-with-path

probe-glob-confined-control  control expect=MIRROR-EQUIVALENT
  cite "~/Projects/bounties/<name>.md:1", files {"relocated/tbh/x.md": …}
  fixed → MIRROR-EQUIVALENT PASS ; baseline → MIRROR-EQUIVALENT PASS
```

`relocated/tbh/sub` must exist so the glob has a component to match before the `../..` hop; with that,
the fixed bytes reject the outside realpath while baseline credits it. This is the case the frozen
note describes, and it is absent.

### F2. Absolute canonical-mirror cites are outside the registry: the absolute form is half-covered and cannot be expressed as a matrix case.

`MIRROR_CANDIDATES` (`:106`) is tilde-only and `mirror_suffix` (`:187-199`) matches the tilde spelling
plus `os.path.expanduser()` of it — the *current* `HOME`. It never contains the literal `/home/vgpnk`
spelling, while `BOUNTY_PREFIXES` does. Registry dump (with `HOME` set away from `/home/vgpnk`):

```
BOUNTY_PREFIXES   = ('~/Projects/bounties', '/home/vgpnk/Projects/bounties')
MIRROR_CANDIDATES = ('~/Projects/the-bounty-hunter', '~/Projects/origin-work/the-bounty-hunter')
/home/vgpnk/Projects/bounties/x.md                bounty='x.md'  mirror=None
/home/vgpnk/Projects/the-bounty-hunter/server.py  bounty=None    mirror=None
```

Consequences:

- m15 `/home/vgpnk/Projects/the-bounty-hunter/server.py:1` with `relocated/tbh/server.py` present:
  `GONE (other)` on fixed **and** baseline under the checker's disposable `HOME`; `RESOLVES` on both
  under `HOME=/home/vgpnk` (m15-realhome). In the harness the cite is a plain other-root literal.
- The absolute spelling of the matrix's canonical-alias controls therefore cannot be added. Scratch
  matrix (`matrix-abs2.json`, 24 cases) through the real checker:
  ```
  abs-canonical-alias-confined-control  control expect=RESOLVES actual=GONE  FAIL path_check=missing-path
      fixed → FAIL ; baseline → FAIL ; mutant A → FAIL        (all three byte sets)
  abs-canonical-alias-escape            control expect=GONE     actual=GONE  PASS
      fixed → PASS ; baseline → PASS ; mutant A → PASS        (vacuous)
  ```
  The confined control fails for every byte set including the confinement-deleted mutant, i.e. the
  failure is a harness property; the escape form passes even with confinement removed, i.e. it has no
  discriminating power.
- Live impact: none yet. The corpus has exactly **one** distinct absolute-form citation,
  `/home/vgpnk/Projects/bounties` (`SKILL.md:9`, `corpus/README.md:4`) → `GONE, domain=bounty`, and
  **zero** absolute canonical-mirror cites. The defect is latent for a citation written as
  `/home/vgpnk/Projects/the-bounty-hunter/...` — a spelling the round-5 lesson quotes in prose
  (`corpus/lessons/round-5-aggregator-mirror-ambiguous-citation-base.md:11`) — or for any lane run with
  a different `HOME`.

### F3. The absolute arm has no `../` escape; the case is expressible today and discriminates.

Current absolute cases are a non-`..` fallback control and a prefix-sibling escape. A scratch
`abs-bounty-parent-traversal` (cite `/home/vgpnk/Projects/bounties/../outside.md:1`, decoy at
`relocated/outside.md`) run through the real checker:

```
fixed    → GONE              PASS
baseline → MIRROR-EQUIVALENT FAIL path_check=gone-with-path
mutant A → MIRROR-EQUIVALENT FAIL path_check=gone-with-path
```

It needs no host write (decoy is mirror-side) and exercises the absolute suffix together with `..`.
Its absence leaves the absolute-spelling `..` path unpinned.

### F4. The literal branch is a pinned carve-out, not a confinement gap; its pins are conditional on an unenforced host premise.

`classify` tests literal existence first in the bounty domain (`:228` → `RESOLVES`) and confines only
the fallback (`:232`). Documented at `:30-33` and pinned by `bounty-literal-present-traversal` /
`bounty-literal-symlink-present`. Independent confirmation and quantification:

- m9b (same cite as `bounty-parent-traversal`, but with `home/Projects/bounties` present and
  `home/Projects/outside.md` planted) → `RESOLVES`, path
  `<root>/home/Projects/bounties/../outside.md` (realpath `<root>/home/Projects/outside.md`, outside
  the mirror). m10/d5: symlink at the literal bounty path → `RESOLVES`. Same on baseline.
- Mechanism of the frozen GONE: `os.path.exists` walks the filesystem rather than normalising
  lexically, so with the bounty root absent the `..` path is ENOENT:
  ```
  target exists  : True     # home/Projects/outside.md
  traversal path : <root>/home/Projects/bounties/../outside.md
  os.path.exists : False    # intermediate bounties/ absent
  after mkdir bounties: True ; realpath → <root>/home/Projects/outside.md
  ```
- Mutation (anchor bytes): deleting the literal branch (`61ee0251…`) now fails exactly the two
  carve-out controls (`pass=18 fail=2`, both `path_check=missing-path`). So the matrix does observe
  the carve-out at this generation — my earlier "matrix blind to the literal branch" observation (§7)
  is superseded.
- Premise: `absolute-bounty-fallback-control`'s note admits the dependency ("requires
  `/home/vgpnk/Projects/bounties/ops/rank.mjs` to stay absent on the run host"). `grep` over the
  checker for `host|premise` finds nothing; the only tolerance mechanism is
  `path_tolerance: carve-out`, used solely by `lane-relative-parent-internal-control`. If the host
  premise breaks, the case fails indistinguishably from a resolver regression — d4 shows the absolute
  sibling spelling becoming `RESOLVES` once its literal exists. This is a reporting limitation, not a
  claim that C1 is wrong.

### F5. The relative escape pin is lane-branch-shadowed and has no carve-out tolerance.

m13 plants decoys at both candidate bases for `../outside-vault/secret.mjs`; the lane branch hits
first, so both byte sets return `INTERNAL` (`<root>/lane/../outside-vault/secret.mjs`), not GONE. The
frozen `relative-mirror-fallback-escape` is GONE only because no lane-level `outside-vault/` exists.
That matches C1's explicit preservation of lane-relative semantics, and the checker already has the
mechanism to record it (`lane-relative-parent-internal-control` →
`path_check=carve-out:path-outside-internal`) — but the escape case would report a legitimate INTERNAL
as FAIL. Placement-conditional pin.

### F6. Directory-symlink confinement is unexercised by the matrix but works and discriminates.

m18 (`~/Projects/bounties/docs/x.md`, `relocated/tbh/docs` → `<root>/secret`) fixed `GONE` / baseline
`MIRROR-EQUIVALENT`; through the real checker (`matrix-abs2.json`): `bounty-dir-symlink-escape`
fixed PASS, baseline FAIL, mutant A FAIL. `under_mirror`'s `realpath`+`commonpath` covers directory
symlinks; the matrix only exercises file-level symlinks.

## 5. Suggested corrections (not applied)

1. Replace `glob-expansion-escape` with the hop form and add its confined control (measured above):
   ```json
   {"id": "glob-hop-escape", "nature": "escape",
    "cite": "~/Projects/bounties/<name>/../../outside-vault/x.md:1",
    "dirs": ["relocated/tbh/sub"],
    "files": {"relocated/outside-vault/x.md": "glob hop target outside the mirror\n"},
    "expect": "GONE"},
   {"id": "glob-confined-control", "nature": "control",
    "cite": "~/Projects/bounties/<name>.md:1",
    "files": {"relocated/tbh/x.md": "confined glob match\n"},
    "expect": "MIRROR-EQUIVALENT"}
   ```
   Expected: hop case fixed PASS / baseline FAIL; control PASS on both (it is a control, so
   non-discrimination is correct there). If the current glob case is kept, its note should not claim a
   hop it does not have, and it should not claim a glob control that does not exist.
2. Add the absolute `../` escape and the directory-symlink escape (both measured discriminating):
   ```json
   {"id": "absolute-bounty-parent-traversal", "nature": "escape",
    "cite": "/home/vgpnk/Projects/bounties/../outside.md:1",
    "files": {"relocated/outside.md": "escaped file outside the selected mirror\n"},
    "note": "absolute arm; requires /home/vgpnk/Projects/bounties to stay absent on the host",
    "expect": "GONE"},
   {"id": "bounty-dir-symlink-escape", "nature": "escape",
    "cite": "~/Projects/bounties/docs/x.md:1", "dirs": ["relocated/tbh", "secret"],
    "files": {"secret/x.md": "directory symlink target outside the selected mirror\n"},
    "symlinks": {"relocated/tbh/docs": "@ROOT@/secret"}, "expect": "GONE"}
   ```
3. Only after F2 is addressed (put the literal absolute spelling into `MIRROR_CANDIDATES`, or let the
   case schema substitute the absolute home) add an absolute canonical-alias control; adding it now
   produces the `FAIL path_check=missing-path` / vacuous pair shown in F2.
4. Regenerate `c1-fixed.json` / `c1-baseline.json` against the current 20-case matrix and anchor bytes
   before sealing (§0).

## 6. Scope limits

- Read-only on the lane; only this report was written. All trees, mutants, receipts, and extended
  matrices live in `/tmp/kasegi-r23-falsify-AbsFormProbe`. The sole production-bytes mutation is the
  one-line `BOUNTY_PREFIXES` rewrite in the `-abshome` copies (diff in §1); mutants never leave /tmp.
- No write to `/home/vgpnk/Projects/bounties` or `…/outside.md` was attempted or is possible under lane
  bounds, so the absolute literal branch is demonstrated via the tilde form (m9b/m10) and the
  constant-rewrite variant (d1/d5), plus the ancestor-free `d4` class flip.
- Class evidence is primary, as in the frozen matrix; `domain`/`method`/`resolved_path`/
  `path_check` are quoted where they change the reading. I do not judge whether `RESOLVES` of a `..`
  path is acceptable policy — the anchor bytes declare it a carve-out and I treat that as the claim
  boundary.
- One host (`/home/vgpnk`, Linux), one Python, no network, no live-target traffic. No C2 artifact was
  probed. Because the tree moved four times, §0's anchor is the only generation to which the exact
  shas apply; the mechanisms (registry asymmetry, glob reachability, literal-first ordering,
  lane-first ordering) are structural and would survive a further byte edit.

## 7. Superseded observations (kept for the record)

- **`//` separator false GONE at `ed9a9dae…`.** At the bytes originally pinned by `c1-fixed.json`,
  `bounty_suffix` returned a leading-slash suffix, so `os.path.join(mirror_root, "/ops/rank.mjs")`
  discarded the mirror root:
  ```
  # ed9a9dae…, HOME=<case>/home
  bounty_suffix('~/Projects/bounties//ops/rank.mjs')          = '/ops/rank.mjs'
  bounty_suffix('/home/vgpnk/Projects/bounties//ops/rank.mjs') = '/ops/rank.mjs'
  mirror_suffix('~/Projects/the-bounty-hunter//server.py')     = 'server.py'   # already lstripped
  ```
  m11/m12 then classified fixed `GONE` vs baseline `MIRROR-EQUIVALENT`, contradicting
  `bounty_suffix`'s docstring ("the boundary matches mirror_suffix()'s"). `9e0b5751…` added
  `.lstrip("/")` at `:211`; on the anchor bytes m11/m12 are `MIRROR-EQUIVALENT` on both byte sets. No
  live cite uses `//`, so no census number moved.
- **Matrix without absolute cases or carve-out controls (13 cases, `5e61a33e…`).** At that generation
  every cite was tilde or relative, and the matrix stayed `pass=13 fail=0` with the bounty literal
  branch deleted (mutant `02757bd4…`), while m9b/m10 flipped `RESOLVES → GONE`. Superseded by
  `5c64e014…` (absolute cases + carve-out controls) and then `4e39f65c…` (expansion cases); on the
  anchor bytes the literal deletion is caught (2 fails, F4).
- **Mutant sensitivity at the anchor** (mutants rebuilt from `fce5b84b…`):
  ```
  A-no-confinement    9363fa94…  fail=7   # 5 mirror escapes + canonical-alias-escape-control + brace
  C-no-literal-branch 61ee0251…  fail=2   # both carve-out controls
  ```
  `glob-expansion-escape` is absent from A's failure list, which is the independent confirmation of
  F1: removing confinement does not change its verdict.
