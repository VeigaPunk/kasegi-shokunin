VERDICT: BROKEN

Seat: R46W2RevRegistry (read-only reviewer, registry and admission). Tree: lane corpus, PROVINCE.md and README.md are byte-identical between commit 5437afeaf9b642c267bba3c31f00ae701e49da68 and the working tree (`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin diff --stat 5437afeaf9b642c267bba3c31f00ae701e49da68 -- corpus PROVINCE.md` printed nothing; `git status --porcelain -- corpus PROVINCE.md README.md SKILL.md` printed nothing). Lane HEAD is 0d121a2, a descendant of 5437afe that changes no corpus file. Base is 914ca0b6 (exported with `git archive` into scratch as the control).

Summary: the registry data holds. The S073 row, the census, the quotes, the capture digests and the F28 frontier count all re-derive from commands I ran. The falsifications are: (D1) the F28 Search-log counts do not reconcile with the items they list; (D2) the round-46 `## Gate` record that CORPUS.md requires does not exist yet, so the landing gate is open; plus shape and attribution defects D3-D9 below.

## Holds (each re-run by me)

H1. Validator. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` printed:
  kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
  kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
  kasegi	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
  kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
  exit=0. Only W04 warnings, no E-codes.

H2. The seven manual census commands of CORPUS.md:135-147 (transcribed verbatim, then diffed against the CORPUS.md text: `IDENTICAL (7 commands)`), run from the lane root:
  C1 rows: 73 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`)
  C2 malformed: 0
  C3 tier: `A=66 B=4 C=3`
  C4 status: `mined=58 rejected=15`
  C5 duplicate ids: (empty)  C6 enum/tier inflation: (empty)  C7 mined used-by missing: (empty)
  Row total 73 = 66+4+3 = 58+15.

H3. Do-nothing control, the base export at 914ca0b (`git archive 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba | tar -x`), with the same seven commands:
  C1 rows: 72; C3 `A=65 B=4 C=3`; C4 `mined=57 rejected=15`; C2, C5, C6, C7 empty.
  The delta is exactly one row (S073, tier A, mined). The base SOURCES.md sha256 is beeef08efdb24f3158a82ee4435b07b9973763bb1af3844037867b4a471208fa, identical to the pure export at /fast/scratch/hyaku/kasegi-r46/L1/pure.

H4. The census is sensitive (mutation fixtures in scratch, not the lane). Tier cell set to ` D `: C3 printed `A=65 B=4 C=3 D=1` and C6 printed `tier S073 D`. Trailing pipe removed from the S073 row: C2 printed `1`. used-by set to `corpus/knowledge/does-not-exist.md`: C7 printed `missing: corpus/knowledge/does-not-exist.md`.

H5. Append-only (CORPUS.md SOURCES rule 2). `diff <base>/corpus/SOURCES.md corpus/SOURCES.md` shows three additive hunks only: `78a79` (S073 row), `108a110,111` (F28 Search-log bullet), `156a160,162` (S073 Registry-changes bullet and supersede-pair bullet). `grep -c '^<'` over that diff printed `0`. README: 0 lines removed, 15 added. PROVINCE: 0 removed, 2 added at 170-171.

H6. S073 capture figures. `wc -l corpus/source-snapshots/round-46/S073.txt` = 589; `wc -c` = 15568; `sha256sum` = 66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930. manifest.json: `"bytes": 577188`, `"snapshot_bytes": 15568`, `"lines": 589`, `"fetched_utc": "2026-10-28T22:56:49Z"`, `"status": 200`, `"final_url"` equal to the row URL. All match the row, the bullet and the manifest.

H7. Quotes. Every manifest quote is at its anchor line verbatim (`grep -nF`): 560 "Anyone can privately report…", 563 "create a draft security advisory directly", 564 "You can only report vulnerabilities privately for repositories where this feature is enabled.", 566 "you need to initiate the reporting process…", 573 "By default, you must provide a summary, details, proof of concept, and impact statement.", 574 "Optionally, select I used AI assistance…", 577 "GitHub automatically adds the reporter…", 578 "only the repository maintainer can merge…". The registry quote (SOURCES.md:161, 13 words, `S073.txt:564`) counts to 13 words, within the ≤25 limit. `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073` printed `S073:sha256 OK` and Q1-Q8 `OK ... anchor=<n>-ok`, exit 0.

H8. Anchor line numbers. Line 556 is the heading "Privately reporting a security vulnerability"; 557-583 is the body; 561 enablement sentence; 564 SECURITY.md separation; 568 "Security and quality tab"; 573 default fields; 575 submit; 578 temporary private fork. All match the bullet and the knowledge entry.

H9. The legacy URL in the row and Search-log. I re-ran it (documentation lookups, not a target test): `curl -sIL -A 'kasegi-shokunin/1.0' -w 'legacy: final=%{url_effective} status=%{http_code} redirects=%{num_redirects}\n' <legacy URL>` printed `legacy: final=https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately status=200 redirects=1`; canonical printed `status=200 redirects=0`. Matches "HTTP 200, 1 redirect, final URL equal to the canonical URL".

H10. Search-log sweep re-run. On the base export: `grep -rliE 'private vulnerability reporting|privately report' corpus/knowledge corpus/SOURCES.md corpus/README.md` printed nothing, exit 1 (64 knowledge files, `find corpus/knowledge -maxdepth 1 -type f -name '*.md' | wc -l` = 64). The pure export gave the same empty result and exit 1. `grep -c 'docs.github.com' <base>/corpus/SOURCES.md` = 0. Held rows: S065 rejected tier A, S068 rejected tier B (SOURCES.md:71, :74).

H11. F28 frontier count. `grep -oE '^\| F[0-9]{2} \|' corpus/README.md | sort -u | wc -l` = 28; duplicates = 0; ids F01..F28 contiguous. `python3 corpus/instruments/frontier-recheck-count.py --root <lane>` (no --json, so no receipt written) printed `FRONTIER-PASS F28 ids=S073` and `entries=31 pass=31 exit=0`.

H12. knowledge-expected.txt. The non-comment list equals the `corpus/knowledge/*.md` listing (`diff` empty); 65 = 65 files. The one new line sits between `ev-model.md` and `google-cloud-vrp-customer-resource-boundary.md`. recheck-audit.py reads this file (its `--root` default path, line 372).

H13. Manifest binding. `python3 corpus/instruments/capture-binding-check.py --root <lane>` ends `AUDIT records=60 with_url=60 ... orphans=1 orphan=S040-live.txt` and `records=60 bound=60 unbound=0`, exit 0. The round-46 manifest record is `records=1 url_bound=1 fetched=1`.

H14. Admission prose vs page. Each claim in README.md:658 and PROVINCE.md:171 traces to S073.txt: public-repository enablement (561), SECURITY.md separation (564), Security and quality tab (568), default fields "By default" (573), optional AI disclosure (574), collaborator and credit (577), maintainer-only merge (578). The scope limits (maintainer handling, GHSA database, CVE assignment) match the page's silence. I found no broader-than-page claim in the admission text.

H15. Knowledge entry back-link. corpus/knowledge/github-private-vulnerability-reporting.md opens `source: S073`, `verified-at: 2026-10-28`, `recheck: ...source-recheck.py --manifest ... --source S073 # 180d` (the provenance trio, in order). Its recheck command passes (H7). The census used-by path resolves (H2 C7).

## Defects

D1 (medium, falsified). SOURCES.md:110, F28 Search-log bullet. Quoted text: "identified 1 primary page plus 1 legacy redirect URL (sweep returned 0 files); screened 3 (the primary page, the legacy URL and the 2 held rows); included 1 (S073); excluded 2 (S065, S068…)". The listed screened units are four (primary, legacy URL, S065, S068), not three. Identified is 2 (1+1), so it disagrees with screened 3 and listed 4. Included 1 + excluded 2 = 3, so the legacy URL is unaccounted. "sweep returned 0 files" conflicts with "identified 1 primary page": the page came from the fetch, not the sweep. CORPUS.md Search-log rule 5 requires identified / screened / included / excluded counts that reconcile. Fix: state the enumerated units and their counts consistently (for example identified 4, screened 4, included 1, excluded 3 with the legacy URL marked as a redirect of S073), and say the page came from the fetch.

D2 (landing gate open, falsified). CORPUS.md SOURCES contract rule 1: "The round lesson's `## Gate` records, for every new row, the URL, the access date, and a ≤25-word quote with its location grounding `teaches`." `ls corpus/lessons/round-46.md` printed `No such file or directory`. The round-45 precedent is corpus/lessons/round-45.md:21 `## Gate — frontier, source, and rejection`, which holds the S071/S072 gate. The S073 gate facts currently appear only in SOURCES.md:79 and :161. Required action: the L1 writes corpus/lessons/round-46.md with `## Gate` covering S073 (URL, access date 2026-10-28, quote at S073.txt:564 with location). Not landable until this exists.

D3 (low, shape drift). PROVINCE.md:171 reads `[r46 Frontier amendment, appended 2026-10-28] F28`. Every earlier amendment carries the marker: PROVINCE.md:169 `[r45 Frontier amendment, appended 2026-10-28, end-of-file append per R6] F27`. Fix: add `, end-of-file append per R6`.

D4 (low, shape drift). README.md:655 heading `## Round-46 admission - coverage map row and Frontier F28 (appended 2026-10-28)` uses an ASCII hyphen. README.md:634 uses an em dash (`cat -A` shows `M-bM-^@M-^T`). Fix: use the em dash.

D5 (low-medium, CORPUS "a count carries its command"). README.md:668 "28/28 admitted" and README.md:668 "the lost-domain denominator remains 0/18" carry no `<number> — <command> <date>` form, which CORPUS.md:34-38 requires. The 28 re-derives with the command in H11 (I did not add it to the text). The 0/18 is carried from README.md:215 ("0/18 surfaces are present") and I did not re-derive it here. Round 45's `27/27` line has the same shape, so the template carries the defect forward; fix it in the admission template, not only here.

D6 (nit, wrong line description). SOURCES.md:79 anchor cell says "body lines 556-583". Line 556 is the heading, and SOURCES.md:161 says "heading L556, reporter-flow body L557-L583". Fix: "heading L556, body L557-L583" in the row or drop the 556.

D7 (low-medium, unsourced claim and misnamed reference). SOURCES.md:162 supersede-pair bullet, in Registry-changes, states "(spot-check item 4)" and "the two held duplicates S028 and S029 are pre-existing deliberate duplicates". (a) corpus/lessons/round-45-verifier-spotcheck.md:78-83 has an unnumbered table; its fourth data row (line 83) is the S072 key-quote ≤25-word check, not the supersede pair. So "item 4" does not point where the note implies. (b) Nothing in the lane shows that S028/S029 are "deliberate"; `grep -niE 'deliberate' corpus/SOURCES.md` finds only SOURCES.md:101 (a different sweep) and this bullet. (c) The bullet changes no row, so it sits oddly under Registry-changes. Fix: cite the round-45 row number correctly, drop "deliberate" unless a source says so, and move the note to the Search-log or the round-46 lesson.

D8 (low, pre-existing, not introduced by F28). corpus/instruments/knowledge-expected.txt header says "Sorted list". `LC_ALL=C sort -c` reports `disorder: corpus/knowledge/ev-model.md` at line 28, and the base file shows the same. The F28 line is in order relative to its neighbours. Not caused by this round; record it as a known gap.

D9 (low, reproducibility). SOURCES.md:110 cites `/fast/scratch/hyaku/kasegi-r46/L1/pure` as the search base. That is a scratch path that later readers cannot see. The same sweep reproduces on the committed base 914ca0b (H10, exit 1), so cite the commit, not the scratch copy.

D10 (note for L1, not a lane defect). The pure export at /fast/scratch/hyaku/kasegi-r46/L1/pure contains `corpus/instruments/__pycache__/` that is absent from `git archive 914ca0b`. It was produced by a run inside the "pure" copy. It does not change any SOURCES figure (sha identical), but "pure" is no longer pure.

## Round-45 shape comparison

- Round-45 block (README.md:634-653): heading, paragraph, Area table, id table, amendment line. Round-46 block (README.md:655-668) has the same five parts. Differences are D3, D4 and the longer paragraph.
- S071/S072 (round 45) had no Registry-changes bullet; their Gate lives in corpus/lessons/round-45.md. S073 has a Registry-changes bullet and a Search-log bullet, which CORPUS.md rule 5 supports. The round-46 lesson is still missing (D2).
- Round-45 amendment wording: "[r45 Frontier amendment, appended 2026-10-28, end-of-file append per R6]" vs "[r46 Frontier amendment, appended 2026-10-28]" (D3).

## Verification gaps and limitations

- The lane HEAD is 0d121a2, not 5437afe. I compared the corpus, PROVINCE and README bytes; I did not review the wider tree.
- The legacy and canonical URL checks (H9) are live HEAD requests to docs.github.com, made as documentation lookups. Their results are dated to the run and can change. I made no other network requests.
- The instrument UA (`kasegi-shokunin/1.0`) named in the Search-log bullet is not recorded in manifest.json, so I could not verify it from the lane.
- Manifest `bytes: 577188` is a field I read, not a file I measured; the raw capture is not in the lane.
- I did not review the knowledge entry's body beyond its provenance trio, back-links and recheck line; the entry's content belongs to the entry seats. I did not run the full recheck-audit.py.
- Mutation fixtures (H4) and the base export were built in scratch and removed on exit. The lane was not written to.
- The `grep -c 'round 45'` on the base SOURCES.md printed 0: round 45 added no Search-log bullet, so the F28 bullet has no round-45 twin to compare.
