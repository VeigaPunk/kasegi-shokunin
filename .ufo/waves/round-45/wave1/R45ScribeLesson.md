VERDICT: DRAFT-READY

Scope: R45ScribeLesson, lesson drafter. Deliverable: `.ufo/waves/round-45/wave1/R45ScribeLesson.draft/lesson-skeleton.md` (skeleton of `corpus/lessons/round-45.md`, shape of `corpus/lessons/round-44.md`). No production file, git index, or other lane was touched. No tool was installed or upgraded. Scratch removed on exit.

## F1 — the mined mistake (M45-1) and its class

Attacked: the round-44 S070 reject reason, as the candidate for `## Mistakes`.

- `sed -n '76p' corpus/SOURCES.md | awk` → status cell `rejected`; reason cell "REJECTED: the page's accessible body is a JavaScript shell and its metadata is a directory welcome…"; recheck `180d`; used-by `—`.
- `grep -n 'JavaScript shell' corpus/lessons/round-44.md` → `22:...` and `131:- **Reject — S070, tier C, ...` (same premise).
- `corpus/lessons/round-44-verifier-spotcheck.md:66` (§4) says the same directory is readable at `…/rest/v1/articles/about/rules/about-this-section` (HTTP 200, 10 029-char body); `:79` (§6 item 1) routes the fix.
- Class chosen: `stale-premise` (alternative `scope` recorded in the draft). The scope verdict survived; the premise (body unreadable) was false under the capture method the admit used.
- Captured-by: `grep -niE 'capture method|parity|capture-method' corpus/QUALITY.md` printed nothing at base, so no existing criterion covers it → `none`, routed to R49 (drafted by the sibling `R45ScribeQuality`; not yet landed when I read the tree).

## F2 — the gate quotes, re-located and verified

Attacked: the two gate rows (S071 admit, S072 reject-with-correction), and the five S071 manifest quotes plus S072 quotes, against the pinned snapshots.

Commands and printed output (verbatim):

- `sed -n '310,311p' S071.txt` → `the reporter or an affected party for up to 7 calendar days from the start` / `of the release process, with an exceptional extension to 14 calendar days`. Located with `grep -nF`: lines 310 and 311.
- `sed -n '148,149p' S072.txt` → `   <td>Security issues affecting any Google Cloud product or web service that` / `handles reasonably sensitive user data`.
- Normalised-whitespace locator over the manifest (run in scratch; output verbatim):
  ```
  S071 Q1 anchor 310 words 21 located(start,end)= [(310, 311)]
  S071 Q2 anchor 95 words 16 located(start,end)= [(95, 96)]
  S071 Q3 anchor 39 words 5 located(start,end)= [(39, 40)]
  S071 Q4 anchor 41 words 19 located(start,end)= [(41, 43)]
  S071 Q5 anchor 20 words 10 located(start,end)= [(20, 21)]
  S072 Q1 anchor 148 words 16 located(start,end)= [(148, 149)]
  S072 Q2 anchor 1 words 10 located(start,end)= [(2, 3)]
  ```
- `python3 corpus/instruments/source-recheck.py --manifest …/round-45/manifest.json --source S072` (committed lane script, read-only) → `S072:sha256 OK` / `S072:Q1 OK normalized=markup-whitespace occurrences=1 anchor=148-ok` / `S072:Q2 OK normalized=markup-whitespace occurrences=1 anchor=1-ok`, exit 0. The same for `--source S071`: five `OK` lines, `anchor=310-ok`, `95-ok`, `39-ok`, `41-ok`, `20-ok`, exit 0.
- Sizes: `S072.txt` has 10,032 bytes, 10,030 characters including the final newline, 10,029 characters without it. That matches the `10029` size token the correction must carry. `S071.txt` is 20,152 bytes, 372 lines, sha256 `0918dcfa…346f40` (matches the manifest).

Finding (defect in the frozen manifest, disclosed, not fixed by me): S072 Q2 declares `anchor` 1, but the quote is at lines 2–3. The checker passes it because `corpus/instruments/source-recheck.py:110` reads a four-line window from the anchor. Routed as open question 1 in the draft.

## F3 — do-nothing controls, re-run

Attacked: the frozen counters, graded at the do-nothing base. The counter bytes come from the freeze commit (`git archive 8cf62c8… corpus/instruments`); the tree is a copy of the pure base export.

- `python3 corpus/instruments/r45-routed-defects.py --root <base> --baseline <base>` →
  ```
  limb R1 fixed=0 read=row-S072=absent
  limb R2 fixed=0 read=quality-not-append-only-or-unchanged
  limb R3 fixed=0 read=selftest-rc=2-tokens=None
  limb R4 fixed=0 read=freeze-check-absent
  limb R5 fixed=0 read=refiled-absent
  routed-defects total=5 fixed=0 unresolved=5 exit=1
  ```
  The R1 limb behaves as the freeze expects (red at base).
- `python3 corpus/instruments/r45-c2-gate.py --root <base>` →
  ```
  gate G1 pass=0 read=rows=26 admitted=26
  gate G2 pass=0 read=F27-rows=0
  gate G3 pass=0 read=row-S071=absent-or-malformed
  gate G4 pass=0 read=manifest-absent
  gate G5 pass=0 read=F27-rows=0
  gate G6 pass=0 read=knowledge=63
  gate G7 pass=1 read=census-rc=0
  c2-gate fixed=1/7 exit=1
  ```
  Matches the frozen `expect_before` (`c2-gate fixed=1/7 exit=1`).
- `python3 corpus/instruments/r44-frontier-count.py --root <base> --expect 27` → `frontier rows=26 admitted=26`, `frontier expected=27 admitted=26 verdict=SHORT exit=1`. Matches the frozen secondary.
- The marker-only and fabricated controls are in `.ufo/waves/round-45/controls/freeze-controls.txt` (`controls total=5 red=5 green=0`). I did not re-run them; the draft labels them as freeze-recorded.

## F4 — what I did not verify

- The "fix shown able to fail" row (red-before receipt for the R1 fix on a pre-correction tree) is `<L1 fills>` in the draft. It needs the landed S072 row and the correction, which do not exist at base.
- The final-revision counter lines (`fixed=5`, `fixed=7/7`) are `<L1 fills>`. They need the landed tree.
- Tier letter of S072, its `flip:` clause, and the F27 knowledge entry are `<L1 fills>`.
- I did not re-fetch any source live. The S070 "JavaScript shell" premise is cited from the round-44 record and was not re-measured; the S071 and S072 quotes are verified against the pinned snapshots only.

## F5 — status / recheck / used-by changes

Verified at base: S070 status `rejected`, recheck `180d`, used-by `—`. Expected after landing: no change in these cells; the correction changes the reason text only. Listed as "none expected" with `<L1 confirms at tip>`.

## Limitations

- Pinned snapshots, not live content.
- The `captured-by` check covers `corpus/QUALITY.md` at base only; R49 is a sibling's draft and its landing is unobserved.
- The R45 wave-1 spec has 64 items; only one sibling draft (`R45ScribeRowsB.draft`) existed in `wave1/` when I checked, so "Assimilation: none" is conditional on the L1 confirming no sibling report differs.
- I invoked `r45-routed-defects.py --selftest` once with its output discarded to `/dev/null`; no result from it is cited.
- Scratch under `$HYAKU_SCRATCH/kasegi-r45/R45ScribeLesson/` (base copy, extracted counters, and outputs) was removed at exit.
