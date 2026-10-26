# ScribeEntryF17 — F17 knowledge entry (Immunefi VSCS v2.2, S051)

Seat: scribe, wave-1, round 34. Lane base `014ee2d7aa8c3c095ff57ae51097606a9906228c`, claims freeze
`29f606dbdd28aff6fd4573ab4b90788bbb90af13`. Produced exactly one product file and this receipt; no
instrument, registry, README, QUALITY, SCORECARD, LOG or lesson edit; no commit; no subagent; no write
outside `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## Report

### Artifact

`corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && wc -l -c corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
  113 11143 corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md      (limit: Total <= 120 lines)
$ sha256sum corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a
```

Header (lines 3-6 verbatim):

```
source: S051 — https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/ — page heading “Immunefi Vulnerability Severity Classification System - v2.2” (S051.txt:45; document title tag L1), the five-level statement and its list (L46-51), the criterion sentences (L52-56), and the Smart Contracts table (L72-96) in capture corpus/source-snapshots/round-34/S051.txt
verified-at: 2026-10-26
ground: F17
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051   # 18 assertions (Q1-Q18) on the pinned capture, each `occurrences=1` or anchored (Q9/Q17); exits 2 with no capture or manifest and 1 on a quote that moved, so a missing or corrupted source fails closed; a captured-source comparison, not a fresh network verification
```

Sections: Attribution; Claim 1 (five numbered levels, three per-asset-class tables); Claim 2 (level fixed
largely by impact, likelihood an input); Claim 3 (consequence focus + downgrade-or-reject carve-out);
Claim 4 (Smart Contracts Critical enumerated list); Claim 5 (whose funds / how long frozen); Claim 6 (an
impact belongs to one asset class); Claim 7 (Medium/Low operational and value-preserved; None = best
practices); Honest limit (4 items); Falsifiable checks FC-1…FC-7; Rejected over-generalizations 1–6;
What this adds beyond F13/F15; Scope and limits.

### Pins this entry rests on (read, not written, by this seat)

```
$ wc -l -c corpus/source-snapshots/round-34/S051.txt
  175 8502 corpus/source-snapshots/round-34/S051.txt
$ sha256sum corpus/source-snapshots/round-34/S051.txt
4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5
$ sha256sum corpus/source-snapshots/round-34/manifest.json
d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe    (as restored by ExecSnapshotR34; see finding F4)
```

`manifest.json` record `S051`: `path: S051.txt`, `url: https://immunefi.com/immunefi-vulnerability-severity-classification-system-v2-2/`,
`fetched_utc: 2026-10-26T05:31:10Z` (strict UTC), 18 quote assertions `Q1`–`Q18`. I wrote neither file;
the capture and manifest are ExecSnapshotR34's, and the quote set is the one I sent it (message of
2026-10-26, "ScribeEntryF17 here … S051.txt landed") with the two corrections it applied (`Q5 anchor=53`,
`Q6 anchor=55`, `Q2` no anchor, `Q9 anchor=77`, `Q17 anchor=96`).

### Q1-Q10 mapping, with the check that shows it

| criterion | how this entry satisfies it | evidence |
|---|---|---|
| Q1 | H1 title; three header lines directly under it: `source:` = row id + URL + line anchors, `verified-at: 2026-10-26`, `recheck:` = one runnable command | entry lines 1-6; `grep -cE '^source: S051 '` → `1`; `grep -cE '^verified-at: 2026-10-26$'` → `1` |
| Q2 | every load-bearing claim rests on tier-A row S051, the row registered this round | entry cites only `S051` (`grep -oE '\bS[0-9]{3}\b' entry \| sort -u` → `S051`) |
| Q3 | 18 verbatim quotes, each ≤20 words (max Q3 = 20), each with its capture line; numbers copied from the capture, every count measured | see "FC counts" below; word counts printed by the manifest check |
| Q4 | attribution kept to Immunefi; three explicit disclaimers (not CVSS, not a payout scale, not binding on others) | entry § Attribution; § Claim 1 "within its own asset class" |
| Q5 | 7 falsifiable rules (FC-1…FC-7) + 6 rejected over-generalizations, each with its reason and a count or line | entry §§ Falsifiable checks, Rejected over-generalizations |
| Q6 | documentation only: no probing/submission instruction, no credential, session or private URL | `grep -nEi 'password\|passwd\|secret\|token\|api[_-]?key\|bearer\|session\|cookie\|BEGIN [A-Z ]*PRIVATE\|op://\|vault://'` → 3 hits, all benign: the words `session`/`token` inside prose and inside the quoted bullet `lack of token funds` (L64). No credential value, no URL beyond the public page URL |
| Q7 | one executable command, human note after `#`; output names what it checked; fails closed on missing/corrupt source | `bash -n` → 0; recheck → exit 0 with `S051:sha256 OK` + 18 assertion lines; controls A-D below |
| Q8 | quoted text is the page's text; where the extractor wrapped a sentence the assertion declares normalization | `S051:Q2/Q5/Q6 OK normalized=markup-whitespace` in the recheck output |
| Q9 | `path` stem equals id (`S051.txt`), quote exactly-once or anchor-verified, occurrence count printed | `S051:Q1…Q18 OK occurrences=…` (16× `occurrences=1`, `Q9`/`Q17` `occurrences=2 anchor=N-ok`) |
| Q10 | one command, `cd <lane-root> &&` prefix, parses under `bash -n`, runs from any cwd | `bash -n` replay of the extracted command → exit 0 |

### Recheck, run on the final bytes

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py \
    --manifest corpus/source-snapshots/round-34/manifest.json --source S051
S051:sha256 OK
S051:Q1 OK occurrences=1 anchor=46-ok
S051:Q10 OK occurrences=1 anchor=79-ok
S051:Q11 OK occurrences=1 anchor=83-ok
S051:Q12 OK occurrences=1 anchor=88-ok
S051:Q13 OK occurrences=1 anchor=92-ok
S051:Q14 OK occurrences=1 anchor=94-ok
S051:Q15 OK occurrences=1 anchor=90-ok
S051:Q16 OK occurrences=1 anchor=95-ok
S051:Q17 OK occurrences=2 anchor=96-ok
S051:Q18 OK occurrences=1 anchor=99-ok
S051:Q2 OK normalized=markup-whitespace occurrences=1
S051:Q3 OK occurrences=1 anchor=52-ok
S051:Q4 OK occurrences=1 anchor=52-ok
S051:Q5 OK normalized=markup-whitespace occurrences=1 anchor=53-ok
S051:Q6 OK normalized=markup-whitespace occurrences=1 anchor=55-ok
S051:Q7 OK occurrences=1 anchor=74-ok
S051:Q8 OK occurrences=1 anchor=75-ok
S051:Q9 OK occurrences=2 anchor=77-ok
exit 0    (19 `OK` lines = 1 sha256 + 18 assertions; zero non-OK lines)
```

`recheck:` line parses (command extracted by stripping the `   #` note):

```
$ bash -n recheck.sh
exit 0
```

### Fail-closed controls (scratch copies; the repo files were only read)

Scratch `/fast/scratch/hyaku/kasegi-r34/ScribeEntryF17/ctl/`, holding a copy of `S051.txt` and a copy of
the manifest with `path` reduced to `S051.txt`:

| control | mutation | command output | exit |
|---|---|---|---|
| A | bytes unchanged | last line `S051:Q9 OK occurrences=2 anchor=77-ok` | 0 |
| B | capture removed | `S051:source UNAVAILABLE reason=missing` | 2 |
| C | one byte appended | `S051:sha256 MISMATCH expected=4fd8ed98… actual=96fdb136…` | 1 |
| D | assertion `Q10` reworded to `Miner-extractable value (MEVX)` | `S051:Q10 MISMATCH reason=quote-not-found` | 1 |

Control D's first replay was piped into `grep` and reported `exit=0` — that was the pipeline's exit, not
the instrument's; the unpiped replay above prints `exit=1`. Recorded because it is the kind of
measurement error this lane files as a mistake, and it is not used as evidence here.

### Entry-to-manifest binding

```
$ python3 - <<'PY'   # frontier-recheck-count.evaluate(root, "knowledge/immunefi-vscs-v2-2-smart-contract-severity.md")
contract status=PASS problems=[] exit=0
manifest_assertions=18 entry_missing=[]      # every one of the 18 assertion quotes occurs in the entry
```

`declared_ids=['S051']`, `recheck_ids=['S051']`, `manifest=corpus/source-snapshots/round-34/manifest.json`,
so harness limbs A (header set = recheck set), B (manifest lists S051), C (`source-recheck.py` with
`--manifest` + `--source`, no `--selftest`) and D (line exits 0) all hold for this entry.

`python3 corpus/instruments/frontier-recheck-count.py` could not count this entry while `corpus/README.md`
had no F17 row — it read 16 admitted rows and evaluated none of them to this file. That was finding F2, not an
entry defect; the row has since landed (next block).

### Harness, run after the F17 row landed in `corpus/README.md`

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/frontier-recheck-count.py
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
entries=20 pass=20 exit=0
exit 0
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md
17
```

Earlier, with 16 frontier rows, the same harness could not reach this entry; that gap is finding F2 below and
has since been closed by another seat (not by me).

### FC counts, each measured on the pinned capture

```
$ S=corpus/source-snapshots/round-34/S051.txt
grep -cE '^[1-5]\. (Critical|High|Medium|Low|None)'  -> 15      (FC-1; 3 tables x 5)
grep -cE 'Severe|Moderate'                            -> 0       (FC-1)
grep -c 'v2\.2'                                       -> 2       (FC-2; L1, L45)
grep -c 'v2\.3'                                       -> 0       (FC-2)
grep -c 'CVSS'                                        -> 0       (FC-3)
grep -c 'reward'                                      -> 0       (FC-4)
grep -c '\$'                                          -> 0       (FC-4)
grep -c 'Permanent freezing of funds'                 -> 2       (FC-5; L62, L77)
grep -c 'Temporary freezing of funds'                 -> 1       (FC-5; L88)
grep -c 'Execute arbitrary system commands'           -> 1       (FC-6; L99)
grep -c '1. None- Best practices'                     -> 2       (FC-7; L71, L96)
```

Each of those numbers is printed in the entry next to the command that produces it.

### Findings for the L1 (I am not judging the round)

**F1 — the briefed content item "programs specify which version applies (v2.2 vs v2.3)" has no support in
the capture.** `grep -c 'v2\.3' S051.txt` → `0`; `v2.2` occurs only at L1 (document title tag) and L45 (page
heading). The capture is a single page for one version and prints no rule that a programme selects it. I did
not write the claim: the entry records it as an honest-limit item ("No version-selection statement … recorded
as an open item, not as a finding"). The lesson/scorecard should not state that this entry carries the
v2.2-vs-v2.3 selector. If the lane wants that claim, it needs a second capture (a programme page or the v2.3
classification page) and a second registry row — not a re-reading of S051.

**F2 — no wave-1 seat's prompt owns the `corpus/README.md` F17 row; it landed anyway.** I searched all 65
prompts in `.ufo/waves/round-34/wave1-spec.json` for a line containing `corpus/README.md` together with
`row`/`admit`/`F17`: 0 hits, and ExecHarnessAfter reached the same conclusion independently and asked me; I
answered that the row is not mine. While this seat ran, the row appeared: `grep -cE '^\| F[0-9]+ \|'
corpus/README.md` → `17`, with the entry cell `knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`, and
the harness then printed `PASS F17 … ids=S051` inside `entries=20 pass=20 exit=0`. So the gap I flagged is
closed, by a seat whose brief does not name it — worth an L1 look, because an orphaned integration step that
happens to be picked up is one that can also be missed.

**F3 — the frozen C2 predicate's literal wording collides with two anchored assertions.** C1/C2 phrase the
capture check as "every assertion occurrences=1"; with the printed bullets restored, manifest Q9 and Q17
print `occurrences=2 anchor=N-ok` (both strings are genuinely printed twice in the capture: L62/L77 and
L71/L96). `source-recheck.py` B2 admits that shape and exits 0, and the lane's own precedent is the same
(round-30 `manifest.json`: `S047:Q1 OK occurrences=3 anchor=123-ok`). An intermediate manifest revision
(`3e726d84…`) made both unique by widening the quotes across a line break — Q17 then read
`1. None- Best practices Websites and Apps`, merging a table row with the next section heading — and I asked
for the real bullets back rather than quote the extractor. The claims are frozen, so I did not edit them; the
L1 can either read the predicate as "unique or anchor-verified" or append the correction to QUALITY R20/R21.

**F4 — the manifest digest moved three times while I worked** (`72bac252…` → `3e726d84…` → `d5077f81…`). The
entry therefore pins the capture's sha256 and names the manifest by path plus its assertion count, and does
not repeat a manifest digest — a later manifest edit cannot make the entry's text stale. Every quote is
entry-bound at `d5077f81…` (`entry_missing=[]`).

**F5 — the entry will go stale by construction if the capture is re-fetched.** Its header anchors (L1, L45,
L46-51, L52-56, L72-96) and the FC counts are derived from the 175-line text extraction. A re-capture changes
line numbers even if the page's words do not; that re-pin is a new round's work, and the `recheck:` line
fails closed (sha256 mismatch) until it is done.

### Out of scope / not done (by design)

- No edit to `corpus/SOURCES.md` (S051 row is ScribeSOURCESRow's draft + ExecRegistryAppend-2's append; I
  pinged ExecRegistryAppend-2 that the used-by path now exists), `corpus/README.md`, `corpus/QUALITY.md`,
  `SCORECARD.md`, `LOG.md`, the lessons, `capture-binding-check.py`, `r-defect-closure.sh`,
  `kill-rule-check.py`, `frontier-recheck-count.py`, the capture or the manifest.
- No commit, no `git add`, no jj mutation; the L1 commits. No subagent, no `agent://all`.
- No tool installed or upgraded this round (nothing was needed).

### Scratch

`/fast/scratch/hyaku/kasegi-r34/ScribeEntryF17/` (created for `recheck.sh`, the recheck output and the
control fixture) and a one-line `/dev/shm/rc.sh` used for the first `bash -n` replay — both removed before
this seat ends; nothing of mine remains on disk outside the lane repo.

Peers contacted (all by id, no broadcast): ExecSnapshotR34 (quote list + two anchor corrections + the
restore decision), ExecHarnessAfter (entry path, capture/manifest state, README-row gap),
ExecRegistryAppend-2 (entry on disk at the used-by path), RevEntryF17 (final bytes, digest, unbound-quote
disposition at the time, v2.3 handling).

### Non-author review (appended after this seat's first yield)

`RevEntryF17` returned **ADMIT** on `948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a`
(113 lines — the bytes on disk, re-hashed here after the verdict: unchanged). Its receipt is
`.ufo/waves/round-34/wave1/RevEntryF17.md`; per its message it measured Q1-Q10 all PASS, 16/18 quotes
exactly-once at the cited line, 2 two-line spans verifying across L53-54 and L55-56, the joined level-name
sequence per line L47-51, the two `occurrences=2` bullets via anchors 77-ok / 96-ok with the multiplicity
disclosed in my Scope section, all 11 FC counts reproduced, the recheck line running verbatim from `/tmp` at
exit 0 (19 OK lines) and a missing-manifest control at exit 2, all 18 manifest assertion quotes verbatim in the
entry, and the S051 tier-A row present. It instructs no byte change, so I made none.

Its two non-blocking notes, carried here for the L1: (1) the digest announced mid-wave (`e71fbcd9…`) was
superseded by a manifest restoration and must not be used — the ADMIT binds `948b202e…` only, and the committed
bytes should hash to that; (2) the occ=2/anchor rides are conformant but fail closed on any re-capture that
shifts L77/L96, which is the intended behaviour and matches finding F5.

Report: .ufo/waves/round-34/wave1/ScribeEntryF17.md
