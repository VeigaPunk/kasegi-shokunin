# SentinelSecretsScan — kasegi round 39, wave 2 (falsify): credential-material scan

Leaf attack seat. I did not author any round-39 deliverable; the C1/C2 landed bytes and the frozen
predicates are adversarial targets, not my work. Read-only in the lane except this receipt and its
deliverable. Host clock used throughout (UTC).

Deliverable: `.ufo/waves/round-39/wave2/SentinelSecretsScan.secrets.txt` — verdict **0 credential hits**.
Axes touched: `depth:verifiability` (a negative claim is only worth the scan behind it, so the scan is
published with its controls and its limits), `coverage` (the C2 surface — SOURCES rows and the new
knowledge/lesson files — is the most plausible place for a leaked token to sit).

## Scope as executed

Target set: **309 paths, 4,962,773 bytes** —
296 files under `.ufo/waves/round-39/**` (wave1 receipts + deliverables + fixtures, wave2 as-of-snapshot,
`final-gates/`, `c1-controls/`, `c2-controls/`, `declared-blocks.txt`, `claims*.json`,
`claims-erratum-1.md`, spec/dispatch/plan/results JSON, `__pycache__/*.pyc`) plus 13 new-or-changed
committed lane files (`corpus/knowledge/cisa-when-to-issue-vex.md`, `corpus/lessons/round-39.md`,
`corpus/SOURCES.md`, `corpus/README.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `PROVINCE.md`,
`corpus/instruments/r39-closure.sh`, `corpus/knowledge/considerthese-proposals-ledger.md`,
`corpus/QUALITY.md`, `corpus/source-snapshots/round-39/S057.txt`,
`corpus/source-snapshots/round-39/manifest.json`).

Lane head at scan: `5006097a84305267c9a3e8c1e1d560e60fe41d37`. Tracked working tree clean
(`git status --porcelain --untracked-files=no` → empty), so every tracked path scanned on disk equals
its committed bytes. Wave-2 files were untracked and still landing while the scan ran (§7 of the
deliverable); five passes were taken and the last (20:21:04Z) is authoritative — pass log in §7
of the deliverable. Files landing after 20:21:04Z are outside the snapshot.

Self-exclusion: `.ufo/waves/round-39/wave2/SentinelSecretsScan.*` is excluded from the target set
because the report prose necessarily spells out the pattern vocabulary. Keeping it in (measured at
20:17:53Z) produces 21 self-matches — `id_rsa`, `id_ed25519`, `.netrc`, `PGPASSWORD`, `GH_TOKEN`,
`localhost`, `127.0.0.1`, `scheme://user:pass@`, `client-key-data` at
`SentinelSecretsScan.secrets.txt:24,26,28,29,30,83,85,126` — and **zero** matches anywhere else. That
is a live positive control on real on-disk bytes, not a fixture.

## Method

30 credential patterns (op:// references, cloud/VCS/CI token prefixes, JWTs, PEM blocks, ssh key paths,
`.netrc`, cookie/session/authorization headers, generic secret assignments, URL userinfo, RFC1918 and
`.internal/.lan` hosts, secretish query params, DB/broker connection strings, `*_PROXY` with credentials,
credential env vars, JSON secret kv, basic-auth b64, kubeconfig key material) **+** a secret-shaped
high-entropy filter (≥28 chars, entropy ≥4.0, mixed case + digit, non-hex, path/slug rejection) **+** a
printable-base64 decoder (≥40 chars, entropy ≥4.2, decoded payload >90 % printable ASCII) **+** a
provider env-name sweep (`OPENAI|ANTHROPIC|ELEVENLABS|ZENROWS|SCRAPERAPI|SERPAPI|APIFY|NOTION|SLACK|…
_(API_KEY|TOKEN|SECRET|PASSWORD|KEY|PAT)`) **+** a credential-store filename sweep (`.env`, `.netrc`,
`id_rsa`, `credentials`, `*.pem|*.key|*.p12|*.pfx`, `kubeconfig`, `.npmrc`, `.pypirc`,
`.git-credentials`, `cookies.txt`) **+** a `grep -a` sweep of the two binary `.pyc` files the text pass
skips. Scanner source is reproduced verbatim in the Appendix so any seat can re-run it.

## Evidence — commands and actual output

### 1. Production pass (authoritative snapshot 2026-10-26T20:21:04Z)

```
$ python3 scan.py $(find /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-39 -type f \
      ! -name 'SentinelSecretsScan.*' | sort) \
    <the 13 committed lane files listed above>
SUMMARY files=309 scanned=307 skipped=2 pattern_hits=0 entropy_candidates=82 b64_printable=0
```
`grep -c '^HIT' final4-scan.txt` → `0`. Skipped = the 2 `.pyc`, swept separately below.

### 2. The only loose matches for the queried shapes (`op://`), all benign

```
$ grep -rnoE 'op://[^ "'"'"'<>]{0,40}' "$L/.ufo/waves/round-39" \
    "$L/corpus/knowledge/cisa-when-to-issue-vex.md" "$L/corpus/lessons/round-39.md" \
    --exclude='SentinelSecretsScan.*'
.ufo/waves/round-39/items2.py:69:op://`
.ufo/waves/round-39/__pycache__/items2.cpython-314.pyc:6:op://`
.ufo/waves/round-39/wave2-dispatch.json:581:op://`
.ufo/waves/round-39/wave2-plan.out:586:op://`
.ufo/waves/round-39/wave2/ScoutL0Open.l0.txt:12:op://
.ufo/waves/round-39/wave2/ScoutL0Open.md:17:op://
.ufo/waves/round-39/wave2-spec.json:313:op://`
```
Six are the literal token `op://`` inside the wave-2 item spec (the text that *asks for* this scan);
`ScoutL0Open.md:17` and `ScoutL0Open.l0.txt:12` are prose ("CORPUS.md op:// count", "Rule 8 op://
count") quoting another lane's open question. **No occurrence has the credential-reference shape
`op://<vault>/<item>/<field>`.** Token-prefix shapes (`sk-`, `ghp_`, `AKIA`, `xox`, `glpat`, `eyJ…`,
`BEGIN … PRIVATE KEY`, `Bearer`, `Cookie`, `~/.ssh`) occur **0** times in the 307 text files.

### 3. Entropy candidates — 82, every one classified

**Public URL paths (53):** `gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c` ×37,
`gov/sites/default/files/publications/VEX_Status_Justification_Jun22` ×9,
`/sites/default/files/2023-11/When-to-Issue-a-VEX-508c` ×2, `/2023-11/When-to-Issue-a-VEX-508c` ×2,
`gov/nistpubs/Legacy/SP/nistspecialpublication800-115`,
`com/repos/VeigaPunk/kasegi-shokunin/commits/66703aca…` and `/repos/VeigaPunk/…/66703aca…`.
**Git object ids / digests (15):** `PIN_REF=2387dcf6…` ×4, `PIN_R37_SHA=0da98e37…` ×3,
`PIN_R37_SHA=1da98e37…` (single-hex mutation of the pin, from a mutation seat's probe),
`BASE_REF=480b1a50…` ×2, `PIN_REF=480b1a50…`, `PIN_REF=aeddcd2e…`, `HEAD=5006097a…` ×2,
`HEAD=d65d823e…`. **Scratch / fixture paths (3):** `/var/tmp/souji-r18-FixtureR18Bounded` ×2 (sibling
lane's scratch) and `/home/vgpnk/Projects/the-bounty-hunter/S057`
(`wave2/ScoutInstrumentState.state.md:50` — an operator path naming a sibling project directory; a path,
not a URL and not a credential). **Labels, symbols, metrics (7):** `naming_deviation=RevControls-2`,
`kasegi-r39/RevControls=False|True|-2/base/` (4 forms), `heavy_consumers_mb_ge_100=…`,
`capture/quote/row/…/census-E12`, `BANNED/PARKED/K3/TELEMETRY_EVENTS/gitMutationBlocker`.
**Fixture identity (2):** `GIT_COMMITTER_NAME=g1fixture`, `GIT_COMMITTER_EMAIL=g1fixture`.
**Archive dir name (1):** `evidence/hackerone-1password/fetch-evidence/graphql-request-20260905T165623Z`.
**Probe label (1):** `Q2_under_investigation_lifecycle`. **None is an opaque credential.** Printable
base64 blobs: **0**.

The single env-name-shaped match in the lane docs is `LOG.md:612` — `` `K3_SEATS :9`/`K3_TOKEN :11` `` —
a code span naming a symbol plus a line number inside a review of a validator, not an assignment.

### 4. SOURCES rows carry no credentials (C2 surface)

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
59
```
59 rows, 59 `http(s)` URLs (one per row), 462 URL mentions / 141 distinct across all artifacts at the
final pass. Flagged: userinfo **0**;
secretish query params (`token|key|sig|password|session|auth|code`) **0**; private hosts
(`localhost|127.0.0.1|10.|192.168.|172.16-31.|.internal|.local|.lan`) **0**; share links
(docs.google/drive/notion/sharepoint/dropbox/figma/slack files) **0**; presigned
(`X-Amz-Signature|X-Goog-Signature`) **0**; `.onion` **0**; concrete credentials in any cell **0**. The
four round-39 rows each carry exactly one public URL and no token — S057 CISA *When to Issue VEX*
(mined), S056 CISA *Minimum Requirements* (rejected), S058 OpenVEX spec (rejected), S059 CycloneDX 1.7
(rejected). `app.devin.ai` appears once in `LOG.md:1110` as a public org wiki link with `?branch=master`
only. `example.invalid` ×2 are the deliberate fixture host in `wave1/CritFreezeAudit.md`.

### 5. Committed-diff coverage (independent of my file list)

```
$ git diff 480b1a505a2dfc14a4f718d16d63808247214d0a..HEAD   # 273 files, 30,412 added lines
```
Line-by-line with the same 30 patterns: 3 matches, all the `op://`` spec literal
(`items2.py:69`, `wave2-plan.out:586`, `wave2-spec.json:313`); 0 credential matches. Removed lines: no
additional matches.

### 6. Binary sweep of the two skipped files

```
$ grep -aoE '(op://…|gh[pousr]_…|sk-…|AKIA…|eyJ…\…)' .ufo/waves/round-39/__pycache__/*.pyc | sort | uniq -c
      1 …/__pycache__/items2.cpython-314.pyc:op://` refs, tokens (sk-, ghp_, AKI
```
Only the compiled copy of the spec literal. No key material in either `.pyc`.

## Controls (run before the production pass; §5 of the deliverable)

- **Positive** — synthetic fixture with one value per family: **30/30** pattern families fired, 35 HIT
  rows, 1 entropy candidate, 1 printable-base64 blob decoded
  (`QWxsWW91ckJhc2U2NFNlY3JldHNBcmVCZWxvbmdUb1VzWm9vbQ==` → `AllYourBase64SecretsAreBelongToUsZoom`).
- **Negative** — clean prose fixture (public URLs, a sha256 digest, an absolute lane path): **0** HIT
  rows, 0 entropy candidates, 0 b64 blobs. The digest and the `/home/vgpnk` path were *not* reported, so
  the engine is not merely "flag every long string".
- **Self** — 21 vocabulary self-matches and 0 others when my own report is included (see Scope).
- **Binary** — `.pyc` sweep above.

## Findings

**No credential material in the round-39 artifacts.** No `op://` reference of the
`op://vault/item/field` shape, no cloud/VCS/CI tokens, no session cookies or `Authorization` headers, no
private keys, no `~/.ssh`/`.netrc`/kubeconfig/`.npmrc`/`.pypirc`/`.git-credentials` paths, no URLs with
userinfo or secret-bearing query parameters, no RFC1918/localhost/`.internal` hosts, and no printable
base64 payloads. The C2 registry rows — the surface most likely to acquire a leaked token, because rows
quote fetch ledgers and capture digests — are clean across all 59 rows.

Severity: none (no exposure). The nearest thing to a disclosure is the operator username inside absolute
paths (`/home/vgpnk/…`) and the GitHub owner `VeigaPunk`; that is identity, not a credential, and it is
unavoidable in a lane whose receipts quote repo paths.

Impact if the scan were absent: the lane would still be clean *today*, but the hygiene property is
unverified — the round-39 wave files are the first artifacts in this lane to embed third-party fetch
ledgers and multi-seat receipts wholesale, so an inherited token pasted into a receipt would persist in
git with no gate looking for it.

Smallest remediation: none required for this round. If the property is to be *sustained* rather than
spot-checked, the cheapest durable move is a `--secrets` limb on the existing
`corpus/instruments/r39-closure.sh` pattern (a `grep -RFf` deny-list over the export plus the two
`grep -a` binary sweeps), which would make "no credential material" a closure check instead of a
per-round seat duty — that is a proposal, not a request, and it is out of this seat's write scope.

## Limits (stated, not claimed away)

- A credential consisting only of lowercase hex (32/40/64) is indistinguishable from the digests this
  lane stores in thousands of places and would pass the entropy filter. Every real credential form
  carries a prefix or a labelling context and those patterns are live (30/30 control); a leaked bare
  random hex string with no label would be missed. No such string with a credential label exists here.
- Scope is the round-39 target set plus the round-39 committed diff. Lane history before base
  `480b1a50` was not re-scanned.
- No file in the target set is a symlink (`find -type l`: none), so no artifact resolves outside the lane.
- The `__pycache__` sweep is string-shaped (`grep -a`), not a structural `.pyc` disassembly; a secret
  stored as a non-ASCII constant would be invisible to it. Both `.pyc` files are compiled copies of the
  two wave-2 spec builders, which were scanned as source.

## Adjacent observation (not my item, flagged for the C2 critics)

In `corpus/SOURCES.md` the round-39 rows are ordered **S055, S057, S056, S058, S059** — the mined row
precedes the first rejected row, so "S056/S058/S059 appended" reads as S057 inserted before S056. Row
count (59) and every counter in the C2 predicate are unaffected; only the append order differs from the
predicate's phrasing. Recorded, not judged.

## Tooling and scratch

No tool installs or upgrades (nothing needed; `python3`, `grep`, `find`, read-only `git` sufficed).
Scratch `/fast/scratch/hyaku/kasegi-r39/SentinelSecretsScan` held only the scanner, its control fixtures
and the captured scan outputs; it was removed after the receipt and deliverable were copied into the
wave dir. No mutating git/jj command was run anywhere; no writes outside this seat's receipt, deliverable
and scratch.

## Appendix — scanner source (verbatim, re-runnable)

```python
#!/usr/bin/env python3
"""kasegi round-39 secrets scan (seat SentinelSecretsScan).
Usage: scan.py <root> [<extra file>...]  -> prints HIT lines + summary.
Patterns cover: op:// refs, cloud/VCS/CI token prefixes, JWTs, PEM blocks,
ssh key paths, cookie/session/authorization headers, generic secret
assignments, URL userinfo, private hosts, secretish query params,
connection strings, proxy/credential env dumps, printable base64 blobs,
and secret-shaped high-entropy tokens (>=28 chars, entropy>=4.0).
"""
import os, re, sys, math, base64
from collections import Counter

PATTERNS = [
 ("op_ref", r"op://[^\s\"'<>`]+"),
 ("github_token", r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b|\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
 ("generic_sk", r"\bsk-[A-Za-z0-9][A-Za-z0-9_\-]{15,}\b"),
 ("stripe_live", r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}\b"),
 ("slack_token", r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"),
 ("gitlab_pat", r"\bglpat-[A-Za-z0-9_\-]{16,}\b"),
 ("aws_access_key", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
 ("aws_secret_ctx", r"(?i)aws_?secret_?access_?key\s*[:=]\s*\S+"),
 ("google_api_key", r"\bAIza[0-9A-Za-z_\-]{35}\b"),
 ("npm_token", r"\bnpm_[A-Za-z0-9]{30,}\b"),
 ("docker_pat", r"\bdckr_pat_[A-Za-z0-9_\-]{16,}\b"),
 ("pypi_token", r"\bpypi-[A-Za-z0-9_\-]{30,}\b"),
 ("hf_token", r"\bhf_[A-Za-z0-9]{30,}\b"),
 ("jwt", r"\beyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{4,}\b"),
 ("private_key_block", r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
 ("ssh_key_path", r"(?:~|\$HOME|\$\{HOME\})/\.ssh/[A-Za-z0-9_.\-]+|\bid_(?:rsa|ed25519|ecdsa|dsa)\b"),
 ("netrc", r"(?<![A-Za-z0-9_.\-])\.netrc(?![A-Za-z0-9_])"),
 ("cookie_header", r"(?i)(?:Set-Cookie|Cookie)\s*:"),
 ("session_cookie", r"(?i)\b(?:session(?:_?id|_?token|_?cookie)?|sessid|PHPSESSID|JSESSIONID|csrftoken)\s*[:=]\s*[A-Za-z0-9_\-+/=.]{8,}"),
 ("bearer_literal", r"(?i)\bbearer\s+[A-Za-z0-9_\-\.=:+/]{12,}"),
 ("generic_secret_assign", r"(?i)\b(?:password|passwd|passphrase|secret|client_secret|api[_-]?key|apikey|access[_-]?token|refresh[_-]?token|auth[_-]?token|private[_-]?key)\b\s*[:=]\s*[\"']?[A-Za-z0-9_\-./+=:@!]{10,}"),
 ("url_userinfo", r"\b[a-zA-Z][a-zA-Z0-9+.\-]*://[^/\s:@\"'<>`]+:[^/\s@\"'<>`]+@"),
 ("private_host", r"\b(?:localhost|127\.0\.0\.1|0\.0\.0\.0|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b|[A-Za-z0-9_\-]+\.(?:internal|lan|corp|home\.arpa)\b"),
 ("token_query", r"[?&](?:token|key|api_key|apikey|access_token|id_token|sig|signature|password)=(?!<)[A-Za-z0-9_\-%]{6,}"),
 ("conn_string", r"\b(?:postgres(?:ql)?|mysql|mariadb|mongodb(?:\+srv)?|rediss?|amqp|ftps?|sftp|ldaps?)://[^\s\"'<>]*@?[^\s\"'<>]*"),
 ("proxy_cred_env", r"(?i)\b(?:https?|all|ftp)_proxy\s*=\s*\S+://?[^\s]*"),
 ("cred_env_var", r"(?i)\b(?:PGPASSWORD|MYSQL_PWD|REDISCLI_AUTH|AWS_SESSION_TOKEN|GITHUB_TOKEN|GH_TOKEN|NPM_TOKEN|DOCKER_PASSWORD|VAULT_TOKEN)\b"),
 ("json_secret_kv", r"(?i)\"(?:password|secret|token|api_?key|authorization|cookie|credential)\"\s*:\s*\"[^\"]{6,}\""),
 ("basic_auth_b64", r"(?i)\bAuthorization:\s*Basic\s+[A-Za-z0-9+/=]{8,}"),
 ("kubeconfig_secret", r"(?i)\b(?:client-key-data|client-certificate-data)\b"),
]
SECRET_SHAPED = re.compile(r"[A-Za-z0-9+/=_\-]{28,}")
HEXONLY = re.compile(r"^[0-9a-f]+$")
WORDS = (".md",".txt",".sh",".json",".py",".tsv",".env","SCORECARD","PROVINCE","SHONEN","corpus","wave","scratch","work-",".git","claims","round-","dispatch","results","receipt","SEATNAME")
def H(s):
    c=Counter(s); n=len(s); return -sum(v/n*math.log2(v/n) for v in c.values())

def files_under(root):
    for r,d,fs in os.walk(root):
        for f in fs:
            p=os.path.join(r,f)
            if os.path.isfile(p) and not os.path.islink(p): yield p

def scan(paths):
    hits=[]; entropy=[]; b64=[]; scanned=0; skipped=[]
    for p in paths:
        try: raw=open(p,"rb").read()
        except OSError as e: skipped.append((p,"unreadable")); continue
        if b"\x00" in raw[:8000]: skipped.append((p,"binary")); continue
        scanned+=1
        txt=raw.decode("utf-8","replace")
        for i,line in enumerate(txt.splitlines(),1):
            for name,rx in PATTERNS:
                for m in re.finditer(rx,line):
                    hits.append((p,i,name,m.group(0)[:160]))
            for m in SECRET_SHAPED.finditer(line):
                t=m.group(0)
                if HEXONLY.match(t) or any(w in t for w in WORDS): continue
                if not (re.search(r"[A-Z]",t) and re.search(r"[a-z]",t) and re.search(r"[0-9]",t)): continue
                if H(t)>=4.0: entropy.append((p,i,round(H(t),2),t[:120]))
            for m in re.finditer(r"\b[A-Za-z0-9+/]{40,}={0,2}",line):
                t=m.group(0)
                if not (re.search(r"[A-Z]",t) and re.search(r"[a-z]",t) and re.search(r"[0-9]",t)): continue
                if H(t)<4.2: continue
                try:
                    d=base64.b64decode(t+"="*(-len(t)%4))
                    if sum(32<=b<127 or b in (9,10,13) for b in d)/max(1,len(d))>0.9:
                        b64.append((p,i,t[:80],d[:40]))
                except Exception: pass
    return hits,entropy,b64,scanned,skipped

if __name__=="__main__":
    roots=sys.argv[1:]
    paths=[]
    for r in roots:
        if os.path.isdir(r): paths.extend(sorted(files_under(r)))
        elif os.path.isfile(r): paths.append(r)
        else: print("MISSING",r)
    hits,entropy,b64,scanned,skipped=scan(paths)
    for h in hits: print("HIT\t%s\t%d\t%s\t%s"%h)
    for e in entropy: print("ENTROPY\t%s\t%d\tH=%s\t%s"%e)
    for b in b64: print("B64\t%s\t%d\t%s\t%r"%b)
    print("SUMMARY files=%d scanned=%d skipped=%d pattern_hits=%d entropy_candidates=%d b64_printable=%d"%(len(paths),scanned,len(skipped),len(hits),len(entropy),len(b64)))
```
