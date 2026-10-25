# C2ProvinceScope — wave-2 falsification of the wave-1 C2 scope verdict

Seat: `L1Kasegi25.C2ProvinceScope` (critic, READ-ONLY). Lane root
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`; base revision `b49948f`. No VCS write, no
spawn, no tool install (nothing installed or upgraded this seat). Report only; no production edit.

## 0. What was checked

Wave-1 admitted **two** entries (the wave-1 plan in `claims.json` planned one admit + one
reject; the landed set contains both a re-grounded Japan entry and a re-written crosswalk entry):

1. `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` (Japan vendors, S036–S039, "Japan entry")
2. `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` (Cisco + Japan S040/S036/S038/S039, "crosswalk entry")

Checks performed (all measured, commands below): C2 counter (3 limbs), PROVINCE Core/Frontier
reading (`PROVINCE.md:27-40`), Q1–Q6 against both entries (header form, tier-A rows, verbatim
quotes and ≤25-word limit, attribution, falsifiable rules + rejections, documentation-only), the
two-entry scope (R8 identity, F10 row, manifest binding, no duplicate authority), recheck lines
(bash -n, exit, byte-identical digest from `/`), the 40-row registry (`SOURCES.md`), the F10
row (`corpus/README.md`), capture log, and the frontier harness.

## 1. C2 counter — measured, passes

Commands (exact bytes of `claims.json` C2 counter):

```
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
10
$ grep -lE '^source: S0(3[6-9]|[4-9][0-9])' corpus/knowledge/*.md | wc -l
2
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
$ echo exit=$?    -> exit=0
```

Predicate met: frontier=10, two entries carry `source:` ids first registered this round, census
exit 0 (W04 x2 are the same pre-existing S028/S029 warnings recorded in `claims.json`). The two
citing entries: `vendor-disclosure-policies-as-corpus-objects.md` (S036–S039) and
`vendor-disclosure-policy-commitments-crosswalk.md` (S040/S036/S038/S039).

Kill-rule check: `SOURCES.md` has 40 rows; exactly five are new (S036–S040), all lane-normalized
(lane ids, no staged S055/S056/S057/S060/S068 anywhere: `grep -nE 'S0(4[1-9]|[5-9][0-9])|S1[0-9][0-9]' corpus/SOURCES.md`
→ no output). Every new row is cited by ≥1 admitted entry (S037 only by the Japan entry; S040
only by the crosswalk). No row appended without an admitted entry citing it; no staged row appended
unnormalized. Kill rule not triggered.

## 2. PROVINCE Core / Frontier

`PROVINCE.md:27-33` Core: "program rules, scopes, and claim packages; … triage and claim gates,
and submission/disclosure packaging." `PROVINCE.md:35-40` Frontier: F01–F10; F10 is "round 25:
vendor-side disclosure policies as corpus objects; 10/10 admitted". Both entries are Frontier F10
objects (`ground: F10` in both; F10 row in `corpus/README.md:211` lists both entries, sources
S036–S040). Domain fit: vendor-side disclosure policies are the vendor's half of
submission/disclosure packaging, the lane's refusal clause (`PROVINCE.md:25`) does not exclude
them (no live-target testing is instructed — Q6 scans below). Scope verdict holds for both entries.

## 3. Q1–Q6 per entry (with evidence)

Header form: each entry opens with H1, then **four** `source:` lines, `verified-at: 2026-10-25`,
one `recheck:` line, `ground:` line. Q1 says "three header lines: `source:`, `verified-at:`,
`recheck:`" — the landed form folds all four per-row `source:` lines and adds `ground:`
(precedent: `statutory-authorization-and-unauthorized-access.md` carries 3 `source:` lines +
`ground:`; `authorised-testing-rules-of-engagement.md` carries `ground:`; both admitted in earlier
rounds). The wave-1 seats already declared `head -3` unsatisfiable per-row ids and kept the block
in `head -8`; that deviation is unchanged and is the only way to meet the per-row-id requirement
of the harness. **No new deviation introduced.**

- Q1: header contains id/URL/anchor per source; `verified-at` = capture re-open date
  (2026-10-25; capture-log UTC 08:14Z same day). PASS.
- Q2: all five rows S036–S040 are tier A (`SOURCES.md` rows 42–46, column 4 = A), opened in the
  admitting round (capture-log `utc=2026-10-25T08:14:2xZ`, all status=200). No tier-C sole
  support. PASS.
- Q3: 27 quoted claims in the Japan entry, 22 table quotes in the crosswalk — all verbatim in
  their captures (see §4) and all present in the manifest. English quotes ≤25 words (measured:
  max = `cisco-default-hold` 22 words; all others 1–15). Japanese quotes are counted as
  whitespace-separated tokens under the same rule (the crosswalk states this; max tokens in a
  quoted sentence ≈ 24); the two entries apply the bound consistently. PASS, with one internal
  line-range contradiction — §5.
- Q4: every claim is attributed to the named vendor (the Japan entry's "Attribution" block; the
  crosswalk's per-row vendor column); the crosswalk's "one sentence the sample supports" is
  explicitly scoped to "these four policies". No vendor policy is stated as a universal rule of
  vendors. PASS.
- Q5: Japan entry has 4 falsifiable rules (FR-1..FR-4) and 5 rejected over-generalizations with
  reasons; crosswalk has 4 rules and 2 rejections with reasons. All rules were re-run (below).
  PASS.
- Q6: `grep -nEi 'curl|wget|nmap|scan|probe|submi|contact|login|log in|検証し|スキャン|送信|アクセスし|攻撃し|実行し|credential|password|session|vault'`
  — Japan entry: 4 hits, all benign (source URL line 5; rejection prose lines 178/180; negative
  documentation statement lines 210-211). Crosswalk: 2 hits (source URL line 4; limits note about
  the capture instrument's `curl -L` 403, describing the capture, not instructing activity). No
  credentials/session/private URL/vault URI in either. PASS.
- Documentation-only posture is restated in both entries' limits sections.

Falsifiable-rule greps re-run (all as claimed):

```
$ for f in S036 S038 S039 S040; do printf '%s %s\n' "$f" "$(grep -c 29147 $f.txt)"; done
S036 0 / S038 0 / S039 8 / S040 1          # rule 1 "Edition, not presence"
$ for f in S036 S038 S039 S040; do printf '%s %s %s %s\n' "$f" "$(grep -c JPCERT $f.txt)" "$(grep -c 'CERT/CC' $f.txt)" "$(grep -c 'JP-CERT' $f.txt)"; done
S036 1 1 0 / S038 0 0 0 / S039 2 7 0 / S040 0 2 1   # rule 2 coordinator counts
$ for f in S036 S037 S038 S039 S040; do printf '%s %s\n' "$f" "$(grep -c '報奨金' $f.txt)"; done
S036 1 / S037 11 / S038 1 / S039 0 / S040 0          # rule 3 money states
$ grep -n 'CVSS\|深刻度\|実現可能性' S038.txt  -> 19 (no instrument named; both entries say so)
```

## 4. Recheck binding — measured

Both `recheck:` lines pass `bash -n` (exit 0), run from lane root AND from foreign cwd `/`
with identical exit 0 and byte-identical stdout+stderr:

```
vendor-disclosure-policies-as-corpus-objects.md   lane exit=0 sha256 b15f167f… ; foreign exit=0 sha256 b15f167f… IDENTICAL
vendor-disclosure-policy-commitments-crosswalk.md lane exit=0 sha256 64df1c66… ; foreign exit=0 sha256 64df1c66… IDENTICAL
```

Both lines chain one `source-recheck.py` invocation per source id (the F-1 four-invocation fix,
not the single-value `--source` form). Fragment ids = recheck `--source` ids:
Japan `[S036,S037,S038,S039]`; crosswalk `[S040,S036,S038,S039]` (R12 limb A). The manifest
(`round-25/manifest.json`, rebuilt 05:51, sha256 `4d632090…`) lists sources S036–S040 (5
sources / 39 quotes); every record's sha256 matches its capture file (verified for all five);
`occurrences=1` printed per quote.

Quote→manifest conformance (independent re-extraction):

- Japan entry: 27 quoted pairs all present in the manifest pools (27/27).
- Crosswalk: 22/22 table quotes present in the manifest pools; 0 missing.

Frontier harness: `python3 corpus/instruments/frontier-recheck-count.py` → `entries=12 pass=12
exit=0` (both F10 entries PASS). Note: the harness exposes **no `--selftest` flag** (exit 2 with
"unrecognized arguments"), so the "harness 12/12" figure is the run itself; the manifest is bound
to the actual instrument runs above.

## 5. Found defect — crosswalk Rule 4 line ranges (smallest correction)

`vendor-disclosure-policy-commitments-crosswalk.md` Rule 4 (lines 90-94) states the four
expedite bullets on the S040 capture as "high-severity with fixes planned **(L301)**, observed
active exploitation **(L302-L305)**, potential for increased public awareness **(L306-L308)**,
and a declared high-profile third-party vulnerability **(L309)**". The capture bytes are:

```
301: The Cisco PSIRT has completed the incident response process for a high-severity vulnerability …
302: The Cisco PSIRT has observed active exploitation of a vulnerability that could lead to increased
303: risk for Cisco customers. Cisco will accelerate the publication of a security announcement
304: describing the vulnerability that may or may not include a complete set of patches or workarounds.
305: There is the potential for increased public awareness of a vulnerability affecting Cisco products
306: and/or cloud-hosted services that could lead to increased risk for Cisco customers. Cisco will
307: accelerate the publication of a security announcement describing the vulnerability that may or may
308: not include a complete set of patches or workarounds.
309: The Cisco PSIRT has declared a third-party software vulnerability to be high profile.
```

So bullet 2 = L302–L304, bullet 3 = L305–L308. The rule's ranges "(L302-L305)" and
"(L306-L308)" are **off by one line, in opposite directions**: the first over-includes L305 and
the second under-includes L305 (its own first line). This is an internal inconsistency with the
entry's own crosswalk table (`vendor-disclosure-policy-commitments-crosswalk.md:28`: "L302-L304,
L305-L308, L309") and with `corpus/SOURCES.md` row S040 ("four expedite bullets (L301, L302,
L305, L309)"), both of which match the capture. The claim itself (four bullets, not two — the
wave-1 refusal reason) is true and the count is right; only the two tr ranges in Rule 4's prose
are wrong.

Smallest correction: in Rule 4, change "(L302-L305), (L306-L308)" to "(L302-L304),
(L305-L308)". That matches the table, SOURCES row S040, and the capture. No other line, no
recheck, no manifest change; this does not void C2 (the counter and the four-bullet count are
unaffected) and does not reopen the Q3 refusal (the count claim is accurate — the ranges are a
presentational erratum, exactly the class the lane files as an R9-style correction).

Independent finding stored as-is (not a defect): the crosswalk's recheck verifies 33 quote
assertions including the sibling entry's S039 Q7/Q8/Q9 quotes (manifest records are shared); R12
only binds `--source` ids to the entry (satisfied). This couples the two entries' rechecks to the
shared manifest but does not weaken either claim.

## 6. Counterexample tested and what it settles

Strongest falsification available against the two-entry scope was: *does either entry's substance
survive re-reading the captures, and does the second entry add anything the first could not
carry?* Measured: both entries' load-bearing anchors re-verified (S036 L14/L19/L22/L28/L30/L44;
S037 L99/L101/L109/L111/L115/L123; S038 L17/L19/L20/L24/L25; S039 L491/L497/L506/L510/L519/L520/
L557; S040 L58/L162/L180/L187-L190/L245-L249/L254-L259/L300-L309/L319/L482/L487-L489), including
the S037 "verification environment" clause (S037:123 names 脆弱性検証環境提供プログラム — the Japan
entry's Claim 5 statement is supported) and the S039 section anchors (header §1.5 L535-L537 vs
quoted L557: both inside the actual section L535-L558; the header anchor is the section head, the
quote is its content — both correct). The one divergence found is §5's Rule-4 range slip, which
is a correction, not a rejection: the wave-1 verdict (admit both; refuse only the staged crosswalk
text's "two conditions" claim) stands.

## 7. Verdict

**Wave-1 C2 result holds** under adversarial re-check: frontier=10, rows=40 (5 new tier-A rows),
manifest 5 sources/39 quotes, harness 12/12, census exit 0, kill rule not triggered. Both admitted
entries pass Q1–Q6 and PROVINCE scope. **One smallest correction (non-production, no edit made):**
fix crosswalk Rule 4's bullet ranges to (L302-L304)/(L305-L308) to match its own table, SOURCES
S040, and the capture. That is a presentational erratum, not a claim reversal.
