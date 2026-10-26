# ExecExpectedList — round-33 wave 1

Seat: `ExecExpectedList` (executor). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Lane base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; claims-freeze `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`
(`git log --oneline -3` → `a6a5023` spec, `6e55c8d` freeze, `690b69d` base).
Axes: depth:verifiability, coverage. Milestone: round-33.

Scope: **one** owned path, `corpus/instruments/knowledge-expected.txt`; this receipt is the second write.
Answering model: `opencode-go/deepseek-v4.1-flash` — the session's workspace context line names it; no model
was passed by this seat (config route table decides), matching the peer receipts' form
(`.ufo/waves/round-33/wave1/ExecEntryF16.md:5`).
Tools installed/upgraded: **none** (python3 stdlib only; no pacman transaction run, per the paused-host rule).
No git/jj mutation in the lane (read-only `git log/show/diff/status` only).
No scratch tree: no clone, mirror, work tree or fixture was created this seat, so `$HYAKU_SCRATCH` was never
used and nothing is owed to the cleanup rule.
No write outside the lane; `/home/vgpnk/Projects/shokuknow` never touched; no credential material read or written.

## 0. Dependency: the F16 entry landed, then moved twice

Waited per bounds 9 (20 s poll):

```
$ for i in $(seq 1 14); do [ -s .ufo/waves/round-33/wave1/ExecEntryF16.md ] && break; sleep 20; done
$ ls -la .ufo/waves/round-33/wave1/ExecEntryF16.md
-rw-r--r-- 1 vgpnk vgpnk 16732 Oct 26 01:26 .ufo/waves/round-33/wave1/ExecEntryF16.md
```

The entry file arrived before its receipt and then changed twice while I held the list edit:

| observed at | entry sha256 | lines / bytes | note |
|---|---|---|---|
| 01:23 | `8d209995…d08c` | 278 / 22114 | read only; peer message said "final" — superseded |
| 01:25:32 | `eebd5ea5…910b` | 305 / 24318 | receipt #1 pinned this; superseded |
| 01:28:10 | `53c48b3b…a48` | 306 / 24492 | **final**: receipt rewritten at 01:28:48 to pin it |

`grep -n '53c48b3b\|eebd5ea5\|8d209995' .ufo/waves/round-33/wave1/ExecEntryF16.md`:

```
15:53c48b3b322aa4e5f90e1bae27ad0c1fb60c3452b2cff1e35a52e3276bb60a48  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
216:through `8d4b1489…` → `8d209995…` → `eebd5ea5…`).
```

Every "final" number in §3 is on the `53c48b3b…` bytes; the intermediate run (on `eebd5ea5…`) is kept in §4
as non-comparative (bounds 6 / M30-3). The entry's `recheck:` line is unchanged across those two revisions
(line 7: `cd <lane> && python3 corpus/instruments/source-recheck.py --manifest
corpus/source-snapshots/round-32/manifest.json --source S049 && … --source S050`).

## 1. PRE-STATE baseline (before my edit)

Labelled PRE-STATE: taken before the list was touched, with 44 tree files on disk.

```
$ sha256sum corpus/instruments/knowledge-expected.txt
d6f25227b6025bb070740cd38c03783092dbcb51340e5c99689c9c1737b8f156  corpus/instruments/knowledge-expected.txt
$ python3 corpus/instruments/recheck-audit.py --quiet
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
EXIT=0
$ ls corpus/knowledge/*.md | wc -l
44
```

With the entry already on disk and the list still at 44, the drift was exactly one line (this is what the list
edit removes):

```
$ diff <(grep -v '^#' corpus/instruments/knowledge-expected.txt | LC_ALL=C sort) <(ls corpus/knowledge/*.md | LC_ALL=C sort)
3a4
> corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
```

## 2. The edit

`chinese-crowdsourced-testing-scope-and-rewards.md` sorts after `authorization-safe-harbor-and-scope.md` and
before `citation-bases.md` (`c-h` < `c-i` at the second character), so the line is inserted there, not appended.
The two `#` comment lines are untouched (item: "`#` comments stay").

```
$ git diff -- corpus/instruments/knowledge-expected.txt
diff --git i/corpus/instruments/knowledge-expected.txt w/corpus/instruments/knowledge-expected.txt
index 9471c49..3de1652 100644
--- i/corpus/instruments/knowledge-expected.txt
+++ w/corpus/instruments/knowledge-expected.txt
@@ -3,6 +3,7 @@
 corpus/knowledge/ai-assisted-finding-validation.md
 corpus/knowledge/authorised-testing-rules-of-engagement.md
 corpus/knowledge/authorization-safe-harbor-and-scope.md
+corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
 corpus/knowledge/citation-bases.md
 corpus/knowledge/claim-anatomy-sample.md
 corpus/knowledge/claim-gates.md
```

Post-edit checks:

```
$ grep -v '^#' corpus/instruments/knowledge-expected.txt | wc -l
45
$ grep -c '^#' corpus/instruments/knowledge-expected.txt
2
$ grep -v '^#' corpus/instruments/knowledge-expected.txt | LC_ALL=C sort -c && echo SORTED-OK
SORTED-OK
$ ls corpus/knowledge/*.md | wc -l
45
$ diff <(grep -v '^#' corpus/instruments/knowledge-expected.txt | LC_ALL=C sort) <(ls corpus/knowledge/*.md | LC_ALL=C sort) && echo TREE-EQUAL
TREE-EQUAL
$ git show HEAD:corpus/instruments/knowledge-expected.txt | grep -vc '^#'
44
$ sha256sum corpus/instruments/knowledge-expected.txt
3f68b9a2ff7db654770bc11cb3b178b3d2920cc8e5ca0ba9761d85a65ab81ceb  corpus/instruments/knowledge-expected.txt
```

Entry lines `44 -> 45`, comments `2 -> 2`, tree files `44 -> 45`, list == tree, one line added and nothing else.

## 3. After — quiescent bytes (the numbers this seat stands on)

Bytes pinned before the runs and re-hashed after a 90 s window with no change (`STABLE over 90s`):

```
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py   (483 lines, mtime 2026-10-25 20:34:54)
53c48b3b322aa4e5f90e1bae27ad0c1fb60c3452b2cff1e35a52e3276bb60a48  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md   (306 lines, mtime 2026-10-26 01:28:10)
3f68b9a2ff7db654770bc11cb3b178b3d2920cc8e5ca0ba9761d85a65ab81ceb  corpus/instruments/knowledge-expected.txt   (mtime 2026-10-26 01:27:07)
```

`recheck-audit.py` carries the same sha as round-31's quiescent instrument (`5d4842da…`), and it is on this
round's read-only list, so the audited predicate is the one the claim froze. `git status --porcelain` on my paths:

```
 M corpus/instruments/knowledge-expected.txt
?? corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
```

(`??` is ExecEntryF16's new entry, not mine; the instrument is clean vs HEAD.)

Lane root, exactly the command my item names:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py --quiet
strict pass=45/45 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=21 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=45 total=45 pass=45 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=45 missing=0 unexpected=0 exit=0
LANE_EXIT=0
```

Foreign cwd, exactly the command my item names (session shell pins its own cwd, so it is issued under `bash -c`
and `/bin/pwd` proves the cwd is `/`):

```
$ bash -c 'cd / && /bin/pwd && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/recheck-audit.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet; echo FOREIGN_EXIT=$?'
/
strict pass=45/45 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=21 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=45 total=45 pass=45 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=45 missing=0 unexpected=0 exit=0
FOREIGN_EXIT=0
```

The new entry's own row (`frozen` = parse/cwd/paths, `strict` = parse/cwd/paths/cdroot/instrument/own):

```
$ python3 corpus/instruments/recheck-audit.py | grep -E 'chinese-crowdsourced|^strict pass=|^expect=|^lines='
chinese-crowdsourced-testing-scope-and-rewards.md          frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
strict pass=45/45 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=45 total=45 pass=45 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=45 missing=0 unexpected=0 exit=0
```

So the audit accepts the F16 entry's recheck form on every frozen and strict limb, it executes (`lane=0`), it is
cwd-independent (`foreign=0`), and set equality holds. **No limb had to be reported to ExecEntryF16 by id — the
item's failure branch did not fire.**

Transition (PRE-STATE `44/44` → after `45/45`, both exit 0):
`lines 44 -> 45`, `strict 44 -> 45`, `executes 20 -> 21`, `gated 24 -> 24`, `broken 0 -> 0`,
`expected 44 -> 45`, `missing 0 -> 0`, `unexpected 0 -> 0`, `exit 0 -> 0`.

## 4. Superseded / in-flight runs (not comparisons)

- Run on entry `eebd5ea5…` (305 lines, the receipt-#1 pin), same instrument `5d4842da…` and same list
  `3f68b9a2…`: `strict pass=45/45 … exit=0`, `expect=present expected=45 missing=0 unexpected=0 exit=0`.
  Label: **PRE-STATE/superseded**; re-run on the final `53c48b3b…` bytes is §3, and it agrees. Both revisions'
  `recheck:` lines (entry line 7) pass every limb and begin with the same byte prefix
  (`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest
  corpus/source-snapshots/round-32/manifest.json --source S049 && …`, 260 characters compared from the console
  captures); I did **not** retain the superseded bytes, so I make no byte-identity claim beyond that prefix — the
  instrument-side evidence for both is the same `5d4842da…` and both verdicts are `strict 45/45 exit 0`.
- The 44-entry baseline in §1 predates the list edit and is not an after-answer; the after-answer is §3.

## 5. Risks / notes (no blockers)

- `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` moved twice after its first landing
  (`8d209995…` → `eebd5ea5…` → `53c48b3b…`). My `45/45` is pinned to `53c48b3b…`; a further revision by
  ExecEntryF16 (its owner) would require a re-run of the §3 commands. It is stable as of the 90 s window above.
- `corpus/instruments/recheck-audit.py` is read-only this round; if a later seat edits it, the §3 numbers must be
  re-taken (they are pinned to `5d4842da…`).
- The `#` comment line still reads "round 30". My item says the comments stay, so it was left byte-identical;
  re-dating it is not in this seat's item.
- `ExecHarnessC2` consumes the post-seat state; at hand-off it is `45` expected entries matching `45` tree files,
  exit 0, from both cwds.
- `#` comments count 2 and were not touched; no other line of the file changed (single-hunk diff in §2).

BLOCKED: none.
