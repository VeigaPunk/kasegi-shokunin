# ScribeEntry — round 90 w1: candidate knowledge entry `capture-intake-gate`

Seat: ScribeEntry (scribe, leaf). No subagents, no background jobs. All reads; no lane edit, no git/jj write, no claim re-scoring.

## Behavior

Wrote one candidate knowledge entry, **not admitted into `corpus/`**:

- `.ufo/waves/round-90/w1/ScribeEntry-receipts/capture-intake-gate.md` — 263 lines, 30,193 bytes, sha256 `a71d99201fa014d99683e45de4ad497d1f1af2b43f469b74d11ca1a13113f23f`.

Shape follows the admitted sibling `corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md`: H1, the three provenance lines (`source:` / `verified-at:` / `recheck:` immediately under the title), `## Attribution`, seven claims each carrying located quotes, `## How a seat uses it`, `## Falsifiable rule and checks` (FC-1…FC-6), `## Rejected over-generalizations`, `## Honest limit`.

Content, per the seat spec:

1. **Why at intake** (Claim 1): S131:570's three statements (block before the repository, rather than alert after the fact) plus the lane's own M86-2 (`corpus/lessons/round-86.md:61-62`), the scanner's manual `--files` rule (`corpus/instruments/capture-secret-scan.py:20-21`), and the round-87 proposal / round-88-89 routing / round-90 landing lineage.
2. **The order that makes "before the write" true** (Claim 2): `capture()` converts, hands `data` to `intake_gate()`, and opens `--out` only after a non-refusal (`corpus/instruments/capture-source.py:134-142`); the scan key is `lane_rel(out)` (`:109-112`).
3. **Refusal shape** (Claim 3): nothing written, existing file byte-identical, one `INTAKE-REFUSED` line per shape naming shape and line only, exit 3 (`:23-25`, `:49`, `:136-139`, `:192-193`), proved by the selftest's kept assertion (`:169-173`) and the counter's G1/G2.
4. **The bypass-with-reason analogue** (Claim 4): S131:610/612/613 (a writer bypass, recorded in an alert and an audit log) against the digest-bound allowlist row `path<TAB>shape<TAB>sha256<TAB>reason` (`corpus/instruments/capture-secret-scan.py:68-75`, `:121-136`, `:167`), with the round-89 CloudFront rows (`corpus/instruments/capture-secret-allow.tsv:21-22`) and the F4 control as the concrete instance; `aws-sts-session-token` is never allowlistable (`:73`, `:117`).
5. **Fail-closed vs GitLab's documented skips** (Claim 5): eight sentences quoted from the **live** GitLab page opened 2026-11-07 (a `rejected` row, `corpus/SOURCES.md:144`, no snapshot committed — quoted only as the contrast), against `except Exception … fail closed` (`corpus/instruments/capture-source.py:117-123`) and the absence of any size/timeout branch.
6. **What the gate cannot see** (Claim 6): the eleven shapes, the docstring's named limits (`corpus/instruments/capture-secret-scan.py:61-65`), the pattern bounds, `%26` as boundary only, the absolute-path scan key for an out-of-lane `--out`, coverage limited to this instrument's writes, the post-conversion scan, and the selftest's inability to tell a hit from a gate error.
7. **Operating rule** and the falsifiable rule / checks / rejected over-generalizations / honest limit.

No credential-shaped value is written in the entry: it quotes line spans and the vendor's placeholder *names*, never a value. The entry's own hygiene scan reads clean (below).

## Gates run (read-only; measured 2026-11-07)

| # | command | result |
|---|---|---|
| 1 | `git show 643ddb43…:corpus/instruments/capture-source.py \| sha256sum` and the same for `capture-secret-scan.py` | `0630d32b98d40bd07c4716b0062babfaa1a8cee6b8bb4103c582b71d41d53dbf`, `95f24a541db8b3d6693315a03de28d0b6de0fb0b6e53a68471265382114d20ec`; working-tree copies print the same two digests |
| 2 | `python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-90/manifest.json --source S131` | `S131:sha256 OK`, `Q01-block-before OK occurrences=1 anchor=570-ok`, `Q02-bypass-reason OK occurrences=1 anchor=610-ok`, rc 0; `sha256sum` of S131.txt `0c98d69a…` |
| 3 | `TMPDIR=$S python3 -B corpus/instruments/capture-source.py --selftest` | `selftest normalize=ok deterministic=ok`, two `INTAKE-REFUSED SELFTEST … written=no` lines (`shape=credential`, `shape=aws-sts-session-token`), `selftest intake-refuse=ok existing-kept=ok`, rc 0 |
| 4 | quote checker over every `> "…" — cite` pair in the draft (whitespace-normalised, span-anchored, occurrence counted in the source file, ≤25 words) | 25 quotes, `ENTRY-QUOTE-CHECK pass quotes=25 bad=0`; the 8 GitLab quotes are ≤25 words and are checked live by FC-5 |
| 5 | `python3 -B corpus/instruments/anchorcheck.py .ufo/waves/round-90/w1/ScribeEntry-receipts/capture-intake-gate.md` | `69 in-range cite instances, 0 bad; 50 distinct anchors; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, rc 0 |
| 6 | `python3 -B corpus/instruments/capture-secret-scan.py --files .ufo/waves/round-90/w1/ScribeEntry-receipts/capture-intake-gate.md` | `CAPTURE-SECRET-SCAN mode=files scanned=1 hits=0 files=0 allowed=0 unused_allow=19 rc=0` |
| 7 | live `GET https://docs.gitlab.com/user/application_security/secret_detection/secret_push_protection/` (plain GET, UA of the capture instrument) | HTTP 200, 65,723 bytes; the eight quoted sentences each occur exactly once in the tag-stripped text |

The eight quote spans and the instrument spans are listed with their line text in the table at the end.

**Not run, by design:** the C2 counter (the entry cites its landing receipt lines; FC-4 carries the command), any C1 counter, any lane census, any claim re-verification. No live target was probed, scanned or logged in to.

## Touched surfaces

- Wrote `.ufo/waves/round-90/w1/ScribeEntry-receipts/capture-intake-gate.md` (draft only — **not** in `corpus/`).
- Wrote `.ufo/waves/round-90/w1/ScribeEntry.md` (this report).
- Scratch `/fast/scratch/hyaku/kasegi-r90/ScribeEntry` (the GitLab fetch, the text conversion, the anchorcheck log) is deleted before yield; the receipt carries only digests and the scanner's own summary line.
- Nothing else: no lane file, no `corpus/`, no instrument, no frozen `c1/` `c2/` `controls/` `l1/`, no `.ufo/state/`, no git/jj write anywhere. One network request (the GitLab page named in the seat item).

## Findings / routed defects (reported, not scored)

1. **`corpus/instruments/README.md:173` describes a function that does not exist.** The line reads "the scheme allowlist lives in `allow_url()`, redirects stay on http(s)"; `git grep -n allow_url 643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2 -- corpus` returns that README line only (identical at base `6088c3eb…`), and `git grep … -- '*.py'` at the landing returns nothing. `capture-source.py`'s `fetch()` (`corpus/instruments/capture-source.py:92-98`) performs no scheme check before `urlopen` — the same code path M90-2 records accepting `file://`. Pre-existing, not introduced by C2, outside P3's three paths; the draft entry cites the README only for its intake-gate paragraph (`corpus/instruments/README.md:175-184`) and deliberately does not repeat the `allow_url()` sentence.
2. **The instrument's `--selftest` cannot distinguish a hit from a gate error.** `capture-source.py:169-173` asserts only that the capture refused and the file was kept; a `gate-error` refusal (e.g. scanner removed) also writes nothing, so it satisfies both. The counter is what discriminates (`G1` requires the shape to be named, `G5` requires a clean input to refuse when the scanner is removed — `.ufo/waves/round-90/l1/c2-landing-r90.txt:5`, `:9`). Candidate round-91 fix: make the selftest assert the expected shape name, or run a clean input under the same harness.
3. **One plant yields two `INTAKE-REFUSED` lines.** The selftest's single fixture matches `credential` and `aws-sts-session-token`, so the loop (`capture-source.py:136-138`) prints two lines for one plant. That is what `:24-25` documents ("one line per shape"), but any receipt that counts lines per plant, or asserts exactly one line, is wrong.
4. **The landing receipt's G6 line prints a `/tmp` path** (`.ufo/waves/round-90/l1/c2-landing-r90.txt:10`, `:22`, `:34`: `out=/tmp/capture-source-selftest-…`). The counter passes no `TMPDIR`, so the instrument's own `tempfile.mkdtemp` landed in `/tmp`. No lane file was written and no counter/gate output was filed there; whether the scratch directive covers instrument temp dirs is the L1's call — if it does, the counter should set `TMPDIR` under `--work`.
5. **S132's row carries a flip condition this round did not meet.** `corpus/SOURCES.md:144` reads `rejected` with "flip: a round that adds an input-size bound to the intake gate cites it as the contrast case"; C2 added no size bound, so the draft entry cites the live page as contrast only and claims no flip. Flagged so the citation is not read as a flip claim.

## Out of scope

- Scoring or re-running either frozen claim; the C1 meter; the C2 counter's limbs; any change to `claims.json`, the frozen wave bytes, the instruments, `corpus/`, `SOURCES.md`, `SCORECARD.md`, `SKILL.md`, `PROVINCE.md`.
- The L1's integration decision (where the entry lands, whether it is admitted, whether the README defect is fixed this round or routed).

## Artifacts

- Draft entry: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-90/w1/ScribeEntry-receipts/capture-intake-gate.md`
- This report: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-90/w1/ScribeEntry.md`
- Scratch: `/fast/scratch/hyaku/kasegi-r90/ScribeEntry` — deleted.

## Citation table (every path:line cited by the draft, with the anchor's line text)

Rows marked *withheld* carry a fixture or a vendor placeholder on the cited bytes; the span's sha256 prefix is given instead of the text, per the round's credential-hygiene rule.

| citation | line text at the anchor (first line, ≤150 chars) | verdict |
|---|---|---|
| `corpus/source-snapshots/round-90/S131.txt:570` | Push protection is a secret scanning feature designed to prevent hardcoded credentials, such as secrets or tokens, from ever being pushed to your r… | OK |
| `corpus/source-snapshots/round-90/S131.txt:610` | For push protection for repositories, by default, anyone with write access to the repository can bypass push protection by specifying a bypass reas… | OK |
| `corpus/source-snapshots/round-90/S131.txt:612` | Adds the bypass event to the audit log | OK |
| `corpus/source-snapshots/round-90/S131.txt:613` | Sends an email alert to personal account, organization, and enterprise owners, security managers, and repository administrators who are watching th… | OK |
| `corpus/source-snapshots/round-90/S131.txt:610-613` | For push protection for repositories, by default, anyone with write access to the repository can bypass push protection by specifying a bypass reas… | OK |
| `corpus/lessons/round-86.md:61` | - **What happened:** the L1 captured https://hackerone.com/reports/1997312.json with `capture-source.py` and committed it in the freeze `252df0c9`,… | OK |
| `corpus/lessons/round-86.md:62` | - **Captured-by:** the r43 gate's R-NOSECRET pattern catches it, but it scans packages, and no rule ran it over a capture before the freeze commit. | OK |
| `corpus/instruments/capture-source.py:5-6` | python3 corpus/instruments/capture-source.py --id S001 --url URL \ | OK |
| `corpus/instruments/capture-source.py:20-26` | Intake gate (round 90). Before the snapshot file is opened, its bytes are | OK |
| `corpus/instruments/capture-source.py:23` | lane-relative path. A hit refuses the capture: nothing is written (an existing | OK |
| `corpus/instruments/capture-source.py:24-25` | file at --out is left byte-for-byte as it was), one INTAKE-REFUSED line per | OK |
| `corpus/instruments/capture-source.py:49` | REFUSED_RC = 3 | OK |
| `corpus/instruments/capture-source.py:52` | MAX_FETCH_BYTES = 32 * 1024 * 1024 | OK |
| `corpus/instruments/capture-source.py:53` | SCRIPT_RE = re.compile(r"<(script\|style)\b.*?</\1>", re.I \| re.S) | OK |
| `corpus/instruments/capture-source.py:67-72` | def html_to_text(raw): | OK |
| `corpus/instruments/capture-source.py:94-98` | with urllib.request.urlopen(request, timeout=60) as response: | OK |
| `corpus/instruments/capture-source.py:109-112` | def lane_rel(out): | OK |
| `corpus/instruments/capture-source.py:115-123` | def intake_gate(data, out, allow_path): | OK |
| `corpus/instruments/capture-source.py:120` | found, _ = scan.scan_bytes(data, scan.patterns(), lane_rel(out), allow) | OK |
| `corpus/instruments/capture-source.py:122` | except Exception as e: # fail closed: a gate that cannot run refuses | OK |
| `corpus/instruments/capture-source.py:123` | return [("gate-error:%s" % type(e).__name__, 0)] | OK |
| `corpus/instruments/capture-source.py:126-146` | def capture(source_id, url, out, kind, allow_path=None): | OK |
| `corpus/instruments/capture-source.py:130-131` | elif kind == "text": | OK |
| `corpus/instruments/capture-source.py:134-135` | data = text.encode("utf-8") | OK |
| `corpus/instruments/capture-source.py:135-142` | found = intake_gate(data, out, allow_path) | OK |
| `corpus/instruments/capture-source.py:136-139` | if found: | OK |
| `corpus/instruments/capture-source.py:140-142` | os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True) | OK |
| `corpus/instruments/capture-source.py:143-145` | stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") | OK |
| `corpus/instruments/capture-source.py:164-171` | [fixture-shaped literal on line 164; text withheld; span sha256 bd91f00c940872b6] | OK |
| `corpus/instruments/capture-source.py:169-173` | with open(out, "wb") as fh: | OK |
| `corpus/instruments/capture-source.py:192-193` | if capture(args.id, args.url, args.out, args.kind, args.allow) is None: | OK |
| `corpus/instruments/capture-secret-scan.py:9-21` | Why: round 86 committed and pushed a HackerOne report JSON whose presigned | OK |
| `corpus/instruments/capture-secret-scan.py:14-21` | Scope. `--rev` reads the git tree at REV (no checkout) and scans only | OK |
| `corpus/instruments/capture-secret-scan.py:19-21` | `live-` (the shapes captures and seat receipts take in this lane). `--files` | OK |
| `corpus/instruments/capture-secret-scan.py:20-21` | scans exactly the named working-tree files, whatever their path: run it on | OK |
| `corpus/instruments/capture-secret-scan.py:23-65` | Shapes. The claim-package gate's SECRET_PATTERNS (imported from | OK |
| `corpus/instruments/capture-secret-scan.py:61-62` | Known limits: GCS V2 `GoogleAccessId=`/`Signature=` URLs, CloudFront signed | OK |
| `corpus/instruments/capture-secret-scan.py:61-65` | Known limits: GCS V2 `GoogleAccessId=`/`Signature=` URLs, CloudFront signed | OK |
| `corpus/instruments/capture-secret-scan.py:63-64` | (a whole URL percent-encoded inside another URL's query), more than 20 other | OK |
| `corpus/instruments/capture-secret-scan.py:68-75` | Allowlist. The gate's generic shapes also match non-secrets in captures (a | OK |
| `corpus/instruments/capture-secret-scan.py:72-73` | A row binds one exact matched value at one path, so a different value at the | OK |
| `corpus/instruments/capture-secret-scan.py:73` | same path and shape is still a hit. Rows for aws-sts-session-token are refused | OK |
| `corpus/instruments/capture-secret-scan.py:99` | _SEP = rb"(?:&amp;\|&\|\\u0026)" | OK |
| `corpus/instruments/capture-secret-scan.py:101-102` | _SIG = rb"sig=[A-Za-z0-9%+/]{40,}(?:=\|%3D){0,2}" | OK |
| `corpus/instruments/capture-secret-scan.py:103-104` | _LB = rb"(?:(?<![A-Za-z0-9_])\|(?<=\\u0026)\|(?<=%26))" | OK |
| `corpus/instruments/capture-secret-scan.py:104-107` | _CF_LB = rb"(?:(?<![A-Za-z0-9_-])\|(?<=\\u0026)\|(?<=%26))" | OK |
| `corpus/instruments/capture-secret-scan.py:109-110` | ("gcs-signed-url-signature", re.compile( | OK |
| `corpus/instruments/capture-secret-scan.py:111-112` | ("azure-sas-signature", re.compile( | OK |
| `corpus/instruments/capture-secret-scan.py:113-114` | ("cloudfront-signed-url-signature", re.compile( | OK |
| `corpus/instruments/capture-secret-scan.py:117` | NEVER_ALLOWED = frozenset({"aws-sts-session-token"}) | OK |
| `corpus/instruments/capture-secret-scan.py:121-136` | def load_allow(path): | OK |
| `corpus/instruments/capture-secret-scan.py:132-133` | if (len(cells) != 4 or not cells[0] or cells[1] in NEVER_ALLOWED | OK |
| `corpus/instruments/capture-secret-scan.py:139-148` | def gate_patterns(): | OK |
| `corpus/instruments/capture-secret-scan.py:159-160` | def scan_bytes(data, pats, path="", allow=None, used=None): | OK |
| `corpus/instruments/capture-secret-scan.py:167` | key = (path, name, hashlib.sha256(m.group(0)).hexdigest()) | OK |
| `corpus/instruments/capture-secret-scan.py:173` | found.append((name, data.count(b"\n", 0, m.start()) + 1)) | OK |
| `corpus/instruments/capture-secret-scan.py:269` | [vendor placeholder with a sig= value; text truncated before it; span sha256 cef7e1d330272eb4] | OK |
| `corpus/instruments/capture-secret-scan.py:277` | [vendor placeholder with a Signature= value; text truncated before it; span sha256 e25bec9ccea2675b] | OK |
| `corpus/instruments/capture-secret-allow.tsv:21-22` | corpus/source-snapshots/round-89/S128.txt cloudfront-signed-url-signature f8d573cbc618aea3e4c849c0f2aafa71790d0609862c454d61b9c5054c1619dd Amazon C… | OK |
| `corpus/instruments/README.md:175-184` | **Intake gate (round 90):** before the snapshot is opened, its bytes are scanned | OK |
| `corpus/SOURCES.md:143` | \| S131 \| GitHub Docs, About push protection — https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection \| docs… | OK |
| `corpus/SOURCES.md:144` | \| S132 \| GitLab Docs, Secret push protection — https://docs.gitlab.com/user/application_security/secret_detection/secret_push_protection/ \| docs… | OK |
| `.ufo/waves/round-90/l1/c2-landing-r90.txt:1` | # C2 landing receipt, round 90 (L1). freeze 33f43db9, landing 643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2 | OK |
| `.ufo/waves/round-90/l1/c2-landing-r90.txt:3-12` | CAPABILITY-CHECK rev=643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2 base=6088c3eb0c29040415c69e7b5fb91e110480ab26 seed=1034104039 override=none instrumen… | OK |
| `.ufo/waves/round-90/l1/c2-landing-r90.txt:4` | LIMB G0 pass shapes=11 missing=none extra=none | OK |
| `.ufo/waves/round-90/l1/c2-landing-r90.txt:5-6` | LIMB G1 pass plants=11 bad=none | OK |
| `.ufo/waves/round-90/l1/c2-landing-r90.txt:9` | LIMB G5 pass rc=3 written=False | OK |
| `.ufo/waves/round-90/l1/c2-landing-r90.txt:15-24` | CAPABILITY-CHECK rev=643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2 base=6088c3eb0c29040415c69e7b5fb91e110480ab26 seed=9090 override=none instrument_sha2… | OK |
| `.ufo/waves/round-90/l1/c2-landing-r90.txt:27-36` | CAPABILITY-CHECK rev=643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2 base=6088c3eb0c29040415c69e7b5fb91e110480ab26 seed=1 override=none instrument_sha256=… | OK |
| `.ufo/waves/round-90/controls/c2-controls-r90.txt:51-61` | == F3-write-then-check (expect FAIL) | OK |
| `.ufo/waves/round-90/controls/c2-controls-r90.txt:67-68` | LIMB G3 FAIL clean=6 bad=corpus/source-snapshots/round-89/S128.txt(rc=3,base_rc=0,same=False) | OK |
| `.ufo/waves/round-87/w1/ConnectorOverlap.md:158-176` | **Synthesize an Upstream Intake Gate in `capture-source.py`**: | OK |

Live-page citations (GitLab, 2026-11-07, HTTP 200) are not file rows: eight sentences, each quoted in Claim 5 and each verified to occur exactly once in the tag-stripped page text (gate 7 above). The page is not snapshotted, and the row at `corpus/SOURCES.md:144` stays `rejected`.
