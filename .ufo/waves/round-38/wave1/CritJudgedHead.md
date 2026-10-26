# CritJudgedHead — round-38 judged-head rule attack (claims.json `judged_head_rule`, G2)

Seat: CritJudgedHead (leaf, no dispatch). Item: attack the judged-head rule; propose regex/rule
tightenings; test them on `SCORECARD.md` and `SHONEN.md` at base; receipt only.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only for this seat). Base
`a173b0c2b98c5ae39599fa9be76027fbbead0b9e`; claims-freeze `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`;
wave-1 dispatch commit `700153593eb586c70a6499c8ca225ee4d673bc9b` (= HEAD = `master` = `origin/master`
at read time). No tool installed; no pacman; no network fetch; no mutating git outside a verified
fixture (`git rev-parse --show-toplevel` printed the fixture dir before every fixture operation).
Scratch `/fast/scratch/hyaku/kasegi-r38/CritJudgedHead/` removed on exit.

Text attacked (verbatim, `claims.json`):

> The round-38 judged head J is the `export-ref=` value recorded in `.ufo/waves/round-38/final-gates/all-gates.txt`.
> J is the lane commit that carries every round-38 change except that receipt; the lane tip Y adds only the receipt
> file (`git diff --name-only J Y` = `.ufo/waves/round-38/final-gates/all-gates.txt`). Lane files never name J by
> hash (a commit cannot contain its own hash); the report names J and Y.

and G2 (defect D-B), verbatim:

> `.ufo/waves/round-38/final-gates/all-gates.txt` in the export has header `all-gates v2`, an `export-ref=<40-hex>`
> that is REF or an ancestor of REF with `git diff --name-only <export-ref> REF` a subset of {that receipt path},
> `suite-sha256=` equal to the executing suite's digest, eight `G<n> payload=... closed=1` lines, `closed=8/8 exit=0`,
> eight `selftest case=G<n>` lines and `selftest cases=8 failures=0`; and the round-38 SCORECARD.md section and
> SHONEN.md round-38 lines name the judged head only by reference (`judged head: export-ref of
> .ufo/waves/round-38/final-gates/all-gates.txt`) with zero lines labelling any 7+-hex hash as `final head`,
> `final lane head` or `Final lane commit`

## 1. Verdict on the four questions

1. **Can J..Y contain more than the receipt and still pass?** Yes, five ways under the frozen wording
   (§2 C1–C5): a rename folded into the receipt path (name-only shows one path while a tracked file is
   deleted), a gitlink at the receipt path (mode 160000, `--name-status` still `A`), history-only commits
   that cancel out (diff empty, extra commit in J..Y), a tree object as `export-ref` (archives fine,
   diff-vs-REF = receipt only), and an annotated tag object as `export-ref` (archives, peels, `merge-base
   --is-ancestor` exit 0, diff = receipt only).
2. **Can the receipt's export-ref be a commit that is not on master?** Yes. A tree-equal side-branch
   commit (same tree as the real head, different parent/metadata) is not an ancestor of Y but
   `git diff --name-only <it> Y` = the receipt and its extracted export is byte-identical (§2 C6).
   `merge-base --is-ancestor` is the only discriminator; the frozen predicate's "REF or an ancestor of
   REF with diff subset" does not require it.
3. **Can SCORECARD/SHONEN still name a different "final" hash with wording the regex misses?** Yes.
   Of 14 hash-smuggling prose forms tested against a round-38 hash, the frozen literal caught 1;
   the case-insensitive/same-line variant caught 2; the proposed token rule caught 14/14 (§3.3).
   The base file already contains 7 historical instances the frozen wording misses (split label/value,
   lowercase `final lane commit`, `final hash`, `lane tip`, hyphenated `Final-lane-commit`) (§3.1).
4. **Is the self-reference impossibility handled?** No, and the rule text is literally false: the
   receipt *is* a lane file, is committed at Y, and *does* name J. The impossibility holds only for
   files in J, which makes a `grep -F "$J" SCORECARD.md` guard vacuous (proved: `git grep -F J J` is
   empty by construction; in the fixture `git grep -nF J Y` returns exactly the receipt line). What is
   not handled: any *other* post-base hash can be named in SCORECARD/SHONEN, and nothing binds the
   report's J to the receipt's J.

Structural finding that outranks the four answers: **G2 is unmeetable as written.** The receipt does
not exist in the export of J (`git cat-file -e J:.ufo/waves/round-38/final-gates/all-gates.txt` exits
128 in the fixture), so "`all-gates.txt` in the export" can only mean the export of Y. The frozen
counting command `--export-ref <J>` therefore cannot produce `closed=8/8` if G2 is one of the eight
checks unless G2 reads the receipt from the lane at Y. Round-37 is the same shape: receipt at
`9492c776` names its parent `2735e93f` (bootstrap), the final receipt at `aa88877b` names
`9492c776`, and `git diff --name-status 9492c776 aa88877b` = `M .ufo/waves/round-37/final-gates/all-gates.txt`.
So REF := the receipt commit (Y), J := REF^. Round-37's own `Measured after` line ran
`--export-ref aa88877b` (the receipt commit), not the judged head; the r38 counting command
`--export-ref <J>` is a stricter shape and only works if G2 reads the receipt from Y while exporting J.

## 2. Counterexamples (fixtures; commands and actual output)

Fixture root `$S/fix*` under the seat scratch; each began `git init -q -b main .` and
`git rev-parse --show-toplevel` was asserted equal to the fixture dir. Baseline commit set:
`A` (initial), `J` (adds `y.txt`, `corpus/instruments/r38-closure.sh`), `Y` (adds only
`.ufo/waves/round-38/final-gates/all-gates.txt`, one `export-ref=<J>` line).

Baseline, exact byte targets the fix must compare:

```
$ git -c core.quotepath=false -c diff.renames=false diff --no-renames --name-status -z J Y | od -c
0000000   A  \0   .   u   f   o   ...   a   l   l   -   g   a   t   e   s   .   t   x   t  \0
$ git ls-tree Y -- .ufo/waves/round-38/final-gates/all-gates.txt
100644 blob 2333beed2af211898b194104aac2e0739ebc3dc6	.ufo/waves/round-38/final-gates/all-gates.txt
$ git rev-list --parents -n1 Y
1ce1fe0d53dce0b18959fb8d3af98abc082fd6b9 664f914515ab32b92009c19d2c6a08e02163a30e
$ git cat-file -e J:.ufo/waves/round-38/final-gates/all-gates.txt ; echo $?
128
$ git cat-file -e Y:.ufo/waves/round-38/final-gates/all-gates.txt ; echo $?
0
```

**C1 — rename folded into the receipt (J..Y deletes a tracked file, predicate passes).**

```
$ git checkout -B ren "$J"; mkdir -p .ufo/waves/round-38/final-gates
$ git mv y.txt .ufo/waves/round-38/final-gates/all-gates.txt; git commit -qm REN
$ git diff --name-only "$J" "$R"
.ufo/waves/round-38/final-gates/all-gates.txt
$ git diff --name-status "$J" "$R"
R100	y.txt	.ufo/waves/round-38/final-gates/all-gates.txt
$ git diff --no-renames --name-only "$J" "$R"
.ufo/waves/round-38/final-gates/all-gates.txt
y.txt
```

`--name-only` (rename detection on by default) yields exactly the receipt path, so the frozen
subset test passes while `y.txt` is gone. `--no-renames` exposes it; `--name-status -z` would show
`R100`, not `A`.

**C2 — gitlink at the receipt path (mode 160000; `--name-status` still `A`).**

```
$ git update-index --add --cacheinfo 160000,"$Y",.ufo/waves/round-38/final-gates/all-gates.txt
$ git commit -qm GITLINK ; L=$(git rev-parse HEAD)
$ git diff --name-only "$J" "$L"
.ufo/waves/round-38/final-gates/all-gates.txt
$ git diff --no-renames --name-status "$J" "$L"
A	.ufo/waves/round-38/final-gates/all-gates.txt
$ git ls-tree "$L" -- .ufo/waves/round-38/final-gates/all-gates.txt
160000 commit 1ce1fe0d53dce0b18959fb8d3af98abc082fd6b9	.ufo/waves/round-38/final-gates/all-gates.txt
$ git cat-file -t "$L":.ufo/waves/round-38/final-gates/all-gates.txt
commit
```

Only the `100644 blob` ls-tree mode check catches it. (Also: the file could be a symlink, mode
120000.)

**C3 — cancel-out history (diff is only the receipt; J..Y holds a second commit).**

```
$ git checkout -B canc "$J"; printf 'secret\n' > secret.txt; git add -A; git commit -qm ADD-SECRET
$ rm secret.txt; printf 'all-gates v2\n' > .ufo/waves/round-38/final-gates/all-gates.txt
$ git add -A; git commit -qm REMOVE-AND-RECEIPT ; C=$(git rev-parse HEAD)
$ git diff --name-only "$J" "$C"
.ufo/waves/round-38/final-gates/all-gates.txt
$ git rev-list --count "$J".."$C"
2
```

The name-only subset test passes; the secret exists in lane history though not in the tip tree.
`rev-list --count J..Y == 1` closes it (or `rev-list --parents -n1 Y` = `Y J`).

**C4 — tree object as `export-ref`.**

```
$ T=$(git rev-parse "$J^{tree}")
$ git archive "$T" | tar -t | sort | tr '\n' ' '
a.txt corpus/ corpus/instruments/ corpus/instruments/r38-closure.sh y.txt
$ git diff --name-only "$T" "$Y"
.ufo/waves/round-38/final-gates/all-gates.txt
$ git cat-file -t "$T"
tree
$ git rev-parse --verify "$T^{commit}"
error: 32d6a550b6b924194dfb975ffcc28b01fd36a36a^{commit}: expected commit type, but the object dereferences to tree type
```

`git archive` accepts a tree; the diff test sees only the receipt; the export is the judged bytes.
The 40-hex value is not a commit and "on master" is undefined for it.

**C5 — annotated tag object as `export-ref` (defeats the r37-style ancestor test too).**

```
$ TAGOBJ=$(git mktag <<EOF
object 664f914515ab32b92009c19d2c6a08e02163a30e
type commit
tag judged
tagger t <t@t> 1761500000 +0000

tag object that names the judged head
EOF
)
$ git cat-file -t "$TAGOBJ"
tag
$ git archive "$TAGOBJ" | tar -t | wc -l
5
$ git rev-parse --verify "$TAGOBJ^{commit}"
664f914515ab32b92009c19d2c6a08e02163a30e
$ git cat-file -e "$TAGOBJ^{commit}"; echo $?
0
$ git merge-base --is-ancestor "$TAGOBJ" "$Y"; echo $?
0
$ git diff --name-only "$TAGOBJ" "$Y"
.ufo/waves/round-38/final-gates/all-gates.txt
$ [ "$(git rev-parse --verify "$TAGOBJ^{commit}")" = "$TAGOBJ" ] && echo yes || echo no
no
```

The tag object passes `cat-file -e <ref>^{commit}` and `merge-base --is-ancestor` (the exact
r37 E10 limbs, `r37-closure.sh:647-648`) and archives the judged bytes. Only
`rev-parse --verify "<ref>^{commit}" = <ref>` (and `cat-file -t` = `commit`) separate it from a
commit.

**C6 — export-ref is a commit not on master (tree-equal side branch).**

```
$ T=$(git rev-parse "$J^{tree}"); J2=$(git commit-tree "$T" -p "$A" -m "side copy of J")
$ echo "J2=$J2 tree_equal=yes same_hash=no ancestor=no"   # actual: e5fe7612… tree_equal=yes same_hash=no ancestor=no
$ git diff --name-only "$J2" "$Y"
.ufo/waves/round-38/final-gates/all-gates.txt
$ mkdir x1 x2; git archive "$J" | tar -x -C x1; git archive "$J2" | tar -x -C x2; diff -r x1 x2 && echo EXTRACTED-TREE-IDENTICAL
EXTRACTED-TREE-IDENTICAL
$ git merge-base --is-ancestor "$J2" "$Y"; echo $?
1
```

J2 carries every round byte (same tree), was never on master, and the frozen diff test passes. The
tar digests differ only because `git archive` embeds the commit id in a pax header; extracted bytes
are identical, so the suite cannot tell J from J2.

**C7 — Y == J with the receipt only in the worktree.**

```
$ git checkout -B dirty "$J"; printf 'all-gates v2\nexport-ref=…\n' > .ufo/waves/round-38/final-gates/all-gates.txt
$ git diff --name-only "$J" "$J"
(empty)
$ git status --porcelain
?? .ufo/
```

If the receipt is read from the worktree, every content check can pass with nothing committed.
`git status --porcelain` empty plus reading via `git cat-file blob Y:R` closes it.

**C8 — empty commit between: benign.** A contentless commit E on top of J with Y2 = E + receipt
gives `diff(E,Y2)` = receipt, ancestry ok, `rev-list --count E..Y2` = 1, and `tree(E) == tree(J)`
(verified). The named "judged head" is then E, which is content-identical to J — no measurable
overreach. Do not accuse this; define the judged head as *the maximal tree-equivalent ancestor*
rather than "the commit that authored the changes".

## 3. Regex/rule tests on base `SCORECARD.md` (1509 lines) and `SHONEN.md` (178 lines)

### 3.1 Frozen literal vs historical corpus

`frozen_cs` = `(Final lane commit|final lane head|final head)[^\n]*<7-40 hex>` (the literal predicate,
case-sensitive, label before hash, same line). Matches at base: SCORECARD `[1492, 1494, 1500, 1509]`,
SHONEN `[172]` = **5 of 12** historical "final-ish label + hash" instances. Missed:

| Line(s) | Text | Missing limb |
|---|---|---|
| SC 980 | ``…at lane tip `43c364d`…`` | `lane tip` not in vocabulary |
| SC 987–988 | ``**Final lane commit:`` / `` `7963976e…`**`` | value on the **next line** |
| SC 1110 | ``**Round-33 final lane commit: `7963976e…`**`` | lowercase `final lane commit` |
| SC 1117 | ``final hash `7963976e…` (lane tip `014ee2d7…`…`` | `final hash`, `lane tip` |
| SC 1241 | ``**Round-34 final lane commit: `c1c6a5f8…`**`` | lowercase |
| SC 1271 | ``…final lane commit `0aee0ef…` (recorded in the closing commit).`` | lowercase, ellipsis |
| SC 1507 | ``Anchor ancestor (r36 lane head): `c20300df…` — the r36 Final-lane-commit label…`` | hyphenated label |
| SH 172 | ``evidence (round 37, final lane head aa88877b…)`` | **caught** (this is the r37 drift) |

Case-insensitive + hash-before-label + same-line (`frozen_cs_bidir`) catches 9 of 12; it still misses
the split value (988), `lane tip` (980), `final hash` (1117) and the hyphenated label (1507).
A widened label mix (`(final|judged|closing|shipped|binding|published|measured|filed|anchor)…
(commit|head|hash|tip|sha)`, `lane tip`, `head at filing`) matches **56 lines in SCORECARD and 4 in
SHONEN** at base — all historical. The check is scoped to round-38 text, so these are not false
positives; they prove a whole-file scan is impossible and that the scope must be positional.

### 3.2 Section-heading scoping is vacuous

```
base:  ^## Round 38  -> headings=0 extracted_lines=0
       ^## Round-38  -> headings=0 extracted_lines=0
       ^## [Rr]ound[- ]38 -> headings=0 extracted_lines=0
HEAD 70015359: no `## Round 38` heading in SCORECARD.md either (grep -c 'round 38|Round 38|round-38' = 0)
```

A G5-style "the round-38 SCORECARD section has zero `Final lane commit:` lines" implemented as
`awk '/^## Round 38/{f=1} f'` passes **vacuously** at base and today. Base uses both `## Round 26 —`
and `## Round-26 capabilities` spellings, so a hyphen/space mismatch keeps it vacuous. The scope must
be the added lines (`git diff <base>..Y`), and the check must separately require the section exists.

### 3.3 Attack lines through three rules (round-38 hash `9a10b02…`, historical `f3246559`, 64-hex digest)

| # | Added line | frozen literal | frozen bidir | proposed rule |
|---|---|---:|---:|---|
| 1 | `Final lane commit: 9a10b02…` | caught | caught | FAIL (post-base hash) |
| 2 | `**Final lane commit:**` + next line `9a10b02…` | miss | miss | FAIL (post-base hash) |
| 3 | `9a10b02…` bare | miss | miss | FAIL (post-base hash) |
| 4 | `lane tip 9a10b0` (6 hex) | miss | miss | FAIL (post-base hash) |
| 5 | `closing commit: 9a10b02` | miss | miss | FAIL (post-base hash) |
| 6 | `head at filing 9a10b02` | miss | miss | FAIL (post-base hash) |
| 7 | ``final hash `9a10b02…` `` | miss | miss | FAIL |
| 8 | `<!-- head: 9A10B02FE… -->` (uppercase) | miss | miss | FAIL (uppercase resolves) |
| 9 | `[commit](https://…#commit-9a10b02…)` | miss | miss | FAIL |
| 10 | `the commit the after-column seats measured is 9a10b02` | miss | miss | FAIL |
| 11 | `Round-33 final lane commit: 9a10b02` (lowercase f) | miss | caught | FAIL |
| 12 | `Final-lane-commit: 9a10b02` | miss | miss | FAIL |
| 13 | `the round-38 final head is named in the report` | miss | miss | FAIL (label off-whitelist) |
| 14 | `the head named in the report is 9a10b02` | miss | miss | FAIL |
| — | `judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt` | pass | pass | pass (required) |
| — | `Correction (round 38) — … f3246559 is not a final head` | miss | **caught — false positive on its own required line** | pass (Correction exemption) |
| — | `suite digest sha256: 0da98e37…a30342434d` | miss | miss | pass (64-hex run, boundary lookarounds) |

`9a10b0` (6 hex, not 7) resolves: `git rev-parse --verify 9a10b0^{commit}` →
`9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`; uppercase resolves to the lowercase hash too. Hence the
proposed token threshold is 7 (matching the frozen literal) with the label rule covering the 4–6 gap.

### 3.4 Token-rule false-positive probe on base (post-base = not ancestor-or-equal of base)

| File | distinct tokens, `{7,40}` | post-base | distinct tokens, `{4,40}` | post-base |
|---|---:|---:|---:|---|
| SCORECARD.md | 201 | **0** | 292 | `D3D4` |
| SHONEN.md | 31 | 0 | 57 | 0 |
| LOG.md | 145 | 0 | 237 | 0 |
| PROVINCE.md | 1 | 0 | 11 | 0 |
| corpus/README.md | 9 | 0 | 44 | 0 |
| SKILL.md | 50 | 0 | 118 | 0 |

The `{4,40}` threshold yields exactly one false positive: the defect label `D3D4` sits on
`SCORECARD.md:1312` and resolves to `d3d49bb3e0bc70f13e19ad496198786cdbeb6643`, which is post-base
(`merge-base --is-ancestor` exit 1). At `{7,40}` the token rule has **zero false positives on the
whole historical file**, so it can even be applied unscoped; scoped to added lines it has none by
construction (round-38 delta at HEAD: `git diff <base>..HEAD -- SCORECARD.md SHONEN.md` = 0 added
lines).

## 4. Defects in the frozen rule/G2 (each with the smallest fix)

1. **REF is undefined.** G2 compares against `REF`; `claims.json` never defines it. If an implementer
   sets `REF = export-ref`, the diff is empty and the test is vacuous. Precedent fixes it: the r37 run
   exported `aa88877b` (receipt commit) whose receipt names `9492c776` (parent), diff = receipt only.
   `REF := Y = git rev-parse HEAD = master = origin/master`.
2. **The receipt is not in the export of J.** `git cat-file -e J:R` → 128; "`all-gates.txt` in the
   export" can only mean Y. The suite at `--export-ref J` must read the receipt from the lane at Y
   (or take `--receipt-ref Y`). Without this, the frozen counting command `--export-ref <J>` cannot
   yield `closed=8/8` with G2 among the eight checks.
3. **Diff subset is too weak.** C1 (rename), C2 (gitlink), C3 (cancel-out), C4 (tree), C5 (tag),
   C6 (side branch): use `git -c diff.renames=false diff --no-renames --name-status -z J Y` equal to
   `A\0R\0` or `M\0R\0` (the r37 bootstrap receipt was `M`), plus `ls-tree` = `100644 blob`,
   `cat-file -t J` = commit, `rev-parse --verify "J^{commit}"` = J, `merge-base --is-ancestor J Y`,
   and every commit in `rev-list J..Y` diffs only R (r37 `aa88877b^` = `9492c776` = its header
   export-ref, so an exact-parent pin is unnecessary and reds a re-generated receipt).
4. **Y is not pinned.** Nothing requires Y to be `HEAD`/`master`/`origin/master` at filing, so a
   receipt can name an intermediate tip (r37 D3 recurrence: `83975acc` landed 28 s after `complete`).
   Require all three refs equal and `git status --porcelain` empty.
5. **Ancestry can be rewritten locally.** `refs/replace/*`, `.git/info/grafts` and a shallow clone
   change `merge-base`/`diff` answers without dirtying the tree. At filing the lane currently has
   `shallow=false`, `refs/replace` = 0, grafts absent — assert these, and run the diff with
   `-c core.quotepath=false -c diff.renames=false -z`.
6. **Digest and run-utc do not bind the run.** `suite-sha256` only equals the executing suite if the
   checker executes the blob from Y (not a worktree copy), and the receipt's `G<n>`/`closed=8/8` lines
   are forgeable unless the checker re-runs the committed suite itself and reproduces them; also
   bound `run-utc` to `[committer date of J, now]`.
7. **Label vocabulary is incomplete and case-sensitive, and line-scoped.** Missing `lane tip`,
   `closing commit`, `head at filing`, `final hash`, `shipped/binding/published head`, lowercase
   `final lane commit`, hyphenated `Final-lane-commit`, split label/value (base SC 987–988), HTML
   comments, uppercase hashes, and description-only claims (§3.1, §3.3). Worse, the literal rule
   **flags G5's own required `Correction (round 38)` line** because it contains "not a final head"
   and `f3246559` on one line.
8. **Scope of "SHONEN.md round-38 lines" is undefined.** SHONEN has one heading and four checkbox
   paragraphs; there is no round marker. Scope both files by the diff, and require the canonical
   reference line to exist rather than relying on absence of labels.
9. **Self-reference statement is false and the natural guard is vacuous.** Say: "no file in J names
   J; the receipt at Y is the only lane file that names J, and it does because Y ≠ J". Add the
   forgery tripwire (`git grep -F J J` empty; `git grep -lF J Y` = R only) and bind the report:
   report J = receipt J and report Y = `git rev-parse master` at filing (report-side, since the
   lane suite cannot read the fleet report).
10. **Vacuous heading scope.** Require the `## Round 38`-equivalent section to exist (exactly one
    heading matching `^## Round[- ]38\b`) if any heading scope is used at all; better, use the diff.

## 5. Impacted axes

- `depth:verifiability` (lowest non-retired, 4): the proposed tightening converts G2 from a
  vocabulary check (5/12 historical recall, 0/6 structural holes) into a binding check with 14/14
  prose recall and 0/0 base false positives — a positive move on the owned axis. It does not touch
  the suite's other seven checks.
- `coverage` (7) and `depth:density` (9): untouched — no corpus/registry/knowledge bytes, no base
  line edits; the proposal is append-only to the suite/gate text.

## DELIVERABLE

```
Independent judging check for G2 (D-B) judged-head binding — run by the non-author checker, not the
  suite's frozen-contract G2 — at the receipt commit Y.
  Y := `git rev-parse HEAD`; the filing gate additionally requires `git rev-parse master` =
  `git rev-parse origin/master` = Y, `git status --porcelain` empty,
  `git rev-parse --is-shallow-repository` = false, `git for-each-ref refs/replace` empty and
  `$(git rev-parse --git-dir)/info/grafts` absent.
  R := `.ufo/waves/round-38/final-gates/all-gates.txt`. Require `git ls-tree Y -- R` =
  `100644 blob <40-hex><TAB>R`; read the receipt only as `git cat-file blob Y:R`; first line `all-gates v2`.
  Require exactly one `^export-ref=[0-9a-f]{40}$` line in the header block (the lines before the first
  `== `), never file-wide; J := its value. Require `git cat-file -t J` = commit,
  `git rev-parse --verify "J^{commit}"` = J, and `git merge-base --is-ancestor J Y` exit 0. Require
  `git -c core.quotepath=false -c diff.renames=false diff --no-renames --name-status -z J Y` to be exactly
  `A\0R\0` or `M\0R\0` (one added or rewritten receipt; no rename, delete, mode change or gitlink), and
  for every commit c in `git rev-list J..Y` the same command over `c^ c` to be within {`A\0R\0`,
  `M\0R\0`} (a draft/measured/re-generated receipt chain is allowed; a cancel-out history is not).
  Require `suite-sha256=` = sha256 of
  `git cat-file blob Y:corpus/instruments/r38-closure.sh` = sha256 of the suite bytes the checker executes.
  Re-run the committed suite from `git archive Y | tar -x`, cwd outside the lane:
  `bash corpus/instruments/r38-closure.sh --export-ref J --lane <lane>` and `--selftest --export-ref J`;
  captured stdout must reproduce the receipt's eight `G<n> payload=... closed=1` lines, `closed=8/8 exit=0`,
  eight `selftest case=G<n>` lines and `selftest cases=8 failures=0`, and the receipt's `run-utc` must lie in
  [`git show -s --format=%cI J`, checker UTC now]. G2 reads the receipt from Y, never from the J export
  (R does not exist at J: `git cat-file -e J:R` exits 128).
  Self-reference: `git grep -lF J Y` = R only; `git grep -F J J` empty.
  Judged-head naming, over the lines ADDED by `git diff <base>..Y -- SCORECARD.md SHONEN.md` (scope by the
  diff; if a `## Round 38` section scope is also used it must exist, exactly one heading matching
  `^## Round[- ]38\b`, and an absent/renamed/empty heading is a failure): (i) any line matching
  `(?i)\b(final|judged|closing|shipped|binding|published)\b[^\n]{0,20}\b(commit|head|hash|tip|sha)\b`,
  `\blane tip\b`, `\bhead at filing\b` or `\b(head|tip|sha|hash)\b\s*(:|is|was|=)` is a failure unless it
  references R with no hash token, begins `Correction (round 38)`, or denies a final head
  (not/no/never/cannot); (ii) any 7-40 hex token that `git rev-parse --verify <tok>^{commit}` resolves to
  a commit not ancestor-or-equal of <base> is a failure unless the line begins (after `|`, `-`, `*` or
  spaces) with `Measured before`, `Measured after`, `freeze`, `dispatch`, `base`, `integration`,
  `bootstrap`, `spec`, `wave-1` or `claims-freeze`; (iii) the added SCORECARD lines reference R at least once.
```

Deliverable: 34 lines, sha256 `bd54e9f630d0123ff55213fc6d2b9d3ebe8274c951133c8727ff20355823db28`.

## 6. Verification the main agent should run once the suite lands at Y

1. `bash corpus/instruments/r38-closure.sh --export-ref <J>` from a scratch export of Y →
   `closed=8/8 exit=0`, with G2 reading the receipt at Y; `--selftest --export-ref <J>` →
   `selftest cases=8 failures=0`.
2. `git -c diff.renames=false diff --no-renames --name-status -z J Y` → exactly `A\0R\0` (or `M\0R\0`).
3. For every c in `git rev-list J..Y`, `git -c diff.renames=false diff --no-renames --name-status -z c^ c`
   is within {A/M R}; at filing `git rev-parse HEAD master origin/master` all = Y.
4. `git ls-tree Y -- .ufo/waves/round-38/final-gates/all-gates.txt` → `100644 blob …`.
5. Re-run the §3.3 attack lines as a self-test mutant set (14/14 must be red).
6. `git diff <base>..Y -- SCORECARD.md SHONEN.md | grep '^+'` → every 7+-hex token resolves to an
   ancestor-or-equal of base; the only head mention is the canonical reference line; the
   `Correction (round 38)` line is exempt and present.

## 7. Tooling / scratch

No install or upgrade (authorization unused): analysis used `git` 2.56.0, `python3` 3.14.8, coreutils. All
fixtures under `/fast/scratch/hyaku/kasegi-r38/CritJudgedHead/` (removed on exit); every fixture
`git init` was preceded by `git rev-parse --show-toplevel` matching the fixture dir. Lane reads were
read-only (`rev-parse`, `cat-file`, `ls-tree`, `show`, `diff`, `grep`, `rev-list`, `merge-base`,
`for-each-ref`, `status`). No file outside this receipt was written.

## 8. Revision after the suite-builder exchange

- Exact-parent pin dropped: r37 `aa88877b^` = `9492c776` = the receipt's header export-ref, so the
  parent form would not have red r37; it only reds a receipt re-generated over the same J at a later
  commit. Replaced by the per-commit receipt-only limb over J..Y, which keeps draft->measured->regenerated
  chains green and reds a cancel-out history (fixture: ADD-SECRET then REMOVE-SECRET+receipt;
  `diff(J,Y)` = receipt only, `rev-list --count J..Y` = 2).
- Header scope added: the r37 receipt carries `^export-ref=` twice (line 2 header; line 7 run evidence
  `export-ref=<j> mode=export lane=... suite-sha256=...`), so a file-wide count of 1 reds a genuine
  landing; count only in the header block (before the first `== `).
- Heading scope made non-vacuous: base and HEAD (70015359) have zero `^## Round[- ]38` headings, so a
  section-scoped label rule passes vacuously today; an absent, renamed or empty heading is now a failure.
- Deliverable updated: 32 lines, sha256 `f26a9d6b86d32ce95338a4bc2cd88b4b8e7ac924d7d04673f1fead423bb1cf7d`
  (was 28 lines / `e3c39edf...`).
- Revision 2 (suite-builder counterexample accepted): the blanket post-base token ban was red on a
  real drafted section, `ScribeScorecard.section.md:9` (`Measured before: freeze 9a10b02…` — a
  provenance citation, not a head claim). Replaced with two narrower limbs: a head-assertion phrase
  ban (catches label-only/split lines, `lane tip` at any hex length, `closing commit`, `head at
  filing`, `final hash`, hyphenated and lowercase forms, and any `head is <hex>`), and a post-base
  hash ban that exempts only lines beginning with a provenance label (`Measured before/after`,
  `freeze`, `dispatch`, `base`, `integration`, `bootstrap`, `spec`, `wave-1`, `claims-freeze`).
  Measured on the drafted section: 0 flagged lines, canonical receipt path present; on the 20-line
  corpus: 20/20 as specified (15 red incl. label-only split and 6-hex `lane tip`; 5 pass: canonical
  line, Correction line, freeze line, integration line, 64-hex digest).
- Revision 3 (division of labour agreed): the suite keeps the frozen literal G2 (approved bytes
  `09d46673…`, 38/38 mutants); the two naming limbs are this checker's rule, not the contract's,
  because the denial exemption is prose-sensitive. Landed section evidence: the exact line
  `judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt` is at
  `ScribeScorecard.section.md:10` and twice in `ScribeShonen.block.md` (L35, L58); the section's
  L11 ("The lane files name no commit hash for the round-38 head; the reported lane tip adds only
  that receipt file.") passes only via the `no` denial exemption — accepted as too fragile for a
  contract gate. Residual gap the suite will not catch and the checker must: a stray post-base hash
  under wording outside the literal set (e.g. `lane tip <hash>`, a split label-only line, an HTML
  comment); the canonical reference line still binds the reader to the receipt.
