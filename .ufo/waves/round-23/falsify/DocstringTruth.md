# DocstringTruth — `resolve.py` policy text vs. landed `classify()` bytes

Seat: `L1Kasegi23.DocstringTruth-2` (reviewer, leaf).
Round 23 FALSIFY wave. Read-only against the repo: the only repo write is this file.
All mutation and CLI replay happened under `/tmp/kasegi-r23-falsify-DocstringTruth-2`.
No git/jj command, commit, or index touch. No installs.

Axis attacked: **depth:verifiability** — does the detector's own documented policy describe
the bytes that classify citations, after the C1 containment change?

## 1. Inputs and hashes

| artifact | sha256 |
|---|---|
| `corpus/instruments/resolve.py` — **A**: bytes `c1-fixed.json` pins and the bytes every probe in §3-§5 was first run against (mtime `03:27:44 -0300`) | `ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9` |
| `corpus/instruments/resolve.py` — **B**: working-tree bytes at report time (mtime `03:40:40 -0300`) | `9e0b5751e820a6868edfff70571e38212763a30446204d7d8522cb0f525d7cde` |
| `corpus/instruments/mirror-containment-fixtures.json` | `5e61a33ed5fa530547aff197fad9380d86d5850374bbb4f2a8f99df44b5e76a9` |
| `corpus/instruments/mirror-containment-check.py` | `1bc2db10dfbc59ef863e68afce475cd1d317da517137922804d7fc09cd46cecb` |
| `.ufo/waves/round-23/c1-fixed.json` | pins `resolver_sha256 = ed9a9dae…`, `matrix_sha256 = 5e61a33e…`, `13/13` |
| `.ufo/waves/round-23/c1-baseline-resolver.py` (pre-fix control) | `d6a3c3f1a1d8e97d42d66a8aa3cb34530b7bc1c18b194e487ef8d580d869f903` |

**Bytes drifted mid-review (unattributed; not reverted, per read-only contract).** At the first
read the tree was `ed9a9dae…`; at report time it is `9e0b5751…`. `diff -u` of the two is exactly
three hunks, all outside the passage under review except one:

```diff
@@ bounty_suffix()
-                return base[len(root) + 1:]
+                return base[len(root) + 1:].lstrip("/")
@@ bounty fallback
-        m, p = exists_any(os.path.join(mirror_root, suffix)) if suffix else (None, None)
+        m, p = exists_any(os.path.join(mirror_root, suffix) if suffix else mirror_root)
@@ report totals
-    maxfiles = max(r["nfiles"] for r in rows)
-    maxocc = max(r["occ"] for r in rows)
+    maxfiles = max((r["nfiles"] for r in rows), default=0)
+    maxocc = max((r["occ"] for r in rows), default=0)
```

The frozen 13-case matrix passes **13/13 on both byte sets**. Findings are therefore labelled by
byte set: F1, F2, F3, F6, F7 reproduce on **A and B**; F4 and F5 reproduce only on **A** and are
already fixed in **B**; F8 (receipt/tree drift) is a property of the pair.

## 2. Method

Each probe is an isolated case root with its own `HOME`, `KASEGI_MIRROR` and lane repo; the
real `resolve.py` is copied into `<case>/tool/resolve.py` and executed as a CLI, and the rows
are read from the CLI's own `citation-survival.tsv`. This is the same replay shape as
`mirror-containment-check.py` (`HOME` / `KASEGI_MIRROR` / `lane`, `SKILL.md` carrying the cite).

```bash
S=/tmp/kasegi-r23-falsify-DocstringTruth-2
env -i HOME=$S/a/home KASEGI_MIRROR=$S/a/relocated/tbh PATH=/usr/bin:/bin \
       LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
       python3 $S/a/tool/resolve.py $S/a/lane
```

Tooling note (role requirement): **no LSP device is mounted** in this session
(`read xd://lsp` → `No such tool: xd://lsp`; mounted list contains no `lsp`). Caller/definition
queries therefore used `grep` + the executed CLI as the documented literal fallback, not as
semantic proof. Python has no project type-checker config in this repo, so no diagnostics pass
was possible either.

## 3. Policy-line ledger (docstring line → implementing range → verdict)

Docstring policy text lives at `resolve.py:23-66`; the implementing code is `classify()` at
`resolve.py:223-255` plus `mirror_suffix()` `:187-198`, `bounty_suffix()` `:201-212`,
`under_mirror()` `:215-220`, `exists_any()` `:170-184`, `brace_expand()` `:155-167`,
`BOUNTY_PREFIXES` `:97`, `MIRROR_CANDIDATES` `:106-107`.

| policy lines | statement | implementing lines | verdict |
|---|---|---|---|
| 26-28 | BOUNTY = EXACT root, root-only or `/`-delimited descendant | `:97`, `:201-212`, `:225-226` | **MATCH** (prefix sibling `~/Projects/bounties-x/f.md` → `domain=other`, `RESOLVES`; see §4 ledger run) |
| 29 | "a `../` segment never leaves the root" | `:226-230` (`exists_any(base)`, no confinement) | **STALE** (F1) |
| 30-32 | mirror fallback = same relative path under mirror **AND realpath-confined** | `:231-233` + `:215-220` | **MATCH** (confined control → MIRROR-EQUIVALENT; fallback `../` and symlink escapes → GONE; §5) |
| 32-33 | "parent-traversal or symlink escape outside the selected mirror is never credited" | `:228-230` credit the primary branch unconfined | **STALE** as a general sentence (F1) |
| 34-36, 44-46 | OTHER: any `~`/`/` root → exists? RESOLVES : GONE | `:244-246` | **MATCH** |
| 36-43 | canonical mirror alias handled first; suffix under the SELECTED root only; never a prefix sibling; root-only/trailing slash allowed; realpath-confined | `:235-243`, `:187-198` | **MATCH** (`~/Projects/origin-work/the-bounty-hunter/...` resolves under the relocated selected root; `the-bounty-hunter-x/f.md` → `other`; bare alias root → `RESOLVES`) |
| 41-42 | "`[lost-base]`/`[lost-tree]`-marked tokens are not aliases" | **no implementing line** | **UNANCHORED** (F6) |
| 47-52 | REL: lane repo first → INTERNAL | `:247-250` | **MATCH** on existence; **STALE** on containment (F2) |
| 53-55 | REL mirror fallback only when realpath-confined; `../` walk-outs and symlink escapes GONE | `:251-254` + `:215-220` | **MATCH** (frozen escapes GONE) |
| 58-59 | literal `os.path.exists(expanduser(path))` | `:171-175` | **MATCH** |
| 60-61 | brace: sorted, ≤64 combos, first existing wins | `:155-167`, `:176-180` | **MATCH** (cap enforced; empty alternatives silently skipped — undocumented, harmless) |
| 62-63 | glob: `<...>`→`*`, sorted first match, zero matches does not resolve | `:181-183` | **MATCH with note** (`recursive=True` and globbing on any `*?[`, not only `<...>`, are undocumented) |
| 64 | every class except GONE resolves by construction | `:230`, `:233`, `:242`, `:246`, `:250`, `:254` | **MATCH** |
| 65 | "INTERNAL is assigned only to lane-repo-relative tokens that resolve against the lane repo" | `:248-250` (`join(lane_root, base)`, unconfined) | **STALE** (F2) |
| 66 | non-resolving relative tokens are GONE, "sub-kind `rel-unresolved`" | none; TSV header has no sub-kind column | **UNANCHORED** (F6) |
| 98-105 (round-19 block) | "all other explicit roots keep the plain exists? RESOLVES : GONE behavior" | `:244-246` true for OTHER-domain non-aliases; BOUNTY is also an explicit root with a fallback `:231-233` | **STALE/ambiguous** (F3) |
| 1-2 (module header) | "r15 … self-input/leading-dot fixes r18" | r23 changed `classify()`; `grep -n 'r23\|containment' resolve.py` → no match | **STALE** (F3) |
| 374 (generated prose) | "r18 definition" | r23 changed the definition | **STALE** (F3) |
| 379-380 (generated prose) | prints the selected/derived mirror root | `:379-380` uses `MIRROR_ROOT` | **MATCH** |
| 497-499, 547 (generated prose) | "Sep-5 genesis mirror `~/Projects/the-bounty-hunter`" | mirror is derived (`:98-117`); contradicts line 379 of the same generated document | **STALE** (F3) |

Ledger evaluated against byte set **B** (`9e0b5751…`). On the receipt-pinned set **A**
(`ed9a9dae…`) two rows read differently, both already corrected in **B**: the fallback clause at
`:30-31` did not cover a root-only suffix (F4) and `bounty_suffix()` did not normalise the
leading slash its docstring claims to match `mirror_suffix()` on (F5).

## 4. Findings

### F1 — HIGH (docstring truth, containment over-claim): the BOUNTY *primary* branch credits
### `../` and symlink escapes; the frozen matrix cannot see it

Policy text added by this very fix (`resolve.py:26-33`) asserts:

> "…a `../` segment never leaves the root)" (line 29)
> "A parent-traversal or symlink escape outside the selected mirror is never credited." (32-33)

`classify()` gates only the fallback conjunct (`:231-233`). The primary conjunct at `:228-230`
returns `RESOLVES` for the raw, un-normalised string. Repro (case `a`; `home/Projects/bounties`
and `home/Projects/outside.md` both exist):

```
~/Projects/bounties/../outside.md:1	RESOLVES	/tmp/…/a/home/Projects/bounties/../outside.md	1	literal	bounty	1	SKILL
```

`realpath` of the credited path is `/tmp/kasegi-r23-falsify-DocstringTruth-2/a/home/Projects/outside.md`
— outside both the bounty root and the mirror. Same for a symlink placed inside the canonical
root (case `b`, `home/Projects/bounties/esc.md → …/vault/secret.mjs`, realpath
`…/vault/secret.mjs`):

```
~/Projects/bounties/esc.md:1	RESOLVES	/tmp/…/b/home/Projects/bounties/esc.md	1	literal	bounty	1	SKILL
```

The frozen escape matrix passes only because **no case ever materialises the canonical bounty
root directory**. `defaults.dirs = ["home/Projects", "lane", "relocated/tbh"]`; the only
`home/Projects/bounties*` entry in the whole matrix is `bounties-legacy/README.md` (a different
subtree):

```bash
python3 -c "
import json; d=json.load(open('corpus/instruments/mirror-containment-fixtures.json'))
print([ (c['id'],k,rel) for c in d['cases'] for k in ('dirs','files','symlinks') for rel in (c.get(k) or {}) if rel.startswith('home/Projects/bounties') ])"
# → [('literal-prefix-sibling-control', 'files', 'home/Projects/bounties-legacy/README.md')]
```

So for every BOUNTY cite in the matrix `bounties/..` cannot resolve (parent component absent) and
the case only ever exercises the fallback. Materialising the root (`dirs += ["home/Projects/bounties"]`)
and the escaped target at its literal canonical location flips the two named escape cases:

```bash
python3 corpus/instruments/mirror-containment-check.py --fixtures $S/fixtures-canonical-root.json
bounty-parent-traversal           escape expect=GONE actual=RESOLVES FAIL
bounty-parent-traversal-vault     escape expect=GONE actual=RESOLVES FAIL
cases=13 escape=6 controls=7 pass=11 fail=2
```

Adding `home/Projects/bounties/evil.mjs → @ROOT@/secret/outside.mjs` to
`bounty-fallback-symlink-escape` flips that one too (`actual=RESOLVES`, `fail=1` in that run).
Only the fixture copies in `/tmp` were changed; the frozen matrix and the resolver bytes are untouched.

**Does this falsify C1's `after` claim?** No, not as worded: the claim is narrowly about
"bounty-prefixed and relative **mirror fallback paths**", and those fallback gates held under
every attack I could construct (§5). What it falsifies is (a) the module policy text at
`:29`/`:32-33`, which is broader, and (b) the fixture names `bounty-parent-traversal` /
`bounty-parent-traversal-vault`, which read as "bounty traversal is pinned GONE" while they only
pin "traversal is GONE when the canonical root is absent" — exactly the state in which the
primary branch is structurally unreachable.

### F2 — MEDIUM (docstring vs. its own frozen control): "INTERNAL … resolve against the lane repo" is false

`resolve.py:52` and `:65` say the lane-first candidate is lane-repo-relative and INTERNAL is
assigned only to tokens resolving "against the lane repo". `:248-250` is an unconfined
`exists_any(os.path.join(lane_root, base))`. Repro (case `b`; `outside.md` exists one level
above the lane, `lane/leak.md → …/vault/secret.mjs`):

```
../outside.md	INTERNAL	/tmp/…/b/lane/../outside.md	1	literal	rel	1	SKILL
leak.md:1	INTERNAL	/tmp/…/b/lane/leak.md	1	literal	rel	1	SKILL
```

realpaths: `…/b/outside.md` and `…/vault/secret.mjs` — both outside the lane repo. The frozen
matrix *pins* this behaviour (`lane-relative-parent-internal-control`, `expect=INTERNAL`,
`files={'outside.md'}`), so the module docstring contradicts its own control. C1's claim
discloses the behaviour ("relative ../outside.md is INTERNAL (not targeted)"); what it did not
do is reconcile the policy sentence — the docstring still claims containment that the code does
not provide. This is the same asymmetry F1 exploits, on the INTERNAL side.

### F3 — MEDIUM-LOW (stale pre-fix prose in header, round-19 block, generated report)

- Emitted `citation-survival.md` self-contradicts: line 7 of the generated doc prints the
  derived mirror root (`/tmp/…/relocated/tbh` in my run), line 89 (from `resolve.py:497-499`,
  also `:547`) still says "Sep-5 genesis mirror `~/Projects/the-bounty-hunter`". Post-C1 the
  class means "realpath-confined under the SELECTED mirror", so the scope-limits prose is both
  stale and internally inconsistent when `KASEGI_MIRROR` relocates the root.
- `resolve.py:1-2` still labels the instrument "r15 … r18"; `:374` emits "r18 definition".
  `grep -n 'r23\|containment' resolve.py` → **no match**, although `classify()` changed in r23.
  A reader cannot tell from the bytes that the containment rule exists.
- `:98-105` says "all other explicit roots keep the plain exists? RESOLVES : GONE behavior".
  After the fix the BOUNTY domain (also an explicit root) has a realpath-confined fallback, so
  the sentence is only true for OTHER-domain non-aliases. It needs the same scoping its sibling
  sentences just received.

### F4 — LOW (bytes **A** only; already fixed in **B**): BOUNTY root-only cite → GONE while the alias branch resolved it

On set **A**, `resolve.py:231` used `exists_any(...) if suffix else (None, None)`, so an empty
suffix could never reach the mirror; the sibling alias branch (`:240`) already handled it. Set
**B** changed the guard to `... if suffix else mirror_root`. Evidence on **A**, canonical root
absent, mirror present (case `c`):

```
~/Projects/bounties	GONE		1		bounty	1	SKILL
~/Projects/bounties/	GONE		1		bounty	1	SKILL
~/Projects/the-bounty-hunter	RESOLVES	/tmp/…/c/relocated/tbh	1	literal	other	1	SKILL
```

Same scenario on **B** (case `h`, canonical root absent, mirror present):

```
~/Projects/bounties	MIRROR-EQUIVALENT	/tmp/…/h/relocated/tbh	1	literal	bounty	1	SKILL
~/Projects/bounties/	MIRROR-EQUIVALENT	/tmp/…/h/relocated/tbh	1	literal	bounty	1	SKILL
```

So the docstring's fallback clause ("same relative path exists under …") now holds for root-only
as well. Retained here because `c1-fixed.json` still pins set **A**, and because neither byte set
states the root-only rule in prose — the code is now right, the sentence is still silent.

### F5 — LOW (bytes **A** only; already fixed in **B**): "the boundary matches `mirror_suffix()`'s"

Set **A**'s `bounty_suffix()` kept a leading `/` in the suffix (`return base[len(root) + 1:]`)
while `mirror_suffix()` strips it. Observable on a double slash (case `d`, mirror holds
`ops/rank.mjs`):

```
~/Projects/bounties//ops/rank.mjs:1	GONE		1		bounty	1	SKILL
~/Projects/the-bounty-hunter//ops/rank.mjs:1	RESOLVES	/tmp/…/d/relocated/tbh/ops/rank.mjs	1	literal	other	1	SKILL
```

The double-slash BOUNTY suffix became absolute under `os.path.join` (`/ops/rank.mjs`) and
`under_mirror` rejected it — safe, but the two boundaries were not the same, contrary to `:204`.
Set **B** adds `.lstrip("/")`; the same citation now resolves (case `g`):

```
~/Projects/bounties//ops/rank.mjs:1	MIRROR-EQUIVALENT	/tmp/…/g/relocated/tbh/ops/rank.mjs	1	literal	bounty	1	SKILL
```

### F6 — LOW (unanchored docstring claims)

- `:41-42` "`[lost-base]`/`[lost-tree]`-marked tokens are not aliases": `grep -n -i lost resolve.py`
  returns exactly one hit, the docstring itself; the baseline control has the identical sentence.
  No marker check exists in `classify()`/`mirror_suffix()`. Behaviour happens to hold only
  because a prefixed marker breaks the string prefix.
- `:66` "sub-kind `rel-unresolved`": one hit, the docstring; no sub-kind is produced and the
  TSV header is `citation, class, resolved_path, files_citing_count, method, domain, occurrences, scopes`.

### F7 — LOW (docstring `<u>` not implemented): `BOUNTY_PREFIXES` hardcodes one user

`:27` says "(or /home/<u>/Projects/bounties…)" but `:97` is
`('~/Projects/bounties', '/home/vgpnk/Projects/bounties')` — no other user. Case `e` (canonical
absent, mirror holds `ops/rank.mjs`):

```
/home/vgpnk/Projects/bounties/ops/rank.mjs:1	MIRROR-EQUIVALENT	/tmp/…/e/relocated/tbh/ops/rank.mjs	1	literal	bounty	1	SKILL
/home/alice/Projects/bounties/ops/rank.mjs:1	GONE		1		other	1	SKILL
```

`/home/vgpnk/Projects/bounties` does not exist on this host, so the literal branch could not
mask the result. The same citation shape gets the mirror fallback or not depending on the
username spelled in it.

### F8 — MEDIUM (verifiability, provenance): the C1 "fixed" receipt does not identify the landed bytes

`c1-fixed.json` records `resolver_sha256 = ed9a9dae…`; the working tree is `9e0b5751…` (mtime
`03:40:40 -0300`). Both byte sets pass the frozen matrix 13/13, so no behavioural claim flips,
but the receipt a verifier will read names code that is no longer in the tree.

```bash
sha256sum corpus/instruments/resolve.py
# 9e0b5751e820a6868edfff70571e38212763a30446204d7d8522cb0f525d7cde
python3 -c "import json;print(json.load(open('.ufo/waves/round-23/c1-fixed.json'))['resolver_sha256'])"
# ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9
```

Remedy is either regenerate the receipt from current bytes
(`mirror-containment-check.py --json .ufo/waves/round-23/c1-fixed.json`, which yields 13/13 on
`9e0b5751…`) or attribute the tree change and re-pin. This read-only seat did neither and did not
revert the drift.

## 5. Attacks that held (honest negatives — I could not break the fallback confinement)

| probe | result |
|---|---|
| `~/Projects/bounties//etc/hostname` (absolute-override join `mirror + "/etc/hostname"`) | `GONE` — `under_mirror` rejects `realpath("/etc/hostname")` |
| `~/Projects/bounties/ops/../ok.md` (traversal that stays inside the mirror) | `MIRROR-EQUIVALENT` — realpath, not lexical, confinement |
| `~/Projects/bounties/evil.mjs` where **mirror** file is a symlink to `@ROOT@/secret/outside.mjs` | `GONE` (frozen escape case) |
| `nested/leak.md` with mirror-side symlink escape | `GONE` (frozen escape case) |
| `../outside-vault/secret.mjs` relative fallback escape | `GONE` (frozen escape case) |
| `~/Projects/the-bounty-hunter/../../outside.md` alias escape | `GONE` (frozen control) |
| confined bounty/relative controls | `MIRROR-EQUIVALENT` / `RESOLVES` as pinned |
| prefix siblings `bounties-x`, `the-bounty-hunter-x` | ordinary other root, never an alias (`RESOLVES` as `other` when present) |

The load-bearing line is `under_mirror()` `:215-220`; it correctly rejects both lexical escapes
and symlink escapes, including the `os.path.join` absolute-override case. C1's narrow fallback
confinement is real.

## 6. Residual risk and verification gaps

- **Fixture coverage (highest residual risk).** Zero of the 13 frozen cases has a functioning
  canonical bounty root, so no case pins the primary BOUNTY branch in either direction — not a
  literal resolve, not a literal escape. A future change to `:228-230` is invisible to the matrix.
- **No LSP.** Caller/definition/diagnostics checks were not possible (`xd://lsp` absent); the
  ledger above rests on line-addressed reads, `grep`, and executed CLI rows. Nothing here is
  presented as semantic proof.
- **Byte drift during review.** `resolve.py` changed from `ed9a9dae…` to `9e0b5751…` at
  `03:40:40` while this review ran. I did not write it and did not revert it; F8 records the
  consequence for receipt provenance. Every finding above is labelled with the byte set it
  reproduces on, and §1 records the exact three-hunk diff.
- **Fixture augmentation is scratch-only.** The two augmented matrices live in
  `/tmp/kasegi-r23-falsify-DocstringTruth-2/{fixtures-augmented,fixtures-canonical-root}.json`.
  I modified no repo artifact: `resolve.py` was re-read (and re-hashed) after the external change,
  and `mirror-containment-fixtures.json` / `mirror-containment-check.py` still carry the §1 hashes.
- **Not re-verified / out of scope for this seat:** C2 (F06-F08 admission, source snapshots,
  quote assertions), score movement, admission, the round-19 mirror-root derivation itself, and
  whether `MIRROR_ABSENT` messaging elsewhere matches. `citation-survival.tsv`/`.md` in the repo
  were not regenerated; all runs wrote into `/tmp` case roots.
- **Judgement limits.** F1-F3, F6-F8 are documentation/contract defects on both byte sets; F4 and
  F5 are already fixed in the current tree. None of them asserts that C1's `after` line is false.
  The claim-adjacent consequence is narrower: the 6/6 escape receipt does not demonstrate what
  its case names assert, and it no longer hashes to the landed file.

## 7. Scope limits

Read-only review of `corpus/instruments/resolve.py:1-582` and the frozen C1 fixtures/checker;
reproduction only in `/tmp` scratch. No production file, lane tree, index/state, sibling lane,
or fleet repo touched. Nothing committed or pushed. No self-credit, no admission, no score
statement.
