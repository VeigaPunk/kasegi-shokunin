# LiteralCarveout — C1 literal `exists_any(base)` carve-out vs the frozen predicate

Seat: critic (round-23 FALSIFY wave). Scope: C1 only (`depth:verifiability`), landed
working-tree bytes at commit-in-progress `922a4dde90b60b465e2b8b241d1fe363f1f27e98` base.
Read-only: no production byte edited; all mutation done on copies under
`/tmp/kasegi-r23-falsify-LiteralCarveout/`. No tool installed or updated.
Nothing here claims admission, a verdict change, or score movement.

Artifacts under test (SHA-256 as printed by the replayer below):

- `corpus/instruments/resolve.py` — `ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9`
- `corpus/instruments/mirror-containment-fixtures.json` — `5e61a33ed5fa530547aff197fad9380d86d5850374bbb4f2a8f99df44b5e76a9`

## Question

The frozen C1 claim declares `~/Projects/bounties/../outside.md` an escape and the code
consults literal existence **before** mirror confinement. Decide whether that literal
branch and the `literal-prefix-sibling-control` pin (`expect: RESOLVES`) sit inside or
outside the frozen predicate, then give the least change that removes the ambiguity
without rewriting frozen bytes.

## Verdict (answer first)

**Outside the frozen predicate as the matrix operationalises it, and inside the frozen
claim as it is written.** The two readings are not equivalent, and the landed artifacts
support both; that is the defect, and it is documentary, not behavioural.

1. The claim's subject is scoped to the fallback path, not to existence:

   > `claims.json:4` — `"claim": "Make MIRROR-EQUIVALENT sound: bounty-prefixed and relative mirror fallback paths cannot credit parent traversal or symlink escapes outside the selected mirror. Preserve valid confined mirror and missing-file controls; reject sibling-root prefix confusion."`

   The matrix note states the same partition explicitly:

   > `corpus/instruments/mirror-containment-fixtures.json:93` — `"note": "A literal hit is truthful RESOLVES as an ordinary other root before and after; the claim confines the mirror fallback, not literal existence."`

   Read that way, `literal-prefix-sibling-control` is correctly out of scope: it never
   enters a mirror branch at all (`bounty_suffix()` → `None` because `bounties-legacy` is
   not `/`-delimited-below `bounties`; `mirror_suffix()` → `None`; `base.startswith("~")`
   → the OTHER literal step at `resolve.py:245-246`). It is the converse pin for "a prefix
   sibling is an ordinary other root" (`resolve.py:28-29`), not a prefix-confusion case.

2. The claim's own operative sentences are class-agnostic and are **falsified** by the
   landed code:

   - `"claim"`: *"cannot credit parent traversal or symlink escapes outside the selected mirror"*.
   - `"after"`: *"All declared mirror-escape and prefix-confusion fixtures classify GONE"*.

   `RESOLVES` is credit: it enters the headline numerator
   (`resolve.py:416` — `"Numerator = RESOLVES + MIRROR-EQUIVALENT + INTERNAL."`). So a
   bounty-prefixed `../` walk-out that lands outside the mirror and is classified
   `RESOLVES` **is** credited, and the second sentence is only true for the frozen fixture
   tree, not for the predicate — because **0 of 13 frozen cases ever materialise a path
   under `home/Projects/bounties`** (see E2). The literal step is never positively
   exercised; three escape pins are GONE for want of a parent directory, not for want of
   containment.

3. `resolve.py`'s own docstring asserts the strong reading and contradicts the function
   directly below it:

   > `resolve.py:27-29` — `"domain BOUNTY BASE under the EXACT root ... a prefix sibling 'bounties-x/...' is an ordinary other root, and a '../' segment never leaves the root)"`
   > `resolve.py:32-33` — `"A parent-traversal or symlink escape outside the selected mirror is never credited."`

   Both are false as written (E3, E4). The `under_mirror()` docstring at `resolve.py:217`
   is the only correct one — *"never credited as mirror evidence"* — because it names the
   class.

## Counterexamples (executed, not argued)

### E1 — same citation, both expectations, decided by file state only

```
$ python3 -c '...'   # collect cites from the frozen matrix
cases: 13 escape: 6 controls: 7
DUP CITE: ~/Projects/bounties-legacy/README.md:1
  [('bounty-prefix-sibling-confusion', 'escape', 'GONE'),
   ('literal-prefix-sibling-control', 'control', 'RESOLVES')]
ids containing prefix-sibling: ['bounty-prefix-sibling-confusion', 'literal-prefix-sibling-control']
expect!=GONE escapes: []
```

Consequence: `"after"` — *"All declared mirror-escape and prefix-confusion fixtures
classify GONE"* — is only well-formed if "declared … fixture" means `nature == "escape"`.
Keyed on the citation string, or on the `prefix-sibling` id fragment, the claim asserts
both GONE and RESOLVES for one string. The matrix resolves this via `nature`; the frozen
claim text never says so. This is a *nominal* collision, not a live harness bug — the
replayer materialises one isolated tree per case (`mirror-containment-check.py:77-143`),
so the two expectations never share a TSV.

### E2 — the escape pins depend on a directory the fixture never creates

```
$ python3 - <<'PY'  # per case: any dir/file path containing Projects/bounties
default dirs: ['home/Projects', 'lane', 'relocated/tbh']
bounty-parent-traversal              bounty-path-literals=[]
...
missing-bounty-target-control        bounty-path-literals=[]
literal-prefix-sibling-control       bounty-path-literals=['home/Projects/bounties-legacy/README.md']
canonical-alias-confined-control     bounty-path-literals=[]
canonical-alias-escape-control       bounty-path-literals=[]
```

`home/Projects/bounties` is created by no case. My first mutation (adding only
`home/Projects/outside.md` to `bounty-parent-traversal`) therefore stayed GONE:
`<root>/home/Projects/bounties/../outside.md` cannot be traversed when `bounties` does not
exist. Add the bounty root and the pin flips.

### E3 — the literal branch credits a parent-traversal escape outside the mirror (RESOLVES)

Mutated matrix (copy only, `/tmp/kasegi-r23-falsify-LiteralCarveout/mutated2.json`), cases
`X1`/`X2` add `"dirs": ["home/Projects/bounties"]`; `X1` adds
`"files": {"home/Projects/outside.md": ...}`, `X2` adds a HOME-side symlink
`home/Projects/bounties/evil.mjs -> @ROOT@/secret/outside.mjs`:

```
$ python3 corpus/instruments/mirror-containment-check.py --fixtures /tmp/kasegi-r23-falsify-LiteralCarveout/mutated2.json
X1-traversal-literal-home                  escape  expect=GONE             actual=RESOLVES         FAIL
X2-symlink-literal-home                    escape  expect=GONE             actual=RESOLVES         FAIL
X3-prefix-sibling-with-bounty-dir          escape  expect=GONE             actual=GONE             PASS
cases=3 escape=3 controls=0 pass=1 fail=2
resolver_sha256=ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9
matrix_sha256=6806737d820fa853be537091135aeb3168bba3dc2f30b9ca74a5a28d8d93f031
```

Raw CLI TSV from an independent hand-built tree (`m1/`, HOME=`m1/home`, KASEGI_MIRROR=`m1/relocated/tbh`):

```
citation	class	resolved_path	files_citing_count	method	domain	occurrences	scopes
~/Projects/bounties/../outside.md:1	RESOLVES	.../m1/home/Projects/bounties/../outside.md	1	literal	bounty	1	SKILL
~/Projects/bounties/evil.mjs:1	RESOLVES	.../m1/home/Projects/bounties/evil.mjs	1	literal	bounty	1	SKILL
```

Both rows are `domain=bounty`, `method=literal`, and both resolved paths are outside the
selected mirror. `bounty-parent-traversal` (frozen expect GONE) and
`bounty-fallback-symlink-escape` (frozen expect GONE) become `RESOLVES` under a HOME that
has its own `Projects/bounties` — the ordinary case on an author machine.

### E4 — one claim sentence, two roots, two classes

Same traversal shape written under the canonical mirror alias vs under the bounty root,
both with the literal walk-out present under HOME, both with the mirror-side decoy absent
(`Y1`/`Y3`) or a decoy present (`Y3`):

```
$ python3 corpus/instruments/mirror-containment-check.py --fixtures .../asym.json
Y1-canonical-alias-traversal-literal-home  control expect=GONE  actual=GONE       PASS
Y2-bounty-traversal-literal-home           control expect=GONE  actual=RESOLVES   FAIL
$ python3 corpus/instruments/mirror-containment-check.py --fixtures .../asym2.json
Y3-canonical-alias-traversal-decoy-and-literal control expect=GONE actual=GONE PASS
```

Cause: `resolve.py:236-243` handles the canonical alias (`mirror_suffix`) **before** the
OTHER literal step, so the alias root never consults literal existence and its traversal
is GONE; `resolve.py:226-231` handles the bounty root **after** a literal hit, so the same
shape is RESOLVES. Two roots, one sentence ("bounty-prefixed and relative mirror fallback
paths … outside the selected mirror"), opposite classes — the sentence cannot be read as a
single invariant without naming the class.

### E5 — the `literal-prefix-sibling-control` pin is inert w.r.t. the C1 fix

```
$ python3 -c '... .ufo/waves/round-23/c1-baseline.json per-case ...'
bounty-prefix-sibling-confusion  escape  expect=GONE  actual=MIRROR-EQUIVALENT FAIL
literal-prefix-sibling-control   control expect=RESOLVES actual=RESOLVES      PASS
```

The control already passes on the do-nothing baseline, so it is a non-regression pin for
the literal path rule, not a discriminator for the exact-root boundary; the escape twin is
the only load-bearing half. That is legitimate, but it means the pair cannot carry the
claim's `"All declared … fixtures classify GONE"` sentence on its own.

### E6 — the receipt cannot show which branch won

`mirror-containment-check.py:126-136` keeps only `citation -> class`; `record` never
carries `resolved_path` or `domain`. `c1-fixed.json` and `c1-baseline.json` therefore list
13 class strings and nothing that distinguishes a literal `RESOLVES` (outside the mirror)
from an alias `RESOLVES` (inside it). The frozen claim's ambiguity is invisible in the very
artifacts offered as its evidence.

## Impacted axes

- `depth:verifiability` (C1): the predicate's observable is under-specified, and the
  receipts discard the field that would settle it. Detector soundness for
  `MIRROR-EQUIVALENT` is **not** refuted here (all six frozen escape rows are
  `MIRROR-EQUIVALENT` on the baseline bytes and `GONE` on the fixed bytes; the guard is
  load-bearing in my X-tree too, since X1/X2 never return `MIRROR-EQUIVALENT`).
- `coverage` (C2): untouched.

## Smallest safe correction (no frozen byte rewritten)

Behaviour stays as it is. `claims.json` and the 13-case matrix are frozen, and the matrix
SHA-256 is embedded in both receipts, so editing either invalidates `c1-fixed.json` /
`c1-baseline.json`. The ambiguity must therefore be closed on the unfrozen surfaces where
it is actually produced.

**P1 — make `resolve.py`'s BRANCH docstring say the class it enforces (≈3 lines, no code change).**

- `resolve.py:29`: replace `"and a \`../\` segment never leaves the root)"` with
  `"and a \`../\` segment is never credited as mirror evidence — the literal existence test still applies to the written path)"`.
- `resolve.py:32-33`: replace `"A parent-traversal or symlink escape outside the selected mirror is never credited."`
  with `"A parent-traversal or symlink escape is never credited as MIRROR-EQUIVALENT; when the written path literally exists under HOME the row is RESOLVES (method \`literal\`), and the canonical-alias branch above yields GONE because it never consults literal existence."`

This is the whole contradiction: the docstring states the strong reading, the function
implements the class-scoped one, and the matrix note (`:93`) already states the
class-scoped one. P1 makes the three agree without touching `classify()`.

**P2 — let the receipt name the branch (±6 lines in `mirror-containment-check.py::run_case`).**

Read `resolved_path` and `domain` alongside `class` (columns 3 and 6 of the documented TSV
header at `resolve.py:75-77`) into each `record`; re-run both receipts. Then
`literal-prefix-sibling-control` self-documents as `RESOLVES` outside the mirror and every
escape row as `GONE` with no path, and no reader has to decide which reading of
`"cannot credit"` the freeze intended.

**P3 (optional, new file, frozen matrix untouched) — pin the carve-out instead of leaving it implicit.**

`corpus/instruments/mirror-containment-literal-carveout.json` with the three cases proven
in E3/E4: bounty `../` walk-out with the HOME bounty root materialised → `RESOLVES` (X1);
bounty HOME-side symlink → `RESOLVES` (X2); canonical-alias `../` with the same literal
target → `GONE` (Y3). A carve-out with a witness fails loudly if anyone later "fixes" the
literal branch, which is exactly the drift P1 exists to prevent.

**Rejected as not-least (state for the integration owner):** changing `classify()` so the
bounty literal step rejects `..` walk-outs or symlink escapes outside the bounty root.
That satisfies the strong reading but makes `RESOLVES` lie about `os.path.exists()` of the
written path, changes the documented literal policy for legitimate `..`-written cites,
requires a new frozen matrix and a fresh baseline, and is strictly larger than P1+P2 for
the same disambiguation. If the strong reading is the intended one, it must be a round-24
claim change, not a round-23 defect fix.

## Falsifiable finding (one line)

The landed C1 bytes do not satisfy the frozen claim's class-agnostic sentences — a
bounty-prefixed parent traversal or HOME-side symlink escape outside the selected mirror
is classified `RESOLVES`, which is counted in the numerator — while the frozen matrix
cannot detect this because no case creates `home/Projects/bounties`; the `RESOLVES` pin for
`literal-prefix-sibling-control` is outside the *prefix-confusion* family and outside the
mirror-fallback predicate, so the claim's "All declared … fixtures classify GONE" and the
matrix are only consistent under a `nature`-keyed reading the frozen text never states.

## Scope limits

- Did not test C2/F06-F08, `corpus/README.md`, `SOURCES.md`, `QUALITY.md`.
- Did not mutate `under_mirror`, `mirror_suffix`, or the relative branch; those are the
  `MutateBountyConfine` / `MutateRelConfine` / `ControlsRerun` seats.
- Did not modify, stage, or commit any production, lane, sibling, fleet, or git/jj state;
  the only writes are this report and `/tmp/kasegi-r23-falsify-LiteralCarveout/`.
- `home/Projects/bounties` on the author's real machine was never inspected; the claim
  about "ordinary author machine" is `[INFERENCE]` from the r15 world root, not observed.
- The frozen 13-case replay itself passes on as-written bytes (13/13) and fails 6/13 on the
  baseline bytes; I did not re-run controls beyond that, and I do not assert the C1 axis
  has moved.

## Reproduce

The mutated matrices and the hand-built `m1/` tree live in
`/tmp/kasegi-r23-falsify-LiteralCarveout/` (verified present at write time). `/tmp` is
ephemeral and out-of-tree: if it is swept, rebuild each file from the deltas stated inline
above — E3 = the frozen matrix with one case carrying
`"dirs": ["home/Projects/bounties"]` plus either `"files": {"home/Projects/outside.md": …}`
(X1) or `"symlinks": {"home/Projects/bounties/evil.mjs": "@ROOT@/secret/outside.mjs"}` (X2);
E4 = the two single-case matrices named `Y1`/`Y2` and `Y3` with the dirs/files given at
`asym.json`/`asym2.json` above. The verdict outputs themselves are inlined in E1–E6 and do
not depend on the scratch surviving.

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/mirror-containment-check.py                     # 13/13 fixed bytes
python3 corpus/instruments/mirror-containment-check.py \
  --resolver .ufo/waves/round-23/c1-baseline-resolver.py                   # 7/13, 6 escapes FAIL
python3 corpus/instruments/mirror-containment-check.py \
  --fixtures /tmp/kasegi-r23-falsify-LiteralCarveout/mutated2.json         # X1/X2 RESOLVES
python3 corpus/instruments/mirror-containment-check.py \
  --fixtures /tmp/kasegi-r23-falsify-LiteralCarveout/asym.json             # Y2 RESOLVES, Y1 GONE
python3 corpus/instruments/mirror-containment-check.py \
  --fixtures /tmp/kasegi-r23-falsify-LiteralCarveout/asym2.json            # Y3 GONE
awk -F'\t' 'NR==1 || $1 ~ /bounties/' \
  /tmp/kasegi-r23-falsify-LiteralCarveout/m1/tool/citation-survival.tsv    # literal-branch rows
```
