# RevCounters2 — independent C2 counter re-run, round 28 wave 1

Seat: RevCounters2 (reviewer, leaf — no dispatch). Item: re-run the four frozen C2
counter commands from `.ufo/waves/round-28/claims.json` after the C2 artifacts land;
paste commands/outputs/timestamps; PASS/FAIL each.

All commands executed from lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
read-only against the live tree. No tools installed (nothing needed; RULES.md channel
notes: no installs performed). No production file touched by this seat.

Repo state at observation: HEAD `94f387c` ("round-28: wave1 spec + dispatch"), parent of
which is the stated freeze base `c9f8b11` (`git merge-base --is-ancestor` → confirmed
ancestor). Working tree mid-wave: `M LOG.md`, `M corpus/README.md`,
`M corpus/SOURCES.md`, `?? corpus/source-snapshots/round-28/` — i.e. wave artifacts were
**uncommitted working-tree bytes** at observation time.

## Observation timeline (artifacts landed mid-run)

The C2 artifacts landed while this seat was running, in three snapshots. All values below
are verbatim observed, none interpolated.

| UTC | frontier awk | citing S042 | S042 rows | census | harness |
|---|---|---|---|---|---|
| 17:23:41Z | 12 | 0 | 0 | exit=0 | FileNotFoundError crash, rc=1 |
| 17:25:27Z | 12 | 0 | 1 | exit=1 (E11 ×2) | FileNotFoundError crash, rc=1 |
| 17:26:24Z | 12 | 1 | 1 | exit=0 | entries=15 pass=15 exit=0, rc=0 |

Landing order observed: README F12 row first, then SOURCES.md S042 row + S041 used-by
(17:25:27Z, census correctly flagged `E11 S041/S042 missing used-by …` while the entry
file was still absent), then `corpus/knowledge/japanese-domestic-disclosure-workflow.md`
(between 17:25:49Z and 17:26:24Z), which closed both the census E11s and the harness.

## The four frozen counters — final run, 2026-10-25T17:26:24–25Z

### Counter 1 — frontier admitted (expect after: 12)

```
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
12
```

**PASS** — 12 admitted rows. The F12 row reads
`| F12 | Japanese state-coordinated disclosure workflow | admitted | knowledge/japanese-domestic-disclosure-workflow.md | S041, S042 | … |`
(corpus/README.md:213) plus an appended `[r28 amendment, appended 2026-10-25]` block
recording 12/12 — the old 11/11 parenthetical is retained as history, not rewritten (R9).

### Counter 2 — entries citing S042 (expect after: 1)

```
$ grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l
1
```

**PASS** — exactly one file; the harness run below confirms it is
`knowledge/japanese-domestic-disclosure-workflow.md` with declared `source:` ids
S041,S042 (printed `ids=S041,S042`).

### Counter 3 — S042 row count + census (expect after: 1 row, exit 0)

```
$ grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md
1
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo census_exit=$?
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

**PASS** — exactly one `| S042 |` row (SOURCES.md:48; tier A, docs, `mined`,
opened 2026-10-25, recheck `180d`, used-by exactly
`corpus/knowledge/japanese-domestic-disclosure-workflow.md`). Census exits 0; the two
`W04` duplicate-url warnings are pre-existing (S028/S029, also present at 17:23:41Z).
S041 used-by cell (SOURCES.md:47) gains the entry; the old→new is logged in the registry's
own change-log block (`git diff` shows the appended `S041 used-by cell old → new` line).

### Counter 4 — frontier harness (expect after: entries=15 pass=15 exit=0)

```
$ python3 corpus/instruments/frontier-recheck-count.py; echo rc=$?
… (14 prior PASS rows F01–F11, all exit=0) …
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0
entries=15 pass=15 exit=0
rc=0
```

**PASS** — `entries=15 pass=15 exit=0`, rc=0. The F12 row's recheck actually executed
(`exit=0`, i.e. source-recheck ran against the round-28 manifest selecting S041,S042 and
returned 0 — manifest.json pins ids ["S041","S042"] → paths ["S041.txt","S042.txt"],
schema_version 1, verified by direct json.load this run).

## Kill-rule cross-check (C2)

- Source row without admitted entry citing it: **no** — S042 row + F12 `admitted` row +
  entry header `source: S042` all present.
- Census exit ≠ 0 at round end: **no** — 0 at final observation. (Mid-wave exit=1 was the
  registry-before-entry landing order, resolved by the entry landing; noted, not
  actionable.)
- Harness pass < entries: **no** — 15=15.
- Entry recheck --source ids ≠ declared source: ids: **no** — harness would flag
  `header-sources-not-rechecked`; the F12 row is clean PASS.
- Manifest quote-assertion exactly-once/anchor-broken: **outside this seat's four-command
  scope** — not verified here; other seats own it. Verification gap, named honestly.

## Mid-wave torn-state behavior worth recording (observed, not judged)

- `frontier-recheck-count.py` on a README-admitted-but-absent entry does not print a FAIL
  row: `entry_contract` (line 65) raises raw `FileNotFoundError` out of `evaluate`,
  killing `main` before the `entries=` summary — traceback + rc=1 (verbatim, 17:23:41Z
  and 17:25:27Z). Honest outcome: it cannot fake a pass and cannot print `pass<entries`
  in torn state. Non-blocking once artifacts complete.
- `sources-census.sh` E11 correctly flagged the dangling used-by while the entry file was
  absent — the instrument caught exactly the state it exists to catch.

## Owed re-runs

None outstanding from this seat — all four counters observed **post-land** values at
17:26:24Z. One belt-and-braces re-run is owed **after the L1 commits the wave** (values
above are uncommitted working-tree bytes; a commit could in principle differ):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md && \
grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l && \
grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md && \
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo census_exit=$?; \
python3 corpus/instruments/frontier-recheck-count.py; echo rc=$?
```

Expected post-commit: `12`, `1`, `1`, `census_exit=0`, `entries=15 pass=15 exit=0`, `rc=0`.

## Verdict

All four frozen C2 counters **PASS** on observed post-land bytes at 2026-10-25T17:26:24Z.
Do-nothing control is not in play: values 12/1/1/15-of-15 are genuine post-land results,
not reachable by an unmodified tree (verified across three timed snapshots showing the
progression 11-ancestor → partial → final). Coverage axis predicate satisfied as far as
these four counters measure it.
