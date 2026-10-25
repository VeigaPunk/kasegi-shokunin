# C2Sentinel — falsification of wave-1 SentinelCapture: Q6 issues, personal data, credentials, injection text

Seat: `L1Kasegi25.C2Sentinel` (READ-ONLY; this file is the only write).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (`git rev-parse HEAD` = `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`).
Window: 2026-10-25, wave 2.

## Target and verdict

Audited: the five round-25 captures (`corpus/source-snapshots/round-25/S036.txt…S040.txt`),
the two live entries (`corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md`,
`corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md`), the manifest
(`corpus/source-snapshots/round-25/manifest.json`), and the two staged package files under
`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/`.

**Verdict: wave-1's SentinelCapture is confirmed, not falsified — `5/5` captures CLEAN and
`4/4` entries Q6 PASS on the current bytes, with two corrections to wave-1's *observations*
(the S038:17 elision is fixed; `manifest.json` now exists). NO security finding. The smallest
correction to wave-1 is limited to its observations section — no production edit needed.**

## 1. Bytes of record — digests (exact commands, outputs)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ sha256sum corpus/source-snapshots/round-25/S036.txt corpus/source-snapshots/round-25/S037.txt \
    corpus/source-snapshots/round-25/S038.txt corpus/source-snapshots/round-25/S039.txt \
    corpus/source-snapshots/round-25/S040.txt
022ca4f40b9e07a4e052c4d6ac8a9b4195503489417eb7fd0760d28c35ceb950  corpus/source-snapshots/round-25/S036.txt
b204aa7f60ec2e70713ecd8c605fb1adb6e39549f0ef09d32a297c10f473cb4c  corpus/source-snapshots/round-25/S037.txt
09e077d31ce3b5e366fa435f5c474db7405eef8dd313b64be46f88047dabb68a  corpus/source-snapshots/round-25/S038.txt
657e7b4c67e67d00b190b31942d749a28d0988f15d1e6f5f506130accffc191d  corpus/source-snapshots/round-25/S039.txt
b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c  corpus/source-snapshots/round-25/S040.txt
```

All five match `.ufo/waves/round-25/capture-log.txt` verbatim (S036 sha256=022ca4f4…, S037=b204aa7f…, S038=09e077d3…, S039=657e7b4c…, S040=b7f7b55f…). Capture bytes unchanged since wave-1's audit.

```
$ sha256sum corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
7882ae415733520e9f45d761c9cdc2138b4219817f967289b4f2bce6077936dd  corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
4885218fa07d97dd9d5cfbf4bf3d238f11c98e598e4cf6d597e1a8a6a5269b8b  corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
```

The live entries **differ** from wave-1's pinned digests (`f07a96bc…` 13774 B → now `7882ae41…` 13961 B; `d22f6439…` 15816 B → now `4885218f…` 16211 B). Wave-1's PASS verdict was therefore re-derived by this seat on the current bytes (below). Both entries are untracked new files (`git status --short` → `?? corpus/knowledge/vendor-disclosure-*.md`), so no committed baseline exists to diff; I audited current bytes in full.

## 2. Byte-level sweep (Python `read_bytes()`/decode)

| file | UTF-8 | control bytes | DEL | zero-width/bidi | U+FFFD |
|---|---|---|---|---|---|
| S036.txt | valid | 0 | 0 | 0 | 0 |
| S037.txt | valid | 0 | 0 | 0 | 0 |
| S038.txt | valid | 0 | 0 | 0 | 0 |
| S039.txt | valid | 0 | 0 | 0 | 0 |
| S040.txt | valid | 0 | 0 | 0 | **7 on lines 108(×2), 193, 203, 222(×2), 479** |
| manifest.json | valid | 0 | 0 | 0 | 0 |
| JP entry (live) | valid | 0 | 0 | 0 | 0 |
| crosswalk (live) | valid | 0 | 0 | 0 | 0 |
| staged japanese-…md | valid | 0 | 0 | 0 | 0 |
| staged vendor-cvd-…md | valid | 0 | 0 | 0 | 0 |

S040's U+FFFD set matches wave-1 exactly (lines 108, 193, 203, 222, 479; total 7).

## 3. Credential / secret / vault sweep

Grep pattern set: `AKIA[0-9A-Z]{16}`, `ghp_`, `xox[baprs]-`, `sk-[A-Za-z0-9]{20}`, `api[_-]?key`, `secret`, `passwo?rd`, `token`, `bearer`, `authorization:`, `cookie:`, `PRIVATE KEY`, `ssh-rsa`, `BEGIN`, `jwt`, `op://`, `vault://`, `keychain`, `1password`, `bitwarden`, `.env`, `id_rsa`, `.pem`, `credential` — over captures + manifest + both live entries.

Hits, all false positives:
- `S040.txt:48` — `Hardcoded or undocumented account credentials` (policy term naming what Cisco forbids in its own products; wave-1 called this exact false positive).
- `S040.txt:229` — "Cisco will begin assessing potentially impacted" (prose).
- JP entry `:210` — self-description "carries no credential material" (documents the absence).
- crosswalk `:123` — "whitespace-separated tokens" (quote-counting note; wave-1 flagged this exact line).

Staged files: `LC_ALL=C grep` with the full credential/PII/injection set returned **exit 1 (zero hits)**.

## 4. PII / emails / phone / names

Emails found — all role addresses, public (matches wave-1):
```
$ grep -rhoE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' corpus/source-snapshots/round-25/ corpus/knowledge/vendor-disclosure-*.md | sort | uniq -c
1 cust-security-announce@cisco.com
3 cust-security-announce-join@cisco.com
3 cust-security-announce-leave@cisco.com
1 media_pr@cisco.com
2 psirt@cisco.com
1 security@cybozu.co.jp
1 security@pepabo.com
```
No personal name anywhere: S036:41 mentions names published on a 謝辞 page but carries none; S039:514/647/668 reference the 謝辞 without names; S040:183 acknowledges reporter contributions generically. Phone shapes found are Cisco public support lines (S040:84-85 `+1 877 228 7302`, `+1 408 525 6532`, :95-96 `+1 800 553 2447`, `+1 408 526 7209`) — vendor→customer contact numbers, not personal data. The earlier `manifest.json:189` hit was my own PII pattern `[0-9]{3}-[0-9]{4}` matching the ISO standard id `cisco-iso-29147-2018` (re-verified: `grep -rniE 'localhost|…|session|token=' corpus/source-snapshots/round-25/manifest.json` → exit 1, zero hits; the alternation matches nothing in the manifest).

## 5. URLs — no session/private/query/fragment

Entry URLs (deduplicated, all public, all bare — no userinfo, no query, no fragment):
```
https://cybozu.co.jp/company/security-policy/
https://cybozu.co.jp/products/bug-bounty/faq/
https://pepabo.com/contact/vulnerability-reporting/
https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html
https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html
```
Capture URLs include Cisco's `https://mycase.cloudapps.cisco.com/start` (S040:99 — public landing page of a login-gated support portal; no token, no query string, no session id — matches wave-1's classification), `https://cscrdr.cloudapps.cisco.com/…/Cisco_PSIRT_PGP_Public_Key.asc` (S040:79-80 — public PGP key pointer, not key material), and `http://sec.cloudapps.cisco.com/security/center/rss.x?i=44` (S040:132 — feed id, not a token or session). No `file://` and no local absolute paths in any file. Zero IP addresses: `grep -rhoE '\b[0-9]{1,3}(\.[0-9]{1,3}){3}\b'` → no output.

## 6. Injection text / markup hiding / lane vocabulary

- Injection greps EN (`ignore previous`, `disregard`, `system prompt`, `you are`, `assistant`, `override`, `</?system`, `BEGIN SYSTEM`, `jailbreak`, `prompt`) and JP (`指示`, `命令`, `無視`, `上書き`, `システムプロンプト`, `エージェント`, `前の指示`): the only hit is S040:9 "If you are experiencing a security vulnerability emergency, see Cisco PSIRT Contact Information" — vendor navigation, not injection. Zero JP hits. Zero hits in both entries, manifest, and staged files.
- Markup hiding (`<!--`, `<script`, `<iframe`, `display:none`, `<style`, `<form`, `onclick`, `javascript:`): zero hits in all files. No HTML comment bodies survive in any capture (wave-1 documented dangling `-->` tails only; confirmed no `<!--` openers).
- Lane vocabulary (`corpus/`, `.ufo/`, `SCORECARD`, `kasegi`, `shokunin`, `recheck:`, `source:`, `QUALITY.md`, `subagent`, `LLM`, `assistant`, `claude`, `gpt-`, `openai`): **zero hits in all five captures** (exit 1). Wave-1's zero-hit claim reproduces.

## 7. Instruction-class lines in captures (vendor→reader only)

Highest-risk lines re-verified verbatim:
- `S037:123` — 「報告用サイトでは脆弱性検証を行わないでください。脆弱性検証は、脆弱性検証環境提供プログラムで提供された環境をご利用ください。」 (prohibition + redirect to vendor-provided verification environment).
- `S037:126` — 「「ログインでお困りですか？」へアクセスし、登録済みのメールアドレスを入力してパスワードをリセットしてください。」 (login/credential-recovery instruction).
- `S040:103-105` — support-contract vs non-contract telephone contact instructions; `S040:124-159` — mailing-list subscribe/unsubscribe instructions; `S040:407-475` — customers' support/entitlement instructions. All addressed by the vendor to its own customers/subscribers — none is a lane directive.
- `S036:31/45/50`, `S037:99/101/103/106`, `S038:22-25`, `S039:563/572` — navigational/submission/prohibition text, all vendor→reader.

**Key exclusion verified:** neither live entry quotes `S037:126` (the password-reset line). The JP entry quotes S037:99 (account required), S037:101 (application form) and S037:123 (the prohibition), all as attributed blockquotes.

## 8. Q6 per entry (current bytes)

| entry | credentials | session/private URL | op://vault:// | imperative against a target | Q6 |
|---|---|---|---|---|---|
| vendor-disclosure-policies-as-corpus-objects.md | none | none | none | none (all imperatives inside `>` blockquotes are vendor FAQ text) | **PASS** |
| vendor-disclosure-policy-commitments-crosswalk.md | none | none | none | none | **PASS** |
| staged japanese-vendor-disclosure-policies-2026-10-23.md | none | none | none | none | **PASS** |
| staged vendor-cvd-policy-crosswalk-2026-10-23.md | none | none | none | none | **PASS** |

Entry imperative-hits re-inspected: JP entry `:78` (`お申込みください。` quote), `:82` (`教えてください。` inside Q label), `:87` (`行わないでください。` quote), `:102-103` (full S038:17 quote); EN hits `:187/197/210`, crosswalk `:98` — all prose or blockquotes, no reader-directed imperative. The self-description at JP entry `:209-211` ("It instructs no probing, scanning, login or submission against any target, and carries no credential material, session or private URL") is true of the bytes.

## 9. Error-corrections to wave-1's observations (not its verdict)

1. **Wave-1 observation d3 (quote elision) is fixed in the current bytes.** `vendor-disclosure-policies-as-corpus-objects.md:102-103` now quotes S038:17 whole and names the dropped subject: "> また、当社システムへの侵入または侵入の試みが以下に示す条件を守る限りにおいて、セキュリティ研究者に対して、法的措置をとらない方針です。… (quoted whole: the fragment omits the subject, 当社システムへの侵入または侵入の試みが)". The elision no longer exists.
2. **Wave-1 observation d2 is stale.** `corpus/source-snapshots/round-25/manifest.json` **now exists** (11451 B, sha `…`, mtime 2026-10-25 05:51 local > the 08:40Z wave-1 window). Both entries' `recheck:` lines name it; the fail-closed state wave-1 observed was transient. `source-recheck.py` was not run by this seat.
3. **Wave-1's entry digests are stale** (13774/15816 B then, 13961/16211 B now) — the verdict still holds on current bytes per §8.

## 10. Method and reproduction

Wave-1's method (§e) was reproduced with the same commands: `sha256sum` (compare to capture-log); Python byte scan (control/DEL/bidi/zero-width/UTF-8, FFFD census); credential/PII/private-URL/injection greps (patterns listed in §§3-6, `-i` where wave-1 used `-i`); URL extraction (`grep -rhoE 'https?://…'`); entry header blockquote inspection and line-by-line re-read of every Q6-relevant quote. No live host contacted; no file created/edited outside this report; no tool installed or upgraded.

## 11. Smallest correction if wave-1 were wrong

It is not wrong on any security verdict. The only corrections to wave-1's report are its observations d2 (manifest now exists — removed/reworded) and d3 (elision fixed in current bytes — remove or mark resolved), plus re-pinning entry digests. No production edit.
