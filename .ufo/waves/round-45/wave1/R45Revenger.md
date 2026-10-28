VERDICT: BROKEN

Scope: reverse-engineered intent of routed defects R1-R5 (`corpus/lessons/round-44-verifier-spotcheck.md` §6 items 1-5, with §2-§4 for context) against each limb of the frozen C1 counter `corpus/instruments/r45-routed-defects.py` (sha256 `82004c700decbc3453ba…`, read at the lane tree, frozen in commit 8cf62c8). Read-only. Only this Report was written in the lane; scratch was `$HYAKU_SCRATCH/kasegi-r45/R45Revenger/` (removed on exit).

Bottom line: the frozen counter is red on the do-nothing base (5/5 unresolved, as the freeze claims). But it is not a falsifiable measure of the five defects. A synthetic tree that contains no repair of the defects, only stub tool files and prose or receipt text in the places the limbs look, grades `fixed=5 unresolved=0 exit=0` (fixture ALL, §C-2). The frozen controls do not include such a tree, so the C1 kill rule cannot fire on it.

## 0. Method and evidence hygiene

- Base export: `$S/base` = copy of `/fast/scratch/hyaku/kasegi-r45/L1/pure`. Verified byte-identical to `git show dc5bb8c:<path>` for `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/lessons/round-44.md`, `SKILL.md`, `corpus/instruments/r44-routed-defects.py`, `corpus/instruments/source-recheck.py`, `.ufo/waves/round-44/controls/final-attempt3.txt` (sha256 prefixes match).
- Counter run from the lane path (`python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r45-routed-defects.py --root <tree> --baseline $S/base`); the lane was not written.
- Fixtures are synthetic trees under scratch. Each is `$S/base` plus the named edit; `fx/ALL` is the union of the proxy edits. Fixture contents are described below; they are not committed and are not repairs.
- Claims-file sha: `sha256(.ufo/waves/round-45/claims.json)` = `bbe40503281c90eb9d70f469d7bac10125b285758ca9675be9894ce6c12c6206`, equal to `claims-sha256` in `.ufo/waves/round-45/freeze.txt`.

## 1. Do-nothing control (discrimination baseline)

Command: `python3 <counter> --root $S/base --baseline $S/base`
Output (verbatim):
```
limb R1 fixed=0 read=row-S072=absent
limb R2 fixed=0 read=quality-not-append-only-or-unchanged
limb R3 fixed=0 read=selftest-rc=2-tokens=None
limb R4 fixed=0 read=freeze-check-absent
limb R5 fixed=0 read=refiled-absent
routed-defects total=5 fixed=0 unresolved=5 exit=1
```
Matches the claim's `expect_before`. Verdict on this control: holds (red).

Frozen control set re-run (`python3 .ufo/waves/round-45/controls/freeze-controls.py --base-export $S/base --lane <lane> --work $S/ctl`), C1 lines verbatim:
```
control do-nothing-base counter=C1 routed-defects total=5 fixed=0 unresolved=5 exit=1 expect=RED got=RED
control c1-marker-only counter=C1 routed-defects total=5 fixed=0 unresolved=5 exit=1 expect=RED got=RED
controls total=5 red=5 green=0
```

## 2. Per-defect intent vs. predicate

### R1 — item 1: S070 reject reason (limb code lines 99-140)

Spot-check (lesson §6 line 79): "Append (never rewrite) a correction to `corpus/SOURCES.md` S070 and `round-44.md` `## Gate`: … the true reason is 'overview, no program-specific rule beyond S069 Q5'. Replace the vacuous flip condition with a checkable one (e.g. the directory gains a rule paragraph not present in a program's own rules page)."

Spot-check §4 (lesson line 66) on the flip: "the flip condition ('a readable, dated copy … that carries a quotable rule text') is already satisfied." This is the sentence that makes the flip "vacuous" in the spot-check's sense.

Limb code vs. defect:
- line 110 `if not re.search(r"flip:\s*\S", teaches):` ↔ "replace the vacuous flip with a checkable one". Accepts any non-empty text after `flip:`.
- line 114 `if not re.search(r"\breadable\b", teaches):` ↔ the reason's premise. Sign-blind.
- line 118 `if old is None or old != new:` (S070 row must be byte-identical to base) ↔ "append a correction to S070". The literal action fails this limb.
- lines 106 and 112 test the `supersedes S070 —` prefix and the `10029` token; nothing tests the reason text "overview, no program-specific rule beyond S069 Q5", nor any reference to S069.
- line 136 requires an appended line starting `Correction (round 45` in round-44.md; location is end-of-file, not the `## Gate` section (low; proxy).

Tree that satisfies R1 and leaves the defect standing (fixture F1, F1b, F1c, F1d): a new S072 row plus the appended correction, S070 row untouched.
- S070 row in F1 (line 76) still reads "REJECTED: the page's accessible body is a JavaScript shell and its metadata is a directory welcome, not an operative program rule" — the wrong reason stays in the registry.
- round-44.md `## Gate` flip line (base line 131: "Flip condition: a readable, dated copy of the rules directory that carries a quotable rule text") is untouched; `grep -c 'Flip condition: a readable, dated copy' fx/F1/corpus/lessons/round-44.md` → `1`.
- F1 S072 teaches `supersedes S070 — overview body is readable, 10029 characters; flip: none` → `limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1`.
- F1d S072 teaches uses the lesson's own already-satisfied flip ("flip: a readable, dated copy of the rules directory that carries a quotable rule text") → `limb R1 fixed=1 …` (same read).
- F1b negated claim (`the body is not readable`) → `limb R1 fixed=1 …`.
- F1c replaces the tree's `corpus/instruments/source-recheck.py` with an always-OK stub (prints `S072:sha256 OK`, `S072:Q1 OK`, `S072:Q2 OK`) → `limb R1 fixed=1 …`. Line 123 runs the tree's own copy, not the baseline's.
- F6 (literal item-1 action: correction appended into the S070 row) → `limb R1 fixed=0 read=S070-row-changed-or-baseline-absent`. The counter rejects the action the spot-check named.

Size token: the counter does not bind `10029` to the pinned bytes. `corpus/source-snapshots/round-45/S072.txt` is 10032 bytes, 10030 code points, ending `r>\n\n`; the token is consistent with one reading (code points minus one terminal LF), but no limb computes it.

Verdict R1: proxy. It tests an S072 row plus a lesson line, not that the reason was corrected, the vacuous flip was replaced, or the S070 registry row is no longer wrong. The frozen claim (claims.json `after`) defines R1 the same narrow way, so the predicate matches the claim, not the spot-check.

### R2 — item 2: QUALITY.md criteria (limb code lines 143-179)

Spot-check (line 80): "Add grounded criteria citing `round-44.md` for the classes no criterion caught — 'frozen counter must be replayed on a do-nothing control before data' (M44-3/M44-8), 'presence-only predicates accept denials and fabricated trees' (M44-4/M44-7/M44-10), 'capture method used for admit must also be used for reject'."

Limb code:
- lines 143-147 `CLASS_RX` needles are keyword sets: R47 `do-nothing`+`before data`; R48 `presence-only`; R49 `capture method`+`reject`.
- line 167 `if "corpus/lessons/round-44.md" not in ground:` — substring of the grounding cell; M44 IDs not checked; the lesson's content is not read.
- lines 172-177 `enforced-by:` path checked only for existence (`os.path.exists`). It is not checked that the path enforces the class.

Tree that satisfies R2 and leaves the defect standing (fixture F2): three criteria rows, each naming the keywords, enforced-by `corpus/QUALITY.md` (exists, enforces nothing). Output: `limb R2 fixed=1 read=criteria=3`.

The frozen control's marker-only tree is red on R2 only because its enforced-by path `corpus/instruments/nothing.py` does not exist (freeze-controls.py lines 61-63). Change that one path to an existing file and the same marker-only text goes green.

Verdict R2: proxy (keyword presence and path existence). Also self-referential: the counter's own R2-R5 checks are presence-only, which is the class R48 names (M44-10).

### R3 — item 3: r44-frontier-count.py registration (limb code lines 187-207)

Spot-check (line 81): "register it as a probe or give it a selftest and a registry row at its home (`SKILL.md` Gates & probes …)".

Placement: the limb appends a `## Round-45 Gates & probes registry addition` section (line 197). This matches the lane's existing convention (base `SKILL.md` lines 1094-1130 are appended `Round-NN … registry addition` sections, each an 8-column table `| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |`). The placement is convention-consistent, not a proxy. Not a finding.

Gaps:
- line 191 `if rc != 0 or tk is None or tk[1] != 0 or tk[0] < 8:` trusts the tree's own printed token. The base file has no selftest (argparse has only `--root`, `--expect`, `--ids`; base lines 68-71).
- line 202 `len(rows[0].strip().strip("|").split("|")) != 8` counts cells, not content.

Tree that satisfies R3 and leaves the defect standing (fixture F3): `r44-frontier-count.py` replaced by a stub that prints `selftest cases=8 failures=0` and exits 0; SKILL.md section with placeholder rows `| r44-frontier-count.py | 1 | 2 | 3 | 4 | 5 | 6 | 7 |`; README row. Output: `limb R3 fixed=1 read=selftest-cases=8`.

Verdict R3: proxy (token trust plus cell count).

### R4 — item 4: freeze hygiene (limb code lines 210-222)

Spot-check (line 82): "A frozen counter string must be run on the base before freeze (the C2 string read 0/0); the round-45 planned gates already say so — hold the lane to it."

Limb: runs `corpus/instruments/freeze-check.py --selftest` (tree-supplied) and `--claims <tree>/.ufo/waves/round-45/claims.json --base <base>`; requires `freeze-check claims=2 base_ok=2`.

Gaps:
- line 218 reads claims.json from the tree under test. No comparison with the frozen `claims-sha256` (`bbe40503…`, freeze.txt). A tree can change the claims and the limb reads the changed bytes.
- `freeze-check.py` is absent from base and from `git ls-files` at HEAD; it must be built. Any stub that prints the two tokens passes.

Tree that satisfies R4 and leaves the defect standing (fixture F4): `freeze-check.py` stub printing `selftest cases=6 failures=0` and `freeze-check claims=2 base_ok=2`; claims.json copied from freeze commit 8cf62c8. Output: `limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2`.

Substance check (what the defect was about): the frozen C2 secondary string in claims.json (`r44-frontier-count.py --root {tree} --expect 27  # base: frontier rows=26 admitted=26 exit 1`) run on base gives `frontier rows=26 admitted=26` / `frontier expected=27 admitted=26 verdict=SHORT exit=1`, exit 1, matching its note. No limb runs that string; R4 only runs the (unbuilt) freeze-check replay.

Verdict R4: proxy (self-report token, tree-supplied claims, no pin check).

### R5 — item 5: receipt wording (limb code lines 225-242)

Spot-check (line 83): "`controls/final-attempt3.txt` lists an argparse usage error followed by `exit=0` for the bare `--selftest` call; re-file the selftest invocation line without the failed call."

Base evidence (`git show dc5bb8c:.ufo/waves/round-44/controls/final-attempt3.txt`) contains `usage: r44-routed-defects.py …` / `r44-routed-defects.py: error: the following arguments are required: --root` / `exit=0` before the real selftest line.

Limb: lines 230-237 check for no `usage:`/`error:` line (case-insensitive), `^selftest cases=20 failures=0`, `exit=0`, the invocation `--root \S+ --selftest --work \S+`, and that the original is byte-identical (lines 238-241). It does not check that the refiled file was produced by a run or is derived from the original.

Existing artifact, checked:
- `.ufo/waves/round-44/controls/final-attempt3-refiled.txt` exists on disk, untracked: `git cat-file -e HEAD:.ufo/waves/round-44/controls/final-attempt3-refiled.txt` → `fatal: path '.ufo/waves/round-44/controls/final-attempt3-refiled.txt' exists on disk, but not in 'HEAD'`; `git status --porcelain` → `?? .ufo/waves/round-44/controls/final-attempt3-refiled.txt`. So the committed lane tree cannot satisfy R5 until it is committed.
- Content re-run: exported `c950fa3` to scratch and ran `python3 tip/corpus/instruments/r44-routed-defects.py --root $S/tip --selftest --work $S/w44` → `selftest cases=20 failures=0`, `exit=0`; `diff` of its `^selftest` lines against the refiled file's `^selftest` lines → identical (20 case lines). The refiled content is genuine.

Tree that satisfies R5 and leaves the defect standing (fixture F5): a three-line receipt typed by hand (`$ python3 … --root <tip> --selftest --work <scratch>`, `selftest cases=20 failures=0`, `exit=0`) with no run. Output: `limb R5 fixed=1 read=refiled=ok original=unchanged`.

Verdict R5: proxy for the run (text only); the present file is genuine but untracked.

## 3. Cross-cutting findings

C-1 Tree-supplied instruments are executed and their stdout trusted. Lines 123 (`source-recheck.py`), 188 (`r44-frontier-count.py`), 211/214 (`freeze-check.py`) run files from the tree under test, and lines 136, 183, 191, 216, 220, 232 believe the printed token. Fixtures F1c, F3, F4 show this.

C-2 The frozen control set cannot falsify C1. `freeze-controls.py` builds exactly one C1 control (marker-only), and it is red for reasons a one-token change removes (§2 R2, R4). Fixture ALL — union of the proxies: S072 row with `flip: none` and no S070 change (F1), F2 criteria, F3 stub + placeholder rows, F4 stub, F5 hand-typed receipt:
```
limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
limb R2 fixed=1 read=criteria=3
limb R3 fixed=1 read=selftest-cases=8
limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2
limb R5 fixed=1 read=refiled=ok original=unchanged
routed-defects total=5 fixed=5 unresolved=0 exit=0
```
exit 0. The claim's kill rule ("C1 fails if … any control … grades fixed=5") would fire on this tree if it were a control. Nothing in the freeze set would catch it. This repeats the M44-10 failure class (`lesson round-44.md` line 189: "presence-only predicates accepted denials, stubs and rewrites").

C-3 Limb wording versus the spot-check. The counter implements the claim's narrower R1 wording (new row + lesson line), not the spot-check's "append to S070 and replace the vacuous flip". The literal S070 append fails (F6); the vacuous flip passes (F1d).

## 4. Limb-by-limb: where a tree satisfies the limb and the defect stands

| Limb | Tree that passes | Defect left standing |
|---|---|---|
| R1 | S072 row with `flip: none` or the lesson's satisfied flip; S070 row unchanged; `not readable`; stubbed source-recheck | S070 row still says "JavaScript shell"; round-44 Gate flip (line 131) unchanged; reason ("no rule beyond S069 Q5") never stated |
| R2 | three criteria rows, enforced-by an existing non-enforcing file (`corpus/QUALITY.md`) | criteria not operative; M44 IDs not referenced by the counter |
| R3 | stub `r44-frontier-count.py` printing constant token; placeholder 8-cell rows; README row | no working selftest, no registry content |
| R4 | stub `freeze-check.py` printing the two tokens; claims read from tree | frozen claims not pinned; no run of the frozen C2 string on base |
| R5 | hand-typed 3-line receipt | no run; present artifact untracked |

## 5. Limitations

- Freeze-check.py, a real r44-frontier-count selftest, and any repair are not built; stub-based fixtures are constructed to probe the predicates, not to represent a builder's output.
- Only C1 was reverse-engineered. The C2 counter (`r45-c2-gate.py`) and F27 were not examined beyond the one frontier-count string run above.
- "Vacuous" in R1 is the spot-check's own characterisation (lesson line 66); I did not re-fetch S070/S072 from the network.
- The 10029 size token is not checked by any limb; I did not determine whether the spot-check's "10 029-char body" equals the snapshot's characters under a fixed convention.
- Limb-level R5 "genuine content" depends on the re-run at `c950fa3`; the round-44 receipt's claimed tip export is `c950fa3`, and I used it as stated.
- No commit, push, index or git mutation was performed. The counter and freeze controls were run as read-only scripts; the controls wrote only under scratch.
- Scratch `$S` is removed on exit.
