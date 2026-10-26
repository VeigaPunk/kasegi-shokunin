# ScoutImmunefiLive — round-34 live re-open of S051 (Immunefi VSCS v2.2)

Seat: ScoutImmunefiLive (L2 leaf, kasegi-shokunin round 34). Read-only over the lane; no lane file other than this receipt was written. Access date: **2026-10-26** (UTC stamps below).

## Verdict

| check | expected | observed | verdict |
|---|---|---|---|
| HTTP status, instrument UA | 200 | `status=200` | PASS |
| live text vs `corpus/source-snapshots/round-34/S051.txt`, normalized (whitespace-collapsed) | 0 differing lines | `diff` = 0 lines, exit 0; 175 lines / 8 502 bytes each | PASS |
| byte-level (stronger than asked) | — | `cmp` byte-identical; sha256 equal both sides | PASS |
| gate quote 1 `At Immunefi, we classify bugs on a simplified 5-level scale:` occurs exactly once live | `grep -c` = 1 | 1 (live L46); 1 in snapshot | PASS |
| gate quote 2 `Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield` exactly once live | `grep -c` = 1 | 1 (live L75, `- ` bullet prefix); 1 in snapshot | PASS |
| page identifies v2.2 | yes | live L1 `Immunefi - Immunefi Vulnerability Severity Classification System - v2.2 \| Immunefi`; L45 `Immunefi Vulnerability Severity Classification System - v2.2` | PASS |
| index lists v2.2 and v2.3 both in use | yes | index L49 `Currently in Use`, L50 `… System v2.3`, L51 `… System v2.2`, L52 `Being Phased Out` | PASS |

## Report

Instrument: `corpus/instruments/capture-source.py` (UA `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`, `collapse()` + `html_to_text()` normalization, no change to the script). Scratch: `/fast/scratch/hyaku/kasegi-r34/ScoutImmunefiLive/`, removed by `trap 'rm -rf -- "$S"' EXIT` in each shell call. No tool installed or upgraded.

### Commands and output (verbatim)

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-26T05:35:45Z
$ python3 corpus/instruments/capture-source.py --id S051 --url https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ --out $S/live.txt
S051 status=200 fetched_bytes=219383 snapshot_bytes=8502 sha256=4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5 utc=2026-10-26T05:35:45Z out=…/live.txt
exit=0
$ python3 corpus/instruments/capture-source.py --id IDX --url https://immunefi.com/severity-classification-systems/ --out $S/idx.txt
IDX status=200 fetched_bytes=149273 snapshot_bytes=4122 sha256=2ca35aee10bd7923c0900b8a4502cdd542a24a08cf30c298a047708d42010469 utc=2026-10-26T05:35:46Z
exit=0
$ python3 corpus/instruments/capture-source.py --id V23 --url https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-3/ --out $S/v23.txt
V23 status=200 fetched_bytes=230876 snapshot_bytes=12895 sha256=f669160df3e367abaa2aaaf819f26c1b248062e68190ba30389981085a2a979a utc=2026-10-26T05:35:46Z
exit=0
```

Snapshot comparison (`norm` = `tr -s ' \t\r' ' ' | sed 's/^ //;s/ $//' | grep -v '^$'` applied to both):

```
$ diff <(norm snapshot) <(norm live) | wc -l   -> 0      (diff exit 0)
$ wc -lc a b                                    -> 175 8502 / 175 8502
$ sha256sum S051.txt live.txt a b               -> 4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5 (all four)
$ cmp corpus/source-snapshots/round-34/S051.txt live.txt  -> BYTE-IDENTICAL
```

The committed manifest (`corpus/source-snapshots/round-34/manifest.json`) pins the same sha256 `4fd8ed98…b325a5`, `fetched_bytes=219383`, `snapshot_bytes=8502`; the live fetch reproduces all three (captured 05:31:10Z, re-opened 05:35:45Z, same 219 383 raw bytes).

Gate quotes (`grep -cF`):

```
Q: At Immunefi, we classify bugs on a simplified 5-level scale:
 live grep -c: 1   snapshot grep -c: 1   live: 46:At Immunefi, we classify bugs on a simplified 5-level scale:
Q: Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield
 live grep -c: 1   snapshot grep -c: 1   live: 75:- Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield
```

Anchors L46 and L75 match manifest Q1 (`anchor` 46) and Q8 (`anchor` 75).

Version identification (`grep -n "v2\.2\|v2\.3"` on live): L1 and L45 name v2.2; no v2.3 string occurs on the v2.2 page. `grep -n -i "latest\|current\|superseded\|deprecated\|phased\|newer"` on the v2.2 page: no match (exit 1) — the page itself makes no recency/status claim, consistent with S051's no-`latest` scoping (see ScribeSOURCESRow §3).

Index `https://immunefi.com/severity-classification-systems/` (83 lines, 4 122 bytes), verbatim L47-L59 excerpt:

```
49:Currently in Use
50:Immunefi Vulnerability Severity Classification System v2.3
51:Immunefi Vulnerability Severity Classification System v2.2
52:Being Phased Out
53:Immunefi Vulnerability Severity Classification System v2.1
54:… v2 / 55: … v1.2 / 56: … - Updated / 57: … (unversioned)
```

v2.3 page re-open: status 200, 221 lines, L45 `Immunefi Vulnerability Severity Classification System - v2.3` — a distinct, longer document (12 895 bytes vs 8 502), so v2.2 is not an alias of v2.3.

### Findings for the L1

1. S051 re-opens clean: the committed snapshot is byte-identical to a fresh live capture; both gate quotes occur exactly once; v2.2 is named on the page.
2. The index puts v2.2 and v2.3 together under `Currently in Use`; v2.2 is not retired. Any knowledge-entry wording that says v2.2 is "the current/latest" system would be wrong; "one of the two systems in use on 2026-10-26" is supported. The index and v2.3 captures here are uncommitted observations (digests above, `2ca35aee…010469` and `f669160d…79a`), not repo-pinned evidence.
3. Unresolved/not done: no committed capture of the index page exists; if the entry cites the in-use status it needs one (scribe/exec decision, not mine).
4. Scratch: the session shell is persistent, so the `EXIT` traps did not fire and the directory survived my tool calls; I removed it explicitly (`rm -rf -- /fast/scratch/hyaku/kasegi-r34/ScoutImmunefiLive`) and confirmed `ls -d` → `No such file or directory` (exit 2) after the receipt was written.
