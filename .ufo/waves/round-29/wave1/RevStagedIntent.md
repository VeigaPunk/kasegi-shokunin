# Staged intent provenance receipt — F13

## Scope and method

The campaign package is read-only; this receipt compares its adopted-source claims with the current publisher documents. S031/S032/S033 in `SOURCES.append.md` correspond by **document**, not by staged numeric id, to lane S043/S044/S045. The lane captures are under `corpus/source-snapshots/round-29/`; each manifest record pins its snapshot SHA-256 and quote assertions. I fetched both Bugcrowd raw URLs using `capture-source.py`'s declared instrument UA (`kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`), observed HTTP 200, and observed response body SHA-256s identical to the lane snapshots. This establishes agreement with the publisher bytes fetched in this check; it does not establish that `master` is immutable or that the documents will not change.

HackerOne's staged S031 was also checked against the lane's captured policy text (manifest S043). That pinned record states policy record id 3787452 and the capture's matching body passages. The evidence chain is the staged claim → exact document URL → current fetched text / round-29 capture → located quote or JSON node below. Quotation punctuation and technical identifiers are preserved.

## S031 → lane S043: HackerOne standard program policy

**Holds, with bounded wording.** The staged scope proposition is explicit: “Issues affecting assets under HackerOne's control are in scope.” (policy record 3787452, `Program Scope and Assets / In Scope`; S043 manifest Q1). The third-party limitation is also explicit: “Third-party assets outside HackerOne's control are not authorized for testing because HackerOne cannot grant permission to test infrastructure it does not host or operate.” (same record, `Program Scope and Assets / Out of Scope`; Q2). This supports the claim about HackerOne's standard policy, not a universal legal rule about all programs.

The per-asset/per-finding-class cap is supported for the named example, not as an unrestricted description of every asset's complete reward table: “Eligible Denial of Service (DoS) findings are capped at the **Medium** severity bounty rate for the affected asset.” (`DoS Reward`; Q3). The same section gives distinct example amounts for `www.hackerone.com` ($1,000) and `hackerone.com` ($1,500), confirming asset-specific rates. It also says prohibited testing methods make reports “**not eligible**” for reward (Q4). Thus staged S031's generalization that policy caps severity/reward “per asset and per finding class” should be narrowed: this particular DoS class is capped at Medium and its sample assets have different amounts; the source does not establish that every finding class has a cap.

## S032 → lane S044: Bugcrowd VRT README

**Core description holds verbatim.** The live README describes “Bugcrowd's baseline technical severity rating” and calls the priority “Bugcrowd's suggested baseline technical severity” on the P1–P5 scale (S044 lines 10, 33; manifest Q1/Q3). It gives P1 Critical, P2 High, P3 Medium, P4 Low, P5 Informational (lines 34–38; Q4). The alteration claim is exact: “application complexity, bounty brief restrictions or unusual impact could result in a different rating” (line 11; Q2).

**Staged scope drift.** The staged S032 `teaches` statement changes the README's “bounty brief restrictions” into “a program's own brief.” That is a reasonable paraphrase but not verbatim, and the source is specifically describing Bugcrowd's recommended taxonomy, not an independently demonstrated rule for all programs. Likewise, saying application complexity or unusual impact can change priority is supported; do not convert that into an unqualified statement that each program itself formally changes VRT priority. The source also says VRT is a dynamic resource and that the VRT Council meets weekly (lines 5–8), while the staged row's “reviewed weekly by the VRT Council” is a compressed inference: weekly meetings/discussion and commits on consensus do not literally assert a weekly review cadence for every taxonomy item.

## S033 → lane S045: Bugcrowd CWE mapping dataset

**Data facts hold.** The fetched JSON is 28,482 bytes, SHA-256 `3de912588d845cd57e49dca40e3273b13290c3775b1d6e69b6787efb342ff364`, HTTP 200; this matches the lane S045 capture digest. Parsed JSON has 36 top-level `content` entries and `metadata.default` is null. At `$.content[5]`, `broken_access_control` contains child `idor` with `cwe: ["CWE-932"]`; `$.content[5].children[2]` is that IDOR node. These support the staged anchor's figures and mapping.

**Claim overreach.** The data is a maintained, machine-readable taxonomy-to-CWE mapping tree, but its structure alone does not establish the further operational conclusion that a program “can put its own priority ladder onto CWE without hand-mapping.” The README says mapping files can map VRT IDs to other classification systems and lists CWE as a supported mapping (S044 lines 79–83, 124–128); the dataset is a crosswalk, not a demonstrated automatic integration into a program's own ladder. The staged knowledge entry's “program maps its own priority ladder onto CWE automatically” and the implication that findings necessarily carry both fields are not evidenced by these two sources. Preserve the narrower claim: Bugcrowd publishes this VRT-id-to-CWE crosswalk; its metadata default is null, and some nodes have null CWE values (e.g. `ai_application_security`).

## Explicit staged-entry drift and limits for F13

The staged knowledge entry cites S032/S033 and additionally S034/S036, but its central combined narrative has uneven support. The Bugcrowd evidence establishes a suggested baseline technical-priority ladder and specific context-sensitive departures, plus a VRT/CWE crosswalk. It does **not** itself establish that four “incompatible ladders” are exhaustive, that CVSS is always decided by an analyst, that CNVD's example is a general law, that BILISRC and 360SRC share one reward scale, or that a program automatically combines its priority ladder and CWE mapping. Those are either other-source claims or synthesis/inference and must remain attributed and bounded by the relevant evidence. In particular, staged “Four incompatible ladders exist” is an analytic grouping, not a verbatim source assertion.

For F13's Limits section, cite this receipt and state: the live Bugcrowd README supports its P1–P5 **suggested baseline** and context-sensitive variation; the live CWE JSON supports a 36-category crosswalk with IDOR → CWE-932 and null default, but does not demonstrate automatic program integration. HackerOne supports its own scope and a specific DoS Medium cap, not a universal cap rule. The captures and hashes verify these quoted bytes only; remote re-fetches verify current publisher state at fetch time, not future stability.

## Reproduction evidence

- Live README fetch: HTTP 200, 8,881 bytes, SHA-256 `72576250dfff95344cdda7e2af00b3d4843a5785cef9e2af0ab1e251c69ec022`; round-29 S044 capture SHA-256 `8adfca615f3fc3ba9200c656a8184682b6de6d344d7436b74a7da11662b126bf` (normalized text capture, so digest need not equal raw response).
- Live CWE fetch: HTTP 200, 28,482 bytes, SHA-256 `3de912588d845cd57e49dca40e3273b13290c3775b1d6e69b6787efb342ff364`; S045 capture has the same digest and parses to 36 top-level categories.
- S043 capture SHA-256 `02ecb50086eefcf3d82bb4b3542b93010eda51448874de8d4c63ef5b9db4dfc6`; pinned quotes Q1–Q4 identify the policy anchors above.
- Snapshot comparisons are evidence of capture agreement, not proof of semantic correctness of any broader synthesis.
