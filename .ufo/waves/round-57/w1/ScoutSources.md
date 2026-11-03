VERDICT: AGREE — 14/14 quotes and 28/28 publisher facts reproduce from an independent re-open; both lane recheck runs exit 0; no claim-killing disagreement found.

DETAIL: S089 and S090 were re-fetched with an independent UA (HTTP 200, 88964 / 87845 bytes — byte counts equal to the manifest), converted with a different method (stdlib html.parser), and every pinned quote and publisher fact was re-tested against that text. The committed snapshots are byte-identical to MY fetch run through the LANE conversion (sha256 17ee9c41.../2074d3a1... reproduced exactly), so no content was edited in transit. My independent conversion differs by exactly -21 bytes per source, and every byte of that difference is (a) one HTML-comment remnant "Google Consent Mode + Matomo TM -->" the lane regex leaves in and (b) 16 newlines my parser emits where the lane conversion glues adjacent nav labels. Zero normative/abstract/metadata bytes differ. Anchor line numbers therefore drift by +4 in an independently produced text — the pins are snapshot-relative by design, so this is a portability limit, not a correctness failure.

Seat: ScoutSources (r57 w1, kasegi lane). Role: independent verifier, not author.
Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin (read-only). Scratch: /fast/scratch/hyaku/kasegi-r57/ScoutSources (deleted before yield).
Wave evidence dir: /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-57/w1/ScoutSources/
Lane HEAD at read time: cd3029876eac7189aaff0d32b26031c0defa35aa (claims freeze rev eae1d614542e8d30d77e9f4e8b9dea6a11aad138).

Tooling installed/upgraded: NONE (used the host curl 8.23.0 and python3 3.14.8 already present; no pacman, no uv, no ~/.local/bin writes).

=====================================================================
1. FETCH — two URLs, one open each, independent UA
=====================================================================

Command (loop shown collapsed; each id run once):
  S=/fast/scratch/hyaku/kasegi-r57/ScoutSources
  code=$(curl -sS -L --max-time 60 \
    -A 'kasegi-research-verifier/1.0 (independent re-open; contact: operator)' \
    -o "$S/$id.raw.html" -w '%{http_code} %{size_download} %{url_effective}' "$url")

Printed output:
  S089 EXIT=0 CURL=200 88964 https://www.iso.org/standard/72311.html
  S090 EXIT=0 CURL=200 87845 https://www.iso.org/standard/69725.html
  exit code: 0 (both)

  wc -c:
    88964 /fast/scratch/.../S089.raw.html
    87845 /fast/scratch/.../S090.raw.html
  sha256sum of RAW BYTES (mine):
    55a958b3f6beb543f5809a83f9f538febd4a760c5175b68230f86a0dcffaf922  S089.raw.html
    b87acacf0abc1b1909b2cf29dca73a736802575a340d44668fe6de0bf0366e02  S090.raw.html
  exit code: 0

Byte counts equal the manifest's `bytes` field exactly (S089 88964, S090 87845 —
corpus/source-snapshots/round-57/manifest.json:14 and :31 region), which is evidence
the publisher served the same document body to a different UA 2 h after the recorded open
(fetched_utc 2026-11-03T18:04:24Z; my files mtime 2026-11-03 15:24:23 -0300 = 18:24:23Z).

=====================================================================
2. INDEPENDENT CONVERSION — Python stdlib html.parser
=====================================================================

Method deliberately differs from the lane instrument (corpus/instruments/capture-source.py:48-53,
which regex-strips <script|style>, rewrites </p|div|li|tr|h*> to newlines, strips all tags,
html.unescape()s, then collapses). Mine streams a parsing tag machine:
convert_charrefs=True, SKIP={script,style} suppressed by depth counter, BLOCK set emits a
newline on open AND close, void elements ignored, then per-line " ".join(split()) collapse.

Converter: $S/indep_convert.py (sha256 16b9a5bd46bdafeddc26224c6413fbdbc0ddf73e1765a58fb993faab75a3abdb)

Command:
  for id in S089 S090; do TMPDIR=$S python3 "$S/indep_convert.py" "$S/$id.raw.html" "$S/$id.independent.txt"; done
Printed: (6626, 283) then (5577, 276)   [bytes, lines]   exit 0

Independent text sha256 / bytes / lines:
  27d8a769e55cf3e74b6ce07a1d11c6bce257b015de71b1b3f32847e0cf5c84cb  S089.independent.txt  6626 B  283 lines
  e7233ccdcab01235794cfa938d173d83013ce317a5ef4f377ea38c874e0f028f  S090.independent.txt  5577 B  276 lines
  exit code: 0

THE THREE sha256 SETS

  (a) my raw HTML (independent fetch, independent UA)
      S089 55a958b3f6beb543f5809a83f9f538febd4a760c5175b68230f86a0dcffaf922  88964 B
      S090 b87acacf0abc1b1909b2cf29dca73a736802575a340d44668fe6de0bf0366e02  87845 B
  (b) committed snapshot (lane conversion of the lane fetch)
      S089 17ee9c4191ca2261fbb40a6109c6013677adc4ff7522fff079964f72ebb0e1dd  6647 B  268 lines
      S090 2074d3a1b89fe858e607db8cb6109ee869932a12ea14050ad4276084a6c2976a  5598 B  261 lines
  (c) my independent text (html.parser)
      S089 27d8a769e55cf3e74b6ce07a1d11c6bce257b015de71b1b3f32847e0cf5c84cb  6626 B  283 lines
      S090 e7233ccdcab01235794cfa938d173d83013ce317a5ef4f377ea38c874e0f028f  5577 B  276 lines

  (b) matches the manifest pins exactly: sha256/bytes/lines for both sources
  (manifest.json source records; wc -c -l exit 0).

TRANSITIVE CHECK — is the committed snapshot really my fetch, converted by the lane?
Command: import capture-source.py read-only and call its own html_to_text() on MY raw bytes
  python3 "$S/laneconv.py"     (importlib load of corpus/instruments/capture-source.py, unmodified)
Printed:
  S089 lane_conv_bytes=6647 committed_bytes=6647 identical=True  lane_conv_sha=17ee9c41...e1dd
  S090 lane_conv_bytes=5598 committed_bytes=5598 identical=True  lane_conv_sha=2074d3a1...976a
  exit 0
=> The committed snapshots are byte-for-byte reproducible from an independent fetch
   (same raw byte count, same lane conversion). No content was edited in transit.

=====================================================================
3. PER-QUOTE TABLE — 14 assertions vs MY independent text
=====================================================================

Command: python3 "$S/quotetest.py"   (normalize = " ".join(split()); counts both
normalized-substring and raw-substring occurrences)   exit code: 0

S089 (7 assertions)   occ_norm / occ_raw / committed anchor
  Q1 ISO/IEC 29147:2018 - Information technology — Security techniques — Vulnerability disclosure   1/1   1
  Q2 This document provides requirements and recommendations to vendors on the disclosure of
     vulnerabilities in products and services.                                                     1/1   84
  Q3 Other related activities that take place between receiving and disclosing vulnerability
     reports are described in ISO/IEC 30111.                                                       1/1   91
  Q4 This document is applicable to vendors who choose to practice vulnerability disclosure to
     reduce risk to users of vendors' products and services.                                       1/1   92
  Q5 International Standard to be revised [90.92]                                                  1/1   99
  Q6 This publication was last reviewed and confirmed in 2024.                                     1/1   64
  Q7 ISO/IEC AWI 29147                                                                             1/1   204

S090 (7 assertions)
  Q1 ISO/IEC 30111:2019 - Information technology — Security techniques — Vulnerability handling
     processes                                                                                     1/1   1
  Q2 This document provides requirements and recommendations for how to process and remediate
     reported potential vulnerabilities in a product or service.                                  1/1   84
  Q3 This document is applicable to vendors involved in handling vulnerabilities.                 1/1   85
  Q4 International Standard to be revised [90.92]                                                  1/1   92
  Q5 This publication was last reviewed and confirmed in 2025.                                     1/1   64
  Q6 ISO/IEC WD 30111.2                                                                            1/1   197
  Q7 A standard is reviewed every 5 years                                                          1/1   109

Result: 14/14 quotes AGREE, each occurring exactly once; no mismatch to explain.
Em-dash (U+2014) in Q1 of both sources survives my conversion unchanged, so the
quote is not an artifact of the lane's html.unescape() step.

LINE NUMBERS IN MY TEXT (delta vs committed anchors) — python3 "$S/linefind.py":
  S089  Q1 indep:1 (Δ0)   Q2 :88   Q3 :95   Q4 :96   Q5 :103  Q6 :68    Q7 :208   (Δ+4 each)
  S090  Q1 indep:1 (Δ0)   Q2 :88   Q3 :89   Q4 :96   Q5 :68    Q6 :201   Q7 :113   (Δ+4 each)
  exit 0.  The +4 is entirely the parser splitting four nav labels that the lane
  conversion glues onto one line (before the abstract: "SectorsHealth",
  "Insights & newsInsightsAll insights", "NewsExpert talk", "ResourcesISO 9001 explained").
  Declared anchors are snapshot-relative by design (source-recheck.py:anchor_verdict
  builds its window from the snapshot's own raw_lines), so this is a portability
  limit, not a defect in the pin. See §8.

=====================================================================
4. EXACT DIFFERENCE ACCOUNTING — committed vs independent text
=====================================================================

Command: python3 "$S/accounting2.py" (difflib.SequenceMatcher, char level)  exit 0
  S089 committed=6608 indep=6587  deleted_chars=37 inserted_chars=16  net=-21
       del ops: ['\nGoogle Consent Mode + Matomo TM -->']
       rep ops: [(' ', '\n')]
       insert count: 15, all '\n'
  S090 committed=5571 indep=5550  deleted_chars=37 inserted_chars=16  net=-21
       del ops: ['\nGoogle Consent Mode + Matomo TM -->']
       rep ops: [(' ', '\n')]
       insert count: 15, all '\n'

Line-level enumeration (difflib on splitlines, python3 one-liner) — every non-equal op is one of:
  * S089 committed:2 deleted ('Google Consent Mode + Matomo TM -->') — same at S090 committed:2
  * 15 "replace" ops, each a glued pair of nav/footer labels in committed that my parser
    splits into two or three lines: SectorsHealth; Insights & newsInsightsAll insights (x2);
    NewsExpert talk (x2); ResourcesISO 9001 explained (x2); StandardsBenefits; About ISOWhat
    we do; Taking partWho develops standards; ResourcesDirectives and Policies; StoreStore;
    Sign up for email updates.  These are all inside <a>/<li> header+footer chrome.
  Long-line sequence (lines >60 chars) identical=True, S089 n=15/15, S090 n=9/9
  (python3 "$S/tokens.py", exit 0) — i.e. every prose/metadata line matches in order.

Token multiset after dropping the comment fragment (same run):
  S089 only-committed {SectorsHealth:2, newsInsightsAll:2, NewsExpert:2, ResourcesISO:2,
       StandardsBenefits:1, ISOWhat:1, partWho:1, ResourcesDirectives:1, StoreStore:1}
       only-indep {ISO:3, Standards:1, Sectors:2, Health:2, Insights:2, news:2, All:2, News:2,
       Expert:2, Resources:3, part:1, Store:2, Benefits:1, What:1, Who:1, Directives:1}
  S090 — identical pair of sets.  Decomposing the only-committed strings yields exactly
       the words in only-indep, so ZERO content words are missing from either side.

WHY THE COMMENT LEAKS (lane-side quirk, disclosed for the record; not a claim defect):
  raw contains   </script>\n\n<!-- Bridge: Usercentrics consent_status -> Google Consent Mode + Matomo TM -->\n<script>
  SCRIPT_RE (capture-source.py:44, `<(script|style)\\b.*?</\\1>` with DOTALL, non-greedy)
  consumes from the FIRST <script> to the `<script>` that the comment's ">" terminates on,
  starting mid-comment. TAG_RE then removes "<!-- Bridge: Usercentrics consent_status -> Google"
  and leaves " Google Consent Mode + Matomo TM -->" as visible text.
  Probe: raw offset 1418; after SCRIPT_RE "<!-- Bridge: ... Matomo TM" then TAG_RE leaves
  " Google Consent Mode + Matomo TM -->". My html.parser emits nothing for a comment.
  Impact: exactly 37 bytes on line 2 of both snapshots; no quote, fact or anchor targets it.

DYNAMIC CHROME — explicit answer to the acceptance question:
  The two texts differ ONLY in navigation/footer label line-splitting plus the single
  comment remnant. The dynamic-chrome VALUES are identical between the two opens:
    cart   CHF 179 (S089) / CHF 135 (S090)      committed :77-79 / indep :81-83
    "Add to cart" x2 (mid + footer)              committed :79,:268 / indep :83,:283
    "Just released: the new edition of ISO 9001" 1 / 1 both
    "Cookie policy" 1 / 1 both (committed :258, indep :272)
    "© ISO 2026" 1 / 1 both (line 54 in both, verbatim)
    "Sign up for email updates" — 1 occurrence both, split by the parser into two lines
  So: no cart, cookie-banner or price drift between the committed capture and my re-open.

=====================================================================
5. PUBLISHER FACTS — knowledge file vs independent text
=====================================================================

Command: python3 "$S/facttable.py"   exit code: 0, "bad= 0"
Each row: the md's own pointer line holds the literal in the committed snapshot,
and the literal is present in my independent text.

S089 (corpus/knowledge/iso-29147-30111-standard-records.md:24-31)
  fact                     md line  committed  indep lines  verdict
  edition 2                   54        ok         58,67      AGREE
  publication date 2018-10    97        ok         101        AGREE
  reference 72311             59        ok         63,72      AGREE
  page count 32              103        ok         107        AGREE
  technical committee        105        ok         109        AGREE
  ICS 35.030                 107        ok         111,215    AGREE
  status ": Published"        95        ok         99         AGREE
  stage 90.92                 99        ok         103        AGREE
  currency 2024               64        ok         68         AGREE
  "Therefore this version remains current."  65 ok    69         AGREE
  abstract scope              84        ok         88         AGREE
  split sentence              91        ok         95         AGREE
  applicability (vendor/choose) 92      ok         96         AGREE
  successor "ISO/IEC AWI 29147" 204     ok         208        AGREE

S090 (:24-25,:27-30)
  edition 2                   54        ok         58,67      AGREE
  publication date 2019-10    90        ok         94         AGREE
  reference 69725             59        ok         63,72      AGREE
  page count 13               96        ok         100        AGREE
  technical committee         98        ok         102        AGREE
  ICS 35.030                 100        ok         104,208    AGREE
  status ": Published"        88        ok         92         AGREE
  stage 90.92                 92        ok         96         AGREE
  currency 2025               64        ok         68         AGREE
  "Therefore this version remains current."  65 ok    69         AGREE
  abstract scope              84        ok         88         AGREE
  applicability               85        ok         89         AGREE
  review cadence             109        ok         113        AGREE
  successor "ISO/IEC WD 30111.2" 197    ok         201        AGREE

  disagreements: NONE.

  Additional md literals verified verbatim against my text (python3 "$S/mdquotes.py"):
    "Status : Published"     occ=1 in BOTH texts for BOTH sources   — the md's spaced form
        (md:26 "Status : Published") is real page text: line 98 "Status" / 99 ": Published"
        in my text (S089), 91/92 (S090). "Status: Published" occ=0 — so the md is quoting
        correctly, not paraphrasing.
    "90.92 (To be revised)"  occ=1 both sources both texts (life-cycle gloss).
    "A standard is reviewed every 5 years" occ=1 in BOTH sources. The md cites it for S090 only
    (md:28 S090.txt:109 Q7) and that is correct; note it ALSO stands on the S089 page
    (my S089:120 / committed S089:116) — the md simply does not claim S089 lacks it. No error.

  NEGATIVE CONTROLS (md Claim 1 falsifiable rule, "a different edition is published"):
    grep edition strings in my S089 text: ISO/IEC 29147:2018 x10 (:1,53,56,62,64,70,71,86,119,216);
        ISO/IEC 29147:2014 x1 at :116, inside the life-cycle "Previously / Withdrawn" block
        (my :114-118) — history, exactly as md Claim 1 rejects.
    my S090 text: ISO/IEC 30111:2019 x9; ISO/IEC 30111:2013 x1 at :109, same Withdrawn block
        (my :107-112).
    => no newer published edition appears on either page; the md's edition claim is sound.
  Stage/status pairing re-read in my text: "Status / : Published" then "Stage /
    : International Standard to be revised [90.92]" (S089 :98-103, S090 :91-96) plus
    "Will be replaced by / Under development / ISO/IEC AWI 29147" (S089 :206-208) and
    "… / ISO/IEC WD 30111.2" (S090 :199-201). Consistent with md Claims 2.

  SCRIPT-LEAK CONTROL: gtag / dataLayer / denied / typeof / function( / javascript each
  occ=0 in BOTH committed snapshots and BOTH independent texts — the conversion drops
  script bodies on both sides; only the comment remnant differs.

=====================================================================
6. LANE INSTRUMENT RUNS (the claim's own counting commands)
=====================================================================

Command (from the lane root, as the claim specifies):
  cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-57/manifest.json --source S089

Printed:
  S089:sha256 OK
  S089:Q1 OK occurrences=1 anchor=1-ok
  S089:Q2 OK occurrences=1 anchor=84-ok
  S089:Q3 OK occurrences=1 anchor=91-ok
  S089:Q4 OK occurrences=1 anchor=92-ok
  S089:Q5 OK occurrences=1 anchor=99-ok
  S089:Q6 OK occurrences=1 anchor=64-ok
  S089:Q7 OK occurrences=1 anchor=204-ok
  EXIT_S089=0

  same with --source S090:
  S090:sha256 OK
  S090:Q1 OK occurrences=1 anchor=1-ok
  S090:Q2 OK occurrences=1 anchor=84-ok
  S090:Q3 OK occurrences=1 anchor=85-ok
  S090:Q4 OK occurrences=1 anchor=92-ok
  S090:Q5 OK occurrences=1 anchor=64-ok
  S090:Q6 OK occurrences=1 anchor=197-ok
  S090:Q7 OK occurrences=1 anchor=109-ok
  EXIT_S090=0

Both runs satisfy C2's expectation ("each exit 0 with 7 Q-OK occurrences=1 lines").
wc -c pins also hold: S089.txt 6647, S090.txt 5598 (wc -c, exit 0).

=====================================================================
7. ANCHOR PORTABILITY PROBE (declared limit, measured)
=====================================================================

Built a scratch manifest identical to the lane's except sha256/size/lines point at MY
independent text in $S/portability/ (S089.txt / S090.txt copies). Ran the LANE instrument
unmodified against it:

  python3 corpus/instruments/source-recheck.py --manifest "$S/portability/manifest.json" --source S089
    S089:sha256 OK
    S089:Q1 OK occurrences=1 anchor=1-ok
    S089:Q2 OK occurrences=1 anchor=84-BROKEN      ... Q3..Q7 all anchor=N-BROKEN
    exit=0
  --source S090: same shape, Q1 anchor=1-ok, Q2..Q7 anchor=N-BROKEN, exit=0

Finding: the pins are SNAPSHOT-RELATIVE. A re-capture with a different (even equally valid)
HTML->text conversion keeps all 14 quotes and their uniqueness but moves every anchor by +4.
This is NOT a C2 kill (the claim pins the committed snapshot, and source-recheck compares the
committed bytes), and the instrument already defines anchors against the snapshot's own lines
(source-recheck.py:anchor_verdict -> raw_lines[max(0,anchor-1):anchor+3]). Recorded so a future
re-capture from another converter does not read as a broken pin. Also note the instrument
emits anchor=N-BROKEN on a UNIQUE quote WITHOUT failing (occurrences<=1 short-circuits the
status=1 branch at source-recheck.py:196-206): anchors are advisory for unique quotes.

=====================================================================
8. LANE-SIDE CORRECTION CANDIDATES (text report only — nothing edited)
=====================================================================

R-57-SS-1 (snapshot hygiene, low severity, lane): corpus/instruments/capture-source.py's
  SCRIPT_RE leaves the fragment "Google Consent Mode + Matomo TM -->" on line 2 of both
  round-57 snapshots. 37 bytes; no quote or fact depends on it; it is the ONLY non-chrome
  byte absent from an independent conversion. Reported, not fixed.

R-57-SS-2 (documentation precision, low severity, lane): the md's capture-method limit
  paragraph says the recorded opens used "the instrument's own html_to_text conversion
  (unmodified import)". My re-run reproduces that exactly (identical sha256), so the
  statement is accurate. What the md does NOT note is that this conversion is lossy at nav
  boundaries and leaves one comment remnant; a reader who re-captures with stdlib
  html.parser gets -21 bytes and +15 lines. Worth one sentence in the next touch of that
  file; no numeric assertion in the md or manifest changes.

R-57-SS-3 (observation only): manifest `body_lines: [1, 268]` / `[1, 261]` and `lines`
  equal the full converted line counts; they agree with wc -l (268 / 261). No action.

=====================================================================
9. SCOPE / SAFETY RECEIPTS
=====================================================================

- Read-only on the lane: no write under L except this file and the ScoutSources/ text
  copies. No git add/commit/checkout/stash/reset/pull/push, no jj. Lane `git status`
  read once (shows only LOG.md, SCORECARD.md, .ufo/waves/round-57/w1/ — none of mine).
- No write to the fleet root, sibling lanes, or /home/vgpnk/Projects/shokuknow.
- Network: exactly two GETs, both named URLs, descriptive UA, --max-time 60. No vendor,
  coordinator or program was contacted; nothing was probed, scanned or submitted.
- Credential scan of both raw HTML bodies (shokunin redaction rule): set-cookie 0,
  bearer 0, token=/api_key= 0, op:// 0, AKIA 0, JWT 0 — nothing to redact.
- Scratch /fast/scratch/hyaku/kasegi-r57/ScoutSources deleted before yield; no leftovers.
- Lane HEAD read: cd3029876eac7189aaff0d32b26031c0defa35aa; base/freeze eae1d614...

ARTIFACTS COPIED INTO THIS WAVE DIR:
  .ufo/waves/round-57/w1/ScoutSources/S089.independent.txt
      sha256 27d8a769e55cf3e74b6ce07a1d11c6bce257b015de71b1b3f32847e0cf5c84cb  6626 B  283 lines
  .ufo/waves/round-57/w1/ScoutSources/S090.independent.txt
      sha256 e7233ccdcab01235794cfa938d173d83013ce317a5ef4f377ea38c874e0f028f  5577 B  276 lines
