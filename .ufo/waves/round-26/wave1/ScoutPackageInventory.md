# ScoutPackageInventory — staged package inventory (round 26, wave 1)

Seat: `L1Kasegi26.ScoutPackageInventory` (leaf, read-only on `/home/vgpnk/Projects/shokuknow`).
Package: `/home/vgpnk/Projects/shokuknow/merge/kasegi/`. Date: 2026-10-25 (UTC). Raw tally: `s3-inventory.txt`.

## 1. Package existence and row census — CONFIRMED

| item | status |
|---|---|
| `MERGE-REPORT.md` | exists (13,771 B) |
| `MERGE-REPORT.json` | exists (29.2 KB; `accepted=94`, `refused=[]`) |
| `SOURCES.append.md` | exists (89,718 B; 94 data rows) |
| staged rows | **94**, ids **S031–S124** (first S031, last S124; rows at lines 7–100) |
| knowledge files | 67 under `knowledge/corpus/knowledge/` (matches report's 67); no `amendments/` dir |

**Discrepancy:** `MERGE-REPORT.md:9` says "lane registry currently holds **30** rows; first staged id is S031"; the lane registry at freeze holds **40** (`corpus/SOURCES.md` S001–S040). `claims.json` note records `reg=40 staged=94 collisions=10 (S031-S040)` — the report's "30" is stale.

### Ids (staged vs lane registry)
- **Collide with lane registry (10):** S031, S032, S033, S034, S035, S036, S037, S038, S039, S040. Staged rows at these ids are different documents from the lane rows (e.g. staged S031 = HackerOne standard program policy vs lane S031 = CVE CNA 4.2.6) — adoption must renumber, as claims.json's note anticipates (adopt continues from S041).
- **Free (84):** S041–S124.

## 2. Target staged entries — CONFIRMED with current bytes

| file | bytes | sha256 | ground | source(s) |
|---|---|---|---|---|
| `corpus/knowledge/iso-29147-and-30111-division-of-labour-2026-10-23.md` | 2,642 | `c2dbbe84…` | F19 (extends round-4 divergence entry) | S076 — JPCERT/CC P-guideline 2026-10, 付録6 §2 paragraph on ISO/IEC 30111:2013 + 図 1, p.45 |
| `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk-2026-10-23.md` | 3,907 | `20aaf266…` | F19 (new frontier item) | S064 — 付録6 §4 p.46-47 + 参考1 p.53-54; S068 — Cisco "Cisco Product Security Incident Response" |

Headers: both carry `source:`/`verified-at: 2026-10-23`/`recheck: 180d — … (ran 2026-10-23)` per Q1 shape (entry-wise: Q1's three header lines are present; the `recheck:` field itself is non-conforming — see §4).

### Extracted claims and locations
Entry 1 (division of labour, all S076/付録6 §2, 図1 p.45):
- 29147 = outward handling: 「外部からの脆弱性に関する情報の受領、ユーザに対する脆弱性対策のアドバイザリ配布等」; ベンダ includes product developer / online-service provider / intermediate vendor.
- 30111 = internal process: 「ベンダの社内での脆弱性取扱いのプロセス」; guidance on 「脆弱性の検証」 and 「脆弱性対策の開発」.
- 図 1「ISO/IEC 29147 と ISO/IEC 30111 の対応」, marked 「出所：ISO/IEC 29147:2014 を元に作成」 (drafter's own reconstruction).
- Honest limit states 30111 is characterised, not reproduced (unlike 付録6 §4 for 29147).

Entry 2 (divergence):
- S064: the divergence is one sentence — P-guideline does not require a vendor to adopt a vulnerability-disclosure policy; ISO/IEC 29147:2014 does require one and publication of part of it (付録6 §4, p.46-47); table rows 全体/オンラインサービス/脆弱性公開ポリシー/脆弱性の受領/中間ベンダ.
- S064: 6.2 "Minimum policy aspects" reproduced in English + Japanese incl. elements a)–f); 6.3 "Optional policy aspects"; clause 3.4 on online services; 参考1 maps 1–9 (5.1–5.9, 6.1–6.3, 7.1–7.7) onto P-guideline sections (p.53-54).
- S068 (verbatim, ≤25 words): "The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018" — location: "Cisco Product Security Incident Response" (this matches the lane's pinned S040 quote — the staged S068 is the same Cisco page).

Confidence: high for headers/quotes (read whole files); quote-text extraction from entry 1 is inline Japanese fragments, not block quotes — a Q3-style verbatim-sentence check would need source-recheck against a capture (the package provides no snapshots; `capture-source.py` is the lane's instrument).

## 3. Recheck-line strict-limb evaluation — 4/6 limbs FAIL on both targets

Limb semantics taken from `corpus/instruments/recheck-audit.py` (`audit_entry`, lines 93–131; FROZEN=parse/cwd/paths, STRICT adds cdroot/instrument/own; cf. round-25 lesson §Claims and RevManifestShape T13).

Staged lines:
- E1: ``180d — `curl -sSL https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` and confirm 付録6 §2 still carries the ISO/IEC 30111:2013 paragraph (ran 2026-10-23)``
- E2: ``180d — `curl -sSL https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` then confirm 付録6 still carries 参考1 and the section-4 table (ran 2026-10-23)``

| limb | E1 | E2 | why |
|---|---|---|---|
| parse | FAIL | FAIL | `bash -n` rejects: prose after the backtick command + `(ran …)` tail; also `180d — ` prefix is not a command (same class as the 23 pre-fix hybrids) |
| cwd | pass* | pass* | *trivially*: both cwds fail identically (rc=2 syntax error, same output) so the equality check passes without executing anything |
| paths | FAIL | FAIL | names no `corpus/….(md|py|json|txt|tsv)` token and no `~/Projects/` base |
| cdroot | pass* | pass* | *vacuously*: no `cd <path> &&` prefix, so there is nothing to check |
| instrument | FAIL | FAIL | no `corpus/instruments/*.py`; no `test -[def] ~/Projects/` |
| own | FAIL | FAIL | no own-file token, no `--source` + `corpus/source-snapshots/`, no bare base-state assertion |

Both would land as **non-conforming** entries: strict gate pass would fall below total (37/37 → 37/39), `exit=1`, killing C1's after-state if adopted verbatim. The two passes are non-load-bearing (cwd equality-of-failure; cdroot vacuity). The reject candidates carry the identical shape (vendor crosswalk: prose + curl + `(ran …)`; chinese-criminal: `730d — … curl … (ran …)`), matching the recorded Q7 reject reason.

## 4. Reject candidates — CONFIRMED, grounds vs lane frontier

| file | bytes | sha256 | ground | lane-frontier status |
|---|---|---|---|
| `vendor-cvd-policy-crosswalk-2026-10-23.md` | 3,281 | `be3ddb32…` | **F20** (new frontier item) | no F20 row exists — round-25 lesson recorded reject on exactly this: Q7 prose recheck, `grep -cE '\| F20 '` → 0, Q3 four-vs-two disclosure-trigger conditions |
| `chinese-criminal-thresholds-and-authorisation.md` | 4,124 | `1660c00c…` | **F12** (extends F03) | no F12 row exists — round-24 lesson recorded reject: Q2+Q4 and Q1/Q7 (prose recheck; `curl` exits 0 on a 404; "purely quantitative" falsified by 第一条(五) 其他情节严重的情形; ground F12 names no lane frontier item) |

Lane frontier (`corpus/README.md`) currently holds F01–F10 admitted; **F11** is the round's admission target, and F12/F19/F20 exist nowhere in it. All three package grounds (F12, F19×2, F20) are package-local frontier pointers, not lane frontier ids — consistent with claims.json's "adopt_ids … renumbers staged S076/S064 by document".

## 5. Observations for the adopting seat (facts, not fixes)
1. Both target recheck lines must be rewritten at adoption (`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && <instrument>  # note` form) or C1's strict gate breaks; the package's `curl -sSL` rechecks are not lane instruments and would be unverifiable offline (round-25 access note: plain curl gets 403 on Cisco unless the capture UA is used).
2. Staged S068 (Cisco) duplicates the lane's admitted S040 document; the entry's S068 citation would need re-pointing to S040 (and the claim's "S068" ground row to the admitted id) per R8/R12.
3. Staged S076/S064 both point at the same JPCERT/CC guideline PDF with disjoint anchors (付録6 §2 vs §4/参考1) — fine under R8 if adopted as separate rows, but both would be superseded by the fresh S041 capture per claims.json.
4. `MERGE-REPORT.md`'s "registry holds 30" is stale (40 at freeze); the collision set S031–S040 is exactly the 10 documented in claims.json.

## Unknowns / not verified
- I did not run `source-recheck.py` or `recheck-audit.py` against the staged package (read-only seat; the package has no snapshot manifest, and running the audit from the lane repo would measure lane bytes, not staged bytes). Limb verdicts are derived from the instrument's code and the exact staged line text.
- The 67 knowledge files' per-row `used-by` consistency with the 94 staged rows was not exhaustively cross-checked (outer scope).
