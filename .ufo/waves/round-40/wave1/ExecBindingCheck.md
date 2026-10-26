# ExecBindingCheck — round 40, wave 1: capture-manifest binding over the prospective round-40 capture set

Seat: ExecBindingCheck (leaf executor), round 40 wave 1, dispatched by L1 KasegiR40 (hyaku run 9).
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin, HEAD `5e985b74075dd3813a63d7750966bf8abf693465` (claims freeze).
Axes: depth:verifiability (C1 counter H1-adjacent: the C2 `capture-binding` counting command), coverage (C2).
Instrument (unmodified): `corpus/instruments/capture-binding-check.py` sha256 `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa`.

## Deliverable

`.ufo/waves/round-40/wave1/ExecBindingCheck.txt` — the instrument's full stdout, 18 lines, 1175 bytes,
sha256 `d9e6c5935a5c33156680b24bc7fd1fa4f45e15bd4365d2d2003b244d3a74cbc7`.
Bytes are the exact bytes of the run recorded below (`cmp` against the captured stdout: identical).

## What was measured, and why the run is on a mirror

The lane working tree at HEAD holds no `corpus/source-snapshots/round-40/` directory yet: the scouts deliver
captures into `.ufo/waves/round-40/wave1/` and the L1 lands them (no assemble seat exists in wave1-spec.json;
`ExecRecheckAll`'s own spec names `ExecManifestAssemble` "if present"). The seat spec therefore authorises the
scratch-mirror path: "against the lane (or a scratch mirror that includes the new capture dirs + manifest)".
Both states are measured:

| root | state | stdout tail | exit |
|---|---|---|---|
| lane (`--root` default, working tree at 5e985b7) | 15 snapshot dirs, no round-40 | `records=46 bound=46 unbound=0` | 0 |
| scratch mirror (`--root $S/mirror`) | 16 snapshot dirs, round-40 with 8 captures | `records=54 bound=54 unbound=0` | 0 |

`records=` 46 -> 54 = **+8**, exactly the number of new manifest records the wave delivered, and `bound=` equal
with `unbound=0` and exit 0, as the item requires. Baseline command and actual output:

```
$ python3 corpus/instruments/capture-binding-check.py            # default root = lane
...
AUDIT records=46 with_url=46 with_fetched_utc=8 with_archival=38 snapshot_dirs=15 manifest_dirs=15 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=46 bound=46 unbound=0
EXIT=0
```

Mirror command and actual output (this is the deliverable, verbatim):

```
$ python3 corpus/instruments/capture-binding-check.py --root /fast/scratch/hyaku/kasegi-r40/ExecBindingCheck/mirror
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-35 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-36 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-37 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-38 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-39 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-40 records=8 url_bound=8 fetched=8 archival=0
AUDIT records=54 with_url=54 with_fetched_utc=16 with_archival=38 snapshot_dirs=16 manifest_dirs=16 missing_manifest=0 multi_row_url=3 orphans=1 orphan=S040-live.txt
records=54 bound=54 unbound=0
EXIT=0
```

## Mirror construction (byte provenance, no invention)

`$S/build-mirror.py --lane <lane> --wave <wave1> --out $S/mirror --only-mined` builds, under scratch only:

1. `mirror/corpus/SOURCES.md` = the lane's `corpus/SOURCES.md` (59 `| S### |` rows) with the wave's row
   deliverables transcribed verbatim:
   - `ScribeRows.decisions.txt`: 9 rows replace their queued counterparts -> all mined except S022, S024 (rejected).
     `decided_replaced=9`.
   - `ScribeNewRows.txt`: 3 rows appended (`ScribeNewRows.txt` row bytes, NF=13 each) -> `new_rows_appended=3`;
     mirror registry ends at 62 rows. S060 mined, S061/S062 rejected.
2. `mirror/corpus/source-snapshots/` = lane copy of the 15 existing dirs + new `round-40/` holding one file per
   healthy scout record (`S016.txt`…`S060.txt`, 8 files) and `manifest.json` built from the wave's
   `Scout*.manifest-record.json` deliverables (`sources` list, `orphans: []`). Mirror manifest sha256
   `ece4a095bfe940244d6384ca17f8812ac0d207b88f65f6aba035e713c58b59c1`.

Every included record's row status is `mined` before inclusion (`--only-mined` so the mirror matches the lane's
capture-for-mined-rows convention). Included / excluded, actual assembler output:

```
include id=S060 status=mined capture=ScoutF23Lead.capture.txt
include id=S016 status=mined capture=ScoutS016.capture.txt
include id=S017 status=mined capture=ScoutS017.capture.txt
include id=S019 status=mined capture=ScoutS019.capture.txt
include id=S020 status=mined capture=ScoutS020.capture.txt
include id=S021 status=mined capture=ScoutS021.capture.txt
include id=S023 status=mined capture=ScoutS023.capture.txt
include id=S025 status=mined capture=ScoutS025.capture.txt
mirror=/fast/scratch/hyaku/kasegi-r40/ExecBindingCheck/mirror records=8 decided_replaced=9 new_rows_appended=3
```

Capture bytes were checked against the records themselves (sha256 of the delivered capture file vs the record's
`snapshot_sha256`, else `sha256`; size and line count too). All 8 agree:

| id | url | fetched_utc (record) | HTTP | bytes | lines | sha256 (16) | file sha matches record |
|---|---|---|---|---|---|---|---|
| S016 | https://www.anthropic.com/coordinated-vulnerability-disclosure | 2026-10-26T21:15:52Z | 200 | 4481 | 32 | 91cc996f5bab690f | yes |
| S017 | https://projectzero.google/2025/07/reporting-transparency.html | 2026-10-26T21:16:32Z | 200 | 5058 | 39 | 3b6aaf1f2207c468 | yes |
| S019 | https://csrc.nist.gov/pubs/sp/800/216/final | 2026-10-26T21:16:11Z | 200 | 4901 | 132 | 514cc3796dc2e6c9 | yes |
| S020 | https://www.justice.gov/criminal/criminal-ccips/page/file/983996/dl?inline= | 2026-10-26T21:16:10Z | 200 | 16693 | 319 | 8fc334bebf20734b | yes |
| S021 | https://www.cisa.gov/news-events/directives/bod-20-01-develop-and-publish-vulnerability-disclosure-policy | 2026-10-26T21:15:57Z | 200 | 58004 | 432 | 72dbba57306f786e | yes |
| S023 | https://www.cisa.gov/resources-tools/programs/coordinated-vulnerability-disclosure-cvd-program | 2026-10-26T21:16:01Z | 200 | 14357 | 213 | 52a6671fb24842e6 | yes |
| S025 | https://arxiv.org/abs/2503.17332 | 2026-10-26T21:16:02Z | 200 | 71851 | 1490 | faa1c1f8b9b34615 | yes |
| S060 | https://cyclonedx.org/docs/1.7/json/ | 2026-10-26T21:16:18Z | 200 | 4889 | 111 | d68626222139e839 | yes |

No capture was delivered for S022, S024 (rejected with flip) or S061, S062 (rejected), so the eight records are
the complete new capture set; `orphans=1` is the pre-existing declared lane orphan `S040-live.txt`, unchanged.

## The counter is not green by construction

1. Determinism: two consecutive runs over the same mirror are byte-identical
   (`cmp run-a.txt run-b.txt`; sha256 `d9e6c593…74cbc7`, 18 lines, exit 0 both times).
2. Natural red observation: before `ScribeNewRows.txt` landed, the same mirror printed
   `FAIL rule=no-row record=S060 dir=round-40` / `records=54 bound=53 unbound=1` / `EXIT=1` (captures present,
   registry row absent). That is the exact red state the C2 dependency would otherwise leave.
3. Reproduced negative control A: copy of the passing mirror with only the `| S060 |` row removed ->
   `FAIL rule=no-row record=S060 dir=round-40`, `records=54 bound=53 unbound=1`, exit 1.
4. Reproduced negative control B: copy of the passing mirror with S060's status cell set to `rejected` ->
   `FAIL rule=rejected-row-anchor record=S060 row=S060 dir=round-40`, `records=54 bound=53 unbound=1`, exit 1.

So the passing result depends on the landed row being present *and* mined, not on the instrument's default.

## Deviations and risks (measured, advisory to the L1)

1. Run is on the scratch mirror, not the lane: the lane holds no `corpus/source-snapshots/round-40/` at HEAD
   `5e985b7`, and the landing is the L1's step. The mirror transcribes the wave's own row bytes; if the L1 lands
   different bytes (e.g. different ids for the F23 row) the `records=` value is unchanged but S060's binding must
   be re-checked against the landed row. Recommended post-integration command: the same
   `python3 corpus/instruments/capture-binding-check.py` at the lane root, expect `records=54 bound=54 unbound=0`.
2. Duplicate source URL: S060's source cell carries the same URL as the existing S059 row
   (`https://cyclonedx.org/docs/1.7/json/`), so `multi_row_url` moves 2 -> 3. The instrument treats a shared URL
   across distinct ids as informational (`case_shared_url_passes`), and `bind_record` still resolves S060
   unambiguously, so binding passes. But S059 is still `rejected` with the flip text "flip: a CycloneDX-vs-CSAF
   frontier entry with a scoped analysis-subtree capture" — a condition S060 now satisfies. Unless the round-40
   Gate logs the fired flip (or S059's `teaches` is updated to "superseded by S060"), the registry carries a
   pending flip whose trigger is already met. Not a binding failure; flagged for the L1/coverage gate.
3. Record-shape variance in the scout deliverables, absorbed without loss:
   - `ScoutS017`/`ScoutS019`/`ScoutS021` records carry `sha256` but no `snapshot_sha256` (naming only; bytes match).
   - `ScoutS025` delivered a manifest-shaped JSON (`schema_version`/`purpose`/`sources[]`, self-labelled
     "candidate record") instead of a bare record; the mirror normalises both shapes and takes `sources[0]`.
     If the L1's assembler only reads bare records, S025's capture would silently drop out of the manifest —
     worth checking on landing.
4. Nothing in the lane was modified by this seat: writes are the two files under `.ufo/waves/round-40/wave1/`
   plus scratch. No mutating git command was run. Disk guard was green at start
   (`/tmp` 3 %, `/var/tmp` 35 %, `/fast/scratch/hyaku` 26 %). No tool was installed or upgraded (no pacman
   transaction was run; pacman is paused host-wide).

Scratch `/fast/scratch/hyaku/kasegi-r40/ExecBindingCheck/` (mirror, controls, captured stdout) is removed before
yield; the deliverable and this receipt hold the evidence.
