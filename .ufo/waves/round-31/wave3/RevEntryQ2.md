# RevEntryQ2 — independent re-review of `corpus/knowledge/vendor-third-party-finding-coordination.md` after the wave-2 repair

- Seat: `RevEntryQ2` (round 31, wave 3). Leaf; no subagents, no background jobs, no delegation.
- Answering model actually run (bound 10, from the workstation config route table; no model passed by this seat): `opencode-go/deepseek-v4.1-flash`.
- Review target (not written and not previously reviewed by this seat):
  `corpus/knowledge/vendor-third-party-finding-coordination.md`, 170 lines, 12549 B,
  sha256 `8c0b7331e2809ee529266d99cedb853bbce22acca7cbfaec92b307b2e5756eba`, mtime 2026-10-25 21:59:33 -0300.
- Quiescence (M30-3): the entry sha256 above was re-measured at the end of this review, identical to the value at the
  start; manifest `9693fa3c8a164c97aab3b58f694aaa2644e716a32b31194d55ee744e4cbc8410`, mtime 21:57:52 -0300.
  Every reading below is on quiescent bytes.
- Lane HEAD read: `a155310d1ee9aacc07c3ce62328105a46c0392b4`; the repair under review is in `fd29aac` (wave-2 integration).
  `git log -- corpus/knowledge/vendor-third-party-finding-coordination.md` → `fd29aac`, `eecad59` only.
- Repairs re-read before judging: `.ufo/waves/round-31/wave2/RevEntryQ.md` (REFUSE, Q3),
  `.ufo/waves/round-31/wave2/RevQuoteRoutes.md` (F1–F7), `.ufo/waves/round-31/wave2/CritExpansion.md` §6 (three edits).
- Writes: this receipt only. Scratch `/tmp/revq2.sh` (removed at exit); no lane file, no git/jj mutation, no pacman/uv/npx
  transaction (nothing needed), no network access, no campaign-package tool run.

## 1. Commands run and their output

### 1.1 The entry's own `recheck:` line — extraction, `bash -n`, lane root, `/`

```
$ E=corpus/knowledge/vendor-third-party-finding-coordination.md
$ CMD=$(grep -m1 '^recheck: ' "$E" | sed 's/^recheck: //; s/[[:space:]]*#.*$//')
$ printf 'CMD=[%s]\n' "$CMD"
CMD=[cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048]
$ bash -n /tmp/revq2.sh; echo "bash_n=$?"
bash_n=0
$ ( cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && bash /tmp/revq2.sh; echo "lane_exit=$?" )
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
$ ( cd / && bash /tmp/revq2.sh; echo "root_exit=$?" )
<the same twelve lines, byte-identical>
root_exit=0
```

11 assertions (Q1–Q11) + the sha256 pin, each `occurrences=1`, exit 0 from both cwds. No line carries
`normalized=`, i.e. every asserted quote is a raw substring (the raw branch), consistent with the entry's §Scope claim
of a markup-stripped/whitespace-collapsed comparison.

### 1.2 Manifest now carries Q1–Q11

```
$ python3 -c "import json;d=json.load(open('corpus/source-snapshots/round-31/manifest.json'));q=d['sources'][0]['quotes'];print(len(q),[x['id'] for x in q])"
11 ['Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8','Q9','Q10','Q11']
```

`Q9` = L29 programme self-description (23 words), `Q10` = L34 "As time and resources permit…" (9), `Q11` = L34
"products that run on Microsoft operating systems, but that are not developed by Microsoft" (14). The two
RevEntryQ-F2 spans (L29, L34 scope) are now asserted; the L34 qualifier the entry quotes in addition 1 is asserted too.

### 1.3 Fail-closed controls (`Q7`)

```
$ python3 corpus/instruments/source-recheck.py --selftest; echo "selftest_exit=$?"
SELFTEST clean PASS expected-exit=0 observed-exit=0 ...
SELFTEST corrupt PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256 observed-ids=S900:sha256
SELFTEST missing-source PASS expected-exit=2 observed-exit=2 expected-ids=S900:source observed-ids=S900:source
SELFTEST missing-manifest PASS expected-exit=2 observed-exit=2 expected-ids=manifest observed-ids=manifest
SELFTEST stem-mismatch PASS ... SELFTEST double-occurrence PASS ... SELFTEST double-occurrence-anchored PASS ...
SELFTEST double-occurrence-out-of-range PASS ... SELFTEST double-occurrence-broken PASS ... SELFTEST quote-absent PASS ...
selftest cases=10 failures=0
selftest_exit=0
```

Corrupted source (exit 1) and missing source/manifest (exit 2) both fail closed.

### 1.4 Every number the entry states, recounted on the pinned capture

```
$ C=corpus/source-snapshots/round-31/S048.txt
labelled routes (FC-1) = 3      in three ways = 1        only(ci) = 0
coordinator-of-vulns (FC-2) = 1 clock(ciE) = 0           @microsoft(ci) = 0        http(ci) = 0
bounty 28,35 = 0                bounty all = 1           affected vendor = 2
CERT/CC = 0                     JPCERT = 0               IPA = 0
cert(ci) = 1 at L48 "Certified Refurbished"
bounty at L15 "Microsoft Bug Bounty Programs"
typo "third-party product of affects both" = 1
wc -c = 3755   wc -l = 97   sha256 = 2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55
```

Every FC-1…FC-5 figure and every §Honest-limit figure in the entry reproduces exactly. The negative sweep also
reproduces: four terms, one knowledge file each (the entry itself).

### 1.5 Every cross-entry citation in "What this adds beyond F06 and F10", opened

| entry citation (line) | cited bytes opened | holds? |
|---|---|---|
| `multiparty-vulnerability-coordination.md` line 25 (L63-65) | `:25` = `“Optional participant that can assist vendors and finders in handling and disclosing vulnerability information.”` | quote verbatim (prefix, 9 words); see R3 for the gloss |
| `corpus/README.md` F10 row (L69-70) | `README.md:211` = `…A vendor's published policy is a standing first-party statement, not a programme: read its intake channels…` | verbatim prefix ✓ (row id resolves uniquely; no line number given) |
| `S039.txt:506` quoted in policies Claim 7 (L71-72) | policies `:126` Claim 7; `:131-132` quote `情報セキュリティ早期警戒パートナーシップの脆弱性関連情報の届出窓口に報告することで — 1.2 …, capture S039.txt:506`; `S039.txt:506` opened (Hitachi HIRT 製品開発工程, 他社製品に影響する場合 → 届出窓口) | ✓ |
| `S040.txt:185-193`, `cisco-jpcert-partner` row (L73-76) | `S040.txt:185` `Incidents that may impact other vendors: The Cisco PSIRT works` … `:193` `…on the incident reporter?s behalf.`; crosswalk `:49` = `| cisco-jpcert-partner | Cisco (S040) | "Japan Computer Emergency Response Team (JP-CERT)" | L189, … paragraph "Incidents that may impact other vendors" (wrapped L188-L189) |` | ✓ (row id resolves at `:49`; no line number given) |
| `S036.txt:15`, "line 35" of policies (L76-78) | `S036.txt:15` = `当社が利用しているサードパーティー製品`; policies `:35` = the same Japanese blockquote; policies `:33` = prose `Handling scope covers… plus third-party products it uses:` | **quote fails** — the quoted English is not at either location (R1) |
| "line 23" of policies (L78-79) | policies `:23` = `情報セキュリティ早期警戒パートナーシップや、脆弱性報奨金制度を含む外部からの報告、社内での検出などです。` | line resolves; no verbatim quote carried (R2) |
| `iso-29147-and-30111-division-of-labour.md` / S041 (L99-101) | `grep -niE 'finder|coordinator|seat'` on that entry → no match; `SOURCES.md:47` S041 tier `A` | ✓ |
| F06 "has no row for a vendor occupying the finder and coordinator seats itself" (L66-67) | F06 table rows `:25-30` (Coordinator, Upstream Vendor, communications, minimize exposure, use coordinators) — none seats a vendor as finder/coordinator | ✓ |
| F10 row text "not a programme" (L69-70) | README `:211` as above | ✓ |

Tier check for Q2 (`SOURCES.md`): S048 `:54` `docs | A | … opened 2026-10-25`, S018 `:24`, S039 `:45`, S040 `:46`,
S041 `:47` all tier `A`; no tier-C row appears anywhere in the entry.

### 1.6 What the repair actually changed (`git diff eecad59..HEAD`)

The diff is confined to: the L4 note (8→11 assertions), L30 route-3 scope, the whole "What this adds" paragraph,
FC-5's L33 clause, and the §Scope eleven-quote line. Per-line anchors elsewhere are untouched (R6: no other file cites
this entry by line — `grep -rn 'vendor-third-party-finding-coordination.md:[0-9]' corpus/ SKILL.md` → no match).

### 1.7 Assertion coverage of the entry's quoted S048 spans

```
assertions = 11
entry carries 15 substantive S048 quote spans (7 blockquotes + 6 table cells + 2 inline in addition 1)
covered: L29, L31, the three route-handling statements, the three roles, the CVD sentence, the L34 qualifier, the L34 scope
not covered: the three route LABELS at L26-28 — "Internal Microsoft engineers", "External reports to the Microsoft
             Security Response Center (MSRC)", "Internal research projects"
each label is exactly-once (FC-1's labelled-route grep → 3)
also quoted-but-unasserted, all illustrative chrome: "Microsoft Bug Bounty Programs" (L15), "Certified Refurbished"
(L48), the sic typo (L33)
```

## 2. Q1–Q10, one row per criterion (current bytes)

| id | verdict | line(s) | quote / evidence |
|---|---|---|---|
| Q1 | pass | 1–5 | L2 `source: S048 — https://www.microsoft.com/en-us/msrc/msvr — section "Microsoft Security Vulnerability Research (MSVR)", capture corpus/source-snapshots/round-31/S048.txt:28-35`; L3 `verified-at: 2026-10-25`; L4 `recheck: cd …/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest … --source S048`. Cadence `180d` in the registry cell (`SOURCES.md:54`), matching the lane's convention (no `recheck:` line in `corpus/knowledge/*.md` carries one). |
| Q2 | pass | 2; 5; SOURCES.md:54 | Sole load-bearing row S048 is `tier A`, `opened 2026-10-25` (admitting round), `status` mined. Contrast rows S018/S039/S040/S041 all tier A (§1.5); no tier-C support anywhere. |
| Q3 | **fail** | 76–79 | (b) `handling scope already covers "third-party products it uses" (S036.txt:15, line 35 of knowledge/…)` — the quoted English occurs in `S036.txt` 0 times (`grep -c 'third-party' S036.txt` → `0`; L15 is `当社が利用しているサードパーティー製品`) and at policies `:35` 0 times (that line is the Japanese blockquote); it exists only as *unquoted prose* at policies `:33`. (c) `the same entry holds a vendor-internal detection channel (line 23)` carries no verbatim quote at all. All ten other load-bearing quotes (L14, L19, L26-28 cells, L32, L43, L48, L51, L54, L86) are verbatim and ≤25 words with exact locations. Detail: R1, R2. |
| Q4 | pass | 9–11, 17, 41 | L9 `Every statement below is Microsoft's own description of its own programme`; L11 `not a rule about vendors in general`; L17/L41 headings read `Microsoft's MSVR states…`. The F06 gloss at L64 is an interpretation but is attributed to the lane entry, not generalized to vendors (R3). |
| Q5 | pass | 124–158 | FC-1…FC-5 all reproduce (§1.4) and five rejected over-generalizations carry reasons, e.g. L137 `Every large vendor runs such a programme.` Rejected. |
| Q6 | pass | 2, 132, 168–170 | One public documentation URL (`:2`), no `curl`/`wget`/token/vault/`op://` match, capture Trace Id value not carried (L121 mentions the field only); L168-169 `It instructs no probing, scanning, login or submission against any target`. |
| Q7 | pass | 4 | Command (not prose); exit 0 from lane root **and** `/`; output names the pin and each assertion with `occurrences=1`; note ends `a captured-source comparison, not a fresh network verification`; corrupted/missing-source controls fail (exit 1 / 2). |
| Q8 | pass (residual) | 165–167 | L166 `source-recheck.py`'s declared normalization (capture markup stripped, whitespace collapsed)`; the manifest purpose declares the same. Residual: this record's run prints no `normalized=` token because all 11 quotes are raw substrings (normalize-only branch only). |
| Q9 | pass (residual) | manifest record; 165 | `path` `S048.txt`/`id` `S048` stem-equal, 11 quotes each `occurrences=1`, the run prints the observed count; no anchor needed. Residual: the three route labels quoted at L26-28 are unasserted (R4). |
| Q10 | pass | 4 | `bash -n` exit 0, one command with its own `cd <lane-root> &&` prefix, human note after `#`, exit 0 from `/` (§1.1). |
| R6 (line anchors) | pass | whole file | The repair touched only this entry; no other file cites it by line (§1.6). |

## 3. Status of the wave-2 findings and the CritExpansion edits

| finding | status | evidence |
|---|---|---|
| RevEntryQ F1 / Q3 (the `own products` thesis for F10) | **resolved** | L69-70 now grounds the distinction in `README.md:211` (`A vendor's published policy is a standing first-party statement, not a programme`), and addition 3 at L95-97 is restated as `the finder direction of the Cybozu third-party-products scope`; the refuted thesis is gone (`git diff` shows the sentence deleted). |
| RevEntryQ F2 (8 assertions vs the entry's quotes) | **partly resolved** | Q9/Q10/Q11 added and the note moved 8→11 (§1.2). But the note now says `covering the entry's S048 quotes`, and the three route labels at L26-28 remain unasserted (R4) — the same over-claim, smaller. |
| RevEntryQ F3 (route-3 scope wider than the page) | **resolved** | L30 `Route 3 is scoped by Microsoft to non-Microsoft products that run on Microsoft operating systems (see the quote)`. |
| RevEntryQ F4 / RevQuoteRoutes F5 ("standing" route) | **resolved** | L85 `A conditional internal-research route`, quoting `"As time and resources permit" (L34)`, now also asserted as Q10. |
| RevEntryQ F5 / RevQuoteRoutes F6 (belief placed over the third-party effect) | **not taken** | L35-37 unchanged: `an external report filed against a Microsoft product that the reporter believes also affects a third-party product (or affects both)`. R5. |
| RevQuoteRoutes F1 (note claims more coverage than the manifest) | **partly resolved** | See F2 row: 11 assertions now, three label spans still unasserted. R4. |
| RevQuoteRoutes F2 (FC-5 "L33 names only MSVR") | **resolved** | L133 `L33 names no affected vendor, and MSVR is its only stated handler.` |
| RevQuoteRoutes F3 (route-3 scope) | **resolved** | same edit as RevEntryQ F3. |
| RevQuoteRoutes F4 (Cisco "hands … to"; exemplar list) | **resolved** | L73-76 `works with coordination centres such as CERT/CC, CERT-FI, JP-CERT or NPSA to "manage a coordinated industry disclosure"`; `S040.txt:185-193` says `works with third-party coordination centers such as … to manage a coordinated industry disclosure`. |
| RevQuoteRoutes F7 (manifest Q3 `location` shorthand) | **not taken (documentation only)** | manifest Q3 `location` still reads `external researcher reports to the MSRC that affect a third-party product or both parties`, dropping the page's `they believe affects a Microsoft product` precondition. The instrument does not read `location` (Q9), so nothing is mis-verified. R6. |
| CritExpansion edit 1 (addition 3 → direction; drop "as a corpus object") | **resolved** | L95-97, plus the Cybozu scope named at L76-78 and `F13 already holds programme objects` respected by `This is a difference in what the page is about, not a new corpus-object type`. |
| CritExpansion edit 2 (addition 2 qualifications: Cisco manages; F06:25 does not exclude a vendor; point at F02:9) | **partly resolved** | Cisco qualification carried (L90-92 `work with external coordination centres to manage a coordinated industry disclosure`); **the F06 non-exclusion qualification was not carried** — L64 still reads `in it the coordinator is a participant *outside* the vendor`, and L154 repeats it; no F02:9 pointer (the entry points at `F06's worksheet line` instead). R3. |
| CritExpansion edit 3 (F10-ground paragraph names internal detection + third-party-products scope; drop "F10's vendor rows both") | **resolved** | L76-79 names both; L79-80 replaces the "both rows" sentence (but see R7 for the replacement's wording). |
| C2 kill-rule restatement clause | **passes** | Sweep in §1.4 gives one file per term; F15's residual is carried by additions 1 and 2, not a restatement of F06/F10. Nothing in this receipt asserts a score move. |

## 4. Findings, by severity

### R1 — **HIGH (blocking, Q3)** — a repaired clause quotes an English rendering of a Japanese capture as if verbatim

`corpus/knowledge/vendor-third-party-finding-coordination.md:76-78`:

> handling scope already covers "third-party products it uses" (S036.txt:15, line 35 of `knowledge/vendor-disclosure-policies-as-corpus-objects.md`)

Measured:

```
$ grep -c 'third-party' corpus/source-snapshots/round-25/S036.txt          → 0
$ sed -n '15p' corpus/source-snapshots/round-25/S036.txt                   → 当社が利用しているサードパーティー製品
$ sed -n '35p' corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md → > 当社が利用しているサードパーティー製品
$ sed -n '33p' corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md → Handling scope covers services and products Cybozu creates, plus third-party products it uses:
$ grep -rn 'third-party products it uses' corpus/   → the F10 entry's prose (:33) and this entry's quote (:77) only
```

The clause is new in the repair (`git diff eecad59..HEAD` shows it added), and it is the *first* of the three
overlap concessions that bound the novelty claim — the same role whose non-verbatim warrant caused the wave-2 refusal.
The claim is true (L15 does say "third-party products our company uses"), but the entry carries no verbatim quote for
it, and a downstream package that repeats `S036 says "third-party products it uses"` would be quoting a translation as
source wording. Fix (one clause): quote `当社が利用しているサードパーティー製品` with `S036.txt:15` / policies `:35` and gloss
in prose, or drop the quotation marks and cite policies `:33` as the lane entry's English prose.

### R2 — **MEDIUM (Q3)** — the third overlap concession carries no verbatim quote

L78-79: `(c) the same entry holds a vendor-internal detection channel (line 23)`. policies `:23` is
`情報セキュリティ早期警戒パートナーシップや、脆弱性報奨金制度を含む外部からの報告、社内での検出などです。` — the line resolves,
but Q3 asks each load-bearing claim to *carry* a verbatim quote; `社内での検出` is four characters and can be carried.
Fix as a same-line suffix (R6-safe).

### R3 — **LOW (Q4 / precision, and the one CritExpansion edit left undone)** — F06's coordinator is stated as "outside the vendor"

L63-66: `in it the coordinator is a participant *outside* the vendor — "Optional participant that can assist vendors
and finders" (line 25)`; repeated at L154 (`F06's coordinator is an optional participant outside the vendor`).
F06 `:25` says only `Optional participant that can assist vendors and finders in handling and disclosing vulnerability
information.` Nothing in `multiparty-vulnerability-coordination.md` says *outside* (`grep -niE 'outside|external'` → `:17`
only, about publishing/contacting). The exclusion is the entry's inference, and CritExpansion §4 supplied exactly the
qualification the repair did not carry ("nothing in `:25` or `:30` says the coordinator cannot be a vendor"). Not
refuted — F06 nowhere says the coordinator *is* a vendor — so this is a characterization over-read, not a Q3 fail. The
addition-2 claim survives on its own wording (`The new fact is coordinator-of-record being the vendor`, L93-94).

### R4 — **LOW (verifiability / RevQuoteRoutes F1, partly open)** — the L4 note's coverage claim is still broader than the manifest

L4: `# 11 assertions (Q1-Q11), each exactly-once in the pinned capture, covering the entry's S048 quotes`. The entry
quotes three route labels at L26-28 (`"Internal Microsoft engineers" (L32)`, `"External reports to the Microsoft
Security Response Center (MSRC)" (L33)`, `"Internal research projects" (L34)`) that no assertion binds. Each is
exactly-once under FC-1's own grep (3 labelled lines), so the exposure is silent drift only. Fix: `11 assertions
(Q1-Q11); the three route labels and the illustration strings are hand-measured exactly-once`, or add Q12/Q13/Q14.

### R5 — **TRIVIAL (precision)** — route 2's trigger is still narrowed

L35-37: `an external report filed against a Microsoft product that the reporter believes also affects a third-party
product (or affects both)`. `S048.txt:33` reads `an external researcher will report an issue that they believe affects
a Microsoft product but that either affects a third-party product of affects both the Microsoft product and external
parties` (sic). "filed against" narrows "affects", and "believes" sits one clause left of the page's placement. The
table row L27 keeps the exact text, so the risk is low; unchanged from RevEntryQ F5 / RevQuoteRoutes F6.

### R6 — **NIT (documentation)** — manifest Q3 `location` still drops the page's precondition

`"location": "L33; route 2, external researcher reports to the MSRC that affect a third-party product or both parties …"`
omits `they believe affects a Microsoft product`. Documentation only; the instrument does not read `location` (Q9).

### R7 — **NOTE (precision)** — the F10-overlap summary flattens the products-it-uses case

L79-80: `All of these are a vendor's statement about findings reaching it or its own products, with any coordinator
external.` For concession (b) the subject is third-party products Cybozu *uses* (neither "reaching it" nor "its own
products"), and concession (c) (internal detection) names no coordinator, so "any coordinator external" is vacuous
there. The sentence is the generalizing summary of the paragraph; see §5.

## 5. The single sentence that still most risks over-generalization

L79-80:

> All of these are a vendor's statement about findings reaching it or its own products, with any coordinator external.

It is the one sentence that generalizes three separately-cited statements into a single characterization, and it does so
by flattening the very concession the repair exists to state: Cybozu's `:33`/`:35` scope is third-party products the
vendor **uses** (S036.txt:15), which is neither "findings reaching it" nor "its own products", and concession (c)
(internal detection, policies `:23`) involves no coordinator at all, so "any coordinator external" does not describe it.
A downstream package reading L79-80 as F10's ground would conclude F10 holds no third-party-product scope, which is the
`own products` misreading that produced the wave-2 refusal — one level up. Suggested replacement: name the three
concession shapes as they are (external centre for Hitachi/Cisco; products it uses for Cybozu; internal detection with
no coordinator), which is also what makes addition 3 a matter of direction rather than of subject.

Runner-up: L64 `in it the coordinator is a participant *outside* the vendor` (R3) — an unsupported exclusion rather than
a corpus over-generalization.

## 6. Verdict

**REFUSE** — on **Q3 only**, for R1 (blocking) with R2 as the companion clause. Q1, Q2, Q4, Q5, Q6, Q7, Q8, Q9, Q10 pass
on the evidence in §1–§2, and the C2 restatement clause does not fire (§3 last row).

Reasons:
1. Q3 asks each load-bearing claim to carry a verbatim quote with its exact location. The repaired overlap concession now
   quotes an English rendering (`"third-party products it uses"`) whose bytes are at neither cited location — the capture
   `S036.txt` has 0 occurrences of `third-party`, and policies `:35` is the Japanese blockquote. The string exists only as
   the F10 entry's unquoted prose at `:33`.
2. The concession is load-bearing: it is one of the three places that bound what S048 adds, and the wave-2 refusal was
   caused by a non-verbatim warrant in the same function. Admitting a translated string as a source quote would put a
   quote that no reader can grep into the corpus, on the round's own verifiability axis.
3. Both fixes are one clause each and R6-safe as same-line suffixes: carry `当社が利用しているサードパーティー製品` and
   `社内での検出` (or drop the quotation marks and cite the lane entry's own prose).

Not blocking, but the L1 should route them with any next touch of the file: R3 (F06 "outside the vendor" — restore
CritExpansion's non-exclusion wording), R4 (the L4 coverage note), R7/L79-80 (§5), R5 and R6 (trivial).

## 7. Residual risk and verification gaps

- **Upstream is not re-verified here.** This seat read the entry ↔ pinned capture ↔ instruments only; it did not fetch
  `https://www.microsoft.com/en-us/msrc/msvr`. The live-agreement evidence remains RevQuoteRoutes §2 (8 of 97 lines
  identical except the per-request L2 Trace Id), not this receipt.
- **Q8 token gap stands.** My run prints `occurrences=` without `normalized=` because all 11 quotes are raw substrings;
  the declared normalization is entry text and manifest purpose, not something this record's output exhibits.
- **Coverage measurement is span-level, not semantic.** §1.7 counts quoted spans found in the capture; it does not judge
  whether a quoted span is load-bearing. A span I classified as illustrative (L15/L48/L33 typo) could matter to a critic.
- **Instrument semantics only.** I exercised `source-recheck.py`'s selftest and its S048 run; limb-level mutation of the
  instrument is C1's ledger work, not this seat's, and no limb claim is made or re-measured here.
- **Independence.** This seat wrote no part of the entry and did not review it in wave 1 or wave 2; the three wave-2
  receipts were read only to enumerate the findings I then re-tested against the bytes.
- All evidence commands were read-only; the only lane file written by this seat is this receipt.
