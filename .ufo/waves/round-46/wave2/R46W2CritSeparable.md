VERDICT: HOLDS

# R46W2CritSeparable — are C1 and C2 causally separable at lane tip 5437afe?

Seat: R46W2CritSeparable (critic, leaf, read-only except this Report). Lane: kasegi round 46. Tip: `5437afeaf9b642c267bba3c31f00ae701e49da68` (exported with `git archive`). Base: `914ca0b6956f01d87b2e252ffad06fe74ec5d9ba`. Counter bytes at tip, matching `counter-errata.md`: `r46-c1-gate.py` sha256 `99e0ee55…475cc`, `r46-c2-gate.py` sha256 `b52fea31…34958621`. Only git read commands were run (`cat-file`, `log`, `diff`, `archive`, `show`); nothing committed or mutated.

Interpretation: the brief says "base + freeze counters" for T1. I used the v1.1 harness bytes (the graded counters) in every tree, because the brief also says to run v1.1 on each. The v1 bytes were used only for the errata check in §4.

## 1. Six counter lines (the separability test)

Trees (scratch under `/fast/scratch/hyaku/kasegi-r46/R46W2CritSeparable/`, removed at exit):
- `base`: `git archive 914ca0b6` (do-nothing control).
- `T1` = base + tip's `corpus/knowledge/claim-gates.md` + `claim-package-contract.md` (C1 files only).
- `T2` = base + tip's `corpus/README.md`, `corpus/SOURCES.md`, `PROVINCE.md`, `corpus/instruments/knowledge-expected.txt`, `corpus/knowledge/github-private-vulnerability-reporting.md`, `corpus/source-snapshots/round-46/{S073.txt,manifest.json}` (C2 files only).
- `T12` = T1 + T2.
- Each tree also got the v1.1 `r46-c1-gate.py` and `r46-c2-gate.py` copied in. `diff -rq tip/corpus T12/corpus` shows only the harness files not copied (`r46-counters-selftest-c1.py`, `r46-counters-selftest-c2.py`, `r46-landing-gate.py`, `r46-plain-measure.sh`), so T12 carries the same claim bytes as the tip.

Commands (counters run from the tip copy, `TMPDIR` set per tree):
`python3 <tip>/corpus/instruments/r46-c1-gate.py --root <tree> --baseline <base>` and `python3 <tip>/corpus/instruments/r46-c2-gate.py --root <tree>`.

Output, verbatim last lines:
```
base  c1: c1-gate fixed=1/7 exit=1        base  c2: c2-gate fixed=1/7 exit=1
T1    c1: c1-gate fixed=7/7 exit=0        T1    c2: c2-gate fixed=1/7 exit=1
T2    c1: c1-gate fixed=1/7 exit=1        T2    c2: c2-gate fixed=7/7 exit=0
T12   c1: c1-gate fixed=7/7 exit=0        T12   c2: c2-gate fixed=7/7 exit=0
tip   c1: c1-gate fixed=7/7 exit=0        tip   c2: c2-gate fixed=7/7 exit=0
```
The tip export gives the same gate lines as T12, line for line.

Per-gate detail (verbatim):
- T1 c1: `gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64`; `gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md`; `gate L6 pass=1 read=mutants=46 survivors=none`; `gate L7 pass=1 read=still-gated=22 changed=none`.
- T2 c2: `gate G1 pass=1 read=rows=28 admitted=28 entry=corpus/knowledge/github-private-vulnerability-reporting.md`; `gate G4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0`; `gate G5 pass=1 read=spans=21 located=21 failed=0 uncited=0 cores=5/5`; `gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1`; `gate G7 pass=1 read=census-rc=0 ok-line=1`.
- T1 c2 (C2 absent): `gate G1 pass=0 read=rows=27 admitted=27 dup=0`, `G2 pass=0 read=F28-rows=0`, `G3 pass=0 read=row-S073=absent-or-malformed`, `G4 pass=0 read=manifest-absent`, `G6 pass=0 read=knowledge=64 entries=64 nested-md=64 base-intact=1 entry-bytes-ok=0`; only `G7` passes (census), which is why it reads 1/7.
- T2 c1 (C1 absent): `gate L1 pass=0 read=gated=24 broken=0 lines=65/base=64`; `gate L2 pass=0 read=base-gated=24 regrounded=0 `; only `L7` passes.

Do-nothing control: base reads 1/7 on both counters; each counter's failing limbs are the ones the claims say are missing (C1: L1-L6 red; C2: G1-G6 red, census G7 green).

Reading: C1 alone reads 7/7, C2 alone reads 7/7, and both together read 7/7. The frozen-counter separability question holds. The wave-1 break is gone:
- v1 `r46-c2-gate.py` (`git show 9f23aab4…:corpus/instruments/r46-c2-gate.py`, sha256 `0ee95857…`) on T12 prints `gate G6 pass=0 read=knowledge=65 base-names-intact=0 entry-bytes-ok=1` and `c2-gate fixed=6/7 exit=1`. This reproduces wave-1 `R46ConnSeparable.md` F1.
- v1 on T2 prints `c2-gate fixed=7/7 exit=0`; v1.1 on T12 prints `gate G6 pass=1 read=knowledge=65 entries=65 nested-md=65 base-intact=1 entry-bytes-ok=1`.
- So the v1.1 name-only exemption (`r46-c2-gate.py:68` `CONTENT_EXEMPT = {"claim-package-contract.md", "claim-gates.md"}`, used at `:315`) is what separates the two claims. It is not a general relaxation: the names stay pinned, and a change to any other base entry still fails G6.

## 2. Remaining couplings (each probed; none breaks a reading)

### 2a. The F28 recheck line against C1's L1/L2 (gated count and `lines >= base`)
Attacked: `r46-c1-gate.py:226-229` (`ok = len(gt) <= TARGET_GATED and not broken and len(ct) >= len(cb)`; `ok = len(reg) >= MIN_REGROUNDED and len(gt) == len(gb) - len(reg) and not (gt - gb)`), against the F28 recheck at `corpus/knowledge/github-private-vulnerability-reporting.md:5`:
`recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073 # 180d`
- At tip the line executes (not gated), so `lines=65/base=64` and `gated=22`. The lines limb has one line of slack.
- Mutant M2 (T12 with `round-46/manifest.json` changed to `round-46/manifest-x.json` in that line): `gate L1 pass=0 read=gated=23 broken=0 lines=65/base=64`; `gate L2 pass=0 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md`; `c1-gate fixed=5/7 exit=1`. C2 on the same mutant: `gate G2 pass=0 read=source=1 verified-at=1 recheck=0 …` and `c2-gate fixed=6/7 exit=1`.
- Reading: C1's gated count depends on C2's recheck line. A gated new line in C2 moves C1 directly. C2's own G2 catches the same defect. This is one-way (C2 content into C1's count), not a reading break, and it matches wave-1 F2.

### 2b. knowledge-expected.txt against recheck-audit
Attacked: `recheck-audit.py` expected-list check (default `<root>/corpus/instruments/knowledge-expected.txt`, `:372`), and the `:408` guard that prints `missing=`/`unexpected=` only when not `--quiet`.
- T1b = T1 + C2's non-entry files (README, SOURCES, PROVINCE, knowledge-expected.txt), without the F28 entry. `recheck-audit.py --root T1b` prints `executes=42 gated=22 broken=0` and `expect=present expected=65 missing=1 unexpected=0 exit=1` (the missing name is `corpus/knowledge/github-private-vulnerability-reporting.md`). The same run with `--quiet` exits 1 and omits the `missing=` line.
- `r46-c1-gate.py` does not read knowledge-expected.txt. On T1b it reads `c1-gate fixed=7/7 exit=0`.
- Reading: the counters are separable. The audit's exit status is coupled to C2's expected-list line. The errata's plain pipeline `recheck-audit.py --root . --quiet | grep '^executes='` discards both the exit code and the `missing=` line, so it cannot see this drift.

### 2c. SOURCES/README/PROVINCE/knowledge-expected edits against C1's L7 byte identity
- T1b (C1 files plus C2's non-entry files): `c1-gate fixed=7/7 exit=0`, with `gate L7 pass=1 read=still-gated=22 changed=none` and `gate L4 pass=1 read=entry-mode-green-anchors-unchanged=2`. C2's README, SOURCES, PROVINCE and expected-list edits do not move C1's gates.
- Grep of the 64 base `recheck:` lines for `SOURCES|README|PROVINCE|knowledge-expected|source-snapshots`: no line names SOURCES, README, PROVINCE or knowledge-expected. The only matches are `source-snapshots/round-NN/manifest.json` paths read by source-recheck, which C2 does not edit at those round numbers.
- ANCHOR_DIRS (`r46-c1-gate.py:62`) is `corpus/instruments/` and `corpus/source-snapshots/`. Those directories contain C2 edits (`knowledge-expected.txt`, `S073.txt`, `manifest.json`), so a C1 row could in principle anchor to them. L4 closes this (`r46-c1-gate.py:243-245`: an anchored file that is absent at BASE, or differs from BASE, sets `planted=True`). I did not run a mutant for this; it is a code reading, not an exercised result.
- Census E11 (SOURCES side of C2 with no entry): `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <T1b>/corpus/SOURCES.md` prints `file	E11	S073 missing used-by corpus/knowledge/github-private-vulnerability-reporting.md` and exits 1. So C2's SOURCES row cannot land ahead of its entry, which is a coupling inside C2. C1 is untouched.

### 2d. recheck-audit and score-gap read the live lane for `cd` lines (measurement hazard)
Attacked: `recheck-audit.py:123` `lane_rc, lane_digest = run(line, root)`. The `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` prefix is part of the line, so the `cd` moves the run to the live lane, whatever `--root` says. `r46-c1-gate.py:199` strips the prefix (`CD_RE.sub`) and runs the line in the tree, which is why the C1 counter is tree-rooted and the audit is not.
- Mutant M1 = T1 with one re-grounded token blanked in the tree's own `claim-gates.md`: `'custodian-receipts.json',` → `'custodian-receipts.jsonX',` (token cell of G1). Output:
  - `c1-gate` on M1: `gate L1 pass=0 read=gated=23 broken=0 lines=64/base=64`; `gate L2 pass=0 read=base-gated=24 regrounded=1 claim-package-contract.md`; `gate L7 pass=0 read=still-gated=23 changed=claim-gates.md`; `c1-gate fixed=4/7 exit=1`.
  - `plain-rows.sh M1 claim-gates.md`: `rows=25 located=24`.
  - `recheck-audit.py --root M1 --quiet`: `executes=42 gated=22 broken=0`. The audit reads green, because its `cd`-prefixed line executed the live `claim-gates.md`.
- Base export under the audit: `strict pass=1/64 cdroot_fail=63` (all 63 cd-prefixed lines fail the cdroot limb in a copy).
- Same tree, different live state: wave-1 `R46ConnSeparable.md:82` recorded `recheck-audit --quiet: executes=41 gated=24 broken=0` on its T12. My T12 at tip gives `executes=43 gated=22 broken=0`. I did not rebuild the wave-1 tree, so this is indicative: the change is in the live lane the cd lines execute against, not in the tree.
- Reading: the errata's plain check `recheck-audit.py --root . --quiet | grep '^executes='` is valid at the tip only because `.` is the live lane. It cannot grade a tree (T1, T12, a mutant). `score-gap.py` documents the same invocation (`recheck-audit.py --root <root> --quiet`, its line 19); I did not run score-gap, so its numbers are not in this report.

### 2e. C2's G7 depends on a file outside the lane
`r46-c2-gate.py:54`: `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`. This is the fleet root, not the lane. It was run read-only. The counter is not self-contained: a changed census script changes G7 without any lane change. Not a C1 coupling; a provenance caveat for C2.

### 2f. Host dependence (shared by both claims)
- `test -d ~/Projects/bounties` is absent on this host, and `~/Projects/ufo-fsd-alpha` is present. C1's base gated count (24) and its target (≤22) depend on HOME-relative `test -d` lines. The counter keeps HOME in its environment, so BASE and TREE read under the same host, as the errata says.
- `grep -lE '^recheck:.*test -d ~/Projects/' corpus/knowledge/*.md | wc -l` prints 23 (base), 21 (T1), 23 (T2), 21 (T12). This matches the claim's plain-check targets.

## 3. Controls under v1.1 (kill rule: any control at 7/7 fails)

`python3 <lane>/.ufo/waves/round-46/controls/freeze-controls.py --lane <lane> --base 914ca0b6… --work <scratch>/controls-work`, run with the lane's v1.1 counters. The tail is `controls total=9 red=9 green=0` (exit 0). Every control stays red. The readings differ from the frozen `freeze-controls.txt`, which still records v1:

| control | frozen v1 (`freeze-controls.txt`) | v1.1 now |
|---|---|---|
| c1 do-nothing | 1/7 | 1/7 |
| c1 marker-only | 3/7 | 2/7 |
| c1 fabricated-anchors | 0/7 | 0/7 |
| c1 single-anchor-file | 0/7 | 0/7 |
| c1 gutted-entry | 6/7 | 0/7 |
| c2 do-nothing | 1/7 | 1/7 |
| c2 junk-row | 4/7 | 3/7 |
| c2 fabricated-quote | 4/7 | 3/7 |
| c2 uncited-filler | 5/7 | 4/7 |

The control file was not regenerated for v1.1. It is a stale record, not a failing one. The errata lists the counter changes but not these control readings.

## 4. Errata check (v1 vs v1.1, both on the tip tree)
- v1 C2 on T12: `c2-gate fixed=6/7 exit=1`, G6 red (§1).
- v1 C1 on T12: `c1-gate fixed=7/7 exit=0`. C1 v1 was not broken by the integration, so v1.1's C1 changes are hardening, not a repair of a C1 break. That is consistent with the errata's table.

## 5. Verdict and limitations

Verdict HOLDS: C1 reads 7/7 alone (T1), C2 reads 7/7 alone (T2), and both read 7/7 together (T12 and the tip). Do-nothing reads 1/7 on both. The couplings in §2 are one-way or measurement-level, and none moves a reading from 7/7 on the frozen rules. Two need action before the lane closes:
1. Recheck-audit reads the live lane for cd-prefixed lines (§2d). The plain numbers the claims cite are valid only at the tip. A tree-rooted audit needs the cd stripped, as the C1 counter does.
2. The plain check discards the audit exit code and the `missing=` line (§2b).

Limitations:
- Scratch trees were built from `git archive`, not from a live checkout. Harness files (selftests, landing gate, plain-measure) were not copied into T1/T2/T12, since they are not claim files. The tip export was run as a separate tree.
- The C1 anchor-closure claim (§2c) rests on code reading (`r46-c1-gate.py:243-245`) and was not exercised with a mutant.
- The wave-1 comparison in §2d is indicative only; the wave-1 tree was not rebuilt.
- score-gap.py was not run.
- Host-dependent: `~/Projects/ufo-fsd-alpha` exists here, and that affects the `test -d` gated count.
- The census gate (C2 G7) reads a fleet-root script; I ran it read-only.
- The frontier semantic checks (decision rule, row content, quote overreach) are out of this seat's scope. The counters grade only structure and located quotes.
- All numbers are single runs on this host, 2026-10-28. No commit, push, or index change.
