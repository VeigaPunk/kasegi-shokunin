# Program severity ladders and reward scales

source: S043 — https://hackerone.com/security/policy_versions — standard policy record 3787452 `new_policy` captured as `corpus/source-snapshots/round-29/S043.txt`; In Scope L31, Out of Scope L40, same-finding reward L92, DoS Reward L170
source: S044 — https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md — Description and Data within an Entry > Priority, lines 10–11, 33–38 of `corpus/source-snapshots/round-29/S044.txt`
source: S045 — https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json — `metadata.default`; `content[5].children[2]` (`broken_access_control` → `idor`); `content[0]` and `content[6].children[8]` null examples in `corpus/source-snapshots/round-29/S045.txt`
verified-at: 2026-10-25
ground: F13
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S043 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S044 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-29/manifest.json --source S045

## The claim

Severity labels, program policy, and monetary reward are related but not interchangeable. A platform's published taxonomy supplies its own classification vocabulary; an individual program's policy can bound authorization and reward within that program. The HackerOne and Bugcrowd statements below are those platforms' own statements, not universal rules for bounty programmes.

## HackerOne standard program policy set

The captured standard policy record 3787452 distinguishes the assets the program controls from third-party assets and states a per-asset ceiling for eligible denial-of-service (DoS) findings. Its own text says: “Issues affecting assets under HackerOne's control are in scope.” (S043.txt:31, Program Scope and Assets > In Scope; manifest Q1.) It also says: “Third-party assets outside HackerOne's control are not authorized for testing because HackerOne cannot grant permission to test infrastructure it does not host or operate.” (S043.txt:40, Program Scope and Assets > Out of Scope; manifest Q2.)

For the per-asset reward cap, the policy states: “Eligible Denial of Service (DoS) findings are capped at the **Medium** severity bounty rate for the affected asset.” (S043.txt:170, DoS Reward; manifest Q3.) It also gives a per-finding constraint: “Using multiple approved proof-of-concept reports to demonstrate the same issue does **not** increase the severity or reward of a finding.” (S043.txt:92, Approved Reports for Proofs of Concept; manifest assertion anchors this same policy record.) These are bounds in this policy record, not a general cap formula for other HackerOne programs or other platforms.

## Bugcrowd VRT ladder and override

The Bugcrowd VRT README describes its priority as “Bugcrowd's suggested baseline technical severity of the vulnerability on a P1 (Critical) to P5 (Informational) scale.” (S044.txt:33; manifest Q3.) The displayed labels are:

| VRT priority | Label |
|---|---|
| P1 | Critical |
| P2 | High |
| P3 | Medium |
| P4 | Low |
| P5 | Informational |

The VRT's stated override is: “application complexity, bounty brief restrictions or unusual impact could result in a different rating.” (S044.txt:11; exact contiguous excerpt of the suggested-baseline sentence, manifest Q2.) The excerpt is kept within the 25-word quote limit; the source sentence's full wording is available at the cited captured line. Thus the P1–P5 mapping is Bugcrowd's suggested baseline, not a mandatory rating independent of context.

## CWE crosswalk and visible gaps

The VRT mapping dataset maps `broken_access_control` → `idor` → `CWE-932` (S045.txt:73, 91-94; JSON path `$.content[5].children[2]`; manifest Q1). The captured lines are:

```json
"id": "idor",
"cwe": [
"CWE-932"
]
```

It maps `privilege_escalation` to `CWE-269` (S045.txt:97-100). The dataset exposes uncovered mappings rather than implying every node has a CWE: its root default is `"default": null` (S045.txt:2-4; manifest Q2), and individual nodes can have `"cwe": null`, including `ai_application_security` (S045.txt:7-9; JSON path `$.content[0]`, manifest Q3) and `excessive_jwt_lifetime` (S045.txt:170-171; JSON path `$.content[6].children[8]`, manifest Q4). These are properties of this captured Bugcrowd crosswalk; `cwe: null` means this mapping data supplies no CWE value at that node, not that the weakness has no classification in every scheme.

## Falsifiable checks

1. Given the pinned S044 capture, check that the five priority labels occur in order P1 Critical, P2 High, P3 Medium, P4 Low, P5 Informational at lines 34–38. If a label or its order differs, the ladder stated here is falsified for this capture.
2. Given the S043 record 3787452 text, check that its DoS reward ceiling says Medium for the affected asset and that repeated approved PoCs for the same issue do not increase that finding's severity or reward. A different statement in that record falsifies the policy summary here.
3. Given S045, check `broken_access_control` → `idor` → `CWE-932` at `$.content[5].children[2]` and the null default/node examples at `$.metadata.default`, `$.content[0]`, and `$.content[6].children[8]`. Missing or different values falsify the crosswalk description.

## Rejected over-generalizations

- **Rejected: “P1–P5 is a universal severity or payout scale.”** The P1–P5 wording is explicitly Bugcrowd's suggested baseline, with its own context-dependent override (S044.txt:11, 33-39); neither the text nor the mapping establishes a universal rubric or payout schedule.
- **Rejected: “Every finding must have a CWE, or `cwe: null` means the finding has no CWE.”** S045 explicitly contains a null default and null node values (S045.txt:3, 8, 12, 16, 20); those data show gaps in this crosswalk, not a universal absence of a classification.
- S043 capture is the record-scoped `new_policy` text for policy record 3787452 (204 lines, 7,298 bytes; SHA-256 `d3b815ed75e3e32b2ae363b9f612c3d25b9c8c585df2c4cd797296f2ded69199`, per capture receipt revision 1), rather than the original one-line API wrapper. The raw fetch and the deterministic record extraction are documented in `ExecCapS043.md`. This scoped representation makes the policy locations direct line anchors.
## Attribution and boundary

HackerOne policy statements above are HackerOne's standard-policy text; the VRT ladder and its override are Bugcrowd's statements; the crosswalk is Bugcrowd's dataset. They are not universal authorization, severity, or reward rules. This entry is documentation-only: it gives no instruction to probe, scan, log in to, or submit against any target, and contains no credential or session material.

## Limits

- The staged package entry also included CNVD 众测 and BILISRC ladders and a worked CNVD score example. They are **not adopted this round**: this F13 entry is limited to the three captured lane rows S043/S044/S045 and their round-29 manifest assertions.
- Staged S032 (Bugcrowd VRT README) and S033 (Bugcrowd CWE map) are mapped by document to lane S044 and S045 respectively. Staged S031 (HackerOne policy set) maps to lane S043. Citations here use the lane ids, never staged numeric ids.
- S043 is a raw minified one-line JSON capture. The manifest's line anchor is necessarily line 1; its location fields identify record 3787452 and the relevant `new_policy` section. `source-recheck.py` counts normalized substrings across the whole capture, so repeated boilerplate may report multiple occurrences even where the location identifies this policy record; see the manifest receipt for the observed counts and limitation.
- The quoted VRT override is a contiguous excerpt under 25 words, rather than the complete source sentence, which exceeds the quote-length bound. The citation points to its full sentence at S044.txt:11.
