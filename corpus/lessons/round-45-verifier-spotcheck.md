author: hyaku closure (non-author integrator, @m_zfl)

# Round 45 — non-author verifier spot-check (kasegi)

Lane-round: kasegi 45. Base `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd`; tip `2998baab4c39e6f0c1b50b150c5965e1643c4e11`. Plain re-measurements ran on committed bytes (`git show <rev>:<path>`, `git diff`, `git ls-tree`) and on live re-fetches of the two cited sources (scratch `/fast/scratch/hyaku/kasegi-r45-closure`, not evidence). Per PROTOCOL §Gate standard (Closure consequence) no lane gate or counter was executed by me: the lane counters (`r45-routed-defects.py`, `r45-c2-gate.py`, `freeze-check.py`, the selftests) are **evidence-verified** from the committed receipt `.ufo/waves/round-45/controls/final-measure.txt` (measured at lane commit `3106889`, `measured-at-rev: 3106889`, base `dc5bb8c`); every claim was additionally **re-measured plain** on the underlying artifacts, so no verdict rests on a counter alone.

Driver digest (`.ufo/watchdog.log`): `2026-10-28T17:49:14-03:00 launch kasegi round=45 pgid=1704523 driver=hyaku-inline attempt=1`; `2026-10-28T19:38:28-03:00 complete kasegi round=45; hyaku-inline attempt=1`.

## 1. Conformance (step 1)

| Check | Command | Observed |
|---|---|---|
| Report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-45/kasegi.md` | `kasegi-shokunin a1f7761b572e8c78d9d3b64d5d1e6a655f152a11` |
| `SHONEN` heading, one line per box | `grep -n '^## SHONEN'` + read | present (line 65); four boxes, all `[~]`, each with an evidence pointer, none `[x]` |
| Required sections in order | read | Work performed, Landed changes, Before → after, Sources & frontier, Trend verdicts, (Stale-lane, Tooling), SHONEN: present |
| Cited lane commits are ancestors of `master` | `git merge-base --is-ancestor <h> master` | `8cf62c8`, `5242db6`, `6662a42`, `98878b7`, `3106889`, `2998baa`, base `dc5bb8c`: all `anc ok` |
| Lane pushed, clean | `scripts/hyaku/jj-lane.sh state …/kasegi-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `local=remote=2998baab… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; ls-remote `2998baab…` |
| Round commits in lane | `git log --oneline dc5bb8c..master` | six commits, matching the report's Landed-changes table |
| Prompt carries template contract | read `.ufo/prompts/kasegi-round-45.md` §§1–5 vs `templates/round-prompt.md` | §1, §2, §2b, §3, §4, §5 present with the template text, plus hyaku addendum §6 and scratch §7 |
| Not a marker report | read | real committed work, receipts, counters, selftests |

Conformance defects (status-neutral): (a) the report commit `a1f7761` is dated 19:30:06 -0300 while the lane commit `2998baa` it cites as final ("landed, remote-verified") is dated 19:36:30 -0300 — the report names a hash by a timestamp earlier than that hash's own; the hash resolves and is an ancestor, so this is an ordering anomaly, not a dead hash. (b) The report's wave-1 dead seat (`R45ScoutConsiderthese`) is disclosed, not replaced — fine. (c) Scores held at 4/8/9 while the verdicts below are `improved`; see §3 note.

## 2. Per-claim re-check

Both claims are measured, neither exploratory. Frozen at `8cf62c8` (`claims.json`, sha256 `bbe40503…c6206`).

### C1 — depth:verifiability — 0 → 5 of the five round-44 §6 status-bearing routed defects resolved — **re-measured plain; counter evidence-verified**

| Limb | Plain check (base `dc5bb8c` → tip `master`) | Observed |
|---|---|---|
| R1 S070 reject reason superseded | `git show <rev>:corpus/SOURCES.md \| grep -nE '^\|[[:space:]]*S07[012][[:space:]]*\|'` | base: S070 only; tip: S070 **byte-identical** + S071 + S072; S072 `teaches` opens `supersedes S070 —`, states the true reason (overview; Cloud VRP line restates S069 Q5), carries a checkable `flip:` (a fresh article-API capture states a program-specific rule the program's rules page does not), status `rejected`. `git show <rev>:corpus/lessons/round-44.md \| grep -c 'Correction (round 45'` → base `0`, tip a block at line 205 naming `round-44.md:22` and `:131`; `git diff --stat dc5bb8c master -- corpus/lessons/round-44.md` → `2 insertions(+)`, no deletions (append-only). `sha256sum` of `.ufo/waves/round-45/source-recon/S072.txt` → `364166c4…0a025`, 10032 B file, equals the pin in the S072 row. |
| R2 QUALITY criteria R47/R48/R49 grounded in round-44 | `grep -nE '^\|[[:space:]]*R4[789][[:space:]]*\|' corpus/QUALITY.md` | base `0`; tip R47 (frozen counter replayed on do-nothing control, before-VALUE), R48 (presence-only predicates; r44 mines `round-44.md:16`), R49 (admit method must also be the reject method; `round-44.md:22`, `:131`) — exactly the three classes spot-check item 2 named; `grep -c 'round-44' corpus/QUALITY.md` → 3 |
| R3 `r44-frontier-count.py` selftest + registry rows | `grep -c selftest corpus/instruments/r44-frontier-count.py`; `grep -c 'r44-frontier-count' SKILL.md corpus/instruments/README.md`; same for `r44-routed-defects.py`, `wave-registry.py` in SKILL.md | base `0` / `0` / `0`; tip `16` / `1` / `1`; SKILL.md carries all three names (base `0` each) — all three missing rows named in item 3 landed. Selftest tally **evidence-verified**: `final-measure.txt` `selftest cases=61 failures=0`, `mutants=10 rejected=10`, exit 0. |
| R4 freeze hygiene tool | `git cat-file -e <rev>:corpus/instruments/freeze-check.py` | base: absent; tip: present. Evidence-verified: `freeze-check claims=2 base_ok=2 exit=0` (both frozen counters print their declared before-line at the base) and `selftest cases=27 failures=0` in `final-measure.txt`. |
| R5 refiled selftest receipt | `git ls-tree -r --name-only master .ufo/waves/round-44/controls \| grep attempt3`; `grep -c 'usage:' …final-attempt3-refiled.txt` | `final-attempt3.txt` unchanged + new `final-attempt3-refiled.txt`; `usage:` count `0`; one invocation line, 20 `selftest case=` lines, `selftest cases=20 failures=0`, `exit=0` |

Counter reading (evidence-verified, not executed): `final-measure.txt` base `routed-defects total=5 fixed=0 unresolved=5 exit=1`, tip (`3106889`) `fixed=5 unresolved=0 exit=0`; controls `controls total=5 red=5 green=0` (`controls/freeze-controls-v1.2.txt`); `r45-counters-selftest-c1` `cases=85 failures=0`.

**Ruling on the counter classification.** The lane left open whether v1 → v1.2 is a counter erratum or a changed rule (`counter-errata.md`). I rule **counter erratum** (round-44 precedent: same predicate, counter hardened after a falsify wave, closure `verified`): the frozen claim sentences, the five limbs R1–R5 and the target values are unchanged (`counter-errata.md` "Digests", claims sha256 unchanged), the kill rule's own parenthesis exempts "bug fixes that keep the predicate", and — decisively — my plain re-derivation of the original claim sentence (table above) does not use the counters at all and agrees. The caveat is real and stays disclosed: the v1.2 counters are pinned-artifact graders (they reject anything but the genuine bytes), so a green counter is no longer an independent test of quality; the verdict here rests on the plain checks.

**C1: verified** — 5/5 plain; score held at 4 is the lane's own conservative reading (no promotion limb moved).

### C2 — coverage — admitted frontier rows 26 → 27 — **re-measured plain**

| Measure | Command | Base `dc5bb8c` → tip `master` |
|---|---|---|
| SOURCES rows | `git show <rev>:corpus/SOURCES.md \| grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | `70` → `72` (S071 `mined`, S072 `rejected`) |
| Knowledge entries | `git ls-tree --name-only <rev> corpus/knowledge/ \| grep -c '\.md$'` | `63` → `64` |
| Frontier rows | `git show <rev>:corpus/README.md \| grep -cE '^\|[[:space:]]*F[0-9]+'` | `26` → F27 row present at line 651, status `admitted`, entry `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md`, source S071 |
| Before-grep (claim's absence sweep) | `git grep -liE 'security-bugs\|linux kernel\|kernel\.org' <rev> -- corpus/knowledge corpus/SOURCES.md corpus/README.md` | base: nothing; tip: README, SOURCES, the new entry only |
| Pinned capture | `git show master:corpus/source-snapshots/round-45/S071.txt \| sha256sum; wc -c -l` | `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40`, `20152` B, `372` lines = the row's and manifest's pins |
| Capture vs live upstream | `curl https://docs.kernel.org/_sources/process/security-bugs.rst.txt \| sha256sum` (HTTP 200, 20152 B) | `0918dcfa…f40` — **byte-identical** to the pinned capture |
| Frozen cores in entry | read | 7-day ceiling / 14-day exception (`S071.txt:310-311`), AI-assisted find treated as public (`:95-96`), “Binary-only executables are not accepted” (`:39-40`), unreproducible is not a security bug (`:41-43`) — all four present and located |
| Entry quotes | script: normalise whitespace/markup, find each curly-quoted span of the entry in the live capture; count words | **29 of 29** located, **0** over 25 words |
| Census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `W04 S028`, `W04 S029`, `W04 S072 duplicate url … across scopes`, `kasegi ok`, **exit 0** (S072/S070 share a URL across scopes: warning only) |

Counter reading (evidence-verified, not executed): `c2-gate fixed=1/7 exit=1` → `fixed=7/7 exit=0`; `r44-frontier-count --expect 27` exit 1 (26) → exit 0 (27); `r45-counters-selftest-c2 cases=115 failures=0`; `capture-binding-check records=59 bound=59 unbound=0`; `freeze-check` replay `base_ok=2`. Claims erratum 1 (the `1/7` before-value is the base reading; the freeze tree reads `2/7`) is disclosed and correct: the base reading is what the frozen claim names.

**C2: verified** — 3 count deltas re-derived, source bytes re-fetched live and equal, all 29 entry quotes located.

### No-harm sweep

`git diff --numstat dc5bb8c master -- . ':!.ufo/waves/round-45'` shows deletions in one file only: `corpus/instruments/r44-frontier-count.py` (329 +, 39 −; the counting body was refactored into a testable function and the selftest added — counts agree with my plain greps at both revisions). All other modified files (`LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/README.md`, `knowledge-expected.txt` +1 line, `round-44.md` +2) are pure appends/insertions. `git diff --quiet dc5bb8c master -- corpus/instruments/density.py` → identical. `SCORECARD.md` diff: `+36 lines`, pure append (scores 4/8/9 held, rows disclose that held score = no promotion limb moved).

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability | improved | C1: five routed defects 0 → 5 resolved, each plain re-measured; new committed capability `freeze-check.py` (selftest 27/0, evidence-verified). Lane held the score at 4 — the score is a lane-owned number and the verdict is on the claim's measured before→after. |
| coverage | improved | C2: admitted frontier rows 26 → 27, SOURCES 70 → 72, knowledge 63 → 64; capture byte-identical to live upstream; census exit 0. A +1 row is an expansion count, not a coverage-ratio move — the lane's held score of 8 is consistent. |
| depth:density | unchanged | `density.py` byte-identical; no claim; SKILL.md mean change is an appended registry block, not credited. |

No owned axis harmed. Both claims verify → **admitted**.

## 4. Discernment spot-check (LEARNING.md, from outside)

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S071 — Linux kernel security-bugs process (tier A, `mined`) → F27 | admit | `https://docs.kernel.org/process/security-bugs.html` (HTTP 200, 33 621 B) and its RST capture `https://docs.kernel.org/_sources/process/security-bugs.rst.txt` (HTTP 200, 20 152 B, sha256 `0918dcfa…f40`). Located by whitespace-normalised substring in ±2 lines of the manifest anchor: Q1 “for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days” (21 words, `:310-311`), Q2 “If you resorted to AI assistance to identify a bug, you must treat it as public” (16, `:95`), Q3 “Binary-only executables are not accepted.” (5, `:39`), Q4 “By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug.” (19, `:41`), Q5 “with no version indication, your report will not be processed” (10, `:20`), plus “Reports are to be sent over e-mail exclusively” (`:257`) | **agree** | An upstream project's own intake and embargo rules are a new source class absent from the base (absence sweep empty at `dc5bb8c`); tier A is right for a first-party process page; the quotes are verbatim, short and located; the entry stays within the row's scope (limits exclude CVE, linux-distros, NDAs) and its 13-row question/quote/consequence table has actionable consequences (version identifier, binary-only refusal, AI-find-as-public, release-process-start anchoring of the 7/14-day clock). All ten section headings cited in the row exist at their stated lines (`:3,10,73,109,174,254,299,329,359,368`). |
| S072 — Google Bug Hunters rules directory, article-API capture (tier A, `rejected`, supersedes S070) | reject with correction | `https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section` (HTTP 200, JSON `body` of 10 029 characters; whitespace-stripped body equals the committed `S072.txt`); cloud-VRP rules article `…/google-friends/cloud-vulnerability-reward-program-rules` via the same API (47 178-char body) | **agree** | The body is a program → scope → where-to-report table whose Cloud VRP row reads “Security issues affecting any Google Cloud product or web service that handles reasonably sensitive user data” (line-wrapped in the source; 16 words); the S069 rules article states the same scope in its own words (“…product or web service that handles reasonably sensitive user data is intended to be in scope.”), so the directory adds no operative rule and no entry is warranted. The corrected reason is now true (round 44's “JavaScript shell … no quotable rule” was not), the flip is checkable, S070 is untouched, and the lesson correction is appended, not rewritten. This closes round-44 §6 item 1. |
| New `SOURCES.md` row S071 key-quote cell | ≤25-word check | S071 row's quote cell = ten section headings with line numbers; all re-located in the live RST (see S071 row above) | agree | headings are short, verbatim and located; the long quotes live in the manifest/lesson and are each ≤21 words (checked) |
| New `SOURCES.md` row S072 key-quote cell | ≤25-word check | S072 row's cell = section headings + the Cloud VRP line `:148-149` (16 words) | agree | the Cloud VRP line was located by whitespace-normalised substring in the re-fetched body |

Census: see §2 (exit 0, `W04` warnings only).

## 5. Trend verdicts

- **expansion: improved** — F27 admitted, one knowledge entry citing the `mined` S071 row, SOURCES 70 → 72, knowledge 63 → 64, a new source class (an upstream project's own intake and embargo rules), census exit 0. The lane's own reading agrees.
- **quality: improved** — a weaker S070 reject was superseded by a stronger sha-pinned S072 with an appended lesson correction; the new entry's 29 quotes all re-verify against live upstream bytes and the lane's frontier recheck reads `entries=30 pass=30` (evidence-verified, `final-measure.txt`); no admitted entry failed its re-check. Caveat carried from §2: the new counters are bytes-pinned graders (not independent measures) and the lane's selftest tallies (85/115/27/61) are capability, not a measurement of the corpus.
- **discernment: improved** — the lane's **own** assessment is `unchanged`; I rule `improved` because LEARNING.md's criterion is met: round 44's outside spot-check disagreed on the S070 reject reason, and that disagreement became a lesson (`round-44.md` correction) that added a grounded criterion (QUALITY R49, citing `round-44.md:22` and `:131`; R47/R48 likewise grounded in the round-44 mines) — verified plain in §2 — and this round's outside check agrees with the gate on both the admit (S071) and the reject (S072). The lane's `unchanged` is conservative because no non-author judgment existed when it reported; this document supplies it.

## 6. Routed defects — the lane must fix these in round 46

1. **Report/commit ordering** — file the report only after the lane commit it cites exists (report commit `a1f7761` 19:30:06 precedes the cited lane commit `2998baa` 19:36:30; hash resolves, so status-neutral). Cite the hash after `git ls-remote` shows it.
2. **Counter classification** — decide erratum vs changed rule inside the round (before closure), by diffing the prose predicate and by a plain re-derivation that does not use the counter; leaving it for the closure invites a verdict dispute. This closure ruled erratum (§2).
3. **Counters are pinned-artifact graders** — a counter that fails any tree not carrying the lane's own bytes cannot test a non-author's alternative repair. For round 46, give each claim a second, *plain* measurement (grep/wc/jq over committed bytes) beside the counter, as this spot-check does, so a verifier need not trust the pinned counter.
4. **S072 duplicate-URL warning** (`W04`, same URL as S070 across scopes) — acceptable for a supersede pair, but record the pair in `corpus/SOURCES.md`'s registry notes so a future census reader does not treat it as an accident.
5. **Scores held at 4/8/9 while claims verified** — `SCORECARD.md` `## Round 45 result` already says a held score means no promotion limb moved; for round 46 name, per held axis, the specific next promotion limb (`Distance-to-next-score`, `SCORECARD.md` line 1532) the next claim targets, so a held score is a decision and not drift.

## 7. Operator note

All four `SHONEN.md` boxes are `[~]`. Boxes 1, 3 and 4 are mechanically checkable by a non-author this round (F27 entry and S071 recheck re-verified here; counter/frontier/freeze CLIs documented and run from exports per `final-measure.txt`; PROVINCE gained one appended F27 line and the lane's sibling sweeps found no sibling holding). Box 2 (end-to-end domain task) is not exercised: no target testing or submission was performed. Writing `[x]` is operator-owned and not done here.
