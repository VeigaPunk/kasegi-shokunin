# K73ScoutCapture — S108 capture reproducibility (round 73, attempt 1)

Seat: `K73ScoutCapture` (scout, wave 1). Item: C2's source S108 —
`https://google.github.io/osv.dev/post-v1-query/` — reproducibility of the lane's
capture `corpus/source-snapshots/round-73/S108.txt`.

**Verdict: `S108 reproduces byte-identically`.**

The lane's committed snapshot digest `304baa7db33000b03fe3b9dda9c1823bccbf980f0a69d9a74a936fb312ffc6b9`
(150 lines, 6563 snapshot bytes) is reproduced exactly by an independent re-run of
the lane's own `capture-source.py` against the live URL, and the raw HTML served
twice is byte-identical as well. No per-response nonce is present, so the
round-67 FIRST/PSIRT caveat does **not** apply to this source.

Lane read-only throughout: no git/jj mutation, no write into the lane working tree
except this report directory. Scratch: `/fast/scratch/hyaku/kasegi-r73/K73ScoutCapture`.

## 1 — Two raw fetches

```
$ curl -sS -L -o $S/fetch1.html -w '%{http_code} %{size_download} %{content_type}\n' \
    https://google.github.io/osv.dev/post-v1-query/
200 33417 text/html; charset=utf-8                    exit 0

$ curl -sS -L -o $S/fetch2.html -w '%{http_code} %{size_download} %{content_type}\n' \
    https://google.github.io/osv.dev/post-v1-query/
200 33417 text/html; charset=utf-8                    exit 0
```

| fetch | bytes | raw sha256 |
|---|---|---|
| fetch1.html | 33417 | `5722ec056314f80a70309cd070ec167aa8328b0a8cbe33e6fb77e8d4a1edf4eb` |
| fetch2.html | 33417 | `5722ec056314f80a70309cd070ec167aa8328b0a8cbe33e6fb77e8d4a1edf4eb` |

`sha256sum` exit 0. `cmp $S/fetch1.html $S/fetch2.html` → **exit 0** (raw HTML
identical, not merely equal in length).

## 2 — Re-run of the lane capture instrument

```
$ TMPDIR=$S python3 <lane>/corpus/instruments/capture-source.py --id S108 \
    --url https://google.github.io/osv.dev/post-v1-query/ --kind html \
    --out $S/S108-recapture.txt
S108 status=200 fetched_bytes=33417 snapshot_bytes=6563 \
  sha256=304baa7db33000b03fe3b9dda9c1823bccbf980f0a69d9a74a936fb312ffc6b9 \
  utc=2026-11-05T07:46:13Z out=/fast/scratch/hyaku/kasegi-r73/K73ScoutCapture/S108-recapture.txt
exit 0
```

```
$ cmp $S/S108-recapture.txt <lane>/corpus/source-snapshots/round-73/S108.txt
exit 0     # byte-identical
```

Lane file measured independently: `sha256sum` → `304baa7d…6b9`; `wc -l -c` →
**150 lines, 6563 bytes**. Both match the frozen C2 claim's
(`sha256 304baa7d…6b9`, 150 lines) exactly.

`capture-source.py --selftest` → `selftest normalize=ok deterministic=ok`, **exit 0**.

## 3 — Raw variance and normalized-digest stability

**Raw HTML:** identical between the two fetches (§1), so there is no
per-response variable in the served bytes.

- `grep -c 'nonce' $S/fetch1.html` → **0** (exit 1 = zero matches). The page
  carries no CSP nonce attribute, unlike the round-67 FIRST/PSIRT page which
  injected one into every response.
- Three 32-hex strings do appear in the raw HTML, but they are **page content,
  not nonces**: `6879efc2c1596d11a6a6ad296f80063b558d5e0f` (the `{"commit": …}`
  request sample), `97319697c8f9f6ff27b32589947e1918e3015503` and
  `9cdf439db52b66447b4e37c61179d54fad6c8f33` (response samples). The same three
  appear in the normalized snapshot (3 matches), confirming they are body text.
- Cache headers (`curl -sS -I -L`, exit 0): `HTTP/2 200`, `etag "6aec0805-8289"`,
  `last-modified: Thu, 05 Nov 2026 04:37:25 GMT`, `age: 370`, `x-cache: HIT`,
  `x-origin-cache: HIT`, `content-length: 33417`. The site is a static
  GitHub Pages (Jekyll / "Just the Docs") build — the served bytes are the
  built page, and the snapshot binds them.

**Normalized digest stability across the two fetches:** `capture-source.py` takes
a URL only. A file-path input is **not** supported:

```
$ python3 <lane>/corpus/instruments/capture-source.py --id S108 --url file://$S/fetch2.html \
    --kind html --out $S/S108-fromfetch2.txt
TypeError: %d format: a real number is required, not NoneType   exit 1
```

(`urlopen` returns no `status` for a `file:` URL; the snapshot file was written
before the print statement, and that file's sha256 is `304baa7d…6b9`, identical
to the recapture — `cmp` exit 0 — but the tool exits 1, so it is not a usable
file-path mode.)

Equivalent check executed instead: the instrument's own normalization function
(`html_to_text` from `capture-source.py`) applied to each raw fetch file:

```
fetch1.html raw_bytes=33417 snapshot_bytes=6563 sha256=304baa7db33000b03fe3b9dda9c1823bccbf980f0a69d9a74a936fb312ffc6b9
fetch2.html raw_bytes=33417 snapshot_bytes=6563 sha256=304baa7db33000b03fe3b9dda9c1823bccbf980f0a69d9a74a936fb312ffc6b9
exit 0
```

The normalized snapshot digest is **stable across both fetches** and equals the
lane's committed capture digest.

**Additional variance probes (all exit 0, all HTTP 200, all raw sha256
`5722ec05…4eb`, all 33417 decoded bytes):**

| probe | result |
|---|---|
| cache-buster `?cb=<rand>` (fetch3) | identical |
| the lane's own instrument UA (fetch4) | identical |
| `Cache-Control: no-cache` + `Pragma: no-cache` (fetch5) | identical |
| `--compressed` / `Accept-Encoding: gzip` (fetch6) | identical after decode (`size_download=6472` is the compressed transfer size) |
| `urllib` fetch with the lane UA (the instrument's own client) | `status=200 raw_bytes=33417 raw_sha256=5722ec05…4eb` |

## 4 — The captured content is the POST /v1/query page

On the **fresh** recapture `$S/S108-recapture.txt`:

```
$ grep -c 'POST /v1/query' $S/S108-recapture.txt            -> 6   exit 0
$ grep -c 'pagination\|Pagination' $S/S108-recapture.txt    -> 6   exit 0
```

Structural confirmation: L1 title `POST /v1/query | OSV …`; L26 table of contents
`POST /v1/query Parameters Version rules / Queries for Git records / Payload /
Request samples / Sample 200 response / Pagination`. The five F51 elements named
in the C2 claim are each present and locatable by line:

| F51 element | capture line | text |
|---|---|---|
| request payload | L27–L37 (params) / L58–L67 (JSON payload) | `commit`, `version`, `package{name,ecosystem,purl}`, `page_token` |
| version rule | L40 | "Use either the top-level version field or a versioned purl (pkg:...@<version>), but not both." |
| Git-tag query | L55–L56, L77 | "You can also query for git tags via this API. To do so, set the ecosystem to GIT, enter the full URL of the repository to the name field, and the tag into the version field." |
| pagination | L134–L137 | "The OSV.dev API uses pagination for queries that return a large number of vulnerabilities…" + "…when there more than 1,000 vulnerabilities in the response, or when the query has exceeded 20 seconds." |
| 32 MiB HTTP/1.1 limit | L148 | "The API has a response size limit of 32MiB when using HTTP/1.1. There is no limit when using HTTP/2." |

Occurrence counts for candidate quotes (all exactly once, so a Q9 anchor is not
required for them; only `POST /v1/query` is non-unique at 6 and would need one):

```
"Lists vulnerabilities for given package and version"   1
"Use either the top-level version field"                 1
"You can also query for git tags via this API"           1
"The OSV.dev API uses pagination for queries"             1
"response size limit of 32MiB"                           1
"POST /v1/query"                                         6
```

Independent provenance cross-check: the page's Jekyll source is
`google/osv.dev` → `docs/api/post-v1-query.md`. Fetched
`https://raw.githubusercontent.com/google/osv.dev/master/docs/api/post-v1-query.md`
→ HTTP 200, 8454 bytes, sha256 `f47d4f5dbdbc1d3eca7006afcf2a594daf240042a54125096cb9c0494160cb2c`,
188 lines; upstream L68 is the git-tag sentence, L162 the pagination paragraph,
L186 the 32MiB sentence — i.e. the rendered capture is the current published
source, not a stale or divergent build. (Normalization detail worth noting for
any quote that spans emphasis: upstream "**no limit**" renders as
`<strong>no limit</strong>` and the capture's tag-stripped text reads
"There is no limit when using HTTP/2" at L148.)

## 5 — Lane-tree observations for the integrator (read-only, not fixed by this seat)

These do not affect the S108 capture digest but bear on C2's counters, all
measured with read-only git:

- `git -C <lane> rev-parse HEAD` → `3b53ff839d0747530f95d432aec1ea7b4308fe96`
  (the freeze commit; base `fdf17413`).
- `git -C <lane> status --porcelain corpus/source-snapshots/round-73/` →
  `?? corpus/source-snapshots/round-73/` — **the capture directory is untracked**
  at the freeze commit; only `claims.json` and the two control receipts are
  tracked under `.ufo/waves/round-73/`.
- `ls <lane>/corpus/source-snapshots/round-73/` → `S108.txt` only; **no
  `manifest.json`**, so the round-73 snapshot directory is not yet manifest-bound.
  Consequence, measured: `capture-binding-check.py` on the lane working tree →
  `FAIL rule=missing-manifest dir=round-73` / `records=86 bound=86 unbound=0`,
  **exit 1**. On a clean clone of the freeze commit the same instrument prints
  `records=86 bound=86 unbound=0` with **exit 0** — so the failure is introduced
  by the untracked round-73 directory, not present at base. C2's after-predicate
  (`records=87 bound=87 unbound=0`, exit 0) requires a `manifest.json` in
  `corpus/source-snapshots/round-73/` binding S108 with a `fetched_utc` and the
  pinned quotes.
- `grep -c S108 <lane>/corpus/SOURCES.md` → **0**: no registry row for S108 yet
  (the registry holds 107 `S…` rows, ending at S107). capture-binding-check's
  rule B1 requires a `| S108 | … |` row, and the row's `https://` token must
  equal the manifest record's `url` byte-for-byte.
- `grep -c F51 <lane>/PROVINCE.md` → **0**: the frontier row F51 is not written
  yet (frontier census at base: `FRONTIER-CENSUS rows=50 admitted=50 closed=50
  problem-rows=0 registry=107`; `frontier-recheck-count.py` → `entries=53 pass=53
  exit=0`, with `PASS F50 … ids=S107` as the last row).
- `PROVINCE.md` L178 (F31) carries the scope limit the C2 claim names: F31's
  limit reads "…the osv.dev service API, the JSON Schema validation artifact,
  individual database exports and per-database database_specific values stay
  out". F51 must therefore state explicitly that it admits the **service
  contract** and not the OSV record format, to avoid colliding with F31.

## 6 — What remains unknown

- Whether the *upstream page content* will change in future: the served bytes are
  a Jekyll build regenerated from `google/osv.dev` (the page's `last-modified`
  moved to today 04:37:25 GMT during this round). A future content revision
  would change both the raw HTML digest and the normalized digest — that is a
  content revision, not per-response variance, and the manifest should say so
  explicitly rather than leave a PSIRT-style caveat that does not apply here.
- I did not exercise `source-recheck.py` against a round-73 manifest, because no
  such manifest exists yet in the lane (see §5). The quote/anchor semantics
  above are from `source-recheck.py`'s `anchor_verdict` (read at
  `corpus/instruments/source-recheck.py:85-114`) and from direct occurrence
  counts against the capture.
- The recheck-line cd-prefix repair (C1) and the C2 entry/prose itself are
  outside this seat's scope and were not tested here.

## Files written by this seat

- `.ufo/waves/round-73/w1/K73ScoutCapture.md` (this report)
- `.ufo/waves/round-73/w1/K73ScoutCapture/fetch1.html`, `fetch2.html` (raw fetches)
- `.ufo/waves/round-73/w1/K73ScoutCapture/S108-recapture.txt` (instrument recapture)
- `.ufo/waves/round-73/w1/K73ScoutCapture/digests.txt` (sha256 of the three files above)
- `.ufo/waves/round-73/w1/K73ScoutCapture/receipts-measurements.txt` (command/exit-code receipts)
- `.ufo/waves/round-73/w1/K73ScoutCapture/upstream-post-v1-query.md` (upstream Jekyll source)

Process note: one intermediate `cp` of that upstream file landed transiently at the
lane root (`upstream-post-v1-query.md`) before the report directory path was
supplied; it was removed immediately with `rm -f` and `git status --porcelain`
then showed no trace of it. The only untracked path this seat added to the lane
is the report directory above. The pre-existing untracked
`corpus/source-snapshots/round-73/` (holding the L1's `S108.txt`) was already
present and unmodified by this seat.

## Tooling

No tools were installed or upgraded by this seat; `curl 8.23.0`, `python3 3.14.8`,
`sha256sum`, `cmp` and `git` were already present on the host. No pacman, uv, npm
or `~/.local/bin` action was taken.
