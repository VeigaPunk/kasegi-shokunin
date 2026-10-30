# Zero Day Initiative disclosure policy — an F02 coordinator case

source: S075 — https://www.zerodayinitiative.com/advisories/disclosure_policy/ — corpus/source-snapshots/round-47/S075.txt, policy body lines 20-27, sha256 9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1
verified-at: 2026-10-30
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-47/manifest.json --source S075 # 90d

## Scope and decision rule

This F02 case study records TrendAI ZDI's policy for its third-party broker acquisition-disclosure timeline, not a universal researcher deadline or a vendor's own disclosure policy. TrendAI™ ZDI is the stating party throughout. For a documentation-only package, record the applicable response branch, broker-controlled deadline rule, extension authority, and publication consequence separately. The responsive-vendor branch permits 120 days, but its clock's start event is unstated: receipt of a timely vendor response selects this branch without explicitly identifying the date from which the interval runs (`S075.txt:24`). Keep that start date unknown rather than silently converting it to acquisition, first contact, or acknowledgement.

| Policy branch | Located policy words | Package consequence |
|---|---|---|
| Initial notification | “Simultaneous to the vendor notification, protection filters may be distributed” (`S075.txt:22`) | Record possible customer protection separately from public disclosure. |
| Failed acknowledgement | “within five business days” (`S075.txt:23`) | Record the initial acknowledgement threshold before the second contact attempt. |
| Continued silence | “an additional five business days following the second notification” (`S075.txt:23`) | Preserve the second notification as the stated reference for intermediary escalation. |
| Exhausted contact | “fifteen business days after the initial contact” (`S075.txt:23`) | Record a possible public advisory only after reasonable contact means are exhausted. |
| Responsive vendor | “four months (120 days) to address the vulnerability” (`S075.txt:24`) | Preserve both stated units and leave the unstated clock start unknown. |
| Deadline consequence | “publish a limited advisory including mitigation” (`S075.txt:24`) | Preserve the nonresponse or inadequate explanation condition rather than assuming unconditional publication. |
| Exceptional extension | “granted only in rare circumstances” (`S075.txt:24`) | Record ZDI's sole discretion; an extension is not a vendor entitlement. |
| Faulty patch urgency | “For critical-rated bugs where active exploitation is detected or imminent, the vendor will have 30 days” (`S075.txt:25`) | Apply the 30-day branch only to critical-rated faulty-patch disclosures with this condition. |
| Partial patch protection | “critical- and high-severity vulnerabilities where the original patch does offer some protection and exploitation is not imminent” (`S075.txt:25`); “a disclosure window of 60 days” (`S075.txt:25`) | Preserve both partial protection and no imminent exploitation, not merely severity. |
| Other patch regressions | “a time of 90 days” (`S075.txt:25`) | Keep the residual branch within incomplete or faulty patch disclosures, not all reports. |

The 15-business-day branch is permissive, not an automatic publication promise (`S075.txt:23`). The 120-day branch couples a limited advisory to vendor nonresponse or inability to provide a reasonable explanation at deadline, and leaves extensions to TrendAI ZDI's sole discretion (`S075.txt:24`). These conditions require distinct package fields: a recorded interval alone cannot establish the applicable publication date. For an acquired vulnerability a vendor declines to address, TrendAI ZDI states that suppression will not follow merely from that refusal; it offers coordinated public disclosure with effective workarounds (`S075.txt:26`).

## Overlap and novelty

F02 remains the coordinator-timeline comparison: `corpus/knowledge/coordinated-disclosure-timelines.md:6-17` requires attribution, a clock trigger, publication conditions, and documented exceptions, with unknown dates retained when triggers are absent. F15 remains the vendor third-party intake route: `corpus/knowledge/vendor-third-party-finding-coordination.md:17-39` distinguishes Microsoft's three routes into coordination of other vendors' findings, while `corpus/knowledge/vendor-third-party-finding-coordination.md:41-59` separates its vendor, finder, and coordinator roles. These ZDI clocks and extensions instantiate F02 rather than establish a new general method. ZDI's refusal to suppress an acquired vulnerability merely because its product vendor declines to address it (`S075.txt:26`) is additional policy detail, but this round does not count it as a separate admitted frontier surface. F15 holds Microsoft's intake and roles and explicitly leaves agreements and timelines unstated (`corpus/knowledge/vendor-third-party-finding-coordination.md:114-120`). Applying F02's trigger discipline exposes the missing 120-day start event; applying F15's role discipline prevents treating this broker policy as a vendor's third-party intake programme. This page does not establish a purchase process, legal ownership, an acquisition-based clock, or actual coordination conduct.

## Limits

This entry covers policy page text only, specifically the pinned body at `S075.txt:20-27`. Advisories, reward rules, and the researcher submission page are out of scope; the linked blog's additional details are also not imported. It makes no live-page claim, observation of actual broker conduct, legal conclusion, or authorization to contact or disclose against any target. The capture's website-only official-advisory statement (`S075.txt:27`) is a policy assertion, not proof that any advisory was published. The provenance date identifies this captured-source review; the recheck command compares pinned support and does not establish current network freshness. This is documentation-only analysis, not operational disclosure advice.

## Falsifiable package rule

A researcher can check a proposed package against `S075.txt:23-25`: it must name TrendAI ZDI as policy owner, identify the response or faulty-patch branch, preserve that branch's conditions and units, and mark the 120-day start event unknown unless separately evidenced. Reject the over-generalization that every acquired finding must be published exactly 120 days after acquisition: line 24 neither names acquisition as the clock start nor removes its publication conditions, and lines 23 and 25 supply different conditional intervals. A package claiming a computed date solely from this page fails this rule when the required start event is unstated.

## Located support for branch qualifications

The tiered category is explicitly “vulnerability disclosures resulting from an incomplete or otherwise faulty security patch” (`S075.txt:25`). Its residual branch is “All other reports in this category will be given a time of 90 days.” (`S075.txt:25`), not every ordinary report.

The acquired-finding disposition is stated as “In no cases will an acquired vulnerability be "kept quiet" because a product vendor does not wish to address it.” (`S075.txt:26`). This is ZDI's policy assertion, not evidence of actual conduct and not new frontier credit.
