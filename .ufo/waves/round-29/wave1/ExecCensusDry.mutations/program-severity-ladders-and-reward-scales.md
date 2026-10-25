# Program severity ladders and reward scales

source: S043 — https://hackerone.com/security/policy_versions — Program Scope and Assets and Denial-of-Service (DoS) Policy sections; policy record id 3787452, record timestamp 2026-10-16T15:34:59.854Z
source: S044 — https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md — "Description"
source: S045 — https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json — content > broken_access_control > idor
verified-at: 2026-10-25
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S043 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S044 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S045
ground: F13 (new frontier item; extends F01, which holds CVSS-B semantics only)

## The claim

CVSS-B is not what a program decides on. Four incompatible ladders exist, and the lane
now holds all four:

| Ladder | Shape | Who decides | Notes |
|---|---|---|---|
| CVSS v3/v4 base score | 0.1–10.0 vector score | the analyst | scores severity of the weakness, not business risk, not reward |
| Bugcrowd VRT | P1 Critical → P5 Informational | the program | a *suggested baseline*; the program may move a finding |
| CNVD 众测 points | multiplicative formula over 7 factors | the platform, then the project | severity is only one factor |
| BILISRC / 360SRC 安全币 | 严重 / 高危 / 中危 / 低危 / 忽略 + 经验值 | the vendor SRC | reward is money, scaled by business tier |

The VRT states the override explicitly: application complexity, bounty brief restrictions
or unusual impact can result in a different rating. The CNVD 众测 FAQ states the same in
Chinese — a submitted 高危 can be adjusted down to 中危 because project requirements
override the generic grading.

## The worked example that kills the "severity equals payout" assumption

The CNVD 众测 scoring page publishes a single worked example: a CVSS 10.0 RCE with test
difficulty 0.5, impact 1.5, enterprise size 1.5 and report quality 1.1 scores **12
points**. The same CVSS 10.0 RCE scores **10** on a 1.2 scale, **7** on 0.8, and **4** on
0.5 — the difference is entirely the target enterprise's size and the quality of the
report. A maximum-CVSS finding pays 4 points or 12 points depending on who was tested.

## CWE practice at the program layer

The VRT maintains a machine-readable crosswalk from its own ids to CWE
(`mappings/cwe/cwe.json`, 36 top-level categories): `idor` → `CWE-932`,
`authentication_bypass` → `CWE-287`, `privilege_escalation` → `CWE-269`. This is the
program-layer answer to "how does CWE practice actually work": a program maps its own
priority ladder onto CWE automatically, and a finding carries both a program priority and
a CWE id. Nodes without a CWE carry `cwe: null` (new AI and algorithmic-bias categories do),
so the crosswalk's gaps are visible rather than silent.

## Boundary

Severity ladders decide payout and triage, not legal exposure. Reward ceilings and the
"do not exceed authorised access" test are separate entries.
