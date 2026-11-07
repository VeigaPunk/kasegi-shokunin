# GitHub prefixed tokens in captured evidence — a classic token is one of five three-letter prefixes, an underscore and 36 base62 characters whose last six are a checksum; the stateless installation form is `ghs_<app-id>_<JWT>`; the lane's scanner matches both shapes without an adjacent key name, names fine-grained `github_pat_` as a known limit, and the operating rule is scan before the commit, bind any allowlist row to a digest, and never print the value

source: S136 — GitHub Docs, About authentication to GitHub — https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github — anchors `corpus/source-snapshots/round-92/S136.txt:158` and `:160` (capture 178 lines, 13,895 bytes, sha256 f0edd23c8d6d53a066a6bb90fe4f4f754746df418d833acfc48c44d13943cca0; manifest `corpus/source-snapshots/round-92/manifest.json` records `Q01-prefix-rule` at anchor 158 and `Q02-stateless-40` at anchor 160, each `occurrences=1`; fetched 2026-11-07T08:59:56Z, HTTP 200, kind html); S137 — The GitHub Blog, Behind GitHub's new authentication token formats — https://github.blog/engineering/platform-security/behind-githubs-new-authentication-token-formats/ — anchors `corpus/source-snapshots/round-92/S137.txt:156`, `:167` and `:173` (capture 274 lines, 15,676 bytes, sha256 e4aaf2280203278c954124d8a62ac646c8ce2b3a96348ae3e90cbe173e26640d; manifest records `Q01-three-letter-prefixes` at 156, `Q02-checksum-6` at 167 and `Q03-base62-30` at 173, each `occurrences=1`; fetched 2026-11-07T09:00:04Z, HTTP 200, kind html); instrument — `corpus/instruments/capture-secret-scan.py` at `58c0c115342877ee556cae19928d69839b0b29f0`, sha256 04666f676c09cc3d32e41d506c8198936ac04aff33b207813aab39304baf3a9e, every `capture-secret-scan.py:N` below read at that revision; registry rows `corpus/SOURCES.md:148` (S136) and `corpus/SOURCES.md:149` (S137), both tier A and `queued` with `used-by —`.
verified-at: 2026-11-07 (re-opened at the pinned bytes: `sha256sum corpus/source-snapshots/round-92/S136.txt corpus/source-snapshots/round-92/S137.txt` prints `f0edd23c8d6d…` and `e4aaf2280203…`, equal to the manifest `sha256`; `python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-92/manifest.json --source S136` prints `S136:sha256 OK`, `S136:Q01-prefix-rule OK occurrences=1 anchor=158-ok`, `S136:Q02-stateless-40 OK occurrences=1 anchor=160-ok`, rc 0, and `--source S137` prints `sha256 OK` plus three `Q0n … OK occurrences=1 anchor=N-ok` lines, rc 0; `python3 -B corpus/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-92/S136.txt corpus/source-snapshots/round-92/S137.txt` prints `CAPTURE-SECRET-SCAN mode=files scanned=2 hits=0 files=0 allowed=0 unused_allow=19 rc=0`; `git show 58c0c115342877ee556cae19928d69839b0b29f0:corpus/instruments/capture-secret-scan.py | sha256sum` prints `04666f67…`, the frozen candidate digest, and the same file at the round-92 base `0628fd247914555838a42c02ba5d4ac08b7e095d` prints `89e283c6…` and carries no `github` shape; the landed instrument's `--selftest` prints `SELFTEST-RESULT pass cases=68`; FC-1 to FC-6 below are the runs).
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-92/manifest.json --source S136 && python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-92/manifest.json --source S137 && python3 -B corpus/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-92/S136.txt corpus/source-snapshots/round-92/S137.txt

## Attribution

S136 is GitHub's own current authentication page (`corpus/SOURCES.md:148`, tier A): every sentence here about the prefix rule, the prefix table, the 40-character note and the stateless rollout is GitHub's statement about its own tokens. S137 is GitHub engineering's own blog account of the token format (`corpus/SOURCES.md:149`, tier A): every sentence about the three-letter prefix design, the `_` separator, the checksum and the entropy arithmetic is GitHub's statement about the format it designs. Neither page is a statement about any other provider's tokens, and S137 describes the 2021 design of the classic format while S136 is the current documentation of the resulting prefixes — the blog says `ghp` and separately adds `_` (`corpus/source-snapshots/round-92/S137.txt:156`, `:162`), the docs table shows the joined form (`corpus/source-snapshots/round-92/S136.txt:161-167`). Both rows are `queued` with `used-by —` in the round-92 manifest; this entry is not yet their registered use.

The scanner is the lane's instrument (`corpus/instruments/capture-secret-scan.py` at `58c0c11`). Its shape set, boundaries, scope and output are lane design choices, not a vendor statement, and every sentence in Claim 5 and Claim 6 is about the instrument's own bytes at that revision.

`corpus/source-snapshots/round-92/S138.txt` (the W3C HAR draft) is committed beside these two but is not a source of this entry: its registry row is `rejected` (`corpus/SOURCES.md:150`) because the document states it was abandoned, and it carries no statement about token formats.

## Claim 1 — the prefix rule, and the five classic prefixes

> "GitHub issues tokens that begin with a prefix to indicate the token's type." — `corpus/source-snapshots/round-92/S136.txt:158`

That is the whole detection premise: the type is in the token itself, so a capture does not need an adjacent key name, a header, or a query parameter for the token to be identifiable. S137 states the design decision behind the prefix:

> "We are including specific 3 letter prefixes to represent each token, starting with a company signifier, gh, and the first letter of the token type." — `corpus/source-snapshots/round-92/S137.txt:156`

> "Thus, we are adding a separator: _. An underscore is not a Base64 character" — `corpus/source-snapshots/round-92/S137.txt:162`

The five classic prefixes are the blog's five token types, one line each (`corpus/source-snapshots/round-92/S137.txt:157-161`): `ghp` for personal access tokens, `gho` for OAuth access tokens, `ghu` for user-to-server tokens, `ghs` for server-to-server tokens, `ghr` for refresh tokens. The docs table pairs the same letters with `_` attached — `ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_` — beside the token type each authenticates (`corpus/source-snapshots/round-92/S136.txt:161-167`), and lists a sixth prefix, `github_pat_`, for fine-grained personal access tokens (`corpus/source-snapshots/round-92/S136.txt:163`).

Lane reading: five prefixes are in the classic shape and the sixth is not (Claim 6). The blog's sentence is about design intent, not about which prefixes exist today; the docs table is the current list, and it is why the fine-grained prefix is a named limit rather than a covered case.

S137 states why the separator is an underscore: it is not a base64 character, so encoded data cannot reproduce a token by accident (`corpus/source-snapshots/round-92/S137.txt:162`). The scanner's boundary is a related but separate choice — it refuses a match preceded or followed by `[A-Za-z0-9_]`, so a token is never carved out of a longer identifier (`corpus/instruments/capture-secret-scan.py:156`, `:160`). That boundary is lane design, not a vendor rule; the vendor sentence is what makes the prefix plus underscore a stable byte anchor.

> "With this prefix alone, we anticipate the false positive rate for secret scanning will be down to 0.5%." — `corpus/source-snapshots/round-92/S137.txt:164`

Lane reading: the prefix is a *high-confidence* marker, not a proof. GitHub's own figure is an expectation for its secret-scanning product, and it is stated before the checksum is introduced (`:165-167`), so it is the floor a prefix-only match gives; the checksum is what Claim 2 adds.

## Claim 2 — 36 base62 characters after the prefix, 40 characters in all

> "A 32 bit checksum in the last 6 digits of each token" — `corpus/source-snapshots/round-92/S137.txt:167`

> "We start the implementation with a CRC32 algorithm, a standard checksum algorithm." — `corpus/source-snapshots/round-92/S137.txt:167`

The alphabet is named by the entropy arithmetic, which multiplies the size of `a-z`, `A-Z` and `0-9`:

> "Math.log(((“a”..“z”).to_a + (“A”..“Z”).to_a + (0..9).to_a).length)/Math.log(2) * 30 = 178" — `corpus/source-snapshots/round-92/S137.txt:173`

Sixty-two characters over 30 positions, plus a 6-character checksum, is 36 base62 characters after the prefix; the 62-character class, the 30 and the 6 are all stated on the two lines cited, and the scanner's classic alternative is exactly that arithmetic (`corpus/instruments/capture-secret-scan.py:84-85`, `:160`):

> "followed by exactly 36 base62 characters" — `corpus/instruments/capture-secret-scan.py:84-85`

> "all without changing the token length" — `corpus/source-snapshots/round-92/S137.txt:174`

The docs make the arithmetical consequence concrete for a reader whose code assumes the old length:

> "If your application expects or relies on installation tokens being exactly 40 characters long, it may not handle this new token format correctly." — `corpus/source-snapshots/round-92/S136.txt:160`

Lane reading: 4 characters of prefix (`ghp_`) plus 36 of body is 40, which is the length S136 names, and it is the same length the blog says is unchanged (`:174`). The checksum is checkable offline (`:166`), so a matching string can be confirmed fake without a network call; it cannot be confirmed *live* offline, which is Claim 4's distinction. A 35-character or 37-character tail is therefore a shape miss by construction, and the selftest pins both (`corpus/instruments/capture-secret-scan.py:350-351`).

## Claim 3 — the stateless installation form is `ghs_` + numeric app id + a three-segment JWT

> "Starting April 27, 2026, GitHub began a staged rollout of a stateless format (ghs_APPID_JWT) to all newly minted GitHub App installation tokens" — `corpus/source-snapshots/round-92/S136.txt:160`

The same paragraph says the change is why a 40-character assumption breaks, and that GitHub shipped a temporary request header to turn the format on for a caller's own validation (`corpus/source-snapshots/round-92/S136.txt:160`). The rollout is staged, so both forms coexist: a capture taken after 2026-04-27 can hold either.

The scanner admits the stateless form as a second alternative of the same shape: `ghs_`, then 1 to 20 digits, then `_`, then three dot-separated base64url segments of 10 or more characters each (`corpus/instruments/capture-secret-scan.py:160-161`; segment class `_JWT_SEG` at `:157`). The digits are the app id, the three segments are the JWT, and the whole branch shares the classic branch's left boundary (`corpus/instruments/capture-secret-scan.py:156`).

Lane reading: the two alternatives carry different bounds. The classic branch bounds the tail on both sides — 36 base62 characters, not preceded or followed by a letter, digit or `_` (`corpus/instruments/capture-secret-scan.py:87-89`) — while the stateless branch has no trailing boundary after its third segment (`corpus/instruments/capture-secret-scan.py:160-161`), so a longer dotted string whose first three segments satisfy the branch still matches (measured: FC-5's `K-4seg`). That is a widening, not a miss: it cannot hide a token, and it can flag a non-JWT dotted value that begins with `ghs_<digits>_`.

The docstring states the same boundaries as negatives — the page's own placeholder, a bare prefix, a 35- or 37-character tail, an upper-cased prefix, an unknown prefix, a letter-prefixed token, short JWT segments and the fine-grained form are not hits (`corpus/instruments/capture-secret-scan.py:86-96`, cases at `:341-355`) — and the selftest pins each one (FC-4).

## Claim 4 — a capture holding one is treated as a live grant until the owner says otherwise

> "When Git prompts you for your password, enter your personal access token." — `corpus/source-snapshots/round-92/S136.txt:150`

That is the possession rule in GitHub's words: the token is what a client presents in place of a password, for the account and scopes it was minted with. Nothing else accompanies it — no signature over a policy, no bound identity, no expiry parameter in the string itself — so a reader of a capture cannot narrow what the token authorizes from the token's bytes.

> "We strongly encourage you to reset any personal access tokens and OAuth tokens you have." — `corpus/source-snapshots/round-92/S137.txt:177`

Lane reading: GitHub's stated remedy for a possibly compromised token is a reset by the holder, not a wait for expiry. Neither page states a default lifetime, so the only defensible position on a captured token is that it works until it is reset or revoked; that is the operational reading, and it is why the remedy in Claim 7 is "tell the owner and reset", not "note it and move on". The blog's motive sentence is about detection, not about validity:

> "inefficient or even inaccurate detection of compromised tokens for our secret scanning feature" — `corpus/source-snapshots/round-92/S137.txt:153`

Two qualifiers keep this claim honest. First, the grant is scoped: a `ghp_` classic token carries the scopes its owner granted, and a `ghu_`/`ghs_` app token acts for a user or an installation (`corpus/source-snapshots/round-92/S136.txt:164-167`), so the blast radius is read from the token's type, not from the capture. Second, the shape proves the format, not the liveness: a checksum-valid string can still be a revoked token, and only the owner can say. The rule is treat-as-live, not measured-live.

## Claim 5 — what the landed scanner detects, and where it looks

The docstring at `corpus/instruments/capture-secret-scan.py:1-120` is the specification this entry reads; the instrument's sha256 at `58c0c11` is `04666f676c09cc3d32e41d506c8198936ac04aff33b207813aab39304baf3a9e`.

**Scope.** `--rev REV` reads a git tree without checkout and scans capture-class paths only: anything under `corpus/source-snapshots/`, anything under a practice package's evidence directory, any path with a directory segment ending in `-receipts`, and any file whose name starts with `live-` (`corpus/instruments/capture-secret-scan.py:14-21`, `is_capture_path` at `:198-203`). `--files PATH...` scans exactly the named working-tree files whatever their path, and the docstring's instruction is to run it "on every capture before the commit that first adds it" (`:19-21`). A path outside both classes is not scanned by `--rev`: a token pasted into a knowledge entry or a lesson is outside the capture classes, and the gate's own secret shapes are keyed by an adjacent parameter name (`corpus/instruments/claim-package-check.py:135-142`), so neither reaches a bare prefixed token there — only `--files` on that specific file does.

**The shape.** One shape name, `github-token`, with two alternatives (`corpus/instruments/capture-secret-scan.py:81-94`, patterns at `:156-162`):

> "github-token (round 92) a GitHub token in the prefixed format:" — `corpus/instruments/capture-secret-scan.py:81-82`

- classic: `gh[pousr]_` + exactly 36 base62 characters, left boundary not `[A-Za-z0-9_]` except the `n` of a JSON `\n` escape, right boundary not `[A-Za-z0-9_]` (`corpus/instruments/capture-secret-scan.py:84-89`, lookbehind at `:156`);
- stateless: `ghs_` + 1 to 20 digits + `_` + three dot-separated base64url segments of 10+ characters, same left boundary, no right boundary (`corpus/instruments/capture-secret-scan.py:90-92`, `:157`, `:160-161`).

The left boundary's JSON exception exists because several header or query values joined into one JSON string put a `\n` escape immediately before the next value; the round-91 cookie shape carries the same exception (`corpus/instruments/capture-secret-scan.py:72-74`, `:145`), and the selftest pins the joined case (`:344`).

**Output.** Never the matched value: `HIT shape=<s> path=<p> line=<n>` per file and shape, first non-allowed match, then `CAPTURE-SECRET-SCAN mode=<m> scanned=<n> hits=<h> files=<f> allowed=<a> unused_allow=<u> rc=<rc>` (`corpus/instruments/capture-secret-scan.py:114-119`, `report()` at `:256-268`); `rc = 1 if hits else 0` (`:265`); exit 2 on a usage or read error (`:409-413`). A receipt carrying those lines is safe to commit where the fixture is not — the receipt names a path and a line, never a byte of the value.

**Selftest.** The round-92 cases are pinned at `corpus/instruments/capture-secret-scan.py:341-355`: six positives (`gh-classic-pat-prose`, `gh-oauth-json`, `gh-user-to-server`, `gh-installation-json-joined`, `gh-refresh-line-start`, `gh-stateless-installation`) and nine negatives (`gh-stateless-short-segments`, `gh-doc-placeholder`, `gh-bare-prefix`, `gh-35-chars`, `gh-37-chars`, `gh-upper-prefix`, `gh-unknown-prefix`, `gh-letter-before`, `gh-fine-grained-known-limit`). Measured 2026-11-07: fifteen `SELFTEST gh-… ok` lines with those `got=` values, then `SELFTEST-RESULT pass cases=68` (FC-4).

## Claim 6 — the named known limits, and what a clean run means

The docstring names its limits; this list is that list, restricted to the ones that bear on a token, and nothing else is claimed as a limit.

> "Known limits: fine-grained `github_pat_` tokens (S136 line 163; neither opened source states their length or alphabet)" — `corpus/instruments/capture-secret-scan.py:95-96`

> "values soft-wrapped across lines, and gzip/UTF-16/base64-wrapped captures are not detected." — `corpus/instruments/capture-secret-scan.py:100-102`

Four limits bear on a token:

- **Fine-grained `github_pat_` tokens.** The docs list the prefix (`corpus/source-snapshots/round-92/S136.txt:163`), but neither S136 nor S137 states the fine-grained body's length or alphabet, so no bound can be written from these two rows; the selftest pins the miss (`corpus/instruments/capture-secret-scan.py:355`). This is the largest single hole in the shape, because it is a prefix GitHub documents and the scanner does not match.
- **Values split across lines.** A token soft-wrapped over two lines is outside the byte match, because each alternative needs its characters contiguous (`corpus/instruments/capture-secret-scan.py:100-102`).
- **Wrapped captures.** A capture stored gzip-compressed, UTF-16 or base64-wrapped is outside the byte match (`corpus/instruments/capture-secret-scan.py:101-102`).
- **Percent-encoded forms.** The docstring's percent-encoding limit is stated for parameter names and `=` (`corpus/instruments/capture-secret-scan.py:97-99`); lane reading: a capture whose prefix bytes are percent-encoded (for example the `h` of `ghp` written as `%68`) is likewise outside the shape, because the pattern requires the literal prefix.

Three further boundaries are shape clauses rather than limits, and they are what the selftest's negatives pin: a prefix glued to a preceding letter, digit or `_` other than a JSON `\n` escape is not a hit (`corpus/instruments/capture-secret-scan.py:87-89`, case `:354`); a bare prefix with no 36-character tail is not a hit (`:349`); and the prefix is case-sensitive, so an upper-cased prefix is not a hit (`:352`). Those are deliberate false-positive controls, and each is also a way a deliberately garbled capture escapes.

The docstring's remaining named limits concern other shapes — GCS V2 `GoogleAccessId=`/`Signature=` URLs, CloudFront signed cookies held as HAR/JSON name/value objects, Azure SAS parameter names of 8+ letters, and more than 20 other parameters between the two matched ones (`corpus/instruments/capture-secret-scan.py:95-101`) — and they change nothing about the token reading.

A clean run therefore means "no string in the capture matched one of these shapes at these boundaries", not "the capture holds no credential". Both pinned captures read clean (FC-2) and neither is a claim that no token appears in the pages' prose: the pages' values are documentation placeholders, and the scanner's negatives are what keep them from being hits (`corpus/instruments/capture-secret-scan.py:348-349`).

## Claim 7 — the operator checklist

1. **Scan before the commit that first adds the capture**, with `--files` on each new capture, and paste the `CAPTURE-SECRET-SCAN … rc=` line into the round receipt (`corpus/instruments/capture-secret-scan.py:19-21`). The `--rev` form is for the tree after the fact; the `--files` form is the one that runs before it.
2. **Bind any allowlist exemption to a digest, not to a shape.** A row is `path<TAB>shape<TAB>sha256-of-matched-bytes<TAB>reason` (`corpus/instruments/capture-secret-scan.py:105-112`, `load_allow` at `:168-183`); it binds one exact matched value at one path, so the same shape with a different value at the same path is still a hit (`:214-221`). A malformed or refused row is exit 2, not a silent pass (`:179-181`), and rows for a session token are refused outright (`:164`). No row in this round binds `github-token` (`allowed=0` in FC-2).
3. **Never print the value.** The instrument prints shape, path and line (`corpus/instruments/capture-secret-scan.py:114-119`); a seat receipt that pastes a matched string has re-published the credential the scan existed to keep out. Fixtures live in scratch, receipts carry digests and the `HIT`/summary lines.
4. **On a hit, treat the token as live and route the reset to its owner** (Claim 4; `corpus/source-snapshots/round-92/S137.txt:177`), then redact the capture's value and record the pre-redaction digest beside the committed one — the round-86 manifest's `redaction` block is the model (`corpus/source-snapshots/round-86/manifest.json:47-54`).
5. **Read a clean run as a shape statement** (Claim 6), and re-run the scan when the shape set changes: the base instrument at `0628fd2` reads `hits=0` on every token fixture this entry exercises (FC-3), which is exactly the hole the round-92 extension closed.

## How a researcher uses this

1. **Look for the prefix, not for a key name.** A `ghp_`, `gho_`, `ghu_`, `ghs_` or `ghr_` inside any capture-class file is the detector's target (`corpus/instruments/capture-secret-scan.py:81-89`); no `token=`, `Authorization:` or quote key is needed (Claim 1).
2. **Count the tail.** 36 base62 characters after the prefix, with boundaries, is the classic shape (Claim 2); a 35- or 37-character tail is either a truncated capture or a different string, and it is worth looking at the raw capture rather than at the rendered text.
3. **Recognise the stateless form separately.** `ghs_<digits>_<three base64url segments>` is the current installation-token format, and a 40-character assumption in a parser is the failure S136 names (Claim 3).
4. **Treat the string as a live grant** until the owner resets it (Claim 4).
5. **Redact the value, keep the evidence** — path, line, shape and a digest of the matched bytes let a later reader re-check the finding without the token (Claim 7).
6. **Check the limit before declaring a capture clean of tokens**: fine-grained `github_pat_`, soft-wrapped values, encoded wrappers (Claim 6).

## Falsifiable rule and checks

**Falsifiable rule.** Any sentence asserting that a capture holding a classic prefixed GitHub token with a 36-character base62 tail is credential-free is falsified by `python3 -B corpus/instruments/capture-secret-scan.py --files <capture>` exiting 1 with a `HIT shape=github-token` line. Any sentence asserting that the round-92 base instrument detected that form is falsified by FC-3, where the base instrument prints `hits=0` on the same fixture. Any sentence asserting that a 35-character or 37-character tail, an upper-cased prefix, a bare prefix or a fine-grained `github_pat_` token is detected is falsified by FC-5 and by the selftest's `got=none` lines (FC-4).

**FC-1 — every block quote is verbatim at its anchor, and every backticked citation lies inside its file.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B .ufo/waves/round-91/l1/quote-anchor-check.py --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --rev 58c0c115342877ee556cae19928d69839b0b29f0 .ufo/waves/round-92/w1/candidate-knowledge-github-prefixed-tokens.md
```

Measured 2026-11-07: `QUOTE-ANCHOR checked=0 bad=0 cites=0 out_of_range=0`, rc 0 — and the count is 0 for a reason worth stating: with `--rev`, `quote-anchor-check.py` loads the *entry* itself at that revision (`git show REV:ENTRY`), and a candidate that lives only in the wave directory does not exist at `58c0c11`, so there is nothing to read. The form that actually checks the quotes materialises the landed tree and runs the same tool over it:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
T=$(mktemp -d -p "${TMPDIR:-/tmp}") || exit 9   # set TMPDIR to a scratch dir
git archive 58c0c115342877ee556cae19928d69839b0b29f0 | tar -x -C "$T"
mkdir -p "$T/.ufo/waves/round-92/w1"
cp .ufo/waves/round-92/w1/candidate-knowledge-github-prefixed-tokens.md "$T/.ufo/waves/round-92/w1/"
python3 -B .ufo/waves/round-91/l1/quote-anchor-check.py --lane "$T" .ufo/waves/round-92/w1/candidate-knowledge-github-prefixed-tokens.md
rm -rf -- "$T"
```

Measured 2026-11-07: `QUOTE-ANCHOR checked=17 bad=0 cites=81 out_of_range=0`, rc 0 — seventeen block quotes verbatim at their anchors and eighty-one backticked citations inside their files, every source file read from the landed tree (the instrument's bytes there are the frozen candidate bytes, FC-6).

**FC-1b — no quote exceeds the 25-word cap.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B - <<'PY'
import re
Q = re.compile(r'^> "(.+)" — `([^`:]+):(\d+)(?:-(\d+))?`')
f = '.ufo/waves/round-92/w1/candidate-knowledge-github-prefixed-tokens.md'
n = bad = 0
for i, ln in enumerate(open(f, encoding='utf-8'), 1):
    m = Q.match(ln)
    if not m:
        continue
    n += 1
    w = len(' '.join(m.group(1).split()).split())
    ok = w <= 25
    bad += not ok
    print('%s:%d words=%d %s' % (f, i, w, 'OK' if ok else 'OVER'))
print('QUOTE-WORDS quotes=%d bad=%d' % (n, bad))
raise SystemExit(1 if bad else 0)
PY
```

Measured 2026-11-07: seventeen `OK` lines (words from 6 to 25; the widest is `corpus/source-snapshots/round-92/S137.txt:156` at exactly 25) and `QUOTE-WORDS quotes=17 bad=0`, rc 0.

**FC-2 — the pinned captures match their manifest digests, and both read clean.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
sha256sum corpus/source-snapshots/round-92/S136.txt corpus/source-snapshots/round-92/S137.txt
python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-92/manifest.json --source S136
python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-92/manifest.json --source S137
python3 -B corpus/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-92/S136.txt corpus/source-snapshots/round-92/S137.txt
```

Measured 2026-11-07: `f0edd23c8d6d53a066a6bb90fe4f4f754746df418d833acfc48c44d13943cca0` for S136 and `e4aaf2280203278c954124d8a62ac646c8ce2b3a96348ae3e90cbe173e26640d` for S137, both equal to the manifest `sha256`; seven `OK` lines across the two recheck runs — `S136:sha256 OK`, `S136:Q01-prefix-rule OK occurrences=1 anchor=158-ok`, `S136:Q02-stateless-40 OK occurrences=1 anchor=160-ok`, then `S137:sha256 OK`, `S137:Q01-three-letter-prefixes OK occurrences=1 anchor=156-ok`, `S137:Q02-checksum-6 OK occurrences=1 anchor=167-ok`, `S137:Q03-base62-30 OK occurrences=1 anchor=173-ok` — each rc 0; and `CAPTURE-SECRET-SCAN mode=files scanned=2 hits=0 files=0 allowed=0 unused_allow=19 rc=0`, rc 0. The captures read clean by absence, not by exemption: no allowlist row binds `github-token` (`allowed=0`).

**FC-3 — the shape is load-bearing: the landed instrument fires where the base instrument does not.** Fixtures are generated in `$TMPDIR`, which must be a scratch directory; the fixtures are under 1 KB each and are deleted at the end. No fixture bytes are pasted here.

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
T=$(mktemp -d -p "${TMPDIR:-/tmp}") || exit 9
mkdir -p "$T/base" "$T/fx"
git show 58c0c115342877ee556cae19928d69839b0b29f0:corpus/instruments/capture-secret-scan.py > "$T/landed.py"
git show 58c0c115342877ee556cae19928d69839b0b29f0:corpus/instruments/claim-package-check.py > "$T/claim-package-check.py"
mv "$T/landed.py" "$T/capture-secret-scan.py"
git show 0628fd247914555838a42c02ba5d4ac08b7e095d:corpus/instruments/capture-secret-scan.py > "$T/base/capture-secret-scan.py"
git show 0628fd247914555838a42c02ba5d4ac08b7e095d:corpus/instruments/claim-package-check.py > "$T/base/claim-package-check.py"
python3 -B - "$T" <<'PY'
import sys
T = sys.argv[1]
tail = 'Ab3' * 12                    # exactly 36 base62 characters, built here and never written whole
jwt  = 'eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJ4In0.c2lnbmF0dXJl'
open(T + '/fx/A.txt', 'w').write('use ghp_' + tail + ' as the password\n')
open(T + '/fx/B.txt', 'w').write('token ghs_123456_' + jwt + ' end\n')
open(T + '/fx/C.txt', 'w').write('{"x":"a\\nghs_' + tail + '"}\n')
PY
for f in A B C; do
  printf '%s landed: ' "$f"; python3 -B "$T/capture-secret-scan.py" --files "$T/fx/$f.txt" | grep -E '^(HIT|CAPTURE)' | sed "s#$T#<T>#g" | tr '\n' '|'; echo
  printf '%s base:   ' "$f"; python3 -B "$T/base/capture-secret-scan.py" --files "$T/fx/$f.txt" | grep -E '^(HIT|CAPTURE)' | sed "s#$T#<T>#g" | tr '\n' '|'; echo
done
rm -rf -- "$T"
```

Measured 2026-11-07: `A landed: HIT shape=github-token path=<T>/fx/A.txt line=1|CAPTURE-SECRET-SCAN mode=files scanned=1 hits=1 files=1 allowed=0 unused_allow=0 rc=1|`, and the same shape for `B` and `C`; `A base: CAPTURE-SECRET-SCAN mode=files scanned=1 hits=0 files=0 allowed=0 unused_allow=0 rc=0|`, and the same for `B` and `C`. Six lines, three hits landed and three misses at the base. `unused_allow=0` because the scratch copies carry no allowlist; the landed working-tree run over the same shapes reports `unused_allow=19` (FC-5). The scratch copies are deleted at the end of the block; the digest of the base instrument is `89e283c6423216917c8ae31e1f72239f56ebcb842bda72f7bad4b2f36dc526d7` and of the landed one `04666f67…` (FC-6).

**FC-4 — the selftest pins the round-92 cases.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B corpus/instruments/capture-secret-scan.py --selftest | grep -E '^SELFTEST gh-|^SELFTEST-RESULT'
```

Measured 2026-11-07: fifteen `SELFTEST gh-… ok` lines — six `got=github-token` (`gh-classic-pat-prose`, `gh-oauth-json`, `gh-user-to-server`, `gh-installation-json-joined`, `gh-refresh-line-start`, `gh-stateless-installation`) and nine `got=none` (`gh-stateless-short-segments`, `gh-doc-placeholder`, `gh-bare-prefix`, `gh-35-chars`, `gh-37-chars`, `gh-upper-prefix`, `gh-unknown-prefix`, `gh-letter-before`, `gh-fine-grained-known-limit`) — then `SELFTEST-RESULT pass cases=68`, rc 0.

**FC-5 — the named limits and the shape boundaries are real.** Fixtures generated in `$TMPDIR`; only the `HIT`/summary lines are pasted.

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
T=$(mktemp -d -p "${TMPDIR:-/tmp}") || exit 9
python3 -B - "$T" <<'PY'
import sys
T = sys.argv[1]
tail = 'Ab3' * 12
jwt  = 'eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJ4In0.c2lnbmF0dXJl'
open(T + '/D-fine-grained.txt', 'w').write('github_pat_' + tail[:22] + '_' + (tail + tail)[:59] + '\n')
open(T + '/E-35.txt', 'w').write('ghp_' + tail[:35] + '\n')
open(T + '/F-37.txt', 'w').write('ghp_' + tail + 'Z\n')
open(T + '/G-upper.txt', 'w').write('GHP_' + tail + '\n')
open(T + '/H-bare.txt', 'w').write('Personal access token (classic) ghp_ Managing your personal access tokens\n')
open(T + '/I-placeholder.txt', 'w').write('a stateless format (ghs_APPID_JWT) to all newly minted\n')
open(T + '/K-4seg.txt', 'w').write('ghs_123456_' + jwt + '.ZZZZZZZZZZ\n')
open(T + '/N-percent.txt', 'w').write('%67hp_' + tail + '\n')
PY
for f in D-fine-grained E-35 F-37 G-upper H-bare I-placeholder K-4seg N-percent; do
  printf '%s ' "$f"; python3 -B corpus/instruments/capture-secret-scan.py --files "$T/$f.txt" | grep -E '^(HIT|CAPTURE)' | sed "s#$T#<T>#g" | tr '\n' '|'; echo
done
rm -rf -- "$T"
```

Measured 2026-11-07: seven `hits=0 files=0 … unused_allow=19 rc=0` lines — `D-fine-grained`, `E-35`, `F-37`, `G-upper`, `H-bare`, `I-placeholder`, `N-percent` — and one hit, `K-4seg` printing `HIT shape=github-token path=<T>/K-4seg.txt line=1` then `CAPTURE-SECRET-SCAN mode=files scanned=1 hits=1 files=1 allowed=0 unused_allow=19 rc=1`. So the fine-grained token, both misshapen tails, the upper-cased prefix, the bare prefix, the page's placeholder and the percent-encoded prefix all read clean while carrying a token-shaped string, and the four-segment stateless string matches on its first three segments.

**FC-6 — the instrument bytes cited here are the frozen candidate bytes, and the base instrument carried no such shape.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
git show 58c0c115342877ee556cae19928d69839b0b29f0:corpus/instruments/capture-secret-scan.py | sha256sum
git show 0628fd247914555838a42c02ba5d4ac08b7e095d:corpus/instruments/capture-secret-scan.py | sha256sum
git show 0628fd247914555838a42c02ba5d4ac08b7e095d:corpus/instruments/capture-secret-scan.py | grep -c 'github-token' || true   # prints 0; grep exits 1 on no match
```

Measured 2026-11-07: `04666f676c09cc3d32e41d506c8198936ac04aff33b207813aab39304baf3a9e` for the landed rev (the frozen candidate digest, equal to `claims.json`'s `candidate_sha256`) and `89e283c6423216917c8ae31e1f72239f56ebcb842bda72f7bad4b2f36dc526d7` for the base rev, then `0` — the base instrument carries no `github-token` string at all, which is what FC-3 measures behaviorally.

## Rejected over-generalizations

1. **"A GitHub token is 40 characters, so a 40-character string is a token."** Rejected: the length is a property of the classic format only (`corpus/source-snapshots/round-92/S136.txt:160`), the stateless form breaks it, and the scanner's classic branch requires a 36-character *base62* tail after a prefix, not any 40 characters (`corpus/instruments/capture-secret-scan.py:84-89`).
2. **"A prefixed string is a live token."** Rejected: the prefix plus checksum proves the format, and the checksum is checkable offline (`corpus/source-snapshots/round-92/S137.txt:166-167`); liveness needs the owner (Claim 4).
3. **"`github_pat_` is covered because `ghp_` is."** Rejected: the docs list it as its own prefix (`corpus/source-snapshots/round-92/S136.txt:163`), neither page bounds its body, and the selftest pins the miss (`corpus/instruments/capture-secret-scan.py:355`).
4. **"A clean scan means the capture holds no credential."** Rejected: the shapes are byte patterns at named boundaries and over named scope (`corpus/instruments/capture-secret-scan.py:87-89`, `:198-203`); FC-5 measures five forms that read clean while carrying a token-shaped string.
5. **"The blog's 0.5% figure is a measured false-positive rate for this scanner."** Rejected: it is GitHub's expectation for its own secret-scanning product (`corpus/source-snapshots/round-92/S137.txt:164`), stated before the checksum; the lane's measurement of its own shape is the selftest's negatives (FC-4).
6. **"A stateless hit proves a JWT."** Rejected: the branch bounds three segments of 10+ characters with no trailing boundary (`corpus/instruments/capture-secret-scan.py:160-161`), so a longer dotted string matches on its first three segments (FC-5's `K-4seg`); the hit says the bytes begin with the installation-token form, not that the remainder is a well-formed JWT.
7. **"The docs' `ghs_APPID_JWT` is a token example."** Rejected: it is the page's own placeholder — four characters of prefix, a symbolic app-id field and a symbolic JWT — and it satisfies neither branch's bound; both the selftest and FC-5 pin it as not detected (`corpus/instruments/capture-secret-scan.py:348`).
8. **"The scan covers a token pasted into a knowledge entry or a lesson."** Rejected: `--rev` scans capture-class paths only (`corpus/instruments/capture-secret-scan.py:198-203`), a knowledge file is outside that class, and the gate's shapes there are keyed by an adjacent parameter name (`corpus/instruments/claim-package-check.py:135-142`); only `--files` on the specific file reaches a bare prefixed token.

## Honest limit

- **Two pages, one provider, one format family.** S136 and S137 are GitHub's own statements about GitHub tokens. Nothing here transfers to GitLab, Slack, Stripe or any other provider's prefixed token, even though the prefix pattern shape is common (`corpus/source-snapshots/round-92/S137.txt:156` names Slack and Stripe only as precedent for the idea).
- **The blog is 2021 and was updated in 2023; the docs are current.** The design sentences are GitHub's about the format it shipped; the prefix table and the stateless rollout are the docs' current state (`corpus/source-snapshots/round-92/S136.txt:160-167`), and the blog carries its own dates (`corpus/source-snapshots/round-92/S137.txt:146-148`). The entry reads the blog for structure and the docs for the prefix list, and says so where they differ in spelling.
- **Neither page states a default token lifetime**, so "treat as live" is the operational rule, not a measured property (Claim 4). No live verification is attempted: no token is used, replayed or checked against GitHub, and this lane refuses live-target testing (`PROVINCE.md`).
- **Fine-grained `github_pat_` is uncovered.** That is the largest hole named here, and it is the docstring's own limit (`corpus/instruments/capture-secret-scan.py:95-96`), not a new finding.
- **The stateless branch has no right boundary** (`corpus/instruments/capture-secret-scan.py:160-161`), measured in FC-5; the entry records the widening rather than correcting the instrument.
- **One fixture family, not a corpus.** FC-3 and FC-5 exercise eleven synthetic fixtures in a scratch directory; they show the shape fires, the boundaries hold and the named limits hold, and they say nothing about any real capture's bytes. No fixture bytes are stored here.
- **The SOURCES rows are `queued`.** `corpus/SOURCES.md:148-149` record both as tier A with `used-by —`; this entry is their proposed first use, and the registry update is the L1's integration step, not this file's.
- **The scanner's bounds are the instrument's.** 36 base62 characters, the 1-to-20-digit app id and the 10-character JWT segments are lane choices sized to the two documented forms; a reformatted or partially redacted token falls outside the shape and a clean run says nothing about it.
- Documentation only: no live target was contacted for this entry — every value is read from pinned lane bytes — and the entry carries no credential material, session, private URL or vault reference. Every example is a `<placeholder>` or a generated fixture in scratch.
