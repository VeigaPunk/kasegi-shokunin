VERDICT: HOLDS

# R46SentinelContent: content-safety review, kasegi round 46 (read-only)

Scope: S073 capture, S073 manifest, claims.json, and the two C1 inputs (claim-package-contract.md, claim-gates.md), plus the planned F28 entry inputs (S073 + manifest quotes). Entry `corpus/knowledge/github-private-vulnerability-reporting.md` does not exist yet (`ls` printed "No such file or directory"), so it was reviewed as a plan, not as text. No drafts were written by this seat.

## 1. Scanned bytes are the committed, frozen bytes

Command: `git show 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5:<path> | sha256sum` vs `sha256sum <working path>`

```
corpus/source-snapshots/round-46/S073.txt  66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930
corpus/source-snapshots/round-46/manifest.json  01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34
.ufo/waves/round-46/claims.json  e56ebf872b6073964d98812608275f5799afc9ee2334d4aab1363c06e59cd740
```
Working-tree hashes are identical; the three paths are tracked and `git status --short` on them printed nothing. These match `freeze.txt` (S073-sha256, manifest-sha256, claims-sha256). The S073 size is 15568 bytes, matching manifest `snapshot_bytes`; line count is 589, matching manifest `lines` (Python `split("\n")` gives 590 only because of the trailing newline).

## 2. Credential, token, e-mail, session-URL, op:// scan

Strict pattern set (github PAT/`ghp_`, `github_pat_`, AKIA, PEM headers, `op://`, `Bearer`, `password|api_key|token|secret ... [:=] value`, `token=`, `session=`, cookie/consent/sign-in/log-out UI text, e-mail addresses, any `/home/<user>/` or `~/Projects/` or `$HOME`):

- `grep -nEi 'ghp_|op://|@[A-Za-z0-9.-]+\.[a-z]{2,}|...|[Cc]ookie|[Cc]onsent|[Ss]igned in|[Ll]og ?out|[Ss]ign ?in' S073.txt` printed nothing; `exit=1`.
- Same set against the committed capture: `grep -cE ... <git show 9f23aab:S073.txt>` printed `0`, `count-exit=1`.
- Python scanner (`kv-secret`, `cred-literal`, `op-ref`, `email`, `token-query`, `host-path`, `session-cookie-ui`) on S073.txt, manifest.json: 0 hits in every class.
- URLs: capture contains no `http(s)://` strings. manifest.json:6,7,10 is the public `https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately` with no query string, no token, `capture_url == url`, `final_url == url`.
- claims.json: `author: "KasegiR46"` (lane seat name) is the only identity field; no e-mail, no token.

Conclusion: the S073 capture and manifest hold no credential material, no private or session URL, no op:// reference, and no e-mail address.

## 3. Personal data in the capture

The capture is public docs navigation plus one article. Lines 1-554 are sidebar/menu/nav (e.g. S073.txt:8 `Home`, :9 `Security and code quality`); the article is S073.txt:556-579. No account name, avatar, "signed in as", user handle or org name appears anywhere in the 589 lines. The only identity-like text is the publisher footer at S073.txt:589 `GitHub Inc. © 2026TermsPrivacyStatusPricing`.

Cookie/consent text: none captured (scanner `session-cookie-ui` = 0). Caveat in section 8: the raw 577,188-byte fetch is not committed, so consent-banner stripping by the extractor is not independently verifiable from the corpus.

False-positive class (do not "fix" by stripping): a broad `grep -i secret` matches 23 navigation lines (e.g. S073.txt:18 `Secret security`, :19 `Secret leakage risks`, :20 `Secret scanning`, :23 `Secret security with GitHub`). These are product-section headings, not credentials.

## 4. Quote safety (S073, <=25-word rule)

Manifest quotes Q1-Q8 (manifest.json:20-59) each located verbatim at their anchor line by the Python check (`located True` for all eight). Word counts: Q1 10, Q2 6, Q3 13, Q4 18, Q5 14, Q6 13, Q7 20, Q8 15 — all <=25.

UI strings (button/label names) and their lines:
- `Report a vulnerability` — S073.txt:569 (3 words)
- `Fill in the vulnerability reporting form` — S073.txt:571 (6 words; an instruction, not a label)
- `I used AI assistance to find or write up this report` — S073.txt:574 (11 words; checkbox label)
- `Submit report` — S073.txt:575 (2 words)
- `Start a temporary private fork` — S073.txt:578 (5 words)
- `Security and quality` — S073.txt:555 (nav), :568 (tab name) (3 words)
- `Who can use this feature?` — S073.txt:559 (section heading, 5 words)

Verdict: quoting these UI strings is safe and within the <=25-word rule. Each is short, verbatim, and locatable.

Normalisation trap: S073.txt:568 reads `click the Security and quality tab. If you cannot see the " Security and quality" tab` — the capture has a stray leading space inside the second quoted token. An entry must quote `Security and quality` with no leading space, or the located-check will fail on the space variant. (The substring `Security and quality` is still contained in line 568, so the counter passes either way; the space is an extraction artifact, not page text.)

## 5. What the F28 entry and C1 re-grounds must NOT reproduce

1. Navigation and boilerplate: S073.txt:1-555 sidebar, :558 `Copy markdown`, :580 `Back to top`, :582 `Was this Doc helpful?`, :583 `YesNo`, :584 `Help us make GitHub Docs great!`, :586-589 contribution/support links and the footer copyright line. None is article content.
2. Any URL other than the pinned public URL in manifest.json:6, and never with tracking/session query parameters. The page's cross-link titles (S073.txt:561, :563, :566, :579 — "Configuring private vulnerability reporting for a repository", "Creating a repository security advisory", "Coordinated disclosure of security vulnerabilities", "Managing privately reported security vulnerabilities") may be named as text; do not invent link URLs for them.
3. Any real GitHub account, handle, org, e-mail, reporter name, token, or example maintainer contact. The corpus must use neutral wording ("the reporter", "the maintainer").
4. Any host-specific path. Do not add `/home/vgpnk/...` or `~/Projects/...` to the new entry. Cite corpus-relative paths only (e.g. `corpus/source-snapshots/round-46/S073.txt:577`). Pre-existing host paths in other entries are not a reason to add more (section 6).
5. A proof-of-concept, exploit sequence or reproduction recipe. S073.txt:573 asks the reporter for a "proof of concept" and "impact statement"; the entry may name the form fields (Q5) and the decision rule, but must not write example PoC steps, payloads, or any automation that submits reports.
6. Generalisation from the adjacent secret-scanning/push-protection nav (S073.txt:18-34, :145-153) into the F28 entry. Those are separate product features.
7. The copyright footer and "Make a contribution" text (S073.txt:586-589).

## 6. Pre-existing host paths in the C1 inputs (no new leakage, but do not extend)

- corpus/knowledge/claim-gates.md:3 (`Source: \`~/Projects/bounties/ops/claim-check.mjs\``), :123 (`source: [lost-tree] ~/Projects/bounties/...`), :125 (`recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -d ~/Projects/bounties ...`).
- corpus/knowledge/claim-package-contract.md:3, :19 (`~/Projects/the-bounty-hunter/...`), :66, :68 (recheck line with `/home/vgpnk/...` and `~/Projects/bounties`).
- .ufo/waves/round-46/claims.json:11, :12, :18 (these name the pattern being removed; contain no secret).

Command: `grep -rlE '/home/vgpnk|~/Projects/' corpus/knowledge | wc -l` printed `64`. The host-path convention is pervasive in the base corpus; it is pre-existing, not created by this round.

Rules for the C1 drafts:
- The recheck line of a re-grounded entry must carry no `~/` or `$HOME` path (r46-c1-gate.py:31 L3; the gate checks only the recheck line, via `HOME_RE` at r46-c1-gate.py:62 and :187).
- BASE `source:` lines (claim-gates.md:3, claim-package-contract.md:3) are append-only (r46-c1-gate.py:33 L5); keep them byte-identical. Do not rewrite them to repo-relative paths in this round (that would break L5).
- New `## Re-ground (round 46)` rows must anchor to committed corpus/ or .ufo/ bytes (e.g. `corpus/instruments/claim-package-check.py:N`), never to `~/Projects/bounties`.
- The regex at claim-gates.md:48 (`/(api[_-]?key|secret|token|password|bearer)\s*[:=]...`) is a secret-detector pattern, not credential material. It may be cited or kept.

## 7. Falsification of the content-safety surface (scanner controls)

Controls were run against the same scanner in scratch (`$HYAKU_SCRATCH/kasegi-r46/R46SentinelContent/`, removed on exit):
- do-nothing control (empty file): `{'cred-literal': 0, 'kv-secret': 0, 'op-ref': 0, 'email': 0, 'token-query': 0, 'host-path': 0, 'session-cookie-ui': 0}`
- planted control (real S073 + synthetic lines: a `api_key = "..."` placeholder, an e-mail on `.invalid`, a `?session=` URL, an `op://` ref, a `/home/<user>/Projects` path, a "cookies / consent" sentence): `{'cred-literal': 0, 'kv-secret': 1, 'op-ref': 1, 'email': 1, 'token-query': 1, 'host-path': 0, 'session-cookie-ui': 2}`

So the scanner discriminates the S073 capture (all zeros) from the planted lines (every class except credential-literal and host-path flagged).

Scanner gap found: the `host-path` class is case-sensitive lowercase (`/home/[a-z]+/`); a planted `/home/PLANTEDUSER/...` line scored 0. Real operator paths are lowercase (`vgpnk`), so no current input is missed, but a capitalised user name would be. The C2 gate's control set (freeze-controls.txt) has no content-safety control at all (`total=9 red=9 green=0`); none plants a credential or e-mail into an entry. Recommend the L1 add one; this seat did not edit the frozen counter or controls.

Gate interaction for the F28 entry: r46-c2-gate.py:25-27 (G5) requires every curly-quoted span to be followed by a backticked `S073.txt:N[-M]` citation, <=25 words, and "no curly quote is uncited". Any UI label placed in curly quotes in the entry must carry such a citation, or it counts as uncited.

## 8. Limitations

- The raw 577,188-byte fetch (manifest.json:16 `bytes`) is not committed; only the 15,568-byte extracted snapshot is. Stripping of cookie/consent banners by the extractor cannot be verified from the corpus. The snapshot is the authority for this round.
- No live re-fetch of the URL was made (documentation-only corpus; the pinned capture is the evidence).
- The scanner patterns are this seat's, not exhaustive; "no match" means no match for those classes only.
- Interpretation: "two new knowledge-entry inputs" was read as the two C1 re-ground entries (claim-package-contract.md, claim-gates.md, both existing), since the F28 entry does not yet exist.
- The F28 and C1 drafts were not built by this seat; this review gives the constraints the builders must satisfy.
- Nothing was installed. No commits, pushes, or git/jj mutations were run; only read-only `git show`, `git status`, `git ls-files`, `git rev-parse`, `git cat-file`.
- Scratch dir `$HYAKU_SCRATCH/kasegi-r46/R46SentinelContent/` held only the planted and do-nothing control files; both were deleted and the directory removed on exit.
