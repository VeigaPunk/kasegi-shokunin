VERDICT: BROKEN

Scope: registry rows S071 and S072 in `corpus/SOURCES.md` at lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (exported with `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 6662a4276b6f7bd61e23e12058414e09dd71b9e4 | tar -x -C <scratch>`; export was not the moving lane tree). Contract: `/home/vgpnk/Projects/shokunin/CORPUS.md` lines 64–135 ("Contract v1", rules 1–6, shape, census). The numeric anchors HOLD; the cell-semantics and rule-1/rule-2 contract checks have BROKEN items below.

## What HOLDS (re-run by me)

H1. Pinned bytes, hashes, lines. `sha256sum` / `wc` on the export:
```
0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40  corpus/source-snapshots/round-45/S071.txt
20152 corpus/source-snapshots/round-45/S071.txt   (wc -c)
372 corpus/source-snapshots/round-45/S071.txt     (wc -l)
364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025  corpus/source-snapshots/round-45/S072.txt
10032 corpus/source-snapshots/round-45/S072.txt   (wc -c)
312 corpus/source-snapshots/round-45/S072.txt     (wc -l)
```
Both match the S071 and S072 rows (row S071 cites sha 0918dcfa…9346f40, 20152 bytes, 372 lines; row S072 cites 364166c4…a025, 10032 bytes, 312 lines) and `manifest.json` entries.

H2. S071 section headings (`grep -n` on S071.txt): Preparing your report L10; What qualifies as a security bug L73; Identifying contacts L109; Responsible use of AI to find bugs L174; Sending the report L254; Disclosure and embargoed information L299; Coordination with other groups L329; CVE assignment L359; Non-disclosure agreements L368. All nine heading names in the row match, in the same order.

H3. S072 anchors. `sed -n` on S072.txt: L17 `## Android & Friends`; L57 `## Chrome & Friends`; L107 `## Google & Friends`; L171 `## Open Source`; L249 `## Other`. L148–L149 is the Cloud VRP scope cell text "Security issues affecting any Google Cloud product or web service that" / "handles reasonably sensitive user data". All correct.

H4. Raw JSON binding. `cmp <(jq -r '.body' .ufo/waves/round-45/source-recon/S072.json) corpus/source-snapshots/round-45/S072.txt` printed nothing and returned success (IDENTICAL). `jq -j '.body' | wc -m` = 10029 (body without the jq newline), matching "body 10029 characters" in the row.

H5. Recheck of the manifest quotes: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071` printed `sha256 OK`, Q1 anchor=310-ok, Q2 95-ok, Q3 39-ok, Q4 41-ok, Q5 20-ok (exit 0). `--source S072`: sha256 OK, Q1 anchor=148-ok, Q2 anchor=1-ok (exit 0).

H6. S072 teaches claim vs S069: S069 Q5 at `corpus/source-snapshots/round-44/S069.txt` lines 9–11 reads "In principle, any Google Cloud product or web service that handles reasonably sensitive user data is intended to be in scope." The S072 L148–149 line restates it, as the row says.

H7. Append-only (rule 2). `git diff --stat dc5bb8c6e31efc4a6650819df85e79b72fd64bcd 6662a4276b6f7bd61e23e12058414e09dd71b9e4 -- corpus/SOURCES.md` → `1 file changed, 2 insertions(+)`; the only added lines are the S071 and S072 rows. No prior cell changed; S070 remains `rejected`.

H8. Rows are well-formed: NF=13 for both rows (validate E01 passes); S072 teaches opens `supersedes S070 —` and carries `REJECTED: …; flip: …` (rule 2 correction form); S071 `used-by` path `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` exists; `opened` 2026-10-28 and fetch timestamps (20:52:44Z, 20:53:00Z) agree with `source-snapshots/round-45/manifest.json`.

H9. Census. Validate, exact output (lane export, default today):
```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <export>/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	<export>/corpus/SOURCES.md
EXIT=0
```
The same output appears with `--today 2026-10-28`. Do-nothing control, base tree (`git archive dc5bb8c6…`), prints the same W04 S028/S029 lines and `ok`, EXIT=0. Census (`census --file`): lane rows 72 (A 64, B 5, C 3; mined 57, rejected 15) vs base rows 70 (A 63, B 4, C 3; mined 56, rejected 14). The delta is exactly the two new rows. No E-codes for S071/S072.

## BROKEN findings (ordered by severity)

F1 (medium, scope vs use). Row S071 scope (`corpus/SOURCES.md:77`, scope cell) reads: "The kernel security team's own report-intake and embargo rules only; its CVE and linux-distros statements are outside this row." The admitted knowledge entry cites S071 for exactly those statements:
- `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md:27`: "When may linux-distros be contacted? … “a fix is accepted by the affected code's maintainers” (`S071.txt:350`)".
- `…process.md:29`: "Is a CVE a required intake field? … “The security team does not assign CVEs, nor do we require them for reports or fixes” (`S071.txt:362-363`)".
- `…process.md:37`: distro/vendor coordination quoted from `S071.txt:333-334`.
Commands: `sed -n 27p`, `sed -n 29p` and `sed -n 37p` on `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md` printed the three lines above. The tier-A grade (scoped to the row's own scope) therefore does not cover these three citations; either the scope cell is wrong or the entry overreaches. Also, the S071 anchor cell (L77) lists "Coordination with other groups" (L329) and "CVE assignment" (L359) headings whose content the scope excludes.

F2 (medium, rule 1 gate missing at this commit). Rule 1 requires the round lesson's `## Gate` to record, for every new row, URL, access date and a ≤25-word quote with location. At 6662a42: `find corpus/lessons -name '*45*'` printed nothing (no `round-45.md`); `grep -rn 'S071\|S072' corpus/lessons` matched only `corpus/lessons/round-44.md:205`, which is the correction for S070. No gate record exists for S071 or S072 in any lesson. The quotes exist only in the manifest and knowledge entry. This may be pending round closure, but the integrated tree does not satisfy rule 1 as written.

F3 (medium, canonical URL). Rule "source — title — canonical URL or DOI". S072 uses the article-API endpoint as its URL (`corpus/SOURCES.md:78`: `https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section`). The lane's own precedent records the opposite: `corpus/SOURCES.md:156` (round-44 note) says "S069's canonical source URL remains the row URL; the manifest records the article API separately as `capture_url`/`http.final_url`", and S070 (`corpus/SOURCES.md:76`) carries the canonical page `https://bughunters.google.com/about/rules/about-this-section`. S072 is the same article, so a reader following the registry URL reaches JSON, not the page. [INFERENCE: I did not establish why the API URL was chosen.] Fix: row URL = `https://bughunters.google.com/about/rules/about-this-section` with the API as capture metadata, per the S069 precedent.

F4 (low–medium, tier justification). S072 is tier B because it is "a secondary routing summary". Per the contract, tier is scoped to the row's scope, and A includes "maintainer statement" and "official docs". The scope cell describes Google's own overview of which of Google's VRP programs covers which product family and where reports go, i.e. the publisher's authoritative statement for that claim. The row's stated reason ("secondary") does not match the contract's definition of B ("expert write-up with reproducible detail, survey, textbook"). The row is rejected and no admitted entry rests on it, so impact is low; the justification should be fixed or the tier changed.

F5 (low, verifiability of revision/anchors). (a) S071's anchor cites "last-modified 2026-08-09 21:57:49 GMT" but the only source for it is `.ufo/waves/round-45/source-recon/S071.headers.txt:4` (`last-modified: Sun, 09 Aug 2026 21:57:49 GMT`). The row does not cite that file, and `corpus/source-snapshots/round-45/manifest.json` has no last-modified field (`grep -c last-modified` → 0). The revision is not traceable from the registry. (b) S071 headings have no L-numbers, unlike S072; the knowledge entry supplies ranges instead. Section headings satisfy "exact section" in the letter; L-numbers (10, 73, 109, 174, 254, 299, 329, 359, 368) would match S072's standard.

F6 (low, teaches overstatement). S071 teaches: "expect any fix embargo to run at most 7 calendar days from release start, extendable to 14 only by agreement." Source `corpus/source-snapshots/round-45/S071.txt:305-311`: "Fixes for publicly known bugs are released immediately … this may be postponed at the request of the reporter or an affected party for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days if it is agreed …". The teaches (a) turns a ceiling on a requested postponement into an expectation ("expect … any"), and (b) drops the request precondition and the "only valid reason" limit at L312–314. The 14-day extension wording is accurate. Low risk, but the teaches is not a faithful one-line summary of the cited passage.

F7 (process, limitation of the validator). `validate` is structural only. Control fixture (scratch, written with `write`): a row with sha `000…dead` and `L9999` anchors but a valid used-by path produced `ok`, EXIT 0; a row with a valid sha/L310 but a missing used-by path (`corpus/knowledge/does-not-exist.md`) produced `file E11 S071 missing used-by …`, EXIT 1. So validate's clean exit is evidence of structure, not of anchors or hashes. Those checks were done by me (H1–H5), not by the census.

## Discrimination
- Do-nothing control: base tree (`dc5bb8c6…`) gives the same structural output without S071/S072 (census 70 rows vs 72).
- Fixtures: good / dangling-used-by / wrong-hash-and-line → `ok` / E11 exit 1 / `ok`. Validate's sensitivity is confirmed for used-by but not for anchors or hashes.

## Limitations
- Did not check live source (the live-drift seat owns it); all checks are against the pinned snapshots at the commit.
- Did not verify QUALITY rows R47–R49 or the knowledge entry body beyond the lines cited for F1.
- Did not establish whether a bounded search preceded S071/S072 (rule 5). No search-log entry exists for round 45; the rows appear to come from direct opens. Not established either way.
- F2 may be a pending closure artifact; the finding is against the integrated tree.
- No mutating git command; fixtures were scratch-only; scratch directory removed on exit. No tools installed.
