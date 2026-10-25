#!/usr/bin/env python3
"""Render .ufo/waves/round-25/wave1-spec.json for the kasegi round-25 build wave.

Run from the lane repo root:
  python3 .ufo/waves/round-25/build-wave1-spec.py
"""
import json
import os

GODSPEED = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
PKG = "/home/vgpnk/Projects/shokuknow/merge/kasegi"

CONTEXT = """# Round
kasegi-shokunin round 25, wave 1 (build), dispatched by the L1 (parent omp session). Fleet root
/home/vgpnk/Projects/shokunin. Lane repo /home/vgpnk/Projects/shokunin/kasegi-shokunin — your only
write scope. Lane base revision b49948f1164ef65106b2c4cbee3f53e8a44b8c41.

Read before your item:
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-25/claims.json (frozen claims C1/C2 + counters)
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/SCORECARD.md (axes, saturation, planned rows)
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md (entry bar Q1-Q9, record bar R1-R12)
- /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-24-verifier-spotcheck.md §6 (routed defects D24-1..D24-5)

# The two frozen claims (do not widen, do not re-word)
C1 depth:verifiability (lowest non-retired axis, score 4). Surface: the `recheck:` line of every
corpus/knowledge/*.md entry (35 lines). Predicate: every line is one shell command that (a) parses under
`bash -n`, (b) gives the same exit status AND the same combined stdout+stderr digest from the lane root and
from a foreign cwd (/), (c) names at least one lane-relative corpus/ path or a ~/Projects/ base test, and
every corpus/ path it names exists. Counter: `python3 corpus/instruments/recheck-audit.py --json <out>`
prints `lines=35 pass=N fail-closed=M exit=0|1`. Frozen before receipt (L1, committed under
.ufo/waves/round-25/c1-before.json): `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 exit=1`.
C2 coverage (score 7). Surface: frontier ground the lane does not hold — vendor-side disclosure policies as
corpus objects (F10). Predicate: frontier admitted rows = 10 AND >=1 corpus/knowledge entry carries a header
`source:` id first registered this round AND the sources census validates exit 0. Before: frontier=9,
entries=0, census exit 0 (35 rows).

# Hard rules (every seat)
- Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/kasegi-shokunin — write it at
  /home/vgpnk/Projects/shokunin/kasegi-shokunin/<that path>. Use absolute paths in every command.
- You are a leaf: spawn nothing, start no background job, run no swarm of your own.
- Write ONLY your owned paths (named in your item). A read-only seat makes NO production edit; its output is
  its report file (and, where the item says so, files under .ufo/waves/round-25/wave1/).
- Never write /home/vgpnk/Projects/shokunin (fleet root), any sibling lane, /home/vgpnk/Projects/shokuknow
  (READ-ONLY: no writes, never run renumber-staged.py / merge-plan.py / quote-lint.py /
  absent-defect-register.py there), /home/vgpnk/Projects/shokunin/.ufo/state,
  /home/vgpnk/Projects/shokunin/.scratch, MANIFEST.json, templates/ or fleet scripts/.
- Never run in the lane repo: git add/commit/push/checkout/switch/stash/reset/pull, any mutating jj command
  (commit/new/describe/squash/rebase/abandon/bookmark/undo/op restore), or any other VCS write. Read-only git
  (log/show/diff/status/ls-files/rev-parse) and `jj --ignore-working-copy` are fine. The L1 commits through
  the lane helper; you never do.
- Tooling: you may install or upgrade tools that help your item — read /home/vgpnk/.omp/agent/RULES.md first,
  official channels only, and record tool/version/channel/reason in your report. ALL pacman transactions are
  PAUSED host-wide: use `uv tool` / `npx` / an official binary in ~/.local/bin only; never `pacman -S`,
  `-Sy`, `-Syu`, `-U`, `-R`.
- Honesty: an unrun check has not passed; never fabricate a verdict, a quote, a count or an exit code. Quote
  failures verbatim. If your item cannot be completed, report the exact blocker.
- Never edit considerthese/ (operator-authored), the round-24 verifier spotcheck, or any round-24 wave receipt.
"""


def item(name, role, target, change, acceptance, owned, read_only=False):
    head = "# Target\n" + target + "\n\n# Change\n" + change + "\n\n# Acceptance\n" + acceptance + "\n"
    owned = owned.replace(R25, LANE + "/" + R25).replace(W1, LANE + "/" + W1)
    scope = "\n# Write scope\n" + ("READ-ONLY: no production edit. " if read_only else "") + owned + "\n"
    return {
        "name": name,
        "role": role,
        "item": name,
        "prompt": "/skill:godspeed\n" + GODSPEED + "\n" + head + scope,
    }


R25 = ".ufo/waves/round-25"
W1 = ".ufo/waves/round-25/wave1"
AUDIT = "python3 corpus/instruments/recheck-audit.py"

items = []

# ---------------------------------------------------------------- write items
items.append(item(
    "FixRecheckLines", "executor",
    "C1. Rewrite the 29 non-conforming `recheck:` lines in corpus/knowledge/*.md so every one of the 35 "
    "lines is a cwd-independent executable command. Frozen before receipt: `lines=35 pass=6 fail-closed=23 "
    "parse_fail=23 cwd_fail=6 exit=1` (./" + R25 + "/c1-before.json). The 23 failing `parse` are the lines "
    "shaped `recheck: on-restoration — <CMD> (<NOTE>)`; the 6 failing `cwd` are "
    "ai-assisted-finding-validation, authorization-safe-harbor-and-scope, citation-bases, "
    "coordinated-disclosure-timelines, cvss-v4-severity-and-vector, cwe-top25-2025-methodology.",
    "1. For each of the 23 `on-restoration — ` lines, replace the single line in place with exactly:\n"
    "   `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && <CMD>  # on-restoration — <NOTE>`\n"
    "   where <CMD> is the command text between `on-restoration — ` and the trailing `(<NOTE>)`, and <NOTE> "
    "is the note verbatim without its wrapping parentheses. Keep the em dash inside the comment.\n"
    "2. For each of the 6 cwd-dependent lines, prefix `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ` "
    "and change nothing else.\n"
    "3. One line stays one line: every file keeps its exact line count and every line number (R6). Do not "
    "touch any other line, do not re-wrap, do not add or drop entries.\n"
    "4. Do not delete any `test -d`/`test ! -e`/`test -e` base test: a line's fail-closed semantics must be "
    "preserved exactly (a line that failed closed before must still fail closed, for the same reason).\n"
    "5. If a command needs `python3 corpus/...`, that relative path is resolved by the cd prefix — never "
    "convert a path to an absolute one.",
    "a) `" + AUDIT + " --json " + R25 + "/c1-after.json | tail -1` prints `lines=35 pass=35 fail-closed=23 "
    "exit=0` and the command exits 0 (capture with `; echo exit=$?`).\n"
    "b) `git -C " + LANE + " diff --stat -- corpus/knowledge` lists exactly 29 files, 29 insertions and 29 "
    "deletions.\n"
    "c) `git -C " + LANE + " diff -U0 -- corpus/knowledge | grep -c '^+recheck:'` = 29 and every `-recheck:` "
    "line's command text survives inside its replacement (spot-check all 29 by eye in the diff).\n"
    "d) `git -C " + LANE + " diff -- corpus/knowledge | grep -E '^[-+]' | grep -v 'recheck:'` prints nothing.\n"
    "e) `python3 corpus/instruments/anchorcheck.py corpus/knowledge/triage-thresholds.md` exit unchanged "
    "(no line numbers moved).\n"
    "Report every command with its output and exit code.",
    "You are the sole writer of the `recheck:` line inside corpus/knowledge/*.md (existing files only). "
    "Write your report at " + W1 + "/FixRecheckLines.md."))

items.append(item(
    "EntryJapanVendors", "scribe",
    "C2. Write ONE new knowledge entry at corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md "
    "re-grounded from this round's captures of four Japanese vendor policy pages. Staged source package "
    "(read-only, do not copy its text): " + PKG + "/knowledge/corpus/knowledge/"
    "japanese-vendor-disclosure-policies-2026-10-23.md.",
    "The four captures are already committed this round (fetch time 2026-10-25T08:14Z):\n"
    "- S036 https://cybozu.co.jp/company/security-policy/ (sha256 022ca4f4…)\n"
    "- S037 https://cybozu.co.jp/products/bug-bounty/faq/ (sha256 b204aa7f…)\n"
    "- S038 https://pepabo.com/contact/vulnerability-reporting/ (sha256 09e077d3…)\n"
    "- S039 https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html (sha256 657e7b4c…)\n"
    "Files: corpus/source-snapshots/round-25/S0NN.txt.\n"
    "Write the entry to the lane's own bar (corpus/QUALITY.md Q1-Q6):\n"
    "- three header lines directly under the H1: `source:` (one per row id, with the URL and an exact "
    "anchor naming the section/heading you read), `verified-at: 2026-10-25`, `recheck:` one executable "
    "cwd-prefixed command line of the same form the round-25 fix uses (see any corpus/knowledge entry "
    "after the FixRecheckLines seat lands, or use: `recheck: cd " + LANE + " && python3 "
    "corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json "
    "--source S036 --source S037 --source S038 --source S039`).\n"
    "- every load-bearing claim carries a verbatim quote of <=25 words with its exact location, and every "
    "quote must appear EXACTLY ONCE in its capture (check with `grep -c`); if a quote occurs twice, pick a "
    "longer unique fragment or record the line number you will give the manifest.\n"
    "- state at least one falsifiable rule a reader can check against a report, and at least one rejected "
    "over-generalization with its reason (e.g. 'a Japanese vendor policy is a programme' — it is not).\n"
    "- attribution: each vendor's statement is that vendor's position, never a rule about vendors.\n"
    "- documentation only: no probing/scanning/credential material (Q6).\n"
    "Also write the machine-readable quote list at " + W1 + "/quotes-vendor-jp.json with shape "
    "{\"entry\": \"corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md\", \"records\": "
    "[{\"source\": \"S036\", \"quotes\": [{\"id\": \"Q1\", \"quote\": \"...\", \"location\": \"...\"}]}]} — "
    "one record per source, quote strings byte-identical to what you put in the entry (single-line, no "
    "markup).",
    "a) The file exists, `head -3` shows H1 + `source:`/`verified-at:`/`recheck:` in that order, and "
    "`grep -c '^source: S03[6-9]' <file>` >= 2.\n"
    "b) Every quote in " + W1 + "/quotes-vendor-jp.json occurs exactly once: show the `grep -c` result for "
    "each (1 expected).\n"
    "c) `grep -c '^recheck: cd " + LANE + " && ' <file>` = 1.\n"
    "d) `python3 -c 'import json;json.load(open(\"" + W1 + "/quotes-vendor-jp.json\"))'` exit 0.\n"
    "e) No line of the entry instructs testing, scanning or contacting any target (self-check against Q6).\n"
    "Report the file's line count, the quote table (source, quote, occurrences, location) and each command.",
    "You are the sole writer of corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md and "
    + W1 + "/quotes-vendor-jp.json. Report at " + W1 + "/EntryJapanVendors.md."))

items.append(item(
    "EntryCiscoCrosswalk", "scribe",
    "C2. Write ONE new knowledge entry at corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md "
    "re-grounded from this round's capture of Cisco's published vulnerability policy (S040) and crosswalked "
    "against the three Japanese vendor policies captured as S036/S038/S039. Staged package (read-only): "
    + PKG + "/knowledge/corpus/knowledge/vendor-cvd-policy-crosswalk-2026-10-23.md.",
    "Capture: corpus/source-snapshots/round-25/S040.txt, https://www.cisco.com/c/en/us/about/security-center/"
    "security-vulnerability-policy.html, sha256 b7f7b55f…, fetched 2026-10-25T08:14Z, http 200.\n"
    "Write to the lane's bar (QUALITY.md Q1-Q6): header `source:` lines naming S040 (and S036/S038/S039 where "
    "you compare), `verified-at: 2026-10-25`, and one executable cwd-prefixed `recheck:` line, e.g. "
    "`recheck: cd " + LANE + " && python3 corpus/instruments/source-recheck.py --manifest "
    "corpus/source-snapshots/round-25/manifest.json --source S040`.\n"
    "The crosswalk's point must be a checkable comparison, not a summary: what each policy commits to and "
    "what it leaves out (scope list vs process; named standard version; named coordination partners; the "
    "stated conditions for faster disclosure; whether money exists). Quote each vendor's own words <=25 "
    "words with a location, and keep attribution per vendor. Include one rejected over-generalization with "
    "its reason.\n"
    "Also write " + W1 + "/quotes-vendor-cisco.json in the same shape as the other quote list "
    "({'entry': ..., 'records': [{'source': 'S040', 'quotes': [{'id','quote','location'}]}]}).",
    "a) File exists; `head -3` shows H1 + `source:`/`verified-at:`/`recheck:`; `grep -c '^source: S040' <file>` "
    ">= 1.\n"
    "b) Every quote occurs exactly once in its capture — show each `grep -c`.\n"
    "c) `grep -c '^recheck: cd " + LANE + " && ' <file>` = 1; JSON list parses.\n"
    "d) The entry states at least one falsifiable rule and one rejected over-generalization with reason.\n"
    "Report line count, quote table and commands.",
    "You are the sole writer of corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md and "
    + W1 + "/quotes-vendor-cisco.json. Report at " + W1 + "/EntryCiscoCrosswalk.md."))

items.append(item(
    "QualityCriteria", "scribe",
    "Add the round-25 admission-bar criteria to corpus/QUALITY.md, append-only, grounded in measured "
    "evidence (never in prose alone). Two criteria are expected; add a third only if you can ground it.",
    "Append one table under a `## Round-25 additions — recheck-line form and vendor-policy admission` heading, "
    "rows in the file's existing `| id | criterion | grounded in |` shape:\n"
    "1. A recheck-line criterion (next free Q-id): a `recheck:` line is ONE executable command — it parses "
    "under `bash -n`, carries its own `cd <lane> &&` prefix so it runs from any cwd, and keeps any "
    "human note after a `#`. Grounded in D24-5 (5 of 35 lines prefixed) and this round's measured "
    "29/35 non-conforming (23 prose+command hybrids, 6 cwd-dependent), receipt "
    + R25 + "/c1-before.json.\n"
    "2. A record criterion (next free R-id): a counter's before/after must be produced by one frozen "
    "instrument whose limbs are each shown load-bearing by an isolating fixture (the round-25 "
    "recheck-audit.py selftest is the specimen). Grounded in R11 and the r24 finding that an unchanged "
    "instrument can be cited as a fix.\n"
    "3. Optional third: a vendor-policy admission criterion only if the captures support it (e.g. a "
    "crosswalk must quote each vendor's own words and never merge them into one rule).\n"
    "Do not rewrite, renumber or reorder any existing row; do not touch other sections. Keep every existing "
    "line at its number (R6): append at the end of the file.",
    "a) `git -C " + LANE + " diff --stat -- corpus/QUALITY.md` shows insertions only, 0 deletions.\n"
    "b) Each new row cites a receipt path or lesson pointer that exists (`test -e` each one).\n"
    "c) `grep -cE '^\\| [QR][0-9]+ ' corpus/QUALITY.md` increases by exactly the number of rows you added.\n"
    "Report the diff and the commands.",
    "You are the sole writer of corpus/QUALITY.md. Report at " + W1 + "/QualityCriteria.md."))

items.append(item(
    "InstrumentsCounts", "executor",
    "Close routed defects D24-2 and D24-3 in the lane's instruments documentation, with one measured number "
    "each. Three files disagree about the round-24 snapshot assertion count (instruments/README.md says 62, "
    "corpus/lessons/round-24.md says 77, the report and manifest say 76), and the bound-64-to-8 brace mutant's "
    "8/8 is stated as measured in four places while only the baseline-base 4/8 was measured.",
    "1. Derive the true assertion count from committed bytes, e.g. "
    "`python3 -c \"import json;d=json.load(open('corpus/source-snapshots/round-24/manifest.json'));"
    "print(sum(len(s['quotes']) for s in d['sources']))\"` and cross-check it against the receipt's OK-line "
    "count (`grep -c OK " + R25 + "/../round-24/c1-counterA-manifest-receipt.txt` if present, else the "
    "manifest sha count + quote count).\n"
    "2. In corpus/instruments/README.md, replace the wrong figure with the measured one and put the counting "
    "command next to it.\n"
    "3. In corpus/instruments/README.md, rewrite the bound-8 mutant sentence so it says exactly what was "
    "measured: the mutant scored 8/8 and 24/24 on the BASELINE bytes (receipt: round-24 ResolverAttack.md "
    ":151); no lane file records that mutant on the landed db5e0767… bytes.\n"
    "4. If corpus/QUALITY.md R11 carries the same overstatement, do NOT edit QUALITY.md (another seat owns it) "
    "— report the exact line to the L1 instead.\n"
    "5. Do not change any other content of README.md.",
    "a) `git -C " + LANE + " diff -- corpus/instruments/README.md` shows only the two edits.\n"
    "b) The counting command you added reproduces your number when run (paste output).\n"
    "c) `grep -n '62' corpus/instruments/README.md` and `grep -n '77' corpus/instruments/README.md` no longer "
    "return the assertion-count claim (report what they return).\n"
    "Report the number, the command, the output, and the exact QUALITY.md line if any.",
    "You are the sole writer of corpus/instruments/README.md. Report at " + W1 + "/InstrumentsCounts.md."))

items.append(item(
    "RowsScratch", "executor",
    "C2. Build the NORMALIZED append block for the five new registry rows in scratch, and validate it before "
    "any append. Nothing may be appended to corpus/SOURCES.md this round by you: the L1 appends after this "
    "wave returns.",
    "Id mapping (ids follow the document, never arithmetic): staged S055 cybozu security policy -> **S036**; "
    "staged S056 cybozu bounty FAQ -> **S037**; staged S057 pepabo -> **S038**; staged S060 hitachi HIRT -> "
    "**S039**; staged S068 cisco -> **S040**. Staged rows: " + PKG + "/SOURCES.append.md (read-only).\n"
    "Produce " + R25 + "/assimilation/rows/SOURCES.append.block.md containing the five rows in the lane's "
    "11-column schema (`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | "
    "used-by |`), each row normalised as follows:\n"
    "- `status` = `mined`; `opened` = `2026-10-25`; `recheck` = a schema-valid cadence (`180d`) — never prose.\n"
    "- NO cell may contain a literal or escaped `|`; rewrite any such anchor in your own words.\n"
    "- `used-by` names exactly the entries that cite the row: "
    "`corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` for S036-S039 and "
    "`corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` for S040 (add the JP entry too if it "
    "cites S040).\n"
    "- `anchor` and `teaches` must be checkable against the committed capture "
    "corpus/source-snapshots/round-25/S0NN.txt: keep a staged claim only if you can point at the line in the "
    "capture that supports it; otherwise correct it to what the capture says.\n"
    "Then build the scratch mirror " + R25 + "/assimilation/rows/validate/corpus/SOURCES.md = the lane's "
    "current corpus/SOURCES.md with your five rows inserted at the end of the Registry table, and run:\n"
    "  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "
    + R25 + "/assimilation/rows/validate/corpus/SOURCES.md\n"
    "Iterate until it exits 0 (warnings allowed). E03/E04 findings mean a duplicate id or within-scope "
    "duplicate URL: report it, do not paper over it.",
    "a) The block file has exactly 5 rows, each with 11 cells: "
    "`awk -F'|' '/^\\| S0/ {print NF-2}' <block>` prints 11 five times.\n"
    "b) `grep -c '|' <block>` consistent with 5 rows x 12 pipes; no `\\\\|` anywhere.\n"
    "c) The validate command exits 0 — paste the full output and `echo exit=$?`.\n"
    "d) Every `used-by` path in the block exists or is named by the two entry seats (say which).\n"
    "e) Every `anchor`/`teaches` claim you kept has a capture line pointer (paste the matching `grep -n`).",
    "You are the sole writer of " + R25 + "/assimilation/rows/**. Do not edit corpus/SOURCES.md. Report at "
    + W1 + "/RowsScratch.md."))

items.append(item(
    "CollisionGuard", "executor",
    "Prove the §10 id-collision guard for this lane and produce the renumber map, in scratch only.",
    "1. Run the campaign's collision check exactly as specified:\n"
    "   S=/home/vgpnk/Projects/shokuknow\n"
    "   A=" + R25 + "/assimilation/ids; mkdir -p \"$A\"\n"
    "   grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' " + LANE + "/corpus/SOURCES.md | grep -oE 'S[0-9]+' | "
    "sort > \"$A/reg-ids\"\n"
    "   grep -oE '^ {0,3}\\|[[:space:]]*S[0-9]{3,}' \"$S/merge/kasegi/SOURCES.append.md\" | grep -oE "
    "'S[0-9]+' | sort > \"$A/staged-ids\"\n"
    "   comm -12 \"$A/reg-ids\" \"$A/staged-ids\" > \"$A/collisions\"\n"
    "2. Prove the guard can fail: build a scratch registry fixture with an INDENTED row (`  | S002 |`) that "
    "the staged set also contains, run the same two greps over it, and show the collision list is nonempty. "
    "A column-zero-only pattern must be shown to miss it (that is the failure mode the guard exists to "
    "catch). Write the proof to " + R25 + "/assimilation/ids/guard-proof.txt.\n"
    "3. Produce the renumber map by DOCUMENT (id follows the URL/anchor, never arithmetic): "
    + R25 + "/assimilation/ids/renumber-map.md, listing staged id -> new lane id for every row the round "
    "adopts (S055->S036, S056->S037, S057->S038, S060->S039, S068->S040) with the document title beside each.\n"
    "4. Report the collision count and whether any collision falls on an ADOPTED row.",
    "a) " + R25 + "/assimilation/ids/{reg-ids,staged-ids,collisions} exist; paste their line counts and the "
    "collisions content.\n"
    "b) guard-proof.txt shows: indented fixture -> nonempty collision with the 0-3-space pattern, empty with "
    "a `^\\|` pattern (paste both commands and outputs).\n"
    "c) renumber-map.md has one line per adopted row with its document title.\n"
    "d) State the collision count (expected 5: S031-S035) and that no adopted id collides.",
    "You are the sole writer of " + R25 + "/assimilation/ids/**. Report at " + W1 + "/CollisionGuard.md."))

items.append(item(
    "AuditControls", "executor",
    "C1. Build the isolating controls for the frozen counter corpus/instruments/recheck-audit.py so every limb "
    "is shown load-bearing, on scratch copies only.",
    "1. Copy the BASE bytes of corpus/knowledge (as at b49948f) into a scratch tree: "
    "`git -C " + LANE + " show b49948f:corpus/knowledge/<file> > " + R25 + "/c1-controls/base/corpus/knowledge/"
    "<file>` for all 35 files, plus symlink or copy corpus/instruments.\n"
    "2. Run `python3 corpus/instruments/recheck-audit.py --root " + R25 + "/c1-controls/base` and record the "
    "receipt (it must reproduce lines=35 pass=6).\n"
    "3. Build four mutants of the base tree, one per limb, and score each with the same command:\n"
    "   M1 (parse limb): a line with a prose tail after the command, e.g. `... tool.py (note)`.\n"
    "   M2 (cwd limb): a valid line with the cd prefix removed.\n"
    "   M3 (paths limb): a valid cd-prefixed line naming a corpus/knowledge/ghost.md that does not exist.\n"
    "   M4 (degenerate): a line that is `cd <lane> && true` — must FAIL limb (c) (names no corpus path and no "
    "~/Projects/ test).\n"
    "4. Also score the do-nothing control: the unchanged base tree with the frozen target — it must NOT reach "
    "pass=35.\n"
    "Write receipts as " + R25 + "/c1-controls/<mutant>.txt with the command line, output and exit code.",
    "a) base receipt reproduces `lines=35 pass=6`.\n"
    "b) M1..M4 each fail exactly the intended limb (paste the limb triple `parse,cwd,paths`).\n"
    "c) If any mutant passes, say so loudly: the limb is not load-bearing and the claim's instrument is "
    "weaker than declared.\n"
    "d) The do-nothing control's pass count is reported (must be 6).",
    "You are the sole writer of " + R25 + "/c1-controls/**. Report at " + W1 + "/AuditControls.md."))

items.append(item(
    "LessonDraft", "scribe",
    "Draft the round-25 lesson's `## Mistakes` section (the §2b mined-mistake requirement) and the "
    "assimilation `## Gate` block skeleton. The L1 composes the final corpus/lessons/round-25.md; you write "
    "only the draft.",
    "Write " + W1 + "/lesson-mistakes.md containing:\n"
    "1. `## Mistakes` — mine at least two mistakes with the four required fields: class · evidence pointer · "
    "captured-by (the criterion or rule that should have caught it, or `none`) · fix. Candidates, each to be "
    "verified by you against committed bytes before you write it:\n"
    "   - 23 of 35 `recheck:` lines were prose+command hybrids that cannot run at all (`bash -n` syntax error) "
    "while Q7 (round 23) already required an executable command: class = gate-not-applied-to-legacy-entries; "
    "captured-by = Q7 was written for new entries and never swept over the 25 legacy ones.\n"
    "   - D24-5's routed defect under-counted the same surface (it named 30/35 cwd-dependent lines; the real "
    "before state is 6 cwd-dependent + 23 unparseable = 29 non-conforming): class = "
    "under-measured-routed-defect; captured-by = the round-24 closure ran one limb (exit-code equality) and "
    "never a parse check.\n"
    "   - D24-2/D24-3: one artefact described three times with three different numbers (62/77/76) and an "
    "unmeasured mutant score restated as measured in four places: class = self-description-as-claim (R2); "
    "captured-by = R2 existed but nothing checked the copies.\n"
    "   - A misroot you find in `git -C /home/vgpnk/Projects/shokunin status --porcelain` written by one of "
    "this round's seats (check at the end of your work; if none, say so).\n"
    "2. `## Gate` skeleton for the assimilation set: one block per adopted row (S036-S040) with URL, YOUR "
    "access date 2026-10-25, and a <=25-word located quote copied from the capture; plus one reject block "
    "(candidate: a staged entry you judge out of scope or duplicate — name it, give the failing criterion, and "
    "the flip condition).\n"
    "3. A short `## Fixes that can fail` list: for each fix above, the control that shows it can fail.",
    "a) Every quoted sentence in your draft occurs in the named capture (paste `grep -c` = 1 per quote).\n"
    "b) Every evidence pointer is a real path or command output you ran this session.\n"
    "c) The Gate block carries 5 admit rows + >=1 reject with reason and flip condition.\n"
    "d) No universal clause ('all', 'every', 'complete') unless your command enumerates the full set.",
    "You are the sole writer of " + W1 + "/lesson-mistakes.md. Report at " + W1 + "/LessonDraft.md."))

items.append(item(
    "LogDraft", "scribe",
    "Draft the round-25 LOG.md entry for the L1 to append.",
    "Write " + W1 + "/log-entry.md in the shape of the lane's existing LOG.md round entries (read the last "
    "three: `grep -n '^## Round 2[234]' LOG.md`): a heading `## Round 25 — <one-line theme>`, then bullets "
    "carrying: the two frozen claims with their counters, the assimilation set (S036-S040 + the refused "
    "candidate), the routed defects closed (D24-1..D24-5, one line each, with what closed it), the wave shape "
    "and seat counts (leave a placeholder `{{WAVES}}` for the L1 to fill), the census before/after (leave "
    "`{{CENSUS}}`), and the tool installs (none expected).\n"
    "Every number you state must be one you measured this session or read from a committed receipt; mark "
    "anything the L1 must fill with the placeholders above rather than guessing.",
    "a) The draft names both claims with a before value and a counter command.\n"
    "b) No invented commit hash: leave `{{LANE_HEAD}}` for the L1.\n"
    "c) The D24-1..D24-5 list is complete with one line each.\n"
    "Report the file and any number you could not verify.",
    "You are the sole writer of " + W1 + "/log-entry.md. Report at " + W1 + "/LogDraft.md."))

# ------------------------------------------------------------- read-only items
def ro(name, role, target, change, acceptance, path=None):
    return item(name, role, target, change, acceptance,
                "READ-ONLY. Your only output is " + (path or (W1 + "/" + name + ".md")) + ".", read_only=True)


items.append(ro(
    "CritPredicate", "critic",
    "Attack the frozen C1 predicate for vacuity. The claim is "
    "`lines=35 pass=35 exit=0` on corpus/instruments/recheck-audit.py; the before receipt is "
    + R25 + "/c1-before.json.",
    "Read the instrument and the receipt. Then attack:\n"
    "1. Limb (b) 'same exit status AND same output digest from two cwds' — can it pass vacuously (e.g. a "
    "command whose failure is identical in both cwds, like `true`)? Does limb (c) block that?\n"
    "2. Is a `fail-closed` line counted as verification anywhere a reader would read it as one? The summary "
    "prints fail-closed=23 — is that disclosed honestly enough, and does the report wording the L1 will use "
    "('35/35 recheck lines conform') overclaim?\n"
    "3. Does the predicate measure the axis it names (depth:verifiability) or does it measure operability "
    "(a runnable command)? Name the surface precisely and say what a reader can now do that they could not.\n"
    "4. Name at least one way a line could pass all three limbs while remaining useless to a reader, and "
    "whether the instrument should be changed (if so, say so now — before data, not after).\n"
    "Do not edit any file. Cite the instrument's line numbers.",
    "A verdict per attack: SOUND / WEAK (with the concrete gap) / BROKEN (with the case). If any attack "
    "should change the instrument BEFORE the fix lands, say so at the top in one line so the L1 can act.",
))

items.append(ro(
    "CritC1Axis", "critic",
    "Decide whether C1 belongs on depth:verifiability (score 4) or is really operability/calibration work, "
    "and whether it can be scored as an improvement at all.",
    "Read /home/vgpnk/Projects/shokunin/AXES.md (six axes), the lane SCORECARD.md axis rows, and "
    + R25 + "/claims.json. Answer:\n"
    "1. Is 'every entry's own recheck line runs from any cwd' verifiability (can a reader re-derive the "
    "entry's evidence) or operability (does the command run)? Quote the AXES definitions.\n"
    "2. Does the round-24 verifier's D24-5 framing ('residual cwd dependence') already concede this is "
    "verifiability? Cite corpus/lessons/round-24-verifier-spotcheck.md.\n"
    "3. If the score should move 4 -> 5, on what predicate; if it should stay 4, say why the count 6 -> 35 "
    "is nonetheless the axis's surface. The L1 will follow your recommendation and record it.\n"
    "Do not edit any file.",
    "One paragraph per question plus a one-line recommendation: `score 4 held` or `score 4 -> 5` with the "
    "predicate that justifies it.",
))

items.append(ro(
    "CritC2Ground", "critic",
    "Decide whether F10 (vendor-side disclosure policies as corpus objects) is ground the lane did NOT hold, "
    "i.e. whether it earns coverage credit.",
    "Check the lane's existing corpus for vendor-policy ground: corpus/knowledge/program-quirks.md, "
    "authorization-safe-harbor-and-scope.md, triage-thresholds.md, corpus/README.md coverage map, and "
    "SKILL.md sections that describe program rules. Then answer:\n"
    "1. Does any existing entry already document a vendor's own published disclosure policy (process, "
    "standard alignment, coordination partners, acceleration conditions)? Grep for it and cite lines.\n"
    "2. Is 'vendor policy' distinct from 'programme rules' (HackerOne/Bugcrowd/Cantina) and from "
    "F03/F09 (safe harbour, engagement documents)? State the distinction or the overlap.\n"
    "3. Would admitting it be breadth rather than depth — and does AXES/coverage allow breadth as a coverage "
    "move? Quote the axis definition.\n"
    "Do not edit any file.",
    "A verdict: `new ground` / `already held` (with the entry and line that holds it) / `overlapping ground` "
    "with the exact overlap, plus the sentence the L1 should put in the report.",
))

items.append(ro(
    "CritC2Scope", "critic",
    "PROVINCE scope check for the assimilation set: decide admit/refuse per staged entry, and name at least "
    "one reject with reason + flip condition (§10 requires >=1 admit and >=1 reject in the lesson Gate).",
    "Read " + LANE + "/PROVINCE.md (Core: program rules, scopes, claim packages, triage and claim gates, "
    "submission/disclosure packaging; Adjacent: sibling lanes; live-target testing refused). Then, for each of "
    "these staged entries (" + PKG + "/knowledge/corpus/knowledge/), give a verdict with the failing "
    "criterion or the admitting ground:\n"
    "1. japanese-vendor-disclosure-policies-2026-10-23.md (this round's captures S036-S039)\n"
    "2. vendor-cvd-policy-crosswalk-2026-10-23.md (S040)\n"
    "3. program-severity-ladders-and-reward-scales.md\n"
    "4. claim-packaging-and-report-quality.md\n"
    "5. program-scope-rules-and-asset-boundaries.md\n"
    "6. iso-29147-and-30111-division-of-labour-2026-10-23.md\n"
    "7. vendor-third-party-finding-coordination-2026-10-23.md\n"
    "For the one you refuse, state the flip condition (what would make it admissible). For anything that is "
    "another lane's ground, name the sibling lane. Do not edit any file.",
    "A table: entry | verdict (admit/refuse) | criterion (Q-id or PROVINCE line) | reason | flip. Plus one "
    "line: `reject for the lesson Gate: <entry> — <reason>`.",
))

items.append(ro(
    "RevPredicateIndependent", "reviewer",
    "Independently re-derive the C1 before count with your OWN implementation (not the lane's instrument) and "
    "compare per-line verdicts with " + R25 + "/c1-before.json.",
    "Write a throwaway script under " + R25 + "/wave1/rev-independent/ (your own implementation: parse check, "
    "two-cwd run with exit+output comparison, path existence). Run it over the 35 entries at base b49948f "
    "(export the base corpus/knowledge with `git -C " + LANE + " show b49948f:corpus/knowledge/<f>` into your "
    "scratch dir). Then diff your per-line PASS/FAIL vector against the receipt's. Report every disagreement "
    "with the line that caused it.",
    "a) Your independent count: `lines=35 pass=N`; the receipt says pass=6.\n"
    "b) Disagreements: list each (entry, your verdict, receipt verdict, reason). Zero disagreements is the "
    "expected result and must be stated with the vector compared.\n"
    "c) Name any definitional choice you made that could differ (e.g. output comparison strictness) and "
    "whether it changes the count.",
    path=W1 + "/RevPredicateIndependent.md",
))

items.append(ro(
    "MutAuditLimbs", "mutation-tester",
    "Mutation-test the frozen counter itself: mutate corpus/instruments/recheck-audit.py limb by limb in a "
    "scratch copy and show the before receipt changes.",
    "Copy the instrument to " + R25 + "/wave1/mut-audit/audit-mutant.py and build one mutant per limb: "
    "(a) `parse_ok` always returns True; (b) cwd limb compares exit status only (drop the digest comparison); "
    "(c) `paths` limb always returns True; (d) the summary's pass counter counts `fail-closed` as pass. Score "
    "each mutant against the BASE corpus/knowledge tree (export b49948f into scratch as the AuditControls seat "
    "does, or make your own copy) and record: mutant, receipt summary line, exit code, and whether the frozen "
    "before value changes.",
    "A table of 4 mutants: for each, does the mutant's `pass` differ from 6? A limb whose mutant changes "
    "nothing is NOT load-bearing — say so. Also state which mutant would let a do-nothing round claim pass=35.",
    path=W1 + "/MutAuditLimbs.md",
))

items.append(ro(
    "MutControlSkip", "mutation-tester",
    "Build the cheapest control that SKIPS the claimed work and score it with the frozen counter — the "
    "phase-4 rule ('a target a do-nothing control can reach is a wrong target').",
    "Enumerate the ways to reach `lines=35 pass=35` without doing the work: (1) delete all 35 recheck lines "
    "(what does the audit print? does it crash or print lines=0?); (2) replace every line with "
    "`cd <lane> && true`; (3) make every line `cd <lane> && test -e corpus/knowledge/<its own file>`; "
    "(4) point the audit at an empty corpus/knowledge dir. Run each on a scratch copy and score it. Then say "
    "which of these the frozen predicate blocks and which it does not, and whether the L1 must tighten "
    "anything before the after-measurement.",
    "a) A row per control: command, receipt summary, exit code, and whether it reaches pass=35.\n"
    "b) Control (1) and (2) verdicts are the important ones — if either reaches pass=35 the claim is void; "
    "state it plainly.\n"
    "c) If a control the predicate misses is cheap, name the one-line limb that would block it (the L1 will "
    "decide before the after receipt).",
    path=W1 + "/MutControlSkip.md",
))

items.append(ro(
    "RevRecheckSemantics", "reviewer",
    "Produce the per-file semantics table the fix must preserve: for each of the 35 entries, what its recheck "
    "line verifies today, whether it fails closed by design, and what the fail-closed base is.",
    "Read every `recheck:` line and the entry it belongs to (corpus/knowledge/*.md). For each, state: entry | "
    "class (passing / fail-closed) | base test (~/Projects/bounties, the-bounty-hunter, origin-work, ufo-fsd-"
    "alpha, none) | instrument (source-recheck.py / anchorcheck.py / none) | what a reader learns when it "
    "exits 0. Flag any line whose semantics are ambiguous (e.g. a test that would pass on a restored but "
    "different tree). This table is the reference the fix is reviewed against in wave 2.",
    "35 rows, one per entry. Plus a list of lines whose `test` would pass today (there should be none, or name "
    "them), and a list of entries whose recheck cannot ever verify anything even after restoration.",
    path=W1 + "/RevRecheckSemantics.md",
))

items.append(ro(
    "RevD24Counts", "reviewer",
    "D24-2: re-derive the round-24 snapshot assertion count from committed bytes and state ONE number with its "
    "command.",
    "Run at least two independent derivations: (a) sum of `len(s['quotes'])` over "
    "corpus/source-snapshots/round-24/manifest.json; (b) the OK-line count in the round-24 receipt "
    "(.ufo/waves/round-24/c1-counterA-manifest-receipt.txt) minus its sha lines; (c) any other the artefacts "
    "imply. Then check what corpus/instruments/README.md, corpus/lessons/round-24.md and the round-24 report "
    "say, and give the L1 the exact replacement sentence and the line numbers to change.",
    "a) Each derivation with its command and output.\n"
    "b) The one true number, and a per-file table of which file says what (path:line, value).\n"
    "c) The exact replacement sentence for each wrong file (instruments/README.md and the lesson; the report "
    "is historical and stays).",
    path=W1 + "/RevD24Counts.md",
))

items.append(ro(
    "RevBound8", "reviewer",
    "D24-3: establish exactly what was measured about the bound-64-to-8 brace mutant, and write the corrected "
    "sentence.",
    "Read .ufo/waves/round-24/c1-control-baseline.txt, c1-fixed.txt, the wave-1 ResolverAttack report under "
    ".ufo/waves/round-24/wave1/, corpus/instruments/README.md, SCORECARD.md round-24 section and "
    "corpus/QUALITY.md R11. Determine: on which resolver bytes was the mutant scored, what did it score, and "
    "does any committed file record that mutant against db5e0767… (the landed bytes)? Then write the one "
    "sentence that is true and the list of places to change.",
    "a) A table: artefact | claim | measured or inferred.\n"
    "b) The corrected sentence (<=40 words).\n"
    "c) The exact file:line list for the L1 to change, and which files are historical and stay.",
    path=W1 + "/RevBound8.md",
))

items.append(ro(
    "RevL4Reconcile", "reviewer",
    "D24-4: reconcile the three incompatible descriptions of L4's fail-before behaviour, with the receipt as "
    "the authority.",
    "Read the three artefacts named by the verifier (round-24 erratum 3 in SCORECARD.md, ResolverAttack.md "
    ":176 under .ufo/waves/round-24/wave1/, and .ufo/waves/round-24/c1-control-baseline.txt). State what each "
    "says, what the receipt actually shows for L4 (its primary assertion result and whether path_check ran), "
    "and write the single reconciling sentence for the round-25 lesson.",
    "a) The three claims quoted with path:line.\n"
    "b) The receipt's actual L4 row, quoted.\n"
    "c) The reconciling sentence, <=50 words, that a future reader can check against the receipt.",
    path=W1 + "/RevL4Reconcile.md",
))

items.append(ro(
    "RevFrontierHarness", "reviewer",
    "No-harm guard: confirm the round-24 capability still works on committed bytes (frontier recheck harness "
    "10/10) and that nothing the round touches breaks it.",
    "Run `python3 corpus/instruments/frontier-recheck-count.py` (read its --help first) and record "
    "`entries=K pass=P exit=`. Then check whether the 35 recheck lines this round rewrites are inputs to that "
    "harness: if yes, say exactly which and how the harness parses them, and whether a `cd ... && cmd # note` "
    "form still parses. If the harness would break, that is a blocker the L1 must fix before the fix lands.",
    "a) The harness receipt line and exit code.\n"
    "b) Whether the harness reads the 35 lines (yes/no with the code pointer that parses them).\n"
    "c) A verdict: `fix is safe for the harness` / `harness must change first` (with the exact reason).",
    path=W1 + "/RevFrontierHarness.md",
))

items.append(ro(
    "RevSourceRows", "reviewer",
    "Audit the five staged source rows for schema violations before normalization, and give the L1 the "
    "normalization table.",
    "Read " + PKG + "/SOURCES.append.md rows S055, S056, S057, S060, S068 and the lane schema in "
    "corpus/SOURCES.md. For each row report: column count, any literal or escaped `|` inside a cell, any "
    "prose in `recheck` (which must be an ISO date, `NNd`, or a symbolic cadence), any `used-by` pointer to a "
    "file that will not exist, and any claim in `anchor`/`teaches` you cannot locate in the committed capture "
    "corpus/source-snapshots/round-25/S0NN.txt (give the capture line that supports or refutes it).",
    "A 5-row table with the violations and the corrected cell value for each. Explicitly list any staged "
    "claim the captures do NOT support — those must not be appended as-is.",
    path=W1 + "/RevSourceRows.md",
))

items.append(ro(
    "RevQ9Q13", "reviewer",
    "Dedupe check for the round-25 QUALITY additions: show that no existing criterion already covers them.",
    "Read corpus/QUALITY.md in full (Q1-Q9, R1-R12). For the two planned additions (a recheck-line form "
    "criterion; a counter-instrument limb-isolation criterion) answer: does Q7/R7/R11/Q9 already cover it? "
    "Quote the closest existing row and say what it leaves out. Then propose the exact criterion text in the "
    "file's voice, with the grounding pointer, so the scribe seat can use it verbatim.",
    "a) For each planned criterion: closest existing row, quoted, and the gap.\n"
    "b) Proposed text, <=45 words each, plus the grounding pointer.\n"
    "c) A verdict: `new criterion justified` / `fold into <existing id>`.",
    path=W1 + "/RevQ9Q13.md",
))

items.append(ro(
    "RevManifestShape", "reviewer",
    "Document the exact contract the L1 needs to build corpus/source-snapshots/round-25/manifest.json and to "
    "verify it with source-recheck.py.",
    "Read corpus/instruments/source-recheck.py (arguments, exit codes, what it binds: path stem vs id, "
    "occurrence counting, anchor, normalization) and the round-24 manifest. Then write the precise schema for "
    "the round-25 manifest and the exact commands the L1 must run: (a) build check, (b) verify each entry's "
    "`recheck:` line exits 0, (c) a control that must FAIL (a corrupted quote), (d) the selftest if it "
    "exists. Name every field the checker actually reads and any field it ignores.",
    "a) The schema, field by field, with which fields the checker reads.\n"
    "b) The exact commands with expected output for the four checks.\n"
    "c) Any trap (e.g. a quote that must carry `anchor`, a path stem that must equal the id).",
    path=W1 + "/RevManifestShape.md",
))

items.append(ro(
    "RevQuotesJP", "reviewer",
    "Independently verify the Japanese captures support the claims the two new entries will make.",
    "For each capture corpus/source-snapshots/round-25/S036.txt, S037.txt, S038.txt, S039.txt, S040.txt: "
    "locate with `grep -n` the sentences that support these claims and report the line + the verbatim "
    "sentence (<=25 words):\n"
    "S036: intake sources include the bounty programme and the early-warning partnership; scope = all services "
    "and products the company creates plus third-party products it uses; CVSS is one severity indicator; "
    "disclosure scope and the JVN simultaneous-disclosure principle.\n"
    "S037: invitation/account gating, target-product list, payout timing, what to do if not in the programme.\n"
    "S038: no-legal-action policy and its conditions; no bounty programme; prohibited acts list.\n"
    "S039: product-vendor IRT focus; the coordinated route when another vendor's product is affected.\n"
    "S040: ISO/IEC alignment sentence; named coordination partners; the conditions for faster disclosure; the "
    "definition reservation.\n"
    "Flag any claim the capture does NOT support — that claim must not enter an entry.",
    "A table per source: claim | capture line | verbatim sentence | supported (yes/no). Any unsupported claim "
    "is listed separately at the top.",
    path=W1 + "/RevQuotesJP.md",
))

items.append(ro(
    "ScoutStagedAnchors", "scout",
    "Compare the staged rows' `anchor` cells against what the committed captures actually contain.",
    "For rows S055, S056, S057, S060, S068 in " + PKG + "/SOURCES.append.md, take each named section/heading "
    "in the `anchor` cell and look for it in the matching capture (S036/S037/S038/S039/S040). Report which "
    "anchors resolve to a real heading in the capture, which name a heading that does not exist, and which "
    "are too vague to check. Do not edit anything.",
    "A 5-row table: staged id | anchor cell | capture | found (exact heading text + line) or NOT FOUND. Plus "
    "a one-line verdict on whether each row's anchor must be rewritten before append.",
    path=W1 + "/ScoutStagedAnchors.md",
))

items.append(ro(
    "ScoutCensusWarnings", "scout",
    "Establish the census baseline and the duplicate-URL risk for the five new rows before any append.",
    "Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root "
    "/home/vgpnk/Projects/shokunin kasegi` and record the full output + exit code. Read the census script's "
    "warning codes (W04 etc.). Then check whether any of the five new URLs already appears in "
    "corpus/SOURCES.md (grep the host+path), and whether any new URL shares a host with an existing row in a "
    "way the census would flag. Report the exact warnings the append is expected to add, if any.",
    "a) Census output + exit code (before).\n"
    "b) Duplicate-URL check per new URL: existing row or none.\n"
    "c) The expected post-append warning set (list), so the L1 can prove the append adds none.",
    path=W1 + "/ScoutCensusWarnings.md",
))

items.append(ro(
    "ScoutQuarantine", "scout",
    "Derive kasegi's slice of the campaign's absent-defect register and hand-check it (read-only; the register "
    "is never edited).",
    "Run the §10 slice command against "
    "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:\n"
    "  awk -F'|' -v l='kasegi' '$2 ~ (\"`\" l \"`\") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "
    "<register>\n"
    "Derive the slice yourself (the register's header and its `## By lane` totals are stale — say what they "
    "claim vs what you derive). Then for each slice row: fetch the cited source if a URL is derivable, locate "
    "the quote, and give a verdict: present (adopt-able with the anchor you located) / absent (fabrication "
    "class) / unverifiable (a prose class cell such as 'could not be fetched'). Do not edit the register.",
    "a) The slice command, its output and the row count (state the register's claimed count beside it).\n"
    "b) One verdict line per row: id | class | evidence.\n"
    "c) A one-line statement of whether any row in the slice is adoptable this round.",
    path=W1 + "/ScoutQuarantine.md",
))

items.append(ro(
    "ScoutConsiderthese", "scout",
    "Mine ONE still-unimplemented proposal from considerthese/2026-10-24.md and ground it through the lane's "
    "own bar (the reflection is a pointer, not evidence).",
    "Read considerthese/2026-10-24.md. Its proposals: (1) rechecker normalization + exactly-once/anchor — "
    "landed as Q8/Q9 in round 24; (2) capture clean text so quotes do not have to anticipate markup — check "
    "whether that is landed (read corpus/instruments/capture-source.py and the round-24 manifest: is a "
    "canonical clean-text rendering recorded, or only a compare-time normalization?); (3) close the r23 "
    "dossier — landed r23; (4) cadence — operator-owned; (5) PR fate — operator-owned. Pick the highest-value "
    "still-unimplemented one, verify the current state with commands, and write the grounded form: what the "
    "lane should do, which file it lands in, and the evidence that shows the gap today. Cite "
    "considerthese/2026-10-24.md + its date.",
    "a) Which proposals are landed (with the file/line that lands each) and which are not.\n"
    "b) The chosen proposal, grounded: current-state command + output, the gap, and the minimal landing "
    "(which file, which criterion or code).\n"
    "c) One line the L1 can put in the report: `considerthese: proposal N mined — <one clause>`.",
    path=W1 + "/ScoutConsiderthese.md",
))

items.append(ro(
    "ScoutNoHarm", "scout",
    "Establish the no-harm baseline for the round: the three measurement proxies as they stand before the fix.",
    "Run and record, with exit codes:\n"
    "1. `python3 corpus/instruments/density.py SKILL.md --label r25-before` (file mean, path-citation "
    "instances, block count).\n"
    "2. `python3 corpus/instruments/anchorcheck.py SKILL.md` (bad count, LOST-RECORDED).\n"
    "3. `git -C " + LANE + " status --porcelain` and `git -C " + LANE + " rev-parse master` (base).\n"
    "4. sha256 of corpus/instruments/resolve.py, SKILL.md, corpus/README.md, SCORECARD.md at b49948f (so the "
    "closure can show which files the round did not touch).\n"
    "Do not edit anything.",
    "A receipt file with each command, output and exit code, plus a table `path | sha256 at b49948f`. The L1 "
    "will re-run the same commands after the round and diff.",
    path=W1 + "/ScoutNoHarm.md",
))

items.append(ro(
    "ScoutFetchCisco", "scout",
    "Independently re-fetch Cisco's vulnerability policy and locate the four sentences the crosswalk entry "
    "depends on, so the L1 knows the capture is not a fluke.",
    "Fetch https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html with the "
    "lane's capture UA (`kasegi-shokunin/1.0`) and record http status + bytes; compare the body text to "
    "corpus/source-snapshots/round-25/S040.txt (diff a normalized text extraction). Then locate with "
    "`grep -n` in the committed capture: the ISO/IEC alignment sentence, the coordination-partner list "
    "(CERT/CC, CERT-FI, JP-CERT, NPSA), the two acceleration conditions, and the vulnerability-definition "
    "sentence. Report line + verbatim text (<=25 words each).",
    "a) Fetch receipt: status, bytes, sha256, and whether a re-extraction matches S040.txt.\n"
    "b) Four located quotes with capture line numbers.\n"
    "c) Any sentence the staged package claims that the capture does not contain.",
    path=W1 + "/ScoutFetchCisco.md",
))

items.append(ro(
    "ConnectorSiblings", "connector",
    "Sibling-overlap scan: does another fleet lane already hold vendor-disclosure-policy ground or recheck-line "
    "hygiene, and would this round's move collide with it?",
    "Scan /home/vgpnk/Projects/shokunin/*-shokunin for lanes whose PROVINCE/SKILL/corpus covers: (a) vendor "
    "security policies / CVD policy reading, (b) corpus recheck-line or provenance-field discipline "
    "(kotoba, chousa, kengaku, kumitate, kaidoku are the likely neighbours). Use grep over their PROVINCE.md "
    "and corpus/README.md, not whole-tree reads. For each hit, name the lane, the file:line, and whether the "
    "ground is the same surface or merely adjacent. Then state whether kasegi's F10 and its recheck criterion "
    "should be reported as contested scope (adjacency evidence) to the integrator.",
    "a) A table: lane | file:line | what it holds | same/adjacent.\n"
    "b) A verdict: `no collision` / `adjacent — report as adjacency` / `collision — route to <lane>`.\n"
    "c) The one sentence the L1 should put in the report's Sources & frontier or Trend verdicts section.",
    path=W1 + "/ConnectorSiblings.md",
))

items.append(ro(
    "SentinelCapture", "sentinel",
    "Security review of this round's external captures and of the two new entries' planned content.",
    "1. Review corpus/source-snapshots/round-25/S036-S040.txt for: credential material, session tokens, "
    "private URLs, personal data beyond a public contact address, and any instruction-like text that a "
    "future reader could mistake for the lane's own directive (prompt-injection class).\n"
    "2. Check the round's planned entries against QUALITY Q6 (documentation-only: no probing, scanning, "
    "logging in, or submitting against a target; no credential or vault-reference URI): read the two entry "
    "files if they exist by the time you run, otherwise the staged package versions.\n"
    "3. Check that no seat has written outside the lane (spot-check `git -C /home/vgpnk/Projects/shokunin "
    "status --porcelain` for files naming kasegi round 25) and report what you find without deleting "
    "anything.",
    "a) Per capture: clean / finding (with the line and the class).\n"
    "b) Q6 verdict per entry.\n"
    "c) Any misrooted file you observed (path + first line), for the L1's misroot sweep.",
    path=W1 + "/SentinelCapture.md",
))

items.append(ro(
    "RevReportFacts", "reviewer",
    "Assemble the evidence-pointer table the L1's report needs, from committed receipts only.",
    "Collect, with the exact command that reproduces each: (1) the C1 before/after receipt lines; (2) the "
    "instrument digest; (3) the five capture digests; (4) the frontier count before; (5) the census before; "
    "(6) the 35 recheck lines' file list; (7) the lane base revision. For each, give the command and its "
    "output. Flag any figure that appears in more than one lane file with different values (the round-24 "
    "failure mode).",
    "A table: fact | command | output | single-source (yes/no). Any conflicting figure is listed at the top.",
    path=W1 + "/RevReportFacts.md",
))

items.append(ro(
    "ScoutMisroot", "scout",
    "Misroot sweep input: list untracked/modified files at the fleet root and decide which (if any) were "
    "written by this round's seats.",
    "Run `git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec) and for each entry whose path "
    "is not a known driver artefact, read its first 10 lines and decide: written by a kasegi round-25 seat "
    "(names kasegi / round 25), another lane's seat (names that lane), or driver/operator state (never touch: "
    ".ufo/state/*, .scratch/*). Never delete or move anything — the L1 does that.",
    "a) The status output.\n"
    "b) A table: path | author lane or driver | evidence (quoted first line) | action for the L1 "
    "(copy+delete / leave).\n"
    "c) Explicitly name .scratch/ paths as never-a-misroot if any appear.",
    path=W1 + "/ScoutMisroot.md",
))

items.append(ro(
    "RevWaveEvidence", "reviewer",
    "Verify the provenance of this wave's own receipts: every committed receipt must name the command, the "
    "input bytes and the exit code it claims.",
    "Walk " + R25 + " (excluding wave1/*.md seat reports) and for each receipt file (c1-before.json/.txt, "
    "c1-instrument-digest.txt, assimilation/*, c1-controls/* as they exist when you run): check that (a) it "
    "names or is reproducible by a stated command, (b) the numbers it prints match a re-run you perform "
    "where feasible, (c) it carries the input digest it claims. Report any receipt that cannot be reproduced "
    "or that omits its command.",
    "A table: receipt | command | reproduced (yes/no/not-feasible) | mismatch detail. Plus a verdict on "
    "whether the wave's evidence is closure-checkable.",
    path=W1 + "/RevWaveEvidence.md",
))

items.append(ro(
    "SimplifierScope", "simplifier",
    "YAGNI check: is any part of the planned round-25 work deletable or already covered, so the round adds "
    "less new weight?",
    "Review: (a) corpus/instruments/recheck-audit.py — could an existing instrument (anchorcheck.py, "
    "frontier-recheck-count.py, source-recheck.py) already answer the C1 question, making the new instrument "
    "dead weight? (b) the two planned entries — is one of them a duplicate of the other's ground? (c) the "
    "round's planned QUALITY criteria — does one duplicate an existing row (see corpus/QUALITY.md)? Give a "
    "delete/fold recommendation per item with the evidence.",
    "A row per item: keep / fold into <existing> / delete, with the reason and the line that decides it. Do "
    "not edit anything.",
    path=W1 + "/SimplifierScope.md",
))

spec = {
    "wave": "kasegi-r25-build",
    "context": CONTEXT,
    "reportDir": ".ufo/waves/round-25/wave1",
    "maxLanes": 44,
    "axes": ["depth:verifiability", "coverage"],
    "milestone": "round-25 build wave: C1 recheck-line conformance + C2 F10 assimilation",
    "items": items,
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wave1-spec.json")
with open(out, "w", encoding="utf-8") as handle:
    json.dump(spec, handle, ensure_ascii=False, indent=1)
    handle.write("\n")
print("wrote", out, "items", len(items))
from collections import Counter
print(Counter(i["role"] for i in items))
names = [i["name"] for i in items]
assert len(set(names)) == len(names), "duplicate names"
