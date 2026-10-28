VERDICT: DRAFT-READY

Seat: R46ScribeGroundContractA (C1 re-ground drafter, `corpus/knowledge/claim-package-contract.md`). Draft only: nothing in the live tree was edited, no git/jj mutation, nothing committed. Drafts are at `.ufo/waves/round-46/wave1/R46ScribeGroundContractA.draft/`:
- `tail.md` — the text to APPEND at the end of the entry: one `## Re-ground (round 46)` heading, a three-sentence scope paragraph, and table `| id | current claim | committed anchor | token |` with rows G1..G22.
- `recheck-line.txt` — one line: `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md`

## Finding 1 — the anchors are committed bytes (base and freeze)

The seat checked that every anchor file the rows cite has the same bytes at the frozen base, in the working tree and in the pure export. Command: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba:<path> | sha256sum` (and the same for the working file and `/fast/scratch/hyaku/kasegi-r46/L1/pure/<path>`). Output:

```
corpus/knowledge/claim-package-contract.md base=2233cd0637a69c11 work=2233cd0637a69c11 pure=2233cd0637a69c11
corpus/instruments/claim-package-check.py base=8b6f849349157a91 work=8b6f849349157a91 pure=8b6f849349157a91
corpus/instruments/fixtures/claim-package/exemplar/report.md base=f99e2604eaafd0d2 work=f99e2604eaafd0d2 pure=f99e2604eaafd0d2
corpus/instruments/fixtures/claim-package/exemplar/status.json base=60f06dfebc04e419 work=60f06dfebc04e419 pure=60f06dfebc04e419
corpus/instruments/fixtures/claim-package/exemplar/provenance.json base=c52b75f5390802da work=c52b75f5390802da pure=c52b75f5390802da
corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json base=5e296a37ad0bbc16 work=5e296a37ad0bbc16 pure=5e296a37ad0bbc16
```

Freeze commit `9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5` also carries the entry at the same bytes as the base (`2233cd0637a69c11`) and carries `corpus/instruments/r46-c1-gate.py` (`sha256` prefix `b0c730c834b4d7c6`, identical to the working file and to the scratch copy). At the base rev the counter itself is absent (`git cat-file -e 914ca0b…:corpus/instruments/r46-c1-gate.py` → "absent-at-base"), so the counter is a round-46 freeze artifact, not a base artifact.

## Finding 2 — the rows are the entry's own claims, each on a committed anchor

Scope of the CURRENT claims (entry line numbers are the entry's own):
- l.7 and table l.9-16 (six files), l.11 (literal marker), l.13 (manifest rules: schema, polarity, ≥1 positive, redaction receipts, `redactions:[]`, evidence-relative paths, symlink), l.14 (custodian: `matched_grant_id`, `scope_signal`, head binding), l.15 (`external_effects_performed: []`, pin, `policy_sha256`), l.16 (`manifest_sha256` binding; `claim_review` reviewer distinctness), l.42 (`claimable` bool), l.45 (`finding_count` when claimable), l.52 and l.54 (`hard_gates` and `subchecks` names).

Anchor kinds: 18 rows on `corpus/instruments/claim-package-check.py` (the round-43 gate; ranges of at most 8 lines), 4 rows on exemplar fixture files under `corpus/instruments/fixtures/claim-package/exemplar/` (`report.md:88`, `provenance.json:88`, `evidence/manifest.json:2`, `status.json:3`). Five distinct anchor files, four of them non-.py fixture files.

The tail's three-sentence scope paragraph names the historical lines (l.19-27 lost-checker parity and prose regex; l.31-51 census lines; l.58-62 Validation; l.64-67 Provenance; the l.11 verbatim-excerpt wording that the gate does not check) and says every other line is a `[lost-tree]`/`[lost-base]` observation, not a current claim. G6 is explicitly partial: the gate refuses an empty `redactions[]`, which is only the necessary half of "never claim-ready".

Spot evidence (command `sed -n '<a>,<b>p'` on the anchor; output verbatim):
- `claim-package-check.py:457-461` → line 460: `        if decision.get('scope_signal') != 'NO_SCOPE_OBJECTION':` (G9 token `decision.get('scope_signal') != 'NO_SCOPE_OBJECTION'`)
- `claim-package-check.py:181-182` → `        if stat.S_ISLNK(st.st_mode):` / `            return None, 'symlink'` (G8)
- `exemplar/status.json:3` → ` "manifest_sha256": "5e296a37ad0bbc16253ab756a2543c579bce864a0af3bcff6bfe20db317fc834",` and `sha256sum exemplar/evidence/manifest.json` → `5e296a37ad0bbc16253ab756a2543c579bce864a0af3bcff6bfe20db317fc834  …/exemplar/evidence/manifest.json` (G22 holds in full)

## Finding 3 — the recheck line passes on the scratch tree (proof)

Scratch: `$HYAKU_SCRATCH/kasegi-r46/R46ScribeGroundContractA/work` = copy of the pure export, plus `corpus/instruments/r46-c1-gate.py` copied in, plus the entry with the recheck line replaced in place and `tail.md` appended. Command, run from the scratch root with `TMPDIR` set explicitly:

```
python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md
```

Output (exit 0):

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
reground entry=claim-package-contract.md rows=22 ok=22 files=5 exit=0
```

Recheck-line textual check on the entry (`grep -c '^recheck:'` → 1; the line now reads `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md`). The recheck line contains no `~/` and no `$HOME`; the only `/home/` is the stripped `cd` prefix that the counter's `CD_RE` removes before its HOME check.

## Finding 4 — each row token is load-bearing (one token blanked per run, scratch copy only)

For each row, its token was replaced by `#` characters in the scratch copy of its anchor file, the entry gate was run, and the file was restored before the next row. Each run printed the row line and the summary line below, verbatim (the driver script is in scratch and is removed on exit):

```
G1 blanked=corpus/instruments/claim-package-check.py:101-108 rc=1 | row G1 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G2 blanked=corpus/instruments/claim-package-check.py:305-305 rc=1 | row G2 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G3 blanked=corpus/instruments/claim-package-check.py:332-335 rc=1 | row G3 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G4 blanked=corpus/instruments/claim-package-check.py:354-355 rc=1 | row G4 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G5 blanked=corpus/instruments/claim-package-check.py:413-415 rc=1 | row G5 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G6 blanked=corpus/instruments/claim-package-check.py:366-367 rc=1 | row G6 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G7 blanked=corpus/instruments/claim-package-check.py:336-336 rc=1 | row G7 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G8 blanked=corpus/instruments/claim-package-check.py:181-182 rc=1 | row G8 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G9 blanked=corpus/instruments/claim-package-check.py:457-461 rc=1 | row G9 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G10 blanked=corpus/instruments/claim-package-check.py:469-472 rc=1 | row G10 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G11 blanked=corpus/instruments/claim-package-check.py:527-529 rc=1 | row G11 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G12 blanked=corpus/instruments/fixtures/claim-package/exemplar/provenance.json:88-88 rc=1 | row G12 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=4 exit=1
G13 blanked=corpus/instruments/claim-package-check.py:585-589 rc=1 | row G13 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G14 blanked=corpus/instruments/claim-package-check.py:607-608 rc=1 | row G14 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G15 blanked=corpus/instruments/claim-package-check.py:123-128 rc=1 | row G15 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G16 blanked=corpus/instruments/claim-package-check.py:129-129 rc=1 | row G16 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G17 blanked=corpus/instruments/claim-package-check.py:609-611 rc=1 | row G17 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G18 blanked=corpus/instruments/claim-package-check.py:617-619 rc=1 | row G18 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G19 blanked=corpus/instruments/claim-package-check.py:121-121 rc=1 | row G19 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=5 exit=1
G20 blanked=corpus/instruments/fixtures/claim-package/exemplar/report.md:88-88 rc=1 | row G20 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=4 exit=1
G21 blanked=corpus/instruments/fixtures/claim-package/exemplar/evidence/manifest.json:2-2 rc=1 | row G21 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=4 exit=1
G22 blanked=corpus/instruments/fixtures/claim-package/exemplar/status.json:3-3 rc=1 | row G22 ok=0 read=token-not-in-lines | reground entry=claim-package-contract.md rows=22 ok=21 files=4 exit=1
survivors=none
```

After the loop the restored scratch entry passed again: `reground entry=claim-package-contract.md rows=22 ok=22 files=5 exit=0` (rc 0 captured with `|| rc=$?`).

## Finding 5 — do-nothing control discriminates

Control: the base entry (`git show 914ca0b…:corpus/knowledge/claim-package-contract.md`, no tail, old recheck line) through the same gate, same counter bytes:

```
reground entry=claim-package-contract.md rows=0 ok=0 exit=1 read=section-count=0
```
rc=1. The gate is not vacuous: it fails on a missing section and passes only once the 22 rows are present and every token is located.

Also: `diff base-entry.md scratch-entry.md` shows one removed line (the old recheck at line 68) and the appended section; `grep -c '^<'` over the diff output is 1, so the change is append-only except the recheck line, as L5 requires.

## Integration notes for L1 (required, not optional)

- The old `recheck:` line sits at line 68 and must be REPLACED in place by `recheck-line.txt`, not supplemented. The counter reads the first `recheck:` line (`recheck_line()` returns the first match); a second line would leave the old lost-tree line in charge and the entry would still count as gated.
- Apply the tail AFTER the replaced recheck line; `tail.md` begins with the blank line that separates it from the Provenance block.
- The live-tree recheck command starts with `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin`; the scratch proof ran the identical argv from the scratch root (the counter strips the `cd` prefix when it classifies). The live path itself was not executed because the live entry is not yet mutated (drafts only).

## Limitations

- The rows show that the committed round-43 gate (and its exemplar fixtures) still carry the rule text the entry quotes. They do not show that the gate matches the lost `ops/claim-check.mjs` or the lost `~/Projects/bounties/fleets/mission-template.md`; those sources remain `[lost-tree]` and are not re-verified.
- "Current" here means the committed instrument still encodes the entry's rule. For G6 the committed support is only the refusal of an empty `redactions[]`; "never claim-ready" beyond that is not re-grounded.
- The blanking test blanks one token per run in one file copy; it does not test cross-row interactions, and the blanking driver was run from scratch only.
- Anchor byte equality was checked by sha256 prefix (16 hex) for the six files listed; the full exemplar manifest digest was checked separately (`5e296a37…fc834`).
- The counter-bytes comparison used the sha256 prefix only (16 hex); it does not prove the full digest equality.
- No installs or tool upgrades were made by this seat.
- Scratch `$HYAKU_SCRATCH/kasegi-r46/R46ScribeGroundContractA/` was removed on exit (`test -e` → gone).
