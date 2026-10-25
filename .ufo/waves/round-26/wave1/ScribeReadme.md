# ScribeReadme — corpus README F11 admission (wave 1, round 26)

- Seat: `L1Kasegi26.ScribeReadme`
- Sole owner of `corpus/README.md`; lane base `1b076fa7f2fb5e7dd9d87449514eba526043421b`.
- Date: 2026-10-25 (UTC).

## Behavior

Edited `corpus/README.md` exactly as assigned — two changes, no other row touched:

1. **Frontier table: added row F11** after the F10 row (new line 212):

   ```
   | F11 | ISO/IEC 29147/30111 division-of-labour meta | admitted | knowledge/iso-29147-and-30111-division-of-labour-2026-10-23.md, knowledge/iso-29147-divergence-and-clause-crosswalk-2026-10-23.md | S041 | Treat 29147 as the vendor's outward-facing disclosure standard and 30111 as its internal handling process; record the edition a source names (JPCERT/CC compares against 2014, Cisco claims 2018). |
   ```

   - Status `admitted`; entries link the two new knowledge entries by the names frozen in `claims.json` C2 `staged_entries` (identical to the package files at `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/`).
   - Sources cell: `S041` (the adopted lane id = JPCERT/CC 2026 P-guideline capture; renumbers staged S076/S064 by document — both anchors live in the same PDF, §2/図1 p.45 and 付録6 §4+参考1 p.46-47/53-54).
   - `next` cell guidance is grounded in the staged entries' own claims (outward vs inward scope; edition drift 2014 vs 2018).

2. **Frontier section prose (denominator paragraph):** replaced the round-25 decision text with the round-26 state:

   ```
   -public-practice frontier above is a separate denominator (10/10 admitted at round 25; F01-F08 at
   -round 23, F09 at round 24, F10 at round 25) and is not counted into the 0/18 figure.
   +public-practice frontier above is a separate denominator (11/11 admitted at round 26; F01-F08 at
   +round 23, F09 at round 24, F10 at round 25, F11 at round 26) and is not counted into the 0/18 figure.
   ```

**Frontier logic — F12:** the repo's frontier step (`templates/round-prompt.md` §2b) does not require naming a successor frontier; no admitted-round README (r23/r24/r25) names the next F-id after a row admission, and no lane/fleet doc assigns F12 a topic. Per the instruction's conditional, F11 is marked admitted without inventing an F12 row; the F11 `next` cell carries the continuation guidance, matching the established row pattern.

## Diff (verbatim, `git diff -- corpus/README.md`)

```
diff --git i/corpus/README.md w/corpus/README.md
index 6880525..309eadd 100644
--- i/corpus/README.md
+++ w/corpus/README.md
@@ -209,8 +209,9 @@ Correction (2026-10-19): corpus/QUALITY.md now exists; the preceding closing par
 | F08 | EU Cyber Resilience Act reporting duties | admitted | knowledge/cra-manufacturer-reporting-duties.md | S029 | Distinguish manufacturer statutory tracks from researcher disclosure; Article 14 applies from 2026-09-11. |
 | F09 | Authorisation outside the platform: the engagement document and the statute | admitted | knowledge/authorised-testing-rules-of-engagement.md, knowledge/statutory-authorization-and-unauthorized-access.md | S032, S033, S034, S035 | A safe-harbour badge is not the grant and not the legal definition: read the ROE's scope/exclude list, and the access manager the statute requires. |
 | F10 | Vendor-side disclosure policies as corpus objects | admitted | knowledge/vendor-disclosure-policies-as-corpus-objects.md, knowledge/vendor-disclosure-policy-commitments-crosswalk.md | S036, S037, S038, S039, S040 | A vendor's published policy is a standing first-party statement, not a programme: read its intake channels, its handling-versus-disclosure scope, the standard edition it names, and the conditions (and count of conditions) under which it goes faster. |
+| F11 | ISO/IEC 29147/30111 division-of-labour meta | admitted | knowledge/iso-29147-and-30111-division-of-labour-2026-10-23.md, knowledge/iso-29147-divergence-and-clause-crosswalk-2026-10-23.md | S041 | Treat 29147 as the vendor's outward-facing disclosure standard and 30111 as its internal handling process; record the edition a source names (JPCERT/CC compares against 2014, Cisco claims 2018). |
 
 The original domain-root map is exhausted: 0/18 surfaces are present.
 That sentence describes the lost `/home/vgpnk/Projects/bounties` surface set only; the
-public-practice frontier above is a separate denominator (10/10 admitted at round 25; F01-F08 at
-round 23, F09 at round 24, F10 at round 25) and is not counted into the 0/18 figure.
+public-practice frontier above is a separate denominator (11/11 admitted at round 26; F01-F08 at
+round 23, F09 at round 24, F10 at round 25, F11 at round 26) and is not counted into the 0/18 figure.
```

Summary: `1 file changed, 3 insertions(+), 2 deletions(-)`.

## Gate — frozen counter on my edited copy

Command (claims.json C2 counter 1), run from lane root on the edited file:

```
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
```

Result: **`11`** (before: 10). The F11 row matches the frozen pattern (id field ` F11 `, status field ` admitted `).

## Touchpoints

- `corpus/README.md` — F11 row + frontier denominator paragraph (only changes).
- `.ufo/waves/round-26/wave1/ScribeReadme.md` — this report.

## Out-of-scope / intentionally unchanged

- Coverage-map header correction line (r26 entry count) left untouched: the two knowledge entries were not yet present in `corpus/knowledge/` at write time (37 files; ISO entries land from the entry-executor seats), so an entry-count clause would be speculative.
- `corpus/knowledge/` entry files themselves not written (not my scope).
- `SOURCES.md` S041 row and snapshots owned by other seats (ExecCaptureS041 receipt confirms S041 = JPCERT/CC 2026 guideline, sha256 `e18acbf9…`, captured 2026-10-25T12:34:17Z; staged S076/S064 anchors verified inside it).
- No tool installed/upgraded (none needed; no pacman transaction).

## Findings/limits

- Editor quirk: `edit` calls with a relative `[README.md#TAG]` bracket were rejected ("hash not from this session"); using the absolute path form `[/home/vgpnk/…/README.md#TAG]` succeeded. Tags are per-read; no content surprise.
- The F11 row references entries that exist in the staged package but not yet in `corpus/knowledge/`; the round's own wave will land them. README row stands as the admission marker; the awk counter already yields 11.
