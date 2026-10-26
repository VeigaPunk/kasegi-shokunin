# RevQuoteRoles — quote re-open of S048's roles and coordination statements (round 31, wave 2)

Seat: RevQuoteRoles (leaf; no subagent, no background job, no swarm).
Scope exercised: read-only over the lane; the only file written is this receipt.
Read-only git: lane HEAD at start `eecad59` (`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse --short HEAD`;
no git/jj mutation run, no lane scratch tree created inside the repo).
Answering model: `opencode-go/deepseek-v4.1-flash` (config route table decided; no model parameter passed; this is the
model line the session reports, not a router observation).
Tooling: nothing installed or upgraded (no package manager run; scratch is `mktemp -d` only).
Scratch: `/tmp/revquoteroles.in5l5g` (fresh capture + extracted recheck line), deleted at §8.

Subject of this seat: (a) re-fetch `https://www.microsoft.com/en-us/msrc/msvr` and verify every assertion in
`corpus/source-snapshots/round-31/manifest.json` that concerns Microsoft's roles (affected vendor / finder /
coordinator) and how third-party findings are coordinated — fresh-fetch location, capture line, occurrences,
equality; (b) sentence-level attribution and backing audit of
`corpus/knowledge/vendor-third-party-finding-coordination.md` on those topics.

Verdict summary: **8/8 manifest assertions PASS** (equality, exactly-once, declared line, on the fresh fetch);
**0 HIGH, 2 MEDIUM, 12 LOW** findings in the entry; every finding is wording/precision, none is a misattribution of
a vendor rule to "vendors in general" and none is a claim without a locatable quote.

---

## 1. Fresh fetch (instrument UA, named URL only)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ S=$(mktemp -d /tmp/revquoteroles.XXXXXX); mkdir -p "$S/corpus"
$ python3 corpus/instruments/capture-source.py --id S048 \
    --url https://www.microsoft.com/en-us/msrc/msvr --kind html --out "$S/S048-fresh.txt"
S048 status=200 fetched_bytes=81802 snapshot_bytes=3755 sha256=e44602388b2896643d8c164e662b318f963c80248a07493f13e18940db4603af utc=2026-10-26T00:24:07Z out=/tmp/revquoteroles.in5l5g/S048-fresh.txt
capture_exit=0
$ sha256sum "$S/S048-fresh.txt"; wc -lc "$S/S048-fresh.txt"
e44602388b2896643d8c164e662b318f963c80248a07493f13e18940db4603af  /tmp/revquoteroles.in5l5g/S048-fresh.txt
  97 3755 /tmp/revquoteroles.in5l5g/S048-fresh.txt
```

Fresh-fetch location: `/tmp/revquoteroles.in5l5g/S048-fresh.txt` (scratch; 97 lines, 3755 B, sha256 `e4460238…`).
Comparison against the committed pin (`corpus/source-snapshots/round-31/S048.txt`, sha256 `2001ad77…`):

```
$ diff corpus/source-snapshots/round-31/S048.txt /tmp/revquoteroles.in5l5g/S048-fresh.txt
2c2
< This is the Trace Id: f97e6b1cb578f714d23850f80f018bb3
---
> This is the Trace Id: 58be723db4dabdbee9179d430e1c0665
diff_exit=1
$ python3 - <<'PY'   # byte comparison, line arrays
pinned_lines 98 fresh_lines 98        # 97 lines + trailing newline in both
diff_lines [2]
equal_after_masking_L2 True
quoted_block_L28_35_equal True
PY
```

So the page still serves the same text except the per-request `Trace Id` on L2 — exactly the quirk the manifest
`purpose` declares ("snapshot line 2 … is a per-request identifier and is never quoted"), now **measured** on a
second fetch rather than restated. Every assertion below therefore has a fresh-fetch equality verdict, not only a
local-pin verdict.

## 2. Assertion-by-assertion verdicts — 8/8 PASS

Method: each manifest `quote` was measured with `source-recheck.py`'s own `normalize()` (markup stripped,
whitespace collapsed) and also raw, on **both** the pinned capture and the fresh fetch; its first containing line
was computed in both; the declared `location` line was compared to that line; word count checked against Q3's 25.
Probe (one pass, `normalize()` imported from the instrument):

```
manifest id: S048 path: S048.txt sha_pin: 2001ad7732a1 quotes: 8
Q1  words=10 pinned_raw_occ=1 pinned_norm_occ=1 line=31 fresh_raw_occ=1 fresh_norm_occ=1 fresh_line=31
Q2  words=19 pinned_raw_occ=1 pinned_norm_occ=1 line=32 fresh_raw_occ=1 fresh_norm_occ=1 fresh_line=32
Q3  words= 6 pinned_raw_occ=1 pinned_norm_occ=1 line=33 fresh_raw_occ=1 fresh_norm_occ=1 fresh_line=33
Q4  words=14 pinned_raw_occ=1 pinned_norm_occ=1 line=34 fresh_raw_occ=1 fresh_norm_occ=1 fresh_line=34
Q5  words=11 pinned_raw_occ=1 pinned_norm_occ=1 line=35 fresh_raw_occ=1 fresh_norm_occ=1 fresh_line=35
Q6  words=11 pinned_raw_occ=1 pinned_norm_occ=1 line=35 fresh_raw_occ=1 fresh_norm_occ=1 fresh_line=35
Q7  words= 9 pinned_raw_occ=1 pinned_norm_occ=1 line=35 fresh_raw_occ=1 fresh_norm_occ=1 fresh_line=35
Q8  words=11 pinned_raw_occ=1 pinned_norm_occ=1 line=35 fresh_raw_occ=1 fresh_norm_occ=1 fresh_line=35
```

| id | topic this assertion binds | declared line | measured line (pinned / fresh) | occ raw/norm (pinned / fresh) | words | equality | verdict |
|---|---|---|---|---|---|---|---|
| Q1 | three-route intake sentence | L31 | 31 / 31 | 1/1 / 1/1 | 10 | byte-exact substring | PASS |
| Q2 | route 1: MSVR works with the affected vendor | L32 | 32 / 32 | 1/1 / 1/1 | 19 | byte-exact | PASS |
| Q3 | route 2: third-party findings coordinated by MSVR | L33 | 33 / 33 | 1/1 / 1/1 | 6 | byte-exact | PASS |
| Q4 | route 3: issues reported to the affected vendor | L34 | 34 / 34 | 1/1 / 1/1 | 14 | byte-exact | PASS |
| Q5 | role 1: vendor affected in its own products/services | L35 | 35 / 35 | 1/1 / 1/1 | 11 | byte-exact | PASS |
| Q6 | role 2: finder in third-party products/services | L35 | 35 / 35 | 1/1 / 1/1 | 11 | byte-exact | PASS |
| Q7 | role 3: coordinator across multiple vendors | L35 | 35 / 35 | 1/1 / 1/1 | 9 | byte-exact | PASS |
| Q8 | CVD framing sentence introducing the roles | L35 | 35 / 35 | 1/1 / 1/1 | 11 | byte-exact | PASS |

Every assertion is also structurally valid against Q9: `path` stem `S048` equals its `id`, no assertion carries an
`anchor` (none needs one — each is exactly-once), and no quote is under the 12-character evidence floor.

```
$ python3 -c "..."      # manifest structure
top keys: ['schema_version', 'purpose', 'sources']
source keys: ['id', 'path', 'sha256', 'quotes']
quote keys: ['id', 'location', 'quote']          # no 'anchor' key anywhere
n_quotes: 8
sources: ['S048']
path stem==id: True
```

Manifest `location` prose was checked against the capture independently (the instrument does not read `location`):
Q1 "heads the list of routes (routes follow on L32-L34)" ✓; Q2 "route 1, internal Microsoft engineers" ✓;
Q3 "route 2, external researcher reports to the MSRC" and "the statement that third-party findings are coordinated
by MSVR" ✓; Q4 "route 3, Microsoft's own research projects on non-Microsoft products" ✓; Q5-Q7 roles 1-3 ✓;
Q8's typography note is exact:

```
$ grep -c "Microsoft’s goal" corpus/source-snapshots/round-31/S048.txt          # L30 curly apostrophe
1
$ grep -c "Microsoft's Coordinated Vulnerability Disclosure" .../S048.txt      # L35 ASCII apostrophe
1
```

## 3. Instrument runs on the landed bytes (read-only)

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

Foreign-cwd replay of the entry's own `recheck:` line (Q10: `cd` prefix, `bash -n`-parseable):

```
$ sed -n '4p' corpus/knowledge/vendor-third-party-finding-coordination.md | sed 's/^recheck: //' > /tmp/revquoteroles.in5l5g/recheck.sh
$ bash -n /tmp/revquoteroles.in5l5g/recheck.sh ; echo $?
0
$ cd /tmp && bash /tmp/revquoteroles.in5l5g/recheck.sh
S048:sha256 OK
S048:Q1 OK occurrences=1 … S048:Q8 OK occurrences=1
recheck_from_tmp_exit=0
```

Harness binding of the entry's recheck line (R12), run on the quiescent landed tree:

```
$ python3 corpus/instruments/frontier-recheck-count.py | tail -3
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md  ids=S041,S046,S047 exit=0
PASS     F15  knowledge/vendor-third-party-finding-coordination.md       ids=S048           exit=0
entries=18 pass=18 exit=0
```

Anchor-gate coverage measured, not assumed:

```
$ python3 corpus/instruments/anchorcheck.py corpus/knowledge/vendor-third-party-finding-coordination.md
== corpus/knowledge/vendor-third-party-finding-coordination.md: 0 in-range cite instances, 0 bad; 0 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
anchorcheck_exit=0
```

The `0 distinct anchors` is a **coverage fact, not a pass**: this entry's locations are prose-form
(`(S039.txt:506, quoted in …)`, `capture corpus/source-snapshots/round-31/S048.txt:28-35`), not backticked
`path:NN` tokens, so the anchor gate never sees them. I range-checked the three by hand (§5). This is the same
blind spot round 28 recorded for plain-text `source:` headers.

## 4. The entry's own falsifiable checks, replayed

```
honest limit:  clock: 0 | at_microsoft: 0 | http: 0
FC-1:  labelled-route lines 3 | 'in three ways' 1 | 'only' 0
FC-2:  'as a coordinator of vulnerabilities that affect multiple vendors' 1
FC-4:  bounty in L28-35 0 | bounty in capture 1 (L15)
FC-5:  'affected vendor' 2 | 'affected vendor' on L33 0
rejected-5 greps: CERT/CC 0 | JPCERT 0 | IPA 0 | case-sensitive 'cert' 0   ('cert' -i: 1)
Trace Id 1 | L30 curly 1 | L35 ASCII 1
boundaries: L3 'MSRC' | L27 'Security Researcher Leaderboard' | L36 'Surface Laptop Ultra' | L97 'About our ads'
scope: 3755 B, 97 lines, sha256 2001ad77…  (all match the entry's §Scope)
negative sweep: for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities'
  → corpus/knowledge/vendor-third-party-finding-coordination.md only, for all four terms (exactly as stated)
```

All ten stated **numeric** counts (FC-1's 3/1/0, FC-2's 1, FC-3's 0/0, FC-4's 0/1, FC-5's 2) reproduce exactly. The
two stated claims that do not are FC-5's prose halves, findings L-3 and L-4 below (both wording, not content). The negative sweep reproduces exactly, so the "residual is held by this
entry and no earlier knowledge file" claim stands on the landed tree.

## 5. Cross-references behind the comparison section, verified

| entry claim | check | result |
|---|---|---|
| F06 "holds the role vocabulary … record whether a coordinator exists rather than to assume one" | `sed -n '1,40p' corpus/knowledge/multiparty-vulnerability-coordination.md` | Definition row `Definitions — Coordinator`, consequence "A coordinator is optional; record whether one exists rather than inventing one." ✓ |
| "F06 has no row for a vendor occupying the finder and coordinator seats itself" | F06 table rows (6 located rows) | no row names a vendor as finder/coordinator simultaneously ✓ |
| Hitachi spills beyond Hitachi-group products to the partnership's 届出窓口 at `S039.txt:506` | file is 697 lines; `'届出窓口' in line 506` → True; `'製品開発工程' in line 506` → True | in range and on the stated line ✓ (the same quote is F10 Claim 7, `vendor-disclosure-policies-as-corpus-objects.md:126-132`) |
| Cisco "may impact multiple vendors" at `S040.txt:185-193` and the `cisco-jpcert-partner` row | file is 504 lines; L185 opens "Incidents that may impact other vendors"; L191 carries "may impact multiple vendors"; L193 ends the paragraph; row exists at `vendor-disclosure-policy-commitments-crosswalk.md:49` | in range, row exists ✓ |
| F11 "assigns no finder or coordinator seat to a vendor" | `grep -n 'finder\|coordinator' corpus/knowledge/iso-29147-and-30111-division-of-labour.md` | no match ✓ (absence supports the claim) |

## 6. Findings, by severity

### MEDIUM

**M-1 — `corpus/knowledge/vendor-third-party-finding-coordination.md:107-108`: the Honest limit denies a fact the
entry quotes twice.** The sentence reads "Nothing in this capture establishes what Microsoft agrees with an affected
vendor, and nothing establishes that the affected vendor was told, or when." The capture does establish vendor
notification on routes 1 and 3: L32 "works with the affected vendor to fix the issue" (quoted at entry:26) and L34
"Any issues are reported to the affected vendor" (entry:28), and the entry itself concludes from them at entry:132-134
"Microsoft's stated coordination ends at the affected vendor". Measured: `grep -c 'affected vendor' S048.txt` → 2,
both occurrences on L32/L34; L33 (route 2) has 0. So the negative holds only for **route 2** and for **timing,
agreement terms, address and per-vendor process** — not for "was the affected vendor told" on routes 1/3. The same
over-broad wording appears in the frontier row `corpus/README.md:309` ("read no clock, contact or agreement into an
intake route: the pinned capture states none"), which the L1 may want routed with it. Suggested amendment (L1
routes; this seat does not edit the entry): scope the clause to route 2 and to timing/terms, e.g. "for route 2 the
capture states no recipient and no timing; nowhere does it state an agreement, a deadline or an address."

**M-2 — entry:46 "The same sentence names the roles" points at the wrong sentence.** The block quote at entry:43-44
is sentence 1 of capture L35; the three roles are in sentence 2 of the same line. Measured:

```
L35 sent1: This coordination takes place under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach.
L35 sent2: CVD clarifies how Microsoft responds as a vendor affected by … as a finder … as a coordinator of vulnerabilities that affect multiple vendors.
roles in sent1: False | roles in sent2: True
```

A reader checking the quoted sentence for the roles cannot find them there, which is exactly the Q3/Q9 failure mode
(a location that does not locate). Claim 2's body sentence at entry:57-58 ("Microsoft describes itself … in the same
sentence") is correct because it refers to sent2, and the `source:` header already calls L35 "the three-role
sentence" — so the fix is local: say "line", not "sentence", at :46, or quote sent2 there.

### LOW

**L-1 — entry:9 over-broad attribution frame.** "Every statement below is Microsoft's own description of its own
programme" is false for the entry's own sections below it (the F06/F10/F11 comparison at :61-100, the honest limit,
the FCs, the five rejections), and it contradicts entry:74 ("Against that ground, S048 adds three things the lane did
not hold"). The Q4 direction that matters is intact — no vendor rule is generalized. Fix: "Every quotation below, and
every statement of Microsoft's handling below, is Microsoft's own …".

**L-2 — entry:134 generalizes routes 1/3's recipient to all three routes.** "Microsoft's stated coordination ends at
the affected vendor, not instead of it" is true for L32/L34 and unstated for L33, which the entry itself says at
entry:39 ("route 2 says only that MSVR coordinates the issue") and at FC-5. Measured: L33 contains no "affected
vendor". Fix: "on routes 1 and 3".

**L-3 — entry:123 (FC-5) "L33 names only MSVR" is refutable from L33.** L33 names MSRC in its own route label and
"external parties" in its body:

```
L33 has MSRC: True | external parties: True | affected vendor: False
named-party tokens on L33: ['MSRC', 'MSVR', 'Microsoft']
```

The load-bearing half (`grep -c 'affected vendor'` on L33 → 0) holds, so the conclusion is safe; the wording is not.
Fix: "L33 names MSVR as the handler and MSRC as the receiving centre, and names no affected-vendor recipient."

**L-4 — entry:146-147's `cert` match claim depends on a case-insensitive grep it does not show.** As written the
command family around it is `grep -c`; `grep -c 'cert' S048.txt` → 0, while `grep -ci 'cert'` → 1 and that match is
L48 "Certified Refurbished" (confirmed on L48). Fix: write `grep -ci 'cert'` → `1`, footer L48.

**L-5 — entry:69-70 and :81-82 overstate Cisco's route-out.** "Cisco hands a report that 'may impact multiple
vendors' to CERT/CC, CERT-FI, JP-CERT or NPSA" and "Cisco's stated handling is to route the multi-vendor report out
to an external centre" are stronger than the cited range. S040.txt:185-193 says the PSIRT "works with third-party
coordination centers such as … to manage a coordinated industry disclosure", and "will either assist the incident
reporter with contacting the coordination center or do so on the incident reporter's behalf". That is *works with
the centres and helps the reporter contact them*, not a unilateral hand-off by Cisco. The self-coordinating vs
route-out contrast that F15 rests on survives; the paraphrase should say "works with external coordination centres /
helps the reporter contact them".

**L-6 — the staged-package quote at entry:141 is not a literal substring and carries no location.** The staged
package file (campaign package, read-only, never written by this seat) is
`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md:28-29`
and reads "the \*finder\* also has a coordinated-disclosure obligation". Measured:
`grep -c "the finder also has a coordinated-disclosure obligation"` → 0; with the emphasis markers → 1. The
rejection itself is sound (the MSVR capture states no obligation — FC-3's deadline/embargo greps → 0 and there is
no "obligation" wording in L28-L35), but the quote drops markup and the reference gives no path or id. Fix: keep the
markers or paraphrase, and cite the staged path (or S080) the way the other cross-references are cited.

**L-7 — assertion-set coverage is half the entry's quoted spans, and the two prose statements of "8" do not disclose
it.** entry:4 says "8 assertions, every quote exactly-once in the pinned capture" and entry:155 says "the
exactly-once presence of eight quotes". The entry quotes 16 distinct S048 spans: the 8 assertions plus the L29 object
sentence (entry:14), three route labels (entry:26-28), the route-3 scope fragment (entry:32), "Microsoft Bug Bounty
Programs" (entry:137), "Certified Refurbished" (entry:147) and the L33 sic fragment (entry:112). I measured all 8
unasserted spans on both captures — every one is exactly-once (raw and normalized) at its stated line, so there is
**no live defect**; the gap is that a future edit to any of them passes the entry's own recheck. Fix (L1's routing
call): either add the 8 spans to a superseding manifest, or write "eight of sixteen quoted spans" so a reader knows
which half is machine-bound.

**L-8 — entry:137 "which points at a different page" is not in the capture.** The capture is tag-stripped
(`grep -ci 'http'` → 0), so no link target exists in the bytes; the claim is an inference from the nav label. The
rejection ("MSVR is not a bounty programme") is carried by FC-4 (`bounty` in L28-35 → 0, L15 only), so only the
target clause needs marking as inference.

**L-9 — entry:41 heading attributes the three roles to MSVR specifically.** L35's roles sentence is a statement of
how "CVD clarifies how Microsoft responds …", i.e. Microsoft's CVD-wide description, inside the MSVR section. The
body at entry:57-59 says "Microsoft describes itself", which is the accurate attribution. Low impact; a package
citing "MSVR's three roles" would be asserting more than the sentence says.

**L-10 — entry:35-37 moves the reporter's belief onto the third-party effect.** L33 has the researcher reporting an
issue "that they believe affects a Microsoft product but that either affects a third-party product of affects both"
(sic); the belief is about the Microsoft-product effect, and the third-party effect is stated as fact in an
"either/or" (itself corrupted by the sic the entry records at entry:112). The entry's "believes also affects a
third-party product (or affects both)" shifts what is believed. Fix: "an external report of an issue the reporter
believes affects a Microsoft product but that affects a third-party product, or both".

**L-11 (observed, not a defect in this entry) — the same slide as M-1 in the frontier row.** `corpus/README.md:309`
says "read no clock, contact or agreement into an intake route: the pinned capture states none"; for routes 1 and 3
the capture does state contact with the affected vendor. Report-only: README is outside this seat's write scope.

**L-12 — entry:116-117 overstates what the FC block can refute.** "each prints the count stated here, so a reader
can refute any claim above from the capture alone" — the claims above include the F06/F10/F11 comparison section
(entry:61-91), whose clauses can only be refuted from S039/S040/S018, not from S048. Fix: "any claim about S048
above". (The two FC-5 counts that do not reproduce as stated are L-3 and L-4.)

### What passed clean (so the L1 does not re-open it)

- **No Q4 violation in substance.** Every load-bearing statement about vendor conduct is scoped to Microsoft
  ("Microsoft's stated handling", "Microsoft names", "Microsoft describes itself", "Microsoft's MSVR"), the entry is
  labelled first-party (:9-11), and rejection #1 explicitly kills the frequency claim ("Every large vendor runs such
  a programme"), with rejection #5 killing the substitution rule. I found no sentence that turns Microsoft's
  programme into a rule about vendors in general.
- **No unbacked coordination claim.** Every statement about which party coordinates carries a located quote:
  coordination by MSVR (Q3/L33), vendor engagement (Q2/L32, Q4/L34), Microsoft as self-named coordinator (Q7/L35),
  and the comparison parties via F10's S039/S040 locations verified in §5. The only unlocated reference in the
  entry is L-6's staged-package quote.
- **The manifest is Q8/Q9-compliant**: normalization declared in `purpose`, no anchor on unique quotes, occurrence
  counts printed by the instrument, `path` stem = `id`, pin re-measured on committed bytes.
- **The pin/quirk claim is now proven on a second fetch**, not just asserted.

## 7. Residual risk and verification gaps

- **Fresh fetch ≠ future service.** I prove the page served this text at 2026-10-26T00:24Z (second capture, same
  bytes except L2). Nothing here proves it will serve it tomorrow; the entry's own caveat (entry:155-157) is correct.
- **L2 makes the pin un-refetchable byte-for-byte.** The SHA-256 binds committed bytes only; a future reviewer who
  refetches will always see a different digest. The quirk is declared once (manifest `purpose`), and both the entry
  (:111) and the manifest say L2 is never quoted — measured true here (`Trace Id` count 1, in no quote).
- **Half the quoted spans are outside the machine check** (L-7). My measurement covers them today at the fresh
  fetch; the entry's recheck will not cover them tomorrow. This is the largest verifiability gap I found, and it is a
  coverage gap rather than an error.
- **The anchor gate cannot see this entry's citations** (§3), so the S039/S040 locations rest on my manual range
  check plus their owning entries' checks, not on `anchorcheck.py`.
- **Not verified by this seat (out of scope):** the C2 counts (registry 47→48, frontier 14→15, knowledge-entry count,
  census) and the C1 limb ledger; the S039/S040 captures were read locally, not re-fetched (their URLs are not named
  in this item); the campaign package was read only, with no tool of its own run.
- **No live target contacted.** One GET to the one named public URL, with the mandated UA; no other network call.

## 8. Scratch

```
$ rm -rf /tmp/revquoteroles.in5l5g && test ! -e /tmp/revquoteroles.in5l5g ; echo scratch_deleted_exit=$?
scratch_deleted_exit=0
```

Nothing was written to the lane except this receipt; no git/jj state touched; no tool installed.
