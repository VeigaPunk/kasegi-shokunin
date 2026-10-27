# ExecC2Rows — round-41 wave 1 receipt (C2 structural appends: S063 row, F24 README block, F24 PROVINCE amendment)

Seat: `ExecC2Rows` (executor, leaf). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` only; the fleet
root and `/home/vgpnk/Projects/shokuknow` were read-only to me and were not written. No subagent, labrat
probe, background job or swarm was used. No mutating git/jj command was run anywhere (read-only `git log`,
`git show`, `git archive`, `git cat-file` only). Scratch `S=/fast/scratch/hyaku/kasegi-r41/ExecC2Rows`
(removed at exit). Tooling: nothing installed or upgraded (none needed). Disk guard read before the work:
`/fast/scratch/hyaku 24% use, 610.8G free` — green.

## 1. Deliverables (byte-exact, landable)

| file | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-41/wave1/ExecC2Rows.registry-row.txt` | 1 | 1392 | `41ec51993a09157e1f50df0d857dc5b02146a30e1ff52c42c7820e5aa85a4ce4` |
| `.ufo/waves/round-41/wave1/ExecC2Rows.readme-row.txt` | 29 | 2790 | `367ccdffe7713b158a5d5184deb3d7552ffa9162c4670fde8c3b116d2c0fed4e` |
| `.ufo/waves/round-41/wave1/ExecC2Rows.province-amendment.txt` | 2 | 363 | `c66c823630aa592a57bf8b7c0cb987af33b2eae82db2fdcaed8631932b7a9ed6` |

Byte hygiene on all three: 0 tabs, 0 CR, 0 lines with trailing whitespace, final `\n` present.

- **registry-row.txt** — the one-line SOURCES row `| S063 | … | mined | 2026-10-27 | on-release |
  corpus/knowledge/rfc-9116-security-txt.md |`; 13 awk fields (11 columns, `NF=13`), 0 backticks, no `|`
  inside any cell.
- **readme-row.txt** — the whole appended `## Round-41 admission` block in the round-40 F23 shape:
  separator blank line, heading, R6 paragraph, 3-cell coverage-map row, 6-cell F24 frontier row, and the
  `[r41 amendment, appended 2026-10-27] … **24/24 admitted**` count line. (One line longer than round-40's
  28 because the R6 paragraph wraps to 9 lines.)
- **province-amendment.txt** — 2 lines: blank separator + the F24 amendment line, prefix-identical to the
  F17/F18 form `[rNN Frontier amendment, appended YYYY-MM-DD, end-of-file append per R6] FNN — … —
  admitted round NN; entry <path> (source SNNN)`.

### Landing recipe (measured on the round-40 landing, not assumed)

Round 40's landed diff was reproduced exactly by `landed = prev + b"\n" + deliverable`:

```
$ python3  # round-40: prev/landed git blobs vs ScribeF23.readme-row.txt
prev bytes 49755 landed 52490 deliv 2734
landed ends with deliv: True
extra bytes: b'\n'
```

So each block lands as: write one newline, then `cat` the deliverable (which itself starts with a blank
line). Placement:
- `corpus/SOURCES.md`: insert the row immediately after the `| S062 |` row (present line 68 → new line 69),
  inside `## Registry`, before the blank line + `## Paths`. This is a mid-file insertion, exactly as
  round 40 inserted S060-S062 after S059.
- `corpus/README.md` and `PROVINCE.md`: end-of-file append with the recipe above.

## 2. Capture facts — verified independently, not taken on trust

I fetched the source myself rather than only accepting the sibling's numbers:

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-27T08:19:51Z            # first fetch (pre-wipe)
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o rfc9116.txt \
    -w 'HTTP %{http_code} bytes=%{size_download} url=%{url_effective}\n' \
    https://www.rfc-editor.org/rfc/rfc9116.txt
HTTP 200 bytes=45129 url=https://www.rfc-editor.org/rfc/rfc9116.txt
$ sha256sum rfc9116.txt
79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9  rfc9116.txt
```

Then normalized it with the lane's own instrument (`capture-source.py` `collapse()`), twice — once before
and once after a sibling's over-broad `rm -rf` deleted the shared parent:

```
$ python3  # capture-source.py collapse() over the fetched body
lines 842 bytes 39301 sha256 925512e715be5fae950f3eec88805197d4007875dac825c5603d44d2b71e2faa
$ cmp cap_norm.txt <wave1>/ExecC2Capture.S063.txt && echo IDENTICAL-TO-SIBLING-CAPTURE
IDENTICAL-TO-SIBLING-CAPTURE

# after the wipe, re-fetch and re-normalize:
2026-10-27T08:51:21Z  HTTP 200 bytes=45129
79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9  rfc9116.txt
lines 842 bytes 39301 sha256 925512e715be5fae950f3eec88805197d4007875dac825c5603d44d2b71e2faa
IDENTICAL-TO-SIBLING-CAPTURE
```

So the capture facts in my row (lines/bytes/sha256) are the ones that will land, and the capture is
reproducible from the published URL. The sibling's manifest record (`ExecC2Capture.manifest-record.json`:
`sha256` / `full_text_sha256` = `925512e7…`, `lines` 842, `size_bytes` 39301, `raw_sha256` `79d19ce7…`,
`fetched_utc` 2026-10-27T08:19:23Z) agrees byte-for-byte.

The three quotes the sibling pinned were re-run against the landed bytes on a scratch manifest:

```
$ python3 corpus/instruments/source-recheck.py --manifest <S>/snap/manifest.json --source S063
S063:sha256 OK
S063:Q1 OK normalized=markup-whitespace occurrences=1 anchor=330-ok
S063:Q2 OK normalized=markup-whitespace occurrences=1 anchor=270-ok
S063:Q3 OK normalized=markup-whitespace occurrences=1 anchor=235-ok
exit=0
```

### Splice table — the only markers left in my bytes

`registry-row.txt` carries exactly three `<<<CAPTURE>>>` markers, in the sibling's own idiom and order
(`… (<<<CAPTURE>>> lines, <<<CAPTURE>>> bytes; sha256 <<<CAPTURE>>>) …`), so one splice rule serves both
files:

| marker # | meaning | verified value |
|---|---|---|
| 1 | capture line count | `842` |
| 2 | capture byte count | `39301` |
| 3 | capture sha256 | `925512e715be5fae950f3eec88805197d4007875dac825c5603d44d2b71e2faa` |

The README block and the PROVINCE block contain **no** markers: their locators are RFC section numbers
(`§2.5`, `§2.5.3`, `§2.5.5`, `§3`, `§5.5`), which are document facts and do not depend on the capture's
byte layout.

## 3. Content decisions grounded in the capture (two corrections adopted)

1. **No CSAF field.** `grep -n -i csaf rfc9116.txt` → 0 hits. The RFC defines exactly eight fields
   (Acknowledgments, Canonical, Contact, Encryption, Expires, Hiring, Policy, Preferred-Languages), and the
   anchor cell names those eight and nothing else. (`CSAF` is *not* in RFC 9116; the sibling capture seat
   flagged the same trap, and the register-enum list in the capture confirms it.)
2. **The one-year Expires bound is RECOMMENDED, not MUST.** Verbatim at capture L270-L272: "It is
   RECOMMENDED that the value of this field be less than a year into the future to avoid staleness." The
   separate requirement "This field MUST always be present and MUST NOT appear more than once." is at L273.
   Scope/teaches/anchor never upgrade the RECOMMENDED bound to a MUST.
3. **No `|` in any cell** and the source cell carries exactly one `https://` token, byte-equal to the
   manifest record's `url` (`https://www.rfc-editor.org/rfc/rfc9116.txt`), which is what
   `capture-binding-check.py` rules B4/B5 measure.
4. **PROVINCE entry clause without backticks**, matching the two most recent amendments (F22 r39, F23 r40:
   `entry corpus/knowledge/…md (source S0xx)`). F18-F21 used backticks. The **prefix** is byte-identical to
   F17/F18: `[r41 Frontier amendment, appended 2026-10-27, end-of-file append per R6] F24 — `.

The registry `teaches` cell names the F10 complement as required: the file is the machine-readable channel
while F10's vendor-disclosure-policy objects carry the same intake practice as prose.

## 4. Validation on a scratch mirror (my bytes landed, not simulated)

Mirror = `git archive HEAD corpus PROVINCE.md SKILL.md` into scratch, then my three appends applied with the
landing recipe above, plus the sibling seats' already-delivered stand-ins (`ScribeC2Entry.entry.md` →
`corpus/knowledge/rfc-9116-security-txt.md`, `ExecC2Capture.S063.txt` → `corpus/source-snapshots/round-41/S063.txt`,
a one-record `manifest.json`, and `knowledge-expected.txt` + the entry). Only difference from landed bytes:
the entry's `recheck:` `cd` target repointed at the mirror (same device the round-40 seat used).

### 4.1 The claim's counting commands

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md          23 -> 24        (base -> mirror)
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   62 -> 63
$ awk -F'|' '/^\|[[:space:]]*S063[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); if(s=="mined") n++} END{print n+0}' corpus/SOURCES.md   0 -> 1
$ ls corpus/knowledge/*.md | wc -l                    59 -> 60
$ grep -rlE '^source: S063' corpus/knowledge | wc -l  0 -> 1
```

### 4.2 The instruments (mirror root)

```
$ python3 corpus/instruments/frontier-recheck-count.py --root <mirror>
PASS     F24  knowledge/rfc-9116-security-txt.md                  ids=S063           exit=0
entries=27 pass=27 exit=0

$ python3 corpus/instruments/capture-binding-check.py --root <mirror>
MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=55 … missing_manifest=0 multi_row_url=3 orphans=1 orphan=S040-live.txt
records=55 bound=55 unbound=0          exit=0      (0 FAIL lines)

$ python3 corpus/instruments/recheck-audit.py --root <mirror> --quiet
lines=60 total=60 pass=60 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=60 missing=0 unexpected=0 exit=1
```

The trailing `exit=1` there is a **mirror artifact, not a defect in these bytes**: the audit's STRICT
`cdroot` limb requires each line's `cd <path>` to equal the *audited* root, and 58 pre-existing entries
`cd` the real lane (`strict pass=2/60 cdroot_fail=58`). The same instrument against the real, unmodified
lane is green and its only difference is the root:

```
$ python3 corpus/instruments/recheck-audit.py --quiet     # real lane, 59 entries, nothing landed
lines=59 total=59 pass=59 fail-closed=24 … exit=0
expect=present expected=59 missing=0 unexpected=0 exit=0
```

My entry's own line reads `strict=111111 … PASS` on the mirror once its `cd` points at the mirror root,
which is the limb that resolves on the lane. The three numbers the C2 kill rule names
(`expected=60`, `missing=0`, `unexpected=0`) are all correct.

### 4.3 Sources census (scratch fleet root with a `kasegi|kasegi-shokunin` conf row)

```
$ bash scripts/sources-census.sh validate --root <fleet> --today 2026-10-27 kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/… across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	<fleet>/kasegi-shokunin/corpus/SOURCES.md
validate exit=0

$ bash scripts/sources-census.sh census --root <fleet> --today 2026-10-27 kasegi
kasegi	rows	63
kasegi	tier.A	58   tier.B	3   tier.C	2
kasegi	status.mined	53   status.rejected	10
FLEET	rows	63   FLEET	missing	0
census exit=0
```

`ok`, `rows 63`, and the only warnings are the pre-existing S028/S029 W04s — exactly the claim's
`census exit 0 (W04 S028/S029 only)`. No E-code fired: `NF=13`, kind `spec`, tier `A`, status `mined`,
opened `2026-10-27` (not future), recheck `on-release` (symbolic cadence), used-by path present.

### 4.4 Pure addition, zero deletions

```
$ diff base mirror                                          deleted / added
corpus/README.md      0 / 30      (29 deliverable lines + 1 separator newline)
PROVINCE.md           0 / 3       (2 blanks + the F24 amendment line)
corpus/SOURCES.md     0 / 1       (the S063 row)
$ wc -l  mirror: README.md 573, PROVINCE.md 164, corpus/SOURCES.md 136
```

### 4.5 The F24 row parses on the harness's own regex

```
FRONTIER_ROW.match -> F24 | admitted | knowledge/rfc-9116-security-txt.md
cell split: 6 data cells, 7 pipes, 0 internal pipes; next cell 153 words, cites §2.5, §2.5.3, §2.5.5, §3, §5.5
```

Its three quoted spans are verbatim, exactly-once in the capture, and each ≤20 words:

```
"Unless otherwise stated, all fields MUST be considered optional."                       (9 w, L189)
"This field MUST always be present and MUST NOT appear more than once."                  (13 w, L273)
"It is RECOMMENDED that the value of this field be less than a year into the future to avoid staleness."  (20 w, L270-L272)
in_capture=True occ=1 for all three
```

## 5. Risks, dependencies and observations for the L1

1. **Landing order (E11).** `used-by corpus/knowledge/rfc-9116-security-txt.md` must exist when the census
   runs, so the S063 row and the entry land in the same step; a row-only landing fires `E11`.
2. **Three splice markers** remain in `registry-row.txt` only (§2 table above). The README and PROVINCE bytes
   are marker-free and need no edit; the sibling entry's `<<<CAPTURE>>>` / `<<<CAPTURE:Lnnn>>>` markers are
   the only other splice points in the C2 package.
3. **SOURCES.md line shift.** Inserting S063 after S062 shifts `## Paths` and everything below by one line.
   `corpus/lessons/*.md` cite `corpus/SOURCES.md:NN` in several places (r25, r28, r29, r31); round 40 did the
   same insertion for S060-S062 without re-basing them, so this is the established pattern, but it is a
   real number shift the L1 should be aware of. Nothing I deliver cites SOURCES.md by line.
4. **PROVINCE backticks.** I matched F22/F23 (no backticks around the entry path) rather than F18-F21
   (backticks), because the item names F23 as the byte-for-byte model. Adding the two backticks back is a
   two-character change if the L1 prefers the F18 form; the prefix is identical either way.
5. **Frozen base string is not a valid object name (affects C1, not C2).** The claims/prompt write the base
   as `5b29ea1439450b712581edf5f0bf98dfb262ab` — **38** hex characters. The real commit is
   `5b29ea1439450b712581edf5f0f0bf98dfb262ab` (**40**), and the 38-char string fails
   `git cat-file -t … → fatal: Not a valid object name`. The `counting_commands` in `claims.json` already use
   the 40-char form, but the `base` field and the seat briefs use the 38-char form, so any `--export-ref`
   or `git cat-file -e` negative control fed the short string will error rather than measure. Worth
   correcting before the C1 counters are graded.
6. **RFC 9116 is an Informational RFC** ("This document is not an Internet Standards Track specification; it
   is published for informational purposes", capture L25) and the kind cell is `spec` per the frozen claim.
   The row never claims Standards-Track status; every normative word quoted is the RFC's own.

## 6. Report path

`.ufo/waves/round-41/wave1/ExecC2Rows.md` (this file). Deliverables beside it:
`ExecC2Rows.registry-row.txt`, `ExecC2Rows.readme-row.txt`, `ExecC2Rows.province-amendment.txt`.
