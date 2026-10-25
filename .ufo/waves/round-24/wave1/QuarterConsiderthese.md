# QuarterConsiderthese — considerthese/2026-10-24.md audit (kasegi r24)

Read-only seat. Target file: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-24.md`
(newest of six; `ls` dated 2026-10-25 03:35, content window 2026-10-21 08:12 → 2026-10-24 08:12 BRT).
Every claim below re-checked against the tree; the reflection is a pointer, not evidence.

## Findings (observed)

1. **The reflection is stale by ~20 h, and that is why three of five proposals look open.** It reads HEAD
   `8d2ce5a` and says "lane commits in the 3-day window: none". The r23 seal/rescue commits are dated
   `2026-10-25 03:35–04:01 -0300` (`953c278 … c2480b1`), i.e. after the reflection commit `7916542`
   (`2026-10-24 08:23:53`). Evidence: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin log --format='%h %ad %s' --date=iso -12`.
   Its factual premise ("still only S018/S029/S030, no manifest.json") no longer holds.

2. **Proposal 1 is half-landed: normalization yes, the "pin" no.**
   - Normalization: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py:24-29`
     (`MARKUP_RE`, `normalize()`), applied at `:135-141`; criterion Q8 at
     `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md:57`.
   - The pin conjunct is absent: `:135` is still a bare `in`; nothing counts occurrences or reads an anchor.
   - Live fixture (the one the proposal names): `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S029`
     → all 10 lines `OK`, **exit 0**, including `S029:art14-2a-early-warning`, although that phrase occurs
     **twice** under the tool's own `normalize()` (`S029.txt` lines 10 and 20; raw count 2, normalized count 2).
     A wrong-article binding of this assertion is machine-invisible.
   - Selftest has 4 cases only — `clean`, `corrupt`, `missing-source`, `missing-manifest`
     (`--selftest` exit 0); no duplicate-match, no anchor, no `<u>` case.
   - The only "exactly-once" discipline is prose: the r24 capture brief (`wave1-spec.json` item `CaptureTool`)
     demands assertions "exactly-once under the rechecker's `normalize()`", but the untracked
     `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` writes snapshots only —
     no manifest, no quotes, no occurrence check (`grep -n "quote\|manifest"` returns docstring lines only).
   - Scope of the defect in committed bytes: of the 30 assertions in the round-23 manifest, **exactly one** is
     non-unique (`S029:art14-2a-early-warning`, lines 10/20); the other 29 match once.

3. **Proposal 2 is closed in substance, by a different route than "re-capture S030".** `S030.txt` still carries
   74 `<u>…</u>` pairs, but `S031` (0 tags) supersedes it — `corpus/SOURCES.md:36-37` — and F07 now cites S031
   (`corpus/README.md:204`). So the tagged capture is historical and passes under normalization:
   `--source S030` prints `rule-4-1-9-independently-fixable OK normalized=markup-whitespace`, exit 0.
   Future captures strip markup at fetch (`capture-source.py:48-53, 83-96`). Residual not taken: only the derived
   rendering is committed — `capture()` discards `raw` after conversion and prints the *snapshot* sha256, not the
   fetched-bytes sha256 — so the raw→text transformation is not nameable at recheck time. Lower value than the pick;
   hand to QuarterQuality as a candidate only.

4. **Proposal 3 is landed.** `corpus/source-snapshots/round-23/manifest.json` exists with per-source sha256 pins and
   4 sources (S018/S029/S030/S031); `corpus/README.md:203-205` admits F06-F08 with S018/S031/S029; F08's Article 71
   quotes are `"Article 14 shall apply from 11 September 2026"` and `"This Regulation shall apply from 11 December 2027."`
   (`corpus/knowledge/cra-manufacturer-reporting-duties.md:51-52`); F07 is re-grounded to 4.2.6
   (`corpus/knowledge/cna-assignment-and-vulnerability-rules.md:25-40`). Item (b) "de-tag S030" was not done literally
   but is moot by supersession (finding 3).

5. **Proposal 4 (cadence) has no artifact and no observable state.** `grep -in "idle\|wall-clock" SCORECARD.md` → 0 hits.
   It is a João decision, not round-actionable.

6. **Proposal 5 is still open, external.** `pr://VeigaPunk/kasegi-shokunin/1` = **OPEN, Draft: true**, created
   2026-10-17T15:28:02Z, `updated` same second; 9 `origin/cursor|devin*` branches still present
   (`git branch -a`). No lane-side action available.

7. **Carry-overs, status.** (a) CVSS v4 → HackerOne/Bugcrowd severity lens: absent — `grep -rin "hackerone\|bugcrowd\|vrt"`
   over `corpus/knowledge/claim-gates.md`, `triage-thresholds.md`, `cvss-v4-severity-and-vector.md` → 0 hits; would
   need new SOURCES rows + captures, outside C2's F09 scope. (b) `test_anchorcheck.py` for `94aace2`: absent —
   `corpus/instruments/` holds `anchorcheck.py` but only `test_resolve.py` as a test; second-best pick (cheap, but no
   r24 claim depends on anchorcheck). (c) resolve.py fail-before fixtures: **already this round's C1(B) work** —
   untracked `resolve-dispatch-check.py` + `resolve-dispatch-fixtures.json`, `resolve.py` modified, `.ufo/waves/round-24/c1-fixed.json`
   = 8/8 vs the frozen 4/8 baseline; not a candidate. (d) idleness counter overlaps proposal 4.

8. **Coverage:** none of the five proposals names C2's subject (authorisation outside a platform's safe-harbour text).
   The reflection offers no coverage move this round; F09 must come from the package via the already-dispatched
   `EntryRoE`/`EntryStatute` seats.

## Pick — exactly one

**Proposal text (verbatim, `considerthese/2026-10-24.md:44-47`), second conjunct:**
> "…AND require each quote to match exactly once or carry a `SNNN.txt:LINE` anchor that must hold the match.
> Today's F07 `<u>` case and F08 double-match are the two ready-made fixtures."

**What it points at (opened):**
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py:135-141` — the assertion loop:
  `if assertion["quote"] in source_text: OK` / `elif normalize(...) in normalize(source_text): OK normalized=…`.
  No count, no anchor, no ambiguous status.
- The fixture: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-23/S029.txt:10,20`
  (same phrase in 14(2)(a) and 14(4)(a)) and manifest row `S029:art14-2a-early-warning`.
- The criterion it sits beside: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md:57` (Q8).

**Exact landing shape — QUALITY criterion (one new row), plus the dispatch it names:**
New row in `corpus/QUALITY.md`, captured-source table beside Q8:

```
| Q9 | A captured-source assertion is bound to one passage, not merely present somewhere in the capture: each
assertion's normalized quote must occur exactly once in the pinned snapshot, or carry an explicit anchor
(`SNNN.txt:LINE`, or an exclusive-context substring) that holds exactly one occurrence; a multi-match assertion
without a holding anchor emits `AMBIGUOUS matches=N` and fails. A uniqueness rule written in a capture brief is not
a pin while the committed rechecker only substring-matches. | considerthese/2026-10-24.md:44-47 (proposal 1, "pin"
conjunct); corpus/lessons/round-23.md M15; fixture S029:art14-2a-early-warning matches lines 10 and 20 and the
current recheck exits 0 |
```

**Implementation shape for the executor seat (private clone), stated exactly:**
1. `check_source()`: count occurrences on `normalize(source_text)` (collapsed, so cross-line quotes still match);
   if 1 → `OK`; if 0 → `MISMATCH`; if >1 → require an `anchor` key and pass only when exactly one occurrence's start
   offset maps to that line → `OK anchor=L`, else `AMBIGUOUS matches=N` and return 1.
2. Manifest: `anchor` is an additive per-assertion integer; validation touches only source `id` (`:63-72`), quote
   `id` (`:88-99`), `path`/`sha256` (`:81-86`), and the assertion loop reads only `id`/`quote` (`:133-143`), so
   `schema_version` 1 stays valid and the field is ignored until the dispatch lands.
3. Selftest additions (the proposal's two fixtures): duplicate-without-anchor → exit 1 `AMBIGUOUS matches=2`;
   duplicate-with-anchor → exit 0 `OK anchor=10`; `<u>`-markup quote → exit 0 `normalized=markup-whitespace`.
4. Retro-fit is one field: only `S029:art14-2a-early-warning` needs `anchor: 10` (14(2)(a)); the other 29 committed
   assertions are already unique, so F06/F07/F08 rechecks stay exit 0.

**Why it is not already done:** Q8 (`QUALITY.md:57`) mandates only normalization and the `normalized=` receipt; its
clause "an unnormalized substring match is not the only binding" is satisfied by the `normalize()` fallback, so a
*duplicate normalized* match still prints `OK`. `source-recheck.py:135` has no occurrence dispatch and ignores any
anchor; the four selftest cases contain neither fixture the proposal names; and the two rules that mention uniqueness
(r24 `CaptureTool` brief, M15) are prose and a manual manifest edit. Nothing in the tree implements it today:
`git status` shows `source-recheck.py` unmodified and `grep -n "Q9" corpus/QUALITY.md` → none. No sibling seat owns it:
`CaptureTool` writes snapshots only, `QuarterManifest` is documenting the loader as-is, and C1(B)'s resolver work is
separate (`resolve.py`, not the rechecker).

**Cost:** one function rewrite (~20 lines), three selftest cases, one optional manifest field, one table row. No fetch,
no snapshot change, no new SOURCES row, no verdict-class change. Directly hardens C1 counter A: 8/8 `recheck` exit 0 is
otherwise satisfiable by an assertion that matches two passages, which is exactly the F08 defect M15 recorded.

**Limits to state in the criterion (avoid overclaim):** the anchor binds to the pinned snapshot bytes, not upstream;
a sha256 mismatch already fails closed, and a re-capture invalidates anchors by design. A quote that is legitimately
repeated verbatim (boilerplate) must carry an anchor — that is the intended cost.

## UNVERIFIED
- Whether L1 will re-point F01-F05 `recheck:` lines at `corpus/source-snapshots/round-24/manifest.json` before or after
  the Q9 change (owned by `ScoutAnchor`/L1; round-24 manifest does not exist yet — only S001-S00x snapshots are written).
- Upstream PR/branch review (proposal 5) beyond the PR state and branch list above; no diff reviewed.
- No tool installs or upgrades were made; nothing was run that writes outside `/tmp`.
