# ScribeAssimilation — assimilation section block (round 38, wave 1)

Seat: scribe, leaf (no subagent dispatch). Axis: coverage. Milestone: round-38. Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` at HEAD `700153593eb586c70a6499c8ca225ee4d673bc9b`
(base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e` + claims freeze `9a10b02f` + wave-1 spec `7001535`;
`git diff --name-only a173b0c2 HEAD` touches only `.ufo/waves/round-38/**`). Everything below was
measured read-only by this seat; no peer receipt for the collision guard, the quarantine slice or the
refusal flips existed in `wave1/` when I ran (`ExecQuarantine` and `ScoutStandingRefusals` had not
landed), so nothing here is copied from a sibling.

## Deliverable (byte-exact, landable bytes only)

| file | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-38/wave1/ScribeAssimilation.block.md` | 106 | 8847 | `1a4ca55766205e1a207b17e61cf3be94f85578afb8ee5d35e45bdf162f2dd31e` |

One heading (`## Assimilation: none adopted`), no fences, no validation table, no placeholder tokens
(`grep -nE '⟨pending|<r3[0-9]|<fill>|TBD|TODO|FIXME|XXX|placeholder'` → no output). The body is the
text the L1 lands in `corpus/lessons/round-38.md`; all evidence lives in this receipt.

## 1. Id-collision rerun

Guard extractor (the one the round-35 guard ships, 0–3 leading spaces):

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md \
    | grep -oE 'S[0-9]+' | sort > staged-ids
$ comm -12 reg-ids staged-ids > collisions
reg=54 staged=94 coll=24
reg unique=54 staged unique=94
coll list: S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054
ea4dfaaa459dcb0ba8a648a11896a166a101b39a970b667cae02fc867c385047  reg-ids
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  staged-ids
3f3799a4d918288c122c7c0c062b7d1aa4ee6acb44a412637a1540309d64c492  collisions
```

Inputs: lane `corpus/SOURCES.md` HEAD blob = base blob, 54 rows (`grep -cE
'^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 54, and the 0–3-space count → 54); staged file
`sha256 4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb`, 100 lines, 89,718 B,
mtime `2026-10-24 23:33:20.041997004 -0300`. The three artifacts are byte-equal to
`wave1/ExecIdCollision.{reg-ids,staged-ids,collisions}` (same digests), so the executor's submission
is independently reproduced.

Head-relative variants measured at this head:

```
$ cp reg-ids reg55; echo S055 >> reg55; LC_ALL=C sort -o reg55 reg55
$ comm -12 reg55 staged-ids | wc -l        -> 25   (S031..S055)
$ grep -cE '^ {0,3}\|[[:space:]]*S055[[:space:]]*\|' corpus/SOURCES.md   -> 0   (C2 not landed yet)
```

Document-identity check over every cited id that is also a lane row and carries a URL (34 pairs):
**1** same host (`S042` = `https://www.ipa.go.jp/security/todokede/vuln/process.html` both sides),
**33** different hosts. Examples measured: `S047` staged `sse.com.cn` vs lane `ipa.go.jp`; `S048`
staged `std.samr.gov.cn` vs lane `microsoft.com`; `S053` staged `meti.go.jp` vs lane `first.org`.

Staged `S055` row (`SOURCES.append.md:31`) is the Cybozu vulnerability-handling policy,
`https://cybozu.co.jp/company/security-policy/` — the same document as lane `S036`, and the id the
round-38 CSAF row needs.

## 2. Guard proof (indented-row fixture)

```
$ cat -A proof-registry.md
| S001 | x |$
  | S002 | y |$
$ cat -A proof-staged.md
| S002 | y |$
A reg=[S001 S002] staged=[S002] collisions=[S002] count=1
B (column-zero only) reg=[S001] staged=[S002] count=0
indent=1 A_match=1
indent=2 A_match=1
indent=3 A_match=1
indent=4 A_match=0
indent=5 A_match=0
```

The indented `S002` row is caught only by the 0–3-space extractor; the column-zero-only pattern
misses it. Real inputs carry zero 4+-space-indented `S` rows, so the 24 stands.

## 3. Quarantine slice

```
$ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
$ sha256sum "$R"; wc -lc "$R"
5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833  (register)
  375 83621 (register)
$ awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R"
 S037   `payload-absent`
 S054   `payload-absent`
 S048`   the cited source could not be fetched, so no quote was checked
 S065`   the cited source could not be fetched, so no quote was checked
 S068`   the cited source could not be fetched, so no quote was checked
 S069`   the cited source could not be fetched, so no quote was checked
 S070`   the cited source could not be fetched, so no quote was checked
awk_exit=0   7 lines, 417 B
sha256 d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862
$ cmp slice .ufo/waves/round-37/assimilation/quarantine-slice   -> IDENTICAL
```

Register lines 99 (S037), 100 (S054), 322 (S048), 323–326 (S065/S068/S069/S070); ids on 322–326
carry a stray trailing backtick in the register's own cell.

Live refresh (UA `kasegi-shokunin/1.0`, `curl -sS -L --max-time 90`), all recorded 2026-10-26:

| row | request | status | bytes | result |
|---|---|---|---|---|
| S037 | `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=458BACCE700CA8E0B728CFB5F762DE7A` at 18:32:45Z | 200 | 24,131 | tag-strip + whitespace-collapse: contiguous register quote → **0**; `标准状态：现行`, `2020-11-19`, `2021-06-01`, `网络安全漏洞分类分级指南` → 1 each. Present-and-located, quote stitched |
| S054 | `https://www.ipa.go.jp/security/guide/vuln/ug65p90000019by0-att/request_to_ipa.pdf` at 18:32:36Z | 200 | 513,648 (PDF; `pdftotext` text 3,099 chars) | contiguous quote → **0**; live text `（ア）脆弱性（（法第42条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの`; `悪用が確認されたもの` → 1, `又は疑われるもの` → 1. Present-and-located, quote elided |
| S048 | `https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3` at 18:32:35Z | 404 | 748 | body `HTTP状态 404 - 未找到`; `sha256 95cd25d80d88cce1…` — byte-identical to the r36/r37 probe. Unreachable as cited |

Carried from round 37 (not re-fetched): S065, S068, S069, S070 — all four were located there, and
both the register (`5afe1810…`) and the package (`4fe049cb…`, every mtime `2026-10-24 23:33:20`) are
byte-identical to the state those verdicts were measured against.

Slice result: 0 adopted; 0 fabrication-class, 1 unreachable (S048), 6 present-and-located.

## 4. Standing refusals — the two sampled flips

```
$ sha256sum corpus/knowledge/program-severity-ladders-and-reward-scales.md \
    /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/program-severity-ladders-and-reward-scales.md
6c05c98f3c6851b560098b8f7c43350a951e487e8b34e2ff09831563aa8ff4a6  (lane, 67 lines)
35de5f8b19ed3b20beb3d41c347f4727d9fd2eefc8a23e53c64c6987b60bbc87  (staged, 50 lines)
$ grep -c newsType_6 corpus/source-snapshots/round-32/S049.txt      -> 0     (newsType_21 -> 1)
$ grep -c sse.com.cn corpus/SOURCES.md                              -> 0
$ sha256sum /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/chinese-program-severity-instrument.md
442e0f2bfb08bc2cbb8951f110e64424f82203636928429bc38f46f388c4257c  (41 lines)
```

Flip conditions: byte-identity or a supersedes row (absent); the `newsType_6` anchor (absent); an
`S047` row for `sse.com.cn` (absent). Package stability: 70 files, all mtime `2026-10-24 23:33:20`,
`SOURCES.append.md 4fe049cb…73eb`. **0 of 7 flip conditions met**, so all seven reasons at
`corpus/lessons/round-35.md:155-169` stand.

## 5. Assimilation-set classification

Set: 67 staged `knowledge/corpus/knowledge/*.md` entries against 49 lane `corpus/knowledge/*.md`
entries (`ls … | xargs -n1 basename | LC_ALL=C sort`, `comm`). Method: per entry, extract the ids on
`source:` lines (`\bS\d{3,}\b`), test each against the lane registry ids from `SOURCES.md`, compare
the cited URL host with the registry row's URL host, look for `corpus/source-snapshots/…` references,
a `cd`-prefixed single-command `recheck:` line, quoted sentences, and a `ground: F##` naming a live
lane frontier id.

```
entries=67
with source lines=67
all cited ids registered=12
zero registered ids=52
partial (mixed)=3
entries citing >=1 unregistered id=55
entries referencing a lane capture=0
cd-prefixed recheck lines across all entries=0
entries with no quoted sentence=11
grounds naming a live lane F id=27
same-name divergent=4
cited registered ids with a URL=34   host-same=1   host-different=33
```

- Same-name, divergent bytes (overwrite hazards): `authorised-testing-rules-of-engagement.md`
  `5533fc87…` vs `bf40409e…`; `japanese-domestic-disclosure-workflow.md` `a22d2321…` vs
  `ee667c2f…`; `japanese-severity-vocabulary-and-impact-model.md` `f584f06c…` vs `d7fdd31f…`;
  `program-severity-ladders-and-reward-scales.md` `6c05c98f…` vs `35de5f8b…`.
- Nearest candidate: `japanese-domestic-disclosure-workflow.md` — same `S042` document, but `S043`
  is `jpcert.or.jp` staged vs HackerOne in the lane, no capture, `recheck: 180d — \`curl …\`` is a
  prose+command hybrid (Q10), and the same-name lane file differs. Not admissible.
- **Admit count: 0.** **Rejects recorded (with reasons):**
  `chinese-program-severity-instrument.md` (S047 unregistered, `newsType_6` absent);
  `program-severity-ladders-and-reward-scales.md` (bytes unequal, S036 half unregistered);
  `chinese-crowd-testing-national-standard-2026-10-23.md` (S077/S078/S079 all unregistered);
  staged `S055` Cybozu policy (duplicate-by-document of lane `S036`, id needed by C2).

## 6. Bounds, tooling, scratch

- Writes: only the deliverable and this receipt under `.ufo/waves/round-38/wave1/`, plus scratch.
  No tracked lane file touched, no fleet/shokuknow write, no package tool run.
- No mutating git command; read-only `git log/rev-parse/status/diff/show` only.
- Network: three `curl` probes (§3) with the required UA, statuses and byte counts recorded.
- Tools: none installed or upgraded; `awk`, `grep`, `comm`, `sha256sum`, `curl`, `pdftotext`,
  `python3` from the host sufficed.
- Scratch `S=/fast/scratch/hyaku/kasegi-r38/ScribeAssimilation/` was created with `mkdir -p`, held
  every artifact and probe body, and was removed with `trap 'rm -rf -- "$S"' EXIT`; `ls
  /fast/scratch/hyaku/kasegi-r38/ScribeAssimilation` → `No such file or directory` at yield.
