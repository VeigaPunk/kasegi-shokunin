# MutC2Row — S053 row mutation probe (round 36, wave 1)

Seat: MutC2Row (mutation-tester, leaf). Scope: mutate the drafted S053 row, run the census
validator on a scratch SOURCES.md, record which mutations are caught. Judged on: coverage.

## Subject under mutation

- Detector: `scripts/sources-census.sh` (fleet root, executed read-only), mode `validate --file <path>`.
  Exit contract: 0 clean/warnings-only, 1 findings. Lane label in output: `file`.
- Drafted row: ScribeRowS053 receipt line 22 (895 bytes, 13 pipe-fields = 11 columns), extracted
  byte-exact to scratch `s053-row.txt` and inserted after the S052 row (line 59) inside `## Registry`.
- Fixture tree: `git archive HEAD (b47f2cdf)` exported to scratch `proposed/` (read-only `git archive`,
  no git state touched), plus scratch fixture files:
  - `corpus/knowledge/epss-exploit-prediction-scoring.md` — path-only fixture (E11 checks existence,
    not content; the real drafted entry lands from ScribeEntryF19).
  - `corpus/source-snapshots/round-36/{manifest.json,S053.txt}` — manifest is the REAL ExecC2Capture
    manifest copied verbatim from the ExecC2Capture receipt (json-parsed OK: 1 record, id S053,
    url `https://www.first.org/epss/`, path S053.txt); S053.txt is a path-only fixture (rule B5
    compares record url to the row's https token; capture content is not read by rule B).

## Baseline (prerequisite for any verdict)

- Untouched HEAD export, no S053: `validate` exit 0 (52 rows, no S053 line).
- Wildtype draft (base + correct S053 row): `validate` exit 0, `file ok <path>`; only the two
  pre-existing base-registry W04 warnings (S028, S029). **Baseline passes** — mutant verdicts below are
  meaningful. Wildtype sha256 `e3832adad1ad6c4da32f44810c2e0e0b1b693429d663c17984d4ae33d5e615c3`.
- capture-binding-check baseline: plain tree exit 0 (`records=42 bound=42 unbound=0`); wildtype + real
  round-36 manifest exit 0 (`records=43 bound=43 unbound=0`).

## Mutants (each applied alone to a fresh copy of the wildtype; row-level findings shown)

| # | mutation | census validate | finding line | verdict |
|---|---|---|---|---|
| m1a | drop last cell → 10 data columns (NF=12) | exit 1 | `E01 S053 fields=10` | **killed** |
| m1b | add cell → 12 data columns (NF=14) | exit 1 | `E01 S053 fields=12` | **killed** |
| m2 | embedded `\|` inside teaches cell | exit 1 | `E01 S053 fields=12` | **killed** (caught as field-count, not silently split) |
| m3 | status `mined` → `watch` | exit 1 | `E07 S053 status=watch` | **killed** |
| m4 | duplicate id S053 (second row, distinct url+scope so E04/W04 cannot confound) | exit 1 | `E03 S053 duplicate id` | **killed** |
| m5 | tier `A` → `B` | exit 0 | none (`file ok`) | **SURVIVED by census** |
| m6 | row url `https://www.first.org/epss/` → `https://www.first.org/epss` (mismatch vs manifest) | exit 0 | none (`file ok`) | **SURVIVED by census; killed by capture-binding-check** |

Mutant file sha256s (scratch, deleted with the scratch dir):
m1a `8b636120111d996b18a352fc40471d244bfe70878939b1cb3615c33329047009`,
m1b `e04e3a609dcea395718a5c5ae06868f67f9812f816bf569f35846346ce61ed86`,
m2 `6ce31180241302082fc3e3ef23643ec665d0bc0ec6cb7a1e808d3b2fc3323658`,
m3 `eaca140cb0f208ebae8d13c2f3f708d17588184190761c6bc42f7793b3386b10`,
m4 `02f4f5ad809e6e7bf33ef4c81d8cebeec6fd18428af448fcd8764f56a691a6a9`,
m5 `ca7473c985bc2b6e6c16b692851888146f083866951cdccb6014916eb815a1b4`,
m6 `33ae90d099554a9072616f9989bc01d3bffc96ae1cc8b17a578aabc081084bbc`.

## Survivor analysis (coverage findings, not contract changes)

- **m5 (tier A→B)**: the item's question "allowed? check enum only" — yes. E06 fires only for tiers
  outside `[ABC]`; `B` is enum-valid, so the census validator structurally cannot catch a tier
  downgrade. `validate` exit stays 0. The only census-side signal is a count drift, not an exit code:
  census mode prints `tier.A 50→49, tier.B 1→2` (still exit 0). Enforcement of "load-bearing claims
  rest on tier A" (QUALITY Q2) therefore lives entirely outside this instrument — reviewers/harness
  must carry it. A count-anchored receipt comparison (tier.A = 50 on the proposed tree) would notice.
- **m6 (URL vs manifest)**: the census validator has no manifest awareness at all (no `manifest`
  reference in the script; E04 is a same-registry duplicate-URL+scope rule). Its url normalizer even
  strips the trailing slash, so the near-miss variant is invisible to it. The actual killer is
  `corpus/instruments/capture-binding-check.py` rule B5: with the same mutant row + the real manifest →
  exit 1, `FAIL rule=url-mismatch record=S053 row=S053 dir=round-36`, `records=43 bound=42 unbound=1`;
  restored wildtype row → exit 0, `records=43 bound=43 unbound=0`. So the C2 claim's URL binding is
  covered, but only by the second instrument — census `exit 0` alone proves nothing about manifest
  binding.

## Probe hygiene

- First mutant batch was run with mutant files placed outside the fixture tree, which flooded
  `E11 missing used-by` for every row (used-by paths resolve against `dirname(file)/..`). That batch's
  E01/E03/E07 row findings were identical, but it was discarded and fully re-run in-tree
  (`proposed/corpus/mut-*.md`); the table above is the clean run.
- No detector code was modified; every verdict comes from the committed instruments as-is.

## Restoration evidence

- All mutation work happened on scratch copies only. Lane `corpus/SOURCES.md` sha256
  `0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba` before AND after the whole probe;
  `git status --porcelain -- corpus/SOURCES.md` = empty. No mutating git/jj command was run anywhere.
- Restored wildtype draft re-run: `validate` exit 0 (`file ok`), sha
  `e3832adad1ad6c4da32f44810c2e0e0b1b693429d663c17984d4ae33d5e615c3` — byte-identical to the pre-mutation
  wildtype; binding check exit 0 (43/43 bound).

## Tooling

No tools installed or upgraded (bash, python3, gawk, git, sha256sum sufficed). No pacman use.

## Bottom line

Caught by census validate: broken column count (E01, both directions), embedded `|` (E01), wrong
status enum (E07), duplicate id (E03). Not caught by census validate: tier A→B (enum-valid; only a
tier.A count drift, exit unchanged) and URL-vs-manifest mismatch (caught by capture-binding-check.py
B5 instead). C2's "census exit 0" predicate is therefore necessary but not sufficient for row
integrity — it must keep its capture-binding and tier-count companions.
