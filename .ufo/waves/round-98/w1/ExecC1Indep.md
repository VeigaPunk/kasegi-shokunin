# ExecC1Indep — round-98 w1 — independent re-derivation of C1's census numbers

Seat: `ExecC1Indep` (leaf, read-only verifier). Claim under test: **C1
`depth:verifiability`** — the citation census of record is a reading of a named
revision. Lane HEAD at verification time: `e2d3de7b847f8e9bac72a5bc4dea455ea051cf1a`
(the C1 landing; detached HEAD). Extract under test: `git archive
e2caf4a1561b544a6ea684b0bcfa975f7e7f6061` (the C2 landing, named by the census's
`measured-at:` line).

**VERDICT: AGREE — delta 0 on every pinned and host-inclusive figure, and 0
per-citation class/scope disagreements across all 7961 citations.**

---

## 1. What I did (method)

I did **not** import or run the lane's `resolve.py` / `census-at-rev.py` to
produce my numbers. I wrote my own census (`mycensus.py`, receipt) implementing
the extraction + classification rule as documented in the lane instrument
docstrings, over a `git archive e2caf4a1…` extract at
`/fast/scratch/hyaku/kasegi-r98/ExecC1Indep/ext`:

- Scope: `SKILL.md` + `corpus/**/*.md`, excluding
  `corpus/instruments/citation-survival.md` (371 files scanned: 1 + 370).
- Extraction: every backticked span `` `tok` ``, strip trailing `.,;:`, path-like
  rule (extension / trailing `/` / leading `~/` or `/` / contains `/ < { ~ ..` /
  `:NN[-MM]` anchor tolerance; space allowed only with `/`; `http`, `xd://`,
  `skill://` excluded).
- Classification: `INTERNAL` = lane-relative token (no leading `~`/`/`, not a
  bounty/mirror prefix) that exists in the extract, with the documented
  literal → brace → brace-glob → glob existence ladder. I computed all four
  classes (INTERNAL / RESOLVES / MIRROR-EQUIVALENT / GONE) so I could check both
  the pinned (INTERNAL-only) and host-inclusive rates.
- Per-scope totals: SKILL = citations appearing in `SKILL.md`; CORPUS = appearing
  in `corpus/`; LANE = union. Numerator for pinned = `INTERNAL` only;
  host-inclusive = `INTERNAL + RESOLVES + MIRROR-EQUIVALENT`; host-owned =
  `RESOLVES + MIRROR-EQUIVALENT`.

**Memory-safety note (methodology, not a numbers change):** the lane's
`resolve.py` uses eager `glob.glob(...)` which materializes full match lists; on
this extract (19,061 files, `.ufo/` = 18,281) that peaks at ~2.5–3.3 GB RSS per
process. With 8+ fleet seats running `resolve.py` concurrently the host's
`earlyoom` (active) SIGTERM-killed my first two runs and the first `--check`
attempt (`CENSUS-CHECK fail reason=resolve-rc-15`). I switched my existence check
to `glob.iglob` (lazy generator, identical match set, O(depth) memory) — the
existence boolean is unchanged because classification only tests method
truthiness, never the resolved path. I then proved equivalence empirically: the
per-citation diff against `resolve.py`'s own TSV (§4) shows **0 disagreements**.
For the `--check` re-run I set `PYTHONMALLOC=malloc MALLOC_TRIM_THRESHOLD_=131072`
in the environment (inherited by the `resolve.py` subprocess) so its allocator
returns memory to the OS; this does not alter any classification result.

## 2. Independent census output (my code, no lane instrument)

Command: `python3 -u -B mycensus.py /fast/scratch/hyaku/kasegi-r98/ExecC1Indep/ext`
(full output in `mycensus.out` receipt):

```
distinct citations: 7961 (total occurrences: 16435; citing files: 334)
class totals: {'GONE': 5294, 'INTERNAL': 2589, 'RESOLVES': 78}
host-owned (RESOLVES+MIRROR-EQUIVALENT): 78

scope   pinned(INTERNAL)        host-inclusive
SKILL   162/732   = 22.13%      166/732   = 22.68%
CORPUS  2551/7559 = 33.75%      2629/7559 = 34.78%
LANE    2589/7961 = 32.52%      2667/7961 = 33.50%

pinned rate (INTERNAL only; revision-stable): SKILL 162/732 = 22.13% | corpus 2551/7559 = 33.75% | lane 2589/7961 = 32.52%
host-inclusive rate (resolve.py's definition): SKILL 166/732 = 22.68% | corpus 2629/7559 = 34.78% | lane 2667/7961 = 33.50%
host-owned inputs: 78
```

## 3. Comparison with the census header's pinned line

Committed census `corpus/instruments/citation-survival.md` (HEAD = C1 landing;
`git diff e2d3de7 -- corpus/instruments/citation-survival.md` is empty, i.e.
byte-identical to the landing), lines 5–8:

```
measured-at: e2caf4a1561b544a6ea684b0bcfa975f7e7f6061
pinned rate (INTERNAL only; revision-stable): SKILL 162/732 = 22.13% | corpus 2551/7559 = 33.75% | lane 2589/7961 = 32.52%
host-inclusive rate (resolve.py's definition): SKILL 166/732 = 22.68% | corpus 2629/7559 = 34.78% | lane 2667/7961 = 33.50%
host-owned inputs: 78 absolute-path citations resolve outside the lane ...
```

Side-by-side (mine vs header):

| figure | my census | header pinned line | delta |
|---|---|---|---|
| pinned SKILL | 162/732 = 22.13% | 162/732 = 22.13% | 0 |
| pinned corpus | 2551/7559 = 33.75% | 2551/7559 = 33.75% | 0 |
| pinned lane | 2589/7961 = 32.52% | 2589/7961 = 32.52% | 0 |
| host-incl SKILL | 166/732 = 22.68% | 166/732 = 22.68% | 0 |
| host-incl corpus | 2629/7559 = 34.78% | 2629/7559 = 34.78% | 0 |
| host-incl lane | 2667/7961 = 33.50% | 2667/7961 = 33.50% | 0 |
| host-owned | 78 | 78 | 0 |
| distinct citations | 7961 | 7961 (body line 20) | 0 |
| occurrences | 16435 | 16435 (body line 20) | 0 |
| citing files | 334 | 334 (body line 14) | 0 |

Body class table (lines 24–30): RESOLVES 78 / MIRROR-EQUIVALENT 0 / GONE 5294 /
INTERNAL 2589 — matches my class totals exactly.

## 4. Lane instrument re-run (`census-at-rev.py --check`)

Command:
```
PYTHONMALLOC=malloc MALLOC_TRIM_THRESHOLD_=131072 python3 -B \
  corpus/instruments/census-at-rev.py --lane . \
  --check corpus/instruments/citation-survival.md --work <scratch>
```
Observed (receipt `c1check.out`):

```
CENSUS-CHECK pass rev=e2caf4a1561b544a6ea684b0bcfa975f7e7f6061 skill=162/732 corpus=2551/7559 lane=2589/7961 host_owned=78
RC=0
```

The first attempt (default allocator, fresh `--work`) failed
`CENSUS-CHECK fail reason=resolve-rc-15 rc=2` after 218 s — `earlyoom` SIGTERM
(killed `python3 -B corpus/instruments/resolve.py …`, VmRSS 1877 MiB, at
18:17:18; journal `earlyoom[1368]`). This is a host memory-exhaustion artifact of
running the whole wave's `resolve.py` copies concurrently, not a defect in the
landed instrument; the re-run with the malloc allocator completed rc=0 with the
same figures.

## 5. Per-citation cross-check (strongest evidence)

I diffed my 7961 per-citation rows (`mycensus-rows.tsv`) against the
`citation-survival.tsv` that `resolve.py` generated inside the `census-at-rev`
extract (`c1work2/tree-e2caf4a1561b/corpus/instruments/citation-survival.tsv`),
matching on the tab-safe trailing fields exactly as `census-at-rev.py` does
(class = cells[-7], scopes = cells[-1]):

```
resolve.py rows: 7961   my rows: 7961
citation sets equal: True
only-in-resolve: 0   only-in-mine: 0
class disagreements: 0
scope disagreements: 0
resolve.py class totals: {'GONE': 5294, 'INTERNAL': 2589, 'RESOLVES': 78}
my class totals:         {'GONE': 5294, 'INTERNAL': 2589, 'RESOLVES': 78}
```

Zero disagreements on both class and scope for every one of the 7961 distinct
citations. My independent implementation is behaviorally identical to
`resolve.py` on this revision.

## 6. P3 supporting checks (ancestry + no scratch path)

- `git merge-base --is-ancestor e2caf4a1561b… HEAD` → ancestor (HEAD =
  `e2d3de7b…`). PASS.
- `grep -c 'tree-e2caf4a1561b' corpus/instruments/citation-survival.md` → `0`.
  PASS (the erratum-corrected check).
- `grep -c '/fast/scratch' corpus/instruments/citation-survival.md` → `0`.
  PASS (also clean; the body carries no scratch path).
- `Lane root:` line (line 13) names the lane root and the measured revision.

## 7. Observations (not part of the AGREE/DISAGREE verdict)

1. **Assignment-brief numbers are stale relative to the landing.** The brief I
   was given states the regenerated census records "corpus 2550/7556, lane
   2588/7958". The actually-committed census header (and my independent
   re-derivation, and `--check`) all read **corpus 2551/7559, lane 2589/7961**.
   SKILL (162/732) and host-owned (78) match the brief; corpus/lane differ by
   {+1 numerator, +3 denominator}. The frozen `claims.json` C1 statement does
   **not** hardcode these post-landing figures (it is mechanism-based: "the
   pinned line equals census-at-rev.py's re-measurement"), so no claim limb is
   violated — but the brief's summary numbers should be read as a pre-final
   draft. My verdict is against the **landed** census, which is correct.
2. **Frozen `harness_sha256` does not reproduce against any committed harness
   blob.** `claims.json` (both at freeze `12bb2f9` and at landing `e2d3de7`)
   pins `harness_sha256 = d39a1fc8…`. The harness blob
   `.ufo/waves/round-98/controls/c1-controls-r98.py` hashes to `0488d796…` at the
   freeze commit `12bb2f9` and to `d9713268…` at the landing `e2d3de7` (the
   landing added 4 lines: a `git checkout -q <base>` + error branch). Neither
   matches `d39a1fc8…`, and no other committed revision of that path matches it
   either (checked `e2caf4a1`, `1af0f28`, `8215985`, `1fff7bf`, `8b5c909`). By
   contrast the frozen `instrument_sha256` **does** reproduce post-erratum:
   `census-at-rev.py` at HEAD = `66383371…` = the landing claims.json pin. This
   is a pin-integrity observation for the integrator, outside my C1-numbers
   verdict; the pre- and post-fix control receipts themselves both print
   `C1-CONTROLS-RESULT pass controls=8 rc=0`.
3. **Host infrastructure caveat.** `earlyoom` is active and the host was at
   ~0–9% memory/swap free during this wave; any seat running the eager-glob
   `resolve.py` over the 19k-file extract risks SIGTERM. This affects wall-clock
   reproducibility of `--check`, not correctness. `PYTHONMALLOC=malloc` (or
   `glob.iglob`) avoids it.

## 8. Receipts

`.ufo/waves/round-98/w1/ExecC1Indep-receipts/`:
- `mycensus.py` — my independent census instrument (iglob variant).
- `mycensus.out` — its full stdout (the numbers in §2).
- `mycensus-rows.tsv` — 7961 per-citation rows (citation, class, scopes,
  occurrences; note: a citation containing a literal TAB shifts naive column
  parsing — use `rsplit('\t',3)`; the in-memory totals in `mycensus.out` are
  authoritative and match `resolve.py`).
- `compare.py` / `compare.out` — the per-citation diff vs `resolve.py`'s TSV.
- `c1check.out` — the `CENSUS-CHECK pass … RC=0` output.
- `analyze.py` — the glob-needs domain breakdown (rel=7657, abs=228, bounty=46,
  mirror=30; rel literal-INTERNAL=2511, rel glob-needed=985, rel brace=185).

Scratch `/fast/scratch/hyaku/kasegi-r98/ExecC1Indep` is removed after this report
is written (receipts copied first). No lane-repo writes were made; all git
commands were read-only (`rev-parse`, `log`, `show`, `diff`, `merge-base`,
`archive`).

## VERDICT

- C1 pinned census numbers (SKILL/corpus/lane, pinned + host-inclusive +
  host-owned): **AGREE** — independent re-derivation matches the committed
  header and `census-at-rev.py --check` exactly; delta 0; per-citation diff vs
  `resolve.py` = 0 disagreements / 7961.
- C1 `measured-at:` revision ancestry + no-scratch-path (P3): **AGREE** —
  `e2caf4a1…` is an ancestor of the C1 landing tip; both scratch-path greps = 0.
- Assignment-brief corpus/lane figures (2550/7556, 2588/7958): **DISAGREE with
  the brief, AGREE with the landing** — landed census is 2551/7559, 2589/7961;
  brief numbers are stale (no frozen-claim limb hardcodes them).
