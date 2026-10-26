# ExecCensusAfter — round-34 C2 census after-state

Seat: `ExecCensusAfter` (leaf of the L2 wave; sole writer of this receipt).
Round: kasegi-shokunin round 34, hyaku run 8. Lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Measured: **2026-10-26T05:49Z–05:56Z** (two full battery passes plus a per-command exit pass).
Lane bases: base `014ee2d7aa8c3c095ff57ae51097606a9906228c`, claims-freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13`.

Writes: this receipt only. No lane byte below was modified; every command in §2–§6 is read-only over the repo
(`sources-census.sh` writes nothing without `--out`; the instruments read only). No `git`/`jj` mutation was run.
No tool installs or upgrades were performed (nothing needed).

## Report

### 1. Where in the round these bytes are — read this before quoting any number

The wave-1 landing exists **in the working copy only**. At every measurement instant:

```
$ jj log -r @ --no-graph -T 'commit_id ++ " parent=" ++ parents.map(|p| p.commit_id()).join(",")'
5596caaa1c77707e79c0cdb1b4a0f05460088954 parent=206e5108f1190e61b3e2622d21cab8a5d921650c
$ jj log -r @- --no-graph -T 'commit_id ++ " " ++ description.first_line()'
206e5108f1190e61b3e2622d21cab8a5d921650c round-34: wave-1 spec (65 seats, v2 policy), validated plan and dispatch
```

So the numbers below are measured on **uncommitted working-copy bytes** sitting on top of the wave-1 spec commit,
not on a landing commit (the L1 commits; this seat does not). Digest bookends in §7 let the L1 prove the committed
bytes are the same bytes after integration. `jj status` at measurement time carried **12 modified** and **13
untracked** paths (full list, re-read at 05:58Z after an earlier truncated read was caught — the first pass of
this receipt undercounted untracked paths at 6 because the status was piped through `sed -n '1,20p'`):

```
M .ufo/waves/round-33/wave1/ScribeReportDraft.md   M SCORECARD.md
M corpus/QUALITY.md                                M corpus/README.md
M corpus/SOURCES.md                                M corpus/instruments/README.md
M corpus/instruments/capture-binding-check.py      M corpus/instruments/frontier-recheck-count.py
M corpus/lessons/round-29.md                       M corpus/lessons/round-33.md
M corpus/source-snapshots/round-26/manifest.json   M corpus/source-snapshots/round-32/manifest.json
? .ufo/waves/round-34/assimilation/                ? .ufo/waves/round-34/claims-erratum-1.md
? .ufo/waves/round-34/wave1/                       ? .ufo/waves/round-34/wave1.ready
? .ufo/waves/round-34/wave1.ready.dispatched       ? corpus/instruments/kill-rule-check.py
? corpus/instruments/r-defect-closure.sh           ? corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
? corpus/lessons/round-34.md                       ? corpus/source-snapshots/round-34/
? selftest-baseline.txt
```

Both C1 instruments (`r-defect-closure.sh`, `kill-rule-check.py`), the round-34 manifest directory, the lesson
and the F17 entry are **untracked**: the landing is not merely uncommitted, it is not yet staged in any commit.

**Hygiene observation for the L1 (not this seat's file, not deleted):** `selftest-baseline.txt` sits untracked at
the **lane root**, 1552 bytes, sha256 `ca3759d1c4a047ec1a27f4d6bc8b64df4d6e21a29b74ef9904ccbe91be3a3a51`,
mtime 02:37 local — a seat wrote a `capture-binding-check.py` selftest transcript outside its assigned paths
(`.ufo/waves/round-34/wave1/…` or scratch), where every other receipt lives. The L1 should decide whether it is
committed as evidence or removed; this receipt only records it.

**Quiescence predicate actually used** (not "the wave looked done"): poll every 20 s for
`registry rows>=51`, `S051 rows>=1`, `README F<n> rows>=17`, `knowledge entries citing 'source: S051'>=1`,
`corpus/source-snapshots/round-34/manifest.json` present, `corpus/instruments/r-defect-closure.sh` present,
`kill-rule-check.py` present, `SCORECARD.md` `<LANE_HASH>` count 0 — **and** three consecutive polls with an
identical sha256 set over `corpus/SOURCES.md`, `corpus/README.md`, `SCORECARD.md` and every
`corpus/instruments/*.py|*.sh`. Fired `QUIESCENT` at **05:48:31Z**. Two seats confirmed the same byte set
independently (`RevCensus` message 05:5xZ: "my bookend digests SOURCES.md 4c85ff86… / README.md 876be9cc… equal yours exactly").

The measured surfaces kept moving before that point — `landed=1` first held at 05:38:10Z, but the input digest
changed again at 05:46:51Z, 05:47:11Z and 05:48:11Z. A census run between 05:38Z and 05:48Z would have measured
transient bytes; the numbers below do not.

### 2. A1 — round-end census (`sources-census.sh validate`)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

- exit **0**, one registry (`…/kasegi-shokunin/corpus/SOURCES.md`), verdict line `kasegi ok`.
- **W04 only, and only S028/S029** — the two carried-forward duplicate-URL warnings, unchanged from
  `.ufo/waves/round-34/census-before.txt` (§ "census before", same two lines, same exit 0). No E-code.
- Lane selection is the fleet conf row `kasegi|kasegi-shokunin|depth + coverage (bounty and security research)`
  (`/home/vgpnk/Projects/shokunin/shokunin.conf:46`); the script parses it textually (never sources it).
- Byte-identical in both passes (run1 vs run2 diff, §7).

### 3. A2–A9 — the contract commands (verbatim from `.ufo/waves/round-23/falsify/RegistryR8.md:143-168`)

Run from the lane root. Each command was run twice (§7) with identical output; exit codes were captured in a
separate per-command pass so no pipeline exit is misattributed.

| # | command | output | exit | frozen C2 expectation | verdict |
|---|---|---|---|---|---|
| A2 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `51` | 0 | rows 51 | **match** |
| A3 | `awk -F'\|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md` | `0` | 0 | malformed 0 | **match** |
| A4 | tier histogram (`$5`) | `A=48 B=1 C=2` | 0 | A=48 B=1 C=2 | **match** |
| A5 | status histogram (`$9`) | `mined=39 queued=9 rejected=3` | 0 | mined=39 queued=9 rejected=3 | **match** |
| A6 | duplicate ids (`uniq -d`) | *(empty, 0 bytes)* | 0 | empty | **match** |
| A7 | enum violations + tier inflation (`A`+`community`) | *(empty, 0 bytes)* | 0 | empty | **match** |
| A8 | mined rows whose `used-by` paths do not exist | *(empty, 0 bytes)* | 0 | empty | **match** |
| A9 | independent count of rows whose `used-by` cell is not `—` | `39` | 0 | (not frozen; equals `mined=39`) | consistent |

A9 is the cross-check that the A8 walk is not vacuous: all 39 `mined` rows carry a non-`—` used-by cell and all 39
paths exist. Sum check: `48+1+2 = 51` rows, `39+9+3 = 51` statuses.

### 4. B1–B4 — registry/frontier cells the claim names

| # | command | output | exit |
|---|---|---|---|
| B1 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `17` | 0 |
| B2 | `grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md` | `1` | 0 |
| B3 | `grep -lE '^source: S051 ' corpus/knowledge/*.md \| wc -l` | `1` | 0 |
| B4 | `ls corpus/knowledge/*.md \| wc -l` | `46` | 0 |

B3's one hit is `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` (113 lines, sha256
`948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a`); `grep -c '^source: S051 '` summed over
`corpus/knowledge/*.md` is exactly **1**, so the citation is single-sourced.

Frontier row status, independent of the count: `awk` over the `F<n>` rows gives `admitted=17` (no queued/rejected
frontier rows), so B1's 17 is 17 **admitted** rows, and admitted went 16 → 17 against the freeze state
(`.ufo/waves/round-34/census-before.txt`: `-- frontier admitted -- 16`). The F17 row reads:

```
| F17 | Immunefi Vulnerability Severity Classification System v2.2 — Web3/smart-contract bounty severity classification | admitted | knowledge/immunefi-vscs-v2-2-smart-contract-severity.md | S051 | …
```

Registry row S051, field by field (`-F'|'`, cell index 1..11 = columns id…used-by):

```
f1=[S051]  f3=[docs]  f4=[A]  f8=[mined]  f9=[2026-10-26]  f10=[90d]
f11=[corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md]
f2=[Immunefi Vulnerability Severity Classification System v2.2 — https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/]
```

i.e. tier **A**, status **mined**, opened **2026-10-26**, used-by the entry above — the frozen C2 cell holds.
Registry 50 → 51 and frontier 16 → 17 are both measured here, not taken from the claim.

### 5. B5/B6 — the two C2 runtime re-checks (cross-check; the C2 seat owns their claim)

**B5 `frontier-recheck-count.py`** — full output, 20 `PASS` lines, exit 0:

```
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0
… (F02…F16, 19 lines) …
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
entries=20 pass=20 exit=0
harness_exit=0
```

20 entries over 17 admitted rows because F09, F10 and F11 each have two entries. `ids=S051` appears on exactly
the F17 line.

**B6 `source-recheck.py --source S051`** — 19 lines, exit 0:

```
S051:sha256 OK
S051:Q1 OK occurrences=1 anchor=46-ok      S051:Q10 OK occurrences=1 anchor=79-ok
S051:Q11 OK occurrences=1 anchor=83-ok     S051:Q12 OK occurrences=1 anchor=88-ok
S051:Q13 OK occurrences=1 anchor=92-ok     S051:Q14 OK occurrences=1 anchor=94-ok
S051:Q15 OK occurrences=1 anchor=90-ok     S051:Q16 OK occurrences=1 anchor=95-ok
S051:Q17 OK occurrences=2 anchor=96-ok     S051:Q18 OK occurrences=1 anchor=99-ok
S051:Q2 OK normalized=markup-whitespace occurrences=1
S051:Q3 OK occurrences=1 anchor=52-ok      S051:Q4 OK occurrences=1 anchor=52-ok
S051:Q5 OK normalized=markup-whitespace occurrences=1 anchor=53-ok
S051:Q6 OK normalized=markup-whitespace occurrences=1 anchor=55-ok
S051:Q7 OK occurrences=1 anchor=74-ok      S051:Q8 OK occurrences=1 anchor=75-ok
S051:Q9 OK occurrences=2 anchor=77-ok
recheck_exit=0
```

Assertion census on that output: `grep -c '^S051:Q'` = **18**; `grep -c 'occurrences=1'` = **16**;
`grep -c 'occurrences=2'` = **2**; `grep -n 'MISMATCH\|FAIL'` = **no lines** (exit 1 from grep = none found).
Exit 0, hash pin OK. See §8.1 — the claim's wording "every assertion occurrences=1" is false as written.

Manifest binding for the record (`corpus/source-snapshots/round-34/manifest.json`, sha256
`d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe`): 1 source,
`id=S051 path=S051.txt url=https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/
fetched_utc=2026-10-26T05:31:10Z sha256=4fd8ed98…b325a5 quotes=18`. The `url` byte-equals its own registry-row
`https://` token, and `fetched_utc` is strict-UTC with a `Z` (no local offset), so nothing here feeds R8.

### 6. C1–C3 — the junk twin, measured three ways (read-only)

```
C1 do-nothing shape checker:  junk_twin h1=True source_line=True recheck_line=True / shape_counters=3/3 / exit=0
C2 record in round-34 manifest?                 grep -c 'junk-f17' corpus/source-snapshots/round-34/manifest.json -> 0
C3 twin quote in round-34 captures?             'Direct theft of any user funds' -> 2 hits
                                                (corpus/source-snapshots/round-34/S051.txt:75 and the manifest quote array)
                                                'five severity levels for smart-contract exploits' -> 0 hits
```

The twin `.ufo/waves/round-34/c2-controls/junk-f17.md` (940 bytes, committed at the freeze commit `29f606db`)
is **not invisible to the counters by shape** — its do-nothing checker prints `3/3` and exits 0 — and it is not
rejected by content-grep either, because the fragment it quotes is real. What is fabricated is its synthetic
clause; `grep` finds `five severity levels for smart-contract exploits` **0** times in `S051.txt`. Two
consequences, both measured rather than argued:

1. **The counter is body-blind.** The twin's own `recheck:` line is
   `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051`,
   and that exact command exits **0** (§5, B6). Running the twin's recheck therefore does not reject it.
   `ExecHarnessAfter.md` §F-B measured the same boundary earlier ("the harness does not read entry bodies").
2. **`r-defect-closure.sh`'s R9 limb asserts presence, not rejection.**
   `corpus/instruments/r-defect-closure.sh:433-436` loops `c2-controls/junk-f17.md` /
   `.ufo/waves/round-34/c2-controls/junk-f17.md` and fails only when **neither exists** (`DESC="c2-controls/junk-f17.md absent"; return 1`);
   the case-name loop above it (`:424-428`) is `grep -q -- "\"$name\"" "$f"`, i.e. nine
   string-presence assertions on the checker's source, not nine executed cases. The limb's behavioural half is
   the frontier rule-A mirror/reverse pair (`:437-463`), which is real (mirror exit 0, reverse exit 1 at `:462-463`).

So C2's kill-rule parenthetical "(source-recheck exit != 0; reviewer REFUSE)" is true only through its **reviewer**
limb. The lane already routes this honestly in the entry itself —
`corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md:6` writes the recheck as
"18 assertions (Q1-Q18) … each `occurrences=1` or anchored (Q9/Q17)" — and in `ExecHarnessAfter.md` §F-B.
Recorded here so that no census PASS is read as a mechanical junk-twin rejection.

### 7. Determinism and quiescence evidence

- Two full battery passes (`run1.txt`, `run2.txt`, 126 lines each) diffed to **4 lines**: only the working-copy
  commit id line, `f0b96e81…` → `5596caaa…` (`jj` re-snapshotted the empty working copy). Every other line —
  census, all eight contract commands, digests, harness, recheck, junk measurements — is byte-identical.
- Input digest set sha256'd immediately before and immediately after each pass: `diff` empty both times
  (`DIGESTS_STABLE=yes`, `DIGESTS_STABLE_run2=yes`), and the two "before" sets are identical to each other
  (`SAME_INPUTS_as_run1=yes`). Nothing this receipt measured moved during measurement.
- Digest set at the quiescent state (post-pass re-read, 05:56Z):

| path | sha256 |
|---|---|
| `corpus/SOURCES.md` | `4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6` |
| `corpus/README.md` | `876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29` |
| `SCORECARD.md` | `b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0` |
| `corpus/QUALITY.md` | `77d99df9abf57a66065dbe927ce95f0ddf8acbfba237fefd163bdd3871751af8` |
| `corpus/lessons/round-33.md` | `f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807` |
| `corpus/source-snapshots/round-34/manifest.json` | `d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe` |
| `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` | `948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a` |
| `corpus/instruments/r-defect-closure.sh` | `357a7e4923bf784cd513dfaa94258d4cb6d5dfc1cbb677b36accbab86a05bc2d` |
| `corpus/instruments/kill-rule-check.py` | `c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61` |
| `corpus/instruments/capture-binding-check.py` | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` |
| `corpus/instruments/frontier-recheck-count.py` | `1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249` |
| `corpus/instruments/source-recheck.py` | `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` |

`SCORECARD.md` `<LANE_HASH>` count at these bytes: `grep -c '<LANE_HASH>' SCORECARD.md` → **0**.

### 8. Discrepancies against the frozen C2 cell (report, do not fix — the L1 owns the claim)

1. **"every assertion occurrences=1" is false at the landed bytes.** Two of the 18 S051 assertions print
   `occurrences=2` (`Q9`, `Q17`), both disambiguated by `anchor=77-ok` / `anchor=96-ok`. The recheck still exits 0
   and the pin verifies, so the *instrument* verdict is sound and QUALITY Q9's anchor rule is exactly what makes it
   sound; the *claim sentence* overstates. Fix is wording (or the claim's parenthetical "each `occurrences=1` **or
   anchored**", which the entry at `…-severity.md:6` already uses), not a capture edit.
2. **"junk twin … rejected by the admission gate (source-recheck exit != 0)" is not mechanically reproducible.**
   Measured: the twin's own `recheck:` command exits 0; the twin is absent from the manifest (`0` records) but
   nothing asserts that absence; and `r-defect-closure.sh` R9 tests presence of the twin file plus nine
   `grep`-for-string assertions on `capture-binding-check.py`, never an executed rejection. Rejection is the
   reviewer limb (body-grep of the twin's synthetic clause → 0 hits) plus non-admission to the frontier table. If
   the L1 wants a mechanical limb, the honest shape is a check that a `c2-controls/` fixture's **non-quoted
   synthetic phrase** is absent from the pinned capture — currently unlanded.
3. Non-blocking: the frozen C2 `before` cell says "junk F17 twin … source-recheck on it fails (exit 2)". At the
   landed bytes the twin's recheck exits 0, so that before-cell describes a different invocation (exit 2 is the
   absent-manifest verdict). Consistent with §8.2 — the before and after cells disagree with each other about what
   the twin's rejection consists of.

### 9. What this seat does not establish

- **Not a commit-pinned measurement.** §1: working-copy bytes on top of `206e5108`. Re-run §2–§4 after the L1's
  integration commit and compare with the §7 digest table; identical digests ⇒ identical verdicts.
- **Not a fleet-wide census.** `--root` is the fleet root but the lane list is `kasegi` only; 3 output lines, one
  registry. Other lanes' registries were not read.
- **W04 is a warning, not a failure.** S028/S029 duplicate-URL warnings are carried from earlier rounds and are
  outside the validate exit rule (warnings do not change a clean lane's status); this receipt reports them as
  census facts, not as defects introduced this round.
- **A8 is a path-existence walk, not a content check.** It proves the 39 mined `used-by` paths exist on disk; it
  does not prove each target cites the row (that is `capture-binding-check.py`/`source-recheck.py` territory and
  was measured by other seats).
- **This seat does not judge the round.** It reports the after-state numbers, the two §8 discrepancies and the
  replayable commands; the L1 integrates and decides.

### 10. Post-receipt replay (same bytes, 06:0xZ)

Re-ran the three load-bearing commands after this receipt was written, to prove the receipt still describes live
bytes:

```
$ sha256sum corpus/SOURCES.md corpus/README.md SCORECARD.md corpus/source-snapshots/round-34/manifest.json
4c85ff86…c9e77b6  corpus/SOURCES.md          (== §7)
876be9cc…bf6f29   corpus/README.md           (== §7)
b8fc8c66…389c0    SCORECARD.md               (== §7)
d5077f81…8eebe    corpus/source-snapshots/round-34/manifest.json  (== §7)
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
<same three lines: W04 S028, W04 S029, kasegi ok>   census_exit=0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 51
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md -> 17
```

Independent agreement: `RevC2BeforeAfter` (message 06:0xZ) re-hashed to the same SOURCES.md/README.md digests and
reported the same counters (`rows=51 s051=1 front=17 citing=1 know=46`); `RevCensus` (message 05:5xZ) matched the
same two bookend digests and the same six contract outputs. The harness digest note in their message
(`87b14892… → 1be79af6…`) does not touch this receipt: my input set recorded
`frontier-recheck-count.py = 1be79af6…` (§7) on both passes, i.e. every §5 counter line was produced by the
post-move bytes.

### 11. Scratch hygiene

Scratch root `/fast/scratch/hyaku/kasegi-r34/ExecCensusAfter/` held `wait-landed.sh`, `census-after.sh`,
`run1.txt`, `run2.txt`, `run-diff.txt`, `dig-before.txt`, `dig-after.txt`, `dig2-before.txt`, `dig2-after.txt`,
`contract-exits.txt`, `recheck-s051.txt`. Every figure above is transcribed into this receipt; the directory was
removed with `rm -rf --` after this file was written, so no tree is left on disk.

### 12. Post-measurement drift (append-only correction; supersedes §6's line cites and two §7 digests)

`RevCensus` (06:2xZ) reported `r-defect-closure.sh` at a digest other than the one in §7. Re-measured here at
06:3xZ: **two inputs moved after this seat's battery, and neither is a C2 input.**

| path | §7 digest (05:49–05:56Z) | current (06:3xZ) | moved? |
|---|---|---|---|
| `corpus/instruments/r-defect-closure.sh` | `357a7e49…05bc2d` (688 lines) | `2a635bf575c38e04b028dd26ecbeff73c3b909add892ab727c2ab6b1c821dcfc` (742 lines) | **yes** |
| `SCORECARD.md` | `b8fc8c66…3389c0` | `efa646c83baead97e41d9ccad65fac9a4d8468f6bb8af956446d347d68237e91` | **yes** |
| `corpus/SOURCES.md` | `4c85ff86…c9e77b6` | unchanged | no |
| `corpus/README.md` | `876be9cc…bf6f29` | unchanged | no |
| `corpus/source-snapshots/round-34/manifest.json` | `d5077f81…8eebe` | unchanged | no |
| `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` | `948b202e…ac1d8a` | unchanged | no |
| `kill-rule-check.py` / `capture-binding-check.py` / `frontier-recheck-count.py` / `source-recheck.py` | `c279d952…` / `3d9e5e0d…` / `1be79af6…` / `fd2e01e8…` | unchanged | no |

Working copy id also rewrote again (now `34eb2f68…`, parent still `206e5108…`), i.e. the tree keeps being
re-snapshotted while uncommitted — which is exactly why §1's byte-state caveat and these digests exist.

**§6's line citations are digest-scoped and now stale.** They were read at `357a7e49…` (688 lines). At the current
`2a635bf5…` (742 lines) the same code sits at: `check_r9()` `:427`; nine case-name `grep -q -- "\"$name\"` `:433-438`
(for-list `:433-436`, grep `:437`, `done` `:438`); twin-presence `for` `:442-444` with the absence guard at `:445`;
rule A comment `:446` through the reverse assertion `:472`. Re-read whole at the new digest: the **substance is
byte-for-byte the same logic** as §6 describes — nine string-presence assertions on
`capture-binding-check.py`, a twin-FILE-existence test that never executes a rejection, and the behavioural
mirror/reverse pair (`rc_mirror` must be 0, `rc_reverse` must be 1). So §6's finding stands; only its anchors moved.

**C2 cells re-measured at the drifted bytes (all unchanged):**

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi W04 S028 … / kasegi W04 S029 … / kasegi ok …        census_exit=0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 51
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md -> 17     ls corpus/knowledge/*.md | wc -l -> 46
$ python3 corpus/instruments/frontier-recheck-count.py --root .
… PASS F17 knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051 exit=0
entries=20 pass=20 exit=0                                  harness_exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
18 assertion lines (16 occurrences=1 + Q9/Q17 occurrences=2, anchored)   recheck_exit=0
$ grep -c '<LANE_HASH>' SCORECARD.md -> 0
```

**Rule recorded for the L1 (R13-style): an anchor into this still-uncommitted tree is valid only against the
digest it was measured at.** Every line cite in this receipt names the digest it belongs to; §7 is the 05:49–05:56Z
state, this section is the 06:3xZ state, and the reconciliation is that C2's numbers and §6's finding are identical
in both while two non-C2 surfaces' anchors shifted.
