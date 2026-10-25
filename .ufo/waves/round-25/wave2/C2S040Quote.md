# C2S040Quote — round 25 wave 2 falsification report

Seat: `L1Kasegi25.C2S040Quote`. Lane: kasegi-shokunin.
Target: re-open `corpus/source-snapshots/round-25/S040.txt`; verify the four expedite bullets,
absence of `30111`, absence of any "no-bounty" claim, and byte-exactness of the nine S040 quotes
asserted by `.ufo/waves/round-25/wave1/EntryCiscoCrosswalk.md` and bound in
`corpus/source-snapshots/round-25/manifest.json`.

Capture of record verified first: `sha256sum corpus/source-snapshots/round-25/S040.txt` =
`b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c`, 503 lines — identical to the
manifest and the wave-1 receipt.

## Verdict

**HOLDS with one off-by-one correction.** The wave-1 claims are right on every load-bearing axis:
four bullets, zero `30111`, no bounty denial, 9/9 quotes verified. But the entry's own falsifiable
rule 4 partitions the bullets on the **wrong line boundary**: it prints `L302-L305` and `L306-L308`;
the capture actually splits `L302-L304` and `L305-L308`. Every other line reference in the entry,
the receipt, and the manifest is correct — the defect is local to
`corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:92-93`.

## Findings by severity

### 1. Minor defect — rule 4 bullet ranges off by one (entry L92-L93)

The capture (`S040.txt`, `awk 'NR>=295 && NR<=322'`):

- **L301**: bullet 1 — "The Cisco PSIRT has completed the incident response process for a
  high-severity vulnerability and public disclosure of code fixes is planned to address it."
- **L302-L304**: bullet 2 — "The Cisco PSIRT has observed active exploitation of a vulnerability
  that could lead to increased risk for Cisco customers. Cisco will accelerate the publication of a
  security announcement describing the vulnerability that may or may not include a complete set of
  patches or workarounds."
- **L305-L308**: bullet 3 — "There is the potential for increased public awareness of a
  vulnerability affecting Cisco products and/or cloud-hosted services that could lead to increased
  risk for Cisco customers. Cisco will accelerate the publication of a security announcement
  describing the vulnerability that may or may not include a complete set of patches or workarounds."
- **L309**: bullet 4 — "The Cisco PSIRT has declared a third-party software vulnerability to be
  high profile."

The entry's rule 4 (`vendor-disclosure-policy-commitments-crosswalk.md:90-94`) says
"observed active exploitation (L302-L305), potential for increased public awareness (L306-L308)".
L305 is the *first* line of bullet 3 ("There is the potential for increased public awareness…"),
not the last line of bullet 2. The entry contradicts its own crosswalk row at line 28, which
correctly prints `L302-L304, L305-L308`, and its own receipt finding 1, which also prints
`L302-L304 / L305-L308` (`EntryCiscoCrosswalk.md:178-179`).

Smallest correction: in `vendor-disclosure-policy-commitments-crosswalk.md:92-93`, change
`L302-L305` → `L302-L304` and `L306-L308` → `L305-L308`. One line, two tokens, no other file
touches the wrong ranges. The four-bullet count itself, the L301-L309 span, and the falsifiability
of the rule are unaffected.

Not a defect: `cisco-weekly-slot` is attributed "L319-L320" but the quoted substring
("Cisco generally discloses Cisco Security Advisories at 1600 Greenwich Mean Time (GMT)") ends at
"GMT)" on L319; L320 only carries the continuation "Wednesday." Over-inclusive range, quote still
byte-exact — noted, no correction needed.

### 2. Verified — four expedite bullets, "two conditions" staged text falsified

`grep -c expedite corpus/source-snapshots/round-25/S040.txt` → `1` (L300, the "may, however,
expedite disclosure … in the following situations:" lead-in). Exactly four bullet sentences follow
at L301 / L302-L304 / L305-L308 / L309; L310 ("All Cisco security publications are disclosed…")
is a post-bullet statement, not a fifth condition. `claims.json:45` and the wave-1 rejection of
the staged package are correct: the staged
`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/vendor-cvd-policy-crosswalk-2026-10-23.md:31-34`
says "**It states the two conditions under which it will go faster.**" and names only the
high-severity-fixes-planned and active-exploitation conditions, omitting public-awareness and
high-profile-third-party. The capture proves four.

### 3. Verified — `30111` absent from S040

`grep -c 30111 corpus/source-snapshots/round-25/S040.txt` → `0` (grep exit 1). `30111` occurs only
in `S039.txt` (L498, L618, L619, L620, L621, L624) where the entry correctly attributes it
("ISO/IEC 30111:**2013** … S039", entry L25). The staged package's Cisco section names no standard
other than 29147:2018 (staged L20-21), consistent with S040 having exactly one `29147` occurrence
(L58, "ISO/IEC 29147:2018,"). Rule-1 check string reproduces: `S036 0 / S038 0 / S039 8 / S040 1`.

### 4. Verified — no-bounty claim absent from S040

`grep -in bounty corpus/source-snapshots/round-25/S040.txt` → hits at L32 (TOC), L487 (section
head "Cisco Bug Bounty Programs"), L488-L489 ("For information on Cisco Bug Bounty programs, see
Bug / Bounty Programs at Cisco."). Broader denial scan
(`grep -in "bounty\|reward\|compensat\|remunerat"`) returns no other money lines. The "no bounty"
string `現在、報奨金制度は設けておりません。` lives in `S038.txt:20` (GMO Pepabo), correctly
attributed there by the entry (`pepabo-no-bounty`, entry L59) — not in S040. The staged package's
"no bounty" characterization of Cisco (staged L45) is falsified by S040 L487-L489, and the wave-1
entry does not repeat it: it says only that Cisco *names* its programmes with terms on a separate
page (entry L31, L88, L98-100, L126-127). Accurate.

### 5. Verified — 9/9 S040 quotes exact, once each

Reproduction of the receipt's per-quote count (script from `EntryCiscoCrosswalk.md:226-240`):

```
cisco-iso-29147-2018      raw_grep_c=1  bytes.count=1  normalized.count=1   (L58)
cisco-investigates-all    raw_grep_c=1  bytes.count=1  normalized.count=1   (L162)
cisco-post-ldos           raw_grep_c=1  bytes.count=1  normalized.count=1   (L482)
cisco-jpcert-partner      raw_grep_c=0  bytes.count=0  normalized.count=1   (L189, wrapped L188-L189)
cisco-default-hold        raw_grep_c=1  bytes.count=1  normalized.count=1   (L300)
cisco-active-exploitation raw_grep_c=1  bytes.count=1  normalized.count=1   (L302)
cisco-high-profile-bullet raw_grep_c=1  bytes.count=1  normalized.count=1   (L309)
cisco-weekly-slot         raw_grep_c=1  bytes.count=1  normalized.count=1   (L319)
cisco-bounty-pointer      raw_grep_c=1  bytes.count=1  normalized.count=1   (L488)
```

8/9 byte-exact; `cisco-jpcert-partner` is split across L188-L189
("Japan Computer\nEmergency Response Team (JP-CERT)") and matches once under the declared
whitespace normalization — exactly as the receipt disclosed
(`entry-cisco-quote-counts.txt:4`, `EntryCiscoCrosswalk.md:60-62,71`). No quote crosses a U+FFFD
line (hazard lines confirmed at L108, L193, L203, L222, L479 via `grep -n $'\uFFFD'`).

Instrument replay — `python3 corpus/instruments/source-recheck.py --manifest
corpus/source-snapshots/round-25/manifest.json --source S040` → `S040:sha256 OK` plus 9 quote
assertions `OK occurrences=1` (`cisco-jpcert-partner OK normalized=markup-whitespace`), exit 0.

### 6. Verified — full recheck line, both cwds, byte-identical

Extracted the entry's `recheck:` line (entry L7) to a scratch file:

```
$ bash -n /tmp/s040_recheck.sh            → exit 0
$ bash /tmp/s040_recheck.sh               → exit 0, 37 "OK" lines (4 sha256 + 33 quotes)
$ ( cd / && bash /tmp/s040_recheck.sh )   → exit 0
lane-root stdout sha256  = 64df1c6611f62e561b68627e87b74b172a466ab878066691b680a3f0ce91e753
foreign-cwd stdout sha256 = 64df1c6611f62e561b68627e87b74b172a466ab878066691b680a3f0ce91e753
```

Matches the digest the receipt printed (`EntryCiscoCrosswalk.md:122-124`) exactly: same bytes,
same count, same exit.

## Residual risk / gaps

- The four bullets are prose sentences without list markup; the count of four is a structural
  reading (four "The Cisco PSIRT has… / There is…" sentences between the lead-in at L300 and the
  closing statement at L310). The count is falsifiable but a reformat of the live page could
  change line numbers without changing meaning — the manifest's sha256+quote binding pins the
  bytes, so this is covered.
- `cisco-jpcert-partner` is the only quote not byte-exact; it is declared as normalized in the
  entry (L48, L123-125), the receipt, and the manifest output. If the bar is "all quotes raw
  byte substrings", this quote fails it — but that bar was never claimed.

## Tooling record

Nothing installed or updated. No pacman, uv, npx, cargo, or npm channel used; pacman transactions
are paused per wave-2 context. `RULES.md` not needed — no install attempted.
