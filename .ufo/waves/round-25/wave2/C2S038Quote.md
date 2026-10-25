# C2S038Quote — S038 legal-action quote: subject present, no safe-harbour overclaim?

Seat: `L1Kasegi25.C2S038Quote` (read-only wave-2 falsifier).
Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, worktree at wave-1 tip (round-25 files are
untracked: `git status --porcelain` shows `?? corpus/source-snapshots/round-25/`,
`?? corpus/knowledge/vendor-disclosure-*.md`; last commit is `b49948f`, untouched).
Target: re-open S038; verify (a) the legal-action quote includes its subject, (b) no safe-harbour
overclaim in committed wave-1 text.

## Verdict

**UPHELD — the wave-1 repair is real and the two named concerns are cleared in committed text, with
one minor residual (M2) and one informational note (M1).** The wave-1 result is not wrong about the
quote; the canonical legal-action quote is the whole conditional sentence. Falsifiable form:

- F1 (subject): the S038 legal-action quote committed to `manifest.json` and to
  `vendor-disclosure-policies-as-corpus-objects.md` contains `当社システムへの侵入または侵入の試みが` —
  **TRUE (verified, command C1/C2 below)**. Falsifier: remove that substring from the committed quote
  and `source-recheck.py` still exits 0 → verdict flips to WRONG.
- F2 (no overclaim): no committed corpus text asserts the S038 policy grants authorisation or safe
  harbour for testing; the sole `safe-harbour` token on an S038 line is a quote-id label —
  **TRUE (command C4)**. Falsifier: a grep hit on committed corpus text asserting the grant → flips.
- F3 (residual): committed text at two spots asserts the non-litigation statement is conditioned on
  the *two-item prohibition list*; the capture carries no enumerated 条件 list — **TRUE (C5/C6)**, the
  wave-1 authority `RevQuotesJP.md` U1 (binding: "may **not** enumerate or characterise those
  conditions") bars exactly this. Severity minor: it adds, not over-claims — it makes the waiver
  *narrower and checkable* rather than broader.

## Commands, outputs, exits

C1 — capture line of record:

```
$ sed -n '17p' corpus/source-snapshots/round-25/S038.txt
また、当社システムへの侵入または侵入の試みが以下に示す条件を守る限りにおいて、セキュリティ研究者に対して、法的措置をとらない方針です。
$ grep -n '条件\|守る' corpus/source-snapshots/round-25/S038.txt
17:また、当社システムへの侵入または侵入の試みが以下に示す条件を守る限りにおいて、…
exit=0 (only occurrence of 条件 in the 77-line capture)
```

C2 — manifest verification, all S038 assertions:

```
$ python3 corpus/instruments/source-recheck.py --manifest \
    corpus/source-snapshots/round-25/manifest.json --source S038
S038:sha256 OK
S038:Q1 OK occurrences=1
S038:Q2 OK occurrences=1
S038:Q3 OK occurrences=1
S038:Q4 OK occurrences=1
S038:Q5 OK occurrences=1
S038:Q6 OK occurrences=1
S038:Q7 OK occurrences=1
EXIT=0
```

Q1 is the whole sentence (subject + 限り conditional); Q6 is its subjectless tail — see M1.
sha256 `09e077d3…` matches `wave1/RevQuotesJP.md:17` and `corpus/lessons/round-25.md:107`.

C3 — committed quote occurrences:

```
corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:102  → Q1 verbatim + annotation
  "(quoted whole: the fragment omits the subject, 当社システムへの侵入または侵入の試みが)"  (:103)
corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:60 → `pepabo-safe-harbour` row,
  quote = Q6 fragment only, cited "L17, 脆弱性報告制度 opening"
corpus/lessons/round-25.md:107                                        → Q1 verbatim, "located quote" col
corpus/source-snapshots/round-25/manifest.json:90-97                  → S038 record, Q1 = whole sentence
```

C4 — safe-harbour overclaim grep over committed corpus text:

```
$ grep -rn 'safe.harbour\|safe.harbor' corpus/knowledge/vendor-disclosure-*.md \
    corpus/SOURCES.md corpus/lessons/round-25.md
corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:188:
  3. **"A published non-litigation policy grants safe harbour for testing."** Rejected.
corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:60: `pepabo-safe-harbour` (id label)
corpus/SOURCES.md: other hits are S006/S007/S008/S028/S032 rows, none S038
```

The staged row's overclaim — `wave1/RevSourceRows.md` D4: `scope` read "legal safe-harbour for
authorised testing" (A7 class, `corpus/QUALITY.md:17`) — did **not** land. Committed
`corpus/SOURCES.md:44` cell 5 now reads "A Japanese vendor's published **no-legal-action** undertaking
for researchers who keep to its stated conditions, the two acts it forbids even for verification, and
the absence of any bounty"; entry A's Rejected-over-generalization #3 (`:188-191`) explicitly refuses
the authorisation reading; crosswalk prose (`:16`) says Pepabo "binds itself to a legal posture" and
the reporter-facing-duty cell (`:32`) lists the prohibitions as prohibitions.

## Findings

**M1 (informational) — a second, subjectless form of the legal-action quote is also committed.**
`vendor-disclosure-policy-commitments-crosswalk.md:60` quotes `pepabo-safe-harbour` as
`セキュリティ研究者に対して、法的措置をとらない方針です。` (= manifest S038 Q6), the exact fragment the L1
widening repudiated. Mitigation, all inside the same file: location cites L17 (`:60`), the scope cell
names the subject `当社システム` (`:23`), and the claim prose frames a posture not a grant (`:16`). The
entry's own preamble (`:39-41`) openly binds `pepabo-safe-harbour` → manifest Q6 as a "substring of Q1"
record, so the truncation is declared, not hidden. Standalone the fragment still carries no subject
and no conditionality — if the ticket's "includes its subject" applies to *every* committed form of
the quote, the smallest correction is to swap that row's verbatim for Q1 (or relabel the id, e.g.
`pepabo-non-litigation`, since "safe-harbour" is also stronger than 方針).

**M2 (minor defect) — committed prose conditions the waiver on the prohibition list; U1 forbids it.**
`RevQuotesJP.md:33` (binding U1): `以下に示す条件` "is never expanded" by the capture; an entry "may
**not** enumerate or characterise those conditions" (the L23-25 list is headed `禁止いたします` —
prohibited acts, not the 条件). Two committed texts do exactly that:

- `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:121`:
  "the non-litigation statement is conditional **on the two listed prohibitions**" (reinforced by
  FR-3 at `:169-170`, "falsified by the condition clause at S038.txt:17 and the two prohibited acts",
  though FR-3 itself is defensible since it keeps clause and list as separate limbs).
- `corpus/lessons/round-25.md:124`: "S038's protection is conditioned on the *published prohibition
  list*".

Receipt disagreement: `wave1/RevSourceRows.md:138-139` made the same equation ("prohibited acts at
lines 23–25" named as the stated conditions), so wave 1 left the question split and the committed text
took the U1-barred side. The reading is *plausible* (the prohibition list is the only list below L17)
but it is an inference, and U1 drew the binding line. Smallest correction, no surgery to quotes:

- entry `:121` → "…decided separately, and the non-litigation statement is conditional on compliance
  with conditions the page references but does not enumerate; the page separately prohibits DoS-class
  verification and access beyond one's own account (:24-25)."
- `lessons/round-25.md:124` → "…and S038's protection is conditioned on an *unexpanded* `以下に示す条件`,
  with a prohibition list published beside it."

Note the residual is the inverse of an overclaim: it over-specifies the waiver's bound, which cannot
read as a testing grant.

**N1 (note, not a defect) — `现在` dropped once.** Entry A `:179` says "no reward at all"; the page's
`現在` ("currently") qualifier was the point of `RevSourceRows.md` P2. `SOURCES.md:44` cell 7 still
carries "at all" — staged P2 unapplied — but both are precision items, not safe-harbour items; the
`no-legal-action` limb is intact in both.

## Wave-1 result adjudication

- `wave1/EntryJapanVendors.md:25-28,100` records the L1 widening Q1 "from the conditional fragment to
  the whole sentence" and re-verifying 30/30 quotes exactly-once — **confirmed** (C2; Q1 = whole
  sentence at `manifest.json:94-97`, entry `:102`).
- `wave1/RevQuotesJP.md:75` supported-verdict on the L17 quote ("yes (policy only)") — **confirmed**;
  the quote is verbatim at `S038.txt:17`.
- `wave1/RevSourceRows.md` D4 violation + corrected cell — **confirmed applied** in
  `corpus/SOURCES.md:44` cell 5.
- `wave1/RevQuotesJP.md` U1 — **violated** by entry `:121` and lessons `:124` (M2 above).

## Residual risk / verification gaps

- I did not re-fetch `https://pepabo.com/contact/vulnerability-reporting/`; fidelity to the live page
  rests on the pinned capture (`capture-log.txt`, sha256 match C2) — same limit the wave-1 seats
  recorded.
- The U1-vs-D4 disagreement is settled here by U1's explicit "binding limit" language (`RevQuotesJP.md:140`
  says the U-table is binding if a scribe phrases differently), but a dissenting read — the prohibition
  list *is* the referent of `以下に示す条件` — is textually arguable and is the one the corpus now carries.
- Crosswalk L17 citation for the Q6 fragment is honest but a reader of the quote table alone sees an
  unconditional-sounding sentence (M1).
- No installs or updates performed; read-only seat, nothing to record for tooling.

Report: `.ufo/waves/round-25/wave2/C2S038Quote.md`
