VERDICT: class confirmed and NOT closed by C1 — the live-counter derive count is 1/27 at base and 0/35 at tip (C1's own repair works), but the same class survives in two committed places this sweep measured: (a) the r54 red fixture `red-d53-ledger.json` still derives its figure by re-running `frontier-recheck-count.py`, and on this host that derive is `UNAVAILABLE reason=derive-exit-1` where the r54 receipt printed `derived=33`; (b) the census substrate is host-stamped — 1130 of 1130 INTERNAL rows in `corpus/instruments/citation-survival.tsv` carry a `C:\Users\jpvei\...` absolute path, so `census-freshness-check.py` reads `CENSUS-FRESH=stale` (exit 1) on a pure export of r56 tip 8a5d7538, the very rev whose committed receipt pinned `CENSUS-FRESH=ok`, and the C1 ledger pins that `ok` as a verified figure (`census-fresh-literal-r56`, ledger:257-262). Sizing: 16 host-bound live-counter lines in 13 of 66 committed r52-56 receipts, while only 3 of 66 receipts name a host at all.

Seat: ScoutHostBound (kasegi round 57, wave 1). Question: does the lane still carry the round-53 `fail-entry-records` mistake class — a committed figure, ledger derive or receipt that re-runs a LIVE counter whose result depends on the host. Read-only on the lane; no dispatch; no lane suite run.

# 1. Lane state at measurement

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git rev-parse HEAD && git status --porcelain
cd3029876eac7189aaff0d32b26031c0defa35aa
 M LOG.md
 M SCORECARD.md
?? .ufo/waves/round-57/w1.ready.dispatched
?? .ufo/waves/round-57/w1/
```
exit 0, run-utc 2026-11-03T18:36:51Z (state re-checked 18:48:33Z, unchanged). Base rev for the frozen claims is `eae1d614542e8d30d77e9f4e8b9dea6a11aad138`; the working tree already holds the in-flight C1/C2 implementation (ledger at 35 entries), which is what this sweep audits. Nothing under L was written except this file; all scratch work ran in `/fast/scratch/hyaku/kasegi-r57/ScoutHostBound`.

# 2. Step 1 — which ledger derives re-run a live counter

Command (the seat's own grep, then an exhaustive scan because the seat grep is a substring filter):

```
$ grep -n -E 'frontier-recheck-count|capture-binding-check|source-recheck|resolve\.py|anchorcheck|recheck-audit|figure-audit' corpus/instruments/figure-audit-ledger.json
111:   "id": "figure-audit-mentions-base-scorecard",
115:   "derive": "git show 32782bd6b564f80454af853b38868603a4140e79:SCORECARD.md | grep -c 'figure-audit'",
119:   "id": "figure-audit-mentions-base-log",
123:   "derive": "git show 32782bd6b564f80454af853b38868603a4140e79:LOG.md | awk '/figure-audit/{n++} END{print n+0}'",
127:   "id": "figure-audit-mentions-base-knowledge-expected",
131:   "derive": "git show 32782bd6b564f80454af853b38868603a4140e79:corpus/instruments/knowledge-expected.txt | awk '/figure-audit/{n++} END{print n+0}'",
```
exit 0. All three hits are literal `grep`/`awk` counts of the STRING `figure-audit` over a pinned rev — the word matches the filename, the command does not run the instrument.

Exhaustive scan (every one of the 35 `derive` strings, classified by whether the command head invokes an instrument):

```
$ grep -c '"id"' corpus/instruments/figure-audit-ledger.json
35
$ grep -c '"derive": "python' corpus/instruments/figure-audit-ledger.json
0
```

Same scan at the claims base, via `git show` (read-only):

```
$ git show eae1d614542e8d30d77e9f4e8b9dea6a11aad138:corpus/instruments/figure-audit-ledger.json | grep -c '"derive": "python'
1
```
exit 0. The single base live-counter derive is `fail-entry-records` (`corpus/instruments/figure-audit-ledger.json:213` at tip, verbatim):
`grep -oE 'FAIL_entry_records=[0-9]+' .ufo/waves/round-53/controls/c2-counter-final-r53.txt | head -1 | cut -d= -f2` — at base its derive was, verbatim:
`python corpus/instruments/frontier-recheck-count.py 2>/dev/null | grep -c '^FAIL'`
So: **live-counter derives = 1 of 27 at base, 0 of 35 at tip.** C1's repair is complete for the ledger itself.

Structural note on why the class is only *displaced*, not prevented: `figure-audit.py` deliberately admits a counter as a derive, so nothing rejects the pattern on the next edit —
```
$ sed -n '75,80p' corpus/instruments/figure-audit.py
def check_read_only(cmd):
    head = cmd.split("|")[0].split(">")[0].strip()
    if head.startswith(("python ", "python3 ")):
        # a counter run is admissible only against a committed instrument
        parts = head.split()
        return len(parts) >= 2 and parts[1].replace("\\", "/").startswith("corpus/instruments/")
```
(`corpus/instruments/figure-audit.py:75-80`, admission at `:103`).

# 3. The table (all 35 tip entries)

Host result column read from one run at cwd L, run-utc 2026-11-03T18:36:51Z (`FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`, exit 0). "live counter?" = does the derive itself re-execute a counter. Class "host-stamped provenance" = the derive is portable but the recorded value was produced by a host-dependent counter (see §6).

| # | entry id | derive | live counter? | host result vs want | class |
|---|---|---|---|---|---|
| 1 | frontier-rows | `git show 32782bd:corpus/README.md \| grep -cE '^\| F[0-9]+ \|'` | no | ok (34) | portable (rev-pinned) |
| 2 | registry-rows | `git show 32782bd:corpus/SOURCES.md \| grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | no | ok (85) | portable (rev-pinned) |
| 3 | knowledge-expected-entries | `git show 32782bd:corpus/instruments/knowledge-expected.txt \| grep -c '^corpus/knowledge/'` | no | ok (72) | portable (rev-pinned) |
| 4 | knowledge-files | `git ls-tree --name-only 32782bd -- corpus/knowledge/ \| grep -c '\.md$'` | no | ok (72) | portable (rev-pinned) |
| 5 | capture-lines-s085 | `git show 32782bd:corpus/source-snapshots/round-53/S085.txt \| wc -l` | no | ok (542) | portable (rev-pinned) |
| 6 | capture-bytes-s085 | `git show 32782bd:corpus/source-snapshots/round-53/S085.txt \| wc -c` | no | ok (7590) | portable (rev-pinned) |
| 7 | capture-lines-s086 | `wc -l < corpus/source-snapshots/round-54/S086.txt` | no | ok (731) | receipt-literal (WT), append-only |
| 8 | capture-sha256-s086 | `sha256sum corpus/source-snapshots/round-54/S086.txt \| cut -d' ' -f1` | no | ok (fa84a017…) | receipt-literal (WT), append-only |
| 9 | frontier-rows-r54 | `git show 5108584a…:corpus/README.md \| grep -cE '^\| F[0-9]+ \|'` | no | ok (35) | portable (rev-pinned) |
| 10 | registry-rows-r54 | `git show 5108584a…:corpus/SOURCES.md \| grep -cE '^…S[0-9]{3,}…\|'` | no | ok (86) | portable (rev-pinned) |
| 11 | entries-r54 | `git show 5108584a…:corpus/README.md \| grep -E '^\| F[0-9]+ \|' \| awk -F'\|' …` | no | ok (38) | portable (rev-pinned) |
| 12 | knowledge-expected-r54 | `git show 5108584a…:corpus/instruments/knowledge-expected.txt \| grep -c '^corpus/knowledge/'` | no | ok (73) | portable (rev-pinned) |
| 13 | knowledge-files-r54 | `git ls-tree --name-only 5108584a… -- corpus/knowledge/ \| grep -c '\.md$'` | no | ok (73) | portable (rev-pinned) |
| 14 | figure-audit-mentions-base-scorecard | `git show 32782bd6…:SCORECARD.md \| grep -c 'figure-audit'` | no | ok (2) | portable (rev-pinned) |
| 15 | figure-audit-mentions-base-log | `git show 32782bd6…:LOG.md \| awk '/figure-audit/{n++} END{print n+0}'` | no | ok (0) | portable (rev-pinned) |
| 16 | figure-audit-mentions-base-knowledge-expected | `git show 32782bd6…:corpus/instruments/knowledge-expected.txt \| awk '/figure-audit/…'` | no | ok (0) | portable (rev-pinned) |
| 17 | frontier-rows-r55 | `git show 133c5753…:corpus/README.md \| grep -cE '^\| F[0-9]+ \|'` | no | ok (36) | portable (rev-pinned) |
| 18 | registry-rows-r55 | `git show 133c5753…:corpus/SOURCES.md \| grep -cE '^…S[0-9]{3,}…\|'` | no | ok (87) | portable (rev-pinned) |
| 19 | entries-r55 | `git show 133c5753…:corpus/README.md \| grep -E '^\| F[0-9]+ \|' \| awk -F'\|' …` | no | ok (39) | portable (rev-pinned) |
| 20 | knowledge-expected-r55 | `git show 133c5753…:corpus/instruments/knowledge-expected.txt \| grep -c '^corpus/knowledge/'` | no | ok (74) | portable (rev-pinned) |
| 21 | knowledge-files-r55 | `git ls-tree --name-only 133c5753… -- corpus/knowledge/ \| grep -c '\.md$'` | no | ok (74) | portable (rev-pinned) |
| 22 | census-fresh-literal-r55 | `grep -oE 'CENSUS-FRESH=[a-z]+' .ufo/waves/round-55/controls/gate-final-r55.txt \| head -1 \| cut -d= -f2` | no | ok (stale) | receipt-literal (WT), host-stamped provenance |
| 23 | census-internal-r55-receipt | `grep -oE 'internal=[0-9]+' …/gate-final-r55.txt \| head -1 \| cut -d= -f2` | no | ok (1118) | receipt-literal (WT), host-stamped provenance |
| 24 | census-gone-r55-receipt | `grep -oE 'gone=[0-9]+' …/gate-final-r55.txt \| head -1 \| cut -d= -f2` | no | ok (3883) | receipt-literal (WT), host-stamped provenance |
| 25 | census-fixedpoint-internal-r55 | `grep -oE 'internal=[0-9]+' …/df3-fixedpoint-r55tip.txt \| tail -1 \| cut -d= -f2` | no | ok (1119) | receipt-literal (WT), host-stamped provenance |
| 26 | census-fixedpoint-gone-r55 | `grep -oE 'gone=[0-9]+' …/df3-fixedpoint-r55tip.txt \| tail -1 \| cut -d= -f2` | no | ok (3882) | receipt-literal (WT), host-stamped provenance |
| 27 | fail-entry-records | `grep -oE 'FAIL_entry_records=[0-9]+' …/round-53/controls/c2-counter-final-r53.txt \| head -1 \| cut -d= -f2` | no | ok (33) | receipt-literal (WT), append-only |
| 28 | frontier-rows-r56 | `git show 8a5d7538…:corpus/README.md \| grep -cE '^\| F[0-9]+ \|'` | no | ok (37) | portable (rev-pinned) |
| 29 | registry-rows-r56 | `git show 8a5d7538…:corpus/SOURCES.md \| grep -cE '^…S[0-9]{3,}…\|'` | no | ok (88) | portable (rev-pinned) |
| 30 | entries-r56 | `git show 8a5d7538…:corpus/README.md \| grep -E '^\| F[0-9]+ \|' \| awk -F'\|' …` | no | ok (40) | portable (rev-pinned) |
| 31 | knowledge-expected-r56 | `git show 8a5d7538…:corpus/instruments/knowledge-expected.txt \| grep -c '^corpus/knowledge/'` | no | ok (75) | portable (rev-pinned) |
| 32 | knowledge-files-r56 | `git ls-tree --name-only 8a5d7538… -- corpus/knowledge/ \| grep -c '\.md$'` | no | ok (75) | portable (rev-pinned) |
| 33 | census-fresh-literal-r56 | `grep -oE 'CENSUS-FRESH=[a-z]+' .ufo/waves/round-56/controls/gate-final-r56.txt \| head -1 \| cut -d= -f2` | no | ok (ok) | receipt-literal (WT), host-stamped provenance |
| 34 | census-internal-r56-receipt | `grep -oE 'internal=[0-9]+' …/gate-final-r56.txt \| head -1 \| cut -d= -f2` | no | ok (1130) | receipt-literal (WT), host-stamped provenance |
| 35 | census-gone-r56-receipt | `grep -oE 'gone=[0-9]+' …/gate-final-r56.txt \| head -1 \| cut -d= -f2` | no | ok (3915) | receipt-literal (WT), host-stamped provenance |

Rows 9-13, 17-21, 28-32 abbreviate the rev to its first 8 hex in this table only; the full 40-hex rev is in the ledger and in §2's verbatim list. Counts: 24 rev-pinned, 11 working-tree; of the 11, 8 are census receipt literals (host-stamped provenance), 2 are capture literals, 1 is the repaired fail-entry-records.

Revision-control check: at the claims base the same audit is red exactly on the repaired entry, reproduced read-only from the base ledger against the current repo:
```
$ git show eae1d61…:corpus/instruments/figure-audit-ledger.json > $S/base-ledger.json
$ python corpus/instruments/figure-audit.py --ledger $S/base-ledger.json
FIG fail-entry-records recorded=33 (the class-check line; the trailer's 34 superseded) derived=UNAVAILABLE reason=derive-exit-1 stale
FIGURE-AUDIT figures=27 ok=26 stale=1 exit=1
```
exit 1. Identical to the committed base control `.ufo/waves/round-57/controls/do-nothing-c1-r57.txt` (same 27/26/1 with the same `UNAVAILABLE reason=derive-exit-1`).

# 4. Step 2 — running the live-counter derives

Live derives in the tip ledger: none (§2). Two live-counter derives exist in committed fixtures/records and were run with cwd L, read-only, `TMPDIR=<S>`, `timeout 120`, run-utc 2026-11-03T18:36Z:

(a) the base form of the repaired entry, verbatim from the base ledger —
```
$ python corpus/instruments/frontier-recheck-count.py 2>/dev/null | grep -c '^FAIL'
0
exit=1      # wall 2.18s
```
The counter prints no `FAIL` line on this host, `grep -c` prints `0` and exits 1; the audit reports it as `UNAVAILABLE reason=derive-exit-1`, never as a number. Recorded want=33 (Windows host). **Host result differs from the record: class present.**

(b) the r54 red fixture `.ufo/waves/round-54/controls/red-d53-ledger.json` (tracked; `git ls-files` confirms), entry `d53-1-trailer`, derive verbatim `python corpus/instruments/frontier-recheck-count.py 2>/dev/null | grep -c '^FAIL'`, want `34`:
```
$ python corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json
FIG d53-1-trailer recorded=34 derived=UNAVAILABLE reason=derive-exit-1 stale
FIG d53-2-lines recorded=543 derived=542 want=543 stale
FIGURE-AUDIT figures=2 ok=0 stale=2 exit=1
exit 1
```
Compare the committed r54 receipt `.ufo/waves/round-54/controls/c1-red-d53literals-r54.txt:4`, which printed `FIG d53-1-trailer recorded=34 derived=33 want=34 stale`. The control is still red here, but for the wrong reason: it can no longer distinguish "the filed 34 is stale" from "the counter read nothing", so the red control is now degenerate on this host — it would also pass if `frontier-recheck-count.py` crashed. That is the class in committed form, and it is *not* repaired by C1.

For contrast, the two other committed mutant ledgers are portable and reproduce their receipts' verdicts on this host (all three rows stale for the filed-vs-want reason, no `UNAVAILABLE`):
```
$ python corpus/instruments/figure-audit.py --ledger .ufo/waves/round-55/controls/red-df1-ledger.json
FIG red-df1-scorecard-prose recorded=0 (the filed prose literal, superseded by the r55 DF-1 erratum) derived=2 want=0 stale
FIG red-entries-r54-wrong recorded=38 derived=38 want=39 stale
FIG red-frontier-rows-r54-wrong recorded=35 derived=35 want=36 stale
FIGURE-AUDIT figures=3 ok=0 stale=3 exit=1
```
Also run individually (step 2 asks for first line + exit code per live derive); the three `figure-audit-mentions-*` entries that the seat grep flags are literal counts and were run to prove it: `2`/exit 0, `0`/exit 0, `0`/exit 0, all equal to want.

# 5. Step 3 — derives that read working-tree files with no rev (drift-prone)

11 of 35. Listed verbatim, with the file each reads:

| entry id | derive | reads (working tree, no rev) |
|---|---|---|
| capture-lines-s086 | `wc -l < corpus/source-snapshots/round-54/S086.txt` | corpus/source-snapshots/round-54/S086.txt |
| capture-sha256-s086 | `sha256sum corpus/source-snapshots/round-54/S086.txt \| cut -d' ' -f1` | same |
| census-fresh-literal-r55 | `grep -oE 'CENSUS-FRESH=[a-z]+' .ufo/waves/round-55/controls/gate-final-r55.txt \| head -1 \| cut -d= -f2` | r55 receipt |
| census-internal-r55-receipt | `grep -oE 'internal=[0-9]+' .ufo/waves/round-55/controls/gate-final-r55.txt \| head -1 \| cut -d= -f2` | r55 receipt |
| census-gone-r55-receipt | `grep -oE 'gone=[0-9]+' .ufo/waves/round-55/controls/gate-final-r55.txt \| head -1 \| cut -d= -f2` | r55 receipt |
| census-fixedpoint-internal-r55 | `grep -oE 'internal=[0-9]+' .ufo/waves/round-56/controls/df3-fixedpoint-r55tip.txt \| tail -1 \| cut -d= -f2` | r56 fixed-point receipt |
| census-fixedpoint-gone-r55 | `grep -oE 'gone=[0-9]+' .ufo/waves/round-56/controls/df3-fixedpoint-r55tip.txt \| tail -1 \| cut -d= -f2` | same |
| fail-entry-records | `grep -oE 'FAIL_entry_records=[0-9]+' .ufo/waves/round-53/controls/c2-counter-final-r53.txt \| head -1 \| cut -d= -f2` | r53 receipt |
| census-fresh-literal-r56 | `grep -oE 'CENSUS-FRESH=[a-z]+' .ufo/waves/round-56/controls/gate-final-r56.txt \| head -1 \| cut -d= -f2` | r56 receipt |
| census-internal-r56-receipt | `grep -oE 'internal=[0-9]+' .ufo/waves/round-56/controls/gate-final-r56.txt \| head -1 \| cut -d= -f2` | r56 receipt |
| census-gone-r56-receipt | `grep -oE 'gone=[0-9]+' .ufo/waves/round-56/controls/gate-final-r56.txt \| head -1 \| cut -d= -f2` | r56 receipt |

Drift is real, not theoretical. One appended line in a scratch export of HEAD flips exactly these two unpinned capture entries while the rev-pinned `capture-lines-s085` stays fixed (its stale in this export is the missing `.git`, see below):
```
$ cd $S/probe && printf 'drift-line\n' >> corpus/source-snapshots/round-54/S086.txt
$ python corpus/instruments/figure-audit.py --root "$D"
FIG capture-lines-s086 recorded=731 derived=732 want=731 stale
FIG capture-sha256-s086 recorded=fa84a01… derived=0fcb739ca5c891bff958b660baeac6081bda480b71301f3138cc08b68409f701 want=fa84a01… stale
FIGURE-AUDIT figures=35 ok=11 stale=24 exit=1
```
Mitigations actually present: the 9 receipt greps use `head -1`/`tail -1` over append-only receipts, and the two capture literals point at a round-54 snapshot that has never been rewritten. Residual risk is an edit *above* the first matching display line in a receipt, or an in-place re-capture of S086 — both silently move the audit.

A second, unasked but decisive portability property fell out of the same probe: the 24 rev-pinned derives need git history. On a pure `git archive` export (no `.git`) 22 entries go red, and two of them do so *silently as values* rather than as errors:
```
$ cd $S/probe && python corpus/instruments/figure-audit.py --root "$D"
FIG frontier-rows recorded=34 derived=UNAVAILABLE reason=derive-exit-1 stale
…
FIG capture-lines-s085 recorded=543 (filed; superseded by the r54 D53-2 correction) derived=0 want=542 stale
FIG capture-bytes-s085 recorded=7590 derived=0 want=7590 stale
FIGURE-AUDIT figures=35 ok=13 stale=22 exit=1
```
`git show <rev>:<path> | wc -l` returns `0` with exit 0 when the object is absent, so a `wc`-suffixed derive reports a plausible number instead of an error. Any future derive that must not run outside a git working tree should use a bare `git show`/`grep -c` form (which exits 1) rather than pipe into `wc`.

# 6. Step 4 — receipts produced on the other host

Host-named lines (`Windows|C:\|win32|zcode|jpvei`), per round, over `L/.ufo/waves/round-5[2-6]/controls/`:
```
$ for r in 52 53 54 55 56; do n=$(grep -rhE 'Windows|C:\\|win32|zcode|jpvei' .ufo/waves/round-$r/controls/ | wc -l); f=$(grep -rlE 'Windows|C:\\|win32|zcode|jpvei' .ufo/waves/round-$r/controls/ | wc -l); echo "round-$r lines=$n files=$f"; done
round-52 lines=0 files=0
round-53 lines=1 files=1
round-54 lines=2 files=1
round-55 lines=0 files=0
round-56 lines=2 files=1
```
5 host-named lines in 3 receipts out of 66 committed receipts (`find .ufo/waves/round-5[2-6]/controls -type f | wc -l` → 66). The lines: `.ufo/waves/round-53/controls/c1-donothing-r53.txt:2` (prose, "on this Windows host os.path.relpath emits backslash separators"); `.ufo/waves/round-54/controls/c1-gate-final-r54.txt:6-7` and `.ufo/waves/round-56/controls/gate-final-r56.txt:5-6` (both `wrote C:\Users\jpvei\.zcode\workspace\…\citation-survival.tsv` / `.md`, the census writer). Receipts containing any absolute path at all: 0/0/1/0/1 per round, i.e. 2 of 66.

Host naming badly under-counts host provenance. The counter's own output does better: every committed r52-56 `FRONTIER-CENSUS` line carries the Windows-only class `problem-rows=30` (`closed = rows − 30`), while the same counter at the same base bytes on this host reads `closed=37 problem-rows=0` (`.ufo/waves/round-57/controls/do-nothing-c2-r57.txt:5-6`):
```
$ for r in 52 53 54 55 56; do l=$(grep -rh 'problem-rows=30' .ufo/waves/round-$r/controls/ | wc -l); f=$(grep -rl 'problem-rows=30' .ufo/waves/round-$r/controls/ | wc -l); echo "round-$r lines=$l files=$f"; done
round-52 lines=3 files=2
round-53 lines=2 files=2
round-54 lines=5 files=3
round-55 lines=3 files=3
round-56 lines=3 files=3
```
16 lines in 13 of 66 receipts (20%) carry a live-counter result that is false on this host; only 3 of those 13 declare a host. The distinct values seen (each a different round's tree) are all of the family `rows=32..37 admitted=rows closed=rows-30 problem-rows=30 registry=82..88`.

# 7. The unrepaired instance: the census substrate is host-stamped

This is the part of the class C1 does not touch, and the reason the ledger can be green while a pinned figure is false on this host.

Mechanism, from source: `resolve.py` classifies a relative citation that exists under the lane root as `INTERNAL` and returns the *absolute resolved path* — `return "INTERNAL", p, m, "rel"` (`corpus/instruments/resolve.py:281`, `p` from `exists_any(os.path.join(lane_root, base))`), and writes that path verbatim into column 3 (`corpus/instruments/resolve.py:374`). Proven on a 3-token scratch fixture (fast, no full-tree run):
```
$ cd $S/fx && python corpus/instruments/resolve.py .
distinct=3 resolves=0 mirror=0 internal=1 other=0 gone=2 skill=1/1 corpus=1/3 all=1/3
$ cut -f1,2,3 corpus/instruments/citation-survival.tsv
corpus/*.md                       GONE
corpus/knowledge/missing.md       GONE
corpus/knowledge/a.md             INTERNAL   /fast/scratch/hyaku/kasegi-r57/ScoutHostBound/fx/corpus/knowledge/a.md
```
exit 0 — the host root is in the artifact.

Consequence in the committed artifact (`corpus/instruments/citation-survival.tsv`, 5057 rows + header):
```
$ awk -F'\t' 'NR>1 && $3 ~ /^[A-Za-z]:\\/' …/citation-survival.tsv | wc -l      # 1136
$ awk -F'\t' 'NR>1{print $2}' …/citation-survival.tsv | sort | uniq -c
   3913 GONE     1130 INTERNAL     12 RESOLVES     1 ok     1 W04
```
1136 drive-letter paths: 1130 of 1130 `INTERNAL` rows plus 6 `RESOLVES` rows; `citation-survival.md` carries 471 such lines. Every `INTERNAL` row is host-stamped with `C:\Users\jpvei\.zcode\workspace\…\kasegi-shokunin\…`. (`internal=1130` in the r56 receipt is exactly this row count; the two `ok`/`W04` rows are citation tokens containing tabs that shift their class cell, unrelated to this class.)

Measurement. `census-freshness-check.py` compares the committed pair byte-for-byte against a fresh regeneration (`corpus/instruments/census-freshness-check.py:61-88`, stale at `:86`), restoring the pair afterwards. On a pure export of the r56 tip — the rev whose receipt pinned the figure — the gate is red on this host:
```
$ git archive 8a5d7538b0caa50300b1eee88442a230d9a433f2 | tar -x -C $S/r56
$ cd $S/r56 && grep -cE '[A-Za-z]:\\' corpus/instruments/citation-survival.tsv
1136
$ python corpus/instruments/census-freshness-check.py .
CENSUS-FRESH=stale files=citation-survival.md+citation-survival.tsv (committed bytes differ from what resolve.py generates over the current tree; regenerate the census or repair the tree)
exit 1      # wall 273.67 s, 10598 files
```
Same result on a pure export of the current HEAD (`CENSUS-FRESH=stale`, exit 1, wall 282.73 s), so this is not an r57-tree artifact: it is the r56 figure itself that does not survive the host change. Against it, `.ufo/waves/round-56/controls/gate-final-r56.txt:9-10` prints `CENSUS-FRESH=ok files=2`, and C1's ledger pins that literal as a figure:
```
$ grep -n '"id": "census-fresh-literal-r56"' -A4 corpus/instruments/figure-audit-ledger.json
257:   "id": "census-fresh-literal-r56",
258:   "record": ".ufo/waves/round-56/controls/gate-final-r56.txt - the true-tee receipt's printed freshness limb (CENSUS-FRESH=ok; pair and fixed point coincide by construction, the r56 DF-3 discipline); pinned machine-checkably by round-57 C1",
259:   "recorded": "ok",
260:   "derive": "grep -oE 'CENSUS-FRESH=[a-z]+' .ufo/waves/round-56/controls/gate-final-r56.txt | head -1 | cut -d= -f2",
```
The ledger entry is honest about being a receipt literal, and it is portable as a derive — but the figure it verifies is host-relative and no record cell names the host (`grep -i host` over the ledger hits only the fail-entry-records amendment, ledger:211). The twin entry `census-fresh-literal-r55` (want `stale`) is *accidentally* green here: the gate also reads stale on this host, for the host-stamp reason rather than the r55 self-reference reason its record describes.

Ruling for the round lesson: this is not a failure of C1's kill rule (the rule is satisfied as written), and I did not edit claims.json. It is evidence that the class's repair was applied to the derive and not to the substrate, and it is the exact hook a future C1-style figure would hang on.

# 8. Proposed QUALITY criterion (text only — not written to QUALITY.md)

**QHOST — a pinned figure is a function of committed bytes, never of the host.**
A figure, ledger derive, gate or receipt that records a number MUST obtain it by one of: (a) reading committed bytes at an explicit rev (`git show <rev>:<path>`, `git ls-tree <rev>`), or (b) reading a committed receipt file literally. A derive MUST NOT re-execute a lane instrument (`python|bash|sh corpus/instruments/...`); if a recorded value was produced by a live counter, the record cell MUST name the generating host, and the counter's substrate MUST be host-neutral — no committed generated artifact may embed a generating host's absolute path in a repo-relative column.

Runnable check (proposed exact command; passes only when the lane is host-neutral):
```
python3 - <<'PY'
import json,re,sys
led=json.load(open("corpus/instruments/figure-audit-ledger.json"))
live=[f["id"] for f in led["figures"] if re.search(r"(python3?|bash|sh)\s+(\./)?corpus/instruments", f["derive"])]
ABS=re.compile(r"^(/|[A-Za-z]:[\\/])"); absrows=drive=0
for line in open("corpus/instruments/citation-survival.tsv",encoding="utf-8"):
    c=line.rstrip("\n").split("\t")
    if len(c)>=3 and c[1]=="INTERNAL" and ABS.match(c[2]):
        absrows+=1; drive+=bool(re.match(r"^[A-Za-z]:[\\/]",c[2]))
print("QUALITY-QHOST live_counter_derives=%d ids=%s host_absolute_internal_rows=%d drive_letter=%d"
      % (len(live), ",".join(live) or "-", absrows, drive))
sys.exit(1 if (live or absrows) else 0)
PY
```
Measured on the tip working tree, run-utc 2026-11-03T18:48Z:
```
QUALITY-QHOST live_counter_derives=0 ids=- host_absolute_internal_rows=1130 drive_letter=1130
CHECK_EXIT=1
```
It is green on the repaired ledger clause and red on the substrate clause — which is precisely the distinction this round's lesson needs. (A first draft of this check tested only `startswith("/")` and reported 0; caught and fixed here, recorded because the false-negative is itself the classic host-blindness.)

# 9. Tooling, scratch, bounds

- Tools installed/updated: none. No pacman was run (paused host-wide); nothing was written to `~/.local/bin` or any PATH directory.
- Scratch: `/fast/scratch/hyaku/kasegi-r57/ScoutHostBound` (exports `probe/`=HEAD, `r56/`=8a5d7538, `fx/`=resolve fixture, `census/`=pristine tsv copy, `base-ledger.json`, `table.md`). Deleted before yield: `rm -rf -- /fast/scratch/hyaku/kasegi-r57/ScoutHostBound`. No leftover.
- Read-only on L throughout; no git/jj mutation in L. `git archive`/`git show`/`git ls-tree` only; both census gate runs executed in scratch exports and restored their own pairs.
- Bounds: (i) the census figure's host-dependence is measured (gate red at r56 tip) but the *diff cause* is shown by mechanism + the 1130 stamped rows, not by a full byte-diff of the regenerated pair — a full resolve over the lane exceeds the 120 s derive budget (measured 273-283 s), so the byte diff was not produced; (ii) `census-internal/gone` *counts* are apparently host-stable (the class of a glob token does not change with the root), marked [INFERENCE], not measured; (iii) no LSP server is mounted in this seat's toolset, so all symbol/path findings are text-grep + source reading, and the artifact facts above are direct command output; (iv) the lane working tree is live (peers landing C1/C2), so the 35-entry census is a point-in-time reading at 18:36-18:48Z; the base reading is rev-anchored and stable.
