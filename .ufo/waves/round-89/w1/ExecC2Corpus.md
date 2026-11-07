# ExecC2Corpus: CloudFront shape FP/FN sweep (round 89, attempt 1)

Seat: ExecC2Corpus (leaf, read-only sweep). Base instrument: `corpus/instruments/capture-secret-scan.py` at master, the frozen C2 landing c61c5586. No lane file was edited; no allowlist row was proposed.

## 1. Four further first-party pages (plain GET, `capture-source.py --kind html`, scratch only)

Master scanner run with `--files` on all four snapshots: `CAPTURE-SECRET-SCAN mode=files scanned=4 hits=0 files=0 allowed=0 unused_allow=19 rc=0`.

| id | page | snapshot sha256 | HIT | why |
|---|---|---|---|---|
| SX1 | CloudFront signed cookies, canned policy | d6fccb86… | miss | Contains only the cookie form (`CloudFront-Signature=`, `CloudFront-Key-Pair-Id=`, cookie value 28 chars). No URL `Signature=` example. Cookie form is the documented known limit; `CloudFront-Signature` also fails the left boundary (`-` before `Signature`) and is under 40 chars. |
| SX2 | CloudFront "Code examples for creating a signature for a signed URL" | 92e3c9bc… | miss | Landing page only. The Perl/PHP/C#/Java example pages it links to are not in the item's four pages and were not fetched. No example signature is present. |
| SX3 | aws-sdk-js-v3 cloudfront-signer README (GitHub) | 6570277c… | miss | Uses placeholder `PUBLIC-KEY-ID-OF-CLOUDFRONT-KEY-PAIR` (hyphens fail `[A-Z0-9]{8,32}`) and no literal `Signature=` value. The snapshot is mostly GitHub page chrome. |
| SX4 | CloudFront private content overview | 126cfa66… | miss | Prose only; no URL or cookie example with a signature value. |

Net: none of the four first-party pages carries a live-shaped or example-shaped CloudFront signed URL. The page-level result is therefore "no hit, nothing to allowlist". The example signatures that would exercise the new shape are the S128/S130 snapshots, which are allowlisted (see §3).

## 2. Fixture sweep (scratch fixtures, 27 cases; values never recorded)

Receipt: `.ufo/waves/round-89/w1/ExecC2Corpus-receipts/fixture-sweep.txt` (case | expected | observed, summary only).

Confirmed as designed:
- HIT: URL both orders; `&amp;` entity; `\u0026` JSON-escaped with Key-Pair-Id first; Policy between Signature and Key-Pair-Id; leading `~-_` in the value; exactly 40 chars; `Signature=` with `==` pad is **not** a hit (see FN-2 below).
- MISS: 39-char value; Key-Pair-Id 7 chars and 33 chars; Key-Pair-Id with trailing lowercase tail; lowercase `key-pair-id`; lowercase `signature`; `X-Amz-Signature=` beside Key-Pair-Id; Set-Cookie form; `Cookie:` header form; `Signature=` with no Key-Pair-Id in prose; newline between the two parameters (soft wrap, known limit).
- Azure: `sv` first with `\u0026` start and `&` separators hit; `sp=r%26sv=…&sig=` hits (the `%26` start boundary works for the leading parameter).

Qualifiers found (not claim failures against the frozen predicate, which fixes the URL-safe charset and the 40/8-32 widths):

- **FN-1 (standard base64 not matched).** `Signature=<30 chars>+<30 chars>==&Key-Pair-Id=…` is not a hit: `+`, `/`, `=` are outside `[A-Za-z0-9_~-]`. CloudFront replaces those with `-`, `_`, `~` (S128 lines 202-211), so a conforming CloudFront signature never contains them. A non-conforming signer, or a value pasted with standard base64, is a real miss. Routed as a qualifier for the L1 (documentation, or a later round if the lane wants standard-base64 coverage). Re-run: `TMPDIR=$S python3 -B corpus/instruments/capture-secret-scan.py --files $S/fx/cf-sig-std-base64-plus.txt` with `$S` the scratch fixture dir.
- **FN-2 (padded value not matched).** `Signature=<60 url-safe chars>==&Key-Pair-Id=…` misses because `=` is not in the class and not a separator. CloudFront does not emit `=` in the signature, so this is by design; qualifier only.
- **FN-3 (`%26` is a start boundary only, not an inter-parameter separator).** Frozen claim text: "azure-sas-signature matches after a \u0026 or %26 separator in any parameter position". The scanner implements `%26` only in `_LB` (start of a match). `…?sp=r%26sv=2022-11-02%26sig=<50 chars>` (sv then sig, joined by `%26`) misses, and so does `…?sig=<…>%26sv=2022-11-02` (sig first). The inter-parameter separator is still `&`, `&amp;` or `\u0026` (`_SEP`). A query whose separators are all `%26` is the percent-encoded-URL-inside-a-URL case, which the scanner's Known limits already list as undetected. So the claim is satisfied for the first matched parameter and for `\u0026`-joined queries, but a reader of "any parameter position" could take it as covering `%26` between every pair. Routed as a wording qualifier: the L1 should decide whether the claim text names only the start boundary. Re-run: `python3 -B corpus/instruments/capture-secret-scan.py --files $S/fx/az-sv-pct26-sig.txt` → NOHIT.
- **Known limits, confirmed by fixture (no action):** Set-Cookie and Cookie-header CloudFront signed cookies miss (`cf-cookie-set-cookie`, `cf-cookie-header-line`); soft-wrapped pair misses (`cf-sig-kpi-newline`); percent-encoded whole URL misses (`cf-url-percent26`).

## 3. Sibling-lane read-only sweep (master scanner, `--lane <sibling> --rev <HEAD>`, no checkout)

Receipt: `.ufo/waves/round-89/w1/ExecC2Corpus-receipts/sweep-summary.txt`.

| lane | rev scanned | scanned | cloudfront hits | other hits (generic `credential`, not this shape) |
|---|---|---|---|---|
| kagi-shokunin | ede4373a (HEAD moved from 27aa53fd during the run; the second tip was re-scanned) | 454 | 0 | 0 |
| kaidoku-shokunin | 0b518f56 | 200 | 0 | 2 |
| kama-shokunin | e6f1dcce | 148 | 0 | 1 |

**No `cloudfront-signed-url-signature` hit in any of the three lanes. No lead on that shape.**

Incidental (not this shape, reported only because the scanner printed them; values not recorded): `kaidoku-shokunin` `.ufo/waves/round-80/w1/ExecBinder/live-16dfa009.json:112` and `live-84d68e90.json:112` (credential, gate SECRET_PATTERNS); `kama-shokunin` `.ufo/waves/round-48/w1/out/K2Selftest/evidence/live-current-driver.out:1` (credential). These are the gate's generic shapes, which this seat does not adjudicate. Routed to the owning lanes as possible FPs for them to check; not touched.

## 4. Allowlist control (already in the claim, reconfirmed)

`corpus/source-snapshots/round-89/S128.txt` and `S130.txt` scanned with `--files`: `hits=0 files=0 allowed=2 unused_allow=17 rc=0`. The two digest-bound rows match.

## 5. Routed items

1. (qualifier, low) FN-1: standard base64 `+ / =` in a `Signature=` value is outside the CloudFront charset. Decide whether the claim text or a known-limits line should name it.
2. (qualifier, low) FN-3: `%26` is accepted only as the start boundary; an all-`%26` query is undetected. Decide whether the azure claim wording or the scanner docstring should name the start-boundary-only scope.
3. (lead, not this shape) generic `credential` hits in kaidoku-shokunin (2) and kama-shokunin (1), listed in §3, for their owning lanes.

No allowlist row, scanner change or fixture was proposed for the lane. The 4 captured pages add no allowlist need.

## 6. Tooling and hygiene

- Installed or upgraded: none. Network: four plain GETs to the four named AWS/GitHub URLs; no other network.
- Credential hygiene: all fixture values were generated into scratch only and never copied into this wave dir. Receipts carry the scanner summary lines, shape/path only, the page sha256 digests, and case names with HIT/NOHIT. No value, no snapshot, no scanner copy is in `w1/`.
- Read-only git only: `git -C <sibling> rev-parse` on three sibling lanes; `git ls-tree`/`cat-file` via the scanner. No checkout, no writes to any sibling.
- Subagents: none spawned. No background job.
- Scratch `/fast/scratch/hyaku/kasegi-r89/ExecC2Corpus/` is removed before yield (see final yield).

## 7. Files written

- `.ufo/waves/round-89/w1/ExecC2Corpus.md` (this report)
- `.ufo/waves/round-89/w1/ExecC2Corpus-receipts/sweep-summary.txt`
- `.ufo/waves/round-89/w1/ExecC2Corpus-receipts/fixture-sweep.txt`
