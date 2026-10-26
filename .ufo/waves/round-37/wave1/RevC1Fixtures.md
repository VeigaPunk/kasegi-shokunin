# RevC1Fixtures — fixture-design requirements + forgery attempts for E1-E14

Round 37, claim C1 (`depth:verifiability`), seat RevC1Fixtures-2 (leaf reviewer; no subagents).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only receipt + scratch written).
Lane HEAD at review time: `b362068195d5489aa94b31e6ec8f880c367e0ba0` (round-37 wave in flight; the r37 suite is **not yet committed** — `c1-controls/before.txt` records `suite_missing=1`).
Reference implementation: `corpus/instruments/r36-closure.sh`, sha256 `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4`, 894 lines (verified by `sha256sum` this session; matches the digest pinned in `wave1/ExecC1BaseFail.md`).

**Deliverable: per-check fixture-design requirements for E1-E14 (minimal must-reject fixture + the single clause each isolates, per QUALITY R13/R17), plus forgery attempts against naive versions of each check with a caught/not-caught conclusion.**

## 0. Method and evidence base

- Clause lists are taken from the frozen C1 predicate (`.ufo/waves/round-37/claims.json`), the builder spec (`.ufo/waves/round-37/wave1-spec.json`, items `ExecC1SuiteBuild`/`ExecC1Fixtures`), and the round-36 spot-check §5 D1-D6 (`corpus/lessons/round-36-verifier-spotcheck.md`). For E1-E9 the claim says "keep the round-36 semantics", so the committed r36 implementation is the reference for the exact mechanics; line refs below are to `r36-closure.sh`.
- **Empirical:** I ran the *real* r36 check functions (`e1_final_hashes`, `e1_has_round36`, `e3_registry_rows`, `check_e1`…`check_e8`, `check_e9`) against 40+ minimal fixtures in scratch (`battery.sh`, `e9probe.sh`), with `LANE` overridden to verified-toplevel fixture repos for the git limbs. Every "measured" line below is quoted verbatim from those runs. E10-E14 have no committed implementation yet; for those the conclusions are design-level, with the naive-forgery mechanics demonstrated by grep one-liners where stated.
- Fixture repos were created only as `mktemp -d "$S/…"` dirs under my scratch with `git rev-parse --show-toplevel` verified equal to the dir before any `git init/add/commit/checkout` ran inside them. No lane/fleet/sibling/source-tree file was edited; no mutating git ran outside those fixtures.

## 1. Per-check requirements

Convention: **MR-n** = minimal fixture that must be REJECTED (check red); the bracketed clause is the one it isolates. "Naive" = the weakest plausible implementation of the check (whole-file substring greps, count-only, presence-only).

### E1 — structural placeholder/hash binding (r36 :254-279, :304-330)

Clauses: (1a) 0 `filled by the L1` lines in SCORECARD.md; (1b) 0 `<LANE_HASH>` lines; (1c) a Round-37 heading exists; (1d) ≥1 40-hex token on a `Final lane commit:` line (that line or the four after it) inside the span from the **last Round-37 heading to EOF**; (1e) every such hash exists as a commit (`cat-file -e h^{commit}`) and is an ancestor of the exported ref (`merge-base --is-ancestor`). Note the r36 code assembles both placeholder literals (`"filled by the $(printf 'L1')"`, `"<LANE$(printf '_HASH')>"`) so the suite's own bytes never contain the hunted tokens — the r37 suite must preserve that trick, otherwise the suite itself carries the placeholder strings it hunts.

Must-reject fixtures (all measured against the real `check_e1` with a scratch lane repo; main=HEAD B, side=C):

| MR | fixture (SCORECARD.md) | isolates | measured |
|---|---|---|---|
| MR-1e-i | `Final lane commit: <side-branch hash>` | 1e ancestry | `E1.t2 … round36-final-lane-commits=1,bound=0` rc=1 RED |
| MR-1e-ii | `Final lane commit: deadbeef…(40 hex, nonexistent)` | 1e existence | `E1.t3 … bound=0` rc=1 RED |
| MR-1e-iii | `Final lane commit: <ancestor> and <side-branch>` | 1e all-bound | `E1.t4 … commits=2,bound=1` rc=1 RED |
| MR-1c | no Round heading at all | 1c section | `E1.t5 … round36-section=0` rc=1 RED |
| MR-1d | `Final lane commit: (filled by the closing commit)` | 1d has-a-hash | `E1.t6 … commits=0` rc=1 RED |
| MR-1b | `Final lane commit: <LANE_HASH>` | 1b + 1d | text probe a4: `hashes=[] has_r36=1` → total=0, lh=1 RED |
| MR-1a | one prose line `filled by the L1`, rest valid | 1a | (grep limb; trivially red) |

Forgery attempts vs naive:
- *Naive existence-only binding* (skip `merge-base`): a side-branch commit exists → passes naive; **caught** by the ancestry limb (MR-1e-i, measured).
- *Naive any-40-hex-near-"final"*: a fabricated 40-hex that is not a commit object → `cat-file -e h^{commit}` fails → **caught** (MR-1e-ii).
- *64-hex digest smuggling*: a `suite-sha256=<64hex>` line adjacent to a Final lane commit line — the split-on-non-hex parse never yields a 40-hex field from a 64-hex run; measured a3: `hashes=[cccc…]` only, digest ignored → **caught**.
- *Prose placeholder* ("the L1 fills this line in"): **NOT caught** — documented r36 limit ("E1 matches the two placeholder spellings … checker-brittleness item"), carried over; the fixture set must record this as an accepted limit, not fix it silently.
- *Scope-constant hazard* (finding F-1): the r36 helper scopes to `Round[- ]?36`. Measured a1 (a file with ONLY a Round-37 section): `hashes=[] has_r36=0`; a2 (Round-36 then Round-37 sections): **both** hashes collected (the scan runs from the last Round-36 heading to EOF). So a copy-pasted 36-scope is *accidentally* adequate on the real append-only SCORECARD (the Round-37 Final line sits after the Round-36 heading and is still EOF-scanned), but it is wrong by design and its selftest cannot distinguish scope. **Required fixture:** the scope mutant — a tree whose Round-36 section carries the valid ancestor hash and whose Round-37 section carries **no** Final lane commit line must be RED. Under 36-scope it is GREEN (total=1, bound — false green: the round-37 binding is never checked); under 37-scope it is RED (total=0). The r37 suite must scope `Round[- ]?37`, rename payload fields (`round37-section`, `round37-final-lane-commits`), and include this mutant in its selftest.

### E2 — round-34 depth:density erratum (r36 :332-352)

Clauses (implementation, three limbs): (2a) marker `Erratum (round 35)` ≥1; (2b) erratum **row** regex `^\|\s*depth:density\s*\|\s*9\s*\|\s*mean \*\*201\.2\*\*` ≥1; (2c) mean `201.2` ≥1. (The frozen-claim summary compresses this to "anchor + mean"; the implementation is the reference — see F-8.)

Must-reject fixtures (measured):

| MR | fixture | isolates | measured |
|---|---|---|---|
| MR-2c | stray prose `201.2`, no marker/row | 2a+2b vs naive mean-grep | `E2.s2 … marker=0,row=0,mean=1` rc=1 RED |
| MR-2b | marker + mean, no row | 2b row-anchor | `E2.s3 … row=0` rc=1 RED |
| MR-2a | row + mean, no marker | 2a | `E2.s4 … marker=0` rc=1 RED |
| green control | marker + row + mean | — | `E2.s1 … marker=1,row=1,mean=2` rc=0 GREEN |

Forgery vs naive: naive `grep -c 201.2` (even ignoring that `.` is a regex any-char) passes MR-2c's stray-mean file → **caught** by the marker+row limbs (measured). A prose sentence quoting the row text passes a naive marker-or-mean grep → **caught** by 2b's row-anchored regex. Conclusion: the described semantics catch all three forgeries; the fixture set above is exactly the three-limb isolation R13 asks for.

### E3 — registry exact-basename rows (r36 :284-292, :354-368)

Clauses: (3a) ≥1 table row whose **first cell is exactly** `r35-defect-closure.sh` (optional backticks) inside a `## …Gates & probes registry…` section; (3b) same for `r36-closure.sh`.

Must-reject fixtures (measured):

| MR | fixture | isolates | measured |
|---|---|---|---|
| MR-3-exact | registry row `r-defect-closure.sh` only + prose mentions of both names | exact-basename (M36-3 class) | `E3.b r35rows=0 r36rows=0` RED |
| MR-3-cell | row with the name in the **second** cell | first-cell anchor | `E3.c … =0` RED |
| MR-3-scope | prose mention outside any registry section | section scoping | `E3.d … =0` RED |
| green control | both exact rows in-section | — | `E3.a r35rows=1 r36rows=1` GREEN |

Forgery vs naive: naive `grep -cF 'r36-closure.sh' SKILL.md` ≥1 is satisfied by MR-3-exact's prose mention and by MR-3-scope → **caught** by the described semantics (measured 0 in both). Conclusion: caught. Isolation note: E3 counts a row whose type cell is the defective `gate\|probe` as a row (green control a used exactly that cell) — E3 = row *existence*, E13 = row *content*; the two checks are properly disjoint and each needs its own fixtures.

### E4 — round-35 wave1-results.json tracked + provenance (r36 :370-386)

Clauses: (4a) `ls-tree -r --name-only <ref> -- .ufo/waves/round-35/wave1-results.json` == 1; (4b) frozen `git ls-files` index limb == 1; (4c) `<path>.provenance.md` exists in the export **and is non-empty** (`-f && -s`).

Must-reject fixtures (measured, scratch lane repo):

| MR | fixture | isolates | measured |
|---|---|---|---|
| MR-4c-i | json present, provenance note absent | 4c existence | `E4.t2 … provenance-note=0` rc=1 RED |
| MR-4c-ii | provenance note present but **0 bytes** | 4c non-empty | `E4.t3 … provenance-note=0` rc=1 RED |
| MR-4b | json committed at ref, then `git rm --cached` (index lacks it) | 4b frozen-index limb | `E4.t4 … tracked-index=0` rc=1 RED |
| green control | both files, note non-empty | — | `E4.t1 … 1,1,1` rc=0 GREEN |

Forgery vs naive: naive "file exists in the export" passes MR-4b (the export/ref still has the json) → **caught** by the frozen index limb (measured). This is the clause that stops a historical-ref export from reading as tracked after the file was dropped from the lane index. Note: the implementation is *stronger* than the claim wording ("provenance note … exists") — the `-s` non-empty limb is fail-closed in the right direction; keep it and pin it with MR-4c-ii. Accepted limit: the note's *content* is unvalidated (any non-empty bytes pass) — existence-grade by design.

### E5 — claims-erratum-d5.md present (r36 :388-398)

Clauses: (5a) `-f` regular file at `.ufo/waves/round-35/claims-erratum-d5.md` in the export; (5b) non-empty (`-s`).

Must-reject fixtures (measured): MR-5-empty (0-byte file) → `E5.t2 … =0` RED [5b]; MR-5-dir (a **directory** named `claims-erratum-d5.md`) → `E5.t3 … =0` RED [5a: `-f` rejects what `-e` would accept]; MR-5-absent → `E5.t4 … =0` RED. Forgery vs naive: naive `-e` existence passes the directory fixture → **caught** by `-f` (measured). Conclusion: caught; content remains unvalidated (accepted limit, same grade as E4's note).

### E6 — L1Integration.md correction, path derived (r36 :400-420)

Clauses: (6a) candidate path derived from the export's own `ls-tree` with suffix filter `(^|/)\.ufo/waves/round-34/wave1/L1Integration\.md$` minus `^corpus/instruments/` prefixes; (6b) exactly **1** candidate (ambiguity → red); (6c) `Correction (round 35)` ≥1 inside the derived file.

Must-reject fixtures (measured, scratch lane repo):

| MR | fixture | isolates | measured |
|---|---|---|---|
| MR-6c | receipt without the correction note | 6c | `E6.t2 … correction-round35=0` rc=1 RED |
| MR-6b | second suffix-matching copy at `docs/.ufo/waves/round-34/wave1/L1Integration.md` | 6b uniqueness | `E6.t4 path-candidates=2,correction-round35=0` rc=1 RED |
| isolation control | decoy under `corpus/instruments/x/.ufo/waves/round-34/wave1/…` | 6a exclusion clause | `E6.t3 … path=.ufo/.../L1Integration.md,correction-round35=1` rc=0 GREEN |

Forgery vs naive: naive "any file in the export contains the note" is satisfied by a decoy carrying the note while the true receipt lacks it → **caught**: the check reads only the derived path (6a+6b), so the decoy never satisfies 6c (MR-6c measured on the derived path). Naive assumed-path (hardcoded) breaks on rename → fail-closed red, acceptable. Measurement nuance worth pinning: the exclusion clause fires only for `corpus/instruments/`-**prefixed** copies (my first decoy attempt at `docs/L1Integration.md` was simply not a candidate — the suffix filter never saw it); the fixture set must contain both shapes (exclusion control + MR-6b) or the uniqueness clause is untested.

### E7 — QUALITY supersedes-R22/R23 rows (r36 :422-436)

Clauses: (7a) ≥1 table row `^\|\s*R[0-9]+\s*\|[^|]*\|\s*supersedes R22($|[^0-9])` (third column **begins** the statement, not followed by another digit); (7b) same for R23.

Must-reject fixtures (measured):

| MR | fixture | isolates | measured |
|---|---|---|---|
| MR-7-row | prose "this supersedes R22 and supersedes R23" | row anchor | `E7.t2 … 0,0` RED |
| MR-7-combined | single row `supersedes R22 and R23` | 7b two-rows clause | `E7.t3 … 1,0` RED |
| MR-7-boundary | row `supersedes R223` | non-digit guard | `E7.t4 … 0,0` RED |
| MR-7-prefix | row `see supersedes R22` | begins-anchor | `E7.t5 … 0,1` RED |
| green control | two proper rows `\| R22 \|` / `\| R23 \|` | — | `E7.t1 … 1,1` rc=0 GREEN |

Forgery vs naive: naive substring grep passes MR-7-row, MR-7-combined and MR-7-prefix → **caught** by the described row/begins semantics (all measured RED). Conclusion: caught; the fixture set is exactly the four-clause isolation.

### E8 — false-evidence-line correction in the round-36 lesson (r36 :438-… check_e8)

Clauses: (8a) `M36` rows ≥1 in `corpus/lessons/round-36.md`; (8b) the corrected instrument is **named** (`source-recheck` ≥1); (8c) the stale line `source-recheck exit 0 on committed bytes` == 0 in `corpus/lessons/round-35.md`; (8d) round-35.md **exists** (an absent file must not read as "stale line absent").

Must-reject fixtures (measured):

| MR | fixture | isolates | measured |
|---|---|---|---|
| MR-8c | M36 rows + naming, stale line still present | 8c removal | `E8.t2 … stale-line=1` RED |
| MR-8d | round-35.md deleted entirely | 8d exists-limb | `E8.t3 … round35-lesson=0` RED |
| MR-8b | M36 rows, correction unnamed | 8b naming | `E8.t4 … names-corrected-line=0` RED |
| MR-8a | no M36 rows | 8a | `E8.t5 … m36-rows=0` RED |
| green control | rows + naming + stale gone + file present | — | `E8.t1 … 1,1,0,1` rc=0 GREEN |

Forgery vs naive: naive stale-line grep with no exists-limb passes **deleting round-35.md** → **caught** by 8d (MR-8d measured — this is the documented r36 clause "an absent file does not read as stale-line absent"). Naive M36-count-only passes MR-8b (rows exist, correction unnamed) → **caught** by 8b. Conclusion: caught on all four limbs.

### E9 — quiescence, rewritten FAIL-CLOSED (r36 :448-484; D6 at :465-466; spec + claims)

Clauses: (9a) status repo IS the lane root (`rev-parse --show-toplevel` == physical path); (9b) worktree clean — **fail-closed**: a `git --no-optional-locks -C <lane> status --porcelain` read that fails must print `status-read=failed` and RED the limb, never default to 0 dirty lines (no `${porcelain:-0}`, no `2>/dev/null` on the status read); (9c) no leftover seat dirs under `/fast/scratch/hyaku/kasegi-r37` (`find -mindepth 1 -maxdepth 1 -type d`, the suite's own `--work` dir excluded by absolute path); (9d) exported ref == lane HEAD. Keep `--no-optional-locks` (a plain `git status` takes/unlinks `.git/index.lock` — a transient lane write the suite must not perform).

Must-reject fixtures:

| MR | fixture | isolates | evidence |
|---|---|---|---|
| MR-9b | repo with a **corrupt `.git/index`** (`rev-parse --git-dir` succeeds, `status --porcelain` exits 128) | 9b fail-closed clause | **measured live**: raw read `exit=128`, piped count `0`; r36 `check_e9` prints `status-dirty=0,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=present` **rc=0** — byte-identical payload to a genuinely clean repo (okrepo rc=0). The D6 false green, demonstrated. The r37 suite must RED this exact fixture with `status-read=failed`. |
| MR-9a | status repo = a subdirectory inside another repo | 9a root identity | r36 :458-462 sets `root_ok=0` → red (carried over; fixture = any nested dir) |
| MR-9c | leftover seat dir in the scratch root | 9c | `find` non-empty → red; isolation control: the suite's own `--work` dir inside the root must stay GREEN (exclusion clause) |
| MR-9d | export of a non-HEAD ref, otherwise clean | 9d staleness guard | `head-match=0` → red (r36 header documents this limb as what makes historical exports read non-quiescent) |
| pinned reading | `--scratch-root` pointing at a nonexistent dir | 9c absent-root semantics | r36 semantics: GREEN with `scratch-root=absent` in the payload (visible, not silently zero) — the fixture set must pin this reading explicitly (F-7) |

Forgery vs naive: the naive form **is** the D6 defect — measured above, the corrupt-index repo is indistinguishable from a clean repo. Conclusion: the fail-closed rewrite + MR-9b catch it behaviorally; E14 is the shape tripwire for the exact spelling (see below). Implementation note for the rewrite: capture the read's exit code, e.g. `if ! out=$(git --no-optional-locks -C "$srepo" status --porcelain 2>&1); then printf '…status-read=failed…'; return 1; fi` — `2>&1` into a variable is fine (E14 bans `2>/dev/null` on the status read, not stderr capture with exit-code checking).

### E10 — final-gates receipt (new; claims + spec; no implementation yet)

Clauses: (10a) `.ufo/waves/round-37/final-gates/all-gates.txt` exists in the export (require `-f` + `-s`, per the E4/E5 grade); (10b) a `suite-sha256=<sha>` header where **sha == sha256 of the executing suite bytes** (`suite_digest()` reads `BASH_SOURCE[0]`, r36 :146-149); (10c) the `E<n> payload=` lines — **fourteen, with the distinct id set {E1…E14}, each exactly once** (spec says "≥14", claims say "fourteen" — pin distinct-14, see F-8); (10d) a **line-anchored** `closed=14/14 exit=0`; (10e) fourteen `selftest case=` lines, distinct ids, `verdict=pass`; (10f) a line-anchored exact `cases=14 failures=0` (r36's judge greps `^selftest cases=9 failures=0$` — exact-line, :763-775).

Must-reject fixtures:

| MR | fixture | isolates | caught by |
|---|---|---|---|
| MR-10b-i | receipt-like file with payload/case lines but **no digest header** (the given example) | 10b presence | red |
| MR-10b-ii | digest header naming **other** bytes (r36 suite's digest, or the receipt's own digest) | 10b equality | red — equality against `suite_digest()` is the clause; mere presence is not enough |
| MR-10c | 15 payload lines (E1 twice, E7 absent) — count ≥14 passes naive | 10c distinct-14 | red only under distinct-id binding |
| MR-10d | `closed=14/14 exit=0` embedded mid-prose ("target: closed=14/14 exit=0") | 10d anchoring | **measured**: unanchored `grep -cF` = 1 (naive passes), anchored `grep -cE '^closed=14/14 exit=0$'` = 0 → red under anchored semantics |
| MR-10e | 14 case lines all `E1`, or any `verdict=fail` | 10e distinct+verdict | red under per-id binding (r36 judge pattern :777-796) |
| MR-10f | `selftest cases=14 failures=0` with trailing text | 10f exact-line | naive substring passes; anchored exact-line rejects |
| real fixture | the committed r36 receipt `.ufo/waves/round-36/final-gates/all-gates.txt` — carries `== selftest ==` judge lines and the two red controls but **no `suite-sha256=` header and no positive export run** (the D1 gap, verified by reading the committed bytes) | 10b | red |

Forgery conclusion: every *shape* forgery above is caught **iff** the clauses are implemented as equality (10b), distinct-ids (10c/10e) and line-anchored exacts (10d/10f). **Residual (F-4):** a fully self-consistent fabricated transcript — correct digest of the true suite bytes plus fourteen well-formed payload lines and case lines that no run ever produced — passes every described clause. The digest binds receipt↔bytes, not output↔run. Closing option: a replay-diff limb (E10 re-runs the suite over the same `--export-ref` and diffs the payload lines against the receipt; ~2× runtime), or accept + document the digest-bound limit explicitly. The r36 selftest judge (`judge_selftest_report`, :763-800) rejects summary-only/case-line forgery **of the selftest report file** but cannot authenticate the committed receipt — the same class, one level up. Ordering constraint to record: the receipt can only be finalized after the suite bytes are final (the digest is self-referential); if the L1 edits the suite after generating the receipt, E10 reds — correct fail-closed behavior, but it means the receipt must be (re)generated at the final digest before the closing commit.

### E11 — LOG.md round-37 correction of the false r36-fixtures path (new)

Clauses: (11a) LOG.md exists in the export; (11b) the **round-37 entry** is located (section scoping — LOG entry headings vary across the file: `## Round 36 — 2026-10-26 — …` at LOG.md:1661; pin the round-37 heading pattern the suite accepts); (11c) a **named correction**: the false path token (`corpus/instruments/r36-fixtures` or `r36-fixtures`) AND a correction cue, co-located inside the round-37 entry.

Must-reject fixtures:

| MR | fixture | isolates | evidence |
|---|---|---|---|
| MR-11b | **the base LOG.md itself** — the round-36 C1 bullet at LOG.md:1665 carries the false claim `corpus/instruments/r36-fixtures/` (verified in-tree this session) | 11b scoping | a naive whole-file token grep is **GREEN at base** (the defect text itself satisfies it — false green); section-scoped → RED. The strongest fixture in the set: the naive check's pass condition is the defect. |
| MR-11c-i | round-37 entry re-asserting the path as if it exists (token, no correction cue) | 11c cue | naive token-grep passes → caught only by the cue clause |
| MR-11c-ii | round-37 entry with a cue but not naming the path ("a path claim was corrected") | 11c token | naive cue-grep passes → caught only by the token clause |
| MR-11-fact (recommended) | export where `corpus/instruments/r36-fixtures/` **actually exists** + a correction entry | fact limb | E11-as-described (grep-only) is GREEN while the correction's premise is false → per the kill rule ("any single E-check's committed fixture proves the check can pass while its defect is present") this fixture must be made RED by adding `git ls-tree -r <ref> \| grep -c r36-fixtures` == 0 as a limb — the claims' parenthetical "(git ls-tree shows r36-fixtures absent)" implies exactly this limb |

Forgery conclusion: the described section-scoped, named-correction semantics catch the given forgeries (wrong-section mention = MR-11b; unnamed mention = MR-11c-i); the fact limb (MR-11-fact) is the one clause the grep-only description misses — require it.

### E12 — anchor-ancestor label + stale-label absence (new)

Clauses: (12a) the round-37 lesson contains the round-36 lane head `c20300df516eb5575d8db2aaad1f0cf4913e7981` **and** the token `anchor ancestor` **co-located** (same line, or E1-style line-window) — the claims bind the full 40-hex; the builder spec says prefix `c20300df` (pin full 40-hex, F-8); (12b) the same co-located label inside the round-37 **SCORECARD section** (scoped); (12c) `Final lane commit: e666d902` absent inside the round-37 SCORECARD section.

Must-reject fixtures:

| MR | fixture | isolates | evidence |
|---|---|---|---|
| MR-12a | the given forgery: lesson says "…recorded as anchor ancestor; final lane commit: e666d902…" (label present, **wrong hash**, c20300df absent) | 12a co-location | measured probe: `anchor-ancestor-lines=1 c20300df-lines=0` — a two-independent-greps naive check fails the hash grep (caught), but the subtler forgery — c20300df mentioned elsewhere in the lesson (it will be, legitimately, as the anchor) + the label elsewhere — passes both naive greps while the label is bound to nothing; **only co-location catches it** |
| MR-12c-i | stale label `Final lane commit: e666d902…` INSIDE the round-37 section | 12c | measured fixture: section-scoped count = 1 → RED |
| MR-12c-ii (anti-fixture) | the stale label ONLY in the Round-36 section — **this is the real SCORECARD today** (SCORECARD.md:1492, a legitimate historical line) | 12c scoping | **measured on the real file: naive whole-file grep = 1, round-37-section-scoped = 0** — the naive whole-file absence check is **uncloseable** (it false-reds the genuine article forever); section scoping is not a refinement, it is mandatory |
| MR-12c-iii | `Final lane commit:  e666d902…` (**two spaces**) inside the round-37 section | 12c shape | **measured**: naive substring `grep -cF 'Final lane commit: e666d902'` = 0 (evasion), whitespace-tolerant `grep -cE 'Final lane commit: +e666d902'` = 1 → the absence limb must be whitespace-tolerant or the two-space variant is a live forgery |

Scoping precision to pin (F-2): "inside the round-37 SCORECARD section" — strict section scoping (heading → next `## `) vs E1's from-last-Round-37-heading-to-EOF span. They coincide on the append-only SCORECARD (Round-37 is terminal) except for a separately-headed `## Round-37 errata` section (outside a strict section, inside a to-EOF span). The fixture set must pin the canonical reading; recommend the to-EOF span (matches E1's extraction pattern, strictly stronger, covers separately-headed errata).

Forgery conclusion: the described semantics catch all three given forgery shapes **provided** (i) the label clause is co-location-bound, (ii) the absence limb is section-scoped and whitespace-tolerant. Without those two bindings the naive versions either false-green (MR-12a subtler form, MR-12c-iii) or are uncloseable (MR-12c-ii).

### E13 — r36-closure.sh registry row completeness (new)

Clauses: (13a) locate the row by exact first-cell `r36-closure.sh` inside the Gates & probes registry section (E3's helper — reuse it); (13b) the type cell is a **single choice**: after stripping backticks and `\` escapes, the cell ∈ {gate, probe}; (13c) the row's verdict map binds exit `2` → `could-not-evaluate` (co-located in the row's cells).

Critical grounding measured this session: SKILL.md carries **both spellings** — 5 lines with unescaped `gate|probe` and 6 lines with the escaped `gate\|probe`; the actual r36-closure.sh row (SKILL.md:1111) is `| r36-closure.sh | gate\|probe | …` — the **escaped** form. A naive E13 grepping only the unescaped literal `gate|probe` finds nothing in the defect row → **false green on the very defect D5 names**. Also `could-not-evaluate` already appears in SKILL.md on exactly 1 line — the recheck-audit.py row (:981, "undeclared nonzero -> could-not-evaluate") — so a naive whole-file verdict-map grep is GREEN at base while D5 is open (measured count = 1).

Must-reject fixtures:

| MR | fixture | isolates | caught by |
|---|---|---|---|
| MR-13-real | the current :1111 row bytes (type `gate\|probe`, verdict map without exit 2) | 13b + 13c | red — the real committed fixture |
| MR-13b | type cell `gate/probe` or `gate or probe` (no literal `gate\|probe` anywhere) | 13b accepted-set | naive absence-of-literal passes → caught only by "cell ∈ {gate, probe}" |
| MR-13c-i | verdict map `1 -> could-not-evaluate` (wrong exit) | 13c binds exit 2 | red |
| MR-13c-ii | `could-not-evaluate` only in a **different** row | 13a row-scoping | naive whole-file grep passes → caught by row-scoping |
| MR-13a | fixed row placed **outside** the registry section | 13a section scoping | red (consistent with E3) |
| isolation control | r36 row fixed, another row still `gate\|probe` | row-scoping (not whole-file) | GREEN — proves E13 does not over-reach into other rows (the kill rule requires only the r36 row) |

Forgery conclusion: caught iff (13b) is an accepted-set test on the normalized cell (both spellings treated as the non-choice literal) and (13c) is row-scoped with the exit-2↔could-not-evaluate pair co-located. The naive versions false-green on the real bytes (measured).

### E14 — quiescence code fail-closed by shape (new)

Clauses: (14a) `grep -cF 'porcelain:-0'` over the suite bytes == 0; (14b) no `2>/dev/null` **on status-read lines** (line-scoped — the r36 suite legitimately uses `2>/dev/null` on other reads, e.g. :454-462; a whole-file zero-grep would false-red any suite that keeps them).

Must-reject fixtures:

| MR | fixture | isolates | caught by |
|---|---|---|---|
| MR-14-real | **the r36 suite bytes themselves** — `${porcelain:-0}` at :466 and `2>/dev/null` on the status read at :465 | 14a + 14b | red — the real committed fixture (the D6 defect, byte-exact) |
| MR-14-scope (isolation) | suite with `2>/dev/null` on other lines but not on the status read | 14b line-scoping | must be GREEN; a naive whole-file zero-grep reds it → proves line-scoping required |
| MR-14-mutant (selftest) | a copy of the suite with the defect re-inserted | 14a/14b fire | E14's own selftest mutant: the greps must reject the mutated bytes |

Forgery conclusion + residual (F-6): the shape check is **defeasible by syntax** — `porcelain=${porcelain:- 0}` (space) or a trailing `|| porcelain=0` evades both greps while staying fail-open. E14 is therefore a regression tripwire for the exact D6 spelling, not the semantics; the behavioral backstop is E9's MR-9b (corrupt-index repo must red with `status-read=failed`). The fixture set must state this division explicitly so E14 is not cited as the fail-closed proof.

## 2. Cross-cutting findings

- **F-1 (E1 scope constant).** The r37 suite must scope E1's hash extraction and section limb to `Round[- ]?37` and rename the payload fields. Killing mutant for the selftest: valid ancestor hash in the Round-36 section + no Final lane commit line in the Round-37 section → 36-scope GREEN (false), 37-scope RED. Measured mechanics: a1 (37-only file → 36-scope sees nothing), a2 (36-then-37 → both hashes collected by EOF-scan).
- **F-2 (E12 scoping + whitespace).** Whole-file absence of the stale label is uncloseable (real SCORECARD naive=1 / scoped=0, measured); section scoping mandatory; absence limb must be whitespace-tolerant (`: +e666d902`, measured evasion); pin section-vs-to-EOF reading.
- **F-3 (E11 fact limb).** The base LOG.md is the minimal must-reject fixture (the defect text at :1665 satisfies the naive whole-file grep — false green at base). Add the `ls-tree`-absence limb; without it an export containing an actually-created `r36-fixtures/` + a correction entry false-greens.
- **F-4 (E10 genuineness residual).** Shape + digest-equality clauses catch every malformed forgery (measured mechanics for anchoring; distinct-id and equality are deterministic), but a fully self-consistent fabricated transcript passes. Recommend the replay-diff limb or an explicit documented limit; also record the receipt-finalized-at-final-digest ordering constraint.
- **F-5 (E13 escaped spelling).** The defect row's type cell is the escaped `gate\|probe` (SKILL.md:1111); naive unescaped-literal checks false-green on the real defect (measured counts 5/6/1). Accepted-set semantics + row-scoping required; `could-not-evaluate` already exists on another row (:981), so whole-file verdict greps are green at base.
- **F-6 (E14 defeasibility).** Shape tripwire only; syntax variants evade it; E9's behavioral MR-9b is the semantics. Line-scoping of the `2>/dev/null` clause is required (whole-file zero-grep false-reds legitimate redirects).
- **F-7 (E9 pinned readings).** Fail-closed status read (MR-9b measured false-green under r36); keep `--no-optional-locks`; own-work-dir exclusion fixture; scratch-root-absent = GREEN with visible payload (r36 semantics — pin it, don't silently strengthen).
- **F-8 (claims ↔ spec ↔ implementation drift).** Four wordings disagree and the fixture set must pin the implementation-grade reading: E2 claims-summary "anchor `round-34 depth:density row`" vs impl marker+row+mean (cover all three limbs); E12 claims full 40-hex vs spec prefix `c20300df` (bind full 40-hex); E13 claims "exit `2` -> `could-not-evaluate`" vs spec "verdict map contains `could-not-evaluate`" (bind the pair); E10 claims "fourteen" vs spec "≥14" (pin distinct-14). The frozen claims are authoritative where they are stricter.
- **F-9 (required-red measurability).** The r37 suite is uncommitted at HEAD (`b362068`; before.txt `suite_missing=1`), so the frozen required-red runs (`--export-ref cc692008…` and `a23dc478…` → `closed<14/14 exit=1`) are not yet runnable. The r36-suite analogs were measured by `wave1/ExecC1BaseFail.md` (r36-base export `closed=4/9 exit=1`; judged head `8/9`, only live E9 open) — the r37 suite must re-derive its own reds once landed.

## 3. Verification gaps and residual risk

- E10-E14 conclusions are design-level (no committed implementation exists at review time); the naive-forgery mechanics quoted for E10/E12 are demonstrated grep one-liners, the rest are deterministic consequences of the described clauses.
- E1-E9 measurements ran the **r36** implementation as the reference for "keeps the round-36 semantics"; the r37 suite must re-demonstrate every rejection inside its own `--selftest` (`cases=14 failures=0`) on its own bytes — my results do not transfer automatically.
- E1's prose-placeholder limit and E4/E5's content-grade limits are accepted limits carried from r36's documented-limits section; E10's self-consistent-forgery residual is open unless the replay-diff limb is adopted (F-4).
- Not verified (out of my seat's scope): the actual r37 suite bytes, the required-red runs, and the C2 side.

## 4. Tooling record and cleanup

- No tools installed or upgraded (none needed; pacman untouched).
- Tools: `read`/`grep` (lane files), `bash` (read-only git: `log/rev-parse/merge-base/cat-file/ls-tree`; `sha256sum`; fixture repos inside verified-toplevel `mktemp -d` dirs under scratch; the r36 suite sourced read-only to exercise its check functions — its guard prevents `main` on source).
- Scratch `/fast/scratch/hyaku/kasegi-r37/RevC1Fixtures-2/` (battery.sh, e9probe.sh, fixture trees) removed before this receipt's yield; all measured outputs are quoted above, and every fixture's content is specified inline in §1, so the battery is reproducible from this receipt alone.
