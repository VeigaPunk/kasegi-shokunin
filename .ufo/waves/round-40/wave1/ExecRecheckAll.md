# ExecRecheckAll — `source-recheck` over every round-40 mined row: eight rows green, exit=0 each (C2 / coverage)

Seat `ExecRecheckAll` (leaf, executor). Item: once the mined rows' captures and manifest records exist under the
wave dir, run `python3 corpus/instruments/source-recheck.py --manifest <manifest> --source S###` for every mined
row (the nine decided rows that become mined, plus any S060+ mined row), record each exit code and tail line, and
deliver one line per row. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, `HEAD=5e985b7`
(`5e985b74075dd3813a63d7750966bf8abf693465`, claims-freeze; read-only `git rev-parse`, no mutating git/jj command
anywhere). Run at `2026-10-26T21:25:10Z`. No tool was installed. Disk guard read before any work: `/fast/scratch/hyaku`
26% used, free 597.4G — green, and the work is light (eight runs over ≤72 KB captures).

Result: **eight mined rows, eight `exit=0`, every declared quote `OK` with its anchor verified.** Three controls
show the green discriminates (byte change → `sha256 MISMATCH exit=1`; tampered quote → `quote-not-found exit=1`;
absent id → `UNAVAILABLE reason=not-listed exit=2`).

---

## 1. The mined set, taken from the delivered decision bytes (not assumed)

`ScribeRows.changes.txt` (nine status cells, no other change):

```
$ cat ScribeRows.changes.txt
S016 queued -> mined (opened 2026-10-26; entry corpus/knowledge/anthropic-cvd-provenance-and-pacing.md; recheck 90d)
S017 queued -> mined (opened 2026-10-26; entry corpus/knowledge/pz-reporting-transparency-trial.md; recheck 90d)
S019 queued -> mined (opened 2026-10-26; entry corpus/knowledge/nist-sp800-216-vdp-framework.md; recheck on-release)
S020 queued -> mined (opened 2026-10-26; entry corpus/knowledge/doj-vdp-framework-scope-and-authorization.md; recheck on-release)
S021 queued -> mined (opened 2026-10-26; entry corpus/knowledge/cisa-bod-20-01-vdp-minimums.md; recheck on-release)
S022 queued -> rejected (superseded by S030, CNA Rules v4.2.0; reason+flip in row)
S023 queued -> mined (opened 2026-10-26; entry corpus/knowledge/cisa-cvd-program-stages.md; recheck 90d)
S024 queued -> rejected (superseded by S029, official CRA Article 14 text; reason+flip in row)
S025 queued -> mined (opened 2026-10-26; entry corpus/knowledge/cve-bench-agent-exploitation-benchmark.md; recheck on-release)
Nine status cells decided, no registry row added or removed by this seat: S016, S017, S019, S020, S021, S023 mined; S022, S024 rejected.
```

`ScribeNewRows.txt` status cells (column 9 of the row shape `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`):

```
$ awk -F'|' '/^\| *S06[0-9]/ {printf "%s status=[%s] opened=[%s] recheck=[%s] usedby=[%s]\n", $2, $9, $10, $11, $12}' ScribeNewRows.txt
 S060  status=[ mined ] opened=[ 2026-10-26 ] recheck=[ on-release ] usedby=[ corpus/knowledge/cyclonedx-analysis-subtree.md ]
 S061  status=[ rejected ] opened=[ 2026-10-26 ] recheck=[ 365d ] usedby=[ — ]
 S062  status=[ rejected ] opened=[ 2026-10-26 ] recheck=[ 30d ] usedby=[ — ]
```

So the recheck set is exactly **S016 S017 S019 S020 S021 S023 S025 S060** — the seven mined rows among the nine
(S022/S024 rejected) plus the one mined S060+ row (F23's CycloneDX source row; `ScribeF23.entry.md` line 3 cites
`source: S060`). S061/S062 are rejected and have no capture, so nothing to recheck (§5).

## 2. The committed layout, assembled in scratch (the instrument's B1 stem rule is why)

`source-recheck.py` resolves each record's `path` relative to the manifest directory and requires
`Path(path).stem == id` (B1). The scout captures are delivered as `ScoutS016.capture.txt` etc., so a run in the wave
dir would report `UNAVAILABLE reason=missing` or `stem-mismatch` for every row and measure nothing. The seat
therefore assembled the *committed* layout — `S###.txt` beside `manifest.json` — in scratch, from the delivered
`*.manifest-record.json` records, admitting a record only after its declared `sha256` matched the capture bytes:

```
$ python3 assemble.py <wave1> /fast/scratch/hyaku/kasegi-r40/ExecRecheckAll/stage
out_dir=/fast/scratch/hyaku/kasegi-r40/ExecRecheckAll/stage
manifest=…/stage/manifest.json sha256=01689fbe461e97ceb9ec97712654de488dce79c2035ddd76463c9adb8ed3a97a sources=8
staged id=S016 capture=ScoutS016.capture.txt capture_bytes=4481 capture_sha256=91cc996f5bab690f574eab62e3803d1d4151cf20bc8adae5796e9d1d3c957a3b record=ScoutS016.manifest-record.json record_sha256=64d69742d7497e410eaf2ee47b8a6080e9446681cb365a2d63f7bdc3f41923c3 quotes=3
staged id=S017 capture=ScoutS017.capture.txt capture_bytes=5058 capture_sha256=3b6aaf1f2207c468e8081010bb6f00203ec89337ebd01d9bc90e377634c083fe record=ScoutS017.manifest-record.json record_sha256=138622e28f118cb313691276fc4d143c8f8da385bc7fe92458373e3a3c796917 quotes=3
staged id=S019 capture=ScoutS019.capture.txt capture_bytes=4901 capture_sha256=514cc3796dc2e6c9076b559c5dfc716c025c18d9aae5e09ab2663c3bb2ad54d6 record=ScoutS019.manifest-record.json record_sha256=9ef2101816875910b12a4a2e2812b41d33be5745e6ba9d5568d38a5c1a921368 quotes=3
staged id=S020 capture=ScoutS020.capture.txt capture_bytes=16693 capture_sha256=8fc334bebf20734ba45e262cd782a8fb8f3edb9829609e1cf321d7312625458c record=ScoutS020.manifest-record.json record_sha256=06fe885da1dcaa063b14dcbfc328d0be5355b391b76a4a587c4634750d750b6b quotes=1
staged id=S021 capture=ScoutS021.capture.txt capture_bytes=58004 capture_sha256=72dbba57306f786ea515856aeefd99666fc5f69ad1d7ae4e0ade63347730e329 record=ScoutS021.manifest-record.json record_sha256=439d2fb63956fc21fe43b3b5989b1157ab9bedb5dec38216294391e0baa790f9 quotes=1
staged id=S023 capture=ScoutS023.capture.txt capture_bytes=14357 capture_sha256=52a6671fb24842e606b808e5cd4c77030c9c5e4f4f8af3082b31fcc927cb6087 record=ScoutS023.manifest-record.json record_sha256=e413ac5748d1a4b39420a3587c2cf2efaa7dd54c0f376f206fb75141181a26e5 quotes=2
staged id=S025 capture=ScoutS025.capture.txt capture_bytes=71851 capture_sha256=faa1c1f8b9b34615e37f26b09e5a0763ad287daf1563b0823a7473867dbf9b7b record=ScoutS025.manifest-record.json record_sha256=9482f0effb4fc4c129a8a92674402f623ed2a49baef019f88e9585fde42778b4 quotes=2
staged id=S060 capture=ScoutF23Lead.capture.txt capture_bytes=4889 capture_sha256=d68626222139e8399bd421bbf023c030e6cace071cacbfc8abe659c629ce6779 record=ScoutF23Lead.manifest-record.json record_sha256=192dd214c5f29390664854391adaf1f2a8d58703066ab605e1b39f6d42a42683 quotes=3
```

Assembly rule (deterministic; `assemble.py` is scratch-only and removed with the scratch dir, so the rule is
stated here so the L1 can reproduce the bytes): for each `*.manifest-record.json` in the wave dir — which is either
a single record (`{"id": …, "sha256": …}`) or a schema-1 document (`{"schema_version": 1, "sources": [...]}`) —
take each record, stage its capture bytes as `<id>.txt`, refuse the record unless `sha256(capture) == record.sha256`
and the staged copy re-hashes equal, then set `record["path"] = "<id>.txt"` and emit
`json.dumps({"schema_version": 1, "sources": [records sorted by id]}, indent=1, ensure_ascii=False) + "\n"`.
Every other record field is carried through unchanged. Expected manifest digest, and the one the runs below were
measured against: `01689fbe461e97ceb9ec97712654de488dce79c2035ddd76463c9adb8ed3a97a` (8 sources). A second assembly
after the runs reproduced the same digest.

Per-row identity of the staged bytes (each also equal to the record's declared `snapshot_bytes`, so no capture was
silently re-normalized by staging):

| row | capture deliverable | staged | bytes | lines | sha256 | quotes (anchors) |
|---|---|---|---|---|---|---|
| S016 | `ScoutS016.capture.txt` | `S016.txt` | 4481 | 32 | `91cc996f5bab690f574eab62e3803d1d4151cf20bc8adae5796e9d1d3c957a3b` | Q1(17) Q2(16) Q3(12) |
| S017 | `ScoutS017.capture.txt` | `S017.txt` | 5058 | 39 | `3b6aaf1f2207c468e8081010bb6f00203ec89337ebd01d9bc90e377634c083fe` | Q1(23) Q2(34) Q3(34) |
| S019 | `ScoutS019.capture.txt` | `S019.txt` | 4901 | 132 | `514cc3796dc2e6c9076b559c5dfc716c025c18d9aae5e09ab2663c3bb2ad54d6` | Q1(80) Q2(80) Q3(97) |
| S020 | `ScoutS020.capture.txt` | `S020.txt` | 16693 | 319 | `8fc334bebf20734ba45e262cd782a8fb8f3edb9829609e1cf321d7312625458c` | Q1(142) |
| S021 | `ScoutS021.capture.txt` | `S021.txt` | 58004 | 432 | `72dbba57306f786ea515856aeefd99666fc5f69ad1d7ae4e0ade63347730e329` | Q1(133) |
| S023 | `ScoutS023.capture.txt` | `S023.txt` | 14357 | 213 | `52a6671fb24842e606b808e5cd4c77030c9c5e4f4f8af3082b31fcc927cb6087` | Q1(151) Q2(154) |
| S025 | `ScoutS025.capture.txt` | `S025.txt` | 71851 | 1490 | `faa1c1f8b9b34615e37f26b09e5a0763ad287daf1563b0823a7473867dbf9b7b` | Q1(32) Q2(507) |
| S060 | `ScoutF23Lead.capture.txt` | `S060.txt` | 4889 | 111 | `d68626222139e8399bd421bbf023c030e6cace071cacbfc8abe659c629ce6779` | Q1(7) Q2(15) Q3(50) |

Cross-check against the entry deliverables already landed at run time: `ScribeEntriesG1.*.md` and
`ScribeF23.entry.md` cite `corpus/source-snapshots/round-40/S016.txt` (4,481 bytes, `91cc996f…`), `S017.txt`
(5,058, `3b6aaf1f…`), `S019.txt` (4,901, `514cc379…`), `S060.txt` (4,889, `d6862622…`) — the same byte counts and
digests this seat staged, and the same `corpus/source-snapshots/round-40/manifest.json` target in their `recheck:`
commands.

## 3. Transcript — one run per mined row, verbatim, exit captured

```
$ cd /fast/scratch/hyaku/kasegi-r40/ExecRecheckAll/stage
$ for s in S016 S017 S019 S020 S021 S023 S025 S060; do
    python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py \
      --manifest ./manifest.json --source "$s"; echo "exit=$?"
  done
S016:sha256 OK
S016:Q1 OK occurrences=1 anchor=17-ok
S016:Q2 OK occurrences=1 anchor=16-ok
S016:Q3 OK occurrences=1 anchor=12-ok
exit=0
S017:sha256 OK
S017:Q1 OK occurrences=1 anchor=23-ok
S017:Q2 OK occurrences=1 anchor=34-ok
S017:Q3 OK occurrences=1 anchor=34-ok
exit=0
S019:sha256 OK
S019:Q1 OK occurrences=2 anchor=80-ok
S019:Q2 OK occurrences=2 anchor=80-ok
S019:Q3 OK occurrences=1 anchor=97-ok
exit=0
S020:sha256 OK
S020:Q1 OK normalized=markup-whitespace occurrences=1 anchor=142-ok
exit=0
S021:sha256 OK
S021:Q1 OK occurrences=1 anchor=133-ok
exit=0
S023:sha256 OK
S023:Q1 OK occurrences=1 anchor=151-ok
S023:Q2 OK occurrences=1 anchor=154-ok
exit=0
S025:sha256 OK
S025:Q1 OK normalized=markup-whitespace occurrences=1 anchor=32-ok
S025:Q2 OK normalized=markup-whitespace occurrences=1 anchor=507-ok
exit=0
S060:sha256 OK
S060:Q1 OK occurrences=1 anchor=7-ok
S060:Q2 OK occurrences=1 anchor=15-ok
S060:Q3 OK occurrences=1 anchor=50-ok
exit=0
```

Each run is the whole manifest loaded and the one record selected (`--source`; `load_manifest` validates every
record id for duplicates and shape before selection), so 8 runs × 1 record each with the manifest's full 8-record
validation ahead of it. Line accounting: 8 `:sha256 OK` lines, 18 `:Q<n> OK` lines (3+3+3+1+1+2+2+3, the same
total as the 18 declared quotes across the eight records), zero `MISMATCH`, zero `UNAVAILABLE`, 8 `exit=0`.

## 4. Controls — the green is discriminating, not a blanket accept

**4.1 Byte change → `sha256 MISMATCH`, exit 1.** One byte of `S016.txt` flipped inside the Q1 sentence:

```
$ cp -r stage ctl && python3 - <<'PY'
from pathlib import Path
p = Path('ctl/S016.txt'); b = bytearray(p.read_bytes())
i = b.index(b'Reports originating'); b[i+3] = ord('X'); p.write_bytes(bytes(b))
PY
mutated S016.txt at byte 3655
$ cd ctl && python3 corpus/instruments/source-recheck.py --manifest ./manifest.json --source S016
S016:sha256 MISMATCH expected=91cc996f5bab690f574eab62e3803d1d4151cf20bc8adae5796e9d1d3c957a3b actual=8ea8c6cdbb1c9fe5900e802759ddc6a05dc50a3cc40222de5a8cf5dba1e4bf5c
exit=1
```

**4.2 Tampered quote → `quote-not-found`, exit 1** (same bytes, same ids, same sha256; only `S023` Q1's text
replaced by a fabricated sentence in the manifest copy):

```
$ python3 corpus/instruments/source-recheck.py --manifest ./manifest.json --source S023
S023:sha256 OK
S023:Q1 MISMATCH reason=quote-not-found
S023:Q2 OK occurrences=1 anchor=154-ok
exit=1
```

**4.3 Absent id → `UNAVAILABLE reason=not-listed`, exit 2** (a rejected row has no record; the instrument says so
rather than passing silently):

```
$ python3 corpus/instruments/source-recheck.py --manifest ./manifest.json --source S022
S022:source UNAVAILABLE reason=not-listed
exit=2
```

The verdicts therefore track the capture bytes and the quote text, not the manifest's presence or this seat's
intent.

## 5. Rows deliberately not run (and why nothing is missing)

| row | status per delivered bytes | why no recheck line |
|---|---|---|
| S022 | `rejected` (superseded by S030, CNA Rules v4.2.0) | no capture and no manifest record by design; §4.3 shows the instrument names it `not-listed`, exit 2 — a rejected row must not anchor a capture |
| S024 | `rejected` (superseded by S029, CRA Article 14) | same |
| S061 | `rejected` (labels already carried normatively by S055; no round-40 capture, so it cannot be quoted or bound) | no capture and no manifest record |
| S062 | `rejected` (no OASIS Standard v2.1 / no `os/`; csd04 is a draft) | no capture and no manifest record |

No mined row was left without a runnable capture: the set in §1 and the set in §3 are identical (8 = 8).

## 6. Deliverable

`.ufo/waves/round-40/wave1/ExecRecheckAll.txt` — 8 lines, 120 bytes,
sha256 `8fef28b320f2f4a624f16291b7885c9bb239795443f3b907fd3dbd2dde58bd74`:

```
$ wc -l ExecRecheckAll.txt && sha256sum ExecRecheckAll.txt
8 ExecRecheckAll.txt
8fef28b320f2f4a624f16291b7885c9bb239795443f3b907fd3dbd2dde58bd74  ExecRecheckAll.txt
```

```
S016 exit=0 ok
S017 exit=0 ok
S019 exit=0 ok
S020 exit=0 ok
S021 exit=0 ok
S023 exit=0 ok
S025 exit=0 ok
S060 exit=0 ok
```

## 7. Landing dependency this seat cannot close (state it plainly)

The runs above are against the assembled layout in scratch, because **`corpus/source-snapshots/round-40/` does not
exist in the lane yet** (`ls corpus/source-snapshots/` → round-23 … round-39). Nothing in this seat's write scope
allows creating it. For every landed entry's `recheck:` command to resolve, the L1 must land:

1. `corpus/source-snapshots/round-40/S016.txt S017.txt S019.txt S020.txt S021.txt S023.txt S025.txt S060.txt` —
   byte-identical to the digests in §2 (staging copies bytes, so the digests are the contract); and
2. `corpus/source-snapshots/round-40/manifest.json` — assembled by the §2 rule, expected sha256
   `01689fbe461e97ceb9ec97712654de488dce79c2035ddd76463c9adb8ed3a97a`.

If a different record set or ordering is landed, the per-row commands of §3 still hold (each is `--source`-scoped);
only the manifest digest changes. `capture-binding-check.py` (seat `ExecBindingCheck`) and the census are the
instruments that additionally bind these records to the registry rows — out of scope here.

## 8. Axes, write scope, hygiene

- **coverage (C2)**: the claim's "source-recheck passes for any mined row" is now measured, not asserted — 8/8
  mined rows green, each with its anchors verified, and the frozen junk shape (fabricated sentences) shown red at
  the sentence level (§4.2).
- **depth:verifiability**: every verdict is re-derivable from the captured bytes + the record bytes in the wave
  dir; the instrument is unchanged (`sha256 fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`, the
  same digest the round-39 receipt recorded), so the green is not the product of a loosened checker.
- Writes: only `.ufo/waves/round-40/wave1/ExecRecheckAll.txt` and this receipt, plus scratch. No lane, fleet,
  source-tree or sibling-repo file modified; no mutating git/jj command; no install; no `agent://all` message; no
  subagent.
- Scratch `S=/fast/scratch/hyaku/kasegi-r40/ExecRecheckAll/` (assembler, staged layout, two control copies,
  transcript) removed with `rm -rf -- "$S"` after the deliverable and this receipt were written.

## 9. Risks and notes

1. **Byte drift is the only thing that can invalidate §3.** Each line is tied to a capture digest; if a scout or the
   L1 re-captures any of the eight files, re-run §3 (one command per row) rather than trusting this transcript.
2. **`S020:Q1` and `S025:Q1/Q2` print `OK normalized=markup-whitespace`** rather than bare `OK occurrences=`: those
   quotes are wrapped across lines in their captures, so the raw-substring branch cannot fire and the normalized
   branch reports the match with `occurrences=1` and the anchor verified. Both are documented green branches of the
   instrument (the round-39 receipt hit the same form on S057 Q1), not a Mismatch and not an anchor failure.
3. **`S019` exercises the B2 anchor rule rather than skipping it**: Q1 and Q2 each occur twice in the capture
   (`occurrences=2`), so they pass only because their declared `anchor=80` holds the normalized quote. If the L1
   re-lands S019 with different line breaks, anchors 80/97 must be re-derived — the run would go red, which is the
   rule working.
4. **S060 is a declared scoped slice**, not the full CycloneDX page (capture L1 + page text L16060-L16169). The
   recheck therefore verifies the slice bytes and the three quotes inside it; the record's `full_text_sha256` is
   metadata, not what the instrument hashes. Nothing here claims the full page was committed.
5. **Entry-to-capture agreement is not this seat's check.** At run time `ScribeEntriesG2.*.md` had not landed
   (S020/S021/S023/S025 entries); the recheck is capture-side and is unaffected, but the L1 should re-run §3 after
   the G2 entries land if any of them changes a cited quote or digest. Entry-vs-capture quote review belongs to
   `ReviewerC2Entries`.
6. **S025's scout noted** that the registry row's older wording ("resolve up to 13%") does not appear in the v4
   capture ("exploit up to 13%…"); the record pins the v4 wording and both quotes verify against `S025.txt`
   (`anchor=32-ok`, `anchor=507-ok`). The row text is the decision scribe's business, not a recheck failure.
