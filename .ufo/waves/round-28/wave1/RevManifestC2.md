# RevManifestC2 — independent Q9 review of `corpus/source-snapshots/round-28/manifest.json`

- date=2026-10-25 (UTC) lane=/home/vgpnk/Projects/shokunin/kasegi-shokunin seat=RevManifestC2 (reviewer, C2 coverage)
- state=POST-LANDING. First dir listing showed `round-28/` holding only S041.txt + S042.txt; ExecManifest
  landed `manifest.json` during review (confirmed ~2026-10-25T17:28Z). All numbers below were re-run
  on the landed bytes, not pre-state scratch.

## Subject bytes
- manifest.json: 5038 B, sha256=`e62ddad133ffc19ebc66822c0fcb3b48ed4993c101f05262302acc58714f291d`
  (matches ExecManifest's receipt claim of `e62ddad1…`, 5038 B).
- S041.txt: 2354 lines, sha256=`e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`
  (matches ExecCaptureS041's logged `sha256_disk`; byte-identical to the round-26 capture per their cmp).
- S042.txt: 974 lines, sha256=`b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966`.

## (1) path stem == id — PASS
`S041.txt`→stem `S041`; `S042.txt`→stem `S042`. Mechanical check (python `Path.stem`): `stem==id:True`
for both records. No id/path divergence.

## (2) sha256 pin == on-disk capture — PASS
Independent `sha256sum` of both captures equals the manifest values, pasted in the subject block:
S041 `e18acbf9…4a47` == pinned `e18acbf9…4a47`; S042 `b432ec16…9666` == pinned `b432ec16…9666`.
`source-recheck.py` agrees: `S041:sha256 OK`, `S042:sha256 OK`.

## (3) every quote exactly-once or anchored — PASS (no named failure)
Per-quote re-runs on the landed captures. `grep-c` = lines containing the quote
(`grep -F -c '<quote>' <capture>`); `grep-o` = occurrence count (`grep -F -o` piped `wc -l`);
`norm` = occurrence count under the instrument's declared normalization
(`<u>`-markup stripped, whitespace collapsed — matches QUALITY Q8 `normalized=markup-whitespace`).

| record | quote | grep -c | grep -o | norm | anchor | Q9 |
|---|---|---|---|---|---|---|
| S041 | Q1 | 1 | 1 | 1 | none | PASS |
| S041 | Q2 | 1 | 1 | 1 | none | PASS |
| S041 | Q3 | 1 | 1 | 1 | none | PASS |
| S041 | Q4 | 1 | 1 | 1 | none | PASS |
| S041 | Q5 | 1 | 1 | 1 | none | PASS |
| S041 | Q6 | 1 | 1 | 1 | none | PASS |
| S042 | Q1 | 1 | 1 | 1 | none | PASS |
| S042 | Q2 | 1 | 1 | 1 | none | PASS |
| S042 | Q3 | 1 | 1 | 1 | none | PASS |
| S042 | Q4 | 1 | 1 | 1 | none | PASS |
| S042 | Q5 | 1 | 1 | 1 | none | PASS |
| S042 | Q6 | 1 | 1 | 1 | none | PASS |

- No quote occurs twice; no `anchor` key exists in the manifest (none required — all 12 are
  exactly-once). **No twice-without-anchor quote exists to name; Q9 kill-rule condition absent.**
- All 12 quotes match raw (`source-recheck` printed no `normalized=` prefix, no `anchor=` note).
- Q9's third conjunct — the check prints the observed count — holds: the instrument's own run
  prints `occurrences=1` per assertion (pasted below); my grep columns independently reproduce 1.

## (4) quotes ≤ 25 words — PASS
Whitespace-token counts (mechanical `len(quote.split())`): max 5 (S041 Q4, S041 Q6, S042 Q5 at 1–5).
Normalized character lengths: 16–93; longest is S042 Q1 at 93 chars (~a single sentence,
well inside any 25-word reading of Japanese). Note: Q3's "≤25 words" is stated for English;
for unsegmented Japanese the whitespace-token reading is the mechanical proxy and passes trivially —
recorded, not a finding.

## (5) source-recheck.py exits — pasted verbatim
```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041
S041:sha256 OK / S041:Q1..Q6 OK occurrences=1    → S041_exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042
S042:sha256 OK / S042:Q1..Q6 OK occurrences=1    → S042_exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json
S041:sha256 OK  S041:Q1..Q6 OK occurrences=1  S042:sha256 OK  S042:Q1..Q6 OK occurrences=1  → full_exit=0
```
Cross-instrument agreement: ExecHarnessC2's `check_q9.py` (wave1 scratch, asserts the conjuncts the
exit code does not — stem==id, anchor notes) reports `PASS S041 … anchor_defects=0`,
`PASS S042 … anchor_defects=0`, `q9 ids=2 failures=0`, `gate_exit=0`.

## Informational (outside Q9's binding surface)
- `location` is documentation the instrument does not read; I still verified each cited line number
  holds the quote under the same normalization: all 12 cited lines (S041 L340/L212/L249/L648/L1916/L305;
  S042 L145/L131/L123/L142/L153/L171) hold. No documentation drift.
- ExecManifest's fix log is consistent with the landed bytes: landed digest `e62ddad1…` (verified above),
  the earlier short-quote draft (`fa1f366f…`) is not the committed file — nothing to flag.

## Verdict
Q9: PASS. Stems==ids, pins==disk, all 12 quotes exactly-once with observed counts printed, no anchor
obligations, word bar met, source-recheck exits 0 on both ids and the full run. **0 findings.**

## Residual risks / gaps (not findings)
- `corpus/source-snapshots/round-28/` was entirely untracked at review time (`??`); the L1's commit of
  the manifest+captures is what makes the pin durable.
- If a capture is rewritten after this pin, the digest line goes MISMATCH — detected by the re-run
  command below.
- The anchor limbs (`anchor=N-ok`, `anchor=BROKEN`) were not exercised by this manifest because no
  record needed one; coverage of those limbs lives in ExecHarnessC2's fixture matrix, not here.
- Mid-review landing race noted for the record; no PRE-STATE downgrade remains.

## Post-change re-run (if manifest or captures are amended before commit)
```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json && \
sha256sum corpus/source-snapshots/round-28/S041.txt corpus/source-snapshots/round-28/S042.txt corpus/source-snapshots/round-28/manifest.json && \
python3 .ufo/waves/round-28/wave1/ExecHarnessC2/check_q9.py corpus/source-snapshots/round-28/manifest.json S041 S042
```
Expect: recheck exit 0 with all `OK occurrences=1`; digests `e18acbf9…`/`b432ec16…`/`e62ddad1…`;
gate `q9 ids=2 failures=0`.
