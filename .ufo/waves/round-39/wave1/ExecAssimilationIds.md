# ExecAssimilationIds — read-only assimilation guard re-run + quarantine verdicts (round 39)

Seat: `ExecAssimilationIds` (executor, leaf; no subagent dispatch, no swarm, no background job).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; fleet root and `/home/vgpnk/Projects/shokuknow`
read-only. Base commit `480b1a505a2dfc14a4f718d16d63808247214d0a` (claims freeze
`dcd31701720a6a4929a32471a62011ed87103421`). Axes: `depth:verifiability` (primary), `coverage` untouched.
Answering model run: `opencode-go/deepseek-v4.1-flash` (runtime route; no model chosen by this seat).
Tools installed or upgraded: **none** (no pacman transaction, no uv/npx/binary download; `git show`,
`grep`, `awk`, `comm`, `sort`, `sha256sum`, `curl`, `pdftotext` 26.08.0, `python3` stdlib only). No mutating
git/jj command. No write outside the wave dir deliverables named below and my scratch (now removed).
No network beyond the seven slice locators (six unique URLs), UA `kasegi-shokunin/1.0`.

Scratch: `S=/fast/scratch/hyaku/kasegi-r39/ExecAssimilationIds` (disk guard green at entry: `/fast/scratch/hyaku`
24%, 611.0G free). Removed at the end; see §7.

Conclusion up front: **the lane adopts nothing.** The staged package is byte-identical to the round-31 package
(`SOURCES.append.md` sha `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb`), the id-space
collision set is 25 (`S031`–`S055`), and no slice row is adoptable on live re-measurement (0 present-and-located,
2 quote-defective, 4 unreachable, 1 unverifiable). Details and exact commands below.

---

## 1. Inputs measured (read-only)

| input | location | lines | bytes | sha256 |
|---|---|---|---|---|
| lane registry at base | `git show 480b1a5…:corpus/SOURCES.md` → `base-SOURCES.md` | 122 | 75948 | `88bcd8c6bfbdca2180a113a60f0c7c3869ace3fd331d8118b65a39cbbf29ae61` |
| staged package | `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` | — | 89718 | `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb` |
| absent-defect register | `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` | 375 | — | `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833` |

Register and package digests equal the round-30/31 measurement set (`5afe1810…`, `4fe049cb…`), so nothing moved
under the read-only sources between those rounds and this one. Lane HEAD at measurement was
`d65d823e7c84813c192b20ee757a8761f878a61f` (`round-39: wave1 spec/dispatch`), a descendant of both base and
claims-freeze (`merge-base --is-ancestor` returned 0 for each); the lane worktree registry row count at HEAD and
in the worktree was 55, matching the base blob.

---

## 2. ID extractor (0-3-space guard) — run on both sides

Frozen extractor, unchanged from round 30 (`ConnStagedCensus.md`) / round 31 (`ScribeGateDraft.md`):

```
PAT='^ {0,3}\|[[:space:]]*S[0-9]{3,}'
grep -oE "$PAT" base-SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids
grep -oE "$PAT" /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > staged-ids
comm -12 reg-ids staged-ids > collisions
```

Actual output:

```
$ wc -l reg-ids staged-ids collisions
 55 reg-ids
 94 staged-ids
 25 collisions
$ sha256sum reg-ids staged-ids collisions
cd5ee2d942f27a618c6a7066e663c2012e914454c5b1eb4e218bbddb1a355df9  reg-ids
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  staged-ids
0875ecb42ce8beede45a9278071690029d86da04a687d0ad1b2e572f1fa203a1  collisions
$ tr '\n' ' ' < collisions
S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055
```

Ranges: `reg-ids` = `S001`–`S055` (55), `staged-ids` = `S031`–`S124` (94), `collisions` = `S031`–`S055` (25).

Cross-round control, measured this seat on the committed round-31 artifacts:

```
$ sha256sum .ufo/waves/round-31/assimilation/{reg-ids,staged-ids,collisions}
ab66f54a2135cea0359318caabb77575740093a32d7be7eb4bde47687be373c9  reg-ids     (47 lines)
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  staged-ids  (94 lines)
ac78cd564ab864b574e0d54d4e4656d448439403839530bb3044d04175acd2d2  collisions  (17 lines)
```

`staged-ids` is byte-identical to round 31 (the package did not move). `reg-ids`/`collisions` grew by 8 ids
because the base now carries `S048`–`S055`; the collision tail moved from `S047,S048` (round 31) to `S055`. The
guard's discriminating property is unchanged.

## 3. Guard proof (sensitivity fixture) — recorded

Scratch fixture, two sides, with the indented row the assignment names:

```
$ printf '| S001 | first doc |\n  | S002 | indented staged doc |\n| S003 | third doc |\n' > fx/fixture-SOURCES.md
$ printf '| S002 | staged doc from package |\n| S009 | other staged doc |\n' > fx/fixture-SOURCES.append.md
$ grep -n 'S002' fx/fixture-SOURCES.md | cat -A
2:  | S002 | indented staged doc |$

-- guard pattern (0-3 leading spaces) --
reg-ids  = S001,S002,S003
staged   = S002,S009
collisions (comm -12) = S002        lines=1

-- column-zero-only control (^\|) --
reg-ids  = S001,S003
collisions (comm -12) =              lines=0
```

Nonempty collisions under the guard, empty under the strict column-zero pattern: the 0-3-space allowance is
required to catch an indented registry row, and the fixture proves it is not a no-op.

## 4. Quarantine slice — frozen awk, byte-exact

```
awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" > quarantine-slice
```

Actual output (`cat -A`, trailing `$` is EOL):

```
 S037   `payload-absent` $
 S054   `payload-absent` $
 S048`   the cited source could not be fetched, so no quote was checked $
 S065`   the cited source could not be fetched, so no quote was checked $
 S068`   the cited source could not be fetched, so no quote was checked $
 S069`   the cited source could not be fetched, so no quote was checked $
 S070`   the cited source could not be fetched, so no quote was checked $
```

- 7 lines, 417 bytes, sha256 `d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862`.
- **Byte-equal to the round-30 committed slice** `.ufo/waves/round-30/assimilation/quarantine-slice`
  (417 B, same digest), so the extraction reproduces across rounds.
- Every line carries an S-id: `awk '{ if ($0 !~ /S[0-9]+/) bad=1 } END { … }'` → `all lines carry an S-id`.
- The two checked rows carry the class cell; the five never-checked rows carry the register's glued trailing
  backtick in the id cell (`S048``), which still satisfies `S[0-9]+` — noted so a reader does not read the
  backtick as corruption.

## 5. Live re-measure of every slice row

Method: `curl -sS -L --max-time 90 -A 'kasegi-shokunin/1.0'`, one request per unique URL (S069 and S070 cite the
same URL), output kept in scratch, `pdftotext` 26.08.0 for PDFs. Full evidence, quote searches and anchors are in
`wave1/ExecAssimilationIds.quarantine-verdicts.md`.

| id | http | bytes | payload sha256 | verdict | anchor |
|---|---|---|---|---|---|
| S037 | 200 | 24131 | `add55637…fa3737` | `quote-defective` | title L16, `标准状态：` L18/`现行` L19, `发布日期` L27/`2020-11-19` L28, `实施日期` L29/`2021-06-01` L30 |
| S054 | 200 | 513648 | `0150c9d1…b12b88` | `quote-defective` | `（ア） 脆弱性（…）の悪用が確認` L42 + `されたもの又は疑われるもの` L43 |
| S048 | 404 | 748 | `95cd25d8…2e2436` | `unreachable` | none (`HTTP状态 404 - 未找到`) |
| S065 | 200 | 7465472 | `e33b0f67…586d83` | `unverifiable` | document L1 `现行有效法律目录（303 件）`; no quote cell |
| S068 | 403 | 465 | `dd13cbcc…9567ae` | `unreachable` | none (`Access Denied`) |
| S069 | 200 | 0 | `e3b0c442…b855` | `unreachable` | none (empty payload) |
| S070 | 200 | 0 | `e3b0c442…b855` | `unreachable` | none (same URL/measurement as S069) |

Key counts behind the two `quote-defective` verdicts:

```
S037: whole recorded quote occurrences in tag-stripped page = 0
      '发布日期：' count 0, '实施日期：' count 0   (page cells carry no colon)
      every factual token present: 标准号：GB/T 30279-2020 L14; title L16; 现行 L19; 2020-11-19 L28; 2021-06-01 L30
S054: whitespace-normalized occurrences of recorded quote = 0 (both pdftotext modes)
      'の悪用が確認されたもの又は疑われるもの' = 1 (L42→L43)
      the quote elides '（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）' with no marker
```

Determinism: S048 retried (19:33:24Z) → 404/748 B, same sha `95cd25d8…` (equals the round-36 verifier's recorded
404 body sha); S068 retried → 403/465 B, and two further fetches at 19:35:14Z (`ff047965…a66a847`,
`dc0ea0f0…41e6cef7`) differ only in the `Reference #` id line and the mirrored `errors.edgesuite.net` URL
(`diff -u` shows nothing else), so the per-request digest is not a payload difference; S069 retried → 200/0 B.
Nothing is labelled a fabrication; the honest reading of S037/S054 is a located quote-level
defect (field concatenation with added punctuation / definition spliced out), which is why neither may be quoted
or adopted until requoted. A stricter reader who maps "not verbatim" onto `unreachable` gets the same action
(non-adoptable); the vocabulary in the deliverable states the rule explicitly.

## 6. Deliverables (written beside this receipt)

| file | lines | bytes | sha256 |
|---|---|---|---|
| `ExecAssimilationIds.reg-ids` | 55 | 275 | `cd5ee2d942f27a618c6a7066e663c2012e914454c5b1eb4e218bbddb1a355df9` |
| `ExecAssimilationIds.staged-ids` | 94 | 470 | `550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f` |
| `ExecAssimilationIds.collisions` | 25 | 125 | `0875ecb42ce8beede45a9278071690029d86da04a687d0ad1b2e572f1fa203a1` |
| `ExecAssimilationIds.quarantine-slice` | 7 | 417 | `d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862` |
| `ExecAssimilationIds.quarantine-verdicts.md` | 170 | 11128 | `28a721d30fdbc38139fa942bb68d11518d32532a951645331286081f2e290cfd` |

The four list files are pure data (one id / one frozen-awk line per record, no headings, no notes) so they can be
landed as bytes. The verdict table is the advisory deliverable and carries its own method + evidence; it is not
landed text.

## 7. Scratch quiescence

Scratch was under `/fast/scratch/hyaku/kasegi-r39/ExecAssimilationIds`; all downloads, extracted PDF/HTML text
and the guard fixture lived there. Removed with `rm -rf -- "$S"` after the deliverables were copied out and
re-hashed. Post-removal check: `ls /fast/scratch/hyaku/kasegi-r39/` → only sibling seats' entries (this seat's
directory absent); `find /fast/scratch/hyaku -maxdepth 2 -name 'kasegi-r3*'` shows no `kasegi-r37`/`kasegi-r38`
entry created by me and no `ExecAssimilationIds` entry.

## 8. Risks and notes for the L1

1. **Adoption is zero, by evidence not by policy.** The package digest is unchanged since round 31 and every
   staged id in the lane's id space (`S031`–`S055`) collides; the staged entries that were refused in rounds
   29–31 are the same bytes. Nothing this seat measured supplies a flip.
2. **S037/S054 verdict wording.** Both are reachable and their quoted claims are located, but the recorded
   spans are not verbatim. I used `quote-defective` (located defect) rather than `unreachable`; the action is
   identical — requote before any adoption — and the deliverable states the mapping so a reviewer can dissent
   without ambiguity.
3. **S065 resolves now** (200, 7.4 MB, `现行有效法律目录（303 件）`), which contradicts the register's
   never-checked reason for that row. It carries no quote, so it stays `unverifiable`; the register itself is
   read-only and was not edited.
4. **S069/S070 share one URL** that returns 200 with zero bytes both attempts; the register's suspicion that the
   locator is truncated is consistent with that, and no filename was invented.
5. **No lane file names the judged head.** This receipt names the base and claims-freeze commits only; the
   round-39 judged head is the L1's to record by reference (C1 G5).
