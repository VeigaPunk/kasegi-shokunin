# SentinelCookie — round 91, attempt 1: adversarial bypass search on the landed C2 shapes

Seat: attack (UFO-FSD sentinel). Leaf; no delegation, no background jobs, no lane writes outside this wave dir.
Surface: `corpus/instruments/capture-secret-scan.py` at `1dd0723fbd0bdc01d2244322f8df8c8c6f1adb70`, run from a scratch
copy beside that rev's `claim-package-check.py` and `capture-secret-allow.tsv`.
Findings are routed defects and qualifiers; **no claim is re-scored**. Nothing below contradicts a frozen predicate:
the landed instrument's own contract behaviour reproduced on every probe I built for it (list in section 3).

## 1. What was run (re-runnable)

| item | value |
|---|---|
| instrument sha256 at 1dd0723 | `89e283c6423216917c8ae31e1f72239f56ebcb842bda72f7bad4b2f36dc526d7` (= frozen candidate sha) |
| gate sha256 at 1dd0723 | `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` (= frozen gate sha) |
| allowlist at 1dd0723 | `76245bbade2f6d0905100913384d5b11ac9ad18b4b3d19f0612f8e152bbc1985`, 19 rows |
| base instrument at bb4309f | `95f24a541db8b3d6693315a03de28d0b6de0fb0b6e53a68471265382114d20ec` (2-6 letter Azure window, no cookie shape) |
| probes | 67 fixtures, one per encoding; values synthetic and assembled at run time |
| landed `--files` over the 67 | `scanned=67 hits=29 files=29 allowed=0 unused_allow=19 rc=1` |
| base `--files` over the 67 | `scanned=67 hits=4 files=4 ... rc=1` (only `az13`, `az19`, `az26`, `az27` — the Azure cases with no `skdutid`) |
| landed `--rev 1dd0723` over the lane | `scanned=1734 hits=0 files=0 allowed=20 unused_allow=0 rc=0`, 3 s |
| landed `--selftest` / base | `cases=53 pass` / `cases=43 pass` |
| negative control | `--files S133.txt S134.txt` → `hits=0 rc=0` (the round-91 snapshots do not trip their own shape) |

Reproduce: `python3 -B .ufo/waves/round-91/w1/SentinelCookie-receipts/repro.py --work $S --scanner <copy of capture-secret-scan.py@1dd0723 beside that rev's gate and allowlist>`.
It rewrites the 67 fixtures and reprints the matrix; output was byte-identical to the recorded run (`REPRO-IDENTICAL`).
Full matrix with per-fixture sha256: `SentinelCookie-receipts/probe-matrix.tsv`. Pins and every control line: `SentinelCookie-receipts/pins-and-runs.txt`.
Scope map: `SentinelCookie-receipts/scope-map.tsv`.

Classification rule used: **DETECTED** = shape fires; **OUT-OF-SCOPE** = no hit and the form is named in the
instrument's Known-limits paragraph *or* the contract requires the miss (case-sensitive name, 28-char doc example,
prose placeholder, 40-char floor, `sig` with no `sv`); **BYPASS** = no hit on a form the docs do not name.
Totals: 29 DETECTED / 21 OUT-OF-SCOPE / 17 BYPASS (2 high realism, 5 medium, 10 low).

## 2. Findings, by severity

### F1 — Medium — colon-form object dumps (the one realistic leak container neither shape covers)
**Evidence:** `cf17` (python dict repr of a cookie jar, realism high), `az24` (`parse_qs`-style dict repr of a query, realism high),
plus `cf18` (JS console object repr, med), `az17` (dict repr of query params, med), `az25` (YAML block, med).
All six are `none` at 1dd0723; fixtures `a4b2fde2…`, `747afaa0…`, `e2da88f6…`, `e55813ba…`, `ec8ce998…` (full digests in the matrix).
**Exploit path:** a seat captures a CloudFront viewer session or an Azure user-delegation SAS, then writes it to a receipt with the
ordinary mapping idiom — `print(response.cookies.get_dict())`, `dict(parse_qsl(url.query))`, `yaml.dump(params)` — into
`.ufo/waves/<r>/w1/<Seat>-receipts/capture.txt`. That path **is** in capture scope (`is_capture_path` True, see scope map),
so the failure is the shapes, not the scope: `--rev`/`--files` report `hits=0`, the live signature is committed and pushed.
Same failure class as lesson M86-2 (a live credential reached the tree because nothing refused the bytes).
**Impact:** with the signature cookie plus `CloudFront-Policy`/`CloudFront-Key-Pair-Id` an attacker fetches any object the policy
covers until policy expiry (S134 lines 19, 40, 96-98; the doc even recommends omitting `Expires`/`Max-Age` (S134 lines 24-27), so a session cookie is
live for the session). For the Azure case the `sig` plus the sibling `sv`/`sr`/`sp` params is a working SAS.
**Smallest remediation:** one bounded alternative per shape — `["']?CloudFront-Signature["']?\s*[:=]\s*["']?[A-Za-z0-9_~-]{40,}` for the
cookie, and for Azure a `sig`/`sv`-in-the-same-object window: a quoted `sig` key whose value is 40+ in-class characters with a quoted
`sv` key within ~200 bytes, either order. Re-run the 17 forgeries (controls F1-F8) and K4/K7/K8 before landing; the colon form must
not fire on the doc placeholder or the 28-char example (both are unquoted prose, so the quoted-key guard is what keeps it clean).
**Calibration:** latent, not yet exercised — across `.ufo/waves` 0 files use `get_dict(`/`parse_qsl(`/`parse_qs(`, while 49 files
mention `Set-Cookie` (the raw-header idiom the landed shape does cover). It is one line of seat habit away from live.

### F2 — Low/Medium — Netscape `cookies.txt` jar (tab-separated columns)
**Evidence:** `cf19`, fixture `1e82b58a…`, `none`. A `curl -c jar` / browser-export artifact stores name and value in separate
tab columns, so the `name=` adjacency the shape needs never appears. Not in the Known-limits paragraph (which names only
HAR/JSON name/value objects).
**Remediation:** third alternative `\tCloudFront-Signature\t[A-Za-z0-9_~-]{40,}`; zero collision risk.

### F3 — Low/Medium — quoted cookie value
**Evidence:** `cf07`, fixture `73fa4fd8…`, `none`. RFC 6265 §4.1.1 defines `cookie-value = *cookie-octet / ( DQUOTE *cookie-octet DQUOTE )`,
so a conforming producer may quote; the shape's value class starts immediately after `=`, so a leading DQUOTE kills the match.
CloudFront's own `Set-Cookie` never quotes (S134 lines 120-130), hence medium at most.
**Remediation:** `CloudFront-Signature="?[A-Za-z0-9_~-]{40,}` (and the Azure `_SIG` likewise).

### F4 — Low — the other spellings of `=`
**Evidence:** `cf14` (`\u003d`, `971b7e89…`), `cf13` (`&#61;`, `4a453aad…`), `cf08` (OWS around `=`, `bd02ca65…`) — all `none`.
Only `%3D` is a documented limit (`cf05`). The shape is otherwise JSON-escape-aware (`\u0026`, `\n`, `%26` in the left boundary), so an
undocumented `\u003d` hole is an inconsistency rather than a design choice.
**Remediation:** fold `\u003d` into the separator alternation (`(?:=|\\u003d)`), keep `&#61;` documented as a limit.

### F5 — Low — a non-letter parameter name ends the Azure window entirely (qualifier, currently unreachable)
**Evidence:** `az22` (`x-ms-version` between `sv` and `sig`, `fb4af688…`), `az23` (`sp1=`, `1ae91bc0…`) — `none`.
The docstring says the window holds "parameter names ... 2-7 letters" and that "an 8-letter name still ends the window"; a name
containing `-` or a digit cannot be skipped at all, so the whole match dies. Blast radius today is nil: every short name in the
Azure table (S133, 35 short names, plus the long name `signature`: `bs bv epk erk rscc rscd rsce rscl rsct saoid scid sdd sduoid se ses sig sip skdutid ske skoid sks skt
sktid skv sp spk spr sr srh srk srq st suoid sv tn`) is letters only and the longest is the 7-letter `skdutid`, so the r91 widening
is exactly complete for documented fields — the "8-letter name" limit is forward-looking only.
**Remediation (optional):** reuse the CloudFront param class `[A-Za-z][A-Za-z0-9_-]{0,31}` for the Azure window and re-check FPs;
the `sv`+`sig` co-occurrence still constrains it. Otherwise add one clause to Known limits.

### F6 — Note (documented scope, process risk) — `--rev` never scans a wave directory
**Evidence (scope-map.tsv):** at `bcbfbde` the tree has 17257 files and `is_capture_path` accepts 1734; **0 of the 20 round-91 wave
files** are accepted. In scope: `corpus/source-snapshots/`, `corpus/practice/<pkg>/evidence/`, any path with a `*-receipts` directory
segment, any file whose name starts `live-`. Out of scope: `w1/<Seat>.md` (the file the L1 actually reads), `w1-dispatch.json`,
`claims.json`, `controls/`, `c1/`, `c2/`, `l1/`.
Consequence: a seat that pastes a capture into its **report** rather than into `<Seat>-receipts/` is invisible to the mode a landing
gate would run; only this round's instruction ("the L1 scans every wave file with the landed scanner") closes it, and that pass is
manual. Cheapest fix: the landing recipe runs `--files` over `w1/` (already this round's rule), or `is_capture_path` gains
`.ufo/waves/` (20 files/round — negligible). Documented scope, so a qualifier, not a claim conflict.

### No findings on these boundaries (checked, clean)
- **Gate pin:** the scanner imports `SECRET_PATTERNS` from the sibling `claim-package-check.py` by `HERE` (directory of the script,
  not the rev), which is exactly the kind of trusted-sibling hole that would let a gate edit silently weaken the shapes — but the
  frozen C2 command pins that file (`--gate-sha256 8b6f8493…`, counter lines 19-20 and 340), and the pin matches at the landing.
  No gap.
- **No mutation:** the `--rev` run is read-only (`git ls-tree` + `git cat-file --batch`); worktree `git status` sha256 identical
  before/after (`96b58ba0…`), `__pycache__` count 8→8, no writes under the lane.
- **Value never printed:** every probe run's output is `HIT shape=… path=… line=…` + the summary line; no matched value in any
  output, including on the two high-realism bypasses.
- **Allowlist binding:** rows are `(path, shape, sha256-of-matched-bytes)`, and the cookie shape's matched bytes include the value,
  so a row can never whitelist a different value at the same path (checked in `load_allow`/`scan_bytes`).
- **Documented limits are truthful:** all 16 documented-limit probes miss (no over-claim), and 2 undocumented probes hit anyway
  (`cf12` obsolete line fold; `az13` base64url value whose first out-of-class character is at offset 60 — the match truncates at 40+
  in-class chars and still fires). Coverage is at least as wide as documented.
- `resume_continuity_v1` does not exist in this lane (only historical wave reports from rounds 30/47 mention it); the nearest
  rejection-must-not-mutate analogue here is the counter/selftest path, which writes only to `--work`.

### Q1 — the 40-char floor cannot hide a live value (checked, with margin)
CloudFront's cookie signature is an RSA signature over the policy, base64 then URL-safe replaced (S134 lines 393-411, 420-428):
even a 1024-bit modulus gives 172 encoded characters, so no real signature fits under the 40-char floor; the floor only excludes
prose and the doc's 28-char example (`cf24`, `cf25`, `cf22`). The Azure signature is HMAC-SHA256 base64 (S133 "encoded by using
Base64 encoding") = 44 characters with padding, 43 without, so the floor sits 3-4 characters under the true minimum and cannot
hide a live SAS either — **but it has only that much margin: raising the floor above 43 would start excluding real SAS
signatures** (`az14` at 39 is the only under-floor miss, and it is not a usable token). Worth pinning in any round-92 change.

## 3. Claim-contract positives reproduced (they hold, for the record)
Cookie shape fires on: `Set-Cookie` baseline (`cf01`), HAR raw header value (`cf03`), `;` and `; ` separators (`cf09`,`cf10`),
real CRLF between headers (`cf11`), bytes repr (`cf15`), `curl -b` (`cf16`), JSON `\n` and `\r\n` joins (`cf20`,`cf21`), exactly-40
value (`cf23`), attributes-first cookie string (`cf29`), `\u0026`/`%26` separators before the pair (`cf31`,`cf32`), raw CRLF inside a
JSON string (`cf33`), mitmproxy-style dump (`cf35`), comma-joined (`cf36`). Correct non-hits: 28-char doc example (`cf24`), prose
placeholder (`cf25`), lower-case name (`cf26`), `X-` prefixed name (`cf27`), 39-char value (`cf22`, documented floor).
Azure: `skdutid` either order (`az01`,`az02`), 20-param window exact (`az03`; 21 misses, `az04`), mixed case (`az05`), `&amp;`
(`az08`), realistic full SAS (`az18`), `%2B/%2F/%3D` (`az19`), raw `+`/`/` (`az26`), `%3D%3D` padding (`az27`), `\u0026` JSON
(`az20`), 19 params then `skdutid` last in window (`az21`).

## 4. Route list for round 92 (smallest first)
1. **R1 (F1) — colon-form object dumps.** Add the quoted-name colon alternative to the cookie shape and the `sig`/`sv` same-object
   window to the Azure shape. Acceptance: `cf17`,`az24`,`cf18`,`az17`,`az25` become hits; `cf24`,`cf25`,`cf02`,`cf04`,`cf42` stay misses.
2. **R2 (F2) — tab-separated cookie jar`: `\tCloudFront-Signature\t[value]{40,}`. Acceptance: `cf19` hits, nothing else changes.
3. **R3 (F3/F4) — optional DQUOTE and `\u003d`** in the name/value separator. Acceptance: `cf07`,`cf14` hit; `cf08`,`cf13` stay
   documented limits.
4. **R4 (F6) — landing gate scans the wave dir**: run `--files` over `w1/*` (and `controls/`, `l1/`) in the landing recipe, or extend
   `is_capture_path`. Acceptance: a planted fixture under `w1/<Seat>.md` is reported by the mode the gate runs.
5. **R5 (F5) — Azure window name class**: widen to `[A-Za-z][A-Za-z0-9_-]{0,31}` or document the non-letter limit explicitly.
6. **R6 (docs) — Known limits paragraph**: name the colon-form dump, the tab/`cookies.txt` jar and the quoted value, so the next
   audit's realism judgement is not re-derived.
7. **R7 (probe corpus) — keep `repro.py`** as the shape's regression set (67 fixtures, synthetic, no literals); it is deliberately
   r91-agnostic so round 92's candidate can be diffed against it (`base` column = 4 hits is the pre-r91 reference).

## 5. Housekeeping
- Scratch `/fast/scratch/hyaku/kasegi-r91/SentinelCookie/` deleted before yield (fixtures, copies, scanner outputs) — **gone**.
- No tool installed or upgraded; no `pacman` transaction; nothing written outside this wave dir and scratch.
- Every file in this seat's output was scanned with the landed instrument before landing: `--files` over
  `probe-matrix.tsv scope-map.tsv repro.py pins-and-runs.txt SentinelCookie.md` → `hits=0 rc=0`.
- No credential-shaped literal in any wave file: fixtures exist only in scratch; probes are identified by id, encoding and sha256.
