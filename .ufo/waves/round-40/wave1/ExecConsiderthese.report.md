# Sky (formerly MakerDAO) — remote code execution on the vote application through gray-matter's JavaScript engine

- Program: Sky bug bounty on Immunefi — `https://immunefi.com/bug-bounty/sky/` (HTTP 307 to `https://immunefi.com/bug-bounty/sky/information/`); triaged by Immunefi, PoC required, KYC not required, Maximum Bounty `$10,000,000`, Last Updated 19 September 2026.
- Affected asset: `https://vote.makerdao.com/` — the polling and proposal-creation flow of the vote application, whose current successor asset in the same program is `https://vote.sky.money/`.
- Vulnerability class: remote code execution (CWE-94 code injection). Proposal front-matter fetched from a user-supplied URL is parsed by `gray-matter` with its JavaScript engine left enabled, so `eval` executes attacker-supplied content in the server process.
- Severity, platform vocabulary: Immunefi Vulnerability Severity Classification System v2.2, `Websites and Apps` table, **5. Critical** — "Execute arbitrary system commands".
- Reward, program's own ladder: **USD 50,000**.
- Payout reported for this finding: **USD 50,000** — the derived figure equals the observed one.
- Disposition: PARKED, `claimable: false`. This is a re-pricing of a finding that was already submitted and paid in 2023; no authorized testing exists behind it and none is claimed. **No submission performed.**

## Scope excerpt

Program text quoted verbatim from `https://immunefi.com/bug-bounty/sky/`, observed at 2026-10-26T21:19:06Z (final URL `https://immunefi.com/bug-bounty/sky/information/`, HTTP 307 → 200, 554144 raw bytes).
Content sha256 of the captured policy text: `7bcbd40754a37f838b48ffc19de3d59019e8081c94516689a4eac9e158ee95d9` over `evidence/sky-program-scope-rewards.txt` (1041 lines, normalized capture: raw HTML with the per-request CSP nonce removed by tag stripping; a second independent fetch normalized to identical bytes).

The asset rule for the affected host:

> "All Medium and High level bug reports are not in-scope for the https://vote.sky.money/ asset. Only Critical severity reports are in-scope for this asset." — `evidence/sky-program-scope-rewards.txt:175`

Program identity, as printed on the page:

> "$10,000,000" — `evidence/sky-program-scope-rewards.txt:72` (the "Maximum Bounty" label is at `:71`)

> "19 September 2026" — `evidence/sky-program-scope-rewards.txt:76` (the "Last Updated" label is at `:75`)

> "Total Assets in Scope 255" — `evidence/sky-program-scope-rewards.txt:1017`

Eligibility and reward text for a website/application impact:

> "Critical website and application bug reports will be rewarded with USD 100 000 only if the impact leads to a direct loss in funds involving an attack that does not require any user action at all." — `evidence/sky-program-scope-rewards.txt:116`

> "All other impacts that do not fall under this definition, but would be classified as Critical, and resulting in a theft of funds, will be rewarded USD 50 000 ." — `evidence/sky-program-scope-rewards.txt:116`

> "Manipulation of polling votes or voting results, including modifications to their display, qualifies for a reward of USD 10,000 only if it leads to the incorrect option being selected as the final winner of an active poll." — `evidence/sky-program-scope-rewards.txt:171`

> "Proof of concept is always required for all severities." — `evidence/sky-program-scope-rewards.txt:993`

> "Any testing on mainnet or public testnet deployed code; all testing should be done on local-forks of either public testnet or mainnet" — `evidence/sky-program-scope-rewards.txt:998` (prohibited activities)

> "No KYC information is required for payout processing." — `evidence/sky-program-scope-rewards.txt:991`

> "Category 3: Approval Required" — `evidence/sky-program-scope-rewards.txt:995` (responsible publication)

Payout mechanics: "payouts are done in DAI or USDS , at the discretion of the Sky team, assuming a full 1:1 ratio with the USD ." — `evidence/sky-program-scope-rewards.txt:195`.

## The finding, as published

Immunefi published the disclosure as a bug fix review on 2025-02-25. The report's own account:

> "On 25 September 2023, a security researcher named xss submitted a critical vulnerability to Sky (formerly known as MakerDAO) through Immunefi." — `evidence/sky-rce-bugfix-review.txt:39`

> "The white-hat was able to execute malicious code on vote.makerdao.com to extract sensitive content from the filesystem such as /etc/passwd." — `evidence/sky-rce-bugfix-review.txt:39`

> "resulting in a maximum critical bounty payout of $50,000" — `evidence/sky-rce-bugfix-review.txt:40`

Root cause, in the disclosure's words:

> "Sky was using the gray-matter library without disabling the JavaScript engine feature, which runs eval on the provided Markdown." — `evidence/sky-rce-bugfix-review.txt:53`

## Repro steps (as published; not executed here)

1. A proposal is created at `https://vote.makerdao.com/polling/create` and pointed at a Markdown URL the attacker controls:

   > "The attacker creates a poll at https://vote.makerdao.com/polling/create using the following URL:" — `evidence/sky-rce-bugfix-review.txt:56`

2. The application fetches and parses that Markdown. With `gray-matter`'s JavaScript engine enabled, a `---javascript` front-matter argument turns the parse into `eval` of an OS command.
3. The command's output is read back from the polling API:

   > "one can visit the following url endpoint https://vote.makerdao.com/api/polling/all-polls?network=goerli to view the output of the malicious command i.e cat /etc/passwd ." — `evidence/sky-rce-bugfix-review.txt:57`

No secret appears in the published steps: the payload is a public gist and the command reads a world-readable file. This package did not re-run any step; see `evidence/no-live-testing.txt`.

## Impact in the program's own terms

The consequence is command execution inside the vote application's server process — the first bullet of the VSCS v2.2 `Websites and Apps` Critical row, "5. Critical- Execute arbitrary system commands" (`evidence/vscs-v2.2-websites-and-apps.txt:13`). The row's file-read bullet enumerates "/etc/shadow", "database passwords" and "blockchain keys" (`:15-17`) and states it excludes "non-sensitive environment variables, open source code, or usernames" (`:18`); `/etc/passwd` is not in that list, so the level rests on the command-execution bullet, not on the file that was read as proof.

The affected host is a governance surface: a proposal-creation flow that writes to the same application that serves vote casting. The disclosure does not claim theft of funds, and no fund loss is attributed to this finding.

## Pricing through the F13 / F17 / F18 rubric

**F17 — Immunefi VSCS v2.2 (platform severity vocabulary).** The tables rank within an asset class; this is a website/application asset, so the `Websites and Apps` table governs and the `Smart Contracts` table does not. Level: **5. Critical**, on the command-execution bullet. v2.2 states the level is fixed "largely by the impact", so exploitation likelihood does not move it.

**F13 — the program's own severity ladder and reward scale.** The platform names the level; the program fixes the money. The page prints two Critical website/application tiers: USD 100,000 where the impact is direct fund loss with no user action (or unauthorised minting of tokens), and USD 50,000 for "all other impacts … resulting in a theft of funds" (`:116`). The finding is not fund loss, so it prices at the lower Critical tier, **USD 50,000** — which is exactly the payout the disclosure reports (`evidence/sky-rce-bugfix-review.txt:40`). Derived equals observed.

Two ladder properties are worth recording, because both are triage hazards:

- **Ladder gap.** The page prints no Critical website tier for an impact that is neither fund loss nor unauthorised minting. A data-exfiltration Critical has no printed price on the current page at all; the USD 50,000 figure is the closest printed Critical tier and is also the empirically paid amount, but the ladder does not derive it. A triager reading only the page cannot price this class without the observed anchor.
- **Anti-anchor.** The same host carries a specific polling clause worth USD 10,000 (`:171`). It is the seductive row — the words "polling" and "vote" appear in it — and using it prices the finding five times low. It does not apply: it prices manipulation of poll outcomes and display, not command execution. The asset rule at `:175` also removes Medium and High on this host, so a triager who downgrades the RCE below Critical has priced a class the program does not accept there.

**F18 — CISA KEV (exploitation status).** The capture holds 1756 CVE records; four probes over vendor/lab name, library name, token name and hostname stem return zero matches, and the public disclosure assigns no CVE identifier at all, so there is no key by which KEV could hold it. KEV status: **absent** (`evidence/kev-absence-query.txt`). KEV is orthogonal here: it cannot raise priority, and it does not lower the VSCS level, which v2.2 fixes on impact.

Net price: **VSCS 5 Critical · program ladder USD 50,000 · KEV absent.**

## Suggested fix (as published)

> "Instead of passing Markdown content directly to the gray-matter library, it’s now routed through the matterWrapper function, which validates the input and disables the JavaScript engine" — `evidence/sky-rce-bugfix-review.txt:60`

The fix is structural rather than input-filtering: the parse is wrapped so the JavaScript engine cannot be reached from content, which removes the `eval` sink instead of blocklisting a front-matter key.

## Disclosure timeline

| When | What | Source |
|---|---|---|
| 2023-09-25 | report submitted to Sky through Immunefi; RCE on `vote.makerdao.com` | `evidence/sky-rce-bugfix-review.txt:39` |
| within two days | report "validated and confirmed by the Sky team" | `evidence/sky-rce-bugfix-review.txt:40` |
| 2023-09-28 | vulnerability fixed | `evidence/sky-rce-bugfix-review.txt:59` |
| 2025-02-25 | bug fix review published by Immunefi | `evidence/sky-rce-bugfix-review.txt:34` |
| 2026-10-26 | this package: program scope and reward ladder re-captured and the finding re-priced | `evidence/sky-program-scope-rewards.txt` |

## No submission performed

This package is a re-pricing of a publicly disclosed and already-paid finding. It was not submitted anywhere, no account was created, and no request was made to any Sky or MakerDAO asset. The literal marker: **No submission performed**.
