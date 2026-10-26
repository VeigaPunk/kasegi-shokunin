# ScribeAssimilationGate — round-36 assimilation Gate block (draft)

Seat: `ScribeAssimilationGate` (scribe, wave 1, round 36). Answering model: `opencode-go/deepseek-v4.1-flash`.
Role: draft the **assimilation Gate block** for `corpus/lessons/round-36.md`. This seat claims no axis score
and judges no claim: it re-derives three measurements read-only, reads the wave's three scout receipts, and
fills every count from them. Where a receipt and an older artefact disagree, both readings are printed.

- Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base `cc692008b0cfd58d18275aa6c4aed79620120799`;
  claims-freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`; `HEAD` at composition `b47f2cdf` (claims freeze).
  Working tree: 9 untracked `.ufo/waves/round-36/*` paths, `corpus/` clean.
- **State at composition** (`2026-10-26T15:39:46Z`): `corpus/SOURCES.md` 52 rows `S001`–`S052`
  (`sha256 0f95a132a69e…`), no `S053` row (`grep -c '^| S053 '` → 0); `corpus/README.md` 18 frontier rows
  `F01`–`F18` (`277f04cedfb0…`), no `F19`; `corpus/knowledge/` **47** entries. So every `S053`/`F19` figure
  below is the round's **prediction**, not a read of landed bytes (`§ 1` prints the projected value).
- All measurements read-only: no mutating `git`/`jj`, no lane instrument run, no package tool run
  (`renumber-staged.py`, `merge-plan.py`, `quote-lint.py`, `absent-defect-register.py` never invoked),
  nothing written under `/home/vgpnk/Projects/shokuknow`, no network call by this seat. **Tools installed:
  none.** Scratch `/fast/scratch/hyaku/kasegi-r36/ScribeAssimilationGate/` removed after this receipt
  (§ Report).
- Measurement window: this seat `15:36Z`–`15:40Z`; scout fetches `15:37:16Z`–`15:38:00Z`
  (`ScoutQuarantine` §2); `ScoutStandingRefusals` "reads at 2026-10-26T15:3xZ".

Inputs (digests read by this seat):

| path | sha256 (12 hex) | note |
|---|---|---|
| `shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` | `5afe1810a6c3` | 83,621 B, mtime `2026-10-24 08:37:00 -0300`; unchanged since round 33 |
| `shokuknow/merge/kasegi/SOURCES.append.md` | `4fe049cbe4ba` | 94 staged ids `S031`–`S124` |
| `shokuknow/merge/kasegi/MERGE-REPORT.md` / `.json` | `0e6759b47595` / `8a42a9109c8c` | package meta, unchanged |
| `corpus/SOURCES.md` | `0f95a132a69e` | 112 lines, 52 rows |
| `corpus/README.md` | `277f04cedfb0` | 396 lines, 18 frontier rows |
| `.ufo/waves/round-35/assimilation/quarantine-slice` | `d02acb68cb40` | 7 lines, 417 B — round-36 slice is byte-equal to it (§2) |
| `.ufo/waves/round-35/assimilation/collide-check.sh` | `6d17e641e943` | the committed collision guard, re-run here |
| `.ufo/waves/round-35/assimilation/scratch-registry.md` | `ee8088e5208f` | the indented-row guard fixture |
| `.ufo/waves/round-36/wave1/ScoutIdCollisions.md` | `afbb29ab08f1` | 3,538 B |
| `.ufo/waves/round-36/wave1/ScoutQuarantine.md` | `5170eae9a396` | 13,190 B |
| `.ufo/waves/round-36/wave1/ScoutStandingRefusals.md` | `8c70e10400fc` | 6,102 B |

---

## Gate block for `corpus/lessons/round-36.md` (drop-in)

### Assimilation: none adopted

Three components, measured read-only on 2026-10-26 against register `absent-defect-register.md`
(`sha256 5afe1810a6c3…bad833`) and package `/home/vgpnk/Projects/shokuknow/merge/kasegi/`
(`SOURCES.append.md 4fe049cb…73eb`, 70 files = 67 knowledge + 3 meta, newest mtime
`2026-10-24 23:33:20 -0300`). The Gate's **≥1 admit** leg is met by the round's C2 admission
(**F19 / S053**, a live-capture admission), **not** by an assimilation adoption; the **≥1 reject** leg is
met twice over — 6 of the 7 quarantine rows carry a refusing verdict (2 `absent`, 4 `unreachable`), the
seventh (S068) is already lane row `S040`, and all seven standing refusals stand. **Adopted: 0.** Each of
the three components is filled from that component's
scout receipt and re-derived where the derivation is mechanical (see **Provenance** and **Reproduction**).

#### 1. Id-collision check — 52 registry ids vs 94 staged ids, **22** collisions, guard shown load-bearing

`wave1/ScoutIdCollisions.md` § Result: registry **52** unique ids `S001`–`S052` (digest `2d95a2702fa2`),
staged **94** unique ids `S031`–`S124` (digest `550a0129a446`), `comm -12` → **22 collisions
`S031`…`S052`, contiguous**, no duplicates inside either list, staged digest identical to round 35's.
A second staged route (`^ {0,3}source:\s*S[0-9]{3,}` over the 94 package knowledge files) yields the same 94
ids, `diff` empty. This seat reproduced the same three numbers through the committed guard
(`assimilation/collide-check.sh`, wide pattern → `kind=wide reg_ids=52 staged_ids=94 collisions=22
ids=S031 … S052`, exit 0) and through an independent Python row scan; the two derivations agree.

Guard proof (fixture = `assimilation/scratch-registry.md`, `ee8088e5…`, one `S031` row indented two spaces):

```
0-3-space pattern:      reg_ids=2 (S001 S031)  collisions=1 [S031]   -> indented collision CAUGHT
column-0-only pattern:  reg_ids=1 (S001)       collisions=0 []       -> indented collision FALSE-GREEN
negative control (S901-only registry): collisions=0                  -> no false positive
missing registry path:  reg_ids=0 collisions=0  exit=2               -> fails closed
indent boundary (0-3-space pattern): 3sp caught=1 | 4sp caught=0 | tab caught=0   (known limit)
```

So the guard is load-bearing (an indented collision row is caught only by the 0–3-space form) and fails
closed on a missing input. Nothing is renumbered in the lane; **adoption is by document, never by number.**

**Prediction, stated before the C2 row lands:** with lane `S053` appended the same check must read
`reg_ids=53 staged_ids=94 collisions=23 S031..S053`. Measured on a scratch copy of the registry with one
synthetic `S053` row → `kind=wide reg_ids=53 staged_ids=94 collisions=23 ids=S031 … S053`, exit 0. Staged
`S053` is a **different document** — ソフトウエア製品等の脆弱性関連情報に関する取扱規程（平成29年経済産業省告示第19号）,
`meti.go.jp/policy/netsecurity/vul_notification.pdf` (`SOURCES.append.md:29`) — from the lane's FIRST-EPSS
row. That new collision is the standing scratch-side renumber class, **not** a lane defect: the registry is
append-only and the new id was assigned by document identity, not by staged number.

#### 2. Quarantine slice — 7 register rows, one verified fetch per row, **none adopted**

Frozen derivation (verbatim, `ScoutQuarantine` §1 and this seat's independent run, both byte-identical):

```
awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R"
```

→ 7 lines, 417 B, sha256 `d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862`,
`cmp` against the committed round-35 `assimilation/quarantine-slice` → **equal**; a second run is
byte-identical; **7/7 lines carry an S-id**. Register lines: `:99` S037, `:100` S054, `:322` S048,
`:323`–`:326` S065/S068/S069/S070 (the five carry a stray trailing backtick from the register's own cell).
`## By lane` (`:251`) counts kasegi **2** because it counts only the `payload-absent` table; 2 + 5 = 7 is the
whole slice, and neither count is a missing row. Every row below was fetched **once**
(`curl -sS -L --max-time 30`, instrument UA `capture-source.py:32`, TLS verified, no `-k`), window
`15:37:16Z`–`15:38:00Z`:

| id | register class | live fetch 2026-10-26 | verdict (`ScoutQuarantine` §2) | adopted? |
|---|---|---|---|---|
| S037 | `payload-absent` | 200, 24,189 B `text/html;charset=utf-8`, sha256 `9cba2e96…`, 0 redirects | **absent** — register quote 0 occurrences in all three folds; each fragment (`标准状态：现行`, `发布日期 2020-11-19`, `实施日期 2021-06-01`, `GB/T 30279-2020`) present once, no contiguous span. Quote-form defect, facts hold | **no** |
| S054 | `payload-absent` | 200, 513,648 B `application/pdf`, sha256 `0150c9d1…`, 0 redirects | **absent** — quote deletes the interpolated statutory parenthetical and crosses a line-wrap; 0/0/0 as quoted, full clause present only under the whitespace-removed fold | **no** |
| S048 | never checked | **404**, 748 B `text/html` (Tomcat `HTTP状态 404 - 未找到`), sha256 `95cd25d8…` | **unreachable** — dead record id, live host; register carries no quote, so nothing is testable and this is never a fabrication | **no** |
| S065 | never checked | 200 headers, then **curl exit 28** timeout at 30.00 s; 677,543 of 7,465,472 B (9.1 %), sha256 `23c73742…` (partial) | **unreachable (this probe)** — truncated PDF has no trailer (`pdftotext` exit 1), so **no anchor was checked this round**; transport, not source | **no** |
| S068 | never checked | `301`→`301`→`200` at `sec.cloudapps.cisco.com`, 94,027 B, sha256 `098f99a8…`, 2 redirects | **present-and-located** — section titles and sentences located; the document is **already lane row `S040`** (same URL), so there is nothing new to adopt | **no** (duplicate of S040) |
| S069 | never checked | `302` → `kass.sacinfo.org.cn` token URL; **curl exit 60** (`unable to get local issuer certificate`), **0 B** | **unreachable** under a verifying client; token URL is per-request (`ltwffirakqlbdrdz`) and cannot be bound by a manifest | **no** |
| S070 | never checked | same transport; **curl exit 60**, **0 B** (token `sakjodkwbcklzvsl`) | **unreachable** (same) | **no** |

Totals (round 36): **present-and-located 1** (S068) · **absent 2** (S037, S054) · **unreachable 4**
(S048, S065, S069, S070) · **prose-class-unverifiable 0** · **adopted 0**. Read the `absent 2` correctly: both
documents are real and both were fetched cleanly; what is absent is the **register's quoted span**. Round
35's wording for this class still applies — `.ufo/waves/round-35/assimilation/quarantine-verdicts.md` §3:
"Verdict `prose-class-unverifiable`: quote form, not fact fabrication."

Id-collision screen on the seven register ids against the lane registry (re-derived here): lane **S037** is
the サイボウズ bounty FAQ and lane **S048** is Microsoft MSVR — **different documents** from the register's
S037/S048; **S054, S065, S068, S069, S070 have no lane row**. So two of the seven register ids would bind a
registered id to a different document, and no quarantine row is adoptable by number regardless of verdict.

#### 3. Standing refusals — seven staged entries, **no flip condition cleared**

`wave1/ScoutStandingRefusals.md` § 1–2, cross-checked by this seat's own `sha256sum`/`stat`: the package is
**byte-identical** to round 35 — 70 files, every mtime `2026-10-24 23:33:20 -0300`,
`find -type f -newer round-35/claims.json` → empty, and all seven entry digests equal the values round 35
recorded. Lane `corpus/knowledge/program-severity-ladders-and-reward-scales.md` is still `6c05c98f…`, still
≠ staged `35de5f8b…`.

| staged entry | digest | reason it stays refused | flip condition (still unmet) |
|---|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` | `120d8cd5…` | 0 located quotes (`txt:N`), no executable recheck, `ground: F09` names a **different** admitted lane item | located quote + executable recheck + a non-colliding frontier id |
| `claim-packaging-and-report-quality.md` | `6ad64d78…` | body cites S036 (BILISRC V1.7) in no lane row and no capture; lane `S036` is the Cybozu policy | an S036 row + capture |
| `cn-crowdsourced-testing-roles-and-conduct.md` | `a5302aaf…` | H1 count **0**; S081/S082 appear only in `corpus/SOURCES.md:76-77` refusal prose, never as rows or captures | an entry shape + the two rows |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | `6c15d941…` | S077/S078/S079 in no row/capture (the only `S077.txt` string is a `kill-rule-check.py` fixture); `ground: F24` is not a lane F-id — the frontier ends **F18** today | three rows + a real frontier id |
| `chinese-criminal-thresholds-and-authorisation.md` | `1660c00c…` | three PRC legal hosts (`court.gov.cn`, `czt.ln.gov.cn`, `nj.jsjc.gov.cn`) → 0 hits in `corpus/` outside lessons; staged `S044`–`S046` collide with lane rows of other documents | three rows + a renumber map |
| `chinese-program-severity-instrument.md` | `442e0f2b…` | `sse.com.cn` → 0 hits; anchor `newsType_6` → **0** in `corpus/source-snapshots/round-32/S049.txt` (`962a451a…`), `newsType_21` → 1 | the row + a locatable anchor |
| `program-severity-ladders-and-reward-scales.md` | `35de5f8b…` | same-name lane file differs (`6c05c98f…` vs staged `35de5f8b…`); S036 half still unregistered | byte-identity or a supersedes row |

**0 of 7 rows cleared; 0 new refusals opened; 0 prior refusals lifted.** Additive to the verdict
(`ScoutStandingRefusals` §3): four more entries name lane F-ids admitted for *different* items
(`claim-packaging…` F11, `chinese-criminal-thresholds…` F12, `chinese-program-severity-instrument` and
`program-severity-ladders…` F10), so a renumber/regrounding step is a prerequisite for adoption there too.

**Neither round-36 addition can unblock a refusal.** `grep -ci epss` → **0** in each of the seven entries;
`grep -rliE 'epss|first\.org|exploit prediction'` over the package → **0 files**; none of the seven cites
`S052` or `S053`. The C2 admission (F19 / S053) is therefore an admission **beside** the refusals, not a
key to any of them.

---

## Provenance — which cell comes from where

| Gate cell | source | independent re-derivation by this seat |
|---|---|---|
| registry ids 52 / staged 94 / collisions 22 `S031..S052` | `ScoutIdCollisions.md` § Result | yes — `collide-check.sh` wide **and** col0, exit 0, identical ids; Python row scan agrees |
| guard proof (indented row caught / col0 false-green / exit 2 / indent limit) | `ScoutIdCollisions.md` § Guard proof | yes — same fixture `ee8088e5…`, wide `collisions=1 [S031]` vs col0 `0`; `S901` control `0`; missing path `exit=2`; 3sp caught, 4sp and tab missed |
| projected 23 collisions after `S053` | `ScoutIdCollisions.md` § Result (fixture) | yes — synthetic-row fixture on a scratch copy → `reg_ids=53 … collisions=23 S031..S053` |
| slice = 7 rows, `d02acb68…`, byte-equal to round 35 | `ScoutQuarantine.md` §1 | yes — frozen awk run twice, `cmp` vs committed slice equal |
| per-row fetch status, bytes, digests, verdicts | `ScoutQuarantine.md` §2 + §5 (this seat ran no network fetch) | no — **scout-executed**; this seat checked the register digests, the slice bytes and the lane id screen only |
| `S068` = lane `S040` duplicate | `ScoutQuarantine.md` note C | yes — `corpus/SOURCES.md:46` row `S040` carries the identical Cisco URL |
| package byte-identity (3 meta + 7 entries, 70 files) | `ScoutStandingRefusals.md` §1 | yes — `sha256sum`, `stat`, `find -newer` re-run; all match |
| per-entry flip status and lane counters | `ScoutStandingRefusals.md` §2 | yes for the mechanical cells — `BILISRC` 0 rows (only non-lesson hit is the do-not-adopt prose in `knowledge/program-severity-ladders-and-reward-scales.md`), `sse.com.cn` 0, `S077`–`S079` no rows, PRC hosts 0, `newsType_6` 0 / `newsType_21` 1, `6c05c98f…` vs `35de5f8b…`, frontier ends F18 |
| EPSS/S053 cannot unblock a refusal | `ScoutStandingRefusals.md` §2 | yes — per-entry `grep -ci epss` = 0 for all seven; package EPSS grep 0 files |

## Conflicts on record (verbatim; the canonical judge resolves)

1. **Label conflict on quarantine rows S037/S054, round 36.** `ScoutQuarantine.md` note A: *"I file both as
   **`absent`** under the register's own definition (`payload-absent` = source fetched cleanly, span in none
   of the folds) … The round-35 ExecQuarantineSlice seat filed the same facts under
   `prose-class-unverifiable` (verdicts §1); the round-35 ScoutQuarantine filed `absent`. Facts and the flip
   condition … are identical either way; the L1 should write one label."* The round-35 lesson carries
   `prose-class-unverifiable` for both rows. This Gate block prints the round-36 label (`absent`) because it
   is the only round-36 verdict, and keeps this note so the lesson does not silently switch labels.
2. **S065 moved class between rounds, on transport only.** Round 35: `present-and-located` (full
   7,465,472 B, `e33b0f67…`). Round 36: `unreachable (this probe)` — 677,543 B in 30 s, no trailer. The scout
   states it plainly: *"The label is `unreachable` for this probe's contract (no complete payload within
   30 s), **not** a source defect and not a fabrication. Earlier-round anchors … are **not re-verified
   here**."*
3. **S069/S070 depend on the TLS policy of the invocation.** Verified client: `curl` exit 60, 0 B
   (round 36, and round 35 `ScoutQuarantine`). `-k`/plain-`http`: 1,470,121 B / 234,182 B with anchors
   located (round 35 `ExecQuarantineSlice` §4, not re-measured this round). Round 36 files both
   `unreachable`; a reader must not carry that label over to "the payload does not exist".

## Limits

- This seat ran **no** network fetch: every byte count, HTTP status and digest in §2 is the scout's, quoted
  with its receipt; only the slice derivation, the collision arithmetic, the guard, and the package/lane
  digests were re-executed here.
- One fetch per row, one UA, one 30 s cap, one time-of-day (`15:37:16Z`–`15:38:00Z`). `std.samr.gov.cn`
  token URLs are per-request and unpinnable.
- `S053`/`F19` are **not** in the lane at composition, so §1's 23-collision figure and the frontier's
  `F19` are predictions; the lane's own closure (C2) must re-run the check after the row lands.
- The `absent` class is a statement about the **quoted span**, never about the document's existence.
- This receipt proposes lesson text only. It edits no lesson, no registry, no claim; the L1 integrates.

## Reproduction (read-only; scratch only)

```
S=/fast/scratch/hyaku/kasegi-r36/ScribeAssimilationGate; export TMPDIR=$S/tmp; mkdir -p "$TMPDIR"
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
cp corpus/SOURCES.md "$S/reg-now.md"
bash .ufo/waves/round-35/assimilation/collide-check.sh "$S/reg-now.md" \
     /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md wide
     # kind=wide reg_ids=52 staged_ids=94 collisions=22 ids=S031 … S052   exit 0
bash .ufo/waves/round-35/assimilation/collide-check.sh "$S/reg-now.md" \
     /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md col0      # collisions=22, exit 0
# guard: copy of assimilation/scratch-registry.md (ee8088e5…)
bash .ufo/waves/round-35/assimilation/collide-check.sh "$S/fixture.md" … wide   # collisions=1 [S031]
bash .ufo/waves/round-35/assimilation/collide-check.sh "$S/fixture.md" … col0   # collisions=0
bash .ufo/waves/round-35/assimilation/collide-check.sh "$S/nope.md"    … wide   # exit=2
# slice
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" \
  > "$S/quarantine-slice" && cmp "$S/quarantine-slice" \
  .ufo/waves/round-35/assimilation/quarantine-slice && sha256sum "$S/quarantine-slice"
```

Fetches are **not** reproduced here; run them from `wave1/ScoutQuarantine.md` §2 (one verified
`curl -sS -L --max-time 30` per row, instrument UA).

## Report

Seat: `ScribeAssimilationGate` (round 36, wave 1). Delivered: the lesson's assimilation Gate block, draft
ready to paste, with **Assimilation: none adopted** and all three components filled from scout receipts —
(1) id-collision: registry **52** / staged **94** / **22** collisions `S031..S052` (`ScoutIdCollisions.md`,
re-derived here through `collide-check.sh`, wide and col0, exit 0), guard load-bearing (indented `S031`
caught 1 vs col0 0), fails closed (`exit=2`), known 4-space/tab limit, **23** projected once `S053` lands
(staged `S053` is the METI rule, a different document); (2) quarantine: **7** rows, slice `d02acb68…` byte-equal
to round 35, one verified fetch per row — present-and-located **1** (S068 = lane S040 duplicate), absent **2**
(S037, S054), unreachable **4** (S048 404, S065 timeout, S069/S070 curl 60), **adopted 0**; (3) standing
refusals: **7** entries, package byte-identical (70 files, newest mtime `2026-10-24 23:33:20 -0300`),
**0 of 7** flip conditions cleared, and the round's F19/S053 admission cannot unblock any of them (EPSS 0 in
all seven, 0 package files). Conflicts recorded verbatim for the judge: the S037/S054 label set (round 36
`absent` vs round 35 `prose-class-unverifiable`), S065's transport-only move, and S069/S070's TLS-dependent
label. Not done by this seat: no network fetch, no lane edit, no lesson edit, no tool install, no judge.
Scratch `/fast/scratch/hyaku/kasegi-r36/ScribeAssimilationGate/` removed before yield.

Report: `.ufo/waves/round-36/wave1/ScribeAssimilationGate.md`
