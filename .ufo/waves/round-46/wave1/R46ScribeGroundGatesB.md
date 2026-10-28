VERDICT: DRAFT-READY

# R46ScribeGroundGatesB — C1 re-ground drafter for corpus/knowledge/claim-gates.md (independent, draft only)

Scope: draft the round-46 re-ground of `corpus/knowledge/claim-gates.md` onto committed bytes, prove it with the frozen counter `corpus/instruments/r46-c1-gate.py` in a scratch copy, and falsify the counter's per-entry mode. Nothing was committed, staged or edited in the lane, the fleet repo or any shared file. Scratch (`/fast/scratch/hyaku/kasegi-r46/R46ScribeGroundGatesB/`) is removed on exit.

## Drafts written (the only files this seat wrote in the lane)

- `.ufo/waves/round-46/wave1/R46ScribeGroundGatesB.draft/tail.md`: the verbatim text to append after the entry's last line (leading blank line, then `## Re-ground (round 46)`, a three-sentence intro, a 25-row table `| id | current claim | committed anchor | token |`, and a historical-claims paragraph).
- `.ufo/waves/round-46/wave1/R46ScribeGroundGatesB.draft/recheck-line.txt`: one line that replaces the entry's round-22 `recheck:` line (entry line 125):
  `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md`

Application to the entry (for L1 integration): keep base lines 1-124 byte-identical, replace line 125 with the recheck line, append `tail.md`. The scratch proof used exactly this construction (checked: `head -n 124` of base equals the first 124 lines of the scratch entry; `tail -n +126` equals `tail.md`; line 125 equals `recheck-line.txt`).

## Finding 1 — the re-ground check passes on the scratch tree (positive proof)

Attacked: the drafted entry `claim-gates.md` (base 125 lines + replaced recheck + tail), counter per-entry mode, scratch root = copy of `/fast/scratch/hyaku/kasegi-r46/L1/pure` with the frozen counter copied in.

Command (run from the scratch root, `TMPDIR` set explicitly):
`cd $S/tree && TMPDIR=$S/tmp python3 -I corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md`; `echo "entry-exit=$?"`

Output (verbatim):
```
entry-exit=0
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
reground entry=claim-gates.md rows=25 ok=25 files=4 exit=0
```
The `reground ... exit=0` line is the required shape. Rows span four anchor files: `corpus/instruments/claim-package-check.py` (22 rows), `corpus/instruments/fixtures/claim-package/defect-7-reviewer/status.json` (G19), `.../exemplar/report.md` (G21), `.../exemplar/custodian-receipts.json` (G25).

Note on the first attempt: G21 was first anchored at `report.md:86-90`; the counter printed `G21 ok=0 read=range-past-eof` (the file has 88 lines) and the run exited 1. That was a drafting error, corrected to `:84-88` in both the draft and the scratch copy; the output above is after the fix.

## Finding 2 — do-nothing control and fabricated-token control discriminate

Do-nothing (base export with no section, same counter):
`cd $S/base && python3 -I $S/tree/corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md --root $S/base`
Output: `reground entry=claim-gates.md rows=0 ok=0 exit=1 read=section-count=0` (exit 1).

Fabricated token (harness control, G1 token replaced in the scratch entry by `zz-fabricated-token-9911`, then restored):
Output: `CONTROL fabricated-token rc=1 | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1` and `CONTROL fabricated-token row1=row G1 ok=0 read=token-not-in-lines`.

So the check is red on a missing section and on an absent token, and green only on the drafted rows.

## Finding 3 — every row is load-bearing (per-row blanking, 25 of 25 red)

Attacked: each row's token, blanked in a scratch copy of its anchored file by the same rule the counter's L6 uses (replace all occurrences with `#`, or blank the anchored line range if the token only matches after normalisation). The anchored file was restored byte-for-byte after each mutant and the restore was checked by sha256 (`restore-bad=none`). Harness: `$S/harness.py`.

Output (verbatim from the final run):
```
harness rows=25
MUTANT G1 anchor=corpus/instruments/claim-package-check.py token="'custodian-receipts.json'," how=replace-all rc=1 | row G1 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G2 anchor=corpus/instruments/claim-package-check.py token='not isinstance(sequence, (int, float))' how=replace-all rc=1 | row G2 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G3 anchor=corpus/instruments/claim-package-check.py token='if positive < 1:' how=replace-all rc=1 | row G3 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G4 anchor=corpus/instruments/claim-package-check.py token='first.lower() == second.lower() == recorded.lower()' how=replace-all rc=1 | row G4 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G5 anchor=corpus/instruments/claim-package-check.py token='producer.strip().casefold() == verifier.strip().casefold()' how=replace-all rc=1 | row G5 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G6 anchor=corpus/instruments/claim-package-check.py token="decision.get('scope_signal') != 'NO_SCOPE_OBJECTION'" how=replace-all rc=1 | row G6 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G7 anchor=corpus/instruments/claim-package-check.py token="for key in ('input_sha256', 'decision_sha256'):" how=replace-all rc=1 | row G7 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G8 anchor=corpus/instruments/claim-package-check.py token='head.lower() != final_digest.lower()' how=replace-all rc=1 | row G8 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G9 anchor=corpus/instruments/claim-package-check.py token='head.lower() != head_expected.lower()' how=replace-all rc=1 | row G9 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G10 anchor=corpus/instruments/claim-package-check.py token='if recorded.lower() != actual:' how=replace-all rc=1 | row G10 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G11 anchor=corpus/instruments/claim-package-check.py token='if actual != recorded.lower():' how=replace-all rc=1 | row G11 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G12 anchor=corpus/instruments/claim-package-check.py token='if real != root and not real.startswith(root + os.sep):' how=replace-all rc=1 | row G12 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G13 anchor=corpus/instruments/claim-package-check.py token='if os.path.islink(os.path.join(dirpath, name)):' how=replace-all rc=1 | row G13 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G14 anchor=corpus/instruments/claim-package-check.py token='if st.st_size > MAX_SCAN_BYTES:' how=replace-all rc=1 | row G14 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G15 anchor=corpus/instruments/claim-package-check.py token="with open(full, 'rb') as handle:" how=replace-all rc=1 | row G15 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G16 anchor=corpus/instruments/claim-package-check.py token="raise _GateFail('hits=%d,first=%s,shape=%s'" how=replace-all rc=1 | row G16 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G17 anchor=corpus/instruments/claim-package-check.py token="failing = [key for key in HARD_GATE_KEYS if hard.get(key) != 'PASS']" how=replace-all rc=1 | row G17 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G18 anchor=corpus/instruments/claim-package-check.py token='if identity.strip().casefold() in _identities(manifest):' how=replace-all rc=1 | row G18 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G19 anchor=corpus/instruments/fixtures/claim-package/defect-7-reviewer/status.json token='"identity": "exec-exemplar-package"' how=replace-all rc=1 | row G19 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
MUTANT G20 anchor=corpus/instruments/claim-package-check.py token='if NO_SUBMISSION not in text:' how=replace-all rc=1 | row G20 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G21 anchor=corpus/instruments/fixtures/claim-package/exemplar/report.md token='No submission performed' how=replace-all rc=1 | row G21 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
MUTANT G22 anchor=corpus/instruments/claim-package-check.py token="SCOPE_EXCERPT = re.compile(r'scope\\s+excerpt', re.IGNORECASE)" how=replace-all rc=1 | row G22 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G23 anchor=corpus/instruments/claim-package-check.py token='if not isinstance(agents, list) or not agents:' how=replace-all rc=1 | row G23 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G24 anchor=corpus/instruments/claim-package-check.py token='if not isinstance(chain, list) or not chain:' how=replace-all rc=1 | row G24 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
MUTANT G25 anchor=corpus/instruments/fixtures/claim-package/exemplar/custodian-receipts.json token='"scope_signal": "NO_SCOPE_OBJECTION"' how=replace-all rc=1 | row G25 ok=0 read=token-not-in-lines | reground entry=claim-gates.md rows=25 ok=24 files=3 exit=1
mutants=25 survivors=none restore-bad=none
CONTROL fabricated-token rc=1 | reground entry=claim-gates.md rows=25 ok=24 files=4 exit=1
CONTROL fabricated-token row1=row G1 ok=0 read=token-not-in-lines
```
25 mutants, 25 red (`rc=1`), no survivors, every anchor restored to its pre-mutation sha256.

## Finding 4 — the frozen counter and its freeze record agree (falsification of the instrument itself)

Command: `sha256sum corpus/instruments/r46-c1-gate.py`. Output begins `b0c730c834b4d7c6b16a…`. The freeze record `.ufo/waves/round-46/freeze.txt` pins `c1-gate-sha256 b0c730c834b4d7c…`. The copy placed in scratch has the same digest. The counter is the frozen one.

## Finding 5 — the aggregate counter with this entry alone does NOT reach the C1 target (honest negative)

Do-nothing aggregate (base vs base; counter run from the scratch root):
`python3 -I $S/tree/corpus/instruments/r46-c1-gate.py --root $S/base --baseline $S/base --work $S/work`
Output (verbatim):
```
gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64
gate L2 pass=0 read=base-gated=24 regrounded=0 
gate L3 pass=0 read=recheck-lines-clean=0
gate L4 pass=0 read=entry-mode-green=0
gate L5 pass=0 read=append-only=0
gate L6 pass=0 read=mutants=0 survivors=none
gate L7 pass=1 read=still-gated=24 changed=none
c1-gate fixed=1/7 exit=1
```
This matches the freeze control's do-nothing expectation (`c1-gate fixed=1/7 exit=1`).

Aggregate with the drafted claim-gates re-ground applied to the scratch tree (`--root $S/tree --baseline $S/base`):
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
So this entry alone moves gated 24 -> 23 and re-grounds one entry; L1 needs gated <= 22 and L2 needs at least two re-grounded entries. C1 closes only when the second intended entry (`claim-package-contract.md`, another seat's draft) is also re-grounded. The limbs L3-L7 hold for this entry on its own.

## Finding 6 — the committed gate, run on its own fixtures, agrees with the rows it anchors

Commands and outputs (scratch tree; same bytes as the lane's committed gate):
- `python3 -I corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar | tail -n 1` gives `package=corpus/instruments/fixtures/claim-package/exemplar rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`.
- `python3 -I corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/defect-7-reviewer | grep -E 'R-STATUS|verdict=DEFECT'` gives `RULE R-STATUS verdict=fail detail=reviewer=not-distinct` and `package=corpus/instruments/fixtures/claim-package/defect-7-reviewer rules=8 pass=7 fail=1 verdict=DEFECT exit=1`.

These support G19 (the defect-7 reviewer identity is the producer, and the gate refuses it) and G25/G21 (the exemplar's decisions and marker are the passing instance).

## Rows and what each one does NOT claim

The 25 rows are in `tail.md`. Where the committed bytes are narrower than the entry's wording, the row says so instead of stretching:
- G15: the entry says "read as UTF-8"; the committed scan reads raw bytes (`open(full, 'rb')`, `claim-package-check.py:676`).
- G17: the entry says every hard gate is `PASS`; the committed check enforces that only under `claimable: true` (lines 612-614).
- G22: the entry's `/scope excerpt/i` is matched as `scope\s+excerpt` in committed bytes.
- G23: the entry's `steps`/`transitions`/`agents` disjunction is `agents` only in committed bytes.

Left historical, not claimed by any row (named in the tail): the `made` alternative of the no-submission marker; the `OPERATOR-GATED` check on `claim_checklist.md` (no committed `.py` gate tests it; the fixtures carry the marker as text only); the `transitions`/`steps` alternatives; the single secrets regex and its UTF-8 reading (committed: six byte-level patterns, `claim-package-check.py:135-142`); the `HARD_STOP` double error; the `state === 'DONE'` and `claimable === true` requirements and their `finding_count` reading; the `outcome === 'APPROVED'` and `kx-reviewer` checks; the global prior-submission scan; the blocker-field and nested-readiness checks; and the claim-index and prepare-claims sections.

## Limitations

- The counter proves that each token is present in its anchored lines and that blanking it turns the check red. It does not prove the gate behaves as the row's sentence says. The rows' semantic fit is my reading; a non-author should check G15, G17, G22 and G23 hardest, because those are where the committed bytes are narrower than the entry.
- I did not verify the second intended entry (`claim-package-contract.md`). The C1 aggregate target (gated <= 22, two re-grounds) is therefore not met by this draft alone; it needs that entry too.
- The scratch tree is a copy of the pure base export plus the frozen counter, not the live lane. The entry was also run only against the scratch root, as the seat spec requires.
- I ran the freeze's do-nothing control and did not re-run the other freeze controls (`controls/freeze-controls.txt`); those belong to other seats or to the L1 integration.
- The recheck line contains the absolute `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin` that the spec mandates. The counter's `~/` and `$HOME` check runs after the `cd` prefix is stripped, and it passed (`recheck-lines-clean=1`).
- Installed or upgraded tools: none. Commits, pushes and git mutations: none. Shared files, fleet repo and sibling lanes: untouched.
