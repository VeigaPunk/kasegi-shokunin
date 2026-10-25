## Round 25 — 2026-10-25 — recheck lines made executable; vendor disclosure policies admitted as F10

Frozen claims `.ufo/waves/round-25/claims.json` (C1 depth:verifiability **4**, the lowest
non-retired axis; C2 coverage **7**); base `b49948f1`, lane HEAD at this entry `{{LANE_HEAD}}`.
Two claims on distinct axes, each with its own counter.

- **C1 depth:verifiability — every entry's own `recheck:` line, made executable.** Counter
  `python3 corpus/instruments/recheck-audit.py --json .ufo/waves/round-25/c1-after.json`
  (frozen before-receipt `.ufo/waves/round-25/c1-before.json` sha256 `3e3eeb4e…`, instrument
  `d07af435…`): before `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1`;
  after `lines=37 total=37 complete=True pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0
  exit=0`, with `pass_strict=37` on the hardened limb set. Every line on the audited surface now
  passes the frozen limbs (a)–(c); the 35-file surface alone measured `lines=35 pass=35` before C2's
  two entries landed. 29 of the 35 original lines were rewritten — the 23 prose hybrids
  `on-restoration — <CMD> (<NOTE>)` became `cd <lane> && <CMD>  # on-restoration — <NOTE>`, and the 6
  cwd-dependent lines gained the prefix; `git diff --numstat` is `1 1` on each of the 29 files, so no
  text was added or dropped, only the command moved out of prose. The 23 fail-closed lines still fail
  closed, now against the documented absent bases (`exit 2 → 1`) instead of a syntax error.
- **C1 published limits — the surface and the instrument both moved after the freeze.** (i) C2's two
  entries take the audited surface from 35 to 37 files, so the frozen `lines=35` is now `37`; the
  counter's completeness check requires `lines` to equal the file count, and the round-25 manifest
  those two lines name was minted at 05:37 (5 records, 42 quote assertions). (ii) The counter
  instrument was hardened twice after the before-receipt (`d07af435…` frozen → `4475d2e6…` at
  05:34:28 → `1ccee066…` at 05:39), adding a strict superset of limbs (d–g: `cdroot`, `instrument`,
  `artifact`, `own`) whose first revision also gated the exit status and failed two pre-existing
  `~/Projects` base-test lines (`repo-git-state.md`, `root-loss-2026-10-12.md`); the final revision
  reports `strict pass=37/37` and `exit=0`. The frozen (a)–(c) limb definitions are unchanged in form,
  but the before-receipt is bound to `d07af435…` and cannot be re-derived from the current bytes, so
  before and after are two instruments' verdicts on one predicate.
- **C2 coverage — F10 admitted on five captures, entries `0 → 2`.** Counters
  `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` ;
  `grep -lE '^source: S0(3[6-9]|[4-9][0-9])' corpus/knowledge/*.md | wc -l` ;
  `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`. Before: frontier
  **9**, entries **0**, census exit 0. After: frontier **10** (F10, vendor-side disclosure policies as
  corpus objects — the row this round appends) and **2** entries citing rows first registered this
  round — `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` (S036 Cybozu
  脆弱性情報ハンドリングポリシー, S037 Cybozu 報奨金 FAQ, S038 Pepabo 脆弱性報告制度, S039 Hitachi
  HIRT-PUB10008) and `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` (S040 Cisco
  PSIRT, crosswalked against S036/S038/S039). Five captures, all `status=200` at
  `utc=2026-10-25T08:14:2xZ`, sha256 `022ca4f4…`, `b204aa7f…`, `09e077d3…`, `657e7b4c…`, `b7f7b55f…`
  (`.ufo/waves/round-25/capture-log.txt`); a plain browser-UA `curl` returned 403 for S040 while the
  capture instrument's own UA returned 200, and the re-fetch is reproduced independently. Registry
  **35 → 40** rows (S036–S040, all tier A, `status: mined`; mined 23 → 28), appended normalized from
  `assimilation/rows/SOURCES.append.block.md`.
- **Assimilation (§10).** Package `/home/vgpnk/Projects/shukuknow/merge/kasegi`, read-only, 94 staged
  ids S031–S124. Collision check `comm -12` of the two id lists: **5 ids (S031–S035)** are already this
  lane's, so ids follow the document and never arithmetic — staged S055→S036, S056→S037, S057→S038,
  S060→S039, S068→S040 (`assimilation/ids/{reg-ids,staged-ids,collisions}`; the guard is proved on an
  indented fixture in `assimilation/ids/guard-proof.txt`). **Refused:**
  `vendor-cvd-policy-crosswalk-2026-10-23.md` — Q3: its "the two conditions" claim is contradicted by
  its own bytes of record, which carry four expedite bullets (S040 `L301`, `L302`, `L305`, `L308`); the
  lane's own entry states four and carries the re-grounding note. Five further staged entries are not
  adopted this round — `program-severity-ladders-and-reward-scales`,
  `claim-packaging-and-report-quality`, `program-scope-rules-and-asset-boundaries`,
  `iso-29147-and-30111-division-of-labour-2026-10-23`, `vendor-third-party-finding-coordination-2026-10-23`
  — each keyed to package ids the lane's registry assigns to other sources
  (S031/S032/S034/S035/S036/S076/S080) and to `ground:` rows that do not exist (F11/F19/F20). The
  planned reject reason in `claims.json` ("S068 Cisco policy unreachable this round") is falsified by
  the capture log and is not filed.
- **Routed defects D24-1…D24-5 — all five closed.**
  - **D24-1** (the round-24 report cited a commit that was not lane HEAD): this entry and the round
    report cite `{{LANE_HEAD}}`, the HEAD at write time, and name which paths each cited commit carries.
  - **D24-2** (62 / 77 / 76 assertions for one artefact): one measured number — **76** assertions over
    19 records, `sum(len(s['quotes']))` on `corpus/source-snapshots/round-24/manifest.json`, printed
    with its counting command at `corpus/instruments/README.md:178-181`; the same figure replaces the
    two surviving 77s (`SCORECARD.md:510`, `corpus/lessons/round-24.md:77`; list in
    `InstrumentsCounts.md` §d).
  - **D24-3** (the bound-64→8 mutant's 8/8 stated as measured): now measured on the landed bytes —
    mutant `88122e10…` (landed `db5e0767…` with `64`→`8`) scores dispatch **8/8 exit 0** and
    containment **24/24 exit 0** while flipping a 10-alternative citation INTERNAL→GONE, and no lane
    citation exceeds 7 alternatives; the four overstatements are replaced with the 29-word sentence
    (`RevBound8.md` §4–§5).
  - **D24-4** (L4's fail-before described three ways): one reconciling sentence in the round-25
    lesson, receipt as authority — L4's printed `FAIL` is the case verdict, its primary citation passed
    (`INTERNAL`, `path_check` empty) and the case failed only on the added bounty/mirror citation
    (`GONE`, `path_check=missing-path`), so that second citation is L4's fail-before, and the receipt
    labels L4 liveness (`.ufo/waves/round-24/c1-control-baseline.txt:5-6`, `RevL4Reconcile.md` §3).
  - **D24-5** (residual cwd dependence): 36 of the 37 `recheck:` lines now carry
    `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`; the one that does not
    (`root-loss-2026-10-12.md`) is already cwd-independent, testing absent `~/Projects` bases. The
    counter's foreign-cwd limb went `cwd_fail=6 → 0`.
- **Census.** Before: exit 0, rows **35**, malformed 0, tier A=32 B=1 C=2, status mined=23 queued=9
  rejected=3, W04 ×2 (S028, S029 — pre-existing). After: {{CENSUS}} — the five normalized rows
  (S036–S040, tier A, `status: mined`, `opened: 2026-10-25`) are staged at
  `assimilation/rows/SOURCES.append.block.md`, and their mirror validates exit 0 with only those two
  pre-existing W04s.
- **Waves.** {{WAVES}} — wave 1 `kasegi-r25-build` was dispatched as **38** seats under the v1 policy
  (`waveMinLanes 32`, `declaredMaxLanes 44`): reviewer 12, scout 7, executor 5, scribe 5, critic 4,
  mutation-tester 2, connector 1, sentinel 1, simplifier 1 (`wave1-dispatch.json` `counts.spawn`).
- **Tool installs.** None — no seat installed or upgraded a tool this round; the lane ran on the
  `python3` / `bash` / `git` / `curl` already present.
