# MutJunkTwin — round-36 wave1 receipt (mutation-tester, coverage)

Seat: MutJunkTwin (leaf; no subagents spawned). Item: verify the junk twin control discriminates —
(a) junk with fabricated quote → source-recheck exit 1 quote-not-found; (b) junk with real quote but
wrong source → exit 1; (c) junk with real quote and real source (i.e., the real entry) → exit 0 only
for the real one. Judged on: coverage. Measured 2026-10-26T12:36–12:42Z (UTC 15:36–15:42Z).

## Method

Independent fixture in my scratch `/fast/scratch/hyaku/kasegi-r36/MutJunkTwin/fixture/` (lane repo
untouched; my only lane write is this receipt). Inputs copied with before-hashes:

| file | sha256 | provenance |
|---|---|---|
| corpus/instruments/source-recheck.py | `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` | landed lane bytes (matches the round-31 lesson's landed-instrument pin) |
| round-36 manifest.json | `f9590c2bbc26244af88dce8fa7c291d67e6138c293ba5198257789911c017da3` | ExecC2QuoteOnce scratch; byte-identical to ExecC2JunkControl `manifests/round-36-real.json` (same digest) |
| round-36 S053.txt | `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9` | identical across 4 sibling scratch copies (QuoteOnce, JunkControl, ScribeEntryF19, ScribeGateLesson), hashed at 12:38Z |
| round-35 S052.txt | `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826` | landed lane bytes (matches round-35 manifest pin) |
| round-35 manifest.json | `06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee` | landed lane bytes |

**Capture authenticity**: re-derived S053.txt from the fetched `epss.html` (26,804 B) using the landed
`capture-source.py` `html_to_text()` → sha256 `4ec61c59b0e9aedf…` exact match. The probe runs against
the real capture, not a stand-in.

**Junk twins constructed independently in my scratch** (fabricated sentence taken from
ExecC2JunkControl's twin `junk-f19.md`, which I read for fidelity; constructions are mine):
- `junk-a.json` (sha `8d6efbb28a113f5388c44103c65304d42806509743f5171613c60a57e0c34711`): record id
  S053 → real S053.txt (sha OK) asserting the FABRICATED sentence
  `EPSS guarantees exploitation within 30 days for every scored CVE.`
- `junk-b.json` (sha `2c6a927d0a994d4b0ddc999652721f7527a64986b548845d7fafe49735857fe9`): record id
  S052 → real S052.txt (sha OK) asserting the verbatim REAL S053 L216 sentence (wrong-source binding).
- `junk-c-stem.json` (sha `8f8a20715de72d5d90631fd558d9c797cb205b88f854a24e5f7f425806cbe332`,
  supplementary): record id S052 → path S053.txt (stem mismatch path).
- `combined.json` (sha `cf5061e8e04d17d535a4c650e091de3b44b6f7a1f2d3b33bad19b95518cefb22`): the real
  S053 record verbatim + the junk S052 record in one manifest.

## Discriminating invocation (build-spec form, over the real capture)

```
grep -cF 'EPSS guarantees exploitation within 30 days for every scored CVE.' S053.txt  -> 0
grep -cF 'guarantees' S053.txt                                                        -> 0
grep -cF '(EPSS) is a data-driven machine-learning model that estimates the probability' S053.txt -> 1
grep -cF 'EPSS is maintained by the EPSS Special Interest Group at FIRST' S053.txt    -> 1
```

The fabricated sentence (and even its verb) occurs nowhere in the capture; both real spans occur
exactly once.

## Matrix results (source-recheck.py, landed digest `fd2e01e8…`, run on fixture copies)

| variant | command (cwd = fixture root) | output | exit | verdict |
|---|---|---|---|---|
| (c) pristine | `source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053` | `S053:sha256 OK`; Q1–Q4 `OK occurrences=1` anchors `216-ok`/`217-ok`/`217-ok`/`235-ok` | **0** | PASS — the real one passes |
| (c) pristine, full manifest (no `--source`) | same manifest, no selection | identical 4 OK lines | **0** | PASS |
| (a) fabricated quote, real source | `--manifest …/round-36/junk-a.json --source S053` | `S053:sha256 OK`; `S053:QJ1 MISMATCH reason=quote-not-found` | **1** | **KILLED** — matches item prediction exactly |
| (b) real quote, wrong source | `--manifest …/round-35/junk-b.json --source S052` | `S052:sha256 OK`; `S052:QJ1 MISMATCH reason=quote-not-found` | **1** | **KILLED** — matches item prediction (exit 1) |
| (b2) wrong-source twin's own recheck line as written | `--manifest …/round-36/manifest.json --source S052` | `S052:source UNAVAILABLE reason=not-listed` | **2** | rejected, but exit 2 not 1 (see observation 2) |
| (b3) stem-bound supplementary | `--manifest …/round-36/junk-c-stem.json --source S052` | `S052:manifest MISMATCH reason=stem-mismatch` | **1** | KILLED via the B1 stem binding |
| combined per-record | `--manifest …/source-snapshots/combined.json` | `S052:QJ1 MISMATCH reason=quote-not-found` AND all four `S053:Q* OK` lines | **1** | only the real record passes in the same run |

In every junk variant the `sha256 OK` line shows the failure is isolated to the quote-vs-capture
comparator (or stem binding), not to a corrupted capture — the discrimination is the quote pin, as
designed.

## Verdict

**The junk twin control discriminates.** Both junk variants are killed (exit 1 each, with the item's
stated `quote-not-found` reason for (a) and for the capture-bound construction of (b)); the real
record is the only one that passes (exit 0, reproduced twice with identical output). No surviving
mutant; no baseline failure (the pristine run is green, so the kills are conclusive).

## Boundary observations (coverage findings; no contract change proposed)

1. **The twin file's own recheck line is not the gate.** `junk-f19.md`'s recheck line names the REAL
   recheck (`--source S053`) and exits 0 — the twin's own comment concedes this ("it names the real
   recheck of S053, so it cannot itself be the gate"). The rejection lives in asserting the twin's
   quote against the capture: my junk-a construction (the control receipt's pinned comparison) and
   the grep count. Consequence: a junk entry that copies the real header + real recheck line passes
   source-recheck and would pass the harness binding; only the body-quote-vs-capture comparison
   rejects it. Consistent with M31-4 (the counters cannot see a fabricated capture). The control is
   sound as designed; this just states where its gate lives.
2. **Exit-class nuance on (b).** The wrong-source twin's literal recheck line fails with exit 2
   (`not-listed`), not exit 1; the item's exit-1 reading is realized by the capture-bound construction
   (junk-b: real quote asserted against S052.txt → `quote-not-found`, exit 1). Both are rejections;
   recorded so the control receipt quotes the intended construction.
3. **DEFECT in the real entry draft (variant (c) identification).** ScribeEntryF19's
   `epss-exploit-prediction-scoring.md` (sha256 `27a4d42abc070b98d4aabe112ba06bda8cac5c1aaaa2b7216fd5508f199c2816`,
   17,267 B, read 12:41Z) pins the capture hash as `4ec61c59b0a9aedf…` in **2 places** — one-hex-digit
   drift at position 10 (`b0a9` vs `b0e9`) vs the manifest/capture `4ec61c59b0e9aedf…`; the correct
   hash appears nowhere in the draft, and it is not the epss.html hash (`66fece52…`) either. The
   entry's other inline facts check out (244 lines, 8448 bytes, URL). source-recheck is immune (it
   reads the manifest), so the matrix verdicts stand — but the entry's inline evidence line is
   currently false, the exact defect class the junk control exists to catch. Peer-messaged
   ScribeEntryF19 at 15:42Z to fix before landing. The draft is moving (ExecC2QuoteOnce's landed
   receipt pinned an earlier digest `75f63bc2…`); re-check the then-current draft before scoring.
4. `c2-controls/before.txt` `junk_present=1` ambiguity: already adjudicated by
   `wave1/ExecRegressionBase.md` F6 (not reproducible from committed base bytes; L1 to pin the
   definition). Cited, not re-litigated.

## Restoration / state evidence

- No lane-repo writes outside this receipt: `git status --porcelain` line count 9 at my first
  observation (12:36Z) and 9 at 12:41Z (the wave's own files; wave is live, count reflects my
  observation instants). No mutating git/jj command run anywhere.
- Fixture tree sha256 snapshot taken after the junk runs equals the final snapshot
  (`TREE-UNCHANGED` diff) — instrument runs mutated nothing; pristine re-run after all junk runs
  exit 0 with byte-identical output (restoration evidence for the pristine/mutated/restored triad).
- Scratch `/fast/scratch/hyaku/kasegi-r36/MutJunkTwin/` removed before yield; all evidence is quoted
  in this receipt.
- Tooling: nothing installed or upgraded (no need; pacman untouched).

## Replay (from a fixture root with the same relative layout)

```
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053   # exit 0
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/junk-a.json --source S053      # exit 1 quote-not-found
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/junk-b.json --source S052      # exit 1 quote-not-found
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S052    # exit 2 not-listed
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/junk-c-stem.json --source S052 # exit 1 stem-mismatch
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/combined.json                           # exit 1, S053 OK + S052 MISMATCH
```

Artifact: `.ufo/waves/round-36/wave1/MutJunkTwin.md`.

## Addendum — finding 3 closed by the author (2026-10-26T15:44Z)

ScribeEntryF19 confirmed the one-nibble pin drift I reported, re-derived the hash from the capture
bytes embedded in `ExecC2Capture.md` §6 before changing anything, and fixed all four occurrences.
Verified by me in the landed receipt `wave1/ScribeEntryF19.md`: correct form `b0e9aedf` ×6; the wrong
form `b0a9aedf` survives only as meta-mention — the V11 row's negation ("no pin in this receipt
carries the former `b0a9aedf` form") at :73 and the §5 correction quoting it as the error at :116 —
no live pin carries it. The entry draft was removed from their scratch and is **not yet landed** in
`corpus/knowledge/` at my 15:44Z check; whoever scores the F19 cell should confirm the landed entry
carries only `b0e9aedf` (one grep: `grep -c 'b0a9aedf' corpus/knowledge/epss-exploit-prediction-scoring.md`
→ 0). Author also re-measured post-fix: 11 blockquotes all occurrences=1, max 25 words, anchors 11/11,
recheck `bash -n` rc=0. Matrix verdicts above are unaffected (source-recheck reads the manifest).
Verified 15:46Z that the staged deliverable is clean: the entry text sits verbatim in
`wave1/ScribeEntryF19.md` §6 (marker at :138) and its `source:` line (:143) carries only the correct
`b0e9aedf` form; the wrong form appears solely at :73 (V11 negation) and :116 (§5 correction quote).
The landed-file grep at integration is therefore a formality, not an open risk.
