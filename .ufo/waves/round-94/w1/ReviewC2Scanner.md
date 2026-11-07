# ReviewC2Scanner — Kasegi round 94, wave 1

Leaf seat. Lane `kasegi`, C2 only (C1 is ReviewC1Labels-5's scope). Commits:
base `dff5a0a01e8aafe6be81f4ee61567745c3c4c485`, freeze
`96b5033f4dfa8d6605c13e0c9aad458be3cd7df3`, C1 landing
`d51220aeb4a538b7b211bb2629e83210669cd56d`, C2 landing
`996460861d4130ddb2da6b7554e905d3e47504a3`.

All work read-only against the lane; scratch under
`/fast/scratch/hyaku/kasegi-r94/ReviewC2Scanner` (removed on exit); no tool
installs (none needed); no subagents.

## Verdict

**C2 STANDS.** P1, P2 and P3 re-derived at the landing: K1–K9 pass at the
printed run-time seed (3014267912) and at seeds 1 and 9191; the landed
instrument sha256 is the frozen candidate
`22ba32d145f90f7759caf16d3ee524eb1779153d3f2a33611675a93a4667beaf`; the
landing commit changes exactly `SCORECARD.md` and
`corpus/instruments/capture-secret-scan.py`, and the landed capability row is
byte-identical to the frozen candidate row
(`4f10e273f3c27e5b43cec77b280071d13284c3c475e976ac160bb674ca4beed8`).
P4's receipt prints `C2-CONTROLS-RESULT pass controls=10`, but one control the
frozen P4 text names is not in the executed set (F1). Under the frozen kill
rule ("any limb FAIL … or P3 naming another path set") that mismatch is not a
NOT VERIFIED trigger; it is routed as a claim-text defect. All remaining
findings are routed qualifiers that do not re-score C2.

## Clause-by-clause

### S140 anchors and capture integrity

The three quoted regex lines in `corpus/source-snapshots/round-94/S140.txt`
are unredacted and equal the manifest quotes (`Q01` anchor 4, `Q02` anchor 114,
`Q03` anchor 255):

```
line   4: regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glpat-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''
line 114: regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?glrtr?-(?:t[1-3]_)?[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''
line 255: regex = '''\b((?:[a-zA-Z0-9]{1,20}-)?gldt-[0-9a-zA-Z_\-]{20})(?:[^0-9a-zA-Z_\-]|$)'''
```

Committed capture: sha256
`f3fd09e46db3b2447f237318fd2dbb8979f204c9242f19cddef98986039a158c`,
25537 bytes, 563 lines; it equals the freeze blob and `git show HEAD:` bytes.
The manifest/redaction receipt record the raw 20035-byte snapshot
`04fc5cfa200c92f54e14a7d104bb56e479aeccf45746234f0965c3c8e637d921` (the
digest `claims.json`'s frontier names) and the committed redaction.

**Redaction count does not match the seat text.** The seat says "the 18
redacted lines"; the measured committed capture has **82** redacted lines
(`wc -l` of `controls/redaction-r94.txt` is 82 list rows + 3 trailer lines, and
`grep` finds 82 marker lines). All 82 carry the one fixed marker verbatim;
there is exactly one distinct marker variant, and every line containing
"redacted" is that marker. Lines 4, 114 and 255 carry none. The three landed
rules' `examples` arrays hold 16 element lines (7 + 4 + 5); the capture has 24
`examples` arrays and no `negativeExamples` arrays, so neither 18 nor 16 is a
second hidden count. This is a premise defect in the assignment, not a landing
defect (F4).

### Shapes (landed instrument `corpus/instruments/capture-secret-scan.py`)

| Clause | Landed evidence | Result |
|---|---|---|
| `gitlab-pat`: `glpat-`, optional 1–20 alphanumeric + `-` prefix, 20-char `[A-Za-z0-9_-]` tail, right boundary `(?![A-Za-z0-9_-])` | line 199: `_GL_LB + _GL_PREFIX + rb"glpat-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])"`; `_GL_PREFIX` at line 197 is `(?:[A-Za-z0-9]{1,20}-)?` | PASS |
| `gitlab-runner-auth-token`: `glrt-` or `glrtr-`, optional `t1_`/`t2_`/`t3_`, 20 tail chars | line 200: `_GL_LB + _GL_PREFIX + rb"glrtr?-(?:t[1-3]_)?[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])"` | PASS |
| `gitlab-deploy-token`: `gldt-` + 20 tail chars | line 201: `_GL_LB + _GL_PREFIX + rb"gldt-[A-Za-z0-9_-]{20}(?![A-Za-z0-9_-])"` | PASS |
| Anchors S140 lines 4 / 114 / 255 | quotes above; manifest `quotes[].anchor` equal to the capture lines | PASS |
| Right boundary | 43-case battery: 19/21-char tails, trailing `Z`, `_`, `-` all miss; trailing `.`, space, newline hit | PASS |
| Optional partition | `t1_`, `t2_`, `t3_` hit; `t4_`, `t0_` miss; `t1_` with a 19-char tail misses | PASS |
| Custom prefix on all three shapes | `acme-glpat-`, `acme-glrt-`, `acme-gldt-` and `acme-glrtr-t3_` all report their shape | PASS |
| Letter-before negative | `xglpat-`, `xglrt-`, `xgldt-` miss (selftest `gl-pat-letter-before`, line 417; K4 plant `S054.txt`) | PASS |
| Prefix bound 1–20 | 1- and 20-char prefixes hit; a 21-char alphanumeric run before `-glpat-` reports the bare token after the hyphen, exactly as S140's `\b` does (`vendor-vs-instrument.txt`, `pat-prefix-21` and `pat-prefix-underscore`) | PASS with note |
| Vendor-regex agreement | 40 constructed cases against the three S140 regexes: 39 identical, 1 intentional difference (`\u0026glpat-` → instrument hit, vendor no hit; the documented round-93 escape-terminator extension) | PASS |
| Selftest | `SELFTEST-RESULT pass cases=101`, rc 0 | PASS |
| Round-93 `glrt-` known limit retired | old line 107–108 sentence removed by the landing; `glrt-<20>` now reports `gitlab-runner-auth-token` (selftest line 422, battery `runner-glrt`) | PASS |

The letter-before sentence is imprecise as written: `xacme-glpat-<20>` **is**
reported (the bare token after the prefix's hyphen), and S140's own regex also
matches it; the intended negative is a letter immediately before the token
with no hyphen (`xglpat-`). See F3.

### Relocation (M93-4) and K9

`relocate()` (`capability-check.py:503-529`) replaces every directory segment
and basename with a run-time nonce/hash while preserving the scan-scope class;
the `live-` filename prefix is preserved because scope requires it. K4 passed
at three run-time nonces (`missing=none extra=none`). The F1 path-shape-keyed
forgery (`controls/c2-controls-r94.py:21-25`) keys on `/round-1/`, `/S0` and
`live-`; its K4 line has no `live-*` entry in `missing` and `extra=none`, i.e.
it **did** catch every relocated `live-*` plant. The claim's inference "so a
path-shape-keyed detector finds nothing" is therefore false as a universal
(F2), even though the control still fails (rc 1) for the 30 non-live plants and
the relocation itself is real.

K9 (`capability-check.py:634-649`, `ROUND94_SHAPES` at 308) passed in all
three seeds: `prev_rc=1 prev_hits=39 lost=none prev_caught_new=none`. The
exclusion of the HTML-entity `live-o` pair from `ROUND94_SHAPES` is documented
at lines 306–308: round 93 already carried that branch, so it is not a new
shape. Matches the frozen sentence.

### Frozen predicate

| Limb | Result | Evidence |
|---|---|---|
| P1 K1–K9 | PASS at seeds 1, 9191 and run-time 3014267912 | three `capability-check-seed-*.txt`, 11 lines each |
| P2 hashes | landed scanner == candidate `22ba32…beaf`; gate `8b6f84…8e6` == pin; counter `7619ea…1d076` == pin | `hashes-and-paths.txt` |
| P3 paths | `git diff-tree --no-commit-id --name-only -r 9964608` → exactly `SCORECARD.md`, `corpus/instruments/capture-secret-scan.py`; row `cmp`-identical to candidate row | `hashes-and-paths.txt` |
| P4 controls | receipt prints `C2-CONTROLS-RESULT pass controls=10`; candidate rc 0 pinned; do-nothing, F1–F6, row-round93, tampered-instrument all rc 1 | `controls/c2-controls-r94.txt`; `p4-control-name-audit.txt` |
| P4 name set | **mismatch**: P4 (`claims.json:28`) names `S140-allowlist-removed`, the `controls` field (`claims.json:38`) names `s140-allow-rows-removed`; the executed receipt's tenth control is `tampered-instrument`, and no such control exists in `c2-controls-r94.py` or anywhere outside `claims.json` | F1 |

### Docstring known-limits list and citation numbers

Every cited S140 line is correct: the known-limits paragraph (instrument lines
120–134) cites 30, 51, 136, 324 (routable forms), 430, 447, 464 (JWT forms) and
73, 190, 229, 213, 375, 278, 392, 174, 412 (remaining prefixes); each number is
exactly the `regex =` line of the named S140 rule. The retained round-93
citations (`S139 lines 86-87` for the 20-char length) still point at the
sentence they quote.

The list is accurate item by item but not exhaustive. S140 carries 30 rules:
3 are detected (`gitlab_personal_access_token` line 4,
`gitlab_runner_auth_token` line 114, `gitlab_deploy_token` line 255), 16 more
are named at the anchors above, and **11 are neither detected nor named**:
runner registration `GR1348941` (101), `feed_token=` (160), `glcbt-` non-JWT
(293), the standalone legacy `t1_` partition (308), `gitlab+deploy-token-N:…@`
(341), `glagent-` routable (358), `gliamrt-` (480), `gliamac-` (497), `glft-`
path-dependent (514), trigger-in-URL (532) and the session cookie (549). The
`declined` text says "the remaining eleven prefixes" are "named known limits in
the instrument"; the landed docstring names 9 remaining prefix families, not
those 11 (F5). Saturation is not claimed anywhere else; the instrument's
"Known limits" heading remains honest but incomplete.

### Retained round-87..93 sentences

The landing's diff touches only the GitLab subtopic, the `_GL_*` constants and
the GitLab selftest cases. Every retained AWS/GCS/Azure/CloudFront/GitHub
sentence and every retained known-limit item is unchanged, and the 101-case
selftest passes (K1). One prior statement drifts (F6): the round-93 frozen C2
statement says `gitlab-pat` is "not preceded or followed by A-Za-z0-9_-", and
the round-94 instrument now reports `-glpat-<20>` (old instrument at 96b5033:
miss; landed instrument: hit; `round93-boundary-diff.txt`). The old sentence
was scoped to "At the landing commit" and remains true of `9225954a`; the new
docstring states the new boundary ("not preceded by a letter, digit or `_`")
and the new selftest pins the hyphen-before hit (line 421).

### Knowledge citations

Five knowledge entries cite the instrument by line
(`grep -rlE 'capture-secret-scan\.py:[0-9]' corpus/knowledge`):

- `capture-intake-gate.md` — 20 citations
- `cloud-signed-cookies-and-user-bound-sas.md` — 16
- `cloud-signed-url-credentials-in-captured-evidence.md` — 24
- `github-prefixed-tokens-in-captured-evidence.md` — 39
- `presigned-url-credentials-in-captured-evidence.md` — 3

102 citations total; **69 have shifted line numbers** at this landing. The
landing inserts 14 net lines before old line 106, 5 more in the rewritten
known-limits block, one line at old 177, two at old 179, and 11 in the selftest, so:
old 109–176 shift by +19 (36 citations), old 180–395 by +22 (19 citations),
and 14 citations have a range origin inside a rewritten block (the 106–115
known-limits paragraph or the 1-13x docstring bound). The full old→new list is
in `ReviewC2Scanner-receipts/knowledge-citation-reanchor.txt` and
`reanchor-shifted.tsv`; the non-uniform cases are:
`capture-intake-gate.md:134` 23–115→23–134;
`cloud-signed-cookies…:90` 1–133→1–152;
`cloud-signed-url…:65` 1–132→1–151;
`github-prefixed…:85` 1–133→1–152;
`github-prefixed…:106` 106–107→120–127 (quote text ends at new 121;
the range end is inside the rewritten block);
`github-prefixed…:294` 106–109→120–128.
The entries were not (and, under P3, could not be) re-anchored in this landing;
this is a later-round repair list, not a C2 defect (R1).

## Findings

### F1 — High (verifiability): P4 names a control the receipt does not contain

`claims.json:28` (P4) names `S140-allowlist-removed` and `claims.json:38`
(`controls`) names `s140-allow-rows-removed` as the tenth control. The executed receipt
(`controls/c2-controls-r94.txt`) has ten controls whose tenth is
`tampered-instrument`; `controls/c2-controls-r94.py:120-130` implements only
that tamper control; `grep -rn s140-allow-rows-removed .ufo` finds it only in
`claims.json`. The receipt still prints `C2-CONTROLS-RESULT pass controls=10`,
and the candidate limb is rc 0 with the pinned instrument hash, so the
behavioural evidence is intact; but P4 *as written* is not literally satisfied.
The frozen kill rule does not name P4, so this is routed as a claim-text defect:
either rename the control in the claim or add and re-run the missing control.

### F2 — Medium (statement truth): "a path-shape-keyed detector finds nothing" is false

`relocate()` (`capability-check.py:503-529`) keeps the `live-` basename prefix
(it is part of the documented scan scope). The F1 forgery keys on `live-` as
well as on `/round-1/` and `/S0`; its K4 evidence has `extra=none` and no
`live-*` path in `missing`, i.e. a path-shape-keyed detector catches every
relocated `live-*` plant. The relocation of directories and basenames is
verified; the universal conclusion is overstated and the F1 comment
(`c2-controls-r94.py:20-25`, "so it finds nothing") is contradicted by its own
K4 line. No verdict change: F1 still fails (rc 1) on the 30 non-live plants.

### F3 — Medium (statement precision): the letter-before clause is only true for the token, not a prefix

`xglpat-`, `xglrt-`, `xgldt-` correctly miss, and K4's clause plant is
`S054.txt` = `xglpat-<20>`. But `xacme-glpat-<20>` **hits** (bare token after
the prefix hyphen) and S140 line 4 matches it too
(`vendor-vs-instrument.txt`); likewise for `runner`/`deploy`. The frozen
sentence "a letter immediately before the prefix without a hyphen is still not
a hit" should read "before the token/prefix start, with no hyphen". Routed
wording fix; behaviour is S140-faithful.

### F4 — Medium (assignment premise, not the landing): "18 redacted lines" vs 82

Measured: 82 redacted element lines, one fixed marker, 0 other "redacted"
strings, lines 4/114/255 unredacted; manifest and `redaction-r94.txt` agree on
82 (`raw snapshot sha256=04fc5c…`, `committed snapshot sha256=f3fd09…`,
`redacted=82`). The landed three rules hold 16 example lines (7+4+5); no
round-94 artifact records an 18-line redaction. The capture's own integrity checks
pass; the seat text needs correction.

### F5 — Low (documentation): known-limits list is accurate but incomplete

Every named item and all 16 anchors check out against S140, but 11 S140 rule
families are neither detected nor named (list in the clause section), and
`claims.json`'s `declined` wording says those eleven are "named known limits in
the instrument". The docstring names 9 remaining prefix families. Fix the claim
text or extend the list; no behaviour change.

### F6 — Low (prior-claim drift): round-93's `gitlab-pat` boundary sentence no longer describes the landed instrument

Round-93 frozen C2 statement: "`gitlab-pat` for `glpat-` … not preceded or
followed by A-Za-z0-9_-". At 9225954a a preceding `-` blocked the match; the
round-94 landing relaxed `_GL_LB` from `(?<![A-Za-z0-9_-])` to
`(?<![A-Za-z0-9_])` and `-glpat-<20>` now hits (`round93-boundary-diff.txt`;
new selftest line 421). The widening is S140-faithful and disclosed in the new
docstring, but the round-94 claim does not name it. The round-93 landing
commit remains as verified; route as a supersession note/lesson.

### F7 — Low (verification gap): no frozen limb quite pins the deploy/runner custom prefix as a mechanism

K4 plants prefixed `glpat-` only (S052); K7 generates a prefixed `glpat-` only;
the landed selftest cases are `gl-pat-custom-prefix` and
`gl-runner-custom-prefix` (lines 418, 426), with **no** `gl-deploy-custom-prefix`.
A scratch mutation removing `_GL_PREFIX` from line 201 still passes the 101-case
selftest and still reports `acme-gldt-<20>` (via the bare branch after the now
allowed hyphen; `deploy-prefix-test-gap.txt`). The clause is true at the
landing (battery), and the shared `_GL_LB` makes the prefix group redundant for
detection; the residual gap is only a per-shape boundary regression, which the
frozen suite would not catch. Keep as a coverage note, not a blocker.

## Residual risk and verification gaps

- The S140 example values are redacted by design (GitHub push protection), so
  the landed instrument was not run on the vendor's literal examples. I ran the
  three vendor regexes themselves side by side with the instrument on 40
  constructed cases (39 agree; the one difference is the documented round-93
  `\u0026` escape extension). The literal example values remain unverified.
- The controls receipt was audited, not re-executed (freeze artefact; the
  candidate clone commit `1ab01c9` is not in the lane). The counter itself was
  re-run at the landing at three seeds, which is the P1 content.
- The 82 redactions prevent proving that every published example value was
  replaced; only marker consistency, the redaction line list and line-number
  preservation are verifiable.
- `allowed=24, unused_allow=0` at the landing (K3, 2224 scanned files) means the
  redacted S140 capture produces no hit and no allowlist row was stale; the
  direct `--files` probe reported `unused_allow=23` of 23 allowlist rows (none
  consumed; `round93-boundary-diff.txt`), and the 43-case battery harness
  suppresses the summary line.
- The re-anchor list (69 of 102 citations) is not applied here; P3 fixes the
  landing to two files, so it belongs to a later round.
- C1's tranche 9 is out of this seat's scope and was not reviewed.

## Receipts

All paths relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Receipts
are under `.ufo/waves/round-94/w1/ReviewC2Scanner-receipts/`.

1. `sha256sum corpus/instruments/capture-secret-scan.py .ufo/waves/round-94/c2/candidate-capture-secret-scan.py corpus/instruments/claim-package-check.py .ufo/waves/round-94/c2/capability-check.py` — rc 0; 4 lines; landed == candidate `22ba32…beaf`, gate `8b6f84…8e6`, counter `7619ea…1d076` (`hashes-and-paths.txt`).
2. `git diff-tree --no-commit-id --name-only -r 996460861d4130ddb2da6b7554e905d3e47504a3` — rc 0; 2 lines: `SCORECARD.md`, `corpus/instruments/capture-secret-scan.py` (`hashes-and-paths.txt`).
3. `cmp <(sed -n '307p' SCORECARD.md) .ufo/waves/round-94/c2/candidate-row.txt` — rc 0; identical; sha256 `4f10e2…eed8` (`hashes-and-paths.txt`). Rechecked against the commit (`git show 9964608:SCORECARD.md`), whose row 307 is also identical (`committed-scorecard-row.txt`); the working tree is being edited by other seats, so the commit-pinned check is the durable one.
4. `python3 -B .ufo/waves/round-94/c2/capability-check.py --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin --rev 99646086… --work $S --instrument-sha256 22ba32… --gate-sha256 8b6f84… --seed 1` — rc 0; 11 lines; `CAPABILITY-CHECK-RESULT pass`, K1–K9 pass (`capability-check-seed-1.txt`).
5. Same command, `--seed 9191` — rc 0; 11 lines; pass (`capability-check-seed-9191.txt`).
6. Same command, no `--seed` — rc 0; 11 lines; printed seed=3014267912; pass (`capability-check-seed-runtime.txt`).
7. `python3 -B corpus/instruments/capture-secret-scan.py --selftest` — rc 0; 102 lines; `SELFTEST-RESULT pass cases=101` (`instrument-selftest.txt`).
8. Vendor-regex side-by-side harness (S140 lines 4/114/255 vs `--files` on 40 scratch files) — script rc 0; `VENDOR-COMPARE cases=40 diffs=1`; the one diff is `pat-json-u0026` (`vendor-vs-instrument.txt`).
9. Corrected boundary battery (43 cases: prefix/tail/partition/boundary/escape) — instrument rc 1 (hits found, expected); `BATTERY cases=43 fail=0` (`regex-boundary-battery-corrected.txt`). The first pass (`regex-boundary-battery-first-pass.txt`) had 7 expectation errors of mine, corrected by the vendor comparison.
10. S140 marker audit — rc 0; 82 marker lines, 82 lines containing `redacted`, 1 distinct marker, 0 marker hits on lines 4/114/255 (`s140-marker-audit.txt`).
11. S140 manifest/redaction audit — rc 0; committed sha256 `f3fd09…a158c`, 25537 bytes, 563 lines; raw `04fc5c…d921`, 20035 bytes; all three manifest quotes equal their capture lines; landed-rule arrays 7+4+5; `negativeExamples` 0 (`s140-manifest-and-redaction.txt`).
12. S140 rule coverage table — rc 0; 30 rules, 3 detected, 16 named anchors, 11 uncovered and unnamed (`s140-rule-coverage.txt`).
13. Knowledge citation enumeration and old→new line mapping — rc 0; 5 files, 102 citations, 69 shifted; 36 × +19, 19 × +22, 14 rewritten-origin (`knowledge-citation-reanchor.txt`, `reanchor-shifted.tsv`).
14. P4 control-name audit — rc 0; 10 executed controls, last `tampered-instrument`; `s140-allow-rows-removed` only in `claims.json:28,38` (`p4-control-name-audit.txt`).
15. Canonical-runtime audit — rc 0; one tracked live scanner (`corpus/instruments/capture-secret-scan.py`); `capture-source.py:102` imports that path; candidate copies exist only under `.ufo/waves/` (`canonical-runtime.txt`).
16. Round-93 vs round-94 boundary probe on `-glpat-<20>` — rc 0; old instrument misses, landed instrument reports `gitlab-pat` (`round93-boundary-diff.txt`).
17. Deploy-prefix mutation probe — rc 0; mutated (no `_GL_PREFIX` on `gldt-`) selftest pass 101 and prefixed deploy still hit (`deploy-prefix-test-gap.txt`).
18. `sed -n '196,201p'` + docstring extraction — rc 0; landed `_GL_LB`/`_GL_PREFIX`/patterns at lines 196–201 (`landed-regex-and-docstring.txt`).
