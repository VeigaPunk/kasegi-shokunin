# SentSecrets — round-37 no-credential (Q6) sweep over the planned additions

Seat: SentSecrets (leaf sentinel, no subagent dispatch). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`;
lane base `b56a41680cefd391868c1c370dc063c69d827e7d`, claims-freeze `224df74db2a46d627ae1475a72ca48796bbd177c`,
erratum head `b362068195d5489aa94b31e6ec8f880c367e0ba0`. Sweep window 2026-10-26T17:0x-17:2xZ, worktree at
`b362068` + 7 dirty entries (all `.ufo/`; `corpus/` byte-unchanged this round — `git status --porcelain` carries no
`corpus/` or top-level path).

Answering model: `opencode-go/deepseek-v4.1-flash` (route from the spawn chain; the item does not depend on it).
**Tooling: nothing installed or upgraded** (no pacman — host-wide pause honoured; no uv/npx/curl fetch by this seat;
`grep (GNU grep 3.12)`, `python3`, `sha256sum` pre-existing). No network call was made by this seat; the capture bytes
audited below were read from the executor's landed receipt, not re-fetched.

Scratch: `/fast/scratch/hyaku/kasegi-r37/SentSecrets/` (scanner, controls, extraction, `pattern-grep.txt`); removed at
yield after this receipt was written. Nothing was fetched into it.

---

## 0. What this seat decides

The frozen claims add a knowledge entry, a registry row, a lesson, a considerthese ledger, a round report, edits to
`LOG.md`/`SCORECARD.md`/`SKILL.md`/`corpus/QUALITY.md`, and two capture artifacts. Every one of them is published into a git
repository that is read by later rounds, so a credential, a session parameter or a private URL that lands here is
permanently public in history. This receipt (a) states the rule the artifacts must satisfy, (b) runs a discriminating
scan over the proposed bytes and reports the count, (c) proves the scan is not vacuous on those same bytes, and (d)
hands the one command that must stay green after integration.

**Verdict: 0 credential, 0 session/signed-URL parameter, 0 loopback/private/internal URL, 0 vault-reference URI in every
planned round-37 artifact, including the 518-line S054 capture bound by `sha256 ff3f3b2c…fdce21`.**

Scope of that "0": the published content artifacts (entry, row, lesson, ledger, capture + manifest, final-gates receipt,
`LOG.md`, `SCORECARD.md`, `SKILL.md`). **Wave receipts are excluded by construction** — an instrument sweep carries
pattern-shaped fixtures on purpose (§4), so a receipt is never content and its bytes are never the thing the rule
protects. What a receipt must never carry is a *value*, and the classifier this seat ran masks every preview to three
characters plus a length (§2).

---

## 1. The rule statement for integration (Q6, round 37)

Quotable text, suitable for the round-37 lesson Gate and for the entry's Q6 line to point at:

> **Q6 no-credential rule (round 37).** Every round-37 addition — the S054 capture (`corpus/source-snapshots/round-37/S054.txt`)
> and its `manifest.json`, the SSVC knowledge entry, the `S054` registry row, the round-37 lesson,
> `corpus/considerthese-ledger.md`, the round report and this round's wave receipts — is documentation-only in the
> QUALITY Q6 sense: it carries no credential value, API key, private-key block, session token, cookie or signed-URL
> parameter, no loopback, private-network or internal-host URL, and no vault-reference URI (the op-scheme form). Where a
> source or a capture does carry such material, its **location** is named (capture line range or `file:line`) and the
> **value is never reproduced**. The gate is one command over the round-37 paths (§2) and it must print `0`; a non-zero
> count is a **rejection of the adding artifact**, not a wording fix. A redaction placeholder that still trips the
> session/signed-URL shapes is read as "review this line", never waived silently (§4.3).

Consequences the integration text should keep:

1. The entry's `Documentation only:` line asserts a fact **about the capture bytes**. It is an assertion until a command
   backs it; §3 of this receipt is that measurement (0 password inputs, 0 cookies, 0 auth headers, 0 PEM blocks, 0
   base64 blobs, 0 IPv4, 0 `mailto:`, 0 `sessionid=`/`?token=` shapes over all 518 lines). Either cite
   `SentSecrets.md §3` or drop the sentence to a weaker "this entry quotes no such line".
2. Capture line numbers may be named; capture bytes may not be pasted when the line is a mailbox, an account
   instruction, or a form. The S054 page contains none of those — so the ordinary quote practice applies unchanged.
3. A later fetch is a new pin; this audit is bound to one hash (§3) and says nothing about a re-fetch.

---

## 2. The scan command (portable, no scratch dependency)

`PAT` is the literal pattern string printed in §6; a one-line definition so the command is reproducible from this receipt:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
PAT=$(sed -n '/^PAT_BEGIN$/,/^PAT_END$/p' .ufo/waves/round-37/wave1/SentSecrets.md | sed '1d;$d')   # or paste §6
grep -rInP "$PAT" \
  corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md \
  corpus/SOURCES.md corpus/lessons/round-37.md corpus/considerthese-ledger.md \
  corpus/source-snapshots/round-37/ corpus/QUALITY.md \
  .ufo/waves/round-37/final-gates/all-gates.txt \
  LOG.md SCORECARD.md SKILL.md \
  | wc -l          # expect 0
```

Run today over the parts that already exist plus the whole wave tree:

```console
$ python3 $S/credscan.py .ufo/waves/round-37          -> files=55 hits=0   (first pass, before this receipt landed)
$ python3 $S/credscan.py .ufo/waves/round-37          -> files=74 hits=30  (final re-check, wave still landing)
      29 matches on this receipt's 16 fixture/descriptive lines (§2 exclusion; classifier counts matches, grep counts lines);
       1 = `…@shokunin.local`, the lane git identity, in `wave1/SentScope.md:249` (class E, §5 O2)
$ python3 $S/credscan.py corpus                       -> files=259 hits=69   (all class E, §5 O2)
$ python3 $S/credscan.py SKILL.md SCORECARD.md LOG.md README.md PROVINCE.md SHONEN.md corpus/QUALITY.md -> files=7 hits=0
$ grep -cP "$PAT" $S/cap-S054.txt $S/cap-manifest.json -> 0 / 0
```

For a **whole-tree** re-run after integration, exclude the sweep receipt, which carries the instrument fixtures:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
grep -rInP --exclude=SentSecrets.md "$PAT" corpus .ufo/waves/round-37 LOG.md SCORECARD.md SKILL.md \
  | grep -v '^corpus/source-snapshots/round-2[0-9]/' | grep -v '^corpus/source-snapshots/round-3[0-6]/' \
  | wc -l     # expect 0 outside the historical class-E addresses of §5 O2
```

This receipt itself trip-counts 16 lines against the gate at filing — the number moves by one every time this file adds
a line that names a shape, so reproduce it rather than trust it:

```console
$ PAT=$(sed -n '/^PAT_BEGIN$/,/^PAT_END$/p' .ufo/waves/round-37/wave1/SentSecrets.md | sed '1d;$d')
$ grep -cP "$PAT" .ufo/waves/round-37/wave1/SentSecrets.md   -> 16
```

The victims are `?token=`, `file:///`, `op://vault/item`, `http://127.0.0.1…`, `http://169.254.169.254…`,
`Set-Cookie:`, `api_key=CONTROL…` and the lines that count them — every one a line that *describes or injects* a shape.
That is the exclusion in practice, not an exception granted to this file: no value appears here, only masks and
synthetics.

Why a bespoke pattern set rather than `grep -i secret`: the round-33 precedent's five-keyword sweep (`curl|password|
token|api[_-]?key|op://`) cannot see a bare `AKIA…`, a PEM block, a `file:///` path, a `?X-Amz-Signature=` or a
`10.0.0.0/8` URL, and it reports the *word* rather than the *value*. The set below is value-shaped: 24 regexes in 7
classes, plus 12 capture-shape probes. Masked classifier (prints `file:line`, class and a 3-char preview + length,
never the value) was used for every count in this receipt; the grep form is for the gate because it has no scratch
dependency.

---

## 3. The S054 capture: audited on the bytes that will land

The capture is not yet committed at sweep time, so I audited the **byte-exact block emitted by the capture executor**
(`.ufo/waves/round-37/wave1/ExecC2Capture.md`, `BEGIN S054.txt byte-exact` … `END S054.txt`, and the same for
`manifest.json`), and checked that the bytes I extracted are the bytes four other seats pinned:

```console
$ python3 - (extract between markers, drop fences, sha256)
S054.txt      lines 518 bytes 32623 sha256 ff3f3b2cc82819eb52b4292f1fee3efaef40e7102962494cceabc1d7e5fdce21
manifest.json lines  57 bytes  3989 sha256 fabc3163dbd31d33bff6e0bccf8b86b94e081b06b3ab1f00538dd9c0a57df642

$ sha256sum cap-S054.txt RevRowS054/pinned/S054.txt ExecDatawalk/S054-overview.txt MutJunkTwin-2/overview/S054.txt
ff3f3b2c…fdce21  cap-S054.txt
ff3f3b2c…fdce21  RevRowS054/pinned/S054.txt
ff3f3b2c…fdce21  ExecDatawalk/S054-overview.txt
ff3f3b2c…fdce21  MutJunkTwin-2/overview/S054.txt
```

Four independent seats (this one, the row reviewer, the datawalk executor, the junk-twin mutation seat) hold the same
518-line bytes, and that hash equals the one the capture receipt and the manifest record claim. So the audit is of the
artifact, not of a description of it.

```console
$ python3 $S/credscan.py cap-S054.txt cap-manifest.json          -> files=2 hits=0
$ grep -cP "$PAT" cap-S054.txt cap-manifest.json                 -> 0 / 0
$ python3 $S/credscan.py --capture cap-S054.txt
password_input=0 set_cookie=0 authorization=0 bearer=0 pem=0 sshkey=0 base64_120=0 ipv4=0 mailto=0 form=0 csrf=0 session_param=0
```

- **Absolute URLs in the whole 518-line page: one** — `https://www.fema.gov/sites/default/files/2020-07/Federal_Continuity_Directive-2_June132017.pdf.`
  (a public federal PDF cited on the Coordinated Vulnerability Disclosure page family). No query string, no signature,
  no session parameter.
- **Manifest record fields** (`sources[0]`): `id=S054`, `path=S054.txt`, `url=https://certcc.github.io/SSVC/tutorials/ssvc_overview/`
  (the erratum-1 URL — consistent with `claims-erratum-1.md`, and the row draft reports the frozen-text conflict
  verbatim), `fetched_utc=2026-10-26T17:02:19Z` (strict UTC), `sha256` and `raw_sha256` present, 4 quotes, prose only.
  No credential field, no local path, no query parameter.
- The page is a GitHub-Pages documentation site (no login, no form, no search endpoint in these bytes); the zero counts
  above are what a documentation page should produce, and they make the entry's Q6 sentence checkable rather than
  asserted.

**If the landed `S054.txt` hashes differently**, this audit does not carry: re-run the three commands above on
`corpus/source-snapshots/round-37/S054.txt` before the entry's Q6 sentence is allowed to cite it.

---

## 4. Controls — the scan is not vacuous

### 4.1 Synthetic fixtures (positive / negative, 28 lines each)

```console
$ python3 $S/credscan.py control-positive.txt    -> files=1 hits=27
   classes: K=11 P=2 A=3 V=2 S=3 U=5 E=1      (AWS key id + session key, ghp_, glpat-, xoxb-, sk-, AIza,
                                                AGE-SECRET-KEY-1, pypi-, npm_, JWT, PEM header, ssh public-key blob,
                                                password=/api_key=/token=, op://, sops://, sessionid=,
                                                ?X-Amz-Signature=, Set-Cookie:, 127.0.0.1:8080, 192.168.1.10,
                                                10.0.0.5:9000, wiki.corp.internal, file:///home/…, external mailbox)
$ python3 $S/credscan.py control-negative.txt    -> files=1 hits=0
$ grep -cP "$PAT" control-positive.txt           -> 24   (line count; three lines carry two shapes)
$ grep -cP "$PAT" control-negative.txt           -> 0
```

The negative fixture keeps every line's *shape* (`AKIA________________`, `ghp_______`, `sk-_______`,
`op_REDACTED`, `password=<REDACTED>`, `http://<REDACTED-HOST>`) and redacts the values: all classes go to zero.
Injection changes exactly one fact per line — the presence of a value — and the scan flips.

### 4.2 Real-artifact injection (the gate on the bytes that will land)

One synthetic credential line appended to a scratch **copy** of three proposed artifacts:

```console
$ cp cap-S054.txt mut-cap.txt   && echo 'api_key=CONTROLAAAAAAAA0000' >> mut-cap.txt   && grep -cP "$PAT" mut-cap.txt -> 1
$ cp ScribeEntryF20.md mut-entry.md && echo 'see op://controlvault/controlitem' >> mut-entry.md && grep -cP "$PAT" mut-entry.md -> 1
$ cp ScribeRowS054.md  mut-row.md   && echo 'session http://127.0.0.1:8080/admin' >> mut-row.md && grep -cP "$PAT" mut-row.md -> 1
$ pristine counterparts: cap-S054.txt 0 ; ScribeEntryF20.md 0 ; ScribeRowS054.md 0
```

3/3 injected copies red, 3/3 pristine artifacts green. A hit on the landed artifact would therefore have been visible,
not swallowed.

### 4.3 Calibration caveat (must travel with the gate)

Two patterns — `[?&](…|X-Amz-Signature|…)=` and `Set-Cookie: …=` — are **parameter-presence** detectors, not value
detectors: a redacted `?X-Amz-Signature=<REDACTED>` still trips them. That direction is the safe one (false positive,
never false negative), but it means a class-`S` hit is "review this line", not "a secret was found". The negative
fixture above reached `0` only after the parameter *names* were redacted too, which is exactly the distinction.

### 4.4 The gate must not red on its own documentation

A pattern containing literal `op://`, `AKIA…`, `file:///` can match the sentence that documents it. Measured:

```console
$ printf 'Gate: grep -rInP '"'"'%s'"'"' <paths>\n' "$PAT" > selfdoc.txt
$ grep -cP "$PAT" selfdoc.txt -> 1      # before the fix: literal `file:///` matched itself
$ (after encoding the alternative as `file:/[//]/`)  -> 0
```

The pattern shipped in §6 is the fixed form: pasting the gate command into the round-37 lesson keeps the gate green.

---

## 5. Findings register (this item's surface)

| id | severity | finding | exploit path / impact | smallest remediation |
|---|---|---|---|---|
| N1 | none | No credential material in any planned round-37 artifact: scope A (`.ufo/waves/round-37`, 55 files on the first pass and 74 on the final re-check as receipts kept landing — the only non-receipt hit added was one lane-internal `…@shokunin.local` identity at `wave1/SentScope.md:249`) 0 credential classes; S054 capture + manifest (sha-bound, 518+57 lines) 0 and 12/12 shape probes 0; top-level docs 6 files 0. `corpus/` adds exactly one class of hit lane-wide — the historical third-party addresses of O2; the whole-lane census and the classification of every non-email hit are in §5.1. | none reachable | none |
| N2 | none | No session, cookie, signed-URL or private/loopback URL in the additions: class `S` and `U` = 0 in the 55 wave files (this receipt excluded, §2) and in the capture. URL census of the wave tree: `certcc.github.io` 313, `kass.sacinfo.org.cn` 3 (r33 legacy citation), `shokunin.invalid` 2 (instrument UA placeholder), `www.fema.gov` 1, `www.cert.org.cn` 1, `services.nvd.nist.gov` 1, `github.com` 1, `cdnjs.cloudflare.com` 1 — all public documentation hosts. | none | none |
| N3 | none | The capture carries no mailbox, form, auth header, PEM block, base64 blob or IP literal (§3), so the entry's Q6 sentence is true of these bytes and the ordinary quoting practice needs no carve-out for S054. | none | cite §3 in the entry's Q6 line, or weaken the sentence |
| O1 | informational (pre-existing, not round-37) | A personal attribution mailbox appears in two knowledge entries — `corpus/knowledge/submitted-registry.md:91` ("attributed …") and `corpus/knowledge/vdp-disclosure-packages.md:22` ("Attribution identity: `…`") — both a `gmail.com` address, masked here. Q6 does **not** ban an address; the address *is* the documented attribution identity a disclosure package must name, and both entries are unchanged this round (`corpus/` has no dirty paths). | operator identifier published in docs, by design; `mailto:` appears once (`submitted-registry.md:141`) to a **vendor** (`doit.com`), not to that identity | none for round 37; if the operator later wants it out, the move is a per-entry policy decision appended as an erratum, not a silent edit (R16/R18) |
| O2 | informational (pre-existing) | 69 class-`E` hits lane-wide: 56 in 15 historical captures (`round-24` S003/S008/S011/manifest through `round-35` S052 — third-party press/contact addresses inside captured public pages) and 13 in docs, of which 10 are the lane's own `…@shokunin.local` git identity or a third-party commit author (`round-6-aggregator-audit.md:113`). Zero of these are round-37 additions; none is a credential. | none | none; the standing rule is already the right one — name the line, never reproduce the address |
| O3 | informational | `git status --porcelain` at sweep time carries one **modified non-round-37** path, `.ufo/waves/round-36/wave1/ScribeConsiderthese.md` (+38 lines: a dated post-integration addendum by a round-37 scribe seat). Scanned (0 hits) and outside this item's verdict; recorded because E9's clean-tree limb is evaluated on this tree, and because a prior-round receipt being appended to mid-wave is a record-ownership question for the L1. | none for credentials; possible interference with round-36 receipts' cited line numbers | L1 decides whether the addendum lands with the round-37 commit or is moved to a round-37 file |
| O4 | informational | The S054 row draft still prints the pre-erratum URL literal inside its "Conflict reported verbatim" section and correctly states that the delivered manifest uses the erratum-1 URL — which the manifest bytes confirm (`url=https://certcc.github.io/SSVC/tutorials/ssvc_overview/`). No credential relevance; noted so nobody reads the stale literal as a third URL in the row's own source cell. | none | none (the row's binding rules B4/B5 are the C2 chain's surface) |

### 5.1 Lane-wide census — every non-email hit accounted for

A whole-repo run (`.git`, `.jj`, `__pycache__` skipped) separates "the additions are clean" from "the lane has never
carried a secret":

```console
$ python3 $S/credscan.py .   -> files=7311 hits=1467     (37 s)
   E=1416  S=18  U=28  A=2  V=2  P=1
```

- **E=1416** — third-party press/contact addresses inside captured public pages and their copies under
  `.ufo/waves/round-25/{mut-audit/base,rev-independent/base-tree}/` (fixture trees that embed a round-23/24 tree).
  Authored docs contribute 13 (O1/O2). Not a credential class; nothing to remediate.
- **16 lines in this receipt** (`A=2 S=7 U=6 V=1` at the census run, one line more after the census was written) — the
  synthetic controls of §4 and the sentences describing them. §2 excludes this file from the gate for exactly this
  reason, and states how to re-measure.
- **30 hits in historical `.ufo` wave evidence, 0 in `corpus/`, 0 in a committed knowledge entry.** Read line by line;
  every one is pattern text, a fixture operand, or a recorded response header:
  - `?token=|?key=|?sig=|?signature=` and `.netrc`/`id_rsa`/`.aws/credentials` **as detector pattern text** in prior
    sentinel receipts (`.ufo/waves/round-35/wave1/SentCred.md:57`, `.ufo/waves/round-36/wave1/SentSecrets.md:49`).
  - `op://vault/item` and `-----BEGIN OPENSSH PRIVATE KEY-----` **as regex literals inside a quoted scanner source**
    (`.ufo/waves/round-36/wave1/CritBoundary.md:110`), which that receipt itself labels "detection patterns, not key
    material".
  - `file:///path/to/capture.html`, `file:///tmp/kasegi-r23-…`, `file:///etc/hostname` — local **fixture** operands of
    `capture-source.py` (`.ufo/waves/round-23/build/CvssRecheck.md:92,174`;
    `.ufo/waves/round-24/wave1/SentinelQ6.md:133,169`), plus `http://127.0.0.1:<port>/` and
    `http://169.254.169.254/latest/meta-data/` as the round-24 Q6 sentinel's **negative control** that the capture
    instrument must not reach loopback or the metadata service (`SentinelQ6.md:147`).
  - `Set-Cookie: ['bStore=Y; …', 'CAS_PROGRAM=foxtrot; …']` — non-authenticated tracking-cookie values recorded as
    capture-personalization evidence on a public host (`.ufo/waves/round-31/wave1/RevSourceBar.md:30,82`,
    `.ufo/waves/round-31/wave2/SentScopeFinal.md:315`); cookie **names and public values**, no session credential.

No live credential, no live session token, and no private service URL exists anywhere in the 7311 files: there is
nothing to rotate and nothing to redact. The single historical `Set-Cookie` value class is third-party and
non-authenticated; a re-fetch that recorded an *authenticated* cookie value would be a real finding — which is why the
`Set-Cookie` shape stays in the pattern set as a "review this line" class (§4.3).

---

## 6. The pattern set (durable copy — scratch is deleted at yield)

`PAT_BEGIN` — one POSIX-class/PCRE alternation, `grep -P`:

```
PAT_BEGIN
AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|glpat-[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|(?<![[:alnum:]_-])sk-(ant-)?[A-Za-z0-9_-]*[0-9][A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{35}|AGE-SECRET-KEY-1[0-9A-Z]{20,}|pypi-AgEIcHlwaS5vcmc[A-Za-z0-9_-]{10,}|npm_[A-Za-z0-9]{36}|eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.|-----BEGIN [A-Z ]*PRIVATE KEY-----|ssh-(rsa|ed25519|dss) [A-Za-z0-9+/=]{40,}|(op|onepassword|1password|vault|sops)://[A-Za-z0-9_-]+/|(password|passwd|passphrase|api[_-]?key|secret[_-]?key|client[_-]?secret|access[_-]?token|auth[_-]?token|private[_-]?key|session[_-]?id)[[:space:]]*[:=][[:space:]]*["']?[A-Za-z0-9/+=._-]{8,}|https?://(127\.0\.0\.1|localhost|10\.[0-9]|192\.168|172\.(1[6-9]|2[0-9]|3[01]))|https?://[A-Za-z0-9.-]+\.(internal|local|lan|corp)([/:]|$)|(sessionid|session_id|PHPSESSID|JSESSIONID)=[A-Za-z0-9%._-]{6,}|[?&](token|sig|signature|X-Amz-Signature|X-Goog-Signature|expires|access_token)=|Set-Cookie: [A-Za-z0-9_-]+=|file:/[//]/
PAT_END
```

Capture-shape probes (counts only, for a snapshot audit):

```
password_input  (?i)type\s*=\s*["']?password      pem            -----BEGIN [A-Z ]*PRIVATE KEY-----
set_cookie      (?i)\bSet-Cookie\b                sshkey         ssh-(rsa|ed25519|dss) [A-Za-z0-9+/=]{40,}
authorization   (?i)\bAuthorization\s*:           base64_120     [A-Za-z0-9+/]{120,}={0,2}
bearer          (?i)\bBearer\s+[A-Za-z0-9._-]{8,} ipv4           \b(\d{1,3}\.){3}\d{1,3}\b
mailto          (?i)mailto:                        form           (?i)<form\b
csrf            (?i)\b(csrf|xsrf)[_-]?token\b       session_param  (?i)\b(sessionid|session_id|phpsessid|jsessionid)\s*=
```

Two pattern notes worth keeping, because both cost a false result if dropped:

- `(?<![[:alnum:]_-])sk-` plus a mandatory digit is required: without it, the NCSC blog slug
  `…/10-questions-ask-using-ai-models-to-find-vulnerabilities` matched `sk-` in `questions-a**sk-**using…` in
  `corpus/SOURCES.md:15`, `corpus/knowledge/ai-assisted-finding-validation.md:2` and `corpus/lessons/round-22.md:85` —
  three false positives from a URL, no credential involved. With the boundary, lane-wide class `K` is exactly 0.
- `pypi-AgEIcHlwaS5vcmc` needs its own `{10,}` tail, or the redacted form in a negative fixture matches.

---

## 7. Reproduction, limits, scope

- **Every count above is reproducible** with the §2 command and the §6 pattern over the named paths; the classifier is
  the masked variant of the same 24 regexes (it also masks, so a hit is safe to look at without copying a value into a
  receipt). Costs nothing to run: 55+259+6 files in ~3 s.
- **Post-integration handoff (one command).** The content artifacts land after this sweep; the §2 gate is then the last
  check and its expected value is 0:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
PAT=$(sed -n '/^PAT_BEGIN$/,/^PAT_END$/p' .ufo/waves/round-37/wave1/SentSecrets.md | sed '1d;$d')
grep -rInP "$PAT" corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md corpus/SOURCES.md \
  corpus/lessons/round-37.md corpus/considerthese-ledger.md corpus/source-snapshots/round-37/ \
  corpus/QUALITY.md .ufo/waves/round-37/final-gates/all-gates.txt LOG.md SCORECARD.md SKILL.md \
  | wc -l   # expect 0
sha256sum corpus/source-snapshots/round-37/S054.txt    # must stay ff3f3b2c…fdce21 or §3 is void
```

  A citation of this receipt by section number (e.g. "`wave1/SentSecrets.md` §3") keeps the gate green; pasting a
  capture line into the entry is what the gate is for. **Absent is red:** while an artifact in that list does not exist,
  `grep` exits 2 for the missing operand — read that as "not yet proven clean", never as a pass (the same fail-closed
  shape the C1 suite's E9 limb had to be rewritten into).
- **Bounded claim.** "0 hits" here means: the classes in §6 over those bytes, at those paths, at `b362068` + the 7
  dirty entries. It is not a statement about a future re-fetch, about prose that names a secret without a value shape,
  or about binary/large files (all files in scope are UTF-8 text; the only non-text bytes in `.ufo/waves/round-37/` are
  none).
- **Not in scope and not done:** no network fetch, no rotation advice (nothing to rotate), no cross-lane scan, no
  reading of `~/.omp/agent/*`, no campaign tools in `shokuknow`. The 220-file `op://` string census is pattern text and
  prose, and this seat did not open any operator credential store to check anything.
- **Write scope honoured.** This receipt is the only lane file this seat wrote. All fixtures, extracted capture bytes
  and the scanner lived in `/fast/scratch/hyaku/kasegi-r37/SentSecrets/` and were removed at yield after the receipt
  was written (`rm -rf`); no `git`/`jj` mutating command was run (read-only `status`, `diff`, `rev-parse`, `ls-files`
  only); no `pacman`/`uv`/`npx`/install; no `agent://all` message; no swarm.
- **Adjacent, not adjudicated here:** the C1 suite's E10/E14 limb bytes, the C2 binding rows, and the frozen predicate's
  stale home-page URL literal are other seats' surfaces; §3 and O4 only report what the bytes say.
