# ReviewWindow — round 89, one falsifiable hypothesis

**Hypothesis.** The round-89 scanner misses a realistic CloudFront or Azure signed URL whose
two matched parameters are separated by more than the 20-parameter window, or by a parameter
whose name falls outside the name class (`_PARAM` `[A-Za-z]{2,6}`, `_CF_PARAM`
`[A-Za-z][A-Za-z0-9_-]{0,31}`).

**Verdict: CONFIRMED for Azure, REFUTED for CloudFront.** One documented Azure SAS query
parameter, `skdutid` (7 letters), is outside `_PARAM`'s name class, and any signed URL that
carries it between `sv` and `sig` is missed in full. The window prong is also real but needs a
fat URL (exactly 20 between = hit, 21 = miss).

Instrument under test: `corpus/instruments/capture-secret-scan.py` at the C2 landing
`c61c55868e6d28653f57413bac6a6de5a398d11f` — file sha256
`95f24a541db8b3d6693315a03de28d0b6de0fb0b6e53a68471265382114d20ec` (equals the frozen
candidate pin in `claims.json`), git blob `f14ee4a695857deb0142416ed73ec6f3fbb895f4`.
Extracted read-only with `git show <rev>:<path>` into scratch; every question below is answered
by running the landed compiled regex, never by re-reading the pattern text.

## 1. The break: `skdutid`

| item | value |
|---|---|
| parameter | `skdutid` = `signedKeyDelegatedUserTenantId` (Azure SAS URI parameter) |
| source | `https://learn.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas`, plain GET, fetched 2026-11-07T06:15:28Z, sha256 `e5e4e893…0a78` (html) / `184d191b…088e` (normalized text) |
| source line | SAS-parameter table **lines 1472–1483** (columns "SAS field name / SAS token parameter / Required or optional / Version support / Description": `skdutid`, Optional, "2025-07-05 and later"); prose **line 3513** "The sduoid and skdutid fields are supported with version 2025-07-05 and later"; prose **line 3471** |
| why it breaks | 7 letters > `{2,6}`; `_PARAM` cannot step over `&skdutid=…`, so the match dies at that `sv` and there is no fallback |
| corpus coverage | 0 mentions of `skdutid`/`sduoid`/`srh`/`srq` in `S127.txt` (r88 "Create a service SAS"); the live doc is the only source that names it |

Smallest documented-shape URL the landed scanner misses (3 parameters; `<…>` are placeholders,
no signature value appears anywhere in this report or the receipts):

```
https://acct.blob.core.windows.net/sascontainer/blob1.txt?sv=2025-07-05&skdutid=<tenant-guid>&sig=<44-char>
```

Minimal semantically meaningful form (what a cross-tenant user-bound delegation SAS looks like;
`skdutid` is required only when the `sduoid` user's tenant differs from the account's):

```
https://acct.blob.core.windows.net/sascontainer/blob1.txt?sv=2025-07-05&sduoid=<user-guid>&skdutid=<tenant-guid>&sig=<44-char>
```

A/B proof that the name — not the value, order, separator or length — is the cause: the same URL
with `skdutid` removed hits (fixtures `az_f1` miss / `az_f2` hit, identical signature bytes).
`skdutid` placed **after** `sig` hits (`az_f7`): the miss is position-dependent, and the canonical
SDK order puts the signature last, so the canonical order is the missing one.

## 2. Counts

| source | documented query-parameter names | outside the class |
|---|---|---|
| user-delegation doc (live, 2026-11-07) | **35** (`sv sr st se sp sip spr skoid sktid skt ske skv sks saoid suoid scid skdutid sduoid srh srq sdd ses tn spk srk epk erk sig rscc rscd rsce rscl rsct bv bs`) | **1** — `skdutid` |
| `S127.txt` (r88 service SAS) | all documented parameter tokens ≤ 5 letters; no parenthesised 7–12-letter short name | 0 |
| `S130.txt` (CloudFront custom policy) | **5** (`Policy`, `Signature`, `Key-Pair-Id`, `Expires`, `Hash-Algorithm`) | **0** |

Behavioural classification (each name inserted as an intervening parameter in a real URL and run
through the landed regex, so the class is measured, not assumed): Azure 33 testable names →
**32 in class, 1 out** (`skdutid`, doc line 1477); CloudFront 3 testable names → **3 in class, 0 out**.

Window boundary, all names in class, no out-of-class name present:

| params between | Azure | CloudFront |
|---|---|---|
| 19 | hit | hit |
| **20** | **hit** | **hit** |
| **21** | **miss** | **miss** |
| 22 | miss | — |

So the window is exactly the declared "up to 20 other parameters between". A Blob
user-delegation SAS can carry **28** documented parameter names between `sv` and `sig`
(`sr st se sp spr sip skoid sktid skt ske sks skv saoid suoid scid sduoid skdutid srh srq sdd ses
rscc rscd rsce rscl rsct bv bs`), i.e. the documented shape can exceed the window; a realistic
17-name UD SAS still hits (`az_f4b`), so the window prong is real but needs an unusually fat URL,
while the name-class prong fires on a 3-parameter URL.

## 3. Fixtures (scratch only; receipts carry digests and scanner lines, never fixture bytes)

| fixture | shape | azure | cloudfront |
|---|---|---|---|
| `az_f1_skdutid_min` | `sv` + `sduoid` + **`skdutid`** + `sig` | **miss** | — |
| `az_f2_control_no_skdutid` | same, `skdutid` removed | hit | — |
| `az_f3_skdutid_alone` | `sv` + **`skdutid`** + `sig` | **miss** | — |
| `az_f4_ud_full` | 18-param user-delegation SAS incl. `skdutid` | **miss** | — |
| `az_f4b_ud_full_no_skdutid` | same, `skdutid` removed | hit | — |
| `az_f5_doc_example_documented_order` | doc's `srh`/`srq` example, request params after `sig` | hit | — |
| `az_f6_doc_example_request_params_first` | same, `operation`/`identifier` before `sv` | hit | — |
| `az_f7_skdutid_after_sig` | `skdutid` after `sig` | hit | — |
| `cf_f1_canned` | S128 doc example shape | — | hit |
| `cf_f2_custom` | S130 doc example shape | — | hit |
| `cf_f3_kpi_then_sig` | `Key-Pair-Id` first | — | hit |
| `cf_f4_underscore_user_param_between` | `Signature` + `_ga` + `Key-Pair-Id` | — | **miss** |
| `cf_f5_dotted_user_param_between` | `Signature` + `foo.bar` + `Key-Pair-Id` | — | **miss** |
| `cf_f6_21_user_params_between` | 21 user params between | — | **miss** |

Scanner CLI over all 14 fixtures: `scanned=14 hits=8 files=8` — the 6 misses are exactly the rows
marked miss. Seed `8901`, printed by the probe; signatures are generated at run time from that
seed, never stored.

## 4. CloudFront prong: REFUTED

Every documented CloudFront parameter name is inside `[A-Za-z][A-Za-z0-9_-]{0,31}`
(`Hash-Algorithm` is the widest at 14 with hyphens), and the documented orders put nothing between
`Signature` and `Key-Pair-Id`, so both canonical shapes hit (`cf_f1`, `cf_f2`, `cf_f3`).
Residual, not a documented CF shape: `S130.txt` lines 46–58 explicitly permit "your own query
string parameters … in any order", so a user parameter named `_ga`, or containing `.`, or 21 of
them, between `Signature` and `Key-Pair-Id` also misses (`cf_f4`–`cf_f6`). Same two limits, but
neither is a documented CF parameter name nor a realistic CF order.

## 5. Routed defect (the instrument is frozen; nothing was edited)

**D1 (severity: high for the instrument's purpose, medium for corpus frequency).**
`_PARAM`'s `[A-Za-z]{2,6}` silently excludes the documented Azure parameter `skdutid`, so a
current, supported (sv ≥ 2025-07-05) Azure user-bound delegation SAS is not detected at all.
The gap is *undeclared*: the instrument's Known-limits block (`capture-secret-scan.py:61-65`)
lists GCS V2, CloudFront cookies, percent-encoded names, "more than 20 other parameters between",
soft-wrap and gzip/UTF-16/base64 — but not the name class. A reader therefore believes the only
inter-parameter limit is the window width.

Fix (for the next claim, not this round): widen `_PARAM` to `[A-Za-z]{2,8}` (or to
`[A-Za-z][A-Za-z0-9_-]{0,31}`, the class already used for CloudFront), add a K4 plant with a
7-letter documented name between `sv` and `sig`, and add a selftest case. Re-pin the instrument.

This is precisely the round-88 survivor that was routed rather than re-planted: mutant 4
`_PARAM` name width `[A-Za-z]{2,6}` → `{2,3}` **SURVIVED** (`.ufo/waves/round-88/w1/MutC2Scanner.md:52`),
and `claims.json` records "the r88 MutC2Scanner survivors on the azure window/name width/sv form
are not re-planted this round (named, routed)". The landed K4 plants carry only 2–4 letter names
(`sp`, `spr`, `st`, `se`, `sv`, `sr`), so K4 still cannot see a name-width change in either
direction — the survivor was not cosmetic: the documented name set needs width 7.

## 6. Qualifiers on the frozen claim (not a re-score)

- The C2 statement declares the window ("up to 20 other parameters between (S128, S130)") and says
  nothing about the Azure name class; the instrument's self-description likewise omits it. The
  finding is a residual false negative outside every claimed clause, so no frozen predicate
  P1–P3 is falsified and the claim is not re-scored here.
- The 20-parameter window is *declared* in the docstring and is measured here at exactly 20/21 —
  consistent, no overstatement found.

## 7. Re-run

```sh
S=$(mktemp -d -p /fast/scratch/hyaku/kasegi-r89 rw.XXXXXX); export TMPDIR=$S
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
for f in capture-secret-scan.py claim-package-check.py capture-secret-allow.tsv; do
  git show c61c55868e6d28653f57413bac6a6de5a398d11f:corpus/instruments/$f > "$S/$f"; done
sha256sum "$S/capture-secret-scan.py"   # 95f24a54…d20ec
RW_SCRATCH="$S" python3 -B .ufo/waves/round-89/w1/ReviewWindow-receipts/probe.py
python3 -B "$S/capture-secret-scan.py" --files "$S"/fixtures/*.txt
```

Receipts (beside this file): `ReviewWindow-receipts/probe.py` (the harness),
`probe-out.txt` (counts + hit/miss table + fixture digests), `scanner-files.txt` (scanner
`--files` output over the 14 fixtures), `source-fetch.txt` (fetch metadata, doc line refs, the
35-name enumeration, S127 token enumeration).

## 8. Residual risk and verification gaps

- `skdutid` requires sv ≥ 2025-07-05 and a cross-tenant `sduoid`; no corpus instance exists yet
  (0 hits in `corpus/source-snapshots/`), so the frequency is unknown — the *shape* is documented
  and current, the *prevalence* is not measured.
- I did not test the account-SAS or queue/table parameter pages beyond `S127`; `S127` names no
  parameter wider than 5 letters, so the confirmed break is the user-delegation page only.
- CloudFront: only the two canonical orders plus the user-parameter variants were exercised;
  signed cookies (`CloudFront-Signature`) stay a declared limit and were not re-tested.
- No live target was probed; the only network call was the one plain GET named in the seat item.
- Scratch `/fast/scratch/hyaku/kasegi-r89/ReviewWindow` is deleted (trap on exit); no fixture
  bytes, signature values or snapshots were copied into the wave directory.
