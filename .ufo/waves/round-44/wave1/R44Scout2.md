# R44Scout2 — separate F26 candidate: OSV package interchange

## Finding

**Candidate, not an admission.** The public primary for a disclosure-package / data-exchange frontier that is not CVE, CVSS, SSVC, KEV, or VEX is the Open Source Vulnerability schema, OpenSSF's own document at `https://ossf.github.io/osv-schema/`.

It is the interchange record for a vulnerability in an open-source package: package identity (`ecosystem`, `name`, optional `purl`) plus an affected-range timeline (`introduced`, `fixed`, `last_affected`, `limit`). That is the residual named by the committed S065 flip. It is not the uncommitted working-tree F26, which is Google Cloud VRP program scope.

Re-opened 2026-10-28. Raw body sha256 `8cf1e3d3f9e10eba902d03af6c281d6bc5e71c22dc351fcb4b811c64030570e8` (228890 bytes) matches the S065 reject record byte for byte. `last-modified: Wed, 14 Oct 2026 01:54:20 GMT`. Inside the page: `Version 1.9.2 (October 13, 2026)` at normalized line 4.

No frontier row was added. Do-nothing at HEAD still cannot reach an OSV admission.

## Quotes (verbatim, ≤25 words)

Normalized capture of the published page (`capture-source.py --kind html`). Each quoted string occurred once. The apostrophe in "object's" / "object's" below is U+2019.

| quote | words | locus |
|---|---|---|
| This document defines a standard interchange format for describing vulnerabilities in open source packages. | 14 | L9–L10 (sentence split after "describing") |
| Version 1.9.2 (October 13, 2026) | 5 | L4, the whole line |
| The ranges object’s events field is a JSON array of objects. | 11 | L737, sentence ending before "Each object" |
| Introduces a vulnerability: {"introduced": string} | 5 | L739, the whole line |
| There must be at least one introduced object in the events array. | 12 | L777, sentence ending before "While" |
| The object itself has two required fields, ecosystem and name, and an optional purl field. | 15 | L549–L550 |
| The meaning of the values within the object is entirely defined by the database and beyond the scope of this document. | 21 | L791–L793 (`database_specific`) |
| Values in this field have no effect on the evaluation algorithm. | 11 | L795–L796 |
| The severity field is a JSON array that allows generating systems to describe the severity of a vulnerability using one or more quantitative scoring methods. | 25 | L460–L461 |

The four event lines under L737 are L739 `introduced`, L740 `fixed`, L741 `last_affected`, L742 `limit`. `CVSS_V4` is a `severity[].type` label at L473, beside `CVSS_V2` (L469) and `CVSS_V3` (L471).

## What this is not

Committed frontier rows that this candidate does not repeat:

- CVE record shape is F25 / `corpus/knowledge/cve-json-record-format.md` / S064. In `corpus/source-snapshots/round-42/S064.txt`, `introduced`, `last_affected`, and `database_specific` each occur 0 times. CVE ranges are `version` + `status` + `lessThan` / `lessThanOrEqual` (status enum `affected` / `unaffected` / `unknown` at L128–L135; `lessThan` at L411–L416). `packageURL` "MUST NOT include a version" (L449). OSV's event objects are a different model. CVE can express ranges; it does not express this event vocabulary.
- CVSS is F01 / S001 / S002. OSV only stores a vector string as one `severity[].type`. L460–L461 defines the severity array; it does not define CVSS.
- SSVC is F20. KEV is F18. VEX product status is F21 (S055); VEX issuance is F22 (S057). CycloneDX `analysis` is F23. `security.txt` is F24.
- On the opened OSV page, `SSVC|KEV|VEX|CVSS_V4|CycloneDX|CSAF` hit only L473 `CVSS_V4`.

`database_specific` is the wrong load-bearing field. L791–L796 say its meaning is database-defined, beyond the document, and that its values do not affect evaluation. The schema-level residual is the events timeline. The flip's `extracted_events` example is one database's extension (kaidoku S015), not the evaluation rule.

## Registry and the F26 label

HEAD `66314015122b9aa32dc40f2f1815df56624c26d1` (descendant of freeze `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`):

- S065 is `corpus/SOURCES.md:71`, status `rejected`, used-by `—`, no lane capture. Flip text: "re-open OSV if the F25 row/knowledge entry for the CVE Record Format is withdrawn, or if a future frontier needs OSV-specific range semantics (affected[].ranges[].events / database_specific extracted_events) that the CVE format cannot express".
- No `corpus/knowledge/*.md` file at HEAD cites `osv-schema`.
- Admitted frontier count at HEAD is 25. `git grep F26 HEAD -- corpus/README.md` printed nothing. Knowledge markdown count 62. Registry rows 68. Highest HEAD id is S068 at line 74. S069 is absent at HEAD.
- Sibling `kaidoku-shokunin/corpus/SOURCES.md:21` S015 is one API instance, `https://api.osv.dev/v1/vulns/CVE-2025-55305`, not this schema URL. That was the r42 disjointness tie-break, not a quality rejection of the schema.

Working tree, not this seat and not committed (`git status --porcelain` showed `M corpus/README.md`, `M corpus/SOURCES.md`, `?? corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`):

- `corpus/README.md:628` drafts F26 as "Google Cloud VRP's own program scope, customer-resource testing prohibition and reward-ineligibility boundary", source S069.
- `corpus/SOURCES.md:75` is that S069 row. S070 at line 76 is a rejected directory page.

Those drafts are program-scope text. They do not cover package interchange. Filing OSV as a second F26 would collide with that draft. Against committed HEAD the F26 id is unused, so OSV is a valid F26 candidate there. This seat does not choose between them and does not edit either file.

A status flip of S065 does not raise the S-row census (rejected rows already count). S065's own anchor says there is no lane capture. If C2 needs a newly opened row id, the S059-rejected / S060-scoped-capture pattern is the precedent; this seat does not assign an id.

## Do-nothing

`.ufo/waves/round-44/controls/do-nothing.txt:9-13` records 25 admitted frontier rows, 68 source rows, 62 knowledge files, and no F26. Re-measured at HEAD this seat: the same three counts, and no F26. S065 stays `rejected`. Replaying do-nothing does not admit this candidate and does not create the Cloud VRP draft.

## Commands and outputs

Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. `git rev-parse --show-toplevel` printed that path.

```
git rev-parse HEAD
66314015122b9aa32dc40f2f1815df56624c26d1

git merge-base --is-ancestor 5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a HEAD
exit 0

git grep -cE '^\| F[0-9]+ \| .* \| admitted \|' HEAD -- corpus/README.md
HEAD:corpus/README.md:25

git grep -n F26 HEAD -- corpus/README.md
(no matches)

git ls-tree -r --name-only HEAD corpus/knowledge | grep -c '\.md$'
62

git show HEAD:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
68
```

HEAD S065 cells from a `|` split: line 71, status `rejected`, used-by `—`.

Capture, from the lane root, `--out` under scratch only:

```
python3 corpus/instruments/capture-source.py --id OSV-HTML \
  --url https://ossf.github.io/osv-schema/ --kind html \
  --out $SCRATCH/osv-schema.html.txt
OSV-HTML status=200 fetched_bytes=228890 snapshot_bytes=70913 \
  sha256=97b850a4bcd90600bb39391df3293e4591b9dd84170e94ecfd48f40e08cfeda9 \
  utc=2026-10-28T18:59:51Z
```

Raw body of the same URL, same UA as `corpus/instruments/capture-source.py` (`kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`):

```
HTTP/2 200
content-type: text/html; charset=utf-8
last-modified: Wed, 14 Oct 2026 01:54:20 GMT
date: Wed, 28 Oct 2026 19:00:26 GMT
raw_bytes 228890
raw_sha256 8cf1e3d3f9e10eba902d03af6c281d6bc5e71c22dc351fcb4b811c64030570e8
match True   # equal to the S065 reject-record digest
```

`grep -c` on `corpus/source-snapshots/round-42/S064.txt`: `introduced 0`, `last_affected 0`, `database_specific 0`.

## Drift (not the locus)

`main` is ahead of the published page. Fetched the same minute:

- `https://raw.githubusercontent.com/ossf/osv-schema/main/docs/schema.md` — status 200, fetched_bytes 95198, snapshot sha256 `617661a61b9f4313a54bc2df3012a68df217f6aba51c33b864f8cf3f78c9d1ad`
- `https://raw.githubusercontent.com/ossf/osv-schema/main/validation/schema.json` — status 200, fetched_bytes 16915, snapshot sha256 `88b236342815d1a22d49618cd64622a0bbc5c86b9bd5419fe812df80b4ecec21`
- Commits API for `docs/schema.md`: `cfe70141baa3cc24184333c4bdf393f3a6fe9b07`, 2026-10-14T23:14:47Z, "Add Raspberry Pi OS ecosystem and RPI prefix (#631)"

`Raspberry` / `RPI` occur in those two `main` files and zero times in the published-page capture. Quotes above are from the published page only. `schema.json` line 99 ("events must contain an introduced object and may contain fixed, last_affected or limit objects") is the later tree, not an S065 locus.

## Limits

- Recon only. No corpus capture, no manifest row, no knowledge entry, no README edit. Q2's "opened in the admitting round" is not met by this scratch fetch.
- The normalized snapshot sha lives only in this report; scratch is deleted on exit. Recheck is a fresh `capture-source.py` of the same URL. The raw sha is already the S065 pin.
- `main` and the published page disagree. Citing `main` line numbers as the page would be false.
- The S065 flip overstates the CVE gap if read as "CVE cannot express ranges." S064 expresses ranges with `lessThan` and a three-value status enum.
- `HYAKU_SCRATCH` was unset. Scratch was `/home/vgpnk/.hyaku/kasegi-r44/R44Scout2` (not `/tmp`). Removed on exit.
- No tool installed. `RULES.md` read. Pacman not invoked. `git rev-parse --show-toplevel` was the lane root before the read-only git commands. No commit, push, or index change.

## Tools

None installed. Channel: none. Python 3 and `corpus/instruments/capture-source.py` plus curl were already on the host.
