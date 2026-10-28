# R44Critic12 — C1/C2 causality and separability

- seat: R44Critic12 (critic, read-only, leaf). Item: *Challenge claim causality and whether C1/C2 remain separable under likely edits.*
- basis: lane `kasegi-shokunin`, HEAD `6631401` ("round-44: freeze claims and validated wave"), frozen base named by the control `5ab3a60` (`controls/do-nothing.txt:2`); HEAD is a descendant of that base and adds only `.ufo/waves/round-44/*` (verified `git merge-base --is-ancestor 5ab3a60 HEAD` → true; `git diff --stat 5ab3a60 HEAD` → six round-44 wave files, 0 corpus lines).
- method: read-only re-derivation on committed bytes (`git show`/`git archive`/`git ls-tree`/`git status`/`sha256sum`) plus scratch-tree replays of the frozen counters, the drafted C1 counter, and the two capture/audit instruments. No lane file was edited by this seat; no git/jj/index mutation; no commit.
- measured window: `2026-10-28T18:58Z`–`19:14Z`. Every live number below is timestamped; the lane tree moved under this seat (see F5/F8).

Verdict in one line: **C1's kill rule is falsified by the drafted counter it names (F4); C2's kill rule survives but its frozen `counter` field is inert and tree-scoped (F1–F3); the two claims are separable in predicates and files (F7) but not in measurement basis or obligation scope.**

---

## F1 — C2's frozen counter cannot return the number it asserts (defect, decisive)

`claims.json:23` freezes:

```
grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md; ...
```

`corpus/README.md` rows carry six cells (`| F01 | topic | status | entry | sources | next |`), so the status cell is never adjacent to the id cell.

```
$ grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md
0
$ git archive HEAD | tar -x -C $S/head; grep -cE '^\| F[0-9]+ \| admitted \|' $S/head/corpus/README.md
0
$ grep -cE '^\| F[0-9]+ \| .* \| admitted \|' corpus/README.md      # the control's variant
25     (at HEAD export) / 26 (live tree)
```

The frozen counter prints `0` at the base and `0` at the live after-state. The before-value `25` in `claims.json:20` is reproducible **only** by the different regex in `controls/do-nothing.txt:10`. So the claim's own counter did not produce the claim's own before-state; as written it can never move.

Impacted axis: `coverage` (C2 counter). Smallest correction: use the regex that produced the control (`^\|[[:space:]]*F[0-9]+.*\|[[:space:]]*admitted[[:space:]]*\|`) or count ids only (`^\|[[:space:]]*F[0-9]+\b`), and keep the three commands identical in claims and control.

## F2 — C2's counters read the working tree, so the frozen before-state is not reproducible and a do-nothing replay already reaches the after-state (defect, decisive)

The three frozen commands (`claims.json:23`, `do-nothing.txt:10-12`) are path-relative and read the **working tree**, while C1's counter (`claims.json:14`) is specified as `--root <lane-export> --baseline <frozen-base>` — i.e. committed bytes. Same tree, two bases.

```
$ date -u +%FT%TZ
2026-10-28T18:58:33Z                      # 13-14 min after the 15:44/15:45 freeze
$ grep -cE '^\|[[:space:]]*F[0-9]+' corpus/README.md ; \
  grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md ; \
  find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l
26
70
63                                        # after-state values, zero commits

$ git archive HEAD | tar -x -C $S/head    # committed basis
25 / 68 / 62                              # before-state values
```

Consequences, both against C2's own text:

1. `claims.json:20`'s before-state (`25/68/62`) is no longer reproducible from the lane at the revision under test; the delta `25→26, 68→70, 62→63` is an export-vs-tree basis artifact, not a round effect. The only remaining red-before for C2 is `git archive 5ab3a60`, a *different* basis from the after-measurement.
2. `claims.json:22`'s kill rule — "A do-nothing replay cannot reach F26 or the new sourced entry" — is false **for the counters it names**: a replay that commits nothing reports `F26` present and `63` knowledge entries. The reach is uncommitted (see F8: `corpus/knowledge/…-boundary.md` is untracked; `corpus/README.md` and `corpus/SOURCES.md` are ` M`), so the discrimination survives only if the replay is pinned to a committed export — which the claim does not say.

Impacted axis: `coverage` (C2 counter, before/after pair). Smallest correction: state the basis in the counter (`git archive <rev> | tar -x -C <dir>` then the three greps with `--root`), and require the after-measurement on a committed export, exactly as C1 already does.

## F3 — C2's counters do not entail the after-state's "its captured source lands" (counterexample)

Counterexample built in scratch: HEAD export **plus** the four after-state artifacts that the counters read (`corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/<new>.md`, `corpus/instruments/knowledge-expected.txt`) and **minus** `corpus/source-snapshots/round-44/` — the most likely commit slip, because the capture is an untracked *directory* that a per-file `git add` omits.

```
$ grep -cE '^\|[[:space:]]*F[0-9]+' corpus/README.md ; \
  grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md ; \
  find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l
26
70
63                                        # full after-state on every frozen counter
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root … kasegi ; echo exit=$?
kasegi ok …/corpus/SOURCES.md
exit=0
$ python3 corpus/instruments/capture-binding-check.py --root .
AUDIT records=57 … snapshot_dirs=19 manifest_dirs=19 missing_manifest=0 … orphans=1
records=57 bound=57 unbound=0
exit=0                                    # live tree: records=58 → the capture is absent and the gate cannot see it
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-44/manifest.json --source S069
manifest UNAVAILABLE reason=missing
exit=2                                    # the only detector
```

So the capture-binding gate is **fail-open on a missing directory**: rule A only inspects `corpus/source-snapshots/*` dirs that exist, so dropping the whole round-44 snapshot lowers `records` 58→57 and still exits 0. The after-state conjunct "its captured source … lands" (`claims.json:21-22`) is therefore guarded by exactly one command — `source-recheck.py --manifest …/round-44/manifest.json` — which no frozen counter runs.

Impacted axis: `coverage` (evidence binding). Smallest correction: add the `source-recheck.py --manifest corpus/source-snapshots/round-44/manifest.json --source S069` probe (exit 0 required) to C2's after-state and to the kill rule; optionally give `capture-binding-check.py` a rule that a knowledge entry's `source:` id must resolve to a manifest record in the tree.

## F4 — C1's kill rule is falsified by the counter C1 names (defect, decisive)

`claims.json:13` — "If a do-nothing replay against the frozen base can report all 8 fixed … C1 fails." `claims.json:14` names `corpus/instruments/r44-routed-defects.py`, which did not exist at freeze (`git log --all -- …/r44-routed-defects.py` → 0 commits) and appeared untracked during wave 1. Digest under test: **`8a5a9c2bd6ac04b08c93e31c7dd9c228b4bd737c240e17f58191b7f303691ee6`** (16:14:24, 3874 B).

Two replays, both `--baseline $S/head` (= frozen base):

```
A. literal byte-identical replay (root == baseline):
   frozen_defects=8 fixed=0 unresolved=8 exit=1        # correct

B. no-repair token replay: base + eight assertion files, defective artifacts byte-identical:
   RD43-1 …=1  RD43-2 …=1  RD43-3 …=1  RD43-4 …=1
   RD43-5 …=1  RD43-6 …=1  RD43-7 …=1  RD43-8 …=1
   frozen_defects=8 fixed=8 unresolved=0 exit=0
```

The B tree performs **no repair of any defective artifact** (build commands in §Reproduction). Per-defect, with the current predicate source:

| defect (§6 line) | artifact the defect names | what the counter actually reads | state in tree B |
|---|---|---|---|
| RD43-1 (`:101`) | `SCORECARD.md`'s unbacked `closed=13/19`, superseded by six per-limb transcripts | `SCORECARD.md` contains `closed=13/19` followed by `Correction (round 43` **and** `superseded` | correction sentence names no transcript; **accepted** |
| RD43-3 (`:103`) | `corpus/lessons/round-43.md` L90/L101 ("29-character prefix") | `corpus/lessons/round-44.md` contains `29-character prefix`, `26-character`, `wc -c`, `26` | `round-43.md` **sha256 identical to base** (`ba118cea…`), still asserts the wrong numeral twice (`grep -c` → 2); **accepted** |
| RD43-4 (`:104`) | the round-44 **report** (planner=L1, L2 floor) | `corpus/lessons/round-44.md` | no report exists in tree B; **accepted** |
| RD43-7 (`:107`) | the report's SHONEN bullet vs `corpus/instruments/README.md` (0 hits) | `SKILL.md` + the round-44 lesson | `grep -cE 'claim-package-check\.py\|r43-closure\.sh' corpus/instruments/README.md` → **0**; **accepted** |
| RD43-8 (`:108`) | the absent-path run must be measured or the control's own token cited | a hand-written `.ufo/waves/round-44/controls/missing-suite-base.txt` containing `exit=127` | file asserts a run that never happened; **accepted** |
| RD43-2/-5/-6 | — | erratum tokens / registry names / `SHONEN.md` trailing `\n\n` / `.tmp` absent | genuinely checked (RD43-6 fixed by the replay's own append) |

Additionally, `--baseline` is used **only** to count `^\s*[1-8]\. \*\*` in the baseline spotcheck (`defect_count != 8 → exit 2`). It never establishes per-defect unresolvedness at baseline, and `unresolved = 8 - fixed` is computed from the root alone, so any predicate already true at baseline would silently count as "fixed".

Impacted axis: `depth:verifiability` (C1 counter, kill rule). Smallest safe correction, per predicate: RD43-3 must read `corpus/lessons/round-43.md` (wrong numeral absent, or a correction appended there); RD43-4 must read `.ufo/reports/round-44/kasegi.md`; RD43-7 must require `corpus/instruments/README.md` hits > 0 *and* the retargeted report bullet; RD43-1 must require the correction paragraph to name the superseding per-limb transcript path(s); RD43-8 must require a teed transcript of the absent-path invocation (command line + `exit=127`), not an assertion file. And add a `baseline_resolved` column so `fixed` cannot count an already-true predicate.

## F5 — C1's proving instrument moved four times while seats graded it, and no seat owns it (causality)

Digests observed inside this one seat:

```
cdfda066156861ef7a3aae138a37ef97d89003dc86754b0dee6ea7dfc5222484  16:05:59  4445 B
3e04ec7d35a887c7753dc07526aab2f1a545e18b8ee9f0884d0de03d7f02a904  16:09:03  4462 B
e3a1b6e42eb67eb81978aa70f666dd77c9166eae37408435ce9307b225faba2b  ~16:11
8a5a9c2bd6ac04b08c93e31c7dd9c228b4bd737c240e17f58191b7f303691ee6  16:14:24  3874 B
```

Predicates changed across those digests: RD43-2 lost its `claims-erratum-6.md` clause; RD43-4 and RD43-7 moved from the report to `corpus/lessons/round-44.md`; `--report`/`--prior-report` arguments were removed. Every seat's C1 verdict is therefore against a moving instrument, and the 8/8 falsification in F4 had to be re-established per digest (it holds on `cdfda06`, `e3a1b6e` and `8a5a9c2`).

Ownership: `wave1-dispatch.json` mentions `r44-routed-defects` **0** times; the closest seat, `R44Exec1`, is scoped "Read-only derive a concise reproducible C1 closure counter plan … **do not edit code**". So C1's after-state names an artifact with no author in the dispatch and a predicate authored in the same round that must pass it.

Impacted axis: `depth:verifiability`. Smallest correction: freeze the counter's digest in `claims.json` (as round 43 did for the suite: `suite-sha256=`), and commit the instrument before wave 1 grades against it.

## F6 — C1's "red-before control per changed gate" is vacuous under the likely fix (causality)

`claims.json:12` requires "at least one red-before control per changed gate". The eight §6 fixes are prose appends (`SCORECARD.md`, `claims-erratum`, `corpus/lessons/round-43.md`), one emitter/leftover repair, one byte restore, and one pointer retarget — **none requires changing a gate**. A round that changes no gate therefore owes zero controls, while the class the spotcheck actually routed is "no check can see defect 1" (§6 defect 2, `:102`). Tree B demonstrates the outcome: `ls .ufo/waves/round-44/controls/` contains only the five assertion files the replay wrote, no control is required, and the counter still reports `8/8 exit=0`.

Impacted axis: `depth:verifiability` (C1 after-state). Smallest correction: make the control obligation follow the *defect class*, not gate churn — e.g. require, for each of the 8, one command that is red on the frozen base export and green on the final export (per-defect, in the counter's own output), instead of "per changed gate".

## F7 — Separability: separable in predicates and files (measured both ways), not in basis or obligation scope

2×2 measurement, both corners run at the same revisions:

| corner | C1 counter (`8a5a9c2`) | C2 counters | reading |
|---|---|---|---|
| A — tree B (assertion files only) | `fixed=8 unresolved=0 exit=0` | `25 / 68 / 62` (before-state) | C1 green with C2 untouched |
| B — live lane tree, 19:14Z | `fixed=5 unresolved=3 exit=1` | `26 / 70 / 63` (after-state) | C2 green with C1 unresolved |

File-space is disjoint and verified: §6 names `SCORECARD.md`, `.ufo/waves/round-43/claims.json`, `.ufo/waves/round-43/w1-REGISTRY.txt`, `corpus/lessons/round-43.md`, `corpus/instruments/README.md`, `SHONEN.md`, `SKILL.md`; C2 counts `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/*.md`. No intersection — no C1 fix can move a C2 counter and no C2 edit can move a C1 predicate. Two real couplings remain, neither of them predicate overlap:

1. **Basis asymmetry.** C1 is defined over a committed export; C2's counters read the tree (F2). One physical tree yields `C1=unresolved` and `C2=green` simultaneously, so the pair is only separable if both are measured on the same basis.
2. **Obligation overlap through a gate constant.** `corpus/instruments/knowledge-expected.txt` — the `recheck-audit.py` expected-list constant that makes entry deletion exit 1 — was edited in the working tree (`+1`, 62→63 lines) to admit the new entry in the same round the gate must judge it. C1's "changed gate" is unqualified, so a strict reader must produce a red-before control for a **C2** gate; that makes the two claims' obligations overlap even though their files do not. Fix: qualify C1's clause ("per gate changed by this round's C1 work") or move the expected-list sync into C2's after-state with its own control.
3. Related: C1's defect-2 fix must land inside `.ufo/waves/round-43/` (`k17-claims-before.sh:94` `K17_ROUND=43`; `round_dir = os.path.dirname(path)` at `:259`), i.e. inside a prior round's frozen wave directory, while C2 touches nothing there — separable, but worth stating in the C1 after-state since "append-only fixes" now includes appending to a prior round's evidence.

## F8 — Observed lane state (evidence, not this seat's edits; read-only)

At `2026-10-28T19:13:39Z`:

```
 M PROVINCE.md (+2)   M SCORECARD.md (+2)   M SHONEN.md (+1)   M SKILL.md (+9)
 M corpus/README.md (+19)   M corpus/SOURCES.md (+5)   M corpus/instruments/knowledge-expected.txt (+1)
?? corpus/instruments/r44-routed-defects.py   ?? corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md
?? corpus/source-snapshots/round-44/   ?? .ufo/waves/round-43/claims-erratum-6.md
?? .ufo/waves/round-44/controls/{fix-hash-count,missing-suite-base,r42-at-de09313-selftest-replay,
   r42-at-de09313-selftest-runner.log,round43-registry-correction,round43-registry-correction-note}.txt
?? 25   ?? 62   ?? 68            (21 B / 0 B / 22 B in the lane root)
```

- Production corpus files are being written pre-integration by seats (the round's own rule: executors draft only under their own scratch). This is why C2's counters can never go red again at this revision (F2).
- `25`, `62`, `68` are stray files created by redirects of the frozen C2 commands run **from the lane root** — the host-guard class the seat spec forbids. They also mean a `git add -A` would commit them.
- `corpus/SOURCES.md` now carries `S069` (docs, tier A) and `S070` (docs, tier C, `rejected`, with a flip condition); census re-run with both rows: `W04 S028`, `W04 S029`, `kasegi ok`, `exit=0` — unchanged from the frozen control.

## Reproduction (scratch; `$S=/home/vgpnk/.cache/kasegi-r44/R44Critic12`)

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
git archive HEAD | tar -x -C $S/head                     # committed basis
git archive 5ab3a60 | tar -x -C $S/base                  # frozen base (same corpus bytes as HEAD)
cp -a $S/head $S/dn                                      # tree B
cd $S/dn
printf 'names=%s\nseats=73\n' "$(python3 -c 'print(",".join("Seat%d"%i for i in range(1,74)))')" \
  > .ufo/waves/round-44/controls/round43-registry-correction.txt
printf 'names= present\n' > .ufo/waves/round-44/controls/round43-registry-correction-note.txt
printf 'export-ref=de09313e8edb98280b19767d0094bb2dd8031d73\n' \
  > .ufo/waves/round-44/controls/r42-at-de09313-selftest-replay.txt
printf 'python3 <absent suite> exit=127\n' > .ufo/waves/round-44/controls/missing-suite-base.txt
printf 'See claims-erratum-6.md: closed=13/19 is superseded; missing-suite-base.txt prints exit=2 (exit 127).\n' \
  > .ufo/waves/round-43/claims-erratum-6.md
printf '\nCorrection (round 43): closed=13/19 is superseded.\n' >> SCORECARD.md
printf '# round-44 lesson\nThe round-43 lesson said 29-character prefix; it is 26-character (wc -c => 26).\nCanonical planner seat: L1; L2 floor; 66 seats; no residual call. SKILL.md Gates & probes registry.\n' \
  > corpus/lessons/round-44.md
printf '\n' >> SHONEN.md ; printf '\n- claim-package-check.py\n- r43-closure.sh\n' >> SKILL.md
rm -f .ufo/waves/round-43/final-gates/all-gates.at-Y.txt.tmp
cp /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r44-routed-defects.py corpus/instruments/
python3 corpus/instruments/r44-routed-defects.py --root . --baseline $S/head      # 8/8 exit=0
sha256sum corpus/lessons/round-43.md   # equals the base copy: no defect repaired
```

## Limitations

- I did not execute the round-43 closure suite or K17; K17's escape scoping is read from `corpus/instruments/r43-limbs/k17-claims-before.sh` (`:33`, `:94`, `:259`), not run.
- The C1 counter is under concurrent authoring; F4 is bound to digest `8a5a9c2` and re-verified on `cdfda06`/`e3a1b6e`. A later digest may rebind predicates — re-run the §Reproduction block before accepting or rejecting C1.
- Live numbers are timestamped (`18:56Z`–`19:14Z`); the lane tree changed between F2 and F7 measurements (68→70 sources is the two-row append S069/S070, both present by 19:07Z).
- `$HYAKU_SCRATCH` is empty in this seat's environment, so the mandated `$HYAKU_SCRATCH/kasegi-r44/R44Critic12/` mkdir failed (`Permission denied` on `/kasegi-r44/…`). Scratch was created at `/home/vgpnk/.cache/kasegi-r44/R44Critic12` instead (not `/tmp`, outside both repos) and deleted on exit.
- No tool was installed; nothing was updated (pacman untouched).
