# Round 29 — kasegi

Lane: `kasegi-shokunin`. Revisions, named separately (the wave's receipts use all three):
**lane tip at round start / base** `7a6591c1eb8a14f427297980a96fa8bb339f29ee` (round-28 verifier
spot-check), **claims-freeze commit** `f28ff5d26b29270f93163117e7255e24f0b1d947` (contains
`claims.json`, `c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt`), and
**dispatch commit** `46e07f6ae8f23debb10034164252e7027b4d9091` (wave-1 spec + dispatch; lane HEAD
while the wave ran). `git merge-base --is-ancestor f28ff5d HEAD` → exit 0.

Shape: one v2-policy wave, `kasegi-r29-build`, **64 seats** (`wave1-dispatch.json`
`counts.spawn=64`, resume 0; `wave1.ready.dispatched` `2026-10-25T15:15:08`). Role split
(ScribeLog, from the swarm registry): scout 5, connector 3, executor 17 + lab-probe 3, scribe 13,
reviewer 11, critic 4, mutation-tester 4, sentinel 1, revenger 1, simplifier 2. The round
re-declared the two frozen claims C1/C2 and ran the frozen counters from the committed before
receipts.

> **Assembly status.** This lesson was assembled by `ScribeLesson` after the wave's seat work
> landed (the three scribe sections and the canonical C1/C2 receipts are in). The production files
> measured below are the **landed working-tree bytes** at assembly (the integration commit had not
> been made yet). Post-integration re-runs are named under Close-out; every value below carries the
> seat, digest and UTC stamp that produced it, and nothing is projected. The `c1-receipt-index.txt`
> `instrument_sha256` line and the C2 after values here are measured at those bytes; the committed-
> digest binding is checked by `ExecPostCommitRecheck` after the L1 commits (owed).

Answering model for this seat: `inception/mercury-3` (config route table; no model was passed).
No tool was installed by this seat.

## Frozen claims — before → after, with the state of every number

| Claim | Axis | Before (measured, committed) | After (measured at the landed bytes) | Verdict at assembly |
|---|---|---|---|---|
| **C1** | depth:verifiability (4, lowest non-retired) | `anchorcheck.py` sha256 `23818c1204…ee7396` (base bytes): `--selftest` `selftest cases=9 failures=0`, exit 0; `grep -cE 'limbs=[0-9]+ covered='` → **0** (no coverage assertion); git-free PATH run → **exit 1** with `FileNotFoundError: 'git'` traceback; `SKILL.md` exit 0, bad 0, LOST-RECORDED 306. Receipts `.ufo/waves/round-29/c1-controls/before.txt`, `wave1/c1-controls/base-control-*` | `anchorcheck.py` sha256 `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97`, 561 lines (`ExecImplC1`; `c1-receipt-index.txt`): (a) `--selftest` → `selftest cases=12 failures=0`, `limbs=9 covered=9`, exit 0; (b) git-free PATH run → `SKIP pin-broken (git not found)`, `selftest cases=12 failures=0`, `limbs=9 covered=9`, **exit 0** (`nogit_exit=0`, clean skip, no traceback); (c) `SKILL.md` → exit 0, bad 0, LOST-RECORDED 306, PIN-BROKEN 0, ORIGIN 0, OUTSIDE-BASE 0, BASE-ABSENT 0; (d) `instrument_sha256` line matches the production digest | **Frozen targets met at the landed bytes** (`ExecCanonC1`, `RevC1Instrument`, `RevC1Controls` agree; this seat re-ran (a)/(b)/(c)). Caveats recorded: (i) in the git-free run the PIN-BROKEN case is skipped yet still counted in `covered=9` — the normal-PATH run executes all nine failing fixtures (`RevC1Instrument` verified the three new fixtures fail on the baseline copy); (ii) the committed-digest binding is owed until the integration commit preserves these bytes |
| **C2** | coverage (7) | frontier admitted **12**; entries citing `S04[3-5]` **0**; registry **42** rows; census exit 0 (W04 S028/S029 only); harness `entries=15 pass=15 exit=0`; no round-29 captures (`c2-controls/before.txt`, `census-before.txt`) | frontier admitted **13** (`README.md` F13 row); entries citing `S04[3-5]` **1** (the F13 entry); registry **45** rows, census **exit 0** (W04 S028/S029 only); harness `entries=16 pass=16 exit=0` with `PASS F13 knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0`; per-id `source-recheck` **exit 0 each** on the frozen round-29 manifest (sha256 `910608e6…2fb16a`, 3,857 B) — all 12 assertions `occurrences=1` raw and normalized, stems==ids, S043 anchors 31/40/170/92 verified (record-3787452 policy-text capture, sha256 `d3b815ed…69199`, 204 lines / 7,298 B) | **Counter set met at the frozen bytes** (`ExecCanonC2` POST-STATE; `RevC2Manifest` canonical run; this seat re-ran all seven counters). The kill-rule clause "any manifest assertion not occurrences=1" is satisfied literally — every assertion is exactly-once. The mid-wave `79b32d50` state (S043 Q1/Q2/Q4 occurrences=12, single-line array capture) tripped that clause and was resolved by the record-scoped re-capture (F1 below) |
| depth:density | 9 | `density.py` on base `SKILL.md` = mean **160.2**, **20** blocks, **656** path-citation instances | same instrument after the SKILL.md append: mean **167.5**, **22** blocks, **659** cites; anchor verdict classes unmoved (7 in-range / 0 bad / LOST=306 / 0/0/0/0, exit 0). Redessed as measurement change from the append, not a score claim | **No verdict-class movement; density change disclosed, not claimed** (`ExecDensityNoHarm`) |

Note on the C2 verdict: the manifest was declared "final" twice while bytes moved; the frozen
state is `910608e6…` (RevC2Manifest F1 recorded the sequence `3a0dec1b` → `79b32d50` (announced
final) → `54a36f4f` (mid-rework) → `910608e6` (frozen)). At `79b32d50` the S043 quotes were
`occurrences=12` on the single-line 153-record array capture, tripping the literal kill-rule
clause; `ExecCapS043` revision 1 replaced the capture with the record-3787452 policy text
(204 lines / 7,298 B, `d3b815ed…`) and the frozen manifest re-anchored Q1–Q4 at 31/40/170/92 —
every assertion is now exactly-once. The canonical counter receipt (ExecCanonC2 POST-STATE) and
`RevC2Manifest`'s binding table agree; the mid-wave trip is recorded as F1, not hidden.

### Both states of the frozen counters, timestamped

Only the runs at a digest that stayed fixed count:

| UTC | seat | instrument digest | result |
|---|---|---|---|
| freeze | `c1-controls/before.txt` | `23818c1204…` | cases=9 / 0 / exit 1 traceback — before |
| freeze | `c2-controls/before.txt` | n/a | 12 / 0 / 42 / 15-15 — before |
| 18:15–16Z | ExecCanonC2 | n/a | seven counters PRE-STATE (subject un-landed), each DIFFERS with named re-run — correctly non-comparative |
| 18:16–17Z | ExecCanonC1 | `68e1bdc6…` | (a) 12/0 + 9/9, (b) nogit_exit=0, (c) 7/0/306 exit 0, (d) digest line — all four targets |
| 18:20Z | RevReceiptsCanon | `68e1bdc6…` | re-ran C1 counters (identical) and C2 counters at post-landing bytes (13/1/3/45/0/16-16/0) |
| 18:22Z | ExecCanonC2 (POST-STATE) | n/a | all seven C2 counters MATCH (13/1/3/45/0/16-16/0) |
| 18:24Z | ScribeReportDigest addendum | `68e1bdc6…` | caught transient intermediate digest `57c5e111…` at 18:20Z whose git-free run exited 1 (covered=8); settled at `68e1bdc6…` (M29-6) |
| assembly | ScribeLesson (this seat) | `68e1bdc6…` | re-ran C1 (a)/(b)/(c) and all seven C2 counters — identical values |
| 18:23–25Z | ExecCapS043 rev 1 / ExecManifestC2 | n/a | S043.txt replaced by record-scoped policy text (`d3b815ed…`, 204 lines); manifest frozen at `910608e6…` |
| 18:30Z | RevC2Manifest (canonical) | `9fe6a4a0…` | 12/12 assertions exactly-once raw+normalized, stems==ids, anchors 31/40/170/92 verified, recheck exit 0; probes P1/P2/P3 fail closed (table `b7d438ef…`) |

**Instrument / control discrimination.** Do-nothing control at base bytes (`wave1/c1-controls/`
+ `c1-controls/before.txt`): cases=9, limbs grep 0, nogit exit 1 traceback → cannot meet the
target. C2 control at base (`c2-controls/before.txt`): 12 / 0 / 42, harness 15/15, no captures →
cannot meet the target. Mutants M1 (drop mirror-outside-base fixture), M2 (drop `limbs=` line),
M3 (force covered=8) each flip the fixed selftest red (`ExecControlC1`, `RevC1Controls`); M4's
isolation is partially unverified (`RevC1Controls` medium finding — compound mutant). The C1
counters accept a hardcoded printer (CritC1Kill C2); the C2 counters pass degenerate shapes
(CritC2Kill C1–C4) — recorded as instrument limits below.

## Gate — the assimilation set

*Drafted by `ScribeLessonGate` (`.ufo/waves/round-29/wave1/ScribeLessonGate.md`), quarantine
verdicts finalized by `ScribeQuarantine`, and reconciled by this seat against the landed tree.
The gate draft was written mid-wave, so its "could not verify" items (F13 row, entry body, canon
receipts, reviewer spot-check) are resolved here against the landed state.*

Package: `/home/vgpnk/Projects/shokuknow/merge/kasegi` (read-only in this round; nothing written
into it). Theme: **program severity ladders and reward scales** (F13). Package bytes read this
round: `MERGE-REPORT.md`; `SOURCES.append.md` (94 staged rows S031–S124); staged entries
`knowledge/corpus/knowledge/program-severity-ladders-and-reward-scales.md`,
`program-scope-rules-and-asset-boundaries.md`, `claim-packaging-and-report-quality.md`. Register
read (read-only): `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`.

### Collision / adoption ids

Numeric collisions: **12** (staged S031–S042 vs lane S031–S042) — `assimilation/collisions`
(12 lines). Guard proved discriminating (ScribeAssimReport): an indented `  | S002 |` fixture
row collides under the 0–3-space-tolerant pattern (1 hit) while the naive `^\|` pattern misses it
(0 hits) — no colliding row can be appended silently.

The adopted rows resolve **by document, never by arithmetic** (URL equality; join table in
`ScribeAssimReport.md` / `ConnStagedCensus.md`): staged S031 (HackerOne policy_versions) → **S043**;
staged S032 (Bugcrowd VRT README) → **S044**; staged S033 (Bugcrowd CWE crosswalk) → **S045**.
All three URLs were absent from the lane pre-append (`grep -cF` → 0) and the ids free. Staged
S042→lane S042 (IPA, round 28); staged S043/S064/S076→lane S041 (JPCERT/CC guideline, already
registered) — cited, not re-registered.

### Admitted

| Row | Admitted as | Document / capture | Opened | Evidence | Entry |
|---|---|---|---|---|---|
| S043 | tier A, `mined` | HackerOne standard program policy set — `https://hackerone.com/security/policy_versions` | 2026-10-25 | `S043.txt` (record-3787452 `new_policy` policy text; 204 lines / 7,298 B; sha256 `d3b815ed…69199`; raw array capture preserved as fetch evidence in ExecCapS043 — 1,220,741 B / `02ecb500…`, ETag cross-bound); manifest asserts Q1–Q4 at anchors 31/40/170/92, all occurrences=1 | `corpus/knowledge/program-severity-ladders-and-reward-scales.md` |
| S044 | tier A, `mined` | Bugcrowd VRT repository README — `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md` | 2026-10-25 | `S044.txt` (8,187 B; sha256 `8adfca61…26bf`); P1–P5 labels (lines 33–38), suggested-baseline override (line 11); manifest Q1–Q4 | same entry |
| S045 | tier A, `mined` | Bugcrowd VRT CWE mapping dataset — `…/master/mappings/cwe/cwe.json` | 2026-10-25 | `S045.txt` (14,575 B; sha256 `f583a396…0f86`); `idor`→`CWE-932` (`$.content[4].children[2]`), `metadata.default` null, `cwe: null` nodes; manifest Q1–Q4 | same entry |

**The admitted entry** (`corpus/knowledge/program-severity-ladders-and-reward-scales.md`, 58 lines,
7,583 B, sha256 `6beeedd7d2b2cb5ff3ecb5383041dbee63b9be54d9be50e282352b1b41a39ed4`; created this
round):
`capture-source.py` could not fetch S043 (Cloudflare JS-disabled stub to urllib); the snapshot was
taken with the assignment's curl fallback and is fetch-reproducible today (LabC2Probe §4). S044/S045
are instrument-reproducible byte-identical today.


| Property | Landed value |
|---|---|
| header | `source: S043` / `source: S044` / `source: S045` (each with URL + capture anchor), `verified-at: 2026-10-25`, `ground: F13` |
| recheck | one executable, cwd-independent line: `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S043 && … --source S044 && … --source S045` |
| measured, foreign cwd (`/tmp`) | `bash -n` exit 0; run exit 0; all three ids re-verified from pinned captures (ExecHarnessC2 §G; ExecEntryF13; RevC2Entry) |
| `--source` id set = declared `source:` id set | S043/S044/S045 — equal; three chained invocations (flag is single-valued) |
| frontier binding | `PASS F13 knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0`, `entries=16 pass=16 exit=0` |
| Q9 binding | manifest assertions all pinned and exactly-once (12/12, raw = normalized); stems==ids; S043 anchors 31/40/170/92 verified by the instrument and by the reviewer's byte-offset check |
| corpus census | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0, rows 45, W04 S028/S029 only |

**What the entry had to be re-grounded away from (staged → lane).** The staged package entry
covered four ladders (CVSS-B, VRT, CNVD 众测, BILISRC/360SRC). The landed entry restricts F13 to
the three captured lane rows S043/S044/S045; the CNVD 众测 and BILISRC ladder claims (staged
S034/S036) are not adopted because those rows are not lane-registered (Q2), and the entry's
`## Limits` says so. Staged S032/S033 are cited under lane S044/S045 (document mapping). The
staged `opened` date 2026-10-23 → 2026-10-25; the staged `anchor` prose was rewritten from the
captures.

### Refused (rejects carry flip conditions)

| Candidate (package path) | Failing gate | Reason (measured evidence) | Flip condition |
|---|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` | Q2, Q3, Q7/Q10, ground | adopted S043 is registered, but the entry's platform-branch claims cite staged S034 (CNVD 众测) and S035 (360SRC) — not lane rows; no located quote for those claims; `recheck:` is the package's prose form; `ground` is package F-space, not a lane frontier topic | register S034+S035 as lane rows with captures + exactly-once quotes; add a named lane frontier row |
| `claim-packaging-and-report-quality.md` | Q2, Q3, Q7/Q10, ground | sources S034/S035/S036 all staged, none registered; ground F11 is package F-space (lane F11 = ISO 29147/30111). Measured openings: all three URLs reachable (200; S036 PDF 439,149 B), but refusal is by-registration, not unavailability | register S034–S036 with captures + located quotes; re-ground claims |
| `chinese-criminal-thresholds-and-authorisation.md` (standing, re-confirmed) | Q2, Q3, Q4, Q5, Q7/Q10, ground | staged S044/S045/S046 not lane rows; Q4 generalizes three instruments into a jurisdiction-wide rule; no located quote; prose recheck | register S044/S045/S046 with captures; attribute per instrument |
| `vendor-third-party-finding-coordination-2026-10-23.md` (standing, re-confirmed) | ground, Q2, Q3, Q7/Q10 | `ground: F20` names no lane frontier row (`grep -cE '\| F20 ' corpus/README.md` → 0); sole source staged S080 not a lane row; quote restated with no location; prose recheck | register the MSRC page; capture; locate an exactly-once quote; add a lane frontier row |

No Q/R bar was relaxed. None of the refused files exists in the lane.

### Quarantine slice — seven rows hand-checked (2026-10-25, instrument UA)

Slice from the register: S037/S054 (`payload-absent`), S048/S065/S068/S069/S070 (unfetchable at
register time). Fresh fetch/quote-locate verdicts (ScribeQuarantine, from ScribeLessonGate's
runs): **S037** 200/24,189 B → `fetched-no-quote` (composite register quote 0×; `发布日期` 1×);
**S054** 200/513,648 B PDF → `fetched-no-quote` (`府連第7号` 0×, glyph-spaced header); **S048**
404/748 B → `unfetchable`; **S065** 200/7,465,472 B PDF → `reachable-quote-located` but no entry
cites it (unmotivated row); **S068** 301→302→200/94,027 B → `already-mined-by-document` (URL
byte-equal to lane S040); **S069/S070** — the register's truncated URLs as cited return 302/0 B and
fail TLS (curl exit 60) so are `unfetchable` as registered, while the full staged `20_WD_…pdf` /
`20_DI_…pdf` URLs return 200 (1,470,121 B / 234,182 B) with the staged sections located
(`reachable-quote-located` — ScoutAssimilation's final re-hand-check; the register URL is truncated).
**None adopted; flips vs round 28: S069/S070 flip `unfetchable` → `reachable-quote-located` under
the full staged URL (the register URL itself remains dead as cited).**

### Spot-check result (LEARNING.md §Discernment)

Non-author reviewer `RevC2Entry` re-opened the final F13 entry bytes and one refused candidate:

| item | gate decision | re-opened by | agree/disagree | reason |
|---|---|---|---|---|
| S043/S044/S045 + F13 entry | admit | `RevC2Entry` (reviewer, non-author) | **Partial agree** | Q1–Q7 and Q9 pass on the final 58-line bytes: source-id equality holds, foreign-cwd `bash -n` and run exit 0, capture anchors verified, attribution/falsifiability/documentation-only sound. Two bar failures remain: Q8 (normalization/receipt transformation not declared) and Q10 (recheck line lacks the required `#` human note) → not an unconditional admit. The reviewer's earlier stub-time disagreement applies to those bytes only; the current entry landed after it. |
| `program-scope-rules-and-asset-boundaries.md` (package) | reject | `RevC2Entry` (reviewer, non-author) | **Agree** | Re-opened the package candidate: "Three different mechanisms, one invariant" and "every platform's scope list is a restatement of that ownership" universalize platform-specific policy across HackerOne/CNVD/360SRC — the precise Q4 failure. Refusal confirmed. |
| staged "automatic CWE integration" subclaim (inside the staged F13 entry) | reject | `RevStagedIntent` (revenger, non-author seat) | **Agree** | S045 proves a crosswalk (`idor`→CWE-932, 36 categories, null default), not automatic program integration; the inference is refused. Role is revenger, not reviewer — recorded as supporting evidence, not as the reviewer-role re-open. |

`RevC2Registry` independently re-derived the registry rows (45, 0 malformed, 0 dup, enums clean,
mined used-by paths exist, census exit 0) and agrees with the S043–S045 additions. The
reviewer-role re-open of the admit and of one refusal is therefore on record; the Q8/Q10
disagreements are the standing entry-level defects.

### Registry changes — every change old → new, inline

- **S043 appended** (`corpus/SOURCES.md`): tier A, `mined`, `opened 2026-10-23 → 2026-10-25`,
  `recheck 90d`, `anchor` rewritten from the round-29 capture (policy_versions array, record
  3787452, sections Program Scope and Assets / DoS Reward; manifest Q1–Q4), `used-by` exactly
  `corpus/knowledge/program-severity-ladders-and-reward-scales.md`.
- **S044 appended**: tier A, `mined`, `opened 2026-10-23 → 2026-10-25`, `recheck 90d`, `anchor`
  from capture (Description lines 9–11; Data within an Entry lines 26–33; Priority lines 32–38),
  `used-by` = the F13 entry.
- **S045 appended**: tier A, `mined`, `opened 2026-10-23 → 2026-10-25`, `recheck 90d`, `anchor`
  from capture (metadata.default; content 36 top-level entries; idor/CWE-932 line 91–93; null
  nodes lines 7–8), `used-by` = the F13 entry.
- No status/recheck/used-by cell changed on any existing row; no row superseded/retired/re-titled;
  S041/S042 untouched (logged). `corpus/SOURCES.md` sha256 `e59240f8…` → `fa54ba528eadc032e3cf0cbc6f431e683b2d0d5e7bc1123dd5bb874ac92d1836` (ScribeSourcesGate; rows 42 → 45).

## Mistakes

**M29-1 · the wave re-demonstrated the M28-1 timing hazard: canonical/review seats ran before the subject landed.** Class: wave-sequencing. Evidence: `ExecCanonC2` produced a PRE-STATE C2 receipt at 18:15Z (correctly labelled, re-run named — the rule worked), and `RevC2Entry` bar-checked the F13 entry while its body was still `body stub S043 S044 S045` (631 B), returning disagree on Q1–Q10 against stub bytes; both had to be re-run/re-considered after the body landed. Captured-by: the seats' own state labels (bounds 6); no mechanism enforced the ordering. Fix: gate canon/review seats on the subject's receipt existing on disk (dispatcher-level depends-on), not on prose "runs last"; a seat whose subject is absent must wait or emit PRE-STATE and be re-dispatched by the integrator. A fix counts if the dispatcher refuses to start a canon seat before the subject receipt exists.

**M29-2 · a frozen C2 counter cannot emit the total registry row count its kill rule watches (M28-3 class).** Class: unsatisfiable instrument. Evidence: C2 predicate/kill rule say `registry rows increment 42 -> 45` / `registry rows != 45`, but counter command 2 (`grep -cE '^\|[[:space:]]*S04[3-5]…'`) emits `0 -> 3` and command 3 (`sources-census.sh validate`) emits only `census_exit` — no frozen command emits `45` (`ConnClaims` §3; `RevReceiptsCanon` H3). Captured-by: `ConnClaims` (connector). Fix: bind the row count to `sources-census.sh census --root … kasegi | awk '$1=="kasegi" && $2=="rows" {print $3}'` → 45 (measured this round), or append a claims correction naming the counter; the re-bound counter demonstrably fails on the 42-row base.

**M29-3 · Q9's occurrence/stem binding is still not enforced by the committed instrument (M28-8 carried unfixed); the C2 kill-rule clause was tripped mid-wave by the first manifest and is now satisfied only by the frozen set.** Class: criterion/implementation gap. Evidence: `source-recheck.py` prints `OK occurrences=12 anchor=MISSING` and exits 0 for a record whose stem ≠ id (S043→S045.txt, 53× quote) — reproduced by `CritC2Kill` C1; the first frozen-declared manifest `79b32d50` had S043 Q1/Q2/Q4 at `occurrences=12` (single-line 153-record array capture), tripping "any manifest assertion not occurrences=1" as written; `ExecCapS043` rev 1 replaced the capture with the record-scoped policy text and the frozen manifest `910608e6` re-anchored Q1–Q4 (31/40/170/92) — all 12 assertions now exactly-once (`RevC2Manifest` verified stems/anchors and that the three failure states fail closed only in its binding table `b7d438ef…`; a committed `corpus/instruments/check_q9.py` still does not exist). Captured-by: `RevC2Manifest` F1/F2, `RevReceiptsCanon` H3, `ConnClaims`. Fix: promote a Q9 reader into `corpus/instruments/` and make `source-recheck.py` exit 1 on stem≠id and on unanchored multi-occurrence / broken-anchor quotes; the promoted checker fails each of the three probe states (P1/P2/P3 measured).

**M29-4 · the frontier harness still crashes on an absent entry and can pass pointing at an unrelated entry (M28-5 partial).** Class: landing order / harness. Evidence: `frontier-recheck-count.py` raises an uncaught `FileNotFoundError` when an admitted row's entry is absent (CritC2Kill C2 reproduction), and a row whose entry cell names the existing F12 entry passes `entries=16 pass=16 exit=0` with zero new content. Captured-by: none (routed fix not landed). Fix: fail with a named row instead of a traceback; reject duplicate entry targets across admitted rows (same realpath twice); bind counter 2 (`grep -lE '^source: S04[3-5] '`) to the F13 row's own entry file, not any `corpus/knowledge/*.md`.

**M29-5 · S043's capture pipeline diverges from the committed instrument, and the final snapshot is a documented extraction rather than an as-served capture.** Class: instrument/source mismatch. Evidence: `capture-source.py --kind html` fetches a 128-B Cloudflare JS-disabled stub for the HackerOne policy API; the raw 1,220,741-B JSON array capture was made via the curl fallback (fetch-reproducible, not instrument-reproducible — LabC2Probe §4); the frozen S043.txt is a deterministic extraction of record 3787452's `new_policy` (204 lines / 7,298 B), whose derivation command is documented in `ExecCapS043` rev 1 but not in the entry, the capture file, or the registry row (M29-9). Captured-by: none before freeze. Fix: state the fallback command, the extraction derivation, and the non-instrument reproducibility in the entry's `## Limits` and the row's changelog; extend `capture-source.py` to an HTTP/2-capable client so a future re-capture reproduces the pinned bytes.

**M29-6 · receipt digests drifted behind the bytes between measurements (M28-12 recurrence).** Class: bookkeeping. Evidence: `ScribeReportDigest` caught an on-disk `anchorcheck.py` digest `57c5e111…` at 18:20Z whose git-free run exited 1 (`cases=12 failures=1 covered=8`); the file settled at `68e1bdc6…`; receipt digests written against intermediate bytes would have pinned a stale state. Captured-by: the report digest's cross-check. Fix: the instrument owner writes once per stage and canon seats re-hash immediately before writing the receipt; `ExecPostCommitRecheck` re-verifies at the integration commit (`git show <commit>:corpus/instruments/anchorcheck.py | sha256sum` must equal `68e1bdc6…`).

**M29-7 · `covered=9` counts a skipped limb as executed in the git-free run.** Class: overclaim in a covered metric. Evidence: the PIN-BROKEN case prints `SKIP pin-broken (git not found)` and is appended to `executed`, so `limbs=9 covered=9` is printed even though that fixture did not run (`CritC1Kill` C1; `RevC1Instrument` finding; `CritGlobal`). The frozen predicate's semantic clause "every declared verdict limb has an isolating failing fixture" is therefore only demonstrated in a git-present run. Captured-by: `RevC1Instrument`/`RevC1Controls` (non-author reviewers). Fix: track skips separately and print `limbs=9 covered=8 skipped=1` when git is absent (or exclude skipped names from `covered`); the corrected print fails on the current locked git-free output (which claims 9/9), so the fix is shown able to fail.

**M29-8 · stale round-28 peers were revived by name and wrote into round-28 wave paths.** Class: coordination/namespace. Evidence: `ScribeLessonGate`'s first coordination reply referenced `.ufo/waves/round-28/wave1/ScribeLessonGate.md` and round-28 gate content; `ExecHarnessC2` wrote its round-29 transcript to `.ufo/waves/round-28/receipts/ExecHarnessC2.txt` and `.ufo/waves/round-28/wave1/ExecHarnessC2.md`; `ExecDensityNoHarm` §5 observed `.ufo/waves/round-28/receipts/ScoutAssimilation.txt` modified during round 29. Captured-by: none (no rule covered cross-round seat identity). Fix: namespace wave identities per round (or force parked agents to exit), and have `SentScope`'s post-integration sweep check that no round-N seat wrote under `.ufo/waves/round-M` for M≠N; the sweep flags both observed files.


**M29-9 · the SOURCES S043 row cell still describes the superseded raw-array capture; the R8
changelog correction has now landed.** Class: stale cell after a capture replacement. Evidence:
`RevC2Manifest` F4 — the `corpus/SOURCES.md` S043 row cell (line 49) carries the
"policy_versions API array of 153 records; record id 3787452, timestamp …" wording, while the
frozen capture at the pinned path is the extracted record-3787452 policy text (`d3b815ed…`, 204
lines). The fix has landed: `ExecManifestC2` appended the R8 old→new change cell at
`corpus/SOURCES.md:83` (raw 153-record array → record-scoped capture; quote locations at lines
31/40/170/92), verified in the working tree. Captured-by: `RevC2Manifest` (until the fix). The
remaining residual is the derivation-command documentation gap recorded under M29-5.
## considerthese

**Proposal mined this round:** `considerthese/2026-10-25.md` **proposal 5** — keep an open-defects ledger with runnable closure checks — landed as **`corpus/QUALITY.md` R15** (Round-29 additions; ScribeConsiderthese drafted, ScribeQuality landed). Text: "A named open defect stays open only while its runnable closure check exits non-zero; every open-defect row carries its closure-check command (`bash -n`-parseable) and an evidence pointer." Grounded in this round's routed defects M28-1/3/5/6/8/12 and the open-debt list; cites `considerthese/2026-10-25.md` (2026-10-25). Evidence: `QUALITY.md` sha256 `00d4b2a3…` → `a39e0b5e2bf4631c07bd75f40209f2fc33a65c5844dca0191b51db9448ca13f9`, 83 → 89 lines, `head -83` byte-identical (R6).

Proposals-status ledger (considerthese/2026-10-25.md 1–6): 1 mined → R14 (round 28); 2 open (distance-to-next-score); 3 partially landed — the severity-tables plank is covered by C2/F13 (S043/S044/S045) though claims.json cites the package theme, SHONEN box 2 still open; 4 being mined (first ledger note is ScribeConsiderthese §1; permanent home open); **5 mined here → R15**; 6 open.

## Compliance

**Freeze discipline (R25-1, R9).** `claims.json` committed at `f28ff5d` before dispatch and never
edited in place; no erratum was needed this round. No measurement in this lesson precedes the
freeze commit; before receipts are the committed `c1-controls/before.txt`, `c2-controls/before.txt`,
`census-before.txt`.

**Ownership.** Every production path had exactly one writer: `corpus/instruments/anchorcheck.py`
(`ExecImplC1`, `68e1bdc6…`), `corpus/knowledge/program-severity-ladders-and-reward-scales.md`
(`ExecEntryF13`, `6beeedd7…`), `corpus/source-snapshots/round-29/manifest.json` (`ExecManifestC2`,
`79b32d50…`), `corpus/SOURCES.md` (`ScribeSourcesGate`), `corpus/README.md`
(`ScribeReadmeC2`), `SKILL.md` (`ScribeSkillGate`, 1035 → 1047 lines, append-only, `head -1035`
byte-identical), `corpus/QUALITY.md` (`ScribeQuality`, +R15), `corpus/instruments/knowledge-expected.txt`
(`ExecRecheckAudit`, 40 → 41 entries / 42 → 43 lines; red-before `unexpected=1 exit=1` → green
`expected=41 exit=0`), `LOG.md` (`ScribeLog`). Cross-write check: `SentScope` found no confirmed
out-of-bounds write (final post-integration sweep owed); `ExecScopeSweep` reports no fleet-root
strays.

**Census, before / after.** Before (committed): exit 0, 42 rows, W04 S028/S029 only. After
measured: exit 0, **45 rows** (tier A 42 / B 1 / C 2; mined 33, queued 9, rejected 3), W04
S028/S029 only — `ScribeSourcesGate`, `RevC2Registry`, `ExecCanonC2`, and this seat agree.

**Scope and safety.** No write to the fleet root, sibling lanes, `/home/vgpnk/Projects/shokuknow`
(read-only), lane git index, `/home/vgpnk/Projects/shokunin/.ufo/state`, or `MANIFEST.json`. Live network use: three captures
(S043 via documented curl fallback after the instrument stub) plus verification probes, all public
GETs with the instrument UA; no fixture contacted a live target.

**Tooling.** No `pacman` transaction was attempted by any seat (host-wide pause respected). This
seat installed nothing. Answering model recorded per seat in the receipts.

**Close-out ledger — what is still owed, with the command that closes it.**

1. `ExecPostCommitRecheck` at the integration commit: `git rev-parse master`; re-run the four C1
   counters and the seven C2 counters at that commit; `git show <commit>:corpus/instruments/anchorcheck.py | sha256sum`
   must equal `68e1bdc6…`; write `wave1/post-commit-recheck.txt`.
2. The committed-digest conjunct of C1's kill rule is satisfied only after (1).
3. The S043 kill-rule wording decision (occurrences=12 vs anchor binding) is the L1's: either
   accept the Q9-anchored reading (as ExecCanonC2's verdict states) or append a claims correction /
   promote `check_q9.py` (M29-3).
4. `ScribeScorecard` lands the round-29 SCORECARD section (score held 4 / 7 / 9; no move).
5. Final `SentScope` sweep after integration; refresh `receipt-index.txt` (ExecAssembleReceipts).

## Erratum (round 34) — M33-3: the `SOURCES.md` line anchors cited from this lesson are stale by +7

Appended 2026-10-26 (round 34) to `corpus/lessons/round-29.md` at lane base `014ee2d` — changed-file
scope: this file only; pre-append sha256
`78ae8080fc3653b2f7291df7fd229ff4aeccc9965db2042c1825ca1f5aa52f5b`, 263 lines. Nothing above this
block is edited (QUALITY R6/R9: append-only, every pointer re-opened against the cited revision,
base and changed-file scope named). Apparatus: **M33-3** (`corpus/lessons/round-33.md` § Mistakes),
carried open at round-33 close (`corpus/lessons/round-33.md` § Open items item 6) and still open
here.

### The citations that moved

`M29-9` (this file, `:214`) cites `corpus/SOURCES.md:83` for the R8 S043 old→new change cell, and
`corpus/lessons/round-29-verifier-spotcheck.md:74` cites the same `SOURCES.md:83` for the same
cell. At the round-29 integration commit `0ab8929` that cell sat at line 83; the round-33 six-line
append (2 registry rows at `:55`–`:56`, 1 Search-log bullet at `:75`, 3 `## Registry changes` lines
at `:98`–`:100`) carried it to line **90**. **The current pointer is `corpus/SOURCES.md:90`**;
`:83` now names the `## Registry changes` heading, not the S043 cell. The
`round-29-verifier-spotcheck.md:74` mention carries the same stale value — that file is not this
seat's write scope and stays byte-identical, so this block states the correction for both mentions.

Also re-opened: `M29-9`'s "`corpus/SOURCES.md` S043 row cell (line 49)" is **still line 49** in
today's registry (the only rows added after it are S049/S050 at `:55`/`:56`), so that pointer needs
no change.

### Current `corpus/SOURCES.md` anchors

Measured 2026-10-26T05:33Z on `corpus/SOURCES.md` at `014ee2d` (100 lines, sha256
`b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b`). Column 2 is the same file at
the round-29 integration commit, column 3 at the round-33 claims base, column 4 now:

| anchor | round-29 (`0ab8929`, 86 lines) | round-33 base (`690b69d`, 94 lines) | now (`014ee2d`, 100 lines) | drift since round-29 |
|---|---|---|---|---|
| `## Registry` | 3 | 3 | 3 | 0 |
| S043 registry row (cited as "line 49") | 49 | 49 | **49** | 0 |
| `## Paths` | 53 | 56 | 58 | +5 |
| `## Search log` | 60 | 63 | 65 | +5 |
| `## Leads (unopened)` | 70 | 74 | 77 | +7 |
| `## Registry changes` | 76 | 80 | 83 | +7 |
| S043 R8 change cell (the cited `:83`) | 83 | 87 | **90** | **+7** |

Producing command (read-only `git show`; prints line counts and every `##` heading plus the S043
change-cell line, as line numbers in file order):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
for rev in 0ab8929 690b69d 9f98488 HEAD; do
  printf '%s lines=%s ' "$rev" "$(git show $rev:corpus/SOURCES.md | wc -l)"
  git show $rev:corpus/SOURCES.md | grep -n '^## \|^Change cell old → new: the S043' | cut -d: -f1 | tr '\n' ' '
  echo
done
```

output (2026-10-26T05:33Z; column order = `## Registry`, `## Paths`, `## Search log`, `## Leads`,
`## Registry changes`, S043 change cell):

```
0ab8929 lines=86 3 53 60 70 76 83
690b69d lines=94 3 56 63 74 80 87
9f98488 lines=100 3 58 65 77 83 90
HEAD lines=100 3 58 65 77 83 90
```

### Reading rule carried forward

A `corpus/SOURCES.md:NNN` pointer filed before round 33 is off by `(current line of its target −
NNN)`: +7 for the S043 change cell today, and it moves with every append. Cite the anchor text
(`Change cell old → new: the S043 …`) or re-measure with the command above before citing a number.
The section offsets this round did not cite (`## Paths`, `## Search log`, `## Leads`) are given
above so a future pointer can be opened against this revision instead of re-derived. Post-append
digest of this file is recorded in the round-34 seat receipt
(`.ufo/waves/round-34/wave1/ExecLessonErrata.md`); `head -263` is byte-identical to the pre-append
file.
