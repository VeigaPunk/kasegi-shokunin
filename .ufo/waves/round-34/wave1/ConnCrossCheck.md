# Seat ConnCrossCheck — round 34 wave 1

Seat: ConnCrossCheck (connector, leaf). Scope: cross-check the source chains end to end
(S051 chain; round-32 and round-26 manifests) and confirm the census W04 pair is unchanged
with no new warnings. Lane write scope only; no scratch fixtures were created (every command
below is read-only against the lane), so there is no scratch tree to remove.

Measured at: 2026-10-26, working tree of /home/vgpnk/Projects/shokunin/kasegi-shokunin
(HEAD 206e510 round-34 wave-1 spec; claims freeze 29f606d; base 014ee2d).

## Report

### 1. S051 chain — all six links agree (id, URL, sha256)

| Link | Location | Measured value | Agrees |
|---|---|---|---|
| Registry row | `corpus/SOURCES.md:57` | `S051`, url `https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/`, kind docs, tier A, status `mined`, opened `2026-10-26`, recheck `90d`, used-by `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`, anchor sha256 `4fd8ed98…b325a5` | — |
| Capture file | `corpus/source-snapshots/round-34/S051.txt` | sha256 `4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5` | ✓ = registry + manifest |
| Manifest record | `corpus/source-snapshots/round-34/manifest.json` (sha256 `d5077f81…`) | id `S051`, path `S051.txt`, sha256 `4fd8ed98…b325a5`, same url, `fetched_utc 2026-10-26T05:31:10Z` (strict UTC, Z-suffix) | ✓ |
| Entry header | `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md:3` | `source: S051 — https://immunefi.com/…-v2-2/ — … in capture corpus/source-snapshots/round-34/S051.txt`; recheck line (L6) invokes `source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051` | ✓ |
| Harness | `frontier-recheck-count.py` | `PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0`; `entries=20 pass=20 exit=0` | ✓ |
| Source-recheck | run below | `S051:sha256 OK`, Q1–Q18 all OK, exit 0 | ✓ |

Commands (all run from the lane root):

```text
$ sha256sum corpus/source-snapshots/round-34/S051.txt
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
S051:sha256 OK / S051:Q1..Q18 OK (Q9 occurrences=2 anchor=77-ok; Q17 occurrences=2 anchor=96-ok; all others occurrences=1) ; exit=0
$ python3 corpus/instruments/frontier-recheck-count.py
… PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0 … entries=20 pass=20 exit=0 ; exit=0
$ grep -cE '^source: S051 ' corpus/knowledge/*.md
corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md:1   (all others 0; no other file references S051)
```

Entry bytes at measure time hash to `948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a` —
identical to the digest `RevEntryF17.md` binds its ADMIT to (948b202e…), so the reviewed bytes are
the committed bytes. Registry rows counted 51 (`grep -cE '^\|\s*S[0-9]{3,}\s*\|'` → 51), frontier
rows 17 (`grep -cE '^\| F[0-9]+ \|'` → 17).

### 2. Round-32 manifest — both records agree with files and registry

| Record | Manifest sha256 | File sha256 (measured) | Registry url | fetched_utc | source-recheck |
|---|---|---|---|---|---|
| S049 | `962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8` | `962a451a…9cb8` ✓ | `https://zc.cnvd.org.cn/news/helpList` = row S049 ✓ | `2026-10-26T04:16:06Z` strict-UTC ✓ | exit 0 (Q1–Q8) |
| S050 | `2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888` | `2f9c6406…888` ✓ | `https://security.360.cn/Reward/rules` = row S050 ✓ | `2026-10-26T04:16:16Z` strict-UTC ✓ | exit 0 (Q1–Q6) |

```text
$ sha256sum corpus/source-snapshots/round-32/S049.txt corpus/source-snapshots/round-32/S050.txt
962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8  S049.txt
2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888  S050.txt
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049 ; echo exit=$?   # exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050 ; echo exit=$?   # exit=0
```

No non-UTC `fetched_utc` anywhere in the round-32 manifest (R8 closure holds). The manifest purpose
cites capture commit `288ea9a` — verified present in `git log` ("round-32: wave-1 spec and dispatch,
S049/S050 captures"). Registry anchor cells for S049/S050 name these same capture paths.

### 3. Round-26 manifest — record and orphan both agree

| Item | Manifest sha256 | File sha256 (measured) | Registry/url | source-recheck |
|---|---|---|---|---|
| S041 (record) | `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` | `e18acbf9…ab47` ✓ | `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` = row S041 ✓; `archival: true` (pre-round-32, no fetched_utc field — declared in purpose) | exit 0 (Q1a–Q5) |
| S040-live.txt (orphan listing) | `b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c` | `b7f7b55f…286c` ✓ | orphan entry names row S040 and row_url `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` = registry row S040 url ✓; captured_url is the redirect target; `fetched_utc 2026-10-25T12:34:27Z` strict-UTC | n/a (orphan by declaration) |

R6 closure holds: S040-live.txt carries an explicit orphan listing in the round-26 manifest
(sha256 `33ac33c3…`), and the manifest purpose text accounts for both directory files.

### 4. Census — W04 pair unchanged, no new warnings

```text
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
exit=0
```

Byte-for-byte the same two W04 lines as the frozen `.ufo/waves/round-33/census-before.txt`
(S028, S029, ok line, `census_exit=0`). No new warnings. Related counters measured on the same
tree: `capture-binding-check.py` → `records=41 bound=41 unbound=0 exit=0` (the 41st record is S051;
the frozen "records=40" literal is disclosed in `.ufo/waves/round-34/claims-erratum-1.md`);
`grep -c '<LANE_HASH>' SCORECARD.md` → 0; `r-defect-closure.sh` → `closed=9/9 exit=0`;
`kill-rule-check.py` → `survivors=0 exit=0`.

### 5. Dangling links / gaps found

**G-1 (real, confirmed independently) — the junk-twin "rejection" is not executable as claimed,
and the reviewer-REFUSE record is not on disk.** C2 claims the twin at
`.ufo/waves/round-34/c2-controls/junk-f17.md` (sha256 `2752a994…4026`, measured) is "rejected by
the admission gate (source-recheck exit != 0; reviewer REFUSE)". Measured:
- the twin's own `recheck:` line is **byte-identical** to the real entry's recheck command, so
  `source-recheck.py --manifest …/round-34/manifest.json --source S051` on the twin's line exits
  **0** (same 18-OK output as the real entry). `source-recheck.py` has no entry-file argument
  (confirmed: `--entry` is rejected as an unrecognized argument), so it cannot see entry bodies.
- the twin's embedded quote "Direct theft of any user funds" **is** a substring of the real
  capture bullet at S051.txt:75 (`grep -c` → 1), so even a naive quote-grep does not reject it.
  Only the twin's full fabricated sentence is verifiably absent:
  `grep -c "defines five severity levels for smart-contract exploits" corpus/source-snapshots/round-34/S051.txt` → **0** (grep_exit=1).
- `grep -rln "junk-f17" .ufo/waves/round-34/` matches only the four receipts that *discuss* the gap
  (ScoutDatawalk F-1/F-1b, ExecHarnessAfter F-B, RevC2BeforeAfter, RevC1BeforeAfter) plus the
  freeze/spec machinery — **no reviewer issues a REFUSE verdict on the twin anywhere in round-34**.
  RevC2BeforeAfter.md:282-321 records the REFUSE record as "pending at my final measure";
  RevEntryF17.md's verdict is **ADMIT** for the real entry only (its final bytes 948b202e… match
  the current tree, verified above) and says nothing adjudicating the twin.
- the R9 closure check (`ExecRDefectClosureSuite.md:48,66`) requires only that the twin **exists**;
  `closed=9/9` does not demonstrate rejection.
Net: the chain registry↔capture↔manifest↔entry↔harness↔recheck is internally consistent, but the
"rejected junk twin" limb of C2 rests on a reviewer verdict that is not on disk and a source-recheck
form that does not discriminate. ScoutDatawalk filed this as F-1/F-1b; ExecHarnessAfter filed the
harness limb as F-B (control (c): a junk twin pointed at by an admitted row PASSES the counter,
`entries=1 pass=1 exit=0`). I confirm both measurements.

**G-2 (wording, not a broken link) — "every assertion occurrences=1" is false at tip.** The live
run prints `S051:Q9 OK occurrences=2 anchor=77-ok` and `S051:Q17 OK occurrences=2 anchor=96-ok`
(the two cross-table duplicate bullets, anchored per Q9/B2). sha256 OK and exit 0 hold; the
manifest purpose and the entry's recheck comment both disclose "occurrences=1 or anchored (Q9/Q17)".
The frozen claim's "=1" shorthand is the only divergence (ScoutDatawalk F-2; independently
reproduced here).

**G-3 (wording, minor) — `PASS F17 ids=S051` is not a contiguous literal.** The harness pads
columns (`PASS     F17  knowledge/…md ids=S051           exit=0`), so
`grep -c 'PASS F17 ids=S051'` → 0; the match needs a whitespace-tolerant pattern (ScoutDatawalk F-4a).

### 6. Verdict

Every id/URL/sha256 link in the S051, round-32, and round-26 source chains checks out end to end;
the census W04 pair (S028, S029) is unchanged with exit 0 and no new warnings; the reviewed F17
entry bytes equal the committed bytes. Two claim-wording soft spots (G-2, G-3) and one genuine
admission-gate gap (G-1: junk-twin rejection not executable via source-recheck as phrased, and no
reviewer-REFUSE receipt on disk at this measure) are reported for the L1's integration decision.
No edits made; no jj/git mutations run.

### Digests (sha256, measured 2026-10-26)

- `corpus/source-snapshots/round-34/manifest.json` d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe
- `corpus/source-snapshots/round-34/S051.txt` 4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5
- `corpus/source-snapshots/round-32/manifest.json` 72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6
- `corpus/source-snapshots/round-26/manifest.json` 33ac33c3caa6d43f3772b8cf8532b37cdb50f48db8ba667b5dd90645e8eacefa
- `corpus/SOURCES.md` 4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6
- `corpus/README.md` 876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29
- `SCORECARD.md` b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0
- `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` 948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a
- `corpus/lessons/round-33.md` f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807

Report: .ufo/waves/round-34/wave1/ConnCrossCheck.md
