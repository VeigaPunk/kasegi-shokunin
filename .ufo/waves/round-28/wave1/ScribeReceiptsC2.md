# ScribeReceiptsC2 — C2 receipt bundle index (round-28, wave 1)

Seat: `ScribeReceiptsC2` (scribe, leaf — no subagents, no background jobs, no swarm).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Lane HEAD `94f387cbee71a532a51ce075f01701a557231e85`; claims-freeze base
`c9f8b115a098c65356e4b3b6048af45a37ab8395` (ancestor, `git merge-base --is-ancestor` exit 0).
Snapshot stamps: receipts/reports pinned 2026-10-25T17:32:56Z; frozen counters run
17:32:02Z–17:32:03Z; artifact pins 17:32:18Z; controls 17:33:36Z; lesson re-pinned 17:38:59Z.
Tooling installed/upgraded: **NONE** (python3 + coreutils + the repo instruments sufficed; pacman is
host-paused and was not attempted).

## Deliverable

`.ufo/waves/round-28/receipts/ScribeReceiptsC2.txt` (372 lines) — the C2 bundle digest the canonical
C2 receipt block and the round report cite. It carries:

1. the five frozen-counter rows (four claims.json commands, the third split into row-grep 3a and
   census 3b) with before/after, post-state observation timestamps and receipts of record;
2. a per-counter coverage matrix naming the PRE receipt, the POST receipt written by another seat,
   and the independent review — no frozen counter rests on this index's run alone;
3. the non-counter C2 predicate clauses (capture pins, manifest Q9, entry headers/recheck, S042 row,
   S041 used-by, assimilation Gate, QUALITY R14) mapped to receipts;
4. kill-rule limb coverage, including which limbs were actually exercised mid-wave;
5. full/truncated sha256 pins for every artifact and every C2 receipt;
6. one-line summaries for the `receipts/*.txt` files and the reviewer/attacker `wave1/*.md` reports;
7. §8 named gaps with the exact closing command for each;
8. §9 this seat's verbatim measurements, labelled as index-observed, not seat receipts.

No canonical index was created under `.ufo/waves/round-28/` root (defect-4 conformance).

## Frozen C2 counter coverage — verdict

All four frozen `counter_commands` (five measured values) reached their frozen after values, and each
has at least one POST-state receipt written by a seat other than this index:

| counter | after | POST receipt(s) |
|---|---|---|
| frontier admitted | 12 | ScribeReadmeC2 (row landed), ExecReceiptCanonC2 17:27:13Z, RevCounters2 17:26:24Z |
| entries citing S042 | 1 | ScribeEntryC2 (entry landed), ExecReceiptCanonC2, RevCounters2 |
| S042 row | 1 | ScribeRegistryC2 (SOURCES.md:48), RevRegistryC2, ExecReceiptCanonC2 |
| census | exit 0, 42 rows, W04 ×2 only | ScribeRegistryC2 §6(c), ExecHarnessC2 E1, RevCensusEnd, ExecReceiptCanonC2 |
| frontier harness | `entries=15 pass=15 exit=0` | ExecHarnessC2 B3, ExecReceiptCanonC2, RevCounters2, ExecGateLog §E |

Byte pins: S041 `e18acbf9…` (147267 B, byte-identical to round-26), S042 `b432ec16…` (60508 B),
manifest `e62ddad1…` (5038 B), entry `a22d2321…` (18544 B), SOURCES `e59240f8…` (42 rows), README
`5f458a7a…` (245 lines, F12 at :213), QUALITY `00d4b2a3…` (R14 at :83), lesson `973b6362…` (517 lines).
Census stdout sha256 `920e6fd4…`; harness stdout sha256 `17ffa632…`.

## Findings handed to the canonical judge

1. **Gate predicate wording is the one open C2 question.** The landed lesson has exactly one inline
   `「…」` quote — the S042 L145 admit quote (63 chars / 2 whitespace-words). The two reject rows carry
   measured reasons and flip conditions but no verbatim quote of the rejected candidate's load-bearing
   sentence; `ScoutAssimilation.txt` §7's "inline quote available" string is S041/staged-S043 anchor
   text, not the rejected claim. If C2's "with inline ≤25-word quotes" is read as binding the reject
   arm, append a correction (R25-1); if it is read as the Gate's new-source disclosure (round-26
   defect-3 shape), it is satisfied. Recorded in the digest as G1a, not asserted either way.
2. **Entry receipt drift.** `ScribeEntryC2.txt` pins the entry at `a0f8e617…` / 18452 B, but the live
   entry is `a22d2321…` / 18544 B (revised in place 17:29:21Z after the receipt). ScribeQualityCross
   audited the live bytes; re-pin the receipt at close.
3. **Expected-list refresh is still owed.** Live `recheck-audit.py` prints `lines=40 total=40 pass=40`
   with `expected=39 … unexpected=1 exit=1`; only the new entry is unexpected. Regeneration to 40
   entries / 42 lines clears it (ExecExpectedList names the commands; scratch-measured exit 0).
4. **Instrument gaps, routed not patched:** `frontier-recheck-count.py` raises an uncaught
   `FileNotFoundError` instead of failing a row when an admitted frontier row's entry is absent;
   `source-recheck.py` does not enforce manifest path stem == id (MutManifestC2 M1 survives) and does
   not fail an unanchored duplicate (MutQuoteC2 M3 live). Both limbs currently hold by review and by
   the live bytes.
5. **"six-step" is false on both captures.** S042.txt:162-182 numbers the web-app flow 1.–7.; the
   landed entry, S042 registry row, F12 README row and lesson all say seven. Any later text asserting
   six must be rejected on these bytes.
6. **`claims-erratum-1.md` is C1-scope only** (corpus-disclosure cell superseded: zero backticked
   anchored bounties citations, no verdict-class movement). Re-ran the C2 counters after the erratum:
   unchanged.

Also noted in the digest: direct admission review `CritC2Admission.md` finds the F12 admission
survives its four tested grounds but records one fixable silent drop (the staged pre-publication
user-notification claim is omitted from the re-grounded entry: restore with its S041 anchor or
disclose the omission).

## Touched surfaces

Writes by this seat (only):
- `.ufo/waves/round-28/receipts/ScribeReceiptsC2.txt` (bundle index)
- `.ufo/waves/round-28/wave1/ScribeReceiptsC2.md` (this report)

No production file, no instrument, no claims file, no prior-round artifact, no VCS write, no write
under `/home/vgpnk/Projects/shokuknow`, the fleet root, `.ufo/state`, `.scratch`, `MANIFEST.json`,
`templates/` or fleet `scripts/`.

## Not verified / out of scope

- No counter, fixture, manifest or capture was re-derived as a pass by this seat: the index cites the
  producing seat's receipt and its own observation, and labels both.
- C1 (anchorcheck.py, SKILL.md) receipts are excluded and listed separately; the C1 instrument digest
  moved during the wave (`95333e29…` at snapshot) and is the C1 seats' to pin.
- The lesson's own content was checked for the C2 predicate clauses only (Gate, admits/rejects,
  used-by old→new, inline quote count); its prose quality is ScribeLesson's and the reviewers' scope.
- Seat receipts are rewriteable: every hash in the digest pins bytes at 17:32:56Z. Any receipt
  rewritten after that must be re-hashed; the digest says so (G6).

## L1 re-run set at close (from the lane root)

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md   # 12
grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l                                          # 1
grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md                                   # 1
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo census_exit=$?   # 0
python3 corpus/instruments/frontier-recheck-count.py                                             # entries=15 pass=15 exit=0
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json   # 12/12 OK exit 0
sha256sum corpus/lessons/round-28.md corpus/knowledge/japanese-domestic-disclosure-workflow.md \
          corpus/source-snapshots/round-28/{manifest.json,S041.txt,S042.txt}
# then fix G2/G3/G4 (expected list, entry receipt re-pin) and assemble the canonical receipt at the
# landed digest (assemble-receipts.py + the ExecReceiptCanonC2 block).
```
