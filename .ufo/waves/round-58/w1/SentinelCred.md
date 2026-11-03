FINDINGS — round-58 credential/safety/scope scan: CLEAN on credential material (0 credential values; the 14 substantive-named-pattern hits are pattern *names* in prose/prompt text, not values; 0 op:// references in the round's 23 implementation bytes; 0 private/session URLs across the round's 31 swept files); 1 medium safety finding (the figure-audit read-only derive gate is bypassable, so the round's "read-only derive gate" framing overstates the guarantee) and 2 low provenance findings (the manifest `bytes` field records the snapshot size under a field name that earlier rounds used for the fetched size, and no round-58 capture receipt records the fetch itself).

# SentinelCred — kasegi round 58, wave 1

Seat: credential, safety and scope scan of the round's new bytes.
Lane (read-only): `/home/vgpnk/Projects/shokunin/kasegi-shokunin` at `18ddb054a82a59e530ba86b2511bcfa5ecd49b6b` (implementation under test); freeze commit `543cac13886b91ac660d788ed20e64ae70ee0fa5`; base `1e5c8f2cdc1c9d14672444c6fca0e67414366494`.
Scratch: `/fast/scratch/hyaku/kasegi-r58/SentinelCred` (created with `mkdir -p`; every probe, clone-equivalent copy and temp file lives there; deleted before yield — see §9).
Tools: no tool was installed or upgraded. The scan used only the pre-installed `python3` (3.14.8, the host interpreter the lane's own `capture-source.py` docstring and the claims' `host` field name) plus coreutils `grep`/`find`/`diff`/`sha256sum`. No `pacman`, `uv tool`, `npm`, `cargo` or `~/.local/bin` write was performed, so there is no tool/version/channel/reason row to record.

---

## 1. Scope of the scan — which bytes were scanned, and how the file set was derived

The seat named six targets plus the builders directory. To avoid missing round bytes I swept the union of (a) the named targets, (b) every file under `.ufo/waves/round-58/controls/builders/`, (c) every file the round changed between base and implementation, and (d) the round's untracked-but-present artifacts.

Command and output:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git diff --name-only \
    1e5c8f2cdc1c9d14672444c6fca0e67414366494 18ddb054a82a59e530ba86b2511bcfa5ecd49b6b
.ufo/waves/round-54/controls/red-d53-ledger.json
.ufo/waves/round-58/claims.json
.ufo/waves/round-58/controls/builders/build-manifest.py
.ufo/waves/round-58/controls/builders/make-impl.py
.ufo/waves/round-58/controls/builders/run-a.sh
.ufo/waves/round-58/controls/builders/run-after.sh
.ufo/waves/round-58/controls/builders/run-c1-mutants.sh
.ufo/waves/round-58/controls/builders/run-do-nothing.sh
.ufo/waves/round-58/controls/do-nothing-c1-mutants-r58.txt
.ufo/waves/round-58/controls/do-nothing-c1-r58.txt
.ufo/waves/round-58/controls/do-nothing-c2-r58.txt
.ufo/waves/round-58/controls/do-nothing-r67-probe-a2-r58.txt
.ufo/waves/round-58/controls/neighbor-screen-r58.txt
.ufo/waves/round-58/controls/standin-after-r58.txt
PROVINCE.md
corpus/README.md
corpus/SOURCES.md
corpus/instruments/figure-audit-mutbat.py
corpus/instruments/figure-audit.py
corpus/instruments/knowledge-expected.txt
corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md
corpus/source-snapshots/round-58/S091.txt
corpus/source-snapshots/round-58/manifest.json
```
exit code 0. (23 files changed by the round.)

Adding the round's untracked-but-present artifacts (`corpus/lessons/round-58.md`, the four `.ufo/waves/round-58/w1*.json` wave-control files, `w1.ready`, `w1.ready.dispatched`, `w1/swarm-registry.json`, `controls/after-r58.txt`) gives **31 files swept**.

The scanner is `scan.py` (credential/URL/path/instruction classes), `entropy.py` (secret-shaped patterns + high-entropy triage), `triage.py` (masked triage + whole-round tree sweep), `kwclass.py` (keyword classification), `final.py` (untracked artifacts + provenance + instrument review) and `final_table.py` (the consolidated per-file table), all written to the scratch root and all run with `TMPDIR=/fast/scratch/hyaku/kasegi-r58/SentinelCred`.

## 2. Per-file scan result (pattern NAMES and COUNTS only — no matched value is printed anywhere in this file)

Command: `python3 final_table.py` (scratch), section "FINAL per-file scan table".
Columns: `cred` = hits by any credential-material pattern name; `subst` = hits by the *substantive-named* patterns (op-ref, bearer, auth-hdr, api-key, secret, password, private-key, aws/gcp/gh/gitlab/slack/openai/anthropic/hf keys, jwt, basic-auth-url, url-secret, kv-assignment, shell-export-secret, cookie-jar); `url` = private/localhost URL patterns; `home` = host-specific absolute home-directory path lines; `instr` = probe/scan/login/submit/exfil verb lines.

**How to read the `subst` column.** The `subst` total is **14**, not 0 — but **every one of those 14 hits is the occurrence of a pattern *name*** ("token", "secret", "api key", "password", "bearer", "authorization", "op://") inside a prose sentence or a prompt enumeration, and **none is a credential value**. The count of actual credential *values* in the round's bytes is **0**. The exact breakdown of the 14 (command: the per-pattern breakdown over the four files that carry them):

```
.ufo/waves/round-58/w1-plan.json      pattern=bearer    count=1  line=176
.ufo/waves/round-58/w1-plan.json      pattern=api-key   count=1  line=176
.ufo/waves/round-58/w1-plan.json      pattern=secret    count=1  line=176
.ufo/waves/round-58/w1-plan.json      pattern=password  count=1  line=176
.ufo/waves/round-58/w1-spec.json      pattern=bearer    count=1  line=45
.ufo/waves/round-58/w1-spec.json      pattern=api-key   count=1  line=45
.ufo/waves/round-58/w1-spec.json      pattern=secret    count=1  line=45
.ufo/waves/round-58/w1-spec.json      pattern=password  count=1  line=45
.ufo/waves/round-58/w1-dispatch.json  pattern=bearer    count=1  line=171
.ufo/waves/round-58/w1-dispatch.json  pattern=api-key   count=1  line=171
.ufo/waves/round-58/w1-dispatch.json  pattern=secret    count=1  line=171
.ufo/waves/round-58/w1-dispatch.json  pattern=password  count=1  line=171
corpus/README.md                      pattern=auth-hdr   count=1  line=335
corpus/README.md                      pattern=secret    count=1  line=610
TOTAL = 14
```
exit code 0. The twelve in the three wave-control JSONs are the seat prompt's own enumeration "credential material (token, secret, api key, password, cookie, session, bearer), op:// references, …" — the enumeration-context test classified all of them `enumeration/prose-context`. The two in `corpus/README.md` are prose (a sentence using "authorization" and a fixture *directory name* ending in "secret"), both on **pre-existing** lines that the round's diff (`@@ -948,0 +949,20 @@` only) does not touch.

```
file                                                           lines     cred      url     home    instr    subst
.ufo/waves/round-54/controls/red-d53-ledger.json                  20        0        0        0        0        0
.ufo/waves/round-58/claims.json                                   55        0        0        1        2        0
.ufo/waves/round-58/controls/after-r58.txt                       180        0        0        3        0        0
.ufo/waves/round-58/controls/builders/build-manifest.py           81        0        0        0        1        0
.ufo/waves/round-58/controls/builders/make-impl.py               238        0        0        1        0        0
.ufo/waves/round-58/controls/builders/run-a.sh                    83        0        0        2        4        0
.ufo/waves/round-58/controls/builders/run-after.sh                29        0        0        1        0        0
.ufo/waves/round-58/controls/builders/run-c1-mutants.sh           49        0        0        1        0        0
.ufo/waves/round-58/controls/builders/run-do-nothing.sh           38        0        0        1        7        0
.ufo/waves/round-58/controls/do-nothing-c1-mutants-r58.txt        43        0        0        3        0        0
.ufo/waves/round-58/controls/do-nothing-c1-r58.txt                29        0        0        5        0        0
.ufo/waves/round-58/controls/do-nothing-c2-r58.txt                35        0        0        0        0        0
.ufo/waves/round-58/controls/do-nothing-r67-probe-a2-r58.txt      15        0        0        0        5        0
.ufo/waves/round-58/controls/neighbor-screen-r58.txt              54        0        0        2        2        0
.ufo/waves/round-58/controls/standin-after-r58.txt               180        0        0        1        0        0
.ufo/waves/round-58/w1-dispatch.json                             187       25        0       10       21        4
.ufo/waves/round-58/w1-plan.json                                 189       25        0       10       21        4
.ufo/waves/round-58/w1-spec.json                                  58        9        0       10        7        4
.ufo/waves/round-58/w1.ready                                       1        0        0        1        0        0
.ufo/waves/round-58/w1.ready.dispatched                            2        0        0        0        0        0
.ufo/waves/round-58/w1/swarm-registry.json                       108        9        0        0        9        0
PROVINCE.md                                                      205        0        0        0        1        0
corpus/README.md                                                 968        2        0        3        2        2
corpus/SOURCES.md                                                215        1        0        7        5        0
corpus/instruments/figure-audit-mutbat.py                        101        0        0        0        0        0
corpus/instruments/figure-audit.py                               214        0        0        0        0        0
corpus/instruments/knowledge-expected.txt                         79        0        0        0        0        0
corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md 83        1        0        1        2        0
corpus/lessons/round-58.md                                        60        0        0        3        2        0
corpus/source-snapshots/round-58/S091.txt                         67        1        0        0        0        0
corpus/source-snapshots/round-58/manifest.json                    74        0        0        0        1        0
-----------------------------------------------------------------------------------------------------------------
TOTAL over 31 files                                                        73        0       66       92       14
```
exit code 0.

**Named-target rows, read out of that table:**

| named target | lines | cred | url | home | instr | subst |
|---|---|---|---|---|---|---|
| `corpus/source-snapshots/round-58/S091.txt` | 67 | 1 | 0 | 0 | 0 | 0 |
| `corpus/source-snapshots/round-58/manifest.json` | 74 | 0 | 0 | 0 | 1 | 0 |
| `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md` | 83 | 1 | 0 | 1 | 2 | 0 |
| `corpus/instruments/figure-audit.py` | 214 | 0 | 0 | 0 | 0 | 0 |
| `corpus/instruments/figure-audit-mutbat.py` | 101 | 0 | 0 | 0 | 0 | 0 |
| `.ufo/waves/round-58/claims.json` | 55 | 0 | 0 | 1 | 2 | 0 |
| builders (6 files, 518 lines total) | 518 | 0 | 0 | 6 | 12 | 0 |

### 2.1 Every non-zero `cred`/`instr` hit, with its class

Command: `python3 kwclass.py` and `python3 final_table.py` (detail blocks).

| path:line | pattern name | class | verdict |
|---|---|---|---|
| `corpus/source-snapshots/round-58/S091.txt:61` | cookie | site-cookie-banner | benign — the captured page's own cookie notice ("uses cookies essential for website functionality and anonymous usage analytics"), i.e. source prose |
| `corpus/source-snapshots/round-58/S091.txt:21,22,25,26,27,36,43` | token | llm-eval-token | benign — every hit is the article's "tokens per task" / "token cap" / "token budget" / "token spend" vocabulary (the classifier `LLM_TOK` matched all 7) |
| `corpus/source-snapshots/round-58/manifest.json:3,39` | token | llm-eval-token | benign — the manifest note and the Q3 pinned quote, both the "2.5M token cap" wording |
| `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:3` | token | llm-eval-token | benign — the provenance line's "token-cap statement L21 and L27" |
| `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:32,37,38,41` | token | llm-eval-token | benign — the token-cap claim text |
| `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:16` | credential | credential-denial-statement | benign — the sentence "carries no credential material" |
| `corpus/README.md:335` | auth-hdr | prose-only ("authorization" in an English sentence about CNVD 众测 intake) | benign, and **not round-58 bytes**: the round's README diff is `@@ -948,0 +949,20 @@` only, so line 335 is pre-existing |
| `corpus/README.md:610` | secret | a fixture *directory name* (`defect-9-secret`) in a pre-existing line | benign, pre-existing (not in the round's diff hunks) |
| `corpus/SOURCES.md:73` | cookie | a curl advisory's own wording ("cookie path comparison logic") | benign, pre-existing |
| `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:15` | probe/scan | the documentation-only sentence | benign — see §3 |
| `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:16` | login | the documentation-only sentence | benign — see §3 |
| `corpus/source-snapshots/round-58/manifest.json:14` | probe/scan | the word "probe" in `fetch_method` ("probe 20:35:32Z") | benign — a timestamp label for a capture re-open, not an instruction |
| `.ufo/waves/round-58/claims.json:7,51` | probe/scan | "capture probe" and "probe-a2" (the name of a committed control receipt) | benign |
| `.ufo/waves/round-58/controls/builders/build-manifest.py:61` | probe/scan | the word "probe" inside the `fetch_method` prose string | benign |
| `.ufo/waves/round-58/controls/builders/run-a.sh:41,66,68,71` and `run-do-nothing.sh:31-37`, `do-nothing-r67-probe-a2-r58.txt:1,4,5,9,10`, `neighbor-screen-r58.txt:41,44`, `claims.json:51` | probe/scan | the words "probe-a2" / "capture probe" naming the round's own control artifacts | benign |
| `.ufo/waves/round-58/w1-plan.json:4,49-186`, `w1-spec.json:3,10,25,30,45`, `w1-dispatch.json:35-181`, `w1/swarm-registry.json:17-105` | credential, api-key, secret, password, cookie, bearer, op-ref, login, submit, probe/scan | **the seat-prompt text itself** | benign by construction — these files contain *this seat's* instruction, which enumerates the pattern names. Verified: `w1-plan.json:176` and `w1-spec.json:45` both begin `"task": "/skill:godspeed\n\n# Target\nCredential, safety and scope scan…`, and the only `op://` strings in the lane's round-58 tree are inside that prompt's own sentence "no secrets, tokens, cookies, session values or op:// references" |

The `subst` column's 14 hits are broken out in the "How to read the `subst` column" note above: twelve are this seat's own prompt enumeration in the three wave-control JSONs and two are pre-existing prose in `corpus/README.md`. **No file of the round contains a credential value** — no issued token, key, password, cookie, session value or bearer string. Independently corroborated by `entropy.py` §A, which ran 26 secret-shaped patterns (aws/gcp/github/gitlab/slack/openai/anthropic/huggingface keys, PEM blocks, JWTs, basic-auth URLs, url-embedded secrets, key=value assignments, shell secret exports) over all 23 changed files and printed `TOTAL secret-shaped hits over round-58 new bytes = 0`, and by `final.py` §O, which ran the same 16-pattern set over the 8 untracked round artifacts and printed `TOTAL secret-shaped hits in untracked round-58 artifacts = 0`.

### 2.2 The specific classes the seat named, counted

Command: `python3 final_table.py` (§ op:// check, § url check) and `python3 entropy.py` (§A, 26 secret-shaped patterns).

- **op:// references**: **0** in the round's 23 implementation bytes (verified by `grep -c 'op://'` over each of the 23 files: `TOTAL = 0`). Across the full 31-file sweep the literal `op://` count is **6**, all in the three wave-control JSONs (2 each in `w1-plan.json`, `w1-spec.json`, `w1-dispatch.json`) and all inside this seat's own prompt sentence "no secrets, tokens, cookies, session values or op:// references" (§2.1). The strict `op://<value>` pattern matched 0 anywhere, because no `op://` is followed by a value. The lane does contain `op://` in 30 older directories (rounds 21-57), none of them round-58 bytes.
- **Private / session URLs**: `url` column = 0 for every one of the 31 files. No `basic-auth-url`, no `url-embedded-secret` (`?token=`, `?api_key=`, `?sessionid=`, `?sig=`), no private RFC1918 URL, no `localhost`/`127.0.0.1`/`[::1]` URL, no `Set-Cookie`/`cookie-jar`/`cookies.txt`.
- **Credential-shaped filenames**: `entropy.py` §C over the round's new bytes printed nothing — no `.netrc`, `.npmrc`, `.pypirc`, `.dockercfg`, `id_rsa`/`id_ed25519`, `.env*`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.keystore`, `credentials*`, `secrets.{yaml,json,toml,txt}`, `*.kdbx`.
- **High-entropy runs**: `entropy.py` §B triaged every long alphanumeric/base64 run in the round's new bytes. Every one classifies as `sha256-hex64` (the capture digest and the pre-existing digests in `corpus/SOURCES.md`), `wordy-novel` (English/path text), or `url-ish`. The two `opaque-token-like` runs in `S091.txt` were re-triaged masked in `triage.py` §E/§K: both are **whole stripped lines** (`equals-whole-stripped-line=yes`) of pure alphabetic hyphenated heading text (`segments=1`, `all-segments-alpha=yes`) — the article's own section headings, not inline values. `triage.py` §F then found **zero** runs passing the stricter "alnum-and-dash, no digit, ≥3 vowels" word test, i.e. no opaque token-like run survives as a distinct value.
- **Host-specific absolute home-directory paths (class count only, values withheld)**: **66 lines** across the 31-file sweep; **29 lines** across the round's 23 implementation bytes. Per file: `claims.json` 1, `after-r58.txt` 3, `make-impl.py` 1, `run-a.sh` 2, `run-after.sh` 1, `run-c1-mutants.sh` 1, `run-do-nothing.sh` 1, `do-nothing-c1-mutants-r58.txt` 3, `do-nothing-c1-r58.txt` 5, `neighbor-screen-r58.txt` 2, `standin-after-r58.txt` 1, `corpus/README.md` 3, `corpus/SOURCES.md` 7, the new entry 1, `lessons/round-58.md` 3, the three wave-control JSONs 10 each, `w1.ready` 1. **Baseline**: 70 of the 77 pre-existing `corpus/knowledge/*.md` files already carry ≥1 such path (97 lines in the pre-existing knowledge corpus) — this is a long-standing lane convention (the `recheck:` line naming the lane root), not a round-58 introduction. The single home-path line in the new entry is `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:6`, the `recheck:` command, and it is the same convention as the sibling entries.

### 2.3 Instructions to probe, scan, log in to, or submit against a target

Command: `python3 final_table.py`, section "instruction-verb classification"; and `python3 scan.py` §5.

Every instruction-verb hit in the round's bytes is one of: this seat's own prompt text; the lane's own "capture probe" / "probe-a2" control-artifact names; the entry's documentation-only *denial* sentence (§3); or the source article's descriptive prose. **No file of the round instructs a probe, scan, login or submission against any target.**

Specifically for the capture (`corpus/source-snapshots/round-58/S091.txt`), `kwclass.py` §L found 2 lines matching imperative security verbs (`:19` "identify and exploit cybersecurity weaknesses in target systems"; `:36` "a 32-step simulated corporate network attack"). Both are the **captured third party's own descriptive prose** about AISI's closed test suite, carried verbatim in the snapshot; neither is a lane-issued instruction, and `scan.py` §5's target-complement test marked 0 of the capture's verb lines as carrying a target complement. The entry quotes none of it as an instruction and adds a denial sentence (§3).

## 3. The entry's documentation-only statement (Attribution and Limits)

Command: `python3 scan.py` §7 and `python3 final.py` §R.

`corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:15-16` (in the `## Attribution` section, lines 8-16):

```
## Attribution
...
It is documentation-only: it instructs no probing, scanning,
login or submission against any target, and carries no credential material.
```

`scan.py` §7 confirms the statement's own wording names all four verbs (probing, scanning, login, submission) and asserts the absence of credential material — and §2 above independently confirms the absence of credential material in that file (1 `cred` hit, the denial sentence itself).

**Limits section** (`corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:71-83`), full text read in `final.py` §R: five limit bullets — dated blog post (byte stability asserted within this round's opens only; the 90d recheck re-fetches), METR's 4.2-month figure named but not absorbed (the linked Trends Report named but not opened: a lead, not a row), the report's three footnotes read as part of the statements, and province adjacency (LLM evaluation method is kengaku's). **The Limits section itself contains no instruction to probe, scan, log in to, or submit against any target** — it is entirely scope-limiting language. The seat asked to check Limits *and* Attribution for the documentation-only statement: the statement lives in Attribution (the lane's dominant placement — 9 of the 14 entries carrying the phrase put it in an Attribution/boundary section, per the `scan.py`-adjacent placement check), and the Limits section adds no contrary instruction.

`final.py` §S ran a targeted "does any sentence direct an action against a target" test over the entry. Its only two hits were `entry:6` (the `recheck:` command, which runs the lane's own local `source-recheck.py`) and `entry:68` ("not a reproducible public benchmark"). Neither is an instruction against an external target.

## 4. The capture was a plain public GET; no credentials were used

### 4.1 The manifest fetch-method and auth/header field check

Command: `python3 scan.py` §6 (the manifest is parsed and every source key is printed; the blob is probed for auth/header/cookie/token/bearer/credential/apikey/api_key/password substrings).

```
   key=body_lines value=[1, 67]
   key=bytes value=11660
   key=capture_url value='https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing'
   key=fetch_method present len=215
   key=fetched_utc value='2026-11-03T20:35:59Z'
   key=http value={'status': 200, 'final_url': 'https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing'}
   key=id value='S091'
   key=kind value='html'
   key=lines value=67
   key=path value='S091.txt'
   key=quotes (count=9)
   key=sha256 value='d2ba7199faf44fb9f5fc5c48924f20d72ed08959c511af58cb9c1322f9820618'
   key=snapshot_bytes value=11660
   key=url value='https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing'
   manifest top-level keys=['note', 'schema_version', 'sources']
   manifest-blob contains auth       : no
   manifest-blob contains header     : no
   manifest-blob contains cookie     : no
   manifest-blob contains token      : YES
   manifest-blob contains bearer     : no
   manifest-blob contains credential : no
   manifest-blob contains apikey     : no
   manifest-blob contains api_key    : no
   manifest-blob contains password   : no
   fetch_method field verbatim:
     capture-source.py default urllib open, status=200 at this host (the iso.org Cloudflare block of round 57 does not apply here); two same-sha opens recorded (probe 20:35:32Z, recorded + verification re-open 20:35:59Z)
   http block: {'status': 200, 'final_url': 'https://www.aisi.gov.uk/blog/how-fast-is-autonomous-ai-cyber-capability-advancing'}
```
exit code 0.

**Result**: the manifest has **no `auth` field, no `header` field, no `cookie` field, no `bearer` field, no `credential` field, no `apikey`/`api_key` field and no `password` field**. The single `token` substring in the manifest blob is the "2.5M token cap" wording in the `note` and in the Q3 pinned quote (§2.1). The `http` block carries only `status` and `final_url`. The `fetch_method` names `capture-source.py default urllib open` — a plain GET.

### 4.2 The builder command that produced the manifest

Command: read of `.ufo/waves/round-58/controls/builders/build-manifest.py` (81 lines; whole file read).

The builder reads the **committed** snapshot (`SNAP = "corpus/source-snapshots/round-58/S091.txt"`, opened `"rb"`), computes the digest over those bytes, and writes the manifest. It makes **no network call and accepts no credential**: `grep -n 'urllib\|requests\.\|http[s]\?://\|curl\|wget\|Authorization\|Bearer\|api_key\|token\|password\|cookie\|session\|getenv\|environ'` over the file returns only `URL = "https://www.aisi.gov.uk/…"` (the public URL constant), the two "2.5M token cap" prose strings, and the `fetch_method`/`note` prose.

`make-impl.py` is the other builder. Its network-relevant line is `out, rc = sh("git clone -q --shared %s %s" % (L, S), "/")` — a local clone of the lane into the scratch stand-in — plus `shutil.copyfile` of the two committed capture files into that scratch clone. It performs **no** HTTP fetch and reads no credential.

The instrument that actually performs the fetch is `corpus/instruments/capture-source.py` (pre-existing, not changed by this round — it is absent from the round's diff list). Its fetch path is exactly two lines (`capture-source.py:74-75`):

```
request = urllib.request.Request(url, headers={"User-Agent": UA})
with urllib.request.urlopen(request, timeout=60) as response:
```

`scan.py` §9 and `kwclass.py` §N confirm these are the **only two** header/auth-bearing lines in that 137-line file: the only header sent is a fixed `User-Agent` string (`capture-source.py:32`, `"kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)"`), and there is no `Authorization`, `Cookie`, `api_key`, `token`, `password` or `session` anywhere in the file. Its CLI takes only `--id`, `--url`, `--out`, `--kind` and `--selftest` (`capture-source.py:121-126`) — there is no flag by which a credential could be supplied.

### 4.3 The manifest is byte-reproducible from the committed capture (no hand-injected field)

Command (scratch, `$S/repro`):

```
$ cd $S/repro && TMPDIR=$S python3 build-manifest.py
Q1: occurrences=1 words=11 anchor=1
... (Q2..Q9 each occurrences=1)
wrote corpus/source-snapshots/round-58/manifest.json sha256 d2ba7199faf44fb9f5fc5c48924f20d72ed08959c511af58cb9c1322f9820618 bytes 11660 lines 67
builder-exit=0
$ diff -u $S/repro/corpus/source-snapshots/round-58/manifest.json \
       /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-58/manifest.json
IDENTICAL
```
exit code 0. The committed manifest is exactly what the committed builder emits from the committed capture — so no field (including any hypothetical auth field) was hand-inserted into it.

### 4.4 The capture's own bytes carry no credential

`corpus/source-snapshots/round-58/S091.txt` is the public article text (67 lines). Its only credential-word hit is the site's own cookie notice (§2.1). It contains no URL with credentials, no session value, no key.

**Fetch-method verdict: CONFIRMED.** Plain public GET through the lane's `capture-source.py`, a fixed `User-Agent` and nothing else, `HTTP 200`, no auth header, no cookie, no credential-bearing field in the manifest.

## 5. FINDING 1 (medium, safety) — the figure-audit read-only derive gate is bypassable; the round's "read-only derive gate" framing overstates the guarantee

### The claim surface

C1's frozen sentence names "the read-only derive gate" as the thing mutant **m6** disables, and adds the new selftest case **`derive-not-read-only-refused`** ("a non-allow-listed head must be refused with exit 2"). The gate is `check_read_only` in `corpus/instruments/figure-audit.py:78-84`:

```
def check_read_only(cmd):
    head = cmd.split("|")[0].split(">")[0].strip()
    if head.startswith(("python ", "python3 ")):
        # a counter run is admissible only against a committed instrument
        parts = head.split()
        return len(parts) >= 2 and parts[1].replace("\\", "/").startswith("corpus/instruments/")
    return head.startswith(READ_ONLY_HEADS)
```

The gate inspects **only the text before the first `|` or `>`**. Everything after it, and every metacharacter inside the head, is unchecked.

### Exploit path (all probes run in scratch only; no lane byte was executed or modified)

Command: `python3 gate_probe.py` (scratch, imports the gate from the committed instrument bytes; the probes' side-effect commands are a `touch` of a marker file inside the scratch tree and nothing else).

```
=== SECTION U: check_read_only() gate probe (imported from the committed instrument) ===
PROBE p1-baseline-grep         allowed=True   why=read-only head
PROBE p2-plain-echo            allowed=False  why=NOT a read-only head -> must refuse
PROBE p3-chained-semicolon     allowed=True   why=chains a second command
PROBE p4-chained-ampersand     allowed=True   why=chains a second command
PROBE p5-command-substitution  allowed=True   why=command substitution
PROBE p6-backtick              allowed=True   why=backtick substitution
PROBE p7-python-traversal      allowed=True   why=python branch with a path escape
PROBE p8-python-semicolon      allowed=True   why=python branch with a chained command
PROBE p9-redirect              allowed=True   why=redirect target (split on '>')
```
exit code 0.

End-to-end, with the instrument actually running the derive (`scan.py`-independent; `gate_probe.py` §V):

```
=== SECTION V: end-to-end - does the instrument actually EXECUTE a chained derive? ===
   instrument exit=1
   stdout: FIG probe-1 recorded=35 derived=1
   stdout: 35 want=35 stale
   stdout: FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1
   marker file created by the chained derive = YES
```
exit code 0. The derive was `grep -c . <seed> ; touch <marker> ; echo 35` — an allow-listed head plus a `;`-chained write, which the gate **allowed** and the instrument **executed**.

A second scratch probe (`pipeline_probe.py` §X) shows the same for a pipeline stage, a redirect and a command substitution:

```
PROBE x1-newcase-shape           exit=2 refused=True  side-effect-executed=False
PROBE x2-semi-chain              exit=1 refused=False side-effect-executed=True
PROBE x3-pipeline-stage          exit=1 refused=False side-effect-executed=True
PROBE x4-redirect-target         exit=1 refused=False side-effect-executed=True
PROBE x5-substitution            exit=1 refused=False side-effect-executed=True
```
exit code 0. `x1` is the round's own new-case shape (`derive` = `echo 35`) and is correctly refused with exit 2 — so **the new case does hold the line it is named for**. `x2`–`x5` are allow-listed-head variants and all execute their side effect.

The most severe form is the **python branch**: `corpus/instruments/figure-audit.py:80` accepts any `parts[1]` that *starts with* `corpus/instruments/`, with no normalisation of `..`. Probe (`gate-probe5`, scratch), with the escaping target placed outside `corpus/instruments/`:

```
derive shape: python3 corpus/instruments/../../../deep/escape.py
instrument exit=0
  FIG probe recorded=35 derived=35 ok
  FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0
REFUSED by gate = False
script OUTSIDE corpus/instruments executed = True
```
exit code 0. The gate accepted a path that escapes the instruments directory, the script ran, and — because the derive's stdout matched the recorded value — **the audit reported `ok=1 … exit=0`, a green result**. (An earlier probe using `../../../deep/a/b/c/escape.sh` exited 2 because `python3` was handed a shell script; the `.py` form in `gate-probe5` is the one that executes and returns 0.)

### Why the new selftest case does not close this

`gate_probe.py` §Z and the committed fixture (`corpus/instruments/figure-audit.py:147-151`) show the new case's derive is `echo 35`:

```
    committed instrument: {"id": "s-not-ro", "record": "g.txt:1", "recorded": "35", "derive": "echo 35", "want": "35"}
```

`echo 35` has a head that is in neither the allow-list nor the python branch, so the case exercises exactly one refusal path. **m6 replaces only the final `return head.startswith(READ_ONLY_HEADS)`** — the non-python branch's last line. So:

- m6 **is** killed by the new case (the committed fixture's derive is python-free, which is what makes the kill work). The committed battery confirms the kill: command `python3 corpus/instruments/figure-audit-mutbat.py`, output `MUT m6-readonly-gate-off sites=1 py_compile=0 selftest_exit=1 killed=1` / `mutbat killed=2/2 survivors=0 controls=pass`, exit code 0. **C1's kill rule is satisfied on this limb.**
- But the case does **not** cover the python branch at all, and m6 does not touch it. Nothing in the round's new bytes pins the python branch's path check, and nothing pins the head-plus-metacharacter forms.

### Is it reachable today? No live breach from the committed ledger

Command: `python3 triage.py` §Y and a per-ledger scan of every `figures` array in the lane (`corpus/instruments/*.json` + `.ufo/waves/round-*/controls/*.json`):

```
    committed ledger derive strings carrying ;/&&/||/backtick/$(: 6
```
and, separating shell separators from separators *inside* quoted awk/sed programs:

```
derives with raw metachars = 6 ; of those, ones with UNQUOTED shell separators = 2
  corpus/instruments/figure-audit-ledger.json  id=figure-audit-mentions-base-log
  corpus/instruments/figure-audit-ledger.json  id=figure-audit-mentions-base-knowledge-expected
```
exit code 0. Those two are `git cat-file -e <rev>:<path> && git show <rev>:<path> | awk …` — a `&&` between two **read-only** git commands, which is benign. The other four carry their `;` inside a quoted awk program. **No committed ledger derive can execute a write.** This matches the round-57 finding already on file: `.ufo/waves/round-57/w1/LedgerReplay.md:322-337` ("F2 (advisory, instrument safety claim) — `check_read_only` is bypassable with `;`") and its own "Not reachable from the current ledger … all 35 recorded derives were probed … anomalous=0".

### Impact, and the smallest remediation

The gate exists to make the ledger's `derive` strings non-mutating by construction. It does not: it is a prefix check on the first pipeline segment. A ledger file is an input the instrument executes; anyone who can write one can run arbitrary commands under the lane's account (the instrument runs `bash -c <derive>` at `corpus/instruments/figure-audit.py:65`). Today the committed ledger is clean, so there is no live breach — but the guarantee the round's own claim names ("the read-only derive gate") is not the guarantee the code provides, and the round's new selftest case pins only one narrow shape of it, which is what lets the m6 kill stand while the gate stays bypassable.

**Smallest remediation** (text only — I did not edit any instrument; the seat's contract forbids it): refuse any derive whose head contains a shell metacharacter, and normalise the python branch's path before the prefix test. Concretely, in `check_read_only`, (a) reject a head matching `[;&|><`$]` or containing `$(`, and (b) replace the python branch's `parts[1].replace("\\", "/").startswith("corpus/instruments/")` with a `os.path.normpath` on the joined path plus a check that the normalised result is still inside `corpus/instruments/`. Two additional selftest cases (one for the `;`-chain, one for the `..` escape) would then make both limbs load-bearing under R17.

**Severity: medium.** No live breach from any committed byte; the exposure is a gate that a name and a mutation test present as stronger than it is, on an execution path a committed file drives.

## 6. FINDING 2 (low, provenance) — the manifest `bytes` field records the snapshot size under a field name earlier rounds used for the fetched size

Command (`python3 -c` over the four round manifests, sizes cross-checked with `ls -la`):

```
round-55 S087 manifest.bytes=937712  manifest.snapshot_bytes=137738
round-56 S088 manifest.bytes=7203    manifest.snapshot_bytes=7204
round-57 S089 manifest.bytes=88964   manifest.snapshot_bytes=6647
round-58 S091 manifest.bytes=11660   manifest.snapshot_bytes=11660
```
exit code 0.

In rounds 55-57, `bytes` is the **fetched** size and `snapshot_bytes` the snapshot size (round-56 even shows them differing by one byte: 7203 fetched vs 7204 snapshot). In round 58, `build-manifest.py:66-67` computes both from the **committed snapshot** (`"bytes": len(raw)`, `"snapshot_bytes": len(raw)`, where `raw = open(SNAP, "rb").read()`), so both are 11660 and the fetched size (33476) appears **nowhere in the manifest**. It is asserted only in prose: `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:3` ("11660 snapshot bytes over 33476 fetched") and `corpus/lessons/round-58.md:26`.

**Impact.** A field whose name meant "bytes fetched" in the three preceding rounds now means "bytes of the snapshot" — a consumer comparing `bytes` across rounds will read 11660 where 33476 was fetched. The provenance triple the manifest exists to carry (`sha256` binds the snapshot; `fetched_utc` and `fetch_method` are prose) is therefore not machine-checkable for the fetch size, and no instrument validates it (`source-recheck.py` and `capture-binding-check.py` check the digest and the binding, not `bytes`).

**Smallest remediation** (text only): rename or split the field in the round-58 manifest — e.g. keep `snapshot_bytes` and add `fetched_bytes` — or state in the manifest `note` that `bytes` is the snapshot size for this source, so the field's meaning is not silently redefined. Neither the claims' C2 kill rule nor `capture-binding-check.py` is affected today, since neither reads `bytes`.

## 7. FINDING 3 (low, provenance) — no round-58 receipt records the capture; the "two same-sha opens" claim is prose-only

Command: `grep -rn 'capture-source.py' /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-58` (3 matching lines), and `grep -rn '20:35:32' …` (excluding the manifest, the entry, the lessons file and the claims file).

```
   .ufo/waves/round-58/controls/builders/build-manifest.py:50
   .ufo/waves/round-58/controls/builders/build-manifest.py:59
   .ufo/waves/round-58/claims.json:7
```
exit code 0. Every occurrence is inside a **prose string** the builder writes (`build-manifest.py:50` is the `note`'s "Capture method:" sentence; `:59` is the `fetch_method` value), not a recorded invocation. The only other place the probe timestamp `20:35:32Z` appears is `build-manifest.py:61`, again inside the same prose string.

By contrast, rounds 55, 56 and 57 each committed a capture/recheck receipt (`s087-recheck-r55.txt`, `s088-opens-r56.txt`, `s089-s090-recheck-r57.txt`); round 58's `controls/` holds none (directory listing in §1's file set shows only the four do-nothing receipts, `neighbor-screen`, `standin-after`, `after-r58` and the `builders/` directory).

**Impact.** The manifest asserts "two same-sha opens recorded (probe 20:35:32Z, recorded + verification re-open 20:35:59Z)" and the entry asserts "a second same-sha open at 20:35:32Z and a third recorded open at 20:35:59Z are byte-identical", but no committed artifact in the round records either open — there is no capture log and no probe receipt, so the assertion is not independently re-checkable from the lane's committed bytes. This bears on the round's own claim (`claims.json` `host` field) that "the lane instrument capture-source.py opened … with HTTP 200 … controls: capture probe and recorded capture, two same-sha opens". It does **not** affect any kill rule: the C2 kill rule pins the sha256 of `S091.txt` and the nine quote anchors, all of which I confirmed present and matching (`after-r58.txt:84-96` shows `S091:sha256 OK` plus nine `Q` OK lines, `occurrences=1`).

**Smallest remediation** (text only): commit the capture instrument's own stdout line (`S091 status=200 fetched_bytes=… snapshot_bytes=… sha256=… utc=… out=…`, the format `capture-source.py` prints at `capture-source.py:94-96` and the format rounds 24-25 recorded in `capture-log.txt`) as a round-58 control, so the two-open assertion is backed by a receipt rather than by prose. I did not re-fetch the URL — that is the C2 reviewer's and the round's business, and my seat is a scan.

## 8. Scope and process audit of the round's new bytes

### 8.1 Where the builders write

Command: `grep -n 'open(.*"w"\|>>\|shutil.copy\|shutil.rmtree\|os.remove\|unlink\|tee ' …/builders/*.py …/builders/*.sh`.

Every write target in the six builders is one of: the lane's own `.ufo/waves/round-58/controls/` receipt directory; the lane's own `corpus/` files inside a **scratch clone** (`make-impl.py` writes the instrument, the mutbat, the red fixture, the entry, `SOURCES.md`, `README.md`, `PROVINCE.md` and `knowledge-expected.txt` only inside `S = /fast/scratch/hyaku/kasegi-r58/standin`, the shared clone); or a scratch path under `/fast/scratch/hyaku/kasegi-r58/`. `make-impl.py:168` copies the two committed capture files **into** the scratch clone. `make-impl.py:161` `shutil.rmtree(S)` removes only the scratch stand-in. No builder writes outside the lane's own tree and the scratch root; no builder writes into a sibling lane; `run-a.sh:43` only **reads** `kengaku-shokunin/PROVINCE.md` (a `grep -in` over it), which the contract permits.

### 8.2 The mutating-instrument path in `figure-audit.py` / `figure-audit-mutbat.py`

Command: `python3 final.py` §T, plus the full read of both files.

- `figure-audit.py:65` runs `subprocess.run([bash, "-c", cmd], cwd=root or ".")` on the ledger's `derive` string — the execution sink analysed in §5.
- `figure-audit.py:157` / `mutbat.py:45` create a temp dir with `tempfile.mkdtemp` (honours `TMPDIR`) and `shutil.rmtree` it in a `finally` — cleanup is correct, no leaked temp dirs.
- `mutbat.py:21` resolves the instrument as `os.path.join(HERE, "figure-audit.py")` — anchored to the script's own directory, not to a cwd or an env var, so it cannot be redirected.
- `mutbat.py:36` runs `subprocess.run([sys.executable, path, "--selftest"], cwd=tmp, …, timeout=600)` — same interpreter, cwd in the temp dir, bounded timeout.
- No file in either instrument reads an environment variable other than `TMPDIR` (via `tempfile`), and neither reads any credential, cookie jar or session file. `figure-audit.py:61` and `:171` use `shutil.which("bash")` and fail closed with `no-bash-on-host` if bash is absent.
- `figure-audit.py:198` defaults the ledger to `corpus/instruments/figure-audit-ledger.json` relative to the cwd — a relative, lane-internal path; `--ledger` and `--root` are the only overrides, and the red fixtures the round uses live under `.ufo/waves/round-5X/controls/`.

### 8.3 The round's own committed battery, replayed read-only

Command: `TMPDIR=$S python3 corpus/instruments/figure-audit-mutbat.py` (run from the lane root; the battery writes only into `TMPDIR`).

```
PRISTINE selftest_exit=0 last='selftest cases=6 failures=0'
CONTROL c-equivalent-trailing-space selftest_exit=0 must_not_be_killed=held last='selftest cases=6 failures=0'
MUT m4-drop-stale-literal-case sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=5 failures=1'
MUT m6-readonly-gate-off sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=6 failures=1'
mutbat killed=2/2 survivors=0 controls=pass
mutbat-exit=0
```
exit code 0. Consistent with C1's `after` string. (This is corroboration for §5, not a C1 verdict — the C1 verdict belongs to the C1 critic and the mutation-tester seats.)

### 8.4 The round's committed ledgers — chain-metachar audit

Command: the per-ledger scan in §5 ("derives with raw metachars = 6 ; of those, ones with UNQUOTED shell separators = 2"), plus `python3 -c` over `corpus/instruments/figure-audit-ledger.json` (35 entries). Every committed derive's head is one of `git`, `grep`, `sha256sum`, `wc` — all in `READ_ONLY_HEADS` (`corpus/instruments/figure-audit.py:47-50`). The `&&` cases chain two read-only git commands. **No committed derive can write.**

### 8.5 The red fixture the round repointed

Command: `git diff 1e5c8f2 … 18ddb05 -- .ufo/waves/round-54/controls/red-d53-ledger.json`.

```
-   "derive": "python corpus/instruments/frontier-recheck-count.py 2>/dev/null | grep -c '^FAIL'",
+   "derive": "grep -oE 'FAIL_entry_records=[0-9]+' .ufo/waves/round-53/controls/c2-counter-final-r53.txt | head -1 | cut -d= -f2",
```
exit code 0. The repoint **narrows** the exposure: the old derive ran a live counter through the python branch of the gate (a committed instrument, but one that executes); the new derive is a pure `grep | head | cut` over a committed receipt — head `grep`, no metacharacter outside the quoted `-oE` pattern, no python branch, no write. This is a safety improvement, not a regression.

### 8.6 Lane-tree integrity of this seat

Commands: `git status --porcelain` before and after; `find . -newermt '2026-11-03 17:53' -type f`.

The only lane file this seat caused to change is `corpus/instruments/__pycache__/figure-audit.cpython-314.pyc` — a gitignored bytecode cache (`git check-ignore -v` → `.gitignore:2:__pycache__/`), written by CPython when `gate_probe.py` imported the instrument to exercise `check_read_only` directly. Its header records `source_size=8683`, i.e. the **current** instrument (the base instrument is 8221 bytes), so it is my import's artifact and not a pre-existing stale cache. `LOG.md`, `SCORECARD.md` and `corpus/QUALITY.md` show as modified in `git status`; their mtimes are `17:51:50`–`17:52:23`, i.e. **before** my seat's first command, and they are the integrator's concurrent round-58 narrative appends (their diffs are the round-58 LOG/SCORECARD/QUALITY sections), not mine. `ScoutSources.md` and `ReviewerC2.md` in `w1/` are sibling seats' evidence files. **No file under the lane was edited by this seat**; no `git add`, `commit`, `stash`, `checkout`, `switch`, `reset`, `pull`, `push` or `jj` command was run against the lane, and the only git commands used were read-only (`diff`, `show`, `log`, `status`, `ls-files`, `ls-tree`, `check-ignore`).

### 8.7 Builder and instrument prose: any instruction to act against a target?

`scan.py` §8 and §9 over the six builders and the capture instrument: the only matches are the public URL constant, the "2.5M token cap" prose, the `fetch_method` prose, the `TMPDIR` assignment, and `capture-source.py`'s `import urllib.request` / `Request(url, headers={"User-Agent": UA})` / `urlopen(...)`. **No builder and no instrument instructs a probe, scan, login or submission against any target**, and no builder or instrument reads a credential.

### 8.8 The integrator's concurrent narrative files

Command: `python3 -c` over `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`.

```
FILE LOG.md lines=2587 secret-shaped-hits=0
FILE SCORECARD.md lines=2407 secret-shaped-hits=0
FILE corpus/QUALITY.md lines=452 secret-shaped-hits=0
```
exit code 0. The round-58 narrative the integrator appended to these three files carries no credential material. Their home-abs-path line counts (10, 5, 8) are the lane's existing narrative convention.

## 9. Scratch hygiene and leftovers

`mkdir -p /fast/scratch/hyaku/kasegi-r58/SentinelCred` at the start; every clone-equivalent copy, probe tree, mutant copy and temp file was written under it, with `TMPDIR` pointed at it on every invocation that could write. The scratch root was deleted before this evidence file was yielded:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r58/SentinelCred && ls -d /fast/scratch/hyaku/kasegi-r58/SentinelCred
ls: cannot access '/fast/scratch/hyaku/kasegi-r58/SentinelCred': No such file or directory
```
exit code 2 from the `ls` (the expected "gone" result); the `rm` succeeded. The parent `/fast/scratch/hyaku/kasegi-r58/` now holds only other seats' directories (`EntryClaimTable`, `SiblingOverlap`, `l1-recon`, `pre-frozen`, `standin`, `tmp`, `wc`) — none of them mine.

**Named leftover**: one lane-side trace remains from this seat, `corpus/instruments/__pycache__/figure-audit.cpython-314.pyc` (12599 bytes, mtime 2026-11-03 17:53:26). It is CPython's bytecode cache, written when `gate_probe.py` imported the committed instrument to exercise `check_read_only` directly (§5). It is **untracked and gitignored** (`git check-ignore -v` → `.gitignore:2:__pycache__/`), it is not part of the round's committed bytes, and it is regenerated automatically on the next import. It is left in place rather than deleted, because removing a file under the lane is itself a lane mutation and the seat contract restricts me to my own evidence file. Its header records `source_size=8683`, i.e. the current instrument, so it is this seat's artifact and not a stale pre-existing cache. No other file of the lane was modified by this seat (§8.6).

## 10. Summary table

| # | severity | finding | path:line | status |
|---|---|---|---|---|
| 1 | medium (safety) | `check_read_only` is a prefix check on the first pipeline segment: an allow-listed head plus `;`, `&&`, an unchecked pipeline stage, a redirect or `$(...)` executes; the python branch accepts a `..`-escaping path and the audit then reports `ok` and exits 0 | `corpus/instruments/figure-audit.py:78-84` (gate), `:65` (the `bash -c` sink), `:147-151` (the new case's `echo 35` derive) | not reachable from any committed ledger (6 raw metachars, 2 unquoted, both read-only `git && git`); already recorded in part as round-57 F2 (`.ufo/waves/round-57/w1/LedgerReplay.md:322-337`); text-only remediation proposed in §5; **no instrument edited** |
| 2 | low (provenance) | the manifest `bytes` field is the snapshot size (11660) where rounds 55-57 used it for the fetched size (937712 / 7203 / 88964); the fetched size 33476 is prose-only | `corpus/source-snapshots/round-58/manifest.json:18`; builder `.ufo/waves/round-58/controls/builders/build-manifest.py:66-67`; prose at `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:3` | no kill rule affected (no instrument reads `bytes`) |
| 3 | low (provenance) | no round-58 receipt records the capture; the "two same-sha opens" assertion exists only in prose inside the builder's own string | `corpus/source-snapshots/round-58/manifest.json:14`; builder `build-manifest.py:59-62`; absence in `.ufo/waves/round-58/controls/` | no kill rule affected (C2 pins the sha256 and the 9 anchors, both confirmed) |

**Clean on the seat's primary classes**: 0 credential *values* anywhere in the round's bytes — the 14 substantive-named-pattern hits are pattern *names* (twelve in this seat's own prompt enumeration across the three wave-control JSONs, two in pre-existing `corpus/README.md` prose), none a value (§2); 0 `op://` references in the round's 23 implementation bytes (6 literal occurrences across the 31-file sweep, all inside this seat's own prompt text); 0 private/session/localhost URLs; 0 credential-shaped filenames; the entry carries the documentation-only statement (`corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md:15-16`) and its Limits section instructs no probe, scan, login or submission; the capture was a plain public GET with a fixed `User-Agent` and no credential of any kind (`capture-source.py:74-75`; manifest has no auth/header/cookie/bearer/credential/apikey/password field), and the committed manifest is byte-identical to what the committed builder emits from the committed capture.
