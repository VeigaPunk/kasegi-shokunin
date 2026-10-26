# MutCountingCommands — wave-2 falsify receipt (round 40, hyaku run 9)

Seat: mutation-test the frozen claims' **counting commands** — re-run every
counting command in `.ufo/waves/round-40/claims.json` at the verification ref Y
verbatim, re-run each against base `a7af2ce63bce153757d39bf66b366a96caf30c13`,
and check the before values against the before-control files. Any output that
contradicts the claim's after-state is a defect.

- Attacked item: claims C1 (counting_commands 1–5) and C2 (counting_commands 1–8)
  — 13 commands total, plus the C1 kill-rule pending-grep clause and the C2
  junk-twin rejection.
- Date: 2026-10-26 (UTC during run ≈21:1x–21:2xZ).
- Refs: base `a7af2ce63bce153757d39bf66b366a96caf30c13` · r39 judged head
  `8371e7ac9f32cae5ed72f8c28205634603f836fa` · claims freeze
  `5e985b74075dd3813a63d7750966bf8abf693465` · lane tip / judged head J
  `3074c7679d6f527ec3930d7748ccce1dbae4a58a`.
- **Y disclosure (read first):** at dispatch the receipt
  `.ufo/waves/round-40/final-gates/all-gates.txt` is **untracked** in the lane
  working tree; no lane commit contains it yet, so Y = J + receipt does not
  exist as a lane commit. I built the Y window in a scratch fixture: a full
  `git clone` of the lane into scratch, detached checkout of J, the untracked
  receipt bytes copied in, one commit ⇒ fixture Y =
  `56ef046ffeaef61f1aa13a844c76c571bbe645f0`, and `git diff --name-only J Y` in
  the fixture lists exactly `.ufo/waves/round-40/final-gates/all-gates.txt`
  (verified). The lane's tracked working tree equals J (`git diff --stat J`
  empty). C1 runs that need the Y ref pass `--lane <fixture>` (a documented
  option); base/r39/plain runs use the suite's default lane (the real lane,
  read-only `git archive` / `--no-optional-locks` limbs only).
- Tree bytes: `git archive` exports of J+receipt (Y tree), base, and r39 head
  were extracted to scratch; every C2 command ran with cwd at the export root.
  Suite bytes verified identical in all three instantiations:
  `corpus/instruments/r40-closure.sh` sha256
  `bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e` (equals the
  receipt's `suite-sha256`).

## C1 — suite runs (5 commands)

Verbatim form `bash corpus/instruments/r40-closure.sh …` from the Y tree cwd;
auto work dir via exported `TMPDIR` inside the round scratch (so the H6 family
scan sees the work dir contained in `kasegi-r40`); scratch root left at the
default `/fast/scratch/hyaku`.

| # | command | claim | observed | verdict |
|---|---|---|---|---|
| C1-1 | `--export-ref <Y>` | `closed=10/10 exit=0` | `closed=10/10 exit=0`, exit 0 | **reproduced** |
| C1-2 | `--selftest --export-ref <Y>` | `selftest cases=10 failures=0`, one graded pass line per check | `selftest cases=10 failures=0`, 10 × `selftest case=H<n> positive=pass mutants=<k>/<n> verdict=pass` | **reproduced** |
| C1-3 | `--export-ref a7af2ce…` | `closed<10/10 exit=1` | `closed=3/10 exit=1` | **reproduced** |
| C1-4 | `--export-ref 8371e7a…` | `closed<10/10 exit=1` | `closed=2/10 exit=1` | **reproduced** |
| C1-5 | plain run, no args | refused, exit 2 | `r40-closure: refusing to run against the live worktree…`, exit 2 | **reproduced** |

C1-1 full transcript (exit 0) — **byte-identical to the committed receipt**
(`cmp` clean; both sha256
`7b8cda36c793c5855fa6ffcb78d241fca47f0d3679b2d7c38f7a959042463484`), which also
independently re-proves the H7 determinism claim at Y:

```
all-gates v4
export-ref=3074c7679d6f527ec3930d7748ccce1dbae4a58a
suite-sha256=bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e
time-basis=ref-commit
run-utc=2026-10-26T21:56:22Z
H1 payload=suite=1,digest=1,registry=1,registry-in=skill closed=1
H2 payload=corrections=8,named=5,missing=0,fences=closed closed=1
H3 payload=mentions=1,rows=1 closed=1
H4 payload=s056=1,s058=1,s059=1,oversize=0 closed=1
H5 payload=source=1,control=8/8,utc=1,forged-payload=rejected,future-dated=rejected,summary-only=rejected closed=1
H6 payload=strays=0,read=ok closed=1
H7 payload=sentinel=1,ref=3074c7679d6f527ec3930d7748ccce1dbae4a58a,digest=1,time-basis=1,run-utc=1,not-future=1,header-lines=5,run-lines=10,body-lines=11,closed-0=0,closed-line=1,ancestor=1,diff-clean=1,diff-read=ok,payload-match=9,h7-line=1 closed=1
H8 payload=base=3/10,base-exit=1,r39=2/10,r39-exit=1 closed=1
H9 payload=declared=172,valid=172,tail=172,pure=1,paths=1,diff-read=ok closed=1
H10 payload=skill-del=0,province-del=0,density=1,deleted=0,diff-read=ok closed=1
closed=10/10 exit=0
```

Cross-checks on the transcript facts: `run-utc=2026-10-26T21:56:22Z` equals the
committer instant of J (`git log -1 --format=%ct` = 1793051782 =
2026-10-26T21:56:22Z) — `time-basis=ref-commit` holds; my C1-3/C1-4 tallies
(3/10 and 2/10) equal the receipt's own H8 nested payloads (`base=3/10`,
`r39=2/10`) run-for-run. Selftest graded lines (C1-2, exit 0):

```
selftest case=H1 positive=pass mutants=3/3 verdict=pass
selftest case=H2 positive=pass mutants=3/3 verdict=pass
selftest case=H3 positive=pass mutants=2/2 verdict=pass
selftest case=H4 positive=pass mutants=3/3 verdict=pass
selftest case=H5 positive=pass mutants=2/2 verdict=pass
selftest case=H6 positive=pass mutants=4/4 verdict=pass
selftest case=H7 positive=pass mutants=6/6 verdict=pass
selftest case=H8 positive=pass mutants=2/2 verdict=pass
selftest case=H9 positive=pass mutants=5/5 verdict=pass
selftest case=H10 positive=pass mutants=3/3 verdict=pass
selftest cases=10 failures=0
```

Bonus window check (not a claims command): plain suite run at J
(`--export-ref 3074c76…`, no receipt in that export) — the instrument header
promises `closed=9/10 exit=1` fail-closed there; observed exactly that (H7 red,
`receipt=0`), so the 10/10 green window is Y-only as claimed.

C1 kill-rule extra clause re-run at Y: `grep -c '⟨pending'
corpus/lessons/round-40.md` → `0` (grep exit 1 = zero matches) — clause holds.

## C2 — registry/frontier/harness/census counters (8 commands)

Ran with cwd at the Y-tree export and at the base export (and r39-head export
for the record). Verbatim command text from claims.json.

| # | command (verbatim) | before → after claim | at base (observed) | at Y (observed) | verdict |
|---|---|---|---|---|---|
| C2-1 | `awk -F'\'' -F'\'' … if(s=="queued") …' corpus/SOURCES.md` (see claims.json) | 9 → 0 | 9 | 0 | **reproduced** |
| C2-2 | same awk, `s=="mined"` | 0 → ≥4 | 0 | 7 | **reproduced** |
| C2-3 | `grep -rlE '^source: S0(16\|17\|19\|20\|21\|22\|23\|24\|25)' corpus/knowledge \| wc -l` | 0 → = mined count | 0 | 7 (= mined) | **reproduced** |
| C2-4 | `grep -cE '^\|\[[:space:]]*S06[0-9][[:space:]]*\|' corpus/SOURCES.md` | 0 → ≥1 | 0 (grep exit 1) | 3 | **reproduced** |
| C2-5 | `grep -rlE '^source: S06[0-9]' corpus/knowledge \| wc -l` | 0 → ≥1 | 0 | 1 | **reproduced** |
| C2-6 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 22 → 23 | 22 | 23 | **reproduced** |
| C2-7 | `python3 corpus/instruments/frontier-recheck-count.py` | entries=25 pass=25 exit=0 → entries=26 pass=26 exit=0 | `entries=25 pass=25 exit=0` | `entries=26 pass=26 exit=0`, incl. `PASS F23 knowledge/cyclonedx-analysis-subtree.md ids=S060 exit=0` | **reproduced** |
| C2-8 | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit 0, no new W/E | (before recorded in census-before.txt) | exit 0; `W04 S028…`, `W04 S029…`, `ok …/corpus/SOURCES.md` — byte-equal to census-before.txt | **reproduced** |

Exact awk text for C2-1/C2-2 as frozen (single-quoted program, `-F'|'`):
`/^\|[[:space:]]*S0(16|17|19|20|21|22|23|24|25)[[:space:]]*\|/
{s=$9; gsub(/[[:space:]]/,"",s); if(s=="queued") n++} END{print n+0}` (and the
`mined` variant) over `corpus/SOURCES.md`.

Before-control cross-checks (all confirmed at base / r39 bytes):

- `c1-controls/before.txt`: suite absent at base — `ls
  base/corpus/instruments/r40-closure.sh` → "No such file or directory" ✓;
  R2/R5/R6 open at base — suite's own base payloads agree (`H2
  corrections=0,named=0,missing=4`; `H3 mentions=0,rows=0`; `H4
  s056=0,s058=0,s059=0`) ✓.
- `c2-controls/before.txt`: queued 9 ✓, mined among nine 0 ✓, entries citing
  nine 0 ✓, S060+ rows 0 ✓, S060+ entries 0 ✓, frontier 22 ✓, harness 25/25 ✓,
  registry rows total 59 (measured `grep -cE '^\|[[:space:]]*S[0-9]{3}[[:space:]]*\|'`
  = 59 at base) ✓. Same values at the r39 judged head (ran the six grep/awk
  counters there too: 9 / 0 / 0 / 0 / 0 / 22).
- `census-before.txt`: my verbatim census re-run prints the same two W04 lines
  (S028, S029) + `ok` + `exit=0` — no new W/E code ✓. Also re-derived the base
  state by pointing the census at the base export dir
  (`validate <scratch>/base`): same W04 S028/S029 + `ok` + exit 0 (lane id
  prints as the dir name in that mode) ✓.
- r22 measure arithmetic: before (20+22)/(20+22+9) = 42/51 = 0.824 ✓; after
  (20+23)/(20+23+0) = 43/43 = 1.000 ✓.
- Registry growth 59 → 62 = +3 S060+ rows (S060, S061, S062) ✓; the nine rows'
  Y statuses: S016/S017/S019/S020/S021/S023/S025 = mined (7), S022/S024 =
  rejected — matches the predicate's "S022 superseded by S030; S024 superseded
  by S029" and the round-40 lesson Gate blocks (presence checked; deep
  Gate-block verification is sibling seats' scope).

## Junk-twin control (C2 kill clause "junk twin accepted")

`c2-controls/junk-decisions.md` models flipping all nine queued rows to
`rejected` with no evidence. I built that twin in scratch (base SOURCES.md with
the nine rows' status cell set to `rejected` via awk) and re-ran the frozen
counters on it: queued = **0** (queued clause would pass) but mined among the
nine = **0** < 4 — the `mined ≥ 4` clause kills the twin, and no knowledge
entry cites any of the nine (0). **Junk twin rejected by the frozen counters.**

## Invocation artifact found and corrected (not a claim defect)

My first base/r39 suite runs printed `H6 strays=1` because I passed the scratch
dir as `TMPDIR=… && bash …` — a standalone assignment is not exported, so the
suite's auto work dir landed in `/tmp`, outside the `kasegi-r40` family entry,
and H6 (correctly, per its containment rule) counted `kasegi-r40` as a stray.
Re-runs with `env TMPDIR=…` (properly exported) print `strays=0` and match the
committed receipt's nested payloads exactly. Recorded because it is live
evidence that H6's containment discrimination works as documented; the suite's
auto work dirs are removed by the suite itself at exit (no litter left in
`/tmp`).

## Verdict

- **13/13 counting commands reproduced** at Y and at base/r39 as claimed;
  every before value matches its before-control file; the census re-run is
  byte-equal to `census-before.txt`; the Y suite transcript is byte-identical
  to the committed receipt.
- **No contradiction, no defect found by this seat.** The only live-state
  sensitivity observed (H6 strays) was traced to my own invocation artifact and
  disappears with a correct work-dir placement, exactly as the instrument
  documents.
- Boundary note: deep verification of Gate-block *content*, source-recheck
  passes, capture sha256/quotes, and the H1–H10 mutation fixtures belong to
  sibling seats (RevC2Decisions/RevC2Entries/CritSourceTruth, MutH1H5/MutH6H10);
  this receipt covers the frozen counting commands only.
