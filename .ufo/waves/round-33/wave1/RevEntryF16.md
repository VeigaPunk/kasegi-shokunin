# RevEntryF16 — independent Q1-Q10 review of the F16 entry (round 33, wave 1)

Seat: RevEntryF16 (reviewer, non-author — I wrote no line of the reviewed file). Lane:
/home/vgpnk/Projects/shokunin/kasegi-shokunin (only write scope). Answering model:
`devin/glm-5-3-flash-1m` (workstation config; no model passed by hand). Tools
installed/upgraded: none (nothing needed; no pacman transaction, per the paused-host rule).
Date: 2026-10-26.

## 0. Subject and quiescence

Reviewed file: `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`.

```
$ sha256sum corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md   # twice, 45 s apart
53c48b3b322aa4e5f90e1bae27ad0c1fb60c3452b2cff1e35a52e3276bb60a48
53c48b3b322aa4e5f90e1bae27ad0c1fb60c3452b2cff1e35a52e3276bb60a48
$ wc -l -c corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
  306 24492 corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
```

In-flight disclosure (M31-2 class): the file moved `de184a5b…` (270 ln) → `eebd5ea5…` (305 ln)
→ `53c48b3b…` (306 ln) while this seat ran. Every measurement below was (re-)run on the settled
`53c48b3b…` bytes; the author's receipt §1 now declares the same digest. The `recheck:` line is
byte-identical across the last two states (`diff` of the two extracted cmd files → empty).

Bases verified before reviewing: capture pins `S049.txt` = `962a451a…1cb8` (20272 B, 426 ln),
`S050.txt` = `2f9c6406…6888` (31016 B, 630 ln), manifest = `6e4e719a…c774` (14 assertions:
S049 Q1-Q8, S050 Q1-Q6) — all three re-measured by me, all three equal to the entry's
`## Scope and limits` pins. All 14 manifest quote locations were opened against capture bytes
before the entry landed (S049 L208/211/212/214/408/410/419/132; S050 L70/112/418/591/595/597) —
every one holds.

## 1. Q1-Q10 verdict table

| id | verdict | line | quote (from the reviewed file) |
|---|---|---|---|
| Q1 | **pass** | 1,3-7 | `source: S049 — https://zc.cnvd.org.cn/news/helpList — 网络安全众测平台 使用手册, the answers to … (L210-212) … in capture corpus/source-snapshots/round-32/S049.txt:207-214, 408-410, 419` (L3); second `source: S050 — https://security.360.cn/Reward/rules — …` (L4); `verified-at: 2026-10-26` (L5); `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py …` (L7). H1 at L1, header lines directly under it; both `source:` lines carry id + URL + exact anchors; the recheck fails closed (controls in §4). |
| Q2 | **pass** | 17-19, 55-56 (SOURCES.md) | `Every rule below is stated as that platform's own position` (L17). Claims 1-2 rest on S049, claims 3-6 on S050; both registry rows are tier A, `mined`, opened `2026-10-26` (the admitting round), `used-by corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` (`corpus/SOURCES.md:55`, `:56` — landed by ExecRegistryAppend this round). Captures re-opened in the admitting round: ScoutLiveDrift 2026-10-26T04:16Z, 0 differing lines (entry L289-293). No tier-C row cited: `grep -n 'S026\|S027' <entry>` → 0 hits. |
| Q3 | **pass** | 26,37,47,58,68,74,91,96,108,115,126,133,138,151,154 | 15 block quotes, each followed by a `> — ` location line (15/15, script in §3); max length 13 space-tokens / 48 chars (Chinese has no inter-word spaces; the round-32 spotcheck precedent judges 28-32-char quotes within bar). Numbers are quoted, not retyped: `200元` quoted from S049.txt:356 (verified =1), `安全币 ：RMB=1 : 5` from S050.txt:129, `V2.0`/`2023-03-01` from S050.txt:62/68; the scoring-example figures are cited by line range (S049.txt:134-142), never retyped. |
| Q4 | **pass** | 11-19 + every claim heading | `Neither document is treated as a rule for any other platform, and neither is read as a legal authorization` (L18-19). Claims 1-2 are headed `the CNVD 众测 manual states/publishes…`, claims 3-6 `the 360SRC standard states…`; the cross-market money-scale comparison is itself a rejected over-generalization (#7, L235); F13's VRT override and F15's intake routes are conceded and differentiated, not merged (`One overlap named`, L268-281). |
| Q5 | **pass** | 201-206, 210-240 | Six falsifiable checks (FC-1…FC-6), each a runnable grep with its measured count — all 16 stated counts reproduced exactly by this seat (§2). Seven rejected over-generalizations, each with a reason and pointer (e.g. #1 L210-213, #7 L235-240). |
| Q6 | **pass** | 191-194, 305 | `That material is **not reproduced** here — no account, password, profile or certificate value appears in this entry, and none of those lines is quoted (Q6).` (L193-194). Credential scan on the entry: `密码|账号|帐号|password|passwd|token|secret|ovpn|ca.crt|op://` → 2 lines, both inside the non-reproduction disclosure itself (L191, L193); `VPN` → 2 lines, same paragraph. **The CNVD page's VPN/credential content (S049.txt:201-206 retrieval steps, L374-405 OpenVPN walkthrough) is NOT reproduced** — the entry names the lines as located-and-withheld. URLs in the entry: only the two `source:` URLs plus the two public URLs the documents themselves print (`http://www.cnvd.org.cn/` quoted from S049.txt:214; `https://security.360.cn/Product/product` named from S050.txt:71). No session or private URL, no vault-reference URI, no probing/scanning/login/submission instruction anywhere. |
| Q7 | **pass** | 7 | The `recheck:` field is one command (human note after `#`), not prose. Its output names what was checked: 16 lines `S049:Qn OK occurrences=1` / `S050:Qn OK occurrences=1` + 2 `sha256 OK` (§4). Missing/corrupted-source controls fail closed (§4, run by this seat, not copied from the author's). |
| Q8 | **pass** | 7, 297-299 | Normalization declared twice: recheck comment `each \`occurrences=1\` under source-recheck.py's declared normalization` (L7) and Scope bullet `under \`source-recheck.py\`'s declared normalization (capture markup stripped, whitespace collapsed)` (L297-299). No quote depends on converter markup: the one wrap-broken sentence (`合资公司` split across S050.txt:70/71) is explicitly NOT bound — `the full sentence does not bind as one recheck assertion` (L101-103). |
| Q9 | **pass** | manifest + 53, 108, 133 | Path stem == id for both manifest records (`S049`→`S049.txt`, `S050`→`S050.txt`, read from `manifest.json`). All 14 manifest assertions print the observed count: 14 × `occurrences=1` (§4). Every hand-measured string carries its own count in place, and this seat re-measured each: 12 inline strings exactly-once in their captures (§3), the `安全币 ：RMB=1 : 5` label = 7 (L129 + 6 named repeats, all six verified), the awk-scoped CVSS-vocabulary count → 1 (verified). No quote occurs twice unanchored. |
| Q10 | **pass** | 7 | `bash -n` on the extracted recheck line → exit 0; run from the lane root → exit 0; run from `cd /` → exit 0 with identical output (§4). Carries its own `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&` prefix; the human note sits after `#`. |

## 2. FC count reproduction (this seat's runs, capture bytes)

```
FC1a=1 FC1b=1                     # 众测平台仅接收… / 不接受互联网漏洞 in S049.txt
FC2a=2 FC2b=1 FC2c=1              # 授权 / 并不是项目的测试范围约定 / 注：请严格…
FC3a=1 FC3b=1                     # 本标准适用于… / 具体范围可参考… in S050.txt
FC4a=1 FC4b=6                     # 未纳入安全服务… / 不予收录
FC5a=0 FC5b=32 FC5c=12            # 安全币 in S049 / S050 / 奖金 in S049
FC6a=0 FC6b=0 FC6c=0 FC6d=1       # 免责|安全港 ×2 / 授权测试 / 同时 360 保留…
```

All 16 equal the entry's stated counts. Additional hand-measured strings re-measured
exactly-once: 系统将展示相关协议条款…后=1, 降低测试区间异常事件引发的法律风险=1,
不建议在公开群组、或一对一聊天中询问此类信息=1, 奖金的提取没有上限…200元。=1,
网络安全众测平台为每一个被确认的漏洞设计了积分评价机制=1 (27 chars, as stated),
360 集团所投资的公司、子公司、合资公=1, 司等也在收录范围内=1,
初评级后七个工作日内=1, 评分标准和漏洞奖励仅针对对 360 产品和业务有影响的漏洞=1,
360 集团及关联方员工不参与=1, 本标准最终解释权归 360 信息安全部所有=1;
`grep -c 附加分 S049.txt` → 1 (as claimed); the awk-scoped CVSS count → 1 (as claimed).

## 3. Quote audit (settled bytes)

```
$ python3 (block-quote extractor over the entry)
block_quotes= 15 located= 15
L26: tokens=1 chars=31 … L154: tokens=1 chars=32   # per-quote table in the run log
max tokens=13 (the S049.txt:132 formula)  max chars=48 (S049.txt:208 quote)
```

Location lines name capture file + line + section for every quote; the two hand-measured block
quotes (S050.txt:113, S050.txt:129) say so in their own location lines.

## 4. Recheck-line execution and fail-closed controls (this seat's runs)

```
$ bash -n $S/cmd.sh; echo "bash_n_exit=$?"          → bash_n_exit=0
$ bash $S/cmd.sh            # from the lane root
S049:sha256 OK … S049:Q8 OK occurrences=1 … S050:Q6 OK occurrences=1   (16 OK lines)
lane_root_exit=0
$ ( cd / && bash $S/cmd.sh ); echo "foreign_cwd_exit=$?"               → foreign_cwd_exit=0
```

Controls (scratch copies under `$HYAKU_SCRATCH/kasegi-r33/RevEntryF16/`, committed captures
untouched):

```
$ printf 'x' >> $S/ctl/S050.txt && python3 corpus/instruments/source-recheck.py --manifest $S/ctl/manifest.json --source S050
S050:sha256 MISMATCH expected=2f9c6406…6888 actual=c848c1b5…1b6b
corrupt_S050_exit=1
$ rm $S/ctl/S049.txt && python3 corpus/instruments/source-recheck.py --manifest $S/ctl/manifest.json --source S049
S049:source UNAVAILABLE reason=missing
missing_S049_exit=2
```

## 5. Restatement check (C2 kill-rule clause)

- Negative sweep: `grep -rln '众测\|360SRC\|安全币' corpus/knowledge/*.md` → only the new entry
  and `program-severity-ladders-and-reward-scales.md` (F13), whose sole mention is its refusal
  note "CNVD 众测 and BILISRC ladders … **not adopted this round**" (F13:64). No earlier entry
  holds this ground.
- F13:32's VRT override and S043.txt:31's HackerOne asset paragraph are quoted accurately
  (verified against both files) and positioned as different mechanisms, not merged.
- The refused staged entry `chinese-program-severity-instrument.md` (exists in the read-only
  package) is named as prior holder of the S049 formula; the entry re-claims only the
  platform's published formula and declines the CVSS metric set — the awk-scoped count → 1
  verified.
- The refused `program-scope-rules-and-asset-boundaries.md` flip conditions (register+capture
  the two rows, located quotes, per-platform attribution, executable recheck, lane-frontier
  ground) are each met by this entry; it is the flip, not a copy (305→306-line re-grounded
  entry vs the 39-line staged original).
- Harness binding on the real tree (F16 row landed by ScribeReadmeF16):
  `python3 corpus/instruments/frontier-recheck-count.py` → `PASS F16 knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050 exit=0`, `entries=19 pass=19 exit=0`.

## 6. Findings below the bar (routed, none admission-blocking)

1. **LOW — Q3's ≤25-words rule has no Chinese word-segmentation instrument.** The longest quote
   is 48 chars / 13 space-tokens (S049.txt:208). Judged within bar by the lane's own round-32
   spotcheck precedent (28-32-char quotes "under 25 words") and by Chinese lexical-word
   segmentation (~25 words); the entry's receipt prints both measures. A future Chinese-language
   entry with a materially longer quote needs a declared segmentation rule.
2. **LOW — the `source:` lines' anchor lists are a summary, not exhaustive.** The body
   hand-measures lines the `source:` anchor cell does not list (S049.txt:72, 132, 200, 356, 359,
   414; S050.txt:99, 119-124, 126-330). Same shape as the admitted F15 entry (source line
   L28-35, body cites L15/L48); each body cite carries its own pointer, so nothing is
   unlocatable. Not a Q1 failure.
3. **NIT — the entry's whole-file CVSS grep would read 3, not 1** (the awk command line itself
   contains `CVSS`, and the "One overlap named" prose names CVSS 3.0). The entry's claim is
   explicitly scoped "over the claim sections" with the awk span, which this seat verified → 1;
   correct as written, but a reader running the unscoped grep first will see 3.

## 7. Verdict

**ADMIT.**

Reasons: all ten criteria hold on the settled bytes under this seat's own measurements — the
recheck line runs green from the lane root and from `/`, fails closed on corrupted (exit 1) and
missing (exit 2) sources, all 14 manifest assertions are exactly-once with path-stem==id, all
16 falsifiable counts reproduce, both registry rows are tier A opened in the admitting round,
attribution is kept per platform, the CNVD page's VPN/credential material is located and
withheld rather than reproduced, and the entry adds ground (customer-authorization scope object,
service-coverage asset filter, two non-reducible reward instruments) that no earlier entry or
refused staged entry holds — with the one real overlap declared and declined.

Sentence that most strongly supports the verdict (L193-194, verified by this seat's credential
scan): "That material is **not reproduced** here — no account, password, profile or certificate
value appears in this entry, and none of those lines is quoted (Q6)." — the CNVD capture is the
one source in this round carrying platform-issued credential material, and the entry is the
artifact that had to prove it could cite that page while carrying none of it; it does.

## 8. Bounds

Writes this seat: this receipt only. No lane file edited; no git/jj mutation; no fetch; no
subagent; no background job beyond the two item-sanctioned receipt polls. Scratch
`/fast/scratch/hyaku/kasegi-r33/RevEntryF16/` removed before yield. No pacman transaction; no
tool installed.
