# Capture intake gate — a capture is scanned for credential shapes before its snapshot file is opened, a hit writes nothing and exits 3, one documented value passes only through a digest-bound allowlist row that carries a reason, and a gate that cannot run refuses

source: S131 — GitHub Docs, About push protection — https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection — anchor `corpus/source-snapshots/round-90/S131.txt:570` and `corpus/source-snapshots/round-90/S131.txt:610` (capture 647 lines, 20,549 bytes, sha256 0c98d69a14b33d3995f0d7748112f191dcac391157a6cb093054c346ff71fcc9; manifest `corpus/source-snapshots/round-90/manifest.json` records Q01-block-before at anchor 570 and Q02-bypass-reason at anchor 610, each `occurrences=1`); own work — `corpus/instruments/capture-source.py` read at `643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2` (sha256 0630d32b98d40bd07c4716b0062babfaa1a8cee6b8bb4103c582b71d41d53dbf) and `corpus/instruments/capture-secret-scan.py` at the same revision (sha256 95f24a541db8b3d6693315a03de28d0b6de0fb0b6e53a68471265382114d20ec); contrast only — S132, GitLab Docs, Secret push protection, a `rejected` row at `corpus/SOURCES.md:144`, quoted from the live page opened 2026-11-07 (no snapshot committed).

verified-at: 2026-11-07 (re-read at the pinned revision: `git show 643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2:corpus/instruments/capture-source.py | sha256sum` and the same for `capture-secret-scan.py` print the two digests above, and the working-tree copies print the same two digests; `python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-90/manifest.json --source S131` prints `S131:sha256 OK` plus two `Q0n … OK occurrences=1 anchor=N-ok` lines, rc 0; `python3 -B corpus/instruments/capture-source.py --selftest` prints `selftest normalize=ok deterministic=ok`, two `INTAKE-REFUSED SELFTEST … written=no` lines and `selftest intake-refuse=ok existing-kept=ok`, rc 0; the GitLab sentences in Claim 5 were read from the live page at HTTP 200)

recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-90/manifest.json --source S131 && python3 -B corpus/instruments/capture-source.py --selftest | grep -x 'selftest normalize=ok deterministic=ok' && python3 -B corpus/instruments/capture-source.py --selftest | grep -x 'selftest intake-refuse=ok existing-kept=ok'  # fails closed on a moved or rewritten snapshot, a conversion that stops being deterministic, or a gate that stops refusing

## Attribution

S131 is GitHub's own description of GitHub's push protection (`corpus/SOURCES.md:143`, tier A): every sentence here about blocking before the repository, about a bypass that carries a reason and about the alerts that record it is GitHub's statement about GitHub, not about any other vendor's protection. S132 is GitLab's page about GitLab's secret push protection, a `rejected` row (`corpus/SOURCES.md:144`) whose capture was never committed; every sentence in Claim 5 about a skip, a threshold or a diff-only scope is GitLab's statement about GitLab, quoted from the live page at https://docs.gitlab.com/user/application_security/secret_detection/secret_push_protection/ opened 2026-11-07, and it is cited only as the contrast case. `capture-source.py` and `capture-secret-scan.py` are the lane's own instruments: every sentence about the gate's order, refusal line, exit code, allowlist and limits is about those bytes at `643ddb43…`, not a vendor statement, and the shape set is a lane design choice.

## Claim 1 — a capture is the artifact the corpus later quotes, so the scan belongs before the write, not before the commit

> "Push protection is a secret scanning feature designed to prevent hardcoded credentials, such as secrets or tokens, from ever being pushed to your repository" — `corpus/source-snapshots/round-90/S131.txt:570`

> "Rather than alerting you to credential leaks after the fact" — `corpus/source-snapshots/round-90/S131.txt:570` (same line, next sentence)

> "push protection blocks pushes that contain secrets before they reach your repository" — `corpus/source-snapshots/round-90/S131.txt:570`

Lane reading: the property GitHub states is order — the block sits on the path the secret must travel, not on a review that happens afterwards. A capture is that kind of artifact here: a snapshot under `corpus/source-snapshots/` is the byte sequence a later entry quotes and a quote check re-reads, so a credential committed in one is committed at the only moment it could still be refused cheaply.

The lane's own instance is round 86's capture of a HackerOne report, committed and pushed with a live STS session token in it (`corpus/lessons/round-86.md:61`):

> "The JSON held two presigned profile-picture URLs with a HackerOne-issued AWS STS session token" — `corpus/lessons/round-86.md:61`

> "so the token was live when pushed" — `corpus/lessons/round-86.md:61`

> "no rule ran it over a capture before the freeze commit" — `corpus/lessons/round-86.md:62`

The scanner was the fix at the review end, and its docstring states the rule a seat had to remember (`corpus/instruments/capture-secret-scan.py:9-21`):

> "run it on every capture before the commit that first adds it" — `corpus/instruments/capture-secret-scan.py:20-21`

The intake gate turns that rule into a property of the writer: the same scanner, imported rather than copied, called from `capture()` on the snapshot bytes before the file is opened (`corpus/instruments/capture-source.py:20-26`). Round 87 named the shape of the change (`.ufo/waves/round-87/w1/ConnectorOverlap.md:158-176`), rounds 88 and 89 routed or declined it, and round 90 landed it as C2 (`.ufo/waves/round-90/l1/c2-landing-r90.txt:1`).

## Claim 2 — the gate reads the bytes that would be written, and it runs before the file is opened

Three facts from `capture()` (`corpus/instruments/capture-source.py:126-146`):

1. The gate is handed the converted snapshot bytes — `data = text.encode("utf-8")` then `found = intake_gate(data, out, allow_path)` (`:134-135`). What is scanned is exactly the byte sequence that would be written, so a clean run is a statement about the committed file, not about the served page.
2. Only after a non-refusal does the instrument create the directory and open the file — `os.makedirs(...)` then `with open(out, "wb") as fh:` (`:140-142`). The write is downstream of the gate, not beside it.
3. The scan key is the lane-relative `--out`, computed by `lane_rel()` (`:109-112`): inside the lane the path is relativized (`return p if rel.startswith("..") else rel`), outside it the absolute path is used. The key is the output path an allowlist row is written against, not the URL fetched.

`intake_gate()` is five statements (`:115-123`): load the scanner beside the instrument (`:118`), load the allowlist — the `--allow` path, else `capture-secret-allow.tsv` beside the instrument (`:119`) — call `scan_bytes(data, scan.patterns(), lane_rel(out), allow)` (`:120`), and return the `[(shape, line)]` list. The import happens inside the function, not at module import, so a missing scanner cannot break `--help`; it becomes a refusal on the capture that needs the gate (Claim 5).

## Claim 3 — a hit refuses the capture: nothing is written, an existing file is left byte-identical, the line names shape and position, and the exit code is 3

> "A hit refuses the capture: nothing is written" — `corpus/instruments/capture-source.py:23`

> "one INTAKE-REFUSED line per shape names the shape and line only (never the matched value)" — `corpus/instruments/capture-source.py:24-25`

The refusal is built so that reading it is safe: `scan_bytes()` returns `(shape, line)` pairs and never the match (`corpus/instruments/capture-secret-scan.py:159-160`, `:173`); the matched bytes are hashed only to form the allowlist key (`:167`) and are otherwise dropped. `capture()` loops over the pairs, prints `INTAKE-REFUSED <id> shape=<s> line=<n> out=<p> written=no` (`corpus/instruments/capture-source.py:136-139`) and returns `None`; `main()` maps `None` to `REFUSED_RC` = 3 (`:49`, `:192-193`). A single plant can produce more than one line when more than one shape matches the same bytes — the instrument's selftest prints two for one fixture (`:164-171`).

The kept-file half is proved by the instrument itself: the selftest writes `previous\n` to `out`, captures a planted page onto that path, and asserts the file still reads `b"previous\n"` (`corpus/instruments/capture-source.py:169-173`). At the landing, the counter reads `LIMB G1 pass plants=11 bad=none` and `LIMB G2 pass rc=3 kept=True` (`.ufo/waves/round-90/l1/c2-landing-r90.txt:5-6`), and a mutant that writes first keeps G1 passing while G2 and G6 fail (`.ufo/waves/round-90/controls/c2-controls-r90.txt:51-61`) — the ordering is tested by the existing-file assertion, not by the refusal.

## Claim 4 — a documented value passes only through a digest-bound row that carries a reason; that is the bypass analogue, made stricter

GitHub's bypass is a stated reason attached to a person's decision:

> "anyone with write access to the repository can bypass push protection by specifying a bypass reason" — `corpus/source-snapshots/round-90/S131.txt:610`

> "Adds the bypass event to the audit log" — `corpus/source-snapshots/round-90/S131.txt:612`

> "with a link to the secret and the reason it was allowed" — `corpus/source-snapshots/round-90/S131.txt:613`

Lane reading: the vendor's bypass records a decision after the secret has already travelled; the lane's analogue is a data row that decides nothing by itself:

> "A row binds one exact matched value at one path, so a different value at the same path and shape is still a hit" — `corpus/instruments/capture-secret-scan.py:72-73`

> "Rows for aws-sts-session-token are refused" — `corpus/instruments/capture-secret-scan.py:73`

The row is `path<TAB>shape<TAB>sha256-of-matched-bytes<TAB>reason`, and `load_allow()` refuses a row that is not four non-empty cells, names a never-allowed shape, or carries a non-sha256 third column (`corpus/instruments/capture-secret-scan.py:121-136`); the key is recomputed from the matched bytes at scan time (`:167`). So a rewrite of the same capture at the same path is a hit again, and the reason column documents the exemption for a reader instead of authorizing it.

The concrete instance is the two round-89 CloudFront rows (`corpus/instruments/capture-secret-allow.tsv:21-22`), which bind AWS's documentation example at its two snapshot paths. Ignore the allowlist and those very bytes refuse: control F4 reads `LIMB G3 FAIL clean=6 bad=corpus/source-snapshots/round-89/S128.txt(rc=3,base_rc=0,same=False)` and `LIMB G4 FAIL` (`.ufo/waves/round-90/controls/c2-controls-r90.txt:67-68`). Three differences from the vendor's bypass follow: the exemption cannot be a person's assertion (a digest must match), cannot be written for a session token at all (`:117`, `:132-133`), and cannot travel to another path or another value (`:72-73`).

## Claim 5 — the gate refuses when it cannot run; GitLab's documented design skips the scan instead, and the difference is the guarantee

GitLab states its skips and its scope on the page this lane's S132 row points at (live page, https://docs.gitlab.com/user/application_security/secret_detection/secret_push_protection/, opened 2026-11-07; S132 is a `rejected` row, `corpus/SOURCES.md:144`, no snapshot committed):

> "Secret push protection does not block a secret when:" — live GitLab page

> "Secret push protection is skipped because a push contains too many changed paths." — live GitLab page

> "Secret push protection is skipped because the scan received invalid input." — live GitLab page

> "Secret push protection scan timeout occurs and GitLab accepts the push." — live GitLab page

> "Secret push protection is skipped when a push changes more than 3,150 paths or 350,000 lines." — live GitLab page

> "These thresholds prevent push timeouts when you push large changesets." — live GitLab page

> "Secret push protection scans only the diffs of commits pushed over HTTP(S) and SSH." — live GitLab page

> "If a secret is already present in a file and not part of the changes, it is not detected." — live GitLab page

Lane reading: on GitLab's own page the documented behavior is fail-open on size, timeout and invalid input — a push the product could not scan is accepted — and the scan is diff-scoped, so unchanged bytes are out of scope. That is a product decision for a push path, where refusing a large push has its own cost. The intake gate answers a narrower question and refuses the other way:

> "except Exception as e:  # fail closed: a gate that cannot run refuses" — `corpus/instruments/capture-source.py:122`

The failure is shaped like a hit so a caller cannot read it as success: `intake_gate()` returns `[("gate-error:<Type>", 0)]` (`corpus/instruments/capture-source.py:123`), the loop prints it with `line=0` (`:136-138`), and `main()` exits 3 (`:192-193`). There is no size threshold and no timeout branch in the gate: the only bound is `MAX_FETCH_BYTES = 32 * 1024 * 1024` (`:52`), enforced after the fetch and before conversion (`:94-98`), so an oversized response aborts before the gate and before any write. The counter's G5 removes the scanner from the tree and captures a clean input: `LIMB G5 pass rc=3 written=False` (`.ufo/waves/round-90/l1/c2-landing-r90.txt:9`). A lane that imported GitLab's skip list would drop the guarantee for exactly the inputs the gate was added to cover.

## Claim 6 — what the gate cannot see, and what a clean run does not mean

The shape set is the scanner's `patterns()` — the claim-package gate's six `SECRET_PATTERNS` plus two AWS shapes plus three cloud shapes (`corpus/instruments/capture-secret-scan.py:139-148`): `private-key`, `op-ref`, `bearer`, `authorization`, `credential`, `session-cookie`, `aws-sts-session-token`, `aws-access-key-id`, `gcs-signed-url-signature`, `azure-sas-signature`, `cloudfront-signed-url-signature` — eleven names, which the counter derives from the scanner rather than restating (`LIMB G0 pass shapes=11 missing=none extra=none`, `.ufo/waves/round-90/l1/c2-landing-r90.txt:4`).

The docstring's named limits reach the gate unchanged (`corpus/instruments/capture-secret-scan.py:61-65`):

> "GCS V2 `GoogleAccessId=`/`Signature=` URLs, CloudFront signed cookies (`CloudFront-Signature`), percent-encoded parameter names or `=`" — `corpus/instruments/capture-secret-scan.py:61-62`

> "more than 20 other parameters between the two matched ones, values soft-wrapped across lines" — `corpus/instruments/capture-secret-scan.py:63-64`

Six further properties hold at the landing revision, and each is a reason a clean run is not a clearance:

- the bounds are shape-sized: 64+ hex digits after `X-Goog-Signature` (`:109-110`), 40+ `sig=` characters beside an `sv=YYYY-MM-DD` parameter (`:101-102`, `:111-112`), 40+ `Signature=` characters beside an 8-32 character `Key-Pair-Id=`, parameter names case-sensitive (`:104-107`, `:113-114`);
- `%26` is a left boundary only, not a separator inside a match (`:99`, `:103-104`), so a query whose parameters are joined by `%26` is not spanned;
- an allowlist key is `(path, shape, sha256)` (`:167`), and an `--out` outside the lane is scanned under its absolute path (`corpus/instruments/capture-source.py:109-112`), so a row written for a lane-relative path cannot bind that capture;
- the gate covers only writes made by this instrument: a seat that writes a snapshot with `curl` and an editor never reaches it, and there the scanner's manual rule is the only control (`corpus/instruments/capture-secret-scan.py:19-21`);
- the gate reads the converted text, not the served bytes — in the default `html` path the converter drops `<script>`/`<style>` bodies and every tag before the gate runs (`corpus/instruments/capture-source.py:53`, `:67-72`), so a value that appears only inside a stripped tag is neither scanned nor written: no leak, and nothing for the gate to report; `--kind text` keeps the served text as collapsed lines and is scanned as such (`:130-131`)
- the instrument's own selftest cannot tell a hit from a broken scanner: it asserts only that the capture refused and the file was kept (`:169-173`), and a `gate-error` refusal satisfies both. The counter separates them — G1 requires the shape to be named, G5 requires a clean input to refuse when the scanner is removed (`.ufo/waves/round-90/l1/c2-landing-r90.txt:5`, `:9`).

So a clean run means "no shape at these bounds matched these bytes" and a hit means "a shape matched", not "the value is live": the vendor placeholders `azure-doc-placeholder` and `cf-doc-placeholder` are pinned as clean (`corpus/instruments/capture-secret-scan.py:269`, `:277`), and a long enough placeholder is indistinguishable from a live value.

## How a seat uses it

1. Capture with the instrument, never with an editor: `python3 -B corpus/instruments/capture-source.py --id SNNN --url URL --out corpus/source-snapshots/round-NN/SNNN.txt` (`corpus/instruments/capture-source.py:5-6`).
2. Read the exit code before reading the file: 0 means written, with the sha256 printed (`:143-145`); 3 means refused, and the `INTAKE-REFUSED` lines name the shape and line to open (`:136-139`). A refusal is a fact about the bytes, not an obstacle.
3. To admit a documented value, add one row — `path<TAB>shape<TAB>sha256-of-matched-bytes<TAB>reason` — with the digest of the exact matched bytes and a reason a reader can check (`corpus/instruments/capture-secret-scan.py:68-75`); never add a row for `aws-sts-session-token` (`:73`, `:117`, `:132-133`).
4. If the instrument is edited, run `--selftest`, then the counter: the selftest proves determinism and the kept file, not that the gate still names a shape (Claim 6).
5. Keep the commit-time scan: `--rev`/`--files` remains the check for captures that did not come through the instrument (`corpus/instruments/capture-secret-scan.py:14-21`).

## Falsifiable rule and checks

**Falsifiable rule.** Any sentence asserting that a capture written by `corpus/instruments/capture-source.py` is scanned only after it is written is falsified by `corpus/instruments/capture-source.py:135-142` (the gate call precedes `open(out, "wb")`) and by the F3-write-then-check control, which fails G2 and G6 (`.ufo/waves/round-90/controls/c2-controls-r90.txt:51-61`). Any sentence asserting that a hit can alter an existing `--out` is falsified by the selftest's kept assertion (`corpus/instruments/capture-source.py:169-173`) and by `LIMB G2 pass rc=3 kept=True`. Any sentence asserting that a clean run proves a capture credential-free is falsified by the shape set and limits (`corpus/instruments/capture-secret-scan.py:23-65`). Any sentence asserting that the gate skips a capture above a size threshold is falsified by `corpus/instruments/capture-source.py:115-123`, which returns only a hit list, and `:136-142`, which has no size branch.

**FC-1 — every S131 quote is verbatim, anchored, within 25 words and occurs the declared number of times (`normalized=whitespace`).**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B - <<'PY'
def norm(s): return ' '.join(s.split())
Q = [
 ('S131','corpus/source-snapshots/round-90/S131.txt',570,570,1,"Push protection is a secret scanning feature designed to prevent hardcoded credentials, such as secrets or tokens, from ever being pushed to your repository"),
 ('S131','corpus/source-snapshots/round-90/S131.txt',570,570,1,"Rather than alerting you to credential leaks after the fact"),
 ('S131','corpus/source-snapshots/round-90/S131.txt',570,570,1,"push protection blocks pushes that contain secrets before they reach your repository"),
 ('S131','corpus/source-snapshots/round-90/S131.txt',610,610,1,"anyone with write access to the repository can bypass push protection by specifying a bypass reason"),
 ('S131','corpus/source-snapshots/round-90/S131.txt',612,612,1,"Adds the bypass event to the audit log"),
 ('S131','corpus/source-snapshots/round-90/S131.txt',613,613,1,"with a link to the secret and the reason it was allowed"),
]
bad = 0
for sid, p, a, b, want, q in Q:
    raw = open(p, encoding='utf-8').read().split('\n')
    n = norm('\n'.join(raw)); nq = norm(q)
    got = n.count(nq); span = norm('\n'.join(raw[a-1:b]))
    ok = got == want and nq[:40] in span and len(nq.split()) <= 25
    bad += not ok
    print('%s:%d-%d occurrences=%d expected=%d anchored=%s words=%d %s'
          % (sid, a, b, got, want, 'y' if nq[:40] in span else 'n', len(nq.split()), 'OK' if ok else 'FAIL'))
print('QUOTE-CHECK %s spans=%d bad=%d' % ('pass' if not bad else 'fail', len(Q), bad))
raise SystemExit(1 if bad else 0)
PY
```

Measured 2026-11-07: six `OK` lines and `QUOTE-CHECK pass spans=6 bad=0`, rc 0.

**FC-2 — every instrument quote and every cited span resolves at the anchor revision, and the two digests are the pinned ones.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
REV=643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2
git show "$REV":corpus/instruments/capture-source.py | sha256sum
git show "$REV":corpus/instruments/capture-secret-scan.py | sha256sum
git show "$REV":corpus/instruments/capture-source.py | sed -n '23p;24,25p;109,112p;115,123p;134,142p;169,173p;192,193p'
git show "$REV":corpus/instruments/capture-secret-scan.py | sed -n '61,65p;72,75p;99,118p;139,148p;159,175p'
python3 -B corpus/instruments/anchorcheck.py .ufo/waves/round-90/w1/ScribeEntry-receipts/capture-intake-gate.md
```

Measured 2026-11-07: the two digests are `0630d32b…` and `95f24a54…`, the printed spans are the lines Claim 2 through Claim 6 quote, and `anchorcheck.py` prints `0 bad` on this draft (FC-6).

**FC-3 — the gate refuses and keeps an existing file, on the instrument's own bytes.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
T=$(mktemp -d) || exit 9
TMPDIR="$T" python3 -B corpus/instruments/capture-source.py --selftest; echo "selftest_rc=$?"
rm -rf -- "$T"
```

Measured 2026-11-07: `selftest normalize=ok deterministic=ok`, two `INTAKE-REFUSED SELFTEST … written=no` lines (`shape=credential` and `shape=aws-sts-session-token`), `selftest intake-refuse=ok existing-kept=ok`, `selftest_rc=0`.

**FC-4 — the counter passes at the landing (read from the landing receipt; re-runnable with the frozen counter).**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B .ufo/waves/round-90/c2/capability-check.py --lane . --rev 643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2 \
  --base-rev 6088c3eb0c29040415c69e7b5fb91e110480ab26 --work "$(mktemp -d)" \
  --instrument-sha256 0630d32b98d40bd07c4716b0062babfaa1a8cee6b8bb4103c582b71d41d53dbf
```

Measured at the landing on 2026-11-07 at three seeds: `CAPABILITY-CHECK-RESULT pass rc=0` with G0-G6 and P (`LIMB G0 pass shapes=11 missing=none extra=none`, `LIMB G1 pass plants=11 bad=none`, `LIMB G2 pass rc=3 kept=True`, `LIMB G3 pass clean=6 bad=none`, `LIMB G4 pass allowed_rc=0 written=True other_path_rc=3 never_allowed_rc=3`, `LIMB G5 pass rc=3 written=False`, `LIMB G6 pass rc=0 selftest normalize=ok deterministic=ok …`, `LIMB P pass sha256=0630d32b…`), `.ufo/waves/round-90/l1/c2-landing-r90.txt:3-12`, `:15-24`, `:27-36`. Not re-run for this entry.

**FC-5 — the GitLab contrast sentences are on the live page (network; the only network check here).**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B - <<'PY'
import html, re, urllib.request
URL = "https://docs.gitlab.com/user/application_security/secret_detection/secret_push_protection/"
req = urllib.request.Request(URL, headers={"User-Agent": "kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)"})
raw = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
t = re.sub(r"<(script|style)\b.*?</\1>", " ", raw, flags=re.I | re.S)
t = re.sub(r"</(p|div|li|tr|h[1-6]|section|article|br)>", "\n", t, flags=re.I)
t = re.sub(r"<br\s*/?>", "\n", t, flags=re.I)
t = html.unescape(re.sub(r"<[^>]+>", "", t))
n = " ".join((" ".join(l.split()) for l in t.split("\n")))
Q = ["Secret push protection does not block a secret when:",
     "Secret push protection is skipped because a push contains too many changed paths.",
     "Secret push protection is skipped because the scan received invalid input.",
     "Secret push protection scan timeout occurs and GitLab accepts the push.",
     "Secret push protection is skipped when a push changes more than 3,150 paths or 350,000 lines.",
     "These thresholds prevent push timeouts when you push large changesets.",
     "Secret push protection scans only the diffs of commits pushed over HTTP(S) and SSH.",
     "If a secret is already present in a file and not part of the changes, it is not detected."]
bad = 0
for q in Q:
    got = n.count(" ".join(q.split())); bad += got != 1
    print('GITLAB occurrences=%d expected=1 words=%d %s' % (got, len(q.split()), 'OK' if got == 1 else 'FAIL'))
print('GITLAB-CHECK %s spans=%d bad=%d' % ('pass' if not bad else 'fail', len(Q), bad))
raise SystemExit(1 if bad else 0)
PY
```

Measured 2026-11-07: HTTP 200, eight `OK` lines and `GITLAB-CHECK pass spans=8 bad=0`, rc 0. The page changes; a changed sentence fails this check rather than being silently re-anchored, which is why S132 stays `rejected` and no snapshot is claimed for it.

**FC-6 — every `path:line` citation in this entry resolves.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B corpus/instruments/anchorcheck.py .ufo/waves/round-90/w1/ScribeEntry-receipts/capture-intake-gate.md
```

Measured 2026-11-07: `== …capture-intake-gate.md: N in-range cite instances, 0 bad; …` — every instrument, snapshot, receipt and lesson cite resolves; no MISSING-FILE, PAST-EOF or OUTSIDE-BASE.

## Rejected over-generalizations

1. **"A clean capture is credential-free."** Rejected: the gate runs eleven shapes at fixed bounds over the converted text (`corpus/instruments/capture-secret-scan.py:61-65`, `:139-148`); a clean run says no shape matched (Claim 6).
2. **"The gate covers every credential shape that exists."** It covers exactly the shapes `patterns()` returns at run time (`corpus/instruments/capture-source.py:120`), so the gate and the scanner cannot drift; that does not make the set complete — the docstring names shapes outside it (`corpus/instruments/capture-secret-scan.py:61-65`).
3. **"An allowlist row is a general exemption for a path."** Rejected: the row binds one exact matched value at one path (`corpus/instruments/capture-secret-scan.py:72-73`), and the key includes the sha256 of the matched bytes (`:167`).
4. **"The gate can be bypassed with a reason, like GitHub's."** Rejected: GitHub's bypass is a writer's decision recorded in an alert and an audit log (`corpus/source-snapshots/round-90/S131.txt:610-613`); the lane's row decides nothing by itself, must match a digest, and is refused outright for a session token (`corpus/instruments/capture-secret-scan.py:73`, `:117`, `:132-133`).
5. **"GitLab's skip thresholds are the lane's thresholds."** Rejected: they are GitLab's statement about GitLab (live page, Claim 5); the gate has no size threshold and no timeout branch (`corpus/instruments/capture-source.py:115-123`), and its only bound is the fetch cap (`:52`, `:94-98`).
6. **"The intake gate is equivalent to push protection."** Rejected: it guards one instrument's write path, prints to stdout, keeps no alert or audit record and has no user-level or repository-level protection (`corpus/instruments/capture-source.py:136-139`).
7. **"INTAKE-REFUSED proves the capture carried a live credential."** Rejected: it proves a shape matched at fixed bounds (`corpus/instruments/capture-secret-scan.py:101-114`); the vendor placeholders are pinned as clean only because they are short (`:269`, `:277`), so the inverse reads are equally unsafe.
8. **"The gate runs after the write and removes the file on a hit."** Rejected by the call order (`corpus/instruments/capture-source.py:135-142`) and by the F3 mutant, which keeps G1 green and fails G2 and G6 (`.ufo/waves/round-90/controls/c2-controls-r90.txt:51-61`).

## Honest limit

- **No live capture was refused by me for this entry.** The refusal evidence is the instrument's selftest (FC-3) and the landing receipt's G1/G2/G5 (FC-4), both produced by seats that ran them; I re-read the bytes and the receipt, and ran only the selftest.
- **S132 has no committed bytes.** Its capture was never committed (`corpus/SOURCES.md:144`), so the contrast is quoted from the live page, re-checkable only by network (FC-5); it is not an anchored lane fact and is marked as GitLab's statement throughout.
- **The landing receipt's numbers are cited, not re-derived.** FC-4 gives the counter command, but this entry does not re-run it; the counts (`plants=11`, `clean=6`, `shapes=11`) belong to `.ufo/waves/round-90/l1/c2-landing-r90.txt` at the landing revision.
- **The gate is a shape matcher with a path scope.** It scans the snapshot bytes of one instrument (`corpus/instruments/capture-source.py:134-135`); an allowlist row can only bind a path the gate computes (`:109-112`), and a capture written by hand is outside it.
- **The selftest is weaker than the counter.** It cannot distinguish a hit from a gate error (Claim 6, bullet 6); the counter's G1 and G5 are the discriminating limbs, and a reader who runs only `--selftest` is reading a weaker signal than the receipt.
- **No request was made to any host for this entry except the two documentation pages named above**: S131 was re-read from its committed snapshot through `source-recheck.py`, and the GitLab page was opened once, plain GET, 2026-11-07.
- **The instrument's own documentation is not evidence for the instrument.** The README row (`corpus/instruments/README.md:175-184`) states the gate's contract; every claim here is checked against the instrument's code at the anchor revision, not against the README.
