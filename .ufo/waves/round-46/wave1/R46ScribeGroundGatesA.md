VERDICT: DRAFT-READY

Scope: C1 re-ground drafter (gates, A) for `corpus/knowledge/claim-gates.md`. Drafts only; the L1 integrates and commits. Nothing in the lane was committed, staged or edited. No tools were installed or upgraded.

Drafts written (builder draft dir only):
- `.ufo/waves/round-46/wave1/R46ScribeGroundGatesA.draft/tail.md`: the `## Re-ground (round 46)` section, 25 rows (G1-G25), appended at the end of the entry. Anchors: `corpus/instruments/claim-package-check.py` (22 rows), `corpus/instruments/fixtures/claim-package/defect-8-marker/expected-rule:1` (G24), `corpus/instruments/fixtures/claim-package/defect-9-secret/expected-rule:1` (G25).
- `.ufo/waves/round-46/wave1/R46ScribeGroundGatesA.draft/recheck-line.txt`: one line, replaces the entry's line 125 `recheck:` (the lost-tree `anchorcheck.py` line). It has no `~/` or `$HOME`.

Scratch: `$HYAKU_SCRATCH/kasegi-r46/R46ScribeGroundGatesA/` (`/fast/scratch/hyaku/...`), built from a copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure` with the frozen counter copied in. Scratch removed on exit.

## Finding 1: the per-entry check passes on the drafted entry

Command (scratch root, after applying `head -n 124` of the entry, then `recheck-line.txt`, then `tail.md`):
`python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md`

Output, verbatim:
```
row G1 ok=1 read=token-located
row G2 ok=1 read=token-located
row G3 ok=1 read=token-located
row G4 ok=1 read=token-located
row G5 ok=1 read=token-located
row G6 ok=1 read=token-located
row G7 ok=1 read=token-located
row G8 ok=1 read=token-located
row G9 ok=1 read=token-located
row G10 ok=1 read=token-located
row G11 ok=1 read=token-located
row G12 ok=1 read=token-located
row G13 ok=1 read=token-located
row G14 ok=1 read=token-located
row G15 ok=1 read=token-located
row G16 ok=1 read=token-located
row G17 ok=1 read=token-located
row G18 ok=1 read=token-located
row G19 ok=1 read=token-located
row G20 ok=1 read=token-located
row G21 ok=1 read=token-located
row G22 ok=1 read=token-located
row G23 ok=1 read=token-located
row G24 ok=1 read=token-located
row G25 ok=1 read=token-located
reground entry=claim-gates.md rows=25 ok=25 files=3 exit=0
exit=0
```

Recheck line after apply (grep -n '^recheck:'):
`125:recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md`

## Finding 2: do-nothing control discriminates

Command: same per-entry command on the unmodified pure base entry (no section).
Output: `reground entry=claim-gates.md rows=0 ok=0 exit=1 read=section-count=0` then `exit=1`.

## Finding 3: every row's token is load-bearing (blank each token in a scratch anchor copy, one at a time)

Method: for each row, the token is replaced with `#` characters in the anchored scratch file (token-replaced; the range-blank fallback was never needed), the per-entry check is run, the file bytes are restored and checked against the original bytes. Output, verbatim:
```
rows-parsed=25
baseline (unmutated) exit=0 last=reground entry=claim-gates.md rows=25 ok=25 files=3 exit=0
G1 | corpus/instruments/claim-package-check.py:101-108 | token="'custodian-receipts.json'," | token-replaced | exit=1 | row G1 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G2 | corpus/instruments/claim-package-check.py:307-309 | token='isinstance(sequence, (int, float))' | token-replaced | exit=1 | row G2 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G3 | corpus/instruments/claim-package-check.py:332-335 | token="elif artifact.get('polarity') != 'negative':" | token-replaced | exit=1 | row G3 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G4 | corpus/instruments/claim-package-check.py:340-347 | token='actual = hashlib.sha256(handle.read()).hexdigest()' | token-replaced | exit=1 | row G4 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G5 | corpus/instruments/claim-package-check.py:354-355 | token='if positive < 1:' | token-replaced | exit=1 | row G5 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G6 | corpus/instruments/claim-package-check.py:407-409 | token='first.lower() == second.lower() == recorded.lower()' | token-replaced | exit=1 | row G6 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G7 | corpus/instruments/claim-package-check.py:413-416 | token='producer.strip().casefold() == verifier.strip().casefold()' | token-replaced | exit=1 | row G7 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G8 | corpus/instruments/claim-package-check.py:460-461 | token="decision.get('scope_signal') != 'NO_SCOPE_OBJECTION'" | token-replaced | exit=1 | row G8 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G9 | corpus/instruments/claim-package-check.py:469-472 | token='if head.lower() != head_expected.lower():' | token-replaced | exit=1 | row G9 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G10 | corpus/instruments/claim-package-check.py:465-467 | token='head.lower() != final_digest.lower()' | token-replaced | exit=1 | row G10 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G11 | corpus/instruments/claim-package-check.py:584-589 | token='actual = hashlib.sha256(manifest_bytes).hexdigest()' | token-replaced | exit=1 | row G11 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G12 | corpus/instruments/claim-package-check.py:598-606 | token="if not isinstance(reviewer.get('fallback'), bool):" | token-replaced | exit=1 | row G12 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G13 | corpus/instruments/claim-package-check.py:607-608 | token='if identity.strip().casefold() in _identities(manifest):' | token-replaced | exit=1 | row G13 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G14 | corpus/instruments/claim-package-check.py:612-613 | token="failing = [key for key in HARD_GATE_KEYS if hard.get(key) != 'PASS']" | token-replaced | exit=1 | row G14 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G15 | corpus/instruments/claim-package-check.py:614-614 | token="failing += [key for key in SUBCHECK_KEYS if subchecks.get(key) != 'PASS']" | token-replaced | exit=1 | row G15 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G16 | corpus/instruments/claim-package-check.py:617-619 | token='if isinstance(count, bool) or not isinstance(count, int) or count < 1:' | token-replaced | exit=1 | row G16 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G17 | corpus/instruments/claim-package-check.py:140-140 | token="('credential', re.compile(rb'(?i)" | token-replaced | exit=1 | row G17 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G18 | corpus/instruments/claim-package-check.py:656-660 | token='os.walk(pkg.root, followlinks=False)' | token-replaced | exit=1 | row G18 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G19 | corpus/instruments/claim-package-check.py:672-674 | token='if st.st_size > MAX_SCAN_BYTES:' | token-replaced | exit=1 | row G19 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G20 | corpus/instruments/claim-package-check.py:185-187 | token='if real != root and not real.startswith(root + os.sep):' | token-replaced | exit=1 | row G20 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G21 | corpus/instruments/claim-package-check.py:120-120 | token="re.compile(r'scope\\s+excerpt', re.IGNORECASE)" | token-replaced | exit=1 | row G21 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G22 | corpus/instruments/claim-package-check.py:121-121 | token="NO_SUBMISSION = 'No submission performed'" | token-replaced | exit=1 | row G22 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G23 | corpus/instruments/claim-package-check.py:489-491 | token='if not isinstance(agents, list) or not agents:' | token-replaced | exit=1 | row G23 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
G24 | corpus/instruments/fixtures/claim-package/defect-8-marker/expected-rule:1-1 | token='R-REPORT' | token-replaced | exit=1 | row G24 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=2 exit=1
G25 | corpus/instruments/fixtures/claim-package/defect-9-secret/expected-rule:1-1 | token='R-NOSECRET' | token-replaced | exit=1 | row G25 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=2 exit=1
mutants=25 all-nonzero=True
restore-check: entry+anchors unchanged after loop; baseline again: (0, 'reground entry=claim-gates.md rows=25 ok=25 files=3 exit=0')
fabricated-token control: rows-rewritten=25 exit=1 last=reground entry=claim-gates.md rows=25 ok=0 files=0 exit=1
entry restored; baseline exit=0 last=reground entry=claim-gates.md rows=25 ok=25 files=3 exit=0
```

## Finding 4: the frozen aggregate counter with this single re-ground (scratch tree vs pure base)

Command: `python3 corpus/instruments/r46-c1-gate.py --root . --baseline /fast/scratch/hyaku/kasegi-r46/L1/pure --work <scratch>/tmp/agg` (scratch tree).
Output, verbatim:
```
gate L1 pass=0 read=gated=23 broken=0 lines=64/base=64
gate L2 pass=0 read=base-gated=24 regrounded=1 claim-gates.md
gate L3 pass=1 read=recheck-lines-clean=1
gate L4 pass=1 read=entry-mode-green=1
gate L5 pass=1 read=append-only=1
gate L6 pass=1 read=mutants=25 survivors=none
gate L7 pass=1 read=still-gated=23 changed=none
c1-gate fixed=5/7 exit=1
```
Reading: this entry alone takes gated 24 to 23, but the L1 target is at most 22 and L2 needs at least two re-grounded entries. The C1 closure therefore needs the second entry (`claim-package-contract.md`, the other seat's item) re-grounded as well. This draft does not do that and does not claim it.

## Finding 5: frozen do-nothing control reproduces the freeze record

Command: same aggregate on a copy of the pure base with the counter (`--root . --baseline <pure>`).
Output: `gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64` ... `c1-gate fixed=1/7 exit=1` `exit=1`. This matches `.ufo/waves/round-46/controls/freeze-controls.txt` lines 1-10 exactly.

Counter integrity: `sha256sum corpus/instruments/r46-c1-gate.py` printed `b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294`, and `git show 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5:corpus/instruments/r46-c1-gate.py | sha256sum` printed the same digest. This matches `c1-gate-sha256` in `freeze.txt`.

## Finding 6: the committed gate behaves as the witness rows and the anchored rules say

Command: `python3 corpus/instruments/claim-package-check.py <fixture>` for the exemplar and each defect, compared to each `expected-rule`.
Output (verbatim lines):
```
package=corpus/instruments/fixtures/claim-package/exemplar rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
selftest cases=10 failures=0
defect-1-missing-file expected=R-FILES failed=[R-FILES ]
defect-2-digest expected=R-MANIFEST failed=[R-MANIFEST ]
defect-3-negative expected=R-MANIFEST failed=[R-MANIFEST ]
defect-4-escape expected=R-MANIFEST failed=[R-MANIFEST ]
defect-5-redaction expected=R-REDACT failed=[R-REDACT ]
defect-6-custodian expected=R-CUSTODIAN failed=[R-CUSTODIAN ]
defect-7-reviewer expected=R-STATUS failed=[R-STATUS ]
defect-8-marker expected=R-REPORT failed=[R-REPORT ]
defect-9-secret expected=R-NOSECRET failed=[R-NOSECRET ]
```

## What the re-ground says, and what it leaves historical

Current claims (table rows G1-G23): each restates one entry claim with its entry line, narrowed where the committed gate is narrower (G13, G14, G15, G16, G17, G21, G22, G23). G24-G25 are witnesses only: the committed fixture names the failing rule, and the gate's behaviour is shown by the rule rows and by Finding 6, not by the witness itself.

Left historical (named in the section): the `OPERATOR-GATED` checklist marker (L16), the `made` alternative (L15), the `steps`/`transitions` alternatives (L41), the one-regex `bearer` form (L48), the error-set caveat (L59-61), the triage pointer (L63), every status.json gate not in the table (L67-91, including `state === 'DONE'`, `claim_review.outcome`, `claim_ready`, `producer_identity`, the `kx-reviewer` role, the not-claimable heuristics, the prior-submission guard and global scan, blocker fields, nested readiness), the HARD_STOP double-error (L32-34), and the `claim-index.mjs` / `prepare-claims.mjs` notes (L93-119).

## Limitations

- The per-entry check is a substring check of a token in the anchored lines. The blanking run shows each token is load-bearing for that check. It does not show that the gate code enforces the claim beyond what the anchored lines say; that reading is mine.
- Finding 4 shows that this draft alone does not close C1 (L1 and L2 fail). I did not draft `claim-package-contract.md`.
- I did not verify the frozen `claims.json` sha256 or the other frozen controls (only the counter and the do-nothing control).
- Scratch was removed on exit; the draft files and this report are the only artifacts. Commit, push and any mutating git/jj command were not run.
