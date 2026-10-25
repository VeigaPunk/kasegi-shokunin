# Round 25 wave 2 — do the two F10 entries duplicate ground?

Seat: `L1Kasegi25.C2DuplicateTheme` (simplifier, READ-ONLY). Lane tree as of write time:
`corpus/README.md:211` F10 admitted with two entries; both files untracked; harness
`entries=12 pass=12 exit=0`. No production bytes touched, no tools installed (none needed).

## Verdict

**Falsifiable verdict: NOT duplicates.** Each entry carries checkable surface the other does
not contain, so deleting either loses an exact, enumerable set of claims and registry
bindings — it does not remove a second copy of the same ground. The wave-1 outcome (keep
both, `corpus/lessons/round-25.md:85-88` "Two entries, one theme" with a named split:
four Japanese pages vs Cisco PSIRT crosswalked on eleven dimensions) stands.

The genuine duplication is **narrower than one entry**: 13 verbatim strings and the claims
they support are asserted in both files (listed below). That is a duplicated *claim subset*,
not duplicated *ground*, and it is bound to the same manifest records — measured: 12/12
raw shared strings are manifest `quote` texts (the 13th, `hitachi-29147-2014`, is an
ellipsis-joined composite matched under the entry's declared Q8 normalization). A
capture-byte change fails both rechecks identically, so there is no second-authority drift
risk on the evidence bytes; only the English glosses could drift, and they currently agree.

## Exact lost surfaces if either is deleted (the falsification test)

**Delete `vendor-disclosure-policy-commitments-crosswalk.md` (e2) → lose:**

- Every S040 object: ISO/IEC 29147:**2018** alignment (`e2:45`), investigates-all-reports
  (`e2:46`), LDoS lifecycle boundary (`e2:47`), JP-CERT named coordination partner
  (`e2:48`), default-hold + four expedite conditions (`e2:49-51`), 1600-GMT Wednesday
  disclosure slot (`e2:52`), bounty-terms pointer (`e2:53`). e1 contains zero `cisco`
  matches (`grep -ci cisco` → 0).
- The 11-dimension crosswalk predicate itself (`e2:21-33`): "who owns the disclosure
  clock" — a per-cell checkable table e1 does not contain.
- Falsifiable rules `e2:77-94`: 29147 *edition* divergence (2018 vs 2014), "a Japanese
  vendor policy necessarily names the national coordinator" falsified by S038, money as a
  page-property, the four-expedite-bullet count. e1's FR-1..FR-4 (`e1:163-173`) do not
  assert any of these.
- Registry binding: `SOURCES.md` S040 `used-by` names only e2; deleting e2 leaves a
  `mined` row with no user → census W03 class condition, and harness drops to
  `entries=11 pass=11` (F10 loses a PASS line).

**Delete `vendor-disclosure-policies-as-corpus-objects.md` (e1) → lose:**

- All S037 (bounty-FAQ) objects: account gate, お申し込み form, payment form and the
  resolution-anchored clock, no-verification-on-reporting-site (`e1:73-88`). e2 contains
  zero `S037` matches (`grep -c S037` → 0).
- 17 quote blocks present nowhere in e2, incl. the full intake-channel sentence
  (`e1:23`), package-products disclosure scope (`e1:40`), PSIRT-assigned severity
  confirmation (`e1:56`), the conditioned non-litigation clause with its subject
  (`e1:102`), prohibition item 2 (`e1:116`), the 届出窓口 routing sentence (`e1:128`),
  partnership-since-2004 (`e1:134`), 足並み alignment (`e1:140`).
- FR-1..FR-4 (`e1:163-173`) and the five rejected over-generalizations (`e1:177-199`),
  incl. the `招待`-count 0 falsifier of "invitation-only".
- Registry binding: `SOURCES.md` S037 `used-by` names only e1 → same W03 exposure.

## The actual overlap (measured, enumerated)

13 verbatim strings shared, all Japanese-side: `cybozu-scope`, `cybozu-cloud-mobile-excluded`,
`cybozu-jpcert-date`, `cybozu-cvss`, `cybozu-bounty-intake` (e2:54-58 = e1:36,45,64,53,19-substring),
`pepabo-no-bounty`, `pepabo-safe-harbour`, `pepabo-case-by-case`, `pepabo-prohibited`
(e2:59-62 = e1:108,17-substring,105,24-substring), `hitachi-29147-2014`,
`hitachi-two-principles`, `hitachi-coordination`, `hitachi-cna` (e2:63-66 = e1:146,137,149,152).
The claims they support — Pepabo's no-bounty and conditional protection, Cybozu's
handling-vs-publication scope split and JPCERT/CC-agreed date, Hitachi's two principles and
coordinators — are re-asserted in both files with *no contradictory gloss* found on a
claim-by-claim read (e1 "routes reports to an email address" `e1:180` vs e2 "all reports
go to one internal security team" `e2:24` are consistent, not conflicting).

Structural reason the shared strings cannot be deleted from e2: the crosswalk contract is
"each cell is checkable against the captures" (`e2:19`); removing the Japanese verbatim
column unbinds the cells. They are also required for e2's own recheck coverage of its
`source:` header set (S036/S038/S039/S040, R12 shape, verified `lesson-mistakes.md:241-242`).

## Commands run (all from lane root, read-only)

| command | output | exit |
|---|---|---|
| `ls corpus/knowledge/ \| wc -l` | `37` | 0 |
| `grep -nE '^\| *F10 ' corpus/README.md` | `:211` — row lists both entries, sources S036–S040 | 0 |
| `git ls-files corpus/knowledge/vendor-disclosure-*.md` | empty (both untracked) | 0 |
| `grep -nE '^\| *S0(3[6-9]\|40) ' corpus/SOURCES.md` | rows `:42-:46`; `used-by`: S036/S038/S039→both entries, S037→e1 only, S040→e2 only | 0 |
| `python3 corpus/instruments/frontier-recheck-count.py` | `PASS F10` ×2 … `entries=12 pass=12 exit=0` | 0 |
| C2 counter verbatim (claims.json) | `frontier=10`, `entries-citing=2`, census `ok` + W04×2 (S028/S029, pre-existing) | 0 |
| verbatim-overlap script (re-findall both files) | e2 rows=22: 9 E2ONLY (all Cisco), 13 SHARED; e1 blocks=27: 17 E1ONLY | 0 |
| manifest coverage script | 12/12 shared raw strings are manifest `quote` texts; manifest 5 records/39 quotes | 0 |
| `grep -c` cross-references | e1→e2 name: 0; e2→e1 name: 0; e1 `cisco`: 0; e2 `S037`: 0 | 1 (no match) |

## Axes

- **coverage**: keeping both is required — S037 and S040 each have exactly one citing
  entry; deletion of either orphans a `mined` row (W03 class) and drops a harness PASS line.
- **depth:verifiability**: shared claims are fail-closed bound to the same manifest
  assertions; two recheck lines over the same bytes is redundancy without drift surface.
- **weight**: the duplicated subset is 13 strings/~13 re-asserted claims, structurally
  required by the crosswalk's per-cell contract — not a second authority.

## Smallest correction if a reviewer wants the residual tidied (NOT required)

The duplicated claim subset has no declared owner. If a future wave wants it explicit:
add one line to each entry naming the other as the sibling authority on the shared
Japanese quotes (currently `grep -c` cross-references = 0 both ways). This is cosmetic —
no falsifiable claim fails without it. No production edit made or recommended this wave.

## Report trailer

- scope: read-only; no files changed; no installs.
- wave-1 receipts read: `claims.json`, `wave1/SimplifierScope.md` (recommended folding e2
  into e1 — superseded by the landed two-entry row), `wave1/lesson-mistakes.md:234-248`
  (the "L1 must decide" flag), `wave1/EntryJapanVendors.md`, `wave1/EntryCiscoCrosswalk.md`
  (headers), `corpus/lessons/round-25.md:76-131` (the landed decision).
- tool install/update record: none — stock `bash`/`python3`/`grep`/`awk` sufficed.
