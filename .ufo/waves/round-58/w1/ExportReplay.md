VERDICT: PARTIAL — 14/14 counting commands in claims.json C1+C2 reproduce the receipt's values from a clean clone of 18ddb054 (14 matches, 0 value mismatches, expected exit codes), but the run set is not fully export-bound: C2.1 re-runs 35 of its 42 entry rechecks against the lane working tree through an absolute `cd` (including the F39/S091 entry) and still prints `FRONTIER-PASS F39 ids=S091` and `entries=42 pass=42 exit=0` with the export's S091 capture corrupted; C2.9 executes a fleet-root script that is absent from the lane commit; and the comparison receipt `.ufo/waves/round-58/controls/after-r58.txt` is untracked in the lane.

# ExportReplay — round-58 C1/C2 export replay

Seat: ExportReplay (r58 w1). Target: replay the round's after-state counting run set from committed bytes at `18ddb054a82a59e530ba86b2511bcfa5ecd49b6b` in a clean export, not from the working tree.

Scratch: `S=/fast/scratch/hyaku/kasegi-r58/ExportReplay` (created with `mkdir -p`, deleted at the end; see §9). Every command below ran with `TMPDIR=$S/tmp` exported and, unless stated, `cwd=$S/clone`.

## 1. Export construction and identity

```
$ S=/fast/scratch/hyaku/kasegi-r58/ExportReplay
$ mkdir -p "$S"
$ git clone --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin "$S/clone"
Cloning into '/fast/scratch/hyaku/kasegi-r58/ExportReplay/clone'...
done.
$ git -C "$S/clone" checkout -q 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b
$ git -C "$S/clone" rev-parse HEAD
18ddb054a82a59e530ba86b2511bcfa5ecd49b6b
$ git -C "$S/clone" rev-parse --show-toplevel
/fast/scratch/hyaku/kasegi-r58/ExportReplay/clone
$ git -C "$S/clone" status --porcelain=v1
(no output)                                            exit 0
$ git -C "$S/clone" ls-files | wc -l
10712
$ git -C "$S/clone" rev-parse HEAD^{tree}
91fa4cbb1071dbef73fcda8d518307b09650a5f0
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b^{tree}
91fa4cbb1071dbef73fcda8d518307b09650a5f0
```

The clone's tree is the commit's tree (same tree id) and its worktree is clean before the run.

Precondition (reported, not a defect): `git clone --shared` installs `.git/objects/info/alternates` pointing at `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.git/objects`, so history reads resolve from the lane's object database. The commit's historical blobs are committed bytes, not worktree bytes, but the export is not standalone: a history-less export (`git archive`) cannot run the 24 ledger derives that use `git show`/`git cat-file`/`git ls-tree` (§7). The seat spec prescribes this clone form.

## 2. Lane state (read-only)

Implementation paths checked: `corpus/instruments`, `corpus/knowledge`, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/source-snapshots/round-58`, `.ufo/waves/round-54/controls/red-d53-ledger.json`.

```
$ git -C L rev-parse HEAD
18ddb054a82a59e530ba86b2511bcfa5ecd49b6b
$ git -C L status --porcelain=v1 -- corpus/instruments corpus/knowledge corpus/SOURCES.md corpus/README.md corpus/source-snapshots/round-58 .ufo/waves/round-54/controls/red-d53-ledger.json
(no output)                                            exit 0
$ git -C L diff --stat 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b -- corpus/instruments corpus/knowledge corpus/SOURCES.md corpus/README.md corpus/source-snapshots/round-58 .ufo/waves/round-54/controls/red-d53-ledger.json
(no output)                                            exit 0
$ git -C L status --porcelain=v1 --untracked-files=all -- corpus/instruments corpus/knowledge corpus/SOURCES.md corpus/README.md corpus/source-snapshots/round-58 .ufo/waves/round-54/controls .ufo/waves/round-58/controls
?? .ufo/waves/round-58/controls/after-r58.txt          exit 0
```

So at replay time the tracked implementation bytes in L equalled the commit, and the only untracked file under the checked paths was the receipt itself.

Concurrent-seat drift observed after the replay (recorded for §7, not an input to any counting command):

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-03T20:57:27Z
$ git -C L status --porcelain=v1 -uno
 M LOG.md
 M SCORECARD.md
 M corpus/QUALITY.md
$ ls -l --time-style=full-iso LOG.md SCORECARD.md corpus/QUALITY.md
... LOG.md            2026-11-03 17:52:01.381821017 -0300
... SCORECARD.md      2026-11-03 17:52:23.312884622 -0300
... corpus/QUALITY.md 2026-11-03 17:51:50.880907660 -0300
$ git -C L status --porcelain=v1 -- corpus/instruments corpus/knowledge corpus/SOURCES.md corpus/README.md corpus/source-snapshots/round-58 corpus/source-snapshots/round-53 corpus/source-snapshots/round-54 .ufo/waves/round-53/controls .ufo/waves/round-54/controls .ufo/waves/round-55/controls .ufo/waves/round-56/controls
(no output)                                            exit 0
```

`corpus/QUALITY.md` is appended prose (12 added lines vs the commit) and is not read by any counting instrument; the two LOG/SCORECARD figures in the audit ledger derive through `git show 32782bd6…`, i.e. committed bytes. The drift does show that L is a live write target while the wave runs (§7, finding F1).

## 3. Receipt identity

```
$ sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-58/controls/after-r58.txt
7bec9b0fb8b8ab4c390f1ec238277479ed0243c02e6cbbea46993907e312e601  .../after-r58.txt
$ wc -l .../after-r58.txt
180
$ git -C L cat-file -e 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b:.ufo/waves/round-58/controls/after-r58.txt
fatal: path '.ufo/waves/round-58/controls/after-r58.txt' exists on disk, but not in '18ddb054a82a59e530ba86b2511bcfa5ecd49b6b'   exit 128
$ git -C L status --porcelain=v1 -- .ufo/waves/round-58/controls/after-r58.txt
?? .ufo/waves/round-58/controls/after-r58.txt          exit 0
```

The receipt is not a committed receipt: it is an untracked working-tree file with no commit anchor. Its own header says it was "measured on the lane tree" (`after-r58.txt:1`, `run-utc=2026-11-03T20:49:28Z host=plazir27`, `:2`). The values below are therefore compared against a file read from L, whose identity is the sha256 above; only this replay corroborates its content.

## 4. C1 replay (5 counting commands; claims.json:19-25)

| # | command (cwd = clone) | export output (decisive) | exit | receipt (after-r58.txt) | match | dependency |
|---|---|---|---|---|---|---|
| C1.1 | `python3 corpus/instruments/figure-audit.py --selftest` | 6 case lines, all `verdict=pass`; last `selftest cases=6 failures=0` | 0 | `:6-12`, last `selftest cases=6 failures=0` | MATCH | clone-bound |
| C1.2 | `python3 corpus/instruments/figure-audit-mutbat.py` | `CONTROL c-equivalent-trailing-space ... must_not_be_killed=held`; `MUT m4-drop-stale-literal-case ... killed=1`; `MUT m6-readonly-gate-off ... killed=1`; `mutbat killed=2/2 survivors=0 controls=pass` | 0 | `:17-21` identical | MATCH | clone-bound |
| C1.3 | `python3 corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json \| grep d53-1` | `FIG d53-1-trailer recorded=34 derived=33 want=34 stale` | pipeline 0 (grep hit); instrument 1 | `:26` identical | MATCH | clone-bound; derive reads tracked `.ufo/waves/round-53/controls/c2-counter-final-r53.txt` |
| C1.4 | `python3 corpus/instruments/figure-audit.py` | 35 `FIG … ok` lines + `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0` | 0 | `:32-68` identical (36 printed lines in both) | MATCH | clone-bound; 24/35 derives read git objects |
| C1.5 | `grep -c '"id"' corpus/instruments/figure-audit-ledger.json` | `35` | 0 | `:73` `35` | MATCH | clone-bound |

Verbatim export output, C1.1:

```
selftest case=ok-ledger exit=0 want=0 verdict=pass
selftest case=stale-literal exit=1 want=1 verdict=pass
selftest case=derive-fails-fail-closed exit=1 want=1 verdict=pass
selftest case=token-boundary-34-vs-340 exit=1 want=1 verdict=pass
selftest case=unreadable-ledger-exit-2 exit=2 want=2 verdict=pass
selftest case=derive-not-read-only-refused exit=2 want=2 verdict=pass
selftest cases=6 failures=0
exit=0
```

C1.2:

```
PRISTINE selftest_exit=0 last='selftest cases=6 failures=0'
CONTROL c-equivalent-trailing-space selftest_exit=0 must_not_be_killed=held last='selftest cases=6 failures=0'
MUT m4-drop-stale-literal-case sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=5 failures=1'
MUT m6-readonly-gate-off sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=6 failures=1'
mutbat killed=2/2 survivors=0 controls=pass
exit=0
```

C1.3 (pipeline; `grep-exit` and `instrument-exit` captured from `PIPESTATUS`):

```
$ python3 corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json | grep d53-1
FIG d53-1-trailer recorded=34 derived=33 want=34 stale
grep-exit=0 instrument-exit=1
```

C1.4 tail:

```
...
FIG census-internal-r56-receipt recorded=1130 derived=1130 ok
FIG census-gone-r56-receipt recorded=3915 derived=3915 ok
FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0
exit=0
```

C1.5: `35`, exit 0.

## 5. C2 replay (9 counting commands; claims.json:37-46)

| # | command (cwd = clone) | export output (decisive) | exit | receipt (after-r58.txt) | match | dependency |
|---|---|---|---|---|---|---|
| C2.1 | `python3 corpus/instruments/frontier-recheck-count.py` | `FRONTIER-CENSUS rows=39 admitted=39 closed=39 problem-rows=0 registry=91`; `FRONTIER-PASS F39 ids=S091`; `entries=42 pass=42 exit=0` | 0 | `:78-80` identical | MATCH by value | MIXED: census/registry clone-bound; 35/42 entry rechecks `cd` to L (incl. F39) |
| C2.2 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-58/manifest.json --source S091` | `S091:sha256 OK`; `S091:Q1..Q9 OK occurrences=1 anchor=…-ok` | 0 | `:86-95` identical (10 lines) | MATCH | clone-bound (negative control in §6) |
| C2.3 | `python3 corpus/instruments/capture-binding-check.py` | `AUDIT records=74 …`; `records=74 bound=74 unbound=0` | 0 | `:135` identical (36 printed lines in both) | MATCH | clone-bound |
| C2.4 | `ls corpus/knowledge/*.md \| wc -l` | `77` | 0 (both pipeline stages 0) | `:140` `77` | MATCH | clone-bound |
| C2.5 | `grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt` | `77` | 0 | `:145` `77` | MATCH | clone-bound |
| C2.6 | `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt` | (no stdout by design) | 0 | `:150` `sort-ok` (receipt's `&& echo sort-ok` wrapper) | MATCH on exit | clone-bound |
| C2.7 | `grep -cE '^\| F39 ' corpus/README.md` | `1` | 0 | `:155` `1` | MATCH | clone-bound |
| C2.8 | `grep 'rate of autonomous AI cyber-capability progress' corpus/SOURCES.md \| sha256sum` | `631364e0dd3447d6a9bc56830dfc2da26600c5e6cfca054b2b9c3f8cf3627547  -` | 0 | `:160` identical | MATCH | clone-bound |
| C2.9 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md` | 6 `W04` duplicate-url lines + `file ok /fast/scratch/hyaku/kasegi-r58/ExportReplay/clone/corpus/SOURCES.md` | 0 | `:171-177` same 6 `W04` lines + `validate-exit=0` (lane path in the `file ok` line) | MATCH on verdict/exit; path differs by construction | EXTERNAL: fleet-root script, not in the lane commit |

Verbatim export output, C2.1 (decisive lines; full run prints 39 `FRONTIER-PASS` rows and 42 `PASS` entries):

```
FRONTIER-CENSUS rows=39 admitted=39 closed=39 problem-rows=0 registry=91
FRONTIER-PASS F39 ids=S091
entries=42 pass=42 exit=0
exit=0
```

C2.2:

```
S091:sha256 OK
S091:Q1 OK occurrences=1 anchor=1-ok
S091:Q2 OK occurrences=1 anchor=14-ok
S091:Q3 OK occurrences=1 anchor=21-ok
S091:Q4 OK occurrences=1 anchor=23-ok
S091:Q5 OK occurrences=1 anchor=25-ok
S091:Q6 OK occurrences=1 anchor=30-ok
S091:Q7 OK occurrences=1 anchor=34-ok
S091:Q8 OK occurrences=1 anchor=45-ok
S091:Q9 OK occurrences=1 anchor=14-ok
exit=0
```

C2.3 tail:

```
AUDIT records=74 with_url=74 with_fetched_utc=36 with_archival=38 snapshot_dirs=34 manifest_dirs=34 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=74 bound=74 unbound=0
exit=0
```

C2.9:

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	W04	S076 duplicate url docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories across scopes
file	W04	S080 duplicate url ossf.github.io/osv-schema across scopes
file	W04	S085 duplicate url csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema across scopes
file	ok	/fast/scratch/hyaku/kasegi-r58/ExportReplay/clone/corpus/SOURCES.md
exit=0
```

C2.4-C2.8 exact command lines and outputs (inside the table above, a shell pipe is markdown-escaped as `\|`; the fenced lines below are unambiguous):

```
$ ls corpus/knowledge/*.md | wc -l
77
ls-exit=0 wc-exit=0
$ grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt
77
exit=0
$ LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt
(no output) exit 0
$ grep -cE '^\| F39 ' corpus/README.md
1
exit=0
$ grep 'rate of autonomous AI cyber-capability progress' corpus/SOURCES.md | sha256sum
631364e0dd3447d6a9bc56830dfc2da26600c5e6cfca054b2b9c3f8cf3627547  -
grep-exit=0
```

## 6. Supplementary runs (not claims commands)

### 6.1 Unfiltered red fixture (receipt section `:24-29`)

The claims command filters to `d53-1`; the receipt section ran the ledger unfiltered. Replayed in the export:

```
$ python3 corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json
FIG d53-1-trailer recorded=34 derived=33 want=34 stale
FIG d53-2-lines recorded=543 derived=542 want=543 stale
FIGURE-AUDIT figures=2 ok=0 stale=2 exit=1
exit=1
```

Matches `after-r58.txt:26-29` and the claim's exit-1 requirement.

### 6.2 Receipt-only registry-rows section (`after-r58.txt:163-166`)

No claims command covers this section; run for the receipt comparison:

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
91
exit=0
```

Matches `:165`.

### 6.3 Receipt command-line defect at `after-r58.txt:77`

The recorded census command is `bash -c python3 corpus/instruments/frontier-recheck-count.py | grep -E …`. As written, `bash -c` takes `python3` as the command string and the script path as `$0`, so the inner command is bare `python3` with empty stdin. Probe in the export:

```
$ bash -c "bash -c python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F39|FRONTIER-FAIL|entries='; echo counter-pipe-exit=${PIPESTATUS[0]}" </dev/null
counter-pipe-exit=0
probe-exit=0
```

It prints none of the three recorded lines. The claims command text reproduces them:

```
$ bash -c "python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|FRONTIER-PASS F39|FRONTIER-FAIL|entries='; echo counter-pipe-exit=${PIPESTATUS[0]}" </dev/null
FRONTIER-CENSUS rows=39 admitted=39 closed=39 problem-rows=0 registry=91
FRONTIER-PASS F39 ids=S091
entries=42 pass=42 exit=0
counter-pipe-exit=0
probe2-exit=0
```

So `after-r58.txt:77` does not reproduce its own recorded output; the claims command does. This is a receipt transcription defect, not a claims defect.

### 6.4 Negative control for C2.2 and export-dependence probe for C2.1

In the clone, the export capture was replaced with a marker and restored afterwards (clone-only mutation; L untouched):

```
$ cp -p corpus/source-snapshots/round-58/S091.txt "$S/S091.txt.orig"
$ printf 'PROBE-CORRUPTED-BYTES\n' > corpus/source-snapshots/round-58/S091.txt
$ sha256sum corpus/source-snapshots/round-58/S091.txt
d5383fce488e3262fb50f6fd01f0c6fd03786b851b8d05231c0ad0ee923004e1
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-58/manifest.json --source S091
S091:sha256 MISMATCH expected=d2ba7199faf44fb9f5fc5c48924f20d72ed08959c511af58cb9c1322f9820618 actual=d5383fce488e3262fb50f6fd01f0c6fd03786b851b8d05231c0ad0ee923004e1
source-recheck-exit=1
$ python3 corpus/instruments/frontier-recheck-count.py
counter-exit=0
FRONTIER-CENSUS rows=39 admitted=39 closed=39 problem-rows=0 registry=91
FRONTIER-PASS F39 ids=S091
entries=42 pass=42 exit=0
$ cp -p "$S/S091.txt.orig" corpus/source-snapshots/round-58/S091.txt
$ sha256sum corpus/source-snapshots/round-58/S091.txt
d2ba7199faf44fb9f5fc5c48924f20d72ed08959c511af58cb9c1322f9820618
$ git status --porcelain=v1
(no output)                                            exit 0
```

C2.2 is a true export check: the same bytes corrupted make it fail closed (exit 1, MISMATCH). C2.1 is not: with the export's S091 bytes corrupted it still prints `FRONTIER-PASS F39 ids=S091` and `entries=42 pass=42 exit=0`, because the entry recheck it executes resolves to L (§7.2).

## 7. Working-tree dependency check

### 7.1 Clone is not a source of untracked input

`git -C "$S/clone" status --porcelain=v1` printed nothing before the run (§1) and nothing after all commands, with `git ls-files -o --exclude-standard | wc -l` = 0. No command read or wrote an untracked file in the clone; the clone had no untracked files at any point.

### 7.2 C2.1 entry rechecks escape to the lane

`frontier-recheck-count.py:269-270` runs each entry's recorded `recheck` line as `bash -c <recheck>` with `cwd=root`, but the recheck string is used verbatim (`entry_contract`, `:171-188`), and the knowledge entries prefix it with an absolute `cd` into the lane:

```
corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:6
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-58/manifest.json --source S091 …
```

Measured over the 42 entries the counter executes:

```
pass_entries=42 lane_cd=35 relative=7
relative_entries=corpus/knowledge/osv-affected-range-events.md,corpus/knowledge/cisa-vulnrichment-adp-enrichment.md,knowledge/nvd-api-2.0-retrieval-interface.md,knowledge/nvd-api-2.0-response-schema.md,knowledge/openssf-scorecard-checks.md,knowledge/github-repository-security-advisories-rest-api.md,knowledge/cisa-vulnrichment-record-list.md
```

35 of 42 rechecks — including F39 — execute `source-recheck.py` against `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, not the clone. The counter carries no digest logic of its own (`grep -nE 'sha256|hashlib|digest' corpus/instruments/frontier-recheck-count.py` printed `no-digest-logic`), so it trusts that exit code. §6.4 demonstrates the consequence: the export's F39 PASS line is not a function of the export's S091 bytes. In this run the escape landed on a lane whose checked paths equalled the commit (§2), so the values are consistent; on a clean-room host without that absolute path, 35 entry rechecks would fail and the counter would not reproduce `entries=42 pass=42`.

### 7.3 C2.9 executes a file outside the lane export

```
$ sha256sum /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
$ git -C L ls-tree 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b -- scripts/sources-census.sh
(no output)                                            exit 0
$ ls -l /home/vgpnk/Projects/shokunin/kasegi-shokunin/scripts/sources-census.sh
ls: cannot access '/home/vgpnk/Projects/shokunin/kasegi-shokunin/scripts/sources-census.sh': No such file or directory   exit 2
```

The command validates the clone's `corpus/SOURCES.md` (its `file ok` line names the clone path, §5) but the program itself is fleet-root state outside the export; its own bytes are not pinned by the lane commit. The exit-0 verdict and the six `W04` findings reproduce, but the check is not replayable from lane bytes alone.

### 7.4 C1 inputs and the object database

All C1 derive inputs are tracked at the commit and were read relative to the clone:

```
TRACKED .ufo/waves/round-53/controls/c2-counter-final-r53.txt
TRACKED .ufo/waves/round-55/controls/gate-final-r55.txt
TRACKED .ufo/waves/round-56/controls/df3-fixedpoint-r55tip.txt
TRACKED .ufo/waves/round-56/controls/gate-final-r56.txt
TRACKED corpus/source-snapshots/round-53/S085.txt
TRACKED corpus/source-snapshots/round-54/S086.txt
TRACKED corpus/instruments/figure-audit-ledger.json
TRACKED .ufo/waves/round-54/controls/red-d53-ledger.json
```

Blob ids at 18ddb054 (chain of custody):

```
43d255cbb3557513f017483337731bcb508ca281 corpus/instruments/figure-audit.py
b9f8237200a2309fbd052e9cc0a8a548fe8d9281 corpus/instruments/figure-audit-mutbat.py
83347a08b8a121971318b07d1047b81261172fdf corpus/instruments/figure-audit-ledger.json
532ae49d1e577f2a3d746c99258acedc0d6e8fb3 .ufo/waves/round-54/controls/red-d53-ledger.json
9c78c475bd178a994a093ff680cf6ff440e745a0 corpus/source-snapshots/round-58/S091.txt
5c34ad56d0a4d9dde54fc88a35a227a68d44f722 corpus/source-snapshots/round-58/manifest.json
2c15c5640e807d6da08f6da3ce1754a1e675cdf1 corpus/instruments/knowledge-expected.txt
fbc866a7c5b46bde7228cb00c0b529b195755da6 .ufo/waves/round-53/controls/c2-counter-final-r53.txt
```

Derive dependency counts in the audit ledger: `entries 35`, `with_rev 24`, `git_reads 24` — 24 of 35 figures derive through `git show`/`git cat-file`/`git ls-tree` at pinned revisions, resolved from the shared object store (§1), not from the worktree.

The instruments themselves import only the standard library and make no network calls; `grep -nE 'urlopen|urlretrieve|requests\.|http\.client|socket\.|ftp://|https?://[a-z]'` matched only fixture URLs (`https://example.invalid/...`) inside `capture-binding-check.py` self-tests.

### 7.5 Receipt untracked

See §3: the comparison target is `??` in L and absent from the commit (`cat-file -e` exit 128). It is a working-tree artifact; its identity is the sha256 in §3.

### 7.6 Concurrent writes to L

Between the replay and the final state check, L gained tracked modifications from other seats: `M LOG.md`, `M SCORECARD.md`, `M corpus/QUALITY.md` at 2026-11-03T20:57:27Z (file mtimes `17:51:50`–`17:52:23 -0300`). None is an input to any of the 14 commands (`corpus/QUALITY.md` is read by no instrument; the ledger's LOG/SCORECARD figures use `git show 32782bd6…`), and the implementation-path status stayed clean (§2). It is recorded because C2.1's escape reads a tree other seats can write.

## 8. Findings (reported as text; no lane file was edited)

- F1 (material): C2.1's per-entry PASS/exit lines are lane-bound. 35 of the 42 executed rechecks, including F39, `cd` to the absolute lane path (`corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:6`); with the export's S091 capture corrupted the counter still prints `FRONTIER-PASS F39 ids=S091` / `entries=42 pass=42 exit=0` (§6.4). The census numbers themselves (`rows=39 admitted=39 closed=39 problem-rows=0 registry=91`) and the README/manifest id checks are clone-bound; the entry-pass evidence is not. The C2 claim's kill rule is value-based and is met; export-independence is not.
- F2 (material, smaller): C2.9's program lives only at `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (sha256 `3fb72615…`), outside the lane commit; the command is not replayable from lane bytes alone (§7.3).
- F3 (material): the receipt `.ufo/waves/round-58/controls/after-r58.txt` is untracked (sha256 `7bec9b0f…`). Calling it "the committed receipt" is inaccurate; it has no commit anchor and its header itself says "measured on the lane tree" (`:1`).
- F4 (minor): `after-r58.txt:77` records a malformed wrapper (`bash -c python3 <script> | grep …`) that, run as written, prints only `counter-pipe-exit=0` and none of the three recorded lines (§6.3). The claims command text reproduces them.
- F5 (precondition): 24 of 35 figure-audit derives read git objects at pinned revisions; the prescribed `git clone --shared` resolves them from the lane's object database (`.git/objects/info/alternates`). This is committed-byte reading, not worktree reading, but a history-less export (`git archive`) would fail those 24 derives outright.
- F6 (comparison notes, not defects): C1.3's pipeline exit is the grep's 0 while the instrument exits 1 (both checked, §4); C2.6 is silent success by design and the receipt's `sort-ok` comes from its own `&& echo` wrapper; C2.9's `file ok` line names the clone path where the receipt names the lane path, with the same six `W04` findings and exit 0.

## 9. Tooling and cleanup

No tool was installed or upgraded for this seat; no `pacman`, `uv`, `npx` or binary install ran.

Scratch routing: `HYAKU_SCRATCH=<unset>`, `TMPDIR=/fast/scratch/hyaku/kasegi-r58/ExportReplay/tmp`, so the instruments' `$HYAKU_SCRATCH → $TMPDIR` fallback used S.

```
$ ls -ld "$S" "$S/clone"
drwxr-xr-x 4 vgpnk vgpnk    74 Nov  3 17:56 /fast/scratch/hyaku/kasegi-r58/ExportReplay
drwxr-xr-x 8 vgpnk vgpnk  4096 Nov  3 17:51 /fast/scratch/hyaku/kasegi-r58/ExportReplay/clone
$ rm -rf -- "$S"
rm-exit=0
scratch-removed=yes
$ ls -1 /fast/scratch/hyaku/kasegi-r58/
EntryClaimTable
MutationC1
SentinelCred
SiblingOverlap
l1-recon
pre-frozen
standin
tmp
wc
$ ls -ld /fast/scratch/hyaku/kasegi-r58/ExportReplay
ls: cannot access '/fast/scratch/hyaku/kasegi-r58/ExportReplay': No such file or directory   exit 2
$ find /fast/scratch/hyaku/kasegi-r58 -maxdepth 1 -name 'ExportReplay*'
(no output)                                            exit 0
```

No leftover under `S`; the other entries in the parent directory belong to other seats and were not touched. The only lane file this seat wrote is `W/ExportReplay.md`; the other files in `w1/` and the tracked modifications listed in §2/§7.6 belong to concurrent seats.
