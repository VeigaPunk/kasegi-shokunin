# ExecJunkRecheck — C2 negative control proved: junk-f22's four fabricated claims red the S057 recheck (round 39, C2 / coverage)

Seat `ExecJunkRecheck` (leaf, executor). Item: prove the frozen negative control — a manifest naming the committed
C2 capture S057 and carrying the four fabricated claims of `.ufo/waves/round-39/c2-controls/junk-f22.md` must make
`corpus/instruments/source-recheck.py` print exactly four `MISMATCH reason=quote-not-found` lines and exit 1; the
real Q1 quote must print `OK occurrences=1` and exit 0.

Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, `HEAD=d65d823e7c84813c192b20ee757a8761f878a61f` at run time
(read-only git; no mutating git/jj command was run). No tool was installed. All work lived in
`/fast/scratch/hyaku/kasegi-r39/ExecJunkRecheck/` and that directory is removed before yield (§8).

Result: junk manifest → `S057:sha256 OK` + **exactly four** `MISMATCH reason=quote-not-found` (`J1`–`J4`), `exit=1`;
positive control on the capture's real Q1 → `OK ... occurrences=1`, `exit=0`; isolation control (same ids, same
path, same sha256, genuine sentences) → four `OK`, `exit=0`. The discriminator is the quote text, not a blanket
rejecter.

---

## 1. Capture identity — what the manifest names

The capture is the wave-1 deliverable of seat `ExecFrontierCapture` (it did not exist when this seat started; the
driver polls for it and refuses to fabricate):

```
$ ls -l .ufo/waves/round-39/wave1/ExecFrontierCapture.S057.txt
-rw-r--r-- 1 vgpnk vgpnk 17971 Oct 26 16:32 …/wave1/ExecFrontierCapture.S057.txt
$ sha256sum .ufo/waves/round-39/wave1/ExecFrontierCapture.S057.txt
11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f
```

| field | value |
|---|---|
| capture bytes / lines | 17971 / 275 |
| capture sha256 | `11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f` |
| sha256 declared by `ExecFrontierCapture.manifest.json` (`sources[0].sha256`) | identical (`11c8d6d6…d64f2f`) |
| that manifest's own sha256 | `432f2205b368acb39d620bb85fe81c0fd6ccb345dd0878661478085ac1ce6659` |
| instrument | `corpus/instruments/source-recheck.py` sha256 `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` |
| committed target path | `corpus/source-snapshots/round-39/S057.txt` (manifest `path` field is `S057.txt`, the same relative name the round-38 S055 manifest uses) |

The manifest below declares `"path": "S057.txt"`, so it executes in any directory where the committed capture sits
under that name — the committed `corpus/source-snapshots/round-39/` directory (and the scratch replay in §3.4).

## 2. Deliverables

| file | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-39/wave1/ExecJunkRecheck.manifest.json` | 32 | 1211 | `9dafce3647086cd082ab5ebb53d9b9601fd43ff76f701e595c5503afc388470a` |
| `.ufo/waves/round-39/wave1/ExecJunkRecheck.junk-recheck.txt` | 95 | 4924 | `7d6e7df20fc546625a60c5e72a7e24cb9e6803344238f73188651c36fbffbcbc` |

`ExecJunkRecheck.manifest.json` is a schema-1 manifest with one source (`id=S057`, `path=S057.txt`, the capture's
sha256) and exactly four assertions `J1..J4`. Its four `quote` strings are the four quoted sentences of
`c2-controls/junk-f22.md` item by item (extracted with `^\d+\.\s+"(.*?)"\s+—\s+FALSE`, `re.M|re.S`, then
whitespace-collapsed — the control file wraps three of the four sentences over two lines):

```
  J1 norm_occurrences=0 len_norm=123 CISA's When to Issue VEX Information mandates a strict protocol that determines when a supplier must issue VEX information.
  J2 norm_occurrences=0 len_norm=53 Once a VEX status is issued it must never be changed.
  J3 norm_occurrences=0 len_norm=269 The When to Issue VEX Information document defines the five not-affected justification labels (component_not_present, vulnerable_code_not_present, vulnerable_code_not_in_execute_path, vulnerable_code_cannot_be_controlled_by_adversary, inline_mitigations_already_exist).
  J4 norm_occurrences=0 len_norm=123 CISA requires every VEX statement to include an exploitation-likelihood score, and its action_statement field is mandatory.
```

Every occurrence count is 0 under `normalize()` (the instrument's own comparison: `<u>`/`</u>` dropped, whitespace
collapsed, `str.count` over the whole snapshot), and every sentence is ≥ 53 normalized characters, so none is
rejected for a different reason (`MIN_QUOTE_CHARS = 12`; no empty, short, duplicate, invalid-id, stem-mismatch or
sha-mismatch path). The trailing whitespace-collapse is the only transformation applied to the control's sentences:
the delivered control file wraps them, and JSON strings cannot carry the wrap.

## 3. Transcripts (verbatim, `exit` captured per run; full file is the delivered `.junk-recheck.txt`)

### 3.1 Negative control — the four fabricated claims

```
$ python3 corpus/instruments/source-recheck.py --manifest …/ExecJunkRecheck.manifest.json --source S057
S057:sha256 OK
S057:J1 MISMATCH reason=quote-not-found
S057:J2 MISMATCH reason=quote-not-found
S057:J3 MISMATCH reason=quote-not-found
S057:J4 MISMATCH reason=quote-not-found
exit=1
```

Line accounting over the delivered transcript: `grep -c 'MISMATCH reason=quote-not-found' = 4`, `grep -c '^exit=1$'
= 1`, `grep -c '^exit=0$' = 2` (the two green controls). Exactly the expected red, and no other failure mode.

### 3.2 Positive control — the real Q1 quote (plus one one-line sentence)

```
$ python3 corpus/instruments/source-recheck.py --manifest …/positive-manifest.json --source S057
S057:sha256 OK
S057:Q1 OK normalized=markup-whitespace occurrences=1
S057:Q2 OK occurrences=1
exit=0
```

`Q1` is byte-identical to `quotes[0].quote` of `ExecFrontierCapture.manifest.json` (anchor 12):
`Whether, and when, to issue VEX information is a business decision for most suppliers and possibly a more
individual decision for independent open source developers.` The instrument's raw-substring branch reports
`raw_occurrences=0` because the PDF capture wraps that sentence across L12–L14 (`… VEX information. Whether,` /
`and when, … possibly a` / `more individual …`), so the normalized branch reports
`OK normalized=markup-whitespace occurrences=1` — a documented green (considerthese/2026-10-24 proposal 1), not a
mismatch. To also exhibit the literal `OK occurrences=1` form the same positive manifest carries `Q2`, a genuine
verbatim one-line capture sentence (`VEX users choose the most appropriate tools for their ecosystems.`, L170,
normalized occurrences 1). Exit 0 either way.

### 3.3 Isolation control — same ids `J1..J4`, same path, same sha256, genuine sentences

```
$ python3 corpus/instruments/source-recheck.py --manifest …/isolation-manifest.json --source S057
S057:sha256 OK
S057:J1 OK normalized=markup-whitespace occurrences=1
S057:J2 OK normalized=markup-whitespace occurrences=1
S057:J3 OK normalized=markup-whitespace occurrences=1
S057:J4 OK occurrences=1
exit=0
```

The red of §3.1 and the green here differ only in the `quote` strings (`J1..J4` ids, `S057.txt`, sha256, no anchors
in either). The positive and isolation manifests are reproduced verbatim in the transcript appendix, so the two
greens are re-derivable from the committed file alone.

### 3.4 Delivered-bytes replay (after the wave-1 copy)

```
$ cp .ufo/waves/round-39/wave1/ExecFrontierCapture.S057.txt $S/replay/S057.txt
$ cp .ufo/waves/round-39/wave1/ExecJunkRecheck.manifest.json   $S/replay/ExecJunkRecheck.manifest.json
$ cd $S/replay && python3 corpus/instruments/source-recheck.py --manifest ExecJunkRecheck.manifest.json --source S057
delivered manifest sha256: 9dafce3647086cd082ab5ebb53d9b9601fd43ff76f701e595c5503afc388470a
S057:sha256 OK
S057:J1 MISMATCH reason=quote-not-found
S057:J2 MISMATCH reason=quote-not-found
S057:J3 MISMATCH reason=quote-not-found
S057:J4 MISMATCH reason=quote-not-found
exit=1
```

The committed manifest bytes (not a scratch rebuild) produce the red. Run from the wave-1 directory itself the
manifest reports `S057:source UNAVAILABLE reason=missing` (`exit=2`) because the wave-1 capture is named
`ExecFrontierCapture.S057.txt` and `check_source` requires `Path(path).stem == id`; the manifest therefore targets
the committed `corpus/source-snapshots/round-39/S057.txt`, as its path field says. That is a path-semantics
artifact, not a verdict: any directory that makes the committed capture available as `S057.txt` reproduces §3.1.

## 4. Substantive falsity — each claim against the capture (line numbers of the 275-line capture)

| claim | capture counter-evidence | verdict |
|---|---|---|
| J1 "mandates a strict protocol that determines when a supplier must issue VEX" | **L80–L81**: "The decisions and timing around providing VEX information are primarily business decisions and are not determined by a strict protocol." L13–L14 repeats the business-decision scoping. | false |
| J2 "Once a VEX status is issued it must never be changed." | **L131–L135** ("Status changes"): "VEX issuers are expected to communicate any changes in status. … When the investigation has concluded, status should be updated, for example, noting that the product is 'affected' or 'not_affected.'"; **L136–L138**: "By updating a timestamp but not changing status or other information, a VEX issuer can reaffirm that the current status remains accurate at the present time." | false |
| J3 "defines the five not-affected justification labels (…)" | Labels defined elsewhere: **L18–L24** cite the separate *Minimum Requirements for VEX*, *VEX - Status Justifications* and *VEX - Use Cases* documents. Only two labels appear in the capture at all, inside the inheritance example — `vulnerable_code_not_present` (L189, 1 hit) and `component_not_present` (L189, 1 hit); `vulnerable_code_not_in_execute_path`, `vulnerable_code_cannot_be_controlled_by_adversary` and `inline_mitigations_already_exist` each occur **0** times. | false |
| J4 "requires every VEX statement to include an exploitation-likelihood score, and its action_statement field is mandatory." | **L120–L122**: "VEX does not specifically describe threat or the degree to which a vulnerability is being exploited, however, such information could be included in the 'action_statement' field." No score concept: `exploitation-likelihood` 0 hits, no scoring field named; **L139–L141** treats `action_statement` and `impact_statement` as fields that *can* convey changes, not as mandatory content. | false |

The negative control therefore reds for the right reason (unaudited prose that the source contradicts) and the
instrument's normalized comparison is what catches it — a text-only check, not a metadata check.

## 5. Reproduce (post-landing spot check)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-39   # committed S057.txt + manifest.json
cp ../../../.ufo/waves/round-39/wave1/ExecJunkRecheck.manifest.json ./junk.json      # or any dir holding a copy of S057.txt
python3 ../../instruments/source-recheck.py --manifest ./junk.json --source S057     # 4x MISMATCH reason=quote-not-found, exit 1
python3 ../../instruments/source-recheck.py --manifest ./manifest.json --source S057 # committed positive: exit 0
```

## 6. Axes

- **coverage (C2, held 7)**: the F22 negative control is now *evidenced* rather than asserted — the junk twin is
  red against the actual capture under the actual instrument, and the killing signal is the fabricated prose.
- **depth:verifiability**: the control is two-sided and byte-reproducible (delivered manifest + transcript with the
  exact positive/isolation manifest bytes), so a non-author can re-derive the verdict without reading this seat's
  scratch.
- Harm: none — the seat wrote two wave-1 files and nothing else (§7); no claim was weakened.

## 7. Write scope and hygiene

Writes: only `.ufo/waves/round-39/wave1/ExecJunkRecheck.manifest.json`,
`.ufo/waves/round-39/wave1/ExecJunkRecheck.junk-recheck.txt`, this receipt, and scratch. No lane/fleet/source-tree
file was modified; no mutating git/jj command; no install; no `agent://all` message; no subagent.

## 8. Scratch

`S=/fast/scratch/hyaku/kasegi-r39/ExecJunkRecheck/` (capture copy, three manifests, `drive.sh`, transcript,
`replay/`) removed with `rm -rf -- "$S"` after the deliverables were copied. Disk guard read before the run
(`/fast/scratch/hyaku` 24% used); nothing heavy was run.

## 9. Risks / notes

1. **Positive Q1 prints `normalized=markup-whitespace occurrences=1`, not the bare `OK occurrences=1`.** The PDF
   wraps Q1 across L12–L14, so the raw-substring branch cannot fire; the identical-bytes literal `OK occurrences=1`
   line is supplied in the same green run by `Q2` (capture L170). Both lines are `OK`, `exit=0`. Any strict grep for
   the bare form finds it (§3.2).
2. **The manifest is capture-relative.** Its `path` is `S057.txt`, so it must be executed where the committed
   capture is available under that name; in the wave-1 dir the capture is `ExecFrontierCapture.S057.txt` and the
   instrument's stem rule reports `UNAVAILABLE reason=missing` (exit 2) instead of a verdict (§3.4).
3. **The capture is a wave-1 sibling deliverable.** Identity was cross-checked against
   `ExecFrontierCapture.manifest.json` (sha256 equality). If the L1 re-captures or edits the committed capture, the
   manifest's sha256 and all four verdicts must be re-derived — the transcript records the capture digest
   (`11c8d6d6…d64f2f`) it was measured against.
