# ScribeLogR30 — round-31 seat receipt

Assignment: own `LOG.md` only, append-only; land the missing round-30 entry routed as defect 2 of
`corpus/lessons/round-30-verifier-spotcheck.md` §5 ("Land the missing round-30 `LOG.md` entry
(append-only; name the superseded absence)"). Leaf seat, no delegation.

Answering model: `devin/deepseek-v4-1-flash` (harness-provided model string; no model passed by this
seat). Tooling: nothing installed or upgraded; no pacman transaction attempted (host-wide pause).

## 1. Pre-state — the absence, verified

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git rev-parse HEAD
8a8916c7043bd873d191b30dd1744b241b91f4d9
$ grep -n -i 'round 30\|round-30\|r30' LOG.md
(no output; exit 1)
$ git log --oneline -3 -- LOG.md
0ab8929 round-29: land C1 selftest completeness/hermeticity + C2 F13 assimilation (v2 wave 64 seats)
1265fe1 round-28: anchorcheck fail-closed, F12 admission, source and lesson evidence
c2ab51d round-27: freeze C1/C2 claims with pre-freeze fixtures and before-receipts; operator wrap-up lands honest stop (no waves, claims NOT VERIFIED); lesson M27-1/M27-2, LOG, SCORECARD
$ grep -n '^## ' LOG.md | tail -3
1338:## Round 28 — 2026-10-25 — anchorcheck gate soundness + F12 Japanese state-coordinated disclosure workflow (one v2 wave, 69 seats)
1404:## Round 29 — 2026-10-25 — anchorcheck selftest completeness/hermeticity + F13 program-severity assimilation (one v2 wave, 64 seats)
$ sha256sum LOG.md ; wc -l LOG.md
0a1865e90f29c5d4a20fa3fda8f9daf6b6293bbec95710bafcda0cf65d537221  LOG.md
1467 LOG.md
$ tail -c 220 LOG.md | od -c | tail -2
0000300   u   s   a   l   s       w   i   t   h       f   l   i   p
0000320   c   o   n   d   i   t   i   o   n   s   .  \n
```

So the round-29 close-out bullet was the last byte of the file and no round-30 heading existed.
Heading/field shape copied from the round-29 entry (`## Round <n> — <date> — <title> (one v2 wave, N
seats)`, a frozen-claims paragraph, per-claim bullets with Before/After/Verdict, assimilation gate,
registry/no-harm, waves, tooling, plus a close-out section).

## 2. Evidence read for the entry (all committed bytes, no memory)

- `corpus/lessons/round-30.md` (118 lines) — frozen claims, landed changes, Gate, registry deltas,
  M30-1…M30-5, close-out ledger, close-out erratum (landed hashes, B2 caveat, ledger recheck
  correction, residual LOG-editor failure).
- `corpus/lessons/round-30-verifier-spotcheck.md` (71 lines) — §1 conformance table, §2 C1/C2
  re-check, §3 discernment sample, §4 trend verdicts, §5 five routed defects.
- `SCORECARD.md:784-835` — round-30 claims table, B2 fixture note, the stale recheck-audit paragraph,
  capabilities/saturation, move-log rows.
- `.ufo/waves/round-30/claims.json` — `frozen_at_utc` `2026-10-25T18:55:00Z`, base `a9487131…`,
  C1/C2 predicate sentences and counter commands.
- Committed receipts `.ufo/waves/round-30/{c1-controls/,c2-controls/before.txt,census-before.txt,
  harness-after.txt,post-commit-recheck-output.txt,wave1/}`.

## 3. Hashes and ancestry verified now

```
$ for h in 5703f9fbf70ba0717e5c6890f4c338cd5be00b7b 6262daca0feab0ea7a8672cef0398b0754f38f47 bc1a1e140914e65673daa586232128c964216ceb; do git cat-file -e "$h^{commit}" && echo "present $h"; done
present 5703f9fbf70ba0717e5c6890f4c338cd5be00b7b
present 6262daca0feab0ea7a8672cef0398b0754f38f47
present bc1a1e140914e65673daa586232128c964216ceb
$ for p in "5703f9f 6262dac" "6262dac bc1a1e1" "bc1a1e1 HEAD"; do set -- $p; git merge-base --is-ancestor "$1" "$2" && echo "ancestor $1 -> $2"; done
ancestor 5703f9f -> 6262dac
ancestor 6262dac -> bc1a1e1
ancestor bc1a1e1 -> HEAD
$ git log -1 --format='%h %an %ad %s' --date=iso 5703f9fbf70ba0717e5c6890f4c338cd5be00b7b
5703f9f kasegi-shokunin 2026-10-25 15:58:28 -0300 round-30: C1 instrument conformance + C2 F14 assimilation
$ git log -1 --format='%h %an %ad %s' --date=iso 6262daca0feab0ea7a8672cef0398b0754f38f47
6262dac kasegi-shokunin 2026-10-25 16:00:17 -0300 round-30: record final post-commit recheck
$ git log -1 --format='%h %an %ad %s' --date=iso bc1a1e140914e65673daa586232128c964216ceb
bc1a1e1 kasegi-shokunin 2026-10-25 16:00:46 -0300 round-30: final close-out errata and gate evidence
```

`bc1a1e1` is exactly the tip the round-30 verifier recorded (`corpus/lessons/round-30-verifier-spotcheck.md`
header: lane tip / pushed master).

## 4. Checks re-run now (quiescent committed bytes)

Instruments were deliberately NOT executed: round 31 assigns `recheck-audit.py` (ExecRALimbs),
`source-recheck.py` (ExecSRLimbs) and `frontier-recheck-count.py` (ExecFRLimbs) to live executor
seats, so a lane run now measures in-flight bytes and is non-comparative (bound 6 / M30-3). The
after-state in the entry therefore rests on committed receipts. Structural counts were taken from
`bc1a1e1` blobs, and the census from a `git archive` export.

```
$ git status --porcelain | grep -v '^??'
 M .ufo/waves/round-31/build-spec.py
$ git status --porcelain corpus/
?? corpus/instruments/limb-mutation-check.py
?? corpus/source-snapshots/round-31/
$ git show bc1a1e1:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
47
$ T=$(mktemp -d) && git archive bc1a1e1 corpus | tar -x -C "$T" && bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$T/corpus/SOURCES.md"; echo "census_exit=$?"
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/tmp/tmp.L68i0sbPY6/corpus/SOURCES.md
census_exit=0
$ git show bc1a1e1:corpus/README.md | grep -cE '^\|.*admitted'
14
$ git grep -lE '^source: S04[6-7] ' bc1a1e1 -- corpus/knowledge | wc -l
1
$ git grep -lE '^source: S04[6-7] ' bc1a1e1 -- corpus/knowledge
bc1a1e1:corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md
$ for f in corpus/instruments/frontier-recheck-count.py corpus/instruments/source-recheck.py corpus/source-snapshots/round-30/manifest.json corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md; do echo "$(git show bc1a1e1:$f | sha256sum | cut -d' ' -f1)  $f"; done
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f  corpus/instruments/source-recheck.py
dfc8835750bbdcbc2480fc579f7204ba8215d3018d0bd0942e4ea97f3e5e75a6  corpus/source-snapshots/round-30/manifest.json
f584f06c74942a36d9bce6bb97adcb7ab3bd1b2b0503faf8a68d5c60f4494a32  corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md
$ git show 6262dac:.ufo/waves/round-30/post-commit-recheck-output.txt | grep -E 'entries=|_exit='
entries=1 pass=0 exit=1
a1_exit=1
entries=2 pass=2 exit=1
a2_exit=1
b1_exit=1
b2_exit=1
census_exit=0
entries=17 pass=17 exit=0
harness_exit=0
recheck_exit=0
post_commit_recheck_exit=0
$ git show 6262dac:.ufo/waves/round-30/post-commit-recheck-output.txt | tail -25
PASS     F10  knowledge/vendor-disclosure-policy-commitments-crosswalk.md ids=S036,S038,S039,S040 exit=0
PASS     F11  knowledge/iso-29147-and-30111-division-of-labour.md  ids=S041           exit=0
PASS     F11  knowledge/iso-29147-divergence-and-clause-crosswalk.md ids=S041           exit=0
PASS     F12  knowledge/japanese-domestic-disclosure-workflow.md   ids=S041,S042      exit=0
PASS     F13  knowledge/program-severity-ladders-and-reward-scales.md ids=S043,S044,S045 exit=0
PASS     F14  knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0
entries=17 pass=17 exit=0
harness_exit=0
S046:sha256 OK
S046:Q1 OK occurrences=1
S046:Q2 OK occurrences=1
S046:Q3 OK normalized=markup-whitespace occurrences=1
S046:Q4 OK normalized=markup-whitespace occurrences=1
S047:sha256 OK
S047:Q1 OK occurrences=3 anchor=123-ok
S047:Q2 OK occurrences=1
S047:Q3 OK occurrences=2 anchor=130-ok
S047:Q4 OK occurrences=1
S047:Q5 OK occurrences=1
S041:sha256 OK
S041:Q1 OK occurrences=1
S041:Q2 OK occurrences=1
S041:Q3 OK occurrences=1
recheck_exit=0
post_commit_recheck_exit=0
$ git grep -n 'strict pass=43/43' bc1a1e1 -- .ufo/waves/round-30 | head -10
bc1a1e1:.ufo/waves/round-30/wave1/ConnClaims.md:237:   This immediately flips `recheck-audit.py` from `strict pass=42/43 exit=1` to `strict pass=43/43 exit=0`.
bc1a1e1:.ufo/waves/round-30/wave1/ExecDensityNoHarm.md:62:| recheck-audit.py | strict pass=43/43, cdroot_fail=0 instrument_fail=0 own_fail=0; executes=19 gated=24 broken=0; lines=43 total=43 pass=43 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0; `expect=present expected=43 missing=0 unexpected=0 exit=0` | green on both sides (expected list regenerated 41 → 43 entries to match the two new entries; documented R6/round-29 append pattern) |
```

The temp export `/tmp/tmp.L68i0sbPY6` is scratch outside the lane and was removed after the run
(`rm -rf /tmp/tmp.L68i0sbPY6`); the reproducible command is the `git archive bc1a1e1 corpus | tar -x`
line above. Every digest above equals the string the committed lesson and SCORECARD carry
(`aa60b581…`, `33602a9d…`, `dfc88357…`, `f584f06c…`), so the committed claims are bound to the
committed bytes, not to a retyped number.

## 5. The append

One append edit at EOF through the `edit` tool, anchored on the unique last line
(`grep -c 'flip conditions' LOG.md` → 1), after re-reading the file tail immediately before the
edit. Content: heading `## Round 30 — 2026-10-25 — instrument conformance (frontier
missing-entry/duplicate, source stem/occurrence) + F14 Japanese severity vocabulary assimilation (one
v2 wave, 64 seats)`; an explicit late-append disclosure (round-31 seat, model, the `#B26C`/`#114E`
editor failure, the superseded absence at HEAD `8a8916c`, spotcheck §5 defect 2); the frozen-claims
paragraph with base, freeze commit, dispatch commit, landed `5703f9f`, evidence `6262dac` and
verifier tip `bc1a1e1`; C1 and C2 bullets with before/after/verdict as the committed bytes show,
including the preserved M30-1 B2 caveat; the assimilation gate (S049→S046, S050→S047, S043→S041,
three refusals, seven quarantine verdicts); registry 45→47 and the no-harm boundary; the wave shape
and the missing `wave1-results.json`/`WAVE-DONE`; the verifier conformance summary; tooling; then a
"checks re-run for this append" section with the commands in §4, an explicit non-comparative
boundary for the instruments, and the still-open routed defects 1/3/4/5.

Two follow-up edits inside my own new block only (no pre-existing byte touched): the receipt-grep
bullet was made precise about the negative-control block that precedes the after state, and the
boundary bullet was restated as "round 31 assigns these instruments to live executor seats" instead
of claiming unobserved mid-edit bytes. A third follow-up edit restated the check-provenance sentence
so it says the counts come from `bc1a1e1` blobs rather than from a working tree that other seats were
starting to modify.

## 6. Append-only verification (final bytes)

```
$ git diff --stat LOG.md
 LOG.md | 115 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 115 insertions(+)
$ git diff -U0 LOG.md | grep -c '^-[^-]'
0
$ git diff --numstat LOG.md
115	0	LOG.md
$ git diff -U0 LOG.md | grep '^@@'
@@ -1467,0 +1468,115 @@ labelled PENDING until the L1's close re-run records it.
$ git show HEAD:LOG.md | sha256sum
0a1865e90f29c5d4a20fa3fda8f9daf6b6293bbec95710bafcda0cf65d537221  -
$ head -c $(git show HEAD:LOG.md | wc -c) LOG.md | sha256sum
0a1865e90f29c5d4a20fa3fda8f9daf6b6293bbec95710bafcda0cf65d537221  -
$ sha256sum LOG.md ; wc -l LOG.md
864deb7df810539d3a92a9c520c94e218836233da42378ba774e48bbf339cf1b  LOG.md
1582 LOG.md
$ grep -n '^## ' LOG.md | tail -1
1469:## Round 30 — 2026-10-25 — instrument conformance (frontier missing-entry/duplicate, source stem/occurrence) + F14 Japanese severity vocabulary assimilation (one v2 wave, 64 seats)
$ tail -c 60 LOG.md
AVE-DONE` (item 5). This entry closes only the LOG absence.
```

- Additions only: 115 insertions, 0 deletions, a single hunk starting at old line 1467 with zero old
  lines (`-1467,0`), i.e. pure EOF append.
- The first 1467 lines are byte-identical to `HEAD:LOG.md` (prefix sha256 equal).
- File ends with `\n`; no trailing-whitespace or CRLF introduced.
- Pre-append state for comparison: `0a1865e9…`, 1467 lines, last heading `## Round 29 …`.

## 7. Findings (conflicts reported verbatim, nothing relabelled)

- The absence was real and is now closed: round 30 had no LOG entry, and `git log -- LOG.md` last
  touched the file in round 29 (`0ab8929`). The entry names that absence as superseded rather than
  presenting itself as round-30-time work.
- Round-30 claim verdicts recorded as the committed bytes show: C1 **improved, score held 4** and C2
  **improved, score held 7**, with M30-1 (B2 fixture does not isolate its limb) preserved as an open
  caveat, not converted into a kill.
- The round-30 lesson's own hashes and digests are reproducible from `bc1a1e1` blobs today; no digest
  drift was found at the tip.
- Not closed by this append (owned elsewhere this round): routed defect 1 (8 untracked round-30
  leftovers), defect 3 (B2 fixture isolation), defect 4 (stale `SCORECARD.md` "recheck-audit open
  item … exit=1" paragraph — superseded by the erratum's `strict pass=43/43 … exit=0`), defect 5
  (missing `wave1-results.json`/`WAVE-DONE`, so executed role mix and dead-seat counts stay
  unavailable).
- Evidence boundary kept: instruments were not re-executed by this seat; no after number in the
  entry is presented as a fresh execution except the structural counts and the census listed in §4.

## 8. Touched surfaces / out of scope

- Written: `LOG.md` (append only, 114 lines added at EOF) and this receipt
  `.ufo/waves/round-31/wave1/ScribeLogR30.md`. No other lane file modified; `git status --porcelain`
  shows only this seat's `LOG.md` modification plus pre-existing round-31 untracked artifacts owned
  by other seats.
- No git/jj mutation (read-only `git log/show/diff/status/ls-files/rev-parse/cat-file/merge-base/
  grep/archive` only), no commit, no push, no lane index touch, no `jj` command.
- Nothing written outside the lane; `/home/vgpnk/Projects/shokuknow/` untouched and its tools never
  run; no network fetch, no live bounty-target contact, no credential material recorded.
- No tool installed or upgraded; no pacman transaction.
- Left in place, not mine: `corpus/lessons/` (round-30 lesson/spotcheck), `SCORECARD.md`,
  `SHONEN.md`, `claims.json`, the round-31 report — owned by other seats this wave.
