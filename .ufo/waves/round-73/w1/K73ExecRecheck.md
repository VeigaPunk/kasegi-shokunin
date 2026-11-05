# K73ExecRecheck — round-73 attempt 1, wave w1 — C1 (Q10 recheck cwd) repair candidate

Seat: `K73ExecRecheck` (executor, leaf). Item produced: **C1 repair candidate**, scratch-only.
Scope: 11 prefix-less first `recheck:` lines in `corpus/knowledge/`. C2 (F51 / S108) not touched.
Lane was NOT written. No git mutation in the lane. Candidate lived only in a scratch clone,
since removed (`rm -rf` exit 0; path absent afterwards).

## 0. Setup

| step | command | result |
|---|---|---|
| clone | `git clone --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin <S>/lane` | exit 0 |
| HEAD | `git -C <S>/lane rev-parse HEAD` | `3b53ff839d0747530f95d432aec1ea7b4308fe96` (freeze commit, exact) |
| toplevel | `git -C <S>/lane rev-parse --show-toplevel` | `<S>/lane` |

Tooling: no installs or upgrades. pacman not touched.

## 1. The 11 prefix-less entries (verified, not copied from the brief)

`grep -c '^recheck:'` in the clone returns 1 for each of the 11 files (one recheck line each, LF-terminated).
The census (run on the base clone, `--verbose`) flags `noprefix=1` for exactly these 11, and no other entry:

bugzilla-rest-api-bug-endpoints, cisa-vulnrichment-adp-enrichment, cisa-vulnrichment-record-list,
github-repository-security-advisories-rest-api, nvd-api-2.0-response-schema,
nvd-api-2.0-retrieval-interface, openssf-scorecard-checks, osv-affected-range-events,
project-zero-big-sleep-sqlite-variant-analysis, project-zero-fuzzilli-vs-bigsleep-comparison,
root-loss-2026-10-12.

## 2. Transformation

Script: `.ufo/waves/round-73/w1/K73ExecRecheck.prefix-recheck.py` (copy of the scratch script that was run).
It:
- aborts (exit 2, no write) unless the noprefix set equals the 11 names exactly and each target has exactly one recheck line;
- rebuilds the file by replacing only that line index, prepending `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ` to the value after `recheck: `;
- after writing, re-reads each file and asserts the new recheck is prefixed and that no other recheck line changed.

Runs:
- `python3 prefix-recheck.py <S>/lane` (dry-run) → first attempt **exit 1**: `AssertionError` at my own
  `new_text.count(line) == 1` check. Cause: the assertion was inverted (after a correct substitution the old line
  count is 0). No file was written by that run. Assertion fixed; the replacement was changed to index-based rebuild.
- dry-run after fix → `SET-OK noprefix=11 exactly the expected 11`, 11 OLD/NEW pairs, `DRY-RUN no files written`, exit 0.
- `--apply` → `APPLIED 11 files; post-apply noprefix scan clean (0 prefix-less)`, exit 0.

## 3. Prefix-only proof

`git -C <S>/lane diff -U0 -- corpus/knowledge` → 11 files. Checked with a small parser, per file: removed lines = 1,
added lines = 1, and `added[len('recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && '):] == removed[len('recheck: '):]`.
Result: `FILES=11 ALL-PREFIX-ONLY=True`, exit 0. `git status --porcelain` lists only the 11 `corpus/knowledge/*.md` as modified.

Patch saved:
- `.ufo/waves/round-73/w1/K73ExecRecheck.patch` (-U0), sha256 `2e81452c4264020b799c9a9157795f29e853e8ac5a27f7e0e722ca5e0ef6be70`, 15378 bytes.
- `.ufo/waves/round-73/w1/K73ExecRecheck.U3.patch` (-U3, same change, context-bearing), sha256 `13fcd318…a37`, 24077 bytes.

Apply check (fresh scratch clone at 3b53ff83, toplevel verified):
- `git apply --check K73ExecRecheck.patch` → **exit 1** (`patch does not apply`). Cause: `-U0` hunks carry no context and
  git apply needs `--unidiff-zero` for them. The removed lines do match the freeze commit byte for byte
  (`cmp` of `git show 3b53ff83:corpus/knowledge/bugzilla-rest-api-bug-endpoints.md | sed -n 6p` vs the patch `-` line: exit 0).
- `git apply --check --unidiff-zero K73ExecRecheck.patch` → exit 0. `git apply --unidiff-zero` → exit 0.
  `git diff --stat` → `11 files changed, 11 insertions(+), 11 deletions(-)`.
- Re-generated `-U0` diff from the applied scratch tree is byte-identical to the saved patch (`cmp` exit 0).
- Use `--unidiff-zero` with the -U0 patch, or apply the U3 patch with plain `git apply`.

## 4. Counter on the candidate (the C1 predicate)

Command: `TMPDIR=<S> python3 <S>/lane/corpus/instruments/recheck-cwd-census.py --root <S>/lane --verbose`
(full output: `.ufo/waves/round-73/w1/K73ExecRecheck.census-after.txt`).

```
RECHECK-CWD entries=88 noprefix=0 exit2_foreign=0 exit0_foreign=66 exit1_foreign=22 exit_other=0 norecheck=0
RECHECK-CWD-RESULT conformant
AFTER-EXIT=0
```

Predicted by claims.json `after_predicate`: `entries=88 noprefix=0 exit2_foreign=0 exit0_foreign=66 exit1_foreign=22 exit_other=0 norecheck=0`, `conformant`, exit 0. **Exact match.**

Also run on the freshly applied `--unidiff-zero` tree (scratch): same line, `counter-exit=0`.

Base reproduction (the same script on the untouched clone, `census-before.txt`):
```
RECHECK-CWD entries=88 noprefix=11 exit2_foreign=10 exit0_foreign=56 exit1_foreign=22 exit_other=0 norecheck=0
RECHECK-CWD-RESULT nonconformant
BASELINE-EXIT=1
```
Matches the frozen `census_at_base_fdf17413`. No predicted-vs-observed mismatch to report.

Per-entry state diff (kill-rule checks):
- exit1 set: `diff` of the 22 `foreign_exit=1` ENTRY lines, before vs after (names sorted, noprefix column stripped) → identical, diff exit 0. Count 22 → 22.
- exit2 set: before = the 10 names `bugzilla-rest-api-bug-endpoints, cisa-vulnrichment-adp-enrichment, cisa-vulnrichment-record-list, github-repository-security-advisories-rest-api, nvd-api-2.0-response-schema, nvd-api-2.0-retrieval-interface, openssf-scorecard-checks, osv-affected-range-events, project-zero-big-sleep-sqlite-variant-analysis, project-zero-fuzzilli-vs-bigsleep-comparison`; after = 0 (`grep -c foreign_exit=2` → 0).
- exit0 56 → 66 = 56 + the 10 that left exit 2. `root-loss-2026-10-12.md` was already exit 0 at base and stays exit 0 (noprefix 1 → 0).

## 5. Selftest

Command: `TMPDIR=<S> python3 <S>/lane/corpus/instruments/recheck-cwd-census.py --selftest`
(output: `.ufo/waves/round-73/w1/K73ExecRecheck.selftest.txt`).

```
selftest case=prefix-census ok got=entries=3,exit0_foreign=2,exit1_foreign=0,exit2_foreign=1,exit_other=0,noprefix=2,norecheck=0 want=entries=3,exit0_foreign=2,exit1_foreign=0,exit2_foreign=1,exit_other=0,noprefix=2,norecheck=0
selftest cases=1 failures=0
SELFTEST-EXIT=0
```

## 6. Pin hits (gate impact)

Search 1 (`git grep -n -E 'bugzilla-rest|cisa-vulnrichment|github-repository-security-advisories-rest|nvd-api-2.0|openssf-scorecard-checks|osv-affected-range|project-zero-big-sleep-sqlite|project-zero-fuzzilli|root-loss-2026' -- corpus/instruments .ufo/waves`, on the lane working tree): 1338 lines, `PINGREP-EXIT=0`. Almost all hits are path mentions in historical round receipts, README/ledger prose, or citation-survival rows, not hashes or byte counts.

Search 2 (committed-tree pins). For each base file I computed its git blob id and its sha256 at 3b53ff83, then grepped the committed tree (`git grep -l -E "<blob>|<sha256>" 3b53ff83`):

| knowledge file (base) | base sha256 (12) | committed hits at 3b53ff83 | hit location | pin kind | gate that reads it | gate turned red by C1? |
|---|---|---|---|---|---|---|
| cisa-vulnrichment-adp-enrichment.md | d2d326526dd8 | 1 | `.ufo/waves/round-51/freeze.txt:22` | freeze record, sha256 | none (see below) | no (not read) |
| nvd-api-2.0-retrieval-interface.md | 58efe5ad1a85 | 1 | `.ufo/waves/round-52/freeze.txt:23` | freeze record, sha256 | none (see below) | no (not read) |
| nvd-api-2.0-response-schema.md | 15eb2d05e88d | 2 | `.ufo/waves/round-54/controls/d53-base-greps-r54.txt:16` (`sha256sum` output of the base entry); `.ufo/waves/round-54/controls/routed-d53-corrections.md:41` (prose) | base-grep receipt + prose record | none (see below) | no (not read) |
| bugzilla-rest-api-bug-endpoints.md | b74bbe61f971 | 0 | — | — | — | — |
| cisa-vulnrichment-record-list.md | 42a09fc46f89 | 0 | — | — | — | — |
| github-repository-security-advisories-rest-api.md | 0d91a7336389 | 0 | — | — | — | — |
| openssf-scorecard-checks.md | d2f4be38f726 | 0 | — | — | — | — |
| osv-affected-range-events.md | ebe9652f765a | 0 | — | — | — | — |
| project-zero-big-sleep-sqlite-variant-analysis.md | d3bb4f0f1ba6 | 0 | — | — | — | — |
| project-zero-fuzzilli-vs-bigsleep-comparison.md | 53aca05e5465 | 0 | — | — | — | — |
| root-loss-2026-10-12.md | e021ceabfad3 | 0 | — | — | — | — |

Byte-count pins: `grep -n -E '<each name>.*[0-9]+ ?(bytes|B\b)'` over committed `corpus/instruments` → no hits (exit 0 from the pipeline's `cut`; empty output).
One byte-count string exists in a historical receipt: `.ufo/waves/round-54/controls/routed-d53-corrections.md:32` quotes `(543 lines, 7590 bytes; …)` on a `source:` line for nvd-api-2.0-response-schema. [INFERENCE] it describes the source capture (S085), not the entry's own bytes; not verified beyond the surrounding text, and no committed instrument reads that receipt.

Why no gate is red:
- `corpus/instruments/freeze-check.py` consumes one claims file per run (`--claims FILE --tool-root DIR --base DIR`, `corpus/instruments/README.md:995`). Its only directory walk is `os.walk(base)` at line 53; I did not read the walk body, so whether it reaches round-51/52 receipts is unverified [INFERENCE: it does not, since the round-73 claims pin no knowledge bytes].
- `git grep` of committed `corpus/instruments` and `scripts` for `freeze.txt`, `d53-base-greps`, `routed-d53` and `round-5[124]/` returns only the `r43-closure.sh` / `r43-limbs/k19-freeze.sh` round-43 freeze checks (not these files) and `citation-survival.*` citation rows.
- So the round-51 / 52 / 54 freeze and d53 receipts are historical records of the base digest, and nothing in the committed instruments recomputes them. Repairing the 11 files does not turn any committed gate red. Those receipts remain true statements about the base commit.

Unrun (named so the L1 can decide): `recheck-audit.py` (its `cdroot` strict limb compares the cd target to the audit root; the repaired lines use the canonical lane path, the same as the 77 entries already prefixed, so behaviour matches them, but the audit was not run); `frontier-recheck-count.py`, `knowledge-expected` and `capture-binding` (C2 counters; not in this seat's scope).

## 7. Finding for the L1

- The `-U0` patch needs `git apply --unidiff-zero`; a plain `git apply` fails. Integrate with `--unidiff-zero`, or use the `.U3.patch`. The L1 should verify with `git apply --check` on a clean tree before applying.
- The first dry-run crashed on my own inverted assertion (exit 1, no write). Recorded for honesty; the final script is the one that ran the apply.

## 8. Verdict

C1 candidate: predicate met

Failing entries: none. Census `entries=88 noprefix=0 exit2_foreign=0 exit0_foreign=66 exit1_foreign=22 exit_other=0 norecheck=0`, `RECHECK-CWD-RESULT conformant`, exit 0; selftest `cases=1 failures=0`, exit 0.

## 9. Evidence files (under .ufo/waves/round-73/w1/)

- `K73ExecRecheck.patch` (-U0, 15378 bytes, sha256 2e81452c…6be70)
- `K73ExecRecheck.U3.patch` (-U3, 24077 bytes, sha256 13fcd318…e915a37)
- `K73ExecRecheck.prefix-recheck.py` (transform script)
- `K73ExecRecheck.census-before.txt` (base census, `BASELINE-EXIT=1`)
- `K73ExecRecheck.census-after.txt` (candidate census, `AFTER-EXIT=0`)
- `K73ExecRecheck.selftest.txt` (`SELFTEST-EXIT=0`)

Scratch `/fast/scratch/hyaku/kasegi-r73/K73ExecRecheck` removed (`rm -rf` exit 0; absent afterwards).
