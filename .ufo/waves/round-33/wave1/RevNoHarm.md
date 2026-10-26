# RevNoHarm — round-33 wave-1 no-harm verification receipt

Seat: RevNoHarm (reviewer, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; claims freeze `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`.
HEAD at first command: `a6a502351bb90c8cd6d9b8f45f55109b7848e0d1`; HEAD at last command: `53bfa59ff3fa578818e7e5db04fe60e80ed1eb6f` (L1 committed mid-run: ready marker + C1 erratum 1; working bytes of SKILL.md/PROVINCE.md unchanged across it, see hashes).
Scope of this receipt: no-harm of `SKILL.md` and `PROVINCE.md` vs base via density.py, anchorcheck.py, recheck-audit.py, and git diff. No installs were performed (bound 5 n/a; no pacman run).

## 1. Quiescence of the bytes under test (bound 6)

    date +%s.%N                      # t0 = 1792988262.492585761
    sha256sum SKILL.md PROVINCE.md   # t0 hashes
    817636048968caf9801f3bdd22c8b8970f1014fc5a8192c49010e8328c4088b7  SKILL.md
    b42e5fbbbcdd7332ea971d8f9f0500965cc22f485e7766536c488a7e31a96076  PROVINCE.md

    git show 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4:SKILL.md > $S/SKILL.base.md
    git show 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4:PROVINCE.md > $S/PROVINCE.base.md
    wc -c SKILL.md PROVINCE.md $S/SKILL.base.md $S/PROVINCE.base.md
      96028 SKILL.md   96028 $S/SKILL.base.md   4007 PROVINCE.md   4007 $S/PROVINCE.base.md
    cmp SKILL.md $S/SKILL.base.md       && echo SKILL-identical-to-base
    cmp PROVINCE.md $S/PROVINCE.base.md && echo PROVINCE-identical-to-base
    -> SKILL-identical-to-base
    -> PROVINCE-identical-to-base

    date +%s.%N                      # t1 = 1792988445.906182680 (183 s after t0)
    sha256sum SKILL.md PROVINCE.md > hashes-t1.txt; diff hashes-t0.txt hashes-t1.txt
    -> BYTES-QUIESCENT-T0-T1
    git status --porcelain -- SKILL.md PROVINCE.md   # empty output, exit 0

All instrument runs below ran on those quiescent bytes; at verification time the
working SKILL.md and PROVINCE.md are byte-identical to base (no seat append landed yet).

## 2. density.py on current SKILL.md (label r33-rev)

    python3 corpus/instruments/density.py SKILL.md --label r33-rev ; echo exit=$?
    -> exit=0

    # Density census — r33-rev (1071 lines, 24 blocks)
    # ev = path-cites + concrete-tbl-rows + numerics + signatures; dens = ev*100/nb

    | # | block | lines | nb | cites | tbl | num | sig | ev | dens |
    |---|---|---:|---:|---:|---:|---:|---:|---:|---:|
    | 1 | Pipeline (observed, not invented) | 18 | 15 | 1 | 0 | 0 | 1 | 2 | 13.3 |
    | 2 | Program-rule checklist (step 1 of any mission) | 70 | 65 | 22 | 0 | 44 | 0 | 66 | 101.5 |
    | 3 | Policy access playbook (fleet-learned) | 10 | 8 | 24 | 5 | 8 | 0 | 37 | 462.5 |
    | 4 | Finding-triage decision table | 37 | 32 | 24 | 7 | 15 | 4 | 50 | 156.2 |
    | 5 | Intake surface — the map is decorative, ingestion is hidden | 51 | 47 | 15 | 0 | 30 | 4 | 49 | 104.3 |
    | 6 | Mission ledger & audit store | 27 | 24 | 21 | 0 | 16 | 6 | 43 | 179.2 |
    | 7 | Mission control plane | 28 | 26 | 17 | 0 | 14 | 2 | 33 | 126.9 |
    | 8 | UFO runtime workspaces — the untracked `.ufo/` layer + `.omp/` | 42 | 38 | 25 | 0 | 30 | 4 | 59 | 155.3 |
    | 9 | Ops integrity layer — invariants, intake, finalize | 130 | 122 | 103 | 0 | 20 | 14 | 137 | 112.3 |
    | 10 | VDP disclosure packages (sibling format) | 26 | 23 | 18 | 0 | 8 | 1 | 27 | 117.4 |
    | 11 | Retirement lane — autopsies & the detail regex | 62 | 57 | 30 | 0 | 19 | 4 | 53 | 93.0 |
    | 12 | Evidence-package anatomy | 28 | 24 | 20 | 6 | 13 | 3 | 42 | 175.0 |
    | 13 | Disclosure anti-patterns (all observed in fleet wrap review) | 115 | 110 | 68 | 10 | 47 | 3 | 128 | 116.4 |
    | 14 | Claim-hardening wave — the defect layer above the gates | 35 | 30 | 22 | 10 | 21 | 9 | 62 | 206.7 |
    | 15 | Submitted-state registry — the do-not-refile set | 50 | 46 | 25 | 0 | 20 | 5 | 50 | 108.7 |
    | 16 | Operator queue — live audit | 40 | 36 | 18 | 0 | 16 | 1 | 35 | 97.2 |
    | 17 | Triage economics | 172 | 156 | 126 | 18 | 46 | 15 | 205 | 131.4 |
    | 18 | Gates & probes registry | 9 | 6 | 1 | 2 | 4 | 7 | 14 | 233.3 |
    | 19 | Cited paths (verified 2026-09-28 …) [long block-title line, byte-identical to base] |
    | 20 | Frontier decision table (round 22) | 13 | 10 | 10 | 5 | 3 | 2 | 20 | 200.0 |
    | 21 | Round-29 Gates & probes registry addition (appended 2026-10-25) | 8 | 5 | 1 | 1 | 5 | 7 | 14 | 280.0 |
    | 22 | Round-29 frontier note (appended 2026-10-25) | 5 | 2 | 2 | 0 | 1 | 1 | 4 | 200.0 |
    | 23 | Round-30 Gates & probes registry addition (appended 2026-10-25) | 10 | 6 | 3 | 2 | 6 | 4 | 15 | 250.0 |
    | 24 | Round-31 Gates & probes registry addition (appended 2026-10-25) | 12 | 8 | 27 | 2 | 18 | 6 | 53 | 662.5 |
    | | **mean dens** | | | | | | | | **191.5** |

    Total path-citation instances: 689 across 24 blocks.

## 3. Pre-existing rows byte-identical to base (diff vs `git show {BASE}:SKILL.md` with the instrument)

Two independent derivations of base bytes, both diffed against the r33-rev run above
(label normalized):

    python3 corpus/instruments/density.py $S/SKILL.base.md --label r33-base > density.base.txt
    diff <(sed 's/r33-rev/LABEL/' density.current.txt) <(sed 's/r33-base/LABEL/' density.base.txt)
    -> (empty diff) DENSITY-TABLES-IDENTICAL

    git clone --shared <lane> $S/baseclone && git -C $S/baseclone checkout -q --detach 690b69dae23a…
    git -C $S/baseclone rev-parse HEAD -> 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4
    sha256sum $S/baseclone/SKILL.md -> 817636048968caf9801f3bdd22c8b8970f1014fc5a8192c49010e8328c4088b7 (== working file)
    python3 corpus/instruments/density.py $S/baseclone/SKILL.md --label r33-baseclone > density.baseclone.txt
    diff <(sed 's/r33-rev/LABEL/' density.current.txt) <(sed 's/r33-baseclone/LABEL/' density.baseclone.txt)
    -> (empty diff) DENSITY-TABLES-IDENTICAL-CLONE

All 24 block rows, the mean row, and the totals line are byte-identical base→current.

## 4. anchorcheck.py — verdict classes identical

Current working tree:

    python3 corpus/instruments/anchorcheck.py SKILL.md ; echo exit=$?
    -> exit=0
    == SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
    per-line classes: OK=7, LOST-RECORDED=306 ([lost-tree]=104, [lost-base]=202)

True base tree (same instrument, run against the shared clone checked out at base,
cwd = clone root):

    /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/anchorcheck.py $S/baseclone/SKILL.md
    -> exit=0
    == FILE: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0

    sed -E 's#^== .*(SKILL\.md):#== FILE:#' anchor.current.txt > anchor.current.norm
    sed -E 's#^== .*(SKILL\.md):#== FILE:#' anchor.baseclone.txt > anchor.baseclone.norm
    diff anchor.current.norm anchor.baseclone.norm
    -> (empty diff) ANCHOR-OUTPUTS-IDENTICAL

Verdict-class vector identical base→current: 7 in-range/0 bad, 7 distinct anchors,
LOST-RECORDED=306, PIN-BROKEN=0, ORIGIN=0, OUTSIDE-BASE=0, BASE-ABSENT=0; all 306
LOST-RECORDED lines and 7 OK lines match line-for-line (zero-diff after normalizing
only the checked-file path in the summary line).

Methodology footnote: a first attempt ran anchorcheck on the `git show` extract
placed in scratch — invalid (out-of-lane-root path): `BASE-ABSENT=7`, exit 1,
because in-lane cites cannot resolve outside the tree. That run is retained in
scratch only as `anchor.scratch-probe.INVALID.txt` and is NOT evidence; the clone
run above supersedes it.

## 5. recheck-audit.py --quiet

    python3 corpus/instruments/recheck-audit.py --quiet ; echo exit=$?
    -> exit=0
    strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
    executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
    lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
    expect=present expected=44 missing=0 unexpected=0 exit=0

## 6. Additions-only diff vs base

    git diff 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 -- SKILL.md PROVINCE.md | wc -c
    -> 0
    git diff --numstat 690b69d… -- SKILL.md PROVINCE.md
    -> (no rows; zero additions, zero deletions)
    git diff 690b69d… -- SKILL.md PROVINCE.md | grep -c '^-[^-]'
    -> 0

Re-proven after the L1's mid-run commit (HEAD 53bfa59): numstat empty, patch 0 bytes.
Additions-only with 0 deletions holds trivially because both files are currently
byte-identical to base (see §1).

## 7. Scoped findings

No defect found in scope: all three instruments pass on quiescent bytes; every
density block row and the anchor verdict-class vector are identical to base; the
SKILL.md/PROVINCE.md diff vs base is additions-only with 0 deletions (currently
empty).

## 8. Residual risk / verification gaps

- R1: ScribeSkillGate (SKILL.md, R6 lines) and ScribeProvince (PROVINCE.md) appends
  had NOT landed at verification time — working bytes equal base, so the identity
  checks are trivially satisfied. If those appends land after this receipt, the
  additions-only/append-only property is the owners' bound; a post-append re-run of
  §2–§4 would be needed for a fresh attestation (not re-run here: bytes were
  quiescent base-identical for the whole window t0→t1).
- R2: HEAD advanced a6a5023 → 53bfa59 mid-run (L1 commit). Working bytes of both
  files were unchanged across it (hashes t0=t1, both == base bytes); diff re-proven
  at 53bfa59.
- R3: none. No instrument wrote into the lane; scratch
  `/fast/scratch/hyaku/kasegi-r33/RevNoHarm/` (incl. the single `git clone --shared`)
  is removed before yield per bound 12.
