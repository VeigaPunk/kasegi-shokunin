# Independent semantic expectations, before author schema/fixtures/code
Reviewer: parent-appointed judge_kasegi_round58; 2026-11-02. Actual work: one independent review agent, no eight-L2 concurrency claim.

Official source independently opened: https://docs.kernel.org/process/security-bugs.html, Preparing your report; What qualifies as a security bug; Responsible use of AI to find bugs. One short quotation retained: “A stable identifier such as a commit ID or an exact version is required.” (Preparing your report). No other quotation from this source is needed for this review.

Expectations derived from source, not author cases:
1. Exact upstream version and a recent-code check are separate: syntactically exact old/distro identifiers do not establish current upstream reproduction.
2. A report must connect a triggering action and confirmation to the same tested version and applicable configuration, permissions, timing and modifications. All-fields-present can still be unsupported.
3. Corroboration must include actual harmless replay, not a boolean or arbitrary trace string. A trace copied from another input/run/version or a fabricated result must not corroborate the described behavior.
4. Claimed impact must be no stronger than observation; a denial or ordinary authorized action is not evidence for privilege crossing. Correctly configured production-system trust boundary matters. Changed/revoked assumptions invalidate conclusions that depend upon them.
5. A harmless synthetic model can establish only model behavior under its explicit assumptions. No JSON instrument proves a real kernel bug, exploitability, reporter approval, recipient eligibility or permission to submit.
6. AI-assisted discovery's public handling and withholding the security reproducer are separate statuses; human checking does not erase AI origin, and withholding from public publication does not mean unavailable privately or untested.
7. Source is Linux-kernel-specific, not a universal disclosure rule. Unsupported policies must not silently borrow these decisions.
8. Material gain must show domain judgment that prior prose lacked, not merely syntax validation, form completeness, keyword counting or status restatement.

Planned independent contrast classes: corroborated bounded replay vs field-complete irrelevant trace; forged/inconsistent observations; upstream-version mismatch; unsupported impact; absent/wrong triggering conditions; revoked necessary assumptions; AI verification with withheld/public reproducer; unrelated policy. Schema-dependent executable cases will be frozen separately before candidate execution.

Scope: offline synthetic evidence only; no target access, exploit execution, external contact, local computer, paid provider, new authorization, pushes or lane edits. Reviewer writes only this audit directory. Initial prompt lookup at cwd failed, then actual fleet prompt located; no substantive result concealed.
