# R48Review24 — Frozen-checker semantic depth review, C1 verify pass

- **Seat:** R48Review24 (reviewer, leaf — no subagent dispatch, no production edits)
- **Round:** 48, wave 1 · **Lane:** kasegi-shokunin · **Axis:** depth:verifiability
- **Claim under review:** C1 (routed-defect-closure of round-47 route R1 — SHONEN.md canonical-form drift)
- **Rules read first:** `/home/vgpnk/.omp/agent/RULES.md` (tooling directive noted; no installs performed — git/coreutils/python3 only; pacman transactions honored as paused)
- **Scratch:** `/fast/scratch/hyaku/kasegi-r48/R48Review24/` created explicitly; fixtures, receipts and both runner work dirs lived only there; removed at exit after receipts were folded into this report.
- **Round-47 routes R1/R2:** located in `corpus/lessons/round-47-verifier-spotcheck.md` §6 (not the round-47 wave/controls tree). R1 = SHONEN.md canonical-form drift (52 `[~]` lines, 13 accumulated blocks; route: restore toward canonical seed) — the defect C1 closes. R2 = frozen plain-target phrasing (`supersedes S074` target 1 matches 2 lines) — context only, untouched by this claim.

## Frozen-state identification (measured this seat)

| Artifact | Expected | Observed |
|---|---|---|
| Assignment hash `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` | frozen claim anchor | git **commit** `3546f70` "round-48: freeze canonical checklist restoration and controls"; `git cat-file -t` → commit; parent of HEAD `3d7e042` (`git log --format='%H %P' -1 HEAD`) |
| `claims.json` bytes | frozen, matching `freeze.txt` | sha256 `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345` = `freeze.txt` `claims-sha256`; `git show 3546f708:.ufo/waves/round-48/claims.json \| sha256sum` identical; `git diff 3546f708 HEAD -- claims.json` empty |
| Frozen counter `corpus/instruments/shonen-form.py` | unchanged after freeze | sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`; absent from the freeze→HEAD diff (`git diff 3546f708 HEAD --stat`); no post-score checker amendment |
| Archive `controls/shonen-before.txt` | retains SHA256 `596122c0…9c05` (kill rule) | sha256 `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05`; byte-equal to `git show 3546f708:SHONEN.md` (same hash) |
| Live `SHONEN.md` at HEAD | landed canonical form | sha256 `b1352168…46d0`; `git status --porcelain -- SHONEN.md` empty — landed, not in-flight |

Note on the header wording: the assignment cites "frozen claim … at `3546f708…`"; that value is the freeze **commit id**, not a content hash (content sha1 is `50f55f1f…`, sha256 is `b8022cdf…`). `freeze.txt` pins the file hash; the commit id pins the tree state. Both verified independently.

## Bounded probes (exact commands; expected vs observed)

1. **Counter on live tree** — `python3 corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin`
   Expected `canonical=1 finding=SF-CLEAN exit=0` (claim `expect_after`). Observed `shonen-form canonical=1 finding=SF-CLEAN exit=0`, exit 0. ✓
2. **Before/after replay** — `python3 .ufo/waves/round-48/measure.py --root . --base 3546f7089c224ac6c8adc68208b1e648bbf3e6a5 --after 3d7e042ecbb1f17662f5042e8d3da3290722c031 --work /fast/scratch/hyaku/kasegi-r48/R48Review24/measure-work` (runs the checker bytes committed at `--after` over git-exported trees; writes only under scratch)
   - before: expected `canonical=0 finding=SF-PREAMBLE exit=1` (`expect_before`); observed `shonen-form canonical=0 finding=SF-PREAMBLE exit=1` + plain `{checklist_lines: 356, boxes: 52, checklist_sha256: 596122c0…}` ✓
   - after: expected `canonical=1 finding=SF-CLEAN exit=0`; observed same + `{checklist_lines: 12, boxes: 4, checklist_sha256: b1352168…}` ✓
   - frozen-counter-sha256 printed by the runner: `0ab32a2c…` (matches live tree). ✓
3. **Persisted fixture battery** — `python3 corpus/instruments/shonen-form-selftest.py --root . --work /fast/scratch/hyaku/kasegi-r48/R48Review24/selftest-work`
   `controls/fixtures.json` sha256 `10d2aa79e231d1ac7bb02e9c53df4c7f50d78d07931c42bfa0384a82c0cbb288` matches the pin baked into the selftest (snapshot-tamper guard). 17/17 cases green: fenced→SF-PREAMBLE, commented→SF-PREAMBLE, duplicate→SF-TRAILING, extra-prose→SF-TRAILING, crlf/no-newline/missing-file→SF-NEWLINE, wrong-label-N→SF-BOX, missing-evidence-N→SF-EVIDENCE, canonical→SF-CLEAN. Kill-rule limb "no tested hidden/commented/duplicate checklist passes" holds. ✓
4. **Independent edge battery** (this seat's added depth, 16 cases against the frozen checker via `--root <scratch> --file <scratch case>`; driver saved at scratch `edge_probes.py`, receipts in scratch `receipts.txt`): all 14 content cases match predicted exit+finding exactly —
   `x-mark-valid-ev→SF-VERIFIER/1`, `x-mark-no-ev→SF-EVIDENCE/1`, `unchecked-no-ev→SF-CLEAN/0` (the bare template seed form passes), `abs-pointer→SF-POINTER/1`, `dotdot-pointer→SF-POINTER/1`, `missing-pointer→SF-POINTER/1`, `dir-pointer→SF-POINTER/1`, `dot-slash-pointer→SF-POINTER/1`, `empty-pointer→SF-POINTER/1`, `swap-box-order→SF-BOX/1`, `fifth-box→SF-TRAILING/1`, `bad-ev-indent(4sp)→SF-EVIDENCE/1`, `blank-after-title-only→SF-PREAMBLE/1`, `uppercase-[X]-mark→SF-BOX/1`; plus `symlink-escape-pointer (adir/esc.md → /etc/passwd)→SF-POINTER/1` (resolved-path containment check works). Mismatches: 0.
5. **Could-not-evaluate class** (declared, not red findings): invalid-UTF8 file → `shonen-form canonical=0 finding=SF-UNREADABLE error=UnicodeDecodeError exit=2`; directory passed as `--file` → `…error=IsADirectoryError exit=2`. Both match the declared exit-2 class.

## Kill-rule limbs, final measured revision (HEAD 3d7e042)

1. `canonical=0` at final revision — **not triggered** (probe 1/2).
2. Tested hidden/commented/duplicate checklist passes the frozen checker — **not triggered** (probes 3/4; the exact-preamble + exactly-four-boxes + no-trailing grammar leaves no room for a second checklist; pre-freeze-mutants receipt shows 6/6 checker mutants caught).
3. Restoration loses historical bytes — **not triggered** (archive byte-equal to the frozen-before SHONEN.md at the kill rule's SHA256).

## Observations (non-blocking)

- **Candidate vs landed bytes.** Live `SHONEN.md` differs from `controls/canonical-candidate.txt` (candidate: all four boxes `[~]` with `LOG.md — Author assessment only` pointers; landed: box 1 `[~]`/SKILL.md, box 2 `[ ]`/LOG.md, box 3 `[~]`/round-47-verifier-spotcheck.md, box 4 `[~]`/PROVINCE.md). Both forms pass the frozen checker; the candidate is a pre-freeze illustration, not a byte target in the predicate or kill rule. All four landed evidence pointers resolve at HEAD (`ls` + the checker's own pointer pass).
- **Route-location correction.** R1/R2 routes are defined in `corpus/lessons/round-47-verifier-spotcheck.md` §6 "Routed defects and operator notes" — R48Probe45's note that "no route definitions by that name exist" is true only of the round-47 wave/controls tree, not the lane tree.
- **Registry delivery state.** The gate's registry row (SKILL.md "Round-48 author-checklist form checker" table) exists in the working tree but is **uncommitted** at HEAD (+12 lines, `git diff --stat -- SKILL.md`). Gate-standard conformance needs it landed; that is integration-owner work (KasegiR48), outside this claim's kill rule.
- **Checker precedence detail.** For `[x]` + malformed pointer, SF-POINTER fires before SF-VERIFIER; both exit 1, so kill-rule semantics (x marks rejected) are unaffected either way.
- **History.** HEAD commit carries the lane identity (`kasegi-shokunin <kasegi@shokunin.local>`); 64 seats present in wave1 spec (`items: 64`) and swarm registry (roles: 20 executor, 20 mutation-tester, 11 reviewer, 4 critic, 4 scribe, 2 connector, 2 scout, 1 sentinel).

## Verdict

C1 **verifies as scoped** at the final measured revision: before-line `SF-PREAMBLE exit=1` on the frozen state, after-line `SF-CLEAN exit=0` on HEAD, kill rule's three limbs all satisfied, frozen checker and claims bytes untouched since freeze, archive hash exact. Author-side form only — semantic evidence and promotion remain independently judged, per the claim's own mechanical limits. No red findings.

## Residual risk / verification gaps

- The 6 checker mutants in `controls/pre-freeze-mutants.txt` are a disclosed receipt; mutant bodies are not committed this round, so survivors cannot be re-executed from durable bytes (contrast round-47's committed `r47-mutbat.py`).
- The selftest is a separate runner, not a self-invocation flag on the gate (disclosed as a conformance limitation in the uncommitted SKILL.md registry row).
- This seat graded HEAD `3d7e042` as the final measured revision; any later integration commit re-opens probe 1 cheaply (`counter_cmd` is one command).
- My 14-case edge battery is seat-local (receipts in this report); persisting it as fixtures would harden future rounds against checker edits.
