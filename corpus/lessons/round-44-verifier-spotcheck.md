author: hyaku closure (non-author integrator, @m_zfl)

# Round 44 — non-author verifier spot-check (kasegi)

Lane-round: kasegi 44. Base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`; tip `5e4d6bf4324421d0e393f4da9bc623165bb5b0b7`. Re-measurements below ran on committed exports (`git archive 5ab3a60` and `git archive 5e4d6bf` extracted to a scratch directory). Gate rule (PROTOCOL §Gate standard, Closure consequence): the lane-owned counter `r44-routed-defects.py` and its selftest were **not executed** by the closure; they are evidence-verified. Everything else is re-measured.

## 1. Conformance (step 1)

- Report `.ufo/reports/round-44/kasegi.md`: `git log --format='%an %H' -- <report>` → `kasegi-shokunin 18f5a1f5f417f3b7993282b4c15711ba18abfdf7` (lane identity). `## SHONEN` heading present, four `[~]` lines, no `[x]`; `SHONEN.md` has four boxes.
- Cited lane commits `6631401 8063547 4aba89c 00e3bd0 7f6de32 c950fa3 5e4d6bf`: all exist; `git merge-base --is-ancestor <h> master` true for each. `master` = `5e4d6bf…`.
- `jj-lane.sh state kasegi-shokunin` → `local=5e4d6bf… remote=5e4d6bf… ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` empty.
- Prompt `.ufo/prompts/kasegi-round-44.md` (689 lines) carries §1–§5 of the round-prompt template (claims, 2b frontier step, L2 floor, report contract, commit scope) plus the hyaku addendum §6–§7.
- Dispatch digest (copied from `.ufo/watchdog.log`): `15:43:26 launch attempt=1`; `16:52:56 lane-dead-no-report (KasegiR44, report_of FAIL)`; `16:52:58 launch attempt=2`; `17:08:06 lane-dead-no-report (KasegiR44a2)`; `17:40:42 launch attempt=3`; `17:44:01 complete attempt=3`. Two attempts filed no report; the report landed only in attempt 3, which adopted attempts 1–2's lane commits. Conformance note, status-neutral (a real, checkable report with real commits exists, so not a marker).
- Waves: `wave1-results.json` 66 entries, `wave2-results.json` 40 entries, every `output` non-empty (counted by me). Seat-report files under `wave1/` and `wave2/` number 54 and 35 `.md` files, fewer than the 66/40 seats; the seats without a file exist only in the results JSON. Minor, status-neutral.

## 2. Per-claim re-check

### C1 — depth:verifiability (eight routed round-43 defects, 8 unresolved → 0)  
Method: **evidence-verified for the counter, plain re-measurement for each defect's artifact.**

| # | Routed defect (spotcheck §6) | Plain re-measurement at tip | Result |
|---|---|---|---|
| 1 | `closed=13/19` unbacked | `SCORECARD.md` diff base→tip appends `Correction (round 43; appended round 44)` superseding the literal and naming `claims-erratum-6.md`; the frozen `.ufo/waves/round-43/claims.json` is untouched (`git diff --name-status 5ab3a60 5e4d6bf \| grep round-43/` shows only two `A` rows: the erratum and the export-ref sidecar) | fixed |
| 2 | no check can see defect 1 | erratum file `.ufo/waves/round-43/claims-erratum-6.md` (4827 B) exists at tip, absent at base. The lane's own appended correction says K17 skips after-cells, so K17's escape does **not** fire for this token and K18 was not widened; the only committed check that sees the literal is the lane's own counter limb D2. The lane says which mechanism, as the defect demanded | fixed (mechanism disclosed; no pre-existing gate widened) |
| 3 | "29-character" numeral | `printf %s c6ae07c6a541e0e96d0040afb6 \| wc -c` → `26`; full hash → `40`; `round-43.md:90` and `:101` still carry "29-character" as byte-identical history; `Correction (round 43; appended round 44)` appended at `round-43.md:167` with the counting commands | fixed |
| 4 | report omits planner=L1 and L2-floor/residual | `git diff base tip -- LOG.md` adds `Planner mapping: planner=L1 …` and `L2 floor … 66 … residual call: none`; report §Work performed also carries both | fixed |
| 5 | wave-evidence hygiene | `all-gates.at-Y.txt.tmp`: `find . -name '*.tmp'` in the lane tree → 0 hits (it was untracked, never in a base tree); `corpus/instruments/wave-registry.py` exists; the sidecar and `controls/round43-registry-names.txt` supersede the empty `names=` | fixed |
| 6 | `SHONEN.md` lost a final empty line | base ends `…\`[~]\`.\n`; tip ends `…\`[~]\`.\n\n` (xxd) | fixed |
| 7 | registry pointer | `corpus/instruments/README.md` diff adds table rows for `r43-closure.sh`, `claim-package-check.py`, `r44-routed-defects.py`, `wave-registry.py` | fixed |
| 8 | `127` vs `exit=2` | `controls/missing-suite-base.txt` shows the direct `bash corpus/instruments/r43-closure.sh` at the base export → `No such file or directory`, `exit=127`; the erratum separates it from the control's `ls` `exit=2` | fixed |

Counter evidence (not executed): `controls/final-attempt3.txt` (tip export `c950fa3`) prints `routed-defects total=8 fixed=0 unresolved=8 exit=1` at the base and `fixed=8 unresolved=0 exit=0` at the tip; `controls/c1-counter-selftest-v2.txt` ends `selftest cases=20 failures=0`; `git diff --name-only 4aba89c 5e4d6bf -- corpus/instruments` is empty, so the counter bytes that the selftest and the tip run measured are the final bytes; `5e4d6bf` adds receipts, `LOG.md` and `SCORECARD.md` only. The base-red control (marker-only and fabricated trees rejected) is committed: `controls/r44-counter-trial-disposition.txt`, selftest mutants D1–D8. Caveat: `final-attempt3.txt` also prints an argparse usage error for a bare `--selftest` call followed by `exit=0` (a receipt artifact, the real selftest line follows); the receipt wording is sloppy, not the evidence.
Verdict: **verified.** `depth:verifiability` = **improved** (all eight routed defects have a committed artifact fix and a fail-closed counter that is red at base).

### C2 — coverage (admitted frontier rows 25 → 26; SOURCES rows 68 → 70; knowledge 62 → 63)  
Method: **re-measured by me** on exports.

| Count | Command | base | tip |
|---|---|---|---|
| frozen counter | `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md` | 0 | 0 |
| frontier rows | `grep -cE '^\|[[:space:]]*F[0-9]+[[:space:]]*\|' corpus/README.md` | 25 | 26 |
| admitted frontier rows | awk on 4th `|` field `== admitted` | 25 | 26 |
| SOURCES rows | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 68 | 70 |
| knowledge entries | `find corpus/knowledge -maxdepth 1 -name '*.md' \| wc -l` | 62 | 63 |
| pre-existing S0xx rows changed | `diff` of the `S0..` row lines base vs tip, count of `<` lines | — | 0 |

The frozen counter string is defective (the status is the fourth `|`-delimited field, so the regex reads 0/0); the lane disclosed this and did not claim a frozen-counter pass. The same declared predicate re-derived table-aware gives 25 → 26, matching the lane. `r44-frontier-count.py` (the lane's table-aware counter) has **no selftest and no registry row** (grep in `SKILL.md` and `corpus/instruments/README.md` → no mention), so it is a probe, not a gate; the closure rests on my own plain counts. `corpus/README.md` diff is 20 additions / 0 deletions; `corpus/SOURCES.md` 7 / 0. Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `W04 S028`, `W04 S029` duplicate-URL warnings (pre-existing), `kasegi ok`, exit 0.
Verdict: **verified**, with the frozen-counter defect named. `coverage` = **improved**. Non-author gate in the C2 kill rule: §4 below agrees on the admit and on the reject outcome.

### No-harm
`git diff 5ab3a60 5e4d6bf -- SCORECARD.md` is 49 appended lines, 0 removed; scores held 4 / 8 / 9. `PROVINCE.md`, `SKILL.md`, `corpus/instruments/README.md`, `knowledge-expected.txt`, `round-43.md`: all pure appends (no `-` lines). `corpus/instruments/density.py` byte-identical base→tip (`git diff --quiet`). `depth:density` = **unchanged**.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability | improved | C1 verified: eight defects, plain artifact checks plus committed fail-closed counter (20 graded cases, red at base) |
| coverage | improved | C2 re-measured: 25→26 admitted frontier rows, 68→70, 62→63; census exit 0 |
| depth:density | unchanged | `density.py` byte-identical; no claim |

## 4. Discernment spot-check (LEARNING.md, from outside)

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S069 — Google Cloud VRP rules (tier A, `mined`) → F26 | admit | `https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules`: the HTML page is a metadata shell for a plain fetch, so I re-opened the same document through `https://bughunters.google.com/rest/v1/articles/about/rules/google-friends/cloud-vulnerability-reward-program-rules` (HTTP 200, 48 657 B). Located by whitespace-normalised substring: Q1 "The Google Cloud VRP scope is strictly limited to Google-owned infrastructure and services.", Q4 "…still considered unauthorized testing within customer space.", Q5 "…reasonably sensitive user data is intended to be in scope." — all present. Pinned `corpus/source-snapshots/round-44/S069.txt`: sha256 `0932279c…f2`, 45 681 B, lines 10–11, 61–63, 70–72, 76–77 contain the quoted text (`sed -n` on those lines) | **agree** | It is a primary, official program rule; the entry stays inside Cloud VRP, carries the "not a general authorization opinion" limit and a named rejected over-generalisation, and adds ground not held by F01/F03/F09/F13 (customer-IP-range rule, local reproduction). The live body is now 47 202 B, not byte-identical to the pin (lane disclosed formatting drift, `controls/S069-live-drift.txt`); the quoted text is intact |
| S070 — Google Bug Hunters rules directory (tier C, `rejected`) | reject | `https://bughunters.google.com/about/rules/about-this-section` plus `…/rest/v1/articles/about/rules/about-this-section` (HTTP 200, 10 029-char body) | **agree on the decision, disagree with the stated reason** | The directory is an overview table (program → scope → where to report); it restates Cloud VRP scope as "any Google Cloud product or web service that handles reasonably sensitive user data" — already Q5 of S069 — and adds no customer-resource boundary rule, so no knowledge entry is warranted. But the row and lesson say the body "is a JavaScript shell … no quotable rule text"; through the same article API the lane used for S069 the body is readable and quotable, so the rejection reason is factually wrong and the flip condition ("a readable, dated copy … that carries a quotable rule text") is already satisfied. Correct reason: low-information overview that duplicates S069 Q5 |
| New `SOURCES.md` row S069 quote | ≤25-word check | the S069 row's quoted heading "Do Not Test Customer Projects & Resources" (7 words) exists at snapshot line 59; the entry's Q4 quote is 21 words (counted) and located at lines 76–77 | agree | quotes short, located, verbatim |

Census: see §2 (exit 0).

## 5. Trend verdicts

- **expansion: improved** — F26, one admitted knowledge entry citing the `mined` S069 row, SOURCES 68→70, census clean.
- **quality: improved** — a fail-closed, digest-pinned counter replaced two falsified drafts (wave-1 marker-only, wave-2 fabricated tree), each falsification committed; all lane edits append-only. Caveat: the frozen C2 counter is defective and `r44-frontier-count.py` has no selftest.
- **discernment: unchanged** — the outside check agrees on the admit and on the reject outcome, but the reject's stated reason is factually wrong (S070 body is readable via the API) and `corpus/QUALITY.md` gained no criterion from the ten mined mistakes (`grep -c M44 corpus/QUALITY.md` → 0; M44-2, M44-5, M44-9 name no catching criterion). Not `harmed`: the disagreement is routed below.

## 6. Routed defects — the lane must fix these in round 45

1. **S070 reject reason.** Append (never rewrite) a correction to `corpus/SOURCES.md` S070 and `round-44.md` `## Gate`: the article API returns a readable 10 029-char body; the true reason is "overview, no program-specific rule beyond S069 Q5". Replace the vacuous flip condition with a checkable one (e.g. the directory gains a rule paragraph not present in a program's own rules page).
2. **QUALITY.md criteria from mistakes.** Add grounded criteria citing `round-44.md` for the classes no criterion caught — "frozen counter must be replayed on a do-nothing control before data" (M44-3/M44-8), "presence-only predicates accept denials and fabricated trees" (M44-4/M44-7/M44-10), "capture method used for admit must also be used for reject" (this spot-check).
3. **`r44-frontier-count.py`** is an unregistered probe with no selftest; register it as a probe or give it a selftest and a registry row at its home (`SKILL.md` Gates & probes — `r44-routed-defects.py` and `wave-registry.py` are also missing from `SKILL.md`, present only in `corpus/instruments/README.md`).
4. **Freeze hygiene.** A frozen counter string must be run on the base before freeze (the C2 string read 0/0); the round-45 planned gates already say so — hold the lane to it.
5. **Receipt wording.** `controls/final-attempt3.txt` lists an argparse usage error followed by `exit=0` for the bare `--selftest` call; re-file the selftest invocation line without the failed call.
6. **L1 process defect** (self-reported): two L1 attempts ended without a report; no lane-side gate. Not status-bearing.

## 7. Operator note

All four `SHONEN.md` boxes are `[~]`. As in round 43, boxes 1, 3 and 4 are mechanically checkable by a non-author (F26 entry and S069 recheck pass; counter and frontier CLIs documented and run from exports; PROVINCE amendment is a single appended F26 line, sibling sweep `wave1/R44Scout8.md`). Box 2 (end-to-end domain task) is not exercised. Writing `[x]` is operator-owned and not done here.
