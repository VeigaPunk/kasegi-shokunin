# RevCaptureNormalization — S063 byte and normalization review

## Axes
- **depth:verifiability:** independently compare fetched bytes, normalized capture, manifest claims, and recheck behavior.
- **coverage:** verify S063 represents the claimed complete RFC and is bound to its source.

## Reproduced evidence
- Independently fetched `https://www.rfc-editor.org/rfc/rfc9116.txt` with the prescribed curl UA on 2026-10-27 (HTTP 200; 45,129 bytes). Raw SHA-256: `79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9`; raw line count: 1,122; UTF-8 BOM present; zero CR bytes.
- Re-derived the capture with the committed `capture-source.py` `collapse()` implementation. Output is byte-identical to `corpus/source-snapshots/round-41/S063.txt`: 39,301 bytes, 842 LF-terminated lines, SHA-256 `925512e715be5fae950f3eec88805197d4007875dac825c5603d44d2b71e2faa`.
- The leading BOM is preserved as the capture’s first line (`ef bb bf`), which contains no document text. The 280-line raw/capture line-count difference is consistent with normalization dropping blank lines (manifest says three blank lines) and counting the BOM-only first raw line; it does not indicate a sliced capture. Captured document line numbering corresponds to normalized lines, as manifest scope states.
- S063 manifest values for fetched size/raw digest/raw lines and snapshot size/digest/line count exactly matched these independently measured values. `source-recheck.py --manifest .../manifest.json --source S063` returned `S063:sha256 OK`, with Q1/Q2/Q3 all `OK`, occurrence count 1, and anchors 330/270/235 `ok`.

## Finding / disposition
No actionable mismatch or misleading capture/manifest claim reproduced. The live-body digest and capture digest differ because the declared text normalization changes the representation; neither value is misrepresented as the other. Recheck verifies the committed normalized snapshot and pinned quote assertions; it does not independently establish future identity of the live upstream document, which is appropriately not claimed as such by this capture evidence.

## Verification limits
A single live fetch was observed; this review does not claim persistent upstream identity or independently reproduce the historical fetch timestamp. No files beyond the permitted report and scratch were written. No tools installed.
