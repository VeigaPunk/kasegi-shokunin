# Round 25 wave 1 — PROVINCE scope check of the assimilation set

Seat: `L1Kasegi25.CritC2Scope` (critic, READ-ONLY). No production edit, no file outside this one
written, nothing installed or upgraded (no tool change). Lane base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`.

## 1. The test applied

PROVINCE.md, read whole, quoted at line:

- `:29` — "The line-3 domain comprises program rules, scopes, and claim packages; the core also
  covers triage and claim gates, and submission/disclosure packaging."
- `:37` — "General practice that governs every program is indexed in corpus/README.md under
  Frontier F01–F09 (F09, round 24 …; 9/9 admitted)."
- `:43-48` — sibling lanes reported, not absorbed: chousa, kagi, kake, kengaku.
- `:50` — "Live-target testing is refused; this corpus is documentation only."

Admission bar: `corpus/QUALITY.md` Q1–Q9 (entry) and R8/R12 (registry identity, recheck binding).

## 2. Registry facts that decide provenance (measured this seat)

| fact | command / source | observed |
|---|---|---|
| lane registry size | `grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md` | **35**, last `S035` |
| lane meaning of the staged ids | `corpus/SOURCES.md` rows | S031=CVE CNA 4.2.6, S032=NIST SP 800-115, S033=e-Gov 411AC0000000128, S034=総務省 解説, S035=警察庁 解説 |
| package id space | `SOURCES.append.md` | 94 rows, **S031–S124**, "first staged id is S031" (`MERGE-REPORT.md`, which still says "lane registry currently holds **30** rows" — stale by five) |
| this round's own allocation | `.ufo/waves/round-25/capture-log.txt` | S036=Cybozu policy (staged S055), S037=Cybozu FAQ (S056), S038=Pepabo (S057), S039=Hitachi (S060), **S040=Cisco (S068)**; all `status=200`, `utc=2026-10-25T08:14:2xZ` |
| frontier rows | `corpus/README.md` § Frontier | F01–F09 only, 9/9 admitted. **F10 is this round's declared new row** (claims.json C2); F11, F19, F20 do not exist |
| C1 surface | `recheck-audit.py:collect()` globs `corpus/knowledge/*.md`; `ls`/`grep` | `files=35 recheck_lines=35` |
| round-25 manifest | `ls corpus/source-snapshots/round-25/`, `find … -name 'manifest*'` | five `.txt` only; **no `round-25/manifest.json`** (round-23 and round-24 have one) |
| staged recheck form | `bash -n -c "<recheck>"`, then the instrument's own `CORPUS_PATH_RE`/`HOME_BASE_RE` | **all seven: `bash-n=2`, `corpus_path=0`, `homebase=0`** — every staged `recheck:` fails C1 limb (a) and (c) and Q7 |

## 3. Verdicts

| entry | verdict | criterion | reason | flip |
|---|---|---|---|---|
| 1. `japanese-vendor-disclosure-policies-2026-10-23.md` | **admit** (landing conditions below; the claim already calls it "re-grounded") | PROVINCE`:29` Core "submission/disclosure packaging" + PROVINCE`:37` new Frontier **F10** (C2's declared row) | In-domain, and its substance is carried by this round's committed captures, not by inference: S036 L13-15 (対象範囲 = 当社が作成した全てのサービスおよび、製品 + サードパーティー製品), L19 (パートナーシップ / 脆弱性報奨金制度を含む / 社内検出), L22 (CVSS as 指標のひとつ), L28-30 (publication = パッケージ製品, mobile excluded, cloud 原則非公開), L44 (JVN 公表日一致, JPCERT/CC と取り決めた日); S037 L109/L115; S038 L17/L20; S039 L490-491/L506. Three conditions, all measured: (i) header ids S055/S056/S057/S060 are **package** ids — no lane row bears them; capture-log allocates S036–S039; (ii) `ground: F09` redefines the *admitted* F09 (round-24 ROE/statute row) and must read F10; (iii) Q5's "rejected over-generalization" block is absent, and "runs the programme **by invitation**" is unsupported: S037 has 0 hits for 招待/招待制/クローズド/推薦 and supports only an account-gated site requiring an お申込み (L99-101) | — |
| 2. `vendor-cvd-policy-crosswalk-2026-10-23.md` | **refuse** | **Q3** (+ Q1; PROVINCE`:37`) | Its disclosure-trigger paragraph states "**the two conditions** under which it will go faster". Its own bytes of record list **four** situations — S040.txt L300 lead-in, bullets at **L301, L302, L305, L308** (high-severity fix planned; observed active exploitation; potential increased public awareness; third-party declared high profile). A count copied from the source is exactly what Q3 exists for; a gate that admits it is mis-calibrated. Independently: `S068` is a package id (lane capture id **S040**) and `ground: F20` names no indexed row. Its other claims do verify (ISO/IEC 29147:2018 L58; LDoS L163; definition+deviation L66-68; JP-CERT L184-190) | Restate the paragraph as **four** situations with the capture's line anchors; cite **S040**; ground **F10**; recheck as one C1/R12 command over a round-25 manifest. Then admissible — the flip is one sentence, not a re-research |
| 3. `program-severity-ladders-and-reward-scales.md` | **refuse** (this round) | **Q1 + R8** (source-id identity), **Q2** | Scope passes (Core "program rules … triage"). Provenance does not: header ids S032/S033/S034 already name NIST SP 800-115 / the e-Gov statute / the 総務省 page in the lane registry, and S036 now names this round's Cybozu capture; the entry's real supports (Bugcrowd VRT README, `cwe.json`, CNVD 帮助, BILISRC V1.7) hold **no** lane row. `ground: F10` also takes this round's single new frontier slot for a different topic | Register the four supports as fresh rows at the lane's free ids (**S041+**, R8 new-row rule — do not edit S031–S036), re-point the header ids, and cite an existing frontier row (F01/F05) instead of claiming F10 |
| 4. `claim-packaging-and-report-quality.md` | **refuse** (this round) | **Q1 + R8** | Scope passes (Core "claim packages", "submission/disclosure packaging"). S034/S035 collide with the lane's 総務省/警察庁 rows and S036 with this round's Cybozu capture; the three real supports (CNVD 帮助, 360SRC V2.0, BILISRC V1.7) are unregistered. `ground: F11` names no row | Register the three rows at S041+, re-point the header, drop the F11 ground and cite Core |
| 5. `program-scope-rules-and-asset-boundaries.md` | **refuse** (this round) | **Q1 + R8** | Scope passes (Core "scopes"). `source: S031` is the CNA 4.2.6 row in this lane; the entry means the HackerOne `policy_versions` record; S034/S035 collide as above. Its own text says it "extends F03", yet the header claims a **new F09** — the admitted F09 is the round-24 ROE/statute row | Register the HackerOne `policy_versions` record as a **new** row (distinct page from S006, R8), re-point, and cite **F03** (which already holds the rule it extends) |
| 6. `iso-29147-and-30111-division-of-labour-2026-10-23.md` | **refuse** (this round) | **Q1** + PROVINCE`:37` | Scope is arguable-in — 29147 is outward advisory distribution and 30111 inward handling, i.e. Core "submission/disclosure packaging" — so the refusal is **provenance, not scope**: S076 has no lane row and no round-25 capture, and `ground: F19` names no indexed row | Register the JPCERT 2026 guideline 付録6 §2 as a lane row with a committed capture and an anchor disjoint from the package's round-4 §4 row, and ground it on an indexed row (F10 or an existing admitted one) |
| 7. `vendor-third-party-finding-coordination-2026-10-23.md` | **refuse** (this round) | **Q1** + PROVINCE`:37` (dangling ground chain) | S080 has no lane row and no capture; `ground: F20 (extends the round-4 entry vendor-cvd-policy-crosswalk)` names a nonexistent frontier row **and** an entry absent from `corpus/knowledge` (35 files, none of that name) that is itself refused above — a two-link absent chain | Register S080 (MSRC MSVR) with a committed capture and ground it **directly on F10**, dropping the dependency on an unadmitted entry |

`reject for the lesson Gate: vendor-cvd-policy-crosswalk-2026-10-23.md — Q3: its "the two conditions" disclosure-trigger claim is contradicted by its own bytes of record, which list four situations (S040.txt L301, L302, L305, L308).`

**Do not file the planned reject reason.** claims.json (`assimilation.planned_reject`) says "S068 Cisco
policy unreachable this round". That is **falsified by the lane's own capture log**: `S040
status=200 fetched_bytes=94027 sha256=b7f7b55f… utc=2026-10-25T08:14:28Z`; only a plain `curl -L`
with a browser UA returned 403, and the log records that the instrument's UA got 200 and that the
re-fetch is reproduced by `ScoutFetchCisco`. Filing "unreachable" would put a false provenance line
in the lesson — the exact class of defect this lane keeps routing (D24-1..D24-5).

## 4. Sibling-lane check

None of the seven is another lane's ground. `chousa` PROVINCE explicitly **refuses** "bounty-program
scope and claim packages (→ kasegi)", i.e. routes this ground here; kagi (secrets/vault), kake (web
properties), kengaku (LLM evaluation) do not cover any of the seven. No absorption, no routing
needed; all seven refusals above are provenance/identity, not cross-domain.

## 5. Two structural defects that outrank the per-entry ones (for L1, not claim rewording)

1. **The whole set is keyed to the package S-space.** The package allocates S031–S124; the lane holds
   S001–S035 and this round's capture log has already spent S036–S040. Appending `SOURCES.append.md`
   as written would make **S031–S036 each name two different sources** — an identity change against
   R8 and against the three admitted entries that cite them (`cna-assignment…` S031, `authorised-
   testing…` S032, `statutory-authorization…` S033–S035). Smallest safe correction: never append the
   staged ids verbatim; re-key every accepted row to the lane's allocation (capture-log mapping for
   S036–S040, S041+ for the rest) and leave S031–S035 untouched.
2. **C1's frozen surface and C2's admit are mutually exclusive as written.** `recheck-audit.py`
   globs `corpus/knowledge/*.md` (measured `files=35 recheck_lines=35`); landing entry 1 makes
   `lines=36` while C1's target is `lines=35 pass=35`. Correction is sequencing, not re-wording: file
   C1's after-receipt on the **pre-admit** 35-file surface (naming the measured file list in the
   receipt), then land the entry. Otherwise the round publishes a counter that contradicts its own
   frozen surface.
3. **No `corpus/source-snapshots/round-25/manifest.json` exists** (round-23/round-24 only), so no
   R12-conformant recheck can be written yet — R12 needs `--source` ids covering the header ids *and*
   a manifest that lists them. This is the single blocker between "admit" and a landable file 1. The
   conformant shape, given C1 limb (b) and D24-5, is one command:
   `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S036 --source S037 --source S038 --source S039`
   (the `cd … &&` prefix is what the other cwd-safe lines use; without it the foreign-cwd limb exits 2).

## 6. Counterexample tested and what it settles

Strongest test available against the planned admit was "does the *content* survive the captures?" —
because a scope-passing entry with a fabricated clause is worse than a refused one. Result: entry 1's
substance survives (line anchors in §3 row 1), with **one** clause failing — "by invitation" (0 hits
in S037; the capture's fact is an account-gated site with an お申込み form, L99-101). So the admit
stands as a scope verdict, but the file cannot land byte-identical: that clause and the two header
conditions are the price of admission. For entry 2 the same test produced the opposite result: the
prose asserts an exhaustive count its own capture contradicts, which is why the Gate reject is a Q3
defect rather than the round's planned "unreachable" story.
