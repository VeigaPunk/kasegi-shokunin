=== BLOCK A: append to END of corpus/lessons/round-44.md (one physical line; L1 adds one blank separator line first) ===
Correction (round 45, appended 2026-10-28): the S070 reject reason above (`## Gate` and the S070 row) was wrong: the S070 body is readable through the article API (`https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section`, HTTP 200, 10029 chars; re-measured by the round-45 scribe on 2026-10-28 from the API JSON `body` field; pinned as `corpus/source-snapshots/round-45/S072.txt`, sha256 `364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025`, which carries one extra trailing newline, 10030 characters), so the JavaScript-shell reason does not hold. The true reason is "overview, no program-specific rule beyond S069 Q5": the directory's Cloud VRP row says "Security issues affecting any Google Cloud product or web service that handles reasonably sensitive user data" (`corpus/source-snapshots/round-45/S072.txt:148`, located across the line break at 149), which restates S069 Q5 and adds no customer-resource rule. The S070 row stays byte-identical as history; the superseding row is S072 (status `rejected`, teaches `supersedes S070`).
=== END BLOCK A ===

=== BLOCK B: append to END of corpus/README.md (L1 adds one blank separator line first) ===
## Round-45 admission — coverage map row and Frontier F27 (appended 2026-10-28)

The coverage map and frontier table above are not edited in place (R6). The round-45 entry
`corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` (F27, source S071) records the
Linux kernel's own security-bugs reporting process as published on docs.kernel.org: the private
security list, the report requirements (version range, reproducer, no binary-only executables),
the fix-release postponement ceiling (7 calendar days from the start of the release process, with an
exceptional extension to 14), and the process's refusal rules (AI-assisted finds treated as public;
unreproducible issues are not security bugs). Its evidence is limited to this one process page; it
does not assert how other projects or vendors handle disclosure.

| Area | Entry | Source basis |
|---|---|---|
| Linux kernel security-bugs reporting process: private report channel, release postponement ceiling and refusal rules (round 45) | `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` | S071 — docs.kernel.org security-bugs process page (`_sources/process/security-bugs.rst.txt` capture), opened 2026-10-28; capture and located quotes in `corpus/source-snapshots/round-45/manifest.json` |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F27 | Linux kernel's own security-bugs reporting process: the private security list, the 7-day release postponement ceiling with a 14-day exception, and the AI-found, binary-only and unreproducible refusal rules | admitted | `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` | S071 | Keep the kernel process distinct from other projects' and vendors' disclosure policies; re-open the process page before relying on its dated postponement figures. |

[r45 amendment, appended 2026-10-28] The 26/26 count on the round-44 amendment line above records the round-44 state and is retained as history (R9). At round 45 the public-practice frontier stands at **27/27 admitted** — F01-F26 as previously recorded and F27 admitted this round. The lost-domain denominator remains 0/18; the frontier count is separate.
=== END BLOCK B ===

=== BLOCK C: append to END of PROVINCE.md (L1 adds one blank separator line first) ===
[r45 Frontier amendment, appended 2026-10-28, end-of-file append per R6] F27 — Linux kernel security-bugs reporting process (private security list, 7-day release postponement ceiling with a 14-day exception, AI-found, binary-only and unreproducible refusal rules) — admitted round 45; entry `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` (source S071)
=== END BLOCK C ===

=== BLOCK D: append to END of SCORECARD.md (L1 adds one blank separator line first) ===
### Round-45 move-log rows (scribe draft — no score move claimed)

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 45 | depth:verifiability | 4 (round-44 score) | 4 held — **no score move claimed**. The five routed round-44 defects (spot-check §6 items 1-5) are graded by the frozen counter `corpus/instruments/r45-routed-defects.py`; any increment is only what that counter prints at the integration tree (`routed-defects total=5 fixed=<k>`), which this row does not assert | `corpus/instruments/r45-routed-defects.py`; `.ufo/waves/round-45/claims.json`; `.ufo/waves/round-45/controls/freeze-controls.txt`; `corpus/lessons/round-44.md` (Correction, round 45) |
| 45 | coverage | 8 (round-44 score) | 8 held — **no score move claimed**. Admitted frontier rows 26 → 27 with F27 is the measurable increment and holds only once the F27 row, knowledge entry and S071 registry row land at the integration tree; the counters are `corpus/instruments/r44-frontier-count.py --expect 27` and `corpus/instruments/r45-c2-gate.py` | `corpus/README.md` (Round-45 admission block); `PROVINCE.md` (r45 Frontier amendment); `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md`; `corpus/source-snapshots/round-45/S071.txt` |
| 45 | depth:density | 9 (round-44 score) | 9 held (non-target guard: `corpus/instruments/density.py` is not touched by the round-45 drafts) | `corpus/instruments/density.py` |
=== END BLOCK D ===
