# ExecC2Corpus — round 88 attempt 1

ONE v1 wave of 14 seats. Axes: depth:verifiability; coverage. Advisory only: no re-scoring of frozen claims.

## Scope and provenance

Exercised C2 landing `b43dc2154bc09470da2209fb626021da3af3593e`, read from `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-88/landing.json`. Executed landing-byte copies of scanner, capture instrument, imported gate and allowlist in `/fast/scratch/hyaku/kasegi-r88/ExecC2Corpus/`; no lane implementation changed. Scanner SHA256: `d73495364f90f78fa5ee6ad28b83fce772a349a5339d240b21db4d5d04425417`.

Plain GETs through the capture instrument returned HTTP 200 on 2026-11-07. No live signed URL was requested. Evidence directory: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-88/w1/ExecC2Corpus-receipts/`. Fetch receipts retain URL-page labels, capture digests, byte counts and timestamps; scanner receipts retain only HIT/summary lines. No page bytes or matched values retained there.

## Public examples

Each `--files` scan returned `scanned=1 hits=0 files=0 allowed=0 unused_allow=17 rc=0`; no HIT lines. Counts below count documented complete-URL examples, not repeated component-table entries or code templates.

| Page | Example / observed structure | Flags? | Expected / qualification |
|---|---|---|---|
| https://docs.cloud.google.com/storage/docs/access-control/signing-urls-manually | Completed GCS URL at captured lines 471–481; signature has 512 hex digits, wrapped into eight segments; only 21 digits immediately follow its parameter name. | No | Should detect the full-length signature if capture-level hygiene includes documented wrapped URLs. This is a representation false negative, not a live credential finding. |
| Same GCS page | Concatenation template at line 461 and generation code at line 579 use placeholders/variables, not literal full signatures. | No | Correct; no literal signature to flag. |
| https://learn.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas | User-delegation URL at line 870 has an explicit angle-bracket signature placeholder (11 characters including brackets) and a storage-version parameter. Component table repeats the placeholder at line 921. | No | Correct; placeholder, not full-length example signature. |
| https://learn.microsoft.com/en-us/rest/api/storageservices/create-account-sas | Account URL at line 587 has the same explicit 11-character signature placeholder and storage-version parameter; repeated at line 619. | No | Correct; placeholder, not full-length example signature. |
| https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-creating-signed-url-canned-policy.html | Example URL at line 13 has a 172-character CloudFront signature and a public-key identifier. Parameter explanations at lines 70/74 and the concatenation at line 212 are templates. | No | Full-length example should be flagged by a general signed-URL detector, but CloudFront is explicitly outside this scanner's documented shapes (landing scanner lines 43–45). Known coverage gap, not a C2 regression. |

**Bounded verdict:** among four completed URL examples: zero false positives; one representation false negative within the GCS addition; one additional known/out-of-scope CloudFront miss; two correctly ignored Azure placeholders. These are shape/hygiene classifications, not claims that public documentation examples remain usable credentials. There are no full-length Azure signature examples on these fetched pages, so they cannot establish positive Azure detection sensitivity.

### Routed defect: line-wrapped GCS signature

The GCS capture loses detection because the matcher requires 64 contiguous hex digits. A diagnostic unwrapping of only captured lines 471–481 produces `HIT shape=gcs-signed-url-signature ... line=1` and `scanned=1 hits=1 files=1 ... rc=1`. Receipt: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-88/w1/ExecC2Corpus-receipts/gcs-unwrapped-scan.txt`; derived-byte SHA256 is in `digests.txt` in that directory. No fixture values retained.

Re-run command (writes only disposable scratch; uses the public page above, never its signed example as a network target):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && S=/fast/scratch/hyaku/kasegi-r88/ExecC2Corpus && mkdir -p "$S" && trap 'rm -rf -- "$S"' EXIT && export TMPDIR="$S" && python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py --id gcs --url https://docs.cloud.google.com/storage/docs/access-control/signing-urls-manually --out "$S/gcs.txt" && python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py --files "$S/gcs.txt"; python3 -B -c 'import pathlib,os; p=pathlib.Path(os.environ["TMPDIR"]); (p/"gcs-unwrapped.txt").write_text("".join((p/"gcs.txt").read_text().splitlines()[470:481])+"\n")' && python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-secret-scan.py --files "$S/gcs-unwrapped.txt"
```

Expected on captured page bytes: original rc 0, unwrapped rc 1. Future page changes can shift line numbers; compare fetch digest before using this bounded slice. Replay uses current lane instrument, which must match the landing digest above.

## Landing corpus sweeps

Executed arguments: `python3 -B /fast/scratch/hyaku/kasegi-r88/ExecC2Corpus/capture-secret-scan.py --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --rev b43dc2154bc09470da2209fb626021da3af3593e`.

- Normal scope: `scanned=1414 hits=0 files=0 allowed=18 unused_allow=0 rc=0`.
- Whole-tree diagnostic: same command with `/fast/scratch/hyaku/kasegi-r88/ExecC2Corpus/diagnostic-scan.py`; only change was replacing the `is_capture_path` body with `return True`. `scanned=16727 hits=51 files=34 allowed=18 unused_allow=0 rc=1`.
- New-shape HIT list by path, line, shape: **empty** in both sweeps (GCS zero; Azure zero).
- Whole-tree non-new-shape histogram: credential 20; op-ref 13; private-key 8; aws-access-key-id 6; aws-sts-session-token 3; bearer 1. These 51 diagnostics are not classified here as real secrets or false positives: whole-tree includes instrument fixtures and historical records. Full value-free path/line/shape output is retained in `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-88/w1/ExecC2Corpus-receipts/whole-tree-scan.txt`.

Thus zero observed new-shape false positives in either corpus sweep, but no positive examples there and no exhaustive false-negative claim. Scanning emits first non-allowed match per file/shape, not occurrence totals.

## Handoff

Written: this report and `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-88/w1/ExecC2Corpus-receipts/{gcs-fetch,gcs-scan,azure-user-fetch,azure-user-scan,azure-account-fetch,azure-account-scan,cloudfront-fetch,cloudfront-scan,scoped-scan,whole-tree-scan,gcs-unwrapped-scan,digests}.txt`.

No tools installed; no build/lint/formatter/counter suite run. No LSP tool is mounted; no lane symbol refactor performed. Parent owns wave-file hygiene gate. Scratch removed before yield. No blocker.

Self-evaluation (1–5): accuracy 4 (example credential validity intentionally untested); completeness 4 (Azure pages contain no positive literal example); clarity 4 (distinguishes representation miss from explicit CloudFront limit); actionability 4 (slice replay depends on captured page digest); conciseness 4 (replay adds length). Mean 4.0. Highest-impact improvement would be a capture-normalization regression case for the observed wrapping, subject to L1 scope approval. User agreement expected because every conclusion is bounded to retained receipts.
