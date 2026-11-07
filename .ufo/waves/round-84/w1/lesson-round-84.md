# Round 84 — lesson (kasegi, attempt 1) — DRAFT for the L1

One v1 wave of 12 seats. This file is the scribe draft: § Claims records the frozen claims verbatim, § Gate records the S118 registry row and one located quote, § Mistakes carries M84-1 (executed) and M84-2 (fix marked PENDING-L1-EVIDENCE for the L1 to replace), § Routed-defect disposition maps the eight r83 spot-check defects onto this round's claims. Nothing here is a verdict; the L1 owns every verdict and every landing value.

## Claims

Freeze `7f76b7eb690cd6e75e7f3e7729cedcb15611b34b` (base `a089ff3d601b4d53a5515e52720ba27e5ec72c3d`), file `.ufo/waves/round-84/claims.json`, sha256 `30f9355c079677f0a3f8f0555d396bda51c380d45f169ddb2caddf694ae47906` — re-measured equal to the blob at the freeze commit (`git show 7f76b7eb:.ufo/waves/round-84/claims.json | sha256sum`; receipt `ScribeLesson-receipts/gate-row.txt`). Both statements are quoted verbatim from that file; the pointers name the key path so the L1 can diff the quote against the JSON.

- **C1 — depth:verifiability** (`.claims[0]`; predicates `.claims[0].predicate.P1`–`P8`; kill rule `.claims[0].kill_rule`; do-nothing `.claims[0].do_nothing`; axis score `.claims[0].axis_score`). Statement, verbatim:

  > The round-84 recheck-cwd successor, landed byte-identical to the frozen candidate, is killed on its declared check by all 76 non-neutral rows of the 79-row r84 table - including the twelve round-83 MutC1Hunt survivors H01-H12 that the landed r83 bytes and a check-name stub both let survive - passes its 3 neutral rows and the keyed decoys, and is conformant on the lane tree; and the r84 counter's selftest fails on three counter mutants (M09 extra not applied, M10 extra uniqueness dropped, M12 DECOY line dropped) that the r83 counter's selftest passes. Not claimed: the F8/F12/F13 forgery class (recorded limits carried from r83).

- **C2 — coverage** (`.claims[1]`; predicates `.claims[1].predicate.B0`–`B8`; kill rule `.claims[1].kill_rule`; do-nothing `.claims[1].do_nothing`). Statement, verbatim:

  > Admit Frontier F60, corpus/knowledge/osv-gcs-data-dump-layout.md, on the six pinned export-layout clauses of S118 (the full zip includes withdrawn records, the per-record JSON path, the [EMPTY]/ directory, the per-ecosystem modified_id.csv prefix rule, colon-suffixed ecosystems folded into the base directory, the stopped prefixed exports), moving FRONTIER-CENSUS rows 59 -> 60 and corpus/knowledge 97 -> 98 while S118 moves queued -> mined and no other registry row changes; the entry passes the round-83 entry gate unchanged.

Frozen artifact hashes the claims pin (read from `.claims[0]`/`.claims[1]`, not re-measured by this seat): candidate `e5f2e4bd…cf179e`, counter `c67e6912…38d6ea`, table `daf05baca…677aa9e`, builder `4352368e…4a7516`, S118 snapshot `e824a735…fa5359`, r83 gate `42f4b2ac…ace6302`.

## Gate

### C2 — coverage — F60 on the OSV.dev Data sources page (S118)

Scope of this section: the C2 registry row (S118) only. C1's P1–P8 are measured by the L1's landing receipt, not here; this seat ran no predicate.

In one sentence: Frontier F60 is admitted on six pinned export-layout clauses of the OSV.dev Data sources page (S118) — the full-database zip that includes withdrawn records, the per-record JSON path, the `[EMPTY]/` directory for ecosystem-less records, the per-ecosystem `modified_id.csv` rows that omit the directory prefix, colon-suffixed ecosystems folded into their base directory, and the stopped prefixed exports — with the row's status and used-by cells moving at landing and no other registry row changing.

**Registry row S118** (`corpus/SOURCES.md:130`; column header at `:5` is `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`). The row is still `queued` in the frozen commit and in the worktree at this draft's measurement instant (`git diff 7f76b7eb -- corpus/SOURCES.md` prints nothing); the landing change is old → new as tabulated:

| cell (row split by `tr '\|' '\n'`: field 1 and field 13 are the empty leading/trailing fields, so field *n*+1 is header column *n*) | old (freeze `7f76b7eb`, = worktree at this draft) | new (landing target) |
|---|---|---|
| status (field 9) | `queued` | `mined` |
| used-by (field 12) | `—` | `corpus/knowledge/osv-gcs-data-dump-layout.md` |
| opened (field 10) / recheck (field 11) | `2026-11-06` / `90d` | unchanged |
| source / kind / tier | `OSV.dev, Data sources (OSV project) — https://google.github.io/osv.dev/data/` / `docs` / `A` | unchanged |

**Access record** (`corpus/source-snapshots/round-84/manifest.json`, sha256 `80129310e4880f857a0c2225f028ac8e5985ceff21ad5d5496c1867a7de0a65a`; snapshot sha re-measured equal to the freeze blob):

| field | value |
|---|---|
| url / capture_url / final_url | `https://google.github.io/osv.dev/data/` (all three equal) |
| access date | 2026-11-06 (`fetched_utc 2026-11-06T23:34:49Z`) |
| http.status | `200` |
| kind | `html` |
| fetch_method | `capture-source.py --kind html`, default instrument UA; tags stripped, entities decoded, whitespace collapsed per line; raw page 27419 bytes, snapshot 5820 bytes |
| snapshot sha256 | `e824a73545bedd0abae5f84cd120a5c73e482d7e935bc1534a08a1e1adfa5359` |
| lines / quotes | 129 / 6 |

**One located quote (≤25 words), from the six the manifest pins:**

| clause | manifest pin | snapshot line | words | located quote |
|---|---|---|---|---|
| cl1 full zip includes withdrawn records | `Q01-allzip-withdrawn` | `S118.txt:102` | 17 | This bucket contains a zip file with all vulnerabilities across all ecosystems (including withdrawn records) at gs://osv-vulnerabilities/all.zip. |

`grep -n -F` over `S118.txt` finds it once, on line 102; that line additionally carries one following sentence ("This is the easiest way to download the entire OSV database."), so the whole line is 28 words while the pinned quote is 17 (`len(quote.split())`). The other five pins sit at `:104` (Q02, Q03), `:114` (Q04), `:121` (Q05) and `:123` (Q06), each `occurrences=1` with `anchor=<n>-ok` in `.ufo/waves/round-84/controls/c2-prefreeze-r84.txt`.

**State at this draft's measurement instant.** The entry `corpus/knowledge/osv-gcs-data-dump-layout.md` is an untracked worktree draft (98 lines, sha256 `0f9c1486db7756020b935060052ee55455be905da1bc4c0089d1cc816b2b7552`, `git status` shows `??`); the r83 entry gate (sha256 `42f4b2accf704455325f8d1eb8ca4ec21401e35397af7a36861c33a27ace6302`, unchanged) prints `ENTRY-GATE sid=S118 claims=6 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 untied=0 header=ok` / `ENTRY-GATE-RESULT pass` rc 0 over it, and the do-nothing state is `FRONTIER-CENSUS rows=59 admitted=59 closed=59 problem-rows=0 registry=118`, tracked knowledge 97 (`ls corpus/knowledge/*.md | wc -l` prints 98 only because the untracked draft is on disk), S118 `queued` (`controls/c2-prefreeze-r84.txt`; `controls/c2-draft-v0-r84.txt` for the failed predecessor draft below).

- **considerthese:** L1 fills.
- **Assimilation:** L1 fills.
- **Rejected (R119):** none this round — carried rejects named: "Managing the Perishability of OSV Records" (the r82 lead rejected in r83 for having a title and no public copy; flip condition unchanged — a captured public copy at a registry URL whose quotes locate), carried as `corpus/lessons/round-83.md` § Gate, C2 reject row.

## Mistakes

### M84-1 — `rule-paraphrase-drifts-from-quote-vocabulary`

The L1's first F60 draft wrote two of the six falsifiable rules in synonyms of the clause instead of the quote's own nouns, and the round-83 G6 tie limb — lexical by construction (M83-2, QUALITY R134) — scored both `untied`. The inference in each v0 rule is the same as the landed rule's; only the vocabulary moved, and that was enough to lose the stem tie to the pinned span. The two hunks, verbatim from `.ufo/waves/round-84/controls/c2-draft-v0-r84.txt` (v0 on the `<` side, landed on the `>` side):

```
17c17
< Falsifiable rule: a count of advisories taken from the full OSV zip overstates the live set unless the counter drops entries whose withdrawn field is set, since that archive carries withdrawn ones as well (S118.txt:102). A reader checks it by reading the first sentence under "Full database download".
---
> Falsifiable rule: a count of vulnerabilities taken from the full OSV zip overstates the live set unless the counter drops records whose withdrawn field is set, since that archive carries withdrawn records as well (S118.txt:102). A reader checks it by reading the first sentence under "Full database download".
41c41
< Falsifiable rule: a parser written for the top-level modified_id.csv that splits the second column on a slash breaks on a per-ecosystem file, whose rows give the bare identifier without the directory part (S118.txt:114). A reader checks it by reading the two sentences under "Format and Usage".
---
> Falsifiable rule: a parser written for the top-level modified_id.csv that splits the second column on a slash breaks on the per-ecosystem files, whose rows omit the directory prefix and give the bare identifier (S118.txt:114). A reader checks it by reading the two sentences under "Format and Usage".
```

The drift is visible in the diff alone: "advisories"/"entries" become the quote's "vulnerabilities"/"records" (the Q01 quote says "all vulnerabilities … (including withdrawn records)"), and "file … without the directory part" becomes "files … omit the directory prefix" (Q04: "The per-ecosystem files omit the <ecosystem_dir>/ prefix."). This is the M83-2 false-positive face recurring on this round's own draft: a sound rule can fail a lexical limb, so the limb is not evidence about rule quality (R134), and the repair is editorial — the gate bytes are unchanged (`42f4b2ac…`), defect 4 below stays carried.

**Evidence pointer.** `controls/c2-draft-v0-r84.txt` ends `ENTRY-GATE sid=S118 claims=6 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 untied=2 header=ok` / `ENTRY-GATE-RESULT fail` / `rc=1`; the landed rules in `controls/c2-prefreeze-r84.txt` print `… ruleless=0 untied=0 header=ok` / `ENTRY-GATE-RESULT pass` / `rc=0` (B8 likewise pins the pass).

**Captured-by: entry-gate G6 (r83).** G6 is the limb that raised it; no QUALITY row binds a rule's vocabulary to its quote.

**Fix, shown able to fail and pass:** the G6 run before freeze — the v0 receipt is the failing side (rc 1, `untied=2` on the two paraphrased rules) and the landed receipt is the passing side (rc 0, `untied=0`), both over the same gate bytes and the same manifest.

### M84-2 — `landing-receipt-measured-over-pre-commit-worktree`

The r83 landing receipt (`.ufo/waves/round-83/l1/L1-landing-r83.txt`, header `2026-11-06T23:23:32Z`) was measured over the uncommitted worktree before landing commit `795f24da`; the r83 non-author spot-check records it as conformance note (b) and routed defect 7 (`corpus/lessons/round-83-verifier-spotcheck.md` § 1 and § 6). The class is not "a wrong measurement" but "a measurement of bytes that are not the cited commit's bytes": every predicate the receipt prints can be true of a tree that never lands, and a later edit to the same worktree (here: the lane's own landing edits) invalidates the receipt without changing any printed line.

**Evidence pointer.** `corpus/lessons/round-83-verifier-spotcheck.md` § 6 defect 7 ("Landing receipts must be measured over the cited commit (or carry its hash), not a pre-commit worktree"); § 1 note (b) names the pre-commit header time.

**Captured-by: the r83 non-author spot-check's conformance note (b)** — a spot-check observation, not a QUALITY row.

**Fix (PENDING-L1-EVIDENCE):** the landing receipt re-run over `git archive` of the landing commit into scratch, so every printed predicate reads the committed bytes and the receipt header carries the commit hash. The L1 replaces this marker with the r84 receipt path and its commit line.

## Routed-defect disposition (r83 spot-check, defects 1–8)

Dispositions follow `claims.json` `.history_read` (the freeze's own statement of what was routed in), and each pointer names the claim key or receipt the L1 can read; nothing here is executed by this seat.

| # | r83 routed defect | r84 disposition | pointer |
|---|---|---|---|
| 1 | C1 counter: F12 (marker-aware) and F13 (comment-stripping count) pass the r83 counter; adopt the rename-based D3 decoy or declare both beside F8 and add them to `mutbat --selftest` | **carried, not claimed** — C1 declares the forgery class out of scope (`Not claimed: the F8/F12/F13 forgery class`); no new forgery control this round | `.claims[0].statement` (Not claimed sentence); `controls/c1-candidate-r84.txt` |
| 2 | P3 reads only the `MUTBAT` summary suffix, which the target controls; add a per-row verdict or `target_sha256` limb | **answered** — P3 now binds `target_sha256=e5f2e4bd…` in the summary line and counts the counter's own per-row `MUTANT` lines: 76 `KILLED\|EXCEPTION-KILL`, of which 12 are `H01`–`H12` | `.claims[0].predicate.P3` |
| 3 | Counter selftest does not exercise the `extra` limb (MutCounter M09) | **answered** — the r84 selftest limbs `extra`/`dup`/`decoy_line`; `COUNTER-MUTANT M09, M10, M12` each print `rc=0 selftest=ok` under `counter=r83` and `rc=1 selftest=FAIL` under `counter=r84` | `.claims[0].predicate.P4`, `.predicate.P5`; `controls/c1-counter-mutants-r84.txt` |
| 4 | Entry gate G6 is lexical: six echo rules pass and admitted F57 fails (`untied=1`); land a non-lexical tie per R134, and record F57's G6 status | **carried, not claimed** — C2 reuses the r83 gate unchanged (B8 pins `42f4b2ac…`); this round's own draft hit the false-positive face again (M84-1), so the limb is still a heuristic and its pass is not cited as rule quality | `.claims[1].predicate.B8`; § Mistakes M84-1 |
| 5 | MutEntryGate 8/16 survivors (6 behaviour-changing); MutC1Hunt r83 gaps | **half answered** — the MutC1Hunt half is closed as rows `H01`–`H12` (unchanged anchor/replacement bytes) plus six new checks `noprefix-only`, `summary-fields`, `entry-bare-pass`, `argv-values`, `verbose-order`, `entry-set`; the MutEntryGate survivors are not named in `history_read` and are carried | `.claims[0].candidate`; `.claims[0].predicate.P7`; `controls/c1-donothing-r84.txt`, `controls/c1-stub-r84.txt` |
| 6 | `comment_lines` latent f-string issue (ReviewC1 Major 1) | **carried, not claimed** — latent (fails loud, never a false pass); no f-string in this round's candidate and no predicate binds it | `.history_read` ("defect 6 (comment_lines f-string, latent)") |
| 7 | Landing receipts must be measured over the cited commit (or carry its hash), not a pre-commit worktree | **applied procedurally** — `history_read` states the landing receipt is re-run over the landing commit's bytes via `git archive`; M84-2 records the class and its fix, whose r84 execution is the L1's to evidence | `.history_read`; § Mistakes M84-2 |
| 8 | Carried from r82: defect 4 partly answered, 5 and 7 carried | **carried** — the same r82 items stay open behind rows 4, 5 and 7 above; no r82 defect is re-measured this round | `corpus/lessons/round-83.md` § Routed-defect disposition (rows 4, 5, 7) |

## Landing values (L1)

Values that exist only at landing are measured by the L1, not written here: P1–P8 and B0–B8 as printed at the landing commit, the S118 registry-row diff (old → new above), the tracked-knowledge and FRONTIER-CENSUS deltas, the landing commit hash, the `## Gate` considerthese/assimilation lines, and the M84-2 fix evidence. R133 check after the L1's edits: `awk '/^## Gate/{g=1} /^## Mistakes/{g=0} g' <lesson> | grep -c -E 'PENDING-L1\|TBD\|TODO'` must print 0.
