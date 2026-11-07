# ExecC2Probe — independent probe of the ten new GitLab shapes (round 97, C2)

Seat: ExecC2Probe (leaf probe). Lane: kasegi-shokunin. Base `b06af5e07efbd961a8449f7de6b57eeea62c6bd3`, freeze `daf7fc6a627d615178c27594110e956e592e4cd9`, C2 landing `a9a53608dce6aea07d298bb9d5133532078eb1dd` (HEAD = the landing; C1 landing `75a471809cba265c8981ece1c0ed29c7895d9308` beneath it; both `git cat-file -t` = commit, base is ancestor of the landing — receipts `01`).

## Verdict

PASS — all ten round-97 shapes independently verified at the C2 landing, and independently confirmed absent at the round-96 base:

- Landed scanner (`--files`, one invocation per fixture): **60/60 fixtures as expected** — each of the 30 positives fires **exactly the one intended shape** (rc=1, `hits=1`, no co-firing shape), each of the 30 boundary negatives is silent (rc=0, `hits=0`).
- Round-96 base scanner over the same 30 positives: **0 hits on all 30** (rc=0) — the base misses every one of the ten new families.
- Both selftests reproduce: landed `SELFTEST-RESULT pass cases=148` rc=0; base `SELFTEST-RESULT pass cases=128` rc=0 (receipts `04`, `05`).

All fixture values are synthetic; no real credential material was used or produced.

## Method (independent of the gate)

- Own fixture generator (`gen-fixtures.py`, receipt copy; sha256 `68723c5b108a61062ad62451f0c3213c6bf5b48f2636710c1f455ffedbc9d467`) — not the round-97 gate's generator. 10 shapes × 6 fixtures: positives **bare / inside a JSON string / after a literal backslash escape** (`\t` or `\n` two-byte escape, an allowed left-boundary terminator); negatives **tail one char short / one char long / wrong case where the rule has case**.
- Case-negative placement: nine tails are drawn from the case-insensitive class `[A-Za-z0-9_-]` (S140 101/160/174/190/278/341/392/412), so the rule's case lives in the case-sensitive prefix literal → the prefix is flipped (`gr1348941`, `FEED_TOKEN=`, `GLOAS-`, `GLFT-`, `GLSOAT-`, `Gitlab+deploy-token-`, `GLFFCT-`, `GLRCT-`, `GLAGENT-`). `gitlab-incoming-email-token` has the one case-constrained tail `[0-9a-z]{20,25}` (S140 229) → the tail's 3rd char is flipped (`glimt-abC…`, prefix intact).
- Byte-pinned scanners, no checkout: `git show <rev>:corpus/instruments/capture-secret-scan.py` for the landing (`sha256 59909fc4d70819b1a67fa9eec36db2b054462770959828e4c3ff3ce164d2bd92` — equals the frozen C2 instrument pin) and the base (`sha256 71876619a62875049a5526a03806aa740e3ead122aacdc1499fe153be3048ac9`) (receipt `02`). The gate import `claim-package-check.py` is byte-identical at both revisions (`8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` = the frozen gate pin). Scratch copies were run with `python3 -B`, `TMPDIR=$S`; no allowlist beside the scratch copies, so no fixture match could be allowed away.
- Runner (`run-probe.py`): per-fixture invocation, observed = the `HIT shape=…` lines plus the `CAPTURE-SECRET-SCAN mode=files …` summary, rc recorded per run. Expected per the frozen C2 statement: landed positives → exactly the intended shape; landed negatives → no hit; base on positives → no hit.

## S140 grounding (corpus/source-snapshots/round-94/S140.txt, examples redacted upstream)

| line | rule id (S140) | grammar (source regex body) | landed shape |
|---|---|---|---|
| 101 | gitlab_runner_registration_token | `GR1348941[0-9a-zA-Z_\-]{20}` + right boundary, no instance prefix | gitlab-runner-registration-token |
| 160 | gitlab_feed_token | `feed_token=[0-9a-zA-Z_\-]{20}` + right boundary | gitlab-feed-token |
| 174 | gitlab_oauth_app_secret | `gloas-[0-9a-zA-Z_\-]{64}` + right boundary, no instance prefix | gitlab-oauth-app-secret |
| 190 | gitlab_feed_token_v2 | `glft-[0-9a-zA-Z_\-]{20}` + right boundary, no instance prefix | gitlab-feed-token-v2 |
| 213 | gitlab_kubernetes_agent_token | `(?:[a-zA-Z0-9]{1,20}-)?glagent-[0-9a-zA-Z_\-]{50}` + the rule's own right boundary (`\.` not followed by `[0-9a-z]` allowed) | gitlab-kubernetes-agent-token |
| 229 | gitlab_incoming_email_token | `(?:[a-zA-Z0-9]{1,20}-)?glimt-[0-9a-z]{20,25}` (lower-case tail) | gitlab-incoming-email-token |
| 278 | gitlab_scim_oauth_token | `glsoat-[0-9a-zA-Z_\-]{20}`, no instance prefix | gitlab-scim-oauth-token |
| 341 | gitlab_deploy_token_in_url | `gitlab\+deploy-token-[0-9]+:[0-9a-zA-Z_\-]{20}@` | gitlab-deploy-token-in-url |
| 392 | gitlab_feature_flags_client_token | `(?:[a-zA-Z0-9]{1,20}-)?glffct-[0-9a-zA-Z_\-]{20}` | gitlab-feature-flags-client-token |
| 412 | gitlab_runner_controller_token | `(?:[a-zA-Z0-9]{1,20}-)?glrct-[0-9a-zA-Z_\-]{20}` | gitlab-runner-controller-token |

(extracted lines verbatim: receipt `08`)

## Result table (fixture, expected, observed)

Landed scanner, one run per fixture. "observed" is the exact set of `HIT` shapes printed; summary lines all of the form `CAPTURE-SECRET-SCAN mode=files scanned=1 hits=1 files=1 allowed=0 unused_allow=0 rc=1` (positives) / `… hits=0 files=0 … rc=0` (negatives and all base runs). Full per-run TSVs: receipts `06`, `07`.

| shape | variant | expected | observed | rc | verdict |
|---|---|---|---|---|---|
| gitlab-runner-registration-token | bare / json / escape | the shape | the shape (exactly) | 1 | PASS ×3 |
| gitlab-runner-registration-token | short / long / case (`gr1348941`) | no hit | none | 0 | PASS ×3 |
| gitlab-feed-token | bare / json / escape | the shape | the shape (exactly) | 1 | PASS ×3 |
| gitlab-feed-token | short / long / case (`FEED_TOKEN=`) | no hit | none | 0 | PASS ×3 |
| gitlab-oauth-app-secret | bare / json / escape | the shape | the shape (exactly) | 1 | PASS ×3 |
| gitlab-oauth-app-secret | short (63) / long (65) / case (`GLOAS-`) | no hit | none | 0 | PASS ×3 |
| gitlab-feed-token-v2 | bare / json / escape | the shape | the shape (exactly) | 1 | PASS ×3 |
| gitlab-feed-token-v2 | short / long / case (`GLFT-`) | no hit | none | 0 | PASS ×3 |
| gitlab-incoming-email-token | bare / json / escape (22-char lower tail) | the shape | the shape (exactly) | 1 | PASS ×3 |
| gitlab-incoming-email-token | short (19) / long (26) / case (tail `abC…`) | no hit | none | 0 | PASS ×3 |
| gitlab-scim-oauth-token | bare / json / escape | the shape | the shape (exactly) | 1 | PASS ×3 |
| gitlab-scim-oauth-token | short / long / case (`GLSOAT-`) | no hit | none | 0 | PASS ×3 |
| gitlab-deploy-token-in-url | bare / json / escape | the shape | the shape (exactly) | 1 | PASS ×3 |
| gitlab-deploy-token-in-url | short (19+@) / long (21+@) / case (`Gitlab+…`) | no hit | none | 0 | PASS ×3 |
| gitlab-feature-flags-client-token | bare / json / escape | the shape | the shape (exactly) | 1 | PASS ×3 |
| gitlab-feature-flags-client-token | short / long / case (`GLFFCT-`) | no hit | none | 0 | PASS ×3 |
| gitlab-runner-controller-token | bare / json / escape | the shape | the shape (exactly) | 1 | PASS ×3 |
| gitlab-runner-controller-token | short / long / case (`GLRCT-`) | no hit | none | 0 | PASS ×3 |
| gitlab-kubernetes-agent-token | bare / json / escape (50-char tail) | the shape | the shape (exactly) | 1 | PASS ×3 |
| gitlab-kubernetes-agent-token | short (49) / long (51) / case (`GLAGENT-`) | no hit | none | 0 | PASS ×3 |

Round-96 base scanner over the same 30 positives: observed none, rc=0, **30/30 PASS (misses all)** — receipt `07`. No round-96 shape co-fired on any positive (the tails avoid `gl`-prefix collisions by construction and assertion in the generator).

## Exact fixture bytes (all synthetic)

Generated by `gen-fixtures.py` (receipt copy); dump with sha256 `f4a7400528823d3117281e6c73df983fd18c2f852271c13a290944746d17ad8c` (receipt `fixture-bytes.txt`). `\t`, `\n` inside the b'' literals are the two-byte backslash sequences present in the files (the escape-terminator probes); trailing `\n` is a real newline.

```
01-runner-registration-token.bare.txt	b'cfg [gitlab-runner-registration-token-fixture-redacted-r97] end\n'
01-runner-registration-token.json.txt	b'{"cfg": "[gitlab-runner-registration-token-fixture-redacted-r97]"}\n'
01-runner-registration-token.escape.txt	b'cfg:\\t[gitlab-runner-registration-token-fixture-redacted-r97]\n'
01-runner-registration-token.short.txt	b'cfg GR1348941Qw7Zx-Ce9V_4Nm6Kj8L end\n'
01-runner-registration-token.long.txt	b'cfg GR1348941Qw7Zx-Ce9V_4Nm6Kj8LpQ end\n'
01-runner-registration-token.case.txt	b'cfg gr1348941Qw7Zx-Ce9V_4Nm6Kj8Lp end\n'
02-feed-token.bare.txt	b'https://gitlab.example/api/v4/issues?[gitlab-feed-token-fixture-redacted-r97]&scope=all\n'
02-feed-token.json.txt	b'{"q": "https://gitlab.example/api/v4/issues?[gitlab-feed-token-fixture-redacted-r97]&scope=all"}\n'
02-feed-token.escape.txt	b'url=\\t[gitlab-feed-token-fixture-redacted-r97]\n'
02-feed-token.short.txt	b'https://gitlab.example/api/v4/issues?feed_token=Qw7Zx-Ce9V_4Nm6Kj8L&scope=all\n'
02-feed-token.long.txt	b'https://gitlab.example/api/v4/issues?feed_token=Qw7Zx-Ce9V_4Nm6Kj8LpQ&scope=all\n'
02-feed-token.case.txt	b'https://gitlab.example/api/v4/issues?FEED_TOKEN=Qw7Zx-Ce9V_4Nm6Kj8Lp&scope=all\n'
03-oauth-app-secret.bare.txt	b'cfg [gitlab-oauth-app-secret-fixture-redacted-r97] end\n'
03-oauth-app-secret.json.txt	b'{"cfg": "[gitlab-oauth-app-secret-fixture-redacted-r97]"}\n'
03-oauth-app-secret.escape.txt	b'cfg:\\t[gitlab-oauth-app-secret-fixture-redacted-r97]\n'
03-oauth-app-secret.short.txt	b'cfg gloas-Qw7Zx2Ce9Vb4Nm6K-8LpQw7Zx2Ce9Vb4_m6Kj8LpQw7Zx2Ce9Vb4Nm6Kj8LpQw7 end\n'
03-oauth-app-secret.long.txt	b'cfg gloas-Qw7Zx2Ce9Vb4Nm6K-8LpQw7Zx2Ce9Vb4_m6Kj8LpQw7Zx2Ce9Vb4Nm6Kj8LpQw7Zx end\n'
03-oauth-app-secret.case.txt	b'cfg GLOAS-Qw7Zx2Ce9Vb4Nm6K-8LpQw7Zx2Ce9Vb4_m6Kj8LpQw7Zx2Ce9Vb4Nm6Kj8LpQw7Z end\n'
04-feed-token-v2.bare.txt	b'cfg [gitlab-feed-token-v2-fixture-redacted-r97] end\n'
04-feed-token-v2.json.txt	b'{"cfg": "[gitlab-feed-token-v2-fixture-redacted-r97]"}\n'
04-feed-token-v2.escape.txt	b'cfg:\\t[gitlab-feed-token-v2-fixture-redacted-r97]\n'
04-feed-token-v2.short.txt	b'cfg glft-Qw7Zx-Ce9V_4Nm6Kj8L end\n'
04-feed-token-v2.long.txt	b'cfg glft-Qw7Zx-Ce9V_4Nm6Kj8LpQ end\n'
04-feed-token-v2.case.txt	b'cfg GLFT-Qw7Zx-Ce9V_4Nm6Kj8Lp end\n'
05-incoming-email-token.bare.txt	b'cfg [gitlab-incoming-email-token-fixture-redacted-r97] end\n'
05-incoming-email-token.json.txt	b'{"cfg": "[gitlab-incoming-email-token-fixture-redacted-r97]"}\n'
05-incoming-email-token.escape.txt	b'cfg:\\t[gitlab-incoming-email-token-fixture-redacted-r97]\n'
05-incoming-email-token.short.txt	b'cfg glimt-abcdefghijklmnopqrs end\n'
05-incoming-email-token.long.txt	b'cfg glimt-abcdefghijklmnopqrstuvwxyz end\n'
05-incoming-email-token.case.txt	b'cfg glimt-abCdefghijklmnopqrstuv end\n'
06-scim-oauth-token.bare.txt	b'cfg [gitlab-scim-oauth-token-fixture-redacted-r97] end\n'
06-scim-oauth-token.json.txt	b'{"cfg": "[gitlab-scim-oauth-token-fixture-redacted-r97]"}\n'
06-scim-oauth-token.escape.txt	b'cfg:\\t[gitlab-scim-oauth-token-fixture-redacted-r97]\n'
06-scim-oauth-token.short.txt	b'cfg glsoat-Qw7Zx-Ce9V_4Nm6Kj8L end\n'
06-scim-oauth-token.long.txt	b'cfg glsoat-Qw7Zx-Ce9V_4Nm6Kj8LpQ end\n'
06-scim-oauth-token.case.txt	b'cfg GLSOAT-Qw7Zx-Ce9V_4Nm6Kj8Lp end\n'
07-deploy-token-in-url.bare.txt	b'https://[gitlab-deploy-token-in-url-fixture-redacted-r97]gitlab.example/proj.git\n'
07-deploy-token-in-url.json.txt	b'{"remote": "https://[gitlab-deploy-token-in-url-fixture-redacted-r97]gitlab.example/proj.git"}\n'
07-deploy-token-in-url.escape.txt	b'x\\n[gitlab-deploy-token-in-url-fixture-redacted-r97]gitlab.example\n'
07-deploy-token-in-url.short.txt	b'https://gitlab+deploy-token-15:Qw7Zx-Ce9V_4Nm6Kj8L@gitlab.example/proj.git\n'
07-deploy-token-in-url.long.txt	b'https://gitlab+deploy-token-15:Qw7Zx-Ce9V_4Nm6Kj8LpQ@gitlab.example/proj.git\n'
07-deploy-token-in-url.case.txt	b'https://Gitlab+deploy-token-15:Qw7Zx-Ce9V_4Nm6Kj8Lp@gitlab.example/proj.git\n'
08-feature-flags-client-token.bare.txt	b'cfg [gitlab-feature-flags-client-token-fixture-redacted-r97] end\n'
08-feature-flags-client-token.json.txt	b'{"cfg": "[gitlab-feature-flags-client-token-fixture-redacted-r97]"}\n'
08-feature-flags-client-token.escape.txt	b'cfg:\\t[gitlab-feature-flags-client-token-fixture-redacted-r97]\n'
08-feature-flags-client-token.short.txt	b'cfg glffct-Qw7Zx-Ce9V_4Nm6Kj8L end\n'
08-feature-flags-client-token.long.txt	b'cfg glffct-Qw7Zx-Ce9V_4Nm6Kj8LpQ end\n'
08-feature-flags-client-token.case.txt	b'cfg GLFFCT-Qw7Zx-Ce9V_4Nm6Kj8Lp end\n'
09-runner-controller-token.bare.txt	b'cfg [gitlab-runner-controller-token-fixture-redacted-r97] end\n'
09-runner-controller-token.json.txt	b'{"cfg": "[gitlab-runner-controller-token-fixture-redacted-r97]"}\n'
09-runner-controller-token.escape.txt	b'cfg:\\t[gitlab-runner-controller-token-fixture-redacted-r97]\n'
09-runner-controller-token.short.txt	b'cfg glrct-Qw7Zx-Ce9V_4Nm6Kj8L end\n'
09-runner-controller-token.long.txt	b'cfg glrct-Qw7Zx-Ce9V_4Nm6Kj8LpQ end\n'
09-runner-controller-token.case.txt	b'cfg GLRCT-Qw7Zx-Ce9V_4Nm6Kj8Lp end\n'
10-kubernetes-agent-token.bare.txt	b'cfg [gitlab-kubernetes-agent-token-fixture-redacted-r97] end\n'
10-kubernetes-agent-token.json.txt	b'{"cfg": "[gitlab-kubernetes-agent-token-fixture-redacted-r97]"}\n'
10-kubernetes-agent-token.escape.txt	b'cfg:\\t[gitlab-kubernetes-agent-token-fixture-redacted-r97]\n'
10-kubernetes-agent-token.short.txt	b'cfg glagent-Qw7Zx2Ce9Vb4-m6Kj8LpQw7Zx_Ce9Vb4Nm6Kj8LpQw7Zx2Ce9 end\n'
10-kubernetes-agent-token.long.txt	b'cfg glagent-Qw7Zx2Ce9Vb4-m6Kj8LpQw7Zx_Ce9Vb4Nm6Kj8LpQw7Zx2Ce9Vb end\n'
10-kubernetes-agent-token.case.txt	b'cfg GLAGENT-Qw7Zx2Ce9Vb4-m6Kj8LpQw7Zx_Ce9Vb4Nm6Kj8LpQw7Zx2Ce9V end\n'
```

## Probe-integrity notes (findings against my own first draft, not against the claim)

Two of my first-draft fixtures were defective; in both cases the landed scanner behaved correctly and my fixture was wrong — recorded because a probe that never disagrees proves little:

1. First `glimt-` "long" tail was 23 chars (in range 20–25): the scanner correctly fired `gitlab-incoming-email-token` on it, exposing my bug. Rebuilt as a true 26-char tail (one past the range) → silent, as the rule requires.
2. First `gitlab-deploy-token-in-url` positives omitted the required `@` (rule: `…{20}@`): the scanner correctly stayed silent. Rebuilt with the `@` → exactly one hit each.

No scanner defect surfaced. Nothing here re-scores C2 — this seat only re-derives the frozen statement's behavioral limbs on the landing bytes.

## Receipts

All paths relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-97/w1/ExecC2Probe-receipts/`. Scratch `/fast/scratch/hyaku/kasegi-r97/ExecC2Probe` is removed at seat end; nothing else of this seat persists outside the report and receipts paths.

- `01-git-state.txt` — `git rev-parse HEAD` (= `a9a5360…`), `git cat-file -t` ×2 (both `commit`), `git merge-base --is-ancestor base landing` (`ancestor-ok`), `git log --oneline -4`. rc=0.
- `02-extract-scanners.txt` — `git show <landing|base>:corpus/instruments/capture-secret-scan.py` + `sha256sum`: landed `59909fc4…` (= frozen C2 instrument pin), base `71876619a6…`; 650/578 lines. rc=0.
- `03-scanner-diff-r96-r97.txt` — `diff -u` base vs landed (112 lines; the ten new shapes + selftest additions).
- `04-selftest-landed-r97.txt` — `python3 -B scanner-landed-r97.py --selftest`: `SELFTEST-RESULT pass cases=148`, rc=0.
- `05-selftest-base-r96.txt` — `python3 -B scanner-base-r96.py --selftest`: `SELFTEST-RESULT pass cases=128`, rc=0.
- `06-landed-r97-per-fixture.tsv` / `06-landed-r97-raw.log` — 60 per-fixture runs of the landed scanner (`--files <fixture>`): 30× rc=1 `hits=1` with observed = the intended shape, 30× rc=0 `hits=0`; raw stdout per run.
- `07-base-r96-per-fixture.tsv` / `07-base-r96-raw.log` — 30 per-fixture runs of the base scanner over the same positives: all rc=0 `hits=0`.
- `08-s140-grammar-lines.txt` — `sed -n` extraction of S140.txt lines 99–103, 158–162, 172–176, 188–192, 211–215, 227–231, 276–280, 339–343, 390–394, 410–414.
- `09-run-probe-console.txt` — generator + runner console: `wrote 60 fixtures`, `06-landed-r97: 60 runs, 56→60 PASS` (final) `0 FAIL`, `07-base-r96: 30 runs, 30 PASS, 0 FAIL`, per-shape `landed=6/6 base=3/3` ×10. rc=0.
- `fixture-bytes.txt` (sha256 `f4a74005…`), `manifest.tsv`, `gen-fixtures.py` (sha256 `68723c5b…`), `run-probe.py` (sha256 `199c28ac…`) — fixture bytes, manifest, and both scripts for reproduction.

No tool installs were needed (system python3 only); no pacman transaction touched. Lane git state untouched (read-only `git show`/`rev-parse`/`cat-file`/`merge-base`/`log` only); no commits, no checkout.
