# ExecC2Gate — C2 B0–B7 gate on the round-79 F55 draft

Seat: ExecC2Gate (leaf, read-only against the lane; scratch mirror only).
Claim: C2 (axis `coverage`), round 79 attempt 1, base `d16d2124fd5262f5a8088aa598f1e628f897d3ab`, freeze commit `9d0b1eb0709e47c3c6decc09138b5012a8968924`.
Scratch: `/fast/scratch/hyaku/kasegi-r79/ExecC2Gate` (S; deleted at yield). Nothing written outside S and this report. No tool installs were needed.

**Verdict: B0 met, B1 met, B2 met, B3 met, B4 met (non-discriminating — see B4), B5 met, B6 met, B7 met. No defect found in the draft that makes a counter fail.**

---

## 1. Mirror construction (integration receipt)

Inputs from sibling ScribeEntry, all present when first polled (second 55 s poll):

```
$ ls -la .ufo/waves/round-79/w1/c2
-rw-r--r-- 4079 Nov  6 15:54 README-F55.md
-rw-r--r-- 1383 Nov  6 15:54 SOURCES-S113-row.md
-rw-r--r-- 4893 Nov  6 15:54 knowledge-expected.txt
-rw-r--r-- 17424 Nov  6 15:53 osv-determineversion-cc-library-versioning.md
```

Freeze extraction:

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 9d0b1eb0709e47c3c6decc09138b5012a8968924 | tar -x -C $S/tree
EXTRACT OK
$ ls $S/tree/corpus/knowledge/*.md | wc -l
92
```

Integration steps and their arithmetic:

1. Entry placed: `cp <c2>/osv-determineversion-cc-library-versioning.md $S/tree/corpus/knowledge/`
   sha256 source == destination == `ba2638cd22b14a63061d97baa5913f0fad3d4350a13a5b84e6d932b1a068e0a8` (17424 bytes, 120 lines, single final `\n`, no CR).
2. S113 row flipped in `$S/tree/corpus/SOURCES.md`, exact cell comparison old vs `SOURCES-S113-row.md`:

```
CELL 7 DIFFERS
  old: ' queued '
  new: ' mined '
CELL 10 DIFFERS
  old: ' — '
  new: ' corpus/knowledge/osv-determineversion-cc-library-versioning.md '
byte-equal overall: False
```

   Only cells 7 (status) and 10 (used-by) change; the other nine cells are byte-identical to the freeze row.
3. `cp <c2>/knowledge-expected.txt $S/tree/corpus/instruments/knowledge-expected.txt` (sha256 `b4e9b5106937e0da1a770ae08cc150dfc8cab5d0d5fa42215d166e1150341ccf` both sides).
4. `README-F55.md` lines 1–13 appended to `$S/tree/corpus/README.md` after one blank line. Lines 14 (`---`) and 15–19 of that file are a **PROVINCE.md end-of-file amendment**, not README text, and were **not** applied by this seat (PROVINCE.md is outside the seat's write scope; the L1 must apply it).

Landing hashes of the four integrated files:

```
ba2638cd22b14a63061d97baa5913f0fad3d4350a13a5b84e6d932b1a068e0a8  corpus/knowledge/osv-determineversion-cc-library-versioning.md
9273c51a024f0b170ee18d131a923da1dc7b7bddd714248275eaa50c1caf74b4  corpus/SOURCES.md
987f3ec497ff3d453d8285b92d4efb9df4cc814498bf0299b2b425cf8a0b834e  corpus/README.md
b4e9b5106937e0da1a770ae08cc150dfc8cab5d0d5fa42215d166e1150341ccf  corpus/instruments/knowledge-expected.txt
```

Landing delta vs a second pristine extraction of the same commit (`diff -rq base-tree tree`): exactly `corpus/SOURCES.md`, `corpus/README.md`, `corpus/instruments/knowledge-expected.txt` modified and `corpus/knowledge/osv-determineversion-cc-library-versioning.md` added. The only other paths `diff -rq` reports are the round-31 `ExecCensusDry/validate/*` fixtures, whose `corpus/instruments` and `corpus/knowledge` entries are git symlinks (`120000`) into the lane corpus, i.e. the same files, not separate changes.

## 2. Before-state on the same mirror (do-nothing replication)

```
$ cd $S/base-tree && python3 corpus/instruments/frontier-recheck-count.py | grep FRONTIER-CENSUS
FRONTIER-CENSUS rows=54 admitted=54 closed=54 problem-rows=0 registry=113
entries=57 pass=57 exit=0                       # no F55 record

$ ls corpus/knowledge/*.md | wc -l            -> 92
$ wc -l < corpus/instruments/knowledge-expected.txt ; grep -c '\.md$' corpus/instruments/knowledge-expected.txt
94
92
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 113
$ grep -c '| mined ' corpus/SOURCES.md        -> 92
$ python3 corpus/instruments/capture-binding-check.py | tail -1
records=93 bound=93 unbound=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-79/manifest.json --source S113 | tail -2 ; rc=0
```

So at the freeze commit B1/B2/B3 are unmet-in-before-state as the claim's `do_nothing` says; **B4 and B0 are already true at the freeze** (the S113 row landed with the freeze; the committed pre-freeze control `controls/c2-donothing-counters-r79.txt` shows `unbound=1` only because it predates that row). B4 is therefore non-discriminating for this round.

## 3. Per-predicate receipts (all run with cwd `$S/tree`)

### B0 — source recheck on S113 — **met**

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-79/manifest.json --source S113
S113:sha256 OK
S113:Q01-purpose OK occurrences=1 anchor=25-ok
S113:Q04-library-set OK occurrences=1 anchor=41-ok
S113:Q05-coverage-limit OK occurrences=1 anchor=41-ok
S113:Q06-ranked-versions OK occurrences=1 anchor=55-ok
S113:Q07-file-hashes OK occurrences=1 anchor=61-ok
S113:Q08-hash-encoding OK occurrences=1 anchor=62-ok
S113:Q09-extensions OK occurrences=1 anchor=66-ok
S113:Q10-response-order OK occurrences=1 anchor=85-ok
rc=0
```

Byte-identical to `controls/c2-prerecheck-r79.txt` apart from that control's trailing `rc=0` line (`diff` of body: only `10d9 < rc=0`). Snapshot sha256 `f4bce05304157a593dcea94f400238e3eda62f73e6678a6e296260a428138ebf` (5669 bytes, 127 lines) re-derived from the extracted tree.

### B5 — landing recheck + the entry's own `recheck:` line — **met**

The entry carries exactly one `recheck:` line:

```
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-79/manifest.json --source S113
```

`EXACT PREFIX OK: True` against the predicate's required form (the B0 command behind `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && `). Run with the `cd` prefix pointed at the mirror (`cd $S/tree`): the full B0 output above, `rc=0`.

Independent quote check (manifest anchor line vs entry text): all eight quotes are a byte substring of their declared snapshot line and appear verbatim in the entry, word counts 19/18/12/22/14/7/11/14 (`len(split())`, all ≤25, matching the entry's Gate table).

### B1 — exactly one registry row changed — **met**

```
$ diff -u $S/freeze-SOURCES.md corpus/SOURCES.md
--- freeze-SOURCES.md
+++ SOURCES.md
2 removed lines / 2 added lines, both `row=S113`
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   -> 113   (freeze: 113)
$ grep -c '| mined ' $S/freeze-SOURCES.md ; grep -c '| mined ' corpus/SOURCES.md -> 92 / 93
$ grep -c '| queued ' corpus/SOURCES.md -> 1
```

No row added, none removed; the single changed row changes only status (`queued`→`mined`) and used-by (`—`→`corpus/knowledge/osv-determineversion-cc-library-versioning.md`), exactly the predicate's two cells. The row's URL cell still carries one `https://` token (also enforced by B4).

### B2 — knowledge inventory 92→93, expected 94/92→95/93 — **met**

```
$ ls corpus/knowledge/*.md | wc -l                                              -> 93
$ wc -l < corpus/instruments/knowledge-expected.txt ; grep -c '\.md$' <same>    -> 95 ; 93
$ grep '\.md$' corpus/instruments/knowledge-expected.txt | LC_ALL=C sort -c    -> rc=0
$ diff <(grep '\.md$' expected | LC_ALL=C sort) <(ls corpus/knowledge/*.md | LC_ALL=C sort) -> no output, diff_rc=0
```

`diff -u freeze-expected new-expected` is exactly one inserted line, in C-order position:

```
+corpus/knowledge/osv-determineversion-cc-library-versioning.md
```

### B3 — frontier census 54→55 — **met**

```
$ python3 corpus/instruments/frontier-recheck-count.py | grep -E 'FRONTIER-CENSUS|F55'
FRONTIER-CENSUS rows=55 admitted=55 closed=55 problem-rows=0 registry=113
FRONTIER-PASS F55 ids=S113
PASS     F55  knowledge/osv-determineversion-cc-library-versioning.md ids=S113           exit=0
rc=0
```

Full run tail: `entries=58 pass=58 exit=0` (57→58). The F55 README row has the six-cell frontier shape, status `admitted`, entry `knowledge/osv-determineversion-cc-library-versioning.md`, sources `S113` — and the entry's `source: S113` declaration balances the recheck line's `--source S113` in both directions (rule A).

### B4 — capture binding — **met (non-discriminating this round)**

```
$ python3 corpus/instruments/capture-binding-check.py | tail -2
AUDIT records=93 with_url=93 with_fetched_utc=55 with_archival=38 snapshot_dirs=52 manifest_dirs=52 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=93 bound=93 unbound=0
rc=0
```

Before-state on the pristine freeze extraction is also `unbound=0` (§2): the S113 row landed in the freeze commit, so this predicate cannot separate before from after here. It is met, and it is not evidence of the entry's admission on its own.

### B6 — literal distinctness of the eight pinned quotes — **met**

`grep -F -l` of each manifest quote over `corpus/knowledge/*.md`, excluding the new entry (92 base files):

```
Q01-purpose          grep_rc=0 hits_excluding_new=0
Q04-library-set      grep_rc=0 hits_excluding_new=0
Q05-coverage-limit   grep_rc=0 hits_excluding_new=0
Q06-ranked-versions  grep_rc=0 hits_excluding_new=0
Q07-file-hashes      grep_rc=0 hits_excluding_new=0
Q08-hash-encoding    grep_rc=0 hits_excluding_new=0
Q09-extensions       grep_rc=0 hits_excluding_new=0
Q10-response-order   grep_rc=0 hits_excluding_new=0
```

0/8, matching the claim's frozen measurement. The entry's own subject sweep also holds: `grep -rli 'determineversion\|indexer' corpus/knowledge/` on the 92-entry base prints nothing and exits 1. No base file contains any of the eight sentences.

### B7 — sources census — **met**

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/tree/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	W04	S076 duplicate url docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories across scopes
file	W04	S080 duplicate url ossf.github.io/osv-schema across scopes
file	W04	S085 duplicate url csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema across scopes
file	ok	/fast/scratch/hyaku/kasegi-r79/ExecC2Gate/tree/corpus/SOURCES.md
rc=0
```

Exactly the six inherited W04 warnings the predicate allows (S028 S029 S072 S076 S080 S085) and no new finding; the S113 used-by resolves. The literal predicate form (against the lane's committed file, still the freeze state at gate time) also exits 0 with the same six warnings:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04 ... (six inherited)
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
rc=0
```

Counter-sensitivity control: a copy of the landed registry with S113's used-by rewritten to `corpus/knowledge/does-not-exist-r79.md` gives `file E11 S113 missing used-by ...`, `rc=1` — the ok line is not vacuous.

## 4. Entry recheck audit (named in the seat item)

```
$ python3 corpus/instruments/recheck-audit.py --root $S/tree --quiet
strict pass=0/93 cdroot_fail=93 instrument_fail=0 own_fail=0
executes=71 gated=22 broken=0
lines=93 total=93 pass=93 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=93 missing=0 unexpected=0 exit=1
```

The `exit=1` is a mirror artifact, not the entry's: every one of the 93 `recheck:` lines begins `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`, so with `--root` at a scratch copy the `cdroot` limb fails for all 93 (the pristine before-state is `strict pass=0/92 cdroot_fail=92 ... pass=92 ... expected=92 missing=0 unexpected=0 exit=1` — same class, one fewer line). Re-run with the instrument's own scratch-copy option, `--cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin`:

```
$ python3 corpus/instruments/recheck-audit.py --root $S/tree --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
strict pass=93/93 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=71 gated=22 broken=0
lines=93 total=93 pass=93 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=93 missing=0 unexpected=0 exit=0
rc=0
```

(before-state with the same `--cdroot`: `strict pass=92/92`, `exit=0`). The new entry's own record is `... lane=0 foreign=0 executes FROZEN-ONLY`, identical in class and exit behaviour to its 92 peers. Expected-list equality holds: `missing=0 unexpected=0`.

## 5. Draft defects

**None that makes a counter fail.** Every B0–B7 predicate is met on the integrated mirror. Findings that the L1/reviewer should carry, none of which changes a verdict:

1. **`README-F55.md` lines 14–19 are not README content.** After the `---` divider the draft carries a `PROVINCE.md end-of-file amendment` paragraph. It was not appended to `corpus/README.md` here (it would corrupt the frontier tables) and PROVINCE.md is outside this seat's write scope. The L1 must apply it to `PROVINCE.md` as an R6 end-of-file append.
2. **B4 does not discriminate this round.** `unbound=0` already at the freeze commit (the S113 row is part of the freeze). The claim's own `do_nothing` names B1/B2/B3 as the unmet before-state, which reproduces exactly.
3. **B7's literal `--root … kasegi` form validates the lane's committed file**, which is still the freeze state until the L1 lands the row; it exits 0 today. Evidence for the landing bytes is the `--file` form on the mirrored `corpus/SOURCES.md` (rc=0, six inherited W04, no new finding). The L1 must re-run the literal `--root` form after landing.
4. **`recheck-audit --root <scratch>` exits 1 by construction** (cdroot limb against a mirrored root, 93/93). Use `--cdroot <lane>` for a scratch copy; at the real landing root it is `exit=0`.
5. Minor, verified rather than defective: the entry's six Limits absence greps (`rate limit|…|credential`, `paginat|next_page_token`, `timeout|limit|maximum`, `severity|CVE|cvss`, `error|status code|throttl`, `worker|thread|proxy`) all print nothing and exit 1 on the capture; the Distinctness citations `osv-post-v1-query-contract.md:11,19,29,31,37,45,53,75`, `osv-post-batch-query-contract.md:11,19,27,35,43`, `osv-affected-range-events.md:21,33` all resolve to the headings/paragraphs the entry names; the entry's cited unpinned spans (`:46-53` tool section, `:75-83` payload, `:86-100` response schema, `:101-126` sample response, `:67-72` extension list, `:23` page heading, `:37/:39/:64` not-claimed lines) are at those lines in `S113.txt`.

## 6. Scoped statement

The frozen claim's kill rule fires on any of B0–B7 false, on a claimed clause absent from its declared line, or on a B6 literal count above zero. On the integrated mirror: B0–B7 all met, all eight clauses verbatim on their declared lines (25, 41, 41, 55, 61, 62, 66, 85), and the B6 literal count is 0/8. This seat's evidence is a scratch mirror, not the landing commit; the L1's landing re-run of B0/B5 and the literal B7 form remains the closing act.
