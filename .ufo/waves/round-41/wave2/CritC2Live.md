# CritC2Live — C2 live-source falsification

## Axes
- **depth:verifiability:** live retrieval, immutable capture digest, exact quote multiplicities, and section-anchor checks.
- **coverage:** F24/S063 entry’s source claims and useful grounded benefit.

## Reproduced evidence
- Live RFC URL returned HTTP 200 on 2026-10-27T11:40:58Z; 45,129 bytes / 1,122 lines; SHA-256 `79d19ce7a4a35496981095a27fd992797a9fc4d6f3649c2a1e14f494607c61f9`.
- Committed capture `corpus/source-snapshots/round-41/S063.txt`: SHA-256 `925512e715be5fae950f3eec88805197d4007875dac825c5603d44d2b71e2faa`.
- Finding: live-body digest differs from committed capture digest. This does **not** demonstrate an RFC revision: entry provenance explicitly says capture-source.py --kind text collapses the live body to a different representation. Thus the digest comparison is not byte-equivalent and cannot support either a changed-source claim or byte-identical source claim.
- Whitespace-normalized Gate quotes each occur exactly once in live bytes and once in capture: (1) “organizations MUST place the \"security.txt\" file under the \"/.well-known/\" path”; (2) “It is RECOMMENDED that the value of this field be less than a year into the future to avoid staleness.”; (3) “When the value of this field is an email address, it is RECOMMENDED that encryption be used”.
- `source-recheck.py --manifest corpus/source-snapshots/round-41/manifest.json --source S063`: `S063:sha256 OK`; Q1/Q2/Q3 each `OK`, `occurrences=1`, anchor respectively 330, 270, 235 `-ok`.
- Entry provenance trio appears first (lines 3–5): `source`, `verified-at`, `recheck`. RFC anchors named in the entry resolve in capture section headings. I found no nonexistent section anchor. Its concrete benefit is grounded: discovery format provides researchers with a machine-parsable place/contact route (capture §1.1 and §2); entry limits this to the standard, not an organization’s actual practice.
- Re-ran coverage counters: frontier `entries=27 pass=27`; capture binding `records=63 bound=63 unbound=0`; audit `expected=60 missing=0 unexpected=0`; source census exit 0, reporting only the recorded W04 duplicate URL warnings S028/S029 and final `ok`.

## Smallest safe correction / disposition
Do not call the differing SHA-256 values evidence that RFC 9116 changed: the committed object is a normalized capture, while the live object is the fetched representation. Retain both digests and clarify the representation distinction if presenting them comparatively; no entry/capture change is justified by this probe. No confirmed C2 falsification found in quote occurrence, section anchors, provenance ordering, or counters.
