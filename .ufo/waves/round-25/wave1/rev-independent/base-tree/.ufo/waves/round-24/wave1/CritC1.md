# CritC1 — falsification of C1 (depth:verifiability), round 24

Read-only seat. Claim under test: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/claims.json` C1.
Base `d0a3f6a`; observed tip `c2480b1`; no installs, no repo writes, all scratch under `/tmp`.

Measurements are against the working tree as of this review; siblings were landing edits concurrently (`git status` at measurement: ` M corpus/instruments/resolve.py`, ` M corpus/instruments/source-recheck.py`, ` M corpus/source-snapshots/round-23/manifest.json`, `?? corpus/instruments/{capture-source,resolve-dispatch-check}.py`, `?? resolve-dispatch-fixtures.json`, `?? corpus/source-snapshots/round-24/`, `?? corpus/knowledge/authorised-testing-rules-of-engagement.md`). The round-23 manifest still holds 4 records (S018, S029, S030, S031) and counter A still reads 3/8; see F9 for the instrument-bytes drift.

## Verdict summary

| Q | Question | Verdict |
|---|---|---|
| 1 | Is counter A a real measurement of the surface? | **No.** The instrument is honest; the counter measures an editable command line, not manifest coverage. 8/8 reachable with zero new captures. |
| 2 | Can a seat reach 8/8 by editing recheck lines to `true`? | **Yes, measured 8/8.** No rule in the claim or in CORPUS/SKILL blocks it; Q7 bans prose, not `true`. |
| 3 | Can counter B's matrix distinguish GONE-for-everything? | **Yes for that mutant (1/8 measured)** — but it cannot distinguish "fixed" from "over-broad": the fix it certifies credits a non-citation and no case exercises that spelling (R10). |
| 4 | Does C1 name the axis by surface (R7) or by a number? | **By surface** (`surface_changed` names both instruments and their artifacts). R7's binding and disclosure halves are unsatisfied. |
| 5 | Is C1 causally separable from C2? | **On the success path yes; not robustly.** Shared manifest is a single point of failure and C1's 8-entry list goes stale the moment C2 admits F09. |

Weakest sentence (C1 `predicate`): *"At round end every one of the eight Frontier knowledge entries runs its own `recheck:` command and exits 0 from committed captures"* — "its own" is undefined and the seat edits that line by design; measured below, both `true` and a re-point at an already-captured id reach 8/8.

## Findings

### F1 — Counter A's after-target is reachable with zero new captures (blocker)

Reproduced the before state exactly (3/8, F06+F07+F08 = 0, F01–F05 = 2), then replaced every one of the eight `recheck:` lines with a call to an id that is **already** captured in `corpus/source-snapshots/round-23/manifest.json`:

```
cd /tmp && cp <lane>/corpus/knowledge/{8 frontier}.md c1repoint/ && sed -i 's|^recheck: .*|recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S018|' c1repoint/*.md
<same loop as claims.json counter_A>
→ total_zero=8
```

No manifest work, no S001–S015 capture, after-target met. The named surface is "the captured-source rechecker's manifest coverage for S001-S015"; the measured object is the exit status of eight lines the round's own plan tells the seat to rewrite (`wave1-spec.json` item 11: "a `corpus/source-snapshots/round-24/manifest.json` covering S001-S015" plus re-pointed F01–F05 lines). Counter A cannot tell a widened manifest from a narrowed pointer.

### F2 — Which code path decides exit 0, and what exit 0 proves (Q1 detail)

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py` (working-tree bytes, sha256 `65df28cc69b19df9e6f27096e4aed053bed5725863674d5e0c739f6cd9b859eb`; HEAD bytes are `5f72b4c0…` — see F9):

- `load_manifest` (43-74) validates **every** record's id before any selection; any invalid/duplicate id → `manifest UNAVAILABLE`, `return 2`.
- `recheck` (163-185): id not in the list → `{id}:source UNAVAILABLE reason=not-listed`, `return 2`.
- `check_source` (76-161): bad path/sha/quotes → `2`; a quote shorter than `MIN_QUOTE_CHARS = 12` normalized chars → `2` (129); sha mismatch → `1` (127); every quote must be found raw or under the declared markup/whitespace normalization (139-155) → `0`.

Measured on synthetic manifests (`/tmp/c1man/*.json`, one record, `--source S001`), current bytes:

```
-- empty-quotes     S001:manifest UNAVAILABLE reason=missing-quotes                 exit=2
-- no-quotes-key    S001:manifest UNAVAILABLE reason=missing-quotes                 exit=2
-- trivial-quote    S001:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence       exit=2
```

So a listed-but-empty record cannot pass, and the degenerate one-character quote that passed at freeze time no longer passes. The instrument is not the defect; the counter's non-binding to the entry's own source ids is.

Exit 2 also conflates two causes. The claim's command has no `cwd`; run from the fleet root it still scores 3/8, but F01's exit 2 is `python3: can't open file '/home/vgpnk/Projects/shokunin/corpus/instruments/source-recheck.py'` — not `not-listed`. The before-number is right by accident; the counter cannot state *why* an entry fails.

### F3 — Counter B's before-state is a flag the frozen command does not carry (kills "one command from committed bytes")

- Frozen command, run now in the lane: `python3 corpus/instruments/resolve-dispatch-check.py --fixtures corpus/instruments/resolve-dispatch-fixtures.json` → `cases=8 pass=8 exit=0`. The `4/8, exit 1` of `before_expected` is only obtainable with `--resolver .ufo/waves/round-24/c1-baseline-resolver.py`, a flag absent from the frozen text, and I reproduced it there (`cases=8 pass=4 exit=1`; the baseline copy is byte-identical to `git show HEAD:corpus/instruments/resolve.py`, sha256 `690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d`).
- The three artifacts are untracked: `git ls-files corpus/instruments/` does not list `resolve-dispatch-check.py` or `resolve-dispatch-fixtures.json`; `git status --porcelain` shows them as `??`, and `.gitignore` covers only `.ufo/interactive-sessions/`. So before/after is not "reproducible from committed bytes by one command" as the kill rule requires — it is reproducible from a byte-identical but uncommitted copy plus an unwritten flag.

### F4 — The fix that scores 8/8 credits a non-citation (harm to the axis it claims)

Same tree (`git archive HEAD` → `/tmp/c1census/tree`), same env, only the resolver bytes differ (baseline vs working-tree `resolve.py`):

```
base  : | INTERNAL | 215 | … | GONE | 1446 |   lane total 223/1669 = 13.36%
fixed : | INTERNAL | 216 |                    lane total 224/1669 = 13.42%
only changed tsv row: {}  GONE → INTERNAL  /tmp/c1census/tree/  method=brace  occ=2
```

`{}` is a JSON literal, not a path: `corpus/knowledge/triage-thresholds.md:71` ("`leases` default is `{}` when `fleets/leases.json` is absent/unparseable") and `:366` ("so `{}` is schema-valid"). Mechanism, from the fixed bytes:

```
classify('{}') → ('INTERNAL', '<lane>/', 'brace', 'rel')
brace_expand('{}') → ['']
```

The retained empty alternative expands to the empty string; `classify` joins it onto the lane root (`resolve.py:243-283`, relative branch), the lane root exists, and the token is credited as an internal resolvable citation (`brace_expand` 170-183, `exists_any` 186-209). The census numerator therefore rises by one distinct citation for two non-citations. No fixture case exercises a braces-only spelling (`resolve-dispatch-fixtures.json` has `notes/{,sub}/a.md`, `notes/{sub,}/b.md`, `ops/{a,b}.mjs`, and glob/control cases only) — exactly the R10 gap: the matrix is evidence only for what it exercises. No out-of-root escape exists (the empty expansion yields the prefix, which is the lane root), so this is false credit, not a confinement break.

### F5 — Counter A is defeated by `true` (Q2)

```
cd /tmp && cp <lane>/corpus/knowledge/{8 frontier}.md c1probe/ && sed -i 's|^recheck: .*|recheck: true|' c1probe/*.md
<same loop> → all eight 0
```

Nothing in `claims.json` pins the line's content; nothing in `CORPUS.md`/`SKILL.md` does either (`grep -rn recheck CORPUS.md SKILL.md corpus/README.md` → one unrelated hit at `SKILL.md:169`). QUALITY Q7 blocks prose beginning "On each", not a no-op command. R7's "exercise the actual detector" is a reviewer backstop, not a condition the counter tests, so the claim's own kill rule never fires.

### F6 — Counter B's matrix vs a GONE-for-everything resolver (Q3)

Patched baseline with `classify` forced to `("GONE","","","rel")` (`/tmp/gone-resolver.py`) and ran the frozen matrix: `cases=8 pass=1 exit=1` — only `control-absent-face` passes. So the matrix is not vacuous for that mutant. Two defects remain: the fixture's own `why` for `control-absent-face` says such a resolver "passes only this control and the one below", but the case below (`control-glob-two-live-matches`) expects INTERNAL — off by one case; and the matrix passes the F4 regression, which is the realistic failure mode of this fix.

The path column does work as designed: baseline on `glob-dangling-first-match` returns `actual=INTERNAL path=<CASE>/lane/refs/a-lure.md`, `FAIL path_check=missing-path` — class alone would have passed, the resolved path falsifies it (`mirror-containment-check.py:222` path verdict, `:230` PASS gate).

### F7 — Axis naming under R7 (Q4)

C1 names the surface, not a number: `axis: depth:verifiability`, `surface_changed` names "the captured-source rechecker's manifest coverage for S001-S015, and resolve.py's brace/glob dispatch", and counter B executes the real detector on real CLI bytes. That half of R7 (`QUALITY.md:49`) holds.

The other half fails. R7 requires instrument-correctness claims to "report semantic before→after cases, and disclose unchanged source-availability scores". C1 discloses no availability score at all — and the availability score did not stay unchanged (F4: 13.36 % → 13.42 %, from false credit). Counter A reports aggregate exit counts, not the per-entry cases (which id, which quote) that would show the coverage actually widened.

### F8 — Separability from C2 (Q5)

Success path is separable: C1's after-target is reachable with C2 absent (F1 shows it reached with nothing landed at all), and C2's counters do not read C1's artifacts — measured baseline `8` admitted rows and `0` files matching `^source: S1[0-9][0-9] ` (`corpus/README.md`, `corpus/knowledge/*.md`), and C1's counter A hardcodes eight filenames, so F09 cannot enter it.

Two couplings survive:

1. **Shared file, global validation.** If C2's two new entries carry `recheck:` lines pointing at `corpus/source-snapshots/round-24/manifest.json` — the file C1 creates — then any id-level defect in that file fails *every* C1 selection: appending a duplicate-id record to a copy of the round-23 manifest yields `manifest UNAVAILABLE reason=duplicate-source-id`, `exit=2`, for a perfectly valid `--source S018`. C1's 8/8 then reads 0/8 through C2's error. Nothing in either claim fixes which manifest C2's entries must name.
2. **Predicate vs counter at round end.** The predicate says "every one of the eight Frontier knowledge entries"; the counter enumerates eight literal filenames. After C2 admits F09 the frontier set is ten, and C1 can report 8/8 while the two new entries' rechecks are broken. The predicate and the counter diverge exactly where C2 lands (the kumitate "one predicate, three places" rule).

Also in the frozen claim file, `assimilation.collision_map` points at `.ufo/waves/round-24/assimilation/renumber-map.tsv`, which does not exist — the directory holds `census-before.txt`, `collisions`, `reg-ids`, `staged-ids` (`S001…S005`, `S031…S035`; staged ids `S100+` are in `staged-ids`). C2's provenance pointer is dead as frozen.

### F9 — Counter A's instrument changes under the measurement, unpinned

At freeze the entry-deciding instrument was HEAD's `corpus/instruments/source-recheck.py`, sha256 `5f72b4c0c0766bb6a06e786d761495ef016ad3c29511f155a4961c9a71bbe12a`; the before receipt `.ufo/waves/round-24/c1-counterA-before.txt` was taken there. While this review ran, the working-tree file became sha256 `65df28cc…` (`git status` → ` M corpus/instruments/source-recheck.py`, +13/−3): it adds `MIN_QUOTE_CHARS = 12` (25, enforced at 129), `anchor_verdict` (74-97) and occurrence counting, so a quote that passed at freeze now exits 2 (`S001:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence`). C1 pins neither the instrument's sha nor its semantics, so its 3/8→8/8 straddles an uncommitted instrument change with no disclosure — the same class of defect R7 raises for `resolve.py` (r22 C1 was rejected for unchanged instruments; an instrument that changes silently mid-round is rejected for the opposite reason). Counter A re-measured on the current bytes: still 3/8 before, still 8/8 under both falsifiers (F1, F5).

## Smallest safe corrections

1. **Bind counter A to the entry, not the line.** Parse each entry's `source:` line (e.g. `corpus/knowledge/cvss-v4-severity-and-vector.md:2` → S001; Evidence cites S002) and require the recheck command to name a manifest record for **every** id the entry declares, each with a ≥5-word quote; fail if the command names fewer, or if a named record's quote set is shorter than the entry's evidence list. That kills both the `true` edit and the re-point in one rule.
2. **Amend counter B's command** to carry the two invocations it actually measures: `--resolver .ufo/waves/round-24/c1-baseline-resolver.py` → 4/8 and the plain run → 8/8; commit the harness, fixtures and baseline copy before scoring, so "committed bytes by one command" is true.
3. **Close the empty-expansion credit** in `classify`/`exists_any`: an expansion candidate that reduces to the prefix (the lane root) must not be credited unless the token itself names it; measured failing token `{}` at `corpus/knowledge/triage-thresholds.md:71,366`.
4. **Add the braces-only cases to `resolve-dispatch-fixtures.json`** (`{}`, `{nonexistent,}`) expecting `GONE`, so the matrix would have caught (3) — R10 compliance, and it corrects the `control-absent-face` `why` text ("passes only this control", measured 1/8).
5. **Re-scope the predicate** from "the eight" to the frontier set C2 lands, or state explicitly that C1's after-target is 8/8 on F01–F08 and F09's rechecks are C2's obligation; and give C2 its own manifest, or freeze C1's counter-A receipt before C2 appends to the shared file.
6. **Pin instrument bytes in the claim and in every receipt.** Counter A names no sha for `source-recheck.py` and its semantics changed mid-round (F9); counter B does print `resolver_sha256`/`matrix_sha256`/`checker_sha256` and is the model to copy. Any change to `source-recheck.py` after the before receipt invalidates the before→after pair and must be re-taken.

## Not verified

- Whether C2's drafted entries will actually point their `recheck:` at the round-24 manifest: the wave1 prompts are truncated in `.ufo/waves/round-24/wave1-spec.json` (item 13 ends at "docume…"), and no entry file exists yet under `corpus/knowledge/`.
- Round-end 8/8 for counter A: impossible to test now — `corpus/source-snapshots/round-24/` holds `S001.txt…` snapshots but **no** `manifest.json`, and F01–F05 still point at the round-23 manifest, so counter A reads 3/8 in the working tree at review time.
