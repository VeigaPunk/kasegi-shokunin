# RevK17 — adversarial review of ExecK17ClaimsBefore (K17, RD42-8)

Seat: reviewer, kasegi round 43 (L1 KasegiR43). Receipt-only item; no deliverable file is produced.
Target under test: `.ufo/waves/round-43/w1/ExecK17ClaimsBefore.sh`, 591 lines, 23 981 bytes,
sha256 `37a513ed7dfbc8dd83d6a77da2a44843ea424e0a932fb501bea681ccedc7f348`
(mtime 2026-10-28 13:48:47 -0300). Every finding below was produced by executing that byte-exact file.

## 1. What I did

Built 36 export trees in scratch and drove the limb's real entry point, not a model of it:

```
. ExecK17ClaimsBefore.sh ; check_k17 <export-root>
```

Each fixture is a minimal export holding only `.ufo/waves/round-41/` and `.ufo/waves/round-42/`
(claims.json, claims-erratum-1..4.md, c1-controls/, c2-controls/, final-gates/) copied from the base
export `ab98fac9dce87130bc4f66de89e30650d63943dc`, plus one named mutation. Two 21-round trees were
built for the satisfiability test: `head` = `4cb6d4ae` (round-43 freeze) plus a synthetic
round-43 `final-gates/all-gates.txt`, once with the erratum placed at
`.ufo/waves/round-43/claims-erratum-1.md` (`y1`) and once at
`.ufo/waves/round-42/claims-erratum-1.md` (`y2`).

Authoritative real-tree runs, one invocation, `run-utc: 2026-10-28T16:51:57Z`:

```
### base
K17 detail round=round-42 claim=C1 field=before token=closed=10/12 cited=.ufo/waves/round-42/c1-controls/do-nothing.txt control-prints=closed=13/13+closed=8/12 result=unbacked
K17 payload=claims=20,tokens=3,verified=2,superseded=0,unbacked=1 closed=0
rc=1
### head            (round-43 freeze 4cb6d4ae, no erratum yet)
K17 detail round=round-42 claim=C1 field=before token=closed=10/12 cited=.ufo/waves/round-42/c1-controls/do-nothing.txt control-prints=closed=13/13+closed=8/12 result=unbacked
K17 detail round=round-43 claim=C1 field=before token=closed=10/13 record=.ufo/waves/round-42/claims-erratum-4.md result=quoted
K17 detail round=round-43 claim=C1 field=before token=closed=10/12 record=claims.json result=quoted
K17 payload=claims=21,tokens=5,verified=4,superseded=0,unbacked=1,quoted=2 closed=0
rc=1
### r41head         (1f7464612ac4c44e39886b82e812610d3c039b13)
K17 payload=claims=19,tokens=1,verified=1,superseded=0,unbacked=0 closed=1
rc=0
### plain run
rc=2
### selftest        (--tree <head> --selftest)
K17 replay committed-defect expected=reject observed=reject payload=claims=21,tokens=5,verified=4,superseded=0,unbacked=1,quoted=2 verdict=pass
K17 replay repaired expected=accept observed=accept payload=claims=21,tokens=5,verified=4,superseded=1,unbacked=0,quoted=2 verdict=pass
K17 replay erratum-without-superseded expected=reject observed=reject payload=claims=21,tokens=5,verified=4,superseded=0,unbacked=1,quoted=2 verdict=pass
K17 replay near-token expected=reject observed=reject payload=claims=21,tokens=5,verified=4,superseded=1,unbacked=0,quoted=2,rejected=closed=10/120 verdict=pass
K17 replay fabricated-value expected=reject observed=reject payload=claims=21,tokens=6,verified=4,superseded=1,unbacked=1,quoted=2 verdict=pass
K17 replay citation-missing expected=reject observed=reject payload=claims=21,tokens=5,verified=3,superseded=1,unbacked=1,quoted=2 verdict=pass
K17 selftest cases=6 failures=0
rc=0
```

The limb's record of its own measured payloads (base `claims=20,tokens=3,verified=2,unbacked=1`;
freeze `claims=21,tokens=5,verified=4,superseded=0,unbacked=1,quoted=2`; `selftest cases=6 failures=0`)
reproduces exactly. Base is red with K17 open, which is what the frozen C1 requires at
`ab98fac9`. The base detail line names the defect and both values (`closed=10/12` claimed vs
`closed=13/13+closed=8/12` printed) — the required near-token report is honest.

## 2. Findings

Severity is against the K17 predicate ("each `before`/`after` token must appear in the control receipt
the claim cites") and against C1's after-state (K17 must be green at Y).

### F1 — BLOCKER: the erratum landing path in the wave spec cannot close K17

`superseded_by()` (line 224) searches `claims-erratum*.md` **only in the graded claims file's own round
dir**. The unbacked token is round-42's `closed=10/12`, so the erratum must sit in
`.ufo/waves/round-42/`. The ScribeClaimsErratum seat's deliverable is byte-exact for
`.ufo/waves/round-43/claims-erratum-1.md`, and INTEGRATION-PLAN item 6 names `claims-erratum-1.md`
without a round path. Same erratum bytes, same 21-round tree, only the directory differs:

```
### y1-erratum-in-43
K17 detail round=round-42 claim=C1 field=before token=closed=10/12 cited=.ufo/waves/round-42/c1-controls/do-nothing.txt control-prints=closed=13/13+closed=8/12 result=unbacked
K17 payload=claims=21,tokens=5,verified=4,superseded=0,unbacked=1,quoted=2 closed=0
rc=1
### y2-erratum-in-42
K17 detail round=round-42 claim=C1 field=before token=closed=10/12 by=claims-erratum-1.md result=superseded
K17 payload=claims=21,tokens=5,verified=4,superseded=1,unbacked=0,quoted=2 closed=1
rc=0
```

The y1 erratum text explicitly names `.ufo/waves/round-42/claims.json` and the token; the limb still
does not look outside the claims file's round dir. Consequence: land the erratum only where its seat
spec says and the suite cannot exceed `closed=18/19`; C1's frozen after-state dies at integration, not
at review. Required: the L1 also lands those bytes at `.ufo/waves/round-42/claims-erratum-5.md`
(`claims-erratum-1..4.md` already exist there and are append-only history), and K4's declaration list
gains that path. This is the limb's own stated landing requirement; it is absent from the wave spec.

### F2 — HIGH: the record-quotation escape is unverified and self-referential

`attribution()` (line 207) grants `quoted=` when the last path in a 240-char window is a *record*
(`claims.json`, `claims-erratum*`, `corpus/lessons/`, `corpus/knowledge/`) and a quote verb follows it,
and it **never checks that the named record contains the token**. A six-word insertion in the defect
cell launders the exact RD42-8 literal:

```
### q2a-self-record
  before = "see <c1 control> - the round-42 claims.json says closed=10/12 exit=1"
K17 detail round=round-42 claim=C1 field=before token=closed=10/12 record=claims.json result=quoted
K17 payload=claims=2,tokens=1,verified=1,superseded=0,unbacked=0,quoted=1 closed=1
### q2b-absent-record
  before = "see <c1 control> - corpus/lessons/round-99-somewhere.md states closed=10/12 exit=1"
K17 detail round=round-42 claim=C1 field=before token=closed=10/12 record=corpus/lessons/round-99-somewhere.md result=quoted
K17 payload=claims=2,tokens=1,verified=1,superseded=0,unbacked=0,quoted=1 closed=1
```

`corpus/lessons/round-99-somewhere.md` does not exist in that export (it has no `corpus/` tree at all).
Green. The clause exists because round-43's own `before` cell quotes `corpus/.../claims-erratum-4.md:9`
and the round-42 claim (line 284 of the frozen claims), so *some* exemption is load-bearing for
satisfiability — but as written it is an author-controlled switch: the same measurement becomes
ungraded by writing "X says" in front of it. Minimum fix: require the named record to exist and to
carry the token as a whole token (otherwise the exemption is a fabrication), and refuse
`record == the claims file being graded` (self-quotation, q2a). Better: attribute by claim id
(`C1.before`) rather than by free prose in a 240-char window.

### F3 — HIGH: `after` tokens are exempt, so the same literal escapes by changing its JSON key

Line 326 (`if field == "after": continue`) drops every after token after near-token checking, by
design. The result is a one-key bypass of the graded defect:

```
### a1-after-relocated
  before = "... prints closed=8/12 exit=1"        (consistent with the control)
  after  = "closed=13/13 exit=0 at Y; the r41 suite at base printed closed=10/12 exit=1"
K17 payload=claims=2,tokens=2,verified=2,superseded=0,unbacked=0 closed=1
### a1-after-token
  after  = "... selftest cases=77 failures=0 and closed=19/19 at Y"   (no backer anywhere)
K17 payload=claims=2,tokens=2,verified=2,superseded=0,unbacked=0 closed=1
```

Two distinct problems, and they conflict:

- The frozen C1 predicate says "extract each `before`/`after` string … require each token to appear in
  the control receipt the claim cites". The implementation grades `before` only, so the frozen wording
  is not met as written. The L1 report must record the scope decision explicitly (it is the one that
  makes C1 satisfiable: no historical round's after cell is printed by a control receipt, and
  round-43's own after cell states its `closed=13/19` base figure nowhere a receipt prints it).
- The narrowing is exploitable: an assertion of a *past measurement* ("the r41 suite at base printed
  closed=10/12") is equally a claim about a run and equally unbacked, but it is invisible in `after`.
  Cheap fix that stays satisfiable: grade an after token when it is introduced by a past/measurement
  verb (`print(s|ed)`, `output(s|ted)`, `read`, `observed`, `reported`) and leave future/target
  phrasing (`at Y`, `will`, `target`, `required`) exempt; or grade after tokens against the round's
  own committed `final-gates/` transcript when one exists in the export.

### F4 — HIGH: a token in a control the claim does not cite backs it

Line 270 collects **every** string value of the document-level `controls` object, and line 284 appends
all of them to **every** claim's receipt set. So a C1 cell that cites only the C1 control is backed by
the C2 control:

```
### f1-control-cross
  controls = {c1: .../c1-controls/do-nothing.txt, c2: .../c2-controls/before.txt}
  C1.before = "see .../c1-controls/do-nothing.txt - the r41 suite at base prints closed=10/12 exit=1"
  c1/do-nothing.txt prints "closed=8/12 exit=1";   c2/before.txt prints "closed=10/12 exit=1"
K17 payload=claims=2,tokens=2,verified=2,superseded=0,unbacked=0 closed=1
```

This is exactly the assigned vector, and it applies to the live round-43 document, whose
`controls` object is `{"c1": ".ufo/waves/round-43/c1-controls/do-nothing.txt",
"c2": ".ufo/waves/round-43/c2-controls/before.txt"}`. Fix: scope `controls.c1` to C1 cells and
`controls.c2` to C2 cells, and treat an in-string path as the only additional backer.

### F5 — MEDIUM: a supersede line that names a different round's token still excuses this one

`superseded_by()` accepts any paragraph in the round dir that contains the token and `supersed`, with
no attribution check. Round-42's dir therefore accepts an erratum about round-41:

```
### a4a-wrong-round
  claims-erratum-5.md: "- Superseded the round-41 claims.json literal `closed=10/12`; the round-42 counter is unaffected."
K17 detail round=round-42 claim=C1 field=before token=closed=10/12 by=claims-erratum-5.md result=superseded
K17 payload=claims=2,tokens=3,verified=2,superseded=1,unbacked=0 closed=1
```

The correct-attribution control greens identically (`a4b-right-round`, same payload). Require the
paragraph to name the graded claims path or `round-42`, or to carry `supersedes round-42 C1`.

### F6 — MEDIUM: dropping the citation removes the token from the population

Line 328 (`if not receipts: continue`) skips every token in a cell that names no receipt. The RD42-8
defect is precisely a `before` literal that contradicts its control, so removing the pointer discharges
it:

```
### a7-citation-strip
  before = "the r41 suite at base prints closed=10/12 exit=1"      (no path)
K17 payload=claims=2,tokens=1,verified=1,superseded=0,unbacked=0 closed=1
### a10-absolute-cite
  before = "see /fast/.../outside-backer.txt - ... prints closed=10/12 exit=1"
K17 payload=claims=2,tokens=1,verified=1,superseded=0,unbacked=0 closed=1
```

An absolute path is not a `PATH_RX` match, so the cell looks uncited. Live evidence that this
population gap is not hypothetical — the round-41 judged head, whose before cells are exactly this
shape, grades one token total:

```
### r41head
K17 payload=claims=19,tokens=1,verified=1,superseded=0,unbacked=0 closed=1
```

19 claims files, 1 graded token. Round-34's `cases=11` / `cases=0` / `failures=0` before literals and
rounds 35-40's after literals are outside the check entirely. Fail-closed alternative: a `before` cell
that carries a token but names no receipt path is `unbacked` unless a same-round erratum names the
token; that keeps base red and is satisfiable at Y only if the historical uncited cells are excused —
so if this is not adopted, the exemption must be written down (the limb's header does document it;
the frozen predicate does not).

### F7 — LOW/MEDIUM: symlinked control reads bytes outside the export

`under_root()` (line 130) uses `os.path.normpath` only. A committed symlink under the export passes
containment and `read()` follows it out:

```
### a12-symlink-escape
  .../round-42/c1-controls/extra.txt -> /fast/scratch/.../outside-backer.txt  (prints closed=10/12)
K17 payload=claims=2,tokens=2,verified=2,superseded=0,unbacked=0 closed=1
```

The token is then backed by bytes that are not in the export. Use `os.path.realpath` containment (the
`..` form is correctly refused: `a13-dotdot-escape` → `result=unbacked`, `closed=0`).

### F8 — LOW: a double-escaped token is invisible

Real JSON escape forms are handled correctly because the file is parsed: `e1` (`\u002f`), `e2` (`\/`)
and `e3` (`\u0031\u0030`) all grade `closed=10/12` and red against a `closed=8/12` control (`closed=0`),
and `e5` (escaped, control prints `10/12`) greens. But a token whose *parsed* text carries the escape
literally — two escapes in the source, e.g. `\\u0031\\u0030/12` — produces no token at all:

```
### a6d-escaped-digits
K17 payload=claims=2,tokens=1,verified=1,superseded=0,unbacked=0 closed=1
```

`tokens=1` is round-41's literal; the escaped one vanished. Low likelihood, but the failure is silent
(skip, not red). A cell containing `closed=` immediately followed by `\` or `u00` should be a mangled
token, not nothing.

## 3. Attacks the limb repelled (stdout quotes)

```
### a2-uncited-control     (token added to the round's c2 file, claim cites c1)
K17 detail ... token=closed=10/12 cited=.ufo/waves/round-42/c1-controls/do-nothing.txt control-prints=closed=13/13+closed=8/12 result=unbacked
K17 payload=claims=2,tokens=3,verified=2,superseded=0,unbacked=1 closed=0
### a3a-nested-green      (nested claims file present; 3 files, claims=2)
K17 payload=claims=2,tokens=3,verified=2,superseded=0,unbacked=1 closed=0
### a3b-nested-red        (nested file carries closed=99/99; top level consistent)
K17 payload=claims=2,tokens=2,verified=2,superseded=0,unbacked=0 closed=1
### a5a-prefix            (cell holds closed=1/12 and closed=10/120; control prints closed=10/120)
K17 detail ... token=closed=1/12 ... control-prints=closed=13/13+closed=8/12+closed=10/120 result=unbacked
K17 detail ... token=closed=10/120 result=rejected near-token
K17 payload=claims=2,tokens=2,verified=1,superseded=0,unbacked=1,rejected=closed=10/120 closed=0
### a5a2-prefix-clean     (claim closed=1/12, control prints only closed=10/12)
K17 detail ... token=closed=1/12 ... control-prints=closed=10/12 result=unbacked
K17 payload=claims=2,tokens=2,verified=1,superseded=0,unbacked=1 closed=0
### a5b-prefix-rev        (claim closed=1/12, control prints closed=10/12; reversed build)
K17 payload=claims=2,tokens=2,verified=1,superseded=0,unbacked=1 closed=0
### a5d-claim-prefix-ext  (claim closed=10/12, control prints closed=10/120)
K17 detail ... token=closed=10/12 ... control-prints=closed=10/120 result=unbacked
K17 payload=claims=2,tokens=2,verified=1,superseded=0,unbacked=1 closed=0
### a5e-claim-1of12-ext   (claim closed=1/12, control prints closed=1/120)
K17 payload=claims=2,tokens=2,verified=1,superseded=0,unbacked=1 closed=0
### a5f-exact-backed      (claim closed=10/12, control prints closed=10/12 — positive control)
K17 payload=claims=2,tokens=2,verified=2,superseded=0,unbacked=0 closed=1
### a15-trailing-period   (claim token followed by "." then prose)
K17 detail ... token=closed=10/12 cited=... control-prints=closed=13/13+closed=8/12 result=unbacked
K17 payload=claims=2,tokens=2,verified=1,superseded=0,unbacked=1 closed=0
### a16-trailing-backtick (claim token inside backticks)
K17 payload=claims=2,tokens=2,verified=1,superseded=0,unbacked=1 closed=0
### a13-dotdot-escape     (cited path leaves the export with ..)
K17 detail ... cited=.ufo/waves/round-42/../../../../../outside-backer.txt control-prints=none result=unbacked
K17 payload=claims=2,tokens=2,verified=1,superseded=0,unbacked=1 closed=0
### f2-parse              (truncated claims.json)
K17 detail round=round-42 result=parse-error
K17 payload=claims=2,tokens=1,verified=1,superseded=0,unbacked=0,parse=1 closed=0
```

So: the whole-token boundary (prefix, extension, punctuation, backticks), the near-token naming, the
cited-file scope against an *uncited* control in the same round, nested-claims exclusion, `..`
containment and parse failure all behave fail-closed and are correctly evidenced. The gaps are the
exemptions the limb added to make round 43 satisfiable (F2, F3, F4, F6), the erratum's missing
attribution (F5) and its directory rule (F1).

Note on F1's evidential weight: `a4b-right-round` and `y2` show the erratum mechanism works when the
file is in the graded round dir, so F1 is a landing-path defect, not a broken mechanism.

## 4. Residual risk

- **Token presence is not measurement context.** `present()` is a bare whole-token `find`. Round-42's
  before `closed=13/13` is "verified" by control line 7,
  `(observed suite exit = 127; the suite cannot print closed=13/13 — do-nothing cannot reach the
  after-state)` and line 12, i.e. by the two sentences denying it. Any claim can be backed by a
  receipt that quotes it in a negation, a would-be, or another round's defeat log. Verifying the
  polarity/verb context around the hit would close this; it is inherent to the "literal appears in the
  cited receipt" grammar the frozen claim froze.
- **A cited `corpus/instruments/...` path is a receipt.** `is_record()` excludes only
  `corpus/lessons/` and `corpus/knowledge/`, so `corpus/instruments/r42-closure.sh` counts as a cited
  control; its own selftest fixture strings (`closed=13/13`, `closed=13/130`) would back a claim. No
  committed claim cites an instrument, but the class is open.
- **The round-43 freeze is read through two exemptions.** Its own `before` cell is green only because
  `closed=10/13` and `closed=10/12` are `quoted=` (head payload `quoted=2`). If F2 is tightened without
  exempting the round's own quotation of the RD42-8 defect, C1 becomes unsatisfiable. Tighten F2 by
  requiring the quoted record to carry the token — `claims-erratum-4.md` does carry `closed=10/13` and
  round-42's claims.json does carry `closed=10/12`, so the real round-43 cell survives a verifying
  rule, while `q2b` (absent record) stops working. `q2a` (self-quotation) must still be refused, and
  round-42 is graded on its own freeze, so refusing it is safe.

## 5. Verification gaps

- I did not run the integrated `r43-closure.sh` (not landed at review time); K17 was graded through its
  own `check_k17` entry point, which is the function the suite calls. Whether the skeleton wires the
  limb's stderr detail lines into the suite transcript is unreviewed.
- Y is not yet a commit. My `y1`/`y2` trees are the freeze commit plus a synthetic
  `round-43/final-gates/all-gates.txt` (`closed=19/19 exit=0`, `selftest cases=19 failures=0`) and one
  erratum; K17 does not read that receipt, so the placement result is independent of its contents.
- No language server applies: K17 is a bash/python instrument graded by execution, and there is no
  `lsp` device in this seat's tool inventory. All boundary/selection claims above are backed by the
  executed output quoted, not by reading alone.
- I did not re-run the limb's selftest against its own scratch after the 13:48 write; the hash in §1 is
  the file I tested. If the deposit changes, these findings must be replayed (the battery is 36
  one-mutation trees, ~3 s).

## 6. Tooling, scratch, network

- Tools installed or upgraded: none. No `pacman`. No network fetch (no `curl`). Disk guard checked
  before the heavy pass: `/fast/scratch/hyaku` 25 % used, 603.6 G free.
- Scratch `S=/fast/scratch/hyaku/kasegi-r43/RevK17` (base export, freeze export, three 21-round
  trees, 33 one-mutation fixtures, harness) removed before yield; receipts and this file are the only
  artefacts kept. The deliverable is this receipt (no separate landable bytes); it is written last.
- One IRC from W1ScribeLessonGate reported a `corpus/SOURCES.md` row defect (S242 unescaped pipe,
  `sources-census.sh validate --root … souji` → `E01 S242 fields=12`). Out of my write scope (lane
  file, and this seat may not edit it); recorded here so the owning seat is not left without a trace.
