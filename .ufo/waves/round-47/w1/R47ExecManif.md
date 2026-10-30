# R47ExecManif — manifest and capture verification

## Result
- Manifest SHA-256 verified: `6168521b5f5555fd06f2a63c1dc0e8543cd89f8146f79f684daf586f32f35e9b` (`sha256sum` of `corpus/source-snapshots/round-47/manifest.json`).
- `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-47/manifest.json --source S075`: passed; `S075:sha256 OK`; all ten quotes OK with occurrence count 1 and matching anchors (21, 23–26).
- Same command for `S076`: passed; `S076:sha256 OK`; all twelve quotes OK with occurrence count 1 and matching anchors (568, 571, 575, 582–584, 589, 596, 598–600).
- Using committed `corpus/instruments/capture-source.py` (`--kind html`), fetched each manifest URL twice into scratch. S075 both recaptures: `9dee8161347af85ed0c65d1d296a2d432fdb67f9a86017d36427166b4bad04e1`, equal to committed S075 SHA. S076 both recaptures: `9bd8ab57dac9cc605355c60831f51e02b92f5e34990aa99a49566d207e6bbb38`, equal to committed S076 SHA. All four requests returned HTTP 200; fetched byte counts were 25,321 (S075) and 582,877 (S076). Thus each pair was deterministic and both matched the committed snapshot digest.
- S076 manifest lines 92–95 pin `body_lines` to 558–600. In `corpus/source-snapshots/round-47/S076.txt`, lines 558–600 are policy prose (e.g. 558 and 567–600); boundary chrome printed/read includes 556 `In this article`, 559 `Copy markdown`, 562–566 article navigation/TOC, and 601–610 footer/support chrome. This supports the asserted F29 body/prose range, not the surrounding navigation/footer.

## Evidence and control
Commands exercised were the two `source-recheck.py` invocations and four `capture-source.py` invocations described above; their printed results are recorded here. The do-nothing control for capture comparison is the existing committed snapshot bytes/digest in the manifest: unchanged output matching each pinned digest (and matching across two independent captures) is the zero-drift control; no source or manifest files were modified. This is a reproducibility receipt for S075/S076, not a run of either frozen routed-defect counter.

## Limitations
This verifies the live URL captures at the time of this run and the pinned local quote/anchor checks; it does not prove future remote content stability or broader counter coverage. No tools were installed. Scratch captures were removed on command exit.
