# CritVacuityC2 — C2 vacuity attack (round 26, wave 1)

Seat: UFO-FSD critic (leaf; read-only except owned report paths).
Date: 2026-10-25 UTC. Output artifact: `.ufo/waves/round-26/wave1/k2-vacuity.txt`.
Target: frozen claim C2 (coverage, score 7 held) — F11 frontier admission + `>=1` knowledge entry citing a source row first registered this round + sources census exit 0.

## Counterexample (strongest, from local evidence)

**The round-25 tree alone already satisfies the "entries citing S04x" AFTER limb.** The frozen counter
`grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md | wc -l` returns **1** today, before any round-26
knowledge entry exists, because the round-25 F10 entry `vendor-disclosure-policy-commitments-crosswalk.md`
(header line 2) carries `source: S040 ...`. S040 was first registered in round 25, not this round. So:

- the frozen BEFORE value `entries_citing_row_first_registered_this_round: 0` is false (already 1);
- zero round-26 work meets the AFTER value `>=1` — the do-nothing control hits it;
- the predicate "first registered this round" is not testable by this counter.

Second counterexample: **empty shells satisfy every C2 counter** (scratch-mirror demo):
two F11 entries whose entire content is `source: S041`/`verified-at`/`recheck:` headers yield
`awk frontier admitted = 11`, `grep S04x = 3`, census used-by edges resolved, and
`frontier-recheck-count.py: entries=14 pass=14 exit=0`. The harness passes shells because
`source-recheck.py` only verifies the manifest's pinned quotes against the snapshot bytes and never reads
the entry body.

## Evidence (all measured 2026-10-25)

1. **Counter unfairness (live + scratch).** Live: `grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md` → only `vendor-disclosure-policy-commitments-crosswalk.md` (S040). Scratch registry with S040/S041/S039/S050/S049/S04 header rows: the frozen counter matches S040, S041, S049 (count 3); not S039, not S050, not bare `S04`. The regex selects the whole S040–S049 id band — it cannot express registration round.
2. **Empty-shell pass.** Scratch mirror: two header-only entries plus the already-landed F11 row → awk=11, grep=3, frontier harness pass=14/14 exit=0; full-mirror census clears the S041 E11 once the files exist.
3. **Duplication scan.** Versus the admitted corpus: the staged F11 crosswalk's Cisco half (staged S068 = same page as lane S040) duplicates the F10 quote `cisco-iso-29147-2018` ("The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018") and F10's falsifiable rule 1 ("Edition, not presence"). The adopted wave plan (w3, S041-only) drops that half. The division-of-labour claims (29147 outward vs 30111 internal) and the divergence claims (P-guideline does not require a disclosure policy while 29147:2014 does; 6.2/6.3 clause reproduction; 7-day acknowledgement) are absent from the admitted corpus — genuinely new if the scribes write them as planned; no C2 counter verifies any of it.
4. **Frontier counting.** Steady state (scratch): F01–F10 unchanged, `entries=12 pass=12` → `entries=14 pass=14` after F11+2 entries — no break. But **row-before-entries** (the current live state: README already carries the F11 row; the two knowledge files do not exist) makes `frontier-recheck-count.py` crash with an unhandled `FileNotFoundError`, exit 1 — not a clean FAIL. Also, the live F11 row cites `-2026-10-23.md`-suffixed names while the wave's scribe prompts and the S041 used-by cell use unsuffixed names (`iso-29147-and-30111-division-of-labour.md` etc.) — a name mismatch that would keep both the harness crash and the E11 dangling.
5. **Census blocker.** Live census exits **1**: E09 on S040 and S041 (`recheck=180d — <prose>` is not a parsable cadence) plus E11 on S041 (entries absent). Full-mirror test with entries present: E11 clears, E09 remains → census still exit 1. The C2 third limb ("census exits 0") is unreachable with the current S040/S041 recheck-cell texts.

## Impacted axes

- **coverage (C2)**: the "first registered this round" limb is untestable/vacuously satisfied; the "entries citing S04x" limb is satisfied by pre-existing round-25 bytes and by empty shells.
- Hotdepth:verifiability** (indirect): the row-before-entries state breaks `frontier-recheck-count.py` (unhandled exception); the F11 name mismatch would keep it broken.

## Smallest safe corrections (as appended notes/corrections; never in-place edits to frozen claims.json)

1. Bind the S04x counter to the round's newly-appended ids: round 26 → `grep -lE '^source: S041 ' corpus/knowledge/*.md | wc -l` (or a census-backed opened=this-round ∧ mined filter); state explicitly that S040 (round 25) must not count.
2. Require at least one new entry to be Q1–Q9-conformant with a non-empty body — e.g. gate on the recheck-audit expected-list and on a body-quote binding (≥1 manifest assertion whose quoted text also occurs in the entry body) so empty shells cannot pass.
3. Align the README F11 entry cell with the exact filenames the scribes create (and with the S041 used-by cell); land the row only after the entries exist, or make frontier-recheck-count.py report missing entries as FAIL instead of raising.
4. Restore S040/S041 recheck cells to the bare cadence `180d` (notes out-of-cell) so the sources census can exit 0.
