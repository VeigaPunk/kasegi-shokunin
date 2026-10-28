# RevLessonShape — round-42 lesson shape review (receipt-only)

Scope: read `claims.json`, `corpus/lessons/round-41.md` (122 lines) and `round-40.md` (286 lines) in full, plus
`round-41-verifier-spotcheck.md` §3/§5 and the r40/r41 suite code that parses lessons. No file was edited and no
suite was run. Scratch `/fast/scratch/hyaku/kasegi-r42/RevLessonShape` was removed on exit. Disk guard was green.

## Method (commands actually run)

- A line-anchored heading/census/Gate/dispatch-tally lint (Python, scratch only) over both lessons. Dispatch
  counts come from `.ufo/waves/round-{40,41}/wave{1,2}-dispatch.json` (`taskCall.tasks[].agent`, attack =
  reviewer+critic+mutation-tester):
  - r40: wave1 17/54, wave2 25/35.
  - r41: wave1 20/60, wave2 32/33.
- Raw findings from that run:
  - r40 line-anchored `^## Gate$` count = 2 (L29, L31). The bare substring `## Gate` occurs 4 times, because the
    appended Erratum quotes it in prose.
  - r40 census L27 matches `\+\d\?` (garbled `tier A +3?mined …`) with unbalanced parentheses.
  - r40 header L9 states wave 2 `33/35` and total `50/89`; dispatch gives 25/35 and 42/89.
  - r41 Gate has no `### Rejected` subsection and 0 reject bullets.
  - r41 header tally `20/60`, `32/33`, `52/93` matches dispatch (OK).
  - r41 quote span at L49-51 contains 6 `"` characters (nested quoting, details below).

## Structural defects the round-42 lesson MUST avoid

Each item gives the defect, the evidence, and the concrete rule for the r42 lesson.

### Carried from round 40 (all already routed in the r40 Erratum; r42 must not reproduce them)

1. **Duplicated `## Gate` heading** (r40 L29 and L31). Rule: exactly one line-anchored `^## Gate$`. Do not repeat
   the string in prose at line start, and prefer not to repeat it mid-line either. The r40 Erratum's own
   backticked "`## Gate`" inflates a naive substring count (4 vs 2 real headings), so any suite scan must be
   line-anchored.
2. **Garbled census line** (r40 L27: `tier A +3?mined S016/…, rejected …, carried … flips)`). The `(` was typed as `?`
   and the closing `)` is orphaned. Rule: every census line has balanced parentheses and no `?` placed where a
   delimiter belongs. Write counts as `registry 63 -> 64+R rows`. List `mined`, `rejected` and `carried` ids as
   separate plain clauses; do not nest them in a parenthetical.
3. **Stale or wrong attack-role tally** (r40 L9: `33/35 = 94%`, `50/89`; true 25/35 = 71.4%, 42/89 = 47.2%). The
   wave-2 figure counted the whole roster instead of attack roles. Rule:
   - derive attack/total per wave only from the committed `wave{1,2}-dispatch.json` roles (reviewer + critic +
     mutation-tester; scout, connector, sentinel and scribe are not attack roles);
   - the figure must equal the sum of the lesson's own role list (r41 did this correctly: 7+13+12 = 32/33);
   - write the tally once, in the header; round total = wave1 + wave2.
4. **Correct in place, do not append an erratum.** r40 and r41 each needed an `Erratum (round 41)` block because
   the first-landed text was wrong. r42's lesson is a new file at J, so every figure must be correct when
   first committed. A later erratum cannot mend a landed line, and the r41 suite's I4 only string-matches the
   erratum. Also note that `Correction`/`Erratum` blocks must land once (D-r41-1 duplicated 4 SCORECARD
   lines).

### Carried from round 41

5. **Gate lists no reject decision** (r41 L39-70: one admitted candidate, zero rejected; verifier D-r41-2). The
   outside spot-check could not sample the reject direction. Rule, per `claims.json` C2: the r42 Gate carries
   - a `### Rejected` subsection;
   - one bullet per screened-but-rejected S-row, S065 and up, each opening with the S-id and `REJECTED`
     (r40 L130-153 is the model: id, name, `REJECTED:` reason, `Flip:` clause);
   - for each rejected row, URL, access date and a located quote of at most 25 words, in the same Gate block
     (the r40 H4 block parser requires all of these; a block ends at a blank line or heading).
   Also list the screened-and-excluded leads, not only S064 and S065 (r41 search log said "screened 2, included 1",
   but the lesson recorded nothing for the excluded one).
6. **Quote typography defeats the existing span parser.** r41's located quote (L49-51) is a backticked span holding
   `"If a "security.txt" file … "/.well-known/" path MUST be used."`, i.e. six `"` characters. The r40 H4 reader
   (`/"[^"]{1,600}"/`) mis-pairs these as `"If a "`, `"file is present …"` and so on, so an automated limb cannot
   cleanly count the words of the intended span. Rule: pick a quote with no inner double quotes, or render inner
   quotes as `'…'`. Put each quote in exactly one `"…"` span of ≤25 words plus a location token (`L<n>` /
   `line n` / `§`), and count the words.
7. **Frozen vs measured conflated in the "Frozen claims" table** (r41 L21-24). The section says "as frozen" but the
   After cell mixes frozen predicate values with measured outcomes ("At the integrated probe ref … survive",
   "However, wave-2 … found …"). Rule:
   - the Frozen claims table carries only the `claims.json` before/after values, verbatim and unmodified;
   - add a separate `## Measured outcome` or `## Verdict` block (r40 L211+ and r41 L72+ pattern) for what
     happened;
   - verdict language is only "verified" or "not verified" with the firing clause named, never "held" without a
     reason. The r40 → r41 overclaim (M40-1/M41-1) was exactly a grade-versus-kill-rule mismatch.
8. **Mistakes table thin or unreflective of the round's actual defects.** Both lessons carry one row (M40-1, M41-1),
   yet the round-41 routed defects D-r41-1 (duplicated Correction blocks), D-r41-3 (SKILL.md split table +
   duplicate row), D-r41-4 (missing Stale-lane line) and D-r41-5 (0 connectors in wave 2) are self-defects with no
   row. Rule: every self-defect named in the verifier's §5 gets an `M42-n` row with class, evidence path, captured-by,
   fix and a failing-able test. `able to fail` must name a command that reds at base or Z.
9. **Missing Gate sub-blocks that r40 had and r41 dropped.** r40 carried Assimilation, a seam check (row ↔ entry ↔
   bound capture) and a Sourced claim. r41 had none, despite the frozen `assimilation/` dir existing for r42.
   Rule: keep `Assimilation` (id-collision rerun, quarantine, adopted/adoptable counts) and a seam-check line for
   S064 (`used-by` entry exists, entry `source: S064`, anchor names `round-42/S064.txt`, capture sha256 equals the
   manifest record). Put these inside the single `## Gate`, as `###` subsections.
10. **Receipt/hash ordering.** The lesson lands in J; Y = J + receipt only; the receipt cannot be named in J. r41
    appended a `Final Y measurement` section after Y (Z = lesson + LOG/SCORECARD/SHONEN), citing Y's hash and the
    receipt sha256. Consequences for r42:
    - the Y export does not contain any such section, so no J-suite check may depend on one (an `--export-ref Y`
      run would see the J-time lesson);
    - the lesson body must not contain J's hash (claims `judged_head_rule`; a commit cannot contain its own
      hash);
    - if the lesson names Y/J, it does so only as a post-Y Z-time appendix.
11. **Parked-topic hygiene.** F24 / RFC 9116 is PARKED (open L0 question). The r42 lesson must not mention it as a
    candidate, a reject, or a row source. It may refer once to the L0 question by id, without proposing the
    topic. The F25 Gate block and rejected rows must be disjoint from RFC 9116 ground; verify against the kake
    overlap lesson (r41 CritProvinceBoundary).
12. **Pending-text and placeholder scan.** r41's I11 uses `pending_scan` on the lesson:
    `(⟨|〈|<|\[\[)\s*pending` (case-insensitive) must be 0. The r42 lesson must contain no such marker, nor TODO or
    "filled by L1" text.
13. **Heading and fence hygiene.** Keep the r40/r41 section order — `Frozen claims`, `Mistakes`, `Census`, `Gate`,
    `Wave-2 falsification`, `considerthese`. The wave-2 section is written after the wave 2 lands. Every
    code fence opened in the lesson must close (the r41 `fence_eof` limb: EOF CLOSED).
14. **Census line must record both before and after, exactly as printed** (r41 L34 did this well): the `W04`
    lines, `ok`, exit code, plus a registry-row delta line with `63 -> 64+R`. Do not abbreviate to prose.

## One-line pre-landing lint the L1 can run (read-only)

```
f=corpus/lessons/round-42.md
[ "$(grep -c '^## Gate$' $f)" = 1 ]                          # no duplicate Gate
! grep -nE '\+[0-9]\?|\?[A-Za-z]' $f | grep -i census         # no garbled census punctuation
grep -q '^### Rejected' $f && grep -cE '^- \*\*S0(6[5-9]|[7-9][0-9]).*REJECTED' $f   # >=1 reject bullet, status + reason + Flip
! grep -iE '(⟨|〈|<|\[\[)[[:space:]]*pending' $f              # no pending marker
```
and an attack-tally check: recompute `a/n` per wave from `wave{1,2}-dispatch.json` roles and compare with the
header.

## Residual risk / gaps

- The reject-row regex above assumes the S065+ ids; adjust if the scout records the reject only as a lead-level
  row without a registry id (claims.json C2 wants status-rejected rows S065+, so the id form is expected).
- I did not run any r41/r42 suite code or any network fetch; the findings are from file reads and the
  line-anchored lint over committed lessons.
- Not examined: r42 wave-1 deliverables (none landed in `wave1/` at review time beyond `swarm-registry.json`).
