# ExecQuarantineSlice — round 35 wave 1 receipt

Seat: `ExecQuarantineSlice` (leaf; no subagents spawned, no `agent://all`, no writes outside the
lane). Date: **2026-10-26**, fetch window `06:32Z`–`06:44Z`. Lane:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

Item: re-derive the kasegi quarantine slice from the read-only shokuknow absent-defect register,
hand-check every row, land verdicts. **No row adopted.**

Tools: nothing installed this run — `curl 8.x`, `openssl`, `pdftotext` (poppler), `python3` were
already present. No pacman/uv/npx transaction was attempted (host-wide pacman pause respected).
Instrument UA reused from `corpus/instruments/capture-source.py:32`:
`kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`.

## Report

### R1 — slice derivation (frozen command, verbatim; run once, then re-run into a second file)

```
$ A=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-35/assimilation; mkdir -p "$A"
$ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
$ awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" > "$A/quarantine-slice"
exit=0
$ wc -l "$A/quarantine-slice"
7
$ cat "$A/quarantine-slice"
 S037   `payload-absent`
 S054   `payload-absent`
 S048`   the cited source could not be fetched, so no quote was checked
 S065`   the cited source could not be fetched, so no quote was checked
 S068`   the cited source could not be fetched, so no quote was checked
 S069`   the cited source could not be fetched, so no quote was checked
 S070`   the cited source could not be fetched, so no quote was checked
$ awk … (same command) > /fast/scratch/…/slice-recheck; cmp -s slice-recheck "$A/quarantine-slice"
exit=0            # deterministic
$ sha256sum "$A/quarantine-slice"
d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862  (417 B)
```

Register digest: `sha256 5afe1810a6c3d62f…`, 83,621 B (same prefix the round-34 verifier recorded,
so the input has not moved).

**S-id requirement: 7/7 lines carry an S-id; no line lacks one.** Two register-format facts
recorded so they are not mistaken for slice defects: the five never-checked ids carry a stray
trailing backtick from the register's own cell (`absent-defect-register.md:322-326`), and those
rows have **no quote column at all** (`awk` shows `fields=7 quote_col=<>` on NR322–NR326), while
NR99/NR100 do (`$7` = the quote). The register's `## By lane` kasegi count of **2** counts only
the `payload-absent` table (lane counts sum to the stated 194); the five never-checked kasegi rows
sit in the second section (109).

### R2 — live hand-check, one fetch per row (`bash handcheck.sh`, exit 0, 67.7 s)

```
utc=2026-10-26T06:32:41Z
S037 curl_rc=0 http=200 bytes=24189   sha256_16=9cba2e96e343e1d0 kind=html
S048 curl_rc=0 http=404 bytes=748     sha256_16=95cd25d80d88cce1 kind=html
S054 curl_rc=0 http=200 bytes=513648  sha256_16=0150c9d15dee603f kind=pdf   (pdftotext 9780 B)
S065 curl_rc=0 http=200 bytes=7465472 sha256_16=e33b0f67293441f1 kind=pdf   (pdftotext 31710 B)
S068 curl_rc=0 http=200 bytes=94027   sha256_16=098f99a89df3a801 kind=html  (301->301->200, sec.cloudapps.cisco.com)
S069 curl_rc=60 http=302 bytes=0      final=https://kass.sacinfo.org.cn/kfs/token/download/mirciskbdmzdvuov
      stderr: curl: (60) SSL certificate … unable to get local issuer certificate (20)
S070 curl_rc=60 http=302 bytes=0      final=https://kass.sacinfo.org.cn/kfs/token/download/iwpbpsmwxkkibqpk
      stderr: curl: (60) … (20)
```

Full body digests (used in the verdicts file):

```
9cba2e96e343e1d0c95d23fb50454fa1321cb2d01af6ae318653290a1d20f204  S037.body
95cd25d80d88cce1e08528c03d5eb488f56bf9991f820bc31569b001eb2e2436  S048.body
0150c9d15dee603f55573f4692f306ba8ff46f70454b032f813b95fbdbb12b88  S054.body
8eb0e46459bcdc9a4997a9818de2b1e60b05c6b7c61ccd262607e15c0e90d539  S054.txt
e33b0f67293441f19ee519b2ed1619121da84867aa8396a3a16facd572586d83  S065.body
60899363173f68e70426ec7120d66d21c66b7cae84406327b4d8d6985045a210  S065.txt
098f99a89df3a8018ab6eff7529fd8482af70dde6406472b88d526c773ded807  S068.body
77c3b495c0a9bf93514da5daa570b097c4cbacd7e4b8ed4fae127651570c1573  S068.norm
b0c046970f9ca2b7bbfae5ee8e847ec0c630049aec1863fe3d5a0a62718e91a9  S069.body
25394c90152ece51d751923029d02c4821ba026e1778f731b12cd31a421ece4b  S069.txt
2eff0a5b10e2625e7d3a5b45c50992f018dde967cf16c97b38557186cdfb3f95  S070.body
be4a35e3fca3353d1de473018e8620fb2f3efcb01cb9058c420ba7e578824de1  S070.txt
```

### R3 — the discrimination that changed a standing verdict (S069/S070)

A certificate-verifying client cannot follow the attachment host (measured again this round, same
as rounds 24/26). That is transport, not absence — so the seat probed the same URLs twice more:

```
$ curl -sS -L -k -A "$UA" -o /dev/null -w '%{http_code} %{size_download} …' '<S069 url>'
200 1470121 application/octet-stream … redirects=1      exit=0
$ curl -sS -L -k -A "$UA" -o /dev/null -w '%{http_code} %{size_download} …' '<S070 url>'
200 234182  application/octet-stream … redirects=1      exit=0
$ openssl s_client -connect kass.sacinfo.org.cn:443 -servername kass.sacinfo.org.cn </dev/null
subject=C=CN, ST=北京市, L=北京市, O=国家市场监督管理总局国家标准技术审评中心, CN=*.sacinfo.org.cn
issuer=C=CN, O=Beijing Xinchacha Credit Management Co., Ltd., CN=Xcc Trust OV SSL CA
verify error:num=21:unable to verify the first certificate
Verify return code: 21 (unable to verify the first certificate)
```

Payloads then fetched to disk with `-k` and rendered: `S069 200 1470121` (PDF 1.7, **58 pp**),
`S070 200 234182` (PDF 1.7, **8 pp**), `pdftotext` exit 0, 146,961 B / 19,747 B text.
Independent corroboration already inside the read-only campaign package:
`shokuknow/merge/kasegi/SOURCES.append.md:62` (staged `S086`/`S119`) records the same DI
attachment at **234 182 B** and states the incomplete-chain reason in its own cells; and
`SOURCES.append.md:61` says the kass token also answers over plain `http`.

So the five "could-not-be-fetched" rows split: **four now carry payload**, one is still dead.

### R4 — quote location and fold results

```
$ python3 <<'PY' … folds = raw | tag-strip+ws-collapse | whitespace-removed …
S037 register quote -> {'raw': False, 'wscollapse': False, 'nospace': False}
S054 register quote -> {'raw': False, 'wscollapse': False, 'nospace': False}
S054 corrected span (parenthetical intact) in wscollapse: False
S054 corrected span nospace: True
exit=0
```

- S037 — composite never contiguous; constituents present once each:
  `标准状态： 现行 … 发布日期 2020-11-19 实施日期 2021-06-01` (page cells, intervening
  在线预览/CCS/ICS between them).
- S054 — real sentence `S054.txt:46-47`:
  `（ア） 脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認` /
  `されたもの又は疑われるもの`; the quoted span deletes the parenthetical and crosses the wrap.
  Round-28 anchor `府 サ 連 第 ７ 号` present (1); `府連第7号` unspaced → 0.
- S065 — `刑法（7 件）` at `S065.txt:1182`; `现行有效法律目录（303 件）` at `:1` (both verbatim).
- S068 — sentence at offset 22,472 of the tag-stripped/collapsed text, once:
  `… The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018 , which are guidelines for disclosure …`
  (raw-HTML exact = 0: inline markup splits it).
- S069 — `6.3.1 技术分级` at `S069.txt:1019` (under `6.3 漏洞分级方法`, `:1017`); head shows
  `ICS 35.030`, `CCS L 80`, `GB/T 30279—202X`, `代替 GB/T 30279—2020`.
- S070 — `一、工作简况` `:8`, `1.1 任务来源` `:9`, plan no `20260806-T-469` `:13`.

Verdict tally: **present-and-located 4** (S065, S068, S069, S070) · **prose-class-unverifiable 2**
(S037, S054) · **unreachable 1** (S048) · **absent 0**. Reasons per row in the verdicts file §2–§3.

### R5 — id-collision screen (needed before any adoption)

```
$ for id in S037 S048 S054 S065 S068 S069 S070; do grep -nE "^\| $id \|" corpus/SOURCES.md; done
S037 => 43:| S037 | FAQ（脆弱性報奨金制度） (サイボウズ) — https://cybozu.co.jp/products/bug-bounty/faq/ …
S048 => 54:| S048 | Microsoft Security Vulnerability Research (MSVR) — https://www.microsoft.com/en-us/msrc/msvr …
S054/S065/S068/S069/S070 => <no lane row>
$ for id in …; do grep -rl "source: $id" corpus/knowledge | wc -l; done
S037 -> 1 file   S048 -> 1 file   (others -> 0)
$ grep -cF <register source prefix> corpus/SOURCES.md
openstd…hcno=458BACCE -> 0 | ipa…ug65p90000019by0-att -> 0 | std.samr.gov.cn/gb/search/gbDetailed -> 0
npc.gov.cn/c2597 -> 0 | cisco.com -> 3 | dcpspTools -> 0
```

Two register ids (`S037`, `S048`) are **bound to different documents in the lane** and both are
cited by knowledge entries; a third (`S068`) is the legacy id of lane **S040** (`Cisco Security
Vulnerability Policy`, `corpus/SOURCES.md:46`, cited at
`corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:2`). No register source is
registered in this lane today. Adoption by number is therefore unsafe for 3 of 7 rows.

### R6 — artifacts written

```
.ufo/waves/round-35/assimilation/quarantine-slice          417 B    sha256 d02acb68cb40164978146cf0f15f18a8f8a66d3c3470b3f6198e9e072911b862
.ufo/waves/round-35/assimilation/quarantine-verdicts.md  19329 B    sha256 b086936919174837f48e04b4209794cc7738716a25abaae3396d43a2dfe5b5a0
```

No other lane path was written. Sibling assimilation artifacts (`collide-check.sh`, `collisions`,
`reg-ids`, `staged-ids`, `quarantine-slice-rederived`, `guard-proof.txt`) belong to other seats and
were left untouched; my slice file and the sibling's `quarantine-slice-rederived` agree on the
7 ids and their order (my file keeps the frozen `$4 $5` projection, so it carries the register's
class cell verbatim; the sibling adds the round and normalises the class names —
`S048` round2, the rest as in §R1).

### R7 — adoption

**None.** Per-row reason in `quarantine-verdicts.md` §6. Short form: S048 unreachable; S037/S054
not adoptable as quoted (corrected quote needed); S065 has no register quote and its staged entry
was never adopted; S068 duplicates lane S040; S069/S070 locate but need a TLS-bypass/plain-http
verification path that must be written into the row itself — a later-round decision.

### R8 — risks / notes for the L1

1. **Standing verdict correction.** Rounds 24/26 recorded S069/S070 as `unfetchable` from
   `302 / 0 B`. The payload *is* retrievable (`1,470,121 B` / `234,182 B`) once the incomplete
   chain is bypassed or plain `http` on the token host is used; the campaign's own staged rows
   already say so. Any future closure check must not treat `curl` exit 60 as "no payload".
2. **TLS exception is a judgement call.** I read those two PDFs with verification off after
   inspecting the chain (`CN=*.sacinfo.org.cn`, issuer `Xcc Trust OV SSL CA`, code 21). If the
   lane wants a strict-verify rule, S069/S070 stay `unreachable`-by-policy even though the bytes
   exist; the verdicts file records both facts so the choice can be made explicitly.
3. **Register-side formatting.** Id columns in the never-checked section carry a stray trailing
   backtick, and that section has no quote column. Fine for reading, hostile to naive parsing —
   the frozen awk is only safe because it prints rather than joins.
4. **Register URLs truncated for S069/S070.** The register's cell ends at `…%E8%8D%89%2F`; the
   full path came from the round-28 hand-check list and the staged package. A reader following the
   register alone would fetch a directory path, not the PDF.
5. **Id collision is load-bearing.** `S037` and `S048` already name different documents in this
   lane, and both are cited. Any adoption of the register rows must renumber by document, never by
   arithmetic (`renumber-map.md` §3).
6. **Divergence with the wave's gate seat, with the cause identified.** This seat ran at
   `06:32–06:44Z`; `wave1/ScribeGateAssimilation.md` ran at `06:33:56Z–06:34:45Z` and recorded
   S069/S070 as `200, 0 B` and S068 as `403, 465 B`. Both are reproducible from the inputs each
   used: S069/S070 there were fetched from the register's **truncated** cell
   (`…%E8%8D%89%2F`, a directory path → `200` empty body, and that is also why the two cells look
   like "one source"), whereas this seat used the full `20_WD_…` / `20_DI_…` paths from the
   round-28 hand-check list and the staged package; and the Cisco URL returns `403` to a
   browser-style UA but `301→301→200` to the instrument UA with `-L` (round-25 finding, re-measured
   here, digest `098f99a89df3a801…`). S065's digest agrees across both seats
   (`e33b0f67293441f1…`, `200 7465472`). Reconciliation of the two receipts belongs to the L1.

### R9 — scratch

All work (7 bodies, 4 text renders, 5 normalised texts, the hand-check script, its stdout) lived in
`/fast/scratch/hyaku/kasegi-r35/ExecQuarantineSlice/`. Digests above were taken from those files
and this receipt was written before removal; the directory was then deleted with `rm -rf`, and its
absence confirmed. No scratch tree is left on disk.
