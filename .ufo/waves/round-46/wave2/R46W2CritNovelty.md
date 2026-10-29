# R46W2CritNovelty: novelty and value critic for C2 (F28, GitHub private vulnerability reporting)

VERDICT: HOLDS

Subject: `corpus/knowledge/github-private-vulnerability-reporting.md` (entry, sha256 prefix `47028299d797e332`), row S073 in `corpus/SOURCES.md`, capture `corpus/source-snapshots/round-46/S073.txt` (sha256 `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930`, 589 lines, 15568 bytes).

Tree under test: the lane HEAD is `0d121a2` (wave-2 spec commit). It descends from `5437afeaf9b642c267bba3c31f00ae701e49da68`. `git -C <lane> diff --stat 5437afe -- corpus` printed nothing, so the corpus bytes under test equal the committed `5437afe` bytes. I exported `5437afe` with `git archive` into scratch and ran everything there. Base identity: the pure export's `corpus/SOURCES.md` and `SKILL.md` sha256 prefixes equal those of `914ca0b6` (`beeef08efdb24f31`, `a7c4d818300df64e`).

## Finding 1: the entry adds answers the base corpus cannot give (verdict-bearing)

Command (base export, knowledge pages, one pattern per line, counts from `grep -rliE`):

```
Q1  private vulnerability reporting|privately report|report privately|private reporting     base-corpus=0 base-knowledge=0
Q2  SECURITY\.md|security policy for the repository                                        base-corpus=0 base-knowledge=0
Q3  preferred security contact|creating an issue asking|security contact                   base-corpus=2 (snapshots S008,S021 only) base-knowledge=0
Q4  proof of concept, and impact statement|summary, details|...provide a summary           base-corpus=0 base-knowledge=0
Q5  credited user|pending credit|as a collaborator                                          base-corpus=0 base-knowledge=0
Q6  private fork|temporary private                                                          base-corpus=0 base-knowledge=0
Q7  I used AI assistance|AI assistance to find                                              base-corpus=0 base-knowledge=0 (kernel F27 has a different AI rule, see Finding 3)
Q8  maintainers have been notified|GitHub will display a message                           base-corpus=0 base-knowledge=0
Q9  public repositories configure|enable private vulnerability                              base-corpus=0 base-knowledge=0
Q10 GitHub.{0,120}(within [0-9]+ days|timeline)                                             base-corpus=0 base-knowledge=0 (grep exit 1)
Q11 Creating a repository security advisory|draft (security )?advisory                      base-corpus=0 base-knowledge=0
Q12 anonymous(ly)?                                                                          base-corpus=11 base-knowledge=2 (cisa-bod-20-01-vdp-minimums.md, policy-access-playbook.md; not GitHub)
```

Questions the entry answers that the base cannot (11), with the entry location:

1. Is GitHub private reporting a route at all, and what enablement fact must a package record? Entry L13, L17, L49 step (1).
2. Is the repo's SECURITY.md a separate route from the private form? Entry L11, L18.
3. What route applies when the feature is not enabled? Entry L19, L49 step (2) (cites `S073.txt:566`).
4. What fields does the default form require? Entry L20 (`S073.txt:573`).
5. What does submission do to the reporter (collaborator, credited user), and what is left unknown? Entry L22 (permissions kept unknown).
6. Who can merge from the temporary private fork? Entry L23, L49.
7. Is the AI-assistance checkbox optional, and is its absence a non-claim? Entry L21 (`S073.txt:574`).
8. What confirmation does the reporter get, and does the page give a response time? Entry L24 (no response time).
9. Does the page cover private repositories? Entry L42 (page says nothing about them).
10. Is there a GitHub maintainer timeline? Entry L40 (page states none).
11. Do admin or security-permission holders need to submit a report at all? Entry L33 (`S073.txt:563`).

Do-nothing control: a reviewer with the base corpus has no held rule that rejects a claim saying a report went through GitHub private reporting. Q1 returns 0 hits at base. With the entry, the same claim fails rule step (3). That changes the outcome, so the entry is not a restatement of the page for reviewer purposes.

Counter-check: the page body alone answers Q1 to Q11 as text. The entry's added value is the pass/fail gate in column 3 of the table (L17-L24), the falsifiable rule (L49), and the unknowns (L40-L44). It is not the quotes.

## Finding 2: paraphrase audit of the entry

Sentences that only restate the page (no gate, no unknown):

- L9: scope sentence ("This entry records one reporter-side flow..."), a restatement of the page's title and intent.
- L11: three verbatim quotes (`S073.txt:561`, `:564`, `:564`).
- L17-L24, column 2 of each table row: eight verbatim page quotes (`:564`, `:564`, `:566`, `:573`, `:574`, `:577`, `:578`, `:575`). Column 3 of each row is new (gate or unknown).
- L33, last sentence: restates `S073.txt:563` ("concerns who may create a draft advisory").
- L39 and L45: scope restatements.

Sentences that carry the value: L13 (decision rule), column 3 of L17-L24, L30-L33 (cross-references to held entries), L40-L44 (limits), L49 (the rule).

## Finding 3: overlap audit (the entry's own "held elsewhere" list)

Each cited line was checked against the committed file:

- `linux-kernel-security-bugs-reporting-process.md:23` (F27): the kernel row gives the kernel's AI-assisted rule (`S071.txt:95-96`). The entry's "keeps its reproducer out of the public text" matches the kernel's `S071.txt:99` on sharing reproducers. Consistent.
- `ai-assisted-finding-validation.md:7-8`: matches (candidate until reproduced; reviewer distinct from producer). Consistent.
- `vendor-third-party-finding-coordination.md:17-19`: this is Microsoft MSVR's three intake routes, not a generic programme. Consistent.
- `authorization-safe-harbor-and-scope.md:8`: matches.

Omitted from the overlap list, though relevant to reporter intake (see Gaps G1-G2):

- `rfc-9116-security-txt.md` (security.txt as a machine-readable contact channel; "researchers shouldn't assume that the presence or absence of a \"security.txt\" file grants or denies permission for security testing", S063.txt:L571).
- `vdp-disclosure-packages.md` (intake via `security.txt` Contact to a HackerOne embedded-submissions form, "VDP intake can be the vendor's `security.txt` Contact route even when the vendor also runs a paid HackerOne program").
- `cisa-bod-20-01-vdp-minimums.md` (policy minimums including "A clear statement that reporters may submit a report anonymously." L125).

The entry's claim "None of the held entries records these as a reporter-side intake contract" is correct for the GitHub-specific items it lists (field list, collaborator effect, maintainer-only merge). The overlap list is incomplete at the boundary.

## Finding 4: falsifiable rule applied to a real public SECURITY.md, read-only

Fetch (read-only GET, saved to scratch):

```
curl -fsSL -o nodejs-SECURITY.md https://raw.githubusercontent.com/nodejs/node/main/SECURITY.md   -> exit 0, 38176 bytes, 738 lines
```

Quoted lines:

```
5:  Report security bugs in Node.js via [HackerOne](https://hackerone.com/nodejs).
7:  Normally, your report will be acknowledged within 5 days, and you'll receive
18: If you do not receive an acknowledgement of your report within 6 business
```

Grep for GitHub private reporting in the file: `grep -niE 'private|github|advisor|security\.txt|hackerone|...'` returned only HackerOne (L5, L82, L620, L623), GitHub code and team links, and "private security reports" team text. No line states that GitHub private vulnerability reporting is used or enabled.

Worked example (a constructed claim, not a real report): "a vulnerability in nodejs/node was reported through GitHub private vulnerability reporting."

- Step (1): the package must record an observed fact that the feature is enabled on nodejs/node. None is recorded. Reading SECURITY.md cannot supply it, because the enablement lives in the repo's settings, which I did not observe (see Limitations).
- Step (2): enablement absent, so the package must cite the security-policy route. The route is `SECURITY.md:5` (HackerOne), and the package must not call the report a private-reporting submission.
- Step (3): the claim names the feature with neither fact, so it fails as worded.

Result: the rule applies to a real policy text in its negative and fallback branch, without probing any system. It cannot confirm enablement from public reading. The positive branch needs an observed fact about the repo's settings, which the rule does not let public text supply.

Do-nothing control for the example: with no entry, no held rule rejects the claim (Finding 1, Q1 = 0 hits at base), so the same claim passes.

## Finding 5: gaps a reporter or reviewer would hit

- G1 (anonymity, unanswered and unflagged). The page does not say whether a report can be anonymous: `sed -n '556,583p' .../S073.txt | grep -niE 'anonym|identit|account'` printed nothing (exit 1). The entry does not mention anonymity: `grep -niE 'anonym|identit|pseudonym|GitHub account|username' <entry>` printed nothing (exit 1). Yet `S073.txt:577` says the reporter is added as collaborator and credited user, which links the report to a GitHub identity. The base corpus does record an anonymity policy minimum for VDP policies (`cisa-bod-20-01-vdp-minimums.md`, "A clear statement that reporters may submit a report anonymously." L125). The entry should list anonymity as an unknown under Limits.
- G2 (fallback channel incomplete). The entry's fallback is "the security policy" only (L19). `grep -niE 'rfc|9116|security\.txt|vdp|intake-surface|coordinated-disclosure' <entry>` printed nothing (exit 1). A claim citing security.txt as the fallback has no entry statement to check it against, although `rfc-9116-security-txt.md` and `vdp-disclosure-packages.md` are held.
- G3 (recheck overclaims). Limits L44 says the `recheck:` line "re-verifies the capture's bytes and quotes". It ran `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073` on the export and printed `S073:sha256 OK`, then `S073:Q1 OK ... Q8 OK` (eight quotes at anchors 560, 563, 564, 566, 573, 574, 577, 578), exit 0. The entry has 21 curly-quoted strings. A check I ran (normalized, whitespace-collapsed substring test against the capture) printed `quoted strings in entry: 21` and `missing: 0`. So all 21 match, but only 8 are guarded by an instrument. The other 13 (for example the L575 "GitHub will display a message..." quote and the L565 and L579 quotes) have no recheck.
- G4 (wording mismatch in the rule). L13 says "Where the feature is not enabled"; L49 step (2) triggers on "If that enablement fact is absent". Absent (unrecorded) and disabled (observed off) are different states, and the rule gives them the same consequence. That is harmless here, but a reviewer cannot tell which state applies.
- G5 (step 1 has no typed slot). `claim-package-contract.md` has no required field for a target repository's feature setting. The only observation field I found is `observed_at` on the policy scope excerpt (contract line 11). Step (1) therefore can only be satisfied as free prose in `report.md`. I did not check whether `claim-package-check.py` gates prose enablement claims.

## Limitations

- No live target was touched. I did not fetch any repository's Security tab, API or settings, because that is a probe of a live target, which is refused for this corpus. So the enablement of nodejs/node is not observed, and the positive branch of the rule is not exercised.
- Three further SECURITY.md URLs 404'd (expressjs/express at `main` and `master`, pallets/flask at `main`, psf/requests at `main`). The worked example rests on one repository.
- Overlap and absence were judged by string patterns. Semantic overlap outside those patterns could be missed.
- Base identity was checked with sha256 prefixes on two files (`SOURCES.md`, `SKILL.md`), not the whole tree.
- The "no response time" and "no timeline" claims were checked against the pinned capture only, not the live page.
- The constructed claim in Finding 4 is hypothetical. It exercises the rule; it is not a real submission.
- I ran no wave gate instruments (`r46-c1-gate.py`, `r46-c2-gate.py`); they are outside this seat.
