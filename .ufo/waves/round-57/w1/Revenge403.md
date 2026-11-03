VERDICT — The HTTP 403 is a Cloudflare managed challenge, not an ISO origin rule and not a User-Agent block. No HTTP request header discriminates: all five mandated urllib variants (a)-(e) return 403, while curl with the instrument's exact UA returns 200. The smallest controllable difference found that flips the instrument's own request to 200 is at the TLS layer: CPython 3.14's `http.client` adds ALPN `http/1.1` (and PHA) to every HTTPS context it creates (`/usr/lib/python3.14/http/client.py:845-855`, reached from `/usr/lib/python3.14/urllib/request.py:1373-1375`), and dropping that extension takes the identical UA/headers/URL from 403 to 200 in 34/40 and 35/50 trials (vs 1/40 and 8/50 with it). A second, independent knob in the same score: adding any one extra request header outside `{Accept, Accept-Language, Referer}` also flips it to 200 (25/25, 30/30); adding those three does not. The decision is therefore a scored client fingerprint (TLS ClientHello + header-set shape), not a header allow/deny list.

Seat: Revenge403 (revenger), kasegi r57 w1. Scope: one URL, `https://www.iso.org/standard/72311.html` (public catalog page). Read-only on the lane: no file under L was edited; the only lane write is this file. No cookies, no logins, no alternate hosts, no rate-limit evasion. No tools installed (python3 3.14.8, curl 8.23.0 present; nothing upgraded). Scratch `/fast/scratch/hyaku/kasegi-r57/Revenge403` removed at end of seat.

Note on scope: the mandated variants (a)-(e) and the two curl requests (E2, E3) were run first and are complete. To answer step 4 ("name the discriminating header, or state that none discriminates") it was necessary to separate header effects from client-stack effects; the controlled probes in E4-E7 were run for that purpose before the orchestrator's stop instruction arrived. Every number below is from an executed command.

## 1. Mandated reproduction (step 1)

E1. Instrument failure reproduced 5/5.
- cmd: `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && TMPDIR=/fast/scratch/hyaku/kasegi-r57/Revenge403 python3 corpus/instruments/capture-source.py --id PROBE --url https://www.iso.org/standard/72311.html --out /fast/scratch/hyaku/kasegi-r57/Revenge403/probe.txt --kind html`
- exit: 1, five consecutive runs, no output file written (`probe.txt: No such file or directory`)
- last stderr line: `urllib.error.HTTPError: HTTP Error 403: Forbidden`
- raise site: `L/corpus/instruments/capture-source.py:75` (`with urllib.request.urlopen(request, timeout=60) as response:`), called from `:83` (`raw, status = fetch(url)`)
- UA set at `L/corpus/instruments/capture-source.py:32`:
  `32:UA = "kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)"`

## 2. Mandated variants (step 2) — one request each, stdlib urllib only

Probe: `urllib.request.urlopen(urllib.request.Request(URL, headers=<variant>))`, default opener (i.e. the instrument's own stack: default HTTPS context → ALPN http/1.1 + PHA).
- cmd: `cd /fast/scratch/hyaku/kasegi-r57/Revenge403 && TMPDIR=/fast/scratch/hyaku/kasegi-r57/Revenge403 python3 - <<'PY'` … `PY` (script body: five `Request` objects, one `urlopen` each, print status / `len(body)` / `cf-mitigated`).

| # | variant | status | bytes | cf-mitigated |
|---|---------|--------|-------|--------------|
| a | UA exactly as `capture-source.py:32` | 403 | 5618 | challenge |
| b | urllib default UA (no UA header set) | 403 | 5469 | challenge |
| c | UA + `Accept: text/html,application/xhtml+xml` | 403 | 5639 | challenge |
| d | UA + `Accept-Language: en` | 403 | 5639 | challenge |
| e | UA + `Accept: */*` | 403 | 5639 | challenge |

- exit 0 (the harness exits 0; statuses are in the table).
- 10-rep repeat, same five variants: a 0/10 200, b 0/10 200, c 0/10 200, d 0/10 200, e 2/10 200 (the two 200s were 88964 bytes). **No mandated header variant discriminates.**

## 3. Mandated curl requests (step 3)

- cmd A: `curl -sS -o /dev/null -w 'http_code=%{http_code} size_download=%{size_download}\n' -A 'kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)' https://www.iso.org/standard/72311.html`
- out A: `http_code=200 size_download=88964` (20/20 repeats 200; 30/30 in E6 headline run)
- cmd B: `curl -sS -o /dev/null -w 'http_code=%{http_code} size_download=%{size_download}\n' https://www.iso.org/standard/72311.html` (curl's own `curl/8.23.0` UA)
- out B: `http_code=403 size_download=5448` → later 403 x8/8, x6/6.

So the UA string alone is not the trigger, and no header from the variant set is the trigger. curl's `--http1.1` and `--http1.1 --no-alpn` also returned 200 x6/6 and x8/8 with the instrument UA.

## 4. What the 403 is (anatomy)

- cmd: python urllib request with the instrument UA, print `e.code` and every response header; also `curl -sS -D hdr -o body`.
- headers observed: `HTTP/1.1 403 Forbidden`, `Server: cloudflare`, `Cf-Mitigated: challenge`, `Cf-Ray: <present>`, `Content-Type: text/html; charset=UTF-8`, `Content-Length: 5618` (UA-dependent: 5469/5639), `set-cookie: __cf_bm=<redacted; session value not recorded>`, `Server-Timing: chlray;desc="…"`.
- body markers: `Just a moment`, `__cf_chl` (3 occurrences), `Enable JavaScript and cookies to continue`.
- 200 responses carry `cf-cache-status: HIT` (edge cache) or `MISS` (cache-bust control), and the real catalog page (89325 bytes with `Accept-Encoding: identity`, 88964 with `Accept: */*`).
→ The 403 is Cloudflare's managed-challenge interstitial, not an ISO access-control denial.

## 5. Which difference discriminates (step 4) — answer

**No HTTP request header discriminates.** The five mandated variants are all 403 (E2), and a single-request-per-variant repeat of all five produced the same shapes. The discriminator is the client fingerprint:

E4. TLS ALPN toggle, identical UA, identical header block, identical URL.
- Probe: raw TLS socket to `www.iso.org:443` (Python `ssl.create_default_context()`), request `GET /standard/72311.html HTTP/1.1` + `Host` + instrument UA + `Accept: */*` + `Connection: close`; the only changed variable is `ctx.set_alpn_protocols(["http/1.1"])` + `ctx.post_handshake_auth = True` (what CPython 3.14's `_create_https_context` does by default) vs neither.
- run 40+40, randomized (`random.seed(20261103)`): ALPN-on → 403 x39/40; ALPN-off → 200 x34/40.
- run 50+50 via `urllib.request.build_opener(HTTPSHandler(context=ctx))`: ALPN-on → 200 x8/50 (403 x42); ALPN-off → 200 x35/50 (403 x15).
- run 20+20: ALPN-on → 403 x20/20; ALPN-off → 200 x17/20.
- ALPN value sweep, 4 reps each: `['http/1.1']` 403 x4, `['foo']` 403 x4, `['h2c']` 403 x3 + 200 x1, no ALPN 200 x4. PHA alone (no ALPN) 200 x6/10, 403 x4/10.
- ClientHello extension lists captured on a local listener: no-ALPN `[65281,11,10,35,22,23,13,43,45,51,27]`, JA3 `e13a080178d6052cad07cde7ba6232d0`; ALPN `[…,16,…]`, JA3 `967cee479fd91bc303ec667039f39f18`. curl's is `cd911cdb3ae1af6c7bc940cdcad83a1a` (cipher list and extension order differ: 29 ciphers vs Python's 17; no ext 35).

E5. Direct instrument-path proof (no lane edit): load `corpus/instruments/capture-source.py` as a module, build an `HTTPSHandler` whose context has **no** ALPN/PHA, install it as `urllib.request._opener`, call `mod.capture(...)` unchanged.
- out: `PROBE-NOALPN status=200 fetched_bytes=89325 snapshot_bytes=6647 sha256=17ee9c4191ca2261fbb40a6109c6013677adc4ff7522fff079964f72ebb0e1dd`
- that sha256 is byte-identical to the committed `corpus/source-snapshots/round-57/S089.txt` (`cmp` empty). A later 5/5 batch returned 200 with the same sha; the first 3-run batch returned 2/3 200 and 1/3 403 — so this is a strong bias, not a guarantee.
- exit 0 each success.

E6. The header-set knob is also real and independent of TLS.
- Same stock stack (ALPN on), same URL, same UA; one extra request header appended to `{Accept-Encoding: identity, Host, User-Agent, Connection: close}`:
  - `DNT: 1` → 200 25/25; `X-Random: 1` → 200 25/25; `Sec-Fetch-Dest: document` → 200 25/25; `Accept-Charset: utf-8` → 200 25/25; `Upgrade-Insecure-Requests: 1` → 200 25/25.
  - no extra header → 200 11/25, 403 14/25; `Accept: text/html` → 200 10/25; `Accept: */*` → 200 10/25; `Accept-Language: en` → 200 11/25; `Referer: https://www.iso.org/` → 200 14/25.
- Repeat with 40 reps: `X-Random: 1` 200 x39/40; `X-Forwarded-For: 127.0.0.1` 200 x40/40; `X-Random: ""` 200 x40/40; no-extra 200 x5/40; `Accept-Language: en` 200 x9/40; `Referer` 200 x6/40.
- Strict alternation 20 pairs, same UA: no-extra 200 x4/20 vs `DNT: 1` 200 x20/20 (and 15/15 in a second alternation). Cache-buster query (`?bust=<epoch>-<i>`) reproduces it: base 403/200/403/403, `DNT: 1` 200/200/200/200 with `cf-cache-status: MISS`.
- Header-name scan (12 reps each): flips to 200 — `DNT`, `TE`, `Via`, `Forwarded`, `X-Foo`, `Accept-Charset`, `Accept-Datetime`, `X-Forwarded-Proto`, `Sec-Fetch-Dest`, `Upgrade-Insecure-Requests`, and arbitrary names `A`/`AB`/`ABC`/`ABCDE`/`X-A`. Does **not** flip — `Accept`, `Accept-Language`, `Referer`, `Origin`, `Authorization`, `Range`, `X-Requested-With`, `Pragma`, `If-None-Match` (mixed: 4-8/12 200).
- UA class matters independently: under curl's stack, `curl/8.23.0`, `Python-urllib/3.14`, `Wget/1.21.4`, `Go-http-client/2.0` → 403 x6/6 each; instrument UA and a Chrome UA → 200 x6/6 each. Under the Python stack with a fixed header set, `curl/8.23.0` and `Python-urllib/3.14` → 403 x12/12 even with `DNT: 1`.

E7. Same headers, different client stack — curl passes where urllib fails.
- curl with the instrument's exact header set: `curl --http1.1 -A '<UA>' -H 'Accept:' -H 'Accept-Encoding: identity' -H 'Connection: close'` → 200 x6/6; curl default UA with the same header set → 403 x6/6.
- Python raw TLS with byte-identical request line/headers → 403 most of the time (E4 base arm).
→ Same HTTP bytes, different TLS ClientHello, opposite outcome. No HTTP header can be named as the discriminator.

## 6. What this does NOT establish

- It does not establish that Cloudflare blocks this UA or this lane. curl with the identical UA is 200 20/20 and 30/30; the challenge follows the client stack, not the UA.
- It does not establish a stable or permanent rule. The base 403 rate drifted within the session (0/10 → 11/25 → 14/30 200 across ~40 minutes), and the ALPN-off arm still returned 403 in 6/40, 15/50 and 9/30. The decision is a live score with noise, not a deterministic allowlist.
- It does not name the exact Cloudflare score or which rule fires. The ALPN and header-set results are consistent with bot-score fingerprinting (JA3/JA4 plus header shape), but the internal rule is not observable from here; that attribution is [INFERENCE].
- It does not establish behavior for the second catalog URL (`/standard/69725.html`); only 72311 was probed.
- It does not establish that removing ALPN is an acceptable fix for the instrument. That is a lane change (a custom HTTPS context) and was not made; the repo remains untouched.
- It does not establish anything about authenticated or cookie-bearing access. No cookies were sent (the `__cf_bm` challenge cookie was discarded, not replayed); no login was used.
- The 200 bodies are the public catalog page served through Cloudflare's edge cache (`cf-cache-status: HIT`, or `MISS` under cache-busting), so origin-vs-cache provenance of the 200 is not separated.

## 7. Direct bearing on the recorded disclosure

The lane records (`corpus/knowledge/iso-29147-30111-standard-records.md:100`, `corpus/README.md:917`, `corpus/QUALITY.md:437` R66) that "the committed instrument's urllib open is HTTP-403-blocked by www.iso.org; the fetch used curl with the instrument's own UA". That is accurate as an operational statement, and this seat sharpens the mechanism: the failing element is the TLS ClientHello CPython 3.14's HTTPS handler emits (ALPN `http/1.1` + PHA at `http/client.py:845-855`), not the UA and not any request header; the same UA over curl's ClientHello is accepted. The disclosure need not change; the mechanism sentence can be made precise as above.

## 8. Cleanup

- Scratch `/fast/scratch/hyaku/kasegi-r57/Revenge403` deleted after writing this file; no leftovers.
- No tool installs or upgrades.
- No writes to L other than this evidence file.
