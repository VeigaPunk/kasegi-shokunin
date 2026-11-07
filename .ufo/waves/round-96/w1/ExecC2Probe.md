# ExecC2Probe — round-96 w1, independent probe of the seven C2 GitLab shapes

Seat: ExecC2Probe (leaf). Under test: `corpus/instruments/capture-secret-scan.py` at the C2
landing `7ef1d365eb523a83b2567342a6c0f585ab028ab0` (sha256
`71876619a62875049a5526a03806aa740e3ead122aacdc1499fe153be3048ac9`, equals the frozen
`instrument_sha256` in `claims.json`). Base for the round-95 comparator:
`d8a2bb0a2bdc2f6337ea2f849a1a557297067ad6`. Axes: depth:verifiability (independent
reproduction), coverage (boundary critique).

## Method (independent, not the gate's fixtures)

- My own generator (`gen.py`, receipt r1) transcribes the shape specs from the S140 snapshot
  (`corpus/source-snapshots/round-94/S140.txt`, lines 30, 51, 73, 136, 324, 358, 375), not
  from the instrument source: head `[0-9a-zA-Z_-]{27,300}`; routable tail
  `\.[0-9a-z]{2}[0-9a-z]{7}`; versioned tail `\.[0-9a-z]{2}\.[0-9a-z]{2}[0-9a-z]{7}`;
  `glptt-` exactly `{20}` or exactly `{40}`; prefixes are lower-case literals.
- Per shape: 3 positives (bare at byte 0; inside JSON `{"note":"…"}` — key chosen so the
  gate `credential` pattern cannot fire; after a `\t` escape-terminator, bytes 0x5C 0x74) and
  3 negatives (one char short of a minimum/exact limb; one char long past a fixed/exact limb;
  wrong case in the case-bearing limb). 42 mandated fixtures + 1 supplementary (below).
  Every fixture is one line ending in a single LF; all bytes are seat nonces, no real secrets.
- Both scanners ran in `--files` mode over absolute scratch paths with `--allow` pointed at an
  absent file, so no allowlist row can suppress an observation. A fixture passes as a positive
  only if the observed shape set is exactly `{expected}`; as a negative only if it is empty.
- The round-95 comparator ran from a scratch `r95env/` holding `capture-secret-scan.py` and
  `claim-package-check.py` both extracted by `git show` from `d8a2bb0a…` (the copied gate
  module's sha256 `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` equals
  the claims.json `gate_sha256`, so the environment is faithful).
- Declared choices: the `glptt` case-negative upper-cases the prefix (`GLPTT-…`) because its
  tail class `[A-Za-z0-9_-]` has no case limb; `glrtr-versioned` positives use `glrtr-` (bare,
  esc) and the `glrt-` alternate (json); the `glptt` json positive uses the 40-form so both
  published lengths appear as positives.

## Per-shape result (landed scanner)

| shape (landed name) | S140 line | positives | negatives | verdict |
|---|---|---|---|---|
| `gitlab-pat-routable` | 30 | 3/3 exact-shape hits | 3/3 no hit | PASS |
| `gitlab-pat-versioned` | 51 | 3/3 | 3/3 | PASS |
| `gitlab-runner-auth-token-versioned` | 136 | 3/3 | 3/3 | PASS |
| `gitlab-deploy-token-versioned` | 324 | 3/3 | 3/3 | PASS |
| `gitlab-agent-token-versioned` | 358 | 3/3 | 3/3 | PASS |
| `gitlab-workspace-token-versioned` | 375 | 3/3 | 3/3 | PASS |
| `gitlab-pipeline-trigger-token` | 73 | 3/3 | 3/3 | PASS |

Landed summary line: `CAPTURE-SECRET-SCAN mode=files scanned=43 hits=22 files=22 allowed=0
unused_allow=0 rc=1` (22 = 21 mandated positives + 1 supplementary; no extra shape fired
anywhere, so the observed HIT set over the 42 mandated fixtures is exactly the expected one).

## (fixture, expected, observed) — exact bytes (trailing LF omitted for readability)

| fixture | expected | observed | ok |
|---|---|---|---|
| `P-glpat-routable-bare.txt` | gitlab-pat-routable | gitlab-pat-routable | yes |
| bytes | `glpat-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2c4f9b1a` | | |
| `P-glpat-routable-json.txt` | gitlab-pat-routable | gitlab-pat-routable | yes |
| bytes | `{"note":"glpat-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2c4f9b1a"}` | | |
| `P-glpat-routable-esc.txt` | gitlab-pat-routable | gitlab-pat-routable | yes |
| bytes | `log\tglpat-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2c4f9b1a end` (`\t` = 0x5C 0x74) | | |
| `N-glpat-routable-short.txt` | no hit | none | yes |
| bytes | `glpat-ExC2Pr0be_r96-ExC2Pr0be_r9.e2c4f9b1a` (head 26 < 27) | | |
| `N-glpat-routable-long.txt` | no hit | none | yes |
| bytes | `glpat-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2c4f9b1aa` (final run 8 > 7) | | |
| `N-glpat-routable-case.txt` | no hit | none | yes |
| bytes | `glpat-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2C4F9B1A` (`[0-9a-z]{7}` limb) | | |
| `P-glpat-versioned-bare.txt` | gitlab-pat-versioned | gitlab-pat-versioned | yes |
| bytes | `glpat-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a` | | |
| `P-glpat-versioned-json.txt` | gitlab-pat-versioned | gitlab-pat-versioned | yes |
| bytes | `{"note":"glpat-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a"}` | | |
| `P-glpat-versioned-esc.txt` | gitlab-pat-versioned | gitlab-pat-versioned | yes |
| bytes | `log\tglpat-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a end` | | |
| `N-glpat-versioned-short.txt` | no hit | none | yes |
| bytes | `glpat-ExC2Pr0be_r96-ExC2Pr0be_r9.e2.7kc4f9b1a` | | |
| `N-glpat-versioned-long.txt` | no hit | none | yes |
| bytes | `glpat-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1aa` | | |
| `N-glpat-versioned-case.txt` | no hit | none | yes |
| bytes | `glpat-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.E2.7kc4f9b1a` (`[0-9a-z]{2}` limb) | | |
| `P-glrtr-versioned-bare.txt` | gitlab-runner-auth-token-versioned | gitlab-runner-auth-token-versioned | yes |
| bytes | `glrtr-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a` | | |
| `P-glrtr-versioned-json.txt` | gitlab-runner-auth-token-versioned | gitlab-runner-auth-token-versioned | yes |
| bytes | `{"note":"glrt-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a"}` (`glrt-` alternate) | | |
| `P-glrtr-versioned-esc.txt` | gitlab-runner-auth-token-versioned | gitlab-runner-auth-token-versioned | yes |
| bytes | `log\tglrtr-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a end` | | |
| `N-glrtr-versioned-short.txt` | no hit | none | yes |
| bytes | `glrtr-ExC2Pr0be_r96-ExC2Pr0be_r9.e2.7kc4f9b1a` | | |
| `N-glrtr-versioned-long.txt` | no hit | none | yes |
| bytes | `glrtr-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1aa` | | |
| `N-glrtr-versioned-case.txt` | no hit | none | yes |
| bytes | `glrtr-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.E2.7kc4f9b1a` | | |
| `P-gldt-versioned-bare.txt` | gitlab-deploy-token-versioned | gitlab-deploy-token-versioned | yes |
| bytes | `gldt-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a` | | |
| `P-gldt-versioned-json.txt` | gitlab-deploy-token-versioned | gitlab-deploy-token-versioned | yes |
| bytes | `{"note":"gldt-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a"}` | | |
| `P-gldt-versioned-esc.txt` | gitlab-deploy-token-versioned | gitlab-deploy-token-versioned | yes |
| bytes | `log\tgldt-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a end` | | |
| `N-gldt-versioned-short.txt` | no hit | none | yes |
| bytes | `gldt-ExC2Pr0be_r96-ExC2Pr0be_r9.e2.7kc4f9b1a` | | |
| `N-gldt-versioned-long.txt` | no hit | none | yes |
| bytes | `gldt-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1aa` | | |
| `N-gldt-versioned-case.txt` | no hit | none | yes |
| bytes | `gldt-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.E2.7kc4f9b1a` | | |
| `P-glagent-versioned-bare.txt` | gitlab-agent-token-versioned | gitlab-agent-token-versioned | yes |
| bytes | `glagent-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a` | | |
| `P-glagent-versioned-json.txt` | gitlab-agent-token-versioned | gitlab-agent-token-versioned | yes |
| bytes | `{"note":"glagent-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a"}` | | |
| `P-glagent-versioned-esc.txt` | gitlab-agent-token-versioned | gitlab-agent-token-versioned | yes |
| bytes | `log\tglagent-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a end` | | |
| `N-glagent-versioned-short.txt` | no hit | none | yes |
| bytes | `glagent-ExC2Pr0be_r96-ExC2Pr0be_r9.e2.7kc4f9b1a` | | |
| `N-glagent-versioned-long.txt` | no hit | none | yes |
| bytes | `glagent-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1aa` | | |
| `N-glagent-versioned-case.txt` | no hit | none | yes |
| bytes | `glagent-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.E2.7kc4f9b1a` | | |
| `P-glwt-versioned-bare.txt` | gitlab-workspace-token-versioned | gitlab-workspace-token-versioned | yes |
| bytes | `glwt-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a` | | |
| `P-glwt-versioned-json.txt` | gitlab-workspace-token-versioned | gitlab-workspace-token-versioned | yes |
| bytes | `{"note":"glwt-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a"}` | | |
| `P-glwt-versioned-esc.txt` | gitlab-workspace-token-versioned | gitlab-workspace-token-versioned | yes |
| bytes | `log\tglwt-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a end` | | |
| `N-glwt-versioned-short.txt` | no hit | none | yes |
| bytes | `glwt-ExC2Pr0be_r96-ExC2Pr0be_r9.e2.7kc4f9b1a` | | |
| `N-glwt-versioned-long.txt` | no hit | none | yes |
| bytes | `glwt-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1aa` | | |
| `N-glwt-versioned-case.txt` | no hit | none | yes |
| bytes | `glwt-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.E2.7kc4f9b1a` | | |
| `P-glptt-bare.txt` | gitlab-pipeline-trigger-token | gitlab-pipeline-trigger-token | yes |
| bytes | `glptt-GlPtT_x96-9f3aK2mQ8z` (20-form) | | |
| `P-glptt-json.txt` | gitlab-pipeline-trigger-token | gitlab-pipeline-trigger-token | yes |
| bytes | `{"note":"glptt-GlPtT_x96-9f3aK2mQ8zz8Qm2Ka3f9-69x_TtPlG"}` (40-form) | | |
| `P-glptt-esc.txt` | gitlab-pipeline-trigger-token | gitlab-pipeline-trigger-token | yes |
| bytes | `log\tglptt-GlPtT_x96-9f3aK2mQ8z end` (20-form) | | |
| `N-glptt-short.txt` | no hit | none | yes |
| bytes | `glptt-GlPtT_x96-9f3aK2mQ8` (19) | | |
| `N-glptt-long.txt` | no hit | none | yes |
| bytes | `glptt-GlPtT_x96-9f3aK2mQ8zz8Qm2Ka3f9-69x_TtPlGG` (41) | | |
| `N-glptt-case.txt` | no hit | none | yes |
| bytes | `GLPTT-GlPtT_x96-9f3aK2mQ8z` (prefix limb; see declared choice) | | |
| `X-glrtr-versioned-custom-prefix.txt` (supplementary) | gitlab-runner-auth-token-versioned | gitlab-runner-auth-token-versioned | yes |
| bytes | `acme-glrtr-ExC2Pr0be_r96-ExC2Pr0be_r96-Ex.e2.7kc4f9b1a` | | |

## Round-95 scanner over the same positives (+X): misses all

`CAPTURE-SECRET-SCAN mode=files scanned=22 hits=0 files=0 allowed=0 unused_allow=0 rc=0`;
`R95-MISSED 22/22`. Consistent with the base instrument's pattern set (20-char
`glpat-`/`glrtr?-`/`gldt-` forms, JWT forms only): each 27+ head fails the exact `{20}` limb,
and `glagent-`/`glwt-`/`glptt-` have no base pattern at all.

## Routed qualifier (not a verdict change)

S140 line 136 publishes an optional custom instance prefix `(?:[a-zA-Z0-9]{1,20}-)?` for the
runner versioned rule; the landed `gitlab-runner-auth-token-versioned` pattern is
`_GL_LB + "glrtr?-" + _GJ_VER` — it omits `_GL_PREFIX`, while the four sibling versioned
patterns (`glpat-`, `gldt-`, `glagent-`, `glwt-`) include it. Empirically (X fixture) the
shape still fires on `acme-glrtr-…`, but the matched secret value is the `glrtr-…` suffix
only, unlike S140's whole-token match and unlike the sibling shapes. Detection-wise covered;
attribution-asymmetry only. Also noted, no action: S140 itself names line 136's rule
`gitlab_runner_auth_token_routable` although its regex is the versioned tail — the landed
name follows the tail shape, i.e. the source's own naming quirk.

## Verdict

STANDS within this probe's scope, re-derived independently: all seven new shapes hit exactly
their expected shape on all 21 S140-derived positives (bare / JSON / escape-terminator), no
shape fires on any of the 21 boundary negatives (short / long / wrong-case) — the C2 kill-rule
clause "a shape that also fires on its boundary negative" is not triggered — and the round-95
instrument misses all 22 positives. Corroboration only (K1 is the gate's): landed selftest
prints `SELFTEST-RESULT pass cases=128` rc=0. The glrtr-versioned custom-prefix attribution
asymmetry above is routed as a qualifier; it does not re-score C2.

## Receipts

All under `ExecC2Probe-receipts/`; scratch was `/fast/scratch/hyaku/kasegi-r96/ExecC2Probe`
(TMPDIR set per command; removed after the report was written, so nothing outlives the seat).
No tools were installed or upgraded (none needed; pacman guard respected trivially).

- `r1-generate.txt` — `python3 -B $S/gen.py $S/fixtures` rc=0, `fixtures=43` (per-fixture bytes echoed; the two earlier generator crashes — 21-char nonce assertion, bad ctx kind — were fixed before any scan was run; no scan output predates the fixed generator).
- `r2-scan-runs.txt` — `python3 -B $S/run.py $S/fixtures` rc=0. Landed pass: `scanned=43 hits=22`, 43 `ROW` lines all `ok`, `SHAPE … PASS` ×7. R95 pass: `scanned=22 hits=0 rc=0`, `R95-MISSED 22/22`.
- `r0-s140-lines.txt` — `sed -n '28,32p;49,53p;71,75p;134,138p;322,326p;356,360p;373,377p' corpus/source-snapshots/round-94/S140.txt` rc=0 (the seven published regexes; example values structurally redacted in-repo) + `manifest.json`.
- `r3-shas.txt` — sha256s: landed instrument `71876619…8ac9` (equals frozen pin); r95env `capture-secret-scan.py` `3006991a…adfc` and `claim-package-check.py` `8b6f8493…cc8e6` (equals claims.json `gate_sha256`); S140 snapshot `f3fd09e4…a158c`.
- `r4-landed-selftest.txt` — `python3 -B corpus/instruments/capture-secret-scan.py --selftest` rc=0, `SELFTEST-RESULT pass cases=128`.
- Context commands: `git show --stat 7ef1d36…` (instrument +55/−7, SCORECARD 2 files) and `git show --stat d8a2bb0a…` rc=0.
