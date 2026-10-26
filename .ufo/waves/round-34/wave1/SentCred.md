# SentCred — round-34 credential/secret scan

Seat: SentCred (sentinel leaf; no subagents, no wave dispatch). Lane root
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Lane base
`014ee2d7aa8c3c095ff57ae51097606a9906228c`; claims freeze
`29f606dbdd28aff6fd4573ab4b90788bbb90af13`.

**Scan of record:** 2026-10-26T05:44Z, 90 lane artifacts (every new/modified path vs the lane
base plus every untracked file), 90/90 present, 0 missing. Full path→sha256 list in
`wave1/SentCred/artifacts.sha256` (90 lines, sha256 `0d745ac0c5900012f7fa8b291f1276483af80bb7d23b10a4c37c8e33ee2b8e47`).

**Verdict: CLEAN.** No credential value, session/cookie/auth value, private URL, secret-manager
reference, e-mail address, phone number, SSH/PGP key, wallet secret, or `.netrc`-style material in
any scanned artifact. Blocking classes S1 (credential material) and S2 (session/cookie/auth values)
are both **0**.

**Flag (INFO — reported, not refused):** the Immunefi capture carries the page's public login/member
*labels* (`Log in`, `Join Immunefi`, footer `TOKEN`) and its cookie-consent dialog text. It carries
no login form, no member-area content, no cookie or session value, and no URL at all. Locations and
the refusal test in §4.

## Report

### 1. Artifact set

Enumerated from the lane root (exit 0):

```
$ { git diff --name-only 014ee2d7aa8c3c095ff57ae51097606a9906228c -- .; git ls-files --others --exclude-standard; } | sort -u | wc -l
90
```

Composition at enumeration: **27 modified tracked + 63 untracked = 90**; every file UTF-8 text
(0 files containing a NUL byte). In scope:

- captures: `corpus/source-snapshots/round-34/S051.txt` (the Immunefi VSCS v2.2 capture);
- manifests: `corpus/source-snapshots/round-34/manifest.json`, the rewritten `round-26` and
  `round-32` manifests;
- the F17 entry `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`;
- instruments/suite: new `corpus/instruments/kill-rule-check.py`,
  `corpus/instruments/r-defect-closure.sh`; modified `capture-binding-check.py`,
  `frontier-recheck-count.py`, `corpus/instruments/README.md`;
- the whole `.ufo/waves/round-34/` tree (claims, erratum 1, `c1-controls/`, `c2-controls/`,
  `assimilation/`, spec/dispatch/plan, `wave1/` receipts and attachments present at the scan
  instant);
- documents: `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`,
  `corpus/lessons/round-29.md`, `corpus/lessons/round-33.md`, `selftest-baseline.txt`;
- one peer edit outside `round-34/`: `.ufo/waves/round-33/wave1/ScribeReportDraft.md`
  (appended late-state block, `+37 −0`).

The scanner excludes its own receipt and attachment directory (`SELF_TREE` / `SELF_RECEIPT` in
`credscan.py`, declared in its docstring) because this receipt quotes the pattern tokens it
searches for. Including them, the lane's round-34 artifact tree at this instant is 94 files
(90 scanned + 3 attachments + this receipt). Declared, not hidden.

### 2. Method and commands

The scanner is stdlib-only, read-only, never opens a socket, and audits the bytes at their lane
paths; it does not follow symlinks or run repository code. Pattern classes:

| class | what it matches | blocking |
|---|---|---|
| S1 | cloud/API key formats (`sk_live_`/`sk_test_`/`ghp_`/`github_pat_`/`AKIA…`/`xox…`/`AGE-SECRET-KEY-`), JWT, PEM/SSH/PGP private keys, HTTP basic-auth blobs, secret-manager refs with a path, connection strings carrying a password | yes |
| S2 | `Authorization:`/`Cookie:`/`Set-Cookie`/`X-Api-Key` header lines, bearer values, session/csrf id assignments, `password=` / `api_key=` assignments | yes |
| S3 | e-mail addresses, URLs with query strings, non-public hosts (`localhost`, RFC1918, `.internal`, `intranet`) | triage |
| S4 | login/member markers, credential *words*, bare secret-manager scheme words, HTTP header/status lines, 64-hex tokens | triage |

Commands and exit codes (all from the lane root unless noted):

```
$ python3 .ufo/waves/round-34/wave1/SentCred/credscan.py
artifacts=90 hits=82 hex_tokens=459 blocking=0
  S3/URL with query string=5
  S4/credential word=54
  S4/http header/status line=3
  S4/login/member marker=14
  S4/secret-manager scheme word (no path)=6
exit=0

$ sha256sum .ufo/waves/round-34/wave1/SentCred/{artifacts.sha256,scan-hits.txt,credscan.py}
0d745ac0c5900012f7fa8b291f1276483af80bb7d23b10a4c37c8e33ee2b8e47  .ufo/waves/round-34/wave1/SentCred/artifacts.sha256
6d1a13b6d2d7246548d174c604b5b4623d4b820180ccc39cda64d96718a4f95c  .ufo/waves/round-34/wave1/SentCred/scan-hits.txt
99f1f79edb0fa2c6975fb5a9e3d16ff9bd34e35b2fb073bc7a333ed6cc644032  .ufo/waves/round-34/wave1/SentCred/credscan.py

$ grep -nEi 'secret|token|api[_-]?key|passw|auth|cookie|bearer|credential' \
    corpus/instruments/kill-rule-check.py corpus/instruments/r-defect-closure.sh \
    corpus/instruments/capture-binding-check.py corpus/instruments/frontier-recheck-count.py
# 24 hits, all the words `token`/`credentialed` in docstrings about `https://` URL tokens and
# "a source left credentialed by a bare prose mention"; no value. exit=0

$ grep -nE 'urllib|http\.client|socket|requests\.|curl |wget ' \
    corpus/instruments/{kill-rule-check.py,r-defect-closure.sh,capture-binding-check.py,frontier-recheck-count.py}
# no output, exit=1 — none of the four opens a network connection

$ grep -nE 'User-Agent|Request\(|urlopen|Cookie|Authorization' corpus/instruments/capture-source.py
74:    request = urllib.request.Request(url, headers={"User-Agent": UA})
75:    with urllib.request.urlopen(request, timeout=60) as response:
# exit=0 — the only producer sends User-Agent, no Cookie/Authorization
```

`scan-hits.txt` lists every non-hex hit with `path:line [class] match`; `artifacts.sha256` fixes
the bytes scanned.

### 3. Triage of every non-zero class

| class | n | verdict and locations |
|---|---|---|
| S1 credential material | **0** | none |
| S2 session/cookie/auth value | **0** | none |
| S3 URL with query string | 5 | 2 are **pre-existing** public rows in `corpus/SOURCES.md` (`:26` S020 justice.gov `…/dl?inline=`, `:33` S027 HN `…?id=38389728`); the round-34 diff adds only lines 54/74/98+, so neither is new content. 3 are public standards-portal register URLs quoted in `wave1/ScoutQuarantine.md:50,52,55` (`?hcno=…`, `?id=…`, `?path=…` are document identifiers). No URL carries `user:pass@`, an API key parameter, or a session id. |
| S3 non-public host / e-mail | 0 | none |
| S3 phone (ad-hoc regex, not in the scanner) | 0 | the only phone-shaped matches in `wave1/` were commit date-time strings of the form `2026-10-26 02:29:48 -0300`, re-checked by eye; no dialable number |
| S4 credential word | 54 | prose, policy text, and pattern lists: the F17 entry `:113` ("no credential, session or private URL"), `QUALITY.md:19`, lesson errata, the capture's policy bullets, and the assignment prompt text in `build-spec.py`/`wave1-spec.json`/`wave1-dispatch.json`/`wave1-plan.out`. No value. |
| S4 login/member marker | 14 | capture nav `S051.txt:2,23,39` and policy bullet `:145`; the same assignment prompt words in the four spec files; `MutSelftestSummary.md:262` is the substring `log in` inside "full log in the seat transcript"; `RevEntryF17.md:81` is prose about the entry's no-login instruction. |
| S4 HTTP header/status line | 3 | `RevErrata.md:66,100` and `ExecRDefectClosureSuite.md:14` are the **word** `Location:`/`location:` in prose ("Location: `corpus/QUALITY.md:169`", "derived from the script's own location"); no HTTP header. |
| S4 bare secret-manager scheme word | 6 | `build-spec.py:690`, `wave1-spec.json:641`, `wave1-dispatch.json:1067`, `wave1-plan.out:1072` (the assignment's own pattern list), `ScribeEntryF17.md:63` (a `grep` pattern). Each is a bare scheme token with **no path segment**, so none is a `op://`-style reference; the tightened S1 regex requires a path and returns 0. |

No artifact contains a `.netrc`, `id_rsa`/`id_ed25519`, `ssh-rsa AAAA…` key, PGP private key,
`file://` URL, `user:pass@` URL, or an env-style `*_KEY=*` / `*_TOKEN=*` assignment (targeted greps,
all exit 1 = no match; `_ENV` names `AWS_`, `GITHUB_TOKEN`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`,
`OP_SESSION`, `DATABASE_URL`, `SECRET_KEY` also zero).

### 4. The Immunefi capture — the mandated check

`corpus/source-snapshots/round-34/S051.txt`: 8502 B, 175 lines, sha256
`4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5` — equal to the manifest's
`sha256` and to the F17 entry's Scope section. Snapshot is 8502 B of converter text from a 219383 B
HTTP 200 response (`manifest.json` `purpose`).

Byte evidence that no header/attribute/session payload can be present (all counts 0):

```
$ for p in '<' '>' '@' '=' '{' '"' ';'; do grep -cF "$p" S051.txt; done
# each of the seven prints 0
$ grep -cE 'https?://' S051.txt      -> 0
$ grep -nE '[0-9]{6,}' S051.txt      -> no match, exit=1
```

Every credential-lexicon line in the capture, with its class:

| line | text (verbatim) | class |
|---|---|---|
| 2 | `Log in` | public nav link label |
| 26, 42 | `Token` | nav menu label (the IMU token) |
| 44 | `Explore BountiesLog in` | public nav link labels |
| 80 | `- Unauthorized minting of NFTs` | smart-contract policy bullet |
| 82 | `… (e.g. token URI, payload, artistic content)` | policy bullet |
| 90 | `3. Medium- Smart contract unable to operate due to lack of token funds` | policy bullet |
| 102 | `- database passwords` | impact **example**, no value |
| 103 | `- blockchain keys` | impact **example**, no value |
| 107 | `- Taking state-modifying authenticated actions …` | policy bullet |
| 114, 116, 126, 132, 133, 140 | `… wallet …` / `… wallet interaction …` | policy bullets |
| 127 | `- Email or password of the victim, etc.` | impact **example**, no value |
| 145 | `- Locking up the victim from login` | policy bullet |
| 146 | `- Cookie bombing, etc.` | policy bullet |
| 148 | `- Missing HTTP Headers without demonstrated impact` | policy bullet |
| 160 | `TOKEN` | footer nav heading |
| 165 | `Terms of UsePrivacyCookie PolicyEmployee VerificationCookie preferences` | footer legal labels |
| 167 | `Cookies on Immunefi` | consent-dialog heading |
| 168 | `Immunefi uses cookies to enable essential site functionality …` | consent copy |
| 169 | `Manage preferencesStrictly necessary …` | consent copy |
| 173 | `Session recordingRecords how you move through a page …` | consent category copy |

**Refusal test.** A refusal is required for a login *prompt* or session-bearing content. The capture
has neither: `Log in`/`Join Immunefi` are anchor labels rendered as text (no form, no input, no
credential field), there is no member-area or account content (0 `@`, 0 `=`), and the
`session`/`cookie` strings are either the consent dialog's category copy (L165-173) or the policy
bullet `Cookie bombing` (L146) — descriptions, not identifiers. The
capture therefore **passes**; the chrome above is flagged here so the L1 can record it.

**Provenance hygiene.** The capture was produced by the pre-existing
`corpus/instruments/capture-source.py` (sha256
`e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18`), whose only request header is
`User-Agent: kasegi-shokunin/1.0` (`:74`); it constructs no `Cookie` or `Authorization` header, so no
session material could be attached to the fetch even if the host had one. The committed snapshot is
the post-conversion text, so response headers never reach the repository.

### 5. F17 entry and manifest

- `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` (113 lines, 11143 B, sha256
  `948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a`): exactly one URL, the public
  page URL in the `source:` trailer; the `recheck:` line is a local absolute path, not a secret.
  Its Q6 sentence ("the capture carries no credential, session or private URL") is **independently
  confirmed** by §4. No quoted capture line contains credential material.
- `corpus/source-snapshots/round-34/manifest.json` (7654 B, sha256
  `d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe`): fields are
  `id`/`path`/`sha256`/`url`/`fetched_utc` plus 18 quote records
  (`id`/`quote`/`anchor`/`location`). No header, cookie, token, or query parameter; the URL is the
  public page. `fetched_utc` is a strict-UTC instant.

### 6. Instruments and suite

- No network code in `kill-rule-check.py`, `r-defect-closure.sh`, `capture-binding-check.py`,
  `frontier-recheck-count.py` (§2 grep exit 1).
- `kill-rule-check.py` copies the environment at `:352` only to override `TMPDIR`/`HYAKU_SCRATCH`
  (`:319`) for its scratch tree, passes it to its own subprocesses (`:329`), and never prints it;
  no error path dumps `os.environ`. `r-defect-closure.sh` has no `set -x` and no `printenv`.
- No embedded key/token/fixture secret: fixtures use synthetic `example.invalid` URLs
  (`capture-binding-check.py`, `kill-rule-check.py`) and `example.com`
  (`assimilation/scratch-registry.md`).
- Bytes scanned (these two were still being edited by peers during the wave; digests are the
  scanned bytes, not a claim about the final commit): `kill-rule-check.py`
  `096dfb9060829554305b1003494c1248d22e038234d791014a394ca45f602d61`; `r-defect-closure.sh`
  `0beafed2c2ead41e66b8248893448954a3ddadd7dade7451579f49a480d460d1`;
  `capture-binding-check.py` `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa`;
  `frontier-recheck-count.py` `8a79010d557dc9b24c6cd763bc6d2b5f8c3febe0fafde408a8c752107f57499c`.

### 7. Documents, receipts, specs, controls

Whole-file scans of `SCORECARD.md`, `QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, the two
lesson files, the three manifests, `corpus/instruments/README.md`, `selftest-baseline.txt`, the
round-34 spec/dispatch/plan/claims/errata/controls, and every `wave1/` receipt present at the scan
instant. Zero credential material; the only external URLs are the public research sources already in
the registry, Immunefi, the `samr.gov.cn` standards pages, and synthetic `*.invalid` / `example.com` fixtures.

INFO (data hygiene, not a credential finding): receipts carry **local absolute paths**
(`/home/vgpnk/Projects/shokunin/…`, `/fast/scratch/hyaku/kasegi-r34/<seat>/…`) and therefore the host
username; the lane's documents and receipts have used these paths since earlier rounds. No e-mail,
phone, postal address, personal name, wallet address, or account identifier appears in any artifact.

### 8. The 64-hex class

459 occurrences of a 64-hex token. Every one is a declared SHA-256/commit digest: adjacent to a
`sha256`/`digest`/`pin=` label, followed by a file path in a `sha256sum` block, or inside a
checksum table. A ±1-line window triage leaves 24 that are still digest-table rows
(`corpus/instruments/README.md:596-604` per-round digests, `ScoutQuarantine.md:229-237` fetch
checksums, mutation receipts' patched-file digests, `QUALITY.md:113` `pin=`). Zero are key-shaped or
unlabelled. This class is a false-positive source in a repo that pins everything by digest, not a
finding.

### 9. Limits (recorded, not hidden)

- **Point in time.** The wave was live: a peer receipt landed seconds before the scan, and both new
  instruments changed between my first pass (05:37Z) and the scan of record (05:44Z). Artifacts
  written after 05:44Z are not covered by this receipt; re-run §11 at integration.
- **Liveness re-run (2026-10-26T05:46Z), after this receipt was written:** `credscan.py` enumerated
  **102** artifacts — the 12 new ones are wave-1 receipts that landed in the preceding two minutes —
  and printed `hits=85 hex_tokens=592 blocking=0`, **exit 0**. All 12 late receipts were therefore
  scanned and are clean; they are not individually digested in §12 (their digests still churn), and
  the 90-file `artifacts.sha256` remains the pinned set of record.
- The scanner detects value *shapes* and lexicon hits. It cannot prove the absence of a
  hand-typed low-entropy secret; the capture check in §4 is stronger because the committed bytes are
  converter text with zero markup, `=`, `@`, or URL residue.
- Scope is the lane's new artifacts. Uncommitted scratch captures made by the scout seats (v2.3,
  index page) never entered the lane and are not artifacts; the receipts quote their digests only.
- The scanner's own receipt/attachments are excluded from its run (declared in §1); they contain the
  search-lexicon words by construction.

### 10. Scratch

`/fast/scratch/hyaku/kasegi-r34/SentCred/` held the scanner source and JSON reports (10 entries).
Deleted after the attachments were copied into the wave directory:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r34/SentCred ; ls -d /fast/scratch/hyaku/kasegi-r34/SentCred
ls: cannot access '/fast/scratch/hyaku/kasegi-r34/SentCred': No such file or directory   (exit 2)
```

No scratch tree survives this seat.

### 11. Re-run (for the L1 at integration)

From the lane root; exit 0 = clean, 1 = an S1/S2 hit, 2 = enumeration failure. The scanner
re-enumerates the base diff plus untracked files itself, so it covers receipts that land later:

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 .ufo/waves/round-34/wave1/SentCred/credscan.py                 # prints artifacts=… blocking=…
python3 .ufo/waves/round-34/wave1/SentCred/credscan.py --json /tmp/sentcred.json
```

`--base <commit>`, `--root <lane>`, and `--list <file>` (audit a frozen list instead of git
enumeration) are optional.

### 12. Key digests (at the scan instant)

| artifact | bytes | sha256 |
|---|---|---|
| `corpus/source-snapshots/round-34/S051.txt` | 8502 | `4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5` |
| `corpus/source-snapshots/round-34/manifest.json` | 7654 | `d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe` |
| `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` | 11143 | `948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a` |
| `corpus/instruments/kill-rule-check.py` | — | `096dfb9060829554305b1003494c1248d22e038234d791014a394ca45f602d61` |
| `corpus/instruments/r-defect-closure.sh` | — | `0beafed2c2ead41e66b8248893448954a3ddadd7dade7451579f49a480d460d1` |
| `corpus/instruments/capture-binding-check.py` | — | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` |
| `corpus/instruments/frontier-recheck-count.py` | — | `8a79010d557dc9b24c6cd763bc6d2b5f8c3febe0fafde408a8c752107f57499c` |
| `corpus/instruments/README.md` | — | `5418905d7d57510168d151d46b8991a515e894dc20b131549cf6576acc755abb` |
| `SCORECARD.md` | — | `b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0` |
| `corpus/QUALITY.md` | — | `77d99df9abf57a66065dbe927ce95f0ddf8acbfba237fefd163bdd3871751af8` |
| `corpus/README.md` | — | `876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29` |
| `corpus/SOURCES.md` | — | `4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6` |
| `corpus/SOURCES.md` pre-append (`014ee2d`) | 100 ln | `b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b` |
| `corpus/lessons/round-29.md` | — | `4afb96be18355cd958f9ddccc4f9687c2c2afa4b2747d49f687add956484ecce` |
| `corpus/lessons/round-33.md` | — | `f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807` |
| `corpus/source-snapshots/round-26/manifest.json` | — | `33ac33c3caa6d43f3772b8cf8532b37cdb50f48db8ba667b5dd90645e8eacefa` |
| `corpus/source-snapshots/round-32/manifest.json` | — | `72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6` |
| `selftest-baseline.txt` | 1552 | `ca3759d1c4a047ec1a27f4d6bc8b64df4d6e21a29b74ef9904ccbe91be3a3a51` |
| `corpus/instruments/capture-source.py` (pre-existing, provenance) | — | `e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18` |

All 90 scanned paths and digests: `wave1/SentCred/artifacts.sha256`.

### 13. Tooling

No tool was installed or upgraded for this seat. Python 3 (system stdlib) only; no network calls
made by the scanner. No pacman/uv/npx transaction.
