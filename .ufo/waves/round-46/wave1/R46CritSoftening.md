# R46CritSoftening — honesty critic, C1 (depth:verifiability)

VERDICT: HOLDS

Conditional. Restricted re-grounding is faithful for both entries (>=6 gate-faithful rows each). The frozen counter cannot tell faithful rows from overreaching rows, so C1 must not rest on its 7/7. No C1 re-ground drafts exist yet in `wave1/` (only `R46ExecPlain.draft/plain-measure.sh` and an empty `R46ScribeRegistry.draft/`, per `ls`), so this verdict covers the plan in `build-wave1-spec.py` plus oracle trees I built, not drafter text.

Scratch: `/fast/scratch/hyaku/kasegi-r46/R46CritSoftening/` (removed on exit). All commands run read-only against the lane; nothing committed or mutated.

## 1. Frozen counter and controls reproduce

Command: `sha256sum corpus/instruments/r46-c1-gate.py` (worktree), `git show 9f23aab:corpus/instruments/r46-c1-gate.py | sha256sum`.
Output: both `b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294`, equal to `freeze.txt` `c1-gate-sha256`. `claims.json` sha `e56ebf87...c740` equals `claims-sha256`. `git log 914ca0b..HEAD` on the two entries and `claim-package-check.py` is empty: entries unchanged since base.

Command: `python3 .ufo/waves/round-46/controls/freeze-controls.py --lane <lane> --base 914ca0b6... --work <scratch>` then diff against `freeze-controls.txt` (ignoring wall-time).
Output: IDENTICAL-TO-FROZEN. Tail: `controls total=9 red=9 green=0`.

Do-nothing control on the base export: `python3 -I r46-c1-gate.py --root base --baseline base`
```
gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64
gate L2 pass=0 read=base-gated=24 regrounded=0
...
c1-gate fixed=1/7 exit=1
```

## 2. Falsifier: the counter awards 7/7 to contradicted and unenforced rows

Tree (`fals`): base copy; both entries' `recheck:` replaced by `recheck: cd <lane> && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<e>.md`; counter copied into `corpus/instruments/`; appended `## Re-ground (round 46)` with 6 rows each. Rows (anchor → token, token present so the row is "located"):

claim-gates.md:
- G1 `claim_checklist.md must match /OPERATOR-GATED/i` → `exemplar/claim_checklist.md:3` `OPERATOR-GATED: every step below`
- G2 `report.md must match /no submission (performed or made)/i` → `exemplar/report.md:88` `No submission performed.`
- G3 `steps/transitions/agents, at least one non-empty` → `claim-package-check.py:489` `document.get('agents')`
- G4 `state === 'DONE' (anything else fails)` → `exemplar/status.json:4` `"state": "BLOCKED"`
- G5 `claim_review.outcome === 'APPROVED'` → `claim-package-check.py:590` `'claim_review', 'status'`
- G6 `blocker fields blocked_reason ... -> error` → `claim-package-check.py:570` `'blocked_reason'`

claim-package-contract.md:
- G1 `claim_checklist carries OPERATOR-GATED` → `exemplar/claim_checklist.md:3`
- G2 `Scope excerpt = verbatim text + URL + observed_at + sha256` → `exemplar/report.md:9` `## Scope excerpt`
- G3 `DONE requires reviewer APPROVED with claim_ready:true` → `exemplar/status.json:4` `"state": "BLOCKED"`
- G4 `claimable:true is the queue bit` → `exemplar/status.json:6` `"claimable": false`
- G5 `reviewer identity distinct; role kx-reviewer` → `exemplar/status.json:32` `"identity": "exemplar-reviewer"`
- G6 `custodian chain grant + NO_SCOPE_OBJECTION` → `claim-package-check.py:460` `'NO_SCOPE_OBJECTION'`

Command: `python3 -I <fals>/corpus/instruments/r46-c1-gate.py --root <fals> --baseline <base> --work <scratch>`
Output:
```
gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L3 pass=1 read=recheck-lines-clean=2
gate L4 pass=1 read=entry-mode-green=2
gate L5 pass=1 read=append-only=2
gate L6 pass=1 read=mutants=12 survivors=none
gate L7 pass=1 read=still-gated=22 changed=none
c1-gate fixed=7/7 exit=0
```
Row status in this tree: claim-gates G1 and G5 unenforced; G2, G4, G6 contradicted; G3 narrower than the gate. Contract G1 and G3 unenforced; G2 narrower (regex, no observed_at or sha256); G4 is a census-era queue bit with no gate predicate; G5 unenforced for `role`; G6 faithful. Section 4 gives the evidence for each (E0, E1, E3, E4, or the gate's own entry).

## 3. Faithful restricted tree also gets 7/7 (counter does not discriminate)

Tree (`faith`): same mechanics, rows restricted to tokens on committed gate lines plus one exemplar row per entry (rows listed in section 4 under "faithful"). Output:
```
gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
gate L6 pass=1 read=mutants=19 survivors=none
c1-gate fixed=7/7 exit=0
reground entry=claim-package-contract.md rows=11 ok=11 files=2 exit=0
reground entry=claim-gates.md rows=8 ok=8 files=2 exit=0
```
So the counter's 7/7 is compatible with faithful and with overreaching rows. Faithfulness is only decidable by reading the row claim against the anchored line. The frozen kill rule already delegates this to a non-author reading; the claims.json `after` text should not present 7/7 as proof.

Why L6 is weak: `r46-c1-gate.py:221-222` replaces every occurrence of the token in the anchored file, so any token that occurs in the file is load-bearing by construction. Why L1–L7 cannot see semantics: `check_row` (`r46-c1-gate.py:101-122`) is a substring test on raw lines; it does not know whether an anchor is code, docstring or fixture.

## 4. Entry claims vs committed bytes (side by side)

Entry line quoted verbatim; committed line quoted from `corpus/instruments/claim-package-check.py` (gate) or the fixture.

| Entry | Entry text | Committed | Status |
|---|---|---|---|
| contract:11 | `"Scope excerpt" = verbatim policy text + URL + observed_at + content sha256` | gate:120 `SCOPE_EXCERPT = re.compile(r'scope\s+excerpt', re.IGNORECASE)`; gate:634-635 | NARROW (regex anywhere in text; observed_at and sha256 unchecked) |
| contract:11 | `literal marker "No submission performed"` | gate:121 `NO_SUBMISSION = 'No submission performed'`; gate:636-637 | FAITHFUL |
| contract:11 | `program + official URL` | gate:119 `HTTPS_URL = re.compile(r'https://[^\s)\]<>"]+')`; gate:638 | SUPERFICIAL (any https URL) |
| contract:12 | `carries "OPERATOR-GATED"` | `grep -c OPERATOR-GATED corpus/instruments/claim-package-check.py` → `0`; R-FILES gate:275-297 is presence/non-empty only | UNENFORCED (E1) |
| contract:13 | `schema_version: "evidence-manifest/v1"` | gate:305-306 | FAITHFUL |
| contract:13 | `sha256 + polarity; >=1 positive` | gate:332-335, 341-347, 354-355 | FAITHFUL |
| contract:13 | `artifact paths relative, inside evidence/, no symlink` | gate:336 `inspect_path(pkg.root, 'evidence/' + rel)`; gate:158-194 | FAITHFUL |
| contract:13 | `redactions[] nonempty; one same-digest receipt per artifact; distinct producer/verifier` | gate:366-367, 379-416 (415) | FAITHFUL |
| contract:14 | `scope_signal exactly "NO_SCOPE_OBJECTION"` | gate:460-461 | FAITHFUL |
| contract:14 | `head_sha256 == final decision == expected_head_sha256` | gate:462-472 (471 `if head.lower() != head_expected.lower():`) | FAITHFUL |
| contract:15 | `external_effects_performed: []` | gate:527-529 | FAITHFUL |
| contract:15 | `pin / policy_sha256` | gate:515-526 | FAITHFUL (format only) |
| contract:16 | `manifest_sha256 binds status to manifest bytes` | gate:584-589 (588 `recorded.lower() != actual`) | FAITHFUL |
| contract:31-33 | `DONE requires reviewer APPROVED with claim_ready:true` | `grep -c 'outcome\|APPROVED\|claim_ready'` on gate → `0` | UNENFORCED; claim-package-gate.md:24 disclaims |
| claim-gates:15 | `/no submission (performed\|made)/i` | gate:121 literal, case-sensitive, no `made` | CONTRADICTED (E4) |
| claim-gates:16 | `claim_checklist.md must match /OPERATOR-GATED/i` | 0 hits | UNENFORCED (E1) |
| claim-gates:11 | `report.md, claim_checklist.md, custodian-receipts.json, provenance.json, status.json, evidence/manifest.json (L22–24)` | gate:101-108 SIX_FILES; gate:279-297 | FAITHFUL (set; order differs; line refs are the lost tool's) |
| claim-gates:20 | `sequence is a number; expected_head_sha256 key present` | gate:307-312 | FAITHFUL (stricter: 64-hex) |
| claim-gates:24 | `>=1 positive-polarity artifact` | gate:354-355 | FAITHFUL |
| claim-gates:31-37 | `chain non-empty; scope_signal; matched_grant_id; decision_sha256 64-hex; head three-way` | gate:442-472 | FAITHFUL |
| claim-gates:41 | `steps/transitions/agents — at least one non-empty` | gate:489-491 `agents = document.get('agents')` only | NARROWER (agents only) |
| claim-gates:48 | secret regex `(api[_-]?key\|secret\|token\|password\|bearer)\s*[:=]\s*...{16,}` | gate:136-141 (bearer needs `\s+`, not `[:=]`; no bearer-colon shape) | DIVERGENT (E5) |
| claim-gates:54, 57 | blanket symlink ban; `5 * 1024 * 1024` cap | gate:131, 659-669, 672-674, 688-691 | FAITHFUL |
| claim-gates:67 | `state === 'DONE' (anything else fails, incl. SUBMITTED)` | no state check; exemplar `"state": "BLOCKED"` WELL-FORMED (E0) | CONTRADICTED (claim-package-gate.md:24, 33-34) |
| claim-gates:68 | `claimable === true` required | gate:609-611 type check only; exemplar `claimable:false` WELL-FORMED (E0) | CONTRADICTED (claim-package-gate.md:34) |
| claim-gates:69 | `manifest_sha256 = sha256 of manifest bytes` | gate:584-589 | FAITHFUL |
| claim-gates:70, 72 | `claim_review.outcome === 'APPROVED'`; `role === 'kx-reviewer'` | 0 hits | UNENFORCED |
| claim-gates:81 | prior-submission guard `submission_performed`, `submitted_url` | 0 hits; E2 WELL-FORMED | UNENFORCED (claim-package-gate.md:25) |
| claim-gates:86 | `Blocker fields: blocked_reason, ... → error` | gate:570 `for key in ('verdict', 'claimability_blocker', 'blocked_reason'):` used to ACCEPT a named blocker; E3 WELL-FORMED | CONTRADICTED (E3) |
| claim-gates:1 | `claim-check.mjs — the complete gate list` | gate docstring:2-8 "subset the contract states, and nothing more"; claim-package-gate.md:23-24 | CONTRADICTED ("complete") |

Faithful rows I used in the `faith` tree (anchors in committed gate unless noted):
- contract: G1 `SCOPE_EXCERPT = re.compile(r'scope` (120, heading form not checked); G2 `NO_SUBMISSION = 'No submission performed'` (121); G3 `'evidence-manifest/v1'` (305); G4 `if positive < 1:` (354); G5 `inspect_path(pkg.root, 'evidence/' + rel)` (336); G6 `producer.strip().casefold() == verifier.strip().casefold()` (415); G7 `if decision.get('scope_signal') != 'NO_SCOPE_OBJECTION':` (460); G8 `if head.lower() != head_expected.lower():` (471); G9 `if not isinstance(effects, list) or effects:` (528); G10 `recorded.lower() != actual` (588); G11 fixture `exemplar/provenance.json:88` `"external_effects_performed": [],`.
- claim-gates: G1 `SIX_FILES = (` (101, declaration only; weak); G2 `not isinstance(sequence, (int, float))` (308); G3 `if not isinstance(chain, list) or not chain:` (442); G4 `if os.path.islink(os.path.join(dirpath, name)):` (659); G5 `if st.st_size > MAX_SCAN_BYTES:` (672); G6 `raise _GateFail('claimable=true,finding_count=bad')` (619); G7 `raise _GateFail('claimable=not-bool')` (611); G8 fixture `exemplar/custodian-receipts.json:3` policy text.

Experiments (scratch copies of `exemplar`, run with `python3 corpus/instruments/claim-package-check.py <dir>`):
- E0 unmodified exemplar: `package=.../e0 rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0` (exemplar is `claimable:false`, `state: BLOCKED`).
- E1 `OPERATOR-GATED` replaced in `claim_checklist.md` only: `package=.../e1 rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`. So the entry's "carries OPERATOR-GATED" is not a gate predicate.
- E2 `state: SUBMITTED`, `submission_performed: true`, `submitted_url` set: `verdict=WELL-FORMED exit=0`. Matches claim-package-gate.md:25 (disclaimed; must stay historical).
- E3 `claimable: true`, `blocked_reason: "operator gate still open"`, all hard gates and subchecks `PASS`: `RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=true`, `verdict=WELL-FORMED exit=0`. Refutes claim-gates:86 "blocker fields → error".
- E4 `No submission made.` in report: `rules=8 pass=7 fail=1 verdict=DEFECT exit=1`. The committed gate is stricter than claim-gates:15 `(performed|made)`; claim-package-gate.md:29 says the same.
- E5 `notes.txt` containing `bearer: abcdefghijklmnop1234`: `RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0`, `verdict=WELL-FORMED exit=0`. The entry regex (claim-gates:48) matches the same string in Python (`entry regex hit=True`). Divergent.
- Selftest: `python3 corpus/instruments/claim-package-check.py --selftest | tail -3` → `selftest cases=10 failures=0`.

Circularity: the gate was written from the same contract the entries describe (gate docstring 2-8: "the executable gate for the subset the contract states, and nothing more"; `claim-package-gate.md` 22-27). Its exemplar is built from S067 for the scope excerpt text only. Any row anchored to the gate proves "the lane's gate implements the lane's contract", not "the lost `claim-check.mjs` did this" and not "a real bounty package must have this". Rows must be phrased as gate-implementation claims.

## 5. Claims that must stay historical

contract: lines 3-5 and 66-67 (lost-tree source); 7-8 (`claims/<program>/<slug>/` path, not used by the gate); 11 (program+URL, observed_at, sha256, repro, impact, fix, disclosure timeline: not gate-checked); 12 (OPERATOR-GATED); 18-27 (round-13 boundary note on the lost tool; stale, since the gate now enforces four of those per claim-package-gate.md:24); 31-35 (state enum, DONE requires APPROVED); 36-54 (verdict/claimable census, blocker fields); 56-62 (`node ops/claim-check.mjs` validation).

claim-gates: 1-6 (the "complete gate list" header); 15 `(performed|made)`; 16 OPERATOR-GATED; 41 steps/transitions; 43-50 secret regex (replace with the committed pattern set, not the entry's); 65-68 state DONE and claimable===true; 70-80 outcome, claim_ready, kx-reviewer, hard-gates-PASS-always, not-claimable heuristics; 81-85 prior-submission and global duplicate scan; 86 blocker fields; 88-91 nested readiness; 93-125 claim-index, prepare-claims, provenance pointers (not in the committed gate).

Conditions for HOLDS (all must be in the drafts):
1. Each row's claim column is phrased as a committed-gate claim ("R-MANIFEST requires ..." / "gate:NNN enforces ..."), not as a claim about the lost tool or real bounty packages.
2. The section enumerates the historical list above (or the drafter's equivalent), rather than declaring "every other line" historical in one sentence without naming the contradicted lines (claim-gates:15, 48, 67-68, 86 are contradicted, not merely lost).
3. No row anchors to a fixture for a gate behaviour the gate does not implement (E1 shows OPERATOR-GATED is a fixture-only fact).
4. The claims.json `after` text is not read as proof of faithfulness: 7/7 is reproduced on both the falsifier and the faithful tree.

## 6. Limitations

- No C1 drafts exist yet; I did not evaluate drafter wording.
- I only ran the committed gate and the counter; I did not run C2 counters beyond the frozen control re-run.
- The faithful-row list is my own oracle; it shows which claims the committed bytes support, not what the drafters will write.
- Token location cannot distinguish code from docstring from fixture; I verified this from code reading (`r46-c1-gate.py:117-121`), not by a docstring-anchor experiment.
- `recheck_line` reads only the first `recheck:` line (`r46-c1-gate.py:78-83`); a second line is invisible to the counter. Code reading only, not executed.
- The seat spec's quoted scorecard text `a recheck that fails closed on an absent base is an unsupported current claim` does NOT appear verbatim in `SCORECARD.md` (`grep -n` → no match). The nearest text is `SCORECARD.md:1540`: "A `gated` line is one that runs and fails closed, either on an absent base (`test -d ~/Projects/...`) or on a `LOST-RECORDED` anchor; it is an unsupported current claim until its base exists or its anchor is re-based." `SCORECARD.md:1545` is the distance paragraph. The re-basing route at 1540 is what makes faithful re-grounding a legitimate path.
- No installs, no tool upgrades, no git mutations, no writes outside this Report file and scratch (removed on exit).
