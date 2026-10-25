# QuarterResolve — every way `resolve.py` returns a verdict that disk cannot re-derive

Seat: `L1Kasegi24.QuarterResolve` (scout, read-only). Item: enumerate (do not fix) the
non-re-derivable verdict surfaces of `corpus/instruments/resolve.py`.
No production file, lane tree, git/jj state, sibling lane or `/home/vgpnk/Projects/shokuknow`
was written. All probes ran on **byte copies** of the resolver inside disposable fixture trees
under `/tmp/qr*` — the lane's own `citation-survival.tsv` was never regenerated.

## 0. Bytes under test and how symbols were traced

| artifact | sha256 | lines | note |
|---|---|---|---|
| committed blob `git show master:corpus/instruments/resolve.py` | `690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d` | 597 | **byte-identical** to `.ufo/waves/round-24/c1-baseline-resolver.py` and to `d0a3f6a`; the item's "597 lines". **All line numbers below are this blob** (saved at `/tmp/r24-baseline-committed.py`). |
| working tree at 04:14 (in-flight patch) | `035f8844e66357f6dbe6f1158776978f2ce1103108e222d0746afdef9521b661` | 604 | `git status` shows ` M corpus/instruments/resolve.py` |
| working tree at 04:22 (in-flight patch, latest seen) | `99409e879570bdfe569cc2602b5d4995dd31d08f45c8ee6d201224b1b4585013` | 613 | survival claims re-measured here |
| `corpus/instruments/mirror-containment-check.py` | `dddd55496b55eb49138613e3b7143834412cdb104b7f8f6b6e85210f3dd98f8a` | — | the round-23 matrix runner |
| `corpus/instruments/mirror-containment-fixtures.json` | `d05b1e0cf62738ac8bf06497334c16a392089a5792ca9fd930f0cbf73e69b809` | 24 cases | 12 escape + 12 control |
| `corpus/instruments/resolve-dispatch-check.py` | `acbb687094f0fedb3517c744f0bcda68a4edd96ec760087e667fc70c6a0569e1` | — | counter-B runner (untracked, in flight) |
| `corpus/instruments/resolve-dispatch-fixtures.json` | `fef0f02d6d64cfb68702d245ecd156b6bb7eea95115c2a94216a10f8f9414c8c` | 8 cases (`L1 L2 L3 L4 C1 C2 C3 C4`) | was **rewritten while I read it** (an earlier revision used `notes/{,sub}/a.md` etc.) |

The `lsp` device is not mounted in this session (`read xd://lsp` → "No such tool: xd://lsp").
Callers were therefore traced textually, and that trace is recorded as such, not as semantic
proof: `test_resolve.py:117` copies and runs the CLI; `mirror-containment-check.py` and
`resolve-dispatch-check.py` copy and run it; `corpus/instruments/README.md:35,84-86,120-139`
publishes the class contract. The module has no importers — the only contract is the CLI.

**Nets measured before anything else** (so each finding can be scored against them):

```
$ python3 corpus/instruments/mirror-containment-check.py --resolver .ufo/waves/round-24/c1-baseline-resolver.py | tail -1
cases=24 escape=12 controls=12 pass=24 fail=0 resolver_sha256=690153ad… matrix_sha256=d05b1e0c…
$ python3 corpus/instruments/mirror-containment-check.py | tail -1          # working tree
cases=24 escape=12 controls=12 pass=24 fail=0 resolver_sha256=035f8844… matrix_sha256=d05b1e0c…
$ python3 corpus/instruments/resolve-dispatch-check.py --resolver .ufo/waves/round-24/c1-baseline-resolver.py | tail -2
cases=8 pass=4 exit=1
sha256 resolver=690153ad… matrix=fef0f02d… checker=acbb6870…
$ python3 corpus/instruments/resolve-dispatch-check.py | tail -2            # working tree
cases=8 pass=8 exit=0
```

So: the **24-case round-23 containment matrix passes on both the baseline and the patched bytes**
— it is a regression net for mirror confinement and cannot catch any dispatch-liveness or
disk-semantics defect below. The 8-case dispatch matrix is the only net with a fail-before face
(4/8 → 8/8), and it covers exactly two of the defect families (dropped empty brace alternative,
dangling first glob match).

## 1. Verdict table

`R23` = would the 24-case containment matrix catch it (case id if so). `L4` = would the four
frozen liveness cases catch it. `WIP` = does it survive the working-tree patch `99409e87`.

| # | finding | trigger shape (reachable through the extractor) | wrong verdict | R23 | L4 | WIP |
|---|---|---|---|---|---|---|
| Q1 | mirror root + HOME derived from the run environment (`121-130, 185, 219, 231, 321, 396`) | any `~/…` or mirror-domain cite, run under another `$HOME`/`$KASEGI_MIRROR` | `MIRROR-EQUIVALENT`/`RESOLVES` ↔ `GONE`; TSV records neither variable | no (matrix *fixes* both per case) | no | yes |
| Q2 | `os.path.expanduser` on `~user` (`185` via `260-262`) | `~vgpnk/…/QUALITY.md`, `~root/x.md` | resolves via `/etc/passwd`, outside the fixture HOME and outside the lane; `~`-spelling of the bounty root is **not** recognised by `BOUNTY_PREFIXES` (`109, 218-224`) → `GONE` where `/home/vgpnk/…` gives `MIRROR-EQUIVALENT` | no | no | yes |
| Q3 | `MIRROR_ABSENT` computed at import (`130`) and used **only** in the .md sentence (`396`) | mirror root absent/moved | every mirror-dependent row collapses to `GONE` with an empty method — indistinguishable in the TSV from a genuinely absent file; the .md says "fallback disabled", the code never gates on it | no | no | yes |
| Q4 | directories count as hits (`186, 190, 201` all use `os.path.exists`) | `corpus/`, `.git`, `/`, `~`, `~/Projects/**`, `<slug>/`, `dirs{,/entry.md}/` | `INTERNAL`/`RESOLVES`/`MIRROR-EQUIVALENT` for a directory; 20 such rows in the **committed** census | no — and `path_verdict` (`mirror-containment-check.py:144-158`) requires only `os.path.exists`+containment, so a directory case would *pass* | no | yes |
| Q5 | literal dangling symlink vs glob dangling symlink disagree (`186` follows links, `194-196` does not test) | `g/a_dangling.mjs` (literal) vs `g/<n>.mjs` (glob, `a_dangling.mjs` sorts first) | literal → `GONE`; glob → `INTERNAL` with a `resolved_path` that does not exist | no | **L3 catches the glob side**; literal side is a control | glob side fixed; literal side unchanged |
| Q6 | `exists()` conflates ENOENT, EACCES, ELOOP, EINVAL (`186,190,201`); `glob` also swallows unreadable dirs | `locked/x.md` where `locked/` is mode `000` and `x.md` exists | `GONE`, method `""`, no flag — a permission fact reported as absence | no | no | yes |
| Q7 | verdicts are one non-atomic snapshot: `collect()` reads text at `303`, `classify()` hits disk at `327` | any tree mutating during the run | rows of one report can describe different disk states | no | no | yes |
| Q8 | **brace 64-combination truncation** (`173-180`: `break` at `178` mid-DFS, `sorted(out)[:64]` at `180`) | `late/{a,b,c,d}4/{a,b,c,d}4/{a,b,c,d}4/{a,b,c,d}4/f.md` (256 combos; payload at the last combo) | `GONE` although the expansion exists — the retained 64 are the first DFS prefix, not the first sorted 64 | no (every brace case has 1-2 alts) | no | **yes** (cap unchanged at `184` of the WIP) |
| Q9 | **empty brace alternative dropped** (`175-176`) | `only/sighting{,-board}.sh`, `emptyalt/second.sh{,x}`, `~/Projects/bounties/{ops,}/rank.mjs` | `GONE` although the unsubstituted path is on disk | no | **L1/L2 (+ the mirror-fallback case) catch it** | fixed (`if alt.strip() or (not alt and len(alts) > 1)`) |
| Q10 | side effect of the Q9 fix: an empty alternative now credits a **directory** | `dirs{,/entry.md}/` | baseline `GONE` → patched `INTERNAL …/dirs/` (a directory); L1/L2 use file payloads, so no case sees it | no | no (cases use files) | yes (introduced) |
| Q11 | dedupe/order composition of the 64-window (`180` vs WIP `sorted(set(out))[:64]`) | `{a,a,…,b}` style sets | which 64 combos are tested depends on alternative multiplicity and DFS order; the docstring's "first existing expansion wins" (`71-72`) is false beyond 64 | no | no | yes |
| Q12 | **glob returns `matches[0]` with no existence test** (`194-196`) | `g/<n>.mjs` with a dangling symlink sorting first | `INTERNAL`/`MIRROR-EQUIVALENT` with a `resolved_path` no re-check corroborates | no | **L3 catches it** | fixed (`200-202` tests `os.path.exists` per match) |
| Q13 | "first **existing**" is not "first **confined**" | `~/Projects/bounties/sorted/<n>.mjs` where `a-lure.mjs` → outside the mirror and `z-real.mjs` is live+confined | `GONE` although a confined live match exists; the loop stops at the escaping match and `under_mirror` (`248`) then rejects the single result | no (no multi-match case) | no (`C3` pins first-sorted with two *in-lane live* matches) | **yes** |
| Q14 | **glob recursion** (`194` `recursive=True`) follows symlinked directories | `deep/**/t.md` with `deep/x/back -> deep` | `INTERNAL` to a ~40-level `x/back/x/back/…` path: the cycle expansion is the lexicographically first match | no | no | **yes** |
| Q15 | `GLOBMETA = "*?["` (`108`) rewrites ordinary punctuation into glob syntax; `<…>` (`107,192`) rewrites placeholders | `cc/[id].md` → `cc/i.md`; `q/a?.md` → `q/ab.md`; `corpus/lessons/round-*`; `<program>/<slug>` → `corpus/README.md`; `<slug>/` → `corpus/` | a class is credited to a file the citation does not name (all four are **live committed rows**) | no | no | yes |
| Q16 | brace and placeholder-glob are **not composed** (`188-196`: brace candidates are tested literally, then glob runs on the original `p`) | `compose/{aa,bb}/<n>.mjs` with `compose/aa/r.mjs` present | `GONE` although an expansion+glob match exists | no | no | **yes** |
| Q17 | numerator counts expansion credit without saying so (`359-364`); noise table counts only `GONE` (`371-374`) | `corpus/knowledge/*.md`, `corpus/lessons/round-*`, brace idiom | `method=glob|brace` rows enter the headline rate; synthetic tokens are invisible in the noise-of-GONE table (11 glob + 1 brace non-GONE rows in the committed TSV) | no | no | yes |
| Q18 | **the trailing-dot strip**, not SYMANCHOR: `rstrip(".,;:")` at `139` (and again `306`) | `../..` → `../`; `..` → `""` → dropped, no row; `sub/..:3` survives as `sub/..` | a cite ending in `..` denotes one level fewer than written (`../..` reported as the parent), and a bare `..` never becomes a row | no | no | yes |
| Q19 | one anchor form per token (`157-165`); `anchor_kind` returned but unused (`237`) | `sub/t.md::Heading:12`, `sub/t.md:12::Heading` | `GONE` although `sub/t.md` exists: `LINEANCHOR` and `SYMANCHOR` are alternatives, never applied in sequence | no | no | yes |
| Q20 | `is_pathlike` drops any token starting with `http` (`142`) | `httpdocs/conf.md` | no row at all — a real relative path vanishes before classification | no | no | yes |
| Q21 | wrong/partial root argument accepted (`317-323`) | `resolve.py <repo>/corpus`, or any non-repo dir | zero files, `distinct=0`, full report with `n/a` rates, **exit 0** (`594`) | no | no | **fixed** in WIP: `not a directory` → exit 2, `no citations collected` → exit 2, census not written |
| Q22 | missing `SKILL.md` or `corpus/` silently shrinks the denominator (`290, 291, 300`) | deleted/imisdirected `SKILL.md` | `0/0 = n/a` reported as a clean census; exit 0 | no | no | partially (empty-cites guard returns 2) |
| Q23 | self-input: the generated .md is excluded by exact relpath only (`135, 296`) | resolver copied to `<repo>/corpus/tools/` | run 2 reads run 1's report: `distinct=1` → `distinct=11`; falsifies the docstring's "byte-identical across consecutive runs" (`93-95`, echoed at `509`) | no | no | yes |
| Q24 | `under_mirror` applies to mirror credit only; the lane branch (`264-266`) and bounty literal branch (`241-243`) never realpath-confine | `lnk.md` → `/etc/passwd`; `sub/../outside.md`; `../MISSION.md:49-56` | `INTERNAL` for a path whose realpath is outside the lane, and an un-normalised `resolved_path` (`…/lane/sub/../outside.md`) | **partly pinned**: `lane-relative-parent-internal-control`, `bounty-literal-present-traversal`, `bounty-literal-symlink-present` pin the traversal/literal carve-outs — but there is **no lane-internal symlink case**, and `path_verdict` would flag `path-outside-internal` if one existed | no | yes |
| Q25 | anchor table silently drops rows whose `resolved_path` is a directory or unreadable (`524-533, 540-542`) | `sub/..:3`, `noread.md:1` | "anchors checked: N" undercounts with no reason printed (verified: 3 resolvable anchored cites, 1 row) | no | no | yes |

## 2. Detail on the items the brief named

### 2.1 Brace 64-combination truncation — Q8 (survives the patch)

`brace_expand` (`168-180`) expands depth-first and breaks as soon as the accumulator exceeds 64
(`178-179`), then sorts and truncates (`180`). The surviving set is therefore the **DFS prefix**,
not the lexicographically first 64 of the full set. Receipt (in-process, no CLI):

```
brace_expand[baseline] n=64  contains d4/d4/d4/d4: False  contains a4/a4/a4/a4: True
   first: late/a4/a4/a4/a4/f.md      last : late/a4/d4/d4/d4/f.md
brace_expand[wip]      n=64  contains d4/d4/d4/d4: False  contains a4/a4/a4/a4: True
```

and end-to-end, with the payload written at `late/d4/d4/d4/d4/f.md`:

```
late/{a,b,c,d}4/{a,b,c,d}4/{a,b,c,d}4/{a,b,c,d}4/f.md   baseline GONE   wip GONE
early/{a,b,c,d}4/{a,b,c,d}4/{a,b,c,d}4/{a,b,c,d}4/f.md  baseline INTERNAL  wip INTERNAL
```

The docstring's stated policy — "first existing expansion wins" (`71-72`) — does not hold past
rank 64. Caught by round-23 matrix: **no** (its brace cases carry one or two alternatives:
`brace-expansion-escape`, `brace-expansion-confined-control`). Caught by the four liveness cases:
**no**. Present at `99409e87:184`.

### 2.2 Sorted-order determinism — Q8/Q11/Q12/Q15

`sorted()` is used in five verdict-relevant places, and none of them is stable against the *tree*:

- `sorted(cites)` (`326`) — row order only, deterministic.
- `sorted(out)[:64]` (`180`) — deterministic per string, but the *selection* is DFS-order and
  multiplicity dependent (Q11).
- `sorted(globmod.glob(q, recursive=True))` (`194`) — deterministic per tree; **the winner is a
  function of the tree, not of the citation**. Live proof in the committed TSV: `<slug>/` resolves
  to `corpus/`, `<program>/<slug>` to `corpus/README.md`, `corpus/lessons/round-*` to
  `…/round-1-aggregator-audit.md`. Adding any sibling that sorts earlier (`aaa/`) silently moves
  the `resolved_path`, and adding one that sorts after the only match cannot change it.
- `sorted(anchors)` (`557`) — tuples with `n2 = None`; comparable only because `cite` is the first
  element and unique, so no `TypeError` today (fragile, not broken).
- `sorted(rows, key=…)` (`346`) — report order only.

### 2.3 Empty alternatives — Q9/Q10 (fixed, with a new side effect)

Baseline drops `""` alternatives (`175-176`). Receipts:

```
only/sighting{,-board}.sh       baseline GONE      wip INTERNAL  lane/only/sighting.sh
emptyalt/second.sh{,x}          baseline GONE      wip INTERNAL  lane/emptyalt/second.sh
dirs{,/entry.md}/               baseline GONE      wip INTERNAL  lane/dirs/        <- a DIRECTORY
```

The first two are exactly what `L1`/`L2` (and the mirror-fallback case) pin. The third is a class
the patch newly awards to a directory (Q4 + Q10) that no case in either net exercises. The patch
also narrows bare `{}` (`len(alts) > 1`), so `{}` still expands to nothing — that behavior is
`brace_expand` → `[]`, and `exists_any` then falls through to the glob branch against the literal
`{}` string.

### 2.4 `os.path.expanduser` on `~user` — Q2

`exists_any` expands before anything else (`185`); `classify` routes any `~…` base to the
"other" domain (`260-262`) after `bounty_suffix`/`mirror_suffix` have failed to match
`BOUNTY_PREFIXES`/`MIRROR_CANDIDATES`, which are hardcoded to `~/…` or `/home/vgpnk/…` (`109,
119-120`). Consequences, measured with `HOME=/tmp/qr*/home` (a fake home with no `Projects`):

```
~vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md  RESOLVES  /home/vgpnk/…/QUALITY.md   <- escaped the fixture HOME
~vgpnk/Projects/bounties/ops/rank.mjs                       GONE      (other domain, no mirror fallback)
/home/vgpnk/Projects/bounties/ops/rank.mjs                  MIRROR-EQUIVALENT mirror/ops/rank.mjs
~/Projects/bounties/ops/rank.mjs                            MIRROR-EQUIVALENT mirror/ops/rank.mjs
~root/no-such-cite-qr/x.md                                  GONE
```

So two spellings of the same location get different fallback policies, and a `~user` cite is
re-derivable only on a host whose passwd database agrees. Neither net has a `~user` case; the
24-case fixture's only absolute spelling is `absolute-bounty-fallback-control`, and its own note
already declares that case host-dependent ("requires /home/vgpnk/Projects/bounties/ops/rank.mjs to
stay absent on the run host").

### 2.5 Glob recursion — Q14

`recursive=True` is always passed (`194`), so a *literal* `**` in a citation is a recursive
descent, not a single-level wildcard; and `glob` follows symlinked directories when recursing.
Receipt with `deep/x/back -> deep`:

```
deep/**/t.md  INTERNAL  /tmp/qr4/lane/deep/x/back/x/back/…(x40)…/x/y/z/t.md   (baseline and 99409e87)
python3 -c "glob.glob('.../deep/**/t.md', recursive=True)" -> 41 matches, 0.004 s
```

41 matches out of a one-file tree; the sorted-first is a cycle artifact. A `<**>` *placeholder*
does not do this — `PLACEHOLDER.sub("*")` (`192`) replaces `<**>` with a single `*` (verified:
`deep/<**>/t.md` → `GONE`), so the recursive spelling is only reachable when `**` is literal in
the corpus text. Not covered by `glob-expansion-escape` (single-level `<name>` plus `..`).

### 2.6 Dangling symlinks — Q5/Q12

Baseline credits `matches[0]` without testing it (`194-196`):

```
g/<n>.mjs          baseline INTERNAL lane/g/a_dangling.mjs   (os.path.exists -> False)
                   wip      INTERNAL lane/g/b_live.mjs
g/a_dangling.mjs   baseline GONE      wip GONE               (literal branch follows the link)
```

`L3` catches the glob side and the working tree fixes it (`200-202`). The two branches still
disagree about a dangling symlink — literal `GONE`, glob (now) `GONE` only because the loop skips
it; the class is the same but the *reason* is not recorded (`method` is `""` for the literal case,
which is indistinguishable from a missing file).

### 2.7 Directories as hits — Q4

`os.path.exists` is true for directories at all three probes (`186`, `190`, `201`). The committed
census carries **20** such rows; the load-bearing ones:

```
INTERNAL literal rel '.git'    -> …/kasegi-shokunin/.git
INTERNAL literal rel 'corpus/' -> …/kasegi-shokunin/corpus/
RESOLVES literal other '/'     -> /
RESOLVES literal other '~'     -> /home/vgpnk
RESOLVES glob    other '~/Projects/**' -> /home/vgpnk/Projects/
INTERNAL glob    rel   '<slug>/'      -> …/corpus/
INTERNAL glob    rel   'corpus/**'    -> …/corpus/
```

Nine of the ten `RESOLVES` rows in the committed TSV are of this kind (`/`, `/home`,
`/home/vgpnk`, `/tmp`, `~`, `~/Projects`, `~/Projects/**`, `~/Projects/ufo-fsd-alpha` ± trailing
slash); the tenth is a real file **outside the lane**,
`~/Projects/ufo-fsd-alpha/scripts/ufo-sighting.mjs` → `/home/vgpnk/Projects/ufo-fsd-alpha/…`. So
the census of record's `RESOLVES` class contains **no lane-repo file**: it is nine root/home
hits plus one other-project hit, all of them Q1/Q2 host facts. Also note the
`file_lines` interaction (`524-533`): a directory or unreadable path returns `None` and the anchor
row is dropped silently (Q25). Neither net has a directory-as-hit case, and
`mirror-containment-check.py:144-158` would accept one.

### 2.8 The `..`-strip is **not** in SYMANCHOR — Q18

`SYMANCHOR = r"::[A-Za-z_][A-Za-z0-9_.]*$"` (`106`, applied at `162`) has no `..` logic: it
permits `.` inside the *symbol* name and removes the `::symbol` suffix. The only `..` strip is
prose-punctuation cleanup, applied twice:

- `is_pathlike`: `t = tok.strip().rstrip(".,;:")` (`139`)
- `collect`: `t = m.group(1).strip().rstrip(".,;:")` (`306`)

Receipts:

```
'..'     -> rstrip -> ''        -> is_pathlike False -> no row at all
'../..'  -> rstrip -> '../'     -> INTERNAL  /tmp/qr3/lane/../     (parent, not grandparent)
'sub/..:3' -> base 'sub/..'     -> INTERNAL  /tmp/qr3/lane/sub/..  (directory, un-normalised)
```

`classify`'s only `..` guard is the exact-string tuple at `267` — and it sits *after* the lane
branch (`264-266`), so it cannot stop `..` in the lane domain even if it survived extraction.
Consequence for the census: citations that end in `..` are invisible (no row), and citations that
carry `..` mid-path produce un-normalised `resolved_path` values (`../MISSION.md:49-56` is a live
committed row of exactly this shape). The round-23 matrix pins only `lane-relative-parent-internal-control`
(`../outside.md` → `INTERNAL`, `path_tolerance: carve-out`), i.e. it pins the *class* for a form
that never ends in dots. Neither net catches the strip.

### 2.9 A class returned without an `exists` check — exactly one place

- `exists_any` literal (`186-187`) — checked.
- `exists_any` brace (`189-191`) — checked per candidate.
- `exists_any` **glob (`194-196`)** — **unchecked**: `if matches: return "glob", matches[0]`.
  This is the only site; `L3` exercises it and the working tree closes it.
- `classify` (`236-271`) — every branch returns only after `m` is truthy, including the
  root-only suffix cases, which call `exists_any(mirror_root)` (a directory, so "exists").
- `mirror_suffix`/`bounty_suffix` (`200-225`) return a suffix, never a verdict.
- The report's anchor verdict (`540-560`) is derived from `file_lines`, which never checks
  `isfile`; a directory or unreadable file yields `None` and the row is dropped instead of being
  reported (Q25). That is an omission, not an unchecked class.

### 2.10 Environment and report-contract findings (Q1/Q3/Q21/Q23)

- `MIRROR_ROOT`/`MIRROR_ABSENT` are module-level (`129-130`); the TSV header (`345`) carries no
  mirror or HOME column, so mirror-domain rows are only re-derivable together with the .md.
- `MIRROR_ABSENT` appears at exactly two lines — `130` and the sentence at `396`
  (`grep -n MIRROR_ABSENT` on the baseline blob). No code path consults it.
- Wrong root: `resolve.py <repo>/corpus` → `distinct=0 … all=0/0`, exit 0, and a 116-line report
  written. The working tree now refuses (`not a directory` → 2; `no citations collected` → 2).
- Self-input: a copy at `<repo>/corpus/tools/resolve.py` → run 1 `distinct=1`, run 2
  `distinct=11` (10 of them harvested from its own `<repo>/corpus/tools/citation-survival.md`),
  because `GENERATED_REPORT` (`135`) excludes only `corpus/instruments/citation-survival.md`
  (`296`). The docstring determinism clause (`93-95`, echoed at `509`) therefore holds only for the canonical
  install location.

## 3. Would the frozen dispatch cases catch the *named* defects?

Against the observed fixture (`fef0f02d`, ids `L1 dir/{,sub}/file.md`, `L2 dir/{sub,}/file2.md`,
`L3 glob/<n>.md`, `L4 brace/{alpha,beta}.md`, controls `C1`–`C4`):

- `L1`, `L2` — discriminate the dropped empty alternative (baseline `GONE`, patched `INTERNAL`).
- `L3` — discriminates the unchecked glob match via the **path** column (`path-missing-on-disk`
  on baseline), which is the stronger half of the assertion; class alone is identical.
- `L4` as *worded in the frozen prompt* ("brace where the first alternative names a dangling
  symlink and the second is live") **cannot be liveness-positive**: the brace loop already tests
  each candidate with `os.path.exists` (`189-191`), so a dangling first alternative is skipped on
  the baseline. Measured: `brace/{alpha,beta}.md:1` with `alpha.md` a dangling symlink →
  `INTERNAL …/brace/beta.md` on **both** byte sets. It is a control, not a falsifier; if the L4
  slot is meant to be liveness-positive it needs a shape the baseline answers wrongly (the
  mirror-fallback empty alternative used in the earlier fixture revision was such a shape).
- `C2` (`GONE`) and `C3` (`first sorted match of two live in-lane matches`) are the only controls
  that constrain the selection order; neither constrains confinement (Q13) or directories (Q4).

## 4. Drift observed while working (recorded, not judged)

| time (local) | artifact | change |
|---|---|---|
| 04:09 | `.ufo/waves/round-24/c1-baseline-resolver.py` | frozen baseline = `690153ad` (= committed HEAD blob) |
| 04:14:32 | `corpus/instruments/resolve.py` (lane, untracked-mod) | `035f8844`, 604 lines: empty-alt kept, glob per-match exists test |
| 04:22:23 | `corpus/instruments/resolve.py` (lane) | `99409e87`, 613 lines: adds `alt.strip() or (…len(alts) > 1)`, `sorted(glob)` loop, `not a directory` guard (rc 2), `no citations collected` guard (rc 2) |
| 04:11–04:20 | `corpus/instruments/resolve-dispatch-{check,fixtures}` | untracked, **rewritten between two of my reads**; the 8 case ids changed citations (`notes/{,sub}/a.md` → `dir/{,sub}/file.md`) |
| 04:2x | `corpus/instruments/source-recheck.py`, `corpus/source-snapshots/round-23/manifest.json` | also ` M` in `git diff --stat` |

Because the lane file is being edited under this seat, every "WIP" cell above was re-measured on
`99409e87`; line numbers for it, if they shift again: `brace_expand 168`, `exists_any 187`,
`classify 242`, `collect 293`, `main 322`.

## 5. Unverified / out of reach

- **Bind mounts and overlayfs** cannot be seen by `realpath` — a mirror-internal mount that
  escapes would pass `under_mirror` (`228-233`). Untestable here (host package/mount operations
  are paused).
- **Locale/filesystem-encoding effects** on `sorted()` of decoded names are not measured;
  `sorted` is code-point order, so this is low risk, but a non-UTF-8 filename would enter as
  surrogate escapes and reorder matches. Marked UNVERIFIED.
- **`glob` symlink-loop depth** is bounded by the interpreter (41 matches, 0.004 s on 3.14.8), not
  by the resolver; behaviour on another Python version is UNVERIFIED.
- No live census delta was measured: running the resolver against the lane writes
  `corpus/instruments/citation-survival.tsv`, which a read-only seat may not do. All counts above
  are from byte-copy replays; the 20-directory and 10-`RESOLVES` figures are read from the
  committed capture `corpus/instruments/citation-survival.tsv` (1480 rows).

## 6. Reproduction (scratch, all under `/tmp`)

```
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show master:corpus/instruments/resolve.py \
  > /tmp/r24-baseline-committed.py            # the 597-line blob every line number refers to

python3 /tmp/qr/probe.py                      # 23-citation fixture; runs baseline + the LIVE lane
                                              #   bytes. NOTE: its right-hand column label is a
                                              #   literal string ("wip(035f8844)"); the bytes it
                                              #   executes are whatever corpus/instruments/resolve.py
                                              #   is at run time. Both 035f8844 and 99409e87 gave
                                              #   the classes quoted in §2.
python3 /tmp/qr2/probe2.py                    # symlink escape, multi-match mirror, EACCES, anchor
                                              #   forms; exits at its copytree step after printing
                                              #   every class (the chmod-000 fixture blocks copytree)

# inline heredocs (not saved as files), same pattern: build a lane under /tmp with a one-line
# SKILL.md per citation, copy the resolver into a work dir, run with HOME=/tmp/... and
# KASEGI_MIRROR=/tmp/..., read citation-survival.tsv:
#   /tmp/qr4 — first-confined, **-recursion, 64-cap survivors, anchor combos (prints the sha of
#              the bytes it executes)
#   /tmp/qr5 — '?'/'[' glob rewrite, unclosed bracket
#   /tmp/qr2 lane3/subroot — self-input and wrong-root runs
```
