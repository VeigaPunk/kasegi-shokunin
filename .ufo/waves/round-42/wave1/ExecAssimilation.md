# ExecAssimilation — round-42 wave-1 receipt

Seat: executor, leaf member (no subagent dispatch; no labrat probe needed).
Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` at HEAD `0566bd66e93d429b2df8b6751cf10cbdc391e79b`
(read-only this seat; `git status --porcelain -- corpus/SOURCES.md` → empty, i.e. the registry is
tracked and unmodified). Base commit for this round `5053a7f46de35784cff4b56756906e9014a38276`;
the lane HEAD above is the pre-wave-1 tip.
Scratch: `/fast/scratch/hyaku/kasegi-r42/ExecAssimilation` (created with `mkdir -p`, removed before
this yield; all paths absolute).

## 0. Deliverable

| file | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-42/wave1/ExecAssimilation.txt` | 90 | 7138 | `a123ca31afc0355936344f48a1c192e0926af08606f75d221e1a29ae74644c20` |

One heading (`## Assimilation: none adopted`), no fences, no validation table, no placeholder tokens
(`grep -nE '⟨pending|<r[0-9]|<fill>|TBD|TODO|FIXME|XXX|placeholder|\.\.\.$'` → no output). The body
is the landable text; all validation evidence lives in this receipt.

## 1. §10 id-collision check — the canonical commands, run in scratch

`A=$S/assimilation`, `S` = the seat scratch dir. Never wrote to shokuknow.

```
$ A=$S/assimilation; mkdir -p "$A"
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md \
    | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md \
    | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
$ comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"

reg-ids    lines = 63   unique=63   range=S001..S063
staged-ids lines = 94   unique=94   range=S031..S124
collisions lines = 33
collisions = S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060 S061 S062 S063
```

**Reported counts (the item's three asked-for numbers):** lane registry **63** ids, staged package
**94** ids, **33** collisions.

Artifact digests (reproducible from the two public inputs):

```
10deac7a4a52fa2d1a84daf7d8ad840930228488e6eea9fe67e5cfb3928a72e8  $A/reg-ids
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  $A/staged-ids
c60db3a338b2e8a36c524466ab5072be189d8597371954bd97d832b5592b6e43  $A/collisions
```

Input digests:

```
baf2f44a0c8a9e8fe37404797856fa5634e10b5e7ea113c4fde7d625a970a547  kasegi-shokunin/corpus/SOURCES.md
4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb  shokuknow/merge/kasegi/SOURCES.append.md   (100 lines, 89718 B, mtime 2026-10-24 23:33:20.041997004 -0300)
5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833  shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (375 lines, 83621 B)
```

The staged file's digest and mtime are **byte-identical** to the package state measured at rounds
34/35/38 (`4fe049cb…73eb`, mtime `2026-10-24 23:33:20`), so the package has not changed since. The
`staged-ids` digest `550a0129…f8019f` is likewise byte-identical to the round-38 artifact
`wave1/ExecIdCollision.staged-ids`. Only `reg-ids` moved: 54 rows at round 38 → 63 rows now.

### 1a. Head-relativity (the count C2 will change)

```
$ cp "$A/reg-ids" "$A/reg-ids-sim"; echo S064 >> "$A/reg-ids-sim"; LC_ALL=C sort -o "$A/reg-ids-sim" "$A/reg-ids-sim"
$ comm -12 "$A/reg-ids-sim" "$A/staged-ids" | wc -l        -> 34
$ grep -c '^S064$' "$A/collisions-sim"                      -> 1
$ grep -cE '^ {0,3}\|[[:space:]]*S064[[:space:]]*\|' corpus/SOURCES.md -> 0   (lane S064 free for C2)
```

33 is the registry-63 reading; after C2 lands `S064` the figure is **34**. The lesson must state the
registry size it read, never the figure alone.

### 1b. The drift is mass, not scattered

```
lane ids   : S001 .. S063 count=63 contiguous=True
staged ids : S031 .. S124 count=94 contiguous=True
collisions contiguous: True  range S031 .. S063  count 33
package built against a registry ending at: S031 -> lane has since grown to S063 = 33 extra rows
```

`shokuknow/merge/kasegi/MERGE-REPORT.md:9` states the package was staged against a lane registry
holding "**30** rows" with "first staged id is **S031**". The lane has since grown by 33 rows, so
the *entire* staged id space from `S031` up is offset. The §10 clause covers this shape explicitly:
"Drift a read-only check cannot fix (mass id drift, reshuffled register) → append an L0 question and
adopt nothing this round."

### 1c. Id collisions are not document collisions

Per colliding id, the first URL of the lane row's `source` cell against the package row's:

| id | same or different | lane URL | package URL |
|---|---|---|---|
| S031 | DIFFERENT | cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf | hackerone.com/security/policy_versions |
| S032 | DIFFERENT | nvlpubs.nist.gov/…/nistspecialpublication800-115.pdf | raw.githubusercontent.com/bugcrowd/…/README.md |
| S033 | DIFFERENT | laws.e-gov.go.jp/api/1/lawdata/411AC0000000128 | raw.githubusercontent.com/bugcrowd/…/cwe.json |
| S034 | DIFFERENT | soumu.go.jp/…/cybersecurity/kokumin/basic/legal/09/ | zc.cnvd.org.cn/news/helpList |
| S035 | DIFFERENT | npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf | security.360.cn/Reward/rules |
| S036 | DIFFERENT | cybozu.co.jp/company/security-policy/ | security.bilibili.com/static/docs/BILISRC_V1.7.pdf |
| S037 | DIFFERENT | cybozu.co.jp/products/bug-bounty/faq/ | openstd.samr.gov.cn/…?hcno=458BACCE700CA8E0B728CFB5F762DE7A |
| S038 | DIFFERENT | pepabo.com/contact/vulnerability-reporting/ | std.samr.gov.cn/gb/…B4C25880C3E01CB3E05397BE0A0A92D0 |
| S039 | DIFFERENT | hitachi.co.jp/hirt/publications/hirt-pub10008/ | laws.e-gov.go.jp/api/1/lawdata/411AC0000000128 |
| S040 | DIFFERENT | cisco.com/c/en/us/about/security-center/… | soumu.go.jp/…/cybersecurity/kokumin/basic/legal/09/ |
| S041 | DIFFERENT | jpcert.or.jp/vh/partnership_guideline2026.pdf | npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf |
| **S042** | **same-url** | **ipa.go.jp/security/todokede/vuln/process.html** | **ipa.go.jp/security/todokede/vuln/process.html** |
| S043 | DIFFERENT | hackerone.com/security/policy_versions | jpcert.or.jp/vh/partnership_guideline2026.pdf |
| S044 | DIFFERENT | raw.githubusercontent.com/bugcrowd/…/README.md | court.gov.cn/fabu/xiangqing/3085.html |
| S045 | DIFFERENT | raw.githubusercontent.com/bugcrowd/…/cwe.json | czt.ln.gov.cn/czt/attachDir/2026/05/2026050715041524122.pdf |
| S046 | DIFFERENT | ipa.go.jp/security/reports/vuln/jvn/…ug65p90000019ev2-att/…pdf | nj.jsjc.gov.cn/jianwu/zhinan/202109/t20210917_238200.shtml |
| S047 | DIFFERENT | ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html | sse.com.cn/lawandrules/…/028395e1b8364d3bb3fcb28d565de306.pdf |
| S048 | DIFFERENT | microsoft.com/en-us/msrc/msvr | std.samr.gov.cn/gb/…3B865A9398AA6160E06397BE0A0A52F3 |
| S049 | DIFFERENT | zc.cnvd.org.cn/news/helpList | ipa.go.jp/security/reports/vuln/jvn/…ug65p90000019ev2-att/…pdf |
| S050 | DIFFERENT | security.360.cn/Reward/rules | ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html |
| S051 | DIFFERENT | immunefi.com/…vulnerability-severity-classification-system-v2-2/ | gongbao.court.gov.cn/Details/96fea4e0b9e00def2295a1e598666d |
| S052 | DIFFERENT | cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | cnnvd.org.cn/group1/M00/03/2c/rBBl8WrPKoaAKy_IAAT1JLp2GFY923.pdf |
| S053 | DIFFERENT | first.org/epss/ | meti.go.jp/policy/netsecurity/vul_notification.pdf |
| S054 | DIFFERENT | certcc.github.io/SSVC/tutorials/ssvc_overview/ | ipa.go.jp/security/guide/vuln/…request_to_ipa.pdf |
| S055 | DIFFERENT | docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0-os.html | cybozu.co.jp/company/security-policy/ |
| S056 | DIFFERENT | cisa.gov/resources-tools/…/minimum-requirements-vulnerability-exploitability-exchange-vex | cybozu.co.jp/products/bug-bounty/faq/ |
| S057 | DIFFERENT | cisa.gov/resources-tools/…/when-issue-vex-information | pepabo.com/contact/vulnerability-reporting/ |
| S058 | DIFFERENT | github.com/openvex/spec/blob/main/OPENVEX-SPEC.md | ipa.go.jp/security/todokede/vuln/uketsuke.html |
| S059 | DIFFERENT | cyclonedx.org/docs/1.7/json/ | phic.org.cn/wsxxh/wzaqgl/202609/P020260909380470895113.pdf |
| S060 | DIFFERENT | cyclonedx.org/docs/1.7/json/ | hitachi.co.jp/hirt/publications/hirt-pub10008/ |
| S061 | DIFFERENT | cisa.gov/sites/default/files/publications/VEX_Status_Justification_Jun22.pdf | court.gov.cn/fabu/xiangqing/283891.html |
| S062 | DIFFERENT | docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html | court.gov.cn/zixun/xiangqing/449641.html |
| S063 | DIFFERENT | rfc-editor.org/rfc/rfc9116.txt | gongbao.court.gov.cn/Details/4aa50f7ee90ae17896de6699f8fbf3.html |

**32 different, 1 same (`S042`).** A registered number is not a registered document.

### 1d. The id C2 needs is already taken in the package

```
package S064  情報セキュリティ早期警戒パートナーシップガイドライン 2026年10月（付録6 国際標準に準拠するための留意点）
              https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf
lane already holds that URL as: S041
lane rows with S064: 0   (S064 is free for C2's own new row)
```

Staged `S064` must not be renumbered into `S064`. The same URL is staged **three** times
(`S043`, `S064`, `S076`), so a package append lands three rows on one URL.

### 1e. URL-level overlap, lane vs package

```
lane distinct urls  = 60   (63 rows)
pkg  distinct urls  = 76   (81 rows with a URL; 13 staged rows carry no URL)
url overlap         = 19
```

The 21 staged rows carrying an already-held lane URL (`S031 S032 S033 S034 S035 S039 S040 S041 S042
S043 S049 S050 S055 S056 S057 S060 S064 S068 S076 S080 S123`) — of these, **5** sit in the
collision-free band and would be duplicate-by-document on append: `S064`/`S076` (→ lane `S041`),
`S068` (→ lane `S040`), `S080` (→ lane `S048`), `S123` (→ lane `S032`).

13 staged rows have **no URL** in their `source` cell at all (`S072 S109 S110 S112 S113 S114 S115
S116 S117 S118 S120 S121 S122`) — they cite the campaign's own lane artifacts under
`shokuknow/lanes/kasegi/roundNN/evidence/*.txt`, i.e. route knowledge the lane already earned, not
a reopenable primary.

## 2. Guard proof — the item's required check

### 2a. Literal fixture (`  | S002 |` row a staged id collides with)

Scratch fixture `$A/fixture/fixture-SOURCES.md` (row 4 indented by two spaces) against
`$A/fixture/fixture-staged.md` (same id at column 0):

```
$ grep -nE '^ *\|' "$F/fixture-SOURCES.md"
1:| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
2:|---|---|---|---|---|---|---|---|---|---|---|
3:| S001 | Fixture Document Alpha — https://example.invalid/alpha | docs | A | fixture | fixture | fixture | mined | 2026-10-28 | 180d | — |
4:  | S002 | Fixture Document Beta, staged — https://example.invalid/beta | docs | A | fixture | fixture | fixture | mined | 2026-10-28 | 180d | — |

$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' fixture-SOURCES.md | grep -oE 'S[0-9]+' | sort > a-reg-ids
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' fixture-staged.md  | grep -oE 'S[0-9]+' | sort > a-staged-ids
$ comm -12 a-reg-ids a-staged-ids > a-collisions
A: reg=2 staged=2 collisions=1 -> [S002 ]
```

Control — the column-zero-only pattern on the **same bytes**:

```
$ grep -oE '^\|[[:space:]]*S[0-9]{3,}' fixture-SOURCES.md | grep -oE 'S[0-9]+' | sort > b-reg-ids
$ comm -12 b-reg-ids b-staged-ids > b-collisions
B (column-zero-only): reg=1 collisions=0 -> []
```

**Guard proof A: PASS.** The 0–3-space pattern detects the indented collision (`S002` present); the
column-zero-only pattern misses it, so it is not an acceptable guard.

### 2b. Same proof against the **real** inputs

A scratch copy of the live lane registry with the real `| S031 |` row indented by two spaces
(`S031` is a staged id), collided against the real staged set:

```
37:  | S031 | CVE Numbering Authority Operational Rules v4.2.6 — https://www.cve.org/Resources/Roles/Cnas/CN...
0-3-space: reg=63 collisions=33 S031-present=1
col0-only : reg=62 collisions=32 S031-present=0
```

**Guard proof B: PASS.** The real `S031` is found by the 0–3-space pattern and missed by the
column-zero-only pattern. The guard is not broken.

### 2c. Indent boundary sweep

```
indent=1sp  collisions=1
indent=2sp  collisions=1
indent=3sp  collisions=1
indent=4sp  collisions=0
indent=5sp  collisions=0
```

The 0–3-space tolerance is load-bearing; 4+ leading spaces (Markdown indented-code territory) is the
guard's blind spot.

### 2d. Latent-risk check on the real inputs (are they flat today?)

```
indented(1-3sp) rows in package: 0
indented(1-3sp) rows in lane   : 0
4+-sp indented rows in package  : 0
4+-sp indented rows in lane     : 0
```

Both real inputs carry **zero** indented `S`-rows, so the 33 count is unaffected today and the
guard is a latent-risk guard, not an active one.

### 2e. The §10 premise — an indented row is still census-valid

`--file` mode outside the lane tree reports `E11 missing used-by` for every row, but that is a
**path artifact of `--file` mode** (used-by targets resolve relative to the lane dir), not an
indentation effect. Proven by a same-directory control and by `--root` mode on a scratch lane
mirror:

```
# same-dir control: identical finding sets for the unmodified copy and the indented copy
EXIT(unmodified copy)=1 ; EXIT(indented)=1
diff <(sed s#$F/unmodified-copy-SOURCES.md#X# census-unmod-copy.txt) \
     <(sed s#$F/real-indented-SOURCES.md#X# census-indented.txt)   -> IDENTICAL
E03+E04 count in indented findings: 0

# --root mode, full lane mirror, lane dir passed by path
EXIT(mirror plain)=0
kasegi-shokunin  W04  S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi-shokunin  W04  S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi-shokunin  ok   …/mirror/kasegi-shokunin/corpus/SOURCES.md
EXIT(mirror indented)=0
kasegi-shokunin  W04  S028 …
kasegi-shokunin  W04  S029 …
kasegi-shokunin  ok   …/mirror/kasegi-shokunin/corpus/SOURCES.md
diff plain vs indented -> IDENTICAL
```

**The indented `S031` row changes no census verdict** — the §10 premise ("the census parser accepts
rows with 0–3 leading spaces, so the extractor must too") holds on real bytes.

## 3. Adoption gate — the §10 "no staged row is appended as-is" clause, measured

Scratch mirror of the lane corpus; the package's **collision-free** rows `S064`–`S124` (61 rows,
extracted verbatim) appended after the lane's `S063` row; gated with the fleet census:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root "$W" "$W/kasegi-shokunin"
EXIT=1
findings by code:  60 E11   43 E09   9 W04   3 W01   1 E01
E-class total: 104   W-class total: 12
E03 (duplicate id): 0   E04 (duplicate URL+scope): 0
```

**Not one of the 61 rows is clean as staged** (per-row codes: `rows with NO census finding: 0`).

Root causes, each located:

- **`E11` (60 rows) — dangling `used-by`.** The staged rows name 50 distinct `used-by` targets; **49
  of the 50 do not exist** in the lane corpus (only `corpus/knowledge/authorised-testing-rules-of-engagement.md`
  is present). Example: staged `S064`'s `used-by` is
  `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk-2026-10-23.md` — the lane holds
  `…/iso-29147-divergence-and-clause-crosswalk.md` (no date suffix), so the pointer dangles.
- **`E09` (43 rows) — prose `recheck` cells.** e.g. `S081 recheck=90d — re-open the 公告 page and
  confirm "您不得因为漏洞信息私自联系厂商" still present (ran 2026-10-24)` — not a valid ISO date, `NNd`
  or symbolic cadence. Affects `S081`–`S119`, `S121`, `S122`, `S123`, `S124`.
- **`E01` (1 row) — malformed row.** `S120 fields=12`: the row's `scope` cell contains a
  backslash-escaped pipe `\|` (`…/view/content-sd.html?id=…&lib=ck\|zdx`), so it splits into 12
  columns instead of 11. It is the only escaped-pipe row in the whole package
  (`grep -c '\\|'` → 1).
- **`W04` (9) — duplicate URL across scopes**, five of them against documents the lane already
  holds under other ids: `S064`, `S076` (jpcert → lane `S041`), `S068` (cisco → lane `S040`), `S080`
  (microsoft → lane `S048`), `S123` (nist 800-115 → lane `S032`).
- **`W01` (3) — tier-C `mined`**: `S098`, `S100`, `S102`.

## 4. Standing refusals — 0 of 7 flips met

`corpus/lessons/round-35.md:155-169` lists seven staged entries with a flip condition each. Each
re-measured against the byte-identical package:

| staged entry | flip condition | measured at HEAD S063 | met? |
|---|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` | located quote + executable recheck + non-colliding frontier id | `ground: F09` collides with admitted lane F09 (`grep -cE '^\| F09 \|'` → 1); 0 located quotes; 0 `cd`-prefixed `recheck:` | NO |
| `claim-packaging-and-report-quality.md` | an S036 row + capture for BILISRC V1.7 | `BILISRC` in lane SOURCES → 0; lane `S036` is `cybozu.co.jp/company/security-policy/` (a different document) | NO |
| `cn-crowdsourced-testing-roles-and-conduct.md` | entry shape + S081/S082 rows | lane rows with `S081`/`S082` → 0 | NO |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | S077/S078/S079 rows + real frontier id | lane rows with `S077`/`S078`/`S079` → 0 | NO |
| `chinese-criminal-thresholds-and-authorisation.md` | three rows + a renumber map | cites `S044`/`S045`/`S046`; all three are lane rows but name **different** documents; no renumber map exists | NO |
| `chinese-program-severity-instrument.md` | the row + a locatable anchor | `sse.com.cn` in lane SOURCES → 0; `newsType_6` in any lane capture → 0 | NO |
| `program-severity-ladders-and-reward-scales.md` | byte-identity or a supersedes row | lane `6c05c98f3c6851b560098b8f7c43350a951e487e8b34e2ff09831563aa8ff4a6` vs staged `35de5f8b19ed3b20beb3d41c347f4727d9fd2eefc8a23e53c64c6987b60bbc87` → different | NO |

## 5. Quarantine slice (read-only register)

```
$ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
$ awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R"
 S037   `payload-absent`
 S054   `payload-absent`
 S048`   the cited source could not be fetched, so no quote was checked
 S065`   the cited source could not be fetched, so no quote was checked
 S068`   the cited source could not be fetched, so no quote was checked
 S069`   the cited source could not be fetched, so no quote was checked
 S070`   the cited source could not be fetched, so no quote was checked
```

7 rows. Byte-identical to the round-37 stored slice:
`cmp "$A/quarantine-slice" .ufo/waves/round-37/assimilation/quarantine-slice` → identical, both
`sha256 d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862`. Every row stays
quarantined; none is hand-checked present-and-adoptable as quoted this round. (The register's own
cells carry a stray trailing backtick on `S048`/`S065`/`S068`/`S069`/`S070` — a register-side quirk,
not a lane defect; the register was not edited.)

## 6. Entry-level binding — the package's 67 knowledge entries

Per staged entry, the ids on its `source:` lines, checked against the live lane registry, then the
lane row's URL against the package row's URL for the same id:

```
entries with >=1 source line                                    = 67
entries whose every source id is registered in the lane          = 17
total unregistered id citations across the 67 entries            = 62
ids comparable on both sides (both carry a URL)                  = 47
  same-document                                                 = 1   (S042, in japanese-domestic-disclosure-workflow.md)
  different-document                                             = 46
entries with >=1 same-document citation                         = 1
```

The single same-document case is `japanese-domestic-disclosure-workflow.md`, whose `S042` is the
lane's own IPA process page. It still fails on the other counts: its `S043` is `jpcert.or.jp/vh/…`
while lane `S043` is HackerOne; its bytes differ from the same-name lane entry
(`a22d2321e39fd0e547d8ae480eb566648520e59281e69e057aab5ab8502413a6` lane vs
`ee667c2f5d9d24da99eeed903c613a79c12912d83af3d4952f8e7a36458372ec` staged); it references no lane
capture; its `recheck:` is prose plus a backticked `curl`, not a `cd`-prefixed executable line. The
lane already holds this ground as frontier **F12** (`corpus/README.md:213`,
`knowledge/japanese-domestic-disclosure-workflow.md`, sources `S041, S042`), so re-admitting the
staged copy would be a same-name divergent overwrite, not coverage gain.

## 7. Verdict — can the lane adopt anything this round?

**No. Nothing is adopted, and nothing should be.**

Four independent, measured reasons, each sufficient on its own:

1. **Mass id drift.** The collision band is contiguous `S031`–`S063` (33 ids) because the package
   was staged against a 30-row registry and the lane has since grown by 33 rows. §10 routes this
   shape to "append an L0 question and adopt nothing this round".
2. **No staged row is appendable as-is.** The 61 collision-free rows produce **104 E-class census
   findings** (60 E11, 43 E09, 1 E01) and **zero** clean rows. Fixing them means rewriting every
   row's `recheck` and `used-by` cell and re-opening every cited source — the whole §10
   transformation, per row, for a package whose entries all fail admission anyway.
3. **No entry passes admission.** 0 of 7 standing refusal flips are met; of the 47 comparable
   citations only **1** names the same document, and that entry is already held as F12 with
   divergent bytes.
4. **No quarantine row is adoptable.** 7 rows, 2 payload-absent, 5 unreachable-as-cited, none
   hand-checked present-and-adoptable.

Round-42's own claims do not need the package: C1 is the closure suite and C2 mines a fresh
frontier topic (F25) from outside the package. The package's staged `S064` collides with the id C2
needs, so adopting it would have forced a renumber of the very row this round is opening — the
"one id shifted by one repairs one citation and breaks the next" trap the fleet lesson names.

## 8. Bounds, tooling, scratch

- **Writes:** only `.ufo/waves/round-42/wave1/ExecAssimilation.txt` (the deliverable) and
  `.ufo/waves/round-42/wave1/ExecAssimilation.md` (this receipt), both under the lane repo's
  round-42 wave-1 dir, plus the seat scratch dir. No tracked lane file touched — verified
  `git -C <lane> status --porcelain -- corpus/SOURCES.md` → empty. No fleet-root file written. No
  file written under `/home/vgpnk/Projects/shokuknow`; no campaign tool run there
  (`renumber-staged.py`, `merge-plan.py`, `quote-lint.py`, `absent-defect-register.py` were read
  about, never executed). The lane's pre-existing untracked `.ufo/waves/round-42/kasegi-r42-build.ready{,.dispatched}`
  were left untouched.
- **No mutating git/jj command** anywhere: only `rev-parse`, `status --porcelain`, and read-only
  reads of committed bytes. No fixture git repo was created (the guard proof uses plain files, so
  the `git rev-parse --show-toplevel` assertion was not applicable).
- **Network:** no fetches this round — the package bytes are unchanged since the round-37/38 probes
  (`SOURCES.append.md` `4fe049cb…73eb`, mtime `2026-10-24 23:33:20`) and the register is unchanged
  (`5afe1810…d833`), so the round-37/38 quarantine verdicts carry over unchanged. No HTTP status,
  byte count or fetch time to record because no request was made.
- **Scratch:** `S=/fast/scratch/hyaku/kasegi-r42/ExecAssimilation`, created with `mkdir -p`; every
  work copy, mirror and fixture bound under it (`$A`, `$S/work2`, `$S/work`, `$A/fixture`); no
  reliance on an inherited `TMPDIR`; `/tmp` unused. The scratch dir is removed before this yield.
  *Note:* a sibling seat's cleanup pass deleted `$S/fixture` and `$S/mirror` once mid-run; every
  affected measurement was re-run from scratch and is reported above in its final form.
- **Tools:** none installed or upgraded — `grep`, `comm`, `sort`, `awk`, `sed`, `sha256sum`,
  `wc`, `diff`, `python3` (stdlib only) and the fleet's own `scripts/sources-census.sh` were
  sufficient. No `pacman`, no `uv tool install`, no binary written to any PATH directory.
- **Disk guard:** `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → exit 0
  (`/tmp` 5 % / 122.2 G free, `/var/tmp` 36 % / 576.1 G free, `/fast/scratch/hyaku` 27 % / 592.6 G
  free) before the passes; the work here is text-only and created no large trees.

## 9. What the L1 should carry into the report

- The three asked-for numbers: **lane ids 63, staged ids 94, collisions 33** — stated with the
  registry size, and with the head-relative **34** after C2 lands `S064`.
- The guard proof, twice: the literal `  | S002 |` fixture **and** the real `S031` row against the
  real staged set, plus the column-zero-only control that misses both, plus the census premise
  shown in `--root` mode.
- **Assimilation: none adopted**, with the §10 clause cited for the mass-drift route
  (L0 question, no adoption) and the census-gate and flip-condition evidence for the rest.
- One item for the L1 to weigh: the package stages `S064` for a document the lane already holds as
  `S041`, and `S064` is the id C2 opens this round. Any future adoption of package rows must
  renumber **by document**, never by arithmetic, and must start above `S064`.
