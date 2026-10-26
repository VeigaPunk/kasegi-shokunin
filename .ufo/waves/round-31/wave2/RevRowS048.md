# RevRowS048 — S048 registry-row review against SOURCES contract v1 (round 31, wave 2)

- **Seat:** `RevRowS048` (reviewer, leaf; no subagent dispatch)
- **Answering model:** `opencode-go/deepseek-v4.1-flash` (config route table decides; no model passed). This item is **not model-dependent** — every verdict below is a command output, not a judgement call.
- **Tooling installed/upgraded:** none. `pacman` is paused host-wide (orchestrator ruling 2026-10-20), no package transaction run, no binary fetched.
- **Subject:** landed row `S048` in `corpus/SOURCES.md:54`, mapped by DOCUMENT from staged `S080` at `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md:56`.
- **Contract:** `/home/vgpnk/Projects/shokunin/CORPUS.md` § "SOURCES.md — where a shokunin learns", Contract v1 (kaika 2026-10-19, frozen), rules 1–6 plus the Shape paragraph and the frozen census block. (`corpus/CORPUS.md` does not exist in the lane — the contract lives at the fleet root only; measured below.)
- **Lane write scope:** this receipt only. All attack/fetch scratch under `/tmp/revs048.XqijB3`. No lane file other than this receipt was written; `git status --porcelain corpus/` is empty.
- **Verdict summary:** all six rules **CONFORMANT** at row level; the row is an honest, capture-pinned registration of the staged `S080` document. Two rule halves are **PENDING** on `corpus/lessons/round-31.md` (absent — owned by `ScribeLesson`), and three low/informational notes are recorded in §4. No medium or high finding.

---

## 1. Independent re-open of the source (non-author verification sample)

### 1.1 Live re-capture — instrument UA, scratch only

```text
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && W=$(mktemp -d /tmp/revs048.XXXXXX) && python3 corpus/instruments/capture-source.py --id S048 --url https://www.microsoft.com/en-us/msrc/msvr --out "$W/S048.txt" --kind html
S048 status=200 fetched_bytes=81802 snapshot_bytes=3755 sha256=42f7350bf9ad9d6414e0410b24e3cfbd9ade8cc057280464e06f327532e33657 utc=2026-10-26T00:25:43Z out=/tmp/revs048.XqijB3/S048.txt
capture_exit=0
97 /tmp/revs048.XqijB3/S048.txt
```

Committed pin (`sha256sum corpus/source-snapshots/round-31/S048.txt`) = `2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55`, 3,755 B, 97 lines — **matches** `manifest.json` `sources[0].sha256`.

```text
$ diff -u corpus/source-snapshots/round-31/S048.txt "$W/S048.txt"
--- corpus/source-snapshots/round-31/S048.txt
+++ /tmp/revs048.XqijB3/S048.txt
@@ -1,5 +1,5 @@
 msvr
-This is the Trace Id: f97e6b1cb578f714d23850f80f018bb3
+This is the Trace Id: bee78928abe690c9c0b171e0360c2eb7
 MSRC
 ...
diff_exit=1
```

**1 of 97 lines differs — line 2, the per-request Trace Id only.** Every line number the row's `anchor` cell cites is therefore stable on a fresh fetch. This agrees with `wave2/ScoutLiveDrift.md` (same single-line delta, independently fetched 2026-10-26T00:24Z).

### 1.2 URL shape (canonical, not a bare homepage, no redirect, no session artefact)

```text
$ curl -sS -A 'kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)' -o /dev/null -D - -w 'http=%{http_code} redirects=%{num_redirects} final=%{url_effective}\n' https://www.microsoft.com/en-us/msrc/msvr
HTTP/2 200
content-type: text/html; charset=utf-8
http=200 redirects=0 final=https://www.microsoft.com/en-us/msrc/msvr
```

### 1.3 Anchor lines re-opened one by one (fresh bytes)

```text
24|Security Researcher Acknowledgments
28|Microsoft Security Vulnerability Research (MSVR)
29|MSVR is a program specifically designed to help improve the security ecosystem as a whole through the sharing of knowledge and best practices.
30|Microsoft’s goal is to share our collective experience in dealing with security vulnerabilities with the greater security community to foster positive change. ...
31|MSVR learns about vulnerabilities in third-party products in three ways:
32|Internal Microsoft engineers: In the course of their regular work, engineers find potential vulnerabilities in third-party software. These vulnerabilities are reported to the MSVR team, which then works with the affected vendor to fix the issue.
33|External reports to the Microsoft Security Response Center (MSRC): On occasion an external researcher will report an issue ... These issues are coordinated by MSVR.
34|Internal research projects: ... Any issues are reported to the affected vendor under accepted Coordinated Vulnerability Disclosure practices.
35|This coordination takes place under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach. CVD clarifies how Microsoft responds as a vendor affected by vulnerabilities ..., as a finder of new vulnerabilities in third-party products and services, and as a coordinator of vulnerabilities that affect multiple vendors.
```

Anchor cell → observed: `heading ... L28` ✔ · `purpose L29-L30` ✔ (L29 programme purpose, L30 stated goal) · `three-ways lead-in L31` ✔ · `routes L32-L34` ✔ · `three-roles sentence L35` ✔ (three roles: affected vendor / finder / multi-vendor coordinator).

### 1.4 The anchor's "no visible publication or revision date" claim — carried sweep

```text
$ grep -nEi '(last updated|updated|published|revis|modified|[0-9]{4}-[0-9]{2}-[0-9]{2}|©|copyright)' corpus/source-snapshots/round-31/S048.txt
rc=1     # 0 matches over all 97 lines
```

### 1.5 `teaches` grounding, re-measured on fresh bytes (exactly-once)

```text
Internal Microsoft engineers: In the cou -> 1
External reports to the Microsoft Securi -> 1
Internal research projects: As time and  -> 1
as a finder of new vulnerabilities in th -> 1
as a coordinator of vulnerabilities that -> 1
```

Every clause of the row's `teaches` cell ("own engineers (L32), external MSRC reports (L33) and internal research (L34), and names itself finder and multi-vendor coordinator ... (L35)") resolves at the cited line. `grep -c '2026-10-23'` inside the S048 row line → `0`: the staged date did not survive.

### 1.6 Manifest assertions re-checked against the live bytes

```text
Q1 occurrences=1 'MSVR learns about vulnerabilities in thi'
Q2 occurrences=1 'These vulnerabilities are reported to th'
Q3 occurrences=1 'These issues are coordinated by MSVR.'
Q4 occurrences=1 'Any issues are reported to the affected '
Q5 occurrences=1 'as a vendor affected by vulnerabilities '
Q6 occurrences=1 'as a finder of new vulnerabilities in th'
Q7 occurrences=1 'as a coordinator of vulnerabilities that'
Q8 occurrences=1 'This coordination takes place under Micr'
all_exactly_once= True
```

(Normalization applied by this seat: whitespace collapsed to single spaces; the capture's `html_to_text()` output carries no markup tags to strip. This is a live-byte observation at `2026-10-26T00:25Z`, one host, three fetches across two seats — **not** a claim of ongoing currency.)

---

## 2. The six contract census commands, copied verbatim from CORPUS.md § "Census — run from the lane root"

All six were run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

```text
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
48
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
A=45 B=1 C=2
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
mined=36 queued=9 rejected=3
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
(no output)
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; ... if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
(no output)
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; ... if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
(no output)
```

Totals cross-check: 45+1+2 = 48 rows; mined+queued+rejected = 36+9+3 = 48; malformed 0; duplicate ids 0; enum/tier violations 0; every `mined` `used-by` path resolves.

Maintained CLI:

```text
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

Only the two **base** W04 warnings; **no new E/W naming S048** (no duplicate URL, no unused mined row).

---

## 3. Verdict per rule

| rule | contract requirement | verdict | evidence |
|---|---|---|---|
| **1** | A row is a claim, written only after opening the source in the writing round; the round lesson's `## Gate` records URL, access date and a ≤25-word located quote grounding `teaches` | **CONFORMANT (row level); lesson half PENDING** | `opened 2026-10-25` = round 31; capture mtime 2026-10-25 20:29 -03, capture UTC in the Gate draft `2026-10-25T23:29:53Z`; §1.1–§1.5 above re-open the source non-author. Gate record exists as draft `wave1/ScribeGateDraft.md:42` with URL, access date, capture digest and two located quotes (`… three ways` L31, 10 words; `as a coordinator of vulnerabilities that affect multiple vendors` L35, 9 words, each `grep -cF` = 1). `test -e corpus/lessons/round-31.md` → **ABSENT**; that file is `ScribeLesson`'s write path, so this half is pending, not failed. |
| **2** | Append-only; only `status`/`recheck`/`used-by` change in place, each logged old→new; corrections are new rows | **CONFORMANT (row level); lesson half PENDING** | `git diff --numstat b374feb..HEAD -- corpus/SOURCES.md` → `3 0` (three insertions, zero deletions: row L54, search-log L72, change note L94). Stronger row-level check: `git show b374feb:corpus/SOURCES.md \| grep -E '^\| S[0-9]{3,} ' \| sha256sum` = `fd039ca9c881bc5dc03d0619daf48ae8099cf0f2af9c569943e73f7c2d9746ac`; the same extractor over HEAD minus the S048 line = `fd039ca9…` **identical**; 47 rows → 48. The `§ Registry changes` note (`SOURCES.md:94`) logs `id S080 → S048`, `opened 2026-10-23 → 2026-10-25`, scope/teaches rewrite, anchor rewrite, `used-by` old→new, and states "no other row's cell changed (R8)" — verified true. `recheck` did not change (180d → 180d), so no log line is owed. Lesson-side old→new logging is the same pending `round-31.md`. |
| **3** | No second method: admission stays in `QUALITY.md`, research method stays chousa's | **CONFORMANT** | The row and the appended log carry no admission criterion and no research method; the log cites the registry's cell shape and Q4 attribution only. |
| **4** | Expansion is knowledge, not rows; no row quota | **CONFORMANT** | One row for one admitted entry on uncovered ground: `grep -lE '^source: S048 ' corpus/knowledge/*.md \| wc -l` → `1`; that entry's `ground:` is F15, and F15 is appended at `corpus/README.md:309` citing `S048`. No second row was minted for the document. |
| **5** | Search log: question/query, where, date, identified/screened/included/excluded, exclusion reasons, stop rationale; a negative claim carries its sweep | **CONFORMANT — every count reproduced** | `SOURCES.md:72` carries question, where, date 2026-10-25, `identified 5 staged entries (10 staged source rows), screened 5, included 1, excluded 4`, four named rejects with reasons, and a stop rationale. Reproduced by this seat: the 5 screened entries cite exactly 10 distinct staged rows (`S080`; `S031 S034 S035`; `S034 S035 S036`; `S081 S082`; `S077 S078 S079` → 10 unique). `(43 files)` reproduced: `git ls-tree --name-only eadedef corpus/knowledge/ \| grep -c '\.md$'` → `43`. Negative sweep reproduced: `ls corpus/knowledge/*.md \| grep -v vendor-third-party-finding-coordination.md \| xargs grep -lie 'msvr\|msrc\|coordinator of vulnerabilities'` → no hits (rc=1); pre-append `SOURCES.md`, `README.md`, `SKILL.md` each `grep -cie` → `0`. |
| **6** | No credential material, session/private URL, `op://` | **CONFORMANT** | `grep -nEi 'op://\|secret\|token\|api[_-]?key\|password\|cookie\|session=\|bearer\|vault'` over the row, the entry, the capture and the manifest → one hit, page chrome `S048.txt:92 Manage cookies`; no credential, no session URL, no vault reference. The URL is public, unauthenticated, query-string-free, `redirects=0` (§1.2). |

### Shape / item checklist (the questions this seat was dispatched on)

| ask | verdict | measurement |
|---|---|---|
| 11 columns under the census awk | **PASS** | `awk -F'\|' '/^\| S048 \|/ {print "NF="NF}'` → `NF=13`; the malformed-row census over the file → `0` |
| no `\|` inside any cell | **PASS** | same NF=13 (an in-cell pipe raises NF); row `len=913`, last char `\|`, trailing whitespace `0` |
| tier scoped, not global | **PASS** | tier `A` with `scope` = "Microsoft's own statement of its MSVR programme **and of nothing beyond it** …"; not a universal-vendor claim; kind `docs` ≠ `community`, so no tier inflation (§2 enum sweep empty) |
| anchor exact: section + capture lines + date, not a bare homepage | **PASS** | capture path + heading `L28` + `L29-L30`/`L31`/`L32-L34`/`L35` + "page shows no visible publication or revision date, opened 2026-10-25"; every line re-opened in §1.3, date-absence sweep in §1.4. Not a homepage: `/en-us/msrc/msvr` returns 200 with `redirects=0` (§1.2) |
| `teaches` one grounded benefit | **PASS (note N1)** | every clause resolves exactly-once at its cited line (§1.5); the cell is descriptive rather than benefit-framed, see N1 |
| `status mined` with a resolving used-by path | **PASS** | `used-by` = `corpus/knowledge/vendor-third-party-finding-coordination.md`; `test -e` → present; that entry carries `source: S048 …` at L2; mined-used-by census sweep → no `missing:` line |
| `opened 2026-10-25`, not the staged `2026-10-23` | **PASS** | `opened` cell `2026-10-25`; `grep -c '2026-10-23'` inside the row → `0` (the staged date survives only in the change log as the old value, which is correct) |
| `recheck` a valid cadence | **PASS** | `180d`, one of the three cadence forms the contract names (`90d`, `180d`, `on-release`), bare (no inline prose, so census E09 cannot fire), and calibrated to the standing-vendor-policy class (S004/S005/S036–S040 all `180d`) |
| pre-existing rows byte-identical to base | **PASS** | `git diff -U0 corpus/SOURCES.md` (worktree vs index) → empty; `git diff --numstat b374feb..HEAD -- corpus/SOURCES.md` → `3 0`; 47-row block sha256 identical at base and at HEAD-minus-S048 (`fd039ca9…`) |

### Staged `S080` → landed `S048`, cell by cell

| cell | staged `SOURCES.append.md:56` | landed `SOURCES.md:54` | verdict |
|---|---|---|---|
| id | `S080` | `S048` | mapped by DOCUMENT. Staged `S048` is a **different** document (`全国标准信息公共服务平台 标准计划 20260806-T-469 — https://std.samr.gov.cn/…`); staged `S080`'s URL is byte-equal to the landed URL (`od -c` identical). `S048` was free in the lane pre-append (47 rows, max `S047`). Correct. |
| source | `Microsoft Security Vulnerability Research — https://…/msvr` | same + `(MSVR)` | matches the page's own heading (L28). |
| kind / tier / status | `docs` / `A` / `mined` | identical | unchanged, correctly. |
| scope | "Microsoft's programme for handling vulnerabilities found in third-party products, and the routes by which those findings arrive" | scoped to Microsoft's own statement, "and of nothing beyond it", plus the three roles | narrowed to the tier's scope; not global. |
| anchor | `the paragraph beginning "MSVR learns … in three ways", with the three routes` (no lines, no date) | capture + L28/L29-L30/L31/L32-L34/L35 + no-date statement + opened date | staged form failed the anchor contract; landed form fixes it (§1.3–§1.4). |
| teaches | `A vendor's own research programme is a third intake route …` (generic) | `Microsoft's MSVR states it learns …` with per-line cites | staged cell generalizes one vendor page into a rule about vendors (QUALITY Q4); the rewrite attributes to the stating party. Correct trade. |
| opened | `2026-10-23` | `2026-10-25` | rule 1 satisfied. |
| recheck | `180d` | `180d` | unchanged. |
| used-by | `corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md` | `corpus/knowledge/vendor-third-party-finding-coordination.md` | resolves; the staged filename does not exist in the lane. |

---

## 4. Findings by severity

**HIGH / MEDIUM — none.** No cell of the landed row is false against the fresh bytes; no immutable field was edited; no pre-existing row changed.

- **LOW-1 — the two lesson-side halves of rules 1 and 2 are unlanded.** `test -e corpus/lessons/round-31.md` → `ABSENT` (2026-10-26T00:25Z). Rule 1's `## Gate` record and rule 2's old→new logging live there; the Gate exists only as the wave-1 draft `wave1/ScribeGateDraft.md:42`, which is evidence, not the lesson. Owner: `ScribeLesson` (not this seat's write path). Closure check: `test -s corpus/lessons/round-31.md && grep -q 'S048' corpus/lessons/round-31.md` exits 0 only once the Gate row lands. Related drift the L1 should route: `corpus/QUALITY.md` R16/R17 already cite `corpus/lessons/round-31.md` § Mistakes while that file does not exist (`grep -n 'round-31.md' corpus/QUALITY.md`) — a reference-drift risk, in `ScribeQualityFix`'s path, not the row's.
- **LOW-2 — the anchor carries no inline revision identifier.** The page has no visible publication or revision date (§1.4), so the row states the absence and the byte identity lives one hop away in `manifest.json` (`sha256 2001ad77…`). This is exactly the S004 (`page shows no publication or revision date, opened …`) and S043–S047 (capture-pinned) precedent, so it conforms; the residual is that a reader of `SOURCES.md` alone cannot tell which bytes `L28–L35` denotes. No in-place repair is available: `scope`/`anchor` are immutable under R8, so any tightening is a `supersedes S048 —` row, which is not warranted for a compression the manifest already binds.
- **NOTE N1 — `teaches` is descriptive and 33 words / two clauses.** `teaches` word counts measured over the registry: S048 = 33, corpus median 19, max 53 (S040 = 51, S036 = 41, S047 = 8). The contract's ≤25-word cap binds the †Gate quote†, not the cell, and the lane's own accepted cells run to 53 words, so no bar is breached. Taste note only: the cell answers "what does this page state" rather than "what does a reader gain"; the staged cell's benefit framing was dropped deliberately because its generic subject ("A vendor's own research programme") failed Q4. Leaving the attribution is the correct choice.
- **INFO-1 (pre-existing, not caused by this round) — R6 line-ref drift below the insert point.** `corpus/lessons/round-29-verifier-spotcheck.md:74` cites `SOURCES.md:83`. Measured: at base `b374feb`, L83 = `- S042 row added: …` and the S043 R8 note it means sat at L85; at HEAD L83 = `- S040 recheck cell restored …` and the S043 note is L87. The citation was **already** mislocated at base, so the S048 landing did not newly break a correct citation; this round's two inserts (row L54, search log L72) shift lines ≥54 by +1 and ≥72 by +2. Out of my row scope and out of my write scope; routed to the L1.
- **INFO-2 (pre-existing) — `§ Registry changes` bullet missing its marker.** HEAD `SOURCES.md:87` reads `Change cell old → new: the S043 anchor …` with no leading `- `; the same missing marker is at base L85, so it is not attributable to this round's append. It sits in the list the S048 note was appended to; routed to the L1, not repaired here (append-only file, S048 change log is not mine to reformat).

## 5. Residual risk and verification gaps

1. **Currency is unmeasured.** §1 is a single-instant re-open (2026-10-26T00:25Z, one host, three fetches across two seats). It shows the committed capture equals the live page about 55 minutes after capture; it says nothing about tomorrow, and `source-recheck.py` on this manifest re-reads the committed file, not the network. Drift over 90/180 days is unobserved [INFERENCE: standing institutional page, low churn — unmeasured].
2. **Whole-file digest is not reproducible from a re-fetch** because snapshot L2 rotates its Trace Id per request; only the committed file's digest is reproducible. Whole-file sha equality would false-alarm on every re-fetch. The row is safe because its claims are line-anchored and quote-asserted (§1.6), not hash-on-refetch.
3. **Rule 1/2 lesson halves cannot be verified from committed bytes until `corpus/lessons/round-31.md` lands.** If it lands with an S048 Gate row that omits the URL, the access date, or the located ≤25-word quote, rule 1 fails retroactively and the row needs a lesson erratum, not a row edit.
4. **Tier A is a curation claim about this page only.** Nothing in this review says MSVR's routes are how other vendors behave, and the row does not claim it; a future entry generalizing MSVR's three routes into a vendor-universal rule would be a Q4 failure of the entry, not of this row.
5. **No second reviewer was consulted on `teaches` phrasing (N1).** The judgement that the cell is "one grounded benefit" is mine; the grounding and the word count are measurements and stand independently.
