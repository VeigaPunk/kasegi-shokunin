# ExecExpectedList — round-31 wave 1

Seat: `ExecExpectedList` (executor). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`; claims-freeze `738a77999a00efbca129cfccb28a481037f6241f`.
Axes: depth:verifiability, coverage. Model actually run on: `devin/deepseek-v4-1-flash` (route table, not passed by me).

Scope: **one** owned path, `corpus/instruments/knowledge-expected.txt`. This receipt is the second write.
No tool installed or upgraded this seat (nothing needed; `python3` stdlib only). No git/jj mutation run.
No write outside the lane; `/home/vgpnk/Projects/shokuknow` never touched.

## 0. Dependency and state

Waited for the F15 entry and its receipt (bounds 9, 20 s poll, cap 30 min):

```
$ until [ -s corpus/knowledge/vendor-third-party-finding-coordination.md ] && [ -s .ufo/waves/round-31/wave1/ExecEntryF15.md ]; do sleep 20; done
-rw-r--r-- 1 vgpnk vgpnk 12956 Oct 25 20:39 .ufo/waves/round-31/wave1/ExecEntryF15.md
-rw-r--r-- 1 vgpnk vgpnk 10359 Oct 25 20:38 corpus/knowledge/vendor-third-party-finding-coordination.md
```

That first landing was **not** the final entry: ExecEntryF15 rewrote it after a critic pass. The receipt names
the deliverable sha itself (`.ufo/waves/round-31/wave1/ExecEntryF15.md:6`):

```
- Deliverable: `corpus/knowledge/vendor-third-party-finding-coordination.md` — 160 lines, 11501 B, sha256 `1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb`.
```

Final bytes on disk match that (`1f16e371…`, 160 lines, mtime 20:41:30). Every "final" number below is on those
bytes; the one earlier run is labelled PRE-STATE.

`corpus/instruments/recheck-audit.py` is owned by ExecRALimbs and was dirty during my first run. Its receipt
(`.ufo/waves/round-31/wave1/ExecRALimbs.md:11-19`) fixes the quiescent bytes at
`5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09` (483 lines), and records that
"Only `selftest()` changed; `main()`, `audit_entry()`, `collect()`, `expected_mismatch()`, the" rest are untouched
(line 43), so the audited predicate is the same one the claim froze. I confirmed quiescence by hash over a 60 s
window (`h1 == h2 == 5d4842…`, `STABLE`) before the final runs.

## 1. PRE-STATE baseline (before my edit, instrument at HEAD `3fc0d75…`)

Labelled PRE-STATE: taken before the entry landed and before ExecRALimbs' selftest work. Not comparable to the
after column except as a count transition; the after column is §3.

```
$ git status --porcelain corpus/instruments/recheck-audit.py corpus/instruments/knowledge-expected.txt
(empty — both at HEAD)
$ python3 corpus/instruments/recheck-audit.py --quiet
strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=19 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=43 total=43 pass=43 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=43 missing=0 unexpected=0 exit=0
EXIT=0
```

Baseline entry counts: `grep -vc '^#' knowledge-expected.txt` = `43`; `ls corpus/knowledge/*.md | wc -l` = `43`.

## 2. The edit

`corpus/knowledge/vendor-third-party-finding-coordination.md` sorts after `…vendor-disclosure-policy-commitments-crosswalk.md`
(`t` > `d` at the first differing character after `vendor-`) and nothing in the list sorts after it, so it is appended
as the last entry line. The two `#` comment lines are untouched (item: "`#` comments stay").

```
$ git diff -- corpus/instruments/knowledge-expected.txt
@@ -43,3 +43,4 @@ corpus/knowledge/ufo-workspaces.md
 corpus/knowledge/vdp-disclosure-packages.md
 corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
 corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
+corpus/knowledge/vendor-third-party-finding-coordination.md
```

Checks on the edited file:

```
$ grep -v '^#' corpus/instruments/knowledge-expected.txt | wc -l
44
$ grep -v '^#' corpus/instruments/knowledge-expected.txt | LC_ALL=C sort -c && echo SORTED-OK
SORTED-OK
$ grep -c '^#' corpus/instruments/knowledge-expected.txt
2
$ ls corpus/knowledge/*.md | wc -l
44
$ git show HEAD:corpus/instruments/knowledge-expected.txt | grep -vc '^#'
43
```

Entry lines `43 -> 44`, comments `2 -> 2`, tree files `43 -> 44`: one line added, nothing else.

## 3. After — quiescent bytes (the numbers this seat stands on)

Instrument `5d4842da…`, expected list `d6f25227b6025bb070740cd38c03783092dbcb51340e5c99689c9c1737b8f156`,
entry `1f16e371…`; re-hashed after the runs and identical (the counter wrote nothing into the lane tree).

Lane root, exactly the command my item names:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py --quiet
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
EXIT=0
```

Foreign cwd, exactly the command my item names:

```
$ cd / && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/recheck-audit.py \
    --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
EXIT=0
```

(The session shell pins its own cwd to the workspace, so the foreign run was issued as
`bash -c 'cd / && /bin/pwd && python3 …'`; `/bin/pwd` printed `/`. The audit's own cwd does not affect the
`cwd` limb in any case — that limb re-runs each line under `--foreign`, default `/`.)

The new entry's own row, non-quiet run (`frozen` = parse/cwd/paths, `strict` = parse/cwd/paths/cdroot/instrument/own):

```
$ python3 corpus/instruments/recheck-audit.py | grep -E 'vendor-third-party|strict pass=|expect='
vendor-third-party-finding-coordination.md                 frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
expect=present expected=44 missing=0 unexpected=0 exit=0
```

So the F15 entry's recheck line (`cd <lane> && python3 corpus/instruments/source-recheck.py --manifest
corpus/source-snapshots/round-31/manifest.json --source S048`, entry L4) is accepted by every limb, executes
(`lane=0`), and behaves identically from a foreign cwd (`foreign=0`). No limb had to be reported to ExecEntryF15;
the audit did not reject the new entry's recheck form.

Transition: `43/43 -> 44/44`, `executes 19 -> 20`, `gated 24 -> 24`, `broken 0 -> 0`,
`expected 43 -> 44`, `missing 0`, `unexpected 0`, exit `0 -> 0`.

## 4. PRE-STATE / in-flight run kept for the record (not a comparison)

The first 44-entry run was taken while `recheck-audit.py` was dirty (ExecRALimbs mid-seat) and on the entry's
pre-critic-fix bytes `bf40fd9e…`. It printed `strict pass=44/44 … exit=0`, `expect=present expected=44 missing=0
unexpected=0 exit=0`. Its instrument hash turned out to equal the final quiescent hash `5d4842…`, so the instrument
side is the same bytes as §3; the entry side is superseded by §3's `1f16e371…` run. Label: PRE-STATE, re-run named
in §3 — and that re-run is done.

## 5. Risks / notes (no blockers)

- `corpus/instruments/recheck-audit.py` is modified in the working tree by ExecRALimbs (HEAD `3fc0d75…` -> `5d4842…`,
  selftest-only). If any later seat edits it again, the `44/44` above must be re-run; my number is pinned to
  `5d4842…`, not to a future revision.
- `corpus/knowledge/vendor-third-party-finding-coordination.md` moved from `bf40fd9e…` to `1f16e37…` between its first
  landing and its receipt. Only §3's numbers are offered as after-state.
- The `#` comment in `knowledge-expected.txt` still says "round 30". My item says the comments stay, so it was left
  byte-identical; changing it is not in this seat's item.
- `ExecHarnessC2` consumes this file's state; at hand-off it is `44` entries matching `44` tree files, exit 0.

BLOCKED: none.
