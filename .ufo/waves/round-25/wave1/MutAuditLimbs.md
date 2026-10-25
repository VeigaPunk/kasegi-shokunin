# MutAuditLimbs — limb-by-limb mutation test of the C1 counter

Seat: `L1Kasegi25.MutAuditLimbs` (leaf, READ-ONLY on production).
Round 25, wave 1. Lane base revision `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`.
Instrument under test: `corpus/instruments/recheck-audit.py`,
sha256 `d07af435009a0395662b3062c33bd5e5242afd8b6902d30f34b155cd11b564d6`
(equals the frozen pin in `.ufo/waves/round-25/c1-instrument-digest.txt`).
Frozen before (`.ufo/waves/round-25/c1-before.txt`, committed):
`lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1`.

## Method

1. Base corpus export: `git archive b49948f… | tar -x -C .ufo/waves/round-25/wave1/mut-audit/base`
   (read-only git). Verified byte-identical to a fresh archive of `b49948f` after all runs:
   `diff -r --brief <fresh-archive>/corpus base/corpus` → no output, `BASE_TREE_IDENTICAL_TO_b49948f=yes`.
   Needed because sibling seats have since modified `corpus/knowledge/*.md` in the working tree.
2. Instrument copied verbatim to `mut-audit/audit-mutant.py` (hash identical to the lane file) and to
   `mut-audit/audit-pristine.py`.
3. Pristine control run **from the base root**, `--root <base>` (i.e. lane-root semantics on the base copy),
   reproduces the frozen receipt exactly — same summary line, same per-entry verdicts, exit 1:
   `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1`.
4. One mutant per limb, each an exact one-line replacement (asserted `src.count(old)==1`); `diff -u` shows
   exactly one changed line in each file.
5. Every variant run twice (first pass, then a `rerun/` pass taken while sibling edits were live in the
   working tree); identical summary lines both times → results are stable and do not depend on the dirty tree.

## Table 1 — the four assigned limb mutants (base tree, unchanged entry bytes)

| # | Mutant (one line) | Receipt summary line | exit | `pass` vs 6 | Changes frozen before? | Load-bearing? |
|---|---|---|---|---|---|---|
| a | `parse_ok` → `return True` (`audit-mutant-a.py`) | `lines=35 pass=29 fail-closed=23 parse_fail=0 cwd_fail=6 paths_fail=0 exit=1` | 1 | **29** (differs) | yes: `pass 6→29`, `parse_fail 23→0` | **YES** — flips 23 entries |
| b | cwd limb → `lane_rc == foreign_rc` only, digest comparison dropped (`audit-mutant-b.py`) | `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1` | 1 | **6** (identical) | no | **NO on this corpus** — 0 entries changed |
| c | `limbs["paths"]` → `True` (`audit-mutant-c.py`) | `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1` | 1 | **6** (identical) | no | **NO on this corpus** — 0 entries changed |
| d | summary counter → `e["pass"] or e["class"] == "fail-closed"` (`audit-mutant-d.py`) | `lines=35 pass=29 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1` | 1 | **29** (differs) | yes: `pass 6→29` | **YES for the printed value only** — no entry verdict changes |

### Evidence per mutant

**a (parse).** All 23 prose-hybrid lines flip from `011`/FAIL to `111`/PASS; the 23 flipped entries are
exactly the `class=fail-closed` set. Verbatim, `mutant-a.txt`:
`claim-anatomy-sample.md   parse,cwd,paths=111 lane=2   foreign=2   fail-closed PASS`
(pristine, same entry: `parse,cwd,paths=011 … FAIL`). The 6 remaining failures are the cwd-failing
"passing" entries — the parse-fail set and cwd-fail set are **disjoint** (23 + 6 = 29), which is why `pass`
lands on 29 and not 35. Note the mutant prints the self-contradicting pair `fail-closed PASS`: the class
label still says the base is absent while the verdict says pass.

**b (cwd digest).** On the base corpus the digest half is never exercised: every one of the 6 cwd failures
is an **exit-status** mismatch `(lane=0, foreign=2)`, and **0** entries have equal exit status with a
different digest. So dropping the digest comparison is invisible to this counter — but it is a real
predicate weakening, provable with a fixture the base tree does not contain
(`mut-audit/fixture/corpus/knowledge/pwd.md`, line `recheck: test -e corpus/knowledge/pwd.md; pwd` —
exit 0 from both cwds, different stdout):

| variant | fixture receipt | exit | per-entry |
|---|---|---|---|
| pristine | `lines=1 pass=0 … cwd_fail=1 … exit=1` | 1 | `parse,cwd,paths=101 … passing FAIL` |
| mutant b | `lines=1 pass=1 … cwd_fail=0 … exit=0` | 0 | `parse,cwd,paths=111 … passing PASS` |

**c (paths).** `paths_fail=0` before and after: all 35 base lines name a `corpus/…` path or a
`~/Projects/…` base test and every named path exists, so the limb carries no verdict on this corpus.
It is not invisible in general: the instrument's own `--selftest` kills this mutant
(`selftest cases=4 failures=1 exit=1`, ghost.md).

**d (summary counter).** Summary says `pass=29` while the receipt's own entries still sum to 6:
`json pass field: 29 | entries with pass true: 6`. Exit stays 1 because the same `passed` variable gates
`return 0 if passed == len(entries) else 1` (29 ≠ 35). So this limb inflates the headline number and the
JSON `pass` field without touching the exit code or any per-entry verdict — a receipt that contradicts itself.

## Table 2 — which mutant lets a do-nothing round claim `pass=35`?

**None of the four single-limb mutants.** The closest, (a), reaches 29. Because the parse-fail and cwd-fail
sets are disjoint, reaching 35 requires neutralising **both** limbs. A supplementary composite probe proves it:

| # | Mutant | Receipt summary line | exit | vs frozen before |
|---|---|---|---|---|
| e | `parse_ok → True` **and** `limbs["cwd"] → True` (`audit-mutant-e.py`) | `lines=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0` | **0** | `pass 6→35`, `parse_fail 23→0`, `cwd_fail 6→0`, `exit 1→0` |

On byte-for-byte unchanged base entries, mutant (e) prints exactly the C1 target `pass=35 exit=0`. Its
per-entry lines still betray it (`ai-assisted-finding-validation.md … lane=0 foreign=2 passing PASS` — a
foreign exit of 2 while claiming PASS), but the counter contract consumes the summary line, and the summary
line is the target. **The only thing that makes this attack detectable is the frozen instrument digest**
(`c1-instrument-digest.txt`, `d07af…`): the claim is safe only while the counter's bytes are pinned and
re-hashed. An unpinned counter is a do-nothing round away from claiming its own target.

## Findings

1. **The `parse` limb is the load-bearing limb of C1.** It alone owns 23 of the 35 verdicts; without it the
   counter reports `pass=29` on unchanged bytes. This is also the limb whose honest result (23) is the actual
   subject of the claim.
2. **The cwd limb's digest half is not exercised by this corpus.** All 6 cwd failures are exit-status
   mismatches. Removing the digest comparison changes nothing here, yet it converts a 101/FAIL line into
   111/PASS whenever a command's output varies with cwd at equal exit status (fixture above). The counter has
   no coverage of its own digest guard; a round could satisfy limb (b) on exit status alone and never know.
3. **The `paths` limb is not exercised by this corpus** (`paths_fail=0`, all 35 named, none missing). It is
   dead weight on the base tree but is guarded by `--selftest` (ghost.md).
4. **The summary pass counter is load-bearing only for the headline**, and mutant (d) makes the receipt
   self-contradictory (summary 29, entries 6) while the exit code remains honest. Any consumer that trusts
   `summary["pass"]` over `entries[*]["pass"]` is misled.
5. **The built-in selftest does not kill the most dangerous mutant.** `--selftest` results:
   pristine `cases=4 failures=0 exit=0`; (a) `cases=4 failures=0 exit=0`; (b) `cases=4 failures=0 exit=0`;
   (c) `cases=4 failures=1 exit=1`; (d) `cases=4 failures=0 exit=0`; (e) `cases=4 failures=1 exit=1`.
   Mutant (a) — the one that turns 23 prose hybrids into PASS — sails through the selftest. The selftest
   covers the paths limb and a composite cwd/parse breach, not the parse limb alone.
6. **Surviving mutants are coverage findings, not licence to change the frozen predicate.** C1's kill rule
   stays as written; the actionable reading is that the counter's safety rests on the instrument digest pin,
   and that limbs (b) and (c) currently contribute no discriminating power on the base corpus.

## Reproduction (from `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)

```
W=.ufo/waves/round-25/wave1/mut-audit
mkdir -p $W/base && git archive b49948f1164ef65106b2c4cbee3f53e8a44b8c41 | tar -x -C $W/base
(cd $W/base && python3 ../audit-pristine.py --root "$PWD" --json ../pristine-base.json)
for m in a b c d e; do (cd $W/base && python3 ../audit-mutant-$m.py --root "$PWD" --json ../mutant-$m.json); done
(cd $W/fixture && python3 ../audit-mutant-b.py --root "$PWD" --json ../fixture-b.json)
```

## Artifacts (all under `.ufo/waves/round-25/wave1/mut-audit/`)

| file | sha256 | note |
|---|---|---|
| `audit-mutant.py` | `d07af435…b564d6` | verbatim instrument copy (= lane bytes) |
| `audit-pristine.py` | `d07af435…b564d6` | control copy, unchanged after all runs |
| `audit-mutant-a.py` | `27ede87d…c84c43` | parse limb |
| `audit-mutant-b.py` | `4412c179…a951f3` | cwd limb, digest dropped |
| `audit-mutant-c.py` | `8678ef23…f71af4` | paths limb |
| `audit-mutant-d.py` | `db01aef8…88ee5f81` | summary pass counter |
| `audit-mutant-e.py` | `2cbd2ca9…d9768d3029` | composite: parse + cwd ≡ True |
| `pristine-base.{txt,json}`, `mutant-{a..e}.{txt,json}`, `rerun/*`, `fixture*` | — | raw receipts quoted above |

## Restoration / non-mutation evidence

- Production instrument never modified: `corpus/instruments/recheck-audit.py` sha256 still
  `d07af435009a0395662b3062c33bd5e5242afd8b6902d30f34b155cd11b564d6`, git status still `??`
  (untracked, exactly as found). All mutants live only in the scratch directory.
- Frozen receipts untouched: `c1-before.json` still `3e3eeb4e39f0d6200ad521fc02fd1c970c872c9e73b5c2ec8868e66c8b2d877e`,
  `c1-instrument-digest.txt` still `a0b6544a0c22f04289c3d7842c965617f72c43ca8f099da598a10a685941277f`.
- No VCS write, no `pacman`, no network. No tool installed or upgraded this seat.
- Working-tree `corpus/knowledge/*.md` modifications observed mid-run are sibling seats' work; the base
  export was taken before them and verified identical to `b49948f` after all runs, so no verdict here reads
  the dirty tree.
