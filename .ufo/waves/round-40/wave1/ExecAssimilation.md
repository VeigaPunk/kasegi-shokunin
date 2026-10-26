# ExecAssimilation — receipt (kasegi round 40, wave 1)

Item: run the §10 assimilation id-collision guard and the quarantine slice verdicts, read-only
against `/home/vgpnk/Projects/shokuknow`. Lane repo only: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Lane head at measurement `5e985b74075dd3813a63d7750966bf8abf693465` (claims freeze); claim base
`a7af2ce63bce153757d39bf66b366a96caf30c13`.

Deliverable: `.ufo/waves/round-40/wave1/ExecAssimilation.txt` — **287 lines, 16913 bytes,
sha256 `eafa02c116e9d191b1fd48061698e037a78069223d673dc4244c4333077f35b6`**.

## What ran (actual output)

Pins, `2026-10-26T21:17:26Z` (`sha256sum`):

```
f33d10f45142b6d59969cedbfc35a1d29a3ba672d62067da8424fc0d32a728f2  corpus/SOURCES.md
4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb  …/merge/kasegi/SOURCES.append.md
```

Re-pinned after all measurements, `2026-10-26T21:23:10Z`: both hashes unchanged; lane rows 59;
`comm -12` still 29. The package sha256 is byte-identical to round 39's (`4fe049cb…`).

1. **Id extraction and collision (0-3-space pattern).**

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u | wc -l   -> 59
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' …/SOURCES.append.md | grep -oE 'S[0-9]+' | sort -u | wc -l -> 94
reg-ids=59 staged-ids=94 collisions=29
collisions: S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047
            S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059
```

Column-zero-only pattern on the same live files: `col0 reg=59 staged=94 collisions=29` — the two
forms agree **today** because `grep -cE '^ {1,3}\|[[:space:]]*S[0-9]{3,}'` → `0` for both files.

2. **Guard proof on the indented S002 fixture** (`fixture/fixture-SOURCES.md` row 2 indented two
spaces, staged fixture carries S002 at column 0), full transcript in deliverable §6:

```
a-reg-ids   lines=2  S001 S002
a-staged-ids lines=2  S002 S003
a-collisions lines=1  S002          <- 0-3-space form, nonempty, as required
b-reg-ids   lines=1  S001
b-staged-ids lines=2  S002 S003
b-collisions lines=0                <- ^|-only form misses the indented duplicate
```

3. **Document-level duplicate analysis (new this round).** Parsed URL per row on both files:
`document-level duplicate staged rows: 21`, `same id AND same url: ['S042']`,
`same id, different url (true id collision): 28`. 15 of the 29 colliding numbers are documents the
lane already holds (S031–S035, S039–S043, S049, S050, S055–S057); 14 name documents the lane does not
hold. Staged `S060` = Hitachi HIRT-PUB10008 = lane `S039`'s document, sitting exactly at the id the
round-40 coverage rows take.

4. **Quarantine slice — 7 kasegi rows** (2 `payload-absent` + 5 never-checked). Live re-checks,
`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`, all at `2026-10-26T21:18Z`:

```
2026-10-26T21:18:07Z  openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE…  http=200 bytes=24131
2026-10-26T21:18:10Z  ipa.go.jp/…/ug65p90000019by0-att/request_to_ipa.pdf    http=200 bytes=513648
2026-10-26T21:18:11Z  npc.gov.cn/…/P020260904396146393500.pdf                http=200 bytes=7465472
2026-10-26T21:18:54Z  std.samr.gov.cn/dcpspTools/gbPlan/download?path=…      http=200 bytes=0
2026-10-26T21:18:57Z  std.samr.gov.cn/gb/search/gbDetailed?id=3B865A93…     http=404 bytes=748
```

Text probes:

- openstd: `标准号：GB/T 30279-2020`, `中文标准名称：信息安全技术 网络安全漏洞分类分级指南`,
  `标准状态： 现行`, `发布日期 2020-11-19`, `实施日期 2021-06-01` all present (each grep `-c` ≥1).
- IPA PDF: `pdftotext -enc UTF-8` → 8785 bytes; line 42 `…の悪用が確認`, line 43
  `されたもの又は疑われるもの` — payload present with an elided parenthetical and a line wrap.
- npc PDF: bare `pdftotext` → **0 bytes**; `pdftotext -layout` → 34332 bytes; line 1182 `刑法（7 件）`,
  line 1184 `1． 中华人民共和国刑法（1979 年通过，1997 年修订，` … `2009 年修正）`.
- dcpsp: 200 with a zero-byte body → nothing obtainable.

Verdicts: **S037 refuse (not fabrication), S054 refuse (not fabrication), S048 unreachable,
S065 refuse (payload verified; entry gate fails), S068 refuse (duplicate of lane S040),
S069 unreachable, S070 unreachable. Adopted 0.**

Entry-gate basis (read from the package, read-only): staged `chinese-vulnerability-taxonomy-and-grading.md`
says `ground: F14 (new frontier item)` while lane F14 is *Japanese severity vocabulary and the
handling-priority model* (`corpus/README.md:284`); staged `chinese-statute-version-drift-…-r4-amendment.md`
says `ground: F17` while lane F17 is *Immunefi VSCS v2.2* (`corpus/README.md:361`); staged
`vendor-cvd-policy-crosswalk-2026-10-23.md` says `ground: F20` while lane F20 is *SSVC*
(`corpus/README.md:416`) and vendor-policy-as-object is F10 (`:211`). Round 24 judged the Chinese
national-grading-standard family adjacent (r24 lesson, scope check).

## Scope and hygiene

- Writes: this receipt and `ExecAssimilation.txt` only. No lane file, no fleet file, no
  `shokuknow` write, no campaign tool run, no git/jj mutation anywhere.
- Scratch `/fast/scratch/hyaku/kasegi-r40/ExecAssimilation` (fixtures, fetches, transcripts) removed
  after copying results into the wave dir; verified absent.
- No tool install or upgrade was needed; nothing recorded under the tooling directive.
- Disk guard green at start (`/fast/scratch/hyaku` 26% used, 600.2G free).

## Risks / handoffs

- The 29-collision figure is a **lower bound for the round**: staged numbers S060–S124 are all free
  lane ids today, so every round-40 `S060+` admission lands inside the staged range. The guard must
  be re-run after those rows land (deliverable §5.2, §8.2).
- The register's class labels are partly stale for kasegi: S048 is a 404 (page gone), S065 is now
  reachable, and the two `payload-absent` rows are quote-shape defects, not fabrications. The
  register itself is a `shokuknow` artifact — not edited by this seat.
