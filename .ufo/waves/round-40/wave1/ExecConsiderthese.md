# ExecConsiderthese — receipt (round 40, wave 1)

Item: mine `considerthese/2026-10-26.md` proposal 2 — run one end-to-end domain task round: pick one public disclosed finding, build the six-file claim package per `corpus/knowledge/claim-package-contract.md`, price it through the F13/F17/F18 rubric, log it as trigger → action → outcome → pointer.

Lane `kasegi-shokunin`, base `a7af2ce63bce153757d39bf66b366a96caf30c13`, claims read from `.ufo/waves/round-40/claims.json` (C1/C2, non-claim frontier item "considerthese: 2026-10-26 proposal 2 (run one end-to-end domain task round) mined: a claim-package exemplar built from a public disclosed report and logged (SHONEN box 2 pointer)"). Disk guard green at start (`/fast/scratch/hyaku` 26%, 599.9G free). No tooling installed: no pacman (host-paused), no `uv`/`npx`/binary needed — `curl`, `grep`, `sha256sum`, `python3` sufficed.

## What was built, in one paragraph

One public disclosed finding: Immunefi's bug fix review of the Sky (formerly MakerDAO) remote code execution on `vote.makerdao.com`, submitted 2023-09-25 by researcher `xss`, fixed 2023-09-28, paid **USD 50,000**, write-up published 2025-02-25. It was captured together with the Sky program page (scope, eligibility, reward ladder, prohibited activities) and priced through the three rubric entries the lane already holds: **F17** (`corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`, S051), **F13** (`corpus/knowledge/program-severity-ladders-and-reward-scales.md`, S043–S045) and **F18** (`corpus/knowledge/cisa-kev-catalog.md`, S052). Result: **VSCS v2.2 Websites and Apps 5. Critical · program ladder USD 50,000 · KEV absent**, with the derived figure equal to the observed payout.

## Commands run, with their actual output

Network (instrument UA, UTC recorded):

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o review.html -w '%{http_code}|%{size_download}|%{url_effective}' \
    https://immunefi.com/blog/bug-fix-reviews/sky-remote-code-execution-bugfix-review/
2026-10-26T21:19:05Z   200|54099|https://immunefi.com/blog/bug-fix-reviews/sky-remote-code-execution-bugfix-review/
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o program.html -w '%{http_code}|%{size_download}|%{url_effective}' \
    https://immunefi.com/bug-bounty/sky/
2026-10-26T21:19:06Z   200|554144|https://immunefi.com/bug-bounty/sky/information/     (HTTP 307 hop recorded in the header dump)
$ sha256sum review.html review.re.html program.html program.re.html      # review.re/program.re = second independent fetch, 21:19:12Z
1588dbb8eb2d6da17cfa0ea5cc56f3433c4a7bfef1e2b34e971a1b88c25e017d  review.html
1588dbb8eb2d6da17cfa0ea5cc56f3433c4a7bfef1e2b34e971a1b88c25e017d  review.re.html
9c58f3e14b857de7618f5cbd79e3f49bf68146b4a84444d9da11bebdac870ae7  program.html
d73b10211bd6f01363914249e18191c73c4469ccf52eda4fb0e769fa526b1695  program.re.html
```

The program page's raw bytes are volatile in exactly one respect — the per-request CSP `nonce` on `<link>` tags (first differing byte at offset 964, `nonce="M2MzOWQz…"` vs `nonce="ZjUyNDBj…"`; 2 differing lines of 166). Normalizing (drop script/style bodies, block-close and `<br>` to newline, strip tags, entity-decode, collapse spaces) makes both fetches **byte-identical**: `review` normalized sha256 `88e1619e…4efe97e`, `program` `f0b88ebe…63f7d6`, 56 and 1024 body lines, `identical True` for both. That is why the shipped artifacts are normalized captures with the raw digest recorded in their own headers, not raw HTML.

Rubric inputs (all lane-local, read-only):

```
$ sha256sum corpus/source-snapshots/round-34/S051.txt corpus/source-snapshots/round-35/S052.txt
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5  corpus/source-snapshots/round-34/S051.txt
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt   (1479694 B, 27870 lines)
$ grep -n "Websites and Apps\|5. Critical- Execute arbitrary system commands\|/etc/shadow" corpus/source-snapshots/round-34/S051.txt
97:Websites and Apps
99:5. Critical- Execute arbitrary system commands
101:- /etc/shadow
$ grep -c '"cveID"' corpus/source-snapshots/round-35/S052.txt                                   -> exit=0  1756
$ grep -ic 'makerdao' corpus/source-snapshots/round-35/S052.txt                                  -> exit=1  0
$ grep -ic 'gray-matter\|gray matter' corpus/source-snapshots/round-35/S052.txt                  -> exit=1  0
$ grep -icE '\bsky\b' corpus/source-snapshots/round-35/S052.txt                                  -> exit=1  0
$ grep -ic 'vote\.' corpus/source-snapshots/round-35/S052.txt                                    -> exit=1  0
$ grep -n "Live-target testing is refused" PROVINCE.md
52:Live-target testing is refused; this corpus is documentation only.
$ grep -n "Any testing on mainnet or public testnet deployed code" of the program capture -> :998
$ grep -n "vote.sky.money" of the program capture                                             -> :175 (single occurrence)
$ grep -n "Total Assets in Scope" of the program capture                                      -> :1017 ("Total Assets in Scope 255")
```

No request was made to `vote.makerdao.com`, `vote.sky.money` or any other Sky/MakerDAO asset; no PoC was executed; no account was created; no report was submitted (`evidence.no-live-testing.txt`).

## Price through F13 / F17 / F18

| Axis | Source (lane entry / capture) | Result |
|---|---|---|
| F17 severity | S051, VSCS v2.2 `Websites and Apps` table, `evidence.vscs-v2.2-websites-and-apps.txt:13` | **5. Critical** on "Execute arbitrary system commands" |
| F17 precision check | same, `:14-18` | the file-read bullet enumerates `/etc/shadow`, database passwords, blockchain keys and excludes non-sensitive files — `/etc/passwd` is **not** one, so the level must rest on command execution |
| F13 money | program page `:116` | `$100,000` only for direct fund loss with zero user action; "all other … Critical … resulting in a theft of funds" → **USD 50,000** |
| F13 calibration | disclosure `:40` | observed payout **USD 50,000** — derived equals observed |
| F13 anti-anchor | program page `:171` | the `USD 10,000` polling-manipulation clause is the wrong row for this host and would price it 5× low |
| F13 gap | program page `:116` + `:175` | no printed Critical website tier exists for an impact that is neither fund loss nor unauthorised minting; the vote asset admits only Critical (`:175`), so a downgrade prices a class the program does not accept there |
| F18 exploitation status | S052 capture, 1756 `cveID` records | **KEV absent**, 0 matches on four probes; the disclosure assigns no CVE, so there is no KEV key at all |

## Package shipped (flat, beside this receipt)

Package-relative path → shipped deliverable (`ExecConsiderthese.` prefix), lines, sha256:

| package path | shipped file | lines | sha256 |
|---|---|---|---|
| `report.md` | `ExecConsiderthese.report.md` | 112 | `6b1f367fcf5be9d839be3d549a4757c4289e3d8aafd0f85ea78abd2761c6a10d` |
| `claim_checklist.md` | `ExecConsiderthese.claim_checklist.md` | 39 | `a586e64645028a58f604660a73c01eecfda42aa40a291faf6f2613fa4a92a8b8` |
| `evidence/manifest.json` | `ExecConsiderthese.manifest.json` | 80 | `294502661a738fa40f28a632252d64bb681642494ec9f7a1767a80cfd8693805` |
| `custodian-receipts.json` | `ExecConsiderthese.custodian-receipts.json` | 104 | `201789194a00913c9bf95c3c8c24dacea114ef336cf1f0aad3d8ef8c7321ea44` |
| `provenance.json` | `ExecConsiderthese.provenance.json` | 82 | `99861a5b9f5298d0bee70cc49aa782fccee7ee7810cc03e9b27a506b668d0af9` |
| `status.json` | `ExecConsiderthese.status.json` | 67 | `365f9163f371c410923972222c5ded3dd1f0f21078216186e3734d69495f45bd` |
| `evidence/sky-rce-bugfix-review.txt` | `ExecConsiderthese.evidence.sky-rce-bugfix-review.txt` | 73 | `d5066d3d972f808781d9350cc567758288b2c25a001f30032cec552d2ca647ef` |
| `evidence/sky-program-scope-rewards.txt` | `ExecConsiderthese.evidence.sky-program-scope-rewards.txt` | 1041 | `7bcbd40754a37f838b48ffc19de3d59019e8081c94516689a4eac9e158ee95d9` |
| `evidence/vscs-v2.2-websites-and-apps.txt` | `ExecConsiderthese.evidence.vscs-v2.2-websites-and-apps.txt` | 64 | `08e09f6506decabb53703a0d8cf352921a34abe0fd956dfac59d2a60cf174e29` |
| `evidence/kev-absence-query.txt` | `ExecConsiderthese.evidence.kev-absence-query.txt` | 31 | `3d81c31f62ad58d9f3e1cc1c1af60474bd47d661e7102dc3a0e8e6a784358289` |
| `evidence/no-live-testing.txt` | `ExecConsiderthese.evidence.no-live-testing.txt` | 9 | `0856476e42f2bcef751e88f7f5cd7f26d06908db8be452b83824997f8a8ef9fd` |

LOG entry bytes (the landable deliverable, to be appended as one bullet under `## Round 40`; the heading itself is the L1's):

`ExecConsiderthese.e2e-package.md` — 1 line, 2604 B, sha256 `ec03b0187a9e3dcdaaec24a303890c8402f4dfcf3553a3b93817cd9f3fce993b`.

The manifest carries the same map as `shipping.map` so a reader can resolve contract paths from the flat wave-1 layout, plus `shipping.layout: "wave1-flat"`.

## Package self-check (my own deliverables, run once)

```
$ python3 verify-package.py        # scratch script, reads only the shipped files
exit=0   PASS lines=89   FAIL lines=0
RESULT all checks pass
```

What it proves, in its own terms: `status.manifest_sha256` == sha256 of the manifest bytes; `manifest.expected_head_sha256` == `custodian-receipts.head_sha256` == the final (disposition) `decision_sha256`; each of the six decision digests recomputes from the documented canonicalization (`json.dumps(..., sort_keys=True, separators=(',',':'), ensure_ascii=False)` over the decision minus its own digest); every decision carries a nonempty `matched_grant_id` and `scope_signal == "NO_SCOPE_OBJECTION"`; all five artifact digests match the shipped bytes; ≥1 positive polarity (3 positive, 2 negative); `external_effects_performed: []`; 26 `evidence/<file>:<lines>` refs in-range; every blockquote in `report.md` occurs verbatim in the artifact it cites, anchored on the cited line.

## Honest limits

- **The package is PARKED and `claimable:false`, by construction.** Three hard gates fail and one reviewer field is unmet: `authorization` (PROVINCE refuses live testing and none is claimed, and the program's prohibited list forbids the route the public PoC used), `no_duplicate_or_prior_submission` (the finding was paid in 2023), reviewer distinctness (a single wave-1 seat cannot supply a non-author reviewer with a resolved model). `status_state` is therefore `PARKED`, never `DONE`.
- **`redactions: []` deliberately.** All five artifacts are public captures or lane-local query records; the contract's rule that an empty `redactions` is never claim-ready is consistent with `claim_ready:false`. Inventing producer/verifier pairs to fill it would have been fabrication, so the field is empty and the reason is written into `manifest.redactions_note`.
- **The identity `xss` is quoted, not resolved.** It is the researcher name printed in the disclosure; the package does not attempt to bind it to a real person and says so nowhere stronger than the source does.
- **The ladder does not derive the price on its own.** `USD 50,000` is the closest printed Critical website tier and the empirically paid amount, but the page has no tier for a non-fund-loss Critical, so the match is calibration, not derivation-from-text. Recorded as a ladder gap rather than smoothed over.
- **The program's asset inventory is unreachable from the static page.** "Total Assets in Scope 255" is printed, the per-asset list is client-rendered; the only mention of the vote host in the capture is the scope sentence at `:175`. Recorded as a residual gate in `claim_checklist.md` rather than papered over.
- **Proposal-2's second half was not done.** It also proposes rebuilding a minimal claim checker under `corpus/instruments/` ("the `ops/*` executables are gone"). This item's spec was the package + price + log, and a claim checker would be a lane instrument outside a wave-1 seat's write scope. The LOG bullet states this boundary explicitly so the ledger cannot overcount.
- **Live pages drift.** Both captures are pinned by digest with the fetch time; the reward clause that anchors the price is the 2026-09-19 revision of the program page, and the paid amount is from 2023. If either moves, the price must be re-derived, and the two artifacts are re-fetchable at their recorded URLs.

## Lane writes (complete list)

New files, all under `.ufo/waves/round-40/wave1/`: the 11 deliverables above plus this receipt. Nothing else in the lane repo was touched (`git status --porcelain` shows no non-`round-40` entry). No commit, no mutating git command, no write to the fleet root, the lane's `corpus/`, `MANIFEST.json`, `scripts/` or `.ufo/state/`, and no write to `shokuknow` or any sibling lane. Scratch `/fast/scratch/hyaku/kasegi-r40/ExecConsiderthese/` removed before yield; no `kasegi-r39*`/`r40` scratch entry derived from this seat survives.
