# Hash / encoding / path check — falsify report

Seat: `L1Kasegi23.HashCheck-2` (leaf, read-only). Target: `corpus/source-snapshots/round-23/{manifest.json,S018.txt,S029.txt,S030.txt}`
as read by `corpus/instruments/source-recheck.py`. Every number below was produced in this session from bytes on disk;
mutation was confined to `/tmp/kasegi-r23-falsify-hashcheck/`. No production file, lane tree, git/jj index or state was touched.
Only write: this report.

All relative paths are relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## Verdict

| # | Claim attacked | Result |
|---|---|---|
| H1 | Manifest `sha256` equals the real bytes of each `path` | **holds 3/3** |
| H2 | Manifest `path` values are relative | **holds 3/3** (bare filenames, no separator at all) |
| H3 | Those paths resolve inside the snapshot directory | **holds 3/3**, and the guard rejects escapes it is supposed to reject |
| H4 | Each snapshot is plain decodable UTF-8 text | **holds 3/3** (strict decode, no BOM, no NUL, no CR, no C0/Cf control chars, NFC-stable) |
| H5 | "digest mismatch or missing quote fails closed" | **holds** — exit 1 for both; exit 2 for unreadable/invalid/outside |
| V1 | `S029` assertion `art14-2a-early-warning` pins *Article 14(2)(a)* | **falsified as a discriminating test** — an Article 14(3)–(4)-only excerpt with no vulnerability duty passes it with exit 0 |

Digest, encoding and path conformance all hold. The one defect I can execute is assertion *specificity* (V1), not the pins.

## Axis A — digests

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-23 && sha256sum *.txt
d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4  S018.txt
82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c  S029.txt
673526db7c2b4fde2a9682c6a2b8fca3ebb0ff9d4423c0559483f4540c5ab019  S030.txt
```

Identical digests from an independent implementation (`hashlib.sha256`) over a `cp -a` copy in scratch, so the result does
not depend on the `sha256sum` binary:

```
S018 MATCH bytes=8372  stated=d366bf409e7ce9e3... actual=d366bf409e7ce9e3...
S029 MATCH bytes=19900 stated=82514478b6c5fb8f... actual=82514478b6c5fb8f...
S030 MATCH bytes=26660 stated=673526db7c2b4fde... actual=673526db7c2b4fde...
```

Manifest field hygiene (`manifest.json:8,21,34`): `len=64 lowercase_hex=True` for all three; `schema_version = 1` (`int`),
three sources, **no** orphan `*.txt` in the directory (`dir .txt files: ['S018.txt','S029.txt','S030.txt']`), so the manifest
covers exactly the files present.

Provenance agreement — byte counts *and* digests in `.ufo/waves/round-23/opened-source-snapshots.json` match the files:

```
S018: bytes_claim=8372  bytes_actual=8372  sha_match=True path_inside_round23=True
S030: bytes_claim=26660 bytes_actual=26660 sha_match=True path_inside_round23=True
S029: bytes_claim=19900 bytes_actual=19900 sha_match=True path_inside_round23=True
```

And the working tree is not a private variant — the blobs in `HEAD` hash to the same values:

```
$ GIT_OPTIONAL_LOCKS=0 git cat-file -p HEAD:corpus/source-snapshots/round-23/S018.txt | sha256sum
d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4
# same for S029 (82514478…), S030 (673526db…), manifest.json (b8a20607e03743f6782093167b39d65edbf5c742a987488065a54eff79f4a2da)
$ GIT_OPTIONAL_LOCKS=0 git status --porcelain=v1 -- corpus/source-snapshots/round-23/
   (no output — clean against the index)
```

Teeth: a manifest with `sha256 = "0"*64` over the real file yields `S018:sha256 MISMATCH expected=000… actual=d366…`, exit 1.
The pin is live, not decorative.

## Axis B — encoding and shape

Strict `decode("utf-8")` succeeded for all three; per-file facts (bytes / decoded chars / lines):

| file | bytes | chars | non-ASCII chars | BOM | `\r` | NUL | C0/Cf (excl. `\n`,`\t`) | NFC-stable | tab | max line | begins with | ends with `\n` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S018.txt | 8372 | 8364 | 4× (`’` `“` `”`) | no | 0 | 0 | none | yes | 0 | 424 | `## Definitions` | yes |
| S029.txt | 19900 | 19900 | 0 (pure ASCII) | no | 0 | 0 | none | yes | 0 | 1000 | *(empty line — first byte `0x0a`)* | **no** (last char `o`) |
| S030.txt | 26660 | 26622 | 19× (`’` `“` `”` `…`) | no | 0 | 0 | none | yes | 0 | 813 | `URL: https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.0.pdf` | yes |

First bytes as hex: `232320446566696e` (S018, `## Defin`), `0a41727469636c65` (S029, `\nArticle`), `55524c3a20687474` (S030, `URL: htt`).
`file(1)` labels them "Nim source code" / "ASCII text" / "exported SGML document" — heuristics on content, all three also
report as text; S029 being pure ASCII is a valid UTF-8 subset, not an encoding outlier. `stat` reports `links=1` and mode
`-rw-r--r--` for all three, i.e. no hardlink indirection.

Teeth: a `b'\xff\xfe\x00bad'` file with a *correct* digest yields `S018:source UNAVAILABLE reason=not-utf8`, exit 2 — the
UTF-8 gate is real, and it is applied after the digest gate (so a re-encoded snapshot cannot both hash-match and decode).

Two shape observations, no defect: S029 has no trailing newline and opens with a blank line. Neither affects the pin or any
quote; recorded because "plain text file" was the claim under probe.

## Axis C — path containment (positive and negative)

Every manifest path is a bare filename — not merely relative:

```
S018: path='S018.txt' isabs=False has_sep=False has_dotdot=False resolved=S018.txt inside=True sha_len=64 quotes=6
S029: path='S029.txt' isabs=False has_sep=False has_dotdot=False resolved=S029.txt inside=True sha_len=64 quotes=6
S030: path='S030.txt' isabs=False has_sep=False has_dotdot=False resolved=S030.txt inside=True sha_len=64 quotes=7
```

The guard (`source-recheck.py:99-104`: `base.resolve(strict=True)`, `(base/path).resolve(strict=True)`,
`commonpath(...) != str(base)`) is exercised against hostile manifests built in scratch, each carrying the *correct* digest so
that only the path logic can decide the outcome:

| probe | manifest `path` | exit | output |
|---|---|---|---|
| relative-ok | `S018.txt` | 0 | `S018:sha256 OK` / `S018:q OK` |
| dot-slash | `./S018.txt` | 0 | `S018:sha256 OK` (resolves inside; legitimate) |
| dotdot-but-inside | `../round-23/S018.txt` | 0 | `S018:sha256 OK` (resolves inside; legitimate) |
| absolute | `/tmp/…/round-23/S018.txt` | 2 | `S018:manifest UNAVAILABLE reason=invalid-path` |
| sibling-prefix escape | `../round-23-evil/S018.txt` | 2 | `S018:source UNAVAILABLE reason=outside-manifest-directory` |
| symlink to `/etc/hostname`, digest matches target | `link.txt` | 2 | `S018:source UNAVAILABLE reason=outside-manifest-directory` |
| manifest relocated outside the snapshot dir, relative path to an existing outside file | `../specificity/incident-only.txt` | 2 | `S018:source UNAVAILABLE reason=outside-manifest-directory` |
| nested missing | `nope/S018.txt` | 2 | `S018:source UNAVAILABLE reason=missing` |

The `round-23-evil` row is the one that matters: sibling-prefix directories, the classic `startswith` bug, are rejected —
`commonpath` is used instead of a string prefix, so the containment claim is not a substring artefact. The symlink row shows
the check is on the **resolved** path, so a confined-looking name cannot smuggle outside bytes; the digest pin is a second,
independent gate on that same vector. The relocation row shows containment is manifest-directory-relative, which is why the
manifest must live in the snapshot directory — it does.

Also confirmed: manifest resolved through a directory symlink still passes (`S018/S029/S030:sha256 OK`), and the tool is CWD
independent (`cwd=/tmp`, absolute manifest → exit 0, 22 lines). Selection filter fails closed: `--source NOPE` →
`NOPE:source UNAVAILABLE reason=not-listed` exit 2; `--source 'bad id'` → `manifest:selection UNAVAILABLE reason=invalid-source-id` exit 2.

## V1 — falsifiable defect: one quote assertion does not discriminate the duty it is named for

`manifest.json` S029 assertion `art14-2a-early-warning` quotes only
`within 24 hours of the manufacturer becoming aware of it` (56 chars). That string occurs **twice** in the pinned bytes:

```
occurrence 1, line 10: "2.For the purposes of the notification referred to in paragraph 1 … (a)an early warning notification
   of an actively exploited vulnerability … within 24 hours of the manufacturer becoming aware of it"   [Art 14(2)(a)]
occurrence 2, line 20: "4.For the purposes of the notification referred to in paragraph 3 … (a)an early warning notification
   of a severe incident … within 24 hours of the manufacturer becoming aware of it"                        [Art 14(4)(a)]
```

Because the discriminating words (`actively exploited vulnerability` vs `severe incident`) sit *outside* the quoted span,
the assertion cannot tell the vulnerability clock from the incident clock. I executed the consequence instead of arguing it:
I built `/tmp/kasegi-r23-falsify-hashcheck/specificity/incident-only.txt` = `S029.txt` sliced from `3.A manufacturer shall
notify any severe incident` to `5.For the purposes of paragraph 3` (1945 bytes, Article 14(3)–(4) only), gave it its **true**
digest, and ran the instrument:

```
incident_only bytes: 1945 contains 'actively exploited vulnerability': False
contains quote text: True
recheck on INCIDENT-ONLY excerpt (no vulnerability duty present): exit=0 out=S029:sha256 OK
S029:art14-2a-early-warning OK
```

Exit 0 on a document that contains **no** Article 14(2)(a) and no notion of an actively exploited vulnerability at all. So
`art14-2a-early-warning` is satisfied by 14(4)(a); as a witness for the F07 vulnerability-reporting duty it is non-unique
and, on its own, unfalsifiable in the direction that matters. Remediation is one string change and stays inside the
instrument's substring semantics: extend the quote to `an early warning notification of an actively exploited vulnerability,
without undue delay and in any event within 24 hours of the manufacturer becoming aware of it` (unique: 1 occurrence), or at
minimum include `actively exploited vulnerability` in the span. All other 18 assertions are single-occurrence in their own
snapshot (`count_in_own=1`) and appear in no other snapshot, so this is a one-row defect, not a systemic one.

Overlap disclosure: `.ufo/waves/round-23/falsify/S029Quotes.md` finding 4 already recorded the two-occurrence collision and
classified it as an ambiguity note, not a defect. My delta is the executed false-negative above (exit 0 on an excerpt without
the duty) plus the concrete replacement string; I am not claiming that occurrence count as a new discovery.

Severity: does not touch H1–H5. It narrows C2's verifiability surface: a quote set can pass on bytes that lack the duty the
quote id names, so quote-presence "OK" is not by itself proof that the claimed duty is in the capture.

## Observations that are not defects

- **Pin scope.** `opened-source-snapshots.json` records `"kind": "normalized public-doc reader excerpt; not raw HTTP bytes"`
  for all three, and the manifest's own `purpose` says it "verifies captured bytes, not current upstream freshness". The
  digests therefore attest internal consistency and tamper-evidence only; they do not and are not claimed to establish
  upstream authenticity. No misrepresentation found, but any downstream text implying upstream verification would overreach.
- **mtime inversion.** `manifest.json` mtime `2026-10-25 03:30:24` is five days *later* than the three `*.txt` mtimes
  (`2026-10-20 18:38:49`), which is the usual shape of a post-hoc edit. It is not tampering here: the manifest's working-tree
  SHA-256 equals its `HEAD` blob (`b8a20607…`) and the pinned digests equal `HEAD` blob digests, so the later mtime is a
  checkout/touch artefact.
- **`sha256sum` version string.** `/usr/bin/sha256sum --version` prints `sha256sum 0.8.0` while `pacman -Qo` attributes the
  file to `coreutils 9.12-2` and the binary carries GNU coreutils strings. Not an artifact risk: the hashes were reproduced
  by `hashlib.sha256` and by git's own SHA-256 path, which agree byte for byte. Flagged only because a verifier that trusts
  the version banner would be misled about the tool, not about these digests.
- **Regex-scan false positives.** A repo-wide scan for `source-snapshots/round-23/…` references reported `S029.txt.`,
  `S030.txt.`, `manifest.json.` and `S0xx.txt` as non-existent; all four are prose/regex artefacts (sentence periods,
  template placeholders in `.ufo/waves/round-23/build/{Causal,RedBefore}.md`, `considerthese/2026-10-21.md:63`). No dangling
  snapshot path claim exists.

## Scope limits

- I verified captured bytes, decodability, path containment and fail-closed behaviour. I did not grade quote coverage or
  F06–F08 admission (other seats), did not fetch upstream documents (no network), and did not attack `resolve.py`'s
  `bounty_suffix`/`under_mirror` C1 code (assigned to the mutation seats).
- Absence reasoning in the excerpt proves nothing about the rest of the source: S029 is an Article 14–17 + 71 capture, S018
  an excerpt with no title/URL/version, S030 a rules v4.2.0 excerpt.
- No score or admission claim is made. No installs were required (pacman host-wide pause respected; nothing installed or
  upgraded), and scratch use was limited to `/tmp/kasegi-r23-falsify-hashcheck/`.
