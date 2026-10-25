# MutateBountyConfine — mutation probe: bounty-fallback `under_mirror()` conjunct

Seat: `L1Kasegi23.MutateBountyConfine-2` (mutation-tester, leaf).
Round 23 FALSIFY wave. Read-only against the repo: the only repo write is this file.
All bytes under test were copied to `/tmp/kasegi-r23-falsify-MutateBountyConfine-2`
and every mutation ran there. No git/jj command, commit, or index touch. No installs.

## 1. Inputs and hashes

| artifact | sha256 |
|---|---|
| `corpus/instruments/resolve.py` (pristine) | `ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9` |
| `corpus/instruments/mirror-containment-fixtures.json` | `5e61a33ed5fa530547aff197fad9380d86d5850374bbb4f2a8f99df44b5e76a9` |
| `corpus/instruments/mirror-containment-check.py` | `1bc2db10dfbc59ef863e68afce475cd1d317da517137922804d7fc09cd46cecb` |
| mutant `resolve.py` (scratch) | `163f54b07adb30a28913e2df772b87e2cb3bc21b1bd27b89cb251f11f04a2e31` |

Repo `resolve.py` re-hashed after all work: unchanged, `ed9a9dae…`, mtime `2026-10-25 03:27:44`.
Post-run restore check: `cmp -s repo/resolve.py scratch/resolve.py` → `RESTORED_BYTE_IDENTICAL=yes`.

## 2. Mutation (one line, bounty fallback only)

`corpus/instruments/resolve.py:232`, inside `classify()`'s `if suffix is not None:` (bounty) branch:

```diff
@@ -229,7 +229,7 @@
         if m:
             return "RESOLVES", p, m, dom
         m, p = exists_any(os.path.join(mirror_root, suffix)) if suffix else (None, None)
-        if m and under_mirror(p, mirror_root):
+        if m:
             return "MIRROR-EQUIVALENT", p, m, dom
         return "GONE", "", "", dom
     sfx = mirror_suffix(base)
```

Exactly the conjunct was deleted: the sibling conjuncts at `:241` (canonical/`mirror_suffix`) and
`:253` (relative fallback) are untouched; `src.count("under_mirror(p")` is still `3`, and the
mutant parses (`AST_OK`). One-line, behavior-bearing, syntactically minimal.

## 3. Detector (identical on pristine, mutant, restored)

```bash
cd /tmp/kasegi-r23-falsify-MutateBountyConfine-2
python3 mirror-containment-check.py \
  --resolver resolve.py \
  --fixtures mirror-containment-fixtures.json \
  --json <baseline|mutated|restored>.json
```

The checker copies the selected resolver bytes into a disposable fixture tree, runs the real CLI
once per case with isolated `HOME` / `KASEGI_MIRROR` / lane root, and compares the CLI's own
`citation-survival.tsv` `class` column against the frozen expectation.

## 4. Results

| run | resolver sha256 | cases | pass | fail |
|---|---|---|---|---|
| pristine baseline (`baseline.log`, exit 0) | `ed9a9dae1002…` | 13 | 13 | 0 |
| **mutant** (`mutated.log`, exit 1) | `163f54b07adb…` | 13 | 10 | **3** |
| restored (`restored.log`, exit 0) | `ed9a9dae1002…` | 13 | 13 | 0 |

Baseline is clean, so the mutant failures are attributable. Every control passed on the mutant
(`controls 7/7`), i.e. the mutant introduces **no** false credit on any control; all 3 failures
are escape cases flipping into a credit class:

| case | expect | pristine | mutant | under_mirror call site |
|---|---|---|---|---|
| `bounty-parent-traversal` | GONE | GONE | **MIRROR-EQUIVALENT** | `resolve.py:232` |
| `bounty-parent-traversal-vault` | GONE | GONE | **MIRROR-EQUIVALENT** | `resolve.py:232` |
| `bounty-fallback-symlink-escape` | GONE | GONE | **MIRROR-EQUIVALENT** | `resolve.py:232` |
| all 7 controls + other 3 escapes | as frozen | pass | pass | — |

Verdict for this mutant: **KILLED** — 3 independent kills, 0 control damage.

## 5. Raw CLI evidence (reconstructed mutant bytes, sha256 asserted equal)

`raw-cli-probe.py` rebuilds the mutant from pristine bytes, asserts
`sha256 == 163f54b0…`, then runs both byte-sets through the real CLI on the same fixtures:

```
[bounty-parent-traversal] cite=~/Projects/bounties/../outside.md:1 expect=GONE
  pristine rc=0 | ~/Projects/bounties/../outside.md:1  GONE               (empty path)
  mutant  rc=0 | ~/Projects/bounties/../outside.md:1  MIRROR-EQUIVALENT  .../relocated/tbh/../outside.md
[bounty-parent-traversal-vault] cite=~/Projects/bounties/../outside-vault/secret.mjs:1 expect=GONE
  pristine rc=0 | GONE
  mutant  rc=0 | MIRROR-EQUIVALENT  .../relocated/tbh/../outside-vault/secret.mjs
[bounty-fallback-symlink-escape] cite=~/Projects/bounties/evil.mjs:1 expect=GONE
  pristine rc=0 | GONE
  mutant  rc=0 | MIRROR-EQUIVALENT  .../relocated/tbh/evil.mjs   (symlink → <root>/secret/outside.mjs)
[bounty-prefix-sibling-confusion]  pristine GONE | mutant GONE   (insensitive — see §6)
[confined-bounty-fallback-control] pristine MIRROR-EQUIVALENT | mutant MIRROR-EQUIVALENT
```

The escaped bytes are real file content outside the mirror root: the mutant credits them as
`MIRROR-EQUIVALENT` with `method=literal`, `domain=bounty`.

## 6. Is each escape case falsifiable?

Probes are non-mutating (in-memory) unless stated; `predicate-probe.py`, `callsite-probe.py`.

| # | escape case | falsifiable? | by what | evidence |
|---|---|---|---|---|
| 1 | `bounty-parent-traversal` | **yes** | `:232` conjunct deletion | flipped by this mutant |
| 2 | `bounty-parent-traversal-vault` | **yes** | `:232` conjunct deletion | flipped by this mutant |
| 3 | `relative-mirror-fallback-escape` | **yes** | `:253` conjunct deletion (not mine) | call site `[253]` only; flips to MIRROR-EQUIVALENT when `under_mirror` is a no-op |
| 4 | `bounty-fallback-symlink-escape` | **yes** | `:232` conjunct deletion | flipped by this mutant |
| 5 | `relative-fallback-symlink-escape` | **yes** | `:253` conjunct deletion (not mine) | call site `[253]` only; flips under no-op `under_mirror` |
| 6 | `bounty-prefix-sibling-confusion` | **yes, but not by any containment mutation** | `bounty_suffix()` boundary defect | reaches **no** `under_mirror` call site (`none`); with prefix mapping it flips GONE → MIRROR-EQUIVALENT while control 11 stays RESOLVES |

Case-6 detail: with pristine `bounty_suffix()`,
`bounty_suffix("~/Projects/bounties-legacy/README.md") == None`, so `classify` never enters the
bounty fallback; it falls to the literal-absolute branch, `exists_any(base)` misses, GONE. The
conjunct I deleted is not on its path at all — my mutant surviving case 6 is expected, not a gap
in the matrix. Simulating the pre-fix prefix mapping (`base.startswith(root)` without the
`root + "/"` boundary) yields `MIRROR-EQUIVALENT` for case 6 and leaves
`literal-prefix-sibling-control` at `RESOLVES`, so case 6 has a genuine falsifier in the
boundary class.

The global no-op probe also shows `canonical-alias-escape-control` (case 13, a control, expect
GONE) flips to `RESOLVES`; it is guarded solely by `:241`, so no seat should claim it via the
bounty or relative hunks. Disjointness confirmed with `L1Kasegi23.MutateRelConfine-2`
(mine = cases 1,2,4 at `:232`; their relative mutant = cases 3,5 at `:253`).

## 7. Coverage findings (from this probe, not restatements of C1)

1. **No control can kill this mutant.** All 7 controls pass on the mutant, including
   `confined-bounty-fallback-control` — it is *insensitive* to the conjunct (MIRROR-EQUIVALENT
   both with and without the gate), because the confined file is inside the mirror either way.
   The entire kill weight for the bounty-containment hunk rests on 3 escape cases. A control that
   discriminates would need a *bounty*-prefixed cite that resolves to a mirror-internal **symlink
   or traversal** landing inside the mirror, so removal of the gate still passes — as written, no
   control exercises the passing side of that specific predicate.
2. **The committed unit suite does not kill it.** `corpus/instruments/test_resolve.py` replayed
   via `KASEGI_RESOLVER_UNDER_TEST` in scratch: pristine `Ran 10 tests … OK`, mutant
   `Ran 10 tests … OK`. Its only bounty case, `test_bounty_control_relative_under_mirror`
   (`:249`), is a confined control and is insensitive. Detection is carried exclusively by the
   new frozen matrix.
3. **Containment is the only barrier in the bounty fallback.** The suffix is joined into
   `mirror_root` with no rejection or normalization of `..`; the mutant's own `resolved_path`
   column shows the unnormalized `.../relocated/tbh/../outside.md`, and for the symlink case shows
   a path *inside* the mirror whose content is outside. So consumer-visible rows carry no trace of
   the escape — the verdict is sound only because `under_mirror()` realpaths at classify time.
4. **Three independent guard sites, three disjoint mutant classes** (`:232`, `:241`, `:253`).
   Killing one hunk says nothing about the other two; the matrix's 13 cases cover all three, but
   the control set covers none of them discriminatingly.

## 8. Scope limits

- One assigned mutation (bounty-fallback conjunct). The `:253` and `:241` deletions were simulated
  in memory only for falsifiability/attribution evidence; no second mutant file was run as a seat
  deliverable (triaged to `L1Kasegi23.MutateRelConfine-2` for `:253`).
- Classifier behavior only. Nothing here establishes source availability, corpus attribution,
  quote fidelity, C2 coverage (F06–F08), or any score movement — no admission claimed.
- Fixtures are the frozen matrix; no new cases were added, so absence of a discriminating control
  in §7.1 is a finding about the frozen matrix, not a proposed contract change.
- Tooling: no installs or updates; `python3` from PATH only.
- Scratch durability: the cited `/tmp/kasegi-r23-falsify-MutateBountyConfine-2` tree was re-audited
  at 03:47:33 — intact, `resolve.py`/`pristine-resolve.py` still `ed9a9dae…` and
  `mutant-resolve.py` still `163f54b0…`. This report cites no `.ufo/…/scratch` path, and the
  mutation diff, both hashes, the result tables and the raw TSV rows are inlined above, so the
  findings survive any scratch loss. (The round-35 `scratch/` → `scratch-evidence/` relocation is
  `mado-shokunin`'s lane and is not a dependency of this one.)
