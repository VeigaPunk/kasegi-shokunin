# RevEntryQ — independent Q1–Q10 review of `corpus/knowledge/vendor-third-party-finding-coordination.md`

- Seat: `RevEntryQ` (round 31, wave 2, falsify). Leaf; no subagents; no background jobs.
- Answering model actually run: `opencode-go/deepseek-v4.1-flash` (workstation config route table; no model passed by this seat).
- Review target (not written by this seat): `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/vendor-third-party-finding-coordination.md` (160 lines).
- Bar read in full: `corpus/QUALITY.md` (Q1–Q10, R1–R17). Evidence base: the pinned capture `corpus/source-snapshots/round-31/S048.txt`, `corpus/source-snapshots/round-31/manifest.json`, `corpus/SOURCES.md`, `corpus/README.md` (frontier rows), `corpus/instruments/source-recheck.py`, wave-1 receipts `ExecCapManifest.md`, `ScoutF15Sweep.md`, and the entries the target cites (F06/F10/F11 files).
- Writes: this receipt only. No instrument, entry, registry, README, SKILL, PROVINCE, or git/jj mutation touched. No pacman/uv/npx install run (nothing needed).
- Independence: findings below come from the bytes and the instruments. The author's self-review `.ufo/waves/round-31/wave1/ExecEntryF15.md` was read only after the checks below, and only to test whether it already answered them; it does not address F1.

## §1 Commands run and their output

### 1.1 The entry's own recheck line — extraction, `bash -n`, lane cwd, foreign cwd (Q10/Q7)

```
$ E=corpus/knowledge/vendor-third-party-finding-coordination.md
$ CMD=$(grep -m1 '^recheck: ' "$E" | sed 's/^recheck: //; s/[[:space:]]*#.*$//')
$ printf 'CMD=[%s]\n' "$CMD"
CMD=[cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048]
$ bash -n /tmp/reventryq_recheck.sh; echo "bash_n_exit=$?"
bash_n_exit=0
$ ( cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && bash /tmp/reventryq_recheck.sh; echo "lane_exit=$?" )
S048:sha256 OK
S048:Q1 OK occurrences=1
S048:Q2 OK occurrences=1
S048:Q3 OK occurrences=1
S048:Q4 OK occurrences=1
S048:Q5 OK occurrences=1
S048:Q6 OK occurrences=1
S048:Q7 OK occurrences=1
S048:Q8 OK occurrences=1
lane_exit=0
$ ( cd / && bash /tmp/reventryq_recheck.sh; echo "root_exit=$?" )
S048:sha256 OK
S048:Q1 OK occurrences=1
S048:Q2 OK occurrences=1
S048:Q3 OK occurrences=1
S048:Q4 OK occurrences=1
S048:Q5 OK occurrences=1
S048:Q6 OK occurrences=1
S048:Q7 OK occurrences=1
S048:Q8 OK occurrences=1
root_exit=0
```

The run's output carries no `normalized=markup-whitespace` token: every one of the 8 records is also a raw substring, so the raw branch `source-recheck.py:201-203` emits `occurrences=` alone; `normalized=` is emitted only on the normalize-only branch at `source-recheck.py:204-209`. The declared normalization is in the manifest purpose and in the entry's §Scope (Q8 below).

### 1.2 `source-recheck.py --selftest` — the fail-closed controls (Q7)

```
$ python3 corpus/instruments/source-recheck.py --selftest; echo "selftest_exit=$?"
SELFTEST clean PASS expected-exit=0 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST corrupt PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256 observed-ids=S900:sha256
SELFTEST missing-source PASS expected-exit=2 observed-exit=2 expected-ids=S900:source observed-ids=S900:source
SELFTEST missing-manifest PASS expected-exit=2 observed-exit=2 expected-ids=manifest observed-ids=manifest
SELFTEST stem-mismatch PASS expected-exit=1 observed-exit=1 expected-ids=S901:manifest observed-ids=S901:manifest
SELFTEST double-occurrence PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST double-occurrence-anchored PASS expected-exit=0 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST double-occurrence-out-of-range PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST double-occurrence-broken PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST quote-absent PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
selftest cases=10 failures=0
selftest_exit=0
```

`corrupt` (`source-recheck.py:334-335`) and `missing-source` (`:338`) are the required failing controls; the missing-manifest case makes the entry's recheck fail closed when the base is absent.

### 1.3 Every falsifiable check the entry states, re-run from the entry's exact commands (Q5) and the §Honest-limit counts

```
$ C=corpus/source-snapshots/round-31/S048.txt
$ grep -cE '^(Internal Microsoft engineers|External reports to the Microsoft Security Response Center \(MSRC\)|Internal research projects):' $C   → 3
$ grep -c 'in three ways' $C   → 1
$ grep -ci 'only' $C   → 0
$ grep -c 'as a coordinator of vulnerabilities that affect multiple vendors' $C   → 1
$ grep -ciE '90[ -]day|deadline|embargo|timeline' $C   → 0
$ grep -ci '@microsoft' $C   → 0
$ sed -n '28,35p' $C | grep -ci bounty   → 0
$ grep -ci bounty $C   → 1
$ grep -c 'affected vendor' $C   → 2
$ grep -c 'CERT/CC' $C → 0 ; grep -c 'JPCERT' $C → 0 ; grep -c 'IPA' $C → 0
$ grep -ci 'http' $C   → 0
$ grep -in cert $C     → 48:Certified Refurbished
$ grep -in bounty $C   → 15:Microsoft Bug Bounty Programs
$ grep -c 'third-party product of affects both' $C   → 1
```

Every number in the entry's FC-1…FC-5 and §Honest limit is reproduced exactly. `grep -c 'third-party product of affects both'` → `1` (the sic typo at L33).

### 1.4 The entry's residual sweep, run as written

```
$ for t in MSVR MSRC 'research programme' 'coordinator of vulnerabilities'; do grep -rli -- "$t" corpus/knowledge/*.md; done
== MSVR
corpus/knowledge/vendor-third-party-finding-coordination.md
== MSRC
corpus/knowledge/vendor-third-party-finding-coordination.md
== research programme
corpus/knowledge/vendor-third-party-finding-coordination.md
== coordinator of vulnerabilities
corpus/knowledge/vendor-third-party-finding-coordination.md
```

Exactly one knowledge file per term — the entry itself. The sweep is reproducible and the residual is real for those four terms.

### 1.5 Capture pin and the entry's cited numbers (Q3 "numbers are copied")

```
$ wc -c corpus/source-snapshots/round-31/S048.txt   → 3755
$ wc -l corpus/source-snapshots/round-31/S048.txt   → 97
$ sha256sum corpus/source-snapshots/round-31/S048.txt
2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55
```

Matches entry L152-L153 and manifest `sha256`. The 2026-10-25T23:29:53Z fetch time is grounded in `wave1/ExecCapManifest.md:13` (`utc=2026-10-25T23:29:53Z`).

### 1.6 Occurrence count of every distinct S048 quote in the entry, under the instrument's own `normalize()`

```
L29 purpose:  words=23 occurrences=1
L34 scope:    words=14 occurrences=1
L32 route1:   words=19 occurrences=1
L33 route2:   words=6  occurrences=1
L34 route3:   words=14 occurrences=1
L35 CVD:      words=11 occurrences=1
role1:        words=11 occurrences=1
role2:        words=11 occurrences=1
role3:        words=9  occurrences=1
L31:          words=10 occurrences=1
```

Max quote length 23 words (L29). Two of these ten (L29 purpose, L34 scope) are **not** in the manifest's 8 assertions — see F2.

### 1.7 Documentation-only scan of the entry (Q6)

```
$ grep -no 'https\?://[^ )]*' <entry>
2:https://www.microsoft.com/en-us/msrc/msvr
$ grep -nE 'f97e6b1c|vault|token|session|Bearer|curl |wget |POST |<u>|op://' <entry>
160:  session or private URL.
```

One public documentation URL; the per-request `Trace Id` value on capture L2 (`f97e6b1c…`) does **not** appear in the entry; the only `session` match is the entry's own negative declaration. No probe/login/submission instruction.

### 1.8 Manifest record binding (Q9)

```
"id": "S048", "path": "S048.txt", sha256 2001ad77…e55, 8 quotes, no anchor on any
```

`source-recheck.py:123-126` enforces `Path(path).stem == source_id` (B1); the run above passes it and prints `occurrences=1` per quote, so the exactly-once branch, not the anchor branch, is the binding.

### 1.9 Registry and tier (Q2)

`corpus/SOURCES.md:54`: `| S048 | Microsoft Security Vulnerability Research (MSVR) — https://www.microsoft.com/en-us/msrc/msvr | docs | A | … | mined | 2026-10-25 | 180d | corpus/knowledge/vendor-third-party-finding-coordination.md |`.
Other cited rows are all tier A: S018 `SOURCES.md:24`, S039 `:45`, S040 `:46`, S041 `:47`. `grep -lE '^source: S048 ' corpus/knowledge/*.md` → exactly one file (the entry).

## §2 Q1–Q10 table

| id | verdict | line(s) | quote / evidence |
|---|---|---|---|
| Q1 | pass | 1–4 | L3 `verified-at: 2026-10-25`; L2 `source: S048 — https://www.microsoft.com/en-us/msrc/msvr` (id + URL + section + `capture …:28-35` + per-line anchors); L4 `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py`. The three header lines sit directly under the H1 (L1). Cadence `180d` lives in the registry cell (`SOURCES.md:54`), consistent with the lane: 0 of 44 `recheck:` lines in `corpus/knowledge/*.md` carry a cadence token. |
| Q2 | pass | 2; SOURCES.md:54 | Load-bearing claims rest on S048, `tier A`, `opened 2026-10-25` (admitting round), `status mined`. Contrast citations S018/S039/S040/S041 are all tier A (`SOURCES.md:24,45,46,47`); no tier-C row appears, so none is sole support. |
| Q3 | **fail** | 84–87 | `F10's thesis is a vendor's standing statement about the handling of findings in its *own* products` (16 words). No verbatim quote and no exact location is given for this load-bearing warrant of addition 3, and the claim is refuted by F10's own committed row `cisco-jpcert-partner` (`vendor-disclosure-policy-commitments-crosswalk.md:49`, quote `"Japan Computer Emergency Response Team (JP-CERT)"`, S040 L185-L193) which the entry itself cites at L70-L72 as a cross-vendor handling statement. All ten sourced S048 quotes are ≤25 words, verbatim and exactly-once (§1.6); numbers are copied (§1.5). Detail: F1. |
| Q4 | pass | 9–11, 17, 41 | L9 `Every statement below is Microsoft's own description of its own programme`; L11 `not a rule about vendors in general`; claim headings L17/L41 read `Microsoft's MSVR states…`. The F06/F11 absence claims are framed as statements about those entries, not about vendors. |
| Q5 | pass | 119–123, 125–148 | Five runnable FC commands (all reproduced in §1.3) plus five rejected over-generalizations with reasons, e.g. L127 `Every large vendor runs such a programme.` Rejected. FC-1 and FC-5 name the package error a reader can refute. |
| Q6 | pass | 2, 111, 158–160 | L158-L159 `It instructs no probing, scanning, login or submission against any target`; one public documentation URL (§1.7); no credential/session material; the capture's Trace Id value is not carried. |
| Q7 | pass | 4 | Command, not prose; exit 0 from both cwds; output names the pin (`S048:sha256 OK`) and each assertion with `occurrences=1`; note says `a captured-source comparison, not a fresh network verification`. Fail-closed controls: `corrupt` exit 1, `missing-source`/`missing-manifest` exit 2 (§1.2). |
| Q8 | pass (residual) | 155–157 | `capture markup stripped, whitespace collapsed`; manifest purpose declares the same normalization. The entry never quotes converter markup (`<u>` absent, §1.7). Residual: this record's run prints `occurrences=1` but no `normalized=` token because all 8 quotes are raw substrings — the token exists only on the normalize-only branch (`source-recheck.py:204-209`). |
| Q9 | pass (residual) | manifest record | `path` `S048.txt`, `id` `S048` (stem equality enforced at `source-recheck.py:123-126`); 8 quotes, every one `occurrences=1`, no anchor required; the check prints the observed count. Residual: the entry carries ten S048 quotes; the L14 and L32 quotes are unique (measured §1.6) but unasserted — F2. |
| Q10 | pass | 4 | `bash -n` exit 0; exit 0 from the lane root **and** from `/`; one command with the `cd <lane> &&` prefix and the human note after `#`. |

## §3 Findings, by severity

### F1 — HIGH — Q3: addition 3's warrant sentence is unlocated and refuted by F10's committed bytes

Entry L84-L87:

> `3. **A published programme about *other vendors'* products as a corpus object.** F10's thesis is a vendor's standing statement about the handling of findings in its *own* products; S048 is a vendor's standing statement about its routes into *other* vendors' products.`

- No quote and no location are given for `F10's thesis is …`; every other cross-entry claim in the entry carries a file and line (L63-L72, L89-L91).
- The claim is false as written against F10: `vendor-disclosure-policy-commitments-crosswalk.md:21` is a four-vendor matrix (`S040 Cisco | S036 Cybozu | S038 GMO Pepabo | S039 Hitachi`), and its rows `cisco-jpcert-partner` (`:49`, S040 L185-L193) and `hitachi-coordination` (`:66`, quote `"脆弱性対策の調整機関であるCERT/CCやJPCERT/CCの協力を得て"`, L520) are cross-vendor handling commitments. The entry's own L66-L72 says exactly that ("F10's vendor rows … keep coordination outside the vendor"), so the entry contradicts itself within 18 lines.
- The frontier row's own teaching for F10 (`corpus/README.md:211`) is `A vendor's published policy is a standing first-party statement, not a programme` — the supported distinction is **programme-ness**, not own-products scope.
- Effect on the claim: none beyond wording. The F15 residual is carried by addition 1 (route 3, internal research) and addition 2 (vendor as self-named coordinator), which is precisely the credit `wave1/ScoutF15Sweep.md` §"exact residual" identified ("expansion credit requires foregrounding route 3 (internal research) + the self-declared coordinator role"). Fix is one bullet: replace the `own products` clause with the README:211 ground and give F10's file+line, or drop addition 3.

### F2 — LOW — Q7/Q9 coverage: "every quote exactly-once" is broader than the assertion set

L4 note: `# 8 assertions, every quote exactly-once in the pinned capture; a captured-source comparison, not a fresh network verification`. The entry carries ten distinct S048 quotes (§1.6); the manifest asserts eight. The two unasserted are the programme self-description (L14) and route 3's scope (L32); both are exactly-once under the instrument's `normalize()` (measured by this seat), and the sha256 pin still binds the capture bytes, so the exposure is silent drift only if a future manifest re-pins mutated bytes. §Scope is accurate (`eight quotes`, L155); the L4 note's "every quote" is not. Fix: add two assertions (ids `Q9`, `Q10`) or reword L4 to `8 assertions (of the entry's ten S048 quotes)`.

### F3 — LOW — precision: "F10's vendor rows both"

L66-L67: `F10's vendor rows both keep coordination outside the vendor`. F10 spans four vendor columns (`crosswalk:21`) and F10a admits S036-S039+S037 (`vendor-disclosure-policies-as-corpus-objects.md:3-6`); the sentence enumerates only Hitachi and Cisco. True for the two rows that address cross-vendor findings; over-scoped as "F10's vendor rows" (Pepabo rows state no coordination at all, so they cannot "keep coordination outside the vendor"). Fix: `the two F10 rows that address cross-vendor findings both route …`.

### F4 — LOW — source over-read: "standing" internal-research route

L76: `1. **A standing internal-research route into other vendors' products.**` The capture qualifies route 3: `As time and resources permit, Microsoft performs its own vulnerability analysis and research` (L34; occurrence 1). "Standing" converts a conditional activity into a durable route; the qualifier is not carried in this bullet. The entry's Claim 1 table does quote the route body, so the reader can recover it. Fix: `a conditional internal-research route` or quote the qualifier.

### F5 — TRIVIAL — route-2 paraphrase narrows the trigger

L35-L36 reads `an external report filed against a Microsoft product that the reporter believes also affects a third-party product (or affects both)`; L33 says `an external researcher will report an issue that they believe affects a Microsoft product` — "filed against" narrows the page's "affects". The table row at L27 keeps the exact text, so the risk is low; the interpretation paragraph is not a quote.

## §4 The sentence that most risks being an over-generalization

Entry L84-L87 (16 words for the warrant clause):

> `F10's thesis is a vendor's standing statement about the handling of findings in its *own* products`

Reason it is the top risk: it generalizes a four-vendor matrix into a single thesis and adds an `own products` scope the bytes do not carry, while the same entry, 18 lines earlier, cites F10's cross-vendor routing row as evidence. A critic needs one grep (`vendor-disclosure-policy-commitments-crosswalk.md:49`) to refute it. Runner-up: L76 `A standing internal-research route into other vendors' products` (F4) — a source over-read rather than a corpus over-generalization.

## §5 Verdict

**REFUSE** — on **Q3 only**. Q1, Q2, Q4, Q5, Q6, Q7, Q8, Q9, Q10 pass on the evidence in §1–§2.

Reasons:
1. Q3 requires each load-bearing claim to carry a verbatim quote of ≤25 words with its exact location. Addition 3's warrant (L84-L87) carries neither, and it is the only claim in the entry whose positioning is not reproducible from a stated capture/file+line.
2. The sentence is not merely under-cited; it is refuted by committed bytes (`crosswalk:49`, `:66`; S040 L185-L193) that the entry itself cites, so admitting it would put a self-contradicting novelty warrant into the corpus.

Minimal fix for re-review (one bullet, no other change): replace L84-L87's `own products` thesis with the README:211 ground — "F10 holds the vendor's own published policy objects, not a programme" — citing `vendor-disclosure-policy-commitments-crosswalk.md:21-67`; keep addition 3's second clause (S048 is a published research programme about other vendors' products), which is true. Optionally fold F2 (`Q9`/`Q10` assertions) in the same edit. If the L1 instead holds that Q3 binds source claims only, the entry still needs F1 as an appended correction and F2/F4 as cheap wording fixes; I do not edit the entry (outside this seat's write scope).

## §6 Residual risk and verification gaps

- **Source↔upstream is not re-verified here.** My review compares entry ↔ pinned capture ↔ instrument. I did not re-fetch `https://www.microsoft.com/en-us/msrc/msvr` (documentation-only seat; the entry states the same limit at L155-L157). The capture's authenticity rests on the wave-1 receipt `ExecCapManifest.md:13` (HTTP 200, 81802 B fetched, 3755 B snapshot) and `RevSourceBar.md` headers, not on this seat.
- **Q8 token gap.** This record's receipt does not print `normalized=markup-whitespace`; the declaration lives in the manifest purpose and entry §Scope. If a future verifier requires the literal token in the receipt, add an assertion whose quote is only markup/whitespace-normalized, or change the instrument to always print the normalization it applied.
- **Manifest has no explicit `captured_at` field.** The 23:29:53Z time is receipt-grounded (`ExecCapManifest.md:13`), not manifest-grounded; a reader of the manifest alone cannot recover it.
- **Two unasserted quotes.** Measured exactly-once by this seat under the instrument's `normalize()`; not bound by the committed manifest (F2).
- **Instrument semantics checked, not mutated.** I read `source-recheck.py` for the stem/normalization/anchor branches; limb-level mutation of this instrument is C1's ledger work (`RA-*`/`SR-*` rows), not this seat's.
- Evidence commands are all read-only; the only file written by this seat is this receipt.
