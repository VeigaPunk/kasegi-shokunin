# SentinelGate — r90 wave-1 adversarial probe of the C2 intake gate

Seat: SentinelGate (attack/verify, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Surface: `corpus/instruments/capture-source.py` at C2 landing `643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2`
(instrument sha256 `0630d32b98d40bd07c4716b0062babfaa1a8cee6b8bb4103c582b71d41d53dbf`, equal to the frozen
candidate sha256 in `claims.json`). Scanner `corpus/instruments/capture-secret-scan.py` at the same revision.

Environment: Python 3.14.8, `pdftotext` present (`/usr/bin/pdftotext`), inputs served only by a loopback
`http.server` on `127.0.0.1` (no external host contacted). The instrument under test was run from a
`git archive` extract of `corpus/instruments` at the landing revision, not from the working tree. No lane
file was written; every fixture and symlinked/planted tree lived in scratch
`/fast/scratch/hyaku/kasegi-r90/SentinelGate` (removed at the end — see §7). No counter was re-run; nothing
here re-scores C1 or C2. The frozen predicates stand as landed.

Receipts (beside this file):
- `SentinelGate-receipts/matrix-r90.txt` — 41 probe rows, instrument stdout only (shape, line, digest, rc).
- `SentinelGate-receipts/rescan-bypass-r90.txt` — the same scanner re-run over the snapshots the gate wrote.
- `SentinelGate-receipts/dos-r90.txt` — conversion cost scaling and the `MAX_FETCH_BYTES` boundary.
- `SentinelGate-receipts/pdf-temp-r90.txt` — the PDF temp-file path before the gate.
- `SentinelGate-receipts/repro-bypass-r90.sh` — self-contained re-runner for D1–D3 (synthetic values
  generated at run time, own scratch, cleaned up).

## 1. Verdict

The gate's *ordering* is sound and was not bypassed: in every probe the bytes were scanned before anything
was created or opened (`capture-source.py:135` precedes `os.makedirs`/`open` at `:140-141`), a refusal never
created a directory, an existing `--out` was byte-identical after a refusal, the refusal line never echoed a
matched value, the allowlist is digest-bound in both directions, and every load failure (missing scanner,
missing `claim-package-check.py`, bad allowlist row, `--allow` a directory) refused instead of proceeding.

Three encoding families still write credential material with `rc=0` and with no `INTAKE-REFUSED` line,
and because the commit-time `--rev` scan uses the same `patterns()` and the same path rule, those bytes also
scan clean at commit time (verified: `rescan-bypass-r90.txt`, 7/7 written files `hits=0`). That is the class
the round-86 lesson (M86-2) is about. None of the three is covered by the frozen predicate, so they are
routed defects (D1–D3), not a claim failure.

## 2. Probe matrix (summary; full table in `matrix-r90.txt`)

| # | probe | expected | observed | class |
|---|---|---|---|---|
| R01 | STS token, plain | refuse rc3 | rc3, no write, `shape=aws-sts-session-token` + `credential` | CORRECT |
| R02 | key split by `<b>..</b>` | refuse (tags stripped, value rejoined) | rc3 | CORRECT |
| R03 | value split by `<b>`/`<wbr>`/`<!-- -->` | refuse | rc3 | CORRECT |
| R04 | azure SAS, `&amp;` separators | refuse | rc3 `azure-sas-signature` | CORRECT |
| R05 | azure SAS, `&#x26;` separators | refuse (decodes to `&`) | rc3 | CORRECT |
| R06 | azure SAS, `&#38;` separators | refuse | rc3 | CORRECT |
| R07 | azure SAS, `&amp;amp;` separators | refuse (snapshot keeps `&amp;`, accepted by `_SEP`) | rc3 | CORRECT |
| R08 | azure SAS, `&amp;#x26;` separators | refuse | **rc0, written, scanner 0 hits** | **BYPASS (D1)** |
| R09 | cloudfront URL, `&amp;#x26;` separators | refuse | **rc0, written, 0 hits** | **BYPASS (D1)** |
| R10 | azure SAS, `%26` separators | refuse | **rc0, written, 0 hits** | **BYPASS (D2)** |
| R11 | STS value with a tab entity at byte 10 | refuse | **rc0, written, 0 hits** | **BYPASS (D3)** |
| R12 | azure `sig` value with a tab entity at byte 20 | refuse | **rc0, written, 0 hits** | **BYPASS (D3)** |
| R13 | gcs signature with a tab entity at byte 30 | refuse | **rc0, written, 0 hits** | **BYPASS (D3)** |
| R14 | STS value with `&nbsp;` at byte 10 | refuse | **rc0, written, 0 hits** | **BYPASS (D3)** |
| R15 | token inside `<script>` | token must not reach the file | rc0, 6-byte snapshot (`clean` only), key name absent | CORRECT (fidelity qualifier) |
| R16 | token inside `<style>` | token must not reach the file | rc0, 6-byte snapshot | CORRECT |
| R17 | unclosed `<script>` before the token | refuse | rc3 | CORRECT |
| R18 | `--kind text`, CRLF body | refuse, `line=2` | rc3, `line=2` | CORRECT |
| R19 | plant, `--out` in a non-existent dir | refuse, no dir | rc3, dir created=False | CORRECT |
| R20 | clean, `--out` in a non-existent dir | write, mkdir | rc0, written | CORRECT |
| R21 | plant onto an existing `--out` | refuse, keep bytes | rc3, unchanged=True | CORRECT |
| R22 | `--out` a directory | clean error | rc1, uncaught `IsADirectoryError` traceback | LIMIT (D7) |
| R23 | `--out ""` | usage error | rc2 argparse | CORRECT |
| R24–R26 | allowlist `(path,shape,digest)`: same value / other value / other path | allow / refuse / refuse | rc0 / rc3 (file kept) / rc3 | CORRECT |
| R27 | allowlist row for `aws-sts-session-token` | refuse load | rc3 `gate-error:OSError` | CORRECT (fail closed) |
| R28 | `--allow` a directory | refuse | rc3 `gate-error:IsADirectoryError` | CORRECT (fail closed) |
| R29 | `--allow` an absent file | error? | rc0 — rows silently empty, no diagnostic | LIMIT (D6) |
| R30 | re-capture committed S128 at its allowlisted path | allow, byte-identical | rc0, sha16 `cd246e7d…` = committed | CORRECT |
| R31 | relative `--out` run from another cwd | allowlist consulted | rc3 — `lane_rel()` absolute, rows inert | LIMIT (D6) |
| R32 | `claim-package-check.py` removed (`patterns()` raises) | refuse | rc3 `gate-error:FileNotFoundError` | CORRECT (fail closed) |
| R33 | `capture-secret-scan.py` removed | refuse | rc3 `gate-error:FileNotFoundError` | CORRECT (fail closed) |
| R34 | `--out` a symlink to an existing file, plant | refuse, keep target | rc3, target unchanged | CORRECT |
| R35 | same symlink, clean | write | rc0; bytes land at the target, `out=` names the link | LIMIT (D5) |
| R36 | allowlist row keyed to a symlinked in-lane dir | row must not apply | rc0 — row consumed, bytes land outside the tree | LIMIT (D5) |
| R37 | R36 with a different value | refuse | rc3 | CORRECT (digest binds) |
| R38 | clean capture onto `corpus/instruments/README.md` | refuse? | rc0 — any in-tree path is a valid target | LIMIT (D5) |
| R39 | PDF with a token in the text layer | refuse | rc3, no write | CORRECT |
| R40 | clean PDF | write | rc0 | CORRECT |
| R41 | `--id` containing a newline | one line per shape | 4 `INTAKE-REFUSED` lines for 2 shapes | LIMIT (D8) |

## 3. Routed defects

### D1 — entity-encoded separator survives to a literal `&#x26;` (BYPASS, severity: low-medium)

Exploit path. A source that displays an *escaped* URL — documentation of escaping, a JSON string embedded
in HTML, a code sample — carries `&amp;#x26;` where the real query has `&`. `html.unescape` is a single
pass, so the snapshot keeps the six characters `&#x26;`, which is what a reader would also see; a reader (or
any downstream tool) recovers the separator with one more unescape. `_SEP` (`capture-secret-scan.py:99`)
accepts only `&amp;`, `&`, `\u0026`, so neither the `azure-sas-signature` nor the
`cloudfront-signed-url-signature` alternation matches, and no other shape covers `sig=`/`Signature=`.

Evidence. R08 (azure): `rc=0`, snapshot written (sha16 `00e68442c4dcb694`), the line carries
`sv=2022-11-02&#x26;sr=b&#x26;sig=` + a 45-character value; the same scanner over the written file reports
`hits=0 rc=0`. R09 (cloudfront) identical. `&amp;#61;` (double-encoded `=`) is the same class.

Impact. The snapshot is committed; the commit-time `--rev` scan runs the same patterns and reports clean
(`rescan-bypass-r90.txt`). The value is recoverable by a human with one unescape, which is exactly the
M86-2 outcome the gate exists to prevent. The trigger is a page that *shows* the escaped form rather than
serving it, so it is narrower than the plain form — hence low-medium.

Smallest remediation. In `intake_gate` (or in `capture()` before it), add a second view and scan it with the
same `patterns()`:

```python
view2 = re.sub(rb"&amp;#(?:x0*26|0*38);|&#(?:x0*26|0*38);", b"&", data)
view2 = re.sub(rb"&amp;#(?:x0*3d|0*61);|&#(?:x0*3d|0*61);", b"=", view2)
```

(`&#x26;`/`&#38;` decode to `&`; `&#x3d;`/`&#61;` decode to `=`.) Two lines, no pattern change. Add the
form to the scanner docstring's known-limits paragraph, whose current text ("percent-encoded parameter names
or `=`") reads as if entity escapes are covered.

### D2 — `%26` separators are not separators for `_SEP` (BYPASS, severity: low)

Exploit path. A site that percent-encodes only the ampersand (plain `=` parameters) produces
`sv=2022-11-02%26sr=b%26sig=<value>`. `_SEP` has no `%26`; the `%26` lookbehind in `_LB`
(`capture-secret-scan.py:103`) only lets a *match start* after a separator, never an internal one, so the
alternation fails.

Evidence. R10: `rc=0`, written (sha16 `260b4fe9648fbb39`), scanner `hits=0`. (Whole-URL percent-encoding
with `%3D` *is* a documented limit; `%26`-only is not in the docstring.)

Impact / remediation. Same consequence as D1 at a lower trigger rate. Add `%26` to `_SEP`; the change is
inert for the documented cases and cannot turn a clean capture into a refusal except where a `sig=` value of
40+ characters sits next to an `sv=` date across `%26` — which is the shape being sought.

### D3 — whitespace inserted *inside* a fixed-width value defeats the length threshold (BYPASS, severity: low)

Exploit path. `collapse()` (`capture-source.py:58-64`) rewrites runs of space/tab/`\u00a0` to one space, and
the gate scans exactly the bytes it then writes. A source that puts a tab, an NBSP, or any `\s` inside a long
value (`&#9;`, `&Tab;`, `&nbsp;`, a soft wrap) yields a snapshot whose value is split by one space. The
shapes require 20 (`aws-sts-session-token`), 16 (generic `credential`), 40 (`azure`, `cloudfront`) or 64
(`gcs`) contiguous characters, so a split inside that window misses; the generic `credential` backstop also
fails when the first run after `=` is shorter than 16.

Evidence. R11 (`rc=0`, sha16 `eebcaf723e313cc6`, split 10+16), R14 (same snapshot via `&nbsp;`), R12
(azure, split 20+25 of 45), R13 (gcs, split 30+84 of 114); all `hits=0` on re-scan. The threshold is real in both
directions: a split at offset 20 of the STS fixture still refuses (via `credential`), so this is a
window-dependent miss, not a total failure.

Impact. A line wrap is already documented as a known limit; a *single-line* NBSP/tab is not. The value stays
recoverable by deleting one space. Real-world trigger: a soft-wrapped URL or header in a code block whose
renderer emits `&nbsp;` — plausible for documentation captures, which is exactly what this lane captures.

Smallest remediation. Scan one more view with all whitespace removed and match the fixed-width shapes there:

```python
view2 = re.sub(rb"[ \t\u00a0]+", b"", data)
```

The false-positive risk is nil for shapes whose class already excludes whitespace
(`[^&\s"'<>\\]`, `[A-Za-z0-9%+/]`, `[A-Za-z0-9_~-]`), which is all four affected shapes. A single extra
pass also subsumes the documented soft-wrap limit for the fixed-width shapes.

### D4 — conversion has no deadline; `SCRIPT_RE` is quadratic (LIMIT, severity: medium, non-credential)

Exploit path. `SCRIPT_RE = r"<(script|style)\b.*?</\1>"` (`capture-source.py:53`) retries from every `<script`
start that has no closing tag, rescanning to end of document. A page (or a JSON body containing `"<script"`)
with many unclosed `<script ` tokens at the 32 MiB fetch cap pins one core for days.

Evidence. CPU time (`time.process_time`, immune to sibling load) on N bytes of unclosed `<script `:
16 KB 0.11 s, 32 KB 0.44 s, 64 KB 1.71 s, 128 KB 6.88 s, 256 KB 23.31 s — ×3.4–4.0 per doubling, i.e.
`t ≈ 0.11 s · (N/16 KB)²`. Extrapolated at `MAX_FETCH_BYTES` (32 MiB): ≈ 461 000 s ≈ 128 h. Control: 256 KB
of well-formed closed `<script>x</script>` converts in 0.00 s. A benign 32 MiB body converts in 7.1 s with
child maxrss 127.7 MB (124.7 MiB, ≈3.9× the body), so memory is not the bind; time is. `fetch` caps bytes (`:95-97`) but
nothing caps conversion, and `pdftotext` has `timeout=180` while `html_to_text` has none.

Impact. A capture of a hostile or merely awkward page never completes and never refuses; an operator who
times out and moves on leaves no receipt either way.

Smallest remediation. Anchor the close tag without backtracking across the document, e.g.
`<(script|style)\b[^>]*>(?:[^<]|<(?!/\1))*</\1>`, or run `html_to_text` under a deadline / on a size-capped
prefix.

### D5 — `lane_rel()` is lexical and the write follows symlinks; no containment (LIMIT, severity: low)

Exploit path. `lane_rel()` (`:109-113`) uses `os.path.abspath`, never `realpath`, and `open()` (`:141`)
follows symlinks. (a) With a symlinked directory inside `LANE`, a lane-relative `--out` string consumes an
allowlist row keyed to that lexical path while the bytes land at the symlink target outside the tree
(R36: rc0, row consumed, physical file outside; R37: a different value is still refused, so the digest
binding holds). (b) `--out` naming a symlink to an existing file writes through it and prints the link path
(R35). (c) Any in-tree path is a legal target: R38 overwrote `corpus/instruments/README.md` with a clean
capture, and the same command would overwrite `capture-secret-scan.py` (disabling the gate for later runs)
— there is no "must be a snapshot path" check.

Impact. Digest binding prevents value substitution, so the residual risk is path misattribution and
relocation, not value laundering; but an allowlist row can be consumed for a file that is not where the row
says, and a capture can clobber the instrument that guards it.

Smallest remediation. Resolve both sides (`os.path.realpath`) in `lane_rel` and refuse when the resolved
directory escapes `LANE`; open with `os.open(out, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o644)`;
and refuse an `--out` outside the capture subtree (`corpus/source-snapshots/**`).

### D6 — allowlist non-consultation is silent (LIMIT, severity: low)

`load_allow` returns `{}` when the file does not exist (`capture-secret-scan.py:124`), and `lane_rel` returns
an absolute path for any `--out` outside `LANE`, so every row is inert; the gate then discards the `allowed`
count `scan_bytes` already computes. A documented example is refused with the same line a real secret
produces, and nothing says the allowlist was not in play (R31: a relative `--out` run from another cwd
returns rc3 on the allowlisted S128; R29: an absent `--allow` is accepted silently, so the failure is only
visible when a legitimate allowlisted capture is refused).

Smallest remediation. Pass `used`/`allowed` through `intake_gate` and print `allow_rows=<n> matched=<n>` on
the success line (counts only, never values); treat an explicit `--allow` naming an absent file as a gate
error with its own reason.

### D7 — `--out` a directory raises an uncaught traceback (LIMIT, cosmetic)

R22: `IsADirectoryError`, rc 1, traceback on stderr, nothing written. Wrap the open or check
`os.path.isdir(out)` and exit 2 with a usage line.

### D8 — `--id` injects refusal lines (LIMIT, cosmetic / receipt integrity)

R41: `--id` containing a newline produced 4 `INTAKE-REFUSED` lines for 2 shapes. The id is operator-supplied,
so this is not a bypass, but any parser of the refusal protocol (receipt, counter) can be made to see a
different shape set. Escape newlines in `%s`, or emit the id as `id=…` with a token-safe encoder.

### D9 — documented-limited forms reachable through the transform (LIMIT, acknowledged)

`&NewLine;` inside a value produces a soft-wrapped snapshot (miss), and a UTF-16 body decodes to NUL-mangled
text that neither matches nor is written as a usable token. Both are in the scanner docstring's known-limits
paragraph; recorded so the limit list is complete, not as a new defect.

## 4. What held (CORRECT)

- Refusal before write, in every order-sensitive probe: no directory on refusal (R19), existing file
  byte-identical (R21/R25/R34), `written=no` and `rc=3` in all refusals.
- Reassembly reaches the scan: `<b>`/`<wbr>`/comment splits in key *and* value (R02/R03), `&amp;`,
  `&#x26;`, `&#38;`, `&amp;amp;` separators (R04–R07). Entity decoding is the *helpful* direction here.
- `<script>`/`<style>` bodies are dropped before the write, so a token there is never committed (R15/R16: the snapshot is 6 bytes, the word `clean`) —
  correct for the intake purpose. Qualifier: it is also evidence loss (the snapshot is silent about what a
  JS-rendered page fetched), and an unclosed `<script>` does not strip (R17) — which is the safe direction.
- Whitespace normalisation, `--kind text`, CRLF, and line numbering in the *converted* bytes (R18).
- Allowlist digest binding in both directions and across paths (R24–R26, R37); `aws-sts-session-token` rows
  refused at load (R27); re-capture of the committed S128 at its own path is byte-identical (R30).
- Fail closed for a missing scanner (R33), a missing `claim-package-check.py` (R32, i.e. `patterns()` raising
  is caught by the same `except Exception` at `:122`), a bad row, and `--allow` a directory (R28).
- `MAX_FETCH_BYTES`: 32 MiB accepted and counted (7.1 s, 124.7 MiB RSS), 32 MiB+1 refused
  (`response exceeds 33554432 bytes`), nothing written (`dos-r90.txt`).
- Refusal protocol: one line per shape, `shape=<name> line=<n> out=<path> written=no`, exit 3, and the
  matched value appears in neither stdout nor stderr (substring check).
- PDF: a token in the text layer is refused before `--out` is opened (R39), a clean PDF is written (R40).

## 5. Not probed

The C2 counter limbs (G0–G6, P) were not re-run by this seat; the capability-check surface belongs to the
counter seats. No live target, no external host, no fleet or sibling-lane write, no git/jj mutation in the
lane. The three D1–D3 forms are stated as *uncovered by the frozen predicate*, with no claim of a predicate
failure.

## 6. Severity order for routing

D1 (low-medium) > D3 (low) ≈ D2 (low) > D4 (medium but non-credential, DoA) > D5 (low) > D6 (low) >
D7/D8 (cosmetic) > D9 (documented).

## 7. Files written by this seat

- `.ufo/waves/round-90/w1/SentinelGate.md` (this report)
- `.ufo/waves/round-90/w1/SentinelGate-receipts/matrix-r90.txt`
- `.ufo/waves/round-90/w1/SentinelGate-receipts/rescan-bypass-r90.txt`
- `.ufo/waves/round-90/w1/SentinelGate-receipts/dos-r90.txt`
- `.ufo/waves/round-90/w1/SentinelGate-receipts/pdf-temp-r90.txt`
- `.ufo/waves/round-90/w1/SentinelGate-receipts/repro-bypass-r90.sh`

No credential-shaped value appears in any of them (fixtures and their values existed only in scratch; the
receipts carry shape names, line numbers, digests and the scanner's HIT/summary lines). The scratch tree
`/fast/scratch/hyaku/kasegi-r90/SentinelGate` was deleted before this report was yielded.
