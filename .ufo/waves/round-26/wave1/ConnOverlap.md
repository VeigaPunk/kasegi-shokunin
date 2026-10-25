# ConnOverlap — sibling F11-theme overlap scan (round 26 wave 1)

Seat: L1Kasegi26.ConnOverlap · Date: 2026-10-25 (UTC) · Mode: read-only leaf, no subagents.
Output: `.ufo/waves/round-26/wave1/c1-overlap.txt` (this report is the scoped findings).

## Target theme (F11, frozen in claims.json C2)
ISO/IEC 29147 / 30111 division of labour; JPCERT/CC 2026 partnership guideline
(P-guideline 付録6); assimilation package S041 (capture), staged S076/S064 by document.

## Method
- Pattern (case-insensitive): `29147 | 30111 | jpcert | パートナーシップ | partnership_guideline`
- Scope: all 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/` (kasegi
  excluded) + `/home/vgpnk/Projects/kimi-shokunin/skills`. Whole-repo scans
  (gitignore-aware tool) plus corpus-restricted scans; F11-token scan across all repos to
  hunt frontier-row IDs; frontier-section adjacency scan over every sibling corpus/README.md.
- Read-only. No writes outside the two named output paths.

## Verdicts (details in c1-overlap.txt)
| Lane | Hits | Verdict |
|---|---|---|
| mori | hex-hash substrings only | none |
| chousa | seed digits (93330111/12), hex | none |
| tameshi | hex | none |
| tabi | 0 | none |
| kengaku | fixture JSON junk | none |
| kama | 0 | none |
| mado | generated `x29147 = 29147` fixture, hex | none |
| kumitate | hex/jj-store substrings | none |
| kotodama | hex | none |
| kake | RFC 9116 (S078) capture cites `[ISO.29147.2018]`; entry explicitly excludes vulnerability handling | **distinct** |
| revenger | jsac.jpcert.or.jp host in S090 (JSAC2026 deck; quarantined, register-wrong) | **distinct** |
| tsukuroi | hex | none |
| kotoba | 0 | none |
| kaidoku | hex/UART decode ranges | none |
| lore | 0 | none |
| game-dev-2d | 0 | none |
| audio | run-path timestamps (…T124329147597Z…) | none |
| game-dev-3d | 0 | none |
| kagi | 0 | none |
| souji | sizes/mtimes/index digits | none |
| kimi skills | 0 | none |

## F11-equivalent frontier check
No sibling holds an F11-equivalent frontier row:
1. Zero thematic-term hits in any sibling `corpus/README.md` (coverage/frontier maps).
   The only security-adjacency match in the frontier scan is kake's
   `knowledge/security-txt-publishing.md` row, whose own scope sentence states
   "Vulnerability handling itself (report intake, triage, remediation, disclosure timing,
   bounty and policy operation) stays outside this province" — i.e. it explicitly declines
   the F11 subject.
2. Every `F11` token across sibling repos is an internal finding/seat ID (e.g. mori
   r13–r22 F11 rows, tameshi `F11ScopeOverlap`, kengaku `RevF11`/`CorrF11`, lore r93/94
   F11 seats, game-dev-3d F11 cards), never a frontier row ID.
3. The terms 29147 / 30111 / JPCERT / パートナーシップ / partnership_guideline occur in no
   sibling `corpus/README.md`.

## Adjacent lanes (distinct, not overlap)
- **kake**: S078 = RFC 9116 (security.txt) captured 2026-10-22; the captured text's
  "Readers are encouraged to consult other documents such as [ISO.29147.2018] or
  [CERT.CVD]" is a pointer inside RFC 9116, not a claim or frontier. The admitted corpus
  entry (security-txt-publishing.md, S078–S085) is about *serving a security.txt file*
  and deliberately leaves vulnerability handling out. No 30111 / JPCERT / partnership.
- **revenger**: S090 (round3) cites the JSAC 2026 workshop 3 PDF hosted on
  jsac.jpcert.or.jp (.NET/AOT malware RE paper). This is a JPCERT/CC-hosted conference
  deck, not the 2026 partnership guideline; the row is quarantined (absent-defect register:
  payload-absent; re-checks: PRESENT, register-wrong). No 29147/30111/partnership.

## Risk / caveats
- Digit substrings inside sha256 hex digests, timestamps, seeds, sizes and generated
  fixtures produce false-positive lexical hits; all classified and excluded as non-thematic.
- Whole-repo counts that include untracked/ignored files (e.g. audio corpus/live logs,
  tabi reports/, kaidoku session transcripts) inflate raw counts; corpus-restricted scans
  confirm zero thematic content. kasegi's own corpus hits (15 files) are its own
  29147/30111 F11 frontier material (out of scope here).

## Conclusion
No sibling lane's corpus overlaps the planned F11 theme; no sibling holds an F11-equivalent
frontier row. Two lanes (kake, revenger) are adjacent but explicitly distinct. The F11
frontier admission is safe from sibling overlap.
