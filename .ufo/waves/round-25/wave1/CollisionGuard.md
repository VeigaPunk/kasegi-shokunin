# CollisionGuard — §10 id-collision guard proved, renumber map produced

Lane: kasegi-shokunin. Round 25, wave 1 (build). Base revision `b49948f1`.
Owner of this seat: the §10 assimilation collision check only. No production file was edited;
no registry row was appended; nothing was renumbered outside scratch.

## 1. Files written (all inside my scope)

| path (lane-relative) | what |
|---|---|
| `.ufo/waves/round-25/assimilation/ids/reg-ids` | 35 lane registry ids, produced by the campaign command |
| `.ufo/waves/round-25/assimilation/ids/staged-ids` | 94 staged ids, produced by the campaign command |
| `.ufo/waves/round-25/assimilation/ids/collisions` | `comm -12` of the two lists: 5 ids |
| `.ufo/waves/round-25/assimilation/ids/guard-proof.txt` | command-by-command failure-mode proof (indented fixture) |
| `.ufo/waves/round-25/assimilation/ids/guard-proof.sh` | the generator for that transcript, so the proof is re-runnable |
| `.ufo/waves/round-25/assimilation/ids/fixture/fixture-SOURCES.md` | fixture registry with `  \| S002 \|` indented two spaces |
| `.ufo/waves/round-25/assimilation/ids/fixture/fixture-staged.md` | fixture staged set carrying `S002` at column 0 |
| `.ufo/waves/round-25/assimilation/ids/fixture/{a,b}-{reg,staged,collisions}` | the four id lists + two collision sets the proof compares |
| `.ufo/waves/round-25/assimilation/ids/renumber-map.md` | the adopted map, keyed by document |
| `.ufo/waves/round-25/wave1/CollisionGuard.md` | this report |

Read-only inputs: `corpus/SOURCES.md`, `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`.
No campaign tool was run in `shokuknow`; only `grep` read it.

## 2. The collision check, run exactly as specified

Lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, `S=/home/vgpnk/Projects/shokuknow`,
`A=.ufo/waves/round-25/assimilation/ids`:

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/kasegi/SOURCES.append.md" | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```

Line counts and collision content, verbatim:

```
$ wc -l .ufo/waves/round-25/assimilation/ids/reg-ids .ufo/waves/round-25/assimilation/ids/staged-ids .ufo/waves/round-25/assimilation/ids/collisions
 35 .ufo/waves/round-25/assimilation/ids/reg-ids
 94 .ufo/waves/round-25/assimilation/ids/staged-ids
  5 .ufo/waves/round-25/assimilation/ids/collisions
134 total

$ cat .ufo/waves/round-25/assimilation/ids/collisions
S031
S032
S033
S034
S035
```

`reg-ids` = S001–S035 contiguous; `staged-ids` = S031–S124 contiguous (94 rows).

**Collision count: 5 (S031–S035).** This matches the expected figure. It also cross-checks
against round 24's lesson, which recorded lane max S031 / 1 collision (S031): the lane has since
appended S032–S035 (NIST SP 800-115, e-Gov lawdata, 総務省, 警察庁), so the overlap grew from 1
to exactly 5. The check is behaving as the guard's own history predicts.

## 3. No collision falls on an adopted row

Adopted staged ids are S055, S056, S057, S060, S068 — all above the registry head S035, hence
outside the collision set. Measured, not inferred:

```
$ for id in S036 S037 S038 S039 S040; do printf '%s=%s ' "$id" "$(grep -cE "^ {0,3}\|[[:space:]]*$id " corpus/SOURCES.md)"; done
S036=0 S037=0 S038=0 S039=0 S040=0

$ for u in <each adopted URL>; do grep -cF "$u" corpus/SOURCES.md; done
0 0 0 0 0
```

So every target lane id is free, and none of the five adopted documents is already registered
under another lane id (the case that would make "follow the document" produce a duplicate).

Every one of the 5 collisions is an **id-space** collision, not a duplicate document — each lane
id and its staged namesake carry different URLs. Verbatim URL pairs:

| id | lane | staged | same document? |
|---|---|---|---|
| S031 | CVE CNA Rules v4.2.6 `https://www.cve.org/Resources/Roles/Cnas/CNA_Rules_v4.2.6.pdf` | HackerOne `https://hackerone.com/security/policy_versions` | NO |
| S032 | NIST SP 800-115 `https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf` | Bugcrowd VRT README `https://raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy/master/README.md` | NO |
| S033 | e-Gov lawdata `https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128` | Bugcrowd VRT CWE map `…/master/mappings/cwe/cwe.json` | NO |
| S034 | 総務省 `https://www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/` | CNVD 众测 `https://zc.cnvd.org.cn/news/helpList` | NO |
| S035 | 警察庁 `https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf` | 360SRC `https://security.360.cn/Reward/rules` | NO |

This is the concrete reason the map must be per-document: reading a staged id as a lane id, or
shifting by a constant, would bind lane ids to the wrong documents.

## 4. The guard can fail — indented-row proof

Fixture: `.ufo/waves/round-25/assimilation/ids/fixture/fixture-SOURCES.md` holds
`  | S002 | Fixture Document Beta …` indented two spaces (line 10);
`fixture-staged.md` carries `| S002 | …` at column 0. The same two greps were run over the
fixture pair. Both commands and their outputs, verbatim from `guard-proof.txt`:

**A. Guard pattern, `^ {0,3}\|` — collision detected**

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' .ufo/waves/round-25/assimilation/ids/fixture/fixture-SOURCES.md | grep -oE 'S[0-9]+' | sort > .ufo/waves/round-25/assimilation/ids/fixture/a-reg-ids
[exit 0]
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' .ufo/waves/round-25/assimilation/ids/fixture/fixture-staged.md | grep -oE 'S[0-9]+' | sort > .ufo/waves/round-25/assimilation/ids/fixture/a-staged-ids
[exit 0]
$ comm -12 .ufo/waves/round-25/assimilation/ids/fixture/a-reg-ids .ufo/waves/round-25/assimilation/ids/fixture/a-staged-ids > .ufo/waves/round-25/assimilation/ids/fixture/a-collisions
[exit 0]
a-reg-ids    lines=2
S001 S002
a-staged-ids lines=2
S002 S003
a-collisions lines=1
$ cat .ufo/waves/round-25/assimilation/ids/fixture/a-collisions
S002
```

**B. Column-zero-only pattern, `^\|` — collision MISSED**

```
$ grep -oE '^\|[[:space:]]*S[0-9]{3,}' .ufo/waves/round-25/assimilation/ids/fixture/fixture-SOURCES.md | grep -oE 'S[0-9]+' | sort > .ufo/waves/round-25/assimilation/ids/fixture/b-reg-ids
[exit 0]
$ grep -oE '^\|[[:space:]]*S[0-9]{3,}' .ufo/waves/round-25/assimilation/ids/fixture/fixture-staged.md | grep -oE 'S[0-9]+' | sort > .ufo/waves/round-25/assimilation/ids/fixture/b-staged-ids
[exit 0]
$ comm -12 .ufo/waves/round-25/assimilation/ids/fixture/b-reg-ids .ufo/waves/round-25/assimilation/ids/fixture/b-staged-ids > .ufo/waves/round-25/assimilation/ids/fixture/b-collisions
[exit 0]
b-reg-ids    lines=1
S001
b-staged-ids lines=2
S002 S003
b-collisions lines=0
$ cat .ufo/waves/round-25/assimilation/ids/fixture/b-collisions
                       # empty: 0 bytes, no output
```

`a-collisions` is 5 bytes (`S002\n`); `b-collisions` is 0 bytes. The 0-3-space form reports the
duplicate; the column-zero-only form sees one registry row instead of two and reports nothing,
so the indented duplicate would be appended silently. That is the failure mode the guard exists
to catch, and it is reproducible via `bash .ufo/waves/round-25/assimilation/ids/guard-proof.sh`.

Latent-risk note from the same transcript: both real inputs carry **0** indented rows today
(`grep -cE '^ {1,3}\|…'` → 0 on each, exit 1), and both patterns agree at 94 / 35. The guard's
0-3-space form is not redundant — it is the form that still works after the first indented paste.

## 5. Renumber map (`.ufo/waves/round-25/assimilation/ids/renumber-map.md`)

One line per adopted row, id following the document:

| staged id | new lane id | document title |
|---|---|---|
| S055 | S036 | 脆弱性情報ハンドリングポリシー (Cybozu) |
| S056 | S037 | FAQ（脆弱性報奨金制度） (Cybozu) |
| S057 | S038 | 脆弱性報告制度 (GMO Pepabo) |
| S060 | S039 | 日立グループにおける製品脆弱性情報の開示プロセス（HIRT-PUB10008） (Hitachi) |
| S068 | S040 | Cisco Security Vulnerability Policy (Cisco) |

The map also carries each document's URL and fixing anchor, and states the invariants: identity is
the (URL, anchor) pair; no constant offset reproduces the map (offsets 19, 19, 19, 21, 28 because
the staged ids skip non-adopted rows); renumbering is a projection so non-adopted staged ids never
become lane ids; and the map must be applied to entry `source:` headers, since the C2 counter greps
`^source: S0(3[6-9]|[4-9][0-9])`.

## 6. Risks and open items for the L1

1. **S068's adoption is contingent.** `claims.json` records
   `planned_reject: vendor-cvd-policy-crosswalk-2026-10-23.md (S068 Cisco policy unreachable this
   round)`, while my assignment's adoption set includes `S068->S040`. I mapped it as instructed and
   flagged the contingency in the map itself: because the map is per-document, dropping S068 leaves
   S040 free and does not shift the other four. If S068 is rejected, the map needs no rewrite.
2. **Filename divergence from the guard's own record.** `corpus/lessons/round-24.md` names the map
   `assimilation/renumber-map.tsv`; this assignment specifies `renumber-map.md`. I wrote `.md` only
   (my write scope is `assimilation/ids/**`). If the next lesson cites the file, it must cite `.md`
   or the L1 should add the `.tsv` form deliberately — I did not create a second format silently.
3. **A stray write outside the lane, created and removed.** My first two fixture writes used
   lane-relative paths, and the `write` tool resolved them against the session cwd
   (`/home/vgpnk/Projects/shokunin`), creating `/.ufo/waves/round-25/assimilation/ids/` at the fleet
   root. I verified that tree contained only my three files (created 05:26, nothing else), removed it
   with `rm -rf /home/vgpnk/Projects/shokunin/.ufo/waves/round-25`, and confirmed the path no longer
   exists; all lane files were then rewritten with absolute paths. Fleet root is restored, but the
   L1 should know the incident happened. No `.ufo/state`, `MANIFEST.json`, template or fleet script
   was touched at any point.
4. **Unrun checks are not claimed.** I ran no census, no `recheck-audit.py`, no build/lint/test —
   this seat's output is the three id lists, the guard proof and the map. The C1/C2 counters belong
   to their own seats.

## 7. Tooling

None installed or upgraded. `grep`, `comm`, `sort`, `wc`, `od`, `awk`, `bash` from the base system;
no `pacman` transaction was attempted (host-wide pause respected).
