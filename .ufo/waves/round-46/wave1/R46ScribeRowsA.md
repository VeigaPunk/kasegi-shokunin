VERDICT: DRAFT-READY

Scope: C2 registry drafter A (F28 / S073 registry material). Draft: `.ufo/waves/round-46/wave1/R46ScribeRowsA.draft/rows.md` (section 1 the S073 row; section 2 `## Registry changes` bullets; section 3 `## Search log` bullet). Nothing was committed, no git/jj state was touched, and no shared file was edited. Scratch was `/fast/scratch/hyaku/kasegi-r46/R46ScribeRowsA/` and is removed at exit. The row is not yet landed: the used-by entry `corpus/knowledge/github-private-vulnerability-reporting.md` does not exist, so the census reports E11 until it lands (finding 4).

## 1. S073 row: 11 cells, no pipe inside any cell

Attacked: the row text in rows.md, checked against the contract in CORPUS.md:64-148.

Command: `awk -F'|' '{print NF-2}' <row>`  Output: `11`
Command: `awk -F'|' '{print NF-1}' <row>`  Output: `12` (leading and trailing pipe plus 10 separators: 11 cells, no stray pipe)
Census malformed-row check on the scratch registry with the row inserted after S072 (line 78): the output contains no E01 line, so the row parses as 11 cells.

## 2. Anchor and quotes: the committed bytes

Command: `sha256sum corpus/source-snapshots/round-46/S073.txt` (lane tree)  Output: `66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930  …/S073.txt`, which matches the anchor cell and the manifest.
Command: `wc -c` / `wc -l` on that file  Output: `15568 bytes`, `589 lines`.
Command: `python3 -I corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46/manifest.json --source S073`  Output (exit 0):
```
S073:sha256 OK
S073:Q1 OK occurrences=1 anchor=560-ok
S073:Q2 OK occurrences=1 anchor=563-ok
S073:Q3 OK occurrences=1 anchor=564-ok
S073:Q4 OK occurrences=1 anchor=566-ok
S073:Q5 OK occurrences=1 anchor=573-ok
S073:Q6 OK occurrences=1 anchor=574-ok
S073:Q7 OK occurrences=1 anchor=577-ok
S073:Q8 OK occurrences=1 anchor=578-ok
```
Read of the anchored lines (`corpus/source-snapshots/round-46/S073.txt:556-583`): 556 is the heading "Privately reporting a security vulnerability", 564 holds "…You can only report vulnerabilities privately for repositories where this feature is enabled.", 573 holds "By default, you must provide a summary, details, proof of concept, and impact statement.", 575 is "At the bottom of the form, click Submit report.", 578 is the temporary private fork sentence. The Gate quote in the registry bullet is the 13-word sentence at line 564; `grep -n` on it returned `564:Private vulnerability reporting is separate from …`.

Legacy URL: `curl -sS -o /dev/null -w '%{http_code} final=%{url_effective} redirects=%{num_redirects}\n' -L --max-redirs 5 'https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability'`  Output: `200 final=https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately redirects=1`, observed 2026-10-28. The manifest records only the canonical final URL, so this redirect is a dated observation and not a committed capture.

## 3. Census validate: do-nothing control and the drafted row

Do-nothing control, base registry plus base knowledge (`validate --file <scratch>/ctl/corpus/SOURCES.md`):
```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	<scratch>/ctl/corpus/SOURCES.md
```
exit 0. The same base census on the live file (`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md`) printed the same three W04 lines and `file	ok`, exit 0.

Drafted row, exact command `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch>/corpus/SOURCES.md`, scratch registry = live file with the S073 row inserted after S072, knowledge tree = base copy (no S073 entry):
```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	E11	S073 missing used-by corpus/knowledge/github-private-vulnerability-reporting.md
```
exit 1. The only finding is E11, and it names the used-by path the entry will create. Without E11 the row passes every other census check. With a scratch-only stub at that path (a fixture, not a deliverable) the same command prints `file	ok	<scratch>/val/corpus/SOURCES.md` after the three W04 lines, exit 0. Adding the section 2 and section 3 bullets to the scratch file leaves the result unchanged (W04 x3, ok, exit 0).

Spot-check item 4, S072 supersedes S070: S072 `teaches` opens ` supersedes S070 — REJECTED: …`. S070 and S072 share canonical URL `https://bughunters.google.com/about/rules/about-this-section` and have different scope cells, so the census prints W04, not E04. The line is `file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes`, quoted above, exit 0. Recorded as expected in the registry-changes bullet.

## 4. Frozen counter G3 and mutants (the row against the counter's own logic)

The counter `corpus/instruments/r46-c2-gate.py` was loaded read-only (no bytecode written) and `g3(root)` was called on scratch trees. Each tree had a scratch-only F28 README line naming the used-by entry, a scratch-only stub entry, the committed S073.txt, and one mutated copy of the row. Census was run on the same trees.

```
== as-drafted: census-exit=0 | G3 pass=1 read=row-S073=ok
== tier-B: census-exit=0 | G3 pass=0 read=bad=tier
== pipe-in-cell: census-exit=1 | G3 pass=0 read=row-S073=absent-or-malformed
    file	E01	S073 fields=12
== anchor-sha-zeroed: census-exit=0 | G3 pass=0 read=bad=anchor-sha
== opened-future: census-exit=1 | G3 pass=0 read=bad=opened
    file	E08	S073 opened=2026-11-30
== recheck-bad: census-exit=1 | G3 pass=1 read=row-S073=ok
    file	E09	S073 recheck=180 days
== used-by-wrong: census-exit=1 | G3 pass=0 read=bad=used-by
    file	E11	S073 missing used-by corpus/knowledge/other-entry.md
== status-queued: census-exit=0 | G3 pass=0 read=bad=status
```
Discrimination: G3 catches tier, sha, status, opened, used-by and a pipe-broken row; census catches E01, E08, E09 and E11, but not tier-B or the sha. G3 does not check `recheck`, so census is the only gate on that cell. The G3 `row-S073=ok` reading depends on the scratch F28 stub, so it grades the row alone, not the F28 frontier row or the entry (those are other seats' items).

## 5. Search sweep and held rows

Command (on the frozen base export, `/fast/scratch/hyaku/kasegi-r46/L1/pure` copied to scratch; its `corpus/SOURCES.md` sha256 `beeef08efdb24f3158a82ee4435b07b9973763bb1af3844037867b4a471208fa` equals `git show 914ca0b6…:corpus/SOURCES.md`): `grep -rliE 'private vulnerability reporting|privately report' corpus/knowledge corpus/SOURCES.md corpus/README.md`  Output: nothing; `sweep-exit=1`. Base holds 64 knowledge files and 27 F-rows (`grep -cE '^\| F[0-9]+ \|' corpus/README.md` → `27`).
Registry host check: `grep -n 'docs.github.com' corpus/SOURCES.md` printed nothing, so no existing row shares the URL.
Held rows (`awk` over the live registry): `S065 tier=A status=rejected`, `S068 tier=B status=rejected`, both opened 2026-10-28 with reasons quoted in their teaches cells (S065: disjointness tie-break against sibling S015; S068: unreviewed NVD mirror with no package and no affected or patched ranges).
After landing the sweep hits `corpus/SOURCES.md` (the row title "Privately reporting…" and the bullets) and will also hit the README F28 row and the knowledge entry. Run on the scratch registry with bullets: `corpus/SOURCES.md`, exit 0.

## Limitations

- The used-by entry does not exist. The census prints E11 for S073 until the entry lands, and the counter's G7 (the census validate) is red until then. The row is DRAFT-READY, not landed.
- The legacy-URL redirect is a 2026-10-28 HEAD observation and not a committed capture; the manifest records only the canonical final URL.
- I did not draft the F28 README row or the knowledge entry; the G3 probe used scratch-only stubs for both, and the stub entry is not a deliverable.
- The full counter (C2 `r46-c2-gate.py`) was not run on a tree with the real entry, so G1, G2, G5 and G6 were not graded by me.
- The base census already prints W04 for S028 and S029 (pre-existing duplicates). I did not touch them.
- Observation, not changed: the S072 row is tier A with status `rejected`; the census accepts this.
- No S071 registry-change bullet exists in the file; the bullet pattern used is S051/S052 (`S0NN row added: new row (id …)`).
- One stray shell line with an unset variable (`bash $CENSUS validate …`) errored silently to /dev/null; it is not evidence and produced no output.
- Scratch was removed at exit; nothing in this report depends on a /tmp path.
