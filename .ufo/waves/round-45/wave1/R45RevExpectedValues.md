VERDICT: HOLDS

Scope: reproduce every `before` value in `.ufo/waves/round-45/claims.json` (C1, C2), `freeze.txt` and `controls/freeze-controls.txt` from a fresh `git archive dc5bb8c6e31efc4a6650819df85e79b72fd64bcd` export. Lane HEAD at run time: `5242db6`. Counters were run from the lane checkout (`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/`) against the export. No file in the lane, the fleet, git index or any shared file was written. Scratch was removed on exit.

Base export: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive dc5bb8c6e31efc4a6650819df85e79b72fd64bcd | tar -x -C <scratch>/base` (8932 files). After all counter runs, `diff -rq` against a second fresh archive printed nothing (`diff rc=0`), so the counters left the export unchanged.

## 1. C1 before-value: reproduces

Command: `python3 corpus/instruments/r45-routed-defects.py --root <base> --baseline <base>`

Output (verbatim):
```
limb R1 fixed=0 read=row-S072=absent
limb R2 fixed=0 read=quality-not-append-only-or-unchanged
limb R3 fixed=0 read=selftest-rc=2-tokens=None
limb R4 fixed=0 read=freeze-check-absent
limb R5 fixed=0 read=refiled-absent
routed-defects total=5 fixed=0 unresolved=5 exit=1
```
Matches `claims.json` C1 `expect_before` ("routed-defects total=5 fixed=0 unresolved=5 exit=1").

Base-state checks behind the limb reads:
- `ls corpus/instruments/freeze-check.py` at base and lane: `No such file or directory` (R4).
- `ls .ufo/waves/round-44/controls/final-attempt3-refiled.txt` at base: `No such file or directory` (R5).
- `grep -c 'selftest' corpus/instruments/r44-frontier-count.py` finds nothing, and `git diff --quiet dc5bb8c HEAD -- corpus/instruments/r44-frontier-count.py` reports the file identical (R3: the probe has no `--selftest`, so rc=2).
- Lesson §6 has six numbered items (`grep -nE '^[0-9]+\. \*\*'`, lines 79-84). Items 1-5 are the counted set, item 6 is the uncounted L1 process defect. Matches the counter's stated set.
- Item 5 before-state: `.ufo/waves/round-44/controls/final-attempt3.txt` lines 14-18 show the bare `--selftest` call, `usage: ... error: the following arguments are required: --root`, then `exit=0`. The defect as filed reproduces.

## 2. C2 before-value: reproduces

Command: `python3 corpus/instruments/r45-c2-gate.py --root <base>`

Output (verbatim):
```
gate G1 pass=0 read=rows=26 admitted=26 dup=0
gate G2 pass=0 read=F27-rows=0
gate G3 pass=0 read=row-S071=absent-or-malformed
gate G4 pass=0 read=manifest-absent
gate G5 pass=0 read=F27-rows=0
gate G6 pass=0 read=knowledge=63
gate G7 pass=1 read=census-rc=0
c2-gate fixed=1/7 exit=1
```
Matches `expect_before` ("c2-gate fixed=1/7 exit=1").

Secondary: `python3 corpus/instruments/r44-frontier-count.py --root <base> --expect 27` prints
```
frontier rows=26 admitted=26
frontier expected=27 admitted=26 verdict=SHORT exit=1
```
Matches the claims secondary note ("frontier rows=26 admitted=26 exit 1").

Note on G7: the one passing gate at base is the external census `SOURCES_CENSUS` default `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (outside the lane, read by the gate at run time). Re-running `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <base>/corpus/SOURCES.md` printed `census rc=0` and `file ok <base>/corpus/SOURCES.md`. So the `1/7` before-value depends on a fleet file, not on the lane. That is a reproducibility limitation, not a number that fails to reproduce.

## 3. Numerals in claims.json: all reproduce

Counting commands run on `<base>`:

| claim | command | printed |
|---|---|---|
| 26 frontier rows | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` (the CORPUS README basis, line 446) | `26` |
| 26 admitted | `grep -cE '^\| F[0-9]+ \| [^\|]* \| admitted \|' corpus/README.md` | `26` |
| F01-F26 contiguous | `grep -oE '^\| F[0-9]+ \|'` | `F01 F02 ... F26` (26 ids, no gaps, no duplicates) |
| 63 knowledge entries | G6 basis: `find corpus/knowledge -maxdepth 1 -name '*.md' \| wc -l` | `63` |
| 63 (cross-check) | `ls corpus/knowledge/*.md \| wc -l`; `find corpus/knowledge -type f \| wc -l` | `63`; `63` |
| 70 SOURCES rows | `grep -cE '^\| S[0-9]+ \|' corpus/SOURCES.md` | `70` (unique ids 70, `wc -l` of file 154) |

`corpus/instruments/knowledge-expected.txt` has 65 lines = 63 entries + 2 `#` comment lines (`grep -vcE '^\s*(#|$)'` → 63, `grep -cE '^\s*#'` → 2). Sorted entries are set-equal to `ls corpus/knowledge/*.md` at base (`diff` empty), consistent with the README line 236 basis note.

## 4. Frozen control receipt: reproduces

Command: `python3 .ufo/waves/round-45/controls/freeze-controls.py --base-export <base> --lane <lane> --work <scratch>/controls`

Output (identical to the recorded `controls/freeze-controls.txt`, five lines, rc=0):
```
control do-nothing-base counter=C1 routed-defects total=5 fixed=0 unresolved=5 exit=1 expect=RED got=RED
control do-nothing-base counter=C2 c2-gate fixed=1/7 exit=1 expect=RED got=RED
control c1-marker-only counter=C1 routed-defects total=5 fixed=0 unresolved=5 exit=1 expect=RED got=RED
control c2-junk-row counter=C2 c2-gate fixed=4/7 exit=1 expect=RED got=RED
control c2-fabricated-quote counter=C2 c2-gate fixed=5/7 exit=1 expect=RED got=RED
controls total=5 red=5 green=0
```

Discrimination, per limb (run on the control trees the script builds):
- `c1-marker-only` (C1): R1 `row-S072=absent`; R2 `R47-enforced-by-missing-corpus/instruments/nothing.py`; R3 `selftest-rc=2-tokens=None`; R4 `freeze-check-absent`; R5 `invocation-absent`. Marker prose alone fails on the artifact-bearing limbs, and R2 correctly rejects the non-existent `enforced-by:` path.
- `c2-junk-row` (C2): G1 pass, G2 pass, G3 fail (`row-S071=absent-or-malformed`), G4 fail (`manifest-absent`), G5 fail (`spans=0 located=0 failed=0 cores=0/4`), G6 pass (`knowledge=64`), G7 pass. Four passes = `fixed=4/7`, as recorded. The junk row clears presence-only limbs and is stopped by G3-G5, which is the intended behaviour.
- `c2-fabricated-quote` (C2): G4 pass (`recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`, because the snapshot and manifest are genuine), G5 fail (`spans=4 located=0 failed=4 cores=0/4`). The fabricated quotes are rejected by the located-quote limb, not by the manifest limb. Five passes = `fixed=5/7`.

No control grades GREEN, so the do-nothing and fabricated-quote controls are discriminated as claimed.

## 5. Hashes, freeze provenance: reproduce

- `sha256sum .ufo/waves/round-45/claims.json` = `bbe40503281c90eb9d70f469d7bac10125b285758ca9675be9894ce6c12c6206`; identical to `claims-sha256` in `freeze.txt` and to the blob at freeze commit `8cf62c879e6e6b031e67412f8fac1fba0bd378cf`.
- `git diff --stat 8cf62c8 HEAD -- .ufo/waves/round-45/claims.json .ufo/waves/round-45/freeze.txt .ufo/waves/round-45/controls/ corpus/instruments/r45-routed-defects.py corpus/instruments/r45-c2-gate.py` printed nothing: the frozen claims, controls and both counters are unchanged between freeze and HEAD `5242db6`.
- Commit times: `8cf62c8` committer `2026-10-28T17:55:40-03:00` (= 20:55:40Z), consistent with `frozen-at: 2026-10-28T20:55:34Z`. Its author date is `2026-10-28T17:47:59-03:00` (= 20:47:59Z), which is identical to base commit `dc5bb8c`'s date and precedes S071's `fetched_utc: 2026-10-28T20:52:44Z` (corpus/source-snapshots/round-45/manifest.json). Low severity: author dates are mutable and the committer date is after the capture. Recorded, not counted.

## 6. Wording finding (C2 `before`): overbroad scope

`claims.json` C2 `before` says the Linux kernel process is "held nowhere in corpus/", and then cites a grep limited to `corpus/knowledge corpus/SOURCES.md corpus/README.md`. That grep prints nothing (`c2-before-sweep` rc=1, reproduced). A whole-`corpus/` grep returns three files, none of which holds the process:
- `corpus/source-snapshots/round-30/S046.txt:285`: `Linux Kernel (Kernel.org)` (vendor-name table cell)
- `corpus/source-snapshots/round-30/S047.txt:337`: `Linux Kernel (Linux)` (vendor-name table cell)
- `corpus/source-snapshots/round-35/S052.txt`: `git.kernel.org` / `lore.kernel.org` commit and mailing-list links inside CVE `notes` fields (0 `security-bugs` matches)

`grep -rl 'security-bugs' corpus/` prints 0 files. The substance of the claim (the security-bugs reporting process is not held) reproduces; the phrase "held nowhere in corpus/" should read "held in no knowledge entry, SOURCES row or README row, and no snapshot contains `security-bugs`". Wording only; no number changes.

## 7. Limitations

- I did not build F27, S071 or S072 or any C1 repair; the seat was verification-only. The "after" values were not evaluated.
- G7 (C2) and the census are fleet-external: they depend on `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` via the `SOURCES_CENSUS` default. Reproduced at rc=0 here; a different fleet copy could change `1/7`.
- The lane HEAD may not yet contain `freeze-check.py` or the round-44 refiled receipt, so R4/R5 `before` reads are reproduced at base and lane only in the sense of absence (`ls` error). I did not re-run them against any post-builder tree.
- Counts were read from the base export only; I did not count the lane tree beyond the freeze-controls rerun.
- The C2 gate G4 runs `source-recheck.py` through the root tree, so it was not exercised at base (manifest absent); the fabricated-quote control exercised it with the genuine snapshot.
- Nothing was committed, pushed, or mutated in git/jj/index; the only write is this report.
