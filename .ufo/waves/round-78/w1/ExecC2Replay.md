# ExecC2Replay — round-78 w1: independent re-measurement (C2 do-nothing + frozen predicates)

Read-only replay. No lane-tree edits, no git/jj writes (only `git archive` reads), no installs (no tooling installed or upgraded; pacman untouched).
Method: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive <commit> | tar -x -C $S/<tree>` into scratch only — base `0687cca8645884aba30c8eb5fa2d8ecaca7245cf` → `$S/base`, freeze `2d81fe84506b323fb32beb137d5bd21db6a5c13d` → `$S/freeze`. Every run had `TMPDIR=$S/tmp` passed explicitly; both exports stayed under `$S`. Scratch deleted before yield.

## Main table — predicate, base value, freeze value, command, rc

| # | Predicate / control | Base 0687cca8 | Freeze 2d81fe84 | Command (run with cwd = export root, TMPDIR=$S/tmp) | rc |
|---|---|---|---|---|---|
| 1 | B3 / c2-donothing: FRONTIER-CENSUS line | `FRONTIER-CENSUS rows=53 admitted=53 closed=53 problem-rows=0 registry=112` | identical line | `python3 corpus/instruments/frontier-recheck-count.py` | 0 (both; `entries=56 pass=56 exit=0`; PASS lines F01–F53 only, **no F54 anywhere**) |
| 2 | B2a / knowledge .md count | 91 | 91 | `ls corpus/knowledge/*.md \| wc -l` | 0 |
| 3 | B1a / registry S-row count | 112 | 112 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 0 |
| 4 | S112 registry status | `queued` (1 occurrence, row present at base) | `queued` | `grep 'S112' corpus/SOURCES.md \| grep -oE 'queued\|mined'` | 0 |
| 5 | B4 / capture-binding records line | `records=91 bound=91 unbound=0` | `AUDIT records=92 … bound=92 unbound=0` + `MANIFEST round-78 records=1 url_bound=1 fetched=1 archival=0` | `python3 corpus/instruments/capture-binding-check.py` | 0 (both) |
| 6 | c2-recheck-audit: expect block | `expect=present expected=91 missing=0 unexpected=0` | same | `python3 corpus/instruments/recheck-audit.py --root $S/base --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin` (and --root $S/freeze) | 0 (both; `strict pass=91/91`, `lines=91 pass=91 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`) |
| 7 | c2-prerecheck / B0+B5: source-recheck S112 | n/a (no round-78 dir at base — confirmed absent in base export) | `S112:sha256 OK` + 7 × `OK occurrences=1 anchor=<n>-ok` (anchors 24,24,24,166,168,169,195) | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-78/manifest.json --source S112` | 0 |
| 8 | Independent quote presence (whitespace-collapsed substring, whole snapshot) | n/a | sha256 `f3ca04652e444125a1441449e23814107999496d73fa6ac46f35cca3d2bd0907` (matches manifest); each of Q01,Q02,Q03,Q09,Q10,Q11,Q13 `occurrences=1`, `anchor_ok=True` | `python3 $S/quotecheck.py` (collapse `re.sub(r"\s+"," ")`, count `.count()`, anchor-line recheck) | 0 |
| 9 | B6 / quote-absence sweep (7 × `grep -F -l '<quote>' corpus/knowledge/*.md`, freeze export, 91 files) | n/a | **zero files matched for every quote** — Q01, Q02, Q03, Q09, Q10, Q11, Q13: file list empty | `grep -F -l '<quote>' corpus/knowledge/*.md` | 1 per grep (= "no match", expected) |

## Exact retained output (freeze, representative)

- `frontier-recheck-count.py` (identical at base): `FRONTIER-CENSUS rows=53 admitted=53 closed=53 problem-rows=0 registry=112` … `PASS F53 knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md ids=S110 exit=0` … `entries=56 pass=56 exit=0`
- `capture-binding-check.py` freeze tail: `MANIFEST round-78 records=1 url_bound=1 fetched=1 archival=0` / `AUDIT records=92 with_url=92 with_fetched_utc=54 with_archival=38 snapshot_dirs=51 manifest_dirs=51 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt` / `records=92 bound=92 unbound=0` (base tail: `AUDIT records=91 … orphans=1 orphan=S040-live.txt` / `records=91 bound=91 unbound=0`)
- `source-recheck.py` full output:
  ```
  S112:sha256 OK
  S112:Q01-batch-definition OK occurrences=1 anchor=24-ok
  S112:Q02-return-shape OK occurrences=1 anchor=24-ok
  S112:Q03-ordering OK occurrences=1 anchor=24-ok
  S112:Q09-partial-tokens OK occurrences=1 anchor=166-ok
  S112:Q10-individual-1000 OK occurrences=1 anchor=168-ok
  S112:Q11-total-3000 OK occurrences=1 anchor=169-ok
  S112:Q13-next-request OK occurrences=1 anchor=195-ok
  ```
- Independent quote counts: Q01 `occurrences=1 anchor=24 anchor_ok=True`; Q02 `1/24/True`; Q03 `1/24/True`; Q09 `1/166/True`; Q10 `1/168/True`; Q11 `1/169/True`; Q13 `1/195/True`.
- B6 per-quote matched files: Q01 ∅, Q02 ∅, Q03 ∅, Q09 ∅, Q10 ∅, Q11 ∅, Q13 ∅ (grep rc=1, no filenames printed). Absence holds at freeze; non-trivially so — none of the 91 existing entries already carries these exact lines.

## Export-artifact note (not a lane defect)

`recheck-audit.py` run **without** `--cdroot` inside either archive export exits 1: `strict pass=0/91 cdroot_fail=91 instrument_fail=0 own_fail=0`, while the expect block still reads `expected=91 missing=0 unexpected=0`. Cause is in the instrument (line 143: `os.path.abspath(cd_target) == (cdroot or root)`; `--cdroot` help: "set it when --root is a scratch copy of the corpus"): the knowledge recheck lines `cd` into the real lane root, which never equals a `git archive` export path. With the documented `--cdroot <lane>` both exports reproduce the frozen base control exactly (`strict pass=91/91`, exit 0). Row 6 of the table uses the documented scratch mode; the plain-export rc1 is recorded here so no reviewer mistakes it for a regression.

## Cross-check against frozen controls (claims.json `controls`)

- `c2-donothing-counters-r78.txt` (rows=53 admitted=53 registry=112; knowledge=91; 93 lines/91 .md): reproduced (freeze `knowledge-expected.txt` = 93 lines).
- `c2-recheck-audit-base-r78.txt` (expected=91 missing=0 unexpected=0 exit0): reproduced via documented `--cdroot` mode.
- `c2-prerecheck-r78.txt` (7/7 quotes anchor-ok rc0): reproduced, byte-for-byte shape.

## Findings

- **None.** No routed defect: every instrument honored `TMPDIR` (all scratch writes confined to `$S/tmp`; the audits are parse-only), no counter wrote outside TMPDIR, no unexpected tree mutation, and the C2 do-nothing baseline (rows=53, admitted=53, knowledge=91, registry=112, S112 `queued`) matches the frozen receipts exactly at both commits.
- F54 landing predicates (B1 diff queued→mined, B2 91→92, B3 rows=54, B7 census script) are landing-commit predicates and are correctly **not yet observable** at the freeze commit; nothing in this replay contradicts them.
- Do-nothing conclusion holds: a base-bytes tree cannot produce rows=54 / knowledge=92 / `cases=13` — confirmed independently on both exports.

## Scratch hygiene

`$S = /fast/scratch/hyaku/kasegi-r78/ExecC2Replay` (exports `base/`, `freeze/`, `tmp/`, one helper `quotecheck.py`) deleted before yield. Nothing under `/tmp` except transient shell state; no counter/gate output written under `/tmp`.
