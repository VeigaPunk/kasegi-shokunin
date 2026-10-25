# DocstringTruth — `resolve.py` policy text vs. landed `classify()` bytes

Seat: `L1Kasegi23.DocstringTruth-2` (reviewer, leaf). Round 23 FALSIFY wave.
Read-only against the repo: the only repo write is this file. All mutation and CLI replay ran
under `/tmp/kasegi-r23-falsify-DocstringTruth-2`. No git/jj command, commit, or index touch.
No installs.

Axis attacked: **depth:verifiability** — does the detector's documented policy, and the receipt
that certifies it, describe the bytes and the matrix actually on disk?

**Pinned artifact set** (hashes re-checked after writing this report):

| artifact | sha256 | mtime |
|---|---|---|
| `corpus/instruments/resolve.py` | `fce5b84be4cece914260f03a3a8b739dc1108381f97482bbfc7b22143810a4b0` | `03:46:26 -0300` |
| `corpus/instruments/mirror-containment-fixtures.json` | `4e39f65c7c1bdc7d6a390f0aeefe5fa88af67ea84659aa9ff36b84d271c2400b` (20 cases) | `03:43:38 -0300` |
| `corpus/instruments/mirror-containment-check.py` | `53742c8d9529dffb8c40c39b3448de7388b774b548d7831670598d5534bff5d1` | `03:43:01 -0300` |
| `.ufo/waves/round-23/c1-fixed.json` | `21b85212…`, `generated_at 2026-10-25T06:46:26Z`, pins resolver `fce5b84b…`, matrix `4e39f65c…`, checker `53742c8d…`, `20/20` | `03:46:26` |
| `.ufo/waves/round-23/c1-baseline.json` | `8ad926ed…`, `generated_at 2026-10-25T06:46:27Z`, pins baseline `d6a3c3f1…`, same matrix/checker, `12/20` | `03:46:27` |
| `.ufo/waves/round-23/c1-baseline-resolver.py` | `d6a3c3f1a1d8e97d42d66a8aa3cb34530b7bc1c18b194e487ef8d580d869f903` | `03:28` |

## 1. What moved during this review (pin discipline, not a finding)

The tree was edited four times while the audit ran. Recorded so every number below can be tied to
bytes; I wrote none of it and reverted none of it.

| set | resolver sha | fixtures | checker |
|---|---|---|---|
| **A** 03:27:44 | `ed9a9dae…` | 13 cases `5e61a33e…` | `1bc2db10…` |
| **B** 03:40:40 | `9e0b5751…` | 13 cases | `1bc2db10…` |
| **C** 03:42:37 | `8dd45bc8…` | 20 cases `4e39f65c…` (03:43:38) | `53742c8d…` (03:43:01) |
| **D (pinned)** 03:46:26 | `fce5b84b…` | 20 cases (unchanged) | unchanged |

A→D is: the BOUNTY/REL policy paragraphs rewritten to disclose the literal and INTERNAL
carve-outs (`:26-38`, `:52-64`, `:72-75`); `bounty_suffix().lstrip("/")` (`:220`); the root-only
mirror-mapping guard toggled twice — enabled in B/C (`… if suffix else mirror_root`), then
deliberately reverted in D to `(None, None)` with the comment at `:240-242`; and
`max(..., default=0)` for empty row sets (`:359-360`). The matrix grew 13→17→20 cases. The
receipts were regenerated at 03:46:26–27 against the 20-case matrix, so receipt and tree now
agree; see §4 history for the stale-receipt window.

## 2. Method

Each probe is an isolated case root with its own `HOME`, `KASEGI_MIRROR` and lane repo; the real
`resolve.py` is copied to `<case>/tool/resolve.py` and executed as the CLI; rows are read from the
CLI's own `citation-survival.tsv`. Same replay shape as `mirror-containment-check.py`.

```bash
S=/tmp/kasegi-r23-falsify-DocstringTruth-2
env -i HOME=$S/k/home KASEGI_MIRROR=$S/k/relocated/tbh PATH=/usr/bin:/bin \
       LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
       python3 $S/k/tool/resolve.py $S/k/lane
```

Tooling (role requirement): **no LSP device is mounted** (`read xd://lsp` → `No such tool: xd://lsp`).
Caller/definition/diagnostics checks were impossible; the ledger rests on line-addressed reads,
`grep`, and executed CLI rows, and nothing here is offered as semantic proof.

## 3. Policy ledger on the pinned bytes

| docstring lines | statement | implementing lines | verdict |
|---|---|---|---|
| 26-29 | BOUNTY = EXACT root; root-only or `/`-delimited descendant; prefix sibling `bounties-x/...` never enters the domain | `:106`, `:210-221`, `:233-235` | **MATCH** — `~/Projects/bounties-x/f.md` → `other`/`RESOLVES`; `~/Projects/bounties-legacy/README.md` → `GONE` |
| 30-33 | literal `exists` → `RESOLVES` **as written**, even when `../` resolves outside the bounty root ("CARVE-OUT") | `:237-239` | **MATCH** — matrix `bounty-literal-present-traversal` / `bounty-literal-symlink-present` both `RESOLVES`; direct row keeps the raw `..` path |
| 33 | "the matrix pins this class as a control" | those two cases | **MATCH** (pinned set D) |
| 34-38 | fallback: same relative path under mirror **and realpath-confined**, else GONE | `:243-246`, `:224-229` | **MATCH** — all 8 discriminating escape cases flip credit→`GONE`; brace-expanded escape included |
| 34-38 (root-only) | for a root-only BASE, "same relative path exists under the mirror" would credit the mirror root | `:243` (`if suffix else (None, None)`) + comment `:240-242` | **STALE-BY-OMISSION** (F3) — root-only cites are GONE; only the code comment says so |
| 39-46, 48-51 | OTHER: `~`/`/` root → exists? `RESOLVES` : `GONE`; canonical alias first, selected root only, root-only/trailing slash, realpath-confined | `:247-258`, `:196-207` | **MATCH** — alias resolves under the relocated root; `the-bounty-hunter-x/f.md` → `other`; alias escape → `GONE` |
| 46-47 | "`[lost-base]`/`[lost-tree]`-marked tokens are not aliases" | **none** | **UNANCHORED** (F4) |
| 52-60 | REL: lane repo first; `INTERNAL` not confined (`../` or repo symlink outside the lane still `INTERNAL`, "by prior design; r23 did not change this branch and the matrix pins it") | `:259-262`; `lane-relative-parent-internal-control` | **MATCH** — `../outside.md` → `INTERNAL`, path `…/lane/../outside.md`; `lane/leak.md → vault` → `INTERNAL` |
| 61-63 | mirror fallback only when realpath-confined; walk-outs and symlink escapes GONE | `:263-266`, `:224-229` | **MATCH** (matrix) |
| 66-67 | literal `os.path.exists(expanduser(path))` | `:180-184` | **MATCH** |
| 68-69 | brace: sorted, ≤64 combos, first existing wins | `:164-177`, `:185-189` | **MATCH** (cap enforced; empty alternatives silently skipped — undocumented, harmless) |
| 70-71 | glob: `<...>`→`*`, sorted first match, zero matches does not resolve | `:190-193` | **MATCH with note** (`recursive=True`; globbing also triggers on any `*?[`, not only `<...>`) |
| 72-74 | every class except GONE resolves by construction; INTERNAL includes a `../` walk-out past the lane | `:238-266` | **MATCH** |
| 75 | non-resolving relative token is GONE, "sub-kind `rel-unresolved`" | **none**; no sub-kind column | **UNANCHORED** (F4) |
| 2 | header "r15 … fixes r18" | body cites r23 at `:32`, `:60`; header does not | **STALE** (F1) |
| 107-114 (round-19 block) | "all other explicit roots keep the plain exists? RESOLVES : GONE behavior" | `:256-258` true for OTHER non-aliases; BOUNTY is also an explicit root but has the fallback `:243-246` | **STALE/ambiguous** (F1) |
| 386 (generated) | "r18 definition" | definition changed in r23 | **STALE** (F1) |
| 391-392 (generated) | prints the selected/derived mirror root | uses `MIRROR_ROOT` | **MATCH** |
| 509-511, 559 (generated) | "Sep-5 genesis mirror `~/Projects/the-bounty-hunter`" | mirror derived (`:107-125`); contradicts `:391` in the same emitted document | **STALE** (F1) |

## 4. Findings

### F1 — MEDIUM-LOW (stale prose that a verifier reads first)

All four artefacts still carry pre-r23 labels, and one of them contradicts itself inside the same
generated document. Observed on a pinned-set run with a relocated mirror:

```
/tmp/…/k/tool/citation-survival.md:3    Instrument: `corpus/instruments/resolve.py` (…; r18 definition).
/tmp/…/k/tool/citation-survival.md:7    Mirror root for bounty-path equivalence: `/tmp/…/k/relocated/tbh`.
/tmp/…/k/tool/citation-survival.md:89   … the Sep-5 genesis mirror `~/Projects/the-bounty-hunter` …
```

- `:2` still says *"r15 … self-input/leading-dot fixes r18"* while the same docstring now cites
  **r23** at `:32` and `:60`. The header contradicts the body.
- The generated report says *"r18 definition"* (`:386`) and, in §Honest scope limits, names a fixed
  genesis mirror (`:509-511`, `:559`) although the same document prints the actually selected root
  at `:391-392`.
- The round-19 comment block (`:107-114`) still claims *"all other explicit roots keep the plain
  exists? RESOLVES : GONE behavior"*. The BOUNTY domain is an explicit root and does **not** keep
  plain behaviour (it has the confined fallback). The sentence is true only for OTHER-domain
  non-aliases and needs the scoping its sibling paragraphs received.

Prose only — this does not change any classification — but it is the first thing a reader uses to
identify which revision produced a receipt.

### F2 — MEDIUM-LOW (fixture truth): `glob-expansion-escape` does not test confinement

The case is counted among the escapes but classifies identically before and after the fix. Pinned
set D, fixture shape (mirror has no `.md`; the only markdown is `relocated/outside-vault/x.md`):

```
~/Projects/bounties/<name>.md:1   GONE   (no method; domain bounty)
```

It is GONE for the documented zero-match reason, not because a match was rejected: the pattern is
`mirror_root/*.md`, and `*` cannot cross `/` to reach `relocated/outside-vault/x.md`. Adding one
file *inside* the mirror proves the mechanism:

```
# same case + relocated/tbh/inside.md
~/Projects/bounties/<name>.md:1   MIRROR-EQUIVALENT   …/relocated/tbh/inside.md   glob   bounty
```

And the baseline resolver returns `GONE` for the fixture shape as well
(`--resolver .ufo/waves/round-23/c1-baseline-resolver.py` → this case PASSES on the baseline).
So the case pins "no match existed", not "an outside match was refused". Its own note claims the
opposite mechanism — *"Placeholder rewrite matches only outside the mirror through a relative hop"* —
but the citation contains no relative hop and the outside file is unreachable by the pattern.

Effect on the wave's arithmetic: of the **9** escapes in the pinned matrix, **8 are discriminating**
(they flip from a credit class on the baseline to GONE on D). `glob-expansion-escape` is the ninth
and is not. It should gain a `..`/`**` so it actually reaches the outside file, or be reclassified
as a control so the escape count is honest.

### F3 — LOW (doc/policy gap): root-only BOUNTY citations are GONE, and only a code comment says so

Pinned set D, canonical root absent, mirror present (case `k`):

```
~/Projects/bounties	GONE		1		bounty	1	SKILL
~/Projects/bounties/	GONE		1		bounty	1	SKILL
~/Projects/bounties/ops/rank.mjs:1	MIRROR-EQUIVALENT	…/relocated/tbh/ops/rank.mjs	1	literal	bounty	1	SKILL
```

The module policy at `:34-38` says an unsuccessful literal is followed by *"same relative path
exists under ~/Projects/the-bounty-hunter AND realpath-confined there? MIRROR-EQUIVALENT : GONE"*.
For a root-only BASE that relative path is the mirror root (which exists), so the prose implies
`MIRROR-EQUIVALENT`; the code refuses the empty suffix at `:243`. The rule lives only in the
code comment at `:240-242` (*"Root-only bounty citations keep their pre-r23 verdict (no mirror
mapping); r23 changes the confinement of fallback credit, not which citations earn it"*).
The behaviour matches pre-r23 and is deliberate; the **policy docstring** just never states it,
so a verifier reading only the policy cannot predict the verdict. One clause at `:34` closes this.

### F4 — LOW (docstring assertions with no implementing line)

- `:46-47` "`[lost-base]`/`[lost-tree]`-marked tokens are not aliases": `grep -n -i lost
  resolve.py` returns exactly one hit — the docstring sentence. No marker test exists in
  `mirror_suffix()` or `classify()`; the behaviour holds only because a prefixed marker breaks the
  string prefix.
- `:75` "sub-kind `rel-unresolved`": one hit, the docstring. No sub-kind is produced anywhere; the
  TSV header is `citation, class, resolved_path, files_citing_count, method, domain, occurrences, scopes`.

Both are pre-existing (identical in `c1-baseline-resolver.py`) and harmless to classification, but
they are unverifiable claims inside the policy a verifier is told to trust.

### F5 — LOW (host-specific literals): "/home/<u>" is one hardcoded user, and two cases read the host

`:27` says *(or /home/<u>/Projects/bounties…)*; `:106` is
`('~/Projects/bounties', '/home/vgpnk/Projects/bounties')`. The same citation shape is a bounty
citation or an ordinary other root depending on the username spelled in it (case `e`, canonical
absent, mirror present):

```
/home/vgpnk/Projects/bounties/ops/rank.mjs:1   MIRROR-EQUIVALENT   …/relocated/tbh/ops/rank.mjs   bounty
/home/alice/Projects/bounties/ops/rank.mjs:1   GONE                                                other
```

This is also why two matrix cases are not hermetic: `absolute-bounty-fallback-control` and
`absolute-prefix-sibling-confusion` cite absolute `/home/vgpnk/...` paths that the checker's
isolated `HOME` cannot redirect. Their notes admit it ("requires … to stay absent on the run
host"). On this host all four probed paths are absent, so they pass as pinned; on a host where the
real bounty tree exists they would silently change class. Verified absent:
`/home/vgpnk/Projects/bounties`, `/home/vgpnk/Projects/bounties/ops/rank.mjs`,
`/home/vgpnk/Projects/bounties-legacy`, `/home/vgpnk/Projects/bounties-legacy/README.md`.

### History (defects fixed or superseded inside this window — recorded for provenance, not scored)

| old defect | evidence at the time | status at pin D |
|---|---|---|
| Policy said "a `../` segment never leaves the root" while the literal branch credited it (set A) | A: `~/Projects/bounties/../outside.md:1` → `RESOLVES`; the 13-case matrix passed that case only because `home/Projects/bounties` was never created | **reconciled**: `:30-33` discloses the carve-out; `bounty-literal-*` controls pin `RESOLVES`; `absolute-*`/`brace-*` escapes pin GONE |
| Policy said INTERNAL is "only … against the lane repo" while `join(lane_root, base)` escaped it (set A) | A: `../outside.md` → `INTERNAL` with a path outside the lane | **reconciled**: `:52-60`, `:72-74` disclose it; matrix control pins it |
| `bounty_suffix()` left a leading `/`, contradicting "boundary matches `mirror_suffix()`'s" (set A) | A: `~/Projects/bounties//ops/rank.mjs` → `GONE` vs alias double slash → `RESOLVES` | **fixed** (`:220`); D → `MIRROR-EQUIVALENT` |
| Root-only bounty resolved to the mirror root in B/C | B/C: `~/Projects/bounties` → `MIRROR-EQUIVALENT` | **deliberately reverted** in D (`:240-243`); the docstring never stated the B/C rule either — see F3 |
| Receipts pinned a 17-case matrix (`5c64e014…`) that was no longer on disk | at 03:43:07, matrix on disk was already 20 cases (`4e39f65c…`); `c1-fixed.json` reported `17/17` | **resolved** at 03:46:26: both receipts pin `4e39f65c…`, `fce5b84b…`, checker `53742c8d…`, `20/20` and `12/20` |

## 5. Attacks that held on the pinned bytes

I could not break the fallback confinement, the alias confinement, the prefix boundary, or the
brace-expansion confinement.

| probe | result |
|---|---|
| `~/Projects/bounties//etc/hostname` (`os.path.join` absolute override) | `GONE` — `under_mirror` rejects `realpath("/etc/hostname")` |
| `~/Projects/bounties/ops/../ok.md` (traversal that stays inside the mirror) | `MIRROR-EQUIVALENT` — realpath, not lexical, confinement |
| `~/Projects/bounties/{../outside.md,missing.md}` (brace escape) | `GONE` on D, `MIRROR-EQUIVALENT` on baseline → discriminating |
| `~/Projects/bounties/evil.mjs` where the **mirror** file symlinks outside | `GONE` (matrix) |
| `nested/leak.md` mirror-side symlink escape | `GONE` (matrix) |
| `~/Projects/the-bounty-hunter/../../outside.md` | `GONE` (matrix) |
| `~/Projects/bounties/{ops,missing}/rank.mjs` (confined brace) | `MIRROR-EQUIVALENT` (matrix) |
| `~/Projects/bounties//ops/rank.mjs` (double slash) | `MIRROR-EQUIVALENT` — normalised in D |
| prefix siblings `bounties-x`, `the-bounty-hunter-x` | ordinary other root, never an alias |
| literal `../` and symlinked literal inside the canonical root | `RESOLVES` — disclosed carve-out, pinned as controls |

The load-bearing line remains `under_mirror()` `:224-229`; it rejects lexical escapes, symlink
escapes, and the absolute-override join.

## 6. Residual risk and verification gaps

- **One non-discriminating escape (F2)** inflates the escape denominator by one unless reclassified.
- **Non-hermetic cases (F5)**: two cases read `/home/vgpnk/...` outside the temp root; results are
  host-dependent by construction, as their notes say.
- **Prose drift (F1)**: the receipt now matches the bytes, but the labels a reader uses to identify
  the revision ("r18 definition", fixed genesis mirror) do not.
- **No LSP**: no caller/definition/diagnostics pass was possible; nothing here is semantic proof.
- **Moving target**: the tree changed four times during the audit (all recorded in §1). If the
  hashes in the header no longer match at integration time, re-run
  `mirror-containment-check.py` (and `--resolver .ufo/waves/round-23/c1-baseline-resolver.py`)
  rather than trusting this report's counts.
- **Out of scope for this seat:** C2 (F06-F08 admission, snapshots, quote assertions), score
  movement, admission, and the mirror-root derivation beyond the ambiguity noted in F1. Repo
  `citation-survival.tsv`/`.md` were not regenerated; all runs wrote into `/tmp` case roots.
- **Judgement limits.** No finding asserts that C1's `after` line is false. F2 is about what one
  fixture actually exercises; F1, F3-F5 are prose, policy-gap, and unanchored-claim defects.

## 7. Scope limits

Read-only review of `corpus/instruments/resolve.py`, the frozen C1 matrix, the checker, and both
receipts; reproduction only under `/tmp/kasegi-r23-falsify-DocstringTruth-2`. No production file,
lane tree, index/state, sibling lane, or fleet repo touched; artifact hashes were re-read after
this report was written. Nothing committed or pushed. No self-credit, no admission, no score
statement.
