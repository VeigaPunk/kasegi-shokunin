# RevQualityFix — closure checks of `corpus/QUALITY.md` R16/R17 and the R18/R19 supersessions (round 31, wave 3)

Seat: RevQualityFix (leaf; no delegation, no subagent, no background job). Answering model actually run on:
`opencode-go/deepseek-v4.1-flash` (workstation config route; no model passed by this seat).
Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`;
wave-2 integration commit `fd29aac0dd02f4c6783a0df8c4ba8d0e86414242`; lane HEAD at measurement `a155310`.
Writes: this receipt only. No tool installed or upgraded (no pacman transaction, no uv/npx, no binary);
no git/jj mutation; all mutants in one `mktemp -d` under `/tmp` (removed, §10).

## 0. Subjects, digests, quiescence

```
$ date -u +%Y-%m-%dT%H:%M:%SZ; sha256sum SCORECARD.md LOG.md corpus/QUALITY.md \
    corpus/instruments/recheck-audit.py corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json
2026-10-26T01:10:52Z
4076091c3d06d5336858ce7b16a05a8d0722def7f527b8e39b39ac7586a7a9da  SCORECARD.md
864deb7df810539d3a92a9c520c94e218836233da42378ba774e48bbf339cf1b  LOG.md
300f9962e3017ca0846038d193cfe83f674989dccf78d4488caa59e578badaba  corpus/QUALITY.md
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
237fd07cbcb4a12a470e912d1a4b68ff1968fde62f2709b182822fed42d791f4  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
$ wc -l SCORECARD.md LOG.md corpus/QUALITY.md
   947 SCORECARD.md
  1582 LOG.md
   158 corpus/QUALITY.md
$ git diff --stat fd29aac -- corpus/QUALITY.md SCORECARD.md LOG.md | wc -l
0
$ git show fd29aac:corpus/QUALITY.md | sha256sum; git show fd29aac:SCORECARD.md | sha256sum
300f9962e3017ca0846038d193cfe83f674989dccf78d4488caa59e578badaba  -
4076091c3d06d5336858ce7b16a05a8d0722def7f527b8e39b39ac7586a7a9da  -
$ git diff -U0 b374febb -- corpus/QUALITY.md | grep -c '^-[^-]'      → 0
$ date -u ...; sha256sum (re-run at 01:19:18Z and 01:21:45Z)
SCORECARD 4076091c… LOG 864deb7d… QUALITY 300f9962… recheck-audit 5d4842da… counter 237fd07c… ledger c042adf6…
```

All three subjects are the integrated `fd29aac` bytes and did not move across this seat's runs (bound 6:
every number below is on these digests). `QUALITY.md` is append-only vs lane base (0 deleted lines).

Relevant row positions (unchanged from the wave-2 receipt): `R13 :77`, `R16 :95`, `R17 :96`, R18 `:102`,
R19 `:103`; fenced blocks `:110-133` (CHECK A'), `:137-144` (CHECK B'), `:148-158` (R19).
Row shape: `awk` unescaped-pipe count on `:102`,`:103` → `pipes=3` each (valid 3-column rows).

## 1. The three shipped closure blocks, extracted verbatim and parsed

```
$ awk 'NR>110 && NR<133' corpus/QUALITY.md > $T/b1.sh   # CHECK A'
$ awk 'NR>137 && NR<144' corpus/QUALITY.md > $T/b2.sh   # CHECK B'
$ awk 'NR>148 && NR<158' corpus/QUALITY.md > $T/b3.sh   # R19
$ for f in b1 b2 b3; do printf '%s: ' "$f"; bash -n "$T/$f.sh" && echo "bash-n-ok $(wc -l < "$T/$f.sh") lines"; done
b1: bash-n-ok 22 lines
b2: bash-n-ok 6 lines
b3: bash-n-ok 9 lines
```

Q10 form holds — every block opens with `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9`; run from
the foreign cwd `/tmp` all three still reach the lane:

```
$ cd /tmp && bash $T/b1.sh 2>&1 | tail -2
file=SCORECARD.md filed_byte_identical=y phrases=2 anchor=837 naming_erratum=1 live_citation_self_naming=0 live=strict pass=44/44 instrument=5d4842da
erratum_closure=open
$ cd /tmp && bash $T/b2.sh 2>&1 | tail -2
file=LOG.md round30_h2_headings=1 round30_h2_or_h3_headings=2
log_closure=closed
$ cd /tmp && bash $T/b3.sh 2>&1 | tail -2
live_selftest_ok_lines=18 instrument_cases_summary_lines=0 supersedes_r13_rows=1 row_cites_selftest=1
r13_specimen_closure=closed
```

No block writes the lane:
`recheck-audit.py` opens files only under `tempfile` trees (`grep -nE "open\(.*['\"][wa]" corpus/instruments/recheck-audit.py`
→ `:205-207,:230,:242,:262-267`, all `os.path.join(tmp|tree, …)`).

Fixtures for the base column:

```
$ git show b374febb:SCORECARD.md > $T/sc-base.md   → cac64dbdb8cd9ed834a6deca44c5b4fd5874f1e95d2f1118f919c3ccb84811b9, 835 lines
$ git show b374febb:LOG.md      > $T/log-base.md   → 0a1865e90f29c5d4a20fa3fda8f9daf6b6293bbec95710bafcda0cf65d537221, 1467 lines
$ git show b374febb:corpus/QUALITY.md > $T/q-base.md → a39e0b5e2bf4631c07bd75f40209f2fc33a65c5844dca0191b51db9448ca13f9, 89 lines
$ sed -n '813,819p' $T/sc-base.md | sha256sum → d6c6ea77c9450bfc6886bf75e5f5b48e9056e1bd9cd213febea31e25a206a7b1
```

The span pin in CHECK A' matches the base bytes, so arm (i) is a base-valid pin, not a post-hoc one.

## 2. CHECK A' — `SCORECARD.md` (the check R16's clause rests on, carried by R18)

### 2.1 The four required measurements

| # | byte-state | construction | result | required | ok |
|---|---|---|---|---|---|
| a | `sc-base.md` `cac64dbd…` | `git show b374febb:SCORECARD.md` | `filed_byte_identical=y phrases=1 anchor=none naming_erratum=0 live_citation_self_naming=0` / `erratum_closure=open` / exit **1** | 1 | y |
| b | landed `SCORECARD.md` `4076091c…` | default `$1` | `filed_byte_identical=y phrases=2 anchor=837 naming_erratum=1 live_citation_self_naming=0` / `erratum_closure=open` / exit **1** | 0 | **N** |
| c | `sc-erratum-deleted.md` | `awk 'NR>=837&&NR<=860{next}'` | `filed_byte_identical=y phrases=1 anchor=none naming_erratum=0 live_citation_self_naming=0` / `open` / exit **1** | 1 | y |
| d | `sc-both-deleted.md` | paragraph `813-819` **and** erratum `837-860` removed, no erratum anywhere | `filed_byte_identical=n phrases=0 anchor=none naming_erratum=0` / `open` / exit **1** | 1 | y |

```
$ bash $T/b1.sh                    # b, landed
file=SCORECARD.md filed_byte_identical=y phrases=2 anchor=837 naming_erratum=1 live_citation_self_naming=0 live=strict pass=44/44 instrument=5d4842da
erratum_closure=open
exit=1
```

Row (b) is the assignment's "current file must exit 0" and it fails. Cause is measured, not inferred:

```
$ grep -n 'strict pass=' SCORECARD.md | awk -F: '$1>=810{print $1}'
839 841 852 858 875
$ grep -c '44/44' SCORECARD.md          → 1      # line 875, the C1 move-log row
$ grep -n '5d4842da' SCORECARD.md      → 913    # the Round-31 "Measurement state" paragraph
$ sed -n '839p;852p;858p' SCORECARD.md | cut -c1-120
r31 erratum: the paragraph `recheck-audit open item (outside the frozen claims)` filed at `SCORECARD.md:813-819` …
strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0
Measurement limit, recorded rather than hidden: … prints `strict pass=1/43 cdroot_fail=42 …
$ python3 corpus/instruments/recheck-audit.py --quiet | head -1
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
```

The naming erratum at `SCORECARD.md:837-860` (added by wave-1 `eecad59`, `git log -S'### Round-31 erratum to the
round-30 section' -- SCORECARD.md`) quotes **43/43**; the instrument at `5d4842da…` prints **44/44**. The
wave-2 integration `fd29aac` (+87 lines to `SCORECARD.md`) recorded the new reading only in the measurement
paragraph (`:913`) and the move-log (`:875`), never as a `strict pass=` window carrying value + digest +
`SCORECARD.md:813-819`. R18 arm (iii) is therefore red **as specified** ("a changed instrument re-opens the
check until a labelling entry cites the new triple") — the row's own criterion is not met *by the lane*.

### 2.2 The check can close: green-after and forged controls

```
$ cat $T/label.txt >> $T/sc-relabel.md   # the label ScribeQualityFix.md §5 item 1 routed, appended in scratch
### Round-31 errata — instrument relabel for the C1 limb change
r31 erratum: the paragraph `recheck-audit open item (outside the frozen claims)` filed at `SCORECARD.md:813-819`
is re-labelled, not rewritten: after the C1 limb work `corpus/instruments/recheck-audit.py` sha256
`5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09` prints
`strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0` (`lines=44 total=44`), measured 2026-10-26T00:45Z.

$ bash $T/b1.sh $T/sc-relabel.md
file=/tmp/revq-JHM4VnCl/sc-relabel.md filed_byte_identical=y phrases=3 anchor=837 naming_erratum=1 live_citation_self_naming=1 live=strict pass=44/44 instrument=5d4842da
erratum_closure=closed
exit=0
$ bash $T/b1.sh $T/sc-relabel-bad.md        # same label, digest deadbeef…
live_citation_self_naming=0 → erratum_closure=open, exit=1
$ bash $T/b1.sh $T/sc-relabel-stale.md      # same label, strict pass=43/43
live_citation_self_naming=0 → erratum_closure=open, exit=1
```

The check is discriminating, not permanently red: the exact append routed in wave 2 turns it green, and a
wrong digest or a stale value keeps it red. **R18 ships no conforming specimen today**, and the fix is one
append outside `QUALITY.md`.

### 2.3 The row's remaining claimed mutants, re-derived

```
### sc-para-deleted.md   (813-819 deleted, erratum intact)
filed_byte_identical=n phrases=1 anchor=830 naming_erratum=1 live_citation_self_naming=0 → open, exit=1
### sc-reword.md         (line 814 `exit=1`→`exit=0`, in place)
filed_byte_identical=n phrases=2 anchor=837 naming_erratum=1 live_citation_self_naming=0 → open, exit=1
### sc-m4-unrelated.md   (erratum replaced by an unrelated r31 errata quoting the phrase, no address)
filed_byte_identical=y phrases=2 anchor=837 naming_erratum=0 → open, exit=1
### sc-forge.md          (landed + forged `strict pass=44/44 … 5d4842da`, no address)
filed_byte_identical=y phrases=2 anchor=837 naming_erratum=1 live_citation_self_naming=0 → open, exit=1
### sc-relabel-later.md  (label, then a later unrelated row quoting the audit)
live_citation_self_naming=1 → closed, exit=0     ← the §8 false-red case, now green
```

Every mutant R18's grounding cell claims is exit 1 except the label; the label-then-later-window case stays
green (§8 repair effective). The disclosed residual (a fabricated window carrying value+digest+address closes)
is real but is disclosed in the row and in `ScribeQualityFix.md` §5 item 5.

## 3. CHECK B' — `LOG.md`

| # | byte-state | construction | result | required | ok |
|---|---|---|---|---|---|
| a | `log-base.md` `0a1865e9…` | `git show b374febb:LOG.md` | `round30_h2_headings=0 round30_h2_or_h3_headings=0` / open / exit **1** | 1 | y |
| b | landed `LOG.md` `864deb7d…` | default | `round30_h2_headings=1 round30_h2_or_h3_headings=2` / closed / exit **0** | 0 | y |
| c | `log-entry-deleted.md` | round-30 entry `1469-1582` removed ("erratum block") | `h2=0 h23=0` / open / exit **1** | 1 | y |
| d | `log-body-deleted.md` | body `1469-1549` removed, h3 `:1550` kept | `h2=0 h23=1` / open / exit **1** | 1 | y |

Also killed: `log-relabel.md` (`## Round 30` → `## Round 29`, h3 kept) → `h2=0 h23=1` exit 1;
`log-h3only.md` (base + `### Round-30 backfill (appended)`) → `h2=0 h23=1` exit 1.

**Hole found (new, not in either wave-2 receipt): the level test is met by a content-free heading.**

```
$ { cat $T/log-base.md; echo; echo '## Round 30'; } > $T/log-empty-h2.md
$ bash $T/b2.sh $T/log-empty-h2.md
file=/tmp/revq-JHM4VnCl/log-empty-h2.md round30_h2_headings=1 round30_h2_or_h3_headings=1
log_closure=closed
exit=0
```

A bare `## Round 30` with no entry text closes the check. R18's clause excludes "an `###` sub-section that
only mentions the round" for exactly that reason; an `##` heading that only mentions the round is the same
shape one level up and is admitted. The check binds heading level, not entry presence.

## 4. R19 — the R13 specimen closure

| # | byte-state | construction | result | required | ok |
|---|---|---|---|---|---|
| a | `q-base.md` `a39e0b5e…` | `git show b374febb:corpus/QUALITY.md` | `selftest_ok=18 cases_summary=0 supersedes_r13=0 cites=0` / open / exit **1** | 1 | y |
| b | landed `QUALITY.md` `300f9962…` | default | `selftest_ok=18 cases_summary=0 supersedes_r13=1 cites=1` / closed / exit **0** | 0 | y |
| c | `q-append-deleted.md` | R18/R19 append `97-158` removed | `supersedes_r13=0 cites=0` / open / exit **1** | 1 | y |
| d | `q-r13-del-no-append.md` | filed R13 row `:77` deleted, no append | `supersedes_r13=0` / open / exit **1** | 1 | y |

Live figures the row quotes, re-measured: `python3 corpus/instruments/recheck-audit.py --selftest` → exit 0,
`grep -c '^selftest .* ok$'` → **18**, `grep -cE '^selftest cases='` → **0**; the stale literal
`selftest cases=4 failures=0 exit=0` occurs twice in `QUALITY.md` (`:77` and `:103`, the row quoting it).

**Four false greens measured (each is an exit 0 where the row's own criterion demands 1):**

```
$ bash $T/b3.sh $T/q-r13-deleted.md      # filed R13 row (77) deleted, R19 row intact
live_selftest_ok_lines=18 instrument_cases_summary_lines=0 supersedes_r13_rows=1 row_cites_selftest=1
r13_specimen_closure=closed
exit=0
$ bash $T/b3.sh $T/q-r13-reworded.md     # stale literal reworded IN PLACE (cases=4 → cases=18)
… supersedes_r13_rows=1 row_cites_selftest=1 → closed, exit=0
$ bash $T/b3.sh $T/q-figure-25.md        # R19's figure changed to a FALSE "prints 25"
… live_selftest_ok_lines=18 … → closed, exit=0        ← the false 25 is never compared
$ bash $T/b3.sh $T/q-vacuous-row.md      # base + `| R99 | a specimen figure | supersedes R13 — see the live `--selftest` figure |`
… supersedes_r13_rows=1 row_cites_selftest=1 → closed, exit=0
$ bash $T/b3.sh $T/q-stub-row.md         # base + `| R99 | x | supersedes R13 |` (no token)
… row_cites_selftest=0 → open, exit=1
```

Root, from the block's own bytes: `live` is computed at `QUALITY.md:151` and used only in the `printf` at
`:155` — `grep -n 'live' $T/b3.sh` returns exactly its lines 3 and 7 (= `QUALITY.md:151,:155`), no comparison — and
`cmd=$(… | grep -c -- '--selftest')` accepts the token anywhere in the row. The criterion requires the row to
"name the stale literal" and "carry the command that computes the live figure"; the check tests neither, and
it has no analog of R18 arm (i), so the forbidden in-place edit of the filed row is invisible.

## 5. R17's replay, executed (not read)

```
$ python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
counter_exit=0            (114 s wall)
grep -c '^LIMB ' → 13
limbs=13 killed=13 survivors=0
controls=3 rejected=3
guard invalid-live-baseline  verdict=invalid:live-baseline want=invalid:live-baseline ok
guard invalid-find-count     verdict=invalid:find-count   want=invalid:find-count   ok
CONTROL CTL-nocompile  verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor          expected=survivor          ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
$ grep '^LIMB ' … | awk '{print $2}' | tr '\n' ' '
RA-parse RA-cwd RA-paths RA-cdroot RA-instrument RA-own RA-completeness RA-expect-missing
RA-expect-unexpected SR-stem-mismatch SR-occurrence-not-unique FR-missing-entry FR-duplicate-entry
$ grep '^CONTROL ' … | awk '{print $2}' → CTL-noop CTL-nocompile CTL-equivalent
$ python3 -c "import json;d=json.load(open('corpus/instruments/limb-ledger.json'));print(len(d['limbs']),len(d['controls']))"
13 3
```

The 13 ids are exactly the frozen C1 list; the summary lines are the frozen text. The base column for R17 is
**pre-state**, not an after column: at `b374febb` neither file exists —
`git cat-file -e b374febb:corpus/instruments/limb-mutation-check.py` (and `…/limb-ledger.json`) → `fatal: path
… exists on disk, but not in 'b374febb…'`, exit 128 — and the claims' do-nothing control records the absent
counter's `counter_exit=2` at `.ufo/waves/round-31/c1-controls/before.txt:8`.

## 6. Cited lines — resolution check

| cite | location | resolves |
|---|---|---|
| `corpus/lessons/round-31.md` § Mistakes M31-1 | `round-31.md:100` heading, `:104` M31-1 | y |
| `corpus/lessons/round-31.md` § Mistakes (survivor/limb entries) | `:109` **M31-5** ("the class QUALITY **R17** now governs") | y (coarse: no M-id) |
| `SCORECARD.md:813` / stale reading `:814` | `:813` `**recheck-audit open item (outside the frozen claims).**`; `:814` `prints \`expect=present expected=43 missing=0 unexpected=0 exit=1\`` | y |
| `corpus/lessons/round-30.md` § Close-out erratum | `:110` | y |
| `round-30-verifier-spotcheck.md` §1 defect 3 | §1 defects list, item (3) (SCORECARD stale paragraph) | y |
| same, §5 item 4 | `:70` | y |
| `wave1/ExecErratumCheck-before.txt` / `-after.txt` | 8642 B / 6809 B; quoted lines at `before:44,46` and `after:29,31` match R16 verbatim | y |
| `wave1/ledger-fragments/ra.json` RA-completeness quote (21 words) | 5074 B; quote present verbatim | y |
| `wave1/ExecErratumCheck.md` §1, §5 | `:50`, `:221` | y |
| `wave1/ScribeQuality.md` F1 | `:138` | y |
| `CritMistakes.md` §2.1, §3, §4, §6 (M31-4) | `:91`, `:111`, `:138`, `:254` | y |
| `MutErratumCheck.md` §2 mutant (c), (d1) | `:62` Survivor 1 (c), `:76` Survivor 2 (d1) | y |
| `ScribeQualityFix.md` §2–§3, §8 | present | y |
| `corpus/QUALITY.md:95` (R18 quoting R16) | `:95` R16 row | y |
| M31-4 statement (`QUALITY.md:77` `cases=4`) | `lessons/round-31.md:108`; `QUALITY.md:77` carries the literal | y |

No dangling cite found. R16's "Limit measured here" sentence is also accurate, measured with the shipped
check it points at (`awk 'NR>55&&NR<65' wave1/ExecErratumCheck.md`, `bash -n` clean):

```
$ bash $T/shippedA.sh $T/sc-base.md                  # base, claimed paragraph standing
stale_paragraphs=1 erratum_anchor=none names_item_and_cites_corrected_audit=0 → open, exit=1
$ sed 's/recheck-audit open item/recheck audit open item/' $T/sc-base.md → reworded away, no erratum
stale_paragraphs=0 erratum_anchor=none … → closed, exit=0     ← R16's disclosed limit, confirmed
$ bash $T/shippedA.sh                                # the SAME check on the CURRENT file
stale_paragraphs=2 erratum_anchor=837 names_item_and_cites_corrected_audit=1 → closed, exit=0
```

The third line is R16's residual defect: the specimen R16 cites calls today's stale citation **closed**.

## 7. Verdicts

| row | falsifiable | `bash -n` check | (a) | (b) | (c) | (d) | verdict |
|---|---|---|---|---|---|---|---|
| R16 | yes | **no** — no runnable check in the row; points at the shipped CHECK A, not at CHECK A' | 1 ✓ | **1 ✗** | 1 ✓ | 1 ✓ | **weak** |
| R17 | yes | yes (inline command, not fenced; executes) | pre-state exit 2 | **0 ✓** | n/a (method row) | n/a | **holds** |
| R18 | yes | yes — CHECK A' `:110-133`, CHECK B' `:137-144`, both `bash -n` clean, foreign-cwd clean | 1 ✓ | **1 ✗** | 1 ✓ | 1 ✓ | **defect** |
| R19 | yes | yes — `:148-158`, `bash -n` clean | 1 ✓ | **0 ✓** | 1 ✓ | 1 ✓ | **defect** (check weaker than criterion) |

(a)-(d) are §2.1, §3, §4 of this receipt. R18's verdict is defect on two counts: (b) is red — the row's own
clause has no conforming landed specimen — and CHECK B' admits a content-free `## Round 30` heading. R19's
verdict is defect on four measured false greens (§4), even though it passes (a)-(d) as the assignment frames
them, because the assignment's (c)/(d) are the *strong* mutants; the weak ones it must also kill are not killed.

## 8. Findings, by severity, with owners

1. **BLOCKER (state, not the row): `SCORECARD.md` has no labelling erratum — CHECK A' is red on landed bytes.**
   `SCORECARD.md:839/:841/:852/:858` cite `strict pass=43/43`; `recheck-audit.py` `5d4842da…` prints
   `strict pass=44/44` (44 lines). Fix = append the block in §2.2 to `SCORECARD.md` (scratch-verified exit 0).
   Owner: L1 / ScribeScorecard. Until then R16's item is open and the round's verifiability story ships a
   criterion whose own check fails on the corpus it governs.
2. **DEFECT: CHECK B' closes on a content-free `## Round 30` heading** (§3). Fix: require ≥1 non-blank line
   between the h2 and the next heading, or a required identifying string from the entry (e.g. `## Round 30 —
   2026-10-25 —`). Owner: L1 (QUALITY is claims-frozen for scribes this wave).
3. **DEFECT: R19's check is a token grep** (§4): closes on a row with no command, no named stale literal and
   no figure; never compares the `live` count it computes (a false "prints 25" closes); has no byte-binding of
   the filed row, so deleting or rewording `QUALITY.md:77` in place — the one edit R19 forbids — is invisible.
   Fix: pin the filed row's bytes, assert `live` equals the figure the superseding row quotes (or drop the
   figure from the row), and require an executable command (e.g. the block `bash -n`-parseable and its output
   captured), not the literal `--selftest`.
4. **WEAK: R16 points at the superseded specimen.** Its cited shipped CHECK A returns exit 0 on today's stale
   bytes (§6, third run) while CHECK A' returns 1; the row carries no pointer to CHECK A'. Fix (append-only):
   a line in R16's grounding cell naming R18/CHECK A' as the enforcement of its own clause. Keep the disclosed
   limit sentence — it is accurate and it is what makes the row honest.
5. **MINOR (outside the rows): `LOG.md:1579-1581` repeats the stale literal** — "superseded by the erratum's
   final `strict pass=43/43 … exit=0`" — the same class as M31-4, and CHECK B' cannot see it (heading-level
   only). Routed; needs the same 44/44 relabel as finding 1.
6. **MINOR (brittleness, measured):** CHECK A' matches the literal address `SCORECARD\.md:813-819` and R19's
   check matches the literal `supersedes R13 ` (trailing space); an en-dash address or a period after `R13`
   false-reds. Not a defect today; disclosed.
7. **MINOR (degenerate arm):** if the live instrument ever prints no `strict pass=` line, `live` is empty and
   `printf … | grep -qF ""` succeeds on every line (`printf 'x\n' | grep -qF ""` → 0), so arm (iii) degrades to
   digest+address. Fix: guard `[ -n "$live" ]`.

## 9. Residual risk and verification gaps

- **Shape vs intent (disclosed, not closable):** a fabricated `strict pass=44/44 … 5d4842da … SCORECARD.md:813-819`
  window closes CHECK A' even with no real erratum. R18 says so; this review confirms the disclosure is honest.
- **R17's count is not R17's:** the replay binds one line per ledger row, so a 12-row ledger would print
  `limbs=12 killed=12` and exit 0; the 13-limb set is C1's frozen kill rule, not this row's predicate. Stated
  as text, not measured (pruning the ledger would require a root copy and a second 114 s run).
- **Not done here (other seats' scope):** the C1 counter's mutant battery (always-killed, no-live-baseline,
  exit-code-only, find-not-unique); the C2 entry/S048 content; `source-recheck.py`/`frontier-recheck-count.py`
  behaviour. R19's `sum` branch (`instrument_cases_summary_lines>=1`) is unreachable on landed bytes and stays
  unexercised — no mutant can reach it without editing the instrument, which is not this seat's path.
- LOG's round-30 entry content was read only at its headings; no claim is made about its prose.

## 10. Bounds and cleanup

Writes: this receipt only (`.ufo/waves/round-31/wave3/RevQualityFix.md`). No lane file, corpus file,
instrument, entry, registry, `SCORECARD.md`, `LOG.md`, `QUALITY.md`, lesson, `.ufo/state/`, `MANIFEST.json`,
fleet root, sibling lane, lane Git index, jj state, `templates/`, `scripts/`, `/home/vgpnk/Projects/shokuknow`,
or `/home/vgpnk/Projects/shokunin/.scratch/` was written. No git/jj mutation (read-only `git show`, `log`,
`diff`, `status`, `cat-file`, `rev-parse`). No pacman transaction, no network fetch, no live bounty target, no
credential material. No delegation, no background job, no `agent://all`. All mutants lived in one
`mktemp -d` (`/tmp/revq-JHM4VnCl`) and are gone:

```
$ rm -rf /tmp/revq-JHM4VnCl /tmp/revq-dir /tmp/revq-counter.txt /tmp/revq-st.txt
$ ls -d /tmp/revq-*  → ls: cannot access '/tmp/revq-*': No such file or directory
$ git status --porcelain | grep -v '\.ready'
?? .ufo/waves/round-31/wave3/
$ date -u +%Y-%m-%dT%H:%M:%SZ → 2026-10-26T01:21:45Z
```

**Disclosed writing-path slip and its correction (bound 1).** The first `write` of this receipt was given a
relative path and resolved against the fleet root, creating
`/home/vgpnk/Projects/shokunin/.ufo/waves/round-31/wave3/RevQualityFix.md` and its two parent directories.
Caught before yield by `ls` on the lane path. Corrected with no residue: the file was copied into the lane
(sha256 `35300913c6c39fee26dd8df228d4f7660e0c73abadafd3d61c79b7d5b0d3c8a7` on both sides before the copy was
trusted), then the fleet-root file was removed and both empty directories (`…/round-31/wave3`, `…/round-31`)
were `rmdir`ed — `ls -ld /home/vgpnk/Projects/shokunin/.ufo/waves/round-31` now reports
`No such file or directory`. No fleet-root file survives from this seat; nothing outside the lane was read or
altered, and the lane was never written by that slip.
