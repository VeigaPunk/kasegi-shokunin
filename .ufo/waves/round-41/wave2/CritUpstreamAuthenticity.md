# CritUpstreamAuthenticity — S063 upstream authenticity

## Axes
- **depth:verifiability:** separates pinned-capture integrity from live-source authenticity.
- **coverage:** checks the F24 entry's RFC statements against the current publisher response.

## Reproduced live check
- URL: https://www.rfc-editor.org/rfc/rfc9116.txt
- Retrieved 2026-10-27T11:44:20Z UTC using the required curl user-agent; HTTP 200, 45,129 bytes, 1,122 lines; SHA-256 `79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9`.
- Committed capture `corpus/source-snapshots/round-41/S063.txt` is 39,301 bytes / 842 lines, SHA-256 `925512e715be5fae950f3eec88805197d4007875dac825c5603d44d2b71e2faa`. The entry itself describes it as `capture-source.py --kind text`'s collapse (knowledge entry line 4). These digests are of different representations, so their inequality proves neither a revision nor content mismatch.
- Independently re-ran `source-recheck.py --manifest corpus/source-snapshots/round-41/manifest.json --source S063`: `S063:sha256 OK`, Q1/Q2/Q3 OK, each normalized markup-whitespace, occurrences=1, expected capture anchors 330/270/235. This proves the manifest digest and pinned quote occurrence/anchor assertions against the committed capture; it does not contact the URL and cannot establish who supplied the capture, whether it was faithfully transformed from the response, or that the upstream has not changed since retrieval.

## Source comparison / counterexample
The entry's factual core checked against this live response: §2.5 optional-by-default rule and §2.5.3/§2.5.5 required fields; §2.5.4 key-pointer (not key-in-field) and narrowly scoped email-encryption recommendation; §2.5.5 Expires/stale semantics; §3 well-known path and retrieval requirements; §3.1 host scope; §5.5 no implied testing permission. They agree. The three pinned claims agree verbatim after whitespace normalization, each once in live content, at RFC §3 (well-known path), §2.5.5 (recommended <1-year horizon), and §2.5.3 (email contact encryption recommendation). No material quote/fact mismatch reproduced.

Strongest counterexample to any claim that source-recheck validates external authenticity: rerunning it succeeds even though its input is only the local manifest+capture and it performs no network request (the output is `sha256 OK` plus three capture quote checks). The knowledge entry line 5 accurately names this a pinned-capture comparison, not fresh network validation; line 4 separately records a fetched representation and timestamp. Thus this is a boundary of the instrument, not a defect hidden by the entry. The fetch establishes what the named URL returned at the recorded retrieval time under this request, not enduring publisher authenticity, transport trust beyond HTTPS, nor that a later response is identical.

## Other counters exercised
Frontier recheck: `entries=27 pass=27 exit=0`, including F24 PASS ids=S063. Binding: records=63 bound=63 unbound=0. Recheck audit: expected=60 missing=0 unexpected=0 exit=0. These support corpus consistency, not upstream truth.

## Finding and smallest safe correction
No source-content mismatch found; no correction to the entry/capture is justified. Preserve the explicit distinction already present between live fetch metadata and normalized pinned capture, and describe source-recheck only as local capture verification. Do not present the unequal hashes as evidence of change or as proof of byte identity. No final Y verification performed.
