## Verification (all commands run by this seat in scratch)

**Do-nothing control vs patched tree — counter falsification.** Command: `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r47-routed-defects.py --root TREE`. Control tree = unchanged base `SOURCES.md` + the committed `corpus/source-snapshots/round-47/` copies; patched tree = same with this diff's result. Named control: **unchanged base SOURCES.md**.

```
control:  routed-defects total=11 fixed=0 unresolved=11 exit=1     # reproduces the frozen base reading
          limb L1 (D5) fixed=0 read=scaffold-phrases=4
          limb L2 (D5) fixed=0 read=bad=fence-markers=4,search-log-bullet-absent,s074-row-bullet-absent,capture-note-bullet-absent
          limb L8 (D7) fixed=0 read=row-S076=absent-or-duplicated hits=0
          limb L10 (D8) fixed=0 read=rest-api-lead-bullet-absent
patched:  routed-defects total=11 fixed=4 unresolved=7 exit=1
          limb L1 (D5) fixed=1 read=scaffold-phrases=0
          limb L2 (D5) fixed=1 read=bullets-landed fences=0
          limb L8 (D7) fixed=1 read=row-S076=ok          # includes manifest sha pin + source-recheck.py S076:sha256 OK
          limb L10 (D8) fixed=1 read=rest-api-lead-bullet-present
```

Exactly the four limbs this diff's bytes carry (L1/L2 = D5, L8 = D7 row, L10 = D8 lead) flip 0→1; the other seven read `corrections-section-absent` / `entry-absent` / `dropped-findings-unnamed` / `round-47-lesson-absent` in both trees and belong to the lesson/entry seats. Full outputs: `R47SrD5Diff.draft/ctl-counter.txt`, `fix-counter.txt` (exits 1 and 1).

**Round-trip.** Fresh copy of base bytes placed at `rt/corpus/SOURCES.md`; `(cd rt && patch -p1 -s < R47SrD5Diff.diff)` exited 0; `cmp rt/corpus/SOURCES.md patched-SOURCES.md` silent → **byte-identical**.

**Landed-bullet byte identity (card (a) "verbatim from the base fences").**
- `9d45acb40b2061aad660306919ca8d0f073231d81dc484d3ebf9052737e6ffdf` — F29 bullet, patched :115, `cmp` vs base :122 identical
- `374d7d75291d5062b69f2bc6e1afe5cfb0faee03a66deec66b6128424d2b9ada` — S074 bullet, patched :170
- `94c88984da5448fd3d95621fefd58cf32b181d8245984694d0e9245ceaf6d198` — capture-note bullet, patched :171
All three equal `R47ScoutScaffold.md`'s fence-content SHAs.

**Plain greps on patched tree:** `to append`=0 (base 2); ``` ``` ```=0 (base 4); `supersedes S074`=1 (base 0); `docs.github.com/en/rest/security-advisories`=1 (base 0); S-rows 74→76; live `| S076 |` rows=1.

**Byte math:** 124448 − 725 (scaffold) + 850 (S075 row) + 1044 (S076 row) + 375 (lead bullet) − 28 (S074 cell change) = 125964 bytes; 185 − 17 + 3 = 171 lines. Patched sha256 `a328e9cafa04b2fca9f1e8f0235ab23b856ac84cf6407694442cfb7ae6a9c16d`.

**Diff shape:** 3 hunks — `@@ -77,7 +77,9 @@` (S074 flip + row inserts), `@@ -110,23 +112,14 @@` (search scaffold + close fence −10, lead +1), `@@ -174,12 +167,5 @@` (registry scaffold + EOF fence −7); 18 deleted lines (17 scaffold + 1 replaced S074 row), 4 added lines.

## Cross-check vs R47ScoutScaffold.md

- Scout's 725 B / 17-line deletion map: **confirmed exactly** (measured `deleted-lines=17 deleted-bytes=725`).
- Scout's three fence SHAs: **all three reproduced** in the landed bullets.
- Scout's D5-only resulting digest `3eb1daa5…3e20` is intentionally **not** reproduced: this diff also lands the concurrent D7 row+flip, D8 lead and S075 row that Scout itself flagged as digest-invalidating. Combined-tree digest is the `a328e9ca…` above and will shift again as sibling seats land.
- Scout's D5-only line predictions hold modulo the +3 upstream lines: F29 bullet at patched :115 (= Scout's :113 + 2 rows), `## Leads (unopened)` at :117 (= :115 + 2), registry bullets at :170-171 (= :167-168 + 3).

## Drift note (for R47RevD5)

- No historical citation was rewritten: the F29 bullet's embedded `corpus/SOURCES.md:157` / `:74` references (attached to export `04af9bc92229232ea5cce8b32bfe59dd969eb26d`) pass through verbatim; the scaffold-local positional citations at base :115/:180 are deleted **with** the scaffold, as Scout prescribed.
- In the patched tree the REST-API lead sits at :122 and the F29 bullet at :115; downstream seats citing "SOURCES.md:122" for the F29 bullet (a base-tree habit) must re-anchor or cite by text, not number.

## Conflicts preserved verbatim (not suppressed)

- **Capture binding vs the S074 flip.** `R47RevD7`: "capture-binding-check.py B3 fails retained round-46-a2 record. Receipt `.ufo/waves/round-47/w1/R47RevD7.receipts.txt`; unchanged actual-record fixture EXIT=0, rejected EXIT=1." `R47ExecS074Flip`: "recommend keeping S074 mined and documenting explicit supersession, unless L1 intentionally migrates the binding contract." Via `R47SrRegistry`: `R47ScoutRegistry` printed `FAIL rule=rejected-row-anchor record=S074 row=S074 dir=round-46-a2` (`records=63 bound=62 unbound=1 exit1`). This draft follows the seat card's mandated flip (d) and flags the conflict to integration/wave-2; census expectation for the shared S074/S076 URL is warning-only W04 per `R47ExecS074Flip`'s fixture receipt (not rerun here).
- **Frozen L10 is prefix-loose.** Disclosed mutbat survivors `L10a-url-loose` / `L10c-url-invert` (`R47ExecSelftestReplay-mutbat.txt:40,42`) mean the counter cannot enforce the exact page, the not-opened honesty or the pointer semantics; this bullet meets them by construction (`R47RevD8`'s stated preference), and the semantic check remains wave-2/review duty.

## Limits

- The 34 disclosed mutation survivors (C1 16/35, C2 18/21, `baseline_failures=0`) are **not** re-litigated or claimed closed; per-seat bounded probes only (two counter runs) were run — not the full battery.
- L3-L7, L9, L11 are sibling seats' surfaces and stay 0 in this probe; integrated-tree grading (`fixed=11`) is the L1's gate.
- No census run by this seat; W04 expectations are inherited receipts, not measurements by this seat.
- S076 anchor sha `9bd8ab57…` and manifest pin `6168521b…` were exercised by frozen L8 + `source-recheck.py` against the committed manifest/capture in the patched tree (read=ok); the S075 row's `9dee8161…` pin is inherited from `R47SrRegistry`/manifest (`corpus/source-snapshots/round-47/manifest.json:6-23`), not independently re-derived here.
- Tools installed: none. Pacman: untouched (host-wide pause respected). Git: read-only `git show` only; no commit/push/index mutation anywhere. Fleet root, MANIFEST.json, `.ufo/state/`, siblings: untouched. `/home/vgpnk/Projects/shokuknow`: untouched. Disk guard seen before the pass: `/fast/scratch/hyaku 54% used, 377.0G free`.

## Receipts (all under `.ufo/waves/round-47/w1/R47SrD5Diff.draft/`)

`R47SrD5Diff.diff` (the embedded diff bytes), `patched-SOURCES.md` (125964 B result), `ctl-counter.txt`, `fix-counter.txt`, `ctl-exit.txt`, `fix-exit.txt`, `f29-base.txt` (2504 B fence original), `part1.md`, `part2.md`. Scratch `/fast/scratch/hyaku/kasegi-r47/R47SrD5Diff/` removed after copying.

Self-evaluation (1-5): accuracy 5 (every claim above is a command output or `cmp`/`sha256sum` result); completeness 4 (all five card items landed in one diff; entry/lesson limbs intentionally out of seat); clarity 4; actionability 5 (patch applies byte-identically to base bytes; order/cell semantics stated); conciseness 4. Overall 4.6. Would the user agree: this is a verified draft, not an integrated pass — the counter's `fixed=4/11` on the patched probe is the honest reading, with 0/11 as the do-nothing control.

Report: .ufo/waves/round-47/w1/R47SrD5Diff.md
