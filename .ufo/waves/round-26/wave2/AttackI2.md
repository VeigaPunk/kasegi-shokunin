# AttackI2 — report: row-deletion sensitivity (falsify C1/C2 after-states)

- Seat: `L1Kasegi26.AttackI2` (leaf; no subagent dispatch). Round 26, wave 2.
- Date: 2026-10-25 (UTC). Lane: `kasegi-shokunin`; lane root
  `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
- Attack target: the claimed AFTER states that (1) the S041 registry row,
  (2) the F11 knowledge entries, (3) the F11 README row, each exert a gate-red
  effect on the three named gates (census exit / frontier exit / awk count).
- Method: three isolated scratch copies (byte-identical, rsync; `.git`
  excluded), one primitive per copy, run against the same three gates as the
  committed tree. Committed tree untouched. Full evidence: `.ufo/waves/round-26/wave2/i2.md`.

## Results

| Removal (scratch only) | Census exit | Frontier exit | awk count | Gate(s) red |
|---|---|---|---|---|
| committed / pristine (none) | 0 | 0 (14/14) | 11 | none |
| S041 row from `corpus/SOURCES.md` | **0** | **0** (14/14) | 11 | **none — survives all three gates** |
| one F11 entry from `corpus/knowledge/` | **1** (E11 `S041 missing used-by …`) | **1** (`FileNotFoundError`, uncaught) | 11 | **census + frontier** |
| F11 row from `corpus/README.md` | 0 | 0 (12/12) | **10** | **awk count** |

## Verdict

- Assignment items (2) and (3) are each caught by at least one gate: (2) by
  census (E11 used-by) and frontier (entry-file presence, uncaught
  `FileNotFoundError`); (3) by the awk count (11 → 10).
- Assignment item (1) — deleting the S041 row from SOURCES — reddens **none**
  of the three gates. The census's E11 limb only checks used-by paths of
  *present* mined rows; the frontier harness binds F11 entries to the round-26
  manifest/snapshot, not to the registry; the awk count reads only README. So
  the row-deletion sensitivity claim fails for the measured gate set: this is a
  surviving mutant / coverage gap (the gate set has no arm asserting "every
  `--source S###` cited by an admitted entry has a registry row"), recorded as
  a finding, not as permission to change the contract.
- Committed state: nothing missing — census exit 0, frontier 0 (14/14), awk 11,
  and C1 live audit `c1-live.json` 39/39 with `missing=0 unexpected=0`.
- No production edits, no gate changes, no VCS mutations. Scratch trees only.
- Tooling: no installs performed (pacman transactions untouched; no uv/npx/
  cargo/official-binary installs).
- Evidence files: `/tmp/i2/{base-committed,base-scratch,m1-sources,m2-entry,m3-readme}-{census,frontier,awk}.out`; restoration hashes in `i2.md`.
