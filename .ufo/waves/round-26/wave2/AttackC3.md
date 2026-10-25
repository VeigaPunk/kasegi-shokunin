# AttackC3 — duplication scan: F11 entries vs F10 entries

Seat: AttackC3 (read-only; wave 2 falsify). Date: 2026-10-25 UTC.
Item: compare the two new F11 entries against the two F10 entries for duplicated
quotes/themes, mirroring the round-25 verifier's duplication rule.

## The rule mirrored (round-25 verifier)

Round-25 admission recorded (`corpus/lessons/round-25.md:92-94`):

> A critic confirmed no exact admitted entry overlap, and a connector confirmed no
> sibling lane holds F10 …

So the round-25 duplication standard for a newly admitted entry is: **no exact
quote overlap with any already-admitted entry** (critic arm), plus a thematic
sibling-lane check (connector arm, out of scope here). I apply the exact-quote
arm to both new F11 entries against the two F10 entries, and separately report
theme overlap. Comparison normalization follows QUALITY Q8 (collapse whitespace,
incl. full-width space) before exact match; source+capture-line identity is
checked where the entries cite locations.

## Objects compared

| Entry | File |
|---|---|
| F10-A | `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` (S036–S039) |
| F10-B | `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` (S040; S036/S038/S039) |
| F11-1 | `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` (S041; S039/S040 corroboration) |
| F11-2 | `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` (S041) |

## Verdicts

### F11-1 `iso-29147-and-30111-division-of-labour.md` — **FAILS the exact-quote arm (2 duplicate quotes)**

Two of its 11 quoted strings are byte-identical (after Q8 normalization) to
quotes already admitted in the F10 entries, same source, same capture line:

| F11-1 quote id | verbatim | F10 prior occurrence(s) |
|---|---|---|
| `cisco-iso-29147-2018` | "The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018" | F10-B `cisco-iso-29147-2018` (S040.txt:58, §Cisco Product Security Incident Response) — identical string, identical source, identical capture line |
| `hitachi-step1-29147` | "ステップ１：脆弱性情報の入手 ... (1) ISO/IEC 29147:2014 脆弱性情報の開示" | F10-B `hitachi-29147-2014` (S039.txt:497, §1.1 概要) **and** F10-A claim 7 (S039.txt:497) — identical string, identical source, identical capture line |

Grounding: `grep` on the pinned captures confirms both strings are real bytes
(`corpus/source-snapshots/round-25/S040.txt:58`, `S039.txt:497-499`) and appear
verbatim in the F10 entries' quote records (`vendor-disclosure-policy-commitments-crosswalk.md:46,64`;
`vendor-disclosure-policies-as-corpus-objects.md:149-150`).

Partial/adjacent overlap: `hitachi-step2-30111` (S039.txt:498) and
`hitachi-step3-29147` (S039.txt:499) are new strings, but they are the
same-line-paragraph siblings of the duplicated `hitachi-step1-29147` and extend
the same Hitachi ISO-mapping evidence block F10 already carries (F10-A claim 7;
F10-B row `hitachi-29147-2014`). So the *evidence block* overlap is larger than
the exact-string count: 3 of 11 F11-1 quote rows sit inside the Hitachi
S039:497-499 family already cited by F10, plus the Cisco L58 sentence.

Theme overlap: the "edition, not presence" theme (JPCERT/Hitachi 2014 vs Cisco
2018) duplicates F10-B's falsifiable rule 1 and its `named standard + edition`
crosswalk row; the Hitachi three-step ISO mapping duplicates F10-A claim 7's
prose. The *division-of-labour* claim itself (29147 = outward exchanges, 30111 =
in-house verification/countermeasure development, anchored to S041 付録6 §2) is
new.

### F11-2 `iso-29147-divergence-and-clause-crosswalk.md` — **PASSES the exact-quote arm (0 duplicates)**

None of its 6 quoted strings (all S041: `q-policy-not-required`, `q-policy-required`,
`q-seven-day-receipt`, `q-min-policy-aspects`, `q-optional-policy-aspects`,
`q-secure-comm-option`) appears in either F10 entry. Theme overlap is limited to
the trailing S040 pointer paragraph, which the entry explicitly handles: it
states the F10-B entry already verified the Cisco claim and that it does not
re-make it (S040 used only as the guideline's own real-world example). This is
the round-25 rule's intended behaviour — defer to the prior entry rather than
duplicate.

## Unique content each F11 entry adds

F11-1 (division-of-labour):
- New source S041 (JPCERT/CC 2026 P-guideline, 付録6 §2) pins the definitional
  claim: 29147:2014 governs the outward half ("社外とのやりとり": receiving
  vulnerability info from outside + distributing countermeasure advisories to
  users; subjects = product developers, online-service providers, intermediate
  vendors), 30111:2013 governs the in-house half (verification + countermeasure
  development) — S041.txt:1667-1672.
- Figure-1 title/caption ("ISO/IEC 29147 と ISO/IEC 30111 の対応", drawn from
  29147:2014) — S041.txt:1677-1678.
- Hitachi step-level corroboration extended to all three steps, including new
  `hitachi-step2-30111` / `hitachi-step3-29147` strings (step 3 public
  disclosure → 29147, not 30111) — S039.txt:498-499.
- Edition-contrast falsifiable rule with grep-recheckable counts (29147:2018
  occurs once in S040; 29147:2014 occurs 24× in S041).
- Rejected over-generalizations ("29147 is only about receiving reports";
  "vendors follow 29147:2014" without edition).

F11-2 (divergence/clause crosswalk):
- The obligation-contrast pair (guideline does **not** require a vendor to adopt
  a vulnerability disclosure policy; 29147:2014 does require formulation and
  partial publication) — S041.txt:1868-1870.
- Seven-day acknowledgement split into two voices: the guideline's conformance
  guidance ("必要となります", L1916, manifest Q4) vs the standard text it quotes
  ("recommended ... within seven calendar days", L1901-1903).
- The 6.2 minimum-policy-aspects (six lettered elements) vs 6.3 optional
  (credit-to-finder, synchronized disclosure, distribution) partition of the
  29147:2014 clause-6 republication — S041.txt:1813-1866.
- The 参考1 clause-to-section cross-reference table, including the "－" rows for
  clauses 6 (disclosure policy) and 8 (inter-vendor reporting) — S041.txt:1996-2079.
- Explicit attribution rule: standard claims are attributed to the guideline's
  reproduction, not to a direct reading of the paywalled ISO text.

## Risks / notes

- F11-1 violates the exact-quote arm as stated. Its two duplicate quotes are
  load-bearing (Cisco edition alignment; Hitachi step-1 mapping), not incidental;
  the entry uses them as corroboration of a new claim rather than as a new
  finding. If the round-25 rule is applied strictly, F11-1 should have either
  cross-referenced F10 instead of re-quoting, or marked the two as reused
  evidence. This is a duplication defect, not a factual error.
- F11-2's explicit non-duplication paragraph is the model the F11-1 entry could
  have followed.
- Baseline: the two F10 entries themselves share ~10 exact quotes (cybozu-*,
  pepabo-*, hitachi-* families) by design — the F10 crosswalk re-lists the F10-A
  captures. The F11-vs-F10 overlaps above are additive to that baseline, not a
  new phenomenon, but the round-25 rule was applied *at admission* (new entry vs
  previously admitted), which is the standard mirrored here.

## Evidence exercised

- `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` (F10-A)
- `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` (F10-B)
- `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` (F11-1)
- `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` (F11-2)
- `corpus/source-snapshots/round-25/S039.txt:497-499`, `S040.txt:58`
- `corpus/source-snapshots/round-26/S041.txt:1666-1674,1868-1870,1916,1813,1856,1851`
- `corpus/lessons/round-25.md:92-94` (duplication rule), `corpus/QUALITY.md` Q3/Q8
- `corpus/README.md:211-212` (F10/F11 rows)

Tooling: no installs (no tool change needed). No files outside the report path
were written.
