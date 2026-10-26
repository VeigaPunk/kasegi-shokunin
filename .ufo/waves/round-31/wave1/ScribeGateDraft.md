# ScribeGateDraft — round-31 lesson blocks (DRAFT for L1 integration)

Seat `ScribeGateDraft` (leaf, no delegation, no swarm). Round kasegi-shokunin 31, wave 1.
One dependency poll of mine (waiting for `ExecCounter.md`, `ExecLedgerMerge.md`, `ScribeInstrReadme.md`,
`ScribeSkillGate.md`, `ScribeConsiderthese.md`, `ExecHarnessC2.md`) was auto-backgrounded by the shell tool as `bg_18063`;
it is disclosed rather than described as a foreground run, and no other job was spawned by this seat.
Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`;
claims-freeze `738a77999a00efbca129cfccb28a481037f6241f`; HEAD at measurement `8a8916c7043bd873d191b30dd1744b241b91f4d9`
(read-only `git rev-parse`). Answering model actually run on: `devin/deepseek-v4-1-flash` (runtime route; no model passed
by this seat). Tools installed or upgraded: **none** (no pacman transaction, no uv/npx; `grep`/`sha256sum`/`wc`/`sed`/
`python3` stdlib only). No git/jj mutation. No network fetch: the only URL below was captured by another seat under the
instrument UA and is quoted from the committed snapshot.

**Status: DRAFT, not landed.** This file is not the lesson. `corpus/lessons/**` is not this seat's path; the L1 integrates
these blocks into `corpus/lessons/round-31.md`. Every claim below carries the receipt path it came from; nothing is
asserted from memory, and no number is retyped — each was either copied from the named receipt or re-measured here with
the command shown.

Evidence base read by this seat (all under `.ufo/waves/round-31/`): `census-before.txt`, `c2-controls/before.txt`,
`assimilation/{collisions,guard-proof-collisions,reg-ids,staged-ids}`, and `wave1/` —
`ScoutMSVR.md`, `ScoutPackageThemes.md`, `ScoutF15Sweep.md`, `ScoutRALimbMap.md`, `ScoutDatawalk.md`,
`ExecCapManifest.md`, `ExecCensusDry.md`, `ExecEntryF15.md`, `ExecRegistryAppend.md`, `ExecErratumCheck.md`,
`ExecErratumCheck-before.txt`, `ExecErratumCheck-after.txt`, `ExecHarnessC2.md`, `ScribeErratum.md`, `ScribeLogR30.md`,
`ScribeQuality.md`, `ScribeReadmeF15.md`, `ScribeProvince.md`, `CritC2Kill.md`, `CritC1Kill.md`, `RevSourceBar.md`,
`RevClaimsFreeze.md`, `ConnOwnership.md`, `ConnSibling.md`, `SentScopeW1.md`, `ExecRALimbs.md`, `ExecSRLimbs.md`,
`ExecFRLimbs.md`, `MutRAExisting.md`, `MutSRExisting.md`, `MutFRExisting.md`, `ExecExpectedList.md`, `ExecScoreGap.md`,
`ExecCounter.md`, `ExecLedgerMerge.md`, `ScribeInstrReadme.md`, `ScribeSkillGate.md`, `ScribeConsiderthese.md`.
Sweep coverage: 40 `.md`/`.txt` files under `wave1/` at the final re-read.

---

## Gate

Shape follows the round-30 lesson Gate (`corpus/lessons/round-30.md` § Gate — assimilation set): an **Admitted** table,
then the package set as ADMIT/REFUSED with flip conditions.

### Admitted

| Item | Evidence | Gate decision |
|---|---|---|
| **F15** — `corpus/knowledge/vendor-third-party-finding-coordination.md` | Landed bytes measured here: `sha256 1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb`, 160 lines, 11501 B. Header L2 `source: S048 — https://www.microsoft.com/en-us/msrc/msvr — section "Microsoft Security Vulnerability Research (MSVR)", capture corpus/source-snapshots/round-31/S048.txt:28-35`; L3 `verified-at: 2026-10-25`; L4 one `cd`-prefixed `recheck:` command (`ExecEntryF15.md` §2). Q1-Q10 self-check with line pointers: `ExecEntryF15.md` §3; `bash -n` exit 0 and a foreign-cwd run exit 0: §4. All seven C2 counter commands run on these bytes twice independently — verbatim from `claims.json` on quiescence-proved bytes (`ExecHarnessC2.md` §0-§2) and by the critic (`CritC2Kill.md` §8): `c1=15 c2=1 c3=1 c4=48`, census exit 0, harness `PASS F15 … ids=S048` + `entries=18 pass=18 exit=0`, `source-recheck` exit 0. Expansion credit holds narrowly on three residuals (internal-research route L34, self-named multi-vendor coordinator L35, programme-as-object); Q4 attribution passes on the landed bytes (`CritC2Kill.md` §1-§2). Four Q3/Q5 defects the critic found in the first draft are fixed and verified by grep on the final bytes (`CritC2Kill.md` §5, §8). | **Admit.** |
| **S048** — Microsoft Security Vulnerability Research (MSVR) | URL `https://www.microsoft.com/en-us/msrc/msvr`; **access date 2026-10-25** (capture UTC `2026-10-25T23:29:53Z`, `ExecCapManifest.md` §1). Capture `corpus/source-snapshots/round-31/S048.txt` = 3755 B / 97 lines / `sha256 2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55`; manifest `sha256 b80f7f92fbab57c0edbb73d181414560fe0e5e7102405f210865acc84a2f87be` with 8 quote assertions, every one `occurrences=1` (`ExecCapManifest.md` §2-§3). Located quotes grounding the row's `teaches` cell ("…learns of third-party-product vulnerabilities through its own engineers (L32), external MSRC reports (L33) and internal research (L34), and names itself finder and multi-vendor coordinator under its CVD approach (L35)"): `MSVR learns about vulnerabilities in third-party products in three ways` — **capture L31, 10 words, `grep -cF` = 1**; and `as a coordinator of vulnerabilities that affect multiple vendors` — **capture L35, 9 words, `grep -cF` = 1**. Both are manifest assertions Q1 and Q7; both counts re-measured by this seat on the committed capture (`grep -cF -- "<quote>" corpus/source-snapshots/round-31/S048.txt` → `count=1` each; `grep -nF` → lines 31 and 35). Negative controls: wrong pin, foreign stem and a dropped quote word each exit 1 (`ExecCapManifest.md` §4). Census: no `E04`/`W04` for S048, i.e. the URL is unique among the 48 rows (`ExecCensusDry.md` §4; `ExecRegistryAppend.md` §5-§6). | **Tier A, mined.** Staged `S080` mapped **by document** (see mapping below). |

Capture quirks the lesson should keep, because they bound every future quote from this row (`ExecCapManifest.md` §1,
`ScoutMSVR.md` §QUIRKS, `CritC2Kill.md` §0):

- Snapshot line 2 is a per-request `Trace Id`, so the pin binds the **committed** bytes, not a refetch; the second capture
  differed on line 2 only. Never quote line 2.
- Line 30 carries U+2019; line 35 (the three-roles sentence) uses ASCII `'` — Q8's quote uses line 35.
- Line 33 contains a source typo ("third-party product of affects both", sic); it is inside no assertion, so nothing was
  silently corrected.
- Page-level evidence only: no timeline, contact, agreement or per-vendor process is stated (`@microsoft` 0, `http` 0,
  clock terms 0 — `ExecEntryF15.md` §10).

### Assimilation set — package `/home/vgpnk/Projects/shokuknow/merge/kasegi/` (read-only)

Package digests measured by the scout (`ScoutPackageThemes.md` §Evidence base), e.g. `SOURCES.append.md`
`4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb` — the same digest round 30 measured. Gate requirement
(≥1 admit, ≥1 reject) is met with **1 admit + 4 rejects** (`ScoutPackageThemes.md` §Verdict).

**ADMIT — `vendor-third-party-finding-coordination-2026-10-23.md`**, staged `sha256 48e9de4ec971f39e30d0ec4ba9f266ddeb5ac183ec172667b42787dc76c995dc`.
Adopted as the **F15 rewrite**, not as staged bytes: staged id `S080` → lane `S048` by document, staged `ground: F20` →
lane `F15`, prose `recheck:` → one executable command, paraphrase → located quotes from the round-31 capture. The staged
entry fails Q1/Q3/Q4/Q5/Q7/Q10 as written and the rewrite closes each (`ScoutPackageThemes.md` §1(c); `ExecEntryF15.md`
§3, §9).

**Id-collision evidence (why adoption must be by document, never by number).** The package assumed a 30-row registry
(`existing_rows 30`, `first_id S031`, `renumbered []`); the lane holds 47 rows, so every staged id from `S031` up names a
different document (`ScoutPackageThemes.md` §Evidence base). The collision scratch under
`.ufo/waves/round-31/assimilation/` is reproduced byte-for-byte by `ExecCensusDry.md` §3:

| artifact | producer command | digest / reading |
|---|---|---|
| `assimilation/reg-ids` | `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md \| sed -E 's/^ *\| *//'` | 47 lines, `ab66f54a…` — `cmp` clean vs the live registry |
| `assimilation/staged-ids` | same pattern on `merge/kasegi/SOURCES.append.md` | 94 lines, `550a0129…` — `cmp` clean |
| `assimilation/collisions` | `comm -12` of the two sorted sets | 17 lines, `S031…S047`, `ac78cd56…` — `cmp` clean |
| `assimilation/guard-proof-collisions` | first collision id | 5 bytes `S031\n`; both candidate producers (`head -1`, `grep -x 'S031'`) reproduce it byte-equal (`xxd` → `5330 3331 0a`) |

**Independently re-measured by this seat** (not copied): the same extractor over `git show b374febb:corpus/SOURCES.md`
gives `ab66f54a2135cea0359318caabb77575740093a32d7be7eb4bde47687be373c9` (byte-equal to `assimilation/reg-ids`), over
the read-only package `SOURCES.append.md` gives `550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f`
(byte-equal to `assimilation/staged-ids`), and `comm -12` of the two gives 17 ids `S031…S047` at
`ac78cd564ab864b574e0d54d4e4656d448439403839530bb3044d04175acd2d2` (byte-equal to `assimilation/collisions`). The
reproduction must run on the **base blob**, because the live registry now holds 48 rows after the append.

The guard id is a genuine collision, not a pattern artifact: live `S031` = CVE CNA Rules v4.2.6
(`https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf`), staged `S031` = HackerOne standard program policy set
(`https://hackerone.com/security/policy_versions`) — two different documents under one id (`ExecCensusDry.md` §3).
`S048` was free in the lane (`grep -cE '^ {0,3}\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md` → 0), the staged
`S048` is a **different document** (the `20260806-T-469` standard-plan record), and the MSVR URL appears on no lane row
(`grep -ic 'msrc\|msvr\|microsoft' corpus/SOURCES.md` → 0; census emits no `E04`/`W04` for it) (`ExecCensusDry.md` §4).

**Staged ids left un-mapped this round** (no lane id assigned, nothing copied): `S077`, `S078`, `S079`, `S081`, `S082`
(the Chinese crowd-testing set) and `S034`, `S035`, `S036` (`ScoutPackageThemes.md` §Ranking item 3). `S031` maps to the
already-registered lane `S043` by URL; `S033`/`S047`-style staged ids that name lane-held documents are not re-registered.

**REFUSED (each with its reason and flip condition).**

| staged entry | Gate decision | Reason (lane-side, checkable from staged bytes + registry) | Flip condition |
|---|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` (`120d8cd5…`) | **REFUSED** (standing from round 30) | Q1 (three `source:` lines carrying staged ids `S031`/`S034`/`S035`; `ground: F09` collides with lane F09; `recheck:` prose fails `bash -n`), Q2 (S034/S035 are not lane rows), Q3 (no located ≤25-word quote), Q5/Q4 ("every platform's scope list" generalizes three platforms into a universal), Q7/Q10 (non-executable recheck, no cwd prefix, no control). Its HackerOne half is **already held** by F13 (`program-severity-ladders-and-reward-scales.md`, S043) and the safe-harbour-vs-scope split by F03 (S006) (`ScoutPackageThemes.md` §2) | Register and capture the CNVD helpList (staged `S034` URL) and 360SRC rules (staged `S035` URL) as lane rows, reuse lane `S043` for HackerOne, add located quotes, one `cd … &&` recheck with a failing control, name a lane frontier topic, and re-check Q5/Q4 against the located text |
| `claim-packaging-and-report-quality.md` (`6ad64d78…`) | **REFUSED** (standing from round 30) | Q1 (ground not a lane F-id; recheck is `curl … && pdftotext …` prose, `bash -n` fails), Q2 (S034/S035/S036 unregistered), Q3 (three quote-marked Chinese phrases with no page/line), Q4 ("stricter than most Western platforms' published rules suggest" — a regional universal from three first-party documents), Q5, Q7/Q10 (`ScoutPackageThemes.md` §3). The topic itself is core PROVINCE; the entry as staged is not | Register and capture `S034`/`S035`/`S036` (BILISRC_V1.7.pdf), quote each downgrade/proof rule with PDF page or line, state each rule as that platform's own position, add one falsifiable rule plus one rejected over-generalization, and re-ground on a lane frontier item |
| `cn-crowdsourced-testing-roles-and-conduct.md` (`a5302aaf…`) | **REFUSED** (nearest to a flip) | Q1 (**no H1 title at all** — `grep -c '^# '` = 0; `ground: round-6 ledger item 2` is not a lane frontier; prose recheck), Q2 (S081/S082 not lane rows; S082 is a **drafting-stage** project record, so "GB/T 43741-2024 binds all four" rests on a drafting-stage scope sentence — a Q4 problem), Q3 partial (four located Chinese quotes but no revision/page and not checked exactly-once against a lane capture), Q7/Q10 (`ScoutPackageThemes.md` §4) | Add an H1, register and capture `S081`/`S082`, re-quote with page/line and exactly-once counts under the Q8 normalization, replace the drafting-stage scope sentence with a promulgated-text statement, add the `cd`-prefixed recheck and a failing control |
| `chinese-crowd-testing-national-standard-2026-10-23.md` (`6c15d941…`) | **REFUSED** (furthest from a flip) | Q1 (`ground: F24` not a lane F-id; prose recheck), Q2 (S077/S078/S079 unregistered), Q3 (**zero** quote-marked strings — `grep -c '"'` = 0; the 描述了…角色以及职责 sentence is paraphrased), Q5 (no falsifiable rule, no rejected over-generalization; its own limit says the requirements were never read) (`ScoutPackageThemes.md` §5). Also marginal to PROVINCE (catalogue metadata, not a program rule) | Register and capture `S077`/`S078`/`S079`, quote the roles-and-duties sentence with a location, drop the "curator should now read…" reframing or ground it, add the recheck and a rejected over-generalization |

No Q/R bar was relaxed and no package file was copied into the lane (`ScoutPackageThemes.md` §Ranking item 3).

### Gate caveat the lesson must carry — the C2 counters cannot see a fabricated capture

`CritC2Kill.md` §4 built a junk construction (invented capture + manifest + an entry stating an unattributed universal rule
+ a README F15 row + a registry S048 row) and **all seven C2 counter commands pass on it**: frontier 15, exactly 1 entry
citing S048, exactly 1 S048 row, 48 rows, census exit 0 with no new E/W, `entries=18 pass=18`, `PASS F15`, `source-recheck`
exit 0. Counters 2-4 are shape counts that never open the entry body; the census validates registry shape only; the harness
checks id sets and then runs the line, whose own absolute `cd` overrides `cwd=root` (`frontier-recheck-count.py:158` —
re-measured here; `CritC2Kill.md` §4 cites `:137`, which on the landed bytes is a `realpath` line, so the pointer is
corrected, not the finding); and
`source-recheck.py` binds only local bytes — the manifest record carries no `url` field and `capture-source.py` records the
fetched URL nowhere (corroborated on the bytes read here: the stem check is `source-recheck.py:123-125` and the sha check
`:171-182`; the file was mid-edit by ExecSRLimbs, so those line numbers are provisional and only the behavior is cited).
Only the prose clauses (Q2/Q3/Q4 + the restatement clause) reject the junk build.

What actually carried C2 this round was the critic's **live re-fetch** (`CritC2Kill.md` §0: code 200, 81802 B, L31 verbatim,
`diff` vs the committed capture = line 2 only). Two routed fixes belong in the lesson's open-defects list: each manifest
record should carry `url` and `fetched_utc`, and the census should compare a row's URL to its capture's URL
(`CritC2Kill.md` §4 "Minimal fix", §6.2). Neither is landed this round.

### Gate caveat 2 (carried from the sentinel) — the census dry-run fixture is not hermetic

`ExecCensusDry`'s `validate/` roots are **symlinks into the live corpus**, not copies: 52 symlinks, all contained inside the
lane (no escape to the fleet root or the package), but `validate/pre/corpus/{knowledge,instruments}` and the three control
roots link back to `corpus/{knowledge,instruments}` (`SentScopeW1.md` §F3). Consequence: (a) a tool that wrote under a
`validate/` root would write **through** into the live corpus; (b) the dry-run's negative controls test control `SOURCES.md`
against **live** knowledge bytes, so their independence is weaker than a copy-based fixture.

No write-through occurred (the lane's 43 pre-existing knowledge files are unchanged in `git status`, and
`corpus/instruments` shows no unexpected `M` — `SentScopeW1.md` §F3), and the census gate this draft cites as after-state
evidence is `ExecRegistryAppend.md` §5's run on the **real** registry, not the mirror — so the numbers stand. The lesson
should still record that the *pre-append* gate was weaker than it reads: `ExecCensusDry.md`'s own R14 conversion
(knowledge/instruments → symlinks) bought bloat control at the cost of hermeticity, and the two goals were not reconciled.

---

## Registry changes — old → new

Before column from the frozen control `.ufo/waves/round-31/c2-controls/before.txt` (`registry_rows=47`,
`frontier_admitted=14`, `entries_citing_S048=0`, `rows_S048=0`, `census_exit=0`) and `.ufo/waves/round-31/census-before.txt`
(exit 0, W04 S028/S029 only). After column from `ExecHarnessC2.md` §0-§1 (quiescence-proved) with `ExecRegistryAppend.md`
§5-§6 and `CritC2Kill.md` §8 as corroboration; re-read here on the landed bytes.

| Measure | Before (frozen) | After (landed) | Source |
|---|---|---|---|
| registry rows | 47 | **48** | `ExecRegistryAppend.md` §5 (`census --root … kasegi` → `rows 48`); `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 48 |
| S048 rows | 0 | **1** | `grep -cE '^\|[[:space:]]*S048[[:space:]]*\|'` → 1 |
| pre-existing rows/cells changed | — | **0** | `diff <base blob> corpus/SOURCES.md` → 3 insertions, **0 deletions**; `corpus/SOURCES.md` `sha256 5a03c696…` (`ExecRegistryAppend.md` §8) |
| tier histogram | A 44 / B 1 / C 2 | A **45** / B 1 / C 2 | `ExecRegistryAppend.md` §5 |
| status histogram | mined 35 / queued 9 / rejected 3 | mined **36** / queued 9 / rejected 3 | same |
| census findings | exit 0, W04 S028/S029 | exit 0, **same two W04**, no new E/W | `ExecRegistryAppend.md` §1 vs §5 (byte-identical finding lines) |
| malformed rows / duplicate ids / enum violations / missing used-by | 0 | 0 | `ExecRegistryAppend.md` §6 |
| frontier admitted rows | 14 | **15** | `ScribeReadmeF15.md` (append) + `CritC2Kill.md` §8 `c1=15` |
| harness | `entries=17 pass=17` | **`entries=18 pass=18 exit=0`**, incl. `PASS F15 … ids=S048` | `CritC2Kill.md` §8 |

Three lines were appended to `corpus/SOURCES.md`, not one (`ExecRegistryAppend.md` §8): the S048 row inside `## Registry`
(line 54, before `## Paths`), one `## Search log` bullet (now line 72), one `## Registry changes` R8 line (now line 94).
The row is `NF=13` under `awk -F'|'`, i.e. 11 cells with no `|` inside any cell (`ExecRegistryAppend.md` §2).

**The after column is measured on quiescent bytes, not on an in-flight snapshot.** `ExecHarnessC2.md` §0 digested all
eight C2 surfaces twice, 125 s apart with no intervening write, and a third time after its receipt was written; every
digest was identical, and the last write to any measured file preceded the first run by ~3.5 min. Its §1 table is the
authoritative after column above (`entry 1f16e371…`, `SOURCES 5a03c696…`, `README d9865b2e…`,
`knowledge-expected.txt d6f25227…`, `S048.txt 2001ad77…`, `frontier-recheck-count.py aa60b581…`,
`source-recheck.py fd2e01e8…`). `CritC2Kill.md` §8 reached the same seven numbers earlier and is cited as corroboration,
not as the basis.

**Cell-level old → new (staged `S080` → landed `S048`)** — full table with reasons in `ExecCensusDry.md` §5; the landed
values are the ones the registry holds:

| cell | staged `S080` (`SOURCES.append.md:56`) | landed `S048` |
|---|---|---|
| id | `S080` | `S048` — by document (URL equal); staged `S048` is a different document |
| source | `Microsoft Security Vulnerability Research — https://www.microsoft.com/en-us/msrc/msvr` | same URL, `(MSVR)` added from capture L28 |
| kind / tier / status | `docs` / `A` / `mined` | unchanged |
| scope | "programme for handling vulnerabilities found in third-party products…" | bounded to "Microsoft's own statement of its MSVR programme **and of nothing beyond it**" — the staged "handling" is dropped because the page states coordination, not a handling process |
| anchor | prose paragraph pointer | capture path + `L28` heading, `L29-L30` purpose, `L31` lead-in, `L32-L34` routes, `L35` three roles, plus "page shows no visible publication or revision date, opened 2026-10-25" |
| teaches | generic "A vendor's own research programme…" | attributed: "Microsoft's MSVR states…", each route and role cited by line (Q4) |
| **opened** | **`2026-10-23`** | **`2026-10-25`** — the admitting round; the staged date is **not** inherited |
| **recheck** | **`180d`** | **`180d`** (bare cadence, census `E09`-clean: `recheck=[180d]`) |
| used-by | `…vendor-third-party-finding-coordination-2026-10-23.md` | `corpus/knowledge/vendor-third-party-finding-coordination.md` (date suffix dropped, matching the C2 predicate path) |

**R6 disclosure (anchor drift created by this append).** The registry row must sit inside `## Registry` (census `E12` fires
on a row-shaped source outside it), so the append inserts a line at 54 and shifts everything below. Measured here on the
base blob vs the landed file: the `Change cell old → new: the S043 anchor…` line was at `SOURCES.md:85` at base and is at
`:87` now. Two lessons cite `SOURCES.md:83` for that line (`corpus/lessons/round-29.md:214`,
`corpus/lessons/round-29-verifier-spotcheck.md:74`) — already off by 2 before this round (round-30's S046/S047 append),
now off by 4. Every row-level citation (`:22`, `:46`, `:47`, `:48`) keeps its number. The correction is **routed**, not
written: `corpus/lessons/**` is not this wave's write scope (`ExecRegistryAppend.md` §9, re-measured here).

---

## Staged-to-lane normalization notes

These are the transformations the lesson should record as R8 "old → new" notes, distinct from the registry cell table
above because they concern the **staged entry**, not the staged row.

1. **Recheck normalization (the item's `180d — curl …` → `180d`).** Two different objects must not be conflated, and this
   draft states both precisely:
   - the staged **row** cell at `SOURCES.append.md:56` is already the bare cadence `180d` (measured this seat:
     `sed -n '56p'` on the read-only package);
   - the staged **entry** line 4 is the prose hybrid `recheck: 180d — `curl -sSL https://www.microsoft.com/en-us/msrc/msvr`
     and confirm the three routes are still listed (ran 2026-10-23)`. That is the cell that fails Q7/Q10 and `bash -n`
     (`ScoutPackageThemes.md` §Evidence base: "all five fail … `180d — \`curl …\``, no `cd` prefix, no captured-source
     comparison").
   - **Lane normalization:** the cadence survives as `180d`; the `curl` prose is **stripped** and is not carried into any
     lane file. The runnable replacement is the entry's own recheck line
     (`cd <lane> && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json
     --source S048`), which is `bash -n` exit 0 and exit 0 from a foreign cwd (`ExecEntryF15.md` §4). Nothing of the
     stripped prose is quoted anywhere in the lane; it is recorded here only as the discarded staged text.
2. **`ground: F20` → `ground: F15`.** The package's F-space collides in label with the lane's (`ScoutPackageThemes.md`
   §Evidence base); the lane has no F20 (`grep -cE '\| F20 ' corpus/README.md` → 0, `CritC2Kill.md` §2).
3. **`S080` → `S048` by document** (never by number), with staged `S048` naming a different document — see the collision
   table above.
4. **Used-by path: date suffix dropped** (`…-2026-10-23.md` → `…coordination.md`) so the row's `used-by` resolves to the
   entry the C2 predicate counts (`ScoutPackageThemes.md` §1(d)).
5. **Paraphrase → located quote.** The staged entry had no located quote at all (Q3); the rewrite quotes 13 programme
   strings (the inventory has 14 rows; the extra one is a navigation-chrome line, disclosed as chrome), each ≤25 words,
   each exactly-once in the pinned capture, each carrying its capture line (`ExecEntryF15.md` §6).
6. **Two staged sentences were refused rather than normalized** (Q4): "the *finder* also has a coordinated-disclosure
   obligation" and "must hand it over" are inferences the page does not carry; the landed entry refuses the obligation
   reading explicitly (`CritC2Kill.md` §2, `ExecEntryF15.md` §9 item 4).
7. **Anchor prose → capture lines** with the "no visible publication or revision date" note, which is what stops a reader
   importing a date the page does not show.

---

## Mistakes (M31-*)

### M31-1 — stale premise: a filed failure paragraph outlived its own fix, and the round-30 LOG entry was never written

- **Class:** stale-premise / landing (two parts of one defect).
- **What was stale.** (a) `SCORECARD.md:813-819` files "**recheck-audit open item (outside the frozen claims).**" reading
  `expect=present expected=43 missing=0 unexpected=0 exit=1`; the round-30 close-out erratum changed the ledger's recheck
  to `density.py` over its own entry, and the audit then measured `strict pass=43/43 … exit=0`
  (`corpus/lessons/round-30.md` § Close-out erratum; `corpus/lessons/round-30-verifier-spotcheck.md` §1 defect 3, §5
  item 4). (b) `LOG.md` carried no round-30 entry at all (round-30-verifier-spotcheck §1 defect 2; the round-30 seat's
  editor rejected a stale hash, disclosed in its lesson § Close-out erratum).
- **Evidence pointers.** Red-before: `.ufo/waves/round-31/wave1/ExecErratumCheck-before.txt` — CHECK A
  `stale_paragraphs=1 errata_naming_item=0 erratum_cites_corrected_audit=0 / erratum_closure=open`, **exit 1**; CHECK B
  `round30_log_headings=0 / log_closure=open`, **exit 1**, both labelled PRE-STATE against pre-edit digests
  (`SCORECARD cac64dbd…`, `LOG 0a1865e9…`).
- **Captured by:** **none** — no seat captured it in round 30; it was routed to round 31 by the non-author verifier. The
  capture rule it produced is **R16** (`corpus/QUALITY.md` § Round-31 additions): a result paragraph stating an open
  failure or exit code carries its `bash -n`-parseable closure check, and closure is an appended erratum naming that
  paragraph and citing the corrected output, with the filed text byte-identical.
- **Fix, and the fix shown able to fail.**
  - `ScribeErratum.md`: appended `### Round-31 erratum to the round-30 section` at `SCORECARD.md:837`; naming line at
    `:839` begins "r31 erratum: the paragraph `recheck-audit open item (outside the frozen claims)` filed at
    `SCORECARD.md:813-819` …" and the measured-output block carries `strict pass=43/43 … exit=0`. Append-only proof:
    25 insertions, **0 deletions**, filed bytes untouched (`SCORECARD.md` `cac64dbd…` → `5fa41aef…`, 835 → 860 lines).
  - `ScribeLogR30.md`: appended `## Round 30 — 2026-10-25 — …` at `LOG.md:1469`, naming itself a late append made in
    round 31 and the superseded absence at HEAD `8a8916c`; 115 insertions, **0 deletions**
    (`LOG.md 0a1865e9…` → `864deb7d…`, 1467 → 1582 lines).
  - Green-after with **mutant controls** (`ExecErratumCheck-after.txt`): CHECK A `stale_paragraphs=2 erratum_anchor=837
    names_item_and_cites_corrected_audit=1 / erratum_closure=closed`, exit 0 — and deleting the erratum block from a
    scratch copy returns `stale_paragraphs=1 erratum_anchor=none`, exit 1; CHECK B `round30_h2_headings=1 …
    log_closure=closed`, exit 0 — and deleting the round-30 entry from a scratch copy (and re-reading the committed
    pre-entry blob) returns 0/0, exit 1. So the green is carried by the new bytes only.
  - An independent reproduction of CHECK A, red→green→mutant, is in `ScribeQuality.md` §2 (`red_exit=1`,
    `green_exit=0`, `mutant_exit=1`).
- **The wave's own warning about its own number.** The `43/43` quoted by the erratum was measured at
  `2026-10-25T23:33:27Z` on quiescent pre-C1 bytes (`recheck-audit.py 3fc0d751…`). While the C1 seats were editing, a run
  printed `strict pass=44/44 … unexpected=1 exit=1` (unexpected = the new F15 entry, expected list still 43). Both
  `ScribeErratum.md` and `ExecErratumCheck.md` §4.2 label that **IN-FLIGHT / NON-COMPARATIVE**; it is not a regression of
  the erratum, and the canonical C1 after belongs to the C1 seats on quiescent post-land bytes.

### M31-2 — in-flight digest churn: peers gated on an entry that was still being rewritten

- **Class:** sequence / in-flight (the M30-3 class recurring).
- **What happened.** `corpus/knowledge/vendor-third-party-finding-coordination.md` was read by two downstream seats at
  `sha256 bf40fd9e…` (146 lines, 10359 B) and later rewritten twice: `f2a6f02b…` (an intermediate write) then
  `1f16e371…` (160 lines, 11501 B, the final). `ScribeReadmeF15.md` §1 and `ExecRegistryAppend.md` §0 both record the
  `10359 B` state as their gate evidence; `CritC2Kill.md` §7 records `f2a6f02b…` and §8 supersedes it with `1f16e371…`.
- **Why it did no harm this time.** The README append cites no entry line number (verified: the round-31 README section
  names the path only), and the registry row's `used-by` is a path, not a digest. The critic re-ran all seven C2 counters
  on the final bytes, so the C2 numbers are bound to `1f16e371…`, not to the in-flight state.
- **Rule it reinforces (R13/R14 already say it; the wave shows it again):** a digest is a measurement with a timestamp and
  a quiescence statement, not an identifier — `bf40fd9e…`/`f2a6f02b…` must never be cited as the landed entry.
- **One more transient, recorded and not used.** In `ExecHarnessC2.md` §4's 23:31:56Z block (peers still writing) the
  admitted-row `awk` printed `0` once; the identical command printed `15` (and `14` before the append) on every later
  invocation, grouped and plain. The seat treats the `0` as an in-flight read, claims no defect against the counter, and
  does not use it as a measurement. Anyone re-reading that block should do the same.

### M31-3 — the registry append shifted two cited `SOURCES.md` anchors (R6, partial)

- **Class:** anchor drift / R6 partial.
- **What happened.** Inserting the S048 row at `SOURCES.md:54` moved every line below it. The two lessons that cite
  `SOURCES.md:83` for the S043 change cell (`corpus/lessons/round-29.md:214`,
  `corpus/lessons/round-29-verifier-spotcheck.md:74`) were already off by +2 (round-30's append); the target line is now at
  `:87`, i.e. off by +4.
- **Evidence.** `ExecRegistryAppend.md` §9 (table of cited anchors); re-measured here: base blob `SOURCES.md:85` = the
  `Change cell old → new: the S043 anchor…` line, landed `:87` = the same line, landed `:83` = the `S040 recheck cell
  restored old → new` line.
- **Status: open, routed.** The correction belongs to `corpus/lessons/**` (not this wave's scope), and the row could not
  have been appended elsewhere without tripping census `E12` (`CritC2Kill.md` §6.1). Every row-level citation kept its
  number.

### M31-4 — a third stale premise in the same family survived the wave

- **Class:** stale-premise (same family as M31-1, different file).
- **What is stale.** `corpus/QUALITY.md:77` (record R13, specimen sentence) states `recheck-audit.py --selftest` →
  `selftest cases=4 failures=0 exit=0` and calls a parse-only fixture "the selftest's remaining gap". Measured on the
  pre-C1 instrument bytes, the selftest prints **18** `selftest …` case lines, all ok, and **no** `cases=N failures=M`
  summary line at all (`ExecErratumCheck.md` §4.1: `grep -nE 'cases=|failures='` over the output → no match; the peer's
  "six cases" was corrected to 18 there).
- **Evidence pointers.** `ExecErratumCheck.md` §4.1; `ScribeErratum.md` §3 finding 3 (routed to ScribeQuality);
  `grep -c 'selftest cases=4' corpus/QUALITY.md` → **1** (still present after ScribeQuality's append — its R16/R17 rows
  cite `:77` only as an anchor that kept its number, `ScribeQuality.md` §1).
- **Status: open.** Suggested same-shape closure check (R16 form): `q=$(grep -c 'cases=4' corpus/QUALITY.md)` with closure
  requiring an r31 erratum naming `cases=4`; the `cases=4` figure should not be quoted as current behaviour until then.
  **Caveat:** `recheck-audit.py` was mid-edit by ExecRALimbs when that count was taken, so the *replacement* number must be
  re-measured on the landed instrument before it is written into QUALITY.md.
- **Same family, already corrected:** the round-30 Capabilities parenthetical "(last capability entry round 25)" is false —
  round 26 added `source-capture-pdf` (`SCORECARD.md:580-584`); corrected in the appended erratum only, filed text
  untouched (`ScribeErratum.md` §4).

### M31-5 — survivor discipline: three survivor events, two closed by strengthening, one disclosed and not landed

- **Class:** limb-oracle gap (the class R17 now governs).
- **RA-completeness — a real survivor, closed by strengthening.** `MutRAExisting.md` measured 9 limbs: 8 killed,
  **1 survivor** (RA-completeness; the mutant compiled, `find` occurred once, exit 0 and stdout byte-identical —
  `MutRAExisting.md` §Tally, §Survivor analysis). `ExecRALimbs.md` §5 strengthened `recheck-audit.py`'s selftest so the
  mutant dies; the landed fragment prints `limbs=9 killed=9 survivors=0`, and the merged counter prints
  `limbs=13 killed=13 survivors=0` (`ExecRALimbs.md` §4-§5; `CritC1Kill.md` §3).
- **SR M5 — a survivor, closed by the owner.** `MutSRExisting.md` §M5 measured "accept a normalized-quote mismatch" as a
  **SURVIVOR** (5 probes, 4 killed); after `ExecSRLimbs` added a `quote-absent` case the same probe reads
  `killed (was survivor)`, post-fix **0 of 5** survivors (`MutSRExisting.md` §Post-fix re-run).
- **FR mut3/mut4 — survivors disclosed and deliberately NOT landed.** `MutFRExisting.md` §48-§53, §117-§120 report two
  harness mutants no current oracle kills (dropping the `no-source-selection` guard; dropping the
  `not-a-recheck-invocation` branch) — both behaviour-bearing, not equivalent. `ExecFRLimbs.md` §Risks 2 states they are
  outside the frozen 13-limb set and the two isolating fixtures are described but **not landed**. The two FR ledger rows
  themselves are killed (`limbs=2 killed=2 survivors=0`, instrument bytes unchanged at `aa60b581…`).
- **Rule.** A survivor is never relabelled killed; a limb with no failing oracle is either strengthened (as RA and SR were)
  or disclosed as an open oracle gap (as FR mut3/mut4 are). R17 records this as the admission bar.

### M31-6 — the round's evidence tree would commit ~100 scratch/fixture files, and one round-30 receipt was edited during round 31

- **Class:** scope / commit hygiene (not a corpus defect; a landing defect waiting for the L1's commit).
- **What the sentinel measured** (`SentScopeW1.md` §F2): of 180 paths touched in the lane, **54 are owned paths** and
  **126 are unowned** — 22 inherited round-29/30 leftovers (routed defect 1, still open), 5 L1/harness files, 8
  `CritC1Kill-scratch/` files, 1 `CritC2Kill-scratch/live.txt`, 61 `ExecCensusDry/` paths (incl. 44 per-file symlinks and
  4 control roots), 17 `ExecCounter-fixtures/` files, the two `ExecErratumCheck-*.txt` receipts, 7
  `ExecSRLimbs-scratch/` files, 3 `ScoutMSVR-scratch/` files.
- **Why it matters.** A lane-wide `git add -A` would land ~100 scratch/fixture files in the round-31 commit — including
  three copies of the MSVR capture, the raw 81,802-byte MSVR HTML, 13 counter fixture ledgers, and 52 symlinks pointing
  into `corpus/` — plus the per-request `Trace Id` line that makes the capture digest non-reproducible. The counters only
  scan `corpus/`, so the **claims** would still hold while the commit carried evidence the round never argued for.
- **Second, distinct item.** ` M .ufo/waves/round-30/wave1/ExecRegistryAppend.md` is a **tracked round-30 receipt** edited
  during round 31 (by the round-30 seat of that name, `SentScopeW1.md` §F2 row 2). A round-31 commit would carry a
  round-30 file; the L1 must decide explicitly, and the append must be dropped by its round-30 owner if not wanted.
- **Smallest remediation** (`SentScopeW1.md` §F2): commit by explicit path (the 54 owned paths the ownership table already
  names), or have each seat delete its `*-scratch/`/`*-fixtures/` directory after its receipt cites it (`CritC2Kill` already
  did the latter; `ExecCapManifest` and `ScribeErratum` deleted theirs).
- **Counterweight, so the lesson does not overstate the finding** (`SentScopeW1.md` header and §1-§2): **no credential
  material, no session/private URL, no live bounty-target contact and no out-of-lane write by a round-31 seat**; all 54
  owned paths resolve to a named seat with no orphan, and the forbidden zones (`.ufo/state/`, `.ufo/watchdog.log`,
  `MANIFEST.json`, `templates/`, `scripts/`) are clean inside the lane. F1 is a *method* finding: the fleet-root
  `git status` is structurally blind to every lane, so bound-1 compliance must be read from the lane's own status plus the
  two complement commands the sentinel names — not from the fleet root alone.
- **Status: open at the time of this draft** — the commit has not been made; the ruling is the L1's.

---

## Wave sweep — `BLOCKED` / `DEFECT` / `survivor` across the wave-1 receipts

Sweep command (re-run at the end of this seat's item, on every `.md`/`.txt` under
`.ufo/waves/round-31/wave1/`): `grep -n -i -E 'BLOCKED|DEFECT|survivor' *.md *.txt`. Hits that are **quoted contract text
or expected output** (e.g. the literal `verdict=killed|survivor`, `limbs=13 killed=13 survivors=0`, the C1 contract block in
`ConnClaims.md`) are excluded as non-findings; every remaining hit is listed here with its pointer.

| # | File (receipt) | Word | What it actually records | Pointer |
|---|---|---|---|---|
| 1 | `CritC2Kill.md` | defect | Four defects on the first landed F15 entry (FC-5 falsified by its own command; "closed list" overreach; route-2 gloss narrowed the source; no sweep command) — **fixed and verified on the final bytes** | §5, §8 |
| 2 | `ExecEntryF15.md` | defect | Three defects the entry's own author caught in his draft (nav line L12→L15; `cert` count 0→1; "each route ends at the vendor") — **fixed before final** | §8 |
| 3 | `ExecCensusDry.md` | defect | A withdrawn defect claim: a row-digest mismatch was first called a defect, then withdrawn with its cause recorded, "so the lane inherits no false defect claim" | §(handoff), :254, :263 |
| 4 | `ExecFRLimbs.md` | defect | `live_exit 1` is **correct, not a defect** (both FR limbs protect a fail-closed exit 1) — an explicit non-finding, listed so an attack seat does not misread it | §Risks 3 |
| 5 | `ExecFRLimbs.md` | survivor (open) | Two harness guards with no killing oracle (`no-source-selection`, `not-a-recheck-invocation`), outside the frozen 13-limb set, fixtures described but not landed — see M31-5 | §Risks 2 |
| 6 | `MutFRExisting.md` | SURVIVOR (open) | mut3-accept-source-less and mut4-accept-true-selftest survive on LIVE/FROZEN/A1/A2; proofs that they are behaviour-bearing, not equivalent | :52-:53, §Survivor proofs, :117-:120 |
| 7 | `MutRAExisting.md` | survivor (closed) | RA-completeness survivor (8/9 killed) → closed by `ExecRALimbs`' strengthening | :23-:29, `ExecRALimbs.md` §5 |
| 8 | `MutSRExisting.md` | SURVIVOR (closed) | M5 accept-normalized-quote-mismatch → closed by the owner's new `quote-absent` case; post-fix 0 of 5 | :38, §Post-fix re-run |
| 9 | `ScribeErratum.md` | defect | Three findings, one of them **open**: `corpus/QUALITY.md:77` `cases=4` stale premise (routed to ScribeQuality, not fixed) — see M31-4 | §Findings 1-4 |
| 10 | `ScribeLogR30.md` | defect | Records the round-30 routed defects it closes (2) and the ones it does **not** close (1, 3, 4, 5) | :218-:220 |
| 11 | `ExecEntryF15.md`, `ScribeReadmeF15.md`, `ScribeProvince.md` | BLOCKED | Explicit **negative** statements: "`BLOCKED:` is not used" / "No blocker" — no receipt in this wave records a real `BLOCKED:` | `ExecEntryF15.md` §10, `ScribeReadmeF15.md` :191, `ScribeProvince.md` :38 |
| 12 | `ExecExpectedList.md` | BLOCKED | `BLOCKED: none.` — same negative form | :156 |
| 13 | `RevClaimsFreeze.md`, `ConnClaims.md`, `ScoutDatawalk.md`, `ScoutRALimbMap.md`, `CritC1Kill.md`, `ScribeQuality.md` | survivor | Contract/verdict vocabulary and the ledger summary lines (`verdict=…|survivor`, `limbs=13 killed=13 survivors=0`, `controls=3 rejected=3`) — quoted, not findings | see the sweep output in this seat's run |
| 14 | `ExecLedgerMerge.md`, `ConnClaims.md` | survivor (by design) | The merged ledger's `CTL-equivalent` control is an honest **survivor** (`expect=survivor`, `ok=y`) — a comment patch whose run is byte-identical to the live run. The naming wrinkle `ConnClaims.md` §3 raises is real and belongs to C1's own lesson block: `controls=3 rejected=3` counts a control whose expected verdict is `survivor`, so "rejected" must be read as "verdict equals expect", not as "killed" | `ExecLedgerMerge.md` §7-§8, :195-:203; `ConnClaims.md` :41, :218 |
| 15 | `SentScopeW1.md` | defect (open) | F2: 126 of 180 touched paths are unowned — ~100 scratch/fixture files and 52 symlinks would land under a lane-wide `git add -A`, and one **tracked round-30 receipt** was edited during round 31 — see M31-6 | §F2, :195-:206 |
| 16 | `SentScopeW1.md` | defect (open, weakens a gate) | F3: the census dry-run roots are **symlinks into the live corpus** — a trust-boundary weakness with no write-through observed; the after-state census ran on the real registry, so the numbers stand — see the Gate caveat above | §F3, :215-:241 |
| 17 | `SentScopeW1.md` | defect (non-finding) | F4: the committed capture carries one per-request `Trace Id` — a provenance fact explaining the non-reproducible digest, not a leak or a credential | §F4 |
| 18 | `ScribeInstrReadme.md`, `ScribeSkillGate.md`, `ExecCounter.md` | survivor (by design) | The three C1-side scribe/executor receipts restate the merged `limbs=13 killed=13 survivors=0` / `controls=3 rejected=3` and the honest `CTL-equivalent` survivor; `ExecCounter.md:171` is a **fixture** proving a control declared with the wrong `expect` is rejected | `ScribeInstrReadme.md` :34-:38, `ScribeSkillGate.md` :294, `ExecCounter.md` :171 |

**Net reading of the sweep:** no seat reported a hard `BLOCKED:`; five defect classes were hit, **three closed in this
wave** (F15 entry overreaches, M31-1 parts 1-2, RA/SR survivors) and **four open and routed** — the QUALITY `:77` stale
`cases=4` premise (M31-4), the two FR guard mutants (M31-5), the anchor drift (M31-3), and the commit-hygiene/scratch
exposure plus the non-hermetic dry-run fixture (M31-6, Gate caveat) — alongside the two C2 counter-binding fixes
(`url`/`fetched_utc` + census URL↔capture rule) from the Gate caveat and the inherited round-29/30 leftovers (routed
defect 1) that round 31 again did not close.

---

## Provenance, limits, and what this seat did not do

- **Owned path:** this file only. Not written: `corpus/lessons/**` (the lesson itself), `SHONEN.md`, the report,
  `claims.json`, any corpus file, any instrument, `corpus/instruments/README.md`, `SKILL.md`, `PROVINCE.md`, `LOG.md`,
  `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, the proposals ledger.
- **No verification runs of my own on the C1 instruments.** `recheck-audit.py`, `source-recheck.py` and
  `frontier-recheck-count.py` were mid-edit by the C1 executor seats during this seat's window; every C1 number above is
  quoted from a C1 receipt or a critic receipt with its own quiescence statement, never measured by me and never compared
  across a state change (bound 6 / M30-3). One incidental `recheck-audit.py --selftest` invocation during my reading
  printed an in-flight failure line; it is **not** cited anywhere in this file, and the landed C1 after belongs to
  `ExecCounter`/`ExecLedgerMerge`.
- **No fetch, no live target contact.** The MSVR page was captured by `ExecCapManifest` under the instrument UA; the
  critic's re-fetch (`CritC2Kill.md` §0) is the only live check in this wave and is cited as the critic's observation.
- **No git/jj mutation.** Read-only `git rev-parse`, `git show`, `git diff` only.
- **Tooling:** nothing installed or upgraded; no pacman transaction (host-wide pause); no `uv`/`npx`/binary download.
- **Receipts this draft rests on** (paths relative to the lane root): `.ufo/waves/round-31/{claims.json,census-before.txt,
  c2-controls/before.txt,assimilation/*}`, `.ufo/waves/round-31/wave1/{ScoutMSVR,ScoutPackageThemes,ScoutF15Sweep,
  ExecCapManifest,ExecCensusDry,ExecEntryF15,ExecRegistryAppend,ExecErratumCheck,ExecErratumCheck-before,
  ExecErratumCheck-after,ScribeErratum,ScribeLogR30,ScribeQuality,ScribeReadmeF15,ScribeProvince,CritC2Kill,CritC1Kill,
  RevSourceBar,RevClaimsFreeze,ConnOwnership,ConnSibling,SentScopeW1,ExecRALimbs,ExecSRLimbs,ExecFRLimbs,MutRAExisting,
  MutSRExisting,MutFRExisting,ExecExpectedList,ExecScoreGap}.md`, and the landed bytes
  `corpus/knowledge/vendor-third-party-finding-coordination.md` (`1f16e371…`), `corpus/SOURCES.md` (`5a03c696…`),
  `corpus/README.md` (`d9865b2e…`), `corpus/QUALITY.md` (`96b71caa…`), `SCORECARD.md` (`5fa41aef…`), `LOG.md`
  (`864deb7d…`), `corpus/source-snapshots/round-31/{S048.txt,manifest.json}` (`2001ad77…` / `b80f7f92…`).
