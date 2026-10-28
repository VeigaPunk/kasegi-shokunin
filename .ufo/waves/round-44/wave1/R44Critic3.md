# R44Critic3 — falsify the C1 remedy for the lesson hash-prefix numeral (frozen defect 3)

Item: *Try to falsify C1 remedy for lesson hash-prefix count and quantify exact characters.*
Read-only seat. Lane HEAD `66314015122b9aa32dc40f2f1815df56624c26d1`; frozen base
`5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`. All lane evidence below is read from those
commits (the working tree is dirty with sibling drafts, so it is never used as evidence).

**Verdict.** The *count* is confirmed and exact: the served token is **26** characters, not 29.
The *remedy as currently drafted* is **falsified**: the round-44 counter reports defect 3
`resolved=1` while the file the defect names is byte-identical to the frozen base, and reports
`resolved=0` when that file is genuinely corrected. It also prints `fixed=8 unresolved=0 exit=0`
on a tree with **zero commits** and the frozen target untouched.

## 1. The frozen defect and the exact characters

Frozen routing: `corpus/lessons/round-43-verifier-spotcheck.md:103` (§6 item 3) — the lesson's
`29-character prefix` at `corpus/lessons/round-43.md:90` and `:101` is 26 characters.
Lesson blob is unchanged base→HEAD: `git rev-parse 5ab3a60:corpus/lessons/round-43.md
HEAD:corpus/lessons/round-43.md` → `72b91f6962293d68245cb14bfdc0523562e56403` (both);
`grep -c '29-character'` → **2** at both.

| object | command | observed |
|---|---|---|
| served token, chars | `printf '%s' c6ae07c6a541e0e96d0040afb6 \| wc -c` | **26** |
| served token, with newline | `echo c6ae07c6a541e0e96d0040afb6 \| wc -c` | 27 |
| full hash | `printf '%s' c6ae07c6a541e0e96d0040afb62b45dd37711300 \| wc -c` | **40** (echo → 41) |
| full hash begins with the token | `python3 -c "print('c6ae07c6a541e0e96d0040afb62b45dd37711300'.startswith('c6ae07c6a541e0e96d0040afb6'))"` | `True` |
| committed capture line | `sed -n '97p' corpus/source-snapshots/round-43/S067.txt \| cat -A` | `Fixed-in: https://github.com/curl/curl/commit/c6ae07c6a541e0e96d0040afb6$` |
| capture token, chars/bytes | `printf '%s' "$T" \| wc -m` / `wc -c` | 26 / 26 (ASCII) |
| capture binding | `sha256sum corpus/source-snapshots/round-43/S067.txt` | `7e35413a…` = manifest `sha256`; manifest `raw_sha256 58ca9900…` |
| live page equals the capture's raw | `curl -sS https://curl.se/docs/CVE-2025-9086.html \| sha256sum` | `58ca99006c3299456ae7a40a0fb268cef6213f1ce5d07eb2c98f1dcc56716ebd`, 10455 B |
| live page token | `grep -oE 'c6ae07c6[0-9a-f]*' page.html \| sort -u` | exactly one, len **26**, in **both** the `href` and the anchor text |
| JSON sibling (not captured by the lane) | `curl -sS https://curl.se/docs/CVE-2025-9086.json` | 200, 2468 B; one token, len 40 |

So the numeral 29 measures **no object on that line**: `https://github.com/curl/curl/` is
`printf '%s' | wc -c` → **29**, i.e. 29 is the length of the *URL prefix* on the same sentence,
not of the hash. (Measured fact; that this is the origin of the slip is inference.) A correction
that only swaps the number without naming the object can be re-broken the same way.

The lesson's other numeral claims are **correct** and must not be swept: `grep -oE '[0-9]+-character'`
over the lesson → `2 × 29-character`, `2 × 40-character` (L64 "full 40-character fix hash", L101
"the full 40-character hash"). A predicate over all `N-character` tokens flags the two true 40s.

## 2. Counterexample against the drafted counter

Counter bytes tested: `corpus/instruments/r44-routed-defects.py`, **untracked draft** (`git status`
→ `??`), sha256 `8a5a9c2bd6ac04b08c93e31c7dd9c228b4bd737c240e17f58191b7f303691ee6` (an earlier copy,
`3e04ec7d…`, differs only outside RD43-3). Its defect-3 row is:

```python
lesson = text(root, "corpus/lessons/round-44.md")
("RD43-3 29-versus-26 hash prefix",
 "29-character prefix" in lesson and "26-character" in lesson and "wc -c" in lesson and "26" in lesson),
```

Three defects, each reproduced:

**(a) False green — wrong file, presence-only predicate.** Root = frozen-base export + a
*fabricated, untracked* `corpus/lessons/round-44.md` that merely *mentions* both numerals; the
defect's own file is untouched:

```
sha256sum fake/corpus/lessons/round-43.md   -> ba118cea2c98128fe7cd78144fe5d43ac3e91a85829d8c533f16f31ecd163e48  (= frozen base)
grep -c '29-character' fake/corpus/lessons/round-43.md -> 2
python3 counter-live.py --root fake --baseline base-export
  RD43-3 29-versus-26 hash prefix resolved=1
  frozen_defects=8 fixed=1 unresolved=7 exit=1
```

**(b) False red — the remedy §6 item 3 actually prescribes.** Root = frozen-base export with a
one-line `Correction (round 44)` appended to `corpus/lessons/round-43.md` (naming L90/L101, the
26-char token, the 40-char sibling hash, and a counting command that prints 26), no `round-44.md`:

```
refclaim.py fake2/corpus/lessons/round-43.md
  refs=[90, 101] live=0 superseded=3 closed=1 live_at=[] sup_at=[90, 101, 167]
python3 counter-live.py --root fake2 --baseline base-export
  RD43-3 29-versus-26 hash prefix resolved=0
  frozen_defects=8 fixed=0 unresolved=8 exit=1
```

**(c) Eight-of-eight on zero commits.** Root = frozen-base export plus untracked files satisfying
each predicate (no `.git`, nothing committed, `corpus/lessons/round-43.md` still `ba118cea…` with
2 live 29s):

```
python3 counter-live.py --root green2 --baseline base-export
  RD43-1..RD43-8 resolved=1
  frozen_defects=8 fixed=8 unresolved=0 exit=0
```

**(d) `--baseline` never grades.** It is used only for `re.findall(r"(?m)^\s*[1-8]\. \*\*", frozen)`
→ `frozen_defects=8`. Swapping the baseline for the same root leaves every verdict identical
(`--root fake --baseline fake` and `--baseline base-export` both print `RD43-3 resolved=1`). So the
counter emits **no per-defect red-before control**, which C1's `after` requires per changed gate.

**(e) Dirty tree is accepted as "committed evidence".** Run against the live lane root it prints
`fixed=5 unresolved=3`, and the five passing inputs are all untracked/modified:
`git ls-files --error-unmatch` → UNTRACKED for `.ufo/waves/round-43/claims-erratum-6.md`,
`controls/round43-registry-correction{,-note}.txt`, `controls/r42-at-de09313-selftest-replay.txt`,
`controls/missing-suite-base.txt`; `git status --porcelain` → ` M SCORECARD.md`, ` M SHONEN.md`,
` M SKILL.md`; committed `SHONEN.md` still ends `.\n` (`git show HEAD:SHONEN.md | tail -c 20 | xxd`),
so RD43-6 passes only on the uncommitted edit.

## 3. Why no literal predicate can work (structural, not stylistic)

1. **Literal absence is unreachable.** The two live occurrences are in an append-only file; no
   correction may delete them. Measured: `grep -c '29-character'` → base 2, correction that names
   the literal 3, correction that hedges ("twenty-nine") still **2**. A `== 0` predicate can never
   close, and the hedge does not help.
2. **Lane-wide literal scope is also unreachable.** `git grep -c '29-character\|29-char prefix' HEAD`
   outside the routing record: `corpus/lessons/round-43.md:2`,
   `.ufo/waves/round-43/w1/ScribeLessonDraft.round-43-lesson.md:2`,
   `…/ExecSourceCapture.provenance.txt:1`, `…/ExecSourceCapture.md:1`,
   `…/ExecRegistryRows.md:1`, `.ufo/waves/round-43/kasegi-r43-hyaku-results.json:1`. Seven committed
   occurrences that no append-only lesson correction reaches. The predicate must be scoped to the
   file the frozen defect names.
3. **Line-scoped supersede is fragile.** K18's rule is per-line ("a line containing
   `Correction (round 43`"). A correction wrapped like the lesson prose puts the literal on a
   continuation line: `k18-line-scope: live=3 at=[90, 101, 168] closed=0`, versus
   `block-scope: live=2 at=[90, 101]`. And "contains the marker" over-credits: the round-43 lesson
   already carries five table rows that *name* `Correction (round 42)` (`:37-41`), so a
   contains-style rule would mark live claims superseded by a mention.
4. **The only reachable predicate is supersede-by-reference**, and it does close: with
   `refs = {L<n>, :<n>} named inside the `Correction (round 44)` block`, a pre-correction occurrence
   is superseded iff its line is named:
   `base → refs=[] live=2 superseded=0 closed=0 live_at=[90, 101]`;
   `corrected → refs=[90, 101] live=0 superseded=3 closed=1` (the 3rd is the correction's own
   mention — report it separately as `correction-mentions=1`).
5. **The mandated counting command is wrong.** The draft requires `"wc -c" in lesson`, but on the
   capture `grep -oE 'c6ae07c6[0-9a-f]+' S067.txt | wc -c` → **27**; `… | awk '{print length}'` → 26;
   `… | tr -d '\n' | wc -c` → 26; `… | wc -l` → 1. The counter rewards the one command whose output
   contradicts the numeral it certifies. A numeral-only predicate cannot grade §6 item 3's actual
   requirement ("a numeric claim needs its counting command"); the counter must execute the cited
   command and compare.

## 4. Smallest safe correction

1. **Grade the named file:** `lesson = text(root, "corpus/lessons/round-43.md")` — not `round-44.md`.
   (The same wrong-file defect now affects RD43-4 and RD43-7 in the live draft, which read the
   round-44 lesson for report obligations; out of my item's scope but the same edit class.)
2. **Predicate:** count `(\d+)-character prefix` claims; classify each occurrence `live` unless a
   `^Correction \(round 44\)` block names its line (`L<n>` or `:<n>`) or the occurrence is inside
   that block; `closed = live == 0`. Emit `live=,superseded=,correction-mentions=`.
   Expected: base `live=2,superseded=0,closed=0`; final `live=0,superseded=2,closed=1`.
3. **Make `--baseline` grade:** run the same predicate against the baseline export and emit
   `RD43-3 baseline live=2 closed=0` — that is the red-before control C1's `after` demands.
4. **Refuse a dirty root:** require an export (e.g. `git archive <ref>` / `--export-ref`), since C1
   says "committed lane evidence"; a working-tree `--root .` currently yields `fixed=5` with zero commits.
5. **Grade the command, not the numeral:** extract the command cited in the correction, execute it
   against `corpus/source-snapshots/round-43/S067.txt`, require its stdout to be exactly `26`, and
   reject `wc -c` (prints 27).
6. **Correction text (one physical line, matching `corpus/lessons/round-38.md:311`):** name L90 and
   L101, the served 26-char token, the 40-char sibling hash (not on the page), and
   `grep -oE 'c6ae07c6[0-9a-f]+' corpus/source-snapshots/round-43/S067.txt | awk '{print length}'` → 26.

Expected kills for a mutant on this limb: r43 corrected but no r44 lesson → must be `1` (kills the
draft); r44 mentions both numerals with r43 untouched → must be `0` (kills the draft); correction
naming L90 only → `live=1` → `0`; correction citing `wc -c` → command check `27 ≠ 26` → `0`;
correction appended to an uncommitted tree → export root refuses → `0`.

## 5. Do-nothing discrimination

At the frozen base the defect is open and measurable from committed bytes alone: lesson blob
`72b91f69…` at base **and** HEAD, `29-character` count 2, no `Correction (round 4x)` line at column 0
(`grep -c '^Correction (round' → 0`), and no `corpus/instruments/r44-routed-defects.py` in `git
ls-files`. The reference-aware predicate over the committed lesson prints
`live=2 superseded=0 closed=0` — a red-before value that do-nothing reproduces. What do-nothing
cannot reproduce is `live=0`, which needs an appended correction naming L90/L101.

## 6. Impacted axes

- `depth:verifiability` (C1): the defect-3 limb of the proof instrument is unsound in both
  directions and supplies no baseline red; as drafted, C1's `after` ("proven by one committed
  read-only counter over committed lane evidence") is not provable. This is a remedy defect, not a
  score move — I make no score claim.
- `coverage` (C2): unaffected by this item; no evidence either way is offered here.

## 7. Limitations

- Live fetches (advisory page, JSON sibling) are corroboration, not lane evidence; the pinned
  evidence is the committed capture, whose `raw_sha256` equals the live page byte-for-byte
  (`58ca9900…`), so the 26 is re-derivable offline.
- The 40-char hash is not captured in the lane; "full hash = 40" rests on the JSON sibling and the
  frozen routing record, not on a lane capture.
- `29` = `https://github.com/curl/curl/` is a measurement; the causal story is inference.
- The counter is an untracked, actively edited draft (`??`, sha256 `8a5a9c2b…` at
  `2026-10-28T19:16Z`); its RD43-3 row was byte-identical in the earlier `3e04ec7d…` copy, and all
  counter outputs above are from `8a5a9c2b…`. If it changes, re-run §2.
- I did not run the round-43 suite (integrator's gate) and made no production edits.

## 8. Scratch and tooling

Scratch `/home/vgpnk/.hyaku/scratch/kasegi-r44/R44Critic3/` (created, used, removed on exit; the
`HYAKU_SCRATCH` env var was unset in this shell, so the documented default
`/home/vgpnk/.hyaku/scratch` was used). No `/tmp` writes. Tools installed: **none**
(`/home/vgpnk/.omp/agent/RULES.md` read; pacman not invoked — paused host-wide). Only `git`,
`grep`, `sed`, `awk`, `printf`, `sha256sum`, `curl`, `python3` (stdlib) were used.
