# ScribeReportDigest — round-28 report evidence skeleton (evidence digest for the L1)

Seat: ScribeReportDigest (scribe, leaf; read-only for production). Lane root
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Lane HEAD `94f387cbee71a532a51ce075f01701a557231e85`.
Claims-freeze base `c9f8b115a098c65356e4b3b6048af45a37ab8395`. Digest written 2026-10-25T17:23Z–17:33Z UTC.
**State stamp for the measured values: 17:30:13Z–17:33Z** at instrument sha256
`95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514` (bracketed stable before and after every
counter run).

**Purpose.** This is not the report. It is the bullet-and-pointer skeleton the L1 assembles into
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-28/kasegi.md`, section by section. Every number is (i) from
`.ufo/waves/round-28/claims.json`, (ii) from a receipt in §8, or (iii) from a read-only command this seat
ran at the stamp printed beside it. §4b carries one **correction** the report must adopt instead of the
frozen disclosure wording.

**Labels.** `[MEASURED]` run by this seat at the stated digest · `[LANDED]` byte on disk in the worktree,
uncommitted (no seat commits; the L1 does) · `[PRE-STATE]` measured on pre-change bytes · `[PENDING]`
absent at the state stamp · `[IN-FLIGHT]` owner rewriting the byte; never cite as a result.

---

## §0 Snapshot at 17:30:38Z

| artifact | state | evidence |
|---|---|---|
| `corpus/instruments/anchorcheck.py` | `[LANDED]` **`95333e29…6f144514`**, stable across 17:30:03 → 17:30:38; `git diff --stat` `278` changed lines; tokens `FAIL_CLASSES`, `BOUNTIES-ABSENT`, `KASEGI_BOUNTIES`, `--selftest` present | my bracketed runs §3.1; `receipts/ExecImplC1.txt` |
| `SKILL.md` | `[LANDED]` +3 lines (1032 → **1035**), gate\|probe row appended at end of table (R6) | `git diff --stat`; `receipts/ScribeSkillGate.txt`, `ExecSkillGateSupport.txt` |
| `corpus/instruments/README.md` | `[LANDED]` +93 lines | `git diff --stat`; `receipts/ExecInstrReadme.txt` |
| `corpus/QUALITY.md` | `[LANDED]` +6 (R14) | `receipts/ScribeR14.txt` |
| `corpus/README.md` | `[LANDED]` +28 → **245** lines; F12 row (line 213), r28 amendment, reconciliation section | `receipts/ScribeReadmeC2.txt`; my `awk` |
| `corpus/SOURCES.md` | `[LANDED]` 42 rows, **79** lines; S042 appended, S041 `used-by` extended | `receipts/ScribeRegistryC2.txt` §3 |
| `corpus/source-snapshots/round-28/S041.txt` | `[LANDED]` `e18acbf9…2f5ab47`, 147,267 B / 2354 lines; `cmp` vs round-26 capture **exit 0** (`IDENTICAL`) | `receipts/ExecCaptureS041.txt`, `ExecManifest.txt` |
| `corpus/source-snapshots/round-28/S042.txt` | `[LANDED]` `b432ec16…0b9c96966`, 60,508 B / 974 lines, `status=200`, `fetched_bytes=229982` | `receipts/ExecCaptureS042.txt`; my `sha256sum` |
| `corpus/source-snapshots/round-28/manifest.json` | `[LANDED]` `e62ddad1…f291d`, 5038 B; 12 assertions, each `occurrences=1`, `stem==id`, sha pinned | `receipts/ExecManifest.txt` |
| `corpus/knowledge/japanese-domestic-disclosure-workflow.md` | `[LANDED]` `a22d2321…13a6`, 103 lines; both `source:` headers, `verified-at: 2026-10-25`, one `recheck:` line (parses under `bash -n`) | my reads §3.2 / §4 |
| `.ufo/waves/round-28/c1-receipt-index.txt` | `[PENDING]` absent — **the only missing element of the frozen C1 after-value** | my `ls` 17:29:56Z |
| `corpus/instruments/knowledge-expected.txt` | `[PENDING]` still 41 lines → `recheck-audit.py` exit 1 (`expected=39 … unexpected=1`) | my run 17:30:13Z |
| `corpus/lessons/round-28.md` | `[PENDING]` absent | `git status` |
| `LOG.md` / `SCORECARD.md` | `[LANDED]` +49 / +76 lines, claim cells written as `pending` | `receipts/ScribeLog.txt`, `ScribeScorecard.txt` |
| census | `[MEASURED]` **exit 0**, `rows 42` (A 39 / B 1 / C 2; mined 30, queued 9, rejected 3), only the two pre-existing W04 (S028/S029) | my run 17:28:13Z, after the entry landed |
| `frontier-recheck-count.py` | `[MEASURED]` **`entries=15 pass=15 exit=0`**, F12 `PASS ids=S041,S042` | my run 17:30:13Z |
| harness / census red state earlier in the wave | was `exit 1` (E11 ×2; uncaught `FileNotFoundError`) until the entry landed — ordering fact for the lesson, not a result | §3.4 |

---

## §1 Work performed (bullets for the L1)

- **Claims frozen before dispatch.** C1 depth:verifiability (lowest non-retired axis, 4 held) —
  `anchorcheck.py`: (a) exit 1 on the six unverifiable classes, (b) CITE gains a `~/Projects/bounties/`
  arm → `BOUNTIES-ABSENT`, (c) `--selftest` one isolating fixture per limb + receipt at the landed digest,
  (d) no-harm on `SKILL.md`. C2 coverage (7 held) — F12 from an S041 re-capture + new S042.
  Pointer: `.ufo/waves/round-28/claims.json` (predicate / before / after / counter_commands / kill_rule /
  do_nothing_control / corpus_disclosure).
- **Wave shape from the committed spec.** `kasegi-r28-build`, one v2 wave, **69 seats**: executor 18,
  scribe 16, reviewer 12, critic 5, mutation-tester 5, scout 5, connector 3, revenger 2, sentinel 2,
  simplifier 1 — reviewers/critics/mutation-testers inside the build wave (round-26 routed defect 2
  structurally satisfied). Pointer: `wave1-spec.json`, `wave1/swarm-registry.json`.
- **C1 implementation landed.** `ExecImplC1` replaced the pre-change instrument (`c2a9e6c6…`) with
  `95333e29…`; `ExecInstrReadme` (+93 lines) and `ScribeSkillGate` (+3) documented it. The change was
  written **incrementally** between 17:26:14Z and 17:26:49Z (five digests observed: `0a24a173`,
  `7adfc847`, `982d7207`, `3122643c`, then `c3629229` and finally `95333e29`); at `3122643c` the live
  file raised `NameError: name '_selftest' is not defined`. Recorded so the report does not quote a
  mid-write reading as a result.
- **C1 before-values were reproduced by four independent seats** at `c2a9e6c6…`: `ExecFixtureRun`
  (counters a/b + counter-d side + fixture digests `969e2b92…` / `5c37b69e…` / SKILL `fa09d5b8…`),
  `ExecInstrSelftest` (crash twice, byte-identical, 442 B stderr), `ExecNoHarmC1` (13-way verdict table on
  `SKILL.md`; output byte-identical to `c1-controls/skill-before.txt` minus its `exit=0`), and
  `ExecReceiptCanonC1` (re-measured 17:23:00Z–17:24:54Z).
- **C2 capture + manifest legs complete.** `ExecCaptureS041` re-fetch `capture_exit=0`, HTTP 200,
  `fetched_bytes=1338665` → `snapshot_bytes=147267`, `sha256_match=yes`, `pdftotext 26.08.0`
  (pre-existing, no install), `cmp` vs round 26 `exit 0`. `ExecCaptureS042` `status=200`,
  `fetched_bytes=229982` → `snapshot_bytes=60508`, plus the 起算日 keyword audit. `ExecManifest` wrote 12
  assertions; its **first build was rejected by the round's own instrument**
  (`fa1f366f…` exit 2, `S042:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence`, the 8-character
  heading `5.起算日の連絡` < `MIN_QUOTE_CHARS=12`) and the fix replaced Q1 with the L145 body line
  (landed `e62ddad1…`). `ExecHarnessC2` independently ran the Q9 probes: `stem_matches_id=yes`,
  `assertions=7` per capture, `anchor_defects=0`, `q9_exit=0`, plus five mutant fixtures (m1 stem,
  m2 unanchored dupe, m3 broken anchor, m4 short quote, m5 outside).
- **C2 registry / README legs landed.** `ScribeRegistryC2` logs S042 + the S041 `used-by` old→new and
  proves the census on a mirror (`exit 0`) and on production while the entry was absent (`exit 1`).
  `ScribeReadmeC2` proves R6 line identity by per-line sha256 against `HEAD` and records the harness
  crash. `ScribeCensusNote.md` §3 predicted the E11 ordering failure before it happened.
- **Expected-list hardness documented** (`ExecExpectedList`, scratch): before `wc -l 41 / entries 39 /
  lines=39 total=39 pass=39 / expected=39 missing=0 unexpected=0 exit=0`; entry present with a stale list
  → `unexpected=1 exit=1`; after regeneration → `wc -l 42 / entries 40 / expected=40 … exit=0`. Second
  failure mode named: an entry without a `recheck:` line gives `lines=39 total=40 exit=1`.
- **R14 landed and practised.** `considerthese/2026-10-25.md` proposal 1 → `corpus/QUALITY.md` R14
  (wave-evidence economy); exercised in-round: per-seat receipts 3–19 KB, digests under `wave1/`, no
  corpus-file copies, largest control tree 44 KiB. Pointer: `receipts/ScribeR14.txt` §4.
- **Tooling.** Nothing installed or upgraded; `pdftotext 26.08.0` pre-existing; no pacman transaction
  attempted (host-wide pause respected).

---

## §2 Landed changes (bullets for the L1)

- **Commit `[PENDING]`.** Lane HEAD is still `94f387c`; the L1 lands through the lane helper. Until then
  say "worktree changes, uncommitted at 17:30Z" and name the commit afterwards.
- `git diff --stat` (production, 17:30:38Z): `LOG.md +49`, `SCORECARD.md +76`, `SKILL.md +3`,
  `corpus/QUALITY.md +6`, `corpus/README.md +28`, `corpus/SOURCES.md 5 ±`, `corpus/instruments/README.md +93`,
  `corpus/instruments/anchorcheck.py 278` changed → **8 files changed, 518 insertions(+), 20 deletions(-)**,
  plus untracked `corpus/knowledge/japanese-domestic-disclosure-workflow.md` and
  `corpus/source-snapshots/round-28/`.
- One writer per file held: instrument (`ExecImplC1`), instruments README (`ExecInstrReadme`), SKILL
  (`ScribeSkillGate`), captures (`ExecCaptureS041`/`S042`), manifest (`ExecManifest`), entry
  (`ScribeEntryC2`), SOURCES (`ScribeRegistryC2`), README (`ScribeReadmeC2`), QUALITY (`ScribeR14`),
  LOG (`ScribeLog`), SCORECARD (`ScribeScorecard`).
- Still `[PENDING]`: `corpus/lessons/round-28.md`, `.ufo/waves/round-28/c1-receipt-index.txt`,
  `corpus/instruments/knowledge-expected.txt` regeneration, `PROVINCE.md` F12 sentence, and the commit.

---

## §3 Before → after measurements (all `after` values `[MEASURED]` at `95333e29…`)

### §3.1 C1 — anchorcheck.py gate soundness (score 4 held)

Frozen commands: `claims.json` C1 `counter_commands[0..3]`, run from the lane root.

| limb | before (`c2a9e6c6…`) | **after (`95333e29…`, 17:30:03Z)** | frozen target | verdict |
|---|---|---|---|---|
| (a) fail-closed | exit `0`, `BASE-ABSENT` printed on the bad fixture | **`bad_fixture_exit=1`** | `1` | **reached** |
| (b) bounties arm | `0` `BOUNTIES-ABSENT` lines (cite invisible to CITE) | **`1`** line — `BOUNTIES-ABSENT md:3 ~/Projects/bounties/ops/claim-check.mjs:96 (base tree absent: /home/vgpnk/Projects/bounties/ops/claim-check.mjs)` | `1` | **reached** |
| (c) selftest | `--selftest` crash `FileNotFoundError`, exit `1`, 0 stdout | **`selftest cases=9 failures=0`**, `selftest_exit=0`, exactly `1` such line | `cases=N failures=0`, exit 0, `1` index line | **reached except the index line** (`c1-receipt-index.txt` absent) |
| (d) no-harm | exit `0`; `0 bad`; `LOST-RECORDED=306` | **exit `0`; `== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`** | unchanged | **reached** |
| stability | — | digest identical before and after every counter (`s1 == s2 == 95333e29…`) | — | **reached** |
| do-nothing control | exit 0 / 0 lines on unchanged bytes | unchanged bytes still reproduce `0`/`0` (pre-change runs §1; `c1-controls/*-before.txt`) | unreachable | **holds** |

**Report wording:** C1 is **measured at a stable landed digest**, pending only the canonical receipt
index. `ExecReceiptCanonC1`'s template still carries `@@SHA64@@` / `@@SELFTEST_EXIT@@` placeholders —
the L1 must fill it at `95333e29…` (or whatever digest is live at close) and re-run §3.5's index pair.

### §3.2 C2 — coverage (score 7 held)

| # | frozen command (short) | before | **after (17:30:13Z)** | target | verdict |
|---|---|---|---|---|---|
| 1 | frontier admitted (`awk`) | `11` | **`12`** | `12` | **reached** |
| 2 | `grep -lE '^source: S042 ' corpus/knowledge/*.md \| wc -l` | `0` | **`1`** | `1` | **reached** |
| 3 | `grep -cE '^\|\s*S042\s*\|' corpus/SOURCES.md` | `0` | **`1`** | `1` | **reached** |
| 4 | census `validate` | exit `0`, 41 rows | **exit `0`, `rows 42`** (A 39 / B 1 / C 2; mined 30), W04 ×2 only | exit `0`, 42 rows | **reached** |
| 5 | `frontier-recheck-count.py` | `entries=14 pass=14 exit=0` | **`entries=15 pass=15 exit=0`** (`PASS F12 … ids=S041,S042 exit=0`) | `15/15` | **reached** |
| 6 | recheck chain | manifest absent | **`source-recheck.py … --source S041 --source S042` exit `0`**; 12 assertions `occurrences=1` | exit `0` | **reached** |
| 6b | Q9 **enforcement** (not the manifest, the checker) | — | `[MEASURED]` a scratch manifest whose S042 Q2 is replaced by a phrase occurring twice, unanchored, prints `S042:Q2 OK occurrences=2 anchor=MISSING` and **exits 0** — the exactly-once conjunct is *reported, not enforced*; reproduces `MutQuoteC2` M3 LIVE | (published blind spot, R10/R11 shape) | **blind spot — disclose, do not claim enforcement** |
| 7 | entry contract | no entry | 103 lines; `source: S041` + `source: S042` + `verified-at: 2026-10-25`; one `recheck:` line, `bash -n` clean, carries `cd <lane-root> &&` (Q10); `--source` ids equal the declared ids (R12) | conformant | **reached** |
| 8 | expected list (r27 carry-forward 4) | `knowledge-expected.txt` 41 lines | **`recheck-audit.py`: `lines=40 total=40 pass=40 fail-closed=24 exit=1`; `expect=present expected=39 missing=0 unexpected=1 exit=1`** | `expected=40 missing=0 unexpected=0 exit=0` | **NOT reached** |

**Report wording:** the five frozen C2 counters all reach their after-values; the only C2 leg still red is
the expected-list reconciliation (leg 8), which is the round-27 carry-forward item, not one of the five
frozen counters. Fix: regenerate `corpus/instruments/knowledge-expected.txt` to 42 lines / 40 entries and
re-run `recheck-audit.py` until it prints `expected=40 missing=0 unexpected=0 exit=0`.

### §3.3 depth:density guard

| | before (base bytes, 17:24Z) | after (`SKILL.md` +3, 17:30:13Z) |
|---|---|---|
| mean dens | `150.3` | **`160.2`** |
| blocks | `20` | **`20`** |
| path-citation instances | `652` | **`656`** |
| lines | 1032 | 1035 |

- Block count unchanged at 20, so the 3 appended lines fell inside the existing
  `## Gates & probes registry` block: **+4 path cites**, no new low-density block, no structural distortion.
  Report this as the density row's movement, attributed to the appended gate row.
- **Comparand correction (must not be copied from the prompts or the historical rows):** `154.0 / 19
  blocks / 652` is the **r22-byte** baseline (`git show c8b719d:SKILL.md`). Base `c9f8b11` is
  byte-identical to `a04cc6c` (`fa09d5b8…`) and measures `150.3 / 20 / 652`; cause named by
  `ExecNoHarmC1` §2: commit `a04cc6c` added the gate\|probe block (`nb=5 ev=4 dens=80.0`), raising the
  block count 19 → 20 and pulling the **unweighted** mean down while cites stayed at 652. Using 154.0/19
  against base bytes would print a false −3.7 "regression".

### §3.4 In-flight red state (ordering finding for the lesson; not a result)

Between 17:23:49Z (F12 + S042 row landed) and the entry's arrival (before 17:27:57Z) the lane was red:

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	E11	S041 missing used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md
kasegi	E11	S042 missing used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md
census_exit=1
```

and `frontier-recheck-count.py` exited 1 with an uncaught
`FileNotFoundError: … 'corpus/knowledge/japanese-domestic-disclosure-workflow.md'` raised in
`entry_contract()` line 65 — no `entries=`/`pass=` line at all. Both closed when the entry landed; the
harness has **no clean "entry missing" verdict**, which is the lesson-grade defect.

### §3.5 What the L1 still must run

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
# 1. instrument index at the landed digest (fills ExecReceiptCanonC1's placeholders)
sha256sum corpus/instruments/anchorcheck.py
python3 corpus/instruments/anchorcheck.py --selftest; echo selftest_exit=$?
grep -cE 'selftest cases=' .ufo/waves/round-28/c1-receipt-index.txt
grep -oE 'instrument_sha256=[0-9a-f]{64}' .ufo/waves/round-28/c1-receipt-index.txt
# 2. expected list + audit
python3 - <<'PY'   # or ExecExpectedList's own regeneration command
import glob,io
rows=[l.strip() for l in open('corpus/instruments/knowledge-expected.txt') if not l.startswith('#')]
print(len(rows))   # confirm the current 39 before regenerating
PY
# regenerate to 40 entries / 42 lines, then:
python3 corpus/instruments/recheck-audit.py; echo audit_exit=$?   # want expected=40 missing=0 unexpected=0 exit=0
# 3. claim counters, one pass, at the final digest
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo bad_fixture_exit=$?
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT
python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | grep '^== '
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print "frontier="n+0}' corpus/README.md
grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l ; grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo census_exit=$?
python3 corpus/instruments/frontier-recheck-count.py; echo harness_exit=$?
python3 corpus/instruments/density.py SKILL.md --label r28-close | grep -E 'mean dens|Total path|^# Density'
```

---

## §4 Sources & frontier (bullets for the L1)

- **S042 (new, tier A, registry line 48).** URL `https://www.ipa.go.jp/security/todokede/vuln/process.html`;
  kind `docs`; scope = the IPA/JPCERT/CC intake process as that page states it; anchor cites
  `steps 1 to 10 (L132-L160)`, `step 5 起算日の連絡 (L144-L145)` against the round-28 capture, plus the
  page's `最終更新日 2017-05-30`; `mined`, `opened 2026-10-25`, `recheck 180d`, `used-by` exactly the entry.
- **S041 `used-by` old → new (R8, logged).** old
  `…/iso-29147-and-30111-division-of-labour.md, …/iso-29147-divergence-and-clause-crosswalk.md` → same +
  `, …/japanese-domestic-disclosure-workflow.md`; 13/13 cells, every other cell byte-identical
  (`receipts/ScribeRegistryC2.txt` §3; reproduced by me from `git show HEAD:corpus/SOURCES.md`).
- **起算日 anchors (read on the landed captures).** `S042.txt`: token ×3 on 2 lines — `L144`
  `5.起算日の連絡`, `L145`
  「JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。IPAは起算日、および、詳細情報連絡日を発見者へ連絡します。」
  — the coordinator starts the clock and then tells the finder. `S041.txt`: ×9, definition at `L340`
  (first *attempted* contact), edition stamp `2026 年 10 月` at `L10`.
- **Manifest pins (Q9).** 12 assertions: S041 Q1 `L340`, Q2/Q3 `L212`/`L249`; S042 Q1 `L145`; every quote
  `occurrences=1` raw and normalized, so no `anchor` is required; `src stem == id` and sha pins verified by
  `ExecManifest` and independently by `ExecHarnessC2` (`q9_exit=0`). `MIN_QUOTE_CHARS=12` is what rejected
  the 8-character heading — a real discrimination event.
- **Q9 blind spot (publish, do not hide).** The landed manifest happens to satisfy Q9 (`occurrences=1`
  everywhere), but the checker does not enforce it: a scratch manifest (`mktemp -d`, copies of both
  captures, S042 Q2 replaced by a twice-occurring phrase, no anchor) prints
  `S042:Q2 OK occurrences=2 anchor=MISSING` and exits 0 (`[MEASURED]`, my run 17:33Z) — the same
  `M3 LIVE` result as `receipts/MutQuoteC2.txt`. Report the Q9 conjunct as **verified for these 12 quotes**
  and **not instrument-enforced**, which is the R10/R11 disclosure shape.
- **Frontier F12 (README line 213).** `| F12 | Japanese state-coordinated disclosure workflow | admitted |
  knowledge/japanese-domestic-disclosure-workflow.md | S041, S042 | Use 起算日 — the first *attempted*
  developer contact, not an acknowledgement or a submission date — as the Japanese column when comparing
  coordinator timelines against F02. |` Amended admitted-count sentence `12/12` (F12 at round 28); the
  `0/18` lost-domain sentence untouched (separate denominator).
- **Assimilation Gate `[PENDING]`.** `ScoutAssimilation.txt` and `ScribeFrontierNote.txt` exist; the Gate
  section for the lesson does not. Shape: one theme; **ADMIT** = staged entry + S042 by document (staged
  `S043` = lane `S041`, cited, not re-registered); **REJECT** candidates with package-path quotes:
  `chinese-criminal-thresholds-and-authorisation.md` (re-confirm or lift) and
  `vendor-third-party-finding-coordination-2026-10-23.md` (`ground: F20` names no lane row; the lane
  frontier now tops out at F12). Round-26 routed defect 3 binds: URL + access date 2026-10-25 + **inline
  ≤25-word located quote** per new row. Package (read-only):
  `/home/vgpnk/Projects/shokuknow/merge/kasegi/{MERGE-REPORT.md,SOURCES.append.md,knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md}`.
- **Census before → after.** Before: exit 0, 41 rows (A 38/B 1/C 2; mined 29, queued 9, rejected 3),
  W04 ×2. After: exit 0, 42 rows (A 39; mined 30), W04 ×2 only — one tier-A mined row added, no warning.
  Mid-wave red state in §3.4 is the ordering evidence (`ScribeCensusNote.md` §3 predicted it).

---

## §4b **Correction the report must carry: the frozen corpus disclosure does not reproduce**

`claims.json` C1 `corpus_disclosure` says the bounties arm makes 4 corpus marked citations
(`claim-gates.md`, `intake-and-finalize.md`, `mission-control.md`, `source-tree-loss-2026-09-28.md`)
"newly classify LOST-RECORDED". Measured on the landed bytes, with the pre-change instrument
(`git show c9f8b11:corpus/instruments/anchorcheck.py`) as the control:

| file | `LOST-RECORDED` old instrument | `LOST-RECORDED` new instrument (`95333e29…`) |
|---|---|---|
| `claim-gates.md` | `0` | `0` |
| `intake-and-finalize.md` | `0` | `0` |
| `mission-control.md` | `0` | `0` |
| `source-tree-loss-2026-09-28.md` | `15` | `15` |

**No citation was newly classified.** Two structural facts:
1. `LOST-RECORDED` is decided by the `^\[lost-(tree|base)\]\s+` marker **inside a backticked token**
   (`anchorcheck.py` `LOST` regex), before any path arm runs — the bounties arm cannot reclassify a marked
   token, so the disclosure's causal claim is impossible by construction.
2. The four named references are written `source: [lost-tree] ~/Projects/bounties/…` **outside** the
   backticks (and the backticked mentions carry no `:line`), so `CITE` never sees them in either
   instrument. Measured reach of the new arm on the lane's own text: **0** unmarked backticked bounties
   `path:line` tokens across `SKILL.md` + all 40 `corpus/**/*.md`, **0** `BOUNTIES-ABSENT` verdict lines on
   `SKILL.md`, **0** corpus files emitting `BOUNTIES-ABSENT`. The arm is demonstrated only on the committed
   fixture (`1` line, exit 1) and inside the 9-case selftest.

**Recommended report wording:** "The `~/Projects/bounties` arm is proven on the committed fixture (1
`BOUNTIES-ABSENT` line, exit 1) and by the selftest; on the lane's own text it classifies nothing new — the
four files named at freeze report `LOST-RECORDED` 0/0/0/15, identical under the pre-change instrument, and
`SKILL.md`'s classes are unchanged (`LOST-RECORDED=306`)." File it as an appended erratum
(e.g. `.ufo/waves/round-28/claims-disclosure-erratum.md`), **never** as an edit to `claims.json` (R25-1).
Same mistake class as M27-1 (a premise assumed instead of measured); it is a lesson `## Mistakes`
candidate with a ready-made flip condition: re-run the table above after any corpus rewrite.

---

## §5 Trend verdicts — **proposed**; the L1 owns the final call

- **expansion — proposed `improved`.** F12 admitted (`11 → 12`), one new tier-A mined row (`41 → 42`;
  A 38→39, mined 29→30), two sha-pinned captures (S041 byte-identical to round 26, S042 new), a 12-quote
  manifest whose recheck exits 0, and a 103-line entry whose harness verdict is `PASS ids=S041,S042`.
  Evidence: §3.2 rows 1–3, 5–7; `corpus/README.md:213`; `corpus/SOURCES.md:48`.
- **quality — proposed `improved`.** The verifiability gate now fails closed on six named classes
  (`bad_fixture_exit=1`), the bounties arm fires (`1` line), `--selftest` runs 9 isolating cases
  (`selftest cases=9 failures=0`, exit 0), and no-harm holds (`SKILL.md` exit 0, `0 bad`,
  `LOST-RECORDED=306` unchanged). The captures are **re-grounded**, not borrowed from the staged package.
  Two honest limits keep this from being unconditional: the canonical index is still absent (§3.1), and
  §4b's disclosure correction replaces the frozen sentence. Both are disclosure requirements, not
  after-value misses.
- **discernment — proposed `improved`.** Four signals: (i) the manifest's first build was **rejected by
  the round's own instrument** (`quote-too-short-to-be-evidence`) and fixed by re-locating a longer quote
  instead of lowering `MIN_QUOTE_CHARS`; (ii) the census/harness red state was surfaced mid-wave by
  runnable counters and predicted from a scratch tree before it happened; (iii) §4b — the round checked its
  own frozen disclosure and found it false, then published the correction rather than repeating it;
  (iv) the Gate draft (`wave1/ScribeLessonGate.md`, 218 lines / 22,640 B) records **1 admit** (the workflow
  entry + S042 by document, quote at `S042.txt:145`, occ=1, inline) and **2 rejects** with inline quotes:
  `chinese-criminal-thresholds-and-authorisation.md` (re-confirmed; `bash -n` on its `recheck:` line exits 2)
  and `vendor-third-party-finding-coordination-2026-10-23.md` (`grep -cE '\| F20 ' corpus/README.md` → 0).
  It also refuses to reuse `ScoutAssimilation`'s `anchor:` cells as quotes and hand-checks the fetch verdict
  itself — that refusal is the discernment evidence, not the count. The Gate is a draft; only the lesson's
  assembled `## Gate` counts.

---

## §6 SHONEN — four boxes, all `[~]`, refreshed pointers; no `[x]`

No non-author verifier is named for this round at the state stamp, so `[x]` is unavailable by the gate's own
rule (`templates/round-prompt.md`: `[x]` needs a named non-author verifier).

- `[~]` **SKILL.md real decision tables / error patterns / checklists / cited sources** — `density.py
  SKILL.md` at the landed bytes: mean **160.2**, **20** blocks, **656** path cites (base: 150.3/20/652);
  `anchorcheck.py SKILL.md` → `7 in-range / 0 bad / LOST-RECORDED=306`, exit 0; the round-28 gate\|probe row
  is appended (`SKILL.md +3`, line number in `receipts/ScribeSkillGate.txt`).
- `[~]` **At least one end-to-end domain task executed and logged in LOG.md** — the F12 chain is now
  end-to-end and green (capture → sha-pinned snapshot → 12-assertion manifest → 103-line entry → registry
  row → frontier row → harness `15/15`), and LOG.md carries the round-28 entry (+49 lines) — but its claim
  cells still read `pending` and the lane commit does not exist. The hunt-to-claim pipeline half remains
  unmet (`round-24-verifier-spotcheck.md:210-215`).
- `[~]` **Instructions executable by an agent without oral context** — the entry's `recheck:` line is one
  cwd-independent command (`bash -n` clean, `cd <lane-root> &&`, `--source` ids equal to its headers) and
  runs green (`recheck_exit=0`); harness `15/15 exit=0`; the expected-list reconciliation is written down
  with its command (`corpus/README.md` §Round-28 reconciliation) but its regeneration is still `[PENDING]`
  (`expected=39`); 24 of 40 entry rechecks still fail closed on lost bases (`recheck-audit.py`
  `fail-closed=24`).
- `[~]` **No cross-domain bleed (PROVINCE.md still accurate)** — **flag:** `PROVINCE.md:38` still reads
  `F01–F10` (F11 named on line 41) and has **no F12 sentence**; `PROVINCE.md` is not in the round-28
  ownership map, so no seat may edit it. The L1 must append the F12 sentence or caveat the box. Connector
  receipts (`ConnOverlap`, `ConnClaims`, `ConnStagedCensus`) are `[PENDING]`; round-26's sibling-overlap
  verdict is the only adjacency evidence.

---

## §7 Remaining closure checklist for the L1

1. Regenerate `corpus/instruments/knowledge-expected.txt` to 40 entries / 42 lines; `recheck-audit.py` must
   print `expected=40 missing=0 unexpected=0 exit=0` (§3.2 leg 8).
2. Assemble `.ufo/waves/round-28/c1-receipt-index.txt` at the landed digest (`95333e29…` or the close-time
   digest), filling `ExecReceiptCanonC1`'s `@@…@@` placeholders; verify the pair from `claims.json`
   `counter_commands[2]`.
3. `ScribeLesson`: assemble `corpus/lessons/round-28.md` from the landed Gate draft
   (`wave1/ScribeLessonGate.md`), including the S041 `used-by` old→new, the §3.4 ordering defect, and the
   §4b disclosure correction as `## Mistakes` rows; `ScribeQualityCross` supplies the Q1–Q10 table.
4. `ScribeReceiptsC2` receipt bundle; `ScribeSourcesGate` for the Sources & frontier raw material.
5. Decide the `PROVINCE.md` F12 sentence (unowned).
6. Fill the `pending` cells in `LOG.md` and `SCORECARD.md`; use the **same-bytes** density comparand
   (`150.3 / 20 / 652` before → `160.2 / 20 / 656` after), never `154.0 / 19`.
7. Name the landed commit in "Landed changes"; file the §4b erratum as its own appended file.

---

## §8 Receipts present at the state stamp (31 files, 17:33Z)

| receipt | one-line content |
|---|---|
| `ExecImplC1.txt` | instrument change; observed `selftest cases=9 failures=0`, bounties fixture exit 1; mutant M1 (landed minus the bounties arm) |
| `ExecInstrReadme.txt` | instruments README +93 lines (verdict map, selftest spelling, bounties root, write scope) |
| `ExecFixtureRun.txt` | counters (a)(b)(c) + SKILL side baseline at `c2a9e6c6…`, fixture digests pinned |
| `ExecInstrSelftest.txt` | pre-state `--selftest` crash twice (byte-identical), five byte facts, determinism |
| `ExecNoHarmC1.txt` | SKILL 13-way verdict table; density `150.3/20/652` and the stale-154.0 proof |
| `ExecReceiptCanonC1.txt` | canonical-index rules + **template with `@@…@@` placeholders** (not finished) |
| `ExecCaptureS041.txt` | re-capture `e18acbf9…`; `cmp` vs round 26 `IDENTICAL`; 起算日 ×9, L340 |
| `ExecCaptureS042.txt` | `b432ec16…`; `status=200`, `229982 → 60508`; 起算日 ×3 L144/L145; `MIN_QUOTE_CHARS=12` |
| `ExecManifest.txt` | 12 assertions `occurrences=1`; `fa1f366f` (exit 2, quote-too-short) → `e62ddad1` |
| `ExecHarnessC2.txt` | Q9 probe `q9_exit=0` (7 assertions/capture, 0 anchor defects), m1–m5 mutants, B1 `14/14`, B2 harness crash |
| `ExecC2Counters.txt` | five frozen C2 counters, two pre-entry passes, landing table, re-run block |
| `ExecExpectedList.txt` | expected-list before / stale / regenerated triples in scratch; both failure modes |
| `ExecRecheckAuditR28.txt` | recheck-audit and entry-contract checks around the entry landing; its `exit=0` segment is the **regenerated candidate** list, while the live file is still 41 lines (my §3.2 leg 8) |
| `ExecScopeSweep.txt` | write-scope sweep snapshot 17:28:53Z; base ancestry; no tools installed (read-only evidence for "one writer per file") |
| `MutArmC1.txt` | bounties-arm mutants M1 (arm removed), M2 (confinement removed), M3 (wrong root candidates) — all KILLED; PRE-STATE label for the commit |
| `MutQuoteC2.txt` | quote mutants M1/M2 killed; **M3 LIVE** — `source-recheck.py` accepts `occurrences=2 anchor=MISSING` exit 0 (reproduced by me, §3.2 leg 6b) |
| `ScribeLessonGate.txt` | Gate draft receipt: 1 admit + 2 rejects with inline quotes, F20 grep → 0, `bash -n` exit 2 on the refused entry's recheck |
| `ScribeQualityCross.txt` | Q1–Q10 criterion table against the landed entry (independent bar check before admission) |
| `ExecCensusDry.txt` | census `exit 0 → 1 → 0` on a mirror after both registry edits; production pre-state |
| `ExecGateLog.txt`, `ExecSkillGateSupport.txt` | SKILL gate-row support/log for the scribe append |
| `ScoutAssimilation.txt`, `ScribeFrontierNote.txt` | assimilation survey; F12 `next`-cell wording and topic-collision check |
| `ScribeEntryC2.txt` | entry content, quote list re-located in the round-28 captures |
| `ScribeRegistryC2.txt` | S042 row + S041 `used-by` old→new; census on mirror vs production |
| `ScribeReadmeC2.txt` | F12 row + amendments; R6 line-identity proof; harness `exit 1` at the time |
| `ScribeR14.txt` | R14 appended (+6, R6 proof), grounding re-measured, practice instance |
| `ScribeSkillGate.txt` | SKILL gate row appended, prior/new line numbers, anchorcheck before/after |
| `ScribeLog.txt` | LOG.md +49 diff, pre-state values, in-flight gate warning |
| `ScribeScorecard.txt` | SCORECARD +76, `pending` cells, `150.3/20/652`, transient-red notes |

Digests on disk: `wave1/{ExecC2Counters,ExecCaptureS041,ExecFixtureRun,ExecInstrSelftest,ExecNoHarmC1,
ScribeCensusNote,ScribeR14}.md`, plus `wave1/ScribeLessonGate.md` (Gate draft) and harness fixtures under
`wave1/ExecHarnessC2/`.

No credential material, session URL or private URL appears in this digest. This seat installed nothing, ran
no pacman transaction, made no VCS write, started no background job and dispatched no subagent.

---

## §9 Final scan (post-write, 2026-10-25T17:34:36Z)

State unchanged from the measurement stamp: `corpus/instruments/anchorcheck.py` still
`95333e29…6f144514`; the entry still `a22d2321…13a6`; manifest `e62ddad1…f291d`;
`anchorcheck.py --selftest` → `selftest cases=9 failures=0`. Receipts in
`.ufo/waves/round-28/receipts/` now number **32**, the 32nd being this seat's own
`ScribeReportDigest.txt` (§8 lists the 31 that existed before it).

Anything written after this stamp — including the canonical C1 index, the regenerated expected list, the
assembled lesson, the lane commit and any reviewer/mutant/revenger receipt — is **not incorporated** here
and must be read from the receipts themselves. The §3.5 / §7 commands remain the closure gate.
