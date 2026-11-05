# RevengerInherited — round-77 attempt 1, wave w1 (reverse-engineering the round-76 failure chain)

Freeze `539a43877809bd90b6f506e8fd24a6d871598cd5` (verified: `git rev-parse 539a438^` = `2e53fc74776824898b5c5eb914aeddc19a091157`, the claimed base). Scope: read-only audit of frozen bytes; all reruns on `git archive 539a438` copies and on scratch fixtures under `/fast/scratch/hyaku/kasegi-r77/RevengerInherited/`. Nothing in the lane tree was written. Reruns are echoed in `RevengerInherited-*` files in this directory (21 files, listed at the end).

## 1. Verdict table (V-A..V-E and M76-4)

| item (r76) | r77 closing mechanism | status | evidence |
|---|---|---|---|
| **V-A / R-A / M76-3** m2b consuming-conjunct survivor; NameError not a semantic kill | C1: registered closure (`c1-amended-reference.py:264-265`), four gate checks (`:313`, `:323`, `:329`, `:334`), five named kills K-M1..K-M5 (`c1-mutant-transforms.md:12-16`) | **PARTIAL — M76-3 reopened in its consumer-side form** (see §2) | K-M1..K-M5 all exit 1 on rerun (§2.1). Consumer-side removals X1 and X2 exit **0**, `selftest cases=12 failures=0` (§2.2). |
| **V-B / R-B / M76-2** frozen Q01 below the 12-char floor | Fresh S112 manifest; R126 dry run in the freeze commit | **CLOSED** | `controls/c2-prerecheck-r77.txt` committed in `539a438` (17 lines, `S112:sha256 OK`, 13 quotes `OK occurrences=1`, `rc=0`). Re-run on the frozen archive: rc 0 (`RevengerInherited-rerun-B0-s112.txt`). Commit `539a438` committer 12:35:02Z precedes `w1.ready` 12:39:27Z and `w1.ready.dispatched` 12:39:55Z. |
| **V-C / R-C / M76-1** five non-query endpoint contracts; distinctness sweep over admitted entries and captures | C2 limited to `POST /v1/querybatch` on S112, own capture (`corpus/source-snapshots/round-77/S112.txt`, sha256 `f3ca0465…`, matches the lesson) | **PARTIAL** — entry-level sweep done; clause-level overlaps not recorded; four endpoints not registered as leads (§3) | `grep -rn querybatch corpus/knowledge` → only `osv-post-v1-query-contract.md:75` (listed-not-described). Overlaps at `S108.txt:40-41` / `osv-post-v1-query-contract.md:21` and `S108.txt:136` are not disclosed (§3.2). |
| **V-D** two open L0 questions | Routed around; S112 id chosen so the staged package "cannot collide" (C2 B7) | **OPEN — and the dodge premise is FALSE** (new gap G1) | `.ufo/l0-questions.md:340` (Q01) and `:341` (S111 id collision) are the last kasegi round-76 rows, no answer below them, no `kasegi | round-77` row. `shokuknow/merge/kasegi/SOURCES.append.md:88` stages `S112` (TC260). |
| **V-E** round-start census re-run | `controls/sources-census-start-r77.txt` (10 lines, last line `rc=0`, committed `539a438`) | **CLOSED** | Base registry re-measured by me at `2e53fc7`: `git show 2e53fc7:corpus/SOURCES.md \| grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` = **111** (matches `c2-base-counters-r77.txt`, pre-freeze 09:14–09:18 -03). Census receipt itself prints no count; the count lives in the counters file. Knowledge count 91 and frontier 53 not re-measured by me. |
| **M76-4** A2 vs A4 conflict; landing order | r77 A2 names the revision (`C1-landing tree`) and a separate final-tree drift expectation (`entries=92, exit0_foreign=70`) | **PARTIAL** — revisions named; order not frozen; drift limb depends on an unfrozen C2 property (§4) | `claims.json:18` (A2 text). No landing-order sentence in `claims.json` or `w1-spec.json` (the spec only poses the question to seats). |
| **M76-6** working-tree contamination of frozen bytes | — | **Not repeated (as of my read)** | `git status --porcelain`: only `??` entries (`w1-dispatch.json`, `w1-spec.json`, `w1.ready`, `w1.ready.dispatched`, `w1/`, `corpus/lessons/round-77.md`). `git diff --stat 539a438 -- .ufo/waves/round-77 corpus` empty. `claims.json` sha256 prefix `502e8cb5` both committed and working. |
| **M76-7** dispatch order | w1 dispatched 12:39:55Z after freeze 12:35:02Z | **CLOSED for the freeze** (dispatch-internal ordering is out of my scope) | timestamps above. |

## 2. V-A in detail — is the case-6 RESULT consumption now load-bearing?

### 2.1 The five named kills (reproduced, scratch copies diffed against the reference)

Each `controls/m*.py` was diffed against `.ufo/waves/round-77/c1-amended-reference.py` (sha `18bfc439…`); the diff matches the transform table row for row (m1: lines 264-265 deleted; m2: closure body → `True` at :264-265; m3: case-6 line 253 deleted; m4: `is False` → `is True` at :329; m5: both-headers check deleted). Reruns, `python3 -B <file> --selftest`, `TMPDIR` on scratch:

| mutant | rc | last line | FAIL lines | kill class |
|---|---|---|---|---|
| K-M1 m1 | 1 | `cases=12 failures=3` | gate-regs, gate-consume (no-registration), gate-negpolarity (no-registration) | assertion |
| K-M2 m2 | 1 | `cases=12 failures=1` | gate-negpolarity `neg_ok=True` | assertion |
| K-M3 m3 | 1 | `cases=12 failures=2` | gate-consume `exception=NameError("name 'out6' is not defined")`, gate-negpolarity not-evaluated | exception (logged distinctly) |
| K-M4 m4 | 1 | `cases=12 failures=1` | gate-negpolarity `neg_ok=False` under inverted expectation | assertion |
| K-M5 m5 | 1 | `cases=11 failures=1` | gate-checkids `missing=['both-headers']` | assertion |

Reference (`c1-amended-reference.py`): rc 0, `selftest cases=12 failures=0`. Base counter (`2e53fc7`): rc 0, `selftest cases=6 failures=0`. r76 survivor `m2b-conjunct-removed.py` (frozen r76 bytes): rc 0, `selftest cases=8 failures=0` (A4 red-before reproduces).

### 2.2 Single-transform survivors outside the five named kills (my derivations, scratch)

| id | transform on the reference | rc | last line | why it survives |
|---|---|---|---|---|
| **X1** consumer call | `c1-amended-reference.py:318` `clean_ok = limb(out6, ret6)` → `clean_ok = True` | **0** | `cases=12 failures=0` | `gate-consume` checks `True is True`; the closure is still exercised by `gate-negpolarity` on case 2, which passes. The case-6 RESULT is never consumed, and nothing notices. |
| **X2** gate-consume boolean | `:323` `check("gate-consume", clean_ok is True,` → `check("gate-consume", True,` | **0** | `cases=12 failures=0` | the check is still recorded, so `gate-checkids` passes; its verdict is ignored. |
| X3 (admitted) gate-negpolarity boolean | `:329` `neg_ok is False` → `True` | 0 | `cases=12 failures=0` | this is the one survivor the known-limits paragraph names (`c1-mutant-transforms.md:25`). |
| X6 gate-consume line deleted | remove `:323` line | 1 | `gate-checkids FAIL missing=['gate-consume']`, `cases=11 failures=1` | killed by the id census. |
| X4 consumer call on case-2 inputs | `:318` uses `out2c, ret2c` | 1 | `gate-consume FAIL clean_ok=False` | killed. |
| X5 closure → `True` only | `:264-265` → `lambda out, ret: True` | 1 | `gate-negpolarity FAIL neg_ok=True` | killed (same class as K-M2). |

Reproduction: `python3 -B <file> --selftest` on each derivation; copies are `RevengerInherited-survivor-X1-consumer-const.py`, `…-X2-gateconsume-bool.py`, `…-X3-negpol-bool.py`, `…-killed-X6-gateconsume-deleted.py` and their run outputs `RevengerInherited-run-*.txt`.

### 2.3 Findings

- **F-A1 (K-M2 is mislabelled).** `claims.json:18` (A3) calls K-M2 "the required m2b-class kill". K-M2 neuters the registered closure; it dies at `gate-negpolarity` because the closure then returns True on case 2. The m2b class is a *consumer-side* removal: in the r76 design the consuming term was `and res6` in the case-6 check (`controls/m2b-conjunct-removed.py`, the `res6 =` at line 246 and its use at line 251). The r77 analogue of that removal is X1 or X2, and both survive.
- **F-A2 (the statement's own guarantee is falsified by X1).** `claims.json` statement: "a four-check gate consumes it in both polarities". Under X1 the case-6 polarity is not consumed and the selftest still passes. The kill rule does not trip because X1 is not one of the named mutants, so this is a gap in the frozen claim, not a breach of its kill rule.
- **F-A3 (the admission is honest but incomplete).** `c1-mutant-transforms.md:25` admits "a mutant that neuters the gate-negpolarity check's own boolean … or composite mutants". It does not mention X1 or X2, which are the same class (R127's own example is "remove the consuming assertion as well as probing computation deletion"). So M76-3 is reopened for the consumer side. The fix belongs to the next round: add the consumer-call and gate-consume-boolean transforms to the named set, with an external harness (the mutation seat) because an in-file gate cannot detect neutering of its own booleans.
- **F-A4 (the NameError issue is closed).** K-M3 now logs `gate-consume FAIL exception=NameError(...)`; the "consumed" check is a distinct, logged failure, and K-M1/K-M2/K-M4/K-M5 are assertion kills. The r76 failure where a deleted assignment passed as a kill is not reproduced.

## 3. V-C in detail — is the querybatch ground actually swept?

### 3.1 Entry-level sweep (done)
`grep -rn -i querybatch corpus/` shows: admitted entries — only `corpus/knowledge/osv-post-v1-query-contract.md:75` ("listed, not described"); captures — `S108.txt:5`, `S111.txt:5,43`, and S112. No admitted entry describes the batch contract. The endpoint string is held (the lesson's reject line is right about that).

### 3.2 Clause-level overlaps (not disclosed)
- **S112.txt:34-36** (version rules: "Each query item must follow the same rules as /v1/query" / "Use either version or a versioned purl, not both." / "Items with both will return 400 Bad Request.") restates **S108.txt:40-41** ("Use either the top-level version field or a versioned purl … not both." / "Requests that specify the version in both places return 400 Bad Request.") — already held as `osv-post-v1-query-contract.md:21`.
- **S112.txt:168** ("individual query … more than 1,000 vulnerabilities") shares the number and trigger with **S108.txt:136** ("more than 1,000 vulnerabilities in the response", F51 Limits). The batch threshold is per-query and new; the number is held.
- **Internal contradiction (F-C1):** the C2 statement claims "the per-item version rules with the 400 Bad Request consequence" as admitted ground (`claims.json:31`, and `SOURCES.md:124`), but B6 (`claims.json` B6) says "version rule content" is "cross-referenced as already-held … and not claimed". Under the kill rule, a claimed clause already held is NOT VERIFIED. This needs resolving before the entry is admitted; the lesson's Gate (`corpus/lessons/round-77.md`, untracked) does not mention S108:40-41 or S108:136 at all.

### 3.3 The other four endpoint contracts (partially closed)
- `determineversion`, `importfindings`, `ubuntu/binary-to-source`, `GET /v1/vulns/{id}`: **not** registered in `corpus/SOURCES.md` Leads (`:174-177` lists only the NDSS lead). The lesson's reject line names them.
- The receipts exist only in scratch (`/fast/scratch/hyaku/kasegi-r77/l1-research/`). I checked them: the four guessed slugs (`get-v1-vulns-id`, `get-v1experimental-importfindings`, `post-v1experimental-determineversion`, `post-v1experimental-ubuntu-binary-to-source`) are 404 pages of 11373 B each; the querybatch page is 30406 B. None of these is a live page.
- The lesson says "S111 navigation names the live slugs `get-v1-vulns/` …". `grep -i get-v1 corpus/source-snapshots/round-76/S111.txt` returns nothing; the capture shows endpoint labels only. The slug claim is not on committed bytes (G6).

## 4. M76-4 in detail — landing order and the A2 limbs

- Under **C1-then-C2**: A2 at the C1-landing tree reads `entries=91 … exit0_foreign=69` and is byte-identical to `c1-base-realtree-census-r77.txt` (C1 adds no population); at the final tree the drift expectation `entries=92, exit0_foreign=70` holds if the C2 entry is cd-prefixed and exits 0 from a foreign cwd. Both limbs are consistent **only** when measured at their two named revisions.
- Under **C2-then-C1**: at the C1-landing tree A2 reads 92/70, the base-parity limb fails, and M76-4 recurs.
- **R124 (QUALITY.md:576)** requires the landing order named. `claims.json` names two revisions but no ordering sentence; `w1-spec.json` asks seats the question and does not answer it. R124 is half-met (revisions named; order not frozen).
- **Unfrozen coupling (G5).** The drift expectation requires the new C2 knowledge file to carry a cd-prefixed first `recheck:` that exits 0 from a foreign cwd. No C2 predicate (B0–B7) freezes that. B3 counts frontier entries (56→57), not census conformance. A C2 entry with a relative recheck would fail A2's final-tree expectation with C1 correct.
- The kill rule says "at the landing commit" (singular) while A2 binds two revisions; this should be stated as "at the C1 commit (base parity) and at the final tree (drift)".

## 5. Newly-named gaps (routed; no frozen byte edited)

- **G1 — S112 id collision is real and B7's premise is false (highest severity).** `shokuknow/merge/kasegi/SOURCES.append.md:88`: `| S112 | TC260's own suggestion route …`. The staged package is 94 distinct rows, min S031, max S124, 30 rows above S094 (`RevengerInherited-staged-id-collision.txt`). 81 of 94 staged ids collide with the 111-row base registry (the L0 row says 80 at 110). `claims.json` B7 ("the staged shokuknow package (94 ids, S001-S094) cannot collide with it") and the lesson's assimilation line (`corpus/lessons/round-77.md:14`) are wrong. The r76 L0 rows (`.ufo/l0-questions.md:340-341`) remain open, and no round-77 L0 row routes the new S112 collision. Adoption is not happening this round, so the harm is latent, but the frozen predicate states a falsehood.
- **G2 — `claims.json:4` `frozen_at: 2026-11-05T12:45:00Z` is later than the freeze commit (committer 12:35:02Z) and the wave dispatch (12:39:55Z); the file's own mtime is 12:34:51Z.** The git commit is the evidence, and the freeze still predates the wave. The field is a wrong stamp.
- **G3 — mislabelled kill (F-A1)** and the missing consumer-side kill class (F-A2, F-A3). Routed to the next round's mutant table; not closable without rewriting frozen text.
- **G4 — C2 statement vs B6 contradiction on version rules and the per-query 1,000 threshold** (§3.2). Routed.
- **G5 — C2-to-A2 coupling** (§4). Routed.
- **G6 — lesson factual claims not on committed bytes:** "S111 navigation names the live slugs" (not in `S111.txt`); "the new S112 is outside that range and cannot collide" (false, G1); "C2 entry drafted in the wave dir" (no such file under `.ufo/waves/round-77/w1/` at read time). The four-endpoint receipts are scratch-only.
- **G7 — no registry lead for the four endpoints** (`SOURCES.md:174-177`); the r76 claim of a standing overview lead in Leads is also no longer visible there.
- **G8 — frontier numbering reuse.** `F54` names the refused r76 overview candidate and the r77 querybatch candidate (`.ufo/waves/round-76/claims.json:29`, `.ufo/waves/round-77/claims.json:31`). Minor; the next frontier row should take a fresh number.

## 6. Verification I did not run (other seats' scope)

- A2 real-tree census on the amended counter, B1–B7 counters, `capture-binding-check.py`, `frontier-recheck-count.py`, `sources-census.sh validate` on a landed tree, and any landing-tree measurement. I ran only the reference selftest, the mutants, the base counter, the r76 survivor, B0 on the frozen archive, and read-only git/grep checks.

## 7. Evidence files written to this directory (`.ufo/waves/round-77/w1/`)

`RevengerInherited.md` (this report); `RevengerInherited-survivor-X1-consumer-const.py`, `-X2-gateconsume-bool.py`, `-X3-negpol-bool.py`, `-killed-X6-gateconsume-deleted.py`; `RevengerInherited-run-{ref,X1-consumer-const,X2-gateconsume-bool,X3-negpol-bool,X5-closure-const-true-only-case6,X6}.txt`; `RevengerInherited-rerun-{m1-registration-removed,m2-consumption-neutered,m3-computation-deleted,m4-negpolarity-inverted,m5-check-deleted,reference,r76-m2b,base-donothing}.txt`; `RevengerInherited-rerun-B0-s112.txt`; `RevengerInherited-r76-m2b-run-src.py`; `RevengerInherited-staged-id-collision.txt`.

## 8. Notes for the integrator (KasegiR77)

- Messaged KasegiR77 (G1, X1/X2, G2) and MutC1-3 (X1/X2 derivations) before writing this report.
- Tooling: none installed or updated. No git mutation; no writes outside this wave dir and my scratch dir (scratch removed at yield).
