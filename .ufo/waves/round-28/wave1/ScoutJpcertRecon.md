# ScoutJpcertRecon — round-28 wave-1 reconnaissance for the S041 re-capture (C2)

- seat: `ScoutJpcertRecon` (read-only recon; leaf — no subagents, no background jobs, no VCS writes)
- lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base `c9f8b115a098c65356e4b3b6048af45a37ab8395`
- owned path written: `.ufo/waves/round-28/wave1/ScoutJpcertRecon.md` (this file) — **no production file was touched**
- axis judged: coverage (C2)
- date: 2026-10-25 (all UTC timestamps)
- status: recon complete; the capture is **byte-identical** to round 26, and the document still carries
  the 2026年10月 edition stamp and the 2026.09.29 signature date. **One material finding for the
  L1** in §7: the landed entry's `recheck:` line is sound, but the *single-invocation* form of
  `--source S041 --source S042` that the round-27 carry-forward prescribes is **vacuous** —
  `source-recheck.py` takes `--source` as a single-valued argparse option and the last flag wins.

---

## 1. Instrument-UA header probe (`curl -sSIL`)

Command (run from `/tmp`; nothing written into the lane):

```
curl -sSIL --max-time 60 https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf
```

Verbatim output (2026-10-25T17:28:43Z):

```
HTTP/2 200
content-type: application/pdf
content-length: 1338665
accept-ranges: bytes
server: Apache
last-modified: Thu, 01 Oct 2026 00:49:04 GMT
date: Sun, 25 Oct 2026 17:28:43 GMT
etag: "146d29-65cbcc8478000"
x-cache: RefreshHit from cloudfront
via: 1.1 cb16dba19c772824ebc3fa0aa2d64e56.cloudfront.net (CloudFront)
x-amz-cf-pop: GIG51-P1
x-amz-cf-id: -jsMplARYVQMSVt1uaS6xf4RBbWYUEpkUWyadDXQ5PUsaM7Girzm1Q==
```

| Field | Value |
|---|---|
| status | `HTTP/2 200` |
| content-type | `application/pdf` |
| content-length | `1338665` |
| last-modified | `Thu, 01 Oct 2026 00:49:04 GMT` |
| etag | `"146d29-65cbcc8478000"` |

`content-length: 1338665` matches the instrument's `fetched_bytes=1338665` and the round-26
capture's `fetched_bytes=1338665`, so the upstream body size is unchanged across the two days.
`last-modified` (2026-10-01) postdates the PDF's own signature stamp (2026-09-29), which is
consistent with a server-side touch after signing — see §4 for what that does and does not mean.

## 2. Fresh capture vs the round-26 committed capture — IDENTICAL

Two levels were compared, because they answer different questions.

### 2a. Raw PDF bytes vs the round-26 raw-PDF digest

```
$ curl -sS -A "kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)" \
    -o $D/S041.pdf https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf
$ sha256sum $D/S041.pdf
0ff7a6b6b4fa4a9aeffa924e9a1775fbcf044773d79491e0d47aca78eb004f03  $D/S041.pdf
```

The round-26 wave-1 record already carries this digest for the same URL
(`.ufo/waves/round-26/wave1/s5-quote-relocation.txt:10`, committed):

```
sha256(PDF bytes): 0ff7a6b6b4fa4a9aeffa924e9a1775fbcf044773d79491e0d47aca78eb004f03
```

**The upstream PDF is byte-identical to the bytes round 26 fetched** — the same 64-hex digest,
not merely the same length. This is the stronger statement; it forecloses the "equal-length but
different PDF" gap that a length comparison alone leaves open.

### 2b. Text snapshot vs the round-26 committed capture (the C2-relevant artifact)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-source.py \
    --id S041 --url https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf --kind pdf \
    --out $D/S041-fresh.txt
S041 status=200 fetched_bytes=1338665 snapshot_bytes=147267 sha256=e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47 utc=2026-10-25T17:22:34Z out=/tmp/jpcert-recon-8XRo1j/S041-fresh.txt
capture_exit=0

$ sha256sum $D/S041-fresh.txt corpus/source-snapshots/round-26/S041.txt corpus/source-snapshots/round-28/S041.txt
e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47  /tmp/jpcert-recon-8XRo1j/S041-fresh.txt
e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47  corpus/source-snapshots/round-26/S041.txt
e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47  corpus/source-snapshots/round-28/S041.txt

$ cmp corpus/source-snapshots/round-26/S041.txt $D/S041-fresh.txt ; cmp_exit=0
$ cmp corpus/source-snapshots/round-28/S041.txt $D/S041-fresh.txt ; cmp_exit=0
```

**Verdict: a fresh capture IS byte-identical** to the round-26 committed capture
(`e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`, 147267 B, 2354 lines) and
to the round-28 landed copy. No divergence to diff — `cmp` exit 0 at both levels, and there is no
"first divergence" because the files are equal. This is the expected outcome given §2a: the
upstream PDF is unchanged, so the deterministic extraction is unchanged.

The round-28 landed `corpus/source-snapshots/round-28/S041.txt` already carries the same digest
(independently produced by `ExecCaptureS041`; I did not write it and did not modify it).

## 3. Edition stamp and digital-signature date — both still present

Both strings live in the capture's cover/signature block and each occurs **exactly once**.

```
$ grep -n '2026 年 10 月' corpus/source-snapshots/round-28/S041.txt
10:2026 年 10 月

$ grep -n '日付 : 2026' corpus/source-snapshots/round-28/S041.txt
7:日付 : 2026.09.29 18:01:10 +09'00'
```

| Fact | Where | Status |
|---|---|---|
| edition stamp `2026 年 10 月` | capture L10 (cover block, under the title L8–L9 `情報セキュリティ早期警戒` / `パートナーシップガイドライン`) | **confirmed**, 1 occurrence |
| signature date `2026.09.29 18:01:10 +09'00'` | capture L7 (the PDF's own signature block, L1–L7) | **confirmed**, 1 occurrence |

Independent corroboration of the signature, outside the capture text:

```
$ pdfsig $D/S041.pdf
Digital Signature Info of: /tmp/jpcert-recon-8XRo1j/S041.pdf
Signature #1:
  - Signature Field Name: Signature2
  - Signer Certificate Common Name: JPCERT Coordination Center
  - Signer full Distinguished Name: E=office@jpcert.or.jp,CN=JPCERT Coordination Center,O=JPCERT Coordination Center,serialNumber=AATL20260120431031,L=Chuo-ku,ST=Tokyo,C=JP,OID.2.5.4.97=VATJP-9010005006504
  - Signing Time: Sep 29 2026 06:01:10
  - Signing Hash Algorithm: SHA-256
  - Signature Type: adbe.pkcs7.detached
  - Signed Ranges: [0 - 352817], [391377 - 1338665]
  - Total document signed
  - Signature Validation: Signature is Valid.
  - Certificate Validation: Unknown issue with Certificate or corrupted data.
```

`Signing Time: Sep 29 2026 06:01:10` is the host-local rendering (`-03`); converting it gives
`2026-09-29T09:01:10Z`, which is the same instant as the embedded `18:01:10 +09'00'` — the two
agree exactly. `pdfinfo` adds `CreationDate: Mon Sep 28 22:54:43 2026 -03` and
`ModDate: Tue Sep 29 06:01:11 2026 -03`, one second after the signature.

**Honest scope of the signature claim:** `pdfsig` reports the cryptographic signature itself as
**Valid** (`Total document signed`). The `Certificate Validation: Unknown issue with Certificate
or corrupted data` line is the *chain*-validation status, not a signature failure — it reflects
this host's trust store not carrying the issuer chain offline. I did **not** verify the chain
against a trust root; only the embedded signature's own validity is asserted.

**One caution on the `last-modified` header.** The server advertises
`last-modified: Thu, 01 Oct 2026 00:49:04 GMT`, two days *after* the 2026-09-29 signature and
one day *after* the round-26 capture. The bytes are nevertheless identical to round 26 (§2a),
which means the server re-published the same object (a same-content copy is normal behind a CDN
or on a re-upload); the header does **not** evidence a content change. No claim is made here
about *why* the header moved.

## 4. The 起算日 footnote-4 sentence — located, with its exact anchor

**The sentence, verbatim from the capture (L340):**

> 本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。

(42 characters, ≤25 words by the lane's count convention; 9 whitespace tokens; the round-25
convention of "≤25 words / ≤70 chars" is satisfied on both readings.)

**Its structural position, resolved rather than assumed.** The capture's flattened text puts the
footnote *body* at the end of the page's block, which makes it look like it belongs to
`6) 製品開発者との直接の情報交換` (L337). It does not. The page-11 layout rendering resolves it:

```
===== PDF page 11 (printed page 9) =====
 1|                     Ⅳ．ソフトウエア製品に係る脆弱性関連情報取扱
 4|    题に関しては、付録３を参照してください。
 5|     なお、起算日4から 1 年以上経過した届出については、発見者は IPA に対し。
…
41|    6) 製品開発者との直接の情報交換
44|4
45|    本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。
46|5
47|    具体的には、「検証コード」、「画面キャプチャ」、
48|                           「ログ」等。
49|                         9
```

The marker `4` (layout L44) is the superscript attached to the **起算日** in the body text at
capture L305 (`なお、起算日4から 1 年以上経過した届出については、発見者は IPA に対し、`), which
sits under `4) 脆弱性関連情報の管理および開示` (L291) inside `２．発見者の対応` (L268). The body of
footnote 4 is the 起算日 definition; footnote 5 (`具体的には、「検証コード」…`) is the evidence
footnote. The capture's L338/L339 are the bare marker digits `4` and `5`; L340 is footnote 4's
body. **Confirmed against the document's own cross-reference**: L648 and L786 both cite the same
note as `２．注釈 4` ("the note 4 of section 2"), which is exactly the section the superscript at
L305 sits in (`２．発見者の対応`). PDF page 11 = printed page 9.

**Also confirmed — the 45-day target is measured from that same 起算日.** The clause at L648
reads `みた日（起算日、２．注釈 4 を参照）から 45 日後を目安とします。` and sits under
`3) 公表日の決定` (L643) within `４．JPCERT/CC（調整機関）の対応` (PDF p.18 = printed p.16).
`grep -c '45 日'` over the whole capture returns `2` (L648 and L786); the second occurrence is the
developer-track mirror at L786 under `5．製品開発者の対応` → `3) 脆弱性情報の公表日の調整`
(L779, PDF p.23 = printed p.21). Chapter Ⅴ (`Ⅴ．ウェブアプリケーション…`, L856) contains **no**
`起算日` and **no** `45 日` — verified by a direct scan of L856–L1154 (0 hits each), so the
lane's scope rule ("the 45-day figure belongs to the software-product track") holds on the
bytes.

**All nine `起算日` occurrences in the capture, with structure** (for the entry's line anchors):

| capture line | printed page | context |
|---|---|---|
| L305 | 9 | `なお、起算日4から 1 年以上経過した届出については…` — the footnote-4 marker, under `4) 脆弱性関連情報の管理および開示` (L291) |
| L340 | 9 | **the 起算日 definition** (footnote-4 body) |
| L430 | 12 | `IPA は、起算日から 1 年以上経過した届出について…` (IPA-side mirror, under `11) 情報非開示依頼の取下げ` L429) |
| L648 | 18 | `…（起算日、２．注釈 4 を参照）から 45 日後を目安とします…` (JPCERT/CC `3) 公表日の決定`) |
| L786 | 21 | `…（起算日、２．注釈 4 を参照）から 45 日後を目安とします…` (developer track `3) 脆弱性情報の公表日の調整`) |
| L1170, L1171, L1186, L1211 | 33–34 | 図３ flow-diagram labels `起算日の連絡` / `5 起算日の連絡` (付録２) |

The manifest's `S041` record pins six of these (`Q1`=L340, `Q2`=L212, `Q3`=L249, `Q4`=L648,
`Q5`=L1916, `Q6`=L305); I re-verified each is `occurrences=1` against the round-28 bytes
independently of the instrument, and all six resolve.

## 5. Q9 binding check on the landed round-28 manifest (informational for ExecManifest / L1)

I re-derived the Q9 facts myself rather than trusting the manifest's own `location` prose:

| Manifest quote | normalized length | occurrences in S041.txt | anchor |
|---|---|---|---|
| Q1 `本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。` | 42 | 1 (L340) | none needed |
| Q2 `ソフトウエア製品に係る脆弱性関連情報取扱の概要は、図１の通りです。` | 33 | 1 (L212) | none needed |
| Q3 `図１ ソフトウエア製品に係る脆弱性関連情報取扱の概要` | 26 | 1 (L249) | none needed |
| Q4 `みた日（起算日、２．注釈 4 を参照）から 45 日後を目安とします。ただし、` | 39 | 1 (L648) | none needed |
| Q5 `受信した旨を 7 日以内に返信することが必要となります。` | 28 | 1 (L1916) | none needed |
| Q6 `なお、起算日4から 1 年以上経過した届出については、発見者は IPA に対し、` | 40 | 1 (L305) | none needed |

All six are exactly-once, none needs an anchor, and `path` stem == `id` for both records
(`S041.txt` / `S042.txt`). The landed manifest passes:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041
S041:sha256 OK
S041:Q1 OK occurrences=1
… (Q1–Q6 all OK, occurrences=1)
exit_S041=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042
… S042:sha256 OK, S042:Q1–Q6 OK occurrences=1
exit_S042=0
```

Two notes for the record, both documentation-only (Q9 says `location` is prose the instrument
does not read):

- **`Q1`'s `location` label is imprecise.** The manifest calls it `Ⅳ．６．4) 注釈 4`. The
  footnote *body* sits physically after the `6)` heading in the flattened capture, but the note
  belongs to `２．発見者の対応` → `4) 脆弱性関連情報の管理および開示`, and the document's own
  cross-reference says `２．注釈 4`. The `location` string is not read by the instrument, so this
  is a labelling nit for `ExecManifest`, not a gate failure. The **line number L340 and the
  quote are correct**.
- The `2026 年 10 月` edition stamp is **not** among the manifest's pinned quotes, and it cannot
  be pinned as a standalone quote: normalized it is 11 characters, and `source-recheck.py`
  enforces `MIN_QUOTE_CHARS = 12` ("a shorter 'quote' matches any capture"), so a manifest
  assertion of exactly `2026 年 10 月` is refused with `reason=quote-too-short-to-be-evidence`
  and exit 2. I measured this. A compliant form is `2026 年 10 月 独立行政法人情報処理推進機構`
  (normalized 26, occurrences=1, spanning L10–L11) — I verified it resolves `OK` against the
  round-28 bytes with `anchor=10` (`anchor=10-ok`). The landed entry makes the edition claim in
  prose and cites the capture, which is the correct way round it.

## 6. Browser-UA behaviour — the round-26 registry note is now stale

`corpus/SOURCES.md:77` records, for S041: `re-fetch with capture-source.py instrument UA
(browser UA 403s); canonical anchor is the PDF`. I probed the browser-UA claim today and it
**does not reproduce** for this URL:

```
$ curl -sSIL -A "Mozilla/5.0 (X11; Linux x86_64) … Chrome/140.0.0.0 Safari/537.36" \
    https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf
HTTP/2 200 … content-length: 1338665 … etag: "146d29-65cbcc8478000"

$ curl -sS -A "<same browser UA>" -o $D/browser.pdf …   # http_code=200, size=1338665
$ sha256sum $D/S041.pdf $D/browser.pdf
0ff7a6b6b4fa4a9aeffa924e9a1775fbcf044773d79491e0d47aca78eb004f03  $D/S041.pdf
0ff7a6b6b4fa4a9aeffa924e9a1775fbcf044773d79491e0d47aca78eb004f03  $D/browser.pdf
```

Additional UA probes all returned `http_code=200`: Chrome-on-Windows, Safari-on-macOS, and bare
`curl/8.5.0`. The browser UA and the instrument UA serve the **same bytes**. The 403 in the
round-26 note belongs to the *S040* (Cisco) host — `corpus/lessons/round-26.md:104` and
`.ufo/waves/round-26/wave1/ScoutS040Probe.md:21` record `HTTP/2 403, server AkamaiGHost` for
`tools.cisco.com`; no round-26 artifact records a browser-UA probe against the JPCERT PDF
(`grep -i '403|browser|user-agent' .ufo/waves/round-26/wave1/ExecCaptureS041.md` → no hits), so
the S041 clause appears to have inherited the S040 finding.

This is a **registry-note accuracy item, not a capture defect** — the instrument UA still works
and still yields the identical bytes. `SOURCES.md` is `ScribeRegistryC2`'s file, not mine; I am
flagging it for the L1 to route. Per R8/R9 the correction belongs as an appended change-log note
(`S041 recheck cell old → new`), not a rewrite of the historical line.

## 7. **Finding for the L1 — the single-invocation `--source S041 --source S042` form is vacuous**

`corpus/lessons/round-27.md:78` (carry-forward item 3) prescribes the F12 recheck line as:

```
recheck: --source S041 --source S042 --manifest corpus/source-snapshots/round-27/manifest.json
```

That form **does not check both sources.** `source-recheck.py` declares `--source` with
`parser.add_argument("--source", …)` — a **single-valued** argparse option — so the *last* flag
wins and the earlier id is silently dropped. Measured on the landed round-28 manifest:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 --source S042
S042:sha256 OK
S042:Q1 OK occurrences=1
… (only S042 lines; S041 is never checked)
exit=0
```

And the discriminating control — corrupt S041, then compare the two forms:

```
### A) two --source flags in ONE invocation (S041 first) on a CORRUPTED S041:
S042:sha256 OK
S042:Q1 OK occurrences=1
exit=0                      ← S041's corruption is INVISIBLE

### B) chained invocations on the same CORRUPTED S041:
S041:sha256 MISMATCH expected=e18acbf99… actual=2fb2b493…
exit_S041=1                 ← corruption is caught
S042:sha256 OK / exit_S042=0
```

The same gap reproduces at harness level. I built a throwaway lane root in `/tmp` with a
minimal `corpus/README.md` F12 row and a two-source entry, then ran the *real*
`frontier-recheck-count.py` against it:

```
--- S041 CORRUPTED, single invocation with two --source flags:
PASS     F12  knowledge/test-entry.md   ids=S041,S042   exit=0
entries=1 pass=1 exit=0                  ← harness PASSES on a corrupted S041

--- same corrupted S041, chained recheck line:
FAIL     F12  knowledge/test-entry.md   ids=S041,S042   exit=1  problems=recheck-exit-1
entries=1 pass=0 exit=1                  ← harness FAILS, as it should
```

The harness's own regex `RECHECK_SOURCE = re.compile(r"--source\s+(S\d{3,})")` finds **both** ids
in either form, so the harness's *declared-id* bookkeeping says `ids=S041,S042` in both cases and
cannot tell them apart; the difference shows up only in what the instrument actually executed.
That is precisely the r24 "all eight Frontier entries pointed at `--source S018`" failure class
recurring in a new shape: **a recheck line that appears to cover two ids while covering one.**

**Good news: the landed entry already uses the sound form.** `corpus/knowledge/japanese-domestic-disclosure-workflow.md:7`
is a chain of two invocations, each with its own `--source`:

```
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042
```

Verified: `bash -n` parses it (exit 0); it exits 0 from a foreign cwd (`/tmp`) — satisfying Q10's
`cd <lane-root> &&` requirement; and it is the form my corruption control catches. The
round-28 lane is therefore **not** exposed to this gap. The defect is latent in the *carry-forward
wording*, so it will bite whichever future entry copies the round-27 prescription verbatim. I
recommend the L1 record the chained form as the canonical multi-source recheck shape (it is also
what all 8 existing multi-source entries in the lane already do — `grep '^recheck:' corpus/knowledge/*.md`
shows 8 entries chaining `--source` invocations with `&&`, and **zero** use the single-invocation
two-flag form).

**Re-run command for the L1 (post-change), for the record:**

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 && \
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042 && \
  python3 corpus/instruments/frontier-recheck-count.py
```

All three were run against the current lane state: `exit_S041=0`, `exit_S042=0`, and the harness
reports `entries=15 pass=15 exit=0` (F12 among the 15 PASS rows, `ids=S041,S042 exit=0`).

## 8. Files read / written / not touched

**Written:** `.ufo/waves/round-28/wave1/ScoutJpcertRecon.md` (this file) and
`.ufo/waves/round-28/receipts/ScoutJpcertRecon.txt` (my own per-seat receipt) — nothing else.

**Read:** `.ufo/waves/round-28/claims.json`; `corpus/QUALITY.md`; `corpus/SOURCES.md`;
`corpus/README.md`; `corpus/lessons/round-27.md`; `corpus/lessons/round-26.md`;
`corpus/instruments/{capture-source.py,source-recheck.py,frontier-recheck-count.py}`;
`corpus/source-snapshots/round-26/{manifest.json,S041.txt}`;
`corpus/source-snapshots/round-28/{manifest.json,S041.txt,S042.txt}`;
`corpus/knowledge/japanese-domestic-disclosure-workflow.md`;
`.ufo/waves/round-26/wave1/{s5-quote-relocation.txt,ExecCaptureS041.md,ScoutS040Probe.md}`;
`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md`
(read-only). For §10, read-only lookups in the souji lane and the fleet run-state file.

**Not touched:** `corpus/instruments/anchorcheck.py`, `corpus/instruments/README.md`, `SKILL.md`,
`corpus/source-snapshots/round-28/*` (S041.txt, S042.txt, manifest.json),
`corpus/knowledge/japanese-domestic-disclosure-workflow.md`, `corpus/SOURCES.md`,
`corpus/README.md`, `corpus/QUALITY.md`, `corpus/lessons/round-28.md`, `LOG.md`, `SCORECARD.md`,
`.ufo/waves/round-28/claims.json`, any round-27 artifact, any file in the souji lane, the fleet
root, and any VCS state (no `git`/`jj` write was issued; `git status`/`ls-files` were read-only).

**Toolchain:** `curl` (system), `pdftotext` 26.08.0 (`/usr/bin/pdftotext`, poppler — pre-existing),
`pdfsig`/`pdfinfo` (poppler-utils, pre-existing), `python3` 3.14.8, `cmp`/`sha256sum`/`grep`.
**No tool was installed or upgraded; no pacman transaction was attempted** (host-wide pacman
pause in force). All scratch artifacts lived under `/tmp/jpcert-recon-8XRo1j/` and
`/tmp/harness-test-*`, outside the lane, and were removed at the end of the seat.

## 9. Summary of findings

| # | Finding | Evidence | Severity for C2 |
|---|---|---|---|
| F1 | Fresh capture is **byte-identical** to the round-26 capture (sha256 `e18acbf99…`, `cmp` exit 0) | §2b | none — C2's premise holds |
| F2 | Upstream **PDF bytes** are also identical to round 26 (`0ff7a6b6…`) | §2a | strengthens F1 |
| F3 | Edition stamp `2026 年 10 月` present at L10; signature date `2026.09.29 18:01:10 +09'00'` present at L7; `pdfsig` signature **Valid** | §3 | none |
| F4 | 起算日 footnote-4 sentence located at **L340** (printed p.9, PDF p.11); its marker `4` attaches to L305 under `２．発見者の対応` → `4) 脆弱性関連情報の管理および開示`; the document's own cross-ref says `２．注釈 4` | §4 | none — anchor is sound |
| F5 | The 45-day target measures from the same 起算日 (L648, L786); `45 日` count = 2, both in chapter Ⅳ; chapter Ⅴ has 0 `起算日` and 0 `45 日` | §4 | none |
| F6 | Manifest `Q1.location` label says `Ⅳ．６．4)`; the note belongs to `２．注釈 4` (`location` is prose the instrument does not read) | §5 | cosmetic; route to `ExecManifest` |
| F7 | The edition stamp cannot be a standalone manifest quote (11 normalized chars < `MIN_QUOTE_CHARS=12`) | §5 | cosmetic; the landed entry cites it in prose instead |
| F8 | `SOURCES.md:77`'s "browser UA 403s" for S041 **does not reproduce** (200 + identical bytes for 4 different UAs); the 403 belongs to the S040 Cisco host | §6 | registry-note accuracy; route to `ScribeRegistryC2` via an R8/R9 appended change note |
| F9 | **`source-recheck.py --source` is single-valued (last flag wins).** The round-27 carry-forward's `--source S041 --source S042` single-invocation form checks only S042 and passes on a corrupted S041; the harness cannot distinguish the forms. The **landed entry already uses the sound chained form**, so the round-28 lane is not exposed | §7 | **latent defect in the carry-forward wording**; L1 should record the chained form as canonical |

**Confidence.** F1–F5, F7–F9 are measured on the live bytes and the committed files, with
commands and verbatim outputs shown; confidence high. F6 is a reading of the document's own
cross-reference against the capture's physical layout — high, but the disposition (whether to
amend `location`) is `ExecManifest`'s call, not mine.

## 10. Addendum — cross-lane peer message received after the report body

After §9 was written, `SoujiR27` sent two IRC messages to this seat asking for a dispatch /
handoff. Facts established before answering (read-only; **nothing in the souji lane was
written by me**):

- **`SoujiR27` is the souji lane's r27 L1, not a kasegi seat.** It appears in no round-28
  artifact: `grep -c 'SoujiR27'` over `.ufo/waves/round-28/` returns 0, it is absent from
  `wave1/swarm-registry.json` (69 members, none named Souji*), and it appears nowhere in the
  fleet tree except the orchestrator's own run-state file
  `/home/vgpnk/Projects/shokunin/.scratch/goal-20261025-hyaku-run7.md:70-71`:
  *"souji r27 L1 spawned inline (SoujiR27) — it twice stalled thinking the orchestrator supplies
  claims/ready files; told it owns claims+spec+ready. L1 prompt now states 'YOU write the
  .ready file'."* This is the **third** stall on the same premise.
- **The mechanic it was waiting for needs no sibling.** `scripts/hyaku/lane-addendum.md` §6
  (run-7 binding, "Inline spawn handoff") states the L1 writes its own `<wave>.ready`; the
  operator session's dispatcher polls it within ~15 s, writes `<wave>.ready.dispatched`, spawns
  the seats inline, and messages `WAVE-DONE <wave> … results=<path>` once they settle. There is
  no "observe the ready file" step to wait on — the dispatcher's poll *is* the launch, and no
  message arrives before the seats exist.
- **Measured lane state:** `souji-shokunin/.ufo/waves/round-27/` existed but was **empty** (no
  spec, no dispatch, no ready file). Its own lane's round-26 carries the working trio to copy:
  `souji-shokunin/.ufo/waves/round-26/{make-spec.py,w1-spec.json,w1-dispatch.json,w1.ready,
  w1.ready.dispatched,w1/}`, with `w1.ready` = `{"lane":"souji","round":26,"wave":"w1",
  "dispatch":".../round-26/w1-dispatch.json","l1":"SoujiR26"}`.

**Action taken:** I replied to `SoujiR27` directly with the exact paths, the ready-file JSON
shape, the "write it yourself, then call `wait`" instruction, and the correction that nothing
will message it before its seats exist. I also relayed the item to `Main` (the kasegi r28 L1),
flagging that the durable fix belongs in the L1 prompt text the orchestrator issues to that seat.
**Not done, by design:** I did not dispatch it (leaf seat, kasegi-only write scope, no
orchestration-runtime authority), did not write any file in the souji lane, and made no dispatch
decision for another lane.

**Observed after the reply:** `souji-shokunin/.ufo/waves/round-27/` gained an `assimilation/`
subdirectory — the seat resumed producing round-27 artifacts. The round-27 spec, dispatch and
`.ready` file were still absent when I finished; whether the wave lands is `SoujiR27`'s and the
operator session's to complete, not mine.

**Effect on this seat's deliverable:** none. The C2 S041 findings in §1–§9 are unaffected; the
addendum records the peer coordination only. The second file this seat wrote is
`.ufo/waves/round-28/receipts/ScoutJpcertRecon.txt`.
