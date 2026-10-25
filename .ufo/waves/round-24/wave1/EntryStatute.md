# EntryStatute — F09 statute entry (C2, second half)

Seat: scribe (leaf). Draft written in a private clone; the lane tree was read only, except this report.

## Findings (each with an evidence pointer)

1. **The e-Gov consolidated text, not either government explainer, is the authority for the penalty — and both explainers diverge from it in the same direction.**
   - `/tmp/r24-stat/egov.xml` (sha256 `baac5ef21a89ed131bd1d5289487292451da10d8dd6e62735e6311987b5a3992`, 36 058 B) 第十一条: `三年以下の拘禁刑又は百万円以下の罰金に処する`. The whole document contains `拘禁刑` twice (第十一条, 第十二条) and `懲役` **0** times (`grep -o '拘禁刑[^<]*' egov.xml`; count via python on the tag-stripped text).
   - `/tmp/r24-stat/mic.html` (sha256 `dd5e4951…61ce4`, 85 874 B) （罰則）第十一条 block: `三年以下の懲役又は百万円以下の罰金に処する`; footer `© 2009 Ministry of Internal Affairs and Communications`.
   - `/tmp/r24-stat/npa.pdf` (sha256 `1f8ac1fb…0508a6`, 477 938 B, 17 pp.) §3, PDF p. 6: `３年以下の懲役又は100万円以下`; `pdfinfo` reports no creation/modification date and `Metadata Stream: no`.
   - Divergence direction: 懲役 → 拘禁刑, the consolidated text being the newer form. The XML's own supplementary provisions are drafted against the Penal Code amendment (`刑法等一部改正法施行日から施行する` row, quoted in the entry as `刑法等一部改正法施行日から施行する`, 17字), but the amending act itself was **not opened** — see UNVERIFIED below.

2. **The consent carve-out is asymmetric, which is the falsifiable core of the entry.**
   - 第二条第四項第一号括弧書 excludes manager acts + consent of *the manager or the symbol holder* (`アクセス管理者又は当該識別符号に係る利用権者の承諾`, 25字, unique in egov.xml).
   - 第二号括弧書 excludes manager acts + *the manager's consent only* (`当該アクセス管理者の承諾を得てするものを除く`, 22字, unique), and 第三号 inherits it by `次号において同じ` (8字, unique).
   - Consequence recorded as the entry's consent-holder rule: an account holder's consent covers 第一号 use of that symbol; exploit-shaped conduct (第二号/第三号) needs the アクセス管理者's consent.
   - アクセス管理者 is defined by managing the computer's operation (`当該特定電子計算機の動作を管理する者`, 18字, unique in egov.xml), may be a corporation (`アクセス管理者は個人、法人の別を問いません`, 21字, NPA p. 2) and may number more than one per computer (`２以上のアクセス管理者`, 11字, NPA p. 2).

3. **Why safe-harbour text is not the legal definition is stated as two checkable conditions, attributed, not as a universal legal conclusion.** The entry conditions a safe-harbour statement's relevance on (i) the grantor being the アクセス管理者 of the affected computer for the affected 特定利用 and (ii) the statement consenting to that conduct; it names F03's separate asset-scope rule and says NPA does not discuss safe-harbour text and no court holding was opened.

4. **Japanese quotes are all ≤25 characters and all unique per document.** 25 labelled quotes, character counts machine-verified against the strings (`python3` count check over the file: 0 mismatches; max 25). Every string was counted in the fetched document under whitespace-collapsing normalization: each count is 1.

5. **Registry defect found while checking my row ids (not fixed by me).** The new S034 row titles its source `不正アクセス行為の防止等に関する法律の解説`, but the cited page's own `<title>` is `不正アクセス行為の禁止等に関する法律 | 国民のためのサイバーセキュリティサイト` (`grep -m1 -o '<title>[^<]*</title>' /tmp/r24-stat/mic.html`). The statute is 禁止 (平成11年法律第128号), so the row names a law that does not exist; per R8 the repair is a `supersedes S034 —` row or a logged field correction, not a silent edit. My entry cites S034 by URL and the （罰則）第十一条 block, so it is unaffected. Reported to L1 in the same turn.

## Gate evidence (QUALITY Q1–Q6)

| gate | evidence |
|---|---|
| Q1 | Header trio immediately under the H1, no intervening blank line: `source: S033/S034/S035` (row id + URL + article/page anchor), `verified-at: 2026-10-25`, `recheck:` = executable command plus cadence `# 730d, next recheck 2028-10-25`. Extraction test used the C1 counter's own pattern and exited 0 (below). |
| Q2 | Load-bearing claims rest on S033 (tier A, spec) and S035 (tier A, spec/commentary); S034 is tier B and is never sole support for a claim. |
| Q3 | Every load-bearing claim carries a verbatim quote with article/paragraph/item (e-Gov) or PDF page plus section (MIC, NPA), plus its character count; counts are the author's own and machine-checked. |
| Q4 | MIC and NPA are named as their own documents; NPA is labelled the National Police Agency's official commentary cited as interpretation; the safe-harbour section is labelled this entry's reading of S033 with S035. |
| Q5 | Three falsifiable rules (consent-holder, channel, penalty-quote) and four rejected over-generalisations with reasons. |
| Q6 | Documentation-only; the three sources are public documents read by `curl` on 2026-10-25. `grep -nEi 'ops://\|vault://\|token\|password\|credential\|api[_-]?key'` on the entry: 0 hits. |

## Recheck receipt (executed)

```
r=$(grep -m1 '^recheck: ' <entry> | sed 's/^recheck: //'); bash -c "$r"
S033-S035 ok: S033 第三条/第二条第一項/第二条第四項 carve-outs/第十一条 拘禁刑 (懲役 absent, control passed); S034 prints 懲役 (divergence reproduced); S035 prints the 承諾 exclusion
EXIT=0
```

Command length 1 381 B; it fetches S033/S034/S035 into `mktemp -d`, runs `pdftotext` on S035, greps eight exact strings, then runs the negative control `grep -qF "三年以下の懲役" e.xml` which must **not** match.

Missing/corrupted-source control exercised: a copy of the same command with the e-Gov penalty assertion replaced by the stale `三年以下の懲役又は百万円以下の罰金に処する` exits **1** (and the wording control swapped likewise). So the field fails closed on a stale or absent base, and its exit 0 is not vacuous.

Host tooling used (no installs this round; all pre-existing): curl 8.23.0, pdftotext (poppler) 26.08.0, python3 3.14.8. No pacman/uv/network install was performed.

## Touched surfaces

- `/tmp/kasegi-r24-EntryStatute/corpus/knowledge/statutory-authorization-and-unauthorized-access.md` — new file, 16 184 B, 98 lines, sha256 `7b363c536d0e86ae46147b90b5a089ca69487de2d93ed77465c530485e28d1a8`. `git -C /tmp/kasegi-r24-EntryStatute status --porcelain` lists this one path only.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/wave1/EntryStatute.md` — this report.
- Nothing else was written in the lane, the fleet repo, `/home/vgpnk/Projects/shokuknow`, git/jj state, or `MANIFEST.json`/`.ufo/state/`.

Clone base: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kasegi-shokunin /tmp/kasegi-r24-EntryStatute` → HEAD `c2480b143120364728b40397926ffcf30a7309c8` (lane master). The contract text names base `d0a3f6a4…`, which is the parent of the lane tip; the tip is one integrator commit ahead (`c2480b1 round-23 verifier spot-check …`). The entry is a new file, so the two bases are byte-identical for its purpose; **reporting the drift rather than silently checking out the older base.** No commit, no push, no jj, no `git add/checkout/reset/stash` in the lane.

## Out-of-scope items (deliberately not done)

- No README frontier row F09, no SOURCES.md append, no renumber map: L1 owns integration. My `source:` ids are the ones L1 gave (S033 e-Gov / S034 MIC / S035 NPA); L1 also confirmed C2's counter B grep `^source: S1[0-9][0-9]` is mis-specified and being corrected by erratum.
- The Chinese half is **not** imported: the refusal seat owns that, and the entry's Limits records that the derived-from three-traditions entry says 刑法 第285条 could not be opened and points to its `CANNOT-ANSWER.md`.
- No build/lint/test/formatter run beyond executing my own recheck, per contract.

## Limits / UNVERIFIED

- **UNVERIFIED: the amending act.** `刑法等の一部を改正する法律` (the act that replaced 懲役 with 拘禁刑) was not opened; its commencement date and article are not asserted. The entry states the divergence from the consolidated text and the two explainers only, and says so explicitly.
- **UNVERIFIED: any court holding.** No decision on the scope of 承諾 or on the アクセス管理者 of hosted assets was opened; the consent-holder test is a textual reading plus NPA commentary, labelled as such.
- The recheck is a **network** recheck (no committed capture exists for S033-S035), so it proves current-text agreement, not freshness of a pinned snapshot; the entry says so nowhere, but this report does, and the fetch hashes `baac5ef2…`, `dd5e4951…`, `1f8ac1fb…` were stable across two separate fetches minutes apart.
- Article-level reading covers 第二条, 第三条, 第十一条 and the supplementary-provision table only; 第四条–第七条 and 第十二条 are named as outside.
- NPA page attributions are PDF page numbers from the 17-page file, not printed folios.
