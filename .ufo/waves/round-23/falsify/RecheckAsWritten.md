# RecheckAsWritten — the three C2 `recheck:` lines, executed verbatim

Seat: `L1Kasegi23.RecheckAsWritten-2` (leaf). Scope: round-23 FALSIFY.
Target: extract the `recheck:` line from each of the three C2 entries and execute it verbatim with
`cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin`; record exact command, exit code, output; judge
runnability for a reader who copies the line, and enumerate dependencies on unstated environment.

No production file was edited. Only this report was written. No installs or updates were performed.

Repo state at observation: HEAD `953c27880a97e8d3aaf8fac44c97e0252cddcddf`
(`2026-10-25 03:35:36 -0300 round-23: mirror-fallback confinement with matrix receipts; admit F06-F08 with pinned-source rechecks`).
`git status --porcelain` is empty for all five paths named below, so every byte reported here is at HEAD.

## 1. Extracted lines

| Entry | Line | Length | trailing whitespace | non-ASCII |
|---|---|---|---|---|
| `corpus/knowledge/multiparty-vulnerability-coordination.md` | 4 | 125 | 0 | 0 |
| `corpus/knowledge/cna-assignment-and-vulnerability-rules.md` | 4 | 125 | 0 | 0 |
| `corpus/knowledge/cra-manufacturer-reporting-duties.md` | 4 | 125 | 0 | 0 |

The three lines are byte-identical in form, differing only in the `--source` argument:

```
recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018
recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S030
recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S029
```

None carries an `on-restoration` prefix (contrast the nine `anchorcheck.py` entries, which do), i.e. all
three are published as unconditionally runnable. Total command length 117 bytes measured after the
`recheck: ` marker; ASCII-only, no CR, no trailing space — character-level copy-paste is safe.

Bytes under test (sha256):

```
f743942d9643c930453c415414fd4468486140049541e3f7babc935581ae888d  corpus/instruments/source-recheck.py
b8a20607e03743f6782093167b39d65edbf5c742a987488065a54eff79f4a2da  corpus/source-snapshots/round-23/manifest.json
d366bf409e7ce9e361b9f1fe544bc1657e3eea2b6f62eaa51e9c21419dc27ab4  corpus/source-snapshots/round-23/S018.txt
82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c  corpus/source-snapshots/round-23/S029.txt
673526db7c2b4fde2a9682c6a2b8fca3ebb0ff9d4423c0559483f4540c5ab019  corpus/source-snapshots/round-23/S030.txt
```

## 2. Verbatim execution, cwd = repo root

Command form used, exactly as published, three times with `cwd=/home/vgpnk/Projects/shokunin/kasegi-shokunin`:

```
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018   # exit 0
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S030   # exit 0
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S029   # exit 0
```

Exit codes: `0`, `0`, `0`. Output verbatim (stdout only; stderr empty in all three):

```
S018:sha256 OK
S018:comms-prior-to-disclosure OK
S018:coordinator-def OK
S018:coordinator-lead OK
S018:finder-documentation OK
S018:minimize-exposure OK
S018:upstream-vendor-def OK
```
```
S030:sha256 OK
S030:rule-3-1-1-scope-definition OK
S030:rule-3-1-4-covered-products OK
S030:rule-4-1-2-security-impact OK
S030:rule-4-1-9-independently-fixable OK
S030:rule-4-2-1-1-first-opportunity OK
S030:rule-4-2-11-separate-ids OK
S030:rule-4-2-12-uncertainty OK
```
```
S029:sha256 OK
S029:art14-2a-early-warning OK
S029:art14-2b-vulnerability-notification OK
S029:art14-2c-final-report OK
S029:art14-4c-incident-final-report OK
S029:art71-article-14-start OK
S029:art71-general-application OK
```

7 + 8 + 7 = 22 lines, all `OK`, zero `MISMATCH`/`UNAVAILABLE`. Per-source assertion counts are
6, 7, 6 quotes plus one `sha256` line each — 19 quote assertions total, matching the manifest.

Re-run under a minimal environment, same cwd, `env -i PATH=/usr/bin:/bin`:
`S018 EXIT=0 lines=7`, `S029 EXIT=0 lines=7`, `S030 EXIT=0 lines=8`.

## 3. Runnability verdict for a reader who copies the line

**Runnable, but only from the repository root, and that precondition is nowhere stated.**

Copied verbatim into a shell whose cwd is `$HOME`, all three lines fail before reaching the tool:

```
$ cd /home/vgpnk && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018
python3: can't open file '/home/vgpnk/corpus/instruments/source-recheck.py': [Errno 2] No such file or directory
EXIT=2     # identical for S029 and S030
```

With the instrument made absolute but the manifest left relative — i.e. the manifest-only resolution
case — the failure is mislabelled:

```
$ cd /tmp && python3 /home/vgpnk/.../corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018
manifest UNAVAILABLE reason=missing
EXIT=2
```

The manifest exists in the canonical tree; the emitted reason describes the cwd-relative path, not a
missing artifact. From `/home/vgpnk` the same absolute-instrument form reproduces
`manifest UNAVAILABLE reason=missing`, `EXIT=2`.

Both failure modes are **fail-closed and loud** — no `OK` line is ever emitted for an unverified tree,
and exit is 2, not 0. That bounds the severity: this is a documentation/diagnosability gap, not a
false-pass hole.

No document supplies the cwd contract. Repo-wide
`grep -rniE "from (the )?(repository|repo) root|requires? the repository root|cwd" --include=*.md .`
returns no statement covering these three lines; `AGENTS.md` contains no occurrence of
`python`, `recheck`, or `cwd` at all; `README.md`, `corpus/README.md` and `corpus/SOURCES.md` carry no
run-from-root note. The repeat of the same relative form in `corpus/lessons/round-23.md:157-159`
inherits the same gap:

```sh
for s in S018 S029 S030; do python3 corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-23/manifest.json --source $s; done
```

The corpus already treats this defect class as real: `corpus/lessons/round-8-aggregator-box3-coldrun.md:47`
records an unstated-cwd incident of exactly this shape ("a cold operator who has not been told … runs
`node ops/claim-check.mjs …` from the wrong root and gets `Cannot find module`", graded `ambiguous`).

## 4. Environment dependencies — measured

| Dependency | Status | Evidence |
|---|---|---|
| `python3` on `PATH` | **stated** (named in the command) | resolved `/usr/bin/python3`; Python 3.14.8. Only `argparse/hashlib/json/os/re/subprocess/sys/tempfile/pathlib` are imported; no version-specific API beyond f-strings → floor ≈3.6 |
| cwd = repo root | **unstated** (see §3) | exit 0 at root; exit 2 from `$HOME` and `/tmp` |
| shell dialect | none | passes under `sh -c '…'` and `python3` directly |
| locale / encoding | none | `LC_ALL=C LANG=C` → S030 all-OK exit 0; `env -i PATH=/usr/bin:/bin` → all three exit 0. Snapshot bytes are `decode("utf-8")`-pinned (`source-recheck.py:121-124`), so the U+2019 in the S018 quote is font-independent |
| network | none | no `urllib`/`socket`/`http` import; verified by `env -i` with no proxy vars |
| external binaries / `subprocess` | none on the recheck path | the only `subprocess.run` is inside `selftest()` (`source-recheck.py:190-199`) and is never reached by `--manifest … --source …` |
| writable repo / git | none | tool only reads; no `HOME`, `~`, `expanduser` or `getenv` references |
| absolute paths, machine names | none | manifest `path` values are bare `S018.txt`/`S029.txt`/`S030.txt` resolved against `manifest_path.parent` (`source-recheck.py:100-106`), so a renamed or relocated checkout still works |

So the only environment fact a reader must supply beyond the literal line is the working directory.

## 5. Findings

**F-RA-1 (confirmed; depth:verifiability; low severity, doc-level).** The three published `recheck:`
lines are cwd-relative with no stated precondition, so "copy and run" is true only inside the repo root;
from any other cwd they exit 2. Falsifiable by pointing at any doc line that names the working
directory for these commands — the repo-wide grep found none.

**F-RA-2 (confirmed; diagnostics).** When the instrument is addressable and only the manifest is
cwd-relative, the tool reports `manifest UNAVAILABLE reason=missing` for a manifest that exists on disk
in the canonical tree. A reader can be sent to look for a missing file that is present, instead of at
their cwd. Falsifiable by producing that message from a cwd whose
`corpus/source-snapshots/round-23/manifest.json` exists — impossible by construction, since the message
is emitted only when the resolved path does not exist; the defect is the wording, not the branch.

**F-RA-3 (confirmed; attestation breadth).** Exit 0 attests manifest-and-snapshot self-consistency in
the tree under cwd, not the identity of the canonical kasegi tree or of the manifest itself. Demonstrated
in scratch `/tmp/kasegi-r23-falsify-RecheckAsWritten/shadow`: a copy of the round-23 directory with one
byte of `S029.txt` changed (`Regulation`→`RegulatIon`, first occurrence) and the manifest digest
re-pinned to `f805776ec313d41e304a28ff665e294f003a79a3c61b7b464a2bfdc6145e768c`
(canonical `82514478…`) returns, under the *identical* published command line:

```
S029:sha256 OK
S029:art14-2a-early-warning OK
…
S029:art71-general-application OK
EXIT=0
```

This is expected of any manifest-driven recheck and is not an argument against the fix; it is a scope
limit on the claim "the recheck line passes": it must always be read as "passes in this checkout".
Falsifiable if the command embedded an absolute repo path or if the manifest pinned its own digest.

**F-RA-4 (confirmed; positive control).** The exit 0 above is discriminating, not ceremonial. Tampering
a scratch copy of `S018.txt` (inserted `X` after `Optional participant`, digest untouched) gives
`S018:sha256 MISMATCH expected=d366bf40… actual=617d2139…` with **exit 1**; deleting `S029.txt` from a
scratch manifest directory gives `S029:source UNAVAILABLE reason=missing` with **exit 2**. So exit 0
from the three published lines is not obtainable on corrupted pins.

**F-RA-5 (confirmed; history not receipted).** The claimed historical run — the round-23 lesson's
"ran the published command three times … S018 exit 0 (7 OK lines), S029 exit 0 (7 OK), S030 exit 0
(8 OK)" — has no stored machine receipt. The wave directory holds `c1-baseline.json` and
`c1-fixed.json` for the C1 resolver, but no `c2`/recheck JSON; `grep -rl "S018:sha256\|S029:sha256\|S030:sha256"
--include=*.json` matches nothing, only the prose files `corpus/lessons/round-23.md`,
`.ufo/waves/round-23/build/RecheckSources.md`, `.ufo/waves/round-23/build/OverlapWeb.md`. The outputs in
§2 are therefore a fresh receipt for today's bytes, not corroboration of a recorded run. Falsifiable by
producing such a receipt file.

**F-RA-6 (observed, deliberately not claimed as a defect).** Two entries carry `verified-at: 2026-10-20`
while their mtimes are `2026-10-25 03:30:29` and the manifest's is `2026-10-25 03:30:24`; `git status`
is clean at HEAD, so the mtime difference is checkout/index activity, not content drift. `verified-at`
is not attested by any receipt (F-RA-5) and cannot be reconstructed from mtimes — it is a date claim,
not evidence.

## 6. Scope limits

- Only the three F06–F08 `recheck:` lines were executed. The other twelve knowledge entries' `recheck:`
  lines, the `anchorcheck.py` family, `--selftest`, and the nine `on-restoration` entries were not run.
- `source-recheck.py`'s quote-matching semantics, its `outside-manifest-directory` guard, and its
  selftest were read, not attacked; mutation of quote text with re-pinned digests belongs to the
  `S029Quotes` seat, and resolver confinement to the `Mutate*Confine` seats.
- Whether the pinned excerpts are faithful to the upstream FIRST/CVE/EUR-Lex documents is out of scope;
  the manifest itself states the check "verifies captured bytes, not current upstream freshness".
- I did not fetch any upstream source (no network), did not run builds/lint/formatters, did not touch
  git/jj state, and made no claim about admission or score movement.
- Scratch trees left in place as evidence: `/tmp/kasegi-r23-falsify-RecheckAsWritten/{*.out,S018.txt,S029.txt,S030.txt,manifest.json,shadow/,miss/}`.
  Nothing under `$HOME`, `/dev/shm`, or a global cache was written. No package manager, uv, npm or
  cargo install took place, so there is no tool-version record to add.
