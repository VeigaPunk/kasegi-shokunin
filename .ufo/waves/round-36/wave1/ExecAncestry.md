# ExecAncestry — E1 ancestry limb (round 36)

Seat: `ExecAncestry` (executor, leaf). Judged axis: `depth:verifiability`. Milestone: round-36.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only use; **no lane file written**).
Read at 2026-10-26, quiescent tree (`git diff master -- SCORECARD.md` empty).

## 1. Scope and method

Assigned item: verify the E1 ancestry requirement — for each 40-hex token appearing in `SCORECARD.md`
"Final lane commit:" paragraphs, `git cat-file -e <h>` must pass and `git merge-base --is-ancestor <h>
master` must pass; report the branch tip and `git rev-parse master`.

Method (all read-only git: `rev-parse`, `cat-file`, `merge-base`, `log`, `status`, `diff`):

1. tokenise with **maximal hex runs** and classify by run length — 40 = git object id, 64 = sha256
   digest, 7–39 = abbreviation;
2. for every 40-hex run: `git cat-file -e`, then `git cat-file -t`, then `merge-base --is-ancestor <h> master`;
3. flag every paragraph (blank-line-delimited block) containing `final lane commit` case-insensitively,
   so paragraph membership is measured, not guessed;
4. run three discrimination controls (self, exists-but-not-ancestor, missing) so the two limbs are
   shown to be able to fail;
5. also run the claim's literal command (`grep -oE '[0-9a-f]{40}' SCORECARD.md`) and diff its population
   against (1), because that literal is what a closure check would otherwise implement.

Byte binding: `SCORECARD.md` blob at master `a1e366fc56a7e3a986d803d58eef374932e62439`,
sha256 `ed6e931f795c070eda0b996654fd5c1cf7d9b118432e1ee7fee49173946fcd94`, 1404 lines.
`git rev-parse master:.ufo/waves/round-36/claims.json` = `d91f49699eb8e9bbab28a19546e8b083d75f2e74`
(sha256 `a6405e710b242f97361437158536839401c92ea6edb9c65eeab14de0b9e54785`).

## 2. Refs — branch tip and master

```
$ git rev-parse master
b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6
$ git rev-parse origin/master
b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6
$ git rev-parse HEAD
b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6
$ git rev-parse --abbrev-ref HEAD
HEAD                      # detached: no local branch is checked out
$ git symbolic-ref -q HEAD
(empty)                   # detached
```

Findings: there is **no checked-out branch**; the lane is a detached worktree at the claims-freeze
commit `b47f2cdf…`, and `master` / `origin/master` / `HEAD` are the same commit. The only local branch
is `master`. So "current branch tip" = `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` and
`rev-parse master` prints the same value. Round-36 base `cc692008…` and the round-35 head
`0aee0ef105395a2f1d6ace7eaeef13871bb26988` both exist and are ancestors of `master` (measured, §5).

## 3. Table A — every 40-hex token in SCORECARD.md (23 unique, 33 occurrences)

`cat-file -e` = object present in the lane object DB; `ancestor` = `merge-base --is-ancestor <h> master`
exit 0. "Final para" = token occurs inside a paragraph containing "final lane commit".

| # | token | occ | lines | final para | `cat-file -e` | type | ancestor of master |
|---|---|---|---|---|---|---|---|
| 1 | `4b2e30231c20d3374a39976df5a0f998a6c6f90c` | 2 | 210,281 | no | yes | commit | yes |
| 2 | `d43e63c8872c4029c7edb9067d8f272642e7885a` | 3 | 211,243,282 | no | yes | commit | yes |
| 3 | `922a4dde90b60b465e2b8b241d1fe363f1f27e98` | 2 | 369,401 | no | yes | commit | yes |
| 4 | `1fafde8f11454f3b0b98ab7f2b2e640aaf7f399a` | 1 | 402 | no | yes | commit | yes |
| 5 | `d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a` | 1 | 467 | no | yes | commit | yes |
| 6 | `1b076fa7f2fb5e7dd9d87449514eba526043421b` | 1 | 570 | no | yes | commit | yes |
| 7 | `c9f8b115a098c65356e4b3b6048af45a37ab8395` | 1 | 612 | no | yes | commit | yes |
| 8 | `94f387cbeb71a532a51ce075f01701a557231e85` | 1 | 613 | no | **NO** | **absent** | **NO** |
| 9 | `b374febbb33ccadade78a787279707fd5d2e6e1d` | 1 | 858 | no | yes | commit | yes |
| 10 | `fd29aac0dd02f4c6783a0df8c4ba8d0e86414242` | 1 | 958 | no | yes | commit | yes |
| 11 | `022b755008777ee143b566cce3cfd0914c9846c0` | 1 | 962 | no | yes | commit | yes |
| 12 | `43c364d06ccf5a3d1029c0f7816c8e50b509365b` | 1 | 980 | no | yes | commit | yes |
| 13 | `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4` | 1 | 985 | **yes** | yes | commit | yes |
| 14 | `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0` | 1 | 986 | **yes** | yes | commit | yes |
| 15 | `9f9848816503aa0cd566fc2efdc5e69ea501a253` | 1 | 987 | **yes** | yes | commit | yes |
| 16 | `7963976e60b2564860553c6ab4838128d5ca06ea` | 3 | 988,1110,1117 | **yes** | yes | commit | yes |
| 17 | `014ee2d7aa8c3c095ff57ae51097606a9906228c` | 2 | 1117,1124 | **yes** | yes | commit | yes |
| 18 | `29f606dbdd28aff6fd4573ab4b90788bbb90af13` | 1 | 1125 | **yes** | yes | commit | yes |
| 19 | `206e5108f1190e61b3e2622d21cab8a5d921650c` | 1 | 1125 | **yes** | yes | commit | yes |
| 20 | `c1c6a5f826d2425446347173de527c42991b78b0` | 3 | 1130,1241,1259 | **yes** | yes | commit | yes |
| 21 | `3266c9937b03062d9bbc2f436e20820115ed179c` | 2 | 1251,1288 | no | yes | commit | yes |
| 22 | `617496b9c6e92bc671e7e78b83df69a04470d0e9` | 1 | 1289 | no | yes | commit | yes |
| 23 | `da2d3c687f82a9814ee71c91c930cb733050d37c` | 1 | 1290 | no | yes | commit | yes |

Result: **22/23 exist and are ancestors of `master`; 1 fails both limbs** (row 8, §6 F1). No token is
itself the tip (`master` appears in no citation). Under the E1 scope proper — the final-para set (rows
13–20) — the result is **8/8 exist and 8/8 are ancestors**, i.e. E1's ancestry clause passes on the
current bytes.

## 4. Table B — paragraphs containing "final lane commit" (7 blocks; 4 carry a hash)

| lines | label form | 40-hex token(s) in the block | the "Final lane commit" hash | exists | ancestor |
|---|---|---|---|---|---|
| 731–736 | prose: "At the final lane commit, the corrected `anchorcheck.py` digest …" | none | none (no hash cited) | n/a | n/a |
| 776–782 | prose: "At the final lane commit, all frozen counters re-run clean" | none | none (no hash cited) | n/a | n/a |
| 984–997 | `**Final lane commit: `7963976e…`**` (round 33) | `690b69da…`, `6e55c8d5…`, `9f984881…`, `7963976e…` | `7963976e60b2564860553c6ab4838128d5ca06ea` | yes | yes |
| 1110–1114 | `**Round-33 final lane commit: `7963976e…`**` | `7963976e…` | same as above (restated) | yes | yes |
| 1123–1140 | `**Final lane commit: `c1c6a5f8…`**` (round 34) | `014ee2d7…`, `29f606db…`, `206e5108…`, `c1c6a5f8…` | `c1c6a5f826d2425446347173de527c42991b78b0` | yes | yes |
| 1241–1244 | `**Round-34 final lane commit: `c1c6a5f8…`**` | `c1c6a5f8…` | same as above (restated) | yes | yes |
| 1271 | round-35 measurement state: "… integration `aa6ad99…`; final lane commit `0aee0ef…`" | **none** — abbreviation only | `0aee0ef…` → resolves uniquely to `0aee0ef105395a2f1d6ace7eaeef13871bb26988` | yes | yes |

Abbreviations inside these blocks all resolve uniquely and to ancestors of `master`:
`53bfa59f` → `53bfa59ff3fa578818e7e5db04fe60e80ed1eb6f`; `9f98488` → `9f984881…`; `3266c993` →
`3266c993…`; `617496b9` → `617496b9…`; `da2d3c68` → `da2d3c68…`; `aa6ad99` →
`aa6ad99bb90c4fe30dc5c326adf2f82d8ec84b1b`; `0aee0ef` → `0aee0ef105395a2f1d6ace7eaeef13871bb26988`
(`git rev-parse --disambiguate` returns exactly one candidate for each).

There is **no `## Round 36` heading** in `SCORECARD.md` at this read (`grep -c '^## Round 36'` = 0), so
the round-36 "Final lane commit:" line does not exist yet; it is introduced by the closing commit.

## 5. Controls — the two limbs can fail, and they discriminate

| control | hash | `cat-file -e` | `merge-base --is-ancestor <h> master` | expectation met |
|---|---|---|---|---|
| self | `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (= master) | yes | rc 0 (a commit is its own ancestor) | yes |
| positive | `7963976e60b2564860553c6ab4838128d5ca06ea` (round-33 final) | yes | rc 0 | yes |
| **negative** | `00a85af0df169fcdad7ff709c1aa6aca5e31ea40` (jj-kept commit, off `master`) | yes (`cat-file -t` = commit) | **rc 1 — not an ancestor** | yes |
| missing | `0123456789abcdef0123456789abcdef01234567` | **rc 1** | not run | yes |

Nearby lane heads, all exist + ancestor of `master`: round-36 base `cc692008b0cfd58d18275aa6c4aed79620120799`,
claims-freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`, round-35 base
`3266c9937b03062d9bbc2f436e20820115ed179c`, round-35 integration
`aa6ad99bb90c4fe30dc5c326adf2f82d8ec84b1b`, round-35 judged head
`0aee0ef105395a2f1d6ace7eaeef13871bb26988`.

## 6. F1 — a real, reproducible E1 hazard: the claim's literal grep is unsound

The frozen claim names the command `grep -oE '[0-9a-f]{40}' SCORECARD.md`. Run literally on the current
bytes it yields **31 unique tokens, 9 of which fail `cat-file -e`**:

```
$ grep -oE '[0-9a-f]{40}' SCORECARD.md | sort -u | wc -l
31
naive_fail=9
```

All nine, reproduced:

```
125be37d85ffe6be30a3c372b52d96d8074e3c4d
3fc0d751f2a5819879d440f8ef62b607376a8b69
5d4842da6103f17c7798ca2078a77288820bd8b9
94f387cbeb71a532a51ce075f01701a557231e85
95333e29ee5acce549f8e0b6328c6dcab3c542cf
c2a9e6c6088015968b3c6ea7f12a0ea66699c3ec
d91889e5f7d77c3695c366521c348569b4f29269
fa09d5b835451f2443fc96353432a330608baf5f
fe0dae8957c38f9c697b1b851a528bdf516f949f
```

Cause, measured by run length:

- **8 of the 9 are the first 40 characters of a 64-hex sha256 digest**, not git ids:
  `95333e29…4514` (line 620), `c2a9e6c6…f748` (640), `fa09d5b8…4f2d` and `125be37d…cca6` (642),
  `d91889e5…250d` (839), `3fc0d751…d4e1` (843), `5d4842da…7f09` (953), `fe0dae89…2982` (1287).
  These are instrument / file / claims digests. They can never satisfy `cat-file -e`; a closure check
  built on the literal grep reports them as false "missing" tokens even when every citation is honest.
- **1 of the 9 is a genuine citation defect (F1)** — see below.

Sound tokenisation, measured equal to the maximal-run classification in §3:

```
$ grep -oE '[0-9a-f]{40,}' SCORECARD.md | awk 'length($0)==40' | sort -u | wc -l
23                       # exists-fail: 1 (F1 only);  ancestor-fail: 0
```

### F1 (defect, line 613): dropped hex digit in the round-28 dispatch-commit citation

`SCORECARD.md:613` cites the round-28 wave-1 dispatch commit as
`94f387cbeb71a532a51ce075f01701a557231e85` — **no such object** (`cat-file -e` rc 1). The real commit,
cited correctly in ~40 round-28 receipts, is one character longer in the `…cbee71…` position:

```
$ git cat-file -t 94f387cbee71a532a51ce075f01701a557231e85   # receipts' spelling
commit
$ git log -1 --format='%H %cI %s' 94f387cbee71a532a51ce075f01701a557231e85
94f387cbee71a532a51ce075f01701a557231e85 2026-10-25T14:09:46-03:00 round-28: wave1 spec + dispatch (69 seats, v2 policy, m_flash 50.7%, attack 31.9%)
$ git merge-base --is-ancestor 94f387cbee71a532a51ce075f01701a557231e85 master   # rc 0
```

The two strings differ by exactly one inserted `e` (`94f387cb**e**e71…` vs `94f387cbeb71…`); both are
40 chars, so the corruption is invisible to a length check. Blast radius measured by grep: the corrupted
spelling occurs in exactly **two** files — `SCORECARD.md:613` and
`.ufo/waves/round-28/wave1/ScribeScorecard.md:5` — while the correct `94f387cbee71…` occurs **39 times
across 35 files** under `.ufo/waves/round-28/`. So the receipts are the authoritative spelling and the
scorecard line is the outlier; the typo most likely originated in `ScribeScorecard.md:5` and was copied
into the scorecard.

Consequence for E1: with the E1 scope narrowed to the final-lane-commit paragraphs, F1 does not fire
(it is a round-28 preamble citation). With the whole-file reading implied by the claim's literal grep,
E1 is **red on the current bytes** before any round-36 work lands — through F1 plus 8 tokenizer
artefacts. Either the check's tokeniser is fixed and F1 is corrected in the scorecard (or F1 is
declared as a known-exempt citation by id), or E1 must be scoped to the label rather than the file.

## 7. Recommended E1 ancestry limb (exact, minimal, testable)

Tested on the current bytes (this exact function was run; output below is measured, not sketched):

```
# $1 = 1-based line number of a line carrying the label.
# The hash may sit on that line or at the head of the next one (round-33/34 split layout),
# so the line is cut at the label and the next line is appended before extraction.
pick() {
  { sed -n "${1}p" SCORECARD.md | sed "s/.*[Ff]inal lane commit[^:]*://"
    sed -n "$(( $1 + 1 ))p" SCORECARD.md
  } | grep -oE '[0-9a-f]{40,}' | awk 'length($0)==40' | head -1
}

# E1: one target line (the round-36 one) -- and the same three limbs on every older label line.
H=$(pick "$ROUND36_LABEL_LINE")
test -n "$H"                              || fail "no 40-hex hash on the Final lane commit line"
git cat-file -e "$H"                      || fail "Final lane commit hash absent: $H"
git merge-base --is-ancestor "$H" master  || fail "Final lane commit hash is not an ancestor: $H"
```

Measured output of `pick` on every label line in the current file
(`grep -niE 'final lane commit' SCORECARD.md | cut -d: -f1` → 731 776 987 1110 1129 1241 1271):

```
line 731   H=(none 40-hex)      # prose: "At the final lane commit, ..."
line 776   H=(none 40-hex)      # prose
line 987   H=7963976e60b2564860553c6ab4838128d5ca06ea exists=exists ancestor=yes
line 1110  H=7963976e60b2564860553c6ab4838128d5ca06ea exists=exists ancestor=yes
line 1129  H=c1c6a5f826d2425446347173de527c42991b78b0 exists=exists ancestor=yes
line 1241  H=c1c6a5f826d2425446347173de527c42991b78b0 exists=exists ancestor=yes
line 1271  H=(none 40-hex)      # round-35 line cites only the abbreviation `0aee0ef…`
```

That reproduces §4 cell-for-cell. Two traps this form avoids, both of which a simpler form falls into:
`grep -iE 'final lane commit' SCORECARD.md | grep -oE '[0-9a-f]{40,}' | awk 'length($0)==40' | head -1`
returns **`9f9848816503aa0cd566fc2efdc5e69ea501a253`** — the round-33 *wave-1 integration* commit that
sits earlier on the same line as the label — instead of the `Final lane commit` hash; and a line-scoped
extraction returns *nothing* for lines 987 and 1129, because there the hash begins the following line.
`merge-base --is-ancestor` alone would have accepted `9f984881…` silently: it is an ancestor too.

**Regression behaviour, measured on the two exports the frozen C1 requires the suite to reject.**
`pick` at the round-35 base `3266c993…`: lines 987/1110 → `7963976e…` (exists, ancestor), lines
1129/1240 → **no 40-hex**, and those two are *different placeholder forms at the same revision*: the
preamble label (`:1129-1130`) carries placeholder **prose** while the bold restatement (`:1240`) carries
the **literal** the frozen kill rule names. File-wide literal count there is **1**, so a checker that
repairs only the literal slot and re-reads 0 leaves the preamble slot vacant and reports closed — the
arithmetic that makes a slot-bound counter necessary rather than merely tidy. The file also carries
**no `## Round 35` and no `## Round 36` heading** (last heading is round 34 at 1121; 1243 lines). At the
judged head `0aee0ef…`: 1129/1241 → `c1c6a5f8…`, 1271 → **no 40-hex** (the round-35 D1 clause; literal
count 1), one round-35 heading, no round-36 heading (1282 lines). At the round-36 base `cc692008…` both
labels are filled (`:1130` = `c1c6a5f8…`, `:1241` = same, restated at `:1259`) and the literal count is
**0**. So the label-anchored form is red on both regression targets and green on master — but it is red
only because the *unfilled* slot yields no hash. Three obligations follow for E1: (i) select the
**round-36** label line explicitly, never `head -1` over all label lines — a bare `head -1` picks
`7963976e…`, which exists and is an ancestor, and would therefore pass on the base export; (ii) treat a
missing round-36 label line as a **failure**, not a vacuous pass; (iii) bind each counter to a **named
slot** (preamble label vs bold restatement), never file-wide — on `3266c993` the file-wide literal count
of 1 is satisfied by the restatement while the preamble label is still vacant. A block-scoped extractor
is worse than vacuous on the base: with zero round-35/round-36 headings it returns an empty document and
is green by absence.

Four properties this buys that the literal grep does not: (a) it cannot match a sha256 prefix,
because it filters on maximal-run length; (b) it requires the hash to sit at or after the label (plus
the wrapped line), so a stray hash elsewhere cannot satisfy it; (c) it is anchored on the label, so the
round-36 line is the target and older blocks are the invariant check; (d) `merge-base --is-ancestor` is evaluated against
the *lane head*, so a hash from another repository (or an abbreviation that a future fetch resolves
differently) cannot pass. If the intent is to census **all** final-lane-commit blocks (Table B), the
sound form is `grep -oE '[0-9a-f]{40,}' | awk 'length($0)==40'` over the block plus the same two git
limbs, with the two prose blocks (731–736, 776–782) and the abbreviation-only block (1271) excluded by
construction or by name — otherwise the clause is vacuously satisfied there.

## 8. Risks and preconditions for the L1 (measured, not repaired — no lane write permitted)

1. **E1 must not use `grep -oE '[0-9a-f]{40}'` as written in the claim** (§6): 9 false failures on
   current bytes, 8 of them structurally unavoidable. This is the single highest-value correction to
   land before the closure check is written.
2. **F1 is a live citation defect** (`SCORECARD.md:613`, plus its source copy at
   `.ufo/waves/round-28/wave1/ScribeScorecard.md:5`). Correcting it changes a scorecard line in an
   already-closed round, so it wants a disclosed correction line, not a silent edit; alternatively E1
   declares it exempt by id, which is weaker. Not mine to land.
3. **The round-35 final-lane-commit line (1271) is abbreviation-only** (`0aee0ef…`). It resolves and is
   an ancestor, but a 40-hex census cannot bind it. If E1 is to cover round 35, that line needs a full
   40-hex hash; as it stands the round-36 line is the only one E1 can test going forward, and it must
   therefore be written with a **full 40-hex** token. Measured: line 1271 is byte-identical at base
   `cc692008…` and at master (`sha256 9d563c19517eac572d253b8e7390d6742ba3dacdeda89bea754fb8884b20129c`)
   and carries **0 full 40-hex tokens** — only `3266c993…`, `617496b9…`, `da2d3c68…`, `aa6ad99…`,
   `0aee0ef…`, each resolving uniquely (`--disambiguate` → 1 candidate) to an ancestor of `master`.
   Heading shape also differs by revision: `^## Round 35` occurs **twice** at base `cc692008…`
   (lines 1263, 1284) and at master, but **once** at the judged head `0aee0ef…` (line 1263) — so an E1
   extractor keyed to a heading ordinal truncates the receipt-grounded block on the judged head and
   lands on the thin stub on both. Anchor E1 on the label itself (§7 `pick`), not on heading ordinals.
   Measured delta on that same line across revisions: at the judged head `0aee0ef…` line 1271 carries
   **4** abbreviations and 0 full 40-hex, because its final-lane-commit slot still holds the round-35 D1
   placeholder prose (the live-broken C1 clause that section discloses; placeholder-bearing lines: 1 at
   the judged head, 0 at base, 0 at master) — the byte identity above is base↔master only, and the
   repair that inserted `0aee0ef…` is exactly the delta. Section spans: an all-blocks `^## Round 35`
   extraction is **140** lines at base and at master but **19** at the judged head; the naive range
   `sed -n '/^## Round 35/,/^## /p'` gives **22** at base (dropping the receipt-grounded block) and
   **20** at the judged head, where it is complete only because a single heading exists. An E1
   implementation that selects text by heading therefore reads a different document on each of the
   three revisions it has to certify.
4. **Ancestry is only as strong as the ref.** All checks above are against `master`
   (`b47f2cdf…` = tip = `HEAD`, detached). At closure, the closing commit extends `master`, so every
   hash that is an ancestor now stays an ancestor; a check run against a scratch clone that lacks the
   lane's refs would report `cat-file -e` failures for genres the export does not carry — the same class
   of trap `ExecNoHarmFinal` F6 recorded for the instruments (`BASE-ABSENT` on a copied tree).
5. **Quiescence (E9) is not yet satisfiable and is not mine to fix.** `git status --porcelain` at this
   read returns 9 entries, all untracked round-36 wave scaffolding, with no tracked file modified:

   ```
   ?? .ufo/waves/round-36/build-spec.py
   ?? .ufo/waves/round-36/wave1-dispatch.json
   ?? .ufo/waves/round-36/wave1-plan.err
   ?? .ufo/waves/round-36/wave1-plan.out
   ?? .ufo/waves/round-36/wave1-run.err
   ?? .ufo/waves/round-36/wave1-spec.json
   ?? .ufo/waves/round-36/wave1.ready
   ?? .ufo/waves/round-36/wave1.ready.dispatched
   ?? .ufo/waves/round-36/wave1/
   ```

   The closing commit must absorb these (or the gate must run after they are committed) for E9's
   `git status --porcelain` limb to read empty.

## 9. Verification performed / not performed

Performed: 23-token existence + ancestry census; 7-block final-lane-commit paragraph census; 7
abbreviation resolutions; 4 discrimination controls; naive-vs-sound tokenizer differential (31 vs 23
unique, 9 vs 1 failure); F1 root-cause and blast radius; byte binding of `SCORECARD.md` and
`claims.json`; `rev-parse` of `master`, `HEAD`, `origin/master`; `status --porcelain`.

Not performed, and deliberately so: no build/lint/test/suite run (parent owns the gate); no write of any
kind inside the lane repo; no mutating git command; no pacman; no tool install (nothing was needed, so
no tool/version/channel to record); no subagent dispatch.

Evidence: scratch workdir `/fast/scratch/hyaku/kasegi-r36/ExecAncestry/` held `ancestry.py` (the naive
tokenizer, retained only as the differential control), `ancestry2.py`
(sha256 `7362af44c33061d2abc3d3ba7b2416a0057b5ef1e7443176e49fabca19d7d311`), `table-v2.md`
(sha256 `858f382deb690cffaea1ad3844b6bc84380e692a26384ce0d48956695aab8a4d`, reproduced in §3/§4) and
`ancestry-v2.json`; the directory is removed after this receipt was copied here, leaving no
`/fast/scratch/hyaku/kasegi-r36/ExecAncestry/` residue.
