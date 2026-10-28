# CritC1Design — pre-build attack on the J1–J13 design

Axes: depth:verifiability (primary), coverage. Receipt-only item: for each J, the weakest
implementation that still meets the frozen predicate, whether that implementation can ever
print red (vacuity), and what its green actually proves. Read before writing:
`.ufo/waves/round-42/claims.json`, the wave-1 item specs, the r41 suite
`corpus/instruments/r41-closure.sh` (I-checks J1–J13 inherit), the committed r41 wave-2
defeat artifacts, `corpus/instruments/capture-binding-check.py` (J6 target) and
`corpus/instruments/frontier-recheck-count.py` (J7 target), SCORECARD.md, LOG.md, SHONEN.md,
SKILL.md. No suite bytes exist yet; this attacks the design, not a build.

Conventions below: "weakest viable" = smallest implementation satisfying the predicate text;
"vacuous" = cannot red on any input class the predicate names; "survives" = a mutated state
the check still greens.

## The replay contract has two failure modes shared by J1–J7

Every repaired check must carry a REPLAY limb that "re-executes its committed defeat
artifact against the current suite bytes and requires rejection" (claims.json C1 kill
rule). Both failure modes are already visible in the source material:

1. **The artifacts are prose, not fixtures.** `wave2/MutSkillTablePipes.md` is a 4-probe
   table (2 killed, 2 survived); `wave2/MutBindingExistence.md` is 3 probes (all survived);
   `wave2/MutScratchTiming.md` is 1 probe (survived). `replay_defeat` must reconstruct the
   *surviving* variants specifically. A limb that rebuilds a weaker or different variant and
   rejects it satisfies the letter of "requires rejection" while the artifact's own mutation
   still greens — an in-family escape under the frozen kill rule. **Correction:** each
   replay limb must enumerate the artifact's surviving probe set by name
   (e.g. `replay=MutSkillTablePipes:bare-pipe:rejected,leading-ws:rejected`), one limb-token
   per survivor, and absence of any named survivor's rejection token must be red.
2. **Mis-reconstruction.** The MutBindingExistence URL probes report the binding counter
   staying `bound=63` after both `url` and `capture_url` were case-/slash-mutated — yet
   `bind_record` (capture-binding-check.py:283-305) already does exact
   `record.url ∈ row_tokens(source cell)`, which rejects a record-only URL change with
   `rule=url-mismatch`. The observed exit-0 is therefore only consistent with a mutation
   that also changed the SOURCES.md row cell (shared mutation alphabet over the scratch
   corpus). If the J6 replay reconstructs a *record-only* URL mutation, the existing
   unpatched rule B5 already rejects it — the limb is vacuous and proves nothing. If the
   artifact's real mutation was a row+record co-mutation, **no local consistency check can
   reject it** (the row IS the URL authority; record↔row agreement is preserved by
   construction). J6's URL limb is therefore either tautological or unclosable depending on
   reconstruction fidelity — the executor MUST fix the true mutation alphabet first (inspect
   the artifact's scratch procedure, not just its summary line) or this family cannot
   honestly close. The missing-path limb IS closable (file existence + sha256 vs record).

## Per-check attack

### J1 — F-EVID, per-correction evidence (corrections grade the named overclaim; each names the firing evidence ids, not as a union)

- **Weakest viable:** per-RECORD-FILE union — for each of SCORECARD.md/LOG.md/SHONEN.md,
  require ≥1 qualified `Correction (round 42)` line grading the r41 overclaim AND the file's
  qualified-line union to cover every firing evidence id. This already rejects the committed
  replay (see anatomy) and is the coarsest granularity consistent with the honest tree.
- **The wave-1 spec over-commits:** ExecJ1's prompt reads "EACH correction individually must
  … name each firing evidence identifier" (per-LINE). Measured at HEAD, that is false on the
  honest tree: SCORECARD.md:1603-1605 and LOG.md:1737-1738 name zero evidence stems; only
  SCORECARD.md:1602, LOG.md:1736, SHONEN.md:221 carry stems. A per-line J1 can never green
  on a conformant tree — **false-red, not a stricter check**. The predicate's own phrase is
  "per-record, not as a union" — read it as per-record-file.
- **Actual defeat anatomy (verified in source):** the committed mutant strips stems from the
  FIRST `^Correction (round 41)` line per file (`replace_line` replaces only the first match,
  r41-closure.sh:1686-1690). It survived with `evidence=3/3` for TWO stacked reasons: (a)
  cross-file union in `check_i1` (902-906) — LOG/SHONEN stems rescue any single file's loss;
  (b) the D-r41-1 duplicated block (SCORECARD.md 1607-1610 = verbatim copy of 1602-1605)
  retained all three stems after 1602 was replaced. The r41 duplication defect is what
  physically rescued the union mutant in SCORECARD. **Interaction flagged for J11:** any J11
  design that removes or counts-merges the duplicated block changes J1's evidence coverage;
  J1 and J11 fixtures must be built together, not in isolation.
- **Vacuous?** No — reds when a file loses its stems or carries no qualifying line.
- **Green proves:** stems appear inside each record file's qualified lines — and nothing
  more. It does NOT prove the named identifiers resolve to committed artifacts: a correction
  naming the three hardcoded stems is green even if the claim's true firing evidence
  differs, and a hardcoded EVIDENCE list that omits a real firing artifact greens
  incompletely-enforcing lines. A lane-authored list also can't notice new r41-wave2
  findings landing after freeze.
- **Smallest safe correction:** per-file union on qualified lines + each named id must
  resolve to an existing path or heading under the export's `.ufo/waves/round-41/` (an
  invented stem fails) + the evidence-id list derived from the committed artifact set (not a
  literal frozen in the suite — a frozen list silently tolerates a correction naming a
  non-firing artifact).

### J2 — F-TOKEN, token-boundary tallies

- **Weakest viable:** a boundary-exact extractor for `closed=<n>/<m>`, `failures=<k>`,
  `cases=<k>` (bounded by non-digit, non-slash — and per the r41 helper's stricter class,
  non-letter too; see hole), applied at EVERY site the suite reads such values: (i)
  correction lines, (ii) J9's nested-run tail parse, (iii) the selftest case/summary
  matching (`mutants=<a>/<b>` is the same shape), (iv) J8's payload re-derivation. Plus a
  per-LINE rule on qualified correction lines: every `closed=`/`failures=`/`cases=` token on
  a line must be the expected value; no `mangled`-style elif escape.
- **Actual defect anatomy (verified):** three stacked weaknesses, not one:
  (a) `check_i3` tallies per FILE with first-hit-break (966-972) — one residual unmutated
  line rescues the file (and the D-r41-1 duplicate supplied exactly that residual);
  (b) the `mangled=` counter sits in the `elif` of the hit test (973-975) so it is
  unreachable whenever a hit exists — observed `mangled=0` beside the planted
  `closed=10/100`;
  (c) `replace_line` mutates only the first occurrence, so a per-file check that tolerates
  any surviving good line greens. The committed defeat transcript:
  `mutant=mangled-value-token rejected=0 payload=exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0`.
- **Predicate-level laxity:** "bounded by non-digit, non-slash characters" is WEAKER than
  r41's own `value_present` (449-452), which requires space/punct boundaries and so rejects
  `closed=10/10x` (a letter follows the value). A literal reading of the frozen text accepts
  `closed=10/10x` and `closed=13/13junk` as the expected token. **Fix:** implement the r41
  boundary class (space/punct/EOL), not the predicate's literal class.
- **Vacuous?** No — reds on any malformed token at a wired read site.
- **Green proves:** boundary-exactness AT THE WIRED SITES ONLY. Any tally read site that
  bypasses the shared extractor (a stray `grep closed=`, `payload_get` on `closed=`, a
  selftest-line `sed`) is an un-rejected in-family escape the replay does not cover. Green
  is conditional on wiring completeness, which the check itself cannot prove.
- **Smallest safe correction:** one extractor function; J2's payload names the wired sites
  count (`sites=<k>`); the selftest mutates a value at EACH site class (correction line,
  nested tail, selftest line, receipt payload), not only the correction line.

### J3 — F-TABLE, SKILL.md registry integrity

- **Weakest viable:** parse every Gates-and-probes table in SKILL.md; reject a blank line
  inside header→last-row; require every `corpus/instruments/r*-closure.sh` basename in
  exactly one row across all tables; reject bare internal `|` in cells and leading-ws first
  cells (column-count == header column-count).
- **Verified current defects:** SKILL.md:1121 blank inside the round-40 table (orphaned r40
  row at 1122); `r40-closure.sh` rows at 1122 AND 1128 — a CROSS-TABLE duplicate, so a
  within-table uniqueness check misses it.
- **Vacuous?** No — the four survivor/killed probes in MutSkillTablePipes all reach it.
- **Green proves:** table-shape invariants only. It does NOT prove the registered row
  describes the shipped suite: a stale copy of r41's verdict-map prose under an
  `r42-closure.sh` basename passes every shape clause — the row's semantic content is free
  text. Flagged as a low-value green limb; acceptable for the routed family (the family is
  registry INTEGRITY, not registry accuracy) but the receipt should not overclaim it.
- **Hole in the predicate wording:** "no instrument basename appears in more than one row"
  — must be GLOBAL across all registry blocks, and must tolerate that `r40-closure.sh`'s
  legitimate round-40 row is the one kept (the fix removes the round-41-block duplicate,
  not "first wins" arbitrary dedup that could delete the canonical row).
- **Smallest safe correction:** scan ALL `| name | type | …` tables under the registry
  sections; uniqueness over the full set; replay both surviving probes (bare-pipe,
  leading-ws) — not just one — or the kill rule's "in-family escape" clause fires.

### J4 — F-DECL, declared-blocks completeness

- **Weakest viable:** `.ufo/waves/round-42/declared-blocks.txt` listing every export path
  any check reads (fail-closed when the file is absent — at base and r41-head this alone
  reds the check); canonicalize each declared path and reject symlink/`..`/absolute
  escapes (r41 lines 1077-1096 pattern); require the declared tail to equal the appended
  tail with zero deletions (I12 whole-tail).
- **The completeness limb is unprovable as worded:** "every artifact path that a check
  reads is declared" — a static suite cannot enumerate its own reads. Weakest compliant
  proxy = compare `git diff --name-only base ref` against the declared set
  (CritDeclarationCoverage's own suggested fix, .ufo/waves/round-41/wave2/
  CritDeclarationCoverage.md:15). That proxy greens while a check reads a path that did
  NOT change this round (e.g. a limb reading `corpus/lessons/round-39.md` — unchanged,
  undeclared, un-flagged). **Vacuous limb:** the reads-coverage clause can only be honest
  if every check reads through a path-asserting helper (`path_safe`-gated read) — a
  convention the suite must enforce structurally, and even then a hand-rolled `cat` in one
  limb bypasses it silently.
- **Green proves:** the declaration FILE is well-formed and canonical-safe; NOT that it is
  complete. The honest green ceiling is "changed-path coverage + declaration hygiene."
- **Artifact note:** CritDeclarationCoverage's probe itself ended RED (`closed=8/12`) — it
  demonstrated a coverage gap, not a reproduced acceptance. Replaying it to rejection is
  trivially satisfiable; the real closure is the changed-set↔declared-set comparison. Do
  not let the replay limb's existence be read as proof the gap is closed.
- **Smallest safe correction:** declare-reads-by-convention (all tree reads via one helper
  that asserts membership in the declared set) + diff-set comparison as the measurable
  proxy + payload prints `declared=N read-undeclared=K` with K required 0 — the K counter
  is the only honest signal; if a helper bypass exists K is unmeasurable and the payload
  must say so.

### J5 — F-SCAN, scratch hygiene (family scan + outside-configured-root stray)

- **Weakest viable:** enumerate `kasegi-r4[0-9]*`-family entries under the passed
  `--scratch-root` (never hardcoded), exempt this run's `--work` and its clean ancestor
  chain, count everything else a stray; PLUS the outside-root limb exercised inside a
  materialized fixture root under `--work` (fixture parent scanned for family entries).
- **Separator hole in the frozen wording:** the committed artifact's stray was
  `/tmp/kasegi_r41_outside_probe` — UNDERSCORE separator. A `kasegi-r4[0-9]*` literal scan
  does not match `kasegi_r41…` → the replay escapes → kill-rule fire. r41's I6 already
  scanned case- and separator-insensitively (`-`, `_`, `.`, whitespace). The r42 family
  pattern must be `kasegi[_ .\t-]*r4[0-9]`-equivalent or wider, or the named artifact is
  not rejected.
- **Vacuity conditions (two, both observed or near-miss in r41):** (a) an empty/missing
  scratch root greens with `scanned=0` — MutScratchTiming's pristine run showed
  `strays=0,read=ok,scanned=0 closed=1`; the check MUST fail closed on an unreadable or
  empty-of-family-entries root ONLY when entries should exist — an empty root is
  legitimately clean, so the honest signal is `read=ok`, not `scanned>0`; (b) the
  outside-root limb greens by construction if the fixture's parent isn't scanned at all.
- **Green proves:** ONLY the given --scratch-root subtree (plus the materialized fixture's
  parent). The HOST's real leftovers elsewhere (`/tmp`, other roots) are invisible by
  design — green J5 does not prove the host is clean; it proves the suite's configured
  scope is clean. The claims text already scopes it so; the receipt must not read it
  broader.
- **Smallest safe correction:** separator-insensitive family regex + `read=ok|fail` gate +
  ancestor-chain exemption requiring each level hold exactly the next component + replay
  the committed underscore-outside-root stray INSIDE the materialized fixture tree.

### J6 — F-BIND, capture-binding missing-path/URL variants (patched instrument over mutated scratch manifests)

- **Weakest viable:** add to `capture-binding-check.py`: (a) every record's `path` names a
  present file under its snapshot dir (the reverse direction of rule A, which the file
  documents as deliberately absent at line 124-126: "a record naming a file that is absent
  is not a rule"); (b) the record's `sha256` equals the file's sha256 (records already carry
  the field; the instrument never compares it); (c) for the URL limb — SEE THE FAMILY
  PROBLEM in the replay section: record↔row URL equality already exists (B5). The only
  additional local limb with any teeth is `capture_url`/`url` field agreement plus
  record.url ∈ row token (already present) — and BOTH fail to reject the row+record
  co-mutation the artifact most plausibly performed.
- **Vacuous?** The missing-path and sha limbs are non-vacuous (they red on absent/wrong
  bytes). The URL limb is **vacuous-or-unclosable**: if the replay models a record-only URL
  edit, pre-existing B5 already rejects (the limb proves nothing new); if it models the
  artifact's co-mutation, nothing local can reject it. Either way the URL limb's green is
  the weakest evidence in the suite.
- **Green proves:** record paths exist and digests match. It does not prove the capture is
  the document the URL names — a co-mutated URL still binds; content-URL correspondence is
  unverifiable offline (the instrument's own Known-limits admits this, lines 118-126).
- **Regression risk unique to J6:** the patch lands on a LIVE instrument also counted by C2
  (`records=56 bound=56 unbound=0` must hold at Y). A patch that rejects any existing
  committed record breaks C2; a patch weakened to preserve the count may reject nothing.
  J12's digest guard covers only density.py — a patch that silently DELETES rule B5 while
  adding a sha limb passes J12 untouched. **Correction:** J6's replay must run the
  instrument's own `--selftest` as part of the limb (selftest cases exist; a rule deletion
  breaks them), not only the two defeat fixtures.
- **Smallest safe correction:** existence + sha256 limbs; declare the URL limb's scope
  honestly (record-vs-row, accepting the co-mutation limit in the check's own limits note);
  run instrument selftest inside the replay; bind the replay to the artifact's real
  mutation alphabet after inspecting the artifact.

### J7 — F-FLIP, frontier-counter status-flip detection

- **Weakest viable:** enumerate EVERY `| F<n> |` row without the `admitted` filter
  (frontier-recheck-count.py:393 drops non-admitted rows before counting — that IS the
  blind spot); require status==`admitted` per row (any other status → exit 1); require each
  admitted row's `PASS F<n>` record; add the registry-membership limb (recheck `--source`
  ids ⊆ SOURCES.md row ids) — `manifest_ids` (163-176) validates against the manifest, not
  the registry, so this limb is genuinely new work.
- **Vacuous?** No — a status-flipped or PASS-less row reds it.
- **Green proves:** rows counted == rows present and each admitted row ran its recheck.
  It does not prove `entries=N` counts rows rather than ENTRIES — a row whose cell names
  two entries counts 2; the frozen C2 counter `entries=28 pass=28` counts entry-records.
  If a flipped row is also dropped from `entries`, the count silently self-consistent-greens
  (the original defect's exact shape). The fix must compare `entries` to the RAW row count,
  not to the admitted subset.
- **Policy collision flagged:** "exits nonzero if any frontier row is non-admitted"
  forecloses any future parked/queued status. F24's row is `admitted` at freeze, so no
  conflict now — but the round-41 spotcheck leaves an open L0 scope question on F24; any
  future status flip on that row reds J7 by design. That is intended, and worth saying so
  the L1 does not "fix" a designed red.
- **Smallest safe correction:** count rows before filtering; require all-admitted; PASS
  per admitted row; `--source` ids ⊆ registry ids; replay the committed F24→explored
  fixture and require exit!=0 AND the flipped row NAMED in output (a silent drop that
  still exits nonzero is a weaker rejection than the family intends).

### J8 — F-RCPT, receipt integrity (teed transcript; payload values re-derived not trusted)

- **Weakest viable:** inherit r41's I2+I8: canonical transcript rebuilt from tree+ref
  facts; each recorded `J<n> payload=` compared to the recomputed value; forgery classes
  (payload-contradicting, future-dated, foreign-ref, nonexistent-ref, summary-only,
  tampered-payload-line, missed control) each rejected independently; run-utc = committer
  instant of the NAMED ref (ref-commit time-basis); seed bootstrap at J since a commit
  cannot contain its own hash.
- **Not vacuous** — the named forgery classes all reach it.
- **Green proves:** the receipt is self-consistent with the suite's own recomputation —
  i.e., it proves NO RECEIPT FORGERY, not that the checked facts are true. A suite whose
  limbs systematically mis-measure produces a receipt whose values match its own (wrong)
  derivation and J8 greens honestly. J8 is internal-consistency, and that is by design;
  do not read its green as content-verification.
- **Environment-dependence landmine (new in r42):** J5 and J13 read LIVE state
  (scratch-root strays, lane porcelain). If J8 byte-compares the committed receipt
  against a canonical rebuild that includes live-limb payloads, a re-run at Y under a
  non-quiescent environment (the verifier's own scratch root holding a sibling stray)
  re-derives a DIFFERENT canonical transcript → `cmp=0` → J8 red at Y for environmental
  reasons → the counting command `closed=13/13` fails through no defect of the tree.
  r41 had this exact limit (I6 live). The design must either (a) document that the
  counting commands' `--scratch-root` MUST be a clean private dir and the lane quiescent —
  a verifier-discipline constraint baked into the claim — or (b) wildcard the live fields
  in the byte-compare, which silently re-opens the forgery surface for exactly the fields
  most worth binding. Recommend (a), stated in the suite's own limits.
- **Self-hash note:** `suite-sha256` is computed by the suite about itself; honest but
  self-attested — verifier-side `sha256sum` on the export's suite is the external anchor.
- **Smallest safe correction:** full payload compare + run-utc bound to named ref + the
  six forgery clauses + explicit documentation that receipt reproducibility requires a
  clean --scratch-root and quiescent lane (else J8 reds environmentally).

### J9 — negative controls (base & r41-head exports closed<13/13 exit=1; distinct ref-not-found)

- **Weakest viable:** run the EXPORT's own suite copy over BASE_REF and
  `1f7464612ac4c44e39886b82e812610d3c039b13` under a depth cap (R42_DEPTH=1 leaf mode);
  accept each control only when `exit==1` AND `closed=K/13` parses as a whole token with
  `K<13` AND a named set of tree-dependent checks is red inside the nested transcript —
  the checks that CANNOT be satisfied at those refs for tree reasons: J8 (receipt absent /
  wrong grammar), J4 (round-42 declared-blocks absent), J3 (no r42 row). At r41-head the
  r41 receipt exists but fails the r42 grammar — J8 still reliably red.
- **Vacuity trap (the M-H8a class, still live):** an acceptance predicate of `rc==1 &&
  K<13` alone accepts a nested run that is green-but-for-recursion (a base export whose
  tree satisfies every J but the depth-capped J9 prints `closed=12/13 exit=1` and is
  ACCEPTED as "properly red"). r41's `neg_accept` (1334-1348) closed exactly this by
  demanding named checks red. The J9 named-red set is the check's only teeth — without it
  J9 is vacuous for the strongest adversary (a suite green at base except where depth
  forbids it).
- **Parse-boundary requirement:** the `closed=K/13` extraction must use J2's bounded
  extractor — `closed=3/130` or `closed=13/13 ` tail-parse subtleties are the same F-TOKEN
  family arriving through a second door.
- **ref-not-found limb:** must print `ref-not-found` and exit 1 with NO `closed=` tally —
  the r41 design is correct; keep that every J line carries `payload=ref-not-found` so no
  parser can read the run as closed-but-red.
- **Green proves:** the suite reds on the two named refs AND reports a broken ref
  distinctly. It does not prove red-ness for OTHER refs — fine, that is the contract.

### J10 — graded-selftest isolation (each case a private mutated copy; no case reads another's state)

- **Weakest viable:** count selftest cases and assert each materialized under its own dir:
  `cases=13,isolated=13` (r41 I9's shape).
- **MOSTLY VACUOUS as specified.** Who asserts the isolation? The suite, about itself.
  The predicate ("a case must not read another case's state") is enforced by the
  selftest machinery the check is grading — the green is self-attestation, like a student
  grading their own invigilation. The only non-vacuous content is structural: each case
  dir exists, is distinct, and a baseline diff shows no cross-case writes.
- **Green proves:** the suite claims its cases are isolated, and directory grammar was
  followed. It does NOT prove a leak would be detected — UNLESS the graded selftest's J10
  case includes a leak mutant (a fixture case that writes into a sibling case's dir and is
  required to red the limb). Without that negative fixture, J10's green proves literally
  nothing beyond counting.
- **Smallest safe correction:** the J10 selftest case must carry a leak-mutant negative
  (planted cross-case write → red) and a shared-state-read negative (case B's fixture
  importing case A's product → red); the spec's "scratch baseline diffed before/after each
  case" must diff at case granularity, not suite granularity.

### J11 — F-CORR, SCORECARD correction uniqueness (no duplicated verbatim Correction block)

- **Weakest viable:** normalize whitespace per line; require count==1 per distinct
  `Correction (round <n>)` body per FILE (cross-file repetition is legal — LOG and
  SCORECARD honestly re-state corrections); PLUS the appended `Correction-dedup (round 42)`
  marker naming the duplicated ranges, because the r41 duplicate is append-only history —
  it stays forever, so the check can only pass if the design's actual semantics are
  "every duplication is either absent or marker-forgiven."
- **The marker is a general amnesty — the real vacuity vector:** if the marker forgives a
  duplicated body merely by existing and naming two line ranges, then ANY future
  duplication anywhere in the file (at those lines or elsewhere) is also forgiven as long
  as someone appends a marker. To close it, the marker must bind the duplicated BODY
  (digest or normalized prefix) AND its line positions; J11 then requires: dup groups ⊆
  marker-named (body,positions) pairs. Anything weaker is a permanent escape hatch — and
  since J11 is NOT one of the seven kill-rule families, an escape here is a routed defect
  rather than a kill, making weak J11 the cheapest place for sloppiness to hide.
- **Vacuous?** Borderline. Without marker-binding it can never red on a marked-up file
  full of arbitrary dups — effectively vacuous against the adversary who can append text.
  With body+position binding it reds honestly.
- **Green proves:** no UNMARKED verbatim duplication in the three record files — under the
  bound-marker reading; otherwise just "a marker exists."
- **Smallest safe correction:** marker grammar `Correction-dedup (round 42): <body-digest>
  lines <a>-<b> dup <c>-<d>`; J11 verifies digest==normalized body AND positions are the
  observed dup positions; any unlisted dup group → red.

### J12 — no tracked deletions in corpus paths + density.py byte-identical

- **Weakest viable:** `git -C <lane> diff --name-status <base> <ref> -- corpus/` → zero D
  rows; sha256 of export's `corpus/instruments/density.py` == pinned constant
  (ee803726… — verified equals current file).
- **Vacuous at the negative controls — deliberately:** at base, base==ref → diff empty →
  0 deletions → green; density==base → green. J12 CAN be green at base; it relies on other
  Js to keep base red. That is fine — but the receipt must not cite J12 as a base-red
  contributor.
- **Green proves:** corpus paths only. `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`,
  `SHONEN.md` deletions are OUT of scope for J12 — caught only transitively (J1 needs the
  record files, J3 needs SKILL.md; PROVINCE.md deletion evades every J — the C2 counting
  command catches it outside the suite). Flagged: the suite's no-harm guard has a
  PROVINCE.md-shaped hole; the claims predicate does not require closing it, but the gap
  should be named in the suite's limits or J12 extended to the five tracked root files.
- **Smallest safe correction:** extend the diff to `-- corpus/ SKILL.md PROVINCE.md
  SCORECARD.md LOG.md SHONEN.md` — one-line cost, closes the gap rather than documenting
  it.

### J13 — quiescence (no uncommitted lane changes + no family scratch entry in the suite's own root)

- **Weakest viable:** `git -C <lane> status --porcelain` minus the single expected-dirty
  path (the receipt file being written — `--receipt-out` lands inside the lane) + the
  family scan over `--scratch-root` (shared machinery with J5).
- **The clone-worktree limb is vacuous by construction:** ExecJ12J13's spec reads "no
  uncommitted changes in a clone of the exported ref" — a clone of a committed ref is
  ALWAYS clean; the limb can never red and is dead weight. The LIVE limb that carries
  information is `git -C <lane> status` on the real lane — host state, ref-scoped,
  read-only with `--no-optional-locks` — and that is what the frozen predicate means by
  "no uncommitted lane changes."
- **Receipt-path exemption is a second hole:** the exemption must be the byte-exact
  receipt path. A pattern exemption (`*final-gates*`, `*.txt`) lets a stray untracked file
  hide beside the receipt. Tracked modification of the receipt post-commit shows as `M`
  and is correctly caught only if the exemption covers untracked, not modified.
- **Green proves:** a POINT-IN-TIME fact, not a commit property — today's clean worktree
  and clean scratch scope. Re-running next week on a dirty lane reds J13 at Y → the
  committed receipt becomes non-reproducible for environmental reasons (same limit as J5
  and J8's env coupling — document it once, centrally).
- **Smallest safe correction:** drop the clone-clean limb (vacuous); keep live porcelain
  with byte-exact receipt exemption + skip-worktree/assume-unchanged marker scan (r41's
  F8 class, `git ls-files -v`) — that limb is NOT in the claims text but is the cheapest
  in-scope hardening; stray scan shares J5's machinery with the same separator alphabet.

## Cross-cutting findings

1. **Two checks are green-by-design at the negative controls and must not be counted as
   base-red contributors:** J12 (base==ref) and J5 (empty root clean). Base-red accounting
    rests on J1, J3, J4, J6, J7, J8, J9, J11.
2. **J11's marker amnesty and J1's evidence coverage interact:** the D-r41-1 duplicate is
   what kept `evidence=3/3` green under the committed I1 mutant. If J11's landing (marker +
   any body normalization) changes which correction lines J1 scans, the replay outcome
   changes. The two limbs must share the qualified-line selection, or each will silently
   disagree about what a "Correction" is (fences, `Correction-dedup` marker lines —
   the marker MUST NOT match `^Correction \(round` or J1 counts it as a correction).
3. **J8's reproducibility inherits J5/J13's environment:** name the constraint in the
   receipt — `closed=13/13` at Y is reproducible only under a clean verifier scratch root
   and quiescent lane; the counting commands must pass a private `--scratch-root`.
4. **The graded selftest is the only layer that grades limbs; it is also suite
   self-report.** A green `selftest cases=13` proves the suite's own fixtures reject —
   external wave-2 falsifiers remain the trust anchor. Within that limit, every J needs ≥1
   negative whose mutation targets THAT check's limb (a shared global negative that reds
   everything proves nothing per-case; r41's st_neg needle-on-payload design handles this).
5. **`selftest case=J<n>` counting:** the kill rule requires thirteen graded lines with
   `positive=pass` and `verdict=pass` — J2's extractor must guard `mutants=<a>/<b>` and
   `failures=<k>` shapes identically, and a summary-only line must never satisfy a case
   (kill clause names this explicitly).
6. **Family-scope holes the enumeration leaves open (routed-defect material, wave-2
   ammunition — name them now, not after):** F-EVID union-across-files handled, but
   evidence-names-must-exist unhandled; F-TOKEN `closed = 13/13` / `closed:13/13`
   separator variants and letter-suffixed values under the predicate's literal boundary
   class; F-TABLE pipe-escaped cells `\|` and cross-block duplicate basenames; F-DECL
   unchanged-file reads uncovered by the diff proxy; F-SCAN non-hyphen separators and
   post-scan race (a stray created after scanning — noted in the artifact itself);
   F-BIND row+record co-mutation; F-FLIP entries-vs-rows counting.
7. **Cheapest-green ranking for wave-2 attackers:** J13-clone-limb (vacuous), J10 without
   a leak fixture (self-attested), J6-URL (vacuous-or-unclosable), J5-scoped-root (real
   but narrow), J3-prose (shape not semantics), J12-pathspec (narrow), J9-without-named-reds
   (accepts green-but-for-recursion). In descending order of "green that proves least."

## Smallest safe corrections (consolidated)

- J1: per-record-file union; evidence ids must resolve to committed r41 wave-2 paths.
- J2: one bounded extractor (space/punct boundary, NOT the predicate's literal class)
  wired to all four read-site classes; per-line malformed-token scan independent of
  tally hit; selftest mutates a value at each site class.
- J3: global basename uniqueness across all tables; replay BOTH surviving probes.
- J4: reads-through-helper convention + diff-set completeness proxy + `read-undeclared=K`
  payload; acknowledge the proxy's ceiling.
- J5: separator-insensitive family pattern (`-`, `_`, `.`, whitespace) incl. the
  artifact's `kasegi_r41` shape; `read=ok` gate; materialized-fixture outside-root replay.
- J6: existence+sha limbs; instrument `--selftest` inside the replay limb; pin the
  artifact's true mutation alphabet before writing the URL replay (likely unclosable —
  say so in the check's limits rather than ship a vacuous limb).
- J7: rows counted before status filtering; all-admitted required; flipped row named in
  output; registry-membership for recheck ids.
- J8: document the clean-scratch/quiescent-lane reproducibility constraint; reject
  wildcarding live fields.
- J9: named-red set (J3/J4/J8) inside each nested transcript + bounded tally parse.
- J10: leak-mutant and shared-state negatives inside its own selftest case; case-granular
  baseline diff.
- J11: marker binds body-digest + positions; marker line excluded from J1's Correction
  grammar.
- J12: extend pathspec to the five tracked root files.
- J13: drop the vacuous clone limb; live porcelain + byte-exact receipt exemption +
  skip-worktree marker scan; share J5's scan machinery and alphabet.

Report: .ufo/waves/round-42/wave1/CritC1Design.md
