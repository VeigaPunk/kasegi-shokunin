author: hyaku closure (non-author integrator, @m_zfl)

# Round 98 — verifier spot-check (non-author closure judge)

Lane: kasegi. Report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-98/kasegi.md`.
Lane HEAD before the round: `2133f5bd993aaf34efad795d5e0b588485401fb2`; after:
`d00c9ecc83b08bb488548e72c1a2792a03743041` (branch `refs/heads/master`, remote equal).
Driver digest (copied from mutable `.ufo/watchdog.log`):
`2026-11-07T17:17:59-03:00 launch kasegi round=98 pgid=245383 driver=hyaku-inline attempt=1`;
`2026-11-07T18:52:33-03:00 complete kasegi round=98; hyaku-inline attempt=1`.

Method: the lane's `census-at-rev.py`, `c1-controls-r98.py`, `capability-check.py` and the
`capture-secret-scan.py` selftest are lane-owned counters/gates. Per PROTOCOL §Gate standard
(Closure consequence) I verified their **committed evidence** — receipts, limb tallies, frozen
pins, revision printed — and did **not** execute them. Every claim's substance was additionally
re-derived over committed bytes with plain commands I ran myself (`git show`/`diff`/`cat-file`,
`grep`/`awk`/`wc`, `sha256sum`, `curl`, and static Python parsing of the instrument's selftest
tables). The one lane instrument I did execute is the read-only `capture-secret-scan.py --files`
probe over the 17 redacted wave-evidence files (a plain measurement, not the gate). No seat was
dispatched; this file is the non-author record.

## 1. Conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an <%ae> %H %s' -- .ufo/reports/round-98/kasegi.md` (fleet repo) | `kasegi-shokunin <kasegi@shokunin.local> da5eb7ecf824060736777f4e4c6d99761d693f45` | PASS |
| Report lands after the lane work | committer times | lane tip `d00c9ecc` committer `18:51:19`; report `da5eb7ec` committer `18:51:58`; driver complete `18:52:33` | PASS (report author date `18:51:00` precedes the tip — the recurring jj change-creation-time artifact, status-neutral) |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` = 1; `grep -c '^- \['` in `SHONEN.md` = 4; report `^- \`\[` = 4 | four `[~]` lines with resolvable pointers (`corpus/lessons/round-47-verifier-spotcheck.md:94`, `corpus/practice/curl-h1-1913733/report.md`, `corpus/practice/curl-ibb-h1-1997312/report.md`, `PROVINCE.md`); all four paths exist | PASS |
| Cited commits exist and are ancestors of the branch ref | `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> refs/heads/master` for `12bb2f98`, `e2caf4a1`, `e2d3de7b`, `27907746`, `d00c9ecc` | all five exist; all five `ancestor`; `git -C kasegi-shokunin` HEAD = `d00c9ecc` | PASS |
| No uncommitted round work; pushed | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=d00c9ecc remote=d00c9ecc ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `d00c9ecc` | PASS |
| Prompt carries the template contract | `.ufo/prompts/kasegi-round-98.md` vs `templates/round-prompt.md` | the prompt prefix (8,379 bytes / 140 lines) is byte-identical to the rendered template (LANE=kasegi, ROUND=98, AXES="depth + coverage (bounty and security research)", FLEET_ROOT=/home/vgpnk/Projects/shokunin, lane cwd `/home/vgpnk/Projects/shokunin/kasegi-shokunin`); five child-lane items present (report path/filename, commit-then-report ordering, `SHONEN` heading, commit-hash citation, lane write scope); L2 floor "at least 8"; the hyaku §6 addendum follows | PASS (route-map observation below) |
| Real report vs marker | report sections in order | Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN, Round shape, Wave findings, Stale-lane, Tool installs, Open L0 questions; hashes and measurements present | PASS (not a marker) |
| Wave shape | `.ufo/waves/round-98/w1-spec.json`, `w1-dispatch.json`, `w1-results.json` | 13 items / 13 results, 0 empty outputs; roles 3 critic, 2 reviewer, 2 mutation-tester, 1 sentinel, 2 executor, 1 scout, 1 connector, 1 scribe; `counts.spawn=13`; band 8–16; attack 8/13 = 62 %; no `model` key in spec or dispatch | PASS (no planner seat: the L1 holds it per the fleet-wide 2026-10-19 ruling and the round-97 precedent; disclosed in the report) |
| Source census | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `kasegi ok` rc 0; 149 rows; the seven inherited W04 duplicate-URL warnings (S028, S029, S072, S076, S080, S085, S143) | PASS |
| Registry delta | `git show 2133f5bd:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`; same at the tip | 147 → 149; malformed rows 0; duplicate ids 0; every `mined` used-by path exists | PASS |
| LOG ties | `grep -c <hash> LOG.md` per round commit | `12bb2f98` 1, `e2caf4a1` 3, `e2d3de7b` 2, `27907746` 0, `d00c9ecc` 0 | PASS with observation: the integration and wave-evidence commits are described by the LOG's Round 98 bullets and carried by the report's Landed-changes table (the round-97 precedent); their hashes are not in `LOG.md` |
| Report bullet pointers | report Landed-changes "LOG entry" column vs the LOG's Round 98 bullets | the LOG entry has 9 bullets (Base/freeze, Freeze, C2 landing, C1 landing, Sources, Integration, Mistakes, Wave w1, Wave corrections); the report cites "bullet 1/2/3/4–5/5" for Freeze/C2/C1/Integration/Wave evidence | **DEFECT** (low; the pointers do not resolve as written; routed) |
| Evidence-pointer precision | report Sources & frontier vs `corpus/lessons/round-98.md` `## Gate` | the report says "the Gate block records URL, access date and a ≤25-word located quote for each" of S148/S149; the Gate block has **no S148/S149 record** (only S140, S144 and the S144-IAM reject; `grep -n 'S148\|S149' corpus/lessons/round-98.md` = one line, in Wave findings) | **DEFECT** (medium; routed) |
| Count consistency | `grep -n '147 → 147\|S140's own\|superset' SCORECARD.md corpus/lessons/round-98.md` | SCORECARD round-98 `Sources: registry 147 → 147 (no new row)` and lesson Gate `Registry 147 → 147 rows` contradict the actual 147 → 149; the SCORECARD C2 row and the lesson Learning section still say `S140's ... class` against the erratum's superset; the lesson Gate's S140 used-by old→new records two added paths against four actually added | **DEFECT** (medium; correction sweep incomplete; routed) |
| Wave-evidence redaction | `.ufo/waves/round-98/l1/redaction-r98-w1.txt`; my re-scan of the 17 files | `files=17 values=1257`; `python3 -B corpus/instruments/capture-secret-scan.py --files <the 17>` prints `CAPTURE-SECRET-SCAN mode=files scanned=17 hits=0 files=0 allowed=0 unused_allow=25 rc=0` | PASS (the clean re-scan is reproducible; it is not committed as a receipt — low, routed) |

The report is a real report. Conformance defects above are status-neutral; none prescribes `failed`.

## 2. Per-claim re-check

### C1 — `depth:verifiability` (lowest non-retired axis; score 4 held) → **NOT VERIFIED (P1/P2 fail; P3 stands); axis unchanged**

Re-measured by me (plain, over committed bytes):

- **P3 stands.** `git show d00c9ecc:corpus/instruments/citation-survival.md | grep -c 'tree-e2caf4a1561b'` prints `0`;
  `grep -c '/fast/scratch'` prints `0`; `grep -c '^Lane root:'` prints `1`; the header line is
  `measured-at: e2caf4a1561b544a6ea684b0bcfa975f7e7f6061`; `git merge-base --is-ancestor
  e2caf4a1 refs/heads/master` holds. The committed `p3-r98.txt` receipt prints the same.
- **P1 does not stand.** The claim's central label is `pinned rate (INTERNAL only;
  revision-stable)`. It is not revision-stable: two citations in the measured scope use `../`
  walk-outs — `corpus/knowledge/source-tree-loss-2026-09-28.md:315` cites
  `` `../MISSION.md:49-56` `` and `corpus/lessons/round-20-recensus.md:4` cites
  `` `../.ufo/waves/shokunin12h-20261014-p1-repair/members/Kasegi*.md` `` — and
  `census-at-rev.py` extracts to `<work>/tree-<rev12>`, so `../` escapes the extract into the
  verifier's work dir. `CriticClaimsC1` proves the flip with its own fixture (`04-layout-instability.txt`:
  same rev `6486f8f5`, layout A 0/3 vs layout B 1/3) and on the landed file (`05-real-file-layout.txt`:
  `CENSUS-CHECK pass ... lane=2589/7961` against the clean cache, `pinned-mismatch` with
  `lane=2591/7961` against a work dir carrying `MISSION.md` and `.ufo/.../KasegiGateRepair.md`).
  The exact frozen command also failed `CENSUS-CHECK fail reason=resolve-rc-15 rc=2` on three
  attempts in the wave (earlyoom SIGTERM on the 1.8–3.5 GiB `resolve.py` child; journal-attributed).
- **P2 does not stand.** The post-landing re-run printed `C1-CONTROLS-RESULT error reason=write rc=2`
  / `CENSUS-WRITE error reason=resolve-rc-15 rc=2` under the same memory pressure, so the eight
  controls were not observed in the critic's re-run; the author's postfix receipt
  (`controls/c1-controls-r98-postfix.txt`) shows the 8/8 pass, but the frozen `harness_sha256`
  `d39a1fc8…` matches **no committed harness**: freeze `12bb2f98` blob `0488d796…`, landing
  `e2d3de7b` blob `d9713268…`, and `grep -rn d39a1fc8` resolves only to `claims.json:16`.
- **Numbers are not gamed.** My arithmetic over the committed census: RESOLVES 78 + MIRROR 0 +
  INTERNAL 2589 + GONE 5294 = 7961; pinned SKILL 162/732 = 22.13 %, corpus 2551/7559 = 33.75 %,
  lane 2589/7961 = 32.52 %; host-inclusive 166/732, 2629/7559, 2667/7961; host-owned 78. The
  before side is the base file's `132/701 = 18.83 %`, `1202/4766`, `1227/5152`, scope 224 files.
  The failure is the label and the check's layout dependence, not the arithmetic.
- **Check coverage is weak.** `CriticClaimsC1` §4 shows body hand-edits, host-line tampering, a
  `measured-at` re-point and a poisoned cache all pass; `MutC1Counter` kills 5 of 12 mutants.

Axis verdict: **depth:verifiability unchanged** (score 4 held; the named-revision substance
landed — P3 — but the central predicate fails and the "revision-stable" label is false; the
score is not claimed to move).

### C2 — `coverage` (score 8 held), capability extension `capture-secret-scan` → **VERIFIED; axis improved**

Re-measured by me (plain, over committed bytes):

- **Selftest tally.** Static count of the committed instrument's selftest tables:
  base `2133f5bd` 137 cases + 8 paths + 3 checks = **148**; landing `e2caf4a1` 159 + 8 + 3 =
  **170** (`grep -c '^        ("'` plus the fixed `paths`/`checks` lists; the selftest prints
  `len(cases) + len(paths) + len(checks)`).
- **Four shapes.** `git show 2133f5bd:corpus/instruments/capture-secret-scan.py | grep -c
  <shape>` prints 0 for `gitlab-ci-build-token`, `gitlab-iam-refresh-token`,
  `gitlab-iam-authorization-code`, `gitlab-session-cookie`; the landing defines all four at
  lines 302–308 with the grammars the claim states (`glcbt-` + 1–5 alnum + `_` + 20;
  `gliamrt-`/`gliamac-` 43 + `.` + 43; the `_gitlab_session` context, optional `cell-<N>-`,
  64 lower-case hex).
- **Five widened boundaries.** Base has 14 occurrences of `(?![A-Za-z0-9_-])`; the landing has
  6 of `(?![A-Za-z0-9])` — the five round-97 shapes (`GR1348941`, `feed_token=`, `gloas-`,
  `glft-`, `glsoat-`) plus the new ci-build shape. The erratum correctly calls this a superset
  of S140's punct/space/EOL class, not the class.
- **SCORECARD row.** `grep -c '^| capture-secret-scan '` = 1; the row names all nine round-98
  shape ids (one occurrence each) and its last cell is `87`.
- **Knowledge entry.** `corpus/knowledge/gitlab-iam-ci-build-and-session-token-shapes.md` opens
  with `source:` citing S140, S144, S148 and S149, `verified-at: 2026-11-07` and a `recheck:`
  command; the S140 quotes at lines 293/480/497/549-550 match the committed capture
  (`corpus/source-snapshots/round-94/S140.txt`, sha256
  `f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`, 563 lines) verbatim.
- **Evidence-verified, not executed:** `.ufo/waves/round-98/l1/c2-landing-r98.txt` prints K1–K7
  `ok` and `CAPABILITY-CHECK-RESULT pass rc=0` at the landing at seeds 20261107 and 4242;
  `controls/c2-gate-candidate-r98.txt` passes at fixture rev `7376b342`; the do-nothing receipt
  fails K1 (`cases=148`), K3 (0 of nine plants), K5 (`named=False`) and K7 (0 of five widened
  payloads). The instrument pin `45f8d226…` equals the landing bytes; the tip's instrument is
  `b7804b7d…` and differs only in docstrings/comments (F1/F2/F4).

Axis verdict: **coverage improved** (score held at 8; the capability row is extended and no
earlier shape is lost — `CriticHarm` counts 35 → 39 patterns, no removal, five strict
widenings, 140/140 base selftest cases still `ok`).

### Guard — `depth:density` → **unchanged**

`git diff --stat 2133f5bd d00c9ecc -- SKILL.md` prints nothing; `SKILL.md`/`PROVINCE.md`/
`SHONEN.md`/`AGENTS.md` are byte-identical base → C1 landing (`CriticHarm` §1 hashes). The
reported 273.2 is the density instrument's unchanged reading; no density credit is claimed.

## 3. Discernment spot-check (non-author)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S140 — GitLab secret-detection rules, `rules/mit/gitlab/gitlab.toml` at 59ada1f4 | **ADMIT** (`docs`, tier A, `mined`; re-opened from the committed capture) | `corpus/source-snapshots/round-94/S140.txt` (sha256 `f3fd09e4…`, 563 lines) and the live `/-/raw/` URL (HTTP **403**, 6,078 bytes, Cloudflare "Just a moment…") | **agree** | the four quotes at capture lines 293/480/497/549-550 are present verbatim (`glcbt-` regex with the punct/space/EOL class; the two IAM 43+`.`+43 regexes; the session-cookie value/context pair); the live fetch is 403/6,078 bytes as recorded, so the capture is the correct citation base. |
| S144 — GitLab Docs, Security — Tokens | **ADMIT** (`docs`, tier A, `mined`; re-opened) | live `https://docs.gitlab.com/security/tokens/` (HTTP **200**, 67,805 bytes, sha256 `765becf3…`) and `corpus/source-snapshots/round-96/S144.txt:356`/`:362` | **agree** | the live page carries `glcbt-` and `_gitlab_session=` (1 occurrence each); the capture lines are `CI/CD Job tokenglcbt-` and `GitLab session cookies_gitlab_session=`; the tier-A scope (prefix table) is correct. |
| S144 as a second source for the two IAM forms | **REJECT** (no new row; flip stated) | the same live page and capture | **agree** | `grep -c 'gliam'` prints 0 on both the capture and the live page; the page states no `gliamrt-`/`gliamac-` prefix, so it cannot ground the IAM shapes; the flip (a docs page naming the prefixes) is correctly stated. |
| S148 — GitLab secret-detection rule prose, session cookie (new row) | **ADMIT (row accurate)** | live `https://gitlab.com/api/v4/projects/gitlab-org%2Fsecurity-products%2Fsecret-detection%2Fsecret-detection-rules/repository/files/rules%2Fmit%2Fgitlab%2Fgitlab_session_cookie.md/raw?ref=59ada1f4…` (HTTP **200**, 1,028 bytes, 23 lines, sha256 `b50856e4…`) | **agree on the row; DEFECT on the Gate record** | line 6 states "The value is a 64-character hexadecimal session ID, with an optional `cell-<ID>-` prefix." (17 words), matching the row's `teaches`; the row's anchor digest matches. The lesson's `## Gate` carries **no** S148 record (URL, access date, ≤25-word quote), and the report's claim that it does is false. |
| S149 — GitLab secret-detection rule prose, IAM refresh/authorization code (new row) | **ADMIT (row accurate)** | live `.../gitlab_iam_refresh_token.md` (HTTP **200**, 1,190 bytes, sha256 `9b37df1e…`) and `.../gitlab_iam_authorization_code.md` (HTTP **200**, 1,322 bytes, sha256 `52348dd6…`) | **agree on the row; same Gate-record defect** | line 5 of each states `gliamrt-` / `gliamac-` and the IAM service's availability qualifier; tier B and the scope (prefixes only, no length/alphabet) are correct. |

## 4. Trend verdicts

- **expansion: improved** — registry 147 → 149 (S148 tier A `mined`, S149 tier B `mined`); the
  new knowledge entry is on ground the coverage map does not hold (`grep -n -i 'gitlab\|credential
  shape' corpus/README.md` prints nothing); the `capture-secret-scan` capability row is extended;
  S140/S144 `used-by` cells completed. Evidence: the row count command above, the census
  `kasegi ok` rc 0, and the S148/S149 live re-opens.
- **quality: improved** — selftest 148 → 170 with four published shapes and five widened
  boundaries; the census of record names its revision (P3 stands) although P1/P2 fail; the
  wave-evidence redaction is real (17 files, 1,257 values; my re-scan prints `hits=0`); R155/R156/
  R157/R158 added. Defects routed: the false "revision-stable" label left in the census artifact,
  and the stale "147 → 147"/"S140's own class" claims left in SCORECARD and the lesson.
- **discernment: improved** — six mistakes mined (M98-1…M98-6); the wave falsified C1 and the
  lane reported it rather than smoothing it over; my spot-check agrees on the S140/S144 admits,
  the S144-IAM reject and the S148/S149 row accuracy; the Gate-record defect (S148/S149 not
  recorded; the report says they are) is routed below.

## 5. Routed defects for round 99

1. **C1 census label (high).** `corpus/instruments/citation-survival.md` still reads `pinned rate
   (INTERNAL only; revision-stable)`; the wave proves the rate flips with the verifier's scratch
   parent. Confine `../` walk-outs per R157 and regenerate, or correct the label to name the
   layout dependence. The exact `--check` command must also be runnable without an earlyoom kill
   (document the memory profile or the receipt's environment).
2. **C1 harness pin (medium).** `claims.json` `harness_sha256` `d39a1fc8…` matches no committed
   harness (freeze `0488d796…`, landing `d9713268…`). Record the pin update in the erratum or add
   a `harness_sha256_postfix` field.
3. **C1 check coverage (medium).** The check verifies only the pinned line; body hand-edits,
   host-line tampering, a `measured-at` re-point and a poisoned cache pass (`CriticClaimsC1` §4).
   Strengthen the check and add controls for the seven surviving mutants.
4. **Gate records for S148/S149 (medium).** Add the URL, access date and ≤25-word located quote
   for each new row to `corpus/lessons/round-98.md` `## Gate`; the report's claim that the Gate
   records them is false.
5. **Correction sweep (medium).** SCORECARD round-98 `Sources: registry 147 → 147 (no new row)`
   and the lesson Gate `Registry 147 → 147 rows` contradict the actual 147 → 149; the SCORECARD
   C2 row and the lesson Learning section still say `S140's ... class` against the erratum's
   superset; the lesson Gate's S140 `used-by` old→new records two added paths against four
   actually added (`github-refresh-tokens-and-gitlab-jwt-tokens.md` and
   `gitlab-routable-and-versioned-token-forms.md` are also new).
6. **LOG bullet pointers (low).** The report's Landed-changes table cites "Round 98 bullet
   1/2/3/4–5/5"; the LOG's Round 98 entry has 9 bullets (Freeze is 2, C2 is 3, C1 is 4,
   Integration is 6, Wave evidence is 8). Fix the pointers.
7. **Clean re-scan receipt (low).** The report's "clean re-scan prints `hits=0`" has no committed
   receipt; my re-scan of the 17 files prints `hits=0 rc=0`. Commit the receipt or cite the
   command.
8. **C1 body host-dependence (low).** The census body's anchor table differs by the
   `.ufo/watchdog.log` line count between hosts; either pin the body or state that the body is
   host-dependent (the header's "not revision-stable" note covers the host-owned count only).
9. **Dispatch text numbers (low).** The dispatch/Goal text quotes the base census numbers
   (2550/7556, 2588/7958) as the regenerated census's; the landed file says 2551/7559,
   2589/7961. Label the pair as the base or fix the sentence.

None of these re-scores a claim: C1 does not verify on its frozen predicate (P1/P2), C2 verifies
on K1–K7, and no owned axis is harmed. The round is a **rejected honest stop**: C1 declared,
falsified by its own wave, reported without smoothing.
