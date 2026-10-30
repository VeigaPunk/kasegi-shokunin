# R48Review15 — round-48 source Gate critique (S077)

Seat: R48Review15 (scribe, leaf, no subagent dispatch). Axis: depth:verifiability. Lane root: /home/vgpnk/Projects/shokunin/kasegi-shokunin. Claim frozen: `.ufo/waves/round-48/claims.json` (C1 routed-defect-closure, predicate = form only).

## Verdict

- **Admit the form repair** (S077 for the canonical SHONEN.md form only): admitted by the lesson and the row, and the source evidence reproduces. The frozen counter reproduces its committed "after" state.
- **Reject promotion inference**: the lesson and the S077 row both say so. This critique does not supply promotion evidence and does not change any `[x]`/`[ ]` status.
- **Quote local-path/date**: resolves. Quote is at most 25 words, but the lesson's stated word count is wrong (see D1).

Three defects are reported, not fixed (counter bytes and predicate are frozen). They are routed in §Defects.

## 1. S077 source gate checks

| Check | Command (run from /home/vgpnk/Projects/shokunin) | Expected | Observed |
|---|---|---|---|
| Local path exists | `test -e /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md` | exists | exists |
| Snapshot is byte-identical to the path | `sha256sum <kimi PROTOCOL.md> <lane controls/protocol-source.txt>` | equal | both `622b29a043046f0b3b3c7a2240fe62ab516898922885685dd8d89f50b1739fd0` |
| Date | S077 row + lesson `Opened 2026-10-30`; freeze.txt `frozen-at: 2026-10-30T14:30:48.968093Z` | 2026-10-30 | consistent |
| Quote location | `grep -n 'marks are confined to the box character plus one indented evidence line per box' controls/protocol-source.txt` | one hit, File contract row | one hit, line 446 (`SHONEN.md` row) |
| Quote word count | `grep -o '“[^”]*”' corpus/lessons/round-48.md \| wc -w` per quote | ≤25; lesson states "16 words" | **14 words** (≤25 holds; stated 16 is wrong) |
| Canonical seed matches protocol | `sed -n` seed block from protocol-source.txt vs live SHONEN.md | four boxes, verbatim with `<name>`=`kasegi-shokunin` | matches (box text, blank lines, preamble) |
| Claim sha | `sha256sum .ufo/waves/round-48/claims.json` | pinned in freeze.txt `claims-sha256: b8022cdf…` | `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345` (match) |
| Git anchor | `git log -1 -- corpus/instruments/shonen-form.py` | freeze commit | `3546f70 round-48: freeze canonical checklist restoration and controls` |
| Checker predates freeze | `stat` mtimes | checker ≤ freeze | checker 14:30:19Z < freeze 14:30:48Z (local -03 shown as 11:30) |
| Rule cited exists | `grep -n R55 corpus/QUALITY.md` | present | `QUALITY.md:407` present |
| Before-state archive | `wc -l controls/shonen-before.txt`; `sha256sum` | 356 lines, `596122c0…` (claim) | 356 lines; `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` |
| R1/R2 routes | `corpus/lessons/round-47-verifier-spotcheck.md` §6 | R1 SHONEN drift; R2 plain-target phrasing | both present. R1 "356-line" figure matches §1 above. R2 count not re-run (out of this critique's scope). |

## 2. Frozen counter probes (author-side form only)

Read-only runs, cwd /fast/scratch/hyaku/kasegi-r48/R48Review15 (scratch). Checker: `corpus/instruments/shonen-form.py` (read-only; `--root` = lane root).

| # | Input | Command | Expected | Observed |
|---|---|---|---|---|
| P1 | live SHONEN.md (after) | `python3 corpus/instruments/shonen-form.py --root <lane>` | canonical=1 SF-CLEAN exit 0 | **canonical=1 finding=SF-CLEAN exit=0** |
| P2 | controls/shonen-before.txt (before) | `… --root <lane> --file <before>` | canonical=0 SF-PREAMBLE exit 1 | **canonical=0 finding=SF-PREAMBLE exit=1** |
| P3 | live with box-1 `[~]`→`[x]` | `… --file f2_xmark.md` | SF-VERIFIER exit 1 | **SF-VERIFIER exit=1** |
| P4 | live + hidden checklist in `<!-- -->` after box 4 | `… --file f3_trailing.md` | SF-TRAILING exit 1 | **SF-TRAILING exit=1** |
| P5 | live, box-3 `[~]`→`[ ]`, evidence line kept | `… --file f4_unchecked_with_pointer.md` | exit 1 if strict grammar | **SF-CLEAN exit=0** — see D2 |
| P6 | live, evidence pointer `../../etc/passwd` | `… --file f5_badpointer.md` | SF-POINTER exit 1 | **SF-POINTER exit=1** |
| P7 | live with CRLF endings | `… --file f6_crlf.md` | SF-NEWLINE exit 1 | **SF-NEWLINE exit=1** |

P1–P2 reproduce the frozen claim's `after`/`expect_before` exactly. P3–P4 and P6–P7 agree with the kill rule: no hidden, commented, or duplicate checklist passed; x-marks are rejected. Counter bytes were not modified and nothing was written into the lane.

## 3. Defects (reported, not fixed)

- **D1 — lesson word count.** `corpus/lessons/round-48.md` Gate says the located quote is "(16 words)". Mechanical count is 14 (`marks are confined to the box character plus one indented evidence line per box`). Still ≤25, so the admission holds; the stated count is wrong. Correction must be an appended lesson entry, not an in-place rewrite. Expected 16, observed 14.
- **D2 — checker accepts an unchecked box carrying an evidence line (P5).** Protocol File-contract grammar allows only `[x] <verifier-id>` or `[~]` with a resolvable pointer per box. `[ ]` with an evidence pointer is not listed. Checker line 49–50 treats `[ ]` with an evidence line as clean. Predicate text is "canonical four-box author-assessment grammar", so this is a grammar-fidelity gap. It is not on the frozen kill rule (hidden/commented/duplicate checklist; archive bytes), so it does not defeat C1 literally. Reported; counter not changed.
- **D3 — pointer existence only (code read, not run).** Lines 40–45 check that the evidence token is a repo-relative existing file. They do not check that the file supports the box. The claim's `mechanical_limits` already declares this; noted for completeness, not a new defeat.
- Observation (not a defeat): header line 20 hard-codes `# kasegi-shokunin — Promotion checklist`. Correct for this lane; not portable to other lanes' `<name>`.

## 4. Scope and limits

- Admitted: form repair only. Rejected: promotion inference, semantic evidence verification, bounty task, restored lost sources. No source status, recheck, or used-by cell changed in this critique.
- Milestone asked for 64 distinct probes. This seat is a leaf and ran about 15 distinct commands (P1–P7 plus the §1 checks). The milestone is not met; I did not pad it.
- Tool installs: none. No pacman, no network fetch, no git/jj mutation, no delegation, no background jobs.
- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Review15/` (fixtures copied from lane bytes): removed on exit after the receipts above were recorded here.
- Independent non-author admit/reject sampling for S077 remains outstanding, as the lesson states. This report is authored by a lane seat and is not a promotion verifier.
