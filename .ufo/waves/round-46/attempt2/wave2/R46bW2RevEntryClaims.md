# R46bW2RevEntryClaims — attack on corpus/knowledge/github-repository-security-advisories.md

Seat: R46bW2RevEntryClaims (leaf, no delegation)
Tree under attack: lane commit fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4 (integration of wave 1)
Ground: corpus/source-snapshots/round-46-a2/S074.txt (sha256 re-verified 1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039, 42 lines, 7087 bytes)
Item: every quote located (<=25 words, range holds); F28/F07 contrasts actually stated; decision rule actionable; Limits honest about sibling pages.

VERDICT: HOLDS

## Re-run evidence (nothing trusted; every command re-executed)

1. Snapshot integrity: `sha256sum corpus/source-snapshots/round-46-a2/S074.txt` -> `1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039`; `wc -l` -> 42. Matches entry header and manifest exactly.
2. Instrument re-run: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074` -> `S074:sha256 OK`, Q1..Q9 each `OK occurrences=1 anchor=...-ok`, exit 0.
3. Quote audit (scratch script, per-line pairing + full-text pass over all 45 curly-quoted spans): every span located verbatim in S074.txt at the cited line; 0 missing from snapshot; max span 22 words (Q8), all <= 25. Multi-line-wrapped Limits quotes verified individually with `grep -F`: "REST API endpoints for repository security advisories" -> line 16; "Editing a repository security advisory" -> line 34; "Editing security advisories in the GitHub Advisory Database" -> line 19; "The security advisory form on GitHub is a standardized form..." -> line 23; "You can also use the REST API to create, list, and update repository security advisories." -> line 16; "The URL of a security advisory does not change after publication." -> line 33. All match the entry's citations.
4. Live page (read-only curl 2026-10-29): 582877 bytes, identical size to capture-time HTML in manifest; all entry quotes present in raw live HTML (3 apparent misses in naive text extraction were `<strong>` wrapping artifacts, confirmed present in raw markup, e.g. "Whenever possible, you should <strong>add a fix version to a security advisory prior to publishing the advisory</strong>").
5. F28 contrast — `sed -n` of corpus/knowledge/github-private-vulnerability-reporting.md:
   - :9 "This entry records one reporter-side flow: GitHub's documented route for a person who wants to report a security vulnerability privately to a repository's maintainers." (as entry claims)
   - :23 table row "Who can merge a fix from the temporary private fork?" with "Note that only the repository maintainer can merge changes from that private fork into the parent repository." (as entry claims)
   - :40 "The page does not state the maintainer-side flow, CVE requests, timelines or rewards." (entry cites :39-40; holds)
6. F07 contrast — `sed -n` of corpus/knowledge/cna-assignment-and-vulnerability-rules.md:
   - :9-13 "A local CVE-request package review separates technical vulnerability determination, CNA assignment scope, and identifier counting." (as entry claims)
   - :32 row 3.1.1 "CNAs MUST develop, document, and operate within a Scope Definition" (as entry claims)
   - :36 row 4.2.1.1 "The CNA with the most appropriate scope MUST be contacted and given the first opportunity to assign." (as entry claims)
7. Third contrast — corpus/knowledge/coordinated-disclosure-timelines.md:7-8: timeline must name policy/coordinator, clock trigger, interval, patch/publication relationship; "Do not describe one interval as the universal researcher deadline." (as entry claims).
8. Limits sweeps re-run: `grep -n -i -E 'timeline|embargo|deadline|reward|bount' S074.txt` -> no output, exit 1 (entry's claim "printed nothing (grep exit 1)" reproducible); `grep -n -i -E 'private repub|enterprise'` -> exit 1 (nothing about private repositories or Enterprise, as Limits state); line 25 ends "Anyone with admin permissions to a security advisory can request a CVE identification number." (supports Limits' "nothing about who may request a CVE beyond administrators").
9. Two-clock claim: CVE-request clock S074.txt:25 ("GitHub usually reviews the request within 72 hours.") vs post-publication Dependabot clock S074.txt:36 ("This process can take up to 72 hours and GitHub may contact you for more information.") — both present, distinct, correctly not merged by the entry.
10. Sibling-page honesty: Limits name four sibling pages, each quoted as link text and each verified located — "Creating a repository security advisory" (:17), "REST API endpoints for repository security advisories" (:16), "Editing a repository security advisory" (:34), "Editing security advisories in the GitHub Advisory Database" (:19). The capture holds none of their bodies; the claim "Each appears in the capture as link text only" holds.
11. Decision rule actionability: the numbered rule (draft before publish :12; fix in temporary private fork :13; fix version before publish :38; CVE request while private :25 with assigning body :24) plus the four-step "Falsifiable package rule" each name a checkable fact against a quoted line, including failure modes ("A package that records only a published advisory fails this step", "treats the CVE request as the publication event fails"). Discriminates against a do-nothing control: a mere restatement of the page would lack the ordered falsifiable checks and the publication-visibility split (:31 vs :32); this entry has both.

## Findings (defects)

1. LOW — entry line 89 (Limits bullet 1): "S074.txt:1-42 is the whole capture and all 42 lines are body prose". Capture lines 1 ("In this article"), 4 ("Copy markdown") and 7 ("## In this article") are page chrome/navigation furniture, not body prose (verified by `sed -n '1p;4p;5p;7p'`). No quote, rule, or table row depends on those lines, so the defect is cosmetic — but the sentence is factually inaccurate, and the sibling F28 entry (github-private-vulnerability-reporting.md) explicitly segregates chrome (S073.txt:580-583). Capture line range 1,4,7 vs entry line 89.
2. LOW — entry line 16: the decision rule is introduced as "in the order the page states it", but the capture's statement order is draft (:12) -> private fork (:13) -> publish (:14) -> CVE request/72-hour review (:25) -> fix-version duty (:38). The entry numbers fix version as step 3 (line 20) and CVE request as step 4 (line 21), the reverse of the capture order. The rule itself is actionable and correctly sourced; only the ordering meta-claim is wrong. Capture lines 25,38 vs entry lines 16,20,21.

## Limitations of this review

- Live-page check was read-only and structural (byte size + raw-HTML substring presence of quotes); it did not re-run the corpus text extraction pipeline against the live HTML.
- Word-count and location audit used exact substring matching after whitespace normalization; no fuzzy matching was needed (all spans matched exactly).
- The two LOW findings were not re-checked against the f29-gate instrument (out of this seat's scope; gate grading belongs to the gate seats).
- No mutations performed; scratch removed on exit.
