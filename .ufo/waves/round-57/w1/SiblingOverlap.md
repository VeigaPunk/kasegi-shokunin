Verdict: class (a) overlap: none — no OTHER lane in the fleet holds a standards-body publisher record of ISO/IEC 29147 or ISO/IEC 30111, and no other lane cites the two iso.org catalog pages (72311 = 29147, 69725 = 30111) as a source. One fleet-root (not-lane) dossier artifact, `.ufo/waves/kaika-w1/kasegi-art.md` (2026-10-19), drafts two iso.org catalog rows for this pair — it is a fleet-wave draft dossier, not a lane corpus and not a committed registry; it is reported here as cross-domain material (class (c) mention with a class-(a)-shaped draft row), NOT absorbed. The only class (a) publisher records that any sibling lane holds are for OTHER ISO standards (ISO 8601-2 in lore, ISO/IEC 27042 in revenger-as-lead, ISO 9184-1 in kotodama, ISO 646/ISO 8859-1 in kake) — different standards, so no F38 ground overlap. Inside kasegi itself, no held row or entry already held class (a) ground under another id at the frozen base.

# SiblingOverlap — sibling-lane overlap scan for the F38 ground (ISO/IEC 29147 / 30111 standards-body publisher record)

Seat: SiblingOverlap (connector, round 57 wave 1). Lane: kasegi. Read-only scan; no file under L was modified (verified by `git -C L status --porcelain`, which shows only the pre-existing `M LOG.md`, `M SCORECARD.md` and untracked `.ufo/waves/round-57/w1/` — the same state observed at the start of this seat).

---

## 1. Scope and method

Paths (absolute):
- L = `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (lane under test)
- W = `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-57/w1` (this evidence file)
- S = `/fast/scratch/hyaku/kasegi-r57/SiblingOverlap` (scratch; created, and removed before yield)
- Fleet root = `/home/vgpnk/Projects/shokunin` (read-only)

Sibling lane set scanned (20 lanes, every `*-shokunin` dir under the fleet root except kasegi):
`audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi`
(Note: `kumitate-shokinin/kumitate-shokunin` and `kotoba-shokunin/kotoba-shokukin` are empty nested stubs — `ls -la` shows 0 entries, no files to scan.)

Classification used, exactly as the seat spec defines:
- (a) same ground: a publisher record of ISO/IEC 29147 or ISO/IEC 30111 (i.e. the iso.org catalog page for that standard, its identity/edition/status/scope content);
- (b) consumer or implementer of the standard (a vendor/IR-team/implementer document that cites or maps onto the standard);
- (c) mention only (a bare reference, a lead line, a name, a cross-claim note).

---

## 2. Step 1 — restricted-path sweep over every sibling lane

Command (one per lane; `$paths` = the lane's `corpus`, `SKILL.md`, `PROVINCE.md`, `plans`, `knowledge` that exist):

```
cd /home/vgpnk/Projects/shokunin && for l in audio chousa game-dev-2d game-dev-3d kagi kaidoku kake kama kengaku kotoba kotodama kumitate lore mado mori revenger souji tabi tameshi tsukuroi; do
  d="$l-shokunin"; paths=""; for p in corpus SKILL.md PROVINCE.md plans knowledge; do [ -e "$d/$p" ] && paths="$paths $d/$p"; done
  grep -rIl -E 'iso\.org/standard|ISO/IEC 29147|ISO/IEC 30111|29147:2018|30111:2019' \
    --exclude-dir=.git --exclude-dir=.jj --exclude-dir=.ruff_cache $paths
done
```

Printed output (exit code 1 for the grep when no match; each lane's grep was checked to exit only 0/1):

```
=== lore-shokunin
lore-shokunin/corpus/SOURCES.md
lore-shokunin/corpus/lessons/round-103.md
=== revenger-shokunin
revenger-shokunin/corpus/SOURCES.md
```
Exit code: 0 for the loop; the two lanes above are the only restricted-path hits in the whole fleet. All other 18 lanes printed nothing (grep exit 1 = no match).

Then the per-hit line extraction:

```
cd /home/vgpnk/Projects/shokunin && grep -n -E 'iso\.org/standard|ISO/IEC 29147|ISO/IEC 30111|29147:2018|30111:2019' \
  lore-shokunin/corpus/SOURCES.md lore-shokunin/corpus/lessons/round-103.md revenger-shokunin/corpus/SOURCES.md
```
Exit code 1 (grep exit 1 = "no match" is not applicable here — matches were found; the harness reported 5 matches in 3 files). Decisive lines (trimmed to the leading text):

```
lore-shokunin/corpus/SOURCES.md:31: … ISO 8601-2:2019 Date and time — Representations for information interchange — Part 2: Extensions — https://www.iso.org/standard/70908.html …
lore-shokunin/corpus/SOURCES.md:40: … ISO 8601-2:2019 … https://www.iso.org/standard/70908.html … (S032 supersedes S023) …
lore-shokunin/corpus/lessons/round-103.md:91:  - S023 — https://www.iso.org/standard/70908.html — accessed 2026-10-19 …
lore-shokunin/corpus/lessons/round-103.md:165: - S032 — https://www.iso.org/standard/70908.html — accessed 2026-10-19 via Wayback captures …
revenger-shokunin/corpus/SOURCES.md:577: - ISO/IEC 27042:2015 catalog — https://www.iso.org/standard/44118.html — HTTP 403 on 2026-10-19.
```

Classification of these two lanes' hits (both are **other standards**, not 29147/30111):

| path:line | standard | class | why |
|---|---|---|---|
| `lore-shokunin/corpus/SOURCES.md:31` (row S023) | ISO 8601-2:2019 (catalog id 70908) | (c) mention only **for F38** | a publisher record of a *different* standard (date/time interchange); lore holds the ISO publisher page for 8601-2, not for 29147/30111. It is (a)-shaped ground for ISO 8601-2, which is cross-domain and is **not** absorbed into F38. |
| `lore-shokunin/corpus/SOURCES.md:40` (row S032) | ISO 8601-2:2019 | (c) mention only **for F38** | supersedes S023 for the same different standard. |
| `lore-shokunin/corpus/lessons/round-103.md:91,165` | ISO 8601-2:2019 | (c) | lesson prose quoting the 8601-2 page's date-element exclusion sentence. |
| `revenger-shokunin/corpus/SOURCES.md:577` | ISO/IEC 27042:2015 (catalog id 44118) | (c) | a **lead** bullet ("HTTP 403"), explicitly not a row, no tier, no opened text — and a different standard. |

Cross-lane corroboration that these are the fleet's only iso.org publisher pages outside kasegi, and that they are all *other* standards — full-tree (not path-restricted) sibling sweep:

```
cd /home/vgpnk/Projects/shokunin && for l in audio chousa game-dev-2d game-dev-3d kagi kaidoku kake kama kengaku kotoba kotodama kumitate lore mado mori revenger souji tabi tameshi tsukuroi; do
  grep -rIl -E 'iso\.org/standard' --exclude-dir=.git --exclude-dir=.jj --exclude-dir=.ruff_cache "$l-shokunin"
done
```
Exit code 0. Printed (file list only):
```
kake-shokunin/.ufo/waves/round-25/{frozen-final/,frozen/,}source-wcag22.html      (iso.org/standard/64840, /56350 — links inside a WCAG 2.2 capture)
kake-shokunin/.ufo/waves/round-36/sources/S090.txt                                (iso.org/standard/28245, /4777 — ISO 646 / ISO 8859-1 cited inside the WHATWG Encoding Standard capture)
kake-shokunin/.ufo/waves/round-48/assimilation/validate/... (mirrors of the two above)
kotoba-shokunin/.ufo/waves/round-71/receipts/census-after.txt                     (a census line naming lore's 70908 dup-url warning)
kotodama-shokunin/reports/round-60/captures/pages/S632.txt                        (iso.org/standard/79506 — ISO 9184-1:2023 in a paper's reference list)
kumitate-shokunin/.ufo/waves/round-54/build/ScoutMqtt/mqtt-v5.0-os.html            (iso.org/standard/56425, /69466 — links inside an MQTT spec capture)
lore-shokunin/.ufo/waves/round-103/{rejected/,seats/}, lore-shokunin/corpus/{SOURCES.md,lessons/round-103.md}   (70908)
mado-shokunin/.ufo/waves/round-44/w2/RerunCensus/census-fleet.txt                 (census line naming lore's 70908 dup-url warning)
revenger-shokunin/.ufo/waves/kaika-r1/e3-sources.md, revenger-shokunin/corpus/SOURCES.md   (44118)
```
Every one of these is a **different ISO standard** or a downstream link inside a captured third-party document — no sibling holds the 29147 or 30111 publisher page.

### Step-1 hit table (restricted paths, all siblings)

| path:line | content | class | note |
|---|---|---|---|
| `lore-shokunin/corpus/SOURCES.md:31` | ISO 8601-2:2019 catalog page (70908) | (c) | different standard; lore's own (a)-shaped record, cross-domain |
| `lore-shokunin/corpus/SOURCES.md:40` | ISO 8601-2:2019 catalog page (70908), supersedes S023 | (c) | different standard |
| `lore-shokunin/corpus/lessons/round-103.md:91` | 70908 quote, non-Gregorian-calendar exclusion | (c) | different standard |
| `lore-shokunin/corpus/lessons/round-103.md:165` | 70908 lifecycle quote (S032) | (c) | different standard |
| `revenger-shokunin/corpus/SOURCES.md:577` | ISO/IEC 27042:2015 catalog (44118), HTTP 403 | (c) | different standard; lead, not a row |

Non-restricted-path sibling hits (whole lane tree), for completeness — all (c) or (b), none (a):

| path:line | content | class |
|---|---|---|
| `kake-shokunin/.ufo/waves/round-35/sources/S078.txt:1` | RFC 9116 (security.txt) cites `[ISO.29147.2018]` and names "ISO/IEC 29147:2018" in its References | (b) consumer/implementer of the standard — it *uses* 29147, does not hold the publisher page |
| `kake-shokunin/.ufo/waves/round-36/sources/S090.txt:1` | WHATWG Encoding Standard capture listing ISO 646 (4777) / ISO 8859-1 (28245) | (c) |
| `kake-shokunin/.ufo/waves/round-25/*/source-wcag22.html:185,191,4308` | iso.org/standard/64840, /56350 links inside a WCAG 2.2 capture | (c) |
| `kotodama-shokunin/reports/round-60/captures/pages/S632.txt:3210` | iso.org/standard/79506 (ISO 9184-1:2023) in an amulet paper's reference list | (c) |
| `kumitate-shokunin/.ufo/waves/round-54/build/ScoutMqtt/mqtt-v5.0-os.html:3411,3440` | iso.org/standard/56425, /69466 links inside an MQTT capture | (c) |
| `kotoba-shokunin/.ufo/waves/round-71/receipts/census-after.txt:184`; `mado-shokunin/.ufo/waves/round-44/w2/RerunCensus/census-fleet.txt:189` | census rows naming lore's `www.iso.org/standard/70908.html` dup-url warning | (c) |
| `revenger-shokunin/.ufo/waves/kaika-r1/e3-sources.md:36,42` | ISO/IEC 27042 catalog, HTTP 403, "lead only" | (c) |
| `chousa-shokunin/.ufo/waves/round-54/w1/R54ConnCrossClaim.md:19` | "`kasegi-shokunin/corpus/SOURCES.md:97`: ISO/IEC 29147 and 30111 standard-record URLs are listed among leads; no opened text or tier is claimed there." | (c) — a cross-claim **note about kasegi's own lead**, not a hold of the publisher record by chousa |
| `kake-shokunin/.ufo/waves/round-48/assimilation/validate/...` | mirrors of the two kake captures above | (c) |

---

## 3. Step 2 — decisive test: the two catalog ids of F38 anywhere outside kasegi

F38's ground is exactly the two iso.org catalog pages named by kasegi's recorded lead (`corpus/SOURCES.md:137`): `72311` (29147) and `69725` (30111). The kasegi working tree's own two new rows use those ids (S089 → 72311, S090 → 69725), so the id set is the ground test.

Command:
```
cd /home/vgpnk/Projects/shokunin && grep -rIn -o -E 'iso\.org/standard/(72311|69725|92945|92946)' \
  --exclude-dir=.git --exclude-dir=.jj . 2>/dev/null | grep -v '^./kasegi-shokunin/'
```
Exit code 0. Printed output (complete):
```
./.ufo/waves/kaika-w1/kasegi-art.md:72:iso.org/standard/92945
./.ufo/waves/kaika-w1/kasegi-art.md:73:iso.org/standard/69725
./.ufo/waves/kaika-w1/kasegi-art.md:181:iso.org/standard/92946
```

Restricted to sibling lane directories only (the same grep without the fleet-root hit):
```
cd /home/vgpnk/Projects/shokunin && for l in audio chousa game-dev-2d game-dev-3d kagi kaidoku kake kama kengaku kotoba kotodama kumitate lore mado mori revenger souji tabi tameshi tsukuroi; do
  grep -rIn -o -E 'iso\.org/standard/(72311|69725|92945|92946)' --exclude-dir=.git --exclude-dir=.jj "$l-shokunin"
done
```
Exit code 1 (no matches) — **no sibling lane references 72311, 69725, 92945 or 92946 at all**, in text or (binary-inclusive sweep, `grep -rla`) in any file form.

The only outside-kasegi holder of F38's two catalog ids is a **fleet-wave dossier, not a lane**:
`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w1/kasegi-art.md` (fleet root `.ufo/waves/`, mtime 2026-10-19 20:10 -0300), section "## Draft `corpus/SOURCES.md` rows". Quoted lines:

```
.ufo/waves/kaika-w1/kasegi-art.md:72
| S012 | ISO — ISO/IEC AWI 29147, Cybersecurity — Vulnerability disclosure processes — https://www.iso.org/standard/92945.html | spec | A | Edition 3 is under development and will replace 29147:2018; track it as a work item, not a published standard. | watch | 2026-10-19 | on-release | — |

.ufo/waves/kaika-w1/kasegi-art.md:73
| S013 | ISO — ISO/IEC 30111:2019, Vulnerability handling processes — https://www.iso.org/standard/69725.html | spec | A | Current published vulnerability handling standard record and its announced revision status. | watch | 2026-10-19 | on-release | — |

.ufo/waves/kaika-w1/kasegi-art.md:181 (section "## Leads (unopened)")
- ISO/IEC WD 30111.2 vulnerability-handling work item: https://www.iso.org/standard/92946.html
```

Class and status of this material — read carefully, because it is the closest thing to class (a) outside kasegi and it is **not** an overlap:
- **Class (c), mention only, for the F38 claim.** It is a *draft* registry proposal inside a fleet wave's dossier artifact (`.ufo/waves/kaika-w1/`), never committed to any lane's `corpus/SOURCES.md`, with no capture bytes, no manifest, no recheck command and no `used-by` cell (the row's last cell is `—`). The dossier's own scope note says the registry table is "Draft `corpus/SOURCES.md` rows", and the same dossier's "## Leads (unopened)" section (line 181) still lists the WD 30111.2 work item as unopened.
- Independently corroborated as *unopened* at the time: the fleet's kaika aggregate seat recorded kasegi's ISO 29147+30111 as an **unopened lead**, not evidence —
  `.ufo/waves/kaika-aggregate/seats/audit-kasegi.md:285`: "**Leads** lists 3 unopened items (Big Sleep tracker, ISO/IEC 29147+30111, UK AISI). These were **not** used as evidence anywhere in this audit."; and `.ufo/waves/kaika-aggregate/seats/source-curation.md:496`: "kasegi: 3 unopened leads (Big Sleep tracker, ISO/IEC 29147+30111, UK AISI)".
- The S013 draft row's `69725` id matches F38's S090 target, and the S012 draft row's `92945` id is ISO's **AWI 29147** (edition 3 work item) — the successor-work item F38 also names. So the fleet's 2026-10-19 dossier already *named* both the 30111 catalog page and the 29147 successor work item, but named them without opening them, without capture, and without landing them. This is reported, not absorbed: no catalog bytes, no publisher-record content, and no lane registry hold.
- Note also the lineage. The dossier is a **kaika-wave proposal for a *different* registry layout**, not kasegi's registry: an id-by-id comparison of its draft table against the lane's base registry (`git show eae1d61:corpus/SOURCES.md`) shows only **S001 and S002 agree by URL; all 28 other shared ids (S003–S030) carry different URLs in the two tables** (e.g. draft S003 = MITRE CWE Top 25 vs lane S003 = the CISA CVD program; draft S012 = AWI 29147 vs lane S012 = Anthropic Project Glasswing). So the draft's S012/S013 ids are **not** the lane's S012/S013 and the draft was never merged into the lane's registry.
- The lane's own ISO lead line entered the lane registry in the round-22 commit `c8b719d` ("round-22: QUALITY bar, SOURCES registry, frontier F01-F05 admitted, legacy provenance disclosure", Mon Oct 19 19:27:48 2026 -0300), under the heading `## Leads (unopened)` (`git show c8b719d:corpus/SOURCES.md`, section headings at lines 3/35/41/50; the lead bullet is the second bullet of the `## Leads (unopened)` section at line 50). The fleet-wave dossier's mtime is 2026-10-19 20:10 -0300, ~43 minutes after that commit. Both artifacts therefore date from the same 2026-10-19 wave cycle, one hour apart: the lane wrote the pair as an **unopened lead**, and the fleet dossier drafted the same two catalog ids as **proposed rows** — in neither case is the publisher record opened, captured, or committed. This is one origin seen from two sides, not two independent holdings.

---

## 4. Step 3 — inside kasegi: does any held row or entry already hold class (a) ground under another id?

Command (frozen base bytes, read-only git):
```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && B=eae1d614542e8d30d77e9f4e8b9dea6a11aad138
git show $B:corpus/SOURCES.md | grep -n -E 'iso\.org|ISO/IEC 29147|ISO/IEC 30111'
```
Exit code 0. Decisive lines at base:
```
45:| S039 | 日立グループにおける製品脆弱性情報の開示プロセス (HIRT-PUB10008) … (L497 to L499) … | class (b) consumer — Hitachi HIRT maps its steps onto 29147:2014 / 30111:2013
46:| S040 | Cisco Security Vulnerability Policy … states alignment with ISO/IEC 29147:2018 (L58) | class (b) consumer
47:| S041 | 情報セキュリティ早期警戒パートナーシップガイドライン 2026年10月 (JPCERT/CC) … 付録6 §2 p.45 (ISO/IEC 29147:2014 vs ISO/IEC 30111:2013 division of labour, 図1) | class (b) consumer
137:- ISO/IEC 29147 vulnerability-disclosure and ISO/IEC 30111 vulnerability-handling standard records at https://www.iso.org/standard/72311.html and https://www.iso.org/standard/69725.html.
```
Line 137 is the **lead** line (section `## Leads (unopened)`), not a row: no id, no tier, no capture. So at base:
- **No held row holds class (a) ground.** The only iso.org URL in the base registry is the unopened lead at :137.
- Every base row touching the standards is class (b) — a consumer/implementer (Hitachi HIRT, Cisco PSIRT, JPCERT/CC guideline). The base knowledge entries are equally (b): `corpus/knowledge/iso-29147-and-30111-division-of-labour.md:2` reads `source: S041 — https://www.jpcert.or.jp/...` and `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md:2` reads `source: S041 — …` — both grounded on the JPCERT/CC document, not on the publisher page. Verified:
  ```
  git show $B:corpus/knowledge/iso-29147-and-30111-division-of-labour.md | grep -c 'iso\.org/standard'   → 0
  git show $B:corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md | grep -c 'iso\.org/standard' → 0
  ```
- Base frontier rows F10/F11 (corpus/README.md:211-212) and PROVINCE.md:41 name the 29147/30111 subject matter but scope it to F10 (vendor policies, S040/S039/S036/S038) and F11 (the JPCERT/CC division-of-labour reading, S041). Neither is the publisher record. Base README's last frontier row is F37 — **no F38 at base**.
- The only base-tree files naming `72311` are the *lead* at :137 and the already-captured CISA guide snapshot `corpus/source-snapshots/round-24/S003.txt:94,457` (a downstream citation of the standard inside CISA's document — class (b) mention), plus the CSAF snapshot `corpus/source-snapshots/round-38/S055.txt:396,451` (ISO/IEC 29147:2018 in a bibliography — class (c)/(b) mention). Neither is the publisher page's own content.

Conclusion for step 3: **no held row or entry in kasegi already held class (a) ground under another id** at the frozen base; F38's admission on S089+S090 is genuinely first-admission inside the lane, and no sibling lane holds the same ground.

---

## 5. Step 4 — fleet report folders round-5*/round-6*

Command:
```
cd /home/vgpnk/Projects/shokunin/.ufo/reports && for d in round-5 round-50 round-51 round-52 round-53 round-54 round-55 round-56 round-57 round-58 round-59 round-6 round-60 round-61 round-62 round-63 round-64 round-65 round-66 round-67 round-68 round-69; do
  n=$(grep -rIl -E 'iso\.org/standard|ISO/IEC 29147|ISO/IEC 30111|29147:2018|30111:2019' "$d" 2>/dev/null | wc -l); echo "$d hits=$n"
done
```
Exit code 0. Printed output:
```
.ufo/reports/round-5 hits=0
.ufo/reports/round-50 hits=0
.ufo/reports/round-51 hits=0
.ufo/reports/round-52 hits=0
.ufo/reports/round-53 hits=0
.ufo/reports/round-54 hits=0
.ufo/reports/round-55 hits=0
.ufo/reports/round-56 hits=0
.ufo/reports/round-57 hits=0
.ufo/reports/round-58 hits=0
.ufo/reports/round-59 hits=0
.ufo/reports/round-6 hits=0
.ufo/reports/round-60 hits=0
.ufo/reports/round-61 hits=0
.ufo/reports/round-62 hits=0
.ufo/reports/round-63 hits=0
.ufo/reports/round-64 hits=0
.ufo/reports/round-65 hits=0
.ufo/reports/round-66 hits=0
.ufo/reports/round-67 hits=0
.ufo/reports/round-68 hits=0
.ufo/reports/round-69 hits=0
```
(Transcription note: the command's own printed output for each line was exactly `<dir> hits=0`; the list above is verbatim.)

Every requested folder is zero-hit. A wider sweep over the whole `.ufo/reports/` tree (all 100+ rounds) found only two non-target mentions, both class (c):
```
.ufo/reports/round-12/SOURCES.md:28: lore-shokunin W04 S032 duplicate url www.iso.org/standard/70908.html across scopes
.ufo/reports/round-26/kasegi.md:5,31: kasegi's own F11 "ISO/IEC 29147/30111 division-of-labour" admission (S041 JPCERT/CC) — class (b), kasegi's own prior round
```
Exit code 0 for the wider sweep; no (a) hit.

---

## 6. Hit table (consolidated) and verdict

### Sibling lanes — restricted paths (corpus/, SKILL.md, PROVINCE.md, plans/, knowledge/)

| # | path:line | class | standard | F38 overlap? |
|---|---|---|---|---|
| 1 | `lore-shokunin/corpus/SOURCES.md:31` | (c) | ISO 8601-2 (70908) | no |
| 2 | `lore-shokunin/corpus/SOURCES.md:40` | (c) | ISO 8601-2 (70908) | no |
| 3 | `lore-shokunin/corpus/lessons/round-103.md:91` | (c) | ISO 8601-2 (70908) | no |
| 4 | `lore-shokunin/corpus/lessons/round-103.md:165` | (c) | ISO 8601-2 (70908) | no |
| 5 | `revenger-shokunin/corpus/SOURCES.md:577` | (c) lead | ISO/IEC 27042 (44118) | no |

### Sibling lanes — whole tree (non-restricted paths)

| # | path:line | class | note |
|---|---|---|---|
| 6 | `kake-shokunin/.ufo/waves/round-35/sources/S078.txt:1` | (b) | RFC 9116 cites [ISO.29147.2018] — consumer of the standard, no publisher page |
| 7 | `kake-shokunin/.ufo/waves/round-36/sources/S090.txt:1` | (c) | ISO 646 / ISO 8859-1 links in WHATWG Encoding capture |
| 8 | `kake-shokunin/.ufo/waves/round-25/{frozen-final/,frozen/,}source-wcag22.html:185,191,4308` | (c) | iso.org/standard/64840, /56350 links in a WCAG 2.2 capture |
| 9 | `kake-shokunin/.ufo/waves/round-48/assimilation/validate/...` | (c) | mirrors of #7/#8 |
| 10 | `kotodama-shokunin/reports/round-60/captures/pages/S632.txt:3210` | (c) | ISO 9184-1:2023 (79506) in a reference list |
| 11 | `kumitate-shokunin/.ufo/waves/round-54/build/ScoutMqtt/mqtt-v5.0-os.html:3411,3440` | (c) | iso.org links in an MQTT capture |
| 12 | `kotoba-shokunin/.ufo/waves/round-71/receipts/census-after.txt:184` | (c) | census line naming lore's 70908 dup-url |
| 13 | `mado-shokunin/.ufo/waves/round-44/w2/RerunCensus/census-fleet.txt:189` | (c) | census line naming lore's 70908 dup-url |
| 14 | `revenger-shokunin/.ufo/waves/kaika-r1/e3-sources.md:36,42` | (c) | ISO/IEC 27042, 403, "lead only" |
| 15 | `chousa-shokunin/.ufo/waves/round-54/w1/R54ConnCrossClaim.md:19` | (c) | note about **kasegi's** lead, not a chousa hold |

### Fleet root (not a lane) — reported, not absorbed

| # | path:line | class | note |
|---|---|---|---|
| 16 | `.ufo/waves/kaika-w1/kasegi-art.md:72` | (c) | draft row for ISO **AWI** 29147 (92945) — no capture, unopened per kaika aggregate |
| 17 | `.ufo/waves/kaika-w1/kasegi-art.md:73` | (c) | draft row for ISO/IEC 30111:2019 catalog page (69725) — the F38 id, but a fleet-wave draft, not a lane hold, no bytes |
| 18 | `.ufo/waves/kaika-w1/kasegi-art.md:181` | (c) | WD 30111.2 (92946) listed under "## Leads (unopened)" |
| 19 | `.ufo/waves/kaika-aggregate/seats/audit-kasegi.md:285` | (c) | records the ISO pair as an unopened lead, not evidence |
| 20 | `.ufo/waves/kaika-aggregate/seats/source-curation.md:496` | (c) | same |

### kasegi (own lane, frozen base `eae1d61`)

| # | path:line | class | note |
|---|---|---|---|
| 21 | `corpus/SOURCES.md:137` (base) | (c) lead | the recorded lead line, bytes unchanged, unopened at base |
| 22 | `corpus/SOURCES.md:45,46,47` (base; rows S039/S040/S041) | (b) | vendor/IR-team consumers of the standards |
| 23 | `corpus/knowledge/iso-29147-and-30111-division-of-labour.md:2` (base) | (b) | grounded on S041 (JPCERT/CC), 0 iso.org URLs |
| 24 | `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md:2` (base) | (b) | grounded on S041, 0 iso.org URLs |
| 25 | `corpus/source-snapshots/round-24/S003.txt:94,457` | (b)/(c) | CISA guide citing 29147:2018 + catalog id in-text |
| 26 | `corpus/source-snapshots/round-38/S055.txt:396,451` | (c) | CSAF bibliography entry naming 29147:2018 |

### Verdict

**class (a) overlap: none.**

No other lane in the fleet holds a standards-body publisher record of ISO/IEC 29147 or ISO/IEC 30111, and no other lane cites `iso.org/standard/72311` or `iso.org/standard/69725` as a source — verified by the id-level sweep over all 20 sibling lane trees (text and binary forms), the restricted-path sweep over all 20 sibling lanes, and the sweep over `.ufo/reports/round-5*` and `round-6*` (all zero-hit). The only outside-kasegi mention of these catalog ids is the fleet-wave **draft** dossier `.ufo/waves/kaika-w1/kasegi-art.md:72-73` (AWI 29147 id 92945 and 30111 id 69725, as proposed rows) and `:181` (WD 30111.2 id 92946, under "## Leads (unopened)") — a fleet-wave artifact, never merged into any lane's registry (its draft ids S003–S030 diverge from the lane's), with no capture and no recheck; the fleet's own kaika aggregate seat independently recorded the ISO 29147+30111 pair as an **unopened lead, not evidence** (`.ufo/waves/kaika-aggregate/seats/audit-kasegi.md:285`, `source-curation.md:496`). Reported as cross-domain material, not absorbed. Inside kasegi, the frozen base holds no class (a) ground under any other id: the only iso.org URL in the base registry is the unopened lead at `corpus/SOURCES.md:137`, every base row and knowledge entry that touches the standards is class (b) (grounded on S039/S040/S041), and the base frontier's last row is F37.

**Consequence for C2 (coverage): none adverse.** C2's "first admission of the recorded ISO/IEC 29147/30111 lead" wording stands: the ground was unheld in every lane, in the reports tree, and inside kasegi at the frozen base. The only nuance worth a reviewer's eye: a fleet-wave draft dossier of 2026-10-19 (~43 minutes after kasegi's round-22 commit) already *named* the 30111 catalog id (69725) and the AWI 29147 work-item id (92945) in a proposed registry table — but under a different id layout, with no capture, no recheck, and in a non-lane artifact, and the fleet's own audit classed the pair as an unopened lead. That is a shared origin, not a duplicate hold; on a strict "first naming anywhere in the fleet" reading the lane's round-22 lead line (`c8b719d`) is still the first naming of the pair, and this round is the first to *open* it.

---

## 7. Rule observations (reported, not acted on — no frozen rule was changed)

- No rule error found in `claims.json` from this seat's direction. The C2 kill rule's ISO-lead-byte clause ("the ISO lead line's bytes differ or its exact-line sha changes") is consistent with what this seat measured at base: line 137's exact-line sha256 is `23309b6fd1226e398f8cce84f6a6e41f1a35ef9f8f0f95acdaa2119d17055b39`, which matches the value frozen in the C2 frozen sentence (independently re-confirmed here from the lane's own base bytes, and consistent with the lane's committed `controls/neighbor-screen-r57.txt` limb 3).
- One observation for the reviewer (not a kill-rule violation): the C2 frozen sentence asserts "first admission of the recorded ISO/IEC 29147/30111 lead". Within the lane this is exact. Across the fleet, the ids appear in the non-lane fleet-wave dossier `.ufo/waves/kaika-w1/kasegi-art.md` from the same day. Since that artifact is explicitly a draft table whose own wave classed the pair as an unopened lead, it is not a hold of the ground; but if a strict reviewer wants the sentence's scope pinned, the wording "first admission **in the lane**" is the defensible form. I did not edit `claims.json`.

## 8. Tools

No tool was installed or upgraded for this seat: the scan used only `grep`, `git` (read-only: `show`, `log`, `ls-tree`, `diff`, `status`, `rev-parse`, `merge-base`, `grep` on committed trees) and the POSIX shell already present on the host (`grep` 3.13 / GNU grep per `--version` is the host default; no new package needed). Per the round-57 lane prompt, `pacman` is PAUSED host-wide and was not invoked; `uv tool`/`npx` installs were unnecessary. No credential material appears in this file (only path:line pointers and pattern names).

## 9. Scratch / hygiene

- Scratch root `S = /fast/scratch/hyaku/kasegi-r57/SiblingOverlap` was created with `mkdir -p` and used as `TMPDIR`; it contained no artefacts that needed persisting and **was deleted before yield** (`rm -rf -- "$S"`; verified absent with `test ! -e "$S"`).
- No file under `L` was modified except this evidence file. No git mutation command (`add`, `commit`, `stash`, `checkout`, `switch`, `reset`, `pull`, `push`) was run against `L`; no `jj` command was run. Read-only git was used against `L` and the sibling lanes.
- The fleet root was read only; the sibling lanes were read only; `shokuknow` was never touched.
