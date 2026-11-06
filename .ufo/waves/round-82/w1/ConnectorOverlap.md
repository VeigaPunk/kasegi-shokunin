# ConnectorOverlap — kasegi round 82, attempt 1 (v1 wave, 12 seats)

Seat: cross-axis/sibling overlap scan. Read-only over the lane and the named sibling corpora; nothing in the lane tree was edited, no git/jj write was made, no instrument or gate was run.
Scratch: `/fast/scratch/hyaku/kasegi-r82/ConnectorOverlap` (deleted before yield). No tool was installed or upgraded.

Receipts (unedited command output): `ConnectorOverlap-receipts/sibling-knowledge-sweep.txt`, `c2-literal-sweep.txt`, `assimilation-swap-control.txt`.

Axes: **depth:verifiability (C1)** and **coverage (C2)**. The seat finds one move, proposed at §4, that improves verifiability and touches coverage nowhere.

---

## 1. C2 ground — is the OSV record-quality page already held anywhere?

### 1.1 Sibling lanes: no

Exact item grep over `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge`:

| file | status |
|---|---|
| `kasegi-shokunin/corpus/knowledge/osv-high-quality-record-import-bar.md` | the C2 draft itself (uncommitted worktree file) |
| `kasegi-shokunin/corpus/knowledge/osv-importfindings-record-quality-feedback.md` | F57, the r81 endpoint page (see 1.2) |
| `kotodama-shokunin/corpus/knowledge/culture-material/masks-masquerade.md:21` | false positive — `"good enough at likeness"` about Roman ancestor masks |

Extended sweep on the same directories for `data_quality.html`, `osv.dev`, `OSV record`: 8 hits, **all kasegi** (`openssf-scorecard-checks.md` plus the 7 OSV-family entries). Twenty-one sibling lanes hold knowledge corpora (`audio 18 … tsukuroi 134` entries); none holds this page, the OSV record format, or any record-quality ground. **C2's coverage is lane-unique; no sibling duplication risk.**

### 1.2 In-lane adjacency: F57 names the bar and explicitly leaves it unopened

F57's `## Limits` says: *"the quality bar itself: the page links it as a separate document ("Properties of a High Quality OSV Record", S115.txt:14, navigation only), which this entry does not open."* (`corpus/knowledge/osv-importfindings-record-quality-feedback.md:95`). F58 is therefore the page F57 deferred, not a restatement. The draft's `## Distinctness` names F57 and F31 correctly, and the six claimed literals are unique in-lane: `good enough`, `JSON Schema validation`, `Package-level precision`, `distinct ranges`, `another GitHub fork`, `2xx or 3xx` each appear in **0** files beyond the draft (`ConnectorOverlap-receipts/c2-literal-sweep.txt`). `corpus/knowledge` is at 96 entries in the worktree (95 committed + the draft), matching B2's 95 → 96.

### 1.3 PROVINCE fit: the F58 amendment is already present and follows the file's own convention

`PROVINCE.md:233` carries the F58 row, opened `[r82 Frontier amendment, appended 2026-11-06, end-of-file append per R6]`, with the same shape as its predecessors — compare `:225` (F54), `:227` (F55), `:229` (F56), `:231` (F57): round tag, item name with its six clauses, `admitted round <N> on source S### in corpus/knowledge/<entry>.md`, then `Scope limit:`. The append-at-EOF convention is stated at `PROVINCE.md:56` and repeated in every amendment tag (`:74-78`, `:225-233`); `PROVINCE.md:69`'s "the frontier as of round 31 is F01–F15" is a dated annotation, not a live count, so F58 does not contradict it. Writing "admitted round 82" before adjudication matches F56/F57's own practice. The file is dirty in the worktree (`M PROVINCE.md`), i.e. it lands with integration, which is the P5 practice.

Two non-blocking observations, not defects:

- `PROVINCE.md:233` is the only row in the file carrying a `Fits the lane as …` sentence (`grep -c "Fits the lane" PROVINCE.md` = 1). Lane-fit rationale normally lives in the `corpus/README.md` coverage row; if the L1 wants strict parity with F54–F57, that one sentence is the only candidate to drop.
- The row's scope limit names F31 but not F57 as the endpoint holder; F57's own scope limit names F51/F54/F55/F56. Harmless asymmetry, since F58's `## Distinctness` does name F57.

---

## 2. Newest considerthese (2026-10-26): no still-unimplemented proposal fits C1 or C2

`considerthese/` holds eight files, `2026-10-19.md` … `2026-10-26.md`, none since; the newest is `considerthese/2026-10-26.md`. Statuses are the lane's own documented dispositions in `corpus/knowledge/considerthese-proposals-ledger.md` (the R31 home), latest section `## Round-62 dispositions` at `:168`, with the round-46 per-proposal rows at `:152-164` and the round-62 tail at `:170`. Numbering caveat: the ledger's `:69-75` correction records that "1." names different proposals in different tables; this report uses the 2026-10-26 numbering that `:150` mandates.

| # | proposal (quoted) | status | fits C1/C2? |
|---|---|---|---|
| 1 | "Make \"distance to next score\" explicit." (`considerthese/2026-10-26.md:29`) | **landed** — criteria at `SCORECARD.md:1532`, verifiability-5 bar `:1536`, coverage 7→8 `:1547`; ledger `:152` | no — already landed |
| 2 | "Run one end-to-end domain task round." (`:30`) | **partially landed / domain task open** — claim checker committed (r43), the task itself not run; ledger `:154`, `:170`; `SHONEN.md:7` still `[ ]` | coverage **axis**, not C2's claim: it is a whole-round task (an H1/Immunefi report repriced through F13/F17/F18), not a wave-1 entry |
| 3 | "Add a quiescence gate before `complete`." (`:31`) | **landed** — `corpus/instruments/r46-landing-gate.py`, selftest cases=30; driver operator-side; ledger `:156` | no — already landed |
| 4 | "Cap or externalise wave evidence." (`:32`) | **open, operator-owned** — ledger `:158` | no — touches no claim's evidence chain |
| 5 | "Land the owed F18 `PROVINCE.md` amendment." (`:33`) | **landed r36** — `PROVINCE.md:77`; ledger `:160` | no |
| 6 | "Re-tune my own cadence and depth." (`:34`) | **open, operator-owned** — ledger `:162` | no |
| 7 | "Keep a proposal-status ledger." (`:35`) | **landed** — this file; ledger `:164` | no |

**Answer: none.** No still-unimplemented 2026-10-26 proposal fits the frozen C1 or C2 claims. Under an axis-only reading, proposal 2 is the sole coverage-axis fit and it is explicitly round-scale and authorisation-gated (live public reports), not a wave claim; proposals 4 and 6 are operator decisions about storage and cadence and touch neither axis. Quoting any of them into this round's claims would be scope inflation, not coverage.

---

## 3. Assimilation id collision check — re-run, counts, and what the count means

### 3.1 Re-run (frozen form, byte-identical)

Method: extract the `S###` id cell of every `| S` row from `corpus/SOURCES.md` and from `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` (read-only), sort, intersect. Reproduced exactly:

| file | lines | `cmp` vs frozen |
|---|---:|---|
| `reg-ids` | 116 (S001–S116) | rc 0, byte-identical |
| `staged-ids` | 94 (S031–S124) | rc 0, byte-identical |
| `collisions` | 86 (S031–S116) | rc 0, byte-identical |

### 3.2 The 86 is a label overlap, not a source collision

Pairing the two id spaces by canonical source URL (URL-carrying rows only; own-work rows are a lower bound, corpus paths are not URL-shaped) gives a 2×2 (`ConnectorOverlap-receipts/assimilation-swap-control.txt`):

|  | same source | different source |
|---|---:|---:|
| **same label** | **1** (S042 = S042, IPA 届出受付, `corpus/SOURCES.md:48` = `SOURCES.append.md:18`) | **85** |
| **different label** | **20** (invisible to the check) | 73 (staged rows with no lane counterpart) |

So of the 86 reported "collisions", 1 is a re-registration of the same source and 85 are two different sources wearing the same number. The check also misses 20 same-source pairs that carry different numbers. Staged-only ids: S117–S124 (8). Staged file mtime is `2026-10-24 23:33:20 -0300` — a 13-day-old snapshot of a numbering the lane has since changed (`SOURCES.append.md` S031 = HackerOne policy; lane S031 = CVE CNA Rules v4.2.6, landed r23 as "F07 to current CNA 4.2.6 (S031)").

Materialised variants of the staged table through the same three lines of extraction:

| variant | labels | sources | reported collisions |
|---|---|---|---:|
| renumber every id +100 | changed | unchanged (21 same-source pairs) | **0** |
| replace every source cell | unchanged | changed (0 same-source pairs) | **86** |

The verdict tracks the label exactly and the source not at all. This is a routed finding, not a verdict change: the assimilation files sit outside C1's P1–P9 and C2's B0–B8, so no claim is affected. What it would affect is any later merge that uses the id as the key: 85 staged rows would attach to ids that now denote other sources, and the one true re-registration would be indistinguishable from them. Merge semantics live in `shokuknow/merge/`, outside this item's named reads, so this is stated as a conditional risk, not a diagnosed merge failure.

---

## 4. The pattern, and the one proposed move

### 4.1 Pattern: content-addressed identity (label invariance)

C1's decoy limb and C2's G5 are the same test applied to two artifact classes: **the artifact must decide on content, not on the label or the source's literal text.**

| limb | what must survive | what must fail |
|---|---|---|
| C1 decoy (`mutbat.py:22-40`) | the target re-encoded with identical semantics — D1 `ast.unparse`, D2 local rename — must still score exactly like the baseline (`decoy=ok`, `decoy_hidden>=1`) | a counter that fails a row because that row's anchor vanished from its own source text (F6-selfdiff, F7-wsnorm: rc 0 under the r81 counter, `decoy=broken` under the r82 counter). Recorded limit at `:40`: an AST-embedding forgery (F8) passes both. |
| C2 G5 (`entry-gate.py:17`) | the rule text rewritten in the entry's own words (same claim, different wording) passes | a labelled dump: label `Falsifiable rule:` present, text drawn from the manifest quote or any snapshot line → `ruleless` |

The same test catches the round's own pre-freeze ledger: §3's collision check keys on the label and is blind to the source. Three independent instances in one round is the signal that this is a criterion, not a one-off.

### 4.2 Move: add one record criterion, R134

Append-only after R133 (`corpus/QUALITY.md`, last row; 134 R rows, Q1–Q6 unchanged). Exact text:

> **R134** | A gate, census or ledger that decides identity, admission or correctness from a label — a file name, an `S###` id, a path, a heading, a quoted source span — is not a check. Each such decision keys on a content-derived handle (a sha256 of the bytes, or a canonical URL/path), prints that handle beside its verdict, and carries two controls: **(i) label-preserving, content-changing** — the same label with different bytes must be reported or rejected; **(ii) content-preserving, label-changing** — the same bytes under a re-encoded, renamed or renumbered label must pass and score identically. A gate missing either control is labelled admission-only at that limb, and its count is not quoted as a collision, duplicate or identity result. | Grounded in: r82 C1 decoy limb (`.ufo/waves/round-82/c1/mutbat.py:22-40`); r82 C2 G5 (`.ufo/waves/round-82/c2/entry-gate.py:17`); the r82 pre-freeze assimilation check, whose 86 reported collisions are 1 same-source pair and 85 different-source pairs and which reports 0 when the same 94 sources are renumbered (`.ufo/waves/round-82/w1/ConnectorOverlap-receipts/assimilation-swap-control.txt`).

Delta against existing rows, so this is not a restatement: R3 requires an instrument to name its matcher; R11/R13/R17 require mutant discrimination and load-bearing limbs; R18 binds closure checks to a span's digest. None requires a content-derived identity handle or the two swap controls for gates that decide *identity* (collision, duplicate, admission).

First application (part of the same move, not a second proposal): the assimilation check replaces its id intersection with the 2×2 of §3.2 — classify each staged row by canonical source key into re-registration / id-reuse / new row, and quote the three counts, never the raw label overlap. This needs no new data: the staged file and `corpus/SOURCES.md` already carry the URLs; the driver is `ConnectorOverlap-receipts/assimilation-swap-control.py` (its output is the `.txt` beside it), runnable read-only with `TMPDIR=<scratch> python3 -B`.

### 4.3 Harm test (why this move does not cost either axis)

- **C1:** the r82 counter already satisfies both controls (its mutants are label-preserving content changes; its decoys are content-preserving label changes). R134 changes no P1–P9 value.
- **C2:** G5 already satisfies both controls (a quote swap under the same label is `ruleless`; an own-words rewrite passes). R134 changes no B0–B8 value.
- **Coverage:** the criterion constrains instruments and ledgers, not entries; it adds no admission cost to F58 and cannot block a Frontier row.
- The only artifact that fails it is the pre-freeze assimilation check, which is in neither claim.

### 4.4 Risks

- Proxy risk: requiring sha256 on every ledger identity is heavy for large tables; the criterion admits a canonical URL/path as the handle, which bounds the cost to rows that have neither (own-work rows would need a path + byte digest). If the L1 wants it cheaper, the fallback is path + mtime-free digest of the first N bytes — but say so in the row, not in a commit message.
- Criterion inflation: R133 → R134 is the 134th row; the justification is three independent in-round instances, and the row is a generalization of the two r82 limbs, so it retires the duplication rather than adding a fourth special case.
- §3's URL matching under-counts same-source pairs (own-work and path rows); 20 invisible pairs is a **lower bound**, and the 73 "no counterpart" cells include rows whose lane row spells the source differently. The 1-vs-85 split is not affected: 85 is an upper bound on same-source pairs under the same label, and only S042 matched.

---

## 5. Verification a non-author can re-run

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
# §3.1 reproduction (byte-identical): extract | S ids from both files, sort, intersect, cmp against .ufo/waves/round-82/assimilation/{reg-ids,staged-ids,collisions}
# §3.2 control: python3 -B <receipt driver>  -> FROZEN 116/94/86; CELL A=1 B=85 C=20 D=73; renumber 0; contentswap 86
# §1.1: grep -rli 'data_quality\|High Quality OSV\|good enough' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge
# §1.2: for q in "good enough" "JSON Schema validation" ... ; grep -rl -- "$q" corpus/knowledge/*.md | grep -v osv-high-quality-record-import-bar.md
# §2: grep -n '^\*\*[1-7]\.' corpus/knowledge/considerthese-proposals-ledger.md
```

No lane file was modified: `git status --porcelain` in the lane shows only the pre-existing freeze/worktree state plus this wave dir (`?? .ufo/waves/round-82/w1/`).
