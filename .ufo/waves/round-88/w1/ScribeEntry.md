# ScribeEntry — round 88 attempt 1 (w1 leaf): one knowledge-entry candidate

## Deliverable

One candidate knowledge entry, drafted against the admitted sibling entry's form and `corpus/QUALITY.md`:

- `.ufo/waves/round-88/w1/ScribeEntry-candidate/corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md` — 227 lines, 30,021 bytes, sha256 `41a5d83bd054cb39e6891fcab03ca7746ba234415a289cd3c1cd07cc84a0c775`, 11 `##` sections, 6 balanced fenced `sh` blocks. Written only under the wave dir; nothing under `corpus/` was changed.
- `.ufo/waves/round-88/w1/ScribeEntry-receipts/checks.txt` — every measured output the entry cites (recheck line, FC-1/2/3/5/6/7), no credential value.

## What the entry says (mapped to the item)

- **Claim 1-2 (S126, Google Cloud Storage Signed URLs).** An active V4 signed URL authorizes whoever holds it ("…can use it while it's active, regardless of whether…", `corpus/source-snapshots/round-88/S126.txt:423-424`), the authority is in the query string (`:433-434`), the authorizing field is `X-Goog-Signature` (`:487-488`), and the window is `X-Goog-Date` + `X-Goog-Expires` seconds (`:481-482`) capped at 604800 s (`:483-484`).
- **Claim 3-4 (S127, Azure Create a service SAS).** `sig` is an HMAC-SHA256 over the string-to-sign, Base64-encoded (`:402-404`, `:639`); the example URI carries `sv=` and `sig=<signature>` (`:605`); the ends of a SAS are the expiration time, stored-policy deletion, or account-key regeneration (`:596-601`, quoted `:599` and `:601`), so an ad hoc SAS in a capture is a credential until one of those.
- **Claim 5 (the lane's scanner).** Scope (`corpus/instruments/capture-secret-scan.py:14-21`, including the round-88 `corpus/practice/<pkg>/evidence/` clause), shapes (`:23-45`, patterns `:80-87`), output/exit (`:57-62`, `report()` `:182-194`), allowlist semantics (`:48-55`, `:89-90`), and the docstring's named limits (`:43-45`) plus four further limits evidenced by the selftest case table (`:233-243`).
- **Claim 6 (redaction rule).** Strip the query string, keep scheme/host/path (`.ufo/waves/round-86/l1/redact-presigned.py:5-6`), and keep the pre-redaction digest beside the committed one (r86 manifest `sources[S122].redaction`); round-88 captures carry no redaction block because both read clean.

Every quoted span is ≤25 words and anchored; one literal (`sig=<signature>`) occurs twice in S127 and FC-1 declares that count of 2. The entry carries no credential-shaped value: the Azure example is quoted with its `<signature>` placeholder, and the Cloud Storage example signature is cited only by line span (`S126:466-473`), never by value.

## Gates and measured checks (all run 2026-11-07, `python3 -B`, lane root cwd)

| check | result |
|---|---|
| `bash -n` on the entry's `recheck:` line, then executed | parses; `S126:sha256 OK` + 2 `Q0n … OK occurrences=1 anchor=N-ok`, same for S127, then `scanned=2 hits=0 … rc=0`; rc 0 |
| FC-1 quote spans (`normalized=whitespace`) | `QUOTE-CHECK pass spans=11 bad=0`, rc 0 — each span ≤24 words, anchored, declared occurrence count |
| FC-2 missing-source control (`--source S999`) | `S999:source UNAVAILABLE reason=not-listed`, rc 2 |
| FC-2 corrupted-source control (byte flip in a scratch copy) | `S126:sha256 MISMATCH expected=b04de8a9… actual=b5b7c4a3…`, rc 1 |
| FC-3 digests + scanner over both captures | `b04de8a9…`/`66f8a35e…` equal to the manifest; `scanned=2 hits=0 files=0 allowed=0 unused_allow=17 rc=0` |
| FC-5 provider isolation + instrument pin | `S126 azure_sas=0`, `S127 google=0`, instrument `d7349536…` |
| FC-6 redaction tool lines + blocks | tool lines at `:5-6`; `r88_redaction_blocks=0`; r86 `pre_redaction_sha256` len 64 |
| FC-7 wrap control | rejoining `S126:466-473` yields `HIT shape=gcs-signed-url-signature … line=466`, `hits=1 … rc=1` |
| scanner over the candidate entry | `scanned=1 hits=0 … rc=0` |

No full lane census was run; no counter was run; no instrument was executed beyond `capture-secret-scan.py --files`, `source-recheck.py` (read-only) and `sha256sum`/`grep` measurement.

## Touched surfaces

- Written: the two paths above, under `.ufo/waves/round-88/w1/`.
- Read-only: `corpus/knowledge/presigned-url-credentials-in-captured-evidence.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/source-snapshots/round-88/{S126,S127,manifest.json}`, `corpus/source-snapshots/round-86/manifest.json`, `corpus/instruments/{capture-secret-scan,source-recheck}.py`, `.ufo/waves/round-86/l1/redact-presigned.py`, `.ufo/waves/round-88/{landing.json,claims.json}`, `.ufo/waves/round-88/l1/c2-landing-r88.txt`, `.ufo/waves/round-88/controls/{c2-controls-r88.sh,c2-controls-r88.txt,capture-scan-r88.txt}`.
- No git/jj writes; no edits to `corpus/`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `SHONEN.md`, the frozen `c1/`/`c2/`/`controls/`/`l1/` bytes, or any instrument. Scratch `/fast/scratch/hyaku/kasegi-r88/ScribeEntry` deleted before yield.
- Tooling: nothing installed or upgraded.

## Findings (routed as qualifiers, not re-scoring)

**F1 — a hard-wrapped signed URL is not detected, and the instrument's docstring does not name line wrapping.** The GCS shape needs 64+ contiguous hex digits (`corpus/instruments/capture-secret-scan.py:85`); the selftest pins `gcs-doc-wrapped` as clean (`:235`); S126's own example signature is wrapped at 80-character lines (`S126:466-473`), which is the only reason the pinned capture reads `hits=0` — rejoining those eight lines produces a `HIT` (FC-7, receipts). Routed qualifier for the L1: the docstring's limit list (`:43-45`) names gzip/UTF-16/base64-wrapped captures but not line-wrapped signatures, and this is the difference between "reads clean" and "carries a signature". Re-runnable: FC-7 in the candidate.

**F2 — the Azure shape requires `sv=` in the same query.** `azure-sig-without-sv` is pinned clean (`corpus/instruments/capture-secret-scan.py:242`), and Microsoft's page dates the parameter from service version 2012-02-12 (`S127:631-633`). A service-SAS query without `sv=` is outside the detector; the candidate states this as a limit rather than a defect.

**F3 — `sig=<signature>` occurs twice in S127.** Inside the example URI (`:605`) and as the table cell (`:638`). FC-1 declares `expected=2`; a re-verifier applying an exactly-once rule without the declared count would report a false failure.

**F4 — manifest fetch-instant wording (observation, not a defect).** Both round-88 records give `fetched_utc` `2026-11-07T03:30:10Z` and their `fetch_method` says "a second fetch at 2026-11-07T03:30:05Z gave byte-identical snapshot bytes" — 5 s earlier. Consistent with a fetch-start vs fetch-completion reading; not load-bearing for the claim (the `sha256` and `bytes` fields bind the bytes). Flagged for the L1 only if it wants the manifest to state which instant the field records.

**F5 — a clean scan is not absence.** The pinned S126 both reads clean and demonstrably contains a signature example; the candidate's Claim 5, Rejected item 5 and the honest limits say so explicitly, and the entry's falsifiable rule is written against the scanner's HIT line, not against its silence.

## Out of scope

- Integration into `corpus/knowledge/` (file move, `corpus/SOURCES.md` used-by rows, SCORECARD/LOG/lesson sentences) — the L1's.
- Judging C1 or C2: neither frozen claim was re-run or re-scored; the C2 landing receipt was read only, and the entry's sentences about the capability are pointed at it.
- Any live target, any credential-shaped fixture outside scratch, any fleet/sibling-lane write.

## Artifact paths (relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)

- `.ufo/waves/round-88/w1/ScribeEntry-candidate/corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md`
- `.ufo/waves/round-88/w1/ScribeEntry-receipts/checks.txt`
- `.ufo/waves/round-88/w1/ScribeEntry.md` (this report)
