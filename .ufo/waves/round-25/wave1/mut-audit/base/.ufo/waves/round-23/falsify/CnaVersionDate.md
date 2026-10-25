# R23 falsify — F07 CNA Rules version, dates, and the 4.1.10→4.1.9 claim

Seat: `L1Kasegi23.CnaVersionDate-2` (leaf, no dispatch). Date: 2026-10-25.
Target as assigned: open `corpus/source-snapshots/round-23/S030.txt`, confirm the
approved/effective dates and document version, test the entry claim that independently-fixable
guidance moved from §4.1.10 (v4.1.0) to §4.1.9 (v4.2.0), and rule on whether the entry's
`current` claim is properly date-bounded. Note the registry `opened` date against the entry's
`verified-at`.

Read-only. No production file, lane tree, sibling lane, or git/jj index/state was written. Only
this report was written, plus scratch under `/tmp/kasegi-r23-falsify-CnaVersionDate/`. No commit,
no push. No installs: `curl`, `pdftotext` (poppler, already present), `sha256sum`, `python3` were
used as installed; no package transaction was attempted (pacman is paused host-wide anyway).

All paths below are relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless absolute.

## Verdict in one paragraph

The three pinned header facts are correct and reproduce upstream v4.2.0 exactly. The
`4.1.10 (v4.1.0) → 4.1.9 (v4.2.0)` claim is **true upstream**, but its 4.1.0 half has **zero
pinned corpus support**: no v4.1.0 bytes exist in this corpus, and the S022 registry row records
no §4.1.10. The entry's `current` claim (`knowledge/cna-assignment-and-vulnerability-rules.md:14`,
"the public document's current version … is 4.2.0") is **falsified**: CNA Operational Rules
**v4.2.6** (approved 2026-10-14, effective **2026-10-20**) is live on cve.org, that site says
v4.2.0 "has been deprecated", and the v4.2.6 PDF was published at 2026-10-20 18:15:24 GMT —
**before** the S030 capture file's recorded write time of 2026-10-20 21:38:49 GMT. So the
`current` sentence was already false on its own `verified-at` date, not merely stale five days
later. In v4.2.6 the entry's load-bearing §4.2.11 quote also changed modality from SHOULD to MUST.

## 1. Version and dates — confirmed (S030 excerpt is a faithful v4.2.0 capture)

| fact | pinned excerpt | fresh upstream v4.2.0 PDF (`pdftotext -layout`, my GET) |
|---|---|---|
| version | `S030.txt:12` `#### Version: 4.2.0` | `Version: 4.2.0` |
| approved | `S030.txt:14` `#### Approved date: 2026-August-20` | `Approved date: 2026-August-20` |
| effective | `S030.txt:16` `#### Effective date: 2026-August-25` | `Effective date: 2026-August-25` |

The excerpt is not merely self-consistent: all seven manifest-pinned S030 quotes were matched
against the freshly downloaded official v4.2.0 PDF text (whitespace-normalised, `<u>` tags
stripped) — **7/7 present**. Replay in §6. So the capture reproduces real upstream v4.2.0
sentences, and `sha256(S030.txt) = 673526db7c2b4fde2a9682c6a2b8fca3ebb0ff9d4423c0559483f4540c5ab019`
equals the manifest pin.

## 2. The `4.1.10 (4.1.0) → 4.1.9 (4.2.0)` claim — TRUE upstream, HALF-UNPINNED locally

Entry line: `knowledge/cna-assignment-and-vulnerability-rules.md:17` —
"independently fixable guidance moved from 4.1.10 in 4.1.0 to 4.1.9 in 4.2.0."

- **4.2.0 half — verified from pinned bytes.** `S030.txt:165` is
  `4.1.9 To help determine whether separate Vulnerabilities exist, CNAs SHOULD consider whether the Vulnerabilities are <u>Independently Fixable</u>.`
  Immediately below it, `S030.txt:166` is `4.1.10 Interdependent conditions that cause a
  Vulnerability SHOULD be determined to be one Vulnerability.` — i.e. the number 4.1.10 in
  v4.2.0 is a **different rule**. The claim's section-number assertion is correct.
- **4.1.0 half — not verifiable from this corpus.** `corpus/source-snapshots/` contains only
  `round-23/` with S018/S029/S030; no v4.1.0 bytes exist anywhere under `corpus/`
  (`grep -rl "Version: 4.1.0" corpus/` → no files). The S022 row (`corpus/SOURCES.md:28`) records
  only "Sections 3.1 and 4.1; effective and approved 2025-05-14" — no §4.1.10, no quote. The C2
  manifest (`manifest.json`) pins S030 quotes only. So the first half rests on an unpinned
  assertion in an entry whose own warning is "never reuse old section numbers blindly".
- **Independent upstream test (I fetched the official v4.1.0 PDF, 250,107 bytes,
  sha256 `9c55618efcc632b2b498e87ecf8eb9dcc2c724754b6bfacf5270f6b606b29cf0`):**
  `v410.txt:431` (line in my `pdftotext -layout` extraction; §6) reads `4.1.10 To help determine whether separate Vulnerabilities exist, CNAs
  SHOULD consider whether the Vulnerabilities are Independently Fixable.` (page 12). Sentence
  text is **byte-identical** to v4.2.0 §4.1.9 apart from the section number — I compared the two
  extracted sentences programmatically: `IDENTICAL`. The claim is therefore **true**, but only
  provable by going outside the pinned corpus.
- **Why the number moved (mechanism, verified).** v4.1.0 had `4.1.3 Well-documented or
  commonly-understood non-default configuration … SHOULD NOT be determined to be
  Vulnerabilities.` as a top-level rule (`v410.txt:396-397`). v4.2.0 demoted that rule to
  sub-rule `4.1.3.5` (`v420.txt:457-458`) under an expanded `4.1.3` insecure-defaults rule, which
  collapses every following 4.1.x number by one. That is also why `4.1.15` (`v410.txt:454` in v4.1.0; the 4.2.6 revision
  history records "Added 4.1.15" at `v426.txt:1070`) becomes `4.1.14` in 4.2.0 — and why v4.2.0's
  `4.2.9` still says "guidance in 4.1.15" (`S030.txt:206`) for a section that no longer exists.
  That dangling cross-reference exists **upstream** too (`v420.txt:608`), so the excerpt is
  faithful; it is an upstream editorial defect, not a capture defect.
- **Still true in the actually-current version:** v4.2.6 §4.1.9 is the same independently-fixable
  rule (`v426.txt:462-463`). The renumbering claim survives; only its currency framing
  does not.

## 3. FALSIFIED — the entry's `current` claim was already superseded on its own date

Entry lines: `:14` "The public document's **current version** opened this round is 4.2.0.";
`:21` "All quotes below are from S030, version 4.2.0, opened 2026-10-20"; header `:3`
`verified-at: 2026-10-20`.

Observed facts (all reproduced today, 2026-10-25):

1. `https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf` is a real PDF:
   `HTTP/2 200`, `content-type: application/pdf`, `content-length: 271367`,
   `last-modified: Tue, 20 Oct 2026 18:15:24 GMT`, `etag: "dccb6759e795f420bec63a9a40ae4a47"`,
   sha256 `e296c9376cabcd09879f03920d99bb17e545a0e9c270d94478e45eda99677a22`, 27 pages.
   Its title page: `Version: 4.2.6`, `Approved date: 2026-October-14`,
   `Effective date: 2026-October-20` (`v426.txt:1-8`).
2. cve.org's own site text (inside the hashed SPA bundle the site serves) carries the CVE
   Program news item titled **“CNA Rules v4.2.6” Now in Effect**, `date:`2026-10-20``:
   "The … CNA Operational Rules Version 4.2.6 took effect on October 20, 2026 … The previous
   version, CNA Rules v4.2.0, **has been deprecated**. CNAs are now required to comply with the
   CNA Rules v4.2.6."
3. Version probes distinguish real PDFs from the SPA catch-all, with a negative control:
   `CNA_Rules_v4.2.1/.2/.3/.4/.5.pdf` and `CNA_Rules_v9.9.9-nonexistent.pdf` all return
   `HTTP/2 200`, `880` bytes, `text/html` (the SPA shell) — so HTTP status proves nothing by
   itself; only `v4.2.6` and `v4.2.0`/`v4.1.0` return `application/pdf` magic bytes. No 4.2.1–4.2.5
   PDF is published; there is no gap between the pinned 4.2.0 and the current 4.2.6.
4. **Timing against the entry's own bound.** Host TZ is `-03` (`date -Is` →
   `2026-10-25T03:39:55-03:00`). `stat` gives
   `S030.txt` mtime `2026-10-20 18:38:49 -0300` = **21:38:49 GMT**; `SOURCES.md` mtime
   `2026-10-20 18:45:49 -0300` = 21:45:49 GMT. v4.2.6 was published at **18:15:24 GMT**. The
   capture and the registry row were therefore written **3h23m and 3h30m after** the successor
   existed. The 4.2.0 sale was already over when "4.2.0 is current" was recorded.
5. **The `current` wording is duplicated in the registry, not only the entry.**
   `corpus/SOURCES.md:36` (S030): scope "…in version 4.2.0"; anchor "Approved 2026-08-20,
   effective 2026-08-25…"; teaches "supersedes S022 — **use current 4.2.0 requirements** and
   section numbering…"; `opened` `2026-10-20`; recheck `on-release`.
6. **Registry `opened` vs entry `verified-at`: identical — `2026-10-20` in both**
   (`SOURCES.md:36` col `opened`; entry `:3` `verified-at:`). There is no later re-open recorded.
   Because the row's cadence is `on-release` and a release landed on 2026-10-20, the recheck
   trigger had already fired on the day the row was opened.
7. **A superseding normative change the entry now misquotes.** Entry `:30` tabulates
   `4.2.11, page 15 | “CNAs SHOULD assign different CVE IDs to different, Independently Fixable
   Vulnerabilities.”` v4.2.0 does say SHOULD (`S030.txt:211`). Current v4.2.6 §4.2.11,
   page 15 of 27, says **MUST**: `4.2.11 CNAs MUST assign different CVE IDs to different,
   Independently Fixable Vulnerabilities.` (`v426.txt:573-574`). The other six table
   quotes (3.1.1, 3.1.4, 4.1.2, 4.1.9, 4.2.1.1, 4.2.12) are still literally present in v4.2.6.
   So identifier counting under the current rule is mandatory, not advisory — a consequence the
   entry's row ("Count vulnerabilities, not changed files or commits.") does not carry.
8. **The falsifier was already inside this wave's evidence set, unused.**
   `.ufo/waves/round-23/build/CnaFix.md` (mtime `2026-10-20 18:47:40 -0300`) states the same
   v4.2.6 finding at its lines 17-25, including the same PDF sha256 `e296c937…`. It is **1 of the
   44** `.ufo/waves/round-23/build/*.md` reports (the only one mentioning "4.2.6"), and
   `corpus/lessons/round-23.md` attempt 2 lists the 44 inherited build reports among
   "Reused after re-verification". Yet `grep -rn "4\.2\.6" corpus/ corpus/lessons/round-23.md`
   returns nothing but S030's unrelated §4.2.6 sentence: the admission record never discloses the
   supersession, and the entry/row still say 4.2.0 is current.

## 4. Is the `current` claim properly date-bounded? No — bounded in form, false at the bound

- Formal bounding exists but is weak: a bare `verified-at: 2026-10-20` header plus the phrase
  "opened this round" (`:14`, `:21`). The sentence itself carries no as-of date and no successor
  effective date; a reader quoting `:14` alone gets an unbounded freshness assertion.
- The bound is **factually wrong**, not merely expired: the supersession (effective date, site
  notice, and file publication 18:15:24 GMT) all precede the capture's recorded 21:38:49 GMT
  write. "Bounded to 2026-10-20" cannot rescue the sentence; 2026-10-20 is the day 4.2.0 died.
- The `Limits` paragraph (`:65-68`) disclaims *the recheck instrument's* freshness ("proves
  captured-source support only, not current online freshness"), and `manifest.json`'s `purpose`
  says the same. That disclaimer covers the pin, **not** the prose assertion at `:14`, which says
  "current version". Q1's `verified-at` and R1's as-of requirement are satisfied mechanically
  while the assertion they bound is false.
- Today the claim is 5 days stale; the registry `on-release` recheck shows no recorded re-open
  against the 2026-10-20 release.

**Falsifiable statement (red-before).** Freeze the predicate: "On 2026-10-25 the newest official
CNA Operational Rules PDF linked by cve.org is `CNA_Rules_v4.2.0.pdf` and its effective date
exceeds 2026-10-20." Run the probes in §6. Red-before result: the predicate is false on four
independent bytes — the v4.2.6 `application/pdf` body, its `last-modified`, its title page, and
the site's deprecated-successor notice.

## 5. What survives untouched

- S030's version/approved/effective lines and all seven manifest quotes: **correct for v4.2.0**;
  `source-recheck.py --source S030` exits 0.
- The `4.1.10 → 4.1.9` sentence: **true upstream**; and it is still true under v4.2.6.
- Entry page attributions `3.1.1 p7, 3.1.4 p7, 4.1.2 p11, 4.1.9 p12, 4.2.1.1 p13, 4.2.11 p15,
  4.2.12 p15` all verified against the upstream v4.2.0 PDF page-by-page; 4.2.11 is page 15 in
  v4.2.6 as well.
- The excerpt's dangling `4.1.15` reference (`S030.txt:206`) is an **upstream** defect present in
  both v4.2.0 and v4.2.6; do not "fix" it in the pin.
- Overlap disclosure: `falsify/S030Quotes.md` F5 already records entries L14/L17 as holding
  against S030. That check is scoped to the pinned v4.2.0 bytes and cannot see currency. This
  report is the currency half; the dates/section-number confirmations here are recomputed
  independently, not borrowed.

## 6. Replay (exact commands, run 2026-10-25, scratch `/tmp/kasegi-r23-falsify-CnaVersionDate/`)

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/source-snapshots/round-23/S030.txt
python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-23/manifest.json --source S030
grep -n "Version:\|Approved date\|Effective date\|4\.1\.9\|4\.1\.10\|4\.1\.15" \
  corpus/source-snapshots/round-23/S030.txt
stat -c '%y %n' corpus/source-snapshots/round-23/S030.txt corpus/SOURCES.md
date -Is
grep -rl "Version: 4.1.0" corpus/            # no output: no v4.1.0 bytes in the corpus
grep -rn "4\.2\.6" corpus/                   # only S030 §4.2.6, no v4.2.6 rules notice

mkdir -p /tmp/kasegi-r23-falsify-CnaVersionDate && cd $_
curl -sS -o v410.pdf https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.1.0.pdf
curl -sS -o v420.pdf https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.0.pdf
curl -sS -o p4.2.6.bin https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf
curl -sSI https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf | grep -iE \
  '^(HTTP|content-type|content-length|last-modified|etag)'
pdftotext -layout v410.pdf v410.txt; pdftotext -layout v420.pdf v420.txt
pdftotext -layout p4.2.6.bin v426.txt
grep -nE "^\s*4\.1\.1[0-9] " v410.txt      # 4.1.10 = Independently Fixable, p12
grep -nE "^\s*4\.1\.[0-9]+ " v420.txt      # 4.1.9 = Independently Fixable; 4.1.10 = interdependent
sed -n '1,8p' v426.txt                     # 4.2.6 / 2026-October-14 / 2026-October-20
sed -n '570,576p' v426.txt                 # 4.2.11 MUST ...
sha256sum p4.2.6.bin v420.pdf
curl -sS https://www.cve.org/assets/index-BYO9YwiF.js -o spa.js
grep -o ".\{300\}took effect on October 20, 2026.\{100\}" spa.js
for v in 4.2.1 4.2.2 4.2.3 4.2.4 4.2.5 4.2.6 9.9.9-nonexistent; do
  curl -sS -o /dev/null -w "v$v %{http_code} %{size_download} %{content_type}\n" \
    "https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v$v.pdf"; done
```

Key outputs observed:

```
S030:sha256 OK
S030:rule-3-1-1-scope-definition OK … S030:rule-4-2-12-uncertainty OK      (exit 0, 7/7 quotes)

S030.txt:12  #### Version: 4.2.0
S030.txt:14  #### Approved date: 2026-August-20
S030.txt:16  #### Effective date: 2026-August-25
S030.txt:165 4.1.9  To help determine whether separate Vulnerabilities exist, …
S030.txt:166 4.1.10 Interdependent conditions that cause a Vulnerability …
S030.txt:206 … guidance in 4.1.15.          (4.1.15 absent from the document)
S030.txt:211 4.2.11 CNAs SHOULD assign different CVE IDs to different, Independently Fixable Vulnerabilities.

2026-10-20 18:38:49.613531319 -0300 corpus/source-snapshots/round-23/S030.txt
2026-10-20 18:45:49.156998491 -0300 corpus/SOURCES.md
2026-10-25T03:39:55-03:00   -03-0300

v4.2.6: HTTP/2 200, application/pdf, content-length 271367,
        last-modified: Tue, 20 Oct 2026 18:15:24 GMT, etag "dccb6759e795f420bec63a9a40ae4a47"
p4.2.6.bin  e296c9376cabcd09879f03920d99bb17e545a0e9c270d94478e45eda99677a22
v420.pdf    7be61b7fc082c1b388510589d7e2ba86e7b96f908b19fab889e7e9c847b31039
v410.txt:431     4.1.10 To help determine whether separate Vulnerabilities exist, …
v426.txt:573     4.2.11 CNAs MUST assign different CVE IDs to different, Independently Fixable
v4.2.1…4.2.5 + v9.9.9-nonexistent: 200, 880 bytes, text/html   (SPA catch-all — status proves nothing)
```

## 7. Consequence for L1 (reported, not applied)

Minimum accurate repair, if the wave wants a currency-clean F07:

1. A **new** registry row `supersedes S030 —` for v4.2.6 (approved 2026-10-14, effective
   2026-10-20) rather than editing S030's immutable `source`/`scope`/`anchor` fields (R8); log any
   S030 `status`/`recheck`/`used-by` change.
2. Re-open + re-pin v4.2.6 (its §4.2.11 is MUST) and restate entry `:14`/`:17` with an explicit
   effective-date bound, e.g. "4.2.0 was current 2026-08-25 … 2026-10-19; v4.2.6 took effect
   2026-10-20".
3. Keep the `4.1.10 → 4.1.9` sentence but mark its 4.1.0 half as fetched-not-pinned, or add the
   v4.1.0 §4.1.10 capture to the manifest so Q3 has a local quote for it.

## 8. Scope limits

- I did not audit v4.2.6 as a whole: I opened only the title page, §3.1.1/3.1.4, §4.1.x, §4.2.9,
  §4.2.11-4.2.13 and the revision history. Other 4.2.6 changes (e.g. the mandatory §4.2.6
  separateness rule noted in `build/CnaFix.md`) are outside this seat.
- Timestamps are the recorded artifact times (`stat` mtime, HTTP `last-modified`), not proof of
  the author's clock; the intra-day ordering argument is therefore stated as "all recorded times
  are after publication", which is what the bytes support. It does not require an hour-level
  claim about when the author typed.
- `cve.org/Resources/Roles/Cnas` and `/ResourcesSupport/AllResources/CNARules` are JavaScript
  SPA shells (880-byte HTML); the rules/news text quoted from `spa.js` is the site's own shipped
  bundle, not a second authority. Its bundle name (`index-BYO9YwiF.js`) is build-hashed and can
  change without notice — the PDF body, its `last-modified`, and its title page are the load-
  bearing evidence; the bundle corroborates the deprecation wording.
- One GET per URL in my scratch; the sha256 above is from my single fetch. Two-GET stability was
  not re-run here (a sibling seat reports it; not relied on).
- I make no admission or score-movement claim; this seat only reports falsified and surviving
  claims about the bytes under test.
