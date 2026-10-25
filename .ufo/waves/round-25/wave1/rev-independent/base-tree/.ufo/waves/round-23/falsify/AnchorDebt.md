# AnchorDebt — where the lane-relative INTERNAL carve-out is anchored, and where it is not

Seat: `L1Kasegi23.AnchorDebt-2` (critic). Round 23 falsify wave. Read-only review of landed
working-tree bytes; scratch work in `/tmp/kasegi-r23-falsify-AnchorDebt`. No admission, no
score movement, no integration implied.

## Verdict in one paragraph

The carve-out is **named at five anchors across four artifacts** (claim preregistration,
lesson twice, scorecard verdict cell, fixture note) and is therefore not a silent omission at
the round-record layer.
It is **silently absent from the two artifacts a future operator actually reuses** — the
detector's own module contract and the reusable matrix checker — and the places where it is
named state only that the branch is *unchanged*, never that it *credits a real file outside the
lane repo*. The matrix encodes that credit as a **preserved control**, so the headline
`7/7 controls preserved, matrix 13/13` is consistent with an escape being credited, not
evidence against it. An operator who reads the scorecard's Before/After cells, or who reuses
`13/13` as a soundness counter, will over-read C1; an operator who reads the full verdict
sentence to its last clause sees that a carve-out exists but not its size or its shape.

I reproduce the credit myself below, and I show the *same* citation the frozen matrix pins
`GONE` classifying `INTERNAL` under a different placement of the escaped file — so the
discriminator in that case is file placement, not confinement.

## 1. Where it is named

| # | artifact:line | text (quoted) | what it actually says |
|---|---|---|---|
| N1 | `.ufo/waves/round-23/claims.json:4` (`C1.before_observed`) | “relative ../outside.md is INTERNAL (not targeted: explicit lane-relative paths keep prior semantics).” | Names the behaviour and scopes it out. Says nothing about confinement or about the resolved path lying outside the lane. |
| N2 | `corpus/lessons/round-23.md:99-100` | “Literal `exists_any(base)` RESOLVES for bounty citations is deliberately kept (carve-out), and the lane-relative `INTERNAL` branch is unchanged — both are pinned as controls in the matrix.” | Names it, and (correctly) that it is pinned as a control. |
| N3 | `corpus/lessons/round-23.md:143-144` | “The residual lane-relative `INTERNAL` branch remains unconﬁned by design (carve-out) and is not generalized into "the detector is sound".” | The strongest and most accurate statement in the round record. |
| N4 | `SCORECARD.md:403` (C1 verdict cell, final clause) | “Score held: instrument correctness, no source restoration or citation-availability change; the lane-relative `INTERNAL` carve-out is disclosed, not generalized.” | Present. Unquantified; says “disclosed”, not “a path outside the lane is credited”. |
| N5 | `corpus/instruments/mirror-containment-fixtures.json:85` (control note) | “Frozen claim preserves lane-relative semantics: the lane-repo branch runs first, so this stays INTERNAL.” | Names the mechanism; frames the outcome as preservation. |

So the NoHarm seat's substance is already carried by the lesson at N3. My finding is not “the
disclosure is missing”; it is the placement and strength problem below.

## 2. Where it is silently absent (verified absences)

**A1 — `corpus/instruments/resolve.py`, the detector's own contract.** The fix edited this
docstring in exactly the two domains it fixed, and left the third standing:

- `resolve.py:26-33` (BOUNTY, added by this round): “a `../` segment never leaves the root”
  (line 29); “A parent-traversal or symlink escape outside the selected mirror is never
  credited.” (lines 32-33).
- `resolve.py:53-55` (REL, mirror half, added): “`../` walk-outs and symlink escapes are GONE”.
- `resolve.py:52` (REL, lane half, untouched): “-> exists under lane repo? INTERNAL” — no
  qualifier, no confinement claim, no pointer to the carve-out. `git diff 922a4dd --
  corpus/instruments/resolve.py` shows this line unchanged.
- `resolve.py:64-66` (untouched, base `922a4dd` line 57-59): “So every class except GONE
  resolves by construction; INTERNAL is assigned only to lane-repo-relative tokens that
  resolve against the lane repo (non-resolving relative tokens are GONE, sub-kind
  `rel-unresolved`).”

Under the natural reading of that last sentence, an `INTERNAL` row resolves *in* the lane repo.
It does not: `classify` only joins and tests existence, and the join can leave the repo
(`resolve.py:247-250`). Nothing in the module says so. `grep -nE 'unconf|carve|not confined'
corpus/instruments/resolve.py` → no matches. A reader of the instrument is told escapes are
handled three times and told about the exception zero times.

**A2 — `corpus/instruments/mirror-containment-check.py:16-18`**, the reusable checker's
contract: “Escape cases pin GONE. Controls pin the class that must survive the change. This
instrument measures the detector's classification only…”. It never says that one of the seven
controls *is* an escape. `SCORECARD.md:412-414` promotes this script as a capability
(“replay a frozen detector matrix on real copied CLI bytes … and fail closed on digest/quote
corruption”) without repeating the carve-out.

**A3 — the receipt cannot show it.** `mirror-containment-check.py` parses only the `citation`
and `class` TSV columns (`i_cite = header.index("citation")`, `i_cls = header.index("class")`),
so `c1-fixed.json`'s `lane-relative-parent-internal-control` entry records
`actual: INTERNAL` with **no `resolved_path`**. The one datum that would expose the credit — the
resolved path outside the lane — is dropped from the evidence file. Auditing “7/7” therefore
requires re-running the CLI by hand.

**A4 — `corpus/instruments/mirror-containment-fixtures.json:3`** (“purpose”): “Paths never
leave the case root except by the traversal the citation itself performs” — accurate, but the
purpose string never distinguishes “traversal that lands inside the lane” (control) from
“traversal that lands outside it and is still credited” (also a control).

## 3. Over-read test on the scorecard row

`SCORECARD.md:403`, columns as printed:

- Before: “escape fixtures credited `MIRROR-EQUIVALENT`: **0/6 GONE**; matrix 7/13, exit 1”.
- After: “**6/6 escape GONE, 7/7 controls preserved, matrix 13/13, exit 0**”.
- Verdict: “**Improved, score held 4.** … the lane-relative `INTERNAL` carve-out is disclosed,
  not generalized.”

What the cells support: six *mirror-fallback* escape cases went from credited to `GONE`, and
every pinned expectation still holds. That is true — I replayed it (below).

What the cells invite: the token `escape` is unqualified, the total `13/13` is presented as one
number, and one of the seven preserved controls is itself an escape whose credited path is
outside the lane. A reader who stops at the Before/After cells concludes the detector's escape
surface is closed; a reader who quotes `13/13 exit 0` as soundness inherits the over-read. The
caveat sentence is real but is (i) in the same cell as the score-hold prose, (ii) about
*disclosure*, not about the credit, and (iii) contradicted by the two section titles that carry
the broader claim: `SCORECARD.md:370` “C1 depth:verifiability (lowest, score 4): **detector
soundness**” and `corpus/lessons/round-23.md:1` “Round 23 — **detector soundness** and …” —
whereas the frozen C1 claim is only “Make **MIRROR-EQUIVALENT** sound” and the attempt-2
section header gets it right (`corpus/lessons/round-23.md:89`, “mirror-fallback soundness”).
That is the same title-vs-claim mismatch class M1 corrected for r22.

**Answer to the assigned question: yes, an operator reading the scorecard row would over-read
C1 — not into believing the carve-out is undisclosed, but into believing the escape surface is
closed and that `13/13` is an escape-soundness counter.** The row is defensible only if read as
“mirror-fallback confinement only”; nothing in the numeric cells forces that reading.

## 4. Counterexample (my reproduction, not the L1's claim)

Setup, all in `/tmp/kasegi-r23-falsify-AnchorDebt`, `resolve.py` copied byte-for-byte from the
lane (`sha256 ed9a9dae…`):

```sh
R=/tmp/kasegi-r23-falsify-AnchorDebt
mkdir -p $R/tool $R/A/{home/Projects,lane,relocated/tbh,outside-vault} \
         $R/B/{home/Projects,lane,relocated/tbh,relocated/outside-vault}
cp corpus/instruments/resolve.py $R/tool/
printf '# probe\n\n- `../outside.md:1`\n- `../outside-vault/secret.mjs:1`\n- `../relocated/tbh/ops/rank.mjs:1`\n' > $R/A/lane/SKILL.md
cp $R/A/lane/SKILL.md $R/B/lane/SKILL.md
printf 'x\n' > $R/A/outside.md
printf 'x\n' > $R/A/outside-vault/secret.mjs
printf 'x\n' > $R/A/relocated/tbh/ops/rank.mjs
printf 'x\n' > $R/B/relocated/outside.md
printf 'x\n' > $R/B/relocated/outside-vault/secret.mjs
printf 'x\n' > $R/B/relocated/tbh/ops/rank.mjs
HOME=$R/A/home KASEGI_MIRROR=$R/A/relocated/tbh python3 $R/tool/resolve.py $R/A/lane
sed -n '2,4p' $R/tool/citation-survival.tsv
HOME=$R/B/home KASEGI_MIRROR=$R/B/relocated/tbh python3 $R/tool/resolve.py $R/B/lane
sed -n '2,4p' $R/tool/citation-survival.tsv
```

Observed (verbatim):

```
== A: escape targets next to the lane root ==
exit 0 distinct=3 resolves=0 mirror=0 internal=3 other=0 gone=0 skill=3/3 corpus=0/0 all=3/3
   ../outside-vault/secret.mjs:1 | INTERNAL | /tmp/…/A/lane/../outside-vault/secret.mjs
   ../outside.md:1             | INTERNAL | /tmp/…/A/lane/../outside.md
   ../relocated/tbh/ops/rank.mjs:1 | INTERNAL | /tmp/…/A/lane/../relocated/tbh/ops/rank.mjs
== B: same cites, escaped file under the mirror's sibling tree (as the matrix places it) ==
exit 0 distinct=3 resolves=0 mirror=0 internal=1 other=0 gone=2 skill=1/3 corpus=0/0 all=1/3
   ../outside-vault/secret.mjs:1 | GONE     |
   ../outside.md:1             | GONE     |
   ../relocated/tbh/ops/rank.mjs:1 | INTERNAL | /tmp/…/B/lane/../relocated/tbh/ops/rank.mjs
```

Three facts this establishes:

1. `../outside.md` (exactly the cite of the matrix's `lane-relative-parent-internal-control`)
   resolves to `<case>/outside.md`, i.e. the **parent of the lane root**, and is credited
   `INTERNAL` — the class whose published meaning is “inside the lane repo”.
2. `../outside-vault/secret.mjs` is the **exact cite** of the matrix's
   `relative-mirror-fallback-escape`, pinned `GONE`. It is `GONE` only because the fixture puts
   the escaped file at `relocated/outside-vault/…` so the lane branch misses. Move the same
   escaped file one level above the lane root and the same citation is `INTERNAL`. The case's
   verdict is therefore a function of fixture placement, not of confinement; the escape class
   does not cover the lane branch.
3. `../relocated/tbh/ops/rank.mjs` — a traversal *into* the mirror — is credited `INTERNAL`
   rather than `MIRROR-EQUIVALENT` in both layouts, so the lane branch also pre-empts the class
   the mirror branch would assign.

**Live instance.** This is not purely latent. `corpus/instruments/README.md:108` contains the
prose token `` `../` ``; `is_pathlike` accepts it, and `classify` credits it (compact form of the probe I ran; the
same `classify` call returned exactly this tuple):

```
python3 -c 'import importlib.util,os; s=importlib.util.spec_from_file_location("r","corpus/instruments/resolve.py"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(m.classify("../", os.getcwd(), m.MIRROR_ROOT))'
('INTERNAL', '/home/vgpnk/Projects/shokunin/kasegi-shokunin/../', 'literal', 'rel')
```

On a working-tree copy of `SKILL.md` + the 65 `corpus/**/*.md` files, the copied CLI reports
`distinct=1620 … internal=147 … all=159/1620` and that token is `INTERNAL` at
`<copy>/../`, outside the lane copy — one non-citation inside the published numerator. The
token exists at the frozen base (`git grep -n '`\.\./`' 922a4dd` → `corpus/instruments/README.md:108`),
and the baseline resolver (`c1-baseline-resolver.py`) on the same copy gives the identical class
(`'../' baseline: INTERNAL  fixed: INTERNAL`, class changes base→fixed = 0).

**Consequence for the no-harm guard.** The guard's `changed=0 added=0 dropped=0` is therefore
*also* the statement that this outside-lane `INTERNAL` credit survived untouched; it is
confirmation that the branch was not touched, not evidence that no outside-lane path is
credited. (The lesson already publishes the guard as vacuous for a different reason —
`mirror=0`. Both vacuities point the same way.)

## 5. Impacted axes

- `depth:verifiability` (C1's axis): the *claim* (“make MIRROR-EQUIVALENT sound”, plus declared
  fixtures) is not falsified — the six mirror cases and seven pinned expectations reproduce
  (`cases=13 escape=6 controls=7 pass=13 fail=0`, `matrix_sha256=5e61a33e…b5e76a9`,
  `resolver_sha256=ed9a9dae…`, exit 0). What is falsified is the **evidence strength carried by
  the numeric cells** and the **generalization available from the artifact layer**: the
  instrument contract implies escapes are never credited, one preserved control credits one,
  and the receipt schema cannot show it. That is a verifiability defect in the record, not a
  score move.
- `coverage`: untouched; none of this is F06–F08 evidence.
- No claim here touches admission, score, or the frozen matrix's validity for its stated scope.

## 6. Smallest safe correction (read-only recommendation; I made no edits)

Ordered by cost, each independently sufficient to stop the over-read:

1. **One docstring line** in `resolve.py` at the untouched REL lane clause (`:52`) and/or
   `:64-66`: “the lane branch is **not** confined: a `../` walk-out that exists relative to the
   lane root is credited `INTERNAL` even when it resolves outside the repo (deliberate r23
   carve-out).” Same sentence in `mirror-containment-check.py:16-18` for the control set.
2. **Receipt schema**: keep `resolved_path` for every case in `mirror-containment-check.py`
   (the TSV already carries it). `7/7 controls preserved` then shows `<case>/outside.md` next
   to an `INTERNAL` verdict and is self-auditing.
3. **Scorecard wording** (does not touch the frozen matrix): qualify the After cell —
   “7/7 controls preserved (one, `lane-relative-parent-internal-control`, pins the **unconfined**
   lane branch: a parent-traversal file outside the lane is credited `INTERNAL`)”; align
   `SCORECARD.md:370` / `lessons/round-23.md:1` from “detector soundness” to “mirror-fallback
   soundness”, matching `lessons/round-23.md:89` and the claim itself.
4. **Do not** add a red lane-escape case to `mirror-containment-fixtures.json` inside round 23:
   the matrix is frozen and the 13/13 receipt is its evidence. A lane-confinement matrix belongs
   to a new claim, with `../outside-vault/secret.mjs` + `outside-vault/secret.mjs` at the case
   root as its red case (proven `INTERNAL` today, §4 fact 2).

## 7. Scope limits

- I attacked only the lane-relative `INTERNAL` branch and the disclosure of it. I did not
  re-adjudicate the six mirror-escape fixtures, the symlink cases, the canonical-alias gate, or
  the F06–F08 evidence; other seats hold those.
- **Adjacent, not claimed here:** the untouched literal `exists_any(base)` carve-out may make the
  newly written BOUNTY sentence “a `../` segment never leaves the root” false when the escaped
  file exists at `$HOME/Projects/…` (literal hit precedes the mirror check). That is the
  literal-carve-out seat's finding; I flag it only so the two are not double-counted.
- The `INTERNAL` live credit I found is one degenerate prose token (`../`), worth 1/1620 of the
  working-tree numerator; I make no claim that the committed `citation-survival.tsv` (dated
  2026-10-14, counts `RESOLVES 10 / INTERNAL 124 / GONE 1346`) is the attempt-2 run — its totals
  differ from the lesson's frozen-export figures, and I did not re-derive the frozen export.
- No host configuration, package transaction, network access, or repo/git mutation was made;
  no tool was installed. All scratch state is under `/tmp/kasegi-r23-falsify-AnchorDebt`.
