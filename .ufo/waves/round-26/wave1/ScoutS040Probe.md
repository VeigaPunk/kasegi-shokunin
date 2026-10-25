# Scout S040 live probe — R25-5 drift record

Milestone: S040 live probe (R25-5). Date: 2026-10-25 (UTC). Seat: L1Kasegi26.ScoutS040Probe (leaf).

## Question

Record live behavior of the Cisco security vulnerability policy URL for R25-5
(registry row S040: `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html`):
final URL and UA requirement. Run both UA probes, capture the FINAL page with the lane instrument, grep the snapshot.

## Probe 1 — Browser UA (canonical URL)

Command (exact):

```
curl -s -D - -o /dev/null -L -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36" -w "final=%{url_effective} code=%{http_code} num_redirects=%{num_redirects}\n" https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html
```

Observed:

- `HTTP/2 403`, server `AkamaiGHost`, content-length 465, date Sun 25 Oct 2026 12:34:25 GMT
- No redirect served (blocked at the canonical URL before any Location follows)
- `final=https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html code=403 num_redirects=0`

Result: **browser UA → 403, zero redirects**. The canonical URL must not be refetched with a browser UA.

## Probe 2 — Instrument UA (canonical URL)

Command (exact):

```
curl -s -D - -o /dev/null -L -A "kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)" -w "final=%{url_effective} code=%{http_code} num_redirects=%{num_redirects}\n" https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html
```

Observed redirect chain (2 hops):

1. `HTTP/2 301` (Apache, `wemxweb-publish-prod1-05`) — `Location: https://tools.cisco.com/security/center/resources/security_vulnerability_policy.html`
2. `HTTP/1.1 302 Found` — `Location: https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html`
3. `HTTP/2 200` (`sec.cloudapps.cisco.com`, content-type `text/html;charset=ISO-8859-1`, date Sun 25 Oct 2026 12:34:27 GMT)

- `final=https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html code=200 num_redirects=2`

Result: **instrument UA → 301 → 302 → 200**, final URL `https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html`.
Note for the row's recheck: the live chain is two hops (301 to tools.cisco.com, then 302 to sec.cloudapps.cisco.com), not a single 301 to the final host as the R25-5 note phrased it.

## Capture of the FINAL page (lane instrument, instrument UA)

Command (exact):

```
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py --id S040 --url https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html --kind html --out /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-26/S040-live.txt
```

Log line (verbatim):

```
S040 status=200 fetched_bytes=94027 snapshot_bytes=33463 sha256=b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c utc=2026-10-25T12:34:27Z out=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-26/S040-live.txt
```

- Exit: **0** (echoed `exit=0` after the run)
- Snapshot: `corpus/source-snapshots/round-26/S040-live.txt`, 503 lines
- sha256: `b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c`
- Consistency: sha256 is **byte-identical to round-25's `corpus/source-snapshots/round-25/S040.txt`** (`b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c`); the final page renders the same text under the instrument UA after the redirect chain. The round-25 capture remains valid content-wise; the URL used for it must move to the final URL.

## Greps on `round-26/S040-live.txt`

`grep -n -E "ISO/IEC 29147" round-26/S040-live.txt` → 1 hit:

- **line 58**: `security incidents. The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018,` (line length < 120 chars; full line shown)

`grep -n -F "Disclosure of Security Vulnerabilities" round-26/S040-live.txt` → 2 hits:

- **line 28**: `Disclosure of Security Vulnerabilities` (line length < 120 chars; full line shown — TOC/nav entry)
- **line 299**: `Disclosure of Security Vulnerabilities` (line length < 120 chars; full line shown — section heading; the four expedite bullets follow at L301/L302/L305/L309 per the round-25 record, same bytes)

First 120 chars per hit (verified with `awk 'NR==28||NR==58||NR==299 {print NR": "substr($0,1,120)}'`):

```
28: Disclosure of Security Vulnerabilities
58: security incidents. The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018,
299: Disclosure of Security Vulnerabilities
```

## R25-5 resolution data

- Canonical URL (registry): `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html`
- Final URL: `https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html`
- Redirect chain (instrument UA): 301 → `https://tools.cisco.com/security/center/resources/security_vulnerability_policy.html` → 302 → final URL → 200
- UA requirement: **browser UA gets 403 (no redirect); the instrument UA (kasegi-shokunin/1.0) is required**.
- The row's next recheck should run against the final URL with the instrument UA (e.g. `python3 corpus/instruments/capture-source.py --id S040 --url https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html --kind html --out …`), not the canonical URL.

## Scope

No edits to SOURCES.md (scribe w1 owns it). No other writes. Tools used: curl (system), python3/capture-source.py (lane instrument). No installs performed in this seat.
