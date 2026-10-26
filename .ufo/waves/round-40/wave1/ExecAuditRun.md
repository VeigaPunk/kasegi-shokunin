# ExecAuditRun — receipt

Seat: ExecAuditRun (leaf executor, round 40 wave 1). Item: run `python3 corpus/instruments/recheck-audit.py --quiet` on the
current lane tree; record `strict pass=...`, `expect=present expected=... missing=... unexpected=...` and the exit; reconcile
the expected count against `ExecHarnessUpdate.knowledge-expected.txt` after integration, reporting the current mismatch if the
entries were not yet integrated.

Deliverable: `.ufo/waves/round-40/wave1/ExecAuditRun.txt` — 71 lines, 5416 bytes, sha256
`b39c8d1fe3aaf5a9ad0b827b93136798795c076c1e74a03a3611498717b8f26c`.

Lane writes: only the two wave1 files named in this seat spec. No mutating git/jj command was run anywhere; the only git
invocations were `rev-parse`, `status --porcelain`, `ls-tree` and `archive` (read-only). The fleet root, sibling lanes,
`/home/vgpnk/Projects/shokuknow`, `.ufo/state/`, `corpus/` and the operator config were not touched. Nothing was installed
(no tool was needed), so the tooling/channel record is "none".

---

## 1. Primary run — lane tree, exact output (the seat's counting command)

Command and environment were recorded by the same shell invocation that produced the bytes:

```
run-utc-begin: 2026-10-26T21:17:20Z
cmd: python3 corpus/instruments/recheck-audit.py --quiet
cwd: /home/vgpnk/Projects/shokunin/kasegi-shokunin
head: 5e985b74075dd3813a63d7750966bf8abf693465
corpus-status-porcelain: ''
knowledge-files: 51
expected-file: lines=53 entries=51 sha256=71282ee8a717212b90cde1b350817547169ca9f0d478938ae4aa95347e097a62
instrument-sha256: 5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
--- stdout ---
strict pass=51/51 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=27 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=51 total=51 pass=51 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=51 missing=0 unexpected=0 exit=0
--- exit=0 ---
run-utc-end: 2026-10-26T21:17:24Z
```

An independent invocation at 21:15Z printed the same four lines and exit 0. `--json` facts from the same tree:

```
instrument_sha256 5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
root /home/vgpnk/Projects/shokunin/kasegi-shokunin | cdroot <same> | foreign /
lines 51 total 51 complete True
pass 51 pass_strict 51 fail_closed 24 gated 24 broken 0
strict_failing_limbs {'parse': 0, 'cwd': 0, 'paths': 0, 'cdroot': 0, 'instrument': 0, 'own': 0}
expect present expected_entries 51 missing [] unexpected []
entries sorted-equal to expected file: True
```

Counter integrity: `python3 corpus/instruments/recheck-audit.py --selftest` exits 0 on the same tree; its tree-level cases
print `selftest expect-missing exit=1 want=1 missing=['corpus/knowledge/ghost-absent.md'] … ok`,
`selftest expect-unexpected exit=1 want=1 … unexpected=['corpus/knowledge/extra.md'] ok`, `selftest complete-empty … ok`,
`selftest complete-missing-line exit=1 want=1 lines=1/2 complete=False ok` — the expected-set and completeness limbs are live
in the committed instrument (sha256 above), not only in my reading of it.

## 2. Expected-number reconciliation — the delivered list (measured after it landed)

`ExecHarnessUpdate.knowledge-expected.txt` landed at 2026-10-26T21:28:11Z: 61 lines, 2 comments + **59 entries**, sha256
`328041466810f72e7900669e811d36d0434991503e57bec4f1817921b31714a2`. Diff against the committed 51-entry list: exactly eight
added names (and nothing else), the same eight slugs the wave delivered:

```
> corpus/knowledge/anthropic-cvd-provenance-and-pacing.md
> corpus/knowledge/cisa-bod-20-01-vdp-minimums.md
> corpus/knowledge/cisa-cvd-program-stages.md
> corpus/knowledge/cve-bench-agent-exploitation-benchmark.md
> corpus/knowledge/cyclonedx-analysis-subtree.md
> corpus/knowledge/doj-vdp-framework-scope-and-authorization.md
> corpus/knowledge/nist-sp800-216-vdp-framework.md
> corpus/knowledge/pz-reporting-transparency-trial.md
```

So the delivered list is `51 + N` with `N = 8`, i.e. the arithmetic the seat had to pin, and its names match the delivered
entry files (`ScribeEntriesG1.*` 3, `ScribeEntriesG2.*` 4, `ScribeF23.entry.md` 1).

**Current mismatch, stated precisely:** against the lane tree as it stands (51 entries, nothing integrated) the audit is green
and the mismatch is 0; against the delivered 59-name list the tree is short by the eight entries the L1 has not integrated yet
— a landing-order state, not a defect, and exactly the state the next section measures.

## 3. Post-integration state — measured on a scratch mirror (lane untouched)

Method: `git -C <lane> archive 5e985b74… | tar -x -C $S/mirror` (51 knowledge files, 51 expected entries), then
(a) install the eight delivered entry files under the delivered list's own names, (b) assemble
`corpus/source-snapshots/round-40/manifest.json` from the scouts' delivered `Scout*.capture.txt` +
`Scout*.manifest-record.json` pairs (S016, S017, S019, S020, S021, S023, S025, S060 — eight captures), (c) run the committed
audit with `--cdroot <lane>` so the `cdroot` limb is scored against the real lane root.

```
captures assembled: 8  entries installed: 8  tree files: 59  expected entries: 59
--- audit ---
strict pass=59/59 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=27 gated=32 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=59 total=59 pass=59 fail-closed=32 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=59 missing=0 unexpected=0 exit=0
EXIT=0
```

With the committed list extended to 59 names by the same eight (the sim's own construction) the output is identical, and with
the **harness-delivered** list copied in verbatim (`ExecHarnessUpdate.knowledge-expected.txt`) it is identical again:

```
harness expected entries=59  tree files=59
strict pass=59/59 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=59 total=59 pass=59 fail-closed=32 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=59 missing=0 unexpected=0 exit=0
EXIT=0
(missing/unexpected lines: none)
```

One of the new entries' own recheck commands, run against the assembled manifest (spot check of the `sourced` form; the full
per-row sweep is ExecRecheckAll's seat):

```
S060:sha256 OK
S060:Q1 OK occurrences=1 anchor=7-ok
S060:Q2 OK occurrences=1 anchor=15-ok
S060:Q3 OK occurrences=1 anchor=50-ok
SRC_EXIT=0
```

Scope caveat: the mirror uses the scouts' delivered capture bytes and the delivered entry files wrapped in the r38 manifest
shape; it measures the audit counter, not the manifest assembly seat's or source-recheck seat's correctness. It does show
there is no per-entry limb red in the delivered set once the captures and manifest are in place.

## 4. Two integration-order states that are red (each measured; both are ordering, not defects)

a. Delivered list committed before the entries — mirror with 51 + G1's three + F23 (tree 55), harness list copied in:

```
harness expected entries=59  tree files=55
strict pass=55/55 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=55 total=55 pass=55 fail-closed=28 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=59 missing=4 unexpected=0 exit=1
missing=corpus/knowledge/cisa-bod-20-01-vdp-minimums.md
missing=corpus/knowledge/cisa-cvd-program-stages.md
missing=corpus/knowledge/cve-bench-agent-exploitation-benchmark.md
missing=corpus/knowledge/doj-vdp-framework-scope-and-authorization.md
```

b. Entries landed but `corpus/source-snapshots/round-40/` not landed — mirror with all eight entries (tree 59, expected 59),
snapshot dir removed:

```
tree files=59 expected=59 round-40 snapshots present=no
strict pass=51/59 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=59 total=59 pass=51 fail-closed=32 parse_fail=0 cwd_fail=0 paths_fail=8 exit=1
expect=present expected=59 missing=0 unexpected=0 exit=1
EXIT=1
FAIL lines: 8
```

So the capture slice + `manifest.json` must land in the same integration as the entries; the eight `paths` failures are exactly
the eight new entries naming that manifest. The pre-existing 51 stay green in both states.

## 5. Discrimination proof that the law is `51 + N` (scratch mirrors, N=4 and N=8, placeholder entries)

Placeholder entry files with a self-naming, cwd-independent `recheck:` line were added to copies of the freeze mirror, once
with the expected list left at 51 and once extended to 51+N:

```
===== N=4  actual=55  expected-file=51  [expected list NOT yet updated]
strict pass=55/55 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=55 total=55 pass=55 fail-closed=28 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=51 missing=0 unexpected=4 exit=1
===== N=4  [expected list updated: 55 entries]
lines=55 total=55 pass=55 fail-closed=28 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=55 missing=0 unexpected=0 exit=0
===== N=8  actual=59  expected-file=51  [expected list NOT yet updated]
lines=59 total=59 pass=59 fail-closed=32 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=51 missing=0 unexpected=8 exit=1
===== N=8  [expected list updated: 59 entries]
lines=59 total=59 pass=59 fail-closed=32 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=59 missing=0 unexpected=0 exit=0
```

(The `executes=/gated=` middle line of each run is omitted here for length; it reads `executes=27 gated=28` at N=4 and
`executes=27 gated=32` at N=8, identical in both directions.) These placeholders show the arithmetic and the mechanism; they
are not evidence about real entries — §3 is the run over the real ones.

## 6. What the parent should gate post-integration

From the lane root, after the entries, `corpus/source-snapshots/round-40/` and the new list are landed:

```
test "$(ls corpus/knowledge/*.md | wc -l)" = "$(grep -vc '^#' corpus/instruments/knowledge-expected.txt)" && echo count-equal
python3 corpus/instruments/recheck-audit.py --quiet
```

Green is `count-equal`, `strict pass=59/59 … own_fail=0`, `lines=59 total=59 pass=59 … exit=0`,
`expect=present expected=59 missing=0 unexpected=0 exit=0` (59 for the eight-entry set; `<tree count>` in general). `pass` is
a form verdict only: 32 of the 59 will be `fail-closed`/`gated` because their base (`~/Projects/bounties`) is absent, and they
still pass the form limbs.

## 7. Risks / limits

- The 59 is bound to all eight delivered entry files landing under the delivered list's names. If the L1 drops or renames an
  entry, the list must be re-derived from the tree; §4a is the measured shape of that mismatch.
- The expected-set limb compares name sets derived from the tree, so count-correct-but-name-wrong fails as `missing=k
  unexpected=k`, never silently (confirmed by the instrument's own `expect-missing`/`expect-unexpected` selftest cases).
- This seat makes no claim about C1/C2 scoring; it pins the audit counter's current output, its law (`51 + N`), and the two
  landing-order states that turn it red.

## 8. Scratch / hygiene

Scratch `/fast/scratch/hyaku/kasegi-r40/ExecAuditRun/` held the freeze mirror, the N=4/N=8 placeholder mirrors, the
landed-state mirrors, the assembled scratch manifest and all transcripts; `TMPDIR` was set to `$S` for every run. The seat's
own scratch dir is removed before yielding (sibling seats' dirs untouched). Disk guard was green before the heavy passes
(`/fast/scratch/hyaku` 26% used, ~600G free).
