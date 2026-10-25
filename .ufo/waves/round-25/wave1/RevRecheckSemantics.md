# RevRecheckSemantics — per-file `recheck:` semantics, round 25 wave 1

Seat: `L1Kasegi25.RevRecheckSemantics` (leaf, read-only). Lane:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base revision
`b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. This seat made **no production edit**; its only output is
this file. No tool install or upgrade was performed (nothing needed: `bash`, `python3`, `git` already
present). No VCS write, no spawn, no background job.

Purpose: the semantics the C1 fix must preserve, one row per entry, measured against the bytes on
disk — the reference wave 2 reviews the fix against.

---

## 1. Method and state of the tree

Three states are measured and kept separate, because the fix landed in the working tree while this seat
was reading:

| state | source | lines | pass | fail-closed | limbs failing |
|---|---|---|---|---|---|
| frozen **before** | `.ufo/waves/round-25/c1-before.json` (L1, committed) | 35 | **6** | 23 | parse 23, cwd 6, paths 0, exit 1 |
| live **after** (first read, 05:26Z) | this seat's re-run, 35-entry corpus | 35 | **35** | 23 | parse 0, cwd 0, paths 0, exit 0 |
| live **at write time** (08:36Z) | this seat's re-run, 37-entry corpus | 37 | **35** | 25 | parse 0, cwd 0, **paths 2**, exit 1 |

The **35-row table in §3 is the frozen 35 entries** — that is the set the assignment names and the set
C1 froze. Two further entries appeared in `corpus/knowledge/` during this seat (C2's F10 work) and
break the C1 denominator; see §10, which the wave-2 review must read before quoting `pass=35`.

Commands run by this seat (all read-only):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py --json /tmp/r25-live.json --quiet
  -> lines=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0   (audit-exit=0)
for f in corpus/knowledge/*.md; do python3 corpus/instruments/anchorcheck.py "$f"; done   # per-entry verdict summary
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-{23,24}/manifest.json --source <id>
python3 corpus/instruments/frontier-recheck-count.py   -> entries=10 pass=10 exit=0
for p in bounties the-bounty-hunter origin-work ufo-fsd-alpha; do test -e ~/Projects/$p; done
  -> bounties ABSENT, the-bounty-hunter ABSENT, origin-work ABSENT, ufo-fsd-alpha EXISTS
```

`class` below is the receipt's own field (`passing` = the line exits 0 from the lane root;
`fail-closed` = it exits non-zero because its base is absent). In the frozen-35 set, 12 entries are
`passing` and 23 `fail-closed` in **every** receipt — the fix changed form, not class.

One measured change the review must not mistake for a preserved byte: the 23 fail-closed lines exited
**2** before (a bash syntax error on prose) and exit **1** now (`test -d` false is the last executed
command of the `&&` chain). Fail-closed is preserved; the numeric code is not.

---

## 2. What the two instruments actually certify

**`corpus/instruments/source-recheck.py`** (the 10 `S###` entries). Exit 0 ⇔ for every `--source` id
the named local capture hashes to its manifest `sha256` **and** every quote listed for it still occurs
in the captured bytes. It prints one `<id>:sha256 OK` line plus one line per quote. It reads only
`corpus/source-snapshots/**` — a successful check is **capture integrity, not upstream freshness**
(its own docstring, and QUALITY Q7). A stale capture passes forever.

**`corpus/instruments/anchorcheck.py`** (23 entries, incl. `citation-bases.md`). It prints verdict
classes (`IN-RANGE`, `MISSING-FILE`, `PAST-EOF`, `BASE-ABSENT`, `LOST-RECORDED`, …) and a summary, but
**`main()` has no return statement and the module ends `sys.exit(main(...))` → exit status 0 for every
verdict class**. Measured, three ways:

| probe | verdict printed | exit |
|---|---|---|
| `anchorcheck.py corpus/knowledge/claim-gates.md` | `0 in-range, 0 bad` | **0** |
| `anchorcheck.py corpus/knowledge/citation-bases.md` | `10 in-range, 0 bad … BASE-ABSENT=1` | **0** |
| copy of `citation-bases.md` with `[lost-*]` markers stripped, `KASEGI_MIRROR=/tmp/acprobe/fakemirror` | `2 bad`, two `MISSING-FILE` lines | **0** |

So for every `anchorcheck`-gated line that carries a `test` clause (22 of the 23), the line's **exit
status is decided entirely by that clause**; for `citation-bases.md` (no `test`) it is constant 0.
`anchorcheck` contributes printed evidence to a human reader and nothing to the exit code;
it can only exit non-zero by crashing (missing argv / unreadable file).

Second measured limit, which governs the 23 legacy entries: `anchorcheck`'s citation matcher
(`CITE`) accepts `~/Projects/origin-work/open-bug-bounties/…`, `~/Projects/the-bounty-hunter/…`, a
lane-relative prefix (`corpus|ops|claims|docs|…`), or a bare filename — **there is no
`~/Projects/bounties/` arm**. Measured against the imported matcher:

```
NO-MATCH  ~/Projects/bounties/ops/claim-check.mjs:22
NO-MATCH  ~/Projects/bounties/ops/claim-check.mjs:1-233
MATCH     ops/claim-check.mjs:174-199
MATCH     ~/Projects/the-bounty-hunter/ops/rank.mjs:55-58
```

Every legacy entry's lost-tree citation is therefore suppressed twice over: prefixed
`~/Projects/bounties/…` it is **invisible** (not counted at all, not even `BASE-ABSENT`); marked
`[lost-tree]`/`[lost-base]` it is counted as `LOST-RECORDED` and **not checked**. A `0 bad` summary in
these files is not evidence of health.

---

## 3. The 35-row semantics table

Columns: **class** = receipt class; **base test** = the `test` clauses the line runs;
**instrument** = what the line executes; **what a reader learns when it exits 0** = the *whole*
information content of exit 0, measured, not the entry's intent; **flag** codes expand in §4.

| # | entry | class | base test | instrument | what a reader learns when it exits 0 | flag |
|---|---|---|---|---|---|---|
| 1 | `ai-assisted-finding-validation.md` | passing | none | `source-recheck.py`, round-24, S009–S012 | captures S009/S010/S011/S012 hash-match their pins and their 2/3/2/3 quotes are present (14 OK lines). Nothing about upstream. Header `source:` names only S009 while the body quotes all four. | SUPER |
| 2 | `authorised-testing-rules-of-engagement.md` | passing | none | `source-recheck.py`, round-24, S032 | NIST SP 800-115 capture hash-matches and its 6 quotes are present (7 OK lines). | — |
| 3 | `authorization-safe-harbor-and-scope.md` | passing | none | `source-recheck.py`, round-24, S006–S008 | three captures hash-match, 3+3+3 quotes present (12 OK lines). | — |
| 4 | `citation-bases.md` | passing | none | `anchorcheck.py` | **nothing.** Exit is constant 0; today's own output reports `10 in-range, 0 bad, BASE-ABSENT=1` (the absent mirror cite `~/Projects/the-bounty-hunter/ops/rank.mjs:55-58`) and still exits 0. Its in-range cites are lane files (`resolve.py` ×5, `instruments/README.md` ×2, `claim-gates.md`, `ops-invariants.md` ×2). | EXIT, LANE |
| 5 | `claim-anatomy-sample.md` | fail-closed | `bounties` | `anchorcheck.py` | after restoration: **only that `~/Projects/bounties` is a directory.** anchorcheck's 4 in-range cites are intra-lane cross-refs (`submitted-registry.md`, `claim-package-contract.md`), 1 token `LOST-RECORDED`; none touch the lost base. | PRES, EXIT, LANE |
| 6 | `claim-gates.md` | fail-closed | `bounties` | `anchorcheck.py` | only that the directory exists. anchorcheck parses **0 citations** (its single base cite is `` `~/Projects/bounties/ops/claim-check.mjs` ``, no line number, and bounties-prefixed tokens never match). | PRES, EXIT, ZERO, NOID |
| 7 | `claim-package-contract.md` | fail-closed | `bounties` | `anchorcheck.py` | only directory presence; `0 in-range`, 2 `LOST-RECORDED` (not checked). | PRES, EXIT, LOST |
| 8 | `cna-assignment-and-vulnerability-rules.md` | passing | none | `source-recheck.py`, round-23, S031 | CNA Rules 4.2.6 capture hash-matches, 10 quotes present (11 OK lines). | — |
| 9 | `coordinated-disclosure-timelines.md` | passing | none | `source-recheck.py`, round-24, S003–S005 | three captures hash-match, 3+3+5 quotes present (14 OK lines). | — |
| 10 | `cra-manufacturer-reporting-duties.md` | passing | none | `source-recheck.py`, round-23, S029 | CRA capture hash-matches, 9 quotes present (10 OK lines). | — |
| 11 | `cvss-v4-severity-and-vector.md` | passing | none | `source-recheck.py`, round-24, S001–S002 | two captures hash-match, 4+7 quotes present (13 OK lines). | — |
| 12 | `cwe-top25-2025-methodology.md` | passing | none | `source-recheck.py`, round-24, S013–S015 | three captures hash-match, 4+4+1 quotes present (12 OK lines). | — |
| 13 | `ev-model.md` | fail-closed | `bounties` + `the-bounty-hunter` | `anchorcheck.py` | only that **both** directories exist; `0 in-range`, 5 `LOST-RECORDED`. Its own text pins every `ops/ev-report.mjs` line to mirror HEAD `1cfbd86` — that HEAD is neither tested nor checked. | PRES, EXIT, LOST, NOID |
| 14 | `evidence-dir.md` | fail-closed | `bounties` | `anchorcheck.py` | only directory presence; **0 citations parsed**. | PRES, EXIT, ZERO, NOID |
| 15 | `intake-and-finalize.md` | fail-closed | `bounties` | `anchorcheck.py` | only directory presence; **0 citations parsed**. | PRES, EXIT, ZERO |
| 16 | `intake-surface.md` | fail-closed | `bounties` | `anchorcheck.py` | only directory presence; `0 in-range`, 1 `LOST-RECORDED`. | PRES, EXIT, LOST |
| 17 | `mission-control.md` | fail-closed | `bounties` | `anchorcheck.py` | only directory presence; **0 citations parsed**. | PRES, EXIT, ZERO |
| 18 | `mission-ledger.md` | fail-closed | `bounties` + `the-bounty-hunter` | `anchorcheck.py` | only that both directories exist; `0 in-range`, 2 `LOST-RECORDED`. | PRES, EXIT, LOST |
| 19 | `multiparty-vulnerability-coordination.md` | passing | none | `source-recheck.py`, round-23, S018 | FIRST CVD v1.1 capture hash-matches, 6 quotes present (7 OK lines). | — |
| 20 | `operator-queue.md` | fail-closed | `bounties` + `the-bounty-hunter` | `anchorcheck.py` | only that both directories exist; `0 in-range`, 2 `LOST-RECORDED`. | PRES, EXIT, LOST |
| 21 | `ops-invariants.md` | fail-closed | `bounties` + `the-bounty-hunter` | `anchorcheck.py` | only that both directories exist; **0 citations parsed**. | PRES, EXIT, ZERO |
| 22 | `policy-access-playbook.md` | fail-closed | `bounties` + `the-bounty-hunter` | `anchorcheck.py` | only that both directories exist; `0 in-range`, 8 `LOST-RECORDED`. | PRES, EXIT, LOST |
| 23 | `program-quirks.md` | fail-closed | `bounties` | `anchorcheck.py` | only directory presence; **0 citations parsed**. | PRES, EXIT, ZERO |
| 24 | `repo-git-state.md` | fail-closed | `bounties/.git` | none — `git -C ~/Projects/bounties rev-parse HEAD` | after restoration: `~/Projects/bounties` is a git work tree, and prints **whatever** HEAD is. No comparison with `58acb6d8`, no `rebase-merge` check, no autostash check ⇒ every fact the entry states (stalled rebase, detached HEAD, autostash `a00d4c55`) stays unverified. | PRES, EXIT, NOID |
| 25 | `retirement-autopsies.md` | fail-closed | `bounties` + `the-bounty-hunter` | `anchorcheck.py` | only that both directories exist; `0 in-range`, 2 `LOST-RECORDED`. | PRES, EXIT, LOST |
| 26 | `root-loss-2026-10-12.md` | passing | **inverted**: `test ! -e` bounties, `the-bounty-hunter`, `origin-work`; `test -e ufo-fsd-alpha` | none | **exits 0 today**: the three bases are still absent and `~/Projects/ufo-fsd-alpha` exists. Verifies no identity of `ufo-fsd-alpha` (HEAD `964f443e` untested), and exits 1 the day any base returns. | INV, NOID |
| 27 | `source-tree-loss-2026-09-28.md` | fail-closed | `bounties` | `anchorcheck.py` | only directory presence; 11 in-range cites are **all** intra-lane cross-refs (other `corpus/knowledge/*.md`, `corpus/lessons/round-4-aggregator-audit.md`), 15 `LOST-RECORDED`. | PRES, EXIT, LANE |
| 28 | `statutory-authorization-and-unauthorized-access.md` | passing | none | `source-recheck.py`, round-24, S033–S035 | three captures hash-match, 8+6+6 quotes present (23 OK lines). | — |
| 29 | `submitted-registry.md` | fail-closed | `bounties` + `origin-work` | `anchorcheck.py` | only that both directories exist; `0 in-range`, 1 `LOST-RECORDED`. | PRES, EXIT, LOST |
| 30 | `target-checkouts.md` | fail-closed | `bounties` | `anchorcheck.py` | only directory presence; **0 citations parsed** (its anchors are bare `` `:22` `` / `` `:95-133` `` tokens, which `CITE` cannot match). | PRES, EXIT, ZERO |
| 31 | `terminal-classes.md` | fail-closed | `bounties` | `anchorcheck.py` | only directory presence; **0 citations parsed**. | PRES, EXIT, ZERO |
| 32 | `triage-thresholds.md` | fail-closed | `bounties` | `anchorcheck.py` | only directory presence; 148 in-range cites, **all intra-lane** (`claim-gates.md` 50, `mission-control.md` 30, `SKILL.md` 30, `ops-invariants.md` 12, `ev-model.md` 11, `claim-package-contract.md` 10, `intake-surface.md` 5) resolved against lane bytes or the `fc6d398` SKILL pin; 18 `LOST-RECORDED`. Proves lane line-stability (R6), never the lost base. | PRES, EXIT, LANE |
| 33 | `ufo-archive-2026.md` | fail-closed | `bounties` | `anchorcheck.py` | only directory presence; **0 citations parsed**. | PRES, EXIT, ZERO |
| 34 | `ufo-workspaces.md` | fail-closed | `bounties` | `anchorcheck.py` | only directory presence; `0 in-range`, 9 `LOST-RECORDED`. Content also depends on `~/Projects/ufo-fsd-alpha` HEAD `964f443e`, which the line neither tests nor checks. | PRES, EXIT, LOST, NOID |
| 35 | `vdp-disclosure-packages.md` | fail-closed | `bounties` | `anchorcheck.py` | only directory presence; **0 citations parsed**. | PRES, EXIT, ZERO |

Totals by instrument: `source-recheck.py` 10, `anchorcheck.py` 23, none 2 (`repo-git-state`,
`root-loss`). Base-test census (35): `bounties` alone **15** (5,6,7,14,15,16,17,23,27,30,31,32,33,34,35),
`bounties`+`the-bounty-hunter` **6** (13,18,20,21,22,25), `bounties`+`origin-work` **1** (29),
`bounties/.git` **1** (24), inverted-absence **1** (26), none **11** (1,2,3,4,8,9,10,11,12,19,28).
Per-entry `anchorcheck` verdict summaries are reproduced in §7.

---

## 4. Flag codes

| code | meaning | affected entries |
|---|---|---|
| `PRES` | The gate is `test -d <base>`: **presence, not identity**. Any directory at that path satisfies it — including an empty one, or a restored but different tree. | 5–7, 13–18, 20–25, 27, 29–35 (**all 23** fail-closed lines: 22 plain + 1 `…/.git`) |
| `EXIT` | The instrument has **no failing exit path** (`anchorcheck`: `main()` returns `None`; `repo-git-state`: no comparison). Exit 0 carries no verdict information; only stdout does. | 4–7, 13–18, 20–25, 27, 29–35 |
| `ZERO` | `anchorcheck` parses **0 citations** in the file: no verdict line at all is produced. | 6, 14, 15, 17, 21, 23, 30, 31, 33, 35 |
| `LOST` | Every parseable citation is `[lost-tree]`/`[lost-base]`-marked ⇒ counted `LOST-RECORDED` and deliberately not checked. | 7, 13, 16, 18, 20, 22, 25, 29, 34 |
| `LANE` | The in-range cites are intra-lane cross-references (other corpus files / a lane git pin), never the lost base. | 4, 5, 27, 32 |
| `NOID` | No identity pin on the base: no HEAD sha, sentinel, or checksum distinguishes the restored tree from a different one. | 6, 13, 14, 24, 26, 34 |
| `INV` | The line asserts **absence**; it passes today and inverts on restoration. | 26 |
| `SUPER` | Header `source:` id set is a proper subset of the line's `--source` set (body cites the rest). Correct as written, under-read from the header. | 1 |

---

## 5. Lines whose `test` would pass today

Measured: `~/Projects/bounties`, `~/Projects/the-bounty-hunter`, `~/Projects/origin-work` are all
**ABSENT**; `~/Projects/ufo-fsd-alpha` **EXISTS**.

- **No fail-closed line's `test` passes today.** All 22 `test -d` gates and the one `test -d …/.git`
  gate fail on absent directories — that is the fail-closed base, and it is real.
- **One line passes today in full: `root-loss-2026-10-12.md`** (`exit 0`). It is a negative test
  (`test ! -e` ×3 plus `test -e ufo-fsd-alpha`), so passing today is the design, not a defect. It is
  the only line in the corpus whose exit 0 is informative about the present filesystem, and it is
  informative only about *presence*, not identity.

---

## 6. Entries whose recheck cannot ever verify anything, even after restoration

Tier 1 — **no verdict is even produced** (10 entries; `anchorcheck` parses zero citations, so the
output is an empty summary line):
`claim-gates.md`, `evidence-dir.md`, `intake-and-finalize.md`, `mission-control.md`,
`ops-invariants.md`, `program-quirks.md`, `target-checkouts.md`, `terminal-classes.md`,
`ufo-archive-2026.md`, `vdp-disclosure-packages.md`.

Tier 2 — **every parseable citation is `LOST-RECORDED`** (9 entries; verdicts exist only as "not
checked"): `claim-package-contract.md`, `ev-model.md`, `intake-surface.md`, `mission-ledger.md`,
`operator-queue.md`, `policy-access-playbook.md`, `retirement-autopsies.md`,
`submitted-registry.md`, `ufo-workspaces.md`.

Tier 3 — **verdicts exist but the exit status cannot fail** (all 23 `anchorcheck` lines, incl.
`citation-bases.md`). For the 3 of them that do check lane citations — `claim-anatomy-sample.md` (4),
`source-tree-loss-2026-09-28.md` (11), `triage-thresholds.md` (148) — a reader can learn that lane
line numbers still resolve, but only by reading stdout; `MISSING-FILE` exits 0 (measured).

Tier 4 — **no comparison at all** (1 entry): `repo-git-state.md` prints `git rev-parse HEAD` and
compares it to nothing.

Outside the four tiers: `root-loss-2026-10-12.md` verifies presence/absence only, never the identity
of `ufo-fsd-alpha`, and inverts on restoration.

Net: **19 of the 23 fail-closed entries produce no checked citation even after restoration**, and the
remaining 4 (`claim-anatomy`, `source-tree-loss`, `triage-thresholds`, `repo-git-state`) check only
lane stability or print-only facts. The 10 `S###` entries are the only lines whose exit 0 carries
substantive, failing-capable evidence — and it is capture integrity, not freshness.

---

## 7. Ambiguity register (for the wave-2 review of the fix)

1. **Restored but different tree — the named case, and it is real for all 23 `PRES` lines.**
   `test -d` proves a directory exists. Because `anchorcheck`'s exit is constant 0, restoring
   `~/Projects/bounties` as an **empty** directory would turn the **15** bounties-gated lines green
   with zero verification (5,6,7,14,15,16,17,23,27,30,31,32,33,34,35); restoring the mirror as well
   takes it to **21**; adding `origin-work` to **22**; `repo-git-state` additionally needs a real repo
   with at least one commit (**23**). Any restoration contract must therefore add an identity pin (a
   sentinel file, a HEAD sha, or a manifest like the `S###` captures) or these lines' exit 0 will
   overclaim exactly what §6 says they cannot deliver.
2. **`test -d ~/Projects/bounties/.git`** (`repo-git-state`) passes on any repository with at least
   one commit, including a fresh `git init && git commit`. An empty repo fails (`rev-parse` exits
   128), which is the only discrimination the line has.
3. **`citation-bases.md` prints a live loss and exits 0.** Its own output today contains
   `BASE-ABSENT md:31 ~/Projects/the-bounty-hunter/ops/rank.mjs:55-58`. A reader who trusts exit
   status — which is what the C1 predicate measures — misses the recorded loss entirely.
4. **`~/Projects/bounties/…:NN` tokens are invisible, not merely unopenable.** `CITE` has no bounties
   arm (measured `NO-MATCH`). These citations are not counted as `BASE-ABSENT`, so a `0 bad`
   summary in a legacy entry is not evidence that its base citations are well-formed.
5. **The `# on-restoration — …` note is inert text.** The fix moved the fail-closed rationale into a
   shell comment, which preserves the words but creates no obligation: nothing re-runs these lines
   when a base returns, and exit 0 cannot distinguish "restored and checked" from "never checked".
6. **Exit code changed 2 → 1 on the 23.** Fail-closed is preserved; byte-identity is not. A review
   comparing before/after codes must read both as "non-zero for an absent base", not as a regression.
7. **`root-loss-2026-10-12.md` inverts.** On restoration it exits 1. That is correct for a loss
   record but will read as a breakage to a future seat; it needs the same "expected failure" marking
   the other 23 lines now carry.
8. **`ufo-fsd-alpha` is never pinned.** `root-loss` tests presence and `ufo-workspaces` cites HEAD
   `964f443e`; no line tests or compares that HEAD, though the tree exists right now — the one base
   that could be verified today is not.
9. **`ai-assisted-finding-validation.md` header/recheck asymmetry.** Header `source:` names S009;
   the line checks S009–S012 and the body quotes all four. The line is a superset (allowed by R12's
   coverage reading, and `frontier-recheck-count.py` passes it: `ids=S009 … exit=0`), but a
   header-only reader under-reads the entry's provenance.
10. **The 10 `S###` lines cannot detect staleness.** Their manifests are fixed local captures
    (`corpus/source-snapshots/round-23|24/*.txt`, `stem == id` for all 23 records — Q9 satisfied).
    Exit 0 means the capture still matches itself; a source that changed upstream passes forever.

---

## 8. Invariants the fix must preserve (checklist for wave 2)

- 35 entries, one `recheck:` line each; `lines=35` in the receipt.
- `fail-closed=23` — no `test` clause deleted, relaxed, or converted to `true`; every base test kept
  verbatim (`bounties` 15, `bounties`+`the-bounty-hunter` 6, `bounties`+`origin-work` 1,
  `bounties/.git` 1, inverted-absence 1).
- The 10 `source-recheck.py` lines keep their `--source` id sets and their manifest: round-24 ×7
  (entries 1, 2, 3, 9, 11, 12, 28), round-23 ×3 (8, 10, 19); `frontier-recheck-count.py` stays
  `entries=10 pass=10 exit=0`.
- `root-loss-2026-10-12.md` stays **passing** (inverted test) and is not "fixed" into a
  fail-closed line — that would misdescribe the present filesystem.
- `citation-bases.md` stays `anchorcheck`-gated and **passing**; its `BASE-ABSENT=1` is expected.
- The 23 lines' `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` prefix stays absolute, so the
  foreign-cwd digest equality holds (measured `cwd_fail=0`).
- No entry gains a passing exit 0 by deletion of its base test (the C1 kill rule).

## 9. Residual risk and verification gaps

- §6 is a statement about **exit-status** semantics. It is not a claim that the entries are
  worthless: `anchorcheck`'s stdout is real evidence for a human, and 3 legacy entries do check
  intra-lane line stability. The gap is that the C1 predicate measures the exit code, so `pass=35`
  certifies form only — 23 of those 35 lines certify nothing beyond "a directory exists" or nothing
  at all.
- This seat did not run `anchorcheck` against a restored tree (no base exists to restore, and
  fabricating one would be a fabricated verdict). The restored-but-different-tree behaviour in §7.1
  is derived from the code path (`test -d` then constant-0 instrument), and the constant-0 part is
  measured in §2.
- The live tree moved under this seat (the C1 fix landed while reading, then C2's entries landed).
  Class and base tests of the frozen 35 are stable across both receipts; every per-entry verdict
  summary in §3/§7 was measured on the current working-tree bytes, which differ from `b49948f` in the
  29 `recheck:` lines (`git diff -U0 -- corpus/knowledge` → 29 insertions / 29 deletions, **0** changed
  lines that are not `recheck:` lines) plus two untracked files (see §10).

---

## 10. Live drift at write time (08:36Z, measured) — read before quoting `pass=35`

Three changes landed after the frozen receipts, and they move the C1 denominator. Recorded here
because the wave-2 review of the fix will otherwise compare against a stale count.

**(a) The corpus grew from 35 to 37 entries.** Two untracked files now exist:

```
?? corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md     (F10, sources S036–S039)
?? corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md  (F10, sources S040,S036,S038,S039)
```

**(b) Both new lines fail the `paths` limb and exit 2.** Measured on live bytes:

```
lines=37 total=37 pass=35 fail-closed=25 parse_fail=0 cwd_fail=0 paths_fail=2 exit=1
  vendor-disclosure-policies-as-corpus-objects.md  missing=['corpus/source-snapshots/round-25/manifest.json'] lane=2
  vendor-disclosure-policy-commitments-crosswalk.md missing=['corpus/source-snapshots/round-25/manifest.json'] lane=2
```

`corpus/source-snapshots/round-25/` exists and holds `S036.txt … S040.txt` (written 05:14Z), but
**there is no `manifest.json`** in it. `source-recheck.py` therefore prints
`manifest UNAVAILABLE reason=missing` and exits 2 for every `--source` in those lines. Until the
round-25 manifest lands (with `stem == id` paths and sha256 pins, per Q9), these two entries are
fail-closed for a **missing instrument input**, not for an absent base — a different failure class
from the 23 legacy lines.

**(c) The counter instrument changed at 05:34:28Z.** `corpus/instruments/recheck-audit.py` grew from
3 to 7 strict limbs (`cdroot`, `instrument`, `artifact`, `own`) plus a global completeness term, and
now prints `pass` (the frozen (a)(b)(c) limbs) alongside `pass_strict`. The frozen limbs keep their
meaning, so C1's predicate is still measurable; but the receipt schema changed mid-round and
`.ufo/waves/round-25/c1-after.json` was rewritten **twice** under it — this seat observed it holding
`lines=36 pass=35 paths_fail=1 pass_strict=35` (36-entry run, 05:33Z) and then the live 37-entry run
above. Two different denominators for the same claim is the D24-2 / R11 pattern: one artefact must
carry one measured number.

**Consequence for wave 2.** C1's frozen target is `lines=35 pass=35 exit=0`. On live bytes the counter
reads `lines=37 pass=35 exit=1`, so **the target is currently not met** and cannot be met while the
two new entries name a nonexistent manifest. Either (i) the round-25 manifest lands and both entries
pass, making the honest receipt `lines=37 pass=37 exit=0` — which requires re-freezing the
denominator with L1's approval, or (ii) the entries leave `corpus/knowledge/` until their manifest
exists, restoring `lines=35 pass=35`. My 35-row table is the invariant either way: it describes what
each of the frozen 35 lines certifies, and nothing in §3 changes with the denominator.
