# R47RevEntryQ — F30 QUALITY review

Axes: depth:verifiability; coverage.

## Scope and availability

The assigned `R47SrF30Entry.md` and `.draft/` were absent: directory read showed only `swarm-registry.json`; a subsequent glob for `.ufo/waves/round-47/w1/R47SrF30Entry*` returned `No files found matching pattern`. Per the assignment, this reviews the frozen C2 claim shape, not an imaginary entry or integrated diff. No admission verdict is issued.

LSP unavailable: `read xd://lsp` returned `No such tool: xd://lsp`. References below are direct textual evidence, not semantic-reference proof.

## Findings, by severity

### Low — disambiguate “never cite it as a vendor clock” before copying the decision rule

Evidence: `.ufo/waves/round-47/claims.json:37` proposes “a broker deadline is broker-controlled with no stated start event; never cite it as a vendor clock”. The pinned source explicitly says ZDI “will allow the vendor four months (120 days)” (`corpus/source-snapshots/round-47/S075.txt:24`), and assigns vendors 30/60/90-day windows for faulty-patch cases (`:25`). Thus it *is* a deadline applicable to a vendor, although it is not the vendor's own disclosure policy. Without defining “vendor clock”, the proposed rejection can reject an accurate attribution as well as the intended over-generalization. This is a wording risk in the planned rule, not proof that an absent entry fails Q4/Q5.

Recommendation: say “ZDI-set vendor-remediation window, not evidence of the vendor's own disclosure policy”; retain the narrower observation that this page supplies no explicit start event. Keep the conditions: `S075.txt:24` conditions the 120-day allowance on a timely vendor response and limited-advisory publication on lack of response or a reasonable explanation. Do not turn the shorthand “limited-advisory publication at deadline” (`claims.json:36`) into unconditional publication.

## Q1–Q6 evidence and remaining obligations

- **Q1:** No entry header exists to inspect. The exact runnable core required by `corpus/instruments/r47-f30-gate.py:109-111` is:
  `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-47/manifest.json --source S075`
  Its regex permits only the specified restricted trailing comment. `:225-228` checks the first eight live lines; QUALITY Q1 (`corpus/QUALITY.md:14`) is stricter about placement directly under H1. Gate acceptance alone would not prove that placement.
- **Q2:** C2 promises sole tier-A S075 support (`claims.json:37`). The manifest identifies the first-party ZDI policy URL and fetch instant (`corpus/source-snapshots/round-47/manifest.json:6-16`). This is not evidence that the absent Registry row or every future claim is correctly supported. Cross-references to F02/F15 must remain comparisons rather than substitute authority for ZDI policy.
- **Q3:** All ten manifest quote strings are within 25 whitespace-delimited words and anchored in the declared body. Static JSON count output: `Q1 words=24 anchor=21; Q2=17/23; Q3=22/24; Q4=21/24; Q5=21/24; Q6=23/24; Q7=16/25; Q8=10/25; Q9=14/25; Q10=20/26`. The strings were read against `S075.txt:21-26`; no fabricated span was identified. This does not establish that every load-bearing sentence in a future entry has its own located quote. Manifest quote records are at `manifest.json:24-74`.
- **Q4:** The claim identifies ZDI and does not promise universal policy authority. Preserve “may” and the exhausted-contact condition for the fifteen-business-day fallback (`S075.txt:23`), rare sole-discretion extensions (`:24`), and the faulty-patch-only scope of 30/60/90 days (`:25`). The claim-shape ambiguity above is the only actionable wording issue identified.
- **Q5:** The proposed rule and rejected over-generalization are named at `claims.json:37`, but no actual package rule or rejection rationale can be evaluated without the draft. A locally checkable documentation rule could reject a package that attributes a specific clock-start event to this page, because `S075.txt:24` does not state one. This is a suggested testable formulation, not evidence that it is implemented.
- **Q6:** Reviewed claim text and manifest quotes contain no probing/submitting instructions or credential material. The source's contact-mechanism paragraph (`S075.txt:22`) is evidence text, not authorization to reproduce operational instructions. Keep the entry within the declared exclusion of submission pages, rewards and advisories (`claims.json:37`).

## Do-nothing discrimination and limits

Named do-nothing control: `.ufo/waves/round-47/controls/c2-base.txt:1-9`: H1/H2/H3/H4/H5/H6 fail, H7 passes, `f30-gate fixed=1/7 exit=1`, `EXIT=1`. In particular H2 and H5 explicitly report `entry-absent`; a claim alone does not pass as an entry. This is an inspected frozen receipt, not a new counter run. The freeze-tree 2/7 reading is separately disclosed at `claims.json:50`.

No counter or battery was run; no live page was reopened; no integrated tree, actual entry, actual recheck line, rendered table, or final caller set was available to verify. `claims.json:41` and `controls/freeze-controls.txt:3` disclose C2 18 surviving counter mutants (21 total/3 caught), C1 16 survivors; none is treated as closed. No runtime/rerouting/saturation/resume-continuity claim is made by this documentation-only scope.

No production edits, git/jj mutations, installs, delegation, background jobs, or scratch files/directories were made. Only this report was written.

Self-check: accuracy 4/5 and completeness 4/5 because entry bytes and live-source verification are unavailable; clarity 4/5 because fallback obligations necessarily differ from actual findings; actionability 4/5 because the low-severity wording recommendation still needs the real draft; conciseness 4/5 because Q1–Q6 evidence is retained separately. Overall 4.0/5. Highest-impact improvement is review of the actual entry once available, not promotion of this fallback review into admission evidence.
