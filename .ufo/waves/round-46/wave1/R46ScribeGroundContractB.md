VERDICT: DRAFT-READY

Seat: R46ScribeGroundContractB (C1 re-ground drafter, contract, B; independent). Draft only; the L1 integrates and commits. No commit, push, index or git mutation; no shared production file touched; scratch removed.

Artifacts (drafts, not applied to the lane tree):
- .ufo/waves/round-46/wave1/R46ScribeGroundContractB.draft/tail.md (appended at the END of corpus/knowledge/claim-package-contract.md; heading `## Re-ground (round 46)` once; 21 rows G1-G21; 3-sentence lead paragraph naming the claims left historical)
- .ufo/waves/round-46/wave1/R46ScribeGroundContractB.draft/recheck-line.txt (replaces the entry's line 68 `recheck:` line)

Integration shape (verified in scratch; the entry's only changed bytes are line 68 plus the appended tail): `diff` of base 914ca0b6 entry against the scratch result printed `diff-hunk-count=1` (one hunk, `68c68,96`).

## Finding 1 — frozen counter and base bytes match the freeze record

Command: `sha256sum corpus/instruments/r46-c1-gate.py` (in scratch tree) and `grep -o 'c1-gate-sha256 [0-9a-f]*' .ufo/waves/round-46/freeze.txt`
Output:
```
b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294  corpus/instruments/r46-c1-gate.py
c1-gate-sha256 b0c730c834b4d7c6b16ac56f8c574ac599e8ae651aa02c5b2408fd736dd82294
```
Command: `git -C <lane> show 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba:corpus/instruments/claim-package-check.py | sha256sum`; the pure export file hashes to the same value (`8b6f849349157a91` prefix both). The pure export also matched base bytes for `corpus/knowledge/claim-package-contract.md` (`2233cd0637a69c11`), the exemplar manifest (`5e296a37ad0bbc16`), exemplar provenance (`c52b75f5390802da`) and exemplar report (`f99e2604eaafd0d2`).

## Finding 2 — do-nothing control fails closed; original recheck is gated

Command (scratch tree = unmodified pure base export, cwd = scratch root):
`python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md; echo "control-exit=$?"`
Output:
```
reground entry=claim-package-contract.md rows=0 ok=0 exit=1 read=section-count=0
control-exit=1
```
Command: `bash -c 'test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-package-contract.md'; echo "orig-recheck-rc=$?"`
Output: `orig-recheck-rc=1` (the entry's original line is gated today, as the counter's classify expects).

## Finding 3 — drafted entry passes the per-entry check

Procedure: copy pure export to scratch; copy r46-c1-gate.py into scratch corpus/instruments; replace the entry's last line (the `recheck:` line, index 68) with recheck-line.txt and append tail.md; run from the scratch root.
Command: `python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md; echo "exit=$?"`
Output (verbatim):
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
reground entry=claim-package-contract.md rows=21 ok=21 files=4 exit=0
exit=0
```
The `files=4` figure is the distinct anchor files: `corpus/instruments/claim-package-check.py` plus three exemplar fixtures (`evidence/manifest.json`, `provenance.json`, `report.md`).

## Finding 4 — every row is load-bearing (token blanked one by one)

Procedure: for each row, blank its token in a scratch copy of its anchor file (replace the token text with `#` characters; for the one multi-line token, G1, blank the anchored range lines — the same fallback the counter's L6 uses), run the per-entry check, restore the file, verify the entry is byte-identical afterwards.
Output (verbatim, final run):
```
rows_parsed=21
G1 `corpus/instruments/claim-package-check.py:101-108` mode=blank-lines rc=1 | row G1 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G2 `corpus/instruments/claim-package-check.py:305` mode=replace rc=1 | row G2 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G3 `corpus/instruments/claim-package-check.py:334` mode=replace rc=1 | row G3 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G4 `corpus/instruments/claim-package-check.py:354` mode=replace rc=1 | row G4 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G5 `corpus/instruments/claim-package-check.py:413-415` mode=replace rc=1 | row G5 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G6 `corpus/instruments/claim-package-check.py:407-409` mode=replace rc=1 | row G6 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G7 `corpus/instruments/claim-package-check.py:460` mode=replace rc=1 | row G7 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G8 `corpus/instruments/claim-package-check.py:457-458` mode=replace rc=1 | row G8 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G9 `corpus/instruments/claim-package-check.py:467` mode=replace rc=1 | row G9 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G10 `corpus/instruments/claim-package-check.py:471` mode=replace rc=1 | row G10 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G11 `corpus/instruments/claim-package-check.py:497` mode=replace rc=1 | row G11 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G12 `corpus/instruments/claim-package-check.py:515-516` mode=replace rc=1 | row G12 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G13 `corpus/instruments/claim-package-check.py:524-525` mode=replace rc=1 | row G13 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G14 `corpus/instruments/claim-package-check.py:527-528` mode=replace rc=1 | row G14 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G15 `corpus/instruments/claim-package-check.py:585-588` mode=replace rc=1 | row G15 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G16 `corpus/instruments/claim-package-check.py:607` mode=replace rc=1 | row G16 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G17 `corpus/instruments/claim-package-check.py:636-637` mode=replace rc=1 | row G17 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G18 `corpus/instruments/claim-package-check.py:634-635` mode=replace rc=1 | row G18 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=4 exit=1
G19 `corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json:2` mode=replace rc=1 | row G19 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=3 exit=1
G20 `corpus/instruments/fixtures/claim-package/exemplar/provenance.json:88` mode=replace rc=1 | row G20 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=3 exit=1
G21 `corpus/instruments/fixtures/claim-package/exemplar/report.md:88` mode=replace rc=1 | row G21 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=21 ok=20 files=3 exit=1
survivors=none
entry-restored-identical
```
Each blanked row flips the check to exit 1 with exactly that row at `ok=0`; no row survives.

## Finding 5 — aggregate counter: this entry is one of the two needed

Command: `python3 corpus/instruments/r46-c1-gate.py --root <scratch tree> --baseline /fast/scratch/hyaku/kasegi-r46/L1/pure --work <scratch>/tmp/agg; echo "agg-exit=$?"`
Output (verbatim):
```
gate L1 pass=0 read=gated=23 broken=0 lines=64/base=64
gate L2 pass=0 read=base-gated=24 regrounded=1 claim-package-contract.md
gate L3 pass=1 read=recheck-lines-clean=1
gate L4 pass=1 read=entry-mode-green=1
gate L5 pass=1 read=append-only=1
gate L6 pass=1 read=mutants=21 survivors=none
gate L7 pass=1 read=still-gated=23 changed=none
c1-gate fixed=5/7 exit=1
agg-exit=1
```
Reading: this entry alone moves gated 24 -> 23 and passes L3-L7 for itself. L1 (<=22) and L2 (>=2 regrounded) need the second entry (claim-gates.md, owned by the other C1 seat); with only this entry the aggregate correctly stays red. I did not re-ground claim-gates.md.

## Claims in the draft (what each row is anchored to)

Every row is a statement the entry makes (entry line in the claim column) anchored to committed bytes; full table is in tail.md. Summary: G1 six-file set (l.7, 11-16); G2-G6 manifest/polarity/redaction rules (l.13); G7-G10 custodian rules (l.14); G11-G14 provenance (l.15); G15-G16 status binding and reviewer distinctness (l.16); G17-G18 report marker and Scope excerpt heading (l.11); G19-G21 exemplar fixture instances of l.11/13/15 (conforming-instance rows, labelled as such).

Left historical (named in the section, not re-grounded): the round-13 boundary note on what the lost `ops/claim-check.mjs` reads (l.18-27, incl. the prose regex l.26); the DONE/APPROVED, claimable and state/verdict census semantics (l.29-54); the lost checker's validation command (l.56-62); the `OPERATOR-GATED` checklist marker (l.12), which no committed gate checks. Also: the reviewer-distinctness claim is re-grounded only in the narrow form the gate enforces (G16 says so).

## Limitations

- Draft only. Not applied to the lane tree; the L1 integrates, commits and re-runs the aggregate.
- Only this entry was re-grounded; the aggregate is red (L1, L2) until claim-gates.md is also re-grounded. I did not verify the other entry.
- G19-G21 are conforming-instance rows: the exemplar fixture shows the contract's words are satisfied; they do not prove the contract requires them. Gate-enforcement rows are G1-G18.
- G12/G13 anchor presence / format only; the gate's remote, commit-length and 64-hex checks sit on adjacent lines (518-523, 525) that the token does not pin. G18 confirms only the heading, not the excerpt's composition (gate does not check it).
- G1's token is multi-line; the per-row mutation used the counter's blank-lines fallback (anchored range blanked), not a single-token replace.
- The per-entry check reads anchors only inside the scratch tree; no live target, no network.
- Not run: the full `--selftest` of claim-package-check.py and the other lane checks; they are outside this seat's item.
- Tooling: none installed or upgraded (no pacman, no uv, no npm); standard python3/bash only.
- Scratch removed (`rm -rf` of the seat scratch root; `test ! -e` confirmed).
