# RevPredicateText — one predicate, three places (C1, C2)

Seat: read-only. No production file, lane byte, git or jj state was modified. All counters below were
re-run verbatim from the frozen strings; nothing here restates a claim I did not execute.

**Verdict:** C1 cannot currently be scored one way. Its counter-A sentence is cwd-relative, its
"committed captures" term is undefined and unchecked, its denominator ("eight") goes stale the moment
C2 succeeds, and its counter-B command is a forward reference to an instrument authored ~4 minutes
*after* the freeze whose before-state is only reachable with a flag the frozen command does not carry.
C2's counter-B is unsatisfiable against the registry numbering the lane actually uses, and the three
predicate sub-conditions it does not test (this-round registration, this-round access date, located
quote) are all observably false on the staged candidates. Detail and minimal fix per item, below.

Frozen inputs read: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/claims.json`
(`frozen_at_utc` 2026-10-25T00:00:00Z, mtime 04:09:47), spec
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/wave1-spec.json`.

---

## P1 — a reader can score the claim two ways

### 1. C1 counter B is a forward reference; its before-state needs an out-of-band flag

- Predicate: "the frozen resolve dispatch matrix scores 8/8 with exit 0" (`claims.json:15`).
- Counter: `python3 corpus/instruments/resolve-dispatch-check.py --fixtures corpus/instruments/resolve-dispatch-fixtures.json` (`claims.json:24`).
- `before_expected`: "4/8, exit 1 on frozen baseline resolver bytes (.ufo/waves/round-24/c1-baseline-resolver.py)" (`claims.json:25`).

Observed at freeze state: the checker did not exist — `ls -la corpus/instruments/` at 04:11 listed no
`resolve-dispatch-check.py`; it appears with mtime `2026-10-25 04:14` and the fixtures with `04:13:54`,
i.e. **after** `claims.json` 04:09:47. Running the frozen command against baseline bytes requires the
undocumented flag:

```
python3 corpus/instruments/resolve-dispatch-check.py --resolver .ufo/waves/round-24/c1-baseline-resolver.py --fixtures corpus/instruments/resolve-dispatch-fixtures.json
→ resolver_sha256=690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d
  cases=8 pass=4 exit=1
```

Reader A runs the frozen string at base → `python3: can't open file` exit 2, calls it "not 4/8".
Reader B runs it today → `cases=8 pass=8 exit=0`, calls it "8/8 after, and the claim's 4/8 before".
Both are "the command as written". The do-nothing control (`claims.json:28`) is likewise unmeasurable:
in the do-nothing state the script does not exist, so the control exits 2, not the asserted 4/8.

The receipts that landed at 07:14Z make the split explicit but do not close it. Both exist —
`.ufo/waves/round-24/c1-control-baseline.json` (`pass: 4`, `resolver_sha256=690153ad…`,
`resolver=…/.ufo/waves/round-24/c1-baseline-resolver.py`) and `.ufo/waves/round-24/c1-fixed.json`
(`pass: 8`, `resolver_sha256=035f8844…`, `resolver=…/corpus/instruments/resolve.py`). Neither receipt
records the CLI invocation that produced it, and the frozen string reproduces only the second: with
`--resolver` absent it always measures the default path. So one string in `claims.json` addresses two
different objects, and only the after one is addressable today.

**Minimal fix:** freeze counter B as the two-line pair with `--resolver` explicit on both
(`--resolver .ufo/waves/round-24/c1-baseline-resolver.py` for before, `--resolver corpus/instruments/resolve.py`
for after), and add `"baseline_sha256": "690153ad…"` plus `"after_sha256"` to the claim so the bytes,
not the working tree, are the object of the score.

### 2. The "frozen matrix" the claim names is not the matrix the fixtures contain

`claims.json` never enumerates the eight cases; the only frozen definition in the round is the spec's
`FROZEN matrix: exactly 8 cases`, whose **L4** is "brace where the first alternative names a dangling
symlink and the second is live" (`wave1-spec.json`, LivenessMatrix item). The landed fixtures define L4
as `bounty-brace-empty-alternative-mirror-fallback` with cite `~/Projects/bounties/{ops,}/rank.mjs:1`
(`corpus/instruments/resolve-dispatch-fixtures.json`), and the landed patch comment even cites
"cases L1/L2/L4" as empty-alternative cases (`corpus/instruments/resolve.py`, `brace_expand` comment).
The spec's L4 defect class — a *non-empty* first alternative that is a dangling symlink — is exercised
by no case; L3 covers the glob branch only.

Reader A scores "8/8 on the frozen matrix" (spec cases, one of which is absent). Reader B scores
"8/8 on the file that exists" (fixtures sha `5133e98e656f07d2454f1f4799d4b0b5e5ab260ea69b1fd9d1cade3e0f9628b6`).
Different coverage, same number.

**Minimal fix:** put the eight case ids (or `"matrix_sha256": "5133e98e…"`) in `claims.json`, and either
re-add the spec's L4 as a ninth case or amend the spec's L4 text to the bounty-mirror case in the same
commit — the claim and the plan must name the same eight strings.

### 3. C1 counter A is cwd-relative for five of eight entries

`claims.json:18` runs `bash -c "$r"` with no `cd`. Five entry recheck lines are bare relative
invocations (`corpus/knowledge/cvss-v4-severity-and-vector.md:4` … `cwe-top25-2025-methodology.md:4`);
three are self-anchored with `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …`
(`multiparty-vulnerability-coordination.md:5`, `cna-assignment-and-vulnerability-rules.md:5`,
`cra-manufacturer-reporting-duties.md:5`).

Verified divergence, same command, two cwds:

```
cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin → cvss 2, multiparty 0
cwd=/tmp (same recheck lines, absolute grep path)  → cvss 2, multiparty 0
```

After a fix that keeps `--manifest corpus/source-snapshots/…` relative, the five F01-F05 entries stay
exit 2 from any cwd but the lane root: **8/8 from the lane root, 3/8 from anywhere else**. The predicate
says each entry "runs its own `recheck:` command" (self-contained); the counter silently requires cwd=lane.

**Minimal fix:** either prepend `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ` to the five
F01-F05 recheck lines (matching F06-F08) or prepend the same `cd` to the `for` loop in `claims.json:18`;
the predicate should then say "…when run from the lane root".

### 4. "from committed captures" is undefined and untested

`claims.json:15` says "exits 0 from committed captures"; the counter (`:18`) never checks git tracking,
and the manifest the eight entries cite is `corpus/source-snapshots/round-23/manifest.json` in every case
(verified for all eight). The round's own scout plans new captures under
`corpus/source-snapshots/round-24/` (`.ufo/waves/round-24/wave1/SrcS013S015.md:87`: "one excerpt file per
source under `corpus/source-snapshots/round-24/`"), i.e. the plan's capture location contradicts the
path the recheck lines name.

Two readings, both exit 0: (a) append S001-S015 into the round-23 manifest and leave the recheck lines
alone — edits a prior round's committed capture set; (b) create `round-24/manifest.json` and rewrite
eight recheck lines. Only (b) is round-honest and only the counter cannot tell them apart. Separately,
the whole round-24 tree is currently untracked — `git status --porcelain` at tip `c2480b1` prints
`?? .ufo/waves/round-24/` and the baseline blob `690153ad…` is not in git — so nothing here is
"committed bytes" yet.

**Minimal fix:** pin the manifest path in the predicate ("each entry's `recheck:` cites
`corpus/source-snapshots/round-24/manifest.json`") and add one assertion to counter A:
`git ls-files --error-unmatch corpus/source-snapshots/round-24/manifest.json`.

The divergence is now live, not hypothetical. `.ufo/waves/round-24/capture-log.txt` records all fifteen
captures landing at `out=corpus/source-snapshots/round-24/S001.txt … S015.txt` (16 lines, `status=200`,
`utc=2026-10-25T07:15:17Z`…`07:15:23Z`), and `ls corpus/source-snapshots/round-24/` now holds
`S001-S015` plus the round-23 four. But `corpus/source-snapshots/round-24/manifest.json` does not exist,
and every one of the eight knowledge entries still cites `round-23/manifest.json`
(`grep -c 'round-23/manifest.json'` = 1 for each; `grep -rl 'round-24/manifest' corpus/knowledge/` = 0).
Counter A is therefore still 3/8 with the fix's inputs already on disk — and the reverse edit (append the
fifteen rows to the round-23 manifest, touch no recheck line) also reaches 8/8. That is the two-way score.

### 5. C1's denominator is stale the moment C2 succeeds

`claims.json:15` "every one of the eight Frontier knowledge entries"; the spec's own C1 sentence says
"every Frontier knowledge entry's `recheck:` command" (`wave1-spec.json` context). C2 adds F09 with **two**
entries, so at round end the frontier holds 9 topics / 10 entry files (`corpus/README.md:198-205` today =
8 rows, one file each). Counter A's hardcoded eight names can return 8/8 while F09's two entries never run.

**Minimal fix:** predicate: "every knowledge entry named in the frontier table of `corpus/README.md` at
round end (10 files: F01-F08 plus F09's two)"; counter: derive the file list from the table's `entry`
column instead of a literal; `after_target`: `10/10`.

### 6. C1 counter A's receipt carries no label, only an exit number

`claims.json:18` discards the rechecker's emission (`>/dev/null 2>&1`). The receipt
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/c1-counterA-before.txt` is eight
`<name> <0|2>` lines. `source-recheck.py` distinguishes `UNAVAILABLE reason=not-listed` from
`reason=missing`/`unreadable-or-invalid` — all exit 2 (`source-recheck.py`, `recheck()` and
`load_manifest()`). The claim's diagnosis "F01-F05 exit 2 not-listed" (`claims.json:19`) is therefore not
in the receipt: an unreadable manifest produces the identical receipt.

**Minimal fix:** keep the rechecker's first emitted line per source in the receipt
(`bash -c "$r" > "$out" 2>&1; echo "$f $? $(grep -m1 'UNAVAILABLE\|MISMATCH' "$out")"`), so "not-listed"
is a label, not an inference.

---

## P1 — C2

### 7. C2 counter B's `S1[0-9][0-9]` band is not the registry's numbering; target 2 is unsatisfiable as staged

`claims.json:44` `grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l`, target 2 (`:46`).
The lane's registry is sequential: `corpus/SOURCES.md` ends at `S031`; the round's own staged id list runs
`S031 … S124` contiguously (`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/assimilation/staged-ids`),
and `collisions` records `S031` — the package's first staged id already collides with the lane's existing
S031. The two candidates' source lines:

- `authorised-testing-rules-of-engagement.md:2` → `source: S123 — …` (S1xx)
- `statutory-authorization-in-three-traditions.md:3` → `source: S039 — …` (S0xx, first line; three rows)

Adopted verbatim or shifted by one for the S031 collision (S039→S040), the statutory entry's first
`source:` line is in the S0xx band → counter B = **1**, not 2. Counter B = 2 requires inventing an S1xx
id or reordering that entry's source lines — neither is "rows first registered this round".

**Minimal fix:** replace the id-band test with a membership test against the rows this round actually
appends, e.g. `grep -lE '^source: (S0[3-9][0-9]|S1[0-9][0-9]) ' ` **minus** the ids already present in
`corpus/SOURCES.md` at `d0a3f6a`; or, cleanest, one command over the diff: entries whose first `source:`
id appears in this round's appended SOURCES.md block.

### 8. "addendum 10" has no referent anywhere in the lane

`claims.json:38` requires rows "first registered this round under addendum 10". Repo-wide:

```
grep -rn 'addendum' --include='*.md' --include='*.json' --include='*.py' /home/vgpnk/Projects/shokunin/kasegi-shokunin
→ only .ufo/reports/round-21, .ufo/waves/round-23/*, .ufo/waves/round-24/claims.json, LOG.md
```

`corpus/SOURCES.md` contains no "addendum" section, no addendum numbering, and no addendum-10 block.
A reader cannot tell whether "addendum 10" is (a) a block to be created this round, (b) an existing
numbered block in the assimilation package, or (c) prose. The package side has no such number either:
`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` is headed
`corpus-expansion-1 :: staged rows for lane kasegi` with no addendum index.

**Minimal fix:** either define it this round (`## Addendum 10 — round 24` in `corpus/SOURCES.md`, with
`claims.json` citing `corpus/SOURCES.md §Addendum 10`) or delete the term and name the mechanism:
"ids appended in this round's `corpus/SOURCES.md` block, `opened: 2026-10-25`".

### 9. The three C2 sub-conditions the counters do not test are false on the staged candidates

Predicate (`:38`) requires per entry: (i) rows *first registered this round*, (ii) *re-opened by this lane
with its own access date*, (iii) a *located quote*. Counters test none of the three.

- (ii) is already violated by the candidates as staged: `verified-at: 2026-10-24`
  (`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/authorised-testing-rules-of-engagement.md:3`)
  and `verified-at: 2026-10-23` (`statutory-authorization-in-three-traditions.md:5`) — both before the
  2026-10-25 round. Their `recheck:` lines say so explicitly: "ran 2026-10-24", "ran 2026-10-23".
- (iii) is not asserted: neither file carries a `quotes:`-shaped located assertion that
  `source-recheck.py` consumes, and the manifest holds only S018/S029/S030/S031
  (`corpus/source-snapshots/round-23/manifest.json`: `S018 S029 S030 S031`).
- (i) is untestable from counter B, which matches a file count in an id band.

Reader A: 9 and 2 → claim met. Reader B: reads the admitted files, sees access dates of the previous
round and no located quote → claim not met. Same counters.

**Minimal fix:** predicate → "each entry's `verified-at` equals this round's date and its first `source:`
id is in this round's addendum block, and each cited row has a located quote in
`corpus/source-snapshots/round-24/manifest.json` that `source-recheck.py --source <id>` exits 0 on";
counter B → `grep -lE '^verified-at: 2026-10-25$' <the two entry paths>` **and** the two
`source-recheck.py --source` exit codes.

### 10. F09's label is contradicted by the entry it is supposed to admit

`claims.json:38` names the topic **F09**. The candidate it must admit carries
`ground: F12 (new frontier item; extends F03, which attributes safe harbor only to the policy granting it)`
(`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/statutory-authorization-in-three-traditions.md:7`).
Admitted verbatim, the knowledge entry self-labels F12 while `corpus/README.md` and `claims.json` say F09.

**Minimal fix:** at admission, rewrite that `ground:` line to F09 (an admission-time relabel is a
corpus edit, not a source edit); or keep F12 in both places and change `claims.json` and the README row.

### 11. C2's declared collision map does not exist

`claims.json:54` `"collision_map": ".ufo/waves/round-24/assimilation/renumber-map.tsv"` →
`cat: No such file or directory`. The directory holds only raw inputs: `census-before.txt`, `collisions`
(contents: `S031`), `reg-ids` (S001-S031), `staged-ids` (S031-S124). The S031 collision is *detected* and
*unmapped*; which staged id becomes which lane id — the thing C2 counter B depends on — is undefined.

**Minimal fix:** ship `renumber-map.tsv` with one `package_id<TAB>lane_id<TAB>row_hash` line per adopted
row and have counter B read the lane ids from it; if the map is not produced, delete the claim key so the
claim does not point at absent bytes.

### 12. C1's "every entry recheck exits 0" cannot hold for the entries C2 admits

The two candidates' `recheck:` lines are prose with markdown backticks, not commands:

- `recheck: 90d — re-fetch the PDF and \`grep -F\` the four lines (ran 2026-10-24)`
- `recheck: 730d — \`curl -sSL https://laws.e-gov.go.jp/…\` then confirm 第十一条 still reads …`

Counter A pipes the raw line into `bash -c`, so `90d`/`730d` are command names → exit 127, and the
backticks in the second become command substitution. If item 5 is fixed (denominator = the README table),
C1's target becomes unreachable at 10/10 unless the admitted entries are given executable recheck lines
first.

**Minimal fix:** make executable recheck lines a Q-gate for admission (the admitted entry must carry
`recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json --source S1xx`),
and state that gate in C2's predicate — it is the same sentence C1 scores.

---

## P2 — wording that makes a receipt unreproducible, but does not move the score today

### 13. The 24/24 containment guard is in the plan, not in the claim

The ResolverPatch item requires `mirror-containment-check.py` to stay 24/24; `claims.json`'s predicate
and counters carry no such condition, so C1 can be scored met while that matrix regressed. It has not
regressed today — re-run against the landed bytes:

```
python3 corpus/instruments/mirror-containment-check.py
→ cases=24 escape=12 controls=12 pass=24 fail=0 resolver_sha256=035f8844…
```

**Minimal fix:** add `AND python3 corpus/instruments/mirror-containment-check.py` exits 0 as a third
clause of C1's predicate.

### 14. `grep -m1` silently scores a stale recheck line

`claims.json:18` matches only the first `recheck:`. If the round-24 fix is implemented by appending an
amended `recheck:` line rather than replacing it, counter A keeps scoring the old line and 8/8 becomes
unreachable for a reason unrelated to the fix.

**Minimal fix:** assert one `recheck:` per frontier entry (`grep -c '^recheck: '` = 1) inside counter A.

### 15. The counter-B receipts no longer describe the bytes that exist

Receipts for counter B now exist (`c1-control-baseline.json`, `c1-fixed.json`,
`c1-containment-regression.json`, `capture-log.txt`), so "the label in the receipt" has a third place —
but the label is not binding. `c1-fixed.json` binds `checker_sha256` **b03a1023…** and
`matrix_sha256` 5133e98e…; the file those hashes name now hashes to a different value:

```
sha256sum corpus/instruments/resolve-dispatch-check.py → 88090efca9860a83677f7118813f0e34e945b09aaaf2dc8a584464b7b2b47b69
receipt c1-fixed.json                                 → checker_sha256=b03a102306dcbaa5c0a8c26b03bb27d324d3edef3e96e910bffd15e936f7c4a8
```

Both the checker (untracked) and the pre-drift bytes are retrievable from nowhere: the receipt names an
instrument that no longer exists in the tree or in git. Compounding it, item 17 — the resolver the
receipt's `pass: 8` was taken against is also uncommitted. A reader replaying the frozen command today
runs instrument 88090e, not the b03a10 the receipt claims, and cannot confirm the receipt came from the
instrument it cites.

**Minimal fix:** write the receipts only after the instruments are committed (or emit the instrument
source alongside), and add the argv to the receipt schema
(`"argv": [...sys.argv]`, plus `git rev-parse HEAD:<instrument path>`); a `checker_sha256` that matches no
tracked blob should be treated as an unlabelled receipt.

### 16. `checker_sha256` means two different files across the two receipt schemas

`c1-fixed.json`: `checker_sha256=b03a1023…` (resolve-dispatch-check.py) and
`runner_sha256=dddd5549…` (mirror-containment-check.py). `c1-containment-regression.json`:
`checker_sha256=dddd5549…` (mirror-containment-check.py itself; verified — `sha256sum
corpus/instruments/mirror-containment-check.py` = `dddd55496b55eb49138613e3b7143834412cdb104b7f8f6b6e85210f3dd98f8a`).
The same key names a different program in each receipt of the same round, so a reader cross-checking
"which instrument produced this matrix" can attribute the 24/24 containment matrix to the dispatch checker.

**Minimal fix:** one key, one meaning — `instrument_sha256` for the program that printed the rows and
`runner_sha256` for the imported executor in both receipts; never reuse `checker_sha256` for the runner.

### 17. The 8/8 I measured is on lane bytes the plan forbids editing

`git status --porcelain` at tip `c2480b1` reports
` M corpus/instruments/resolve.py`, ` M corpus/instruments/citation-survival.md`,
` M corpus/instruments/citation-survival.tsv`, plus `?? corpus/instruments/resolve-dispatch-check.py`
and `?? corpus/instruments/resolve-dispatch-fixtures.json`. The lane's `resolve.py` is now
`035f8844…`, not the base `690153ad…`, while both the LivenessMatrix item ("Do not change production
resolve.py") and the ResolverPatch item ("never the lane's copy") forbid exactly that. Scope ruling
belongs to the sentinel seat; the predicate consequence is that the claim's after-state is measured on
uncommitted, in-lane-modified bytes and no receipt records it.

**Minimal fix:** the after receipt must name `resolver_sha256` **and** the commit it came from
(`git rev-parse HEAD:corpus/instruments/resolve.py`), so the merged blob is the object of record.

---

## Residual risk / unverified

- **UNVERIFIED:** whether L1 commits `resolve.py`, the checker, the fixtures and the baseline blob before
  the round-level verification, and whether C1's after-target is then re-measured from those commits.
  Until that happens no C1 score can rest on "committed bytes" (`claims.json:29` kill rule).
- **UNVERIFIED:** whether F09's two entries are counted as one surface or two by the coverage score
  (`QuarterDenominator` seat owns it). If two, the frontier denominator 9 topics / 10 files interplay
  with item 5 changes C1's after-target again.
- **Not assessed:** Q1-Q6 admission quality of the two candidates — out of scope here (C2's kill rule
  routes it). I only audited whether the predicate's *text* can be scored from the counter's *condition*
  and the *receipt*.
- **UNVERIFIED:** whether the mirrored `corpus/instruments/README.md` instrument index lists the two new
  untracked instruments; a reader following the index would not find them today. Not a predicate defect,
  but it is the same discovery gap the claim is trying to close.
- `corpus/README.md:209` ("8/8 admitted at round 23") is round-dated and not itself a false claim; it
  becomes a trap only if a reader takes it as the current denominator after F09 lands.
