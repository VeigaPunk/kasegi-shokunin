# ScribeCorrections — round-42 wave-1 receipt

Seat: `ScribeCorrections` (scribe, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Round 42, attempt 1 (run-10 fresh start). Base `5053a7f46de35784cff4b56756906e9014a38276`.
Lane HEAD at work time `0566bd66e93d429b2df8b6751cf10cbdc391e79b` ("round-42: frozen claims + controls +
wave-1 spec/dispatch"). Axes: `depth:verifiability`, `coverage` (this seat drafts records text; it
does not run the counters). Scratch `S=/fast/scratch/hyaku/kasegi-r42/ScribeCorrections/`, created,
used, removed (see §6). No tool installed or updated. No pacman. No git/jj mutation.

Frozen claims were read first (`claims.json`, 5053a7f4 tree; `c1-controls/do-nothing.txt`,
`c2-controls/before.txt` present). No claim text was used to upgrade any unobserved fact below.

## 1. Deliverable

`.ufo/waves/round-42/wave1/ScribeCorrections.blocks.txt`

| Property | Value |
|---|---|
| blocks | 3 (`## BLOCK` headings at lines 1, 5, 9) |
| content lines | 3 (one per block; `grep -vc '^## BLOCK \|^$'` → 3) |
| total lines | 11 |
| bytes | 4259 |
| sha256 | `5a26e1e5a4ca19e0464c5eaaaca66fe8119505e5c6e7b336535f6719e4824b45` |
| line-anchored `^Correction (round` lines | 0 (`grep -c` → 0) — no block is a `Correction (round <n>):` entry, so none enters the correction line sets J1/J11 read |

Block map:

| # | line | target | content |
|---|---|---|---|
| 1 | 3 | `SCORECARD.md` | `Correction-dedup (round 42): duplicated Correction (round 41) blocks at SCORECARD.md lines 1602-1605 and 1607-1610 — the second occurrence is the stray; both kept as history. …` — the wave1 spec's mandated marker sentence verbatim (ranges filled), then the measured evidence: file/size digest, 8 line-anchored entries, the byte-identical four-line runs, blank line 1606, four distinct not eight, dedup by content, J11 as the reading check |
| 2 | 7 | `LOG.md` | `Erratum sweep (round 42, r41 C1 grading): …` — item (2) sweep result: no r41 grading slot grades C1 otherwise, slot-by-slot citations, the two bare-grep false positives, and the routed r40 report line |
| 3 | 11 | `.ufo/reports/round-42/kasegi.md` | `Attack-tally pattern (round 42): …` — the tally pattern, the verified wave-1 dispatched counts with digests, the in-family/routed split, and the replay-counts-as-attack rule |

Nothing else is in the file: no headings that are not part of a landed block beyond the three
`## BLOCK <target>` separators, no notes, no validation tables.

## 2. Item (1) — SCORECARD dedup note: evidence

Landing constraint, verified after the first draft and folded into BLOCK 1: the wave-1 spec already
mandates this note inside the *ScribeScorecard* deliverable —
`.ufo/waves/round-42/wave1-spec.json`, ScribeScorecard prompt: "Include the dedup marker line
`Correction-dedup (round 42): duplicated Correction (round 41) blocks at SCORECARD.md lines <a-b> and
<c-d> — the second occurrence is the stray; both kept as history.`" — and that deliverable exists:
`.ufo/waves/round-42/wave1/ScribeScorecard.round42.txt` (29 lines, sha256
`2c14ad57696ae607e0c4dad44f08e9e055f61cd8d1c4f0e44a89d4d01bb4e25f`), whose line 6 is the marker with
`1602-1605` / `1607-1610` filled. BLOCK 1 therefore now *leads with the same mandated sentence*
(verified byte-exact against the spec template with the ranges substituted) and carries the
measurements after it, so either carrier satisfies the mandate. **Land exactly one of the two** — BLOCK 1,
or `ScribeScorecard.round42.txt:6`. Landing both puts two dedup markers in SCORECARD, which is the
D-r41-1 class again.

J11 acceptance — **reported by the J11 executor (`ExecJ11Corr`), not measured by this seat**: both the
bare mandated sentence and the BLOCK-1 sentence with the measurements appended are GREEN
(`marker=1,marker-covers=4/4,unexcused=0,recorded=1`, exit 0), because hash-embedded digit runs are not
read as line references. The executor states two landing conditions, both checked here against my bytes:
(a) column 0 and outside any fence — `grep -c '^Correction-dedup (round 42):'` → 1,
leading-whitespace variants → 0, fence lines in the deliverable → 0; (b) appended below the last
pre-round-42 correction line, `SCORECARD.md:1610` — the carrier lands after line 1628 and after the
`## Round 42 result` block. It also confirms the range form `1602-1605 and 1607-1610` is what covers all
four occurrences (1602+1607, 1603+1608, 1604+1609, 1605+1610); naming only the stray run would not.
Post-yield amendment it measured (also executor-reported): a tree carrying **both** wave-1 carriers is
GREEN (`recorded=2, marker-covers=4/4, unexcused=0`, exit 0) because every qualifying marker contributes
to the coverage union — so landing one carrier is hygiene, not a J11 blocker, and this seat's
single-carrier instruction is a tidiness rule only.
Executor-measured (not by me), for the round's audit trail: J11 is RED over the claims-freeze export
`0566bd66e93d429b2df8b6751cf10cbdc391e79b` (`records=3,corrections=31,distinct=27,dups=4,dup-lines=4,unexcused=4,marker=0,marker-covers=0/4,recorded=0,closed=0`, exit 1) and RED over both frozen
negative-control refs (base `5053a7f4…`, round-41 judged head `1f746461…`), GREEN over the marker-appended
landing copy (`unexcused=0,marker=1,marker-covers=4/4,recorded=1,closed=1`, exit 0), GREEN over the full
planned three-record landing (`corrections=33,distinct=29,marker-line=1634,closed=1`), GREEN over this
BLOCK 1 carrier (exit 0), and its replay fixtures are `replay fixtures=12 failures=0`, exit 0 — the payload
always keeps reporting the duplication itself (`dups=4`), so the committed defect is detected and named,
never silently passed.

```console
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin grep -n '^Correction (round 41):' SCORECARD.md | cut -d: -f1 | tr '\n' ' '
1602 1603 1604 1605 1607 1608 1609 1610
$ grep -c '^Correction (round 41):' SCORECARD.md
8
$ sed -n '1602,1605p' SCORECARD.md | sha256sum | cut -d' ' -f1
95632a3fcce7e5bb5304b3e873e62ab579129d145ee16322c057c95eddbce4b5
$ sed -n '1607,1610p' SCORECARD.md | sha256sum | cut -d' ' -f1
95632a3fcce7e5bb5304b3e873e62ab579129d145ee16322c057c95eddbce4b5
$ sed -n '1606p' SCORECARD.md | od -c | head -1
0000000  \n
$ wc -l < SCORECARD.md; sha256sum SCORECARD.md | cut -d' ' -f1
1628
f3bd52685278e9848a6bb9ca50154d14b7c06b595799dff7dfe5731812c0aad6
```

Result: eight line-anchored round-41 correction entries, in two four-line runs (1602-1605 and
1607-1610) with exactly one blank line (1606) between them; the two runs are byte-identical, so the
file carries **four distinct** round-41 corrections, and the second run is the stray. This is
the round-41 verifier's D-r41-1 exactly (`corpus/lessons/round-41-verifier-spotcheck.md` §5 item 1:
"lines 1602–1605 and again 1607–1610 … no rewrite — append-only"). The note lands after line 1628
and therefore cannot shift the ranges it names.

## 3. Item (2) — "an erratum for any r41 line that graded C1 as anything but not-verified"

**Finding: no qualifying line exists in the round-41 records, so no erratum is issued against an r41
record.** Block 2 records the sweep and its evidence rather than inventing a correction.

Sweep (run over the six record files that carry round-41 grading text):

```console
$ python3 "$S/sweep.py"   # per line: file:line NEG|AFFIRM <first 160 chars>, for lines containing
                          # both "C1" and a grade word (verified / not verified / unverified)
… 28 lines …
---- total lines touching C1+grade: 28 affirmative: 10
```

All 10 crude `AFFIRM` hits resolve to one of three non-qualifying classes; the r41 slots are all
negative. Slot-by-slot, verbatim:

| record | line | observed |
|---|---|---|
| `SCORECARD.md` `## Round 41 result` depth:verifiability row | 1616 | `\| depth:verifiability \| 4 \| **4 (held; not verified)** \| C1 `corpus/instruments/r41-closure.sh` landed; …` |
| `LOG.md` round-41 entry | 1742 | `- Frozen claims: C1 depth:verifiability (4 held) and C2 coverage (8 held), both unverified; neither score moved.` |
| `LOG.md` round-41 C1 bullet | 1743 | `… I2/I6 also fail at final verification. Base and r40-head negatives are red; plain run refuses exit 2. C1 remains not verified under its frozen kill rule.` |
| `SHONEN.md` round-41 box 3 | 229 | `… C1 final receipt run is `closed=10/12 exit=1` and graded selftest has 6 failures, so the round does not verify the closure suite. Box remains `[~]`.` |
| `corpus/lessons/round-41.md` claims row | 23 | `\| C1 \| depth:verifiability (4, held) \| … \| … C1 is not verified on the frozen kill rule, so no score move is claimed. \|` |
| `corpus/lessons/round-41.md` verdict | 77 | `**C1 — not verified.** At the integrated probe ref, committed I1 and I3 defeat fixtures survived:` |
| `.ufo/reports/round-41/kasegi.md` C1 paragraph | 26 | `… The I1 and I3 surviving mutations violate C1's frozen kill rule, so C1 is not verified.` |

The 10 crude `AFFIRM` hits decompose as:

1. **Other rounds' rows** (not r41): `SCORECARD.md:331, 875, 1001, 1144, 1312` — C1 rows of earlier
   rounds; `corpus/lessons/round-34-verifier-spotcheck.md:128`,
   `round-36-verifier-spotcheck.md:38`, `round-37-verifier-spotcheck.md:41` grade their own rounds
   (`round-35`/`38`/`39` spot-checks grade `NOT VERIFIED`). Out of this sweep's scope.
2. **Round-40's grades, already withdrawn**: `SCORECARD.md:1595` (`**4 (held; verified)**`),
   `LOG.md:1728` (`- C1 (depth:verifiability, 4 held, verified): …`), each corrected by the
   round-41 blocks at `SCORECARD.md` 1602-1605 / 1607-1610 and `LOG.md:1736`.
3. **Non-grading English** in r41 records, both named in block 2:
   `corpus/lessons/round-41-verifier-spotcheck.md:6` ("the C1 suite/selftest was
   evidence-verified from committed bytes only" — the reviewer's method; line 42 of the same file
   reads `### C1 — depth:verifiability (held 4): NOT VERIFIED — evidence-verified, gate not executed`),
   and `corpus/lessons/round-41.md:30` (the M41-1 mistakes row, which reports the round-40
   overclaim under correction).

**Routed finding (out of this seat's write scope).** The round-40 fleet report
`.ufo/reports/round-40/kasegi.md:32` still reads `- **C1 — depth:verifiability, 4 → 4 (held;
verified).**` with no appended withdrawal. Its records copies in the lane were withdrawn in round 41;
the fleet report is a prior round's artifact and this lane cannot append to it, so block 2 names it as
routed, not corrected. L1/integrator decision.

## 4. Item (3) — attack-tally pattern: evidence

```console
$ python3 - <<'EOF'   # over .ufo/waves/round-42/wave1/swarm-registry.json
roles=Counter(m['role'] for m in members); attack = roles['reviewer']+roles['critic']+roles['mutation-tester']
EOF
{'connector': 2, 'critic': 8, 'executor': 19, 'mutation-tester': 5, 'revenger': 1, 'reviewer': 8, 'scout': 11, 'scribe': 7, 'sentinel': 2, 'simplifier': 1} total 64
attack roles 21
$ python3 -c "import json;print(json.load(open('.ufo/waves/round-42/wave1-dispatch.json'))['counts'])"
{'spawn': 64, 'resume': 0, 'total': 64}
$ sha256sum .ufo/waves/round-42/wave1-dispatch.json .ufo/waves/round-42/wave1/swarm-registry.json
138f9f757910b00f3eca7c519e9f9d2847d98d8a0f47f7dad4509e0c91f745eb  .ufo/waves/round-42/wave1-dispatch.json
f49aaca6ba1f5401dc452a2f84cb958885263a386a8b8a383afc9b3d18672b9a  .ufo/waves/round-42/wave1/swarm-registry.json
$ git ls-files .ufo/waves/round-42/wave1/swarm-registry.json
.ufo/waves/round-42/wave1/swarm-registry.json
```

The block carries the dispatched count only and labels it so ("dispatched only, not verdicts"); the
verdict and artifact counts are the report's to add from the wave results file. The in-family /
routed split and the "replay counts the attack" rule are read from the frozen `claim_design_lesson`
and C1 kill rule in `claims.json`, not invented.

## 5. Deliverable validation

```console
$ cd .ufo/waves/round-42/wave1
$ wc -lc ScribeCorrections.blocks.txt
  11 4259 ScribeCorrections.blocks.txt
$ sha256sum ScribeCorrections.blocks.txt
5a26e1e5a4ca19e0464c5eaaaca66fe8119505e5c6e7b336535f6719e4824b45  ScribeCorrections.blocks.txt
$ grep -c '^## BLOCK ' ScribeCorrections.blocks.txt; grep -vc '^## BLOCK \|^$' ScribeCorrections.blocks.txt
3
3
$ grep -c '^Correction (round' ScribeCorrections.blocks.txt
0
```

No block wraps: each block is one physical line, so a byte-exact copy lands one line per block.

## 6. Scratch

`S=/fast/scratch/hyaku/kasegi-r42/ScribeCorrections/` was created with `mkdir -p`; the only files in it
were `claim.txt`, `claim_wrapped.txt`, `sweep.py` (evidence capture; no work copies outside the lane
were needed). Disk guard was green before work (`root 5%`, `/fast/scratch/hyaku 27%`, 592.6G free).
`rm -rf -- "$S"` was run after the deliverable and this receipt were written; verified absent with
`test ! -e`.

## 7. Findings and coordination

1. **D-r41-1 duplication (item 1).** Confirmed with digests: 8 line-anchored round-41 entries, two
   byte-identical four-line runs at 1602-1605 / 1607-1610, blank line 1606. For a J11 (F-CORR)
   implementation: counting by position reads 8; counting by content reads 4 distinct + 4 duplicates.
   The recorded exception is my `Dedup note (round 42, D-r41-1)` line, which does not start
   `Correction (round <n>):` and so changes neither count.
2. **Item (2) is a null result, reported as such.** No round-41 record line grades C1 as anything but
   not-verified (§3). I did not fabricate an erratum for a defect that is not present.
3. **Routed: round-40 fleet report C1 line** (`.ufo/reports/round-40/kasegi.md:32`,
   `4 → 4 (held; verified)`) has no appended withdrawal; out of the lane's append surface.
4. **Duplicate-landing risk on the dedup note — resolved to a single-carrier instruction.**
   `ScribeScorecard.round42.txt:6` already carries the marker, and the spec mandates it there (see §2).
   My first message went to `agent://ScribeScorecard`, which answered as the **round-41** instance: it
   owns `round-41/wave1/` only, cannot edit the round-42 file, and correctly noted that the marker is
   dispatch-mandated. BLOCK 1 was then recast to lead with the mandated sentence (spec byte-exact) plus
   the measurements, so one carrier now satisfies the mandate with evidence attached. Landing **one** of
   BLOCK 1 / `ScribeScorecard.round42.txt:6` is the tidy outcome; J11's measured post-yield fact (§2) is
   that a tree carrying both is still GREEN (`recorded=2`, coverage union), so this is hygiene, not a
   blocker.
5. **J11 (`agent://ExecJ11Corr`) accepted the carrier** (see §2, executor-reported): both the bare marker
   and the marker plus measurements are GREEN (`marker=1,marker-covers=4/4,unexcused=0,recorded=1`). Its
   anchor note matters for the suite: the carrier begins `Correction-dedup (round 42):`, so `^Correction`
   matches it while `^Correction \(round [0-9]+\):` does not — J11 anchors on the latter, and blocks are
   counted by content. The two landing conditions (column 0, outside fences; appended below line 1610) are
   checked against my bytes in §2.

## 8. Scope and limits

- Wrote only: `.ufo/waves/round-42/wave1/ScribeCorrections.blocks.txt` (deliverable) and this receipt,
  plus scratch under `S` (removed). No other lane file, no fleet-root file, no sibling lane, no
  `shokuknow`, no PATH directory.
- `git status --porcelain | grep -v '^??'` → empty: this seat made **0 tracked modifications**; no
  add/commit/push/checkout/reset/stash and no jj command was run.
- Not verified by me (other seats own them): the `r42-closure.sh` J1-J13 suite and its replay limbs,
  J11's actual implementation, the C2/F25 counting chain. This receipt claims nothing about them.
- No network fetch was made by this seat; no HTTP status/bytes/UTC lines to record.
