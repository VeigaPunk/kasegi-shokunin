# CritProvinceScope — province check: the round-43 claim-package gate

Seat `CritProvinceScope` (critic, receipt-only), kasegi-shokunin round 43, frozen claims
`4cb6d4ae`, base `ab98fac9`. Written 2026-10-28T16:57Z, after the wave-1 gate, exemplar and
knowledge-entry bytes settled; §9 carries the digest of every file quoted here so the reader
can tell whether the bytes moved after this receipt.

## 1. Verdict

**IN PROVINCE.** A claim-package gate is kasegi's own ground — not chousa's, kagi's or a
sibling's — and it does not become an authorization mechanism: it reads no live target and
grants no scope. It certifies record *shape* only, measured in §4. Three record-level fixes
before landing: one clause that every lane record is missing (F1, the important one), one
stale duplicate of the exemplar's prose (F2), and one env-redirectable selftest (F3). None of
them moves the gate out of province; F1 moves the *record* back to what the gate actually does.

## 2. Province fit — quotes

`PROVINCE.md` (kasegi):

- :3 — "**Domain:** bounty & security research — scopes ~/Projects/bounties, program rules, claim packages"
- :29-30 — "The line-3 domain comprises program rules, scopes, and claim packages; the / core
  also covers triage and claim gates, and submission/disclosure packaging."
  A machine gate over the six-file claim package is literally "claim gates" and
  "submission/disclosure packaging" from that sentence — an execution of Core, not an extension.
- :31 — "These surfaces are corpus-attested, while their source roots are absent." The gate's
  specification is the lane's own corpus (`corpus/knowledge/claim-package-contract.md`,
  `corpus/knowledge/claim-gates.md`, `corpus/knowledge/triage-thresholds.md` §4), i.e. exactly
  the attested surface Core describes.
- :25 — "**Refuses:** anything outside this domain; report cross-domain evidence back to the
  orchestrator rather than absorbing it."

Sibling hand-off (read-only read of `chousa-shokunin/PROVINCE.md`):

- :10 — "**Refuses:** bounty-program scope and claim packages (→ kasegi)" — chousa routes claim
  packages *to* kasegi. This gate cannot be an absorption of chousa's ground; it is the object
  chousa refuses.
- :5-8 — chousa owns "source hierarchy ... claim-vs-source verification ... the external-target
  approval table". The gate does none of the three: no source hierarchy, no citation chaining,
  and its only source-facing test is "every whole 64-hex token it cites equals a manifest
  artifact digest" (`ScribeKnowledgeGate.entry.md`, R-REPORT), i.e. package-internal integrity,
  not claim-vs-source. Measured §4-C.

`PROVINCE.md` (kasegi) :45-52:

- :45 "Sibling lanes are reported, not absorbed:"; :47 "chousa — research method and source
  hierarchy"; :48 "kagi — secrets and vault handling".
- :52 "Live-target testing is refused; this corpus is documentation only."

`PROTOCOL.md` (fleet) :407-409 — "**Scope.** Read-only over surfaces it does not own, and it
never acts on an external surface — / publishing, vault approval, claim submission and driver
mutation stay operator-owned". The gate is on the right side of that clause: §4-A measures no
external act at all, and the delivered entry states the same guarantee — "It makes no network
call and runs no git command." (`ScribeKnowledgeGate.entry.md:7`).

## 3. The round's one network surface is not the gate

`corpus/instruments/README.md`:172-173 records that `capture-source.py` "**is a network-capable
producer**; the scheme allowlist lives in `allow_url()`". The S067 fetch went through that
instrument (`ExecSourceCapture.provenance.txt`: `curl -sS -L --max-time 90 -A
kasegi-shokunin/1.0` then `capture-source.py --id S067 --url ...
--kind html`). That is pre-existing lane capture practice, not the gate, and it is a single
unauthenticated GET of a public vendor advisory — not a live target.

## 4. Measured: no live target, no scope grant, no secret leak

All runs use the delivered CLI copied to scratch and run from scratch:
`gate.py` sha256 `8b6f8493…cc8e6`, 32520 bytes.

**A. Confinement / no external act.** `strace -f -qq -e trace=openat,connect,socket` over
`python3 gate.py <exemplar>` →

    rc=0
    net=0 opens=185 writes-outside=0

(the only non-package opens are the Python runtime's: `/etc/ssl/openssl.cnf`, site-packages,
`pyvenv.cfg`). The CLI imports only `argparse hashlib json os re stat subprocess sys`;
`subprocess` is reachable only from the `--selftest` branch (`claim-package-check.py:769,775,778`).
It cannot read a live target.

**B. No scope grant — an invented authorization passes.**

    RULE R-CUSTODIAN verdict=pass detail=chain=1,grant-miss=0,signal-bad=0,head=bound
    RULE R-STATUS    verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=true
    package=… rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0

on a package with `custodian-receipts.json:matched_grant_id = "INVENTED-GRANT-0001"` (a string I
made up), `status.claim_review.hard_gates.authorization = "PASS"` (self-asserted) and
`claimable: true`. `matched_grant_id` is checked for non-emptiness only
(`claim-package-check.py:457-460`; same predicate in `ExecGateChain.rules.py:216-218`).
`verdict=WELL-FORMED` therefore says nothing about whether a grant exists.

**C. No scope grant — a denial passes.**

    RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=1,unbound=0
    package=… rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0

on a report whose scope section reads "This package contains no scope excerpt and no program
policy was read." (marker, URL and a bound digest present). R-REPORT is `/scope\s+excerpt/i`
(`:120`, `:634`); it never opens the URL and cannot say the quoted text is programme policy. A
WELL-FORMED verdict is not scope evidence.

**D. Not a "not-submitted" verdict either.** The exemplar with `status.submission_performed:
true`, `submitted_url` and `submission_state: "SUBMITTED"` added →

    package=… rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0

The gate never reads those fields; submission is named as an operator gate in the checklist, so
the record is honest about it, but WELL-FORMED does not imply "not submitted".

**E. kagi boundary held.**

    RULE R-NOSECRET verdict=fail detail=hits=1,first=provenance.json,shape=credential
    echo=0

for a package carrying `password = 0123456789abcdef0123456789abcdef` in `provenance.json`: the
shape check fires and the matched value never reaches stdout (`echo=0` on a grep for the literal).
Detection stays a shape check; custody of a real secret remains kagi's under `PROVINCE.md`:48.
This matches the entry's own wording, "It reports the shape and the first file, never the matched
value."

## 5. F1 — every record stops one clause short of naming scope authorization (fix before landing)

The exemplar is the round's worked package and the gate certifies it: `rules=8 pass=8 fail=0
verdict=WELL-FORMED exit=0` on the current bytes (§9). The records around it, however, read as if
authorization had been established:

- `ExecExemplarPackage.status.json:23` — `"authorization": "PASS"` inside `hard_gates`, while
  `ExecExemplarPackage.custodian-receipts.json:11,20,29` carry `matched_grant_id`
  `R43-EXEMPLAR-SCOPE-001`, `R43-EXEMPLAR-EVIDENCE-001`, `R43-EXEMPLAR-ATTEST-001` — fixture
  identifiers, not a grant from any programme. The package's own source is a public advisory for
  an already-fixed issue (`ExecExemplarPackage.report.md:5-7`), so no authorization exists to
  record.
- `ExecExemplarPackage.claim_checklist.md:29-38` names three residual operator gates
  (submission, prior-submission, reviewer distinctness). **Scope authorization / grant existence
  is not among them** — the one field a reader would take as "in scope, cleared to submit" has no
  gate behind it.
- `ScribeKnowledgeGate.entry.md` "What the gate does not decide" names the same three — "The
  operator gates: submission, prior-submission, reviewer distinctness." — and says of R-CUSTODIAN
  only that it checks "a non-empty `matched_grant_id` and `scope_signal` exactly
  `NO_SCOPE_OBJECTION`". Nothing says those two are producer-written literals the gate cannot
  verify. The entry's rejected-over-generalization paragraph ("that a `WELL-FORMED` verdict means
  the package is claim-ready or safe to submit") is the right guard and should be kept — but it
  guards *readiness*, not *authorization*, and `NO_SCOPE_OBJECTION` is the word a reader will
  read as the gate's own scope finding.
- The round's lesson already states the true position —
  `ScribeLessonDraft.round-43-lesson.md:94`: "it carries no program policy, no scope statement
  and no reward rubric" — which contradicts an exemplar that records `authorization: PASS`.

Smallest safe correction (three one-line edits, measured green):

1. `status.json`: `hard_gates.authorization` → `"PENDING"`; append the blocker
   `OPERATOR-GATED scope authorization / grant existence — the custodian matched_grant_id values
   are fixture identifiers, not a platform grant`, and the same item to `residual_gates`.
2. `claim_checklist.md`: add that fourth `OPERATOR-GATED` line under "Residual gates".
3. `claim-package-gate.md` "What the gate does not decide": add one sentence — scope
   authorization is not decided: `matched_grant_id` and `scope_signal: NO_SCOPE_OBJECTION` are
   producer-written literals; the gate checks non-emptiness and exact spelling, never that a grant
   exists or that the asset is in a programme's scope.

Measured on a copy of the current exemplar with (1)+(2):

    package=… rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0

`claimable` is already `false` and R-STATUS does not constrain gate values on that branch, so the
correction costs the gate nothing.

## 6. F2 — two `report.md` deliverables disagree; one of them is red (reconcile before landing)

The exemplar was rebuilt mid-wave from CVE-2023-38545 to CVE-2025-9086. Its own files are now
self-consistent and green:

- `ExecSourceCapture.S067.txt` = `7e35413a…`, 3822 B, 109 lines (CVE-2025-9086); the S067 row in
  `ExecRegistryRows.rows.txt` carries the same digest.
- `ExecExemplarPackage.manifest.json` binds `source-capture.txt 7e35413a…` plus three new
  digests, `expected_head_sha256 46b50b67…`.
- `ExecExemplarPackage.report.md` cites only manifest digests → `rules=8 pass=8` (§4).
- `ExecExemplarPackage.source-capture.txt` = `7e35413a…`, byte-identical to the landed capture.

But `ScribeExemplarReport.report.md` (sha `2bd06e41…`, 101 lines) — the seat whose prompt says
its file lands as the exemplar's `report.md` — is still the CVE-2023-38545 text: title at :1,
`Official advisory URL: .../CVE-2023-38545.html` at :4, `content sha256 9103704c…` at :17, and
the old digest `327bc909…` cited in the scope section. Measured with that file in place:

    RULE R-REPORT verdict=fail detail=cited=2,unbound=2
    package=… rules=8 pass=7 fail=1 verdict=DEFECT exit=1

If both land, the exemplar's `rules=8 pass=8` claim fails on its own bytes. That stale copy also
still carries the wording `ScribeExemplarReport.report.md:39` "its affected-version
determination, which is the scope authority this package quotes" — an advisory's affected-version
list is the product range of a flaw, not a programme's scope authority, and the regenerated
`ExecExemplarPackage.report.md:17` already says the honest thing ("Verbatim scope, severity and
affected-version lines").

Smallest safe correction: land `ExecExemplarPackage.report.md` as the exemplar's `report.md`; if
the scribe copy is kept instead, regenerate its digests and byte-count against the landed S067
capture and drop the "scope authority" phrase. Do not land both.

## 7. F3 — the green selftest is env-redirectable (should fix)

`claim-package-check.py:769,775` falls back to `$CLAIM_PACKAGE_SELFTEST` (or a companion file) and
runs it with `sys.executable` (`:778`). Measured:

    $ CLAIM_PACKAGE_SELFTEST=$S/fakeselftest.py python3 gate.py --selftest
    selftest cases=10 failures=0
    rc=0

where `fakeselftest.py` is two lines that print that summary and exit 0. With the variable unset
the same command is fail-closed — `selftest module=… verdict=missing exit=2`. The published
counting command does not set the variable, so this is not a live green-forge today; it is still
an environment-supplied authority over the gate's own evidence. Smallest safe correction: paste
`run_selftest` at the anchor (`:799`) and delete the companion/env branch, or drop only the
`CLAIM_PACKAGE_SELFTEST` arm.

## 8. Not tested here (other seats own these)

The nine defect fixtures and the ten selftest cases (`ExecGateSelftest`, `RevGateFixtures`), the
exemplar's quote-to-capture line fidelity (`CritExemplarReal`), the K1-K19 suite, the gate's
near-token matchers (`CritTokenRead`), and the census/capture-binding/recheck-audit counters. I
did not run `r43-closure.sh` and claim nothing about it. I also did not verify that the
`recheck:` line in the knowledge entry runs under the shell the landing tooling uses
(`set -o pipefail` after `test` is bash syntax).

## 9. Artifact digests at read time (2026-10-28T16:57Z)

    gate       8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6  ExecGateCore.claim-package-check.py (32520 B)
    status     60f06dfebc04e4198999d203f0568dc8b7bde1b3caf96399e135132edf38a9c6  ExecExemplarPackage.status.json
    custodian  db85653db9019d4db5ee3e45930daf2bacc3a4b8270de3c9ee1aa5172ab3ab2b  ExecExemplarPackage.custodian-receipts.json
    checklist  855eb392d404b141dc25fa7efe7e25225dd54b34bb1a8ab452b3cff2304568cc  ExecExemplarPackage.claim_checklist.md (41 lines)
    report     f99e2604eaafd0d2a9cac9ca04ff988d83a67ddf23d1b15340b689164a107144  ExecExemplarPackage.report.md
    manifest   5e296a37ad0bbc16253ab756a2543c579bce864a0af3bcff6bfe20db317fc834  ExecExemplarPackage.manifest.json
    evidence   7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b  ExecExemplarPackage.source-capture.txt
    capture    7e35413a8b4f9648191d2769c06596035213548c2f7ea308184442318f975c8b  ExecSourceCapture.S067.txt (3822 B, 109 lines)
    scribe-rep 2bd06e415ee4e63e1a5499a17826b020621c22633e360ceeb5827c29084f1be0  ScribeExemplarReport.report.md (101 lines)
    lesson     85d222ebf92d58107925f3c2780993448cd5ea0b11328d4ba94265ed75a85d26  ScribeLessonDraft.round-43-lesson.md
    entry      f53109d842b185ed49ca599fda221351caf03df9d3443c5d50c8bb19a0cb5940  ScribeKnowledgeGate.entry.md (38 lines)

## 10. Housekeeping

Scratch was `/fast/scratch/hyaku/kasegi-r43/CritProvinceScope` (TMPDIR bound there, all fixtures
under it); it is removed before this seat yields. Writes: this receipt only. No write outside
scratch, no PATH-directory write, no fleet-root or sibling-lane write (the two sibling reads were
read-only `PROVINCE.md`/`PROTOCOL.md` text). No pacman, no tool installs (none were needed), no
mutating git/jj command — the fixtures were plain directories, not git repos. Network: none from
this seat; the captures and digests above were produced by the wave seats, not re-fetched.
