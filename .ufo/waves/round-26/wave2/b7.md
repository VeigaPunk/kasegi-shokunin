# AttackB7 — precise C2 counter (falsify: "entries citing a row first registered this round")

Seat: AttackB7 (leaf, read-only). Round 26, wave 2. UTC 2026-10-25.
Attack target: C2 predicate limb "at least one knowledge entry cites a source row first registered this round" and its frozen counter `grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md | wc -l` (claims.json counter_commands[1], before 0, after >=1).
Verdict: **counter is overmatching and its frozen before 0 is stale; the precise S041-only measure is the honest one and passes (2).**

## 1. Commands run (lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`)

```
$ grep -lE '^source: S041 ' corpus/knowledge/*.md | wc -l
2
$ grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md | wc -l
3
$ grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md
corpus/knowledge/iso-29147-and-30111-division-of-labour.md
corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md
corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
```

Matches expected values: precise 2, overmatch 3 = round-25 S040 + the two S041.

## 2. What the 3 overmatch hits are

| File | source: line | Row | Opened | Round registered |
|---|---|---|---|---|
| `knowledge/iso-29147-and-30111-division-of-labour.md` | `source: S041 — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf …` (line 2) | S041 | 2026-10-25 | round 26 |
| `knowledge/iso-29147-divergence-and-clause-crosswalk.md` | `source: S041 — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf …` (line 3) | S041 | 2026-10-25 | round 26 |
| `knowledge/vendor-disclosure-policy-commitments-crosswalk.md` | `source: S040 — https://www.cisco.com/…` (line 2) | S040 | 2026-10-25 (round-25 row) | round 25 |

Git evidence: `vendor-disclosure-policy-commitments-crosswalk.md` was added at round-25 commit `98261eb` ("round-25: repair rechecks and assimilate vendor policies", `git log --diff-filter=A -1`). Both iso-29147 files are untracked (`git status --short`: `?? corpus/knowledge/iso-29147-…`) — landed this round, not yet committed. S041 row in `corpus/SOURCES.md` line 47: `S041 | 情報セキュリティ早期警戒パートナーシップガイドライン 2026年10月 (JPCERT/CC) …` (opened 2026-10-25, mined, used by both F11 entries).

## 3. Why the frozen "before 0" is stale

The claim's before value `entries_citing_row_first_registered_this_round: "0"` is attached to the literal counter `grep -lE '^source: S04[0-9] ' …`. That grep matches **any** S04x citation, and `vendor-disclosure-policy-commitments-crosswalk.md` has carried `source: S040` since round-25 commit `98261eb`. Therefore the literal counter on any pre-wave-1 tree with round-25 state intact returns **1**, never 0. The frozen 0 cannot be a real run of the literal counter; it encodes the intended semantic ("no entry cites a row *first registered this round*") — an unmeasured implication recorded at freeze (claims.json frozen `2026-10-25T12:27:41Z` before any measurement, per R25-1). This is already logged in `corpus/lessons/round-26.md` M26-4: "the before value is 1, not 0 — the do-nothing control hits the after value (`>=1`) with zero round-26 work". So: (a) 0 is false as a literal measurement (true literal before = 1), and (b) the correct baseline for the frozen grep is 1, making the observed 3 a delta of 2 — same substantive result as the precise counter, but only after subtracting the round-25 S040 shell.

## 4. Why the precise S041-only measure is the honest one for "first registered this round"

- "First registered this round" is a property of the **registry row**, not of the `S04` prefix. The distinguishing predicate is the row id opened in round 26 — S041 (opened 2026-10-25). S040 is a round-25 row: it was not appended this round (the staged Cisco row S068 was explicitly not re-adopted; SOURCES/round-26 lesson: "staged S068 (Cisco) → already lane S040 (round 25)"). `^source: S041 ` selects exactly the entries citing rows newly registered this round → 2.
- It is also the exact kill-rule-relevant test. C2's kill rule is "a source row is appended without an admitted entry citing it". The only row appended this round is S041; the honest question is "every appended row cited by an admitted entry?" → yes: 2 admitted F11 entries cite S041 (README.md F11 row, `sources` cell `S041`).
- The overmatch cannot discriminate and is vacuity-prone (M26-4): a shell entry citing S040 alone would satisfy `>=1` with zero round-26 registration. The S041-only count ties the measure to the row actually registered this round, and its 2 matches the admitted-entry structure (two F11 entries, each with one `source: S041` line).

## 5. Counter status summary

| Measure | Frozen before | Observed now | Verdict |
|---|---|---|---|
| `grep -lE '^source: S041 ' … | wc -l` | — (not frozen) | **2** | honest "first registered this round" count; after >=1 satisfied |
| `grep -lE '^source: S04[0-9] ' … | wc -l` | 0 (stale; literal before = 1) | **3** | overmatch = S040 (round-25) + 2×S041; matches expected 3 |
| sources census (`sources-census.sh validate`) | exit 0 | **exit 0** (only pre-existing W04 S028/S029 warnings) | C2 kill-rule "census exit ≠ 0" limb clear at wave 2 |

## 6. No findings beyond scope

- No defect found in the two S041 entries' `source:` lines; both are `^source: S041 ` and point at the S041 capture (`corpus/source-snapshots/round-26/S041.txt`, sha256 `e18acbf9…` per the divergence entry; SOURCES S041 row cites the same capture).
- The frozen counter's overmatch is documented in lane lessons (M26-4) and this report; no claims/byte edits made (read-only seat).
- No tools installed (no installs required/recorded).
