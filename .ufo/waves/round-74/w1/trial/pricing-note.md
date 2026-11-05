# Pricing note — CVE-2023-38545 through the lane's held severity ground (F13/F17/F18)

Trial: round-74 w1 ExecTrial (SHONEN box 2; considerthese/2026-10-26.md proposal 2;
routed defect R73-V5). Subject finding: libcurl SOCKS5 heap buffer overflow, whose
advisory records "Severity: High" (trial evidence/disclosure-capture.txt L101,
sha256 327bc909…b238b) and a platform-side "Bug bounty: 4660 USD" (L108). This note
places that finding against each held entry's own criteria; every tier statement
quotes the line it was read from.

## F13 — corpus/knowledge/program-severity-ladders-and-reward-scales.md

- Entry l.12 separates the three vocabularies this package spans: "Severity
  labels, program policy, and monetary reward are related but not interchangeable."
  The advisory's High label, the program policy's no-bounty rule
  (policy-capture.txt L43) and the 4660 USD reward record are exactly those three
  separate vocabularies.
- Ladder tier: the advisory's own "Severity: High" (advisory L101) is
  label-identical to the VRT's second tier "| P2 | High |" (entry l.27), on
  Bugcrowd's "suggested baseline technical severity of the vulnerability on a
  P1 (Critical) to P5 (Informational) scale" (entry l.22). This is a label-level
  alignment, not a VRT classification of the finding: the entry's own override —
  "application complexity, bounty brief restrictions or unusual impact could
  result in a different rating." (entry l.32) — is the held caveat, and the
  entry's held CWE crosswalk names no CWE-122 node
  (`grep -c 'CWE-122' corpus/knowledge/program-severity-ladders-and-reward-scales.md`
  → `0`, exit 1), so no finer VRT placement is derivable from held ground.
- Reward: the only dollar figure is the advisory's recorded 4660 USD for the
  HackerOne report (advisory L102, L108). F13's held HackerOne policy record
  gives no numeric ladder for this vulnerability class, so no amount conversion
  is claimed.

## F17 — corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md

- Per the entry's own asset-class rule ("Claim 6 — an impact belongs to one asset
  class", entry l.56), a level requires the finding to sit inside one table.
- The demonstrated impact — heap memory overwrite with no code execution shown —
  does not reach the one Critical bullet the entry holds for the Websites-and-Apps
  class: "Execute arbitrary system commands" (entry l.58, quoting S051.txt:99),
  and the Smart Contracts class is excluded for a C-library finding by the same
  rule. So no VSCS level is claimable from the held bytes. If a follow-up
  demonstrated arbitrary command execution, it would meet the Websites-and-Apps
  Critical bullet quoted at entry l.58.
- F17 prices nothing regardless: "Classification only. No amount, currency or
  reward vocabulary occurs (FC-4)" (entry l.80). The 4660 USD is not derivable
  from this entry.

## F18 — corpus/knowledge/cisa-kev-catalog.md

- Membership check against the pinned feed: 1,756 records at catalogVersion
  2026.10.23 (entry l.18). `grep -c '38545' corpus/source-snapshots/round-35/S052.txt`
  → `0` (exit 1, no match); `grep -ci 'curl' corpus/source-snapshots/round-35/S052.txt`
  → `0` (exit 1, no match). CVE-2023-38545 is not KEV-listed in the pinned
  capture: no KEV-adjacent pricing applies, and none is invented.
- The catalog is not a price source regardless: "**"KEV is a payout ladder."**
  Rejected: no reward, bounty or currency vocabulary (FC-8); F13 and F17 carry
  price structures, this feed carries a deadline." (entry l.82).

## Bottom line

Tier by each held ground: F13 → VRT P2/High label-band by the advisory's own
Severity line (entry l.27), with the override caveat attached (entry l.32);
F17 → no level claimable from the demonstrated impact (entry l.56/l.58 criteria),
and no payout vocabulary at all (entry l.80); F18 → absent from the pinned
catalog (greps above), and not a payout source (entry l.82). The package may
state only the advisory's own recorded 4660 USD (advisory L108); no held entry
converts it into a tier figure.
