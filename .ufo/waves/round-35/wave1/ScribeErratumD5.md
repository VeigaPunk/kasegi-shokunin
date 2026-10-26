# ScribeErratumD5 — D5 claims erratum (round 35, wave 1)

**Status: delivered.** The D5 erratum is written at
`.ufo/waves/round-35/claims-erratum-d5.md` and both required literals are present.
It corrects the round-34 C2 frozen-predicate wording by restatement, with both
restated clauses exercised by execution against committed bytes. No product file,
frozen claim, judge, or sibling lane was edited.

Tree at work: lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, git HEAD
`da2d3c687f82a9814ee71c91c930cb733050d37c` (round-35 wave-1 dispatch), claims freeze
`617496b9c6e92bc671e7e78b83df69a04470d0e9`, `python3 3.14.8`.

## Report

### 1. Inputs read (and what each supplied)

| path | supplied |
|---|---|
| `corpus/lessons/round-34-verifier-spotcheck.md:107,141,189-194` | D5 as routed: the two clauses and the "future twins carry only absent sentences" fix |
| `.ufo/waves/round-34/claims.json` (C1 and C2) | the frozen C2 `predicate`, `after[3]`, `after[6]`, `kill_rule`, plus the C1 `after[10]` twin sentence, all quoted in the erratum |
| `.ufo/waves/round-34/wave1/RevClaimsFreeze.md:172-181` | D-2: measured 16×`occurrences=1`, Q9/Q17 `occurrences=2` anchored; recommended rewording |
| `.ufo/waves/round-34/wave1/RevJunkTwin.md:53-106,153-160` | the quote-comparison route and its measured outputs; F1 wording note |
| `corpus/lessons/round-34.md:195-227` | both readings of the junk-twin dispute, reproduced verbatim |
| `.ufo/waves/round-34/c2-controls/junk-f17.md` | the mixed control: its `recheck:` line (line 11) and its fabricated sentence |
| `corpus/QUALITY.md:64` | Q9: exactly-once **or** a verified `anchor`, and the observed count printed |
| `corpus/instruments/source-recheck.py` | `anchor_verdict` / B2 semantics: non-unique without verified anchor fails |
| `corpus/instruments/README.md` | instrument spelling and the round-24 occurrence/anchor changes |
| `.ufo/waves/round-35/claims.json` | round-35 C1 after-state wording for D5, and the C2 recurrence |
| `.ufo/waves/round-35/c2-controls/junk-f18.md`, `corpus/source-snapshots/round-35/S052.txt` | round-35 twin sentences and read-time capture (see §6 limit) |
| `.ufo/waves/round-34/claims-erratum-1.md` | the appended-erratum form this file follows |

### 2. The frozen text, located exactly

- Round-34 `claims.json` C2 `predicate`: "…source-recheck S051 prints every
  assertion occurrences=1, sha256 OK, exit 0; … the junk F17 twin
  (c2-controls/junk-f17.md) is rejected by the admission gate."
- `after[10]` **of C1** (not C2 — verified by enumerating both lists in Python;
  the sentence is a C1 closure item, R9): "junk-twin control committed under
  c2-controls/ and rejected by the admission gate (source-recheck exit != 0;
  reviewer REFUSE) (R9)"
- C2 `after[3]`: "source-recheck S051 exit 0, every assertion occurrences=1, sha256
  OK"
- C2 `after[6]`: "junk twin rejected: source-recheck exit != 0 and non-author reviewer
  REFUSE on record"
- C2 `kill_rule`: "…source-recheck S051 exit != 0; … junk twin passes source-recheck
  or is admitted."

The round-35 C2 repeats all of these phrasings (`predicate`, `after[3]`, `after[6]`),
which the erratum discloses in §5 rather than editing.

### 3. Execution battery

Scratch root `/fast/scratch/hyaku/kasegi-r35/ScribeErratumD5/` (created with
`os.makedirs`, removed in `finally:`). All runs from the lane root unless noted.
The capture used for byte-stable fixtures was the **committed blob**, extracted as
`git show HEAD:corpus/source-snapshots/round-34/S051.txt`; its sha256 equals the
round-34 manifest pin (`4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5`).

**A1 — the twin's own `recheck:` line (the frozen phrase's only on-disk form).**
Command: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051` — **exit 0**. Output:

```
S051:sha256 OK
S051:Q1 OK occurrences=1 anchor=46-ok
S051:Q10 OK occurrences=1 anchor=79-ok
S051:Q11 OK occurrences=1 anchor=83-ok
S051:Q12 OK occurrences=1 anchor=88-ok
S051:Q13 OK occurrences=1 anchor=92-ok
S051:Q14 OK occurrences=1 anchor=94-ok
S051:Q15 OK occurrences=1 anchor=90-ok
S051:Q16 OK occurrences=1 anchor=95-ok
S051:Q17 OK occurrences=2 anchor=96-ok
S051:Q18 OK occurrences=1 anchor=99-ok
S051:Q2 OK normalized=markup-whitespace occurrences=1
S051:Q3 OK occurrences=1 anchor=52-ok
S051:Q4 OK occurrences=1 anchor=52-ok
S051:Q5 OK normalized=markup-whitespace occurrences=1 anchor=53-ok
S051:Q6 OK normalized=markup-whitespace occurrences=1 anchor=55-ok
S051:Q7 OK occurrences=1 anchor=74-ok
S051:Q8 OK occurrences=1 anchor=75-ok
S051:Q9 OK occurrences=2 anchor=77-ok
```

**A2 — the instrument pointed at the twin file (a non-manifest).** Command:
`python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-34/c2-controls/junk-f17.md --source S051` — **exit 2**:

```
manifest UNAVAILABLE reason=unreadable-or-invalid
```

**B1 — the discriminating invocation.** A scratch manifest pinning the committed
capture's sha256 and carrying the twin's fabricated sentence
`five severity levels for smart-contract exploits` as its single assertion
`J1`. Command: `python3 corpus/instruments/source-recheck.py --manifest <scratch>/m_junk.json --source S051` — **exit 1**:

```
S051:sha256 OK
S051:J1 MISMATCH reason=quote-not-found
```

**B2 — control, same invocation shape, a quote the capture holds** (`At Immunefi,
we classify bugs on a simplified 5-level scale:`, `anchor: 46`) — **exit 0**:

```
S051:sha256 OK
S051:Q1 OK occurrences=1 anchor=46-ok
```

**C1 — per-id: a non-unique quote with a verified anchor passes.** Assertions
`Q9` (`Permanent freezing of funds`, `anchor: 77`) and `Q1` — **exit 0**:

```
S051:sha256 OK
S051:Q1 OK occurrences=1 anchor=46-ok
S051:Q9 OK occurrences=2 anchor=77-ok
```

**C2 — per-id: the same non-unique quote with no anchor fails** — **exit 1**:

```
S051:sha256 OK
S051:Q9 MISMATCH reason=occurrence-not-unique
```

**C3 — per-id: a declared anchor that does not hold fails** (`anchor: 1`) — **exit 1**:

```
S051:sha256 OK
S051:Q9 MISMATCH reason=anchor-broken
```

**D1 — the instrument's own spelling.** `python3 corpus/instruments/source-recheck.py
--selftest` — **exit 0**, last line `selftest cases=10 failures=0`; the ten cases
include `double-occurrence`, `double-occurrence-anchored`,
`double-occurrence-out-of-range`, `double-occurrence-broken`, `quote-absent`.

**E1 — round-35-shaped discriminating invocation** (read-time capture, see §6).
Scratch manifest pinning `corpus/source-snapshots/round-35/S052.txt`
(sha256 `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`) with
junk-f18's sentence `five exploited vulnerabilities to the catalog every Tuesday`
as `J1` — **exit 1**:

```
S052:sha256 OK
S052:J1 MISMATCH reason=quote-not-found
```

**N1 — normalized occurrence counts** (the instrument's `normalize`: whitespace
collapsed, `<u>`/`</u>` stripped), run in Python over the captures:

```
round-34 S051: 'Direct theft of any user funds' -> 1
round-34 S051: 'five severity levels for smart-contract exploits' -> 0
round-35 S052: 'five exploited vulnerabilities to the catalog every Tuesday' -> 0
round-35 S052: 'scores each entry with a CVSS v4 vector rather than a due-date' -> 0
```

### 4. Literal verification (assignment gate)

```
$ grep -c 'discriminating invocation' .ufo/waves/round-35/claims-erratum-d5.md
5
$ grep -c 'per-id occurrences' .ufo/waves/round-35/claims-erratum-d5.md
5
```

Both `>= 1` as required. In the submitted erratum the occurrences are at lines 70,
75, 77, 199 for the first literal and 140, 163, 183, 202 for the second (the
verification block's own command lines at 239/241 excluded). The counts do not
depend on those line numbers; the grep output above is the gate.

### 5. How the erratum answers the assignment

- (1) The junk-twin phrase is restated with a discriminating invocation: the twin's
  own sentence, pinned in a manifest against the committed capture, must print
  `MISMATCH reason=quote-not-found` at exit != 0, while the same invocation shape on
  a present quote exits 0. §2 of the erratum records the two non-discriminating
  routes (A1 exit 0; A2 exit 2 for any non-manifest) with outputs. §3 carries the
  literal and one reproducible construction.
- (2) "Every assertion occurrences=1" is replaced by a per-id occurrences
  restatement: one line per assertion carrying its own count and anchor note; unique
  quotes need no anchor; non-unique quotes pass only with a verified anchor;
  unanchored/broken non-unique quotes fail. Backed by A1 plus C1/C2/C3. The kill
  rule is stated as unaffected (it keys exit != 0, measured 0).
- (3) Future twins carry only absent sentences: §6 of the erratum states the rule
  and measures round-34's mixed twin (1 present / 0 absent) against round-35's clean
  twin (0 / 0).
- §5 of the erratum discloses that round-35's frozen C2 repeats both phrasings and
  applies the restatements by reference without editing the freeze.
- §8 states non-effects: no score change (C2 held 7), no adjudication, no claim on
  round-35 after-states.

### 6. Findings for the L1 (not verdicts on the round)

1. **The frozen twin clause is non-discriminating by execution, not only by
   reading.** A1 exits 0; A2 exits 2 for any non-manifest. The only executable form
   is the quote comparison (B1), which the erratum now carries. This confirms D5's
   wording point and RevJunkTwin's fact separately.
2. **The occurrences clause is false for 2 of 18 committed assertions** (Q9/Q17,
   `occurrences=2` with anchors 77/96). The instrument's per-id output is the
   evidence; the erratum's ruled reading keeps the kill rule intact.
3. **Round-35's C2 repeats all the phrasings** (`predicate`, `after[3]`,
   `after[6]`). Any SCORECARD/lesson text quoting those sentences this round should
   cite `claims-erratum-d5.md` §4-§5 so the recurrence is disclosed rather than
   repeated unqualified.
4. **Round-35's junk twin conforms to the forward rule**: both of its quoted
   sentences are absent from S052 under the instrument's normalization (0/0), unlike
   round-34's mixed twin (one sentence real). No action needed on the control.
5. **Ordering observation, not a defect**: at read time `corpus/source-snapshots/round-35/`
   is untracked and carries only `S052.txt` — `manifest.json` did not exist yet, so
   no S052 per-id occurrences run exists from this seat. The erratum therefore
   claims no round-35 after-state; the gate seats own those measurements.
6. **`source-recheck --selftest` is stronger than the round-34 receipts recorded**
   (`cases=10 failures=0`, including the four double-occurrence limbs). The erratum
   cites that spelling; no README drift found in the sections read.
7. **Claim-location correction (precision, no score effect)**: the sentence
   "(source-recheck exit != 0; reviewer REFUSE) (R9)" is C1 `after[10]`, not a C2
   field — enumerating both lists in Python is how this was found, after a first
   draft cited it as C2 `before[10]`. D5 is still correctly filed as a C2 predicate
   defect (the C2 `predicate`/`after[3]`/`after[6]`/`kill_rule` carry the twin and
   occurrences clauses); the erratum's §1 table now names the owning claim for each
   quoted sentence.
8. **The admitted entry already uses the honest phrasing.** Its `recheck:` comment
   (`corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md:6`) states "18
   assertions (Q1-Q18) … each `occurrences=1` or anchored (Q9/Q17)". The frozen
   predicate's "every assertion occurrences=1" therefore contradicts the entry it
   admits, so the erratum fixes the claim's wording, not the entry. Also corrected
   during the review: the twin's `recheck:` line is not byte-identical to the
   entry's (it lacks the entry's `cd` prefix and trailing comment) but targets the
   same manifest and `--source S051`, which is what makes it exit 0.

### 7. Limits (measured or declared, not inferred away)

- The B1/B2/C1/C2/C3/E1 fixtures existed only in scratch and are deleted; each is
  reproducible from the construction in the erratum §3 plus the digests here, but no
  fixture bytes survive this seat.
- E1 ran against the working-tree S052 capture, **untracked at read time**
  (`git status` listed `?? corpus/source-snapshots/round-35/`). The digest above pins
  the bytes I read; it is not a claim about what the L1 commits.
- The A2 route is stated as "any non-manifest exits 2": I measured it on the twin
  `.md` only. The generalisation rests on `load_manifest` rejecting non-JSON
  (`reason=unreadable-or-invalid`) before any per-twun comparison — code path read,
  not a second fixture run.
- I did not run the r35 closure suite, harness, census, or any gate; those belong to
  other seats. Nothing here verifies C1 or C2 after-states.

### 8. Files written / digests

| path | sha256 | size |
|---|---|---|
| `.ufo/waves/round-35/claims-erratum-d5.md` | `eee0bb579844ad9d02777fb4cd241e726d0bb0630679bc41aa534d7f5d0951e6` | 262 lines / 13,086 bytes |
| `.ufo/waves/round-35/wave1/ScribeErratumD5.md` (this receipt) | recorded by the L1 at commit | — |

Revision note: `RevD5D6D7` verified erratum bytes `2f4fae0a…` (262 ln / 13,078 B;
"byte-identical" already 0, literals 5/5). Three wording-level edits followed that
review — the reproduction snippet now uses `S="$(mktemp -d)/S051"` instead of a seat
scratch path, the `quote-not-found` sentence reads "the rejection the frozen kill
rule presupposes", and §5 reads "the same phrasings verbatim" — so the bytes to
commit are `eee0bb57…` (262 ln / 13,086 B). No measured value, literal, or finding
changed in those edits; the reviewer was told the new digest.

Inputs pinned by digest during the work: round-34 capture
`4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5`; round-34 twin
`2752a994265a1e284ebd236730d169d677e1923cfb7073cf79ad874d19bc4026`; round-35 twin
`0abec3591e4a2dc5195b23b1c2c920f66052327b7f971aa578af76c3459dc176`; round-35
capture (read-time, untracked)
`d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`.

No other lane file was modified by this seat. Scratch
`/fast/scratch/hyaku/kasegi-r35/ScribeErratumD5/` was removed in a `finally:` block
(`scratch_removed: True` printed after each run); nothing under it remains.

Report: .ufo/waves/round-35/wave1/ScribeErratumD5.md
