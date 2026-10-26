# CritC2Kill — C2 kill-rule and F15 candidate (round 31, wave 1)

Seat: critic (leaf). Scope: read-only review of C2's kill rule and the F15 entry; the only lane
writes are this receipt and `CritC2Kill-scratch/` (deleted except `live.txt`). No delegation, no
background jobs, no network beyond the one URL this item names. Tooling installed: none.

Answering model (rule 10, read from the harness project context; not passed by me):
`devin/deepseek-v4-1-flash`.

Bytes reviewed (2026-10-25T23:39:26Z):
```
bf40fd9e56351b3a857f5efc45c508889bde75b736915b5c3011c63d36eafa79  corpus/knowledge/vendor-third-party-finding-coordination.md
2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55  corpus/source-snapshots/round-31/S048.txt
b80f7f92fbab57c0edbb73d181414560fe0e5e7102405f210865acc84a2f87be  corpus/source-snapshots/round-31/manifest.json
```
PRE-STATE (bounds 6, M30-3): the registry row S048 and the README F15 row had not landed when I
read, so `frontier_admitted=14`, `registry_rows=47`, harness `entries=17 pass=17 exit=0`. Those
three numbers are before-columns only; nothing here compares them to an after. The entry, the
capture and the manifest had landed, so the critique below is against those bytes.

## VERDICT (short)

| question | verdict |
|---|---|
| (1) expansion credit | **holds narrowly** — only if the entry leads with the internal-research route, the self-coordinator role and the programme-as-object; r1/r2 alone restate F10 |
| (2) Q4 attribution | **staged text fails, landed text passes** — the staged "finder … obligation"/"must hand it over" sentences are inferences; the landed entry rejects them |
| (3) live page still says it | **yes** — 200, 81802 B, L31 verbatim, 1 occurrence; committed capture differs only on the Trace Id line |
| (4) Q2 on S048 alone | **sufficient for MSVR-scope claims**; the comparison claims must stay lane-row cross-references, and five generalizations must be refused |
| (5) counters | **a fabricated capture + unattributed universal rule passes all 7 counter commands**; only the prose reviewer clause rejects it |
| landed entry defects | 3 overreaches (FC-5, "closed list", route-2 gloss) + 1 missing sweep command; fixes messaged to ExecEntryF15 |

## §0 Live page (item 3)

```
$ curl -sSL -A "kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)" \
    -o live.html -w 'code=%{http_code} url=%{url_effective} ctype=%{content_type} size=%{size_download}\n' \
    https://www.microsoft.com/en-us/msrc/msvr
code=200 url=https://www.microsoft.com/en-us/msrc/msvr ctype=text/html; charset=utf-8 size=81802
$ sha256sum live.html
bf0d3de40b668d9c373cb077a956ca445b5539d55967f35a5f1dbe34907d1f56  live.html
$ python3 corpus/instruments/capture-source.py --id S048 --url https://www.microsoft.com/en-us/msrc/msvr \
    --kind html --out CritC2Kill-scratch/live.txt
S048 status=200 fetched_bytes=81802 snapshot_bytes=3755 sha256=4ad1f038401ad7b3d5f301b010ac096fa9150b9ec40643f699bd74ec7bef4944 utc=2026-10-25T23:31:23Z
capture_exit=0
```
Normalized live text, L31-L35 (kept at `CritC2Kill-scratch/live.txt`, 3755 B):
```
31: MSVR learns about vulnerabilities in third-party products in three ways:
32: Internal Microsoft engineers: … These vulnerabilities are reported to the MSVR team, which then works with the affected vendor to fix the issue.
33: External reports to the Microsoft Security Response Center (MSRC): … These issues are coordinated by MSVR.
34: Internal research projects: … Any issues are reported to the affected vendor under accepted Coordinated Vulnerability Disclosure practices.
35: This coordination takes place under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach. CVD clarifies how Microsoft responds as a vendor affected by vulnerabilities in its products and services, as a finder of new vulnerabilities in third-party products and services, and as a coordinator of vulnerabilities that affect multiple vendors.
```
Quote occurrence counts on the live capture (`grep -cF`): three-ways sentence 1; "These issues are
coordinated by MSVR." 1; "as a coordinator of vulnerabilities that affect multiple vendors" 1;
"as a finder of new vulnerabilities in third-party products and services" 1; the L33 typo clause
"either affects a third-party product of affects both the Microsoft product and external parties" 1.
`diff corpus/source-snapshots/round-31/S048.txt CritC2Kill-scratch/live.txt` → `2c2` only (the
per-request `Trace Id`). So the staged claim is **still on the live page at L31**, and the entry's
L31 anchor and quotes are current. Nothing else on the page supports the staged "obligation" gloss:
`grep -ci 'only' S048.txt` = 0, `grep -ciE '90[ -]day|deadline|embargo|timeline'` = 0.

## §1 Expansion credit (item 1)

Independent sweep (not the scout's, my own):
```
$ for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities'; do
    printf '%-26s %s\n' "$t" "$(grep -rli -- "$t" corpus/knowledge/*.md | tr '\n' ' ')"; done
MSVR                       corpus/knowledge/vendor-third-party-finding-coordination.md
MSRC                       corpus/knowledge/vendor-third-party-finding-coordination.md
research programme         corpus/knowledge/vendor-third-party-finding-coordination.md
coordinator of vulnerabilities corpus/knowledge/vendor-third-party-finding-coordination.md
```
Every hit is the new entry; the four terms are absent from the other 42 knowledge files, README.md,
SKILL.md and SOURCES.md. So the topic is not held. The ground that *is* held, line-exact:

| held ground | exact line | what it covers | what it does not |
|---|---|---|---|
| F06 role vocabulary | `knowledge/multiparty-vulnerability-coordination.md:25` — Coordinator = "Optional participant that can assist vendors and finders…"; `:30` — "one coordinator should be selected as lead" | a coordinator is an outside, optional participant | a vendor occupying the coordinator seat itself |
| F10 Cisco routing | `knowledge/vendor-disclosure-policy-commitments-crosswalk.md:26` (CERT/CC, CERT-FI, JP-CERT, NPSA at S040 L187-L190, paragraph L185-L193) and `:49` (`cisco-jpcert-partner`) | vendor **receives** a multi-vendor report and hands it **out** to an external centre | vendor finds in third-party products; vendor coordinates itself |
| F10 Cisco third-party trigger | `…crosswalk.md:52` (`cisco-high-profile-bullet`, S040 L309) | a third-party software vuln is a Cisco expedite trigger | who found it, or that Cisco found it |
| F10 Hitachi internal discovery | `knowledge/vendor-disclosure-policies-as-corpus-objects.md:126-134` (S039.txt:506: 他社製品に影響する → 届出窓口 → 協調した脆弱性対策), `:152` (調整機関 CERT/CC・JPCERT/CC) | internal discovery that spills to another vendor, handed to the national partnership | a deliberate research programme aimed at non-Microsoft products; self-coordination |
| F11 ISO division of labour | `knowledge/iso-29147-and-30111-division-of-labour.md:11` (29147 = 社外とのやりとり; subjects = product developers, online-service providers, intermediate vendors, S041.txt:1667-1668) | the outward-facing/in-house split of a vendor's own handling | any finder or coordinator role for other vendors' products |

Verdict: **expansion credit holds**, but it is carried by exactly three residuals and no more —
( r3 ) the internal-research route at L34 aimed at "products … not developed by Microsoft",
( self-coordinator ) "as a coordinator of vulnerabilities that affect multiple vendors" (L35), and
( programme-as-object ) a standing statement about *other* vendors' products where F10's thesis is a
statement about the vendor's *own* products. r2 (external multi-party report) alone restates
`crosswalk.md:26`/`:49`; r1 (engineers' ordinary work) restates the Hitachi shape at
`policies-as-corpus-objects.md:126-134` except that Hitachi's is a by-product of its own QA. The
landed entry does lead with all three (§"What this adds beyond F06 and F10", items 1-3), so the
clause is met; the risk it does not close is that the sweep command itself is not in the entry (fix 4
below). F11 is not named there — it holds nothing relevant, but the reviewer clause only names F06/F10.

## §2 Q4 attribution (item 2)

Staged text, `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md`:
- "the *finder* also has a coordinated-disclosure obligation when the finding is not solely about
  the finder" — a universal duty. The page says only that route-3 issues are reported "under
  accepted Coordinated Vulnerability Disclosure practices" (L34) and that coordination "takes place
  under Microsoft's … CVD approach" (L35): Microsoft describing its own practice.
- "the vendor that found the problem and **must hand it over**" — same defect.
- "it is a distinct mechanism rather than a paragraph in the bounty guidelines" — a comparative
  claim the page does not make (lane reading).
- `ground: F20` — not a lane row (`grep -cE '\| F20 ' corpus/README.md` → 0).

Landed entry verdict: **Q4 passes.** The `## Attribution` block states "Every statement below is
Microsoft's own description of its own programme"; Claim 1/2 headings carry "Microsoft's MSVR
states"; rejected over-generalization #4 explicitly refuses the staged obligation sentence. Residual
Q4 risk is nil on the landed bytes; the remaining defects are Q3/Q5 (below), not Q4.

## §3 Q2 — single source S048 (item 4)

S048 is tier A in the registry shape (`docs | A`) and opened in the admitting round, so Q2's
"≥1 tier-A or tier-B row for that claim's scope, opened in the admitting round" is met for every
claim whose scope is *this page*. The comparison claims ("What this adds") rest on S048 plus lane
rows S039/S040 that were opened in earlier rounds; that is the F10-crosswalk precedent and is
admissible only because the entry **cross-references the lane's own admitted rows** (`Claim 7`,
`cisco-jpcert-partner`) instead of re-deriving them — which the landed entry does. Single-source is
therefore enough, but the entry must refuse to generalize beyond the page. The landed entry refuses
five readings (#1 frequency, #2 bypass, #3 bounty, #4 obligation, #5 replaces-external-coordinator).
Three refusals are still missing and are the ones a single-source entry is most exposed to:
- **no industry rule** — the page does not say other vendors run such programmes, nor that a vendor
  *should*; #1 covers the frequency half, not the normative half.
- **no MSRC-policy claim** — the capture carries no MSRC CVD policy, bounty terms, contacts or
  timelines (`grep -ci '@microsoft'` = 0, FC-3); the entry must not let "MSRC" in the route-2 label
  become a claim about MSRC's own programme.
- **no "coordinated by MSVR" = "MSVR controls the disclosure date"** — the honest-limit paragraph
  says no timeline is stated; make that a named rejection so a reader cannot import an embargo.

## §4 The junk construction (item 5)

**Construction.** A scratch copy of the lane (`CritC2Kill-scratch/junk-root/kasegi-shokunin`,
`cp -a corpus`, deleted after this receipt) with four substitutions and nothing else:
1. `corpus/source-snapshots/round-31/S048.txt` replaced by three invented lines (not the page);
2. `manifest.json` rewritten with that file's sha256 and the invented quote
   "Vendors must coordinate all cross-vendor findings within thirty days of discovery.";
3. a junk entry `corpus/knowledge/junk-f15.md` — `source: S048 — https://www.microsoft.com/en-us/msrc/msvr …`,
   a Q10-conforming `recheck:` line, and a body stating a universal rule ("Every vendor … must
   coordinate disclosure within thirty days … no vendor may publish … without the owner's consent")
   attributed to no party, with the invented quote located at "S048, L2";
4. a Frontier row `| F15 | … | admitted | knowledge/junk-f15.md | S048 | … |` in README.md and a
   registry row `| S048 | Microsoft Security Vulnerability Research — https://www.microsoft.com/en-us/msrc/msvr | docs | A | … | mined | 2026-10-25 | 180d | corpus/knowledge/junk-f15.md |`
   inserted inside `## Registry` (before `## Paths`).

**All seven C2 counter commands pass on it** (commands verbatim from claims.json C2, `cd` into the
junk lane; census run with an explicit lane dir instead of `--root /home/vgpnk/Projects/shokunin kasegi`
because the junk root has no shokunin.conf — same validator, same E/W codes):
```
counter 1  awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
15
counter 2  grep -lE '^source: S048 ' corpus/knowledge/*.md | wc -l
1
counter 3  grep -cE '^\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md
1
counter 4  grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
48
counter 5  scripts/sources-census.sh validate --root <junk-root> <junk-lane>
kasegi-shokunin  W04  S028 duplicate url … (base warning)
kasegi-shokunin  W04  S029 duplicate url … (base warning)
kasegi-shokunin  ok   …/junk-root/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
counter 6  python3 corpus/instruments/frontier-recheck-count.py --root <junk-lane>
PASS     F15  knowledge/junk-f15.md   ids=S048   exit=0
entries=18 pass=18 exit=0
counter 7  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048
S048:sha256 OK
S048:Q1 OK occurrences=1
recheck_exit=0
```
So every mechanical conjunct of the C2 kill rule is met — frontier 15, exactly 1 entry citing S048,
exactly 1 S048 row, 48 rows, census exit 0 with no new E/W, `entries=18 pass=18`, `PASS F15`,
`source-recheck S048` exit 0 — by an entry whose capture is **not the page** and whose load-bearing
sentence is a **universal rule no party states**. Only the prose clause rejects it: Q4 (no Microsoft
attribution), Q3 (the "location L2" is a line in a fabricated capture, not in the page), Q2 (the
tier-A row's bytes do not carry the claim) and the restatement clause.

**Why each counter is blind** (with the code that makes it blind):
- counters 2-4 are shape counts (`grep -l`, `grep -c`); they never open the entry body;
- counter 5 (`sources-census.sh`) validates registry *shape* only — E01-E12/W01-W04 never read a
  snapshot, and no rule compares a row's URL to any capture;
- counter 6 (`frontier-recheck-count.py:137`) checks declared/cited/recheck id sets and then runs
  the line: `subprocess.run(["bash","-c",recheck], cwd=root, …)`. The line's own `cd` wins, and 43
  entries carry `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin`, so the executed command is not
  bound to the audited root either;
- counter 7 (`source-recheck.py:140-200`) binds only *local* bytes: `Path(path).stem == id`, a
  pinned sha256 of the local file, and quote occurrence. `capture-source.py` accepts `--url` and
  records it **nowhere** (grep of the tool shows no `url`/`fetched_utc` field), and the manifest
  record has no url field, so nothing ties `S048.txt` to `microsoft.com`.

**Minimal fix (kill-rule level, L1 owns claims.json — not mine to edit).** Add one conjunct that is
runnable in-round and cannot be satisfied by a local fabrication: *the reviewer re-fetches the
row's URL with the instrument UA in the admitting round and shows each load-bearing quote occurring
in the normalized live text, recording code/bytes/occurrence count* — plus require each manifest
record to carry `url` and `fetched_utc` so the census can bind row URL to capture URL. My §0 run is
that conjunct's template and it passes on the real bytes.

## §5 Defects on the landed entry and the minimal fixes (messaged to ExecEntryF15)

1. **FC-5 is falsified by its own command.** `grep -c 'affected vendor' corpus/source-snapshots/round-31/S048.txt`
   = **2** (L32 and L34) across **3** routes; `sed -n 33p … | grep -c 'affected vendor'` = **0**.
   Claim 1's "handed to, or worked with, the affected vendor in each case" and FC-5's "every stated
   route ends at the affected vendor" are therefore unsupported for route 2 ("These issues are
   coordinated by MSVR."). Fix: restrict to routes 1 and 3; state route 2 as coordinated by MSVR
   with no stated recipient; restate FC-5 as "two of three routes name the affected vendor (L32,
   L34); L33 names only MSVR". (Q3/Q5.)
2. **"as a closed list" / "the route list is closed at three".** The capture says "in three ways"
   (1 occurrence) and contains no "only" (0 occurrences); three labelled route lines prove
   enumeration, not closure. Fix: "states three intake routes"; a fourth route is *unsupported by
   this capture*, not excluded by the page. (Q4-adjacent over-generalization.)
3. **Route-2 gloss narrows the source.** "an external report filed against a Microsoft product that
   also touches a third party" drops L33's either/or ("either affects a third-party product of
   affects both …", sic) — the third-party-only alternative. Fix: paraphrase the either/or or quote
   it verbatim. (Q3.)
4. **The reviewer clause has no sweep command in the entry.** Add
   `for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities'; do grep -rli -- "$t" corpus/knowledge/*.md; done`
   to "What this adds beyond F06 and F10" (today it prints this entry only), and name F11 there.
   (Q5/R15 — an open claim needs its runnable check.)

Checked and sound on the landed bytes: Q1 header triple (`source:` with id+URL+`…S048.txt:28-35`,
`verified-at:`, one `recheck:` command that parses — `bash -n` exit 0 — and exits 0 with 8/8
assertions exactly-once); Q6 (no contact instruction, no credential/session URL); Q10 (`cd` prefix,
note after `#`); the staged `ground: F20`, S080 id and prose recheck are not carried.

## §6 Routed to the L1 (not my files, not ExecEntryF15's)

1. **Registry row placement.** A row appended after `## Registry changes` (the SOURCES.append.md
   habit) is census **E12** "row outside Registry section": I hit it in the junk build and fixed it
   by inserting before `## Paths`. ExecRegistryAppend must insert inside `## Registry` (SOURCES.md
   table ends at L53, `## Paths` at L55).
2. **No URL↔capture binding anywhere** (§4). Minimal: manifest `url` + `fetched_utc` per record and
   a census rule comparing it with the row URL.
3. **Harness root binding.** `frontier-recheck-count.py` runs the line with `cwd=root`, but the
   line's absolute `cd` overrides it (43 entries); a scratch-lane audit therefore measures the real
   lane for those entries. Relevant to C1's RA-cwd/RA-cdroot limbs as well as C2 counter 6.

## Reproduce

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
grep -c 'affected vendor' corpus/source-snapshots/round-31/S048.txt          # 2
sed -n 33p corpus/source-snapshots/round-31/S048.txt | grep -c 'affected vendor'  # 0
grep -ci 'only' corpus/source-snapshots/round-31/S048.txt                    # 0
grep -c 'in three ways' corpus/source-snapshots/round-31/S048.txt            # 1
for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities'; do grep -rli -- "$t" corpus/knowledge/*.md; done
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048
```
Live re-fetch: `curl -sSL -A "kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)" https://www.microsoft.com/en-us/msrc/msvr`
(expect 200, 81802 B; normalized L31 as quoted in §0). The junk construction is reproducible from
§4's four substitutions; its 3.2 MB scratch copy was deleted (R14), `CritC2Kill-scratch/live.txt`
(3755 B) is kept as the live-page evidence.

## §7 AFTER — final bytes (appended 2026-10-25T23:41:06Z)

The entry changed under my first read (M30-3 in-flight). Final bytes, all seven C2 counter
commands re-run on them:

```
f2a6f02b0eb35a4b287da3f9f6a506ab207bc7146fb32752d664d88f6732c49d  corpus/knowledge/vendor-third-party-finding-coordination.md
5a03c696312bd5fd8fe8307f75bd9723cac97fe3e44f0f3ba46a68607295f6f5  corpus/SOURCES.md
d9865b2e126c626559de9704d9e8d636b6f4ce7eba2a3a74e6f32d92b2146f98  corpus/README.md

c1 frontier admitted = 15
c2 entries citing S048 = 1
c3 S048 rows = 1
c4 registry rows = 48
census: kasegi W04 S028 … / kasegi W04 S029 … / kasegi ok corpus/SOURCES.md ; census_exit=0
harness: PASS F15 knowledge/vendor-third-party-finding-coordination.md ids=S048 exit=0 ;
         entries=18 pass=18 exit=0 ; harness_exit=0
source-recheck: S048:Q8 OK occurrences=1 … recheck_exit=0
```

So C2's mechanical predicate is met on the landed bytes. The four defects I routed to
ExecEntryF15 are **fixed in these bytes**, verified by grep on the new file: FC-5 now reads "two
of the three routes name the affected vendor; route 2 names no recipient" (L123); Claim 1's
heading no longer says "closed list" (L17) and FC-1 says "the page enumerates three labelled
routes" (L119); the route-2 gloss now carries the either/or and states "route 2 says only that
MSVR coordinates the issue" (L37-L40); the negative sweep command and the F11 paragraph are
present (L89-L100). The registry row landed inside `## Registry` (SOURCES.md:54, before
`## Paths`), so the E12 warning in §6.1 was preventive only.

Residual risk after the fixes is the one the counters cannot see: the capture→URL binding
(§4). On these bytes the live re-fetch (§0) independently confirms the quotes, so C2's
substantive claim stands; the kill rule would not have caught a fabricated capture without
that re-fetch.

## §8 Pin correction — entry rewritten again (appended 2026-10-25T23:43:45Z)

The entry moved once more after §7 (ExecEntryF15 applied the four fixes as a block). Current pin,
re-measured on these bytes:

```
1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb  corpus/knowledge/vendor-third-party-finding-coordination.md  (160 lines)
5a03c696312bd5fd8fe8307f75bd9723cac97fe3e44f0f3ba46a68607295f6f5  corpus/SOURCES.md
d9865b2e126c626559de9704d9e8d636b6f4ce7eba2a3a74e6f32d92b2146f98  corpus/README.md

c1=15  c2=1  c3=1  c4=48
census: kasegi W04 S029 … / kasegi ok corpus/SOURCES.md ; census_exit=0
harness: PASS F15 knowledge/vendor-third-party-finding-coordination.md ids=S048 exit=0 ; entries=18 pass=18 exit=0
source-recheck: S048:Q8 OK occurrences=1 ; recheck_exit=0
grep -n 'closed list|in each case|every stated route' → no output (all three stale phrases gone)
grep -c 'two of the three routes|enumerates three labelled routes|says only that MSVR coordinates|grep -rli --' → 4
```

§7's sha f2a6f02b was an intermediate write, not the final bytes; this §8 supersedes it as the
reviewed pin. Verdicts in §1-§5 are unchanged: expansion credit holds on the three residuals, Q4
passes, the live page still carries L31, and the counter blind spot of §4 is independent of the
entry's prose.
