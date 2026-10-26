# ExecRegressionC2 — final C2 regression at quiescent tip

Seat: ExecRegressionC2 (leaf executor, L2 wave of kasegi-shokunin round 35).
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin (only write scope used: this receipt).
Lane base 3266c9937b03062d9bbc2f436e20820115ed179c; claims-freeze 617496b9c6e92bc671e7e78b83df69a04470d0e9;
worktree HEAD at reading da2d3c687f82a9814ee71c91c930cb733050d37c (jj-colocated; the L1 owns all commits).
Frozen claim under test: C2 `coverage` (`claimed score_before 7 -> held 7`), counting_commands 1-7 in
`.ufo/waves/round-35/claims.json`.

## Report

### 1. What this seat did (scope)

Ran every C2 counting command from claims.json **verbatim**, from the lane root, at the quiescent tip bytes,
and compared each output with the frozen `after` array. No file in the lane was written except this receipt;
no git/jj mutation was issued; no subagent, wave or background job was started; nothing was installed.

Reading protocol: each command is executed as a separate subprocess (`grep`, `python3`, the census
validator) with stdout+stderr captured and the exit status recorded; a run counts as *quiescent* only when
the SHA-256 of all seven C2 surfaces is identical immediately before and immediately after the run
(`q-pre.digests` vs `q-post.digests`) and unchanged again on a re-digest 20 s later.

### 2. Before state — as found at 06:32:22Z (counter discrimination)

Recorded before any C2 landing existed, so the commands are shown to move for the claimed change and not by
construction. This block is the exact log (`before-verbatim.txt`, sha256
`3a743d152bfc76ee4d7398c2699165d2d4b1242422a3594206f0702a95dc596d`):

```
### BEFORE (as found at 2026-10-26T06:32:22Z)
--- CMD1: grep -cE '^\| F[0-9]+ \|' corpus/README.md
17
exit=0
--- CMD2: grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
51
exit=0
--- CMD3: grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md
0
exit=1
--- CMD4: grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l
0
exit=0
--- CMD5: python3 corpus/instruments/frontier-recheck-count.py
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0   
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0   
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0   
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0   
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0   
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0   
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0   
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0   
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0   
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0   
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0   
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0   
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0   
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0   
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0   
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0   
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0   
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0   
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0   
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0   
entries=20 pass=20 exit=0
exit=0
--- CMD6: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
manifest UNAVAILABLE reason=missing
exit=2
--- CMD7: census validate
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
--- knowledge entries: ls corpus/knowledge/*.md | wc -l
46
```

Every before value equals the frozen `before` array: frontier 17; registry 51; S052 row 0 (grep exit 1);
entries citing `source: S052` 0; harness `entries=20 pass=20 exit=0`; source-recheck S052
`manifest UNAVAILABLE reason=missing`, exit 2; census exit 0 with W04 S028/S029 only; knowledge entries 46.

### 3. Quiescence framing — the tip moved three times before the final reading

The entry bytes were still being revised while this seat watched, so earlier green readings are reported
rather than hidden:

| reading (UTC) | entry `cisa-kev-catalog.md` sha256 (first 12) | pre==post during run | counters |
|---|---|---|---|
| 06:41:39Z | `da81204b3fbc` | yes | all 7 matched |
| 06:45:25Z | pre `0988866608c4` -> post `e3f233c0d5e5` | **no (moved)** | all 7 matched |
| **06:47:24Z (final)** | `e3f233c0d5e5` | **yes** | all 7 matched |

Only the entry moved: `corpus/README.md` `277f04cedfb0`, `corpus/SOURCES.md` `0f95a132a69e`,
`corpus/source-snapshots/round-35/manifest.json` `06bfcc71e6df` and `S052.txt` `d69349e86c5c` were
byte-identical across all three readings and across a 110 s observation window
(06:45:33Z-06:47:02Z: entry `e3f233c0d5e5`, README `277f04cedfb0`, SOURCES `0f95a132a69e` at every check).
A re-digest 20 s after the final run still gave entry `e3f233c0d5e5`, README `277f04cedfb0`, SOURCES
`0f95a132a69e`. Because commands 4-6 read the entry (its `source:`/`recheck:` header and its README row
binding), the final reading is the one that counts; §4 is that run.

### 4. Final quiescent reading — 06:47:24Z, verbatim, all seven commands

Exact log `q-verbatim.txt`, sha256 `866b4de9d91247febc5c6cfdea34297a641d62c4575ce569c2f7a24f18379b30`:

```
### C2 counters at 2026-10-26T06:47:24Z (lane root: /home/vgpnk/Projects/shokunin/kasegi-shokunin)

--- $ grep -cE '^\| F[0-9]+ \|' corpus/README.md
18
exit=0

--- $ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
52
exit=0

--- $ grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md
1
exit=0

--- $ grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l
1
exit=0

--- $ python3 corpus/instruments/frontier-recheck-count.py
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0   
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0   
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0   
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0   
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0   
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0   
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0   
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0   
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0   
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0   
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0   
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0   
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0   
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0   
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0   
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0   
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0   
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0   
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0   
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0   
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0   
entries=21 pass=21 exit=0
exit=0

--- $ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
S052:sha256 OK
S052:Q1 OK occurrences=1 anchor=2-ok
S052:Q2 OK occurrences=1 anchor=3-ok
S052:Q3 OK normalized=markup-whitespace occurrences=1 anchor=4-ok
S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=15472-ok
S052:Q5 OK normalized=markup-whitespace occurrences=1 anchor=19165-ok
exit=0

--- $ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0

```

Exit codes: cmd1 `exit=0` (18), cmd2 `exit=0` (52), cmd3 `exit=0` (1), cmd4 `exit=0` (1, grep status via
PIPESTATUS), cmd5 `exit=0` (`entries=21 pass=21`), cmd6 `exit=0`, cmd7 `exit=0`. Wrapper exit 0.

### 5. Claimed `after` vs measured — matches and mismatches

| # | frozen `after` (claims.json C2) | measured at 06:47:24Z | verdict |
|---|---|---|---|
| 1 | `frontier_admitted=18` | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` -> 18 | **match** |
| 2 | `registry rows=52` | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` -> 52 | **match** |
| 3 | `S052 row=1` | `grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md` -> 1 (line 58) | **match** |
| 4 | `entries citing S052=1` | `grep -lE '^source: S052 ' corpus/knowledge/*.md \| wc -l` -> 1 | **match** |
| 5 | `harness entries=21 pass=21 exit=0 incl. PASS F18 ids=S052` | `entries=21 pass=21 exit=0`; line `PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0` | **match** |
| 6 | `source-recheck S052 exit 0, every assertion occurrences=1, sha256 OK` | `S052:sha256 OK`; Q1-Q5 each `OK ... occurrences=1 anchor=N-ok`; exit 0 | **match** |
| 7 | `census exit 0 (W04 S028/S029 only)` | two `W04` lines (S028, S029) + `kasegi ok .../corpus/SOURCES.md`; exit 0 | **match** |
| extra | `knowledge entries=47` | `ls corpus/knowledge/*.md \| wc -l` -> 47 | **match** |

Mismatches: **none**. The seven counters and the knowledge-entry count sit exactly on the frozen after
values, on bytes that did not move during the run.

### 6. C2 surface digests at the final reading (`q-pre.digests` == `q-post.digests`)

```
277f04cedfb06f493ae5da636d665b490ac0e78b26ea282b0d0ef3a469d3ffa2  corpus/README.md
0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba  corpus/SOURCES.md
e3f233c0d5e5a1c5a876aa396b1c42e8265f5e3a4cd076837deac50af6de2730  corpus/knowledge/cisa-kev-catalog.md
06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee  corpus/source-snapshots/round-35/manifest.json
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  corpus/instruments/frontier-recheck-count.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py```

The S052 registry row (line 58) parses to 11 cells (`awk -F'|'` -> 13 fields with the two outer empties):
`S052 | CISA Catalog of Known Exploited Vulnerabilities (KEV catalog JSON feed) — <feed URL> | dataset | A |
... | mined | 2026-10-26 | 90d | corpus/knowledge/cisa-kev-catalog.md`. The final entry header lines 1-6 are
H1, `source: S052 — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`,
`verified-at: 2026-10-26`, `ground: F18`, and one `recheck:` line naming
`--manifest corpus/source-snapshots/round-35/manifest.json --source S052`. The F18 README row (line 388)
has 6 columns (`F18 | <topic> | admitted | knowledge/cisa-kev-catalog.md | S052 | <next>`).

### 7. Checks outside this seat's command set (reported, not adjudicated)

- The L1 appended the F18 frontier row and its coverage-map row at 06:41:06Z after this seat reported that
  no wave1 seat owned it (ScribeEntryF18 R8: "The corpus/README.md F18 frontier row ... L1 owns these").
  The row is what makes command 1 read 18 and command 5 emit `PASS F18`.
- `corpus/knowledge/cisa-kev-catalog.md` was revised four times while this seat watched
  (`da81204b` -> `a5696dc0` -> `7429811c` -> `09888666` -> `e3f233c0`); each revision kept the header
  binding intact (harness passed on every reading), but the final reading covers `e3f233c0` only.
- The junk twin exists at `.ufo/waves/round-35/c2-controls/junk-f18.md` and is outside the admission
  surface measured here: it is not under `corpus/knowledge/` (0 matches) and is not named in the round-35
  manifest (`grep -c junk` -> 0). Its rejection verdict belongs to MutJunkTwin/CritC2Kill, not to this seat;
  `MutC2Entry.md` was present in the wave dir at reading time, `MutJunkTwin.md` was not.

### 8. Risks and limits

1. **Reading covers worktree bytes, not a commit.** HEAD is `da2d3c68` and the C2 landings are uncommitted
   (`git status --porcelain` -> 19 entries, incl. `M corpus/README.md`, `M corpus/SOURCES.md`,
   `?? corpus/knowledge/cisa-kev-catalog.md`, `?? corpus/source-snapshots/round-35/`). If the L1 or any later
   seat edits one of the seven digested files, these readings no longer describe the tip; re-run them after
   the final edit and before the commit. The entry was still moving 80 s before the final reading.
2. **Command 4 is form-sensitive.** `^source: S052 ` includes the trailing space; the landed entry matches
   it (line 3), but an edit that drops that space would make the counter read 0 while the entry still
   declares S052. The count is a shape check, not a semantic one.
3. **Command 1 and 5 read the README row shape.** `frontier-recheck-count.py` binds rows through its
   `FRONTIER_ROW` pattern (`^\|\s*(F\d+)\s*\| ...`); a reflow that breaks the six-column shape drops the
   entry silently (`entries=20`) rather than failing.
4. **Command 6 is a captured-bytes check.** It proves the pinned 1,479,694-byte JSON feed still carries each
   quote exactly once at its anchor; it does not verify the live CISA feed and does not assert that the
   entry's reading of those bytes is the only possible one.
5. **Census W04 lines are pre-existing.** S028/S029 duplicate-URL warnings are unchanged by S052; the S052
   URL (the `/sites/default/files/feeds/known_exploited_vulnerabilities.json` feed path, not the 404
   `/known-exploited-vulnerabilities.json`) is unique in the registry, so no new warning appears.

### 9. Tooling and hygiene

- No tool installed or upgraded (none needed); no `pacman`, `uv`, `npx` or binary download was run.
- No network call beyond the read-only census validator and the two committed-by-others instruments; no
  credential, token or session material was read.
- Scratch `/fast/scratch/hyaku/kasegi-r35/ExecRegressionC2/` held only the runner script, the before and
  final logs and digest files; all of it was removed before this seat yielded (see §10). Evidence lives in
  this receipt, not in scratch.
- No `git add`/`commit`/`push`, no `jj` mutation, no write outside this lane.

### 10. Scratch teardown

`rm -rf /fast/scratch/hyaku/kasegi-r35/ExecRegressionC2` is executed as this seat's last step, after this
receipt is in place; the receipt carries both verbatim logs and every digest, so nothing in the regression
depends on the scratch tree.
