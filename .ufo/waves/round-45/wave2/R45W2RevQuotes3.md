VERDICT: HOLDS

# R45W2RevQuotes3 — F27 entry quote review 3 (curly-quoted spans 17–24)

Attacked object: `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` in the export of lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (exported with `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 6662a4276b6f7bd61e23e12058414e09dd71b9e4 | tar -x -C <scratch>/export`). Snapshot checked: `corpus/source-snapshots/round-45/S071.txt`. Live check: `https://docs.kernel.org/process/security-bugs.html`.

## Span enumeration (file order)

Command: python regex `“([^”]*)”` over the export file, per line. Output (24 spans total; opens = closes = 24):

```
17 28 'you must also always Cc: the Linux kernel security team'
18 29 'The security team does not assign CVEs, nor do we require them for reports or fixes'
19 36 'the validity of the report should be seriously questioned'
20 37 'other groups focus on fixing issues in distros and coordinating disclosure between operating system vendors'
21 42 'Prepare a plain-text report explaining the problem. It must contain the four items listed at the top of this file as absolutely necessary'
22 58 'this may be postponed at the request of the reporter or an affected party'
23 59 'or use of AI-based tools'
24 60 'solely focuses on getting bugs fixed'
```

Spans 17–24 are the eight quotes above, at knowledge-file lines 28, 29, 36, 37, 42, 58, 59, 60.

## Snapshot location (S071.txt)

Command: whitespace-collapsed contiguous match of each quote in S071.txt with line mapping. Output:

```
17 found lines 272 - 273
18 found lines 362 - 363
19 found lines 208 - 209
20 found lines 333 - 334
21 found lines 241 - 242
22 found lines 309 - 310
23 found lines 117 - 117
24 found lines 332 - 332
```

Each quote matches once, verbatim, and the matched line range equals the cited range in the entry (`S071.txt:272-273`, `:362-363`, `:208-209`, `:333-334`, `:241-242`, `:309-310`, `:117`, `:332`). No cited range is wider than the located quote, so no LOOSE-RANGE finding. Snapshot integrity: `sha256sum .../S071.txt` = `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40`, equal to the manifest sha256 for S071.

Sample printed context (`sed -n`), for the check that the lines hold the quoted words:

```
271: The report must be sent to maintainers.  If there are two or fewer
272: recipients in your message, you must also always Cc: the Linux kernel
273: security team who will ensure the message is delivered to the proper
332: While the kernel security team solely focuses on getting bugs fixed,
333: other groups focus on fixing issues in distros and coordinating
334: disclosure between operating system vendors.  Coordination is usually
```

## Live rendered page

Command: `curl -sS -L --max-time 60 -o live.html -w 'HTTP %{http_code} final=%{url_effective} bytes=%{size_download}\n' https://docs.kernel.org/process/security-bugs.html`
Output: `HTTP 200 final=https://docs.kernel.org/process/security-bugs.html bytes=33621`. Tags stripped with a python regex pass (`<script|style>` removed, block tags to newlines, `html.unescape`); curly apostrophes and quotes normalised to ASCII before matching. Output (word-level, contiguous, whitespace-collapsed):

```
17 LIVE hits at lines [(278, 279)]
18 LIVE hits at lines [(352, 353)]
19 LIVE hits at lines [(226, 227)]
20 LIVE hits at lines [(328, 329)]
21 LIVE hits at lines [(253, 254)]
22 LIVE hits at lines [(309, 310)]
23 LIVE hits at lines [(152, 152)]
24 LIVE hits at lines [(327, 327)]
```

Live line numbers differ from snapshot line numbers because the HTML rendering wraps differently; the entry cites the snapshot, which is correct for that source. Word-level mismatch count: 0 of 8. No MISMATCH.

## Per-quote verdicts

| Span | Entry line | Quote location (S071) | Live | Quote verdict | Paraphrase fidelity |
|---|---|---|---|---|---|
| 17 | 28 | 272–273 (tight) | verbatim | OK | Faithful. "With two or fewer maintainer recipients, the security team must be Cc'd" matches "If there are two or fewer recipients ... you must also always Cc:". |
| 18 | 29 | 362–363 (tight) | verbatim | OK | Faithful. The page says the team does not require CVEs "for reports or fixes"; "Its absence is not a defect under this page" follows. |
| 19 | 36 | 208–209 (tight) | verbatim | OK | Minor narrowing. The page gives two triggers ("the reproducer does not work, or if the tool cannot produce one"); the paraphrase "a reproducer which fails" keeps only the first. Meaning not flipped. |
| 20 | 37 | 333–334 (tight) | verbatim | OK | Faithful as an inference. "records no kernel-security-team coordination role" follows from "the kernel security team solely focuses on getting bugs fixed" (line 332) plus the attribution to other groups. |
| 21 | 42 | 241–242 (tight; sentence ends at the colon of the four-item list) | verbatim | OK | Faithful. The truncation at the colon does not flip meaning; the four items are at line 243–245 and the MUST list is cited at 239–245. Context checked: 195–196 (plain text, no formatting), 213–217 (test the fix before reporting), 246 (recipients section). |
| 22 | 58 | 309–310 (tight) | verbatim | OK (quote) | Paraphrase gap. The entry says the postponement is "caps[ped]" and "a ceiling on requested postponement". The cap on line 310–312 is 7 calendar days, extendable to 14 "if it is agreed that the criticality of the bug requires more time" (line 311–312). The entry omits the 14-day agreed extension, so "ceiling" is only partly right. No meaning flip. |
| 23 | 59 | 117 (tight) | verbatim (line 152) | OK (quote) | Paraphrase gap. The page says not to use a public list "unless you have good reasons to consider the issue as being public or trivial to discover" (116–117). The entry drops "you have good reasons to consider", which is the reporter's judgement qualifier. "names ... as one such case" is faithful: AI-based tools appear as a parenthetical example. |
| 24 | 60 | 332 (tight) | verbatim (line 327) | OK | Faithful. "S071 says the security team 'solely focuses on getting bugs fixed' ... and attributes distro and vendor coordination to other groups (333–334)". |

Totals: OK 8, MISMATCH 0, LOOSE-RANGE 0, BROKEN 0. Paraphrase gaps (no meaning flip): spans 19, 22, 23.

## Discrimination (do-nothing control)

Commands and output:

```
S071 hits: 1 | S072 hits: 0 | live hits: 1 | shuffled-control S071 hits: 0 | you must also always Cc: the Linux kerne
S071 hits: 1 | S072 hits: 0 | live hits: 1 | shuffled-control S071 hits: 0 | The security team does not assign CVEs,
S071 hits: 1 | S072 hits: 0 | live hits: 1 | shuffled-control S071 hits: 0 | the validity of the report should be ser
S071 hits: 1 | S072 hits: 0 | live hits: 1 | shuffled-control S071 hits: 0 | other groups focus on fixing issues in d
S071 hits: 1 | S072 hits: 0 | live hits: 1 | shuffled-control S071 hits: 0 | Prepare a plain-text report explaining t
S071 hits: 1 | S072 hits: 0 | live hits: 1 | shuffled-control S071 hits: 0 | this may be postponed at the request of 
S071 hits: 1 | S072 hits: 0 | live hits: 1 | shuffled-control S071 hits: 0 | or use of AI-based tools
S071 hits: 1 | S072 hits: 0 | live hits: 1 | shuffled-control S071 hits: 0 | solely focuses on getting bugs fixed
```

- The quotes do not occur in the other S072 snapshot (0 hits), so the match is specific to S071 and the live page.
- A word-shuffled variant of each quote has 0 hits, so a match cannot be a bag-of-words coincidence.
- A near-miss variant ("the validity of the report should be strictly questioned") has 0 hits in both live and snapshot text (`LIVE: False SNAP: False`), so the matcher is not fuzzy.

## Limitations

- The snapshot is the reStructuredText source (`_sources/process/security-bugs.rst.txt`) captured 2026-10-28T20:52:44Z; the live check is the HTML page, tag-stripped with a regex, not a browser render. Tag-stripping could hide a mis-rendered quote, but all 8 quotes matched contiguously in the live text.
- I checked only spans 17–24 and the sentences that contain them, plus the cited context lines needed for those sentences. I did not audit the other 16 spans, the table rows, or the F04/F15 cross-references beyond the sentences that hold spans 19–20.
- The fetch was one request at one time; the live page can change after this check.
- I made no edits and no git mutations. The lane working tree was not read; the export was used throughout. Scratch directory removed on exit.
