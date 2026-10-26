## Assimilation: none adopted

Id-collision rerun (this seat, read-only, the guard's own 0–3-space extractor
`grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` applied to both sides, ids intersected with
`comm -12`): lane `corpus/SOURCES.md` at HEAD `70015359` — the same blob as base `a173b0c2` —
holds **54** rows and **54** ids, unique, `S001`–`S054`; staged
`shokuknow/merge/kasegi/SOURCES.append.md` (`sha256 4fe049cb…73eb`, 100 lines, 89,718 B, mtime
`2026-10-24 23:33:20 −03:00`) holds **94** ids, unique, `S031`–`S124`. `comm -12` → **24**
collisions: `S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046
S047 S048 S049 S050 S051 S052 S053 S054`. Artifact digests: `reg-ids`
`ea4dfaaa459dcb0ba8a648a11896a166a101b39a970b667cae02fc867c385047`, `staged-ids`
`550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f`, `collisions`
`3f3799a4d918288c122c7c0c062b7d1aa4ee6acb44a412637a1540309d64c492` — byte-equal to
`wave1/ExecIdCollision.{reg-ids,staged-ids,collisions}`, re-derived independently by this seat.

Three facts keep the number honest:

- **It is head-relative.** 24 is the registry-54 reading. C2 lands `S055` after this measurement;
  adding `S055` to the lane id list and re-running `comm -12` against the unchanged staged list
  prints **25** (`S031`–`S055`), so the lesson must state the registry size it read, never the
  figure alone.
- **Id collisions are not document collisions.** Of the 34 cited ids that are also lane rows and
  carry a URL, exactly **1** names the same host as its lane row (staged `S042` =
  `https://www.ipa.go.jp/security/todokede/vuln/process.html` = lane `S042`); **33** name a
  different host (staged `S047` = `sse.com.cn` vs lane `S047` = `ipa.go.jp`; staged `S048` =
  `std.samr.gov.cn` vs lane `S048` = `microsoft.com`; staged `S053` = `meti.go.jp` vs lane
  `S053` = `first.org`). A registered number is not a registered document.
- **The incoming row is already taken twice over.** Staged `S055` is the Cybozu
  vulnerability-handling policy (`cybozu.co.jp/company/security-policy/`), which is lane `S036`'s
  document under a second number, and `S055` is the id C2 needs for CSAF. It must not be
  renumbered into `S055`.

Guard proof (`wave1/ExecIdCollision.md` §1 holds the same fixture; re-run here): on
`| S001 | x |` + `  | S002 | y |` against `| S002 | y |`, extractor A reports
`collisions=[S002] count=1`, while the column-zero-only pattern `grep -oE '^\|…'` reports
`count=0` on the same bytes. An indent sweep (`1`–`5` leading spaces on one `S099` row) matches at
1, 2 and 3 and misses at 4 and 5 — the 0–3-space tolerance is load-bearing and 4+ spaces is the
guard's blind spot. Neither real input carries an `S`-row indented four or more spaces, so the
count above is unaffected.

Quarantine slice: the read-only register
`shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (`sha256
5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 375 lines, 83,621 B) yields
7 kasegi rows under the frozen awk
`awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'`
(lines 99, 100, 322–326) — 7 lines, 417 B, `sha256
d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862`, `cmp`-identical to
`.ufo/waves/round-37/assimilation/quarantine-slice`. **0 adopted.** Three rows were re-measured
live this round (UA `kasegi-shokunin/1.0`, 2026-10-26T18:32:3xZ); four are carried from round 37
on a byte-identical register and an unchanged package:

| id (staged) | register class | verdict | basis |
|---|---|---|---|
| S037 | `payload-absent` | present-and-located, quote defective (stitched) | `openstd.samr.gov.cn` 200, 24,131 B at 18:32:45Z; the contiguous register quote occurs **0** times in the tag-stripped, whitespace-collapsed page, while `标准状态：现行`, `2020-11-19`, `2021-06-01` and `网络安全漏洞分类分级指南` each occur **1** time — the quote splices separate fields |
| S054 | `payload-absent` | present-and-located, quote defective (elided) | IPA request PDF 200, 513,648 B at 18:32:36Z (`pdftotext`); live text reads `（ア）脆弱性（（法第42条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの`, so the contiguous register quote occurs **0** times and the embedded parenthetical is dropped from it |
| S048 | unreachable | unreachable as cited | `std.samr.gov.cn/gb/search/gbDetailed?id=3B865A…` 404, 748 B, `sha256 95cd25d8…` at 18:32:35Z — byte-identical to the r36/r37 probe |
| S065, S068, S069, S070 | unreachable | present-and-located (carried, round 37) | not re-fetched this round; r37 located each quote (NPC catalogue PDF p. break; Cisco hop to `sec.cloudapps.cisco.com`; draft standard §6.3.2 p.25; drafting note 1.2 p.1) and register + package are byte-stable |

The measured slice is **0 fabrication-class, 1 unreachable (S048), 6 present-and-located** — the
register's class column is a candidate list, not a verdict. The quarantine ids are package ids:
quarantine `S054` is the IPA request PDF, not the round-37 SSVC source, and quarantine `S037` is
the GB/T 30279-2020 catalogue record while lane `S037` is the Cybozu bounty FAQ.

Standing refusals — the two flips the round-37 verifier sampled re-measured, still unmet:
`program-severity-ladders-and-reward-scales.md` is `6c05c98f3c6851b560098b8f7c43350a951e487e8b34e2ff09831563aa8ff4a6`
(67 lines) in the lane against `35de5f8b19ed3b20beb3d41c347f4727d9fd2eefc8a23e53c64c6987b60bbc87`
(50 lines) staged, so there is no byte-identity and no supersedes row;
`grep -c newsType_6 corpus/source-snapshots/round-32/S049.txt` → **0** (`newsType_21` → 1), so the
`chinese-program-severity-instrument.md` anchor is still absent; `grep -c sse.com.cn
corpus/SOURCES.md` → **0**, so `S047` is still unregistered. The package is byte-identical to
rounds 35–37 (70 files, every mtime `2026-10-24 23:33:20`, `SOURCES.append.md 4fe049cb…`), so all
seven reasons in `corpus/lessons/round-35.md:155-169` stand and **0 of 7 flip conditions is met**.

Assimilation set — the package's 67 `knowledge/` entries against the lane's 49, measured against
`corpus/QUALITY.md` Q1–Q10:

- **4 shared basenames, all divergent bytes** — `authorised-testing-rules-of-engagement.md`
  (`5533fc87…` vs `bf40409e…`), `japanese-domestic-disclosure-workflow.md` (`a22d2321…` vs
  `ee667c2f…`), `japanese-severity-vocabulary-and-impact-model.md` (`f584f06c…` vs `d7fdd31f…`)
  and `program-severity-ladders-and-reward-scales.md` (above): copying any of them overwrites lane
  text, so each is **rejected as an overwrite hazard**, not a flip.
- **Registration and binding:** 67 of 67 carry a `source:` line; **12** cite only ids that exist in
  the lane registry, **52** cite zero registered ids, **3** are mixed
  (`authorization-safe-harbor-and-scope-2026-10-23-amendment.md`,
  `chinese-criminal-case-law-2026-10-23.md`, `chinese-national-grading-applied-2026-10-23.md`), so
  **55 of 67** cite at least one unregistered id (Q1/Q2 red). **0 of 67** reference a lane capture
  under `corpus/source-snapshots/` (Q9 unbound), **0 of 67** carry a `cd`-prefixed executable
  `recheck:` line (Q10 red), and **11 of 67** carry no quoted sentence at all (Q3 red).
- **`ground:` collides with live lane ids:** 27 of 67 write a `ground: F##` that is also an
  admitted lane frontier id but means something else — e.g. `program-scope-rules-and-asset-boundaries.md`
  says `ground: F09 (new frontier item; extends F03…)` while lane F09 is *authorisation outside the
  platform*, and `japanese-domestic-disclosure-workflow.md` says `ground: F13 (new frontier item…)`
  while lane F13 is *program severity ladders*.
- **Admit: none.** The nearest candidate is `japanese-domestic-disclosure-workflow.md`: its `S042`
  is the lane's own IPA process page, but `S043` in that entry is `jpcert.or.jp/vh/…` while lane
  `S043` is HackerOne, its bytes differ from the same-name lane entry, it references no capture, and
  its `recheck:` is a prose sentence plus a backticked `curl` (Q10). It fails on four counts.
- **Rejects recorded, with their reasons:** `chinese-program-severity-instrument.md` (S047
  unregistered, `newsType_6` absent — the standing flip stays unmet);
  `program-severity-ladders-and-reward-scales.md` (same-name bytes unequal, S036 half
  unregistered); `chinese-crowd-testing-national-standard-2026-10-23.md` (cites S077/S078/S079,
  none of which is a lane row); staged `S055` (duplicate-by-document of lane `S036`, and the id C2
  needs).

Assimilation result: **none adopted** — no staged entry passes `PROVINCE.md`/`corpus/QUALITY.md`
admission at this head, no id-collision row is free to reuse, and no refusal flip condition is met.
