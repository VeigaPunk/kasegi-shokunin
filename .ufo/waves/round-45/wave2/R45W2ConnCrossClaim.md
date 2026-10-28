VERDICT: HOLDS
Scope: predicate-level causal separability of C1 and C2 holds in both directions on the export of 6662a4276b6f7bd61e23e12058414e09dd71b9e4. Artifact-level independence does NOT hold: the two claims share pinned bytes (claims.json, manifest.json) and one census-validated table (SOURCES.md). Findings F4-F6 record the stale control pointer and the missing selftest wiring.

Seat: R45W2ConnCrossClaim (leaf, read-only; no installs, no git mutation, no edits to the lane tree).

## Method
1. Export: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 6662a4276b6f7bd61e23e12058414e09dd71b9e4 | tar -x -C <scratch>/exp`. Base export: `git archive dc5bb8c6e31efc4a6650819df85e79b72fd64bcd` into `<scratch>/base`.
2. Fixture trees, built by copying the export and reverting files to the base bytes or deleting the listed artifacts:
   - `c1only` (C1 without C2): SOURCES.md minus the `| S071 |` row (line 77); corpus/README.md, PROVINCE.md and corpus/instruments/knowledge-expected.txt reverted to base; `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` and `corpus/source-snapshots/round-45/S071.txt` deleted. S072 row, round-44 correction (line 205), QUALITY R47-R49 (lines 380-382), SKILL/README rows, freeze-check.py and the refiled receipt kept.
   - `c2only` (C2 without C1): SOURCES.md minus the `| S072 |` row (line 78); corpus/lessons/round-44.md, corpus/QUALITY.md, SKILL.md, corpus/instruments/README.md reverted to base; `corpus/instruments/freeze-check.py` and `.ufo/waves/round-44/controls/final-attempt3-refiled.txt` deleted. S071 row, F27 README row, knowledge entry, S071 snapshot kept.
   - `base` = the do-nothing control.
3. Counters run with the exported (v1.1) copies, TOOL_ROOT = the export, `--root` set to each tree:
   `python3 <exp>/corpus/instruments/r45-routed-defects.py --root <T> --baseline <base>`
   `python3 <exp>/corpus/instruments/r45-c2-gate.py --root <T>`

## Results (verbatim counter output)
| tree | C1 counter | C2 gate |
|---|---|---|
| base (do-nothing) | `routed-defects total=5 fixed=0 unresolved=5 exit=1` | `c2-gate fixed=1/7 exit=1` |
| exp (landed tree) | `routed-defects total=5 fixed=5 unresolved=0 exit=0` | `c2-gate fixed=7/7 exit=0` |
| c1only | `routed-defects total=5 fixed=5 unresolved=0 exit=0` | `c2-gate fixed=1/7 exit=1` |
| c2only | `routed-defects total=5 fixed=0 unresolved=5 exit=1` | `c2-gate fixed=7/7 exit=0` |

Base matches the frozen expect_before values exactly (`routed-defects total=5 fixed=0 unresolved=5 exit=1`; `c2-gate fixed=1/7 exit=1`). Do-nothing discriminates: 0/5 and 1/7 on base, full score only when the claim's own artifacts are present.

C1 limb detail on c2only: `limb R1 fixed=0 read=row-S072=absent`, `limb R2 fixed=0 read=quality-not-append-only-or-unchanged`, `limb R3 fixed=0 read=registry-section-absent`, `limb R4 fixed=0 read=freeze-check-absent`, `limb R5 fixed=0 read=refiled-absent`. Every C1 limb fails exactly because the C2-only deletion removed a C1 artifact it needs; C1 does not fall for any reason it could not have been predicted from the deletion list.

C2 gate detail on c1only: `gate G1 pass=0 read=rows=26 admitted=26 dup=0`, `gate G3 pass=0 read=row-S071=absent-or-malformed`, `gate G4 pass=0 read=recheck-rc=2 quotes-ok=0 frozen-cores-missing=0`, `gate G7 pass=1 read=census-rc=0 ok-line=1`.

## Causal separability: verdict per claim
- C1 verifies without C2 artifacts: YES (c1only 5/5). The F27 row, knowledge entry, S071 row and S071 snapshot are not inputs to any R-limb.
- C2 verifies without C1 artifacts: YES (c2only 7/7). The S072 row, round-44 correction, QUALITY R47-R49, SKILL/README rows, freeze-check.py and the refiled receipt are not inputs to any G-gate.
- Separable at predicate level, but not at artifact level. See F1-F3.

## Findings: coupling (what ties the two claims together)

F1. claims.json is a shared pinned file, and C1 R4 depends on the C2 claim's bytes.
- Evidence: `corpus/instruments/r45-routed-defects.py:73` pins `"claims.json": "bbe40503..."`; R4 at lines 282-288 checks `sha(cb) != PINS["claims.json"]`, then replays the claims with `freeze-check.py --claims ... --tool-root TOOL_ROOT --base base` (line 286). `freeze-check.py:15` renders each claim's counter_cmd with {tree}=base, so R4 also replays the C2 gate at base.
- Test V1 (claims.json with the C2 claim removed, otherwise c1only): `limb R4 fixed=0 read=claims-not-the-frozen-bytes` and `routed-defects total=5 fixed=4 unresolved=1 exit=1`.
- Consequence: C1's 5/5 requires that the C2 claim (its counter_cmd, expect_before "c2-gate fixed=1/7 exit=1") sit in the frozen claims file and replay at base. C1 is not separable from C2's claim text, although it is separable from C2's artifacts.

F2. manifest.json is a shared pinned file, and C2 G4 depends on the S072 entry that C1 uses.
- Evidence: `corpus/instruments/r45-c2-gate.py:60` pins `"manifest.json": "125339d9..."`; G4 (lines 223-235) checks that pin. C1 R1 (lines 168-172) runs source-recheck on the S072 entry in the same file. The landed manifest holds `['S071', 'S072']`.
- Test V2 (c2only with the S072 entry removed from manifest.json, sha becomes 5ccae63d...): `gate G4 pass=0 read=manifest-not-the-pinned-bytes`; `c2-gate fixed=6/7 exit=1`.
- Test V3 (c1only with the S071 entry removed from manifest.json): C1 stays `fixed=5`; C2 G4 gives `manifest-not-the-pinned-bytes`. So the asymmetry is: C1 does not need S071 entries, but C2's pin covers the whole file including C1's S072 entry.
- Test V4 (c2only with corpus/source-snapshots/round-45/S072.txt deleted): C2 still `fixed=7/7`. C2 does not need the S072 snapshot, only the S072 bytes inside the pinned manifest.

F3. SOURCES.md is one table, and the census validates the whole file, so a row of either claim can fail the other.
- C1 R1 reads only the S072 row and requires the S070 row byte-identical to base (line 149, 164-167). C2 G3 reads only the S071 row (line 200). C2 G7 runs `bash <census> validate --file corpus/SOURCES.md` (line 273), which validates every row.
- Test V6 (c2only plus one malformed line appended at the end of SOURCES.md): `gate G7 pass=0 read=census-rc=1 ok-line=0`; `c2-gate fixed=6/7 exit=1`; census printed `file	E12	S999 row outside Registry section`, rc=1. The census does honor `--file` (the exp registry printed `file	ok	.../exp/corpus/SOURCES.md`), so the gate does grade the tree passed in.
- Direction: C2's G7 depends on C1's rows; C1 never calls census. Asymmetric.

F4. The frozen control pointer carries pre-hardening (v1) numbers, not the v1.1 numbers the landed counters print.
- claims.json C2 `control` field and freeze.txt line 4 name `.ufo/waves/round-45/controls/freeze-controls.txt` (measured-at 2026-10-28T20:55:13Z). That file's blob at freeze commit 8cf62c8 is 2685584a...; its rows are `control c2-junk-row counter=C2 c2-gate fixed=4/7 exit=1 ...` and `control c2-fabricated-quote counter=C2 c2-gate fixed=5/7 exit=1 ...`.
- The v1.1 control file (`freeze-controls-v1.1.txt`, added in 6662a42, blob 3f4081e3...) prints `fixed=2/7` and `fixed=3/7`.
- I re-ran `python3 <exp>/.ufo/waves/round-45/controls/freeze-controls.py --base-export <base> --lane <exp> --work <scratch>` and it printed `control c2-junk-row counter=C2 c2-gate fixed=2/7 exit=1 expect=RED got=RED`, `control c2-fabricated-quote counter=C2 c2-gate fixed=3/7 exit=1 expect=RED got=RED`, `controls total=5 red=5 green=0`. So v1.1 reproduces the v1.1 file, not the frozen file.
- Kill rule: every control is still RED under v1.1, so the kill rule is not tripped. But the pinned claims.json cannot be updated without changing its sha (bbe405...), so the cited control evidence for v1.1 lives only in a file the claim does not point to.

F5. Counters changed after the freeze commit; the claims file did not. Predicates are unchanged by name.
- C1 counter: v1 sha 82004c700decbc3453baa57919ccff71cbfe322a8d2a71b558d75951c24f04ee (8cf62c8) -> v1.1 680c881af4a5f9a660c203c7a9e7e44e5ba4a860870e0d655121709e34f2fb67 (6662a42).
- C2 gate: v1 sha 5e0796168cfe09f1e7db1b270a4f563cb40516c676d2c5c7921b46cd70730082 (8cf62c8) -> v1.1 639a038a99bdd19d1ae612b45cff63a5631b4b2e5fc7e727e9e5f78339c205f2 (6662a42).
- claims.json sha bbe40503... is identical at 8cf62c8 and 6662a42.
- Predicate names: v1 and v1.1 are identical by name and by docstring line (C1: R1-R5 at lines 10, 16, 22, 28, 31 in both; C2: G1-G7 at lines 10, 13, 15, 18, 20, 26, 27 in both). The v1.1 erratum E1 keeps the predicate names, which is the kill-rule allowance for "bug fixes that keep the predicate". Not a violation, but the graded bytes are not the frozen bytes; the freeze record names "counters ... committed in the same commit", which is the v1 commit.

F6. The selftests that SKILL.md and corpus/instruments/README.md register for both counters are not in the landed tree.
- SKILL.md:1154-1155 and corpus/instruments/README.md:996-997 name `corpus/instruments/r45-counters-selftest-c1.py` and `corpus/instruments/r45-counters-selftest-c2.py` as the self-test with `--selftest`.
- `ls corpus/instruments` in the export lists `r45-c2-gate.py` and `r45-routed-defects.py` only. The only copies are under `.ufo/waves/round-45/wave1/R45ExecSelftestC1.draft/` and `.ufo/waves/round-45/wave1/R45ExecSelftestC2.draft/`.
- The counters reject the flag: `python3 r45-routed-defects.py --selftest --root ... --baseline ...` -> `unrecognized arguments: --selftest`, rc=2; `python3 r45-c2-gate.py --selftest` -> rc=2 (argparse, `--root` required). So the registered self-test column does not run on the landed tree. This is a verifiability defect in the registry rows, owned by the SKILL/instruments-README coupling, not by the counters' predicates.

F7. Census is an unpinned host file outside the repo and is clock-dependent. Not C2-specific in its clock behavior.
- `r45-c2-gate.py:56` sets `CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`; it is not in PINS (lines 58-62) and is not in the lane tree. sha256 at scan time: 3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30.
- Census validates against the current date by default. `bash <census> validate --today 2026-10-27 --file <exp>/corpus/SOURCES.md` printed `file	E08	S064 opened=2026-10-28` and `file	E08	S065 opened=2026-10-28` and rc=1; `--today 2026-10-28` rc=0. The base registry shows the same behavior (`--today 2026-10-27 --file <base>/corpus/SOURCES.md` -> `E08 S064 opened=2026-10-28`, rc=1), so the clock dependence predates round 45. G7 therefore passes today and can fail tomorrow on the base rows too.

F8. Nominal coupling only (checked, no predicate coupling).
- SKILL.md and corpus/instruments/README.md: C1 R3 requires the `## Round-45 Gates & probes registry addition` section and three rows (r44-frontier-count.py, r44-routed-defects.py, wave-registry.py) and the r44 README row (r45-routed-defects.py:262-268). It does not read the `r45-c2-gate.py` rows. Test V5 (c1only with the `| r45-c2-gate.py |` rows removed from SKILL.md and the instruments README): `routed-defects total=5 fixed=5 unresolved=0 exit=0`. Coupling is file-level only.
- QUALITY.md: read only by C1 R2. c2only reverts QUALITY.md to base and C2 stays 7/7.
- corpus/README.md: read only by C2 G1 (frontier rows). c1only reverts it to base and C1 stays 5/5.
- corpus/lessons/round-44.md: read only by C1 R1. c2only reverts it and C2 stays 7/7.
- corpus/instruments/knowledge-expected.txt line 37 (the F27 entry) is not read by either counter. corpus/instruments/recheck-audit.py:45-47 documents the file as a consumer. Not graded here.
- freeze-check.py: C1 R4 only (plus the replay of C2's counter in F1).

## Pattern summary (cross-claim)
| shared file | read by C1 | read by C2 | coupling type | evidence |
|---|---|---|---|---|
| claims.json | R4 (sha pin + replay of both claims) | counter_cmd/expect in the replay | pinned bytes, bidirectional in content | F1, V1 |
| manifest.json | R1 (S072 entry via source-recheck) | G4 (whole-file sha pin) | pinned bytes, C2 pins C1's entry | F2, V2, V3, V4 |
| SOURCES.md | R1 (S072 row, S070 row identical) | G3 (S071 row), G7 (whole-file census) | one table; census gates all rows | F3, V6 |
| census (fleet file) | none | G7 | unpinned external script, clock-dependent | F7 |
| SKILL.md, instruments README | R3 (section and 3+1 rows) | none graded | file-level, nominal | F8, V5 |
| QUALITY.md, corpus/README.md, lessons/round-44.md | R2, none, R1 | none, G1, none | file-level only | F8 |

## Limitations
- Trees were built by file-level reverts and deletions of the listed artifacts. The C1-only tree keeps the S071 manifest entry (dangling: the snapshot is removed), and the C2-only tree keeps the S072 snapshot and manifest entry. These are the minimal edits the seat spec named; other removal choices would change V2-V4 results but not the main separability result.
- I ran the counters from the export's copy (TOOL_ROOT = export), as the instruments require; I did not run the tree-local copies.
- freeze-check's replay was observed only through R4's `base_ok=2` line; I did not run freeze-check standalone on the fixtures.
- I did not run the round-44 counters, the census selftest, or the non-author closure. I did not re-run the wave-1 falsifications.
- The census date test used two dates only.
- C1's V1 removes the C2 claim entirely; I did not test a sha-consistent edit to claims.json (that would require re-freezing).

## Tooling
No tools installed or upgraded. Read-only git (archive, show, ls-tree, log) and read-only counter/census/freeze-check runs only. Scratch dir removed on exit.
