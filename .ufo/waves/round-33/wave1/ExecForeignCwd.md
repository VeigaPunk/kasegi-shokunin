# ExecForeignCwd — Foreign-CWD Probe of the Round-33 Instruments (Round 33, Wave 1)

- **Seat**: `ExecForeignCwd` (role: `executor`, leaf member — no subagent dispatch, no background work of my own)
- **Answering model**: `opencode-go/deepseek-v4.1-flash` (workstation route; no model was passed)
- **Date**: 2026-10-26
- **Lane**: `kasegi-shokunin` — `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write scope)
- **Lane base**: `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`
- **Claims-freeze commit**: `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`
- **HEAD at probe time**: `53bfa59ff3fa578818e7e5db04fe60e80ed1eb6f` (`round-33: dispatcher ready marker, C1 erratum 1 (Rule B per-id binding ruling), l1-ref sid-url table`)
- **Judged axes**: `depth:verifiability`, `coverage`
- **Milestone**: `round-33`
- **Report target**: `.ufo/waves/round-33/wave1/ExecForeignCwd.md`
- **Environment**: `Python 3.14.8`, `Linux 7.2.11-arch1-1`

---

## 0. Scope of this seat

Four invocations, each launched with the working directory at `/` (foreign to the lane), against
`LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin`:

| # | Subject | Expected |
|---|---|---|
| P1 | the F16 entry's own `recheck:` line via `bash -c` | exit 0 |
| P2 | `python3 $LANE/corpus/instruments/capture-binding-check.py --root $LANE` | exit 0 |
| P3 | `python3 $LANE/corpus/instruments/recheck-audit.py --root $LANE --quiet` | strict pass=45/45 |
| P4 | `python3 $LANE/corpus/instruments/frontier-recheck-count.py --root $LANE` | entries=19 pass=19 |

All four passed. No lane file was written by this seat, no scratch tree was created (the seat runs
no fixtures), no `/tmp` path is cited, and no tool was installed or upgraded.

---

## 1. Bytes the probe ran on (quiescence evidence)

### 1.1a PRE-STATE, before the prerequisites landed (not cited)

Before the landing wait, the artifacts this seat probes did not exist:

```
ls: cannot access 'corpus/instruments/capture-binding-check.py': No such file or directory
ls: cannot access 'corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md': No such file or directory
corpus/source-snapshots/round-32/:
-rw-r--r-- 1 vgpnk vgpnk 20272 Oct 25 23:09 S049.txt
-rw-r--r-- 1 vgpnk vgpnk 31016 Oct 25 23:09 S050.txt
```

and the two regression instruments printed `strict pass=44/44` / `lines=44 total=44` (recheck-audit,
44 knowledge entries) and `entries=18 pass=18 exit=0` (frontier harness). Those are PRE-STATE
figures (bound 6) and are **not** comparable to the after column of §9.

### 1.1b First post-landing pass, superseded (not cited)

A first pass over the landed artifacts ran while peer seats were still editing: its subject bytes
carried `chinese-crowdsourced-testing-scope-and-rewards.md` sha256 `eebd5ea572b3…` and
`corpus/SOURCES.md` sha256 `15babfc70b89…`, both of which changed before the watch in §1.3 began
(they became `53c48b3b…` and `b22c7f01…`). That pass printed the same four verdicts as §2-§5, but it
is **superseded and not cited** — the cited numbers are the §1.3 bracketed run on quiescent bytes.

### 1.2 Landing wait (bound 9, cap 30 min)

```
for i in $(seq 1 74); do ok=1
  [ -s corpus/instruments/capture-binding-check.py ] || ok=0
  [ -s corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ] || ok=0
  [ -s corpus/source-snapshots/round-32/manifest.json ] || ok=0
  grep -qE '^\|[[:space:]]*S049[[:space:]]*\|' corpus/SOURCES.md || ok=0
  grep -q 'chinese-crowdsourced-testing-scope-and-rewards' corpus/instruments/knowledge-expected.txt || ok=0
  [ "$ok" = 1 ] && { echo "READY after $((i*20))s"; break; }; sleep 20; done
```

```
READY after 620s
state: cb=yes entry=yes m32=yes s049=1 expected=47
-rwxr-xr-x 1 vgpnk vgpnk 21527 Oct 26 01:23 corpus/instruments/capture-binding-check.py
-rw-r--r-- 1 vgpnk vgpnk  5753 Oct 26 01:18 corpus/source-snapshots/round-32/manifest.json
```

### 1.3 Byte-stability watch

An 180 s two-read watch caught a mid-wave edit (`SOURCES.md` `15babfc7…` → `b22c7f01…`, and the
F16 entry body changed after the PRE-STATE pass), then a 60 s two-read watch returned
`STABLE after 60s of watch (2 identical reads 60s apart)`. The probe was run inside a single call
bracketed by `sha256sum` before and after; the F16 entry body then changed once more
(`53c48b3b…` → `1f7ac0a2…`), so the bracket was repeated on the final bytes. **Both bracketed runs
have identical pre- and post-hashes, and both produced the verdicts in §2-§5.** The cited set is the
second (final) bracket:

```
=== pre-hashes ===
1f7ac0a2c39a0fbfdbee2ecbe112316dfc1bf7095b18cb8fb4eb9d6dfce171d1  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9  corpus/instruments/capture-binding-check.py
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774  corpus/source-snapshots/round-32/manifest.json
b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b  corpus/SOURCES.md
3779e77f07a2d76119a074f598389d35353e01a4651cec8c75201c770f754932  corpus/README.md
3f68b9a2ff7db654770bc11cb3b178b3d2920cc8e5ca0ba9761d85a65ab81ceb  corpus/instruments/knowledge-expected.txt
=== post-hashes ===   (identical to pre-hashes; diff empty)
```

The earlier (superseded) bracket carried entry sha256 `53c48b3b322aa4e5f90e1bae27ad0c1fb60c3452b2cff1e35a52e3276bb60a48`
with the other seven hashes already at their final values. The entry's `source:` lines (S049 line 3,
S050 line 4) and its `recheck:` line (line 7) are textually identical across all three body versions;
only the prose body moved.

Probe-time `git hash-object` for the same paths, and the HEAD state:

```
53bfa59 round-33: dispatcher ready marker, C1 erratum 1 (Rule B per-id binding ruling), l1-ref sid-url table
a6a5023 round-33: wave-1 spec (64 seats, v2 policy), validated plan and dispatch
6e55c8d round-33: freeze claims C1/C2 with do-nothing controls, census-before, assimilation guard, watch-dog digest, LOG r32 entry (D1)

corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md wt=77e0681116b77852b900080641a9d5c8d58c4fb2 head=ABSENT-AT-HEAD
corpus/instruments/capture-binding-check.py                      wt=41fea75a9494354f3f4a3e6a641d737d6ff5edfe head=ABSENT-AT-HEAD
corpus/source-snapshots/round-32/manifest.json                   wt=10961dc9a2442c3c9d33f48c67c42837456be9b0 head=ABSENT-AT-HEAD
corpus/SOURCES.md                                               wt=198b2bc53345fd0af38bfdf5c9f4284c6337bc47 head=9b906580c50cc3ed236fbee7a5d5fd7b8e6e4024
corpus/README.md                                                wt=785ec2245c540027fb3c987b849ca7cf0a882890 head=dc9c20771c308e51d215a838d857cbdcd0d47e2f
corpus/instruments/knowledge-expected.txt                       wt=3de1652a9088d2d0e2063b75f4ff0d82b085c0aa head=9471c496fc34f7421e8193669d077b1ef4b31408
```

Read: the probed subject is the **uncommitted working tree** at HEAD `53bfa59` — the three new
artifacts are `??`/absent at HEAD and the three edited files differ from their HEAD blobs. These are
the bytes the L1 will commit through the lane helper; this receipt binds to the sha256 set in §1.3,
not to a commit id.

Landed peer receipts the probe post-dates (existence check only):

```
-rw-r--r-- 1 vgpnk vgpnk 17675 Oct 26 01:29 .ufo/waves/round-33/wave1/ExecCaptureBinding.md
-rw-r--r-- 1 vgpnk vgpnk 19836 Oct 26 01:29 .ufo/waves/round-33/wave1/ExecEntryF16.md
-rw-r--r-- 1 vgpnk vgpnk 10479 Oct 26 01:25 .ufo/waves/round-33/wave1/ExecManifest32.md
-rw-r--r-- 1 vgpnk vgpnk 15638 Oct 26 01:24 .ufo/waves/round-33/wave1/ExecManifestUpgrade.md
-rw-r--r-- 1 vgpnk vgpnk 22560 Oct 26 01:29 .ufo/waves/round-33/wave1/ExecRegistryAppend.md
```

---

## 2. P1 — F16 entry `recheck:` line, `bash -c`, cwd `/`

Command (launched from `/`; `LINE` is the entry's line 7, stripped of its `recheck:` prefix exactly
as `recheck-audit.py` strips it):

```
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin; cd /; pwd
LINE=$(grep -m1 '^recheck:' $LANE/corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md | sed 's/^recheck:[[:space:]]*//')
bash -c "$LINE"; echo "probe1_exit=$?"
```

Output:

```
/
LINE=cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050   # 14 assertions on the round-32 manifest (S049 Q1-Q8, S050 Q1-Q6), each `occurrences=1` under source-recheck.py's declared normalization; the strings marked hand-measured below are not manifest-bound; a captured-source comparison, not a fresh network verification
S049:sha256 OK
S049:Q1 OK occurrences=1
S049:Q2 OK occurrences=1
S049:Q3 OK occurrences=1
S049:Q4 OK occurrences=1
S049:Q5 OK occurrences=1
S049:Q6 OK occurrences=1
S049:Q7 OK occurrences=1
S049:Q8 OK occurrences=1
S050:sha256 OK
S050:Q1 OK occurrences=1
S050:Q2 OK occurrences=1
S050:Q3 OK occurrences=1
S050:Q4 OK occurrences=1
S050:Q5 OK occurrences=1
S050:Q6 OK occurrences=1
probe1_exit=0
```

**Verdict: exit 0, as expected.** 14 assertions reported (S049 Q1-Q8, S050 Q1-Q6) plus 2 sha256
lines; every assertion line reads `occurrences=1`. The line's own `cd $LANE &&` prefix is what makes
it cwd-independent from `/`; the trailing `#` comment rides on the last command and does not change
the exit status (it is the S050 invocation's exit that `bash -c` returns).

---

## 3. P2 — `capture-binding-check.py --root $LANE`, cwd `/`

Command:

```
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin; cd /; pwd
python3 $LANE/corpus/instruments/capture-binding-check.py --root $LANE; echo "probe2_exit=$?"
```

Output:

```
/
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
probe2_exit=0
```

**Verdict: exit 0, summary exactly `records=40 bound=40 unbound=0`, as expected.** Distribution
matches the frozen C1 predicate on these bytes: 9 snapshot dirs = 9 manifest dirs (rule A clean,
`missing_manifest=0`), 40 records all carrying a `url` (rule B), 38 archival + 2 `fetched_utc`
(rule C; the 2 are the round-32 records, `archival=0` there so no exemption).

---

## 4. P3 — `recheck-audit.py --root $LANE --quiet`, cwd `/`

Command:

```
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin; cd /; pwd
python3 $LANE/corpus/instruments/recheck-audit.py --root $LANE --quiet; echo "probe3_exit=$?"
```

Output:

```
/
strict pass=45/45 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=21 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=45 total=45 pass=45 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=45 missing=0 unexpected=0 exit=0
probe3_exit=0
```

**Verdict: exit 0, strict `pass=45/45`, as expected.** `executes=21` is the base's 20 plus the new
F16 entry (its line executes rather than fails closed); `gated=24` unchanged; `expect=present
expected=45 missing=0 unexpected=0` means the expected-entry list (`ExecExpectedList`) already covers
the new file. `cwd_fail=0` is the limb this seat exists to probe: the audit runs each line from both
the lane root and `/` and compares exit code **and** output digest.

---

## 5. P4 — `frontier-recheck-count.py --root $LANE`, cwd `/`

Command:

```
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin; cd /; pwd
python3 $LANE/corpus/instruments/frontier-recheck-count.py --root $LANE; echo "probe4_exit=$?"
```

Output (F01-F15 rows identical to the round-32 set; F16 row is new):

```
/
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
entries=19 pass=19 exit=0
probe4_exit=0
```

**Verdict: exit 0, `entries=19 pass=19`, and `PASS F16 ids=S049,S050` present, as expected.** This
is the C2 harness line on the landed bytes, measured from `/`.

---

## 6. Determinism and second foreign cwd (supplementary)

Two consecutive runs of the two output-heavy instruments produce byte-identical stdout
(output digests, not run digests):

```
python3 $LANE/corpus/instruments/capture-binding-check.py --root $LANE | sha256sum
1861fec846ca9a5c0e1a7a54591888896fb2c4f2ab89255c640e46eda3c5a9f1  -
python3 $LANE/corpus/instruments/capture-binding-check.py --root $LANE | sha256sum
1861fec846ca9a5c0e1a7a54591888896fb2c4f2ab89255c640e46eda3c5a9f1  -
python3 $LANE/corpus/instruments/frontier-recheck-count.py --root $LANE | sha256sum
18a19fef7ce4fef7f80adb5bae7424129fa2a9f6435297ff8f7fc794ff0e14d3  -
python3 $LANE/corpus/instruments/frontier-recheck-count.py --root $LANE | sha256sum
18a19fef7ce4fef7f80adb5bae7424129fa2a9f6435297ff8f7fc794ff0e14d3  -
```

Same three instruments from a **second** foreign cwd (`/usr`), on the same bytes:

```
/usr
records=40 bound=40 unbound=0
cb_from_usr_exit=0
strict pass=45/45 cdroot_fail=0 instrument_fail=0 own_fail=0
entries=19 pass=19 exit=0
```

No `--root`-relative path leaked into the instruments' behaviour: the three instruments read only
under `--root`, so `/` and `/usr` agree. (`recheck-audit.py` additionally *executes* each entry line
from both `--root` and `--foreign` (default `/`) and compares exit code plus output digest; the
`cwd_fail=0` in §4 is that comparison passing for all 45 entries.)

---

## 7. Observation carried for the L1 (not a verdict)

`capture-binding-check.py` prints `multi_row_url=2` on the AUDIT line while exiting 0. The
instrument's own docstring makes this informational, not a rule-B failure: rule B is id-scoped
(claims-erratum-1, HEAD `53bfa59`), so a record must bind to **its own** row byte-exactly, and a URL
that also appears in a different row is only counted. The two records behind the count are the
registry's pre-existing duplicate-URL pairs:

```
MULTI_ROW record=S029 own_row=True also_rows=['S024', 'S029']
MULTI_ROW record=S006 own_row=True also_rows=['S006', 'S028']
```

(computed read-only from `corpus/source-snapshots/*/manifest.json` `url` fields against the
`https://` tokens in the `| S0xx |` source cells of `corpus/SOURCES.md`). The four registry rows, at
`corpus/SOURCES.md` lines 12/30/34/35:

```
| S006 | HackerOne Safe Harbor Overview and FAQ — https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq | ...
| S024 | Regulation (EU) 2024/2847, Cyber Resilience Act — https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng | ...
| S028 | HackerOne Safe Harbor Overview and FAQ, duplicate-row proposal — https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq | ...
| S029 | Regulation (EU) 2024/2847, CRA manufacturer reporting clocks — https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng | ...
```

Both records show `own_row=True`, so this seat records the fact and leaves the claim-reading question
(the C1 predicate sentence's "matches exactly one registry-row URL" phrasing vs. the erratum-1
id-scoped reading) to the critics and the L1. This is the base W04 duplicate-URL pair already present
in `census-before.txt`; it is not a round-33 regression.

---

## 8. Bounds and no-write proof

- **No lane mutation.** Read-only git only: `git rev-parse`, `git log`, `git status`, `git hash-object`.
  No `git`/`jj` mutation of any kind in the lane; no commit, add, stash, checkout, reset, pull, push.
  `git status --porcelain corpus/` stayed at the same 16 entries throughout (13 `M` + 3 `??`):
  `QUALITY.md`, `README.md`, `SOURCES.md`, `instruments/README.md`, `instruments/knowledge-expected.txt`,
  the eight legacy `manifest.json`s (`round-23,24,25,26,28,29,30,31`), and `??` = `capture-binding-check.py`,
  `knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`, `source-snapshots/round-32/manifest.json`.
  Final `git status --porcelain` sha256: `346ae19949cd2ec1c201c80f3db8dd6b9bed61e5bc2f41ad1a98ffdebd8f78b5`.
  Nothing in `corpus/` changed between the §1.3 pre-hashes and post-hashes, so running the four
  instruments wrote no file.
- **No scratch tree.** This seat runs no fixtures and takes no clone/worktree, so
  `$HYAKU_SCRATCH/kasegi-r33/ExecForeignCwd/` was never created; a seat ending with a tree on disk
  is a self-reported defect, and there is none. No `/tmp` path appears in this receipt.
- **No fixtures, no network.** I did not fetch any URL, contact any bounty target, or run
  `--selftest` (owned by `CritC1Kill`). No credential material, session URL, or vault reference is
  reproduced here; the S049 capture was never opened by this seat.
- **No tooling change.** No install, upgrade, or host-service interaction; `pacman` untouched.
  Nothing to record under the 2026-10-19 tool-install directive.
- **Scope.** Wrote exactly one file: `.ufo/waves/round-33/wave1/ExecForeignCwd.md`. No peer file, no
  `claims.json`, no `c1-controls/`, `c2-controls/`, `LOG.md`, `SCORECARD.md`, or report.

---

## 9. Result

| Probe | Command (cwd `/`) | Expected | Observed | Status |
|---|---|---|---|---|
| P1 | `bash -c "<F16 recheck: line>"` | exit 0 | exit 0, 14 × `occurrences=1`, 2 × `sha256 OK` | **PASS** |
| P2 | `python3 $LANE/corpus/instruments/capture-binding-check.py --root $LANE` | exit 0 | exit 0, `records=40 bound=40 unbound=0` | **PASS** |
| P3 | `python3 $LANE/corpus/instruments/recheck-audit.py --root $LANE --quiet` | strict pass=45/45 | exit 0, `strict pass=45/45`, `cwd_fail=0` | **PASS** |
| P4 | `python3 $LANE/corpus/instruments/frontier-recheck-count.py --root $LANE` | entries=19 pass=19 | exit 0, `entries=19 pass=19`, `PASS F16 ids=S049,S050` | **PASS** |

All four invocations are cwd-independent on the §1.3 byte set. **Risks / blockers: none from this
seat.** Two things the integrating parent should note: (a) the cited numbers are working-tree bytes
at HEAD `53bfa59`, since the wave artifacts are still uncommitted — re-run P1-P4 on the post-commit
bytes if any seat edits the F16 entry, `corpus/SOURCES.md`, `corpus/README.md`, or
`knowledge-expected.txt` after this receipt (P3 and P4 both read those files, so a late scribe append
to README invalidates P4's after column unless re-run); (b) the §7 `multi_row_url=2` observation is
informational under the instrument's documented rule B and needs no action from this seat.
