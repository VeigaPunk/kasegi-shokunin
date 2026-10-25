# SimplBloat — round-28 wave-evidence economy sweep (R14 practice)

Seat: `SimplBloat` (simplifier, leaf; no subagents, no background waves, no production edits).
Round: 28, wave 1. Date: **2026-10-25** (UTC). Lane root
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, lane base
`c9f8b115a098c65356e4b3b6048af45a37ab8395`, measured at `HEAD = 94f387c`.
Every figure below was produced by a command this seat ran in this session; nothing is copied
from another seat's receipt as measurement. Where a figure is another seat's, it is attributed.

Axis named: **depth:verifiability** (R14 practice instance: can the round's evidence be reviewed
and regenerated from committed bytes without carrying a second copy of the corpus?).

---

## 1. Measurement of `.ufo/waves/round-28/` as it exists now

Snapshot **2026-10-25T17:48:48Z**, `HEAD 94f387c`:

| quantity | command | value |
|---|---|---|
| apparent bytes | `du -sb .ufo/waves/round-28 \| cut -f1` | **13,395,335** (12.77 MiB) |
| disk (1 KiB blocks) | `du -sk .ufo/waves/round-28` | **13,856** (13.5 MiB) |
| files | `find .ufo/waves/round-28 -type f \| wc -l` | **360** |
| dirs | `find .ufo/waves/round-28 -type d \| wc -l` | 59 |
| symlinks | `find .ufo/waves/round-28 -type l \| wc -l` | 3 |
| **unique blob bytes** (sha256 de-dup) | python walk | **11,525,047** across 295 unique blobs |
| **redundant bytes** | total − unique | **1,870,102** (14.0 % of the tree) |
| committed at HEAD | `git ls-tree -r -l HEAD -- .ufo/waves/round-28` | **13 files / 297,893 B** (2.2 % of the working tree) |
| receipts | `find receipts -type f` | **36 files / 448,675 B**, largest **41,201 B** (`ExecRecheckAuditR28.txt`) |

The wave was still landing while I measured (the tree grew 301,632 B / 20 files at 17:23Z →
13,395,335 B / 360 files at 17:51Z). Figures are timestamped, not round-final; re-run the two
commands in §1 to re-measure.

## 2. Artifacts over 256 KiB (the flag rule) — exactly two, both flagged

`find .ufo/waves/round-28 -type f -size +256k`

| bytes | path | class | verdict |
|---|---|---|---|
| 7,465,472 | `wave1/ScribeLessonGate/S065.body` | **raw fetch body** (PDF, `%PDF-1.7`, sha256 `e33b0f67293441f19ee519b2ed1619121da84867aa8396a3a16facd572586d83`) | **FLAGGED** — not a capture snapshot, not an instrument |
| 513,648 | `wave1/ScribeLessonGate/S054.body` | **raw fetch body** (PDF 1.7, sha256 `0150c9d15dee603f55573f4692f306ba8ff46f70454b032f813b95fbdbb12b88`) | **FLAGGED** — same |

Why they are not covered by the exemption: `corpus/source-snapshots/round-28/manifest.json`
binds exactly two ids, `['S041','S042']`; S054/S065 are neither manifest records nor registry rows
(`grep -cE '^\s{0,3}\| *S05[45] *\|' corpus/SOURCES.md` → 0; same for `S06[58]` → 0). They are
fetch scratch for the lesson-gate quarantine hand-check, retained with no digest in any receipt
(`grep -rn 'S065.body\|e33b0f67' receipts/ wave1/*.md` → no hits).

No other artifact exceeds 256 KiB. Next largest are three **control-plane** files under the
threshold (`wave1-dispatch.json` 102,538 B, `wave1-spec.json` 75,968 B, `build-wave1-spec.py`
67,176 B) and nine capture-sized copies (147,267 B / 60,508 B, §5). Receipts comply with the
"text, kilobytes at most" bar: 36 files, mean 12.2 KiB, max 41,201 B — 34 `text/plain`, 1 `text/x-diff`, and
1 `text/html` MIME sniff on `ExecCaptureS042.txt` that is a plain-text receipt (`file` mis-sniffs it;
`grep -c "<html\|<div\|<script"` → 0).

The seat tree carrying them is also the largest seat: `du -sb wave1/ScribeLessonGate` →
**8,258,680 B / 23 files**; the two bodies are **96.8 %** of it (`8,098,084 B`). Everything the
gate actually asserts is carried by the text side — `*.norm` 111,342 B total, `*.txt` 49,254 B,
`quarantine-handcheck.out` 1,636 B, `quarantine-handcheck.sh` 2,792 B — and the gate verdicts
reproduce from the `.norm` files alone (measured: S037 anchor 1×, S048 0×, S054 0×, S065 1×,
S068 1× — the same counts the `.out` records).

## 3. R14 remedy, with exact commands and real digests

Rehearsed in `mktemp -d`, nothing written into the lane. All tarballs are **reproducible**:
`sorted + mtime=0 + uid/gid 0` gives byte-identical rebuilds (`cmp` → identical on re-run).

**A. Keep the evidence, drop the bulk (recommended).** One content-addressed tarball for the
whole wave tree with the raw bodies excluded:

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
tar --sort=name --mtime='@0' --owner=0 --group=0 --numeric-owner --format=posix \
    -cf /tmp/round-28-wave-evidence.tar -C .ufo/waves/round-28 --exclude='*.body' .
zstd -19 -q -c /tmp/round-28-wave-evidence.tar > /tmp/round-28-wave-evidence.tar.zst
sha256sum /tmp/round-28-wave-evidence.tar /tmp/round-28-wave-evidence.tar.zst
```

Measured: tar **6,000,640 B**, sha256 `7292c58eadc2b3d467bbdbff2f1f6946449db269d076b10e308997d1da086937`;
zstd **489,687 B**. Working tree 13,395,335 B → **489,687 B is 27× smaller**, at 360 → 355 paths
and zero loss of a text artefact.

**B. If the fetched PDFs must be kept as bytes.** One content-addressed tarball, digest in the
receipt (this is the literal R14 wording):

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-28/wave1/ScribeLessonGate
tar --sort=name --mtime='@0' --owner=0 --group=0 --numeric-owner --format=posix \
    -cf /tmp/slgate-bodies.tar S037.body S048.body S054.body S065.body S068.body
sha256sum /tmp/slgate-bodies.tar
```

Measured: **8,110,080 B**, sha256 `8b8750c6a61f0b81e22e563c40063aaaf589d8eb45b7aca2ca228823b2a7c3e1`;
zstd `7,990,832 B` — the PDFs do not compress, so the tarball only buys path-count reduction, not
bytes. The lean half alone is **194,560 B**, sha256
`91ac8587769e1cddded1255d8e0c9f698a1865c47d6e56e954a4dafa870c6557`:

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
tar --sort=name --mtime='@0' --owner=0 --group=0 --numeric-owner --format=posix \
    -cf /tmp/slgate-lean.tar -C .ufo/waves/round-28/wave1/ScribeLessonGate --exclude='*.body' .
mkdir /tmp/slgate-x && tar -xf /tmp/slgate-lean.tar -C /tmp/slgate-x
diff -r --brief .ufo/waves/round-28/wave1/ScribeLessonGate /tmp/slgate-x
```

Measured round-trip: exactly **5** difference lines, all
`Only in …: S{037,048,054,065,068}.body` — the excluded bodies and nothing else, so the lean
tarball is a lossless archive of every artefact the gate asserts from.

**C. Regeneration arm (measured, and it works here).** All five bodies reproduce **byte-identically**
by re-fetch today with the instrument UA
`kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`
(`corpus/instruments/capture-source.py:32`), `curl -sS -L --max-time 120 -A "<UA>"`:

| id | http | bytes | sha256 | refetch verdict |
|---|---|---|---|---|
| S065 | 200 | 7,465,472 | `e33b0f67…` | `cmp` → identical |
| S054 | 200 | 513,648 | `0150c9d1…` | `cmp` → identical |
| S037 | 200 | 24,189 | `9cba2e96…` | identical |
| S048 | **404** | 748 | `95cd25d8…` | identical (the 404 page itself is the captured body) |
| S068 | 200 | 94,027 | `098f99a8…` | identical |

So the cheaper arm for A/B is a **named regeneration script instead of the bytes**: keep
`quarantine-handcheck.sh` (2,792 B, already in-tree, already produces `.body/.txt/.norm/.stderr`)
plus the five expected sha256 values above in the receipt, and delete the bodies. That satisfies
R14's second arm ("regenerated from `git archive <rev>` plus a named mutation script") without any
new tarball.

**D. `git archive` arm for what is already committed.** `Get-Content`-free, no writes:
`git archive HEAD -- .ufo/waves/round-28` → **317,440 B**, sha256
`7cf2a79fa824dc8dac0b33b8a80866cf50402671275804dde9b47f419a27f46c`.

## 4. Did anyone commit a full-corpus copy this round? **No.**

Baseline — what the round-25 mistake actually was (re-measured, not quoted):

* `.ufo/waves/round-25/c1-after-35` at `98261eb` = **115 files / 1,822,119 B**, and **115/115 blobs
  are byte-identical to that same commit's `corpus/`**. File set = parent `corpus/` (107 paths) ∪
  the 7 corpus files that same commit added → a **superset copy of the live corpus**.
* It was not alone: `c1-controls/{M1-parse,base,do-nothing,M2-cwd,M3-paths,M4-degenerate}/corpus`
  were six more full copies — **108 files / ~1,683,500 B each**, each also a superset of the
  parent corpus (`comm -23` → no missing paths).
* Effect on the commit: `.ufo/waves/round-25` tracked **3,773 paths / 57,511,001 B**; the commit
  still cost **550 new objects / 5,156,417 B** even after git's own blob de-dup (335 of the 773
  distinct blobs already existed). That is the "+850,085 lines, compare API truncates at 300
  files" finding in `corpus/lessons/round-25-verifier-spotcheck.md:163-165`.

Round 28, checked three ways:

1. **Committed bytes:** 13 tracked paths / 297,893 B under `.ufo/waves/round-28`.
   `comm -12` of round-28 tracked blob ids against `HEAD:corpus` blob ids → **0 shared blobs**.
   `git ls-tree -r --name-only HEAD -- .ufo/waves/round-28 | grep -c '/corpus/'` → **0**.
2. **Any `corpus/`-shaped directory >= 20 files in the working tree:** currently **none**
   (was 12 — see §6, a near-miss that pruned itself).
3. **Content identity, not names:** 24 wave-tree files are byte-identical to a live corpus file,
   **1,591,773 B** total. They are single-file scratch mirrors, not corpus trees:

   | copies | file | corpus original |
   |---|---|---|
   | 7 | `S041.txt` (147,267 B) | `corpus/source-snapshots/round-28/S041.txt` |
   | 7 | `S042.txt` (60,508 B) | `corpus/source-snapshots/round-28/S042.txt` |
   | 6 | `manifest.json` (5,038 B) | `corpus/source-snapshots/round-28/manifest.json` |
   | 4 | `anchorcheck*.py` (26,780 B) | `corpus/instruments/anchorcheck.py` |

   None of the 24 is tracked (all under `git status` `??`), and all 24 blobs are **new** to `.git`
   (`git cat-file -e` → absent), i.e. they would cost 1,591,773 B exactly once if staged.

Closest thing to a corpus copy this round: `assimilation/schema{,2,3,4}/corpus/SOURCES.md`
(34,262–35,679 B) and `assimilation/base/SOURCES.md` (32,215 B, byte-identical to
`c9f8b11:corpus/SOURCES.md`). These are **single-file** registry fixtures for grammar/indent
experiments, 5 files / 172,036 B total — 1.4 % of the live corpus (2,133,023 B, 128 tracked files)
and materially below a corpus copy. Acceptable under R14; named here so the L1 sees them.

## 5. Redundancy, and what it would cost at commit time

`1,870,102 B` of the 13,395,149 B is duplicate. Top groups (waste = size × (copies − 1)):

| waste | size | copies | exemplar |
|---|---|---|---|
| 883,602 | 147,267 | 7 | `wave1/MutManifestC2/m1/S041.txt` (+ `pristine`, `m2`, `m3`, `m3b`, `MutQuoteC2/work`, `ScribeEntryC2/scratch`) |
| 363,048 | 60,508 | 7 | same seven dirs, `S042.txt` |
| 273,150 | 27,315 | 11 | `wave1/ExecReceiptCanonC1/skill.*.out` — SKILL.md captures |
| 81,009 | 27,003 | 4 | `wave1/ScribeSkillGate/*.n` |
| 80,340 | 26,780 | 4 | `wave1/MutSelftestC1/live-base.py` (anchorcheck copies) |
| 32,215 | 32,215 | 2 | `wave1/CritC2Kill/lab/pre-SOURCES.md` |
| 25,190 | 5,038 | 6 | `manifest.json` scratch copies |

Git de-dupes identical blobs, so this costs **0 extra object bytes** — but it triples the
**path** count, which is exactly what broke round-25 reviewability.

Staging projection (dry-run only; index left untouched — `git diff --cached --name-only` → 0):

| | paths | bytes | new object bytes |
|---|---|---|---|
| `git add .ufo/waves/round-28` as-is | **345** (342 files + 3 symlinks) | 12,950,359 (12.35 MiB) | 10,736,334 (260 new blobs) |
| with the exclusions below | **317** (314 files + 3 symlinks) | 3,352,434 (3.20 MiB) | 2,557,516 (250 new blobs) |

Recommended exclusion pathspec (verified: 0 `.body`, 0 scratch, 0 `try.txt` hits remain; no other
file drops):

```bash
git add .ufo/waves/round-28 \
  ':!*.body' ':!*/ScribeEntryC2/scratch/*' ':!*/MutManifestC2/*' ':!*/MutQuoteC2/*' \
  ':!*.try.txt' ':!*/__pycache__/*'
```

`__pycache__/` is already covered by `.gitignore:2`; it is spelled out for the L1's copy-paste
safety only (5 `.pyc`, 146,897 B, `git check-ignore` confirms ignored).

## 6. Near-miss worth recording: 12 live-corpus mirrors that pruned themselves

At **17:40:51Z** the same sweep measured `wave1/CritC2Kill/lab` at **26,604,423 B / 1,214 files**,
holding **12** directories of 98–101 files each (2,164,900–2,377,841 B), i.e. **26,268,175 B**
(66 % of the whole wave tree) of per-chain copies of the live corpus:

```
lab/{chain,chain2,chain3,j0,j3,j4,j8,jhid,w4a,w4b,w4c,w4d}/corpus
```

Measured fidelity of one chain: 99 files, **96 byte-identical to live corpus files**, file set =
live `corpus/` minus 39 (all 37 `lessons/` + `QUALITY.md` + the new entry) plus 1 stub → a
**pruned corpus copy**, not a fixture set. The seat also left no builder script, so those trees
were only reproducible by re-running `cp -a corpus`. Had they landed, this round would have been
round-25's mistake at roughly **half its byte cost but 1,157 extra staged paths** (measured at
17:41Z: `git add --dry-run | grep -c CritC2Kill/lab` → 1,157).

By 17:42:14Z the directory had been emptied by its owner: `wave1/CritC2Kill` is now
**137,564 B / 26 files**, `find -type d -name corpus` under it → none. Nothing was committed
(`git log --all -- .ufo/waves/round-28/wave1/CritC2Kill/lab` → empty). Recorded because the
detector, not luck, is the transferable part:

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
for d in $(find .ufo/waves/round-28 -type d -name corpus); do
  n=$(find "$d" -type f | wc -l); [ "$n" -ge 20 ] && echo "MIRROR $n $(du -sb "$d" | cut -f1) $d"
done
```

## 7. Depth:verifiability side-findings (deletion candidates, nothing deleted)

1. **`wave1-dispatch.json` is a derived duplicate of `wave1-spec.json` + `build-wave1-spec.py`.**
   Measured: `taskCall.context` is byte-identical to `spec["context"]`; all **69/69** `task` fields
   are exactly `spec.prompt` + a two-variant trailer that is a pure function of the item
   (`role == "executor"` → "… except your single labrat.", else "… no subagent dispatch.";
   `Judged on:` = `", ".join(axes)`; `Milestone:` = item milestone; `Report:` =
   `reportDir/<name>.md`) — 51 plain + 18 executor. 77,218 of the file's 102,538 B (75 %) are
   reconstructible; the remaining ~25 KB is `registry`/`counts`/`policy` bookkeeping. Candidate:
   regenerate rather than commit both. Kept as-is because §7 is advisory here and `wave1-dispatch.json`
   is cited by `LOG.md`, `corpus/lessons/round-28.md` and four wave reports.
2. **`build-wave1-spec.py` is deterministic.** Re-run with the output path redirected to a temp dir
   reproduces `wave1-spec.json` **byte-identically** (sha256
   `76e3560d78baec507c620962c069de555e18a1803bcdd8ff8624c5c8c95a7e45`, `cmp` → equal, lane tree
   untouched). So spec+dispatch are regenerable from 67 KB of script — the strongest single lever
   on this round's control-plane bytes.
3. **3 absolute symlinks into the live corpus** at
   `assimilation/schema{2,3,4}/corpus/knowledge -> <lane>/corpus/knowledge`. Safe for git —
   verified in a throwaway `mktemp -d` repo: `git ls-files -s` stores `120000` mode, 0 target bytes.
   **Unsafe for archives**: `tar -h` on the wave tree grew it by **583,680 B and embedded 123 live
   corpus entries** (`tar -tvf | grep -c corpus/knowledge` → 123). Any R14 tarball command MUST NOT
   use `-h`/`--dereference`; the commands in §3 do not.
4. **Correction to `receipts/ScribeR14.txt` §4 (its own file, not mine to edit).** Its "zero
   corpus-file copies" probe is name-based —
   `find … -name QUALITY.md -o -name SOURCES.md -o -name README.md -o -name anchorcheck.py` — and
   therefore cannot see content copies. Re-run verbatim *now* it returns **6**, not 0 (four
   `assimilation/*/corpus/SOURCES.md`, one `assimilation/base/SOURCES.md`, one
   `ExecInstrReadme/readme-base/README.md`, the latter byte-identical to `c9f8b11:corpus/instruments/README.md`).
   The content question is answered in §4: 24 corpus-identical files, no corpus tree. Also stale
   there: footprint `759,791 B / 53 files` (live-wave snapshot; final 13,395,335 B / 360 files) and
   "largest control tree 44 KiB, so no tarball is owed" — `c1-controls` is still 28,402 B, but
   `ScribeLessonGate` (8,258,680 B) post-dates that measurement and does owe one under R14 §3A/C.

## 8. Touched surfaces

* `.ufo/waves/round-28/wave1/SimplBloat.md` — this report (sole write, new file).
* `.ufo/waves/round-28/receipts/SimplBloat.txt` — this seat's receipt.
* Nothing else. **Zero production bytes** written; `corpus/instruments/anchorcheck.py` not touched
  or run (ExecImplC1 owns it). No VCS write (read-only `git log/ls-tree/status/check-ignore/
  hash-object/cat-file/archive` and `mktemp -d` + `git init` fixtures only). No tool installed, no
  pacman/uv/npx transaction, no writes to the fleet root, `/home/vgpnk/Projects/shokuknow`, `.ufo/state`,
  `MANIFEST.json`, `templates/` or fleet `scripts/`. One empty scratch dir I created
  (`wave1/SimplBloat/`) was removed before writing this report.

## 9. L1 verification commands

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
du -sb .ufo/waves/round-28 | cut -f1                    # 13362703 at 17:48:48Z (live wave; will drift)
find .ufo/waves/round-28 -type f | wc -l                # 360
find .ufo/waves/round-28 -type f -size +256k            # exactly S065.body, S054.body
find .ufo/waves/round-28/receipts -type f | wc -l       # 35
git ls-tree -r -l HEAD -- .ufo/waves/round-28 | awk '{s+=$4}END{print s}'   # 297893
for d in $(find .ufo/waves/round-28 -type d -name corpus); do n=$(find "$d" -type f|wc -l); [ "$n" -ge 20 ] && echo MIRROR $d; done   # empty
git log --all --oneline -- '.ufo/waves/round-28/wave1/CritC2Kill/lab'       # empty (never committed)
```
