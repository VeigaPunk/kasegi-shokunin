# Round-25 report evidence pointers (read-only seat)

Seat: `L1Kasegi25.RevReportFacts`. Lane base revision
`b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. No production edit; the only write is this file.

**Capture window: 2026-10-25T08:24Z – 08:44Z.** The lane was moving under this seat (29 modified
`corpus/knowledge/*.md` at 08:26Z; a 36th entry at 08:31:21Z; a 37th at ~08:34Z; the frozen
instrument rewritten five times, 08:33Z–08:43Z). Every figure below is stamped with the state it was measured
in. A figure without a state stamp is not reproducible.

`single-source` is defined as: **every occurrence of the figure in the lane agrees, and the command
reproduces it from bytes pinned by a digest.** A `no` means either another lane file states a
different value for the same object, or the value cannot be reproduced from pinned bytes.

---

## 1. Conflicts (read first — these are the round-24 failure mode, live)

### X1 — the C1 "after" is quoted with six different verdicts across lane files; the frozen target string is unprintable

The C1 surface is "the `recheck:` line of every `corpus/knowledge/*.md` entry". Two C2 entries
landed while the round was measuring, so the denominator moved from 35 to 37 and two of the new
lines fail the `paths` limb.

| when (UTC) | artefact | instrument | lines | pass | fail-closed | paths_fail | exit |
|---|---|---|---|---:|---:|---:|---:|---:|
| 08:28:04Z | `c1-after.json` snapshot 1, sha256 `54081c5b85f75b8cff571de96fb771421edca18c06a672ab47e83c3befb578e1` | `d07af435…` or later (see X2) | 35 | 35 | 23 | 0 | 0 |
| 08:33:43Z | `c1-after.json` snapshot 2 (same path, rewritten in place), sha256 `98fa3f02ad45f798547723891f160a352de472288d3b0ade4a9d6e23fda89006` | `efbd18ee…` | 36 | 35 | 24 | 1 | 1 |
| 08:36:31Z | live counter, before the round-25 manifest landed | `4475d2e6…` | 37 | 35 | 25 | 2 | 1 |
| **08:39:19Z** | **`c1-after.json` snapshot 3, sha256 `e4bdd98cec2cfe94c472f4e72eaca7fad861fa23b51457b9c5aed4098f32856d`** | `1ccee066…` | **37** | **37** | **23** | **0** | **0** |

`corpus/source-snapshots/round-25/manifest.json` landed at 08:37Z (sha256
`45789aa44b3c7cca8bd66a9557e71093c36f499ad2b6ca112b11ae3c7dd0c206`, 5 records, 33 quotes,
`source-recheck.py` over it exits 0), which cleared both `paths` failures. The counter's **final**
line is therefore:

```
lines=37 total=37 pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
```

The substantive finding survives that resolution: **the frozen target string `lines=35 pass=35
exit=0` is not printable by any tree that also satisfies C2**, and the round's own lane files quote
six different verdicts for the same counter. Every one of them must be reported with its state and
digest.

The same round's counter is quoted with **six** different verdicts across lane files. Only the
first, second and fourth are measured-and-receipted; one is a prediction; one is a disclaimed
transient; two are labelled mutant runs.

| figure | where | status |
|---|---|---|
| `lines=35 pass=35 … exit=0` | `c1-after.json` snapshot 1; `FixRecheckLines.md:47,56`; `CritC1Axis.md:78,92`; `CritC2Ground.md:121` | **measured** — valid only for the 35-entry tree |
| `lines=36 pass=35 … paths_fail=1 exit=1` | `c1-after.json` snapshot 2; `EntryJapanVendors.md:170` | **measured** — the first C2 entry's recheck names a manifest that does not exist |
| `lines=36 pass=36 exit=0` | `CritC2Ground.md:123` ("*Correction:* report C1 as …"), `EntryJapanVendors.md:174` ("after the manifest lands … should print") | **predicted, not measured** — no tree has printed it. Quoting it as a measurement would be fabrication |
| `lines=37 pass=35 … paths_fail=2 exit=1` | live counter at 08:36:31Z | **measured** — pre-manifest tree, no receipt file |
| `lines=37 pass=37 … paths_fail=0 exit=0` | `c1-after.json` snapshot 3 (sha256 `e4bdd98c…`, 08:39:19Z) | **measured and receipted** — the round's citable after, on 37 entries |
| `lines=35 pass=32 … cwd_fail=3 exit=1` | `AuditControls.md:121` (`c1-controls/live-lane.json`) | **measured, disclaimed in-file** — mid-edit worktree, not the round's after |
| `pass=29` / `pass=6` | `MutAuditLimbs.md:31,34` / `:9,21,32,33` | **measured** — labelled limb-isolation mutants on scratch copies, not the after |

`c1-after.json` is a **single file that has held three different after-states in eleven minutes**.
Consequences the report must state rather than paper over:

- `claims.json` C1 says the surface is "every `corpus/knowledge/*.md` entry (35 lines)". At 37 files
  "every entry" and "35 lines" are no longer the same set. The frozen target string
  `lines=35 pass=35 exit=0` is **not** what the live counter prints.
- The two new lines are `vendor-disclosure-policies-as-corpus-objects.md` and
  `vendor-disclosure-policy-commitments-crosswalk.md`; between 08:31Z and 08:37Z both named
  `corpus/source-snapshots/round-25/manifest.json`, which **did not exist** then
  (`ls corpus/source-snapshots/round-25/` → five `.txt`, no manifest), so both failed the `paths`
  limb and were class `fail-closed` with lane/foreign exit 2. That verbatim failure, at 08:35Z:

  ```
  $ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S036
  manifest UNAVAILABLE reason=missing
  exit 2
  ```

- The C1 after-claim is citable only as **"`lines=37 total=37 pass=37 fail-closed=23 parse_fail=0
  cwd_fail=0 paths_fail=0 exit=0`, receipt sha256 `e4bdd98c…`, 08:39:19Z"**, paired with the
  disclosure that the frozen target string says `lines=35` and the denominator moved because C2's
  own vehicle added two entries. Do not quote `lines=36 pass=36 exit=0` (never printed) or
  `lines=35 pass=35 exit=0` (a superseded state) as the round's after.

### X2 — the frozen instrument digest no longer matches the live instrument

| object | digest | source |
|---|---|---|
| `corpus/instruments/recheck-audit.py` at receipt time (pinned) | `d07af435009a0395662b3062c33bd5e5242afd8b6902d30f34b155cd11b564d6` | `.ufo/waves/round-25/c1-instrument-digest.txt:1` |
| `corpus/instruments/recheck-audit.py` at 08:33:22Z | `efbd18ee191b25b7bc74ef0d9cbbcca50c1630f95eb2084be75d0afe30ca676d` | `sha256sum` |
| `corpus/instruments/recheck-audit.py` at 08:36Z | `4475d2e60ca624c5b63b790c7f11eaebd154333300fb4dadc5020aa7e41acccc` | `sha256sum` |
| `corpus/instruments/recheck-audit.py` at 08:39Z | `1ccee066a50be51cd528e31810a1fee1cab178fdb84ea38c47026973ce341c82` | `sha256sum` |
| `corpus/instruments/recheck-audit.py` at 08:43Z (live at close) | `8ab4dff70b578268bb2ff625dff99168d17e24629856180c30f8b9f5204f1475` | `sha256sum` |

**Five recorded digests in one round (plus one unrecorded intermediate), and the pinned one is none
of the live four.** The edits add two
**strict** limbs (`cdroot`, `instrument`), `pass_strict`, a `strict pass=…` line printed *above* the
frozen summary line, and (third version) `total=` plus `artifact_fail`/`own_fail` inside that
summary line. The frozen `pass` is documented as unchanged (still limbs a–c) and the base-bytes run
still prints the identical frozen before-fields — but the summary line's *shape* moved, so a quoted
line can now be matched to an instrument version only by its fields.

- `c1-after.json` **carries `pass_strict` and `strict` keys**, so snapshots 1–3 were all written by
  a version *after* `d07af435`. **No receipt records the digest of the instrument that produced any
  of them**; snapshot 3 was produced by `1ccee066…` only by mtime coincidence (receipt 08:39:19Z,
  instrument mtime 08:39Z), which is not a pin. The before receipt is pinned; the after is not.
- The instrument is **untracked** (`git ls-files corpus/instruments/recheck-audit.py` → empty), so
  no version is in git at the base revision.
- The frozen `pass` semantics did survive the churn: every version this seat ran printed
  `pass=6` on the base tree and `pass=37` on the settled tree, with the same limb definitions for
  (a)–(c). The added fields are `total=`, `strict …`, `artifact_fail`, `own_fail`.

### X3 — round-24 assertion count: 77 vs 76, still unfixed in three lane files

Measured: `corpus/source-snapshots/round-24/manifest.json` has 19 `quotes` arrays totalling **76**.

| file:line | says |
|---|---|
| `SCORECARD.md:510` | "19 records, **77** assertions, exit 0" |
| `LOG.md:1213` | "19 captures, **77** assertions" |
| `corpus/lessons/round-24.md:77` | "19 records / **77** assertions" |
| `.ufo/waves/round-24/wave1/CaptureTool.md:237` | "all **77** assertions" |
| `corpus/instruments/README.md:179` (working tree, round-25 edit) | "19 captured records, **76** assertions" + the counting command |
| `.ufo/waves/round-24/c1-counterA-manifest-receipt.txt` | **95** `OK` lines = 19 `:sha256` + 76 |

This is D24-2 (`corpus/lessons/round-24-verifier-spotcheck.md` §6) marked fixed only in
`instruments/README.md`; the three other files still carry 77. **Do not restate 77 in the round-25
report.**

### X4 — one document, two id spaces

`capture-log.txt:5` says the lane ids "continue the append-only registry from S035", and the table
below it assigns S036–S040 to the five captures while listing a *staged* id for the same document:
S036→S055, S037→S056, S038→S057, S039→S060, S040→S068. `claims.json` `assimilation.planned_admit`
names the staged ids (S055/S056/S057/S060). The lane registry ends at S035 (35 rows, no S05x row
exists), so a header citing S055 cites **no registry row**, while the frozen C2 counter
`^source: S0(3[6-9]|[4-9][0-9])` matches **both** id spaces and cannot tell them apart. Both new
entries in fact cite the lane ids S036–S040 — state the id space explicitly in the report.

### X5 — a transient worktree figure already written into a wave-1 report

`.ufo/waves/round-25/wave1/AuditControls.md:121` records the live worktree as
`lines=35 pass=32 … cwd_fail=3 exit=1` (`c1-controls/live-lane.json`). That is a real measurement
of a moving tree, and the file itself disclaims it ("not the frozen before … not used by this report
for any verdict"). It must not be quoted as the round's after; at 08:30:50Z the same command printed
`lines=35 pass=35 … cwd_fail=0 exit=0`.

---

## 2. Fact table

| # | fact | command (from `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless noted) | output | single-source |
|---|---|---|---|---|
| 1 | lane base revision | `git rev-parse HEAD` | `b49948f1164ef65106b2c4cbee3f53e8a44b8c41` | **yes** — the only 40-hex value in `.ufo/waves/round-25/*.json`/`*.txt` (`grep -rhoE '\b[0-9a-f]{40}\b' … \| sort \| uniq -c` → `3 b49948f…`), and identical in `claims.json:base_revision`, `wave1-spec.json` context, `wave1-dispatch.json` context, `ScoutNoHarm.md:125` |
| 2 | C1 before receipt line | `tail -2 .ufo/waves/round-25/c1-before.txt` | `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1` / `BEFORE_EXIT=1` | **yes** — same line at `claims.json:17-18` (as prose counts), `AuditControls.md:78,142`; reproduced below |
| 3 | C1 before **reproduced on base bytes** | `git archive b49948f corpus \| tar -x -C /tmp/r25-before && cp corpus/instruments/recheck-audit.py /tmp/r25-before/corpus/instruments/ && cd /tmp/r25-before && python3 corpus/instruments/recheck-audit.py` | `lines=35 total=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1` — every frozen field identical to the receipt; the only difference is the newer instrument's added `total=` field, exit 1 | **yes** — byte-pinned: `git show b49948f:<path> \| sha256sum` vs the export, **35 files / 0 mismatches** (run by this seat) |
| 4 | C1 after, snapshot 1 (08:28:04Z) | `python3 -c "import json;d=json.load(open('.ufo/waves/round-25/c1-after.json'));print(d['lines'],d['pass'],d['fail_closed'],d['failing_limbs'])"` | `35 35 23 {'parse':0,'cwd':0,'paths':0}` → `lines=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`; sha256 `54081c5b…` | **no** — see X1/X2 |
| 5 | C1 after, snapshot 2 (08:33:43Z) | same command | `36 35 24 {'parse':0,'cwd':0,'paths':1}`; sha256 `98fa3f02…` | **no** — see X1 |
| 6 | C1 after, final (snapshot 3, 08:39:19Z) | `python3 corpus/instruments/recheck-audit.py` (and `python3 -c "…c1-after.json…"`) | `lines=37 total=37 pass=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`; receipt sha256 `e4bdd98c…32856d`; instrument `1ccee066…` (unpinned) | **no** — the value is reproducible now, but the frozen target says `lines=35` and no receipt pins the producing instrument (X1/X2) |
| 7 | instrument digest, pinned vs live | `sha256sum corpus/instruments/recheck-audit.py; cat .ufo/waves/round-25/c1-instrument-digest.txt` | live `1ccee066…341c82` (08:39Z); earlier `efbd18ee…`, `4475d2e6…`; pinned `d07af435…b564d6` | **no** — see X2 |
| 8 | before-receipt digest | `sha256sum .ufo/waves/round-25/c1-before.json` | `3e3eeb4e39f0d6200ad521fc02fd1c970c872c9e73b5c2ec8868e66c8b2d877e` = digest-file line 2 | **yes** |
| 9 | five capture digests | `sha256sum corpus/source-snapshots/round-25/*.txt` | S036 `022ca4f4…ceb950`, S037 `b204aa7f…73cb4c`, S038 `09e077d3…bb68a`, S039 `657e7b4c…fc191d`, S040 `b7f7b55f…c4e286c` | **yes** — all five equal `capture-log.txt:10-14` **and** the `sha256` cells of `corpus/source-snapshots/round-25/manifest.json` (5 records, 33 quotes, sha256 `45789aa4…c206`, `source-recheck.py` exit 0) |
| 10 | capture byte sizes | `ls -l corpus/source-snapshots/round-25/` | 4815 / 11194 / 3093 / 37126 / 33463 | **yes** — equal `snapshot_bytes` in `capture-log.txt` |
| 11 | frontier admitted, before | `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | `9` (F01–F09) | **yes** — same on base bytes (`git show b49948f:corpus/README.md \| awk …` → 9); `corpus/README.md:212` "9/9 admitted at round 24"; `claims.json:31` frontier=9. `SCORECARD.md:404` "frontier 8/8" is the round-23 row, not this round |
| 12 | census before | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi` | `rows 35`, `tier.A 32`, `tier.B 1`, `tier.C 2`, `status.mined 23`, `status.queued 9`, `status.rejected 3`, exit 0 | **yes** — equals `claims.json:39` and `corpus/lessons/round-24.md:119`; independent row count `grep -cE '^\| *S[0-9]{3} ' corpus/SOURCES.md` → 35. `SCORECARD.md:301` "27 rows" is the round-22 capability row |
| 13 | census validate before | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `W04 S028 duplicate url …`, `W04 S029 duplicate url …`, `ok …/corpus/SOURCES.md`, exit 0 | **yes** — equals `claims.json:39` "W04 x2 (S028,S029 pre-existing)" |
| 14 | the 35 recheck lines' file list | `git ls-tree --name-only b49948f corpus/knowledge/ \| wc -l` and `git grep -c '^recheck:' b49948f -- corpus/knowledge \| awk -F: '{s+=$NF} END{print s}'` | `35` files, `35` lines, exactly one per file | **yes** — identical to the entry list in `c1-before.json` (`set(entries)` matches) |
| 15 | kill-rule limb (fail-closed tests not deleted) | `python3 -c "import json;d=json.load(open('.ufo/waves/round-25/c1-after.json'));print(sum(1 for e in d['entries'] if e['class']=='fail-closed'), sum(1 for e in d['entries'] if 'test -d ~/Projects/bounties' in e['command']))"` | 23 fail-closed entries, each keeping its `test -d ~/Projects/bounties` guard with the prose moved to a trailing `# on-restoration — …` comment; lane_exit=foreign_exit=2 | **yes** — 0 entries lost the guard between receipts |
| 16 | cwd pinning | `python3 -c "…startswith('cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&')…"` | before: **5** of 35 (the D24-5 figure); after: **34** of 35 — the exception is `root-loss-2026-10-12.md`, whose command is a pure `test ! -e …` (cwd-free by construction) | **yes** — D24-5's "5 of 35" is the before state only |
| 17 | C2 counter, current tree | `awk … corpus/README.md` ; `grep -lE '^source: S0(3[6-9]\|[4-9][0-9])' corpus/knowledge/*.md \| wc -l` ; `scripts/sources-census.sh validate … kasegi` | `frontier=9` ; `2` ; exit `0` | **yes** — F10 is not in `corpus/README.md` (`grep -nE '^\| *F1[0-9] '` → empty), so C2's frontier limb is unmet; `SOURCES.md` still 35 rows, so no row was appended for S036–S040 |
| 18 | round-25 receipts are untracked | `git ls-files .ufo/waves/round-25 corpus/instruments/recheck-audit.py corpus/source-snapshots/round-25 \| wc -l` | `0` | **yes** — "committed receipts only" is not satisfiable at this moment: every round-25 receipt, the instrument, and the five snapshots are working-tree files. Cite paths + digests, not commits |

### The 35 recheck files (base revision `b49948f`)

Verbatim output of `git ls-tree --name-only b49948f1164ef65106b2c4cbee3f53e8a44b8c41 corpus/knowledge/ | sed 's|corpus/knowledge/||'` (35 lines, order as git emits it):

```
ai-assisted-finding-validation.md
authorised-testing-rules-of-engagement.md
authorization-safe-harbor-and-scope.md
citation-bases.md
claim-anatomy-sample.md
claim-gates.md
claim-package-contract.md
cna-assignment-and-vulnerability-rules.md
coordinated-disclosure-timelines.md
cra-manufacturer-reporting-duties.md
cvss-v4-severity-and-vector.md
cwe-top25-2025-methodology.md
ev-model.md
evidence-dir.md
intake-and-finalize.md
intake-surface.md
mission-control.md
mission-ledger.md
multiparty-vulnerability-coordination.md
operator-queue.md
ops-invariants.md
policy-access-playbook.md
program-quirks.md
repo-git-state.md
retirement-autopsies.md
root-loss-2026-10-12.md
source-tree-loss-2026-09-28.md
statutory-authorization-and-unauthorized-access.md
submitted-registry.md
target-checkouts.md
terminal-classes.md
triage-thresholds.md
ufo-archive-2026.md
ufo-workspaces.md
vdp-disclosure-packages.md
```

At 08:35Z the working tree holds 37 such files; the two additions are
`vendor-disclosure-policies-as-corpus-objects.md` (08:31:21Z) and
`vendor-disclosure-policy-commitments-crosswalk.md`.

---

## 3. Receipt integrity and verification gaps

1. **The after receipt is unpinned in both directions** (X1, X2): no receipt records the digest of
   the instrument that produced it, and the file was rewritten in place three times. Before citing
   an after figure, the L1 should re-run the counter on a frozen tree and write a receipt whose
   `c1-instrument-digest.txt` line names the `1ccee066…` bytes (the current file still pins
   `d07af435…`).
2. **Denominator scope — the live issue.** `claims.json` C1 binds "every entry" to "35 lines". With
   37 files that binding is false, and the frozen target string `lines=35 pass=35 exit=0` cannot be
   printed by any tree that also satisfies C2. The counter now reads `lines=37 … pass=37 … exit=0`;
   the report must state the denominator change (35 → 37, C2's two entries) rather than quote the
   frozen string.
3. **No census receipt file exists** for round 25 (`.ufo/waves/round-25/` has no
   `census-before.txt`/`census-after.txt`). The `claims.json:39` figures reproduce exactly from the
   command in row 12, but there is no frozen artefact behind them.
4. **`c1-before.txt` and `c1-before.json` agree** (6 pass / 23 fail-closed / 23 parse / 6 cwd / 0
   paths) and the before line reproduces byte-for-byte on `b49948f` — the before side of C1 is the
   only part of this claim that is currently receipt-clean.
5. **Not checked here** (other seats own them): whether each rewritten line's *test* is still
   load-bearing, whether the 23 fail-closed lines still fail for the right reason, and whether the
   two new C2 entries meet QUALITY Q1–Q9 / R1–R12. This seat measured only the counters and the
   digests the report will cite.
