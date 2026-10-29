VERDICT: BROKEN

Scope: side-by-side verification of re-ground rows G18-G25 in `corpus/knowledge/claim-gates.md` (section `## Re-ground (round 46)`) against `corpus/instruments/claim-package-check.py` and the committed fixtures. Tree examined: `5437afeaf9b642c267bba3c31f00ae701e49da68`, exported with `git archive` to `$HYAKU_SCRATCH/kasegi-r46/R46W2RevGroundGates3` (removed on exit). Lane HEAD is `0d121a2`; `git diff --name-only 5437afe HEAD` lists only `.ufo/waves/round-46/{build-wave2-spec.py,wave2-dispatch.json,wave2-dispatch.stderr.txt,wave2-spec.json,wave2/swarm-registry.json}`, so `corpus/instruments` and `corpus/knowledge` are byte-identical across the two commits. No file was edited in the lane.

## Row table

| row | entry line | anchor lines | class | evidence |
|---|---|---|---|---|
| G18 | L54-55 | `claim-package-check.py:656-660` (raise at 689 not cited) | faithful (anchor incomplete) | F1 |
| G19 | L57-58 | `:672-674` (constant 131, raise 691 not cited) | faithful (anchor incomplete) | F2 |
| G20 | L21-23 | `:185-187` (primary rejector 181-182 not cited) | faithful; cited line is a race backstop | F3 |
| G21 | L15 | `:120` (use site 634 not cited) | narrow (committed weaker) | F4 |
| G22 | L15 | `:121` (use site 636-637 not cited) | narrow (committed stricter, case-sensitive) | F5 |
| G23 | L41 | `:489-491` | narrow (committed requires `agents`) | F6 |
| G24 | L15 | `fixtures/claim-package/defect-8-marker/expected-rule:1` | circular as witness (oracle label cited as evidence of gate output) | F7 |
| G25 | L48-50 | `fixtures/claim-package/defect-9-secret/expected-rule:1` | circular as witness; and the witnessed shape is not matched by the entry's own regex | F8, F9 |

Entry lines were verified verbatim (F0). The row's entry-line citations are correct for G18-G25.

## Findings

### F0 — entry lines cited by G18-G25 (quoted)

Command: `sed -n` of `corpus/knowledge/claim-gates.md`. Output (abridged to the cited lines):
```
15: - `report.md` must match `/scope excerpt/i` AND `/no submission (performed|made)/i` (L28–29).
21: - Every artifact: resolves inside package (`resolve(dir,'evidence',a.path)`
22:   prefixed by `dir/`); exists; `realpathSync` stays inside realDir (symlink
23:   escape check); sha256 matches; `polarity` ∈ {positive, negative}.
41: `steps`/`transitions`/`agents` — at least one non-empty.
48: `/(api[_-]?key|secret|token|password|bearer)\s*[:=]\s*["']?[A-Za-z0-9_\-]{16,}/i`.
49: Any hit errors. Note: it is a single permissive pattern — real secret hygiene
54: - **Blanket symlink ban**: any directory entry that is a symlink errors
55:   without traversal (L104-105) — separate from the manifest-artifact
57: - **Per-file size cap**: files > `5 * 1024 * 1024` B error as `oversize
58:   artifact (>5MB)` and skip the secrets scan (L111).
```
Note: the entry's own line 57-58 says the error is `oversize artifact (>5MB)`; the committed token is `oversize=N` (line 691). No row and no "left historical" entry records that string change (see F10).

### F1 — G18 (symlink ban, no traversal): faithful

Command (anchor): `sed -n '656,660p'`, output:
```
656:    for dirpath, dirnames, filenames in os.walk(pkg.root, followlinks=False):
657:        dirnames.sort()
658:        for name in sorted(dirnames):
659:            if os.path.islink(os.path.join(dirpath, name)):
660:                symlinks += 1
```
Error raise (not in the cited range): `689: raise _GateFail('symlinks=%d' % symlinks)`.

Re-run on the export with a copy of the exemplar package plus a directory symlink `dlink -> evidence` and a file symlink `evidence/alias.txt -> source-excerpt.txt`:
```
RULE R-NOSECRET verdict=fail detail=symlinks=2
package=.../work2/g18 rules=8 pass=7 fail=1 verdict=DEFECT exit=1
```
The count is 2, not 3, so `dlink` was not traversed (traversal would have counted `dlink/alias.txt` again). The unmodified exemplar control gives `R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0`, `pass=8 fail=0`. Claim faithful. Anchor incomplete: the error that makes it an error is line 689, which the row does not cite (the cited token is only the walk call).

### F2 — G19 (5 MiB cap, skip scan): faithful

Anchor `sed -n '672,674p'`: `672: if st.st_size > MAX_SCAN_BYTES:` / `673: oversize += 1` / `674: continue`. Constant `131: MAX_SCAN_BYTES = 5 * 1024 * 1024`. Error `691: raise _GateFail('oversize=%d' % oversize)` (not cited).

Re-runs (secret line `api_key: abcdefghijklmnopqrstuvwxyz0123` at the start of `big.bin`):
```
exactly 5 MiB (5242880 B):  RULE R-NOSECRET verdict=fail detail=hits=1,first=big.bin,shape=credential
5 MiB + 1 (5242881 B):      RULE R-NOSECRET verdict=fail detail=oversize=1
```
At the cap+1 size the secret is not reported, so the scan was skipped; at the cap the same bytes are scanned. Claim faithful. Anchor incomplete (constant and error line not cited).

### F3 — G20 (artifact path inside package, realpath check): faithful; the cited line is a backstop

Anchor `186: if real != root and not real.startswith(root + os.sep):`, with `187: return None, 'escape'`.

The primary rejector is earlier, `181-182: if stat.S_ISLNK(st.st_mode): return None, 'symlink'`, and `183-184` rejects non-directory intermediate components. Direct calls to `inspect_path` on the export:
```
plain artifact  evidence/source-excerpt.txt -> None        (accepted)
../report.md                                  -> dotdot
linkdir/source-excerpt.txt (linkdir -> evidence) -> symlink
```
The `escape` token at line 187 fires only if the component lstat'd as a non-symlink later realpaths outside the root. I simulated that race by making the first `os.lstat` of `linkdir` report a directory while `linkdir` was in fact a symlink to a directory outside the package:
```
lstat-calls-on-linkdir-faked: 1
backstop (TOCTOU race simulated) -> (None, 'escape')
```
So the realpath check is a TOCTOU backstop; the row's claim ("with a realpath escape check") is literally true. Note for reword: the cited line is not the rejector in normal operation.

### F4 — G21 (scope excerpt regex, whitespace-tolerant): narrow, correctly declared

Anchor `120: SCOPE_EXCERPT = re.compile(r'scope\s+excerpt', re.IGNORECASE)`; use site `634: if not SCOPE_EXCERPT.search(text):`.
Entry regex `/scope excerpt/i` accepts only one space. Committed accepts `scope\s+excerpt`. Re-run with the heading changed to `## SCOPE\texcerpt`: the scope check passes (the report then fails on the unrelated marker, see F5 controls). The committed check is weaker than the entry and the row says so.
Wording issue: the row calls this "narrowed"; the committed check accepts strictly more strings, so "relaxed" is the accurate word (see F11).

### F5 — G22 (no-submission marker, literal): narrow, correctly declared; direction is stricter

Anchor `121: NO_SUBMISSION = 'No submission performed'`; use site `636-637: if NO_SUBMISSION not in text: raise _GateFail('marker=absent')`. Case-sensitive `in`.
Re-runs on copies of the defect-8 fixture (only the one sentence changed; the fixture's sentence is `No filing has been made..`):
```
No submission performed.  -> R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
No submission made.       -> R-REPORT verdict=fail detail=marker=absent
no submission performed.  -> R-REPORT verdict=fail detail=marker=absent
```
The entry's `/no submission (performed|made)/i` accepts the second and third forms; the committed gate rejects them. The row's text ("requires the literal `No submission performed` and no other wording") states this correctly. The "made" alternative is correctly listed as historical in the "Claims left historical" paragraph ("committed check says the opposite"). Wording issue: "narrowed" is the wrong direction for this row (stricter, not weaker) — see F11.

### F6 — G23 (provenance agents list): narrow, correctly declared

Anchor `490: if not isinstance(agents, list) or not agents:` / `491: raise _GateFail('agents=empty')`.
Re-runs on the exemplar (provenance.json edited in the scratch copy):
```
steps=[{...}], agents=[]      -> RULE R-PROVENANCE verdict=fail detail=agents=empty
transitions only, no agents   -> RULE R-PROVENANCE verdict=fail detail=agents=empty
```
The committed gate requires `agents`; the entry accepts any of three. Row says "narrowed to ... non-empty `agents` list": accurate. Alternatives are listed as historical.

### F7 — G24 (witness, R-REPORT): circular as written

Anchor: `corpus/instruments/fixtures/claim-package/defect-8-marker/expected-rule:1` = `R-REPORT`. The file is the selftest's expected rule (oracle label), not gate output. Citing the oracle to show the gate fails the defect restates the claim ("is a marker defect"); it does not observe the gate. The entry's own paragraph ("the gate's behaviour is attested by the rule rows ..., not by the fixtures") concedes this, but the claim cell still says "is a marker defect".

Observed gate output on the fixture (the behaviour is true, the anchor just does not show it):
```
RULE R-REPORT verdict=fail detail=marker=absent
package=.../defect-8-marker rules=8 pass=7 fail=1 verdict=DEFECT exit=1
```
Scope of the witness: the fixture's report contains `## Scope excerpt` (line 9 of the fixture report.md), so it lacks only the no-submission marker. The row's phrase "without the no-submission and scope-excerpt markers" is wider than the fixture exercises. Scope-excerpt absence is witnessed only by my scratch control (`## Scope excerpt` renamed): `R-REPORT verdict=fail detail=scope-excerpt=absent`, not a committed fixture.
Action: reword G24 to "names R-REPORT as the expected rule of defect-8-marker (label only)", or re-anchor on a run line, and state the one-marker coverage. Otherwise cut.

### F8 — G25 (witness, R-NOSECRET): circular as written

Anchor: `corpus/instruments/fixtures/claim-package/defect-9-secret/expected-rule:1` = `R-NOSECRET`. Same objection as F7.

Observed gate output:
```
RULE R-NOSECRET verdict=fail detail=hits=1,first=provenance.json,shape=credential
```
Do-nothing control (defect-9 with only `"api_key": "0123…"` changed to `"api_key": "redacted"`): `R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0`, `pass=8 fail=0`. So the hit is discriminating.
"Anywhere" check: a dotfile in a nested directory not in the manifest, `notes/deep/.env` with `token=abcdefghijklmnop1234`: `RULE R-NOSECRET verdict=fail detail=hits=1,first=notes/deep/.env,shape=credential`. The claim "anywhere in the package" holds.

### F9 — G25: the witnessed shape is not matched by the entry's regex as written

Command: `re.compile(entry L48 regex, re.I)` run on `defect-9-secret/provenance.json` and the whole package.
Output: `entry regex hits on defect-9 provenance.json: []` and `entry regex hits on defect-9 whole package: 0`.
The fixture line is `95:  "api_key": "0123456789abcdef0123456789abcdef01234567"`. The entry's `(api[_-]?key|...)\s*[:=]` requires `[:=]` directly after the key (after optional whitespace), so the closing JSON quote blocks it. The committed hit comes from the broader pattern `claim-package-check.py:140` (`credential`, `\\?["\']?\s*[:=]`) which allows quotes.
So the G25 witness shows the committed pattern works, not the entry's regex. The row does not say the committed pattern is broader than the entry's regex (committed is stronger here, so this is a claim-to-anchor mismatch, not a weakening). Action: either add "the committed pattern at :140 is broader than the entry regex; the entry regex as written misses the JSON-quoted witness" to G25 / the historical list, or re-anchor on :140.

### F10 — unlisted entry claim: error string for the size cap

Entry L57-58 claims the error text `oversize artifact (>5MB)`. Committed error is `oversize=N` (line 691). The row G19 says only "are oversize and their secrets scan is skipped", and the historical list does not mention the error string. Add the string to the historical list (or to G19 wording) so the entry does not present a token the committed gate does not emit.

### F11 — terminology inversion: "narrowed" used in both directions

G21 "narrowed to ... whitespace-tolerant" describes a weaker check (accepts more). G22 "narrowed to ... literal" describes a stronger check (rejects `made` and lowercase). The class names are correct in each row's text, but the single word "narrowed" in both is misleading. Suggest "relaxed" for G21 and "tightened" for G22.

### F12 — counter (mechanical check, not semantics)

Command: `TMPDIR=$S python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-gates.md`
Output (G18-G25 lines): `row G18 ok=1 read=token-located` ... `row G25 ok=1 read=token-located`; trailer `reground entry=claim-gates.md rows=25 ok=25 files=3 distinct=1 exit=0`.
Sensitivity control on a scratch copy with the G19 token changed to `MAX_SCAN_BYTES_GONE`: `row G19 ok=0 read=token-not-in-lines`, `ok=24`, `exit=1`. The counter does discriminate; it does not judge the semantics in F1-F11.

## Verdict basis

BROKEN, per the seat rule (any overreach or circular row): G24 and G25 are circular as witnesses (F7, F8). Named rows to cut or reword:
- **G24**: reword to name-only with the one-marker coverage, or cut (F7).
- **G25**: reword to name-only, or re-anchor on `claim-package-check.py:140`; add the regex-mismatch note (F8, F9).
No row is overreach. The gate behaviour the rows describe was re-run and holds (F1-F6, F8). G18/G19/G20 are faithful with incomplete anchors (cite 689, 691 and 131, and mark 186 as the backstop) — these are reword, not cut.

## Limitations

- Only G18-G25 and the r46-c1 counter's G-row verdicts were examined. The landing gate, F28 entry and counter v1.1 internals outside these rows were not verified here.
- Oracle-label check (F7/F8) rests on the selftest reading `expected-rule` as the expected rule; I did not run `claim-package-selftest.py` end to end.
- The TOCTOU backstop (F3) was demonstrated with a simulated race, not a real concurrent swap.
- The lane HEAD is `0d121a2`; I examined the integrated commit `5437afe` as instructed, which has identical corpus bytes for the paths in scope.
- No candidate fixes applied; all edits were in scratch copies that were removed on exit.
- Tools: no tools installed or upgraded.
