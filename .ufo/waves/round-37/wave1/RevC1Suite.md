# RevC1Suite — design review of the r37 C1 closure suite (E1–E14)

Round 37, claim C1 (`depth:verifiability`), seat RevC1Suite (leaf reviewer; no subagents, no probe budget used).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only lane write: this receipt; all work in scratch).
Lane HEAD during review: `b362068195d5489aa94b31e6ec8f880c367e0ba0` (round-37 wave in flight; 6 untracked wave entries).

**Verdict: the suite architecture is sound and the D6 fail-closed rewrite is real — behaviorally proven, not just shaped. But three of the five defect-closing checks (E10, E12, E14) plus E1 carry DEMONSTRATED false-green paths that the L1 must fix before landing the suite, and E11/E13 need smaller strengthenings. Every fix below is strictly stronger than the frozen claim's byte condition — none contradicts the claim; all keep the required reds red.**

## 0. What was reviewed and how

Design sources: frozen `.ufo/waves/round-37/claims.json` C1 predicate + kill rule; the `ExecC1SuiteBuild` item spec (`.ufo/waves/round-37/wave1-spec.json`); the committed r36 template `corpus/instruments/r36-closure.sh` (sha256 `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4`, 894 lines) whose E1–E9 semantics the claim carries forward; the routed defects D1–D6 (`corpus/lessons/round-36-verifier-spotcheck.md` §5).

Draft under review: the builder's scratch copy `/fast/scratch/hyaku/kasegi-r37/ExecC1SuiteBuild/r37-closure.sh`, pinned at two versions — `d4f65f0a6c1d557b6fe233b402e0d30362d65c8d2ef5f34d28a8cb7c71bf69d2` (60020 B, snapshotted) and `ed88f8801554b484d44d12f6a6de20eebcf092af1870299299d8b5225712ab59` (60063 B, current). The delta is comment-only (5 diff lines, header wording), so every probe result applies to both. The suite is NOT yet committed in the lane (`git log -- corpus/instruments/r37-closure.sh` empty; absent at HEAD) — this is a design review of the draft the L1 will land byte-identically.

Method: full read of both suite versions; a probe harness that sources the draft's check functions and runs them against fixture trees in scratch; plain-mode runs of the draft against the r36 base export, the r36 judged-head export, and the builder's fixture lane (`80b1cc11707d993f059716aa6a4e7286df743c7b`); kill-rule greps on the draft bytes. All probes under `/fast/scratch/hyaku/kasegi-r37/RevC1Suite/` (removed at yield).

House-byte facts the checks bind to (verified this round):

| fact | evidence |
|---|---|
| stale label is plain, single-spaced | `SCORECARD.md:1492` = `Final lane commit: e666d902337a49dcbfc77880939874f39c6f477b` (inside the round-36 section) |
| wrapped `Final lane commit:` forms exist in-house | `SCORECARD.md:987` and `:1129` put the 40-hex on the NEXT line — the wrapped variant is a real house pattern, not hypothetical |
| multiple same-round headings are a real house pattern | SCORECARD has TWO `## Round 35` headings (lines 1263, 1284) |
| r36-closure.sh type cell bytes | `SKILL.md:1111` cell 2 is literally `gate\|probe` (od-verified); 6 rows carry it (1064, 1077, 1097, 1098, 1110, 1111); `SKILL.md:981` has an UNESCAPED `gate\|probe` variant; verdict-map arrow convention is `->` (`981`: `undeclared nonzero -> could-not-evaluate`); type vocabulary in use: `gate`, `rule` |
| false path bullet | `LOG.md:1665` round-36 C1 bullet names `corpus/instruments/r36-fixtures/`; LOG round headings are `## Round N — date — title` |
| round-37 lesson | `corpus/lessons/round-37.md` exists in no commit yet |
| naive cell-splitting is unusable on registry rows | `awk -F'|'` on `SKILL.md:1111` gives NF=13 (escaped pipes split cells) — any E13 implementation must be escape-aware |

## 1. Per-check verdict table

| check | closes | byte condition as drafted | false-green paths found | verdict |
|---|---|---|---|---|
| E1 | standing placeholder/hash-binding defects (r36 carry-over) | 0 `filled by the L1` + 0 `<LANE_HASH>` file-wide in SCORECARD.md; a Round[- ]?37 heading exists; every 40-hex on/after a `Final lane commit:` line (that line +4) inside the LAST round-37 block resolves and is an ancestor of the export ref | **unbound hash in a non-last round-37 block escapes** (T13: first block binds `0123…4567`, last block binds the real head → `closed=1`, rc=0) | FIX (F7) |
| E2 | round-34 depth:density erratum (carry) | `Erratum (round 35)` ≥1 ∧ corrected row regex ≥1 ∧ `201.2` ≥1 | none found; prose-only paths are mutant-proven (3/3) | SOUND |
| E3 | registry rows r35+r36 by exact basename (carry) | first-cell rows inside `## …Gates & probes registry…` sections | none found; mention/outside-section mutants 5/5 | SOUND |
| E4 | round-35 wave1-results.json tracked (carry) | ls-tree@ref=1 ∧ lane ls-files=1 ∧ provenance note nonempty | none found | SOUND |
| E5 | claims-erratum-d5.md present (carry) | file exists and is nonempty | none found | SOUND |
| E6 | 'Correction (round 35)' in round-34 receipt (carry) | path derived from ls-tree (single candidate) ∧ grep ≥1 | none found | SOUND |
| E7 | QUALITY supersedes-R22/R23 rows (carry) | row-shaped 3rd-column matches ≥1 each | none found; prose mutant 2/2 | SOUND |
| E8 | round-36 lesson records the correction (carry) | `M36` ≥1 ∧ `source-recheck` ≥1 ∧ stale line 0 ∧ round-35 lesson exists | none found; 4 mutants | SOUND |
| E9 | D6 — quiescence, REWRITTEN fail-closed | status read's EXIT STATUS decides; failed read → `status-read=failed`, `status-dirty=?`, RED; no `${…:-0}`, no stderr suppression on the read; 5 limbs (lane-root, status, seat dirs, head-match, scratch-root visibility) | none found in the rewrite — **behaviorally proven**: corrupt `.git/index` repo → `git status` rc=128 → E9 rc=1, payload `status-read=failed,status-dirty=?` (T5/T5b). Residuals below | SOUND — keep |
| E10 | D1 — committed gate receipt | receipt contains `suite-sha256=` == executing `suite_digest()`; per-id `^E<n> payload=` present (14); exact line `closed=14/14 exit=0`; per-id `^selftest case=E<n> ` present (14); exact line `selftest cases=14 failures=0` | **T6/T6c: a receipt whose 14 payload lines all say `closed=0` and whose 14 case lines all say `verdict=fail mutants=0/1` PASSES** (id-presence counting, no consistency limb). T14: a stale second `suite-sha256=` line is tolerated (first-match extraction) | FIX — highest priority (F1–F3) |
| E11 | D2 — LOG correction of the false r36-fixtures path | LAST `## …Round[- ]?37…` LOG block: `Correction (round 37)` ≥1 ∧ path named ≥1 ∧ falsity word ≥1 (three independent block-wide counts) | **T12: the falsity word satisfied by an UNRELATED line** ("some unrelated path is not present anymore") while the correction line itself states no falsity. Also: no absence limb — the claim's own grounding (`git ls-tree shows r36-fixtures absent`) is unused | FIX (F8–F9) |
| E12 | D4 — anchor-ancestor label + stale-label absence | LAST `## …Round[- ]?37…` SCORECARD block: `c20300df` ≥1 ∧ `anchor[- ]ancestor` ≥1 ∧ literal `Final lane commit: e666d902` =0; lesson file exists with both tokens | **T7: stale label in the FIRST round-37 block escapes** (last-block scoping). **T8: wrapped stale label escapes** (hash on the next line — the house form at SCORECARD:987/1129). Tokens need not be co-located (documented limit). All-blocks scanning also removes a latent FALSE RED (a later `## Round-37 …` block, cf. `## Round-33 capabilities` at SCORECARD:1097, would become "last" and miss the label) | FIX (F4–F6) |
| E13 | D5 — registry row single-choice type + exit-2 verdict | ≥1 r36-closure.sh registry row (escape-aware cell parse) with type ∈ {gate,probe} ∧ verdict cell matching `2[^[:alnum:]]{0,8}could-not-evaluate` | **T11: passes with the malformed row still present** (registry-rows=2, single=1, exit2=1) — the draft's documented append-only-correction semantics. Defensible under the claim's wording, but the L1 must choose the convention consciously (F10). Unescaped `gate\|probe` shifts cells and cannot satisfy exit2 — acceptable | DECISION (F10) |
| E14 | D6 — fail-closed BY SHAPE on the committed suite bytes | export's `corpus/instruments/r37-closure.sh`: assembled `porcelain:-0` needle =0; per-line swallow scan (`2>/dev/null`, `|| true`) over lines containing `status --porcelain` =0; ≥1 read site; `status-read=failed` marker present | **T9b/T9c: a status read split across lines with the suppression on the CONTINUATION line escapes the per-line scan** (both `2>/dev/null` and `|| true` variants). Self-scan fragility: the header comment co-locates the `status --porcelain` literal and the `|| true` spelling on adjacent lines — a naive window fix would false-red the suite's own bytes | FIX (F11–F12) |

Carried-check drift check: `check_e2/e4/e5/e6` byte-identical to r36; `check_e3/e7/e8` differ in COMMENTS only (trimmed rationale lines) — logic identical. E1 differs by design (round-37 scoping). No semantic drift in the carry-over.

## 2. Demonstrated false greens (probe evidence, all reproducible from scratch)

| id | probe | fixture | result |
|---|---|---|---|
| T6/T6c | E10 vs internally-inconsistent receipt | 14 payload lines `closed=0`, 14 case lines `verdict=fail mutants=0/1`, forged `closed=14/14 exit=0` + `cases=14 failures=0`, CORRECT executing-suite digest | **check_e10 rc=0 — FALSE GREEN** (on both draft versions) |
| T7 | E12 vs multi-block SCORECARD | first round-37 block carries `Final lane commit: e666d902…`, last block is clean+bound | **check_e12 rc=0 — FALSE GREEN** |
| T8 | E12 vs wrapped stale label | `**Final lane commit:` + hash on next line inside the round-37 section | **check_e12 rc=0 — FALSE GREEN** |
| T9b/T9c | E14 vs continuation-line swallow | status read split with `2>/dev/null` / `|| true` on the next line | **check_e14 rc=0 — FALSE GREEN** (both variants) |
| T12 | E11 vs falsity-elsewhere | correction line names the path without a falsity word; an unrelated line in the same block says "not present" | **check_e11 rc=0 — FALSE GREEN** |
| T13 | E1 vs unbound hash in first round-37 block | first block binds `0123…4567`, last block binds the real head | **check_e1 rc=0 — FALSE GREEN** (`round37-final-lane-commits=1,bound=1` — the first block's hash was never counted) |
| T14 | E10 vs stale second digest line | current-digest header first, `suite-sha256=000…0` line later | check_e10 rc=0 — minor false green (first-match extraction) |
| T11 | E13 vs malformed+conforming rows | round-36 malformed row + appended conforming row | check_e13 rc=0 (`registry-rows=2,single-choice-type=1,exit2-verdict=1`) — the DESIGNED ≥1 semantics; L1 decision F10 |

## 3. What holds (positive evidence, exercised this round)

- **Required reds hold with the draft suite**: `--export-ref cc692008…` → `closed=4/14 exit=1` (open: E1, E3, E4, E8, E9–E14); `--export-ref a23dc478…` → `closed=7/14 exit=1` with **E10–E14 all open there exactly as the claim predicts** (E13 payload `registry-rows=1,single-choice-type=0` — the malformed row is correctly not single-choice; E14 `suite-file=0`). Note E9 is ALSO red on both stale refs (`head-match=0`) — the staleness guard guarantees the reds independently of E10–E14.
- **Plain-run refusal**: no-args run → exit 2 with the refusal message (kill-rule shape).
- **E9 fail-closed rewrite is behaviorally real**: corrupt `.git/index` fixture → `git status --porcelain` rc=128 (`fatal: .git/index: index file smaller than expected`) → E9 rc=1, payload `status-read=failed,status-dirty=?,scratch-seat-dirs=0,head-match=1,lane-root=1` — a failed read is RED and the dirty count prints `?`, never 0. The draft's selftest includes this exact mutant (`status-read-failed`, needle `status-read=failed`).
- **Positive path is achievable end-to-end**: draft (ed88f880) against the builder's fixture lane `80b1cc1…` → `closed=14/14 exit=0`, E10 `digest-match=1` against the fixture's committed receipt; `--selftest` there → `cases=14 failures=0` exit 0, 48 mutants all rejected (4,3,5,1,1,1,2,4,5,6,4,6,3,3), all 7 report forgeries rejected (summary-only, case-lines-only, failed-cases, detail-free, 13-cases, duplicate-id, own-report accepted).
- **Kill-rule shape on the draft bytes**: `grep -cF 'porcelain:-0'` = 0 (needle assembled at runtime); the draft bytes pass their own E14 shape check; `bash -n` clean on both versions.
- **E10's digest binding works**: the fixture receipt embedded the PREVIOUS draft's digest; running the current draft over it reds `digest-match=0` — a receipt from a different suite version cannot pass. (This is also the operational warning in I1.)

## 4. Design fixes the L1 must apply when integrating

**F1 (E10, must) — payload/summary consistency.** For each id E1..E14 require a line matching `^<id> payload=.* closed=1$` (14 of them), not merely `^<id> payload=`. Kills T6: a receipt whose payload lines disagree with its own summary line cannot pass.

**F2 (E10, must) — judge the receipt's selftest section with the suite's own rule.** Add `judge_selftest_report "$p"` (already implemented: 14 case lines, all `verdict=pass`, per-id exactly-once, `mutants=<ok>/<n>` with n≥1, per-id `selftest detail=` lines matching n with rejected=ok=n, exact summary line) as an additional E10 limb. Kills the verdict=fail-case-lines forgery and the detail-free vacuous receipt — notably the builder's own hand-built fixture receipt (case lines `mutants=1/1` with NO detail lines) would be rejected, forcing the committed receipt to be a genuine full transcript. Compatible with genuine output: the genuine transcript satisfies every clause.

**F3 (E10, should) — digest-line totality.** Require count of lines containing `suite-sha256=` == count of lines containing `suite-sha256=$want` (≥1): no stale digest line may coexist with the current one (T14).

**F4 (E12, must) — all-blocks scoping.** Iterate EVERY `^## .*Round[- ]?37([^0-9]|$)` block in SCORECARD.md: absence limb = NO round-37 block contains the stale label; presence limb = ≥1 round-37 block contains both `c20300df` and `anchor[- ]ancestor`. Kills T7, removes the latent false-red from a later `## Round-37 …` block, and matches the kill rule's "appears nowhere inside the round-37 SCORECARD section".

**F5 (E12, must) — wrapped-label window.** Within round-37 blocks, for each line matching `[Ff]inal lane commit`, collect hex tokens from that line and the next 2 lines; red if any collected token starts with `e666d902`. Keep the single-line literal grep too (it is the kill rule's literal and matches today's bytes at SCORECARD:1492). Kills T8 and covers backtick/spacing variants.

**F6 (E12, should) — token conjunction.** Require a `c20300df`-carrying line within 2 lines of an `anchor[- ]ancestor`-carrying line (same line tolerated) in the section and in the lesson — kills independent-token satisfaction while tolerating the house's adjacent-cell/wrap layout (the draft's documented limit becomes a bounded window instead of "anywhere in the section").

**F7 (E1, should) — all-blocks binding.** Every 40-hex token on/after a `Final lane commit:` line in ANY round-37 block (not just the last) must resolve and be an ancestor of the export ref. Kills T13.

**F8 (E11, must) — same-line conjunction.** The falsity word must be on the SAME line as the named path (require a line matching `corpus/instruments/r36-fixtures/` AND one of `absent|never committed|does not exist|not present`). Kills T12. The L1's LOG correction must then be one line carrying all three tokens.

**F9 (E11, should) — absence limb.** Add `[ ! -e corpus/instruments/r36-fixtures ]` under the export (payload `path-absent=`) — the claim's own grounding ("git ls-tree shows r36-fixtures absent") becomes a checked limb instead of prose.

**F10 (E13, decision — pick one convention and make E13 match).**
- Option A (in-place row fix): require ZERO r36-closure.sh registry rows whose type cell is the literal `gate\|probe`, AND exactly one r36-closure.sh row total, well-formed. Honest fix; note SKILL.md edits have been append-only in observed rounds, and one edited line does not move any density claim filed this round.
- Option B (append-only correction, the draft's stated assumption): require exactly ONE conforming row (`single==1 && exit2==1`, not ≥1) AND that row must be the LAST r36-closure.sh row in registry-section order (recency = authority). Kills the two-divergent-fixed-rows hazard that plain ≥1 admits (T11 passes today by design).
- Either way the landed row must carry: type cell exactly `gate` (or `probe`) and a verdict-map cell containing `2 -> could-not-evaluate` (the registry's `->` arrow convention, cf. SKILL.md:981). Keep the escape-aware cell parse (`e13_rows` sentinel approach) — naive `-F'|'` splitting is unusable on these rows (NF=13).

**F11 (E14, must) — continuation-aware swallow scan.** For each NON-COMMENT line containing `status --porcelain`, scan that line AND — iff it ends with `\` — the next line for `2>/dev/null` and `|| true`. Exclude comment lines (first non-space char `#`) from the scan entirely: the current header comment co-locates the `status --porcelain` literal and the `|| true` spelling on adjacent lines, so a naive window scan would false-red the suite's own bytes. Kills T9b/T9c.

**F12 (E14, should) — assemble the scan pattern.** Build the `status --porcelain` scan pattern at runtime (e.g. `status --$(printf porcelain)`) so E14's own command lines never enter its own scan; keep the assembled `porcelain:-0` needle (verified 0 occurrences in the draft bytes — the external kill-rule grep stays 0).

**F13 (selftest, must after F1–F12) — add the mutants that prove the new limbs.** The current mutant set mirrors only the current, weaker checks — every false green in §2 is invisible to the selftest. Add: E10 closed=0-payload-lines mutant + verdict=fail-case-lines mutant; E12 multi-block-stale mutant + wrapped-label mutant; E14 multi-line-swallow + `|| true`-continuation + no-read-site mutants; E1 unbound-hash-in-first-block mutant; E11 falsity-elsewhere + path-present mutants. Each must be rejected with the limb named in the payload.

## 5. Integration requirements (operational, for the L1)

- **I1 — freeze the suite bytes before generating the receipt.** The receipt must embed the digest of the FINAL committed suite bytes. Demonstrated: the builder's fixture receipt (previous draft's digest) reds `digest-match=0` under the current draft. Any post-receipt suite edit — even a comment — invalidates the receipt and forces regeneration.
- **I2 — fixed-point receipt protocol** (E10's digest limb makes the receipt self-referential; the draft's documented limit already concedes the embedded run names an earlier head):
  1. Land all round-37 artifacts + the suite; commit (H1, tree clean).
  2. Run plain mode at H1 → harvest the 13 genuine payload lines (E10 red: no receipt yet).
  3. Write the draft receipt: digest header + the 13 harvested payloads + the predicted E10 payload + `closed=14/14 exit=0` + predicted selftest section (case lines `verdict=pass`); commit (H2).
  4. Run plain + selftest at H2 (tree clean, HEAD=H2, scratch root empty) → genuine transcripts in which every check passes (E10 reads the draft receipt — shape-correct → green).
  5. Verify the genuine E-lines match the draft's predicted lines; replace the draft receipt's content with the genuine transcripts (same shape); commit (H3).
  6. Re-run at H3 and diff the E-lines against the committed receipt — they must be byte-identical (E10's payload is a pure function of receipt shape, which is unchanged). This re-run IS the fixed-point proof; without it the receipt's embedded `closed=14/14` is an unverified claim.
- **I3 — final-state ordering.** The counting commands run live: HEAD must equal the export ref named to the judge (E9 head-match), the worktree must be clean, and the scratch root must have NO directories left — the seat-dir limb counts ANY directory, including the L1's own `l1prep` (stricter than the claim's "seat dirs"; fail-closed, keep it, but the L1 must remove `l1prep` too). All 64 seats' scratch dirs must be gone first.
- **I4 — wording pins for the artifact seats** (the checks bind exact tokens): LOG round-37 correction = one line containing `Correction (round 37)` + `corpus/instruments/r36-fixtures/` + a falsity word (`absent` / `never committed` / `does not exist` / `not present`) — F8 makes this mandatory; round-37 lesson + SCORECARD round-37 section = `c20300df` + `anchor ancestor` (one line or within 2 lines, F6); the r36-closure.sh registry row per F10; the round-37 SCORECARD section must NOT co-locate `Final lane commit` with `e666d902` in any spelling or wrapping — word the correction so the stale label is not quoted verbatim inside the round-37 section (put it in the lesson/LOG instead).
- **I5 — re-verify the fixes against the FINAL draft.** The draft is a moving target (builder still iterating; two versions reviewed here, comment-only delta). This review's fix list is what to check, not a patch; the L1 must confirm F1–F13 against the bytes it actually lands, and the selftest (with F13's mutants) must pass on the fixture lane before the receipt is generated.

## 6. Residual risks (accepted, documented — not defects)

- **Byte-shape checks cannot prove genuineness.** Even after F1–F3, a determined forger can fabricate an internally consistent receipt with the correct digest. The ultimate controls are outside E10: the digest binds the receipt to one suite version, and the claim's counting commands re-run the suite live — the judge's fresh `closed=14/14` plus a diff against the committed receipt is the genuineness proof. State this in the report rather than implying E10 proves more than it does.
- **E9 scratch-root=absent passes** (payload-visible only) — carried r36 semantics; at the final verification the default root exists, so the limb measures. Optional strengthening: red when the root is absent AND `--scratch-root` was not overridden.
- **E9 ignored files are invisible to plain `--porcelain`** — carried r36 semantics; the spot-check used the same read.
- **E1/E2/E7/E8's `${var:-0}` defaults** turn a failed grep read (existing-but-unreadable file) into green — the same CLASS as D6 on non-mandated limbs; exotic (requires an unreadable existing file). Optional hardening: `[ -r FILE ] || exit 1` before those greps. The claim mandates fail-closed only for E9's status read.
- **E1's documented limit**: prose placeholders ("the L1 fills this line in") are not matched — carried from r36, unchanged scope.

## 7. Scope, side effects, tooling

- **Writes:** this receipt only (written last). Scratch `/fast/scratch/hyaku/kasegi-r37/RevC1Suite/` (draft snapshots, probe fixtures, run transcripts) removed at yield.
- **Read-only everywhere else:** no file in the lane, fleet, sibling lanes or source trees modified; no mutating git command (only `rev-parse`, `log`, `ls-tree`, `archive` via the draft suite's own export path, `status` via the draft's `--no-optional-locks` read, `diff`, `cat-file` via check functions). The two `git init` calls (T5 fixture, draft's own E9 selftest fixture) ran inside verified scratch toplevels per the fixture rule.
- **Tooling:** no installs or upgrades (system bash 5.3.20, git 2.56.0, GNU awk/grep/sed/tar/sha256sum). `pacman` untouched.
- **Verification gaps:** the draft's positive path was exercised on the builder's FIXTURE lane, not on the real lane head (the round-37 artifacts do not exist at `b362068…` yet — mid-wave). The real-head `closed=14/14` remains the L1's to produce via I2; the required reds and every false-green claim in §2 were exercised for real.
