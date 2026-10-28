VERDICT: INFO

# R46ScoutLeadZDI — lead screen: Zero Day Initiative (ZDI) disclosure policy

Scope: one lead, read-only. Target: https://www.zerodayinitiative.com/advisories/disclosure_policy/. No registry row, no knowledge entry, no commit. Milestone items (F28 entry, C1 re-grounds, counter falsification) are not this seat's item and were not run here.

## 1. Capture (what was fetched)

Command (scratch `$HYAKU_SCRATCH/kasegi-r46/R46ScoutLeadZDI`, TMPDIR passed explicitly):
`python3 corpus/instruments/capture-source.py --id S0XX --url https://www.zerodayinitiative.com/advisories/disclosure_policy/ --out <scratch>/zdi.txt --kind html`

Output:
`S0XX status=200 fetched_bytes=25321 snapshot_bytes=4701 sha256=9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1 utc=2026-10-28T23:10:34Z`

Do-nothing / determinism control: a second capture to `zdi2.txt` printed the same digest, and `sha256sum zdi.txt zdi2.txt` gave `9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1` for both. `--selftest` printed `selftest normalize=ok deterministic=ok`. Raw bytes were fetched separately with curl: `http=200 bytes=25321`, matching the probe.

Comment check: the raw HTML has 32 `<!--` and 32 `-->`. A scan showed the policy paragraphs (raw offsets 10329–13739, "This policy outlines" at 10329) are not inside any comment pair. The instrument does not strip HTML comments, so capture lines 1–4 and some later lines are commented-out shell text. The quotes below come from policy body lines only.

Snapshot line numbers (capture `zdi.txt`, 60 lines):

## 2. Policy facts (located quotes, each ≤25 words)

- **Deadline:** L24 "allow the vendor four months (120 days) to address the vulnerability with a security patch or other corrective measure" (19 words).
- **Tiered patch-regression windows:** L25 "critical-rated bugs where active exploitation is detected or imminent, the vendor will have 30 days"; "All other reports in this category will be given a time of 90 days." (60-day tier also in L25).
- **What starts the clock:** the 120-day clock has no stated start event. L24 says only "If a vendor response is received within the timeframe outlined above". The one trigger named is L23 "fifteen business days after the initial contact" (public advisory after exhausted contact). Per F02's rule, the 120-day start is **unknown**.
- **Earlier clocks:** L23 "within five business days, TrendAI™ ZDI will attempt a second formal attempt" (acknowledgement); L23 "If a vendor fails to respond after an additional five business days".
- **Extension rule:** L24 "Extensions to the 120-day disclosure timeline are up to the sole discretion of TrendAI™ ZDI and will be granted only in rare circumstances." (23 words).
- **At deadline:** L24 "will publish a limited advisory including mitigation in an effort to enable the defensive community to protect the user" (no patch by deadline).
- **Researcher communication:** not in the policy body. Command: `grep -niE 'research|finder|reporter|credit|notify|communicat|summary' zdi.txt` matched L21, L26, L31, L45, L53. L31 "RESEARCHERS" and L53 "Researcher Rewards" are nav/footer. `grep -ciE 'researcher|finder|reporter'` printed `2`, both nav. The only communication commitments are vendor-facing: L21 "promptly notify the appropriate product vendor", L26 "publishing a summary of the communication we've had with the vendor regarding the issue". The policy says nothing about notifying, crediting or updating the reporter.
- **Revision date:** none in the capture. The only footer date is L39 "©2026 TrendAI™ Zero Day Initiative™ (ZDI)."

## 3. Corpus check (no ZDI policy present)

Command: `grep -rliE 'zero day initiative|zerodayinitiative|ZDI' corpus` printed:
`corpus/lessons/round-43.md`
`corpus/SOURCES.md`

Line-level: round-43.md:60 "ZDI-26-811 (no fix commit and no scope or reward sentence)"; round-43.md:65 "the ZDI index (2551868 B) used only to confirm the advisory URL"; SOURCES.md:154 is a hunt note naming "ZDI published-advisories index" and ZDI-26-811. These are advisory pages and an advisory index. None is the disclosure policy.

Precise absence grep: `grep -rniE 'zerodayinitiative\.com/advisories/disclosure_policy|TrendAI|five business days|fifteen business days|Zero Day Initiative' corpus` printed `(no matches)`.

Positive control (the grep works on policy text): `grep -rliE 'Project Zero|CERT/CC' corpus/knowledge` printed five files including `corpus/knowledge/coordinated-disclosure-timelines.md`.

`ls corpus/knowledge | grep -ciE 'zdi|zero-day'` printed `0`.

## 4. Overlap with existing frontier

- **F02 (coordinated-disclosure-timelines.md, S003/S004/S005):** overlaps on clocks. F02's rule (lines 7–17) requires naming the coordinator, the trigger, the interval, the patch/publication relation and any extension. ZDI's 120-day clock has no stated trigger, so F02 would record it as unknown. F02 forbids transplanting another coordinator's interval, so ZDI's 5/15-day and 120-day figures cannot be merged into F02's CERT/CC 45-day or Project Zero 90+30 rows.
- **F15 (vendor-third-party-finding-coordination.md, S048):** closest topical match. ZDI is a security vendor's programme that acquires other vendors' bugs ("an acquired vulnerability"). F15 says to record which party coordinates and to read no clock from it, so ZDI can only add a coordinator-identity cross-reference there.
- **F10 (S036–S040):** vendor-side policies for product vendors. ZDI is a third-party coordinator, so it does not fit F10 as a vendor's own policy.

## 5. Proposal for round 47 (for L1 decision)

- Admit ZDI as a **candidate**, not a new frontier topic. Recommended form: one new F02 coordinator row (next free S-id after the F28 reservation S073, so S074 if the L1 keeps that numbering), tier **A** (ZDI's own first-party policy page, same kind as S003–S005).
- Scope limits: the disclosure-policy page text only. Exclude advisories (ZDI-26-811 stays screened out), reward and program rules, and the researcher-facing submission page (not captured here).
- Required findings: the 120-day clock start is unknown; extensions are discretionary and rare; researcher communication is absent from the policy body.
- A separate frontier would double-count F02's clock rule. F15 gets only a cross-reference.

## 6. Limitations

- One fetch plus one same-instant re-capture; the host can serve different bytes later, so the digest binds only these bytes.
- Comment-leak lines in the capture (1–4 and later) are not policy text; the quotes avoid them, but the instrument does not strip comments.
- The policy's revision date is absent from the page, so the snapshot date is the only dating.
- Clock-start conclusion is a reading of the policy text; it is not confirmed by ZDI.
- No registry row was written; no knowledge file was written; the F28 and C1 milestone items were not run by this seat.
