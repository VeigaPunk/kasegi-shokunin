# ScribeLesson — round 81, attempt 1

## Behavior

Drafted `.ufo/waves/round-81/w1/lesson-round-81.md` (331 lines) as the round-81 lesson, for the L1 to integrate into `corpus/lessons/round-81.md`. It states one v1 wave of **13 seats** (`.ufo/waves/round-81/w1-spec.json` `items` = 13) and carries `## Gate` (C1 + C2) and `## Mistakes` (M81-1, M81-2), plus the two appended-correction bullets for `corpus/lessons/round-80.md` and one QUALITY row draft (R132). Every `path:line` cited is re-grepped and pasted in the lesson's own "Cite-check receipts" section.

Values are labelled by provenance: *measured this draft* (sha256sum / `git show` / `grep -n` / `awk` / `wc`), *control* (pre-freeze run committed in the freeze commit, quoted, not re-run), **PENDING-L1** (landing, live re-fetch, or verdict).

## Gates run in this seat (read-only; no lane instrument or lane gate executed)

| what | command | result |
|---|---|---|
| frozen bytes = freeze-commit blobs | `sha256sum` over `.ufo/waves/round-81/{c1,c2,controls}/…` and `git show 7ad3118c:<path> \| sha256sum` | candidate `a3b58aa5…dbec0`, counter `fa96223b…43b4`, table `abcc834e…d095`, builder `57ab70e9…6a7f`, entry-gate `51ee45fb…d0d2`, forgery driver `28fde387…9246`, claims `604b788a…0f40` — both copies agree on all seven |
| C2 snapshot | `sha256sum`, `wc -l -c` | `S115.txt` `e304eb88…6f7f`, 44 lines, 2224 bytes; manifest `7429df80…05cf` |
| table composition | `python3` over `c1/mutant-table.json` | 59 rows = 55 assertion + 1 exception (`K-M3`) + 3 neutral (`NT1 NT2 NT3`); 28 r80 ids + 28 new ids; `kill_cases` list per row |
| six quotes located | containment over `S115.txt` | each occurs once, on its declared line; words 14/12/23/18/1/12 |
| P6 pin state | `awk` on `SKILL.md:982`, `corpus/instruments/README.md:354` | both `cases22=no cases15=yes` → not met at draft time |
| P7 literals | `grep -c` over frozen candidate | 1 / 1 / 0 |
| registry / expected list | `git show 7ad3118c:corpus/SOURCES.md`, `wc -l` | base 114 → freeze 115 rows; expected 96 → 97 lines (worktree); knowledge 94 (freeze) → 95 (worktree) |
| M81-1 evidence | `grep -n` / `sed -n` over `osv-post-batch-query-contract.md`, `round-80.md`, `git show 0039d670:…` | R131 (`QUALITY.md:588`) and the `:19` cites (`round-80.md:88,160`) are in the **same landed commit** `0039d670`; `:19` is the heading, `:21` the sentence |
| M81-1 fix | `cite()` one-liner | FAIL on `:19` (heading / token absent), PASS on `:21` |
| M81-2 evidence | `grep -n`, `sed -n` range + `grep -c` | prose "four rejects" (`round-80.md:169`) vs 3 bullets (`:87`–`:89`), block lead-in already says "all three"; admits = 6 |
| M81-2 fix | count-rule one-liner | FAIL bound to 4; PASS bound to 3 |

## Touched surfaces

Written (only these):
- `.ufo/waves/round-81/w1/lesson-round-81.md`
- `.ufo/waves/round-81/w1/ScribeLesson.md` (this report)

No receipts subdirectory was needed: every pasted output is inside the lesson. Scratch `/fast/scratch/hyaku/kasegi-r81/ScribeLesson` created empty and removed before yield. No tool installed or upgraded. No git/jj mutation; the only git calls were `cat-file`, `show`, `rev-parse`, `status --porcelain`, `diff`, `ls-tree`.

## Findings (routed to the L1; none is a verdict change)

1. **The r80 spot-check's routed defect 1 undercounts its own defect.** It names three `:19` sites (`round-80-verifier-spotcheck.md:101`: "lines 88, 160, 162"); measured with `grep -n ':19' corpus/lessons/round-80.md` there are four substantive sites — `88`, `160`, `162` (`(:19, measured)`) and `169` (`F54:19`), plus the self-flag at `14`. Same class, one level up.
2. **`F5-allcases` is not rejected by the kill tally.** Under the r81 counter it prints `killed=56 survived=0 miskilled=0` and is rejected only by `neutral_ok=0/3`. Any summary of P4 that says "the tally rejects every forgery" is wrong for F5; the lesson says so explicitly.
3. **The r80 counter has no neutral limb at all** (`grep -c -i neutral .ufo/waves/round-80/c1/mutbat.py` = 0), which is why its `rows=56` over a 59-row table — recorded as a measured fact, not as a claim about intent.
4. **P6 is not yet satisfiable at draft time.** `SKILL.md:982` and `corpus/instruments/README.md:354` still read `cases=15` / no `cases=22`; the worktree instrument is still the r80 `420151fd…`. This is the L1's swap, listed PENDING-L1.
5. **The C2 entry is already in the worktree, uncommitted, byte-identical to `w1-input/`** (`diff` rc 0, sha `2895011e…1940`); `git status` shows `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/knowledge-expected.txt` modified. All B-values are therefore reported as "measured, uncommitted" rather than as landing measurements.
6. **`S115.txt:32` is a single line doing double duty** — audience sentence admitted, status and feedback sentences rejected — the round's sharpest cut, recorded in § Learning.
7. **Peer receipts were folded into § Gate while this draft was being written.** `w1/ExecC1RealTree.md` (P5 analogue `entries=95 … conformant`; P6 patch `cases=15`→`cases=22`, `patch_rc=0`, `dryrun_rc=0`) and `w1/ExecC2Gate.md` (B0 six anchors; B3 `rows=57 … registry=115` + `FRONTIER-PASS F57 ids=S115`; B4 `records=95 bound=95 unbound=0`; B8 `claims=6 want=6 … unpinned=0` / `pass`) are quoted there as *receipt* values, mirror runs only — the lane's own bytes were still unswapped at the moment of writing (`instrument 420151fd…`, pins `cases=15`, both re-measured just before this report), so every landing value stays PENDING-L1. The lesson states this split explicitly rather than promoting a mirror run to a landing measurement.
8. **Observation, receipt-sourced and not re-measured here:** `ExecC2Gate.md`'s B4 row prints `AUDIT records=95 with_url=95 … orphans=1 orphan=S040-live.txt` alongside `unbound=0`. B4 passes as written; the orphan is outside the frozen set and belongs to round 82 if the L1 wants it routed.

## Out of scope / not done by this seat

No counter, candidate, gate or entry was run; no `FRONTIER-CENSUS`, `capture-binding-check`, `sources-census.sh`, `source-recheck.py` or `entry-gate.py` invocation; no live re-fetch of `https://google.github.io/osv.dev/get-v1-importfindings/`; no lane file outside `w1/` written; no `corpus/lessons/round-80.md` edit (the corrections are drafted, never applied); no QUALITY row written (draft only).

## Artifact paths

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/lesson-round-81.md`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ScribeLesson.md`

## PENDING-L1 (restated from the lesson)

P1/P3/P5/P6/P7/P8 landing re-runs; P2's landed sha and the instrument swap; the `cases=22` pin rows; B0–B8 at the landing commit (one-row SOURCES diff, `FRONTIER-CENSUS rows=57 … registry=115`, `FRONTIER-PASS F57 ids=S115`, `unbound=0`, B8 over the new entry); the live page status/raw size; the appended-corrections and R132 landings; the fleet report; the C1/C2 verdict lines and the landing commit.
