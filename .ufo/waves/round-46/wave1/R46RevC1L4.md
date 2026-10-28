VERDICT: BROKEN

# R46RevC1L4 — C1 limb attack on L4 (per-entry mode, token-location only)

Scope: limb L4 of `corpus/instruments/r46-c1-gate.py` (sha256 b0c730c834b4d7c6…, identical to the lane copy). L4 = "every entry of R: per-entry mode (this script's own bytes) exits 0 at TREE". Scratch: `$HYAKU_SCRATCH/kasegi-r46/R46RevC1L4/` (removed on exit). Driver: `drive.py` in that scratch. Base: pure export `/fast/scratch/hyaku/kasegi-r46/L1/pure` (copied, never edited).

## Finding 1 — L4 passes rows whose anchors hold the token by accident (BROKEN)

Recipe (construction K1-single-line): copy pure base; copy the counter into `corpus/instruments/`; in `corpus/knowledge/claim-gates.md` and `claim-package-contract.md` replace the recheck line with `recheck: python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<e>` and append:

```
## Re-ground (round 46)

| id | current claim | committed anchor | token |
|---|---|---|---|
| G1 | six contract files present, regular, non-symlink, non-empty | `corpus/instruments/r46-c1-gate.py:67` | `return` |
| G2 | schema_version must equal evidence-manifest/v1 | `corpus/instruments/r46-c1-gate.py:83` | `return` |
| G3 | redactions[] must be non-empty | `corpus/instruments/r46-c1-gate.py:122` | `return` |
| G4 | every custodian decision carries scope_signal NO_SCOPE_OBJECTION | `corpus/instruments/claim-package-check.py:152` | `return` |
| G5 | head_sha256 must equal the final decision digest | `corpus/instruments/claim-package-check.py:164` | `return` |
| G6 | the gate prints eight RULE lines | `corpus/instruments/claim-package-check.py:166` | `return` |
```

The anchored lines (sed output, quoted):
- `r46-c1-gate.py:67`: `    return " ".join(s.split())` (the `norm` helper)
- `r46-c1-gate.py:83`: `    return None` (`recheck_line`, no match)
- `r46-c1-gate.py:122`: `    return True, "token-located", rel`
- `claim-package-check.py:152`: `    return text or 'unknown'`
- `claim-package-check.py:164`: `        return None, 'empty'`
- `claim-package-check.py:166`: `        return None, 'absolute'`

None of these lines says anything about the claim in its row (schema, redactions, scope_signal, head digest, eight rules). Rows are token-vacuous: `return` is a 6-character token that every Python function contains.

Command: `python3 tree/corpus/instruments/r46-c1-gate.py --root tree --baseline /fast/scratch/hyaku/kasegi-r46/L1/pure --work <scratch>/tmp` (K1 tree). Output (quoted from run-final.txt):

```
row G1 ok=1 read=token-located
...
row G6 ok=1 read=token-located
reground entry=claim-gates.md rows=6 ok=6 files=2 exit=0
[per-entry claim-gates.md exit=0]
...
reground entry=claim-package-contract.md rows=6 ok=6 files=2 exit=0
[per-entry claim-package-contract.md exit=0]
gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-clean=2
gate L4 pass=1 read=entry-mode-green=2
gate L5 pass=1 read=append-only=2
gate L6 pass=1 read=mutants=12 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```

So the exact gate line that reads green while the defect (rows unsupported by their anchors) is present is:
`gate L4 pass=1 read=entry-mode-green=2`

Wider constructions, same result (run-all.txt): K2-wide-40 (1-40 window holding `stdlib`, line 40 `READ-ONLY on TREE and BASE; ... stdlib only.`; and claim-package-check.py:1-40 holding `contract`) → `c1-gate fixed=7/7 exit=0`. K3-window-return (60-99 / 150-189 windows holding `return`) → `fixed=7/7 exit=0`. K4-cross-line (token `--entry corpus/knowledge/<entry>.md` spanning r46-c1-gate.py:15-16, which is only matched after whitespace normalisation; `with the per-gate derivations` spanning claim-package-check.py:4-5) → `fixed=7/7 exit=0`. L6 stays green in all of them (`mutants=12 survivors=none`): blanking a vacuous token in the anchored file makes that row fail, so "load-bearing" is only token presence, not support.

## Finding 2 — L4 cannot tell honest rows from vacuous rows (discrimination)

- Honest comparator K5 (correct anchors: claim-package-check.py:276 `six contract files present`, :305 `evidence-manifest/v1`, :367 `redactions=empty`, :460 `NO_SCOPE_OBJECTION`, :464 `head_sha256`; claim-package-selftest.py:12 `prints exactly the eight RULE lines`) prints the same `gate L4 pass=1 read=entry-mode-green=2` and `c1-gate fixed=7/7 exit=0` (run-final.txt, K5 block).
- Do-nothing control (tree = pure base + counter, no re-grounds), `control-donothing.txt`: `gate L4 pass=0 read=entry-mode-green=0`, `c1-gate fixed=1/7 exit=1` (matches the frozen control and `expect_before`). Tool exit code 1.
- Frozen control `controls/freeze-controls.txt:41-45` ("gutted-entry", body deleted, rows valid): `gate L4 pass=1 read=entry-mode-green=2`. Only L5 catches it. Corroborates that L4 reads token presence, not content.

So the L4 read is identical for honest and vacuous rows; the only separation between them is the do-nothing control (1/7), which is not a content discriminator. Semantic support is left to the "non-author reading" kill-rule clause, which the counter cannot run.

## Finding 3 — L4 can fail alone (load-bearing for softened recheck lines)

Construction K6-softened-one-bad-row: honest rows except G6 whose token is absent (`zz-no-such-token-zz` at r46-c1-gate.py:1-40), and the recheck line gets a `; true` suffix (`tree/.../claim-gates.md:125`: `recheck: python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md; true`). Output (run-final.txt, K6 block):

```
gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-clean=2
gate L4 pass=0 read=bad=claim-gates.md,claim-package-contract.md
gate L5 pass=1 read=append-only=2
gate L6 pass=1 read=mutants=12 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=6/7 exit=1
```

Per-entry: `row G6 ok=0 read=token-not-in-lines` / `reground entry=claim-gates.md rows=6 ok=5 files=2 exit=1`. L3 misses the `; true` softening (it only checks for `~/`, `$HOME`, `r46-c1-gate.py` and `--entry corpus/knowledge/<e>` substrings), so L4 is the only limb that reads it. Without the softening (K6b), the entry stays gated and the whole counter collapses to `fixed=0/7` (L1, L2, L3, L4, L5, L6 red with `gated=24`). So L4 is not decorative: it is the only catch for a softened recheck line. It is not load-bearing for support.

## Constructions tried (6 distinct, 4 vacuous)

1. K1 single-line accidental token (`return`, one-line anchors) — fixed=7/7 (BROKEN)
2. K2 40-line windows with generic `stdlib` / `contract` — fixed=7/7 (BROKEN)
3. K3 40-line windows with `return` — fixed=7/7 (BROKEN)
4. K4 cross-line normalised tokens — fixed=7/7 (BROKEN)
5. K5 honest comparator (correct anchors) — fixed=7/7 (same L4 read)
6. K6 softened `; true` recheck + one absent token — L4 alone red, fixed=6/7
(+ K6b unsoftened control, fixed=0/7.)

## Limitations

- The counter's L4 is token location; my "rows do not support the claims" judgement for K1–K4 is a manual reading of the anchored lines quoted above, not a counter output.
- The aggregate ran with the tree's copy of the script as the tool (identical sha256 to the lane copy); L4 itself uses the script's own bytes via `-I`, as specified.
- Each construction was run once; the runs are deterministic (no timing dependence observed).
- Scope: I did not build the F28 entry, the honest C1 re-grounds for the lane, or any C2 material. My item was the L4 attack only.
- The `control-donothing.txt` file lacks a trailing `exit=` line I intended to write; the exit status 1 is the tool's report and the printed line `c1-gate fixed=1/7 exit=1` is in the file.
- No tools installed or upgraded. No git/jj mutation; read-only `git rev-parse` only. No commits, pushes, or edits to shared files.

Suggested check for the main agent: a counter-level fix would need L4 to fail on rows whose tokens are shorter than a per-row support check or whose anchor line lacks a claim keyword, which the frozen counter does not do; until then, the C1 score move rests on a non-author reading (kill rule), not on `c1-gate fixed=7/7`.
