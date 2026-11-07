# CriticHarm — round 97 harm audit (base b06af5e -> C1 75a4718 -> C2 a9a5360)

Seat: leaf critic, no subagents. Scratch `/fast/scratch/hyaku/kasegi-r97/CriticHarm`
(base and tip trees via `git archive`, a 137-file fixture repo, probe files); removed on exit.
Read-only on the lane's git state: only `rev-parse`, `show`, `diff`, `ls-tree`, `cat-file`, `archive`.
No tool installed or upgraded this seat (nothing needed).

## HARM lines

**NO HARM — item 1 (governance/density guard).** `SKILL.md` blob `27f23a93848be29b76992ac35ce423ab9a23c269`
at base and tip (identical); `PROVINCE.md` `33458d01…`, `SHONEN.md` `8c91054f…`, `AGENTS.md` `2996452…`
identical base->tip. `density.py` on both copies: mean dens **273.2**, **932** path-citation instances,
**38** blocks, byte-identical output. The C1 and C2 commits touch no governance file (C1: 16
`corpus/knowledge/*.md`; C2: `SCORECARD.md` + `capture-secret-scan.py`).

**NO HARM — item 2 (knowledge citations).** C1 (`75a4718`) changes exactly 16 `corpus/knowledge/*.md`
files, 30 insertions / 30 deletions. Independent audit: 33 map rows on 30 changed lines, 33 exact
sites, 30 lines with an exact token delta (`-key`xN / `+label`xN), **0 failures**; every other
`corpus/knowledge/*.md` byte-identical; no line added or removed; **0** changed lines inside a fenced
code block or a blockquote. `resolve.py` meter (each revision's own `resolve.py`, `corpus/knowledge`
scope, distinct tokens classified against the extracted tree): **base 1040/2041 -> tip 1043/2035**,
reproducing the frozen numbers; **LOST_RESOLUTION=0** (no token non-GONE at base is GONE at tip);
9 tokens removed all GONE, 3 tokens added all INTERNAL; all nine qualified paths exist at tip and
classify INTERNAL, all nine bare basenames classify GONE. The one edit inside quotation marks
(`first-psirt-maturity-document.md:68` quoting the preamble at `:11`) moved together with its
referent, so the quotation still matches what it quotes.

**NO HARM — item 3 (C2 cannot mask an earlier shape).** C2 (`a9a5360`) changes 2 files, 4 hunks in
`capture-secret-scan.py`: two docstring hunks, **+10** `GITLAB_PATTERNS` entries (0 modified, 0
removed), **+20** selftest cases. No change to `ALLOWED_VALUES`, `NEVER_ALLOWED`, `scan_bytes`,
`report`, `is_capture_path`, `_GL_LB`, `_GL_PREFIX`, `_GJ_VER`, `_GJ_ROUTABLE`. Case lists: base 117
cases (64 pos / 53 neg) are a strict subset of tip 137 (74 / 63), **0** shared cases changed,
**0** base-only. Same 137-plant fixture repo through both scanners (`--rev HEAD`): base **69**
(path, shape) pairs, tip **79**; **MASKED (base-only) = 0**, NEW (tip-only) = 10, one per new shape
on its own plant. Ten adversarial overlap/boundary probes: no probe file reports a shape at base and
none at tip; the tip-only firings are the 50-char `glagent-` form with an upper-case version tail
(base reported nothing there) and the deploy-token URL form. Selftest arithmetic reproduces the claim:
117 cases + 8 scope paths + 3 allow checks = **128**; 137 + 8 + 3 = **148**.

**NO HARM — item 4 (allowlist unchanged, landed run clean).** `capture-secret-allow.tsv` blob
`b5b97c6873de366ebd2966fb56e61eec475450e7` at base, C1 and tip (identical, 25 rows, 0 duplicate
keys). Landed scanner `--rev a9a53608dce6aea07d298bb9d5133532078eb1dd`: rc=0, scanned=3018,
hits=0, files=0, allowed=27, unused_allow=0. The round-96 scanner over the same revision returns the
same line (rc=0, hits=0, allowed=27, unused_allow=0), so the C2 change adds no hit on the tree and
disturbs no allow row. The 27 allowed matches come from 25 distinct keys (two keys match twice inside
their own file: `gone.json` credential, `06-github-firstparty-examples.txt` github-refresh-token) —
pre-existing accounting, identical at base.

## Routed defects

None. Nothing in this audit re-scores C1 or C2: the C1 meter reading is re-derived exactly
(1040/2041 -> 1043/2035) and the C2 masking property is re-derived as 0 masked pairs.

## Non-re-scoring observations

- `resolve.py`'s full-tree `main()` does not finish inside a 300 s job cap on this host: the only
  token whose `classify` exceeds 2 s is the recursive glob `~/Projects/**`, and it is the same single
  slow token at base and tip (`same_slow_set=True`). Pre-existing, not caused by either landing; the
  claim's scope (`corpus/knowledge`, what `knowledge-meter.py` measures) completes in 1.2 s.
- The nine bare basenames still appear outside `corpus/knowledge` (4-48 files each), which is why the
  full-scope distinct-token count is 7899 at both revisions while the knowledge scope drops 6.
- Exact-50 `glagent-`: a 51-character tail is not detected at either revision (the rule is exactly 50
  per S140 line 213). A boundary, not a regression.

## Verdict

NO HARM on all four items: the C1 landing qualifies 33 citation rows without touching a line it did
not label, without losing a single resolution, and with the frozen meter reading reproduced; the C2
landing adds ten shapes purely additively, masks none of the earlier shapes, leaves the allowlist
byte-identical and scans the landing revision clean. No routed defect; no claim is re-scored.

## Receipts

All under `.ufo/waves/round-97/w1/CriticHarm-receipts/` (command + observed output; 221 lines total; the four audit scripts are archived in `audit-scripts/`).

| file | command | observed |
|---|---|---|
| `01-governance-blobs-and-density.txt` | `git rev-parse <rev>:<f>` x4; `density.py <rev>/SKILL.md` x2 | 4 blobs identical base/tip; mean dens 273.2, 932 cites, 38 blocks both |
| `02-c1-line-audit.txt` | `python3 -B check2-lines.py base tip repair-map.tsv`; `git show --stat 75a4718` | files_touched=16 map_rows=33 changed_lines=30 exact_sites=33 token_delta_ok=30 FAILURES=0, rc=0; 16 files, 30/30 |
| `03-c1-meter-base-tip.txt` | `python3 -B check2-meter.py base tip` | BASE 1040/2041 TIP 1043/2035; LOST=0 GAINED=0; 9 removed all GONE, 3 added all INTERNAL; rc=0 |
| `04-c2-change-surface.txt` | `git show --name-only a9a5360`; hunk count; `GITLAB_PATTERNS` diff; scan-logic grep; case extractor | 2 files, 4 hunks, +10 patterns / 0 modified; no scan-logic line changed (grep rc=1); cases 117 -> 137, shared=117 changed=[] base_only=[] |
| `05-c2-sample-diff.txt` | fixture `git init` + toplevel assert; both scanners `--rev HEAD`; pair diff | base 69 pairs, tip 79; MASKED=0; NEW=10 (one per new shape) |
| `06-c2-overlap-probe.txt` | both scanners `--files` over 10 probe files | base 1 hit; tip 4 hits, all tip-only; no base-only hit |
| `07-allowlist-and-clean-run.txt` | allowlist blob x3; row/dup count; landed `--rev a9a5360`; base scanner same rev; allow accounting | blob identical x3; rows=25 dup=0; both runs rc=0 scanned=3018 hits=0 allowed=27 unused_allow=0; 27 matches / 25 keys, 0 non-allowed |
| `08-c1-changed-line-context.txt` | fence/blockquote context of every changed line | changed_lines=30 inside_fence=0 inside_blockquote=0 |
| `09-instrument-scope-note.txt` | per-token classify with 2 s alarm; bare-basename grep outside knowledge | both revs: only `~/Projects/**` >2 s; 4-48 files per basename outside knowledge |
| `10-quote-faithfulness.txt` | referent `:11` vs quotation `:68`, base and tip | both qualified together; quotation still matches its referent |
| `11-self-scan.txt` | landed scanner `--files` over this report and its receipts | scanned=12 hits=0 files=0 allowed=0 unused_allow=25 rc=0 (seat artifacts add no credential-shaped hit) |
| `12-self-scan-with-scripts.txt` | archive `check2-lines.py check2-meter.py extract-cases.py build-sample.py`; rescan report + receipts + scripts | scanned=17 hits=0 files=0 allowed=0 unused_allow=25 rc=0 |
