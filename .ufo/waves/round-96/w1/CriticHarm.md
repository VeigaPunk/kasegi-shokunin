# CriticHarm — round-96 harm audit

Base `d8a2bb0a2bdc2f6337ea2f849a1a557297067ad6`; freeze `804e7bc344df0808c880815dde077c28be5db18a`;
C1 landing `3c0581e2616df7a10af494a785b479d5e5293749`; C2 landing `7ef1d365eb523a83b2567342a6c0f585ab028ab0`.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Scratch: `/fast/scratch/hyaku/kasegi-r96/CriticHarm` (removed on exit).
All commands read-only on the lane's git state; every citation census was run on `git archive` extracts in scratch, never in the lane tree.

## Verdict

| item | line |
|---|---|
| 1 density guard + governance files | **NO HARM** |
| 2 citation tokens byte-unchanged + resolution | **NO HARM** |
| 3 C2 scanner cannot mask an earlier shape | **NO HARM** |
| 4 allowlist unchanged + clean `--rev` run | **NO HARM** |

One routed defect (**D1**, C2 docstring/SCORECARD known-limits overclaim for the 50-character `glagent-` form) — it does **not** re-score C2 under the frozen predicate K1–K6. Three pre-existing observations (§Pre-existing) that this round neither introduced nor touched.

## 1. Density guard and governance files — NO HARM

`SKILL.md` blob is `27f23a93848be29b76992ac35ce423ab9a23c269` at all three revisions (base, C1, C2 tip): the density guard cannot have moved because the bytes are identical. `PROVINCE.md` (`33458d01…`), `SHONEN.md` (`8c91054f…`) and `AGENTS.md` (`29964529…`) are byte-identical base→tip.

The two landings together (`804e7bc..7ef1d36`) modify exactly four paths — `SCORECARD.md`, `corpus/instruments/capture-secret-scan.py`, `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md`, `corpus/knowledge/triage-thresholds.md` — and nothing else. The parent chain is `d8a2bb0 → 804e7bc → 3c0581e → 7ef1d36`, so no landing sits on a stale base.

## 2. Citation tokens byte-unchanged and resolution — NO HARM

`corpus/knowledge/` holds 104 `.md` files; exactly two changed. Backticked `(file, token)` multisets over all 104 files:

| | distinct pairs | occurrences |
|---|---|---|
| base `d8a2bb0` | 6430 | 8726 |
| tip `7ef1d36` | 6431 | 8726 |

Removed pairs: 3 — `S041.txt:1680-1681`, `SKILL.md:182-184`, `SKILL.md:182-184,255-257`. Added pairs: 3 — `corpus/source-snapshots/round-30/S041.txt:1680-1681`, `SKILL.md:182-185`, `SKILL.md:182-185,255-257`. Every other citation token in the knowledge corpus is byte-unchanged; the occurrence total is identical (8726), so no token was silently dropped or duplicated.

Resolution, `corpus/instruments/resolve.py` run over `git archive` extracts of both revisions (base rc=0, tip rc=0; the instrument is the same file at both revisions, copied into each extract so its census writes stay in scratch):

```
base: distinct=7839 resolves=76 mirror=0 internal=2535 other=0 gone=5228 skill=166/732 corpus=2573/7437 all=2611/7839
tip:  distinct=7841 resolves=76 mirror=0 internal=2537 other=0 gone=5228 skill=166/732 corpus=2575/7439 all=2613/7841
```

The normalized census diff (scratch root replaced by `<ROOT>`) is four hunks and nothing else:

| change | detail |
|---|---|
| added | `corpus/source-snapshots/round-30/S041.txt:1680-1681` → INTERNAL |
| added | `SKILL.md:182-185` → INTERNAL |
| occurrences 3→2 | `S041.txt:1680-1681` stays GONE (the token survives at `corpus/lessons/round-95.md` and `round-95-verifier-spotcheck.md`) |
| occurrences 8→7 | `SKILL.md:182-184` stays INTERNAL (survives at four other triage-thresholds sites) |

`GONE` is **5228 at both revisions** and `RESOLVES` is 76 at both: not one citation lost resolution, and two gained it. The corpus rate moves 2573/7437 → 2575/7439 (+2/+2). The comma-combined forms `SKILL.md:182-184,255-257` / `SKILL.md:182-185,255-257` produce no census row at either revision (resolve.py does not extract them as path-like); a direct `classify` call returns GONE for both, so they change nothing either way.

Targeted classification of the six affected tokens (`resolve.classify` against each root; mirror root `/home/vgpnk/Projects/the-bounty-hunter` does not exist, so no mirror credit is possible in either run):

| token | base | tip |
|---|---|---|
| `S041.txt:1680-1681` | GONE | GONE (still cited at two `corpus/lessons` sites; the census row survives) |
| `corpus/source-snapshots/round-30/S041.txt:1680-1681` | — | INTERNAL |
| `SKILL.md:182-184` | INTERNAL | INTERNAL (still cited at 4 other sites) |
| `SKILL.md:182-185` | — | INTERNAL |
| `SKILL.md:182-184,255-257` | GONE | (token removed) |
| `SKILL.md:182-185,255-257` | — | GONE |

No citation lost resolution: the only class changes are GONE→INTERNAL (the bare-capture repoint) and the new `SKILL.md:182-185` (INTERNAL). The comma-combined form is GONE before and after, so the round neither gained nor lost anything there. Over the full `SKILL.md + corpus/**/*.md` scope the delta is +2 distinct tokens and +2 INTERNAL, with `GONE` unchanged at 5228 — both new tokens resolve. Over the meter's narrower scope (corpus/knowledge plus the files a label cites) the same edits give +1 distinct token and +2 resolving, because `SKILL.md:182-184` is still cited at four other triage-thresholds sites and so is not removed from the token set; that is exactly the meter's `1030/2027 → 1032/2028`.

## 3. C2 scanner cannot mask an earlier shape — NO HARM

Same input through the round-95 instrument (`d8a2bb0:corpus/instruments/capture-secret-scan.py`, sha256 `3006991a…`) and the landed instrument (sha256 `71876619…`), both with the tip allowlist:

- **Synthetic sample** built from the landed selftest's 117 case payloads (all positives and all boundary negatives, one case per line). Base reported **14** distinct shapes, tip reported **21**. The base set is a strict subset of the tip set — all 14 earlier shapes survive (`aws-access-key-id`, `aws-sts-session-token`, `azure-sas-signature`, `cloudfront-signed-cookie-signature`, `cloudfront-signed-url-signature`, `credential`, `gcs-signed-url-signature`, `github-refresh-token`, `github-token`, `gitlab-deploy-token`, `gitlab-jwt-token`, `gitlab-pat`, `gitlab-runner-auth-token`, `private-key`) and exactly the seven new shapes are added.
- **Real corpus** at `7ef1d36`: both instruments scan 2744 capture-path files and report `hits=0` — identical `(path, shape)` sets (empty).
- **Boundary probes**: `glpat-` + 27 chars with no dot → no hit on either (unchanged limit); `glrtr-` with a custom instance prefix (`myinst-glrtr-…`) → hit on the landed `gitlab-runner-auth-token-versioned`. The runner-versioned pattern omits `_GL_PREFIX` while S140 line 136 carries it, but `_GL_LB` already accepts a preceding `-`, so the omission costs no coverage — cosmetic, not a defect.

Mechanism: `scan_bytes` iterates every pattern and every `finditer` match and reports the first non-allowed hit **per shape name**, so a new shape cannot suppress an old one. The seven new patterns also cannot overlap an old span: `gitlab-pat` requires exactly 20 characters followed by a non-word character, and every routable/versioned head continues with word characters.

## 4. Allowlist unchanged and clean `--rev` run — NO HARM

`corpus/instruments/capture-secret-allow.tsv` is blob `b5b97c6873de366ebd2966fb56e61eec475450e7` at base **and** tip; the diff is empty. The landed instrument's `--rev 7ef1d365eb523a83b2567342a6c0f585ab028ab0 --allow corpus/instruments/capture-secret-allow.tsv` run prints `scanned=2744 hits=0 files=0 allowed=27 unused_allow=0 rc=0`; the round-95 instrument on the same revision prints the identical counters. `capture-source.py --selftest` (the intake gate, which imports the whole extended pattern tuple) still prints `intake-refuse=ok existing-kept=ok`, so the capability extension did not break the consumer.

## Routed defect

**D1 — the known-limits list drops `glagent-` entirely while the 50-character form stays undetected.**
The round-95 docstring listed `glagent-` at **S140 line 213** in the known-limits list; S140 line 213 is `glagent-[0-9a-zA-Z_\-]{50}` (50 characters, no `.`-suffixed tail). Round 96 adds only the *versioned* `glagent-` form (S140 line 358, `27-300` + `.xx.xx+7`) and then removes `glagent-` from the known-limits list altogether. Probe: `glagent-` + 50 characters produces **no hit** on the landed instrument. The SCORECARD row repeats the same claim ("the docstring's known-limits list drops the six families this round detects"), so the overclaim is carried at a second site.

- **Re-scores a claim?** No. K1–K6 never inspect the known-limits text: K1 pins the selftest count and the sha, K3's plants are the seven new shapes only, K4 compares the twelve earlier shapes. All six limbs reproduce on the landed instrument from my own runs — K1 `SELFTEST-RESULT pass cases=128` and sha256 `71876619…`; K2 `scanned=2744 hits=0 allowed=27 unused_allow=0 rc=0`; K3 the seven new shapes fire on the sample and no boundary negative does; K4 base ⊂ tip over the same sample; K5 exactly one `capture-secret-scan` row with first-round cell `87`; K6 `--rev 252df0c` (round-86 freeze) still reports `aws-sts-session-token` (rc=1, 6 hits, 2 files). The defect contradicts the C2 *statement*'s trailing clause "keeps the rest", not the predicate.
- **Smallest safe correction:** restore one clause to the known-limits sentence — the 50-character `glagent-` form (S140 line 213) — in the docstring and in the SCORECARD row. No pattern, selftest, or allowlist change.

## Pre-existing (not introduced by this round, no re-score)

- `corpus/instruments/citation-survival.tsv` was last regenerated at round 57 (`e300ad5`). At both base and tip it still lists `S041.txt:1680-1681` as GONE and does not know `SKILL.md:182-185`; it is a stale census of record, untouched by either landing. C1's predicate is the meter, not this file, so this does not re-score.
- Two census rows are column-shifted by a tab inside a citation (`file\tW04\tS072 …`, `kasegi\tok\t/home/…/corpus/SOURCES.md`) — round-57-era, unrelated.
- `iso-29147-divergence-and-clause-crosswalk.md:13`'s `S041.txt:1680-1681` numbers point at the "no major contradiction or inconsistency" sentence (S041 1680-1681), not at the "ISO/IEC 29147:2014 requires the policy and publication of part of it" clause (which the same paragraph cites at 1868-1870 and 1792-1867). The numbers were **not** changed by this round — only the path prefix was added — so this is a pre-existing attribution question, not a regression.

## Receipts

See `.ufo/waves/round-96/w1/CriticHarm-receipts/` — every command output cited above is stored there as `NN-*.txt` / `NN-*.out`, in the order referenced:

`01-skill-blob.txt`, `02-changed-files.txt`, `03-c1-knowledge-diff.txt`, `04-c1-iso-worddiff.txt`, `05-iso-current-lines.txt`, `06-iso-changed-substrings.txt`, `07-c1-triage-diff.txt`, `08-triage-changed-substrings.txt`, `09-skill-178-190.txt`, `10-s041-1830-1840.txt`, `11-resolve-base.out`, `12-resolve-tip.out`, `13-c2-scanner-diff.txt`, `14-gitlab-patterns-tip.txt`, `15-scanner-shas.txt`, `16-base-scan-rev.out`, `17-tip-scan-rev.out`, `18-base-scan-sample.out`, `19-tip-scan-sample.out`, `20-probe-tip.out`, `21-allowlist-diff.txt`, `22-allowlist-blobs.txt`, `23-governance-blobs.txt`, `24-knowledge-changed.txt`, `25-scorecard-diff.txt`, `26-scorecard-row.txt`, `27-s041-tokens.txt`, `28-scorecard-firstround.txt`, `29-scorecard-r96-clause.txt`, `30-resolve-tsv-diff.txt`, `31-committed-census-shas.txt`, `32-skill-182-185.txt`, `33-s041-1680-1681.txt`, `34-skill182184-sites.txt`, `35-base-selftest.out`, `36-capture-source-selftest.out`, `37-landings-only.txt`, `38-committed-class-totals.txt`, `39-census-history.txt`, `40-census-odd-rows.txt`, `41-targeted-classify.txt`, `42-k6-history.out`, `43-shape-set-diff.txt`, `44-fresh-census-diff.txt`, `45-s041-other-sites.txt`, `46-normalized-census-diff.txt`, `47-census-totals.txt`.

Commands and observed results (rc / key lines):

| # | command | observed |
|---|---|---|
| 01 | `git rev-parse <rev>:SKILL.md` for the three revs | all `27f23a93848be29b76992ac35ce423ab9a23c269` |
| 02 | `git diff --name-status d8a2bb0 7ef1d36` | 2 knowledge files + SCORECARD + scanner modified; freeze files added |
| 06/08 | `git diff -U0 --word-diff=plain …` | 5 changed substrings, exactly the labelled ones |
| 11 | `resolve.py <base extract>` | rc=0, `distinct=7839 … internal=2535 … gone=5228 … corpus=2573/7437` |
| 12 | `resolve.py <tip extract>` | rc=0, `distinct=7841 … internal=2537 … gone=5228 … corpus=2575/7439` |
| 16 | round-95 scanner `--rev 7ef1d36` | rc=0, `scanned=2744 hits=0 allowed=27 unused_allow=0` |
| 17 | landed scanner `--rev 7ef1d36` | rc=0, same counters |
| 18/19 | both scanners `--files <sample>` | rc=1, base 14 shapes / tip 21 shapes |
| 20 | landed scanner on boundary probes | 3 hits; `glagent-`+50 → none |
| 23 | `git rev-parse <rev>:PROVINCE.md` etc. | PROVINCE/SHONEN/AGENTS/SKILL identical base→tip |
| 28 | `awk -F'|'` on the SCORECARD row | `NF=6`, first-round cell ` 87 ` |
| 35 | round-95 scanner `--selftest` | `SELFTEST-RESULT pass cases=115` |
| 36 | `capture-source.py --selftest` | rc=0, `intake-refuse=ok existing-kept=ok` |
| 42 | landed scanner `--rev 252df0c` | rc=1, `aws-sts-session-token` present, 6 hits / 2 files |
| 43 | set difference of 18/19 | base ⊆ tip, missing none, +7 new shapes |
| 46 | normalized census diff | 4 hunks: +2 INTERNAL tokens, 2 occurrence-count drops |
| 47 | class totals | INTERNAL 2535→2537, GONE unchanged, RESOLVES 76→76 |
