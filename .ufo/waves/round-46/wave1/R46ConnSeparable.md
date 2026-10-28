VERDICT: BROKEN

# R46ConnSeparable — are C1 and C2 causally separable?

Seat: R46ConnSeparable (connector, leaf, read-only except this Report). Lane: kasegi round 46. Frozen claims sha256 `e56ebf87…` (matches `freeze.txt`). Base `914ca0b6`, freeze `9f23aab4`, lane HEAD `323d1f5` (spec commit; the freeze tree is an ancestor).

## Answer

- **Each claim is verifiable alone.** C1 alone reads `c1-gate fixed=7/7 exit=0` (tree T1). C2 alone reads `c2-gate fixed=7/7 exit=0` (tree T2). Both satisfy the AXES.md sense of "each verifiable without the other having landed".
- **They are not composable under the frozen counters.** At the joint tip (T12 = C1 + C2) the frozen C2 counter reads `c2-gate fixed=6/7 exit=1`. C2 gate G6 fails because C1's re-grounds necessarily edit two of the 64 base knowledge files that G6 pins byte-for-byte. C2's kill rule ("fixes < 7/7 at the final lane revision") fires at the tip. No tip satisfies both frozen counters.
- The C2 entry's own recheck form is a second, weaker coupling: if it is written as a gated line, C1 drops to `5/7` (F2).

## Counter readings (lane counters run against each tree; trees are scratch copies)

Method: `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-c1-gate.py --root <tree> --baseline <base-export>` and `python3 …/r46-c2-gate.py --root <tree>`, with `TMPDIR` set to the seat scratch. Lane counter bytes are the freeze bytes (`sha256 b0c730c8…` / `0ee95857…`, matching `freeze.txt`).

| tree | what it contains | C1 line | C2 line |
|---|---|---|---|
| base (do-nothing) | pure base export | `c1-gate fixed=1/7 exit=1` | `c2-gate fixed=1/7 exit=1` |
| F (freeze) | base + freeze-commit counters and S073 capture | `c1-gate fixed=1/7 exit=1` | `c2-gate fixed=2/7 exit=1` |
| T1 (C1 only) | F + C1 re-grounds of 2 entries | `c1-gate fixed=7/7 exit=0` | `c2-gate fixed=2/7 exit=1` |
| T2 (C2 only) | F + C2 entry, F28 row, S073 row, expected line | `c1-gate fixed=1/7 exit=1` | `c2-gate fixed=7/7 exit=0` |
| T12 (both) | F + C1 + C2 | `c1-gate fixed=7/7 exit=0` | `c2-gate fixed=6/7 exit=1` |
| T12g (both, C2 recheck gated) | T12 with `test -d ~/Projects/absent-r46 &&` prefixed to the C2 recheck | `c1-gate fixed=5/7 exit=1` | `c2-gate fixed=6/7 exit=1` |

Base and F match the freeze record: base `c1 fixed=1/7`, `c2 fixed=1/7`; F `c1 fixed=1/7`, `c2 fixed=2/7` (claims.json `freeze_tree_reading`).

## Findings

### F1 (BROKEN) — C1 landing breaks C2 gate G6 at the tip

Attacked: `corpus/instruments/r46-c2-gate.py` G6 base-knowledge pin (PINS at line 63; `base_ok` / `cont` at lines 284-289 hash the 64 non-F28 knowledge entries).

Command and output, T12:
```
gate G6 pass=0 read=knowledge=65 base-names-intact=0 entry-bytes-ok=1
c2-gate fixed=6/7 exit=1
```
Same gate on T1 (C1 only): `gate G6 pass=0 read=knowledge=64 base-names-intact=0 entry-bytes-ok=0`. On T2 (C2 only): `gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1`. Between T2 and T12 the only C2 gate that changes is G6 (every other C2 gate reads `pass=1` in both); the C1 bytes alone cause the break. On T1 the C2 entry is absent, so G1, G2, G3 and G5 read 0 by construction.

Pin check: my recomputation of the base hash on the pure export gives `names-sha bf304481…` and `content-sha f734506f…`, both equal to PINS (`base-knowledge-content f734506f…`). So the pin is the base bytes, not the tip bytes. (The G6 docstring says "the other 64 files are the round-46 tip's bytes"; the value pinned is the base's.)

Why this cannot be engineered around inside C1's frozen rules: C1 L2 requires at least two base-gated entries to become ungated (`|R| >= 2`); L3 requires each such entry's recheck line to be the `r46-c1-gate.py --entry` line; the base recheck lines are `test -d ~/Projects/…` lines that fail on this host (`gated=24`). Therefore each re-grounded entry's bytes must change, and the changed set is at least two of the 64 pinned files. C2's pin covers exactly those files (`base_like` excludes only the F28 path). Any C1 landing with the frozen counters breaks C2 G6.

### F2 (coupling) — C2's recheck form moves C1's gated count

Attacked: C2 entry recheck line. C2 G2 only requires `source-recheck.py` and `--source S073` as substrings in the first eight live lines (`r46-c2-gate.py:193`), so a gated prefix still passes C2.

Command and output, T12g:
```
gate L1 pass=0 read=gated=23 broken=0 lines=65/base=64
gate L2 pass=0 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
c1-gate fixed=5/7 exit=1
gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=6 xrefs=2/2
```
Reason: C1 L1 (`len(gt) <= 22`, `r46-c1-gate.py:180`) and L2 (`not (gt - gb)`, `:182`) count any newly gated entry at the tip. The as-drafted C2 recheck (`cd … && python3 corpus/instruments/source-recheck.py --manifest … --source S073 # 180d`) executes and is not gated (T12 `gated=22`).

### F3 — the 65th entry against C1's `lines >= base` limb and gated count

Attacked: `r46-c1-gate.py:180` (`len(ct) >= len(cb)`), and the gated count.

- Lines limb: with the C2 entry present, C1 reads `lines=65/base=64` (T2 and T12). The limb's inequality holds with one line of slack; it is not moved by C2's landing. It would also hold at `64/64` if the entry had no recheck line.
- Gated count: with an executing recheck, C2 leaves the gated count unchanged (T2 `gated=24`, same as base; T12 `gated=22`). It moves only when the recheck is gated (F2).
- Conclusion: the answer to the coupling question is "no" for the lines limb and "only through the recheck form" for the gated count.

### F4 — C2 touches the lane's expected list, which neither counter grades

Attacked: `corpus/instruments/knowledge-expected.txt` (the recheck-audit expected list; `recheck-audit.py:372` default path).

Command and output, T2x (C2 entry landed, expected-list line not added):
```
expect=present expected=64 missing=0 unexpected=1 exit=1
```
On T2 with the line added: `expect=present expected=65 missing=0 unexpected=0`. Run on the same tree with the line missing (T2x), the C2 counter prints `c2-gate fixed=7/7 exit=0` (`gate G1 … G7 pass=1`, identical to T2), so C2 passes while the lane's own audit goes red. C2 must therefore land the expected-list line; the counter does not check it. C1 adds no entry and touches no expected list.

### F5 — measurement hazard: recheck-audit and score-gap read the live lane, not a tree

Attacked: `recheck-audit.py` `audit_entry` (lines 109-122) runs the whole recheck line, including its `cd <lane> &&` prefix, in the lane. The C1 counter strips that prefix and runs the line in the tree.

Output on the same tree T12:
```
recheck-audit --quiet: executes=41 gated=24 broken=0    (lines=65 total=65 from the tree)
c1-gate L1:           gated=22 broken=0 lines=65/base=64
score-gap (T12):      recheck: lines=65 executes=41 gated=24 broken=0 exit=1
```
The two disagree because `recheck-audit` ran the re-grounded `cd <lane> && python3 corpus/instruments/r46-c1-gate.py --entry …` in the lane, where the re-grounds do not exist. So a copy-tree run of `recheck-audit.py` or `score-gap.py` does not measure C1. The C1 plain check `recheck-audit.py --quiet | grep '^executes='` is valid only on the lane tip after landing. Also noted: `recheck-audit` prints `cdroot_fail=63/64` on any export, as SCORECARD already records.

Score-gap text moves with C2: base `gap: 24 of 64 rechecks still gated …`, T2 `gap: 24 of 65 rechecks still gated …`. C1's "plain" string check therefore changes its denominator when C2 lands (not graded by either counter).

### F6 — C1 draft row-id error (caught and corrected)

First build of the C2-facing contract entry used row ids `C1..C10`. `r46-c1-gate.py:96` (`section_rows`) only recognises `^\|\s*G\d+\s*\|`, so the entry read `rows=0` and T1 read `gated=23 … regrounded=1 … fixed=4/7`. Renumbering to `G1..G10` gave `rows=10 ok=10` and T1 `fixed=7/7`. Any integrator must use `G<n>` ids.

### F7 — the do-nothing controls and freeze controls reproduce

Command: `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/controls/freeze-controls.py --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --base 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba --work <scratch>/controls-work` (writes only to the scratch work dir; reads the lane via `git archive`).

Output tail: `controls total=9 red=9 green=0`, and `diff` of the rerun (91 lines) against `controls/freeze-controls.txt` printed `IDENTICAL`. No frozen control was graded green. The controls do not include a joint C1+C2 tip, so F1 is not caught by any frozen control.

## Shared-surface map (what each claim touches)

| surface | C1 touches | C2 touches | graded by | coupling |
|---|---|---|---|---|
| `corpus/knowledge/claim-gates.md`, `claim-package-contract.md` | yes (recheck line + appended `## Re-ground (round 46)`) | read by G6 pin | C1 L1-L7; C2 G6 | **F1, breaking** |
| new `corpus/knowledge/github-private-vulnerability-reporting.md` (65th entry) | no | yes (new entry + its recheck line) | C2 G2, G5; C1 L1/L2 via recheck | **F2, F3** |
| `corpus/README.md` (F28 row) | no | yes (27→28) | C2 G1; `r44-frontier-count.py --expect 28` | none |
| `corpus/SOURCES.md` (S073 row) | no | yes (S072→S073) | C2 G3, G7 (census) | none |
| `corpus/instruments/knowledge-expected.txt` (= recheck-audit expected list) | no | yes (one line) | lane recheck-audit only, not C2 | **F4** |
| `corpus/source-snapshots/round-46/` (S073.txt, manifest.json) | no (anchors could point here; drafts do not) | yes (already at freeze) | C2 G3, G4, G5 | none |
| `corpus/instruments/claim-package-check.py`, `claim-package-selftest.py` (C1 anchors) | anchors only | no | C1 L6 (mutation) | none (C2 does not edit them) |
| `corpus/instruments/README.md` | not in either draft | not in either draft | not graded | not verified; no r46 counter row exists in base |
| `SKILL.md` (counter registry rows) | not in either draft | not in either draft | not graded | not verified |
| `QUALITY.md` | not in either draft | not in either draft | not graded | none found |
| `claims.json` | none (no counter reads it: `grep` of both counters) | none | freeze record only | none |
| `scripts/sources-census.sh` (fleet) | none | G7 validate | C2 G7 | none |

Only F1 (C1→C2) is a hard conflict. F2 and F4 are conditional conflicts that the author can avoid. The census, snapshots, frontier row and S073 row are not coupled to C1.

## Recipes (drafts; scratch removed on exit, text reproduced in the appendices)

- **Tree F (freeze):** `pure base` copy, then `git -C <lane> archive 9f23aab corpus/instruments/r46-c1-gate.py corpus/instruments/r46-c2-gate.py corpus/source-snapshots/round-46 | tar -x -C F`.
- **C2 draft (T2):** add Appendix A as `corpus/knowledge/github-private-vulnerability-reporting.md` (6,361 bytes); insert the F28 row after the `| F27 |` line of `corpus/README.md`; insert the S073 row after `| S072 |` in `corpus/SOURCES.md`; insert `corpus/knowledge/github-private-vulnerability-reporting.md` into `corpus/instruments/knowledge-expected.txt` before `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`.
- **C1 draft (T1):** in `claim-gates.md` and `claim-package-contract.md`, replace the base `recheck:` line with the `r46-c1-gate.py --entry` line (Appendix B) and append the `## Re-ground (round 46)` section (Appendix B); keep the base line text as history inside the section.
- **Both (T12):** apply both.

Row values verified by reading the committed bytes: `claim-package-check.py` lines 105 (`'custodian-receipts.json',`), 106 (`'provenance.json',`), 127, 129, 131, 140, 305, 308-312, 332, 367, 460, 464, 527-529, 536, 588, 672-674, 689; `claim-package-selftest.py:82` (`(("custodian", "head-mismatch", "head"), "R-CUSTODIAN")`).

Counter detail for the C1 draft (T1): `gate L6 pass=1 read=mutants=19 survivors=none` (9 + 10 rows, every row load-bearing).

Counter detail for the C2 draft (T2): `gate G2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=6 xrefs=2/2`, `gate G5 pass=1 read=spans=10 located=10 failed=0 uncited=0 cores=5/5`, `gate G6 pass=1 read=knowledge=65 base-names-intact=1 entry-bytes-ok=1`.

## Recommendation to the integrator (L1)

The frozen claim set is internally inconsistent at the tip. Options that stay within the frozen rules do not exist; the L1 must decide, and the decision should be recorded before any landing:
1. Re-base C2's G6 pin on the post-C1 bytes. This changes a frozen counter; C2's kill rule forbids that after scoring unless it is declared as erratum with a plain re-derivation.
2. Withdraw or re-scope one claim.
3. Land C1 only after C2 is scored, with C2's score recorded at 7/7 pre-C1 and a stated tip reading of 6/7 — this is the only option that keeps both frozen counters unedited, but the tip still reads C2 6/7.

I did not pick one; that is a decision for the planner (L1).

## Limitations

- I did not run the lane's own selftests (`r46-c*-gate.py` have no selftest; `r45-counters-selftest-*.py` were not run).
- The C1 rows check that each anchored line implements the claim as the committed gate enforces it. That is a reading by me, not a non-author semantic check, which the kill rule also requires.
- The C2 entry quotes are located in the pinned capture. I did not re-open the live GitHub page; the non-author closure is not performed here.
- `recheck-audit` and `score-gap` read the live lane for `cd`-prefixed lines (F5); tree numbers from them are not tree measurements.
- The host has no `~/Projects/bounties`; a host where that path exists would change the gated count of the base lines without any edit. Not tested.
- The drafts are my recipe, not committed; they are reproducible from the appendices and recipes above.
- Nothing was committed, pushed, or changed in git. Read-only `git archive`, `git show`, `git ls-tree`, `git grep`, `git status` only. Scratch removed on exit. No tools installed.

## Appendix A — C2 draft entry (`corpus/knowledge/github-private-vulnerability-reporting.md`)

```
# GitHub private vulnerability reporting (reporter flow)

source: S073 — https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately — section anchors: Privately reporting a security vulnerability (S073.txt:556-578); capture at `corpus/source-snapshots/round-46/S073.txt`, manifest `corpus/source-snapshots/round-46/manifest.json`.
verified-at: 2026-10-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073 # 180d

## Scope and decision rule

This entry records one upstream platform's reporting flow: GitHub's own page on private vulnerability reporting, meaning the reporter-side form that a public repository's maintainers can enable for their repository. It governs one report filed through that form to the repository's maintainers. It is not the repository's own advisory-publishing workflow, not the global advisory database, and not a rule for any other project or platform.

The page's core statement is “Anyone can privately report a security vulnerability to repository maintainers.” (`S073.txt:560`). Enablement is per repository: “Owners and administrators of public repositories can enable private vulnerability reporting on their repositories.” (`S073.txt:561`).

Decision rule: a package may describe a report as filed through this flow only when the target repository shows the feature enabled and the report carries the form's fields. Where the feature is off, the page routes the reporter elsewhere (row 2 of the table). A package may not describe the reporter as able to merge a fix: only the maintainer merges from the temporary private fork.

| observed question | page text | package consequence |
|---|---|---|
| Is this flow open for this repository? | “You can only report vulnerabilities privately for repositories where this feature is enabled.” (`S073.txt:564`) | Name the repository and confirm the feature is on for it; a report to a repository without it is not filed through this flow. |
| Where does a reporter go when the feature is off? | “you need to initiate the reporting process by following the instructions in the security policy for the repository” (`S073.txt:566`) | Use the repository's security policy or its request for a preferred contact; do not describe a submission to the private form. |
| Which fields must the report carry? | “By default, you must provide a summary, details, proof of concept, and impact statement.” (`S073.txt:573`) and “Maintainers can customize the form and require other information.” (`S073.txt:573`) | Carry all four default fields, and check the form the repository actually shows, because the maintainer may change it. |
| Is AI assistance declared on the form? | “Optionally, select I used AI assistance to find or write up this report.” (`S073.txt:574`) | The mark is optional, so the package states whether it was selected; an unselected mark does not by itself establish that no AI assistance was used. |
| Who is added to the advisory on submission? | “GitHub automatically adds the reporter of the vulnerability as a collaborator and as a credited user on the proposed advisory.” (`S073.txt:577`) | Record the automatic collaborator and credited-user status; do not describe credit as a separate step the report must request. |
| Who merges a temporary private fork? | “only the repository maintainer can merge changes from that private fork into the parent repository” (`S073.txt:578`) | A reporter's temporary private fork may carry a fix; the package states that only the maintainer merges it. |

## Overlap and novelty

The frontier before this round holds F25 (CVE record format), F26 (Google Cloud VRP scope) and F27 (the Linux kernel's e-mail reporting process), plus F04 (AI-assisted finding validation). None of them describes the reporter-side form of a platform's built-in private reporting channel, so this entry adds coverage rather than restating those rows.

The nearest rows are contrasts, and they are stated here rather than inherited. The kernel process refuses AI-found reports (F27, `corpus/README.md`); the captured GitHub section contains no refusal rule and asks only for the optional disclosure mark (`S073.txt:574`). F04 treats an AI-originated finding as a candidate until human validation is recorded (`corpus/knowledge/ai-assisted-finding-validation.md:7`); the GitHub form collects a report and does not validate its finding.

The page also separates this flow from the repository's policy file: “Private vulnerability reporting is separate from a repository’s SECURITY.md file.” (`S073.txt:564`). The kernel's decision rule (`corpus/knowledge/linux-kernel-security-bugs-reporting-process.md:13`) uses a different channel, an e-mail list, so the two rules are not interchangeable.

## Limits

- The capture is one page fetched 2026-10-28T22:56:49Z (manifest S073). The UI labels the page uses, such as the Security and quality tab and the Report a vulnerability button, are as captured and may move.
- The field list is the default only. The page says maintainers can customise the form, so a repository's actual form may ask for more or different fields.
- The page says the next steps depend on the action the repository maintainer takes (`S073.txt:579`). It gives no response times and no maintainer procedure, and this entry states none.
- The entry does not verify that any named repository has the feature enabled; that per-repository check belongs to each package.
- The entry makes no claim about the global advisory database, about repositories that disable the feature, or about any other GitHub product.

## Falsifiable package rule

A package that describes a report through this flow must (a) name the repository and show that the feature is enabled on it, (b) carry the four default fields or the fields of the form shown, (c) state whether the optional AI-assistance mark was selected, and (d) state that only the maintainer merges from the temporary private fork.

The rule is falsified by a later capture of the same page in which one of the five quoted sentences is absent or changed. The recheck line verifies the pinned capture only; a change on the live page is caught only by a new capture and a new manifest row.
```

Companion rows (exact):
- `corpus/README.md`, after the `| F27 |` line:
  `| F28 | GitHub private vulnerability reporting: the reporter-side form a public repository enables for its own advisories — feature enabled per repository only, four default fields, optional AI-assistance mark, automatic collaborator and credit, only the maintainer merges the temporary private fork | admitted | knowledge/github-private-vulnerability-reporting.md | S073 | Route a report through this form only where the repository shows the feature enabled; otherwise follow its security policy, and state the fork-merge limit in any package. |`
- `corpus/SOURCES.md`, after the `| S072 |` line:
  `| S073 | GitHub Docs, Privately reporting a security vulnerability — https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately | docs | A | Reporter-side private vulnerability reporting flow on a public repository's advisory form, from the page's own text only | section Privately reporting a security vulnerability S073.txt:556-578; capture sha256 66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930 (manifest S073; fetched 2026-10-28T22:56:49Z; 589 lines) | Report only where the feature is enabled; default fields; optional AI-assistance mark; automatic collaborator and credit; only the maintainer merges the private fork | mined | 2026-10-28 | 180d | corpus/knowledge/github-private-vulnerability-reporting.md |`

## Appendix B — C1 draft (`claim-gates.md`, `claim-package-contract.md`)

Replacement recheck line (both entries; `<entry>` = file name):
`recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<entry>  # round-46 re-ground: runs on its own rows; base line kept in the Re-ground section`

Appended section (intro shared by both entries): `Re-ground on committed bytes (round 46, C1). Each row states one claim of this entry as the committed gate implements it, anchored at the committed line that implements it. The anchors are the round-43 gate and its fixtures, not the lost claimant tree this entry was read from: a row supports a claim only as far as the anchored line enforces it.`

`claim-gates.md` rows (9; files: `claim-package-check.py`, `claim-package-selftest.py`):

| id | current claim | committed anchor | token |
|---|---|---|---|
| G1 | the manifest carries a numeric `sequence` and a 64-hex `expected_head_sha256`; a bad value fails R-MANIFEST | `corpus/instruments/claim-package-check.py:308-312` | `expected_head_sha256` |
| G2 | a custodian decision whose `scope_signal` is not exactly `NO_SCOPE_OBJECTION` counts as a signal error | `corpus/instruments/claim-package-check.py:460` | `NO_SCOPE_OBJECTION` |
| G3 | the per-file size cap is 5 MiB | `corpus/instruments/claim-package-check.py:131` | `MAX_SCAN_BYTES = 5 * 1024 * 1024` |
| G4 | a file over the cap is counted as oversize and is not read for secrets | `corpus/instruments/claim-package-check.py:672-674` | `st.st_size > MAX_SCAN_BYTES` |
| G5 | a labelled credential (api key, secret, token or password followed by a 16-character value) matches the credential pattern | `corpus/instruments/claim-package-check.py:140` | `\b(?:api[_-]?key` |
| G6 | `manifest_sha256` must equal the sha256 of the manifest bytes; any other value fails R-STATUS | `corpus/instruments/claim-package-check.py:588` | `recorded.lower() != actual` |
| G7 | a package must contain the six contract files, among them `custodian-receipts.json` | `corpus/instruments/claim-package-check.py:101-108` | `custodian-receipts.json` |
| G8 | the subchecks `no_secrets` and `operator_attribution` must be present and PASS | `corpus/instruments/claim-package-check.py:129` | `operator_attribution` |
| G9 | a custodian head mismatch is a fixture the selftest expects to fail under R-CUSTODIAN | `corpus/instruments/claim-package-selftest.py:82` | `head-mismatch` |

`claim-package-contract.md` rows (10; files: `claim-package-check.py`, `claim-package-selftest.py`):

| id | current claim | committed anchor | token |
|---|---|---|---|
| G1 | the six contract files include `provenance.json` | `corpus/instruments/claim-package-check.py:106` | `provenance.json` |
| G2 | the manifest `schema_version` must be `evidence-manifest/v1` | `corpus/instruments/claim-package-check.py:305` | `evidence-manifest/v1` |
| G3 | at least one artifact has polarity `positive` | `corpus/instruments/claim-package-check.py:332` | `artifact.get('polarity') == 'positive'` |
| G4 | `redactions` must be non-empty; `redactions:[]` is not claim-ready | `corpus/instruments/claim-package-check.py:367` | `redactions=empty` |
| G5 | every custodian decision's `scope_signal` must be exactly `NO_SCOPE_OBJECTION` | `corpus/instruments/claim-package-check.py:460` | `NO_SCOPE_OBJECTION` |
| G6 | the custodian head is read from `head_sha256` and bound to the manifest head | `corpus/instruments/claim-package-check.py:464` | `document.get('head_sha256')` |
| G7 | `external_effects_performed` must be an empty list | `corpus/instruments/claim-package-check.py:527-529` | `external_effects_performed=not-empty` |
| G8 | a secrets attestation that is absent or not affirmative fails | `corpus/instruments/claim-package-check.py:536` | `secrets_attestation=not-affirmative` |
| G9 | `status.json` `manifest_sha256` must match the manifest bytes | `corpus/instruments/claim-package-check.py:588` | `recorded.lower() != actual` |
| G10 | a head-mismatch fixture must fail the custodian rule | `corpus/instruments/claim-package-selftest.py:82` | `head-mismatch` |

Counter result for both re-grounds on T1: `gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64`, `gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md`, `gate L6 pass=1 read=mutants=19 survivors=none`, `c1-gate fixed=7/7 exit=0`.

## Appendix C — exact commands run (all read-only w.r.t. the lane)

- `git -C <lane> archive 914ca0b6… corpus …` / `… archive 9f23aab4… corpus/instruments/r46-c1-gate.py corpus/instruments/r46-c2-gate.py corpus/source-snapshots/round-46 | tar -x -C <scratch>`
- `git -C <lane> ls-tree -r --name-only 914ca0b6…`, `git -C <lane> diff --stat`, `git show --stat 323d1f5`, `git grep … 914ca0b6…` (read-only)
- `python3 <lane>/corpus/instruments/r46-c1-gate.py --root <tree> --baseline <base>` and `python3 <lane>/corpus/instruments/r46-c2-gate.py --root <tree>` for base, F, T1, T2, T12, T12g
- `python3 <lane>/corpus/instruments/recheck-audit.py --root <tree> --quiet`; `r44-frontier-count.py --root <tree> --expect 28`; `score-gap.py --root <tree>`
- `python3 <lane>/.ufo/waves/round-46/controls/freeze-controls.py --lane <lane> --base 914ca0b6… --work <scratch>/controls-work`, diffed against `controls/freeze-controls.txt` → IDENTICAL
