# ExecDatawalk — round-35 spot-check §5 routed-defect walk (round 36)

Seat: `ExecDatawalk` (executor, leaf). Judged axis: `depth:verifiability`, calibration. Milestone:
round-36. Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` — **no lane file written**; every
measurement is read-only git or a run of a committed instrument over a scratch `git archive` export.

Item: walk the six routed defects of `corpus/lessons/round-35-verifier-spotcheck.md` §5 against the
base tree and produce an open/closed matrix with the exact command and output for each, so that the
selection of C1's E1–E9 is grounded in measurement rather than in the spot-check's prose.

## 1. Base bytes under test

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git rev-parse HEAD
b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6
$ git archive cc692008b0cfd58d18275aa6c4aed79620120799 | tar -x -C $S/base   # 126M, export_ok
```

| object | blob at base | sha256 | size |
|---|---|---|---|
| `SCORECARD.md` | `a1e366fc56a7e3a986d803d58eef374932e62439` | `ed6e931f795c070eda0b996654fd5c1cf7d9b118432e1ee7fee49173946fcd94` | 1404 lines |
| `corpus/instruments/r35-defect-closure.sh` | `ac96d7b7321e8525dac005e75b722528cbcd7e29` | `0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f` | 834 lines |
| `SKILL.md` | `b1bdf8f914f921b97608be883002fbd39077d0e9` | — | — |
| `corpus/lessons/round-35.md` | `dd7cb0cb4430d5f4097f415d53a7ee5496915dc0` | — | — |
| `.ufo/waves/round-35/wave1-results.json` | `ef2e87c44cb4dea1d9ba88e5d69cbf85259786dd` | — | 301,842 B |

Chain context (read-only): base `cc692008` contains the post-`complete` round-35 commits —
`8ce6fb4` (D1 wording), `5a25337` (wave leftovers), `bb2dc8c`, `48e6053`, `87f6b95` (the spot-check
itself), `980aa3d` (wave-done integration) — and the judged head is `0aee0ef` with r35 base
`3266c993`. `git merge-base --is-ancestor 0aee0ef… HEAD` → yes.

## 2. Matrix (open/closed at base; exact command and output per defect)

`$S` = scratch seat dir, `$B` = base export, `$A` = `0aee0ef` export, `$R35B` = `3266c993` export.

| # | routed defect (spot-check §5) | probe (exact) | observed output | status at base | E-check it grounds |
|---|---|---|---|---|---|
| 1 | **Close against one head** — run the suite over `git archive <final commit>`, not the worktree | `bash corpus/instruments/r35-defect-closure.sh --export-ref cc692008…` | `r35-defect-closure: unknown argument: --export-ref` (exit 2) | **OPEN** — no export mode | E1 + E9 |
| 1b | — | `bash …r35-defect-closure.sh --root $B` (pure `git archive` export of the all-fixed base) | `D4 check=tracked=0,provenance=1 open=1` … `closed=6/7 exit=1` | **OPEN** — one check is index-bound, so an export can never read 7/7 | E4 |
| 1c | — | plain run at lane HEAD `b47f2cd` | `closed=7/7 exit=0`; hex tokens in output: `1 c1c6a5f` (the D1 payload, **not** the measured head) | **OPEN** — output carries no head identity | E1 |
| 2 | **Re-claim with frozen evidence** — a next-round claim may carry r35's closures only with a frozen export run of that head | `git cat-file -e 0aee0ef:<six claim-bearing paths>` | all `absent` (`S052.txt`, `c1-controls/fake-suite.sh`, `c2-controls/junk-f18.md`, `wave1/ExecDoNothingReject.md`, `wave1/ScribeLesson.md`, `wave1.ready`) | **OPEN at claim level, PARTIAL in fact** | C1 `counting_commands[2..4]` |
| 2b | — | the only late-head export run on record: `.ufo/waves/round-35/wave1/ExecDoNothingReject.md:326` (`git archive 5a253372… \| tar -x -C $S/head5a25`), suite run at `:344` | that receipt's own readings: export → `closed=6/7 exit=1` (`D4 tracked=0`); clone of the same commit → `closed=7/7 exit=0` | the green number is a clone/worktree reading; the **export** reading is 6/7 | E1/E4 |
| 2c | — | `sha256sum $B/corpus/source-snapshots/round-35/S052.txt` vs the round-35 manifest `sha256` | both `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826` | **CLOSED** (capture is bound) | C2 |
| 3 | **D1 guard is file-wide literal** | `grep -cF 'filled by the L1' SCORECARD.md` | base **0**; judged head **1**, at `:1271`, inside the `## Round 35` section starting `:1263` | **OPEN** — spelling- and identity-blind (§5) | E1 |
| 3b | — | `sed -n '/^## Round 35/,/^## /p' SCORECARD.md \| wc -l` (naive first-heading scoping) | base **22** lines (stub only); base has **two** `## Round 35` headings (`1263`, `1284`) | **OPEN** — a naive section extractor misses 120 lines of the owning section | E1 |
| 4 | **Append corrections, not rewrites** (D6 rewrote a round-34 bullet in place) | `git diff --numstat 3266c993 0aee0ef -- .ufo/waves/round-34/wave1/L1Integration.md` | `6 3` — three committed lines deleted | **OPEN** — original bytes gone; the note discloses but does not preserve | E6 (and E7's shape) |
| 5 | **False evidence lines at A** — lesson `## Gate` and `## No-harm` | `git show 0aee0ef:corpus/lessons/round-35.md \| grep -n 'source-recheck exit 0 on committed bytes'` → `15`; base lesson → **0** | the line was **deleted/restructured** by `980aa3d` (`git log -S` shows that commit as last touching it); no correction note exists | **OPEN** — reconciled by rewriting, not errataed | E8 |
| 5b | — | `git diff --numstat 3266c993 0aee0ef -- SKILL.md LOG.md` vs `… 5a25337` | at A: `10 0 LOG.md` only (SKILL lines **absent** = 0/0); at 5a25337: `10 0 LOG.md` + `13 0 SKILL.md` | base lesson `:428` now asserts `SKILL.md 13 0` and `LOG.md 10 0` — true only after the late commits | E8 |
| 5c | — | `grep -c 'verifier spot-check' corpus/lessons/round-35.md` · `grep -n 'spot-check' corpus/QUALITY.md` | **0** · no round-35 row (only older rounds' citations) | the §5.1 companion ask ("append a lesson/QUALITY row citing this spot-check") is unmet | E8 |
| 6 | **Dirty tree at closure** | `git status --porcelain` **now** | **9** untracked paths, all `.ufo/waves/round-36/*` (wave in flight); `/fast/scratch/hyaku/kasegi-r36/` → **40** seat dirs | **OPEN by construction** — at r35 filing 9 paths, after `48e6053` 6; the base *commit* is clean, so only a filing-time read can judge it | E9 |

## 3. Defect 1 — close against one head: the suite has no export mode

```
$ grep -n -- '--export-ref' corpus/instruments/r35-defect-closure.sh ; echo $?
1                                          # 0 hits
$ grep -n -- 'git archive' corpus/instruments/r35-defect-closure.sh
13:#   bash corpus/instruments/r35-defect-closure.sh --root DIR
14:#       The same seven checks against another tree (e.g. a `git archive`
                                           # both hits are header prose; no invocation
$ grep -n 'export' corpus/instruments/r35-defect-closure.sh
67:#       `git diff --numstat` deletion count cannot express on a git-free export).
122:  --root DIR     run them against another tree (base export -> `closed=0/7 exit=1`)
$ grep -n 'LANE_ROOT=' corpus/instruments/r35-defect-closure.sh
109:LANE_ROOT=/home/vgpnk/Projects/shokunin/kasegi-shokunin
```

Three structural consequences, each measured:

1. **The caller must extract; the instrument never names a head.** `--root` takes a directory. The
   plain run is hardcoded to the live lane worktree (line 109) and its output names no head — the one
   7–40-hex token in the output is `c1c6a5f`, a D1 *payload*, not the measured revision.
2. **A pure `git archive` export cannot be scored.** In `$B`: `git rev-parse --show-toplevel` →
   `fatal: not a git repository (or any parent up to mount point /)` (exit 128). `check_d4` (line
   205) counts `git ls-files -- .ufo/waves/round-34/wave1-results.json`, so on the all-fixed export
   the suite reads:

   ```
   D4 check=tracked=0,provenance=1 open=1
   closed=6/7 exit=1
   ```

   The lane's own fixtures README documents the mechanism (`corpus/instruments/r35-fixtures/README.md`
   lines 38–46: "`git ls-files` resolves the top-level repository of its cwd, so an in-place run would
   credit the lane's own index for D4"), so the failure is known and documented, not latent.
3. **The 0/7 base control is real** (defect 1 is not a false alarm about the base limb):

   ```
   $ bash corpus/instruments/r35-defect-closure.sh --root $R35B    # 3266c993 export
   D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
   D7 check=supersedes-R22=0,supersedes-R23=0 open=1
   closed=0/7 exit=1                                               # exit 1
   ```

   So the suite distinguishes base from fixed on a *tree*, but the "one head" question — which bytes
   — is answered only by the caller's `--root`, never by the instrument. C1's `--export-ref` closes
   exactly this: the instrument creates the export from the ref it names and reports the ref in the
   header. Line 205 also tells E4 what to do instead: `git ls-tree <ref> -- <path>` is ref-bound and
   export-safe, `git ls-files` in `$root` is not.

## 4. Defect 2 — re-claim with frozen evidence

The late head `5a253372` *was* exported and run, by a seat, in the round's last wave receipt
(`ExecDoNothingReject.md` §4): `git archive 5a253372… | tar -x -C $S/head5a25` (export_ok), S052
capture + both controls present, `source-recheck` exit 0, and the suite on that export reading
`closed=6/7 exit=1` with `D4 tracked=0`; a `git clone` + `checkout` of the same commit reads
`closed=7/7 exit=0`. C2's counters on the export read `frontier=18 rows=52 s052=1 citing=1` and
`PASS F18 … ids=S052`.

So the exact gap the spot-check names is measurable: the *export* run exists but its green number
required a git clone, and no claims-level frozen export run binds `5a253372` to `closed=7/7`. At
`0aee0ef` six claim-bearing paths the r35 claims rest on are absent from the tree
(`S052.txt`, both controls, two receipts, the ready marker), which is why the judged revision could
not be re-claimed. At base all six are present and the capture digest is bound
(`d69349e8…` = manifest `sha256`), so base bytes *can* support a re-claim — provided the r36
instrument produces the export run itself (defect 1).

## 5. Defect 3 — the D1 guard is a file-wide literal

`SCORECARD.md` has **two** identically-worded `## Round 35` headings at base (starts `1263`, `1284`;
the 19-line stub and the receipt-grounded block). The placeholder at the judged head sat at `:1271`,
inside the first block; at base the same block reads `final lane commit \`0aee0ef…\` (recorded in the
closing commit)`.

```
# base
$ grep -cF 'filled by the L1' SCORECARD.md          -> 0     (grep exit 1)
$ grep -cF '<LANE_HASH>' SCORECARD.md               -> 0
# judged head $A
$ grep -cF 'filled by the L1' SCORECARD.md          -> 1     (line 1271)
$ awk '/^## Round 35/{f=1;next} /^## /{f=0} f' $A/SCORECARD.md | grep -E 'filled by the L1|<LANE_HASH>'
8:Measurement state: … final lane commit filled by the L1 in the closing commit.
```

A section-scoped read therefore *works* on the judged head — but only if it reads **all** blocks with
that heading: the naive `sed -n '/^## Round 35/,/^## /p'` returns 22 lines at base (the stub) and
silently omits the 120-line owning block, while the all-blocks awk returns 140 lines.

Measured for all three refs with `git show <ref>:SCORECARD.md | awk '/^## Round 35/{f=1;next}
/^## /{f=0} f'` (three separate counters, because they disagree):

| ref | block lines | placeholder-bearing lines (`filled by the L1\|<LANE_HASH>`) | full 40-hex tokens in the block |
|---|---:|---:|---:|
| `3266c993` r35 base | **0** (no `## Round 35` heading at all; round 34 is the last) | 0 | 0 |
| `0aee0ef` r35 judged | 19 | 1 | 0 |
| `cc692008` base | 140 | **0** | **3** |

The same extractor reads **nothing** at the r35 base (green by absence unless the check also asserts
the section exists), a **19-line** stub at the judged head, and a **140-line** document at base; the
base block's three full 40-hex tokens come from the round-35 claims preamble in the second heading
block (not from the lane-commit line). So an E1 implementation that selects text by heading ordinal is
reading a different document on each revision it must certify, and "0 hits / 1 hit" means different
things under the placeholder counter and the hash counter. E1 must anchor on the `Final lane commit`
label line inside the round's own section, never on a heading span, and must require the section to
exist.

The r35 base also shows why the literal alone is insufficient, measured in the round-34 section
(heading `:1121`), which carries **two** lane-commit slots:

```
$ git show 3266c993:SCORECARD.md | sed -n '1129,1130p'
`c2-controls/before.txt`) and `census-before.txt`. **Final lane commit: the L1 fills this line in the
closing commit.** This section is written at the wave-1 integration state on the bytes digested under
$ git show 3266c993:SCORECARD.md | grep -nF 'filled by the L1'
1240:**Round-34 final lane commit: filled by the L1 in the closing commit.** Every value in this section
```

The prose spelling sits in the slot the label owns (`:1129-1130`) and is invisible to the D1 literal,
which counted only the second slot (`:1240`). A D1 that reads 0 after fixing `:1240` would leave a
placeholder in `:1130` and report closed — the spelling-brittleness the spot-check routed. `pick`
(label + continuation → first 40-hex) returns none for **both** slots at that revision, so the
ancestry limb and the literal counter are red there for different reasons: the ancestry limb for a
missing hash in each slot, the literal for a count that saw only `:1240`. At base both slots are
filled (`:1130` and `:1241` → `c1c6a5f826…`), which is why the literal reads 0.

Both defects of a literal matcher were reproduced on scratch copies:

```
# respelling inside the section: prose placeholder, no literal
$ sed 's/filled by the L1 in the closing commit/filled in by the L1 at closure/' $A/SCORECARD.md > p.md
file-wide=0     section-scoped=0          # both limbs blind
# mention/negation: a TRUE sentence fails the check
$ printf '\nthe token `filled by the L1` is retired and does not occur.\n' >> base/SCORECARD.md
file-wide=1                                # check reads OPEN on a correction note
```

The clause is `check_d1` line 164, `grep -c -F -- 'filled by the L1' SCORECARD.md` — file-wide, so
it cannot attribute a hit to the round that owns the line and cannot tell a placeholder from a
quotation of one. This is why E1 replaces the literal with structural binding (token absence **and**
a Final-lane-commit hash that resolves and is an ancestor), and why the section scope must be defined
as "every block whose heading is the round's", not "the first such heading".

## 6. Defect 4 — append corrections, not rewrites: the D6 rewrite site

```
$ git diff --numstat 3266c993 0aee0ef -- .ufo/waves/round-34/wave1/L1Integration.md
6	3	.ufo/waves/round-34/wave1/L1Integration.md
```

At base the file carries, at `:30-31`, the **replacement** bullet (`The round-33 summary
ExecRegressionC1 filed its receipt, committed in c1c6a5f (round-34 closure); …`) and at `:34` the
note `- Correction (round 35): the bullet above was corrected in place — the dead-seat claim was
false; …`. The original sentence (`did not file a receipt (dead seat`) reads 0.

Marked location: `.ufo/waves/round-34/wave1/L1Integration.md:30-34` (base), rewriting the round-34
receipt's committed bullet from `3266c993` — three deleted lines, six inserted, no preserved original.

The deeper finding is that the round's own check **mandates** the rewrite: `check_d6` line 240 is

```
[ "$stale" -eq 0 ] && [ "$corr" -ge 1 ] && exit 0
```

with `stale` = count of `did not file a receipt (dead seat` in that file. A tree that preserves the
original and appends the correction — the append-only form the frozen `after` asked for — reads
`stale=1` and is scored **OPEN**. So E6, if it is written as a presence check over the same file,
reproduces the defect it is meant to close: it must accept the preserved original *plus* an appended
errata that names it (R16's form), or it is only measuring that the stale bytes were destroyed.
E7 (`supersedes R22` / `supersedes R23` presence) has the same shape — it cannot tell an appended
row from a row that replaced one — and is currently the round's only fully green append-class check.

## 7. Defect 5 — the false evidence lines were rewritten away, not corrected

At the judged head, `corpus/lessons/round-35.md:15` read `… source-recheck exit 0 on committed bytes
…` and `:39` read `Numstat: \`SKILL.md\` +13/0 …, \`PROVINCE.md\`/\`LOG.md\` 0 changed`.

Measured at that head: `git diff --numstat 3266c993 0aee0ef -- SKILL.md LOG.md` → `10 0 LOG.md` only;
`SKILL.md` does not appear at all (0/0), so both halves of `:39` were false (SKILL was 0/0, LOG was
10/0), and `:15` was false because the S052 capture was absent at that head.

At base both sentences are gone in the form quoted: `grep -cF 'source-recheck exit 0 on committed
bytes'` → **0**, and `:428` now asserts `SKILL.md 13 0` and `LOG.md 10 0` — numbers that became true
only at `5a25337` (`git diff --numstat 3266c993 5a25337 -- SKILL.md LOG.md` → `13 0 SKILL.md`,
`10 0 LOG.md`). `git log -S` attributes the removal to `980aa3d` ("seat-final lesson"), which carries
no correction naming the false lines. There is also no round-35 lesson or QUALITY row citing the
spot-check (`grep -c 'verifier spot-check' corpus/lessons/round-35.md` → 0; QUALITY cites only older
spot-checks). This is exactly the class R16 codifies: "a check that turns green because the stale
sentence was reworded or deleted has closed nothing." E8 must therefore record the correction for the
two specific lines, not just assert the round-36 lesson exists.

## 8. Defect 6 — dirty tree at closure

Judged at filing, not after: the spot-check read **9** porcelain paths at 04:01 and **6** still
moving at 04:05. At base those bytes are committed, so `git status` at base is clean — the defect is a
closure-order property, invisible in tree content. Current read (wave in flight, `15:38Z`):

```
$ git status --porcelain | wc -l
9                # all under .ufo/waves/round-36/ (build-spec, dispatch, plan/run logs, spec, ready, wave1/)
$ ls -1 /fast/scratch/hyaku/kasegi-r36/ | wc -l
40               # live seat dirs, this seat's included
```

E9 must therefore be a filing-time read of both limbs (porcelain empty **and** no `kasegi-r36` seat
dir), which is also why the frozen claims list it as E9 rather than a claim counter.

## 9. Two further identity/satisfiability findings (needed by E3 and E4)

**A. D3's literal matches a different instrument — the round-35 suite was never registered.**

```
$ grep -cF 'r35-defect-closure.sh' SKILL.md      -> 0
$ grep -cF 'r36-closure.sh' SKILL.md             -> 0
$ grep -cF 'r-defect-closure' SKILL.md           -> 4
$ grep -nF 'r-defect-closure' SKILL.md | head -1
1097:| r-defect-closure.sh | gate\|probe | `bash corpus/instruments/r-defect-closure.sh [--root DIR]` …
```

The four hits are the **round-33** instrument's registry row (R1–R9, `closed=K/9`) and its three
prose lines. `r35-defect-closure.sh` (D1–D7, `closed=K/7`) is registered nowhere, yet `check_d3`
(line 194, fragment `r-defect-closure`) reads `registry-r-defect-closure=4` → **open=0**. A
round-34 defect was closed by a fragment that a different basename satisfies; the round's own
instrument was never added to the registry home. E3's "**exact basenames**" requirement is therefore
load-bearing, and at base it is red for both names (0/0): round 36 must add the rows.

**B. E4 as frozen is unsatisfied at base — there is no round-35 provenance note.**

```
$ git ls-files | grep -i provenance
.ufo/waves/round-34/wave1-results.json.provenance.md
corpus/instruments/r35-fixtures/{D1,D2,D3,D5,D6,D7,clean,two-defect/D1D2}/.ufo/waves/round-34/wave1-results.json.provenance.md
$ ls .ufo/waves/round-35/ | grep -i 'result\|provenance'
wave1-results.json
```

`check_d4` (line 209) reads `.ufo/waves/round-34/wave1-results.json.provenance.md`, so the round-35
suite is green on the *round-34* artefact. Round-35's own results file is tracked (`tracked=1`) but
has no provenance note, so C1's E4 ("round-35 `wave1-results.json` tracked **with provenance note**")
reads red at base: round 36 must land
`.ufo/waves/round-35/wave1-results.json.provenance.md` (digest, producer, what the file is — the
round-34 note is the template) or E4 cannot pass at the final head. Recorded as an R22/R25-class
satisfiability item, not a defect in the round-36 claim's wording.

**C. E1's hash limb needs an explicit form rule.** The round-35 "Measurement state" line carries **0**
full 40-hex tokens. At the judged head (`SCORECARD.md:1271`) it names four abbreviations with
ellipsis — `3266c993…`, `617496b9…`, `da2d3c68…`, `aa6ad99…`; at base the same line carries five,
adding `0aee0ef…`. All resolve unambiguously (`--disambiguate` → 1 candidate) and are ancestors of
`master`. (An earlier aggregate over *every* line containing "Measurement state" also collected
`eecad59db…`; that token belongs to the round-31 block at line 907, not to the round-35 line —
corrected after `ExecAncestry` re-measured the same bytes. My own re-run confirms 4 tokens at
`0aee0ef:1271`, 5 at `cc692008:1271`.)

So a `[0-9a-f]{40}` matcher reads zero hashes on a semantically correct line, and "any 40-hex on the
line" picks the wrong commit (line 1271's neighbours in other blocks include
`9f9848816503aa0cd566fc2efdc5e69ea501a253`, the round-33 wave-1 integration commit, which
`merge-base --is-ancestor` accepts silently). The rule should therefore **require the round-36 line
to carry the full 40-hex** and not resolve abbreviations on the pass path: prefix resolution lets a
truncated citation pass, which re-introduces the closure-order class this round is closing. Keep a
resolver as a diagnostic only, asserting `--disambiguate` == 1 candidate. For the same reason E1
should not use the claim's literal `grep -oE '[0-9a-f]{40}'` on `SCORECARD.md`: 8 of its 9 failures
are the first 40 characters of 64-hex sha256 digests (`ExecAncestry` §6, measured independently).

Two further obligations follow from the same bytes, measured across the three refs (label line + its
wrapped continuation, maximal-run filter, first 40-hex):

| ref | placeholder-bearing label slot | 40-hex at the r35 label | 40-hex at the r34 label |
|---|---|---|---|
| `3266c993` | **1** — the round-34 slot (`:1240`) | n/a (no such section) | **none** (placeholder prose) |
| `0aee0ef` | **1** — the round-35 slot (`:1271`) | **none** (placeholder prose) | `c1c6a5f826d2425446347173de527c42991b78b0` |
| `cc692008` | **0** | `0aee0ef…` (abbreviation) | `c1c6a5f8…` |

1. **The placeholder counter must be bound to a named slot.** It reads 1 on both base and the judged
   head — from a *different* line each time (round-34 slot then round-35 slot). A count-only assertion
   passes or fails for the wrong reason; E1 must name the round-36 label it reads.
2. **Existence must be its own limb.** The ancestry limb is not what makes E1 red on base: the base's
   filled labels yield `7963976e60b2564860553c6ab4838128d5ca06ea`, which exists and is an ancestor.
   Red comes from the placeholder limb *and* from the round-36 label line being absent. So E1 needs
   "the round-36 `Final lane commit` label exists and yields a 40-hex", with absence = failure.

Selection is therefore load-bearing, not cosmetic: a bare `head -1` over all label lines picks
`7963976e…` and **passes on the base export**, and the label hash is wrapped onto the next line at
`:1129-1130`, so the extractor must join the label with its continuation and select the round-36
occurrence explicitly. (Same conclusion as `ExecAncestry` §7, reached from the ancestry side.)

## 10. E1–E9 state at each ref (grounds the selection, and predicts the suite's two controls)

Measured on exports, not the worktree: `E2` = `grep -cF 'round-34 depth:density row'`; `E3` = exact
basenames; `E4` = r35 results tracked + r35 provenance note; `E5` = `claims-erratum-d5.md`; `E6` =
`Correction (round 35)`; `E7` = `supersedes R22`/`R23`; `E8` = round-36 lesson with the false-line
correction; `E9` = porcelain + scratch.

| E | what it reads | `3266c993` (r35 base) | `0aee0ef` (r35 judged) | base `cc692008` |
|---|---|---|---|---|
| E1 | placeholder tokens 0 + Final-lane-commit hash resolves & is an ancestor | red (`filled by the L1`=1 at `:1240`, round-34 section; no `## Round 35` heading exists yet, so E1 must assert the section exists) | **red** (`:1271`) | literal limb green (0/0); hash limb **needs r36 line** |
| E2 | round-34 depth:density erratum row | red | green (1) | **green** (1) |
| E3 | SKILL rows, exact basenames `r35-defect-closure.sh` **and** `r36-closure.sh` | red (0/0) | red (0/0) | **red** (0/0) |
| E4 | r35 `wave1-results.json` tracked + provenance note | red (absent) | red (absent) | tracked 1, provenance **0** → **red** |
| E5 | `claims-erratum-d5.md` present | red | green (present) | **green** (13,086 B) |
| E6 | `Correction (round 35)` in L1Integration | red | green (1) | **green** (1) |
| E7 | QUALITY `supersedes R22` / `R23` | red (0/0) | green (1/1) | **green** (1/1) |
| E8 | false-evidence-line correction in the round-36 lesson | red | red (no r36 lesson) | **red** (no r36 lesson) |
| E9 | porcelain empty + no `kasegi-r36` seat dir | red (9 dirty at filing) | red | filing-time only |

At the judged head this reads **4/9 closed** (`E2,E5,E6,E7`), matching C1's required `<9/9`; at
`3266c993` it reads **0/9**, matching `closed=0/9 exit=1`. The E-checks are not decorative: four of
them (E2, E5, E6, E7) are the append-class corrections and are already green at base, so a round-36
suite that prints 9/9 at base would be measuring nothing. E1, E3, E4 and E8 carry the work.

## 11. Verification performed / not performed, scratch, tooling

Performed: one `git archive` export per ref (`cc692008`, `0aee0ef`, `3266c993`) into scratch; the
committed `r35-defect-closure.sh` run three ways (`--export-ref` argument, `--root` on a pure export,
`--root` on the r35 base export, plain at lane HEAD); clause-level greps on `SCORECARD.md`, `SKILL.md`,
`QUALITY.md`, `L1Integration.md`, `corpus/lessons/round-35.md`, `wave1-results.json*`; `git
diff --numstat` / `git log -S` / `cat-file` / `ls-tree` / `ls-files` / `merge-base` reads; two scratch
mutants of `SCORECARD.md` (respelling; negation-mention); blob and sha256 binding of the five base
objects; one scratch copy of `SCORECARD.md` for the section-scoping differential.

Not performed, deliberately: no build/lint/test gate (the parent owns post-integration verification);
no lane, fleet or sibling-lane write; no mutating git command; no pacman; no tool install (nothing
needed — nothing to record under the operator's tooling directive); no subagent dispatch; no edit to
`.ufo/waves/round-36/claims.json`.

Scratch: `/fast/scratch/hyaku/kasegi-r36/ExecDatawalk/` held `base/`, `judged/`, `r35base/` (exports),
`r35base-run.txt`, `base-run.txt` (suite transcripts), `d1probe*.md`, `probe-respell.md`. The directory
is removed after this receipt was copied into the wave dir, leaving no `ExecDatawalk` residue under
`/fast/scratch/hyaku/kasegi-r36/`.

## Report

Six routed defects, walked on base bytes with the exact command and output for each:

1. **Open.** The suite has no export mode — `--export-ref` exits 2 (`unknown argument`), the only
   `git archive` in the file is header prose, and `check_d4` is an index read, so the all-fixed export
   scores `closed=6/7 exit=1` and the plain run names no head.
2. **Open at claim level, partially satisfied in fact.** The late head `5a253372` was exported and run
   by a seat, but that export reads 6/7; the green 7/7 is a clone reading. At `0aee0ef` six
   claim-bearing paths are absent; at base they are present and the capture digest is bound.
3. **Open.** File-wide literal: 0 at base, 1 at the judged head inside the round-35 section; a
   respelled placeholder reads 0 both file-wide and section-scoped, a true negation reads 1; base has
   two identically-worded `## Round 35` headings, so naive section scoping truncates at 22 of 142 lines.
4. **Open.** D6 rewrote the committed round-34 bullet in place (`6 3`), and `check_d6`'s `stale=0`
   clause forbids the append-only form the frozen `after` asked for.
5. **Open.** Both false lines were removed/reconciled by `980aa3d` with no correction note; the Gate
   sentence reads 0 at base, the No-harm row now asserts numbers true only after `5a25337`; no
   lesson/QUALITY row cites the spot-check.
6. **Open by construction.** 9 dirty paths at r35 filing, 6 after `48e6053`; 9 untracked round-36
   paths and 40 scratch seat dirs at this read. Only a filing-time read can judge it.

Two findings beyond the six, both actionable for C1: `check_d3`'s fragment `r-defect-closure` is
satisfied by the **round-33** registry row, so `r35-defect-closure.sh` was never registered (exact
basenames 0/0 — E3 is red at base); and E4 as frozen needs a **round-35** provenance note that
does not exist at base (`git ls-files | grep provenance` lists only round-34's plus fixtures), so round 36
must land it. E1's hash limb must also require the round-36 line to carry the full 40-hex: the
round-35 line carries none (four or five ellipsis abbreviations only), so the literal matcher reads
zero hashes on a correct line.

E-state at the two controls — 0/9 at `3266c993`, 4/9 at `0aee0ef` — matches C1's required
`closed=0/9` / `<9/9`; E2/E5/E6/E7 are already green at base, so the live work is E1, E3, E4, E8.
