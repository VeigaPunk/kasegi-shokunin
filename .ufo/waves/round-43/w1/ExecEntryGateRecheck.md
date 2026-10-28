# ExecEntryGateRecheck — receipt (kasegi-shokunin round 43, seat ExecEntryGateRecheck)

Base `ab98fac9dce87130bc4f66de89e30650d63943dc`. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(read-only to this seat except the wave dir). Measured lane head `5b4a8503fd7ab1ccf5bcb0630763db8ab73d211d`
(the round-43 C2 files were committed when the final runs were made). Scratch
`/fast/scratch/hyaku/kasegi-r43/ExecEntryGateRecheck/` — removed after the copy, verified absent below.

## Deliverables (landable bytes only)

| path | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-43/w1/ExecEntryGateRecheck.entry-fix.txt` | 1 | 570 | `fbee7c32f17a1566e6e25653c0ccafeb0d494688a5189b6e99c5534b78adc26d` |
| `.ufo/waves/round-43/w1/ExecEntryGateRecheck.transcript.txt` | 110 | — | `0b6a0518a64d7852c8fadba8e6f4bbf9fe1b629228903e2dfda2037fea32252e` |

`entry-fix.txt` is exactly the line `corpus/knowledge/claim-package-gate.md` now carries after `recheck: `
(the scribe appended a `# fails closed` note to the command I supplied; this deliverable is the landed
bytes, so the entry and the deliverable agree byte for byte; the first 447 bytes are the bare command).

## The line (one shell line, cd-prefixed)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -s corpus/knowledge/claim-package-gate.md && set -o pipefail && python3 corpus/instruments/claim-package-check.py --selftest | grep -x 'selftest cases=10 failures=0' && python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar | grep -x 'package=corpus/instruments/fixtures/claim-package/exemplar rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0'  # fails closed: a missing gate, a selftest that stops grading ten cases, or an exemplar that stops passing exits non-zero
```

Line count 1, newline count 1. `bash -n -c` exit 0. No `;`-separated prose; every step is one `&&`
chain; `set -o pipefail` keeps each pipeline's real status; `grep -x` pins the *whole* summary and
verdict lines, which is what makes the output digest cwd-stable (the selftest prints no tempdir or
absolute path, verified).

Why it is a real recheck and not a degenerate line:

- names its own entry (`test -s corpus/knowledge/claim-package-gate.md`) — audit `own` limb;
- names the committed instrument `corpus/instruments/claim-package-check.py` — audit `instrument` limb;
- `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin` is the audited root — audit `cdroot` limb;
- re-derives the gate's two headline results (ten graded cases green, exemplar `rules=8 pass=8`);
- runs, and exits 0 on the delivered tree (below), not merely fail-closed.

## Measured evidence (all in the transcript, commands and outputs)

Lane state at measurement: `git rev-parse HEAD` → `5b4a8503fd7ab1ccf5bcb0630763db8ab73d211d`;
`sha256sum` → gate `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` (the
ExecGateCore bytes, internals renamed `_GATE_RULE_*` so the companion cannot collide), companion
`04951ca0e72050725fc01a16ba1e42d7a52bd29bb0ae653b164a39ed39b57b17`, entry
`f53109d842b185ed49ca599fda221351caf03df9d3443c5d50c8bb19a0cb5940`; `fixture_dirs=9`;
`expected_list_has_entry=1`.

1. Lane-root run: `cd <lane> && bash -c "<line>"` → exit 0, stdout
   `selftest cases=10 failures=0` + `package=corpus/instruments/fixtures/claim-package/exemplar rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`,
   stdout sha256 `30ca9575c2811abaa0f77abedeb22fdccf475dc37596961979efef4e458f33ed`.
2. Foreign-cwd runs from `/` and `/tmp`: exit 0 each, same stdout sha256
   `30ca9575c2811abaa0f77abedeb22fdccf475dc37596961979efef4e458f33ed` — the audit's cwd limb holds.
3. Mutant: `cp -a <lane>/corpus $S/mut/corpus`, then one inserted always-pass branch at the top of the
   per-rule loop:
   ```
       for rule_id in _GATE_RULE_ORDER:
   +       if rule_id == 'R-REPORT':
   +           results.append({'id': rule_id, 'verdict': 'pass', 'detail': 'forced-pass'}); continue
           try:
   ```
   Gate sha moves `8b6f8493…` → `dae79bd4407aeda67289bf164d9713bae131d9052761a0491bafd64edc5c4609`.
   The mutation is real: the mutant gate now prints `RULE R-REPORT verdict=pass detail=forced-pass` and
   `verdict=WELL-FORMED exit=0` on `defect-8-marker` (the R-REPORT defect fixture). The line against the
   mutant exits **1** from both the mutant root and `/`, 0 stdout bytes; the unfiltered companion selftest
   shows `selftest case=8 … expected=R-REPORT observed=none verdict=fail` and `selftest cases=10 failures=1`.
4. Restore: mutant tree deleted; the lane's gate sha is unchanged (`8b6f8493…` before and after); the
   line at the lane root exits 0 again.
5. `recheck-audit.py --quiet` at the lane root after landing:
   ```
   strict pass=62/62 cdroot_fail=0 instrument_fail=0 own_fail=0
   executes=38 gated=24 broken=0
   lines=62 total=62 pass=62 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
   expect=present expected=62 missing=0 unexpected=0 exit=0
   ```
   New entry's record from `--json`: `frozen=111 strict=111111 lane_exit=0 foreign_exit=0 class=executes`
   (the line executes under the audit, every frozen and strict limb green).
6. Pre-landing measurement by this seat at `2026-10-28T16:52:07Z`, before the entry existed:
   `strict pass=61/61 … lines=61 total=61 pass=61 … expect=present expected=61 missing=0 unexpected=0 exit=0`.
   So the entry **is** counted: `expected` moves 61 → 62 when the file lands, and the post-landing run
   above is that after-state (the entry is the 62nd, executing, not merely listed).
7. Integration robustness: the line was also measured with the selftest pasted into the gate (pre-landing
   staged tree, gate sha `441f75513bb7e86efa23d538a48cbe81cd4e4eb5e6ad369e2bea8cf3fecc9704`) — identical
   output and digest `30ca9575…`. The current landing is companion mode; both satisfy the line.

## Risks / notes for the L1

- The line deliberately binds exact output strings (`selftest cases=10 failures=0`, the exemplar verdict
  line). Renaming `defect-<k>` fixture dirs, moving the exemplar, or reworded summaries reds the line —
  that is the intended fail-closed behaviour, not a defect to paper over.
- If the gate is later landed with the selftest pasted in, the gate sha changes (the entry's cited
  `bdb50a82…` class of hash); the line still passes (measured in 7), but any receipt that pins the
  companion gate sha must pin the landed one.
- The trailing `# fails closed` note is inside the same shell line; it is inert and the audit parses the
  line as one command (`bash -n` 0). Dropping it would not change any limb.
- `knowledge-expected.txt` must keep the entry (it did at measurement: `expected_list_has_entry=1`);
  otherwise the audit reports `unexpected=corpus/knowledge/claim-package-gate.md` and reds.

## Discipline

- Writes: only the two deliverables above plus scratch; no lane corpus file, no fleet-root file, no PATH
  directory touched. Scratch removed; `test -e` shows absent.
- No git/jj mutation anywhere; lane git use was read-only (`rev-parse`, `status`).
- No tooling installed; pacman not run; no network fetch needed.

## Coordination

- Told `ScribeKnowledgeGate` the exact line (message `15b829ce…`); it deployed it verbatim with the
  trailing note and confirmed the summary format; re-confirmed the landed 570-byte line's re-measurement.
- `ExecGateSelftest` confirmed `selftest cases=10 failures=<k>` is the whole summary line, that a mutant
  gate reds the cases whose rule it breaks, and that no tempdir/absolute path reaches stdout.
