# ExecSourceCapture — round 43, S067 capture

Lane kasegi-shokunin, round 43, base ab98fac9dce87130bc4f66de89e30650d63943dc. Leaf seat: one source, no dispatch.

## Source

**https://curl.se/docs/CVE-2025-9086.html** — "curl - Out of bounds read for cookie path - CVE-2025-9086",
"Project curl Security Advisory, September 10 2025". Designated by the wave's source hunter
(`w1/ScoutSourceHunt.md`, "Capture this URL and no other") and captured as S067.

Why it fits: public HTML, no login, no cookie, no customer data, no live target (the repro text uses
the placeholder host `target`); first-party (curl.se is the project's own disclosure page — it names
`Reported-by: Google Big Sleep` / `Patched-by: Daniel Stenberg` and the fixed-in commit), and it
carries the report/provenance/status split a claim package must reproduce: VULNERABILITY + INFO
(report), AFFECTED VERSIONS + SOLUTION + RECOMMENDATIONS (status), TIMELINE + CREDITS (provenance),
with severity `Severity: Low` and `CWE-125: Out-of-bounds Read` in the same document.

Boundary kept from the scout's screen: the JSON sibling, the `/dev/vuln-disclosure.html` policy page,
the HackerOne original report and `GHSA-v676-f8gm-92r9` (the S068 reject) are **not** part of this
capture. The served fix link at L97 is the truncated 29-char prefix; the full 40-char hash exists only
in the JSON sibling and was not spliced in. L84's `Bug bounty: 505 USD` is an award on this advisory,
not a standing reward ladder — it must not be cited as the project's policy.

### Superseded draft (disclosed, not present in deliverables)

Before the scout's routing arrived I captured `https://curl.se/docs/CVE-2023-38545.html` as S067
(13940 B raw, sha256 `e9038f569b4dfe6b9fc0e2b8e984bba908f093254de4f928c636d98ae3372a30`; 131-line
snapshot, sha256 `327bc909e01ee3dc78272c06d3d568b78e92e5b4c35c7e527394422d763b238b`). It was replaced
byte-for-byte by the designated capture below, the deliverables were overwritten, and
ExecRegistryRows was corrected with the new URL, digests and anchors. Nothing of the 2023 advisory
survives in `w1/ExecSourceCapture.*`.

KasegiR43's standing call (received after this seat yielded): this seat stands down on the S067
registry row; the L1 owns the corpus landing and writes the row from the capture that is on disk and
rechecked — the CVE-2025-9086 set above. Both sources are named here so the round report can cite the
superseded capture and the landed one.

## Commands and real output

Scratch: `S=/fast/scratch/hyaku/kasegi-r43/ExecSourceCapture`, removed after use (verified below).
Disk guard before the pass (`bash scripts/hyaku/disk-guard.sh status`): `/fast/scratch/hyaku` 25%
used, 607.1G free.

1. Raw fetch, unauthenticated, redirect chain recorded:

```
$ date -u +%Y-%m-%dT%H:%M:%SZ; curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 \
    -D raw.headers -o raw.html -w 'code=%{http_code} bytes=%{size_download} redirects=%{num_redirects} effective=%{url_effective}' \
    https://curl.se/docs/CVE-2025-9086.html; date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-28T16:46:33Z
code=200 bytes=10455 redirects=0 effective=https://curl.se/docs/CVE-2025-9086.html
2026-10-28T16:46:34Z
$ sha256sum raw.html; wc -c raw.html
58ca99006c3299456ae7a40a0fb268cef6213f1ce5d07eb2c98f1dcc56716ebd  raw.html
10455 raw.html
```

Headers: `HTTP/2 200`, `content-type: text/html`, `content-length: 10455`,
`last-modified: Sun, 25 Oct 2026 11:18:21 GMT`, `etag: "28d7-65ea85f0593b9"`,
`date: Wed, 28 Oct 2026 16:46:34Z`, `via: 1.1 varnish, 1.1 varnish`, `x-cache: HIT, HIT`.
Zero redirects: requested URL == effective URL. The body digest equals the scout's independent fetch
digest (`w1/ScoutSourceHunt.md`, 2026-10-28T16:40:33Z), so two fetches saw the same document.

2. Normalization by the committed instrument, `--kind html` (the page is HTML; the seat's
`--kind text` allowance is for plain text/JSON and was not used):

```
$ python3 corpus/instruments/capture-source.py --id S067 \
    --url https://curl.se/docs/CVE-2025-9086.html --out "$S/instrument/S067.txt" --kind html
S067 status=200 fetched_bytes=10455 snapshot_bytes=3822 sha256=7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b utc=2026-10-28T16:46:41Z out=/fast/scratch/hyaku/kasegi-r43/ExecSourceCapture/instrument/S067.txt
rc=0
```

Binding the raw digest to the landed snapshot — normalize the curl-captured bytes with the
instrument's own `html_to_text`:

```
raw bytes 10455
raw sha256 58ca99006c3299456ae7a40a0fb268cef6213f1ce5d07eb2c98f1dcc56716ebd
norm sha256 7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b
norm lines 109   norm bytes 3822
```

All three independent paths (curl bytes, instrument refetch, scout's local normalization) agree on
`7e35413a…f975c8b` / 3822 bytes / 109 lines.

3. Quote anchors, computed against the snapshot and required unique + ≤25 words:

```
Q1 lines [69]  occurrences 1 words 8   Project curl Security Advisory, September 10 2025 Permalink
Q2 lines [82]  occurrences 1 words 3   CWE-125: Out-of-bounds Read
Q3 lines [84]  occurrences 1 words 4   Bug bounty: 505 USD
Q4 lines [88]  occurrences 1 words 8   Affected versions: curl 8.13.0 to and including 8.15.0
Q5 lines [97]  occurrences 1 words 2   Fixed-in: https://github.com/curl/curl/commit/c6ae07c6a541e0e96d0040afb6
Q6 lines [103] occurrences 1 words 19  This issue was reported to the curl project on August 11, 2025. We contacted distros@openwall on September 5, 2025.
```

4. Recheck of the manifest copy in scratch (its `path` resolves beside it):

```
$ python3 corpus/instruments/source-recheck.py --manifest "$S/manifest.json" --source S067
S067:sha256 OK
S067:Q1 OK occurrences=1 anchor=69-ok
S067:Q2 OK occurrences=1 anchor=82-ok
S067:Q3 OK occurrences=1 anchor=84-ok
S067:Q4 OK occurrences=1 anchor=88-ok
S067:Q5 OK occurrences=1 anchor=97-ok
S067:Q6 OK occurrences=1 anchor=103-ok
rc=0
```

sha256 OK and Q1..Q6 OK (seat floor was Q1..Q4; six were pinned because the package needs the
severity, the reward line, both version ranges and the fix link, not just three).

## Deliverables (in .ufo/waves/round-43/w1/)

| file | bytes | lines | sha256 |
|---|---|---|---|
| `ExecSourceCapture.S067.txt` (land at `corpus/source-snapshots/round-43/S067.txt`) | 3822 | 109 | `7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b` |
| `ExecSourceCapture.manifest.json` (schema_version 1, one record, `sources[0].path = "S067.txt"`, six quotes) | 1195 | 48 | `716e34872460552f868a9a41c772e2b6d1967301bcbec133451ff70551158b13` |
| `ExecSourceCapture.provenance.txt` | 4102 | 73 | `827e8c82c3dbd6eba5f6eee6df4e5b5789700bfa8b483926c0e931df4f690f7c` |

Manifest record fields: `id S067`, `url`, `kind html`, `fetched_utc 2026-10-28T16:46:34Z`,
`path S067.txt`, `sha256` (normalized snapshot), `bytes 10455` (raw served), `snapshot_bytes 3822`,
`lines 109`, `raw_sha256`, `quotes[Q1..Q6]` each with `anchor`.

The capture is the complete document: nav chrome L1-L68, advisory body L69-L109, nothing sliced.

## Write scope / cleanliness

Only the three deliverables above plus this receipt were written, all under
`.ufo/waves/round-43/w1/`. No write to `corpus/` (the L1 lands the bytes), no write to the fleet
root, shokuknow, or any PATH directory. No mutating git ran anywhere. Scratch
`/fast/scratch/hyaku/kasegi-r43/ExecSourceCapture` removed and verified absent.

Tooling: nothing installed or upgraded. `curl`, `python3`, `sha256sum` as present on the host
(pacman was not run — host-wide pause respected).

## Risks / boundaries

- The snapshot records what curl.se served at 2026-10-28T16:46:34Z; it does not assert current
  advisability or byte stability. `ETag`/`Last-Modified` are in the provenance file so a later
  recheck can detect drift. `last-modified: 2026-10-25` postdates the 2025 publication, so the page
  is a re-render; the captured body is the advisory text.
- The advisory's `Original report:` link (L86) points at HackerOne, which serves a JavaScript shell
  to this user agent (per `w1/ScoutSourceHunt.md`); it was not fetched and no second-party bytes
  underpin this capture.
- L97's commit link is the served prefix. A consumer wanting the full hash must take the JSON sibling
  record, which is not this snapshot; splicing it in would break byte binding.
