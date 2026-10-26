# ExecCensusDry — round-31 receipt (scratch census validation before the S048 registry append)

Answering model: `devin/deepseek-v4-1-flash` (the route table's resolution for this seat; no model passed).
Axes: depth:verifiability, coverage. Claims touched: C2 (pre-append gate only — no C2 counter is claimed here).
Writes: this receipt + `.ufo/waves/round-31/wave1/ExecCensusDry/**` (scratch mirror). No corpus file, no instrument, no
lane Git index, no fleet-root file was written. No tool installed, no pacman transaction, no network fetch.
All commands below ran from `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless the command shows a `cd`.

## 0. Scratch layout

```
.ufo/waves/round-31/wave1/ExecCensusDry/
├── validate/
│   ├── controls.py                 # regenerates the three negative control registries (idempotent)
│   ├── corpus/SOURCES.md           # mirror registry = live lane registry + the planned S048 row (line 54)
│   ├── corpus/README.md            # copy
│   ├── corpus/knowledge/**         # symlinks to the live files + one real placeholder used-by file
│   ├── corpus/instruments -> live   # symlink (fidelity only; no instrument was run on the mirror)
│   ├── corpus/source-snapshots/round-31/S048.txt   # copy of the in-flight capture (fidelity for the anchor cell)
│   ├── pre/corpus/SOURCES.md       # byte copy of the live lane registry (row absent), knowledge/instruments symlinked
│   └── ctl-{dup-id,dup-url,dangling-usedby}/corpus/SOURCES.md   # negative controls, knowledge/instruments symlinked
└── (this receipt)
```

Construction commands (verbatim):

```
W=.ufo/waves/round-31/wave1/ExecCensusDry
mkdir -p "$W/validate/corpus" "$W/validate/pre/corpus"
cp -a corpus/SOURCES.md corpus/README.md "$W/validate/corpus/"
cp -a corpus/knowledge "$W/validate/corpus/"
mkdir -p "$W/validate/corpus/instruments"
cp -a corpus/instruments/*.py corpus/instruments/*.md corpus/instruments/*.txt \
      corpus/instruments/*.tsv corpus/instruments/*.json "$W/validate/corpus/instruments/"
cp -a corpus/SOURCES.md "$W/validate/pre/corpus/SOURCES.md"
ln -s ../../corpus/knowledge "$W/validate/pre/corpus/knowledge"
ln -s ../../corpus/instruments "$W/validate/pre/corpus/instruments"
printf '# placeholder — ExecCensusDry mirror stand-in for the F15 entry (ExecEntryF15 owns the real path)\n\nsource: S048 — https://www.microsoft.com/en-us/msrc/msvr\n' \
  > "$W/validate/corpus/knowledge/vendor-third-party-finding-coordination.md"
mkdir -p "$W/validate/corpus/source-snapshots/round-31"
cp -a corpus/source-snapshots/round-31/S048.txt "$W/validate/corpus/source-snapshots/round-31/S048.txt"
```

Mirror bytes: `validate/corpus/SOURCES.md` sha256 `75e413721080147bfb6081d3fb91b7b4e565b14886b05bb366da634faa92021e`;
`validate/pre/corpus/SOURCES.md` sha256 `a126a5f339323d5ae417a944d163d75a0427d9c77a5a330308e193dc7b81d927` — **byte-identical to the live
`corpus/SOURCES.md`** at the time of the copy (`cmp` clean), so the PRE run is the live registry, not a re-typed one.
The capture copy is `2001ad7732a16cd385b649a3eb2b9f2c6000fd90ca1cce219868a646cbc67e55`, byte-identical to the in-flight
`corpus/source-snapshots/round-31/S048.txt` at copy time — **in-flight, owned by ExecCapManifest, non-comparative (M30-3)**;
the mirror keeps it only so the anchor cell's path exists, and no census check reads it.

Bloat control (R14): the first build copied `corpus/knowledge` and `corpus/instruments` outright; those 43 knowledge files
and the instruments dir were then replaced by relative symlinks to the live tree, leaving only the placeholder file, the
five registry files, the README copy, `controls.py` and the capture as real bytes — **242,850 bytes of regular files + 52
symlinks** in the whole seat dir (`find … -type f -exec wc -c + | tail -1`). The gate was re-run *after* the conversion and
is byte-for-byte the same result as before it (§1, re-proof below), so the symlink-backed mirror is the mirror of record.

Re-proof on the symlink-backed mirror (identical findings, identical counts, controls still fire):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file ".../validate/corpus/SOURCES.md"
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-31/wave1/ExecCensusDry/validate/corpus/SOURCES.md
post_exit=0
$ … census --file ".../validate/corpus/SOURCES.md" | grep -E 'rows|mined|tier.A'
file	rows	48
file	tier.A	45
file	status.mined	36
$ … validate --file ".../ctl-dup-id/corpus/SOURCES.md"        → file	E03	S047 duplicate id                                      exit 1
$ … validate --file ".../ctl-dup-url/corpus/SOURCES.md"       → file	E04	S048 duplicate url www.ipa.go.jp/… within scope …      exit 1
$ … validate --file ".../ctl-dangling-usedby/corpus/SOURCES.md" → file	E11	S048 missing used-by …-ABSENT.md                     exit 1
```

## 1. OUTPUT 1 — gate: `sources-census.sh validate --file <mirror>/corpus/SOURCES.md` → exit 0

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file "$PWD/.ufo/waves/round-31/wave1/ExecCensusDry/validate/corpus/SOURCES.md"
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-31/wave1/ExecCensusDry/validate/corpus/SOURCES.md
post_exit=0
```

Findings = the two base W04 warnings only; **no E-code at all**, and in particular no `E03` (duplicate id), `E04`
(duplicate URL within scope), `E11` (dangling used-by), `E01` (NF≠13) or `E12` on the new row. Gate **PASSES**.

Attribution run — same mirror with the row absent (PRE):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file "$PWD/.ufo/waves/round-31/wave1/ExecCensusDry/validate/pre/corpus/SOURCES.md"
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-31/wave1/ExecCensusDry/validate/pre/corpus/SOURCES.md
pre_exit=0
```

PRE and POST findings are identical (same two W04 lines, same exit 0): the S048 row adds **zero** findings. Row count
from the instrument itself:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file ".../validate/pre/corpus/SOURCES.md"
file	rows	47     (tier.A 44, tier.B 1, tier.C 2; mined 35, queued 9, rejected 3)
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file ".../validate/corpus/SOURCES.md"
file	rows	48     (tier.A 45, tier.B 1, tier.C 2; mined 36, queued 9, rejected 3)   census_exit=0
```

47 → 48 rows, mined 35 → 36, tier.A 44 → 45: the row lands as exactly one new mined tier-A record, which is the C2
registry figure the append must produce.

## 2. Gate discrimination — the exit 0 above is not vacuous

Three negative controls, regenerated by `validate/controls.py` (idempotent: the aggregate sha256 of the three control
registries is `762682043563669f8c0ef5e85751918fe303c322452b97615d7c3e479708bbc6` before and after a second run):

```
$ python3 .ufo/waves/round-31/wave1/ExecCensusDry/validate/controls.py
wrote ctl-dup-id/corpus/SOURCES.md
wrote ctl-dup-url/corpus/SOURCES.md
wrote ctl-dangling-usedby/corpus/SOURCES.md
regen_exit=0

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file ".../ctl-dup-id/corpus/SOURCES.md"
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E03	S047 duplicate id
ctl_dup-id_exit=1

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file ".../ctl-dup-url/corpus/SOURCES.md"
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E04	S048 duplicate url www.ipa.go.jp/security/reports/vuln/jvn/ipedia2026q3.html within scope JVN quarterly severity distribution
ctl_dup-url_exit=1

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file ".../ctl-dangling-usedby/corpus/SOURCES.md"
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	E11	S048 missing used-by corpus/knowledge/vendor-third-party-finding-coordination-ABSENT.md
ctl_dangling-usedby_exit=1
```

Each control changes exactly the one thing its name says (id / URL+scope / used-by path) and each fires the matching
E-code at exit 1. The gate therefore refuses a duplicate id, a duplicate URL and an unresolvable used-by on this exact
row shape — the exit 0 in §1 is a real pass, not a gate that cannot fail.

## 3. OUTPUT 2 — live-lane id collision reproduction (byte equality with `.ufo/waves/round-31/assimilation/`)

Extractor = the round prompt's own 0–3-leading-space pattern, run on the live lane registry and on the staged package
(`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`, read-only):

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | sed -E 's/^ *\| *//' > /tmp/reg.txt
47 lines   sha256 ab66f54a2135cea0359318caabb77575740093a32d7be7eb4bde47687be373c9
  vs assimilation/reg-ids   ab66f54a2135cea0359318caabb77575740093a32d7be7eb4bde47687be373c9   → cmp clean, BYTE-EQUAL

$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md \
    | sed -E 's/^ *\| *//' > /tmp/staged.txt
94 lines   sha256 550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f
  vs assimilation/staged-ids 550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f   → cmp clean, BYTE-EQUAL

$ comm -12 <(sort -u /tmp/reg.txt) <(sort -u /tmp/staged.txt) > /tmp/coll.txt
17 lines   sha256 ac78cd564ab864b574e0d54d4e4656d448439403839530bb3044d04175acd2d2
  vs assimilation/collisions  ac78cd564ab864b574e0d54d4e4656d448439403839530bb3044d04175acd2d2   → cmp clean, BYTE-EQUAL
  first=S031  last=S047   (17 collisions, S031…S047 — the count and range the round prompt names)
```

Guard proof (`.ufo/waves/round-31/assimilation/guard-proof-collisions`, 5 bytes `S031\n`): both plausible producers
reproduce it byte-for-byte —

```
$ head -1 /tmp/coll.txt | cmp - assimilation/guard-proof-collisions        → BYTE-EQUAL
$ grep -x 'S031' /tmp/coll.txt | cmp - assimilation/guard-proof-collisions → BYTE-EQUAL
$ xxd assimilation/guard-proof-collisions
00000000: 5330 3331 0a                             S031.
```

The guard id is a genuine collision, not an artefact of the pattern: the same id names **two different documents** —
live `S031` = "CVE Numbering Authority Operational Rules v4.2.6 — https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf";
staged `S031` = "HackerOne standard program policy set — https://hackerone.com/security/policy_versions". Ids therefore
cannot be carried over from the package by number; only documents map. (Recorded as a reconstruction of the producer's
command — the file itself is data, and both candidate producers agree on its bytes.)

Note on the pattern: no row in either file is indented 1–3 spaces today, so a column-zero-only `^\|` pattern yields the
same 47/94/17 sets. The 0–3-space form is strictly more general and reproduces the committed files exactly; it is not
distinguishing anything on today's bytes, and this receipt does not claim that it does.

## 4. OUTPUT 2 (cont.) — S048 is free; the staged S080 URL is on no lane row

```
$ grep -cE '^ {0,3}\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md        → 0
$ grep -ic 'msrc\|msvr\|microsoft' corpus/SOURCES.md                          → 0
```

Instrument-native proof, not just a hand normalization: the §1 POST run scans all 48 rows and emits **no** `E04` and no
`W04` for S048. `E04` fires only on the same URL inside the same scope and `W04` only on the same URL across scopes, so
their absence is the census's own statement that the MSVR URL is unique among the 48 rows (the only W04 lines are the
pre-existing S028/S029 pair). Corroborating manual normalization (host lowercased, fragment and trailing slash stripped —
the same transform as the script's `url_of`): target normalizes to `www.microsoft.com/en-us/msrc/msvr`; zero lane rows
match it, zero lane rows contain the substring `msrc/msvr`, and no lane row has a `microsoft.com` host at all.
The URL also occurs exactly once in the package (`grep -c` → 1, the S080 row itself), so the row is not duplicated
inside the staged append either.

Staged ids in the way of the target id, for the record: staged `S048` is a **different document** —
"全国标准信息公共服务平台 标准计划 20260806-T-469 — https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3"
— and staged `S047` is "JR/T 0276—2023 证券期货业信息系统渗透测试规范". That is exactly why the MSVR document must take
the **lane's** next free id rather than its staged number.

## 5. Renumber map — staged S080 → lane S048, **by document**

Drafting basis (no cell was retyped from memory): the staged row `S080` and the staged entry
`knowledge/corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md` in the read-only package
`/home/vgpnk/Projects/shokuknow/merge/kasegi/` (both read directly — `ScoutPackageThemes`' report was still in flight and
not yet in `wave1/` at drafting time, and the package bytes are the authority either way), plus `ScoutMSVR.md`'s capture
locations, whose line numbers were then re-verified against the landed capture bytes in §6 rather than trusted.

| # | staged S080 cell | landed S048 cell (planned) | why |
|---|---|---|---|
| id | `S080` | `S048` | renumber by document: the lane's next free id is S048 (47 rows, `S048` absent); staged S048 is a different document (§4) |
| source | `Microsoft Security Vulnerability Research — https://www.microsoft.com/en-us/msrc/msvr` | `Microsoft Security Vulnerability Research (MSVR) — https://www.microsoft.com/en-us/msrc/msvr` | URL carried unchanged; the programme's own acronym added from the capture heading L28 (`Microsoft Security Vulnerability Research (MSVR)`) |
| kind | `docs` | `docs` | unchanged |
| tier | `A` | `A` | unchanged — first-party vendor statement |
| scope | prose: "Microsoft's programme for handling vulnerabilities found in third-party products, and the routes by which those findings arrive" | "Microsoft's own programme statement for findings in third-party products: the three intake routes MSVR lists, its coordination of them, and the three roles Microsoft claims for itself" | rewritten to the registry's cell shape and to what the capture actually states (routes + MSVR's coordination + the three roles); the staged phrasing "handling" is dropped because the page states coordination, not a handling process |
| anchor | prose: `the paragraph beginning "MSVR learns about vulnerabilities in third-party products in three ways", with the three routes` | `capture corpus/source-snapshots/round-31/S048.txt: MSVR learns about vulnerabilities in third-party products in three ways (L31) with the three routes at L32-L34, and the three-roles sentence at L35` | capture-anchored with line numbers **verified against the landed capture**, not carried from the staged prose (§6) |
| teaches | `A vendor's own research programme is a third intake route for findings about other vendors' products, handled under coordinated disclosure.` | `A vendor's own research programme is a third intake route for findings about other vendors' products, coordinated by that vendor under its CVD approach rather than by the affected vendor's programme` | keeps the staged lesson, adds the direction (the finder-side vendor coordinates) and attributes the approach to Microsoft (Q4) instead of a generic "coordinated disclosure" |
| status | `mined` | `mined` | unchanged |
| opened | `2026-10-23` | `2026-10-25` | the round that admits it (lane convention; the capture is dated 2026-10-25) |
| recheck | `180d` | `180d` | unchanged; valid cadence, `E09`-clean |
| used-by | `corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md` | `corpus/knowledge/vendor-third-party-finding-coordination.md` | package date-suffixed name → the lane path the F15 entry is being written to (ExecEntryF15); this is the only cell the used-by check reads |

Landed row bytes of the **mirror draft** (single line, 11 cells, NF=13, no `|` inside any cell). Measured, not estimated.
**This digest binds the mirror line only** — the row ExecRegistryAppend-2 landed in `corpus/SOURCES.md` is a different
string with its own digest, recorded in §5b:

```
$ sed -n '54p' .../validate/corpus/SOURCES.md | wc -m ; wc -c          → 793 chars / 795 bytes (row + newline)
$ sed -n '54p' .../validate/corpus/SOURCES.md | sha256sum              → c1edc552ebcfc3b8bf0be852b2557511dfbab3e26d9b86f8618d52b06c7b3db6
$ … | tr -d '\n' | sha256sum                                           → 6034ec28453bb367eeb4aa5c83b484a246df7b608a187cdd7c0d88078bda5c80
$ grep -oP '[^\x00-\x7F]' on the row | sort | uniq -c                  → 1 "—"   (the only non-ASCII char: source-cell em dash)
```

So the row is **794 bytes / 792 chars without the newline, 795 bytes with it**; the two digests above bind those exact
bytes. The fenced row in this receipt is `cmp`-clean against the mirror's line 54 (checked), so the published text and
the hashed text are the same string.

```
| S048 | Microsoft Security Vulnerability Research (MSVR) — https://www.microsoft.com/en-us/msrc/msvr | docs | A | Microsoft's own programme statement for findings in third-party products: the three intake routes MSVR lists, its coordination of them, and the three roles Microsoft claims for itself | capture corpus/source-snapshots/round-31/S048.txt: MSVR learns about vulnerabilities in third-party products in three ways (L31) with the three routes at L32-L34, and the three-roles sentence at L35 | A vendor's own research programme is a third intake route for findings about other vendors' products, coordinated by that vendor under its CVD approach rather than by the affected vendor's programme | mined | 2026-10-25 | 180d | corpus/knowledge/vendor-third-party-finding-coordination.md |
```

## 5a. Cross-check with the registry seats

`corpus/SOURCES.md` has one writer this round: **`agent://ExecRegistryAppend-2`** (round-31). `agent://ExecRegistryAppend`
answered that it is the round-30 seat, declines the path, and reports its own frozen round-30 C2 counter reads `rows==47` —
correct for its round, and a second writer on the path would be the defect. This receipt's handoff therefore goes to
`ExecRegistryAppend-2`, and no lane file was touched by this seat either way.

That seat independently confirmed the anchor lines against the landed capture (L31 route intro, L32-L34 the three routes,
L35 the CVD sentence) — agreeing with §6 below. It also reported a row digest of `1ca202e2…` over a 773-byte string; that
string is **not** this row: the row is 794 bytes without the newline, and a 772-byte string is 22 bytes short of it. The
digest that binds the published mirror bytes is `c1edc552…` (795 B with newline) / `6034ec28…` (794 B without), reproduced
above from the mirror line itself. **That seat has since re-measured and withdrawn the mismatch** — it reproduced
`c1edc552…` / `6034ec28…` on the mirror line and traced its own `1ca202e2…` to a 772-byte truncated inbound paste; its
receipt records the withdrawal and the cause, so the lane inherits no false defect claim. Any seat hashing a row should
re-measure length first: a 772/773-byte length means the copy lost bytes in transit, not that the row is a different row.

## 5b. Landed registry state (measured after `agent://ExecRegistryAppend-2` appended — this is the registry row)

`corpus/SOURCES.md` now carries 48 registry rows with `S048` exactly once, at **line 54**. The round-31 owner,
**`agent://ExecRegistryAppend-2`** (the FILE OWNERSHIP seat for `corpus/SOURCES.md`), did **not** append my mirror draft
byte-for-byte: it rewrote the scope, anchor and teaches cells (its own wording, its own limits), keeping the id, source,
kind, tier, status, opened, recheck and used-by. `agent://ExecRegistryAppend` is the **round-30** instance, made no write
to this path in round 31, and contributed read-only verification only — one writer, one write. Measured on the landed
bytes:

Size convention (so a later verifier does not file a phantom off-by-one): `sed -n '54p' … | wc -m` counts the newline and
prints **914**; `printf '%s' "$(sed -n '54p' …)" | wc -m` prints **913**; `wc -c` prints **916**. So the row is **913 chars
/ 915 bytes without the newline and 914 chars / 916 bytes with it**; the 2-byte excess of bytes over chars is the single
em dash (U+2014, 3 bytes) in the source cell. The mirror row in §5 follows the same convention (792 chars / 794 bytes
without the newline, 793 / 795 with it).

```
$ grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md          → 48
$ grep -cE '^ {0,3}\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md                → 1
$ grep -nE '^ {0,3}\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md                → 54   (## Paths starts at 56 → no E12)
$ sed -n '54p' corpus/SOURCES.md | wc -m ; wc -c                                      → 914 chars / 916 bytes (row + newline; see convention above)
$ sed -n '54p' corpus/SOURCES.md | sha256sum                                          → 0f2d9cb61c8743577476906fb6ea2a9285082931e5ff811dac98d0f26f83de7a
$ … | tr -d '\n' | sha256sum                                                           → db871511b56e841de8cdc22127526d59b44a9439f239a391728e98d0d680e0a2
$ ls -l corpus/knowledge/vendor-third-party-finding-coordination.md                    → present, 11501 B (E11 resolves)
$ sha256sum corpus/SOURCES.md                                                          → 5a03c696312bd5fd8fe8307f75bd9723cac97fe3e44f0f3ba46a68607295f6f5
$ sed -n '72p;94p' corpus/SOURCES.md                                                   → search-log entry "Vendor third-party-finding coordination sweep (round 31) …" (L72)
                                                                                          and R8 line "- S048 row added: new row (id `S048`, kind `docs`, tier A scoped to …)" (L94)
```

**Landed row** (`corpus/SOURCES.md:54`, sha256 `0f2d9cb6…`, 915 B without newline):

```
| S048 | Microsoft Security Vulnerability Research (MSVR) — https://www.microsoft.com/en-us/msrc/msvr | docs | A | Microsoft's own statement of its MSVR programme and of nothing beyond it: the three third-party intake routes it lists, its coordination of them, and the three CVD roles it claims for itself | capture corpus/source-snapshots/round-31/S048.txt: heading Microsoft Security Vulnerability Research (MSVR) L28, purpose L29-L30, three-ways lead-in L31, routes L32-L34, three-roles sentence L35; page shows no visible publication or revision date, opened 2026-10-25 | Microsoft's MSVR states it learns of third-party-product vulnerabilities through its own engineers (L32), external MSRC reports (L33) and internal research (L34), and names itself finder and multi-vendor coordinator under its CVD approach (L35). | mined | 2026-10-25 | 180d | corpus/knowledge/vendor-third-party-finding-coordination.md |
```

Live gate on the landed registry (read-only `--file` run, this seat):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$PWD/corpus/SOURCES.md"
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
live_exit=0
```

Delta, mirror draft → landed row (all three rewritten cells still satisfy the checks that matter):

| cell | mirror draft | landed | check |
|---|---|---|---|
| scope | "Microsoft's own programme statement for findings in third-party products: the three intake routes MSVR lists, its coordination of them, and the three roles Microsoft claims for itself" | "…and of nothing beyond it… the three third-party intake routes it lists, its coordination of them, and the three CVD roles it claims for itself" | landed adds an explicit page-level limit ("nothing beyond it"), which matches ScoutMSVR's finding that the page carries no finer-grained coordination process; no `\|`, E01-clean |
| anchor | capture + L31 / L32-L34 / L35 | capture + heading L28, purpose L29-L30, lead-in L31, routes L32-L34, roles L35, plus "no visible publication or revision date" | **verified against the capture in §6**: L28 is the heading line, L29 and L30 are the two purpose paragraphs, L31 the lead-in, L32-L34 the routes, L35 the roles — every landed line claim is true of the bytes |
| teaches | "…coordinated by that vendor under its CVD approach rather than by the affected vendor's programme" | "…learns of third-party-product vulnerabilities through its own engineers (L32), external MSRC reports (L33) and internal research (L34), and names itself finder and multi-vendor coordinator under its CVD approach (L35)." | each route attribution is the capture's own line; keeps Microsoft as the stating party (Q4) |

Registry effect confirmed by the instrument: 48 rows, and the only findings are the two pre-existing W04 warnings — the
landed row adds no E-code (no E03, E04, E11, E01, E12). `c1edc552…` therefore describes **my mirror draft only**; the
registry row is `0f2d9cb6…`, and this receipt no longer implies the two are equal.

Owner-side obligations, checked read-only on the current landed file (`corpus/SOURCES.md` sha256 `5a03c696…`) and **closed**:
the R8 registry-changes line for the append is present at L94 ("- S048 row added: new row (id `S048`, kind `docs`, tier A
scoped to …"), and the round-31 search-log entry is present at L72 ("Vendor third-party-finding coordination sweep
(round 31) …"). The row itself sits at L54, above `## Paths` at L56, so E12 does not fire. The validate re-run on these
final bytes (read-only `--file`) is again exit 0 with only W04 S028/S029, so the later lines did not disturb the gate.
`agent://ExecRegistryAppend` had flagged the R8 line and search-log note as still owed; that flag is stale as of these
bytes, and this seat measured it rather than taking either seat's word for it.

## 6. Anchor line numbers checked against the capture bytes (not retyped)

```
$ awk 'NR>=28 && NR<=36 {printf "%d: %s\n", NR, $0}' corpus/source-snapshots/round-31/S048.txt
28: Microsoft Security Vulnerability Research (MSVR)
31: MSVR learns about vulnerabilities in third-party products in three ways:
32: Internal Microsoft engineers: … These vulnerabilities are reported to the MSVR team, which then works with the affected vendor to fix the issue.
33: External reports to the Microsoft Security Response Center (MSRC): … These issues are coordinated by MSVR.
34: Internal research projects: … Any issues are reported to the affected vendor under accepted Coordinated Vulnerability Disclosure practices.
35: This coordination takes place under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach. CVD clarifies how Microsoft responds as a vendor affected by vulnerabilities in its products and services, as a finder of new vulnerabilities in third-party products and services, and as a coordinator of vulnerabilities that affect multiple vendors.
```

Occurrence counts of the strings the row relies on (`grep -cF`, each 1): the L31 route-intro sentence; each of the three
route lead-ins; `as a coordinator of vulnerabilities that affect multiple vendors`. The mirror row's anchor claim (L31
intro, routes L32-L34, three-roles sentence L35) matches the capture exactly, and so does the **landed** row's wider claim
(§5b): L28 is the `Microsoft Security Vulnerability Research (MSVR)` heading line, L29 and L30 are the two purpose
paragraphs, L31 the three-ways lead-in, L32-L34 the three routes, L35 the CVD sentence carrying the three roles. Its
teaches cell's line attributions — engineers L32, external MSRC reports L33, internal research L34, finder/coordinator L35
— are the same lines.

## 7. Verdict

**PASS — the planned S048 row is admissible on the lane's registry contract, the lane had no id or URL obstacle to it, and
the row has since landed (registry 48 rows, `S048` exactly once, live validate exit 0).**

- Gate: `sources-census.sh validate --file <mirror>/corpus/SOURCES.md` → **exit 0**, findings = the two pre-existing
  W04 warnings only; PRE (row absent) is identical, so the row contributes no finding.
- Landed: `corpus/SOURCES.md` line 54, 48 registry rows, `S048` exactly once, live `validate --file` → **exit 0** with only
  W04 S028/S029; landed row sha256 `0f2d9cb6…` (916 B with newline), used-by path present (11501 B) — §5b.
- Refusal classes the seat was told to refuse (E03 duplicate id, E04 duplicate URL) both fire at exit 1 on this exact row
  shape in the controls, together with E11 — the gate discriminates.
- Live-lane extractor reproduces `reg-ids` (47), `staged-ids` (94) and `collisions` (17, S031–S047) byte-for-byte, and
  `guard-proof-collisions` (`S031`) byte-for-byte.
- S048 is free as an id and the MSVR URL is on no lane row (census-native: no E04/W04 for S048 across 48 rows).
- Registry figure the append must reach: **47 → 48** rows, mined 35 → 36, tier.A 44 → 45.

Handoff **closed**: `agent://ExecRegistryAppend-2` (the round-31 registry seat — `ExecRegistryAppend` is the round-30
seat and declined the path, §5a) appended a row of its own wording; §5b records the landed bytes (`0f2d9cb6…`, line 54),
the cell delta against my draft, and the live `validate --file corpus/SOURCES.md` → **exit 0, 48 rows, only W04
S028/S029**. Every anchor line the landed row cites (L28 heading, L29-L30 purpose, L31 lead-in, L32-L34 routes, L35 roles)
was checked against the capture bytes, and its used-by path resolves (`corpus/knowledge/vendor-third-party-finding-coordination.md`,
11501 B). Still outside this seat: the `--root … kasegi` run and the C2 counter figures, which belong to the L1 and to C2.
Do not copy the row from the staged package: the staged S080 cells and used-by path differ in five columns (§5).

## 8. Limits (what this receipt does not establish)

- The mirror run proves the row is admissible and that the gate discriminates. The **landed** registry was then validated
  read-only by this seat (`--file corpus/SOURCES.md` → exit 0, 48 rows, W04 S028/S029 only, §5b); the `--root … kasegi`
  run and C2's counter figures remain ExecRegistryAppend-2's and the L1's.
- The mirror's `instruments/`, `knowledge/` and capture copies are fidelity scaffolding; no instrument ran on them, and no
  result here depends on their bytes beyond the used-by path resolution and the anchor line numbers.
- The in-flight capture (`2001ad77…`, 97 lines) is owned by ExecCapManifest and may change; if it does, the anchor's line
  numbers must be re-checked against the landed bytes (this receipt checked the bytes it copied, and the capture's own
  Trace-Id line makes refetch digests non-reproducible — the manifest pins the committed bytes).
- The guard-proof producer is reconstructed, not known: two byte-equal producers are shown above; the file's content is
  treated as data, not as an instruction.
- Nothing here asserts a score move. C2's before/after numbers are the L1's to measure on quiescent bytes.
