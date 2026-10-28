# ScribeLesson — receipt (kasegi round 42, wave 1 `kasegi-r42-build`)

Role: `scribe`. Assignment: draft the `corpus/lessons/round-42.md` skeleton (deliverable
`ScribeLesson.lesson.md`) — header with `<pending>` where unknowable, frozen-claims table, two
mistake rows (M42-1 evidence-union, M42-2 token-boundary), census before → after, `## Gate`
placeholder, the wave-shape paragraph (two v1 waves, connector seats in both — D-r41-5), and the
`## Wave-2 falsification` placeholder.

## Deliverable

- `.ufo/waves/round-42/wave1/ScribeLesson.lesson.md` — **53 lines, 6,668 B**, sha256
  `65895c42a34d0daa40e4bdfeefb900a26ab18119f6cc4a4064f4199aab45d8f9`.
- Section order (headings at column 0): `# Round 42 — kasegi` (L1), `## Frozen claims` (L18),
  `## Mistakes` (L27), `## Census` (L34), `## Gate` (L42), `## Wave-2 falsification` (L49).
  `## Gate` appears exactly once (round-40's D4 duplicate-heading defect is not reproduced).
- Shape audit of the landed bytes: claim rows 2 (`| C1 |`, `| C2 |`), mistake rows 2
  (`| M42-1 |`, `| M42-2 |`), `## Gate` headings 1, `<pending>` 9 occurrences on 8 lines.

Placeholder inventory (all filled by the L1 / later waves, never by this seat):

| Line | `<pending>` slot | Filled by |
|---|---|---|
| 5 | judged head J hash | L1 at integration (a commit cannot contain its own hash) |
| 6 | verification ref Y hash | L1 after the receipt lands at Y |
| 11 | wave-2 seat count + round total | wave-2 dispatch when it lands |
| 12 | wave-2 connector count | wave-2 dispatch |
| 16 | wave-2 attack share + round total | wave-2 dispatch |
| 31 | round-42 QUALITY criterion id (M42-1 captured-by) | ScribeQuality's landed append (see Conflict 1) |
| 37 | census after-state | L1 at round end |
| 44 | `## Gate` body | ScribeC2Gate's `ScribeC2Gate.gate-block.txt`, spliced verbatim |
| 51 | `## Wave-2 falsification` body | wave 2 |

## Provenance — commands run (actual output, read-only)

```
$ git cat-file -t 5053a7f46de35784cff4b56756906e9014a38276
commit
$ git rev-parse 5053a7f46de35784cff4b56756906e9014a38276
5053a7f46de35784cff4b56756906e9014a38276
$ git cat-file -t 1f7464612ac4c44e39886b82e812610d3c039b13
commit
$ git log --format='%h %cI %s' -3 -- .ufo/waves/round-42/claims.json
0566bd6 2026-10-28T08:00:01-03:00 round-42: frozen claims + controls + wave-1 spec/dispatch
$ git rev-parse 0566bd6
0566bd66e93d429b2df8b6751cf10cbdc391e79b
$ git merge-base --is-ancestor 5053a7f46de35784cff4b56756906e9014a38276 0566bd66e93d429b2df8b6751cf10cbdc391e79b; echo ancestor-exit=$?
ancestor-exit=0
$ git diff --name-only 5053a7f46de35784cff4b56756906e9014a38276 0566bd66e93d429b2df8b6751cf10cbdc391e79b | wc -l
9
$ git rev-parse HEAD
0566bd66e93d429b2df8b6751cf10cbdc391e79b
```

The header therefore carries a **resolved** base (`5053a7f…`, the round-41 verifier spot-check commit)
and a **resolved** claims-freeze commit (`0566bd6…`, the commit that added
`.ufo/waves/round-42/claims.json` and the controls); J and Y are `<pending>` because no round-42
judged head or receipt exists at this seat's read. Unlike round 41, the base string in `claims.json`
is 40 hex chars and resolves — the r41 corrupt-base conflict does not recur.

Wave tally and attack share, counted from `.ufo/waves/round-42/wave1-dispatch.json`
(`registry.members`, an object keyed by seat name; `counts.spawn` 64):

```
$ jq -r '(.registry.members // {})[] | .role' .ufo/waves/round-42/wave1-dispatch.json | sort | uniq -c | sort -rn
     19 executor
     11 scout
      8 reviewer
      8 critic
      7 scribe
      5 mutation-tester
      2 sentinel
      2 connector
      1 simplifier
      1 revenger
$ jq -r '.counts' .ufo/waves/round-42/wave1-dispatch.json
{"spawn": 64, "resume": 0, "total": 64}
$ jq -r '.items[] | select(.role=="connector") | .name' .ufo/waves/round-42/wave1-spec.json
ConnCrossClaims
ConnWave2Seed
```

Attack share = reviewer 8 + critic 8 + mutation-tester 5 = 21/64 = **32.8%** (the r41 lesson's counting
rule). Wave 2 and the round total are left `<pending>` rather than estimated.

## Evidence used by the two mistake rows

Committed artifacts only (all `git ls-files`-tracked): `.ufo/waves/round-41/wave2/CritC1KillRule.md`,
`.ufo/waves/round-41/wave2/RevC1Counters.md`, `corpus/lessons/round-41-verifier-spotcheck.md`,
`corpus/QUALITY.md`, `.ufo/waves/round-42/{claims.json,c1-controls/do-nothing.txt,
c2-controls/before.txt,census-before.txt}`.

- **M42-1 (evidence-union).** `RevC1Counters.md` and `CritC1KillRule.md` both carry the verbatim
  transcript line `selftest detail=I1 mutant=evidence-not-named rejected=0 rc=0
  payload=records=3,lines=14,graded=3,evidence=3/3,missing=0`, and `RevC1Counters.md` states the cause:
  evidence is collected as a cross-record union (`check_i1`, lines 902–906). Routed at
  `round-41-verifier-spotcheck.md` §5 item 6 ("I1 per-correction evidence enforcement").
- **M42-2 (token-boundary).** Same two receipts: `selftest detail=I3 mutant=mangled-value-token
  rejected=0 rc=0 payload=exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0`; `RevC1Counters.md`
  records the mutant input `closed=10/100` (instrument lines 1757–1759) and the independent
  `value_present` limb (438–459). Routed at the same §5 item 6 ("I3 token-boundary grading").
- **C1 before column.** `c1-controls/do-nothing.txt` (committed): the r42 suite is absent at base
  (`exit=127`), and the r41 suite at base prints `selftest cases=12 failures=8` / `closed=8/12 exit=1`,
  with the I1/I3 families named as still open.
- **C2 before column.** `c2-controls/before.txt` (committed): frontier 24, registry 63, knowledge 60,
  harness `entries=27 pass=27`, binding `records=55 bound=55`, audit `expected=60`, S064+ absent.
  `census-before.txt`: `W04 S028`, `W04 S029`, `ok`, `exit=0`.

Attempted first-hand reproduction (recorded because it failed):

```
$ bash corpus/instruments/r41-closure.sh --selftest --export-ref 5053a7f46de35784cff4b56756906e9014a38276 \
    --work /fast/scratch/hyaku/kasegi-r42/ScribeLesson/work --scratch-root /fast/scratch/hyaku/kasegi-r42/ScribeLesson
selftest export-ref=5053a7f46de35784cff4b56756906e9014a38276 suite-sha256=3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd
# command deadline 240 s hit; no further lines were emitted (a ~60-seat wave was running on the same host)
```

No value in the lesson rests on this aborted run: the base reds come from the committed control and
the I1/I3 details from the committed wave-2 receipts. I did not rerun it a second time.

## Conflicts (reported verbatim, not edited)

1. **The round-42 QUALITY criterion id is contested across two wave-1 artifacts.** ScribeQuality's own
   spec (`wave1-spec.json`) orders four criteria `R-a`…`R-d` with "next R-numbers after the file's
   current max" — current max is `R38` (`corpus/QUALITY.md:337`, `grep -c '^| R[0-9]* |'` → 38), so
   per-correction evidence (`R-b`) would be `R39`/`R40` depending on the scribe's ordering; while the
   wave-1 reviewer `RevQuality.md` analyses the gaps as `R39` = per-record verdict (union evidence,
   status flip, payload re-derivation), `R40` = whole token, `R41` = scratch root, `R42` = replay
   limb, `R43` = duplicated Correction block. No landed append exists at this seat's read (the
   `corpus/QUALITY.md` I read is 337 lines / 60,663 B, sha256
   `a76f42d76f10c123be853f0575bb347848d38e7dcdabdcb2d4eaaccb32a19ac6`, R1–R38 only). The
   deliverable therefore names the M42-1 captured-by criterion **by its content** ("per-record
   verdicts: evidence claims are per-correction, never union aggregates") and leaves the id
   `<pending>`; the L1 fills `R39` under the RevQuality mapping or `R40` under ScribeQuality's
   prompt order.
2. **RevQuality's `R39` also covers the frontier-counter status flip** (its "same limb: tally follows
   membership"), while `claims.json` C1 names F-FLIP as its own repair family with its own J-check.
   Recorded only: the lesson's M42-1 row covers the evidence-union shape, and the status-flip repair
   is named in the C1 before column as part of the routed queue.

## Known limits

- The frozen-claims table's after-columns are the **declared** after-states from `claims.json`, not
  observed values; observation lands post-integration at Y.
- `## Gate` is a placeholder naming the sibling deliverable `wave1/ScribeC2Gate.gate-block.txt`; this
  seat did not splice it (it had not landed at read time) and did not verify any S064/F25 source,
  capture, quote or entry.
- `## Census` after-state, wave-2 seat/connector/attack tallies and the wave-2 verdict body are
  `<pending>`; none is estimated.
- The freeze hash in the header is the commit that added `claims.json` at this read; if the L1
  re-commits the claims file, the header needs the new hash.
- No tool installed, no network fetch, no mutating git/jj command, no lane file written outside the
  deliverable and this receipt. `corpus/lessons/round-42.md` was **not** created by this seat — the
  L1 lands the bytes from `ScribeLesson.lesson.md`.

## Scratch

Work copy at `/fast/scratch/hyaku/kasegi-r42/ScribeLesson/` (draft `round-42.md`, the aborted run's
`r41-at-base.txt` and its 297 MB `work/` export); removed after this receipt and the deliverable were
copied into the wave dir.
