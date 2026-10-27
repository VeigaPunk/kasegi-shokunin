# MutPredicates — round-41 wave-1 receipt (mutation-tester, leaf)

Seat: `MutPredicates` (mutation-tester, leaf — no subagents dispatched, one labrat not needed).
Wave: kasegi-shokunin round 41, dispatched by KasegiR41 (L1). Item: **receipt-only** —
attempt to satisfy each frozen predicate with the cheapest possible cheat, in scratch;
walk each kill-rule clause; name every hole; propose the minimal limb fix.
Axes touched: **depth:verifiability** (primary), **coverage**. No lane, fleet, or
source-tree file was edited; no subagents; no tool installs; no network fetches
(the C2 cheat's whole point is that none are needed). Read-only git only.

Everything below was run against scratch fixtures under
`S=/fast/scratch/hyaku/kasegi-r41/MutPredicates` (removed at yield, trap-verified).
Lane repo touched: none (only this receipt written, in the wave dir).

Reference hashes (verified to resolve, read-only):
- base `5b29ea1439450b712581edf5f0f0bf98dfb262ab` resolves. The 38-char literal
  `5b29ea1439450b712581edf5f0bf98dfb262ab` printed in claims.json resolves to
  NOTHING (`git rev-parse --verify` fails) — independently confirming the
  freeze-typo erratum already mined by ScribeShonenLog in c1-controls/do-nothing.txt.
- round-40 judged head `c7aea5ef97902f38289cbdc1cf267068876a62dd` resolves.

---

## C1 — cheat attempts against the r41-closure.sh predicate

### Cheat A — the naive 34-line unconditional suite (KILLED)

`c1/fakeA/r41-closure.sh` (34 lines, sha256
`eb4c693f0e5d3d2b1d7f062e881631687d1591a91c824edafa4938389a6589c0`): refuses a
plain run with exit 2; for ANY `--export-ref` prints twelve
`I<n> payload=fake,cheat closed=1` lines + `closed=12/12 exit=0` (rc 0);
`--selftest` prints twelve graded `selftest case=I<n> positive=pass mutants=1/1
verdict=pass` lines + `selftest cases=12 failures=0`. No export is ever read.

Actual runs:

```
$ bash fakeA      → "refused: export mode only (pass --export-ref)"  rc=2
$ bash fakeA --export-ref 5b29ea1439450b712581edf5f0f0bf98dfb262ab --lane <lane>
  … I11 payload=fake,cheat closed=1 / I12 payload=fake,cheat closed=1
  closed=12/12 exit=0   rc=0          ← REAL base export
$ bash fakeA --export-ref c7aea5ef97902f38289cbdc1cf267068876a62dd --lane <lane>
  closed=12/12 exit=0   rc=0          ← REAL round-40 judged head export
$ bash fakeA --selftest --export-ref deadbeef…   → 12 graded lines, cases=12 failures=0
```

Kill: C1 kill-rule clause **"the base or round-40 judged head export prints
closed=12/12"** fires on both real negative controls. The naive cheat is dead on
arrival. Verdict: **KILLED (clause K4)**.

### Cheat B — the 51-line content-gated suite (passes all five counting commands; KILLED only by the committed-fixture clause)

Natural escalation after Cheat A: gate green on *artifact presence* in the export
(mirroring the real suite's export mode: `git -C <lane> archive <ref> | tar -x`),
but stay blind to every defect class. `c1/fakeB/r41-closure.sh` (51 lines, sha256
`71b8e828948da8c2d59913a6f6fdabc1af848ce033f0e976d696b0fa05a30abe`) greens iff the
export contains `corpus/instruments/r41-closure.sh` AND `grep 'Correction (round 41)'`
hits SCORECARD.md, LOG.md and SHONEN.md; otherwise prints `closed=11/12 exit=1`
(rc 1). Selftest prints the twelve graded lines unconditionally.

Fixture repo (`c1/fix2`, `git init`, toplevel asserted before every commit, fixture
identity `MutPredicates-fixture <mutpredicates.fixture@local>`):

```
43381057609b14b24aebd954f4537ac7b098795a  r40h: round-40-like tree (no r41 suite/corrections)
7e0429dec163f0a2a1e65dfefe4ba05e68df288c  j1:    fake suite committed + 3 Correction lines
                                          + well-formed SKILL.md registry row + declared-blocks
                                          + PROVINCE append (NO receipt)
28c08208313c6623602f988f1d4970f75588139f  y1:    j1 + .ufo/waves/round-41/final-gates/all-gates.txt
```

Run matrix (all actual output):

| probe | result |
|---|---|
| plain run | `rc=2` (refused) |
| `--export-ref Y1` | `closed=12/12 exit=0` rc=0 |
| `--selftest --export-ref Y1` | 12 graded case lines, `selftest cases=12 failures=0` rc=0 |
| `--export-ref r40h` (fixture) | `closed=11/12 exit=1` rc=1 |
| `--export-ref 5b29ea14…f0f0bf98dfb262ab` (REAL base) | `closed=11/12 exit=1` rc=1 |
| `--export-ref c7aea5ef…` (REAL r40 head) | `closed=11/12 exit=1` rc=1 |
| receipt byte-identity: re-run at Y1, `cmp` vs committed `all-gates.txt` | BYTE-IDENTICAL |

**Cheat B passes every frozen counting command and the receipt-tee clause.** What
kills it: only the committed-fixture clause. Four defect-class fixtures, each
committed on top of Y1 (detached, object store verified: `git cat-file -t commit`
for all four):

| defect commit | injected class (named limb) | fake B output | real I-limb must |
|---|---|---|---|
| `c0853b25…` y_t2 | T2 substring values `closed=7/80` + `failures=10` written into the SCORECARD Correction line (I3) | `closed=12/12 exit=0` rc=0 | RED |
| `3626d7eb…` y_t4 | Correction line wrapped in a ```` ```text ```` CommonMark fence (I4/T4) | `closed=12/12 exit=0` rc=0 | RED |
| `f7e04ab7…` y_t7 | `declared-blocks.txt` declares `pwn`, a symlink resolving outside the export (I5/T7) | `closed=12/12 exit=0` rc=0 | RED |
| `fc0a8ea5…` y_t13 | SKILL.md registry row replaced by a mention-only prose row (I7/T13) | `closed=12/12 exit=0` rc=0 | RED |

…and the graded selftest is mutation-blind too: on the y_t2 tree it prints
`selftest cases=12 failures=0` (twelve `positive=pass`) with the T2 defect present.

### C1 kill-rule clause walk (Cheat B vs every frozen clause)

| clause | catches Cheat B? | evidence |
|---|---|---|
| K1 suite absent from Y export | no — suite committed at j1 | export contains it |
| K2 Y export prints closed≠12/12 or exit≠0 | no | `closed=12/12 exit=0` rc=0 |
| K3 selftest <12 graded lines / failure / summary-only-satisfies-a-case | no | 12 graded lines, 0 failures |
| K4 base or r40-judged-head export prints closed=12/12 | no | both red `11/12 exit=1` (this is the clause that killed Cheat A) |
| **K5 committed fixture shows a check passing while its defect is present** | **YES — the only catch** | y_t2 / y_t4 / y_t7 / y_t13 all green (table above) |
| K6 Correction set does not grade r40 C1 not-verified + name firing evidence | content clause, not suite logic | a cheater landing plausible Correction lines passes; suite blindness still falls under K5 |
| K7 census exit≠0 / new W/E code | no — side condition | census stays green if rows are well-formed (proven under C2 below) |
| K8 working tree not clean at filing | no — hygiene | satisfiable |
| K9 kasegi-r41* scratch sibling at filing | no — hygiene | satisfiable (and CritKillRule F1/F2 showed even the real scan is geometry-sensitive) |
| K10 receipt not byte-identical to the teed transcript | no — deterministic fake | `cmp` BYTE-IDENTICAL |

### C1 holes and minimal limb fixes (for the L1)

- **H-C1-1 (the one that matters): the five frozen counting commands alone cannot
  kill Cheat B.** Every command passes; K5 fires only when someone runs committed
  defect fixtures *through the suite* — which today lives in wave-2 falsify seats,
  not in the frozen commands. Minimal fix: make K5 operational inside the frozen
  commands — the graded selftest must consume the **committed** kill fixtures (the
  `corpus/instruments/limb-fixtures/` + ledger machinery wave-1 is already
  building) and the receipt at Y must carry per-fixture lines
  `selftest detail=I<n> mutant=<committed-fixture-id> rejected=1`. Then counting
  command #2 (`--selftest --export-ref Y`) transitively enforces K5 and Cheat B
  dies at the frozen-command layer. Keep the round-40 patterns the r41 predicate
  text does not mention but the r40 selftest had: `selftest judge=` forgery
  rejections and per-case `detail=` lines, so the selftest transcript is externally
  auditable without re-running anything.
- **H-C1-2: I10's killable acceptance predicate is the load-bearing clause for the
  whole negative-control architecture.** Cheat B fakes red negative controls by
  gating on artifact presence; the real suite must reject a leaf-capped green base
  by a *real numeric comparison* (the MutH6H10 D2/M-H8a class). Fixture that in the
  committed set, or a future content-gated fake that hardcodes `closed<12/12` for
  the two known negative refs survives K4 as well.
- **H-C1-3 (minor):** the r41 selftest text in the claim has no summary-vs-case
  cross-check and no case-name multiset check; kill-rule-check.py already
  implements both for other instruments — reuse it verbatim for r41-closure.sh.

**C1 verdict: Cheat A KILLED (negative controls, demonstrated on the real base and
real r40 judged head). Cheat B KILLED only by the committed-fixture clause
(demonstrated on four named defect classes). No other frozen clause catches a
deterministic content-gated fake — the frozen counting commands must be made to
transitively enforce K5 or the cheat class survives the command layer.**

---

## C2 — cheat attempt: junk S063 capture, full fabricated row/entry/manifest

Assignment: registry S063 mined + README F24 admitted + entry with provenance trio
+ manifest record — but a **FAKE capture (echo junk)**. Does source-recheck pass?
**Yes. Everything passes.**

Fixture (`c2/fix`): the REAL base tree (`git -C <lane> archive
5b29ea1439450b712581edf5f0f0bf98dfb262ab | tar -x`), then the cheat:

- `printf 'junk junk junk junk junk junk junk\n' >
  corpus/source-snapshots/round-41/S063.txt` (35 bytes, sha256
  `367bd7b29ba29a4981bbd94745b1c622509c0a2ad728a951436309b64af1e829`) — the literal
  echo-junk capture.
- `manifest.json` record written by hand: id S063, path S063.txt, url
  `https://www.rfc-editor.org/rfc/rfc9116.txt`, sha256 = the junk's, one quote
  `"junk junk junk junk junk"`, `fetched_utc: 2026-10-27T09:30:00Z`, http status
  200, and a `tool` field **claiming a reproduction fetch that never happened**.
- S063 registry row inserted INSIDE the `## Registry` table (after S062) —
  appending at EOF trips census E12, a placement subtlety a real miner gets right.
- README F24 row (`admitted`, entry + sources S063), PROVINCE F24 amendment,
  knowledge entry `rfc-9116-security-txt.md` with the full trio
  (`source: S063` / `verified-at: 2026-10-27` / `recheck: cd <fixture> && python3
  corpus/instruments/source-recheck.py --manifest … --source S063`), entry added to
  `knowledge-expected.txt`, and the 66 absolute lane paths inside the copied
  entries' recheck lines rewritten to the fixture root (otherwise recheck-audit's
  `cdroot` strict limb reds on the copy — a fixture-fidelity step, not part of the
  cheat).

Consolidated run — actual outputs:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-41/manifest.json --source S063
S063:sha256 OK
S063:q1 OK occurrences=1
rc=0                                            ← source-recheck PASSES on junk

$ python3 corpus/instruments/capture-binding-check.py --root .
… MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0
records=55 bound=55 unbound=0                   rc=0

$ python3 corpus/instruments/frontier-recheck-count.py --root .
PASS     F24  knowledge/rfc-9116-security-txt.md   ids=S063   exit=0
entries=27 pass=27 exit=0                       rc=0

$ python3 corpus/instruments/recheck-audit.py --quiet --root .
lines=60 total=60 pass=60 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=60 missing=0 unexpected=0 exit=0      rc=0

$ bash scripts/sources-census.sh validate --file corpus/SOURCES.md
W04 S028 … ; W04 S029 … ; ok                    rc=0   (only the standing W04 pair)

measure: (20+F_admitted)/(20+F_total) = 44/44 = 1.000, queued=0
counting greps: frontier 24, registry 63, S063-mined 1, entries-citing-S063 1, knowledge 60
```

Every frozen C2 counting command prints its after-state value off a junk capture.

Negative baselines (the limbs themselves work — the hole is not broken instruments):

```
N1 capture one byte flipped → S063:sha256 MISMATCH … rc=1
N2 fetched_utc stripped     → FAIL rule=provenance-missing record=S063 …
                              records=55 bound=54 unbound=1 rc=1
N3 pinned quote absent      → S063:q1 MISMATCH reason=quote-not-found rc=1
```

And the O4-class control the c2 before-file names (mined row WITHOUT
capture+entry) fails as claimed there — my probe is the complement the before-file
does not cover: junk WITH self-consistent capture+entry+harness pass.

### C2 hole and minimal limb fixes (for the L1)

**Hole: no instrument anywhere in the C2 stack compares capture bytes to the live
source, or to any out-of-band ground truth.** source-recheck pins the manifest to
the file; capture-binding pins the manifest to the registry row (id + byte-equal
URL + strict-UTC `fetched_utc`); frontier-recheck runs the entry's recheck line;
recheck-audit checks line form; census checks row shape. All five verify *internal
consistency of committed bytes*. The `tool` field's reproduction sentence and the
entry's `verified-at` date are unverified assertions — capture-source.py itself
documents that it "does not establish that the source is current today". The C2
kill rule's junk-twin clause only names "a mined-marked row WITHOUT
capture+entry+harness pass" (round-40 O4); a junk capture WITH all three passing is
accepted by every automated limb.

Cheapest-to-strongest fixes:

1. **F1 (verification-side, no new code — recommended):** add one frozen C2
   counting command for any round that mines a source: re-run
   `python3 corpus/instruments/capture-source.py --id S063 --url <registry URL>
   --out $TMP/S063.txt` at verification time and require its printed snapshot
   sha256 to equal the manifest `sha256` (the tool already prints sha256, byte
   count and UTC fetch instant for exactly this binding). One fetch per newly
   mined row per round; a host that cannot be reproduced gets a named
   `fetch-unreproduced` W-code + human review, not a silent pass. This kills both
   naive and crafted junk; it also subsumes the O4 clause.
2. **F2 (instrument-side):** extend capture-binding-check.py with an opt-in
   `--live` reproduction rule (offline `validate` keeps passing; the frozen
   verification run enforces it), so the check is repeatable instead of a manual
   L1 step.
3. **F3 (cheap sanity, not sufficient alone):** let a manifest record pin an
   `identity` regex (e.g. `Request for Comments: 9116`) that source-recheck
   requires in the capture — kills naive junk instantly, crafted junk never.
4. **F4 (clause widening):** amend the C2 kill rule's junk-twin clause to
   "…or a capture whose bytes fail reproduction against the row URL", so the
   frozen text matches what F1/F2 enforce.

**C2 verdict: cheat SURVIVES every automated limb (demonstrated end-to-end:
source-recheck rc=0, binding 55/55, harness 27/27 incl. PASS F24 ids=S063, audit
60/60, census rc=0, measure 44/44). This is a live coverage hole in the frozen
C2 predicate, not a broken instrument — all negative baselines fire. The minimal
closing move is a verification-time reproduction fetch (F1), optionally frozen as
an instrument rule (F2) and a widened kill clause (F4).**

---

## Hygiene / conduct

- Writes: this receipt only. No byte-deliverables (receipt-only item; all probes
  lived in scratch). No lane/fleet/source-tree file edited; `git status` in the
  lane shows zero tracked modifications (only the pre-existing untracked `.ufo`
  wave files plus this receipt).
- Git: read-only against the lane (`rev-parse`, `archive`, `log`, `status`,
  `cat-file`); the only commits are inside the two scratch fixture repos
  (`c1/fix2`, and none in `c2/fix` — a plain extracted tree), toplevel-asserted,
  fixture identity `MutPredicates-fixture <mutpredicates.fixture@local>`.
- No mutating git/jj anywhere else; no subagents; no installs (nothing needed —
  pacman untouched, host-wide pause irrelevant); **no network fetches at all**:
  the C2 cheat works precisely because no instrument fetches.
- Tools used (preinstalled system): GNU bash 5.3.20(1), git 2.56.0, Python 3.14.8.
- Disk guard green before and after (`/fast/scratch/hyaku` 24%, ~611G free).
- Scratch `S` removed at yield (`trap 'rm -rf -- "$S"' EXIT` semantics — removal
  verified after the receipt was copied here); no `kasegi-r41*` sibling survives
  from this seat.

## Verdict summary

| probe | cheat | outcome | catching clause / hole |
|---|---|---|---|
| C1-A | unconditional 34-line suite | KILLED | K4 negative controls (real base + real r40 head both printed 12/12) |
| C1-B | content-gated 51-line suite | KILLED, but only by K5 | passes all 5 counting commands + receipt tee; green on 4 committed defect classes (T2/T4/T7/T13) |
| C2 | junk S063 capture + full fabricated row/entry/manifest | **SURVIVED all automated limbs** | hole: no live-content/reproduction limb; fixes F1–F4 proposed |

Bottom line for the L1: the C1 architecture holds *only if* the frozen commands
transitively enforce the committed-fixture clause (selftest over committed kill
fixtures with per-fixture `detail=` lines in the receipt). The C2 architecture as
frozen admits fabricated captures; one reproduction fetch per newly mined row
closes it for the cost of a single HTTP GET per round.
