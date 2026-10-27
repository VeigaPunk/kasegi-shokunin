# ScribeLesson — receipt (kasegi round 41, wave 1 `kasegi-r41-build`)

Role: `scribe`. Assignment: draft the `corpus/lessons/round-41.md` skeleton (deliverable
`ScribeLesson.lesson.md`) with the frozen-claims table, mistake row M41-1, census/gate/wave-2
placeholders, and ScribeC2Gate's gate block spliced verbatim.

## Deliverable

- `.ufo/waves/round-41/wave1/ScribeLesson.lesson.md` — **73 lines, 6,565 B**, sha256
  `2f54ae0ac5c3360fa43f5b4c1dfd5e70f79cadb7ea216833f159fec86b102664`.
- Section order (headings at column 0): `# Round 41 — kasegi` (L1), `## Frozen claims` (L15),
  `## Mistakes` (L24), `## Census` (L30), `## Gate` (L37), `### Admitted — F24 / S063 (RFC 9116
  security.txt)` (L39, inside the spliced block), `## Wave-2 falsification` (L70). `## Gate` appears
  exactly once — round-40's D4 defect (`## Gate` at both L29 and L31) is not reproduced.
- Shape audit of the landed bytes: claim rows 2, mistake rows 1, `## Gate` headings 1, capture tokens
  6 × `<<<CAPTURE>>>` + 3 × `<<<CAPTURE:Lnnn>>>`, other placeholders `<<<CENSUS-AFTER>>>`,
  `<<<WAVE2-TALLY>>>`, `<<<WAVE2>>>`, `<<<WAVES>>>`, zero occurrences of the unresolvable base string
  and two of the canonical base hash.

## Gate block splice (peer `ScribeC2Gate`)

- Source `.ufo/waves/round-41/wave1/ScribeC2Gate.gate-block.txt` — 30 lines, 2,585 B, sha256
  `9b42ce0b920213733da01f55f4c09df78728bc0918a38e3dd089f9c511d83fa3` (matches the sha256 the peer
  messaged).
- Splice check: `sed -n '39,68p' ScribeLesson.lesson.md > spliced.txt; cmp spliced.txt
  ScribeC2Gate.gate-block.txt` → identical; `sha256sum` of the extracted region =
  `9b42ce0b…d83fa3`, i.e. byte-exact. The block carries no `## Gate` heading, so exactly one was
  added; the 9 unresolved capture tokens were preserved byte-exact, not filled.

## Commands run (actual output, read-only git)

```
$ git rev-parse 5b29ea1
5b29ea1439450b712581edf5f0f0bf98dfb262ab
$ git cat-file -t 5b29ea1439450b712581edf5f0bf98dfb262ab
fatal: Not a valid object name 5b29ea1439450b712581edf5f0bf98dfb262ab
catfile-exit=128
$ git rev-parse 5b29ea1439450b712581edf5f0bf98dfb262ab; echo len
38                      # the claims/dispatch string: 38 hex chars, unresolvable
$ git grep -c '^Correction (round 41)' fbba3d96cdf8d37c1ea41304a1ba35691329684b --
(no output) grep-exit=1  # I1 limb red at the claims freeze, 0 matching lines
$ git grep -c '^Correction (round 41)' b3b08b2 -- | wc -l
0                        # still red at the dispatch commit
$ git grep -n '^## Gate' fbba3d96:corpus/lessons/round-40.md
fbba3d96:corpus/lessons/round-40.md:29:## Gate
fbba3d96:corpus/lessons/round-40.md:31:## Gate   # D4 defect, not copied
$ git ls-files .ufo/waves/round-40/wave2/{RevC1Counters.defeats.txt,CritKillRule.md,MutH6H10.md}
.ufo/waves/round-40/wave2/CritKillRule.md
.ufo/waves/round-40/wave2/MutH6H10.md
.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt   # all three tracked = committed evidence
```

Wave-1 attack tally, computed from `.ufo/waves/round-41/wave1-dispatch.json` (`registry.members`, 60
`spawn` records, `counts.spawn=60`):

```
executor 17, scout 11, reviewer 9, scribe 6, critic 6, mutation-tester 5,
connector 2, sentinel 2, simplifier 1, revenger 1
attack = reviewer 9 + critic 6 + mutation-tester 5 = 20/60 = 33.3%
```

The lesson states that wave-1 figure and leaves wave 2 / round total as `<<<WAVE2-TALLY>>>` rather
than estimating (round-40 M/D5 was an estimated-and-wrong tally: the lesson said 33/35 and 50/89
where the dispatch showed 25/35 and 42/89).

## Provenance used

- `claims.json` (frozen 2026-10-27T09:05:00Z by KasegiR41): C1 depth:verifiability (4, held), C2
  coverage (8, held); judged-head rule reproduced (J = every round-41 change except the receipt, Y = J
  + `.ufo/waves/round-41/final-gates/all-gates.txt`; lane files never name J; counting commands at Y,
  negative controls at base and round-40 judged head `c7aea5ef97902f38289cbdc1cf267068876a62dd`).
- Before values: `c1-controls/do-nothing.txt` (`bash: corpus/instruments/r41-closure.sh: No such file
  or directory`, `exit=127`, "suite absent"), `c2-controls/before.txt` (frontier 23 / F24 0 / registry
  62 / S063 0 / entries 0 / knowledge 59 / queued 0 / admitted 23 / harness 26/26 / binding 54/54 /
  expected=59 / census baseline), `census-before.txt` (`W04 S028`, `W04 S029`, `ok`, `exit=0`).
- M41-1 evidence: `corpus/lessons/round-40-verifier-spotcheck.md` §5 D1 (routed defect text quoted:
  "C1 graded 'verified' while its frozen kill rule fires"), plus the committed
  `RevC1Counters.defeats.txt` (T2 substring `closed=7/80`/`failures=10` green, T4 fenced pseudo-table
  green, T7 symlink out-of-export green, T13 mention-only row green, T14 `Kasegi-R40-stray` /
  `kasegi_r40-stray` green — `RevC1Counters.defeats.txt` L9, L13, L22, L46, L52-L53),
  `CritKillRule.md`, `MutH6H10.md`.

## Conflicts (reported verbatim, not edited)

1. **Base commit hash is corrupt in the frozen inputs.** The assignment, `claims.json:5`
   (`"base": "5b29ea1439450b712581edf5f0bf98dfb262ab"`, 38 hex chars) and
   `c1-controls/do-nothing.txt` L1-L2 all carry `5b29ea1439450b712581edf5f0bf98dfb262ab`, which
   `git cat-file -t` rejects (`fatal: Not a valid object name`, exit 128). The resolvable lane commit is
   `5b29ea1439450b712581edf5f0f0bf98dfb262ab` (`git rev-parse 5b29ea1`, `git rev-parse HEAD~2` — the
   claims string dropped the `f0` before `bf98`). The deliverable uses the **resolvable** hash in both
   places and this receipt records the claims string as-is. Consequence for C1: the control transcript
   was produced while the suite was absent (`exit=127`), so it never resolved the ref; once the suite
   lands, the base negative control must be run against a resolvable hash, otherwise git's
   revision-resolution failure mimics the required red and I10/I12 would be green for the wrong reason.
2. `claims.json` C1 counting command 3 quotes the same 38-char string
   (`--export-ref 5b29ea1439450b712581edf5f0bf98dfb262ab`); the frozen claim text is the authority for
   C1 seats, so this is reported, not changed.

## Known limits

- The gate block's fetch facts (`<<<CAPTURE>>>` ×6) and quote line anchors (`<<<CAPTURE:Lnnn>>>` ×3)
  are left for the L1 to fill from ExecC2Capture's manifest record; this seat spliced the peer's bytes
  and did not re-verify the RFC 9116 fetch or the ≤25-word quote matching (ScribeC2Gate's lane).
- `## Census` after-state is `<<<CENSUS-AFTER>>>`; `## Frozen claims` after-columns record the declared
  after-state, not an observed one — the observation lands post-integration.
- `## Wave-2 falsification` is a placeholder with the counting rule stated; no wave-2 verdict is
  asserted.
- No tooling installed; no network fetch; no mutating git/jj command; writes limited to this receipt,
  the deliverable, and scratch (removed at yield).

## Scratch

Work copy at `/fast/scratch/hyaku/kasegi-r41/ScribeLesson/` (draft, final, spliced extract); removed at
yield.
