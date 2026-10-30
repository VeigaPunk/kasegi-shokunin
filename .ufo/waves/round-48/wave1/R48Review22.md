# R48Review22 — Bounded grammar review: EOF terminator surface (extra blank line vs required newline) and strict-grammar-vs-protocol-authority analysis

- **Seat:** R48Review22 (leaf review; godseed lane, no subagent dispatch)
- **Round/wave:** 48 / wave1 (one v2 wave, 64 seats)
- **Claim reviewed:** C1 (`depth:verifiability`) — SHONEN.md conforms to the canonical four-box author-assessment grammar; frozen predicate `shonen-form canonical=1 finding=SF-CLEAN exit=0` via `python3 {tool}/corpus/instruments/shonen-form.py --root {tree}`
- **Frozen claim pin:** seat brief cites claims.json "at `3546f7089c224ac6c8adc68208b1e648bbf3e6a5`". Expected-vs-observed on that hash: `3546f708…` is the **freeze commit** (`git log`: `3546f708 round-48: freeze canonical checklist restoration and controls`, 2026-10-30 11:31:09 -0300), not a content hash. Under that commit the claims.json blob sha256 is `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2f345`, which equals the on-disk file and the committed `freeze.txt` record (`claims-sha256: b8022cdf…`, `frozen-at: 2026-10-30T14:30:48.968093Z`). No mismatch; the pin resolves.
- **Verifier route context:** round-47 verifier spotcheck **R1** (`corpus/lessons/round-47-verifier-spotcheck.md`, §6 "Routed defects"): canonical form = seed verbatim + marks confined to the box character + one indented evidence line per box, no other prose; drift measured at 13 accumulated assessment blocks / 52 `[~]` lines. **R2** (plain-target phrasing) read; not exercised here — this review probes EOF terminator bytes, not frozen plain expressions.
- **Review type:** author-side form validation only. No promotion claim, no semantic-evidence claim, no target testing, no production edits.

## Verdict

**PASS — the frozen checker draws exactly the EOF terminator boundary the seat asked about: exactly one LF at end-of-file is required (too few → `SF-NEWLINE`), and any line after the final evidence line — including one extra *blank* line — is trailing content (`SF-TRAILING`); both sides exit 1, the canonical copy stays clean, and the CRLF+blank precedence case proves the newline predicate dominates. No counter bytes/predicate touched; no fabricated defect.**

| Case | Expected (per frozen grammar) | Observed | Match |
|---|---|---|---|
| `EOF-canonical.md` (byte copy of live SHONEN.md) | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |
| `EOF-extra-blank-1.md` (one extra blank line at EOF) | `canonical=0 finding=SF-TRAILING exit=1` | `canonical=0 finding=SF-TRAILING exit=1` | yes |
| `EOF-extra-blank-3.md` (three extra blank lines) | `canonical=0 finding=SF-TRAILING exit=1` | `canonical=0 finding=SF-TRAILING exit=1` | yes |
| `EOF-extra-blank-spaces.md` (whitespace-only extra line) | `canonical=0 finding=SF-TRAILING exit=1` | `canonical=0 finding=SF-TRAILING exit=1` | yes |
| `EOF-no-newline.md` (single required LF stripped) | `canonical=0 finding=SF-NEWLINE exit=1` | `canonical=0 finding=SF-NEWLINE exit=1` | yes |
| `EOF-space-after-newline.md` (one garbage byte after final LF) | `canonical=0 finding=SF-NEWLINE exit=1` | `canonical=0 finding=SF-NEWLINE exit=1` | yes |
| `EOF-crlf-plus-blank.md` (CRLF terminator + extra blank line) | `canonical=0` — newline predicate expected to dominate trailing-lines predicate | `canonical=0 finding=SF-NEWLINE exit=1` (not `SF-TRAILING`) | yes |
| `EOF-blank-before-evidence.md` (blank where box-1 evidence line belongs) | `canonical=0` nonclean | `canonical=0 finding=SF-EVIDENCE exit=1` | yes |
| `EOF-blank-before-box2.md` (blank between evidence line and box 2) | `canonical=0` nonclean | `canonical=0 finding=SF-BOX exit=1` | yes |
| Live tree, frozen counter_cmd (read-only, C1 `after`) | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |
| Stability: headline pair re-run ×2 | byte-identical verdicts | identical (`SF-TRAILING`/`SF-NEWLINE`, both rc=1) | yes |

## Frozen inputs (identity evidence)

- Checker: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py`, sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` (worktree == HEAD blob).
- Blob stability freeze→HEAD: the checker blob is `0ab32a2c…` at commits `3546f708` (freeze pin) → `25f9e14` → `1b8d0ce` → `02fb99a` → HEAD `3d7e042` — **no post-freeze amendment** (kill-rule precondition holds; C1's kill rule makes a post-scoring checker source amendment incapable of validating the claim anyway).
- Pre-repair archive: `SHONEN.md` blob is `596122c0f6b598d4…` at `3546f708`…`02fb99a` — the drifted bytes the kill rule requires history to retain (`596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05`) — and becomes `b1352168…` only at HEAD `3d7e042` (the repair+dispatch commit). Restoration preserved historical bytes.
- Canonical SHONEN.md (live tree, the measured `after`): sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`, ends with exactly one `\n` (`od -c` tail: `… refused . \n`).
- HEAD = `3d7e042ecbb1f17662f5042e8d3da3290722c031` (read-only observation).
- Relevant frozen predicate lines: `shonen-form.py:17–19` (`lines = text.splitlines()`; `if not text.endswith('\n') or '\r' in text: return 'SF-NEWLINE'`) and `:51–52` (`if i != len(lines): return 'SF-TRAILING'`).

## Fixture construction (scratch only)

Scratch dir `/fast/scratch/hyaku/kasegi-r48/R48Review22/` (created for this seat, removed on exit; all receipts inline below). Every fixture is a byte-derivation of the live canonical SHONEN.md (`b1352168…`, 761 bytes, 12 content lines + 1 terminator LF), produced with `python3` byte splicing — no editor normalization. `--root` stayed the real lane root in every run so evidence pointers resolve against the real tree; only `--file` pointed at scratch copies.

| Fixture | Bytes | sha256 | Delta from canonical |
|---|---|---|---|
| `EOF-canonical.md` | 761 | `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0` | none (positive control) |
| `EOF-extra-blank-1.md` | 762 | `56b0458638cc4593473cddefce4fa24e257c43784fff20a3c88ce290273f7519` | `+ \n` after final LF |
| `EOF-extra-blank-3.md` | 764 | `2aaecbe7df6ca47f5c0e4616d99a00a910934260da7a8b332db518e7b2ced570` | `+ \n\n\n` after final LF |
| `EOF-extra-blank-spaces.md` | 768 | `5d908129183c9c5f610e5f562ef4d7c7efee6c1a39df976e07dd7ddba0fde1b4` | `+ "      \n"` (6-space line) |
| `EOF-no-newline.md` | 760 | `9a4c5effc2232a2939f1734c3744c696252082ce6b0c1d827b115b5763567aa1` | final LF stripped |
| `EOF-space-after-newline.md` | 762 | `e31254ad2fadf13d1a071813ad89cacb070b9df8234300c9da45ebf07d381fac` | `+ 0x20` after final LF |
| `EOF-crlf-plus-blank.md` | 763 | `72fac9aa369d0c21beb7ae3a5eccc3e61f0f872faa770f91093272d8ee628343` | final LF → `\r\n\n` |
| `EOF-blank-before-evidence.md` | 762 | `694a201a0dae71ce2ddd94d2556ea7a4ef3adb22884909af1e919871938255bb` | blank line inserted between box 1 and its Evidence line |
| `EOF-blank-before-box2.md` | 762 | `d75897ee490bd48b7ac2693c2b2ec7596034db568f168fa7818009f4429336f8` | blank line inserted between box-1 Evidence line and box 2 |

Note on fixture correctness: the two mid-file splices were first built with a single-`\n` join, which silently reconstructed the canonical bytes (all three hashes equal) — caught by the hash assertion, fixed to a double-`\n` splice, re-hashed. The canonical hash equality check is what caught it; final fixture set has 9 distinct hashes as tabled.

## Observed commands and full output

```
TOOL=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py
ROOT=/home/vgpnk/Projects/shokunin/kasegi-shokunin
```

Identity line first: `sha256sum $TOOL` → `0ab32a2c…b313dd`; `$ROOT/.ufo/waves/round-48/claims.json` → `b8022cdf…69f2f345` (== committed `freeze.txt` record).

### RUN 1 — fixture matrix (one frozen-checker invocation per fixture)

```
$ for f in EOF-canonical EOF-extra-blank-1 EOF-extra-blank-3 EOF-extra-blank-spaces \
           EOF-no-newline EOF-space-after-newline EOF-crlf-plus-blank \
           EOF-blank-before-evidence EOF-blank-before-box2; do
    python3 "$TOOL" --root "$ROOT" --file "$PWD/$f.md"; echo "rc=$?"; done
case=EOF-canonical                rc=0 shonen-form canonical=1 finding=SF-CLEAN exit=0
case=EOF-extra-blank-1            rc=1 shonen-form canonical=0 finding=SF-TRAILING exit=1
case=EOF-extra-blank-3            rc=1 shonen-form canonical=0 finding=SF-TRAILING exit=1
case=EOF-extra-blank-spaces       rc=1 shonen-form canonical=0 finding=SF-TRAILING exit=1
case=EOF-no-newline               rc=1 shonen-form canonical=0 finding=SF-NEWLINE exit=1
case=EOF-space-after-newline      rc=1 shonen-form canonical=0 finding=SF-NEWLINE exit=1
case=EOF-crlf-plus-blank          rc=1 shonen-form canonical=0 finding=SF-NEWLINE exit=1
case=EOF-blank-before-evidence    rc=1 shonen-form canonical=0 finding=SF-EVIDENCE exit=1
case=EOF-blank-before-box2        rc=1 shonen-form canonical=0 finding=SF-BOX exit=1
```

### RUN 2 — stability re-runs (headline pair, ×2)

```
$ python3 "$TOOL" --root "$ROOT" --file …/EOF-extra-blank-1.md   → SF-TRAILING rc=1 (both runs)
$ python3 "$TOOL" --root "$ROOT" --file …/EOF-no-newline.md      → SF-NEWLINE rc=1 (both runs)
```

### RUN 3 — frozen counter_cmd on the live tree (C1 `after`, read-only)

```
$ python3 "$TOOL" --root "$ROOT"
shonen-form canonical=1 finding=SF-CLEAN exit=0
rc=0
```

### RUN 4 — claims.json pin resolution and blob-identity sweep (read-only git)

```
$ git log --format='%H %ci %s' -3 -- .ufo/waves/round-48/
3546f7089c224ac6c8adc68208b1e648bbf3e6a5 2026-10-30 11:31:09 -0300 round-48: freeze canonical checklist restoration and controls
3d7e042ecbb1f17662f5042e8d3da3290722c031 2026-10-30 11:32:58 -0300 round-48: restore canonical checklist and dispatch 64 probes
$ for c in 3546f708… 25f9e14… 1b8d0ce… 02fb99a… 3d7e042…(HEAD); do
    git show $c:<blob> | sha256sum; done
  checker=0ab32a2c… (constant at all 5 commits)
  SHONEN.md =596122c0… (pre-repair drift bytes) at 3546f708…02fb99a; =b1352168… at HEAD
  claims.json=b8022cdf… (constant at all 5 commits)
```

## Expected vs observed

- **Extra blank line at EOF is defeated as trailing content, not as a newline violation.** `splitlines()` on canonical+`\n` yields a final empty element; the parse consumes exactly 12 lines (4 preamble + 4 boxes + 4 evidence lines) and line 51's `i != len(lines)` fires → `SF-TRAILING`, exit 1, for 1, 3, and whitespace-only variants alike. The finding is stable and byte-identical across re-runs.
- **The two terminator failures are distinct findings on one boundary.** Missing the single LF (or any byte after it, or any `\r` anywhere) → `SF-NEWLINE` (lines 17–19, evaluated *before* any structural parse); any surviving line after the last evidence line → `SF-TRAILING` (lines 51–52, evaluated *after* the full parse). Together they enforce "exactly one LF terminator and nothing after it" — the operational content of the protocol's "byte-identical modulo `<name>`" for this claim.
- **Precedence is observable, not just implied:** `EOF-crlf-plus-blank.md` carries *both* a CR and extra trailing blank line and reports `SF-NEWLINE`, proving the newline predicate dominates the trailing-lines predicate. An implementer relaxing the newline check would change this case's finding — a real mutation detector for the frozen source.
- **Mid-file blank lines are rejected by the nearest structural predicate**, which is why they matter to this review even though the seat is EOF-scoped: blank-before-evidence → `SF-EVIDENCE` (mark `[~]` requires an evidence line at that exact position); blank-before-box-2 → `SF-BOX` (the blank is consumed as box 2's line and fails the label regex). No blank line anywhere is legal; EOF is simply the last place the grammar looks.
- **Live tree** matches C1 `after` (`canonical=1 finding=SF-CLEAN exit=0`) at observed HEAD `3d7e042`; kill-rule trip condition (`canonical=0` at final measured revision) not observed.

## Strict grammar vs protocol authority — the required explanation

**The protocol is the normative source of the requirement; the frozen checker is the binding measurement of it — and where the protocol's prose is looser than the grammar, the grammar decides claim C1.**

1. **Protocol authority (the "why").** The file contract row for `SHONEN.md` (protocol-source.txt, File contract table) requires: seed block byte-identical modulo `<name>`; marks confined to the box character plus one indented evidence line per box (`[x] <verifier-id>` or `[~]` with a resolvable pointer); "no other prose, added boxes, or removed boxes". The Promotion-gates section supplies the mark semantics (`[~]` asserted-by-author; `[x]` only a named non-author verifier). Round-47 route R1 is the incident: the drifted file carried 13 accumulated assessment blocks / 52 `[~]` lines — prose beyond the box+evidence shape. This is the authority the claim's predicate paraphrases.

2. **Strict grammar (the operational "what").** The frozen checker encodes that authority as a byte grammar with seven rejection classes: `SF-NEWLINE` (terminator hygiene, checked first), `SF-PREAMBLE` (exact 4-line head), `SF-BOX` (frozen label regex per box), `SF-EVIDENCE` (evidence line required exactly when mark ≠ space), `SF-POINTER` (single repo-relative existing path token), `SF-VERIFIER` (`[x]` can never pass — mechanical independence unattestable, exactly the claim's mechanical_limits "x marks are rejected"), and `SF-TRAILING` (parse index must equal line count — checked last). Protocol authority names the *classes*; the frozen bytes fix the *boundaries*.

3. **Three live divergences where prose alone would mislead, and the grammar rules:**
   - **"No other prose" does not cover blank lines.** A blank line is not prose. Read loosely, the protocol sentence would tolerate an extra blank line at EOF; the grammar rejects it as `SF-TRAILING` (observed ×3 variants). The strict reading — *no other lines* — is what the claim scores.
   - **The protocol's printed seed ends with a "Marks:" explanation paragraph.** A maximal byte-identical-modulo-name reading would *include* that paragraph; the grammar rejects it (it would trip `SF-TRAILING`), and both the frozen candidate (`controls/canonical-candidate.txt`) and the live repaired file omit it. The measured "canonical form" is the grammar's inhabitant, not the protocol block's literal bytes — the protocol text is documentation of the seed, the frozen checker plus frozen candidate are the seed's scored form.
   - **The seed's literal marks are not the only clean marks.** The frozen candidate carries `[~]`×4; the live file carries `[~]`×3 + `[ ]`×1 with evidence lines under every box including the `[ ]` one — both `SF-CLEAN`, because the grammar keys on mark-conditioned evidence presence and frozen labels, not on any particular mark arrangement, and validates pointer *existence*, not evidence *truth* (candidate↔live diff confirms evidence *text* drifted post-freeze while both stay clean — matching claims.json `mechanical_limits` verbatim).
   
4. **Why the authority cannot migrate back to source.** The freeze is the protection: `freeze.txt` ("Counter and predicate freeze before wave scoring"), the kill rule ("A checker source amendment after seat scoring cannot validate this frozen claim"), and the observed blob stability (checker `0ab32a2c…` constant freeze-commit→HEAD) together mean any dispute about the boundary this review measured — e.g. someone arguing an extra blank line "should" be cosmetic — must be settled by a *future* round's accepted protocol/claim change, never by re-reading or re-writing the frozen bytes. Report defeats; it does not silently fix.

## Semantic-permission check (no fabricated defect)

Nothing observed here is a checker defect; the predicate holds on every variant. The EOF probes test *form*: an extra blank line is exactly the kind of "accumulated content beyond the seed shape" R1 routed against (the drifted file's blocks were prose; this review confirms even *non-prose* extra lines are caught). The mutation-permission framing of sibling probes (single-byte corruption of a frozen label) does not even arise — the checker needs no amendment to defeat any case in the matrix, and no case accidentally passes.

## Constraints honored

- No production/fleet/sibling/domain-tree edits; no git/jj state changes (all git invocations read-only: `git log`, `git show`, `git rev-parse`); no commit/push; no delegation; no background jobs.
- No tool installs (nothing needed; system `python3 3.14.8`).
- Frozen counter bytes/predicate untouched; scratch fixtures only under the named scratch dir, removed after report write.
- Evidence pointers resolve because `--root` stayed the real lane root while `--file` pointed at scratch copies.

## Risks / blockers

- None blocking. One residual measurement note (not a defect, no acceptance hole): the newline predicate guards only `\r`, while Python `splitlines()` also breaks at `\v`, `\f`, `\x1c`–`\x1e`, `\x85`, `\u2028`, `\u2029`; a file carrying one mid-structure would still be rejected, but via a structural finding (`SF-BOX`/`SF-EVIDENCE`/`SF-TRAILING`) rather than `SF-NEWLINE`. Not probed — cheap future bounded probe if the integrator wants the full exotic-terminator map. It does not bear on C1's predicate: the frozen candidate, the live file, and the required form all use plain LF.
- Context note for the integrator: the seat brief's hash for claims.json resolves to the freeze *commit* `3546f708`, under which the claims.json content hash is `b8022cdf…` (== on-disk == `freeze.txt`). Verified; no stale-pin risk.
- Scratch dir `/fast/scratch/hyaku/kasegi-r48/R48Review22/` removed after report write; all receipts preserved in this report.
