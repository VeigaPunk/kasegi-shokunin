# ScoutAnchor — R6 anchor audit for the C1 recheck re-point

Seat: L1Kasegi24.ScoutAnchor (read-only). Base read from committed bytes at lane `master` = `c2480b143120364728b40397926ffcf30a7309c8` (`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse master`). Frozen claims read first: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/claims.json` (C1 counter A: `for f in …; do r=$(grep -m1 '^recheck: ' corpus/knowledge/$f.md | sed 's/^recheck: //'); bash -c "$r"; done`).

Verdict up front: **the re-point is anchor-free.** No file in `SKILL.md`, `corpus/`, or `plans/` cites any of F01–F05 with a line number, so a line-4 edit cannot break a live anchor. The only line-numbered cites into these five live in frozen round-23 wave reports and all point at body lines (2, 20, 22, 23, 25), i.e. below line 4. The edit I name below keeps each file's byte count and line count **identical**, so even the frozen report anchors stay valid.

---

## F1 — No live `path:line` / `file:line` anchor targets F01–F05 (confidence: high)

Command (per entry, from lane root):

```
grep -rn "$f" SKILL.md corpus/ plans/ PROVINCE.md README.md SCORECARD.md LOG.md AGENTS.md SHONEN.md
grep -rnE '(cvss-v4-severity-and-vector|coordinated-disclosure-timelines|authorization-safe-harbor-and-scope|ai-assisted-finding-validation|cwe-top25-2025-methodology)\.md[:#]?[[:space:]]*(line[[:space:]]*)?[0-9L]' --exclude-dir=.git .      # exit 0: 9 matches in 6 files, all under .ufo/
```

Exact live-hit counts (`corpus/knowledge/<self>.md` excluded):

| entry | SKILL.md | corpus/ files | corpus/ lines | plans/ lines |
|---|---|---|---|---|
| cvss-v4-severity-and-vector | 1 | lessons/round-22.md, lessons/round-23.md, README.md, SOURCES.md | 6 | 0 |
| coordinated-disclosure-timelines | 1 | lessons/round-22.md, README.md, SOURCES.md | 6 | 0 |
| authorization-safe-harbor-and-scope | 1 | lessons/round-22.md, README.md, SOURCES.md | 6 | 0 |
| ai-assisted-finding-validation | 1 | lessons/round-22.md, README.md, SOURCES.md | 7 | 0 |
| cwe-top25-2025-methodology | 1 | lessons/round-22.md, README.md, SOURCES.md | 6 | 0 |

Every one of those live hits is a **whole-file** reference, with no `:NN` suffix:

- `SKILL.md:1019-1023` — the five Frontier decision-table rows, path in backticks, e.g. `` `corpus/knowledge/cvss-v4-severity-and-vector.md` ``.
- `corpus/README.md:37-41` (knowledge index) and `corpus/README.md:198-202` (F01–F05 table, `| F01 | … | knowledge/cvss-v4-severity-and-vector.md | S001, S002 |`).
- `corpus/SOURCES.md:7-21` — `used-by` column, S001–S015 each naming its entry path.
- `corpus/lessons/round-22.md:126-128`, `corpus/lessons/round-23.md:16` — prose.
- `plans/` has zero hits (`grep -rn … plans/` exit 1; `plans/` holds only `wwkd-round-20-recensus.md`, `wwkd-round-21-authority-audit.md`).

So: `fork_anchor_count = 0` for a `path:N` edit hazard in every live file.

## F2 — Line-numbered cites into these five exist only in frozen round-23 wave reports, and all target lines > 4 (confidence: high)

`grep -rnE '<stem>\.md:[0-9]' --exclude-dir=.git .` → 9 matches, 6 files, all under `.ufo/waves/round-23/`:

| anchor | file:line of the citing text | resolves to entry line |
|---|---|---|
| `corpus/knowledge/ai-assisted-finding-validation.md:22` | `.ufo/waves/round-23/build/AiRecheck.md:38` | 22 (body quote) |
| `corpus/knowledge/ai-assisted-finding-validation.md:23` | `.ufo/waves/round-23/build/AiRecheck.md:39` | 23 (body quote) |
| `corpus/knowledge/coordinated-disclosure-timelines.md:22-23` | `.ufo/waves/round-23/build/CvdRecheck.md:13` | 22–23 |
| `corpus/knowledge/cvss-v4-severity-and-vector.md:25` | `.ufo/waves/round-23/build/CvssRecheck.md:230` | 25 |
| `corpus/knowledge/authorization-safe-harbor-and-scope.md:20` | `.ufo/waves/round-23/falsify/LessonGateRows.md:143` | 20 |
| `authorization-safe-harbor-and-scope.md:2,20` | `.ufo/waves/round-23/build/ImmutableSources.md:24` | 2 (the `source:` line) and 20 |

Lowest line number cited anywhere is **2** (the `source:` line), which the edit does not touch; next is 20. Nothing cites `:1`, `:3` or `:4`. `:4` is the line I change, and after the edit it still exists and still begins `recheck: ` — so even a reviewer re-reading `.ufo/waves/round-23/build/RecheckSources.md:46` ("Each has `source:`, `verified-at:`, and `recheck:` headers") finds the header where it was.

## F3 — The `recheck:` line is a single physical line, at line 4, in all five (confidence: high)

Command and result (`sed -n '1,8p' <file> | cat -A | sed -n '4p'` — every line ends `$` immediately after the command, no trailing `\`, no continuation, no embedded newline):

| entry | `^recheck:` count | recheck at line | lines on that line containing `source-snapshots/round-23/manifest.json` | occurrences of that path on line 4 |
|---|---|---|---|---|
| corpus/knowledge/cvss-v4-severity-and-vector.md | 1 | 4 | 1 (line 4 only) | 2 |
| corpus/knowledge/coordinated-disclosure-timelines.md | 1 | 4 | 1 | 3 |
| corpus/knowledge/authorization-safe-harbor-and-scope.md | 1 | 4 | 1 | 3 |
| corpus/knowledge/ai-assisted-finding-validation.md | 1 | 4 | 1 | 4 |
| corpus/knowledge/cwe-top25-2025-methodology.md | 1 | 4 | 1 | 3 |

(`grep -c '^recheck:'` = 1 each; `grep -c 'source-snapshots/round-23/manifest.json'` = 1 each, and `grep -n 'source-snapshots/'` returns exactly line 4 for all five. Total path occurrences to rewrite: 2+3+3+4+3 = 15.)

Header shape confirmed identically in all five: line 1 `# <Title>`, line 2 `source: S00x — <url> — “<quote>”`, line 3 `verified-at: 2026-10-19`, line 4 `recheck: python3 corpus/instruments/source-recheck.py --manifest … --source S001 && …`, line 5 blank, line 6 `## Rule`.

## F4 — The exact edit that preserves every anchor (confidence: high; proven on scratch copies, not on the lane)

Replace the substring `source-snapshots/round-23/manifest.json` with `source-snapshots/round-24/manifest.json` **on line 4 only, all occurrences on that line**, in each of the five files. `round-23` and `round-24` are the same length, so the replacement is byte-count-preserving as well as line-preserving.

Exact command (run inside a writer clone, e.g. `/tmp/kasegi-r24-<seat>`; I ran it only on throwaway copies at `/tmp/scoutanchor-verify/`):

```
for f in cvss-v4-severity-and-vector coordinated-disclosure-timelines \
         authorization-safe-harbor-and-scope ai-assisted-finding-validation \
         cwe-top25-2025-methodology; do
  sed -i '4s#source-snapshots/round-23/manifest\.json#source-snapshots/round-24/manifest.json#g' \
    corpus/knowledge/$f.md
done
```

Proof of anchor preservation — the command above applied to copies under `/tmp/scoutanchor-verify/`, then compared to the lane bytes:

| entry | bytes before → after | lines before → after | diff `^[<>]` lines | changed lines |
|---|---|---|---|---|
| cvss-v4-severity-and-vector | 4504 → 4504 | 48 → 48 | 2 (one `4c4` pair) | 4 only |
| coordinated-disclosure-timelines | 4371 → 4371 | 44 → 44 | 2 | 4 only |
| authorization-safe-harbor-and-scope | 4393 → 4393 | 46 → 46 | 2 | 4 only |
| ai-assisted-finding-validation | 4814 → 4814 | 46 → 46 | 2 | 4 only |
| cwe-top25-2025-methodology | 4633 → 4633 | 47 → 47 | 2 | 4 only |

Post-edit line 4 (cvss entry, verbatim from the scratch copy):

```
recheck: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json --source S001 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-24/manifest.json --source S002
```

Because line count and byte count are both unchanged, **all four anchor classes survive**: whole-file refs (F1), `:2`/`:20`/`:22`/`:23`/`:25` line cites (F2), the `grep -m1 '^recheck: '` + `sed 's/^recheck: //'` + `bash -c` counter-A shape (still one line, still starts `recheck: `, still parses under `bash -c`), and the `verified-at:`/`source:` header lines.

Before/after sha256 pins (before = lane `master` bytes; after = the scratch copy produced by the command above, so L1 can diff its own result against a known value):

| entry | before | after |
|---|---|---|
| cvss-v4-severity-and-vector.md | `99d48251039416c2d12bffd5fea0f4f33a2b63fc3c11662c5e18462fff5a8153` | `797867e1009b89bce70f1b7dc7fc0eb9ee8c2bcbacee38564313815b3bb26524` |
| coordinated-disclosure-timelines.md | `dce37a3e4054e270660071f3fb5e8b18d1d5e4ba3b2d8257332fc5e3c6e51970` | `4a9801859d0bf2972b726fa135abdea8ca087255e0d6bbc4c56803df3e91d052` |
| authorization-safe-harbor-and-scope.md | `ddfa93a92a41a32e3a38dbc04bb677fc1ac829513cd1bdbde3347b901c8f276b` | `d8185c7843fa9a2b5bae4f161dfbd162e9b46d4ccfabb3905049cb27d6afb658` |
| ai-assisted-finding-validation.md | `153fe901e88bde2b910d290875b6e880c95d6e51a2f7424559202d3265d3334f` | `335acb6ca4816b1bb16e7109f52d90e3afa15445a5d5d5b242eb8f94a595f4f0` |
| cwe-top25-2025-methodology.md | `1e0569c79525b789aebc567dd4c7603c64dbfd664019ae4e16965b67d6cb28a6` | `3665ba8a36c011069bfe47b9106ea7162d486c525fb8163c7d7c133c85fe76cb` |

## F5 — Precondition the edit depends on: the round-24 manifest does not exist yet (confidence: high)

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-24/` holds `S001.txt` … `S015.txt` (15 captures, 04:15 today) but **no `manifest.json`** (`ls -la corpus/source-snapshots/round-24/`; `git ls-files corpus/source-snapshots/` lists only `round-23/*`, and `git status --porcelain corpus/source-snapshots/` = `?? corpus/source-snapshots/round-24/`).
- Therefore the re-pointed line exits **2 / `manifest UNAVAILABLE reason=missing`** until the manifest is minted and committed. That is fail-closed behaviour, correct per Q1, but it means the edit alone does not move counter A.
- The manifest must carry `"schema_version": 1` as a JSON **int** plus a non-empty `sources` list with unique valid ids — `corpus/instruments/source-recheck.py:56-70` rejects anything else (`unsupported-schema`, `missing-sources`, `invalid-source-id`, `duplicate-source-id`), and `corpus/source-snapshots/round-23/manifest.json` is the exemplar (`{"schema_version": 1, "purpose": …, "sources": […]}`). Source file paths in each record resolve relative to the manifest's own directory (`source-recheck.py:105`, `base = manifest_path.parent`).
- The planned target path is already the one written into the wave-1 prompts: `.ufo/waves/round-24/wave1-spec.json` (and `wave1-dispatch.json`) contain exactly one `corpus/source-snapshots/round-24/manifest.json` mention — "Design the round-24 capture set that makes counter A pass: a `corpus/source-snapshots/round-24/manifest.json` covering S001-S015".

## F6 — Do not re-point F06–F08 (confidence: high)

`corpus/knowledge/multiparty-vulnerability-coordination.md:4`, `cna-assignment-and-vulnerability-rules.md:5`, `cra-manufacturer-reporting-duties.md:4` already point at `corpus/source-snapshots/round-23/manifest.json` and prefix `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&`. The round-23 manifest's `sources` ids are `['S018', 'S029', 'S030', 'S031']` — it holds none of S001–S015. Round-24 is scoped to S001–S015 only, so re-pointing F06–F08 would drive those three (currently exit 0) to exit 2. Leave them.

## F7 — Adjacent path pin outside the five (confidence: high; not an anchor)

`corpus/instruments/README.md:144` documents "`source-recheck.py` + `corpus/source-snapshots/round-23/manifest.json` — checks …". It is a doc sentence, not a `path:N` anchor, and C1's predicate does not require it; but it becomes one round stale the moment round-24 becomes the F01–F05 base. L1 decides; I do not edit.

## F8 — Q1 wording gap the minimal edit does not close (confidence: high on the text, medium on whether it is enforced)

`corpus/QUALITY.md:14` (Q1) requires `recheck:` to carry "**date or cadence plus** the runnable command or URL anchor". All five current lines are command-only; the edit in F4 keeps that shape (it only changes the manifest path). This is a pre-existing condition, not a regression the re-point introduces, and `corpus/QUALITY.md:24-28`'s "appended block, never inserted at the top, so every existing line anchor … stays valid" text shows the lane's own preference for append/same-line over reflow. If L1 wants Q1 conformance in the same pass, prefixing line 4 with a cadence token (e.g. `on-release — `) is also anchor-safe, because line-based anchors are insensitive to length; the F4 form is the strictly safer one because it also preserves byte offsets (and therefore the F2 `:NN` cites under any byte-offset reader).

## Remaining unknowns

1. UNVERIFIED whether anything outside this repo (fleet `templates/`, `scripts/`, sibling lanes, `MANIFEST.json`) greps these five paths with a line number. Out of my read scope by contract; `grep -rn` inside the lane is the whole evidence surface I claim.
2. UNVERIFIED that the round-24 manifest will contain quote assertions for all of S001–S015 and reach exit 0 — the captures exist, the manifest does not. Counter A's exit-0 target is a build outcome, not an anchor question.
3. No `path:line` anchor convention is enforced over `.ufo/` by any instrument I could find (`grep -rn 'anchorcheck.py corpus'` outside `corpus/knowledge/` returns nothing), so the F2 citations are prose pins a human reads, not gate-checked anchors.

## Tool installs

None. No package installed, upgraded, or removed this seat; no network fetch performed (all evidence is local committed bytes plus scratch copies under `/tmp/scoutanchor-verify/`).
