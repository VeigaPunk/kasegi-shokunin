# Sentinel — Q6 documentation-only review (round 24, wave 1)

Seat: `L1Kasegi24.SentinelQ6`. Read-only. No file under review was edited.

Base: `d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a` (claims: `.ufo/waves/round-24/claims.json`).

## Surface actually reviewed

- `(a)` **The drafted entries do not exist yet.** `/tmp/kasegi-r24-EntryRoE/corpus/knowledge/`
  and `/tmp/kasegi-r24-EntryStatute/corpus/knowledge/` are both absent (`ls` → *No such file or
  directory*, 2026-10-25T04:1x Z); only `kasegi-r24-{CaptureTool,ResolverPatch,ResolverAttack,
  LivenessMatrix,guard,probe,qr2,scout,src,export,SOURCESRows,SrcS001S003}` exist. I reviewed the
  package bytes that those seats would copy from: the two `candidates_admit`
  (`authorised-testing-rules-of-engagement.md`, `statutory-authorization-in-three-traditions.md`)
  and the `candidate_refuse` (`chinese-criminal-thresholds-and-authorisation.md`) under
  `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/`.
- `(b)` `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md:19` (Q6). Unchanged from
  base: `git diff d0a3f6a -- corpus/QUALITY.md` is empty.
- `(c)` The capture script design, at its canonical path
  `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py` (untracked,
  `??` in `git status`), plus the earlier draft in `/tmp/kasegi-r24-CaptureTool/...` (different
  bytes, sha256 `a2aeda28…` vs canonical `e183188d…`), plus the 19 committed captures in
  `corpus/source-snapshots/round-24/`.

---

## BLOCK findings

### S-1 `block` — the Rules-of-Engagement entry's `ground:` cites a lane record that does not exist

`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/authorised-testing-rules-of-engagement.md:5`

```
ground: round-15 ledger item 2 — a published acquittal of a tester who acted wholly within an authorisation
```

Evidence that the cited record does not exist:

- `grep -rn "acquittal" /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/ SKILL.md` → **0 hits**.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-15.md` is a lesson with
  numbered sections (`## 1. Verify the surface exists before you plan to cite it`,
  `## 2. A surviving same-named file is not the same file`, …); `grep -n "ledger item"` over it →
  **0 hits**, and there is no `ledger/` in the lane (`round-15.md:92` records exactly that).
- The entry's own `### Kasegi use` block says the lane's "unresolved question" is *"what is an
  acquittal of a tester who acted wholly within an authorisation?"* (`:44-46`) — i.e. the entry
  simultaneously asserts the acquittal exists as a round-15 item and that it is unfound.

Impact: the one provenance field that justifies admitting the entry is fabricated. Under C2's kill
rule ("If either entry fails a Q1–Q6 gate … the entry is refused with reason"), admitting these
bytes converts a false claim into committed corpus provenance. Smallest remediation: delete
`ground:`, or replace it with a row/lesson pointer that resolves (`grep` the exact string and paste
the hit), or admit and mark it "no lane record; entered from package".

### S-2 `block` — the same entry fails Q1's structural gate

`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/authorised-testing-rules-of-engagement.md:1-5`

```
$ head -1 | od -c   →   \n   s   o   u   r   c   e   : ...
```

The file begins with an empty line and then `source:` — **there is no H1 title**, and the header
block is `source: / verified-at: / recheck: / ground:` in that order. `corpus/QUALITY.md:13` (Q1)
requires the three header lines "directly under its H1 title". Every admitted entry does this
(`corpus/knowledge/cvss-v4-severity-and-vector.md:1-4`). Impact: a Q1 gate failure on the entry
that C2 counts; remediation is a title line plus dropping the blank first line — cheap, but it must
happen before admission, not after.

### S-3 `block` — both admit candidates' `recheck:` fields are not runnable and fail **open**

- `authorised-testing-rules-of-engagement.md:4` — `recheck: 90d — re-fetch the PDF and `grep -F`
  the four lines (ran 2026-10-24)` is prose: there is no command to execute, so Q1 ("plus the
  runnable command") and Q7 (`QUALITY.md:48`, "an executable recheck field contains a command")
  both fail. Nothing can be re-derived from committed bytes.
- `statutory-authorization-in-three-traditions.md:8` — ``curl -sSL https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128``.
  `curl` without `-f`/`--fail` exits **0** on HTTP errors. Measured on the cited public host:

  ```
  $ curl -sSL -o /dev/null -w '%{http_code}\n' 'https://laws.e-gov.go.jp/api/1/lawdata/NOT-A-LAW-ID'
  404
  exit=0
  $ curl -sSfL -o /dev/null 'https://laws.e-gov.go.jp/api/1/lawdata/NOT-A-LAW-ID'
  curl: (22) The requested URL returned error: 404 ; exit=22
  ```

  So the check reports success against a dead or moved URL — the failure mode Q7/R3 exist to stop.
  (The source itself is real: `HTTP 200`, `grep -c '三年以下の拘禁刑'` = 1 today. The command's
  exit discipline is the defect, not the citation.)
- `chinese-criminal-thresholds-and-authorisation.md:8` — same `curl -sSL` fail-open on
  `https://www.court.gov.cn/fabu/xiangqing/3085.html`.
- No committed capture exists to back either entry: `ls corpus/source-snapshots/round-24/*.json` →
  no such file (the directory holds `S001…S031.txt` and **no manifest**), so
  `source-recheck.py --manifest` — the form F06/F07/F08 already use
  (`corpus/knowledge/cra-manufacturer-reporting-duties.md:5`) — cannot run for any round-24 row.
  Zero lane entries currently use `curl` in `recheck:` (`grep -rl '^recheck:.*curl'
  corpus/knowledge/ | wc -l` → 0); these bytes would be the first, and they regress the bar the
  round's own C1 is trying to raise.

Remediation: give both entries the `python3 corpus/instruments/source-recheck.py --manifest
corpus/source-snapshots/round-24/manifest.json --source S###` form and produce the manifest; for
the RoE entry that means a real capture of SP 800-115, which the library already fetches
(`/tmp/sentinel-q6/nist800-115.pdf`, sha256 `58e5ed41…`).

### S-4 `block` — `ground: F12` is a package-local frontier id that dangles in the lane

`statutory-authorization-in-three-traditions.md:9` and `chinese-criminal-thresholds-and-authorisation.md:9`
both carry `ground: F12`. The package's own numbering runs `F09…F14`
(`program-scope-rules-and-asset-boundaries.md:9` = F09, `program-severity-ladders…:10` = F10,
`claim-packaging…:9` = F11, this entry = F12, `japanese-domestic-disclosure…:8` = F13,
`chinese-vulnerability-taxonomy…:8` = F14). The lane's frontier table has **F01–F08 only**
(`corpus/README.md:198-205`) and is admitting **F09** for this very topic (`claims.json` C2);
`grep -rn F12 corpus/` → **0 hits**. If the entry lands with `ground: F12` unchanged, it points at
nothing and collides with the id `F09` that C2 is about to assign. Remediation: renumber to the
lane's admitted id in the same edit that renumbers the `S###` rows.

### S-5 `block` — the capture instrument will read any local file and follow any redirect into a committed snapshot

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py:73-79`

```python
def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=60) as response:
```

`urlopen` dispatches through the default opener, whose handlers are
`['HTTPHandler','HTTPDefaultErrorHandler','HTTPRedirectHandler','FTPHandler','FileHandler','DataHandler','HTTPSHandler',…]`
(measured). There is no scheme allowlist and no address check, so:

1. **Arbitrary local read → committed snapshot.** Executed against the real CLI:

   ```
   $ python3 corpus/instruments/capture-source.py --id S999 --url file:///etc/hostname \
         --out /tmp/sentinel-q6/escaped/S999.txt --kind text
   $ cat /tmp/sentinel-q6/escaped/S999.txt   →   plazir27
   ```

   `--out` is unconstrained (S-6), so the same one-liner writing to
   `corpus/source-snapshots/round-24/S123.txt` puts private local bytes into the committed tree
   under a source id. `file://$HOME/.ssh/…`, `~/.aws/credentials`, `~/.netrc`,
   `~/.config/gh/hosts.yml` are all readable by this process; the earlier draft in
   `/tmp/kasegi-r24-CaptureTool/.../capture-source.py:189-196` accepts `file://` explicitly **and
   records the absolute path verbatim** in `manifest.json` (`"url": doc["url"]`, `:405`), so that
   variant commits the personal path too — exactly the leak Q6 excludes.
2. **Redirect-mediated SSRF.** `HTTPRedirectHandler` is present with `max_redirections=10` and no
   host allowlist (`has host allowlist attr: False`, measured). A cited public URL that 302s to
   `http://127.0.0.1:<port>/` or `http://169.254.169.254/latest/meta-data/` is captured and hashed
   as a "public source". `http://` is accepted as a first-class scheme, so a plain-http plan needs
   no redirect at all.

Impact on this lane's contract: the instrument is the mechanism by which round-24 will claim
"committed captures". A capture that can silently contain non-public bytes is a provenance
fabrication vector, not a tooling nit. Smallest remediation (three lines, before any further
capture): allow only `https://`; reject any resolved host in `127/8`, `169.254/16`, `10/8`,
`172.16/12`, `192.168/16`, `::1`, `fe80::/10` and re-check after redirects (resolve via
`socket.getaddrinfo` and refuse); confine `file://` to an explicit `--fixtures-dir` argument used
only by `--selftest`.

---

## ADVISORY findings

### A-1 `advisory` — a capture can write the snapshot and then die without a receipt

Same file, `:82-98`. `capture()` writes the snapshot (`open(out,"wb")`, `:92`) and only then prints
the digest line using `%d` on `response.status`. For non-HTTP schemes `status` is `None`:

```
$ python3 …/capture-source.py --id S999 --url file:///etc/hostname --out /tmp/sentinel-q6/escaped/S999.txt --kind text
TypeError: %d format: a real number is required, not NoneType   (exit 1)
$ ls -l /tmp/sentinel-q6/escaped/S999.txt   → 9 bytes, written
```

A written `S###.txt` with no printed sha256 and no `utc=` is indistinguishable from a stale
capture of a previous round. Fix: compute/print the receipt before or independent of `status`, or
refuse non-HTTP before fetching.

### A-2 `advisory` — `--out` is unconstrained: one typo overwrites a corpus file

`:91-93` — `os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)` then
`open(out, "wb")`. Nothing requires `out` to resolve under `corpus/source-snapshots/`. Demonstrated
out-of-tree above. A mistyped `--out corpus/knowledge/cvss-v4-severity-and-vector.md` would replace
an admitted entry with page text and exit 0. Fix: resolve `out` and require
`commonpath([snapshot_root, out]) == snapshot_root` (the consumer `source-recheck.py:120-124`
already does exactly this check on the read side — the producer should match it).

### A-3 `advisory` — the instrument's selftest has no negative control, and the instrument is undocumented and unbound

- `capture-source.py:100-113` `selftest()` proves only that `html_to_text` is deterministic on one
  fixture. No case exercises refusal of `file://`/`data:`/`ftp:`, a redirect to a private address,
  an oversized body (`MAX_FETCH_BYTES`, `:33`), or an out-of-tree `--out`. `QUALITY.md:37` (R3)
  requires an instrument verdict to name its matcher; the docstring's claim "Capture a public
  source" (`:1`) is unenforced and untested.
- `grep -n "capture-source" corpus/instruments/README.md README.md corpus/QUALITY.md` → **0 hits**:
  every other instrument is registered in the README ("Round-23 instruments" section); this one is
  not, so its declared contract exists only in its own docstring.
- The 19 snapshots are unbound: no `manifest.json` exists for round-24, and the receipt prints no
  URL, so nothing in the committed tree ties `S123.txt` to `https://nvlpubs.nist.gov/…`. Until a
  manifest exists, C1 counter A cannot exit 0 for any round-24 row.

### A-4 `advisory` — the RoE entry's evidence quotes are cut at `pdftotext` line wraps (Q3 fragmentation)

`:25-27`:

```
- S123, the glossary entry: "Rules of Engagement (ROE): Detailed guidelines and constraints regarding the execution of information"
- S123, the operative clause: "The ROE is established before the start of a security test, and gives the test team"
- S123, its consequence: "authority to conduct defined activities without the need for additional permissions."
```

I re-extracted the cited PDF (`pdftotext -layout`, sha256 `58e5ed41…`) — the three fragments are
lines 3921/3922/3923 of the extraction, i.e. one glossary sentence sliced at the converter's
80-column break. The scout's justification
(`.ufo/waves/round-24/wave1/SrcNISTROE.md:130-137`) is "so a line-oriented `grep -F` rechecker
works without joining lines" — but the committed consumer normalizes whitespace
(`corpus/instruments/source-recheck.py:22-24`, `normalize()`), and the canonical manifest driver
counts under the same normalization (`capture-source.py` draft `count_occurrences`). The split is
therefore unnecessary and leaves two evidence bullets ending mid-phrase, unusable as a citation by
a reader. Not a Q6 breach (no markup is being quoted); fix by asserting one ≤25-word sentence or
disclosing the cut.

### A-5 `advisory` — Q6 as written does not govern the round's new capability (criterion scope gap)

`corpus/QUALITY.md:19` is entry-scoped: it forbids an *entry* from instructing probe/scan/login and
from carrying credentials, a session, a private URL or an `op://` URI. Round 24 adds a
network-capable *instrument* (S-5) and a new *class of committed evidence* (captures). Neither is
covered, and Q6 has no detector at all — unlike Q7/R3, there is no command a reviewer can run to
falsify it, so "Q6 passes" is currently an assertion. Smallest remediation (one row, three
mechanical clauses, one command each):

1. remote fetch: `https:` only; refuse loopback/link-local/RFC1918 and cross-host redirects;
2. `file://` only inside a declared fixtures directory, never into `corpus/source-snapshots/`;
3. no absolute personal path outside the already-published lane root in any manifest or capture —
   gate with `grep -rEn 'op://|/(home|Users)/[A-Za-z0-9._-]+|AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY' corpus/source-snapshots/`;
4. writes confined to the snapshot root (`commonpath`, as `source-recheck.py` already does on read).

Also tighten "private URL" to name the classes (RFC1918, `127/8`, `169.254/16`, `.internal`,
`*.local`), and "session" to include cookies and CSRF tokens — the package's own
`cn-case-library-search-needs-a-session.md:34` ("a later round should spend its budget on a
session") is precisely the instruction Q6 forbids, and it survives in the package today.

---

## Verified clean (no finding)

- **No credential material, session token, cookie, private URL or `op://` URI in the three
  candidates.** `grep -nE 'op://|vault://|secret://|\$VAULT|token=|x-api-key|Bearer |Cookie:|session=|password'`
  over the three files → only `password` as judicial vocabulary
  (`chinese-criminal-thresholds-and-authorisation.md:33,40`,
  `authorised-account-scope-and-intrusion.md:9` — all describe holdings, no secret).
- **No absolute personal paths in the candidates.** `grep -rnE '/home/(vgpnk|[a-z]+)/'` → empty.
  The two candidates' `recheck:` lines carry no local path at all, so they leak strictly less than
  the published baseline (F06/F07/F08 rechecks already publish
  `/home/vgpnk/Projects/shokunin/kasegi-shokunin`).
- **All candidate URLs are public institutional documents**: nvlpubs.nist.gov, laws.e-gov.go.jp,
  soumu.go.jp, npa.go.jp, court.gov.cn, czt.ln.gov.cn, nj.jsjc.gov.cn. No intranet, loopback,
  RFC1918, `file:`, or userinfo (`user:pass@`) URL.
- **No converter markup in the candidates.** `grep -nE '<u>|</u>|<b>|&nbsp;|&#[0-9]|&amp;|\u200b'`
  → no hits. The lane's `normalize()` strips `<u>/<u>` anyway
  (`source-recheck.py:22-24`), and the canonical capture strips all tags (`capture-source.py:38-49`),
  so no entry is ever forced to quote markup to pass a check.
- **The 19 round-24 captures carry no secrets.** Sweep over
  `corpus/source-snapshots/round-24/` for `op://`, `Bearer <tok>`, `AKIA[0-9A-Z]{16}`,
  `BEGIN … PRIVATE KEY`, `Set-Cookie`, `Authorization:`, `/home/vgpnk` → **zero hits**.
- **The consumer is path-safe even though the producer is not.** `source-recheck.py:117-124`
  refuses an absolute manifest `path` (`reason=invalid-path`) and a resolved path outside the
  manifest directory (`reason=outside-manifest-directory`); `capture-source.py` (draft)
  `check_plan` rejects absolute/`/`-bearing paths. Cite this asymmetry in any remediation: fix the
  producer to the consumer's bar, do not weaken the consumer.
- **The cited sources are real** (public-document reads only): SP 800-115 fetched, glossary and
  Appendix-B sentences confirmed verbatim at `nist.txt:3921-3923` and `:412`; e-Gov lawdata returns
  `HTTP 200` with `三年以下の拘禁刑` present once. `curl` fail-open, not the citation, is the defect
  (S-3).

## Not exercised / UNVERIFIED

- The entry seats had produced nothing at review time, so **whether the admitted bytes will match
  the package bytes is UNVERIFIED** — S-1…S-4 apply to the package bytes as they stand; if the
  seats rewrite them, re-run those four checks.
- S-5's redirect path was proven by default-handler composition and code reading, not by a live
  redirect fetch: I did not contact any host other than the cited public documents and one 404
  sentinel path on the same public API. The `file://` half was executed.
- `--kind` autodetection is absent (`:120`, default `html`); I did not test a PDF captured under the
  wrong `--kind`, since the resulting quote mismatch fails closed at recheck time.

## Installs

None. No `pacman` call was made (host gate stands); nothing was installed or upgraded. `curl` and
`pdftotext` were already present.
