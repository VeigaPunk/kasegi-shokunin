# ScribeIntegrationNotes — LOG.md round-35 entry draft + D4 provenance-note template

Seat: `ScribeIntegrationNotes`, scribe, leaf of round-35 wave 1 (wave `kasegi-r35-build`, L1
`KasegiR35`, 64 seats). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, lane base
`3266c9937b03062d9bbc2f436e20820115ed179c`, claims-freeze commit
`617496b9c6e92bc671e7e78b83df69a04470d0e9`, lane `HEAD` at composition
`da2d3c687f82a9814ee71c91c930cb733050d37c` (`round-35: wave-1 spec + dispatch (64 seats, v2)`).

**Scope of this receipt.** Two drafts only: (A) the `LOG.md` round-35 entry, ready to append at end of
file; (B) the D4 provenance-note deliverable. This seat wrote no product file: it did not append to
`LOG.md`, did not write `.ufo/waves/round-34/wave1-results.json.provenance.md` (that note already
exists — see B), did not commit, did not stage, and ran no jj/git mutation. The L1 appends and
commits.

**Draft-time is not close-out-time.** The wave was in flight while this draft was composed
(2026-10-26T06:34Z–06:38Z). Counters below were read from the *live worktree*, and some of them
moved between two reads of the same file (recorded in §Report F1). Every number in Draft A that
could not be read from a named receipt at composition time is written as `⟨FILL: …⟩` with the
command that produces it; **no value in Draft A is inferred**. The L1 re-measures at quiescence and
substitutes.

---

## Draft A — `LOG.md` round-35 entry (append at end of file; L1 commits)

Format mirrors the round-34 entry: `## Round N — date — subject (wave shape, seats)` heading, one
provenance paragraph, `**C1 …**` / `**C2 …**` bullets with before→after, a `Frontier step:` /
`Shape:` paragraph pair, a verifier close-out block, and a tooling line.

```
## Round 35 — 2026-10-26 — C1 D1–D7 closure suite (`r35-defect-closure.sh`); C2 F18 CISA Known Exploited Vulnerabilities admitted (S052); one v2 wave, 64 seats

Claims frozen in `.ufo/waves/round-35/claims.json` (sha256
`fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982`, `frozen_at_utc`
`2026-10-26T07:30:00Z`, attempt 1; claims-freeze commit `617496b`, base `3266c99`). Before controls
measured at the freeze and committed with it: `.ufo/waves/round-35/c1-controls/before.txt` (sha256
`352d3da2…`), `c2-controls/before.txt` (`2835700332…`), `census-before.txt` (`74fc6a26…`), plus the
two do-nothing controls `c1-controls/fake-suite.sh` (`292aaac048…`, prints `closed=7/7 exit=0` with no
check) and `c2-controls/junk-f18.md` (`0abec3591e…`, F18-shaped, fabricated quotes, no manifest
record). Wave-1 spec/dispatch (64 seats, policy v2, `spawn 64 / resume 0`) `da2d3c6`
(`wave1-spec.json` sha256 `3fcf44e1…`, `wave1-dispatch.json` `aedd0320…`); integration commit
`⟨FILL: integration commit — the L1's own hash⟩`.

**C1 depth:verifiability (4 held) — three limbs landed, three pending the L1's commit.** New committed
`corpus/instruments/r35-defect-closure.sh` carries the seven round-34 verifier-routed defects D1–D7 as
seven check functions, each exiting non-zero while its defect is open. Measured readings, kept apart
because they are not the same tree: **live lane, 06:38Z** `closed=4/7 exit=1` with `D4 open=1`, `D6
open=1`, `D7 open=1` and D1/D2/D3/D5 `open=0` (`ExecClosureSuite.md` §3, lines 68–75); **live lane
`--selftest`** `cases=7 failures=3` — the three failures are exactly those still-open defects, not a
broken selftest; **all-fixed tree** `closed=7/7 exit=0` and `--selftest cases=7 failures=0`
(`ExecClosureSuite.md` §5/§7, lines 124–140, 208–249), plus a two-defect control at `closed=5/7
failed=D1,D2`; **base-tree export** `closed=0/7 exit=1`. `closed=7/7` is reachable on the lane only
after D4/D6/D7 land, so this entry's final C1 sentence must quote a post-integration run
⟨FILL: plain `closed=7/7 exit=0` + `--selftest cases=7 failures=0` re-run at quiescent tip; receipts
`ExecClosureSuite.md`, fixtures `ExecSelftestFixtures.md`, mutation `MutClosureSuite.md`/
`MutFixturesLimbs.md`, review `RevClosureSuite.md`⟩. The do-nothing control is rejected: the fake
suite's `--selftest` is refused by the suite's own judge (`judge=fake-suite rejected=1`), and the
plain `closed=7/7 exit=0` line alone does not satisfy it ⟨`ExecDoNothingReject.md`⟩. Per defect,
before → the state measured at composition, with the closing condition separated out: **D1**
`filled by the L1` 1 → 0, correction naming `c1c6a5f826d2425446347173de527c42991b78b0` present
(`grep -c c1c6a5f` 0 → 3, angle-bracket marker count 0) — **landed**; **D2** round-34
depth:density-row erratum naming the corrected mean 201.2 (`round-34 depth:density row` 0 → 1,
`201.2` 0 → 2, stale row bytes untouched) — **landed**; **D3** `SKILL.md` Gates & probes registry
registers `r-defect-closure.sh` and `kill-rule-check.py` (`grep -c` 0 → 4 each; D3's two instruments
are the *nine*-check round-34 suite `r-defect-closure.sh` and the kill-rule counter — distinct files
from C1's new seven-check `r35-defect-closure.sh`), registration-level only, with the plain-run verdict
map read from the committed source rather than from a round-35 run — **landed**
⟨`ExecD3SkillRegistry.md` §3–§6⟩; **D4** `.ufo/waves/round-34/wave1-results.json` still **untracked**
(`git ls-files … | wc -l` = 0 at 06:43Z), with `.ufo/waves/round-34/wave1-results.json.provenance.md`
present beside it (312874 B, sha256
`3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4`; note sha256 `e1c44301…`) —
**pending the L1's commit, which is the whole closure** ⟨`ExecD4ResultsTrack.md`; see Draft B⟩;
**D5** `.ufo/waves/round-35/claims-erratum-d5.md` carries both required literals (`discriminating
invocation`, `per-id occurrences`) — **landed, untracked** ⟨`ScribeErratumD5.md`⟩; **D6** the
round-34 `wave1/L1Integration.md` dead-seat sentence is **unchanged** (stale sentence 1,
`Correction (round 35)` 0) and the check demands the stale count reach 0, so an append-only correction
cannot close this limb without rewriting that sentence (or changing the check to accept an erratum
form) — **open, and it has no seat owner in the wave spec** ⟨checked by `r35-defect-closure.sh` D6 and
`RevD5D6D7.md`; see §Report F7⟩; **D7** `corpus/QUALITY.md` still reads `supersedes R22` = 0 and
`supersedes R23` = 0 at 06:43Z — **the draft rows (`ScribeQualityDraft.md`) are not landed rows**.
Score held at 4.

**C2 coverage (7 held) — landed and measured on the live tree.** Frontier F18 admitted 17 → 18
(`grep -cE '^\| F[0-9]+ \|' corpus/README.md` = 18 at 06:43Z) — the CISA Known Exploited
Vulnerabilities catalog: prioritization by *exploitation status* (an addition deadline plus a
known-ransomware flag per CVE), which is not a severity ladder and therefore not a duplicate of F17's
CVSS-derived classification. Entry `corpus/knowledge/cisa-kev-catalog.md` cites `source: S052`
(`grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l` = 1) ⟨receipt: `ScribeEntryF18.md`⟩;
registry 51 → 52 (`grep -cE` S-rows = 52; S052 row = 1) — tier A scoped to CISA's own catalog
statements, status `mined`, opened 2026-10-26, recheck 90d, used-by the F18 entry ⟨`ScribeSOURCESRow.md`
+ `ExecRegistryAppend.md`⟩; capture `corpus/source-snapshots/round-35/S052.txt` (1479694 B, sha256
`d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`, 27870 lines, fetched
`2026-10-26T06:32:40Z`, HTTP 200 served directly from
`https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`) with manifest
`corpus/source-snapshots/round-35/manifest.json` (sha256 `06bfcc71…`, record S052, assertions Q1–Q5
each anchored at its capture line) ⟨`ExecC2Capture.md`⟩; harness **measured by this seat** at
`2026-10-26T06:44:31Z`: `entries=21 pass=21 exit=0` including `PASS F18 knowledge/cisa-kev-catalog.md
ids=S052` (read-only run of `corpus/instruments/frontier-recheck-count.py`; exit 0) — the final entry
still owes the quiescent regression receipt ⟨FILL `ExecRegressionC2.md`⟩, and an earlier
`entries=20 pass=20` reading is a pre-F18 state, not a contradiction; source-recheck S052 exit 0
(every assertion `occurrences=1`, `sha256 OK`) ⟨`ExecC2Capture.md` §self-check⟩; census exit 0 with the
unchanged W04 S028/S029 duplicate-URL warnings only ⟨`ExecCensusAfter.md`⟩; knowledge entries 46 → 47
(`ls corpus/knowledge/*.md | wc -l` = 47). The junk twin is not admitted and its fabricated sentence is
rejected against the pinned capture (`grep -c` of the twin's distinctive sentence in `S052.txt` → 0)
⟨`ExecDoNothingReject.md`, `MutJunkTwin.md`⟩; the round-34 D5 wording repair is what makes that
statement executable, so the twin's rejection is stated as a capture check, not as "the twin's
`recheck:` line exits non-zero" (the twin's line re-checks the real manifest and exits 0 by
construction).

Frontier step: census before → after exit 0 (both; W04 S028/S029 only). Mistakes: M35-1 — the
round-34 wave wrote `wave1-results.json` 3 min 48 s after the `complete` line (D4); class
landing/closure-order; captured-by R4's "landed means committed" reading not applied to the results
file; fix = commit the results file with its provenance note and quiesce seats before the final commit
⟨`.ufo/waves/round-35/wave1/ScribeMistakesDraft.md` + `corpus/lessons/round-35.md` §Mistakes⟩. Sourced
claim: C2 rests on S052, opened this round. Assimilation: **none adopted** — id-collision check
re-run with the guard proved once on an indented-row fixture ⟨`ExecIdCollisions.md`: ⟨FILL collisions
count and fixture result⟩⟩, quarantine slice re-derived from the read-only register (7 rows, per-row
verdicts ⟨FILL from `ExecQuarantineSlice.md`⟩), standing refusals re-measured with flip conditions
still unmet ⟨`ScribeGateAssimilation.md` + `corpus/lessons/round-35.md` §Gate⟩.
`considerthese/2026-10-25.md` proposal 2 (distance to the next score, not only "improved, held")
mined → `corpus/QUALITY.md` R26, with the read-only gap computation in `ExecScoreGap.md` ⟨receipts:
`ExecScoreGap.md`, `ScribeQualityDraft.md`; note the numbering decision recorded in §Report F3⟩; the
other five proposals keep their recorded dispositions with reasons in the lesson §considerthese.

Shape: one v2 wave `kasegi-r35-build`, 64 seats — executor 18, scribe 12, reviewer 10, scout 6,
mutation-tester 5, critic 5, connector 4, sentinel 2, simplifier 2; attack share 22/64 = 34.4% under
the round-34 definition (reviewer + mutation-tester + critic + sentinel, simplifier not counted);
dispatch `spawn 64 / resume 0`, registry 64 members (all `kind=spawn`, `agentId` null at
composition), no lane-external write ⟨`.ufo/waves/round-35/wave1-dispatch.json` `counts`,
`.ufo/waves/round-35/wave1/swarm-registry.json`⟩. Dead seats: ⟨FILL `K`⟩/64 — receipts filed
⟨FILL⟩, names without a receipt ⟨FILL⟩ (command in the fill list below); each dead seat's slice is
covered by ⟨FILL: which seat re-ran it⟩. `wave1-results.json`: ⟨FILL: present/absent
for round 35, with mtime — absent at composition, and if it lands after the `complete` line the D4
defect recurs and the file must be committed with its own note before this entry is appended⟩.

Verifier close-out (non-author, hyaku; placeholders — the L1 fills from the canonical report, never
from this seat): report `.ufo/reports/round-35/kasegi.md` committed by lane identity as ⟨FILL⟩; one
`## SHONEN` heading with 4 box lines all `[~]` ⟨FILL: check⟩; cited hashes ⟨FILL: the five⟩ all
present and ancestors of `master`; lane `ahead=0 behind=0` ⟨FILL⟩; per-axis verdicts ⟨FILL:
depth:verifiability improved/holds-4, coverage improved/holds-7, depth:density unchanged-9⟩; routed
defects ⟨FILL: D1… from the spot-check §6, status-neutral⟩.

Tooling: no tool installed or upgraded; no pacman transaction attempted (host-wide pause); no
`uv tool`/`npx`/`~/.local/bin` install. Answering model ⟨FILL: read from a seat receipt or the
config route table — not asserted here⟩.
```

### Fill list (each slot, its command, its expected literal)

| slot | command | expected |
|---|---|---|
| integration commit | `git log --oneline -1` at close | lane tip after the L1's commit |
| C1 suite plain | `bash corpus/instruments/r35-defect-closure.sh` | `closed=7/7 exit=0` |
| C1 suite selftest | `bash corpus/instruments/r35-defect-closure.sh --selftest` | `cases=7 failures=0` |
| C1 suite on base bytes | `bash corpus/instruments/r35-defect-closure.sh --root <base export>` | `closed=0/7`, exit 1 |
| D1 | `grep -c 'filled by the L1' SCORECARD.md`; `grep -c 'c1c6a5f' SCORECARD.md` | `0`; `≥1` |
| D2 | `grep -c 'round-34 depth:density row' SCORECARD.md`; `grep -c '201.2' SCORECARD.md` | `≥1`; `≥1` |
| D3 | `grep -c 'r-defect-closure' SKILL.md`; `grep -c 'kill-rule-check' SKILL.md` | `≥1`; `≥1` |
| D4 | `git ls-files .ufo/waves/round-34/wave1-results.json \| wc -l`; `ls .ufo/waves/round-34/wave1-results.json.provenance.md` | `1`; exists |
| D5 | `grep -c 'discriminating invocation' .ufo/waves/round-35/claims-erratum-d5.md`; `grep -c 'per-id occurrences' …` | `≥1`; `≥1` |
| D6 | `grep -c 'did not file a receipt (dead seat' .ufo/waves/round-34/wave1/L1Integration.md`; `grep -c 'Correction (round 35)' …` | `0`; `≥1` |
| D7 | `grep -c 'supersedes R22' corpus/QUALITY.md`; `grep -c 'supersedes R23' …` | `≥1`; `≥1` |
| C2 frontier | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `18` |
| C2 registry / S052 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`; `… S052 …` | `52`; `1` |
| C2 entry | `grep -lE '^source: S052 ' corpus/knowledge/*.md \| wc -l` | `1` |
| C2 harness | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=21 pass=21 exit=0` incl. `PASS F18 … ids=S052` |
| C2 recheck | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052` | all `occurrences=1`, `sha256 OK`, exit 0 |
| C2 census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit 0, W04 S028/S029 only |
| C2 entries | `ls corpus/knowledge/*.md \| wc -l` | `47` |
| dead seats | `comm -23 <(python3 -c "import json;print('\n'.join(sorted(i['name'] for i in json.load(open('.ufo/waves/round-35/wave1-spec.json'))['items'])))" \| sort) <(ls .ufo/waves/round-35/wave1/*.md \| xargs -n1 basename \| sed 's/\.md$//' \| sort)` | names without a receipt; empty = 0 dead |
| results file (r35) | `ls -la .ufo/waves/round-35/wave1-results.json` | absent, or present with an mtime **before** the `complete` line |

Boundary carried into the entry: each C1/C2 value is quoted from the named receipt or from the frozen
claims' `after` list; the entry may not claim a run this seat did not perform, and the spot-check
verdicts stay placeholders until the non-author verifier files them.

[INFERENCE] The attack-share roster (reviewer + mutation-tester + critic + sentinel, simplifier
excluded) is **derived**, not quoted: no file in this lane states the definition, and round-34's
committed line (`LOG.md:1639`, inside the entry that starts at `LOG.md:1601`) gives only
`27/65 = 41.5%` with roles reviewer 13, mutation-tester 7, critic 5, sentinel 2 — 13+7+5+2 = 27,
which fits and is the reading used above. If the L1 knows the intended roster, recompute before
appending.

---

## Draft B — D4 provenance deliverable (the note already exists; do not rewrite it)

**Status: prepared, and now on disk. Closure is the L1's commit.** The note is not a template to be
filled from scratch — seat `ExecD4ResultsTrack` wrote the real note at the target path during this
wave. This section records its identity, the exact closure steps, and a reusable skeleton for future
rounds; it deliberately does **not** republish a second body of text for the same path.

### B.1 Identity pin (measured read-only at 2026-10-26T06:34Z)

```
$ sha256sum .ufo/waves/round-34/wave1-results.json .ufo/waves/round-34/wave1-results.json.provenance.md
3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4  .ufo/waves/round-34/wave1-results.json
e1c4430133adeb58b8d3b3af9edcb49739eacd3f40536dca529105c609e86c98  .ufo/waves/round-34/wave1-results.json.provenance.md
$ stat -c '%s %n' .ufo/waves/round-34/wave1-results.json .ufo/waves/round-34/wave1-results.json.provenance.md
312874 .ufo/waves/round-34/wave1-results.json
5639 .ufo/waves/round-34/wave1-results.json.provenance.md
$ git ls-files .ufo/waves/round-34/wave1-results.json | wc -l
0
```

The note's own §3 pins the same `312874` B / `3afa3581…` identity and its §4 pins
`git ls-files … → 0` at filing, so the note and the bytes agree; nothing needs regenerating.

**Do not overwrite.** `ExecD4ResultsTrack.md` §5 states the risk verbatim: *"If that seat instead
writes the round-34 path directly, it would overwrite this note. The digest in §2 identifies the real
note; anything differing from `e1c44301…` is a rewrite, not mine."* A rewrite would also break the
note's §5 self-consistency rule ("this note records the same bytes the L1 will commit; if the bytes
ever differ from §3, treat the file as replaced and treat this note as stale rather than editing
either file").

### B.2 Closure steps (three limbs, in this order)

1. **Add both new files in one commit** — `git add .ufo/waves/round-34/wave1-results.json
   .ufo/waves/round-34/wave1-results.json.provenance.md`. No `-f`: the note's §4 records
   `git check-ignore -v … → exit 1` (not ignored). Verify with `git status --porcelain
   --untracked-files=all -- .ufo/waves/round-34/` → no `??` / ` M` entries left.
2. **The tracked limb must read 1**: `git ls-files .ufo/waves/round-34/wave1-results.json | wc -l`
   → `1` (frozen C1 `counting_commands[4]`; prints `0` before the commit, by design).
3. **The note limb must exist**: `test -f .ufo/waves/round-34/wave1-results.json.provenance.md` and
   `sha256sum` still `e1c4430133adeb58b8d3b3af9edcb49739eacd3f40536dca529105c609e86c98`. Both limbs
   are exactly what the closure suite's D4 check reads (`build-spec.py` `ExecClosureSuite`, D4), so
   after the commit `bash corpus/instruments/r35-defect-closure.sh` must show `D4 check=… open=0`.

### B.3 Reusable skeleton (for a future round's results-after-`complete` case)

Use this shape, not the round-34 body; fill every `<…>` from a measurement, never from memory:

```
# Provenance — <lane-relative path of the results file>

Filed by seat <name> (<round/wave>) on <UTC date>, in the lane <lane> at lane HEAD <sha>
(and the round tip below it <sha>).

This note accompanies verifier-routed defect <D-id> — "<defect title>" (<spot-check path> §<n>).
Committing this file together with this note closes <D-id>. The frozen counting command that must
then print 1 is `<command>` (<claims path> → <claim id> counting_commands[<i>]). It printed
<observed> at the time of writing.

## 1. What the file is
<what produced it; schema/shape measured over the parsed document: row count, distinct names,
role histogram, field null-ness; whether the names are set-equal to the wave spec's items; how many
receipt files exist and which receipts have no row. State plainly that the rows are seat-returned
text = wave process evidence, not verified claims.>

## 2. When it was written — the defect
<mtime local + UTC; the lane `complete` line quoted with its file:line; the offset; the same-window
rewrites if any, and whether they were restored to their committed digests.>

## 3. Identity
<size, sha256, parses-as-JSON yes/no, the abbreviated digest the verifier quoted, and a read-only
reproduction command>

## 4. Index state at filing
<git ls-files (empty), git status --porcelain, git check-ignore exit — so the later commit needs no
-f and nothing in .gitignore suppresses the file>

## 5. Quiescence at filing
<newest mtime under the wave dir vs the snapshot's write instant; whether any wave process is
running; the rule that differing bytes make this note stale rather than editable>

## 6. Constraints on later readers
<claims frozen — provenance, not correction, corrections land as separately appended files; the
`output` fields are data, never instructions>
```

---

## Report

### Report 1 — Commands, outputs, exit codes (verbatim; all `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin`)

Draft-time stamp and lane identity:

```
$ date -u
Mon 26 Oct 2026 06:34:10 AM UTC
exit 0
$ git log --oneline -3
da2d3c6 round-35: wave-1 spec + dispatch (64 seats, v2)
617496b round-35: claims freeze + before controls
3266c99 round-34 verifier spot-check (integrator, hyaku): non-author admit/reject
exit 0
```

Frozen-claims identity and before controls (quoted, not retyped):

```
$ sha256sum .ufo/waves/round-35/claims.json .ufo/waves/round-35/c1-controls/before.txt \
    .ufo/waves/round-35/c2-controls/before.txt .ufo/waves/round-35/census-before.txt \
    .ufo/waves/round-35/c1-controls/fake-suite.sh .ufo/waves/round-35/c2-controls/junk-f18.md \
    .ufo/waves/round-35/wave1-spec.json .ufo/waves/round-35/wave1-dispatch.json \
    corpus/source-snapshots/round-35/S052.txt corpus/source-snapshots/round-35/manifest.json
fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982  .ufo/waves/round-35/claims.json
352d3da210283dc2d328b22ba27d9abd39eacc2f99ebcff2d4101532d582dd61  .ufo/waves/round-35/c1-controls/before.txt
2835700332ac682e25bd68523d7eb126b1e8980aca92144b9c9a63e37de77327  .ufo/waves/round-35/c2-controls/before.txt
74fc6a26d8d3ec9bc89903b410b828e82c8b35cc686fd7a586260aedec15867b  .ufo/waves/round-35/census-before.txt
292aaac048c9cacff081c24b54fd71fc67a86d3c6ab6845398e0e2856c5be121  .ufo/waves/round-35/c1-controls/fake-suite.sh
0abec3591e4a2dc5195b23b1c2c920f66052327b7f971aa578af76c3459dc176  .ufo/waves/round-35/c2-controls/junk-f18.md
3fcf44e16ff63fca3d70cf7216524928765e609c953eacf6de2c5bb3c940d595  .ufo/waves/round-35/wave1-spec.json
aedd03202ac17add5225e85f8642e179680c116a8ea551db197152f9f854b716  .ufo/waves/round-35/wave1-dispatch.json
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt
06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee  corpus/source-snapshots/round-35/manifest.json
exit 0
```

Frozen controls, read from the committed files (C1 block from `c1-controls/before.txt`, C2 from
`c2-controls/before.txt` and `census-before.txt`):

```
C1: ls r35-defect-closure.sh -> ls_exit=2 | 'filled by the L1'=1 | c1c6a5f=0 | '201.7'=2 |
    '201.2'=0 | D3 registry greps=0 | results tracked=0 | provenance note=0 | erratum-d5=0 |
    D6 stale sentence=1 | D7 supersedes=0 0
C2: frontier=17 | registry=51 | S052 rows=0 | entries citing S052=0 |
    harness=entries=20 pass=20 exit=0 | source-recheck S052=manifest UNAVAILABLE reason=missing
    recheck_exit=2 | knowledge entries=46
census-before: W04 S028, W04 S029, kasegi ok, census_exit=0
```

Wave arithmetic (measured over the parsed spec, dispatch and registry; this is the only hard
quantitative input the entry's Shape paragraph takes from this seat):

```
$ python3 - <<'PY'   (spec/dispatch/registry read, printed)
roles {'connector': 4, 'critic': 5, 'executor': 18, 'mutation-tester': 5, 'reviewer': 10,
       'scout': 6, 'scribe': 12, 'sentinel': 2, 'simplifier': 2} sum 64
distinct names 64; every item axes ('depth:verifiability','coverage')
attack share 22/64 (reviewer 10 + mutation-tester 5 + critic 5 + sentinel 2)
dispatch counts {'spawn': 64, 'resume': 0, 'total': 64}; policy.maxLanes 128, source config
registry members 64, all kind=spawn, agentId null on all 64
```

State of every C1/C2 landing at composition (live worktree, `06:34Z`–`06:38Z`; the second column is
what the frozen `after` list requires — this table is why Draft A carries `⟨FILL⟩` rather than
assertions). **Superseded for every row by the `06:43Z`–`06:44Z` read in Report 6**, which found D5
landed (untracked) and all four C2 counters landed; D4/D6/D7 and the QUALITY rows are still open:

| subject | measured now | frozen after-value |
|---|---|---|
| `corpus/instruments/r35-defect-closure.sh` | absent (`ls` exit 2) | present, `closed=7/7`, `cases=7` |
| `SCORECARD.md` `filled by the L1` / `c1c6a5f` / `201.2` / `<LANE_HASH>` | `0` / `3` / `2` / `0` | `0` / `≥1` / `≥1` / `0` |
| `SKILL.md` registry greps (`r-defect-closure`, `kill-rule-check`) | `4`, `4` | `≥1`, `≥1` |
| `QUALITY.md` `supersedes R22` / `R23`; `R26` | `0` / `0`; absent | `≥1` each; R26 present |
| `.ufo/waves/round-35/claims-erratum-d5.md` | absent | present with both literals |
| round-34 `wave1/L1Integration.md` stale sentence / correction | `1` / `0` | `0` / `≥1` |
| round-34 `wave1-results.json` tracked / note | `0` / present (5639 B) | `1` / present |
| frontier / registry / S052 / entry / knowledge | `17` / `51` / `0` / `0` / `46` | `18` / `52` / `1` / `1` / `47` |
| round-35 wave receipts filed | 13 `*.md` at the last read (`06:38Z`, still growing) | — |
| `.ufo/waves/round-35/wave1-results.json` | absent | — (record present/absent + mtime) |

Observation on the kill rule's marker clause, quoted verbatim from `claims.json` C1 `kill_rule`:
*"`<LANE_HASH>` still present in SCORECARD.md"*. At `06:35Z` the literal count was `1`: the D1
correction prose itself read *"because it matched only the `<LANE_HASH>` spelling"*. At `06:36:18Z`
that sentence was rewritten to *"matched only the angle-bracket lane-hash marker"* and the literal
count went to `0`. The kill clause is therefore clean against a literal `grep`, and the suite's D1
check does not read that token either. Recorded because a reader re-running the kill rule should get
`0`, not the `1` this draft first saw.

### Report 2 — File digests of bytes this seat wrote

| path (lane-relative) | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-35/wave1/ScribeIntegrationNotes.md` (this receipt) | — | not self-pinned (a file cannot carry its own final digest); the L1 records it in the commit |
| `.ufo/waves/round-34/wave1-results.json.provenance.md` (**not written by this seat** — identity verified, quoted above) | 5639 | `e1c4430133adeb58b8d3b3af9edcb49739eacd3f40536dca529105c609e86c98` |

No other file was created or modified by this seat.

### Report 3 — Findings and integration risks (L1 decisions, not this seat's)

- **F1 — the worktree moved under the draft (expected, but it dates every number).** Two reads of
  `SCORECARD.md` about two minutes apart returned `<LANE_HASH>` `1` (line 1133, inside the D1
  correction prose) then `0`, with mtime `2026-10-26 03:36:18 -0300` (`06:36:18Z`) and
  `git diff --numstat` `33 15`. Wave seats were landing the whole time: the wave dir held 2 `*.md`
  receipts when this seat began (`ExecD3SkillRegistry.md`, `ExecD4ResultsTrack.md`) and 13 at
  `06:38Z`. Draft A's `⟨FILL⟩` slots are the consequence: the L1 must take the
  numbers at quiescence, after the last seat, or the entry will publish a mid-flight count as a
  final one.
- **F2 — two different "defect-closure" instruments, one claim.** C1's predicate names
  `corpus/instruments/r35-defect-closure.sh` (seven checks, D1–D7). Spotcheck D3 and the SKILL.md
  registry cover `corpus/instruments/r-defect-closure.sh` (nine checks, R1–R9) plus
  `kill-rule-check.py`. `ExecD3SkillRegistry.md` §Findings 1 raises the same split and declined to
  widen its scope. Draft A states both files explicitly and says the D3 rows are registration-level.
  If the L1 renumbers or aliases them, the entry's D3 sentence is the one line to change.
- **F3 — R26 numbering is not settled between the two specs that name it.** `claims.json` →
  `non_claim_frontier_items.considerthese` says proposal 2 is "mined into QUALITY R26";
  `build-spec.py` `ScribeQualityDraft` drafts *R26 as the row that supersedes R22* and *R27 as the
  row that supersedes R23*, and also says "place as the supersedes-R22 row or as its own R26 row per
  shape consistency". C1's counters only require the two literals `supersedes R22` and
  `supersedes R23`. Draft A says "R26" for the criterion and names the supersession rows separately;
  if the landed numbering differs, change the criterion's id in Draft A, not the literals.
- **F4 — the capture URL in the manifest differs from the URL the seat prompt named.** `ExecC2Capture`
  was told to capture
  `https://www.cisa.gov/sites/default/files/csv/known_exploited_vulnerabilities.csv` (CSV); the landed
  manifest records `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`
  (JSON feed), `HTTP status=200 served directly (no redirect)`, `fetched_bytes=1807090`,
  `snapshot_bytes=1479694`, `--kind text` chosen deliberately because `html_to_text()` would rewrite
  entity sequences inside JSON strings. The same seat prompt also carried the note "the JSON endpoint
  `https://www.cisa.gov/known-exploited-vulnerabilities.json` returns HTTP 404". Those are three
  different URLs; the search-log bullet and the S052 registry row must use the **manifest's** URL
  verbatim, or R20's exact-URL binding (`capture-binding-check.py`) will not bind record to row.
  Draft A quotes the manifest URL and the manifest's measurements, not the prompt's.
- **F5 — D4's proof is now split across two seats.** `ExecD4ResultsTrack` prepared and wrote the note;
  no seat has yet committed. Draft B keeps the closure checklist and warns against a rewrite of a note
  whose digest is pinned. If the L1 prefers to move the note's text into the LOG side, it must move
  the file, not fork the content: two bodies for one path is exactly the failure the note's §5 names.
- **F6 — evidence this seat did not produce, with one exception.** No C1 check was executed here (the
  wave reserves gate execution for the parent post-integration; the instruments README also says a
  mid-wave run measures in-flight bytes), so every C1 `after` value is attributed to the receipt that
  owns it. The single exception is the C2 frontier harness: `frontier-recheck-count.py` was run
  read-only at `2026-10-26T06:44:31Z` to settle a contested literal (Report 6), exit 0, no write; its
  reading is labelled as this seat's own and still marked against the missing `ExecRegressionC2.md`
  receipt in Draft A. Plain counter greps (frontier, registry, S052, entry, knowledge, `ls-files`,
  QUALITY) were re-read at `06:43Z` and are reported with that stamp.
- **F7 — D6 has no seat owner, and its check shape forbids the append-only repair the lane prefers.**
  Measured over all 64 spec items' prompts (`python3 -c` walk of `wave1-spec.json`): `L1Integration`
  appears as an *action* only inside the C1 context blurb; the round-34 file
  `wave1/L1Integration.md` is named by exactly three items — `ExecClosureSuite` (D6 **check**,
  `build-spec.py:141`), `ExecSelftestFixtures` (D6 **fixture**, `:162`) and `RevD5D6D7`
  (verification, `:493-495`). No executor or scribe is told to correct the file. Worse, the check as
  written requires `grep -c 'did not file a receipt (dead seat' == 0` **and**
  `grep -c 'Correction (round 35)' >= 1`: an appended correction leaves the stale count at 1, so the
  check stays `open=1` (measured in `ExecClosureSuite.md:73` — `dead-seat-sentence=1,
  correction-round-35=0 open=1`). The fix is therefore one of two deliberate choices, and it is the
  L1's: rewrite the round-34 sentence in place (violating the lane's append-only preference but
  satisfying the frozen check), or change the check to accept the erratum form (then the frozen
  predicate's "stale sentence corrected" needs the erratum reading). "Append a note and hope" closes
  nothing; CritOverclaim-2 measured exactly that (appended note + stale=1 → open=1). Draft A's D6 slot
  is worded to force that choice into the open.
- **F8 — one reviewer keeps its evidence in a subdirectory, not a receipt file.**
  `.ufo/waves/round-35/wave1/RevD3D4/` is a *directory* (mtime `06:37Z`) holding
  `killrule-plain.log` 5401 B, `killrule-selftest.log` 250 B, `r-suite-plain.log` 1002 B,
  `r-suite-selftest.log` 796 B, beside its `RevD3D4.md` receipt. It is legitimate evidence, but it is
  a shape the dead-seat and no-harm counters do not expect (they read `wave1/*.md`); it must be
  committed with the wave or recorded as an open item, not left for `git status` to surprise the L1.
  No counter above depends on it, and this seat did not read its contents.

### Report 4 — Scratch, boundary, tooling

- Scratch: **none created** — every measurement was a read-only `git`/`grep`/`python3` read against
  the lane. `/fast/scratch/hyaku/kasegi-r35/ScribeIntegrationNotes/` does not exist, so there is
  nothing to delete:

  ```
  $ test -d /fast/scratch/hyaku/kasegi-r35/ScribeIntegrationNotes && echo PRESENT || echo ABSENT
  ABSENT
  exit 0
  ```

- Boundary: no write outside the wave dir; no `git add`/`commit`/`push`, no jj command; the fleet
  repo, `/home/vgpnk/Projects/bounties`, sibling lanes and `/home/vgpnk/Projects/shokuknow` were read
  at most, never written, and no shokuknow campaign tool was run.
- Tooling: **none installed or upgraded** (python3, coreutils, git only); no pacman transaction
  (host-wide pause honoured); no `uv tool`/`npx`/release-binary install.

### Report 5 — Known limits of this draft

1. It is a draft: the entry lands only when the L1 appends it, and its numbers are only as current as
   the receipts named beside them.
2. Draft A's claim bullets restate the frozen `after` list as the entry's *intended* state; a reader
   must not treat any un-substituted `⟨FILL⟩` as an observed value.
3. The verifier close-out block is deliberately empty of verdicts — this seat is not the non-author
   verifier and did not read any report.
4. The reusable skeleton in B.3 is a shape, not a measurement; its slots must be filled from the file
   it describes.
5. **The table is a snapshot, and it aged within the claim window.** At the closing read
   (`2026-10-26T06:40Z`, 40 s after the table's `06:38Z`) `.ufo/waves/round-35/claims-erratum-d5.md`
   already existed as an untracked file, and `assimilation/` had gained `collide-check.sh`,
   `collisions`, `guard-proof.txt`, `quarantine-verdicts.md`, `quarantine-slice-rederived`,
   `reg-ids`, `staged-ids`, `renumber-map-{pre,post}-c2.txt` and the two scratch-registry files.
   That is the D5 landing and the id-collision seat, not a contradiction of the table; the L1's
   quiescent read is the one that counts.
6. This receipt's own final bytes are not self-pinned (a file cannot carry its own digest, and any
   digest typed into it describes the revision before that line was written). The L1 records the
   committed digest; this seat's closing `wc` read `442` lines / `31477` bytes on the revision it
   was about to extend with this item.

### Report 6 — answer to `CritOverclaim-2`, and the superseding read (`06:43Z`–`06:44Z`)

Four overclaim challenges arrived after the first draft. Each was re-measured; three were correct
against the state at `06:38Z`, one was stale. Draft A was rewritten rather than annotated.

Superseding read (all `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin`):

```
$ grep -c 'supersedes R22' corpus/QUALITY.md ; grep -c 'supersedes R23' corpus/QUALITY.md   -> 0 ; 0
$ grep -c '^| R26' corpus/QUALITY.md                                                        -> 0
$ git ls-files .ufo/waves/round-34/wave1-results.json | wc -l                               -> 0
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                                                -> 18
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md                     -> 52
$ grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md                            -> 1
$ grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l                                   -> 1
$ ls corpus/knowledge/*.md | wc -l                                                          -> 47
$ grep -c 'did not file a receipt (dead seat' .ufo/waves/round-34/wave1/L1Integration.md    -> 1
$ grep -c 'Correction (round 35)' .ufo/waves/round-34/wave1/L1Integration.md                -> 0
$ python3 corpus/instruments/frontier-recheck-count.py | tail -2
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
entries=21 pass=21 exit=0
harness_exit=0        (2026-10-26T06:44:31Z)
```

Per challenge:

1. **Suite readings — accepted, and the draft now separates the trees.** The receipt itself records
   the live tree as `closed=4/7 exit=1` with `D4/D6/D7 open=1` (`ExecClosureSuite.md:68-75`) and says
   so in words: *"`closed=7/7 exit=0` on the live lane is not reachable from my seat"* (`:99`),
   *"`cases=7 failures=0` is reachable on these bytes through the frozen CLI; it is withheld on the
   live tree only because three limbs are not yet landed"* (`:263-265`). `closed=7/7` appears only in
   §5 (all-fixed tree) and §7 (its `--selftest`). Draft A now prints all four readings with their
   tree, and the final `closed=7/7` is a `⟨FILL⟩` for a post-integration run.
2. **D4 `tracked 0 → 1` — accepted.** `git ls-files … | wc -l` = 0 at `06:43Z`; the flip is the L1's
   commit, so the draft now says "still untracked … pending the L1's commit, which is the whole
   closure".
3. **D7 rows — accepted.** `0/0` on disk at `06:43Z`; the draft now says the draft rows
   (`ScribeQualityDraft.md`) are *not* landed rows, and the same for R26 (absent).
4. **Harness `entries=21` — the challenge was stale, and the draft now carries a live measurement
   instead of a receipt claim.** The harness reads `entries=21 pass=21 exit=0` **including**
   `PASS F18 knowledge/cisa-kev-catalog.md ids=S052` at `06:44:31Z`; `README` F-rows read **18**, not
   17, at that moment. An `entries=20 / 17 F-rows` reading describes the pre-F18 tree, which is the
   same state the frozen before-control recorded. `ExecRegressionC2.md` is indeed absent, so the draft
   still owes that quiescent regression receipt and says so.
5. **D6 check shape — accepted, and it is the sharper finding.** The critic's measurement matches the
   suite's own: `D6 check=dead-seat-sentence=1,correction-round-35=0 open=1`
   (`ExecClosureSuite.md:73`). Because the check requires the stale sentence **count to reach 0**, an
   appended correction cannot close it — the round-34 sentence must be rewritten in place, or the
   check must accept the erratum form. §Report F7 now states that fork explicitly and names it as the
   L1's decision; Draft A's D6 slot is worded to force the choice rather than to assume an append.

Nothing in this answer is derived from the critic's message except the questions; every number above
was re-read or re-run by this seat, and the harness run is labelled as this seat's own measurement.
No file outside `.ufo/waves/round-35/wave1/ScribeIntegrationNotes.md` was written, and the scratch
directory remained absent (`test -d …/ScribeIntegrationNotes` → `ABSENT`).
