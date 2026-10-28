VERDICT: DRAFT-READY

Scope: C2 entry drafter A (F28, GitHub private vulnerability reporting, reporter flow). Draft only: `.ufo/waves/round-46/wave1/R46ScribeEntryA.draft/github-private-vulnerability-reporting.md` (8830 bytes). No commit, no git mutation, no shared file touched, no other draft read. C1 was not in this seat's item and was not worked. Scratch `/fast/scratch/hyaku/kasegi-r46/R46ScribeEntryA/` removed on exit.

## 1. Source read (S073)

Command: `sed -n '563,566p;573,575p;577,579p' corpus/source-snapshots/round-46/S073.txt` (run in the lane root). Output (verbatim, abridged to the cited sentences):
- 564: "Private vulnerability reporting is separate from a repository’s SECURITY.md file. You can only report vulnerabilities privately for repositories where this feature is enabled. If the repository has a security policy, the policy is displayed above the reporting form ..."
- 566: "If the repository doesn't have private vulnerability reporting enabled, you need to initiate the reporting process by following the instructions in the security policy for the repository, or by creating an issue asking the maintainers for a preferred security contact. ..."
- 573: "By default, you must provide a summary, details, proof of concept, and impact statement. Maintainers can customize the form and require other information. ..."
- 574: "Optionally, select I used AI assistance to find or write up this report."
- 575: "... GitHub will display a message letting you know that maintainers have been notified and that you have a pending credit for this security advisory."
- 577: "When the report is submitted, GitHub automatically adds the reporter of the vulnerability as a collaborator and as a credited user on the proposed advisory."
- 578: "... Note that only the repository maintainer can merge changes from that private fork into the parent repository."
- 579: "The next steps depend on the action taken by the repository maintainer. See Managing privately reported security vulnerabilities."
Also `sha256sum corpus/source-snapshots/round-46/S073.txt` printed `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930` (matches the pin).

## 2. Draft self-check (quote → verified line)

Counter-equivalent check run by `python3 -B selfcheck.py` (exec of the frozen `r46-c2-gate.py` functions, entry path patched to the draft; no bytecode written). Per-quote result: all 14 curly spans cited and located, 0 failed, 0 uncited, word counts 9–24 (≤25):
- L564 "You can only report vulnerabilities privately for repositories where this feature is enabled." (13 words, located=1)
- L564 "Private vulnerability reporting is separate from a repository’s SECURITY.md file." (10, located=1; curly apostrophe kept inside the span)
- L573 "By default, you must provide a summary, details, proof of concept, and impact statement." (14, located=1)
- L573 "Maintainers can customize the form and require other information." (9, located=1)
- L574 "Optionally, select I used AI assistance to find or write up this report." (13, located=1)
- L575 "GitHub will display a message ... pending credit for this security advisory." (24, located=1)
- L577 "GitHub automatically adds the reporter ... on the proposed advisory." (20, located=1)
- L578 "only the repository maintainer can merge changes from that private fork into the parent repository." (15, located=1)
- L566 "by following the instructions in the security policy for the repository" (11, located=1)
- L566 "creating an issue asking the maintainers for a preferred security contact." (11, located=1)
- L579 "The next steps depend on the action taken by the repository maintainer." (12, located=1)
- L565 "If a public repository has private vulnerability reporting enabled, anyone can submit a private vulnerability report to the repository maintainers." (20, located=1)
- L564 (second quote, repeated in the falsifiable rule) and L566 (second, repeated in rule) — same spans as above.

Required quotes, one per required item:
- private only where enabled + separate from SECURITY.md: L564 (two quotes above).
- default fields summary/details/PoC/impact: L573.
- optional AI checkbox: L574.
- automatic collaborator and credited user: L577.
- only maintainer merges from the private fork: L578.

## 3. Gate-equivalent results on the draft

Command: `python3 -B selfcheck.py`; output (verbatim):
- `g2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 table-rows=8 xrefs=5/5`
- `g5 pass=1 read=spans=14 located=14 failed=0 uncited=0 cores=5/5`
- `g4 pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0` (the counter's own call to source-recheck.py on manifest S073; real tool, read-only)
- `curly-quotes total 14 cited 14`

Not run: G1, G3, G6, G7 need the F28 row in corpus/README.md, the S073 row in corpus/SOURCES.md and the entry placed in corpus/knowledge (65 files); those are integration edits for the L1, which this seat does not make. The entry path was patched only for G2/G5.

## 4. Falsification of the draft's checks (mutants on the draft text)

Command: `python3 -B mutants.py` (mutated copies written only to scratch; output verbatim):
- fabricated-quote (the 573 quote with "and a CVE number" added): `g5 pass=0 read=spans=14 located=13 failed=1 uncited=0 cores=4/5`. Red.
- drop-core-5 (the 578 core replaced): `g5 pass=0 read=spans=14 located=13 failed=1 uncited=0 cores=4/5`. Red.
- uncited-curly (a stray curly phrase appended): `g5 pass=0 read=spans=14 located=14 failed=0 uncited=1 cores=5/5`. Red.
- bad-xref-line (kernel :23-24 changed to :999): `g2 pass=0 ... xrefs=4/5`. Red.
- no-ai-xref (both AI-validation refs replaced): `g2 pass=0 ... xrefs=3/5`. Red.
Unmutated draft: g2 and g5 green. So the gate's G2/G5 logic discriminates the draft from these mutants.

## 5. Overlap references (verified line numbers)

- `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md:23` — row "Does an AI-assisted find stay private?" (`sed -n '23p'` printed that row); `:24` — reproducer row.
- `corpus/knowledge/ai-assisted-finding-validation.md:7` ("Treat an AI-originated finding as a candidate..."), `:8` ("For Kasegi claim-ready status, the package must identify ... a reviewer distinct from its producer"), `:14`–`:15` (validation record list).
- `corpus/knowledge/authorization-safe-harbor-and-scope.md:8` ("A safe-harbor badge or statement alone does not add assets to scope ...").
- `corpus/knowledge/vendor-third-party-finding-coordination.md:91` (rule item 2, "The vendor stated as coordinator itself").
- The knowledge directory has 64 files in the lane tree (`ls corpus/knowledge | wc -l` → 64), consistent with the freeze.

## 6. Limits

- Sweep for what the page does NOT say: `sed -n '556,583p' corpus/source-snapshots/round-46/S073.txt | grep -inE 'CVE|reward|bount|timeline|embargo|days|weeks|triage|publish|disclos'`. Output: a single line `11:` (S073 line 566), the link name "Coordinated disclosure of security vulnerabilities". No CVE request, timeline, reward or triage duty appears in the body. The entry says so and does not infer them.
- The draft cites only the pinned capture; no live fetch was made. The `recheck:` line re-verifies the capture bytes and pinned quotes, not the live page.
- The falsifiable rule and the table use only the page's words plus labelled derivations (e.g., "an unselected box is not evidence of no AI use" follows from "optionally"); they are consequences, not quotes.
- The F27 contrast states what each page says; it does not assert either project's policy is the other's.
- Not verified: the L1's integration (F28 README row, S073 SOURCES row, corpus/knowledge placement, G1/G3/G6/G7). The draft's entry bytes ≥ 3000 (G6 size rule) are met by 8830 bytes but the full-tree counter was not run.

## 7. Installs

None.
