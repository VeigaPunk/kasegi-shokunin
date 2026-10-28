VERDICT: HOLDS

# R46ScoutAdjacent — adjacency sweep for F28 (GitHub private vulnerability reporting)

Scope: read-only lexical sweep of sibling lanes' corpora and skills for `private vulnerability`, `privately report`, `GHSA`, `security advisor`, `SECURITY.md`, `vulnerability reporting`, `report a vulnerab`, `private fork`; plus the lanes named in the seat spec (kake, kagi, kumitate, chousa). Baseline is the frozen kasegi base 914ca0b (exported read-only to scratch, removed on exit). No file outside this report was written.

## 1. Claim: no sibling lane holds reporter-side GitHub private vulnerability reporting ground

Commands and printed output:

```
$ for l in *-shokunin; do c=$(grep -rlEi 'private vulnerability|privately report|GHSA|security advisor|SECURITY\.md|vulnerability reporting|report a vulnerab|private fork' "$l/corpus" --exclude-dir=.ufo --exclude-dir=.git --exclude-dir=__pycache__ | wc -l); s=$(grep -lEi '<same terms>' "$l/SKILL.md" | wc -l); [ "$c$s" != 00 ] && echo "$l corpus=$c skill=$s"; done
kaidoku-shokunin corpus=3 skill=0
kama-shokunin corpus=2 skill=0
kasegi-shokunin corpus=55 skill=0
kotoba-shokunin corpus=1 skill=0
mori-shokunin corpus=6 skill=0
revenger-shokunin corpus=3 skill=0
tabi-shokunin corpus=4 skill=0
```

Triage of every listed sibling hit (kaidoku, kama, kotoba, tabi lines printed with `grep -rnEi`): all are non-relevant lexical noise — `private fork-exec` (kama-shokunin/corpus/lessons/round-15.md:236), `security.md` inside a tar listing (kaidoku-shokunin/corpus/evidence/round-42/local-sources/S048/rea-agents-6.5.0-cited-members.tar:17719), a FreeBSD nav link `Security Advisories` (kaidoku-shokunin/corpus/evidence/round-49/c2/freebsd-sysexits.html:1224), `security.md` URL path (kotoba-shokunin/corpus/lessons/round-68.md:111), and vendored node_modules text in tabi-shokunin/corpus/evidence/round-13/aria/node_modules/... plus a GitHub rate-limit page (tabi-shokunin/corpus/evidence/round-31/decision-table/bytes/S121.html:151). None is a disclosure-channel claim.

Corpus/knowledge-level sweep of the four named lanes (`grep -rniE` on corpus/knowledge, SOURCES.md, SKILL.md) returned zero advisory-channel hits in kake, kagi, kumitate and chousa. The sibling hits that carry real ground are listed in §2.

Positive control (grep reaches the publisher-side security.txt ground): `grep -rliE 'security\.txt' kake-shokunin/corpus/knowledge` → `kake-shokunin/corpus/knowledge/security-txt-publishing.md`.
Negative control (empty lane): `grep -rliE "$P" audio-shokunin/corpus | wc -l` → `0`.
Do-nothing control (kasegi base 914ca0b, the frozen state): export via `git -C kasegi-shokunin archive 914ca0b... corpus SKILL.md | tar -x -C <scratch>`, then
```
$ grep -rliE 'private vulnerability reporting|privately report' <scratch>/corpus/knowledge <scratch>/corpus/SOURCES.md <scratch>/corpus/README.md | wc -l
0
$ grep -rliE 'private vulnerability reporting|privately report' <scratch>/corpus | wc -l
0
```
This reproduces the C2 base reading (`grep -rliE ... corpus/knowledge corpus/SOURCES.md corpus/README.md prints nothing`). Working-tree note: the kasegi checkout HEAD is 323d1f5, not the freeze 9f23aab; the 4 working-tree hits for the same grep are the freeze-committed r46-c2-gate.py (line 5), its __pycache__ copy, and the committed S073 capture/manifest (source-snapshots/round-46/S073.txt:1,556-579; manifest.json:23). None is in the base.

## 2. What each lane holds (path:line)

- kasegi (own lane, pre-existing ground F28 must cite and not duplicate):
  - S067 curl CVE-2025-9086 advisory (corpus/SOURCES.md:73) and S068 GitHub Advisory Database entry GHSA-v676-f8gm-92r9 (corpus/SOURCES.md:74, tier B, "carrying the database's own status and metadata cells rather than a project-written report"). S068 is the published advisory-database record, not a reporter flow.
  - S055 CSAF/VEX standard (corpus/SOURCES.md:61) and F21 (corpus/README.md:477): "Common Security Advisory Framework" — a machine-readable advisory format, not a reporting channel.
  - F10 vendor-side disclosure policies (corpus/README.md:211; knowledge/vendor-disclosure-policy-commitments-crosswalk.md; S036-S040). This is the nearest held ground: a vendor policy "commits to a clock, not to a scope" (crosswalk header).
  - F27 Linux kernel security-bugs e-mail channel (corpus/README.md:651; knowledge/linux-kernel-security-bugs-reporting-process.md:9, S071.txt:95-96 on AI-found bugs). F04 AI-assisted finding validation (corpus/README.md:205).
  - RFC 9116 security.txt discovery (knowledge/rfc-9116-security-txt.md:8, :47; S063). Its own line-47 boundary: "This is the RFC drawing F10's line: `security.txt` answers where to report … the disclosure policy page answers what a researcher may and may not do …".
  - Channel-in-practice: knowledge/vdp-disclosure-packages.md:13 (security.txt Contact → HackerOne `embedded_submissions`, not a bounty form); knowledge/submitted-registry.md:90.
  - SECURITY.md text: no kasegi row. S050 (Claude-Red SECURITY.md) lives in revenger, see below.
- kake (web properties / publishing side of security.txt):
  - knowledge/security-txt-publishing.md:4 — "Nothing here says what an operator-owned property serves." :65-72 — "What the file covers … coverage is answered by the publisher's deployment and Policy link."
  - S084 (corpus/SOURCES.md:92) GitHub's served /.well-known/security.txt, with a `Policy` field; S085 Google's served file (:93); S078 RFC 9116 (:86).
  - Hit: kake-shokunin/corpus/knowledge/response-header-expectations.md:1 and corpus/SOURCES.md:177 — Content-Security-Policy / HSTS only (false positives for "security policy").
- kagi (secrets & vault):
  - S048 GitHub Secret Protection, secret detection versus validity checks (corpus/SOURCES.md:55; opened-lead note corpus/SOURCES.md:74, corpus/README.md:241). S047 OIDC (:54). Zero knowledge entries on secret scanning (grep of corpus/knowledge for `secret.scanning|secret protection|push protection` → no output). kagi holds no advisory or reporting ground.
- kumitate (orchestration): zero corpus advisory-channel hits. Its `advisory` hits (e.g. knowledge/dispatch-shapes.md:8, kimi-modes-machinery.md:179) are the word in its dispatch sense.
- chousa (research method): zero corpus advisory-channel hits. Its SKILL.md:10 states the boundary: "Not the bounty programs (kasegi) and not model-quality claims (kengaku)". Its `disclos` hits (chousa-shokunin/corpus/knowledge/hardening-r10.md:701, metadata-screen-r25.md:45) are research-record disclosures.
- revenger: corpus/SOURCES.md:64 S050 — "Claude-Red SECURITY.md (maintainer intended-use and disclosure policy)" — the authorized-testing boundary and disclosure window of one third-party repo; corpus/SOURCES.md:145 bounty-triage training note. This is a SECURITY.md policy held as a source; F28 must not restate it.
- mori: corpus/SOURCES.md:18 S012 GHSA-652q-wxr6-h5j6 (systemd-oomd advisory), and knowledge/userspace-oom-killers-r12.md:24: "GHSA-652q-wxr6-h5j6 is adjacency only: patch-state assessment belongs to tsukuroi and is not absorbed by this entry."
- tsukuroi (named by mori): the corpus holds no GHSA token (grep `GHSA|advisor` over tsukuroi-shokunin/corpus returns only generic words). Its nearest row is corpus/SOURCES.md:35 S029 "Arch Linux Security Tracker" (package vulnerability status). So mori's delegation of GHSA patch-state to tsukuroi points at ground tsukuroi does not hold as a GHSA row. Dangling pointer, not F28's to absorb; report to mori/tsukuroi owners.

## 3. Boundary sentence for F28 (proposed text)

Stays kasegi's: the reporter-side flow of a repository's built-in private vulnerability reporting form as a disclosure channel — when the owner has enabled it, what the reporter must supply, the optional AI-assistance disclosure, the automatic collaborator and credit, and the maintainer-only merge path from the temporary private fork — treated as a channel, not a grant of permission (the rfc-9116 line-47 rule, applied to the form).

Only reported, never restated as F28 ground: the repository's SECURITY.md policy text and its disclosure window (revenger S050; kasegi F10 for vendor policies); the security.txt pointer and its serving (kasegi rfc-9116 entry; kake security-txt-publishing); the published GHSA advisory record and its CVE/severity cells (kasegi S068 as a reference only); secret detection and validity (kagi S048); advisory patch state (mori's pointer to tsukuroi); orchestration of any triage queue (kumitate); research method (chousa SKILL.md:10).

## 4. Limitations

- Lexical sweep only: English terms; Japanese vendor-report phrasing (脆弱性報告, 報告窓口) was not swept across siblings. kasegi's own Japanese entries (F10 crosswalk: Cybozu, Pepabo, Hitachi) were read only by their knowledge headers.
- `.ufo/waves/` lane-internal records were excluded by design; they are not corpus ground.
- The sweep reads the working trees; sibling HEADs were not pinned. Sibling SKILL.md descriptions were read at their current revision.
- No live fetch of GitHub's PVR page was made (the S073 capture at freeze is the only source; not re-fetched, per the live-target refusal).
- I did not run the frozen C1 or C2 counters or the controls; that is other seats' single item. I did not build the F28 entry or the C1 re-grounds; the milestone line is lane-level and my seat is the adjacency sweep.
- The grep is over-broad (CSP, "security advisories" nav text, "private fork-exec"); every hit listed here was read, not counted as evidence.

## 5. Install/update record

None. No tool was installed or upgraded. Scratch `$HYAKU_SCRATCH/kasegi-r46/R46ScoutAdjacent/` (default /fast/scratch/hyaku) held only the base export and was removed on exit. No git mutation, no commit, no write outside this report.
