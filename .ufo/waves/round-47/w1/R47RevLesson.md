# R47RevLesson — scoped lesson review

Axes: depth:verifiability; coverage. Review recommendation only; no admission or integration performed.

## Findings (severity order)

1. **Low — M47-5 overstates its captured-by rule.** Reviewed draft `.ufo/waves/round-47/w1/R47SrLesson.draft/round-47.md:17` names QUALITY R5 for an attempt without a valid report. `corpus/QUALITY.md:39` applies specifically to a round without a lesson. Fleet `.ufo/watchdog.log:1955` establishes only `FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B)`, not absence of a lesson. Keep R4; remove R5 unless a missing-lesson witness is supplied. The draft correctly preserves the report predicate's disjunction. Sent to the author.
2. **Low — M47-5 needs an explicit prospective failure condition.** Unlike rows M47-1..4 (`:13-16`), row `:17` gives the historical red witness and a must-land instruction, but no explicit condition under which its proposed fix fails. Add that the fix fails without a resolvable work commit/before→after measurement (R4) or if the report predicate still fails. This avoids treating merely recording the deaths as repairing landing. Sent to the author.

An additional status-contract mismatch in the first reviewed version (`:61`, historical used-by left unchanged) was acknowledged corrected by the author: frozen `claims.json:13` requires S074 used-by → `corpus/lessons/round-46.md`. Author also reports adding the exact REST sibling pointer `S076.txt:574` at `:48`. These updates were not independently re-opened during this review.

## Requirements checked

- All five Mistakes rows have class, evidence pointer, captured-by, and fix columns (`:11-17`). D5 landing, D6 stale-premise, D7 attribution/provenance and D8 reference-drift match actual inherited evidence in `corpus/lessons/round-46-verifier-spotcheck.md:179-215`; no invented defect required. M47-5 is genuinely this round: watchdog `:1955,1964-1965` records two failed attempts and attempt-3 launch. Report absence must not be inferred more narrowly than the logged predicate.
- M47-1..4 explicitly name how each fix can fail and cite actual red-before receipts. `controls/c1-base.txt:1-12` supplies all eleven failing limbs; `controls/selftest-receipt.txt:2-20` supplies the cited negative fixture results, not integrated success.
- Gate contains a bounded proposed admit (`:27,42-44`) and four rejects/deferred items with reasons and flips (`:46-51`). The broker rule preserves the unstated 120-day start event, contact-exhaustion condition, and faulty-patch-only tiers: compare S075.txt:23-26.
- Eight Gate quotes (`:31-38`) locate in S075.txt:23-26 and manifest Q2,Q3,Q5-Q10 (`manifest.json:30-74`); each is at most 25 whitespace-delimited words (Q3 and Q6 reach 25). No Q1 quotation is incorrectly included under that limit.
- Exact required tokens present: `ZDI` and `reservation` at `:55`; `S068` and `one GHSA advisory entry` at `:57`. These satisfy the *textual* conjunction used in `corpus/instruments/r47-routed-defects.py:313-318`; the surrounding prose also actually resolves the consumed reservation through S075 rather than promising an already consumed id.
- Four non-author spot-check slots (`:63-68`) identify the live URL, bounded decision-rule questions, frozen counter commands plus base identity, and exact D5 comparison requirements. These are answerable once the intended artifacts are committed; the live-reopen slot additionally requires network access, honestly distinguished from committed capture evidence. No slot asks the author to provide a private judgment or hidden artifact.

## Do-nothing discrimination and limits

Read, not rerun: `.ufo/waves/round-47/controls/c1-base.txt:12-13` = `routed-defects total=11 fixed=0 unresolved=11 exit=1`, EXIT=1; `c2-base.txt:8-9` = `f30-gate fixed=1/7 exit=1`, EXIT=1. `freeze-controls.txt:1` identifies these as do-nothing controls. Draft :19 correctly separates base C2 1/7 from freeze-tree 2/7, and positive fixtures from integration. This is documentary discrimination, not a fresh counter execution or proof the draft integration passes.

Draft :21 honestly discloses the observed 16 C1 + 18 C2 survivors, backed by `controls/mutbat-receipt.txt:36,58`; no zero-survivor or saturation claim. The 43-case selftest receipt is not equivalent to full mutation coverage.

`xd://lsp` was requested but is not mounted (tool response: `No such tool: xd://lsp`); semantic references/definition/diagnostics therefore unavailable. Used literal search and direct evidence reads only, not semantic proof. No builds, counters, full battery, live fetches, alternate agent runtime, or integration checks executed. No code caller/resume/runtime identity behavior is changed by this lesson review.

Residual risks: final freeze placeholder and proposed/landed wording require L1 integration; F02 overlap remains independent semantic review; fleet watchdog is not lane-committed evidence (`git -C /home/vgpnk/Projects/shokunin ls-files --error-unmatch .ufo/watchdog.log` exited 1), so preserve the quoted failure witness in committed round evidence if durable independent replay is required. This does not invalidate the observed deaths. Full integrated bytes and author follow-up changes remain unverified here.

No installs, delegation, background jobs, git/jj mutation, or scratch creation. Only this findings file was written by this reviewer; no scratch remains.

Self-evaluation: accuracy 4 (author follow-up not re-opened); completeness 4 (integration intentionally outside scope); clarity 4 (severity and evidence separated); actionability 4 (two exact row changes identified); conciseness 4 (scope and limits retained). Overall 4.0/5. Main improvement: verify the final integrated lesson against these two row findings and the declared spot-check slots.
