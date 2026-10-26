# ExecC1JudgedHeadFail — r36 judged-head red baseline for C1

Round 37 (`kasegi-shokunin`), wave 1, leaf executor seat. Judged on `depth:verifiability`.
Item: produce the r36 judged-head red baseline for C1 (frozen claim C1's second required red,
"r36 judged-head export -> closed<14/14 exit=1 (E10-E14 open there)").

## Binding

| fact | value |
|---|---|
| lane repo | `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only lane repo touched; read-only git) |
| round base | `b56a41680cefd391868c1c370dc063c69d827e7d` |
| claims freeze | `224df74db2a46d627ae1475a72ca48796bbd177c` |
| **judged head under test** | **`a23dc4788aa7c98831eed6db953434034ce5ae8d`** |
| judged head tree | `78f74821afb6d22479d3c3bdefb27a6c6e270709` |
| judged head commit | `round-36: final gate receipts + measured closure`, 2026-10-26 13:00:31 -0300 |
| export | `git archive a23dc478 \| tar -x`; reconciled exactly: `ls-tree -r` = 7253 entries = 6730 regular (`100644`) + 465 executable (`100755`) + 58 symlinks (`120000`); the export holds 7195 regular files + 58 symlinks; no gitlinks, no `.gitattributes`/`export-ignore`, so the extraction is complete |
| r36 suite bytes | `corpus/instruments/r36-closure.sh`, sha256 `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4` (matches the `suite-sha256=` header the run prints) |
| live lane HEAD at run time | `b362068` (mid-wave; see the E9 note) |
| scratch | `/fast/scratch/hyaku/kasegi-r37/ExecC1JudgedHeadFail/` (deleted before yield) |

## Verdict in one table

| item step | probe | measured at `a23dc478` | red? |
|---|---|---|---|
| 1 | `bash corpus/instruments/r36-closure.sh --export-ref a23dc478…` | `closed=8/9 exit=1`; E1–E8 `closed=1`, E9 `closed=0` (`status-dirty=6,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=present`) | exit 1 (E9 only — see caveat F1) |
| 2a (D1) | `.ufo/waves/round-37/final-gates/all-gates.txt` in the export | **ABSENT** (no `round-37` path is tracked at all: `ls-tree \| grep -c round-37` = 0) | RED |
| 2b (D2) | `grep -n r36-fixtures <export>/LOG.md` | hit at `LOG.md:1665` (r36 C1 bullet claims `corpus/instruments/r36-fixtures/` landed); tracked in 0 paths, absent in the export, **0** named corrections | RED |
| 2c (D4) | `grep -c 'Final lane commit: e666d902' <export>/SCORECARD.md` | **1** (`SCORECARD.md:1492`); no `## Round 37` section in `SCORECARD.md`; `anchor ancestor` in 0 export files / 0 commit matches; `c20300df` named in 0 files; same stale label at `corpus/lessons/round-36.md:3` | RED |
| 2d (D5) | `SKILL.md:1111` row `r36-closure.sh` | type cell is the literal escaped `gate\|probe` (`grep -cF 'gate\|probe'` = 6); `could-not-evaluate` = 0 in the row ±3 lines, 1 file-wide (line 981, the `recheck-audit.py` row) → no exit-2 verdict for the r36 row | RED |
| 2e (D6) | shape of `r36-closure.sh` quiescence limb | `grep -cF 'porcelain:-0'` = **1** (`:466`); status read at `:465` is `git … status --porcelain 2>/dev/null \| count_lines`; `count_lines` is `grep -c . 2>/dev/null \|\| true` → a failed read yields empty, then `${porcelain:-0}` = clean | RED |
| 3 | r37-style E10–E14 stand-in vs the export | **E10, E11, E12, E13, E14 all `closed=0`; `closed=0/5 exit=1`** | RED ×5 |

Controls proving the step-3 stand-in is not blind: a synthetic green twin reads `closed=5/5 exit=0`,
and five single-flip mutants built from that twin each read `closed=4/5 exit=1` with **exactly** the
flipped check red (E10 digest unbind, E11 correction removed, E12 stale label re-inserted inside the
round-37 section, E13 `gate\|probe` literal + exit-2 map removed, E14 `porcelain:-0` + `2>/dev/null`
swallow re-introduced). So the judged-head REDs are discriminating, not harness blindness.

## Reading of step 1 (r36 suite at the r36 judged head)

```
closed=8/9 exit=1
```

E1–E8 are all `closed=1` at `a23dc478` — the r36 suite's own content checks do close at the r36 judged
head. The single red is E9, and E9 is **not** an export-content check: `check_e9` defaults
`STATUS_REPO` to `$LANE` (`r36-closure.sh:451`) and `EXPECTED_HEAD` to the export ref (`:452`), so it
reads the *live lane worktree* and *live HEAD*. At run time the lane was mid-wave (HEAD `b362068`,
`git status --porcelain` = 6 lines, all untracked round-37 wave files), hence
`status-dirty=6,…,head-match=0` → `closed=0`. **Consequence for the claim:** the r36 suite can only
print `9/9` at a moment when the lane worktree is clean *and* HEAD equals the named ref; it cannot do so
now, and its red carries no information about `a23dc478`'s content. The r37 D1–D6 closure signal at this
head is the E10–E14 stand-in in step 3 (0/5), not E9. Both readings are red, as the claim requires,
but only step 3 measures the routed defects.

## Reading of step 2 (the routed defects are open at the judged head)

D1's lineage is visible at the same commit: `.ufo/waves/round-36/final-gates/all-gates.txt` exists
(1203 bytes) but carries **0** `suite-sha256=` headers, **0** `E<n> payload=` lines and **0**
`selftest case=` lines — exactly the omission the r36 spot-check routed as D1; the r37 target file
`.ufo/waves/round-37/final-gates/all-gates.txt` does not exist at all.

D2: the false path is real — `git ls-tree -r --name-only a23dc478 | grep -c r36-fixtures` = 0 and the
path is absent from the export, so `LOG.md:1665`'s "Landed `…r36-closure.sh` + `…r36-fixtures/`" names a
path that never existed; no correction line exists (window-bounded correction grep → exit 1, no match).
Note the r36 bullet *does* contain the words "false evidence lines" in its E8 sentence; a naive
`false`-token grep matches it, which is why E11's correction test must be window-bounded to the path.

D4: the stale `Final lane commit: e666d902…` label is at `SCORECARD.md:1492` (inside the **round-36**
section — there is no round-37 section at all; headers end at `## Round 36` line 1406), and the same
stale label is also at `corpus/lessons/round-36.md:3`. `e666d902` is itself a round-36 *wave-evidence*
commit ("round-36: wave evidence — spec/dispatch/ready, seat receipts (60/64)…"), not a lane head. The
true r36 lane head `c20300df…` is named in **0** files at `a23dc478`, and the string `anchor ancestor`
appears in **0** files. So at this head E12 reds on *absence* (no round-37 section, no anchor-ancestor
label); the "stale label inside the round-37 section" clause is only vacuously satisfied because the
section does not exist. The r37 suite must therefore require the round-37 section to exist and carry the
label, not merely require the stale string to be absent from it.

D5 counting nuance: `grep -cF 'gate|probe'` = 5 and `grep -cF 'gate\|probe'` = 6 at this head. The
registry rows that use the *escaped* form (`gate\|probe`) are the r35/r36 rows, so E13 must test the
escaped literal (or parse the type cell) — an unescaped-only count misses exactly the rows D5 is about.
The r36 row's own text also contains `exit 2` (the plain-run refusal) yet maps it to nothing; the only
`could-not-evaluate` in the whole file is line 981's `recheck-audit.py` row.

## Findings handed to the L1 (not defects of mine, but they change how the r37 suite must be written)

- **F1 — E9 is environment-coupled.** `r36-closure.sh:451-452` make E9 read the live lane and live HEAD.
  Any r37 suite that keeps that shape will red on a dirty wave worktree regardless of the export under
  test, and its E9 payload cannot be reproduced from the export alone. E9 in r37 is required to be
  fail-closed by *shape* (E14) **and** its status read must be red on failure — both matter, but the
  live-lane coupling is a separate reproducibility defect worth naming in the round-37 lesson.
- **F2 — D4 has two sites.** `SCORECARD.md:1492` and `corpus/lessons/round-36.md:3`. E12's SCORECARD-only
  wording leaves the lesson site open; the round-37 lesson should correct or explicitly supersede both.
- **F3 — D5 needs the escaped-literal count** (see above), or a type-cell parse; a plain `grep -F 'gate|probe'`
  under-counts by exactly the two rows at issue.
- **F4 — environment, transient:** `/home/vgpnk/.local/bin/git` (a 3526-byte Python wrapper, mtime
  14:05 today, ahead of `/usr/bin/git` on PATH) failed with `No such file or directory` from inside a
  non-interactive script during this seat's first transcript pass, then worked again when invoked
  directly; `git --version` = 2.56.0 from both paths. Nothing was modified. This seat pinned
  `/usr/bin/git` in its harness for determinism. Sibling seats driving `git` from non-interactive
  scripts should expect the same transient ENOENT if that wrapper is rewritten concurrently.

## Reproduction

```sh
S=/fast/scratch/hyaku/kasegi-r37/ExecC1JudgedHeadFail
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
REF=a23dc4788aa7c98831eed6db953434034ce5ae8d
mkdir -p "$S"
( cd "$LANE" && bash corpus/instruments/r36-closure.sh --export-ref "$REF" )   # step 1
mkdir -p "$S/exp" && ( cd "$LANE" && git archive "$REF" ) | tar -x -C "$S/exp" # step 2 export
bash "$S/r37-standin.sh" "$S/exp"                                             # step 3: E10-E14 -> 0/5
```

The step-3 stand-in is scratch-only (it is **not** the lane's `r37-closure.sh`, which does not exist at
`a23dc478`); its exact source is embedded below, and the builder that creates the green twin and the five
flip mutants is embedded after it. Both are reproduced verbatim so the L1 can re-run the controls.

<details><summary>r37-standin.sh (sha256 01ed701ce934ee813b4533d6ffc7a7d261fd71e862db4cf9819e4bbeb41f089a)</summary>

```bash
#!/usr/bin/env bash
# Minimal scratch-only stand-in for the round-37 E10-E14 check shapes (frozen claim C1).
# It is NOT the lane's r37-closure.sh: it exists to prove each r37 check is RED at a
# named export root. Usage: r37-standin.sh <export-root>
set -uo pipefail
root=${1:?usage: r37-standin.sh <export-root>}
cd "$root" || { echo "root-unreadable=$root"; exit 9; }
closed=0; total=0
p() { # ID ok payload
  total=$((total+1))
  if [ "$2" -eq 1 ]; then closed=$((closed+1)); printf '%s payload=%s closed=1\n' "$1" "$3"
  else printf '%s payload=%s closed=0\n' "$1" "$3"; fi
}

# E10 (D1): r37 final-gates transcript: digest header over the r37 suite bytes,
# 14 payload lines, closed=14/14 exit=0, 14 selftest case lines, cases=14 failures=0.
f=.ufo/waves/round-37/final-gates/all-gates.txt
if [ -f "$f" ]; then
  hdr=$(sed -n '1s/^suite-sha256=\([0-9a-f]\{64\}\)$/\1/p' "$f")
  want=$(sha256sum corpus/instruments/r37-closure.sh 2>/dev/null | cut -d' ' -f1)
  epl=$(grep -cE '^E([1-9]|1[0-4]) payload=' "$f")
  stl=$(grep -cE '^selftest case=' "$f")
  st=$(grep -c 'cases=14 failures=0' "$f"); cl=$(grep -c 'closed=14/14 exit=0' "$f")
  ok=0; [ -n "$hdr" ] && [ "$hdr" = "$want" ] && [ "$epl" -eq 14 ] && [ "$stl" -eq 14 ] && [ "$st" -ge 1 ] && [ "$cl" -ge 1 ] && ok=1
  p E10 "$ok" "file=1,digest-bound=$([ -n "$hdr" ] && [ "$hdr" = "$want" ] && echo 1 || echo 0),E-lines=$epl,selftest-lines=$stl,summary=$st,closed-line=$cl"
else
  p E10 0 "file=0(reason=absent:.ufo/waves/round-37/final-gates/all-gates.txt),digest-bound=0,E-lines=0,selftest-lines=0,summary=0,closed-line=0"
fi

# E11 (D2): LOG.md carries a named correction of the r36 C1 bullet's false
# corpus/instruments/r36-fixtures/ path (window-bounded so the bullet's own
# unrelated "false evidence lines" wording cannot satisfy it).
if [ -f LOG.md ]; then
  false_line=$(grep -cF 'corpus/instruments/r36-fixtures/' LOG.md)
  corr=$(grep -cE 'r36-fixtures.{0,100}(does not exist|not a real path|false path|is false|was false|never existed|phantom|misnamed|invented)|(correction|corrected|corrigendum|erratum)[^.]{0,100}r36-fixtures' LOG.md)
  ok=0; [ "$corr" -ge 1 ] && ok=1
  p E11 "$ok" "false-path-lines=$false_line,named-correction-lines=$corr"
else p E11 0 "LOG.md=absent"; fi

# E12 (D4): round-37 SCORECARD section + round-37 lesson label r36 lane head c20300df
# as 'anchor ancestor'; stale 'Final lane commit: e666d902' absent inside that section.
if [ -f SCORECARD.md ]; then
  sec=$(awk '/^## Round[- ]37/{f=1;next} f&&/^## Round[- ]3[0-9]/&&!/Round[- ]37/{exit} f' SCORECARD.md)
  if [ -n "$sec" ]; then
    anc=$(printf '%s\n' "$sec" | grep -cE 'c20300df[^|]{0,120}anchor ancestor|anchor ancestor[^|]{0,120}c20300df')
    stale=$(printf '%s\n' "$sec" | grep -c 'Final lane commit: e666d902')
    lesson=$(grep -rlsE 'c20300df' corpus/lessons/ 2>/dev/null | xargs -r grep -lE 'anchor ancestor' 2>/dev/null | grep -c 'round-37')
    ok=0; [ "$anc" -ge 1 ] && [ "$stale" -eq 0 ] && [ "$lesson" -ge 1 ] && ok=1
    p E12 "$ok" "round37-section=1,anchor-ancestor-c20300df=$anc,stale-e666d902=$stale,r37-lesson-anchor=$lesson"
  else
    p E12 0 "round37-section=0,anchor-ancestor-c20300df=0,stale-e666d902=$(grep -c 'Final lane commit: e666d902' SCORECARD.md)(whole-file),r37-lesson-anchor=0"
  fi
else p E12 0 "SCORECARD.md=absent"; fi

# E13 (D5): r36-closure.sh registry row: single-choice type cell (NOT the literal
# escaped text gate\|probe) and a verdict map carrying exit 2 -> could-not-evaluate.
if [ -f SKILL.md ]; then
  row=$(grep -F '| r36-closure.sh |' SKILL.md | head -1)
  if [ -n "$row" ]; then
    # markdown-table escaped pipe keeps the cell text 'gate\|probe' literal; count it
    esc=$(printf '%s\n' "$row" | grep -oF 'gate\|probe' | wc -l | tr -d ' ')
    single=0; [ "$esc" -eq 0 ] && single=1
    # exit 2 -> could-not-evaluate may sit in the row or in a verdict-map line nearby
    ln=$(grep -nF '| r36-closure.sh |' SKILL.md | head -1 | cut -d: -f1)
    lo=$((ln>5 ? ln-5 : 1)); hi=$((ln+5))
    vmline=$(sed -n "${lo},${hi}p" SKILL.md | grep -cE '2[^0-9]{0,40}could-not-evaluate')
    vm=0; [ "$vmline" -ge 1 ] && vm=1
    ok=0; [ "$single" -eq 1 ] && [ "$vm" -eq 1 ] && ok=1
    p E13 "$ok" "row=1,literal-escaped-gate-pipe-probe=$esc,single-choice=$single,exit2-verdict=$vm(window=$vmline)"
  else p E13 0 "row=0(no r36-closure.sh registry row),single-choice=0,exit2-verdict=0"; fi
else p E13 0 "SKILL.md=absent"; fi

# E14 (D6): quiescence fail-closed by shape in the r37 suite (no 'porcelain:-0'
# default-to-clean, no status-read '2>/dev/null' swallow).
suite=''
[ -f corpus/instruments/r37-closure.sh ] && suite=corpus/instruments/r37-closure.sh
if [ -n "$suite" ]; then
  pc=$(grep -cF 'porcelain:-0' "$suite")
  sw=$(grep -cE 'status --porcelain[^|]*2>/dev/null' "$suite")
  ok=0; [ "$pc" -eq 0 ] && [ "$sw" -eq 0 ] && ok=1
  p E14 "$ok" "r37-suite=1,porcelain:-0=$pc,status-swallow=$sw"
else
  pc=$(grep -cF 'porcelain:-0' corpus/instruments/r36-closure.sh 2>/dev/null || echo 0)
  sw=$(grep -cE 'status --porcelain[^|]*2>/dev/null' corpus/instruments/r36-closure.sh 2>/dev/null || echo 0)
  p E14 0 "r37-suite=0(absent),r36-fallback:porcelain:-0=$pc,status-swallow=$sw"
fi

printf 'closed=%d/%d exit=%d\n' "$closed" "$total" "$([ "$closed" -eq "$total" ] && echo 0 || echo 1)"
[ "$closed" -eq "$total" ] || exit 1
exit 0

```

</details>

<details><summary>mktranscript.sh — builds the export, the green twin, the five flip mutants and the transcript</summary>

```bash
#!/usr/bin/env bash
# ExecC1JudgedHeadFail: rebuilds the r36 judged-head export, the green twin, the five
# single-flip mutants and the whole transcript in one deterministic pass.
set -uo pipefail
S=/fast/scratch/hyaku/kasegi-r37/ExecC1JudgedHeadFail
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
REF=a23dc4788aa7c98831eed6db953434034ce5ae8d
GIT=/usr/bin/git
X=$S/exp-a23dc478
T=$S/transcript.txt

sec() { printf '\n########## %s ##########\n' "$1" >> "$T"; }
run() { printf '$ %s\n' "$*" >> "$T"; "$@" >> "$T" 2>&1; printf '[exit=%s]\n' "$?" >> "$T"; }

# --- export the named commit -------------------------------------------------
mkdir -p "$X" && "$GIT" -C "$LANE" archive "$REF" | tar -x -C "$X"

# --- green twin + single-flip mutants (scratch controls) ---------------------
twin() {
  local G=$1
  rm -rf "$G"; mkdir -p "$G/.ufo/waves/round-37/final-gates" "$G/corpus/instruments" "$G/corpus/lessons"
  printf '#!/usr/bin/env bash\n# synthetic green twin instrument (scratch control only)\n' > "$G/corpus/instruments/r37-closure.sh"
  { echo "suite-sha256=$(sha256sum "$G/corpus/instruments/r37-closure.sh" | cut -d' ' -f1)"
    for n in $(seq 1 14); do echo "E$n payload=ok closed=1"; done
    echo "closed=14/14 exit=0"
    for n in $(seq 1 14); do echo "selftest case=E$n"; done
    echo "cases=14 failures=0"; } > "$G/.ufo/waves/round-37/final-gates/all-gates.txt"
  cat > "$G/LOG.md" <<'EOS'
## Round 36 — 2026-10-26 — C1 head-closure suite
- **C1 depth:verifiability (4 held).** Landed `corpus/instruments/r36-closure.sh` + `corpus/instruments/r36-fixtures/`.
## Round 37 — 2026-10-26 — C1 closure of the r36 spot-check defects
- **C1 correction (D2).** The round-36 C1 bullet named `corpus/instruments/r36-fixtures/` — that path does not exist in any commit; it is a false path and is corrected here.
EOS
  cat > "$G/SCORECARD.md" <<'EOS'
## Round 36 — frozen claims C1/C2 (2026-10-26)
Final lane commit: e666d902337a49dcbfc77880939874f39c6f477b
## Round 37 — frozen claims C1/C2 (2026-10-26)
r36 lane head `c20300df516eb5575d8db2aaad1f0cf4913e7981` is labelled `anchor ancestor`; the red anchors land at it.
EOS
  cat > "$G/SKILL.md" <<'EOS'
| Instrument | Type | Run | Outputs | Selftest | Red anchors | Side effects | Author |
| r36-closure.sh | gate | `bash corpus/instruments/r36-closure.sh --export-ref <hash>` | one E line each | `--selftest` | r35 base export | read-only | kasegi |
verdict map: 0 closed | 1 open | 2 -> could-not-evaluate
EOS
  printf '## Round-37 lesson\nr36 lane head c20300df516eb5575d8db2aaad1f0cf4913e7981 is the anchor ancestor.\n' \
    > "$G/corpus/lessons/round-37-lesson.md"
}
rehash() { # refresh the transcript's digest header after a suite mutation
  local G=$1
  local f d
  f=$G/.ufo/waves/round-37/final-gates/all-gates.txt
  d=$(sha256sum "$G/corpus/instruments/r37-closure.sh" | cut -d' ' -f1)
  sed -i "1s/^suite-sha256=.*/suite-sha256=$d/" "$f"
}
twin "$S/green-twin"
# flip E10: digest header no longer binds the suite
rm -rf "$S/flip-e10"; cp -a "$S/green-twin" "$S/flip-e10"
sed -i '1s/^suite-sha256=.*/suite-sha256=deadbeef/' "$S/flip-e10/.ufo/waves/round-37/final-gates/all-gates.txt"
# flip E11: correction removed, false path kept
rm -rf "$S/flip-e11"; cp -a "$S/green-twin" "$S/flip-e11"; sed -i '/C1 correction (D2)/d' "$S/flip-e11/LOG.md"
# flip E12: stale label inside the round-37 section
rm -rf "$S/flip-e12"; cp -a "$S/green-twin" "$S/flip-e12"
sed -i '/anchor ancestor/a Final lane commit: e666d902337a49dcbfc77880939874f39c6f477b' "$S/flip-e12/SCORECARD.md"
# flip E13: literal escaped gate\|probe type cell and no exit-2 verdict map
rm -rf "$S/flip-e13"; cp -a "$S/green-twin" "$S/flip-e13"
sed -i 's/| r36-closure.sh | gate |/| r36-closure.sh | gate\\|probe |/; s/verdict map: 0 closed | 1 open | 2 -> could-not-evaluate/verdict map: 0 closed | 1 open/' "$S/flip-e13/SKILL.md"
# flip E14: fail-open quiescence shape (digest header refreshed so only E14 reds)
rm -rf "$S/flip-e14"; cp -a "$S/green-twin" "$S/flip-e14"
printf 'porcelain=$(git -C "$r" status --porcelain 2>/dev/null | grep -c .)\nporcelain=${porcelain:-0}\n' \
  >> "$S/flip-e14/corpus/instruments/r37-closure.sh"
rehash "$S/flip-e14"

: > "$T"
sec "0. binding (UTC now: $(date -u +%Y-%m-%dT%H:%M:%SZ))"
run "$GIT" --version
printf '$ %s -C %s rev-parse %s\n' "$GIT" "$LANE" "$REF" >> "$T"
"$GIT" -C "$LANE" rev-parse "$REF" >> "$T" 2>&1
printf '$ %s -C %s rev-parse %s^{tree}\n' "$GIT" "$LANE" "$REF" >> "$T"
"$GIT" -C "$LANE" rev-parse "$REF^{tree}" >> "$T" 2>&1
printf '$ %s -C %s log -1 --format="%%H %%ci %%s" %s\n' "$GIT" "$LANE" "$REF" >> "$T"
"$GIT" -C "$LANE" log -1 --format='%H %ci %s' "$REF" >> "$T" 2>&1
printf 'export files=%s   commit ls-tree files=%s\n' \
  "$(find "$X" -type f | wc -l)" "$("$GIT" -C "$LANE" ls-tree -r --name-only "$REF" | wc -l)" >> "$T"
printf 'worktree HEAD=%s (lane is mid-wave; E9 reads this, not the export)\n' \
  "$("$GIT" -C "$LANE" rev-parse HEAD)" >> "$T"

sec "1. r36 suite vs the r36 judged head $REF (item step 1, literal command)"
printf '$ bash corpus/instruments/r36-closure.sh --export-ref %s\n' "$REF" >> "$T"
( cd "$LANE" && bash corpus/instruments/r36-closure.sh --export-ref "$REF" ) >> "$T" 2>&1
printf '[exit=%s]\n' "$?" >> "$T"
printf 'suite sha256 of the export bytes: %s\n' "$(sha256sum "$X/corpus/instruments/r36-closure.sh" | cut -d' ' -f1)" >> "$T"

sec "2a. D1: r37 final-gates transcript absent at $REF (item step 2)"
printf '$ test -e <export>/.ufo/waves/round-37/final-gates/all-gates.txt\n' >> "$T"
if [ -e "$X/.ufo/waves/round-37/final-gates/all-gates.txt" ]; then echo PRESENT >> "$T"; else echo ABSENT >> "$T"; fi
printf '$ ls <export>/.ufo/waves/round-37\n' >> "$T"
ls "$X/.ufo/waves/round-37" >> "$T" 2>&1; printf '[exit=%s]\n' "$?" >> "$T"
printf '$ %s ls-tree -r --name-only %s | grep -c round-37\n' "$GIT" "$REF" >> "$T"
"$GIT" -C "$LANE" ls-tree -r --name-only "$REF" | grep -c 'round-37' >> "$T" 2>&1
printf '$ ls -la <export>/.ufo/waves/round-36/final-gates/ ; head -6 all-gates.txt   (r36 lineage of D1)\n' >> "$T"
ls -la "$X/.ufo/waves/round-36/final-gates/" >> "$T" 2>&1
sed -n '1,6p' "$X/.ufo/waves/round-36/final-gates/all-gates.txt" >> "$T" 2>&1
printf 'r36 transcript: suite-sha256 headers=%s E-payload-lines=%s selftest-case-lines=%s\n' \
  "$(grep -c '^suite-sha256=' "$X/.ufo/waves/round-36/final-gates/all-gates.txt")" \
  "$(grep -cE '^E[0-9]+ payload=' "$X/.ufo/waves/round-36/final-gates/all-gates.txt")" \
  "$(grep -c '^selftest case=' "$X/.ufo/waves/round-36/final-gates/all-gates.txt")" >> "$T"

sec "2b. D2: false r36-fixtures path in LOG.md, no named correction (item step 2)"
printf '$ grep -n r36-fixtures <export>/LOG.md\n' >> "$T"
grep -n 'r36-fixtures' "$X/LOG.md" >> "$T" 2>&1
printf '$ %s ls-tree -r --name-only %s | grep -c r36-fixtures\n' "$GIT" "$REF" >> "$T"
"$GIT" -C "$LANE" ls-tree -r --name-only "$REF" | grep -c 'r36-fixtures' >> "$T" 2>&1
printf '$ ls -d <export>/corpus/instruments/r36-fixtures\n' >> "$T"
ls -d "$X/corpus/instruments/r36-fixtures" >> "$T" 2>&1; printf '[exit=%s]\n' "$?" >> "$T"
printf '$ grep -nE "<window-bounded named correction of that path>" <export>/LOG.md\n' >> "$T"
grep -nE 'r36-fixtures.{0,100}(does not exist|not a real path|false path|is false|was false|never existed|phantom|misnamed|invented)|(correction|corrected|corrigendum|erratum)[^.]{0,100}r36-fixtures' "$X/LOG.md" >> "$T" 2>&1
printf '[exit=%s]\n' "$?" >> "$T"

sec "2c. D4: stale 'Final lane commit: e666d902', no round-37 SCORECARD section, no 'anchor ancestor' (item step 2)"
printf '$ grep -c "Final lane commit: e666d902" <export>/SCORECARD.md\n' >> "$T"
grep -c 'Final lane commit: e666d902' "$X/SCORECARD.md" >> "$T" 2>&1
printf '$ grep -n "Final lane commit" <export>/SCORECARD.md | tail -3\n' >> "$T"
grep -n 'Final lane commit' "$X/SCORECARD.md" | tail -3 >> "$T" 2>&1
printf '$ grep -n "^## Round" <export>/SCORECARD.md | tail -3\n' >> "$T"
grep -n '^## Round' "$X/SCORECARD.md" | tail -3 >> "$T" 2>&1
printf '$ grep -rIl "anchor ancestor" <export> | wc -l ; %s grep -c "anchor ancestor" %s\n' "$GIT" "$REF" >> "$T"
printf 'export-tree files=%s commit-matches=%s\n' \
  "$(grep -rIl 'anchor ancestor' "$X" 2>/dev/null | wc -l)" \
  "$("$GIT" -C "$LANE" grep -c 'anchor ancestor' "$REF" 2>/dev/null | wc -l)" >> "$T"
printf '$ grep -rIl c20300df <export> | wc -l   (true r36 lane head named anywhere?)\n' >> "$T"
printf 'files=%s\n' "$(grep -rIl 'c20300df' "$X" 2>/dev/null | wc -l)" >> "$T"
printf '$ grep -in "final lane commit" <export>/corpus/lessons/round-36.md\n' >> "$T"
grep -in 'final lane commit' "$X/corpus/lessons/round-36.md" >> "$T" 2>&1

sec "2d. D5: r36-closure.sh registry row type cell literal gate|probe, no exit-2 verdict map (item step 2)"
printf '$ sed -n 1111p <export>/SKILL.md\n' >> "$T"
sed -n '1111p' "$X/SKILL.md" >> "$T" 2>&1
printf '$ grep -cF "gate\\|probe" <export>/SKILL.md   (escaped literal, spot-check D5 counting)\n' >> "$T"
grep -cF 'gate\|probe' "$X/SKILL.md" >> "$T" 2>&1
printf '$ grep -c "could-not-evaluate" over SKILL.md lines 1108-1114 (the r36 row block)\n' >> "$T"
awk 'NR>=1108 && NR<=1114' "$X/SKILL.md" | grep -c 'could-not-evaluate' >> "$T" 2>&1
printf '$ grep -c "could-not-evaluate" over all of <export>/SKILL.md\n' >> "$T"
grep -c 'could-not-evaluate' "$X/SKILL.md" >> "$T" 2>&1

sec "2e. D6: fail-open quiescence shape in r36-closure.sh (item step 2)"
printf '$ grep -cF "porcelain:-0" <export>/corpus/instruments/r36-closure.sh\n' >> "$T"
grep -cF 'porcelain:-0' "$X/corpus/instruments/r36-closure.sh" >> "$T" 2>&1
printf '$ grep -nF "porcelain:-0" <export>/corpus/instruments/r36-closure.sh\n' >> "$T"
grep -nF 'porcelain:-0' "$X/corpus/instruments/r36-closure.sh" >> "$T" 2>&1
printf '$ sed -n "293,295p;448,452p;460,467p" <export>/corpus/instruments/r36-closure.sh\n' >> "$T"
sed -n '293,295p' "$X/corpus/instruments/r36-closure.sh" >> "$T" 2>&1
sed -n '448,452p' "$X/corpus/instruments/r36-closure.sh" >> "$T" 2>&1
sed -n '460,467p' "$X/corpus/instruments/r36-closure.sh" >> "$T" 2>&1
printf '$ %s ls-tree -r --name-only %s | grep -c r37-closure.sh\n' "$GIT" "$REF" >> "$T"
"$GIT" -C "$LANE" ls-tree -r --name-only "$REF" | grep -c 'r37-closure.sh' >> "$T" 2>&1
printf '$ %s status --porcelain | wc -l   (live lane, explains the E9 payload)\n' "$GIT" >> "$T"
"$GIT" -C "$LANE" status --porcelain | wc -l >> "$T" 2>&1

sec "3. r37-style E10-E14 stand-in vs the $REF export (item step 3; each RED)"
printf '$ bash r37-standin.sh <export %s>\n' "$REF" >> "$T"
bash "$S/r37-standin.sh" "$X" >> "$T" 2>&1; printf '[exit=%s]\n' "$?" >> "$T"

sec "3c. control: green twin must read 5/5 exit 0 (the stand-in is not blind)"
printf '$ bash r37-standin.sh green-twin\n' >> "$T"
bash "$S/r37-standin.sh" "$S/green-twin" >> "$T" 2>&1; printf '[exit=%s]\n' "$?" >> "$T"

sec "3d. control: single-flip mutants from the green twin (each reds its own check only)"
for f in e10 e11 e12 e13 e14; do
  printf '\n-- flip %s --\n' "$f" >> "$T"
  bash "$S/r37-standin.sh" "$S/flip-$f" >> "$T" 2>&1
  printf '[exit=%s]\n' "$?" >> "$T"
done

printf '\ntranscript lines=%s\n' "$(wc -l < "$T")"

```

</details>

## Tooling

No installs, no upgrades, no pacman (transactions are paused host-wide). Only pre-existing tools were
used: `bash`, `/usr/bin/git` 2.56.0, GNU coreutils/`tar`/`sha256sum`, `grep`, `awk`, `sed`,
`python3` (stdlib only, used solely to patch my own scratch scripts).

## Write hygiene

Wrote exactly two things: this receipt, and files under `/fast/scratch/hyaku/kasegi-r37/ExecC1JudgedHeadFail/`
(removed before yield, `rm -rf`). No lane file, no fleet-root file, no sibling repo, no source tree was
modified; no mutating git/jj command was run (only `rev-parse`, `log`, `ls-tree`, `status`, `archive`,
`grep`, `cat-file`). `git status --porcelain` of the lane was read, never written.

## Residual risk / what this seat did not do

- This is a **red baseline only**. It does not score the r37 instrument, does not verify that the r37 suite
  actually implements E10–E14 with these semantics (the stand-in is my reading of the frozen claim text,
  not the lane's implementation), and does not judge any other seat's evidence.
- If the r37 suite's E10–E14 differ from my stand-in (e.g. a differently-shaped digest header, or an E12
  that only checks SCORECARD), the REDs above still hold for the underlying facts (file absent, false path
  uncorrected, stale label present, escaped type cell present, fail-open shape present); only the
  machine-readable payloads would differ.
- The E9 caveat (F1) means a future `closed=14/14` reading is only meaningful together with the state of the
  live lane at that moment, unless r37 decouples quiescence from the live lane.

## Appendix — raw transcript (verbatim, sha256 40db734cbd1595f6a441304800f9df3f11013153fba24784756704edd583f896)

```text

########## 0. binding (UTC now: 2026-10-26T17:06:43Z) ##########
$ /usr/bin/git --version
git version 2.56.0
[exit=0]
$ /usr/bin/git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse a23dc4788aa7c98831eed6db953434034ce5ae8d
a23dc4788aa7c98831eed6db953434034ce5ae8d
$ /usr/bin/git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse a23dc4788aa7c98831eed6db953434034ce5ae8d^{tree}
78f74821afb6d22479d3c3bdefb27a6c6e270709
$ /usr/bin/git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin log -1 --format="%H %ci %s" a23dc4788aa7c98831eed6db953434034ce5ae8d
a23dc4788aa7c98831eed6db953434034ce5ae8d 2026-10-26 13:00:31 -0300 round-36: final gate receipts + measured closure
export files=7195   commit ls-tree files=7253
worktree HEAD=b362068195d5489aa94b31e6ec8f880c367e0ba0 (lane is mid-wave; E9 reads this, not the export)

########## 1. r36 suite vs the r36 judged head a23dc4788aa7c98831eed6db953434034ce5ae8d (item step 1, literal command) ##########
$ bash corpus/instruments/r36-closure.sh --export-ref a23dc4788aa7c98831eed6db953434034ce5ae8d
export-ref=a23dc4788aa7c98831eed6db953434034ce5ae8d mode=export lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin suite-sha256=4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4
E1 payload=placeholders=0,lane-hash-markers=0,round36-section=1,round36-final-lane-commits=2,bound=2 closed=1
E2 payload=erratum-marker=1,erratum-row=1,erratum-mean=7 closed=1
E3 payload=registry-r35-defect-closure=1,registry-r36-closure=1 closed=1
E4 payload=tracked-ref=1,tracked-index=1,provenance-note=1 closed=1
E5 payload=claims-erratum-d5=1 closed=1
E6 payload=path=.ufo/waves/round-34/wave1/L1Integration.md,correction-round35=1 closed=1
E7 payload=supersedes-r22=1,supersedes-r23=1 closed=1
E8 payload=m36-rows=4,names-corrected-line=3,stale-line=0,round35-lesson=1 closed=1
E9 payload=status-dirty=6,scratch-seat-dirs=0,head-match=0,lane-root=1,scratch-root=present closed=0
closed=8/9 exit=1
[exit=1]
suite sha256 of the export bytes: 4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4

########## 2a. D1: r37 final-gates transcript absent at a23dc4788aa7c98831eed6db953434034ce5ae8d (item step 2) ##########
$ test -e <export>/.ufo/waves/round-37/final-gates/all-gates.txt
ABSENT
$ ls <export>/.ufo/waves/round-37
ls: cannot access '/fast/scratch/hyaku/kasegi-r37/ExecC1JudgedHeadFail/exp-a23dc478/.ufo/waves/round-37': No such file or directory
[exit=2]
$ /usr/bin/git ls-tree -r --name-only a23dc4788aa7c98831eed6db953434034ce5ae8d | grep -c round-37
0
$ ls -la <export>/.ufo/waves/round-36/final-gates/ ; head -6 all-gates.txt   (r36 lineage of D1)
total 8
drwxr-xr-x 2 vgpnk vgpnk   27 Oct 26 13:00 .
drwxr-xr-x 6 vgpnk vgpnk 4096 Oct 26 13:00 ..
-rw-r--r-- 1 vgpnk vgpnk 1203 Oct 26 13:00 all-gates.txt
== selftest ==
selftest judge=forged-caselines rejected=1
selftest judge=forged-failed-cases rejected=1
selftest judge=forged-detail-free rejected=1
== neg base ==
closed=0/9 exit=1
r36 transcript: suite-sha256 headers=0 E-payload-lines=0 selftest-case-lines=0

########## 2b. D2: false r36-fixtures path in LOG.md, no named correction (item step 2) ##########
$ grep -n r36-fixtures <export>/LOG.md
1665:- **C1 depth:verifiability (4 held) — head-closure suite over exports.** Landed `corpus/instruments/r36-closure.sh` + `corpus/instruments/r36-fixtures/`. `--export-ref <commit>` extracts the lane with `git -C … archive <commit>` into a scratch root and runs every check against that export; a plain run without the flag refuses (exit 2) instead of reading the worktree. Nine checks E1–E9 print one payload line each plus `closed=K/9 exit=E`: `closed=9/9 exit=0` at the round-36 final lane head, `selftest case=<name>` verdict lines with `cases=9 failures=0` under `--selftest` (a summary-only forgery does not satisfy it), and the required reds — round-35 base export `closed=0/9 exit=1`, round-35 judged head export `closed<9/9 exit=1`. What the checks bind, re-measured by this seat on committed bytes at freeze `b47f2cd` against both round-35 refs: E1 placeholder/hash binding — `filled by the L1` **1** at each r35 export (`SCORECARD.md:1240` at the base, `:1271` at the judged head) and **0** at freeze, the angle-bracket lane-hash marker 0 in all three revisions, and the `Final lane commit:` line's 40-hex hash must resolve and be an ancestor of the exported ref; E2 round-34 depth:density erratum — `201.2` **0** at the r35 base vs **6** lines at freeze; E3 exact-basename registry rows — `r35-defect-closure.sh` **0** and `r36-closure.sh` **0** in `SKILL.md` at freeze, both still owed (the near-name `r-defect-closure.sh` occupies 3 `SKILL.md` lines, the stem `r-defect-closure` 4 lines / 9 occurrences, so the round-35 literal was satisfied by a sibling name — M36-3); E4 `.ufo/waves/round-35/wave1-results.json` tracked **1** at freeze (0 at the judged head) with a provenance note beside it (**0** at freeze — this round's add); E5 `.ufo/waves/round-35/claims-erratum-d5.md` present **1**; E6 `Correction (round 35)` in `.ufo/waves/round-34/wave1/L1Integration.md` **1** at freeze, **0** at the r35 base (file present in both); E7 `supersedes R22` / `supersedes R23` rows in `corpus/QUALITY.md` **1 / 1**; E8 the round-35 lesson's false evidence lines (`source-recheck exit 0 on committed bytes`, `SKILL.md +13/0`, `LOG.md 0 changed`) — **1** stale line at the judged head, **0** at freeze, correction recorded in `corpus/lessons/round-36.md`; E9 quiescence — `git status --porcelain` empty and no leftover `/fast/scratch/hyaku/kasegi-r36` seat dirs at filing. `corpus/QUALITY.md` gains **R28** (a round's claims rest on committed paths at the quoted head; counters run over exports; the lane is quiescent before filing — considerthese 2026-10-26 proposal 3) and **R29** (an instrument is registered in `SKILL.md` by its exact basename; a near-name sibling does not satisfy the registry literal — M36-3). The round-36 after-state figures are the frozen claims' contract values; the instrument's own run at the final head and the round report are the evidence of record, and a deviation lands as an appended erratum, never as an edit.
$ /usr/bin/git ls-tree -r --name-only a23dc4788aa7c98831eed6db953434034ce5ae8d | grep -c r36-fixtures
0
$ ls -d <export>/corpus/instruments/r36-fixtures
ls: cannot access '/fast/scratch/hyaku/kasegi-r37/ExecC1JudgedHeadFail/exp-a23dc478/corpus/instruments/r36-fixtures': No such file or directory
[exit=2]
$ grep -nE "<window-bounded named correction of that path>" <export>/LOG.md
[exit=1]

########## 2c. D4: stale 'Final lane commit: e666d902', no round-37 SCORECARD section, no 'anchor ancestor' (item step 2) ##########
$ grep -c "Final lane commit: e666d902" <export>/SCORECARD.md
1
$ grep -n "Final lane commit" <export>/SCORECARD.md | tail -3
987:integration commit `9f9848816503aa0cd566fc2efdc5e69ea501a253`). **Final lane commit:
1129:`c2-controls/before.txt`) and `census-before.txt`. **Final lane commit:
1492:Final lane commit: e666d902337a49dcbfc77880939874f39c6f477b
$ grep -n "^## Round" <export>/SCORECARD.md | tail -3
1263:## Round 35 — frozen claims C1/C2 (2026-10-26)
1284:## Round 35 — frozen claims C1/C2 (2026-10-26)
1406:## Round 36 — frozen claims C1/C2 (2026-10-26)
$ grep -rIl "anchor ancestor" <export> | wc -l ; /usr/bin/git grep -c "anchor ancestor" a23dc4788aa7c98831eed6db953434034ce5ae8d
export-tree files=0 commit-matches=0
$ grep -rIl c20300df <export> | wc -l   (true r36 lane head named anywhere?)
files=0
$ grep -in "final lane commit" <export>/corpus/lessons/round-36.md
3:Lane: `kasegi-shokunin`. Base `cc692008b0cfd58d18275aa6c4aed79620120799`; claims-freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`; final lane commit `e666d902337a49dcbfc77880939874f39c6f477b` (filled at closure). Shape: one v2 wave `kasegi-r36-build`, 64 seats (executor 18, scribe 12, reviewer 10, critic 6, scout 6, mutation-tester 5, connector 3, sentinel 2, simplifier 2; attack roles 23/64 = 35.9%).

########## 2d. D5: r36-closure.sh registry row type cell literal gate|probe, no exit-2 verdict map (item step 2) ##########
$ sed -n 1111p <export>/SKILL.md
| r36-closure.sh | gate\|probe | `bash corpus/instruments/r36-closure.sh --export-ref <hash>` (export-mode only; a plain run refuses with exit 2) | one `E<n> payload=… closed=0\|1` line per check E1–E9, then `closed=K/9 exit=0\|1`; exit 0 only for K=9 | `bash corpus/instruments/r36-closure.sh --selftest` -> `selftest cases=9 failures=0` exit 0 | r35 base export `3266c993` -> `closed=0/9 exit=1`; r35 judged head `0aee0ef` -> `closed<9/9 exit=1` | read-only (export to a scratch work dir) | kasegi (round 36) |
$ grep -cF "gate\|probe" <export>/SKILL.md   (escaped literal, spot-check D5 counting)
6
$ grep -c "could-not-evaluate" over SKILL.md lines 1108-1114 (the r36 row block)
0
$ grep -c "could-not-evaluate" over all of <export>/SKILL.md
1

########## 2e. D6: fail-open quiescence shape in r36-closure.sh (item step 2) ##########
$ grep -cF "porcelain:-0" <export>/corpus/instruments/r36-closure.sh
1
$ grep -nF "porcelain:-0" <export>/corpus/instruments/r36-closure.sh
466:  porcelain=${porcelain:-0}
$ sed -n "293,295p;448,452p;460,467p" <export>/corpus/instruments/r36-closure.sh
count_lines() { # reads stdin
  grep -c . 2>/dev/null || true
}
check_e9() { # TREE REF [SCRATCH_ROOT [STATUS_REPO [EXPECTED_HEAD]]]
  local ref=$2
  local sroot=${3:-$SCRATCH_ROOT}
  local srepo=${4:-$LANE}
  local want=${5:-$ref}
  root=$( cd "$srepo" 2>/dev/null && pwd -P )
  top=$(git -C "$srepo" rev-parse --show-toplevel 2>/dev/null)
  if [ -n "$top" ] && [ -n "$root" ] && [ "$top" = "$root" ]; then root_ok=1; fi
  # --no-optional-locks: plain `git status` takes and unlinks .git/index.lock,
  # a transient write under the lane. This suite must leave the lane untouched.
  porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain 2>/dev/null | count_lines)
  porcelain=${porcelain:-0}
  if [ -n "${WORK:-}" ]; then skip=$( cd "$WORK" 2>/dev/null && pwd -P ); fi
$ /usr/bin/git ls-tree -r --name-only a23dc4788aa7c98831eed6db953434034ce5ae8d | grep -c r37-closure.sh
0
$ /usr/bin/git status --porcelain | wc -l   (live lane, explains the E9 payload)
6

########## 3. r37-style E10-E14 stand-in vs the a23dc4788aa7c98831eed6db953434034ce5ae8d export (item step 3; each RED) ##########
$ bash r37-standin.sh <export a23dc4788aa7c98831eed6db953434034ce5ae8d>
E10 payload=file=0(reason=absent:.ufo/waves/round-37/final-gates/all-gates.txt),digest-bound=0,E-lines=0,selftest-lines=0,summary=0,closed-line=0 closed=0
E11 payload=false-path-lines=1,named-correction-lines=0 closed=0
E12 payload=round37-section=0,anchor-ancestor-c20300df=0,stale-e666d902=1(whole-file),r37-lesson-anchor=0 closed=0
E13 payload=row=1,literal-escaped-gate-pipe-probe=1,single-choice=0,exit2-verdict=0(window=0) closed=0
E14 payload=r37-suite=0(absent),r36-fallback:porcelain:-0=1,status-swallow=1 closed=0
closed=0/5 exit=1
[exit=1]

########## 3c. control: green twin must read 5/5 exit 0 (the stand-in is not blind) ##########
$ bash r37-standin.sh green-twin
E10 payload=file=1,digest-bound=1,E-lines=14,selftest-lines=14,summary=1,closed-line=1 closed=1
E11 payload=false-path-lines=2,named-correction-lines=1 closed=1
E12 payload=round37-section=1,anchor-ancestor-c20300df=1,stale-e666d902=0,r37-lesson-anchor=1 closed=1
E13 payload=row=1,literal-escaped-gate-pipe-probe=0,single-choice=1,exit2-verdict=1(window=1) closed=1
E14 payload=r37-suite=1,porcelain:-0=0,status-swallow=0 closed=1
closed=5/5 exit=0
[exit=0]

########## 3d. control: single-flip mutants from the green twin (each reds its own check only) ##########

-- flip e10 --
E10 payload=file=1,digest-bound=0,E-lines=14,selftest-lines=14,summary=1,closed-line=1 closed=0
E11 payload=false-path-lines=2,named-correction-lines=1 closed=1
E12 payload=round37-section=1,anchor-ancestor-c20300df=1,stale-e666d902=0,r37-lesson-anchor=1 closed=1
E13 payload=row=1,literal-escaped-gate-pipe-probe=0,single-choice=1,exit2-verdict=1(window=1) closed=1
E14 payload=r37-suite=1,porcelain:-0=0,status-swallow=0 closed=1
closed=4/5 exit=1
[exit=1]

-- flip e11 --
E10 payload=file=1,digest-bound=1,E-lines=14,selftest-lines=14,summary=1,closed-line=1 closed=1
E11 payload=false-path-lines=1,named-correction-lines=0 closed=0
E12 payload=round37-section=1,anchor-ancestor-c20300df=1,stale-e666d902=0,r37-lesson-anchor=1 closed=1
E13 payload=row=1,literal-escaped-gate-pipe-probe=0,single-choice=1,exit2-verdict=1(window=1) closed=1
E14 payload=r37-suite=1,porcelain:-0=0,status-swallow=0 closed=1
closed=4/5 exit=1
[exit=1]

-- flip e12 --
E10 payload=file=1,digest-bound=1,E-lines=14,selftest-lines=14,summary=1,closed-line=1 closed=1
E11 payload=false-path-lines=2,named-correction-lines=1 closed=1
E12 payload=round37-section=1,anchor-ancestor-c20300df=1,stale-e666d902=1,r37-lesson-anchor=1 closed=0
E13 payload=row=1,literal-escaped-gate-pipe-probe=0,single-choice=1,exit2-verdict=1(window=1) closed=1
E14 payload=r37-suite=1,porcelain:-0=0,status-swallow=0 closed=1
closed=4/5 exit=1
[exit=1]

-- flip e13 --
E10 payload=file=1,digest-bound=1,E-lines=14,selftest-lines=14,summary=1,closed-line=1 closed=1
E11 payload=false-path-lines=2,named-correction-lines=1 closed=1
E12 payload=round37-section=1,anchor-ancestor-c20300df=1,stale-e666d902=0,r37-lesson-anchor=1 closed=1
E13 payload=row=1,literal-escaped-gate-pipe-probe=1,single-choice=0,exit2-verdict=0(window=0) closed=0
E14 payload=r37-suite=1,porcelain:-0=0,status-swallow=0 closed=1
closed=4/5 exit=1
[exit=1]

-- flip e14 --
E10 payload=file=1,digest-bound=1,E-lines=14,selftest-lines=14,summary=1,closed-line=1 closed=1
E11 payload=false-path-lines=2,named-correction-lines=1 closed=1
E12 payload=round37-section=1,anchor-ancestor-c20300df=1,stale-e666d902=0,r37-lesson-anchor=1 closed=1
E13 payload=row=1,literal-escaped-gate-pipe-probe=0,single-choice=1,exit2-verdict=1(window=1) closed=1
E14 payload=r37-suite=1,porcelain:-0=1,status-swallow=1 closed=0
closed=4/5 exit=1
[exit=1]
```
