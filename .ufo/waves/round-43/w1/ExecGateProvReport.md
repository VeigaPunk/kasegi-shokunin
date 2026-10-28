# ExecGateProvReport — R-PROVENANCE / R-REPORT / R-NOSECRET rule module

Round 43, wave 1, seat `ExecGateProvReport`. Base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Frozen claims read first and never edited: `.ufo/waves/round-43/claims.json`.

Item: sourceable module implementing three of the eight `claim-package-check.py`
rules, plus a transcript that proves a passing scratch package and one mutation
per defect class failing the named rule with the matched secret value redacted.

## Deliverables

| file | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-43/w1/ExecGateProvReport.rules.py` | 458 | `97003db342b713d20a159690e289c1b3aaeb7091a9a07531a44a6d1d80dc3aa5` |
| `.ufo/waves/round-43/w1/ExecGateProvReport.transcript.txt` | 202 | `e645664f269a26627d9bde3b59d42cdc755954f8039c4577ac357bfa52ec2caa` |

Both were measured after the last module edit and after scratch removal
(`wc -l` / `sha256sum` quoted below). The module is the landable integration
unit; the transcript is evidence.

## Interface (what the L1's `claim-package-check.py` can call)

- Sourceable/importable module (no relative imports, stdlib only, `importlib`
  by file path works). Proved in the transcript:
  `import-check result-keys=counts,detail,id,reasons,verdict rules=3 verdicts=pass,pass,pass`.
- `rule_provenance(root, manifest=_UNSET)`, `rule_report(root, manifest=_UNSET)`,
  `rule_nosecret(root, manifest=_UNSET)` — `root` is the package directory
  (`str`/`bytes`/`Path`); `manifest` is optional so the core can hand over an
  already-parsed `evidence/manifest.json` instead of a second read.
- Result dict is the same shape the sibling `ExecGateManifest.rules.py` returns:
  `{"id", "verdict": "pass"|"fail", "detail", "counts", "reasons"}`.
  `detail` is space-joined `key=value` pairs plus `fail=<reason,...>`; `emit(result)`
  prints `RULE <id> verdict=<v> detail=<detail>`.
- `run(root, manifest=_UNSET)` returns the three results in order
  R-PROVENANCE, R-REPORT, R-NOSECRET.
- Standalone CLI: `python3 <module> <package-dir>` → three `RULE` lines,
  `package=<path> rules=3 pass=<k> fail=<m> verdict=<WELL-FORMED|DEFECT>`,
  exit 0 only at pass=3, 1 on any fail, 2 with `package=<path> verdict=ERROR`
  when the directory is absent.

## Rule predicates implemented

### R-PROVENANCE (`provenance.json`)

Pass iff the file parses as a JSON object and:

- `agents`: non-empty list; every entry an object with non-empty, unique
  `identity` (or `name`), non-empty `requested_model` and `resolved_model`, and
  a transition — either inline `"transition": "<non-empty string>"` or a
  matching entry in `transitions[]` (both shapes accepted; a package with
  neither is `transitions-empty`).
- `transitions`, when present, is a non-empty list; each entry is an object
  whose `agent`/`identity` names a declared agent and which carries its own
  `requested_model` + `resolved_model`.
- `commands`: non-empty list; each entry an object with non-empty
  `command`/`cmd` and integer `exit_code`/`exit` (bool rejected).
- `pin`: object with non-empty `remote`/`url` and `commit`/`sha` matching
  `^[0-9a-fA-F]{7,64}$`.
- `policy_sha256`: 64 hex.
- `external_effects_performed`: present and exactly `[]` (an object `{}`, a
  non-empty list, or an absent key all fail).
- `secrets_attestation`: non-empty string, or a non-empty object that is
  clean — `"no_secrets": true` or `"findings": 0` — with non-empty `by` when
  `by` is present. `findings: 1` / `no_secrets: false` fail.

Fail reasons seen in the transcript: `unparseable`, `pin-missing`,
`external-effects-absent`, `external-effects-not-empty-list`,
`attestation-not-clean`, `transitions-empty`.

### R-REPORT (`report.md` + `evidence/manifest.json`)

Pass iff `report.md` decodes UTF-8 and:

- matches `/scope excerpt/i`;
- contains the exact literal `No submission performed` (case-sensitive);
- contains at least one `https://` URL token;
- every whole 64-hex token in the report (bounded by non-hex characters, both
  cases) occurs in the manifest digest set, and at least one digest is cited.
  Manifest digest set = `artifacts[].sha256`, `redactions[].{artifact_sha256,
  scanned_artifact_sha256, sha256}`, `expected_head_sha256`, lowercased.

Fail reasons seen: `report-missing`, `report-unreadable`,
`manifest-unparseable`, `no-submission-marker-absent`, `cited-digest-absent`.

### R-NOSECRET (package text + walk gates)

Pass iff the package tree has no symlink entry, no file over 5 MiB, and no
regular file (≤5 MiB, UTF-8 with replacement) matches a secret shape:

| class | shape |
|---|---|
| `private-key` | `-----BEGIN (…)?PRIVATE KEY-----` |
| `op-ref` | `op://<1+ ref chars>` |
| `bearer-token` | `Bearer <16+ token chars>` |
| `authorization-token` | `Authorization` `["']?` `:`/`=` `["']?` `<16+ token chars>` |
| `labelled-hex` | `token`/`secret`/`password`/`passwd`/`api_key` `["']?` `:`/`=` `["']?` `<32+ hex>` |
| `session-cookie` | `Set-Cookie:`/`Cookie:` … `session=` `<16+>` and `session`/`session_cookie`/`sessionid`/`jsessionid`/`phpsessid`/`connect.sid` `["']?` `:`/`=` `["']?` `<16+>` |

The result carries only class names, `hits`, `files`, `symlinks`, `oversize`
and the first relative `file:line` — never the matched bytes. The closure
quote in labels is accepted because JSON stores a quoted value that way (that
gap was caught by mutant M6; see below).

## Evidence

The transcript is the delivered session. The fixture package is a complete
six-file package (`report.md`, `claim_checklist.md`, `evidence/manifest.json`,
`evidence/scope.txt`, `custodian-receipts.json`, `provenance.json`,
`status.json`) built under `TMPDIR`; each mutant is that package with exactly
one delta.

Passing package:

```
$ python3 ExecGateProvReport.rules.py pkg   # passing-package
RULE R-PROVENANCE verdict=pass detail=agents=1 transitions=1 commands=1
RULE R-REPORT verdict=pass detail=cited=1 manifest=2 absent=0
RULE R-NOSECRET verdict=pass detail=files=7 hits=0 symlinks=0 oversize=0 classes=none
package=pkg rules=3 pass=3 fail=0 verdict=WELL-FORMED
exit=0
```

### The six required mutations (all fail the named rule)

| mutation | fixture | failing rule | rule detail |
|---|---|---|---|
| M1 empty external effects | `mut-1-external-effects-object` | R-PROVENANCE | `fail=external-effects-not-empty-list` |
| M1b (extra) key absent | `mut-1b-external-effects-absent` | R-PROVENANCE | `fail=external-effects-absent` |
| M2 missing pin | `mut-2-missing-pin` | R-PROVENANCE | `fail=pin-missing` |
| M3 report without marker | `mut-3-report-no-marker` | R-REPORT | `fail=no-submission-marker-absent` |
| M4 report cites absent digest | `mut-4-report-absent-digest` | R-REPORT | `cited=2 manifest=2 absent=1 fail=cited-digest-absent` |
| M5 `op://` reference | `mut-5-op-ref` | R-NOSECRET | `hits=1 classes=op-ref at=claim_checklist.md:11` |
| M6 labelled hex token | `mut-6-labelled-token` | R-NOSECRET | `hits=1 classes=labelled-hex at=provenance.json:26` |

M1 is the literal shape the contract forbids: the key is present but emptied
as an object (`{}`) rather than the required empty list; M1b covers the
absent-key reading. Each case line is
`expected=<rule> observed=<rule> exit-want=1 verdict=pass`.

### Extra coverage in the same run

- every claimed token family fires: `mut-7-private-key`, `mut-8-authorization-bearer`
  (`classes=bearer-token`), `mut-8b-authorization-token`
  (`classes=authorization-token`), `mut-9-session-cookie` (`hits=2`),
  `mut-9b-session-cookie-key` (`classes=session-cookie`);
- R30 fail-closed: `mut-10-provenance-unparseable` (`fail=unparseable`),
  `mut-11-manifest-unparseable` (`fail=manifest-unparseable`),
  `mut-12-report-binary` (`fail=report-unreadable`);
- walk gate: `probe-13-symlink-outside` — a symlink to a secret-bearing file
  outside the package fails the rule with `symlinks=1 hits=0 fail=symlink-entry`
  and the outside value never appears (`leak-check ... matches=0`), so the scan
  neither follows nor reads outside the package;
- absent directory: `$ python3 ExecGateProvReport.rules.py absent-package-dir`
  → `package=absent-package-dir verdict=ERROR`, `exit=2`;
- accepted shapes: `alias-pkg` (alternate key names `name`/`cmd`/`exit`/`url`/`sha`)
  and `core-shape-pkg` (inline agent `transition`, `"no_secrets": true`
  attestation, 7-hex commit) both print `verdict=WELL-FORMED exit=0`.

Summary line, run against the delivered bytes:

```
transcript cases=22 graded=21 mismatches=0 value-matches=0
```

### Redaction proof

Every case runs a leak check over the module's own stdout for the six literal
fixture values (op-ref, labelled hex, private-key header, bearer token,
authorization token, cookie value): `leak-check needles=6 matches=0
value-redacted=yes` on all 21 graded cases, and the driver's terminal figure is
`value-matches=0`. The detail line reports class names and a file:line only.

## Defect found and fixed during this item

The first battery run graded M6 `WELL-FORMED` — the labelled-credential pattern
required the colon immediately after the label, so a JSON key written as
`"token": "<40 hex>"` was invisible:

```
RULE R-NOSECRET verdict=pass detail=files=7 hits=0 skipped=0 classes=none
package=mut-6-labelled-token rules=3 pass=3 fail=0 verdict=WELL-FORMED
exit=0
```

The label is now followed by an optional closing quote before the separator.
Regression evidence on the exact JSON line:

```
$ python3 - <<'EOF' … old/new labelled pattern on json.dumps({"token": "9f"*20}) …
ast-parse=ok old-pattern-matches=0 new-pattern-matches=1
```

After the fix M6 fails at `provenance.json:26` (transcript). The same quote
separator was added to the authorization and session-cookie key patterns.

## Cross-seat conventions read and aligned

`ExecGateCore.rules.txt` and `ExecGateManifest.rules.py` were read after they
landed in the same wave dir. To make one core able to consume both modules, I
aligned: the result-dict shape and `emit`/`run` helpers; inline agent
`transition`; `"no_secrets": true` attestation; a 7–64 hex commit; the
symlink/oversize walk gates; and the `session_cookie` key. Divergences I did
not absorb (the frozen claim text is my authority) and that the L1 must
reconcile in `claim-package-check.py`:

1. **labelled credential breadth** — frozen claim: “32+ char hex strings
   labelled token/secret/password” (implemented); `ExecGateCore.rules.txt` says
   16+ characters of any class. The wider form flags prose like
   `password: operator-provided`.
2. **R-REPORT cited digest set** — frozen claim: “a cited digest must occur in
   the manifest” (implemented manifest-wide: artifacts, redaction digests,
   `expected_head_sha256`); `rules.txt` restricts to `artifacts[].sha256`.
3. **R-REPORT zero-cited case** — I require ≥1 cited digest, grounded in the
   contract’s report row (“Scope excerpt = verbatim policy text + URL +
   observed_at + content sha256”); `rules.txt` permits a report citing none.
4. **`op://` minimum length** — 1+ ref characters (implemented) vs 3+ in
   `rules.txt`.
5. Detail vocabulary (`pin=ok`/`effects=none`/…) differs cosmetically; the
   core prints `detail=` verbatim, so only the three above change verdicts.

Exemplar consequence for the L1: the exemplar’s report must cite a digest that
is a manifest digest (register the scope capture as an artifact), and its
`provenance.json` must satisfy one of the accepted transition/attestation
shapes — `core-shape-pkg` proves the `ExecGateCore.rules.txt` shape passes.

## Scratch

`S=/fast/scratch/hyaku/kasegi-r43/ExecGateProvReport`, created with `mkdir -p`;
`TMPDIR=$S` for the generator and driver; `PYTHONDONTWRITEBYTECODE=1` on every
run. Removed before yield, after the transcript was copied:

```
scratch-removed /fast/scratch/hyaku/kasegi-r43/ExecGateProvReport
```

Disk guard before the heavy pass: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`
→ `exit=0`, `/fast/scratch/hyaku  use% 25%  free 604.2G`, `/tmp use% 17%`,
`/var/tmp use% 38%`.

## Writes, scope, tooling

- Wrote only the two deliverables above, this receipt, and scratch. No fleet
  root, sibling lane, `/home/vgpnk/Projects/shokuknow` or PATH write. No
  git/jj mutation (no fixture git repo was needed). No network fetch, so no
  HTTP status/byte/UTC record applies.
- Tooling: none installed or upgraded.
- Transient scope note: my first `python3 -m py_compile` on the module created
  `.ufo/waves/round-43/w1/__pycache__/`; I removed it. The `__pycache__/`
  present now holds `.pyc` files for `ExecGateChain.rules`,
  `ExecGateManifest.rules` and `ExecGateProvReport.rules` created by an
  importing process at 13:44/13:46, not by my final runs — verified with
  `PYTHONDONTWRITEBYTECODE=1` import against the existing pyc:
  `pyc-mtime-before=1793205996 after=1793205996 rewritten=no`. I left it in
  place because it belongs to the integrating process.

## Risks / blockers

- Integration assumption: the core imports this file by path and prints
  `result["detail"]` verbatim (as `ExecGateManifest.rules.py` does). If it
  instead expects tuple returns, the L1 must adapt one side; the shape is
  otherwise identical to the sibling module.
- The four divergences above are real verdict differences, not cosmetic; the
  L1 owns the merge. My module is the more permissive side for cited digests
  and the stricter side for zero citations.
- False-positive surface worth watching on the exemplar: `Authorization:`
  followed by 16+ token characters in prose, and a quoted `op://` reference in
  documentation text.
- No blocker. The module was not run against the (not yet landed) exemplar or
  `ExecGateCore.claim-package-check.py`; the `core-shape-pkg` and `pkg` cases
  are the interface stand-ins.

## Verification the L1 should run after landing

```
python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar
python3 corpus/instruments/claim-package-check.py --selftest
```
plus a direct re-run of `ExecGateProvReport.rules.py` over the exemplar and
`defect-8`/`defect-9` to confirm R-REPORT and R-NOSECRET are the rules that
fail there.
