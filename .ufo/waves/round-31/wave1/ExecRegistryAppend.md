# ExecRegistryAppend — round 31 receipt (S048 registry append)

- Seat: `ExecRegistryAppend` (leaf). Round 31, wave 1. Lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`.
- Answering model: `devin/deepseek-v4-1-flash` (route-table resolution for this seat; no model passed).
- Write scope exercised: `corpus/SOURCES.md` (3 appended lines) + this receipt. Nothing else written. No git/jj mutation (only read-only `git show` / `git status` / `git log`); no network fetch; no tool installed or upgraded (python3 + coreutils + gawk only); no pacman transaction.
- Axes: depth:verifiability, coverage (C2 registry limb). No score move asserted.

## 0. Gates waited for (both present before any write)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ until [ -s .ufo/waves/round-31/wave1/ExecEntryF15.md ] && [ -s .ufo/waves/round-31/wave1/ExecCensusDry.md ]; do sleep 20; done
READY
-rw-r--r-- 12956 Oct 25 20:39 .ufo/waves/round-31/wave1/ExecEntryF15.md
-rw-r--r-- 19522 Oct 25 20:38 .ufo/waves/round-31/wave1/ExecCensusDry.md
-rw-r--r-- 10359 Oct 25 20:38 corpus/knowledge/vendor-third-party-finding-coordination.md
```

| Dependency | What it gates | Verdict taken |
|---|---|---|
| `wave1/ExecEntryF15.md` | the F15 entry whose path the row's `used-by` must resolve | landed entry `corpus/knowledge/vendor-third-party-finding-coordination.md` (10,359 B, 146 lines per its receipt); header L2 names `S048` |
| `wave1/ExecCensusDry.md` | pre-append census gate on the planned row | **PASS**: mirror `validate --file` exit 0, only base W04 S028/S029; negative controls E03/E04/E11 each exit 1; `rows 47 → 48` on the mirror |
| `wave1/ExecCapManifest.md` + `corpus/source-snapshots/round-31/manifest.json` | the capture the anchor cites | `S048.txt` 3755 B / 97 lines / sha256 `2001ad77…e55`; `--source S048` exit 0, 8 assertions |
| `wave1/RevSourceBar.md` | required cell rewrites vs staged S080 | **ADMIT-ROW** with 4 required rewrites (scope bounds tier A to Microsoft's own statement; anchor cites capture heading L28 + intro L29-L30 + L31 + L32-L34 + L35 + no-visible-date note; `teaches` attributed to Microsoft/MSVR for Q4; log the staged→landed cell changes under `## Registry changes`) |
| `wave1/ScoutF15Sweep.md`, `wave1/ScoutPackageThemes.md` | the Search-log note's counts | 43 knowledge files, ten terms, verdict `residual-exists`; package set 5 staged entries, 1 admit + 4 reject |

## 1. PRE-STATE (labelled: measured before this seat wrote anything)

```
$ sha256sum corpus/SOURCES.md
a126a5f339323d5ae417a944d163d75a0427d9c77a5a330308e193dc7b81d927  corpus/SOURCES.md
$ git show b374febbb33ccadade78a787279707fd5d2e6e1d:corpus/SOURCES.md | sha256sum
a126a5f339323d5ae417a944d163d75a0427d9c77a5a330308e193dc7b81d927  -
```

The live registry was byte-identical to the lane base blob at the moment of my first read (91 lines, 47 rows), so the
before/after below is a real before→after on quiescent bytes, not a comparison against another seat's in-flight edit.

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi   # PRE
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
47
```

## 2. The landed row (verbatim, line 54, directly after the S047 row)

```
| S048 | Microsoft Security Vulnerability Research (MSVR) — https://www.microsoft.com/en-us/msrc/msvr | docs | A | Microsoft's own statement of its MSVR programme and of nothing beyond it: the three third-party intake routes it lists, its coordination of them, and the three CVD roles it claims for itself | capture corpus/source-snapshots/round-31/S048.txt: heading Microsoft Security Vulnerability Research (MSVR) L28, purpose L29-L30, three-ways lead-in L31, routes L32-L34, three-roles sentence L35; page shows no visible publication or revision date, opened 2026-10-25 | Microsoft's MSVR states it learns of third-party-product vulnerabilities through its own engineers (L32), external MSRC reports (L33) and internal research (L34), and names itself finder and multi-vendor coordinator under its CVD approach (L35). | mined | 2026-10-25 | 180d | corpus/knowledge/vendor-third-party-finding-coordination.md |
```

Byte binding of the landed line (this seat's own digest, not carried from a peer):

```
$ sed -n '54p' corpus/SOURCES.md > /tmp/s048row.txt && wc -c /tmp/s048row.txt && sha256sum /tmp/s048row.txt && awk '{print length($0)}' /tmp/s048row.txt
916 /tmp/s048row.txt
0f2d9cb61c8743577476906fb6ea2a9285082931e5ff811dac98d0f26f83de7a  /tmp/s048row.txt
913
$ awk -F'|' '/^\| S048 /{print "NF=" NF}' corpus/SOURCES.md
NF=13
```

`NF=13` under `awk -F'|'` is 11 cells with no `|` inside any cell. The row differs from the `ExecCensusDry` planned text
on purpose: `RevSourceBar`'s ADMIT-ROW verdict required the anchor's heading/date note and a Q4-attributed `teaches`
cell, both of which the census gate does not read (§4 below is the same gate passing on these bytes).

Column-by-column, against the staged `S080` row (`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md:56`,
read-only):

| cell | staged S080 | landed S048 |
|---|---|---|
| id | `S080` | `S048` — mapped by DOCUMENT (URL equal); staged `S048` is a different document (the 20260806-T-469 standard-plan record) |
| source | `Microsoft Security Vulnerability Research — https://www.microsoft.com/en-us/msrc/msvr` | same URL, programme acronym added from capture L28 |
| kind | `docs` | `docs` |
| tier | `A` | `A` |
| scope | "programme for handling vulnerabilities found in third-party products, and the routes by which those findings arrive" | Microsoft's own statement of its MSVR programme **and of nothing beyond it** — three intake routes, its coordination of them, three CVD roles |
| anchor | prose paragraph pointer | capture path + heading L28 + purpose L29-L30 + lead-in L31 + routes L32-L34 + three-roles L35 + no-visible-publication-or-revision-date note, opened 2026-10-25 |
| teaches | generic "A vendor's own research programme…" | attributed: "Microsoft's MSVR states…", routes and roles cited by line |
| status | `mined` | `mined` |
| opened | `2026-10-23` | `2026-10-25` — the admitting round; the staged date is NOT inherited |
| recheck | `180d` | `180d` (bare cadence, census E09-clean) |
| used-by | `corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md` | `corpus/knowledge/vendor-third-party-finding-coordination.md` |

Anchor lines re-verified against the landed capture by this seat (not retyped):

```
$ awk 'NR>=28 && NR<=35 {printf "%d: %.60s\n", NR, $0}' corpus/source-snapshots/round-31/S048.txt
28: Microsoft Security Vulnerability Research (MSVR)
29: MSVR is a program specifically designed to help improve the securit
30: Microsoft’s goal is to share our collective experience in dealing wit
31: MSVR learns about vulnerabilities in third-party products in three w
32: Internal Microsoft engineers: In the course of their regular work, en
33: External reports to the Microsoft Security Response Center (MSRC): On
34: Internal research projects: As time and resources permit, Microsoft p
35: This coordination takes place under Microsoft's Coordinated Vulnerabil
```

## 3. The Search-log note (appended as the last bullet of `## Search log`, now line 72)

```
- Vendor third-party-finding coordination sweep (round 31); question: does the lane already hold "a vendor's research programme as an intake route for other vendors' bugs", and does the staged package's vendor entry add ground the corpus lacks; where: read-only the campaign package `/home/vgpnk/Projects/shokuknow/merge/kasegi/` (`SOURCES.append.md` plus its five staged knowledge entries), a ten-term negative sweep over the lane's own `corpus/knowledge/*.md` (43 files), `corpus/README.md`, `corpus/SOURCES.md` and `SKILL.md`, then the live `https://www.microsoft.com/en-us/msrc/msvr` page captured under the instrument UA into `corpus/source-snapshots/round-31/S048.txt`; date: 2026-10-25; identified 5 staged entries (10 staged source rows), screened 5, included 1, excluded 4. Included: the vendor third-party-finding coordination entry, admitted as Frontier F15 with new row S048 mapped by document (staged S080 → lane S048, URL equal). Excluded, with reason: `program-scope-rules-and-asset-boundaries` and `claim-packaging-and-report-quality` (standing round-30 refusals — the HackerOne half is already held by S043 and the rest fails Q2/Q3/Q7/Q10 on unregistered rows and prose rechecks); `cn-crowdsourced-testing-roles-and-conduct` (nearest to a flip: no H1 title, staged S081/S082 on no lane row); `chinese-crowd-testing-national-standard-2026-10-23` (zero quote-marked strings and a reframing the unread standard text cannot support). The ten-term sweep returned no hit for MSVR, MSRC or "coordinator of vulnerabilities" in any knowledge entry, README or SKILL.md, so the included entry's residual is real rather than a restatement. Stop: the bounded package set plus the lane's own ground answered the F15 question and one captured page supplied the located quotes; no wider target-facing research was run and no other staged entry was carried.
```

Every count in that note is the peer receipt's measured count, not a re-derivation:
`ScoutF15Sweep.md` — "Scope S = `corpus/knowledge/*.md corpus/README.md corpus/SOURCES.md SKILL.md` (43 knowledge files)" and its ten-term table; `ScoutPackageThemes.md` — "Gate requirement (>=1 admit, >=1 reject): met, 1 admit + 4 reject. Exactly one ADMIT." and the ten staged rows listed in its URL-join block. The stop rationale is the contract's PRISMA clause (question · where · date · identified/screened/included/excluded · reasons · stop).

## 4. The R8 line (appended last in `## Registry changes`, now line 94)

```
- S048 row added: new row (id `S048`, kind `docs`, tier A scoped to Microsoft's own statement of its MSVR programme, status mined, opened 2026-10-25, recheck `180d`, used-by `corpus/knowledge/vendor-third-party-finding-coordination.md`), anchor pinned to the round-31 capture `corpus/source-snapshots/round-31/S048.txt` (heading L28, purpose L29-L30, three-ways lead-in L31, routes L32-L34, three-roles sentence L35; the page shows no visible publication or revision date). Staged `SOURCES.append.md` S080 cells → landed: `id S080` → `S048` (mapped by DOCUMENT, URL equal — staged S048 is a different document); `opened 2026-10-23` → `2026-10-25`; `scope` and `teaches` rewritten to the registry's cell shape and to name Microsoft/MSVR as the stating party (Q4), the staged generic "A vendor's own research programme" not carried; `anchor` rewritten from the round-31 capture, the staged prose anchor not carried; `used-by` `corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md` → `corpus/knowledge/vendor-third-party-finding-coordination.md`. Registry 47 rows pre-append → 48 post-append; no other row's cell changed (R8).
```

## 5. POST-STATE — the target command, exit 0

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

Findings are byte-identical to §1's PRE run: the only lines are the two base W04 warnings (S028/S029), and the S048 row
adds **zero** findings — no E01/E02/E03/E04/E05/E06/E07/E08/E09/E10/E11/E12 and no new W-code.

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi
kasegi	rows	48
kasegi	tier.A	45
kasegi	tier.B	1
kasegi	tier.C	2
kasegi	status.mined	36
kasegi	status.queued	9
kasegi	status.rejected	3
FLEET	rows	48
FLEET	tier.A	45
FLEET	tier.B	1
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	9
FLEET	status.mined	36
FLEET	status.rejected	3
FLEET	status.invalid	0
FLEET	missing	0
census_counts_exit=0
```

47 → 48 rows, mined 35 → 36, tier.A 44 → 45 — the three C2 registry figures.

## 6. Contract census commands (each run by this seat, each output literal)

```
$ grep -cE '^\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md          → 1        (S048 appears exactly once)
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md    → 48       (registry rows)
$ awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/ && NF!=13 {c++} END{print c+0}' corpus/SOURCES.md
0                                                                                     (malformed rows = 0)
$ grep -oE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | sed -E 's/^\| *//' | sort | uniq -d | wc -l
0                                                                                     (duplicate ids = none)
$ awk -F'|' '/^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|/{gsub(/ /,"",$4); if ($4!="spec"&&$4!="docs"&&$4!="paper"&&$4!="code"&&$4!="tool"&&$4!="dataset"&&$4!="talk"&&$4!="book"&&$4!="community"&&$4!="own-work") print "BAD kind "$2}' corpus/SOURCES.md | wc -l
0                                                                                     (kind enum violations = none)
$ ... same shape on $5 (tier A|B|C) ... → 0                                           (tier enum violations = none)
$ ... same shape on $9 (queued|mined|rejected) ... → 0                                (status enum violations = none)
$ awk -F'|' '... split $12 on "," ...' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "MISSING $p"; done | wc -l
0                                                                                     (missing used-by paths = none)
$ awk -F'|' '/^\| S048 /{gsub(/^ +| +$/,"",$11); print "recheck=[" $11 "]"}' corpus/SOURCES.md
recheck=[180d]                                                                        (bare cadence, E09-clean)
```

Duplicate URL+scope (census E04) is covered by the POST validate run: no `E04` line and no `W04` line for S048, i.e. the
MSVR URL is unique across the 48 rows (the only W04 pair is the pre-existing S028/S029 one).

## 7. Captured-source recheck for the row's own source (re-measured here on quiescent bytes)

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048
S048:sha256 OK
S048:Q1 OK occurrences=1
S048:Q2 OK occurrences=1
S048:Q3 OK occurrences=1
S048:Q4 OK occurrences=1
S048:Q5 OK occurrences=1
S048:Q6 OK occurrences=1
S048:Q7 OK occurrences=1
S048:Q8 OK occurrences=1
recheck_exit=0
```

The anchor cell's `L28/L29-L30/L31/L32-L34/L35` claims are exactly the lines this seat printed in §2.

## 8. The edit is a pure addition (no pre-existing row touched)

```
$ git show b374febbb33ccadade78a787279707fd5d2e6e1d:corpus/SOURCES.md > /tmp/base-sources.md
$ diff /tmp/base-sources.md corpus/SOURCES.md | grep -c '^>'   → 3
$ diff /tmp/base-sources.md corpus/SOURCES.md | grep -c '^<'   → 0
$ wc -l /tmp/base-sources.md corpus/SOURCES.md                 → 91 / 94
$ sha256sum corpus/SOURCES.md
5a03c696312bd5fd8fe8307f75bd9723cac97fe3e44f0f3ba46a68607295f6f5  corpus/SOURCES.md
```

Three added lines (the S048 row, the Search-log bullet, the R8 bullet), zero removed or modified lines. No status,
recheck or used-by cell changed on any pre-existing row.

## 9. R6 disclosure — which cited line numbers moved, and why the move was unavoidable

The registry row must sit inside `## Registry` (census E12 fires on a row-shaped source outside it), so the append
inserts one line at line 54 and shifts everything below it. Measured cited anchors:

| citation | base `b374feb` line | now | effect |
|---|---|---|---|
| `corpus/lessons/round-25.md:90` → `SOURCES.md:22` | 22 | 22 | unchanged |
| `corpus/lessons/round-28.md:104` → `SOURCES.md:47` (S041 row) | 47 | 47 | unchanged |
| `corpus/lessons/round-28.md:193` → `SOURCES.md:46` (S040 row) | 46 | 46 | unchanged |
| `corpus/lessons/round-28.md:203` → `SOURCES.md:48` (S042 row) | 48 | 48 | unchanged |
| `corpus/lessons/round-29.md:214` and `round-29-verifier-spotcheck.md:74` → `SOURCES.md:83` (the S043 change-cell line) | **85 at base** | **87** | already stale by +2 before this seat (round-30's S046/S047 append); this round adds a further +2 (registry row + Search-log bullet) |

Every row-level citation (:22, :46, :47, :48) keeps its number, because the three inserts all land at or below line 54.
The two `:83` citations were broken by round 30 and are now further off; `corpus/lessons/**` is not this seat's path,
so the correction is routed here rather than written. The correct anchor for that line today is `SOURCES.md:87`
(`Change cell old → new: the S043 anchor originally describe…`), and `SOURCES.md:85` is the `- S042 row added:` line.

## 10. Risks, limits, blockers

- **No blocker.** Both dependency receipts existed, the capture and manifest were landed, and every counter this item names exits 0.
- **Not run by this seat, deliberately:** `python3 corpus/instruments/frontier-recheck-count.py` (the C2 harness counter). It reads the `## Frontier` row that `ScribeReadmeF15` owns; F15 is not yet an admitted README row on these bytes, so a run now would be PRE-STATE for the harness and is not cited anywhere. Its `entries=18 pass=18` figure belongs to the L1's post-integration gate.
- **Anchor is page-level only.** The capture states no clock, contact or agreement (`@microsoft` 0, `http` 0 per the entry receipt); the row's `teaches` cell claims only what L32-L35 state.
- **Line 2 of the capture is a per-request Trace Id**, so a refetch changes the capture digest. The row cites the pinned snapshot, never a re-fetch; the manifest records this quirk.
- **Row text vs the `ExecCensusDry` planned row.** The peer's planned row (§5 of its receipt, 794 B) omits the anchor's heading/date note and does not attribute `teaches` to Microsoft; `RevSourceBar`'s ADMIT-ROW verdict required both. The landed row (916 B, `0f2d9cb6…`) carries both and passes the same gate identically (§5).
- Tooling installed or upgraded: **none**.
