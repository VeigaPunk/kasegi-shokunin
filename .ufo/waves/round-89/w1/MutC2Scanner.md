# MutC2Scanner — round 89 attempt 1, C2 mutation probe

Seat: `MutC2Scanner` (leaf, mutation tester). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `090a46f89932324787e00ca20b1007f893934c9a`, freeze `94573d2573dc6cca83454cc65b787d37d96988f5`,
C1 landing `eb5f0df8eaceca617465e493c710e8626e9aa618`, C2 landing `c61c55868e6d28653f57413bac6a6de5a398d11f`
(`.ufo/waves/round-89/landing.json`).

Bytes under mutation: `corpus/instruments/capture-secret-scan.py` at the C2 landing, sha256
`95f24a541db8b3d6693315a03de28d0b6de0fb0b6e53a68471265382114d20ec` — byte-equal to
`.ufo/waves/round-89/c2/candidate/capture-secret-scan.py` (P2 pin) and to the working-tree file.

Detector: the frozen counter `.ufo/waves/round-89/c2/capability-check.py`, sha256
`176effca85337a67093462b6239d7e6486566d72eeaf300958b298b00785abcf`, run **unpinned** (no
`--instrument-sha256`, no `--gate-sha256`) so K1's selftest and every behavioural limb must catch the
mutation, at `--seed 8989` and `--seed 1`.

Statement of scope: the two claims are judged only on their frozen predicates at the landing commits.
Everything below is a routed defect / coverage qualifier for a later round, never a re-score of C2.

## Method

One scratch clone of the lane at base `090a46f8` (`git clone --shared`, `rev-parse --show-toplevel`
asserted equal to the clone), the round-89 snapshots copied into `corpus/source-snapshots/round-89/`,
the candidate allowlist and the candidate `SCORECARD.md` row applied, one commit with identity
`fixture@invalid` — exactly `build()` of `.ufo/waves/round-89/controls/c2-controls-r89.sh`. Each mutant
is one further commit that changes only `corpus/instruments/capture-secret-scan.py`, so the tree at
`HEAD` differs from the passing positive control **only** in the instrument bytes; the counter reads
committed bytes (`git show`), never the working tree.

Every mutation is a single substring replacement with `source.count(old) == 1` asserted before writing
(or the deletion of exactly one selftest case line), and the mutated instrument's sha256 is recorded in
its receipt. Counter invocation, one mutant at a time:

```
python3 -B .ufo/waves/round-89/c2/capability-check.py --lane <clone> --rev HEAD --work <scratch> --seed {8989,1}
```

Positivity control first, restoration control last. Both are recorded verbatim:

```
BASELINE (pristine candidate, seed 8989)  K1 pass K2 pass K3 pass K4 pass K6 pass K7 pass K8 pass K5 pass  CAPABILITY-CHECK-RESULT pass rc=0
BASELINE (pristine candidate, seed 1)     CAPABILITY-CHECK-RESULT pass rc=0
RESTORED (pristine re-committed, 8989/1)  CAPABILITY-CHECK-RESULT pass rc=0 / pass rc=0
```

## Result

**61 mutants: 47 on the round-89 additions (44 in the main sweep + 3 follow-ups) and 14 re-runs of the
r88 survivor list. 25 killed, 35 survived, 1 seed-dependent, 0 inconclusive.**

No mutant was caught by K5 or K6. K6 reads the base instrument at `BASE_REV` and K5 reads
`SCORECARD.md`, so both are candidate-independent by construction (`claims.json` says so). K2 fired once,
for the mutant whose instrument crashed (`cf_sig_nocase`, `K2 sts_files=0`). K3 fired where the whole
instrument broke (`summary=none`) or where the mutation changed the bytes matched in the S128/S130
documentation example — in that case the two new allowlist rows make K3 a real second oracle
(`allowed=18, unused_allow=2`): `cf_param_window_1_20`,
`cf_sig_class_drop_tilde`, `cf_sig_class_drop_hyphen`, `cf_sig_class_add_plus_slash`, `cf_sig_name_typo`,
`cf_kpi_len_8_8`, `cf_kpi_name_case`, `cf_alt_drop_sig_first`, `cf_lb_escape_only`.

## Table A — round-89 additions (47 mutants)

Observed column = seed 8989 / seed 1 (`fail(LIMBs)` or `pass`). Every mutant was run at both seeds.

| # | mutant (single point) | expected detector | observed | verdict | killing limb |
|---|---|---|---|---|---|
| 1 | `cf_lb_drop_json_u0026` | kill only if some fixture starts a CF match right after a \u0026 (K1 cf-kpi-first-json starts at '?', K4 live-d at '?') | fail(K7) / pass(-) | **SEED-DEP** | K7 |
| 2 | `cf_lb_drop_pct26` | survive (no CF %26 fixture) | pass(-) / pass(-) | **SURVIVED** | — |
| 3 | `cf_lb_dash_admitted` | kill K4 extra S011 | fail(K1,K4,K8) / fail(K1,K4,K8) | **KILLED** | K1,K4,K8 |
| 4 | `cf_lb_removed` | kill K4 extra S011 | fail(K1,K4,K8) / fail(K1,K4,K8) | **KILLED** | K1,K4,K8 |
| 5 | `cf_param_window_0_1` | kill if any fixture has 2+ intervening params between Signature and Key-Pair-Id | pass(-) / pass(-) | **SURVIVED** | — |
| 6 | `cf_param_window_0_0` | kill K4 live-d/live-e missing, K7 g2 | fail(K1,K4,K7,K8) / fail(K1,K4,K7,K8) | **KILLED** | K1,K4,K7,K8 |
| 7 | `cf_param_window_1_20` | kill K1 cf-canned, K4 S008/S009 (0 intervening) | fail(K1,K3,K4,K7,K8) / fail(K1,K3,K4,K7,K8) | **KILLED** | K1,K3,K4,K7,K8 |
| 8 | `cf_param_name_2_6` | kill K4 live-d missing (Expires is 7 letters), K7 g2 | fail(K1,K4,K7,K8) / fail(K1,K4,K7,K8) | **KILLED** | K1,K4,K7,K8 |
| 9 | `cf_param_name_letters_only` | survive if no intervening name has a digit or hyphen | pass(-) / pass(-) | **SURVIVED** | — |
| 10 | `cf_param_name_upper_first` | survive if every intervening name starts upper-case | pass(-) / pass(-) | **SURVIVED** | — |
| 11 | `sep_drop_html_amp` | kill K1 cf-html-amp, K4 live-e missing | fail(K1,K4,K8) / fail(K1,K4,K8) | **KILLED** | K1,K4,K8 |
| 12 | `sep_drop_json_u0026` | kill K1 cf-kpi-first-json, K4 live-d missing | fail(K1,K4,K7,K8) / fail(K1,K4,K7,K8) | **KILLED** | K1,K4,K7,K8 |
| 13 | `cf_sig_floor_12` | kill K4 extra S013 | fail(K1,K4,K8) / fail(K1,K4,K8) | **KILLED** | K1,K4,K8 |
| 14 | `cf_sig_floor_64` | survive if every positive sig is >=64 (CFSIG=74, generated 172-344) | pass(-) / pass(-) | **SURVIVED** | — |
| 15 | `cf_sig_floor_75` | kill K1 cf-canned (CFSIG is 74) | fail(K1,K4,K8) / fail(K1,K4,K8) | **KILLED** | K1,K4,K8 |
| 16 | `cf_sig_class_drop_tilde` | kill (first ~ at index 18) | fail(K1,K3,K4,K7,K8) / fail(K1,K3,K4,K7,K8) | **KILLED** | K1,K3,K4,K7,K8 |
| 17 | `cf_sig_class_drop_hyphen` | kill (first - at index 26) | fail(K1,K3,K4,K7,K8) / fail(K1,K3,K4,K7,K8) | **KILLED** | K1,K3,K4,K7,K8 |
| 18 | `cf_sig_class_drop_underscore` | kill (first _ at index 37) | fail(K1,K4,K7,K8) / fail(K1,K4,K7,K8) | **KILLED** | K1,K4,K7,K8 |
| 19 | `cf_sig_class_add_plus_slash` | kill: this spec also **drops `-`** (first `-` at index 26), so it is not a pure widening; the pure widening is #45 | fail(K1,K3,K4,K7,K8) / fail(K1,K3,K4,K7,K8) | **KILLED** | K1,K3,K4,K7,K8 |
| 20 | `cf_sig_nocase` | kill by crash: `(?i)` placed mid-pattern raises an uncaught `re.error` (K3 `summary=none`); the behavioural case is #46 | fail(K1,K2,K3,K4,K7,K8) / fail(K1,K2,K3,K4,K7,K8) | **KILLED** | K1,K2,K3,K4,K7,K8 |
| 21 | `cf_sig_name_typo` | kill K1/K4 | fail(K1,K3,K4,K7,K8) / fail(K1,K3,K4,K7,K8) | **KILLED** | K1,K3,K4,K7,K8 |
| 22 | `cf_kpi_len_8_8` | kill K1 cf-canned (KPI is 15) | fail(K1,K3,K4,K7,K8) / fail(K1,K3,K4,K7,K8) | **KILLED** | K1,K3,K4,K7,K8 |
| 23 | `cf_kpi_len_8_64` | survive (no 33+ id fixture) | pass(-) / pass(-) | **SURVIVED** | — |
| 24 | `cf_kpi_len_1_32` | survive (no 1-7 id fixture; S010 value starts lower-case) | pass(-) / pass(-) | **SURVIVED** | — |
| 25 | `cf_kpi_lowercase_admitted` | survive (no lower-case id value fixture) | pass(-) / pass(-) | **SURVIVED** | — |
| 26 | `cf_kpi_no_lookahead` | survive (no fixture has an alnum/dash run after the id) | pass(-) / pass(-) | **SURVIVED** | — |
| 27 | `cf_kpi_lookahead_no_dash` | survive (no id followed by - or _) | pass(-) / pass(-) | **SURVIVED** | — |
| 28 | `cf_kpi_name_case` | kill K1/K4 | fail(K1,K3,K4,K7,K8) / fail(K1,K3,K4,K7,K8) | **KILLED** | K1,K3,K4,K7,K8 |
| 29 | `cf_alt_swap` | survive (equivalent: both branches tried at every start) | pass(-) / pass(-) | **SURVIVED** | — |
| 30 | `cf_alt_drop_sig_first` | kill K1 cf-canned, K4 S008/S009 | fail(K1,K3,K4,K7,K8) / fail(K1,K3,K4,K7,K8) | **KILLED** | K1,K3,K4,K7,K8 |
| 31 | `cf_alt_drop_kpi_first` | kill K4 live-d, K7 g2 | fail(K1,K4,K7,K8) / fail(K1,K4,K7,K8) | **KILLED** | K1,K4,K7,K8 |
| 32 | `az_alt_swap` | survive (equivalent) | pass(-) / pass(-) | **SURVIVED** | — |
| 33 | `az_lb_drop_both_escapes` | kill K1 azure-json-escaped-s127-order, K4 E3, K7 g3 | fail(K1,K4,K7,K8) / fail(K1,K4,K7,K8) | **KILLED** | K1,K4,K7,K8 |
| 34 | `az_lb_drop_json_u0026` | kill K1 azure-json-escaped-s127-order | fail(K1,K4,K7,K8) / fail(K1,K4,K7,K8) | **KILLED** | K1,K4,K7,K8 |
| 35 | `az_lb_drop_pct26` | survive (no azure %26 fixture) | pass(-) / pass(-) | **SURVIVED** | — |
| 36 | `az_lb_underscore_relaxed` | survive (no _sv= negative) | pass(-) / pass(-) | **SURVIVED** | — |
| 37 | `az_case_insensitive_dropped` | survive (every azure fixture is lower-case) | pass(-) / pass(-) | **SURVIVED** | — |
| 38 | `st_cases_zero` | survive (K1 checks only the substring SELFTEST-RESULT pass) | pass(-) / pass(-) | **SURVIVED** | — |
| 39 | `st_drop_cf_canned` | survive (K4 S008 keeps behavioural ground) | pass(-) / pass(-) | **SURVIVED** | — |
| 40 | `st_drop_cf_amz_beside_kpi` | survive (K4 S011 keeps behavioural ground) | pass(-) / pass(-) | **SURVIVED** | — |
| 41 | `st_drop_cf_lowercase_names` | survive (K7 n2 keeps behavioural ground) | pass(-) / pass(-) | **SURVIVED** | — |
| 42 | `st_drop_cf_short_sig` | survive (K4 S013 keeps behavioural ground) | pass(-) / pass(-) | **SURVIVED** | — |
| 43 | `st_drop_az_s127_order` | survive (K4 E3 + K8 keep ground) | pass(-) / pass(-) | **SURVIVED** | — |
| 44 | `st_flip_cf_short_sig` | kill K1 (selftest FAIL) | fail(K1) / fail(K1) | **KILLED** | K1 |
| 45 | `cf_sig_class_widen_keep_hyphen` | survive if no fixture has + or / adjacent | pass(-) / pass(-) | **SURVIVED** | — |
| 46 | `cf_nocase_at_pattern_start` | kill K1 cf-lowercase-names, K7 n2 extra | fail(K1,K7) / fail(K1,K7) | **KILLED** | K1,K7 |
| 47 | `cf_lb_escape_only` | kill K1 cf-canned (starts at '?'), K4 | fail(K1,K3,K4,K7,K8) / fail(K1,K3,K4,K7,K8) | **KILLED** | K1,K3,K4,K7,K8 |

## Table B — the 15 r88 `MutC2Scanner` survivors re-run against the r89 counter

| r88 # | r88 mutant | r89 re-run | r89 verdict | killing limb |
|---|---|---|---|---|
| 3 | `_PARAM` window `{0,20}?` -> `{0,1}?` | `r88_azure_param_window_1` (B) | SURVIVED | — |
| 4 | `_PARAM` name `[A-Za-z]{2,6}` -> `{2,3}` | `r88_azure_param_name_max3` (B) | SURVIVED | — |
| 6 | `_SIG` floor `{40,}` -> `{32,}` | `r88_azure_sig_floor_32` (B) | SURVIVED | — |
| 7 | `_SIG` drops `(?:=|%3D){0,2}` | `r88_azure_sig_padding_drop` (B) | SURVIVED (equivalent) | — |
| 8 | `_SV` -> literal `sv=2022-11-02` | `r88_azure_sv_hardcode` (B) | SURVIVED | — |
| 12 | `_LB` -> `(?<![A-Za-z0-9_])` (lookbehind deleted) | `az_lb_drop_both_escapes` (A #33) | **KILLED** | K1,K4,K7,K8 |
| 13 | `_LB` -> `(?<![A-Za-z0-9])` (underscore admitted) | `az_lb_underscore_relaxed` (A #36) | SURVIVED | — |
| 14 | GCS hex floor `{64,}` -> `{128,}` | `r88_gcs_floor_128` (B) | SURVIVED | — |
| 15 | GCS hex floor `{64,}` -> `{80,}` | `r88_gcs_floor_80` (B) | SURVIVED | — |
| 16 | GCS pattern loses `(?i)` | `r88_gcs_nocase` (B) | SURVIVED | — |
| 20 | scope `parts[:2] == [corpus, practice]` -> `parts[0] == corpus` | `r88_scope_prefix_loose` (B) | SURVIVED | — |
| 21 | scope `parts[3] == evidence` -> `parts[-2] == evidence` | `r88_scope_evidence_at_end` (B) | SURVIVED | — |
| 22 | selftest deletes `gcs-json-key` | `r88_st_drop_gcs_json_key` (B) | SURVIVED | — |
| 23 | selftest deletes `azure-html-amp` | `r88_st_drop_azure_html_amp` (B) | SURVIVED | — |
| 24 | selftest prints `cases=0` | `r88_st_cases_zero` (B) | SURVIVED | — |

One of the fifteen is now killed: r88 #12 (the azure lookbehind deleted) is caught by the r89 addition —
K1 `azure-json-escaped-s127-order FAIL got=none`, K4 `missing=corpus/practice/p/evidence/E3.json|azure-sas-signature`,
K7 `missing=g/x-receipts/live-g3.json|azure-sas-signature`, K8 `azure: \u0026 separator, sv sixth (S127 line 605 order), JSON-escaped`.
The other fourteen still survive. As a contrast, the r88 #5 mutant (`_SIG` floor `{40,}` -> `{64,}`) is still
killed at both seeds (K1, K4, K7, K8), so the kill path is not broken.

## Survivors: the planted case that would kill each (35)

Each probe below compares the frozen instrument with the mutant on one generated fixture (values drawn at
run time; only shape names are recorded). `separate=True` means frozen and mutant disagree, i.e. the stated
plant is a working kill case for that survivor.

| survivor | killing planted case (shape only) | limb that would then fire | probe (frozen vs mutant) |
|---|---|---|---|
| `cf_lb_drop_pct26` | CF URL whose first matched parameter follows a `%26` separator (`?Expires=1%26Signature=…&Key-Pair-Id=…`) | K4 `missing` (or K7) | frozen=cloudfront / mutant=none, separate=True |
| `cf_param_window_0_1` | CF URL with two intervening parameters between `Signature` and `Key-Pair-Id` (`&Expires=1&Hash-Algorithm=SHA256&`) | K4 `missing`, K7 | frozen=cloudfront / mutant=none, separate=True |
| `cf_param_name_letters_only` | CF URL whose intervening parameter name carries a hyphen (`Hash-Algorithm=SHA256`) | K4 `missing` | frozen=cloudfront / mutant=none, separate=True |
| `cf_param_name_upper_first` | CF URL whose intervening parameter name starts lower-case (`expires=…`) | K4 `missing` | frozen=cloudfront / mutant=none, separate=True |
| `cf_sig_floor_64` | positive with a 48-character `Signature` value | K4 `missing`, K7 | frozen=cloudfront / mutant=none, separate=True |
| `cf_kpi_len_8_64` | 40-character `Key-Pair-Id` value (frozen truncates at 32 and the lookahead fails) | K4 `extra` | frozen=none / mutant=cloudfront, separate=True |
| `cf_kpi_len_1_32` | 6-character `Key-Pair-Id` value | K4 `extra` | frozen=none / mutant=cloudfront, separate=True |
| `cf_kpi_lowercase_admitted` | `Key-Pair-Id` value containing lower-case letters | K4 `extra` | frozen=none / mutant=cloudfront, separate=True |
| `cf_kpi_no_lookahead` | `Key-Pair-Id=<id>-EXTRA` (frozen: the lookahead refuses; mutant: hit) | K4 `extra` | frozen=none / mutant=cloudfront, separate=True |
| `cf_kpi_lookahead_no_dash` | same `-EXTRA` fixture | K4 `extra` | frozen=none / mutant=cloudfront, separate=True |
| `cf_alt_swap` | none — both alternation branches are tried at every start | — (equivalent) | 6 fixtures, separated=none |
| `az_alt_swap` | none — same | — (equivalent) | 6 fixtures, separated=none |
| `az_lb_drop_pct26` | Azure SAS whose `sv` follows a `%26` separator (`?sp=rw%26sv=2022-11-02&sr=b&sig=…`) | K4 `missing`, K7 | frozen=azure / mutant=none, separate=True |
| `az_lb_underscore_relaxed` | negative `?_sv=2022-11-02&sig=…` (`_sv` is not a parameter) | K4 `extra` | frozen=none / mutant=azure, separate=True |
| `az_case_insensitive_dropped` | upper-case azure names (`?SV=2022-11-02&SIG=…`) | K4 `missing` | frozen=azure / mutant=none, separate=True |
| `cf_sig_class_widen_keep_hyphen` | negative: a 40+ run containing `+` or `/` beside a Key-Pair-Id (not a CloudFront signature) | K4 `extra` | frozen=none / mutant=cloudfront, separate=True |
| `r88_azure_param_window_1` | Azure SAS with two intervening parameters (`?sv=…&aa=1&bb=2&sig=…`) | K4 `missing` | frozen=azure / mutant=none, separate=True |
| `r88_azure_param_name_max3` | Azure SAS with a five-letter intervening name (`&skoid=1&`) | K4 `missing` | frozen=azure / mutant=none, separate=True |
| `r88_azure_sig_floor_32` | negative: 35-character `sig` value | K4 `extra` | frozen=none / mutant=azure, separate=True |
| `r88_azure_sv_hardcode` | Azure SAS with `sv=2024-11-04` | K4 `missing` | frozen=azure / mutant=none, separate=True |
| `r88_gcs_floor_128` | `X-Goog-Signature=<96 hex>` | K4 `missing` | frozen=gcs / mutant=none, separate=True |
| `r88_gcs_floor_80` | `X-Goog-Signature=<72 hex>` | K4 `missing` | frozen=gcs / mutant=none, separate=True |
| `r88_gcs_nocase` | lower-case `x-goog-signature=<128 hex>` | K4 `missing` | frozen=gcs / mutant=none, separate=True |
| `r88_scope_prefix_loose` | negative path `corpus/practice2/p/evidence/F.txt` (a sibling corpus tree) | K4 `extra` | frozen=False / mutant=True, separate=True |
| `r88_scope_evidence_at_end` | negative path `corpus/practice/p/sub/evidence/F.txt` (deeper than `<pkg>/evidence/`) | K4 `extra` | frozen=False / mutant=True, separate=True |
| `r88_azure_sig_padding_drop` | none — the group is unreachable (three padding forms separate nothing) | — (equivalent) | 3 fixtures, separated=none |
| `st_cases_zero` | none — behaviour identical; kill = K1 asserting the selftest case set (`SELFTEST <case> ok` present, `cases=43`) | K1 (strengthened) | cases=43 vs cases=42/0, both `pass` |
| `st_drop_cf_canned` | none — behaviour identical; kill = K1 asserting the selftest case set (`SELFTEST <case> ok` present, `cases=43`) | K1 (strengthened) | cases=43 vs cases=42/0, both `pass` |
| `st_drop_cf_amz_beside_kpi` | none — behaviour identical; kill = K1 asserting the selftest case set (`SELFTEST <case> ok` present, `cases=43`) | K1 (strengthened) | cases=43 vs cases=42/0, both `pass` |
| `st_drop_cf_lowercase_names` | none — behaviour identical; kill = K1 asserting the selftest case set (`SELFTEST <case> ok` present, `cases=43`) | K1 (strengthened) | cases=43 vs cases=42/0, both `pass` |
| `st_drop_cf_short_sig` | none — behaviour identical; kill = K1 asserting the selftest case set (`SELFTEST <case> ok` present, `cases=43`) | K1 (strengthened) | cases=43 vs cases=42/0, both `pass` |
| `st_drop_az_s127_order` | none — behaviour identical; kill = K1 asserting the selftest case set (`SELFTEST <case> ok` present, `cases=43`) | K1 (strengthened) | cases=43 vs cases=42/0, both `pass` |
| `r88_st_drop_gcs_json_key` | none — behaviour identical; kill = K1 asserting the selftest case set (`SELFTEST <case> ok` present, `cases=43`) | K1 (strengthened) | cases=43 vs cases=42/0, both `pass` |
| `r88_st_drop_azure_html_amp` | none — behaviour identical; kill = K1 asserting the selftest case set (`SELFTEST <case> ok` present, `cases=43`) | K1 (strengthened) | cases=43 vs cases=42/0, both `pass` |
| `r88_st_cases_zero` | none — behaviour identical; kill = K1 asserting the selftest case set (`SELFTEST <case> ok` present, `cases=43`) | K1 (strengthened) | cases=43 vs cases=42/0, both `pass` |

## Findings (routed defects / qualifiers)

**F1 — K8's clause map is a subset, and every survivor sits on an unmapped clause.** `CLAUSES` has 10
entries; the frozen C2 statement has clauses with no entry: (a) the URL-safe character class (only the
*floor* is mapped, via a 12-character negative), (b) `Key-Pair-Id=<8-32 upper-case alnum>` (neither bound,
nor the class), (c) "case-sensitive names", (d) "up to 20 other parameters between", (e) the azure `%26`
separator, (f) the azure signature-first parameter position (planted in K4 `w/z-receipts/live-c.json` but
not in `CLAUSES`). The `claims.json` annotation "maps every statement clause to a plant" overstates the
map. Every survivor that is a coverage gap sits inside (a)-(f) or is a selftest-case-presence point; the
two alternation swaps and the padding-drop mutant are equivalent by construction, not gaps.

**F2 — the CloudFront `\u0026` boundary has exactly one ground and it is seed-dependent.** K1
`cf-kpi-first-json` and K4 `w/q-receipts/live-d.json` both start their match at `?`; only K7's `live-g2.json`
starts after a `\u0026`, and `generated()` draws its leading parameters with `r.randint(0, 4)`, so about one
seed in five produces an empty prefix and leaves the boundary unexercised. Mutant `cf_lb_drop_json_u0026`:
`fail(K7)` at seed 8989 (`missing=g/x-receipts/live-g2.json|cloudfront-signed-url-signature`), `pass` at
seed 1. The azure counterpart is deterministic (K1, K4, K7, K8 all fire).

**F3 — `%26` is unexercised in both patterns.** `cf_lb_drop_pct26` and `az_lb_drop_pct26` pass every limb
at both seeds while the probes separate; no snapshot, selftest case, K4 plant or K7 plant uses `%26` as a
separator. The statement names `%26` for azure and the docstring names it for both.

**F4 — the CloudFront parameter window is pinned only at 0 vs >=1.** `{0,1}?` survives; `{0,0}?` and
`{1,20}?` are killed. No fixture has two intervening parameters, so "up to 20 other parameters between" is
untested. The name class is pinned only by `Expires` (letters only, upper first, 7 characters):
`[A-Za-z]{1,32}` and `[A-Z][A-Za-z0-9_-]{0,31}` both survive.

**F5 — every `Key-Pair-Id` bound is individually unpinned.** `{1,32}`, `{8,64}`, `[A-Za-z0-9]{8,32}`, the
lookahead deleted, and the lookahead narrowed to `(?![A-Za-z0-9])` all pass both seeds. Only the 15-character
fixture (`{8,8}` collapse) and the literal name are caught.

**F6 — the CloudFront signature floor is pinned only in 40..74, and the class only incidentally.** `{64,}`
survives, `{75,}` is killed (the single 74-character fixture). Dropping `~`, `-` or `_` from the class kills,
but only because each of those characters occurs before index 40 in that one fixture; widening the class with
`+` and `/` survives, and the probe separates on a negative (`+`/`/` inside a 40+ run is not a CloudFront
signature).

**F7 — case-sensitivity is grounded for CloudFront but not for Azure.** `(?i)` at the CloudFront pattern
start is killed by K1 (`cf-lowercase-names`) and K7 (`extra=g/x-receipts/live-n2.txt`), but K4 has no
lower-case CloudFront plant. Removing `(?i)` from the azure pattern survives: no fixture anywhere uses an
upper-case azure parameter name.

**F8 — selftest case presence and count are unpinned (r88 #22-#24 unchanged).** Seven case deletions and
two `cases=0` mutants pass every limb; only an inverted expectation is caught (`st_flip_cf_short_sig`, K1). The new
CloudFront cases each have independent behavioural ground in K4/K7, so deleting one does not reduce
behavioural coverage — but the selftest's own completeness is unchecked.

**F9 — `(?:=|%3D){0,2}` in `_SIG` is still a dead group (r88 #7).** Three padding forms (`%3D%3D`, `==`,
none) separate nothing; the group can never enable a match the `{40,}` run does not already make.

**F10 — the two new allowlist rows are load-bearing for K3.** Any mutation that changes the matched bytes of
the S128/S130 documentation example fails K3 with `unused_allow=2` as well as K4. This is the one place where
the allowlist acts as an oracle for the new shape; it does not cover the class, the bounds or the window.

## Hygiene, restoration and reproducibility

* No lane, fleet or sibling-lane write. Every clone, commit and probe ran in
  `/fast/scratch/hyaku/kasegi-r89/MutC2Scanner/`, which is deleted before yield.
* No git mutation in the lane: the only git writes were inside the scratch clone (toplevel asserted).
* No fixture bytes and no matched value in any wave file: receipts carry `LIMB` lines, sha256 digests and
  selftest case names; `probes.json` carries shape names only. Self-check with the landed scanner over this
  report and every file in `MutC2Scanner-receipts/`:

```
$ python3 -B corpus/instruments/capture-secret-scan.py --files .ufo/waves/round-89/w1/MutC2Scanner.md .ufo/waves/round-89/w1/MutC2Scanner-receipts/*
CAPTURE-SECRET-SCAN mode=files scanned=65 hits=0 files=0 allowed=0 unused_allow=19 rc=0
```

(`unused_allow=19` is the default allowlist's rows for paths `--files` did not scan; no row was consumed
and no hit was reported.)

* Restoration evidence (the frozen bytes were never mutated in place; the clone was restored and re-run):

```
before: sha256(corpus/instruments/capture-secret-scan.py) = 95f24a541db8b3d6693315a03de28d0b6de0fb0b6e53a68471265382114d20ec
        git show c61c5586:corpus/instruments/capture-secret-scan.py | sha256sum = 95f24a54...14d20ec
        sha256(.ufo/waves/round-89/c2/candidate/capture-secret-scan.py) = 95f24a54...14d20ec
after : sha256(corpus/instruments/capture-secret-scan.py) = 95f24a541db8b3d6693315a03de28d0b6de0fb0b6e53a68471265382114d20ec
        git -C <lane> status --porcelain --untracked-files=no -> (empty)
        clone HEAD instrument sha256 = 95f24a54...14d20ec, git -C <clone> status --porcelain -> (empty)
```

* Re-runnable: `MutC2Scanner-receipts/mutants.tsv` lists every mutant with its exact `old -> new` pattern
  text (no fixture values), the mutated sha256, both seeds' failing limbs and the verdict; each receipt is
  the counter's own `LIMB`/`CAPABILITY-CHECK` output for that mutant. `sweep.json` is the machine-readable
  table and `probes.json` the survivor separation evidence.

## Files written

* `.ufo/waves/round-89/w1/MutC2Scanner.md` (this report)
* `.ufo/waves/round-89/w1/MutC2Scanner-receipts/` — 61 per-mutant receipts, `sweep.json`, `probes.json`,
  `mutants.tsv`
