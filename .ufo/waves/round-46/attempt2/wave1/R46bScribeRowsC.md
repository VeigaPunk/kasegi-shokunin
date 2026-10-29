VERDICT: DRAFT-READY

# R46bScribeRowsC — C2 registry drafter C (F29 / S074), round 46 attempt 2

Scope: draft SOURCES.md material only — (a) the S074 registry row, (b) the `## Registry
changes` bullets to append, (c) the `## Search log` bullet. Draft written to
`.ufo/waves/round-46/attempt2/wave1/R46bScribeRowsC.draft/rows.md`. Nothing was
committed; no git/jj mutation, no index or working-tree edit anywhere; no file outside
this seat's draft directory and this Report was written. Scratch was
`/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsC/` and is removed at exit (the draft
directory holds no receipt that depends on it).

The entry `corpus/knowledge/github-repository-security-advisories.md` does not exist yet
(it is another seat's item), so the census prints `E11` for S074 on the live tree. That
is the expected pre-entry state, quoted in Finding 5; the row itself passes every other
census check and the gate's own H3 limb.

---

## Finding 1 — The S074 row: 11 cells, no pipe inside any cell

Attacked: the row text in `R46bScribeRowsC.draft/rows.md` §1, against the contract in
`/home/vgpnk/Projects/shokunin/CORPUS.md` ("SOURCES.md — where a shokunin learns", the
frozen Contract v1) and the F29 gate's H3 limb.

Command (on the row line extracted verbatim from the draft file):
`grep -m1 '^| S074 |' .../R46bScribeRowsC.draft/rows.md > $S/row_final.txt`
Output: `1216 /fast/scratch/hyaku/kasegi-r46/R46bScribeRowsC/row_final.txt`

Command: `awk -F'|' '{print "NF="NF" cells="NF-2}' $S/row_final.txt`
Output: `NF=13 cells=11`

Command: `awk -F'|' 'NR==1{for(i=2;i<NF;i++) if ($i ~ /\|/) print "PIPE IN CELL " i}' $S/row_final.txt`
Output: nothing (no pipe inside any of the ten interior cells).

Command: `diff <(sed 's/[[:space:]]*$//' $S/row.txt) <(sed 's/[[:space:]]*$//' $S/row_final.txt)`
Output: `IDENTICAL` (the row validated below is byte-identical to the one in the draft).

The drafted row:

```
| S074 | GitHub Docs, Repository security advisories — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories | docs | A | GitHub's own statement of the maintainer-side repository security advisory lifecycle only (draft advisory, temporary private fork, CVE request via GitHub as CNA, credit, publication and the fix-version duty); not the reporter-side reporting flow, not advisory editing, not the REST API and not the Advisory Database edit flow | body lines 1-42 of corpus/source-snapshots/round-46-a2/S074.txt (the whole capture is the page body), sha256 1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039 (snapshot 42 lines, 7087 bytes; manifest raw 582877 bytes; fetched 2026-10-29T20:19:30Z, HTTP 200, final URL equals the row URL); the nine located manifest quotes Q1-Q9 sit at L10, L13, L17, L24, L25 (Q5 and Q6), L26, L31 and L38 | A maintainer drafts the advisory, fixes in a temporary private fork, requests a CVE from GitHub as CNA while the advisory stays private, credits contributors, then publishes with a fix version attached. | mined | 2026-10-29 | 90d | corpus/knowledge/github-repository-security-advisories.md |
```

Placement: directly after the S073 row in the `## Registry` table (at base `04af9bc9`
the S073 row is `corpus/SOURCES.md:79`; the new row becomes line 80). Placing a
row-shaped line outside the Registry section draws `E12 row outside Registry section`
from the census.

Registry counts (census `census` mode, base export vs the drafted registry):

```
file	rows	73      <- base export
file	rows	74      <- with the S074 row inserted
file	tier.A	66  ->  file	tier.A	67
```

## Finding 2 — The anchor cell rests on the committed capture bytes

Attacked: does the anchor cell's sha256, byte count, line count and fetch record match
the committed `corpus/source-snapshots/round-46-a2/S074.txt` and `manifest.json`?

Command: `sha256sum corpus/source-snapshots/round-46-a2/S074.txt corpus/source-snapshots/round-46-a2/manifest.json`
Output:
```
1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039  corpus/source-snapshots/round-46-a2/S074.txt
46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f  corpus/source-snapshots/round-46-a2/manifest.json
```
Both equal the digests in `.ufo/waves/round-46/attempt2/freeze.txt`
(`S074-sha256 1296528d…c278039`, `manifest-a2-sha256 46e8077a…81569f`) and the values
the F29 gate pins (`r46-f29-gate.py` `PINS["S074.txt"]`, `PINS["manifest.json"]`).

Command: `wc -c -l corpus/source-snapshots/round-46-a2/S074.txt`
Output: `42 7087` (42 lines, 7087 bytes) — matching the anchor cell's
"snapshot 42 lines, 7087 bytes".

Command: `python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074`
Output (exit 0):
```
S074:sha256 OK
S074:Q1 OK occurrences=1 anchor=10-ok
S074:Q2 OK occurrences=1 anchor=13-ok
S074:Q3 OK occurrences=1 anchor=17-ok
S074:Q4 OK occurrences=1 anchor=24-ok
S074:Q5 OK occurrences=1 anchor=25-ok
S074:Q6 OK occurrences=1 anchor=25-ok
S074:Q7 OK occurrences=1 anchor=26-ok
S074:Q8 OK occurrences=1 anchor=31-ok
S074:Q9 OK occurrences=1 anchor=38-ok
```
The anchor cell's "L10, L13, L17, L24, L25 (Q5 and Q6), L26, L31 and L38" is exactly
this list. The manifest's own record confirms the fetch: `fetched_utc
2026-10-29T20:19:30Z`, `http.status 200`, `http.final_url` equal to the row URL, `bytes
582877` (the raw page) and `snapshot_bytes 7087`.

## Finding 3 — `teaches` is grounded in located quotes (Rule 1)

Attacked: is every clause of the `teaches` cell supported by text that is actually in
the capture, at a locatable line?

Command: a Python check that looks for each candidate quote string in the snapshot's own
lines. Output:
```
20 words | lines [12] | Create a draft security advisory, and use the draft to privately
16 words | lines [14] | Publish the security advisory to alert your community of the vul
12 words | lines [17] | You can give credit to individuals who contributed to a security
11 words | lines [13] | Privately collaborate to fix the vulnerability in a temporary private 
15 words | lines [24] | GitHub is a CVE Numbering Authority (CNA) and is authorized to assign 
11 words | lines [25] | Requesting a CVE identification number doesn't make your security advi
15 words | lines [38] | you should add a fix version to a security advisory prior to publishin
```
So `teaches` — draft the advisory, fix in a temporary private fork, request a CVE from
GitHub as CNA while the advisory stays private, credit contributors, publish with a fix
version attached — is carried by L12/L13/L24/L25/L17/L14/L38, all inside the capture
body (lines 1-42). The Rule-1 Gate quote offered for the lesson's `## Gate` section is
the 11-word **"Requesting a CVE identification number doesn't make your security
advisory public."** (`S074.txt:25`) — inside the ≤25-word limit.

## Finding 4 — The gate's own H3 limb accepts the row and kills 12 mutants

Attacked: does `r46-f29-gate.py`'s H3 (the SOURCES-row limb) accept the drafted row,
and does it discriminate against a junk row?

Harness: each tree is `git archive fe0f56b… corpus` (the freeze commit, which carries
the round-46-a2 capture) with the drafted row inserted after S073 and a scratch-only
stub entry at `corpus/knowledge/github-repository-security-advisories.md`; the gate is
loaded read-only via `importlib` and `h3(root)` is called. The census is run on the
same tree.

```
== as-drafted               H3 pass=1 read=row-S074=ok | census-exit=0
== tier-B                   H3 pass=0 read=bad=tier | census-exit=0
== kind-spec                H3 pass=0 read=bad=kind | census-exit=0
== status-queued            H3 pass=0 read=bad=status | census-exit=0
== opened-wrong             H3 pass=0 read=bad=opened | census-exit=0
== anchor-sha-zeroed        H3 pass=0 read=bad=anchor-sha | census-exit=0
== anchor-locator-outside   H3 pass=0 read=bad=anchor-locator | census-exit=0
== anchor-no-capture        H3 pass=0 read=bad=anchor-locator | census-exit=0
== used-by-wrong            H3 pass=0 read=bad=used-by | census-exit=1
     census: file	E11	S074 missing used-by corpus/knowledge/other-entry.md
== scope-thin               H3 pass=0 read=bad=scope-words | census-exit=0
== teaches-thin             H3 pass=0 read=bad=teaches-words | census-exit=0
== recheck-bad              H3 pass=0 read=bad=recheck-cell | census-exit=1
     census: file	E09	S074 recheck=90 days
== url-wrong                H3 pass=0 read=bad=url | census-exit=0
     census: file	W04	S074 duplicate url docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately across scopes
```

Discrimination: the gate's H3 limb is the only check that catches a wrong tier, a wrong
kind, a wrong status, a wrong opened date, a corrupted anchor sha256, an anchor locator
outside the snapshot body, a missing capture path, a too-thin scope, a too-thin teaches
and a wrong URL — the census is blind to all of those (it printed `ok`/exit 0 on nine of
the twelve mutants). The census is the only check that catches a malformed recheck
(`E09`) and a dangling used-by (`E11`); H3 catches the dangling used-by too, via its own
`used-by` test. The two gates therefore cover each other.

The `url-wrong` mutant is instructive: pointing S074 at S073's reporter-side URL leaves
both gates "green-ish" (census exit 0, only a W04 warning) — the row would silently
double-count the reporter-side source under the maintainer-side scope. H3's `bad=url` is
the only thing that stops it, which is why the URL cell must be the canonical
`repository-security-advisories` URL and not S073's.

## Finding 5 — Census validate: do-nothing control, then the drafted row

Attacked: does the drafted registry still pass `sources-census.sh validate`, and what
does the census print for the not-yet-existing used-by path?

Do-nothing control — the untouched base export (no row inserted):

Command: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/val/corpus/SOURCES.md`
Output:
```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsC/val/corpus/SOURCES.md
```
exit 0. The three W04 warnings are pre-existing at the base and are not touched by this
row.

The drafted registry (base export + the S074 row inserted after S073), with the
used-by path absent because the entry is another seat's item:

Command: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/val/corpus/SOURCES.md`
Output:
```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	E11	S074 missing used-by corpus/knowledge/github-repository-security-advisories.md
```
**exit 1**. So the census prints exactly one new finding over the do-nothing control —
`E11 S074 missing used-by corpus/knowledge/github-repository-security-advisories.md` —
and nothing else: no `E01` (malformed row), no `E03` (duplicate id), no `E04`/`E05`/
`E06`/`E07`/`E08`/`E09`/`E10`/`E12`, and no new `W04` (the S074 URL is unique in the
registry — `grep -c 'repository-security-advisories'` on the drafted registry prints `1`).

The same run with a scratch-only stub entry placed at the used-by path (a fixture, not
a deliverable, removed immediately afterwards):

```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsC/val/corpus/SOURCES.md
```
exit 0. That is the post-entry state the L1 will see.

The same validation on the freeze-commit tree with the row inserted and a scratch stub
entry (`corpus/SOURCES.md` row 80) gives the same three W04 lines and `file	ok`,
exit 0, and the gate's H3 reads `row-S074=ok`.

## Finding 6 — The capture-directory note is factually load-bearing

Attacked: the claim in bullet (b) that `corpus/source-snapshots/round-46-a2/` exists
*beside* `round-46/` because the round-46 manifest is sha-pinned by the attempt-1
receipts and must stay byte-identical. A counterfactual tree was built: the S074
record was appended to the pinned `round-46/manifest.json` instead of a sibling
directory.

Command (counterfactual): build the tree, merge the S074 record into
`corpus/source-snapshots/round-46/manifest.json`, then call the attempt-1 counter's
capture limb.

Output:
```
counterfactual: S074 merged into the pinned round-46 manifest
attempt-1 c2-gate g4 (capture pin) on that tree: pass=0 read=manifest-not-the-pinned-bytes
  round-46/manifest.json sha now: 5e97bbded806067e2568367e8fe8d45d621837fd32972ac070cf28f33beca3bb
  pin expects:                 01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34
attempt-1 c2-gate g4 on the sibling-dir tree: pass=1 read=recheck-rc=0 quotes-ok=8 frozen-cores-missing=0
```
So merging into the pinned directory breaks the attempt-1 counter
(`corpus/instruments/r46-c2-gate.py:61` pins `PINS["manifest.json"] =
01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34`; the same digest is
recorded in `.ufo/waves/round-46/freeze.txt:7` and in the attempt-1 receipts
`.ufo/waves/round-46/wave1/R46ScribeRegistry.md:90`,
`.ufo/waves/round-46/wave1/R46SentinelContent.md:13`,
`.ufo/waves/round-46/wave1/R46ScribeScoreboard.md:18`). The live
`corpus/source-snapshots/round-46/manifest.json` still hashes to
`01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34` — unchanged. The
sibling directory is therefore the only arrangement that keeps the attempt-1 counter
green, which is what the Registry-changes bullet states.

## Finding 7 — The Search-log bullet's absence sweep, re-run here

Attacked: the PRISMA-style absence claim behind the Search-log bullet: does the corpus
already hold the maintainer-side advisory lifecycle?

Command (base export):
`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus | tar -x -C $S/base`

Command: `grep -rliE 'repository securit. advisor|GHSA' $S/base/corpus/knowledge $S/base/corpus/SOURCES.md $S/base/corpus/README.md`
Output:
```
/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsC/base/corpus/knowledge/github-private-vulnerability-reporting.md
/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsC/base/corpus/SOURCES.md
EXIT=0
```

Command (line level, same pattern and paths):
`grep -rniE 'repository securit. advisor|GHSA' $S/base/corpus/knowledge $S/base/corpus/SOURCES.md $S/base/corpus/README.md`
Output (4 line hits in 2 files):
```
.../base/corpus/knowledge/github-private-vulnerability-reporting.md:40:- The page does not state the maintainer-side flow, CVE requests, timelines or rewards
.../base/corpus/knowledge/github-private-vulnerability-reporting.md:43:- Four linked pages appear only as link text in the capture, and their bodies are not
.../base/corpus/SOURCES.md:74:| S068 | GitHub Advisory Database entry GHSA-v676-f8gm-92r9 for CVE-2025-9086 — https://github.com/advisories/GHSA-v676-f8gm-
.../base/corpus/SOURCES.md:157:- Public disclosed advisory pair for the claim-package gate exemplar (round 43); question: which single first-par
EXIT=0
```

Command: `grep -ciE 'repository securit. advisor|GHSA' $S/base/corpus/README.md`
Output: `0`, exit 1.

Command (live lane): `grep -rliE 'repository securit. advisor|GHSA' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md`
Output: the same two paths (`corpus/knowledge/github-private-vulnerability-reporting.md`,
`corpus/SOURCES.md`), exit 0; the `-n` re-run gives the same line numbers 40, 43, 74,
157; `grep -ciE … corpus/README.md` prints `0` (exit 1); `grep -rn 'S074'
corpus/SOURCES.md corpus/README.md` prints nothing, exit 1.

Command (do-nothing / presence discrimination): `grep -rn 'S074' $S/base/corpus/SOURCES.md $S/base/corpus/README.md`
Output: `(no output)`.

Counts for the bullet: identified 2 files (identical in both trees), screened 4 line
hits, included 1, excluded 3, README 0. Excluded with reason: the F28 entry's own
scope-out notes (`github-private-vulnerability-reporting.md:40,43` — the lifecycle pages
appear there only as link text, explicitly outside F28's reporter-side scope); the S068
row (`SOURCES.md:74` — a rejected GitHub Advisory Database mirror of an NVD record, not
a maintainer-published advisory); the round-43 search-log bullet (`SOURCES.md:157` — a
historical hunt for the claim-package exemplar, a different question). Stop rationale:
the hits are exhausted with saturation — every hit is either the gap's own note or an
unrelated scope, so a wider corpus sweep would only re-find the F28 pointer.

Adjacent rows already held, each with its scope cell (for the entry's Overlap section):
- **S073** (`corpus/SOURCES.md:79`) — "GitHub's own statement of the reporter-side private-reporting flow only (who may report, the form's default fields, submission and the temporary private fork); not maintainer handling of a report, the GitHub Advisory Database or CVE assignment"
- **S031** (`corpus/SOURCES.md:37`) — "CVE Program CNA scope, vulnerability determination and assignment requirements in the current version 4.2.6"
- **S069** (`corpus/SOURCES.md:75`) — "Google Cloud VRP scope and the program's boundary against testing customer-owned resources; not a universal authorization rule"

## Finding 8 — What the draft contains, and what it deliberately does not

The draft file `.ufo/waves/round-46/attempt2/wave1/R46bScribeRowsC.draft/rows.md` holds:
§0 placement instruction; §1 the row plus an 11-cell breakdown table; §2 the two
`## Registry changes` bullets; §3 the `## Search log` bullet; §4 the Rule-1 grounding
table for `teaches`; §5 the explicit out-of-scope list.

The `## Registry changes` bullets follow the S073 bullet pattern
(`corpus/SOURCES.md:162`): id / kind / tier-and-scope / status / opened / recheck /
used-by, the pinned capture with its sha256 and the located lines, a Rule-1 Gate quote
with its word count and location, the access date from the manifest's `fetched_utc`, and
the registry row-count transition. The second bullet is the capture-directory note.
The row-count transition is 73 → 74.

Out of scope for this seat and left to their owners: the entry
`corpus/knowledge/github-repository-security-advisories.md`, the README frontier row F29
(the base README carries 28 `| Fnn |` rows and no F29 row), and the round-46 lesson's
`## Gate` section. No `status`, `recheck` or `used-by` cell of any pre-existing row
(S001–S073) is changed.

## Limitations

- The census `E11` on S074 is real today and will clear only when the entry file lands;
  every other census check passes on the drafted row (Finding 5).
- The gate's H1/H2/H5/H6/H7 limbs are not exercised by this seat: they grade the entry,
  the README frontier row and the knowledge tree, none of which exist in the lane yet.
  H3 alone is exercised here, and only against a scratch tree with a stub entry.
- The absence sweep is the prescribed textual pattern over the three admission-bearing
  surfaces only (`corpus/knowledge`, `corpus/SOURCES.md`, `corpus/README.md`).
  `corpus/lessons/`, `corpus/instruments/` and `corpus/source-snapshots/` were not
  swept, so "absent" means absent from the admission-bearing surfaces, not corpus-wide.
- Live-lane state is as of 2026-10-29 (host `date -u +%F` prints `2026-10-29`); a
  sibling landing a row after my sweep is not reflected.
- `git archive` reproduces tree content, not commit metadata; provenance rests on the
  frozen rev ids printed in the command lines.
- No tooling was installed or upgraded (nothing in `~/.local/bin`, no `pacman`, no
  `uv`/`npx` install); the pacman guard was respected by doing nothing.
- No credential material, session URL or `op://` reference appears in the draft.
- Scratch `/fast/scratch/hyaku/kasegi-r46/R46bScribeRowsC/` is removed on exit; no
  `/tmp` path is cited as evidence anywhere in this Report.
