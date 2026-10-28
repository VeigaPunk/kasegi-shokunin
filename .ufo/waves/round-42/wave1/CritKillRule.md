# CritKillRule — round-42 kill-rule attack receipt

Axes judged: depth:verifiability (primary), coverage. Target: the F-* family enumeration inside the
frozen C1 kill_rule / predicate text at `.ufo/waves/round-42/claims.json` (frozen 2026-10-28T12:05:00Z).
The suite under attack (`corpus/instruments/r42-closure.sh`) is NOT committed at attack time —
`corpus/instruments/` newest closure is `r41-closure.sh` — so the strongest counterexample available
from local evidence is the enumeration's own verbatim wording run against the shipped r41 parser
family and the r41 wave-2 defeat artifacts it claims to repair. Every hole below is a defeat class
INSIDE one family's stated intent that the enumeration's named forms do not reach: a r42 check that
implements the enumeration literally accepts each listed input, and the kill clause then calls that
acceptance a repair.

Method: scratch `/fast/scratch/hyaku/kasegi-r42/CritKillRule` (removed before filing), no lane writes,
no git mutation, no installs, no network. Disk guard green at start. Read-only sources: claims.json,
`corpus/instruments/r41-closure.sh`, `capture-binding-check.py`, `frontier-recheck-count.py`,
`corpus/lessons/round-41-verifier-spotcheck.md` §5, `.ufo/waves/round-41/wave2/` defeat artifacts,
committed `Correction (round 41)` lines in SCORECARD.md / LOG.md / SHONEN.md.

## F-EVID (J1) — two verbatim holes

Enum verbatim: "every `Correction (round <n>)` line set in SCORECARD.md, LOG.md and SHONEN.md grades
the named overclaim not verified AND names each firing evidence identifier per-record, not as a union".

Hole 1 — "per-record, not as a union" does not name the union granularity. The r41 committed defeat
was a union across FILES; the enum closes exactly that shape but leaves the union across LINES inside
one file unnamed. The committed r41 state itself exhibits the surviving shape: in SCORECARD.md,
`Correction (round 41)` lines 1603, 1605, 1608, 1610 carry ZERO evidence identifiers while the file's
stem coverage comes from line 1602/1607 alone (measured: 14 lines across 3 records; stems-per-line
0,1 or 3 — never "each line names each stem"). If "record" = file, a r42 file with one rich line and
sparse sibling corrections is per-record-clean by the enum while most corrections carry no evidence.
Counterexample input: SCORECARD.md `Correction (round 42)` lines where the evidence identifiers live
on one line and three other corrections name none — rejected under the family's intent (per-correction
evidence), accepted under the enumeration (per-file union complete).
Hole 2 — "names each firing evidence identifier" requires a named STRING, not a named FIRING
identifier. r41's matcher is `qualified_corrections | grep -qF -- "$stem"` (r41-closure.sh:902-906): a
substring hit. A correction naming `MutSuite` (a real committed artifact, not the firing mutation),
or `CritKillRuleXYZ`, satisfies the string clause while no firing identifier is named. The enum also
never requires the identifier to resolve to a committed path — `wave2/Nonexistent.md` is a named
identifier. And "grades the named overclaim" binds no claim id or round: a correction grading the
wrong overclaim (e.g. C2 or a prior round) fits the shape while the actual overclaim stays uncorrected.
Impact: depth:verifiability (J1 false green; the correction ledger looks per-record-evidenced while
individual corrections are unbound).
Smallest safe correction: replace "per-record, not as a union" with "each `Correction` line names each
firing evidence identifier as a bounded token (no union at any granularity)" and require each named
identifier to resolve to a path committed at the judged ref; name the overclaim target (claim id +
round) the correction must grade.

## F-TOKEN (J2) — two verbatim holes

Enum verbatim: "a `closed=<n>/<m>` or `failures=<k>` value is read only as a whole token bounded by
non-digit, non-slash characters".

Mechanical comparison (verbatim transcription of r41 `value_present` vs the enum class `[^0-9/]`,
value `closed=13/13`):

    LINE                                         R41      ENUM
    closed=13/13 exit=0                          ACCEPT   ACCEPT
    closed=10/100 exit=1                         REJECT   REJECT   (named defeat, closed)
    xclosed=13/13 exit=0                         REJECT   ACCEPT   <- enum-only hole
    unclosed=13/13                               REJECT   ACCEPT   <- enum-only hole
    selftest.closed=13/13                        ACCEPT   ACCEPT
    closed=13/13.5                               ACCEPT   ACCEPT   <- hole both classes share
    closed=13/13-9                               ACCEPT   ACCEPT   <- hole both classes share
    closed=13/13/0                               ACCEPT   REJECT
    closed=13/130                                REJECT   REJECT
    closed = 13/13                               REJECT   REJECT
    closed:13/13                                 REJECT   REJECT

Hole 1 — key-side adjacency is wider under the enum than under r41. Any letter or identifier
character is "non-digit, non-slash", so `xclosed=13/13`, `unclosed=13/13`, `pre-closed=13/13` read as
the honest tally where r41's punct-class rejected them. A transcript whose real line is
`closed=10/13 exit=1` and which also prints `not-closed=13/13` (or `summary.closed=13/13`) yields the
honest token under the enum's boundary definition.
Hole 2 — punctuation-continued values are accepted by BOTH classes and the enum names nothing about
them: `closed=13/13.5` and `closed=13/13-9` present `closed=13/13` as a bounded token (`.`/`-` are
non-digit, non-slash). The enumeration names digit and slash adjacency only; field-continuation
punctuation (`. , : % - +` and the `'`/`"` wrappers, e.g. `closed='13/13'` — in-family: the enum's own
example `closed:13/13` shows separator spellings are intended members) escapes.
Impact: depth:verifiability — the J2 check validates a mangled tally as the round truth; same kill
class as the committed `closed=10/100` defeat.
Smallest safe correction: bound the value with `[[:space:][:punct:]]` minus the value-continuation
set AND bound the KEY `closed=`/`failures=` by a non-identifier character (start-of-line or
`[^A-Za-z0-9_.-]`), and require exactly one `closed=` occurrence per tally line so a shadowed second
token cannot satisfy the limb (occurrence selection is likewise unnamed by the enum).

## F-TABLE (J3) — three verbatim holes

Enum verbatim: "the Gates-and-probes table has no blank line between header separator and its last
row, no instrument basename appears in more than one row, and bare internal pipes /
leading-whitespace cells are rejected".

Hole 1 — the enumeration never requires the suite's row to exist, to sit inside a table, or the
table's header to name `name`. D-r41-3's repair target was registry INTEGRITY; r41 I7 required a
well-formed row inside a contiguous table (r41-closure.sh:1158-1190). Under the enum, a SKILL.md
whose only `r42-closure.sh` row is a mention-only orphan after prose — measured on a fixture:
blank-inside-interval=0, dup-basenames=0, no bare pipes — satisfies all three clauses. The T13
mention-only class, one of the two named r41 repair objects, survives the enumeration.
Hole 2 — "blank line" names only the strictly-empty line. A whitespace-only separator (`" "`, `"\t"`),
an `| |` empty row, an HTML comment, or any prose line splits the table identically (measured: a
`" "` line inside the header-separator..last-row interval leaves strictly-empty-inside=0 while two
pipe-rows follow the split). The enum's clause 1 is silent for every non-empty split line.
Hole 3 — `awk -F'|'` treats an escaped `\|` exactly like a bare `|` (measured NF: 10 vs 10 vs 11 on
near-identical rows). Nothing in the enumeration distinguishes them: an implementer counting cells
on `|` either inflates NF (a 2-cell row with `\|` masquerades as a 3-cell row — too-FEW cells escapes
a `NF>=8`-style limb) or rejects escaped pipes as bare ones. Either way the class is unnamed.
Impact: depth:verifiability (J3 green on a mention-only or ws-split registry) + coverage (the lane's
registry table is the sources ledger the C2 counting commands read).
Smallest safe correction: require "the suite's own basename appears in ≥1 well-formed row inside a
contiguous table whose header names `name`"; define table range as header-separator..last contiguous
`|`-row and require "no non-`|` line inside it" (not "no blank line"); parse cells on unescaped `|`
only and require the canonical cell count.

## F-DECL (J4) — two verbatim holes

Enum verbatim: "every round-N artifact path that a check reads is declared in declared-blocks.txt and
a path read outside the export root through a symlink is rejected".

Hole 1 — the outside-root enumeration names the symlink transport only. Measured on a fixture:
`realpath -m export/../outside/secret.txt` resolves outside the export root with NO link present
(direct `..` traversal — and r41's `path_safe` rejects `..` components, but the enum's clause names
symlinks, so a literal read declares the traversal out of scope). A hardlink inside the export tree
carries the outside file's inode while `[ -L ]` is false (measured: outside/export inodes equal).
Reads through `--work`/`$MUT`/`$SCRATCH_ROOT` are outside-root by design and unnamed.
Hole 2 — the declaration subject is "artifact path that a check reads", not the changed-path set. r41
CritDeclarationCoverage (committed, wave2) named the surviving gap verbatim: the validator checks
listed declarations and "never enumerates all paths changed between BASE_REF and REF". The enum's
wording preserves that hole exactly: an appended, never-read path is undeclared by construction and
no clause reaches it (the r41 run showed the aggregate catch reded only via the shared-declaration
mismatch, not via changed-set enumeration). Sub-file granularity is also unnamed: a declaration binds
the file's TAIL sha (r41 semantics); a content change above the declared window plus a line-count
bump keeps the tail-sha constant — a same-tail append-over-edit escapes.
Impact: depth:verifiability.
Smallest safe correction: name the transport class ("a read resolving outside the export root — by
symlink, `..` component, hardlink, or relative traversal — is rejected"; r41 already implements
`path_safe`+canonicalization, the enum just fails to say it) and require the declared set to equal
`git diff --name-status BASE..REF` minus a named exclusion list.

## F-SCAN (J5) — three verbatim holes

Enum verbatim: "the suite's scratch scan covers `kasegi-r4[0-9]*` prefixes and an
outside-configured-root stray under a seat-named dir is detected".

Hole 1 — `r4[0-9]` is a single-digit range. Measured against r41's normalization table:
`kasegi-r50`, `kasegi-r5x`, `kasegi-r4` (no second digit), `kasegi-r39` are all in-family scratches
the glob does not match. The enum enumerates rounds 40–49 only; a stray from round 50 or round 4 is
hygiene by the family's intent and unmatched by its glob.
Hole 2 — the enum names a case-sensitive glob. `KASEGI-R42-X`, `kasegi_r42` and `kasegi.r42`
normalize to the family under r41's `family_name` (measured r42fam:yes for each; enum glob: no) —
the r41 T14/H6 class — but the enum's literal prefix does not match them; the repair's class is
unnamed.
Hole 3 — "under a seat-named dir" binds detection to nesting. A stray file AT the scratch root
(`<root>/kasegi-r42-note.txt`) or under a non-seat-named dir is in-family and unnamed. The enum is
also silent on the work-ancestor exemption: a family stray sitting inside --work is never a stray by
construction.
Impact: depth:verifiability (J5/J13 quiescence silently green over residue).
Smallest safe correction: define the family by normalization, not glob — "any name that normalizes
(lowercase, separator-collapse, dot-strip) to `kasegi-r<digits>*`" — and drop the seat-dir qualifier
to "any leftover entry inside the suite's scratch root except the live work dir itself".

## F-BIND (J6) — verbatim hole

Enum verbatim: "capture-binding-check.py rejects a manifest record whose capture path is absent and
a record whose url field is mutated".

Live-instrument probe (`--root` on a scratch fixture registry+manifest+capture, real committed
checker at Z): a record whose `path` names an absent file still prints `records=1 bound=1 unbound=0`,
exit 0, once the abandoned capture is honestly declared as an orphan — `bound` never reads
`record.path` (capture-binding-check.py:283-305, 427-428, 435-444). The enum's two named mutations
are a strict subset of what `bound` can misstate. Verified mechanically, each still `bound=1
unbound=0`:
- `capture_url` mutated while `url` is intact — `bind_record` never reads `capture_url` (the enum's
  "url field" names the wrong/only field);
- `path` pointing at a PRESENT but different capture (`S888.txt`) — not an "absent" path;
- `path` pointing at an existing directory;
- `sha256`/`snapshot_sha256`/`full_text_sha256` mutated with path and urls intact — the real record
  carries three digests the binding never consults (round-41 manifest shape confirmed).
So a manifest whose record misstates the captured bytes' digest or binds a different file is "bound"
by the instrument and unenumerated by the family. Record-to-record identity swaps (two records each
naming the other's existing file) are the same class.
Impact: coverage (the S064 capture the C2 claim adds is checked by this very instrument) +
depth:verifiability.
Smallest safe correction: extend the family wording to "any record field that falsifies the
capture-binding (path absent/wrong-type/wrong-file, capture_url or url mutated, digest mutated,
record-swap)" or bind the record's content claims (digest vs file bytes) in the check itself.

## F-FLIP (J7) — two verbatim holes

Enum verbatim: "frontier-recheck-count.py exits nonzero when an admitted frontier row's PASS line is
absent or a row status flips".

Hole 1 — denominator mutations are neither named member. The committed r41 defeat (MutC2Chain A):
`admitted`→`explored` dropped F24 from `entries=` entirely — `entries=26 pass=26 exit=0`. The enum's
first member requires an ADMITTED row to lose its PASS line; the second requires the status cell to
flip. A row deletion, an ID re-key (`F24`→`F024`, which also escapes the `^\| F[0-9]+ \|` counting
regex), or a move of the row outside the counted region removes the row with NO status flip and NO
admitted-row PASS absence — the denominator shrinks silently. Paired mutation (`admitted`→`explored`
on one row + `explored`→`admitted` on another) preserves `entries=`/`pass=` and every admitted PASS
line while a status flip undeniably occurred — direction and identity are both unnamed by "a row
status flips".
Hole 2 — "PASS line" absence is counted, not authenticated: a `PASS F24` line whose `ids=` payload
points at the wrong source, or a PASS for a non-admitted row, is unenumerated.
Impact: coverage (the frontier counter is the C2 measure input) + depth:verifiability.
Smallest safe correction: require "exits nonzero whenever the admitted-row set loses a member (status
change, deletion, re-key, or PASS/absence by ID payload), including denominator-preserving swaps";
name the comparison basis (admitted-row ID set, not counts).

## Meta-hole A — the kill clause protects seven families; the predicate names nine

claims.json kill_rule verbatim: "within one of the seven named repair families F-EVID / F-TOKEN /
F-TABLE / F-DECL / F-SCAN / F-BIND / F-FLIP". The same predicate names family `F-RCPT` (J8: "family
F-RCPT: the Y receipt is the teed transcript … forged payload values are rejected") and family
`F-CORR` (J11: "no `Correction (round <n>)` block is duplicated verbatim"). A committed artifact at Z
showing the current suite accepting a forged-payload receipt (F-RCPT) or a whitespace-variant
duplicate correction (F-CORR — "duplicated verbatim" does not reach a near-duplicate, the exact
D-r41-1 repair's weakest wording) is IN-FAMILY for those named checks yet does NOT satisfy the kill
clause — under `claim_design_lesson` it is only a routed defect. Either the kill clause's enumeration
omits two families the predicate itself names (wording hole), or the freeze deliberately leaves the
receipt-integrity family — the r39–r41 failure site — outside the kill clause (a tradeoff the
verifier should be told is deliberate).

## Meta-hole B — "EVERY repaired check carries a REPLAY limb" vs kill clause's J1-J7 scope

The frozen summary (predicates + wave spec) says every repaired check's replay limb is required;
the kill_rule verbatim protects only "the committed replay limb of any J1-J7 check". A skipped or
absent replay limb on J8–J13 cannot kill. Same class as Meta-A: the enumeration overstates the
protected surface by five checks.

## Residual limits

The r42 suite bytes are absent at attack time, so each hole is demonstrated against the enumeration's
wording and the shipped r41 implementation family it repairs — the strongest committed
counterexample, per the design lesson. None of these are lane-state findings; they are wording holes
that become live escapes iff J1–J7 are implemented to the enumeration literally. J8 (F-RCPT) and J11
(F-CORR) in-family escapes are routed by construction and listed for completeness, not as kill
clauses.

## Commands run (all inside seat scratch)

- `bash tokendemo.sh` — verbatim r41 `value_present` vs enum `[^0-9/]` boundary class, 12 lines
  (output table above; `xclosed=`/`unclosed=`/`13.5`/`13-9` escapes shown).
- `bash tabledemo.sh` + `bash tabledemo2.sh` — NF inflation on `\|` (10 vs 11), blank vs
  whitespace-only split verdicts, orphan-row fixture: enum clauses all hold while the suite row is a
  mention-only line outside every table.
- `bash binddemo.sh` — real `capture-binding-check.py` over 6 scratch fixtures: M1 absent path,
  M2 capture_url-only mutation, M3 wrong-but-present path, M4 directory path, M5 mutated sha256 —
  every run `bound=1 unbound=0`; orphans undeclared cause exit 1 via orphan rule, not via the record.
- `bash binddemo2.sh` — missing-path record with honestly-declared orphan: `records=1 bound=1
  unbound=0 exit=0` (the instrument-side ground truth for the J6 limb).
- `bash scandemo.sh` — family normalization vs enum glob (11 entries) + hardlink/dotdot traversal
  fixture (`realpath -m export/../outside/secret.txt` escapes the root; hardlink shares the outside
  inode, `[ -L ]` false).
- `grep -n 'Correction (round 4[12])' SCORECARD.md LOG.md SHONEN.md` + per-line stem counts —
  sparse-line evidence shape confirmed (0–3 stems per line; file unions complete).
- Instrument reads: r41-closure.sh (helpers 421-575, checks 891-1348), capture-binding-check.py
  (173-461), frontier-recheck-count.py (94-424), round-41-verifier-spotcheck.md §5, r41 wave2:
  CritC1KillRule.md, RevC1Counters.md, MutSkillTablePipes.md, MutScratchTiming.md,
  CritDeclarationCoverage.md, MutFrontierParser.md, MutBindingExistence.md, MutC2Chain.md.

No tools installed (pacman paused host-wide; none needed). Scratch removed before filing. Report:
`.ufo/waves/round-42/wave1/CritKillRule.md`
