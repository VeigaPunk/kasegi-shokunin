# ScoutSiblingF22 — receipt (round 39, wave 1)

Seat: read-only cross-lane sweep for F22 ground. Leaf, no tools installed, no network fetch, no git/jj mutation. Scratch `/fast/scratch/hyaku/kasegi-r39/ScoutSiblingF22/` removed on exit. Disk guard green before the heavy pass (`/fast/scratch/hyaku/` 25% used). Run at 2026-10-26T19:33Z; kasegi lane HEAD read as `d65d823e7c84813c192b20ee757a8761f878a61f` (untracked round-39 build files present; nothing of mine in the lane except the two wave1 files).

## Deliverable

`.ufo/waves/round-39/wave1/ScoutSiblingF22.sibling.md` — 11 lines, sha256 `15eeff068ca12a61885681504fac31e7c9f72d4231d617b1c5dd3559a012b961`. Landable ruling text only (one `###` heading plus bullets); no validation material in it.

## Ruling

No sibling lane and no shokuknow merge row holds the VEX issuance / lifecycle / reaffirmation / inheritance ground. F22 (S057) is a first write. kake's `security-txt-publishing.md:63` `CSAF` mention stays adjacent, as ruled in round 38.

## Method (commands as run)

Sibling set = `ls -d *-shokunin | grep -v '^kasegi-shokunin$'` at the fleet root = 20 lanes: audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi. (`ok/`, `research/`, `scripts/`, `templates/` are not lanes.) Every one has a `.git`.

```
cd /home/vgpnk/Projects/shokunin
rg -n --no-heading -uu -g '!.git' -g '!.jj' -g '!.ufo' -e "<pat>" $L      # L = the 20 lanes
rg --files -uu -g '!.git' -g '!.jj' -g '!.ufo' $L | wc -l                  # 829134 files searched
cd /home/vgpnk/Projects/shokuknow
rg -n -uu -g '!.git' -g '!.jj' -e '\bVEX\b' -e 'When to Issue|when-issue-vex|when_to_issue' -e '\bCISA\b' -i -e 'exploitability exchange' -e '\bCSAF\b' .
rg --files -uu -g '!.git' merge | wc -l    # 1646 ;  whole tree 24415
```

`-uu` includes hidden and gitignored files (kotodama `.scratch/` copies are searched and counted as duplicates below).

## Results per pattern (siblings)

| Pattern | Hits | Disposition |
|---|---|---|
| `When to Issue\|when-issue-vex` | 0 | — |
| `when to issue\|when-issue\|issue vex\|vex information\|issuance` (ci) | 40 shown | kagi `corpus/SOURCES.md:68` (Vault lease issuance); kotodama `d4-typed-labels` yml/py (cultural "issuance and recall") and Persepolis texts (oip92.txt "issuance of rations"). Not VEX. |
| `\bVEX\b` (case-sensitive) | 0 | — |
| `\bVEX\b\|\bvex\b` (ci) | 39 | All kotodama: 16 files of dictionary/OCR text (`reports/supplement-opencode-1/scratch/...`: grein_handy_dict_1886.txt 13, gragas_finsen_1852.txt 10, sweet_student_dict_1897.txt 2, bright_reader_1891.txt 2, one each in gollancz_exeter_v1/v2, gummere, gummere_djvu.xml, origines_islandicae, clauson-edpt, hj1886, hj1903) plus `reports/round-60/captures/pages/S619.txt:5054` and its three `.scratch/{base,smoke,eval-base}` copies. The verb "vex"/Old-Norse "vex". |
| `\bCISA\b` | 2 + 1 | `kake-shokunin/corpus/lessons/round-35.md:58` (BOD 20-01 template proposed for rejection; kasegi holds BOD 20-01 as S021); `kake-shokunin/corpus/SOURCES.md:255` (round-35 question line naming CISA as a host); `kotodama .../hj1886_djvu.txt:60267` ("cisa" inside OCR botany text, ci match). None is VEX. |
| `\bWEX\b\|\bwex\b` | 12 | kagi `corpus/checklist-run.sh:412,417,418` (shell variable `wex`); the rest kotodama Old English "wex" (`bright_reader_1891.txt:30127`, `S619.txt:5133,5217` and the three `.scratch` copies each). Not VEX. |
| `CSAF\|OpenVEX\|CycloneDX\|VDR\|NOT_AFFECTED\|not_affected\|reaffirm` | 57 | Only `kake-shokunin/corpus/knowledge/security-txt-publishing.md:63` matches CSAF (adjacent, round-38 ruling). `mori-shokunin/corpus/evidence/sources-r31/S167.src:347,372` is `PR_SPEC_NOT_AFFECTED` in kernel C. The rest are the English word "reaffirm" in kotodama/tsukuroi/tabi (a minified JS bundle line). |
| `exploitability exchange\|CSAF\|SBOM\|software bill of materials\|openvex\|cyclonedx\|secvisogram\|vulnerability disclosure\|vulnerability exploitab` (ci) | several | kake `security-txt-publishing.md:63` (CSAF) and `SOURCES.md:86` (RFC 9116 row); kaidoku SBOM hits (`2026-10-13-ghidra-install.md:15,19`, `2026-10-13-r4-14-libsignal.md:5,31,37,87`, `corpus/README.md:25`): reverse-engineering "SBOM" of a binary, not an issuance layer; chousa `SCORECARD.md:1037,1069,1123` and `LOG.md:761` ("vulnerability disclosure" search terms); mori and kotodama HHS/GitHub "Vulnerability Disclosure" nav-link text; kaidoku evidence envelopes (JSON sha lines). No VEX issuance content. |

Positive control: the same sibling command re-found kake `security-txt-publishing.md:63` for CSAF, so the sweep reaches a known site.

## shokuknow (read-only)

- `merge/` (1,646 files): no `VEX`, no `When to Issue`, no CSAF. Only adjacent hit: `merge/kasegi/SOURCES.append.md:76` ("vulnerability exploitability classification, according to Appendix A" — GB/T 30279 recheck line, a Chinese national standard, not VEX) and the merge copy `merge/kasegi/knowledge/corpus/knowledge/gb30279-2020-english-edition-front-matter.md`.
- `doctrine/channel-recurrence.md:62` — `cisa.gov` → kasegi (ownership row, not content).
- `lanes/kasegi/` (kasegi's own staging lane, not a sibling): CISA mentions in `DOMAIN.md:41,59,60`, `CHANNELS.md:14`, `CANNOT-ANSWER.md:148`, `round7/KNOWLEDGE-PROPOSED.md:4`, `.deepresearch/20261023_171716_kasegi-bounty-program-sources/final_turn_001.md:5`; no VEX text.
- `.ufo/waves/corpus-expansion-1/.qcache/` unrelated pages: Docker `docker scout vex` reference (`24698539df5a7ecc9df58c1a.txt:963,967`, `6ca35cbd69e75cb12333b848.txt:963,967`; Docker Compose and Dockerfile reference pages), OWASP FSTM Japanese (`e782b292201785a25be63092.txt:467,469,570,603,605,615`: "SBOM VEX \(Vulnerability Exploitability eXchange\) サポート" feature bullet and CISA 2025 SBOM minimum elements, link `https://www.cisa.gov/sbom`), angr VEX IR (`253c78e7dffc2a0727269b4c`, `lanes/kaidoku/round7/work/arxiv-survey-text.txt:3630`), a browser-extension paper (`ae124ff9730256e9df45ef14.txt:956`; also `lanes/tabi/.deepresearch/.../arxiv-2305.11506.txt:956`), CISA SSVC guide citation (`aaf68de16bb49c29a5df8a80.txt:2733`; `lanes/kasegi/round7/evidence/zxd_wd.txt:2733`), a CISA GitHub-token news item (`da731f41700560d8aed7e3fe.txt:190,223`), and a Gutenberg-style "vex" novel line (`ce807041be18a27b20160f42.txt:564`). The "SBOM VEX" bullet names VEX support as a product feature; it states no issuance timing, update, reaffirmation or inheritance rule.

## Kasegi self-check (read-only)

`rg -i 'when-issue-vex|when to issue'` over the lane working tree (excluding `.git`, `.jj`) at the time of the run: 0 hits, so S057 is not yet present, consistent with a first write. `corpus/knowledge/csaf-vex-product-status-and-justifications.md` has no issuance/lifecycle/reaffirmation/inheritance text (only a "supersedes" line at 18 about CVRF), so F22 is beyond the held CSAF profile.

## Unresolved

None for the assigned question. Limit: sweep is lexical; a sibling describing issuance without any of the tokens above would be missed, but no token variant (vulnerability exploitability exchange, CSAF, OpenVEX, CycloneDX, not_affected) hit anywhere outside kake's security.txt line.
