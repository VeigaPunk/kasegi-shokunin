# R39 C1 design falsification — discriminating checklist for `corpus/instruments/r39-closure.sh`

Seat `CritDesignReview` (critic, leaf). Target: the frozen C1 spec (`.ufo/waves/round-39/claims.json` @ `dcd3170`,
G1–G8) and the build contract handed to `ExecSuiteBuild`. This is a design review before/independent of the landed
suite: for every check it names a minimal synthetic state that should be RED but a naive limb accepts, a state that
should be GREEN but a naive/strict limb rejects, and the requirements the implementation MUST carry so that the
selftest mutant set and the wave-2 attack have something to bite. "MUST" = the claim's own kill-rule strength.
Raw evidence (commands, fixtures, outputs) is in the seat receipt `CritDesignReview.md`, not here.

Axes: depth:verifiability (the claim's axis; every requirement below is a fail-closed gate over exported bytes).
No score move is asserted. Nothing here edits the frozen claim; P0 items are decisions the L1 must take in an
erratum or in the landing sequence.

## P0 — claim-level blockers (no suite change closes these)

### P0.1 The green export is the receipt-carrying tip, not J

The frozen command is `r39-closure.sh --export-ref <J> -> closed=8/8 exit=0`, and the frozen head rule says J
"carries every round-39 change **except** that receipt; the lane tip Y adds only the receipt file". G2 requires
the receipt *in the export*. Therefore the J export has no receipt, G2 is `receipt=0`, and the command cannot
print 8/8 — by construction. This is the round-38 verifier R1 class, and the r38 receipt itself records the
failure mode on its own bytes (`export-ref-run: G2 ... closed=0`; `export-ref-run: closed=7/8 exit=1`). The r39
head rule is byte-identical to the r38 head rule after round-number substitution (measured), so the recurrence
is not an accident of wording.

Consequence: the correct green command is `--export-ref <Y>` where Y is the receipt-carrying tip (HEAD == Y,
clean tree). The receipt inside Y names `export-ref=J`. The J export remains a documented red (G2, and G8 when
HEAD != REF) and that red run belongs in the receipt as prefixed lines, exactly as r38's `export-ref-run:` block
did.

Required correction (L1, erratum or report wording): say "the judged head J is named by the receipt; the export
that must print `closed=8/8 exit=0` is the receipt-carrying tip Y (HEAD == Y)". Amending the frozen command
string itself is out of this seat's scope; leaving it unamended makes C1 fail its own kill rule no matter how
good the suite is. The same substitution applies to `--selftest --export-ref <J>`: at J the G2 and G8 positives
are red by construction, so `selftest cases=8 failures=0` is only reachable at Y.

### P0.2 G8 couples to the live lane HEAD

The pinned r37 suite's E9 compares the lane repos HEAD with the run ref (`head-match`), and requires a clean
worktree and an empty `kasegi-r37` scratch prefix. Running the r39 suite over J while HEAD is Y makes G8 red
for a reason that has nothing to do with the bytes. The G8 green limb is only meaningful on the tip (HEAD ==
REF == Y). Do not "fix" this by passing `--scratch-root` or patching the pinned bytes; pin the bytes and run on
the tip.

### P0.3 Commit-graph shape that satisfies G2 + G3 together

All of these must be in J (the code head), because Y may add **only** the receipt path:

- `corpus/instruments/r39-closure.sh`, `.ufo/waves/round-39/declared-blocks.txt` (generated from the worktree
  before the commit; it describes J's tails), the frontier/knowledge/registry/ledger/SCORECARD/SHONEN/LOG/
  lesson/QUALITY appends, the wave-1 dispatch **and** its results file, and the red-run transcripts over the
  base and the r38 head (runs that do not depend on J).
- In Y: `all-gates.txt` only. A separate `reds.txt`, a transcript file, or a second receipt committed at Y makes
  `git diff --name-only J Y` list more than the receipt and turns G2 red. Embed run output as prefixed lines
  inside the receipt (r38's `reds.txt` was committed at J, not at Y — that is why its diff stayed clean).
- Bootstrap flow that keeps the receipt genuine: J → Y1 (= J + a field-complete receipt) → run over Y1 (HEAD=Y1,
  clean) → Y2 (= Y1 + the genuine receipt embedding the Y1 run, with a `run-ref=<Y1>` line). `git diff
  --name-only J Y2` is still the receipt path only; Y2 is the tip the scorer re-runs. A single receipt commit
  cannot contain its own run; do not pretend otherwise.
- `results.json` for every committed `*-dispatch.json` must be in J; a dispatch committed at Y is G2-red. The
  same rule kills committing a wave-2 dispatch after J.

### P0.4 Erratum dependencies the suite must not inherit wrongly

- E2 (claims erratum 1): the r38 judged head is the 40-hex `66703acaaff50529a35be49aa8759d04140720ad`. The
  37-char string in the frozen summary and in the build "Prove it" block is unresolvable; a run with it dies in
  `git archive` (exit 128), not with the frozen `closed<8/8 exit=1`. The suite should refuse an unresolvable ref
  with exit 2 and no `closed=` line; the control run must use the 40-hex value.
- The r39 receipt must not cite a mistake row the lesson never minted (M38-8 is exactly that; M39-1 records it).

### P0.5 Landing dependencies in the lane text

- G2/G5 require the exact string `judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt` in
  the SCORECARD `## Round 39…` section **and** in the SHONEN round-39 lines. No seat's item guarantees that
  string for SHONEN; the L1 must land it, or relax the suite to the r38 form (`export-ref of .ufo/.../round-39/
  final-gates/all-gates.txt`) and record the relaxation. A missing phrase is a G2 red at the green ref.
- The SCORECARD `## Round 39` section is L1-authored (no ScribeScorecard seat this round). It must exist exactly
  once and be non-empty; an absent section makes a naive G5 vacuously green.

## G1 — whole-tail declarations, fences, corrections, confinement

| | minimal state | naive limb that gets it wrong |
|---|---|---|
| RED-should-pass | file 90 → 100 lines; declared `PROVINCE.md 2 <sha of tail-2>`; numstat `10 0` | digest-only check: tail-2 matches, green (measured) |
| RED-should-pass | unclosed `~~~` block, or 4-tick opener closed by 3 ticks | backtick-only/exact-3 walk says closed |
| RED-should-pass | `Correction (round 39)` inside a tilde or backtick fence | r38's `g1_correction` counts it (no fence awareness) |
| RED-should-pass | declared `../outside.md 1 <sha>` resolving outside the export | `[ -f "$export/$1" ]` is true |
| RED-should-pass | declared `N` equals added but the added lines are a mid-file insertion | count-only equality |
| GREEN-may-fail | 4-tick opener closed by 4 ticks | exact-3 walk says open (measured) |
| GREEN-may-fail | `~~~` door whose content has one stray ``` line | backtick-only walk says open (the fixture-(d) case) |

MUST:

1. Parse each declaration as exactly three whitespace fields (`path lines sha`), lowercase 64-hex, `lines >= 1`;
   skip blank lines and `#` comments only; any invalid line makes the check RED; exactly one declaration per
   distinct path.
2. Confine the path: relative, no `..`, no leading `/`; `realpath -m "$EXPORT/$p"` is under `realpath -m "$EXPORT"`
   and the target is a regular file (`-f`, not a symlink that resolves outside).
3. Digest is exactly `tail -n "$lines" -- "$p" | sha256sum` under `LC_ALL=C`, field 1 only; no reconstruction.
4. Added count comes from `git -C "$LANE" diff --numstat "$BASE" "$REF" -- "$p"` (fail-closed; a failed read is
   RED, not 0); require `added == lines` **and** `deleted == 0`, or require the diff's `+` lines to equal the
   tail bytes. Using the receipt's export-ref instead of the executing REF lets a tampered export validate
   against the wrong diff.
5. Declarations must cover PROVINCE.md and corpus/README.md (the landed appends are 1 and 28 lines; do not
   hardcode those numbers — derive them).
6. Fence walk over the whole file from line 1: opener `^ {0,3}(`{3,}|~{3,})` plus info (a backtick opener's
   info may not contain a backtick); closer is the same character with length >= the opener and only trailing
   spaces; a closer while closed is an opener; state at EOF must be closed. Count `^Correction (round 39)` only
   where the state is closed at that line. A shared `outside_fence(file, pattern)` helper must also serve G5 and
   the G3 correction paragraphs; otherwise a fenced correction satisfies G5 while being code.
7. The check must be independent of which of the two front doors is declared first, and must not require a
   declaration for an unchanged front door (a zero-line declaration is invalid).

Selftest mutants (>= 2, each must name the reopened limb): partial tail; unclosed `~~~`; 4-tick opener closed by
3; correction inside a fence; `../` path; mid-file insertion; duplicate declaration.

## G2 — graded receipt, head binding, digest

| | minimal state | naive limb that gets it wrong |
|---|---|---|
| RED-should-pass | `selftest case=G1 positive=pass verdict=pass` (no mutants) | item's "both fields pass" rule accepts (measured) |
| RED-should-pass | `mutants=0/0` | field-presence rule accepts (measured) |
| RED-should-pass | `G1 payload= closed=1` | r38 regex `payload=.*` accepts (measured) |
| RED-should-pass | receipt naming `export-ref=REF` (self-name) | "ancestor-or-equal" accepts equality |
| RED-should-pass | receipt read from the lane tip while REF is J | G2 green on a tree that does not contain the receipt |
| GREEN-may-fail | r38-style receipt with prefixed red-run lines (`export-ref-run: …`) | substring counts see 7 `export-ref=` and 20 `closed=`; anchored counts see 1 and 1 (measured) |
| GREEN-may-fail | receipt with a bare `run-ref=<Y1>` line | a parser that treats it as a second ref rejects |

MUST:

1. Exact path in the export; first line exactly `all-gates v3`; exactly one `^all-gates v` line.
2. Exactly one anchored `^export-ref=[0-9a-f]{40}$`; the commit exists in the lane; it is a **strict ancestor** of
   REF (`merge-base --is-ancestor` and `xref != REF`) — equality is only reachable by forgery and is the R1 shape.
3. `git diff --name-only "$xref" "$REF"` fails closed and lists exactly one path, the receipt. Allow nothing else;
   P0.3 says how to keep it true.
4. Exactly one anchored `^suite-sha256=[0-9a-f]{64}$`; it equals sha256 of the executing file **and** of the
   export's `corpus/instruments/r39-closure.sh` (three-way binding; a worktree edit must not produce a receipt
   digest that no commit carries).
5. Exactly eight anchored `^G[1-8] payload=… closed=1$` lines, ids 1–8 once, payload with at least one
   `key=value` and no empty values; zero anchored `G…closed=0`.
6. Exactly one anchored `^closed=8/8 exit=0$`; zero other anchored `^closed=` (red runs must be prefixed).
7. Exactly eight anchored `^selftest case=G1…G8 ` lines, each with `positive=pass`, `verdict=pass`, and
   `mutants=K/N` with `N >= 2` and `K == N`; zero `verdict=fail`; exactly one anchored
   `^selftest cases=8 failures=0$`. The claims' "graded … whose mutants are all rejected" is stronger than the
   item's field-presence rule; implement the claim. Prefer also requiring >= 2 `selftest detail=…mutant=…
   rejected=1` lines per case and no `rejected=0`, so a hand-written case line is not evidence.
8. SCORECARD `^## Round 39([^0-9]|$)` section exactly once and non-empty; SHONEN round-39 lines exist; both
   contain the exact reference phrase; zero case-insensitive `final lane commit` / `final lane head` / hex
   following a final/judged/head label in those scopes.

Selftest mutants: v2 header; export-ref == REF; export-ref not ancestor; extra file in the diff; mutated suite
digest; missing receipt; unprefixed red-run line (two anchored summaries / nine G lines); ninth case line;
summary-only; `verdict=fail`; `mutants=0/0`; empty payload; missing reference phrase; `Final lane commit` in the
section; receipt at J while the run ref is Y.

## G3 — committed-run truth

| | minimal state | naive limb that gets it wrong |
|---|---|---|
| RED-should-pass | `--export-ref deadbeef -> closed=8/8` with no transcript; the word `report-only` on another line | file-wide `grep -q report-only` accepts (measured) |
| RED-should-pass | a quote that names the ref and the count without the literal `--export-ref` (e.g. "at 7dd2fcd the suite printed closed=8/8") | the narrow arrow regex misses it |
| RED-should-pass | pair split across a wrapped paragraph (the R2 corrections do exactly this) | a same-line-only parser misses or mispairs |
| GREEN-may-fail | whole-file scope over SCORECARD/SHONEN/LOG/round-38.md: 17/6/5/2 `closed=` mentions, 3/1/0/0 ref pairs, all pre-existing | whole-file rule red at every honest head (measured) |
| GREEN-may-fail | the R2 correction paragraphs quote the r38 receipt's 7/8 and 8/8 with two refs | round-39-only transcript dir red; the bytes are in the r38 receipt |

MUST:

1. Scope: the added lines of `git -C "$LANE" diff --unified=0 "$BASE" "$REF" -- <file>` for SCORECARD.md,
   SHONEN.md, LOG.md, corpus/lessons/round-38.md **and corpus/lessons/round-39.md** (the lesson is where a round
   overstates most easily and the frozen file list omits it). Fail closed on a failed diff read.
2. Parse per blank-line paragraph, not per line: collect refs (7–40 hex) and counts (`closed=K/K`, optional
   `exit=E`) in segments containing `closed=`; pair each ref with the count in its sentence/paragraph.
3. Coverage per pair: (a) a committed transcript block under `.ufo/waves/round-*/final-gates/` whose run header
   or `run-ref=` names the ref and whose summary names the same count (allow the quoted run's own round
   directory — the r38 receipt is the only honest witness for the r38 numbers); or (b) the paragraph names a
   committed transcript path whose bytes contain the pair; or (c) the paragraph contains a word-bounded,
   case-insensitive `report-only`. Fail closed if the transcript directory is unreadable.
4. The green `closed=8/8` over the receipt-carrying ref may **not** be report-only; it must be backed by the
   receipt's own run block (G2 already binds it).
5. A `report-only` token in another paragraph/file never covers a quote.

Selftest mutants: no transcript and no report-only; report-only on another line; wrong count for the named ref;
green 8/8 labeled report-only; an unreadable transcript dir; a quote added to round-39.md with no witness.

## G4 — seat identity

| | minimal state | naive limb that gets it wrong |
|---|---|---|
| RED-should-pass | N distinct bogus names X/Y/Z against tasks A/B/C | count-only equality (measured) |
| RED-should-pass | zero-task dispatch + empty results | `0 == 0` (r38 code accepts `rtasks >= 0`) |
| RED-should-pass | stale `<wave>-results.json` with the right count | sibling picked without matching `wave` |
| RED-should-pass | top-level `seats: N` int with no `results` list | trust the count field |
| GREEN-may-fail | real r38 shape: `name` unique 73/73; `agent` is the **role**, 9 distinct | keying on `agent` reds (measured) |

MUST:

1. Export-only glob `.ufo/waves/round-39/*-dispatch.json`, at least one; parse `taskCall.tasks` fail-closed.
2. `len(tasks) >= 1`; zero tasks is RED.
3. Results resolution: `<base>-results.json` first, else `<wave>-results.json` with a matching `wave`; two
   candidates that disagree are RED; unparseable/missing is RED. Require the `results` list (not the `seats`
   int); its length equals `len(tasks)`.
4. Identities: use `name` on both sides; accept `id` if present; accept `agent` only when it is unique **and**
   its value set equals the task names. Require distinct names and set equality with the dispatch names, plus a
   non-empty result payload (`output`).
5. Emit a payload with `dispatches= pairs= seats-ok= identity= names-equal=` so a reader sees which limb failed.

Selftest mutants: duplicate names; count-only bogus names; zero-task; missing results; stale wave; seats-only;
one wrong name.

## G5 — label drift

| | minimal state | naive limb that gets it wrong |
|---|---|---|
| RED-should-pass | no `## Round 39` section (the current tree) | `awk` range yields nothing → 0 final-label lines → green (measured) |
| RED-should-pass | `Final lane commit — abc1234` / lowercase / `final lane head: <hex>` | exact-string scan misses |
| RED-should-pass | a hash labeled `judged head: <hex>` in the section | "by reference only" not enforced |
| RED-should-pass | `Correction (round 39)` inside a fence | line-grep counts it (measured) |
| GREEN-may-fail | whole-file final-label scan: 5 old lines in SCORECARD | red on history (measured) |
| GREEN-may-fail | the section quotes red-run hashes legitimately | any-hash-in-section rule reds |

MUST:

1. The `## Round 39…` section exists exactly once (last-match is not enough: duplicated headings must be RED) and
   has a non-empty body; SHONEN round-39 lines exist.
2. Zero `final lane commit` (case-insensitive, any separator) in the section and in the SHONEN round-39 lines;
   zero 7–40-hex token on a line that also carries a final/judged/head label.
3. The exact reference phrase appears in both scopes; the reference is the only head naming (a `--export-ref`
   quote of a red-run hash is allowed and is not a head label).
4. `Correction (round 39)` line naming the round-38 overstatement (`f06148c6` report-only / the J-vs-run-ref
   split), outside a fence (shared helper). File-wide placement is acceptable (the item's wording), section-only
   placement is a stronger rule; pick one and document it.

Selftest mutants: absent section; duplicated section; `Final lane commit: abc1234`; em-dash/lowercase variant;
hash labeled judged head; fenced correction; missing phrase; correction naming the wrong hash.

## G6 — scratch quiescence (live, fail-closed)

| | minimal state | naive limb that gets it wrong |
|---|---|---|
| RED-should-pass | `chmod 000` on `$root/kasegi-r38` | `find … 2>/dev/null | wc -l` = 0 (measured) |
| RED-should-pass | `kasegi-r37` is a symlink or a plain file | `-type d` counts 0 (measured) |
| RED-should-pass | a sibling entry beside the tolerated work chain | top-level tolerance without chain guard |
| GREEN-may-fail | the run's own `--work` is several levels under `kasegi-r39` | exact-path-only tolerance reds |
| GREEN-may-fail | `kasegi-r39-l1` exists at the root | over-broad "any kasegi-r39*" rule reds |

MUST:

1. `root = realpath(--scratch-root)`; `kasegi-r37` and `kasegi-r38` absent or hold zero top-level entries; count
   every entry (`find -mindepth 1 -maxdepth 1 -print`), never `-type d`; an unreadable dir is `read=fail` RED.
2. `kasegi-r39` absent/empty, or tolerate exactly the realpath chain from its top-level ancestor to
   `realpath(--work)` (each level holds exactly one entry, the next component); a sibling is residual; print
   `tolerated=`.
3. `--work` must be outside the lane (refuse before creating anything), resolve its realpath, and be unresolvable
   → RED. Honour TMPDIR only through `mktemp`; clean the export/mut/work on exit.
4. Ignore prefixes that are not the three named ones; print the root so a typo is visible.

Selftest mutants: stray file under `kasegi-r39`; symlink; chmod 000; sibling in the chain; work outside the root
(green); own work chain (green).

## G7 — ledger fill

| | minimal state | naive limb that gets it wrong |
|---|---|---|
| RED-should-pass | rows `| 1x | … |`, `| 3y | … |`, `| 9 | |` | prefix regex + ">=3 rows, 1 and 3" green (measured) |
| RED-should-pass | heading + correction only, zero rows | heading-presence check (M38-5) |
| RED-should-pass | empty status/evidence cells | cell-content-unconstrained count |
| GREEN-may-fail | landed rows are `| 1. Make … | **mined round 39** (criteria; …) | … |` | exact-cell vocabulary reds |
| GREEN-may-fail | the ledger has two numberings (6 and 7 proposals) | checking against the base 6-row table reds |

MUST:

1. Heading `## Round-39 dispositions` (the item's exact form `## Round-39 dispositions (appended 2026-10-26)`),
   exactly one, after the round-38 filled section; body non-empty.
2. `^Correction (round 39)` line inside the section, outside a fence.
3. Data rows only (skip header and separator); first cell matches `^[0-9]+\.`; expected id set = the seven
   `considerthese/2026-10-26.md` proposals (1–7), each exactly once, no extras (derive from the source and cite
   it, or hardcode 1–7 with the source in a comment); status cell contains a word-bounded closed-vocabulary word
   (`mined|landed|carried|open|rejected|deferred|partially|resolved|unchanged`); evidence cell is non-empty, not
   a placeholder, and names a path/line/commit.
4. The section line number is after the round-38 filled section's heading; the last matching section wins only
   after duplicates are rejected.

Selftest mutants: dropped row; duplicate row; `1x`; empty status; empty evidence; heading-only; correction
outside the section; section before round-38.

## G8 — pinned carry-over

| | minimal state | naive limb that gets it wrong |
|---|---|---|
| RED-should-pass | export copy is a stub printing `closed=14/14 exit=0` | last-line-only check accepts (measured) |
| RED-should-pass | digest compared against the export copy's own digest | circular comparison always green |
| GREEN-may-fail | pinned bytes are compared to a git **blob id** (sha1) | always mismatches a sha256 (or is skipped) |
| GREEN-may-fail | run over J while HEAD is Y | r37 E9 `head-match=0` reds (see P0.2) |

MUST:

1. Hardcode the expected sha256 of the pinned bytes (`0da98e37…`, with the `2387dcf6` blob path in a comment) and
   extract with `git -C "$LANE" show 2387dcf6ccfefcfb703783387b9aade8fc82abfa:corpus/instruments/r37-closure.sh`
   fail-closed to `<work>/r37-pinned/r37-closure.sh`; verify sha256 == the constant.
2. Verify the export's own `corpus/instruments/r37-closure.sh` sha256 == the same constant **before** trusting
   anything (a stub or edited copy is RED even if it prints 14/14).
3. Run the **pinned** copy with `--export-ref "$REF" --lane "$LANE" --work "$WORK/r37"`; require exit 0 and the
   last non-empty line exactly `closed=14/14 exit=0`; do not parse the sub-suite's internals beyond that.
4. Report `r37-suite=1,r37-digest=1,r37-export-digest=1,r37-closed=1,r37-exit=0` so a reader can see which limb
   reds.

Selftest mutants: changed pin constant; mutated export copy (one appended byte); stub export copy printing
14/14; missing pinned path; sub-run red; REF != HEAD.

## Cross-cutting contract

- Export-only: a plain run exits 2 before writing; an unresolvable `--export-ref` exits 2 and prints no
  `closed=` line; `--work` inside the lane exits 2 before creating; every check reads only the export root
  except G6 (live scratch) and ref-scoped git reads (`cat-file`, `merge-base`, `diff`, `show`, `rev-parse`).
- Output: `export-ref=<resolved> mode=export lane=… suite-sha256=…`; one `G<n> payload=… closed=0|1` per check
  (ids 1–8, all payload keys non-empty); `closed=<k>/8 exit=0|1`. Selftest: one graded
  `selftest case=G<n> positive=pass mutants=K/N verdict=pass` per check, `selftest detail=` lines with
  `rejected=1` limbs, `selftest cases=8 failures=0`, plus the judge (own report accepted, forged reports
  rejected).
- Cleanup trap removes export/mut/work; no writes under the lane; `bash -n` clean.
- The suite's own bytes are frozen at J; after the receipt is generated, no edit may change the digest.

## Verification sequence for the L1 (on the tip Y, HEAD==Y, clean tree)

1. `bash -n corpus/instruments/r39-closure.sh`
2. plain run → exit 2, no output files.
3. `--export-ref <base>` → `closed<8/8 exit=1`, with G1/G2/G4/G5/G7/G8 payloads red (G3 is added-line-scoped
   and may be vacuous at base; G6 is live).
4. `--export-ref 66703acaaff50529a35be49aa8759d04140720ad` (E2's 40-hex) → `closed<8/8 exit=1`.
5. `--export-ref <Y>` → `closed=8/8 exit=0`.
6. `--selftest --export-ref <Y>` → 8 graded case lines, every `positive=pass mutants=K/N verdict=pass`
   (K=N, N>=2), `selftest cases=8 failures=0`; the judge rejects forged summaries.
7. `--selftest --export-ref <base>` → the mutants are still all rejected; the positives may be red (item says
   record honestly) but no case may be satisfied by a summary line.
8. `--export-ref <J>` → record the 7/8 (G2, plus G8 if HEAD≠J) as the documented self-reference red; the receipt
   embeds it prefixed. Do not quote it as the green run.

## Fixture map

- `ExecWholeTailFixture` (fixtures a–e): G1 full-tail green, partial-tail red, inside-fence correction red,
  tilde door green (old walk red), outside path red — the five states above.
- `ExecGradedSelftestFixture`: G2 case-line states (summary-only, positive-without-mutants, mutants=0/0, K<N,
  K=N) and the anchored-field counts.
- `ExecPinnedG8Fixture`: G8 stub/mutant/constant states.
- `ExecG4ResultsFixture`: G4 identity/zero-task/stale-sibling states.
- `ExecProofSuiteSelftest` / `ExecSuiteBuild`: the judge and the eight case lines.

A fixture that only proves "the check can print closed=1" proves nothing; each mutant must name the reopened
limb in its payload (`grep -F` the expected limb string) because the selftest case line must show it was the
intended clause that flipped.
