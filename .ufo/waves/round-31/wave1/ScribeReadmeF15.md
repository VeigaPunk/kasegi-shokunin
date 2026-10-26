# ScribeReadmeF15 receipt — round 31, C2/F15 README appends

- Seat: `ScribeReadmeF15` (leaf). Round 31, wave 1. Lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`.
- Answering model: `devin/deepseek-v4-1-flash` (route-table default; no model passed).
- Write scope exercised: `corpus/README.md` (append only) + this receipt. No other path written. No git/jj mutation of any kind; read-only `git status` / `git diff` / `git rev-parse` only. No network fetch. No tool installed or upgraded (python3 + coreutils only); no pacman transaction.

## 1. Dependency receipt waited for, then read

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && timeout 1750 bash -c 'until [ -s .ufo/waves/round-31/wave1/ExecEntryF15.md ]; do sleep 20; done'
poll_exit=0
```
- `ExecEntryF15.md` arrived at 20:39 (12956 B); the entry it produced is
  `corpus/knowledge/vendor-third-party-finding-coordination.md` — 146 lines, 10359 B,
  sha256 `bf40fd9e56351b3a857f5efc45c508889bde75b736915b5c3011c63d36eafa79` (measured this seat:
  `wc -l -c` + `sha256sum`, output below).

```
$ wc -l -c corpus/knowledge/vendor-third-party-finding-coordination.md
  146 10359 corpus/knowledge/vendor-third-party-finding-coordination.md
$ sha256sum corpus/knowledge/vendor-third-party-finding-coordination.md
bf40fd9e56351b3a857f5efc45c508889bde75b736915b5c3011c63d36eafa79  corpus/knowledge/vendor-third-party-finding-coordination.md
```

**Superseded — see §7**: the entry was revised by its owner after this measurement; the
landed bytes are 160 lines / 11501 B / sha256 `1f16e371…`.

What I took from the entry for the appended wording (read at `:1-60` and `:60-146`):
- `source: S048` header (L2) with capture `corpus/source-snapshots/round-31/S048.txt:28-35`;
- three intake routes (L31-L34) and Microsoft naming itself "as a coordinator of
  vulnerabilities that affect multiple vendors" (L35);
- `## Honest limit` (L88): "It does not state the coordination agreements, a timeline, a
  reporting address or a per-vendor process" — the limit the `next` cell is tied to;
- `## What this adds beyond F06 and F10` (L60) names the contrast rows S039 (Hitachi) and
  S040 (Cisco), both F10 rows, which the `next` cell cites as the route-out shape.

## 2. Pre-append state (measured before the edit)

```
$ sha256sum corpus/README.md
df04b0490591446c6605d421569a497845c22546dc27ea5a020fff770f2fc64f  corpus/README.md
$ wc -c -l corpus/README.md
  291 29620 corpus/README.md
$ git status --porcelain corpus/README.md   # empty: file clean at HEAD
$ git rev-parse HEAD
8a8916c7043bd873d191b30dd1744b241b91f4d9
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
14
```

## 3. Append (R6: existing lines untouched)

Appended a `## Round-31 admission — coverage map row and Frontier F15 (appended 2026-10-25)`
section at the end of the file, mirroring the round-30 F14 section shape: R6 preamble, one
coverage-map row, one frontier row, one amendment paragraph. Verbatim (now lines 292-316):

```
## Round-31 admission — coverage map row and Frontier F15 (appended 2026-10-25)

The coverage map above is not edited in place (R6): the round-31 entry
`knowledge/vendor-third-party-finding-coordination.md` (Frontier F15, source S048; source
basis: the Microsoft Security Response Center's own Microsoft Security Vulnerability
Research (MSVR) page, captured 2026-10-25 under `corpus/source-snapshots/round-31/`) is
recorded here as an appended amendment so every existing line keeps its number. The
coverage-map row is appended here rather than inserted into the map, and the F15 frontier
row is listed here on the same table shape as the frontier above.

| Area | Entry | Source basis |
|---|---|---|
| A vendor's research programme as an intake route for other vendors' bugs (round 31) | knowledge/vendor-third-party-finding-coordination.md | S048 — public primary, opened 2026-10-25 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F15 | A vendor's research programme as an intake route for other vendors' bugs | admitted | knowledge/vendor-third-party-finding-coordination.md | S048 | Record which party coordinates a multi-vendor finding — the vendor itself, as S048's three intake routes and self-named coordinator role state, or an external centre, as F10's S039/S040 rows route it — and read no clock, contact or agreement into an intake route: the pinned capture states none. |

[r31 amendment, appended 2026-10-25] The parenthetical above records the round-26 frontier
state and is retained as history, not rewritten (R9): at round 31 the frontier stands at
**15/15 admitted** — F01-F08 at round 23, F09 at round 24, F10 at round 25, F11 at round
26, F12 at round 28, F13 at round 29, F14 at round 30, F15 at round 31. The 0/18 sentence
is untouched: the lost-domain denominator still holds 0 of 18 surfaces present, and the
frontier count stays outside it.
```

## 4. Verification — post-append, measured

```
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
15
```
```
$ git diff -U0 corpus/README.md | grep -E '^[-+]' | grep -v '^+++\|^---' | awk '{print substr($0,1,1)}' | sort | uniq -c
     25 +
$ git diff -U0 corpus/README.md | grep -c '^-[^-]'
0
$ git diff --stat corpus/README.md
 corpus/README.md | 25 +++++++++++++++++++++++++
 1 file changed, 25 insertions(+)
$ git diff -U0 corpus/README.md | sed -n '1,7p'
diff --git i/corpus/README.md w/corpus/README.md
index be773ed..dc9c207 100644
--- i/corpus/README.md
+++ w/corpus/README.md
@@ -291,0 +292,25 @@ outside it.
+
+## Round-31 admission — coverage map row and Frontier F15 (appended 2026-10-25)
```
So the diff is **additions only** — one hunk, `@@ -291,0 +292,25 @@`, zero deleted lines; the
`0/18` sentence and every earlier line keep their numbers.

R6 head-bytes identity (the strongest form: the first 29620 B of the post-append file are
byte-identical to the pre-append whole file):

```
$ head -c 29620 corpus/README.md | sha256sum
df04b0490591446c6605d421569a497845c22546dc27ea5a020fff770f2fc64f  -
pre-append whole-file sha256: df04b0490591446c6605d421569a497845c22546dc27ea5a020fff770f2fc64f
$ sha256sum corpus/README.md ; wc -c -l corpus/README.md
d9865b2e126c626559de9704d9e8d636b6f4ce7eba2a3a74e6f32d92b2146f98  corpus/README.md
  316 31530 corpus/README.md
```
Post-append: 29620 → 31530 B (+1910), 291 → 316 lines (+25).

Frontier-row parse check against the harness's own regex
(`FRONTIER_ROW = ^\|\s*(F\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`?([^|`]+?)`?\s*\|`,
`corpus/instruments/frontier-recheck-count.py:45`): the appended row yields
id=`F15`, status=`admitted`, entry=`knowledge/vendor-third-party-finding-coordination.md`.
The coverage-map row above it begins `| A vendor's …`, so it is not matched by that regex and
is not counted as a frontier row.

Read-only harness run on the tree as it stood at 20:41 (other seats' paths may still be in
flight; this run is cited only as evidence that **my** row parses and the F15 entry passes,
not as the C2 after-column — that belongs to the C2 counter owner):

```
$ python3 corpus/instruments/frontier-recheck-count.py 2>&1 | tail -4
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
entries=18 pass=18 exit=0
harness_exit=0
```

## 7. Erratum (appended 2026-10-25, after ExecEntryF15 finalised the entry)

`ExecEntryF15` revised the entry after my §1 measurement; the digest cited there is
superseded and is retained only as history (R9), not as the landed state. Re-measured on the
final bytes:

```
$ sha256sum corpus/knowledge/vendor-third-party-finding-coordination.md
1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb  corpus/knowledge/vendor-third-party-finding-coordination.md
$ wc -l -c corpus/knowledge/vendor-third-party-finding-coordination.md
  160 11501 corpus/knowledge/vendor-third-party-finding-coordination.md
```
(was 146 lines / 10359 B / `bf40fd9e…` at my §1 read — superseded draft.)

Corrected section pointers into the final entry: `## What this adds beyond F06 and F10` is
**L61** (not L60), and `## Honest limit` is **L104** (not L88). Re-read both on the final
bytes: the S039/S040 route-out contrast (L63-L73) and the limit sentence "It does not state
the coordination agreements, a timeline, a reporting address or a per-vendor process"
(L104-L105) are unchanged in substance, so the appended `next` cell needs no change. The
revised entry adds an F11 paragraph plus a four-term negative sweep; neither contradicts the
README text.

Re-run on the final bytes (read-only):

```
$ python3 corpus/instruments/frontier-recheck-count.py 2>&1 | tail -3
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
entries=18 pass=18 exit=0
```

README state unchanged by the revision: frontier count 15, `git diff --numstat` 25/0.

## 8. Files changed

- `corpus/README.md` — append only, 291 → 316 lines, sha256 `df04b049…` → `d9865b2e…`.
- `.ufo/waves/round-31/wave1/ScribeReadmeF15.md` — this receipt.

## 9. Scope, limits, blockers

- Only `corpus/README.md` and this receipt were written; `corpus/SOURCES.md`,
  `knowledge-expected.txt`, `PROVINCE.md`, `SKILL.md`, `QUALITY.md`, `LOG.md`,
  `SCORECARD.md`, the entry, the instruments, the captures and `claims.json` were not touched.
- The appended rows name another seat's deliverables (the F15 entry, S048 registry row,
  round-31 capture/manifest). The entry was revised by its owner mid-wave (see §7); the
  README text was re-checked against the final bytes and needed no change. If any of those
  paths changes again, the C2 counter commands — not this README — are the gate.
- The `next` cell is derived from the entry's own `## Honest limit` and its `## What this
  adds beyond F06 and F10` contrast rows; it asserts nothing the capture does not carry.
- No blocker; `BLOCKED:` not used.
