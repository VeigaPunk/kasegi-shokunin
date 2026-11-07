# CriticClaims — round 90, attempt 1: attack report

Seat: CriticClaims. Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin.
Scope: falsify C1 and C2 only on their frozen predicates (`.ufo/waves/round-90/claims.json` at freeze `33f43db9`). Findings are routed defects/qualifiers, never re-scoring. Every reading below is revision-pinned (`git archive <rev>` extracts, `git show <rev>:<path>`); the live working tree was read only for `git status`. I edited no lane file.
Scratch `/fast/scratch/hyaku/kasegi-r90/CriticClaims` (clone, extracts, fixtures, mutants) was deleted before yield. Receipts: `.ufo/waves/round-90/w1/CriticClaims-receipts/`.

## Verdicts

| Claim | Verdict | Basis |
|---|---|---|
| C1 | **VERIFIED** | P1 pass on the live lane and on a `git clone --shared` checked out at `4a7e6768`; P2 pins equal claims.json/worktree/freeze; P3 exactly one path; selection independently reproduced. |
| C2 | **VERIFIED** | P1 pass at seeds 9090, 1 and runtime seeds 1507620440 (receipt) and 1132209826 (earlier run); P2 landed bytes = candidate = `0630d32b…`; P3 exactly the three permitted paths; do-nothing control reproduced failing. |

## Freeze and order check (both claims)

- Chain: base `6088c3e` → freeze `33f43db9` → C1 `4a7e6768` → C2 `643ddb43` → receipts `779062a`. `merge-base --is-ancestor` returns 0 for base→freeze, freeze→C1, freeze→C2.
- Freeze tree contains the executed controls: `controls/c1-controls-r90.{sh,txt}`, `controls/c2-controls-r90.{sh,txt}`, `controls/c2-forgeries.py`, `controls/capture-scan-r90.txt`, `controls/census-start-r90.txt`. `claims.json` at freeze is byte-equal to the worktree copy (`892d9d88…`).
- Control receipts: C1 candidate PASS; no-work (`after=base`), shift+1, superset (846/1829), unlabelled CORRECT site, working-tree-only all FAIL. C2 candidate PASS; no-work/base FAIL (G1 writes all 11 plants, G2 destroys the existing file, G4 rc=2, G5 writes); F1 blanket, F2 partial, F3 write-then-check, F4 no-allow, F5 fail-open, F6 leaky each FAIL at least one limb. I re-ran the C2 no-work control myself: `G1 FAIL … written=True` ×11, `G2 FAIL rc=0 kept=False`, `G4 FAIL allowed_rc=2`, `G5 FAIL rc=0 written=True`; result `fail rc=1` (`CriticClaims-receipts/c2-no-work.txt`).
- Commit timestamps are consistent with freeze-before-landing (04:03:51 vs 04:03:58/04:04:19), but timestamps are not independent proof; topology + the receipts' contents (candidate runs at base, no landing references) are what I can verify.

## C1 — depth:verifiability tranche 5

### Predicate

- P1 live lane (`--lane .`): `base=812/1827 after=843/1829 sites=34`; LIMB M0,M1,M3,M4,M5,M9,M6 all `pass`; `KNOWLEDGE-METER-RESULT pass rc=0` (`c1-meter-live.txt`).
- P1 clone: same output with `--lane <clone at 4a7e6768>` (`c1-meter-clone.txt`). Identical numbers, so the round-89 closure fix (both trees from `git archive REV`) holds on a clean clone.
- P2: counter `8f4ac218…36d4`, map `7c420856…38b3`; equal in claims.json, the worktree, and the freeze tree. Labels file `d1e87645…3229` at `02b6d88f` equals its worktree copy.
- P3 (`git diff-tree --no-commit-id --name-only -r 4a7e6768`): exactly `corpus/knowledge/triage-thresholds.md`.
- Excluded lines 152, 155, 249, 438 are byte-identical base→landing (M3 also binds every unmapped line).

### Independent selection check (`c1-selection-check.txt`)

Labels at `02b6d88f`: 46 data rows = 40 WRONG (38 with a supported range, 2 with `none`), 2 CORRECT, 3 UNCLEAR, 1 MENTION. Set equality holds both ways:

- map rows (34) \ WRONG-with-range labels = ∅;
- WRONG-with-range labels \ map rows = exactly the 4 excluded sites `152,155,249,438`;
- every excluded site is a WRONG-with-range label pair, and each excluded `.tsv` reason matches the label's reason text (stale premise / contradicted content / unsupported tail).

So the stated rule "34 = 38 WRONG-with-range − 4 stale/unsupported" is what the frozen map encodes, not just a subset of it. The two WRONG/`none` rows (141,142) are correctly outside the "with a supported range" clause.

Label drift: every label-target entry (`claim-gates`, `claim-package-contract`, `ev-model`, `intake-surface`, `mission-control`) has the same blob at `eb5f0df8`, base `6088c3e`, C1 `4a7e6768` and C2 `643ddb43`. The two entries that changed between `eb5f0df8` and base are the signed-URL-credentials entries, not label targets. I spot-read 20+ labelled ranges at the landing (claim-gates L41,45-48,67..77,82-85,86-87; claim-package-contract 24-26,31-34,54; ev-model 14-18,22-23; intake-surface 80-85; mission-control 17,29,36,40,59-60,61-64,64-66,66): each states the row content.

Token arithmetic (re-derived with the counter's own `reading()`; `c1-token-diff.txt`): base 1827 tokens/812 non-GONE → landing 1829/843; 29 key tokens removed (all GONE), 31 value tokens added (all non-GONE), 0 verdict flips. The 34 sites give 31 new tokens because three values are duplicated (claim-gates.md:68 ×2, ev-model.md:22-23 ×2, mission-control.md:61-64 ×2), and two map keys stay GONE because excluded/unmapped lines still cite them (claim-gates.md:42-47 line 249; mission-control.md:13-14 lines 141/142). Net +2 denominator, +31 non-GONE — exactly the claimed numbers.

### Findings

- **C1-F1 (routed defect, low).** M9 binds every map row to a WRONG label but never asserts the map is the *complete* selected set; `sites=34` is `len(rows)`, not a label-derived count, and the counter never reads `excluded.tsv`. A map that swaps an applied site for an excluded site (both are WRONG labels) could pass M9. Not exploitable here: M6 pins the map sha, and I verified the selection independently. Smallest safe correction: a completeness limb — compute `{WRONG with supported range} − excluded.tsv` from the labels at `labels-rev` and require set equality (and print 38/4/34), so the next round's map does not depend on the author's selection.
- **C1-F2 (interpretation qualifier, no defect).** The meter counts unique citation tokens, so "34 sites repointed" produces +31 non-GONE, not +34; the claim asserts only the meter numbers, which are exact. Do not read 843−812 as 31 resolved sites beyond the token set.
- **C1-F3 (checked assumption).** Label-rev drift would have falsified the repoints; it is absent for every label target (above).

## C2 — coverage, capture-intake-gate

### Predicate

- P1 at `643ddb43` with `--instrument-sha256 0630d32b…`:
  - seed 9090, seed 1, runtime seed 1507620440 (a second runtime run drew 1132209826 and passed identically): `LIMB G0 pass shapes=11`, `G1 pass plants=11`, `G2 pass rc=3 kept=True`, `G3 pass clean=6`, `G4 pass allowed_rc=0 written=True other_path_rc=3 never_allowed_rc=3`, `G5 pass rc=3 written=False`, `G6 pass rc=0`, `P pass sha256=0630d32b…`, `CAPABILITY-CHECK-RESULT pass rc=0` (`c2-seeds.txt`).
- P2: `643ddb43:corpus/instruments/capture-source.py` = `0630d32b…`, equal to the candidate and to the worktree; base instrument = `e1831888…`.
- P3: exactly `SCORECARD.md`, `corpus/instruments/README.md`, `corpus/instruments/capture-source.py`.
- S131: added by the freeze, present at both landings; `S131.txt:570` is the push-protection sentence the instrument docstring cites; sha `0c98d69a…` equals the landing receipt's gate re-capture of the live page.

### Beyond-counter probes (landed instrument, loopback HTTP; fixtures in deleted scratch)

| Probe | Result |
|---|---|
| A multi-line credential on line 3 | rc 3, out absent, `INTAKE-REFUSED … shape=aws-sts-session-token line=3`, no value echo |
| B `--kind text` credential | rc 3, out absent, shapes credential + aws-sts-session-token |
| C malformed allowlist row | rc 3, out absent, `shape=gate-error:OSError` (fail closed) |
| D allowlist row with wrong digest, same path | rc 3, out absent, `shape=credential` (digest-bound) |
| E missing explicit `--allow` file | credential input rc 3; clean input rc 0 and written (missing = empty, not "unloadable") |
| F scanner present but unparseable | rc 3, out absent, `shape=gate-error:SyntaxError` |
| G credential after a 1 MiB clean prefix | rc 3, out absent (full-bytes scan) |
| H S128 at its committed allowlisted path / same bytes at another path | rc 0, written, bytes equal to the stored snapshot / rc 3, cloudfront shape |
| I credential only inside `<script>` (stripped before the snapshot) | rc 0, written — consistent with "snapshot bytes" |
| J documented example key `AKIAIOSFODNN7EXAMPLE` | rc 0, written, no shape (scanner's hardcoded exception, any path) |
| K another AKIA id | rc 3, out absent, `shape=aws-access-key-id` |

(`c2-probes.txt`.) The landed instrument therefore satisfies the statement on every element I could exercise; the gaps below are predicate gaps, not landing defects.

### Findings

- **C2-F1 (routed defect, medium).** G1 does not bind the `line` element of "(shape, line, never the value)". A candidate identical to the frozen one except that the refusal print drops `line=%d` passes G0–G6 and P (mutant sha `be181b2d…`; `c2-mutants.txt`). The landed bytes are correct (probe A). Smallest safe correction: one G1 fixture with the credential on a known line (e.g., line 3) and an assertion that the `INTAKE-REFUSED` line carries `line=3`.
- **C2-F2 (routed defect, high).** G1–G6 do not bind "scans every capture" to the whole bytes. A candidate that scans only `data[:65536]` passes all seven limbs and P (mutant sha `8dcedb10…`); on a 1 MiB-prefixed capture it writes the credential in a snapshot (rc 0), while the landed instrument refuses rc 3 with shapes credential + aws-sts-session-token. The landed statement holds; the frozen predicate does not force it. Smallest safe correction: one G1 plant behind a >64 KiB clean prefix (a 1 MiB prefix costs nothing at this counter's scale), or plant at an offset that proves the scan end.
- **C2-F3 (qualifier).** "(imported)" is only weakly bound: G0 derives shape names from the scanner at REV and G5 requires refusal when the scanner file is absent, but a copied pattern table plus a presence check would pass. The landed instrument does import (`load_scanner` → `importlib`), verified by code read. Smallest correction: either drop "(imported)" from the claim or add a stub-scanner limb (replace `capture-secret-scan.py` with a stub whose `scan_bytes` reports a hit on a clean input and require the instrument to refuse), which binds that the gate consumes the scanner's result.
- **C2-F4 (qualifier).** "an unloadable scanner or bad allowlist refuses (fail closed)" holds for a malformed or never-allowed allowlist row (probe C, G4) and for a broken/missing scanner (probe F, G5), but a *missing* `--allow` file is treated as an empty allowlist (probe E). State "malformed/refused row" instead of "unloadable allowlist", or refuse a missing explicit `--allow`.
- **C2-F5 (qualifier).** The scanner's hardcoded `ALLOWED_VALUES` lets the documented AWS example key through at any path with no allowlist row (probe J; another AKIA id is refused, probe K). Pre-existing scanner behaviour, imported; not credential material, but it is an allow-through the statement's "an allowlist row lets one documented value through at one path" does not name. Name it in the instrument docstring/README.
- **C2-F6 (observation, pre-existing, not introduced).** A successful `file://` capture crashes after writing in both the base and landed instruments (`response.status` is `None` → `%d` TypeError): rc 1 with the file written. The C2 counter drives only loopback HTTP, so G3 sees rc 0; byte-identity still holds (both write the same bytes then crash). Route to instrument cleanup (format `status` or reject non-http URLs in `fetch`), not to C2.
- **C2-F7 (axis judgement, not re-scoring).** C2 is a capability acquisition in the lane's bookkeeping (new SCORECARD row, new refuse-before-write operation), but it hardens an existing instrument (`capture-source.py`) rather than adding a new domain surface; rounds 88–89 called the analogous scanner additions "capability extension". Coverage is held at 8 either way; if the judge distinguishes acquisition from extension, this is an extension on an existing surface.

### Statement vs predicate (C2)

Bound: refusal before write (G1/G2), nothing written and existing bytes kept, exit 3, per-shape naming, no drawn-value echo, digest-bound path allowlist, clean byte-identity to the base instrument, malformed/never-allowed allowlist and missing scanner refusal. Not bound: the `line` field (C2-F1), whole-bytes scan scope (C2-F2), "(imported)" (C2-F3), missing-allowlist behaviour (C2-F4), and the hardcoded documented-example exception (C2-F5). The verdict stands on the landed artifact because the landed bytes were directly probed where the counter is silent.

## Hygiene

No credential-shaped value was written into the wave directory. All fixtures, mutants and planted captures lived under the scratch root and were deleted; receipts carry only counter output (shapes, rc, paths, digests), never a matched value. The only key id in the receipts is `AKIAIOSFODNN7EXAMPLE`, which the scanner's `ALLOWED_VALUES` permits. Self-scan: `CriticClaims-receipts/hygiene-scan.txt`.

## Files written

- `.ufo/waves/round-90/w1/CriticClaims.md` (this report)
- `.ufo/waves/round-90/w1/CriticClaims-receipts/c1-meter-live.txt`
- `.ufo/waves/round-90/w1/CriticClaims-receipts/c1-meter-clone.txt`
- `.ufo/waves/round-90/w1/CriticClaims-receipts/c1-selection-check.txt`
- `.ufo/waves/round-90/w1/CriticClaims-receipts/c1-token-diff.txt`
- `.ufo/waves/round-90/w1/CriticClaims-receipts/c2-seeds.txt`
- `.ufo/waves/round-90/w1/CriticClaims-receipts/c2-no-work.txt`
- `.ufo/waves/round-90/w1/CriticClaims-receipts/c2-mutants.txt`
- `.ufo/waves/round-90/w1/CriticClaims-receipts/c2-probes.txt`
- `.ufo/waves/round-90/w1/CriticClaims-receipts/pins-and-topology.txt`
- `.ufo/waves/round-90/w1/CriticClaims-receipts/hygiene-scan.txt`
