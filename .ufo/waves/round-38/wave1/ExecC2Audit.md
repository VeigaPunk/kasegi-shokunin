# ExecC2Audit — round 38 (C2 knowledge-expected sync for F21)

Item: prove the `knowledge-expected.txt` sync for the F21 entry. Read
`corpus/instruments/recheck-audit.py` and `corpus/instruments/knowledge-expected.txt`
(49 entries, C-locale sorted); in a scratch mirror add
`csaf-vex-product-status-and-justifications.md` to the expected list at its C-locale sorted
position and add a stub entry with an executable `recheck:` line; run the mirror audit →
`expected=50 missing=0 unexpected=0 exit=0`; show that NOT syncing gives `unexpected=1`.
Deliver the exact expected-list line and its line position. Receipt only.

Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only for this seat; no lane
file written). Lane head observed at work time:
`700153593eb586c70a6499c8ca225ee4d673bc9b` (`round-38: wave1 spec + validated dispatch
(73 seats, v2)`); claims base `a173b0c2…`. Instrument under test
`corpus/instruments/recheck-audit.py` sha256
`5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09` (lane and mirror copies
identical). Frozen list `corpus/instruments/knowledge-expected.txt` sha256
`92aa812447f516b88f07146591e1ee05421860cf677b283162c2d3f4ada474ce`, 51 lines = 2 comment
lines + 49 entries; `grep -v '^#' | LC_ALL=C sort -c` exits 0.
Scratch: `/fast/scratch/hyaku/kasegi-r38/ExecC2Audit` (removed before yield).
No network fetch; no tool install; no mutating git; no write outside this receipt and scratch.

## 1. What the audit's exit rule actually requires

From `recheck-audit.py` `main()` (`corpus/instruments/recheck-audit.py:264-360`):

```
complete = len(entries) == total and total > 0
expect_ok = not expect_active or (not missing_entries and not unexpected_entries)
ok = passed == len(entries) and complete and strict_passed == total and expect_ok
```

- `passed` counts the three frozen limbs (parse, cwd, paths); `strict_passed` counts all six
  (parse, cwd, paths, cdroot, instrument, own). `strict_passed == total` (all 50 files, not
  just audited ones) is a conjunct, so a stub with a broken strict limb reds the audit even
  when the expected sets match.
- The expected list is read from `<root>/corpus/instruments/knowledge-expected.txt` by
  default; `expected_mismatch()` compares it as a set against the tree's
  `corpus/knowledge/*.md`, so an extra tree entry prints `unexpected=<name>` and a listed but
  absent one prints `missing=<name>`; either flips `expect_ok` false.
- `lane_exit` is **not** a conjunct: a command that runs and fails closed on an absent base
  still counts as a form-pass. The stub below nevertheless executes green (`lane=0
  foreign=0 executes`), so that allowance is not load-bearing here.

## 2. Mirror control (untouched copy, before any change)

```
$ mkdir -p $S/mirror && cp -a <lane>/corpus $S/mirror/corpus
mirror files: 270
mirror knowledge: 49
expected entries: 49
$ TMPDIR=$S python3 $S/mirror/corpus/instruments/recheck-audit.py \
    --root $S/mirror --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin --quiet
strict pass=49/49 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=25 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=49 total=49 pass=49 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=49 missing=0 unexpected=0 exit=0
baseline_rc=0
```

Green control, so every later difference is attributable to the two scratch edits.

## 3. Stub entry added, expected list NOT synced → `unexpected=1`

Stub written only in the mirror at
`corpus/knowledge/csaf-vex-product-status-and-justifications.md`:

```
# CSAF VEX Product Status and Justifications
source: S055 — https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html
verified-at: 2026-10-26
recheck: python3 $S/mirror/corpus/instruments/anchorcheck.py $S/mirror/corpus/knowledge/csaf-vex-product-status-and-justifications.md

## Rule
Scratch stand-in used by the ExecC2Audit knowledge-expected sync proof; it carries the same recheck-line shape (cd-independent instrument + own entry file) as the landed corpus entries.
```

The `recheck:` line is executable and cwd-independent by construction (absolute path for both
the instrument and the entry), which satisfies all six limbs: instrument names an existing
`corpus/instruments/anchorcheck.py`, own names the entry's own file, no leading `cd`, both cwds
byte-identical.

```
$ (cd <lane> && python3 $S/mirror/corpus/instruments/anchorcheck.py \
     $S/mirror/corpus/knowledge/csaf-vex-product-status-and-justifications.md)
== .../csaf-vex-product-status-and-justifications.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
anchorcheck_rc=0

$ TMPDIR=$S python3 $S/mirror/corpus/instruments/recheck-audit.py \
    --root $S/mirror --cdroot <lane>
csaf-vex-product-status-and-justifications.md              frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
unexpected=corpus/knowledge/csaf-vex-product-status-and-justifications.md
strict pass=50/50 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=50 total=50 pass=50 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=49 missing=0 unexpected=1 exit=1
unsynced_rc=1
```

The stub itself passes (`strict=111111 executes PASS`) and the audit still reds: the only
failure is the unsynced expected list naming one file fewer than the tree.

## 4. Expected list synced at its C-locale position → `expected=50 … exit=0`

Insertion done programmatically over the header/entries split, then verified with
`LC_ALL=C sort -c`:

```
inserted_at_resulting_line=16 entries=50 total_lines=52
$ grep -v '^#' $S/mirror/corpus/instruments/knowledge-expected.txt | LC_ALL=C sort -c
entries_sorted_C=0

$ TMPDIR=$S python3 $S/mirror/corpus/instruments/recheck-audit.py \
    --root $S/mirror --cdroot <lane>
csaf-vex-product-status-and-justifications.md              frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
strict pass=50/50 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=50 total=50 pass=50 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=50 missing=0 unexpected=0 exit=0
synced_rc=0
```

## 5. Position proof

C-locale order puts `csaf-…` after `cra-manufacturer-reporting-duties.md` (`r` < `s`) and
before `cvss-v4-severity-and-vector.md` (`s` < `v`). Neighbourhood of the synced list
(`sed -n '14,17p'` numbered 1-4; `grep -n` absolute):

```
14  corpus/knowledge/coordinated-disclosure-timelines.md
15  corpus/knowledge/cra-manufacturer-reporting-duties.md
16  corpus/knowledge/csaf-vex-product-status-and-justifications.md
17  corpus/knowledge/cvss-v4-severity-and-vector.md

15:corpus/knowledge/cra-manufacturer-reporting-duties.md
16:corpus/knowledge/csaf-vex-product-status-and-justifications.md
17:corpus/knowledge/cvss-v4-severity-and-vector.md
```

The edit is a pure one-line insertion relative to the lane file (`diff -u lane mirror`):

```
@@ -13,6 +13,7 @@
 corpus/knowledge/considerthese-proposals-ledger.md
 corpus/knowledge/coordinated-disclosure-timelines.md
 corpus/knowledge/cra-manufacturer-reporting-duties.md
+corpus/knowledge/csaf-vex-product-status-and-justifications.md
 corpus/knowledge/cvss-v4-severity-and-vector.md
 corpus/knowledge/cwe-top25-2025-methodology.md
 corpus/knowledge/epss-exploit-prediction-scoring.md
```

Lane file today: 49 entries (line 16 is still `cvss-v4-severity-and-vector.md`), so landing
this line makes 50 entries / 52 lines and shifts `cvss-…` from line 16 to line 17.

## Costs

- Two audit runs over 50 entries: 3.5 s each (each entry's recheck line executed from its own
  recorded cwd). No long-running instrument, no network.

## Risks / scope notes

- The stub's `recheck:` body is a scratch stand-in (`anchorcheck.py` + absolute mirror paths),
  not a proposed landed line. The landed C2 entry will carry its own evidence line
  (`source-recheck.py` against the round-38 manifest for S055); the expected-list arithmetic
  proved here is independent of that body once the six limbs pass on the real entry.
- The proof is of set equality + strict form across the mirrored tree; it does not re-verify
  the 49 existing entries' evidence beyond what their own recheck lines execute (they are the
  same bytes as the lane's, audited identically).
- `L1` lands the line below; this seat wrote no lane corpus file.

## DELIVERABLE

```
corpus/knowledge/csaf-vex-product-status-and-justifications.md
```

Deliverable: 1 line (63 bytes with its trailing newline, 62 bytes without), sha256
`19e35bd2e96298f9494c778e4e2b744c415cf91601ee83b7f54fda8c61153808`. Sorted position: line
16 of the resulting 52-line file, after line 15 `corpus/knowledge/cra-manufacturer-reporting-duties.md`
and before `corpus/knowledge/cvss-v4-severity-and-vector.md` (which moves 16→17).
