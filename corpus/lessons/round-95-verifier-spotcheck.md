author: hyaku closure (non-author integrator, @m_zfl)

# Round 95 — verifier spot-check (non-author closure judge)

Lane: kasegi. Report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-95/kasegi.md`.
Lane HEAD before the round: `9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10`; prompt snapshot after:
`1e7b42692ef7ee35dc91764c58a0ecf73e02d3fe`; **actual lane tip at closure:
`fdaaaf36f1d08dcb209fd45f8c1130009076f909`** (the prompt snapshot is stale; see §1).
Driver digest (copied from mutable `.ufo/watchdog.log`):
`2026-11-07T13:47:48-03:00 launch kasegi round=95 pgid=2566176 driver=hyaku-inline attempt=1`;
`2026-11-07T14:45:36-03:00 complete kasegi round=95; hyaku-inline attempt=1`.

Method: the lane's `knowledge-meter.py` and `capability-check.py` are lane-owned counters/gates.
Per PROTOCOL §Gate standard (Closure consequence) I verified their **committed evidence** — receipt,
tally, frozen pins, revision printed — and did **not** execute them. Every claim's substance was
additionally re-derived from committed bytes with plain commands I ran myself (`git show`/`diff`,
`grep`, `sha256sum`, and a small independent token census).

## 1. Conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an <%ae> %h %s' -- .ufo/reports/round-95/kasegi.md` (fleet repo) | two commits, both `kasegi-shokunin <kasegi@shokunin.local>`: `dbee3413` (filed report) and `e17da0a9` (erratum) | PASS |
| Report lands after the lane work | committer times | report erratum committer `2026-11-07T14:50:43-03:00`; final lane tip `fdaaaf36` committer `14:50:22-03:00`; the erratum names `fdaaaf36` and every earlier hash it cites | PASS (author date `14:48:21` precedes the tip — the recurring jj change-creation-time artifact, status-neutral) |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` = 1; `grep -c '^- \['` = 4 | four `[~]` lines, each with a resolvable pointer (`corpus/lessons/round-47-verifier-spotcheck.md:94`, the two practice reports, `PROVINCE.md`); both practice reports and `PROVINCE.md` exist | PASS |
| Cited commits exist and are ancestors of the branch ref | `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> refs/heads/master` for `9ef0126c`, `347519f2`, `53ec479d`, `38e7319f`, `d050e286`, `43cc15e8`, `01ff9865`, `f6b94519`, `1e7b4269`, `4ee3455d`, `88bc4127`, `fdaaaf36` | all twelve exist; all twelve print `ancestor=yes` | PASS |
| No uncommitted round work; pushed | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=fdaaaf36 remote=fdaaaf36 ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `fdaaaf36` | PASS |
| Prompt carries the template contract | dispatched `.ufo/prompts/kasegi-round-95.md` | sections 1–5 verbatim plus the hyaku §6 addendum; all five child-lane items (report path/filename, commit-then-report ordering, `SHONEN` heading, commit-hash citation, lane write scope); L2 floor “at least 8” matches `MISSION.md`; no route map is quoted, so no map can drift | PASS |
| Real report vs marker | report sections in order | Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN, round shape; evidence pointers, hashes and measurements present | PASS (not a marker) |
| Wave shape | `.ufo/waves/round-95/w1-spec.json`, `w1-results.json` | 13 items / 13 results; agents: 3 critics, 2 reviewers, 2 mutation-testers, 1 sentinel (**8/13 attack**), 2 executors, 1 scout, 1 connector, 1 scribe; zero dead seats | PASS |
| Source census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `kasegi ok` rc 0; 143 rows, malformed 0, duplicate ids none; the six inherited W04 warnings (S028, S029, S072, S076, S080, S085) plus the S143/S141 supersession duplicate | PASS |
| Late fix commits tied to a LOG entry | `grep -n '4ee3455\|88bc412\|fdaaaf36\|docfix' LOG.md` | no hit; the report erratum names the commits but the “Landed changes” table has no LOG entry for them | **DEFECT** (routed, status-neutral) |
| Erratum point 3 has a committed receipt | `grep -rn 'MANIFEST round-95 records=1\|missing_manifest=0' .` | no committed round-95 hit; the manifest itself exists and binds S142 (`sha256 727ba6a0…` = the snapshot, URL and line-169 quote present), but the claimed `capture-binding-check.py` output is not on disk | **DEFECT** (routed, status-neutral) |
| Snapshot-hash drift | prompt says after `1e7b426`; lane state says `fdaaaf36` | `4ee3455` (docstring fix + S142 manifest), `88bc412` (allowlist hygiene), `fdaaaf36` (docfix receipt) landed after the prompt snapshot and are pushed; the committed erratum names `fdaaaf36`; `1e7b426` remains an ancestor | status-neutral; noted for the operator digest |

The report is a real report. Conformance defects above are status-neutral; none prescribes `failed`.

## 2. Per-claim re-check

### C1 — `depth:verifiability` (lowest non-retired axis; score 4 held) → **VERIFIED; axis improved**

Re-measured by me (plain, over committed bytes):

- `git diff --stat 9ef0126c 1e7b4269 -- corpus/knowledge/triage-thresholds.md corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md`
  → **14 insertions / 14 deletions** (14 changed lines), the exact line count the wave's ExecC1Indep reported.
- A Python pass over `.ufo/waves/round-95/c1/repair-map.tsv` and `git show` of the base and after files:
  **16 map rows** (11 `triage-thresholds.md`, 5 `iso-29147-divergence-and-clause-crosswalk.md`); every
  `old` occurs exactly once in its base file, every `new` occurs in the after file, no `old` remains;
  applying all 16 replacements in order to the base reproduces the after bytes **exactly** for both
  files (`apply_equal True`). Map sha256 `8545eba2c39a1fed66b5d6eba59de973c182208aa8b06d28013417821359beb6`
  = the frozen pin; labels 16 rows (4 `cell-repair`, 5 `part-repair`, 7 `range`) sha256
  `cf73949702a569385e0c68390177f454f050f101659edc5ad89410973f0379d0` = the frozen pin; meter sha256
  `c0799f4c52441671b722ccdaa51b579a71c1e3f3c51074d062c7952606878db8` at both the freeze and the tip.
- `git diff-tree --no-commit-id --name-only -r 53ec479d` → exactly the two knowledge files (P3).
- Independent citation census I wrote (backticked path-like tokens over `corpus/knowledge/*.md`, the
  documented extraction rule, no lane code imported): base **1998 unique tokens**, after **1994**;
  my simple resolver counts 991 / 992 non-GONE. The report's numerator is 1007 / 1008; the 16-token
  absolute gap is my resolver's missing mirror/brace/glob credits (the meter's HOST line records 127
  absolute tokens, 23 non-GONE; my literal check counts 22). **The denominator change 1998 → 1994 and
  the numerator delta +1 match exactly.**
- The five bare `S041.txt` citations named in the map (`iso-29147…` lines 13/34/43/54/64) now carry
  `corpus/source-snapshots/round-30/S041.txt`; the target path exists. A sixth bare
  `S041.txt:1680-1681` survives at line 13 (CriticHarm D2) — disclosed and routed, outside the five
  the claim named.

Evidence-verified (gate not executed):

- `.ufo/waves/round-95/l1/landing-r95.txt` at `after_rev=53ec479d…`: `KNOWLEDGE-METER base=1007/1998
  after=1008/1994`, M3/M4/M5/M9/M10 pass (`labelled=16 want=16 mapped=16 kinds=cell-repair=4,part=5,range=7`),
  `KNOWLEDGE-METER-RESULT pass rc=0`.
- `.ufo/waves/round-95/l1/c1-controls-postlanding-r95.txt`: `C1-CONTROLS-RESULT pass controls=15`
  (candidate PASS, do-nothing rc 1, the eleven negative controls rc 1, `missing-labels` rc 2,
  `union-applied` PASS against the round-93 counter's rc 1 + Traceback). The receipt's `candidate=` /
  `after_rev=` is **`38e7319f`**, not the C1 landing `53ec479d`; the knowledge files are byte-identical
  between the two revisions (checked), so the 15/15 result stands, but the receipt's revision label is
  imprecise (routed).

Harm check: `git diff --stat 9ef0126c <tip> -- SKILL.md` empty; `PROVINCE.md` empty; `git diff` over
`SCORECARD.md` changes only the `capture-secret-scan` capability row and appended round text — no axis
row moved; the C1 landing touches only the two knowledge files. Two edits are **PARTIAL** on anchor
precision (`triage-thresholds.md:88` first part and `:90` cite `SKILL.md:182-184` for a correction that
completes on line 185); ReviewC1Sites measured 14/16 CORRECT / 2 PARTIAL / 0 WRONG and wrote round-96
labels. Disclosed, routed, not a predicate failure.

**C1 verdict: VERIFIED on its frozen P1–P3; `depth:verifiability` improved, score 4 held.**

### C2 — `coverage` (score 8 held; capability extension `capture-secret-scan`) → **VERIFIED; axis improved**

Re-measured by me (plain):

- Selftest case count by source rows (`git show <rev>:corpus/instruments/capture-secret-scan.py | grep -cE '^        \("'`):
  base `9ef0126c` 90 case rows + 8 path checks + 3 allow checks = **101**; after `38e7319f` 104 + 11 = **115**.
  The 14 new rows are 5 `github-refresh-token` and 9 `gitlab-jwt-token` cases (positives, 75/77/36
  negatives, escape boundary, three prefixes, custom prefix, non-`eyJ`, short head, 19-char third
  segment, letter-before, doc placeholder).
- Frozen candidate `.ufo/waves/round-95/c2/candidate-scanner.py` sha256 `66edd66143ec62f6e40c864817a97383916d7ff67e5ab384e130b65c44516707`;
  the landed `corpus/instruments/capture-secret-scan.py` at `38e7319f` and `1e7b4269` is the same
  `66edd661…` (P2). `corpus/instruments/claim-package-check.py` at `38e7319f` is
  `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` = the claim's gate pin.
- `git diff-tree --no-commit-id --name-only -r 38e7319f` → exactly `SCORECARD.md`,
  `corpus/instruments/capture-secret-allow.tsv`, `corpus/instruments/capture-secret-scan.py` (P3).
- `.ufo/waves/round-95/c2/candidate-row.txt` is present byte-equal as a line in `SCORECARD.md` at
  `38e7319f`; `.ufo/waves/round-95/c2/candidate-allow-row.txt` is present byte-equal in
  `capture-secret-allow.tsv`. The allow row's digest `c7ad99a1…060d` is the sha256 of the 80-byte
  `ghr_` placeholder; my plain `ghr_[0-9a-zA-Z]{76}` scan finds two identical 80-byte occurrences in
  `.ufo/waves/round-94/w1/ScoutGitLabRules-receipts/06-github-firstparty-examples.txt`; the old
  36-character matcher with a right boundary does not fire on them.
- The landed scanner at `38e7319f` carries `_GH_REFRESH = rb"ghr_[A-Za-z0-9]{76}(?![A-Za-z0-9_])"`
  and `_GJ_HEAD = _GL_LB + rb"(?:" + _GL_PREFIX + rb"(?:glcbt|glsat)|gliamat)-eyJ" + _GJ_SEG`
  (`github-refresh-token` at line 196, `gitlab-jwt-token` at 207).

Evidence-verified (gate not executed):

- `.ufo/waves/round-95/l1/landing-r95.txt` at `rev=38e7319f` seed 9191: `K1 ok … selftest=pass cases=115`,
  `K2 ok scanned=2477 hits=0 allowed=26 unused_allow=0`, `K3 ok rc=1 hits=6 missing=none extra=none`,
  `K4 ok base_new_shape_hits=0 old_shapes_missing=none`, `K5 ok rows=1 last=87`, `K6 ok`,
  `CAPABILITY-CHECK-RESULT pass rc=0`.
- `.ufo/waves/round-95/controls/c2-controls-r95.txt`: the round-94 instrument at the base fails K1
  (`cases=101`), K3 (`hits=0` for the six plants) and K5; the candidate passes K1–K6 at seed 4242.

Post-landing changes: `4ee3455` changes only the scanner docstring (+25/−2 lines; no logic line) and
adds `corpus/source-snapshots/round-95/manifest.json`; `88bc412` adds one digest-bound allowlist row
for a seat receipt that quotes the S139 allowlist row (the scanner's `bearer` shape matches the shape
cell + digest, not a credential); `fdaaaf36` adds the committed receipt
`.ufo/waves/round-95/l1/docfix-r95.txt` — `CAPABILITY-CHECK-REV rev=88bc4127 seed=777`, K1–K6 ok,
`cases=115`, `scanned=2744 hits=0 allowed=27 unused_allow=0`, pass rc=0. The C2 claim's P2 remains
measured at the C2 landing `38e7319f`; the doc fix is behaviour-neutral, as the receipt shows.

Harm check: the C2 landing touches only the scanner, allowlist and SCORECARD row; the scanner still
passes its selftest and K1–K6 at the tip (receipt); no earlier shape is removed (K4); the only later
allowlist row is a hygiene admission for the round's own seat receipt. No axis harmed.

**C2 verdict: VERIFIED on its frozen P1–P3; `coverage` improved, score 8 held.**

## 3. Spot-check table (LEARNING.md §Discernment is checked from outside)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S142 — GitHub Docs, Refreshing user access tokens (admits `docs`, tier A, `mined`) | admit | Live URL re-opened (HTTP 200, markdown); committed capture `corpus/source-snapshots/round-95/S142.txt:169` re-read | AGREE | The page's response-parameter table says “The token starts with `ghr_`” in the `refresh_token` row; the quote is 5 words at line 169. The row claims only the prefix, and explicitly says the page gives no length; tier A is right for GitHub's own statement. |
| S143 — GitLab `rules/mit/github/github.toml` at commit `59ada1f4` (admits `code`, tier B, `mined`; correction row superseding S141) | admit | Live GitLab API raw URL at `59ada1f4` re-opened; line 72 is `regex = "ghr_[0-9a-zA-Z]{76}"`; committed receipt `.../08-github-rules-file.txt:16` agrees | AGREE | The 76-character length is exactly what the file says; tier B is correct because this is GitLab's third-party copy of GitHub's shapes, not GitHub's own statement. The `supersedes S141 —` opening is the CORPUS rule-2 correction form; the used-by paths exist. |
| S141 — the same GitLab repository's `github.toml` (rejects; kept `rejected`) | reject | Same live GitLab API raw at line 72; `corpus/SOURCES.md:153` row re-read | AGREE (with a wording note) | At round 94 no admitted entry cited the row; its `teaches` cell already carries the rejection record and CORPUS rule 2 forbids rewriting it. Leaving it `rejected` and landing S143 as the correction row is the contract path. Minor: the flip says “cites this row”, but the round cited S143, so that exact flip can never fire — clarify in a new row/lesson next round, do not rewrite this one. |
| S142 / S143 `corpus/SOURCES.md` rows (new rows) | admit (rows) | `corpus/SOURCES.md` rows 154–155; S142 quote `S142.txt:169` (5 words), S143 quote line 72 (one code line); census rc 0; both used-by paths exist | AGREE | Rows were written after the sources were opened; anchors, tiers, status and used-by are coherent; the lesson’s quotes are ≤25 words and located. Census is `kasegi ok` rc 0 (six inherited W04 plus the S141/S143 duplicate-URL warning, by design). |

## 4. Trend verdicts (closure side)

- **expansion: improved** — registry 141 → 143 counted by me (base 141, tip 143; tier A 128 → 129,
  B 7 → 8, C 6 → 6; mined 116 → 118); both new rows are opened, scoped and `mined`, the knowledge
  entry `github-refresh-tokens-and-gitlab-jwt-tokens.md` is admitted with S142/S143/S140 as sources,
  and the `capture-secret-scan` capability row gains two provider classes (first-working round stays
  87). Basis is registry + capability extension, the same form accepted at rounds 92/93, **not** a new
  frontier row; the report states that honestly instead of claiming the entry-admission form.
- **quality: improved** — the eleven deferred rows close as 16 byte-exact edits over 14 lines (my
  independent map application reproduces both files exactly); five bare `S041.txt` citations become
  committed paths; the independent census matches the meter's denominator 1998 → 1994 and numerator
  delta +1; QUALITY R148/R149 enter from the two mined process mistakes; no admitted entry failed its
  re-check. Qualifiers routed: two PARTIAL anchor ranges (triage 88 first part, 90), the R148/R149
  lesson-pointer swap (§6), the manifest landing after the capture (R105 miss, repaired after filing),
  and the missing capture-binding receipt (§6).
- **discernment: improved** — this outside spot-check agrees with the gate on the sampled S142 admit
  and S141 reject; the wave's independent seats found the two C1 PARTIALs, the stale scanner docstring,
  and two gate survivors that self-attestation missed; the lane accepted the findings, fixed the
  docstring, committed the post-fix receipt, and routed the rest. The two residual process defects
  (LOG tie, binding-check receipt) are named here, not left unlearned.

## 5. Per-axis verdicts (closure)

| Axis | Verdict | Evidence |
|---|---|---|
| depth:verifiability | **improved** | C1 verified on P1–P3; 16 edits on 14 lines byte-exact, meter 1007/1998 → 1008/1994, controls 15/15; score 4 held. |
| coverage | **improved** | C2 verified on P1–P3; `github-refresh-token` + `gitlab-jwt-token`, selftest 101 → 115, K1–K6 pass; capability row extended; score 8 held. |
| depth:density | unchanged | `SKILL.md` blob identical base↔tip (`git diff --stat … -- SKILL.md` empty), so density 273.2 is unchanged; no density claim. |

The other four axes are owned by their lanes (SCORECARD header); this round reports no adjacency
evidence and moves none of them.

## 6. Routed defects the lane must fix next round (status-neutral)

1. **LOG tie for the late commits (low).** `4ee3455` (docstring + S142 manifest), `88bc412`
   (allowlist hygiene) and `fdaaaf36` (docfix receipt) are named in the committed report erratum but
   have no `LOG.md` entry and no row in the report's “Landed changes” table. Append a LOG entry next
   round; never rewrite this round's entries.
2. **C1 post-landing control receipt revision label (low/medium).** `c1-controls-postlanding-r95.txt`
   prints `candidate=38e7319f` and `after_rev=38e7319f`, not the C1 landing `53ec479d` named in the
   C1 measurement. The knowledge files are byte-identical at the two revisions, so 15/15 stands;
   re-run at `53ec479d` or label the receipt “after the C2 landing” next round.
3. **QUALITY R148/R149 lesson pointers are swapped (medium).** R148 (a frozen `controls` field is a
   verbatim copy of the executed receipt) cites M95-1, whose lesson row is the **reproducibility**
   mistake; R149 (a control fixture clones a pinned revision) cites M95-2, whose lesson row is the
   **frozen-control** mistake. The criteria are right; correct the grounds in a new row/lesson next
   round, do not rewrite R148/R149.
4. **Lesson `## Gate` omits the new rows' URLs (low).** CORPUS SOURCES contract v1 requires every new
   row's Gate entry to carry the URL, the access date and a ≤25-word located quote. The round-95 Gate
   carries the titles, dates and quotes but no URL for S142 or S143. Add them in the next lesson.
5. **Erratum point 3 has no committed receipt (medium).** The manifest exists and binds S142
   (`sha256 727ba6a0…`, URL, line 169), but the claimed `capture-binding-check.py` output
   (`MANIFEST round-95 records=1 … missing_manifest=0`) has no committed path. Commit the green run
   or drop the command claim; the manifest itself is verified.
6. **Frozen C2 statement citations (low; disclosed).** The frozen statement cites `S141 line 72` and
   `S140 lines 429/446/463` for the grammar; the landed citation is S143, and the grammars are on
   430/447/464. The committed erratum names this and defers the correction to round 96; never reword
   the filed claim retroactively.
7. **Two C1 PARTIAL anchors (medium; disclosed).** `triage-thresholds.md:88` (first part) and `:90`
   cite `SKILL.md:182-184` for a correction that completes on 185. Round-96 labels are written; land
   them next round.
8. **MutC2Counter F6 survivor (low; disclosed).** The fixture-literal forger survives when
   `--instrument-sha256` is absent; the gate authenticates bytes, not correctness. Route per the
   lesson.
9. **Manifest landed after its capture (low; repaired).** `corpus/source-snapshots/round-95/S142.txt`
   landed at the freeze without `manifest.json`, violating QUALITY R105; the manifest was added at
   `4ee3455` after ScoutSources R1 found it. The repair is real; record the R105 miss in the next
   quality review.
10. **Inherited debt (low).** The six W04 duplicate-URL warnings (S028, S029, S072, S076, S080, S085)
    and the `capture-binding-check` `rejected-row-anchor S138` FAIL predate this round (present at the
    base `9ef0126`); carried, not new.

## 7. Notes for the operator

- All four `SHONEN.md` boxes carry `[~]` with resolvable pointers; boxes 1, 3 and 4 look fully
  checkable by a non-author on the current repo state, and box 2's two practice reports exist and are
  logged. Promotion is operator-owned; no `[x]` was written here.
- Late erratum work: the report's two commits are by `kasegi-shokunin`; the erratum's committer time
  (14:50:43) is after the final lane tip `fdaaaf36` (14:50:22), so the report lands last by the
  ordering that matters. The prompt's snapshot hash `1e7b426` is stale but an ancestor; the committed
  erratum names the final tip. The lane worktree is clean and `ahead=0`; `ls-remote` is
  `fdaaaf36`.
- No promotions, mints, or new L0 questions; assimilation remains `none` (the staged `merge/kasegi/`
  ids collide with the registry, as the report states).

**Closure verdict: kasegi round 95 ADMITTED** — both claims verified on their frozen predicates, no
axis harmed, conformance and quality defects routed and status-neutral.
