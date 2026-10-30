# R48Review16 — SHONEN historical-assessment locations + migration rationale (archive & report preserving)

- **Seat:** R48Review16 (scribe, leaf member — no subagent dispatch), round 48 wave 1, lane `kasegi-shokunin`
- **Axis:** depth:verifiability · **Judged on:** depth:verifiability
- **Assignment:** "Review SHONEN historical assessments locations in existing reports, and draft migration rationale preserving archive and reports."
- **Rules read first:** `/home/vgpnk/.omp/agent/RULES.md` (tooling directive noted: no installs performed — none needed; host-wide pacman pause honored, pacman never invoked). Frozen claim `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/claims.json` at freeze `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` read; source snapshot `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/controls/protocol-source.txt` read (§Lifecycle, §Promotion gates, §report contract); round-47 verifier routes R1/R2 read (below).
- **Hygiene:** read-only against the lane; no production/fleet/sibling/domain files written; no git/jj mutation (only `git rev-parse`, `git status --porcelain`); no commits; no delegation; no background jobs. Scratch `/fast/scratch/hyaku/kasegi-r48/R48Review16/` created explicitly, receipts saved, removed at exit.

## 0. Frozen context this seat works inside

C1 (`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/claims.json`): author-side form only — "SHONEN.md conforms to the canonical four-box author-assessment grammar with existing local evidence pointers; this is form validation, not promotion or evidence truth." Archive clause of the kill_rule, verbatim: "restoration loses historical bytes (archive must retain SHA256 596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05)".

Round-47 verifier routes (`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-47-verifier-spotcheck.md:85-86`), verbatim:

> **R1 — SHONEN.md canonical-form drift.** The file now carries 13 accumulated per-round assessment blocks (52 `- [~]` lines) against the canonical form (seed verbatim + marks confined to the box character plus one indented evidence line per box, no other prose). Predates this round — every historical block is earlier rounds' work — but this round appended one more (+7 lines). Route: keep per-round SHONEN assessments in the reports (they are already there), restore SHONEN.md toward the canonical seed shape, or record the fleet-sanctioned convention explicitly.
>
> **R2 — plain-target phrasing.** `supersedes S074` frozen target 1 matches 2 lines because the second match is prose in a Registry-changes bullet. Disclosed by the lane; frozen targets stay unrepaired. Future frozen plain expressions should anchor to row form (`^\| S[0-9]+ \|.*supersedes`) so prose cannot meet the target.

R1 is the route C1 executes; R2 was read for context and constrains this seat only in one way: this report quotes frozen bytes, it does not propose re-anchoring any frozen target.

State measured this seat: base `903d47e13058982460f0d90c1c2b9c7c02680646` (historical SHONEN.md, blob `b0bd443a55dd0aac1fe86684bc3cae96454a6f7d`, 41339 bytes) → freeze `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` → HEAD `3d7e042ecbb1f17662f5042e8d3da3290722c031` (canonical SHONEN.md, 12 lines, sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`, working tree clean for `SHONEN.md` and `claims.json`). The blob/archive chain (byte-identity of control capture to base export, `expect_before` replay, ancestor check) was verified by sibling seat R48Review02 (`.ufo/waves/round-48/wave1/R48Review02.md`); this seat independently re-measured the archive hash, mark count, and the frozen counter on the landed tree.

## 1. Finding A — where the historical SHONEN assessments actually live

Five location classes, all observed this session. Together they are what "migration" must preserve.

**A1. The pre-repair SHONEN.md bytes themselves (356 lines, 52 `- [` marks, 13 accumulated blocks per R1).** Recoverable byte-exactly at three pinned locations:
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/controls/shonen-before.txt` — sha256 `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` (measured this seat), byte-frozen by the C1 kill_rule;
- git blob `b0bd443a55dd0aac1fe86684bc3cae96454a6f7d` at base `903d47e1` (identified by R48Review02 via `git ls-tree`/`git cat-file`; history append-only: base → freeze → repair);
- transiently, the working tree itself: my first read of `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` this session returned the 356-line historical form; minutes later the same path read 12 lines / sha256 `b1352168…` — the integrated candidate landing under integration owner KasegiR48 during wave 1 (observed, not seat-caused; LOG.md round-48 entry at `LOG.md:2045-2051` documents the restoration and the archive retention). Headed blocks inside the historical bytes: round-34 history paragraphs at `:4-63`; `## BLOCK SHONEN.md` (round-40 corrections) at `:205`; `## Round 41 evidence` `:225`; `## Round 42 evidence` `:232`; `## Round 46 evidence` `:304`; `## Round 46 (attempt 2) evidence` `:318`; `## Round 47 evidence (asserted only)` `:351`; the remainder are unheaded paragraph/list blocks (rounds 35–40 etc.), 52 marks total (counted this seat: `grep -c '^- \['` → 52).

**A2. The per-round lane reports — the protocol's designated assessment record.** Every dispatched lane's report must carry a `## SHONEN` heading with one `[x]`/`[ ]`/`[~]` line per box (protocol-source snapshot, report-contract section: "A report without this heading does not satisfy the contract"); reports are filed once and never rewritten ("a correction to it lands in the correcting round's own report, or as an erratum … never a rewrite of the filed bytes"). Observed kasegi `## SHONEN` headings in the fleet repo `/home/vgpnk/Projects/shokunin/.ufo/reports/` — 28 files matched `^## SHONEN`:

| round | line | round | line | round | line |
|---|---|---|---|---|---|
| 6 | `round-6/kasegi.md:53` | 27 | `round-27/kasegi.md:93` | 38 | `round-38/kasegi.md:74` |
| 20 | `round-20/kasegi.md:36` | 28 | `round-28/kasegi.md:47` | 39 | `round-39/kasegi.md:51` |
| 22 | `round-22/kasegi.md:78` | 29 | `round-29/kasegi.md:31` | 40 | `round-40/kasegi.md:56` |
| 23 | `round-23/kasegi.md:157` | 30 | `round-30/kasegi.md:58` | 41 | `round-41/kasegi.md:42` |
| 24 | `round-24/kasegi.md:237` | 31 | `round-31/kasegi.md:67` | 42 | `round-42/kasegi.md:177` |
| 25 | `round-25/kasegi.md:50` | 32 | `round-32/kasegi.md:61` | 43 | `round-43/kasegi.md:89` |
| 26 | `round-26/kasegi.md:43` | 33 | `round-33/kasegi.md:76` | 44 | `round-44/kasegi.md:72` |
| 34 | `round-34/kasegi.md:143` | 35 | `round-35/kasegi.md:80` | 45 | `round-45/kasegi.md:65` |
| 36 | `round-36/kasegi.md:74` | 37 | `round-37/kasegi.md:71` | 46 | `round-46/kasegi.md:77`, 47: `round-47/kasegi.md:118` |

Notables: round 6 is the only observed historical `[x]` (pre-dating the current verifier-naming gate text — form history, not re-graded here); the fleet round-21 copy shows **no** `## SHONEN` match, while the lane-local copy `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/reports/round-21/kasegi.md:170` carries the heading — `LOG.md:883-884` records exactly this ("The new report assessment adds the missing SHONEN section"), i.e. the correction lives in the later record, the original bytes stay untouched.

**A3. Wave-internal seat reports and drafts carrying SHONEN assessments** (lane `.ufo/waves/`): `round-30/wave1/draft-report.md:76`; `round-33/wave1/ScribeReportDraft.md:273`; `round-35/wave1/ScribeReportDraft.md:333`; `round-36/wave1/ScribeReportDraft.md:384`; `round-37/wave1/ScribeReportDraft.md:333`; `round-41/wave1/RevD4D5D6.md:54`; `round-43/w1/L1Report.report.md:72` and `round-43/w1/ScribeReportSkeleton.report.md:425`; `round-46/attempt2/wave1/R46bCritCalibration.md:13`; `round-46/wave2/R46W2RevLanding.md:59`; `round-47/w1/R47SrReport.md:142`. Fixture copies inside probe trees (`round-25/wave1/mut-audit/base/.ufo/reports/round-21/kasegi.md:170`, `round-25/wave1/rev-independent/base-tree/.ufo/reports/round-21/kasegi.md:170`, `round-47/w1/R47RevCounterC1.draft/attack-B/corpus/lessons/round-46.md:69`) are test fixtures, not assessment records — migration may ignore them; they must merely not be deleted while their probes' receipts cite them.

**A4. `LOG.md`** (`/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md`, append-only): SHONEN-assessment mentions observed at `:883-884` (round-21 section add), `:1541-1545` (round-30 verifier close-out: "one `## SHONEN` heading with 4 box lines"), `:1711` (round-39 correction sweep touching SHONEN), `:1752` (round-42 erratum sweep reading `SHONEN.md` round-41 box 3 at line 229 of the historical file), `:1974` (round-43: "SHONEN checkboxes remain `[~]`"), `:2043` (round-47: "SCORECARD/SHONEN remain held/asserted"), `:2045-2051` (round-48 restoration entry, naming the archive path).

**A5. The evidence receipts the historical blocks point at** — wave artifacts such as `round-34/wave1/RevNoHarm.md`, `round-34/wave1/ScribeSkillGate.md`, `round-34/wave1/ExecCaptureBindingHarden.md`, `round-33/wave1/ExecRegressionC1.md` — all still in place under `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/`; the canonical repair removed the blocks from SHONEN.md, not the receipts they cited.

## 2. Finding B — migration rationale (draft), preserving archive and reports

**Proposed rationale statement** (grounded in R1's route text and the protocol's own allocation of durability):

> The canonical four-box form is the protocol seed ("Minimum bar: the seed below changes only with this gate text", protocol-source snapshot §Promotion gates). The per-round assessment blocks that accumulated inside SHONEN.md were never the record of record: by protocol, every round's assessment is filed under a `## SHONEN` heading in that round's dated, hash-cited, never-rewritten report, and the promotion review reads those reports — on promotion SHONEN.md is deleted outright and "the review is recorded in the promoter's lane report and the repo's `LOG.md`". The protocol therefore designates reports + LOG.md as the durable assessment home and SHONEN.md as transient seed state; R1's route ("keep per-round SHONEN assessments in the reports (they are already there), restore SHONEN.md toward the canonical seed shape") executes exactly that allocation. Removing the 13 embedded blocks / 52 author marks restores the seed form without deleting any assessment: each historical assessment remains resolvable through (a) its dated fleet report (A2 table), (b) the byte-frozen control capture and git blob for the in-file bytes (A1), and (c) the wave receipts its evidence lines cited (A5). The migration is form-only: no mark is upgraded, downgraded, or re-graded, and promotion/semantic truth stay independently judged (C1 `mechanical_limits`).

**Why not carry the history inside the canonical file:** the form grammar R1 states (seed verbatim; marks confined to the box character plus one indented evidence line per box; no other prose) rejects accumulated blocks by construction — re-embedding them would re-grade `SF-PREAMBLE`/drift, the exact failure the frozen counter exists to catch. History's correct home is the immutable append-only surfaces (reports, LOG.md, frozen controls), which already hold it.

**Preservation constraints any landing must satisfy (all currently satisfied):**
1. The control capture `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/controls/shonen-before.txt` keeps sha256 `596122c0…` forever (C1 kill_rule) — measured this seat post-landing: still `596122c0…`.
2. Git history stays append-only; the historical blob `b0bd443a…` stays reachable at base `903d47e1…` — verified by R48Review02 (`git merge-base --is-ancestor` exit 0; base→freeze→repair).
3. No fleet or lane report is rewritten, moved, or deleted — the A2/A3 locations are read-only for this repair; corrections would land as new-round records/errata, never as edits to filed bytes.
4. `LOG.md` is corrected only by appended entries (round-48 entry at `:2045-2051` already names the archive path).
5. SHONEN.md is **not** deleted by this migration — deletion happens only at the promotion gate, a separate, independently-judged act.
6. Evidence receipts cited by historical blocks (A5) stay put; nothing in the repair range touched `.ufo/waves/round-2x..4x` artifacts (round-48 commits per R48Review02: `3d7e042` "round-48: restore canonical checklist and dispatch 64 probes", `3546f70` freeze).

**Resolution chain a future auditor can walk:** round-N assessment → `/home/vgpnk/Projects/shokunin/.ufo/reports/round-N/kasegi.md` (dated, lane-authored commit cited by LOG.md) → in-file drift bytes → `shonen-before.txt` (sha-pinned) or `git show 903d47e1…:SHONEN.md` → cited receipts under `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-N/`. Every hop observed present this session.

## 3. Expected vs observed (this seat's own commands)

| Check | Expected | Observed | Command (exact) |
|---|---|---|---|
| Landed form | C1 `expect_after`: `shonen-form canonical=1 finding=SF-CLEAN exit=0` | `shonen-form canonical=1 finding=SF-CLEAN exit=0` | `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin` |
| Archive SHA retained | kill_rule: `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` | identical | `sha256sum .ufo/waves/round-48/controls/shonen-before.txt` |
| Historical mark count | C1 before-text "52 author marks" | `52` | `grep -c '^- \[' .ufo/waves/round-48/controls/shonen-before.txt` |
| Canonical landed bytes | R48Review02-cited `b1352168…`, 12 lines | identical, 12 lines | `sha256sum SHONEN.md && wc -l SHONEN.md` |
| Evidence pointers exist | 4 local pointers resolvable | all four present (`LOG.md`, `SKILL.md`, `PROVINCE.md`, `corpus/lessons/round-47-verifier-spotcheck.md`) | `ls -l LOG.md SKILL.md PROVINCE.md corpus/lessons/round-47-verifier-spotcheck.md` |
| Tree state | clean at HEAD `3d7e042e` | clean; HEAD `3d7e042ecbb1f17662f5042e8d3da3290722c031` | `git rev-parse HEAD && git status --porcelain -- SHONEN.md .ufo/waves/round-48/claims.json` |

No counter defeat observed; no frozen byte amended; no conflict to report verbatim (none encountered).

## 4. Limits

- Author-side form only: this seat judges locations and migration form, not promotion or semantic evidence truth (C1 `mechanical_limits`).
- The 356→12-line working-tree transition was observed mid-seat and attributed to the integration owner's landing (LOG.md `:2045-2051`); this seat performed no write to any lane file.
- The historical block map in A1 is complete for `##`-headed blocks; the unheaded blocks (rounds 35–40 era) are covered by the 52-mark count and R1's 13-block count rather than a per-block line map — recoverable from the pinned capture if ever needed.
- Sibling-verified claims (blob identity, byte-identity capture↔base, ancestor check) are cited to R48Review02, not re-derived here except the archive hash and mark count.

## 5. Hygiene

No tool installs or updates (none needed; git + coreutils + python3 host only). Pacman never invoked (host-wide pause honored). Read-only git only. No commits, no pushes, no jj commands. No fleet-root tracked file touched. Scratch `/fast/scratch/hyaku/kasegi-r48/R48Review16/` held `receipts.txt` (verbatim command outputs, saved before removal) and was removed at exit (`rm -rf`, removal confirmed).
