# ScoutAssimilation — round-28 wave-1 assimilation pre-checks (kasegi)

Seat: `ScoutAssimilation` (leaf, read-only on production; scratch only under
`.ufo/waves/round-28/assimilation/`).
Lane: `kasegi-shokunin`. Lane base revision: `c9f8b115a098c65356e4b3b6048af45a37ab8395`
(claims-freeze commit). Date: 2026-10-25 (UTC).

**No production file was created, edited or deleted by this seat.** Every write below is under
`.ufo/waves/round-28/assimilation/`. The read-only package
`/home/vgpnk/Projects/shokuknow/merge/kasegi` was read only; no campaign tool was run there.
No tool was installed. No pacman transaction was attempted (host-wide pause respected).

---

## 1. Id-collision check — the pattern, run exactly as the round prompt specifies

Pattern (0-3-space-tolerant, identical to the round-25 guard):
`'^ {0,3}\|[[:space:]]*S[0-9]{3,}'`

Commands (verbatim, from `.ufo/waves/round-28/assimilation/collision-check.sh`):

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > staged-ids
$ comm -12 reg-ids staged-ids > collisions
```

### 1a. Against the FROZEN lane base (rev `c9f8b11…`) — the count the claims were frozen against

Because a sibling seat (`ScribeRegistryC2`) appended the S042 row to the live worktree while this
seat was running, the collision set was measured twice: once against the frozen base via
`git show` (read-only, `.ufo/waves/round-28/assimilation/collision-check-frozen-base.sh`), and
once against the live worktree. **The frozen-base figure is the claimable one.**

| list | lines | contents |
|---|---|---|
| lane registry ids (base `c9f8b11`) | **41** | `S001 … S041` (contiguous) |
| staged ids (package `SOURCES.append.md`) | **94** | `S031 … S124` (contiguous) |
| **collisions (`comm -12`)** | **11** | `S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041` |

Both full id lists are pasted in `assimilation/base/reg-ids` and `assimilation/base/staged-ids`;
the collision set is `assimilation/base/collisions` (11 lines).

**Live-worktree re-run** (after `ScribeRegistryC2` landed the S042 row): lane registry ids = 42
(`S001 … S042`), staged = 94, **collisions = 12** (`S031 … S042`) — the extra id is the newly
adopted lane S042, which by design collides with staged S042 by *number* while denoting the
*same* document (see §3). Both figures are recorded; neither is a defect.

### 1b. Every collision is an id-space collision, never a duplicate document

The prompt predicted "staged S031-S043+ collide with lane S031-S041 by number but differ by
document". Measured (URL extracted per row, base vs staged), `assimilation/collision-check-frozen-base.txt`:

```
S031  DIFFER  lane=https://www.cve.org/.../CNA_Rules_v4.2.6.pdf      staged=https://hackerone.com/security/policy_versions
S032  DIFFER  lane=https://nvlpubs.nist.gov/.../800-115.pdf         staged=https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md
S033  DIFFER  lane=https://laws.e-gov.go.jp/api/1/lawdata/411AC…     staged=https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/mappings/cwe/cwe.json
S034  DIFFER  lane=https://www.soumu.go.jp/…/legal/09/               staged=https://zc.cnvd.org.cn/news/helpList
S035  DIFFER  lane=https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf  staged=https://security.360.cn/Reward/rules
S036  DIFFER  lane=https://cybozu.co.jp/company/security-policy/    staged=https://security.bilibili.com/static/docs/BILISRC_V1.7.pdf
S037  DIFFER  lane=https://cybozu.co.jp/products/bug-bounty/faq/    staged=https://openstd.samr.gov.cn/…?hcno=458BAC…
S038  DIFFER  lane=https://pepabo.com/contact/vulnerability-reporting/  staged=https://std.samr.gov.cn/gb/search/gbDetailed?id=B4C25880C…
S039  DIFFER  lane=https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html  staged=https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128
S040  DIFFER  lane=https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html  staged=https://www.soumu.go.jp/…/legal/09/
S041  DIFFER  lane=https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf  staged=https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf
--- collisions=11 same-document=0 different-document=11
```

`same-document=0, different-document=11` — the mapping must be per-document, never by number and
never by a constant offset. (Lane S039 and lane S033 vs staged S039/S033 are the same *URLs* but
at **different ids**: lane S033 = e-Gov lawdata = staged S039; lane S039 = Hitachi = staged S060.
This is exactly the case a constant shift would get wrong.)

Latent-risk check on the real inputs: `grep -cE '^ {1,3}\|[[:space:]]*S[0-9]{3,}'` → **0** on
both the lane registry and the package (exit 1). Both files are flat today, so the 0-3-space form
and a column-zero form agree — the tolerant form is what survives the first indented paste.

---

## 2. Guard proof — the 0-3-space pattern detects what a column-zero pattern misses

Fixture (scratch): `assimilation/fixture/fixture-SOURCES.md` holds
`  | S002 | Fixture Document Beta — https://example.invalid/fixture/beta | …` **indented two
spaces** (line 6); `assimilation/fixture/fixture-staged.md` carries `| S002 | …` at column 0.
Generator: `assimilation/guard-proof.sh`; transcript: `assimilation/guard-proof.txt`.

**A. Guard pattern `^ {0,3}\|` — collision detected**

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' fixture/fixture-SOURCES.md | grep -oE 'S[0-9]+' | sort > a-reg-ids
[exit 0]
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' fixture/fixture-staged.md | grep -oE 'S[0-9]+' | sort > a-staged-ids
[exit 0]
$ comm -12 a-reg-ids a-staged-ids > a-collisions
[exit 0]
a-reg-ids    lines=2   -> S001 S002
a-staged-ids lines=2   -> S002 S003
a-collisions lines=1
$ cat a-collisions
S002
```

**B. Column-zero-only pattern `^\|` over the same fixtures — collision MISSED**

```
$ grep -oE '^\|[[:space:]]*S[0-9]{3,}' fixture/fixture-SOURCES.md | grep -oE 'S[0-9]+' | sort > b-reg-ids
[exit 0]
$ grep -oE '^\|[[:space:]]*S[0-9]{3,}' fixture/fixture-staged.md | grep -oE 'S[0-9]+' | sort > b-staged-ids
[exit 0]
$ comm -12 b-reg-ids b-staged-ids > b-collisions
[exit 0]
b-reg-ids    lines=1   -> S001
b-staged-ids lines=2   -> S002 S003
b-collisions lines=0
$ cat b-collisions
                       # empty: 0 bytes, no output
```

**Verdict: the guard is proved once, and it is proved discriminating.** A = 1 collision (S002),
B = 0 bytes. `a-collisions` is 5 bytes; `b-collisions` is 0 bytes. The 0-3-space-tolerant form
reports the duplicate; the column-zero-only form sees one registry row instead of two and reports
nothing, so an indented duplicate id would be appended silently. Reproducible via
`bash .ufo/waves/round-28/assimilation/guard-proof.sh` (script exit 0).

---

## 3. By-document mapping for the rows this round adopts

`assimilation/by-document-map.sh` → `assimilation/by-document-map.txt`.

### staged S042 → lane S042 (free; a genuinely NEW document)

| check | command | result |
|---|---|---|
| staged S042 URL | `grep -E '^ {0,3}\| *S042 *\|' SOURCES.append.md \| grep -oE 'https?://[^ \|]+'` | `https://www.ipa.go.jp/security/todokede/vuln/process.html` |
| lane S042 id free at base | `grep -cE '^ {0,3}\| *S042 *\|' base/SOURCES.md` | **0** (exit 1) |
| **no lane row carries that URL** (prompt's check) | `grep -cF 'https://www.ipa.go.jp/security/todokede/vuln/process.html' corpus/SOURCES.md` | **0** (exit 1) — measured against the base registry; the only occurrence in the live file now is the row `ScribeRegistryC2` appended during this wave |

The staged S042 row is the IPA/JPCERT/CC **intake-process** page — a document the lane did not
hold. Mapping: **staged S042 → lane S042**, free, no duplicate by document. Correct.

### staged S043 → lane S041 (SAME URL, verified by document not by number)

| check | result |
|---|---|
| staged S043 URL | `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` |
| lane S041 URL | `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` |
| **identical** | **yes — byte-identical URL string** |

Lane S041 (line 47 of the base registry) is
`情報セキュリティ早期警戒パートナーシップガイドライン 2026年10月 (JPCERT/CC) — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf`,
registered in round 26 with scope limited to 付録6 (the ISO/IEC 29147 / 30111 annex). Staged S043
is the **same PDF**, scoped to Ⅳ / 図1 / 付録3 / 起算日. So staged S043 is **not re-registered**:
it is cited as lane **S041** (the row's anchor set is broadened by the round-28 re-capture, not by
a new id). The frozen claim's C2 text agrees ("staged S043 = already lane S041 round 26, cited
not re-registered").

### Proof that registering S043 as a new id would be wrong (measured, not asserted)

`assimilation/row-grammar-test.sh` → `assimilation/row-grammar-test.txt`, scratch `schema4/`:

- Staged **S042** inserted alone (live S042 removed): census `validate` → **only the two
  pre-existing W04 warnings** (S028 HackerOne, S029 CRA). No E01-E12 finding against the row.
- Staged **S043** inserted alone (live S041 removed): census `validate` → **only the two
  pre-existing W04 warnings**. No E-code.
- Staged **S043** inserted *alongside* live S041 (both rows present): census emits
  `W04 S043 duplicate url www.jpcert.or.jp/vh/partnership_guideline2026.pdf across scopes` and
  `E04` if the scopes matched. Confirmed by direct run: `file W04 S043 duplicate url
  www.jpcert.or.jp/vh/partnership_guideline2026.pdf across scopes`.
  → **Registering staged S043 as a new id creates a duplicate-document warning on a document the
  lane already holds.** This is the concrete reason the mapping is by document.

### Whole-registry duplicate-URL scan (for completeness)

`grep -oE 'https?://[^ |]+' corpus/SOURCES.md | sort | uniq -d` → 3 hits, all pre-existing and
explained: HackerOne (S006/S028, the deliberate duplicate-row proposal), CRA (S024/S029,
same-URL-different-scope), and the Cisco redirect host appearing in the two `## Registry changes`
log lines (not rows). **No duplicate URL among registry rows involving S041 or S042.**

---

## 4. Quarantine slice — the kasegi rows of the absent-defect register

Register (READ-ONLY): `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`.
Extract (the prompt's awk verbatim): `assimilation/quarantine-slice.txt` — **7 rows**.

| staged id | round | class cell (verbatim) | adopted this round? |
|---|---|---|---|
| S037 | round1 | `` `payload-absent` `` | no |
| S054 | round3 | `` `payload-absent` `` | no |
| S048 | round2 | `the cited source could not be fetched, so no quote was checked` | no |
| S065 | round4 | `the cited source could not be fetched, so no quote was checked` | no |
| S068 | round4 | `the cited source could not be fetched, so no quote was checked` | no |
| S069 | round4 | `the cited source could not be fetched, so no quote was checked` | no |
| S070 | round4 | `the cited source could not be fetched, so no quote was checked` | no |

**Confirmation that no adopted row appears:**

- `grep -nE '\| *S04[23] *(`|$)' <register>` → the only S042/S043 hit is **lane `game-dev-2d`'s**
  row (`https://docs.godotengine.org/en/4.7/classes/class_input.html`) — a different lane, a
  different document. No kasegi row names S042 or S043.
- `grep -cF 'todokede/vuln/process' <register>` → **0** (exit 1).
- `grep -cF 'partnership_guideline2026' <register>` → **0** (exit 1).

**Verdict list (rows NOT adopted stay quarantined):** S037, S048, S054, S065, S068, S069, S070 —
all seven remain quarantined, none adopted, none cleared by this wave. Note S068 (Cisco policy)
was already mined in the lane as **S040** in round 25; it is a legacy-id duplicate of an
already-registered document, so it is out of scope for adoption here. (Round-26's `ScoutQuarantine`
recorded the same per-row classes; this wave re-extracts the slice, it does not re-fetch.)

---

## 5. Staged-row schema survey of the rows this round adopts

`assimilation/schema-survey.sh` → `assimilation/schema-survey.txt`.

### 5a. Census grammar conformance (11 columns, no pipes in cells, recheck-cell form)

| property | staged S042 | staged S043 |
|---|---|---|
| field count (`NF`, 11 columns ⇒ NF=13) | **NF=13**, fields_minus_edges=**11** | **NF=13**, fields_minus_edges=**11** |
| literal or escaped pipe (`\|`) inside any cell | **0** (both probes) | **0** (both probes) |
| `kind` enum | `docs` ✔ | `spec` ✔ |
| `tier` enum | `A` ✔ | `A` ✔ |
| `status` enum | `mined` ✔ | `mined` ✔ |
| `opened` ISO date | `2026-10-23` ✔ | `2026-10-23` ✔ |
| **recheck cell** | **`180d`** — NNn cadence ✔ (NOT prose) | **`180d`** — NNn cadence ✔ (NOT prose) |
| `used-by` paths exist on disk in the lane? | `corpus/knowledge/japanese-domestic-disclosure-workflow.md` — **not yet** (entry seat still to land) | 3 paths, **none yet** in the lane — moot: S043 is not re-registered |

Full staged cell dump for S042 (verbatim):

```
id       S042
source   IPA 脆弱性関連情報の届出受付業務における取扱いプロセス — https://www.ipa.go.jp/security/todokede/vuln/process.html
kind     docs      tier  A
scope    IPA and JPCERT/CC's own intake process for vulnerability reports, including the 起算日 and publication-date steps
anchor   脆弱性関連情報の取扱いプロセス steps 1 to 10, step 5 起算日の連絡; ウェブアプリケーションの取扱いプロセス steps 1 to 6
teaches  Japan runs a coordinator-mediated flow in which the finder is told the 起算日 and the detail-information date, and may query progress
status   mined     opened 2026-10-23     recheck 180d
used-by  corpus/knowledge/japanese-domestic-disclosure-workflow.md
```

### 5b. The round-27 lesson's flag on the staged S042 `teaches` cell — RESOLVED, with evidence

The round-27 lesson recorded: *"the staged row `| S042 |` carries a prose-flavoured `teaches` cell
that the lane's census grammar would need re-checking before append."* That re-check is now done:

- **The census grammar does not police the `teaches` cell of a mined row.** The census validator's
  only `teaches` rule is **W02** (thin reject reason, `status == rejected`), plus the `supersedes
  S###` escape inside E04. There is no E-code for a prose `teaches` cell on a mined row. Measured:
  inserting the package's own staged S042 row into a scratch registry and running
  `sources-census.sh validate` produces **no E-code at all** for that row
  (`assimilation/row-grammar-test.txt`, case A).
- **The lane's own house convention is stricter than the census.** 6 of the lane's 42 rows carry
  an `(Lnn)` capture-line anchor in `teaches` (S036, S037, S038, S039, S040, and the new S042);
  35 carry none; 1 carries another locator form. The convention is applied by the rows *this
  round's* seats write (S036-S040 from round 25, S042 from round 28).
- **The landed S042 row already satisfies it.** `ScribeRegistryC2`'s appended lane S042 row
  (registry line 48) reads
  `teaches: A coordinator mediates the flow: the finder is told the 起算日 and the detail-information date, while IPA and JPCERT/CC contact the developer (L145).`
  and its anchor cell cites `L132-L160`, `L144-L145`, `verified against the round-28 capture
  S042.txt`. The `(L145)` anchor is real: `corpus/source-snapshots/round-28/S042.txt:145` carries
  the step-5 body line, and `:153` carries the finder-can-query-progress sentence.
  → **The round-27 flag is discharged: the landed row carries the capture-line anchor the staged
  cell lacked.** No correction is owed to the package.

### 5c. A package-wide defect that is NOT triggered by this round's two rows

Surveying all 94 staged rows' recheck cells (`schema-survey.txt`):

| recheck form | count |
|---|---|
| NNn (`180d`, `90d`, `30d`, `730d`) | 50 |
| ISO date | 1 |
| **prose** (`90d — re-open the … page and confirm … still present (ran 2026-10-24)`) | **43** |

All 43 prose cells are in S081-S124. **A prose recheck cell is an E09 violation.** Measured
directly: inserting staged S081 into a scratch registry and running the census gives
`file E09 S081 recheck=90d — re-open the 公告 page and confirm … still present (ran 2026-10-24)`.
The two rows this round adopts are **not** in that set (both carry a bare `180d`), so **this round
is unaffected** — but any future round that adopts a staged row from S081-S124 must rewrite the
recheck cell to a bare cadence (or the census exits 1). Flagged for the L1 and the lesson seat.

### 5d. The package's `ground:` pointers use a DIFFERENT frontier namespace than the lane

The adopted staged entry `japanese-domestic-disclosure-workflow.md` carries
`ground: F13 (new frontier item; extends F02, which compares coordinator timelines)`. The lane's
frontier is F01-F12 and **lane F12 is this round's Japanese workflow row**. The package's own
`F12` is a different topic (the Chinese statutory-authorisation family:
`chinese-criminal-thresholds-and-authorisation.md`, `authorization-safe-harbor-and-scope-…`,
`japanese-disclosure-legal-framework.md`, etc. — 8 entries). Package grounds absent from the lane
frontier: **F13 F14 F16 F17 F18 F19 F20 F21 F24**.

Consequence for this round: **the staged `ground:` line must not be copied verbatim into the lane
entry.** The lane's entry must ground on the lane's own **F12**. The round-26 precedent is the
same failure mode at row level (round-26 `ScoutPackageInventory` §4: package `ground: F20` named
no lane frontier row, so the entry was rejected). The lane entry must cite its sources by lane
row id (**S041 + S042**), not by staged id — the staged entry's own `source:` header says
`source: S043 — …`, which is the **staged** id for the document the lane already holds as S041.

---

## 6. Facts measured in this wave that the L1 should know

1. **Live census at the time of writing (read-only run, stdout only):**
   ```
   $ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
   kasegi W04 S028 duplicate url docs.hackerone.com/… across scopes
   kasegi W04 S029 duplicate url eur-lex.europa.eu/… across scopes
   kasegi E11 S041 missing used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md
   kasegi E11 S042 missing used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md
   exit=1
   ```
   The two **E11** findings are the *expected* transient state: the entry file
   `corpus/knowledge/japanese-domestic-disclosure-workflow.md` did not exist on disk when this
   seat ran (it is `ScribeEntryC2`'s owned path). **C2's counter `census exit=0` depends on that
   file landing.** W04 S028/S029 are pre-existing warnings that do not affect the exit code.
   The L1 must re-run the census after `ScribeEntryC2` lands the entry.
2. **Collision count: 11 against the frozen base, 12 against the live worktree** (§1). Both are
   correct for their respective registry states; the claimable frozen-base figure is 11.
3. **`frontier-admitted` count:** `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md`
   → **12** (F01-F12 all `admitted`; F12 already appended by `ScribeReadmeC2` during this wave).
4. **Registry S042 row is live** (registry line 48) with used-by exactly
   `corpus/knowledge/japanese-domestic-disclosure-workflow.md`; **S041's used-by already gained
   that entry** (`…division-of-labour.md, …divergence-and-clause-crosswalk.md,
   japanese-domestic-disclosure-workflow.md`) and the old→new change is logged in
   `## Registry changes`. Both are `ScribeRegistryC2`'s owned paths; this seat changed nothing.
5. **Round-28 manifest is landed** (`corpus/source-snapshots/round-28/manifest.json`,
   sha256 `e62ddad133ffc19e…` per `ExecManifest`'s receipt) pinning S041 (`e18acbf99d137c26…`,
   147 267 B) and S042 (`b432ec165693d005…`, 60 508 B) with Q-assertions.

## 7. The ≥1 reject this round needs (assimilation Gate)

The Gate requires ≥1 admit **and** ≥1 reject with inline ≤25-word quotes. The package's staged
entry `japanese-domestic-disclosure-workflow.md` grounds on package-`F13`, which is **not** a lane
frontier id (lane F12 is the Japanese workflow; the package's F12 is the Chinese statutory-
authorisation family). The cleanest reject available in the package is the round-26-recorded
standing refusal, re-confirmed on current bytes:

- **Reject candidate — `chinese-criminal-thresholds-and-authorisation.md`** (staged S044/S045/S046).
  Grounds: its `ground: F12 (extends F03, which holds safe-harbor attribution only)` names a
  package frontier id whose lane counterpart is a *different topic*; its `recheck:` line is the
  package's prose form (E09-class, `730d — curl … (ran 2026-10-23)`), which the lane's census
  grammar rejects; and its quoted thresholds are not anchored to the lane's round-28 captures.
  (Round 24/26 lessons recorded the same refusal on the same grounds.)
- The **F19/F20** package entries remain rejected for the same ground-namespace reason
  (round-26 `ScoutPackageInventory` §4: `grep -cE '\| F20 '` → 0).

> Quoting this seat's own evidence: the package's staged S043 anchor cell reads
> `2026年10月 edition, PDF digital signature dated 2026.09.29; section Ⅳ ソフトウエア製品に係る脆弱性関連情報取扱, 図1`,
> while lane S041's already-registered anchor cell reads
> `付録6 §2 p.45 …, §4 p.46-47 …, 参考1 p.53-54 …` — same PDF, disjoint anchors, one document.

**This seat's scope does not include writing the Gate quotes into the lesson** (`ScribeLesson`
owns `corpus/lessons/round-28.md`); the above is offered as measured evidence for that seat.

## 8. Re-run commands for the L1 (post-change)

```bash
# §1 collision check against the frozen base (11) and the live tree
bash /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-28/assimilation/collision-check.sh
bash /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-28/assimilation/collision-check-frozen-base.sh

# §2 guard proof (A = 1 collision, B = 0 bytes)
bash /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-28/assimilation/guard-proof.sh

# §3 by-document mapping + §5 schema/grammar tests
bash /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-28/assimilation/by-document-map.sh
bash /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-28/assimilation/schema-survey.sh
bash /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-28/assimilation/row-grammar-test.sh

# §6 census, AFTER the entry lands (this seat's measured exit was 1 with two E11s)
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo census_exit=$?
```

## 9. Files written by this seat (all scratch)

| path | what |
|---|---|
| `.ufo/waves/round-28/assimilation/collision-check.sh` / `.txt` | the §1 collision check (live tree) |
| `.ufo/waves/round-28/assimilation/collision-check-frozen-base.sh` / `.txt` | the §1 collision check against rev `c9f8b11` + per-collision document comparison |
| `.ufo/waves/round-28/assimilation/collision-check-postchange.txt` | live-tree re-run transcript (12 collisions) |
| `.ufo/waves/round-28/assimilation/reg-ids`, `staged-ids`, `collisions` | the three id lists |
| `.ufo/waves/round-28/assimilation/base/{SOURCES.md,reg-ids,staged-ids,collisions}` | the frozen-base copies |
| `.ufo/waves/round-28/assimilation/guard-proof.sh` / `.txt` + `fixture/` | the §2 guard proof (fixture registry, fixture staged, a-/b- id lists and collision sets) |
| `.ufo/waves/round-28/assimilation/by-document-map.sh` / `.txt` | the §3 mapping |
| `.ufo/waves/round-28/assimilation/quarantine-slice.txt` | the §4 kasegi slice (7 rows) |
| `.ufo/waves/round-28/assimilation/schema-survey.sh` / `.txt` | the §5 cell-by-cell survey |
| `.ufo/waves/round-28/assimilation/census-grammar-test{,2,3}.sh` / `.txt` + `schema{,2,3}/` | census-grammar trials (v1/v2 superseded by v3: an `awk` insert failed silently in v1/v2 — v3 inserts with python3) |
| `.ufo/waves/round-28/assimilation/row-grammar-test.sh` / `.txt` + `schema4/` | the isolated per-row census measurements (S042, S043, S081) |
| `.ufo/waves/round-28/wave1/ScoutAssimilation.md` | this report |
| `.ufo/waves/round-28/receipts/ScoutAssimilation.txt` | the seat receipt |

## 10. Unrun / unresolved

- **No fetch of the IPA or JPCERT pages was performed by this seat** (read-only scope; the capture
  seats own the fetches). The quoted capture lines quoted in §5b (`S042.txt:145`, `:153`) were read
  from the **landed round-28 capture bytes**, not from a fresh fetch — that is a capture-grounded
  check, not a network re-verification.
- **The census E09 finding on staged S081** (§5c) was measured on a scratch registry copy, not on
  the lane registry; the lane registry itself has no prose-recheck row today.
- **The 43 prose-recheck staged rows (S081-S124)** were surveyed for form only. Whether each is
  otherwise adoptable (fetchability, quote verifiability) was not re-checked — that is the
  quarantine column's job, and rows S065/S068 were re-verified in round 26, not here.
- **No assertion is made about any claim's after-value.** C1 and C2 counters belong to their own
  seats and to the L1's close; this seat ran no build, lint or test.
- Tooling: none installed or upgraded. `bash`, `grep`, `awk`, `sed`, `comm`, `sort`, `wc`,
  `python3`, `git` (read-only: `rev-parse`, `show`, `status`, `log`) from the base system. No
  pacman transaction attempted.
