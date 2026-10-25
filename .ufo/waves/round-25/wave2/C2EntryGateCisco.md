# C2EntryGateCisco — wave 2 falsification review of the wave-1 Cisco crosswalk

Seat: `L1Kasegi25.C2EntryGateCisco`. Lane: kasegi-shokunin. Scope: falsify the wave-1
`EntryCiscoCrosswalk` artifact (Q1-Q6/Q9 = the QUALITY entry-bar gates; "eleven-dimension
comparison" = the crosswalk matrix) against the committed captures. Read-only review; no
production edit, no VCS write. Report trailer relative to
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` (Lane root). Reference file:
`corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` (the entry), `corpus/QUALITY.md`
(Q1-Q9 definitions), `corpus/source-snapshots/round-25/{S036,S038,S039,S040}.txt` (captures),
`corpus/source-snapshots/round-25/manifest.json` (record binding), `.ufo/waves/round-25/wave1/EntryCiscoCrosswalk.md`
(wave-1 receipt).

## Verdict

**The wave-1 result stands: the Cisco crosswalk Q1-Q6/Q9 entry is not falsified on any measured
assertion I could attack.** Every verbatim quote occurs exactly once in its capture (21/22 raw,
1/22 under the declared whitespace normalization), the recheck line is live and cwd-independent,
the manifest binds the S040 quote ids, the 11-dimension matrix answers match the capture bytes,
and the four falsifiable rules' substantive claims (edition split, coordinator naming, money
states, four expedite bullets) reproduce. **One internal defect is real but does not kill the
entry: rule 4's cited line ranges for bullets 2-3 are off by one against the capture** (and
against the entry's own matrix cell and the JSON record). I also note a second, weaker
imprecision in the "published schedule" column for S036 (an agreed JPCERT/CC publication date
exists at S036 L44 but the cell says "none stated"). Both are smallest-safe-corrections below;
neither invalidates the entry's claims, the 37-line recheck, or the C2 claim.

## Evidence

### 1. Entry bar Q1-Q6/Q9 against the artifact

Q1 (header): header block L2-L7 = H1 (L1), four `source:` (L2-L5), `verified-at:` (L6),
`recheck:` (L7) — the `recheck:` line is a single executable command with `cd <lane-root> &&`
prefix; `bash -n` passes. Verified: `bash -n -c "$(sed -n '7p' <entry>)"` → exit 0.

Q2 (load-bearing claims rest on tier-A rows opened this round): `corpus/SOURCES.md` rows L42-L46
register S036/S037/S038/S039/S040 as tier A `docs` in this round; the entry cites all four.
Verified by reading SOURCES.md (see appendix command 8).

Q3 (verbatim quote ≤25 words + exact location): all 22 quote strings are literal substrings of
their captures, each at the cited line (one wrapped-across-lines case declared). Word counts:
max English quote is `cisco-iso-29147-2018` at 22 words; the Japanese quotes are single
whitespace-tokens by the capture's convention (declared in the entry's quoted-record preamble),
consistent with how every Japanese row is attributed in the same matrix. Exact-location check per
quote: see appendix command 4 (22/22 parsed; 21/22 exact-line containment, the one exception
`cisco-jpcert-partner` is documented as wrapped L188-L189 and its JSON record and manifest id
both carry the wrap note).

Q4 (attribution kept): each quote row is attributed to its vendor id (S040/S036/S038/S039) with
its own capture; no universal generalization is attributed across pages; the two rejected
over-generalizations are attributed to the sample ("these four pages").

Q5 (falsifiable rule + rejected over-generalization): rules 1-4 and two rejections present
(entry L75-L108), each rule names a checkable command. Rules 1, 2, 3 reproduced; rule 4's
*count* reproduced but its cited line ranges are off by one (defect 1 below).

Q6 (documentation-only): no probing/scanning/submitting instructions, no credentials, no live
URL as an instruction; the only live-URL text is the descriptive capture record and the stale
`verified-at`/recheck text. The `recheck:` line reads local capture bytes only.

Q9 (captured-source assertion binding): (a) manifest record `path` stem `S040.txt` = id `S040`
— holds; (b) the quote is exactly-once in the capture or carries an `anchor` the instrument
verifies — all S040 quotes report `occurrences=1` (the wrapped quote under `normalized=markup-whitespace`);
(c) the check prints the occurrence count — it does (`occurrences=N` per line). Q9 passes.

### 2. The eleven-dimension comparison — cell-by-cell attack

Matrix rows (entry L21-L33) attacked against capture bytes:

| dimension | verdict |
|---|---|
| explicit scope list | PASS (S040 L200/L218-L234 verified; S036 L14-L15/L27-L30 verified; S038 L17 verified; S039 L491 verified) |
| process commitment | PASS (S040 L162; S036 L16-L25; S038 L16; S039 L497-L499) |
| named standard + edition | PASS — S040 `29147` ×1 at L58; S036 ×0; S038 ×0; S039 ×8 (L497/L499/L612/L613/L615/L621... 2014+2018 links) |
| named coordination partner | PASS (S040 L187-L190; S036 L44; S038 `JPCERT`=0 `CERT/CC`=0; S039 L510/L512/L520/L533) |
| severity instrument | PASS (S040 CVSS v3.1 L245-L249 + SIR L254-L259; S036 L22 + L49-L51; S038 CVSS=0; S039 CVSS=0) |
| stated conditions for going faster | PASS for the four-bullet count (L301/L302-L304/L305-L308/L309); **minor framing imprecision** in the row name vs S036/S039 cells (see defect 2b) |
| published schedule | PASS for S040 (L319-L320, L321-L331, L334-L341); **S036 "none stated" is imprecise** — S036 L44 records a publication date agreed with JPCERT/CC (defect 2a) |
| lifecycle boundary | PASS (S040 L456 "FCS to LDoS", L482-L484 past-LDoS; S036/S038/S039 none stated) |
| money | PASS (S040 L487-L489; S036 L19; S038 L20; S039 `報奨金`=0) |
| reporter-facing duty | PASS (S040 L180-L182; S038 L23-L25; S036/S039 none stated) |
| reserved definition | PASS (S040 L66-L68) |

### 3. Falsifiable rules — command outputs

Rule 1: `for f in S036 S038 S039 S040; do printf '%s %s\n' "$f" "$(grep -c 29147 corpus/source-snapshots/round-25/$f.txt)"; done`
→ `S036 0 / S038 0 / S039 8 / S040 1` (matches the entry's predicted output exactly).

Rule 2: `grep -c JPCERT` / `grep -c CERT/CC` per capture → S036 1/1, S038 0/0, S039 2/7,
S040 0/2; `grep -c JP-CERT` → S040 1. S038 names no coordinator — holds.

Rule 3: `grep -c '報奨金'` → S039 0; S036 L19 names 脆弱性報奨金制度; S038 L20 states no scheme;
S040 L487-L489 names bounty programmes with terms on a separate page — holds.

Rule 4: capture L300-L309 carries exactly four bullets — holds. **But the entry's cited ranges
are wrong** (defect 1).

### 4. The recheck line — full 37-Ok line run

```
$ ( cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S040 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S036 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S038 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S039 ) | tee /tmp/recheck4.out | wc -l
37
$ grep -c OK /tmp/recheck4.out
37
$ grep -v OK /tmp/recheck4.out   # (empty)
```

All four `sha256 OK` + 33 quote assertions OK (S040 9, S036 8, S038 7, S039 9). S040's
`cisco-jpcert-partner` passes under `normalized=markup-whitespace occurrences=1`. Exit 0 from
lane root. `S040:sha256 OK` matches `sha256=b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c`
in `capture-log.txt` L14 and in the manifest record.

### 5. Manifest binding

The manifest's S040 record carries the same nine quote ids as the JSON `quotes-vendor-cisco.json`
record. The Japanese ids Q1-Q8/Q9 exist in the manifest; each entry quote string maps to exactly
one manifest id (verified programmatically: cybozu-scope→Q2, cybozu-cloud-mobile-excluded→Q4,
cybozu-jpcert-date→Q7, cybozu-cvss→Q5, cybozu-bounty-intake→Q8, pepabo-no-bounty→Q3,
pepabo-safe-harbour→Q6, pepabo-case-by-case→Q2, pepabo-prohibited→Q7). S040's nine quote strings
are the entry's own ids, matching the quoted-record table. No assertion lost coverage.

### 6. Falsification attempts that failed (strongest counterexamples tried)

- **"Rule 4 says two conditions in the staged text"**: the staged `vendor-cvd-policy-crosswalk-2026-10-23.md`
  does claim "two conditions" (L31-L34); the wave-1 entry supersedes it with four bullets and
  states the correction in its re-grounding note (L110-L116). The wave-1 *entry* is correct; the
  staged text (a different artifact, not the entry) is the one falsified. No entry defect.
- **"Quotes are paraphrases, not verbatim"**: all 22 quote strings are byte-substrings of the
  captures (verified by `grep -c -F` per quote, 21 raw 1; the wrapped JP-CERT quote is declared
  and instrument-checked under normalization). No fabrication.
- **"JP-CERT appears only once; the paragraph has five names"**: verified L185-L193 has exactly
  the four names CERT/CC, CERT-FI, JP-CERT, NPSA. No fifth.
- **"S039 has a lifecycle boundary"**: tried `grep -n 'ライフ\|EOL\|サポート終了'` → no hits.
  "None stated" holds.
- **"S039 has a severity instrument"**: tried `grep -n '深刻度\|重要度\|CVSS'` → no hits.
  "None stated" holds.
- **"S040 has no schedule"**: verified L319-L320 (1600 GMT Wednesday), L321-L331 (twice-yearly
  bundles), L334-L341 (out-of-cycle list). Holds.
- **"LDoS quote is missing"**: verified L482 "will continue to accept vulnerability reports" and
  L483 "not analyze, fix, or disclose potential vulnerabilities" — the entry's lifecycle cell
  matches.
- **"Money state differs"**: verified each page's own words (S040 names programmes, no amount; S036
  names scheme; S038 states none; S039 never mentions). Holds.
- **"Q1 header format deviates"**: the entry has repeated `source:` lines for four sources. This
  is a stated deviation in the wave-1 receipt (L52-L56), the `frontier-recheck-count.py` limb-A
  requirement, and the C2 claim expects ≥1 new source. Not a defect.

## Defects found (smallest safe corrections)

**Defect 1 — rule 4 line ranges off by one (entry L92-L93).** The capture shows bullet 2
(active exploitation) spans L302-L304 and bullet 3 (public awareness) spans L305-L308. The
entry's rule 4 text says "observed active exploitation (L302-L305)" and "potential for increased
public awareness (L306-L308)". This is contradicted by the entry's own matrix cell (L28 cites
L302-L304, L305-L308), its own JSON record (`cisco-active-exploitation … (L302-L304)`), and the
SOURCES.md row for S040 (which cites L301/L302/L305/L309 — correct). Line L305 is the *first*
line of bullet 3, not the last of bullet 2. **Smallest correction:** in the entry, change rule
4's ranges from `(L302-L305)/(L306-L308)` to `(L302-L304)/(L305-L308)` (two number spans). This
is a line-pointer fix, not a claim fix; the count and the bullets themselves are correct.

**Defect 2a — S036 "published schedule: none stated" is imprecise (entry L29).** S036 L44
("情報公開は公表日一致の原則に従い、JPCERT/CC と取り決めた日に合わせて公開します。") is a
publication-date commitment — a negotiated, non-calendared date. The entry's Own S036 faster-
conditions cell cites exactly this L44, while the schedule cell says "none stated". The "none
stated" is the most defensible reading (no fixed date/slot), but the entry should point to L44
here too (or say "no calendared date; publication waits on a JPCERT/CC-agreed date (L44)").
The same cell in S039 already does the analogue ("the date is negotiated, not calendared").
**Smallest correction:** adjust the S036 schedule cell to reference L44 with the negotiated-date
wording, mirroring S039.

**Defect 2b — matrix header "stated conditions for going faster" does not match S036/S039
cells (entry L21, L28).** The cells for S036/S039 contain *publication-timing principles* (公表日
一致の原則, fixes-ready-at-publication), not faster-disclosure conditions; Cisco's four bullets are
the only true "expedite" content. The comparison is accurate but the row name over-generates.
**Smallest correction:** rename the row "disclosure-timing commitments (incl. any expedite
conditions)" or add a parenthetical "Cisco: conditions to go faster; others: timing principles".
No data change.

## Commands / outputs / exits

All commands run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (lane root) unless noted.

1. `bash -n -c "$(sed -n '7p' <entry>)"; echo $?` → `0`.
2. `for f in S036 S038 S039 S040; do printf '%s %s\n' "$f" "$(grep -c 29147 corpus/source-snapshots/round-25/$f.txt)"; done` → the exact predicted rule-1 output.
3. `grep -c '報奨金' corpus/source-snapshots/round-25/S039.txt` → `0`.
4. Quote verification script (python3, read-only; writes nothing) — parsed all 22 quote rows from the entry, ran `grep -c -F` raw and normalized, checked quote containment on the cited line: 21/22 exact-line, 1/22 declared wrapped (L188-L189). Full table in the wave-1 receipt reproduced identically.
5. `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S040` → 10 lines (`sha256 OK` + 9 `OK occurrences=1`), exit 0.
6. Full four-source recheck (appendix §4) → 37 lines, 37 OK, exit 0; `wc -l` = `37`.
7. `grep -nP '\x{FFFD}' corpus/source-snapshots/round-25/S040.txt` → L108, L193, L203, L222, L479 (matches the entry's limits note). `grep -nP '\x{202F}'` → L97, L145, L163, L186-L190, L199, L201, L203-L204, L236-L237, L243, L245-L246, L294, L313-L314, L367, L378, L381, L385-L386, L456, L468-L469, L473, L477-L479, L488. No quote crosses either.
8. `grep -n 'S036\|S037\|S038\|S039\|S040' corpus/SOURCES.md` → rows L42-L46 (tier A, all docs, opened this round).
9. `grep -n 'S040' .ufo/waves/round-25/capture-log.txt` → L14 `status=200 fetched_bytes=94027 snapshot_bytes=33463 sha256=b7f7b55… utc=2026-10-25T08:14:28Z`; L25 `| S040 | Cisco Security Vulnerability Policy | … | S068 |` (the staged-id alias, as the entry's finding 2 says).
10. `wc -l corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` → `133` (receipt says 133; the embedded `wc` snippet says 130 — the snippet is stale, but the report's own Behavior and Touched-surfaces tables say 133; no inconsistency in the artifact proper).

No tool installs or upgrades were made (no packages, no uv/npx/cargo/npm channels used); the
tooling-directive record is therefore "none owed".

## Impacted axes

`coverage` (C2): the artifact and its recheck hold under attack, so the F10 claim's evidence
framework is intact. `depth:verifiability` (C1): the entry's line-7 recheck passes the frozen
instrument (37/37 with the sibling entry); the two defects are documentation-level line-pointer
imprecisions and do not change any instrument verdict. If the wave-1 receipt is re-read after a
fix, only the two numbers in rule 4 change.

## Smallest safe corrections (no production edit performed)

1. Entry rule 4 (L92-L93): `(L302-L305)/(L306-L308)` → `(L302-L304)/(L305-L308)`.
2. Entry matrix S036 schedule cell (L29): add L44 reference with "negotiated date" wording.
3. Entry matrix row header (L21): rename to cover timing principles, or add parenthetical.
