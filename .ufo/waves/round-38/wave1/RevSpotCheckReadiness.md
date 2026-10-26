# RevSpotCheckReadiness — round-38 non-author spot-check readiness contract

Seat `RevSpotCheckReadiness` (leaf reviewer; no subagent dispatch). Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` — read-only for this seat except this receipt.
Item: compile the non-author spot-check readiness contract for round 38 — **receipt only**; the
contract is the single fenced block under `## DELIVERABLE` below (no separate deliverable file).

## 1. Deliverable

| artifact | lines | bytes | sha256 |
|---|---:|---:|---|
| the `## DELIVERABLE` block below (the contract) | 421 | 28056 | `a2abfc284e4cdafa57af8dbdfcf49bfe73a8c2f6a123ac092ae3e64b4c9a2ff9` |

The block's bytes are exactly the file drafted at
`/fast/scratch/hyaku/kasegi-r38/RevSpotCheckReadiness/contract.md` (scratch removed before yield;
the digest above is computed from those bytes and re-verified against the embedded block after
writing — see §7).

## 2. Inputs and method

- Frozen claims `.ufo/waves/round-38/claims.json` (C1 G1-G8 predicate, C2 predicate, kill rules,
  counting commands, judged_head_rule) — authoritative; read, not edited.
- Before-controls: `c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt`.
- Method precedent: `corpus/lessons/round-37-verifier-spotcheck.md` (`git archive` + plain
  grep/awk/wc/sha256sum/python3 over committed bytes; no `corpus/instruments/*` executed; the fleet
  census script run).
- Round-38 wave1 deliverable bytes (the seats' byte-exact deliverables in
  `.ufo/waves/round-38/wave1/`) and the check semantics read from the landed
  `corpus/instruments/r38-closure.sh` (sha256 `85d33ea9d386926e88f9818bbdae5c49ef9cf951363ea09de641cb22a26979a6`,
  1473 lines / 61159 B — byte-identical to the delivered `wave1/ExecSuiteBuild.r38-closure.sh`).

## 3. Validation evidence (this seat's runs)

Observation window 2026-10-26T18:2x-18:4xZ against lane HEAD
`700153593eb586c70a6499c8ca225ee4d673bc9b` while the L1's integration was landing the round-38 bytes
in the worktree (9 modified files plus the entry/capture/manifest/suite/declared-blocks/junk files
untracked; SHONEN.md, LOG.md, `corpus/lessons/round-38.md`, `corpus/instruments/r38-fixtures/`,
`final-gates/all-gates.txt` and the J/Y commits still pending at last read). Every contract
expectation that could be checked against landed bytes was checked (✓ in the contract); the rest
(◇) are pinned by the frozen claims plus the delivered bytes.

Landed-byte battery (all outputs as the contract expects):

- C2 counters: frontier F-rows 21; F21 row 1 (NF 8); registry 55; S055 row 1 (NF 13); entries citing
  `^source: S055` 1; knowledge files 50; `knowledge-expected.txt` carries the entry (1).
- Capture/manifest: capture sha256 `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42`
  (5146 lines / 272441 B); manifest sha256 `95b3f46d9c502573f299ed565325a0db27009c2a5eb50205c1ca27b3556f9a9f`
  (3841 B); manifest-bound True (lines 5146, snapshot_bytes 272441, raw_sha256 `fad0c60d…`); Q1-Q4 at
  anchors 2135 / 2844 / 2151-2152 / 1767 with occurrences 1 each; entry 137 lines with
  `source:` / `verified-at: 2026-10-26` / `ground: F21` / cd-prefixed `recheck:` lines 1 each;
  located quotes pairs=65 missing=0 over25=0.
- Junk twin: the four fabricated sentences 0 hits each in the capture; the committed rejection
  record `c2-controls/junk-f21-recheck.txt` = 4 `MISMATCH reason=quote-not-found` + `exit=1`.
- G1: declared-blocks.txt = `corpus/README.md 32 f0318ac8…` + `PROVINCE.md 4 797666b9…`; both verify
  OK (`tail -n <n> | sha256sum`); `ExecDeclaredBlocks.gen.sh check` -> `declared=2 ok=2 fail=0 base=0 exit=0`;
  fence walks PROVINCE closed / README closed (base contrast: PROVINCE closed, README open — opener
  L426); `Correction (round 38)` lines 1 each naming `L79-L152` / `L399-L454` + `misplaced`;
  `[r38 Frontier amendment` line 1; `## Round-38 admission` heading 1.
- G3: resolutions section 1; row tokens L10/L90/L95/L216/L265/L300/L320/L85 = 1 each; added-line
  token scan (base..worktree with the claims' exclusions) all 0 — `⟨pending` `<fill>`
  `filled by the L1` `<LANE_HASH>` `<r38-` and word-bounded TBD/TODO.
- G7: R31 heading at ledger :37, filled heading at :45 (order ok), Correction line 1,
  proposal-rows=7.
- G5 (partial): the Correction line landed at SCORECARD.md:1511 with `f3246559` +
  `anchor ancestor`; the round-38 section not yet landed at read time (fin/head-token scans vacuous
  0); the delivered section bytes are clean (0 `Final lane commit:`, 0 head-token matches,
  reference phrase 1).
- G2 carrier: head-token regex 0 on the delivered SCORECARD section and on the delivered SHONEN
  block's round-38 lines; reference phrase 1 (section) / 2 (SHONEN block).
- QUALITY R32/R33 rows 1 each; SKILL.md `r38-closure.sh` registry row 1.
- r37 receipt greps: `all-gates v1`; `export-ref=9492c776…`; `suite-sha256=0da98e37…`; 14 closed
  E-lines; `closed=14/14 exit=0`; `selftest cases=14 failures=0`; r37 suite blob digest `0da98e37…`
  (unchanged); the r37 receipt exists at 9492c776, aa88877b and 2387dcf6 (the r37 suite's E10 had no
  diff-clean limb, so the r37 receipt could grade a ref whose tree contained it; the r38 G2
  diff-clean limb forces the J/Y split — finding 2).
- Red transcripts: `ExecBaseRed.base-red-transcript.txt` `eee9569c…` (254 lines / 13733 B);
  `ExecR37HeadRed.transcript.txt` `a6cbf185…` (881 lines / 51578 B) — digests match the seats' own
  receipts.
- Base-red corroboration: the delivered suite bytes run over the base export printed
  `closed=0/8 exit=1` with G1-G8 all red — G1 `province-correction=0,readme-correction=0,province-fence=closed,readme-fence=open,declared-blocks=0,declared-ok=0`;
  G2 `receipt=0,…`; G3 `resolutions-section=0,…`; G4 `dispatches=0,…`; G5 `round38-section=0,…`;
  G6 `r36=absent,r37=absent,r38=present,work=inside,tolerated=none,read=ok`; G7
  `filled-section=0,…`; G8 `r37-suite=1,r37-closed=0,r37-exit=1`.
- numstat (base..worktree, excl `.ufo`): 9 modified files all x/0 (PROVINCE 4, SCORECARD 2, SKILL 1,
  QUALITY 14, README 32, SOURCES 4, knowledge-expected 1, ledger 24, round-37 15); violations 0;
  renames 0; protected-ten check 0. `ExecFenceWalk.sh --selftest` -> `cases=10 failures=0`.
- Dispatch: `taskCall.tasks` = 73 (the G4 seat-count expectation).

## 4. Findings for the L1

1. **Correction-line placement (resolved by the landed order — keep it).** The delivered
   `ScribeScorecard.correction.md` contains the quoted phrase `Final lane commit:` and 40-hex tokens
   on one line. The suite's G5 `fin` limb (`grep -cF 'Final lane commit:'` over the round-38
   section) and G2 head-token limb
   (`(final (lane )?(head|commit)|judged head)[^|]*[0-9a-f]{7,40}` over the section plus SHONEN's
   round-38 lines) would both red if the line landed inside the round-38 section. The L1 landed it
   BEFORE the `## Round 38 result` heading (SCORECARD.md:1511), where both section-scoped scans do
   not see it — verified. Residual: any re-order that moves the line inside the section re-opens
   G5/G2; the contract's §5 D-D commands pin the expected 0s.
2. **K1 — the frozen green ref is the receipt-bearing tip (encode; do not kill on the literal
   reading).** `CritC1Kill.md` §2 (S1) proves `--export-ref <J>` cannot print `closed=8/8`: a J
   export lacks the receipt G2 requires, so an honest suite prints `closed=7/8 exit=1` there. The
   satisfiable green ref is Y with the receipt's `export-ref=J` and `git diff --name-only J Y` = the
   receipt only. The contract's §0 verifies the pair (including `git cat-file -e "$J:$R"` -> absent)
   and §6 verifies the receipt's limbs; the judge does not run the suite. The report should state
   the pair (export-ref=J, run-ref=Y) per K1's smallest safe correction.
3. **G6 mid-wave -> filing expectation.** Live at compile time: kasegi-r36 = 0, kasegi-r37 = 0 (the
   r37 `build-spec.py` leftover already removed), kasegi-r38 = 135911 entries (seats running). The
   kill rule requires 0 for all three at filing; every seat removes its own scratch before yielding
   (this seat does — §6).
4. **fetched_bytes variance across tools (cosmetic).** The manifest records fetched_bytes=414858
   (curl size_download at 18:25:51Z); ExecCsafStatus's capture-source runs recorded 415225. The
   snapshot bytes and digest are stable (272441 / `63c8ad52…` across 4 independent fetches). The
   contract pins the snapshot digest + manifest fields, not fetched_bytes.
5. **Fence-walk heuristic vs walk (base-state contrast).** ExecBaseRed's table used odd-count parity
   ("PROVINCE.md fences L81/L96/L124 (odd -> open_at_eof=1)") while the claims'/suite's CommonMark
   walk says PROVINCE closed at base (ExecR37HeadRed §3 G1 row; verified by this seat's walk). The
   contract's command is the walk; the base-red's G1 red does not depend on the fence limb
   (corrections 0 + declared-blocks absent already red it).
6. **Suite limits the judge strengthens around** (from the suite's own documented limits +
   CritC1Kill): G4 compares counts, never seat identities (contract §5 D3 adds the name-multiset
   check); G8 does not bind the r37 suite's digest (contract §7 adds the `0da98e37…` blob check);
   the declared-blocks limb is tail-only (contract §5 D-A adds the base-guard/wc check; the suite
   already requires >=1 declaration per front door); G3's added-line scan is lane-scoped (a line
   added and removed inside the range is invisible — inherent to the frozen scope).
7. **Selftest line format.** The landed suite prints the richer
   `selftest case=G<i> positive=... mutants=<ok>/<n> verdict=...`; the contract's §6 gives the
   claims-level grep (8 case lines + summary) and the richer backreference grep (GNU grep) for when
   the richer form is present.

## 5. Tooling

No tool installed, upgraded or removed; no pacman invocation; no network fetch by this seat (all
capture/manifest facts read from the committed/delivered bytes; live-fetch facts quoted from the
ExecC2Capture / ExecCsafStatus / ExecC2QuoteOnce receipts). python3 3.14.8, GNU bash 5.3.20(1),
coreutils 9.12 preexisting (the baseline CritC1Kill recorded). No mutating git/jj command was run;
all git use was read-only (`status/log/ls-tree/cat-file/diff/rev-parse/merge-base`) with
`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## 6. Scratch

`/fast/scratch/hyaku/kasegi-r38/RevSpotCheckReadiness/` (sim/, w-base/, contract.md, the assembly
parts) is removed before this seat yields (G6/D-E); the receipt and the embedded contract are
already in the wave dir.

## 7. Self-verification of the embedded block

After writing this receipt, the block between the ```` markers was extracted and hashed; it must
equal `a2abfc284e4cdafa57af8dbdfcf49bfe73a8c2f6a123ac092ae3e64b4c9a2ff9` (421 lines / 28056 bytes).
Result: recorded in the yield message.

## DELIVERABLE

````
# Round-38 spot-check readiness contract — non-author judge (kasegi)

Compiled 2026-10-26 by seat RevSpotCheckReadiness from the frozen claims
(`.ufo/waves/round-38/claims.json`, authoritative), the before-controls
(`.ufo/waves/round-38/c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt`), the
round-37 method precedent (`corpus/lessons/round-37-verifier-spotcheck.md`: `git archive` + plain
grep/awk/wc/sha256sum/python3 over committed bytes; no `corpus/instruments/*` executed), and the
round-38 wave1 deliverable bytes. Marking: ✓ = re-derived against the landed round-38 bytes at
compile time; ◇ = pinned by the frozen claims plus the delivered bytes (the L1 lands deliverables
byte-exact; the landed prefix already matched everywhere it could be checked).

Setup — the judge exports the tip and reads only committed bytes:

    LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
    S=<judge's own scratch dir>              # created and removed by the judge
    Y=$(git -C "$LANE" rev-parse HEAD)       # lane tip at closure; the report names J and Y
    E="$S/export"; mkdir -p "$E" && git -C "$LANE" archive "$Y" | tar -x -C "$E"
    R=.ufo/waves/round-38/final-gates/all-gates.txt

Ref-scoped checks (ancestry, diffs, numstat, added-line scan) run `git -C "$LANE" ...` against the
lane repo; every byte check reads under `$E` — run the python3 snippets with cwd `$E` (their paths
are export-relative). No `corpus/instruments/*` file is executed (§10).

## 0. Heads and receipt identity (D-B foundation)

    sed -n '1p' "$E/$R"                                          # -> all-gates v2
    grep -cE '^export-ref=[0-9a-f]{40}$' "$E/$R"                 # -> 1
    J=$(sed -n 's/^export-ref=//p' "$E/$R" | head -n1)
    git -C "$LANE" cat-file -e "$J^{commit}"                     # -> exit 0
    git -C "$LANE" merge-base --is-ancestor "$J" "$Y"            # -> exit 0
    git -C "$LANE" diff --name-only "$J" "$Y"                    # -> exactly one line:
                                                                 #    .ufo/waves/round-38/final-gates/all-gates.txt
    git -C "$LANE" cat-file -e "$J:$R"                           # -> exit 1 (absent: J carries every
                                                                 #    round-38 change EXCEPT the receipt)
    grep -cE '^suite-sha256=[0-9a-f]{64}$' "$E/$R"               # -> 1
    git -C "$LANE" cat-file blob "$Y:corpus/instruments/r38-closure.sh" | sha256sum
                                                                 # -> equals the receipt's suite-sha256 value
                                                                 #    (delivered = landed suite bytes:
                                                                 #    85d33ea9d386926e88f9818bbdae5c49ef9cf951363ea09de641cb22a26979a6,
                                                                 #    1473 lines / 61159 B) ✓
    grep -cE '^run-utc=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$' "$E/$R"
                                                                 # -> 1 if the receipt carries run-utc (the r37
                                                                 #    format did); any value must be >= J's commit
                                                                 #    time; run-utc > Y's commit time is the
                                                                 #    expected shape under the K1 split below

K1 (claim-truth note — do not kill a correct round on the literal reading): the frozen counting
command `bash corpus/instruments/r38-closure.sh --export-ref <J> -> closed=8/8 exit=0` is
unsatisfiable as literally written, because a J export does not contain the receipt that G2 requires
(the claims' own judged_head_rule: "J carries every round-38 change except that receipt; the lane tip
Y adds only the receipt"), so an honest suite prints `closed=7/8 exit=1` there
(`.ufo/waves/round-38/wave1/CritC1Kill.md` §2, severity S1). The satisfiable green ref is the
receipt-bearing tip: `--export-ref "$Y"` with the receipt's `export-ref=J` and
`git diff --name-only J Y` = the receipt only. The judge verifies the pair above plus the receipt's
limbs (§6); the judge does not run the suite (§10).

## 1. S055 capture, manifest, quotes (C2)

    sha256sum "$E/corpus/source-snapshots/round-38/S055.txt"
        # -> 63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42  ✓
    wc -lc < "$E/corpus/source-snapshots/round-38/S055.txt"
        # -> 5146 272441  ✓
    sha256sum "$E/corpus/source-snapshots/round-38/manifest.json"
        # -> 95b3f46d9c502573f299ed565325a0db27009c2a5eb50205c1ca27b3556f9a9f  ✓
    wc -c < "$E/corpus/source-snapshots/round-38/manifest.json"   # -> 3841  ✓

Manifest binding (plain python3; the manifest is the only place the capture's digest is declared):

    python3 - <<'EOF'
    import hashlib, json
    m = json.load(open('corpus/source-snapshots/round-38/manifest.json'))
    s = m['sources'][0]
    sha = hashlib.sha256(open('corpus/source-snapshots/round-38/S055.txt','rb').read()).hexdigest()
    print('manifest-bound:', s['sha256'] == sha, 'lines:', s['lines'], 'snapshot_bytes:', s['snapshot_bytes'], 'raw_sha256:', s['raw_sha256'][:12])
    EOF
        # -> manifest-bound: True lines: 5146 snapshot_bytes: 272441 raw_sha256: fad0c60d5857  ✓

The four pinned quotes at their manifest anchors (Q1/Q2/Q4 sit on one capture line; Q3 spans two —
the sentence splits after "For each item in"):

    sed -n '2135p' "$E/corpus/source-snapshots/round-38/S055.txt" | grep -cF 'The main purpose of the VEX format is to state that and why a certain product is, or is not, affected by a vulnerability.'
        # -> 1  ✓
    sed -n '2844p' "$E/corpus/source-snapshots/round-38/S055.txt" | grep -cF 'For each item in /vulnerabilities it MUST be tested that at least one of the elements fixed, known_affected, known_not_affected, or under_investigation is present in product_status.'
        # -> 1  ✓
    sed -n '2151,2152p' "$E/corpus/source-snapshots/round-38/S055.txt" | tr '\n' ' ' | grep -cF 'For each item in /vulnerabilities[]/product_status/known_not_affected an impact statement SHALL exist as machine readable flag in /vulnerabilities[]/flags or as human readable justification in /vulnerabilities[]/threats.'
        # -> 1  ✓
    sed -n '1767p' "$E/corpus/source-snapshots/round-38/S055.txt" | grep -cF 'vulnerable_code_not_in_execute_path: The affected code is not reachable through the execution of the code, including non-anticipated states of the product.'
        # -> 1  ✓

Once-only (plain; the QuoteOnce limb): normalize the whole capture to one space-joined string and
count each of the four quotes -> 1 each  ✓ (measured: Q1..Q4 occurrences 1/1/1/1).

Optional live re-open (discernment, r37 §3 precedent):
`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html`
-> HTTP 200; the raw body hashed fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b at
the manifest's 2026-10-26T18:25:51Z fetch (reproduced byte-identically 4x by ExecCsafStatus and
ExecC2QuoteOnce). A later fetch may differ (upstream drift): record it; the round's pinned ground is
the committed capture — do not fail C2 on live drift alone.

## 2. Junk twin (C2 negative control)

The four fabricated sentences of `.ufo/waves/round-38/c2-controls/junk-f21.md` (sha256
6742705ec69537cfd949b1a7df506fe8446267c712aaec8b7e714d6cbdaa1630, 23 lines / 983 B) are absent from
the capture:

    grep -cF 'CSAF requires every advisory to carry a CVSS v4.0 score.' "$E/corpus/source-snapshots/round-38/S055.txt"
        # -> 0  ✓
    grep -cF 'The VEX status known_not_affected needs no justification.' "$E/corpus/source-snapshots/round-38/S055.txt"
        # -> 0  ✓
    grep -cF 'CSAF is maintained by FIRST.' "$E/corpus/source-snapshots/round-38/S055.txt"
        # -> 0  ✓
    grep -cF 'CSAF v2.0 mandates SSVC decision points.' "$E/corpus/source-snapshots/round-38/S055.txt"
        # -> 0  ✓

The committed rejection record (the instrument run over a manifest whose four quotes were replaced
by the twin's four claims, capture byte-identical):

    grep -cE 'MISMATCH reason=quote-not-found' "$E/.ufo/waves/round-38/c2-controls/junk-f21-recheck.txt"
        # -> 4  ✓
    grep -cE '^exit=1$' "$E/.ufo/waves/round-38/c2-controls/junk-f21-recheck.txt"
        # -> 1  ✓

The twin is not an entry: `ls "$E/corpus/knowledge/junk-f21.md"` -> absent (exit 2); the twin lives
only under `.ufo/waves/round-38/c2-controls/`; the S055 source line resolves to exactly one
knowledge file (§4).

## 3. Census (C2)

    bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
        # -> kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
        #    kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
        #    kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
        #    exit=0
        # process exit 0; exactly those two W04 rows and no E-row  ✓
        # (byte-shape = census-before.txt; the S055 row adds no warning — ExecC2Census's mirror run
        #  is byte-identical to the before-control)

## 4. C2 counters and instrument receipts

Plain counters:

    grep -cE '^\| F[0-9]+ \|' "$E/corpus/README.md"                            # -> 21  ✓
    grep -cE '^\| F21 \|' "$E/corpus/README.md"                                # -> 1  ✓
    grep -E '^\| F21 \|' "$E/corpus/README.md" | awk -F'|' '{print NF}'        # -> 8 (6 data cells)  ✓
    grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$E/corpus/SOURCES.md"  # -> 55  ✓
    grep -cE '^\|[[:space:]]*S055[[:space:]]*\|' "$E/corpus/SOURCES.md"        # -> 1  ✓
    grep -E '^\|[[:space:]]*S055[[:space:]]*\|' "$E/corpus/SOURCES.md" | awk -F'|' '{print NF}'
                                                                               # -> 13  ✓
    grep -rlE '^source: S055' "$E/corpus/knowledge" | wc -l                    # -> 1  ✓
    ls "$E/corpus/knowledge/"*.md | wc -l                                      # -> 50  ✓
    grep -c 'csaf-vex-product-status-and-justifications' "$E/corpus/instruments/knowledge-expected.txt"
                                                                               # -> 1  ✓ (the audit's expected list synced)

Entry `corpus/knowledge/csaf-vex-product-status-and-justifications.md` (137 lines  ✓): header greps
-> 1 each  ✓:

    grep -cE '^source: S055' "$E/corpus/knowledge/csaf-vex-product-status-and-justifications.md"
    grep -cE '^verified-at: 2026-10-26' "$E/corpus/knowledge/csaf-vex-product-status-and-justifications.md"
    grep -cE '^ground: F21' "$E/corpus/knowledge/csaf-vex-product-status-and-justifications.md"
    grep -cE '^recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055' "$E/corpus/knowledge/csaf-vex-product-status-and-justifications.md"

Located quotes (plain python3 over the entry + capture, the r37 §2 form):

    python3 - <<'EOF'
    import re
    entry = open('corpus/knowledge/csaf-vex-product-status-and-justifications.md', encoding='utf-8').read()
    cap = open('corpus/source-snapshots/round-38/S055.txt', encoding='utf-8').read().split('\n')
    norm = ' '.join(cap)
    pairs = re.findall(r'"([^"\n]+?)"\s*(?:[—–-]+|\()\s*L(\d+)(?:-L(\d+))?\)?', entry)
    missing = [q for q, a, b in pairs
               if not (q in ' '.join(cap[int(a)-1:(int(b) if b else int(a))+1]) or q in norm)]
    over25 = [q for q, _, _ in pairs if len(q.split()) > 25]
    print(f'pairs={len(pairs)} missing={len(missing)} over25={len(over25)}')
    EOF
        # -> pairs=65 missing=0 over25=0  ✓

Instrument outputs are NOT re-run; they are evidence-verified from the committed wave receipts:

    grep -c 'entries=24 pass=24 exit=0' "$E/.ufo/waves/round-38/wave1/ExecC2Harness.md"
        # -> >=1  ✓ (line 74 of the delivered receipt; the mirror delta 23->24 is the F21 binding)
    grep -c 'PASS     F21  knowledge/csaf-vex-product-status-and-justifications.md ids=S055' "$E/.ufo/waves/round-38/wave1/ExecC2Harness.md"
        # -> >=1  ✓
    grep -c 'records=45 bound=45 unbound=0' "$E/.ufo/waves/round-38/wave1/ExecC2Binding.md"
        # -> >=1  ✓ (44/44 at base -> 45/45 with the round-38 manifest)
    grep -c 'expected=50 missing=0 unexpected=0 exit=0' "$E/.ufo/waves/round-38/wave1/ExecC2Audit.md"
        # -> >=1  ✓ (expected list 49 -> 50 with the landed entry)

## 5. D-A..D-F plain greps (C1 checks G1..G7)

D-A (G1) — front doors:

    grep -cE '^Correction \(round 38\)' "$E/PROVINCE.md"                        # -> >=1  ✓ (1 landed)
    grep -E '^Correction \(round 38\)' "$E/PROVINCE.md" | grep -c 'L79-L152'    # -> >=1  ✓
    grep -E '^Correction \(round 38\)' "$E/PROVINCE.md" | grep -cw misplaced    # -> >=1  ✓
    grep -cE '^Correction \(round 38\)' "$E/corpus/README.md"                   # -> >=1  ✓ (1 landed)
    grep -E '^Correction \(round 38\)' "$E/corpus/README.md" | grep -c 'L399-L454'   # -> >=1  ✓
    grep -E '^Correction \(round 38\)' "$E/corpus/README.md" | grep -cw misplaced    # -> >=1  ✓
    grep -c '^\[r38 Frontier amendment' "$E/PROVINCE.md"                        # -> 1  ✓
    grep -c '^## Round-38 admission' "$E/corpus/README.md"                      # -> 1  ✓ (the heading the r37 append lost)

Fence state at EOF (CommonMark walk; the committed walker, selftest cases=10 failures=0  ✓):

    bash "$E/.ufo/waves/round-38/wave1/ExecFenceWalk.sh" "$E/PROVINCE.md"       # -> closed  ✓
    bash "$E/.ufo/waves/round-38/wave1/ExecFenceWalk.sh" "$E/corpus/README.md"  # -> closed  ✓
        # base state for contrast: PROVINCE closed, README open (opener at L426 never closed)  ✓

Declared blocks (the G1 contract; the committed file is authoritative, one `<path> <lines> <sha256>`
line per block):

    cat "$E/.ufo/waves/round-38/declared-blocks.txt"
        # -> corpus/README.md 32 f0318ac8306f52c8085c192ee0c32f8f72dd2f4f5675164294433c9210fbbdff
        #    PROVINCE.md 4 797666b943244f9174b627918f84b9027858a6d4ffe0213c026c568ff1ed3acf  ✓
    while read -r p n sha; do
      case $p in '#'*) continue ;; esac
      [ "$(tail -n "$n" "$E/$p" | sha256sum | awk '{print $1}')" = "$sha" ] && echo "OK $p" || echo "FAIL $p"
    done < "$E/.ufo/waves/round-38/declared-blocks.txt"
        # -> OK corpus/README.md / OK PROVINCE.md; no FAIL line  ✓
    bash "$E/.ufo/waves/round-38/wave1/ExecDeclaredBlocks.gen.sh" check \
      "$E/.ufo/waves/round-38/declared-blocks.txt" --root "$E"
        # -> declared=2 ok=2 fail=0 base=0 exit=0  ✓ (optional cross-check)
    K2 strengthening: any `# base <path> <pre>` guard line must satisfy `wc -l <path>` ==
    pre + lines; both front doors keep >=1 declaration each (the suite requires it).

D-B (G2) — judged head by reference (§0 plus):

    sed -n '/^## Round 38/,$p' "$E/SCORECARD.md" | grep -cF 'judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt'
        # -> >=1  ◇ (the delivered round-38 section carries it once)
    grep -cF 'judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt' "$E/SHONEN.md"
        # -> >=1  ◇ (the delivered round-38 block carries it twice)
    sed -n '/^## Round 38/,$p' "$E/SCORECARD.md" | grep -ciE '(final (lane )?(head|commit)|judged head)[^|]*[0-9a-f]{7,40}'
        # -> 0  ◇ (delivered section: 0)
    grep -E 'round 38|round-38' "$E/SHONEN.md" | grep -ciE '(final (lane )?(head|commit)|judged head)[^|]*[0-9a-f]{7,40}'
        # -> 0  ◇ (delivered block: 0)
    grep -rnF "$J" "$E" --exclude=all-gates.txt | wc -l
        # -> 0  (no lane file names J by hash; the report names J and Y — fleet repo, out of scope)

D-C (G3) — pending markers:

    grep -cF '## Pending-marker resolutions (round 38)' "$E/corpus/lessons/round-37.md"
        # -> 1  ✓
    sec=$(awk '/^## Pending-marker resolutions \(round 38\)/{f=1;next} f && /^## /{exit} f' "$E/corpus/lessons/round-37.md")
    for tok in L10 L90 L95 L216 L265 L300 L320 L85; do
      printf '%s=%s ' "$tok" "$(printf '%s\n' "$sec" | grep '^|' | grep -cE "(^|[^0-9])${tok}([^0-9]|$)")"
    done
        # -> L10=1 L90=1 L95=1 L216=1 L265=1 L300=1 L320=1 L85=1  ✓
    git -C "$LANE" diff --no-color a173b0c2b98c5ae39599fa9be76027fbbead0b9e "$Y" -- . \
      ':!.ufo' ':!corpus/instruments/r38-closure.sh' ':!corpus/instruments/r38-fixtures' \
      | grep '^+' | grep -v '^+++' > "$S/added.txt"
    for tok in '⟨pending' '<fill>' 'filled by the L1' '<LANE_HASH>' '<r38-'; do
      printf '%s:%s ' "$tok" "$(grep -cF -- "$tok" "$S/added.txt")"
    done
        # -> ⟨pending:0 <fill>:0 filled by the L1:0 <LANE_HASH>:0 <r38-:0  ✓
    grep -cE '(^|[^[:alnum:]_])(TBD|TODO)([^[:alnum:]_]|$)' "$S/added.txt"
        # -> 0  ✓
    ls "$E/corpus/lessons/round-38.md"                            # -> present  ◇ (K12: check existence first)
    grep -c '⟨pending' "$E/corpus/lessons/round-38.md"            # -> 0  ◇ (kill rule)

D3 (G4) — closure order:

    git -C "$LANE" ls-tree -r --name-only "$Y" -- .ufo/waves/round-38 | grep -E '-results\.json$'
        # -> >=1 line  ◇ (expect wave1-results.json, the dispatch's sibling)
    python3 - <<'EOF'
    import json
    d = json.load(open('.ufo/waves/round-38/wave1-dispatch.json'))
    r = json.load(open('.ufo/waves/round-38/wave1-results.json'))
    tasks = (d.get('taskCall') or {}).get('tasks') or []
    seats = r.get('results') if isinstance(r.get('results'), list) else None
    print('tasks', len(tasks), 'seats', len(seats) if seats is not None else r.get('seats'))
    EOF
        # -> tasks 73 seats 73  ◇ (dispatch taskCall.tasks = 73, measured at the freeze tip)
    K5 strengthening: the results' seat-name multiset equals the dispatch's task-name multiset
    (python3) -> equal  ◇ (the suite compares counts only — documented limit).

D-D (G5) — label drift:

    sed -n '/^## Round 38/,$p' "$E/SCORECARD.md" | grep -cF 'Final lane commit:'
        # -> 0  ◇
    grep -cE '^Correction \(round 38\)' "$E/SCORECARD.md"                       # -> >=1  ✓ (landed at :1511)
    grep -E '^Correction \(round 38\)' "$E/SCORECARD.md" | grep -c 'f3246559'   # -> >=1  ✓
    grep -E '^Correction \(round 38\)' "$E/SCORECARD.md" | grep -ciE 'anchor[- ]ancestor'  # -> >=1  ✓
    Placement note: the landed Correction line sits BEFORE the `## Round 38 result` heading
    (SCORECARD.md:1511, section below it), so the suite's section-scoped `Final lane commit:` scan
    and head-token scan do not see the line's quoted phrase; keep that order at integration. The
    line's quoted `Final lane commit: f3246559…` hash is truncated (8 hex + ellipsis), so the r37
    suite's E1 40-hex collector does not pick it up, and its full 40-hex sits after
    `Anchor ancestor (r37 wave evidence):` — deduplicated to the same single hash (ExecR37Carry.md
    §5, B2). Do not move the line inside the round-38 section.

D-E (G6) — live scratch quiescence, measured at filing:

    find /fast/scratch/hyaku/kasegi-r36 /fast/scratch/hyaku/kasegi-r37 -mindepth 1 | wc -l
        # -> 0  ✓ (the r37 build-spec.py leftover is already removed)
    find /fast/scratch/hyaku/kasegi-r38 -mindepth 1 | wc -l
        # -> 0  ◇ (kill rule: any leftover entry at filing kills; mid-wave the dir held 135911 seat
        #   entries — every seat removes its own scratch before yielding)

D-F (G7) — ledger fill:

    grep -nF '## Round-37 dispositions (appended 2026-10-26, R31 home)' "$E/corpus/knowledge/considerthese-proposals-ledger.md"
        # -> 37:## Round-37 dispositions (appended 2026-10-26, R31 home)  ✓
    grep -nF '## Round-37 dispositions — filled (round 38)' "$E/corpus/knowledge/considerthese-proposals-ledger.md"
        # -> 45:## Round-37 dispositions — filled (round 38)  ✓ (after the empty heading)
    grep -cE '^Correction \(round 38\)' "$E/corpus/knowledge/considerthese-proposals-ledger.md"
        # -> >=1  ✓
    awk '/## Round-37 dispositions — filled \(round 38\)/{f=1;next} f && /^## /{exit} f && /^\|/ {
           c=$2; gsub(/^[ \t]+|[ \t]+$/,"",c); if (c ~ /^[0-9]+/) { sub(/\..*/,"",c);
           if (c+0>=1 && c+0<=7) seen[c+0]=1 } }
         END { n=0; for (i=1;i<=7;i++) if (seen[i]) n++; print "proposal-rows=" n }' \
      "$E/corpus/knowledge/considerthese-proposals-ledger.md"
        # -> proposal-rows=7  ✓ (each of proposals 1-7 present)

## 6. Suite reds and selftest via the committed all-gates receipt (C1)

The judge does not execute the suite. The receipt is the committed record of the green run; the reds
are re-derived from the two committed transcripts plus the receipt's selftest:

    grep -cE '^G[1-8] payload=.* closed=1$' "$E/$R"               # -> 8  ◇
    grep -E '^G[1-8] payload=.* closed=1$' "$E/$R" | sed -n 's/^\(G[1-8]\) payload=.*/\1/p' | sort -u | wc -l
        # -> 8  ◇ (ids G1..G8 once each)
    grep -cE '^G[1-8] payload=.* closed=0$' "$E/$R"               # -> 0  ◇
    grep -cE '^closed=8/8 exit=0$' "$E/$R"                        # -> 1  ◇
    grep -cE '^selftest case=G[1-8] ' "$E/$R"                     # -> 8  ◇ (unique ids 8)
    grep -cE '^selftest cases=8 failures=0$' "$E/$R"              # -> 1  ◇
    grep -cE '^selftest case=G[1-8] positive=pass mutants=([1-9][0-9]*)/\1 verdict=pass$' "$E/$R"
        # -> 8 when the landed suite's richer selftest form is present  ◇ (GNU grep backreference;
        #   the landed suite prints `selftest case=G<i> positive=... mutants=<ok>/<n> verdict=...`)

Reds without running — the two committed transcripts (digests verified  ✓):

    sha256sum "$E/.ufo/waves/round-38/wave1/ExecBaseRed.base-red-transcript.txt"
        # -> eee9569cb1d91eb7fc5a2bbb6da5d6eac09152c7d472b9ac4e4db6cb4645b51e  ✓ (254 lines / 13733 B)
    sha256sum "$E/.ufo/waves/round-38/wave1/ExecR37HeadRed.transcript.txt"
        # -> a6cbf185cb7c1669c0937750ff453ba60224fd10b63a37bb9598dcee51778e95  ✓ (881 lines / 51578 B)

Base transcript anchors (defect state at a173b0c2): `corpus/instruments/r38-closure.sh` absent at
the ref (L17); G1 reds — corrections 0, declared-blocks absent (L46, L51-52); G2 red — no round-38
receipt (L76); G5 red — the stale `Final lane commit: f3246559bed2fd085dde860e00247ce394f02bad` at
LOG.md:15 and SCORECARD.md:1509 (L165, L170); G7 red — the empty ledger heading,
non_empty_body_rows=0 (L193); the r37-carry runs print `closed=13/14 exit=1` (L233, L242, L247).
r37-head transcript anchors (defect state at 2387dcf6): the G1-G8 defect-state table with every
check open, and `closed=13/14 exit=1` with only E9 red (L626, L650, L654-655, L689-690, L709-710).

Chain: defect state present at base and at the r37 judged head (transcripts) + every check's mutants
rejected (the receipt's selftest) + the suite digest bound (§0) ⇒ the suite's reds at those refs.
The L1's own counting-command runs (base -> `closed<8/8 exit=1`; 2387dcf6 -> `closed<8/8 exit=1`) are
[L1-MEASURE] assertions in the report/SCORECARD. Corroboration by this seat: the delivered suite
bytes run over the base export printed `closed=0/8 exit=1` with G1-G8 all red (payloads in the seat
receipt §2).

E9 time-dependence caveat (not a contradiction): the transcripts' `closed=13/14` measurements were
taken mid-wave (lane HEAD 7001535, dirty tree) where the r37 suite's LIVE E9 limbs (head-match,
status-dirty) red; the freeze-time control recorded `closed=14/14` when the lane HEAD was the base
and the tree clean (c1-controls/before.txt). ExecBaseRed.md §"Why 13/14" and ExecR37HeadRed.md §3
G8 rows document the isolation.

## 7. G8 carry-over without running (C1)

    sed -n '1p' "$E/.ufo/waves/round-37/final-gates/all-gates.txt"
        # -> all-gates v1  ✓
    grep -cE '^export-ref=9492c776724e737caf5815fabc98e59ea04830df$' "$E/.ufo/waves/round-37/final-gates/all-gates.txt"
        # -> 1  ✓
    grep -cE '^suite-sha256=0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d$' "$E/.ufo/waves/round-37/final-gates/all-gates.txt"
        # -> 1  ✓
    grep -cE '^E[0-9]+ payload=.* closed=1$' "$E/.ufo/waves/round-37/final-gates/all-gates.txt"
        # -> 14  ✓
    grep -cE '^closed=14/14 exit=0$' "$E/.ufo/waves/round-37/final-gates/all-gates.txt"
        # -> 1  ✓
    grep -cE '^selftest cases=14 failures=0$' "$E/.ufo/waves/round-37/final-gates/all-gates.txt"
        # -> 1  ✓
    git -C "$LANE" cat-file blob "$Y:corpus/instruments/r37-closure.sh" | sha256sum
        # -> 0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d  ✓
        #   (K8 strengthening: binds the r37 suite bytes, which the suite's G8 limb does not)
    git -C "$LANE" merge-base --is-ancestor 9492c776724e737caf5815fabc98e59ea04830df "$Y"
        # -> exit 0  ✓

The `closed=14/14` run of `r37-closure.sh` over REF is L1-measured at the green run (lane HEAD equal
to the run ref, clean tree — the r37 suite's E9 live limbs; ExecR37Carry.md §5). The judge does not
run it.

## 8. No-harm numstat

    git -C "$LANE" diff --numstat a173b0c2b98c5ae39599fa9be76027fbbead0b9e "$Y" -- . ':!.ufo' \
      | grep -vE $'^[0-9]+\t0\t' | wc -l
        # -> 0  ✓ (every changed non-.ufo file is additions-only; a binary `-` row does not match
        #   the pattern and is caught)
    git -C "$LANE" diff --numstat a173b0c2b98c5ae39599fa9be76027fbbead0b9e "$Y" -- . ':!.ufo' | grep -c '=>'
        # -> 0  ✓ (no renames)
    git -C "$LANE" diff --numstat a173b0c2b98c5ae39599fa9be76027fbbead0b9e "$Y" -- \
      SKILL.md PROVINCE.md SCORECARD.md LOG.md SHONEN.md corpus/QUALITY.md corpus/SOURCES.md \
      corpus/README.md corpus/knowledge/considerthese-proposals-ledger.md corpus/lessons/round-37.md \
      | awk '$2 == "-" || $2 != 0' | wc -l
        # -> 0  ✓ (the protected ten append-only)

Landed insertions observed at compile time (all x/0): PROVINCE.md 4, SCORECARD.md 2 (+ the round-38
section when it lands), SKILL.md 1, corpus/QUALITY.md 14, corpus/README.md 32, corpus/SOURCES.md 4,
corpus/instruments/knowledge-expected.txt 1, corpus/knowledge/considerthese-proposals-ledger.md 24,
corpus/lessons/round-37.md 15, plus the new files (the entry 137 lines, the capture, the manifest,
the suite 1473 lines, the wave1 evidence, declared-blocks.txt, the junk twin and its recheck
record) as N/0 rows. Stronger form (optional): `bash
"$E/.ufo/waves/round-38/wave1/ExecNoHarm.sh" a173b0c2b98c5ae39599fa9be76027fbbead0b9e "$Y" --repo
"$LANE"` -> EXIT=0 (byte-prefix identity per protected file; the seat's fixtures V1-V5 in its
receipt).

## 9. Filing state

    git -C "$LANE" status --porcelain | wc -l                     # -> 0  ◇ (kill rule)
    git -C "$LANE" rev-parse HEAD                                 # -> $Y  ◇
    git ls-remote origin refs/heads/master                        # -> $Y  ◇ (pushed)
    find /fast/scratch/hyaku/kasegi-r36 /fast/scratch/hyaku/kasegi-r37 /fast/scratch/hyaku/kasegi-r38 -mindepth 1 | wc -l
        # -> 0  ◇ (kill rule; §5 D-E)

## 10. What the judge does NOT run

`corpus/instruments/*` — r38-closure.sh, r37-closure.sh, frontier-recheck-count.py,
source-recheck.py, capture-binding-check.py, recheck-audit.py, capture-source.py, density.py,
anchorcheck.py, score-gap.py — their outputs are evidence-verified from the committed receipts named
above (all-gates.txt, ExecC2Harness.md, ExecC2Binding.md, ExecC2Audit.md, ExecC2Census.md,
ExecDensity.md) and re-derived by the plain commands in §1-§8. The fleet census script
(scripts/sources-census.sh) IS run (r37 §3 precedent). Wave-evidence helpers committed under
`.ufo/waves/round-38/wave1/` (ExecFenceWalk.sh, ExecNoHarm.sh, ExecDeclaredBlocks.gen.sh,
ExecRefChecker.py) are not lane instruments; the judge may run them from the export as cross-checks.
````
