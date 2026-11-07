# ReviewC2Scanner — round-91 C2 code and source review

Reviewed at base `bb4309fffbe9bf98153a2933af72c8f2c3f4b5b1`, freeze `53ab692a7b544c35141e2b19f7413cbdb767c1ad`,
C2 landing `1dd0723fbd0bdc01d2244322f8df8c8c6f1adb70` (HEAD `bcbfbde`, receipts only).
Instrument: `corpus/instruments/capture-secret-scan.py`; sources S133 (`corpus/source-snapshots/round-91/S133.txt`)
and S134 (`…/S134.txt`). Receipt: `ReviewC2Scanner-receipts/c2-review-r91.txt`.

**Verdict: REQUEST-CHANGES (routed to r92).** The frozen predicate holds under my own re-run
(P1–P3 all pass, instrument behaves exactly as the statement says on every falsifiable clause), and
the new shape is sound: no code change is requested. The requested changes are documentation and
counter binding — the r89 F1 class recurring: this landing's docstring insertion shifts 29+ explicit
instrument-line cites in two knowledge entries and leaves four sentences asserting the *opposite* of
the landed code (that CloudFront signed cookies are not detected).

## Verified (so the L1 need not re-derive it)

- **P2** — landed instrument sha256 `89e283c6…c526d7` equals the frozen candidate and the claim pin;
  gate `8b6f8493…cc8e6`; wave counter sha256 `39deae67…37b6f0` equals the claim pin.
- **P3** — `git diff-tree --no-commit-id --name-only -r 1dd0723` prints exactly `SCORECARD.md` and
  `corpus/instruments/capture-secret-scan.py`; the capability row is byte-identical to
  `.ufo/waves/round-91/c2/candidate/scorecard-row.txt` (`cmp` clean).
- **P1** — frozen C2 command at the landing, three seeds (run-time `2068659922`, `9191`, `1`):
  K1–K8 pass, `CAPABILITY-CHECK-RESULT pass rc=0`; K3 `scanned=1734 hits=0 files=0 allowed=20
  unused_allow=0`. `--selftest` prints `SELFTEST-RESULT pass cases=53`, rc 0 (base: `cases=43`).
- **Frozen controls** — read, not re-run: F1–F8 each FAIL K4 and K8 (F8 on K4+K8; F5 on K4/K7/K8);
  the no-work base instrument FAILs K4/K7/K8. Each forgery is rejected on behaviour, unpinned.
- **No shadowing, no regression** — `cloudfront-signed-url-signature` cannot fire on
  `CloudFront-Signature=` (its `_CF_LB` rejects the preceding `-`), and the cookie shape cannot fire
  on a `Signature=` URL parameter; all round-89 plants still hit (K4), K3 is clean.
- **Source↔code** — S133 line 177 (`skdutid`) and 566-571 (user-bound SAS, version 2025-07-05+)
  support clause (b); S134 lines 19/40/96-98/428 support the cookie bullet; the documentation's
  example value at S134 line 123 is 28 characters, below the 40 floor, as stated.

## Answers to the questions the seat asked

1. **Is `[A-Za-z]{2,7}` the right bound?** Yes, and it is exact. S133's table (lines 94-227)
   documents 26 distinct SAS portion names: longest is `skdutid` = 7 (line 177), next `sduoid` = 6
   (line 182); `skoid`/`sktid`/`saoid`/`suoid` = 5; shortest are 2 (`sv`, `sr`, `st`, `se`, `sp`,
   `tn`); there is no 1-letter and no 8+-letter SAS portion. The only `&<8+ letters>=` strings in the
   snapshot (`&identifier=`, `&operation=`) are other pages' examples, not SAS fields. Side effect:
   any 7-letter parameter name (`session`, `expires`) is now spanned, not just `skdutid` — bounded,
   because the window still requires `sv=YYYY-MM-DD` and a 40+ `sig=` in one query (probe
   `az-7letter-between` hits; `az-8letter-between` misses).
2. **Does `_CK_LB` with `(?<=\\n)` admit false positives?** It admits a narrow, permissive class,
   never a missed secret: the lookbehind matches any backslash-then-`n` byte pair, including the last
   two bytes of `\\n` (an escaped backslash + `n`, e.g. a JSON-encoded Windows path), and the *first*
   alternative already accepts any non-`[A-Za-z0-9_-]` byte, so `C:\new\CloudFront-Signature=<40>`
   and `foo.CloudFront-Signature=<40>` match. The match still requires the exact cookie name plus a
   40+ URL-safe value, so the residue is a path-like/renamed-cookie false *hit* (allowlist-absorbable).
   A name preceded by a letter is still rejected (`C:\newCloudFront-Signature=<40>` misses).
3. **Is case-sensitivity correct per S134 line 31?** Yes as coded (no `(?i)`); `cf-cookie-lowercase-name`
   pins it and K8's clause binds line 31. The docstring does not cite line 31 for the claim (F3).
4. **Does the new shape duplicate or shadow `cloudfront-signed-url-signature`?** No. Probes:
   `?CloudFront-Signature=<40>` → cookie shape only; `?Signature=<44>&Key-Pair-Id=…` → URL shape only;
   `X-CloudFront-Signature=<40>` → none. The two shapes are disjoint by construction and by the
   selftest's exact-set assertions.
5. **Is the Known-limits list accurate for the new shape?** HAR name/value objects and
   `CloudFront-Signature%3D` are correctly listed and verified to miss. One gap: quoted cookie
   values (`CloudFront-Signature="<40>"`, legal per RFC 6265 §4.1.1 cookie-value) miss and are not
   listed (F4).

## Findings

### F1 — HIGH (routed to r92): the landing shifts 29+ explicit instrument-line cites in two knowledge
### entries and leaves four sentences asserting the opposite of the code
The C2 landing inserts ~22 docstring lines before line 99 and 2 pattern lines before
`CLOUD_PATTERNS`, and 10 selftest cases (+25 shift there). The r90 repair of the r89 F1 class pointed
these entries at the base bytes; every cite at or below the insertion point now resolves to unrelated
text. Shift table (base → landing): `Known limits:` 61→81 (+20); `_SEP`…`_CF_KPI` 99-107→121-129
(+22); `CLOUD_PATTERNS` 108→131 (+23); `def load_allow`/`gate_patterns`/`scan_bytes`/`report`/
`selftest` and the selftest cases +25 (`scan_bytes` 159→184, `report` 209→234, `cf-doc-placeholder`
277→302, `azure-json-escaped-s127-order` 272→297).

- `corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md`: 14 explicit cites shifted
  (entry lines 49, 79, 83, 84, 87, 124, 138, 157, 316, 317, 322, 327, 328, 331), plus bare `:N`
  continuation cites in the same sentences (census: 41 instrument anchors, 33 shifted); `:23-60`,
  `:47-60` and `:1-82` are also stale because the docstring now ends at line 105, not 82.
- `corpus/knowledge/capture-intake-gate.md`: 15 explicit cites shifted (entry lines 53, 69, 71, 73,
  105, 107, 109, 111, 122, 128, 246, 247, 248, 249, 252); `:23-65` is stale for the same reason.
- `corpus/knowledge/presigned-url-credentials-in-captured-evidence.md`: `instrument lines 77-82`
  (entry:69, repointed by r90) now lands in the cookie bullet — output is 99-104; `lines 32-42`
  (entry:13) now truncates the Azure bullet (37-52).

Four sentences are now *false*, not merely mis-numbered (each quoted from the entry):
- cloud entry:79 — "Named limits, verbatim from `…:61-65`: … CloudFront signed cookies
  (`CloudFront-Signature`) … are not detected." Landing 61-65 is the CloudFront-URL paragraph; the
  named limits are 81-87 and no longer exclude signed cookies.
- cloud entry:317 — "the named limits at `…:61-65` exclude … CloudFront signed cookies".
- cloud entry:322 — signed cookies "which the docstring's named limits exclude (`…:61-62`)";
  the shape is implemented at 138-139.
- cloud entry:327 — "Account SAS, user-delegation SAS, GCS V2 and CloudFront signed cookies are
  outside both the entries and the detector's shape set (`…:61-65`)".
- capture-intake-gate.md:109 quotes "…CloudFront signed cookies (`CloudFront-Signature`)…" as a
  current named limit; that text no longer exists. The same file's :105 says "three cloud shapes"
  and lists eleven names — now four cloud shapes and twelve names.
- cloud entry:87 also says "at most 20 intervening parameters with 2-6 letter names (`:100`)"; the
  landed `_PARAM` is `{2,7}` at line 122. And `cases=33` (presigned entry:111) is stale since r89
  (base 43, landing 53).

Re-runnable: `git show bb4309f…:corpus/instruments/capture-secret-scan.py | sed -n '61,65p;99,107p;159,160p;209,221p'`
against `git show 1dd0723f…:… | sed -n '81,87p;121,129p;184,185p;234,246p'`, and
`python3 -B corpus/instruments/anchorcheck.py corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md`
(it prints `OK md:79 … :61-65 [Hash-Algorithm) between: an Amazon CloudFront signed URL, …]` — an
in-range cite with the wrong bytes).
**Fix:** repoint the three entries in an r92 doc commit (the r89 fix pattern), rewrite the four
sentences and the shape/case counts, and re-run `anchorcheck` on all three.

### F2 — MEDIUM (routed to r92): no counter limb binds these anchors, so K1–K8 pass while the docs lie
`anchorcheck.py` is range-only: at the landing it prints `86 in-range cite instances, 0 bad` for the
C2 entry and `69 in-range, 0 bad` for the gate entry, exit 0, while the printed lines are unrelated.
Nothing in `capability-check.py` (K1–K8) or the round-90 gate counter reads the knowledge entries, so
a green claim can coexist with a knowledge entry that denies the capability. **Fix:** add one limb
(e.g. K9) that, for each cited `capture-secret-scan.py:N` in the three entries, asserts the landing
line's first token equals a frozen expectation (the M9/M10 binding style used on the C1 side), or at
minimum run `anchorcheck` and fail on the mismatch set; the r89 routed defect this repeats was closed
only by repointing, not by a check.

### F3 — MEDIUM: the new shape's docstring asserts two clauses it does not cite
(a) The value alphabet "`A-Za-z0-9`, `-`, `_`, `~`" (the `+ → -`, `= → _`, `/ → ~` replacement) cites
only S134 lines 19, 40, 96-98, 428; the source is S134 lines 416-426 ("Replace characters that are
invalid in a URL query string…"). (b) "cookie name case-sensitive" rests on S134 lines 30-31, not
cited. The round-89 URL bullet cites its alphabet source (S128:202-211), so this is a regression in
the docstring's sourcing discipline. **Fix:** add `S134 lines 30-31, 416-426` to the bullet's
citation list (optionally S133 line 56 for the user-bound framing).

### F4 — LOW: Known limits omits quoted cookie values
Probe: `Cookie: CloudFront-Signature="<40 chars>"` yields no hit (the value class starts at `=`),
while RFC 6265 §4.1.1 permits a DQUOTE-wrapped cookie-value and the bullet promises "a `Set-Cookie:`
or `Cookie:` header, or any text". HAR objects and `%3D` are correctly listed. **Fix:** add "quoted
cookie values (`CloudFront-Signature=\"…\"`)" to Known limits, or admit an optional `"` after `=`.

### F5 — LOW: `_CK_LB` is textual, not JSON-aware; the docstring overstates it
The bullet says "unless that is the `n` of a JSON `\n` escape". The lookbehind accepts *any*
backslash-`n` pair, so `"C:\\nCloudFront-Signature=<40>"` (escaped backslash + `n` in JSON) also
matches, and the general boundary accepts any non-`[A-Za-z0-9_-]` byte. Consequence is a false *hit*
on path-like text, never a missed secret; the allowlist absorbs it. **Fix:** reword to "after a
backslash-`n` byte pair" (or tighten the boundary), or record the permissiveness under Known limits.

### F6 — INFO: the statement's "every round-89 shape behaves as before" is imprecise for Azure
Clause (b) widens `azure-sas-signature` by design; probe `?sv=2025-07-05&session=x&sig=<40>` now hits
and the base instrument did not. The round-89 CloudFront-URL and GCS shapes are unchanged, all
round-89 plants still hit (K4), and the landed corpus is clean (K3). No action beyond wording in a
future statement ("the round-89 CloudFront-URL and GCS shapes").

## Residual risk and verification gaps

- No live URL or cookie was exercised (lane prohibition): every positive is a documented example or a
  synthetic fixture. The 40-character floor is safe for real values because the cookie signature is an
  RSA signature over the SHA1/SHA256 hash (S134:396-401, 409-415), i.e. key-length sized, not a 20/32-byte
  digest — `[INFERENCE]` from the RSA wording; no real signed-cookie capture exists in the lane.
- The C2 counter's K7 negatives do not exercise a quoted value or a `%3D` separator; F4's case is
  synthetic.
- I read the frozen forgeries (`c2-controls-r91.txt`) but did not re-run them; F1–F8 FAIL lines are the
  frozen controls' measurements, not mine.
- No LSP device/server is mounted in this runtime (`xd://lsp` → "No such tool"), so caller/definition
  checks were textual (`git show`, grep) — recorded as such, not presented as semantic proof.
