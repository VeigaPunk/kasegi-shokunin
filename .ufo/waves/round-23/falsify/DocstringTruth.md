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
| `corpus/instruments/mirror-containment-fixtures.json` | `332a5fe95b94207cdf25caf29d52b394f81701b4fe441b92e47ab3ac100005e3` (23 cases) | `03:48:20 -0300` |
| `corpus/instruments/mirror-containment-check.py` | `53742c8d9529dffb8c40c39b3448de7388b774b548d7831670598d5534bff5d1` | `03:43:01 -0300` |
| `.ufo/waves/round-23/c1-fixed.json` | `c8041b9d…`, `generated_at 2026-10-25T06:48:29Z`, pins resolver `fce5b84b…`, matrix `332a5fe9…`, checker `53742c8d…`, `23/23` | `03:48:29` |
| `.ufo/waves/round-23/c1-baseline.json` | `6c36cf3e…`, `generated_at 2026-10-25T06:48:30Z`, pins baseline `d6a3c3f1…`, same matrix/checker, `12/23` | `03:48:30` |
| `.ufo/waves/round-23/c1-baseline-resolver.py` | `d6a3c3f1a1d8e97d42d66a8aa3cb34530b7bc1c18b194e487ef8d580d869f903` | `03:28` |

## 1. What moved during this review (pin discipline, not a finding)

The tree was edited four times while the audit ran. Recorded so every number below can be tied to
bytes; I wrote none of it and reverted none of it.

| set | resolver sha | fixtures | checker |
|---|---|---|---|
| **A** 03:27:44 | `ed9a9dae…` | 13 cases `5e61a33e…` | `1bc2db10…` |
| **B** 03:40:40 | `9e0b5751…` | 13 cases | `1bc2db10…` |
| **C** 03:42:37 | `8dd45bc8…` | 20 cases `4e39f65c…` (03:43:38) | `53742c8d…` (03:43:01) |
| **D** 03:46:26 | `fce5b84b…` (pinned) | 20 cases | `53742c8d…` |
| **E** 03:48:20 | `fce5b84b…` (pinned) | **23 cases `332a5fe9…`** (pinned) | `53742c8d…` |

A→E is: the BOUNTY/REL policy paragraphs rewritten to disclose the literal and INTERNAL
carve-outs (`:26-38`, `:52-64`, `:72-75`); `bounty_suffix().lstrip("/")` (`:220`); the root-only
mirror-mapping guard toggled twice — enabled in B/C (`… if suffix else mirror_root`), then
deliberately reverted in D to `(None, None)` with the comment at `:240-242`; and
`max(..., default=0)` for empty row sets (`:359-360`). The matrix grew 13→17→20→23 cases
(E added `relative-priority-lane-first-control`, `mirror-root-prefix-sibling-escape`,
`absolute-parent-traversal`, and rewrote `glob-expansion-escape` to include a real `../` hop).
The receipts were last regenerated at 03:48:29–30 against the 23-case matrix, so receipt and tree
now agree; §4 history records the stale-receipt window.

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
| 33 | "the matrix pins this class as a control" | those two cases | **MATCH** (pinned set E) |
| 34-38 | fallback: same relative path under mirror **and realpath-confined**, else GONE | `:243-246`, `:224-229` | **MATCH** — all 11 escape cases flip credit→`GONE` on the baseline; brace- and glob-expanded escapes included |
| 34-38 (root-only) | for a root-only BASE, "same relative path exists under the mirror" would credit the mirror root | `:243` (`if suffix else (None, None)`) + comment `:240-242` | **STALE-BY-OMISSION** (F3) — root-only cites are GONE; only the code comment says so |
| 39-46, 48-51 | OTHER: `~`/`/` root → exists? `RESOLVES` : `GONE`; canonical alias first, selected root only, root-only/trailing slash, realpath-confined | `:247-258`, `:196-207` | **MATCH** — alias resolves under the relocated root; `the-bounty-hunter-x/f.md` → `other`; alias escape → `GONE` |
| 46-47 | "`[lost-base]`/`[lost-tree]`-marked tokens are not aliases" | **none** | **UNANCHORED** (F4) |
| 52-60 | REL: lane repo first; `INTERNAL` not confined (`../` or repo symlink outside the lane still `INTERNAL`, "by prior design; r23 did not change this branch and the matrix pins it") | `:259-262`; `lane-relative-parent-internal-control` | **MATCH** — `../outside.md` → `INTERNAL`, path `…/lane/../outside.md`; `lane/leak.md → vault` → `INTERNAL` |
| 61-63 | mirror fallback only when realpath-confined; walk-outs and symlink escapes GONE | `:263-266`, `:224-229` | **MATCH** (matrix) |
| 66-67 | literal `os.path.exists(expanduser(path))` | `:180-184` | **MATCH** |
| 68-69 | brace: sorted, ≤64 combos, first existing wins | `:164-177`, `:185-189` | **MATCH** (cap enforced; empty alternatives silently skipped — undocumented, harmless) |
| 70-71 | glob: `<...>`→`*`, sorted first match, zero matches does not resolve | `:190-193` | **MATCH with note** (`recursive=True`; globbing also triggers on any `*?[`, not only `<...>`). The escape case now carries a real `../` hop and discriminates (baseline `MIRROR-EQUIVALENT` → `GONE`) |
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

### F2 — resolved during this audit (retained for the record): `glob-expansion-escape` did not test confinement

At matrix `4e39f65c…` the case cited `~/Projects/bounties/<name>.md` against a fixture whose only
markdown sat outside the mirror. `*` cannot cross `/`, so the verdict was `GONE` for the documented
zero-match reason and was identical on the baseline. Adding one `.md` inside the mirror flipped it
to `MIRROR-EQUIVALENT`, proving the pin was "no match existed", not "an outside match was refused".

At pinned matrix `332a5fe9…` the case is `~/Projects/bounties/<name>/../../outside-vault/x.md`, with
`relocated/tbh/sub` present, so the placeholder resolves to a directory *inside* the mirror and the
`..` hop then leaves it. It now discriminates:

```
fixed     ~/Projects/bounties/<name>/../../outside-vault/x.md:1   GONE
baseline  ~/Projects/bounties/<name>/../../outside-vault/x.md:1   MIRROR-EQUIVALENT
```

Escape arithmetic at the pin: **11 escapes, 11 discriminating** (baseline: 12 pass / 11 fail).

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

### F5 — LOW (host-specific literals): "/home/<u>" is one hardcoded user, and three cases read the host

`:27` says *(or /home/<u>/Projects/bounties…)*; `:106` is
`('~/Projects/bounties', '/home/vgpnk/Projects/bounties')`. The same citation shape is a bounty
citation or an ordinary other root depending on the username spelled in it (case `e`, canonical
absent, mirror present):

```
/home/vgpnk/Projects/bounties/ops/rank.mjs:1   MIRROR-EQUIVALENT   …/relocated/tbh/ops/rank.mjs   bounty
/home/alice/Projects/bounties/ops/rank.mjs:1   GONE                                                other
```

This is also why three matrix cases are not hermetic: `absolute-bounty-fallback-control`,
`absolute-prefix-sibling-confusion`, and `absolute-parent-traversal` cite absolute
`/home/vgpnk/...` paths that the checker's isolated `HOME` cannot redirect. Their notes admit it
("requires … to stay absent on the run host"). On this host every probed precondition is absent, so
they pass as pinned; on a host where the real bounty tree or `Projects/outside-vault` exists they
would silently change class. Verified absent: `/home/vgpnk/Projects/bounties`,
`/home/vgpnk/Projects/bounties/ops/rank.mjs`, `/home/vgpnk/Projects/bounties-legacy`,
`/home/vgpnk/Projects/bounties-legacy/README.md`, `/home/vgpnk/Projects/outside-vault`,
`/home/vgpnk/Projects/outside-vault/secret.mjs`, `/home/vgpnk/Projects/tbh-evil`.

### History (defects fixed or superseded inside this window — recorded for provenance, not scored)

| old defect | evidence at the time | status at the pin (D resolver / E matrix) |
|---|---|---|
| Policy said "a `../` segment never leaves the root" while the literal branch credited it (set A) | A: `~/Projects/bounties/../outside.md:1` → `RESOLVES`; the 13-case matrix passed that case only because `home/Projects/bounties` was never created | **reconciled**: `:30-33` discloses the carve-out; `bounty-literal-*` controls pin `RESOLVES`; `absolute-*`/`brace-*` escapes pin GONE |
| Policy said INTERNAL is "only … against the lane repo" while `join(lane_root, base)` escaped it (set A) | A: `../outside.md` → `INTERNAL` with a path outside the lane | **reconciled**: `:52-60`, `:72-74` disclose it; matrix control pins it |
| `bounty_suffix()` left a leading `/`, contradicting "boundary matches `mirror_suffix()`'s" (set A) | A: `~/Projects/bounties//ops/rank.mjs` → `GONE` vs alias double slash → `RESOLVES` | **fixed** (`:220`); D → `MIRROR-EQUIVALENT` |
| Root-only bounty resolved to the mirror root in B/C | B/C: `~/Projects/bounties` → `MIRROR-EQUIVALENT` | **deliberately reverted** in D (`:240-243`); the docstring never stated the B/C rule either — see F3 |
| Receipts pinned a 17-case matrix (`5c64e014…`) that was no longer on disk | at 03:43:07, matrix on disk was already 20 cases (`4e39f65c…`); `c1-fixed.json` reported `17/17` | **resolved**: receipts regenerated at 03:48:29–30 pin the 23-case matrix `332a5fe9…`, resolver `fce5b84b…`, checker `53742c8d…`, `23/23` and `12/23` |
| `glob-expansion-escape` classified GONE on both baseline and fixed (zero matches; no `../` in the cite) | at matrices `4e39f65c…`; see F2 above | **fixed** in matrix E: cite is now `<name>/../../outside-vault/x.md` with `relocated/tbh/sub`, and it discriminates |

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
| `../tbh-evil/decoy.md` (joined string lexically starts with the mirror path) | `GONE` — realpath boundary, not string prefix; the baseline credits it |
| `docs/shared.md` present in both lane and mirror | `INTERNAL` — lane-first priority (pinned by the new control) |
| `~/Projects/bounties/<name>/../../outside-vault/x.md` (glob hop out) | `GONE` at the pin, `MIRROR-EQUIVALENT` on the baseline |
| prefix siblings `bounties-x`, `the-bounty-hunter-x` | ordinary other root, never an alias |
| literal `../` and symlinked literal inside the canonical root | `RESOLVES` — disclosed carve-out, pinned as controls |

The load-bearing line remains `under_mirror()` `:224-229`; it rejects lexical escapes, symlink
escapes, and the absolute-override join.

## 6. Residual risk and verification gaps

- **Escape arithmetic at the pin**: 11 escape cases, all 11 discriminating (fixed `23/23`,
  baseline `12/23`). F2's non-discriminating case was fixed in matrix E.
- **Non-hermetic cases (F5)**: three cases read `/home/vgpnk/...` outside the temp root; results
  are host-dependent by construction, as their notes say. All preconditions verified absent here.
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
