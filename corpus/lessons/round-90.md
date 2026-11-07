# Round 90 — lesson (kasegi, attempt 1)

Read first: the r89 closure (`admitted`) and `corpus/lessons/round-89-verifier-spotcheck.md` (both claims verified; routed defects 1–6), `corpus/lessons/round-89.md` (M89-1..3). Base `6088c3eb0c29040415c69e7b5fb91e110480ab26`, freeze `33f43db99c06e89bb9fb78c538313e9450da649f`, C1 landing `4a7e676895d3fc74e18c853457c9b465ade2ddf5`, C2 landing `643ddb4379536e7a5ff7cdfe5c5befe9afbf63f2`, landing receipts `779062a3676cc6b10bf855f18ff897baf0cc6fd5`. Frozen claims, predicates, kill rules and executed controls: `.ufo/waves/round-90/claims.json`, `.ufo/waves/round-90/controls/`.

## Claims

- **C1 — depth:verifiability (lowest axis, score 4; internal-citation repoint, score not claimed to move).** Tranche 5: 34 citing sites in `corpus/knowledge/triage-thresholds.md` that the round-89 non-author seat ReviewC1Labels labelled WRONG with a supported range, repointed per site (map `.ufo/waves/round-90/c1/repair-map.tsv`); 4 WRONG-with-range sites excluded because the label reason says the row content itself is stale or unsupported (`c1/excluded.tsv`: lines 152, 155, 249, 438). Counter successor pins every reading to the measured revision (routed defect 1). Meter 812/1827 → exactly 843/1829.
- **C2 — coverage (score 8 held), capability acquisition `capture-intake-gate` (sourced: S131).** `capture-source.py` scans each capture with `capture-secret-scan` before the snapshot file is opened and refuses on a hit (exit 3, nothing written, an existing file kept, shape and line only), fails closed when the scanner or allowlist cannot load, and honours the digest-bound allowlist per path. This is the `considerthese/2026-10-24.md:49-52` intake-gate proposal, routed in rounds 87, 88 and 89; its stated flip condition (a round without a `capture-secret-scan` claim) holds.

## Outcome

- **C1:** P1 `KNOWLEDGE-METER-RESULT pass rc=0` (M0 base 812/1827, M1 after 843/1829, M3, M4, M5, M6, M9 34/34), P2 pins equal, P3 one path (`.ufo/waves/round-90/l1/c1-landing-r90.txt`).
- **C2:** P1 `CAPABILITY-CHECK-RESULT pass rc=0` at a run-time seed, 9090 and 1 (G0–G6, P), P2 landed sha256 `0630d32b…` = frozen candidate, P3 three paths (`.ufo/waves/round-90/l1/c2-landing-r90.txt`). Live demonstration: S131 re-captured through the landed gate, rc 0, sha256 equal to the committed snapshot.
- **Correction (routed defect 1):** the round-89 report's and `tip-reading-r89.txt`'s "814/1827 at `b9fcf005`" is not a re-derivable number. The pinned reading of `b9fcf005` is **812/1827**, identical on the live lane and a clean clone (`controls/c1-controls-r90.txt`, environment receipt); the round-89 meter reads 815 live and 814 in a clean clone of the current tip, and the r89 closure read 812 in its clone at `eb5f0df8`.

## Gate

### S131 — GitHub Docs, About push protection (admitted, used by the instrument)

- **URL:** https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection, HTTP 200.
- **Accessed:** 2026-11-07 (capture 06:58:38Z).
- **Capture:** `corpus/source-snapshots/round-90/S131.txt`, sha256 `0c98d69a14b33d3995f0d7748112f191dcac391157a6cb093054c346ff71fcc9`; manifest `corpus/source-snapshots/round-90/manifest.json`, `source-recheck.py` rc 0 (2 quotes, anchors 570 and 610); scanned before the freeze, hits 0 (`controls/capture-scan-r90.txt`).
- **Located quote, S131.txt:570 (12 words):** "push protection blocks pushes that contain secrets before they reach your repository". Also :610 "anyone with write access to the repository can bypass push protection by specifying a bypass reason" (the allowlist's reason column is the analogue).
- **Row change (old → new):** new row, status `queued` (freeze `33f43db9`) → `mined` (integration); used-by `—` → `corpus/instruments/capture-source.py`.

### Rejected this round

- **S132 — GitLab Docs, Secret push protection**, https://docs.gitlab.com/user/application_security/secret_detection/secret_push_protection/, HTTP 200 on 2026-11-07, captured to scratch only (sha256 `78fe9740…`). Located quote, scratch line 169 (12 words): "Secret push protection is skipped because a push contains too many changed paths." Kept as a `rejected` row: the blocking design is already sourced on S131; what S132 adds is skip conditions (too many paths or lines, invalid input), a fail-open path the intake gate refuses by design. Flip: a round that adds an input-size bound to the gate cites it as the contrast case.

### considerthese and assimilation

- **considerthese:** `considerthese/2026-10-24.md:49-52` (2026-10-24, capture hygiene at intake; the r87 ConnectorOverlap pairing names an intake gate in `capture-source.py` that calls the scanner before a snapshot is written) — **implemented as C2** after four routings. The proposal's other half (store clean text: strip markup upstream) is already the instrument's conversion; not re-claimed.
- **Assimilation: none.** Registry ids at the check 132 (after S131/S132), staged 94, collisions 94/94 (`.ufo/waves/round-90/assimilation/collisions`; the staged file predates the lane's S031–S132 expansion, as in round 89). Quarantine slice re-derived: 7 rows (`assimilation/quarantine-slice`), not hand-checked this round. The guard proof is round 89's (`.ufo/waves/round-89/assimilation/guard-proof.txt`); nothing was appended from the package.

## Mistakes

**M90-1 — class `meter-reads-ambient-tree` (the r89 closure's routed defect 1).**

- **What happened:** the round-89 counter read scope files from the measured commit but classified every citation against the `--lane` working tree (untracked wave receipts, pycache, whatever the checkout holds) and imported `resolve.py` from it. The filed tip reading "814/1827 at `b9fcf005`" reproduced nowhere: 815 on the live lane, 814 in a clean clone of the tip, 812 in the closure's clone at `eb5f0df8`.
- **Captured-by:** none before filing. M1-M9 bound the delta, which is environment-invariant; nothing bound the absolute reading to a tree.
- **Fix:** the round-90 counter extracts `git archive REV` and uses that extract both as the classification root and as the `resolve.py` import path; absolute-path citations (host-owned) are counted on a separate `HOST` line. QUALITY R142.
- **Shown able to fail:** `controls/c1-controls-r90.txt` environment receipt — round-89 meter at `b9fcf005`: live 815/1827, clean clone 814/1827 (disagree); round-90 meter: 812/1827 on both (agree).

**M90-2 — class `harness-input-scheme-differs-from-use` (this round, pre-freeze).**

- **What happened:** the first C2 counter drove `capture-source.py` with `file://` inputs. urllib's file response carries `status=None`, so the instrument's `%d` print raised after the file was written: every clean capture returned rc 1 on both the base and the candidate, and G3 failed on the positive control for a reason unrelated to the gate (first run, L1 scratch). A counter that had passed on `file://` would have measured a path the lane never uses.
- **Captured-by:** the executed positive control (claim-sizing rule: build and run the controls before freezing).
- **Fix:** the frozen counter serves its inputs from a loopback `http.server` (127.0.0.1, ephemeral port), the scheme real captures use. The `file://` crash itself is a latent instrument defect (status `None` → TypeError after the write), routed to round 91, not fixed inside the C2 landing (P3 binds the landing's scope).
- **Shown able to fail:** reproduce with `python3 corpus/instruments/capture-source.py --id X --url file:///etc/hostname --out $S/x.txt; echo $?` → traceback, rc 1, file written.

**M90-3 — class `selection-reads-label-reason-not-row` (this round, found after landing).**

- **What happened:** the frozen C1 selection excluded a WRONG-with-range site only when its label *reason* said the row content was stale (lines 152, 155, 249, 438). Sites 158 and 439 carry the same stale SUPERSEDES gloss ("that entry lists 3 signatures, omitting `usage_limit_reached`"; "(three signatures)") but their labels judged only the main statement ("four signatures are L61-64"), so the map admitted them and the repoint made both rows cite a range that states four signatures (ReviewC1Sites Finding 1, CriticHarm F1). Every frozen limb passes: M9 binds the value to the label, not the gloss to the range.
- **Captured-by:** none before the freeze; the non-author attack seats after landing.
- **Fix (in-round content repair, tokens unchanged):** both glosses now say the audit-time text listed three and the entry lists four since its round-13 correction (integration commit; the table's own convention, `triage-thresholds.md:426-429`, is that the Supersedes column names the audit-time target). Routed rule for round 91: a tranche's labels judge the whole citing row (main statement and every gloss) against the new range, and the selection admits a site only when that full-row label is CORRECT.
- **Shown able to fail:** the frozen map at `4a7e6768` is the failing case: rows 158 and 439 read "3 signatures"/"three signatures" beside a range whose line 62 reads "FOUR".

## Routed-defect disposition (r89 spot-check §6)

| # | r89 routed defect | r90 disposition |
|---|---|---|
| 1 | Meter environment dependence; correct "814" | Done: C1 counter pins to `git archive REV` (M90-1, R142); correction 812/1827 filed above and in SCORECARD. |
| 2 | M89-2 / M89-3 counter fixes for `capture-secret-scan` | Not this round: C2 takes the intake gate, whose flip condition required a round without a `capture-secret-scan` claim. C2's own counter applies both lessons: shapes derived from the scanner at REV (G0), control inputs read from a pinned rev or frozen wave files (`c2-forgeries.py` reads the frozen candidate). Routed to round 91. |
| 3 | `r140-check.py` four-column labels | Not this round: tranche 5 is a non-author census (every site labelled), and M9 binds each row to its label; the checker successor is routed to round 91. |
| 4 | Composite token `triage-thresholds.md:457` | Not this round; ReviewC1Sites asked for its label as round-91 input. |
| 5 | Sibling credential material | Unchanged, operator-owned (L0 `kasegi | round-89`). |
| 6 | considerthese intake gate | Done as C2. |

## Wave findings (none re-scores a claim)

One v1 wave, 12 seats (`.ufo/waves/round-90/w1-dispatch.json`; results `w1-results.json`).

- **CriticClaims:** C1 VERIFIED, C2 VERIFIED (P1 at seeds 9090, 1, 1132209826). Routed: C1-F1 (no completeness limb: M9 binds rows to labels but never asserts the map equals {WRONG with range} − excluded); C2-F1 (`line=` field unbound: a mutant dropping it passes), C2-F2 (whole-bytes scan unbound: a `data[:65536]` mutant passes G0–G6; landed bytes refuse a 1 MiB-prefixed plant), C2-F3 ("imported" weakly bound), C2-F4 (a missing explicit `--allow` file loads as empty, so "unloadable allowlist refuses" holds for malformed rows, not for missing files), C2-F5 (scanner's hardcoded `AKIAIOSFODNN7EXAMPLE` passes at any path), C2-F6 = M90-2's `file://` crash, C2-F7 (axis: capability acquisition by bookkeeping, a hardening of an existing instrument by surface; coverage held at 8 either way).
- **ExecC1Indep:** AGREE on every number; own verifier 17/17; live lane and shared clone byte-identical; untracked-decoy attack moves the round-89 meter and not the round-90 meter.
- **ReviewC1Sites:** 34/34 judged — 32 CORRECT (6 partial support: 264, 278, 90, 442, 147, 157), 2 WRONG (158, 439 = M90-3, repaired); exclusions 4/4 agree; round-91 labels for 457, 141, 142, 226, 368 (content repair) and 454 (repoint to `ev-model.md:13-25`) at `ReviewC1Sites-receipts/`.
- **CriticHarm:** NO HARM on density (273.2), callers (no tracked caller of `capture()`), SOURCES/census; HARM F1 = M90-3, repaired in the integration commit.
- **MutC1Counter:** 26 mutants, 24 killed, 2 case-equivalent survivors (M4 INTERNAL conjunct, M5 reading base files) with proofs; Q1: M5 folds M4's verdict.
- **ReviewC2Gate:** APPROVE. F1 an allowlisted capture leaves no `allowed=` trace in its record; F2 `lane_rel()` is lexical (absolute rows, symlinked dirs); F3 the instrument's selftest bytes trip its own scanner shapes (not a capture path); F4 README's `allow_url()` sentence names a function that does not exist (pre-existing); F5 gate-error names the type, not the row; F6 = M90-2. Hygiene: its preamble names `mktemp -d /tmp/...` for scratch (directive: `/fast/scratch/hyaku`).
- **MutC2Gate:** 26 mutants, 19 killed, 7 survived — partial scan (`data[:256]`), `lane_rel` from cwd and without the outside guard, three selftest weakenings, gate skipped for `--kind text` (G1 plants are HTML only). Routed: a text-kind plant, an offset plant, an out-of-lane `--out` case.
- **MutC2Counter:** 30 counter mutants: 27 survive because five of six forgeries are each caught by two or three limbs; only F6 (leak) is single-limb. Routed: one single-limb forgery per conjunct.
- **SentinelGate:** ordering sound in 41 probes (refusal before any open, existing file kept, no echo, fail closed on every load error). Value-shape bypasses D1 double-encoded `&amp;#x26;` separators, D2 `%26`-only separators, D3 whitespace inside a fixed-width value; limits D4 conversion has no deadline (`SCRIPT_RE` quadratic), D5 symlinked `--out`, D6 silent allowlist non-consultation, D7 directory `--out` traceback. All scanner-shape or instrument limits, routed to round 91.
- **ScoutSources:** S131 re-captured through the landed gate, sha256 equal to the snapshot and manifest, quotes at anchors; S132 rejection reason holds on the live page. Gate behaviour: GitHub's "Supported secret scanning patterns" page is refused (`shape=private-key line=596`, a documented example header) and needs a digest-bound row. Round-91 leads opened: Microsoft "Create a user delegation SAS" (`skdutid`, line 571), GitHub supported patterns, one more (`ScoutSources-receipts/round91-leads.txt`).
- **ConnectorOverlap:** kake holds two capture writers (`scripts/live_snapshot.py`, `scripts/response_snapshot.py`) with no pre-write scan; no sibling holds a copy of kasegi's `capture-source.py`. Routed to the owners as a report line, never edited here.
- **ScribeEntry:** candidate `corpus/knowledge/capture-intake-gate.md`, admitted by the L1 after a mechanical check: 51 backticked `path:line` citations all in range, 17 block quotes all found at their cited lines, scanner `--files` hits 0.
