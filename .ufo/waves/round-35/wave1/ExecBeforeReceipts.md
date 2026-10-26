# ExecBeforeReceipts — round-35 wave 1 (leaf)

Replay window: 2026-10-26T06:31Z–06:35Z (all fleet-state statements below are time-stamped to
that window; seats landing after it are out of this receipt's scope).

Role: replay the frozen before-controls of round 35 at the claims-freeze commit and confirm every
stored value in `c1-controls/before.txt` and `c2-controls/before.txt` (plus `census-before.txt`)
matches on the freeze bytes. Advisory only: findings for the L1, no round verdict, no lane commit.

- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- Lane base: `3266c9937b03062d9bbc2f436e20820115ed179c`
- Claims-freeze commit (replayed): `617496b9c6e92bc671e7e78b83df69a04470d0e9`
- Live lane HEAD at seat start (read only): `da2d3c687f82a9814ee71c91c930cb733050d37c`
- Scratch: `/fast/scratch/hyaku/kasegi-r35/ExecBeforeReceipts/` (deleted at exit; receipt copied first)
- Tools installed/upgraded: **none** (nothing was needed; no pacman, uv, npx or cargo transaction ran)

## Report

### 1. Export + provenance

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git archive 617496b9c6e92bc671e7e78b83df69a04470d0e9 > $S/freeze.tar          # exit 0
$ git get-tar-commit-id < $S/freeze.tar
617496b9c6e92bc671e7e78b83df69a04470d0e9                                        # exit 0
$ sha256sum $S/freeze.tar
a008adf24ed9fa5c93e35b51c84b2dc2df0fe60722098a481f222ac71782467a              # 115,701,760 B
$ git archive 617496b9… | tar -x -C $S --one-top-level=freeze                    # exit 0, 6934 files
```

`git get-tar-commit-id` echoes the freeze commit, so the extracted tree is provably the committed
tree of `617496b9` (no untracked, no gitignored, no `.git` — the replay therefore also proves the
controls do not depend on git state).

Base-vs-freeze wording: `c1-controls/before.txt:1` is headed "base 3266c993…". The freeze commit is
purely additive over that base, so replaying at the freeze commit and at the base are the same tree
for every probed path:

```
$ git diff --stat 3266c9937b03062d9bbc2f436e20820115ed179c 617496b9c6e92bc671e7e78b83df69a04470d0e9
 .ufo/waves/round-35/c1-controls/before.txt | 26 +++++++++
 .ufo/waves/round-35/c2-controls/before.txt | 16 ++++++
 .ufo/waves/round-35/census-before.txt      |  5 ++
 .ufo/waves/round-35/claims.json            | 87 ++++++++++++++++++++++++++++++
 4 files changed, 134 insertions(+)
```

Byte identity of every probed file, export vs `git cat-file blob 617496b9:<path>` (7/7 MATCH):

```
MATCH  SCORECARD.md                                        efa646c83baead97e41d9ccad65fac9a4d8468f6bb8af956446d347d68237e91
MATCH  SKILL.md                                            ba5ebe5d9417b1801d48bbdb8fa533eb9df586f588bbad398eacd062e408163e
MATCH  corpus/QUALITY.md                                   807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8
MATCH  corpus/README.md                                    876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29
MATCH  corpus/SOURCES.md                                   4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6
MATCH  .ufo/waves/round-34/wave1/L1Integration.md          5472f60ab33a2241e7051c071e1469ca89b2c874e571d93420499cd0998a0fd5
MATCH  corpus/lessons/round-34-verifier-spotcheck.md       dc10c6501a1992abb08880b1f8d8477992db70b03b3b3f985557036d0752748e
```

### 2. claims.json is the committed bytes, unmodified

```
$ git rev-parse 617496b9:.ufo/waves/round-35/claims.json
0364c426ef605c88b7b9e7d32f1d6c846ede6fff
$ git show 617496b9:.ufo/waves/round-35/claims.json | sha256sum
fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982  -
$ sha256sum <export>/.ufo/waves/round-35/claims.json
fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982  <export>/…/claims.json
$ sha256sum .ufo/waves/round-35/claims.json            # lane worktree
fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982  .ufo/waves/round-35/claims.json
$ git show HEAD:.ufo/waves/round-35/claims.json | sha256sum
fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982  -
$ git hash-object .ufo/waves/round-35/claims.json
0364c426ef605c88b7b9e7d32f1d6c846ede6fff
$ wc -c  # export and worktree
 7112 /fast/…/freeze/.ufo/waves/round-35/claims.json
 7112 .ufo/waves/round-35/claims.json
```

Freeze blob, HEAD blob and worktree file are all sha256 `fe0dae89…` / blob sha1 `0364c426…`
(7112 B): the frozen claims have not drifted since freeze — including under the wave that is
currently landing.

Stored control receipts themselves are also unmodified (freeze blob = worktree = HEAD):

```
.ufo/waves/round-35/c1-controls/before.txt   352d3da210283dc2d328b22ba27d9abd39eacc2f99ebcff2d4101532d582dd61
.ufo/waves/round-35/c2-controls/before.txt   2835700332ac682e25bd68523d7eb126b1e8980aca92144b9c9a63e37de77327
.ufo/waves/round-35/census-before.txt        74fc6a26d8d3ec9bc89903b410b828e82c8b35cc686fd7a586260aedec15867b
```

### 3. C1 per-line match report (`c1-controls/before.txt`)

All commands run with cwd = the freeze export root. "stored" = the value on the receipt line
named in `path:line`; "got" = this replay (`.ufo/waves/round-35/wave1/ExecBeforeReceipts.md` §3).

Caveat carried from rounds 33–34: the stored receipts are output-only, so the commands below are
reconstructed from each receipt's own section labels (`-- r35-defect-closure.sh presence --`,
`-- D1: … --`, …). Matching every stored value is evidence the frozen numbers are reproducible from
the frozen bytes; it is not proof that the L1's original argv was character-identical.

| stored line | control | command (as replayed) | stored | got | exit | verdict |
|---|---|---|---|---|---|---|
| `04-06` | r35-defect-closure.sh presence | `ls corpus/instruments/r35-defect-closure.sh` | `ls: cannot access …: No such file or directory` / `ls_exit=2` | same message, `exit=2` | 2 | MATCH |
| `07-08` | D1 `filled by the L1` | `grep -c 'filled by the L1' SCORECARD.md` | `1` | `1` | 0 | MATCH |
| `09-10` | D1 round-34 tip hash citations | `grep -c 'c1c6a5f' SCORECARD.md` | `0` | `0` | 1 | MATCH |
| `11-12` | D2 stale `201.7` | `grep -c '201\.7' SCORECARD.md` | `2` | `2` | 0 | MATCH |
| `13-14` | D2 corrected `201.2` | `grep -c '201\.2' SCORECARD.md` | `0` | `0` | 1 | MATCH |
| `15-16` | D3 registry rows | `grep -cE 'r-defect-closure\.sh\|kill-rule-check\.py' SKILL.md` | `0` | `0` | 1 | MATCH |
| `17-18` | D4 results tracked | `ls .ufo/waves/round-34/wave1-results.json \| wc -l` | `0` | `0` | 0 | MATCH |
| `17-18` | D4 results tracked (index) | `git ls-tree -r --name-only 617496b9 -- .ufo/waves/round-34/wave1-results.json \| wc -l` | `0` | `0` | 0 | MATCH |
| `19-20` | D4 provenance note | `find .ufo/waves/round-34 -maxdepth 1 -name '*provenance*' -type f \| wc -l` | `0` | `0` | 0 | MATCH |
| `21-22` | D5 erratum present | `find . -name 'claims-erratum-d5.md' -type f \| wc -l` | `0` | `0` | 0 | MATCH |
| `23-24` | D6 dead-seat sentence | `grep -c 'did not file a receipt (dead seat' .ufo/waves/round-34/wave1/L1Integration.md` | `1` | `1` | 0 | MATCH |
| `25-26` | D7 supersedes rows | `grep -c 'supersedes-R22' corpus/QUALITY.md` / `supersedes-R23` | `0 0` | `0 0` | 0 | MATCH |

Named locations behind the two non-trivial counts (quoted from the freeze export):

- D1 — `SCORECARD.md:1240`: `**Round-34 final lane commit: filled by the L1 in the closing commit.** Every value in this section`
- D2 — `SCORECARD.md:1003` (round-33 table, depth:density): `| depth:density | 9 | mean 191.5, … | mean **201.7**, 25 blocks, 710 cites (…) …`
  `SCORECARD.md:1145` (round-34 table, depth:density): `| depth:density | 9 | mean **201.7**, 25 blocks, 710 path-citation instances … | mean **201.7**, 25 blocks, 710 cites, 1090 lines; SKILL.md and PR…`
- D6 — `.ufo/waves/round-34/wave1/L1Integration.md:30`: `- The round-33 summary \`ExecRegressionC1\` did not file a receipt (dead seat, 1 of 65); the`
- D3 — `grep -n 'r-defect-closure\|kill-rule-check' SKILL.md` → 0 lines, although
  `corpus/instruments/kill-rule-check.py` and `corpus/instruments/r-defect-closure.sh` both exist in
  the export (present-but-unregistered, exactly as D3 states). `SKILL.md:977` is the registry home
  (`## Gates & probes registry`), followed by appended per-round sections at `:1037`, `:1050`, `:1060`.
- D7 — `corpus/QUALITY.md:226` R22 and `:227` R23 exist, and no supersession targets either id:
  `grep -c 'supersedes-R22'` = 0, `grep -c 'supersedes-R23'` = 0. The word "supersedes" does occur
  6× in `QUALITY.md` at freeze (`:50` R8 prose, `:102` R18, `:103` R19, `:153-155` an embedded shell
  snippet that greps `supersedes R13`) — none of them is an R22/R23 supersession row, so a global
  `grep -c supersedes` is *not* a valid closure test for D7; the id-scoped count is.

### 4. C2 per-line match report (`c2-controls/before.txt`)

| stored line | command (as replayed) | stored | got | exit | verdict |
|---|---|---|---|---|---|
| `02-03` frontier admitted | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `17` | `17` | 0 | MATCH |
| `04-05` registry rows | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `51` | `51` | 0 | MATCH |
| `06-07` S052 rows | `grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md` | `0` | `0` | 1 | MATCH |
| `08-09` entries citing S052 | `grep -lE '^source: S052 ' corpus/knowledge/*.md \| wc -l` | `0` | `0` | 0 | MATCH |
| `10-11` harness | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=20 pass=20 exit=0` | `entries=20 pass=20 exit=0` as the 21st and last harness line (last enumerated row `PASS F17 … ids=S051`); the driver's appended `exit=0` marker follows it | 0 | MATCH |
| `12-14` source-recheck S052 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052` | `manifest UNAVAILABLE reason=missing` / `recheck_exit=2` | same two lines | 2 | MATCH |
| `15-16` knowledge entries | `ls corpus/knowledge/*.md \| wc -l` | `46` | `46` | 0 | MATCH |

Frontier ids actually present in `corpus/README.md` at freeze:
`F01 F02 F03 F04 F05 F06 F07 F08 F09 F10 F11 F12 F13 F14 F15 F16 F17` (17 — no `F18` row, matching the
before side of C2; `corpus/source-snapshots/` also has no `round-35/` directory, matching
`manifest UNAVAILABLE reason=missing`).

### 5. Census before-control (`census-before.txt`)

Stored value: two W04 rows (`S028`, `S029`) + `ok` line, `census_exit=0`. Replayed two ways —
the recorded invocation against the live fleet root, and the identical parser against the freeze
bytes via `--file` (needed because `--root` requires a `shokunin.conf` that a lane export does not
carry):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/freeze/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/fast/scratch/…/freeze/corpus/SOURCES.md
census_exit=0

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root $S/freeze
ERROR: config not found: …/freeze/shokunin.conf      # exit 2 — control invocation needs the lane's
ERROR: no lanes parsed …                              # conf, so --file is the faithful replay path
```

Same two W04 codes, same ids, same `ok` line, exit 0: MATCH.

### 6. Reproduction-quality checks

- **Implementation independence of the grep counts.** In this harness the shell's `grep` is a
  bash-builtin shim (`builtin grep --version` → `grep grep (pi-uu-grep) 0.2.0`); `/usr/bin/grep` is
  `GNU grep 3.12-modified`. Every grep-based control above was run under both: 12/12 AGREE
  (e.g. `D2 201.7` shim `2`/exit 0 vs gnu `2`/exit 0; `C2 rows` `51` vs `51`; `C2 citing S052`
  `-l` empty/exit 1 both). The counts are not an artefact of the shim.
- **Determinism.** The driver was run twice: stdout and JSON identical (`stdout_deterministic=yes`,
  `json_deterministic=yes`).
- **Read-only.** Whole-export digest before/after the replay is unchanged:
  `a81abe08801ddb8d20c1564fca6601a868bc72092f0eae756bfb29ebdb4a6fae` (6934 files,
  `export_tree_unmutated=yes`). No control command mutates the tree it measures.
- **No git dependency.** The export has no `.git` and the harness/recheck/census/grep controls all
  reproduce there, so the before-state is reproducible from committed bytes alone.

### 7. Findings for the L1 (advisory — I do not judge the round)

1. **All 18 stored C1/C2 values plus the census replay exactly.** No stored before-value is
   unreproducible, so the "before" halves of C1 and C2 are grounded at the freeze bytes.
   `claims.json` is also byte-identical at freeze, HEAD and in the worktree.
2. **D2 closure checks must be row-scoped, not globally counted.** `201.7` has two hits at freeze:
   `SCORECARD.md:1003` is the *round-33* depth:density row where `201.7` is that round's own after
   value (legitimately unchanged), and `SCORECARD.md:1145` is the round-34 row that is stale. A
   closure assertion of the form `grep -c '201\.7' SCORECARD.md == 0` is therefore unsatisfiable
   while `:1003` stands; the check must scope to the round-34 row (or to the round-34 section) and
   to the presence of the appended erratum naming `201.2`. (`corpus/instruments/r35-defect-closure.sh`
   did not exist in the worktree at my snapshot — `ls` → exit 2 — so I could not test the landed
   assertion; this is a pre-check, not a verdict on it.)
3. **D1 has two placeholder spellings, and the frozen count sees only one.** The freeze count
   `grep -c 'filled by the L1'` = 1 (`SCORECARD.md:1240`), but `SCORECARD.md:1129` also carries an
   unfilled placeholder spelled `**Final lane commit: the L1 fills this line in the\nclosing
   commit.**` (`grep -c 'the L1 fills this line'` → 1). That is exactly the brittleness D1 names
   ("the R1 marker check only matches the `<LANE_HASH>` spelling"). A closure check driven only by
   `filled by the L1` can go green with `:1129` still unfilled; check both locations.
4. **The before-controls are output-only; no committed runner replays them — fourth round running.**
   Both `before.txt` files record values and section labels but no command line, and no instrument
   or script in the lane consumes them (`grep -rln 'before.txt' corpus/instruments/` → only
   `corpus/instruments/README.md` prose; the only lane files that reference
   `c1-controls/before.txt` are lessons and wave receipts). The seat has therefore re-derived the
   commands by hand in round 30 (`.ufo/waves/round-30/wave1/ExecBeforeVerify.md`), round 33
   (`ExecBeforeReceipts.md:19`: "The frozen receipts are **output-only** … **reconstructs** the
   commands … not proof that the L1's original invocation was character-identical"), round 34
   (`ExecBeforeReceipts.md:22`: same caveat, "reconstructed") and now round 35. That is a
   reproducibility cost, not a wrong value: every value reproduces, but the *invocation* is never
   pinned, which is exactly the class R18 penalises on the after side ("binds three byte facts and
   has no count-zero escape"). If C1 is to be "runnable", the replay belongs in a committed
   instrument (e.g. `r35-defect-closure.sh --before <export>`, or a `*/before.txt` variant that
   stores the argv next to each value) so a non-author does not have to re-invent the greps.
5. Scratch-only, no lane artefact: this seat wrote exactly one file in the lane
   (`.ufo/waves/round-35/wave1/ExecBeforeReceipts.md`). No git/jj command other than read-only
   `rev-parse` / `cat-file` / `show` / `ls-tree` / `hash-object` / `archive` / `diff` was run.

### 8. Artifact digests (scratch, deleted after this receipt was written)

```
a008adf24ed9fa5c93e35b51c84b2dc2df0fe60722098a481f222ac71782467a  freeze.tar (115,701,760 B)
9bbe55d7b93f7a8ab1c2ab2edba4c230b46702727c40241792f30e0272ec5258  replay.json (per-case argv/stdout/exit)
efe9a3eff851421c728fff3255ba3932e6f5c85ac15bcbd035f725bb4a7bd9fb  replay.py (driver, reproduced in appendix)
49234ff9f6f881dab06642e04e7c7b0e68d1061e59e711e17752e000c874c4c6  byte-identity.tsv
01b40101aa22f942262fe6764a4ff3439d12a48eb050f8fa098e26b1101c90ba  harness.out
920e6fd4b2e82aee969bf489a9a2a4cd97188cf84ec001b4df1c944ea5901499  census-live.out
de4ffe2c522cfe2881cb75f3577b04b2735fe7b2b986f4145c61b7d765e49b3e  census-freeze.out
```

Toolchain used: `git 2.56.0`, `GNU bash 5.3.20(1)`, `GNU grep 3.12-modified` (+ builtin
`pi-uu-grep 0.2.0`), `Python 3.14.8`, `GNU tar 1.35`.

### Appendix — replay driver (parameterised; runs against any `git archive <freeze>` export)

```python
#!/usr/bin/env python3
"""Replay round-35 frozen before-controls against a git archive export of the freeze commit."""
import json, os, subprocess, sys

F = os.environ.get("FREEZE_EXPORT") or sys.argv[1]      # export root
LANE = os.environ.get("LANE_REPO", "/home/vgpnk/Projects/shokunin/kasegi-shokunin")
C = os.environ.get("FREEZE_COMMIT", "617496b9c6e92bc671e7e78b83df69a04470d0e9")

def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr

CASES = []
def case(idx, ctrl, label, cmd, cwd, expect):
    rc, out, err = run(cmd, cwd)
    CASES.append(dict(idx=idx, ctrl=ctrl, label=label, cmd=cmd, cwd=cwd, exit=rc,
                      stdout=out.rstrip("\n"), stderr=err.rstrip("\n"), expect=expect))

# C1 (depth:verifiability)
case(1,  "c1", "r35-defect-closure.sh presence",            "ls corpus/instruments/r35-defect-closure.sh", F, "ls_exit=2")
case(2,  "c1", "D1 'filled by the L1' lines",               "grep -c 'filled by the L1' SCORECARD.md", F, "1")
case(3,  "c1", "D1 c1c6a5f citations",                      "grep -c 'c1c6a5f' SCORECARD.md", F, "0")
case(4,  "c1", "D2 201.7 lines",                            "grep -c '201\\.7' SCORECARD.md", F, "2")
case(5,  "c1", "D2 201.2 lines",                            "grep -c '201\\.2' SCORECARD.md", F, "0")
case(6,  "c1", "D3 registry rows",                          "grep -cE 'r-defect-closure\\.sh|kill-rule-check\\.py' SKILL.md", F, "0")
case(7,  "c1", "D4 results present in export",              "ls .ufo/waves/round-34/wave1-results.json 2>/dev/null | wc -l", F, "0")
case(7.1,"c1", "D4 results tracked at freeze",              "git ls-tree -r --name-only %s -- .ufo/waves/round-34/wave1-results.json | wc -l" % C, LANE, "0")
case(8,  "c1", "D4 provenance note",                        "find .ufo/waves/round-34 -maxdepth 1 -name '*provenance*' -type f | wc -l", F, "0")
case(9,  "c1", "D5 claims-erratum-d5.md",                   "find . -name 'claims-erratum-d5.md' -type f | wc -l", F, "0")
case(10, "c1", "D6 dead-seat sentence",                     "grep -c 'did not file a receipt (dead seat' .ufo/waves/round-34/wave1/L1Integration.md", F, "1")
case(11, "c1", "D7 supersedes rows",                        "printf '%s %s\\n' \"$(grep -c 'supersedes-R22' corpus/QUALITY.md)\" \"$(grep -c 'supersedes-R23' corpus/QUALITY.md)\"", F, "0 0")
# C2 (coverage)
case(12, "c2", "frontier admitted",                         "grep -cE '^\\| F[0-9]+ \\|' corpus/README.md", F, "17")
case(13, "c2", "registry rows",                             "grep -cE '^\\|[[:space:]]*S[0-9]{3,}[[:space:]]*\\|' corpus/SOURCES.md", F, "51")
case(14, "c2", "S052 rows",                                 "grep -cE '^\\|[[:space:]]*S052[[:space:]]*\\|' corpus/SOURCES.md", F, "0")
case(15, "c2", "entries citing S052",                       "grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l", F, "0")
case(16, "c2", "harness",                                   "python3 corpus/instruments/frontier-recheck-count.py; echo \"exit=$?\"", F, "entries=20 pass=20 exit=0")
case(17, "c2", "source-recheck S052",                       "python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052; echo \"recheck_exit=$?\"", F, "recheck_exit=2")
case(18, "c2", "knowledge entries",                         "ls corpus/knowledge/*.md | wc -l", F, "46")

json.dump(CASES, sys.stdout, indent=1)
```

Expected on the freeze export: 18 stored values (+2 added discriminating variants `6.1`, `7.1`),
all matching; on a tree that has landed C1/C2 the same driver flips (e.g. `ls_exit=0`,
`entries=21 pass=21`, `recheck_exit=0`), so it doubles as a discriminating control for the after side.
