# ConnectorOverlap — round 84 v1 (cross-lane / cross-source overlap, considerthese, assimilation ids)

Seat: connector. Axes touched: coverage (F60's ground) and depth:verifiability (F60's provenance surface).
Read-only everywhere except this wave dir and scratch `/fast/scratch/hyaku/kasegi-r84/ConnectorOverlap` (deleted at exit).
Freeze `7f76b7eb690cd6e75e7f3e7729cedcb15611b34b`, base `a089ff3d601b4d53a5515e52720ba27e5ec72c3d`.

---

## 1. Sibling lanes hold none of F60's ground

Command (all 20 sibling lanes, lane-excluded):

```sh
cd /home/vgpnk/Projects/shokunin
for d in *-shokunin; do [ "$d" = kasegi-shokunin ] && continue
  grep -rIl -E 'osv\.dev/data|osv-vulnerabilities|all\.zip|modified_id\.csv|\[EMPTY\]' "$d/corpus/knowledge"
  grep -nE  'osv\.dev/data|osv-vulnerabilities|all\.zip|modified_id\.csv|\[EMPTY\]' "$d/corpus/SOURCES.md'
done
```

Result: three hits, all false positives for a **different marker**, all in `mado-shokunin`:

- `mado-shokunin/corpus/knowledge/config-health-report-r3.md:541`, `:824`;
  `hyprctl-verification-layer.md:127`; `hyprland-input-devices-r46.md:32` — these match `[EMPTY]`,
  but in the Hyprland STRVAL_EMPTY sense (`| input:accel_profile | [[EMPTY]] | unset | live-default |`),
  not the OSV `gs://osv-vulnerabilities/[EMPTY]/` directory.

No sibling `SOURCES.md` carries `osv.dev/data`, `osv-vulnerabilities`, `all.zip` or `modified_id.csv`.
Broadening to the token `osv` in sibling registries, the only row is kaidoku's one CVE record:

```
kaidoku-shokunin/corpus/SOURCES.md:21: | S015 | OSV CVE-2025-55305 record — https://api.osv.dev/v1/vulns/CVE-2025-55305 | dataset | A | ...
```

and `grep -rl 'gs://osv-vulnerabilities\|osv-vulnerabilities\|OSV.dev' */corpus/knowledge | grep -v kasegi` is empty.
The r83 reading holds and is unchanged: **kaidoku S015 is one CVE's API record — a different document
(api.osv.dev `/v1/vulns`, not the Data sources page) and a different proposition (that CVE's affected
ranges), no bucket layout.** Kaidoku Q142/Q143 are source-novelty criteria, not ground.
Verdict: **F60 duplicates no sibling's held ground**, and no sibling frontier row names the OSV GCS dump.

Second-order effect: no sibling can absorb an S118 capture or quote; the six manifest quotes are
unique to this lane, which is what B6's literal sweep can only prove lane-internally.

## 2. Lane-internal citers of S117/S116/S115/S108, and F60's overlap

`grep -rln -E 'S117|S116|S115|S108' corpus/knowledge/` → 9 files:

| entry | cited id | role of the citation | overlap with F60's six claims |
|---|---|---|---|
| `osv-faq-post-import-record-lifecycle.md` (F59) | S117 | primary source | **adjacent on cl1 and cl4 — see below** |
| `osv-gcs-data-dump-layout.md` (F60) | S117/S116/S115/S108 | its own Distinctness block | self |
| `osv-high-quality-record-import-bar.md` (F58) | S116 | primary | none (import bar; `Not claimed` at `:70` excludes the companion doc, nothing about the bucket) |
| `osv-importfindings-record-quality-feedback.md` (F57) | S115 | primary | none (`:61` names F51 only as distinctness) |
| `osv-post-v1-query-contract.md` (F51) | S108 | primary | none (query endpoint) |
| `osv-post-batch-query-contract.md` (S112) | S108 | distinctness `:53-54` | none |
| `osv-determineversion-cc-library-versioning.md` (S113) | S108 | distinctness `:77-79` | none |
| `osv-ubuntu-binary-to-source-mapping.md` (S114) | S108 | distinctness `:61` | none |
| `fuzzilli-ndss2023-jit-fuzzing-paper.md` | S117 | **cross-lane id, not this lane's S117** | none |

`fuzzilli-ndss2023-jit-fuzzing-paper.md:42` — "Revenger's tool-documentation rows, DecFuzzer (S117)
and mishegos (S396) in ../revenger-shokunin/corpus/SOURCES.md, are not used." That is revenger's
id space; nothing to do with kasegi S117 (the OSV FAQ).

### The one real adjacency: F59

F59's Claim 5 (`corpus/knowledge/osv-faq-post-import-record-lifecycle.md:47`):

> The file sits at the root of the GCS bucket, with rows formatted
> `<iso modified date>,<ecosystem_dir>/<id>` (S117.txt:94-98), **and a per-ecosystem copy sorted in
> reverse chronological order** (S117.txt:99-100; Q05 pins line 94 only).

F60's Claim 4 pins S118.txt:114 ("The per-ecosystem files omit the `<ecosystem_dir>/` prefix.").
These share the **existence** of a per-ecosystem `modified_id.csv` and nothing else: F59 states the
top-level row format plus the per-ecosystem file's sort order; F60 states that the per-ecosystem
rows drop the directory prefix. F59 already fences this:

> `:71` — Not claimed: … the per-ecosystem modified_id.csv and its sort order (S117.txt:99-100)
> beyond Claim 5's paraphrase …

So the fence is drawn on the **sort order**, not on "the file exists". F60's cl4 is the row-field
rule, which no entry states. Not a duplicate; it is the one sentence pair a reviewer should check,
because the two entries describe the same artifact from two documents.

F59's Claim 2 (`:23`) says "the GCS exports with the withdrawn field (S117.txt:115-118)" and F60's
Claim 1 pins S118.txt:102 (all.zip includes withdrawn records). Both assert withdrawn records appear
in the GCS exports; F59's pin is a by-ID-API answer that mentions exports in passing, F60's pin is
the archive-composition sentence. Different sentence, different proposition (retrieval vs archive
contents). State it as adjacency, not contradiction: neither entry says the other is false, and
F60's "Distinctness" already says it "does not restate the top-level format or the sort order".

Residual risk worth naming (routed, not a defect claim): predicate **B6 is a literal sweep over the
six pinned quotes** (0/97 today). It cannot see a *propositional* overlap such as the cl4/F59-cl5
pair — the two sentences are lexically disjoint. Same class as the r83 defect 2 lesson (a check that
reads only the summary suffix). The F60 draft's Distinctness paragraph is the only control on that
overlap, and it is prose, not a predicate.

## 3. considerthese 2026-10-26 — proposal status, and the one still open

Latest file is still `considerthese/2026-10-26.md` (no newer file in `considerthese/`). Status of its
seven proposals, checked against `corpus/QUALITY.md`, `SCORECARD.md`, `PROVINCE.md`, `SHONEN.md`,
`corpus/instruments/` and `corpus/lessons/round-{36,38,41,47,59,60,61}.md`:

| # | proposal | status | evidence |
|---|---|---|---|
| 1 | distance-to-next-score criteria in §Saturation | **implemented r39** | `SCORECARD.md:1534` ("Mined from considerthese 2026-10-26 proposal 1 … landed in round 39"), `### coverage, 7 → 8` at `:1547`; per-round reading is an L1 obligation (`:1389`, `:1465`) |
| 2 | one end-to-end domain task round, minimal claim checker | **half implemented** | checker landed r43: `corpus/instruments/claim-package-check.py` (802 lines, 8 rules, `--selftest`). The **task itself is not run**: `SHONEN.md:7` box 2 `[ ]`, evidence `corpus/lessons/round-61.md` |
| 3 | quiescence gate before `complete` | **implemented** | `corpus/QUALITY.md:263` R28 (porcelain empty + no leftover seat scratch dirs); `corpus/instruments/r46-landing-gate.py:20,113-115` `tree-clean` |
| 4 | cap / externalise wave evidence | **open** | `corpus/lessons/round-47.md:85` ("4's externalisation … remain open"); operator/LFS decision, not a lane move |
| 5 | land the owed F18 PROVINCE amendment | **implemented r36** | `PROVINCE.md:77` "[r36 Frontier amendment …] F18 — CISA Known Exploited Vulnerabilities" |
| 6 | re-tune considerthese cadence/depth | **recorded, no change** | `corpus/lessons/round-36.md:39` item 6 |
| 7 | proposal-status ledger | **implemented** | `corpus/knowledge/considerthese-proposals-ledger.md` + `corpus/QUALITY.md` R31 |

**The one still-unimplemented proposal that fits this round's surfaces: proposal 2's remaining half —
run one end-to-end domain task and log it (SHONEN box 2).**

What it points at: `SHONEN.md:7` ("At least one end-to-end domain task executed and logged in LOG.md",
`[ ]`, last evidence `corpus/lessons/round-61.md`), the contract it must satisfy
`corpus/knowledge/claim-package-contract.md` (six files), the checker already built for it
`corpus/instruments/claim-package-check.py`, and the pricing tables it is supposed to exercise
(F13 severity ladders, F17 Immunefi VSCS v2.2, F18 KEV).

Fit, stated honestly: it fits **C1** (an instrument that has never been run on a real package is
verifiability asserted, not shown — exactly the r84 C1 premise that a gate must be seen to fail) and
it **uses** C2's frontier (F13/F17/F18) rather than admitting a new row, so it does not move
coverage's operator-owned denominator. Proposals 4 and 6 fit neither surface (substrate cost and
process cadence, both operator-owned).

## 4. Assimilation id check (read-only on shokuknow)

Exact prompt commands (section 6 item 10, 0–3-space pattern), output in
`.ufo/waves/round-84/w1/ConnectorOverlap-receipts/assimilation/`:

| measure | value |
|---|---|
| `reg-ids` (`corpus/SOURCES.md`) | **118** ids, S001..S118 |
| `staged-ids` (`merge/kasegi/SOURCES.append.md`) | **94** ids, S031..S124 |
| `comm -12` → `collisions` | **88** ids, contiguous **S031..S118** |
| `doc-collisions.txt` | `same_url=1 diff_or_urlless=87` |
| `guard-proof-collisions.txt` | indented-row fixture → `S118`; column-zero-only control → `0` |

**88 vs the r83 report's 87.** The increment is exactly the id this round mints (S118); the invariant
holds: **collisions = registry max − 30** (112−30=82 r77, 114−30=84 r80, 116−30=86 r82, 117−30=87 r83,
**118−30=88 r84**).

Guard proven before any append (prompt requirement): a scratch registry row `  | S118 | indented-collision-row |`
(2-space indent) against a staged fixture carrying S118 yields `collisions=S118`; the same fixture
with a column-zero-only extractor yields `0` — the 0–3-space pattern is load-bearing, not decorative.

**The S118 twin is this round's hazard, same class as r83's S117.** Staged `merge/kasegi/SOURCES.append.md:94`
is `| S118 | 全国网络安全标准化技术委员会's own suggestion route … | own-work | A | … |`, URL
`https://www.tc260.org.cn/`` (trailing backtick in the cell); the staged knowledge file citing it is
`merge/kasegi/knowledge/corpus/knowledge/tc260-portal-serves-one-catch-all-shell.md`. Lane
`corpus/SOURCES.md:130` is the OSV Data sources page. An adoption that carried that entry's citations
unchanged would bind the CNVD/tc260 portal entry to the OSV data page **and pass the source census**
(the id exists) — the exact failure the document-first renumbering rule exists for. Nothing appends
while the r77 L0 question stays open (`corpus/lessons/round-79.md:77`).

Freeze check: at `7f76b7eb`, `corpus/SOURCES.md` carries 118 rows and S118 is `queued`; the worktree
is also still `queued` (F60 integration has not landed). The collision count is therefore identical
at freeze and now.

## 5. Files written

- `.ufo/waves/round-84/w1/ConnectorOverlap.md` (this report)
- `.ufo/waves/round-84/w1/ConnectorOverlap-receipts/assimilation/{reg-ids,staged-ids,collisions,doc-collisions.txt,assimilation-commands.txt,guard-proof-collisions.txt,guard-proof-reg-ids}`

No tool installed or upgraded; no lane, corpus, instrument, c1/, state or sibling-lane byte touched.
