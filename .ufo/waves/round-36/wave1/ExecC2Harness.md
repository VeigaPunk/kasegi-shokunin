# ExecC2Harness — round-36 proposed-tree replay of the four C2 instruments

Seat: `ExecC2Harness` (executor, axis `coverage`). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
base `cc692008b0cfd58d18275aa6c4aed79620120799`, claims-freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`.
**No lane file was written.** Everything below was measured on `git archive` exports and copies under
`/fast/scratch/hyaku/kasegi-r36/ExecC2Harness/` (removed at the end of the seat).

---

## 0. Verdict (read this first)

| # | Required line from the item | measured | status |
|---|---|---|---|
| 1 | `frontier-recheck-count.py` → `entries=22 pass=22 exit=0` incl. `PASS F19 … ids=S053` | **as-shipped tree: `FAIL F19 … exit=2 problems=recheck-exit-2`, `entries=22 pass=21 exit=1`.** The literal `entries=22 pass=22 exit=0` is reproduced **only** in a labelled relocation copy (§3), and with a **derived F19 README row that no seat drafts** (§1.2, §5 F1). | ⚠ not yet reachable pre-integration; reproducible after landing |
| 2 | `source-recheck.py --manifest …/round-36/manifest.json --source S053` → exit 0, `occurrences=1` per quote | **exit 0**, `S053:sha256 OK`, `Q1..Q4 OK occurrences=1 anchor=216/217/217/235-ok` | ✅ |
| 3 | `recheck-audit.py` → `strict pass=48/48`, `expect=present expected=48 missing=0 unexpected=0 exit=0` | **exit 0**, `strict pass=48/48 cdroot_fail=0 instrument_fail=0 own_fail=0`, `expect=present expected=48 missing=0 unexpected=0` | ✅ |
| 4 | `capture-binding-check.py` → exit 0, records bound | **exit 0**, `round-36 records=1 url_bound=1 fetched=1`, `records=43 bound=43 unbound=0` | ✅ |

One unowned write and one number-drift guard decide whether that evidence line can land — both are for the
L1, neither is fixed here:

- **F1 (unowned write).** `corpus/README.md`'s Frontier F19 row is drafted by **no seat** in this wave (both
  scribe items are the entry and the SOURCES row/bullet/Paths only), yet `frontier-recheck-count.py`
  enumerates admitted rows from `corpus/README.md`. Without that row the harness prints
  `entries=21 pass=21` (§2.1). A minimal derived row that satisfies the harness regex and the C2 shape is
  given verbatim in §5 F1.
- **F2 (number drift — observed then self-corrected).** The entry draft I first pulled (12:41 receipt state,
  17267 B, sha256 `27a4d42a…`) carried `sha256 4ec61c59b0**a**9aedf…` in both the `source:` header line and
  the pin section, with the true `4ec61c59b0**e**9aedf…` occurring **0** times. The seat's receipt was
  re-issued at 12:43 (17374 B, sha256 `36df1b1f…`) and the current entry bytes carry the true digest
  **twice** and the drifted form **0** times; the wrong form now survives only inside the receipt's own
  disclosure prose. Every figure below was re-measured after the re-pull, so they describe the current
  draft. Residual hazard: the wave receipts contain both forms in prose, and no instrument reads the entry
  text (`source-recheck.py` compares the *manifest*), so the L1 should assert `b0e9` in the landed entry.

---

## 1. What was assembled

### 1.1 Inputs (read-only, from wave receipts — not from scratch drafts)

| artifact | source | bytes | sha256 |
|---|---|---|---|
| `corpus/source-snapshots/round-36/S053.txt` | `ExecC2Capture.md` §6 fence (`text`), last fence = capture | 8448 (244 lines) | `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9` |
| `corpus/source-snapshots/round-36/manifest.json` | `ExecC2Capture.md` §3 fence (`json`) | 3566 | `f9590c2bbc26244af88dce8fa7c291d67e6138c293ba5198257789911c017da3` |
| `corpus/knowledge/epss-exploit-prediction-scoring.md` | `ScribeEntryF19.md` between `---BEGIN ENTRY---` / `---END ENTRY---` (12:43 re-issue) | 17374 (263 lines) | `36df1b1f9b4f828c631be8703ee5bd1a5bedc87d84410a7ecd07c8b0241aa641` |
| S053 registry row / Search-log bullet / Paths line | `ScribeRowS053.md` §1.1–1.3 (`markdown` fences 1–3) | 895 / 1464 / 312 | `35c530af…`, `9b1278d6…`, `9939203a…` |
| `corpus/instruments/knowledge-expected.txt` | derived: the entry inserted **sorted** (after `cwe-top25-2025-methodology.md`, before `ev-model.md`), once | 2439 | `f0d4bb0dcc12c2f3492d117a651264aa1c38638e57dd365de4655d87a46e4321` |
| `corpus/SOURCES.md` (post) | base + row after `| S052 |`, Paths line at the end of `## Paths`, bullet at the end of `## Search log` | 68151 | `a2c4828ffca2362cc93a656ebd9558f413b50a7b4720229c63a175514d3544d6` |
| `corpus/README.md` (post2 only) | derived F19 row after `| F18 |` (§5 F1) | 38880 | `73399d8896ef7896125b2eaa23cce25bb6e5e49de393687c36e159afc1d50967` |

The capture's digest was **re-derived from the receipt text**, not trusted: extracting the fence and
hashing it gives `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`, byte-identical to the
digest the receipt, the manifest and the SOURCES row all state.

### 1.2 Trees

- `base` = `git archive cc692008… | tar -x --one-top-level=base` (not a git repo: `git -C base rev-parse` → "not a git repository").
- `post1` = base + capture + manifest + entry + SOURCES.md (row/bullet/Paths) + `knowledge-expected.txt` (47→48).
  `diff -rq base post1` reports exactly four paths: `corpus/SOURCES.md`, `corpus/instruments/knowledge-expected.txt`,
  `corpus/knowledge/epss-exploit-prediction-scoring.md`, `corpus/source-snapshots/round-36/`.
- `post2` = `post1` + the derived F19 README row. `diff -rq post1 post2` reports exactly one path:
  `corpus/README.md` (one added line).
- `post1-reloc` / `post2-reloc` = copies of `post1` / `post2` where the **only** edit is the literal
  `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin` → the copy's own root: 53 occurrences in 47 files
  (`diff -r post2/corpus/knowledge post2-reloc/corpus/knowledge` → 53 `<` and 53 `>` lines, all `cd` prefixes).

**Why the relocation copy exists.** Every `recheck:` line in `corpus/knowledge/*.md` begins
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …`, and every instrument runs the line *as written*.
A scratch export therefore executes against the **live lane**, not against the tree — so
`frontier-recheck-count.py --root post2` measures a mixed object and `recheck-audit.py`'s `cdroot` limb
fails 47/47 unless `--cdroot` is the lane root. The as-shipped runs below are reported as the honest
pre-integration measurement; the relocation runs are the labelled simulation of the same bytes with a
self-referential root, which is what the post-landing lane *is*.

Assembly is reproducible: the assembler is §Appendix A; it asserts the capture digest and the 11-cell row
before writing anything.

Structural counts (base → post1/post2):

```
knowledge files            47 → 48        knowledge-expected lines  47 → 48
registry rows (^| S)       52 → 53        frontier rows (^| F)      18 → 19 (post2 only)
snapshot manifest dirs     11 → 12        capture records           42 → 43
```

`knowledge-expected.txt` diff (single added line, sorted position):

```
@@ -15,6 +15,7 @@
 corpus/knowledge/cra-manufacturer-reporting-duties.md
 corpus/knowledge/cvss-v4-severity-and-vector.md
 corpus/knowledge/cwe-top25-2025-methodology.md
+corpus/knowledge/epss-exploit-prediction-scoring.md
 corpus/knowledge/ev-model.md
 corpus/knowledge/evidence-dir.md
```

`SOURCES.md` diff: exactly 3 added lines (row; Paths line; Search-log bullet). Cell audit of the drafted
row: 11 cells, no inner `|`, one `https://` token in the source cell, `S053 docs A … mined 2026-10-26 90d
corpus/knowledge/epss-exploit-prediction-scoring.md`.

---

## 2. Required instrument runs — as-shipped trees

### 2.1 `frontier-recheck-count.py` on `post1` (drafts, no README row)

```
$ cd post1 && python3 corpus/instruments/frontier-recheck-count.py
PASS     F01  knowledge/cvss-v4-severity-and-vector.md             ids=S001           exit=0
PASS     F02  knowledge/coordinated-disclosure-timelines.md        ids=S003           exit=0
PASS     F03  knowledge/authorization-safe-harbor-and-scope.md     ids=S006           exit=0
PASS     F04  knowledge/ai-assisted-finding-validation.md          ids=S009           exit=0
PASS     F05  knowledge/cwe-top25-2025-methodology.md              ids=S013           exit=0
PASS     F06  knowledge/multiparty-vulnerability-coordination.md   ids=S018           exit=0
PASS     F07  knowledge/cna-assignment-and-vulnerability-rules.md  ids=S031           exit=0
PASS     F08  knowledge/cra-manufacturer-reporting-duties.md       ids=S029           exit=0
PASS     F09  knowledge/authorised-testing-rules-of-engagement.md  ids=S032           exit=0
PASS     F09  knowledge/statutory-authorization-and-unauthorized-access.md ids=S033,S034,S035 exit=0
PASS     F10  knowledge/vendor-disclosure-policies-as-corpus-objects.md ids=S036,S037,S038,S039 exit=0
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
entries=21 pass=21 exit=0
```

**No F19 line at all.** The entry exists in the tree (`corpus/knowledge/epss-exploit-prediction-scoring.md`),
but the harness enumerates only admitted rows of `corpus/README.md`, where F19 is absent: this is the
item's (a)+(b)+(c) list reproduced exactly, and it yields 21, not 22.

### 2.2 `frontier-recheck-count.py` on `post2` (post1 + derived README row)

```
$ cd post2 && python3 corpus/instruments/frontier-recheck-count.py
…
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
FAIL     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=2    problems=recheck-exit-2
entries=22 pass=21 exit=1
EXIT=1
```

(The `…` stands for the F01–F18 lines, byte-identical to §2.1. The literal `entries=22 pass=22 exit=0`
appears only in the relocation copy, §3.)

`exit=2` is `source-recheck.py`'s fail-closed "manifest UNAVAILABLE reason=missing": the entry's line cds
to the live lane, where `corpus/source-snapshots/round-36/manifest.json` does not exist yet. **This is the
landing-order fact** — the entry, the capture and the manifest must land in the same commit; an entry
landed before its capture fails closed (exit 2), never silently passes.

### 2.3 `source-recheck.py --source S053` on `post1`

```
$ cd post1 && python3 corpus/instruments/source-recheck.py \
    --manifest corpus/source-snapshots/round-36/manifest.json --source S053
S053:sha256 OK
S053:Q1 OK occurrences=1 anchor=216-ok
S053:Q2 OK occurrences=1 anchor=217-ok
S053:Q3 OK occurrences=1 anchor=217-ok
S053:Q4 OK occurrences=1 anchor=235-ok
EXIT=0
```

Control on the same command without the capture (`base` tree, `cd base`):

```
manifest UNAVAILABLE reason=missing
EXIT=2
```

### 2.4 `recheck-audit.py` on `post1` (`--cdroot` = lane root, every line's literal `cd`)

```
$ python3 corpus/instruments/recheck-audit.py --root <post1> \
    --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin
epss-exploit-prediction-scoring.md                          frozen=111 strict=111111 lane=2   foreign=2   gated       PASS
strict pass=48/48 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=23 gated=25 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=48 total=48 pass=48 fail-closed=25 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=48 missing=0 unexpected=0 exit=0
```

Base control, same flags: `strict pass=47/47 … lines=47 total=47 pass=47 fail-closed=24 … expected=47
missing=0 unexpected=0 exit=0`, `executes=23`.

The as-shipped run keeps every frozen+strict limb green but classifies the new entry `gated` (lane=2,
foreign=2): the line parses, names existing paths, names its own instrument and its own `--source`, and
fails closed because the live lane has no round-36 capture yet. `strict pass=48/48` here is a **form**
verdict; §3 is the run where the new line actually executes.

### 2.5 `capture-binding-check.py` on `post1`

```
$ cd post1 && python3 corpus/instruments/capture-binding-check.py
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-35 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-36 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=43 with_url=43 with_fetched_utc=5 with_archival=38 snapshot_dirs=12 manifest_dirs=12 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=43 bound=43 unbound=0
EXIT=0
```

(base control: `records=42 bound=42`.) The new record binds: `url https://www.first.org/epss/` equals the
source cell's single `https://` token, `fetched_utc 2026-10-26T15:35:10Z` is strict UTC (round-36 has no
archival exemption), `path` stem equals `id`.

### 2.6 Adjacent read-only check: fleet census over the proposed registry

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file <post1>/corpus/SOURCES.md --today 2026-10-26
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	<post1>/corpus/SOURCES.md
EXIT=0
```

Identical to the `base` run (same two pre-existing W04 warnings), so the S053 row adds no new finding and
no E-code. `E11` is load-bearing, not vacuous: the same `SOURCES.md` in a tree **without** the entry prints
`file	E11	S053 missing used-by corpus/knowledge/epss-exploit-prediction-scoring.md`, `EXIT=1`.

---

## 3. Relocation replay (`post2-reloc`) — what the landed lane will look like

`post2-reloc`'s only difference from `post2` is the 53 `cd <lane>` prefixes, retargeted at the copy.

```
$ cd post2-reloc && python3 corpus/instruments/frontier-recheck-count.py
… (F01–F18 PASS as in §2.1)
PASS     F19  knowledge/epss-exploit-prediction-scoring.md         ids=S053           exit=0
entries=22 pass=22 exit=0
EXIT=0
```

```
$ python3 corpus/instruments/recheck-audit.py --root <post1-reloc> --cdroot <post1-reloc>
epss-exploit-prediction-scoring.md                          frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
strict pass=48/48 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=24 gated=24 broken=0
lines=48 total=48 pass=48 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=48 missing=0 unexpected=0 exit=0
```

`executes` rises 23 → 24 while `fail-closed` stays 24: the new entry's own line is the one that now runs
successfully against its own capture, and no previously-gated line changed class. This is the literal
`entries=22 pass=22 exit=0` / `strict pass=48/48 … exit=0` pair the frozen claim names, measured on the
proposed bytes with the tree as root — **a simulation, to be re-taken verbatim in the real lane after the
L1 lands the six artifacts.**

---

## 4. Controls — every limb above can fail

| control | perturbation | result |
|---|---|---|
| `base` | no drafts at all | frontier `entries=21 pass=21` (no F19); audit `47/47`, `expected=47`; binding `records=42`; `source-recheck … round-36` → `manifest UNAVAILABLE reason=missing`, exit 2 |
| `ctl-nocap` | `post2` relocated, `S053.txt` deleted | `FAIL     F19 … ids=S053 exit=2 problems=recheck-exit-2` / `entries=22 pass=21 exit=1` |
| `ctl-flip` | `post2` relocated, one byte changed in the capture (`30 days.` → `30 days!`) | `FAIL     F19 … ids=S053 exit=1 problems=recheck-exit-1` / `entries=22 pass=21 exit=1` |
| `ctl-expect47` | `post1`, `knowledge-expected.txt` reverted to base (47) while the tree has 48 files | `expect=present expected=47 missing=0 unexpected=1 exit=1` (even though `pass=48/48`) |
| `ctl-e11` | `post1`'s `SOURCES.md` in a tree without the entry | census `E11 S053 missing used-by …`, `EXIT=1` |

The first paired run of the controls is itself a finding about *this* harness family: copies of a relocated
tree still passed while their capture was deleted, because the copies' `cd` still named the **other** tree.
The check binds to the tree its own command line names, not to the instrument's `--root`. Controls must be
relocated per copy; a reader re-running them must not "fix" a red by copying.

Per-line quote fidelity of the drafted entry (independent of the instruments, which never read entry text):
all **11** blockquoted passages occur exactly once in `S053.txt` after whitespace normalization, and all are
≤ 25 words (25, 13, 8, 12, 23, 10, 17, 19, 23, 16, 18). The pin budget truncation the ScribeRowS053 receipt
records (the 30-word definition sentence pinned from its `(EPSS)` parenthetical) is what the capture shows:
the entry's quote is the 25-word span, and the manifest's `location` carries the full-sentence note.

Entry header line checks: `source: S053 — https://www.first.org/epss/ — …`, `verified-at: 2026-10-26`,
`ground: F19`; `recheck:` parses (`bash -n` exit 0), carries `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`,
`--manifest corpus/source-snapshots/round-36/manifest.json` and `--source S053`.

---

## 5. Findings for the L1

**F1 — the F19 README row is an unassigned write; without it the harness cannot reach 22.** No round-36
receipt drafts `corpus/README.md`'s frontier table: `grep -l '^| F19 |' .ufo/waves/round-36/wave1/*.md`
over the 48 receipts present at write time matches **only this receipt** (the derived row below); the two
scribe items cover the entry (`ScribeEntryF19`) and the SOURCES row/bullet/Paths (`ScribeRowS053`) and
nothing else, while `ScribeScorecard.md:62` already expects `grep -cE '^\| F[0-9]+ \|' corpus/README.md ->
19`. The minimum row that satisfies the harness (`FRONTIER_ROW` regex, `status == admitted`, entry cell
split on `,`) and the 6-column table is:

```
| F19 | FIRST EPSS exploitation-likelihood scoring | admitted | knowledge/epss-exploit-prediction-scoring.md | S053 | EPSS estimates the probability that a published CVE will be exploited in the wild in the next 30 days; treat it as a likelihood signal distinct from CVSS severity and KEV catalog status |
```

Cells used above: entry path and `S053` from the frozen claim; topic and `next` from the drafted S053 row's
source/`teaches` cells. **This row is this seat's derived simulation input, not a drafted artifact**; the
L1 owns its final wording. Wherever it lands, the harness gate is exactly `entries=22 pass=22` (§3).

**F2 — the entry's pinned digest drifted, was self-corrected, and remains unguarded.** The draft I first
pulled (12:41 receipt, 17267 B, `27a4d42a…`) read `4ec61c59b0**a**9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`
on line 3 (`source:` header) **and** line 253 (pin section), with the capture's true
`4ec61c59b0**e**9aedf…` occurring 0 times. The receipt was re-issued at 12:43 (17374 B, `36df1b1f…`) and
the current entry carries the true digest twice and the drifted form 0 times; all measurements here were
re-taken on those bytes and are unchanged. Residual risk, which the L1 should close at landing: the wave
receipts contain both forms in prose, and no instrument reads the entry text (`source-recheck.py` compares
the *manifest*), so a future drift of this field would land false while every C2 gate stays green. Assert
`4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9` in the landed entry.
(`RevHarnessSync` independently caught this and confirms the current receipt is corrected; the flag stands
as a guard, not as a live defect.)

**F3 — landing order is a hard requirement, not a nicety.** With the entry but without the capture in the
same tree, F19 reports `recheck-exit-2` (§2.2) and the audit classifies it `gated`. Entry + `S053.txt` +
`manifest.json` must land together.

**F4 — the item's own assembly list is incomplete relative to its expected output.** The list is
BASE + entry + SOURCES row/bullet + `knowledge-expected.txt`; the expectation `entries=22` additionally
requires the README row (F1) — and `knowledge-expected.txt` must be *inserted in sort order*, not appended
(a tail append would break the file's own sorted contract; a duplicated line would print `expected=49`).
§1.1 records the ordered insertion and the single-line diff.

**F5 — the audit's green is a form verdict pre-landing.** `strict pass=48/48 exit=0` on the as-shipped tree
is reached while the new entry is `gated` (lane=2). A receipt that quotes only that line without the class
column would overstate execution; quote `executes=24 gated=24` (§3) or state `gated` explicitly.

---

## 6. Limits — what this seat did not measure

- The literal `entries=22 pass=22 exit=0` / `pass=48/48 executes=24` pair was **not** measured in the real
  lane: it cannot exist there until the six artifacts land. §3 is a relocation simulation of those bytes.
- Not measured: whether the entry's prose claims are *current upstream* (the capture is a point-in-time
  pin), the junk twin `c2-controls/junk-f19.md` rejection (ExecC2JunkControl), the round-36 lesson/scorecard
  writes, the C1 `r36-closure.sh` suite, and the census on the **landed** lane (census reads the lane; §2.6
  is the same instrument on the proposed registry via `--file`).
- No mutation of the entry's quote text with a matching manifest digest (that would test quote binding
  independent of sha256 and belongs to MutC2Entry); the two controls used here stop at digest/capture
  presence, which is enough to show F19's PASS is byte-bound.
- Nothing installed, nothing upgraded; `pacman` not invoked; no `uv tool install`; no `npx`; no binary
  dropped. Tools used as present: `bash`, `git` (read-only), `python3` (3.14), `sha256sum`, `diff`, `grep`,
  the fleet's `scripts/sources-census.sh` (read-only `--file` mode).

---

## 7. Provenance

| # | command (cwd) | exit | key line |
|---|---|---|---|
| 1 | `git archive cc692008… \| tar -x --one-top-level=base` (lane) | 0 | 9 top-level entries; not a git repo |
| 2 | `assemble.py <scratch>` (scratch) | 0 | digests + counts of §1.1 |
| 3 | `frontier-recheck-count.py` (post1) | 0 | `entries=21 pass=21 exit=0` |
| 4 | `frontier-recheck-count.py` (post2) | 1 | `FAIL F19 … exit=2`; `entries=22 pass=21 exit=1` |
| 5 | `frontier-recheck-count.py` (post2-reloc) | 0 | `PASS F19 … ids=S053 exit=0`; `entries=22 pass=22 exit=0` |
| 6 | `source-recheck.py --manifest …/round-36/manifest.json --source S053` (post1) | 0 | `sha256 OK`; Q1–Q4 `occurrences=1`, anchors 216/217/217/235 |
| 7 | same command (base) | 2 | `manifest UNAVAILABLE reason=missing` |
| 8 | `recheck-audit.py --root post1 --cdroot <lane>` | 0 | `strict pass=48/48`; `expected=48`; new entry `gated` |
| 9 | `recheck-audit.py --root post1-reloc --cdroot post1-reloc` | 0 | `strict pass=48/48`; `executes=24 gated=24` |
| 10 | `recheck-audit.py --root base --cdroot <lane>` | 0 | `strict pass=47/47`; `expected=47` |
| 11 | `capture-binding-check.py` (post1) | 0 | `round-36 records=1 url_bound=1`; `records=43 bound=43 unbound=0` |
| 12 | `sources-census.sh validate --file <post1>/corpus/SOURCES.md --today 2026-10-26` | 0 | `W04 S028`, `W04 S029`, `ok` |
| 13 | controls §4 (`ctl-nocap`, `ctl-flip`, `ctl-expect47`, `ctl-e11`) | 1/1/1/1 | each named limb red as tabulated |
| 14 | controls rebuilt and re-run after the 12:43 entry re-pull (`ctl-nocap`, `ctl-flip`, `ctl-expect47`) | 1/1/1 | red as tabulated, unchanged |
| 15 | `re-pull`: re-extract entry between `---BEGIN ENTRY---` / `---END ENTRY---` and re-assemble + re-run 3–13 | 0 | entry 17374 B / `36df1b1f…`; digest `b0e9` ×2, `b0a9` ×0; every §2–§4 figure reproduced unchanged |

All figures above were measured on the **12:43 re-issued** entry draft (17374 B, sha256 `36df1b1f…`), after
`RevHarnessSync` flagged that the 12:41 snapshot I first pulled carried the drifted digest (§0 F2). The
re-pull changed no instrument verdict: frontier 21/21 (post1) · 22 entries/21 pass (post2 as shipped) ·
22/22 (post2-reloc); audit 48/48 with `gated` (as shipped) and `executes=24` (relocated); recheck exit 0 with
`occurrences=1` on all four quotes; binding 43/43 bound.

Scratch `/fast/scratch/hyaku/kasegi-r36/ExecC2Harness/` removed at end of seat.

---

## Appendix A — assembler (replayable)

```python
#!/usr/bin/env python3
"""Assemble the proposed round-36 tree state in scratch (read-only over the lane)."""
import hashlib, json, os, re, shutil, sys

S = sys.argv[1]
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
WAVE = os.path.join(LANE, ".ufo/waves/round-36/wave1")
BASE, POST1, POST2 = (os.path.join(S, n) for n in ("base", "post1", "post2"))

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

def fences(text):
    out, i, lines = [], 0, text.split("\n")
    while i < len(lines):
        if lines[i].startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"): j += 1
            out.append((lines[i][3:].strip(), "\n".join(lines[i + 1:j]) + "\n")); i = j + 1
        else: i += 1
    return out

cap_blocks = fences(open(os.path.join(WAVE, "ExecC2Capture.md"), encoding="utf-8").read())
manifest = [b for l, b in cap_blocks if l == "json"][0]
s053 = [b for l, b in cap_blocks if l == "text"][-1]
assert hashlib.sha256(s053.encode()).hexdigest() == \
    "4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9"
json.loads(manifest)

entry = re.search(r"---BEGIN ENTRY---\n(.*?)\n---END ENTRY---",
                  open(os.path.join(WAVE, "ScribeEntryF19.md"), encoding="utf-8").read(), re.S).group(1) + "\n"
row, bullet, paths_line = [b.rstrip("\n") for _, b in fences(
    open(os.path.join(WAVE, "ScribeRowS053.md"), encoding="utf-8").read())[:3]]
assert len(row.strip().strip("|").split("|")) == 11

if os.path.isdir(POST1): shutil.rmtree(POST1)
shutil.copytree(BASE, POST1)
snap = os.path.join(POST1, "corpus/source-snapshots/round-36"); os.makedirs(snap)
open(os.path.join(snap, "S053.txt"), "w", encoding="utf-8").write(s053)
open(os.path.join(snap, "manifest.json"), "w", encoding="utf-8").write(manifest)
open(os.path.join(POST1, "corpus/knowledge/epss-exploit-prediction-scoring.md"), "w", encoding="utf-8").write(entry)

# SOURCES.md: row after | S052 |, Paths line at the end of ## Paths, bullet at the end of ## Search log
p = os.path.join(POST1, "corpus/SOURCES.md")
out, sec, r_ok, b_ok, p_ok = [], None, False, False, False
for line in open(p, encoding="utf-8").read().split("\n"):
    if line.startswith("## "):
        if sec == "paths" and not p_ok: out.append(paths_line); p_ok = True
        if sec == "search" and not b_ok: out.append(bullet); b_ok = True
        sec = {"## Paths": "paths", "## Search log": "search"}.get(line)
    out.append(line)
    if not r_ok and line.startswith("| S052 |"): out.append(row); r_ok = True
assert r_ok and b_ok and p_ok
open(p, "w", encoding="utf-8").write("\n".join(out))

# knowledge-expected.txt: sorted insertion, exactly once (47 -> 48)
p = os.path.join(POST1, "corpus/instruments/knowledge-expected.txt")
ke = open(p, encoding="utf-8").read().split("\n")
names = [l for l in ke if l and not l.startswith("#")] + ["corpus/knowledge/epss-exploit-prediction-scoring.md"]
names.sort()
open(p, "w", encoding="utf-8").write("\n".join([l for l in ke if l.startswith("#")] + names + [""]))

# post2 = post1 + a DERIVED F19 frontier row (no seat drafts it; see §5 F1)
if os.path.isdir(POST2): shutil.rmtree(POST2)
shutil.copytree(POST1, POST2)
cells = [c.strip() for c in row.strip().strip("|").split("|")]
f19 = "| F19 | FIRST EPSS exploitation-likelihood scoring | admitted | %s | %s | %s |" % (
    cells[10].replace("corpus/", ""), cells[0], cells[6])
p = os.path.join(POST2, "corpus/README.md"); out, placed = [], False
for line in open(p, encoding="utf-8").read().split("\n"):
    out.append(line)
    if not placed and line.startswith("| F18 |"): out.append(f19); placed = True
assert placed
open(p, "w", encoding="utf-8").write("\n".join(out))
```

Relocation (needed for §3, and only there): copy `post1`/`post2`, then replace the literal
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` with the copy's absolute path in `corpus/knowledge/*.md`
(53 occurrences / 47 files); every other byte identical, verified by `diff -r`.

Artifact: `.ufo/waves/round-36/wave1/ExecC2Harness.md`.
