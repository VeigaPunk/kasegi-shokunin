# ReviewC2Gate — C2 `capture-intake-gate`, code review

**Verdict: APPROVE.** The frozen predicates hold under independent reproduction: the
gate refuses before `--out` is opened, fails closed on every scanner/allowlist error,
covers `--kind html|text|pdf`, prints no matched value on any stream, and exit 3 is
unambiguous. Findings below are routed defects/qualifiers, not re-scoring; none
falsifies a frozen predicate. F1 and F2 are worth fixing before the gate is cited as
an allowlist control.

## Reviewed bytes (sha256)

| file | sha256 |
|---|---|
| `corpus/instruments/capture-source.py` @ `643ddb4` | `0630d32b98d40bd07c4716b0062babfaa1a8cee6b8bb4103c582b71d41d53dbf` (= the frozen candidate `0630d32b…`) |
| `corpus/instruments/capture-secret-scan.py` @ `643ddb4` | `95f24a541db8b3d6693315a03de28d0b6de0fb0b6e53a68471265382114d20ec` |
| `corpus/instruments/claim-package-check.py` @ `643ddb4` | `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` |
| `corpus/instruments/README.md` @ `643ddb4` | `b7d799a6718db298b1f01dd301fe73879f607c4b86671d6ad7d31019d0048b93` |

Diff base `6088c3e`, landing `643ddb4` (+65/−4 in `capture-source.py`, +10/−0 in
`README.md`). Diff read in full; the whole file at the landing read line-numbered
(198 lines). All probes ran against `git show 643ddb4:…` extracts in scratch, never
the lane worktree; no lane file was opened for write.

**LSP:** no `lsp` device is mounted in this session (`read xd://lsp` → not found), so
caller/definition/diagnostics checks were done by reading the full 198-line file and
its two imports, not by a language server. Grep is used only as a literal complement,
never presented as semantic proof.

## Verified — the seat's checklist

Re-runnable preamble **P0** (every command below assumes it; write nothing outside `$S`):

```bash
S=$(mktemp -d /tmp/c2r.XXXXXX); L=$S/lane; R=643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2
mkdir -p "$L/corpus/instruments" "$S/fx"
for f in capture-source.py capture-secret-scan.py claim-package-check.py capture-secret-allow.tsv; do
  git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show $R:corpus/instruments/$f > "$L/corpus/instruments/$f"; done
python3 -B -c 'import json;print(json.dumps({"token":"k"*20}))' > "$S/fx/cred.html"       # value generated, never written here
printf '<p>u?X-Amz-Security-Token=%s&X-Amz-Signature=1</p>' "$(printf 'F%.0s' $(seq 1 48))" > "$S/fx/plant.html"
printf '<p>Alpha</p>' > "$S/fx/clean.html"
cat > "$S/serve.py" <<'PY'
import functools, http.server, sys
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Q, directory=sys.argv[1]))
open(sys.argv[2], "w").write(str(s.server_address[1])); s.serve_forever()
PY
cap(){ ( cd "$L" && python3 -B corpus/instruments/capture-source.py "$@" ); }
cat > "$S/mkrow.py" <<'PY'
import hashlib, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("cs", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
body = {"credential": json.dumps({"token": "k" * 20}).encode(),
        "aws-sts-session-token": ("X-Amz-Security-Token=%s&X-Amz-Signature=1" % ("F" * 48)).encode()}[sys.argv[2]]
print("%s\t%s\t%s\tprobe" % (sys.argv[3], sys.argv[2], hashlib.sha256(dict(m.patterns())[sys.argv[2]].search(body).group(0)).hexdigest()))
PY
mkrow(){ python3 -B "$S/mkrow.py" "$L/corpus/instruments/capture-secret-scan.py" "$@"; }   # <shape> <out-path> -> allowlist row
python3 -B $S/serve.py $S/fx $S/port & SRV=$!; sleep 0.5; B=http://127.0.0.1:$(cat $S/port)/
```

| check | result | evidence |
|---|---|---|
| refusal precedes any `open`/`makedirs` of `--out` | **holds** — gate at :135, `makedirs` :140, `open` :141; a refusal into a missing parent leaves the directory uncreated | `cap --id X --url ${B}plant.html --out corpus/source-snapshots/round-91/X.txt` → rc 3; `[ -d $L/corpus/source-snapshots/round-91 ]` → no |
| existing `--out` byte-identical on a **hit** | **holds** | pre-write `previous\n`, rc 3, bytes unchanged, `written=no` |
| existing `--out` byte-identical on a **gate-error** | **holds** | `mv` the scanner away, same run → rc 3, bytes unchanged |
| fail closed: scanner unimportable | **holds** | `INTAKE-REFUSED … shape=gate-error:FileNotFoundError line=0 … written=no`, rc 3 |
| fail closed: malformed allowlist (bad digest / short row) | **holds** | both → `shape=gate-error:OSError line=0`, rc 3, nothing written |
| fail-closed exception: a **missing** allowlist file | loads as empty (scanner `load_allow` contract), i.e. *stricter*; `--allow` typo is silent but cannot admit anything | `--allow /nonexistent.tsv` → clean capture still succeeds |
| `--kind text` gated | **holds** | plant as `text` → rc 3, 2 shape lines, not written |
| `--kind pdf` gated | **holds** | generated PDF whose *text layer* carries the span → rc 3, not written |
| scanned bytes == written bytes | **holds by construction** (the same `data` object at :134 → `scan_bytes` :120 and `fh.write` :142) and by probe: a span present only in an `<a href>` is stripped by `html_to_text` before both, snapshot contains no span and is written | href probe: rc 0, snapshot `linkbody\n` |
| exit 3 collision | **none** — `REFUSED_RC` :49 used only at :193; scanner uses 0/1/2; argparse 2; selftest failure 1; no other instrument in `corpus/instruments/*.py` exits 3 | `grep -rn "return 3\|sys.exit(3)" corpus/instruments/*.py` |
| stdout/stderr carry a matched value | **no** — refusal prints `id/shape/line/out` only; gate-error prints the exception *type*; `out=` is the operator's path | `grep` over every captured stdout/stderr for the plant → none |
| exception inside `fetch`/`pdf_to_text` and an existing `--out` | rc **1**, file untouched, nothing written (fetch precedes the gate; `--out` is never opened) | `URLError` traceback; `pdftotext not found` `SystemExit` message; both keep the pre-existing bytes |
| README format vs actual line | **exact** (`INTAKE-REFUSED <id> shape=<s> line=<n> out=<p> written=no`, on stdout); one line per shape (the STS plant yields `credential` + `aws-sts-session-token`) | probe output |

Correction to a first-pass read: an earlier run reported the refusal creating the
parent directory; that was stale state from a later case in the same harness. The
isolated probe (`round-91`) and the code order both show no directory is created.

## Findings

### F1 (medium, introduced) — an allowlisted capture leaves no trace in the capture record
`intake_gate` discards `scan_bytes`' second return value (`found, _ = …`, :120), and
the success line (:144-145) prints no `allowed=` count or row reference. A capture
that only succeeded because an allowlist row matched is byte-for-byte
indistinguishable, in the record the manifest binds, from a clean capture. The
docstring (:27-29) justifies the bypass "as a push-protection bypass carries a
reason"; today the reason exists only inside the committed TSV, not in the capture
receipt or manifest. Post-hoc recovery is possible (`capture-secret-scan.py --files
<snapshot> --allow <tsv>` reports `allowed=`/`unused_allow=`), so this is
verifiability, not a leak. Fix: print `allowed=<n>` on success (or one
`INTAKE-ALLOWED shape=<s> out=<p>` line) — the scanner already returns the count and
the consumed keys.

```bash
# P0, then:
mkrow credential corpus/source-snapshots/round-90/a.txt > $S/allow.tsv
cap --id A --url ${B}cred.html --out corpus/source-snapshots/round-90/a.txt --allow $S/allow.tsv; echo rc=$?
cap --id A2 --url ${B}cred.html --out corpus/source-snapshots/round-90/a2.txt --allow $S/allow.tsv | grep -ci allow   # 0
```

### F2 (medium-low, introduced) — the path key is lexical; no lane confinement, no symlink resolution
`lane_rel` (:109-112) returns the **absolute** path whenever the resolved target is
outside `LANE`, and `load_allow` accepts any first-column string, so an absolute
allowlist row authorizes an out-of-lane write (F2a). `os.path.abspath` does not
resolve symlinks, so a symlinked directory *inside* the lane yields a lane-relative
key while the bytes land outside (F2b). And the refusal line prints the raw `out=`
argument, not the resolved path that was scanned, so a receipt's `out=` is
cwd-dependent (F2c). `README.md:177` ("under the lane-relative `--out` path") is
therefore true only when the target resolves inside the lane.

Current exposure is **latent**: 0 symlinks under `corpus/` at `643ddb4`, and all 19
allowlist rows are lane-relative. A row must still be committed to exploit it, so
this is not an unauthenticated bypass of the *scan* — only of the path binding.
Fix: `os.path.realpath` before relativizing, refuse (or key by something other than
lane-relative) when the resolved target leaves the lane, reject absolute/`..`
first-column rows, and print the resolved path in `out=`.

```bash
# P0, then:
mkrow credential "$S/out-abs.txt" > $S/allow-abs.tsv
cap --id B --url ${B}cred.html --out "$S/out-abs.txt" --allow $S/allow-abs.tsv; echo "rc=$? wrote=$([ -f $S/out-abs.txt ] && echo yes)"
mkdir -p $S/outside; ln -sfn $S/outside $L/corpus/source-snapshots/linkdir
mkrow credential corpus/source-snapshots/linkdir/z.txt > $S/allow-link.tsv
cap --id C --url ${B}cred.html --out corpus/source-snapshots/linkdir/z.txt --allow $S/allow-link.tsv
realpath -m $L/corpus/source-snapshots/linkdir/z.txt          # .../outside/z.txt
cap --id D --url ${B}plant.html --out ../escaped.txt          # INTAKE-REFUSED ... out=../escaped.txt written=no
```

### F3 (low, introduced) — the landed instrument trips its own scanner
The round-90 selftest plant at `capture-source.py:164-167` compiles a `credential`
match in the file itself (`token = "<48 chars>"`). A `--files` sweep over the
instruments reports a hit at line 164; `is_capture_path` keeps it out of the
rev-scoped census, so the frozen claim is unaffected, but any future sweep or any
seat that copies the snippet is refused. Fix: build the fake token from parts at run
time (`"IQoJ" + "b3Jp…"`), or add a lane-relative allow row for the instrument.

```bash
python3 -B $L/corpus/instruments/capture-secret-scan.py --files $L/corpus/instruments/capture-source.py
# HIT shape=credential path=…/capture-source.py line=164 ; rc=1
```

### F4 (low, pre-existing, inside the edited hunk's context) — `allow_url()` does not exist
`README.md:173` says "the scheme allowlist lives in `allow_url()`". No such function
exists in `capture-source.py` at `6088c3e` or at `643ddb4` (and in no `.py` in the
lane; the name survives only in archived README copies under `.ufo/waves/` (rounds 25, 28, 29, 31)).
`fetch` accepts any scheme urllib handles, and the round-90 selftest *depends* on
`file://` (it fetches a `file://` fixture), so the sentence is both stale and
contradicted by the new code. The round-90 hunk added 10 lines to this same bullet
(`README.md:175-184`) and left the false claim above it. Fix: delete the sentence or
state the actual policy (no scheme allowlist; `file://` is reachable and used by the
selftest).

```bash
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show $R:corpus/instruments/capture-source.py | grep -c allow_url   # 0
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show $R:corpus/instruments/README.md | grep -n allow_url           # 173
python3 -B $L/corpus/instruments/capture-source.py --selftest    # refusal lines name a /tmp/... out: the file:// fixture was fetched
```

### F5 (low, introduced) — gate-error names the type, not the row
Every scanner/allowlist load failure collapses to `shape=gate-error:<TypeName>
line=0` (:123). `load_allow` raises `OSError("allowlist row %d")`
(`capture-secret-scan.py:134`), but the row number never reaches the operator, and
one malformed row refuses *every* capture (global fail-closed). Two different
malformations produce identical output, so the operator cannot tell which row to fix
without re-running the scanner by hand. Fix: special-case the `load_allow` `OSError`
and print the lane-authored message (row number, path) — do not print arbitrary
exception text, which could embed matched bytes.

```bash
# P0, then:
printf 'corpus/x.txt\tcredential\tdeadbeef\tbad digest\n' > $S/b1.tsv
printf 'only\ttwo\n' > $S/b2.tsv
cap --id E --url ${B}clean.html --out corpus/source-snapshots/round-90/e1.txt --allow $S/b1.tsv
cap --id E --url ${B}clean.html --out corpus/source-snapshots/round-90/e2.txt --allow $S/b2.tsv
# both: INTAKE-REFUSED E shape=gate-error:OSError line=0 … written=no
```

### F6 (low, pre-existing; uncovered by the new selftest) — `file://` success path writes then crashes without a digest
`%d` with `response.status is None` at :144-145 raises `TypeError` **after** the
snapshot is written: rc 1, no `sha256=` line, an existing file already replaced. The
same line is at `6088c3e:95`, so this is not a C2 regression, and the C2 counter's G3
drives clean captures over `http` (status is an int) so its `rc=0` claim stands. The
round-90 defect is coverage: `selftest()` calls `capture()` only in the refusing
branch (:171), so `--selftest` returns 0 while the success path on the same URL
scheme it uses is broken. Fix: `status=%s` (or `%d if status is not None else 0`) and
assert one successful capture in `selftest()` (rc 0, digest line, byte count) so a
gate regression that writes cannot hide behind a refusal-only test.

```bash
printf 'previous\n' > $S/o6.txt
cap --id F --url "file://$S/fx/clean.html" --out $S/o6.txt 2>&1 | tail -2; echo "rc=${PIPESTATUS[0]}"
# TypeError: %d format … ; rc=1 ; file replaced, no sha256 line
```

## Residual risk (not defects)

- The gate trusts the co-located scanner **at runtime** with no pin. The frozen G0
  binds shapes to the scanner at REV; a worktree scanner whose `patterns()` returned
  `[]` would yield a silent pass with rc 0. The scanner is committed and reviewed,
  but the gate cannot detect its own dependency being gutted.
- For `--kind pdf`, the raw fetched body is written to a temp file (`mkstemp`, 0600,
  unlinked in `finally`, :79-89) **before** the gate; a credential-bearing PDF
  touches `TMPDIR` before it is scanned. Not `--out`, and not a committed artifact.
- On a fetch failure the traceback prints the URL to stderr; a credential placed in
  `--url` would be echoed there. Pre-existing, operator-supplied input only.
- `pdftotext failed rc=…` embeds 200 bytes of the tool's stderr (:86) — tool
  diagnostics, not document text; low risk.
- The gate inherits every scanner blind spot (soft-wrapped values, percent-encoded
  parameter names, >20 interposed parameters); the README's new known-limit sentence
  says so, and the docstring's "its bytes" is exact — only the snapshot bytes are
  scanned, and they are the bytes written.

## Verification gaps

- The C2 counter was not re-run (not this seat; frozen predicates judged elsewhere).
  My limbs reproduce G1/G2/G3/G4/G5/G6 behaviorally, but they are not the counter.
- The 32 MiB fetch ceiling was not exercised (a pre-gate `SystemExit`; static read of
  :95-98 plus the small-file probes).
- No concurrency/TOCTOU probe: the gate and the write are single-process, and the
  allowlist is read per capture; a mid-run allowlist swap was not tested.
- No LSP server is mounted, as recorded above.

## Hygiene

No credential value (planted or real) was written into the wave directory: the
fixtures used spans generated at run time, the report and receipt carry only shape
names, line numbers, rc and sha256 digests, and the fixtures themselves lived only
under the scratch root. Both wave files were then scanned with the lane's own
scanner at the landing bytes: `CAPTURE-SECRET-SCAN mode=files scanned=2 hits=0
files=0 allowed=0 rc=0`. Scratch `/fast/scratch/hyaku/kasegi-r90/ReviewC2Gate` was
removed (`rm -rf`). No git/jj write, no lane write, no pacman transaction; no tool
was installed.

## Files written

- `.ufo/waves/round-90/w1/ReviewC2Gate.md` (this report)
- `.ufo/waves/round-90/w1/ReviewC2Gate-receipts/verbatim-output.txt` (the exact
  reproduced outputs for F1–F6 and the verified limbs; digests and rc only)
