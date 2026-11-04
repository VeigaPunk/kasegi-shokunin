# ReviewC2 — round 68, C2 capture chain (S102)

**Verdict: VERIFIED** for the capture chain (items 1, 2, 4, 5, 6 pass, and item 3 passes every rule the manifest controls). **One predicate condition is still OPEN, and it is not a defect:** the `corpus/SOURCES.md` S102 row had not landed when I ran the checks (HEAD `82b3b7d4704e914eb224e7bb24e57aa9cbd8603f`). So `capture-binding-check.py` currently prints `records=82 bound=81 unbound=1` and exits 1, failing only on `rule=no-row record=S102`. The C2 target `records=82 bound=82 unbound=0` is **not yet measured as holding**. It holds only after the row lands and the checker is rerun.

Raw receipts are in `.ufo/waves/round-68/w1/ReviewC2/01..07-*.txt`. Each one starts with its exact command and ends with its exit code. All commands ran with cwd `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## (1) source-recheck — receipt `01-source-recheck.txt`
```
$ python3 corpus/instruments/source-recheck.py --manifest /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-68/manifest.json --source S102
S102:sha256 OK
S102:Q01-description OK occurrences=1 anchor=13-ok
S102:Q02-title OK occurrences=1 anchor=14-ok
S102:Q04-operation OK occurrences=1 anchor=24-ok
S102:Q05-commit-parameter OK occurrences=1 anchor=30-ok
S102:Q06-200-schema OK occurrences=1 anchor=37-ok
S102:Q07-repo-name OK occurrences=1 anchor=285-ok
S102:Q08-repo-commit OK occurrences=1 anchor=290-ok
S102:Q09-aggregate-score OK occurrences=1 anchor=353-ok
exit=0
```

## (2) Digest and line count from disk — receipt `02-sha-lines.txt`
```
6ebb8552ac3e0c4085f4a9239e29551fa1be19cebbdf99ccabb96400d8c2caa0  corpus/source-snapshots/round-68/S102.txt
429 corpus/source-snapshots/round-68/S102.txt
7595 corpus/source-snapshots/round-68/S102.txt
```
The sha256 and line count from disk match the manifest (`sha256` 6ebb8552…c2caa0, `lines` 429) and the frozen claim pins (`capture_sha256`, `capture_lines` 429).

The manifest's `bytes: 11802` is **not** the size of the file on disk (7595). It is the served response size, before whitespace collapse. This follows the lane's existing convention: round-67 S100 has `bytes` 82978 against a 59068-byte file, and S101 has 644190 against 58889. My refetch confirms the figure (see the next section). This is not a defect, but the field name is ambiguous.

### Independent reproduction (going beyond the brief) — receipt `07-refetch-reproduce.txt`
I fetched the URL fresh at 2026-11-04T21:54:13Z with `curl` and ran the lane's own `capture-source.py collapse()` on it, loaded as a module with nothing written to the lane:
```
http=200 size=11802 final=https://api.securityscorecards.dev/swagger.json
served_bytes=11802 collapsed_bytes=7595 collapsed_lines=429 sha256=6ebb8552ac3e0c4085f4a9239e29551fa1be19cebbdf99ccabb96400d8c2caa0
byte_identical_to_S102= True
swagger= 2.0 info.version= 1.1.0 host= api.scorecard.dev
definitions= ['Error', 'Repo', 'ScorecardCheck', 'ScorecardResult', 'ScorecardVersion', 'VerifiedScorecardResult', 'VersionInfo']
paths= ['/projects/{platform}/{org}/{repo}', '/projects/{platform}/{org}/{repo}/badge', '/version']
```
The committed capture is byte-identical to a fresh fetch passed through the documented pipeline. The manifest's `bytes` 11802, the http 200 and the `final_url` all reproduce. The facts the claim names (swagger 2.0, info.version 1.1.0, host api.scorecard.dev, and the ScorecardResult/ScorecardCheck/Repo/Error definitions) are all in the served document. The document also defines three more types the claim does not name: ScorecardVersion, VerifiedScorecardResult and VersionInfo. The served bytes are live data and could drift after this instant.

## (3) capture-binding-check rules applied to the round-68 manifest — receipt `03-capture-binding-check.txt`
These are the relevant output lines:
```
MANIFEST round-68 records=1 url_bound=0 fetched=1 archival=0
AUDIT records=82 with_url=82 with_fetched_utc=44 with_archival=38 snapshot_dirs=41 manifest_dirs=41 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
FAIL rule=no-row record=S102 dir=round-68
records=82 bound=81 unbound=1
rc=1
$ grep -c "^| S102 |" corpus/SOURCES.md
0
```
I worked through each docstring rule:

| Rule | Round-68 result | Evidence |
|---|---|---|
| A: manifest present, per-file binding | **Satisfied.** The directory holds only `S102.txt` and `manifest.json`; S102.txt is named by `path`, and there is no `orphans` key. | `06-dir.txt`; the checker prints no orphan-capture FAIL for round-68 |
| B1: row exists | **Not yet satisfiable.** There is no `\| S102 \|` row in SOURCES.md. | `FAIL rule=no-row record=S102`, grep count 0 |
| B2: id unique | Pending the row. S102 currently occurs nowhere in SOURCES.md. | grep 0 |
| B3: row not `rejected` | Pending the row. | — |
| B4: exactly one `https://` token in the source cell | Pending the row. | — |
| B5: record `url` equals the row's https token byte-for-byte | Pending the row. | — |
| C: provenance | **Satisfied.** `fetched_utc` is `2026-11-04T21:49:46Z`, strict UTC. Round 68 counts as a modern round, so the archival exemption is closed. | `fetched=1` |
| D: no duplicate id/path in the manifest | **Satisfied.** There is one record. | no dup-record FAIL |
| E1: path resolves inside the directory to a regular file | **Satisfied.** | no capture-missing FAIL |
| E2: sha256 matches the file | **Satisfied.** The digest is well-formed 64-char hex. | no digest FAIL; (2) |
| E3: `capture_url` = `http.final_url` = `url` | **Satisfied.** All three are `https://api.securityscorecards.dev/swagger.json`. | no capture-url-mismatch FAIL |

The one FAIL in the whole tree is `no-row S102`. Every other directory binds, and the orphan `S040-live.txt` belongs to a different directory's declared orphan set, with no FAIL line printed for it.

**Requirements for the integrator's S102 row** (these follow from rules B4 and B5, and I have not observed the row): the source cell must carry exactly **one** `https://` token, and that token must equal `https://api.securityscorecards.dev/swagger.json` byte-for-byte. If the row's prose writes the `host` value `api.scorecard.dev` as an `https://` URL, it fails B4 (`double-https-row`) and the record becomes `url-ambiguous`. The status must not be `rejected`, and the id must be unique.

## (4) Gate ≤25-word rule — receipt `04-wordcount.txt`
Each quote was fed through `wc -w`: Q01 9, Q02 3, Q04 4, Q05 7, Q06 7, Q07 4, Q08 9, Q09 5. **The maximum is 9 words** (Q01 and Q08), so all 8 quotes are within 25 words. Each quote occurs exactly once in the capture.

The quote ids skip Q03 (Q01, Q02, Q04…Q09). The manifest gives no reason, and since the ids are labels only, this is informational.

## (5) Line anchors — receipt `05-anchors.txt`
```
13: "description": "API to interact with a project's published Scorecard result",
14: "title": "OpenSSF Scorecard API",
24: "summary": "Get a repository's ScorecardResult",
30: "description": "SHA1 commit hash expressed in hexadecimal format",
37: "description": "A JSON object of the repository's ScorecardResult",
285: "description": "respository that was analyzed",
290: "description": "SHA1 value of the analyzed commit expressed as hexadecimal",
353: "description": "Aggregate score of the repository",
```
All 8 anchors show the quoted text on exactly the stated line. A Python substring test (`quote in lines[anchor-1]`) returned True for all 8. Q07's "respository" typo is faithful to the source: it is in the served bytes, which reproduce byte-identically. Any Gate block that cites it should keep the spelling verbatim.

## (6) No orphan, S103 absent — receipt `06-dir.txt`
- The directory holds `manifest.json` (2762 B) and `S102.txt` (7595 B), and nothing else.
- `grep -c S103` on the manifest returns `0`.
- `git ls-tree -r HEAD` for round-68 lists only those two files.
- `git log --all -- 'corpus/source-snapshots/round-68/S103*'` is empty, so S103 was never committed in any ref.
- The manifest note says "only S102 is recorded here" and has no top-level `orphans` key.

## Open items and disagreements
1. **OPEN:** The C2 condition `records=82 bound=82 unbound=0` has not been measured as holding. It currently reads `bound=81 unbound=1`, exit 1, and the only cause is the missing S102 row. The L1 must rerun `capture-binding-check.py` after the row lands. I did not observe the row and did not run the census, frontier-recheck or knowledge counts, because the brief did not ask for them and they also depend on the row.
2. The manifest's `bytes` field means served bytes, not capture bytes. It is consistent with the round-67 convention, but a reader could take it as the file size.
3. The Q03 gap in the quote ids is informational.
4. The capture-source reproduction depends on live data and only covers 2026-11-04T21:54:13Z.

## Tooling and hygiene
- I installed nothing.
- Scratch was `/fast/scratch/hyaku/kasegi-r68/ReviewC2/` (fetched `served.json`, `served2.json`), and I removed it before yielding.
- I ran no git mutation and wrote nothing outside this report and its receipt directory.
