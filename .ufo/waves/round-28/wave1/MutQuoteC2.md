# MutQuoteC2 — manifest quote-binding mutation test (round 28 wave 1)

Seat: MutQuoteC2 | Role: UFO-FSD mutation tester | Detector: `corpus/instruments/source-recheck.py`
(digest 9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96)
Scratch: `.ufo/waves/round-28/wave1/MutQuoteC2/work/` (manifest + S041.txt + S042.txt copied byte-for-byte from
`corpus/source-snapshots/round-28/`; live hashes: manifest e62ddad133ffc19ebc66822c0fcb3b48ed4993c101f05262302acc58714f291d,
S041 e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47, S042 b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966).
Baseline pristine check: exit 0, all 12 assertions `OK occurrences=1` (no `anchor` fields declared).

## Mutants (all in `work/`, captures untouched; assert = assertion id named by the detector)

| mutant | mutation | expected | observed output tail | exit | verdict |
|---|---|---|---|---|---|
| M1 | S041:Q1 final char `。` → `！` | exit 1 naming failing assertion | `S041:Q1 MISMATCH reason=quote-not-found` | 1 | killed |
| M2 | swap quote strings S041:Q2 ↔ S042:Q2 (cross-occurrence 0 pre-swap) | exit 1 naming failing assertions | `S041:Q2 MISMATCH reason=quote-not-found` + `S042:Q2 MISMATCH reason=quote-not-found` | 1 | killed |
| M3 | S042:Q3 quote → `JPCERT/CCは、製品開発者に対して脆弱性関連情報に係る以下の対応を依頼します。` (occurs 2× in S042 normalized; `anchor` absent) | exit 1 | `S042:Q3 OK occurrences=2 anchor=MISSING`; all other lines OK; **exit 0** | 0 | **LIVE** |

Mutant manifest digests: m1 b8063cf6440351dd019f0f9faae3f2b865ea7896ff5c61a028efdb41e31b38dd,
m2 c5883a46b8d485fd6cdd32ddc2ca3745cb1134499378f38c3432b1ffe64bf352,
m3 aaedb76930e82085e56723cffaf8e2de4f5cb4b4e3e1c2b8a7dcdf1f80108009.

Live mutant: **M3** — the detector prints the violation (`occurrences=2 anchor=MISSING` on receipt line
`S042:Q3`) but keeps status `OK` and exit 0. The assertion it fooled is **S042:Q3**; the unenforced rule is
QUALITY **Q9** (quote not exactly-once → must carry a verified `anchor`; Q9 says "a quote that occurs twice must
carry the anchor" and is currently an unlanded conjunct). `frontier-recheck-count.py` checks only the entry's
recheck exit code, so its harness also records the entry as passing. Nothing in the automated chain fails on a
non-unique unanchored quote; only human receipt review sees `anchor=MISSING`. This is a coverage finding, not a
contract change: the fix belongs in the instrument (exit non-zero / fail on `anchor=MISSING` when `occurrences>1`),
per C2 kill rule "any manifest quote assertion not exactly-once (or anchor-broken)".

## Restoration evidence

- The pristine `work/manifest.json` was never mutated in place; each mutant is a separate manifest file.
- Post-attack `sha256sum` of `work/manifest.json`, `work/S041.txt`, `work/S042.txt` equals the live committed
  hashes above (byte-identical, `diff -q` pristine-vs-live manifest: IDENTICAL).
- Scratch trimmed to 236K (R14 economy): capture fixtures + the manifest variants; duplicate `pristine/` copy
  removed after hash verification. No writes outside `.ufo/waves/round-28/wave1/MutQuoteC2/`.

Re-run command (post-landing, from lane root):
`python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/source-recheck.py --manifest /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-28/wave1/MutQuoteC2/work/manifest-m3.json`
