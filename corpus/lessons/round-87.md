# Round 87 — lesson (kasegi, attempt 1)

Read first: the r86 closure, `corpus/lessons/round-86-verifier-spotcheck.md` (routed defects 1–6, operator note on the pushed STS token) and `corpus/lessons/round-86.md`. Base `cd1f568a6be2656b5f5dc479eb90ef99b91131b5`, freeze `afb13a88e6fbc8e2f8a0c11f9cfbfde77e907e69`, C1 landing `d87b1b55a51d78411438e962a9abbebdd17930cd`, C2 landing `132e16c588a2424c06b5ca15ea01fce1ee9a396d`. The frozen claims, predicates, kill rules and executed controls are in `.ufo/waves/round-87/claims.json` and `.ufo/waves/round-87/controls/`. One v1 wave `w1` ran 12 seats; the reports are under `.ufo/waves/round-87/w1/`.

## Claims

- **C1 — depth:verifiability (lowest axis, score 4; internal-citation repoint, score not claimed to move).** Knowledge-scope tranche 2: the frozen map `.ufo/waves/round-87/c1/repair-map.json` repoints 83 distinct bare snapshot citations (S029 ×1, S040 ×1, S069 ×10, S100 ×1, S102 ×70) whose basename is held by exactly one tracked file under `corpus/source-snapshots/` (the r86 counter also counted `.ufo/` fixture copies; ReviewC1Semantics r86 routed candidate 1). The four quoted manifest-field tokens of r86 Finding 1 are excluded by a new limb M7. Meter 596/1720 → exactly 678/1719; counter `.ufo/waves/round-87/c1/knowledge-meter.py` (M1–M7).
- **C2 — coverage, capability acquisition `capture-secret-scan` (sourced: S124, S125).** `corpus/instruments/capture-secret-scan.py` scans captures (snapshots, `*-receipts/`, `live-*`) at a revision or a file list with the claim-package gate's SECRET_PATTERNS plus two AWS shapes grounded in S124/S125, under a digest-bound allowlist. Frozen counter `.ufo/waves/round-87/c2/capability-check.py` (K1–K5). It answers r86 spot-check routed defect 1 (M86-2's fix was stated, not a committed check).

## Outcome

- **C1:** P1 (counter `KNOWLEDGE-METER-RESULT pass rc=0`, after 678/1719, M1–M7) and P2 (13/13 pins) hold at `d87b1b55`; **P3 is false**: the landing commit also carries `.ufo/waves/round-87/w1-spec.json`, `w1-dispatch.json` and `w1/swarm-registry.json` (`.ufo/waves/round-87/l1/c1-landing-r87.txt`, `outside corpus/knowledge/: 3`). Kill rule: NOT VERIFIED. The knowledge-scope diff itself is exactly the map (M3 bad_lines=0). See M87-2.
- **C2:** K1–K5 pass and P2 holds at `132e16c5` (`.ufo/waves/round-87/l1/c2-landing-r87.txt`: K2 `rc=1 sts_files=2`, K3 `hits=0 allowed=18 unused_allow=0`, K4 exact planted set, STS allowlist row refused rc 2). VERIFIED on its frozen predicates.

## Gate

### S124 — AWS IAM User Guide, Create a signed AWS API request (SigV4) (admitted, used by the instrument)

- **URL:** https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv-create-signed-request.html, HTTP 200.
- **Accessed:** 2026-11-07 (captures at 01:54Z and 02:01:46Z, byte-identical).
- **Capture:** `corpus/source-snapshots/round-87/S124.txt`, sha256 `88d4f703cef1b9d1cead11053dd9f02692bd4629a7110e42caecc74a2fc2f1cb`, 437 lines; manifest `corpus/source-snapshots/round-87/manifest.json`, `source-recheck.py` rc 0.
- **Located quote, S124.txt:83-85 (20 words):** "you must add X-Amz-Security-Token to the Authorization header or include it in the query string to hold the session token". Also pinned: :409 the documented example key id `AKIAIOSFODNN7EXAMPLE` (the instrument's one allowed value).
- **Row change (old → new):** status `queued` (freeze) → `mined`; used-by `—` → `corpus/instruments/capture-secret-scan.py, corpus/knowledge/presigned-url-credentials-in-captured-evidence.md`.

### S125 — AWS IAM User Guide, IAM identifiers (admitted, used by the instrument)

- **URL:** https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html, HTTP 200.
- **Accessed:** 2026-11-07 (two byte-identical captures).
- **Capture:** `corpus/source-snapshots/round-87/S125.txt`, sha256 `65c99351e731b743f18243e93613da7e05b4030d5fe2060a6cc484a320de55fe`, 363 lines.
- **Located quote, S125.txt:330-332 (19 words):** "ASIA / Temporary (AWS STS) access key / IDs use this prefix, but are unique only in combination with the secret". Also :318-319 "AKIA / Access key" (the table renders one cell per line; single-cell quotes are too short for `source-recheck.py`, so the manifest pins :303, :331, :332).
- **Row change (old → new):** status `queued` → `mined`; used-by `—` → `corpus/instruments/capture-secret-scan.py, corpus/knowledge/presigned-url-credentials-in-captured-evidence.md`.

### Rejected this round

- **Amazon S3 API Reference, "Authenticating Requests: Using Query Parameters (AWS Signature Version 4)"** — https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-query-string-auth.html, HTTP 200 on 2026-11-07, but the served page is a 2,343-byte meta-refresh shell to `Welcome.html` (`<meta http-equiv="refresh" content="0;URL=Welcome.html">`); `capture-source.py` wrote a 10-byte snapshot. Reason: no capturable text at that URL, so no located quote is possible. Flip condition: a direct-HTML URL for the same page that `capture-source.py` captures with the X-Amz-Security-Token paragraph. S124 (IAM guide) states the same rule and replaces it.

### considerthese and assimilation

- **considerthese:** the still-unimplemented proposal that fits C2 is `considerthese/2026-10-24.md:49-52` (2026-10-24: "Fix snapshot capture to store clean text" — upstream capture hygiene; ConnectorOverlap §3-4 pairs it with an intake gate in `capture-source.py` that calls the scanner before a snapshot is written). Not implemented this round; routed to round 88 as the intake-gate move (ReviewC2Scanner F3 and CriticClaims F6 make the same point: the `--files` pre-commit mode is not wired).
- **Assimilation: none.** Lane 125 ids, staged 94, collisions 94/94 (the staged file predates the lane's S031–S125 expansion); the guard proof on an indented `  | S002 |` row gives a nonempty set while the column-zero pattern gives none (`.ufo/waves/round-87/assimilation/guard-proof.txt`). The r77 L0 question stays open.
- **Admitted curation (not a claim):** `corpus/knowledge/presigned-url-credentials-in-captured-evidence.md` (ScribeEntry draft, L1-reviewed; `verified-at` corrected to the UTC date 2026-11-07). It cites S124, S125 and S122.
- **Erratum (ScoutSources D-1):** the manifest quote `S125:Q01-prefix-intro` is declared at anchor 303, but the sentence starts on line 304 (303 is the heading "Understanding unique ID prefixes"); `source-recheck.py` accepts it, so its anchor check tolerates a one-line offset. The manifest is a frozen pin of this round and is not edited; correct the anchor and test the tolerance in round 88.

## Mistakes

**M87-1 — class `pipe-deadlock-in-candidate-instrument`.**

- **What happened:** the first C2 candidate (`b3164f3f`) wrote every blob id to `git cat-file --batch` before reading any answer. Past ~1,560 ids the request exceeds the pipe buffer and both processes block. The lane's capture scope is ~1,316 files today, so the candidate passed its positive control and would have hung silently as the lane grew. Two control batteries hung (`.ufo/waves/round-87/controls/c2-controls-r87-attempt1-timeout.txt`, `...-attempt2-timeout.txt`) on the scope-widening forgeries, the only controls whose scope crossed the threshold.
- **Captured-by:** the pre-freeze forgery controls (whole-tree and corpus-wide scope), though as hangs rather than verdicts; no selftest exercises volume.
- **Fix:** request/response interleaving in `read_blobs` (one id written, its answer read) before the freeze; the final battery's whole-tree control scans 16,572 blobs and returns a verdict (`.ufo/waves/round-87/controls/c2-controls-r87.txt`).
- **Shown able to fail:** the two hung batteries are the failing evidence; the fixed instrument scans 16,567 blobs at `master` in 14 s (L1 timing, recorded in the C2 controls receipt header run).

**M87-2 — class `unscoped-path-list-swept-into-landing`.**

- **What happened:** the L1 built the C1 landing commit's path list from `git status --porcelain | awk '{print $2}'`, which also listed three untracked wave files (`w1-spec.json`, `w1-dispatch.json`, `w1/swarm-registry.json`). The helper committed them with the five knowledge files, so the frozen P3 ("the landing diff lists only corpus/knowledge/ files") is false at `d87b1b55` and C1 is not verified, although its counter passes.
- **Captured-by:** none before the commit; P3 caught it after.
- **Fix:** QUALITY R139 — derive a landing path list from `git status --porcelain -- <scope>` and run `.ufo/waves/round-87/l1/landing-scope-check.py` before citing the landing.
- **Shown able to fail:** `.ufo/waves/round-87/l1/r139-check-r87.txt` prints `outside=3 verdict=FAIL exit=1` on `d87b1b55`, `PASS` on the C2 landing and on the round-86 C1 landing `fdb5f4af`.

## Routed-defect disposition (r86 spot-check §6)

| # | r86 routed defect | r87 disposition |
|---|---|---|
| 1 | Capture secret hygiene: committed check with a self-test | Answered by C2: `corpus/instruments/capture-secret-scan.py` (selftest 19 cases), QUALITY R138, run over every capture-class file at `132e16c5` (hits=0) and at `252df0c9` (the two STS files flagged). History inventory: ExecC2History. |
| 2 | S122 `scope` cell edited in place (CORPUS rule 2) | Recorded as a named correction in `corpus/SOURCES.md` Registry changes (round-87 line). Not exempt: rule 2 allows only `status`, `recheck`, `used-by` in place, and the row was already pushed. The r86 edit stays as history; the correction line names old and new text. |
| 3 | Reject-reason date for the IBB 80/20 split | Corrected here: the comparison date for the 2023 award is the S122 record's dates (IBB report submitted 2023-05-23, disclosed 2023-06-25), not "2023-05-17" (that is curl's advisory date). The ruling is unchanged: the split is first archived 2024-07-27, after both dates. |
| 4 | Frozen pins at tip (S122, round-86 manifest) | Not repeated: r87 pins (`claims.json` `instruments`) exclude every file the round edits after the freeze; the redacted S122 bytes are not pinned by any r87 claim. |
| 5 | Mixed citation forms (33 map keys bare in prose) | Prose rule stated: a bare `S###.txt` name in running prose beside a repointed backtick citation is a mention, not a citation; `resolve.py` does not count it and the repoint maps only backticked tokens (M3). No repoint of prose mentions. |
| 6 | Carried: E0 binds labels not body; stale census of record; empty r86 results.json | Carried unchanged: no package claim this round; census not regenerated (full census ~13 GB with ~9 lanes live). |

## Wave findings routed to round 88 (none re-scores a claim)

- **C2 scope (ReviewC2Scanner F1, CriticHarm Q-87-2):** `is_capture_path` misses `corpus/practice/*/evidence/` (where practice packages keep their captures, including the redacted S122 copy), plain `receipts/` dirs and 15 tracked raw HTTP/HTML fetches under `.ufo/waves/`. A whole-tree scan at the tip finds no STS value anywhere; the hits are fixture literals in the scanner/counter and old seat fixtures (L1 receipt `.ufo/waves/round-87/l1/whole-tree-scan-r87.txt`).
- **C2 detection gaps (ReviewC2Scanner F2, F4–F8; ScoutSources §5):** HAR-style name/value JSON, percent-encoded names, UTF-16/gzip/base64 captures; allowlist keyed on the literal `--files` path; digest binds the matched prefix, not the whole value; symlinks unread; no GCS/Azure/CloudFront signed-URL shapes (leads L1–L4 with first-party URLs in ScoutSources §4).
- **C2 counter (ReviewC2Scanner F3, MutC2Scanner 14 killed / 5 survived, MutC2Counter 12/19 killed):** no limb exercises `--files`; header/JSON STS forms are attested only by the selftest; survivors include STS case folding and a relaxed HEX64.
- **C1 counter (MutC1Counter 19/28 killed, the 9 survivors equivalent or killable by named controls):** add duplicate-basename, appended-line, extra-file and range-edge controls.
- **CriticClaims F2/F4:** commit the claim→commit mapping (landing.json now committed) and bind the meter's base reading to a tree.
