# SOURCESRows — round-24 SOURCES append block (executor, private clone)

Clone: `/tmp/kasegi-r24-SOURCESRows` (never the lane registry). Only `corpus/SOURCES.md` modified
(`git diff --stat` → `corpus/SOURCES.md | 6 ++++++`, 6 inserted lines: 4 registry rows, 1 Paths
bullet, 1 Search-log bullet). No commit, no jj, no push.

Clone tip `c2480b1` ("round-23 verifier spot-check (integrator, hyaku): non-author admit/reject");
contract base `d0a3f6a…` is an ancestor (`git merge-base --is-ancestor` → true) and
`git diff --stat d0a3f6a..HEAD -- corpus/SOURCES.md corpus/README.md` is empty, so the registry I
built on is byte-identical to the frozen base.

## Findings

1. **The renumber map named in the dispatch does not exist.** `ls` of
   `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/assimilation/` holds only
   `census-before.txt`, `collisions` (=`S031`), `reg-ids` (S001–S031), `staged-ids`
   (S031–S124); `find … -name '*renumber*'` returns nothing, and
   `grep -n 'renumber' .ufo/waves/round-24/wave1*` matches only my own dispatch prompt. The map
   below is **reconstructed** from those three artifacts plus the dispatch sentence it was meant
   to encode; it is UNVERIFIED against any L1-authored artifact. Recorded as a routed gap.

2. **Reconstructed map = `lane_id = staged_n + 1` for every staged id.** Evidence: `reg-ids`
   ends at S031; `staged-ids` starts at S031; `collisions` = `S031` (single collision, at the
   block's first id). A +1 offset over the whole staged block therefore clears the lane's S031
   *and* leaves no future collision (highest staged S124 → S125). It also means lane ids
   S032–S039 are reserved-but-unallocated: if another seat adopts staged S031–S038 this round,
   those land at S032–S039 and nothing here moves.

3. **Adopted entries cite four staged ids → four lane rows.** Package
   `authorised-testing-rules-of-engagement.md:2` cites `S123`; package
   `statutory-authorization-in-three-traditions.md:4-6` cites `S039`, `S040`, `S041`. Under the
   map: S123→**S124**, S039→**S040**, S040→**S041**, S041→**S042**. All four URLs are new to the
   lane (`grep -c` of each URL in the built `corpus/SOURCES.md` = 1, so no E04/W04 duplicate was
   introduced; the only W04s in the receipt are the two pre-existing r23 ones, which already
   appear in `.ufo/waves/round-24/assimilation/census-before.txt`).

4. **C2 counter B cannot reach its frozen target of 2 under this map.**
   `grep -lE '^source: S1[0-9][0-9] ' corpus/knowledge/*.md | wc -l` = **1** both with the entries
   as staged and after applying the map to the entries (measured in
   `/tmp/kasegi-r24-SOURCESRows-fixture` and `/tmp/kasegi-r24-c2check`). Only the RoE entry cites
   an S1xx row (S124); the statute entry's rows land at S040–S042. The claim's
   `after_target_B: 2` presumes adopted ids land in the S1xx band, which the +1 map does not
   produce. **Do not bend the numbering to the counter** — either the counter's form is wrong
   (rows-first-registered-this-round is the predicate's actual test, and all four qualify) or C2
   lands short as an honest stop. This needs L1's ruling before scoring.

5. **Verbatim package rows fail the fleet schema.** Feeding staged S123's row into the registry
   unchanged (id renamed only) yields
   `file\tE09\tS124 recheck=90d — re-fetch the PDF and \`grep -F\` the four lines (ran 2026-10-24)`,
   validate rc=1 (`/tmp/kasegi-e09`). The prose clause after the cadence is the E09 trigger; it was
   stripped to `90d` and the "re-fetch the PDF and `grep -F` the four lines (ran 2026-10-24)"
   clause is preserved in the scratch note below. The other three rows already carried bare
   `730d`.

6. **One package teaching was misquoted and is corrected.** Staged S040 (MIC page) taught "using a
   computer you have no **使用権限** for"; the page's bytes say **利用権限**
   (`使用権限` absent, `利用権限` present in the 不正アクセス行為 definition paragraph). The row now
   uses `利用権限`. Verified against the fetched page, not the package text.

7. **All four rows were re-opened by this lane today** (documentation-only discipline: public
   documents read with `curl`, nothing contacted beyond them), so `opened 2026-10-25` is this
   lane's own access, not the package's transcription:

   | row | URL | HTTP | bytes | located quote re-read |
   |---|---|---|---|---|
   | S040 | `https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128` | 200 | 36 058 | 第十一条 … 三年以下の拘禁刑又は百万円以下の罰金; アクセス管理者 present |
   | S041 | `https://www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/` | 200 | 85 874 | 第十一条 … 三年以下の懲役又は百万円以下の罰金 (still 懲役) |
   | S042 | `https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf` | 200 | 477 938 | アクセス管理者又は…利用権者の承諾を得て行う場合は禁止の対象から除外しています |
   | S124 | `https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf` | 200 | 544 047 | Rules of Engagement (ROE): Detailed guidelines and constraints…; The ROE is established before the start of a security test…; Appendix B provides a template… |

   Note: `pdftotext` on SP 800-115 yields 250 145 characters here versus the package's 271 214 —
   different extractor, not a contradiction; the row states bytes only.

## Exact block text (registry rows, inserted after S031, before `## Paths`)

```
| S040 | e-Gov 法令検索 不正アクセス行為の禁止等に関する法律 — https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128 | spec | A | The consolidated text of the Japanese statute that defines unauthorized access and its owner-consent carve-out | 法令 ID 411AC0000000128, 平成十一年法律第百二十八号; 第二条 (定義) 第四項 and 第十一条 (罰則) reading 三年以下の拘禁刑又は百万円以下の罰金; retrieved through the e-Gov lawdata XML API, 200 and 36 058 B on 2026-10-25 | Japanese law defines unauthorized access around access control and absence of consent, so the scope owner's consent is the legal hinge | mined | 2026-10-25 | 730d | corpus/knowledge/statutory-authorization-and-unauthorized-access.md |
| S041 | 総務省 国民のためのサイバーセキュリティサイト 不正アクセス行為の禁止等に関する法律 — https://www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/ | docs | B | MIC's plain-language citizen statement of the offence; its penalty clause predates the consolidated amendment | （定義）第二条 第四項 第一号・第二号の括弧書 and 第十一条 (罰則) reading 三年以下の懲役 where the consolidated statute reads 拘禁刑; page footer © 2009 総務省; page cites the e-Gov 法令検索 record in its 参照 section; 200 and 85 874 B on 2026-10-25 | MIC states the offence as using a computer you have no 利用権限 for, but its 第十一条 still reads 懲役 while the consolidated statute reads 拘禁刑 | mined | 2026-10-25 | 730d | corpus/knowledge/statutory-authorization-and-unauthorized-access.md |
| S042 | 警察庁 不正アクセス行為の禁止等に関する法律の解説 — https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf | spec | A | The National Police Agency's official commentary: the meaning of アクセス管理者 and the consent carve-out | section 3 不正アクセス行為の禁止、処罰 (第2条第4項、第3条、第11条関係), subsection (1) 他人の識別符号を悪用する行為, with アクセス管理者又は入力する識別符号を付与されている利用権者の承諾を得て行う場合は禁止の対象から除外しています; PDF published by 警察庁; 200 and 477 938 B on 2026-10-25 | The official commentary treats access-control testing done with the access manager's or the user's consent as outside the offence | mined | 2026-10-25 | 730d | corpus/knowledge/statutory-authorization-and-unauthorized-access.md |
| S124 | NIST Special Publication 800-115, Technical Guide to Information Security Testing and Assessment — https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf | spec | A | The United States' primary guide to information-security testing and assessment: what a Rules of Engagement document is, what it authorises, and the template the guide ships for it; the western statement of the authorisation boundary the Chinese case law turns on | NIST SP 800-115, September 2008; glossary entry Rules of Engagement (ROE): Detailed guidelines and constraints regarding the execution of information security testing; The ROE is established before the start of a security test, and gives the test team authority to conduct defined activities without the need for additional permissions; Appendix B provides a template for creating Rules of Engagement (ROE); 200 and 544 047 B on 2026-10-25 | The western instrument for scoping an authorised test is the Rules of Engagement, established before the work starts, so what a tester may do is exactly what that document defines and no more | mined | 2026-10-25 | 90d | corpus/knowledge/authorised-testing-rules-of-engagement.md |
```

Plus one `## Paths` bullet (round-24 precedent is the round-23 bullet):

```
- Round-24 engagement-and-statute authorisation — S124 → S040 → S041 → S042: start from the engagement document that a defined authorisation is written in, then read the statute's own definition and consent carve-out, then the official commentary that reads the carve-out onto security checks.
```

Plus one `## Search log` bullet:

```
- Round-24 authorisation-outside-safe-harbour re-grounding; question: what authorises a security test when a platform's safe-harbour text is not the instrument; where: NIST SP 800-115, the e-Gov consolidated 不正アクセス行為の禁止等に関する法律, the MIC citizen page and the NPA commentary; date: 2026-10-25; identified 4 documents from the merge package's staged rows, screened 4, included 4, excluded 0. Each URL was re-opened from this lane (200; 544 047 B, 36 058 B, 85 874 B and 477 938 B) and its located quote re-read, so the four rows rest on this round's own open rather than on the package's transcription. The package's remaining staged rows were not screened: only the rows cited by the two adopted F09 entries were re-registered. Stop: the two traditions' own instruments answer the bounded question.
```

## Renumber decisions per id

| staged | lane | source | used-by (admitted entry) | decision |
|---|---|---|---|---|
| S031 | S032 | HackerOne standard program policy set | — | **not adopted**; the colliding id. Reserved for S032 if another seat adopts it. |
| S039 | **S040** | e-Gov 法令検索 不正アクセス行為の禁止等に関する法律 | statutory-authorization-and-unauthorized-access.md | new row, re-opened 2026-10-25 |
| S040 | **S041** | 総務省 MIC citizen page (tier B) | statutory-authorization-and-unauthorized-access.md | new row, re-opened 2026-10-25 |
| S041 | **S042** | 警察庁 NPA commentary | statutory-authorization-and-unauthorized-access.md | new row, re-opened 2026-10-25 |
| S123 | **S124** | NIST SP 800-115 | authorised-testing-rules-of-engagement.md | new row, re-opened 2026-10-25 |

All other staged ids (S032–S038, S042–S122, S124) were **not** registered: they are cited by
neither adopted entry, and registering an uncited row moves no coverage counter (CORPUS rule 4).

Safe application order if you renumber the entries' `source:` lines: **descending**
(`S041→S042` before `S040→S041` before `S039→S040`, and `S123→S124`), otherwise a second pass
double-shifts. Verified in `/tmp/kasegi-r24-c2check`:
`authorised-testing-rules-of-engagement.md:2 source: S124`, statute entry `:4 S040`, `:5 S041`,
`:6 S042`.

## Scratch note (stripped recheck prose, per row)

- S124 (staged S123) original recheck cell: `90d — re-fetch the PDF and \`grep -F\` the four lines (ran 2026-10-24)`.
  The clause survives here because the fleet schema's `recheck` column admits only an ISO date,
  `NNd` or a symbolic cadence (E09 otherwise). Recheck target: SP 800-115 glossary "Rules of
  Engagement (ROE)", the "established before the start of a security test" sentence, and the
  Appendix B template line.
- S040/S041/S042 already carried bare `730d`; no prose was stripped.
- Also stripped for fleet shape only: the package's `**bold**` emphasis inside the S124 scope and
  teaches cells, and its em-dash interjections (`opened 2026-10-24 (544 047 B …)`) replaced with
  the date-and-bytes form used by rows S004 and S031.

## Verification

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/kasegi-r24-SOURCESRows/corpus/SOURCES.md`

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E11	S040 missing used-by corpus/knowledge/statutory-authorization-and-unauthorized-access.md
file	E11	S041 missing used-by corpus/knowledge/statutory-authorization-and-unauthorized-access.md
file	E11	S042 missing used-by corpus/knowledge/statutory-authorization-and-unauthorized-access.md
file	E11	S124 missing used-by corpus/knowledge/authorised-testing-rules-of-engagement.md
rc=1
```

The two W04s are inherited from baseline (`census-before.txt`) and are warnings, not findings.
The four E11s are the only errors and they are **expected at this seat's boundary**: E11 resolves
`used-by` against the registry's parent directory, and the two entry files are the
EntryRoE/EntryStatute scribe seats' output, not mine.

Proof that the block is otherwise clean — same registry, entries staged verbatim from the package
into a throwaway copy (`/tmp/kasegi-r24-SOURCESRows-fixture`) at the exact `used-by` paths:

```
file	ok	/tmp/kasegi-r24-SOURCESRows-fixture/corpus/SOURCES.md
rc=0
```

Additional shape checks on the built registry:
`awk -F'|'` NF for S040, S041, S042, S124 = **13** each (11 columns, no cell swallows a pipe);
`grep -nE '\\\|' corpus/SOURCES.md` → no hits (no escaped pipe either);
`census --file` → `rows 35` (31 + 4), `tier.A 32`, `tier.B 1`, `tier.C 2`,
`status.mined 23`, `status.queued 9`, `status.rejected 3`, `FLEET.missing 0`, rc=0.

## Risks and blockers for L1

1. **Filename divergence on the statute entry.** Frozen `claims.json` lists the package candidate
   `statutory-authorization-in-three-traditions.md`; the EntryStatute dispatch instructs
   `corpus/knowledge/statutory-authorization-and-unauthorized-access.md`. My rows use the
   **dispatch** path (the file a seat will actually land). If L1 integrates the claims filename
   instead, re-point the three `used-by` cells — otherwise E11 fires on S040–S042.
   `authorised-testing-rules-of-engagement.md` matches both sources; no risk there.
2. **The +1 map is reconstructed, not read** (finding 1). If L1 has a different map, re-derive the
   four ids before integrating; the rows are otherwise map-independent.
3. **Counter B = 1, not 2** (finding 4). Decision needed before C2 is scored.
4. **The adopted entries still carry staged ids** in their `source:` lines (`S123`, `S039`,
   `S040`, `S041`). Whoever lands the entries must apply the descending renumber above, or the
   entries will cite rows that name different documents (S039 in lane numbering does not exist;
   S041 in lane numbering is the MIC page — a silent mis-citation of the same shape the r23
   spot-check caught).
5. **Ordering at integration.** Registry rows must land before the entries, or the round's
   validate receipt shows E11 for the whole window; both orders converge once both files exist.
6. Nothing was probed beyond the four cited public documents; no live target, no package tool run
   (`/home/vgpnk/Projects/shokuknow` was read-only). No tool installed or upgraded this seat.
