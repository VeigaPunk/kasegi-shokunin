# ExecC2History — capture-secret-scan exposure inventory (Kasegi round 87, C2)

Seat: ExecC2History. Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Instrument run in place: `corpus/instruments/capture-secret-scan.py` (reads
`capture-secret-allow.tsv` beside itself). Command per commit:
`python3 -B corpus/instruments/capture-secret-scan.py --lane <lane> --rev <sha>`.
No credential values were read, copied, or written anywhere in this inventory:
the instrument prints only `HIT shape=/path=/line=` lines and summary counts.

## Range scanned

34 commits, oldest first, from `4ab545865f747fca8456370b5927fe51236fe579`
(round-80 freeze) to `132e16c588a2424c06b5ca15ea01fce1ee9a396d` (round-87 C2
landing, == `master` tip). All 34 dated 2026-11-06. Every commit ran to a
summary line: 27 × `rc=0` (clean), 7 × `rc=1` (hits), 0 × `rc=2` (errors).
The caller's formula `git log --format=%H --since=2026-11-01 master` was run
as a cross-check over 178 commits and produced the identical hit set on the
same 7 commits (older commits are uniformly clean).

Full per-commit TSV: `ExecC2History-receipts/history.tsv` (columns: commit,
date, hits, files, allowed, unused_allow, scanned, rc, lines — see
`ExecC2History-receipts/README.txt`). Run receipt:
`ExecC2History-receipts/run-receipt.txt`. Timing:
`ExecC2History-receipts/master-timing.txt`.

## `aws-sts-session-token` exposure inventory

First commit carrying the hit: `a48fe8b9ee34cf4b38106ce0b2357bbff489cb1d`
(2026-11-06 21:49:19 -0300, "round-85: land C2 end-to-end priced practice
package corpus/practice/curl-h1-1913733 …"). `git log --diff-filter=A`
confirms this commit first added the file. Its parent `c0507adf` is clean
(scanned=900, hits=0) and has no such path in its tree.

Last commit carrying the hit: `e73c1f945b5c08f5ecfec13d9ff5acfaf8f865d0`
(2026-11-06 22:13:48 -0300, "round-86: revert 4 C1 repoints …"). The very next
commit, `b079a106f4108f5dea377ff72e1ef1ef5bd2efb5` (22:14:11 -0300, "round-86:
redact presigned-URL credential material …"), is clean — it is the redacting
commit, and its diff touches exactly the two hit paths (2 files, 2 lines).

Exact path set across the whole window (all 7 hit-commits, both paths, line 1,
one line per file):

- `.ufo/waves/round-85/w1/ScoutSources-receipts/live-LEAD-hackerone-ibb-1997312.json` (all 7 commits)
- `corpus/source-snapshots/round-86/S122.txt` (last 3 of the 7 commits: from `252df0c9` onward)

Commit-by-commit (all 2026-11-06, -0300):

| commit | time | hits | files | notes |
|---|---|---|---|---|
| `a48fe8b9` | 21:49:19 | 3 | 1 | first appearance of the r85 receipt JSON |
| `170cadf4` | 21:49:37 | 3 | 1 | round-85 landing receipt |
| `6013dc98` | 21:49:45 | 3 | 1 | ScoutSources KEV feed receipt |
| `d7296645` | 21:55:02 | 3 | 1 | round-85 verifier spot-check |
| `252df0c9` | 21:55:02 | 6 | 2 | round-86 freeze; adds `S122.txt`, which is the same JSON capture |
| `fdb5f4af` | 22:13:48 | 6 | 2 | round-86 C1 landing |
| `e73c1f94` | 22:13:48 | 6 | 2 | round-86 C1 revert correction (last dirty commit) |
| `b079a106` | 22:14:11 | 0 | 0 | **redaction commit; first clean commit after the window** |

Hit shapes on those paths (all three per file, each only on line 1):
`aws-sts-session-token`, `aws-access-key-id`, and the gate's generic
`credential` shape. 30 HIT lines total in the TSV (21 on the receipt JSON, 9
on `S122.txt`). No other shape appears anywhere in the window: the 27 clean
commits produce zero HIT lines, and no HIT line names any other path.

## Is every hit explained by the r85/r86 incident?

Yes, within this window:

- Both paths are the two files named in lesson M86-2
  (`corpus/lessons/round-86.md`): "the same shape was already in round-85
  receipt `.ufo/waves/round-85/w1/ScoutSources-receipts/live-LEAD-hackerone-ibb-1997312.json`"
  and the S122 capture of the same HackerOne report JSON, captured with
  `capture-source.py` and committed in freeze `252df0c9`.
- `b079a106`'s diff redacts exactly those two paths (one line each) and its
  own receipts bound the result: `.ufo/waves/round-86/l1/redact-presigned-r86.txt`
  records `REDACT` for `S122.txt` (`ceb01841…` → `08cab370…`) and for the r85
  receipt JSON (`c9359d11…` → `aa99fa71…`), plus seat copies; the follow-up
  scan `.ufo/waves/round-86/l1/redaction-scan-r86.txt` reports
  `artifacts=4 bad=0` over the redacted bytes.
- Note the asymmetry the scanner exposes: `S122.txt` only exists from the
  freeze `252df0c9` onward (6-hit commits), while the r85 receipt JSON was
  landed earlier, in `a48fe8b9` (3-hit commits) — i.e. the identical live
  token reached the pushed history once via the round-85 wave landing and
  again via the round-86 freeze capture, before the single redacting commit
  `b079a106` closed both. History itself was never rewritten (M86-2: "History
  is unchanged (no force-push)"), so the 7 dirty commits remain in `master`
  today; the instrument still reports them as hits, which is the correct
  behaviour for the open L0 exposure question.

## Allowlist note (counts only; no values)

`allowed`/`unused_allow` per commit are in the TSV. Summary: the
`capture-secret-allow.tsv` beside the instrument has 17 data rows. Commits
`cd1f568a`→`132e16c5` (with the round-87 rows) report `allowed=18
unused_allow=0`; the 12 commits `252df0c9`→`d7296645` report `allowed=16
unused_allow=2` (the two round-87 `S124.txt` rows are unused at those revs);
the 163 older commits outside the 34-commit window report `allowed=1
unused_allow=16` (17 rows, only one consumed). No match is ever allowed for
shape `aws-sts-session-token` — the instrument refuses such rows by design
(`NEVER_ALLOWED`), and none is present.

## Timing

One full `--rev master` scan: `real 1.053s` (user 0.945s, sys 0.033s),
`scanned=1319 hits=0 files=0 allowed=18 unused_allow=0 rc=0` — receipt in
`ExecC2History-receipts/master-timing.txt`. The 34-commit sweep took ~32s of
scanner time (~1s/commit; tree sizes grow from 236 to 1319 capture-class
paths across the window).

## Re-run

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
git log --reverse --format=%H 4ab545865f747fca8456370b5927fe51236fe579^..master | while read c; do
  python3 -B corpus/instruments/capture-secret-scan.py --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --rev "$c"
done
```

## Findings / routed defects

None beyond the recorded incident. The inventory finds no `aws-sts-session-token`
(or any other) hit in the round-80→round-84 range, no hit outside the two
M86-2 paths in rounds 85–87, and no residual hit at or after the redacting
commit `b079a106` (all 27 commits from `b079a106` to the C2 landing `132e16c5`
are `hits=0`). Nothing was changed: this seat wrote only this report and the
`ExecC2History-receipts/` directory it cites.
