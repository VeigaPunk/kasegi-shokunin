# CriticClaims — round-76 attempt 1, adversarial review of frozen C1 and C2

Seat: CriticClaims (leaf critic, read-only + scratch). Freeze: `5da54cd4451cbbb9e4b87e2f83475feb13c65c9e` (base `a788021675873a96e09e91aa033d8c26ac2fe212`). No lane edits, no network, no subagents. All reads were `git -C <lane> show|archive` at the freeze commit or copies in my scratch dir. The real lane worktree was not touched.

## Verdicts

- **C1 (recheck-cwd census amendment): GAP — F1 (BLOCKER), F2, F3, F4, F5, F6, F7.** As frozen, F1 makes the claim fail its own kill rule at any single integration commit that also carries C2. Not `HOLDS as frozen`.
- **C2 (F54 admission on S111): GAP — F10 (BLOCKER), F12 (BLOCKER), F11, F13, F14, F15, F16, F17, F18.** As frozen, B5 cannot pass (`source-recheck.py` exits 2 on the committed manifest) and the endpoint-name clause is already held ground under the kill rule's own named sources. Not `HOLDS as frozen`.

Severity: BLOCKER = the claim fails its own kill rule as written; GAP = a predicate or statement clause is unverified, unenforced, or overstated; NOTE = observation, no fix required for the claim.

## Verification ledger (every number below was produced by the command shown)

| # | Command (cwd: lane or my scratch) | Exit | Result |
|---|---|---|---|
| V1 | `git -C <lane> show 5da54cd4…:corpus/instruments/recheck-cwd-census.py \| sha256sum` | 0 | `e666ae11…a21a`, matches claim base hash |
| V2 | `diff base.py .ufo/waves/round-76/controls/mut/m{1,2,3}-*.py` | 1 (diffs expected) | Each mutant is a full base-bytes copy with exactly one hunk: m1 neither-header → restoration_only (lines 93-98); m2 drops `ret6 == 1 and "…nonconformant" in out6` (line 244); m3 `if value is None or has_restoration_recheck(path)` |
| V3 | `python3 -B base.py --selftest` | 0 | `selftest cases=6 failures=0` (matches receipt) |
| V4 | `python3 -B mC-drop-case5-check.py --selftest` (scratch mutant: `check("first-line", …)` replaced by a bare expression) | 0 | `selftest cases=6 failures=0` — the case is gone and the literal count is unchanged |
| V5 | `python3 -B mA-exit1-to-exit0.py --selftest` (scratch mutant: exit-1 foreign results counted in `exit0_foreign`) | 0 | `selftest cases=6 failures=0` — survivor |
| V6 | `python3 -B mB-prefix-substring.py --selftest` (scratch mutant: `noprefix = prefix not in value`) | 0 | `selftest cases=6 failures=0` — survivor |
| V7 | static census of freeze tree: `git -C <lane> archive 5da54cd4… corpus/knowledge \| tar -x` then header scan of `*.md` | 0 | entries=91; recheck-only 89; both-header 2 (`claim-gates.md`, `claim-package-contract.md`); restoration-only 0; neither 0 |
| V8 | `python3 -B base.py --root <missing> --lane x` | 1 | `recheck-cwd: no corpus/knowledge …`, rc 1 (docstring promises exit 2) |
| V9 | `grep -c '"bash"'`, `grep -c 'subprocess.run('`, `grep -c '"bash", "-c"'` on base.py | 0 | 1, 1, 1 |
| V10 | `sha256sum` of freeze `corpus/source-snapshots/round-76/S111.txt` | 0 | `6f92e5b7…5581ab` (matches claim); 1810 bytes, 48 lines |
| V11 | python check of the 13 manifest quotes against `S111.txt` at declared anchors (exact line equality) | 0 | 13/13 EXACT at anchors 21,22,28,29,30,31,32,33,34,35,36,38,39 |
| V12 | `python3 -B corpus/instruments/source-recheck.py --manifest <freeze manifest> --source S111` (scratch copy of freeze `corpus/source-snapshots/round-76/`, instrument from freeze) | **2** | `S111:Q01-api-version UNAVAILABLE reason=quote-too-short-to-be-evidence`; no `sha256 OK` line emitted |
| V13 | same, with Q01 removed (scratch-only manifest), Q04 anchor=99, Q12 anchor=1 | 0 | `S111:sha256 OK`; `Q04 OK occurrences=1 anchor=OUT-OF-RANGE`; `Q12 OK occurrences=1 anchor=1-BROKEN` |
| V14 | occurrence count of every manifest quote in normalized S111 | 0 | all 13 = 1 (so anchors are never consulted by source-recheck) |
| V15 | `git -C <lane> show <freeze>:corpus/source-snapshots/round-73/S108.txt` lines 4-9, 148; round-73 manifest Q27-Q29 | 0 | nav lines 4-9 hold the same six endpoint lines; line 148 holds "32MiB … HTTP/1.1. There is no limit when using HTTP/2. We recommend using HTTP/2 for queries that may result in large responses."; Q27-Q29 anchor 148 |
| V16 | `git -C <lane> grep -n` over freeze corpus for OSV endpoint terms and `osv.dev` | 0 | F51 knowledge line 75 names the S108 nav endpoints "listed, not described (S108.txt:5-9)"; S080 (round-50) lines 146, 185, 190, 205 hold `https://api.osv.dev/v1/vulns/<ID>` |
| V17 | `sed -n` of `scripts/sources-census.sh` duplicate-URL scan (lines ~600-650) | 0 | only Registry-section table rows enter the URL scan; lead bullets (SOURCES.md:175) do not |
| V18 | `scripts/sources-census.sh validate --root <scratch fleet>` | 2 | not reproduced: needs `shokunin.conf` in the fleet root; W04/E04 finding is from reading the script, not from an executed run |

Not run by me: the lane's own census (`recheck-cwd-census.py` on the real tree) — its rechecks execute against the live lane and I did not want writes there. The base receipts were taken as given and cross-checked statically (V7: 69 + 22 = 91 agrees with the receipt's exit0/exit1 split).

---

## C1 — recheck-cwd census amendment

### F1 — BLOCKER — A2 and A4 contradict each other once C2 lands in the same tree
- A4 requires the amended real-tree census stdout to be byte-identical to the base receipt (`entries=91 … exit0_foreign=69 … exit1_foreign=22`) "at the C1-landing tree".
- A2 literal requires the same numbers at the same tree, but its parenthetical says the drift expectation is `entries=92, exit0_foreign=70` "once C2 lands".
- C2's B2/B3/B4 are measured "at integration", i.e. on the tree where the F54 knowledge file exists. A knowledge file added by C2 necessarily moves `entries` to 92 (V7 proves the base is 91 and the only other change is one new `*.md`).
- So if C1 and C2 land in one integration commit (the normal reading of "round-76 attempt 1 landing"), A4 is false and A2-literal is false, and the claim fails under its own kill rule ("any of A1-A5 false at the landing commit = claim fails").
- R121 is also violated: "C1-landing tree" is not a named revision (a commit hash or an explicit "before C2" state). The claim names a drift expectation but not the revision it applies to.
- Fix class (for the L1 to choose before scoring): name a landing order (C1 commit strictly before the F54 commit, with its own hash), or drop the byte-identical A4 in favour of "diff of census output vs base receipt differs only in the F54 entry".

### F2 — GAP — A1 `cases=8` is a literal, not a measured count
- `recheck-cwd-census.py` prints `print("selftest cases=6 failures=%d" % len(failures))`; the `6` is a string literal. `source-recheck.py`, by contrast, prints `len(cases)`.
- V4: deleting a case's check (scratch mutant) still prints `selftest cases=6 failures=0`, rc 0.
- Consequence: A1 as written ("prints 'selftest cases=8 failures=0' and exits 0") is satisfiable by a counter that runs fewer than eight cases and prints 8. This is the exact axis under claim (depth:verifiability). The amendment must compute the count from the case list (or the predicate must count `check(` calls) — otherwise the number is not evidence.

### F3 — GAP — A3 kill semantics are not defined on amended bytes
- (a) "exit nonzero" is satisfied by an uncaught `NameError` traceback. Removing the RESULT limb's computation (`out6, ret6 = capture(main, …)`) under an amendment that consumes `ret6` would crash the selftest with rc 1 and no `selftest … failures=N` line. The kill is then a crash, not an assertion. A3 must require the printed line `selftest cases=8 failures=N` with N ≥ 1 and a `selftest case=… FAIL` line.
- (b) The committed mutants (`controls/mut/m{1,2,3}-*.py`, V2) are full base-bytes files with one hunk each. They cannot be run "on the amended selftest" as they stand: applying them to amended bytes requires a patch recipe, and none is committed. The README documents base-selftest survival only.
- (c) M-R2 "the case-6 RESULT limb removed" is not an operation on amended bytes until the amendment exists: the limb's text is ambiguous (the `ret6 == 1 and "…"` conjunct, the `main()` call, or both). A fixer can satisfy (ii) by coupling `ret6` into a detail string that the removal leaves intact, and A3 would then fail for a reason the claim did not measure.
- (d) No named command: A3 says "make the amended selftest exit nonzero" with no invocation of the mutant bytes. (QUALITY R121 class.)
- Fix class: commit the amended-mutant recipe (patch text applied to the amended file with `find`-count=1, as `limb-mutation-check.py` does), and state the kill as the `failures=N` line with N ≥ 1.

### F4 — GAP — the kill rule is wider than the predicate, and two survivors sit outside the three named classes
- Kill rule: "a mutant that survives the amended selftest = claim fails" (unrestricted).
- Predicate A3: three named classes (M-R1, M-R2, M-R3).
- The unrestricted reading is unsatisfiable by any counter in practice. V5 and V6 show two survivors of the base selftest that the amendment's listed fixtures do not discriminate: mA (exit-1 foreign results counted as `exit0_foreign`, rc 0) and mB (substring prefix test, rc 0). The amendment's listed fixtures (restoration-only + neither-header + prefixed passing entry; both-header; case-6 limb) contain no exit-1 entry and no prefix-in-the-middle value, so neither is killed.
- Fix class: narrow the kill rule to "a mutant of the three named classes that survives the amended selftest", or add the fixtures that kill mA/mB and name them. Either is a scope decision for the L1; I am not rewriting the predicate.

### F5 — GAP — A5 has no named command; the scratch clause is non-checkable as written
- A5 counts (V9): 1 `"bash"`, 1 `subprocess.run(`, 1 `"bash", "-c"` pair in base — these are verifiable by a `grep -c` command the claim does not name.
- "create no file outside tempfile.mkdtemp directories honoring TMPDIR" has no command at all. Nothing in the counter writes outside its mkdtemp scratch; that is a reading, not a measured predicate.
- The receipt environment had TMPDIR unset: the base selftest's tmpdir-parent case printed `dirs=None,None,None` (`c1-donothing-selftest-r76.txt`), so the honour-TMPDIR check is vacuous there. A1 must run with TMPDIR set to an explicit scratch path (the seat spec requires it); the claim does not say so.
- Fix class: name the grep counts and an explicit-TMPDIR selftest run as the A5 command.

### F6 — GAP — registry pins are stated but not measured
- The claim object's `registry_pins` require `SKILL.md` and `corpus/instruments/README.md` to move from `selftest cases=6` to the amended count (QUALITY R113).
- Verified pin sites at the freeze: `SKILL.md:982` (`selftest cases=6 failures=0`) and `corpus/instruments/README.md:354` (same string for this counter). `corpus/instruments/README.md:851` and `:887` pin `frontier-recheck-count.py`, not this counter.
- No predicate names the R113 check (`grep -rn 'selftest cases=' SKILL.md corpus/instruments/README.md` equals the counter's own output). The claim therefore has a pin obligation with no measurement. Add it as A6.

### F7 — GAP — universal sentences over enumerated fixtures
- Statement (i): "a neither-header knowledge file … is counted **only** in norecheck" — the amendment tests one such file.
- Statement (iii): "a mutant forcing restoration_only on **any** restoration-recheck: carrier" — the amendment tests one both-header carrier.
- Statement (ii): "the case-6 RESULT limb **becomes load-bearing**" — one limb, one case.
- These are fixture-level facts. A mutant that discriminates a sub-case (e.g. a both-header file whose `restoration-recheck:` precedes `recheck:`, or a neither-header file in a directory that also holds a restoration-only file) survives. The scope must read "on the enumerated fixtures (i)-(iii)"; "any", "only" and "becomes load-bearing" must be bounded by the fixture list. C1's scope is an enumerated mutant set; it is not a sandbox claim, and the wording should say so.

### F8 — NOTE — A4 diff recipe is unnamed
- The base receipt `c1-donothing-realtree-r76.txt` ends with an appended `census_rc=0` line that is not census stdout. A raw diff of census stdout against that receipt is therefore non-empty by construction. Name the recipe (compare the `RECHECK-CWD` and `RECHECK-CWD-RESULT` lines only).
- A4 also forbids any new real-tree diagnostic line (for example, a "BOTH-HEADERS" informational print for the two real files). The amendment must not add one.

### F9 — NOTE — pre-existing exit-code mismatch (outside the A letters)
- `census()` raises `SystemExit("recheck-cwd: no corpus/knowledge …")`, which exits 1 (V8). The docstring says "Exit 2: harness or read error". Not in C1's scope; record it or fix it in the same landing if the L1 wants the docstring true.

### C1 kill-rule complement (answer to attack item 2)
- Frozen three classes: each is killed by a fixture the amendment adds (M-R1 by the tally in (i), M-R3 by the both-header fixture in (iii)); M-R2 is killed only if the kill is an assertion (F3a). Its complement is therefore not closed: M-R2's kill can be a crash.
- Survivors outside the classes (F4) pass the amended selftest as specified. Under the unrestricted kill rule that is a failure; under the three-class reading it is not, but then the claim proves less than its prose ("the counter is amended so that…" plus "load-bearing") suggests.
- The do-nothing control is sound: V3 and the receipt show the base selftest passes all three mutants (`c1-redbefore-mutant-survival-r76.txt`), so the red-before is real for these three classes.

### Facts checked for C1 that HOLD
- The three base mutants are one-hunk patches of the freeze bytes (V2) and the base selftest passes them (receipt).
- Real-tree census shape at freeze: 91 entries = 89 recheck-only + 2 both-header + 0 neither + 0 restoration-only; exit0 69 + exit1 22 = 91 (V7 agrees with receipt). The two both-header files are `claim-gates.md` and `claim-package-contract.md`, both prefixed, so (iii) is a behaviour-preservation fixture for the real tree and does not change A4 parity by itself.
- The round-75 motivation items (R75-1, R75-2, R75-3) appear in `corpus/lessons/round-75-verifier-spotcheck.md:103-105`.

---

## C2 — F54 admission on S111

### F10 — BLOCKER — B5 cannot pass on the committed manifest
- V12: `source-recheck.py --manifest … --source S111` exits 2. The first quote, `Q01-api-version` = `API (1.0)`, normalizes to 9 characters, below `MIN_QUOTE_CHARS = 12`. The instrument aborts before the sha check, so the `S111:sha256 OK` line B5 names is never printed.
- This is the R123 class already recorded in round 75 (`source-recheck.py` enforces `MIN_QUOTE_CHARS=12`); the round-76 manifest reintroduces it with a 9-character pin.
- Cascade, which is the important part:
  - F54's knowledge entry will carry the same recheck shape as F51 (`source-recheck.py --manifest … --source S111`, V-check: `osv-post-v1-query-contract.md:5`). It will therefore exit 2.
  - B3's `FRONTIER-PASS F54 … pass=57`, `problem-rows=0`, `exit=0` fails (`frontier-recheck-count.py` runs the recheck and records `recheck-exit-2`).
  - A2's drift expectation becomes entries=92, exit0_foreign=**69**, exit2_foreign=**1** — not the stated `exit0_foreign=70`, and not "all other fields unchanged". So the drift arithmetic in C1 is right only if this blocker is fixed (see F1 and the F5 drift note below).
- Fix class: a quote of ≥12 normalized characters that the capture carries (a two-line span such as `API (1.0) Download the OpenAPI specification` normalizes across the line break and occurs once), or drop Q01 and state the API-version clause from Q03 context. Choice is the L1's; I am not rewriting the manifest.

### F11 — GAP — B5's "anchor-located" clause is not enforced for unique quotes
- `source-recheck.py` consults the anchor only when `occurrences > 1` (`anchor_verdict` is computed and then ignored for unique quotes). V13 demonstrates: Q04 anchor=99 prints `OK occurrences=1 anchor=OUT-OF-RANGE` and Q12 anchor=1 prints `OK occurrences=1 anchor=1-BROKEN`, exit 0.
- All 13 manifest anchors are correct today (V11), so the B5 text is true of the data but not of the command. B5 says the command reports "all 13 quotes anchor-located" — it does not; it reports the broken anchor and passes it. Either add an anchor check for every quote in the instrument (a change to a frozen-tool-owned instrument, which needs its own claim) or narrow B5 to "occurrences=1 and anchor verified by CORPUS recheck (V11)".

### F12 — BLOCKER — the endpoint-name clause is already held ground (M71-3 class)
- The statement's six-request surface names — `POST /v1/query`, `POST /v1/querybatch`, `GET /v1/vulns/{id}`, `GET /v1experimental/importfindings`, `POST /v1experimental/determineversion`, `POST /v1experimental/ubuntu/binary-to-source` — are already in the lane's held ground:
  - S108 (round-73, tier A, F51) lines 4-9: the same six lines in the navigation (V15). Lines 4-9 are the page's left nav, which is the same site nav as S111.
  - F51 `osv-post-v1-query-contract.md:75`: "the other endpoints in the page's navigation (POST /v1/querybatch, GET /v1/vulns/{id} and the experimental endpoints, S108.txt:5-9). They are listed, not described." The lane already records these names as held and lists the S111 overview as the unheld remainder (line 74).
  - S080 (round-50, F31) lines 146, 185, 190, 205: `https://api.osv.dev/v1/vulns/<ID>` (V16).
- The kill rule for C2 names this exact class: "a distinctness failure (ground already held from S080/S108 or any other row) … = NOT VERIFIED". As frozen, the endpoint-name clause fails it.
- What is honestly new on S111: the sentence "There are six different types of requests" (line 28) and the one-line descriptions of the six at lines 29-34, including the three `(Experimental)` labels; the API (1.0) and Download-OpenAPI lines (21-23); the rate-limit question and its no-limits answer (35-36). Those are the ground to claim. The endpoint names must be cross-referenced to S108.txt:5-9 and S080, not claimed as new.

### F13 — GAP — the endpoint paths are not located at the cited anchors and one literal is not verbatim
- `located_anchors` (manifest Q01-Q13) are lines 21-39. The paths appear only at nav lines 4-9 and TOC lines 42-47 (V-grep on S111). None of the 13 pinned quotes is a path (Q03-Q09 are descriptions). So the statement's six-path clause has no pinned quote in the manifest at all.
- The determineversion path is not verbatim in the capture: lines 8 and 46 read `POST /v1experimental/ determineversion` (a space from the capture's whitespace handling). The statement's `POST /v1experimental/determineversion` therefore does not occur in `S111.txt`.
- Fix class: either anchor the paths to lines 4-9 and 42-47 with the space normalized and state why, or limit the statement to the descriptions the manifest pins. Under the kill rule's "not located in the capture" clause this is NOT VERIFIED as written; I rate it GAP because the paths are located in the page's nav, just not at the stated anchors.

### F14 — GAP — line 39 is also held ground and is not declared as such
- The manifest pins Q13 (`We recommend using HTTP/2 for queries that may result in large responses (e.g. big OSV Linux queries).`) at S111 line 39. S108 line 148 holds the same recommendation (round-73 manifest Q29: "We recommend using HTTP/2 for queries that may result in large responses.").
- B6 cross-references line 38 as held and says nothing about line 39. The located-anchors list includes 39 as new ground. M71-3 class: add line 39 to the held cross-reference list.

### F15 — GAP — B6 (distinctness) has no named command; the subject sweep is not recorded
- B6 is a prose predicate ("names only clauses located … at lines 21-36 …"). No command enforces it. R121 requires a named check; R114 names the sweep: `grep -n '<organisation>\|<programme>' corpus/SOURCES.md corpus/knowledge/*.md` before freeze, with a per-hit verdict after.
- The OSV subject files (freeze, V16-style grep for `osv.dev`): `corpus/README.md`, `corpus/SOURCES.md`, `knowledge/osv-affected-range-events.md` (F31), `knowledge/osv-post-v1-query-contract.md` (F51), `knowledge/openssf-scorecard-checks.md` (F35, OpenSSF Scorecard docs referencing osv.dev), and captures S080, S086, S108 plus the round-76 pair. The sweep must cover those, not only S080/S108.
- "Same organisation" also reads as Google (`google.github.io`, `projectzero`, Google Cloud VRP F26, Big Sleep F40/F41). The sweep should record that subject boundary.

### F16 — GAP — B7's "six inherited W04 warnings allowed" is a count the command does not enforce (R123 class)
- `sources-census.sh validate … kasegi` predicate: exit 0. A seventh W04 would still exit 0. "Six … allowed" is a ceiling without a measured bound (R123).
- Fix: `validate … | grep -c '^kasegi.*W04'` equals 6, named in B7.
- Note (V17): an S111 row with a URL unique in the fleet adds no W04/E04 (only Registry rows enter the URL scan, and the lead bullet at SOURCES.md:175 is not a Registry row). I did not execute validate (V18), so this is by reading.

### F17 — GAP — B1 and B2 letters need named commands and a removal rule
- B2 says "`LC_ALL=C sort -c` clean, set-equal to the corpus/knowledge directory" with no command. `recheck-audit.py` (lines 45-47, 292) reads `knowledge-expected.txt` when present, so an instrument consumer exists but B2 does not name it. Name the sort and set-diff commands.
- B1 says "exactly one added S-row and zero removed rows". The round-74 lead bullet at `SOURCES.md:175` is the same URL; when the L1 admits S111 that bullet is normally closed. Its removal is not an S-row removal, so B1 is silent. Name the rule (the lead bullet is closed or kept as a non-row note).

### F18 — GAP — cross-entry contradiction on the rate-limit boundary is not addressed
- F51 (`corpus/README.md:1159`, `osv-post-v1-query-contract.md:71-75`) states the S108 page has no rate-limit sentence and "a reader must not supply either from the OSV overview page or another tracker". F54 admits "Currently there are no limits on the API." from that overview page as ground.
- Admitting F54 makes the F51 boundary text stale. B6 says the rate-limit clause is new ground, which is correct, but no predicate or non-claim draft reconciles F51's instruction. The L1 must amend F51's README row and knowledge line 71 in the same landing, or F54 contradicts the lane's own instruction to readers.

### F19 — NOTE — tier A is honest for this row, with a scope condition (attack item 4)
- Provenance: the OSV.dev project's own API overview, same publisher as S108 (tier A, F51). Tier A is the right tier for first-party provenance; a tier-B label would understate it.
- But the admitted clauses are one-line index/nav statements. They support descriptive teaching ("six request types, three marked experimental"; "no rate limit is stated, with a point-in-time answer dated 2026-11-05"), not a contract. The row's `teaches` must not go beyond that, and the F12/F13 correction is the condition that makes tier A honest. If the row keeps teaching the endpoint names as new, tier B is the honest label.

### F20 — NOTE — literal drift in the statement
- Statement: "API 1.0". Capture (and manifest Q01): `API (1.0)`. Harmless, but B6 is a literal reading; quote the capture form.

### C2 kill-rule complement (answer to attack item 2)
- The kill rule's named failures are all detectable: B5 fails at once (F10), the distinctness failure is the F12 class, and "after-counter not reproducing" is caught by B3/B4. So the complement is closed for the counters — but the frozen B5 cannot pass at all, so the claim's own "reproduce at landing" test would return NOT VERIFIED before any distinctness question is reached.

### C2 ground checks that HOLD
- S111 sha256 `6f92e5b7…` and 1810-byte/48-line snapshot match the claim (V10).
- All 13 manifest quotes are exact at their declared anchors (V11) and occur once (V14).
- The 32 MiB clause (S111 line 38) is held: S108 line 148 with the same text, round-73 manifest Q27/Q28 anchor 148 (V15). The "no limits" statement (line 36) is not held as evidence; the SOURCES lead line 175 quotes it but explicitly says "not evidence", and the lead is not a registry row.
- The OSV overview page was lead-only at round 74 (`corpus/lessons/round-74.md:13`); the round-76 capture's sha matches the round-74 lead's converted sha, as the claim says.

---

## A2 drift expectation (attack item 5)

Is `entries=91 → 92`, `exit0_foreign=69 → 70` exactly right?

- Arithmetic: yes, if and only if the one new file is a cd-prefixed recheck that exits 0 from a foreign cwd. C2 adds exactly one `corpus/knowledge/*.md`, so `entries` becomes 92, and the other fields stay 0 (V7: no neither or restoration-only entries today).
- As frozen it is wrong: the F54 recheck (F10) exits 2, so the drift is `entries=92 exit0_foreign=69 exit1_foreign=22 exit2_foreign=1`, which breaks A2's "all other fields unchanged" and the RESULT line (`nonconformant`).
- The expectation also depends on the C1-landing revision (F1). Once F10 is fixed and the landing order is named, `entries=92 exit0_foreign=70` is the right value.

---

## Universal-sentence sweep (attack item 3), consolidated

- C1: "ONLY" (i), "any" (iii), "load-bearing" (ii), "no file outside" (A5). Bounded only by fixtures and by no command (F5, F7).
- C2: "names only clauses located" (B6) — not enforced by any command (F15); "six … allowed" (B7) — not enforced (F16); "all 13 quotes anchor-located" (B5) — not enforced for unique quotes (F11); "the page has none" phrasing appears in S108's row, not in the claim, and is consistent with S111 line 36 only once F18 is reconciled.

## Summary of routed items for the L1

1. Name the landing order of C1 and C2 with commit revisions (F1, F5 drift note).
2. Fix the S111 manifest Q01 so the recheck can exit 0 (F10); B5/B3 and A2 depend on it.
3. Cross-reference the endpoint names and line 39 to S108/S080 (F12, F14) and anchor or drop the endpoint paths (F13); decide tier A with the teaching limit (F19).
4. Make the counter's case count and selftest kill an assertion (F2, F3); commit the amended-mutant recipe (F3b); narrow or extend the kill rule (F4).
5. Add the registry-pin measurement (F6) and the B2/B5/B7/B6 command names (F11, F15, F16, F17).
6. Reconcile F51's overview-page boundary text (F18).
