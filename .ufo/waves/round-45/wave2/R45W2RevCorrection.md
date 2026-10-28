VERDICT: BROKEN

Scope: the `Correction (round 45, appended 2026-10-28)` paragraph at the end of `corpus/lessons/round-44.md` in lane commit `6662a4276b6f7bd61e23e12058414e09dd71b9e4` (parent `5242db6`, round base `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd`). All checks ran against a `git archive` export of 6662a42 in scratch, plus one live re-fetch. The numbers, the located quote, the pure append and the no-rewrite claim HOLD. The paragraph's causal claim is overstated, its pointer to the wrong reason is incomplete, and its provenance is missing. Those three are the BROKEN part.

## Findings

### F1 — Numbers: HOLD
Attacked: the paragraph's HTTP 200, 10029 chars, 10030 characters, sha256, 312 lines, and `corpus/source-snapshots/round-45/S072.txt`.
- Live re-run: `curl -sS -o live.json -w 'HTTP %{http_code} bytes=%{size_download}\n' https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section` printed `HTTP 200 bytes=10588`. `cmp live.json .ufo/waves/round-45/source-recon/S072.json` printed nothing (byte-identical to the recon capture).
- `json.loads(live.json)['body']`: `body chars 10029 bytes 10031`, `body ends newline True`.
- `S072.txt` (export): `10032 bytes`, `312 lines` (`wc -l`), `sha256 364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025`, Python `chars 10030 ... endsNL True`. `S072.txt == body + "\n"` → `True`. So "10030 characters with one extra trailing newline" is exact.
- `corpus/source-snapshots/round-45/manifest.json` S072 entry: `"status": 200`, `"sha256": "364166c4…a025"`, `"lines": 312`, quote Q1 anchor 148.
- Limitation: no response-header file exists for S072 (only S071 has `S071.headers.txt`); the 200 in the manifest is recorded, not independently captured. My re-run now returns 200.

### F2 — Located quote: HOLD
Attacked: "located across the line break at 149" (`corpus/source-snapshots/round-45/S072.txt:148`).
- `sed -n '145,152p'` shows line 148 `   <td>Security issues affecting any Google Cloud product or web service that` and line 149 `handles reasonably sensitive user data`. Whitespace-normalised substring check: `S072 located ws-normalised: True`.

### F3 — "restates S069 Q5": HOLD
Attacked: the paragraph's "which restates S069 Q5 and adds no customer-resource rule".
- `corpus/source-snapshots/round-44/S069.txt`, normalised: `…## Services in scope In principle, any [Google Cloud](…) product or web service that handles reasonably sensitive user data is intended to be in scope. On the flip side, the…` The S072 line 148 wording matches. `grep -i customer corpus/source-snapshots/round-45/S072.txt` returned nothing, so no customer-resource rule appears in S072.

### F4 — Pure append, no history rewrite: HOLD
Attacked: "pure append" and "does not rewrite history".
- `git diff --numstat dc5bb8c… 6662a42… -- corpus/lessons/round-44.md` → `2	0	corpus/lessons/round-44.md`. Removed-line count `0`.
- `git show dc5bb8c:corpus/lessons/round-44.md | wc -l` → `203`. `head -n 203` of the lane file `cmp`s equal to the base file (`PREFIX_203_IDENTICAL`). Base file ends in `\n`.
- `git merge-base --is-ancestor dc5bb8c… 6662a42…` → `BASE_IS_ANCESTOR`. Lane log: `6662a42 round-45: integrate wave 1 …` on top of `5242db6`.
- S070 row in `corpus/SOURCES.md` line 76: `diff` of base and lane rows printed nothing (`S070_ROW_IDENTICAL`).
- `corpus/lessons/round-44-verifier-spotcheck.md` is byte-identical base→lane (`SPOT_SAME`).

### F5 — DEFECT (overclaim): "the JavaScript-shell reason does not hold"
Attacked: the paragraph sentence "the S070 body is readable through the article API (…), so the JavaScript-shell reason does not hold."
- The S070 URL that the reject reason is about is the HTML page `https://bughunters.google.com/about/rules/about-this-section`, not the article API. Live re-run: `curl -sS -o page.html -w 'HTTP %{http_code} bytes=%{size_download}'` printed `HTTP 200 bytes=3593`. Stripping `<script>`/tags leaves visible text of 28 characters: ` Rules | Google Bug Hunters `. The body is `<body class="mat-app-background">` with 3 `<script>` tags. The "Welcome to Google's Bug Hunting community…" string appears only in meta.
- So the JavaScript-shell observation about the S070 URL still holds for a plain fetch. What is wrong is the inference that the rule text is unavailable: the article API serves the same content. The spot-check uses the same distinction for S069 (`round-44-verifier-spotcheck.md` line 65: "the HTML page is a metadata shell for a plain fetch, so I re-opened the same document through …/rest/v1/articles/…"). The correction's sentence contradicts that method.
- Suggested replacement (draft, not applied): "The S070 HTML page still serves only an application shell to a plain fetch; the same content is readable through the article API …, so the reject reason 'accessible body is a JavaScript shell' is not the reason. The true reason is …".

### F6 — DEFECT (incomplete pointer): the wrong reason appears twice
Attacked: "the S070 reject reason above (`## Gate` and the S070 row)".
- `corpus/lessons/round-44.md:22` (under `## Gate — frontier, source, and rejection`, line 20): `…rejected because its accessible body is a JavaScript shell and its metadata is only a directory welcome.`
- `corpus/lessons/round-44.md:131` (under `### Gate — admit and reject from this round's source set`, line 128, inside `## Attempt 2`): `- **Reject — S070, tier C, \`rejected\`.** … the accessible body is a JavaScript shell and the metadata is a directory welcome with no quotable rule.`
- The correction names only `## Gate`. Line 131 is neither named nor corrected, and its `### Gate` heading differs. The verifier spot-check's routed item (`round-44-verifier-spotcheck.md` line 79) also names only `## Gate`, so the omission was inherited.

### F7 — DEFECT (provenance): the correction does not credit the spot-check
Attacked: whether the paragraph separates S070's wrong reason from the verifier spot-check's wording.
- The paragraph's phrase "overview, no program-specific rule beyond S069 Q5" is verbatim the spot-check's wording (`round-44-verifier-spotcheck.md` line 79: `the true reason is "overview, no program-specific rule beyond S069 Q5"`). The paragraph never cites the spot-check file or section; the finding that the reason was wrong is the spot-check's (line 75 and 66), so it is unattributed.
- The spot-check's own quote, line 66, `the row and lesson say the body "is a JavaScript shell … no quotable rule text"`: the words "no quotable rule text" do not appear in `round-44.md`. `grep -rn 'no quotable rule text' corpus/` finds only the spot-check. `round-44.md:131` reads "with no quotable rule". So the spot-check misquotes its target by adding "text". The correction does not reproduce that misquote.
- The separation the assignment asks for is therefore only implicit: the paragraph quotes neither the round-44 reason nor the spot-check.

### F8 — PARTIAL routed-defect compliance: the S070 row is untouched
Attacked: `round-44-verifier-spotcheck.md` section 6 item 1: "Append (never rewrite) a correction to `corpus/SOURCES.md` S070 … Replace the vacuous flip condition with a checkable one."
- The lane made no append to the S070 row (F4: byte-identical). The S070 row still reads `REJECTED: the page's accessible body is a JavaScript shell …` with the old flip condition.
- The correction lives only in the new S072 row (`lane SOURCES.md:78`): `supersedes S070 — REJECTED: the body is readable through the article API (10029 characters), so S070's no-body reason is corrected; …`. A reader who looks up S070 alone does not see the correction. This is a valid "supersede" design, but it is not the appended S070 correction the routed item asked for. Flagging it as partial; the lane may have chosen this deliberately (the paragraph says "stays byte-identical as history").

### F9 — Do-nothing control discriminates
`/fast/scratch/…/ctl/check.py` (scratch, removed) implements 18 checks: correction present, pure append, the numbers, file sha/lines/chars, body = 10029 and file = body+"\n", located quote at 148/149, S070 row identical, spot-check unchanged, and two provenance/wording checks (C9 cites the spot-check; C10 quotes "JavaScript shell").
- Lane export (`6662a42`): `C1…C8 PASS, C10 PASS, C9 FAIL` → `fails: ['C9_para_cites_spotcheck']`. C9 is the F7 defect.
- Do-nothing control (base `dc5bb8c` round-44.md as the "after"): `fails: ['C1_correction_paragraph_present', 'C2_pure_append', 'C3a_HTTP200', 'C3b_10029_chars', 'C3c_10030_characters', 'C3d_sha256_in_para', 'C3e_snapshot_path_in_para', 'C9_para_cites_spotcheck', 'C10_para_quotes_JS_shell_reason']`. The check discriminates the paragraph from the do-nothing tree.
- Mutants (lane tree with one change each): A, S072 trailing newline stripped → `C4a, C4b, C4c, C5b` fail. B, round-44.md line 22 edited in place → `C2_pure_append` fails. C, recon body +1 char → `C5a, C5b` fail. D, spot-check appended one line → `C8` fails. Every mutant is rejected by a check it should trip.

## Limitations
- Only one live re-fetch of each URL; the API and HTML results are for 2026-10-28 and may change. No JavaScript execution: "shell" is judged from static HTML (visible-text extraction), not a browser.
- No S072 response-header capture; HTTP 200 for the 2026-10-28 capture rests on the manifest plus my re-run.
- F5–F7 are wording and provenance defects; they do not change any number or the append-only property. I did not check the S072 SOURCES row, QUALITY rows, or other lane artifacts beyond the paragraph's claims.
- Public documentation fetches only; no target testing. No edits, commits, or mutating git commands were run.
- Suggested wording in F5 is a draft for the L1, not applied.
