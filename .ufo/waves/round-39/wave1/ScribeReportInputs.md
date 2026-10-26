# ScribeReportInputs — receipt (round 39)

## Deliverable

- `.ufo/waves/round-39/wave1/ScribeReportInputs.inputs.md` — report input pack for the L1.
- 147 lines, 15737 bytes, sha256 `b1c471a89202508fd292fb28c3b8f88e1f7bfa71910b474abe466a9a25e4cbba`.
- Contents: §1 C1 rows, §2 C2 rows (frozen counting commands verbatim + before values tagged `[m]`
  measured / `[c]` control / `[t]` frozen target), §3 wave shape (49 seats by role, dispatch and
  registry identity counts, G1–G8 map, control digests), §4 ordered evidence pointers, §5 current
  lane state of every cited artefact, §6 conflicts F1–F3.
- No `Final lane commit:` token (grep `-c` → 0), no `⟨pending` marker, two fenced blocks only.

## Axes

- `coverage` — drafting-input completeness: every frozen counting command (C1.1–C1.5, C2.1–C2.9)
  present verbatim with a before value traced to a control or a base-commit measurement, and every
  after value labelled a target. Nothing upgraded to evidence.
- `depth:verifiability` — untouched by me except as input: all after values left as targets; J and
  `final-gates/` absent at pack time.

## Commands run and their actual output

All read-only. `L=/home/vgpnk/Projects/shokunin/kasegi-shokunin`, `S=/fast/scratch/hyaku/kasegi-r39/ScribeReportInputs`.

1. `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → `/tmp 3% 125.2G`,
   `/var/tmp 35% 585.6G`, `/fast/scratch/hyaku 25% 609.4G`; no red line. Heavy passes were not run.
2. `git -C $L log -1 --format='%H %ci %s'` →
   `d65d823e7c84813c192b20ee757a8761f878a61f 2026-10-26 16:28:27 -0300 round-39: wave1 spec/dispatch`.
3. `git -C $L status --porcelain --untracked-files=no | wc -l` → `0` (tracked tree clean; untracked
   `.ufo/waves/round-39/wave1/` receipts in flight, 49 entries at pack time).
4. `git -C $L cat-file -e 480b1a5…:corpus/instruments/r39-closure.sh` →
   `fatal: path 'corpus/instruments/r39-closure.sh' does not exist in '480b1a505a2dfc14a4f718d16d63808247214d0a'` (exit 128);
   the same `cat-file -e` for `r38-closure.sh` and `r37-closure.sh` at base → exit 0 (both present).
5. Base before counts, `git show 480b1a5…:<path>` piped into the frozen greps:
   `corpus/README.md` frontier rows → `21`; `corpus/SOURCES.md` S-rows → `55`; `S057` in
   `corpus/SOURCES.md` → `0`; `corpus/knowledge/*.md` (via `ls-tree -r`) → `50`.
6. Same three counts at HEAD → `50` knowledge, `21` frontier, `55` registry (no round-39 landing yet).
   `ls corpus/source-snapshots` latest tracked round dir → `round-38`; `round-39` absent at base and tip.
   `git ls-tree -r HEAD corpus/knowledge | grep -c '\.md$'` → `50`; knowledge files matching
   `^source: S057` → `0` at base and `0` at tip.
7. Commit resolution, `git -C $L log -1 --format='%h %s' <sha>`:
   - `480b1a50…` → `480b1a5 round-38 verifier spot-check (integrator, hyaku): non-author admit/reject`
   - `dcd3170…` → `dcd3170 round-39: claims freeze C1/C2 + controls`
   - `2387dcf6…` → `2387dcf6 round-37: F3 final head — bind final lane hash in SHONEN/SCORECARD`
   - `66703aca50529a35be49aa8759d04140720ad` → `fatal: ambiguous argument '66703ac…': unknown revision or path not in the working tree.` (exit 128)
   - `66703acaaff50529a35be49aa8759d04140720ad` → resolves, `round-38: integrate C1 r38-closure suite + D-A..D-F corrections, C2 F21 CSAF v2.0 VEX (S055), lesson/LOG/SCORECARD/SHONEN, wave evidence + results (judged head)`
   Ancestry: `merge-base --is-ancestor 480b1a5 d65d823` → yes; `dcd3170 d65d823` → yes;
   `rev-list --count 480b1a5..d65d823` → `2`.
8. `git -C $L cat-file -t 66703aca50529a35be49aa8759d04140720ad` → MISSING in the lane repo, the
   fleet root repo and shokuknow. `git -C $L ls-remote origin` → `d65d823… HEAD`, `d65d823… refs/heads/master`,
   no ref containing `66703ac`.
9. `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 https://api.github.com/repos/VeigaPunk/kasegi-shokunin/commits/66703aca50529a35be49aa8759d04140720ad`
   → `http=422 bytes=171`, body `No commit found for SHA: 66703aca50529a35be49aa8759d04140720ad`
   at `2026-10-26T19:31:51Z`.
10. Variant propagation: `grep -o` counts → 37-char variant `66703aca50529a35be49aa8759d04140720ad`
    appears `51` times in `wave1-spec.json`, `51` in `wave1-dispatch.json`, `2` in `claims.json`;
    the 40-char variant appears `0` times in all three.
11. Wave shape: `wave1-spec.json` keys `wave=kasegi-r39-build`, `milestone=round-39`,
    `reportDir=.ufo/waves/round-39/wave1`, `maxLanes=64`, 49 items; role counts
    `executor 27, scribe 11, reviewer 6, scout 2, critic 2, connector 1`. `wave1-dispatch.json`
    `taskCall.tasks` → 49; `wave1/swarm-registry.json` members → 49, distinct → 49; task names
    distinct → 49, unnamed → 0. Sizes: spec 413733 B, dispatch 433466 B.
12. G8 pin: `git show 2387dcf6:corpus/instruments/r37-closure.sh` → 1558 lines, 73132 bytes,
    sha256 `0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d`.
13. Registry reality: 55 S-rows, ids `S001…S055` contiguous, `uniq -d` → empty, 3 rows already carry
    status `rejected` (`S026`, `S027`, `S028`). `S056`–`S059` absent at tip.
14. Seat-spec arithmetic (`wave1-spec.json` prompts): `ScribeRowsRejected` instructs three rejected
    row files (`S056`, `S058`, `S059`) **and** says `old→new: registry 55 → 58`; `ScribeRowS057`
    instructs one mined row (`S057`); `ScribeFrontierF22` says `the frontier stands at **22/22 admitted**`.
15. Absent at pack time: `.ufo/waves/round-39/final-gates/` (`ls` → `No such file or directory`),
    `corpus/instruments/r39-closure.sh`, `corpus/knowledge/cisa-when-to-issue-vex.md`,
    `corpus/source-snapshots/round-39/`, `corpus/lessons/round-39.md`.
16. Ledger state: `corpus/knowledge/considerthese-proposals-ledger.md` last heading
    `## Round-37 dispositions — filled (round 38)`; no `## Round-39 dispositions` yet.
17. Report-target docs (lane): `SCORECARD.md` 176890 B, `SHONEN.md` 17451 B, `LOG.md` 151862 B,
    `PROVINCE.md` 11794 B, `SKILL.md` 111619 B — each `grep -c 'Round 39\|round-39'` → `0`. Fleet
    root has `SCORECARD.md`/`LOG.md` (both 0 round-39 mentions) and no `SHONEN.md`/`PROVINCE.md`/`SKILL.md`.
18. Control digests: `claims.json` `e427ab6a6ecec4b1f49ed5eed95860c468e0982af331a3a1ba135649d27e051c`;
    `c1-controls/before.txt` `0363c8c072b7a3f7f09e91241149e903af73b757dd02d25b3ff7eedd999e348b`;
    `c2-controls/before.txt` `866ac75797e89409c409cd883051f9f9be4ed78bba9112df972dd800e3977af2`;
    `c2-controls/junk-f22.md` `8a719e6aad12832c443298e9c1a2f939ef60297da3ad0640d51fd0d81ab75506`;
    `census-before.txt` `88a3c813135f4c7260c65918ff51981e668ca31c50c83cec0995db11f170747a`.

## Findings

**F1 — the frozen r38-head revision is 37 characters and cannot resolve.** `claims.json` C1
`kill_rule` and counting command C1.4 carry `66703aca50529a35be49aa8759d04140720ad` (37 chars). It is
absent from the lane, fleet-root and shokuknow object databases (`cat-file -t` MISSING), absent from
`origin` (`ls-remote`: `master` = `d65d823…` only), and GitHub returns
`422 No commit found for SHA: 66703aca50529a35be49aa8759d04140720ad`. The real round-38 head is
`66703acaaff50529a35be49aa8759d04140720ad` per `.ufo/waves/round-38/final-gates/all-gates.txt` line 2
`export-ref=66703acaaff50529a35be49aa8759d04140720ad`, and that object resolves. The bad string was
propagated to every seat (51× spec, 51× dispatch, 2× claims). Impact: the r38 red control as frozen
cannot be executed, and a `git archive` failure exits non-zero without ever printing `closed=8/8`, so a
naive reader can score the red as passed. Reported in the pack §6 F1 with the erratum precedent
(`.ufo/waves/{round-28,round-33,round-34,round-35,round-37}/claims-erratum-*.md`).

**F2 — C2 registry arithmetic is off by one.** Frozen target and kill rule: 58 rows
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 58`). Measured base: 55
rows. The wave instructs four appended rows — `S057` (mined) plus `S056`, `S058`, `S059` (rejected) —
so the instructed plan yields 59 by the same grep (rejected rows already count: `S026`/`S027`/`S028`
are in the 55). `ScribeRowsRejected`'s spec additionally states `registry 55 → 58` for its three rows
alone, which is arithmetically wrong whichever order the rows land. Either target/erratum = 59, or one
row must not land as a registry row. Reported in the pack §6 F2.

**F3 — no after-value could be measured.** `final-gates/` absent and J unnamed by rule; every after
cell is a frozen target. I did not run the suite, the harness, or the census; those are other seats'
gates, and re-running them would have decorated the pack without adding evidence.

## Scope, discipline, limits

- Writes: only `.ufo/waves/round-39/wave1/ScribeReportInputs.inputs.md` (deliverable) and this receipt,
  plus scratch `/fast/scratch/hyaku/kasegi-r39/ScribeReportInputs/` which was removed
  (`[ -e "$S" ]` → NO; `ls -d …/ScribeReportInputs` → absent).
- No mutating git/jj command; `git archive` never run; all git use was `log`/`show`/`ls-tree`/
  `cat-file`/`merge-base`/`rev-list`/`ls-remote`/`status`/`for-each-ref`/`reflog` (read-only).
- One network fetch (GitHub API, status/bytes/time recorded above). No pacman, no installs, no PATH
  writes, no fleet-root or source-tree writes, no `agent://all` message, no subagent dispatch.
- Limits: after values unmeasured; J unknown; F1/F2 are conflicts for the L1 to reconcile, not
  questions I answered by editing the frozen claims.
