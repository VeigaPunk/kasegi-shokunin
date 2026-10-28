# R44Critic4 — falsification: C1 report completeness and planner/L2 accounting

**Seat item:** attack whether C1's after-state ("0 of those same 8 frozen routed defects remain
unresolved, proven by one committed read-only counter over committed lane evidence") can be
reached and *proven*, and whether the planner=L1 / L2-floor accounting that defect 4 requires is
graded at all.

**Verdict (not a lane verdict):** **C1's report-completeness limb is ungraded.** The drafted
counter never reads the round-44 report — it has no report argument at all — and grades defect 4
(and defects 3 and 7) from `corpus/lessons/round-44.md` instead. A round-44 report that omits both
the planner=L1 mapping and the L2-floor/residual line still yields `unresolved=0`. The eight-item
*set* is complete and correctly frozen; the *evidence surface* for three limbs is the wrong
artifact.

All measurements below are against the uncommitted drafted counter. Latest observed digest:
`9566b225484ee1543d9ab648b4a747e3fac4f6938e9e6553038556dcdfd20275` (151 lines; file was
actively changing during this seat, so re-pin before use), lane `6631401` + working-tree drafts,
frozen base `5ab3a60`, fleet root `/home/vgpnk/Projects/shokunin`.

---

## 1. F1 — the round-44 report is never read (blocking; the defect is a *report* defect)

**Counterexample.** `check()` (`r44-routed-defects.py:28-52`) takes only `root`; the CLI has only
`--root` and `--baseline` (`:114-119`). The round-44 report lives at
`{{FLEET_ROOT}}/.ufo/reports/round-44/kasegi.md` (`scripts/hyaku/lane-addendum.md:291`;
`MISSION.md:79` "on the main repo"), i.e. outside `--root`. RD43-4 (`:48`) therefore grades
`corpus/lessons/round-44.md`. A report with **no** planner/L2 content still scores `resolved=1`.

**Evidence.**
- `grep -n 'RD43-4' corpus/instruments/r44-routed-defects.py` → `48: … "Canonical planner seat: L1" in lesson and "L2 floor" in lesson and "66 seats" in lesson and "no residual call" in lesson`.
- `lesson = text(root, "corpus/lessons/round-44.md")` (`:31`); the report path appears nowhere in the file (`grep -c 'reports/'` → 0).
- The round-44 report does not exist yet: `ls /home/vgpnk/Projects/shokunin/.ufo/reports/round-44/kasegi.md` → `No such file or directory`; the lane repo tracks no round-43/44 report (`git ls-tree -r --name-only 5ab3a60 -- .ufo/reports` → `.ufo/reports/round-21/kasegi.md` only).
- Defect 4's own text: `corpus/lessons/round-43-verifier-spotcheck.md:104` — "**Report omissions** … The report records neither the planner=L1 mapping … nor the L2-floor/residual-call line"; remedy "Record them next round (and in the next round's report shape)".
- Live tally at the latest tested digest: `python3 corpus/instruments/r44-routed-defects.py --root . --baseline .` → `fixed=5 unresolved=3 exit=1`, with RD43-4 red only because `corpus/lessons/round-44.md` is absent (`ls` → no such file). One lesson file, not the report, flips it.

**Impacted axis:** `depth:verifiability` (C1). **Correction:** restore a required
`--report {{FLEET_ROOT}}/.ufo/reports/round-44/kasegi.md` and grade RD43-4 from the report; the
lesson may *also* carry the lines, but the report is the artifact the frozen defect names. Keep the
frozen `--root/--baseline` pair as-is so the claim's declared invocation still reproduces (see F7).

## 2. F2 — three limbs collapse onto one lane file (saturation)

RD43-3 (`:47`), RD43-4 (`:48`) and RD43-7 (`:51`) all read `lesson`. The last three unresolved
limbs are therefore satisfiable by a single appended lesson paragraph. None of the three is the
artifact its defect names:
- defect 3 (`:103`) names `corpus/lessons/round-43.md` L90/L101 — that file is **unmodified**
  (`git status --porcelain corpus/lessons/round-43.md` → 0 lines; both lines still read "a
  29-character prefix", `sed -n '90p;101p'`), so the wrong numeral stands uncorrected in the record
  that carries it while the counter can go green on round-44 prose;
- defect 7 (`:107`) names the report's SHONEN pointer and the registry rows — the rows are real
  (see F5), the report pointer is still unaddressed.

**Correction:** grade defect 3 from a correction appended to `corpus/lessons/round-43.md` (or a
`Correction (round 43)` line in an append-only record naming both numerals), and defect 7 from the
registry file plus the report pointer. Do not let one file close three limbs.

## 3. F3 — RD43-4's predicate is a substring oracle with a hardcoded count

`"Canonical planner seat: L1" in lesson and "L2 floor" in lesson and "66 seats" in lesson and
"no residual call" in lesson` (`:48`).
- **False pass demonstrated on the previous revision** (digest `3e04ec7d…`, same substring logic
  against the report): `python3 … --report corpus/instruments/r44-routed-defects.py` → `RD43-4 …
  resolved=1`, `fixed=7` — the instrument's own source satisfied the report limb because it
  contains its own literals. No report was read.
- `"66 seats"` is a literal in the code, not derived from `.ufo/waves/round-44/wave1-dispatch.json`
  (`.counts.spawn` = 66, `.registry.members` = 66). A sentence like "66 seats were planned but 60
  landed" passes; a correct report that says "63 delivered" fails.
- No planner identity is checked (the L1 id is `KasegiR44`, `claims.json .author`; it is not in the
  dispatch — `grep -c 'KasegiR44' wave1-dispatch.json` → 0), and nothing rejects a lesson that both
  claims planner=L1 and asserts a spawned planner seat, although
  `templates/round-prompt.md:86` still mandates `- 1× planner` while
  `lane-addendum.md:236-239` forbids spawning one.

**Correction:** require `planner=L1 KasegiR44`, derive the seat count from the dispatch JSON at
`--root`, require `residual=none` (or a named call) and the round total, and reject any planner
entry in the seat accounting.

## 4. F4 — RD43-2 is weaker than the gate its remedy names

:46 → `"closed=13/19" in errata and "superseded" in errata` — whole-file substrings. K17's
actual escape is **paragraph-scoped**: `k17-claims-before.sh:112`
`ERRATA_RX = re.compile(r"^claims-erratum.*\.md$")` and `superseded_by(round_dir, token)`, which
accepts a blank-line-separated paragraph containing the token **and** matching `supersed`.
Defect 2's frozen remedy is "K17's existing escape then covers it" (`:102`) — so resolution must be
K17-green, not substring-present. A file with the token in one paragraph and "superseded" in
another passes the counter and fails K17.

**Correction:** replicate K17's paragraph predicate (or source the limb and call it), and cite the
round-43 K17 run as the red-before. The erratum is correctly placed
(`.ufo/waves/round-43/claims-erratum-6.md`; it must be same-round for `ERRATA_RX`/`superseded_by`),
and both of its paragraphs do carry token + "superseded", so this limb is genuinely closable.

:51 → `"claim-package-check.py" in skill and "r43-closure.sh" in skill and "SKILL.md Gates &
probes registry" in lesson`.
- The append route is legitimate and already satisfied: `SKILL.md` has a real
  `## Gates & probes registry` section at base (`git show 5ab3a60:SKILL.md` line 977; 10 hits), and
  base `SKILL.md` contained **0** of the two basenames (`git show 5ab3a60:SKILL.md | grep -c …` →
  0) while the working tree now has 2 (`grep -c` → 2; `git diff --stat SKILL.md` → `9 +++++++++`).
  `corpus/instruments/README.md` still has 0 hits (`git grep -c` → rc 1) — the round-43 report's
  false claim is retargeted, not hidden.
- But the frozen remedy is disjunctive ("Retarget the pointer **or** append the two rows", `:107`)
  and the counter demands both. The lesson string is also satisfied by `SKILL.md` itself: on the
  previous revision, `--report SKILL.md` flipped RD43-7 to `resolved=1` — the limb is not anchored
  to any report.

**Correction:** accept either route; if the retarget route is taken, grade the *report* line that
does it (which requires F1's `--report`).

## 6. F6 — RD43-5 re-attests the symptom; 5c is vacuous at baseline

:49 requires `seats=73` and 73 names from a **round-44** companion
(`.ufo/waves/round-44/controls/round43-registry-correction.txt`; measured: one `names=` line, 73
comma-separated names, `seats=73`), plus an `export-ref=de09313e…` token from
`r42-at-de09313-selftest-replay.txt` (present since 16:10; the earlier `-runner.log` carried the
same token, `grep -o 'export-ref=[a-f0-9]*'` → `export-ref=de09313e8edb98280b19767d0094bb2dd8031d73`).
- The defective line is untouched: `.ufo/waves/round-43/w1-REGISTRY.txt:7` is still
  `names=` (`sed -n '7p' | od -c` → `n a m e s = \n`). The companion is a defensible append-only
  restatement, but the frozen remedy also says "**Fix the emitter**" (`:105`) and nothing grades
  that: no round-44 artifact of the same emitter exists (`grep -rl '^names=' .ufo/waves/round-44/`
  → only the companion).
- 5c is `not (root / ".ufo/waves/round-43/final-gates/all-gates.at-Y.txt.tmp").exists()`. That file
  was **never committed** (`git cat-file -e 5ab3a60:…tmp` → `fatal: path … does not exist`, rc 128;
  `git log --all -- '*all-gates.at-Y.txt.tmp'` → empty), so it is absent from every export and the
  clause is green at the frozen base by construction — it has no red-before and cannot be graded by
  a read-only counter over committed evidence. The companion note's claim that it "has been removed
  in round 44" (`round43-registry-correction-note.txt`) is unsupported by any committed record: an
  untracked file leaves no deletion evidence.

**Correction:** grade 5a/5b only; record 5c as closed-by-inspection with the never-committed
command, outside the red-before set, and drop the unverifiable "removed in round 44" wording.

## 7. F7 — the counter is uncommitted and rewrote itself during this seat

At least four distinct digests were observed while the draft was changing:

| observed digest | observed shape | consequence |
|---|---|---|
| `3e04ec7d…` | 90-line version with `--report` and optional `--prior-report` | the frozen invocation `--root . --baseline .` failed argparse (`--report` required; exit 2); its report limb was vulnerable to the own-source mutation in F3 |
| `8a5a9c2b…` | `--report` removed; RD43-4 read `corpus/lessons/round-44.md` | fixed=5, unresolved=3 |
| `564945b0…` | 150-line version, selftest added | predicate still lesson-based |
| `9566b225…` | latest observed, 151-line version | frozen invocation runs; fixed=5, unresolved=3 |

Because edits occurred concurrently with reads, digest/line observations are not atomic for every
intermediate snapshot; the table records observed hashes and shapes, not a claim that each hash
uniquely binds every adjacent excerpt. The latest version remains uncommitted and moves the
predicate while the wave is under way.

C1 requires "**one committed**" read-only counter. A predicate that changes between control and
after-state cannot prove either. In the first revision, the `--prior-report` red-before clause was
also optional (`(not prior or …)`), so a run without it graded defect 4 with no red-before at all.

**Correction:** freeze the counter's bytes (commit it, cite its sha256 in the report and in the
counter's own output line, as round-43's suite does with `suite-sha256=`), and make the do-nothing
control name the same digest.

## 8. What holds (positive controls — do not inflate the failures)

- **The eight-item set is complete and correctly bounded.** `grep -Ec '^6\\. Routed defects|^[0-9]+\\. \\*\\*' corpus/lessons/round-43-verifier-spotcheck.md` → `8`; the matches are exactly lines **101–108**; all five §1 conformance bullets map into them (`:26`→4, `:27`→5a, `:28`→6, `:29`→5b, `:30`→7) and none is orphaned. The counter's frozen-set guard (`:134-137`, `^\\s*[1-8]\\. \\*\\*`, `expected=8`) pins the count to the `--baseline` export.
- **Per-limb base reds are individually established from committed bytes**: SHONEN tail at `5ab3a60` = `.\\n` vs `.\\n\\n` at `ab98fac9` (defect 6 red; working tree now `\\n\\n`); base `SKILL.md` 0 basenames (defect 7 red); `w1-REGISTRY.txt:7` = `names=` (5a red); no `claims-erratum-*.md` under `.ufo/waves/round-43/` at base (defect 2 red); round-43 report `grep -cni planner` → 0 and `grep -cniE 'residual|L2 floor'` → 0 (defect 4 red); `corpus/instruments/r44-routed-defects.py` absent at HEAD (no r44 correction at base).
- **Defect 1's lane artifacts are real**: `git diff SCORECARD.md` → `+Correction (round 43; appended round 44): … \\`closed=13/19 exit=1\\` is superseded…`; erratum carries `closed=13/19`; both append-only.
- **No-harm on the round-43 suite**: `sha256sum corpus/instruments/r43-closure.sh` → `a832908e15f49de89066d8168a833d3ffa0f5fad432ba1c2b5a813ba45bef168`, identical to `suite-sha256=` in `.ufo/waves/round-43/final-gates/all-gates.at-Y.txt`. Do not add limbs to it; the r44 counter must stay standalone.
- **Minor**: RD43-6 (`:50`) guards the missing-file case, but proves only the tail, not that the base bytes were preserved.

## 9. Limitations

- The counter is an **uncommitted draft** edited by peers during this seat; latest observed digest is `9566b225…` (earlier observed digests are listed in F7) and may be stale by the time the L1 commits. Re-pin before grading.
- No base-export replay: `HYAKU_SCRATCH` is unset and `mkdir -p /nonexistent/kasegi-r44/R44Critic4` → `Permission denied` (rc 1). No scratch was created; a full do-nothing run against `5ab3a60` was therefore not possible and the base reds were established limb-by-limb from `git show` instead.
- I ran the draft counter read-only (it only reads and prints; verified by inspecting `check()` and `main()`), but ran **no committed gate** — no `r43-closure.sh`, no K17/K18/K19, no census.
- The lane root now carries three untracked strays — `25` (`corpus/README.md:631`), `62` (empty), `68` (`corpus/SOURCES.md:152`) — created during the wave, almost certainly a mis-parsed C2 counting command. Not my item; they must not be committed.
- I did not judge, admit, edit, integrate or ship anything; no message to another runtime.

## 10. Report

- Files read: `.ufo/waves/round-44/claims.json`, `controls/do-nothing.txt`, `controls/{missing-suite-base,round43-registry-correction,round43-registry-correction-note,r42-at-de09313-selftest-runner.log,fix-hash-count}.txt`, `corpus/instruments/r44-routed-defects.py`, `corpus/instruments/r43-limbs/{k17,k18,k19}*`, `corpus/instruments/README.md`, `corpus/lessons/round-43-verifier-spotcheck.md`, `corpus/lessons/round-43.md:90,101`, `.ufo/waves/round-43/{claims-erratum-6.md,w1-REGISTRY.txt}`, `.ufo/waves/round-44/{wave1-dispatch.json,wave1-spec-valid.json}`, `scripts/hyaku/lane-addendum.md:225-242,291`, `MISSION.md:53-79`, `templates/round-prompt.md:78-96`, `.ufo/prompts/kasegi-round-43.md:80-86`, `.ufo/reports/round-43/kasegi.md`, `wave1/R44Review11.md`.
- Commands run: `git rev-parse/log/ls-tree/ls-files/cat-file/diff/show/status/grep`, `sha256sum`, `stat`, `grep -Ec/-En/-cni/-o`, `sed -n`, `od -c`, `wc`, `ls`, `python3 corpus/instruments/r44-routed-defects.py` (read-only, 4 runs), one failed `mkdir`.
- Edits: this report only. No commits, pushes, git/jj/index mutation, fleet-root writes, pacman, or tool installs.
- Report path: `.ufo/waves/round-44/wave1/R44Critic4.md` (lane-relative).
