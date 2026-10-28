# ExecCoverageMapNote — receipt (round 43, wave 1, leaf)

Seat: `ExecCoverageMapNote`, role executor (leaf). Lane `kasegi-shokunin`; base
`ab98fac9dce87130bc4f66de89e30650d63943dc`; lane HEAD at work `4cb6d4a`; work UTC
`2026-10-28T16:48Z`–`16:50Z`. Item: one append-only note for `corpus/README.md` recording that the
six-file claim-package contract moved from documentation-only to an instrumented surface, with no
frontier-row change and no change to the measured ratio.

## Deliverables (in `.ufo/waves/round-43/w1/`)

| File | lines | bytes | sha256 |
|---|---|---|---|
| `ExecCoverageMapNote.append.md` (landable bytes only) | 12 | 914 | `77db2f8b18f4f6496e92c02f7e5451a92109615c566e575dd0b0cd760a7ca09c` |
| `ExecCoverageMapNote.transcript.txt` (evidence) | 136 | 5864 | `6df8bb39e6b64646d508035e660489789d42be74d47b7a5fadc5b34e8b5f69be` |

Landing: `cat .ufo/waves/round-43/w1/ExecCoverageMapNote.append.md >> corpus/README.md`. Byte 1 of the
block is `\n` (the blank-line separator), so the landed README gets exactly one blank line between
the round-42 paragraph and the new `##` section, matching the existing section seam.

## The block (12 lines, exactly the landable text; no fences, no tabs, max line 99 chars)

It states that the coverage map and the frontier table are not edited in place (R6); that the map's
`Claim-package contract` row has so far been documentation-only — `knowledge/claim-package-contract.md`,
whose `ops/claim-check.mjs` went with `~/Projects/bounties` — and names the three new surface members:
the gate `instruments/claim-package-check.py` (eight rules, one `RULE <id> verdict=` line each), the
fixtures `instruments/fixtures/claim-package/exemplar/` plus nine one-delta `defect-1-missing-file`
through `defect-9-secret`, and the entry `knowledge/claim-package-gate.md`. It closes with the explicit
claim: **NO frontier row (F01-F25) changes and the measured ratio is unchanged — 25/25 admitted, still
0 of 18 lost-domain surfaces present.**

## Evidence (full command/output pairs in the transcript)

- `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → **25** (before), and on the scratch copy after the
  append → **25**; the block itself matches 0 times (it introduces no frontier row).
- `wc -c/-l` on the block → **914 bytes, 12 lines**; `sha256sum` →
  `77db2f8b18f4f6496e92c02f7e5451a92109615c566e575dd0b0cd760a7ca09c`; max line length 99; first byte
  `\n`; fence count 0.
- Append simulation (`cp corpus/README.md` → scratch `README.after.md`, then `cat block >>`):
  bytes 58224 → 59138 (+914); lines 600 → 612 (+12); sha256 before
  `bb897bf07b3e6e14706817679be49450d98bba28be313bce7362965b3ba29a6b`, after
  `82dedcea2055d9425179addd11fe17ef0a5abdc17be5f9cb4322e9fe742f40b6`; frontier-row count 25 → 25;
  fence-line count 2 → 2 (no imbalance); `##` headings 17 → 18 (one new section);
  `head -c 58224 README.after.md | cmp - README.before.md` → exit 0 (byte-identical prefix: pure EOF
  append, no existing line touched).
- `python3 corpus/instruments/frontier-recheck-count.py` → exit 0,
  `FRONTIER-CENSUS rows=25 admitted=25 closed=25 problem-rows=0 registry=66`,
  `entries=28 pass=28 exit=0`. The ratio the block cites (rows/admitted/closed 25/25/25) is unchanged;
  the lane's `registry=` counter is not a frontier-ratio input and is not cited in the block.
- Grounding of the names used in the block: `grep -oE 'R-[A-Z]+' .ufo/waves/round-43/w1/ExecGateCore.rules.txt
  | sort -u | wc -l` → **8** (R-FILES, R-MANIFEST, R-REDACT, R-CUSTODIAN, R-PROVENANCE, R-STATUS,
  R-REPORT, R-NOSECRET); `ls -d .ufo/waves/round-43/w1/ExecGateFixtures.defect-* | wc -l` → **9**
  (`defect-1-missing-file`, `-2-digest`, `-3-negative`, `-4-escape`, `-5-redaction`, `-6-custodian`,
  `-7-reviewer`, `-8-marker`, `-9-secret`, matching `ExecGateFixtures.index.txt` one-to-one);
  `grep -o 'corpus/knowledge/claim-package-gate.md' .ufo/waves/round-43/claims.json | head -1` →
  `corpus/knowledge/claim-package-gate.md` (frozen C2 claim and `ScribeKnowledgeGate` item target).
  The map row text the note names is the committed `corpus/README.md:11`
  `| Claim-package contract | \`knowledge/claim-package-contract.md\` | \`fleets/mission-template.md\` + live packages |`.

## Bounds and hygiene

- `corpus/README.md` was **not** modified by this seat: it is still 600 lines, sha256
  `bb897bf07b3e6e14706817679be49450d98bba28be313bce7362965b3ba29a6b`, 25 frontier rows (re-read at the
  end of the run). The append was exercised only on a scratch copy.
- Writes limited to the two wave-1 deliverables above and this receipt; scratch
  `/fast/scratch/hyaku/kasegi-r43/ExecCoverageMapNote/` held every work copy and was removed before
  yielding (`rm -rf`; verified absent). `TMPDIR` was not relied on.
- No mutating git/jj command anywhere; the only git use was `git -C <lane> rev-parse --short HEAD` and
  read-only `git status --porcelain` (showed only round-43 wave untracked files created by the wave,
  unchanged by me) and `git check-ignore` (`corpus/instruments/__pycache__` is gitignored and its .pyc
  mtimes are 2026-10-26 — my harness run added no bytecode there).
- No host/fleet-root/`shokuknow` writes, no PATH directory write, no tool installation (nothing needed;
  no pacman, no `uv`). No service restarts. No subagent spawn.
- No sibling wave file was edited: `ExecGateCore.*`, `ExecGateFixtures.*`, `ScribeKnowledgeGate.*`
  (not yet written by its seat) are untouched.

## Risks / notes for the L1

1. Landing order: the note names `corpus/instruments/claim-package-check.py`,
   `corpus/instruments/fixtures/claim-package/{exemplar,defect-*}` and
   `corpus/knowledge/claim-package-gate.md`. Land it only after those paths exist, or the README will
   cite paths the judged head does not carry (K4-style declaration mismatch would then be visible).
2. The block is exactly 12 lines including the leading separator and the heading; re-appending it twice
   yields a duplicate section and breaks the "one note" reading — append once, byte-exact
   (sha256 `77db2f8b…`).
3. The block deliberately does not cite the registry counts, `CORPUS`-census numbers, or S067/S068: those
   move at landing (`registry=66` → 68) and are not frontier-ratio inputs; the ratio statement is
   restricted to rows/admitted/closed (25/25/25) and the README's own 0/18 lost-domain figure.
4. No blocker. Item complete: one landable EOF block, its measured shape, and the transcript with all
   real outputs.
