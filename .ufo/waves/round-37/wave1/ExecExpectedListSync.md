# ExecExpectedListSync — round 37: knowledge-expected sync closes the audit (F20)

Seat: ExecExpectedListSync (leaf, executor). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `b56a41680cefd391868c1c370dc063c69d827e7d`, claims freeze `224df74db2a46d627ae1475a72ca48796bbd177c`).
Axis owned by this seat: coverage (C2's knowledge-expected binding). Date of all measurements: 2026-10-26.
Report path: `.ufo/waves/round-37/wave1/ExecExpectedListSync.md`.

This seat wrote only this receipt and files under `/fast/scratch/hyaku/kasegi-r37/ExecExpectedListSync/`.
The scratch directory was removed after this receipt was written. No lane file, registry row, manifest,
capture, entry or instrument was edited; nothing was written to the fleet root or any sibling tree;
no git/jj mutation was run (read-only `git archive` only); no tool was installed or upgraded.

---

## 1. What was run, in order

1. Mirror the lane corpus at the round-37 base into scratch:

```sh
S=/fast/scratch/hyaku/kasegi-r37/ExecExpectedListSync
mkdir -p "$S/export"
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive b56a41680cefd391868c1c370dc063c69d827e7d | tar -x -C "$S/export"
```

The export carries 48 `corpus/knowledge/*.md` files and a 48-entry
`corpus/instruments/knowledge-expected.txt` (50 lines: 2 `#` header lines + 48 entries).

2. Baseline audit of the untouched mirror — this is the pre-condition the sync must preserve:

```sh
cd "$S/export" && python3 corpus/instruments/recheck-audit.py \
  --root "$S/export" --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --quiet --json "$S/baseline-receipt.json"
```

```text
strict pass=48/48 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=24 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=48 total=48 pass=48 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=48 missing=0 unexpected=0 exit=0
```

exit 0. The mirror is a faithful lane copy: list and tree agree at 48 before any stubbing.

3. Place the stub F20 entry (header `source: S054`) and the round-37 manifest stub the entry's recheck
   line names (both scratch-mirror only, never committed), then append the F20 row to the mirror's
   expected list.

4. `cp -a "$S/export" "$S/export-nosync"` **before** the append, so the control mirror carries the entry
   and the manifest stub but the untouched 48-entry list.

5. Run the audit on both mirrors with identical flags. `--root` is the mirror; `--cdroot` is the real lane
   because every committed recheck line `cd`s to the lane root — this is the instrument's documented
   copy-audit mode (`--root` audits the copy, `--cdroot` supplies the lane root the lines expect).

---

## 2. Exact new expected-list line

Appended at line 40 of the committed file (C-sorted position: after
`corpus/knowledge/source-tree-loss-2026-09-28.md`, before
`corpus/knowledge/statutory-authorization-and-unauthorized-access.md`):

```text
corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md
```

Sync proof, C locale (the list's own ordering; the base list passes `LC_ALL=C sort -c`):

```text
$ grep -v '^#' export/corpus/instruments/knowledge-expected.txt | wc -l
49
$ grep -v '^#' export-nosync/corpus/instruments/knowledge-expected.txt | LC_ALL=C sort -c && echo BASE_C_SORTED
BASE_C_SORTED
$ grep -v '^#' export/corpus/instruments/knowledge-expected.txt | LC_ALL=C sort -c && echo SYNCED_C_SORTED
SYNCED_C_SORTED
$ diff <(grep -v '^#' export-nosync/corpus/instruments/knowledge-expected.txt | LC_ALL=C sort) \
       <(grep -v '^#' export/corpus/instruments/knowledge-expected.txt | LC_ALL=C sort)
37a38
> corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md
```

One line added, nothing else changed; the synced list is 49 entry lines (51 lines total with the two
`#` header lines). List sha256: synced `92aa812447f516b88f07146591e1ee05421860cf677b283162c2d3f4ada474ce`
(2514 bytes) vs control `f0d4bb0dcc12c2f3492d117a651264aa1c38638e57dd365de4655d87a46e4321` (2439 bytes) —
exactly the 75-byte row.

---

## 3. Stub F20 entry (scratch mirror only; sha256 `d8a11a4fb35c0cfcdc7ea75f6af8d053bd3cd867f4014a912acdc5aec5ca0351`, 848 bytes)

```markdown
# F20 — SSVC (Stakeholder-Specific Vulnerability Categorization), CERT/CC at Carnegie Mellon University

source: S054 — https://certcc.github.io/SSVC/ — capture corpus/source-snapshots/round-37/S054.txt
verified-at: 2026-10-26
ground: F20
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054   # stub binding against the committed S054 capture; exits 2 while the round-37 manifest is absent (fails closed), 1 on a sha256 or pinned-quote mismatch

## Stub (scratch mirror only)

ExecExpectedListSync scratch-mirror stub: it exists only to prove that the
knowledge-expected set-equality check closes the audit once the F20 entry lands.
The C2 executor's committed entry replaces this file; this one is never committed.
```

The recheck line mirrors F19/`epss-exploit-prediction-scoring.md` (same `source-recheck.py`, same
`--manifest` + `--source` pairing), so it satisfies the strict `own` limb by the documented
`--source` + `corpus/source-snapshots/` pairing, and the strict `instrument` limb by naming an existing
`corpus/instruments/*.py`. `corpus/source-snapshots/round-37/manifest.json` was stubbed in the mirror
(274 bytes) purely so the strict `paths` limb resolves the path the final committed capture will provide:

```json
{
 "schema_version": 1,
 "purpose": "ExecExpectedListSync scratch-mirror stub: stand-in for the round-37 F20/S054 manifest so the mirror's knowledge-expected set-equality check can resolve the path named by the stub entry's recheck line; never committed.",
 "sources": {}
}
```

Measured behaviour of that line in the audit: `lane_exit=2 foreign_exit=2`, class `gated`,
`frozen={'parse': True, 'cwd': True, 'paths': True}`,
`strict={'parse': True, 'cwd': True, 'paths': True, 'cdroot': True, 'instrument': True, 'own': True}`,
`pass_strict=True`. Exit 2 is the instrument's fail-closed answer while the round-37 capture/manifest is
still uncommitted at the lane head; the audit counts that as gated (form passes, base absent), which is why
the stub does not fake a green execution.

---

## 4. Transcript A — mirror WITH the sync (exit 0)

```sh
cd "$S/export" && python3 corpus/instruments/recheck-audit.py \
  --root "$S/export" --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --quiet --json "$S/synced-receipt.json"
```

```text
strict pass=49/49 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=24 gated=25 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=49 total=49 pass=49 fail-closed=25 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=49 missing=0 unexpected=0 exit=0
```

`SYNCED_EXIT=0`. Receipt fields: `lines=49 total_knowledge_files=49 complete=True pass=49 pass_strict=49
fail_closed=25 gated=25 broken=0 expect=present expected_entries=49 missing_entries=[] unexpected_entries=[]
strict_failing_limbs={'parse':0,'cwd':0,'paths':0,'cdroot':0,'instrument':0,'own':0}
instrument_sha256=5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09`.

This is exactly the required shape: `strict pass=49/49`, `expect=present expected=49 missing=0 unexpected=0
exit=0`.

---

## 5. Transcript B — same mirror WITH the entry but WITHOUT the sync (exit 1)

```sh
cd "$S/export-nosync" && python3 corpus/instruments/recheck-audit.py \
  --root "$S/export-nosync" --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --quiet --json "$S/nosync-receipt.json"
```

```text
strict pass=49/49 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=24 gated=25 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=49 total=49 pass=49 fail-closed=25 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=48 missing=0 unexpected=1 exit=1
```

`NOSYNC_EXIT=1`. Receipt fields: `expected_entries=48 missing_entries=[]
unexpected_entries=['corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md']`.

The control differs from Transcript A in exactly one thing: the missing list row. Every per-entry limb is
still 49/49 strict (`pass_strict=49 fail_closed=25` in both runs), and the only red is the expected-list
set-equality — so the red is caused by the unsynced list, not by the stub entry. That is the load-bearing
proof: an F20 entry landing without its expected row fails the audit with `unexpected=1 exit=1`, naming the
offending file.

---

## 6. Result table

| run | knowledge files | expected rows | strict | missing | unexpected | exit |
|---|---|---|---|---|---|---|
| pristine base mirror | 48 | 48 | 48/48 | 0 | 0 | 0 |
| base mirror + F20 entry + synced list | 49 | 49 | 49/49 | 0 | 0 | 0 |
| base mirror + F20 entry, list untouched | 49 | 48 | 49/49 | 0 | 1 | 1 |

Conclusion: the knowledge-expected append is both necessary and sufficient for the audit to stay green when
the F20 entry lands. The C2 claim's `knowledge-expected.txt synced (audit expected=49 unexpected=0)` is
reproduced end-to-end on a `git archive` mirror of the round-37 base, and the counter-control shows the
audit reds without it.

Scope note for the parent: this seat proves the *sync closes the audit* on the base mirror. The final
committed state must still (a) keep `knowledge-expected.txt` C-sorted, (b) carry the real C2 entry whose
recheck line resolves against the committed round-37 capture, and (c) re-run the audit on the final lane
head — the r37-closure E-series owns that final-head gate, not this receipt.
