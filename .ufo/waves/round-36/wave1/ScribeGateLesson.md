# ScribeGateLesson — round-36 lesson draft (§ Gate + § Mistakes anchors) with its evidence

Seat: `ScribeGateLesson` (scribe, leaf — no dispatch, no swarm). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(the only lane repo); base `cc692008b0cfd58d18275aa6c4aed79620120799`; claims-freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`;
`HEAD` at every measurement below `b47f2cdf` (the worktree carried only untracked `.ufo/waves/round-36/*` paths).
Round 36, wave `kasegi-r36-build`, hyaku run 9 (`.ufo/watchdog.log:1527`).

Model (host-reported): `opencode-go/deepseek-v4.1-flash`; no model argument was passed by this seat.

**Report.** Behaviour: this seat drafted the round-36 lesson text (§ Shape, § Frozen claims, § Gate,
§ Mistakes anchors, § considerthese summary, § Registry change log, § Census, § contested scope, § pending
spot-check, § Open items) and wrote it only into this receipt; it did not write `corpus/lessons/round-36.md`,
any registry row, capture, manifest, instrument, SCORECARD section, or sibling/source tree. Gates: the Gate
block carries one admit (F19/S053), three reject classes (junk twin, 6-of-7 quarantine rows, 7 standing
refusals), the quarantine and id-collision numbers with their derivations, the considerthese dispositions, and
the spot-check placeholder. Every number states the artifact it was read from; target values are labelled
targets. Findings: the register in § 4 (twelve entries — eleven findings plus the peer review this seat
applied), covering the unbacked `junk_present=1` control, the unresolved S037/S054 label, the
closed-but-greppable `b0a9` digest conflict, the provenance-note path in E4, E1's blindness to an abbreviated
closing hash, the non-verbatim recommended Q1, S065's transport-only movement, the suite's measured-vs-landed
revision drift, the two revisions' `4/9` vs `3/9` negative control, the census excerpt, and the landed lesson's
condensed form. Out of scope: no re-execution of the suite,
harness, census or `source-recheck`; no re-fetch of any quarantine row; no sibling re-sweep. Artifact paths:
this receipt, plus the five inputs named in § 2.

- **Writes used:** this receipt only, and scratch `/fast/scratch/hyaku/kasegi-r36/ScribeGateLesson/`
  (`lesson.md` draft, `S053.txt` capture copy, `quarantine-slice`, `reg-ids`, `staged-ids`, `epss.html`).
  The scratch dir is removed after this receipt is written; nothing here depends on a surviving scratch file.
- **Tooling:** nothing installed or upgraded. `pacman` was not invoked (host-wide pause respected); no
  `uv tool install`, no `npx`, no binary drop. Tools used as already present: `bash`, `curl`, `awk`, `grep`,
  `git` (read-only), `python3` 3.14.x, `sha256sum`, `cmp`.
- **Mutation:** no `git`/`jj` mutation. Read-only `rev-parse`, `log`, `show`, `ls-tree`, `ls-files`,
  `cat-file`, `merge-base --is-ancestor`, `status`, `archive`-free inspection only. No `agent://all` message;
  two peer messages (spot-check reviewer) and no tool run inside `/home/vgpnk/Projects/shokuknow` beyond
  reading the register and the package with `sha256sum`/`awk`/`grep`.

## 1. Deliverable — `corpus/lessons/round-36.md` (draft text)

Paste the block between the markers verbatim (UTF-8, single trailing newline). The block **as it sits in this
receipt**, between the marker lines (the extraction includes one leading and one trailing empty line), is
**sha256 `732bcb1527e7255856e771a674ee409cf34318d1aa69a1cd68f14ed221a5156c`**, 413 lines / 37,641 B /
5,346 words. This seat kept no separate lesson file — its scratch tree was removed by another process before
the final assembly, so the bytes inside these markers are the authoritative draft, and the L1 should re-hash
after pasting since every later append in the same round moves it.

---BEGIN LESSON---

# Round 36 — kasegi

Lane: `kasegi-shokunin`. Round 36, wave `kasegi-r36-build`. Revisions: base
`cc692008b0cfd58d18275aa6c4aed79620120799`; claims-freeze commit
`b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (committer instant not re-read by this seat); round-36 final
lane commit: recorded in the closing commit, and its hash must satisfy E1 (see § Frozen claims, C1). This
lesson reports working-tree, receipt and `git archive` export evidence; it is not a canonical judge decision.

**Draft status.** This file is drafted by seat `ScribeGateLesson` (leaf, no dispatch). § Shape, § Frozen
claims, § Gate, § Mistakes, § Registry change log, § Census and § Open items are this seat's. § considerthese,
§ No-harm, § SHONEN, § LOG and the SCORECARD section are named with their owner receipts in § Sections this
draft does not own; this seat did not draft them and does not bind their numbers. Every value below states
which artifact it was read from and at which instant; no value is a prediction dressed as a measurement.
The draft contains neither of the two placeholder spellings E1 counts — verified, command in the seat
receipt (`.ufo/waves/round-36/wave1/ScribeGateLesson.md` § 6.1) — and it deliberately quotes no lane-hash
marker.

Shape: **one v2 wave**, `.ufo/waves/round-36/wave1-dispatch.json` (`schema=ufo-swarm-wave-dispatch-v1`,
`wave=kasegi-r36-build`, `counts={spawn: 64, resume: 0, total: 64}`, `policy.maxLanes=128`,
sha256 `cbed673a26e05dba…`); `wave1-spec.json` carries 64 `items` with 64 unique names
(sha256 `af5cf818a46aa01d…`); `wave1.ready` (170 B) names `l1: KasegiR36`. Declared role counts: executor 18,
scribe 12, reviewer 10, critic 6, scout 6, mutation-tester 5, connector 3, sentinel 2, simplifier 2 (= 64).
Route: L1 inline spawn handoff, hyaku run 9
(`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1527` —
`2026-10-26T12:31:14-03:00 launch kasegi round=36 pgid=14809 driver=hyaku-inline attempt=1`). Axes owned:
`depth:density`, `depth:verifiability`, `coverage`; saturation line 9/10 per axis, window N=3; lowest
non-retired axis `depth:verifiability (4)`.

## Frozen claims — before → after

Before column: the frozen controls committed at the freeze (`.ufo/waves/round-36/c1-controls/before.txt`,
`c2-controls/before.txt`, `census-before.txt`), re-measured by this seat on the `b47f2cd` worktree. After
column: the frozen `claims.json` target, plus what the round's counter actually printed at each export. The
suite readings are the suite author's own runs (`wave1/ExecC1SuiteBuild.md` § Export runs) and are bound to
that seat's draft revision `ff616adc…`; the on-disk file is a **different** revision (`4db1ae70…`) that
appeared during this draft — see the `suite present` row below and § Open items 11.

### C1 — depth:verifiability (4, held)

| counter (E-check) | before, freeze `b47f2cd` | suite over `git archive` (author's runs) | target / state at draft |
|---|---|---|---|
| suite present | absent at every measurement this seat made (`ls` exit 2; `c1-controls/before.txt` `suite_missing=1`) | the export runs and selftest quoted below are bound to the **draft** sha256 `ff616adc045a…4720` (737 lines / 28,980 B, `bash -n` exit 0). A **different revision** appeared in the lane worktree at `12:54:34 -0300` during this draft: `corpus/instruments/r36-closure.sh`, **894 lines / 39,022 B, sha256 `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4`**, untracked, `bash -n` exit 0, same E1–E9 semantics read from its header | the `closed=9/9` claim must be run on the **landed** bytes; the payloads in this table are not a reading of `4db1ae70…` |
| E1 placeholder/hash binding | `placeholders=0`, `lane-hash-markers=0`; **3** distinct 40-hex commit tokens in the suite's five-line window rule (`9f9848816503…` `:987`, `7963976e60b2…` `:988`, `c1c6a5f826d2…` `:1130`), each `cat-file -t`=commit and `merge-base --is-ancestor b47f2cd`=yes (this seat reproduced the suite's `final-lane-commits=3,bound=3`) | `3266c993` → `placeholders=1,…,bound=2 closed=0`; `0aee0ef` → `placeholders=1,…,bound=3 closed=0`; `b47f2cd` → `placeholders=0,…,bound=3 closed=1` | E1 is **open at both r35 heads and closed at the round-36 freeze** |
| E2 round-34 density erratum | `erratum-row` 0 at `3266c993`, 1 at `0aee0ef` and at `b47f2cd` (`erratum-mean=6`) | see payload column | closed since `0aee0ef` |
| E3 registry exact basenames | `grep -cF 'r35-defect-closure.sh' SKILL.md` = **0**; `grep -cF 'r36-closure.sh'` = **0**; near-name literal `r-defect-closure` = 4 lines | `closed=0` at all three exports | **open at draft**; the two rows are the L1's landing |
| E4 round-35 results + provenance note | `.ufo/waves/round-35/wave1-results.json` tracked (`tracked-ref=1`, `tracked-index=1`); `.ufo/waves/round-35/wave1-results.json.provenance.md` **absent** (`provenance-note=0`) | `closed=0` at all three exports | **open at draft**; the note is the L1's landing. The committed note on disk is the *round-34* one (`round-34/wave1-results.json.provenance.md`, `e1c44301…`), which E4 does not read |
| E5 claims erratum d5 | `.ufo/waves/round-35/claims-erratum-d5.md` present (1 file) | `claims-erratum-d5=1 closed=1` from `0aee0ef` on | closed |
| E6 correction note | `.ufo/waves/round-34/wave1/L1Integration.md` carries `Correction (round 35)` (1) | closed from `0aee0ef` on | closed |
| E7 supersedes rows | `supersedes R22`=1, `supersedes R23`=1 (`QUALITY.md:249-250`) | closed from `0aee0ef` on | closed |
| E8 lesson correction + stale line | round-36 lesson absent → `m36-rows=0`; stale phrase in `round-35.md` = **0** at `b47f2cd` | `stale-line=1` at `0aee0ef`; `closed=0` at all three | **open at draft only on the `m36-rows` limb**; closed once this lesson lands |
| E9 quiescence | `git status --porcelain` = 9 lines (all untracked `.ufo/waves/round-36/*`); scratch seat dirs under `/fast/scratch/hyaku/kasegi-r36` = 47 at `15:5xZ` | `0aee0ef` → `status-dirty=9,head-match=0 closed=0`; `b47f2cd` → `status-dirty=9,…,head-match=1 closed=0` | **open at draft** by construction (a wave is running); must read 0/0 at filing |
| suite totals | — | `3266c993` (r35 base) → **`closed=0/9 exit=1`**; `0aee0ef` (r35 judged head) → **`closed=4/9 exit=1`** (E2/E5/E6/E7 closed; E1/E3/E4/E8/E9 open); `b47f2cd` (this freeze) → **`closed=5/9 exit=1`** (adds E1) | kill rule's two failure legs are already satisfied by the author's runs; the `closed=9/9` leg is unproven until the final head exists |
| `--selftest` | — | `selftest cases=9 failures=4` at the freeze — the four failing positives are exactly the four landings (E3, E4, E8, E9); every clause mutant rejected on its own reopened limb (`mutants=3/3` … `1/1`), and all three forged reports rejected (`judge=own-report accepted=0`, three `rejected=1`) | target `cases=9 failures=0 exit=0`. The green path is proven on a synthesized tree (freeze export + the three missing artifacts): `green_closed=9/9`, `E8 payload=m36-rows=2,stale-line=0` |

**The two closure-order readings this round is built on.** (a) The round-35 judge pinned `0aee0ef` and
routed six items (`corpus/lessons/round-35-verifier-spotcheck.md` § 5.1–§ 5.6; the frozen claim counts five
of them plus the two standing closure-order defects); the lanes that close them (`8ce6fb4`, `5a25337`, `bb2dc8c`, `48e6053`) were
committed 38 s–4 min 21 s **after** the driver printed `complete kasegi round=35` (`watchdog.log:1495`,
04:00:34). (b) At the judged head the placeholder was re-published in the round-35 section; at `b47f2cd`
`SCORECARD.md:1271` reads `final lane commit \`0aee0ef…\` (recorded in the closing commit)` — the
placeholder is gone, the hash is present but abbreviated to 7 hex, and the parenthetical survived.

### C2 — coverage (7, held)

| counter | before, freeze `b47f2cd` | target (frozen `after`) | state at draft |
|---|---|---|---|
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | **18** (F01–F18) | 19 (F19) | not landed |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | **52** (S001–S052) | 53 (S053) | not landed |
| S053 rows | 0 | 1 (tier A, mined, opened 2026-10-26) | drafted (`wave1/ScribeRowS053.md` § 1.1), not applied |
| `ls corpus/knowledge/*.md \| wc -l` | **47** | 48 | not landed; entry drafted (`wave1/ScribeEntryF19.md` § 6) |
| entries citing `^source: S053 ` | 0 | 1 | as above |
| harness | `entries=21 pass=21 exit=0` (`c2-controls/before.txt`) | `entries=22 pass=22 exit=0` incl. `PASS F19 ids=S053` | not measured at draft (owning seats: ExecC2Harness / RevHarnessSync) |
| `source-recheck --source S053` | manifest UNAVAILABLE (no `round-36/` snapshot) | exit 0, `Q1..Q4 occurrences=1` | measured against the drafted manifest only (`ExecC2Capture.md` § 4, `ExecManifestChecks.md` § 0) |
| census | 3 lines, `census_exit=0` (W04 S028/S029 only) | exit 0, same W04 pair, no new `W`/`E` | after-state not measured at draft |
| junk twin rejected | control not in tree | rejected | fixture drafted (`ExecC2JunkControl.md` § 2), not landed; see § Gate |
| capture binding | `records=42 bound=42 unbound=0` at `b47f2cd` (baseline) | `records=43 bound=43` after the landing | not measured at draft |

**C2's zero-cost trap, stated once.** The "uncovered EPSS ground" assertion must use
`EPSS|exploit prediction`, not `exploitation likelihood`: the latter already matches
`corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md:26` (1 file, 0 EPSS hits) and a gate
written against it would read red on a pre-existing file (`wave1/ScoutF19Open.md` § 3).

## Gate

### Candidates considered

| candidate | kind | outcome |
|---|---|---|
| F19 / S053 — FIRST EPSS page (`https://www.first.org/epss/`) | live-capture admission (C2) | **admitted** |
| `.ufo/waves/round-36/c2-controls/junk-f19.md` | do-nothing junk twin for C2 | **rejected** (quote not in the capture) |
| 7 staged package entries (`shokuknow/merge/kasegi/knowledge/…`) | assimilation candids | **all 7 refused**, no flip condition cleared |
| 7 quarantine register rows (`absent-defect-register.md`) | quarantine slice | **0 adopted** (2 absent, 4 unreachable, 1 duplicate of lane S040) |

### Admitted — F19 / S053 (FIRST Exploit Prediction Scoring System)

- **Row** (`corpus/SOURCES.md`, appended after `:58`; drafted `wave1/ScribeRowS053.md` § 1.1): id `S053`,
  source cell `FIRST EPSS documentation page — https://www.first.org/epss/`, kind `docs`, tier **A** scoped
  to FIRST's own EPSS statements on the fixed page, anchor cell naming
  `corpus/source-snapshots/round-36/S053.txt` Q1 L216 plus the three supporting lines and the full sha256,
  `status mined`, `opened 2026-10-26`, `recheck 90d`,
  `used-by corpus/knowledge/epss-exploit-prediction-scoring.md` — 11 cells, no `|` inside a cell
  (`wave1/ScribeRowS053.md` § 2, measured on the drafted row).
- **URL:** `https://www.first.org/epss/` — requested URL == effective URL, **0 redirects**, HTTP **200**,
  `text/html; charset=UTF-8`, **26,804** served bytes = `content-length`, `last-modified: Thu, 30 Jul 2026
  13:48:13 GMT`. The trailing slash is load-bearing: `https://www.first.org/epss` answers **301** to the
  slashed form (`wave1/ScoutCaptureAvailability.md` § 1). UA-independent: plain `curl/8.0`, python urllib,
  the full instrument UA and the short UA all return the same 26,804 bytes
  (served-body sha256 `66fece529978e3b2…7868`).
- **Access date:** `2026-10-26T15:35:10Z` — the manifest's `fetched_utc` (strict ISO8601, `Z`), server
  `date:` header `Mon, 26 Oct 2026 15:35:06 GMT` (`wave1/ExecC2Capture.md` § 1). Re-opened live twice more
  the same minute: `15:36:36Z` (`wave1/ScoutF19Open.md` § 1) and `15:36:47Z`
  (`wave1/ScoutCaptureAvailability.md` § 1) — raw body `cmp`-identical, 0 differing normalized lines; this
  seat's own `capture-source.py` run at `15:36:30Z` produced a **byte-identical snapshot**
  (8,448 B, 244 lines, sha256 `4ec61c59b0e9aedf…83e9`).
- **Capture:** `corpus/source-snapshots/round-36/S053.txt`, 8,448 B, 244 lines, sha256
  **`4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`**; manifest 3,566 B
  (`f9590c2b…`), normalized with the lane's own `capture-source.py html_to_text()`.
- **Quote (≤25 words, located, exactly once):** `(EPSS) is a data-driven machine-learning model that
  estimates the probability that a published CVE will be exploited in the wild in the next 30 days.` —
  **25 words**, `S053.txt:216`, `occurrences=1`. The full L216 sentence (`The Exploit Prediction Scoring
  System (EPSS) is a data-driven…`) is **30 words** and is therefore recorded as the source sentence, never
  as a pin. Supporting pins: Q2 `EPSS publishes a 0–1 probability (with ranking percentiles)` (8 words,
  L217, occ 1, en dash U+2013 is the page's own character); Q3 `every day for every CVE and makes the data
  freely and openly accessible via CSV and API as well as a github repo` (23 words, L217, occ 1); Q4
  `EPSS is maintained by the EPSS Special Interest Group at FIRST. Scores are generated by Empirical
  Security and published freely to the community.` (23 words, L235, occ 1).
- **What the pin must not become.** The item brief's recommended Q1 wording (`EPSS is a data-driven
  machine-learning model …`) occurs **0** times — the page prefixes the model name — and a hyphen-tolerant
  count is a second trap (`is a…` is 24 tokens split on whitespace, 26 if `data-driven`/`machine-learning`
  are re-split). Both are recorded in `wave1/ScoutF19Open.md` § 2, found before the entry was drafted.
- **Distinctness, as a measured vocabulary fact, not an assertion about CVSS.** In the capture: `CVSS`
  **33 occurrences across 28 lines** (this seat's re-count; dominated by site navigation, with the page's
  own prose at L222 and L224 — `wave1/ScribeEntryF19.md` § 3 V8), `severity` **0**, `KEV` 2 lines (the
  "Using EPSS" sentence that names combining EPSS with CVSS and KEV), `probability` 2 lines (L216, L217).
  So the page defines a *probability with percentiles* and hands severity and KEV membership to other
  documents; the entry states that split and does not claim the page measures severity.
- **Freshness boundary:** the page body is dated `2026-07-30`, i.e. 88 days old at capture
  (`wave1/ScoutF19Open.md` § 1). The capture pins content, not currency; `source-recheck` is a local byte
  check.
- **Admission history:** the entry's header was signed with a wrong capture digest
  (`4ec61c59b0a9aedf…`, one hex character off) and was caught by `wave1/ExecC2QuoteOnce.md` § 6 and
  reported by `wave1/ScribeRowS053.md` § 8; the entry's current bytes pin the manifest digest
  (correct-digest lines `wave1/ScribeEntryF19.md` `:46,:73,:87,:124,:143,:394`), and `ExecC2QuoteOnce`
  records `PASS on the final entry bytes (36df1b1f9b4f…a641, 17,374 B / 263 lines)` — the earlier
  `c4f7d5b4e16f…88e0` (17,327 B) is the intermediate first-fix revision, not the final one
  (`wave1/ExecC2QuoteOnce.md:3,:22,:28-29,:161-162`). The wrong string survives only inside those two
  records and two
  observations, so **a future grep for `b0a9` will find record sections, not live pins** — the trap is
  recorded in § Open items.

### Rejected — the junk twin does not yet discriminate on the instrument alone

`c2-controls/junk-f19.md` is **not in the tree** at this draft's instant
(`git ls-tree -r b47f2cd | grep -c junk-f19` = 0; no lane-root `c2-controls/` exists). The fixture is
drafted (`wave1/ExecC2JunkControl.md` § 2, sha256 `ea078f05b057…fc8b`): it copies the real entry's header
shape, cites S053, and carries the fabricated sentence `EPSS guarantees exploitation within 30 days for
every scored CVE.` — measured **0 occurrences** in the capture by this seat and by
`wave1/ExecC2QuoteOnce.md`. Its `recheck:` line names the *real* S053 manifest, so `source-recheck` alone
selects the real capture and exits 0: that is M35-5's class recurring on the next round's control. The
discriminating form is therefore the quote comparison (fabricated sentence count 0 vs Q1 count 1), not the
instrument exit code, and the rejection also has a second limb no counter needs: no frontier row names the
fixture (`grep -c junk-f19 corpus/README.md` = 0).

**Frozen-control defect, recorded rather than smoothed:** `c2-controls/before.txt` prints
`"junk_present": "1"` while no `junk-f19.md` exists at `b47f2cd` in any path and the item spec's replay
list does not include the key. The key is unbacked by any recorded command; the junk-twin rejection is
provable only from `wave1/ExecC2JunkControl.md` and `wave1/MutJunkTwin.md`, never from the frozen control.

### Rejected — quarantine slice: 7 rows, one fetch each, 0 adopted

Derivation is the frozen awk over the read-only register
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(sha256 `5afe1810a6c3d62f…bad833`, 375 lines — unchanged since round 33). This seat re-ran it: 7 lines,
417 B, sha256 `d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862`, `cmp` against the
round-35 committed slice → identical; 7/7 lines carry an S-id. Register lines `:99` S037, `:100` S054,
`:322` S048, `:323`–`:326` S065/S068/S069/S070 (the last five carry a stray trailing backtick from the
register's own cell). `## By lane` counts kasegi 2 because it counts only the `payload-absent` table;
2 + 5 = 7, and neither count is a missing row.

Verdicts below are `wave1/ScoutQuarantine.md` § 2 (one `curl -sS -L --max-time 30` per row, instrument UA,
TLS verified, window `15:37:16Z`–`15:38:00Z`); this seat did not re-fetch.

| id | register class | live fetch 2026-10-26 | verdict | adopted |
|---|---|---|---|---|
| S037 | `payload-absent` | 200, 24,189 B `text/html;charset=utf-8`, sha256 `9cba2e96…`, 0 redirects | **absent** — the register's quote is a four-cell composite; each fragment located once, no contiguous span (facts hold: GB/T 30279-2020, 发布 2020-11-19 / 实施 2021-06-01) | no |
| S054 | `payload-absent` | 200, 513,648 B `application/pdf`, sha256 `0150c9d1…` | **absent** — the quote elides the statutory parenthetical and crosses a line-wrap; full clause present only under the whitespace-removed fold | no |
| S048 | never checked | **404**, 748 B Tomcat `HTTP状态 404 - 未找到`, sha256 `95cd25d8…` | **unreachable** — dead record id on a live host; the register carries no quote, so nothing is testable and this is not a fabrication | no |
| S065 | never checked | 200 headers, then curl exit 28 at 30.00 s; 677,543 of 7,465,472 B (9.1 %) | **unreachable (this probe)** — truncated PDF has no trailer, so **no anchor was checked this round**; transport, not source | no |
| S068 | never checked | `301`→`301`→`200` at `sec.cloudapps.cisco.com`, 94,027 B, sha256 `098f99a8…` | **present-and-located**, and the document **is already lane row S040** (same URL) | no — duplicate |
| S069 | never checked | `302` → `kass.sacinfo.org.cn` token URL, **curl exit 60**, 0 B | **unreachable** under a verifying client; the token URL is per-request and cannot be bound by a manifest | no |
| S070 | never checked | same transport, **curl exit 60**, 0 B | **unreachable** (same) | no |

Totals: present-and-located 1 · absent 2 · unreachable 4 · adopted **0**. Two things the Gate keeps from it:

1. **A label the round could not settle by definition alone.** `ScoutQuarantine` files S037/S054 as
   `absent` (the register's own class: payload fetched cleanly, span in none of the folds);
   round 35's `ExecQuarantineSlice` filed the same bytes as `prose-class-unverifiable`
   (`.ufo/waves/round-35/assimilation/quarantine-verdicts.md` § 1–2), and round 35's own scout filed
   `absent`. The fetched bytes are identical (`9cba2e96…`, `0150c9d1…`); only the class name differs. Both
   readings agree the row is not adoptable as quoted and both agree it is a quote-form defect, not a
   fabrication. The scout asks for one label; **this lesson prints both and treats the label as an open
   L1/judge decision**, because the two names carry different accusations.
2. **S065 moved by transport only.** Rounds 33–35 fetched the full 7,465,472 B; this probe got 9.1 % inside
   the 30 s cap and no anchor was re-checked. A later reader must not read this row as "the document
   changed".

### Rejected — standing refusals: 7 staged entries, 0 flip conditions cleared

Package `/home/vgpnk/Projects/shokuknow/merge/kasegi/` is byte-identical to round 35: 70 files (67
knowledge + `SOURCES.append.md` + `MERGE-REPORT.{md,json}`), every mtime `2026-10-24 23:33:20 -0300`,
`SOURCES.append.md` sha256 `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb`. This seat
re-hashed all seven entries; every digest equals the round-35 value (`wave1/ScoutStandingRefusals.md` § 1).

| staged entry | digest | why it stays refused | flip condition (unmet) |
|---|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` | `120d8cd5…` | 0 located quotes; no executable recheck; `ground: F09` names a **different** admitted lane item | located quote + executable recheck + a non-colliding frontier id |
| `claim-packaging-and-report-quality.md` | `6ad64d78…` | body cites S036 = BILISRC V1.7 (`security.bilibili.com`), in no lane row and no capture; lane S036 is the Cybozu policy | an S036 row **for that document** + capture |
| `cn-crowdsourced-testing-roles-and-conduct.md` | `a5302aaf…` | H1 count 0; S081/S082 appear only as refusal prose at `corpus/SOURCES.md:76-77` | an entry shape + the two rows |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | `6c15d941…` | S077/S078/S079 in no row/capture (the only `S077.txt` string is a `kill-rule-check.py` fixture); `ground: F24`, frontier ends F18 today | three rows + a real frontier id |
| `chinese-criminal-thresholds-and-authorisation.md` | `1660c00c…` | three PRC legal hosts → 0 hits in `corpus/` outside lessons; staged S044–S046 collide with lane rows of other documents | three rows + a renumber map |
| `chinese-program-severity-instrument.md` | `442e0f2b…` | `sse.com.cn` → 0 hits; staged S047 is SSE, lane S047 is the IPA JVN report; anchor `newsType_6` → 0 in `corpus/source-snapshots/round-32/S049.txt` (this seat re-measured: 0; `newsType_21` → 1) | the row + a locatable anchor |
| `program-severity-ladders-and-reward-scales.md` | `35de5f8b…` | same-name lane file differs (`6c05c98f3c6851b5…`, this seat re-hashed) | byte-identity or a supersedes row |

Refusals stand by **document identity, not by id number**: staged `S036`/`S047` ids now exist in the lane
registry but name different documents, so "a row exists" is not the flip condition being met.

### Assimilation: none

Zero staged entries and zero quarantine rows were adopted. The Gate's ≥1-admit leg is met by the round's
C2 admission (F19/S053, a live-capture admission); the ≥1-reject leg is met three times over (junk twin,
6 of 7 quarantine rows carrying a refusing verdict, 7 standing refusals).
`wave1/ScribeAssimilationGate.md` carries the same three components as a drop-in block with the same
numbers; **paste one of them, not both** — the two tables are equivalent and duplicating them would
double-count rows in a reader's tally.

#### Id-collision check — 52 vs 94, **22** standing, **23** predicted after the row lands

Frozen commands (0–3-space tolerant), run by `wave1/ScoutIdCollisions.md` § Commands and re-run by this
seat:

| list | count | range | note |
|---|---|---|---|
| registry ids (`corpus/SOURCES.md`, sha256 `0f95a132a69e…`) | **52** | S001–S052, contiguous | no duplicates |
| staged ids (`SOURCES.append.md`) | **94** | S031–S124, contiguous | same digest as round 35 |
| `comm -12` collisions | **22** | S031–S052 | after the S053 row: **23**, S031–S053 |

Staged `S053` is a **different document** — ソフトウェア…取扱規程（平成29年経済産業省告示第19号）,
`meti.go.jp/policy/netsecurity/vul_notification.pdf`, `SOURCES.append.md:29` — so the lane's S053 will
collide by number with a METI regulation while being adopted by document. That is the standing
scratch-side renumber class, not a lane defect. The guard is load-bearing and fails closed
(`wave1/ScoutIdCollisions.md` § Guard proof): a 2-space-indented collision row is caught by the 0–3-space
pattern and **false-greened** by the column-0-only pattern; missing registry path → exit 2; known limit
4-space indent / tab not caught. **Nothing is renumbered.**

### considerthese — `considerthese/2026-10-26.md` (2026-10-26)

| # | proposal | disposition | evidence |
|---|---|---|---|
| 1 | make "distance to next score" explicit | **computed** (gap reported; § Saturation criteria still not written) | `score-gap.py --root .` exit 0, `gap: 24 of 47 rechecks still gated on a lost base`; threshold quoted from `SCORECARD.md:331`; R26 at `QUALITY.md:249` |
| 2 | one end-to-end domain task round | **not this round** — recorded; SHONEN box 2 stays `[~]` | no domain-hunt seat among the 64 items; `SHONEN.md:108` unchanged |
| 3 | quiescence gate before completion | **adopted** → **R28** + C1's **E9** | `wave1/ScribeQualityRows.md` § 1 (R28); E9 in `claims.json` C1 and `wave1/ExecQuiescenceProbe.md` |
| 4 | cap / externalise wave evidence | **not this round** — needs an operator or LFS decision | footprint measured at the freeze by `wave1/ScribeConsiderthese.md` § 1: 6,905/7,175 tracked files and 109,375,581/115,034,856 blob bytes under `.ufo/` (96.2 %/95.1 %); no retention policy row exists |
| 5 | land the owed F18 `PROVINCE.md` amendment | **adopted** — with F19 this round | `PROVINCE.md` is 75 lines ending at the F17 amendment; `grep -c 'F18'`=0, `'F19'`=0 at the freeze |
| 6 | re-tune reflection cadence/depth | **recorded, no change** | R23 (`QUALITY.md:227`) and R27 (`:250`) already mandate next-round review, not a second daily run |
| 7 | keep a proposal-status ledger | **recorded, not started** | `corpus/knowledge/considerthese-proposals-ledger.md` exists (the round-30 landing); no 2026-10-26 section |

Proposals 3 and 5 are adopted in the round's frozen scope; at this draft's instant neither landing is
observable (no R28 in `QUALITY.md`, `PROVINCE.md` unchanged), so they are stated as adopted-with-landing-
pending, never as landed.

### Registry change log (old → new)

| cell | old | new |
|---|---|---|
| registry row count | 52 (S001–S052) | 53 (S001–S053) |
| S053 row | absent | `kind=docs`, `tier=A` (FIRST's own page statements only), `status=mined`, `opened=2026-10-26`, `recheck=90d`, `used-by=corpus/knowledge/epss-exploit-prediction-scoring.md`, anchor = S053.txt Q1 L216 + sha256 |
| staged/lane collisions | 22 (S031–S052) | 23 (S031–S053) — new collision is by number only, different document |
| knowledge entries | 47 | 48 |
| frontier rows | 18 (F01–F18) | 19 (F19) |
| capture records bound | 42 | 43 (`round-36/` manifest adds S053) |

### Census before → after

- **Before** (`.ufo/waves/round-36/census-before.txt`; replayed by `wave1/ExecCensusReplay.md` § 2, twice,
  identical):

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

- **After:** to be measured at integration on the landed registry with the same command
  (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`). The expected reading
  is the same three lines and exit 0 with registry 53 and the S053 URL carried once; **this draft records
  no after-value**, because none has been measured.

### Contested scope — none, ruled rather than left silent

The splice-ready ruling is `wave1/ConnSibling.md` (consolidating `wave1/ScoutF19Sibling.md` and
`wave1/ExecSiblingSweep.md`); this seat read the scout and did not re-run the sweep. In one line: **all 20
sibling lanes hold zero EPSS ground** under three formulations; near-matches are classified non-ground
(`epssweep` Godot test identifiers, the `LeinenEPSSJ24` bibliography key, encoded-substring noise, generic
`exploitation` boilerplate); kagi's retained NVD probes carry SSVC fields (a different framework), mori's
CVSS hits are raw advisories; `kasegi` is the fleet's only vulnerability-domain lane. Doctrine assigns
`first.org` at domain level but has no host-table row for it (contrast F18's `cisa.gov` row at
`shokuknow/doctrine/channel-recurrence.md:62`), so the host row is owed to the read-only campaign and is
**report-only** here.

### Non-author spot-check — result pending

No spot-check artifact exists at this draft's instant: `.ufo/reports/round-36/kasegi.md` and
`corpus/lessons/round-36-verifier-spotcheck.md` are absent (`ls` exit 2 for both). The sample plan exists at
`wave1/RevSpotCheckReadiness.md`. When the verifier files, this section must carry: its verdict line
(admitted / rejected-honest-stop / other), the per-claim C1/C2 re-derivation at the pinned head, its own
`git archive` run of `r36-closure.sh` (`closed=9/9 exit=0` is the claim; anything else is the finding), and
its routed defects for round 37. **Until that text exists, nothing in this lesson certifies the round**, and
no axis score moves.

## Mistakes

Numbering follows `claims.json` `non_claim_frontier_items.mistake`, which fixes the set at **M36-1…M36-4** —
exactly four rows, and (unlike round 35) no provisional tail. The full rows — class · event · evidence with
a re-runnable command · captured-by · fix with its landed state · fix shown able to fail — are in
`.ufo/waves/round-36/wave1/ScribeMistakes.md` § 1 in that six-field form; the bullets below are the anchors,
one line per row, and the six-field rows are to be appended under them at integration (the `M36` grep E8 runs
counts either form). Field vocabulary is kaika §5 (landing, closure-order, stale-premise,
counter-discrimination, number-drift, reference-drift, scope, attribution, provider).

- **M36-1 — recurrence of M35-1: claim-bearing work landed after the driver's `complete` line.** Class
  `landing`/`closure-order`; captured-by `none` (new), criterion missed R4. Fix this round: E9 quiescence
  (status + scratch seat dirs + head match) and an export-bound suite. Red/green: a dirty tree with one
  modification and one untracked file prints `2`; a clean tree prints `0`.
- **M36-2 — a false evidence line survived in a lesson.** The round-35 lesson's § Gate asserted
  `source-recheck` exit 0 "on committed bytes" while the capture it named was uncommitted at the judged head;
  the same § No-harm numstat claims were false there. Class `stale-premise`; captured-by R16. **The correction
  this round is this lesson's recording of it and the E8 limb**: `grep -cF` of that sentence in
  `corpus/lessons/round-35.md` reads **1** at `0aee0ef`/`5a25337`/`48e6053` and **0** at `980aa3d` and at
  `b47f2cd` — the lane removed it in a post-completion commit, so E8's stale-line limb is already green at
  the round-36 freeze and the E8 check cannot distinguish "never written" from "removed afterwards". Red/green:
  the sentence count flips 1 → 0 across those revisions; E8's other limb (`M36` present in this lesson)
  flips 0 → ≥1 when this file lands.
- **M36-3 — the D3 registry row never landed and a near-name literal satisfied the old counter.** Class
  `counter-discrimination`; captured-by R17 limb / R11. `grep -cF 'r35-defect-closure.sh' SKILL.md` = **0**
  at `b47f2cd` while `grep -cF 'r-defect-closure'` = 4 lines. Fix: E3's two exact basenames + R29. Red/green:
  a tree holding only the near-name row reads exact 0 (open), one with both exact rows reads 1/1 (closed).
- **M36-4 — the report was re-filed after `complete`.** Class `landing`; captured-by R4. Round-35's report
  landed at 04:00:23 and was re-filed at 04:01:19, 04:02:33 and 04:20:03, all after the 04:00:34 completion
  line. Fix: full integration before the single report commit; the report lands last. Red/green: the epoch
  predicate `report_ct ≥ max(lane_ct)` is red for the first three filings and green only for the last.

Cleared on re-check and deliberately **not** minted: the EPSS page's 301 on the slashless URL (external
behaviour, and the manifest carries the slashed canonical form); the 30-second S065 timeout (transport, no
claim rests on it); the recommended-Q1 wording defect (caught before landing — it is a finding of the round,
not a mistake in landed bytes); the entry's wrong capture digest (caught and fixed pre-landing by
`ExecC2QuoteOnce` § 6 and `ScribeRowS053` § 8).

## Sections this draft does not own

| section | owner receipt | state |
|---|---|---|
| `## considerthese` (long form) | `wave1/ScribeConsiderthese.md` § 2 | drafted; § considerthese above is this seat's summary of the same seven proposals |
| `## No-harm` (density, anchorcheck, numstat, unowned writes) | `wave1/RevNoHarm.md` (absent at this draft's instant), `wave1/ExecRegressionBase.md` | pending; no values quoted here |
| `## Census before → after` (after column) | `wave1/ExecCensusReplay.md` (before) + the L1's post-landing run | after-value pending |
| SCORECARD `## Round 36` section | `wave1/ScribeScorecard.md` | filed at the draft instant; not read by this seat, no score move quoted |
| `## SHONEN` | `wave1/ScribeShonen.md` | filed at the draft instant; not read by this seat |
| `## LOG` entry | `wave1/ScribeLOG.md` | filed at the draft instant; not read by this seat |
| QUALITY rows R28/R29 | `wave1/ScribeQualityRows.md` § 1 | drafted, append-only block after `:250` |
| report, suite, fixtures, capture, registry row, lesson-return | the C1/C2 executor seats and the L1 | this draft records what each has measured, and marks the rest pending |

## Open items / unverified

1. **The cluster of values that are targets, not measurements**: F19 row, S053 row, EPSS entry, harness
   `22/22`, `source-recheck S053` on the landed manifest, census after, knowledge 48, junk-twin rejection,
   `closed=9/9`. Each belongs to a named receipt; none is read here from landed bytes.
2. **E3, E4-provenance and E8's `m36-rows` limb are the three landings the suite reports open at the
   round-36 freeze** (`b47f2cd` → `closed=5/9 exit=1`). Until they land, the suite's own reading of this
   tree is 5/9, and a `closed=9/9` claim must name the export it was measured on.
3. **`c2-controls/before.txt` `junk_present=1` is unbacked** by any file or recorded command (§ Gate). The
   frozen control cannot carry the junk-twin rejection.
4. **The quarantine label for S037/S054 is unresolved** (`absent` this round and last round's scout vs
   `prose-class-unverifiable` last round's executor). Bytes identical; only the accusation differs.
5. **`b0a9` survives in record sections.** The entry's wrong digest lives on in `ScribeRowS053.md:149,158`,
   `ExecC2QuoteOnce.md:140`, `ScribeEntryF19.md:116` (correction note) and `MutJunkTwin.md:88`
   (observation). A future check that greps the tree for the bad digest must exempt record sections or it
   will read four files red on a closed defect.
6. **S065's row moved by transport only** (9.1 % of bytes inside a 30 s cap; no anchor checked). Do not read
   it as a source change.
7. **The 25-word pin is a ceiling, not a target**: the definitional sentence is 30 words and the pin starts
   mid-sentence at `(EPSS)`. A reader who re-extracts the sentence and re-counts will get 30; the manifest's
   `location` field records the full sentence so the truncation is visible rather than silent.
8. **The EPSS capture is 8,448 B** (served 26,804 B) — well inside the commit ceiling; the raw HTML is not
   committed, so re-deriving the served-byte digest requires a fresh fetch, which will drift when FIRST
   edits the page (body dated `2026-07-30`).
9. **This lesson's § Gate is a re-open of receipts, not an audit of them.** Every number carries its receipt;
   nothing here re-executed the suite, the harness or `source-recheck`, and no sibling lane was re-swept.
10. **E1 cannot see an abbreviated round-36 closing hash.** E1 binds 40-hex tokens only, and the round-35
   section's line (`SCORECARD.md:1271`) abbreviates its hash to 7 hex (`0aee0ef…`), so it contributes
   nothing to the counter while the two older sections contribute three bound tokens. If the round-36
   section writes its own hash the same abbreviated way, `final-lane-commits=3,bound=3` stays green without
   ever checking the round this claim is about. The closing commit should write the full 40-hex on its
   `Final lane commit:` line, and a later round's E1 should require the *last* such line's token to be 40-hex
   and an ancestor of the exported ref.
11. **Two revisions of the suite exist and only one has been measured.** `corpus/instruments/r36-closure.sh`
   appeared in the worktree at `12:54:34 -0300` (894 lines / 39,022 B, sha256 `4db1ae70…`, untracked,
   `bash -n` exit 0). The export readings and the selftest in § Frozen claims are bound to the 737-line
   revision `ff616adc…` (`wave1/ExecC1SuiteBuild.md`). Semantics match on a header read (E1 five-line window
   and ancestry, E3 exact basenames, E4 `.provenance.md`, E8 `M36` plus the stale line, E9 status/scratch/
   head), but a `closed=9/9` claim must be run on the bytes that are committed, and the suite's own digest
   must be recorded in the closing receipt (round-28 convention, restated because round 35's suite drift was
   the reason).
---END LESSON---

## 2. Measurements this receipt rests on (command → output, all at `b47f2cd` unless stated)

### 2.1 Lane state and base counters

```
$ git rev-parse HEAD
b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6
$ git status --porcelain | wc -l
9                          # all under .ufo/waves/round-36/; no corpus/ or SKILL.md path dirty
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md
18
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
52
$ grep -cE '^\|[[:space:]]*S053[[:space:]]*\|' corpus/SOURCES.md
0
$ ls corpus/knowledge/*.md | wc -l
47
$ ls corpus/instruments/r36-closure.sh
ls: cannot access 'corpus/instruments/r36-closure.sh': No such file or directory   # exit 2
$ wc -l < PROVINCE.md ; grep -c 'F18' PROVINCE.md ; grep -c 'F19' PROVINCE.md
75 ; 0 ; 0
$ grep -n '^| R23\|^| R26\|^| R27' corpus/QUALITY.md | cut -c1-6
227 ; 249 ; 250
```

Frozen controls read verbatim (`.ufo/waves/round-36/{c1-controls/before.txt,c2-controls/before.txt,census-before.txt}`):
`suite_missing=1, placeholder_filled=0, placeholder_angle=0, r36_registry=0, r35_registry=0,
scratch_leftovers=0, worktree_clean=0`; `frontier=18, registry_rows=52, s053_rows=0, entries_citing=0,
knowledge_entries=47, harness=entries=21 pass=21 exit=0, junk_present=1`; census 3 lines + `census_exit=0`.

### 2.2 The suite's own export readings (read, not re-executed)

`wave1/ExecC1SuiteBuild.md` § Export runs, draft sha256 `ff616adc045a…4720`, 737 lines, `bash -n` exit 0:
`3266c993` → `closed=0/9 exit=1`; `0aee0ef` → `closed=4/9 exit=1`; `b47f2cd` → `closed=5/9 exit=1`;
selftest at HEAD `cases=9 failures=4`; green-path proof on a synthesized tree `green_closed=9/9`.

**Those payloads are not a reading of the bytes now in the lane.** During this draft the worktree gained
`corpus/instruments/r36-closure.sh` (mtime `2026-10-26 12:54:34 -0300`, untracked at this read):
**894 lines / 39,022 B, sha256 `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4`**,
`bash -n` exit 0. This seat hashed and header-read it read-only and **did not execute it**; the header states
the same E1–E9 semantics (five-line E1 window plus ancestry, E3 exact basenames, E4 `.provenance.md`, E8
`M36` plus the stale line, E9 status/scratch/head). A `closed=9/9` claim must be run on the committed bytes
and the suite's digest recorded in the closing receipt.

### 2.3 E-check subjects measured by this seat

```
$ T1=$(printf 'filled by the %s' 'L1'); grep -cF "$T1" SCORECARD.md          # 0
$ T2=$(printf '<LANE%s>' '_HASH');     grep -cF "$T2" SCORECARD.md          # 0
$ grep -cF 'r35-defect-closure.sh' SKILL.md ; grep -cF 'r36-closure.sh' SKILL.md ; grep -cF 'r-defect-closure' SKILL.md
0 ; 0 ; 4
$ git ls-files .ufo/waves/round-35/wave1-results.json | wc -l                 # 1
$ ls .ufo/waves/round-35/wave1-results.json.provenance.md                     # absent (exit 2)
$ ls .ufo/waves/round-34/wave1-results.json.provenance.md                     # present (e1c44301…)
$ ls .ufo/waves/round-35/claims-erratum-d5.md | wc -l                         # 1
$ grep -cF 'Correction (round 35)' .ufo/waves/round-34/wave1/L1Integration.md # 1
$ grep -c 'supersedes R22' corpus/QUALITY.md ; grep -c 'supersedes R23' corpus/QUALITY.md
1 ; 1
$ ls corpus/lessons/round-36*.md                                              # absent (exit 2)
```

E1 token reproduction (the suite's own five-line window rule, re-implemented read-only):

```
window hits: (987,987,9f9848816503aa0cd566fc2efdc5e69ea501a253)
             (987,988,7963976e60b2564860553c6ab4838128d5ca06ea)
             (1129,1130,c1c6a5f826d2425446347173de527c42991b78b0)
unique: 3   each: cat-file -t = commit ; merge-base --is-ancestor <h> b47f2cd = yes
=> reproduces the suite's `final-lane-commits=3,bound=3`
```

E8 stale-line history (the phrase is assembled so this receipt does not itself contain it literally):

```
$ P=$(printf 'source-recheck exit 0 on %s' 'committed bytes')
$ for r in 0aee0ef 5a25337 48e6053 980aa3d b47f2cd; do git show $r:corpus/lessons/round-35.md | grep -cF "$P"; done
1 1 1 0 0
```

E9, at the draft instant (a wave is running, so a red E9 is expected here and is not a defect):

```
$ git status --porcelain | wc -l                                              # 9
$ find /fast/scratch/hyaku/kasegi-r36 -mindepth 1 -maxdepth 1 -type d | wc -l  # 47 (seats live at this instant)
```

### 2.4 F19 / S053 capture and pins

```
$ python3 corpus/instruments/capture-source.py --id S053 --url https://www.first.org/epss/ \
      --out $S/S053.txt --kind html
S053 status=200 fetched_bytes=26804 snapshot_bytes=8448 \
     sha256=4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9 utc=2026-10-26T15:36:30Z
$ wc -l S053.txt                                                              # 244
$ grep -cF -- '(EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days.' S053.txt
1                     # L216, 25 words
$ grep -cF -- 'EPSS publishes a 0–1 probability (with ranking percentiles)' S053.txt            # 1 (L217, 8 words)
$ grep -cF -- 'every day for every CVE and makes the data freely and openly accessible via CSV and API as well as a github repo' S053.txt   # 1 (L217, 23 words)
$ grep -cF -- 'EPSS is maintained by the EPSS Special Interest Group at FIRST. Scores are generated by Empirical Security and published freely to the community.' S053.txt   # 1 (L235, 23 words)
$ grep -cF 'EPSS is a data-driven machine-learning model' S053.txt             # 0  <- the item brief's recommended Q1 is not on the page
$ grep -cF 'EPSS guarantees exploitation within 30 days for every scored CVE' S053.txt   # 0  <- the junk twin's fabricated sentence
$ grep -ciF 'severity' S053.txt                                               # 0
$ grep -oF 'CVSS' S053.txt | wc -l ; grep -cF 'CVSS' S053.txt                 # 33 occurrences / 28 lines
$ grep -ciF 'KEV' S053.txt ; grep -ciF 'probability' S053.txt                  # 2 ; 2
```

Lane negative sweep for the uncovered-ground claim:

```
$ grep -rilE 'EPSS|exploit prediction' corpus/knowledge corpus/README.md corpus/SOURCES.md SKILL.md | wc -l
0
$ grep -ril 'exploitation likelihood' corpus/knowledge | wc -l
1        # corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md:26 — pre-existing, not EPSS
```

### 2.5 Quarantine slice and id collisions (re-derived by this seat)

```
$ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
$ sha256sum "$R" ; wc -l "$R"
5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833 ; 375
$ awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" > quarantine-slice
$ wc -l quarantine-slice ; sha256sum quarantine-slice
7 ; d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862
$ cmp quarantine-slice .ufo/waves/round-35/assimilation/quarantine-slice     # identical (exit 0)

$ P='^ {0,3}\|[[:space:]]*S[0-9]{3,}'
$ grep -oE "$P" corpus/SOURCES.md | grep -oE 'S[0-9]{3,}' | sort -u > reg-ids        # 52
$ grep -oE "$P" /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md | grep -oE 'S[0-9]{3,}' | sort -u > staged-ids   # 94
$ comm -12 reg-ids staged-ids | wc -l ; comm -12 reg-ids staged-ids | tr '\n' ' '
22 ; S031 S032 … S052
$ sha256sum /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md
4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb
$ grep -n '^|[[:space:]]*S053[[:space:]]*|' .../SOURCES.append.md            # :29 METI 平成29年経済産業省告示第19号 (different document)
```

### 2.6 Standing refusals (re-hashed by this seat)

```
120d8cd5d50b703809a1c1030eb3b16564251e69a8208e4c90b500343d99abc8  program-scope-rules-and-asset-boundaries.md
6ad64d785f8f767bc0e86a4967b80bcc636b5939af4ac41b1138911978ec8dbc  claim-packaging-and-report-quality.md
a5302aaf0b9a1502c8711cd620cf0cb87cd9fea8db192269fae31619548fe813  cn-crowdsourced-testing-roles-and-conduct.md
6c15d94114248beb433eeb35aca116eb2ff4beaf7abfbc9d2b9957aeb56ef83f  chinese-crowd-testing-national-standard-2026-10-23.md
1660c00c16369d0a50870185607e0a8006ed573cc4ae69a696ce568e4e8a59ae  chinese-criminal-thresholds-and-authorisation.md
442e0f2bfb08bc2cbb8951f110e64424f82203636928429bc38f46f388c4257c  chinese-program-severity-instrument.md
35de5f8b19ed3b20beb3d41c347f4727d9fd2eefc8a23e53c64c6987b60bbc87  program-severity-ladders-and-reward-scales.md (staged)
6c05c98f3c6851b560098b8f7c43350a951e487e8b34e2ff09831563aa8ff4a6  same name, lane copy (≠ staged)
```

Flip-condition spot-checks re-run by this seat: registry rows `S077=S078=S079=S081=S082=0`; `F24` → 0 in
`corpus/README.md` (frontier ends F18); `newsType_6` → 0 in `corpus/source-snapshots/round-32/S049.txt`;
staged `S036` body cites `security.bilibili.com/…/BILISRC_V1.7.pdf` while lane row `S036` is the Cybozu
policy; staged `S047` cites `sse.com.cn` while lane row `S047` is the IPA JVN report.

### 2.7 Wave shape

```
wave=kasegi-r36-build  reportDir=.ufo/waves/round-36/wave1  maxLanes=128  items=64  unique names=64
roles: executor 18, scribe 12, reviewer 10, critic 6, scout 6, mutation-tester 5, connector 3, sentinel 2, simplifier 2
wave1-spec.json 347380 B sha256 af5cf818a46aa01d…   wave1-dispatch.json 372309 B sha256 cbed673a26e05dba…
wave1.ready 170 B sha256 54d680399dd52317…  -> {"lane":"kasegi","round":36,"wave":"kasegi-r36-build",...,"l1":"KasegiR36"}
watchdog.log:1527  2026-10-26T12:31:14-03:00 launch kasegi round=36 pgid=14809 driver=hyaku-inline attempt=1
```

### 2.8 Post-draft integration record (measured after the draft was written)

The lane moved while this seat was drafting. Everything below is a read; the draft's "state at draft" cells
remain the draft-instant readings and are not retro-edited.

```
$ git log --oneline -4
a23dc47 round-36: final gate receipts + measured closure
274fa9a round-36: late receipt updates (Gate/Simpl)
e9c57c4 round-36: late seat receipt updates
2c26a97 round-36: E1 Final lane commit line, E4 provenance note, lesson hash
$ git show --stat --oneline caa3146 | head -3
caa3146 round-36: integration — r36-closure suite, F19 EPSS capture+entry+S053 row, R28/R29, PROVINCE F18/F19, SKILL registry, lesson/scorecard/SHONEN/LOG drafts
 corpus/instruments/r36-closure.sh                   | 894 +++++
 corpus/knowledge/epss-exploit-prediction-scoring.md | 263 ++++++
 corpus/lessons/round-36.md                          |  45 ++
```

| subject | landed value (read at `HEAD`) | how measured |
|---|---|---|
| suite | `corpus/instruments/r36-closure.sh`, 894 lines, sha256 `4db1ae70c76afd28b29e9ec24c2e44835322c61fa33e30c966f75ce0dfadb7c4`; the committed blob digest equals the worktree digest | `sha256sum`, `git show HEAD:… \| sha256sum` |
| capture | `corpus/source-snapshots/round-36/S053.txt`, sha256 `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9` — **identical to the capture this seat produced independently** | `sha256sum` |
| manifest | landed file digest `dd591cd4743b148db492cce78932a01125a4b7b69f7d4f1e40732dee48566a85`; the record is semantically the drafted one (`url`, `fetched_utc 2026-10-26T15:35:10Z`, `fetched_bytes 26804`, `lines 244`, same capture sha256, pins Q1/Q2/Q3/Q4 at anchors 216/217/217/235 with 25/8/23/23 words). The **file** digest differs from the drafted `f9590c2b…` (formatting at landing) | `python3 -c` over the JSON + `sha256sum` |
| registry / frontier / knowledge | rows **53** (`S053` present), frontier **19**, knowledge **48**, entries citing `source: S053` **1** | the frozen greps in § 2.1 |
| E3 registry rows | `r35-defect-closure.sh` **1**, `r36-closure.sh` **1** | `grep -cF` on `SKILL.md` |
| QUALITY / PROVINCE | `R28` **1**, `R29` **1**; `PROVINCE.md` 78 lines with `F18` **1** and `F19` **1** | `grep -c '^\| R28 '`, `wc -l`, `grep -c` |
| E4 provenance note | `.ufo/waves/round-35/wave1-results.json.provenance.md` **present** | `ls` |
| lesson | `corpus/lessons/round-36.md` exists as **45 lines / 4,939 B, sha256 `cea4fcaffc77904f1295a87cfeef2a73481c581c98d6034995ee439cc0e43080`** — a condensation, **not** the 413-line draft in § 1 | `wc -lc`, `sha256sum` |
| L1 closure reading (read, not re-run) | `.ufo/waves/round-36/final-gates/all-gates.txt` and the `SCORECARD.md` append: export `274fa9ae…` → `closed=9/9 exit=0`; `--selftest cases=9 failures=0`; negatives `3266c993` → `0/9 exit=1`, `0aee0ef` → `3/9 exit=1`; C2 `entries=22 pass=22`, `source-recheck S053` exit 0 with Q1–Q4 `occurrences=1`, `capture-binding-check records=43 bound=43` | file read; this seat executed none of them |
| census | this seat's own run still prints **three** lines — `W04 S028`, `W04 S029`, `ok`, `census_exit=0` — while the `final-gates` artifact shows only `W04 S029` and `ok` | `bash ../scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` |

**A counter-reading on the selftest, peer-reported and not re-run here.** `RevSpotCheckReadiness` reports that
`--selftest` on the **landed** suite at HEAD `a23dc478` prints `cases=9 failures=1` (its E9 positive fails at
`status-dirty=5, scratch-seat-dirs=3` mid-wave), and that it re-ran the negative controls itself: landed suite
`0aee0ef` → `closed=3/9 exit=1`, base `3266c993` → `closed=0/9 exit=1`. That is consistent with E9's design —
quiescence is a property of the live lane, so `cases=9 failures=0` is only measurable at the quiescent head the
closure was run at (`274fa9ae…`), not at a head with wave receipts still untracked. Consequence for a reader:
**every `cases=` and `closed=` figure must carry its head *and* the digest of the suite that printed it**; the
`4/9` in § 2.2, the `3/9` above and the `failures=1` here are three different (head, suite) pairs, not three
opinions about one measurement.

## 3. What this seat did not do

- Did not write `corpus/lessons/round-36.md`, `SCORECARD.md`, `SKILL.md`, `QUALITY.md`, `PROVINCE.md`,
  `corpus/SOURCES.md`, `corpus/README.md`, any snapshot/manifest, any instrument, or any sibling/source tree.
- Did not execute `r36-closure.sh` — absent from the lane at every measurement this seat made, and the
  revision that appeared later (`4db1ae70…`) was hashed and header-read only — nor the F19 harness,
  `source-recheck.py`, `capture-binding-check.py`, the census, or `score-gap.py`. Their readings are cited to
  the receipts that ran them, with the receipt named at each number.
- Did not fetch any quarantine row (one fetch per row belongs to the scout); did not re-fetch the EPSS page
  beyond the single `capture-source.py` run in § 2.4.
- Did not re-sweep sibling lanes; the contested-scope ruling is `wave1/ConnSibling.md`, and this seat read the
  scout half of it only.
- Did not open `RevNoHarm`, `ExecC2Harness`, `MutC2Entry` or `CritC2Kill` (not filed at the draft instant), so
  no no-harm value, harness count or mutation verdict is quoted from them.

## 4. Findings register (for the canonical judge; not resolutions)

1. **`c2-controls/before.txt` `junk_present=1` is unbacked.** No `junk-f19.md` exists at `b47f2cd` in any
   path (`git ls-tree -r b47f2cd --name-only | grep -c junk-f19` = 0; no lane-root `c2-controls/`), and the
   item spec's replay list does not include the key, so no recorded command produces it. Consequence: the
   frozen C2 control cannot carry the junk-twin rejection; the discrimination is provable only from
   `wave1/ExecC2JunkControl.md` (fabricated-sentence count 0 vs Q1 count 1) and `wave1/MutJunkTwin.md`, plus
   the no-frontier-row limb.
2. **S037/S054 carry two class names across rounds for identical bytes.** `wave1/ScoutQuarantine.md` files
   `absent`; round 35's `ExecQuarantineSlice` filed `prose-class-unverifiable` for the same fetched digests
   (`9cba2e96…`, `0150c9d1…`). Both agree the rows are not adoptable as quoted and not fabrications. The
   lesson prints both and leaves the label to the L1/judge, because the two names accuse differently.
3. **A closed digest conflict is still greppable.** The EPSS entry was signed with
   `4ec61c59b0a9aedf…` and corrected to `…b0e9aedf…` before landing (`wave1/ExecC2QuoteOnce.md` § 6,
   `wave1/ScribeRowS053.md` § 8). The wrong string survives in that record section (2 full strings), in
   `ExecC2QuoteOnce.md:140` (1 full string) and as abbreviations in `ScribeEntryF19.md:116` and
   `MutJunkTwin.md:88`. Current distribution in `wave1/`: 26 full correct strings, 3 full wrong strings.
   Any later check that greps for the bad digest must exempt record sections.
4. **E4's provenance-note path is round-35, while the committed note is round-34.**
   `check_e4` requires `.ufo/waves/round-35/wave1-results.json.provenance.md`; the note on disk is
   `.ufo/waves/round-34/wave1-results.json.provenance.md` (`e1c44301…`, the round-35 M35-1 fix). So E4 stays
   open until a round-35 note is written, and a reader who greps for "provenance" finds the wrong file first.
   Recorded as the L1's remaining landing, not as a suite defect.
5. **E1 cannot see an abbreviated round-36 closing hash.** E1 counts only 40-hex tokens; the round-35
   section's `final lane commit` line (`SCORECARD.md:1271`) abbreviates to 7 hex and contributes nothing, so
   `final-lane-commits=3,bound=3` can be green while the round-36 hash is never checked. Recommend writing the
   full 40-hex on the round-36 line (lesson § Open items 10).
6. **The item brief's recommended Q1 is not on the page** (`EPSS is a data-driven…` → 0 occurrences) and the
   definitional sentence is 30 words. Caught before landing by `wave1/ScoutF19Open.md` § 2; the pin used is the
   25-word span starting at `(EPSS)`.
7. **S065's quarantine row moved by transport only** (200 headers, 9.1 % of bytes inside a 30 s cap, no trailer,
   no anchor checked). Not a source change.
8. **Peer review applied, not merely received.** `SimplReport` (simplifier) reviewed the draft before landing and
   raised four items; this seat re-verified each against the receipts and applied all four: (a) the round-35
   spot-check routes **six** items (§5.1–§5.6), not five — the lesson now says six and records that the frozen
   claim counts five plus the two standing closure-order defects; (b) `ExecC2QuoteOnce`'s PASS is on the
   **final** entry bytes `36df1b1f9b4f…a641` (263 lines / 17,374 B), with `c4f7d5b4e16f…88e0` (17,327 B) the
   intermediate first-fix revision; (c) the entry's correct-digest lines are `:46,:73,:87,:124,:143,:394`
   (the earlier `:59,:85,:123,:373` list was stale after the fix); (d) the § Mistakes section now states that
   its four bullets are **anchors** and that the six-field rows from `wave1/ScribeMistakes.md` § 1 are appended
   under them, instead of claiming rows already pasted.
9. **The suite's measured revision and the suite's landed revision are different objects.** The export runs and
   the selftest quoted in § 2.2 belong to draft `ff616adc…` (737 lines / 28,980 B). The file present in the
   worktree at `12:54:34 -0300` is `4db1ae70…` (894 lines / 39,022 B, untracked, `bash -n` exit 0). Both are
   read-only facts; no `closed=K/9` value in this receipt was produced by `4db1ae70…`, and this seat did not
   execute it.
10. **The two suite revisions disagree on the negative control at the r35 judged head.** The draft suite reads
   `0aee0ef` → `4/9` (`wave1/ExecC1SuiteBuild.md` § Export runs); the landed suite's closure run reads
   `0aee0ef` → `3/9` (`.ufo/waves/round-36/final-gates/all-gates.txt`, `neg judged`). Both satisfy the frozen
   kill rule (`closed<9/9`), so the claim is unharmed, but a reader comparing the two receipts sees a
   one-check difference that is explained only by the revision change. Any later round quoting `4/9` must name
   `ff616adc…`, and any quoting `3/9` must name `4db1ae70…`.
11. **The closure artifact's census excerpt is not the command's full output.** This seat's own run at `HEAD`
   prints three lines — `W04 S028`, `W04 S029`, `ok`, `census_exit=0`; the `final-gates` C2 block prints only
   `W04 S029` and `ok`. The frozen claim's literal is "census exit 0 (W04 S028/S029 only)", which the
   three-line output satisfies and the two-line excerpt cannot demonstrate. Recorded; the re-runnable command
   is in § 2.8.
12. **The landed lesson is a 45-line condensation, not the draft in this receipt.** `corpus/lessons/round-36.md`
   is 45 lines / 4,939 B / sha256 `cea4fcaf…` and carries the claim values in summary form (including
   `final lane commit e666d902…` and the closure readings). This seat's 413-line draft (§ 1) was not pasted.
   That is the L1's call, recorded here so no reader assumes the draft is the landed text; the draft's value is
   the Gate detail the condensation does not carry (candidate table, label conflict, guard proof, refusal
   table, open items). The landed manifest's **file** digest is also not the drafted one
   (`dd591cd4…` vs `f9590c2b…`) while its record content is identical.

## 5. Touched surfaces and provenance

Production paths touched: **none**. This receipt is the only lane write. Inputs read (with the digests this
receipt binds):

```
b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6  lane HEAD (claims freeze)
0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba  corpus/SOURCES.md      (52 rows)
5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833  shokuknow absent-defect-register.md (375 lines)
4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb  shokuknow merge/kasegi/SOURCES.append.md (94 ids)
d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862  quarantine slice (7 lines, == round-35 committed)
4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9  round-36 S053 capture (this seat's run; 8448 B / 244 lines)
66fece529978e3b2f34c57b8c37b041a6d817f2cff135cf117375bf414117868  EPSS served body (this seat's fetch, 26804 B)
ff616adc045a8938c7ca69b3693565ef0f676a0d1d67df293b1b6c4a82da4720  r36-closure.sh draft (receipt-cited, not executed)
f9590c2bbc26244af88dce8fa7c291d67e6138c293ba5198257789911c017da3  round-36 manifest (receipt-cited)
732bcb1527e7255856e771a674ee409cf34318d1aa69a1cd68f14ed221a5156c  the lesson block as extracted from this receipt (413 lines, 37,641 B)
```

Receipts **opened** (content read; each cited where its number is used): `ExecC1SuiteBuild`, `ExecC2Capture`,
`ExecC2JunkControl`, `ExecC2QuoteOnce` (head + § 6), `ExecManifestChecks` (head), `ExecCensusReplay` (head),
`ExecQuiescenceProbe` (head), `ExecScoreGap` (head), `ScoutCaptureAvailability`, `ScoutF19Open`,
`ScoutF19Sibling`, `ScoutIdCollisions`, `ScoutQuarantine`, `ScoutStandingRefusals`, `ScribeAssimilationGate`
(head + drop-in block), `ScribeConsiderthese` (head), `ScribeEntryF19` (head + tail), `ScribeQualityRows`
(head), `ScribeRowS053` (head + § 8), `ScribeMistakes` (head), `ConnSibling` (splice block only).

Receipts **named but not opened** (present in `wave1/` at the draft instant, or absent): `ExecC1BaseFail`,
`ExecDatawalk`, `ExecGateReviewPrep`, `ExecInstrumentsSynopsis`, `ExecRegressionBase`, `ExecSiblingSweep`,
`CritMotivation`, `RevSourceRecheck`, `MutJunkTwin` (one line read at `:88` for the digest observation),
`ScribeLOG`, `ScribeScorecard`, `ScribeShonen`, `ScribeSOURCSCorrection`; **absent** at the draft instant:
`ExecC2Harness`, `RevNoHarm`, `RevHarnessSync`, `MutC2Entry`, `CritC2Kill`, and the remaining reviewer,
critic and sentinel seats.

## 6. Constraint checks on the deliverable

### 6.1 Placeholder tokens

```
$ T1=$(printf 'filled by the %s' 'L1'); grep -cF "$T1" lesson.md
0
$ T2=$(printf '<LANE%s>' '_HASH'); grep -cF "$T2" lesson.md
0
```

The tokens are assembled at run time so this receipt is not itself a carrier of the literals E1 counts.

### 6.2 E8's lesson limb

```
$ awk '/^---BEGIN LESSON---$/{f=1;next} /^---END LESSON---$/{f=0} f' ScribeGateLesson.md | grep -cF 'M36'
8
```

Eight lines in the lesson block: the numbering paragraph, the E8 note, the four row bullets, the "cleared on
re-check" line and the M36-3 cross-reference inside R29's citation. E8 requires ≥1.

### 6.3 E8's stale-line limb, stated as a limit

The draft does not quote the round-35 stale sentence literally (`grep -cF` for it in `lesson.md` = 0), and
`round-35.md` itself has not carried it since `980aa3d` (§ 2.3). The check therefore reads green at the freeze
whatever the lesson says; what makes the correction visible to a reader is the § Mistakes M36-2 text, not the
counter.

### 6.4 Size and shape

```
413 lines / 37,641 B / 5,346 words; sections: Shape, Frozen claims (C1, C2), Gate (candidates, admit, three
reject classes, assimilation, id collisions, considerthese, registry change log, census, contested scope,
pending spot-check), Mistakes, sections not owned, open items (11).
```
