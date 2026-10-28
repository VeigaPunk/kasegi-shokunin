VERDICT: BROKEN

Scope: S071 (docs.kernel.org/process/security-bugs.html, RST source) as used by corpus/knowledge/linux-kernel-security-bugs-reporting-process.md and the S071 row of corpus/SOURCES.md, read from the integration export 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (round base dc5bb8c6e31efc4a6650819df85e79b72fd64bcd). Scratch was /fast/scratch/hyaku/kasegi-r45/R45W2CritSourceTrust (removed on exit). All network access was read-only GET of public kernel documentation and the kernel.org git mirror (curl only). No live target was touched.

Summary:
- The quoted TEXT holds. The capture is byte-identical to the upstream RST at the signed kernel tag v7.3 (and at v7.2-rc7, v7.2, and master HEAD), and all 24 curly-quoted spans in the knowledge entry occur verbatim in it.
- The entry's `recheck:` line is BROKEN as a freshness claim. It is a local-bytes check that cannot see upstream, covers 5 of 24 quoted spans, and its 180d interval is not supported by the observed upstream churn.
- The `7.3.0` label is not a revision pin. The same bytes are served at v7.2-rc7 through v7.3, so the label should be replaced with a sha-pinned revision range. The entry's current "does not rely on that label" is safe but leaves the verifiable pin unused.
- `verified-at: 2026-10-28` is honest: I re-fetched the live source today and got the same sha256.

## Finding 1: upstream second authority (kernel git tree) confirms the text at the same revision

Attacked: capture corpus/source-snapshots/round-45/S071.txt (sha256 0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40, 20152 bytes, 372 lines) against the upstream file at several revisions.

Commands and printed output (sha256 truncated to 16 hex):
- `curl -sS -D - -o ... https://docs.kernel.org/_sources/process/security-bugs.rst.txt` → `HTTP/2 200`, `last-modified: Sun, 09 Aug 2026 21:57:49 GMT`, `content-length: 20152`, `age: 2725`, `x-cache: HIT`, `date: Wed, 28 Oct 2026 21:38:09 GMT`; body sha256 `0918dcfa7979f348...` = capture.
- `curl -sS .../linux.git/plain/Documentation/process/security-bugs.rst` (HEAD) → `0918dcfa7979f348 372`.
- `plain/...security-bugs.rst?h=v7.3` → `0918dcfa7979f348 372`.
- `?h=v7.2-rc7` → `0918dcfa7979f348`; `?h=v7.2` → `0918dcfa7979f348 372`.
- `?h=v7.2-rc1` → `0f7177ec0c9f95c0 346` (differs); `?h=v7.1` → `0f7177ec0c9f95c0 346`; `?h=v7.0` → `252e9ded81f6a9de 244`; `?h=v6.18` → `696485952de9ecab 116`.
- Revisions on the file's log (`atom/Documentation/process/security-bugs.rst`, 10 newest entries): 6ffecfe0 (2026-08-04 committer date, author date 2 Aug 2026, Willy Tarreau, Signed-off-by Greg Kroah-Hartman) → `0918dcfa7979f348 372`; e447f7f3 (2026-08-04) → `f6bc9a92a31f563b 350`; 561458db (2026-05-14) → `0f7177ec0c9f95c0 346`; 4bf85afb (2026-05-12) → `937778cd4137fab6 345`; a03ef333 (2026-05-12) → `f767b80c26c74ed6 288`; aed3c334 (2026-05-12) → `f7293bb14ab0539b 252`; f387e2e2 (2026-04-04) → `252e9ded81f6a9de 244`; 496fa1be (2026-04-03) → `6806fd215194744d 244`; a72b832a (2026-04-03) → `8f623506d8e0c69b 192`; f2b1cbef (2026-04-03) → `9ab3e163308e7557 122`.
- Tag v7.3 object (`tag/?h=v7.3`): tagger Linus Torvalds, `tagged object commit c03c1a1450...`, body contains a `-----BEGIN PGP SIGNATURE-----` block. I did NOT verify that signature (no key material fetched).
- Master Makefile: `VERSION = 7`, `PATCHLEVEL = 3`, `SUBLEVEL = 0`, `EXTRAVERSION =`.

Located quotes at the upstream tag v7.3 (file identical to capture, so line numbers match the capture):
```
20:  * **affected kernel version range**: with no version indication, your report
95:**If you resorted to AI assistance to identify a bug, you must treat it as
241:1. Prepare a plain-text report explaining the problem. It must contain the
310:the reporter or an affected party for up to 7 calendar days from the start
311:of the release process, with an exceptional extension to 14 calendar days
350:mailing list UNTIL a fix is accepted by the affected code's maintainers
```
Quote-presence matrix (12 manifest-style quotes, present=Y) per revision: `6ffecfe0 12/12`, `v7.3 12/12`, `docs-rst-live 12/12`, `e447f7f3 11/12`, `561458db 11/12`, `4bf85afb 11/12`, `a03ef333 10/12`, `aed3c334 8/12`, `496fa1be 7/12`, `f387e2e2 7/12`, `a72b832a 4/12`, `f2b1cbef 4/12`. The "treat as public" AI rule is absent at aed3c334 (2026-05-12, `0`) and present at a03ef333 and 4bf85afb (2026-05-12, `1`), so it entered in the 2026-05-12 group; it is absent at v7.0 and present at v7.1. The 7-day text (`for up to 7 calendar days`) is present in every fetched revision including the oldest, f2b1cbef (2026-04-03, `1`), and at v6.18, so the 7/14-day rule is long-standing. The `with no version indication` text is absent at v6.18 and present at v7.0.

Decision: the upstream tree at v7.3 is a valid second authority for the TEXT of S071 and confirms all 24 spans (Finding 2). MAINTAINERS is a weaker second authority, see Finding 7.

## Finding 2: knowledge-entry quote spans vs. capture (coverage of the recheck)

Attacked: all 24 curly-quoted spans in corpus/knowledge/linux-kernel-security-bugs-reporting-process.md, each checked for verbatim presence in the capture after whitespace and RST-markup normalization, and against the `S071.txt:N[-M]` anchors on the same line.

Output (abridged): `curly quotes in knowledge file: 24`; each line printed `occ=[N]` with N inside the cited window; `not found: 0`; no `<-- cited anchor ... not near occurrence` flags. So all 24 quotes and their anchors hold.

Attacked: the `recheck:` command (knowledge line 5) and SOURCES S071 recheck column (`180d`). Running `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071` printed:
```
S071:sha256 OK
S071:Q1 OK normalized=markup-whitespace occurrences=1 anchor=310-ok
S071:Q2 OK ... anchor=95-ok
S071:Q3 OK ... anchor=39-ok
S071:Q4 OK ... anchor=41-ok
S071:Q5 OK ... anchor=20-ok
exit=0
```
The manifest pins 5 quotes (anchors 310, 95, 39, 41, 20). Those 5 are among the 24 spans; the other 19 (e.g. lines 17-18, 22-24, 28-29, 36-37, 42, 58-60 of the entry) are not covered by the recheck the entry names.

## Finding 3: the `recheck:` line is a local-bytes check, not a freshness recheck

Attacked: corpus/instruments/source-recheck.py and the entry's `recheck:` line.
- Its own docstring: "This instrument reads only local files; a successful check verifies captured bytes, not current upstream availability or freshness."
- `grep -n -i 'urllib\|http\|socket\|curl\|subprocess' corpus/instruments/source-recheck.py` → only `24:import subprocess` and subprocess calls at 304-308; no network call.
- corpus/instruments/recheck-audit.py docstring: it asks "is the entry's own recheck line an executable, cwd-independent command that actually re-derives something for THAT entry?" — it validates executability, not that upstream was re-read.

Discriminating control (do-nothing vs. the instrument). I built fixtures with the same manifest, replacing S071.txt with an older upstream revision and recomputing its sha256/bytes/lines:
- positive (capture): `S071:sha256 OK` ... all Q OK ... `exit=0`.
- revision 496fa1be (2026-04-03, 244 lines): `Q2 MISMATCH reason=quote-not-found`, `Q1 OK ... anchor=OUT-OF-RANGE`, `Q3 OK ... anchor=39-BROKEN`, `Q4 OK ... anchor=41-BROKEN`, `exit=1`. So the quote check does discriminate local content.
- revision 4bf85afb (2026-05-12, 345 lines): `Q1 OK ... anchor=310-BROKEN`, `Q2 OK ... anchor=95-BROKEN`, `Q3 OK ... anchor=39-BROKEN`, `Q4 OK ... anchor=41-BROKEN`, `exit=0`.

Two conclusions. (a) The instrument does not read upstream at all, so its PASS is identical whether or not docs.kernel.org has changed; as a freshness check it is a do-nothing. (b) For unique quotes it prints `anchor=N-BROKEN` yet still reports OK and exit 0; the line anchors the entry cites (S071.txt:N) are therefore not enforced by the recheck. I verified them only by my own Finding 2 script.

Upstream discrimination that the recheck lacks: sha256 of the live/mirror file equals the manifest for HEAD, v7.2-rc7, v7.2 and v7.3, and differs for v7.1, v7.0, v6.18 and the 2026-04 to 2026-05 revisions. A one-line upstream check, e.g. `curl -sS https://docs.kernel.org/_sources/process/security-bugs.rst.txt | sha256sum`, does discriminate; the entry's recheck does not do it.

## Finding 4: verified-at / recheck honesty

- `verified-at: 2026-10-28`: HONEST. The capture was fetched 2026-10-28T20:52:44Z (manifest); my independent re-fetch at 21:38Z returned the same sha256 and 20152 bytes.
- `recheck: ... # 180d`: NOT HONEST as stated. (i) It does not recheck upstream (Finding 3). (ii) It covers 5 of 24 spans (Finding 2). (iii) 180d from 2026-10-28 is 2027-04-26; the observed churn is 10 commits on 5 distinct change-days in Apr–Aug 2026 (2026-04-03, 04-04, 05-12, 05-14, 08-04), and the rule text changed inside the v7.2-rc cycle (v7.2-rc1 `0f7177ec...` → v7.2-rc7 `0918dcfa...`). A 180-day interval is not supported by that churn. recheck-audit passes it anyway because it checks executability only.
- The S071 SOURCES row `last-modified 2026-08-09 21:57:49 GMT` is the HTTP header of the docs deploy (live header confirmed); the content commit is 6ffecfe0, committer date 2026-08-04T14:24:50Z. Label it as the deploy date.
- Note also that the live docs response was a varnish cache HIT (`age: 2725`), so "live" here means cache-fresh within its TTL.

## Finding 5: the `7.3.0` label

Attacked: knowledge line 48 ("The assignment labels the page as versioned 7.3.0 at capture, but the capture carries no version string ... This entry does not rely on that label."). That is accurate for the RST capture, but:
- The cited HTML page does carry the label: `curl -sS https://docs.kernel.org/process/security-bugs.html` → line 42 `<p class="blurb">7.3.0</p>`. This is the docs build's version, not the text's revision.
- The same RST bytes are at v7.2-rc7, v7.2, v7.3 and HEAD (Finding 1). So "7.3.0" pins neither the text nor the earliest revision holding it. The honest pin is "sha256 0918dcfa7979f348..., identical at kernel tags v7.2-rc7 through v7.3 (master HEAD included)".

## Finding 6: row and entry wording vs. the page

Attacked: SOURCES S071 `teaches` cell: "expect any fix embargo to run at most 7 calendar days from release start, extendable to 14 only by agreement." The page (capture lines 308-311) says: "this may be postponed at the request of the reporter or an affected party for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days if it is agreed". The row drops the requester qualifier and generalizes to "any fix embargo". The entry itself rejects that generalization (knowledge lines 58-59), so the row contradicts the entry it feeds. Recommended wording: "a requested postponement of a fix may run up to 7 calendar days from release start; 14 only if agreed".

## Finding 7: upstream MAINTAINERS entry (second authority, weaker)

Attacked: MAINTAINERS at v7.3 (`plain/MAINTAINERS?h=v7.3`, sha256 6151790c22698b0f…):
```
24767:SECURITY CONTACT
24768-M:	Security Officers <security@kernel.org>
24769-S:	Supported
24770-F:	Documentation/process/security-bugs.rst
```
This confirms who maintains the file, not the 7/14-day text or the AI rule. It is consistent with the entry's attribution to the kernel security team. Both git.kernel.org and docs.kernel.org are kernel.org infrastructure, and the security team authors the text, so the second authority establishes revision integrity, not independent authority over the policy.

## Limitations
- I did not verify the PGP signature on tag v7.3 (no key material fetched).
- The file log was read only as far as the atom feed (10 newest entries); earlier history beyond v6.18 was not walked.
- Tags checked: v6.18, v7.0, v7.1, v7.2-rc1, v7.2-rc7, v7.2, v7.3, master HEAD. I did not bisect the rc2–rc6 window that changed the bytes.
- The live docs response was a cache HIT; the git mirror responses were not cache-tagged.
- I did not verify S072 (out of scope for this seat).
- The fixture tests replaced the manifest sha/bytes/lines for each revision; they test quote logic, not upstream freshness.
- No live-target testing; only documentation GETs.

## Smallest safe corrections (for the L1)
1. Replace the entry's `recheck:` with an upstream comparison (sha256 of the docs `_sources` RST or the git plain file at `?h=v7.3`) and keep source-recheck as a second, local-integrity command; or relabel the 180d as "local integrity only; upstream not rechecked".
2. Tie the recheck trigger to the next kernel tag (v7.4-rc1 onward) and to any commit touching Documentation/process/security-bugs.rst, not to 180 days.
3. Extend the manifest to all 24 quote spans, or state that only 5 are machine-pinned.
4. Replace `7.3.0` in the entry's provenance with the sha-pinned revision range (v7.2-rc7 through v7.3).
5. Fix SOURCES S071 `teaches` to keep the "at the request of the reporter or an affected party" qualifier.
6. Flag to the instrument owner: source-recheck prints `anchor=N-BROKEN` yet exits 0 for unique quotes.
