# ScribeRows — round-40 receipt: the nine queued registry rows decided

Seat: `ScribeRows` (scribe, leaf, no subagent dispatch). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `a7af2ce63bce153757d39bf66b366a96caf30c13`, claims-freeze `5e985b74075dd3813a63d7750966bf8abf693465`. Claim C2 (coverage). Item: deliver the final registry-row bytes for S016/S017/S019/S020/S021/S022/S023/S024/S025 plus the `old -> new` change-log lines. Tools installed or upgraded: **none** (bash, python3, awk, git, curl already present; no `pacman`, no `uv tool install`, no `npx`). Disk guard green at start (`disk-guard.sh status`: `/fast/scratch/hyaku 26%`, free 600.2G). All dates and times UTC, 2026-10-26.

## 0. Answer in one paragraph

Seven of the nine rows are delivered `mined` and two `rejected`, as one landable line each, changing only the cells the decision requires: the seven mined rows change `anchor` (now naming the round-40 capture with line locators), `status` (`queued` -> `mined`), `opened` (2026-10-26, the date the source was opened) and `used-by` (the entry path agreed in writing with the entry seats); the two rejected rows change `teaches` (to `REJECTED: … ; flip: …`) and `status` (`queued` -> `rejected`), and keep `opened` 2026-10-19 because they were never opened. Every one of the seven captures passes `source-recheck.py` (`sha256 OK` plus 15 quote lines, exit 0) and all seven records bind to their rows with `multi_row_url=0` (`capture-binding-check.py`: `records=7 bound=7 unbound=0`, exit 0). A scratch mirror of the lane registry with these nine rows in place validates clean (`exit 0`, warnings `W04 S028` and `W04 S029` only); deleting one of the new `used-by` files from that mirror makes the census print `E11 S019 missing used-by corpus/knowledge/nist-sp800-216-vdp-framework.md` and exit 1, which proves the checker read the mirror and that the seven `used-by` paths are load-bearing. Entry reconciliation at my cut: `ScribeEntriesG1` had landed all three of its entries in `wave1/` under exactly the bound slugs, each opening `source: S016` / `S017` / `S019`; `ScribeEntriesG2`'s four were still pending, their names fixed in writing.

## 1. Deliverables

Paths relative to the lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

| # | path | lines | bytes | sha256 |
|---|---|---|---|---|
| 1 | `.ufo/waves/round-40/wave1/ScribeRows.decisions.txt` | 9 | 6393 | `83633196e4e616aa81b7ed00d8f78d15e29cb42b55970a9971ebd4c5d69e8817` |
| 2 | `.ufo/waves/round-40/wave1/ScribeRows.changes.txt` | 10 | 1140 | `b9242256ef8d7a7fdd4f3fe76da36e9317d691f7ee2b3218bb3747e55599231b` |

File 1 is nine registry rows, ids in ascending order (S016, S017, S019, S020, S021, S022, S023, S024, S025), one per line, each a complete 11-column row for `corpus/SOURCES.md` §Registry: no headings, no notes, nothing that is not a row. The `S0NN` in cell 1 is the block key, so replacing the existing row line with the delivered line is the whole landing edit. File 2 is the eight `old -> new` lines the lesson needs plus one closing count line; it is not landed inside the registry.

## 2. Rows as delivered

Header shape (`corpus/SOURCES.md` L5): `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`.

| id | status | opened | recheck | used-by (entry) | anchor names |
|---|---|---|---|---|---|
| S016 | mined | 2026-10-26 | 90d | `corpus/knowledge/anthropic-cvd-provenance-and-pacing.md` | `corpus/source-snapshots/round-40/S016.txt`: L17 AI-provenance label, L16 45-day post-patch buffer, L12 7-day exploited-critical target |
| S017 | mined | 2026-10-26 | 90d | `corpus/knowledge/pz-reporting-transparency-trial.md` | `…/round-40/S017.txt`: L23 one-week public notice, L34 no technical detail before the deadline |
| S019 | mined | 2026-10-26 | on-release | `corpus/knowledge/nist-sp800-216-vdp-framework.md` | `…/round-40/S019.txt`: L80 abstract clause (recurs L83), L97 document history final 05/24/23 — **landing page only** |
| S020 | mined | 2026-10-26 | on-release | `corpus/knowledge/doj-vdp-framework-scope-and-authorization.md` | `…/round-40/S020.txt`: L142 authority limit for cloud-provider-hosted servers |
| S021 | mined | 2026-10-26 | on-release | `corpus/knowledge/cisa-bod-20-01-vdp-minimums.md` | `…/round-40/S021.txt`: L133 ban on restricting a reporter's disclosure |
| S022 | rejected | 2026-10-19 | on-release | `—` | unchanged (Sections 3.1 and 4.1; effective 2025-05-14) |
| S023 | mined | 2026-10-26 | 90d | `corpus/knowledge/cisa-cvd-program-stages.md` | `…/round-40/S023.txt`: L151 45-day disclosure floor, L154 VDP separate from CVD |
| S024 | rejected | 2026-10-19 | on-release | `—` | unchanged (OJ L 2024/2847 of 20.11.2024) |
| S025 | mined | 2026-10-26 | on-release | `corpus/knowledge/cve-bench-agent-exploitation-benchmark.md` | `…/round-40/S025.txt`: L32 abstract 13%, L507 10% zero-day / 12.5% one-day (v4 PDF, 24 Jun 2025) |

Rejected `teaches` cells, verbatim:

- **S022** — `REJECTED: superseded by S030 (CNA Rules v4.2.0, approved 2026-08-20, effective 2026-08-25), whose mined row records 'supersedes S022'; no lane capture of the v4.1.0 PDF exists. flip: re-open only if S030's capture is withdrawn or a citing source quotes v4.1.0 section numbering that 4.2.0 no longer holds.`
- **S024** — `REJECTED: superseded by S029 (official CRA Article 14 text, OJ 20.11.2024, mined 2026-10-20), whose row records 'supersedes S024'; this row's Article 14 wording was never verified from EUR-Lex. flip: re-open only if S029's Article 14 capture is withdrawn or the consolidated text changes Article 14 or the Article 71 application date.`

Both grounds are checkable in the lane as it stands: `corpus/SOURCES.md` L35 (S029) and L36 (S030) carry `supersedes S024 —` / `supersedes S022 —`, and `grep -rl '"id": "S022"' corpus/source-snapshots/` and the same for `S024` print nothing (no capture exists for either row, so neither can be mined without opening the source).

## 3. Gates run, with actual output

### G1 shape and byte fidelity of the emitted rows

All 59 pre-existing registry rows round-trip byte-identically through the same strip/rebuild path used to emit the nine (`roundtrip_rows_equal 59 of 59`), so the emitted rows carry the file's own cell-padding style, not a new one. Delivered shape:

```
L1 bytes=684 pipes=12 NF=13 id=S016
L2 bytes=629 pipes=12 NF=13 id=S017
L3 bytes=782 pipes=12 NF=13 id=S019
L4 bytes=743 pipes=12 NF=13 id=S020
L5 bytes=728 pipes=12 NF=13 id=S021
L6 bytes=626 pipes=12 NF=13 id=S022
L7 bytes=656 pipes=12 NF=13 id=S023
L8 bytes=792 pipes=12 NF=13 id=S024
L9 bytes=716 pipes=12 NF=13 id=S025
```

`NF=13` with `-F'|'` is 11 cells; `pipes=12` means no cell contains a `|`. Each line ends with one `\n`; `wc -lc` on the delivered file = `9 6393` (changes = `10 1140`).

### G2 changed cells against the base registry — nothing else moved

```
S016 changed: anchor,status,opened,used-by
S017 changed: anchor,status,opened,used-by
S019 changed: anchor,status,opened,used-by
S020 changed: anchor,status,opened,used-by
S021 changed: anchor,status,opened,used-by
S022 changed: teaches,status
S023 changed: anchor,status,opened,used-by
S024 changed: teaches,status
S025 changed: anchor,status,opened,used-by
```

`source`, `kind`, `tier`, `scope`, `recheck` and (for the seven mined rows) `teaches` are byte-identical to the queued rows at base; for the two rejected rows `anchor`, `opened`, `recheck` and `used-by` are unchanged.

### G3 every named capture passes source-recheck (seven of seven)

A scratch aggregate manifest was built from the seven scout `manifest-record.json` files (S025's is already a `schema_version:1` manifest) with the seven `*.capture.txt` files beside it, then:

```
$ python3 corpus/instruments/source-recheck.py --manifest /fast/scratch/hyaku/kasegi-r40/ScribeRows/snap/manifest.json
S016:sha256 OK
S016:Q1 OK occurrences=1 anchor=17-ok
S016:Q2 OK occurrences=1 anchor=16-ok
S016:Q3 OK occurrences=1 anchor=12-ok
S017:sha256 OK
S017:Q1 OK occurrences=1 anchor=23-ok
S017:Q2 OK occurrences=1 anchor=34-ok
S017:Q3 OK occurrences=1 anchor=34-ok
S019:sha256 OK
S019:Q1 OK occurrences=2 anchor=80-ok
S019:Q2 OK occurrences=2 anchor=80-ok
S019:Q3 OK occurrences=1 anchor=97-ok
S020:sha256 OK
S020:Q1 OK normalized=markup-whitespace occurrences=1 anchor=142-ok
S021:sha256 OK
S021:Q1 OK occurrences=1 anchor=133-ok
S023:sha256 OK
S023:Q1 OK occurrences=1 anchor=151-ok
S023:Q2 OK occurrences=1 anchor=154-ok
S025:sha256 OK
S025:Q1 OK normalized=markup-whitespace occurrences=1 anchor=32-ok
S025:Q2 OK normalized=markup-whitespace occurrences=1 anchor=507-ok
exit=0
```

22 verdict lines, exit 0. Every line number the row anchors cite (L12, L16, L17, L23, L32, L34, L80, L97, L133, L142, L151, L154, L507) is one of these verified anchors or the sentence that follows it inside the same anchored paragraph.

### G4 the seven records bind to the delivered rows

The mirror below also carries `corpus/source-snapshots/round-40/{S016,S017,S019,S020,S021,S023,S025}.txt` and the aggregate `manifest.json`:

```
$ python3 corpus/instruments/capture-binding-check.py --root /fast/scratch/…/mirror/kasegi-shokunin
MANIFEST round-40 records=7 url_bound=7 fetched=7 archival=0
AUDIT records=7 with_url=7 with_fetched_utc=7 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=0
records=7 bound=7 unbound=0
exit=0
```

`multi_row_url=0` is the census-side claim: none of the seven row URLs already occurs in another registry row, so landing these rows adds no `W04` duplicate-URL warning.

### G5 census over a scratch mirror with the nine rows in place

Mirror = `<scratch>/mirror/kasegi-shokunin/` with the lane's `corpus/SOURCES.md` having the nine delivered rows substituted in place of the queued rows (`mirror rows replaced 9`), the lane's whole `corpus/knowledge/` copied, and the round-40 snapshot directory above.

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-26 /fast/scratch/…/mirror/kasegi-shokunin
kasegi-shokunin	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi-shokunin	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi-shokunin	ok	/fast/scratch/…/mirror/kasegi-shokunin/corpus/SOURCES.md
exit=0
```

The two warnings are the pre-existing ones named in the frozen C2 after-state. No `E` code fires: `E04` does not fire for the S024 row even though it now shares S029's URL, `E05`/`E06` kinds and tiers are inside the enum, `E07` accepts `mined`/`rejected`, `E08` accepts 2026-10-26, `E09` accepts `90d` and `on-release`, `E11` resolves all seven new `used-by` paths, `E12` does not fire and `W02` does not fire (the rejected `teaches` cells are 305 and 334 chars, far past the thin-reason threshold).

Mirror-read proof (the same mirror with one new `used-by` file moved away):

```
kasegi-shokunin	W04	S028 duplicate url …
kasegi-shokunin	W04	S029 duplicate url …
kasegi-shokunin	E11	S019 missing used-by corpus/knowledge/nist-sp800-216-vdp-framework.md
exit=1
```

So the checker read the mirror's rows, not the lane's.

### G6 the frozen C2 counting commands, run on the mirror

```
$ awk -F'|' '/^\|[[:space:]]*S0(16|17|19|20|21|22|23|24|25)[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); if(s=="queued") n++} END{print n+0}' corpus/SOURCES.md
0
$ … if(s=="mined") n++ …
7
$ … if(s=="rejected") n++ …
2
```

Frozen values were `queued 9 -> 0` and `mined 0 -> >=4`; delivered 0 and 7, with the remaining 2 rejected.

### G7 write surface

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain corpus/SOURCES.md
(empty)
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain | grep -v '^?? .ufo/waves/round-40/wave1/'
?? .ufo/waves/round-40/build-wave1-spec.py
?? .ufo/waves/round-40/build-wave2-spec.py
… (round-40 plan/dispatch files written by the L1, not by this seat)
```

The only files this seat created are the two deliverables and (last) this receipt, all inside `.ufo/waves/round-40/wave1/`. No artifact from another wave, no edits to `corpus/SOURCES.md`, `corpus/knowledge/`, any source snapshot directory, `.ufo/state/`, the fleet root, or a sibling lane.

### G8 entry-name reconciliation against the delivered files

`ScribeEntriesG1` landed its three entries in `wave1/` while this seat was running; their file names equal the `used-by` slugs cell-for-cell, and their provenance lines equal the row ids:

```
ScribeEntriesG1.anthropic-cvd-provenance-and-pacing.md:3:source: S016 — https://www.anthropic.com/coordinated-vulnerability-disclosure — capture corpus/source-snapshots/round-40/S016.txt (32 lines, 4,481 bytes; sh…
ScribeEntriesG1.nist-sp800-216-vdp-framework.md:3:source: S019 — https://csrc.nist.gov/pubs/sp/800/216/final — capture corpus/source-snapshots/round-40/S019.txt (132 lines, 4,901 bytes; sha256 514cc3796dc2e…
ScribeEntriesG1.pz-reporting-transparency-trial.md:3:source: S017 — https://projectzero.google/2025/07/reporting-transparency.html — capture corpus/source-snapshots/round-40/S017.txt (39 lines, 5,058 bytes; sh…
```

Each line is cut at 160 characters of the entry's own L3 (`…` marks the cut), so the path and digest prefix quoted here are the entry's bytes, not a rewrite. The three entries name the same landing paths the delivered row anchors name (`corpus/source-snapshots/round-40/S0NN.txt`), so row and entry agree on where the capture must be copied. Re-running the mirror census with those three real entries in place of placeholders and the other four still placeholders:

```
kasegi-shokunin	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi-shokunin	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi-shokunin	ok	/fast/scratch/…/mirror/kasegi-shokunin/corpus/SOURCES.md
exit=0
$ grep -rlE '^source: S0(16|17|19|20|21|22|23|24|25)' …/mirror/kasegi-shokunin/corpus/knowledge | wc -l
3
```

Three is the correct count for the three entries that exist; it rises to seven when `ScribeEntriesG2` lands its four, which is the number C2's counting command has to reach.

## 4. Findings

**F1 (limit of evidence, HIGH for whoever reports C2). S019's capture is the CSRC record page, not the SP 800-216 document.** `ScoutS019.capture.txt` is 132 lines / 4901 bytes and holds the title, authors, the full abstract, keywords, the document history and the DOI/PDF links; it holds no procedure text. The scout probed the PDF (HTTP 200, 1,510,851 bytes) but did not deliver it. The anchor cell therefore says `landing page only — the SP 800-216 PDF was not captured in this round`, and the row's `mined` status must be read as abstract-level: the S019 `teaches` cell ("formalize intake, assessment, tracking and communications") is only partly supported by the captured page. An entry that quotes procedure detail would be quoting something the lane does not hold.

**F2 (wording, recorded so it cannot become a false quote). S025's captured text is the v4 PDF (24 Jun 2025), whose abstract says `exploit up to 13% of the vulnerabilities` (L32) and whose §4 reports 10% zero-day and 12.5% one-day (L507).** The earlier queued row and the round's own discussions paraphrase this as "resolve up to 13%"; that sentence is not in the captured bytes. The anchor cell records the v4 wording and the document date so the discrepancy is visible at the row.

**F3 (cell choice, deliberate and reversible).** The seven mined rows get `opened` = 2026-10-26: the source was opened today, and census `overdue` computes its clock from `opened + recheck`, matching the precedent of the mined S029/S030 rows, which carry their mining date. The two rejected rows keep `opened` = 2026-10-19, when they entered the queue, because nothing was opened. If the L1 prefers `opened` to mean "row first written", restore 2026-10-19 on the seven; nothing else in the row depends on it.

**F4 (dependency, satisfied for three of the seven at my cut).** The seven `used-by` paths are entry files. At my cut `ScribeEntriesG1` had landed S016, S017 and S019 under exactly the bound slugs, with `source:` lines naming the right row ids and the same `corpus/source-snapshots/round-40/S0NN.txt` capture paths the row anchors name (§G8). Still pending were `ScribeEntriesG2`'s four — `doj-vdp-framework-scope-and-authorization.md`, `cisa-bod-20-01-vdp-minimums.md`, `cisa-cvd-program-stages.md`, `cve-bench-agent-exploitation-benchmark.md` — whose names that seat confirmed in writing this round. If any entry is withheld, that row must be flipped to `rejected` (reason: `no entry`; flip: a capture-bound entry citing it) instead of being landed `mined`, or the census goes `E11` red and C2's `grep -rl '^source: S0…'` count falls below the mined count.

**F5 (scope, recorded). The S022/S024 rejections rest on rows already mined, not on new reading.** Neither the CNA v4.1.0 PDF nor CRA Article 14 was opened by this seat; the flip conditions are written so a later seat can test them from the lane (`S030`/`S029` captures present or not; consolidated CRA text unchanged or not).

## 5. Out of scope (not done, by design)

`corpus/SOURCES.md` is unedited (the L1 lands these rows); no knowledge entry, no capture landing into `corpus/source-snapshots/round-40/`, no round-40 `manifest.json`, no S060+ rows, no F23 material, no lesson `## Gate` or `## Registry changes` section, no harness run, no census-after claim, no C1 (`r40-closure.sh`) artifact, no QUALITY/SCORECARD/LOG/SHONEN edit, no git mutation anywhere, no install.

## 6. Artifact paths

- Deliverables: `.ufo/waves/round-40/wave1/ScribeRows.decisions.txt`, `.ufo/waves/round-40/wave1/ScribeRows.changes.txt` (§1 has lines, bytes, sha256).
- This receipt: `.ufo/waves/round-40/wave1/ScribeRows.md`.
- Read for provenance: `.ufo/waves/round-40/claims.json`, `.ufo/waves/round-40/c2-controls/before.txt`, `.ufo/waves/round-40/wave1-spec.json` (items 34/37/38), `.ufo/waves/round-40/wave1/Scout{S016,S017,S019,S020,S021,S023,S025}.{capture.txt,manifest-record.json,md}`, `corpus/SOURCES.md` (rows S016-S030), `corpus/instruments/{source-recheck,capture-binding-check,recheck-audit}.py`, `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`.

## 7. Scratch

`/fast/scratch/hyaku/kasegi-r40/ScribeRows/` (aggregate manifest, per-capture copies, mirror tree, probe copy, builder) is removed before yield; nothing was written under `/tmp` and nothing outside the lane's `wave1/` stayed behind.
