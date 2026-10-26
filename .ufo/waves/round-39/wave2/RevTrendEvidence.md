# RevTrendEvidence — round 39 wave 2 (falsify) — trend-evidence receipt

Seat: RevTrendEvidence (leaf, reviewer; non-author of the round-39 deliverables — I wrote no
round-39 lane content). Date: 2026-10-26. Dispatch: L1 KasegiR39, hyaku run 9, wave 2 (falsify).
Refs: base `480b1a505a2dfc14a4f718d16d63808247214d0a`; claims freeze `dcd31701720a6a4929a32471a62011ed87103421`;
judged head J = `46c66c268502abd1b2c342fc71bf88ccf721845b` (the `export-ref=` of
`.ufo/waves/round-39/final-gates/all-gates.txt`); lane tip Y = `5006097a84305267c9a3e8c1e1d560e60fe41d37`;
`git diff --name-only J Y` → `.ufo/waves/round-39/final-gates/all-gates.txt` only (verified).
Erratum read: `claims-erratum-1.md` E1 (registry 59), E2 (r38 head 40-char), E4 (verification ref Y), E5 (non-vacuous semantics).
Claims read first, not edited. All paths below are relative to the lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless prefixed. Scratch
`/fast/scratch/hyaku/kasegi-r39/RevTrendEvidence/` removed before yield; no tool installs (pdftotext
already at `/usr/bin/pdftotext`; pacman untouched); no mutating git command anywhere.

Environment snapshot at measurement (matters for two live-state checks): lane `git status --porcelain`
= 6 untracked wave-2 entries (`final-gates/reds.txt`, `kasegi-r39-falsify.ready{,.dispatched}`,
`wave2-dispatch.json`, `wave2-run.err`, `wave2/`); `/fast/scratch/hyaku/kasegi-r39/` held 13 entries
(12 sibling seat dirs + the receipt run's `gates-work`); disk guard green (605G free on /fast).

---

## 1. Expansion — verdict: **improved** (verified at Y)

| Assertion | Evidence (command → observed) | Pointer |
|---|---|---|
| New admitted entry on uncovered ground, citing mined S057 | `corpus/knowledge/cisa-when-to-issue-vex.md` landed (144 lines, base diff +144/−0): `source: S057`, `verified-at: 2026-10-26`, `ground: F22`, executable `recheck:` line; 10 numbered claims + 8 rejected over-generalizations + falsifiable rule — far beyond the E5-#9 ≥10-line floor. Ground uncovered at base: no VEX-issuance entry existed; F21/S055 covers document content only, and the entry grounds the layer split from the capture (`component_not_present=1`, `vulnerable_code_not_in_execute_path=0`, … — FC-3) | `corpus/knowledge/cisa-when-to-issue-vex.md:3-6`, `:33-40` |
| Frontier F21 → F22 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → **22** (base 21 per `c2-controls/before.txt`); F22 row appended in `## Round-39 admission` (README:506), row shape `awk -F'|'` → NF=8 (F19/F20/F21 shape); main frontier table untouched (README diff base..Y = pure 28-line tail append, `pure-append=1` per G1) | `corpus/README.md:488-515` |
| Registry S057 row | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **59** (E1-corrected; base 55); S057 row at SOURCES.md:62: kind `docs`, tier `A`, status `mined`, opened `2026-10-26`, recheck `180d`, `awk -F'|'` → **NF=13**, exactly one `https://` token = manifest url; capture `corpus/source-snapshots/round-39/S057.txt` (275 lines, 17,971 B, sha256 `11c8d6d6…`) + `manifest.json` committed and bound (`capture-binding-check.py` → `records=46 bound=46 unbound=0`, exit 0) | `corpus/SOURCES.md:62`, `corpus/source-snapshots/round-39/manifest.json` |
| "New source kind docs A" | **Wording note, not a claim defect:** S057 is kind `docs` tier `A`, but `docs|A` is not a new kind — base registry already held 39 `docs|A` rows (→ 41 at Y). Frozen claims.json says only "tier A, kind docs", which is accurate; the item-spec phrase overstates. | `corpus/SOURCES.md` kind column counts |
| Capability table unchanged | `git diff base..Y -- SCORECARD.md` = single tail hunk `@@ -1528,3 +1528,52 @@` (the `## Round 39 result` section); `## Capabilities` table (SCORECARD.md:301-307) byte-identical; round-39 section states "Capabilities: no row enters this round". Whole-round no-harm: `git diff --numstat base..Y` shows **zero deletions** in all 277 changed files (+30,412/−0). | `SCORECARD.md:301-307`, `:1528+` |
| Do-nothing control (C2 before) | `c2-controls/before.txt`: frontier 21, registry 55, S057 0, knowledge 50, harness 24/24, binding 45/45, audit expected=50 — the after-state measured this seat (below) moves every counter | `.ufo/waves/round-39/c2-controls/before.txt` |

Independent re-measurement of the C2 counting commands at Y (this seat, not copied from receipts):
frontier **22**; registry **59**; `grep -rlE '^source: S057' corpus/knowledge | wc -l` → **1**;
`frontier-recheck-count.py` → `entries=25 pass=25 exit=0` incl. `PASS F22 knowledge/cisa-when-to-issue-vex.md ids=S057`;
`source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057` → `S057:sha256 OK` +
`Q1..Q4 OK … occurrences=1 anchor=<n>-ok`, exit 0; `capture-binding-check.py` → `records=46 bound=46 unbound=0` exit 0;
`recheck-audit.py --quiet` → `expected=51 missing=0 unexpected=0 exit=0`; `ls corpus/knowledge/*.md | wc -l` → **51**;
`sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `W04 S028`, `W04 S029`, `ok`, exit 0
(standing warnings only, no new code). No C2 kill clause fires.

## 2. Quality — verdict: **improved, with two defects** (both new this seat, routed to round 40)

Instruments re-verified by independent re-run (this seat executed the suite; work dirs under my scratch):

| Counting command (claims.json C1 / E4) | Observed at this seat | Matches frozen expectation? |
|---|---|---|
| `r39-closure.sh --export-ref Y` | `closed=6/8 exit=1` — G1-G5,G7 `closed=1`; **G6 `closed=0`** (`r39=present,work=inside,tolerated=…/RevTrendEvidence`) and **G8 `closed=0`** (`r37-closed=0,r37-exit=1`) | **No — but environmental, see below** |
| `r39-closure.sh --export-ref J` | `closed=5/8 exit=1`, G2 payload `receipt=0` (all G2 limbs 0), G6/G8 environmental reds | Yes per E4 (7/8 under a quiescent host; my 5/8 = 7/8 minus the two live-state reds) |
| `--export-ref 480b1a50…` (base) | `closed=1/8 exit=1` | Red ✓ (kill rule not fired) |
| `--export-ref 66703acaaff50529a35be49aa8759d04140720ad` (r38 head, 40-char per E2) | `closed=1/8 exit=1` | Red ✓ |
| plain run | `refusing to run against the live worktree … exit=2` | ✓ |

**Why G6/G8 red here is environmental, not a lane defect:** G6 scans the live scratch root and found 13
entries (12 sibling wave-2 seat dirs + `gates-work`) — wave 2 is in flight, so "kasegi-r39 holds nothing
but this run's --work" cannot hold now; the receipt's run happened at ~20:12Z (file mtime
`2026-10-26T20:12:08Z`, 4 s before its committing commit Y at `20:12:12Z`), and every sibling seat scratch
dir was created later (earliest ctime `20:17:53Z`, `gates-work` contents cleaned `20:17:59Z`), so the
scratch root held only the run's own work dir then and printed `closed=8/8 exit=0`. (The receipt's
declared `run-utc=2026-10-26T21:35:00Z` is itself defective — see D-T2.)
G8's embedded pinned-r37 run fails on the r37 suite's E9: `status-dirty=6 … closed=0` — the 6 untracked
wave-2 entries in the lane tree, again live state. I re-ran the pinned r37 suite directly
(`git show 2387dcf6…:corpus/instruments/r37-closure.sh`, sha256 `0da98e37…`) → `closed=13/14 exit=1` with
only E9 red (`status-dirty=6, scratch-root=absent`), all 13 tree-scoped checks green. Both live-state
guards are fail-closed by design; neither indicates a defect in the round-39 bytes. Residual: the C1
counting commands are only reproducible on a quiescent host (clean tree + clean scratch) — worth a line
in the next freeze's dry-run criterion (R34 class).

Selftest re-run (`--selftest --export-ref Y`): 34 mutants, **all rejected** — G1 4/4, G2 8/8, G3 2/2,
G4 6/6, G5 4/4, G6 4/4, G7 3/3, G8 3/3; forged judges 6/6 rejected, `accepted=0`; `cases=8 failures=2` in
my environment — the two positive failures are G6/G8 with the same live-state payloads above (the
receipt's quiescent run printed `cases=8 failures=0` with the same per-case mutant counts). Every graded
line carries `mutants=n/n, n≥1` and non-empty payloads (E5 #1 satisfied). Suite bytes sha256
`2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b` = receipt `suite-sha256=` ✓.

R1-R5 closure (routed defects from `corpus/lessons/round-38-verifier-spotcheck.md` §5):

| Defect | Closure evidence at Y | Status |
|---|---|---|
| R1 frozen self-referential predicate | M39-1 + erratum E4: verification ref Y = J + receipt; run at J documented `7/8` with G2 `receipt=0` — reproduced by this seat (G2 all-zero payload at J) | closed |
| R2 records overstate C1 at J | `Correction (round 39)` blocks: `corpus/lessons/round-38.md` ×1 (:311), `SCORECARD.md` ×2 (:1560, :1579), `SHONEN.md` ×1 (:190) — bare line-start form; **`LOG.md` ×0 in frozen form** (see defect) | **closed 4/5 records; LOG.md fails the frozen form** |
| R3 positive run not committed | Y-run transcript committed at Y (`final-gates/all-gates.txt`, `closed=8/8 exit=0` + graded selftest); G3 `added-quotes=0 covered=0 uncovered=0` — no untranscribed run quote in added lines | closed |
| R4 M38-5/M38-7 lack criteria | `corpus/QUALITY.md:309` R36 row cites M38-5/M38-7 with the criterion (grep `M38-5|M38-7` → 1) | closed |
| R5 suite coverage | G4 now checks distinct per-seat identities + zero-task dispatch RED (`dispatches=1 pairs=1 seats-ok=1`); G8 pins r37 bytes by commit AND digest and runs the pinned copy (`pinned-sha=1 export-copy=1`); selftest carries 34 new graded mutants. Residual: the 25 r38 surviving source mutants were not ported as r39 fixtures (routed to round 40 per `corpus/lessons/round-39.md` §Instrument attack findings) | closed for the named limbs; mutant port residual routed |

Corrections applied: M38-5/M38-7 criterion ✓ (R36); `⟨pending` markers in `corpus/lessons/round-39.md` → **0**;
ledger `## Round-39 dispositions` at `corpus/knowledge/considerthese-proposals-ledger.md:69` (after the
round-38 section at :45), 7 rows, proposal-1 and proposal-3 present (G7 `rows=7,proposal-1=1,proposal-3=1`).

No admitted entry failed re-check: harness 25/25 (every entry's recheck command exit 0), S057
source-recheck exit 0, recheck-audit `expected=51 missing=0 unexpected=0`.

### DEFECT (new this seat — quality)

**D-T1 — LOG.md correction misses the frozen line-start form; M39-2's own falsifier is red on LOG.md.**
E5 #7 freezes `grep -c '^Correction (round 39)' corpus/lessons/round-38.md LOG.md SCORECARD.md SHONEN.md`
with "at least 1 per file"; M39-2's `able to fail` cell states exactly that. Measured at J and at Y:
`git show J:LOG.md | grep -c '^Correction (round 39)'` → **0**; worktree same → **0**. The LOG correction
exists substantively but as a bullet: `LOG.md:1704` = `- **Correction (round 39):** …` (leading `- **`),
while the other three records use bare `Correction (round 39):` at line start. `LOG.md:1711` claims
"Correction (round 39) blocks in round-38 lesson, LOG, SCORECARD, SHONEN" — true in prose, false under
the frozen measurement. This is the M39-1/R1 class again (a frozen counting command not dry-run against
the landed bytes). Fix is one append-only line in LOG.md (or an erratum re-reading the command); routed
to round 40. No claim kill fires (C1's kill rule does not include the sweep), but the quality trend's
"corrections applied" is 4/5 records in frozen form, not 5/5.

Minor note: `final-gates/reds.txt` (base + r38-head red transcript) is **untracked** at this moment —
the reds are independently reproduced by this seat (table above), so C1 does not rest on the untracked
file, but it should be committed with the wave-2 integration or the pointer dangles.

**D-T2 — the C1 receipt declares a future run time.** `final-gates/all-gates.txt` carries
`run-utc=2026-10-26T21:35:00Z`, but the file's own mtime/ctime are `2026-10-26T20:12:08Z` (4 s before its
committing commit Y at `20:12:12Z`), and 21:35Z is still ~1 h in the future at this seat's measurement
time (host `date -u` = `20:24:53Z`, local `-03:00`). A run recorded at 21:35Z cannot have produced bytes
that existed at 20:12:08Z — the declared run time is impossible as written (mis-computed UTC conversion
or a pre-drafted placeholder that survived into the committed receipt). G2 does not validate `run-utc`,
so no kill fires and the substantive payloads stand (reproduced by this seat), but the receipt's declared
metadata is not truthful; route to round 40 (validate `run-utc` ≤ commit time, or derive it at run time).
Note the selftest fixture generator hardcodes `run-utc=2026-10-26T20:00:00Z` for synthetic receipts
(`r39-closure.sh:1150`, `g2_content()`) — a fixture constant, not the producer of the live value.

## 3. Discernment — verdict: **agree on admit and on both rejects sampled; no disagreement recorded**

Spot-check by re-opening the sources live (curl `-sS -L --max-time 90 -A kasegi-shokunin/1.0`):

| Item | Gate decision | Re-opened source (this seat, UTC 2026-10-26T20:22:55Z–20:23:36Z) | Agree/disagree | Reason |
|---|---|---|---|---|
| F22 / S057 CISA "When to Issue VEX Information" | **admit** | landing page `code=200 type=text/html bytes=54453` sha256 `4e6aa483c20013bb84d43d166e3f20c91fba63ece7c35861f6d95c8b61af0e4d` = manifest `landing_page.raw_sha256`; PDF `code=200 type=application/pdf bytes=235270` sha256 `cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99` = manifest `raw_sha256`; `last-modified: Mon, 06 Nov 2023 15:43:40 GMT`, etag `"39706-6097db7d52c78"` match manifest | **agree** | Byte-identical live re-open, and the committed capture is reproducible from the live PDF: `capture-source.py pdf_to_text(live bytes)` → `cmp` **IDENTICAL** vs `corpus/source-snapshots/round-39/S057.txt` (275 lines, 17,971 B, sha256 `11c8d6d6…`). Pinned Q1-Q4 verified (`occurrences=1`, anchors ok); Q1/Q4 text read in the reproduced capture (L13/L80 business decision; L183-191 inheritance caution + two-label allowance). Content supports the F22 layer claim (issuance/lifecycle/reaffirmation/inheritance beyond the CSAF profile). Tier A docs for CISA's own guidance is right; guidance-not-standard is scoped in the entry |
| S056 CISA "Minimum Requirements for VEX" | **reject** | landing page `code=200 bytes=49253` sha256 `67bafe172cb7ba5cee8938235abce59ca2a0069d96c65fa1078dc42f05a8eab8` = the row's recorded sha; PDF `code=200 bytes=1047967` sha256 `1e73325c674aa55c5665e3d2b647201acc46ee1fa9c8ee8bf88e4ff044f975c8` = the row's recorded sha | **agree** | My pdftotext repro of the live PDF carries the four statuses (affected 16, not_affected 7, fixed 3, under_investigation 4), all five justification labels in capitalized form (repro L287-289, L298-305), requirements version `1.0.0` (L57), and the cross-format statement "CSAF, CycloneDX, and OpenVEX can contain or be used to generate VEX documents" (L85-86). The committed S055 CSAF capture already carries the same vocabulary (all five labels present: 5/2/2/3/2; statuses 101/18/40/12) — the reject reason "its status and justification vocabulary is the one CSAF's VEX profile already mirrors (S055)" holds; the row also truthfully records "no lane capture, so no manifest record can anchor this row" |
| S058 OpenVEX v0.2.0 (bonus reject) | **reject** | raw spec at `main` `code=200 text/plain bytes=30580` sha256 `9375415ccb351260a998864cbeebbaff1808d1b09a306919b79cc75e5519f884` = the row's recorded sha | **agree** | Byte-identical to the r38 scout ledger; still fetched at the mutable `main` ref (no pinned commit); carries the same four statuses + five labels (all present) and `v0.2.0` ×6 — the reject reason (same vocabulary, community spec at a mutable ref, no release date) holds |
| junk-f22 negative twin | reject (control) | independent re-run of `source-recheck.py` on a scratch manifest binding the committed capture (path contained per the instrument's rule) | **agree** | `S057:sha256 OK` + `J1..J4 MISMATCH reason=quote-not-found`, **exit 1**; isolation control (same ids J1-J4, genuine capture sentences) → 4× `OK … occurrences=1`, **exit 0** — the rejection is discriminating, not shape-driven; matches the committed transcript `c2-controls/junk-f22-recheck.txt` |

Gate-vs-sample verdict: the admit's capture chain is byte-reproducible from the live web today, and both
sampled rejects carry recorded digests that still match live bytes with reject reasons that survive
content inspection. No disagree recorded; no overreach found in the tier/kind fields sampled.

---

## Verdict table (required deliverable)

| Trend | Verdict | Key pointers |
|---|---|---|
| **expansion** | **improved** (verified) | `corpus/knowledge/cisa-when-to-issue-vex.md` (new entry, `source: S057`, ground F22); `corpus/README.md:506` (F22 row; frontier 21→22, grep=22); `corpus/SOURCES.md:62` (S057 docs/A mined, NF=13, bound 46/46); SCORECARD `## Capabilities` untouched (single tail hunk, +30,412/−0 round-wide). Note: "new source kind docs A" is imprecise — `docs|A` had 39 rows at base |
| **quality** | **improved, with two defects** | Suite re-run this seat: G1-G5,G7 green at Y; base `1/8`, r38-head `1/8`, J `5/8` (G2 `receipt=0`, E4-documented), plain exit 2 — reds correct; selftest 34/34 mutants rejected, forged judges 6/6 rejected; R1/R3/R4/R5-named-limbs closed; corrections applied in frozen form in lesson/SCORECARD/SHONEN but **not LOG.md** (D-T1: `grep -c '^Correction (round 39)' LOG.md` = 0 vs M39-2's ≥1); **D-T2: receipt `run-utc=21:35:00Z` postdates its own mtime/commit (20:12:08Z/20:12:12Z)**; no admitted entry failed re-check (25/25, S057 exit 0, audit 51/51) |
| **discernment** | **agree (admit + 2 rejects sampled); no disagreement** | S057 live byte-identical (landing 54,453 B; PDF 235,270 B; capture `cmp` IDENTICAL from live PDF); S056 live byte-identical (49,253 B page; 1,047,967 B PDF) with reject reason confirmed against S055's vocabulary; S058 live byte-identical (30,580 B at mutable main); junk twin 4× MISMATCH exit 1 with discriminating isolation control |

Residual risk / verification gaps: (a) C1's live-state checks (G6, G8→r37 E9) make the frozen counting
commands non-reproducible green during any concurrent wave — by design, but the next freeze should
dry-run them under a populated scratch (R34 extension); (b) the 25 r38 surviving source mutants are not
ported into the r39 selftest (routed round 40); (c) `final-gates/reds.txt` untracked at measurement time;
(d) D-T1/D-T2 above (LOG.md frozen-form correction miss; future-dated receipt `run-utc`); (e) my G6/G8
reds are environment-conditioned — a quiescent-host rerun is the only way to print the receipt's
`closed=8/8 exit=0` verbatim, and this seat could not create one without touching lane state it must not
touch.

Report: .ufo/waves/round-39/wave2/RevTrendEvidence.md
