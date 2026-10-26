# ExecCensusAfter — round-33 final census after-state

Seat: `ExecCensusAfter` (leaf; no delegation). Round: kasegi-shokunin 33.
Run date: 2026-10-26T04:34:38Z. Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Lane HEAD at run: `53bfa59ff3fa578818e7e5db04fe60e80ed1eb6f` (`round-33: dispatcher ready marker, C1 erratum 1 …`);
base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4` is an ancestor. The wave's seat edits are uncommitted
working-tree bytes at this point; the L1 commits them. Answering model:
`opencode-go/deepseek-v4.1-flash` (host project-context; no model passed).

## 0. Dependency gate — both upstream receipts present

```
$ ls -l .ufo/waves/round-33/wave1/ExecRegistryAppend.md .ufo/waves/round-33/wave1/ExecHarnessC2.md
-rw-r--r-- 1 vgpnk vgpnk 15526 Oct 26 01:33 ExecHarnessC2.md
-rw-r--r-- 1 vgpnk vgpnk 22560 Oct 26 01:29 ExecRegistryAppend.md
```

Waited (cap 30 min) until both were non-empty; run started after. `ExecHarnessC2.md` §4 records
`b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b  corpus/SOURCES.md`, and my
before/after bookend over the same run measured the same digest — the census input is the quiescent
byte set the C2 harness measured, not an in-flight intermediate.

```
$ sha256sum corpus/SOURCES.md corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md   # t1 == t2
b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b  corpus/SOURCES.md
1f7ac0a2c39a0fbfdbee2ecbe112316dfc1bf7095b18cb8fb4eb9d6dfce171d1  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
BOOKEND-IDENTICAL (measured bytes unchanged across the run)
```

Observation (not a census input): the entry digest differs from `ExecHarnessC2.md` §4
(`53c48b3b…`), so the entry changed after that seat's bookend. The census reads the entry only as a
`used-by` path-existence check (`[ -e ]`); the file exists and SOURCES.md did not move. No content
claim is made here about the entry.

## 1. Frozen contract validate command (C2 counter #6, exact text)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "census_exit=$?"
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

Exactly `W04 S028` + `W04 S029` + `ok`; no `E` finding, no new `W` finding:

```
$ … validate … | grep -cE '	E[0-9]+	'      → 0
$ … validate … | grep -E '	W[0-9]+	'       → the two W04 lines above only
```

## 2. Six contract census commands (CORPUS.md §Census, run from the lane root)

Command text transcribed from `/home/vgpnk/Projects/shokunin/CORPUS.md:133-149` (rows, malformed,
tier histogram, status histogram, duplicate ids, enum+tier-inflation, mined used-by existence),
with the `census-before.txt` labels. Before trusting it, I replayed it on the frozen base bytes and
it reproduced the stored block byte-for-byte:

```
$ git show 690b69da:corpus/SOURCES.md > "$S/base-SOURCES.md"
$ <six commands on base-SOURCES.md> vs <sed -n '/## six contract census commands/,$p' .ufo/waves/round-33/census-before.txt>
REPRO-IDENTICAL
```

After-state on the landed bytes:

```
rows=50
malformed=0
tier=A=47 B=1 C=2 
status=mined=38 queued=9 rejected=3 
dups=
enum_violations=0
missing_usedby=0
```

All seven targets hold: rows 50, malformed 0, tier A=47 B=1 C=2, status mined=38 queued=9
rejected=3, dups empty, enum 0, missing used-by 0. (Tier sums 47+1+2=50; status sums
38+9+3=50.)

## 3. `diff -u` against the frozen before capture — exactly the expected deltas

Validate block (before lines 2-5 vs now):

```
$ diff -u <(sed -n '2,5p' .ufo/waves/round-33/census-before.txt) <(… validate …; echo census_exit=$?)
VALIDATE-BLOCK-UNCHANGED (no delta)
```

Six-command block (before lines 6-13 vs now):

```
$ diff -u <(sed -n '/## six contract census commands/,$p' .ufo/waves/round-33/census-before.txt) \
           <( { echo '## six contract census commands'; <six commands>; } )
--- /dev/fd/63
+++ /dev/fd/62
@@ -1,8 +1,8 @@
 ## six contract census commands
-rows=48
+rows=50
 malformed=0
-tier=A=45 B=1 C=2 
-status=mined=36 queued=9 rejected=3 
+tier=A=47 B=1 C=2 
+status=mined=38 queued=9 rejected=3 
 dups=
 enum_violations=0
 missing_usedby=0
```

The only deltas are the expected `+2` registry rows (`S049`, `S050`), `+2` tier-A rows and `+2`
mined rows. Nothing else moved: malformed, dups, enum violations, missing used-by and the validate
block are identical.

Row-level corroboration (each new id appears exactly once):

```
$ grep -cE '^\|[[:space:]]*S049[[:space:]]*\|' corpus/SOURCES.md   → 1
$ grep -cE '^\|[[:space:]]*S050[[:space:]]*\|' corpus/SOURCES.md   → 1
```

## 4. Scope, hygiene, risks

- Wrote one path: this receipt. No other lane file, no fleet root, no `shokuknow`, no git/jj
  mutation, no network fetch, no credential material read or echoed.
- Scratch `$HYAKU_SCRATCH/kasegi-r33/ExecCensusAfter/` (default `/fast/scratch/hyaku`) held
  `base-SOURCES.md`, `d1`/`d2`, `val`, `six`; removed before yield
  (`rm -rf -- "$S"`; `ls -d` → `No such file or directory`). No tree left on disk by this seat.
- No tool installed or upgraded; none was needed.
- No blockers. Risk (inherited, not mine): later scribe edits to `corpus/SOURCES.md` would
  invalidate this snapshot; the digest above (`b22c7f01…`) makes any such change detectable by
  re-hashing that one path.
