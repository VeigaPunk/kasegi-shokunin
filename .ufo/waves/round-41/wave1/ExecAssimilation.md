# ExecAssimilation — receipt (kasegi round 41, wave 1)

Item: run the §10 assimilation checks — id-collision guard, quarantine-slice verdicts,
round verdict — read-only against `/home/vgpnk/Projects/shokuknow`.

Lane repo (only repo written): `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Fleet root and `/home/vgpnk/Projects/shokuknow` were read only; no campaign tool was run in
`shokuknow` and nothing was written into either. The lane's `git status --porcelain` shows
**no tracked file modified** by this seat; the only lane paths this seat created are the two
named in this receipt.

Deliverable: `.ufo/waves/round-41/wave1/ExecAssimilation.txt` — **332 lines, 24190 bytes,
sha256 `499f2fd50370da24bd6e5333d656a67af3b2b9fb96bad4cbdca55f897efa79d4`**.

Pins at measurement (`sha256sum`):

```
cfe25e07616fad912b219d81816f944dcbe470a0025789afe4a88c4d549cfb4f  kasegi-shokunin/corpus/SOURCES.md
4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb  shokuknow/merge/kasegi/SOURCES.append.md
5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833  shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

Lane head `b3b08b276af6146217efd89f7595243a644ed00b`; claims freeze
`fbba3d96cdf8d37c1ea41304a1ba35691329684b`; claim base `5b29ea1439450b712581edf5f0bf98dfb262ab`.
The package sha256 is byte-identical to round 40's (`4fe049cb…`), so round 40's refusals
carry byte-identical inputs; only the lane side moved (registry 59 → 62 rows).

## 1. Id-collision guard — 32 collisions, guard proven

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u | wc -l   -> 62
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' …/merge/kasegi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort -u | wc -l -> 94
$ comm -12 reg-ids staged-ids | wc -l   -> 32
collisions: S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047
            S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060 S061 S062
```

`sort` and `sort -u` give the same counts (62 / 94 / 32). Round 40 measured 29 collisions
against the then-59-row registry; the lane has since opened S060–S062, so the same staged
block now collides on 32 numbers.

**Guard proof on an indented-row scratch fixture — nonempty collisions, transcript in
deliverable §6.** The fixture's registry row `  | S002 |` is indented two spaces and the
staged fixture carries S002 at column 0:

```
A (0-3 spaces):  a-reg-ids lines=2  S001 S002 | a-staged-ids lines=2  S002 S003 | a-collisions lines=1  S002
B (^| only):     b-reg-ids lines=1  S001        | b-staged-ids lines=2  S002 S003 | b-collisions lines=0
```

B misses the indented duplicate, so the census-compatible 0-3-space form is required, not
redundant. On the two real inputs both forms agree today (32/32) only because neither file
carries an indented row (`grep -cE '^ {1,3}\|[[:space:]]*S[0-9]{3,}'` → 0 for each).

Per-colliding-id document comparison (recomputed, not copied from round 40): of the 32
colliding numbers, **31 name a different document** in the lane than the package row of the
same number (staged S037 = GB/T 30279-2020 catalogue record vs lane S037 = Cybozu
bug-bounty FAQ; staged S054 = IPA Cabinet-Office request PDF vs lane S054 = CERT/CC SSVC
overview), and **1 names the same document** — staged S042 = lane S042,
`https://www.ipa.go.jp/security/todokede/vuln/process.html`, byte-equal (refused as a
duplicate before any id question).

Package-wide document-level duplicate count recomputed: **21 staged rows** name a URL the
live registry already holds as a mined row (staged S031→lane S043, S032→S044, S033→S045,
S034→S049, S035→S050, S039→S033, S040→S034, S041→S035, S042→S042, S043→S041, S049→S046,
S050→S047, S055→S036, S056→S037, S057→S038, S060→S039, S064→S041, S068→S040, S076→S041,
S080→S048, S123→S032). 3 staged rows carry no URL (own-work rows S072, S110, S113).
**70 staged rows name only documents the lane does not hold.**

## 2. Quarantine slice — 7 kasegi rows, every line carries an S-id

The §10 awk (data rows only; the register's header and `## By lane` totals are stale and
were not used) produced 7 lines: `S037 payload-absent`, `S054 payload-absent`, and
`S048 / S065 / S068 / S069 / S070` in the "could not be fetched" family. An id-presence
check over the slice printed **OK: all 7 lines carry an S-id**.

Per-row verdict (live re-checks, `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`; HTTP
status, bytes and UTC fetch window in the deliverable §7 table):

| row | fetch result | verdict |
|---|---|---|
| S037 | **HTTP 200, 24131 B** (08:19:25→08:19:27Z) | **refuse as staged — quote-form defect, not fabrication.** The register's span is a spliced field collage (four separate table cells joined with `：` after 发布日期/实施日期); whitespace-folded exact match absent; fragment counts measured 1×/1×/1×/1×/2×. |
| S054 | **HTTP 200, 513648 B** (08:19:39→08:19:40Z), `pdftotext -enc UTF-8` → 8785 B | **refuse as staged — quote-form defect, not fabrication.** The §1（ア）clause carries `脆弱性（（法第42条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの`; the register's quote elides that statutory parenthetical, only the suffix is contiguous. |
| S048 | **HTTP 404, 748 B** on both attempts (08:20:22Z, retry 08:23:29Z) | **unreachable as cited.** The same plan is live under the sibling id `4C30E22D…` (**HTTP 200, 99883 B**, 08:23:33Z) carrying `计划号 20260806-T-469`, `正在征求意见`, `项目周期 16个月`, `下达日期 2026-03-02`, `归口 全国网络安全标准化技术委员会` — but **not** the `公示 2025-10-23 … 2025-11-22` dates and **not** `范围和主要技术内容 items 4) to 13)` the staged anchor names. Never a fabrication. |
| S065 | **HTTP 200, 7465472 B** (08:20:27→08:21:13Z); `pdftotext` in all four modes yields 31727–34332 B | **refuse as staged, but the register class is stale** — reachable and payload located (`现行有效法律目录`, `303件`, `刑法（7件）`, `附件一`, `附件二`, `刑法修正案（十二）`; the 刑法 clause is contiguous once the page folio `27` spliced in at the form-feed break is removed). |
| S068 | cited URL **HTTP 403, 465 B** twice (08:21:13Z, retry 08:23:34Z); the lane's own S040 final locator `sec.cloudapps.cisco.com/…/security_vulnerability_policy.html` **HTTP 200, 94027 B** (08:25:59Z) | **refuse — document already held.** The URL is byte-equal to lane row **S040** (`status: mined`). A duplicate, never a fabrication. |
| S069 | **HTTP 200, 0-byte body** on every route (full path 08:21:13Z; the register's literal truncated path 08:23:34Z; with `Referer` 08:26:15Z; `http://` scheme; `kass.sacinfo.org.cn/kfs/token/download/dhppvhmmtuuwkehg` → **HTTP 404**, 0 B, 08:24:16Z) | **unreachable** — the endpoint serves an empty body to this client; the attachment is named upstream on the live plan page. Never a fabrication. |
| S070 | **HTTP 200, 0-byte body** on every route (full path 08:21:14Z; literal path 08:23:35Z; mint route 08:24:05Z; `kass.sacinfo.org.cn/kfs/token/download/udghvosaqozjdqze` → **HTTP 404**, 0 B, 08:24:17Z) | **unreachable** — empty body; named upstream. Never a fabrication. |

**Adopted 0. Adoptable under PROVINCE/QUALITY this round 0.** The three reachable rows
still fail: S037's staged entry binds `ground: F14`, which in the lane is *Japanese severity
vocabulary* (and the round-24 gate ruled the Chinese national grading-standard family
adjacent on PROVINCE scope); S054's staged entry is an amendment layer over the **admitted**
lane entry `authorization-safe-harbor-and-scope.md` (F03); S065's staged entry binds
`ground: F17`, which the lane uses for *Immunefi VSCS v2.2*.

**Two corrections this slice files against the standing record:**

1. **Round 40's "bare `pdftotext` → 0 bytes" for S065 is a measurement artifact, not a
   property of the PDF.** Reproduced here: `pdftotext -enc UTF-8 s065.bin f.txt 2>&1 | head -2`
   leaves `f.txt` at **0 bytes** (the pipe closes and `pdftotext` dies on SIGPIPE), while the
   same command without the pipe leaves **31899 bytes**. The document extracts fine.
2. **S065's digits.** The raw extraction reads `…1997年修订，272009年修正）`; the `27` is the
   **page folio** spliced in at a form-feed page break (`…1997 年修订，\n\n\n   27\n\x0c2009 年修正）`).
   Removing that folio line yields the contiguous clause
   `1．中华人民共和国刑法（1979年通过，1997年修订，2009年修正）` — verified present. The
   round-40 "full clause wraps only at a PDF line break" note is the same effect seen from
   the other side.

## 3. Round verdict — `Assimilation: none`

Blocking reasons, in binding order (deliverable §8 carries the full text):

1. **The claims are frozen and pin the registry at exactly 63 rows.** C2's declared
   after-state is `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md ->
   62 -> 63` with `S063` opened this round for RFC 9116. Any adopted package row makes the
   registry 64+ and falsifies that frozen counter; §10 forbids rewriting a frozen claim.
2. **The package holds nothing that serves a frozen claim.** C1 is the closure suite, C2 is
   RFC 9116 (`/.well-known/security.txt`). Grep for `9116` and `security.txt` over
   `merge/kasegi/SOURCES.append.md` and all 67 package entries returns **0 hits** — the
   package cannot serve C1 or C2 as §2b curation, so adoption would be a new claim.
3. **Every candidate entry fails the per-entry gates on its own.** Measured over the 67
   package entries: **51** cite at least one S-id the live registry does not hold; **0**
   reference a lane capture under `corpus/source-snapshots/`; **39** carry a prose-only
   `recheck:` where Q7 requires a runnable command (28 carry one). The package's `ground:`
   labels also mis-bind to the lane's F-table — package F14 = Chinese national grading vs
   lane F14 = Japanese severity vocabulary; package F17 = Chinese statute drift vs lane
   F17 = Immunefi VSCS; package F11 = claim packaging vs lane F11 = ISO 29147/30111; and
   package F24 = the crowd-testing national standard while **lane F24 is RFC 9116 this
   round** (that mis-bind is on
   `chinese-crowd-testing-national-standard-2026-10-23.md`, the one package entry whose
   `ground:` names an F-number the lane does not hold). The 16 entries whose every source id
   *is* a live lane id are exactly the ones whose documents the lane already holds; 4 of
   them share a filename with an existing lane knowledge file
   (`authorised-testing-rules-of-engagement.md`, `japanese-domestic-disclosure-workflow.md`,
   `japanese-severity-vocabulary-and-impact-model.md`,
   `program-severity-ladders-and-reward-scales.md`) and are thinner than the lane's copy
   (no lane capture, prose `recheck:`), so landing them would replace richer admitted text.
4. **The seven quarantine rows are all refuse/unreachable** (adopted 0).

**Plain statement on the id space, as the item asked.** The staged ids start at **S031** and
the live registry already uses **S031–S062**; C2 opens **S063** this round, so at the judged
head the staged band **S031–S063 is entirely collision-bound** and the free staged band is
**S064–S124** (collision count 33 there, 32 today). A scratch renumber is therefore
arithmetically available for any adopted row — but **no adoption is possible this round**:
the collisions are not the binding constraint (reasons 1 and 2 are), and every candidate
entry fails the per-entry gates regardless (reason 3). **No renumber map is filed**, because
§10 requires a map only for adopted rows and each adopted entry's citation must be
re-pointed **by document**, never by arithmetic (the round-32 correction is what a
speculative arithmetic map costs).

## 4. Nothing else in the lane changed

This seat wrote exactly two files, both inside `.ufo/waves/round-41/wave1/`: the deliverable
`ExecAssimilation.txt` and this receipt `ExecAssimilation.md`. No registry row, knowledge
file, `## Gate` block, lesson, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `SHONEN.md`,
`PROVINCE.md`, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/` or
`corpus/instruments/` file was created, edited or deleted; no fleet file was touched; no
mutating git or jj command was run anywhere. `git status --porcelain` on the lane reports
**no tracked file modified**.

Read-only cross-check run for context (not a claim of this seat):
`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kasegi` → `ok`, exit 0, with the two standing W04
same-URL-across-scopes warnings (S028, S029) — the C2 before-state baseline.

## 5. Tooling

No tool was installed, upgraded or removed. The host guard's pacman pause was respected —
no `pacman` invocation. Pre-existing host tools used as-is: `curl` (network fetches with
`-A kasegi-shokunin/1.0 --max-time 90`), `pdftotext` (poppler), `gs` (ghostscript `txtwrite`),
`awk`/`grep`/`comm`/`sha256sum`/`cmp`. `uv` 0.13.0 was checked for availability only and
not used to install anything (`/home/vgpn/.omp/agent/RULES.md` does not exist on this host;
the operator-owned `~/.omp/agent/config.yml` and `~/.omp/agent/mcp.json` were not touched).
Nothing was written to any PATH directory.

## 6. Scratch

`S=/fast/scratch/hyaku/kasegi-r41/ExecAssimilation/` — created with `mkdir -p`, held the
id lists, the guard fixture and script, the fetch bodies and the built deliverable. Removed
before this yield (`rm -rf -- "$S"`), after the deliverable and this receipt were copied
into the lane's wave directory.

## 7. Checks the L1 should run

1. `sha256sum .ufo/waves/round-41/wave1/ExecAssimilation.txt` → `499f2fd50370da24bd6e5333d656a67af3b2b9fb96bad4cbdca55f897efa79d4`
   (332 lines, 24190 bytes) and confirm the file is byte-identical to the bytes this seat
   wrote.
2. `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain | grep -v '^??'`
   → empty, and confirm the only new paths are this seat's two wave-1 files.
3. Re-run the guard **after** the round-41 registry rows land: the collision count measured
   here (32) is a lower bound; the judged head will be 33 once C2's S063 is taken.
4. If the L1 lands the `Assimilation: none` verdict in the round lesson's `## Gate` block,
   carry the two corrections from receipt §2 verbatim — the S065 SIGPIPE artifact and the
   S065 page-folio splice — so the round-40 spot-check record is corrected at the source
   rather than restated.
