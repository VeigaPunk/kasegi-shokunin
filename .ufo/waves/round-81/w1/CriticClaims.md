# CriticClaims — round 81, attempt 1 (attack on C1 and C2)

Frozen bytes only: candidate `a3b58aa5…`, counter `fa96223b…`, table `abcc834e…`, entry gate
`51ee45fb…`, forgery driver `28fde387…`. Nothing under the lane was edited; every artifact below
was built in `/fast/scratch/hyaku/kasegi-r81/CriticClaims` and is copied into
`CriticClaims-receipts/`.

## Verdicts

| item | question | verdict | receipt |
|---|---|---|---|
| (a) | a cheaper forgery passes P3 under the r81 counter without assertions and without P2 | **FALSIFIED** (the claim's independence limb) | `mutbat-forgery.txt`, `forgery-selfdiff.py` |
| (b) | the R58 nominal clause names the non-moving metric | **NOT FALSIFIED** | `b-e-axis-and-corpus.txt` |
| (c) | a predicate P1–P8 is satisfiable by a junk edit | **FALSIFIED** (P1, P3, P5; P7 trivially) | `c-junk-predicates.txt`, `mutbat-junkedit.txt` |
| (d) | a worthless entry passes B0–B8 | **FALSIFIED** (B8's discriminating power) | `d-junk-entry.txt`, `junk-labelled.md` |
| (e) | a claimed clause restates admitted ground | **NOT FALSIFIED** | `b-e-axis-and-corpus.txt` |

Per claim: **C1 FALSIFIED** in its stated evidence — the axis_score and P4 parenthetical assert
"the kill tally's independence from the byte pin" and "the r81 tally rejects every forgery"; a
forgery that executes no assertion reaches `killed=56 … rc0`. The letter of P1–P8 is unaffected
(the five named forgeries still exit 1, and the frozen candidate a3b58aa5 is still killed 56/56),
so this is an evidence/axis defect, not a landing blocker.
**C2 NOT FALSIFIED** — the entry is real ground and passes B0–B8; (d) is a defect in the gate's
power, routed to r82, not a verdict change.

## (a) Cheaper forgery — FALSIFIED

Counterexample: `forgery-selfdiff.py` = the frozen candidate verbatim plus a 30-line driver. The
driver embeds the frozen 59-row table (zlib+base64, so no anchor appears literally), intercepts
`--selftest` before the candidate's `main` is reachable, and for every non-neutral row whose
anchor no longer occurs exactly once in its own source prints
`selftest case=<declared kill_cases> FAIL not-asserted`.

No assertion of the target executes. The candidate's 466-line selftest is dead text kept only to
carry the anchors; the whole "check" is a lookup in the counter's own expectation table. Neutral
rows need no special case beyond `class == "neutral"`, i.e. exactly the hint's "fires only on
rows whose transforms are not comments".

Receipt (`mutbat-forgery.txt`, the frozen P3 command against the forged target):

```
MUTBAT target_sha256=2900793870aec56906148a6c6a806079d00870e478c2c518944c5c1c5c9253ec baseline=ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3
rc=0
```

and the same file satisfies P1 literally:

```
$ python3 -B forgery-selfdiff.py --selftest
selftest cases=22 failures=0
rc=0
```

Why it works: `verdict()` in `mutbat.py:82` takes the target's own stdout as the kill signal,
and `kill_cases` travel in the table the author froze. The counter asks "did the target print a
FAIL naming the case I declared", which a target can answer by reading the declaration. Cost:
30 lines against a 466-line assertion set; the table is 5.6 KB compressed.

So P3 is independent of P2 and *dependent on the table*: it does not establish that the landed
bytes assert anything. The r81 counter moved the forgery problem from "the target can fake its
own success" to "the target can read the counter's expectations"; it did not remove it.

## (b) R58 nominal naming — NOT FALSIFIED

`corpus/instruments/resolve.py:304-313` collects `SKILL.md` plus `corpus/**/*.md` and skips
non-`.md`; `corpus/instruments/recheck-cwd-census.py` is never opened by the axis census.
`SCORECARD.md:33` and `:66` name `resolve.py`'s census of record
(`corpus/instruments/citation-survival.md`) as the depth:verifiability counter. The C1 claim names
that metric, says it does not read the instrument, and holds the score at 4. R58's clause — label
nominal, hold the score, name the non-moving metric — is satisfied.

Observation, not a defect: with R58 applied, an instrument round on this axis can never move the
axis, so the "measured move" the claim reports (the kill set) is internal to the instrument. That
is the sanctioned path, but it means the axis score stays 4 for structural, not substantive,
reasons.

## (c) Junk edits satisfy the predicates — FALSIFIED

Three stubs satisfy three predicates by their letter (`c-junk-predicates.txt`): a 3-line file that
prints `selftest cases=22 failures=0` passes P1; a 2-line file that prints a hardcoded
`RECHECK-CWD entries=… noprefix=0 …` and `conformant` passes P5; a 2-line file with one
`subprocess.run(`, one `"bash", "-c"` and no `/tmp` passes P7.

The decisive case is a **one-line junk edit to the frozen candidate**: after
`counts["entries"] += 1` insert `if name.startswith("osv-"): continue`. Then

- P1: `selftest cases=22 failures=0`, rc0 (the selftest fixtures are named `a-`, `b-`, `c-`… so no
  fixture is skipped; `recheck-cwd-census.py:323-503`);
- P3: `MUTBAT … killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 rc=0`
  (`mutbat-junkedit.txt`, target sha `55c24206…`);
- P5: `RECHECK-CWD entries=95 noprefix=0 exit2_foreign=0 exit_other=0 norecheck=0
  restoration_only=0` / `RECHECK-CWD-RESULT conformant`, rc0 — every field P5 pins is unchanged.

The edit silently deletes the recheck of six entries (every `osv-*` entry, including the new
S115 entry): the honest run prints `exit0_foreign=73`, the junk edit `exit0_foreign=67`, and no
predicate reads `exit0_foreign`. A junk edit that stops the census from running 6 of 95 rechecks
passes P1, P3 and P5 identically.

## (d) A worthless entry passes B8 — FALSIFIED (gate power)

`junk-labelled.md` is a header plus six `## Claim k` sections, each holding only the pinned quote,
the sentence "See above.", an empty `Falsifiable rule:` line and an empty
`Rejected over-generalization` line. It is indistinguishable from the landed entry to the gate:

```
ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 header=ok
ENTRY-GATE-RESULT pass
rc=0
```

Cause: `entry-gate.py:60` tests only the *presence* of the two prefixes
(`re.search(r"(?m)^Falsifiable rule:", body)`), never a sentence after them, so a 1.3 KB quote
dump with labels and no analysis passes. The gate's own selftest never exercises this path: its
`norule` fixture *deletes* `Falsifiable rule:` (`entry-gate.py:108`) instead of emptying it, and
the pre-freeze junk control (`controls/c2-junk-entry-r81.md`) is the *unlabelled* dump
(`claims=0`, `unpinned=6`), which fails only because it has no claim headers. B0–B7 are
bookkeeping (registry row, expected list, frontier census, capture binding) and are indifferent to
the prose, so a labelled dump reaches a landing that satisfies B0–B8.

The landed entry itself is substantive — six distinct clauses, each with a falsifiable rule and a
named rejected over-generalization — so this does not falsify the C2 statement. It falsifies the
reading that B8 is an entry-content limb: it is a shape limb.

## (e) Restatement of admitted ground — NOT FALSIFIED

`importfindings`, `source.yaml`, `home database`, `quality check`, `targeted to`,
`only parameter` and `quality bar` each match only the new entry across `corpus/knowledge/`; the
B6 literal sweep over the other 94 entries is 0/6. The one real overlap — the "still considered
experimental" sentence on S115.txt:32 and the case-sensitivity note on :39, both held by F51
(`corpus/knowledge/osv-post-v1-query-contract.md:31,75`) — is named under "Not claimed", appears
in no Claim section and no located span, and the entry cites F51's Limits bullet as the holder.
No claimed clause restates admitted ground.

## Impacted axes

- **depth:verifiability** (4, nominal): the round's stated evidence (a kill tally independent of
  the byte pin) does not hold. The score is held either way, so no score change is argued; what is
  at stake is what the tally may be cited for.
- **coverage** (8, held): C2's admission is unaffected; the defect is B8's power to certify
  content, which is the limb that will carry future entries.

## Smallest safe correction (route to r82; no frozen byte is edited)

1. **Counter**: count a row killed only when two limbs agree — the case-matched FAIL line *and*
   divergence of the target's real output from the baseline's on a counter-owned fixture root
   (expected counts in the counter, never in the target). One extra run per row over an existing
   fixture; closes self-report and table-embedding together.
2. **Entry gate**: require ≥ 8 words after `Falsifiable rule:` and after
   `Rejected over-generalization` that do not occur anywhere in the snapshot, and add a
   labelled-dump control (six Claims, empty rule lines) to `entry-gate.py --selftest`; the current
   `norule` case deletes the line instead of emptying it, which is why the gap survived the
   pre-freeze controls.

## Receipts (`CriticClaims-receipts/`)

`mutbat-forgery.txt`, `forgery-selfdiff.py`, `mutbat-junkedit.txt`, `candidate-junkedit.py`,
`c-junk-predicates.txt`, `p1-junk.py`, `p5-junk.py`, `p7-junk.py`, `d-junk-entry.txt`,
`junk-labelled.md`, `b-e-axis-and-corpus.txt`.

Tooling: nothing installed or upgraded. Scratch `/fast/scratch/hyaku/kasegi-r81/CriticClaims`
removed on exit.
