author: hyaku closure (non-author integrator, @m_zfl)

# Round 97 — verifier spot-check (non-author closure judge)

Lane: kasegi. Report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-97/kasegi.md`.
Lane HEAD before the round: `b06af5e07efbd961a8449f7de6b57eeea62c6bd3`; after:
`73f8241ac734a794a6b2854f046dfb77cc82a8fc` (branch `refs/heads/master`, remote equal).
Driver digest (copied from mutable `.ufo/watchdog.log`):
`2026-11-07T16:07:13-03:00 launch kasegi round=97 pgid=446459 driver=hyaku-inline attempt=1`;
`2026-11-07T17:06:50-03:00 complete kasegi round=97; hyaku-inline attempt=1`.

Method: the lane's `knowledge-meter.py`, `capability-check.py`, control harness and the
`capture-secret-scan.py` selftest are lane-owned counters/gates. Per PROTOCOL §Gate standard
(Closure consequence) I verified their **committed evidence** — receipt, limb tally, frozen pins,
revision printed — and did **not** execute them. Every claim's substance was additionally
re-derived over committed bytes with plain commands I ran myself (`git show`/`diff`/`numstat`,
`grep`/`awk`/`wc`, `sha256sum`, `curl`, and static Python parsing of the instrument's selftest
tables). No seat was dispatched; this file is the non-author record.

## 1. Conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an <%ae> \| %ai \| %ci \| %h %s' -- .ufo/reports/round-97/kasegi.md` (fleet repo) | two commits, both `kasegi-shokunin <kasegi@shokunin.local>`: `20045898` (filed report, committer 17:05:40) and `e24b7587` (erratum, committer 17:06:12) | PASS |
| Report lands after the lane work | committer times | lane tip `a7416b18` committer `17:04:56`; report `20045898` committer `17:05:40`; late receipt `73f8241a` committer `17:06:00` named by the erratum `e24b7587` at `17:06:12`; driver complete `17:06:50` | PASS (author date `16:45:03` on the filed report precedes the tip — the recurring jj change-creation-time artifact, status-neutral) |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` = 1; `grep -c '^- \['` = 4; `SHONEN.md` has 4 boxes | four `[~]` lines with resolvable pointers (`corpus/lessons/round-47-verifier-spotcheck.md:94`, `corpus/practice/curl-h1-1913733/report.md`, `corpus/practice/curl-ibb-h1-1997312/report.md`, `PROVINCE.md`); both practice reports exist | PASS |
| Cited commits exist and are ancestors of the branch ref | `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> refs/heads/master` for `b06af5e0`, `daf7fc6a`, `b3c2aff9`, `75a47180`, `a9a53608`, `369758f3`, `b4bb939a`, `a7416b18`, `73f8241a` | all nine exist; all nine `ANCESTOR-of-master OK` | PASS |
| No uncommitted round work; pushed | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=73f8241a remote=73f8241a ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `73f8241a` | PASS |
| Prompt carries the template contract | `.ufo/prompts/kasegi-round-97.md` vs `templates/round-prompt.md` | the prompt prefix (8,285 bytes / 140 lines) is byte-identical to the rendered template (LANE=kasegi, ROUND=97, AXES="depth + coverage (bounty and security research)", FLEET_ROOT=/home/vgpnk/Projects/shokunin); five child-lane items present (report path/filename, commit-then-report ordering, `SHONEN` heading, commit-hash citation, lane write scope); L2 floor "at least 8"; the hyaku §6 addendum follows | PASS (route-map observation below) |
| Real report vs marker | report sections in order | Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN, Round shape, Wave findings, Stale-lane, Tool installs, Open L0 questions, Erratum; hashes and measurements present | PASS (not a marker) |
| Wave shape | `.ufo/waves/round-97/w1-spec.json`, `w1-dispatch.json`, `w1-results.json` | 14 items / 14 results, 0 empty outputs; roles 3 critic, 2 reviewer, 2 mutation-tester, 1 sentinel, 3 executor, 1 scout, 1 connector, 1 scribe; `counts.spawn=14`; band 8–16; attack 7/14 = 50 % (8/14 = 57 % counting sentinel); no `model` key | PASS (no planner seat: the L1 holds it per the fleet-wide 2026-10-19 ruling documented in other prompts and the L0 queue, disclosed in the report) |
| Source census | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `kasegi ok` rc 0; 147 rows; the seven inherited W04 duplicate-URL warnings (S028, S029, S072, S076, S080, S085, S143) | PASS |
| Registry delta | `git show b06af5e0:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`; same at the tip; malformed/dupe/used-by sweeps | 145 → 147; malformed rows 0; duplicate ids 0; every `mined` used-by path exists | PASS |
| LOG ties | `grep -c <hash> LOG.md` per round commit | `daf7fc6a` 1, `b3c2aff9` 1, `75a47180` 2, `a9a53608` 2, `369758f3` 1, `b4bb939a` 1; `a7416b18` 0, `73f8241a` 0 | PASS with observation: the single Round 97 bullet describes both addenda; the report's Landed-changes table carries their hashes |
| Evidence-pointer precision | `ls .ufo/waves/round-97/l1/`; `grep -rn 'seed=20261107' .ufo/waves/round-97/` | the report cites `.ufo/waves/round-97/l1/c2-landing-r97.txt` (landing pass at `a9a53608`, seed 20261107); **that path does not exist**. The landing run is committed at `.ufo/waves/round-97/w1/ExecC2Counter-receipts/gate-seed20261107.txt` (six limbs ok, pass rc=0); the L1 copy stayed in scratch (`/fast/scratch/hyaku/kasegi-r97/l1/c2-landing.txt`, the wave's own ScribeGate F7) | **DEFECT** (routed, status-neutral) |
| Count consistency | `grep -o` over LOG/SCORECARD/lesson/seat | LOG says "six mined mistakes" against 7 rows in `corpus/lessons/round-97.md`; LOG, SCORECARD and the `a7416b18` subject say "6 of the 10 named probes" against MutC1Counter's "7 of the 10" | **DEFECT** (routed, status-neutral) |

The report is a real report. Conformance defects above are status-neutral; none prescribes `failed`.

## 2. Per-claim re-check

### C1 — `depth:verifiability` (lowest non-retired axis; score 4 held) → **VERIFIED; axis improved**

Re-measured by me (plain, over committed bytes):

- Map census over `.ufo/waves/round-97/c1/repair-map.tsv`: **33 rows, 30 distinct
  (file:line) sites, 16 distinct `corpus/knowledge/*.md` files, 9 distinct keys**
  (`resolve.py`, `anchorcheck.py`, `capture-source.py`, `source-recheck.py`, `density.py`,
  `capture-secret-scan.py`, `claim-package-check.py`, `r35-defect-closure.sh`,
  `r36-closure.sh`).
- Application: for each of the 30 sites I read the base line at `b06af5e0` and the landing line
  at `75a47180`; every landing line equals its base line with every occurrence of each mapped
  `old` replaced by `new` (0 mismatches; the three two-row lines are
  `capture-intake-gate.md:11`, `considerthese-proposals-ledger.md:125`,
  `root-loss-2026-10-12.md:54`). `git diff --numstat b06af5e0 75a47180 -- corpus/knowledge`
  prints **16 files, 30 added, 30 deleted**.
- Token census (my own, `corpus/knowledge/*.md`, backticked tokens): the nine bare basenames
  occur **33** times at base (`resolve.py` 5, `anchorcheck.py` 6, `capture-source.py` 5,
  `source-recheck.py` 9, `density.py` 2, `capture-secret-scan.py` 2,
  `claim-package-check.py` 1, `r35-defect-closure.sh` 1, `r36-closure.sh` 2) and **0** times at
  the landing and at the tip; the qualified `corpus/instruments/<name>` occurrences go
  **17 → 50**.
- Delta arithmetic, reproduced from my census: all **9** distinct bare tokens leave the scope;
  **3** qualified tokens are new (`resolve.py`, `source-recheck.py`, `density.py` had zero
  qualified occurrences at base); **6** already existed (`anchorcheck.py`, `capture-source.py`,
  `capture-secret-scan.py`, `claim-package-check.py`, `r35-defect-closure.sh`,
  `r36-closure.sh`). Net denominator −9 + 3 = **−6**, numerator **+3** — exactly the reported
  `1040/2041 → 1043/2035`.
- Every map row's `new` is exactly `` `corpus/instruments/<key>` `` (33/33), so the routed M4
  hole (a wrong-instrument label passes) is latent, not exploited by this landing.
- Evidence-verified, not executed: `.ufo/waves/round-97/l1/c1-landing-r97.txt` prints M0–M10
  pass, `after_rev=75a471809cba…`, `KNOWLEDGE-METER rev=75a47180 rate=1043/2035`;
  `c1-controls-postlanding-r97.txt` prints `C1-CONTROLS-RESULT pass controls=14` and
  `ATTRIBUTION pass fixtures=13`; the `r96-no-qualify-branch` control fails M4/M5/M9/M10; the
  do-nothing control fails M1/M3 with `bad_lines=30`.

Axis verdict: **depth:verifiability improved** (score held at 4). No axis harmed: `SKILL.md`,
`PROVINCE.md`, `SHONEN.md`, `AGENTS.md` are byte-identical base→tip; `anchorcheck` over
`corpus/knowledge` prints 1206 in-range / 8 bad at the tip against 1206 / 8 at the base (the
same 8).

### C2 — `coverage` (score 8 held), capability extension `capture-secret-scan` → **VERIFIED; axis improved**

Re-measured by me (plain, over committed bytes):

- The ten shape ids are absent at `b06af5e0` (`grep` 0 each) and present at `a9a53608` (regex
  table lines 284–303): `gitlab-runner-registration-token`, `gitlab-feed-token`,
  `gitlab-oauth-app-secret`, `gitlab-feed-token-v2`, `gitlab-kubernetes-agent-token`,
  `gitlab-incoming-email-token`, `gitlab-scim-oauth-token`, `gitlab-deploy-token-in-url`,
  `gitlab-feature-flags-client-token`, `gitlab-runner-controller-token`.
- Selftest tally by static parse of the committed instrument: base `cases` 117 + `paths` 8 +
  `checks` 3 = **128**; landing 137 + 8 + 3 = **148** — matching
  `SELFTEST-RESULT pass cases=148` in the candidate receipt and the gate's K1.
- The ten cited S140 lines are byte-identical to the committed capture
  `corpus/source-snapshots/round-94/S140.txt` (sha256
  `f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`, 563 lines): lines
  101/160/174/190/213/229/278/341/392/412 carry `GR1348941`+20, `feed_token=`+20,
  `gloas-`+64, `glft-`+20, `glagent-`+50, `glimt-`+20–25 lower-case, `glsoat-`+20,
  `gitlab+deploy-token-<N>:`+20+`@`, `glffct-`+20, `glrct-`+20.
- The new entry `corpus/knowledge/gitlab-remaining-token-families.md` opens with `source:`
  citing S140 and S146, `verified-at:` 2026-11-07 and a `recheck:` command; it carries the
  ten-row shape table and ten verbatim S140 quotes. The S146 capture
  (`corpus/source-snapshots/round-97/S146.txt`, sha256 `a8e77bd6…`, 238 lines) carries the
  18-word quote at lines 69–70.
- Evidence-verified, not executed: the gate's landing run at `a9a53608` seed 20261107 is
  committed at `.ufo/waves/round-97/w1/ExecC2Counter-receipts/gate-seed20261107.txt`
  (`LIMB K1…K6 ok`, `CAPABILITY-CHECK-RESULT pass rc=0`); the candidate receipt at
  `659e320f` seed 4242 prints the same six limbs; the base instrument at `7ef1d365` prints
  `cases=128` (`CriticClaimsC2-receipts/selftest-base.txt`).
- Redaction: `redaction-r97.txt` prints `REDACTION-RESULT files=43 values=181`;
  `redaction-r97-w1.txt` prints `files=260 values=30`; the allow audit prints
  `rows 25 live 25 dead 0`.

Axis verdict: **coverage improved** (score held at 8). No axis harmed: no earlier shape is
lost (K6 reports `aws-sts-session-token` at the round-86 freeze), the allowlist is
byte-identical, and `SKILL.md`/`PROVINCE.md` are untouched.

## 3. Discernment spot-check (non-author)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S146 — GitLab Docs, Deploy tokens | **ADMIT** (`docs`, tier A, `mined`) | live `https://docs.gitlab.com/user/project/deploy_tokens/` (HTTP 200, 51,391 bytes) and the committed capture `corpus/source-snapshots/round-97/S146.txt:69-70` | **agree** | the quote "The default username format is gitlab+deploy-token-{n}. You can specify a custom username when you create the deploy token." is present verbatim in the live page (18 words), the capture digest matches the manifest, and the page states the username structure only — the tier-A scope (username form) is correct; the secret length stays S140's ground (line 341). |
| S147 — GitLab Docs, Incoming email | **REJECT** (`docs`, tier B, `rejected`) | live `https://docs.gitlab.com/administration/incoming_email/` (HTTP 200, 164,826 bytes) | **agree** | `grep -ci glimt` prints 0 on the live page; the page describes incoming-email configuration but states no token prefix, length or alphabet, so it cannot ground the `glimt-` shape; the flip condition is correctly stated. |
| S146 row quote | new row, ≤25-word quote | `corpus/SOURCES.md:158` and the live page | **agree** | the anchor quote "A deploy token is a pair of values; The default username format is gitlab+deploy-token-{n}" is 14 words and present in the live page; the row is `mined` and both used-by paths exist. Minor: the anchor cell omits the capture line numbers (the lesson's Gate carries lines 69–70; the wave's ScribeGate F6 asked for them in the row). |

## 4. Trend verdicts

- **expansion: improved** — registry 145 → 147; S146 admitted and mined; a new knowledge entry
  (`corpus/knowledge/gitlab-remaining-token-families.md`, knowledge files 105 → 106) on ground
  the coverage map does not hold (no credential-shape row in `corpus/README.md`); the
  `capture-secret-scan` capability row extended; S147 opened and rejected (taste evidence with
  a flip).
- **quality: improved** — ten published shapes with exact-length boundary negatives (selftest
  128 → 148); ten S140 rules quoted verbatim against a digest-pinned capture; the lane's own
  wave evidence repaired (181 + 60 credential-shaped literals redacted, landing `hits=0`,
  allowlist 25/25 live); QUALITY R153/R154 added from seven mined mistakes; no admitted entry
  was found false or stale.
- **discernment: improved** — seven mistakes mined (M97-1..M97-7); the S146 admit and the S147
  reject both re-opened and agreed by this non-author; the wave's non-author seats re-derived
  both claims and routed nine defects, all recorded; no disagreement is left unlearned.

## 5. Routed defects for round 98

1. **C1 counter M4 hole (medium).** M4 does not require `target == "corpus/instruments/" + key`;
   the wrong-instrument fixture (`bfdfae1a`) passes. Add the equality and a
   `qualify-wrong-instrument` fixture. The landing's 33 labels are all same-name, so C1 stands.
2. **C2 right boundary narrower than S140 (medium).** Five shapes reject a real token followed
   by `_` or `-` (SentinelShapes MUST-FIX 1, ReviewC2Scanner F2).
3. **C2 gate forgery survives (high).** K3's plants are not independent of K1's selftest; ten
   literal-locked patterns pass (MutC2Counter F01). Generate plants independently.
4. **Four further S140 rules undetected and unnamed (medium).** `gitlab_ci_build_token`
   (S140:293), `gitlab_iam_refresh_token` (480), `gitlab_iam_authorization_code` (497),
   `gitlab_session_cookie` (549).
5. **S140 capture anchors offset from upstream (medium).** Capture 101 = live 105; capture
   412 = live 433; the manifest's "line numbering preserved" sentence is inaccurate.
6. **`citation-survival.md` still not regenerated (low, carried).** 132/701; needs a
   revision-pinned wrapper.
7. **Claim-text qualifiers (low).** `claims.json` C1.surface says "12 corpus/knowledge files"
   (sixteen); the "-6" parenthetical compresses the arithmetic; the seat spec said P1–P4 while
   the frozen predicate is P1–P3; row 12's "header comment" wording.
8. **Pre-freeze candidate revs are scratch objects (low, carried).** `f410e91f`/`2059fcba` do
   not resolve; the post-landing re-run at `75a4718`/`daf7fc6` is the reproducible half.
9. **Mirror-dependent reproduction (low).** The meter prints `mirror_absent=True`; the
   predicate does not pin it.
10. **Dead landing receipt pointer (low).** The report cites
    `.ufo/waves/round-97/l1/c2-landing-r97.txt`; commit the L1 copy or cite
    `w1/ExecC2Counter-receipts/gate-seed20261107.txt`.
11. **Count discrepancies (low).** LOG says "six mined mistakes" (lesson has seven); LOG,
    SCORECARD and the `a7416b18` subject say "6 of the 10 named probes" (MutC1Counter says
    seven).
12. **`corpus/README.md` coverage map not extended (low, pre-existing since r84).** The new
    entry has no coverage-map row.
13. **GH013 refusal output not committed (low).** The push incident rests on the report/LOG
    narrative plus the redaction receipts; the blocked commits are gone by design.
14. **`ExecC2Probe.md` boundary literals (low).** Nine synthetic short/long/case fixture
    literals remain outside the gate's `is_capture_path` scope; reconcile with M97-7's "every
    file" wording or record the scope decision.
15. **S146 row anchor (low).** Add the capture line numbers (ScribeGate F6) to the anchor cell.

None of these re-scores a claim: C1 verifies on its frozen predicate and C2 on K1–K6; no owned
axis is harmed.
