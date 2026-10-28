VERDICT: BROKEN

# R46RevC1L3 — C1 limb L3 attack (recheck lines name the gate and run it)

Attacked: limb L3 of `corpus/instruments/r46-c1-gate.py` (sha256 `b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294`, matches `freeze.txt` `c1-gate-sha256`). Frozen sentence (claims.json C1 `after`): "a recheck line that runs `r46-c1-gate.py --entry` on itself with no ~/ or $HOME path". The counter's L3 implementation, verbatim:

- `corpus/instruments/r46-c1-gate.py:61` `CD_RE = re.compile(r"^cd[ \t]+[^&;]+?[ \t]*&&[ \t]*")`
- `corpus/instruments/r46-c1-gate.py:62` `HOME_RE = re.compile(r"(?:~/|\$HOME|\$\{HOME\}|/home/)")`
- `corpus/instruments/r46-c1-gate.py:187` `if HOME_RE.search(CD_RE.sub("", ln, count=1)) or ("r46-c1-gate.py" not in ln) or ("--entry corpus/knowledge/%s" % e) not in ln:`

L3 is a pure substring/regex test on the recheck line. It never executes the line. The only execution of the line is in `classify()` (L1/L2), where exit 0 means "not gated", whatever the line ran. The `cd` prefix is stripped before both the HOME test and the execution.

Scratch: `/fast/scratch/hyaku/kasegi-r46/R46RevC1L3/` (copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure` plus the frozen gate). Command for every counter run: `TMPDIR=<scratch>/tmp python3 <tree>/corpus/instruments/r46-c1-gate.py --root <tree> --baseline /fast/scratch/hyaku/kasegi-r46/L1/pure`. Nothing in the lane, the fleet, or git was touched. No commits.

## Finding 1 — L3 passes a recheck line that never runs the gate (cheapest tree)

Edit: `corpus/knowledge/claim-gates.md:125` replaced with

    recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && true  # r46-c1-gate.py --entry corpus/knowledge/claim-gates.md

Counter output (scratch tree, single edit, no re-ground section):

    gate L1 pass=0 read=gated=23 broken=0 lines=64/base=64
    gate L2 pass=0 read=base-gated=24 regrounded=1 claim-gates.md
    gate L3 pass=1 read=recheck-lines-clean=1
    gate L4 pass=0 read=bad=claim-gates.md
    gate L5 pass=0 read=bad=claim-gates.md
    gate L6 pass=0 read=mutants=0 survivors=none
    gate L7 pass=1 read=still-gated=23 changed=none
    c1-gate fixed=2/7 exit=1

L3 reads pass=1 with the defect present: the entry has no re-ground section (L4 and L5 red) and its recheck line never invokes the gate. Discriminated against the do-nothing control (scratch tree = base + gate, unedited):

    gate L3 pass=0 read=recheck-lines-clean=0
    c1-gate fixed=1/7 exit=1

## Finding 2 — full forgery reads 7/7 with recheck lines that run nothing

Tree: both `claim-gates.md` and `claim-package-contract.md` carry the Finding-1 comment-trick recheck line, plus a real `## Re-ground (round 46)` section of six rows each over two committed files (`corpus/instruments/claim-package-check.py` and `corpus/instruments/fixtures/claim-package/defect-1-missing-file/status.json`). Rows used (verbatim):

    | G1 | the committed report gate requires the scope-excerpt heading | `corpus/instruments/claim-package-check.py:74-75` | `report.md carries the` |
    | G2 | the committed report gate requires the literal no-submission line | `corpus/instruments/claim-package-check.py:75` | `No submission performed` |
    | G3 | the committed manifest gate requires a 64-hex expected_head_sha256 | `corpus/instruments/claim-package-check.py:54` | `64-hex expected_head_sha256` |
    | G4 | the committed custodian gate fails a non-NO_SCOPE_OBJECTION decision | `corpus/instruments/claim-package-check.py:460-461` | `if decision.get('scope_signal') != 'NO_SCOPE_OBJECTION':` |
    | G5 | the committed status gate fails a non-boolean claimable | `corpus/instruments/claim-package-check.py:610-611` | `raise _GateFail('claimable=not-bool')` |
    | G6 | the defect-1 fixture pins claimable false | `corpus/instruments/fixtures/claim-package/defect-1-missing-file/status.json:6` | `"claimable": false,` |

(contract entry: G1 `claimable = status.get('claimable')` at 609-611; G2 `count = status.get('finding_count')` at 617-619; G3 `'no_duplicate_or_prior_submission',` at 123-128; G4 `head = manifest.get('expected_head_sha256')` at 310-312; G5 `if not _named_blocker(status):` at 621-622; G6 as above.)

Counter output on that tree:

    gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
    gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
    gate L3 pass=1 read=recheck-lines-clean=2
    gate L4 pass=1 read=entry-mode-green=2
    gate L5 pass=1 read=append-only=2
    gate L6 pass=1 read=mutants=12 survivors=none
    gate L7 pass=1 read=still-gated=22 changed=none
    c1-gate fixed=7/7 exit=0

    reground entry=claim-gates.md rows=6 ok=6 files=2 exit=0
    reground entry=claim-package-contract.md rows=6 ok=6 files=2 exit=0

So the counter's 7/7 is reached while neither recheck line executes the gate. Its only protection against this is L4/L6, which run the entry-mode directly, not the recheck line.

## Finding 3 — the lane's recheck line is decorative after drift (the real defect)

Tree `dr` = Finding-2 tree with one row token drifted (`claim-gates.md` G3 token changed to `64-hex expected_head_sha384`). Output of running each command in the tree root:

    FORGED LINE: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && true  # r46-c1-gate.py --entry corpus/knowledge/claim-gates.md
    forged-line rc=0
    row G3 ok=0 read=token-not-in-lines
    reground entry=claim-gates.md rows=6 ok=5 files=2 exit=1
    entry-mode rc=1
    (honest line: python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md, run in dr)
    honest-line rc=1

The forged line stays green (rc 0) while the entry is red (rc 1). That is the defect: the recheck line is supposed to be the lane's drift detector, and here it detects nothing.

The lane's own strict audit already distinguishes this. `corpus/instruments/recheck-audit.py` on a minimal tree holding the two forged entries (`--root <scratch>/mini`):

    claim-gates.md                                  frozen=111 strict=111001 lane=0   foreign=0   executes    FROZEN-ONLY
    claim-package-contract.md                       frozen=111 strict=111001 lane=0   foreign=0   executes    FROZEN-ONLY
    strict pass=0/2 cdroot_fail=2 instrument_fail=2 own_fail=0

(strict order is parse,cwd,paths,cdroot,instrument,own: `instrument` = 0 on both lines because no `corpus/instruments/*.py` is named. `cdroot` also fails here partly because the `cd` targets the live lane, not the mini root, so cite only `instrument`.) The frozen counter's L1/L2 classify the same forged lines as "executes" (not gated), so the score-gap gated count drops without any execution. The weakness is in the counter's L3 (text-only), not in recheck-audit's strict limbs.

## Finding 4 — further constructions that pass L3 (each a distinct, run construction)

Each run on the Finding-2 base unless stated.

(a) Exit override: `corpus/knowledge/claim-gates.md:125` = `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md ; true`, on the pure base with no re-ground section.
    gate L3 pass=1 read=recheck-lines-clean=1
    c1-gate fixed=2/7 exit=1
    direct: gate alone rc=1 (`reground entry=claim-gates.md rows=0 ok=0 exit=1 read=section-count=0`); line form `bash -c '... ; true'` rc=0.
    The gate runs and fails, but the trailing `; true` masks it; L3 passes and classify counts the entry as not gated.

(b) Another file's gate: `corpus/knowledge/claim-gates.md:125` = `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md  # --entry corpus/knowledge/claim-gates.md`
    gate L3 pass=1 read=recheck-lines-clean=2
    c1-gate fixed=7/7 exit=0
    The line runs the gate on the other (really re-grounded) entry; the substring test is satisfied by the trailing comment naming this entry.

(c) Home-path cd prefix: `corpus/knowledge/claim-gates.md:125` = `recheck: cd ~/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md`
    gate L3 pass=1 read=recheck-lines-clean=2
    c1-gate fixed=7/7 exit=0
    CD_RE (line 61) strips the cd prefix before HOME_RE (line 62) runs, so `~/` in the prefix is invisible to the test while the sentence forbids it. Mechanism of the path itself, run in a fake HOME:
    `HOME=<scratch>/fakehome bash -c 'cd ~/Projects/shokunin/kasegi-shokunin && pwd'` -> `<scratch>/fakehome/Projects/shokunin/kasegi-shokunin`, `fakehome-cd rc=0`. The `cd` target is HOME-relative, so the line runs wherever `~` points, not the audited root.

(d) Comment-only mention (Finding 1 / Finding 2): `true  # r46-c1-gate.py --entry corpus/knowledge/<e>.md`. L3 pass=1 both times.

(e) Limb-alone control (not a bypass): `corpus/knowledge/claim-gates.md:125` = `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md  # note: the bounties base lived at ~/Projects/bounties`
    gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
    gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
    gate L3 pass=0 read=bad=claim-gates.md
    gate L4 pass=1 read=entry-mode-green=2
    gate L5 pass=1 read=append-only=2
    gate L6 pass=1 read=mutants=12 survivors=none
    gate L7 pass=1 read=still-gated=22 changed=none
    c1-gate fixed=6/7 exit=1

Answer to "can the limb fail alone": yes. In (e) L3 is the only red limb, and the verdict is 6/7 because of it. So L3 is load-bearing in the text sense. It is still the only limb that asserts "runs the gate", and it does so by substring, so the five constructions in (a)-(d) pass it.

## Control gap in the frozen controls

`.ufo/waves/round-46/controls/freeze-controls.txt` has nine controls (red=9). The only control that makes L3 red is "marker-only" (`true`, no comment) with `gate L3 pass=0 read=bad=claim-gates.md,claim-package-contract.md`. No control in the file exercises a comment naming the gate, an exit override, another file's gate, or a `cd ~/` prefix. The frozen control set therefore does not falsify L3; the constructions above do.

## Verdict basis

- Frozen counter falsified: the `c1-gate fixed=7/7 exit=0` run in Finding 2 is reached with recheck lines that run `true`, against the frozen sentence. The frozen kill rule has no clause for this case (it only tests `fixed<7/7` at the final revision and the listed controls); this is a counter defect the kill rule does not cover, so it is reported here as a falsification of the counter's claim to measure "recheck runs the gate", not as a kill-rule trigger.
- Recipe (cheapest, reads L3 pass=1): change `corpus/knowledge/claim-gates.md:125` to the single line in Finding 1. Full 7/7 recipe: Finding 2 (two comment-trick lines + the two 6-row sections above).

## Limitations

- The forged 7/7 tree is mechanically valid, not semantically sound: the rows were chosen to locate tokens, not reviewed for whether they support the entries' claims. This does not affect the L3 finding, which concerns the recheck line, not the rows.
- Finding 3 ran the recheck lines via `bash -c` in scratch roots. The lines begin with `cd /home/vgpnk/...`, so the `cd` did change into the live lane directory before `true`. `true` does nothing there; I did not run any non-trivial command in the live lane.
- Finding 4(c) was tested for the counter's text test and for the path's expansion in a fake HOME. I did not run the verbatim line against the real HOME `~`, because it would execute against the live lane.
- Tilde-user forms (`~vgpnk/...`) were not tested; a `$(…)`-built path and `eval` indirection were not tested either.
- Not tested: whether `recheck-audit.py`'s strict `cdroot` limb holds on a correctly-rooted tree (only `instrument` was cited).
- Observation outside L3 scope: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD` printed `323d1f5d825a61cfd0dbf93f9580e092ee21c72a`, while the freeze record names `9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5`. I did not verify the freeze commit; the on-disk gate sha256 matched the freeze record.
- Scratch removed on exit. No commit, push, index change, or edit to a shared file was made. No tool was installed or upgraded.
