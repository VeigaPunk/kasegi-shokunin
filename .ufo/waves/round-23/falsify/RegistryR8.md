# RegistryR8 — falsification of R8 against `corpus/SOURCES.md`

Seat: `L1Kasegi23.RegistryR8-2` (falsify wave, read-only). Target: verify R8
(`corpus/QUALITY.md:50`, grounded in `corpus/lessons/round-23.md` M5) against the landed
registry bytes. This report is the only file written. No production file, lane tree, git/jj
index or state was modified; no commit, push, admission or score movement is claimed.

## 0. What R8 actually requires (normative text, read before testing)

`corpus/QUALITY.md:50`:

> R8 | Source rows' immutable fields stay immutable: a corrected anchor or broadened scope
> in a registry row is a new row beginning "supersedes S### —". A wrong quote location in a
> filed lesson is instead an appended R9 erratum, not duplicate source authority. Log every
> status/recheck/used-by old→new change.

The governing contract is stricter and machine-shaped —
`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` (frozen 2026-10-19),
rule 2, lines 49–51:

> **Append-only.** Only `status`, `recheck` and `used-by` change in place, and each change is
> logged old→new in the round lesson. A correction is a new row whose `teaches` opens
> `supersedes S0NN —`.

and rule 1, lines 43–47:

> The round lesson's `## Gate` records, for every new row, the URL, the access date, and a
> ≤25-word quote with its location grounding `teaches`.

So R8 decomposes into five testable propositions: (P1) no pre-existing row's immutable
fields changed in place; (P2) corrected/superseding rows are *added* rows whose `teaches`
opens `supersedes S0NN —`; (P3) every in-place `status`/`recheck`/`used-by` change has an
old→new record in the round lesson; (P4) superseded rows are not rewritten; (P5) each new
row has a Gate record whose quote grounds its `teaches`.

## 1. Method and exact commands

No `lsp` device is mounted in this seat, and `corpus/SOURCES.md` is a plain Markdown data
table with no language server, so there is no semantic server to consult. Verification is
therefore a **structural field parser** over the table plus git-object comparison — not a
grep-as-proof. Grep is used only to locate lines and to reproduce the contract's own census
one-liners verbatim. Working scratch: `/tmp/kasegi-r23-falsify-RegistryR8`.

Repository state when the registry was first measured (`git status --porcelain`): only
`M LOG.md`. Sibling seats subsequently wrote other corpus files (`instruments/*`,
`knowledge/*`, `source-snapshots/round-23/manifest.json`), so a re-run now shows those as
dirty. **`corpus/SOURCES.md` itself was never dirty** — re-checked clean at report time
(`git status --porcelain corpus/SOURCES.md` → empty) — so every registry measurement here is
against released lane-tip bytes, not against a sibling's in-flight edit.

### 1.1 Whole-registry field diff, base vs working tree

Base revision per `.ufo/waves/round-23/claims.json` is `922a4dde`. `c8b719d` is an ancestor
of `922a4dd` and `git show c8b719d:corpus/SOURCES.md` is byte-identical to
`git show 922a4dd:corpus/SOURCES.md`, so the base object is unambiguous.

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 - <<'EOF'
import subprocess
base = subprocess.run(["git","show","922a4dd:corpus/SOURCES.md"],capture_output=True,text=True).stdout
head = open("corpus/SOURCES.md").read()
def rows(t):
    d={}
    for ln in t.splitlines():
        s=ln.strip()
        if s.startswith("| S") and len(s)>3 and s[3].isdigit():
            d[[c.strip() for c in s.strip("|").split("|")][0]]=[c.strip() for c in s.strip("|").split("|")]
    return d
b,h=rows(base),rows(head)
cols=["id","source","kind","tier","scope","anchor","teaches","status","opened","recheck","used-by"]
print("base rows",len(b),"head rows",len(h))
for k in sorted(b):
    for i,c in enumerate(cols):
        if b[k][i]!=h[k][i]: print(f"CHANGED {k}.{c}\n  old={b[k][i]!r}\n  new={h[k][i]!r}")
print("added:",[k for k in sorted(set(h)-set(b))])
EOF
```

Output (verbatim):

```
base rows 27 head rows 30
CHANGED S018.status
  old='queued'
  new='mined'
CHANGED S018.used-by
  old='—'
  new='corpus/knowledge/multiparty-vulnerability-coordination.md'
total field changes among pre-existing rows: 2
added: ['S028', 'S029', 'S030']
```

This is the single most load-bearing measurement in this report: **across all 27 pre-existing
rows, exactly two fields changed, both contract-mutable** (`status`, `used-by`). Zero
immutable fields (`source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `opened`) changed;
zero rows removed.

### 1.2 `teaches` cell is column 7 and opens with the exact required token

```sh
for id in S028 S029 S030; do echo -n "$id: "; grep "^| $id " corpus/SOURCES.md | awk -F' \| ' '{print $7}'; done
```

```
S028: REJECTED: S006 already names the correct enablement heading; the error is in the filed r22 Gate, not its source row; flip: a distinct correction to an immutable registry field is evidenced.
S029: supersedes S024 — official Article 14 text distinguishes vulnerability and incident reporting clocks; Article 71 applies Article 14 from 11 September 2026.
S030: supersedes S022 — use current 4.2.0 requirements and section numbering; distinguish assignment scope, security impact and independently fixable vulnerabilities.
```

Header at `corpus/SOURCES.md:9` is `| id | source | kind | tier | scope | anchor | teaches |
status | opened | recheck | used-by |`, so field 7 is `teaches`. Both superseding rows open
with `supersedes S0NN —` (U+2014) and nothing precedes it.

### 1.3 Superseded rows untouched (byte identity, not "no diff hunk looked relevant")

```sh
for id in S022 S024 S006; do a=$(git show 922a4dd:corpus/SOURCES.md | grep "^| $id "); b=$(grep "^| $id " corpus/SOURCES.md); [ "$a" = "$b" ] && echo "$id IDENTICAL" || echo "$id CHANGED"; done
```

```
S022 IDENTICAL
S024 IDENTICAL
S006 IDENTICAL
```

### 1.4 Contract census, run verbatim from the lane root

The contract ships its own census block (lines 70–81); reproduced unmodified:

```sh
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md          # rows
awk -F'|' '... NF!=13 {n++} END{print n+0}' corpus/SOURCES.md                  # malformed
awk -F'|' '... {t=$5; ... n[t]++}' corpus/SOURCES.md                           # tier
awk -F'|' '... {s=$9; ... n[s]++}' corpus/SOURCES.md                           # status
awk -F'|' '... {i=$2; ... print i}' corpus/SOURCES.md | sort | uniq -d         # dup ids
awk -F'|' '... enum violations ...' corpus/SOURCES.md
awk -F'|' '... mined used-by ...' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
```

Output:

```
== rows ==            30
== malformed ==       0
== tier ==            A=28 C=2
== status ==          mined=18 queued=9 rejected=3
== dup ids ==         (empty)
== enum violations == (empty)
== mined used-by missing paths == (empty)
```

Every number in `corpus/lessons/round-23.md:209-212` ("27 → 30 (tier A=28, C=2; status mined
18, queued 9, rejected 3; 18 rows carry `used-by`)") reproduces exactly. Independent count of
non-`—` `used-by` cells: **18**.

### 1.5 The lessons' own census command resolves and exits 0

The command at `corpus/lessons/round-23.md:207` is `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kasegi`. That script does **not** exist under
`kasegi-shokunin/scripts/` (there is no `scripts/` directory in the lane); it lives at the
fleet root as `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, which is consistent
with the explicit `--root` flag. Run from the fleet root:

```sh
cd /home/vgpnk/Projects/shokunin && ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "EXIT=$?"
```

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
EXIT=0
```

Exit 0 with exactly the two claimed W04 warnings on S028 and S029 — the lessons' census
claim is true, not merely asserted. (Recorded as a **cleared check**: I initially expected a
missing-script defect because the path does not resolve from the lane root; the `--root` flag
makes the fleet-root location correct, so this is not a finding.)

## 2. Verdict on the four assigned propositions

| # | Proposition | Verdict | Basis |
|---|---|---|---|
| P1 | S029/S030 are new rows opening `supersedes S###` in `teaches`, not edits of S024/S022 | **TRUE** | §1.1 added = `[S028, S029, S030]`; §1.2 exact prefixes; §1.3 S022/S024 byte-identical |
| P2 | S018 `status`/`used-by` reflect its admitted entry | **TRUE at HEAD** | §1.1 two changes only; `used-by` = the F06 entry path; F06 cites `S018` at `corpus/README.md:200`. See F-3 for the causal caveat |
| P3 | S022/S024 remain `queued` and unmodified | **TRUE** | §1.3 IDENTICAL; both cells read `queued` at `SOURCES.md:28`/`:30` |
| P4 | Every status/recheck/used-by change has an old→new lesson record | **TRUE for the registry; one misclassification** | `round-23.md:198-200` logs all three S018 fields; F-1 flags the S028 row |
| P5 | No immutable field changed in place | **TRUE** | §1.1 — exactly 2 mutable fields changed across 27 rows |

R8 holds on the registry bytes. The findings below are defects in the *record surrounding*
the registry (round-lesson classification and Gate-quote binding), not in `SOURCES.md`.

## 3. Findings (severity order)

### F-1 (Low–Medium) — the round lesson logs the added row S028 as an in-place `rejected → rejected` no-op

`corpus/lessons/round-23.md:204`:

```
| S028 | status | rejected | rejected (duplicate-row proposal; flip unchanged) |
```

S028 did not exist before this round. Proof:

```sh
git show 922a4dd:corpus/SOURCES.md | grep -c "^| S028 "
```
```
0
```

and §1.1 returns `added: ['S028', 'S029', 'S030']` with row count 27 → 30. So the `old`
cell `rejected` refers to a row that had no prior state. Consequences:

- It contradicts the prose two paragraphs above, `round-23.md:192`: "Opened rows this round
  are S018, S029, S030 and S028 (rejected)".
- It contradicts the ledger's own count at `round-23.md:209` ("registry rows 27 → 30") —
  an auditor counting "(new row)" entries in the Gate table finds 2, not 3.
- It is inconsistent with S029/S030, logged one row earlier as `| S029 | (new row) | — | ... |`.

Contract rule 2 governs *in-place* changes; an added row is not one. The record should read
`| S028 | (new row) | — | rejected, docs/A, duplicate-row proposal; flip unchanged |`.

Scope limit: this is a classification defect in the lesson, not a registry defect. The
registry's own S028 row is correct and contract-compliant (starts `REJECTED: <reason>; flip:
<...>` per contract lines 34–35), and `round-23.md:35` does carry S028's rule-1 Gate record
(URL, 2026-10-20, 9-word quote, location).

### F-2 (Low–Medium) — for both superseding rows the Gate binds a quote that leaves the supersession-defining clauses unquoted

Contract rule 1 (`SOURCES-CONTRACT-v1.md:43-47`) requires the Gate, "for every new row", to
carry "a ≤25-word quote with its location grounding `teaches`". Measured against `teaches`:

**S029.** `teaches` (`SOURCES.md:35`) asserts three things: (a) the official text
*distinguishes* vulnerability and incident reporting clocks, (b) Article 71 applies Article 14
from 11 September 2026, plus the supersession. The Gate quote (`round-23.md:36`) is
Art 14(2)(c): "no later than 14 days after a corrective or mitigating measure is available".
That grounds one vulnerability-track clock. It does not ground the *distinction* (which needs
the 14(4) incident clock) and does not ground the 11 September 2026 application date.

**S030.** `teaches` (`SOURCES.md:36`) asserts current 4.2.0 requirements *and section
numbering*, and three substantive distinctions (assignment scope, security impact,
independently fixable). The Gate quote (`round-23.md:37`) is rule 4.2.11 on separate CVE IDs
for independently fixable vulnerabilities — it grounds the third distinction only, and grounds
neither "section numbering" nor assignment-scope/security-impact.

This matters specifically for R8, whose stated hazard is **duplicate source authority**: a
Gate-only auditor cannot distinguish "S029/S030 are genuinely different, newer sources" from
"the same source re-filed", because the quotes that carry the difference are absent from the
Gate. The evidence does exist — `corpus/source-snapshots/round-23/manifest.json` asserts
`art71-article-14-start`, `art14-4c-incident-final-report`, `rule-3-1-1-scope-definition`,
`rule-4-1-2-security-impact` — so this is a *binding* gap between the Gate and the manifest,
not a missing quote. Falsifier: show that `teaches` for S029/S030 is single-clause, or that
the Gate's one quote is intended by the contract to be representative rather than grounding.

Overlap risk: `S029Quotes.md` validates the six *entry* quotes byte-exactly (its finding 1) and
does not examine the Gate↔`teaches` binding. This finding is complementary, and I flag it as
possibly intersecting the `EntryQuoteBinding` seat's scope.

### F-3 (Low) — the registry transition predates the admission it is said to reflect, so it is not independent evidence of admission

`corpus/SOURCES.md` was **not** modified by the round-23 admission commit:

```sh
git diff 8bf9807..HEAD -- corpus/SOURCES.md    # (empty)
git show --stat 953c278 | grep SOURCES         # (no match)
```

Every registry byte under test landed in `8bf9807` (2026-10-20), whose message is
`checkpoint(r23): archive developed corpus and local tooling; policy-paused, unadmitted, no
task resumption`. At that checkpoint the frontier table still said:

```sh
git show 8bf9807:corpus/README.md | grep -E "^\| F0[6-8] "
```
```
| F06 | Multi-party CVD — FIRST guidelines v1.1 | queued | — | S018 | ... |
| F07 | CVE CNA operational rules | queued | — | S022 | ... |
| F08 | EU Cyber Resilience Act reporting duties | queued | — | S024 | ... |
```

So for five days the registry asserted S018/S029/S030 `mined` with `used-by` paths while the
frontier marked those same surfaces `queued | —`. R8's "now reflect its admitted entry" is
true at HEAD, but the direction of support is one-way: the registry flip cannot be offered as
evidence that F06–F08 were admitted, because it preceded the admission and would have read
identically had admission never happened. This is a verifiability caveat on any argument that
uses the registry to corroborate C2.

### F-4 (Low, residual — sibling-owned) — S022's `used-by` is stale; reproduced here only for scope completeness

`SOURCES.md:28` still reads `queued | ... | — |`, yet the round-23 entry
`corpus/knowledge/cna-assignment-and-vulnerability-rules.md:17` relies on the 4.1.0→4.2.0
movement reproduced from the 4.1.0 text. `used-by` is contract-mutable (§0, rule 2) and any
change must be logged; it was not changed. **This is already filed by
`Q2TierSupport.md` F-4** and is not claimed here as a new finding — recorded so the R8
proposition P4 sweep is visibly complete rather than silently narrowed.

### F-5 (Informational, out of R8 scope) — S030 entry header and registry anchor disagree on section depth

`corpus/SOURCES.md:36` anchor: "sections 3.1, **3.2.4.2**, 4.1 and 4.2, especially 4.2.11
page 15". `corpus/knowledge/cna-assignment-and-vulnerability-rules.md:2`: "sections 3.1,
**3.2.4**, 4.1 and 4.2". The same entry's body (`:33`) cites "section 3.2.4.2, pages 9–10",
and `corpus/source-snapshots/round-23/S030.txt:108-110` contains both the parent heading
`3.2.4 Availability and Responsiveness` and the subsection `3.2.4.2`. The registry anchor is
the precise one; the *entry header* is the inconsistent artifact. This is **not** a registry
defect and R8's append-only rule does not reach it (the registry anchor should not be
"corrected" to match a looser header). Noted because the anchor is immutable, so any future
divergence here can only be fixed by minting another superseding row.

## 4. Checks that passed (tested, no defect — recorded to bound the search)

- Whole-registry field diff: 2 changes, both mutable; 0 removals; 3 additions (§1.1).
- `teaches` prefixes exact, em dash U+2014, no leading text (§1.2).
- S022/S024/S006 byte-identical to base (§1.3).
- Contract census: 0 malformed rows, 0 duplicate IDs, 0 enum violations, 0 `kind`/`tier`
  violations including the `community` never-A rule, 0 missing `mined` `used-by` paths (§1.4).
- Ledger counts (27→30; A=28/C=2; mined 18/queued 9/rejected 3; 18 `used-by`) reproduce
  exactly, independently of the ledger's commands (§1.4).
- `scripts/sources-census.sh validate` exits 0 with exactly the two disclosed W04 duplicate-URL
  warnings (S028↔S006, S029↔S024) (§1.5).
- `recheck` values (`on-release` for S029/S030, `180d` unchanged for S018) are in the
  contract's permitted vocabulary (ISO date, `90d`, `180d`, `on-release`).
- S018's `mined` status is consistent with the contract's definition (`mined` = cited by ≥1
  path in `used-by`) — its `used-by` is a real existing path, and the census' missing-path
  check is empty.
- R8's grounding in M5 (`QUALITY.md:50`) is legitimate: M5 is the origin case (S006 row
  already correct, S028 rejected as duplicate authority). I initially treated the absence of
  S029/S030 from M5 as an evidence-pointer gap and discarded it — the column is "grounded in",
  i.e. the origin case, not a per-round compliance proof.

## 5. Residual risk and verification gaps

1. **No forward marker on S022/S024.** The contract's status vocabulary is exactly
   `queued|mined|rejected` (validated at `SOURCES-CONTRACT-v1.md:78` → §1.4 empty enum
   output); there is no `superseded` state. Consequently the only machine-visible
   supersession signal is one-directional, in S029/S030's `teaches`. A consumer enumerating
   the 9 `queued` rows receives S022/S024 with their pre-supersession scope/anchor text
   (`S024`: "Article 14 wording not yet verified against EUR-Lex ... re-open before mining")
   and no pointer forward. This is contract-compliant but is a discoverability gap that a
   future round could close only by a new row or a logged `used-by` update (F-4).
2. **This report cannot validate the admission itself.** Per F-3 the registry predates
   `953c278`. Whether F06–F08 *should* be admitted is the closure's judgment; I measured only
   whether the registry record is append-only and honestly logged.
3. **Round-lesson edits are uncommitted-adjacent.** `corpus/lessons/round-23.md` is committed,
   but the working tree carries `M LOG.md`. I did not evaluate `LOG.md`; if it restates the
   registry transition counts it could inherit F-1.
4. **Two records of the S018 transition exist** (`round-23.md:62-66` prose and `:196-204`
   table). Both agree; I checked them against each other rather than trusting either.

## 6. Scope limits

- Read-only. Only this file was written. No mutation testing was needed or performed: the
  claims under test are record/byte-identity claims, so contradicting them requires only
  reading base and head objects, not mutating copies.
- I verified *registry record integrity* — column identity, append-only behaviour,
  old→new logging, census counts, and Gate binding — not the substantive correctness of the
  CRA/CNA/FIRST law or policy, and not whether the C2 entries' claims are true. Those are the
  quote scouts' and the closure's scope.
- Base is `922a4dd` per `claims.json`; `c8b719d` is an ancestor with an identical SOURCES
  object, so the base choice cannot hide a change.
- I did not audit the 44 inherited build reports or `.ufo/waves/round-23/build/`; they are
  author-side evidence and outside this target.
- No sibling report was read for its verdict before forming mine; `Q2TierSupport.md` and
  `S029Quotes.md` were consulted afterwards only to attribute overlap (F-4) and avoid
  duplicating their findings.

## 7. Tooling

No install or upgrade was performed; every command used pre-existing system tools
(`python3`, `git`, `awk`, `grep`, `diff`) plus the repo's own `scripts/sources-census.sh`.
