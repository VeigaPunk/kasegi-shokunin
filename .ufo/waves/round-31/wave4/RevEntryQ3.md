# RevEntryQ3 — final independent Q1–Q10 review of `corpus/knowledge/vendor-third-party-finding-coordination.md`

- Seat: `RevEntryQ3` (round 31, wave 4, final residual re-review). Leaf; no subagents, no background jobs, no delegation.
- Answering model actually run (bound 10, from the workstation config route table; no model passed by this seat): `opencode-go/deepseek-v4.1-flash`.
- Review target (not written and not reviewed in any earlier revision by this seat):
  `corpus/knowledge/vendor-third-party-finding-coordination.md`, **172 lines, 12900 B**,
  sha256 `a488df492e2a72a929e0502ac9fabc80d00214a8fd6d83335ac624deb9c8d56f`,
  mtime 2026-10-25 22:32:38 -0300.
- Lane tip read: `43c364d06ccf5a3d1029c0f7816c8e50b509365b` ("round-31: final residual call dispatch (2 seats)").
  The bytes under review were landed by `0de072c` (wave-3 residual integration, "F15 entry Q3 repair"); the file's commits are
  `0de072c`, `fd29aac`, `eecad59` only.
- Quiescence (M30-3): entry sha256 re-measured at the **end** of this review — identical to the start value
  (`a488df49…d56f`); manifest `9693fa3c8a164c97aab3b58f694aaa2644e716a32b31194d55ee744e4cbc8410`; capture
  `2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55`. Every reading below is on quiescent bytes.
- Writes: this receipt only. Scratch `/tmp/revq3_recheck.sh` (outside the lane). No instrument, entry, registry, README,
  SKILL, PROVINCE, git/jj state touched. No pacman/uv/npx install run (nothing needed); no network fetch.
- Independence: the bytes and the instruments produced every finding below. Both prior refusals
  (`wave2/RevEntryQ.md`, `wave3/RevEntryQ2.md`) and the repair diffs were read to enumerate findings, then each was
  re-tested against the current bytes.

## 1. Commands run and their output

### 1.1 The entry's own `recheck:` line — extraction, `bash -n`, lane root, `/`

```
$ E=corpus/knowledge/vendor-third-party-finding-coordination.md
$ grep -n '^recheck: ' "$E"
4:recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048   # 11 assertions (Q1-Q11), each exactly-once in the pinned capture; the three route labels at L26-28 and the strings in the falsifiable checks are hand-measured, not manifest-bound; a captured-source comparison, not a fresh network verification
$ CMD=$(grep -m1 '^recheck: ' "$E" | sed 's/^recheck: //; s/[[:space:]]*#.*$//')
$ printf 'CMD=[%s]\n' "$CMD"
CMD=[cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048]
$ printf '%s\n' "$CMD" > /tmp/revq3_recheck.sh; bash -n /tmp/revq3_recheck.sh; echo "bash_n=$?"
bash_n=0
$ ( bash /tmp/revq3_recheck.sh; echo "lane_exit=$?" )        # cwd = lane root
S048:sha256 OK
S048:Q1 OK occurrences=1
S048:Q10 OK occurrences=1
S048:Q11 OK occurrences=1
S048:Q2 OK occurrences=1
S048:Q3 OK occurrences=1
S048:Q4 OK occurrences=1
S048:Q5 OK occurrences=1
S048:Q6 OK occurrences=1
S048:Q7 OK occurrences=1
S048:Q8 OK occurrences=1
S048:Q9 OK occurrences=1
lane_exit=0
$ ( cd / && bash /tmp/revq3_recheck.sh; echo "root_exit=$?" )
<same twelve lines, byte-identical>
root_exit=0
```

11 assertions (Q1–Q11) + the sha256 pin, each `occurrences=1`, exit 0 from the lane root **and** from `/`.
No line carries `normalized=` — every asserted quote is a raw substring, so the raw branch at
`corpus/instruments/source-recheck.py:201-203` prints `occurrences=` alone; the `normalized=` token exists only on the
normalize-only branch (`:204-209`).

### 1.2 Manifest assertion set and capture pin

```
$ python3 -c "import json;d=json.load(open('corpus/source-snapshots/round-31/manifest.json'));s=d['sources'][0];print(s['id'],s['path'],len(s['quotes']),[q['id'] for q in s['quotes']])"
S048 S048.txt 11 ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11']
$ # quote word counts from the same record
Q1 10  Q2 19  Q3 6  Q4 14  Q5 11  Q6 11  Q7 9  Q8 11  Q9 23  Q10 13  Q11 14   (max 23)
$ sha256sum corpus/source-snapshots/round-31/S048.txt ; wc -l -c corpus/source-snapshots/round-31/S048.txt
2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55  corpus/source-snapshots/round-31/S048.txt
  97 3755 corpus/source-snapshots/round-31/S048.txt
```

Manifest purpose declares the comparison normalization: `Normalization: capture-source.py's html_to_text() output is
compared under source-recheck.py normalize() (markup tags such as <u>...</u> stripped, all whitespace collapsed to single
spaces)`. Record `path` `S048.txt` and `id` `S048` are stem-equal; the instrument enforces that at
`source-recheck.py:123-126` (`reason=stem-mismatch`, exit 1). The 3755 B / 97-line / sha256 values match the entry's
§Scope (L164-165) and the wave-1 capture receipt (`wave1/ExecCapManifest.md`: `status=200 fetched_bytes=81802
snapshot_bytes=3755 sha256=2001ad77…e55 utc=2026-10-25T23:29:53Z`).

### 1.3 Fail-closed controls (Q7)

```
$ python3 corpus/instruments/source-recheck.py --selftest; echo "selftest_exit=$?"
SELFTEST clean PASS expected-exit=0 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST corrupt PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256 observed-ids=S900:sha256
SELFTEST missing-source PASS expected-exit=2 observed-exit=2 expected-ids=S900:source observed-ids=S900:source
SELFTEST missing-manifest PASS expected-exit=2 observed-exit=2 expected-ids=manifest observed-ids=manifest
SELFTEST stem-mismatch PASS expected-exit=1 observed-exit=1 expected-ids=S901:manifest observed-ids=S901:manifest
SELFTEST double-occurrence PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST double-occurrence-anchored PASS expected-exit=0 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST double-occurrence-out-of-range PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST double-occurrence-broken PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST quote-absent PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
selftest cases=10 failures=0
selftest_exit=0
```

Corrupted source exits 1; missing source and missing manifest exit 2 — the recheck fails closed when the base is absent.

### 1.4 Every cited cross-entry location, opened, with the quoted string counted **at that location**

```
$ sed -n '15p' corpus/source-snapshots/round-25/S036.txt
当社が利用しているサードパーティー製品
$ sed -n '15p' corpus/source-snapshots/round-25/S036.txt | grep -c '当社が利用しているサードパーティー製品'   → 1
$ sed -n '35p' corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md                 → > 当社が利用しているサードパーティー製品
$ sed -n '35p' corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md | grep -c '当社が利用しているサードパーティー製品'   → 1
$ sed -n '23p' corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
> 情報セキュリティ早期警戒パートナーシップや、脆弱性報奨金制度を含む外部からの報告、社内での検出などです。
$ sed -n '23p' … | grep -c '社内での検出'                                                     → 1
$ sed -n '25p' corpus/knowledge/multiparty-vulnerability-coordination.md | grep -c 'Optional participant that can assist vendors and finders'   → 1
$ sed -n '185,193p' corpus/source-snapshots/round-25/S040.txt | grep -c 'manage a coordinated industry disclosure'   → 1
$ sed -n '185,193p' corpus/source-snapshots/round-25/S040.txt | grep -c 'may impact multiple vendors'                → 1
$ sed -n '211p' corpus/README.md | grep -c "A vendor's published policy is a standing first-party statement, not a programme"   → 1
$ sed -n '506p' corpus/source-snapshots/round-25/S039.txt | grep -c '情報セキュリティ早期警戒パートナーシップの脆弱性関連情報の届出窓口に報告することで'   → 1
```

`S036.txt` carries the Cybozu phrase twice in the whole capture (L15 under `対象範囲`, L31 in a disclosure-procedure
sentence); the entry cites **L15**, which is the handling-scope line, and the phrase is on L15 exactly once. The
policies-entry quote at `:35` is unique. The internal-detection fragment is on policies `:23` exactly once.

### 1.5 The refuted wave-2 strings are gone from the current bytes

```
$ grep -n 'own products\|third-party products it uses\|outside the vendor' corpus/knowledge/vendor-third-party-finding-coordination.md
(no output; exit 1)
```

The `own products` F10 thesis (wave-2 F1), the translated rendering in quote marks (wave-3 R1) and the F06
`outside the vendor` gloss (wave-3 R3) occur **0 times** on the current bytes.

### 1.6 Every cross-entry quote measured against its own file (occurrence, words)

```
$ # under source-recheck normalize(): markup stripped, whitespace collapsed
1 11 'as a vendor affected by vulnerabilities in its products and services'          (S048 L35)
1 11 'as a finder of new vulnerabilities in third-party products and services'       (S048 L35)
1  9 'as a coordinator of vulnerabilities that affect multiple vendors'              (S048 L35)
1  6 'that are not developed by Microsoft'                                            (S048 L34)
1  8 'with the affected vendor to fix the issue'                                      (S048 L32)
1  5 'reported to the affected vendor'                                                (S048 L34)
1 23 'MSVR is a program specifically designed to help improve the security ecosystem…' (S048 L29)
1 14 'products that run on Microsoft operating systems, but that are not developed by Microsoft' (S048 L34)
$ sed -n '211p' corpus/README.md     → | F10 | Vendor-side disclosure policies as corpus objects | admitted | … A vendor's published policy is a standing first-party statement, not a programme: read its intake channels, …
```

Every S048 quote span in the entry is verbatim, exactly-once, and ≤25 words (longest 23). The README F10 row quoted at
entry L70 resolves uniquely at `README.md:211`; the F10 row identifier is the location, no line number is printed.

### 1.7 Every number the entry states, recounted on the pinned capture

```
$ C=corpus/source-snapshots/round-31/S048.txt
labelled routes (FC-1) = 3   in three ways = 1    only(ci) = 0
coordinator-of-vulns (FC-2) = 1   clock(ciE) = 0   @microsoft(ci) = 0   http(ci) = 0
bounty 28,35 = 0   bounty all = 1   affected vendor = 2
CERT/CC = 0   JPCERT = 0   IPA = 0
cert(ci) = 1 at L48 "Certified Refurbished"     bounty at L15 "Microsoft Bug Bounty Programs"
typo "third-party product of affects both" = 1
```

Every FC-1…FC-5 figure and every §Honest-limit figure reproduces exactly. Residual sweep run as written:

```
$ for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities'; do grep -rli -- "$t" corpus/knowledge/*.md; done
== MSVR            corpus/knowledge/vendor-third-party-finding-coordination.md
== MSRC            corpus/knowledge/vendor-third-party-finding-coordination.md
== research programme            corpus/knowledge/vendor-third-party-finding-coordination.md
== coordinator of vulnerabilities            corpus/knowledge/vendor-third-party-finding-coordination.md
```

One file per term — the entry itself. `grep -lE '^source: S048 ' corpus/knowledge/*.md` → exactly this one file.

### 1.8 Registry, tier, cadence convention, anchors

```
$ sed -n '54p' corpus/SOURCES.md | cut -c1-120
| S048 | Microsoft Security Vulnerability Research (MSVR) — https://www.microsoft.com/en-us/msrc/msvr | docs | A | Microsoft's o…
$ sed -n '24p;45,47p' corpus/SOURCES.md | cut -c1-110      # S018, S039, S040, S041 rows
… all four rows carry tier `A` …
$ grep -h '^recheck:' corpus/knowledge/*.md | wc -l                                      → 44
$ grep -h '^recheck:' corpus/knowledge/*.md | grep -ciE '180d|90d|30d|cadence'           → 0
$ grep -rn 'vendor-third-party-finding-coordination\.md:[0-9]' corpus/ SKILL.md          → (no match; exit 1)
$ git -C … log --oneline -- corpus/knowledge/vendor-third-party-finding-coordination.md
0de072c round-31: residual-call integration (F15 entry Q3 repair, …)
fd29aac round-31: wave-2 integration (…)
eecad59 round-31: wave-1 integration (…)
$ git -C … diff HEAD --stat -- corpus/knowledge/vendor-third-party-finding-coordination.md   → (empty)
```

Registry cell: `docs | A | … opened 2026-10-25 | 180d | corpus/knowledge/vendor-third-party-finding-coordination.md`.
0 of the lane's 44 knowledge `recheck:` lines carry a cadence token, so the cadence living in the registry cell is the
lane convention (see NIT-3). No other file in `corpus/` or `SKILL.md` cites this entry by line number, so R6 is
non-binding for this file.

### 1.9 Documentation-only scan (Q6)

```
$ grep -no 'https\?://[^ )]*' <entry>
2:https://www.microsoft.com/en-us/msrc/msvr
$ grep -nE 'vault|token|Bearer|op://|session|curl |wget |POST |<u>' <entry>
172:  session or private URL.
$ grep -nE '[0-9a-f]{32}' <entry>
165:  sha256 `2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55`. Page-level
```

One public documentation URL; no credential, session, vault or op-scheme material; the capture's per-request `Trace Id`
value is not carried (the only 64-hex string is the snapshot pin, and flag L123 mentions the `Trace Id` field, not its
value). No probe/login/submission instruction.

## 2. Q1–Q10, one row per criterion (current bytes)

| id | verdict | line(s) | quote / evidence |
|---|---|---|---|
| Q1 | pass (convention) | 1–5 | L2 `source: S048 — https://www.microsoft.com/en-us/msrc/msvr — section "Microsoft Security Vulnerability Research (MSVR)", capture corpus/source-snapshots/round-31/S048.txt:28-35`; L3 `verified-at: 2026-10-25`; L4 `recheck: cd …/kasegi-shokunin && python3 corpus/instruments/source-recheck.py … --source S048`; the three header lines sit directly under the H1 (L1). Cadence `180d` lives in the registry cell (`SOURCES.md:54`); 0 of 44 lane `recheck:` lines carry one (§1.8). |
| Q2 | pass | 2, 5; SOURCES.md:54 | Sole new-ground row S048 is `docs | A`, `opened 2026-10-25` (the admitting round), `status mined`; contrast rows S018/S039/S040/S041 are all tier `A` (§1.8); no tier-C row appears, so none is sole support. |
| Q3 | pass | all quoted spans | Every quoted span is verbatim, ≤25 words, with its exact location, counted at that location: S048 L29 (23 w), L31 (10 w), table rows L26-28 (19/6/14 w), L34 scope (14 w), L34 qualifier (6 w), L35 CVD (11 w) and roles (11/11/9 w) — §1.2, §1.6; F06 `"Optional participant that can assist vendors and finders"` at `multiparty-vulnerability-coordination.md:25`; README F10 row text at `README.md:211`; `"may impact multiple vendors"` and `"manage a coordinated industry disclosure"` inside `S040.txt:185-193`; `当社が利用しているサードパーティー製品` at `S036.txt:15` and policies `:35`; `社内での検出` at policies `:23`; `届出窓口` at `S039.txt:506` with the verbatim quote carried in policies Claim 7 (`:131-132`). All FC/honest-limit numbers reproduce (§1.7). |
| Q4 | pass | 9–11, 17, 41, 81–82 | L9 `Every statement below is Microsoft's own description of its own programme`; L11 `not a rule about vendors in general`; claim headings L17/L41 read `Microsoft's MSVR states…`; the F06/F10/F11 statements are about those entries, not about vendors; L81-82 is a negative claim over three individually cited objects. |
| Q5 | pass | 128–160 | FC-1…FC-5 are runnable and reproduce (§1.7); five rejected over-generalizations each with a reason (L139, L143, L147, L150, L155), and FC-1/FC-5 name the package error a reader can refute (`A package claiming a fourth MSVR intake route is unsupported by this capture`, L131). |
| Q6 | pass | 2, 170–172 | `It instructs no probing, scanning, login or submission against any target`; one public documentation URL; no credential/session/vault material; the capture `Trace Id` value is not carried (§1.9). |
| Q7 | pass | 4 | Command (not prose), `bash -n` exit 0, exit 0 from the lane root **and** from `/`; output names the pin (`S048:sha256 OK`) and each assertion with `occurrences=1`; note ends `a captured-source comparison, not a fresh network verification`; corrupted source exits 1 and missing source/manifest exit 2 (§1.1, §1.3). |
| Q8 | pass (residual) | 165–169 | L168 `source-recheck.py`'s declared normalization (capture markup stripped, whitespace collapsed)`; the manifest purpose declares the same. Residual NIT-5: this record's run prints `occurrences=` with no `normalized=` token because all 11 quotes are raw substrings. |
| Q9 | pass | manifest record; 167 | `path` `S048.txt` / `id` `S048` stem-equal (enforced `source-recheck.py:123-126`); 11 quotes, every one `occurrences=1`; the run prints the observed count; no anchor needed and none is declared. |
| Q10 | pass | 4 | `bash -n` exit 0; one command carrying its own `cd <lane-root> &&` prefix; the human note sits after `#`; exit 0 from `/` (§1.1). |

## 3. Status of the two prior refusals on the CURRENT bytes

| finding | status | current-bytes evidence |
|---|---|---|
| RevEntryQ F1 / Q3 — F10 `own products` thesis unlocated and refuted | **resolved** | The sentence is absent (§1.5). L69-70 grounds F10 in `README.md` F10 row `"A vendor's published policy is a standing first-party statement, not a programme"` (verbatim at `README.md:211`), and addition 3 (L97-99) is restated as `the finder direction of the Cybozu third-party-products scope`. |
| RevEntryQ F2 / RevQuoteRoutes F1 — assertion note broader than the manifest | **resolved** | L4 now reads `11 assertions (Q1-Q11), each exactly-once in the pinned capture; the three route labels at L26-28 and the strings in the falsifiable checks are hand-measured, not manifest-bound`; the manifest carries Q1–Q11 (§1.2) and every one is exactly-once. What remains is the token `L26-28` reading ambiguously as capture lines — NIT-1. |
| RevEntryQ F3 / RevQuoteRoutes F3 — route-3 scope wider than the page | **resolved** | L30 `Route 3 is scoped by Microsoft to non-Microsoft products that run on Microsoft operating systems (see the quote)`; the L32/33 blockquote is S048 L34 verbatim, and the qualifier `As time and resources permit` is asserted as manifest Q10. |
| RevEntryQ F4 / RevQuoteRoutes F5 — `standing` internal-research route | **resolved** | L87 `**A conditional internal-research route into other vendors' products.**`, quoting `"As time and resources permit" (L34)` — 5 words, occurrence 1 (§1.6). |
| RevEntryQ F5 / RevQuoteRoutes F6 / RevEntryQ2 R5 — route-2 trigger narrowed | **not taken (trivial)** | L36-37 `an external report filed against a Microsoft product that the reporter believes also affects a third-party product (or affects both)`; S048 L33 says `they believe affects a Microsoft product but that either affects …`. `filed against` narrows the page's `affects`; the table row at L27 carries the exact text. Paraphrase outside quote marks — not a Q3 fail. Carried as LOW-2. |
| **RevEntryQ2 R1 — translated string inside quote marks** | **resolved** | L78-79 `Cybozu's handling scope covers 当社が利用しているサードパーティー製品 (S036.txt:15, quoted at line 35 of knowledge/vendor-disclosure-policies-as-corpus-objects.md), the third-party products Cybozu itself uses`; the Japanese string is verbatim on `S036.txt:15` and on policies `:35` (counts 1/1, §1.4); the English is prose outside quotation marks. |
| **RevEntryQ2 R2 — internal-detection claim without a verbatim quote** | **resolved** | L80-81 `(c) internal detection with no coordinator named — 社内での検出 (line 23 of the same entry)`; fragment is verbatim on policies `:23` (count 1, §1.4), and that line names no coordinator. |
| **RevEntryQ2 R3 — F06 coordinator stated as `outside the vendor`** | **resolved** | L63-67 `its coordinator is an "Optional participant that can assist vendors and finders" (line 25), so its worksheet asks a package to record whether a coordinator exists rather than to assume one. Nothing at line 25 says the coordinator cannot be a vendor`; the `outside` token is 0 times in the file (§1.5), and L156 quotes only `"Optional participant"`. |
| **RevEntryQ2 R7 — flattening summary sentence** | **resolved** | L81-82 now reads `None of the three is a vendor stating a programme whose subject is other vendors' products, and none names the vendor as coordinator.` Each of the three shapes is stated with its own quote/location above it (external centre L71-77; products it uses L77-80; internal detection L80-81), so the summary no longer flattens concession (b) or asserts a coordinator where none is named. |
| RevEntryQ2 R4 — L4 coverage note | **resolved in substance** | The over-claim `covering the entry's S048 quotes` is gone; the note now separates manifest-bound assertions from hand-measured strings and disclaims network verification. See NIT-1 for the residual ambiguity. |
| RevEntryQ2 R6 — manifest Q3 `location` drops the page precondition | **not taken (documentation only)** | Manifest Q3 `location` still reads `L33; route 2, external researcher reports to the MSRC that affect a third-party product or both parties`; the instrument does not read `location` (Q9), so nothing is mis-verified. NIT-4. |

## 4. Findings, by severity

No HIGH and no MEDIUM finding remains on the current bytes; nothing falsifies a load-bearing claim.

### LOW-1 — the recheck note's `L26-28` pointer is ambiguous in a file whose `L<n>` tokens mean capture lines

`corpus/knowledge/vendor-third-party-finding-coordination.md:4`:

> `the three route labels at L26-28 and the strings in the falsifiable checks are hand-measured, not manifest-bound`

Everywhere else in this entry `L<n>` denotes a **capture** line (`L29`, `L31`, `L32-L34`, `L35`). Read under that
convention, `L26-28` points at capture lines 26–28, which are navigation chrome and the section heading
(`AI Safety Acknowledgements`, `Security Researcher Leaderboard`, `Microsoft Security Vulnerability Research (MSVR)` —
`sed -n '25,28p' S048.txt`) and hold no route label; the labels are on capture L32, L33, L34 and in the entry's table at
**entry** lines 26–28. One-clause fix, same line, executable-safe: `the three route labels (entry table lines 26-28)`.
No quoted string is claimed to sit at capture L26-28, so this is a pointer defect in the note, not a false claim.

### LOW-2 — route-2 paraphrase still narrows the page's trigger (carried, unchanged)

L36-37: `an external report filed against a Microsoft product that the reporter believes also affects a third-party
product (or affects both)`. S048 L33 (verbatim): `an external researcher will report an issue that they believe affects
a Microsoft product but that either affects a third-party product of affects both the Microsoft product and external
parties` (sic). `filed against` replaces the page's `affects`, and `believes` is attached one clause left of where the
page puts it. The table row at L27 keeps the exact sentence, so a reader cannot mistake the paraphrase for source
wording; Q3 is satisfied by the table, not by this paragraph. Fix if the file is touched: `an external report that the
reporter believes affects a Microsoft product`. Identical to RevEntryQ F5 / RevQuoteRoutes F6 / RevEntryQ2 R5.

### NIT-1 — the note's hand-measured clause does not say the labels are exactly-once

The note says the labels are `hand-measured, not manifest-bound`; measured here, each of the three label strings occurs
exactly once in S048 (table quotes, §1.6), and FC-1's labelled-route `grep -cE` prints `3`. Rewording to `hand-measured
exactly-once` would close the same loop RevEntryQ2 R4 opened, in the same line as LOW-1's fix.

### NIT-2 — `recheck:` carries no cadence token (Q1 read literally)

Q1's letter asks the `recheck:` field to carry `date or cadence plus the runnable command`. L4 carries the command and
its note, no cadence; the registry cell carries `180d` (`SOURCES.md:54`). The lane's own convention is 0 of 44
knowledge `recheck:` lines with a cadence token (§1.8), so this seat does not fail Q1 on it. If literal compliance is
wanted, append `cadence 180d;` inside the existing `#` note (keeps `bash -n` and cwd-independence intact).

### NIT-3 — README F10 row cited by row id, not line

L69-70 cites `corpus/README.md` F10 row; the quoted text is unique at `README.md:211`. Q3's "exact location" allows a
section/row identifier, and the row id resolves uniquely (grep prints one line). Optional: add `:211`.

### NIT-4 — manifest Q3 `location` still omits the page's precondition

`location` reads `L33; route 2, external researcher reports to the MSRC that affect a third-party product or both
parties`, dropping the page's `they believe affects a Microsoft product`. Documentation only: `source-recheck.py` never
reads `location`; the binding is quote + occurrence count (Q9). Carried from RevEntryQ2 R6.

### NIT-5 — Q8's `normalized=` token is not exhibited by this record's run

All 11 asserted quotes are raw substrings, so the instrument takes the raw branch (`source-recheck.py:201-203`) and
prints `occurrences=` only; the normalize-only branch (`:204-209`) prints `normalized=markup-whitespace`. The
normalization is declared in the manifest purpose and named at entry L168. No assertion in this record depends on
normalization, so nothing is unverified; a future record whose quote needs normalization will print the token.

### NOTE — the L81-82 summary is now accurate but load-bearing on the word `programme`

`None of the three is a vendor stating a programme whose subject is other vendors' products` is true of the three
objects as cited (a policy paragraph about incidents that may impact other vendors is not a programme; a handling scope
is not a programme; an internal collection channel is not a programme). A downstream package that drops `programme` and
reads the sentence as "no vendor states anything about other vendors' products" would over-read it, but Cisco's
`Incidents that may impact other vendors` paragraph is quoted at L74-76 immediately above, and addition 3 (L97-99)
already scopes the novelty to `A published programme whose subject is other vendors' products`. Not a defect on these
bytes; recorded because it is the sentence a critic will attack next.

## 5. Verdict

**ADMIT.** Q1–Q10 all pass on the evidence in §1–§2, and every blocking finding of the two prior refusals is resolved
on the current bytes (§3): the translated string is now the Japanese capture text with the English gloss outside
quotation marks (R1), the internal-detection concession carries `社内での検出` with its location (R2), the F06
`outside the vendor` exclusion is gone and replaced by the non-exclusion sentence (R3), and the flattening summary is
replaced by a negative claim that holds for each of the three individually cited shapes (R7). The F10 `own products`
thesis that caused the first refusal is absent.

Reasons the verdict is not REFUSE: the only findings left are LOW/NIT — an ambiguous `L26-28` token in a human note
(LOW-1), a paraphrase outside quote marks that the table already quotes exactly (LOW-2), and four documentation nits
(NIT-1…NIT-5). None of them makes a load-bearing claim unreproducible from the pinned capture, and none requires a
correction to a quote, a number or an attribution. Route LOW-1 (one clause) and NIT-1 with the next touch of the file;
LOW-2 only if the paragraph is edited anyway.

## 6. Residual risk and verification gaps

- **Upstream is not re-verified here.** This seat compared entry ↔ pinned capture ↔ instruments. It did not fetch
  `https://www.microsoft.com/en-us/msrc/msvr` (documentation-only seat; the entry states the same limit at L167-169).
  Capture authenticity rests on the wave-1 receipt (`wave1/ExecCapManifest.md`: HTTP 200, 81802 B fetched, 3755 B
  snapshot, sha256 `2001ad77…e55`, utc 2026-10-25T23:29:53Z), which this seat opened and read.
- **Q8 token gap stands** (NIT-5): the run prints `occurrences=` without `normalized=` because every assertion is a raw
  substring; the declared normalization is manifest purpose + entry §Scope, not something this record's output exhibits.
- **The manifest has no `captured_at` field**; the 23:29:53Z time is receipt-grounded, not manifest-grounded.
- **Coverage measurement is span-level.** §1.6 counts quoted spans found in the capture and their word counts; it does
  not judge whether a span is load-bearing. Spans this seat classified as illustrative (capture L15 `Microsoft Bug
  Bounty Programs`, L48 `Certified Refurbished`, the L33 sic typo) are unasserted and could matter to a critic.
- **Instrument semantics only.** This seat ran `source-recheck.py`'s selftest and the S048 record; limb-level mutation
  of that instrument is C1's ledger work (`SR-*` rows), not this seat's, and no limb claim is made or re-measured here.
- **Quiescence.** Entry sha256 `a488df49…d56f` and manifest `9693fa3c…8410` were identical at the start and end of this
  review; the working tree matched HEAD for the entry (`git diff HEAD --stat` empty). Nothing in this receipt was
  measured against a file another seat was editing.
- All evidence commands were read-only; the only lane file written by this seat is this receipt.
