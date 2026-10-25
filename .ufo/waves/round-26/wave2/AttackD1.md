# AttackD1 — round-26 lesson integrity audit (`corpus/lessons/round-26.md`)

Seat: `L1Kasegi26.AttackD1` (reviewer, read-only leaf). Date: 2026-10-25 (UTC).
Target: `corpus/lessons/round-26.md` (171 lines, incl. the appended `## Integration closure (2026-10-25)` block).
Method: direct read of the lesson against the wave-1 receipts (`.ufo/waves/round-26/wave1/`, `c1-controls/`, `c2-controls/`), the frozen `claims.json`, `SCORECARD.md`, and live re-runs of every frozen counter (all read-only; no lane writes; no tools installed — preinstalled `grep/awk/sha256sum/stat/git/python3/curl` used).

## Verdict

The lesson's gate block (admits/rejects/quarantine) matches the wave-1 data; the C2 kill-rule status is consistent with the final state via the appended `## Integration closure` block (the earlier §Gate/§Fixes/§Routed debt text is explicitly compose-time and superseded); fix-control #3 is restated correctly and records 0 (verified); the counters table matches the final measured values (verified live); access-date evidence is all today (2026-10-25 UTC); the four L1-closed open items are closed in the lesson. No fabricated outputs found. Two minor fidelity notes remain (item A3, B2 below). No unresolvable stale statement remains.

## 1. Gate block vs wave-1 data

- **Quarantine — seven verdicts, exact match.** `wave1/quarantine-verdicts.txt` contains exactly seven rows: `S037 fetched no-quote; S054 fetched no-quote; S048 unfetchable; S065 fetched quote-located; S068 already-mined-legacy; S069 unfetchable; S070 unfetchable`. Lesson §Quarantine table lists the same seven rows with identical classes (S037/S054 `payload-absent`; S048/S065/S068/S069/S070 `could-not-be-fetched`) and matching verdicts. Per-row evidence in the lesson (S037 200/24,189 B composite cells; S054 200/513,648 B line-wrap + legal-citation parenthetical; S048 404/748 B Tomcat `未找到`; S065 200/7,465,472 B fragments verbatim, wrap at PDF line break; S068 200/94,027 B quote located verbatim; S069/S070 302/0 B, TLS curl 60) matches `wave1/ScoutQuarantine.md` byte-for-byte in substance. "payload-absent / could-not-be-fetched remain the register's unchecked families" matches ScoutQuarantine's cross-cutting note.
- **Rejects — reasons + flips match.** Both rows in §Refused match `wave1/s3-inventory.txt` (staged shape: no `cd` prefix, prose+backtick+`(ran …)` rechecks; both fail 4/6 strict limbs) and the round-24/25 records. The Q3 four-vs-two claim was verified against the live snapshot: `S040-live.txt` L301, L302–L304, L305–L308, L309 are exactly the four expedite conditions (high-severity completion; observed active exploitation; potential public awareness; third-party high profile). `ground: F20` absent confirmed (s3 §6: no F20 row in lane frontier). Flip conditions are present and consistent (L1-level wording read in full via `:raw:54-55`). "No Q/R bar was relaxed" not contradicted by any receipt.
- **Admits.** S041 row claims (mined, JPCERT/CC 2026 guideline, 2,354 lines, 1,338,665 B → 147,267 B, sha256 `e18acbf9…`, utc 2026-10-25T12:34:17Z, status 200) match `wave1/ExecCaptureS041.md` and `on-disk` (`sha256sum`, `wc -l`, `stat`: 147,267 B @ 12:34:17Z). Manifest binds 7 quote assertions (`Q1a,Q1b,Q2a,Q2b,Q3,Q4,Q5`); `source-recheck.py --manifest … --source S041` runs exit 0 today with `occurrences=1` (Q2a `occurrences=2 anchor=1874-ok`). Staged S076/S064 → adopted S041 and S068 → already S040 match `claims.json` notes and s3 inventory (reg=40, staged=94, collisions=10 S031–S040). S5 quote locations (FULL 2009-2010, 2020, 2238, 2291, 2180/2225, 2382-2383; drift notes) match `wave1/s5-quote-relocation.txt` exactly.
- **No fabrication in evidence chains.** `claims.json` working-tree sha256 = `343e568e…` = blob at freeze commit `1b076fa7` (`git show 1b076fa7:.ufo/waves/round-26/claims.json | sha256sum`), so the R25-1 no-in-place-edit claim holds. Entries exist at claimed sizes (division 54 lines, crosswalk 67 lines) with Q1 headers (`source:` S041 + URL/anchor, `verified-at: 2026-10-25`, `recheck:` = `cd <lane-root> && python3 …/source-recheck.py --manifest … --source S041`) and body quotes matching the manifest text.

## 2. Kill-rule status vs final state

- **Compose text vs closure.** §Gate kill-rule status (line 78) says C2's "census exit ≠ 0 at round end" limb is "**not yet satisfied** and must be cleared before round close" and C1(b) "requires the receipt-index regeneration below before commit" (line 77). Those are compose-time statements, now superseded by the lesson's own `## Integration closure (2026-10-25)` block (lines 149-171), which records the four L1 resolutions and a "Final measured counters" table. I verified every closure row live:
  - Row 1: `c1-receipt-index.txt:2-4,13-14` — `instrument_sha256=3fc0d751…`, `selftest cases=15 failures=0 exit=0`, `## regeneration history` line. C1(b) closed. ✓
  - Row 2: `SOURCES.md` S040/S041 recheck cells now bare `180d` (awk-verified 11th column); final-URL/UA/fetch-procedure prose lives under `## Registry changes` (3 lines, incl. the two restoration rows). Census `validate --root /home/vgpnk/Projects/shokunin kasegi` exits **0** today, only pre-existing `W04 S028/S029`. E09/E11 cleared. C2 kill rule satisfied. ✓
  - Row 3: README F11 row cites actual unsuffixed filenames (`knowledge/iso-29147-and-30111-division-of-labour.md`, `knowledge/iso-29147-divergence-and-clause-crosswalk.md`); SCORECARD round-26 C2 row uses the same names; `frontier-recheck-count.py` live = `entries=14 pass=14 exit=0` (F11 contributes 2, both `ids=S041`). ✓
  - Row 4: `knowledge-expected.txt` = 39 entry lines (2 header lines), identical set to the 39 `corpus/knowledge/*.md` files (live audit `expect=present expected=39 missing=0 unexpected=0 exit=0`). ✓
- **Final measured counters (table lines 162-171) all re-run live:** C1a 1; C1b 1; C1c 0; C1d exit 1 `missing=<name>` (semantics; see B2); C2 awk 11; precise S041-citing 2 (frozen S04x grep reads 3 via S040 overmatch — consistent with M26-4, verified: the 3 files are `vendor-disclosure-policy-commitments-crosswalk.md` (S040) + the two S041 entries); census exit 0; frontier 14/14 exit 0.
- So the lesson's kill-rule status *does* match final state — via the closure block; the earlier §Gate/§Fixes/§Routed debt sentences remain as labelled historical compose records ("Earlier blocks are unchanged", line 151). If read without the closure block they are stale (see section 5).

## 3. Fix-control #3 (C1(c))

- The lesson restates the command exactly as in `claims.json`: `grep -rnE '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md | grep -v 'round-24.md:77' | wc -l`. Live result: **0** (verified). The only `62/77 assertions` occurrence in the three files is the retained historical `round-24.md:77` line ("…exits 0 over 19 records / 77 assertions."), confirmed with proper ERE alternation; excluding it yields 0.
- M26-6's mechanics verified: under `-E`, `\|` is a literal pipe, so the frozen pattern alone matches nothing; the recorded 0 is grounded in content ground truth, as the lesson says.
- Minor wording nit (no numeric error): §Fixes item 3 says "with it removed the same command returns 1 (round-24.md:77…)". Literally, removing the `grep -v` from the *frozen* command still returns 0 (the literal-pipe pattern never matches line 77); it returns 1 only when the content check is run with proper alternation (`62 assertions|77 assertions`). M26-6 already explains the distinction; the sentence in fix 3 should say "with proper alternation and the exclusion removed" to be strictly true.

## 4. Counters table vs final measured values

- Overview table after-values: C1(a) 1 ✓, C1(b) 1 ✓ (index now at `3fc0d751…`/cases=15), C1(c) 0 ✓, C1(d) exit 1 naming deleted entry ✓, C2 awk 11 ✓, C2 grep 3 (observed; ≥1 target) ✓. Row 15 (census "after") reads "exit 1 at compose — see §Gate kill-rule status and §Fixes item 5" — compose-state; the closure table's final table records exit 0. Both are present and labelled; no contradiction remains if read with the closure block.
- Appendix commands (lines 121-137) all re-run identical to the recorded values (1, 1, 0, 11, 3, 2 for precise S041); the appendix's "currently 1: E09 S040/S041" census note is compose-time, superseded by closure row 2.

## 5. Stale statements / open items (the L1 has closed all four)

The four open items recorded in §Fixes 2/5/6 and §Routed debt are all closed and are confirmed closed inside the lesson itself (closure table rows 1-4, all verified above):
1. C1(b) receipt-index regeneration — **closed** (`c1-receipt-index.txt` at `3fc0d751…`, cases=15).
2. C2 census exit (E09 on S040/S041 cells) — **closed** (cells cadence-only `180d`; prose in `## Registry changes`; census exit 0).
3. F11 row entry-cell names — **closed** (README + SCORECARD rows use actual filenames; frontier 14/14 exit 0).
4. `knowledge-expected.txt` stale at 37 — **closed** (regenerated to 39; live audit 39/39).

Residual wording (pointers to the closure, not false): lines 77-78, 82, 101, 110, 113-114, 136, 145-147 still phrase the four items as outstanding ("must be regenerated… must be cleared… at compose … exits 1… currently the index pins…"). They are explicitly kept as compose history by line 151; if the lane prefers zero stale phrasing, annotate each with "closed — see ## Integration closure" (cosmetic; no factual error remains once the closure block is read).

**B2 (fidelity, minor):** lesson fix 1(a) cites "verified on the landed bytes: `missing_entries=['corpus/knowledge/multiparty-vulnerability-coordination.md']`, exit 1". The landed-bytes deletion receipt I found (`c1-controls/e1-selftest-live.txt`, deleted-scratch) removed `vdp-disclosure-packages.md` (missing=vdp…, expected=37). `m1-d.txt` is a pre-fix deletion (exit 1 but unnamed). The `multiparty` name is not traceable to a receipt I located; the semantics (exit 1 + `missing=<name>`) are fully verified. Suggest pinning the exact fixture name used.

## 6. Access-date evidence (all today)

Lesson line 141 asserts every fetch/probe/receipt/counter ran 2026-10-25 UTC. Verified: claims freeze `2026-10-25T12:27:41Z`; S041 capture utc 12:34:17Z (= file mtime 2026-10-25 09:34:17 -0300); S040 probe 12:34:25Z–27Z (`s040-probe.txt`); C2 do-nothing 12:34:41Z (`c2-controls/do-nothing.json`); m1 batch 12:35:12Z–24Z (`m1-summary.json`); entries landed 12:39:49Z / 12:43:28Z (mtimes, within the lesson's 12:39Z–12:43Z window); closure/receipt regen 12:46:57Z–12:50:33Z (SOURCES/README/SCORECARD/index/live.json/lesson mtimes). No date outside 2026-10-25 appears in the lesson's record line (staged package `verified-at 2026-10-23` dates are historical and correctly labelled).

## Residual risk / verification gaps

- No applicable `lsp` server for markdown/registry artifacts; all semantic claims were verified against raw receipts, exact command outputs, and file bytes (no grep-only proof of semantics).
- The census re-run above was against the live lane (read-only validate); the lesson's and scorecard's claim of exit 0 at round close is confirmed.
- Deletion-fixture exit-0-before baseline (36/36) is taken from `claims.json` frozen values; a from-scratch before-state replay on 36-file bytes was not re-executed (only the after-state was exercised live). Not a defect — the after-state is the claim.
- Installs: none (no tool installed or updated).

## Files written (owned paths only)

- `.ufo/waves/round-26/wave2/AttackD1.md` (this report)
- `.ufo/waves/round-26/wave2/d1.md` (identical copy, per assignment's d1.md naming)
