# RevQuoteRoutes — F15 route quotes vs a fresh capture (round-31 wave 2)

Scope: verify the three intake routes admitted under Frontier F15 (S048, MSVR) against my
own fetch of the page, against the pinned capture at the manifest's anchors, and against
every route sentence in `corpus/knowledge/vendor-third-party-finding-coordination.md`.

Result in one line: **all 8 manifest assertions AGREE** (exactly once, at the stated anchor,
wording equal to a fresh capture); the entry's route model is faithful; 5 low-severity
items (F1–F5: one verifiability, four wording) and 2 nits (F6–F7), one of them a literal
falsehood ("L33 names only MSVR"); no high-severity defect and nothing that touches the C2
predicate.

Working state: scratch `/tmp/revquoteroutes.OrSjnr` (outside the lane). The only lane file
written is this receipt. Instrument UA
`kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)` on both
fetches. Normalization used: `normalized=markup-whitespace` — `source-recheck.py`'s
`normalize()` (`</?u>` stripped, whitespace collapsed), applied to text produced by
`capture-source.py`'s `html_to_text()` imported read-only from the lane. Nothing installed;
no pacman; no git/jj mutation; no live bounty target contacted (two GETs to the one public
documentation URL my item names). This task is not model-dependent; session reports
`opencode-go/deepseek-v4.1-flash`.

Quiescence: the files I cite (manifest, S048.txt, the knowledge entry) are not on any
wave-2 single-writer list, and the entry's mtime is 2026-10-25 20:41:30 -03
(`sha256 1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb`), so every
reading below is on quiescent bytes. Manifest
`sha256 b80f7f92fbab57c0edbb73d181414560fe0e5e7102405f210865acc84a2f87be`.

## 1. Fresh fetch (two independent GETs)

```
$ curl -sS -o page.html -w 'status=%{http_code} bytes=%{size_download} url=%{url_effective}\n' \
    -A 'kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)' \
    'https://www.microsoft.com/en-us/msrc/msvr'
status=200 bytes=81802 url=https://www.microsoft.com/en-us/msrc/msvr
$ sha256sum page.html
da66476a78d67ec9d698e3a852a256934517d9b05333fcaa5ba04a95ea5dc503  page.html
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-26T00:24:00Z
```

Second GET at 2026-10-26T00:26:38Z: also `status=200 bytes=81802`.

Conversion to snapshot text (same converter the capture used, imported read-only):

```
$ python3 conv.py page.html fresh.txt      # capture-source.py html_to_text()
fresh_snapshot_bytes=3755 sha256=8bfcdba3ac37ac44f9ba8468e3d374a540bc52353b5828f5ae9b257db02ff6f5 lines=97
$ python3 conv.py page2.html fresh2.txt
fresh_snapshot_bytes=3755 sha256=7a3153df733ac180501782d18bf3ed289b17fbbb1b3b2da36fbe2aa7aedc69e7 lines=97
```

Both fetches: 81802 fetched B → 3755 snapshot B → 97 lines, i.e. the L1's byte count and the
entry's stated size/line count (3755 B, 97 lines) reproduce exactly.

## 2. Pin fidelity: the pinned capture is the live page, not a paraphrase

```
$ diff -u corpus/source-snapshots/round-31/S048.txt /tmp/revquoteroutes.OrSjnr/fresh.txt
@@ -1,5 +1,5 @@
-This is the Trace Id: f97e6b1cb578f714d23850f80f018bb3
+This is the Trace Id: 26adbb5a4b48637fd947f9d2d5607dd5
$ diff <(sed 2d pinned) <(sed 2d fresh.txt)   -> IDENTICAL_EXCEPT_L2
$ diff <(sed 2d fresh.txt) <(sed 2d fresh2.txt) -> FETCH2_IDENTICAL_EXCEPT_L2
```

Pinned `S048.txt` sha256 `2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55`,
97 lines — matches the manifest pin. Lines differing, pinned vs live: **1 of 97**, snapshot
L2, the per-request `Trace Id` (32 hex; my two requests returned `26ad…` and `e3d6…`, and the
committed capture carries a third value `f97e…`). That is exactly the quirk the manifest declares, and the manifest
never quotes L2 (`Trace Id` appears in 0 of 8 quotes; no assertion carries an `anchor`).

Consequence for reading: the route text I verify below is not merely self-consistent with a
lane file — the lane file is byte-equal to the live page apart from a per-request identifier.
This is stronger than `source-recheck.py`, which binds bytes and says nothing about upstream
(Q7's limit); it is still one instant, one host, one UA (see §9).

## 3. Manifest route assertions, each located in the fresh capture

`python3 final.py` (normalizes pinned capture, fresh, fresh2; counts occurrences; checks the
quote lies wholly inside its stated anchor line):

```
normalization=markup-whitespace (source-recheck.py normalize(): </?u> stripped, whitespace collapsed)
assertion anchor cap fresh fresh2 words wording
Q1 L31 1 1 1 10 equal
Q2 L32 1 1 1 19 equal
Q3 L33 1 1 1 6 equal
Q4 L34 1 1 1 14 equal
Q5 L35 1 1 1 11 equal
Q6 L35 1 1 1 11 equal
Q7 L35 1 1 1 9 equal
Q8 L35 1 1 1 11 equal
```

Route-bearing assertions (Q1–Q4) with their verdicts:

| id | anchor | quote (verbatim; ≤25 words) | occurrences pinned/fresh/fresh2 | wording | verdict |
|---|---|---|---|---|---|
| Q1 | L31 | "MSVR learns about vulnerabilities in third-party products in three ways" | 1/1/1 | equal | **agree** — the enumeration sentence heads the route list, as the manifest's `location` says |
| Q2 | L32 | "These vulnerabilities are reported to the MSVR team, which then works with the affected vendor to fix the issue." | 1/1/1 | equal | **agree** — route 1 = internal Microsoft engineers; the recipient is the affected vendor ("works with") |
| Q3 | L33 | "These issues are coordinated by MSVR." | 1/1/1 | equal | **agree** — route 2 (external report to MSRC); MSVR is the stated handler, no vendor named |
| Q4 | L34 | "Any issues are reported to the affected vendor under accepted Coordinated Vulnerability Disclosure practices." | 1/1/1 | equal | **agree** — route 3 = internal research; the recipient is the affected vendor ("reported to") |

Role assertions (Q5–Q8, all L35) also AGREE, exactly once, wording equal: role 1 "as a vendor
affected by vulnerabilities in its products and services" (11 words), role 2 "as a finder of
new vulnerabilities in third-party products and services" (11), role 3 "as a coordinator of
vulnerabilities that affect multiple vendors" (9), and the framing "This coordination takes
place under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach." (11). Role order
in the manifest (role 1 vendor, role 2 finder, role 3 coordinator) matches L35's order.

Route-block containment: the only lines in the fresh capture matching
`third-party|vendor|coordinat` (case-insensitive) are **L31–L35** — the nav (L3–L27), the
programme object L29 and the footer (L36–L97) carry no route statement. So no route assertion
can be satisfied by page chrome, and no fourth route statement exists elsewhere on the page.

Lane instrument agreement, run on the pinned bytes:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048
S048:sha256 OK
S048:Q1 OK occurrences=1
... Q2..Q8 OK occurrences=1
recheck_exit=0
```

## 4. Entry quote spans the manifest does not assert

The entry uses 13 source-quote spans — 7 `>` blockquotes plus 6 quoted table cells; 8 are
manifest assertions. The other 5 are route-bearing
or framing, and all 5 are exactly-once in the pinned capture **and** in both fresh fetches
(hand-measured here, since no assertion covers them):

```
E1 L29 programme L29 1 1 1 23 equal
E2 L32 label     L32 1 1 1  3 equal
E3 L33 label     L33 1 1 1  9 equal
E4 L34 label     L34 1 1 1  3 equal
E5 L34 scope     L34 1 1 1 14 equal
```

All within Q3's ≤25-word bound; longest is E1/L29 at 23 words. So every substantive route
quote in the entry is verbatim and locatable — the only gap is that 5 of the 13 are not
instrument-bound (§6 F1).

## 5. Entry sentences about the routes, sentence by sentence

Verdicts: AGREE / AGREE-with-qualification / DISAGREE-as-worded. Every number below was
recounted on my fresh text, not copied from the entry.

| # | entry sentence (shortened) | supporting words | verdict |
|---|---|---|---|
| S1 | Claim 1 heading: "states three intake routes for third-party-product vulnerabilities" | Q1/L31 ("in three ways", `grep -c 'in three ways'` = 1) | **agree** |
| S2 | table: three route labels and three handling quotes | E2–E4, Q2–Q4 at L32/L33/L34, all exactly once | **agree** |
| S3 | "Microsoft names a recipient for two of them" | `grep -c 'affected vendor'` = 2, at L32 and L34; L33 names no affected vendor | **agree** |
| S4 | "Route 3 is scoped by Microsoft to non-Microsoft products" | E5/L34: "products that run on Microsoft operating systems, but that are not developed by Microsoft" | **agree-with-correction** — the paraphrase drops the OS conjunct and so reads wider than the page; the quote on the next line restores it (F3) |
| S5 | "an external report filed against a Microsoft product that the reporter believes also affects a third-party product (or affects both)" | L33: "an issue that they believe affects a Microsoft product but that either affects a third-party product of affects both" (sic) | **agree** — disjunction preserved by the parenthetical; but "believes" is placed over the third-party effect, which L33 states as fact, not as belief (nit, F6) |
| S6 | Claim 2: three roles in one sentence, third = coordinator across vendors | Q5–Q8, all L35, each exactly once | **agree** |
| S7 | "The three roles are one vendor's three seats, not three parties" | L35: "how Microsoft responds as a vendor affected by vulnerabilities in its products and services" (14 words, then "as a finder", "and as a coordinator") | **agree** |
| S8 | §1: "A standing internal-research route into other vendors' products" | L34 leads "As time and resources permit", then states the research on "products that run on Microsoft operating systems, but that are not developed by Microsoft" | **agree-with-qualification** — existence of the route is stated; its cadence is resource-gated and the entry never quotes that gate (F5) |
| S9 | §2: "The vendor stated as coordinator itself" | Q7/L35 | **agree** |
| S10 | §3: "a vendor's standing statement about its routes into *other* vendors' products" | L31–L34 (four `third-party` occurrences, all inside L31–L34) | **agree** |
| S11 | FC-1: 3 labelled routes, `in three ways` = 1, `only` = 0 | fresh: 3 / 1 / 0 | **agree** |
| S12 | FC-2: coordinator sentence stated once | fresh: 1 | **agree** |
| S13 | FC-3: no clock, no address | fresh: `90[ -]day\|deadline\|embargo\|timeline` = 0, `@microsoft` = 0 | **agree** |
| S14 | FC-4: no payment term in the programme body; 1 bounty in chrome at L15 | fresh: `sed -n '28,35p' \| grep -ci bounty` = 0; whole file = 1; L15 = "Microsoft Bug Bounty Programs" | **agree** |
| S15 | FC-5 first clause: `affected vendor` = 2 (L32, L34); "L33 names only MSVR" | L33 names MSRC, "an external researcher", "external parties", and MSVR | **DISAGREE-as-worded** (F2) — the operative point (no affected vendor on route 2) is true |
| S16 | Honest limit: no agreement, timeline, address or per-vendor process | S13 counts; `http` = 0 | **agree** |
| S17 | "navigation chrome is L3-L27 and the footer L36-L97" | 97 lines; L28 heading, L35 last role line, L36 "Surface Laptop Ultra", L97 "About our ads" | **agree** |
| S18 | L33 carries a source typo "third-party product of affects both" (sic), no quote repeats it | typo count = 1 in fresh; 0 of 8 manifest quotes contain `of affects` | **agree** |
| S19 | L30 curly apostrophe, L35 ASCII (per the manifest note) | L30 contains U+2019; L35 contains U+0027 | **agree** |
| S20 | F06 "has no row for a vendor occupying the finder and coordinator seats itself" | F06 L25: coordinator "Optional participant that can assist vendors and finders"; L28 finder addressed as a separate party | **agree** |
| S21 | F11 "assigns no finder or coordinator seat to a vendor" | `grep -iE 'finder\|coordinator'` on that entry → no match | **agree** |

## 6. Findings, by severity

No high and no medium finding. Five low items (F1–F5) plus two nits (F6–F7); F1 is the only
one on the verifiability axis, the rest are wording precision. All fixes land outside my write scope —
reported for the L1 to route.

**F1 (low, verifiability) — the recheck note claims more instrument coverage than the manifest
has.** `corpus/knowledge/vendor-third-party-finding-coordination.md:4` ends the `recheck:` line
with `# 8 assertions, every quote exactly-once in the pinned capture`. The entry carries 13
source-quote spans (7 `>` blockquotes plus 6 quoted table cells); 5 (E1–E5: L29, the three
route labels, the L34 scope line) are not assertions. Measured by hand in §4, the sentence is **true today** on both the pin and the live
page — but it is not bound by the instrument, so a later edit that retypes one of those five
would pass `source-recheck --source S048` unchanged. Remediation (either): add five
`quotes` entries to `corpus/source-snapshots/round-31/manifest.json` (all five are ≥12 chars,
so they clear `MIN_QUOTE_CHARS`, and all are exactly-once), so the record asserts all 13 spans
and the note's count becomes 13; or narrow the note to "8 assertions (Q1-Q8); the three route
labels and the L34 scope line are hand-measured exactly-once". Extending the record does not
touch the capture, so the `2001ad77…` pin stands; the cheaper edit is the note.

**F2 (low, precision) — FC-5 asserts something false about L33.** Same file, FC-5: "L33 names
only MSVR." L33 names "the Microsoft Security Response Center (MSRC)", "an external
researcher", "the Microsoft product", "external parties" and MSVR. The claim the entry needs
is narrower and true: route 2 names no affected-vendor recipient (`affected vendor` occurs
twice, L32 and L34 only). Suggested same-line suffix: "L33 names no affected vendor; MSVR is
its only stated handler." (Append, do not reflow — R6 keeps line anchors.)

**F3 (low, precision) — route 3's scope is stated wider than the page.** Claim 1: "Route 3 is
scoped by Microsoft to non-Microsoft products". L34 scopes it to "products that run on
Microsoft operating systems, but that are not developed by Microsoft" — the OS conjunct is
dropped. The verbatim quote immediately below restores it, so the entry cannot be read as
claiming MSVR researches arbitrary third-party products; still, a downstream package citing
the sentence alone would overstate. Suggested same-line suffix: "(scoped to products that run
on Microsoft operating systems — see the quote)".

**F4 (low, precision) — the Cisco contrast is worded stronger than S040.** §2 says Cisco's
stated handling is to "route the multi-vendor report out to an external centre", and the
"What this adds" preamble says Cisco "hands a report that 'may impact multiple vendors' to
CERT/CC, CERT-FI, JP-CERT or NPSA". The cited bytes say Cisco "works with third-party
coordination centers such as ... to manage a coordinated industry disclosure"
(`corpus/source-snapshots/round-25/S040.txt:185-187`) and that Cisco "will either assist the
incident reporter with contacting the coordination center or do so on the incident
reporter<U+FFFD>s behalf" (`S040.txt:192-193`; the replacement character is in the capture —
see §8). `hands ... to` implies transfer where the page says
co-management; the page's list is `such as A, B, C, and D` (exemplars) where the entry writes
`CERT/CC, CERT-FI, JP-CERT or NPSA`. The F15 contrast survives either way — the centre is external in both
readings — so this is a wording fix, not a claim fix.

**F5 (low, precision) — "standing" is not quoted with its gate.** §1 heading "A standing
internal-research route" and the text "Route 3 is a programme activity"; L34 opens "As time
and resources permit". Existence is supported; cadence is explicitly conditional, and the
entry emphasises the standing character without showing the condition. Either quote the gate
or say "a programme route Microsoft states it runs as time and resources permit".

**F6 (nit, precision) — whose belief covers the third-party effect.** Claim 1's "an external
report ... that the reporter believes also affects a third-party product" puts the third-party
effect inside the reporter's belief. L33 puts it outside: "an issue that they believe affects
a Microsoft product but that either affects a third-party product of affects both"
(source typo "of" for "or", sic)
(typo in source, sic). The parenthetical "(or affects both)" already carries the disjunction;
the word "believes" simply sits one clause too far left.

**F7 (nit, documentation) — manifest `location` shorthand for Q3** reads "external researcher
reports to the MSRC that affect a third-party product or both parties", dropping the page's
"they believe affects a Microsoft product" precondition. `location` is documentation the
instrument does not read (Q9), so nothing is mis-verified; it is noted so a later reader does
not take it as the page's sentence.

Also recorded, not a defect: the entry's `source:` line says "the programme description L29"
while the registry row says `purpose L29-L30`; both lines are inside the entry's declared
`28-35` span, so no anchor is wrong.

## 7. Numbers reproduced (nothing retyped from memory)

On the pinned capture **and** on both fresh fetches, identical:

```
affected vendor: 2      in three ways: 1     only(ci): 0
coordinator-of-vulns: 1 clock(ciE): 0        @microsoft: 0
http: 0                 bounty(ci) all: 1    bounty 28-35: 0
labelled routes: 3      CERT/CC: 0           JPCERT: 0        IPA: 0
cert(ci): 1             third-party: 4       vendor: 3        coord: 3
```

`cert`'s single match is the footer line "Certified Refurbished" at L48, as the entry says.
No date-like string exists on the page at all (`grep -nE '(19|20)[0-9]{2}|January|...'` → no
match; `grep -niE 'updated|published|last modified|revision|revis'` → no match), which supports
the registry row's "page shows no visible publication or revision date" more strongly than the
row states.

The entry's negative sweep reproduces exactly as written (four terms, only this entry):

```
$ for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities'; do grep -rli -- "$t" corpus/knowledge/*.md; done
corpus/knowledge/vendor-third-party-finding-coordination.md   (for each of the four terms)
```

The `recheck:` line is Q10-conforming and runs from the lane root: `sed -n 's/^recheck: //p'`
piped to `bash -n` → `bash_n_ok`; the command itself exits 0 with `occurrences=1` on Q1–Q8.
`--source S048` matches the entry's `source:` id and the manifest lists S048 (R12).

## 8. Adjacent observation, outside the F15 assertions

`corpus/source-snapshots/round-25/S040.txt` (the Cisco capture F15's contrast leans on) is not
clean UTF-8 text: 7 U+FFFD replacement characters, one of them at L193 in
"reporter<U+FFFD>s behalf". Consequence: that line cannot be quoted verbatim in a markdown
entry with an ASCII or curly apostrophe and still match the pin — a future quote of L192-193
must either carry the replacement character or stop before it. Not an F15 defect and not my
item's scope; worth a lane note because F4's remediation touches that sentence.

## 9. Residual risk and verification gaps

- **One instant, one host, one UA.** The live agreement in §2 covers 2026-10-25T23:29:53Z
  (capture) and my two GETs at 2026-10-26T00:24Z/00:26:38Z, from this host, with the
  instrument UA. Geo/locale variants, a mobile path, and any later edit to the page are
  unmeasured. This is not currency evidence.
- **Converter-relative equality.** Byte equality in §2 holds for text produced by
  `capture-source.py`'s `html_to_text()`. Since the pinned capture was produced by the same
  converter, equality is meaningful for what the lane stores; a converter change would move
  both sides, and I did not test a different extraction (e.g. a DOM parse) for text the
  converter drops.
- **Route sentences verified by hand.** E1–E5 (§4) are exactly-once as measured today but
  unasserted, so this receipt's guarantee for them ends when the manifest changes (F1).
- **Cross-entry contrast checked at the cited lines only.** I re-opened S039.txt:506 (Hitachi
  reporting to the 早期警戒パートナーシップ 届出窓口 when impact leaves Hitachi-group products),
  S040.txt:185-193, F06's coordinator definition and F11's seat vocabulary — enough to confirm
  the contrast sentences are not fabricated, not a re-review of those entries.
- **Independent corroboration, not a substitute.** Seat `ScoutLiveDrift` fetched the same URL
  in the same minute and reported the same `bytes=81802` / 3755 B / 97 lines, with the same
  one-line Trace Id difference. Two seats, two scratch trees, separate conversions, same
  conclusion; the quote-level work above is mine and is what this receipt rests on.
