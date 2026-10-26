# ExecRegistryAppend — round-30 wave-1 seat report

Seat: `ExecRegistryAppend` (L2 executor, leaf). Lane: kasegi-shokunin. Base `a94871315cafa368f79c17d8c62d71fddd967986`; claims-freeze `3c5573541300ba0fd3d89372dda3d841172eaa3f`. Answering model: `inception/mercury-3` (config route table; no model passed). No tool installed (none needed).

## Scope

Sole writer of the `corpus/SOURCES.md` registry appends for this round:
1. Append rows S046 and S047 after the last registry row (S045), 11 columns each, no `|` inside any cell.
2. Append "Registry changes" lines (R8: rows added old → new; any status/recheck/used-by cell change logged old → new).

## Files changed

- `corpus/SOURCES.md` — exactly the two registry rows + three Registry-changes lines. No existing row touched.

## Registry rows appended (verbatim, as landed at lines 52–53)

```
| S046 | IPA JVN activity report — https://www.ipa.go.jp/security/reports/vuln/jvn/ug65p90000019ev2-att/000095610.pdf | docs | A | JVN's own severity vocabulary: the CVSS-to-深刻度 band definitions | capture corpus/source-snapshots/round-30/S046.txt: 注1) CVSSv2 基本値の深刻度による色分け (レベルI 注意 0.0-3.9 / レベルII 警告 4.0-6.9 / レベルIII 危険 7.0-10.0) and 注2) CVSSv3 (注意 0.1-3.9 / 警告 4.0-6.9 / 重要 7.0-8.9 / 緊急 9.0-10.0), lines 555-570 | JVN has no native severity scale — it maps CVSS base scores onto Japanese labels keeping legacy v2 bands | mined | 2026-10-25 | 180d | corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md |
| S047 | IPA JVN quarterly registration report — https://www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html | docs | A | JVN quarterly severity distribution | capture corpus/source-snapshots/round-30/S047.txt: 2-2 深刻度別割合, 図2-2 (CVSSv2 レベル1-3) and 図2-3 (CVSSv3 注意/警告/重要/緊急), lines 215-240 | Japan's national database carries CVSS-derived severities at scale | mined | 2026-10-25 | 90d | corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md |
```

Both anchors verified against the captured bytes:
- S046.txt lines 555–570: `注 1）CVSSv2 基本値の深刻度による色分け` (0.0–3.9 レベルI 注意 / 4.0–6.9 レベルII 警告 / 7.0–10.0 レベルIII 危険) and `注 2）CVSSv3 基本値の深刻度による色分け` (0.1–3.9 注意 / 4.0–6.9 警告 / 7.0–8.9 重要 / 9.0–10.0 緊急).
- S047.txt lines 215–240: `2-2. 脆弱性に関する深刻度別割合` with `図2-2` (CVSSv2, レベル1–3) and `図2-3` (CVSSv3, 注意/警告/重要/緊急), including the 2026 Q3 distribution percentages.

Capture digests measured (sha256):
- `corpus/source-snapshots/round-30/S046.txt` = `884481f3781e200d4c7e6efd91b2912ada513fa126c534d3392ccd48003a03a3` (575 lines)
- `corpus/source-snapshots/round-30/S047.txt` = `bcf4f605d75909301f02560df894e0c4c15d97c7928a1759f57b15b5a7d905f4` (1402 lines)

## Registry changes lines appended (R8)

- S046 row added: new row (id S046, tier A, mined, opened 2026-10-25, recheck 180d, used-by `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md`); staged SOURCES.append.md S049 cells → landed: opened 2026-10-23 → 2026-10-25; anchor rewritten from the round-30 capture; used-by → the F14 entry only.
- S047 row added: new row (id S047, tier A, mined, opened 2026-10-25, recheck 90d, used-by same entry); staged SOURCES.append.md S050 cells → landed: opened 2026-10-23 → 2026-10-25; recheck 180d → 90d; anchor rewritten from the round-30 capture; used-by → the F14 entry only.
- No status/recheck/used-by cell changed on any pre-existing row; S041–S045 untouched (logged). Registry 45 rows → 47 rows.

## Verification

Measured at the landed working-tree bytes. `corpus/SOURCES.md` sha256 (final, post-changelog) = `a126a5f339323d5ae417a944d163d75a0427d9c77a5a330308e193dc7b81d927` (pre-changelog append-state digest `ce54089cfd3efa9301c12fe3b58ea0281b7632f749338ada8746f88a2f4fe01c`).

- Registry rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`): **47** ✔
- S046+S047 rows present (`grep -cE '^\|[[:space:]]*S04[6-7][[:space:]]*\|' corpus/SOURCES.md`): **2** ✔
- `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`: output `kasegi W04 S028 …`, `kasegi W04 S029 …`, `kasegi ok /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md`, **exit 0** (W04 S028/S029 only) — measured after the F14 entry landed; E11 was present while the entry was absent, see below.

### Timeline note (E11 dependency)

Immediately after the append, census validate reported `E11 S046/S047 missing used-by corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` (exit 1) because the F14 knowledge entry had not landed yet (another seat's write). Polled for the entry; final validate result above is post-entry-landing.

## As-of stamps (read this before quoting any row count)

`corpus/SOURCES.md` rows are cumulative across rounds, so this seat's numbers are **as-of stamps**, not current state:

| as-of | file sha256 | rows | S046+S047 | S048 |
|---|---|---|---|---|
| end of this seat's append (round-30 state) | `a126a5f339323d5ae417a944d163d75a0427d9c77a5a330308e193dc7b81d927` | **47** | 2 | 0 |
| after the round-31 owner's S048 append | `5a03c696312bd5fd8fe8307f75bd9723cac97fe3e44f0f3ba46a68607295f6f5` | 48 | 2 | 1 |

Round-30's frozen C2 clause `registry rows != 47` is satisfied **at round-30's commit**, which is what the round-31 base census-before records (`rows=47`). Any later round that appends a row moves the live count; quoting 47 as *current* would be wrong from round 31 on, and quoting 48 as round-30's result would be wrong in the other direction. Both directions are named here so neither is inherited as a defect.

The risk this seat flagged earlier — round-31's R8 line and Search-log note still owed — is **closed at the current bytes**, verified read-only at sha256 `5a03c696…`: `corpus/SOURCES.md:94` is the R8 line `- S048 row added: new row (id S048, kind docs, tier A scoped to Microsoft's own statement of its MSVR programme, status mined, opened 2026-10-25, recheck …` and line 72 is the Search-log entry `- Vendor third-party-finding coordination sweep (round 31); question: does the lane already hold "a vendor's research programme as an intake route for other ven…`. Census `validate --file corpus/SOURCES.md` → exit 0, only W04 S028/S029; S048 row digest unchanged at `0f2d9cb61c8743577476906fb6ea2a9285082931e5ff811dac98d0f26f83de7a`.

## Risks / notes

- The F14 entry `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` and the round-30 manifest (`corpus/source-snapshots/round-30/manifest.json`) are owned by other seats; this seat only registered the rows they cite.
- No write outside the lane repo; no git/jj mutation, no live target contact, no tooling installed.
- No open risk against this seat's deliverable. The two round-31 items this seat flagged are both closed and verified: the owner's R8 line and Search-log note are on disk (above), and the mis-attribution in `ExecCensusDry-3`'s §5b was relabelled to `ExecRegistryAppend-2` (receipt now sha256 `da45f3c3333910a4deaa9f465570d1a08499267e36e38649d893f59fe689da67`, 386 lines; superseding `71a1e9ae…` and `f6a49da1…`).

## Post-handoff note — S048 belongs to round 31, not this seat

`ExecCapManifest` (round-31 seat) reported the round-31 `S048.txt` snapshot landed (`3755 B`, 97 lines, sha256 `2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55`; `round-31/manifest.json` 2800 B) and asked that the registry row not be recaptured. Verified at the landed bytes by this seat, read-only: the digest matches, and `grep -cE '^\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md` → **0** (registry still 47 rows).

**No S048 row was appended by this seat, deliberately.** This seat's frozen round-30 C2 kill rule is `registry rows != 47` → fail, so an S048 append here would falsify round 30's claim. The round-31 dispatch already names the owner: `wave1-dispatch.json` `taskCall/tasks[15]` = seat `ExecRegistryAppend` ("Own `corpus/SOURCES.md` ONLY", gated on `.ufo/waves/round-31/wave1/ExecEntryF15.md` and `ExecCensusDry.md` exit 0), which must take rows 47 → 48. Nothing in `corpus/source-snapshots/round-31/` was fetched, rewritten, or touched by this seat.

Relay performed (coordination only, no writes): the S048 paths, sizes, digest, URL, the "cite the snapshot path, never a re-fetch — line 2 is a per-request Trace Id" anchor rule, and the rows 47 → 48 target were sent to `agent://ExecRegistryAppend-2` (the second live instance of that seat name, i.e. the round-31 owner) and confirmed back to `ExecCapManifest`. `ExecCapManifest` confirmed it will not recapture and that its write scope never included `SOURCES.md`. Re-measured after the relay: `corpus/SOURCES.md` still 47 rows, 0 S048 rows, sha256 `a126a5f339323d5ae417a944d163d75a0427d9c77a5a330308e193dc7b81d927` — no double-landing.

Ownership confirmed, not inferred: `history://ExecRegistryAppend-2` shows its assignment verbatim as "kasegi-shokunin round 31 … Seat ExecRegistryAppend … Own corpus/SOURCES.md ONLY", with the round-31 FILE OWNERSHIP line `corpus/SOURCES.md: ExecRegistryAppend`. That instance is live and mid-flight, so this seat's refusal to append is the correct single-writer behaviour, not an omission.

`ExecCensusDry-3` then sent this seat the verbatim S048 row with an instruction to append. Declined and redirected to `ExecRegistryAppend-2`. Two facts were returned to it and to the owner, both measured here:

1. **Anchor claims hold.** `corpus/source-snapshots/round-31/S048.txt` L31 is `MSVR learns about vulnerabilities in third-party products in three ways:`, L32–L34 are the three routes, L35 is `This coordination takes place under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach.` — the proposed L31 / L32-L34 / L35 anchor cell is correct against the landed bytes.
2. **My digest objection was wrong and is corrected here.** I reported that `ExecCensusDry-3`'s claimed line sha256 `c1edc552ebcfc3b8bf0be852b2557511dfbab3e26d9b86f8618d52b06c7b3db6` did not bind the row it published, because my copy hashed to `1ca202e2…` at 773 B. That copy was **truncated in transit**: the inbound IRC paste lost 22 bytes (772 B against the real 795 B) and its padding spaces, so I hashed a different string. Re-measured independently against the bytes the census seat actually used — `sed -n '54p' .ufo/waves/round-31/wave1/ExecCensusDry/validate/corpus/SOURCES.md` → **795 B / 793 chars, NF=13 (11 columns), sha256 `c1edc552ebcfc3b8bf0be852b2557511dfbab3e26d9b86f8618d52b06c7b3db6` with the newline and `6034ec28453bb367eeb4aa5c83b484a246df7b608a187cdd7c0d88078bda5c80` without; one non-ASCII char (the em dash)**. The census seat's claim is correct and my finding was a measurement artefact of the truncated message. Lesson for the lane: hash a file, never an inbound message body.

Round-31's owner then landed its own row (not the mirror row byte-for-byte): `corpus/SOURCES.md` line 54, cells scope/anchor/teaches rewritten to its item's spec — heading L28, purpose L29-L30, three-ways lead-in L31, routes L32-L34, three-roles sentence L35. I verified each of those anchors against the landed capture (L28 is the `Microsoft Security Vulnerability Research (MSVR)` heading; L29-L30 the purpose paragraphs; L31/L32-L34/L35 as above), so the landed anchor cell is accurate. Landed line digest: `0f2d9cb61c8743577476906fb6ea2a9285082931e5ff811dac98d0f26f83de7a` (with newline; `db871511b56e841de8cdc22127526d59b44a9439f239a391728e98d0d680e0a2` without), 916 B / 914 chars (913 without the newline; the 2-byte excess is the single em dash U+2014); live registry **48 rows, S048 exactly once**, census `validate` **exit 0** with only W04 S028/S029. `c1edc552…` therefore binds the census mirror bytes, not the landed line — the round-31 receipt should hash the landed bytes.

**Attribution, corrected with the peers — and the correction is verifiable in their receipt.** `ExecCensusDry-3` recorded line 54 as "your landed row" in its receipt §5b; I asked it to relabel that to `ExecRegistryAppend-2`, the round-31 owner, because a wrong attribution makes a single-writer path look double-written. It did: `.ufo/waves/round-31/wave1/ExecCensusDry.md` (now sha256 `da45f3c3333910a4deaa9f465570d1a08499267e36e38649d893f59fe689da67`, 386 lines; the sequence was `f6a49da1…` → `71a1e9ae…` → `da45f3c3…` as it absorbed each correction) states at line 252 that `corpus/SOURCES.md` has one writer this round — `agent://ExecRegistryAppend-2` — and at line 271 that `agent://ExecRegistryAppend` is the round-30 instance which made no write to that path in round 31, and its §5b label at line 232 scopes `c1edc552…` to the mirror line only. This seat's only relation to that row is read-only verification. Independently confirmed at the landed bytes: `ExecEntryF15`'s entry digest `1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb` / 160 lines / 11,501 B; `source:` line 2 names S048; the row sits at line 54 with `## Paths` opening at 56, so the census E12 (row outside `## Registry`) cannot fire — and does not, at exit 0.
