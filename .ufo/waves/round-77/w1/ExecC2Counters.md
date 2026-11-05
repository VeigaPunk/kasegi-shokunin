# ExecC2Counters — round-77 attempt-1 C2 counter re-derivation (seat ExecC2Counters-2)

Scope: read-only over the lane tree and my scratch. No lane file edited, no git mutation.
Scratch used: /fast/scratch/hyaku/kasegi-r77/ExecC2Counters-2/ (removed before yield; receipts copied here).
Tool installs: none (no tool installed or upgraded by this seat).
Freeze HEAD verified: `git -C kasegi-shokunin rev-parse HEAD` -> 539a43877809bd90b6f506e8fd24a6d871598cd5; `--show-toplevel` -> the lane root.

## Verdict

- B0 (pre-freeze source-recheck, frozen manifest): PASS
- B5 (landing-time source-recheck re-run, frozen manifest): PASS (identical output to B0)
- Base counters at 2e53fc74776824898b5c5eb914aeddc19a091157: PASS (111 / 91 / 93 / 91 / sort clean on .md rows)
- Freeze-tree counters: PASS (registry 112 with S112 at line 124; records=91 bound=91 unbound=0 rc 0; FRONTIER-CENSUS rows=53 admitted=53 closed=53 problem-rows=0 registry=112; entries=56 pass=56 exit=0)
- Frozen bytes: `git diff --stat 539a4387 -- <frozen paths>` empty, diff_rc=0. Controls, claims.json, manifest, S112.txt and SOURCES.md match the freeze commit.

## Findings

F1 (routed, instrument/manifest semantics; not a counter failure). Two declared anchors do not
point at the line that holds their quote. Under `corpus/instruments/source-recheck.py:anchor_verdict`
the anchor check reads a four-line window, `raw_lines[anchor-1:anchor+3]`, so `anchor=N-ok` means
"quote lies within lines N..N+3", not "quote is on line N".
- Q04-params-same: declared anchor 30 (line 30 = `Parameters`); quote is on line 31.
  Verbatim-at-anchor (exact line) = NO. Source-recheck still prints `anchor=30-ok` because the window covers 30-33.
- Q05-pagination-instructions: declared anchor 31; quote is on line 32. Exact-line = NO. Window prints `anchor=31-ok`.
- The other 11 quotes are verbatim on their declared anchor line.
- Frozen manifest bytes cannot be edited. Routed to the L1 as a semantics finding: either the
  instrument documents the window as the verification rule, or the anchor definition is stated as
  "window start". Evidence: `.ufo/waves/round-77/w1/ExecC2Counters-quotes.tsv` columns verbatim_at_anchor,
  `sed -n '30,33p'` output below.

F2 (informational, base SOURCES.md). The S-row lexical order is not sorted at base: `LC_ALL=C sort -c`
on the base `| S### |` rows reports `sort: -:57: disorder: | S056 |` (rc=1). Not a predicate of
C2 (B1-B7 sort only the `.md` rows of knowledge-expected.txt, which are clean). Recorded so the base
row order is not assumed sorted.

F3 (observed, lane status). `git status --porcelain` lists 6 untracked paths, none in the frozen set:
`.ufo/waves/round-77/w1-dispatch.json`, `w1-spec.json`, `w1.ready`, `w1.ready.dispatched`, `w1/`,
`corpus/lessons/round-77.md`. The freeze-path diff is empty.

## Quote table (manifest S112, 13 quotes)

Full table: `.ufo/waves/round-77/w1/ExecC2Counters-quotes.tsv`. Summary:
- All 13 quotes have normalized alphanumeric length >= 36 (min Q08-400 = 36). None under MIN_QUOTE_CHARS=12.
- All 13 normalized occurrences in S112.txt = 1 (no quote is non-unique).
- Verbatim at declared anchor: 11 YES; Q04 (anchor 30) and Q05 (anchor 31) NO (see F1).
- Normalized-at-anchor (the instrument's window rule): 13 YES.

## Command receipts

Each block: command, then output, then rc.

### 1. Base counters (2e53fc74...)
```
$ git show 2e53fc74...:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
111   [rc=0]
$ git ls-tree --name-only 2e53fc74... corpus/knowledge/ | grep -c '\.md$'
91    [rc=0]
$ git show 2e53fc74...:corpus/instruments/knowledge-expected.txt | wc -l
93    [rc=0]
$ git show 2e53fc74...:corpus/instruments/knowledge-expected.txt | grep -cE '\.md$'
91    [rc=0]
$ knowledge-expected .md rows | LC_ALL=C sort -c
sort_rc=0   [rc=0]
$ diff(knowledge-expected .md rows sorted, corpus/knowledge/ listing sorted)
SET-EQUAL   [rc=0]
$ SOURCES S-rows | LC_ALL=C sort -c       (informational, F2)
sort: -:57: disorder: | S056 | CISA, Minimum Requirements ...   [rc=1]
```

### 2. Freeze-tree counters
```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   -> 112  [rc=0]
$ grep -n 'S112' corpus/SOURCES.md
124:| S112 | OSV.dev API reference, POST /v1/querybatch (OSV project) — https://google.github.io/osv.dev/post-v1-querybatch/ | docs | A | ...   [rc=0]
$ python3 corpus/instruments/capture-binding-check.py      (rc=0)
AUDIT records=91 with_url=91 with_fetched_utc=53 with_archival=38 snapshot_dirs=50 manifest_dirs=50 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=91 bound=91 unbound=0
FAIL lines = 0
$ python3 corpus/instruments/frontier-recheck-count.py      (rc=0)
FRONTIER-CENSUS rows=53 admitted=53 closed=53 problem-rows=0 registry=112
FRONTIER-PASS lines=53  FRONTIER-FAIL lines=0  other=0
entries=56 pass=56 exit=0
```

### 3. Manifest quote table
Table as in the TSV above (13 rows, columns: id, anchor, word_count, norm_alnum_len, under_12, verbatim_at_anchor,
normalized_at_anchor, normalized_occurrences_capture, quote). Every quote has word count 7-20 and alnum length 36-104.

### 4. source-recheck B0/B5 receipt (independent re-run)
```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-77/manifest.json --source S112
S112:sha256 OK
S112:Q01-batch-definition OK occurrences=1 anchor=24-ok
S112:Q02-return-shape OK occurrences=1 anchor=24-ok
S112:Q03-ordering OK occurrences=1 anchor=24-ok
S112:Q04-params-same OK occurrences=1 anchor=30-ok
S112:Q05-pagination-instructions OK occurrences=1 anchor=31-ok
S112:Q06-item-rules OK occurrences=1 anchor=34-ok
S112:Q07-version-rule OK occurrences=1 anchor=35-ok
S112:Q08-400 OK occurrences=1 anchor=36-ok
S112:Q09-partial-tokens OK occurrences=1 anchor=166-ok
S112:Q10-individual-1000 OK occurrences=1 anchor=168-ok
S112:Q11-total-3000 OK occurrences=1 anchor=169-ok
S112:Q12-threading-variance OK occurrences=1 anchor=170-ok
S112:Q13-next-request OK occurrences=1 anchor=195-ok
rc=0
```
Identical to the frozen pre-freeze receipt `controls/c2-prerecheck-r77.txt` (diff: none).

### 5. Capture bytes
```
$ sha256sum corpus/source-snapshots/round-77/S112.txt
f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907
$ wc -c < ...S112.txt  -> 4575 ;  wc -l -> 216      (manifest: bytes 4575, lines 216, sha256 f3ca0465...)
```

### 6. Anchor evidence for F1
```
$ sed -n '30,33p' corpus/source-snapshots/round-77/S112.txt | cat -n
1 Parameters
2 The parameters are the same as those in POST /v1/query, but you can make multiple queries.
3 Instructions are available for handling pagination for querybatch requests.
4 Version rules
$ grep -nF '<Q04 quote>' S112.txt  -> 31:...
$ grep -nF '<Q05 quote>' S112.txt  -> 32:...
```

## Checks main agent should run
- `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-77/manifest.json --source S112` (rc 0, 13 OK)
- `python3 corpus/instruments/capture-binding-check.py` (records=91 bound=91 unbound=0)
- `python3 corpus/instruments/frontier-recheck-count.py` (FRONTIER-CENSUS rows=53 ... registry=112; entries=56 pass=56 exit=0)
- `git show 2e53fc74...:corpus/instruments/knowledge-expected.txt | grep -cE '\.md$'` (91)

## Not run by this seat
The C1 counter (recheck-cwd-census.py) is outside this assignment; it was not executed.
