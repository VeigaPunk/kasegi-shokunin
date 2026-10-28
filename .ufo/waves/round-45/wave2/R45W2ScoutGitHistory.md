VERDICT: HOLDS

Attacked object: torvalds/linux `master` `Documentation/process/security-bugs.rst`, fetched 2026-10-28 from git.kernel.org, against the S071 snapshot exported from lane commit `6662a4276b6f7bd61e23e12058414e09dd71b9e4` (not the moving worktree). Manifest quotes are the five `S071.quotes` strings in that commit's `corpus/source-snapshots/round-45/manifest.json`. The 7/14-day sentence searched is the whitespace-joined sentence that contains Q1:

> Although our preference is to release fixes for publicly undisclosed bugs as soon as they become available, this may be postponed at the request of the reporter or an affected party for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days if it is agreed that the criticality of the bug requires more time.

Whitespace normalisation used for the diff: CRLF to LF, each run of spaces/tabs collapsed to one space, trailing whitespace stripped per line, trailing empty line dropped. Quote search uses a second collapse, `" ".join(text.split())`, so a quote wrapped across RST lines still matches. Both collapses were equal for the export and the live file.

## Finding 1 — export S071 and today's master RST are the same bytes

Attacked: `git archive 6662a427` path `corpus/source-snapshots/round-45/S071.txt` versus `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/process/security-bugs.rst` (HTTP 200, 20152 bytes, 2026-10-28T21:38:52Z). The `?h=master` URL returned HTTP 301 to that same plain URL and the same etag. The plain URL at `?id=6ffecfe0805e8811e7637e8f381b6740a3e9767b` was fetched separately.

Command and printed output:

```
sha256sum <export>/corpus/source-snapshots/round-45/S071.txt security-bugs.kernel.org.rst
0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40  .../S071.txt
0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40  security-bugs.kernel.org.rst
cmp EXPORT S071 vs kernel.org plain: IDENTICAL
cmp plain vs ?h=master: IDENTICAL
cmp plain vs id=6ffecfe: IDENTICAL
git hash-object security-bugs.kernel.org.rst
c7dfecc87764c05e437e9ecccf6605f31907f27c
```

That sha256 is the manifest pin on the exported `manifest.json` (`export_manifest_sha256 0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40`, `bytes 20152`, `lines 372`). The cgit etag was `W/"c7dfecc87764c05e437e9ecccf6605f31907f27c"`, the same blob id `git hash-object` printed. The worktree copy of `S071.txt` compared identical to the export (`cmp EXPORT S071 vs worktree S071: IDENTICAL`); the cited object is the export.

A second git host, `https://kernel.googlesource.com/pub/scm/linux/kernel/git/torvalds/linux.git/+/refs/heads/master/Documentation/process/security-bugs.rst?format=TEXT` (HTTP 200), base64-decoded to 20152 bytes with the same sha256 (`cmp SNAP vs googlesource master TEXT: IDENTICAL`). The GitHub raw URL was not usable: two GETs of `https://raw.githubusercontent.com/torvalds/linux/master/Documentation/process/security-bugs.rst` printed `http_code=429` (bodies 324 and 199 bytes, rate-limit text). It is not evidence of the file.

## Finding 2 — whitespace-normalised diff is empty

Attacked: exported `S071.txt` versus the kernel.org plain body.

Command: Python `difflib.unified_diff` on the line normalisation above. Printed:

```
line_norm_equal=True
unified_diff_lines=0
unified_diff=<empty>
collapse_equal=True
```

## Finding 3 — five manifest quotes and the 7/14-day sentence are in the live RST; controls do not contain them

Attacked: the kernel.org plain body (byte-identical to the export). Quotes copied from the exported manifest:

- Q1 anchor 310: `for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days`
- Q2 anchor 95: `If you resorted to AI assistance to identify a bug, you must treat it as public`
- Q3 anchor 39: `Binary-only executables are not accepted.`
- Q4 anchor 41: `By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug.`
- Q5 anchor 20: `with no version indication, your report will not be processed`

Collapsed-text search printed:

```
POSITIVE kernel.org master plain
  Q1 present=True
  Q2 present=True
  Q3 present=True
  Q4 present=True
  Q5 present=True
  sentence_7_14 present=True
  fabricated_21day present=False
  quotes_present=5/5
```

The same search on the export printed `quotes_present=5/5` and `sentence_7_14 present=True`.

Located lines in the live body (1-based), which the diff shows are the export's lines:

```
L20:  * **affected kernel version range**: with no version indication, your report
L21:    will not be processed.  Note that a time-dependent version such as "latest
L39:    instructions, file-system image etc).  Binary-only executables are not
L40:    accepted.  Working exploits are extremely helpful and will not be released
L41:    without consent from the reporter, unless they are already public.  By
L42:    definition if an issue cannot be reproduced, it is not exploitable, thus it
L43:    is not a security bug.
L95:**If you resorted to AI assistance to identify a bug, you must treat it as
L96:public**. While you may have valid reasons to believe it is not, the security
L308:Although our preference is to release fixes for publicly undisclosed bugs
L309:as soon as they become available, this may be postponed at the request of
L310:the reporter or an affected party for up to 7 calendar days from the start
L311:of the release process, with an exceptional extension to 14 calendar days
L312:if it is agreed that the criticality of the bug requires more time.  The
```

Q1, Q3, Q4, and Q5 are wrapped across those lines. Q2 is wrapped L95–L96 and is surrounded by `**` markers; the quote without the asterisks is still a substring of the collapsed text.

Do-nothing and negative controls, same collapse, same five strings, same sentence, same fabricated string `for up to 21 calendar days from the start of the release process`:

```
CONTROL empty do-nothing
  quotes_present=0/5
  sentence_7_14 present=False
  fabricated_21day present=False
CONTROL submitting-patches.rst same host same method
  quotes_present=0/5
  sentence_7_14 present=False
  fabricated_21day present=False
control_first_nonempty='.. _submittingpatches:' in_control=True in_security_bugs=False
```

The control file is `Documentation/process/submitting-patches.rst` from the same git.kernel.org plain URL (HTTP 200, 41614 bytes). The empty file is a zero-byte do-nothing document. The live security-bugs text does not contain the control's heading, and it does not contain the fabricated 21-day string. A raw `grep -n -F` of each full quote against the kernel.org plain file printed `raw_grep=MISS rc=1` five times. That miss is the line wrap, not absence: `grep -n -F` of the on-line fragments printed L20, L39, L43, L95, L310, and L311.

## Finding 4 — latest commit on the git.kernel.org log page

Attacked: `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/Documentation/process/security-bugs.rst` (HTTP 200, 11511 bytes, page footer `generated ... at 2026-10-28 21:38:55 +0000`). The branch dropdown has `value='master' selected='selected'`. The pager element is empty (`<ul class='pager'></ul>`). The path log lists 18 commits, newest first.

First row, as printed by extraction from that saved HTML:

```
first_row_title_attr 2026-08-04 16:24:50 +0200
first_row_age 2026-08-04
first_row_href /pub/scm/linux/kernel/git/torvalds/linux.git/commit/Documentation/process/security-bugs.rst?id=6ffecfe0805e8811e7637e8f381b6740a3e9767b
first_row_subject docs: security-bugs: clarify some mandatory steps for AI reports
first_row_author Willy Tarreau
row_count 18
pager_empty True
branch_selected_master True
```

The commit page `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=6ffecfe0805e8811e7637e8f381b6740a3e9767b` (HTTP 200) prints:

- author Willy Tarreau `<w@1wt.eu>`, `2026-08-02 22:35:40 +0200`
- committer Greg Kroah-Hartman `<gregkh@linuxfoundation.org>`, `2026-08-04 16:24:50 +0200`
- commit `6ffecfe0805e8811e7637e8f381b6740a3e9767b`
- parent `3d7c44f73765d98665fb97a4fb89c002c88ba1b9`
- subject `docs: security-bugs: clarify some mandatory steps for AI reports`
- diff header `index 6f7c21515e9ea..c7dfecc87764c`, one file, `1 files changed, 22 insertions, 0 deletions`

The resulting blob abbrev `c7dfecc87764c` is the blob id from Finding 1, and the plain file at that commit id compared identical to master. The log's second row shares the committer timestamp `2026-08-04 16:24:50 +0200` but is a different commit, `e447f7f33fa0a50d42d0539c161a662e67bd1a2c` (`docs: security-bugs: clarify what counts as a valid version`), whose own commit page names parent `11f46e30e6885734be609e337e65a4784bdd282d`, not `6ffecfe`. Master plain matches the `6ffecfe` blob, so that second commit has not replaced the file on master.

The Atom feed for the same path (`<updated>2026-08-04T14:24:50Z</updated>`, first entry id `urn:sha1:6ffecfe0805e8811e7637e8f381b6740a3e9767b`) agrees with the log page. `2026-08-04T14:24:50Z` is `2026-08-04 16:24:50 +0200`.

The plain response's own `last-modified: Wed, 28 Oct 2026 21:38:09 GMT` is the cgit response timestamp, not the commit date. The commit date is the log/commit page value above.

## Finding 5 — docs.kernel.org still serves those bytes; its Last-Modified is not the git commit date

Attacked: `https://docs.kernel.org/_sources/process/security-bugs.rst.txt`, the capture URL on the exported manifest. This run's GET printed `http_code=200 size=20152`, `last-modified: Sun, 09 Aug 2026 21:57:49 GMT`, sha256 `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40`, `cmp SNAP vs docs.kernel.org body: IDENTICAL`.

That Last-Modified is the date the exported `SOURCES.md` row S071 records for this URL. It is five days after the git committer date `2026-08-04 16:24:50 +0200`. The bodies match, so the gap is publication time of the docs site, not a different RST.

## Limitations

- GitHub raw `master` returned HTTP 429 on both attempts. The second host that did return the file was kernel.googlesource.com `format=TEXT`, not GitHub.
- No clone was made. Ancestry was not walked past the parent line on the `6ffecfe` commit page. The log page is newest-first with an empty pager, and master plain is byte-identical to `?id=6ffecfe`, which is the evidence that this path's current master blob is that commit's blob.
- The path log begins at the move into `Documentation/process/` (`44ac5abac86b`, 2023-03-12, last row). Older history under `Documentation/admin-guide/` is a different path and is not a later commit.
- A single-line `grep -F` of the five manifest strings misses all five because the RST wraps them. Presence is the collapsed-whitespace search plus the line quotes above.
- cgit `Last-Modified` on the plain URL is not the commit date.
- Documentation fetches only. No mail was sent and no kernel was tested.
- This seat did not grade `r45-c2-gate.py`. It checked the second authority for the RST text.
