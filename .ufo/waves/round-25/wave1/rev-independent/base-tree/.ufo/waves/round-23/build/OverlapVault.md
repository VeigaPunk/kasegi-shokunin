# OverlapVault — authorization / safe harbor vs credential and kagi

Seat: `KasegiR23.OverlapVault-5`. Read-only. Base named in `.ufo/waves/round-23/claims.json`: `922a4dde90b60b465e2b8b241d1fe363f1f27e98`. No production edit, no clone, no install, no detector run, no network fetch, no admission.

Axes this scan is not allowed to move:

- **depth:verifiability** — C1 detector mirror containment (`corpus/instruments/resolve.py` plus copied CLI). This scan does not read resolver fixtures and does not propose a resolver change.
- **coverage** — C2 F06–F08 only, frozen denominator eight public-practice surfaces, 5/8 → 8/8. F03 is already inside the 5.

## Finding

Authorization and safe harbor, as kasegi holds them, are public program-policy observations. They are not credential custody and they are not kagi scope. The words `authorization`, `authority`, `scope`, `credential`, and `vault` are homonyms across F03, F07, F08, kasegi hygiene, and kagi. A round-23 draft that treats any two of those as one object either inflates the F06–F08 count or pulls vault work into this lane.

## Exact boundary

**Kasegi owns** the four-way split already written in `corpus/knowledge/authorization-safe-harbor-and-scope.md:5-6`: safe-harbor language, explicit asset scope, testing grant, and prohibited methods are separate observations. A badge does not add assets or permit an excluded action (`:6-7`, `:16`). Frontier row F03 is `admitted` (`corpus/README.md:197`) on S006–S008 (`corpus/SOURCES.md:12-14`). `PROVINCE.md:27-33` classifies program rules, scopes, and claim packages as core. `PROVINCE.md:42-49` refuses adjacent lanes and names kagi as “secrets and vault handling.” Live-target testing is refused (`PROVINCE.md:49`).

**Kagi owns** secrets and vault ops (`/home/vgpnk/Projects/shokunin/kagi-shokunin/PROVINCE.md:3`) and runtime auth plus credential custody (`:63`). Core there is 1Password machine-credential custody, SOPS/age rotation, and Vault/OpenBao token, lease, and KV clocks (`:61`). Vault-side structure stays unmapped (`:55`). Kagi’s own frontier is OIDC, secret-scanning detection vs verification, and NIST key management (`kagi-shokunin/corpus/README.md:110-112`), not bounty safe harbor.

**The cut:** kasegi may record that a public policy read used no credential. Kagi owns the credential if one exists. Quoted lines:

- Scope snapshot retrieval flags are booleans, all false in the exemplar: `credentials_used`, `accounts_created`, `terms_accepted` (`SKILL.md:96-98`).
- Custodian skeleton for `read_public_policy`: `data_classes: ['public']`, `credential_binding` and `external_effect` both none (`SKILL.md:919-922`).
- Envelope field list includes `credential_policy` and `external_effect_authorization` (null unless operator preauthorized) (`corpus/knowledge/policy-access-playbook.md:27-29`). The field name is kasegi schema. A populated secret value is not.
- Package secrets gate is a regex over package text (`corpus/knowledge/claim-gates.md:43-50`) and a `no_secrets` subcheck beside hard gate `authorization` (`:75-77`). Kagi classifies that class of check as a hygiene filter, not vault ops: “chousa, kasegi and kumitate run their own secret-shaped tripwires over their outputs (hygiene filters, not vault ops)” (`kagi-shokunin/PROVINCE.md:63`). Same split in kagi’s frontier note (`kagi-shokunin/corpus/README.md:111`).
- Q6 forbids credential material, session or private URL, and a vault-reference URI in an admitted entry (`corpus/QUALITY.md:19`). `LOG.md:1102-1104` records that the literal vault-scheme token was reworded so the commit credential sweep would not fire. Round 23 must not paste that scheme back into F03 or into an F06–F08 draft.

**Not this boundary:** C1 mirror “scope” (`claims.json` C1) and kagi `corpus/scope-gate.sh` directory partition (`kagi-shokunin/PROVINCE.md:51`). Neither is program-asset scope.

## Homonyms that must not be merged

| Token in round 23 | Label | Owner | Not |
|---|---|---|---|
| Safe-harbor statement, asset list, testing grant, method prohibition (S006–S008) | `F03-policy` | kasegi F03, already admitted | not a testing permission by itself; not a vault grant; not an F06–F08 row |
| S006 sentence that researchers “are authorized to conduct such activity” | `F03-policy` | entry `:21` calls this HackerOne’s description, “not a universal legal conclusion” | not kagi `AUTH_OK` / `AUTH_REQUIRED` (`kagi-shokunin/PROVINCE.md:28-29`) |
| CNA Scope Definition / assignment authority (S022) | `F07-cna` | coverage candidate | not F03 asset scope; not `scope-gate.sh` |
| CRA manufacturer reporting (S024) | `F08-cra` | coverage candidate; DraftF08 says manufacturer duty, not researcher authorization | not F03; not a credential |
| `credentials_used: false`, `credential_binding: none`, `credential_policy` with no secret value, `no_secrets` | `hygiene-only` | kasegi record | not a transfer of the entry into kagi |
| Vault unlock, secret bytes, op-reference, lease, session, private URL | `kagi-custody` | kagi, operator-present | not corpus quote material |

`SKILL.md:868-870` names “vault unlock, MFA, KYC, the Submit click, payout rails” as one lost operator-only contract. Only vault unlock is kagi. KYC, submit, and payout stay operator/kasegi packaging. The clause is a pointer to a lost runbook, not a procedure.

`corpus/knowledge/program-quirks.md:56-57`: an unprovisioned Bugcrowd identity means `credentialed testing` is not granted. That negative is kasegi program-rule text. Provisioning the identity would leave this lane.

`corpus/knowledge/evidence-dir.md:53` names a lost program directory `hackerone-1password/round-1`. That is a kasegi program label, not kagi’s 1Password custody entry.

`corpus/knowledge/evidence-dir.md:25` and `:71`: `authorization-envelope.json` is “grant scope derived from snapshot bytes”; `negative-auth-walled.json` is an auth-walled negative class. An auth-walled policy read parks in kasegi (`SKILL.md:128-132`, `policy-access-playbook.md:10`, `:13`). It is not completed by a kagi vault read.

## S006 heading contradiction (stays inside F03)

Same quote, three location labels, none of them a credential path:

- Entry `:20` places “Adopting a Safe Harbor does not change the program scopes.” under “How to Enable Safe Harbors (Program Owners & Admins)”. Header `:2` uses that same heading as the S006 anchor.
- `corpus/lessons/round-22.md:82` places that sentence (plus the following sentence) under “What is safe harbor?”.
- `corpus/lessons/round-22-verifier-spotcheck.md:12` and `:17` call the defect “S006's Gate location” / “M5 S006 Gate location”.
- `corpus/QUALITY.md:48` R8 says the quote “was attributed to the wrong heading” and cites `corpus/lessons/round-23.md` M5. That lesson path is absent in this tree.

`claims.json` `supporting_corrections` lists “M5 S006 quote location” and says these corrections get no independent axis credit. Whichever heading a later public-doc seat confirms, the correction is an R8 superseding row (`QUALITY.md:48`: new row beginning “supersedes S###”, old S006 fields immutable). It does not add a frontier id and it does not move 5/8.

This seat did not re-open the HackerOne page. SafeHarborLocation owns that fetch.

## Cross-domain routing

1. **SafeHarborLocation, ImmutableSources, RegistryDraft.** S006 heading repair stays `F03-policy`. New source row only if R8 requires it. Do not edit S006 in place. Do not count it in F06–F08. Do not send the quote to kagi.
2. **DraftF06 / OverlapResearch.** FIRST multi-party coordination is chousa-method vs kasegi-application (OverlapResearch). It is not safe harbor and not vault auth. S018 remains the F06 source (`corpus/README.md:200`).
3. **DraftF07.** “Scope Definition” and assignment authority are `F07-cna`. If the draft says the CNA rule authorizes a researcher to test, that sentence is a failed F03/Q4 generalization, not a kagi finding.
4. **DraftF08 / SourceSafety.** Article 14/71 manufacturer duty is `F08-cra`. A sentence that turns it into researcher authorization fails SourceSafety’s lane and Q4. It is still not routed to kagi.
5. **RecheckSources / any 403.** C2 text (`claims.json` C2): absent official text is rejected/unprovable, not a substituted authority. Do not open a vault or a program login to manufacture the page. Kasegi already parks auth-walled policy reads.
6. **FixtureSafety / CountMirror.** Mirror fixtures stay on the resolver. They must not read secret, account, or live-target material. That constraint is FixtureSafety’s; this seat does not add fixture paths.
7. **Kagi.** Receive only `kagi-custody` tokens, and only through the orchestrator. Kagi `PROVINCE.md:5` refuses out-of-domain work. Public safe-harbor FAQ text is out of domain there.

## Proposed move

One integration rule for L1, not a production patch from this seat:

Before any F06–F08 admission decision, label each round-23 sentence that contains authorization, authority, scope, credential, vault, or safe harbor with exactly one of `F03-policy`, `F07-cna`, `F08-cra`, `hygiene-only`, `kagi-custody`. Unlabeled or dual-labeled sentences do not count toward 3/3. A `kagi-custody` token inside a knowledge entry fails Q6. A missing official page stays rejected/unprovable rather than being fetched with credentials.

Affected axis: **coverage**. The rule keeps the numerator on S018, S022, and S024 (`corpus/README.md:200-202`) and keeps F03 inside the already-admitted five. It does not change `resolve.py`, so **depth:verifiability** is untouched.

## Falsifier

The partition is false if any one of these is observed in an integrated round-23 tree:

- An F06, F07, or F08 `corpus/README.md` row whose sources are not S018, S022, or S024 respectively, or whose entry’s load-bearing quote is the S006 safe-harbor sentence.
- F03 or the S006 heading repair included in the 0/3 → 3/3 count.
- A kasegi knowledge entry that contains secret bytes, a session, a private URL, or a vault-reference URI in order to “prove” safe harbor or to open FIRST/CNA/EUR-Lex text.
- A kagi knowledge entry that takes the HackerOne/Bugcrowd/CISA safe-harbor quotes as vault or runtime-auth evidence.

## Risks

- Tagging `credential_policy` or `credentials_used: false` as `kagi-custody` would move the lost envelope schema out of kasegi. Those are `hygiene-only` while the value is absent, null, false, or none.
- Tagging S006 “authorized” or S008 “not authorized for testing” (`corpus/lessons/round-22.md:84`) as `F08-cra` would launder platform policy into the CRA row and fail Q4.
- Treating kagi `scope-gate.sh` as the owner of “scope” would send bounty asset lists to a directory-partition gate.

## Verification and limits

Read at the lane tree: `PROVINCE.md`, `claims.json`, `corpus/QUALITY.md`, `corpus/README.md:191-202`, `corpus/SOURCES.md:12-14` and `:38-39`, `corpus/knowledge/authorization-safe-harbor-and-scope.md`, `SKILL.md:54-98`, `:124-132`, `:640-643`, `:868-870`, `:919-922`, `:1021`, `corpus/knowledge/claim-gates.md:43-77`, `policy-access-playbook.md:17-29`, `program-quirks.md:56-57`, `evidence-dir.md:24-25` and `:53` and `:71`, `corpus/lessons/round-22.md:82` and `:125-137`, `corpus/lessons/round-22-verifier-spotcheck.md:12` and `:17`, `LOG.md:1102-1104`, `SCORECARD.md:380-385`. Sibling province read: `kagi-shokunin/PROVINCE.md:1-5`, `:27-29`, `:51`, `:55`, `:61-63`, and `kagi-shokunin/corpus/README.md:110-112`.

`corpus/lessons/round-23.md` is not in the tree; R8’s citation of it is unresolved here. HackerOne was not re-fetched, so this seat does not pick among the three S006 headings. No score, no admission, no detector before/after.

Installs: none.
