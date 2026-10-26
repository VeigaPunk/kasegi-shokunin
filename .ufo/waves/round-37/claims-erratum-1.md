# Claims erratum 1 — kasegi round 37 (filed before any seat scored)

Frozen claims: `.ufo/waves/round-37/claims.json` (commit `224df74db2a46d627ae1475a72ca48796bbd177c`). This
erratum is appended, never an edit to the frozen file. It changes the **C2 S054 capture URL literal** from

    https://certcc.github.io/SSVC/            (the docs home page)

to

    https://certcc.github.io/SSVC/tutorials/ssvc_overview/   (the "What is SSVC?" overview tutorial page)

Reason (pre-freeze satisfiability, QUALITY R22/R25): the home page capture contains only the SSVC
definition/stakeholder sentences and navigation. The entry's load-bearing claims — the methodology's
stakeholder-tailored prioritization, the decision-point/outcome mechanism (Exploitation, Exposure,
Automatable, Human Impact, ...), and its distinctiveness from technical-severity and exploitability
scoring — are grounded in the overview tutorial page, which the same docs site publishes and which is
reachable from the home page. A single captured URL must ground the row (capture-binding rule B5: the
record's `url` equals the row's exactly-one `https://` token), so the row and capture point at the
overview page. The S054 row's `source` cell, the manifest record's `url`, and the capture file
`S054.txt` all use the corrected URL. No other claim literal, kill rule, or counter changes. C1 is
untouched. Filed 2026-10-26T14:04Z, before the kasegi-r37-build seats began scoring; every seat
prompt's URL is steered to this value by the L1 message.
