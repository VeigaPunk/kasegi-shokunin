# RevJunkTwin — junk-twin control review (round 34, wave 1)

Seat: reviewer, wave-1, round 34. Lane base `014ee2d7aa8c3c095ff57ae51097606a9906228c`, claims freeze
`29f606dbdd28aff6fd4573ab4b90788bbb90af13`. Read-only over the lane except this receipt; no git/jj
mutation (only `git log`/`git show`/`git ls-tree`/`git diff`/`git status` reads); no subagent; no tool
installed (none needed); scratch `/fast/scratch/hyaku/kasegi-r34/RevJunkTwin/` deleted before yield.
Peers contacted: `RevEntryF17` (one status question; reply quoted in §4).

## Report

Verdict up front: **the junk-twin control holds.** All four seat criteria verified by execution:
(1) committed at the freeze commit; (2) shape counters pass it `3/3`; (3) the admission gate rejects
its bytes — fabricated quote `MISMATCH reason=quote-not-found` exit 1, manifest-missing mode exit 2;
(4) the F17 entry review does not admit the junk bytes (digest-bound ADMIT of the real entry only).

### 1. `junk-f17.md` is committed; controls unchanged since freeze

```
$ git log --oneline -- .ufo/waves/round-34/c2-controls/junk-f17.md
29f606d round-34: freeze claims C1/C2 with do-nothing controls, census-before, assimilation guard prep
$ git log --oneline -- .ufo/waves/round-34/c2-controls/junk-checker.py
29f606d round-34: freeze claims C1/C2 with do-nothing controls, census-before, assimilation guard prep
$ git show --stat 29f606d -- .ufo/waves/round-34/c2-controls/
 .ufo/waves/round-34/c2-controls/before.txt      | 45 +++++++++++++++++++++++++
 .ufo/waves/round-34/c2-controls/junk-checker.py | 19 +++++++++++
 .ufo/waves/round-34/c2-controls/junk-f17.md     | 18 ++++++++++
 3 files changed, 82 insertions(+)
$ git ls-tree 29f606d -- .ufo/waves/round-34/c2-controls/
100644 blob 752cec4c…  .ufo/waves/round-34/c2-controls/before.txt
100755 blob 14a217ea…  .ufo/waves/round-34/c2-controls/junk-checker.py
100644 blob 50f7a84c…  .ufo/waves/round-34/c2-controls/junk-f17.md
$ git ls-tree 014ee2d -- .ufo/waves/round-34/        # base: no output → controls absent at base
$ git diff --stat 29f606d -- .ufo/waves/round-34/c2-controls/   # empty → working copy byte-identical to freeze
```

Digests measured (sha256sum):

```
2752a994265a1e284ebd236730d169d677e1923cfb7073cf79ad874d19bc4026  .ufo/waves/round-34/c2-controls/junk-f17.md
c8438b4da19145efa7594dd576be0eba270fad3d27c378b5b6f99c1b6b0d8e1a  .ufo/waves/round-34/c2-controls/junk-checker.py
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  corpus/source-snapshots/round-34/S051.txt
d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe  corpus/source-snapshots/round-34/manifest.json
948b202ebe1f32728a19d7bf2ead67911ba624d3699bde2dfd486f6725ac1d8a  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
```

(`junk-checker.py` working-copy mode `-rwxr-xr-x` matches the committed `100755`. `git status
--porcelain` lists no `c2-controls` path and no `M corpus/instruments/source-recheck.py`, so the
control bytes and the gate bytes I ran are the committed ones.)

### 2. Shape counters pass the twin (as designed)

```
$ python3 .ufo/waves/round-34/c2-controls/junk-checker.py
junk_twin h1=True source_line=True recheck_line=True
shape_counters=3/3
exit=0
```

Matches the recorded pre-freeze run in `.ufo/waves/round-34/c1-controls/fake-controls-receipt.txt:11-17`
(`shape_counters=3/3`, `junk_checker_exit=0`, `junk_recheck_exit=2`).

### 3. The admission gate rejects the twin's bytes — explicit run on the fabricated quote

The twin's own `recheck:` line points at the real manifest, so the falsifying comparison is a
manifest **derived from the twin's bytes**: I extracted the fabricated evidence sentence from
`.ufo/waves/round-34/c2-controls/junk-f17.md` § "What this adds" (the `[FABRICATED …]` marker line
excluded), asserted it against a byte-identical copy of the committed `S051.txt`, and ran the real
committed `corpus/instruments/source-recheck.py` on it. Fixture builder
`/fast/scratch/hyaku/kasegi-r34/RevJunkTwin/junk_recheck_fixture.py` (deleted with scratch; it
imports the instrument's own `normalize()` and `MIN_QUOTE_CHARS` — no reimplementation). Output:

```
fabricated_quote='Immunefi\'s VSCS v2.2 defines five severity levels for smart-contract exploits;
Critical includes "Direct theft of any user funds".'
capture_copy_sha256=4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5
capture_lane_sha256=4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5
fabricated_quote_occurrences_in_S051=0
fixture_manifest=/fast/scratch/hyaku/kasegi-r34/RevJunkTwin/junk-manifest-dir/manifest.json
fixture_quote_id=junk-fabricated (single assertion; all other record fields byte-equal to the real manifest)
```

Gate run on the junk-quote manifest (schema_version, id S051, path, sha256 pin, url, strict-UTC
fetched_utc all byte-equal to the real record; only `quotes` replaced by the twin's sentence):

```
$ python3 corpus/instruments/source-recheck.py --manifest <scratch>/junk-manifest-dir/manifest.json --source S051
S051:sha256 OK
S051:junk-fabricated MISMATCH reason=quote-not-found
junk_gate_exit=1
```

Control — same command, real manifest, real entry (proves the gate discriminates, not merely fails):

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
S051:sha256 OK
S051:Q1 OK occurrences=1 anchor=46-ok          S051:Q10 OK occurrences=1 anchor=79-ok
S051:Q11 OK occurrences=1 anchor=83-ok         S051:Q12 OK occurrences=1 anchor=88-ok
S051:Q13 OK occurrences=1 anchor=92-ok         S051:Q14 OK occurrences=1 anchor=94-ok
S051:Q15 OK occurrences=1 anchor=90-ok         S051:Q16 OK occurrences=1 anchor=95-ok
S051:Q17 OK occurrences=2 anchor=96-ok         S051:Q18 OK occurrences=1 anchor=99-ok
S051:Q2 OK normalized=markup-whitespace occurrences=1   S051:Q3 OK occurrences=1 anchor=52-ok
S051:Q4 OK occurrences=1 anchor=52-ok          S051:Q5 OK normalized=markup-whitespace occurrences=1 anchor=53-ok
S051:Q6 OK normalized=markup-whitespace occurrences=1 anchor=55-ok
S051:Q7 OK occurrences=1 anchor=74-ok          S051:Q8 OK occurrences=1 anchor=75-ok
S051:Q9 OK occurrences=2 anchor=77-ok
exit=0
```

Second failure mode, "manifest missing" (the pre-freeze state the twin's `recheck:` line actually
points at inside commit `29f606d`, since `corpus/source-snapshots/round-34/` is still untracked
`??` in the working copy and absent from the freeze tree):

```
$ python3 corpus/instruments/source-recheck.py --manifest <scratch>/absent/manifest.json --source S051
manifest UNAVAILABLE reason=missing
exit=2
```

Honest scope note (closes the PENDING-AFTER-BATTERY flag at
`.ufo/waves/round-34/wave1/RevC2BeforeAfter.md:129-132`): the twin's *verbatim* `recheck:` line run
at the tip exits 0, because it names the real manifest and therefore re-checks the real S051 record
— byte-for-byte the real entry's command. That failure (`exit=2`) held only pre-freeze, as recorded.
At the tip, the twin is rejected by (a) the fabricated-quote comparison above (exit 1), (b)
structural exclusion from the harness and reviewer scope (§4). Anyone citing "the twin's recheck
line fails" as the tip-time rejection would be wrong; the quote comparison is the mechanism.

### 4. The F17 entry review does not admit the junk bytes

- **Harness exclusion:** `python3 corpus/instruments/frontier-recheck-count.py` → 20 PASS lines
  ending `PASS F17 knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051`,
  `entries=20 pass=20 exit=0`. Entries are README-row-bound to `corpus/`-relative paths
  (`frontier-recheck-count.py:128-130`), so the twin under `.ufo/waves/round-34/c2-controls/` is
  structurally uncountable, not merely uncounted.
- **No junk bytes anywhere admitted:** `grep -r "defines five severity levels for smart-contract
  exploits" corpus/` → 0 matches; the twin's sentence exists only under `c2-controls/`.
- **Entry binding:** `grep -cE '^source: S051 '
  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` → `1`.
- **Non-author reviewer verdict, landed and read:**
  `.ufo/waves/round-34/wave1/RevEntryF17.md:147-152` — "**ADMIT.** The final bytes (`948b202e…`)
  satisfy Q1–Q10 on measured evidence…". Receipt header (`:8-14`): bytes reviewed =
  `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` sha256
  `948b202ebe1f32728a19d7bf2ead67911ba624d3699bde2dfd486f6725ac1d8a` (113 lines); capture pin
  re-opened `4fd8ed98…` (`:16-17`). Reply to my direct question (2026-10-26): review scope was
  exclusively those entry bytes, "the junk twin played no part in the ADMIT and is non-admissible
  by scope"; the ADMIT is digest-bound — any other bytes are not admitted by it. Consistent with my
  `reason=quote-not-found` exit 1.

## Findings

None blocking. Three precision notes for the L1:

1. **F1 (wording, no defect):** the claim sentence "junk twin … rejected by the admission gate
   (source-recheck exit != 0)" is true at the tip only via the twin-derived manifest
   (`reason=quote-not-found`, exit 1 — recorded above) or pre-freeze via manifest-missing (exit 2,
   recorded in `c1-controls/fake-controls-receipt.txt`). The twin's own committed `recheck:` line
   passes at the tip. Future readers should cite the quote-comparison mechanism.
2. **F2 (from RevEntryF17, echoed because my criterion rests on their verdict):** their receipt
   `:139-141` notes the author's first announced digest `e71fbcd9…` was superseded mid-review by
   `948b202e…`; the L1 must commit exactly `948b202e…` (measured digest in §1 matches).
3. **F3 (naming):** `r-defect-closure.sh:405-408` accepts the twin at either `c2-controls/` or
   `.ufo/waves/round-34/c2-controls/`; only the latter exists in this tree. The claim's
   "committed under c2-controls/" is satisfied by that path; pure naming precision.

## Residual risk / verification gaps

- The fixture manifest and builder lived only in scratch and are deleted with it; the receipt
  quotes full outputs, and the fixture is reproducible from §3 in one command.
- I did not re-verify RevEntryF17's Q1–Q10 measurements (their §Report carries them; my criterion
  was scope/admission of the junk bytes, which is proven by their digest-bound verdict + my greps).
- Scratch directory `/fast/scratch/hyaku/kasegi-r34/RevJunkTwin/` removed before yield (verified by
  the rm exit status in the session log; nothing under it remained).

Report: .ufo/waves/round-34/wave1/RevJunkTwin.md
