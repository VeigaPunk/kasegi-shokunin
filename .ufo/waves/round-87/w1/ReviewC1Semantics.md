# ReviewC1Semantics — round 87, C1 landing semantic review

Inputs: base `cd1f568a6be2656b5f5dc479eb90ef99b91131b5`, freeze `afb13a88`, C1 landing
`d87b1b55a51d78411438e962a9abbebdd17930cd` (`.ufo/waves/round-87/landing.json`). Diff:
`git diff afb13a8 d87b1b5 -- corpus/knowledge/` = **5 files, +70/−70, 83 keys / 99 occurrences**
(S029 ×1, S040 ×1, S069 ×10 (12 occ), S100 ×1, S102 ×70 (84 occ)). No other knowledge file changed.

Every repointed value was judged against (a) the S-id's `corpus/SOURCES.md` row and the round
manifest record (id/path/sha256/line count), and (b) the anchored snapshot line(s) themselves.
All **82 anchored values** were opened and read (S102: every anchor; S069: all 10; S029: L20;
S100: L462/463), plus the five S040 hazard lines. Receipt: `ReviewC1Semantics-receipts/anchor-table.txt`.

Counter re-run as specified, on a `git clone --shared` of the landing under scratch (not at the
lane path): **pass, M1–M7, base 596/1720 → after 678/1719**, rc 0
(`ReviewC1Semantics-receipts/c1-counter.txt`). The frozen builder re-run at base reproduces the
frozen map and exclusion list exactly (`ReviewC1Semantics-receipts/builder-reproduction.txt`:
`MAP IDENTICAL (83 keys)`, `EXCLUDED IDENTICAL (10 tokens)`).

## Verdict per file

| file | keys/occ | capture | verdict |
|---|---|---|---|
| `corpus/knowledge/cra-manufacturer-reporting-duties.md` | 1/1 | `round-23/S029.txt` | **CORRECT** |
| `corpus/knowledge/first-psirt-maturity-document.md` | 1/1 | `round-67/S100.txt` | **CORRECT** |
| `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` | 10/12 | `round-44/S069.txt` | **CORRECT** |
| `corpus/knowledge/openssf-scorecard-api-contract.md` | 70/84 | `round-68/S102.txt` | **CORRECT** |
| `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` | 1/1 | `round-25/S040.txt` | **CORRECT** |

No WRONG and no UNCLEAR key.

### cra-manufacturer-reporting-duties.md — `S029.txt:20` → `round-23/S029.txt:20` (CORRECT)
- Capture is right: round-23 is the only tracked `S029.txt` (`git ls-files 'corpus/source-snapshots/*/S029.txt'`,
  one hit); round-23 manifest binds S029 to the EUR-Lex URL with sha `82514478…`; the entry's recheck
  line already uses `corpus/source-snapshots/round-23/manifest.json`.
- Anchor supports the sentence: L20 is Article 14(4)(a), "(a)an early warning notification of a severe
  incident … within 24 hours of the manufacturer becoming aware of it". The "not unique" claim is
  measured: the phrase occurs exactly twice in the capture, L10 (14(2)(a)) and L20 (14(4)(a)), so
  `:20` is the incident track the sentence names.
- Context: parenthetical citation. Nothing quoted or executable.

### first-psirt-maturity-document.md — `S100.txt:462` → `round-67/S100.txt:462` (CORRECT)
- round-67 is the only `S100.txt`; manifest sha `cf834a65…`, 478 lines; the entry's own `source:` and
  `recheck:` lines already bind round-67. The V67-3 correction is about the C15 anchor, not a re-quote.
- Anchor supports the sentence: L462 = `Training & Education`, L463 = `Train development teams`
  (so the area list ends at L462 and L463 is its item, exactly as written; 462/463 lie inside the
  recorded content range L216–L464).
- Context: backticked citation in prose; the `:463` continuation stays a short form and resolves
  against the now-full path in the same sentence — acceptable.

### google-cloud-vrp-customer-resource-boundary.md — 10 keys → `round-44/S069.txt` (CORRECT)
- round-44 is the only `S069.txt`; manifest sha `0932279c…`, 1132 lines; `SOURCES.md` S069 anchor cell
  names `corpus/source-snapshots/round-44/S069.txt` and the entry's `source:`/`recheck:` lines match.
- All ten anchors read as the sentences say: `10-11` contains the quoted scope sentence and matches
  manifest **Q5 (anchor 10)**; `61-62` boundary sentence; `62-63` prohibition sentence; `68-69`
  customer-domain examples; `70-72` ineligibility; `61-69` the whole "Do Not Test Customer Projects &
  Resources" block; `65-72` the two bullets the Limits paragraph summarises; `76-77` the customer-IP
  sentence (word count 21 verified); `78-86`/`78-87` the multi-tenant paragraph (both ranges contain
  "do not test it against the live multi-tenant environment" and "submit a report with your technical
  analysis and local reproduction"; 87 adds only the closing clause).
- Contexts: all parenthetical citations. Note (pre-existing, preserved): the same claim is cited as
  `78-86` in the table and `78-87` in the appended paragraph; both are true for their sentences.

### openssf-scorecard-api-contract.md — 70 keys → `round-68/S102.txt` (CORRECT)
- round-68 is the only `S102.txt`; manifest sha `6ebb8552…`, **429 lines**, identical to the sha and
  line count the entry states in its own `source:` line — the strongest possible binding.
- Every anchor was opened. Grouped evidence: info `9/11/13/14/15/17`; GET route `19/24/25/28/30/31-32/37/53/69`
  and `139/142/146/153` (platform/org/repo descriptions and their three `required` lines);
  POST `93/94/97/99/101/107`; `/version` `234/236/240/241/244`; badge `160/168/181-183/209`;
  definitions `268/271-272/275-276` (Error), `281/285/290/292` (Repo), `297/300-301/304-305/305/306/309-310/313-314/316-317/320-321/327-330`
  (ScorecardCheck), `336/339-340/343-345/347-350/352-355/353/354/358-361/365-366` (ScorecardResult),
  `371/375/380` (ScorecardVersion), `387/390-391/394-395/398-399/402-403` (VerifiedScorecardResult),
  `408/412` (+ continuations `:417`, `:422`) (VersionInfo). All match the quoted text and the
  type/description claims. `OIDC` occurs once (L93) and `grep -c '^"/'` = 3, as the entry says.
- Contexts: all 70 are parenthetical citations in prose or table cells. The file's command strings,
  file references and template were **not** rewritten: L53 `` `grep -c '^"/' S102.txt` ``, L97
  `over S102.txt`, L139 `byte-identical to S102.txt`, L13 `` `S102.txt:LINE` `` — all still bare.
  This is the point where the r86 Finding-1 class could have bitten; it did not.

### vendor-disclosure-policy-commitments-crosswalk.md — `S040.txt` → `round-25/S040.txt` (CORRECT)
- round-25 is the only `S040.txt` (manifest sha `b7f7b55f…`, 503 lines); the entry's Limits section
  already says locations are capture lines in `corpus/source-snapshots/round-25/`.
- The hazard note's lines are true of those bytes: L108, L193, L203, L222 and L479 each carry U+FFFD
  (verified `EF BF BD` with `cat -v`), and the entry's "no quote crosses them" statement is unaffected
  by the repoint.
- Context: this is the **only** key that is a bare file-name reference (a code span naming the capture,
  no `:N` anchor) rather than an anchored citation. It is not a quoted manifest field and not a command
  string, so it is not the r86 Finding-1 class; the rewrite is accurate and improves resolvability.
  Recorded as an observation, not a defect.

## r86 Finding-1 class check (quoted manifest field / command / file name)
- None of the 83 repointed occurrences sits inside a quotation of a manifest field or a command string.
  The four QUOTED tokens were left bare and each is indeed a manifest record's `path` field value being
  quoted: `doj-…:136` (`` path `S020.txt` ``), `cisa-bod-20-01-…:159` (`S021`), `cisa-cvd-program-stages.md:131`
  (`S023`), `cve-bench-agent-exploitation-benchmark.md:138` (`S025`). M7 holds.
- The un-repointed bare tokens in the five files are exactly the four command/template/file-reference
  cases listed above plus five prose tokens on `openssf…:3` and three on `first-psirt…:11`; none is a
  map key occurrence. Full census: `ReviewC1Semantics-receipts/context-census.txt`.
- The single filename-class rewrite is `S040.txt` (above); judged accurate.

## S041 exclusion — right, and only nominally ambiguous
The basename is held by three tracked files (`round-26`, `round-28`, `round-30`), so limb M4's
uniqueness rule cannot be met and the builder must exclude; the exclusion list is exactly the six
backticked S041 citations (they are the only backticked S041 citations in the scope).

| token | occurrence | capture it means | evidence |
|---|---|---|---|
| `S041.txt` | `iso-29147-divergence-and-clause-crosswalk.md:64` | **round-26** | same bullet: "capture log in `.ufo/waves/round-26/`; sha256 `e18acbf9…`"; entry `source:` + `recheck:` bind round-26 |
| `S041.txt:1680-1681` | `…crosswalk.md:13` | **round-26** | L1680-1681: "これらの国際標準は…大きな矛盾や不整合はありません。" — supports "no major contradiction (§3)" |
| `S041.txt:1792-1867` | `…crosswalk.md:34` | **round-26** | L1792 "(2) 脆弱性公開ポリシー" … L1867 "（出所：ISO/IEC 29147:2014 を元に作成）" |
| `S041.txt:1868` | `…crosswalk.md:54` | **round-26** | L1868 "P ガイドラインでは、ベンダに脆弱性公開ポリシーの策定を求めていません" |
| `S041.txt:1868-1870` | `…crosswalk.md:13` | **round-26** | L1868-1870 the obligation contrast sentence pair |
| `S041.txt:1996-2079` | `…crosswalk.md:43` | **round-26** | L1996 "参考 1 ISO/IEC 29147:2014 と…ガイドラインの対応" … L2079 "文献目録"; all ≤ 2354 lines |

The three candidate files are **byte-identical** (sha256 `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`
for all three; `cmp` silent, receipt `ReviewC1Semantics-receipts/s041-exclusion.txt`). So the
ambiguity is nominal (which stored copy), not material (which bytes). Per-token the intended capture is
fixed by each citing entry's own header: division-of-labour → round-26, divergence → round-26,
japanese-domestic-disclosure-workflow → round-28, japanese-severity-vocabulary-and-impact-model →
round-30 (the latter two are not backticked, so they were never candidates). The exclusion is correct
as frozen; if a later round amends M4, the per-file header — never a global choice — is the evidence
to use. Receipt: `ReviewC1Semantics-receipts/s041-exclusion.txt`.

## Residual risk and verification gaps
1. **Meter scope is backticked spans only** (`corpus/instruments/resolve.py:102`: `TOKEN` is a regex for one backticked span, `` `([^`\n]+)` ``).
   The 678/1719 reading therefore says nothing about non-backticked citations. In the five touched
   files that is 12 raw occurrences: `openssf…:3` carries five bare citations
   (`S102.txt:13`, `:19-37`, `:93-107`, `:234-244`, `:268-370`) in a line with zero backticks — note
   that `:13` is simultaneously a map key at lines 17/86 and remains bare at line 3 — plus
   `first-psirt…:11` (`S100.txt`, `S101.txt` file references) and the command/template cases above.
   Corpus-wide the same test finds 1401 of 1411 bare-token occurrences outside a citation-style code
   span. Not a defect of this landing (the claim is scoped to the map), but the meter must not be read
   as "all knowledge citations resolve".
2. The six S041 tokens and the four QUOTED tokens remain bare by design; their sentences still read
   correctly (anchors verified above).
3. `MIRROR_ABSENT=True` in this environment: classification has no mirror fallback, so the reading is
   entirely INTERNAL/GONE. That is the environment the claim was frozen against; a mirror present on
   another host could move M1.
4. Continuation anchors (`:463`, `:149`, `:156`, `:417`, `:422`) remain short forms by design; they
   resolve against the full path earlier in the same parenthetical/sentence.
5. The C1 landing commit also carries three wave-scaffold files (`.ufo/waves/round-87/w1-spec.json`,
   `w1-dispatch.json`, `w1/swarm-registry.json`), so frozen predicate P3 is false at `d87b1b5` — already
   recorded in `landing.json` and the L1 receipt; the `corpus/knowledge/` diff itself is limited to the
   five files above. Not re-scored here.
6. I did not run C2, the claim-package gate, or the full `resolve.py` census (out of this seat's scope;
   the knowledge-meter is the designated scope reading).

## Verdict
**APPROVE** — no key to change. Every repointed value names the capture its sentence means and its
anchor supports the sentence; the S041 exclusion is correct per token; no r86 Finding-1 context was
rewritten. The residual items above are qualifiers for the claim's reading and candidates for a future
tranche, not defects of this landing.

Files written:
- `.ufo/waves/round-87/w1/ReviewC1Semantics.md`
- `.ufo/waves/round-87/w1/ReviewC1Semantics-receipts/anchor-table.txt`
- `.ufo/waves/round-87/w1/ReviewC1Semantics-receipts/c1-counter.txt`
- `.ufo/waves/round-87/w1/ReviewC1Semantics-receipts/builder-reproduction.txt`
- `.ufo/waves/round-87/w1/ReviewC1Semantics-receipts/context-census.txt`
- `.ufo/waves/round-87/w1/ReviewC1Semantics-receipts/s041-exclusion.txt`
