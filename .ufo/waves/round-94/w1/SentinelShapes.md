# SentinelShapes — adversarial probe of the landed capture-secret-scan (round 94, C2)

**Seat:** SentinelShapes (w1, round 94, attempt 1) · **role:** sentinel · **lane:** kasegi
**Judged on:** depth:verifiability, coverage
**Wave:** one v1 wave of 13 seats (the round-94 `w1-spec.json` item count).
**Surface:** the scanner landed at `996460861d4130ddb2da6b7554e905d3e47504a3` (C2), run as a copy beside that rev's
`claim-package-check.py` and `capture-secret-allow.tsv`. No file outside this report and its receipts was written; no
git/jj mutation was run; every fixture is synthetic and lived in `/fast/scratch/hyaku/kasegi-r94/SentinelShapes`.

## Verdict

**C2 STANDS on the probed scanner surface — three routed defects (D1–D3) and four qualifiers (Q4–Q7), none re-scores C2.**

I re-derived the landed regex behaviour against the vendor regexes that S140 itself quotes (lines 4, 114, 255) and
checked the frozen statement clause by clause on the code at the pinned rev: the `glpat-` custom-prefix class
`(?:[A-Za-z0-9]{1,20}-)?`, the `[A-Za-z0-9_-]{20}` tails, the runner `glrtr?-(?:t[1-3]_)?` and the deploy `gldt-`
shapes, the right boundary `(?![A-Za-z0-9_-])`, the retirement of the round-93 `glrt-` known limit, and the
`xglpat-` negative. I also ran the frozen counter myself: K1–K9 pass at the printed seed `1772304069` and at seeds
`1` and `9191`, `CAPABILITY-CHECK-RESULT pass rc=0` each time. Every one of the 52 encoding fixtures and all 32
boundary fixtures behaves as the statement says. What I found is *outside* the statement: two credential-shaped
vendor classes from the same S140 file are neither detected nor named, the allowlist cannot be derived for a
prefixed token in an escaped context, and two provenance/limit sentences need precision. C1 is out of this seat's
surface; I did not probe the knowledge-meter.

### What was probed and what held

| Probe | Fixtures | Result |
|---|---|---|
| (a) three shapes × 13 encodings (JSON `\t`/`\u0020`/`\u0026`, `%20`, `%26`, HTML `&#x26;`/`&#38;`, line start, after `=`, in a URL, in a `Cookie:` header, quoted JSON value, header colon) | 52 | **52/52 DETECTED** with the right shape (the four `Private-Token: ` fixtures additionally hit the gate's `credential` shape, as designed) |
| (b) boundary class: 1-, 20-, 21-char prefixes, `_` prefix, `-glpat-` at line start, `xglpat-`, dot prefix — each on all three shapes (four token variants: `glpat-`, `glrt-`, `glrtr-t2_`, `gldt-`) | 32 | 28 DETECTED; the 4 `xglpat-` cases MISSED, which is the frozen negative. 21-char and `_`/dot prefixes are detected **on the bare 20-char tail** (span table below), not via the prefix |
| (c) false positives: prose `gldt-`, doc placeholders, 21-char tail, token followed by `-`, `gldt-` inside a word | 36 | prose, angle placeholders (`gldt-<your_token_here>`), `PLACEHOLDER_VALUE`, `mygldt-`, `XGLDT-`, `buildgldt-`, 21-char tails and `token-` are all CLEAN; **the four 20-character placeholders (`gldt-` + 20 `x`) are hits** (Q4) |
| (d) ReDoS, 1 MiB single-line worst cases, each new pattern | 8 shapes × 3 sizes × 3 patterns | linear: 32.7–98.3 ns/byte, 1 MiB ≤ 103.11 ms, 1 MiB/256 KiB ratios 2.31–4.92 (linear = 4.0), no superlinear case; whole instrument on a 1 MiB line 0.55–0.74 s |
| vendor differential: landed vs the verbatim S140 regexes on random near-tokens | 12,000 | **0 vendor hits lost**; 18 gain classes, every one the documented escape-terminator extension (`\t`, `\u0020`, `\u0026`, `%20`, `%26`, `%2D`); 3 span classes (prefix absorbed after an escape) |
| frozen counter, three seeds, scratch work dir | K1–K9 | pass, pass, pass (`rc=0` each) |
| scanner selftest on the pinned copy | 101 cases | `SELFTEST-RESULT pass` |

## Findings routed (none re-scores C2)

### D1 — two credential-shaped S140 classes are undetected and unnamed (severity: medium-low, coverage)

**Exploit path.** A capture commits a GitLab **runner registration token** (`GR1348941…`) or a **legacy runner
authentication token** (`t1_`/`t2_`/`t3_` + 20 base32 chars) in the ordinary key `runner_token` /
`registration_token`. The generic gate shape `credential` needs `\b(?:…|token|…)\b` before the separator, and `\b`
fails between `_` and `t`, so it does not fire; no `gitlab-*` pattern matches either class. The pre-commit scan
returns rc=0 and the bytes are committed. That is the M86-2 failure class the instrument exists to prevent.

S140 publishes both classes in the same file the claim sources:
`gitlab_runner_registration_token` (line 101, `\b(GR1348941[0-9a-zA-Z_\-]{20})(?:[[:punct:]]|[[:space:]]|[[:blank:]]|$)`)
and `gitlab_runner_auth_token_legacy_partition` (line 308,
`(?:(?m:^)|[^0-9a-zA-Z_\-\r\n])(t[1-3]_[1-9a-km-zA-HJ-NP-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)`). The legacy rule's two
example lines **were in the redaction set** (`.ufo/waves/round-94/controls/redaction-r94.txt` lines 310–311), so the
rule was seen. A third: `gitlab_deploy_token_in_url` (line 341,
`gitlab\+deploy-token-[0-9]+:([0-9a-zA-Z_\-]{20})@`) — a deploy token in a clone URL, also missed. The docstring's
*Known limits* paragraph names neither class (it names the routable/JWT forms and nine other prefixes, not these).

**Evidence** (`08-unlisted-classes.txt`), one synthetic fixture each, rc and shapes as observed:

```
{"runner_token": "GR1348941abcDEF123456789xyz"}          rc=0 shapes=none
registration_token = GR1348941abcDEF123456789xyz          rc=0 shapes=none
{"token": "GR1348941abcDEF123456789xyz"}                  rc=1 shapes=credential   (only the generic gate shape)
{"runner_token": "t1_ABC123456789abcdefgh"}               rc=0 shapes=none
t1_ABC123456789abcdefgh                                   rc=0 shapes=none
https://u:gitlab+deploy-token-7:0123456789abcdefghij@…    rc=0 shapes=none
```

**Impact.** A real runner registration/auth token or a deploy token in a URL can enter the corpus unremarked. The
instrument's own source file names the shapes; the landing stops one rule short.

**Smallest remediation.** Two lines in the docstring's *Known limits* naming these classes (no widening), and a
round-95 row that lands them from the S140 regexes already in the capture. Not a C2 re-score: the frozen statement
names exactly three shapes, and K8's 61 statement-mapped clauses pass.

### D2 — the claim line binds the capture path to the pre-redaction digest (severity: low, provenance text)

`claims.json` `frontier.sourced_claim` says “capture `corpus/source-snapshots/round-94/S140.txt`, sha256
`04fc5cfa…d921`”. The file at that path is `f3fd09e4…a158c` at **both** the freeze (`96b5033`) and the C2 landing
(`9964608`), 25537 bytes; `04fc5cfa…` (20035 bytes) is the whitespace-collapsed snapshot **before** the 82
example-line replacements, as the manifest note and `redaction-r94.txt` state, and the manifest's
`sources[0].sha256` records the committed `f3fd09e4…`. A verifier hashing the named path gets a mismatch and has to
find the reconciliation in the receipts.

**Impact.** Verification friction, and a plausible false “the capture moved under the pin” alarm.
**Smallest remediation.** In round 95's claims/SOURCES text, cite both digests with their roles (pre-redaction
`04fc5cfa…`, committed `f3fd09e4…`); do not rewrite the freeze. ScoutGitLabRules independently reconciled the same
two digests (its §1), so this is a text-precision defect only.

### D3 — prefix spans make the allowlist row underivable for escaped occurrences (severity: low-medium, operability)

`scan_bytes` keys the allowlist on `sha256(m.group(0))` and the tool never prints matched bytes. The `_GL_PREFIX`
group **cannot change hit/miss** — removing it from all three landed patterns changes 0 of 12,000 random near-token
outcomes — it only moves the match start. Because the left boundary is “not preceded by `[A-Za-z0-9_]`”, the prefix
can begin **inside an escape terminator**, so the match bytes are not the token a human sees:

```
q=a%26acme-glpat-0123456789abcdefghij        match="26acme-glpat-0123456789abcdefghij"   span=[4,37]
\tacme-glpat-0123456789abcdefghij            match="tacme-glpat-0123456789abcdefghij"    span=[1,33]
\u0026a-glpat-0123456789abcdefghij           match="u0026a-glpat-0123456789abcdefghij"   span=[1,34]
\u0020acme-glpat-0123456789abcdefghij        match="u0020acme-glpat-0123456789abcdefghij" span=[1,37]
&#x26;acme-glpat-0123456789abcdefghij        match="acme-glpat-0123456789abcdefghij"     span=[9,40]
```

Concrete cost: with an allowlist row bound to the bare match `sha256("glpat-…") = f7b8f94f…`, the bare fixture is
allowed (`rc=0`, `allowed=1`), while the same tail with `acme-` in front is a hit (`rc=1`, `unused_allow=1`) whose
matched digest is `7fa6cf59…`. A human deriving the row from the visible token value cannot clear the prefixed or
escaped form, and the scanner gives no diagnostic to derive it.

**Impact.** A capture carrying an already-adjudicated token in prefixed/escaped form wedges the pre-commit gate
until someone replicates the regex; blinded troubleshooting.
**Smallest remediation (round 95).** Document that the allowlist binds the whole match span (prefix and escape
residue included) and add a diagnostic that prints only the matched-bytes sha256; alternatively bind rows to the
canonical token substring. Do not widen any pattern.

### Q4 — 20-character documentation placeholders are hits (severity: low, false positive)

`glpat-xxxxxxxxxxxxxxxxxxxx`, `glrt-xxxxxxxxxxxxxxxxxxxx`, `gldt-xxxxxxxxxxxxxxxxxxxx` → `rc=1`. This is
indistinguishable from a token by shape; the AWS documented key id has an `ALLOWED_VALUES` entry, but a generic
20-`x` GitLab placeholder must **not** be globally allowed. A future doc capture (the S140 intake is the precedent:
it was refused and had to be redacted) will be refused until a per-path allowlist row is added.
**Remediation.** Use the documented allowlist row at the capture path; note the cost in the capture-intake guide.

### Q5 — escape terminators outside the documented seven forms are a blind spot (severity: low, known limit)

`a\x26glpat-0123456789abcdefghij` → `rc=0`; `a\012glpat-…` → `rc=0`; the covered `a\u0026glpat-…` → `rc=1`. The
vendor's own `\b` regex misses these too (0 losses in the differential), and the docstring lists the seven supported
forms, so this is honest rather than broken. **Remediation.** Name `\xXX`/octal in the *Known limits* sentence in
round 95.

### Q6 — token followed by `-`/`_`, or a 21-char tail, is not a hit (severity: low, boundary)

`gldt-0123456789abcdefghij-` → `rc=0`; `glpat-…k` (21) → `rc=0`. This is the vendor's own right boundary
(`(?:[^0-9a-zA-Z_\-]|$)`), so it is source-faithful, but a real token followed immediately by a punctuation hyphen
or underscore is missed. **Remediation.** Name it as a known limit; no change without a source.

### Q7 — note so it is not misread as a false positive

`xacme-glpat-0123456789abcdefghij` is a hit with span `xacme-glpat-…`: the letter before the *prefix* is not a
boundary failure, because the match can start at the bare `glpat-` where the preceding `-` is a valid boundary. The
vendor regex behaves identically. The frozen clause “a letter immediately before the prefix without a hyphen is
still not a hit” holds for `xglpat-` (the case it targets), not for a hyphenated tail.

## Why this is not a C2 verdict change

Every clause of the frozen C2 statement that I probed re-derives true on the pinned bytes: the three shapes'
patterns are byte-for-byte the vendor rules at S140 lines 4/114/255 (modulo the lane's documented escape-terminator
left-boundary extension, which the differential shows only ever *adds* hits), the custom-prefix class matches every
1–20 alphanumeric prefix, the right boundary is `(?![A-Za-z0-9_-])`, the round-93 `glrt-` limit is retired, and the
counter's K1–K9 pass at all three required seeds. D1/Q4–Q7 are coverage and operability residue outside the three
named shapes; D2 is a citation-precision defect. None of them touches P1–P4 of the frozen claim, and per the wave
rules a finding that does not re-score a claim is a routed defect, not a verdict change.

## Receipts

All receipts are under `.ufo/waves/round-94/w1/SentinelShapes-receipts/`. Every driver below exited `rc=0`; the
per-fixture scanner rc is in its row (0 = no hit, 1 = hit, 2 = usage/read error). Scratch (removed on exit):
`/fast/scratch/hyaku/kasegi-r94/SentinelShapes`, with `TMPDIR` set to it for every run.

| # | File | Command (cwd `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless noted) | Observed |
|---|---|---|---|
| 01 | `01-pins-and-anchors.txt` | `git cat-file -t 9964608…`; `git show --stat 9964608`; `sha256sum pkg/*`; `git show <rev>:corpus/source-snapshots/round-94/S140.txt \| sha256sum` (freeze and landing); `grep -c '^id = ' S140.txt`; `grep -n "regex = .*gl\(pat\|rt\|dt\)" S140.txt`; manifest fields | `commit`; 2 files / +47 −14; scanner `22ba32d1…beaf`, gate `8b6f8493…c8e6`, allow `a5abeb53…7c3c`; S140 `f3fd09e4…a158c` at both revs; 30 vendor rules; anchors 4, 114, 255 (and 30, 51, 136, 324); manifest `sha256=f3fd09e4…`; claim line cites `04fc5cfa…` |
| 02 | `02-encoding-matrix.txt` + `02-probe-raw.json` | `python3 -B probe.py` (one fixture file per probe, CLI `--files`) | 52 rows, 52 DETECTED / 0 MISSED |
| 03 | `03-boundary-and-span.txt` | same driver for the boundary fixtures + module import for `m.group(0)` spans | 32 rows: 28 DETECTED / 4 MISSED (all `xglpat-`); span table (15 rows) including the escape-residue starts |
| 04 | `04-false-positive.txt` | same driver for the false-positive fixtures | 36 rows; clean except the four 20-`x` placeholders (rc=1) |
| 05 | `05-vendor-differential.txt` + `05-diff-raw.json` | `python3 -B diff.py` (vendor regexes verbatim from S140 4/114/255; 12,000 random near-tokens) + three escape fixtures through the CLI | `random_cases=12000 vendor_hits_lost_by_landed=0`; 18 gain classes (escape extension only); 3 span classes; `\x26`/`\012` rc=0, `\u0026` rc=1 |
| 06 | `06-prefix-inertness.txt` | remove `_GL_PREFIX` from all three patterns, compare hit/miss over the same 12,000 | `cases=12000 hit-miss_differences=0` |
| 07 | `07-redos.txt` + `07-redos-raw.json` | `python3 -B redos.py` (module import, `finditer` over 64 KiB/256 KiB/1 MiB, min of 3) | 1 MiB ≤ 103.11 ms; 32.7–98.3 ns/byte; ratios 2.31–4.92 |
| 08 | `08-unlisted-classes.txt` | vendor rule inventory; three GitLab patterns from the landed file; nine placement fixtures through the CLI | 30 rules listed; the landed three; rc/shapes as quoted in D1 |
| 09 | `09-cc-default-seed.txt`, `09-cc-seed-1.txt`, `09-cc-seed-9191.txt` | `python3 -B .ufo/waves/round-94/c2/capability-check.py --lane … --rev 9964608… --work $S/work --instrument-sha256 22ba32d1… --gate-sha256 8b6f8493… [--seed N]` | `pass`/`rc=0`, 9 LIMB lines each; seeds `1772304069`, `1`, `9191`; K9 `prev_caught_new=none`, `lost=none` |
| 10 | `10-allowlist-binding.txt` | `python3 -B probe.py` allow-binding section (bare vs `acme-`-prefixed, row bound to the bare digest) | bare `rc=0 allowed=1`; prefixed `rc=1 unused_allow=1`; `f7b8f94f…` vs `7fa6cf59…` |
| 11 | `11-selftest.txt` | `python3 -B pkg/capture-secret-scan.py --selftest`; `--files` on a 1 MiB single-line file | `SELFTEST-RESULT pass cases=101 rc=0`; `rc=0 wall≈0.55–0.74 s` |

Tooling: nothing installed or upgraded this seat (Python 3.14 stdlib only, `git` reads only).
