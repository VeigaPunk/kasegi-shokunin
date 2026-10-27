# ExecC2Capture — round-41 C2 / S063 capture (RFC 9116 `security.txt`)

Seat: ExecC2Capture (executor) · Lane: kasegi-shokunin · Round 41 (hyaku run 10, fresh-start) · Axis: coverage (C2)
Base commit 5b29ea1439450b712581edf5f0bf98dfb262ab · Frozen claims read from `.ufo/waves/round-41/claims.json` (unedited).
Disk guard: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → exit 0 (green) before the fetch.

## 1. Deliverables written (only these; receipt written last)

| file | lines | sha256 | bytes |
|---|---|---|---|
| `.ufo/waves/round-41/wave1/ExecC2Capture.S063.txt` | 842 | `925512e715be5fae950f3eec88805197d4007875dac825c5603d44d2b71e2faa` | 39301 |
| `.ufo/waves/round-41/wave1/ExecC2Capture.manifest-record.json` | 60 | `bad6e7ab22246d00a52a17ff8f5ca29458e57733cea9b81630a53d081cdbf30c` | 4055 |

- `ExecC2Capture.S063.txt` **is** the capture: it is to be landed as `corpus/source-snapshots/round-41/S063.txt` (bytes unchanged).
- `ExecC2Capture.manifest-record.json` is **one `sources[]` element** (the shape of a `corpus/source-snapshots/round-40/manifest.json` record), for source id `S063`, to be embedded in `corpus/source-snapshots/round-41/manifest.json` by the L1. It carries `url`, `status`, `fetched_utc`, `fetched_bytes`, `size_bytes`/`snapshot_bytes`, `lines`, `full_text_lines`, `sha256`/`snapshot_sha256`/`full_text_sha256`, `raw_sha256`/`raw_bytes`/`raw_lines`, `scope`, `tool`, `normalized`, `http`, and the three located `quotes` (`Q1`/`Q2`/`Q3`, each with `id`, `quote`, `anchor`, `location`).

## 2. Fetch transcript

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -D headers.txt -o raw.txt \
    -w 'HTTP_STATUS=%{http_code}\nSIZE_DOWNLOAD=%{size_download}\nURL_EFFECTIVE=%{url_effective}\nNUM_REDIRECTS=%{num_redirects}\nCONTENT_TYPE=%{content_type}\nTIME_TOTAL=%{time_total}\n' \
    'https://www.rfc-editor.org/rfc/rfc9116.txt'
HTTP_STATUS=200
SIZE_DOWNLOAD=45129
URL_EFFECTIVE=https://www.rfc-editor.org/rfc/rfc9116.txt
NUM_REDIRECTS=0
CONTENT_TYPE=text/plain;charset=utf-8
TIME_TOTAL=0.199566
```
- Fetch instant (UTC): `2026-10-27T08:19:23Z` (response `date:` header `Tue, 27 Oct 2026 08:19:23 GMT`; script clock read before/after the fetch agrees).
- Raw body: **45129 bytes**, sha256 `79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9`.
- Other response headers: `etag: W/"be7f83388b58df04e4d55a1728262778"`, `cache-control: public, max-age=86400`, `server: cloudflare`, `link: <https://www.rfc-editor.org/info/rfc9116/>; rel="canonical"`, `access-control-allow-origin: *`. No `Content-Length` (chunked).
- Body shape measured on the raw bytes: UTF-8 **with BOM** (`ef bb bf` at offset 0), **0 CR bytes** (already LF), **0 form feeds**, **no `[Page n]` footers**, 1122 lines.

## 3. Normalization (declared, reproducible)

`corpus/instruments/capture-source.py --kind text` (its `collapse()`: CRLF/CR → LF, runs of space/tab/NBSP collapsed, lines trimmed, blank lines dropped, UTF-8, final newline) applied to the curl body above. **No slice** — the capture is the whole document.

- Reproducibility evidence: the instrument's own fetch (`--id S063 --url … --kind text`) at `2026-10-27T08:23:40Z` printed `status=200 fetched_bytes=45129 snapshot_bytes=39301 sha256=925512e7…` and its output is **byte-identical** to the collapse() of the curl body (`cmp` exit 0). Both paths are recorded in the manifest record's `tool` field.
- `lines` = `full_text_lines` = **842** (capture line k = normalized document line k; the 1122-line served body loses its blank lines under collapse()).
- **Known cosmetic fact, disclosed**: `collapse()` does not strip a byte-order mark, so capture **line 1 is the BOM alone** (bytes `ef bb bf`, no document text). Every document line is at or after L2; all anchors below are ≥ L100. If the L1 prefers a BOM-free first line, the one-line change is `tail -c +4` on the raw body before collapse() — it would change the digest and every anchor, so it is not applied unilaterally.

## 4. Facts recorded for the scribes (all read from the capture; line numbers are capture lines)

- **Publication**: capture L2-L6 = `Internet Engineering Task Force (IETF) E. Foudil` / `Request for Comments: 9116` / `Category: Informational Y. Shafranovich` / `ISSN: 2070-1721 Nightwatch Cybersecurity` / **`April 2022`** (L6). Title line L7 `A File Format to Aid in Security Vulnerability Disclosure`. Authors' addresses L837-L842 (Edwin Foudil, Yakov Shafranovich / Nightwatch Cybersecurity). Category: Informational; §1.2 defines MUST/SHOULD per BCP 14.
- **Location requirement — §3 "Location of the security.txt File" (heading L329)**: L330-L331 `For web-based services, organizations MUST place the "security.txt" file under the "/.well-known/" path, e.g., https://example.com/.well-known/security.txt as per [RFC8615] of a domain name or IP address.`; L333-L337 legacy top-level-or-redirect allowance and `the one in the "/.well-known/" path MUST be used`; L338-L341 access MUST be HTTP 1.0+, MUST use `https`, Content-Type MUST be `text/plain` with charset `utf-8`; L343-L346 redirects must be recorded and inspected (§5.2). **§3.1 "Scope of the File" (L348)**: a file MUST only apply to the domain/IP used to retrieve it, not subdomains or parent domains; L357-L359 organizations SHOULD use the policy directive for scope detail.
- **Field definitions — §2.5 "Field Definitions" (L186: `Unless otherwise stated, all fields MUST be considered optional.`)**, eight fields, one per subsection:
  | field | section | heading line | body | required? |
  |---|---|---|---|---|
  | Acknowledgments | §2.5.1 | L190 | L191-L199 | optional; web URI MUST be `https://` |
  | Canonical | §2.5.2 | L207 | L208-L220 | optional (recommended with signatures) |
  | Contact | §2.5.3 | L224 | L225-L242 | **MUST always be present** (L227-L228); repeatable, preference-ordered |
  | Encryption | §2.5.4 | L247 | L248-L258 | optional; keys MUST NOT appear, value MUST be a URI (L249-L251) |
  | Expires | §2.5.5 | L265 | L266-L272 | **MUST always be present and MUST NOT appear more than once** (L273) |
  | Hiring | §2.5.6 | L275 | L276-L278 | optional |
  | Policy | §2.5.7 | L280 | L281-L285 | optional |
  | Preferred-Languages | §2.5.8 | L288 | L289-L298 | optional, MUST NOT appear more than once (L297) |
  - IANA field registry §6.2 (L635-L712) repeats the set with `Multiple Appearances:` — Canonical/Contact/Encryption/Acknowledgments/Hiring/Policy = yes; Expires and Preferred-Languages = no; all `Status: current`, change controller IETF.
- **Expires semantics — §2.5.5 (the item's guess "Section 2.5 / MUST be no more than a year" is wrong on both counts)**: the bound is **RECOMMENDED**, not MUST, and it is **less than** a year ahead, not "no more than": `It is RECOMMENDED that the value of this field be less than a year into the future to avoid staleness.` (L270-L272). The value is an RFC 3339 / ISO 8601 Internet-profile timestamp (L268-L269); the field MUST always be present and MUST NOT appear more than once (L273); §5.3 (L532-L543) makes Expires the mechanism by which a publisher declares its data no longer valid, and prefers **no file** to a stale one (L536).
- **Encryption — §2.5.4 (not §2.3)**: §2.5.4 L248-L253 — the value MUST be a URI pointing to where the key can be retrieved, keys MUST NOT appear in the field, a web URI MUST begin with `https://`; authenticity of the key is the researcher's responsibility (L254-L255). The **encryption RECOMMENDATION** is in §2.5.3 (Contact): `When the value of this field is an email address, it is RECOMMENDED that encryption be used (as per Section 2.5.4).` (L235-L237). **§2.3 is "Digital Signature"** (L168-L178): OpenPGP cleartext signature RECOMMENDED, paired with `Canonical`. §5.7 (L582-L608) adds `implementors MUST use HTTPS` and recommends OpenPGP signing plus encryption keys for report submission.
- **Security considerations — §5 (L500-L623)**: 5.1 Compromised Files and Incident Response (L504), 5.2 Redirects (L526), 5.3 Incorrect or Stale Information (L532), 5.4 Intentionally Malformed Files (L545, incl. the 32 KB / 2 048-char / 1 000-line parse limits), 5.5 No Implied Permission for Testing (L559), 5.6 Multi-User Environments (L576), 5.7 Protecting Data in Transit (L582), 5.8 Spam and Spurious Reports (L610). §6.1 (L628-L633) registers `security.txt` in the IANA Well-Known URIs registry (permanent, IETF).
- **CSAF: absent.** The string `CSAF` occurs **0 times** in the capture; RFC 9116 defines exactly the eight fields above. Supplementary check (not part of the capture, not committed): the RFC 9116 errata list fetched `2026-10-27T08:26:05Z` (HTTP 200, 25394 bytes) shows 3 errata — 6946 (Verified, Editorial: ABNF comment "Section 3.5.3" → "Section 2.5.3", matching the capture's L383), 7264 (Reported, Technical: `Expires: 2021-12-31T18:37:07z` → `…Z`), 7743 (Reported, Technical: ABNF `CRLF = CR LF` → `CRLF = [CR] LF`) — **none** of them about CSAF. The entry must not present CSAF as an RFC 9116 field.

## 5. The three Gate quotes (located, ≤25 words each)

| id | anchor | quote | words | capture lines |
|---|---|---|---|---|
| Q1 | 330 | `For web-based services, organizations MUST place the "security.txt" file under the "/.well-known/" path` | 15 | L330-L331 |
| Q2 | 270 | `It is RECOMMENDED that the value of this field be less than a year into the future to avoid staleness.` | 19 | L270-L272 |
| Q3 | 235 | `When the value of this field is an email address, it is RECOMMENDED that encryption be used (as per Section 2.5.4).` | 23 | L235-L237 |

## 6. Validation actually run (all exit codes observed)

1. `python3 corpus/instruments/source-recheck.py --manifest <scratch>/manifest.json --source S063` → **exit 0**:
   ```
   S063:sha256 OK
   S063:Q1 OK normalized=markup-whitespace occurrences=1 anchor=330-ok
   S063:Q2 OK normalized=markup-whitespace occurrences=1 anchor=270-ok
   S063:Q3 OK normalized=markup-whitespace occurrences=1 anchor=235-ok
   ```
   (scratch manifest = the delivered record wrapped in `{"schema_version":1,…,"sources":[…]}` with the delivered capture named `S063.txt`; whole-manifest run → exit 0, same three lines.)
2. `python3 corpus/instruments/capture-binding-check.py --root <scratch>/bind-sim` → **exit 0**: `MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0`, `AUDIT records=1 with_url=1 with_fetched_utc=1 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=0`, `records=1 bound=1 unbound=0`. The scratch tree carried a **simulated** S063 registry row (real `corpus/SOURCES.md` copied into scratch + one appended row); no lane file was touched. The binding depends on the landed S063 row's source cell carrying exactly one `https://` token byte-equal to `https://www.rfc-editor.org/rfc/rfc9116.txt` (capture-binding-check rules B4/B5) — the rows seat was told this.
3. Reproducibility: instrument re-fetch vs curl-body collapse → identical sha256, `cmp` exit 0 (see §3).
4. Cross-seat cross-check of the scribe's entry (`ScribeC2Entry.entry.md`, read-only): all **33** distinct quoted spans in that entry were located in this capture, each **unique** (`occurrences=1`), at these capture lines — entry L8→L104 and L115; L11→L189; L12→L227; L13→L182 and L184; L16→L235; L17→L249 and L250; L18→L254; L19→L169 (×2) and L256; L22→L266; L23→L270; L24→L273; L25→L267; L28→L281; L29→L330; L30→L333; L31→L335; L32→L358, L339, L340; L35→L349; L36→L357; L37→L350; L40→L528; L41→L536; L42→L538; L46→L571; L47→L573; L51→L249. Every `<<<CAPTURE:Lnnn>>>` placeholder in that entry therefore has a grounded, unique capture line. (The entry's §3 pins 330/333/335, §2.5.5 pins 270/273, §2.5.3 pin 235 and §5.x pins 528/536/538/571 all agree with this table.)

## 7. Risks, dependencies, blockers

- **Dependency (not mine to land)**: the record binds only once `corpus/SOURCES.md` carries the S063 row with exactly one `https://` token `https://www.rfc-editor.org/rfc/rfc9116.txt`; the manifest record's `url` is byte-equal to that token.
- The capture's line 1 carries the served body's BOM (no text) — disclosed in the record's `normalized` field; it is the house instrument's output, byte-identical to `capture-source.py --kind text`.
- **Factual correction the L1 must carry forward**: RFC 9116 defines **no CSAF field**, and Expires' one-year bound is a RECOMMENDED (not MUST) *less than* a year. If the F24 row, the PROVINCE amendment or the knowledge entry says otherwise, C2's claim would misstate the standard.
- The published text's ABNF comment at L383 says "(see Section 3.5.3)" — verified editorial erratum 6946; the correct reference is §2.5.3. Cite as a published-text defect.
- No blocker: the capture, the record and the fetch evidence are complete and self-verifying.

## 8. Tooling / hygiene

- No tool was installed or upgraded for this seat (the lane's own `capture-source.py`, `source-recheck.py` and `capture-binding-check.py` plus `curl`/`python3`/`sha256sum` from the base image were sufficient). No `pacman`, no PATH-directory writes, no service restarts.
- Scratch: `S=/fast/scratch/hyaku/kasegi-r41/ExecC2Capture` (all work copies, `TMPDIR=$S`, fixtures under `$S`); removed before this report was finished — a surviving scratch dir would be an I6-class round-41 defect.
- No lane file other than the two deliverables and this receipt was written; no mutating git/jj command was run anywhere.
