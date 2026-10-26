# RevGateSpot — round-31 Gate discernment spot-check

Seat `RevGateSpot` (leaf; no delegation, no swarm, no background job spawned by me — one shell poll was
auto-backgrounded by the tool and is disclosed below). Round kasegi-shokunin 31, wave 2, falsify wave.
Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`;
HEAD at measurement `eecad59db166e0626ca2472e96ea48bc28a35153` (read-only `git rev-parse`).
Answering model actually run on: `opencode-go/deepseek-v4.1-flash` (runtime route; no model passed by this seat).
Tools installed or upgraded: **none** (no pacman transaction — host pause respected; no uv/npx/binary download;
`curl`, `grep`, `sha256sum`, `wc`, `python3` stdlib, read-only `git` only).
No git/jj mutation. No package tool run. No write outside this receipt. No network beyond the one URL item (a)
names (`https://www.microsoft.com/en-us/msrc/msvr`, instrument UA), fetched twice.

**Verdict label: `lane-seat`.** I am a seat this lane dispatched; nothing below is offered as an independent
(non-author) closure. The four items were re-derived from bytes and from two fresh fetches rather than restated
from the receipt under review, but the adjudication of my own checks stays with the non-author reviewer.

Polling: my item's file `.ufo/waves/round-31/wave2/ScribeLesson.md` was absent at 21:31 local; the poll
(`until [ -s … ]; do sleep 20; done`, cap 2100 s) was auto-backgrounded as `bg_20963` and returned
`polls=16 elapsed=320s` with the file present at 14999 B. The subject under review, `corpus/lessons/round-31.md`,
landed at 21:37 while the poll was still running, so I waited on the file's digest instead: stable at
`be2c993e30047f694740d425ca0ba248c1911c2b08076d139657f63ee896a1f5` (149 lines, 50258 B) after three
consecutive equal reads 25 s apart; every Gate line quoted below is from that digest. `corpus/lessons/round-31.md`
§ Open items item 10 states `RevGateSpot.md` "were still absent at composition, so the final scope sweep and the
gate spot-check are owed" — this receipt is that owed check.

Host condition, disclosed because it touched one command: `/tmp` reported `128G … 8.4M avail 100%` during this
seat's window. The first fresh fetch exited `curl: (23) client returned ERROR on write` with `http=200 bytes=0`;
the retry with `--output` wrote `81802` bytes and was used. No lane byte was affected.

---

## Verdict summary

| item | verdict | reason (one line) |
|---|---|---|
| (a) S048 registry row's located anchor against a fresh fetch | **AGREE** | two independent fresh fetches (HTTP 200, 81802 B) reproduce the committed 97-line capture except line 2; every manifest quote and every anchor line (L28, L29-L30, L31, L32-L34, L35) verifies exactly once, in its cited line |
| (b) assimilation ADMIT: staged `S080` → lane `S048` by document | **AGREE** | the URL field is byte-for-byte identical (41 chars), the URL is absent from the base registry, staged `S048` is a different document, and the R8 bullet records the mapping as by-document |
| (c) assimilation REFUSALs: stated failing criteria and flip conditions | **AGREE**, one numeral corrected | every lane-side failure re-checked true on the staged bytes; one count in the wave-1 receipt is wrong (two quote-marked Chinese phrases, not three) and the lesson already dropped the numeral |
| (d) id-collision evidence and guard proof | **AGREE on the digits, DISAGREE on the word "guard proof"** | `reg-ids`/`staged-ids`/`collisions` reproduce byte-for-byte on the base blob; the artifact called a guard proof is the first collision id, not a sensitivity demonstration — I supply the missing fixture |

---

## (a) S048 row located quote vs a fresh fetch — AGREE

Subject: `corpus/SOURCES.md:54` anchor cell, `corpus/source-snapshots/round-31/S048.txt`,
`corpus/source-snapshots/round-31/manifest.json`, `corpus/knowledge/vendor-third-party-finding-coordination.md`
(head `f15`, digest `1f16e371…`).

### Pins (measured this seat)

```
$ sha256sum corpus/source-snapshots/round-31/S048.txt corpus/source-snapshots/round-31/manifest.json \
            corpus/knowledge/vendor-third-party-finding-coordination.md
2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55  corpus/source-snapshots/round-31/S048.txt
b80f7f92fbab57c0edbb73d181414560fe0e5e7102405f210865acc84a2f87be  corpus/source-snapshots/round-31/manifest.json
1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb  corpus/knowledge/vendor-third-party-finding-coordination.md
$ wc -lc corpus/source-snapshots/round-31/S048.txt corpus/knowledge/vendor-third-party-finding-coordination.md
   97  3755 corpus/source-snapshots/round-31/S048.txt
  160 11501 corpus/knowledge/vendor-third-party-finding-coordination.md
```

These equal the lesson Gate's cited values (`sha256 2001ad77…c67e55`, `3755 B / 97 lines`; entry
`1f16e371…`, `160 lines, 11501 B`).

### The instrument's own check

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

### Fresh fetch (the clause the counter cannot supply)

```
$ curl -sS -L --max-time 60 -A 'kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)' \
       -o msvr.html -w 'http=%{http_code} bytes=%{size_download}\n' https://www.microsoft.com/en-us/msrc/msvr
http=200 bytes=81802
```

Both fetches rendered with the lane's own `capture-source.py::html_to_text` and compared to the committed capture:

| pair | line count | differing lines |
|---|---|---|
| committed `S048.txt` vs fetch 1 | 97 / 97 | **1** — line 2, `This is the Trace Id: f97e6b1c…` vs `…7da35133…` |
| committed `S048.txt` vs fetch 2 | 97 / 97 | **1** — line 2 only |
| fetch 1 vs fetch 2 | 97 / 97 | **1** — line 2 only (`7da35133…` vs `9e2bc20c…`) |

So the capture is the live page, not a paraphrase: outside the per-request trace id the two fetches and the
committed capture are byte-identical, and each fetch is exactly `81802` B. This independently reproduces the
critic's re-fetch (`wave1/CritC2Kill.md` §0: code 200, 81802 B, diff = line 2 only) and the three wave-2
re-opens the lesson Gate cites.

### Row and manifest quote locations, checked against the fresh text

Each quote normalized (capture markup stripped, whitespace collapsed — `source-recheck.py::normalize`), then
counted in the fresh page and searched inside its cited line range:

| id | occurrences in fresh | words | cited lines | present in cited lines |
|---|---|---|---|---|
| Q1 | 1 | 10 | L31 | yes |
| Q2 | 1 | 19 | L32 | yes |
| Q3 | 1 | 6 | L33 | yes |
| Q4 | 1 | 14 | L34 | yes |
| Q5 | 1 | 11 | L35 | yes |
| Q6 | 1 | 11 | L35 | yes |
| Q7 | 1 | 9 | L35 | yes |
| Q8 | 1 | 11 | L35 | yes |

Every manifest quote is ≤25 words (max 19). The registry row's own anchor cells verify line by line against the
fresh text: L28 = `Microsoft Security Vulnerability Research (MSVR)` (the heading), L29-L30 = the purpose
paragraph, L31 = `MSVR learns about vulnerabilities in third-party products in three ways:` (also
`grep -c 'in three ways'` → 1, `grep -ci only` → 0), L32-L34 = the three labelled routes
(`grep -cE '^(Internal Microsoft engineers|External reports …|Internal research projects):'` → **3**), L35 = the
three-role CVD sentence, and L33 carries the source typo the entry discloses
(`grep -c 'third-party product of affects both'` → 1).

The row's "page shows no visible publication or revision date" also holds on the fresh text: no
`20\d\d-\d\d-\d\d`, no `Month D, YYYY`, no `published`/`last updated` marker in the extracted text (0 hits each).

Entry self-checks re-run on the committed capture, all matching the counts the entry itself states:

```
FC-1 labelled routes=3   in three ways=1   only=0
FC-2 coordinator sentence=1
FC-3 clock terms=0   @microsoft=0
FC-4 body bounty=0   whole-file bounty=1 (L15 nav item)
FC-5 affected vendor=2 (L32, L34)   CERT/CC=0 JPCERT=0 IPA=0   cert=1 (L48 "Certified Refurbished")
```

and the negative sweep the entry says a reader can run prints exactly one file per term:

```
$ for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities'; do printf '%s -> ' "$t"; grep -rli -- "$t" corpus/knowledge/*.md | tr '\n' ' '; echo; done
MSVR -> corpus/knowledge/vendor-third-party-finding-coordination.md
MSRC -> corpus/knowledge/vendor-third-party-finding-coordination.md
research programme -> corpus/knowledge/vendor-third-party-finding-coordination.md
coordinator of vulnerabilities -> corpus/knowledge/vendor-third-party-finding-coordination.md
```

Entry header hygiene: one `source:` line naming S048, `S080` absent (0), `F20` absent (0), `curl` absent (0),
`recheck:` parses (`bash -n` ok) and exits 0 from a foreign cwd (`cd /tmp` → `recheck_exit=0`, last lines
`S048:Q7 OK`, `S048:Q8 OK`).

One convention note, not a defect: the registry row's `anchor` cell carries section names plus line ranges but no
verbatim ≤25-word quote; that matches the lane's own rows (e.g. S004's anchor) and Q3's site is the knowledge
entry, which does carry located quotes.

**Verdict (a): agree.** The located quote and the anchor survive a fresh fetch; the only non-reproducible byte is
the disclosed trace id.

---

## (b) Assimilation ADMIT, staged S080 → lane S048 by document — AGREE

Compared cell against cell, read-only, on `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md:56`
and lane `corpus/SOURCES.md:54`:

```
lane  : 'https://www.microsoft.com/en-us/msrc/msvr'
staged: 'https://www.microsoft.com/en-us/msrc/msvr'
equal : True len 41
```

Byte-for-byte equality of the URL field, no normalization applied. Supporting checks:

- the URL was on **no** lane row at base: `git show b374febb…:corpus/SOURCES.md | grep -ic 'msrc\|msvr\|microsoft'`
  → **0**, and `grep -cE '^ {0,3}\|[[:space:]]*S048[[:space:]]*\|'` on the same blob → **0**; the round-31 snapshot
  directory does not exist in the base tree (`git ls-tree -r b374febb -- corpus/source-snapshots/round-31` → empty).
  So S048 is a genuinely new document, not a re-registration.
- the lane's new `S048` is **not** the staged `S048`: `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md:24`
  is `| S048 | 全国标准信息公共服务平台 标准计划 20260806-T-469 — https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A…`,
  a different document under the same id — which is exactly why adoption has to be by document.
- cells that changed are the ones the lesson's normalization notes claim: `opened 2026-10-23` → `2026-10-25`
  (admitting round), `used-by …-2026-10-23.md` → `…coordination.md` (path resolves; the C2 predicate counts it),
  `scope`/`teaches`/`anchor` rewritten, `kind docs`/`tier A`/`status mined` preserved, `recheck 180d` preserved.
- the mapping is recorded on the landed bytes, not only in the lesson: `corpus/SOURCES.md:94` reads
  "`id S080` → `S048` (mapped by DOCUMENT, URL equal — staged S048 is a different document)".

**Verdict (b): agree.** The admission is by document on byte-equal URLs, the new row is new, and the same-id
coincidence is disclosed where a reader of the registry will meet it.

---

## (c) Assimilation REFUSALs — AGREE with one numeral correction

Package digests re-measured, all equal to the wave-1 scout's set:
`SOURCES.append.md 4fe049cbe…` , `MERGE-REPORT.json 8a42a910…`,
`vendor-third-party-finding-coordination-2026-10-23.md 48e9de4e…`, `program-scope… 120d8cd5…`,
`claim-packaging… 6ad64d78…`, `cn-crowdsourced… a5302aaf…`, `chinese-crowd-testing-national-standard… 6c15d941…`,
`chinese-criminal-thresholds-and-authorisation.md 1660c00c…4e8a59ae` (the fifth, standing refusal the lesson
adds). The package did not move between the scout and this check.

Per refusal, I opened the staged entry and re-ran the criterion that is claimed:

| staged entry | stated failure | measured on the staged bytes | flip condition present |
|---|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` | Q1 staged ids + colliding `ground: F09` + prose recheck; Q2 S034/S035 unregistered; Q3 no located quote; Q4/Q5 universal; Q7/Q10 | `source: S031/S034/S035` (3 lines), `ground: F09 (new frontier item; extends F03…)`, `recheck: 90d — \`curl …\`` → `bash -n`: `unexpected EOF while looking for matching `''`; **zero** `L<n>`/`p.<n>`/page refs in the file; the quoted fragments are hypotheticals ("we will not pursue you for doing X"), not source text; L28-L29 assert "every platform's scope list is a restatement of that ownership"; none of S034/S035 URLs is on any lane row (0 hits each); the HackerOne half is lane-held (F13 entry quotes S043 L31; lane S043 URL = `hackerone.com/security/policy_versions`) | yes |
| `claim-packaging-and-report-quality.md` | Q1 ground + prose recheck; Q2 rows unregistered; Q3 quotes without page/line; Q4 regional universal; Q5; Q7/Q10 | `ground: F11 (new frontier item)` (lane F11 = ISO 29147/30111); `bash -n`: `syntax error near unexpected token '('`; S034/S035/S036 all 0 lane hits; the file carries **no** `L<n>`/`p.<n>`/page reference at all (`grep -nE '\bL[0-9]+\b\|\bp\.[0-9]+\b\|[Pp]age [0-9]+\|[0-9]+页'` → no match), its section pointers existing only in `source:` cells; "stricter than most Western platforms' published rules" and "it is standard practice in the Eastern programs" both present (L24, L44) | yes |
| `cn-crowdsourced-testing-roles-and-conduct.md` | Q1 no H1, ground not a frontier, prose recheck; Q2 S081/S082 unregistered, S082 drafting-stage; Q3 four located quotes but no revision/page and no exactly-once check | `grep -c '^# '` → **0**; `ground: round-6 ledger item 2`; `recheck: 90d — re-open both URLs and confirm the two quoted sentences` → `bash -n`: `syntax error near unexpected token '('`; S081/S082 0 lane hits; exactly 4 CJK quoted strings, each with a section/item pointer (S081 五、…item 2/3; 一、…item 1; S082 范围和主要技术内容) and none with a revision or page; the entry's own Limits calls S082 "the **project record** (drafting stage)" | yes |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | Q1 ground + prose recheck; Q2 rows unregistered; Q3 zero quote-marked strings; Q5; marginal to PROVINCE | `ground: F24 (new frontier item…)`; `bash -n`: `syntax error near unexpected token '('`; `grep -c '"'` → **0**; the `描述了…角色以及职责…` sentence appears unquoted at L25; S077/S078/S079 0 lane hits | yes |

The standing refusals also hold: round-29 (`corpus/lessons/round-29.md:137-138`) and round-30
(`corpus/lessons/round-30.md:44-45`) refused the first two on the same Q2/Q3/Q7/Q10/ground grounds, and round-30
(`:43`) refused `chinese-criminal-thresholds-and-authorisation.md`, whose staged `S044`/`S045`/`S046` are
Chinese legal documents while lane `S044`/`S045`/`S046` are Bugcrowd taxonomy, Bugcrowd `cwe.json` and the IPA JVN
report — the id-space collision the lesson names.

No bar was relaxed and nothing was copied: none of the six staged digests occurs in any file under `corpus/`
(`sha256sum` scan over `corpus/**/*.md`, 0 matches per digest), and the landed F15 entry is a rewrite, not the
staged bytes (`1f16e371…` vs `48e9de4e…`).

**Correction (low).** The wave-1 receipt the Gate cites says the claim-packaging entry carries "three quote-marked
Chinese phrases" (`wave1/ScoutPackageThemes.md` §3(c)). The staged file contains exactly **two** ASCII-quoted
CJK strings — `"仅从理论层面说明漏洞的存在而无利用\n和复现过程将不予收录"` (spans a line break) and
`"拒绝无实际危害证明的扫描器结果"`; the `降级场景` items sit in parentheses, unquoted. The criterion survives
unchanged (neither quote carries a page or line, and no lane capture exists for either platform), and the lesson
Gate already drops the numeral ("quote-marked Chinese phrases with no page/line"), so no gate decision moves —
but a reader reproducing the wave-1 number gets 2.

**Verdict (c): agree**, with the numeral above corrected and one framing caveat: the ordering "nearest to a flip"
is a routing priority computed from how many rows each entry would need, not a claim that the flip would then pass
Q1-Q10; the shutdown of each refusal rests on the lane-side criteria above, which I re-checked, not on that
ordering.

---

## (d) Id-collision evidence and the guard proof — digits agree, the word "guard proof" does not

### Reproduction on the base blob (byte-for-byte)

```
PAT='^ {0,3}\|[[:space:]]*S[0-9]{3,}'
git show b374febb…:corpus/SOURCES.md > base-SOURCES.md
grep -oE "$PAT" base-SOURCES.md | sed -E 's/^ *\| *//' | sort > reg-ids
grep -oE "$PAT" /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md | sed -E 's/^ *\| *//' | sort > staged-ids
comm -12 reg-ids staged-ids > collisions

sha256sum reg-ids staged-ids collisions
ab66f54a2135cea0359318caabb77575740093a32d7be7eb4bde47687be373c9  reg-ids
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  staged-ids
ac78cd564ab864b574e0d54d4e4656d448439403839530bb3044d04175acd2d2  collisions
lines: 47 94 17
```

All three digests are byte-equal to `.ufo/waves/round-31/assimilation/{reg-ids,staged-ids,collisions}`. The guard
id is a real collision, not a pattern artefact:

```
lane   S031 = CVE Numbering Authority Operational Rules v4.2.6 — https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf
staged S031 = HackerOne standard program policy set — https://hackerone.com/security/policy_versions
```

### What the artifact called `guard-proof-collisions` actually is

*(`corpus/lessons/round-31.md` § Gate cites this paragraph as `wave2/RevGateSpot.md` §3.)*

It is 5 bytes, `S031\n` — the first line of the collision set. The lesson Gate describes it correctly as
"first collision id" with two byte-equal candidate producers (`head -1`, `grep -x 'S031'`), which I reproduced
(`xxd` → `5330 3331 0a`). That is a **provenance** proof (which command produced the file), not a **sensitivity**
proof (that the 0-3-space pattern is required). Round 28's guard proof was the latter: an indented fixture row the
wide pattern catches and `^\|` misses (`.ufo/waves/round-28/assimilation/guard-proof.sh` §A vs §B). No such
fixture exists in the round-31 tree, and the round ships the scratch outputs without the producer script that
round 28 kept beside them.

I built the missing fixture in scratch (`/tmp/rgspot/ids/fx`) — a lane registry with `  | S031 |` indented two
spaces against a staged set carrying `S031` at column 0:

```
-- A guard pattern (0-3 leading spaces) --
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' fx/fixture-SOURCES.md | grep -oE 'S[0-9]+' | sort   # -> S030 S031 S047
$ comm -12 a-reg a-st                                                                             # -> S031
a-col lines=1
-- B column-zero-only pattern (^\|) --
b-col lines=0
```

So the guard's discriminating power is real and demonstrable; it is simply not demonstrated anywhere in this
round's committed evidence. That is an evidence gap of the O6 class, not a wrong digit.

### The number a reader gets on landed bytes

*(`corpus/lessons/round-31.md` § Gate cites this paragraph as `wave2/RevGateSpot.md` §2.)*

On the landed registry the set is **18**, not 17: the append makes lane `S048` collide in id-space with staged
`S048`, which is a different document.

```
landed reg-ids=48 staged=94 landed-collisions=18   (tail: S047, S048)
sha256 of landed collisions = e76f5f65f7c068fd5c1de59e2cffb3ec249d1f8db49ce5472a2f4f0df2059f2c
```

The lesson Gate's 17 is correct **because it says `comm -12` of the base-blob `reg-ids`**; what is missing is the
landed-state reading, so a later reader re-running the same command pair gets 18 and may treat the S048 member as
an unexplained new collision. One sentence — "on landed bytes the set is 18, `S031…S048`, the S048 member being
the document-different id the adoption deliberately leaves alone" — closes it.

**Verdict (d): digits agree (byte-for-byte on base); disagree with the term "guard proof" as applied to
`guard-proof-collisions`, which is a first-element provenance artifact. The sensitivity proof is supplied above.**

---

## Findings on the Gate text (severity ordered)

**F1 — MEDIUM (verifiability): two base-state readings are cited with commands that do not reproduce on landed
bytes.** `corpus/lessons/round-31.md` § Gate — id-collision evidence reads: "`S048` was free in the lane
(`grep -cE '^ {0,3}\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md` → 0)" and "no lane row carried the MSVR
URL before this round (`grep -ic 'msrc\|msvr\|microsoft' corpus/SOURCES.md` → 0)".

```
$ grep -cE '^ {0,3}\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md      # landed
1
$ grep -ic 'msrc\|msvr\|microsoft' corpus/SOURCES.md                          # landed
3
$ git show b374febb…:corpus/SOURCES.md | grep -ic 'msrc\|msvr\|microsoft'     # base
0
```

The claims are true — both are past-tense statements about the state before the append, and the trace-id/entry
digests around them are current — but the two bracket commands are recorded without the state that produced the
0, so neither reproduces as written. This is the M31-1 family (a filed number outliving the bytes that produced
it) appearing in the lesson that catalogues that family, and the same paragraph's own collision table does it
correctly ("on the **base blob**"). Smallest fix: prefix both invocations with
`git show b374febbb33ccadade78a787279707fd5d2e6e1d:corpus/SOURCES.md |` or annotate "(base blob, `b374febb…`)".
Note the draft this lesson integrated had the present-tense form of the same sentence, which the lesson corrected
to "before this round"; only the command qualifier is still owed.

**F2 — LOW (number vs. receipt): the wave-1 refusal reason overcounts quote-marked Chinese phrases.** See (c):
`wave1/ScoutPackageThemes.md` §3(c) says three; the staged file has two. The lesson Gate already omits the
numeral, so no decision moves; the wave-1 receipt keeps a number that does not reproduce.

**F3 — LOW (evidence): the id guard's sensitivity is asserted, not shown.** `assimilation/guard-proof-collisions`
is the first collision id; nothing in the round demonstrates that the 0-3-space pattern is required (round 28's
`guard-proof.sh` did). My fixture in (d) supplies it; the lesson should either cite such a run or stop calling the
artifact a guard proof.

**F4 — LOW (completeness of a reproduction datum): the landed collision set is 18, not 17.** Stated in (d); the
base-blob 17 is right, the landed 18 is unstated, and the S048 member is the interesting one.

**F5 — INFO (held, verified): no Q/R bar was relaxed.** Every refusal's criteria re-check true on the staged bytes,
every flip condition names the rows that must be captured, six staged digests appear in no lane file, and the
landed entry is a rewrite (`1f16e371…`) rather than the staged bytes (`48e9de4e…`).

---

## Residual risk

1. **The pin binds committed bytes.** Whole-file sha equality will never reproduce from a refetch because line 2
   is a per-request trace id (the committed capture plus two fetches by this seat gave three different values:
   `f97e6b1c…`, `7da35133…`, `9e2bc20c…`). What a
   reader can reproduce is "identical except L2", which held for both of my fetches and both of the wave-2
   re-opens. Upstream edits after 2026-10-25 are unobservable until the next recheck; the manifest records no
   `url`/`fetched_utc` (routed, not landed — `wave1/CritC2Kill.md` §4/§6.2).
2. **Currency is a single-instant observation.** My two fetches are one host, minutes apart, inside the same
   hour as the wave-2 re-opens; drift over the 90/180-day cadence is unmeasured, as the lesson's open item 8 says.
3. **The counter family cannot see a fabricated capture** (Gate caveat 1). My (a) check is exactly the
   prose-level check that clause says is doing the work; it does not change the routed status of the two
   instrument fixes.
4. **Id-space collisions recur by design.** Each appended row raises the landed collision count; the guard's job
   is to keep adoption by-document, and the lesson should carry the landed numbers so the growth is expected
   rather than rediscovered.

## Verification gaps (what this seat did not check)

- C1's 13-limb ledger, the counter, and the counter-mutant results are out of my item's scope (four Gate checks);
  of the lane's instruments I ran only `source-recheck.py`, `frontier-recheck-count.py`, `capture-source.py`'s
  `html_to_text` (as a renderer) and the census validator. The census run below is a shape check, not a claim audit.
- `corpus/instruments/frontier-recheck-count.py` and the C2 counter commands were re-run once on quiescent bytes
  to confirm the Gate's after column (`admitted=15`, `registry_rows=48`, `rows_S048=1`,
  `entries_citing_S048=1`, harness `entries=18 pass=18 exit=0` including `PASS F15 … ids=S048`, census
  `exit=0` with only `W04 S028`, `W04 S029`); I did not audit the harness's own internals.
- I opened the six assimilation-set entries and the four refusals' evidence; the remaining ~38 package entries
  were not opened (item scope: the theme set and the refusals).
- No sibling receipt was used as evidence for any verdict above; `wave2/RevRowS048.md`, `RevQuoteRoutes.md`,
  `RevEntryQ.md` and `RevQuoteRoles.md` were only grepped afterwards to confirm F1-F4 are not already filed by
  them (they are not).

## Reproduce (read-only; run from the lane root unless stated)

```
sha256sum corpus/source-snapshots/round-31/S048.txt corpus/source-snapshots/round-31/manifest.json \
          corpus/knowledge/vendor-third-party-finding-coordination.md
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048
curl -sS -L -A 'kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)' \
     -o /tmp/msvr.html -w 'http=%{http_code} bytes=%{size_download}\n' https://www.microsoft.com/en-us/msrc/msvr
# render with corpus/instruments/capture-source.py::html_to_text and diff against the capture: 1 line, L2
PAT='^ {0,3}\|[[:space:]]*S[0-9]{3,}'
git show b374febbb33ccadade78a787279707fd5d2e6e1d:corpus/SOURCES.md | grep -oE "$PAT" | sed -E 's/^ *\| *//' | sort
grep -oE "$PAT" /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md | sed -E 's/^ *\| *//' | sort
grep -c '^# ' /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/cn-crowdsourced-testing-roles-and-conduct.md
grep -c '"'  /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/chinese-crowd-testing-national-standard-2026-10-23.md
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
python3 corpus/instruments/frontier-recheck-count.py
```

---

## Bounds and provenance

Wrote only this file. Did not write: the lane's corpus (instruments, entries, registry, README, SKILL.md,
PROVINCE.md, QUALITY.md, SCORECARD.md, LOG.md, lessons), `.ufo/state/`, `.ufo/watchdog.log`, `MANIFEST.json`,
`templates/`, `scripts/`, `/home/vgpnk/Projects/shokuknow` (read-only; no campaign tool run), the fleet root, or
any sibling lane. No git/jj mutation (read-only `rev-parse`, `show`, `ls-tree`, `status`, `grep`). Scratch lives
in `/tmp/rgspot` and is deleted at close. No credential material, session URL or vault reference in this file.
Quotes are ≤25 words with their location; every number above is copied from a command output in this receipt or
from the named file at the measured digest.

---

## Amendment — lesson re-pinned after the fixes (F1-F3 applied)

The Gate lines quoted above come from `corpus/lessons/round-31.md` at
`be2c993e30047f694740d425ca0ba248c1911c2b08076d139657f63ee896a1f5` (149 lines). `ScribeLesson` then applied F1-F3
and reported the file at `3f3a5501ede104fcda3e5b7511bcf2eb71c1c8aa56b08cd1bddfaddb75762503`. Re-measured here:

```
$ sha256sum corpus/lessons/round-31.md ; wc -lc corpus/lessons/round-31.md
3f3a5501ede104fcda3e5b7511bcf2eb71c1c8aa56b08cd1bddfaddb75762503  corpus/lessons/round-31.md
    161  51728 corpus/lessons/round-31.md
$ git show b374febb…:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S048[[:space:]]*\|'   # base
0
$ git show b374febb…:corpus/SOURCES.md | grep -ic 'msrc\|msvr\|microsoft'                      # base
0
$ grep -cE '^ {0,3}\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md                         # landed
1
$ grep -ic 'msrc\|msvr\|microsoft' corpus/SOURCES.md                                            # landed
3
```

What the re-pinned Gate now carries, checked by reading it and by running the described fixtures:

- **F1 closed.** Both readings are now prefixed with
  `git show b374febbb33ccadade78a787279707fd5d2e6e1d:corpus/SOURCES.md |`, printing **0** and **0**, with the landed
  values (**1**, **3**) stated beside them and a sentence saying the prefix is deliberate because the numbers do not
  reproduce on the tree that now holds the row. This is the form I asked for.
- **F4 closed by a count-basis paragraph** rather than by editing the 17: the `collisions` artifact is base-blob vs
  staged, 17 stands on that basis, and the same extractor on landed bytes reads **18** with the extra member named as
  this round's own `S048` row ("a count-basis difference, not an additional collision"). I reproduced both bases
  (17 and 18).
- **F3 closed.** `assimilation/guard-proof-collisions` is relabelled "provenance only — it names *which* id collided
  first, not that the pattern is discriminating", and a measured fixture paragraph follows: indented `  | S031 | x`
  → tolerant `^ {0,3}\|[[:space:]]*S[0-9]{3,}` = **1**, strict `^\|` = **0**; a bare `S031` at column 0 → 0/0. That is
  the same discrimination my own fixture showed (mine used a staged table row rather than a bare id line, hence my
  `0`/`1` complements), and it is now evidence rather than assertion.
- **F2 acknowledged, not acted on.** The Gate still omits the numeral; `wave1/ScoutPackageThemes.md` §3(c) keeps its
  "three", so the wave-1 receipt remains the wrong-numbered artifact a reader may hit. Not a Gate decision.
- The lesson's citations `wave2/RevGateSpot.md` §2 and §3 now resolve: I marked the count-basis paragraph (§2) and the
  guard-sensitivity paragraph (§3) in section (d) of this file.

**No verdict changes.** (a) and (b) stand on bytes that did not move; (c) still agrees with the four refusals and
still carries the numeral correction; (d) still reads "digits agree, the word 'guard proof' did not, sensitivity now
supplied". The fixes were corrections of provenance and naming, not of any gate decision, and no Q/R bar is relaxed by
them. Every other number in this receipt was measured before the lesson edit and is unaffected by it: the lesson is
not an input to any count above except the quotations.

