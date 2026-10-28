# ScoutR42Defects — RD42-1..RD42-9 at HEAD

Seat: ScoutR42Defects. Lane HEAD `4cb6d4ae768481e1a14afbedc2d865a060ebacfd` (round-43 freeze commit, 2026-10-28 13:37:11 -0300). Base `ab98fac9dce87130bc4f66de89e30650d63943dc` is that commit's parent. Quoted bytes below are from HEAD, not from the spotcheck's memory. The spotcheck pointers still land on the same lines: the freeze commit did not rewrite SCORECARD.md, LOG.md, SHONEN.md, or `corpus/lessons/round-42.md`.

R9 (`corpus/QUALITY.md:51`): "Append the correction to historical lessons/logs rather than silently rewriting their filed assertions." Every "rewrite" or "delete the promise" action in the spotcheck is illegal. The legal close is an appended `Correction (round 43)` line, a new artifact, or a new claims-erratum file. Never an edit of the cited line.

Frozen owners (claims.json C1 predicate): K14 corrections literals, K15 wave-dispatch narrative, K16 placeholder promise, K17 claims before/after tokens, K18 quoted closed=/selftest values vs transcripts, K19 round-43 freeze ordering. The claim-design lesson names six defects (RD42-1, -2, -3, -4, -5, -6, -8). RD42-7 and RD42-9 are outside that six.

Live correction count, re-derived with `r42-closure.sh`'s own `fence_scan` + `^Correction \(round (\d+)\)` (outside fences) over SCORECARD.md/LOG.md/SHONEN.md: **34** (SCORECARD 19, LOG 7, SHONEN 8). The Y receipt `.ufo/waves/round-42/final-gates/all-gates.txt:16` prints `J11 payload=corrections=34,...`. The round-43 control `.ufo/waves/round-43/c1-controls/do-nothing.txt:22` prints the same `corrections=34` from the r42 suite at base. `SHENON.md` does not exist; the file is `SHONEN.md`.

## Ownership

| id | HEAD pointer | Honest machine pattern | Fix class (R9) | Owner |
|---|---|---|---|---|
| RD42-1 | `SCORECARD.md:1634` | `corrections=<n>` outside fences vs the J11 count, including a result sentence that quotes a payload | appended `Correction (round 43)` in SCORECARD.md naming `corrections=33` | K14, with the caveat below |
| RD42-2 | `LOG.md:1804` | slug `kasegi-r42-falsify` + `dispatched`, and `wave2-results.json` absent | appended `Correction (round 43)` in LOG.md, same file, words `never-true` or `not taken` | K15 |
| RD42-3 | `corpus/lessons/round-42.md:11` and `:16` | NOT visible to a slug pattern; visible only to a `round total` / `wave 2 dispatched` pattern | appended `Correction (round 43)` in that lesson, same file | K15 only if the limb does not require the slug |
| RD42-4 | `corpus/lessons/round-42.md:52-56` | section `## Wave-2 falsification` whose own body matches `when the … reports` | appended `Correction (round 43)` naming that heading. Do not delete or replace the section | K16, with the false-positive caveat below |
| RD42-5 | spotcheck `:65`, `claims-erratum-4.md:9`; fleet report is outside the lane | whole token `closed=10/13` and `selftest cases=13 failures=3` absent from the four transcript dirs | new artifact `.ufo/waves/round-43/final-gates/r42-at-de09313.txt` (the unedited tee) | K18, lane copies only |
| RD42-6 | `.ufo/waves/round-42/claims.json:6` | the wrongness is not in the export; K19 does not read this field | new claims-erratum naming the label; do not rewrite claims.json | not K19 |
| RD42-7 | `.ufo/waves/round-42/` absent `wave2-results.json` | absence of the results file is visible; "r43 ran the unexecuted attacks" is not | no byte change closes the process half | not owned; K15 covers only the false sentence |
| RD42-8 | `.ufo/waves/round-42/claims.json` C1 before | whole token `closed=10/12` vs `c1-controls/do-nothing.txt`'s `closed=8/12` | new `claims-erratum*.md` in `.ufo/waves/round-42/` quoting the token and `superseded` | K17 only on that one token |
| RD42-9 | `SHONEN.md:232-285` | `^## Round N evidence` plus a multiline box | prospective append of four single lines, no new heading. The r42 block cannot be closed | none of K14-K19 |

## RD42-1 — stale `corrections=33`

`SCORECARD.md:1634` (outside any fence), a `Correction (round 42)` line:

> Correction (round 42): D-r41-1's measurement is no longer pending: the r42 suite at Y prints `J11 payload=corrections=33,groups=4,dups=4,excused=4,unexcused=0,marker=1,marker-substantive=1,marker-appended=1,eof-closed=3/3,fenced=0 closed=1` (`.ufo/waves/round-42/final-gates/all-gates.txt`, instrument `corpus/instruments/r42-closure.sh`), …

That is the only `corrections=<n>` literal outside fences in SCORECARD.md, LOG.md, and SHONEN.md. `groups=4` on the same line matches the Y receipt. The count is 34 because this line is itself a `Correction (round ` line: the sentence reports the tally from before it was appended.

Machine pattern that sees it: reuse `check_j11`'s `correction_lines` (the `^Correction \(round (\d+)\)` matcher, outside fences, three records) and compare every `corrections=<n>` / `groups=<g>` literal in those records to that count. A same-file later `Correction (round 43)` line that quotes `corrections=33` verbatim as superseded is the R9 close. Do not edit line 1634.

**Cannot be implemented as the K14 prompt is written.** The prompt says a literal on a line whose text also carries `payload=` is evidence, never a result. Line 1634 contains both `payload=` and `corrections=33`. Excluding it yields stale=0, so K14 is closed at base, which the C1 kill rule forbids. The exclusion has to be narrower than the line: drop transcript rows and fenced defect logs, but keep a `^Correction (round ` sentence that asserts the suite's result. `SHENON.md` in the prompt and in the frozen predicate is a misspelling; requiring that path to exist fails the limb for a file that is not there. The defect itself is in SCORECARD.md, so the misspelling does not hide RD42-1, but the third record the limb must actually read is SHONEN.md.

## RD42-2 — LOG wave-2 sentence

`LOG.md:1802-1804` (the spotcheck's pointer is 1804):

> - Wave shape: wave 1 `kasegi-r42-build` 64 seats — executor 19, scout 11, critic 8, reviewer 8,
>   scribe 7, mutation-tester 5, connector 2, sentinel 2, simplifier 1, revenger 1
>   (`.ufo/waves/round-42/wave1-dispatch.json`); wave 2 `kasegi-r42-falsify` 36 seats dispatched against the repaired head; dead seats counted from `wave2-results.json` in the round report.

Observed at HEAD: `kasegi-r42-build-results.json` and `kasegi-r42-build.ready.dispatched` are tracked. `kasegi-r42-falsify.ready` is tracked. `kasegi-r42-falsify.ready.dispatched` is absent. `wave2-results.json` is absent (`git ls-files` empty; `test -e` ABSENT). `wave2-dispatch.json` `counts.spawn` is 36 and the tasks array length is 36. Roles: reviewer 7, critic 13, mutation-tester 11, scout 2, connector 2, sentinel 1. Attack roles reviewer+critic+mutation-tester = 31; plus sentinel = 32.

Machine pattern that sees RD42-2: a clause containing `kasegi-r<NN>-<word>` and `\bdispatched\b`, with the results path `.ufo/waves/round-<NN>/<wave>-results.json`. The committed missing name is `wave2-results.json`, not `kasegi-r42-falsify-results.json`. A limb that concatenates the slug with `-results.json` looks for a file the round never used. Parse `wave 2` from the sentence onto `wave2-results.json`. Close: appended `Correction (round 43)` in LOG.md naming `kasegi-r42-falsify` and `never-true` or `not taken`. A correction only in a new round-43 lesson does not satisfy "same file".

The wave-1 half of the same bullet is true (64 seats, results file present). The limb must split on the semicolon, not grade the whole bullet as one sentence.

## RD42-3 — lesson sentences have no slug

`corpus/lessons/round-42.md:9-16`:

> Shape: two v1 waves; wave 1 `kasegi-r42-build` dispatched 64
> seats (32–64 band), and wave 2 and the round total are counted from the wave-2 dispatch when it lands,
> never estimated: wave 2 dispatched 36 seats; the round total is 100. …
> Attack share: wave 1 `kasegi-r42-build` 21/64 = 32.8% …; wave 2 and the round total are counted
> from the wave-2 dispatch when it lands: 36 seats, 32 attack roles.

Line 9 names `kasegi-r42-build` and `dispatched`. That one is backed: `kasegi-r42-build-results.json` exists. Lines 11 and 16 are the defect and contain neither `kasegi-r42-falsify` nor any `kasegi-r<NN>-<word>` slug. A limb that "parses the wave name from the sentence itself" has nothing to parse, so it cannot require `wave2-results.json` and cannot demand a correction. The parenthetical "or gives a `round total` for such a wave" is the only hook, and "such a wave" is not named.

**RD42-3 cannot be machine-checked by the slug rule.** An honest extension is: a sentence that states `round total is <N>` or `wave 2 dispatched <N> seats` with no results file is unbacked. That extension false-fires on historical lessons (`round-40.md:9` "round total 50/89") unless it is bound to a sentence whose round is explicit. The spotcheck's prescribed fix ("correct in the r43 lesson/QUALITY record") is the wrong file: K15 requires the correction in the same file as the sentence. Append to `round-42.md`. Do not rewrite lines 11 or 16.

Same-line false positives a slug+`dispatched` scan already produces:

- `corpus/lessons/round-42-verifier-spotcheck.md:34` — wave 1 `dispatched` and wave 2 `kasegi-r42-falsify` … `undispatched` share one line. `\bdispatched\b` does not match `undispatched`, but a line-level AND of the falsify slug and the word `dispatched` flags a sentence that says wave 2 was not taken.
- `corpus/lessons/round-42-verifier-spotcheck.md:174` — the defect table quotes the false LOG sentence. A same-file correction would have to be appended to the spotcheck.
- `corpus/lessons/round-30-verifier-spotcheck.md:15` — the filename `.ready.dispatched` matches `\bdispatched\b`.

## RD42-4 — placeholder section

`corpus/lessons/round-42.md:52-56`, and the next heading is `## Gate` at line 58 (a second Gate; the promise body is only 54-56):

> ## Wave-2 falsification
>
> Appended when the round-42 falsify wave reports: per-claim verdicts, attack tallies counted
> from the wave-2 dispatch (never estimated), each routed family named with the J-check that reds it, and
> each committed defeat artifact re-executed by its replay limb.

No `wave2-results.json`. Round-40 and round-41 lessons have `## Wave-2 falsification` sections that were filled; they do not match `when the … reports`. The tight phrase `when the .{0,60}reports` occurs in exactly two places under the K16 scan roots (corpus/lessons, LOG.md, SCORECARD.md, SHONEN.md): this section, and the spotcheck's own RD42-4 row at `round-42-verifier-spotcheck.md:176`, which sits in the body of `## 7. Routed defects`.

**A section-body substring scan cannot honestly own this.** It flags §7 of the spotcheck, a table that quotes the promise, and the only R9 close would be a `Correction (round 43)` naming the heading `## 7. Routed defects`. The honest pattern is a `## ` section whose own body (not a defect-table quotation) is the forward promise, which at HEAD is only `round-42.md`'s `## Wave-2 falsification`. The bare word `placeholder` as an alternate, which the K16 prompt lists, matches dozens of historical sections (round-31 through round-38 lessons, LOG, SCORECARD) that discuss placeholders already fixed. That alternate cannot go green without a mass of correction lines, so it must not be a bare substring.

The spotcheck says "replace with the non-dispatch record … or delete the promise". Both are rewrites. The legal close is one appended `Correction (round 43)` line in `round-42.md` that names the heading `## Wave-2 falsification` and says the promise was not fulfilled.

## RD42-5 — quoted `closed=10/13` has no committed transcript

Quoting bytes at HEAD:

- `.ufo/waves/round-42/claims-erratum-4.md:9-10`: "the instrument scored `closed=10/13 exit=1` and `selftest cases=13 failures=3` at the round-42 integration head before these repairs (`de09313e8edb98280b19767d0094bb2dd8031d73`)."
- `corpus/lessons/round-42-verifier-spotcheck.md:65`: "the pre-repair instrument at `de09313` prints `closed=10/13 exit=1` and `selftest cases=13 failures=3`".
- `corpus/lessons/round-42-verifier-spotcheck.md:177`: the RD42-5 row quotes `` `closed=10/13`, `failures=3` ``.
- Fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-42/kasegi.md:39-40` (Work performed) and `:169` quote the same numbers. That file is not in the lane. `git ls-files` in the lane has no round-42 report. An export-mode suite cannot see it.

The committed red transcript is `.ufo/waves/round-42/final-gates/all-gates.pre-repair.txt`: `export-ref=d238e36c28d73d1e76002a6943baaa9616917c31`, `closed=9/13 exit=1`, `selftest cases=13 failures=4`. `all-gates.txt`, `verify-Y0.txt`, and `c1-controls/do-nothing.txt` contain neither `closed=10/13` nor `failures=3` nor `de09313`. `de09313e8edb98280b19767d0094bb2dd8031d73` exists; its subject is "round-42: remove poisoned w2.ready …", committer `2026-10-28T11:08:59-03:00`. This seat did not re-run the suite at that ref.

`corpus/lessons/round-42.md` does not contain `closed=10/13`. M42-4 (`round-42.md:34`) says "pre-repair `failures=3`" while its evidence cell cites `all-gates.pre-repair.txt`, whose summary is `failures=4`. That bare `failures=3` is not the paired token `selftest cases=<n> failures=<k>`, so the K18 pattern as specified does not bind it. The K18 prompt's "base red naming `closed=10/13` in the round-42 lesson" is wrong if "lesson" means `round-42.md`. The glob `round-42*.md` does see it, via the spotcheck.

Machine close that works: the unedited tee of `r42-closure.sh --export-ref de09313e8edb98280b19767d0094bb2dd8031d73` landed at `.ufo/waves/round-43/final-gates/r42-at-de09313.txt`, which is inside K18's scan set. The tee has to actually print `closed=10/13` and `selftest cases=13 failures=3`; a summary-only file does not. A `Correction (round 43)` or `report-only` mark also closes the line mechanically, but the number is not known to be false — the transcript is missing — so the new artifact is the honest fix. The fleet report stays outside the check. That half of RD42-5 cannot be machine-checked from the lane export.

`claims-erratum-4.md` is the canonical quote and is not under `corpus/lessons/round-42*.md`. The frozen predicate's "round-42/43 lane records" is wider than the K18 prompt. If the limb scans only the glob, erratum-4 stays invisible. Include that file, or the defect's own statement is unchecked.

## RD42-6 — freeze label. K19 does not see it

`.ufo/waves/round-42/claims.json:6`: `"frozen_at_utc": "2026-10-28T12:05:00Z"`. Round-42 claims.json has no `controls` key.

Commit `0566bd66e93d429b2df8b6751cf10cbdc391e79b` (`git log -1 --format`): author `2026-10-27T10:06:29-03:00`, committer `2026-10-28T08:00:01-03:00` (11:00:01Z). Parent `5053a7f46de35784cff4b56756906e9014a38276` has the same author date, so the author date is inherited. 12:05:00Z is 65 minutes after the committer instant. That comparison needs `git log`. `git archive` does not carry commit dates, and the original mtime is not in the tree.

`.ufo/waves/round-42/claims-erratum-3.md:3` already records the label and the observed mtime `2026-10-28T10:51:52Z`. The lesson still cites the label with no pointer at the erratum: `corpus/lessons/round-42.md:20` "as frozen in `.ufo/waves/round-42/claims.json` (2026-10-28T12:05:00Z, KasegiR42)."

K19, as frozen and as prompted, reads `.ufo/waves/round-43/claims.json` `frozen_at_utc` and the two round-43 controls. At HEAD those are already ordered, and `freeze.txt` already matches:

- claims `frozen_at_utc` `2026-10-28T16:37:07Z`
- c1 `measured-at=2026-10-28T16:32:23Z`
- c2 `measured-at=2026-10-28T16:34:15Z` (the later one)
- `freeze.txt`: `frozen-at=2026-10-28T16:37:07Z`, `measured-at-max=2026-10-28T16:34:15Z`, `claims-sha256=a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630` (sha256sum of claims.json matches), `base=ab98fac9dce87130bc4f66de89e30650d63943dc`
- at base `ab98fac9`, `freeze.txt` is absent (`git cat-file -e` fails)

So K19 is open at base because the file is absent, and the ordering/sha limbs are already true at the freeze commit. Nothing in K19 reads `2026-10-28T12:05:00Z`, erratum-3, or `0566bd6`. **RD42-6 cannot be machine-checked by K19.** A check that every citation of `12:05:00Z` is superseded cannot go green under R9: the string is in claims.json:6 (not rewritable), in erratum-3 (the disclosure itself), and in wave-1 receipts. The wrongness relative to mtime is not re-derivable from export bytes. The legal record is a new erratum that names the label superseded by `2026-10-28T10:51:52Z`. That erratum is not what K19 grades.

## RD42-7 — undispatched wave

Facts above (RD42-2): 36 tasks validated, `.ready` present, `.ready.dispatched` absent, `wave2-results.json` absent. Attack share in the dispatch is 31, or 32 with sentinel. The lesson's "32 attack roles" matches the with-sentinel count; the fleet report's 31/36 matches without. Not a separate numeric defect.

The spotcheck's required action has two halves. "Count wave 2 only when `<wave>-results.json` exists" is the K15 side, and it misses the lesson sentences (RD42-3). "r43 opens with the wave-2 plan's unexecuted items (live J2/J6/J13 tree-level mutations, census adversarial rows)" is not a byte pattern. Those seats are in the undispatched spec (`MutJ2Token`, `MutJ6Bind`, `MutSuite` mentions J13, `RevC2Numbers` mentions census). The round-43 wave spec's 73 names include `ScoutCorpusCensus` and `MutK14`–`MutK19` / `MutGateRules`. They do not include a live J2, J6, or J13 tree-mutation seat. No K-check can see whether those attacks ran, because the results file that would record them was never produced, and producing it now would be a fake dispatch. **RD42-7's attack half cannot be machine-checked honestly.** Do not invent a `wave2-results.json`.

## RD42-8 — `closed=10/12` vs the control's `closed=8/12`

`.ufo/waves/round-42/claims.json` C1 `before` (no `controls` object; the path is inline):

> see .ufo/waves/round-42/c1-controls/do-nothing.txt — … the r41 suite at base prints closed=10/12 exit=1 …

The cited receipt `.ufo/waves/round-42/c1-controls/do-nothing.txt:15-16` prints:

> selftest cases=12 failures=8
> closed=8/12 exit=1

`closed=10/12` occurs in neither that file, nor `all-gates.txt`, nor `all-gates.pre-repair.txt`. `closed=13/13` in the same before sentence ("cannot print closed=13/13") does occur in the control, so a whole-token presence check correctly fails only `closed=10/12` for that cell. The lesson's C1 row (`round-42.md:24`) already says `closed=8/12 exit=1`. The spotcheck says the close is a `Correction (round 43)` and never a rewrite of claims.json. K17's prompt instead wants a `claims-erratum*.md` line in the **same round dir** that quotes the token and carries `superseded`. Those are different tokens in different directories. The erratum that satisfies K17 for this claims file is a new file under `.ufo/waves/round-42/`, next to errata 1–4. The scribe prompt lands `claims-erratum-1.md` at `.ufo/waves/round-43/`. If the limb is implemented as written, a round-43-only erratum does not close the round-42 claims file.

**K17 as specified cannot honestly go green.** A scan of every `.ufo/waves/round-<NN>/claims.json` before and after cell, requiring each `closed=`, `failures=`, and `cases=` whole token to appear in the cited control, is red on rounds 34–43 for reasons that are not RD42-8:

- Rounds 34–41 have no `controls` object. Their after cells state the round's target (`closed=9/9`, `closed=7/7`, `cases=<n>`, `failures=0`). Those tokens are not in a cited control. Closing them wants an erratum that calls a true after-state `superseded`.
- Round-42's after cell states `closed=13/13` and `selftest cases=13 failures=0`, which are in `all-gates.txt` and not in `do-nothing.txt`. The after cell names no path. Presence-in-the-before-control fails the true after-state.
- Round-43's own C1 before quotes `` `closed=10/13` `` as the thing erratum-4 says with no committed transcript. That token is not in either round-43 control (the controls do contain `closed=12/13`, `closed=10/12`, and `closed=8/12`). The after cell's `closed=19/19`, `cases=19`, `failures=0`, `closed=13/19`, and C2's `cases=10` / `failures=0` are targets, not observations, and are absent from the before controls.

The honest K17 is one comparison: round-42 C1 before's `closed=10/12` against the file the sentence names, whole token (so `closed=10/120` does not match), closed by an erratum in `.ufo/waves/round-42/` that quotes `closed=10/12` and `superseded` and quotes the control's `closed=8/12`. Do not require after-cell targets to occur in the before control. Do not treat a sentence that says a token has no transcript as a demand that the control contain it.

## RD42-9 — SHONEN form. Not closable

`SHONEN.md` is 285 lines. `## Round 41 evidence` at line 225 is the canonical shape: four `- [~]` boxes, each one line, no multiline continuation (block lines 225-231). `## Round 42 evidence` at line 232 runs through EOF (lines 232-285, 54 lines). The spotcheck says 55 added lines; the committed block from that heading through EOF is 54. All four boxes are multiline. No `[x]`. The heading is the defect. R9 forbids deleting it.

A check that fails while any `^## Round \d+ evidence` heading exists stays red forever, because the heading cannot be removed. The spotcheck's required action is prospective: the next block is four indented lines and no new heading. That does not make the r42 bytes conform. None of K14-K19 reads SHONEN structure. **RD42-9 cannot be machine-checked as a closable defect.** Grade the new append (no `## Round 43 evidence` heading, one line per box) and do not write a check whose after-state requires editing lines 232-285.

## Routed risks for the L1

1. K14's `payload=` exclusion hides the only stale literal it exists to catch. Narrow the exclusion or K14 is green at base.
2. K14/K15 prompts and the frozen predicate say `SHENON.md`. The file is `SHONEN.md`. `SHENON.md` is absent.
3. K15's slug rule does not see RD42-3 (`round-42.md:11` and `:16`). A line-level slug+`dispatched` rule false-hits the spotcheck rows that correctly say wave 2 was not taken. The results filename is `wave2-results.json`, not `<slug>-results.json`.
4. K16's bare `placeholder` alternate, and a section-body match on `when the … reports`, flags the spotcheck's `## 7. Routed defects` as well as the real section. The spotcheck's "delete or replace" fix violates R9.
5. K17 scanning every round's before and after tokens cannot go green without calling true after-states superseded. Restrict it to round-42's `closed=10/12`. Land the erratum in `.ufo/waves/round-42/`, not only under round-43.
6. K18's `closed=10/13` quote is in the spotcheck and in `claims-erratum-4.md`, not in `round-42.md`. The fleet report is outside the lane export; that copy is unchecked. The tee belongs at `.ufo/waves/round-43/final-gates/r42-at-de09313.txt` and must contain the tokens. M42-4's bare `failures=3` disagrees with the cited pre-repair transcript's `failures=4` and the specified pattern does not bind it.
7. K19 is already satisfied by the committed round-43 freeze record. It does not observe RD42-6. The r42 label's wrongness is not in the archive.
8. RD42-7's unexecuted J2/J6/J13 and census attacks are not seats in the round-43 wave and have no results file. Do not fake one.
9. RD42-9 cannot be closed by an append. Do not add a K-check that requires the r42 heading to disappear.

## Evidence

Commands and the output this seat actually got.

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
4cb6d4ae768481e1a14afbedc2d865a060ebacfd
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin log -1 --format='%H %ci %s'
4cb6d4ae768481e1a14afbedc2d865a060ebacfd 2026-10-28 13:37:11 -0300 round-43: frozen claims C1 (r43-closure.sh K1-K19 narrative-evidence) + C2 (claim-package gate capability), controls, freeze record, v2 wave spec and dispatch (73 seats)

$ git log -1 --format='commit=%H author=%aI committer=%cI %s' 0566bd66e93d429b2df8b6751cf10cbdc391e79b
commit=0566bd66e93d429b2df8b6751cf10cbdc391e79b
author_date=2026-10-27T10:06:29-03:00
committer_date=2026-10-28T08:00:01-03:00
subject=round-42: frozen claims + controls + wave-1 spec/dispatch
parent 5053a7f46de35784cff4b56756906e9014a38276 author_date=2026-10-27T10:06:29-03:00 committer_date=2026-10-27T10:06:29-03:00
subject=round-41 verifier spot-check (integrator, hyaku): non-author admit/reject

$ git rev-parse --verify de09313e8edb98280b19767d0094bb2dd8031d73
de09313e8edb98280b19767d0094bb2dd8031d73
$ git log -1 --format='%H %cI %s' de09313e8edb98280b19767d0094bb2dd8031d73
de09313e8edb98280b19767d0094bb2dd8031d73 2026-10-28T11:08:59-03:00 round-42: remove poisoned w2.ready (pointed at spec without taskCall; orchestrator hygiene)
$ git log -1 --format='%H %cI %s' d238e36c28d73d1e76002a6943baaa9616917c31
d238e36c28d73d1e76002a6943baaa9616917c31 2026-10-28T09:55:59-03:00 round-42: regenerate declared-path pins at complete integration head
```

Wave-2 files (`git ls-files` then `test -e`):

```
.ufo/waves/round-42/kasegi-r42-build-results.json
.ufo/waves/round-42/kasegi-r42-build.ready.dispatched
.ufo/waves/round-42/kasegi-r42-falsify.ready
ABSENT wave2-results.json
EXISTS kasegi-r42-falsify.ready
ABSENT kasegi-r42-falsify.ready.dispatched
```

`git ls-files` of a round-42 kasegi report inside the lane returned only historical round-21 copies under `.ufo/reports/round-21/` and two round-25 fixture trees. `git grep -l de09313e8edb98280b19767d0094bb2dd8031d73` under `final-gates` and `c1-controls` printed nothing.

Correction count (Python; `fence_scan` copied from `corpus/instruments/r42-closure.sh:306-334`; `CORRECTION_RX = ^Correction \(round (\d+)\)`):

```
J11-style correction lines (outside fences): 34 {'SCORECARD.md': 19, 'LOG.md': 7, 'SHONEN.md': 8}
corrections= literals outside fences:
SCORECARD.md:1634 corrections=33 HAS_payload= IS_correction_line
```

Wave-2 dispatch JSON: `counts.spawn=36`, 36 tasks, roles reviewer 7, critic 13, mutation-tester 11, scout 2, connector 2, sentinel 1.

Transcript dir token scan: `closed=10/13` False and `failures=3` False and `de09313` False in `all-gates.txt`, `all-gates.pre-repair.txt`, `verify-Y0.txt`, and round-42 `do-nothing.txt`.

Freeze record:

```
$ sha256sum .ufo/waves/round-43/claims.json
a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630
$ git cat-file -e ab98fac9dce87130bc4f66de89e30650d63943dc:.ufo/waves/round-43/freeze.txt
fatal: path '.ufo/waves/round-43/freeze.txt' exists on disk, but not in 'ab98fac9dce87130bc4f66de89e30650d63943dc'
```

`freeze.txt` at HEAD:

```
frozen-at=2026-10-28T16:37:07Z
measured-at-max=2026-10-28T16:34:15Z
claims-sha256=a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630
base=ab98fac9dce87130bc4f66de89e30650d63943dc
```

`frozen_at` is not earlier than either control `measured-at` (`2026-10-28T16:32:23Z`, `2026-10-28T16:34:15Z`).

Not run: `r42-closure.sh --export-ref de09313e8edb98280b19767d0094bb2dd8031d73`. The K18 executor owns that tee. This seat does not assert what that ref prints beyond the committed quotes above.

`wc -l SHONEN.md` = 285. Heading `## Round 42 evidence` is line 232; the block through EOF is 54 lines; four boxes, all multiline. `## Round 41 evidence` is line 225; four boxes, zero multiline.
