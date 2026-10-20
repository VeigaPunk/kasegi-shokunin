# Round 23 — GeneratedReport review

Axes: **depth:verifiability** (C1 detector soundness); **coverage** (whether the copied CLI fixture exercises the stated exclusion).

## Finding — C1 behavioral blocker

**[INFERENCE; static control-flow derivation, not executed]** With fixture-style roots `lane=<fix>/lane` and `mirror=<fix>/relocated/tbh`, create `<fix>/relocated/outside-vault/secret.mjs` but leave `<fix>/outside-vault/secret.mjs` absent. Cite `` `../outside-vault/secret.mjs:1` ``. `PATHY` accepts `..` as path-like (`resolve.py:85`); after stripping the line anchor, the lane-first candidate misses, then `classify` checks `os.path.join(mirror_root, base)` (`resolve.py:226-233`). That join resolves to `<fix>/relocated/outside-vault/secret.mjs`, outside the selected mirror, and the branch returns **MIRROR-EQUIVALENT** without `under_mirror`. C1 requires **GONE** for this mirror-fallback escape. `under_mirror` is defined at `resolve.py:194-199` but only guards the explicit-canonical-alias branch at `resolve.py:219-222`; it does not guard either the bounty fallback (`resolve.py:204-213`) or relative fallback (`resolve.py:226-234`). This is a falsifiable wave2 probe: feed the token to the copied CLI with the described fixture and assert GONE.

The existing dot-dot case does not falsify this: `test_resolve.py:255-272` uses canonical-alias tokens, which enter the guarded branch. The symlink case likewise uses a canonical alias (`test_resolve.py:274-279`).

## Compatibility invariant

Keep relative lane-first behavior: `ops/check-freshness.mjs:1` present under both roots remains **INTERNAL** at the lane path; mirror-only `ops/claim-index.mjs:7` remains **MIRROR-EQUIVALENT** at the confined mirror path; absent `ops/absent-rel.mjs:2` remains **GONE** (`test_resolve.py:221-235`). These are existing compatibility controls and should survive the confinement fix.

## Generated-report exclusion / fixture coverage

Production collection excludes only the lane-root-relative `corpus/instruments/citation-survival.md` (`resolve.py:115,250-260`). The fixture runner copies the resolver to `<fix>/work/resolve.py`, passes `<fix>/lane` as the scan root, and checks the TSV under `work` (`test_resolve.py:66-74,105-138`); output location is derived from the copied script (`resolve.py:285-286,306-308,546-548`). Therefore `work/citation-survival.md` is outside the scanned lane tree, so this runner does **not** exercise the `GENERATED_REPORT` exclusion or prove repeated-run self-input exclusion. This is a test-coverage gap, not evidence that the normal repo-root path is currently included: when the script is in `corpus/instruments` and the lane root is the repo, the exact relative path is excluded.

## Verification and limits

Read-only source inspection only; tests were not run as requested. `git diff -- corpus/instruments/resolve.py corpus/instruments/test_resolve.py` returned no output. LSP was unavailable (`read xd://lsp` reported no such mounted tool); no grep was used as semantic proof. Findings cover only C1 mirror-fallback confinement and generated-report fixture coverage.