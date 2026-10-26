# ExecNoHarmFinal — no-harm sweep of the landed bytes (round 35, wave 1)

Seat: `ExecNoHarmFinal` (leaf, read-only sweep). Lane: `kasegi-shokunin`, base
`3266c9937b03062d9bbc2f436e20820115ed179c`, claims freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`,
lane `HEAD` at sweep `da2d3c687f82a9814ee71c91c930cb733050d37c`. Nothing in the lane or the fleet root was
written by this seat; this receipt is its only write.

## Report

### Method and the honesty problem

The wave was **still landing while this seat swept**: four of the seven named files changed bytes inside
the sweep window, at least twice each. A single "the tree reads X" sentence would therefore be a
lie about a moving object, so every number here is bound to a **UTC timestamp and a file digest**, and
where a criterion was red at one sample and green at a later one, both samples are reported. This seat did
not fix anything (read-only item): findings are for the L1.

### T-series (UTC; lane file mtimes are UTC-3)

| sample | UTC | SKILL.md sha256 | SCORECARD.md sha256 |
|---|---|---|---|
| T1 | 2026-10-26T06:32:06Z | `ba5ebe5d9417b1801d48bbdb8fa533eb9df586f588bbad398eacd062e408163e` (= base bytes) | `29c91114f78f1544cbc72183c30c6f7bb2320f7fde274254977facd184b91d2d` |
| T2 | 2026-10-26T06:40:50Z | `daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc` | `51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7` |
| T4/T5 | 2026-10-26T06:41:09Z / 06:41:30Z | `daeff71b…` | `51337bf1…` |
| T6 | 2026-10-26T06:46:46Z | `daeff71b…` (stable) | `51337bf1…` (stable) |

T6 also shows `corpus/SOURCES.md` grown to `7 0` (sha `0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba`) —
the C2 seat was still appending registry/search-log lines, append-only throughout. `corpus/QUALITY.md` was
still byte-identical to base at every sample.

Intermediate bytes measured at 06:32:52Z and 06:36:55Z: SKILL.md `0cc9563824328a762b3acf168fe719101a9164cf64e51fcc6cccb8a8a23b5190`
(1104 lines) — this digest is what §2 F1 is about.

Other digests at T4 (unchanged from base ⇒ zero round-35 bytes):
`PROVINCE.md b4bb5fee0a37cb2a81e351ee837a3e23fc64fbe002dfb25e4688d0ed4782ff91` (= base),
`corpus/QUALITY.md 807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8` (= base),
`LOG.md 3a7300559eeab78ed364f600229f44e43c26b56862112b5ff3a88f81586ecae3` (= base),
`corpus/SOURCES.md 510e3bba977a744382438fdb7b79ecce90a75e1590f2491e9f373ab88d9b8829`,
`corpus/README.md 277f04cedfb06f493ae5da636d665b490ac0e78b26ea282b0d0ef3a469d3ffa2`.

### 1. density — mean and block/citation counts vs the round-34 recorded 201.2

```
$ python3 corpus/instruments/density.py SKILL.md            # T1 bytes (= base, sha ba5ebe5d…, 1091 lines)
# Density census — SKILL.md (1091 lines, 25 blocks)
| | **mean dens** | | | | | | | | **201.2** |
Total path-citation instances: 711 across 25 blocks.
exit=0

$ python3 corpus/instruments/density.py SKILL.md            # T2/T4 landed bytes (sha daeff71b…, 1104 lines)
# Density census — SKILL.md (1104 lines, 26 blocks)
| | **mean dens** | | | | | | | | **220.9** |
Total path-citation instances: 742 across 26 blocks.
exit=0
```

Round-34 recorded value, `corpus/lessons/round-34.md:546`:

> Post-append no-harm: `density.py SKILL.md` mean 201.2 (base 201.7,

Verdict: **the recorded 201.2 reproduces exactly** on the round-34 tip bytes (1091 lines / 25 blocks /
711 cites). The landed round-35 bytes read **220.9 / 26 blocks / 742 cites** — the D3 registry append is one
new high-density block, which raises the mean. That is a disclosed append, not a counter move; the 201.2
erratum must stay scoped to `3266c99:SKILL.md` and not be read as the round-35 number.

### 2. anchorcheck — failure classes

```
$ python3 corpus/instruments/anchorcheck.py SKILL.md        # T1 bytes (base, ba5ebe5d…)
== SKILL.md: 12 in-range cite instances, 0 bad; 12 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
exit=0

$ python3 corpus/instruments/anchorcheck.py SKILL.md        # intermediate bytes (0cc95638…)
== SKILL.md: 15 in-range cite instances, 0 bad; 15 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=1
BASE-ABSENT md:1097 S050.txt:70 (base tree absent: /home/vgpnk/Projects/the-bounty-hunter/S050.txt)
exit=1

$ python3 corpus/instruments/anchorcheck.py SKILL.md        # T4/T5 bytes (daeff71b…)
== SKILL.md: 16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
exit=0
```

Verdict on the landed bytes: **criterion met** — `LOST-RECORDED=306, PIN-BROKEN=0, ORIGIN=0,
OUTSIDE-BASE=0, BASE-ABSENT=0`, exit 0, exactly the five numbers the item names. But it was **not** met for
~8 minutes: the D3 registry append first carried a bare `` `S050.txt:70` `` and that single token re-armed
the `BASE-ABSENT` fail class (see F1). It is now `corpus/source-snapshots/round-32/S050.txt:70` in the row
at `SKILL.md:1097`.

**Instrument hazard (F6).** Both instruments resolve relative to the lane root. Run from a copied tree the
same bytes report a *false* failure:

```
$ (cd /fast/scratch/…/snap && python3 …/anchorcheck.py SKILL.md)
BASE-ABSENT=11 … exit=1     # every lane-relative cite reads "base tree absent"
```

Any verify-elsewhere harness must copy the tree **and** keep the lane root, or it will manufacture eleven
defects.

### 3. append-only (`git diff --numstat <base> -- …`)

```
$ git diff --numstat 3266c99 -- SKILL.md PROVINCE.md corpus/README.md corpus/SOURCES.md corpus/QUALITY.md SCORECARD.md LOG.md
33	15	SCORECARD.md
13	0	SKILL.md
28	0	corpus/README.md
7	0	corpus/SOURCES.md
```

(`SOURCES.md` read `5 0` at T4 and `7 0` at T6 — append-only both times.) The T1 reading of the same
command was `6 5 SCORECARD.md` only — the tree moved while measuring; `PROVINCE.md`, `corpus/QUALITY.md` and
`LOG.md` have **zero** changed lines at every sample, i.e. no round-35 bytes.

**Six of the seven are append-only. SCORECARD.md is not: 15 deletions.** All 15 deleted lines are one
region — the round-34 section's intro paragraph plus its "final lane commit" paragraph:

```
-`c2-controls/before.txt`) and `census-before.txt`. **Final lane commit: the L1 fills this line in the
-closing commit.** This section is written at the wave-1 integration state on the bytes digested under
-§ Measurement state, claims no lane-commit hash, and deliberately introduces no placeholder token —
-round-33 R1's defect was a published placeholder, the C1 counter reads that count as 0, and nothing
-here moves it. Receipts land under `.ufo/waves/round-34/` (`c1-controls/`, `c2-controls/`,
-`census-before.txt`, `claims-erratum-1.md`, `assimilation/`, `wave1/`; 58 seat receipts at this
-seat's read). The last round heading at this round's base is round 33, so C1's and C2's last-change
-column stays 33 and every before-column below is the frozen control measured at this round's base
-bytes. The round-34 subject is instrument-soundness closure for the nine round-33 verifier-routed
-defects R1–R9 (C1) and frontier F17 / Immunefi Vulnerability Severity Classification System v2.2
-(C2).
-**Round-34 final lane commit: filled by the L1 in the closing commit.** Every value in this section
-was measured at the wave-1 integration state on the quiescent bytes digested under § Measurement
-state; the closing commit may add seat receipts, `LOG.md`, `SHONEN.md`, `corpus/lessons/round-34.md`
-and this section itself, none of which any counter above reads.
```

replaced by 33 lines that carry the real tip hash `c1c6a5f826d2425446347173de527c42991b78b0` and a note
that the prose "originally carried the placeholder prose this hash replaces … the round-34 R1 check missed
[it] because it matched only the `<LANE_HASH>` spelling". Content check: no *measured value* in the file
changed (before/after columns, evidence tuples, digests are untouched); what was deleted is the round-34
record's own false self-description. So the deletions are not a measurement harm — but the file is no
longer append-only, and the deleted sentences are consequently recoverable only from git
(`3266c99:SCORECARD.md`, `c1c6a5f:SCORECARD.md`), not from the worktree.

### 4. lane working tree (`git status --porcelain`)

```
 M .ufo/waves/round-35/build-spec.py            (749 0 vs base — L1/dispatcher spec, not a seat stray)
 M SCORECARD.md                                 (33 15 — §3)
 M SKILL.md                                     (13 0   — D3 registry append)
 M corpus/README.md                             (28 0   — F18 row)
 M corpus/SOURCES.md                            (5 0    — S052 row)
 M corpus/instruments/knowledge-expected.txt    (1 0    — C2 expected-list)

?? .ufo/waves/round-34/wave1-results.json               (+ `…json.provenance.md`, same dir)
?? .ufo/waves/round-35/{assimilation/,c1-controls/fake-suite.sh,c2-controls/junk-f18.md,
                        claims-erratum-d5.md,wave1.ready,wave1.ready.dispatched,wave1/}
?? corpus/instruments/r35-defect-closure.sh
?? corpus/instruments/r35-fixtures/
?? corpus/knowledge/cisa-kev-catalog.md
?? corpus/source-snapshots/round-35/
```

Every entry is either a wave path, a named receipt/control, or a round-35 artifact the claims require —
**no stray scratch or fixture tree inside the lane**. `corpus/instruments/__pycache__` exists but is
ignored (`.gitignore:2`). Both D4 files are still **untracked** at T5: `git ls-files
.ufo/waves/round-34/wave1-results.json | wc -l` → `0` (D4 stays open until the L1 commits — F3).

### 5. fleet-root misroot check

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
?? .ufo/state/disk-guard.log                    (only untracked; rolling monitor log, 12199 lines)
157 x " A "  (pre-existing staged: `.tower/comms/**` round-18 material, `.scratch/…`, …)
19  x " M "  (.ufo/state/*.report-baseline — kasegi's moved 27→35, i.e. the round marker;
              .ufo/watchdog.log; scripts/hyaku/{hyaku.env,lane-addendum.md})
```

No `.ufo/waves/round-35` at the fleet root and **no lane-artifact name at the fleet root**
(`SKILL.md`/`SCORECARD.md`/`QUALITY`/`SOURCES`/`wave1`/`claims` all clean there at T5). The only ` M
SCORECARD.md` seen at the fleet root was **transient**, as were two untracked directories:

- 2026-10-26T06:31:5xZ — fleet status showed ` M SCORECARD.md`, `?? census/`, `?? tests/`
- 2026-10-26T06:32:20Z — all three gone/reverted (`ls` → no such file), and they stayed gone.

Recorded because a transient untracked `census/`/`tests/` at the fleet root is exactly the misroot
signature this check hunts; no round-35 seat claims those paths, and the fleet-root `SCORECARD.md` diff was
empty at the next read. **Nothing for the L1 to sweep on names alone; the two transients are unattributed.**

### 6. Supplementary: the C1 closure counter itself (read-only runs)

Not required by the item, but it is the counter every other check feeds, so it was run:

```
$ bash corpus/instruments/r35-defect-closure.sh                     # live, T2 and T5
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=0,provenance=1 open=1
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=4/7 exit=1

$ git archive 3266c99 | tar -x -C <scratch>/base
$ bash corpus/instruments/r35-defect-closure.sh --root <scratch>/base
all seven Di open=1  →  closed=0/7 exit=1        # the claim's base control reproduces

$ KASEGI_SCRATCH=<scratch>/closure bash corpus/instruments/r35-defect-closure.sh --selftest   # 06:37
selftest problem=fixture-missing id=D5 path=corpus/instruments/r35-fixtures/D5
selftest problem=fixture-missing id=D6 …
selftest problem=fixture-missing id=D7 …
selftest problem=control-missing path=corpus/instruments/r35-fixtures/clean
selftest problem=control-missing path=corpus/instruments/r35-fixtures/two-defect/D1D2
selftest case=D5 live=pass fixture=unusable mutants=2/2 verdict=fail
selftest cases=7 failures=7 control-failures=1        exit=1
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=short-report rejected=1
selftest judge=fake-suite rejected=1 path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0
selftest judge=fake-plain rejected=1 output=closed=7/7 exit=0
```

Reading: the suite is a **real** gate (base 0/7, live differs from base, and all five forgery limbs reject a
forged summary, forged baselines, a short report, the fake suite and a fake `closed=7/7` plain run). It is
red at T5 and again at T6 (06:46:46Z, same seven lines) only on integration-order items: D4 needs the
L1's commit, D6 and D7 are not landed (`QUALITY.md` digest = base digest, zero round-35 edits). The
`--selftest` failure is the same three open checks plus fixtures/controls not yet on disk; it must be
re-run after integration, not read as a verdict.

### Findings for the L1

| id | state | what | action |
|---|---|---|---|
| **F1** | closed in flight | D3's registry append first carried a bare `` `S050.txt:70` ``; `anchorcheck.py SKILL.md` read `BASE-ABSENT=1 … exit=1` at `md:1097` on SKILL digest `0cc95638…` (06:32:52Z – 06:40:50Z). Fixed to `corpus/source-snapshots/round-32/S050.txt:70` by digest `daeff71b…`; exit 0, all five classes clean. | none for correctness; worth a lesson/mistake row — a registry row that *quotes a bare filename* re-arms a fail class the registry exists to keep at 0, and the suite's own red/green transition is the proof the instrument works. |
| **F2** | **open, L1 decision** | `SCORECARD.md` is **not append-only**: 33 insertions / **15 deletions**, all in the round-34 § intro + "final lane commit" paragraph, rewritten in place to carry `c1c6a5f…`. The same round's own D2 clause (`r35-defect-closure.sh` header) demands the opposite discipline for the density row: "corrected by appending, not by rewriting it in place". | decide: accept the in-place correction (it is truthful and the appended `Erratum (round 35)` at `:1246` discloses it) **or** restore the round-34 text and carry the correction only as appended rows. Do not leave the claim text ("append-only, 0 deletions") standing unqualified against a 15-deletion diff. |
| **F3** | open, integration-order | `closed=4/7 exit=1` at T5 **and T6**: D4 `tracked=0` (both results file and provenance note untracked; `git ls-files … | wc -l` = 0), D6 (`correction-round-35=0`), D7 (`supersedes-R22=0, supersedes-R23=0`, `QUALITY.md` untouched). | commit D4's two files; land D6/D7; then re-run the suite to 7/7. |
| **F4** | hazard, now clean | At 06:32:52Z `grep -c 'filled by the L1' SCORECARD.md` = **1** (the untouched `:1241` header line) and `grep -c '<LANE_HASH>'` = **1** — the D1 correction *quoted* the token it is required to eliminate. Both are 0 at T4 (`placeholders=0,lane-hash-markers=0`). | none; record the pattern: prose that quotes a forbidden token re-arms its literal counter, so a counter's kill rule must be re-read against the correction that closes it. |
| **F5** | corroboration | The D2 erratum is **byte-true**: `SCORECARD.md:1248-1252` claims the 201.2 limb is `3266c99:SKILL.md` `ba5ebe5d…`, 1091 lines, 711 cites, 25 blocks; this seat's independent census of those exact bytes returns 1091 / 711 / 25 / mean 201.2. | none — cite this receipt as the independent reproduction of the 201.2 limb. |
| **F6** | instrument note | `anchorcheck.py`/`density.py` are lane-root-relative; a copied-tree run reports `BASE-ABSENT=11 exit 1` on clean bytes. | verification seats must run in-lane (or `--root` the lane), never on a bare copy. |
| **F7** | fleet root clean | only `?? .ufo/state/disk-guard.log`; 157 staged + 19 modified are pre-existing/state files (`.report-baseline` 27→35 is the round marker); transient `?? census/`, `?? tests/` and ` M SCORECARD.md` at 06:31:5xZ were gone by 06:32:20Z and are unattributed. | nothing to sweep by name. |

### Re-run list at integration (for the L1)

1. `bash corpus/instruments/r35-defect-closure.sh` → `closed=7/7 exit=0` (T5/T6: `4/7`, D4/D6/D7 open)
2. `bash corpus/instruments/r35-defect-closure.sh --selftest` → `cases=7 failures=0` (T-selftest: `7`, fixtures/controls missing on disk)
3. `python3 corpus/instruments/anchorcheck.py SKILL.md` → exit 0, `LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` (green at `daeff71b…`; red at `0cc95638…`)
4. `python3 corpus/instruments/density.py SKILL.md` → expect **220.9 / 26 blocks / 742 cites** at `daeff71b…`; keep the **201.2** erratum bound to `3266c99:SKILL.md`
5. `git diff --numstat 3266c99 -- SCORECARD.md` → **15 deletions** unless F2 is resolved
6. `git ls-files .ufo/waves/round-34/wave1-results.json | wc -l` → `1` after the commit (T5/T6: `0`)

### Tooling, scratch, limits

- Tools installed/upgraded: **none** (no install was needed; `pacman` untouched).
- Scratch: `/fast/scratch/hyaku/kasegi-r35/ExecNoHarmFinal/` (snapshot + instrument outputs + base
  extraction) — **removed** at close, receipt copied to the wave dir first.
- Limits: this is a point-in-time sweep of a moving tree, not a verdict on C1; every red cell above is
  re-runnable with the listed command and the digest it was measured on. Deterministic, no network.
