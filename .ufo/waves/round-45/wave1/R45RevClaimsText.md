VERDICT: BROKEN

# R45RevClaimsText — claim-text review of round-45 claims.json

Scope: frozen `.ufo/waves/round-45/claims.json` (sha256 `bbe40503…6206`, matches `freeze.txt:2`) against `AXES.md`, `.ufo/prompts/kasegi-round-45.md:529-551` (§6 item 9 "Claim sizing"), counters `corpus/instruments/r45-routed-defects.py` (C1) and `corpus/instruments/r45-c2-gate.py` (C2), and `.ufo/waves/round-45/controls/freeze-controls.txt`. Read-only. No git mutation, no lane file edited other than this report. Scratch (`/fast/scratch/hyaku/kasegi-r45/R45RevClaimsText`) removed on exit. No installs.

Note on sources: §9 is **not** in `templates/round-prompt.md` (sections 1–5, 2b, 3 only). The rule lives in the round-45 prompt at `.ufo/prompts/kasegi-round-45.md:529`. `$S` below is the scratch root.

## Ranked findings

### F1 — BROKEN: C2 "curly quotes are each located" is not enforced; counter grades an uncited fabricated quote 7/7
- Attacked: `claims.json` C2.after ("whose curly quotes are each located in snapshot lines"); `r45-c2-gate.py` G5 docstring lines 20-25 and code line 175 `re.findall(r"“([^”]+)”\s*\(`?S071\.txt:(\d+)(?:-(\d+))?`?", body)`.
- Fixture `$S/fx-g5`: copy of base + lane's committed `corpus/source-snapshots/round-45/`; F27 row in `corpus/README.md`; `corpus/knowledge/kernel-security-bugs.md` with five cited genuine spans, one **uncited** fabricated `“every reporter receives a 30-day embargo regardless of severity.”`, one cited single-curly fabricated `‘kernel embargo is 90 days’ (`S071.txt:310`)`; S071 row inside the Registry section, recheck `on-release`.
- Command: `python3 corpus/instruments/r45-c2-gate.py --root $S/fx-g5`
- Output (verbatim):
```
gate G1 pass=1 read=rows=27 admitted=27 entry=corpus/knowledge/kernel-security-bugs.md
gate G2 pass=1 read=source=1 verified-at=1 recheck=1
gate G3 pass=1 read=row-S071=ok
gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0
gate G5 pass=1 read=spans=5 located=5 failed=0 cores=4/4
gate G6 pass=1 read=knowledge=64
gate G7 pass=1 read=census-rc=0
c2-gate fixed=7/7 exit=0
```
- The entry contains six double-curly spans and one single-curly span; G5 read five. The fabricated phrases are absent from the snapshot: `grep -c -E '30-day embargo|90 days|every reporter receives' corpus/source-snapshots/round-45/S071.txt` → `0`.
- Consequence: "each" is a universal the counter does not enumerate (§9 item 2). The frozen fabricated-quote control (5/7) only exercises *cited* fabrication, so the do-nothing reachability bar (§9 item 6, `kasegi-round-45.md:538-542`) is not met for this form.
- Fix before any seat scores: G5 must enumerate every curly span (both `“”` and `‘’`) and require a citation for each, or the claim text must say "every cited span".

### F2 — BROKEN: C2 before "held nowhere in corpus/" is not re-derivable with its stated command
- Stated check: `grep -rliE 'security-bugs|linux kernel|kernel\.org' corpus/knowledge corpus/SOURCES.md corpus/README.md` prints nothing → confirmed, `rc=1` at base.
- The claim universal is "nowhere in corpus/". Same pattern, recursive over `$S/base/corpus`:
```
…/corpus/source-snapshots/round-30/S046.txt
…/corpus/source-snapshots/round-30/S047.txt
…/corpus/source-snapshots/round-35/S052.txt      (rc=0)
```
  These are `git.kernel.org` stable-commit links inside CVE notes (S052.txt:660), not the process.
- With the process-specific token, `grep -rlE 'docs\.kernel\.org|security-bugs' $S/base/corpus` → `rc=1`. The sentence is true for the process, but the claim's enumerated check is a three-path grep. Fix: name the token and the path set (corpus/ recursive, `docs.kernel.org|security-bugs`).

### F3 — BROKEN: C1 kill rule "any control … grades fixed=5" literally matches a C2 control line
- `claims.json` C1.kill_rule: "…if any control in controls/freeze-controls.txt (do-nothing base, marker-only tree) grades fixed=5".
- `grep -n 'fixed=5' .ufo/waves/round-45/controls/freeze-controls.txt` →
  `5:control c2-fabricated-quote counter=C2 c2-gate fixed=5/7 exit=1 expect=RED got=RED`
- As worded, a C2 control line can fire the C1 kill. Fix: "any C1 control (counter=C1) grades fixed=5".

### F4 — BROKEN: one predicate is not one sentence across plan, counter, and receipt (R44 freeze rule)
- Plan: `claims.json` top-level keys are `['author','base','claims','frontier_step','lane','round','schema','sourced_claim']`; claim keys (both claims) contain no `predicate`. `grep -n -i predicate claims.json` returns only line 13: the kill rule's "counter's predicate sentence (five limbs R1-R5)". That sentence is not in claims.json.
- Counter: the only predicate text is the docstring block "WHAT IT MEASURES" (`r45-routed-defects.py:4-35`; `r45-c2-gate.py:4-29`). Wording differs from claims (see F5-F8).
- Receipt: summary lines only (`control do-nothing-base counter=C1 routed-defects total=5 …`); no predicate label.
- Freeze: `freeze.txt` pins the claims digest only; it pins neither counter file. Its five lines: frozen-at, claims-sha256, base, controls measured-at, and a note. "Counter changed after a seat scored" is therefore detectable only by manual diff. Current state: `git -C kasegi-shokunin diff --stat 8cf62c8 -- corpus/instruments/r45-*.py .ufo/waves/round-45/claims.json .ufo/waves/round-45/controls/freeze-controls.txt` → empty (unchanged at review time).
- Fix: one predicate sentence per claim in claims.json, echoed verbatim in the counter docstring and the receipt header; add counter sha256 to freeze.txt.

### F5 — BROKEN: C2 frozen-core count and names differ across claims and counter
- claims C2.after: "cites the four frozen cores (7-day embargo ceiling with 14-day exception; AI-found bugs treated as public; binary-only reproducers refused; unreproducible is not exploitable)".
- `r45-c2-gate.py` CORES (lines 48-53): four regexes; core 1 is `up to 7 calendar days` (no 14-day); core 3 is `Binary-only executables are not accepted` (claims say "binary-only reproducers refused").
- MANIFEST_CORES (lines 54-60): five strings, including `with no version indication, your report will not be processed`, which is not one of the four.
- G4 docstring (line 19) says "the five frozen quote cores"; G5 docstring (lines 23-24) says "the four frozen cores". Same file, two counts.
- Fix: one list of four, claim text quoting the counter's wording.

### F6 — mismatch, unrecorded narrowing: C1 R1 routed fix differs from lesson §6 item 1
- Lesson `corpus/lessons/round-44-verifier-spotcheck.md:79`: "Append (never rewrite) a correction to `corpus/SOURCES.md` S070 and `round-44.md` `## Gate` … Replace the vacuous flip condition with a checkable one".
- Counter `limb_r1` (`r45-routed-defects.py:116-119`) requires the S070 row byte-identical to base (`old != new` → fail): no S070 correction is tested. Lines 110-111 test `re.search(r"flip:\s*\S", teaches)`: presence only, not "checkable".
- claims C1.after ("R1 S070 reject reason superseded by a sha-pinned row S072 plus an appended round-44 lesson correction") matches the counter, not the lesson. The narrowing is recorded nowhere.

### F7 — mismatch: C1 R2 "grounded in corpus/lessons/round-44.md" is presence-only
- `limb_r2` (`r45-routed-defects.py:166-177`): ground cell must contain the substring `corpus/lessons/round-44.md`; the `enforced-by:` path must exist.
- Fixture `$S/fx-r2`: QUALITY.md rows R47/R48/R49 with `enforced-by: corpus/instruments/README.md` (existing, unrelated file). Command: `python3 corpus/instruments/r45-routed-defects.py --root $S/fx-r2 --baseline $S/base`. Output: `limb R2 fixed=1 read=criteria=3`.
- The lesson's own criterion R48 ("presence-only predicates accept denials") is violated by R2. The frozen controls do not exercise this path: marker-only uses `corpus/instruments/nothing.py`, which does not exist.

### F8 — mismatch: C1 R3 "selftest and registry rows" (claims) vs "probe or selftest-and-row" (lesson)
- Lesson item 3 (line 81): "register it as a probe or give it a selftest and a registry row". Claims and counter (`r45-routed-defects.py:200-206`) require selftest AND three SKILL rows AND a README row. The stricter choice is not recorded.
- Base reality: `python3 corpus/instruments/r44-frontier-count.py --root $S/base --selftest` → `r44-frontier-count.py: error: unrecognized arguments: --selftest`, `exit=2`. R3 is red.
- Withdrawn: the counter's `## Round-45 … Gates & probes registry addition` heading matches the existing convention (SKILL.md:1037, 1050, 1060). Not a mismatch.

### F9 — mismatch: C1 R4 "replay clean at the base" vs exact counter token
- claims C1.after: "round-45 claims replay clean at the base". Counter line 220: `^freeze-check claims=2 base_ok=2\b`, with flags `--claims --tool-root --base` that the docstring omits.
- `corpus/instruments/freeze-check.py` does not exist in the lane (`No such file or directory`). R4 cannot be measured yet.

### F10 — mismatch: C1 R5 after-state omits conditions the counter tests; "as read by the committed counter" is untrue for R5
- claims C1.after: "R5 a refiled selftest receipt without the failed bare call". Counter `limb_r5` (lines 225-242) also requires `selftest cases=20 failures=0`, `exit=0`, the invocation pattern `--root … --selftest --work …`, and `final-attempt3.txt` byte-identical to base (`original-receipt-changed`).
- `git status --porcelain`: `?? .ufo/waves/round-44/controls/final-attempt3-refiled.txt` (untracked). The lane run prints `limb R5 fixed=1 read=refiled=ok original=unchanged` only because the untracked file is in the working tree. The counter reads `--root` (docstring: READ-ONLY over --root). "As read by the committed counter" (C1.after) describes something that does not happen; commit the receipt or change the wording.

### F11 — mismatch: C2 kill-rule conditions are not one command
- C2.kill_rule: "if the non-author closure re-opening S071 does not locate the cited quotes". Neither counter performs network I/O (`grep -nE 'urllib|curl|requests|http|socket'` → only the `URL` constant, `r45-c2-gate.py:47`). The re-open is a manual step.
- Both counters use a host-absolute census default: `CENSUS = os.environ.get("SOURCES_CENSUS", "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh")` (`r45-c2-gate.py:46`; `r45-routed-defects.py:55`). A closure off this host must set `SOURCES_CENSUS`; the claim text says nothing about it.
- G7 runs `validate --file`; the template census command (`templates/round-prompt.md` §2.2) is `validate --root <FLEET> <lane>`. The `--file` form was run on base and fixtures (`census_file_exit=0`); the `--root` form was not run.
- C1.kill_rule "changed after a seat has scored (bug fixes … logged as counter errata)" and C2.kill_rule "not narrowed after landing" are prose. The counter pins `27` (G1, line 112) and `64` (G6, line 194), but nothing pins the counter file (see F4).

### F12 — tension: C2 "one new knowledge entry (64 total)" is a file count; sourceless gates also pass
- G6 is `n == 64`, counting any `.md` file (line 194). Receipt `c2-junk-row … fixed=4/7` already passes G1, G2, G6, G7 with no sourcing. §9's last bullet ("counting rows a sourceless fixture also counts is quality work, never coverage", `kasegi-round-45.md:548-550`) applies: the coverage credit rests on G3–G5 (sourced). The claim text should say so, or G6 should count admitted F27 entries.

### F13 — causal separability: separable on counters, coupled on shared gates and files
- C2 G7 validates all of `corpus/SOURCES.md` (`r45-c2-gate.py:197-199`). C1's S072 row lands in the same file (`r45-routed-defects.py:99-101`); a census-invalid S072 turns C2's "census exit 0" red.
- C1 R1 (`r45-routed-defects.py:120-124`) and C2 G4 (`r45-c2-gate.py:157-161`) both run `source-recheck.py` against `corpus/source-snapshots/round-45/manifest.json`, which lists S071 and S072.
- C2's secondary `r44-frontier-count.py --expect 27` is the file C1 R3 must extend with `--selftest`; that flag is absent today (F8).
- `frontier_step` joins both as "SOURCES rows 70 -> 72". No gate reads the other claim's limb, so the counters are separable; the census gate and the shared file are not. The claim text should say so.

### F14 — mismatch: the frontier step's round-45 mined mistake has no counter
- Round prompt §2b item 3 requires `corpus/lessons/round-45.md ## Mistakes`. `grep -n 'round-45.md\|lessons/round-45' corpus/instruments/r45-routed-defects.py corpus/instruments/r45-c2-gate.py` → no match (`rc=1`). Neither claim's after-state includes it.

### F15 — §9 checks that hold
- Two claims: holds (`kasegi-round-45.md:536`).
- Distinct axes: holds (depth:verifiability, coverage).
- Lowest-axis: holds on the lane's own statement, `SCORECARD.md:331` ("depth:verifiability (C1, lowest axis) | 4"). The other axis rows (operability, freshness, calibration, adjacency) did not surface in my grep, so the "lowest" claim is not independently fully verified.
- Before-states: C1 "0 of 5" and C2 "26 / 63 / 70" all match base (below).

## Do-nothing control and reproduction (re-run by me, serially)
- Regenerated receipt: `python3 .ufo/waves/round-45/controls/freeze-controls.py --base-export $S/base --lane $L --work $S/work2`, then `diff` against the committed `freeze-controls.txt`: **IDENTICAL**.
- C1 on base: `limb R1 fixed=0 read=row-S072=absent`, `limb R2 … quality-not-append-only-or-unchanged`, `limb R3 … selftest-rc=2-tokens=None`, `limb R4 … freeze-check-absent`, `limb R5 … refiled-absent`, `routed-defects total=5 fixed=0 unresolved=5 exit=1`.
- C2 on base: `gate G7 pass=1 read=census-rc=0`; `c2-gate fixed=1/7 exit=1`. Base counts: frontier rows 26, SOURCES rows 70, knowledge 63.
- Lane working tree now: C1 `fixed=1 unresolved=4` (R5 only, via the untracked receipt); C2 `c2-gate fixed=2/7 exit=1` (G4 and G7 pass against the committed snapshot and manifest).
- Secondary: `r44-frontier-count.py --root $S/base --expect 27` → `frontier expected=27 admitted=26 verdict=SHORT exit=1`, matching the claim's "exit 1".

## Recommendation to L1
- Wave-1 seats are running. Any repair to F1, F3, F4 or F5 after a seat scores must be logged as a counter erratum, not a new rule (kill-rule text, `claims.json` line 13). Fix F1 and F3 before data if feasible.
- F4 needs the predicate sentence in claims.json plus counter and receipt digests in `freeze.txt`.

## Limitations
- The G5/7-7 result is a scratch fixture built from the lane's committed snapshot. It shows counter behaviour, not the eventual F27 entry. Wave-1 builder drafts were not read.
- The fleet census `validate --root` form was not run; only `--file`.
- R3 and R4 semantics are not measured (no selftest flag, no `freeze-check.py`).
- The lowest-axis check is partial (see F15).
- Wording judgments are my reading of the quoted text, checked against the counter code at commit `8cf62c8` (no diff since).
- One batch of my parallel bash calls raced the base copy. I re-ran those checks serially; every output cited above is from a serial run.
