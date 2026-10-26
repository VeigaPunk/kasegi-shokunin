# ScribeGateBlocks — round 40 receipt (lesson `## Gate` block)

Seat: `ScribeGateBlocks` (scribe, leaf, no subagent dispatch). Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base `a7af2ce63bce153757d39bf66b366a96caf30c13`,
claims-freeze `5e985b74075dd3813a63d7750966bf8abf693465`. Tooling: **nothing installed or upgraded**
(no `pacman`, no `uv tool install`, no `npx`; `python3`, `bash`, `git`, `grep`, `awk` already present).
Disk guard checked before work (`/fast/scratch/hyaku` 26%, 600.2G free) and green.

## 1. Deliverable

| path | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-40/wave1/ScribeGateBlocks.txt` | 179 | 14438 | `7d19a43a92d22b17d5efad497473368ff2255f0d3721c56dfbd4b2db18c715a0` |

One `## Gate` heading (line 1) and its subsections only: `### Admitted — seven of the nine queued rows`
(S016, S017, S019, S020, S021, S023, S025), `### Admitted — F23 / S060`, `### Rejected` (S022, S024, S061,
S062, plus the S059-remains-rejected note), `### Nine decided rows — status change log` (9 lines),
`### Seam check — registry row ↔ knowledge entry ↔ bound capture`, `### Assimilation`,
`### Sourced claim`. No validation tables, no notes outside the landed text; the L1 merges the file into
`corpus/lessons/round-40.md`.

`grep -c '^## '` = 1. `grep -c '⟨pending'` = 0 (the file carries no placeholder).

## 2. Inputs consumed (all read-only)

| input | path | what it supplied |
|---|---|---|
| row decisions | `wave1/ScribeRows.decisions.txt`, `wave1/ScribeRows.changes.txt` (sha256 `b9242256ef8d7a7fdd4f3fe76da36e9317d691f7ee2b3218bb3747e55599231b` per its receipt) | the 9 `queued -> mined/rejected` lines and each mined row's `used-by` |
| new rows | `wave1/ScribeNewRows.txt` | S060 mined (F23), S061 rejected, S062 rejected |
| F23 admission | `wave1/ScribeF23.entry.md`, `ScribeF23.readme-row.txt`, `ScribeF23.province.txt` | F23 row/coverage-map/PROVINCE bytes, the S060 entry text |
| scout receipts + captures | `wave1/ScoutS016/S017/S019/S020/S021/S023/S025.{md,capture.txt,manifest-record.json}`, `wave1/ScoutF23Lead.{md,capture.txt,manifest-record.json}`, `wave1/ScoutS060Leads.txt` | URL, HTTP status, byte counts, fetch UTC, sha256, located quotes |
| entries | `wave1/ScribeEntriesG1.*.md` (S016/S017/S019), `wave1/ScribeEntriesG2.*.md` (S020/S021/S023/S025), `wave1/ScribeF23.entry.md` | `source:` seam limb |
| recheck | `wave1/ExecRecheckAll.txt` | `S016 … S060 exit=0 ok` (8 rows) |
| binding | `wave1/ExecBindingCheck.txt` / `.md` | `records=54 bound=54 unbound=0` (46 before); the two negative controls |
| assimilation | `wave1/ExecAssimilation.txt` | collision/quarantine numbers |
| registry + frontier + census | `corpus/SOURCES.md`, `corpus/README.md`, `wave1/ScribeRows.md` §G5 | S059 flip wording, frontier 22 -> 23 basis, census mirror output |
| claims/controls | `.ufo/waves/round-40/claims.json`, `c2-controls/before.txt`, `census-before.txt` | frozen after-state the Gate is written against |

No artifact was rerun to decorate the report: the gate values quoted in the block are the sibling seats'
observed outputs (`ExecRecheckAll`, `ExecBindingCheck`, `ExecAssimilation`, `ScribeRows`), and the only
commands this seat ran are the two read-only checks in §3.

## 3. Checks this seat ran (commands and actual output)

### 3.1 Seam check — row ↔ entry ↔ bound capture

Script `/fast/scratch/hyaku/kasegi-r40/ScribeGateBlocks/seam.py`: parses the mined row lines out of the
two row deliverables (columns 2/7/9/12 = source, anchor, status, used-by), maps each `used-by` basename to
a delivered entry file, requires the entry's `source: S###` line, extracts `corpus/source-snapshots/round-40/S###.txt`
from the anchor, re-hashes the committed capture bytes and compares them with the scout manifest record's
`sha256`, and compares the row's one `https://` token with the record's `url`.

```
$ python3 seam.py
mined rows: ['S016', 'S017', 'S019', 'S020', 'S021', 'S023', 'S025', 'S060']
S016 entry=anthropic-cvd-provenance-and-pacing.md capture=S016.txt url_match=True problems=none
S017 entry=pz-reporting-transparency-trial.md capture=S017.txt url_match=True problems=none
S019 entry=nist-sp800-216-vdp-framework.md capture=S019.txt url_match=True problems=none
S020 entry=doj-vdp-framework-scope-and-authorization.md capture=S020.txt url_match=True problems=none
S021 entry=cisa-bod-20-01-vdp-minimums.md capture=S021.txt url_match=True problems=none
S023 entry=cisa-cvd-program-stages.md capture=S023.txt url_match=True problems=none
S025 entry=cve-bench-agent-exploitation-benchmark.md capture=S025.txt url_match=True problems=none
S060 entry=cyclonedx-analysis-subtree.md capture=S060.txt url_match=True problems=none
seam ok=8 fail=0
```

Intermediate observation (kept because it is the check's own discrimination): before `ScribeEntriesG2`
landed, the same script printed `seam ok=4 fail=4` with `entry-file-missing` on S020/S021/S023/S025 — the
entry limb is a real limb, not a constant. An earlier cut of the script also mis-read the anchor column
(used the `scope` cell) and reported `anchor-no-capture-path` for all eight, so the 8/8 is not an artefact
of an always-green parser: the anchor regex only resolves after the column index was corrected.

### 3.2 Quote check — every quoted span in the deliverable, ≤25 words, located

```
$ python3  # extract "..." spans, collapse whitespace, require len>=4 words
spans 11 failures []
```

Ten spans resolve in the capture the block attributes them to (`ScoutS016`, `ScoutS017`, `ScoutS019`,
`ScoutS020`, `ScoutS021`, `ScoutS023`, `ScoutS025`, `ScoutF23Lead`); the eleventh is the S059 flip clause,
which resolves in `corpus/SOURCES.md` (`flip: a CycloneDX-vs-CSAF frontier entry with a scoped
analysis-subtree capture`). Longest evidence span 22 words (S020).

A first cut of this check reported failures on four spans; all four were parser artefacts, not quote
defects: (a) the regex excluded `\n`, so multi-line wrapped quotes (§S019/S021/S025) were cut mid-span —
fixed with `re.S` + whitespace collapse; (b) short non-evidence quotes (`"exploit"`, `"resolve"`) shifted
the quote pairing — fixed by extracting all spans first and filtering by word count afterwards. The quotes
themselves were never edited to pass; only the extractor was.

### 3.3 Cross-check of the numbers quoted in the block (transcribed, not rerun)

```
$ cat wave1/ExecRecheckAll.txt
S016 exit=0 ok
S017 exit=0 ok
S019 exit=0 ok
S020 exit=0 ok
S021 exit=0 ok
S023 exit=0 ok
S025 exit=0 ok
S060 exit=0 ok

$ tail -2 wave1/ExecBindingCheck.txt
AUDIT records=54 with_url=54 with_fetched_utc=16 with_archival=38 snapshot_dirs=16 manifest_dirs=16 missing_manifest=0 multi_row_url=3 orphans=1 orphan=S040-live.txt
records=54 bound=54 unbound=0
```

`multi_row_url 2 -> 3` is S060 sharing S059's URL (both `https://cyclonedx.org/docs/1.7/json/`), which
`ExecBindingCheck.md` §"Deviations and risks" item 2 states; the block does not claim a `multi_row_url`
increase but the row does expose it, so the L1 may want the S059/S060 duplicate noted in the round's census
section.

## 4. Findings and limits recorded in the deliverable (reporting these, not promoting them)

1. **S019 is abstract-level.** The committed capture is the CSRC publication record (132 lines), not SP
   800-216; the block says so in the S019 bullet, matching `ScribeRows` F1 and `ScribeEntriesG1` F1. The row
   is `mined` because the abstract/publication-record ground is real, but nothing clause-level may be cited
   from it.
2. **S025's paraphrased abstract does not exist in the captured v4.** The block records the v4 wording
   (`exploit up to 13%`, L32) and says the "resolve" paraphrase is absent from the captured bytes
   (`ScribeRows` F2; `ScoutS025.md` Discrepancy).
3. **`ExecAssimilation`'s collision count is a lower bound.** It measures at freeze (59 reg-ids, 29
   collisions) and tells the round to re-run after the registry rows land, because the staged package's own
   S060 is Hitachi HIRT-PUB10008 (a document the lane holds as S039) and the lane now opens S060 for
   CycloneDX. The block carries that; it does not claim a post-landing number.
4. **Census over the new rows is not in hand.** The census this round is `ScribeRows`' mirror with the nine
   decided rows substituted (`W04 S028`, `W04 S029`, `ok`, exit 0) plus its `E11 S019 missing used-by` red
   when an entry file is removed. The block says the post-landing census is the L1's step rather than
   implying it already ran over S060-S062.
5. **S062 is a monitor row, not a source.** It is rejected with the flip and with the draft-drift note (nine
   `product_status` properties in csd04 vs eight in v2.0; SHALL where v2.0 reads MUST); the block keeps it
   in the rejected list so the flip is checkable next round at 30d.

## 5. Out of scope / not touched

No edit to `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/README.md`, `PROVINCE.md`,
`corpus/lessons/round-40.md`, the registry, snapshots or manifests — the L1 lands those from the sibling
seats' deliverables. No git/jj mutation anywhere (read-only `git log`, `git status`, `rev-parse` only). No
write to the fleet root, `shokuknow`, sibling lanes, `.ufo/state/`, `MANIFEST.json`, `scripts/`, or any
PATH directory. No message to `agent://all`; no swarm.

## 6. Scratch

`/fast/scratch/hyaku/kasegi-r40/ScribeGateBlocks/` held only `ScribeGateBlocks.txt` and `seam.py`; the
deliverable was copied into `wave1/`, the scratch tree is removed before yield (`rm -rf -- "$S"`), so no
`ScribeGateBlocks` entry remains under `/fast/scratch/hyaku/kasegi-r40/`.
