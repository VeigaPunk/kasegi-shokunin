# ExecRegistryRows — kasegi round 43, wave 1 receipt

Seat: ExecRegistryRows (leaf executor; no subagents, no swarm, no second judge).
Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Frozen claims read first and never edited: `.ufo/waves/round-43/claims.json`.
Axes this seat moves: `coverage` (S067 mined, S068 rejected) and `depth:verifiability` (each row is
line-anchored to measured capture bytes, and the delivered rows are run through the census validator,
`capture-binding-check.py` and `source-recheck.py` before hand-off).

## Deliverables (final bytes)

| file | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-43/w1/ExecRegistryRows.rows.txt` | 2 | 3262 | `6e8a2ee4fbc67cb3c53420bf924c35b896d8850deffa7de03284a352b408bd3a` |
| `.ufo/waves/round-43/w1/ExecRegistryRows.searchlog.txt` | 1 | 2814 | `2a0daa2faa88e572eadadd9f5c4bc58d10026400c181769b14f7533e38880770` |
| `.ufo/waves/round-43/w1/ExecRegistryRows.dupcheck.txt` | 45 | 2692 | `53ca55d096b14df1f20a2c8371ae06ee7fa38aabdaf911a9704e5f837753ed6f` |

Install point: `rows.txt` appends after the `| S066 |` row (registry L72, inside `## Registry`, before the blank
line that ends the table); `searchlog.txt` appends as one bullet under `## Search log`. No pre-existing row's
status, recheck or used-by cell is changed, so no old → new entry belongs under `## Registry changes`.

## Two mid-wave supersessions (recorded, because this seat rewrote both rows)

1. S067 first arrived from ExecSourceCapture as the curl advisory for CVE-2023-38545 (131-line capture,
   sha256 `327bc909…3b238b`). The capture seat then overwrote its own deliverable with the curl advisory for
   CVE-2025-9086, on ScoutSourceHunt's direction. The S067 row was rewritten against the overwritten capture and
   every number in it was re-measured from the new bytes. A second supersession had already moved S068 off Mozilla
   Foundation Security Advisory 2026-99 — which this seat had screened and measured — onto the scout's
   GHSA-v676-f8gm-92r9 reject, which this seat re-fetched and re-measured independently. No superseded number
   survives in the delivered `rows.txt`; ScribeLessonDraft was told in the same step that S068 changed.

## Rows delivered

S067 — mined. `Project curl security advisory, CVE-2025-9086 (out-of-bounds read for cookie path)` —
`https://curl.se/docs/CVE-2025-9086.html`, kind `docs`, tier A (the curl project's own advisory of its own CVE:
weakness class, severity, affected and not-affected ranges, fix, timeline and credit all first-party), scope
narrowed to that one finding, status `mined`, opened `2026-10-28`, recheck `annual`,
used-by `corpus/knowledge/claim-package-gate.md`.

S068 — rejected. `GitHub Advisory Database entry GHSA-v676-f8gm-92r9 for CVE-2025-9086` —
`https://github.com/advisories/GHSA-v676-f8gm-92r9`, kind `docs`, tier B (a curated database republishing NVD's
record, not the disclosing party's own write-up). Rejected on primary-of-record and record completeness: the page
is self-labelled `Unreviewed`, lists no package, records affected and patched versions both `Unknown`, states
`No known source code`, and names the project's own advisory only as one reference — that advisory is this round's
S067. Flip condition is in the row (Reviewed status plus a named package with per-version affected/patched ranges
or the fixing commit).

Kind vocabulary: the census accepts `spec|docs|paper|code|tool|dataset|talk|book|community|own-work`
(`scripts/sources-census.sh:655`); `advisory` is not a kind, so `docs` is the honest value for both rows.

## Evidence — S067 capture bytes and anchors (re-verified from the delivered file)

```
$ cd .ufo/waves/round-43/w1
$ sha256sum ExecSourceCapture.S067.txt
7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b  ExecSourceCapture.S067.txt
$ wc -lc ExecSourceCapture.S067.txt
109 3822 ExecSourceCapture.S067.txt
$ sed -n '69p;82,84p;88,90p;97p;103p' ExecSourceCapture.S067.txt
Project curl Security Advisory, September 10 2025 Permalink
CWE-125: Out-of-bounds Read
Severity: Low
Bug bounty: 505 USD
Affected versions: curl 8.13.0 to and including 8.15.0
Not affected versions: curl < 8.13.0 and >= 8.16.0
Not affected versions: curl >= 8.14.2 in the 8.14.X branch
Fixed-in: https://github.com/curl/curl/commit/c6ae07c6a541e0e96d0040afb6
This issue was reported to the curl project on August 11, 2025. We contacted distros@openwall on September 5, 2025.
```

The row also cites L81 (CVE assignment), L85 (area), L99 (upgrade recommendation), L104 (release line) and
L107-L108 (`Reported-by: Google Big Sleep`, `Patched-by: Daniel Stenberg`), all read from the same file. The
`Fixed-in` line serves a truncated 29-character hash; the row cites only the line, never splices the full hash, and
the 505 USD figure is described as an award on this advisory, not as a standing bounty ladder.

## Evidence — the rows bind to the capture bytes

A scratch pseudo-lane was built under the seat scratch dir (since removed) holding the lane `corpus/SOURCES.md`
with the delivered rows inserted after S066, the real `corpus/knowledge` tree plus a one-line placeholder for
`claim-package-gate.md`, the delivered capture as `corpus/source-snapshots/round-43/S067.txt`, the delivered
manifest as `corpus/source-snapshots/round-43/manifest.json`, and the fleet `shokunin.conf`.

```
$ python3 corpus/instruments/capture-binding-check.py --root <scratch>/root/kasegi-shokunin
MANIFEST round-43 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=1 with_url=1 with_fetched_utc=1 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 digest_unpinned=0 orphans=0
records=1 bound=1 unbound=0
bind_rc=0

$ python3 corpus/instruments/source-recheck.py --manifest <scratch>/root/kasegi-shokunin/corpus/source-snapshots/round-43/manifest.json --source S067
S067:sha256 OK
S067:Q1 OK occurrences=1 anchor=69-ok
S067:Q2 OK occurrences=1 anchor=82-ok
S067:Q3 OK occurrences=1 anchor=84-ok
S067:Q4 OK occurrences=1 anchor=88-ok
S067:Q5 OK occurrences=1 anchor=97-ok
S067:Q6 OK occurrences=1 anchor=103-ok
recheck_rc=0
```

## Evidence — row shape, ids, census

```
$ awk -F'|' '{printf "line %d NF=%d\n", NR, NF}' ExecRegistryRows.rows.txt
line 1 NF=13
line 2 NF=13
$ (per row) grep -oE 'https?://[^ |]+' | wc -l
1
1
```

`NF=13` is the 11-cell + 2-outer-pipe shape (no literal or escaped pipe in a cell); each row carries exactly one
`https://` token, and the S067 token is byte-equal to the manifest's `url` (rule B5, proven by the binding run).

Census validator over the pseudo-lane (the only way to exercise E11 before the knowledge entry exists; the real
`corpus/knowledge/claim-package-gate.md` is another seat's deliverable):

```
$ bash scripts/sources-census.sh validate --root <scratch>/root kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	<scratch>/root/kasegi-shokunin/corpus/SOURCES.md
census_rc=0
```

Only the two pre-existing W04 warnings the live lane already prints; no E01/E03/E04/E05/E06/E07/E08/E09/E11/E12 and
no W01/W02/W03 on the new rows. Registry rows in the pseudo-lane: 66 → 68.

Duplicate check against the live registry (full transcript in `ExecRegistryRows.dupcheck.txt`):

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort | uniq -d
(no output)
$ grep -nE '^\| *S06[78] *\|' corpus/SOURCES.md
(no output; exit 1)
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
66
```

## Evidence — S068 screening ledger (real fetches, 2026-10-28 UTC)

`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`, bodies saved under the seat scratch dir:

| # | URL | HTTP | bytes | fetched (UTC) |
|---|---|---|---|---|
| 1 | https://www.zerodayinitiative.com/advisories/published/ | 200 | 2551868 | 2026-10-28T16:40:09Z |
| 2 | https://github.com/advisories | 200 | 241861 | 2026-10-28T16:40:09Z |
| 3 | https://www.mozilla.org/en-US/security/advisories/ | 200 | 398327 | 2026-10-28T16:40:11Z |
| 4 | https://www.zerodayinitiative.com/advisories/ZDI-26-811/ | 200 | 26851 | 2026-10-28T16:40:26Z |
| 5 | https://www.mozilla.org/en-US/security/advisories/mfsa2026-99/ | 200 | 57551 | 2026-10-28T16:40:27Z |
| 6 | https://github.com/advisories/GHSA-v6mg-96c6-gmpq | 200 | 142056 | 2026-10-28T16:40:27Z |
| 7 | https://github.com/advisories/GHSA-v676-f8gm-92r9 | 200 | 141796 | 2026-10-28T16:46:26Z |

S068's page, normalized twice through the lane's own instrument:

```
$ python3 corpus/instruments/capture-source.py --id S068 --url https://github.com/advisories/GHSA-v676-f8gm-92r9 --out <scratch>/ghsa1.txt --kind html
S068 status=200 fetched_bytes=141795 snapshot_bytes=5936 sha256=530cbcf9925b082f9effea7bbc5e96650949794d80893d7ac8ec5e289b4c97e6 utc=2026-10-28T16:46:43Z
$ python3 corpus/instruments/capture-source.py --id S068 --url https://github.com/advisories/GHSA-v676-f8gm-92r9 --out <scratch>/ghsa2.txt --kind html
S068 status=200 fetched_bytes=141796 snapshot_bytes=5936 sha256=530cbcf9925b082f9effea7bbc5e96650949794d80893d7ac8ec5e289b4c97e6 utc=2026-10-28T16:46:43Z
$ cmp -s <scratch>/ghsa1.txt <scratch>/ghsa2.txt && echo identical
identical
$ wc -lc <scratch>/ghsa1.txt
191 5936
```

The served HTML is **not** byte-stable across fetches (141795 and 141796 bytes, and different raw digests: my curl
fetch hashed `95b33146…3401f`, the scout's `f238e2fe…24b497` at the same 141796-byte length), while the
instrument-normalized text is byte-identical on both runs — so the row pins the normalized digest
`530cbcf9…4c97e6` at 191 lines and says so explicitly.

Structural facts on that normalized text, as the row states them:

```
Unreviewed label L64 and L68   title L66   High severity L67
No package listed L75          affected versions Unknown L78   patched versions Unknown L80
Published by the National Vulnerability Database L105          CWE-125 L161
No known source code L170      Dependabot unsupported L171
```

Candidates screened but not rowed (all measured, all in the search-log bullet): Mozilla Foundation Security
Advisory 2026-99 (43 per-CVE entries, each title plus reporter plus impact tier plus Bugzilla id; `Description` 0,
`Severity` 0, `github.com` 0 occurrences; a single `Fixed in` cell at L57-L58 spanning 43 CVEs; the instrument's
own capture reproduced 57551 bytes / 401 lines / sha256 `2e528893…6ccb44e0` twice), GHSA-v6mg-96c6-gmpq (a
curated database view of an advisory the maintainer published on its own repository), and ZDI-26-811 (a
coordinator record of a third-party product whose remediation statement is the affected vendor's release note:
`Fixed in version 10.60` linking out to MailEnable's notes).

## Duplicate ground beyond ids

```
$ grep -onE 'curl|CVE-2025-9086|8\.16\.0|GHSA-v676|505 USD' corpus/SOURCES.md
94:curl
$ grep -rlnE 'CVE-2025-9086|GHSA-v676' corpus/knowledge
(no output; exit 1)
$ grep -rlE 'CVE-2025-9086|GHSA-v676' /home/vgpnk/Projects/shokunin --include=SOURCES.md
(no output; exit 1)   # over 597 SOURCES.md files (find … | wc -l = 597)
```

The single lane hit is the word "curl" in the round-35 search-log prose at L94, in no table row.

## Tooling

Nothing installed or upgraded: pacman transactions are paused host-wide and none was run; `uv tool install`, `npx`
and `~/.local/bin` were not used. Tools exercised: `curl 8.23.0` (libcurl 8.23.0), `Python 3.14.8`,
`GNU Awk 5.4.1`, `grep`, `sha256sum`. No mutating git/jj command was run — no git command was needed. Disk guard
checked before the last pass: `/fast/scratch/hyaku` at 26% used, 598.7G free, `rc=0`.

## Scratch

`S=/fast/scratch/hyaku/kasegi-r43/ExecRegistryRows` (4.3M at peak, then reused for the S068 screen and the
pseudo-lane rebuild). Removed after the receipt and deliverables were in the wave directory:

```
$ rm -rf -- "$S"; test -d "$S" && echo "SCRATCH STILL PRESENT" || echo "scratch removed: $S absent"
scratch removed: /fast/scratch/hyaku/kasegi-r43/ExecRegistryRows absent
```

## Risks and cross-seat dependencies

- S067's `used-by` cell names `corpus/knowledge/claim-package-gate.md`, which another seat delivers this round.
  Until that file exists on disk the live registry reports `E11 S067 missing used-by`; the pseudo-lane run shows the
  row is clean once it is present. If the entry lands under a different name, the S067 `used-by` cell must change
  with it, and C2's `grep -rlE '^source: S067' corpus/knowledge` count of 1 will otherwise fail.
- S067 moved under this seat once already (CVE-2023-38545 → CVE-2025-9086). Every number in the delivered row was
  re-measured from the final capture bytes; if the capture seat overwrites its deliverable again, the row must be
  re-cut, because the digest, line count and anchors all change together.
- S068 deliberately has no lane capture, so no manifest record may anchor it (binding rule B3 rejects a record on a
  `rejected` row). Its evidence is this receipt plus the recorded raw and normalized measurements; re-verification is
  a refetch of a page whose raw bytes are not stable, which is why the pin is the normalized text.
- Both rows assert only what their pages state. Neither claims the source is current today, that a submission was
  made, or that the exemplar is claimable; `claimable:false` and the operator gates belong to other seats.
