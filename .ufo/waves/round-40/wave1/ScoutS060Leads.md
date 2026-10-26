# ScoutS060Leads receipt (round 40)

Item: open the two planned leads and decide row / reject / fold. Deliverable: ScoutS060Leads.txt (22 lines, sha256 96dc0c268eacd3e802f1e78c2439e5683a4eb2cf3ab2196c5e39f9d42e3695c5), beside this receipt.

## Outcome
1. CISA VEX Status Justifications (June 2022): the lead URL is HTTP 404. The real publication page (200, 56383 B) and PDF (200, 313386 B, sha256 9a4027c6...cf0513f) exist. Recommendation: OPEN ROW (docs, tier A, anchor the PDF). S055 only cites it as [VEX-Justification] and copies the labels; the lane knowledge entry carries none of its section 3.3-3.7 definitions, 3.7.3 distinction or flowchart (grep printed nothing).
2. OASIS CSAF v2.1: the page exists (200, 1231332 B) but is Committee Specification Draft 04 (21 October 2026); the directory has csd01-csd04 and schema, no os/; os/ probes return 404. The flip monitor has not fired. Recommendation: REJECT with flip (os/csaf-v2.1-os.html returns 200 reading "OASIS Standard"); optional draft-drift note on S055 (nine product_status properties in csd04).

## Commands run (all curl -sS -L --max-time 90 -A kasegi-shokunin/1.0, from scratch dir)
Fetch ledger with HTTP status / bytes / sha256 / UTC time is in the deliverable lines per URL. Derived texts: cisa.txt via pdftotext -layout (sha256 2b480ac8...df4e6, 274 lines); csaf21.txt = tag-stripped HTML (sha256 626cac7f...473158). Located lines: cisa.txt L46, L208-209; csaf21.txt L498, L7611; S055.txt L485 (cites the PDF), L1762 (MUST) versus csaf21.txt (SHALL, "The values SHALL be used as follows").
Lane reads only: corpus/SOURCES.md rows S055-S059, round-39 lesson L45-47 (the candidates-not-taken lines), knowledge entry grep.
Disk guard status: green (/tmp 3%, /var/tmp 35%, /fast/scratch/hyaku 27%).
web_search was used once to find the working CISA URL after the lead URL 404ed (found the resources-tools path and the PDF; both then fetched directly).

## Tools installed
None.

## Caveats
- Round-39 lesson L45-47 lists the CISA lead as moved to "Leads (unopened)"; this seat did not edit it.
- The "eight lists" for S055 is the S055 row's own wording; not re-derived from the v2.0 text this round.
- No capture was written into the lane (out of write scope); the L1/ScribeNewRows must capture the PDF under source-snapshots/round-40/.
