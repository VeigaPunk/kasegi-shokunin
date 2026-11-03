IN-SCOPE — every changed path in the two audited commits (freeze 00b535758d2cfa4511cda7167b67cdc045b85fb4, implementation 472737847ff31d1255bf1a0745822a5e878e9622) falls inside the round-59 declared change set (claims.json, the declared carry-in, and the round's control receipts); no product path is outside the claims. Four freeze-commit evidence files and three implementation receipts are not named verbatim in claims.json (role-declared only; §7), and one instrument line widens the allow-list without a claims.json anchor (§9c) — none of these changes a lane product path or the claim's measured behaviour.

# ExecDiffScope — round-59 w1 scope audit

- audited commits: freeze `00b535758d2cfa4511cda7167b67cdc045b85fb4`, implementation `472737847ff31d1255bf1a0745822a5e878e9622`
- lane (read-only): `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; `git -C … rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, exit 0
- audit close timestamp: `date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-11-03T21:58:40Z`, exit 0
- tools installed: none. `git --version` → `git version 2.56.0`, exit 0. No pacman/uv/npx transaction was run.
- scratch: `/fast/scratch/hyaku/kasegi-r59/ExecDiffScope` was created for the clone cross-check and removed in the same command (`rm -rf -- "$S"`, exit 0; `ls -d "$S"` afterwards → exit 2, absent). Nothing left over.
- writes: this file only, under `W = .ufo/waves/round-59/w1/`.

## 1. Commit identity, parents, ancestry

```
$ git -C "$L" rev-parse 00b535758d2cfa4511cda7167b67cdc045b85fb4
00b535758d2cfa4511cda7167b67cdc045b85fb4                                  exit=0
$ git -C "$L" rev-parse 472737847ff31d1255bf1a0745822a5e878e9622
472737847ff31d1255bf1a0745822a5e878e9622                                  exit=0
$ git -C "$L" rev-parse 472737847ff31d1255bf1a0745822a5e878e9622^
00b535758d2cfa4511cda7167b67cdc045b85fb4                                  exit=0
$ git -C "$L" rev-parse 00b535758d2cfa4511cda7167b67cdc045b85fb4^
69de8d363b2193fdb37d03fd3e235bceeb1c2daa                                  exit=0
$ git -C "$L" merge-base --is-ancestor 00b535758d2cfa4511cda7167b67cdc045b85fb4 472737847ff31d1255bf1a0745822a5e878e9622
                                                                          exit=0
$ git -C "$L" merge-base --is-ancestor 69de8d363b2193fdb37d03fd3e235bceeb1c2daa 00b535758d2cfa4511cda7167b67cdc045b85fb4
                                                                          exit=0
$ git -C "$L" log --oneline --no-decorate 69de8d363b2193fdb37d03fd3e235bceeb1c2daa..472737847ff31d1255bf1a0745822a5e878e9622
4727378 round-59: C1 derive gate refuses shell-chaining … SKILL registry rows for figure-audit (round-58 defect 1)
00b5357 round-59: freeze C1 … claims, do-nothing and stand-in receipts, probe runner, S092 capture and manifest
                                                                          exit=0
```

The implementation commit is the freeze commit's single child; the freeze commit is the base commit's single child. Both audited commits are reachable and unchanged at audit close.

## 2. Freeze commit 00b5357 — 17 paths, 17 additions, 0 modifications, 0 deletions, +834/−0

```
$ git -C "$L" show --numstat --format= 00b535758d2cfa4511cda7167b67cdc045b85fb4
58	0	.ufo/waves/round-59/claims.json
38	0	.ufo/waves/round-59/controls/c1-probe-run.sh
13	0	.ufo/waves/round-59/controls/c1-probes-base-r59.txt
13	0	.ufo/waves/round-59/controls/c1-probes-standin-r59.txt
18	0	.ufo/waves/round-59/controls/c1-standin-after-r59.txt
37	0	.ufo/waves/round-59/controls/c2-standin-after-r59.txt
35	0	.ufo/waves/round-59/controls/do-nothing-c1-r59.txt
33	0	.ufo/waves/round-59/controls/do-nothing-c2-r59.txt
7	0	.ufo/waves/round-59/controls/freeze-digests-r59.txt
82	0	.ufo/waves/round-59/controls/neighbor-screen-r59.txt
3	0	.ufo/waves/round-59/controls/s092-curl-raw.txt
168	0	.ufo/waves/round-59/controls/s092-issue-shell.html
64	0	.ufo/waves/round-59/controls/s092-opens-r59.txt
168	0	.ufo/waves/round-59/controls/s092-savedsearch-shell.html
16	0	.ufo/waves/round-59/controls/s092-variance-check.txt
2	0	corpus/source-snapshots/round-59/S092.txt
79	0	corpus/source-snapshots/round-59/manifest.json
                                                                          exit=0
$ git -C "$L" show --name-status --format= 00b535758d2cfa4511cda7167b67cdc045b85fb4
A	<the same 17 paths, in the same order>                              exit=0
$ git -C "$L" show --numstat --format= 00b5357… | awk 'NF==3{a+=$1;d+=$2;n++} END{printf "files=%d added=%d deleted=%d\n",n,a,d}'
files=17 added=834 deleted=0                                              exit=0
$ git -C "$L" diff --shortstat 69de8d3… 00b5357…
 17 files changed, 834 insertions(+)                                      exit=0
$ git -C "$L" diff --summary 69de8d3… 00b5357…
 create mode 100644 .ufo/waves/round-59/claims.json
 create mode 100755 .ufo/waves/round-59/controls/c1-probe-run.sh
 create mode 100644 <the other 15 paths>                                 exit=0
$ git -C "$L" diff --diff-filter=DR --name-status 69de8d3… 00b5357…
                                                                          exit=0 (empty: no deletion, no rename)
$ git -C "$L" show --numstat --format= 00b5357… | awk 'NF==3 && $2!=0 {printf "%s del=%s\n",$3,$2}'
                                                                          exit=0 (empty: no file with deletions)
```

Kinds: 16 × `A` mode 100644, 1 × `A` mode 100755 (`c1-probe-run.sh`, the probe runner). Sum check: 58+38+13+13+18+37+35+33+7+82+3+168+64+168+16+2+79 = 834.

## 3. Implementation commit 4727378 — 10 paths, 4 additions + 6 modifications, +261/−4

```
$ git -C "$L" show --numstat --format= 472737847ff31d1255bf1a0745822a5e878e9622
19	0	.ufo/waves/round-59/controls/c1-lane-after-r59.txt
12	0	.ufo/waves/round-59/controls/c1-probes-lane-after-r59.txt
38	0	.ufo/waves/round-59/controls/c2-lane-after-r59.txt
2	0	PROVINCE.md
11	0	SKILL.md
20	0	corpus/README.md
1	0	corpus/SOURCES.md
76	4	corpus/instruments/figure-audit.py
1	0	corpus/instruments/knowledge-expected.txt
81	0	corpus/knowledge/google-big-sleep-findings-tracker.md
                                                                          exit=0
$ git -C "$L" show --name-status --format= 472737847ff31d1255bf1a0745822a5e878e9622
A	.ufo/waves/round-59/controls/c1-lane-after-r59.txt
A	.ufo/waves/round-59/controls/c1-probes-lane-after-r59.txt
A	.ufo/waves/round-59/controls/c2-lane-after-r59.txt
M	PROVINCE.md
M	SKILL.md
M	corpus/README.md
M	corpus/SOURCES.md
M	corpus/instruments/figure-audit.py
M	corpus/instruments/knowledge-expected.txt
A	corpus/knowledge/google-big-sleep-findings-tracker.md
                                                                          exit=0
$ git -C "$L" show --numstat --format= 4727378… | awk 'NF==3{a+=$1;d+=$2;n++} END{printf "files=%d added=%d deleted=%d\n",n,a,d}'
files=10 added=261 deleted=4                                              exit=0
$ git -C "$L" diff --shortstat 00b5357… 4727378…
 10 files changed, 261 insertions(+), 4 deletions(-)                      exit=0
$ git -C "$L" diff --summary 00b5357… 4727378…
 create mode 100644 .ufo/waves/round-59/controls/c1-lane-after-r59.txt
 create mode 100644 .ufo/waves/round-59/controls/c1-probes-lane-after-r59.txt
 create mode 100644 .ufo/waves/round-59/controls/c2-lane-after-r59.txt
 create mode 100644 corpus/knowledge/google-big-sleep-findings-tracker.md exit=0
$ git -C "$L" diff --diff-filter=DR --name-status 00b5357… 4727378…
                                                                          exit=0 (empty: no deletion, no rename)
$ git -C "$L" diff -U0 00b5357… 4727378… | awk '/^\+[^+]/||/^\+$/{n++} END{print n}'
261                                                                       exit=0
$ git -C "$L" diff -U0 00b5357… 4727378… | grep -c '^-[^-]'
4                                                                         exit=0
$ git -C "$L" diff -U0 00b5357… 4727378… | grep -c '^-$'
0                                                                         exit=1 (no match: no blank deleted line)
```

Body-line reconciliation: 222 non-empty added lines + 39 blank added lines = 261 added; 4 non-empty + 0 blank = 4 deleted. Kinds: 4 × `A` (three control receipts + the knowledge entry, all 100644), 6 × `M`.

## 4. Deletion accounting (target step 2)

Only `corpus/instruments/figure-audit.py` has deletions:

```
$ git -C "$L" show --numstat --format= 4727378… | awk 'NF==3 && $2!=0 {printf "%s del=%s\n",$3,$2}'
corpus/instruments/figure-audit.py del=4                                  exit=0
```

The four deleted lines, with their base-side line numbers (`git -C "$L" diff -U0 00b5357… 4727378… -- corpus/instruments/figure-audit.py`, hunk headers `@@ -49 +49 @@`, `@@ -53 +53 @@`, `@@ -78,2 +78,54 @@`):

| base line | deleted line | class |
|---|---|---|
| 49 | `    "sha256sum", "cat ", "cut ", "sort ", "awk ", "sed -n ", "python ", "python3 ",` | literal line (replaced: `head `, `tail ` inserted) |
| 53 | `EXPECTED_CASES = 6  # R17 pin: a dropped selftest case turns the selftest red` | literal line (replaced: `= 14`) |
| 78 | `def check_read_only(cmd):` | replaced function block |
| 79 | `    head = cmd.split("|")[0].split(">")[0].strip()` | replaced function block |

That is exactly the allowed class — the replaced function block (2 lines) and two literal lines — and nothing else.

Every other modified tracked file has 0 deletions:

```
$ for f in corpus/README.md PROVINCE.md SKILL.md corpus/instruments/knowledge-expected.txt; do printf "%-46s dels=%s\n" "$f" "$(git -C "$L" diff -U0 00b5357… 4727378… -- "$f" | grep -c '^-[^-]')"; done
corpus/README.md                               dels=0                     exit=0
PROVINCE.md                                    dels=0
SKILL.md                                       dels=0
corpus/instruments/knowledge-expected.txt      dels=0
$ git -C "$L" diff -U0 00b5357… 4727378… -- corpus/SOURCES.md | grep -c '^-[^-]'
0                                                                         exit=1 (no match: pure insertion)
```

`corpus/SOURCES.md` is +1/−0, so the S001–S091 rows are byte-identical (one inserted line at the `@@ -96,6 +96,7 @@` hunk, the S092 row). The other modified files' 0-deletion numstat lines are in §3.

## 5. Pinned digest (target step 3)

```
$ sha256sum "$L/corpus/instruments/figure-audit.py"
32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0  …/corpus/instruments/figure-audit.py   exit=0
$ git -C "$L" show 472737847ff31d1255bf1a0745822a5e878e9622:corpus/instruments/figure-audit.py | sha256sum
32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0  -                                    exit=0
$ git -C "$L" show 15cd5771f460ba5e999af416b45edeed4fd54236:corpus/instruments/figure-audit.py | sha256sum
32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0  -                                    exit=0
$ git -C "$L" show 00b535758d2cfa4511cda7167b67cdc045b85fb4:corpus/instruments/figure-audit.py | sha256sum
dc09049a64ea3ebc68f89a3b7cdfe160ad3709db3a93f3f05f757ebcbd378f8c  -                                    exit=0
$ git -C "$L" show 69de8d363b2193fdb37d03fd3e235bceeb1c2daa:corpus/instruments/figure-audit.py | sha256sum
dc09049a64ea3ebc68f89a3b7cdfe160ad3709db3a93f3f05f757ebcbd378f8c  -                                    exit=0
```

The worktree file, the committed blob at the implementation commit, the committed blob at the then-current HEAD, and the blob in a fresh clone (§5b) are the same bytes: `32e1cddb…e83ff0`, which equals the candidate line at `.ufo/waves/round-59/controls/freeze-digests-r59.txt:2` and the `sha256sum` want at `.ufo/waves/round-59/claims.json:25`. The base and freeze blobs are `dc09049a…b378f8c`, matching `freeze-digests-r59.txt:3` (`base`).

Blob size and line-count consistency:

```
$ git -C "$L" cat-file -s 69de8d3…:corpus/instruments/figure-audit.py   → 8683   exit=0
$ git -C "$L" cat-file -s 4727378…:corpus/instruments/figure-audit.py   → 11298  exit=0
$ git -C "$L" show 69de8d3…:corpus/instruments/figure-audit.py | wc -l  → 214    exit=0
$ git -C "$L" show 4727378…:corpus/instruments/figure-audit.py | wc -l  → 286    exit=0
$ wc -l "$L/corpus/instruments/figure-audit.py"                         → 286 …  exit=0
```

214 + 76 − 4 = 286, which matches the numstat pair (+76/−4) and the worktree line count.

### 5b. Fresh-clone cross-check (contract fixture clause; `git clone -q --shared L`)

```
$ S=/fast/scratch/hyaku/kasegi-r59/ExecDiffScope; mkdir -p "$S"; D=$(mktemp -d -p "$S")
$ git clone -q --shared "$L" "$D/clone"                                   exit=0
$ git -C "$D/clone" rev-parse --show-toplevel
/fast/scratch/hyaku/kasegi-r59/ExecDiffScope/tmp.QmQIRqJaFW/clone        exit=0
$ git -C "$D/clone" rev-parse 00b5357… 4727378…
00b535758d2cfa4511cda7167b67cdc045b85fb4
472737847ff31d1255bf1a0745822a5e878e9622                                  exit=0
$ git -C "$D/clone" show --numstat --format= 00b5357… | awk '…sum…'
files=17 added=834 deleted=0                                              exit=0
$ git -C "$D/clone" show --numstat --format= 4727378… | awk '…sum…'
files=10 added=261 deleted=4                                              exit=0
$ git -C "$D/clone" show 4727378…:corpus/instruments/figure-audit.py | sha256sum
32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0  -     exit=0
$ sha256sum "$D/clone/corpus/instruments/figure-audit.py"
32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0  …/clone/corpus/instruments/figure-audit.py  exit=0
$ rm -rf -- "$S"                                                          exit=0
$ ls -d "$S"                                                              exit=2 (absent)
```

The clone reproduces the lane's per-commit totals and the pinned digest, so the numbers in §2–§5 do not depend on the lane worktree or index.

## 6. Negative scope checks — declared artifacts were not rewritten

```
$ git -C "$L" diff --name-only 00b5357… 4727378… -- corpus/instruments/figure-audit-ledger.json
                                                                          exit=0 (empty)
$ git -C "$L" diff --name-only 00b5357… 4727378… -- corpus/source-snapshots/
                                                                          exit=0 (empty)
$ git -C "$L" diff --name-only 00b5357… 4727378… -- .ufo/waves/round-59/claims.json
                                                                          exit=0 (empty)
$ sha256sum "$L/corpus/instruments/figure-audit-ledger.json"
2a9f5f898c7f55acbc1f1e680709c6ddd3094add64e4176bc9cd6bdc532d0e5c  …        exit=0
$ git -C "$L" show 69de8d3…:corpus/instruments/figure-audit-ledger.json | sha256sum
2a9f5f898c7f55acbc1f1e680709c6ddd3094add64e4176bc9cd6bdc532d0e5c  -       exit=0
$ git -C "$L" show 4727378…:corpus/instruments/figure-audit-ledger.json | sha256sum
2a9f5f898c7f55acbc1f1e680709c6ddd3094add64e4176bc9cd6bdc532d0e5c  -       exit=0
$ sha256sum "$L/.ufo/waves/round-59/claims.json"
becf44d1a29bba94dc8374f63787c8a2a450209506f4282cd9ca0b65614aa0d6  …        exit=0
$ git -C "$L" show 4727378…:.ufo/waves/round-59/claims.json | sha256sum
becf44d1a29bba94dc8374f63787c8a2a450209506f4282cd9ca0b65614aa0d6  -       exit=0
```

The 35-figure ledger is byte-identical at base, at the implementation commit and in the worktree (`2a9f5f89…`), so C1's `figures=35 ok=35` was not obtained by editing the ledger. `claims.json` is byte-identical in the worktree and at the implementation commit (`becf44d1…`), so the frozen claims were not edited after the freeze. The capture and manifest were not touched by the implementation commit.

Freeze-record corroboration (not my assigned step, recorded because the same commit is in scope):

```
$ sha256sum "$L/corpus/source-snapshots/round-59/S092.txt"
048937306e211937ac857d982f43bfe0a1eb7da7bbd7cfa149126d4b5768da38  …        exit=0
$ sha256sum "$L/corpus/source-snapshots/round-59/manifest.json"
5b2f4dc7ce5aba3643afbdd06a77c853c13ed5323f48257f400bc46b79b040aa  …        exit=0
$ sha256sum "$L/corpus/instruments/figure-audit-mutbat.py"
d18935fd7b2bdf2a3e58035b76f7e28739f9fd60a520e7d40e03cfc9823a7741  …        exit=0
```

These match `freeze-digests-r59.txt:5` (S092), `:6` (manifest) and `:4` (mutbat). `figure-audit-mutbat.py` does not appear in the implementation commit's numstat (§3), so the mutant battery was not modified to pass.

## 7. Path-by-path scope classification

Anchor = the claims.json line that declares the path (line map: 7 host, 8 carry_in, 15 C1 frozen_sentence, 16 C1 before, 17 C1 after, 18 C1 kill_rule, 20–25 C1 counting commands, 34 C2 frozen_sentence, 35 C2 before, 36 C2 after, 37 C2 kill_rule, 39–47 C2 counting commands; `wc -l claims.json` → 58, exit 0).

Freeze commit — 17 × A:

| path | + | anchor |
|---|---|---|
| `.ufo/waves/round-59/claims.json` | 58 | the frozen claims artifact itself (named in the seat target; a file cannot cite itself) |
| `.ufo/waves/round-59/controls/c1-probe-run.sh` | 38 | claims.json:15,18,20 |
| `.ufo/waves/round-59/controls/c1-probes-base-r59.txt` | 13 | claims.json:16 |
| `.ufo/waves/round-59/controls/c1-probes-standin-r59.txt` | 13 | claims.json:17 |
| `.ufo/waves/round-59/controls/c1-standin-after-r59.txt` | 18 | claims.json:17 |
| `.ufo/waves/round-59/controls/c2-standin-after-r59.txt` | 37 | claims.json:36 |
| `.ufo/waves/round-59/controls/do-nothing-c1-r59.txt` | 35 | claims.json:7,16 |
| `.ufo/waves/round-59/controls/do-nothing-c2-r59.txt` | 33 | claims.json:7,35 |
| `.ufo/waves/round-59/controls/freeze-digests-r59.txt` | 7 | claims.json:17,18 |
| `.ufo/waves/round-59/controls/neighbor-screen-r59.txt` | 82 | no claims.json reference — role only (§9a) |
| `.ufo/waves/round-59/controls/s092-curl-raw.txt` | 3 | role only: "an independent curl open", claims.json:7 (§9a) |
| `.ufo/waves/round-59/controls/s092-issue-shell.html` | 168 | role only: "shell screens", claims.json:7 (§9a) |
| `.ufo/waves/round-59/controls/s092-opens-r59.txt` | 64 | claims.json:7 |
| `.ufo/waves/round-59/controls/s092-savedsearch-shell.html` | 168 | role only: "shell screens", claims.json:7 (§9a) |
| `.ufo/waves/round-59/controls/s092-variance-check.txt` | 16 | claims.json:7 |
| `corpus/source-snapshots/round-59/S092.txt` | 2 | claims.json:34,37 |
| `corpus/source-snapshots/round-59/manifest.json` | 79 | claims.json:34,40 |

Implementation commit — 4 × A, 6 × M:

| path | kind | +/− | anchor |
|---|---|---|---|
| `.ufo/waves/round-59/controls/c1-lane-after-r59.txt` | A | +19/−0 | role only: C1 after-state receipt for the commands at claims.json:17,18,20–25 (§9b) |
| `.ufo/waves/round-59/controls/c1-probes-lane-after-r59.txt` | A | +12/−0 | role only: C1 P1–P8 lane run, claims.json:18 (§9b) |
| `.ufo/waves/round-59/controls/c2-lane-after-r59.txt` | A | +38/−0 | role only: C2 after-state receipt for claims.json:36,39–47 (§9b) |
| `PROVINCE.md` | M | +2/−0 | claims.json:36 ("the PROVINCE amendment") |
| `SKILL.md` | M | +11/−0 | claims.json:8 (carry_in defect 1: "SKILL.md's Gates and probes registry" row, a non-claim) |
| `corpus/README.md` | M | +20/−0 | claims.json:36 ("the README block") |
| `corpus/SOURCES.md` | M | +1/−0 | claims.json:34 (registry row S092), 37 (existing rows unchanged) |
| `corpus/instruments/figure-audit.py` | M | +76/−4 | claims.json:15,17,18,25 |
| `corpus/instruments/knowledge-expected.txt` | M | +1/−0 | claims.json:36 ("the expected-list insert") |
| `corpus/knowledge/google-big-sleep-findings-tracker.md` | A | +81/−0 | claims.json:34,36 |

No path in either commit is outside the lane, and no path is a product file the claims do not name. The three implementation receipts and four freeze evidence files are control/evidence artifacts under the round's declared controls directory; they carry no lane product content.

## 8. Lane state at audit close (outside the two-commit verdict)

Lane HEAD moved during the audit: `git -C "$L" rev-parse HEAD` at 21:58:40Z → `15cd5771f460ba5e999af416b45edeed4fd54236`, exit 0; `git -C "$L" log --oneline -3` → `15cd577`, `4727378`, `00b5357`; `git -C "$L" reflog -5 --date=iso` → `15cd577 HEAD@{2026-11-03 18:58:19 -0300}: export from jj`, i.e. the commit landed at 21:58:19Z, 21 s before the audit's close-time check (21:58:40Z). `git -C "$L" rev-parse 15cd577^` → `472737847ff31d1255bf1a0745822a5e878e9622`, exit 0. So the seat target's "lane HEAD = 4727378" was true at dispatch; 4727378 is now HEAD's parent.

`15cd577` is outside this audit's two named commits. Its shape, recorded so the audited numbers are anchored to the right commits:

```
$ git -C "$L" diff --shortstat 4727378… 15cd577…
 12 files changed, 958 insertions(+)                                      exit=0
$ git -C "$L" show --numstat --format= 15cd577…   (all A except three M; 0 deletions on every line)
204	0	.ufo/waves/round-59/build-spec.py
11	0	.ufo/waves/round-59/controls/c1-residual-base-r59.txt
11	0	.ufo/waves/round-59/controls/c1-residual-lane-r59.txt
33	0	.ufo/waves/round-59/controls/c1-residual-run.sh
251	0	.ufo/waves/round-59/w1-dispatch.json
253	0	.ufo/waves/round-59/w1-plan.json
78	0	.ufo/waves/round-59/w1-spec.json
1	0	.ufo/waves/round-59/w1.ready
11	0	LOG.md
28	0	SCORECARD.md
10	0	corpus/QUALITY.md
67	0	corpus/lessons/round-59.md
                                                                          exit=0
$ git -C "$L" diff --name-only 4727378… 15cd577… -- corpus/instruments/figure-audit.py corpus/SOURCES.md .ufo/waves/round-59/claims.json corpus/source-snapshots/
                                                                          exit=0 (empty)
$ git -C "$L" diff --name-only 4727378… 15cd577… -- corpus/instruments/
                                                                          exit=0 (empty)
$ git -C "$L" status --porcelain --untracked-files=no
                                                                          exit=0 (clean worktree)
$ git -C "$L" status --porcelain
?? .ufo/waves/round-57/w1.ready.dispatched
?? .ufo/waves/round-58/w1.ready.dispatched
?? .ufo/waves/round-59/w1.ready.dispatched
?? .ufo/waves/round-59/w1/                                               exit=0
```

`15cd577` touches no audited file: the pinned `figure-audit.py` digest at HEAD is still `32e1cddb…e83ff0` (§5), `SOURCES.md`, `claims.json` and the round-59 snapshots are untouched, and `corpus/instruments/` has no delta. The three tracked files that were still modified at the audit's first status call (`LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`) are exactly the three `M` rows in `15cd577`'s name-status above, so that staging state is now committed and the worktree is clean.

## 9. Observations (non-verdict, recorded not judged)

**a. Four freeze-commit files are role-declared, not name-declared.** `neighbor-screen-r59.txt` (82 lines), `s092-curl-raw.txt` (3), `s092-issue-shell.html` (168) and `s092-savedsearch-shell.html` (168) have no verbatim reference in `claims.json` (`grep -o '.\{0,100\}neighbor.\{0,100\}' claims.json` → no output, exit 1; `grep -o '.\{0,100\}curl.\{0,100\}' claims.json` → the host field's "an independent curl open is parsed-structure-identical, controls/s092-variance-check.txt"; `grep -o '.\{0,100\}shell.\{0,100\}' claims.json` → the host field's "the HTML pages … serve an application shell … shell screens"). The two HTML files are the SPA shells the host field calls "shell screens" (first line `<!DOCTYPE html>…`, 88981 and 82629 bytes, `wc -c` exit 0); the raw curl body backs `s092-variance-check.txt`; `neighbor-screen-r59.txt` is the pre-freeze neighbor screen (`run-utc=2026-11-03T21:39:57Z base=69de8d3…`, grep limbs over the front-door files, `corpus/source-snapshots/` and the sibling `PROVINCE.md` files) and is the only path in either commit with no claims.json reference at all. The same control name appears in earlier rounds' wave dirs (`grep -rln "neighbor-screen" .ufo/waves/round-58 .ufo/waves/round-57` → `round-58/controls/builders/run-a.sh`, `round-58/w1/SentinelCred.md`, `round-58/w1/SiblingOverlap.md`, `round-57/w1/SentinelCred.md`, `round-57/w1/SiblingOverlap.md`, exit 0), so it is a standing round control, not a new invention. All four are measurement receipts; none carries lane product content.

**b. Three implementation receipts are role-declared.** `c1-lane-after-r59.txt`, `c1-probes-lane-after-r59.txt`, `c2-lane-after-r59.txt` have no verbatim reference in `claims.json` (`grep -o '.\{0,100\}lane-after.\{0,100\}' claims.json` → no output, exit 1). They are the after-state records of the claim's own counting commands (`claims.json:17–18` requires the lane to reproduce the stand-in values byte-for-byte; `:36` requires the C2 values) and live under the round's controls dir. Evidence by role, not by name.

**c. Allow-list widening inside the declared instrument.** `corpus/instruments/figure-audit.py:49` adds `"head "` and `"tail "` to `READ_ONLY_HEADS` (the deleted base line 49 becomes `… "awk ", "sed -n ", "head ", "tail ", "python ", "python3 ",`). `claims.json` names only "an allow-listed read-only head" (`:15`) and never names `head`/`tail` (`grep -c '"head "' claims.json` → 0; `grep -c '"tail "' claims.json` → 0). This is a widening of the admitted head set inside the file the claim declares, not a path-scope violation; it does not touch the P1–P8 refusal set or the CTRL admission, which C1's own receipts measure. Flagged because the frozen sentence does not enumerate it. The `EXPECTED_CASES 6 → 14` literal change (base line 53) is declared by the selftest pin at `claims.json:15`.

**d. README repetition is the standing convention.** The r59 appended block repeats the "0/18 sentence is untouched" paragraph (`corpus/README.md:987-988`) that the r58 block already ends with (`:966-967`); `grep -c "0/18 sentence is untouched" corpus/README.md` → 16, exit 0, spanning lines 289–987. Every prior amendment block restates it, so this is convention, not a duplication defect.

**e. C2's capture bytes are fixed at freeze, not at implementation.** The freeze commit lands `corpus/source-snapshots/round-59/S092.txt` and `manifest.json` (declared at `claims.json:34` and in the freeze commit message: "S092 capture and manifest"), and the implementation commit does not modify them (§6). This is consistent with the round contract's "frozen at the freeze commit" reading and with the implementation commit's role (product bytes only).

## 10. Bottom line

- Freeze commit: 17 paths, 17 additions, 0 modifications, 0 deletions, +834/−0; no mode change other than the probe runner's 100755.
- Implementation commit: 10 paths, 4 additions + 6 modifications, 0 deletions of tracked files, 0 renames, +261/−4; the only deletions are the 4 replaced lines in `corpus/instruments/figure-audit.py` (base lines 49, 53, 78, 79), exactly the allowed class; every other modified file is 0 deletions, and `corpus/SOURCES.md` is +1/−0 so S001–S091 are byte-identical.
- Pinned digest: worktree = implementation blob = then-HEAD blob = fresh-clone blob = `32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0`, matching `freeze-digests-r59.txt:2` and `claims.json:25`; base/freeze blob = `dc09049a…b378f8c`, matching `freeze-digests-r59.txt:3`.
- Verdict: IN-SCOPE for both commits, with the four role-declared evidence files, three role-declared receipts, and the undeclared `head`/`tail` allow-list widening recorded above as text corrections/observations only.
