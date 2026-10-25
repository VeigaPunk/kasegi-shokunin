# ScoutQuarantineSlice — kasegi quarantine slice (round 30 wave 1)

Role: UFO-FSD scout (leaf; no subagent dispatch). Task: extract the kasegi lane's
quarantine slice from the read-only absent-defect register, print the full row table,
mark truncated vs full locators, record the slice count. No fetching (ExecQuarantineFetch
does that).

## Inputs (bytes measured, sha256)

- Register `R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` — `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`
- Slice `A=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-30/assimilation/quarantine-slice` — `d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862`

## Extraction method

```
awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" > "$A/quarantine-slice"
```

All 7 extracted lines carry an S-id. The register has two row sections: (1) checked
rows with ABSENT quotes (class `payload-absent`, 194 rows total; kasegi per "By lane" =
2), and (2) rows whose quotes were NEVER CHECKED (109 rows total; 5 are kasegi). The awk
matches both sections because section 2's `id` cell still satisfies `S[0-9]+` (it is
rendered as `S048`` — trailing backtick glued to the id, no leading backtick).

## Slice count: **7** kasegi rows

| S-id | round | register section | class / why not checked | cited source (locator) | quote(s) / register cell text | locator status |
|---|---|---|---|---|---|---|
| S037 | round1 | ABSENT (checked) | `payload-absent` | `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A` | `信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01` | full |
| S054 | round3 | ABSENT (checked) | `payload-absent` | `https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf` | `脆弱性の悪用が確認されたもの又は疑われるもの` | full |
| S048 | round2 | NEVER CHECKED | the cited source could not be fetched, so no quote was checked | `https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3` | (no quote cell) | full |
| S065 | round4 | NEVER CHECKED | the cited source could not be fetched, so no quote was checked | `http://www.npc.gov.cn/c2597/c5854/c5855/202609/P020260904396146393500.pdf` | (no quote cell) | full |
| S068 | round4 | NEVER CHECKED | the cited source could not be fetched, so no quote was checked | `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` | (no quote cell) | full |
| S069 | round4 | NEVER CHECKED | the cited source could not be fetched, so no quote was checked | `https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F` | (no quote cell) | suspected truncated |
| S070 | round4 | NEVER CHECKED | the cited source could not be fetched, so no quote was checked | `https://std.samr.gov.cn/dcpspTools/gbPlan/download?path=%2Fzxd%2F2025005470%2F20_%E6%A0%87%E5%87%86%E8%B5%B7%E8%8D%89%2F` | (no quote cell) | suspected truncated |

## Locator truncation marks

- **Full locators (5/7):** S037, S054, S048, S065, S068 — cited-source cells end in a
  terminal path/query token (`.pdf`, `.html`, `?id=…`); no ellipsis/`…` in the cell.
- **Suspected truncated (2/7):** S069 and S070 — both rows carry the *identical* cited
  source ending in a URL-encoded terminal slash (`…%2F`, decodes to `path=/zxd/2025005470/20_标准起草/`).
  A `gbPlan/download` locator normally names a file after the directory; ending at a
  directory segment suggests the locator was cut when recorded. This is a flag for
  ExecQuarantineFetch: try the row as recorded first, then examine the same directory path
  for an actual filename (both rows point at the same directory).
- No kasegi row carries a truncated *quote* cell: S037 ends with full CJK stop `。`;
  S054 ends with `もの` (looks like a sentence fragment, but the cell itself shows no
  ellipsis marker — flagged here as an observation, not a truncation verdict). The five
  NEVER-CHECKED rows have no quote cells at all.

## Notes for downstream

- S037 and S054 are the only two **checked** ABSENT rows (the fabrication class — verify
  by hand via the cited sources listed).
- S048/S065/S068/S069/S070 are **never-checked** (unreachable), i.e. NOT fabrications and
  NOT confirmed; they need re-fetch, not editing.
- The register's "By lane" table counts only the ABSENT section (2 for kasegi); the full
  quarantine slice is 7 rows once the NEVER-CHECKED section is included.
- No tools were installed (standard `awk`, `mkdir`, `sha256sum`; no installs to record).
