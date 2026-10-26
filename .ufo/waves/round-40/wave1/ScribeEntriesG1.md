# ScribeEntriesG1 — three knowledge entries for the first mined group (S016, S017, S019)

Seat: scribe, round 40 wave 1. Lane HEAD at work time: `5e985b74075dd3813a63d7750966bf8abf693465` (`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD`) — the claims-freeze commit named in the seat prompt. No mutating git/jj command was run anywhere; no pacman, no tool install, no lane file outside this receipt and the three deliverables was written.

## 1. Deliverables (byte-exact, beside this receipt)

| file in `wave1/` | lands at | lines | bytes | sha256 |
|---|---|---|---|---|
| `ScribeEntriesG1.anthropic-cvd-provenance-and-pacing.md` | `corpus/knowledge/anthropic-cvd-provenance-and-pacing.md` | 132 | 16937 | `9536e1b321dd285a1e3f3552a26edd5d6e4f8c6c58d8620446b4c4331ea01f38` |
| `ScribeEntriesG1.pz-reporting-transparency-trial.md` | `corpus/knowledge/pz-reporting-transparency-trial.md` | 136 | 15072 | `270b6a0a73061d85063a463a120c87c6786a6bf03a7cc492a949383034408c1a` |
| `ScribeEntriesG1.nist-sp800-216-vdp-framework.md` | `corpus/knowledge/nist-sp800-216-vdp-framework.md` | 121 | 16018 | `757058a5d8e03c83c61c6b7c22852400bcbea1b252504a9e8f5c7a56da79d596` |

Names were fixed with `ScribeRows` by IRC before drafting (its `used-by` cells use these paths); the three files are already in `wave1/`, so `ExecHarnessUpdate` can list them without waiting. Each file opens `H1`, then `source:` / `verified-at:` / `ground:` / `recheck:` (QUALITY Q1; Q10 form), has no fenced blocks (`grep -c '```'` = 0 in all three), and carries no receipt text.

| entry | ground | block-quoted spans | words max | quote anchors |
|---|---|---|---|---|
| S016 | `F02` (extends S003/S004/S005 clocks with a discoverer-side post-patch details buffer, AI-origin label, pacing rule) | 22 | 24 | 22/22 start on the declared line |
| S017 | `F02` (a fourth timeline shape: unchanged 90-day deadline + ~1-week notice milestone; defines the upstream patch gap F06 presumes) | 24 | 25 | 24/24 |
| S019 | `core` (no frontier row covers a government-side framework; nearest F02/F06/F10/F11 stated in the entry) | 14 | 24 | 14/14, six of them anchored because the abstract recurs |

## 2. Capture dependency and independent re-open

All three rows had been captured by the wave-1 scouts before I wrote anything; I re-opened each URL myself and reproduced or compared the landed bytes. Fetch form: `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`.

| source | my fetch (UTC) | HTTP | raw bytes | raw sha256 | landed capture | reproduction |
|---|---|---|---|---|---|---|
| S016 | 2026-10-26T21:16:37Z | 200, text/html; charset=utf-8 | 164307 | `d7dbc1766f4b7cc3d600b42d87f1f140c44679d3495eb902434861d8a1110ded` | `ScoutS016.capture.txt` 32 lines / 4481 B / `91cc996f…` | corpus L5–L17 byte-identical; footer sentence at L28 differed (site A/B text) → my converted snapshot 32 lines / 4550 B / `7070a363…`; `diff` shows exactly that one line |
| S017 | 2026-10-26T21:16:38Z | 200, text/html | 14764 | `6addf3baff5f61ff7a6a8750007cc2b0d4aa2153a317ed2a8974412bbce2cfb3` | `ScoutS017.capture.txt` 39 lines / 5058 B / `3b6aaf1f…` | `cmp` clean — identical snapshot (raw bytes differ per fetch because the page carries a per-request nonce; the scout recorded the same effect: raw `4bd7186c…`, same snapshot sha) |
| S019 | 2026-10-26T21:16:38Z | 200, text/html; charset=utf-8 | 44658 | `1703b2954151b5f3e9dbe53a1da5fd0517ba1852de83b0d76ffafebf74e54b7d` | `ScoutS019.capture.txt` 132 lines / 4901 B / `514cc379…` | `cmp` clean — identical snapshot |
| S019 PDF (not committed) | 2026-10-26T21:16:57Z | 200, application/pdf | 1510851 | `363183f02e9366e63a0913080c6576cb4f10f1b635e0a3f12ad7367d8980b67f` | — | fetched only to confirm the recommendations are *not* on the captured landing page; no quote in any entry comes from it |

Normalization for every conversion was the lane's own `corpus/instruments/capture-source.py` (`html_to_text()` / `pdf_to_text()`), imported read-only from the lane; nothing in the lane was modified.

Consequence recorded in the S019 entry itself: the S019 capture is the CSRC **publication record** (title, dates, authors, abstract, keywords, DOI, Document History), not the 800-216 body. The entry therefore makes abstract/publication-record claims only and states that limit; it does not describe clauses, section numbers or procedure.

## 3. Validation (commands and actual output)

**V1 — every block quote is verbatim, ≤25 words, starts on its declared line.** Checker: normalize capture (`whitespace collapse`, `<u>` stripped) and entry quote, count occurrences, test that the declared line's byte range contains an occurrence.

```
S016 spans=22 words_max=24 failures=0
S017 spans=24 words_max=25 failures=0
S019 spans=14 words_max=24 failures=0   (distinct=14; six abstract spans occ=2-3, each anchored)
```

**V2 — cited line numbers inside the entries resolve (lane citations only).** `KASEGI_LANE_ROOT=/home/vgpnk/Projects/shokunin/kasegi-shokunin python3 corpus/instruments/anchorcheck.py <entry>`:

```
entry-S016: 1 in-range cite instances, 0 bad; BASE-ABSENT=0 → OK md:24 corpus/knowledge/coordinated-disclosure-timelines.md:24
entry-S017: 1 in-range cite instances, 0 bad; BASE-ABSENT=0 → OK md:68 corpus/README.md:207 (the F06 row)
entry-S019: 0 in-range cite instances, 0 bad; BASE-ABSENT=0
```
(exit 0 each). Without `KASEGI_LANE_ROOT` the same files report `BASE-ABSENT`, because anchorcheck infers the lane root from the checked file's ancestry and these live in scratch — that failure is an artifact of draft location, not a bad cite.

**V3 — source-recheck readiness for each entry's `--source`, on landed capture bytes.** Scratch manifest built from the three scout records (`path` stems equal ids), captures copied under those names:

```
S016:sha256 OK
S016:Q1 OK occurrences=1 anchor=17-ok
S016:Q2 OK occurrences=1 anchor=16-ok
S016:Q3 OK occurrences=1 anchor=12-ok                       rc=0
S017:sha256 OK / Q1 anchor=23-ok / Q2 anchor=34-ok / Q3 anchor=34-ok   rc=0
S019:sha256 OK / Q1 occurrences=2 anchor=80-ok / Q2 occurrences=2 anchor=80-ok / Q3 anchor=97-ok   rc=0
```

**V4 — the same check fails closed when its base is missing or mutated** (the Q7/R15 control):

```
corrupt capture (+1 byte)      -> S016:sha256 MISMATCH expected=91cc996f… actual=a0440562…   rc=1
capture file removed           -> S019:source UNAVAILABLE reason=missing                     rc=2
manifest path absent           -> manifest UNAVAILABLE reason=missing                        rc=2
```

**V5 — the entries' `recheck:` lines are executable, cwd-independent and fail-closed before landing.**
`bash -n -c` rc=0 for all three; running the line from the lane root and from `/` produces byte-identical output and the same status; today both are `manifest UNAVAILABLE reason=missing`, rc=2 (the round-40 manifest is not landed yet — the entry text says the line fails closed in that case). After landing it must print the V3 lines.

**V6 — recheck-audit form, measured on a scratch mirror of the lane HEAD** (`git -C <lane> archive HEAD | tar -x` into scratch; the three entries copied to `corpus/knowledge/`; the three captures + a three-record manifest placed at `corpus/source-snapshots/round-40/`; the entries' `cd` prefix repointed at the mirror so limb (d) can be exercised):

```
before the round-40 manifest exists in the mirror:
  lines=54 total=54 pass=51 fail-closed=27 parse_fail=0 cwd_fail=0 paths_fail=3 exit=1   <- the 3 are my new lines' manifest path
after the captures + manifest exist in the mirror:
  lines=54 total=54 pass=54 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
  strict pass=4/54 cdroot_fail=50        <- limb (d) compares against the audited root; every line that names the true lane root fails it in a mirror, my three included by construction, so this figure is not evidence for or against these entries
with the HEAD expected list (the landed list + 0 new names):
  expect=present expected=51 missing=0 unexpected=3 exit=1
with the three paths appended:
  expect=present expected=54 missing=0 unexpected=0
```

**V7 — no collateral text or fences in deliverables.** `grep -c '```'` = 0 in all three; each file's only H1 is the entry title; no `## DELIVERABLE` block is used because the deliverables are separate files.

## 4. Dependencies the L1 must close (not my write scope)

1. **Land the round-40 snapshot dir** as `corpus/source-snapshots/round-40/{S016,S017,S019}.txt` plus `manifest.json` containing those three records. Every entry's `recheck:` names that manifest; before it exists the line exits 2 (V5) and recheck-audit reports `paths_fail=3` (V6). If the L1 names the snapshots differently, the three `recheck:` lines and the `source:` capture paths must be updated in the same commit.
2. **`corpus/instruments/knowledge-expected.txt` must gain exactly the three landed paths**, else `recheck-audit` prints `unexpected=3` and exits 1 (V6, measured). Messaged to `ExecHarnessUpdate` with the three names and shas.
3. **`corpus/SOURCES.md`** rows S016/S017/S019 `used-by` cells must point at the three paths (messaged to `ScribeRows`; it had already fixed the same three names).
4. **Manifest record shape**: the scouts' S016/S019 records carry extra fields (`files`, `status`, `size_bytes`) that committed records elsewhere do not; assembling them verbatim still passes source-recheck (V3), so this is informational, not a blocker.

## 5. Findings

- **F1 (limit, not defect).** S019's captured source is the CSRC landing page; the 800-216 recommendations are in a PDF that no seat captured. The entry is honest and useful at the abstract/publication-record level but cannot carry clause-level ground. If the round wants clause-level NIST ground, that is a new capture (PDF) in a later round, not a correction of this entry.
- **F2 (verified instability).** Anthropic's page returns a different footer sentence between two fetches about a minute apart (my 21:16:37Z body vs the scout's 21:15:52Z body) while the policy lines L5–L17 are stable; my `verified-at:` discloses this instead of claiming a byte-identical reproduction.
- **F3 (date granularity).** S019 carries three date facts with two granularities — `Date Published: May 2023` (L74), `Planning Note (05/24/2023)` (L75), Document History `05/24/23: SP 800-216 (Final)` (L97). The registry row's `2023-05-24` is the Document History reading; the entry says which field any day-level citation came from.
- **F4 (multi-occurrence quotes are normal for abstract captures).** Six of S019's fourteen spans occur 2–3 times (L80 full abstract, L81 truncated copy, L83 repeat under "See full abstract"). They are anchored, the instrument accepts them (`occurrences=2 anchor=80-ok`), and the entry says so rather than quoting a shorter unique fragment to look cleaner.
- **F5 (attribution trap avoided).** An early draft of the S017 entry attributed "an upstream fix is not downstream evidence" to S018; `grep -n 'upstream fix'` on the S018 capture returns nothing, so the sentence now cites the lane's own F06 teaching cell (`corpus/README.md:207`) and anchorcheck confirms that line.

## 6. Scratch, tooling, disk

- Scratch `S=/fast/scratch/hyaku/kasegi-r40/ScribeEntriesG1` held the raw fetches, normalized copies, candidate-quote validator, entry drafts, scratch manifest and the audit mirror; it is removed after this receipt and the deliverables were copied out. No `kasegi-r39*` or sibling `kasegi-r40*` path was created by me.
- Disk guard before the pass: `/fast/scratch/hyaku` 27% used, 591.2G free — green.
- Tool installs: none (no pacman, no `uv`/`npx`/binary installs). Instruments used were the lane's own committed ones, read-only.
- Writes outside `wave1/`: none. `git -C <lane> status --porcelain` shows only the pre-existing untracked round-40 wave artifacts.
