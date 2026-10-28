# R44Scribe4 — round-44 lesson mistake rows (draft, report only)

- seat: `R44Scribe4` (scribe, leaf). Item: **draft lesson mistake rows for round 44 — class / evidence /
  captured-by / fix, no unsupported claims.** Report-only: no production edit, no commit, no git/jj/index
  mutation, no lane-tree write except this file.
- lane: `kasegi-shokunin`; round 44; HEAD at inspection `66314015122b9aa32dc40f2f1815df56624c26d1`
  (freeze commit, `2026-10-28 15:47:51 -0300` = `18:47:51Z`); frozen base named by the control is
  `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`.
- scope: read-only re-derivation over committed bytes plus the round's own uncommitted wave artifacts.
  Nothing here grades C1/C2; it files round-44 defects the lesson must carry.

## 1. Method (commands actually run)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
git rev-parse HEAD; git status --porcelain; git diff --stat
git ls-tree -r --name-only 6631401 -- .ufo/waves/round-44
git ls-tree -r --name-only 5ab3a60 -- .ufo/waves/round-44 corpus/source-snapshots/round-44   # 0 lines
sed -n '1,25p' .ufo/waves/round-44/controls/do-nothing.txt
python3 -c '<decode claims.json counter, run it verbatim>'
bash -c "$(sed -n '10p'|'11p'|'12p' .ufo/waves/round-44/controls/do-nothing.txt)"   # as written, and with ' => …' stripped
grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md            # 0
grep -cE '^\| F[0-9]+ \| .* \| admitted \|' corpus/README.md      # 26 (25 at 5ab3a60)
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   # 70 (68 at 5ab3a60)
find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l            # 63 (62 at 5ab3a60)
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root …/kasegi-shokunin kasegi ; echo exit=$?
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi ; echo exit=$?
ls -la --time-style=full-iso /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
python3 -c '<raw API JSON vs pinned snapshot: sizes, sha256, body+LF equality>'
du -sh .ufo/scratch/kasegi-r44; git check-ignore -v .ufo/scratch/kasegi-r44
grep -rn "7e2004ba" corpus/ .ufo/waves/round-44/                  # no hits
grep -rn "kasegi-round-claims" --include=*.py --include=*.sh --include=*.json corpus/ .ufo/waves/round-44/ /home/vgpnk/Projects/shokunin/scripts | grep -v claims.json   # no hits
```

## 2. Do-nothing discrimination (applies to every row)

`git ls-tree -r --name-only 5ab3a60 -- .ufo/waves/round-44 corpus/source-snapshots/round-44` → **0 lines**.
Every artifact a row below cites (the claims file, both controls, the S069 manifest, the new knowledge
entry, `.ufo/scratch/kasegi-r44/`) is absent at the frozen base, so a do-nothing replay at `5ab3a60`
produces none of these rows. The rows are therefore round-44 artifacts, not inherited ones; the
inherited-defect set is C1's business and is not widened here.

Per-row status at base: M44-1, M44-2, M44-3, M44-4, M44-8 cite **committed** bytes of `6631401`
(`claims.json` blob `f63f5546b1696da529fe3d3781597581299c90bf`; `controls/do-nothing.txt` blob
`08c0209d8aa451ea9cd562c433549cad5d4e8b40`). M44-5, M44-6, M44-7 cite **uncommitted working-tree**
bytes (untracked control, untracked manifest, untracked scratch) — flagged in §6.

## 3. Mistake rows (schema of `corpus/lessons/round-43.md` §Mistakes)

| id | class | event | evidence | captured-by | fix | able to fail |
|---|---|---|---|---|---|---|
| M44-1 | receipt not reproducible (a control's command text is not a command) | `controls/do-nothing.txt:10-12` record the C2 counting commands **with their outputs inline** (`… => 25`) and with doubled ERE pipes (`'^\\| F[0-9]+ \\| .* \\| admitted \\|'`). Run as written: `bash -c "$(sed -n '10p' …)"` → `grep: =: No such file or directory`, rc=2; line 11 same; line 12 → `wc: '=': No such file or directory`, rc=1. With ` => …` stripped but the doubling kept: line 10 → **631**, line 11 → **149**, against the recorded **25** and **68**. The intended selector (single pipes, `.*` kept) prints **25/68/62** at `5ab3a60` and **26/70/63** now. | `sed -n '8,12p' .ufo/waves/round-44/controls/do-nothing.txt`; the five runs above with their rc/stdout; `git show 5ab3a60:corpus/README.md \| grep -cE '^\| F[0-9]+ \| .* \| admitted \|'` → 25 | none before this seat — no gate re-executes a control's command text, and R39 grades receipts, not command cells | store the counting commands in an executable file (or single-escaped ERE with no inline output), and have the round's control step re-execute each command and compare its stdout to the recorded token; a mismatch is a control defect, not a rounding difference | re-running the stored command prints 25/68/62 at `5ab3a60` and 26/70/63 at the round head, and the comparison fails today (631≠25, 149≠68) |
| M44-2 | counter selector (a frozen counter cannot reproduce its own before literal) | `claims.json:23` C2 counter is `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md; …`. It omits the `.*` segment the control has, so it requires `admitted` to be the **second** cell; every frontier row carries it as the **third** (`corpus/README.md:202` `\| F01 \| CVSS v4.0 … \| admitted \| …`). Run verbatim from the JSON: stdout `0 / 70 / 63`, exit 0 — the first token is 0 at the frozen base too, where the control records 25. | `python3 -c` decode-and-run of `claims.json:23` → `0`,`70`,`63`; `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md` → 0; at `5ab3a60` → 0; the `.*` form → 26 (25 at base); `sed -n '202p' corpus/README.md` | none — the control used a different selector, so no comparison between counter and control ever fired | amend the frozen counter to the control's selector (and record the amendment as an erratum), and add the freeze-time rule that every frozen counter is executed against the frozen base and must print its own `before` literal | the counter prints 25 at `5ab3a60` and 26 at the round head; today it prints 0 and 0 |
| M44-3 | freeze-record timestamp (R44 recurrence, and a regression from round 43) | `claims.json:5-6` record `"author": "KasegiR44"` and `"frozen_at": "2026-10-28"` — a bare date, no instant, no `Z`; round 43's record carried `"frozen_at_utc": "2026-10-28T16:37:07Z"` and `"frozen_by"` (`git show 5ab3a60:.ufo/waves/round-43/claims.json`, lines 6-7). Neither round-44 control states a `measured-at` instant either (`controls/do-nothing.txt:1` "measured 2026-10-28"), so the ordering R44 asks for cannot be derived from any artifact; the only corroborated instant is the containing commit's `18:47:51Z`. | `sed -n '1,8p' .ufo/waves/round-44/claims.json`; `git show 5ab3a60:.ufo/waves/round-43/claims.json \| sed -n '6,7p'`; `git log -1 --format='%H %ci' 6631401`; `corpus/QUALITY.md:370` (R44) | `corpus/QUALITY.md:370` — the criterion exists (round-43 addition) and nothing reads `claims.json`, so it recurred | append a round-44 erratum (or the claims' own correction block) stating the instant actually corroborated by the containing commit, and make the claims schema carry `frozen_at_utc`/`frozen_by` again; add a check that reads the claims file | the check rejects `2026-10-28` (no `T`, no `Z`) and accepts an instant ≥ the controls' `measured-at` and ≤ the commit stamp |
| M44-4 | non-executable counter (a freeze declares a measurement it cannot run) | `claims.json:14` C1 counter is `python3 corpus/instruments/r44-routed-defects.py --root <lane-export> --baseline <frozen-base>`: the instrument is absent (`ls` → `No such file or directory`; control §"Do-nothing result" agrees "no r44 counter exists"), both arguments are angle-bracket placeholders, and the claims file has no `base` field to substitute into `--baseline` (top-level keys are `author, claims, frozen_at, lane, round, schema`); the base appears only in `controls/do-nothing.txt:2` (and the control's own §C1 line 7 records "no r44 counter exists"). | `sed -n '14p' .ufo/waves/round-44/claims.json`; `ls corpus/instruments/r44-routed-defects.py`; `python3 -c 'print(sorted(json.load(open(".ufo/waves/round-44/claims.json"))))'`; `sed -n '2p' .ufo/waves/round-44/controls/do-nothing.txt` | `R44Review9.md:14` (a seat read the path and recorded `not found`); the placeholders and the missing `base` are new here | land the instrument and freeze a literal invocation with the concrete base, or freeze the cell as `<pending: instrument>` and grade C1 `report-only` until the run exists | substituting the frozen base into the counter runs it and prints one line per routed defect; today the counter cannot be invoked at all |
| M44-5 | receipt mismatch (recorded stdout is not the tee of a run of the shipped script) | `controls/census-invocation-error.txt:1-6` record, "while following the prompt's literal command", `ERROR: config not found: …/kasegi-shokunin/shokunin.conf` then `ERROR: no lanes parsed from …/kasegi-shokunin/shokunin.conf`, exit=2. Executing that same line 2 from the lane dir **and** from the fleet root prints `ERROR: unknown lane (not a dir, not in conf or root): kasegi` as the second line, exit=2. `scripts/sources-census.sh` is unchanged since `2026-10-19 21:22:45` (last commit `f47ad6ba`, 2026-10-25), and its `no lanes parsed from` branch is line 507 while `unknown lane` is line 525. The prompt's own census command (`/home/vgpnk/Projects/shokunin/.ufo/prompts/kasegi-round-44.md:65`) names the **fleet** root; the lane-root form occurs **0** times in the prompt and **0** times in `wave1-dispatch.json`, so line 1's attribution to "the prompt's literal command" is unbacked as well. | the two runs above with their exit codes; `grep -n "no lanes parsed\|unknown lane" scripts/sources-census.sh` → 507, 525; `ls -la --time-style=full-iso scripts/sources-census.sh`; `grep -c "sources-census.sh validate --root /home/vgpnk/Projects/shokunin/kasegi-shokunin" .ufo/prompts/kasegi-round-44.md` → 0; `grep -c sources-census wave1-dispatch.json` → 0 | none — the control is untracked and no gate reads it | re-run and replace the file with the real tee (it is uncommitted, so this is a pre-landing repair, not an append-only correction), keep both invocations, and correct the attribution sentence | the recorded second line equals the executed second line, and the attribution names the document that actually carries the lane-root form |
| M44-6 | provenance (the pin is not reproducible from the declared `url`) | `corpus/source-snapshots/round-44/manifest.json:6` declares the HTML rules page; `:15-17` pin `sha256 0932279c…`, `bytes 45681`. Re-derivation: the raw article-API response in `.ufo/waves/round-44/source-recon/S069.txt` is **47136 B**, sha256 `7e2004ba30638ba8ce2a123d6385ade62685e148c661b46ffd93519db0bc4609`; its `body` field is **45680 B**, sha256 `d1198fc99109172025fcfa55eb0d6ad58a938e8ac281b4ded7f76fa10d5cf804`; `body + b"\n" == snapshot` is **True**. So the pinned stream is a locally re-terminated API body, not the HTML page and not the raw response; the raw digest `7e2004ba…` appears nowhere in `corpus/` or `.ufo/waves/round-44/`. `capture-binding-check.py:113-123` defines exactly this vocabulary (`snapshot_sha256`, `full_text_sha256`, `capture_url`/`http.final_url`) and the record carries none of them; rule B5 only compares the `url` text to the registry row's token. The knowledge entry does disclose "captured through the official article API" in prose, so the capture is disclosed, not hidden — the machine-readable record is what is missing. | the `python3` re-derivation above; `grep -n '"url"\|"sha256"\|"bytes"' corpus/source-snapshots/round-44/manifest.json`; `grep -rn 7e2004ba corpus/ .ufo/waves/round-44/` → no hits; `corpus/instruments/capture-binding-check.py:113-123`; `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md:3` | none — B5 compares url text, E2 hashes local bytes, E3 fires only when `capture_url`/`http` are present | append the request URL and the raw-response digest to the manifest (a `capture_url` + `full_text_sha256` block, or a round-44 erratum beside the record), and extend the check so extracted captures must name the request that produced them | the check fails today on a record whose `url` fetch hashes differently from its pin; after the fix, re-fetching `capture_url` reproduces the pinned digest, and the body-plus-LF step is stated |
| M44-7 | scratch discipline / landing hygiene | `.ufo/scratch/kasegi-r44/` sits **inside the lane work tree** and holds **4.2 GB** (`R44Conn2` 3.8 GB, `R44Simplifier1` 311 MB, `R44Critic10` 8.1 MB, `R44Mutant4` 428 KB). It is untracked (`git status --porcelain` → `?? .ufo/scratch/`) and **not** ignored (`git check-ignore -v .ufo/scratch/kasegi-r44` → rc 1; `.gitignore:1` only names `.ufo/interactive-sessions/`). The round prompt puts every clone and work tree under `$HYAKU_SCRATCH/kasegi-r44/<seat-name>/` (`.ufo/prompts/kasegi-round-44.md:669-671`) and `5ab3a60` has **0** files under `.ufo/scratch`. | `du -sh .ufo/scratch/kasegi-r44`; `find .ufo/scratch -maxdepth 2`; `git check-ignore -v .ufo/scratch/kasegi-r44` (rc 1); `git status --porcelain`; `git ls-tree -r --name-only 5ab3a60 -- .ufo/scratch \| wc -l` → 0 | the prompt §7 directive and the M43-5 precedent; no gate sweeps the lane tree for it | seats place clones under `$HYAKU_SCRATCH/kasegi-r44/`; the L1 deletes `.ufo/scratch/kasegi-r44` before landing and checks that `git status --porcelain` has no `.ufo/scratch` entry — deleting, not gitignoring, is the fix | the landing check fails today on the untracked 4.2 GB entry and passes after the directory is removed |
| M44-8 | decorative schema label (a claim of machine-checkability with no checker) | `claims.json:2` declares `"schema": "kasegi-round-claims-v1"`, a schema id no earlier round used (round 43's file carried **no** `schema` key) and no consumer knows: `grep -rn "kasegi-round-claims"` over `corpus/`, `.ufo/waves/round-44/` and the fleet `scripts/` finds **0** hits outside the claims file itself. The declared shape also drops fields round 43 carried (`base`, `frozen_at_utc`, `frozen_by`, per-claim `predicate`, `counting_commands`, `score_before/after`). | `sed -n '1,8p' .ufo/waves/round-44/claims.json`; `git show 5ab3a60:.ufo/waves/round-43/claims.json \| python3 -c '…print(sorted(d))…'` → no `schema`, has `frozen_at_utc/frozen_by/base`; the zero-hit `grep` above | none | either land a validator for `kasegi-round-claims-v1` (shape + required `base`/`frozen_at_utc`) and run it in the round's gate, or drop the label and name the record free-form — a schema id with no reader is a claim about tooling | the validator accepts the round-43 record and the round-44 record and rejects one with a missing `base`; today no command reads the field |

## 4. Candidates I examined and did **not** file (discrimination)

- **S069 quote anchors (`manifest.json:20-22`).** All three quotes are hard-wrapped, so none is a literal
  single-line substring (`grep -nF` for Q1/Q2/Q3 → no match); but `source-recheck.py:103-113` verifies an
  anchor against a **four-line window** (`" ".join(raw_lines[anchor-1:anchor+3])`, normalized), and Q1
  (L61-62), Q2 (L62-63) and Q3 (L70-72) all fall inside their declared windows. The anchors are legal under
  the lane's own rule — no row.
- **`verified-at: 2026-10-28` in the new entry.** Date-only is the lane convention: 50 of the 62 committed
  entries carry `verified-at: YYYY-MM-DD` alone (12 annotate the date, none omits the field;
  re-derived over `git ls-tree -r 5ab3a60 corpus/knowledge/` → 62 files, 50 / 12 / 0). No row.
- **The entry's recheck command.** `source-recheck.py` defines `--manifest` and `--source`
  (`grep -n add_argument` → 397-398), so the entry's cited command is runnable as written. No row.
- **Uncommitted `PROVINCE.md` (+2), `corpus/README.md` (+19), `corpus/SOURCES.md` (+2),
  `knowledge-expected.txt` (+1).** These are the L1's in-flight integration of F26/S069/S070/entry; the
  PROVINCE append is an end-of-file R6 append naming F26. Mid-round state, not a defect.
- **The correct census invocation reproduces.** `--root /home/vgpnk/Projects/shokunin kasegi` → `W04 S028`,
  `W04 S029`, `kasegi ok …/corpus/SOURCES.md`, exit 0 — identical to the control's after-line, so M44-5 is
  about the *error* record only, not about the census result.

## 5. Watch items (not rows — they may be transient)

- `.ufo/waves/round-44/wave1.ready.dispatched` and `.ufo/waves/round-44/source-recon/` are untracked; the
  recon raw response is the only copy of the `7e2004ba…` bytes M44-6 needs, so either land it or record its
  digest in the manifest erratum before it is deleted.
- `.ufo/waves/round-44/wave1.ready.partial` existed during the wave (`R44Review9.md:12`,
  `R44Review16.md:19`) and is gone now; a reader citing it would cite a vanished path.
- No round-44 artifact has been committed yet beyond the freeze commit, so §6 limits bite for every row.

## 6. Limitations

- The round is live. `claims.json` and both controls are committed at `6631401` and unmodified in the
  working tree, so their line numbers are stable; the S069 manifest, the knowledge entry,
  `controls/census-invocation-error.txt` and `.ufo/scratch/` are **uncommitted working-tree bytes**, and a
  sibling may change them between this read and landing. Re-verify each pointer at the landing revision.
- I did not run any lane gate, the round-43 suite, `source-recheck.py`, `capture-binding-check.py` or
  `r43-closure.sh`; M44-6's "the check passes today" is inferred from the check's own documented rules
  (`capture-binding-check.py:113-123`) and the absent fields, not from a run — read it as
  `[INFERENCE: rule text + absent fields]`, not as an executed receipt.
- I ran the census twice (lane root → exit 2; fleet root → exit 0) because M44-5 turns on whether the
  recorded stdout reproduces; both runs are read-only and neither writes the lane.
- Rows are drafted for the lesson file; the L1 owns whether they land, and the lesson's R6 append form
  (end-of-file append, no in-place edit) governs how.

## 7. Touched surfaces, gates, tooling, artifacts

- wrote: this file only. Scratch `$HYAKU_SCRATCH/kasegi-r44/R44Scribe4/` was created (default root
  `/fast/scratch/hyaku`, 547 GB free at start) and is removed on exit; no failure to report.
- did not touch: lane git/jj/index, any commit, `PROVINCE.md`, `corpus/**`, `.ufo/waves/round-44/controls/`,
  the fleet repo, sibling repos, `~/.local/bin`, operator config.
- gates run: none. Tool installs: none (no pacman, no network).
- artifact: `.ufo/waves/round-44/wave1/R44Scribe4.md` (this report).
