# ConnCrossClaims — round 42 wave 1 receipt

Seat: ConnCrossClaims (connector, leaf; no subagents). Lane: kasegi-shokunin. Base `5053a7f46de35784cff4b56756906e9014a38276`. Lane HEAD when scanned: `0566bd6` (`round-42: frozen claims + controls + wave-1 spec/dispatch`). Scan window: 2026-10-28, about 11:09Z to 11:20Z (`date -u` at start: `2026-10-28T11:09:12Z`). Axes read: depth:verifiability, coverage (connector: no axis score moved). Frozen `claims.json` read first, not edited.

Deliverable: `.ufo/waves/round-42/wave1/ConnCrossClaims.txt`, 7 lines, sha256 `d72a9f636e3730c9bd7d7d373bc89a347593a0998bf363732903289d4f9157a4`. It holds only four landable `Correction (round 42):` paragraphs (listed in §1 as U1–U4). The deliverable does not duplicate the SCORECARD duplicate-block note, which ScribeCorrections owns.

Lane writes: none. Every lane read was `read`, `grep`, `git show`/`log`/`ls-files`/`cat-file`/`status` (read-only). The lane's only tracked-tree change since base is `.ufo/waves/round-42/` (commit `0566bd6`). The working tree shows only untracked files written by sibling seats and the L1. The instrument runs in §4 used `PYTHONDONTWRITEBYTECODE=1` and wrote only under scratch.

---

## 1. Correction ledger: which past corrections are still unmarked

Method. Every `Correction (round N)` line and every `Correction` or `Erratum` block in `SCORECARD.md`, `LOG.md`, `SHONEN.md` and `corpus/lessons/round-{38,39,40,41}*.md` was read against the claim it corrects, and the claim was checked against the committed file it names. A claim counts as marked only when a correction names the same claim (by line or by quoted text) and states the corrected value. Rounds 22–37 were checked only by grep for "still open"/"not yet" language, not line by line. Findings:

| id | record & line | claim as written | status at base | evidence |
|---|---|---|---|---|
| U1 | `LOG.md:1746` (round-41 Repairs) | "D6 SKILL registry block repaired and r41 suite row appended" | **unmarked, false at base.** No `Correction (round 41/42)` names it. | `SKILL.md:1120` separator, `:1121` blank, `:1122` `r40-closure.sh` row (table split); `:1128` duplicate `r40-closure.sh` row inside the round-41 block; `:1129` `r41-closure.sh`. Round-41 verifier §5 item 3 (D-r41-3) records the same defect as open. |
| U2 | `corpus/lessons/round-40.md:15` and `:220` | `closed=10/10 exit=0` at Y; graded `selftest cases=10 failures=0` | **unmarked.** The round-41 corrections in SCORECARD (`:1604`), LOG (`:1738`) and SHONEN (`:223`) cover this tally, but the lesson is not among the three records corrected. | Round-40 verifier §5 D2: Y receipt has no selftest line; the only graded tally is over scratch Y′. `corpus/lessons/round-40.md:211` begins the section containing `:220`. |
| U3 | `SHONEN.md:21-23` (box 1) | "the append-only EOF correction is not yet in `SKILL.md`" | **stale, partly marked.** The L1 integration note (`SHONEN.md:75-83`) says the correction landed, but names box 1's "byte-unchanged" sentence and box 4's "owed" sentence, not `:21-23`. | `SKILL.md:1091` carries the round-34 correction; `corpus/instruments/capture-binding-check.py` is `892` lines, sha256 `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` (matches the pin, re-measured in §3). |
| U4 | `SHONEN.md:198` (round-39 box 3) | "r39 suite run + graded selftest at the verification ref Y (all-gates.txt)" | **unmarked by number.** The round-40 `Correction` at `SHONEN.md:207` is written against `:194` (box 1, which carries the quoted "suite `--selftest` graded cases=8 failures=0 at the verification ref") and labels it "box 3". | Y receipt `8371e7ac9f32cae5ed72f8c28205634603f836fa`: `closed=7/8 exit=1`, `selftest cases=8 failures=1`, `G2 positive=fail` (quoted in SHONEN `:207`). |
| U5 | `corpus/lessons/round-41.md` Gate (`:39-71`) | no reject recorded | **routed, not marked** (round-41 verifier D-r41-2). | `grep -i reject corpus/lessons/round-41.md` → no hits. Round 42 C2 must add the reject. |
| U6 | `SCORECARD.md:1602-1605` and `:1607-1610` | four `Correction (round 41)` lines, each duplicated verbatim | **marked only by the LOG note** (`LOG.md:1750`: "accidentally appended twice; they remain byte-identical"). Not repaired. | `cmp` of `sed -n 1602,1605p` and `1607,1610p`: IDENTICAL. Introduced by integration commit `03ca614` ("round-41: integrate wave-1 C1/C2 deliverables"): 8 `+Correction (round 41)` lines in SCORECARD, 3 each in LOG and SHONEN. No other file has a duplicated correction block (global awk scan of SCORECARD/LOG/SHONEN and `corpus/lessons/round-*.md`). |
| U7 | `corpus/lessons/round-41-verifier-spotcheck.md` §5 items 2, 4, 5 | D-r41-2 (reject), D-r41-4 (report "Stale-lane" line), D-r41-5 (connector seats) | **routed, open.** Item 5 is satisfied for wave 1 by the spec (two connector seats: `ConnCrossClaims`, `ConnWave2Seed`), not yet for wave 2. Item 4 appears in no round-41 landed record: `grep -n 'Stale-lane'` finds only the verifier's own item (`round-41-verifier-spotcheck.md:141`) and an older LOG note (`LOG.md:1642`). | — |
| U8 | `SCORECARD.md:1628` ("Planned for round 42") | "build a fresh frozen C1 predicate only after repairing I1 … and I3 …; include a green I2/Y receipt and clean scratch baseline before dispatch" | **plan precondition unmet at freeze.** Not a correction; an ordering decision for the L1 (see §2, H12). | `claims.json` frozen before any J-limb landed; control scratch not clean (§4). |

Closed and marked, for the record: round-38 box 3 and LOG/SCORECARD round-38 C1 lines (`Correction (round 39)` at `SHONEN.md:190`, `LOG.md:1704`, `SCORECARD.md:1560`); round-39 C1 8/8 claims (`Correction (round 40)` at `SCORECARD.md:1588`, `SHONEN.md:207`, `LOG.md:1723`, `corpus/lessons/round-39.md:98-99`); round-39 rejects S056/S058/S059 now carry URL/date/quote (`corpus/lessons/round-39.md:103-105`, appended block "Gate additions (round 40, verifier R6)"); M39-2 criterion (`corpus/QUALITY.md`, round-40 verifier R5); round-40 D1 (`Correction (round 41)` at `SCORECARD.md:1602-1603`, `LOG.md:1735`, `SHONEN.md:221`), D2 (`:1604`, `LOG.md:1738`, `SHONEN.md:223`), D4/D5 (`corpus/lessons/round-40.md` `## Erratum (round 41)`, L265–L286), D7 (round-40 lesson `:236-241` restored `teaches`). Round-41 `Correction` lines on r40 C1 (`SCORECARD.md:1602-1610`) mark D1 and D2 at the record level; the duplication is U6.

## 2. Wave-1 interactions and ordering hazards for the L1

Each hazard names a producer, a consumer, and the evidence. Hazards H1, H5, H7 and H8 are decisions the L1 must make before the judged head J is cut.

H1 — Scratch root decides J13 and I6 (C1). The round-42 counting commands take `--scratch-root <scratch>`. Seat scratch lives under `/fast/scratch/hyaku/kasegi-r42/`, which held 33 entries at this seat's last listing and changes while wave 1 runs. Measured in §4: the r41 suite run on base with a populated shared root (the do-nothing control) prints `closed=8/12`; the same suite with a clean private root prints `closed=9/12` on two consecutive runs. The difference is I6, which is green on the clean root only because it scans nothing (`I6 payload=strays=0,read=ok,scanned=0 closed=1`). Sequence: (a) J5 must make the scan non-vacuous (`scanned=0` is not green); (b) the Y counting run uses a fresh empty `--scratch-root` outside `/fast/scratch/hyaku/kasegi-r42/`, run after every wave-1 and wave-2 seat has removed its scratch dir.

H2 — Judged-head assembly and the placeholder rule. J must carry every round-42 change except the receipt, and lane files may not name J by hash. `ScribeLesson`'s draft uses `<pending>` placeholders for base, freeze, J and Y. The base and freeze hashes are knowable and should be written. J and Y cannot be named inside the lane, so the lesson states the receipt as the source of those values. Any `<pending>` that reaches J is a placeholder-bleed defect of the class the round-38 verifier recorded (`corpus/lessons/round-38.md:285`, M38-3). Integrate by copying the wave-dir drafts into the lane, then cut J, then add only `all-gates.txt` for Y.

H3 — The SKILL.md registry fix is one block, and the pin moves with J6. (a) `ExecJ3Registry.skill-fix.txt` must replace `SKILL.md:1117-1129` as one block. Appending a corrected block after the current text leaves the split at `:1121` and the duplicate at `:1128` in place, which is how U1 happened. Any r42 registry row goes inside the same replacement. (b) `SKILL.md:1091` pins `capture-binding-check.py` at `3d9e5e0d…`. J6 patches that file, so a new appended re-pin must follow J6 in the same integration. Both edits touch SKILL.md; order J6 → re-pin → J3 fix, or do them in one append.

H4 — C2 counts are only valid after J6 and J7. `ExecHarnessSync` is a runbook, not a run. Binding `56/56` and harness `28/28` must be measured after `ExecJ6Bind` and `ExecJ7Flip` land, because F-BIND and F-FLIP change the instruments those counts come from. The frozen before-values (`c2-controls/before.txt`: harness 27/27, binding 55/55) were measured before any patch.

H5 — The C2 pick is a barrier, not a parallel lane. Roster at this seat's spawn: `ExecC2Rows-2` running ("Reading round-41 manifest") and `ScoutF25Lead` running ("Listing lane repo structure"). The `ExecC2Rows` prompt says to build rows only after `ScoutF25Lead` files its facts, capture and manifest record. `ScribeC2Entry` and `ScribeC2Gate` have the same dependency. `ScoutSibling` (OSV and CVE Record Format overlap across sibling lanes) must also report before rows are written. Lane pre-check (fixed-string, read-only): `grep -rlF 'OSV'` over `corpus/`, `SKILL.md`, `PROVINCE.md`, `README.md` returns no files; `grep -rlF 'CVE Record Format'` returns no files; the lane's CVE-adjacent coverage is the CNA rules (`S022`, `S030`, `S031`; `corpus/knowledge/cna-assignment-and-vulnerability-rules.md`). The CNA rules govern assignment, not record structure; CritBoundary owns that boundary call. These greps are inputs to the scout's no-overlap check, not a pick.

H6 — Source ids: S064 and S065 collide with staged rows; the rerun is stale. Read-only comparison of lane `corpus/SOURCES.md` ids (S001–S063) with the staged `shokuknow/merge/kasegi/SOURCES.append.md` ids (S031–S124), using the 0–3-space extractor the round-40 lesson requires: `comm -12` gives 33 colliding numbers, S031–S063. One is the same URL (S042, IPA process page). The round-40 rerun counted 29 for S001–S059. The four lane rows added in rounds 40–41 (S060–S063) were never checked against the staged package and add four more collisions: staged S060 is a Hitachi PSIRT page, S061 and S062 are Chinese court cases, and staged S063 is a Chinese court case, while the lane's S060–S063 are CycloneDX, CISA VEX status justifications, OASIS CSAF 2.1 and RFC 9116. C2's planned S064 and reject S065 are staged-occupied: staged S064 is the JPCERT partnership guideline and staged S065 is the NPC law catalogue (read-only `grep -nE '\bS06[3-6]\b'`). Nothing collides in the lane today, because nothing from the staged package is adopted. The L1 must rerun the collision guard over S001–S063 (expect 33) before any adoption, and any adopted staged row needs a renumber map starting above S063.

H7 — Duplicate-block repair against the append-only rule (U6). `ExecJ11Corr` removes SCORECARD `:1607-1610`, which are byte-identical to `:1602-1605`. `ScribeCorrections` drafts a dedupe note that says the duplicate entries are "kept as history". Those two positions cannot both hold: J11 forbids a duplicated `Correction (round N)` block at Y. Resolution the L1 must choose: delete the second, identical copy and cite both ranges in the note (no information is lost), or leave the duplicates and let J11 red. Also: `ScribeScorecard` and `ScribeCorrections` both append to `SCORECARD.md`, which is how the round-41 duplicate happened (`03ca614`). Run the J11 check after both appends, and cite line ranges only after the dedupe.

H8 — The replay and kill clauses cover J1–J7; the predicate names nine families. `claims.json` C1 predicate names F-EVID (J1), F-TOKEN (J2), F-TABLE (J3), F-DECL (J4), F-SCAN (J5), F-BIND (J6), F-FLIP (J7), F-RCPT (J8) and F-CORR (J11). The C1 kill rule names only the first seven as "repair families", and its replay clause says "the committed replay limb of any J1-J7 check". So the receipt-integrity family (J8, which is what makes Y credible) and the correction-uniqueness family (J11) have no replay requirement and no kill clause. The round's own text says "EVERY repaired check carries a REPLAY limb" (`claim_design_lesson`). The L1 must either extend the replay and kill clauses to J8 and J11 by claims erratum before freeze is honored, or record that J8 and J11 are unfalsifiable by the frozen rule. This seat recommends the erratum.

H9 — The replay substrate for J1/J2 is prose today. The round-41 defeats are described in `RevC1Counters.md:10,22,34` and `CritC1KillRule.md:17-26` as selftest transcript lines (`mutant=evidence-not-named`, `mutant=mangled-value-token`). No standalone mutant fixture exists: a grep for `union` and `10/100` across `.ufo/waves/round-41/wave2/` matches only transcript lines. The J1/J2 replay limbs therefore depend on the round-41 suite's internal mutant generators. Either commit fixtures under the round-42 tree (so replay does not depend on `r41-closure.sh`, which J12 does not forbid deleting but which the round will retire) or name the generator as the replayed artifact. Commit before J is cut; a fixture that exists only in a wave dir does not reach Y.

H10 — Prompt coverage of the replay requirement. Only `ExecJ1Evidence`'s prompt mentions replay. `ExecJ2Token` through `ExecJ12J13` (12 prompts) contain no replay requirement. `ExecSuiteCore` says "each J check MUST carry its REPLAY limb", and it is the only integrator. The L1 should verify at integration that every J limb calls `replay_defeat` (or its equivalent), and that J8–J13 have explicit replay clauses (H8).

H11 — Interface dependency: `replay_defeat`. `ExecReplayHarness` defines `replay_defeat <artifact> <mode>`. No J-limb prompt names that function. Freeze the signature when `ExecReplayHarness.sh` lands, and integrate J-limbs against it. Limbs written before the library lands must be re-checked.

H12 — Freeze timing (`claims.json`). The frozen claims predate every repair, against SCORECARD `:1628`. Its own `frozen_at_utc` value is `2026-10-28T12:05:00Z`. The freeze commit `0566bd6` is `2026-10-28T08:00:01-03:00` (`11:00:01Z`), the file mtime is `07:51:52 -0300`, and this seat's clock read `11:09:12Z`. The `frozen_at_utc` value is therefore later than the commit that contains it and later than the clock now; `errata` is `[]`. The same class was filed as an erratum in round 28 (`LOG.md:1340`). Recommend `claims-erratum-1.md` correcting `frozen_at_utc` to the commit instant, and deciding the U8 precondition explicitly.

H13 — The C1 before-text does not reproduce. `claims.json` C1 `before` says "the r41 suite at base prints closed=10/12 exit=1". The do-nothing control (`c1-controls/do-nothing.txt`) prints `closed=8/12 exit=1` with `selftest cases=12 failures=8`, on the shared root. This seat's two clean-root runs print `closed=9/12 exit=1` with `selftest cases=12 failures=7`. Neither matches 10/12. The base-closed<13/13 clause of the frozen predicate holds in every run, so no kill is triggered, but the before-value is not a reproducible number. Correct it by erratum, and treat the difference as H1's environment effect.

H14 — C2 before-state inherits an unverified number. `SCORECARD.md:1617` records coverage `8 (held; not verified)` for round 41, and the round-42 claim carries `score_before 8` with no "not verified" annotation. The C2 after-state counts F24 as admitted (frontier 24 → 25), while F24 is parked for an open L0 scope question. If L0 rules F24 out of scope, F_admitted falls and the round-42 after-state moves with it. The L1 should record the round-42 before-state as "8, not verified (round-41)" and keep F24 out of the F25 claim text.

H15 — Reject and staged-id coupling (C2). The reject required by D-r41-2 must carry URL, access date and a ≤25-word located quote (C2 kill). If the reject is S065 (the lesson's natural next id), it collides with staged S065 (H6). `ScoutF25Lead.reject-record.txt` and `ExecC2Rows.registry-rows.txt` must use the same id, and the id must be settled before `ExecHarnessSync` counts registry rows (`64+R`, R ≥ 1).

## 3. Commands and artifacts read (all read-only against the lane)

- `read` of `.ufo/waves/round-42/claims.json` (full), `wave1-spec.json` (items and prompts), `c1-controls/do-nothing.txt`, `c2-controls/before.txt`.
- `grep`/`read` of `SCORECARD.md`, `LOG.md`, `SHONEN.md`, `corpus/lessons/round-{38,39,40,41}*.md`, `SKILL.md:977-1129`, `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/instruments/knowledge-expected.txt`.
- `git -C <lane> log --oneline -6`, `rev-parse HEAD`, `status --porcelain`, `show --stat 0566bd6`, `show 03ca614 -- SCORECARD.md`, `log -S'Correction (round 41): round-40 C1 is not verified'`, `merge-base --is-ancestor 1f74646… 0f64b8c…`, `diff --stat 1f74646… 0f64b8c…` (31-line receipt only), `ls-files .ufo/waves/round-41 / round-40 / round-39`, `cat-file -t 1f74646…`.
- `sha256sum` of `capture-binding-check.py`, `r-defect-closure.sh`, `kill-rule-check.py` (pins at `SKILL.md:1091,1104` match).
- `cmp` of SCORECARD `1602-1605` and `1607-1610`.
- Read-only `grep` of `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` (the staged package): ids and rows for S060–S065 only. No shokuknow campaign tool was run.

## 4. Instrument runs (scratch only; lane untouched)

The round-41 suite is the only instrument this seat ran, to test H1 and H13. Two runs against base `5053a7f` with a clean private root:

```
bash corpus/instruments/r41-closure.sh --export-ref 5053a7f46de35784cff4b56756906e9014a38276 \
    --work $S/w-base --scratch-root $S/root-clean
```

Run 1 (48.2 s wall) and run 2 (47.5 s wall) printed the same per-check values. Run 1 excerpt (`exit=1`):

```
I1 closed=1   I2 closed=0   I3 closed=1   I4 closed=1   I5 closed=0   I6 closed=1
I7 closed=1   I8 closed=1   I9 closed=1   I10 closed=1  I11 closed=1  I12 closed=0
selftest cases=12 failures=7
closed=9/12 exit=1
```

Notable lines: `I6 payload=strays=0,read=ok,scanned=0 closed=1` (vacuous green); `I12 ... neg-red=1 ... closed=0`; `I10 payload=suite=1,base=4/12,base-exit=1,r40=4/12,r40-exit=1,probe=3/3 closed=1`.

Comparison (values printed by runs; `claims.json` is frozen text):

| source | root | closed | selftest |
|---|---|---|---|
| `claims.json` C1 before-text | (not stated) | 10/12 | (not stated) |
| `c1-controls/do-nothing.txt` (control) | shared `/fast/scratch/hyaku/kasegi-r42/l1-ctl` | 8/12 | cases=12 failures=8 |
| this seat, run 1 | clean private | 9/12 | cases=12 failures=7 |
| this seat, run 2 | clean private | 9/12 | cases=12 failures=7 |

Plain run refusal, the two base and r41-head negatives, and the Y counting commands were not run here; they are the main agent's verification. Nothing in this seat claims a round-42 pass.

## 5. Interactions summarized for the L1 (sequence)

1. Cut `claims-erratum-1.md` (H8 erratum for J8/J11 replay and kill; H12 `frozen_at_utc`; H13 before-text) before J is judged.
2. Commit replay fixtures (H9) and `replay_defeat` (H11) before J-limb integration; then J1–J13 limbs; then `ExecSuiteCore` integration.
3. J6 and J7 patches; then the SKILL re-pin (H3b); then the SKILL registry block replacement (H3a, U1).
4. SCORECARD dedupe (H7) after all SCORECARD appends; decide option first.
5. C2: `ScoutSibling` and `ScoutF25Lead` verdicts → `ExecC2Rows` (rows, manifest, reject with S-id settled per H15) → capture binding → knowledge entry → harness, binding, audit, census (H4 after J6/J7).
6. ScribeLesson placeholders removed (H2); draft lesson lines with no J/Y hashes.
7. Copy drafts into the lane; cut J; run the suite on J with a fresh private `--scratch-root` after all seats have exited (H1); add `all-gates.txt` as Y (only file in Y−J).

## 6. Tooling and network

No tools installed. No network fetches. `pacman` not run. `uv`/`npx` not used.

## 7. Scratch

Scratch: `/fast/scratch/hyaku/kasegi-r42/ConnCrossClaims/` (contains `lane-ids.txt`, `staged-ids.txt`, `coll.txt`, `a.txt`, `b.txt`, `items.txt`, `r41-base-clean*.txt`, `root-clean*`, `w-base*`). Removed by the seat's EXIT trap after this receipt and the deliverable are written.

## 8. Not verified / out of scope

- Did not run the r42 suite (it does not exist yet). Did not check any J-limb's correctness.
- Did not re-derive the 33-id collision set with a second extractor; one extractor was used, the one the round-40 lesson specifies.
- Did not read `considerthese`, `ScoutConsiderthese` material, or F24 candidates (F24 stays parked).
- Did not check rounds 22–37 corrections line by line (grep only; see §1 scope note).
