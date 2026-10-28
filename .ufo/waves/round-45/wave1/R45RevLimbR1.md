VERDICT: BROKEN

# R45RevLimbR1 — C1 limb attack on `limb_r1` (corpus/instruments/r45-routed-defects.py, def at line 99)

Attacked: limb R1 = routed defect S070 reject reason, spot-check `corpus/lessons/round-44-verifier-spotcheck.md` §6 item 1 (line 79: "Replace the vacuous flip condition with a checkable one"; "the true reason is 'overview, no program-specific rule beyond S069 Q5'"). Predicate sentence: counter docstring lines 10-15 ("a checkable `flip:` clause ... a sha-pinned snapshot with located quotes ... readable-body size token (10029 characters) ... S070 row byte-identical ... appended `Correction (round 45` line ... cites S072 and the size token"). Frozen claim: `.ufo/waves/round-45/claims.json` C1 `after`.

Counter used: `corpus/instruments/r45-routed-defects.py`, sha256 `82004c700decbc34…` (copied to scratch `tool/`; `git -C <lane> ls-files --error-unmatch corpus/instruments/r45-routed-defects.py` prints the path, i.e. tracked; the lane file was not modified by me). Baseline tree: copy of `/fast/scratch/hyaku/kasegi-r45/L1/pure` (`diff -rq pure base` empty). Round-45 snapshots copied from the lane's `corpus/source-snapshots/round-45/` (S072.txt sha256 `364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025`, equal to manifest pin).

## Finding 1 (BROKEN): a vacuous `flip:` plus a one-line stub correction reads fixed=1

Recipe (scratch tree `attack`; all edits are appends to the pure base copy plus the round-45 snapshot copy):
1. Append one 11-cell row to `corpus/SOURCES.md`:
   `| S072 | Google Bug Hunters REST article body (about-this-section) — … | docs | C | … | sha256 364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025; Q1 anchor 148 | supersedes S070 — readable body 10029 chars; flip: tbd | rejected | 2026-10-28 | 180d | — |`
2. Append one line to `corpus/lessons/round-44.md`:
   `Correction (round 45): S070 reject reason restated against S072 (readable body 10029 chars).`
3. `python3 tool/r45-routed-defects.py --root attack --baseline base`

Printed (verbatim):
```
limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
```
Do-nothing control (same counter, `--root base --baseline base`):
```
limb R1 fixed=0 read=row-S072=absent
```
The defect is still present: the `flip:` clause is `tbd`, so there is no checkable flip condition, and the true reason (no program-specific rule beyond S069 Q5) appears nowhere in the tree. The limb reads it as fixed because `limb_r1` tests `re.search(r"flip:\s*\S", teaches)` (line 110): `tbd` is a non-space character.

## Finding 2: the limb is blind to the reason and to the flip's content (shown by discrimination)

Nine constructions were run through the same counter, each on a copy of the base. The R1 line of each:

| construction (teaches / lesson line / snapshot) | printed R1 line |
|---|---|
| do-nothing base (no S072 row) | `limb R1 fixed=0 read=row-S072=absent` |
| marker-only: `supersedes S070 — TODO`, no lesson | `limb R1 fixed=0 read=flip-absent` |
| marker+tokens: `supersedes S070 — TODO readable body 10029 chars flip: TODO`, no lesson | `limb R1 fixed=0 read=lesson-correction-absent` |
| attack without lesson line (`… flip: tbd`) | `limb R1 fixed=0 read=lesson-correction-absent` |
| attack without `flip:` (`… readable body 10029 chars`) | `limb R1 fixed=0 read=flip-absent` |
| attack without size token (`… readable body; flip: tbd`) | `limb R1 fixed=0 read=size-token-absent` |
| **attack (vacuous flip + stub lesson line)** | **`limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`** |
| **honest flip (true reason + checkable flip "the directory gains a rule paragraph absent from a program rules page")** | **`limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`** |
| **fabricated snapshot (S072.txt extra fabricated program-rule line; manifest sha re-pinned; anchor re-pinned)** | **`limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`** |
| S070 row rewritten in place (reason changed) | `limb R1 fixed=0 read=S070-row-changed-or-baseline-absent` |

Reading: the limb discriminates on token presence and on append-only placement (the marker, size, flip-absent, lesson-absent, and S070-rewrite controls go red, as the freeze controls require), but it does not discriminate on the content of the correction. Both the vacuous and the honest variant read fixed=1.

## Finding 3: the frozen predicate sentence promises a check the code does not make

Docstring line 110-111 promises "a checkable `flip:` clause"; the code checks only `flip:\s*\S`. No code path checks that the flip is checkable, names a condition, or differs from the placeholder. This is the defect itself: the spot-check item asked for the vacuous flip to be replaced, and the counter accepts the vacuous form.

## Finding 4: the recheck binds bytes to the manifest, not to upstream (fabrication route)

`fabricated snapshot` tree: `source-recheck.py --manifest <tree>/…/manifest.json --source S072` on that tree prints exit 0 with `S072:sha256 OK` and two `OK` quote lines, because the manifest sha was re-pinned in the same tree. `limb_r1` line 129 checks the snapshot hash against the row anchor, which is also in the same tree. Nothing in the limb ties S072.txt to the live article. The source-recheck docstring says the same ("verifies captured bytes, not current upstream availability"). The limb's "readable body 10029 chars" token is also never compared with the capture's length (S072.txt is 10032 bytes; the token is free text).

## Finding 5: a minimal tightening closes Finding 1 in scratch (repair candidate, not applied to the lane)

`tool2/r45-routed-defects.py` replaces line 110 with: `m = re.search(r"flip:\s*(.+)", teaches)`; fail `flip-vacuous` if `m` is absent, if the text is `tbd|todo|n/a|x|-+|.+`, or if it has fewer than 4 words. Run:
- attack: `limb R1 fixed=0 read=flip-vacuous`
- marker-only: `limb R1 fixed=0 read=flip-vacuous`
- honest flip: `limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`

Limitation: this is still a token heuristic. A four-word stub ("flip: to be decided by a reviewer") passes. Per the C1 kill rule, a change of this kind is a counter erratum, not a new rule, and must be logged as one before any seat scores again. Not applied; the lane file is unchanged.

## Constructions tried (≥5 distinct, as the assignment requires)

Nine above: marker-only, marker+tokens, no-lesson, no-flip, no-size, vacuous-flip (attack), honest-flip, fabricated-snapshot, S070 in-place rewrite. Result: the vacuous flip, the honest flip and the fabricated snapshot all read fixed=1; the rest read fixed=0 with the reason named.

## Limitations

- Attacked the R1 limb only. Limbs R2-R5 were not attacked; the full counter on my attack tree printed `routed-defects total=5 fixed=1 unresolved=4 exit=1` (R2-R5 red because those trees lack their artifacts). The C1 kill rule is about the whole counter; this report is a limb-level hole.
- Scratch trees are built from the pure export plus the lane's round-45 snapshot files. The counter was run from a copy of the lane's current file; I did not run it from the lane tree in place, and did not run the lane's freeze controls (`controls/freeze-controls.txt` cites `c1-marker-only`, whose tree I did not have; my marker-only tree is my own construction).
- No network access was used; no live upstream was checked (corpus is documentation only). "readable body 10029 chars" is not verified against upstream.
- Repair candidate (Finding 5) was tested only against the nine trees above, not against the round-45 lane tree.
- Scratch directory removed on exit; no git/jj mutation; no commits; lane tree not modified (`git status --porcelain` and `git rev-parse HEAD` were the only git calls; they are read-only).
