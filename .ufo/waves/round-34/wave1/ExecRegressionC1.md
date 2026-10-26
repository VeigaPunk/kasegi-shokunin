# ExecRegressionC1 — final C1 regression at quiescent tip bytes (round 34)

- seat: `ExecRegressionC1` (executor, leaf of the L2 wave; no dispatch, no commit)
- lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- lane base: `014ee2d7aa8c3c095ff57ae51097606a9906228c`; claims-freeze commit `29f606dbdd28aff6fd4573ab4b90788bbb90af13`
- `HEAD` at measurement: `206e5108f1190e61b3e2622d21cab8a5d921650c` (wave-1 spec/dispatch commit); round-34 work is in the working tree, uncommitted by design
- measured at: `2026-10-26T06:16:16Z` … `06:16:29Z`
- quiescence envelope (input digest identical before/after the run and from `06:04:29Z`): `6ed34f484f0f68d2ac9c02d928ea694d74cf5eddcd7c87dc8be27d1cc9ba346a`

## Report

### 0. Measurement state and quiescence

The six frozen C1 counting commands were run from the lane root, in this order, twice (the two
non-trivially deterministic ones plus the suite were run a second time immediately; diff shown in
§1). The input digest covers every file the six commands read: `corpus/**/*` (instruments,
snapshots, manifests, `SOURCES.md`, `README.md`, `knowledge/`, `lessons/`), `SCORECARD.md`,
`QUALITY.md`, `SKILL.md`, and the round-34 wave-root files (`claims.json`, `claims-erratum-1.md`,
`c2-controls/`, `c1-controls/`). It was computed by `find … -printf '%T@ %s %p' | sort | sha256sum`
inside the lane. Evidence of quiescence (watcher log, 20 s polls):

```
06:04:29Z poll=50 inp=75db4e8fa569e82ef3ecd5a98159bad5ee158ecae885d56d4cbc6868cc244579
06:04:49Z poll=51 inp=6ed34f484f0f68d2ac9c02d928ea694d74cf5eddcd7c87dc8be27d1cc9ba346a
...
06:16:09Z poll=85 inp=6ed34f484f0f68d2ac9c02d928ea694d74cf5eddcd7c87dc8be27d1cc9ba346a   (deadline)
inp_before(06:16:16Z)=6ed34f484f0f68d2ac9c02d928ea694d74cf5eddcd7c87dc8be27d1cc9ba346a
inp_after (06:16:29Z)=6ed34f484f0f68d2ac9c02d928ea694d74cf5eddcd7c87dc8be27d1cc9ba346a
```

`wave1/*.md` receipts were still being written after this point (65 receipt files present from
`06:10:29Z`); no receipt is read by any of the six commands, so that churn does not move a C1
value. Earlier in the wait the same seat observed the C1 inputs moving (see §6.2); those
intermediate bytes are reported there, not here.

Working-tree state at measurement (`git status --porcelain=v1`; `M` = modified vs `HEAD`, `??` =
new in the working-copy commit):

```
 M .ufo/waves/round-33/wave1/ScribeReportDraft.md
 M SCORECARD.md
 M SHONEN.md
 M corpus/QUALITY.md
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/instruments/README.md
 M corpus/instruments/capture-binding-check.py
 M corpus/instruments/frontier-recheck-count.py
 M corpus/lessons/round-29.md
 M corpus/lessons/round-33.md
 M corpus/source-snapshots/round-26/manifest.json
 M corpus/source-snapshots/round-32/manifest.json
?? .ufo/waves/round-34/assimilation/
?? .ufo/waves/round-34/claims-erratum-1.md
?? .ufo/waves/round-34/wave1.ready
?? .ufo/waves/round-34/wave1.ready.dispatched
?? .ufo/waves/round-34/wave1/
?? corpus/instruments/kill-rule-check.py
?? corpus/instruments/r-defect-closure.sh
?? corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
?? corpus/lessons/round-34.md
?? corpus/source-snapshots/round-34/
```

Digests of every measured file (bytes/lines measured by `wc`):

| file | sha256 | size | lines |
|---|---|---|---|
| `corpus/instruments/r-defect-closure.sh` | `809aaf9078a2c788c2aec29afd23db251f46c4c0c7e0be5caa7a381ac34d567d` | 35971 | 832 |
| `corpus/instruments/capture-binding-check.py` | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` | 40556 | 892 |
| `corpus/instruments/kill-rule-check.py` | `c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61` | 43138 | 881 |
| `corpus/instruments/frontier-recheck-count.py` | `1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249` | — | — |
| `SCORECARD.md` | `efa646c83baead97e41d9ccad65fac9a4d8468f6bb8af956446d347d68237e91` | 137665 | — |
| `corpus/QUALITY.md` | `77d99df9abf57a66065dbe927ce95f0ddf8acbfba237fefd163bdd3871751af8` | 30340 | — |
| `corpus/lessons/round-33.md` | `f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807` | 49907 | — |
| `corpus/source-snapshots/round-32/manifest.json` | `72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6` | 6138 | — |
| `corpus/source-snapshots/round-26/manifest.json` | `33ac33c3caa6d43f3772b8cf8532b37cdb50f48db8ba667b5dd90645e8eacefa` | 4864 | — |
| `.ufo/waves/round-34/c2-controls/junk-f17.md` | `2752a994265a1e284ebd236730d169d677e1923cfb7073cf79ad874d19bc4026` | — | — |
| `corpus/source-snapshots/round-34/S051.txt` | `4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5` | 8502 | 175 |

`.ufo/waves/round-34/c2-controls/junk-f17.md` is in `HEAD`: `git cat-file -e 206e510:.ufo/waves/round-34/c2-controls/junk-f17.md` → exit 0 (`git ls-files` lists `before.txt`, `junk-checker.py`, `junk-f17.md`). The two new instruments, the round-34 snapshot manifest and the F17 entry are working-tree files (`git cat-file -e 206e510:<path>` → exit 128 each), i.e. the L1 commits them.

### 1. The six frozen C1 counting commands — verbatim

Run from the lane root; `CMD<n>_exit` is the command's own exit status.

```
===== [CMD1] $ bash corpus/instruments/r-defect-closure.sh
R1 check=SCORECARD.md lane-hash-markers=0 + appended 'Correction (round 34)' naming 7963976e/014ee2d open=0
R2 check=SCORECARD.md round-33 'Erratum 2' per-id restatement + QUALITY.md R22 pre-freeze step open=0
R3 check=QUALITY.md appended round-34 note below R20 (per-id supersedes 'exactly one') open=0
R4 check=tightened kill rule recorded (R24 row: kill rule + one 'selftest case=' line per case) + round-33 lesson R4 3-of-4 erratum open=0
R5 check=capture-binding-check.py url-matching-two-rows=0 cases=21 (>=11) open=0
R6 check=round-26 manifest binds S040-live.txt (record or orphan list) + purpose corrected open=0
R7 check=round-33 lesson appended R7 erratum (19->31, 23->22 characters, S050.txt:70) open=0
R8 check=round-32 manifest fetched_utc is a real strict-UTC instant (date-T time Z, zero offset), no '-' offset open=0
R9 check=capture-binding H4-H8 cases=9 + frontier rule A bidirectional (mirror=0 reverse=1) + junk=.ufo/waves/round-34/c2-controls/junk-f17.md open=0
closed=9/9 exit=0
CMD1_exit=0
```

```
===== [CMD2] $ bash corpus/instruments/r-defect-closure.sh --selftest
selftest case=R1 live=pass fixture=rejected control=absent verdict=pass
selftest case=R2 live=pass fixture=rejected control=absent verdict=pass
selftest case=R3 live=pass fixture=rejected control=absent verdict=pass
selftest case=R4 live=pass fixture=rejected control=absent verdict=pass
selftest case=R5 live=pass fixture=rejected control=absent verdict=pass
selftest case=R6 live=pass fixture=rejected control=absent verdict=pass
selftest case=R7 live=pass fixture=rejected control=absent verdict=pass
selftest case=R8 live=pass fixture=rejected control=pass verdict=pass
selftest case=R9 live=pass fixture=rejected control=absent verdict=pass
selftest cases=9 failures=0
selftest judge=forged-summary rejected=1
selftest judge=short-report rejected=1
selftest judge=complete-report accepted=1
CMD2_exit=0
```

```
===== [CMD3] $ python3 corpus/instruments/capture-binding-check.py --selftest
selftest case=clean-all-pass exit=0 want=0 verdict=pass
selftest case=missing-manifest-dir exit=1 want=1 verdict=pass
selftest case=record-without-url exit=1 want=1 verdict=pass
selftest case=shared-url-between-two-records exit=0 want=0 verdict=pass
selftest case=duplicate-id-rows exit=1 want=1 verdict=pass
selftest case=url-mismatch exit=1 want=1 verdict=pass
selftest case=no-row exit=1 want=1 verdict=pass
selftest case=shared-url-not-a-failure exit=0 want=0 verdict=pass
selftest case=round-32-record-without-fetched_utc exit=1 want=1 verdict=pass
selftest case=pre-round-32-record-without-archival exit=1 want=1 verdict=pass
selftest case=round-32-record-with-fetched_utc-passes exit=0 want=0 verdict=pass
selftest case=pre-round-32-archival-passes exit=0 want=0 verdict=pass
selftest case=fetched-utc-pending-rejected exit=1 want=1 verdict=pass
selftest case=fetched-utc-local-offset-rejected exit=1 want=1 verdict=pass
selftest case=per-file-orphan-detected exit=1 want=1 verdict=pass
selftest case=per-file-orphan-listed exit=0 want=0 verdict=pass
selftest case=nested-snapshot-dir exit=0 want=0 verdict=pass
selftest case=nested-snapshot-missing-manifest exit=1 want=1 verdict=pass
selftest case=dup-record-in-manifest exit=1 want=1 verdict=pass
selftest case=double-https-row exit=1 want=1 verdict=pass
selftest case=rejected-row-anchor exit=1 want=1 verdict=pass
selftest case=summary-only-selftest-rejected exit=1 want=1 verdict=pass
selftest case=complete-selftest-report-accepted exit=0 want=0 verdict=pass
selftest cases=23 failures=0
CMD3_exit=0
```

```
===== [CMD4] $ python3 corpus/instruments/kill-rule-check.py
KILL-RULE instrument=corpus/instruments/capture-binding-check.py sha256=3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa bytes=40556 lines=892 floor=19 counter_sha256=c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61
probe selftest-shape pristine=pass exit=0
probe record-without-url pristine=pass exit=1
probe per-file-orphan pristine=pass exit=1
probe unnamed-record-id pristine=pass exit=1
probe stale-orphan-declaration pristine=pass exit=1
probe malformed-fetched-utc pristine=pass exit=1
probe punctuated-url-cell pristine=pass exit=0
probe malformed-orphan-declaration pristine=pass exit=2
probe nested-legacy-round pristine=pass exit=0
pristine selftest cases=23 case-lines=23 floor=19 floor_met=1
mutant-patch name=skip-selftest-summary patch_sha256=c457083e5d99f9f0 find_sha256=e6262244cffa1e1e find_count=1 status=ok
mutant-bytes name=skip-selftest-summary pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=b9d40dbee7521dbd
mutant-probe name=skip-selftest-summary probe=selftest-shape pristine=pass mutant=fail exit=0 reasons=summary-only;case-set-mismatch
mutant-probe name=skip-selftest-summary probe=record-without-url pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=per-file-orphan pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=punctuated-url-cell pristine=pass mutant=pass exit=0
mutant-probe name=skip-selftest-summary probe=malformed-orphan-declaration pristine=pass mutant=pass exit=2
mutant-probe name=skip-selftest-summary probe=nested-legacy-round pristine=pass mutant=pass exit=0
mutant=skip-selftest-summary killed=1
mutant-patch name=accept-record-without-url patch_sha256=83cbd622ad2fd1e2 find_sha256=cbf461982c746e9d find_count=1 status=ok
mutant-bytes name=accept-record-without-url pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=5897a1f044bcbf3f
mutant-probe name=accept-record-without-url probe=selftest-shape pristine=pass mutant=fail exit=1 reasons=exit=1;failures=1;case-verdict
mutant-probe name=accept-record-without-url probe=record-without-url pristine=pass mutant=fail exit=0 reasons=exit=0 want=1;missing='detail=absent';missing='unbound=1'
mutant-probe name=accept-record-without-url probe=per-file-orphan pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=punctuated-url-cell pristine=pass mutant=pass exit=0
mutant-probe name=accept-record-without-url probe=malformed-orphan-declaration pristine=pass mutant=pass exit=2
mutant-probe name=accept-record-without-url probe=nested-legacy-round pristine=pass mutant=pass exit=0
mutant=accept-record-without-url killed=1
mutant-patch name=per-file-binding-removal patch_sha256=f872ef12408d9162 find_sha256=f1a44079b9477ef2 find_count=1 status=ok
mutant-bytes name=per-file-binding-removal pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=616ce9dd0637a23b
mutant-probe name=per-file-binding-removal probe=selftest-shape pristine=pass mutant=fail exit=1 reasons=exit=1;failures=2;case-verdict
mutant-probe name=per-file-binding-removal probe=record-without-url pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=per-file-orphan pristine=pass mutant=fail exit=0 reasons=exit=0 want=1;missing='rule=orphan-capture';missing='orphans=1 orphan=S009.txt'
mutant-probe name=per-file-binding-removal probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=punctuated-url-cell pristine=pass mutant=pass exit=0
mutant-probe name=per-file-binding-removal probe=malformed-orphan-declaration pristine=pass mutant=pass exit=2
mutant-probe name=per-file-binding-removal probe=nested-legacy-round pristine=pass mutant=pass exit=0
mutant=per-file-binding-removal killed=1
control=CTL-noop verdict=invalid:noop expect=invalid:noop ok=1
control=CTL-nocompile verdict=invalid:nocompile expect=invalid:nocompile ok=1
control=CTL-equivalent verdict=survivor expect=survivor ok=1 witness_survivors=1 witness_exit=1
control=CTL-fake-killrule verdict=opaque expect=opaque ok=1 fake=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-34/c1-controls/fake-killrule.py fake_exit=0 fake_mutant_lines=0 fake_patch_digests=0 fake_mutants_line=0 fake_survivors=0 real_mutant_lines=3 witness_survivors=1 differs=1 stable=1
controls=4 rejected=4
GATE ok name=named-rows
GATE ok name=pristine-selftest
GATE ok name=pristine-fixtures
GATE ok name=pristine-determinism
GATE ok name=rows-valid
GATE ok name=controls
GATE ok name=survivors-zero
mutants=3 killed=3 survivors=0 invalid=0
gates=7 failed=0
survivors=0
CMD4_exit=0
```

```
===== [CMD5] $ grep -c <LANE_HASH> SCORECARD.md
0
CMD5_exit=1
```

`grep -c` exits 1 when the count is zero; the claimed value is the count (`0`), and the exit status
is grep's no-match status, not a counter failure.

```
===== [CMD6] $ python3 corpus/instruments/capture-binding-check.py
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=41 bound=41 unbound=0
CMD6_exit=0
```

Repeat run of CMD1/CMD3/CMD6 immediately after the first pass, diffed against the first output:

```
CMD1.run2_exit=0
CMD1.run2=identical
CMD3.run2_exit=0
CMD3.run2=identical
CMD6.run2_exit=0
CMD6.run2=identical
```

CMD2 and CMD4 were additionally re-run during the wait (§6.2); at the measured bytes their
decisive lines were identical (`cases=9 failures=0`; `survivors=0`), and the whole six-command
block above is one unbroken run at the quiescent digest.

### 2. Comparison to the frozen `counting_commands` literals (claims.json C1)

| # | frozen counting command | frozen literal | observed | verdict |
|---|---|---|---|---|
| 1 | `bash corpus/instruments/r-defect-closure.sh` | `closed=9/9 exit=0` | `closed=9/9 exit=0` | **match** |
| 2 | `bash corpus/instruments/r-defect-closure.sh --selftest` | `cases=9 failures=0` exit 0 | `selftest cases=9 failures=0`, `CMD2_exit=0` | **match** |
| 3 | `python3 corpus/instruments/capture-binding-check.py --selftest` | `selftest cases=N failures=0` (N>=19) | `selftest cases=23 failures=0`, exit 0 | **match** (N=23) |
| 4 | `python3 corpus/instruments/kill-rule-check.py` | `survivors=K` | `survivors=0`, `mutants=3 killed=3`, `gates=7 failed=0`, exit 0 | **match** |
| 5 | `grep -c '<LANE_HASH>' SCORECARD.md` | `0` | `0` (grep exit 1 = no match) | **match** |
| 6 | `python3 corpus/instruments/capture-binding-check.py` | `records=40 bound=40 unbound=0 exit=0` | `records=41 bound=41 unbound=0`, `CMD6_exit=0` | **numeric mismatch (40→41); invariant match** |

On command 6: the frozen literal `records=40` is a round-33 snapshot count, not the invariant.
The landed tree adds one record (`MANIFEST round-34 records=1`, `S051`, capture sha
`4fd8ed98…`), so the audit enumerates 41; every record binds (`bound=41`, `unbound=0`,
`missing_manifest=0`) and the run exits 0. This is disclosed and ruled by the L1 before any seat
scored: `.ufo/waves/round-34/claims-erratum-1.md` ("the landed record count is 41 … the measured
after-state … `records=41 bound=41 unbound=0 exit=0`"). The same reading is independently recorded
at `wave1/ConnCrossCheck.md:83-84` and `wave1/CritOverclaim.md:194-197`. No other frozen literal
moved.

### 3. Comparison to the C1 `after` list in claims.json

| after item | observed evidence | verdict |
|---|---|---|
| `r-defect-closure.sh` exists; `closed=9/9 exit=0`; `--selftest cases=9 failures=0` | §1 CMD1/CMD2; suite `809aaf90…`, 832 lines | **met** |
| `capture-binding-check --selftest` `cases=N>=19`, incl. the nine named cases | §1 CMD3: 23 cases, and each named case present — `per-file-orphan-detected`, `per-file-orphan-listed`, `nested-snapshot-dir`, `fetched-utc-pending-rejected`, `fetched-utc-local-offset-rejected`, `dup-record-in-manifest`, `double-https-row`, `rejected-row-anchor`, `summary-only-selftest-rejected` | **met** |
| `kill-rule-check.py survivors=0` (skip-selftest and accept-record-without-url killed) | §1 CMD4: `survivors=0`; `mutant=skip-selftest-summary killed=1`; `mutant=accept-record-without-url killed=1`; plus `per-file-binding-removal killed=1`; `controls=4 rejected=4` | **met** |
| `SCORECARD.md` `<LANE_HASH>` count 0 + appended correction naming `7963976e`/`014ee2d` | CMD5 = 0; `SCORECARD.md:1116` "Correction (round 34): the two lane-hash placeholders above (R1) were replaced with the round-33 final hash `7963976e…` (lane tip `014ee2d…`)" | **met** |
| erratum 2 appended + pre-freeze satisfiability step recorded | `SCORECARD.md:1014` "**Erratum 2, disclosed (round-34 append, round-25 form).**"; `SCORECARD.md:1028` "**Pre-freeze satisfiability step, recorded (QUALITY R22).**"; rule row `corpus/QUALITY.md:226` (`R22`); `R2 check=… open=0` | **met** |
| `QUALITY.md` appended note below R20 (per-id supersedes "exactly one") | `corpus/QUALITY.md:220` "Note (round 34): R20's 'exactly one registry-row URL' reading is superseded by the C1 erratum-2 per-id reading…"; R20 text itself byte-identical (R6 form) | **met** |
| round-33 lesson carries the R7 erratum (31/22 char counts, `S050.txt:70`) | `corpus/lessons/round-33.md:140` heading "Erratum (round 34) — R7…"; §(a) corrects 19→31 and 23→22; §(b) corrects the sentence cite to `S050.txt:70`. Reproduced the counts with the erratum's own command: `printf '%s' '众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。' \| wc -m` → `31`; `printf '%s' '未纳入安全服务的资产一般情况下不收录相关漏洞' \| wc -m` → `22` | **met** |
| round-32 manifest carries only strict-UTC `fetched_utc` | §5(a): S049 `2026-10-26T04:16:06Z`, S050 `2026-10-26T04:16:16Z`, `non_strict_utc= []` over 2 records | **met** |
| `S040-live.txt` has a manifest record or explicit orphan listing; round-26 purpose corrected | §5(e): CMD6 `orphans=1 orphan=S040-live.txt`; `corpus/source-snapshots/round-26/manifest.json` `orphans=[{"path":"S040-live.txt",…}]`, and the purpose now says "This manifest accounts for exactly the two files committed in this directory … (2) S040-live.txt has no `sources` record and is declared in the top-level `orphans` list below: 33463 B, 503 lines, sha256 b7f7b55f…" | **met** |
| `frontier-recheck-count.py` rule A enforces both directions | §5(f): `selftest cases=6 failures=0` with separate cases `selection-not-declared`, `header-source-not-rechecked`, `evidence-declared-not-rechecked`, `selection-neither-declared-nor-mentioned`; plain run `entries=20 pass=20 exit=0` | **met** |
| junk twin committed under `c2-controls/` and rejected | §5(g): twin at `HEAD` (`git cat-file -e 206e510:.ufo/…/junk-f17.md` → 0); fabricated sentence absent from `corpus/` (0 files) and from `S051.txt` (0 hits); rejection via a twin-derived manifest on the real `S051.txt` → `source-recheck.py --source S051` prints `S051:junk-fabricated MISMATCH reason=quote-not-found`, exit 1 (`wave1/RevJunkTwin.md` §3), plus harness exclusion (`RevJunkTwin.md` §4) | **met** (see §7 note on the "source-recheck exit != 0" wording) |

### 4. Base-tree failability of the same suite (predicate limb)

`git archive 014ee2d7aa8c3c095ff57ae51097606a9906228c | tar -x -C <scratch>/base` (read-only,
no lane write), then the landed suite bytes (`809aaf90…`) against those bytes:

```
$ bash corpus/instruments/r-defect-closure.sh --root <scratch>/base
R1 check=SCORECARD.md lane-hash-markers=2 open=1
R2 check=no 'Erratum 2' block in SCORECARD.md open=1
R3 check=no appended 'Note (round 34)' below R20 open=1
R4 check=tightened kill-rule requirement not recorded (QUALITY R24 row or a SCORECARD paragraph: kill rule + one 'selftest case=' line per case) open=1
R5 check=misnamed selftest case 'url-matching-two-rows' still present (count=2) open=1
R6 check=round-26 manifest has no S040-live.txt record and no orphan list open=1
R7 check=round-33 lesson has no appended R7 erratum open=1
R8 check=round-32 manifest carries a fetched_utc that is not a strict-UTC instant open=1
R9 check=capture-binding H4-H8 cases missing: per-file-orphan-detected per-file-orphan-listed nested-snapshot-dir fetched-utc-pending-rejected fetched-utc-local-offset-rejected dup-record-in-manifest double-https-row rejected-row-anchor summary-only-selftest-rejected open=1
closed=0/9 exit=1
base_exit=1
```

This satisfies the predicate's parenthetical "(the suite fails on the base tree, `closed=0/9`)" and
shows all nine checks individually red while their defects are open. The suite's `--selftest` adds
the second limb (one broken-fixture copy per check, `fixture=rejected` for all nine, plus
`selftest judge=forged-summary rejected=1`).

### 5. Static after-value checks (commands and outputs)

(a) round-32 manifest, strict-UTC:
```
$ python3 - <<'PY'  # read manifest, regex ^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$ per record
rec S049 '2026-10-26T04:16:06Z' archival= None
rec S050 '2026-10-26T04:16:16Z' archival= None
records= 2 non_strict_utc= []
```

(b) `SCORECARD.md` erratum 2 / pre-freeze step: `grep -n` → `1014:**Erratum 2, disclosed (round-34 append, round-25 form).**`, `1028:**Pre-freeze satisfiability step, recorded (QUALITY R22).**`.

(c) `QUALITY.md` per-id note: `grep -n "Note (round 34)"` → `220`; R22/R23/R24 rows at `226`/`227`/`228`.

(d) lesson R7 erratum: heading at `140`; counts reproduced in §3 above.

(e) round-26 orphan:
```
round26_records= ['S041']
S040_in_records= False
purpose= … (1) `sources` holds one record, S041.txt … (2) S040-live.txt has no `sources` record and is declared in the top-level `orphans` list below: 33463 B, 503 lines, sha256 b7f7b55f…
orphans= [{"path": "S040-live.txt", "reason": "Live probe capture of the S040 page, fetched by ScoutS040Probe after this manifest was built; …"}]
```

(f) frontier rule A:
```
selftest case=bidirectional-holds exit=0 want=0 verdict=pass
selftest case=selection-not-declared exit=1 want=1 verdict=pass
selftest case=header-source-not-rechecked exit=1 want=1 verdict=pass
selftest case=evidence-list-declares-selection exit=0 want=0 verdict=pass
selftest case=evidence-declared-not-rechecked exit=1 want=1 verdict=pass
selftest case=selection-neither-declared-nor-mentioned exit=1 want=1 verdict=pass
selftest cases=6 failures=0            FRONTIER_SELFTEST_exit=0
… 20 PASS lines incl. `PASS F17 knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051 exit=0`
entries=20 pass=20 exit=0              FRONTIER_COUNT_exit=0
```
Both directions exist in the code (`corpus/instruments/frontier-recheck-count.py:212`
`problems.append("header-sources-not-rechecked")` for the forward limb; the reverse limb is
`selection-not-declared-by-entry` and `selection-not-cited-by-entry`, exercised by the
`selection-not-declared` case above).

(g) junk twin:
```
$ ls .ufo/waves/round-34/c2-controls/            # before.txt, junk-checker.py, junk-f17.md (940 B)
$ grep -rc "defines five severity levels for smart-contract exploits" corpus/ | grep -v ':0'   # (no rows)
$ grep -c "defines five severity levels for smart-contract exploits" corpus/source-snapshots/round-34/S051.txt
0
```

### 6. Cross-checks against sibling receipts, and non-final bytes I observed

#### 6.1 Agreement with the after-value receipts

Read at the receipts named; each states the same value the live run printed:

- `wave1/ExecRDefectClosureSuite.md:54,67,71,84` — `closed=9/9 exit=0`, `selftest cases=9 failures=0`.
- `wave1/ExecKillRuleCheck.md` + `ExecKillRuleCheck.json` — `mutants=3 killed=3 survivors=0`, controls rejected 4/4 (grep hits at `ConnClaims.md:89-91`, `CritMistakes.md:160-166`).
- `wave1/ExecCaptureBindingHarden.md:84-86` — `AUDIT records=41 … orphans=1 orphan=S040-live.txt`; the same file records the pre-fix `records=41 bound=40 unbound=1` state, i.e. the named FAIL the erratum calls the proof of rule B.
- `wave1/ExecScorecardMarkers.md`, `ExecManifestR32Normalize.md`, `ExecS040Orphan.md`, `ExecLessonErrata.md`, `ExecQualityAppends.md`, `ExecErratum2.md` — the R1/R8/R6/R7/R3/R2 artifacts measured in §3/§5.
- `wave1/ExecHarnessAfter.md:118` — `entries=20 pass=20 exit=0` (harness limb; C2-owned, quoted only as a cross-check).
- `wave1/ConnClaims.md:22-23,42,61,87,89,91` and `wave1/ConnCrossCheck.md:83-86` — same six values including `records=41 bound=41 unbound=0`.
- `wave1/CritOverclaim.md:27-30` — same C1 counter table; `:194-197` records the `records=40 → 41` frozen-literal defect (F7).
- `wave1/RevJunkTwin.md` §3-§4 — the rejection mechanism quoted in §5(g).

No receipt I read states a C1 value that differs from the live measurement at the measured bytes.

#### 6.2 In-flight states (not the measurement of record)

These were observed while waiting for quiescence; each was superseded and is recorded so a later
reader does not mistake a transient for the landed number:

1. `05:41Z` — `frontier-recheck-count.py` working-copy bytes: `selftest cases=4 failures=1` (case
   `extra-source-not-cited` printed `selection-not-in-header-sources,selection-not-cited-by-entry`)
   and plain run `entries=19 pass=14 exit=1` (F01-F05 `selection-not-in-header-sources`). Reported
   to `ExecFrontierBidirectional`; they replied that the header-only reverse rule was superseded and
   landed a fixed instrument (`entries=20 pass=20`; `selftest cases=6 failures=0`), which I
   re-measured green in §5(f).
2. `05:46Z` — the first fully-green C1 state I measured had `r-defect-closure.sh`
   `0beafed2…`/665 lines and `kill-rule-check.py` `7a20e724…`; by `05:52Z` they were
   `aa3128e6…`/`8d12d45f…` and by `06:04Z` `809aaf90…`/`c279d952…` (the measured bytes). All three
   states printed `closed=9/9`, `cases=9 failures=0`, `survivors=0`; only R8 wording, probe rows and
   the gate count (`6 → 7`) moved. `wave1/CritOverclaim.md:144-148` records the same family of
   transients (including a moment when the suite selftest printed `failures=1`), all closed before
   the measured bytes.

### 7. Limits and risks (not blockers)

- **Measurement surface.** The numbers above are the working tree at `HEAD 206e510…` plus the
  wave-1 changes listed in §0. If any file in the input digest changes, the six commands must be
  re-run; the L1's commit itself does not change these bytes.
- **Mutant population.** `kill-rule-check.py` replays three mutants (skip-selftest-summary,
  accept-record-without-url, per-file-binding-removal). The frozen after-list names the first two,
  both killed; the third is additional. `CritOverclaim.md` (F5) notes the population is smaller
  than round 33's four-mutant matrix; that is a counter-strength limit, not a value mismatch.
- **Junk-twin wording.** The twin's own `recheck:` line passes at the tip (it names the real
  manifest); the claim's "(source-recheck exit != 0)" is realized by the twin-derived manifest
  (`reason=quote-not-found`, exit 1) or, pre-freeze, by the missing manifest (exit 2). Recorded as
  `RevJunkTwin.md` §3/§4 state it; not a counter value I can print from the six commands.
- **`grep -c` exit status.** CMD5 prints `0` and exits 1 by grep's no-match convention; the claimed
  quantity is the count.
- **Frozen literal 40.** Command 6 matches the invariant and the L1's `claims-erratum-1.md`, not the
  frozen literal; the divergence is one record (S051) and is disclosed above, not waived here.

### 8. Scratch

All work (the two watcher scripts, the measurement script, its captured outputs, and the
`git archive` extraction of base `014ee2d`) lived under
`/fast/scratch/hyaku/kasegi-r34/ExecRegressionC1/`. The tree is removed after this receipt is
written (`rm -rf -- /fast/scratch/hyaku/kasegi-r34/ExecRegressionC1`); no lane or fleet path was
written by this seat except this receipt. No tools were installed or upgraded for this item.

Report: .ufo/waves/round-34/wave1/ExecRegressionC1.md
