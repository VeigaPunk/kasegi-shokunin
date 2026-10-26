# A vendor's research programme as an intake route for other vendors' bugs
source: S048 — https://www.microsoft.com/en-us/msrc/msvr — section "Microsoft Security Vulnerability Research (MSVR)", capture corpus/source-snapshots/round-31/S048.txt:28-35 — the programme description L29, the three-route intake sentence L31, the three routes L32-L34, the three-role sentence L35
verified-at: 2026-10-25
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048   # 8 assertions, every quote exactly-once in the pinned capture; a captured-source comparison, not a fresh network verification
ground: F15 — a vendor's research programme as an intake route for other vendors' bugs

## Attribution

Every statement below is Microsoft's own description of its own programme, published on
its MSRC site: a first-party self-description of published programme text, not an audit
finding, and not a rule about vendors in general. One page, one vendor. Microsoft's MSVR
states its own object:

> MSVR is a program specifically designed to help improve the security ecosystem as a whole through the sharing of knowledge and best practices.
> — L29

## Claim 1 — Microsoft's MSVR states three intake routes for third-party-product vulnerabilities

> MSVR learns about vulnerabilities in third-party products in three ways:
> — L31

The three labelled routes follow, one per capture line:

| Route label (its capture line) | Microsoft's stated handling of the finding | Capture |
|---|---|---|
| "Internal Microsoft engineers" (L32) | "These vulnerabilities are reported to the MSVR team, which then works with the affected vendor to fix the issue." | L32 |
| "External reports to the Microsoft Security Response Center (MSRC)" (L33) | "These issues are coordinated by MSVR." | L33 |
| "Internal research projects" (L34) | "Any issues are reported to the affected vendor under accepted Coordinated Vulnerability Disclosure practices." | L34 |

Route 3 is scoped by Microsoft to non-Microsoft products:

> products that run on Microsoft operating systems, but that are not developed by Microsoft
> — L34

So the three routes are three different arrivals — a Microsoft engineer's ordinary work, an
external report filed against a Microsoft product that the reporter believes also affects a
third-party product (or affects both), and Microsoft's own research — and Microsoft names a
recipient for two of them: route 1 works with the affected vendor and route 3 reports to the
affected vendor, while route 2 says only that MSVR coordinates the issue.

## Claim 2 — Microsoft's MSVR states three roles for itself in one sentence, the third being coordinator across vendors

> This coordination takes place under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach.
> — L35

The same sentence names the roles:

> as a vendor affected by vulnerabilities in its products and services
> — role 1, L35

> as a finder of new vulnerabilities in third-party products and services
> — role 2, L35

> as a coordinator of vulnerabilities that affect multiple vendors
> — role 3, L35

The three roles are one vendor's three seats, not three parties. Microsoft describes itself
as affected vendor, as finder and as coordinator in the same sentence, and places the
third-party coordination under its own CVD approach (L35).

## What this adds beyond F06 and F10

F06 (`knowledge/multiparty-vulnerability-coordination.md`, S018 FIRST v1.1) holds the role
vocabulary, and in it the coordinator is a participant *outside* the vendor — its worksheet
asks a package to record whether a coordinator exists rather than to assume one. F06 has no
row for a vendor occupying the finder and coordinator seats itself. F10's vendor rows both
keep coordination outside the vendor: Hitachi reports an issue that spills beyond
Hitachi-group products to the partnership's 届出窓口 (S039.txt:506, quoted in
`knowledge/vendor-disclosure-policies-as-corpus-objects.md` Claim 7), and Cisco hands a
report that "may impact multiple vendors" to CERT/CC, CERT-FI, JP-CERT or NPSA
(S040.txt:185-193, the `cisco-jpcert-partner` row of
`knowledge/vendor-disclosure-policy-commitments-crosswalk.md`).

Against that ground, S048 adds three things the lane did not hold:

1. **A standing internal-research route into other vendors' products.** Route 3 is a
   programme activity aimed at products "that are not developed by Microsoft" (L34), not a
   by-product of the vendor's own product QA — which is the shape Hitachi describes
   (S039.txt:506).
2. **The vendor stated as coordinator itself.** Microsoft names itself "as a coordinator of
   vulnerabilities that affect multiple vendors" (L35), where Cisco's stated handling is to
   route the multi-vendor report out to an external centre (S040.txt:185-193) and Hitachi's
   is to file it with the national partnership (S039.txt:506).
3. **A published programme about *other vendors'* products as a corpus object.** F10's
   thesis is a vendor's standing statement about the handling of findings in its *own*
   products; S048 is a vendor's standing statement about its routes into *other* vendors'
   products.

F11 (`knowledge/iso-29147-and-30111-division-of-labour.md`, S041) holds the
outward-disclosure / inward-handling division of labour and assigns no finder or coordinator
seat to a vendor, so it carries none of the three additions.

The negative sweep behind that claim, runnable from the lane root on the landed tree:

```
for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities'; do grep -rli -- "$t" corpus/knowledge/*.md; done
```

prints only `corpus/knowledge/vendor-third-party-finding-coordination.md` for all four terms
— so the residual is held by this entry and by no earlier knowledge file.

## Honest limit

The page states intake routes and roles. It does not state the coordination agreements, a
timeline, a reporting address or a per-vendor process: measured on the pinned capture,
`grep -ciE '90[ -]day|deadline|embargo|timeline'` → `0`, `grep -ci '@microsoft'` → `0` and
`grep -ci 'http'` → `0`. Nothing in this capture establishes what Microsoft agrees with an
affected vendor, and nothing establishes that the affected vendor was told, or when.

The capture is also page-level: the navigation chrome is L3-L27 and the footer L36-L97, both
outside the quoted block; L2 carries a per-request `Trace Id` and is never quoted; and L33
carries a source typo ("third-party product of affects both", sic) that no quote repeats.

## Falsifiable checks

Run from the lane root; each prints the count stated here, so a reader can refute any claim
above from the capture alone.

- **FC-1 — the page enumerates three labelled routes.** `grep -cE '^(Internal Microsoft engineers|External reports to the Microsoft Security Response Center \(MSRC\)|Internal research projects):' corpus/source-snapshots/round-31/S048.txt` → `3`, and `grep -c 'in three ways' corpus/source-snapshots/round-31/S048.txt` → `1`, `grep -ci 'only' corpus/source-snapshots/round-31/S048.txt` → `0`. Three labelled lines prove an enumeration, not a closure: the page states three ways and claims no exclusivity. A package claiming a fourth MSVR intake route is unsupported by this capture — not excluded by the page.
- **FC-2 — the coordinator seat is Microsoft's own, stated once.** `grep -c 'as a coordinator of vulnerabilities that affect multiple vendors' corpus/source-snapshots/round-31/S048.txt` → `1`. A package reading the coordinator as an external centre is reading a role the page does not assign.
- **FC-3 — no clock and no channel on the page.** `grep -ciE '90[ -]day|deadline|embargo|timeline' corpus/source-snapshots/round-31/S048.txt` → `0`; `grep -ci '@microsoft' corpus/source-snapshots/round-31/S048.txt` → `0`. Any "MSVR's N-day embargo" or "report it to MSVR at ⟨address⟩" line cannot be supported from S048.
- **FC-4 — the programme body carries no payment term.** `sed -n '28,35p' corpus/source-snapshots/round-31/S048.txt | grep -ci bounty` → `0`, while `grep -ci bounty corpus/source-snapshots/round-31/S048.txt` → `1` (the navigation item "Microsoft Bug Bounty Programs" at L15). A package equating MSVR with the bounty programme is citing page chrome.
- **FC-5 — two of the three routes name the affected vendor; route 2 names no recipient.** `grep -c 'affected vendor' corpus/source-snapshots/round-31/S048.txt` → `2` (L32 and L34); L33 names only MSVR. A package claiming MSVR remediates a third-party product itself, rather than working with or reporting to the affected vendor, is unsupported; a package claiming route 2 hands the issue to the affected vendor is also unsupported, because the page does not say so.

## Rejected over-generalizations

1. **"Every large vendor runs such a programme."** Rejected. This is one page stating one
   vendor's programme, and the page makes no claim about any other vendor's programmes. The
   lane's other vendor captures describe handling policies and routing to external centres
   (S039.txt:506; S040.txt:185-193), so the capture set supports no frequency claim.
2. **"A third-party finding sent to a vendor's response centre bypasses the affected
   vendor."** Rejected. Route 1 has the MSVR team working "with the affected vendor to fix
   the issue" (L32) and route 3 has issues "reported to the affected vendor" (L34);
   Microsoft's stated coordination ends at the affected vendor, not instead of it.
3. **"MSVR is a bug bounty programme."** Rejected. The programme body (L28-L35) carries no
   payment term (FC-4); the only bounty wording in the capture is the navigation link
   "Microsoft Bug Bounty Programs" (L15), which points at a different page.
4. **"The page imposes a coordinated-disclosure obligation on finders."** Rejected. The
   capture states Microsoft's own roles and routes and a CVD framing (L35); it states no
   obligation, no deadline and no address (FC-3). The staged package entry's sentence that
   "the finder also has a coordinated-disclosure obligation" is an inference these bytes do
   not carry, and is not adopted here.
5. **"A vendor that coordinates third-party findings replaces the external coordinator."**
   Rejected. F06's coordinator is an optional participant outside the vendor, and S048 names
   no external centre at all (`grep -c 'CERT/CC'` → `0`, `grep -c 'JPCERT'` → `0`,
   `grep -c 'IPA'` → `0`; the capture's only `cert` match is the footer line
   "Certified Refurbished" at L48); the self-coordinating shape and the route-out shape are
   distinct, and a package must record which party coordinates rather than assume either.

## Scope and limits

- One page, one vendor, read as the pinned capture of 2026-10-25T23:29:53Z: 3755 B, 97 lines,
  sha256 `2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55`. Page-level
  evidence only; it carries no per-vendor process, contact or timeline.
- The recheck verifies the pin and the exactly-once presence of eight quotes under
  `source-recheck.py`'s declared normalization (capture markup stripped, whitespace
  collapsed). It does not verify that the upstream page still serves this text.
- Documentation only: this entry records published programme text. It instructs no probing,
  scanning, login or submission against any target, and carries no credential material,
  session or private URL.
