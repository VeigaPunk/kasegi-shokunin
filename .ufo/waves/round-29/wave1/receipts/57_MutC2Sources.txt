# MutC2Sources — mutation probe of registry row bytes (round 29, wave 1)

- Seat: MutC2Sources (leaf, no delegation). Date: 2026-10-25.
- Claim attacked: C2 (coverage) — "sources census exits 0" as a detector over `corpus/SOURCES.md` row bytes.
- Detector (same bounded command for pristine, mutated and restored bytes):
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/corpus/SOURCES.md`
  (script = fleet root `scripts/sources-census.sh`, conforming to SOURCES-CONTRACT-v1; selftest-green instrument, bash+gawk only).
- Subject bytes: `corpus/SOURCES.md` snapshot taken 2026-10-25, sha256
  `fa54ba528eadc032e3cf0cbc6f431e683b2d0d5e7bc1123dd5bb874ac92d1836`, 45 registry rows (S001–S045).
  **Not PRE-STATE**: the round-29 rows S043 (HackerOne policy set, docs/A/mined), S044 (Bugcrowd VRT README, docs/A/mined)
  and S045 (Bugcrowd VRT CWE crosswalk, dataset/A/mined) were already landed at probe time, opened 2026-10-25,
  used-by `corpus/knowledge/program-severity-ladders-and-reward-scales.md` (present, 7583 B). No re-run pending on this probe.
- Scratch: `/tmp/mutc2r29/` — one pristine `base` case + one isolated case per mutant; every case root carries
  copies of all 16 distinct used-by targets so the pristine detector run is self-contained. The lane repo was never written.

## Baseline (pristine, all 8 cases)

Exit 0, `file ok <path>`, with only the lane's two disclosed W04 warnings
(`W04 S028 duplicate url docs.hackerone.com/... across scopes`, `W04 S029 duplicate url eur-lex.europa.eu/... across scopes`).
Baseline passes ⇒ kills below are conclusive, not baseline artifacts.

## Mutants and verdicts

| # | Mutant (exact byte edit) | Expected | Actual detector output (exit) | Verdict |
|---|---|---|---|---|
| M1 | duplicate S043 id: S044 row id `S044`→`S043` (one byte) | E03, exit 1 | `E03 S043 duplicate id` (1) | **KILLED** |
| M1b | belt-and-braces variant: full S043 row duplicated (row inserted before S044) | E03 (+E04) | `E03 S043 duplicate id` + `E04 S043 duplicate url hackerone.com/security/policy_versions within scope …` (1) | **KILLED** |
| M2 | literal `\|` inserted inside S043 teaches cell (`caps severity \| and reward`) | E01, exit 1 | `E01 S043 fields=12` (1) — NF 13→14, reported as data fields NF−2=12 vs the required 11 | **KILLED** |
| M3 | S043 opened `2026-10-25`→`25/10/2026` (non-ISO) | E08, exit 1 | `E08 S043 opened=25/10/2026` (1) | **KILLED** |
| M4 | S043 used-by → `corpus/knowledge/absent-mutc2-probe.md` (nonexistent; row is status=mined, so the path check applies) | E11, exit 1 | `E11 S043 missing used-by corpus/knowledge/absent-mutc2-probe.md` (1) | **KILLED** |
| M5 | set tier C on the community-kind row (S027, the registry's only `community` row) | "caught" per tasking | mutated bytes == pristine bytes (sha256 unchanged `fa54ba52…`); detector output identical to baseline, exit 0 | **NOT KILLED — vacuous no-op (survivor)** |
| M5ctl | adjacent control, run to localize M5: S027 tier `C`→`A` | E10, exit 1 | `E10 S027 community-at-A` (1) | **KILLED** |

Mutant digests (sha256 of mutated `corpus/SOURCES.md`): M1 `ed0840c93767652a149de720fc0dd8503bd0c6778d0094812af46ddd1af28cc7`,
M1b `5aefaeea0450c511f8927dffdf41460face2d4064853bc09b831c6b4cf31593a`, M2 `aee1f5564a292e241127c476c4fe5c6a180d00233e3c39e85ecb92b9cde291a0`,
M3 `7e40ac585ce67a4e307eba986ebc1f21f034b024122563af421dab12278f070b`, M4 `4810f8d134219ac0be0e8c22ec3be9988e5a3cbce24ae2a66a2683c6b422c927`,
M5ctl `deb44dbbc5978cd55ff56b5311b1e4a20850af7e7005d7200c571b2083bea692`.

## M5 analysis — coverage finding, not a contract change

M5 as assigned cannot be caught, by construction rather than by detector weakness:

1. The registry's only community-kind row, S027, is **already tier C** (`| community | C | … | rejected | 2026-10-19 | 180d | — |`),
   so "set tier C" mutates zero bytes (`mut_sha == base_sha`) and the detector trivially returns the baseline verdict.
2. SOURCES-CONTRACT-v1's only kind×tier rule is "community is never tier A", enforced as E10. Community at B/C is
   contract-legal — S027-at-C sits inside the accepted clean baseline, so **no E-code can exist for community-at-C**
   without changing the contract. The tasking's "each mutant must be caught" fails for M5 because the mutant state is
   the baseline state, not because validation is broken.
3. The adjacent control proves the policed limb works: C→A is killed immediately by `E10 S027 community-at-A`, exit 1.
   If any downstream reader believed "community ⇒ must not be tier C" was an enforced invariant, this probe falsifies
   that belief; the enforced invariant is exactly "community ≠ A".

## Restoration evidence

After each mutated run the pristine bytes were restored from the untouched `base` copy and re-probed:

| Case | restored sha256 | restored run |
|---|---|---|
| m1, m1b, m2, m3, m4, m5, m5ctl | `fa54ba528eadc032e3cf0cbc6f431e683b2d0d5e7bc1123dd5bb874ac92d1836` (== pristine) | exit 0, `file ok` — RESTORED_OK ×7 |

No mutation survived in the lane (all work was in `/tmp/mutc2r29/`); the lane file was only read. No sibling source,
jj state, Git index, `.ufo/state/`, watchdog log, MANIFEST or template was touched. No tools were installed or
upgraded (bash/gawk/coreutils sufficed), so there is nothing to record under the 2026-10-19 tooling authorization.
Probe is model-independent (pure shell), so no answering-model note applies (bound 8 n/a).

## Extra observations (measured, zero-cost)

- E01 reports the data-field count (`fields=12`), i.e. pipes−2, not the raw pipe count — read it as "11 expected".
- A full-row duplication (M1b) trips both E03 and E04 (same URL+scope, non-rejected, no `supersedes S###` in teaches);
  the single-byte id retarget (M1) isolates E03 alone. Either shape kills.
- The two W04 warnings on S028/S029 are present in pristine and every mutant and never move the exit — consistent with
  "warnings do not affect clean lanes" and with the lane's disclosed W04 baseline.
- The `## Paths` section's non-S-shaped rows produce no E12 on the snapshot.
