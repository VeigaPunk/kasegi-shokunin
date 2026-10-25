# ExecExpectedList — round-28 wave 1 (recheck-audit expected-list count basis)

Item: round-27 carry-forward 4 — reconcile the `recheck-audit.py` expected-list count basis; decide
whether regeneration after the F12 entry lands must produce N or N+1, with the instrument's own logic
quoted; produce the exact L1 command and expected before/after values. Read-only seat: **no production
file changed, the expected list was NOT regenerated.** Receipt:
`.ufo/waves/round-28/receipts/ExecExpectedList.txt`.

Lane HEAD at measurement `94f387cbee71a532a51ce075f01701a557231e85` (2026-10-25T17:24:13Z); claims-freeze
base `c9f8b115…` is an ancestor (`git merge-base --is-ancestor` exit 0). State label: **PRE-STATE** for
§1–§7 as measured at 17:23Z — `corpus/knowledge/japanese-domestic-disclosure-workflow.md` and the README
F12 row were absent; `corpus/source-snapshots/round-28/manifest.json` landed mid-item (sha256
`e62ddad1…`). **§9 records the live POST-LANDING re-measurement after the entry landed at 17:29Z and
supersedes §1 for current state.**

Instrument byte state: `corpus/instruments/recheck-audit.py` sha256
`3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` (the C1 claim's `c2a9e6c6…`
pre-change digest is `anchorcheck.py`, a different instrument). Expected list sha256 `30ba5860…`.

## 1. Live run (measured, 2026-10-25T17:23Z)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py
strict pass=39/39 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=16 gated=23 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=39 total=39 pass=39 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=39 missing=0 unexpected=0 exit=0
EXIT=0
```

`lines=` is the number of audited entries (files carrying a `recheck:` line); `total=` is
`len(glob(corpus/knowledge/*.md))`. They agree at 39 and the audit exits 0.

## 2. Count-basis reconciliation (r27 carry-forward 4)

| Probe | Value |
|---|---|
| `git ls-files 'corpus/knowledge/*.md' \| wc -l` | 39 |
| `ls corpus/knowledge/*.md \| wc -l` | 39 |
| non-`.md` files directly under `corpus/knowledge/` | none |
| `wc -l corpus/instruments/knowledge-expected.txt` | 41 |
| `grep -c '^#' …knowledge-expected.txt` | 2 |
| `grep -vc '^#' …knowledge-expected.txt` | 39 |

Reconciliation: the r27 note's “41 lines (`wc -l`)” is **39 entry lines + 2 `#` header comment lines**;
the r26 integration's “39 entries” is the entry-count basis. The two figures never disagreed — they
counted different things. Current set equality holds (`expected=39 missing=0 unexpected=0`).

## 3. Why the instrument decides the count (quoted, `corpus/instruments/recheck-audit.py`)

```python
178  def load_expected(path):
179      names = []
180      with open(path, encoding="utf-8") as handle:
181          for raw in handle:
182              line = raw.strip()
183              if line and not line.startswith("#"):
184                  names.append(line)
185      return names
```

```python
188  def expected_mismatch(root, expected):
189      actual = {
190          os.path.relpath(p, root)
191          for p in glob.glob(os.path.join(root, "corpus/knowledge/*.md"))
192      }
193      wanted = set(expected)
194      return sorted(wanted - actual), sorted(actual - wanted)
```

```python
330      total = len(glob.glob(os.path.join(root, "corpus/knowledge/*.md")))
...
350      complete = len(entries) == total and total > 0
351      expect_ok = not expect_active or (not missing_entries and not unexpected_entries)
352      ok = passed == len(entries) and complete and strict_passed == total and expect_ok
```

Consequences:
1. `load_expected` skips blanks and `#` comments → `wc -l` is **not** an entry count; 41 ⇒ 39 entries.
2. `actual` comes from the **working-tree glob**, not from `git ls-files` and not from arithmetic → every
   new `corpus/knowledge/*.md` is an `unexpected` entry until the list is regenerated.
3. `entries` (audited lines) counts only files with a `recheck:` line — `audit_entry` returns `None`
   (line 117) and `collect` drops it (line 173) — while `total` counts all `.md` files, so `lines` and
   `total` split if the F12 entry has no recheck line (`strict_passed == total` then reds).

## 4. Answer: N+1, not N

With **N = 39** (current expected-entry count = current `corpus/knowledge/*.md` count), the regenerated
list must hold **N+1 = 40 entry lines** (42 physical lines with the two `#` headers kept). It must not
stay at 39. Equivalently, with N′ = 41 (`wc -l` today, the figure the carry-forward quotes), the file
goes 41 → 42 = N′+1.

Reason: F12 lands exactly one new `corpus/knowledge/*.md`; `expected_mismatch` compares the committed
list against `glob(corpus/knowledge/*.md)`, so a stale list yields
`unexpected=corpus/knowledge/japanese-domestic-disclosure-workflow.md` and exit 1 via line 351–352.

## 5. Measured post-landing simulation (scratch copies, no lane write)

Scratch A `/tmp/r28-exp-sim-A`: copy of the live corpus + a simulated F12 entry whose recheck line is
C2-shaped (`… source-recheck.py --source S041 --source S042 --manifest corpus/source-snapshots/round-28/manifest.json`)
+ placeholder manifest; expected list left at the live 39 entries:

```
strict pass=40/40 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=16 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=40 total=40 pass=40 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=39 missing=0 unexpected=1 exit=1
unexpected=corpus/knowledge/japanese-domestic-disclosure-workflow.md
```

Scratch B `/tmp/r28-exp-sim`, same tree, list regenerated from the working-tree glob:

```
strict pass=40/40 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=40 total=40 pass=40 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=40 missing=0 unexpected=0 exit=0
EXIT=0; regenerated list wc -l = 42, entry lines = 40
```

Scratch C side-check (entry present, recheck line removed, list regenerated): `lines=39 total=40 pass=39
exit=1`, `strict pass=39/40` — regeneration cannot mask a missing recheck line.

Honesty note: a first regeneration attempt wrote absolute `/tmp/...` names and produced
`expected=40 missing=40 unexpected=40 exit=1`; list entries must be **lane-relative**, which is why the
L1 command runs from the lane root.

## 6. Exact command for the L1 after the F12 entry lands (not run by this seat)

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
{ printf '%s\n' \
    '# Expected knowledge entries for corpus/instruments/recheck-audit.py — round 28' \
    '# Sorted list from the working tree (one entry per line); keep in sync with corpus/knowledge/.'; \
  LC_ALL=C ls corpus/knowledge/*.md | LC_ALL=C sort; } \
  > corpus/instruments/knowledge-expected.txt.new && \
mv corpus/instruments/knowledge-expected.txt.new corpus/instruments/knowledge-expected.txt && \
python3 corpus/instruments/recheck-audit.py --json .ufo/waves/round-28/receipts/recheck-audit-after.json
```

Precondition: entry + round-28 manifest + both captures present; the `paths` limb resolves the entry's
manifest under the lane root, so an entry whose manifest is missing reds `paths` even with a correct list.

Expected before/after:

| Stage | `wc -l` | entry lines | knowledge files | audit summary | expect line |
|---|---|---|---|---|---|
| before (live, measured) | 41 | 39 | 39 | `lines=39 total=39 pass=39 … exit=0` | `expected=39 missing=0 unexpected=0 exit=0` |
| entry landed, list stale (scratch) | 41 | 39 | 40 | `lines=40 total=40 pass=40 … exit=1` | `expected=39 missing=0 unexpected=1 exit=1` |
| after regeneration (scratch) | 42 | 40 | 40 | `lines=40 total=40 pass=40 strict 40/40 … exit=0` | `expected=40 missing=0 unexpected=0 exit=0` |

The live `expected=40 missing=0 unexpected=0 exit=0` line is the L1's to produce; the 40-entry figures
above are scratch-measured, not a live after-value.

## 7. Risks and caveats

- The simulation proves the expected-list machinery, not ScribeEntryC2's actual recheck line. If that
  line is missing: `lines=39 total=40 … exit=1` (measured, scratch C); if it fails a strict limb the
  audit reds on that limb instead.
- `git ls-files`-based regeneration run **before** the landing commit would omit the still-untracked
  entry and write 39 (wrong). Use the working-tree listing above (the instrument's own basis), or use
  the `git ls-files 'corpus/knowledge/*.md' | LC_ALL=C sort` variant only after the entry is committed.
- The committed list is not byte-sorted (`evidence-dir.md` at line 15, `ev-model.md` at line 16; `LC_ALL=C`
  puts `ev-model.md` first). Harmless today — the comparison is set equality — and the regeneration fixes
  the order.
- The round-28 manifest was written during this item; if it is rewritten afterwards, the entry's
  `--manifest` line and the `paths` limb must be re-checked at the L1's re-run, not trusted from this
  PRE-STATE observation.

## 8. Compliance

No production edits (only this report and the receipt); no subagent, background job, VCS write, or tool
install (no pacman/uv/npx run). Expected list deliberately not regenerated. All commands ran from the
lane root with absolute paths.

## 9. Post-landing live re-measurement (2026-10-25T17:29:59Z — supersedes §1)

The F12 entry landed while this report was being written:

- `corpus/knowledge/japanese-domestic-disclosure-workflow.md` — 18544 B, sha256
  `a22d2321e39fd0e547d8ae480eb566648520e59281e69e057aab5ab8502413a6` (mtime 14:29 local).
- `corpus/knowledge/*.md` count → **40**.
- `corpus/instruments/knowledge-expected.txt` unchanged by this seat: sha256 `30ba5860…`, `wc -l` 41,
  entry lines 39.
- `corpus/instruments/anchorcheck.py` now sha256 `95333e29…` (C1 instrument finalized; observed context
  only, no bearing on this item).

Live canonical audit (committed list still stale):

```
$ python3 corpus/instruments/recheck-audit.py
unexpected=corpus/knowledge/japanese-domestic-disclosure-workflow.md
strict pass=40/40 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=40 total=40 pass=40 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=39 missing=0 unexpected=1 exit=1
```

Exit 1 — exactly the stale-list verdict §5 predicted from the scratch simulation.

Live after-probe with a 40-entry temp list (read-only; committed list untouched; temp entries verified
equal to the live glob by `diff` → empty):

```
$ python3 corpus/instruments/recheck-audit.py --expect /tmp/r28-exp-sim/corpus/instruments/knowledge-expected.txt
strict pass=40/40 cdroot_fail=0 instrument_fail=0 own_fail=0
lines=40 total=40 pass=40 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=40 missing=0 unexpected=0 exit=0
```

Exit 0 — the live after-value the L1 must reproduce against the committed file with the §6 command.
The entry's own recheck line executes with exit 0 (fail-closed stays 24, i.e. the entry counts as
executing, not gated).

Digest discrepancy flag: a peer seat reported the entry digest as `a0f8e617…`; the bytes measured here
hash to `a22d2321…`. Either the file was rewritten between probes or the peer's digest covers different
bytes — the L1 must re-hash the entry at re-run time rather than trust either figure.
