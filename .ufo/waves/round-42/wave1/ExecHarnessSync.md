# ExecHarnessSync — r42 post-integration instrument runbook: scoped findings

Seat: `ExecHarnessSync` (wave 1, round 42, lane `kasegi`).
Axes owned: `depth:verifiability`, `coverage`.
Scope: prepare the post-integration instrument runbook for the C2 coverage landing
(five commands, their expected outputs, and which of them actually discriminate), and
prove the readings on a scratch copy of the corpus with the C2 rows simulated.

No lane file was edited. No git/jj mutating command was run. The fleet root and
`~/Projects/shokuknow` were read only. The only writes are this receipt, the
deliverable below, and the seat scratch dir (removed before yield).

---

## 1. Deliverable

    .ufo/waves/round-42/wave1/ExecHarnessSync.runbook.txt
    230 lines, 11373 bytes
    sha256 e0fb8123a8ed2f0303c0fbb1d2cf50e58fb3fb3d9104e9e7cdf23f3f9fb519ad

Contents: the five gating commands in run order with their expected outputs, the two
rules that make a scratch-copy rehearsal meaningful, and a per-command account of what
each instrument does and does not discriminate. Nothing in the deliverable is a
placeholder: every expected-output line in it was observed on the landed scratch clone.

---

## 2. Method

The rehearsal copy was built from the lane's own corpus with the C2 landing
simulated on top, using the **real** wave-1 scout artifacts that had landed while I
worked:

    .ufo/waves/round-42/wave1/ScoutF25Lead.S064.txt            (the capture)
    .ufo/waves/round-42/wave1/ScoutF25Lead.manifest-record.json (the manifest record)

The scout's capture verified against the scout's own manifest record before use:

    $ sha256sum .ufo/waves/round-42/wave1/ScoutF25Lead.S064.txt
    b90a51f7b356e7683483d9ac0753e3eb06fe3ab53806a57fdd4bf129b2f141fa  ScoutF25Lead.S064.txt
    $ wc -c -l .ufo/waves/round-42/wave1/ScoutF25Lead.S064.txt
    3545 84520 ScoutF25Lead.S064.txt        # == manifest record's sha256 / size_bytes / lines

    $ python3 corpus/instruments/source-recheck.py \
        --manifest <copy>/corpus/source-snapshots/round-42/manifest.json --source S064
    S064:sha256 OK
    S064:Q1 OK occurrences=1 anchor=5-ok
    S064:Q2 OK occurrences=1 anchor=3466-ok
    S064:Q3 OK occurrences=1 anchor=3510-ok
    exit=0

The simulated landing added to the scratch copy: the `S064` registry row (mined,
`recheck` = `on-release`, `used-by` = the entry path), one rejected screened row
`S065` (rejected, `recheck` = `on-release`, `used-by` = `—`), the `F25` frontier row
(status `admitted`), `corpus/source-snapshots/round-42/{S064.txt,manifest.json}`, the
knowledge entry `corpus/knowledge/cve-record-format-json-schema.md` with the
provenance trio, and the `corpus/instruments/knowledge-expected.txt` line.

Every entry's `recheck:` line was repointed from `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`
to `cd <scratch clone> &&` so the copy is a self-contained lane (see finding F4).

I made **no network fetches** of my own; the only network traffic in this seat's
evidence is the scout's, quoted above from the scout's deliverable.

---

## 3. Baseline: the lane as it stands today (no C2 landing)

    $ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
    $ python3 corpus/instruments/frontier-recheck-count.py
    ...
    PASS     F24  knowledge/rfc-9116-security-txt.md                   ids=S063           exit=0
    entries=27 pass=27 exit=0                                     exit=0

    $ python3 corpus/instruments/capture-binding-check.py
    MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0
    AUDIT records=55 with_url=55 with_fetched_utc=17 with_archival=38 snapshot_dirs=17 \
           manifest_dirs=17 missing_manifest=0 multi_row_url=3 orphans=1 orphan=S040-live.txt
    records=55 bound=55 unbound=0                                exit=0

    $ python3 corpus/instruments/recheck-audit.py --quiet
    strict pass=60/60 cdroot_fail=0 instrument_fail=0 own_fail=0
    executes=36 gated=24 broken=0
    lines=60 total=60 pass=60 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
    expect=present expected=60 missing=0 unexpected=0 exit=0      exit=0

    $ python3 corpus/instruments/source-recheck.py \
        --manifest corpus/source-snapshots/round-42/manifest.json --source S064
    manifest UNAVAILABLE reason=missing                            exit=2

    $ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
        --root /home/vgpnk/Projects/shokunin kasegi
    kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
    kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
    kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
                                                                  exit=0

    $ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census \
        --root /home/vgpnk/Projects/shokunin kasegi
    kasegi	rows	63

These agree with the frozen before-control (`.ufo/waves/round-42/c2-controls/before.txt`:
frontier 24, registry 63, knowledge 60, harness 27/27, binding 55/55, audit expected 60).

---

## 4. The landed scratch clone: all five commands reach the after-state

    $ python3 corpus/instruments/frontier-recheck-count.py --root <clone>
    PASS     F24  knowledge/rfc-9116-security-txt.md                   ids=S063           exit=0
    PASS     F25  knowledge/cve-record-format-json-schema.md           ids=S064           exit=0
    entries=28 pass=28 exit=0                                     exit=0

    $ python3 corpus/instruments/capture-binding-check.py --root <clone>
    MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0
    MANIFEST round-42 records=1 url_bound=1 fetched=1 archival=0
    AUDIT records=56 with_url=56 with_fetched_utc=18 with_archival=38 snapshot_dirs=18 \
           manifest_dirs=18 missing_manifest=0 multi_row_url=3 orphans=1 orphan=S040-live.txt
    records=56 bound=56 unbound=0                                exit=0

    $ python3 corpus/instruments/recheck-audit.py --root <clone> --cdroot <clone> --quiet
    strict pass=61/61 cdroot_fail=0 instrument_fail=0 own_fail=0
    executes=37 gated=24 broken=0
    lines=61 total=61 pass=61 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
    expect=present expected=61 missing=0 unexpected=0 exit=0      exit=0

    $ python3 corpus/instruments/source-recheck.py \
        --manifest <clone>/corpus/source-snapshots/round-42/manifest.json --source S064
    S064:sha256 OK
    S064:Q1 OK occurrences=1 anchor=5-ok
    S064:Q2 OK occurrences=1 anchor=3466-ok
    S064:Q3 OK occurrences=1 anchor=3510-ok                        exit=0

    $ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate <clone>
    landed	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
    landed	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
    landed	ok	<clone>/corpus/SOURCES.md                          exit=0

    $ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census <clone>
    landed	rows	65        (S064 + S065)   —  64 with S064 only

Every after-state value in the frozen C2 predicate is reachable on the clone:
`entries=28 pass=28` incl. `PASS F25`, `records=56 bound=56 unbound=0`,
`expected=61 missing=0 unexpected=0`, source-recheck exit 0, census exit 0 with only
the standing W04 S028/S029 pair. Frontier rows 24 -> 25, knowledge files 60 -> 61.

---

## 5. Which commands already discriminate

I ran thirteen single-defect probes against the landed clone (each probe: one copy of
the clone, one injected defect, all five commands). The full transcript is retained
in the seat scratch (removed at yield); the decisive readings are reproduced here.

| probe (injected defect) | frontier | binding | audit | source-recheck | census |
|---|---|---|---|---|---|
| baseline (no defect) | 0 `entries=28 pass=28` | 0 `56/56` | 0 `expected=61` | 0 `sha256 OK` | 0 |
| P01 F25 status flip `admitted`->`candidate` | **0** but `entries=27 pass=27` | 0 | 0 | 0 | 0 |
| P02 F25 entry file missing | 1 `problems=missing-entry` | 0 | 1 `missing=1` | 0 | 1 E11 |
| P03 S064 status `mined`->`queued` | 0 | 0 | 0 | 0 | 0 |
| P04 manifest record `url` mutated | 0 | 1 `rule=url-mismatch` | 0 | 0 | 0 |
| P05 capture file deleted | 1 `problems=recheck-exit-2` | **0** | 0 | 2 `reason=missing` | 0 |
| P06 capture bytes corrupted | 1 `problems=recheck-exit-1` | **0** | 0 | 1 `sha256 MISMATCH` | 0 |
| P07 `knowledge-expected.txt` not updated | 0 | 0 | 1 `unexpected=1` | 0 | 0 |
| P08 entry's recheck `--manifest` path absent | 1 `problems=manifest-unreadable` | 0 | 1 `paths_fail=1` | 0 | 0 |
| P09 S064 row source cell carries two https URLs | 0 | 1 `double-https-row`+`url-ambiguous` | 0 | 0 | 0 |
| P10 S064 `used-by` path does not exist | 0 | 0 | 0 | 0 | 1 E11 |
| P11 a pinned quote moved in the capture | 1 `problems=recheck-exit-1` | **0** | 0 | 1 `sha256 MISMATCH` | 0 |
| P12 entry's recheck selects `S063` not `S064` | 1 four problems | 0 | 0 | 0 | 0 |
| P13 manifest id is not `S064` | 1 `manifest-missing-ids` | 1 `rule=no-row` | 0 | 2 `reason=not-listed` | 0 |

Decisive lines, verbatim:

    P01  frontier  entries=27 pass=27 exit=0                 <-- exit stays 0, only the COUNT moves
    P03  (all five) exit=0                                   <-- no instrument sees a non-mined S064
    P05  frontier  FAIL F25 knowledge/cve-record-format-json-schema.md ids=S064 exit=2 problems=recheck-exit-2
         binding   records=56 bound=56 unbound=0
         recheck   S064:source UNAVAILABLE reason=missing
    P06  recheck   S064:sha256 MISMATCH expected=b90a51f7b356e7683483d9ac0753e3eb06fe3ab53806a57fdd4bf129b2f141fa \
                   actual=54965aa5184e7ff353e5aedff0ac990c9afacd2bdff28804323483edb0ef6066
    P04  binding   FAIL rule=url-mismatch record=S064 row=S064 dir=round-42
                   records=56 bound=55 unbound=1
    P07  audit     expect=present expected=60 missing=0 unexpected=1 exit=1
    P09  binding   FAIL rule=double-https-row row=S064 n=2
                   FAIL rule=url-ambiguous record=S064 row=S064 tokens=2 dir=round-42
    P10  census    landed E11 S064 used-by corpus/knowledge/absent-entry.md
    P12  frontier  FAIL F25 ... problems=header-sources-not-rechecked,selection-not-declared-by-entry,\
                          selection-not-cited-by-entry,manifest-missing-ids
    P13  binding   FAIL rule=no-row record=S099 dir=round-42
         recheck   S064:source UNAVAILABLE reason=not-listed

**Answer to the item's question.** All five commands discriminate *something*, and
each covers a different defect class:

- `frontier-recheck-count.py` is the only command that binds the frontier row to the
  entry to the manifest to the quote: it catches a missing entry, an unreadable
  manifest, a manifest that does not list the selected id, a recheck line that selects
  an undeclared or uncited source, and any recheck line that exits non-zero.
- `capture-binding-check.py` is the only command that binds the manifest record to
  the registry row (url, row id, duplicate ids, rejected-row anchors) and to the
  fetch provenance (`fetched_utc`), and the only one that catches an orphan capture
  or a double-URL row.
- `recheck-audit.py` is the only command that catches drift between the knowledge
  tree and `knowledge-expected.txt` in either direction.
- `source-recheck.py` is the only command that opens the capture bytes: it is the only
  detector of a corrupted capture, a moved quote, a missing capture and an unlisted id.
- `sources-census.sh validate` is the only command that checks the registry row
  grammar and the `used-by` path's existence on disk.

**Three gaps that the five commands do not close, so the L1 must not read a green
run as a complete landing:**

- **G1 — the F25 `admitted` status cell is not enforced anywhere.** P01 flipped it to
  `candidate`: the frontier harness printed `entries=27 pass=27 exit=0`. The count
  must be asserted (`entries=28`) and the status cell read directly; the harness's
  exit code alone is blind to the flip.
- **G2 — the S064 `mined` status cell is not enforced anywhere.** P03 flipped it to
  `queued`: all five commands stayed green. Only the claim's own `awk`/`grep` reading
  of column 9 sees it.
- **G3 — `capture-binding-check.py` never opens the capture.** P05/P06/P11 left it at
  `records=56 bound=56 unbound=0` while the capture was deleted, corrupted, or had a
  moved quote. The frontier harness went red only because the entry's recheck line
  failed; `source-recheck.py` is the direct detector.

---

## 6. Findings the L1 should act on before the landing

**F1 — the registry row count after the landing is 64 or 65, and the frozen claim's
counting command says 64.** `claims.json` C2 `counting_commands` lists
`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 63 -> 64`,
and its `after` says "registry 64 (S064 mined)". But the same predicate requires the
screened reject to be recorded "in the lesson Gate block", and the wave-1 spec
(`ExecC2Rows`) asks for the rejected candidate to also be a registry row (S065),
which makes the count 65. I measured both shapes: frontier 28/28, binding 56/56,
audit expected=61, source-recheck exit 0, census exit 0 in **both**; the registry row
count is the only difference (`census ... rows 64` vs `rows 65`). The C2 kill rule
contains no registry-count clause, so either shape is claim-safe, but the verifier's
stated after-value should match the landed file. Decision is the L1's; flagged to
`ExecC2Rows` as well.

**F2 — a rejected row's `recheck` cell must be a real cadence, never `—`.** Measured
on the clone: `E09 S065 recheck=—` and `sources-census.sh validate` exit **1**, which
would trip the C2 kill rule "census exit!=0 or a new W/E code". With `recheck` =
`on-release` the same registry validates exit 0 with only the standing W04 S028/S029
pair. (`used-by` = `—` is correct for a rejected row and raises no E11.)

**F3 — `recheck-audit.py --root` defaults to `$PWD`, not to the lane that owns the
script** (the other three instruments default to the script's own lane). Run from a
foreign cwd it prints `lines=0 total=0`, `expect=absent`, exit 1. The claim's
counting command `python3 corpus/instruments/recheck-audit.py --quiet` is only correct
when the cwd is the lane root; the runbook says so.

**F4 — a scratch copy of the corpus is not self-contained, and this silently defeats
any replay limb that mutates one.** 59 of the 60 entries' `recheck:` lines begin
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`, so inside a copy they still
`cd` into the **real lane**:

    $ python3 <copy>/corpus/instruments/recheck-audit.py --root <copy> --cdroot <copy> --quiet
    strict pass=1/60 cdroot_fail=59 instrument_fail=0 own_fail=0
    exit=1

and `frontier-recheck-count.py --root <copy>` scores the copy's F25 row by running
the real lane's files (a capture deleted in the copy still resolves; the harness
reports `recheck-exit-0` instead of the defect). After repointing the entries at the
copy:

    $ sed -i "s|cd /home/vgpnk/Projects/shokunin/kasegi-shokunin \&\&|cd <copy> \&\&|" <copy>/corpus/knowledge/*.md
    $ python3 <copy>/corpus/instruments/recheck-audit.py --root <copy> --cdroot <copy> --quiet
    strict pass=61/61 cdroot_fail=0 instrument_fail=0 own_fail=0
    expect=present expected=61 missing=0 unexpected=0 exit=0      exit=0

The ampersands must be escaped in the sed replacement: a bare `&` stands for the whole
match and pastes the old text back in (measured: the first attempt produced
`recheck: cd <copy> cd /home/.../kasegi-shokunin &&cd /home/.../kasegi-shokunin && ...`).
This matters directly for the J6 (F-BIND) and J7 (F-FLIP) replay limbs of the C1
suite, which are to run the real instruments over mutated scratch manifests; I
messaged `ExecJ6Bind` and `ExecJ7Flip` with the measured facts.

**F5 — `capture-binding-check.py` binds the manifest record's `url` field but not its
`capture_url` field** (measured: mutating `capture_url` alone leaves the check
green). Both fields carry the same value in the scout's record, so this is a latent
gap rather than a live defect, but the binding limb should not be described as
"the URL is verified" without naming the field.

**F6 — the census's W04 duplicate-URL rule only fires when the two rows' `scope`
cells differ.** S059 and S060 share `https://cyclonedx.org/docs/1.7/json/` and draw
no W04 because their scope cells are identical. A new row that reuses a URL with a
different scope text will add a W code and break the "only the standing W04
S028/S029" expectation — the S064 URL must be new to the registry (it is: the CVE
Record Format URL appears nowhere in the current registry).

---

## 7. Retained evidence and hygiene

- Scratch dir `/fast/scratch/hyaku/kasegi-r42/ExecHarnessSync/` held: the base corpus
  copy, the landed clone, the no-S065 variant, thirteen probe copies, the two
  builders, and the command logs. It is removed with `rm -rf` before this yield; the
  only things kept are this receipt and the deliverable, both copied into the wave
  directory.
- Disk guard was green before the work (`/fast/scratch/hyaku` 27% used, 592.6G free).
- No tool was installed or upgraded in this seat; no new channel was used.
- No build, lint or test of the C1 closure suite was run: `corpus/instruments/r42-closure.sh`
  does not exist in the lane at the time of writing (the c1 before-control records it
  absent at base), and building it is another seat's deliverable. This seat's
  commands are the five instruments only.
- Files changed by this seat:
  - `.ufo/waves/round-42/wave1/ExecHarnessSync.runbook.txt` (new, deliverable)
  - `.ufo/waves/round-42/wave1/ExecHarnessSync.md` (new, this receipt)
  - nothing else anywhere.

## 8. Blockers

None for this seat's item. Two open decisions for the L1: the registry row count
(F1) and whether the screened reject is additionally registered as a row; the
instrument readings are identical either way, as measured.
