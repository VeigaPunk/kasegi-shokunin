# RevSelftestBar — selftest acceptance bar (round 38, receipt-only)

Seat: RevSelftestBar (leaf, reviewer). Item: set and test the selftest acceptance bar for
`corpus/instruments/r38-closure.sh --selftest` — `selftest cases=8 failures=0` with one
`selftest case=G<n> positive=... mutants=a/b verdict=...` line per G; a summary-only forgery and a
selftest that skips positives must not pass; construct three forged outputs and specify the judge
that rejects each; grade the landed `ExecSuiteBuild.r38-closure.sh` `--selftest` on a base export if
it appears. Judged on depth:verifiability. Receipt only — no deliverable files. Every output below
is verbatim from commands this seat ran.

## 1. The acceptance bar (v1, frozen)

A `--selftest` run meets the bar iff its output contains:

1. exactly one summary line `selftest cases=8 failures=0`;
2. exactly eight case lines, one per check id, each exactly
   `selftest case=G<n> positive=pass mutants=<o>/<t> verdict=pass` with n ∈ G1..G8, each id exactly
   once;
3. `o == t >= 1` on every case line — every planted mutant was rejected, none skipped (`0/0`), none
   survived (`o < t`);
4. internal consistency: a line carrying `positive=fail` can never carry `verdict=pass`, and the
   summary numbers must equal the counted lines (8 case lines; 0 `verdict=fail` case lines);
5. any line beginning `selftest case=` or `selftest cases=` that fails its grammar is a REJECT,
   never a silent skip; all other run noise (`== selftest ==`, export lines, `selftest detail=`,
   `selftest judge=`) is ignored, so the judge grades a full run's output.

Mapping to the C1 kill rule: "a summary-only forgery satisfies it" → rules 2+4 (0 case lines, ids
missing); "fewer than 8 cases" → rules 2+4; "any failure" → rules 3+4 (`positive=fail` and
`verdict=fail` can never sit under `failures=0`); "skips positives" → rule 3 (`mutants=0/0`);
"a check passing while its defect is present" → rule 3 (`o < t` survivor).

Boundary note (deliberate): the bar does NOT require `selftest detail=` lines. The suite's internal
judge already requires them (`det == n`, `rej == ok == n`; `ExecSuiteBuild.r38-closure.sh`
lines 1348-1350) — the external bar is the item's case-line grammar, the internal judge is the
stricter in-suite convention. Both apply; see finding F-R1 for the hole in the internal judge that
only the external bar closes.

## 2. The judge (grep/awk)

POSIX awk (GNU Awk 5.4.1, the system `awk` — no tool installs this round; pacman untouched; no
mutating git command was run: only `ls-tree` and `status --porcelain` under `GIT_OPTIONAL_LOCKS=0`).
The same program grades the r37 suite with `-v pre=E -v idre='E[0-9]+' -v want=14`.

```awk
# selftest-bar.awk — acceptance-bar judge for the r38-closure --selftest run.
# (RevSelftestBar, round 38; pure POSIX awk, no gawk extensions.)
#
# Bar:
#   exactly one summary line  selftest cases=8 failures=0
#   exactly eight case lines  selftest case=G<n> positive=pass mutants=<o>/<t> verdict=pass
#   n in G1..G8 each exactly once; o==t>=1 (every planted mutant rejected, none
#   skipped, no survivor); summary numbers equal the counted lines.
# A line beginning `selftest case=` or `selftest cases=` that fails its grammar
# is a REJECT, never a silent skip. Other run noise (== selftest ==, export
# lines) and other `selftest ` lines (detail=/judge=) are ignored, so the judge
# grades a full run. A `positive=fail` case line can never coexist with
# `verdict=pass`, and with `failures=0` required it fails the bar outright.
# stdin: selftest run output (or its == selftest == block). exit 0 = bar met.
# Variants: -v pre=E -v idre='E[0-9]+' -v want=14 grades the r37 suite output.
BEGIN {
  if (pre == "")  pre  = "G"
  if (idre == "") idre = "G[1-8]"
  if (want == "") want = 8
  fullrx = "^selftest case=" idre " positive=pass mutants=[0-9]+/[0-9]+ verdict=pass$"
  bad = 0; ncase = 0; nsum = 0; cases = -1; failures = -1
}
/^selftest cases=/ {
  nsum++
  if (nsum > 1) { print "REJECT duplicate summary line: " $0; bad = 1; next }
  if ($0 ~ "^selftest cases=[0-9]+ failures=[0-9]+$") {
    split($0, a, /cases=/);   split(a[2], b, / /); cases   = b[1] + 0
    split($0, c, /failures=/);                   failures = c[2] + 0
  } else { print "REJECT malformed summary line: " $0; bad = 1 }
  next
}
/^selftest case=/ {
  ncase++
  id = $0; sub(/^selftest case=/, "", id); sub(/ .*/, "", id)
  if (seen[id]++) { print "REJECT duplicate case id: " id; bad = 1 }
  if ($0 ~ /positive=fail/ && $0 ~ /verdict=pass/) {
    print "REJECT inconsistent line (positive=fail but verdict=pass): " $0
    bad = 1; next
  }
  if ($0 !~ fullrx) { print "REJECT case line off-bar: " $0; bad = 1; next }
  split($0, m, /mutants=/); split(m[2], n, /\//); split(n[2], p, / /)
  o = n[1] + 0; t = p[1] + 0
  if (o != t || t < 1) {
    print "REJECT mutants not o==t>=1 (positives skipped or mutant survived): " $0
    bad = 1
  }
  next
}
/^selftest / { next }
{ next }
END {
  if (nsum == 0)    { print "REJECT no summary line"; bad = 1 }
  if (ncase != want) { print "REJECT case-line count " ncase " != " want; bad = 1 }
  for (i = 1; i <= want; i++) {
    g = pre i
    if (!(g in seen)) { print "REJECT missing case " g; bad = 1 }
  }
  if (cases != want)  { print "REJECT summary cases=" cases " != " want; bad = 1 }
  if (failures != 0)  { print "REJECT summary failures=" failures " != 0"; bad = 1 }
  if (!bad)
    printf "ACCEPT selftest bar met: 1 summary, %d case lines %s1..%s%d once each, positive=pass verdict=pass, mutants o==t>=1, cases=%d failures=0\n", ncase, pre, pre, want, cases
  exit bad ? 1 : 0
}
```

Invocation for the L1's verification (exit 0 = bar met):

```sh
bash corpus/instruments/r38-closure.sh --selftest --export-ref <J> > run.out 2> run.err
awk -f selftest-bar.awk run.out          # G/8 bar; rc must be 0
```

## 3. The three required forgeries — all rejected

Fixtures were byte files in this seat's scratch; the judge ran on each whole file.

**F1 — summary-only** (with fake `detail=` lines to look like work; still dies on the missing case
lines):

```text
== selftest ==
selftest detail=G1 positive=pass payload=G1 faked
selftest detail=G2 positive=pass payload=G2 faked
selftest detail=G3 positive=pass payload=G3 faked
selftest detail=G4 positive=pass payload=G4 faked
selftest detail=G5 positive=pass payload=G5 faked
selftest detail=G6 positive=pass payload=G6 faked
selftest detail=G7 positive=pass payload=G7 faked
selftest detail=G8 positive=pass payload=G8 faked
selftest cases=8 failures=0
```

```text
REJECT case-line count 0 != 8
REJECT missing case G1
REJECT missing case G2
REJECT missing case G3
REJECT missing case G4
REJECT missing case G5
REJECT missing case G6
REJECT missing case G7
REJECT missing case G8
judge-rc=1
```

**F2 — eight lines, mutants=0/0** (positives skipped: no fixture ever ran):

```text
== selftest ==
selftest case=G1 positive=pass mutants=0/0 verdict=pass
selftest case=G2 positive=pass mutants=0/0 verdict=pass
selftest case=G3 positive=pass mutants=0/0 verdict=pass
selftest case=G4 positive=pass mutants=0/0 verdict=pass
selftest case=G5 positive=pass mutants=0/0 verdict=pass
selftest case=G6 positive=pass mutants=0/0 verdict=pass
selftest case=G7 positive=pass mutants=0/0 verdict=pass
selftest case=G8 positive=pass mutants=0/0 verdict=pass
selftest cases=8 failures=0
```

```text
REJECT mutants not o==t>=1 (positives skipped or mutant survived): selftest case=G1 positive=pass mutants=0/0 verdict=pass
REJECT mutants not o==t>=1 (positives skipped or mutant survived): selftest case=G2 positive=pass mutants=0/0 verdict=pass
REJECT mutants not o==t>=1 (positives skipped or mutant survived): selftest case=G3 positive=pass mutants=0/0 verdict=pass
REJECT mutants not o==t>=1 (positives skipped or mutant survived): selftest case=G4 positive=pass mutants=0/0 verdict=pass
REJECT mutants not o==t>=1 (positives skipped or mutant survived): selftest case=G5 positive=pass mutants=0/0 verdict=pass
REJECT mutants not o==t>=1 (positives skipped or mutant survived): selftest case=G6 positive=pass mutants=0/0 verdict=pass
REJECT mutants not o==t>=1 (positives skipped or mutant survived): selftest case=G7 positive=pass mutants=0/0 verdict=pass
REJECT mutants not o==t>=1 (positives skipped or mutant survived): selftest case=G8 positive=pass mutants=0/0 verdict=pass
judge-rc=1
```

**F3 — positive=fail but verdict=pass** (G3 line):

```text
== selftest ==
selftest case=G1 positive=pass mutants=2/2 verdict=pass
selftest case=G2 positive=pass mutants=3/3 verdict=pass
selftest case=G3 positive=fail mutants=2/2 verdict=pass
selftest case=G4 positive=pass mutants=1/1 verdict=pass
selftest case=G5 positive=pass mutants=2/2 verdict=pass
selftest case=G6 positive=pass mutants=1/1 verdict=pass
selftest case=G7 positive=pass mutants=1/1 verdict=pass
selftest case=G8 positive=pass mutants=3/3 verdict=pass
selftest cases=8 failures=0
```

```text
REJECT inconsistent line (positive=fail but verdict=pass): selftest case=G3 positive=fail mutants=2/2 verdict=pass
judge-rc=1
```

## 4. Hardening set — bar boundary pinned both ways

Three more forgeries beyond the required three, plus two genuine shapes that must ACCEPT (a judge
that only rejects the three exact strings would be brittle; a judge that rejects compliant output
would be wrong):

| Fixture | Shape | Judge verdict |
|---|---|---|
| forge4-dup-gap | 8 lines, G4 twice, G5 missing, counts consistent | `REJECT duplicate case id: G4` + `REJECT missing case G5`, rc=1 |
| forge5-mutant-survivor | G1 `mutants=2/3` (survivor), rest 1/1 | `REJECT mutants not o==t>=1 … mutants=2/3 …`, rc=1 |
| forge6-seven-lines | 7 well-formed case lines + summary | `REJECT case-line count 7 != 8` + `REJECT missing case G8`, rc=1 |
| genuine.txt | 8 case lines (mixed 1/1..3/3) + `detail=`/`judge=` noise + summary | `ACCEPT selftest bar met: 1 summary, 8 case lines G1..G8 once each, positive=pass verdict=pass, mutants o==t>=1, cases=8 failures=0`, rc=0 |
| minimal-compliant.txt | 8 case lines + summary, no detail lines at all | `ACCEPT selftest bar met: …`, rc=0 (details are the internal judge's requirement, not the external bar's) |

## 5. Real-output cross-checks (not synthetic)

**(a) The judge rejects a real red selftest.** `corpus/instruments/r37-closure.sh --selftest
--export-ref a173b0c2… --lane <lane> --work <scratch>/r37-selftest-work` (TMPDIR pinned to this
seat's scratch) printed `selftest cases=14 failures=1` with

```text
selftest detail=E9 positive=fail rc=1 payload=status-read=ok,status-dirty=3,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=absent
selftest case=E9 positive=fail mutants=5/5 verdict=fail
```

The E9 red is live-by-definition (worktree dirty mid-round, HEAD ahead of the export ref), not a
suite regression — L1's freeze-time run measured `closed=14/14 exit=0` on the same base with
"live lane == base, porcelain empty" (c1-controls/before.txt, line 1). The E-variant judge on that
real output:

```text
REJECT case line off-bar: selftest case=E9 positive=fail mutants=5/5 verdict=fail
REJECT summary failures=1 != 0
e-judge-rc=1
```

**(b) The fleet convention already refuses forged reports.** The same r37 run's own judge lines:
`selftest judge=own-report accepted=0` (it refused its own red report) and six forged reports all
`rejected=1` (forged-summary, forged-caselines, forged-failed-cases, forged-detail-free,
forged-13-cases, forged-duplicate-id). The r38 external bar is that convention, externalized and
extended with the positive-token rule.

## 6. Graded run: the landed suite's `--selftest` on a base export

Deliverable-appearance checks (3, spaced): absent ~18:36Z (glob), absent 18:39:53Z, **present
18:46:14Z** (the first two were ~3.4 min apart, the last two 6.4 min; the file was found on the
final check). Graded bytes:
`sha256(ExecSuiteBuild.r38-closure.sh) = 85d33ea9d386926e88f9818bbdae5c49ef9cf951363ea09de641cb22a26979a6`
— re-verify equality after the L1 lands it at `corpus/instruments/r38-closure.sh` before reusing
this grading.

Command (work dir and TMPDIR pinned under this seat's scratch, outside the lane):

```sh
TMPDIR=$S bash <wave1>/ExecSuiteBuild.r38-closure.sh --selftest \
  --export-ref a173b0c2b98c5ae39599fa9be76027fbbead0b9e \
  --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --work $S/r38-selftest-work
```

Result: **rc=1, honest red** — every positive failed (defects open at base), every mutant was
rejected, the summary did not lie:

```text
selftest case=G1 positive=fail mutants=3/3 verdict=fail
selftest case=G2 positive=fail mutants=6/6 verdict=fail
selftest case=G3 positive=fail mutants=2/2 verdict=fail
selftest case=G4 positive=fail mutants=2/2 verdict=fail
selftest case=G5 positive=fail mutants=4/4 verdict=fail
selftest case=G6 positive=fail mutants=5/5 verdict=fail
selftest case=G7 positive=fail mutants=2/2 verdict=fail
selftest case=G8 positive=fail mutants=2/2 verdict=fail
selftest cases=8 failures=8
selftest judge=own-report accepted=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=forged-failed-cases rejected=1
selftest judge=forged-detail-free rejected=1
selftest judge=forged-7-cases rejected=1
```

Mutant exercise verified per id with the judge's own pattern
(`grep -c "^selftest detail=<id> mutant="` / `…rejected=1`): G1 3/3, G2 6/6, G3 2/2, G4 2/2, G5 4/4,
G6 5/5, G7 2/2, G8 2/2 — 26 planted mutants, 26 rejected, zero survivors. (An earlier count that
showed `+1` per id was this seat's own counting program matching the `positive=fail` detail line
too; the judge-pattern recount above is the correct one.)

External-bar verdict on this output: **REJECT** (rc=1) — correct, because base must not certify:
all eight case lines are off-bar (`positive=fail … verdict=fail`) and `failures=8 != 0`. The
anti-forgery property held end to end: the suite refused to print `cases=8 failures=0` on a red
tree, and the bar refuses to accept anything but the full green shape.

## 7. Findings

- **F-R1 (defect in the delivered suite's internal judge — minor, concrete, one-line fix).**
  `judge_selftest_report` (`ExecSuiteBuild.r38-closure.sh` lines 1327-1354) never requires
  `positive=pass` on a case line. Proven with a minimal-diff pair run through the extracted judge
  (harness = `CHECK_IDS=(G1 … G8)` line 158 + lines 1327-1355 + a call line):
  - forge3b — byte-identical to a fully clause-compliant report except G3's line reads
    `selftest case=G3 positive=fail mutants=2/2 verdict=pass` (with its two matching
    `detail=G3 mutant=… rejected=1` lines): **their judge ACCEPTS (rc=0)**; my external bar
    REJECTS (rc=1).
  - forge3c — same bytes with `positive=pass`: their judge rc=0, my bar rc=0.
  So a forged report in exactly the item's third forgery class slips past the internal judge.
  Their own emitter cannot produce the shape (`st_verdict`, lines 846-857, only prints
  `verdict=pass` when the positive passed), so their own report is safe — the hole opens only for
  forged reports, which is the class the kill rule cares about. Fix: after the `verdict=pass$`
  check add `printf '%s' "$line" | grep -q 'positive=pass' || return 1` (and optionally require
  `positive=pass` in the `verdicts` grep). The external bar already rejects the shape either way.
- **F-R2 (observation, expected).** The base-export selftest is honestly red (`failures=8`,
  26/26 mutants rejected) — fail-closed semantics confirmed; the bar stays red on base by design.
- **F-R3 (boundary, deliberate).** The external bar does not require `detail=` lines; the internal
  judge does (`det==n`, `rej==ok==n`). Division of labor: the internal judge kills
  detail-free/zero-mutant forgeries, the external bar kills positive-token forgeries. Keep both.
- **F-R4 (disclosure).** This seat's first harness run against their judge was invalid — the
  harness call line was built with double quotes, so `$1` expanded to empty at creation time and
  the judge was called on `""` (rc=1 for every input, including the control). Rebuilt single-quoted
  and rerun; only the rerun results are evidence. The invalid run is disclosed, not used.

## 8. Discipline

Scratch `S=/fast/scratch/hyaku/kasegi-r38/RevSelftestBar/` created with `mkdir -p`; both suite runs
pinned to it (`TMPDIR=$S`, `--work` under `$S`); the directory is removed before this seat yields
(G6 quiescence). No tool installs (system GNU Awk 5.4.1, bash, coreutils); pacman untouched; no
mutating git/jj command anywhere — only read-only `ls-tree` and `GIT_OPTIONAL_LOCKS=0
status --porcelain` against the lane. No writes outside the receipt and scratch. No subagents, no
`agent://all` traffic.

## 9. Reproduction recipe for the L1

The judge source is §2; the three forged outputs are §3 (byte-exact fenced blocks); the hardening
fixtures are described in §4. To re-verify: write `selftest-bar.awk` and the fixtures to files,
run `awk -f selftest-bar.awk <fixture>` per file — expected rc: genuine/minimal 0, all six forgeries
1 — then run the §2 invocation over a real `--selftest` output of the landed suite (after checking
its sha256 against §6).
