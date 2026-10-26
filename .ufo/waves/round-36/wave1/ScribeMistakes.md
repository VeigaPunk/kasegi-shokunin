# ScribeMistakes — round-36 `## Mistakes` rows M36-1..M36-4 (draft; the L1 integrates)

Seat: `ScribeMistakes` (scribe, leaf). Lane `kasegi-shokunin`, round 36, wave `kasegi-r36-build`.
Lane base `cc692008b0cfd58d18275aa6c4aed79620120799`; claims-freeze commit
`b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`; lane `HEAD` = `b47f2cd` unless a command names another
revision. Measurements taken `2026-10-26T15:37Z`; time-sensitive values carry their instant.

This file is the row set for `corpus/lessons/round-36.md` `## Mistakes`. It is not the lesson and it
carries no round verdict. Field order: id · class (kaika §5 vocabulary) · event · evidence (command →
output) · captured-by · fix · fix shown able to fail. Per this seat's item spec, M36-2/M36-3/M36-4
name a **criterion** in `captured-by` (R16 / R17-limb+R11 / R4); M36-1 is `none (new)`.

**Landed-state rule.** Every "fix" field states whether the fix exists in committed bytes at the
measurement instant. Three of the four fixes depend on artefacts that **do not exist yet** in this
wave (`.ufo/waves/round-36/wave1/ScribeMistakes.md` is the only file this seat may write), so their
entries read *not landed* with an owner and a closure command. Nothing below upgrades a contract into
a measurement.

---

## 1. The table

| id | class | event (one clause) | evidence | captured-by | fix (state at 15:37Z) | able to fail (red → green) |
|---|---|---|---|---|---|---|
| **M36-1** | landing / closure-order | Round-35's lane kept writing and committing claim-bearing paths after the driver printed `complete kasegi round=35` (04:00:34) — M35-1's class recurring on the next round. | `watchdog.log:1495` complete 04:00:34; commits 8ce6fb4 04:01:12, 5a25337 04:02:21, bb2dc8c 04:04:46, 48e6053 04:04:55, 980aa3d 04:19:52; judged head `0aee0ef` has 0 S052 captures. | `none` (new) — **criterion missed: R4** | *Not landed*: `corpus/instruments/r36-closure.sh` absent (`git ls-tree -r b47f2cd | grep -c r36-closure` → 0). Contract: E9 quiescence gate + export-bound suite. Owner: C1 suite seats / L1. | scratch fixture: clean tree `git status --porcelain \| wc -l` → `0` (green); tree with 1 modified + 1 untracked → `2` (red). Live red now: 49 leftover seat dirs. |
| **M36-2** | stale-premise | The round-35 lesson `## Gate` line claims "source-recheck exit 0 on committed bytes" for S052 while the capture it names was not committed at the judged head; the same `## No-harm` bullet's numstat claims are also false there. | `git show 0aee0ef:corpus/lessons/round-35.md \| grep -cF 'source-recheck exit 0 on committed bytes'` → **1**; capture tracked at A → **0**; instrument over the A export → `S052:source UNAVAILABLE reason=missing` **exit 2**. | R16 (result paragraph closure) | *Not landed*: `corpus/lessons/round-36.md` absent (`ls` → No such file). Contract: E8 correction recorded in the round-36 lesson. Owner: round-36 lesson seat / L1. | A=`0aee0ef` → exit 2, 0 capture bytes (red: sentence false); B=`5a25337` → `sha256 OK` + Q1–Q5 `OK … anchor=N-ok`, exit 0, capture tracked (green: sentence true). |
| **M36-3** | counter-discrimination | The round-35 suite's own D3 registry row never landed; the loose literal `r-defect-closure` was satisfied by the near-name sibling, so the counter scored the defect closed with the exact basename absent. | `grep -cF 'r35-defect-closure.sh' SKILL.md` → **0** (0 at `0aee0ef` too); stem `r-defect-closure` → **4** lines / **9** occurrences (`:1097`=5, `:1100`=1, `:1102`=1, `:1104`=2); the `.sh` form → 3 lines / 8 occurrences; near-name row at `SKILL.md:1097`. | R17 limb / R11 (discrimination) | *Not landed*: same grep for `r36-closure.sh` → **0**. Contract: E3 exact-basename rows for r35 **and** r36 + mutant. Owner: C1 suite seats / L1. | fixture holding only the near-name row → exact 0 / near 1 (red, check open=1); after appending both exact rows → exact r35 **1**, exact r36 **1** (green). Live `SKILL.md` is the red fixture. |
| **M36-4** | landing | The round-35 report did not land once, last: it was re-filed three times after `complete`, the third time only after the lane's wave-done commit. | fleet `git log -- .ufo/reports/round-35/kasegi.md` → e4eb5140 04:00:23, 63ce2a63 04:01:19, 8cfcb5b6 04:02:33, 375f9514 04:20:03; complete 04:00:34. | R4 (landed = committed and pushed) | *Not landed for round 36* (no report yet). Contract: full integration before the single report commit; report lands last. Owner: L1. | epoch predicate `report_ct ≥ max(lane_ct)`: red at e4eb5140 (1792998023 < 1792998295) and at 8cfcb5b6 (1792998153 < 1792999192); green only at 375f9514 (1792999203 ≥ 1792999192) — green bought by re-filing. |

---

## 2. Per-row evidence, verbatim

### M36-1 — closure order (M35-1 recurrence)

Watchdog (fleet root, read-only; the log is mutable, so the spot-check's frozen copy is cited too):

```
$ sed -n '1490p;1495p' /home/vgpnk/Projects/shokunin/.ufo/watchdog.log
2026-10-26T03:26:29-03:00 launch kasegi round=35 pgid=2458141 driver=hyaku-inline attempt=1
2026-10-26T04:00:34-03:00 complete kasegi round=35; hyaku-inline attempt=1
```

Committed work after that line (lane repo):

```
$ git log -1 --format='%h %cI %s' 8ce6fb4f 5a253372 bb2dc8c 48e6053 980aa3d 0aee0ef
8ce6fb4 2026-10-26T04:01:12-03:00 round-35: D1 closure fix — scorecard closing-commit wording
5a25337 2026-10-26T04:02:21-03:00 round-35: commit wave leftovers — S052 capture (named >1MiB), SKILL registry, controls, ready markers, receipts
bb2dc8c 2026-10-26T04:04:46-03:00 round-35: receipt finalization — ExecDoNothingReject updated receipt, ExecD1Markers receipt fix
48e6053 2026-10-26T04:04:55-03:00 round-35: scorecard + SHONEN late seat appends
980aa3d 2026-10-26T04:19:52-03:00 round-35: WAVE-DONE integration — wave1-results.json (64/64 settled), late receipts, seat-final lesson + SHONEN
0aee0ef 2026-10-26T04:00:05-03:00 round-35: integration — lesson, scorecard, SHONEN, LOG, wave receipts, assimilation artifacts
```

Epoch arithmetic (measured, not inferred): `complete=1792998034`, `lane_final(48e6053)=1792998295`
(**+261 s**), `wave_done(980aa3d)=1792999192` (**+1158 s**). The judged head `0aee0ef` predates the
completion line by 29 s and lacks the paths the claims rest on:

```
$ git ls-tree -r --name-only 0aee0ef | grep -c 'source-snapshots/round-35/S052'
0
```

Verifier routes it as §5.1 (`corpus/lessons/round-35-verifier-spotcheck.md:127-130`) and records both
halves in §1 ("leftovers at filing" 9 paths; "still moving at closure" `tracked=4 untracked=2`) at
`:24-26`. M35-1 is the same class one round earlier (`corpus/lessons/round-35.md:210-214`); M36-1 is
the recurrence, so the id is new but the class is not.

Able-to-fail fixture (scratch git repo, `git rev-parse --show-toplevel` verified equal to the scratch
dir; no production file touched):

```
clean : git status --porcelain | wc -l → 0 ; git archive HEAD | tar -t → f.txt
dirty : git status --porcelain | wc -l → 2 ( M f.txt / ?? seat-receipt.md)
        git archive HEAD | tar -t      → f.txt        ← untracked receipt invisible to the export
```

So the two limbs are not interchangeable: `git status --porcelain` sees the untracked receipt, the
`git archive` export cannot. A suite run only over an export would call the dirty tree closed — which
is why E9 must read the live tree as well as bind the export to `--export-ref <hash>`.

Live E9 state at 15:37Z: `ls -d /fast/scratch/hyaku/kasegi-r36/*/ | wc -l` → **49** (red; green
requires 0 after wave cleanup — unreachable while seats run, so the gate's green is only meaningful
at closure).

### M36-2 — false evidence line at A

```
$ git show 0aee0ef:corpus/lessons/round-35.md | grep -nF 'source-recheck exit 0 on committed bytes'
15:- **Admitted — F18 / S052**: capture + manifest + registry row + entry, all landed this round;
   source-recheck exit 0 on committed bytes; live re-open byte-identical. …
$ git show 0aee0ef:corpus/lessons/round-35.md | grep -cF 'source-recheck exit 0 on committed bytes'
1
$ git ls-tree -r --name-only 0aee0ef | grep -c 'source-snapshots/round-35/S052'
0
```

At `0aee0ef` only `manifest.json` is committed under `corpus/source-snapshots/round-35/`:

```
$ mkdir -p $S/A $S/B
$ git archive 0aee0ef | tar -x -C $S/A ; git archive 5a25337 | tar -x -C $S/B
$ ls $S/A/corpus/source-snapshots/round-35/
manifest.json
$ python3 $S/A/corpus/instruments/source-recheck.py \
    --manifest $S/A/corpus/source-snapshots/round-35/manifest.json --source S052
S052:source UNAVAILABLE reason=missing
A exit=2
$ python3 $S/B/corpus/instruments/source-recheck.py \
    --manifest $S/B/corpus/source-snapshots/round-35/manifest.json --source S052
S052:sha256 OK
S052:Q1 OK occurrences=1 anchor=2-ok
S052:Q2 OK occurrences=1 anchor=3-ok
S052:Q3 OK normalized=markup-whitespace occurrences=1 anchor=4-ok
S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=15472-ok
S052:Q5 normalized=markup-whitespace occurrences=1 anchor=19165-ok
B exit=0
```

The sentence is true at `5a25337` and false at `0aee0ef`: it was written against a worktree that was
later committed, and the committed A never carried the bytes. The same bullet's numstat sentence is
false at A too:

```
$ git show 0aee0ef:corpus/lessons/round-35.md | grep -nF 'SKILL.md` +13/0'
39:… Numstat: `SKILL.md` +13/0 (registry rows), … `PROVINCE.md`/`LOG.md` 0 changed; …
$ git diff --numstat 3266c993 0aee0ef -- SKILL.md LOG.md
10	0	LOG.md
```

`SKILL.md` is absent from the numstat (0/0 at A) and `LOG.md` is +10/0, not 0 — the verifier's §5.5
measurement (`:137-139`) reproduced independently.

### M36-3 — the exact basename vs the near-name

```
$ grep -cF 'r35-defect-closure.sh' SKILL.md   → 0
$ git show 0aee0ef:SKILL.md | grep -cF 'r35-defect-closure.sh' → 0
$ grep -cF 'r36-closure.sh' SKILL.md          → 0
$ grep -cF 'r-defect-closure' SKILL.md        → 4
$ grep -oF 'r-defect-closure' SKILL.md | wc -l → 8
$ sed -n '1097p' SKILL.md | cut -c1-60
| r-defect-closure.sh | gate\|probe | `bash corpus/instruments/…
```

The near-name rows exist (`SKILL.md:1097-1104`; stem `r-defect-closure` = 4 lines / 9 occurrences:
`:1097`=5, `:1100`=1, `:1102`=1, `:1104`=2; the `.sh` form = 3 lines / 8 occurrences: `:1097`=5,
`:1102`=1, `:1104`=2) — and the exact `r35-` row does
not exist — inside the live tree the counter's D3 limb reads green. This is M35-4's finding
(`corpus/lessons/round-35.md:283ff`) carried forward as its own row because the fix that closed D3
chose a near-name registration that the literal cannot distinguish.

Able-to-fail fixture (scratch):

```
fixture with only  | r-defect-closure.sh | …      → exact_r35=0  near=1        (red: open=1)
after appending   | r35-defect-closure.sh | …     → exact_r35=1
                  | r36-closure.sh | …            → exact_r36=1                (green)
```

### M36-4 — the report landed four times

```
$ git -C /home/vgpnk/Projects/shokunin log --format='%h %cI %s' -- .ufo/reports/round-35/kasegi.md
375f9514 2026-10-26T04:20:03-03:00 round-35: kasegi report erratum 3 (WAVE-DONE, results)
8cfcb5b6 2026-10-26T04:02:33-03:00 round-35: kasegi report erratum 2 (final lane commit)
63ce2a63 2026-10-26T04:01:19-03:00 round-35: kasegi report erratum (final lane commit)
e4eb5140 2026-10-26T04:00:23-03:00 round-35: kasegi report
```

Epochs: `e4eb5140=1792998023` (**−11 s** vs complete), `63ce2a63=1792998079` (+45 s),
`8cfcb5b6=1792998153` (+119 s), `375f9514=1792999203` (+1169 s; **+11 s after** wave-done
`980aa3d=1792999192`). The primary commit's own "final lane commit" errata were re-issued because
the lane moved under them — the ordering that R4 wants (report last, one commit) existed only after
three refilings.

Able-to-fail: the predicate `report_ct ≥ max(lane_ct)` returns **red** for e4eb5140
(1792998023 < 1792998295, −272 s) and for 8cfcb5b6 (1792998153 < 1792999192, −1039 s), and **green**
for 375f9514. A check that only asks "is the last report commit after the last lane commit?" reads
green at HEAD; the count of report commits is what discriminates.

---

## 3. Landed-state ledger (what a later receipt may overturn)

| claim-side artefact | at 15:37Z | command |
|---|---|---|
| `corpus/instruments/r36-closure.sh` | absent (worktree and `b47f2cd`) | `ls` → No such file; `git ls-tree -r b47f2cd \| grep -c r36-closure` → 0 |
| `corpus/lessons/round-36.md` | absent | `ls` → No such file |
| `.ufo/waves/round-36/claims-erratum-d5.md` | absent | `ls` → No such file |
| E3 exact rows (`r35-`,`r36-`) | absent | `grep -cF` → 0 / 0 |
| E9 quiescence | red | `git status --porcelain` non-empty (wave files only); 49 seat dirs |
| E4 round-35 `wave1-results.json` tracked | present | `git ls-files … \| wc -l` → 1 |
| E6 'Correction (round 35)' in round-34 `L1Integration.md` | present already | `grep -cF` → 1 |

E8's correction target (the round-36 lesson) is a sibling seat's deliverable; this seat cannot land
it. Closure command for M36-2 once it exists: the lesson carries the S052 false-line correction and
`git show <final>:corpus/lessons/round-35.md` is left untouched (append-only, per §5.4).

## 4. Conflicts and drift recorded for the judge

- **"Re-filed twice" vs three errata.** `round-35-verifier-spotcheck.md:135-136` says "the report was
  re-filed twice post-`complete`". Measured at HEAD: three errata, the third at 04:20:03. The
  difference is time, not contradiction (the spot-check ran ~04:05Z; erratum 3 landed after the
  WAVE-DONE commit). M36-4 states three and cites both instants.
- **Near-name count (two units, one stem).** `corpus/lessons/round-35.md:283ff` reports
  `grep -c -F 'r-defect-closure' SKILL.md` → 4. Measured today: **4 lines / 9 occurrences** of the
  stem (:1097=5, :1100=1, :1102=1, :1104=2), and **3 lines / 8 occurrences** of the `.sh` form
  (:1097=5, :1102=1, :1104=2). This draft first printed "4 lines / 8 occurrences" of the stem —
  the 8 was the `.sh` count, a mislabel of exactly the number-drift class; `ScribeLOG` measured 9
  independently and this file now carries the per-line breakdown. The LOG entry's "4 SKILL.md
  lines" and this row's 4 lines / 9 occurrences agree; the lesson should quote the stem form.
- No claim text in `claims.json` was edited or reinterpreted by this seat; corrections belong in
  appended erratum files.

## 5. Limits

- `r36-closure.sh` does not exist at this measurement, so no E1–E9 verdict is claimed here; the
  able-to-fail values come from scratch fixtures and from two real exports (`0aee0ef`, `5a25337`).
- Only one lane instrument was executed (`source-recheck.py`, twice, over `git archive` exports).
  No lane gate, suite, harness or census was run by this seat.
- All writes: this file plus `/fast/scratch/hyaku/kasegi-r36/ScribeMistakes/` (removed after the
  receipt landed). No git/jj mutation; the two fixture repos were `git init` inside the scratch dir
  with `--show-toplevel` verified.
- No tool was installed.

Report: .ufo/waves/round-36/wave1/ScribeMistakes.md
