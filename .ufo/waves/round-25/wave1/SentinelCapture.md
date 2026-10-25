# SentinelCapture — security review of the round-25 captures and the two new entries

Seat: `L1Kasegi25.SentinelCapture` (READ-ONLY; this file is the only write).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`
(`git rev-parse HEAD` = same at start and end of this review).
Window: 2026-10-25T08:24Z–08:40Z. Nothing outside this file was created, edited, moved or deleted.

## 0. Objects audited (bytes of record)

| object | bytes | sha256 |
|---|---|---|
| `corpus/source-snapshots/round-25/S036.txt` | 4815 | `022ca4f40b9e07a4e052c4d6ac8a9b4195503489417eb7fd0760d28c35ceb950` |
| `corpus/source-snapshots/round-25/S037.txt` | 11194 | `b204aa7f60ec2e70713ecd8c605fb1adb6e39549f0ef09d32a297c10f473cb4c` |
| `corpus/source-snapshots/round-25/S038.txt` | 3093 | `09e077d31ce3b5e366fa435f5c474db7405eef8dd313b64be46f88047dabb68a` |
| `corpus/source-snapshots/round-25/S039.txt` | 37126 | `657e7b4c67e67d00b190b31942d749a28d0988f15d1e6f5f506130accffc191d` |
| `corpus/source-snapshots/round-25/S040.txt` | 33463 | `b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c` |
| `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` (live, final read 08:40Z) | 13774 | `f07a96bc71d71ba75dc2ccb92c5614cdebb1d401b41ecafed699f842b0dedf97` |
| `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` (live, final read 08:40Z) | 15816 | `d22f6439cfee5bd4ef9b31a1706eb903ab01aa68e4e280e8a8b59667a4b8db45` |
| `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/japanese-vendor-disclosure-policies-2026-10-23.md` (staged) | — | read-only |
| `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/vendor-cvd-policy-crosswalk-2026-10-23.md` (staged) | — | read-only |

The five capture digests are byte-identical to the digests the capture instrument printed in
`.ufo/waves/round-25/capture-log.txt` (recomputed here with `sha256sum`). Both live entries were
being edited by other seats while this review ran (`vendor-disclosure-policies-as-corpus-objects.md`
changed twice between 08:31Z and 08:40Z, 11905 → 12646 → 13774 B); the digests above pin the final
versions audited, and each Q6 finding below was re-run against that final version.

---

## a) Per-capture verdicts

**Summary: 5/5 CLEAN** on credential material, session tokens, private URLs and personal data.
Instruction-class text is present in three captures (S037, S038, S040) and is enumerated below with
line and class; none of it is a prompt injection aimed at an agent.

Byte-level sweep, all five files: valid UTF-8, **0** control bytes (`<0x20` excluding TAB/LF/CR),
**0** DEL, **0** zero-width or bidi characters (`U+200B–U+200F`, `U+202A–U+202E`, `U+2060–U+2064`,
`U+FEFF`), **0** IP addresses, **0** `file://` or local absolute paths. HTML comments survive only as
dangling `-->` tails (e.g. `S036.txt:48,52`, `S039.txt:150`, `S040.txt:4,6,7`); the comment *bodies*
were stripped by the converter, so no text can hide in a comment. Grep for lane vocabulary
(`corpus/`, `.ufo/`, `SCORECARD`, `kasegi`, `shokunin`, `recheck:`, `source:`, `QUALITY.md`,
`agent`, `subagent`, `LLM`, `指示`, `命令`, `無視`) returned **zero hits in all five files**: no capture
contains text that names this lane, its files, or an agent.

### S036 — Cybozu 脆弱性情報ハンドリングポリシー — CLEAN

No email address, no URL, no personal name, no credential. The only instruction-like lines are
navigational, addressed by the vendor to its own reader:

| line | text (excerpt) | class |
|---|---|---|
| 31 | 「…CSIRT記述書の…ポリシー」をご参照ください。 | navigational directive (vendor→reader) |
| 45 | …下記の資料をご覧ください。 | navigational directive |
| 50 | …以下の資料をご参照ください。 | navigational directive |

L41–42 mention that contributor names are published on an 謝辞 page; the capture carries no name.

### S037 — Cybozu 脆弱性報奨金制度 FAQ — CLEAN (no credential material); 6 instruction-class lines

| line | text (excerpt) | class |
|---|---|---|
| 99 | 専用サイト（報告用サイト）にアクセスし、報告いただきます。報告にはアカウントが必要になります。 | account-gated submission instruction |
| 101 | 報告用サイトアカウントお申し込みフォームからお申込みください。 | account-application instruction |
| 103 | 脆弱性報告フォームからお申込みください。 | submission instruction |
| 106 | …こちらのフォームまたはメールでお問い合わせください。 | contact instruction |
| **123** | **報告用サイトでは脆弱性検証を行わないでください。脆弱性検証は、脆弱性検証環境提供プログラムで提供された環境をご利用ください。** | **prohibition + redirect to a vendor-provided verification environment** |
| **126** | **「ログインでお困りですか？」へアクセスし、登録済みのメールアドレスを入力してパスワードをリセットしてください。** | **login / credential-recovery instruction** |

L123 is the highest-risk instruction-like line in the round: detached from its vendor and read as a
lane rule, it says verification against a vendor environment is available and sanctioned. L126 is the
only line in any capture that tells a reader how to log in to a target-side surface; it carries no
credential value, but it must never be quoted into an entry as guidance.

Role address, public: `security@cybozu.co.jp` (L107). No personal data.

### S038 — GMO Pepabo 脆弱性報告制度 — CLEAN; 2 instruction-class lines

| line | text (excerpt) | class |
|---|---|---|
| 22 | …メールを security@pepabo.com までお送りください。…PGP もご利用いただけます。公開キーはこちらです。 | submission instruction + public-key pointer |
| 23–25 | 禁止行為 1. DoS攻撃… 2.自分自身のアカウントや情報以外へのアクセス、改ざんを試みるなどの行為 | vendor prohibition list |

L23–25 are the lines that decide whether a reader may treat Pepabo's page as authorisation; they are
a *prohibition*, so an entry that quotes them cannot manufacture permission from them. Role address,
public: `security@pepabo.com` (L22). PGP here is a public key offered to the reporter, not key
material held by the lane.

### S039 — Hitachi HIRT-PUB10008 — CLEAN

No email, no credential, no personal name. Instruction-like lines are navigational only:
L563 「各製品ページで確認してください。」, L572 「…を参照してください。」. L514 and L647/L668 refer to a
脆弱性ハンドリングに関する謝辞 page but the capture carries no name from it.

*Erratum to my own first pass:* a `LC_ALL=C grep` over a byte range flagged `S039.txt:525` as
containing a control byte. It is a false positive — the line is ordinary Japanese UTF-8 (CERT/CC and
XDR-library text) and the authoritative Python byte scan finds 0 control bytes in the file.

### S040 — Cisco Security Vulnerability Policy — CLEAN, with two named notes

| line | text (excerpt) | class / verdict |
|---|---|---|
| 48 | Hardcoded or undocumented account credentials | **false positive on a credential grep** — a policy term naming what Cisco forbids in its own products, not material |
| 79–80 | `https://cscrdr.cloudapps.cisco.com/cscrdr/security/center/files/Cisco_PSIRT_PGP_Public_Key.asc` | **public** PGP key pointer; not a private key, no credential |
| 99 | `https://mycase.cloudapps.cisco.com/start` | login-gated vendor support portal — public landing page, **no token, no query string, no session id**; not a private or session URL, but it is a login-gated surface and should not be quoted into an entry as an access route |
| 124–159 | "You will receive a confirmation email…" / "Requests to subscribe must be sent to cust-security-announce-join@cisco.com" / "You must send the messages from the email account that you want to be subscribed to" | mailing-list subscribe/unsubscribe instructions addressed to a human subscriber — instruction-class (EN); never a lane directive |
| 132 | `http://sec.cloudapps.cisco.com/security/center/rss.x?i=44` | feed id, not a token |

Emails present are role addresses only: `psirt@cisco.com` (L74, L500), `media_pr@cisco.com` (L42),
`cust-security-announce{,-join,-leave}@cisco.com`. No personal data beyond that.

**Capture-fidelity defect (not security):** `S040.txt` carries 7 `U+FFFD` replacement characters on
lines **108 (×2), 193, 203 (×1), 222 (×2), 479** — cp1252 bytes decoded with `errors=replace`, e.g.
L193 `the incident reporter�s behalf`. Verified independently here; the crosswalk entry already
declares the same five lines and states that no quote crosses them.

---

## b) QUALITY Q6 verdict per entry

Q6 reads: *documentation-only: never instructs probing, scanning, logging in to, or submitting against
any target; carries no credential material, session or private URL, or vault-reference URI (the
op-scheme form).*

| entry | version audited | credential material | session/private URL | `op://` / `vault://` | imperative against a target | **Q6** |
|---|---|---|---|---|---|---|
| `vendor-disclosure-policies-as-corpus-objects.md` | live, sha `f07a96b…` | none | none (4 public vendor pages) | none | none (0 reader-directed imperatives) | **PASS** |
| `vendor-disclosure-policy-commitments-crosswalk.md` | live, sha `d22f643…` | none | none (4 public vendor pages) | none | none (0 reader-directed imperatives) | **PASS** |
| `japanese-vendor-disclosure-policies-2026-10-23.md` | staged package | none | none (4 public vendor pages) | none | none | **PASS** |
| `vendor-cvd-policy-crosswalk-2026-10-23.md` | staged package | none | none (1 public vendor page) | none | none | **PASS** |

Every URL named by the four files, deduplicated — all public, all bare (no query, no fragment, no
userinfo):

```
https://cybozu.co.jp/company/security-policy/
https://cybozu.co.jp/products/bug-bounty/faq/
https://pepabo.com/contact/vulnerability-reporting/
https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html
https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html
```

The single grep hit for `token` in the crosswalk is L120, "Japanese quotes are counted as
whitespace-separated tokens" — a quote-counting note, not a credential.

**Selection evidence (positive).** The live JP entry quotes S037:99 (account required) and S037:123
(the prohibition) but **does not** carry S037:126, the password-reset instruction. The risky
instruction-like lines in the captures were left out of the entries, not transcribed. The one place
the live JP entry touches a target-side surface, it reports the vendor's prohibition and its own
limit — L209–211: "It instructs no probing, scanning, login or submission against any target, and
carries no credential material, session or private URL." That self-description is true of the bytes
audited here.

**Q6 note (not a failure).** `vendor-disclosure-policies-as-corpus-objects.md:87` quotes
「報告用サイトでは脆弱性検証を行わないでください。…」 and the prose then says the FAQ "point[s] to a
separately provided verification environment". That is attributed reported speech, not an imperative;
it passes Q6. It is the sentence most likely to drift into an instruction on a later edit, so a
reviewer should re-read it if the entry is amended.

---

## c) Misrooted files observed (for the L1's misroot sweep) — 2 files, both kasegi round-25 seats

Both were written under the **fleet root**, not the lane, and neither existed under the lane at the
time I observed them. I deleted nothing.

| path observed | first line | size / mtime |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/.ufo/waves/round-25/wave1/ScoutFetchCisco.md` | `# ScoutFetchCisco — independent re-fetch of the Cisco vulnerability policy` | 10978 B, 2026-10-25 05:32 |
| `/home/vgpnk/Projects/shokunin/.ufo/waves/round-25/wave1/RevD24Counts.md` | `# D24-2 — the round-24 snapshot assertion count, re-derived from committed bytes` | 13691 B, 2026-10-25 05:33 |

Evidence, verbatim. At 08:32Z the fleet root's status gained the line:

```
?? .ufo/waves/round-25/
```

and `find .ufo/waves/round-25 -type f` listed exactly the two files above. Both files declare the
lane they should have written into — `ScoutFetchCisco.md:3` "Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `b49948f1…`" and `RevD24Counts.md:3` "lane: `kasegi-shokunin`, base revision `b49948f1…`" — so this is a path-resolution defect, not a wrong-lane dispatch. At 08:24Z the same status read had no
`.ufo/waves/round-25/` line at all, and the fleet-root `.ufo/waves` directory's mtime moved to 05:27,
so the directory was created inside this review window.

Resolution, observed and not caused by me: by 08:37Z the fleet-root directory was gone
(`ls .ufo/waves/round-25/wave1/` → `No such file or directory`; the status line no longer appears,
22 entries as before), and both files exist in the lane at
`kasegi-shokunin/.ufo/waves/round-25/wave1/{ScoutFetchCisco,RevD24Counts}.md` with the same sizes and
mtimes (10978 B @05:32, 13691 B @05:33). I alerted `L1Kasegi25` at 08:33Z with the two paths and the
first lines.

**Root cause (located, smallest remediation).** `.ufo/waves/round-25/build-wave1-spec.py:83` sets

```
W1 = ".ufo/waves/round-25/wave1"
```

a lane-relative string, and `item()` at `:71–80` builds each seat's write scope from `owned` alone:

```
scope = "\n# Write scope\n" + ("READ-ONLY: no production edit. " if read_only else "") + owned + "\n"
```

`LANE` is defined at `:20` (`"/home/vgpnk/Projects/shokunin/kasegi-shokunin"`) but is never
interpolated into `item()`. Every one of the 38 dispatched task bodies in `wave1-dispatch.json`
therefore carries only `Report: write your scoped findings to .ufo/waves/round-25/wave1/<Seat>.md`
— measured over all 38, not sampled: **38/38 lack the absolute-root sentence, 38/38 lack the
`# Hard rules` block that carries it, and 0/38 contain any absolute lane path at all.** A seat whose
cwd is the fleet root resolves that relative path to the fleet root. Two of 38 did.

Smallest fix: emit the write-scope and `Report:` path as `LANE + "/" + owned` (and make `reportDir`
absolute) at `build-wave1-spec.py:73`, and re-dispatch the two seats. 35 seat `.md` files in the
lane's `.ufo/waves/round-25/wave1/` — including the two seats' files, now correctly placed — show the
rest of the wave resolved it correctly, so the lane copies are the ones to keep.

No other misroot: the fleet-root status contains no other path naming kasegi round 25. The 22 entries
are the 14 `*.report-baseline` driver files, `.ufo/watchdog.log`, `scripts/hyaku/{hyaku.env,lane-addendum.md}`,
`.omp/mcp.json`, `.scratch/goal-20261025-hyaku-12h.md`, and the three new `*.report-baseline` files —
none of them a seat artefact; `ScoutMisroot.md` reached the same disposition independently.

---

## d) Observations outside the security mandate (for the L1; no verdict attached)

1. **C2's stated reject rationale is falsified by this round's own capture.** `claims.json`
   `assimilation.planned_reject` says "vendor-cvd-policy-crosswalk-2026-10-23.md (S068 Cisco policy
   unreachable this round)". `capture-log.txt` records
   `S040 status=200 fetched_bytes=94027 snapshot_bytes=33463` for that same page, and the lane now
   holds a live crosswalk entry citing S040. The reject reason needs restating (the staged text was
   written against an unreachable page and is superseded), not "unreachable".
2. **`corpus/source-snapshots/round-25/manifest.json` does not exist** — the directory holds only
   `S036.txt … S040.txt` (`ls`). Both live entries' `recheck:` lines pass
   `--manifest corpus/source-snapshots/round-25/manifest.json`, so those rechecks fail closed today.
   I did not run `source-recheck.py` or `recheck-audit.py`; this is an `ls` observation, not a verdict
   on C1.
3. **Quote elision drops the authorisation subject.**
   `vendor-disclosure-policies-as-corpus-objects.md:102` quotes S038:17 as
   「条件を守る限りにおいて、セキュリティ研究者に対して、法的措置をとらない方針です。」, with no elision
   marker. The capture line reads 「また、**当社システムへの侵入または侵入の試みが**以下に示す条件を守る限りにおいて、
   セキュリティ研究者に対して、法的措置をとらない方針です。」. The elided clause is the only place the page says
   *what conduct* the statement covers — intrusion or attempted intrusion into Pepabo's systems.
   The quote is a verbatim substring and occurs exactly once, so it passes Q9 mechanically, and the
   entry's reading (conditional, bounded by the prohibition list) is still correct. But on the
   authorisation hinge the elision hides the subject; severity **low**, class *quote elision removing
   the authorisation subject*. Remediation: quote the whole line, or mark the elision with 「…」 and
   name the dropped clause in the prose. (`RevQuotesJP.md:68` carries the full line, so the omission is
   in the entry, not in the reviewer's table.)
4. **`S040.txt` U+FFFD damage** (7 characters, 5 lines) is a capture-fidelity defect worth an entry or
   lesson line: the capture instrument decoded cp1252 bytes with `errors=replace`. Both live entries
   already keep their quotes clear of those lines; nothing to fix in the entries.

## e) Method (reproducible)

- Digests: `sha256sum S03{6,7,8,9}.txt S040.txt` from `corpus/source-snapshots/round-25/`, compared to
  `.ufo/waves/round-25/capture-log.txt`.
- Byte sweep: Python over `read_bytes()` for control/DEL/bidi/zero-width and UTF-8 validity; line-level
  `U+FFFD` census for S040.
- Class greps: credential patterns (`AKIA`, `ghp_`, `xox[baprs]-`, `sk-…`, `api[_-]?key`, `secret`,
  `passwo?rd`, `token`, `bearer`, `authorization`, `cookie`, `BEGIN … PRIVATE`, `ssh-rsa`, `jwt`),
  `op://`/`vault://`/`keychain`/`1password`/`bitwarden`/`.env`/`id_rsa`/`.pem`; PII (`@`-addresses,
  `TEL`, `電話`, `〒`, `氏名`, `謝辞`, phone shapes); private-URL hosts (`mycase`, `cloudapps`,
  `intranet`, `localhost`, `127.0.0.1`, `192.168`, `10.`, `login`, `sso`, `auth`); injection class
  (`ignore previous`, `disregard`, `system prompt`, `you are`, `assistant`, `override`, `</system`,
  `BEGIN SYSTEM`, plus lane vocabulary); markup hiding (`<script`, `display:none`, `<!--`).
- Entry audit: header/source/verified-at/recheck/ground extraction, URL deduplication, imperative
  grep, and line-by-line re-read of every Q6-relevant quote against the capture
  (`sed -n '14p;19p;21p;22p;28p;30p;44p' S036.txt`, `'99p;109p;123p' S037.txt`, `'17p;19p;20p;24p;25p' S038.txt`).
- Misroot: `git -C /home/vgpnk/Projects/shokunin status --porcelain` (22 entries, no `kasegi-shokunin/`
  line because the fleet root gitignores `*-shokunin/`), `find` by mtime, and
  `python3` extraction of the `taskCall.tasks` prompts in `wave1-dispatch.json` to test each seat's
  task body for an absolute root.

**Unrun checks (no verdict claimed):** `recheck-audit.py` (C1) and `source-recheck.py` (entry
rechecks) were not executed by this seat; `anchorcheck` was not run. No live host was contacted by
this seat — every byte audited was already on disk.

**Tooling:** none installed or upgraded.
