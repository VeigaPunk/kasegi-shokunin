# ExecEntryF16 — F16 knowledge entry (round 33, wave 1)

Seat: ExecEntryF16. Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin (only write scope).
Item: write `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` to QUALITY Q1-Q10
for Frontier F16, sources S049 + S050. Milestone round-33; judged on depth:verifiability, coverage.
Answering model: `opencode-go/deepseek-v4.1-flash` (config route table; no model passed by hand —
the seat env line names it). Tools installed/upgraded: none (nothing needed; no pacman transaction
was run, per the paused-host rule).
Date: 2026-10-26.

## 1. Artifact

```
$ sha256sum corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
1f7ac0a2c39a0fbfdbee2ecbe112316dfc1bf7095b18cb8fb4eb9d6dfce171d1  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
$ wc -l -c corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
  306 24539 corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
```

New file; no other lane path written (no README row, no SOURCES row, no manifest, no LOG entry —
each belongs to another seat; messages sent, see §7).

Inputs read before writing:

| input | why |
|---|---|
| `corpus/QUALITY.md` (Q1-Q10, R1-R19) | the admission bar this receipt answers |
| `corpus/source-snapshots/round-32/S049.txt` (426 lines), `S050.txt` (630 lines) | the two captures; every quote measured against these bytes |
| `corpus/source-snapshots/round-32/manifest.json` | ExecManifest32's landed record set (URL + `fetched_utc` + assertions) |
| `corpus/knowledge/vendor-third-party-finding-coordination.md` (F15) | entry shape, header-line form, hand-measured disclosure convention |
| `corpus/knowledge/program-severity-ladders-and-reward-scales.md` (F13) | the overlap the C2 kill rule names; differentiated in §Claim 3/"One overlap named" |
| `corpus/instruments/source-recheck.py`, `frontier-recheck-count.py` | the two instruments my `recheck:` line and the harness are measured by |
| `.ufo/waves/round-33/wave1/{ExecManifest32,ScoutF16Sweep,ConnSibling,ScoutLiveDrift}.md` | item-mandated peer receipts (manifest pin, negative sweep, province scan, fresh drift) |
| `.ufo/waves/round-33/claims.json` | C2's predicate (rows, ids, harness shape, no-restatement clause) |

Waiting, per the item: `{WD}/ExecManifest32.md` was polled with
`until [ -s .ufo/waves/round-33/wave1/ExecManifest32.md ]; do sleep 20; done`; it landed (13133 B
at 01:22) and its §1 pins the manifest. `ScoutF16Sweep.md` (13631 B) and `ConnSibling.md`
(8237 B) were already present and were read in full.

## 2. The entry

Header block verbatim (lines 1-7, long lines truncated here only):

```
1: # Chinese crowdsourced-testing platform scope and reward rules (CNVD 众测, 360SRC)
3: source: S049 — https://zc.cnvd.org.cn/news/helpList — 网络安全众测平台 使用手册, the answers to …
4: source: S050 — https://security.360.cn/Reward/rules — 360SRC 外部漏洞处理和评分标准 V2.0 (2023.03.01), …
5: verified-at: 2026-10-26
6: ground: F16
7: recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050   # 14 assertions …
```

Sections: `## Attribution`, `## Claim 1` … `## Claim 6`, `## Honest limit`,
`## Falsifiable checks` (FC-1…FC-6), `## Rejected over-generalizations` (1-7),
`## What this adds beyond F13 and F15`, `## Scope and limits`.

Claim set (each platform's rule stated as that platform's own, Q4):

1. CNVD 众测 intake bounded by the customer's per-project authorization; internet-wide findings
   refused and redirected to the CNVD 漏洞共享平台; the submission page's target list is not the
   scope document (S049.txt:211-214, 410).
2. CNVD 众测 publishes no per-severity money table; payout is enterprise rating + project rules;
   points are a multiplicative formula; per-project re-rating; trusted-testing-system sanction
   (S049.txt:132, 208, 359, 408, 419).
3. 360SRC applicability = 360 Group products/businesses + invested companies/subsidiaries/JVs,
   asset list deferred to a separate URL (S050.txt:70-71, 113).
4. 360SRC collection exclusions keyed to security-service coverage, with a stated major-harm
   exception (S050.txt:558, 591-593).
5. 360SRC reward = 业务系数 × 基础安全币 over per-type base tables, unit labeled
   `安全币 ：RMB=1 : 5`, five grades, seven-working-day final-rating clock (S050.txt:99, 112,
   113, 129, 418).
6. 360SRC report-hygiene/disclosure rules with forfeiture (S050.txt:595-598), plus legal
   reservation, employee exclusion and reserved interpretation (S050.txt:601, 607, 611); the
   CNVD manual's nearest rule is a non-sanctioned record-keeping recommendation (S049.txt:414).

## 3. Q1-Q10 self-check

`$E` = corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md. Measured on the final
bytes above.

| id | how it is met | pointer / measurement |
|---|---|---|
| Q1 | H1 at line 1; directly under it two `source:` lines (id + URL + exact anchors), `verified-at:`, `ground:`, one runnable `recheck:` | lines 1-7; `grep -c '^source: S049 '` → 1, `'^source: S050 '` → 1, `^verified-at: 2026-10-26$` → 1, `^ground: F16` → 1, `^recheck: cd ` → 1 |
| Q2 | every load-bearing claim rests on S049/S050 (tier-A public platform documents); both captures re-opened in the admitting round by a fresh read (ScoutLiveDrift, 2026-10-26T04:16Z, 0 differing lines); the rows are now landed | §Claim 1-6 each cite `S049.txt:…` / `S050.txt:…`; drift evidence in `## Scope and limits`; registry measured after ExecRegistryAppend landed: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `50`, rows at `SOURCES.md:55` (S049) and `:56` (S050), and `grep -cE '^source: S049 |^source: S050 ' corpus/knowledge/*.md` lists only this entry (2) |
| Q3 | 15 block quotes, each with an exact location line; longest 51 characters / 13 space-tokens (Chinese text has no spaces between words, so both measures are printed); every number quoted from the capture, none retyped from memory | 15 `> ` quote blocks, 15 `> — ` location lines, 0 unlocated (script in §5); e.g. `S049.txt:208` 48 chars, `S049.txt:132` 13 tokens |
| Q4 | attribution kept: each platform named as the stating party, and no rule generalized | `grep -c -F 'the CNVD 众测 manual states'` → 3, `'the 360SRC standard states'` → 5; `In English:` translation glosses → 3; F13/F15 similarity named, not merged |
| Q5 | 6 falsifiable checks, each a runnable grep with its measured count; 7 rejected over-generalizations with reasons | `grep -c '^- \*\*FC-[0-9]'` → 6; numbered items under `## Rejected over-generalizations` → 7 |
| Q6 | documentation only; no probing/scanning/login/submission instruction; no credential material, session or private URL | the CNVD page's platform-issued VPN retrieval (S049.txt:202-205) and OpenVPN walkthrough (S049.txt:398-406) are named and explicitly not reproduced; `grep -c` on the entry: `密码` → 0, `账号` → 0, `token` → 0, `ovpn` → 0 (the only `password`/`account`/`VPN` strings are in the Q6 paragraph describing non-reproduction); only the two public document URLs appear |
| Q7 | the `recheck:` line is one command whose output names what was checked (`S049:Qn OK occurrences=1`); a corrupted-source control fails closed | §4 full output, exit 0; control: one appended byte to a copied `S049.txt` → `S049:sha256 MISMATCH …` exit 1 |
| Q8 | no quote depends on markup; the declared normalization is stated in the `recheck:` comment and in `## Scope and limits` (`source-recheck.py`'s markup-strip + whitespace collapse) | line 7 comment; `## Scope and limits` bullet 2 |
| Q9 | every manifest assertion prints its occurrence count (14 × `occurrences=1`); the 16 hand-measured strings each carry their own `grep -c`/count in place, and none of them is claimed as manifest-bound | §4 output; `grep -o 'hand-measured'` → 18 (16 body markings + the recheck comment + the summary sentence) |
| Q10 | one executable line: `bash -n` clean and exit 0 from a foreign cwd, with its own `cd <lane-root> &&` prefix and the human note after `#` | §4 `bash_n_exit=0`, `foreign_cwd_exit=0` run from `/` |

Q3/Q9 literal counts (final bytes):

```
$ grep -c '^> ' $E ; grep -c '^> — ' $E
15
15
$ python3 -c "…quote audit…"      # §5 script
quotes= 15 unlocated= 0 max_tokens= 13 max_chars= 51
```

Manifest-bound vs hand-measured: 14 manifest assertions are all quoted in the entry (13 as block
quotes + S049 Q8 `注：请严格按照项目测试范围进行测试。` inline), and 2 further block quotes
(`S050.txt:113`, `S050.txt:129`) plus 14 inline strings are marked *hand-measured* with the
command/count that re-checks them.

```
$ python3 -c "…manifest cross-check…"
manifest_quotes 14 missing []
```

## 4. Recheck and Q10 evidence (final bytes)

```
$ grep '^recheck: ' $E | sed 's/^recheck: //' > $S/cmd.sh; bash -n $S/cmd.sh; echo "bash_n_exit=$?"
bash_n_exit=0
$ ( cd / && bash $S/cmd.sh ); echo "foreign_cwd_exit=$?"
S049:sha256 OK
S049:Q1 OK occurrences=1
S049:Q2 OK occurrences=1
S049:Q3 OK occurrences=1
S049:Q4 OK occurrences=1
S049:Q5 OK occurrences=1
S049:Q6 OK occurrences=1
S049:Q7 OK occurrences=1
S049:Q8 OK occurrences=1
S050:sha256 OK
S050:Q1 OK occurrences=1
S050:Q2 OK occurrences=1
S050:Q3 OK occurrences=1
S050:Q4 OK occurrences=1
S050:Q5 OK occurrences=1
S050:Q6 OK occurrences=1
foreign_cwd_exit=0
```

Q7 corrupted-source control (`$S` = a scratch dir; committed captures untouched):

```
$ cp corpus/source-snapshots/round-32/{manifest.json,S049.txt,S050.txt} $S/ && printf 'x' >> $S/S049.txt
$ python3 corpus/instruments/source-recheck.py --manifest $S/manifest.json --source S049
S049:sha256 MISMATCH expected=962a451a…1cb8 actual=7c845dfc…0367c
corrupt_S049_exit=1
$ python3 corpus/instruments/source-recheck.py --manifest $S/manifest.json --source S050
S050:Q5 OK occurrences=1 … (exit 0)
intact_S050_exit=0
```

Manifest pin this entry cites (frozen; ExecManifest32 confirmed by message, digest re-measured
here):

```
$ sha256sum corpus/source-snapshots/round-32/manifest.json
6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774  corpus/source-snapshots/round-32/manifest.json
```

Entry pin paragraph cites the same digest plus the two capture digests
(`962a451a…1cb8` 20272 B/426 lines; `2f9c6406…6888` 31016 B/630 lines).

## 5. Harness binding (pre-landing control, labelled)

The lane's own `frontier-recheck-count.py` cannot see this entry until the `| F16 | … |` row lands
in `corpus/README.md` (ScribeReadmeF16's file). Lane-tree state, PRE-STATE for F16:

```
$ python3 corpus/instruments/frontier-recheck-count.py
… PASS F15 … ids=S048 exit=0
entries=18 pass=18 exit=0
$ grep -c '| F16 ' corpus/README.md
0
```

Pre-landing control in a scratch copy (`cp -a corpus $S/corpus`, F16 row appended to
`$S/corpus/README.md`; the harness reads `root/corpus/README.md`, not `root/README.md`):

```
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
entries=19 pass=19 exit=0
fixture_exit=0
```

**AFTER — the real lane tree, measured once the reader row landed** (ScribeReadmeF16 appended
`| F16 | … |` at `corpus/README.md:335`):

```
$ python3 corpus/instruments/frontier-recheck-count.py
… PASS F15 … ids=S048 exit=0
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
entries=19 pass=19 exit=0
harness_exit=0
```

Discrimination control on the same fixture (drop `--source S050` from the copied entry only):

```
FAIL     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=-  problems=header-sources-not-rechecked
entries=19 pass=18 exit=1
```

So the harness binds my line to both header ids (A-D), and the C2 target shape
(`entries=19 pass=19` incl. `PASS F16 ids=S049,S050`) is reached by my entry plus the row.
**Re-run named:** the lane harness on the real tree after ScribeReadmeF16 lands the row — the
18/18 above must not be compared to an after column, and the 19/19 figure is a fixture number on a
copied README, not the lane's gate.

Row text handed over (also sent to the seat): `| F16 | Chinese crowdsourced-testing platform
scope and reward rules | admitted | knowledge/chinese-crowdsourced-testing-scope-and-rewards.md |
S049, S050 | Keep each platform's scope object distinct… |`.

## 6. Reviewer corrections applied to my own file

Three reviewers sent findings; all were applied to these bytes (this is why the digest moved
through `8d4b1489…` → `8d209995…` → `eebd5ea5…`).

| from | finding | change |
|---|---|---|
| ExecManifest32 (message) | manifest grew 6+6 → 8+6 (`Q7` formula at S049.txt:132, `Q8` 注-line at S049.txt:212); full L70-71 sentence cannot bind (wrap space inside 合资公司) | cited Q7 and Q8; removed the *hand-measured* marker on the 注 line; recheck comment now `14 assertions (S049 Q1-Q8, S050 Q1-Q6)`; scope bullet pins `6e4e719a…` |
| CritBoundary (message) | stale manifest digest; stale `12 assertions (6 per capture)` | both corrected (already done when the message arrived; FC-5's 安全币 count corrected 64 → 32 in the same pass) |
| CritC2Kill (message + receipt) | 1 cross-market comparison sentence (Q4); 2 Claim 2 headline restated F13's override shape; 3 F13-overlap + refused-entry provenance undeclared; 4 missing "instruments not commensurable" rejection; 5 `verified-at` not distinguished from the capture instant and one hand-measured quote without its count | all five applied: Claim 5 now states the mechanism difference (S050 fixed clock vs S049 post-submission re-rating); Claim 2 headline leads with "publishes no per-severity money table"; "One overlap named" paragraph cites F13:32's pre-submission override and declares the S049 formula's refused-entry provenance while declining the CVSS 3.0 metric set; Rejected #7 added (S049.txt:356 withdrawal floor vs S050.txt:129 peg; occ 1); limits bullet added for ScoutLiveDrift's 2026-10-26T04:16Z fresh read, and `grep -c` → 1 printed beside the S050.txt:113 quote |
| RevQuoteSweep | the FAQ question stem was transposed in my two *citations of the section heading* (not in a quote): I wrote `漏洞提交时…` where the capture's L210 reads `提交漏洞时…` (`grep -c '提交漏洞时'` on the entry was 0, so this was a retyped stem, not a quote — the class R19 forbids) | both spots corrected; the location line now also separates question and answer (`S049.txt:210-211 … at L210; the answer, quoted above, at L211`), because the quote it introduces sits at L211 while the question sits at L210. Self-audit after the fix: all 13 Chinese strings in quotation marks in the entry resolve into S049 or S050 under the instrument normalization; the only non-resolving one is my own template phrase `“the CNVD 众测 manual states…”` in the Attribution paragraph |
| CritC2Kill (second pass) | my fix-3 counter was self-referential: `grep -c -E 'CVSS\|0.85\|时效评价\|利用代码'` on the entry printed `3`, not `1`, because the declaration paragraph itself carries the terms (R19 stale premise) | replaced with a section-scoped measure whose count is stable and re-measured: `awk '/^## Attribution/{f=1} /^## What this adds/{f=0} f' <entry> \| grep -c -E 'CVSS\|0.85\|时效评价\|利用代码'` → `1` (only the seven-aspect quote in Claim 2) |

## 7. Peer messages sent (coordination only; no peer file edited by me)

| peer | content |
|---|---|
| ExecManifest32 | my 12 quote candidates for the manifest (before it froze), then a freeze question |
| ExecRegistryAppend | entry path + digest, both source URLs byte-exact as the manifest `url` values (C1 rule B), `used-by` target, anchor cells, suggested cadence (90d S049 / 180d S050 — their call) |
| ScribeReadmeF16 | the exact `| F16 | … |` row text, plus the two fixture mechanics (`root/corpus/README.md`, ids cell must equal header ids) |
| ScribeProvince | proposed F16 province-amendment text and the boundary the entry holds |
| ExecExpectedList | the one sorted line to add to `corpus/instruments/knowledge-expected.txt` and its insertion point (`chinese…` before `citation-bases.md`); measured 45 files on disk vs 44 listed entries |
| ScribeSearchLog | F16 entry data for the SOURCES Search log / R8 lines (staged S034→S049, S035→S050 by document, cell rewrites, 48→50 rows) |
| ScribeGateDraft | **delivery failed**: `write agent://ScribeGateDraft` → `Failed: ScribeGateDraft is not running. Unknown agent` — the gate-row data (admit F16, Q1-Q10 numbers, harness after-state, refuse rows from the refused package entries) is preserved verbatim in this receipt's §3 and §6 for whoever files the gate |

`agent://all` was never messaged. No message asks a peer to copy my bytes without measuring.

## 8. Bounds, risks, blockers

- Writes: the one knowledge file plus this receipt. `git status --porcelain` over my scope shows
  only `?? corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` and
  `?? .ufo/waves/round-33/wave1/ExecEntryF16.md` as mine; the tracked modifications present
  (`corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/knowledge-expected.txt`, the
  eight legacy manifests, `corpus/source-snapshots/round-32/manifest.json`,
  `corpus/instruments/capture-binding-check.py`, `PROVINCE.md`, `corpus/QUALITY.md`) belong to the
  seats named in the item's ownership table. I wrote none of `corpus/README.md`, `corpus/SOURCES.md`, a manifest, `LOG.md`,
  `SCORECARD.md`, `QUALITY.md`, instruments, `.ufo/state/`, `MANIFEST.json` or any fleet-root
  path. No git/jj mutation of any kind; no background job; no subagent; no fetch
  (documentation-only: I read the committed captures, and ScoutLiveDrift's fresh read is cited, not
  repeated by me).
- Scratch: `$HYAKU_SCRATCH/kasegi-r33/ExecEntryF16*` was used twice (Q10/control + harness
  fixtures) and both dirs were removed; verified after cleanup:
  `ls -d /fast/scratch/hyaku/kasegi-r33/ExecEntryF16*` → `No such file or directory`. No `/tmp`
  use except two one-line helper files that were deleted in the same command (not citable
  evidence; the Q10 run above was redone from scratch under `$HYAKU_SCRATCH`).
- Q2 dependency resolved after my write: ExecRegistryAppend landed the rows (registry 50, S049 at
  `SOURCES.md:55`, S050 at `:56`) and ScribeReadmeF16 landed the F16 row (`corpus/README.md:335`),
  so the harness and row halves are now measured post-state (see §5). Neither file is mine; I did
  not edit them.
- The `safe-harbor`/`免责` absence claims are claims about these two captures, not about the
  platforms' other pages (a linked policy or product-list page could exist and is not read here).
- Known measurement limits stated inside the entry: the 360SRC capture is flattened PDF text, so
  table cell pairings are read from printed order; the CNVD capture is page-level with chrome at
  L1-22 and contacts at L420-426; `verified-at` is not the capture instant.
- Nothing here is a gate run: the lane's census, capture-binding-check, recheck-audit and the real
  harness are the parent's post-integration checks.

## 9. Open items owned upstream (reported by CritC2Kill; routing only, measured by them)

Recorded here so they are not lost with the seat. None is a defect in the entry (CritC2Kill closed
the entry on the live digest `1f7ac0a2…71d1`, its §12 superseding its earlier hashes); all five are
rulings or wording in C2's kill rule that belong to the L1.

1. **C2's refused-ground clause is mis-worded.** Read literally it kills F16 for ground that the
   earlier refusal's own flip condition ordered recovered, and it names a refused file
   (`chinese-crowdsourced-testing…`) that does not exist — ScoutF16Sweep measured the real staged
   names as `cn-crowdsourced-testing-roles-and-conduct.md` and
   `chinese-crowd-testing-national-standard-2026-10-23.md`.
2. **The reviewer clause has no committed control.** CritC2Kill reports a measured junk twin
   (restatement body with real-but-non-asserting exactly-once quotes) that passes every C2 counter —
   frontier=16, 1/1 citing files, 1/1 rows, 50 rows, census exit 0, harness 19/19,
   source-recheck exit 0. I did not build or measure that twin; it is cited as the reviewer's
   finding. This entry does not resemble it: its quotes are the manifest's own assertions and its
   claims are each the named platform's stated rule.
3. **Stating parties should be named page+operator, not acronyms** — `网络安全众测平台` manual /
   CNCERT-CC for S049, `360 安全应急响应中心` for S050. The entry's Attribution paragraph already
   does this (it names the manual and its footer rights holder, and the 360SRC standard and its
   publisher); the open item is about the clause's own wording.
4. **A quote-verbatim conjunct is missing** from the clause: a quote must be re-opened against a
   round-current live fetch or be a prose-only line. The entry's own limit section states exactly
   this asymmetry — `source-recheck.py` on a pin is not a fresh network verification, and only
   ScoutLiveDrift's 2026-10-26T04:16Z read was.
5. **Counter 2 should be restricted to the Q1 header block** so a body mention of an id cannot
   satisfy it. Measured against my entry: the two `source:` lines are lines 3-4 and the only other
   `S049`/`S050` occurrences are citations of capture lines, not `source:` lines.

The five refused files the clause must name exactly (CritC2Kill §12; I read two of them via
ScoutF16Sweep and did not re-derive the list myself): `cn-crowdsourced-testing-roles-and-conduct.md`,
`chinese-crowd-testing-national-standard-2026-10-23.md`,
`program-scope-rules-and-asset-boundaries.md`, `claim-packaging-and-report-quality.md`,
`chinese-program-severity-instrument.md`.

Final reviewer state: CritC2Kill's §12 re-verified this entry on the live digest
`1f7ac0a2…71d1` — stem corrected (L210/L211), recheck 14/14 exit 0, harness `PASS F16`
`entries=19 pass=19`, C2 counters unchanged (frontier 16, 1/1 files both ids, 1/1 rows both ids,
registry 50, census exit 0 with only base W04 S028/S029) — and superseded its earlier hashes.
