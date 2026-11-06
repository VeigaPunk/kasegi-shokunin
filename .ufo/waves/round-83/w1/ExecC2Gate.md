# ExecC2Gate — C2 score: F59 OSV.dev FAQ post-import lifecycle (S117)

Seat `ExecC2Gate`, round 83 attempt 1, wave 1. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; scratch `/fast/scratch/hyaku/kasegi-r83/ExecC2Gate` (deleted before yield). No lane file, corpus file, registry, skill or instrument was edited; no git/jj write; no tool installed.

## Frozen inputs (measured)

- Snapshot `corpus/source-snapshots/round-83/S117.txt`: sha256 `0a5fa51c987544789d3c84fee6be2b1246a7a6a865457668f9e94a37e60bd53e`, 137 lines, 10229 bytes (`wc -l -c`). Manifest: `http.status 200`, `final_url == url`, `fetched_utc 2026-11-06T21:55:29Z`, six quotes at anchors 112/116/121/122/94/108.
- Draft under test: `corpus/knowledge/osv-faq-post-import-record-lifecycle.md`, uncommitted (`??`), sha256 `a91963a84e72bb38a78668a6a1c44b2f2ab90ceef0e898b92c135bcd62af00b0`.
- Gate `.ufo/waves/round-83/c2/entry-gate.py`; controls `.ufo/waves/round-83/controls/c2-controls-r83.py`; frozen control receipt `.ufo/waves/round-83/controls/c2-prefreeze-r83.txt` and `.ufo/waves/round-83/controls/c2-g6-controls-r83.txt`.

## (1) B0 — source recheck

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-83/manifest.json --source S117
S117:sha256 OK
S117:Q01-withdrawn-excluded OK occurrences=1 anchor=112-ok
S117:Q02-withdrawn-get OK occurrences=1 anchor=116-ok
S117:Q03-gcs-ten-percent OK occurrences=1 anchor=121-ok
S117:Q04-rest-git-orphaned OK occurrences=1 anchor=122-ok
S117:Q05-modified-id-csv OK occurrences=1 anchor=94-ok
S117:Q06-aliases-bump-modified OK occurrences=1 anchor=108-ok
rc=0
```

Receipt `ExecC2Gate-receipts/b0-source-recheck.txt`. **B0 pass.**

## (2) B5 — the entry's own recheck line, foreign cwd

Entry line value (text after `recheck: `):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-83/manifest.json --source S117
```

Run with `bash -c` from fresh dir `/fast/scratch/hyaku/kasegi-r83/ExecC2Gate/b5` (no lane cwd): the same seven lines as B0, **rc=0**. The command is byte-identical to B0 behind the required `cd ... && ` prefix. Receipt `ExecC2Gate-receipts/b5-entry-recheck-freshcwd.txt`. **B5 pass.**

## (3) B8 — entry gate and G6 forgery controls

Draft gate:

```
ENTRY-GATE sid=S117 claims=6 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 untied=0 header=ok
ENTRY-GATE-RESULT pass
rc=0
```

Controls (`c2-controls-r83.py --lane <lane> --work <scratch>`), every line:

```
CONTROL forgery=copyrule gate=r82 rc=0 ENTRY-GATE sid=S116 claims=6 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 header=ok
CONTROL forgery=copyrule gate=r83 rc=1 ENTRY-GATE sid=S116 claims=6 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 untied=1 header=ok
CONTROL forgery=crosscite gate=r82 rc=0 ENTRY-GATE sid=S116 claims=6 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 header=ok
CONTROL forgery=crosscite gate=r83 rc=1 ENTRY-GATE sid=S116 claims=6 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 untied=1 header=ok
CONTROL forgery=filler gate=r82 rc=0 ENTRY-GATE sid=S116 claims=6 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 header=ok
CONTROL forgery=filler gate=r83 rc=1 ENTRY-GATE sid=S116 claims=6 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 untied=1 header=ok
CONTROL admitted=osv-determineversion-cc-library-versioning.md gate=r82 rc=0 ENTRY-GATE sid=S113 claims=8 want=8 spans=10 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 header=ok
CONTROL admitted=osv-determineversion-cc-library-versioning.md gate=r83 rc=0 ENTRY-GATE sid=S113 claims=8 want=8 spans=10 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 untied=0 header=ok
CONTROL admitted=osv-ubuntu-binary-to-source-mapping.md gate=r82 rc=0 ENTRY-GATE sid=S114 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 header=ok
CONTROL admitted=osv-ubuntu-binary-to-source-mapping.md gate=r83 rc=0 ENTRY-GATE sid=S114 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 untied=0 header=ok
CONTROL admitted=osv-importfindings-record-quality-feedback.md gate=r82 rc=0 ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 header=ok
CONTROL admitted=osv-importfindings-record-quality-feedback.md gate=r83 rc=1 ENTRY-GATE sid=S115 claims=6 want=6 spans=6 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 untied=1 header=ok
CONTROL admitted=osv-high-quality-record-import-bar.md gate=r82 rc=0 ENTRY-GATE sid=S116 claims=6 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 header=ok
CONTROL admitted=osv-high-quality-record-import-bar.md gate=r83 rc=0 ENTRY-GATE sid=S116 claims=6 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 untied=0 header=ok
```

Script exit 0. **The three forgeries meet B8 exactly:** each of `filler`, `crosscite`, `copyrule` is `rc=0` under `gate=r82` and `rc=1` with `untied=1` under `gate=r83`. The four admitted controls are not uniform: S113, S114 and S116 pass both gates; **S115 (F57) passes r82 but fails r83 with `untied=1`** — the frozen G6 limb rejects one previously admitted entry. That outcome is already recorded in the frozen receipt `.ufo/waves/round-83/controls/c2-g6-controls-r83.txt`, so it is a known cost of G6, not a new measurement; it is a risk against the claim that the limb "admits admitted entries", not against B8's forgery limb. Receipts `b8-entry-gate-draft.txt`, `b8-controls.txt`.

## (4) B6 — literal sweep of the six manifest quotes

Six quotes over the other 96 `corpus/knowledge/*.md` (draft excluded; 97 files on disk):

```
swept_files=96 excluded=osv-faq-post-import-record-lifecycle.md
Q01-withdrawn-excluded files=0 -
Q02-withdrawn-get files=0 -
Q03-gcs-ten-percent files=0 -
Q04-rest-git-orphaned files=0 -
Q05-modified-id-csv files=0 -
Q06-aliases-bump-modified files=0 -
literal_sweep_total=0
rc=0
```

**B6 pass** (one file count per quote, total 0). Receipt `b6-literal-sweep.txt`. The draft's own claim "0 files each over the other 96" is true; the prefreeze receipt's `ls ... | wc -l` = 96 counts the tree before the draft was on disk, while the draft is now the 97th file, so "the other 96" is the correct denominator.

## (5) Cite audit — every `(S117.txt:N)` and `(S117.txt:A-B)` in the draft

Method: Python over the draft and `S117.txt`; every cite printed with the full sentence and each cited line (`ExecC2Gate-receipts/cite-audit.txt`, 235 lines). **45 cites**, all line numbers within 1..137; every free anchor was compared literally.

Flagged cites (the only rows where the cited line does not carry the sentence's content):

| draft line | claim / sentence | cite | what the cited line carries | verdict |
|---|---|---|---|---|
| 17 | C1 rule: "empty POST /v1/query answer ... excluded because its withdrawn field is set" | `S117.txt:112` | `:112` carries "excluded from:"; the POST-query item is `:113` ("the responses to POST API queries") | **OVERREACH by cite range**; candidate cites `112-113` and says "first sentence and its first list item" |
| 33 | C3 rule: "a mass upstream deletion ... is aborted, so those records stay unmarked until the next import" | `S117.txt:121` | `:121` says "if more than 10% of records are about to be marked as withdrawn, OSV.dev aborts and does not proceed"; no denominator ("its records"), no "until the next import", and the actor that aborts is OSV.dev/the marking, not "a mass upstream deletion" | **OVERREACH** (three additions); candidate keeps the page's words and names the unstated denominator |
| 47 | C5 body: "one line per record as `<iso modified date>,<ecosystem_dir>/<id>`" | `S117.txt:94-100` | `:96` gives the row format and `:98` one example; no statement that each record is exactly one line | **OVERREACH** (minor inference); candidate says "rows formatted" |
| 49 | C5 rule: "can find ... without a full download, since the page names it ..." | `S117.txt:94` | `:94` carries the naming; "without a full download" is `:100` ("stream the file and stop ... since your last download") | **cite too narrow**; candidate cites `94, 100` |
| 51 | C5 rejected over-generalization: "modified_id.csv also lists records deleted upstream" | `S117.txt:94`, `:119-122` | `:94` is a capability ("can be used to identify recently added or changed"), not an exclusivity; `:119-122` describe deletion handling, not the CSV's contents; no line refutes the stated over-generalization | **UNGROUNDED rejection**; candidate replaces it with a page-refuted over-generalization ("must download the full database") citing `:94, 100` |

Non-blocking observations (no correction):

- draft L25's "200 from the vulns GET by ID" and L41's "still served" are technical paraphrases of `S117.txt:116` "returned by the /vulns/<ID> GET API" and `S117.txt:122` "leaves the existing records valid but orphaned"; the page implies a successful retrieval and validity, and no line contradicts them.
- The "Not claimed" line's `S117.txt:86-88` is accurate for the route, but the data-correction answer spans `:83-88` and the "Why isn't a record available?" answer (`:79-82`) is unlisted. This is a completeness gap in the non-claim list, not a false statement; the candidate leaves it (the entry's scope is the six post-import statements).

Claim table (R76 categories) over the draft's load-bearing sentences:

| claim | rows | verdict |
|---|---|---|
| C1 withdrawn excluded | quote `:112`; paraphrase `:113-114`; rejection `:115` | GROUNDED; rule row OVERREACH by cite range (above) |
| C2 withdrawn by ID | quote `:116`; paraphrase `:115-118`; rule; rejection `:112-114`/`:116-118` | GROUNDED |
| C3 GCS 10% abort | quote `:121`; paraphrase `:121`; rejection `:121` | GROUNDED; rule row OVERREACH (above) |
| C4 REST/Git orphaned | quote `:122`; paraphrase `:122`; rule; rejection `:121`/`:122` | GROUNDED |
| C5 modified_id.csv | quote `:94`; paraphrase `:94-100`; rule; rejection `:94`/`:119-122` | paraphrase row OVERREACH (one line per record); rule cite too narrow; rejection UNGROUNDED (above) |
| C6 aliases bump modified | quote `:108`; paraphrase `:104-108`; rule; rejection `:108` | GROUNDED |
| Gate block | URL/200, sha, 137 lines, 10229 bytes, fetched_utc, six word counts 11/6/19/12/17/12 | GROUNDED; all match the manifest and `wc`, and each quote is verbatim at its anchor (`occurrences=1`) |
| Distinctness | F58 `S116.txt:27`; F57 `S115`; F51 `S108` Limits `:75`; F47 `S103.txt:306-307` | GROUNDED (F58's companion out-of-scope sentence is at S116:27; F51 "listed, not described" at its Limits; S103:306-307 is `is_withdrawn boolean` / "Whether to only return advisories that have been withdrawn.") |

## Corrected draft (written because four rows failed the literal check)

- Candidate: `.ufo/waves/round-83/w1/ExecC2Gate-candidate-osv-faq-post-import-record-lifecycle.md`, sha256 `67e96446eb10ec20bbea1325068476e65b76f8bbffc0554c9cbbddd1e16985c2`.
- Diff: `.ufo/waves/round-83/w1/ExecC2Gate-candidate.diff`, sha256 `c8b61e621c2b2fdb5b322387410747cd8daffe653730b92db34df52624117c21`; five changed lines and no other bytes.
- Changes: (a) C1 rule cite `112` -> `112-113` and reader check "first sentence and its first list item"; (b) C3 rule rewritten to "a GCS import that is about to mark more than 10% of records as withdrawn aborts and does not proceed, so a mass upstream deletion can leave those records unmarked after that import", plus the unstated-denominator note; (c) C5 body "one line per record" -> "rows formatted" with `94-98` and `99-100`; (d) C5 rule cites `94, 100` for "without a full download"; (e) C5 rejection replaced by the full-database over-generalization refuted by `94, 100`.
- Corrected draft gate:

```
ENTRY-GATE sid=S117 claims=6 want=6 spans=7 mislocated=0 overlong=0 claimless=0 unpinned=0 ruleless=0 untied=0 header=ok
ENTRY-GATE-RESULT pass
rc=0
```

Receipt `b8-entry-gate-candidate.txt`. The candidate keeps the header, `recheck:` line, six quotes, Gate block and all other bytes identical; B0/B5/B6 are therefore unchanged, and B8 passes on the corrected body.

## (6) B4 — capture binding check

```
$ python3 corpus/instruments/capture-binding-check.py | tail -2
AUDIT records=97 with_url=97 with_fetched_utc=59 with_archival=38 snapshot_dirs=56 manifest_dirs=56 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=97 bound=97 unbound=0
```

Full run **rc=0**; the B4 predicate `unbound=0` holds. The `orphans=1 orphan=S040-live.txt` row is pre-existing audit output (an orphaned snapshot, not an unbound record) and is not part of B4. Receipts `b4-capture-binding-tail.txt`, `b4-capture-binding-full.txt`.

## Verdict

- **B0 pass, B5 pass, B6 pass, B8 pass (draft; the three forgeries meet the control exactly), B4 pass (`unbound=0`).** The five frozen predicates this seat owns are true on the draft; B1/B2/B3/B7 are outside this seat's item.
- The draft nevertheless fails the **R71/R76 literal standard** in four rows: C1 rule's POST limb (`:113` not cited), C3 rule's denominator/"until the next import"/abort subject, C5 body's "one line per record", and C5's unrefuted rejection; a fifth, narrower cite (`C5` rule's "without a full download") rests on `:100`. The corrected candidate fixes all five and passes B8. **Recommendation: land the candidate rather than the draft** if the L1 wants the entry to satisfy the anchor-referent/claim-table checks; landing the draft unchanged still satisfies the frozen C2 predicates but carries these defects.
- **Risk:** G6's `untied` limb rejects the previously admitted S115 (`osv-importfindings-record-quality-feedback.md`) under r83 (`rc=1 untied=1`) while r82 admits it. That is a known G6 false-positive cost recorded in the frozen controls; it should be stated in the C2 closure rather than hidden.
- No host tooling installed or upgraded; no pacman transaction; no git/jj write; no lane file edited. Scratch deleted.

## Files written

- `.ufo/waves/round-83/w1/ExecC2Gate.md` (this report)
- `.ufo/waves/round-83/w1/ExecC2Gate-candidate-osv-faq-post-import-record-lifecycle.md`
- `.ufo/waves/round-83/w1/ExecC2Gate-candidate.diff`
- `.ufo/waves/round-83/w1/ExecC2Gate-receipts/b0-source-recheck.txt`
- `.ufo/waves/round-83/w1/ExecC2Gate-receipts/b5-entry-recheck-freshcwd.txt`
- `.ufo/waves/round-83/w1/ExecC2Gate-receipts/b8-entry-gate-draft.txt`
- `.ufo/waves/round-83/w1/ExecC2Gate-receipts/b8-controls.txt`
- `.ufo/waves/round-83/w1/ExecC2Gate-receipts/b8-entry-gate-candidate.txt`
- `.ufo/waves/round-83/w1/ExecC2Gate-receipts/b6-literal-sweep.txt`
- `.ufo/waves/round-83/w1/ExecC2Gate-receipts/b4-capture-binding-tail.txt`
- `.ufo/waves/round-83/w1/ExecC2Gate-receipts/b4-capture-binding-full.txt`
- `.ufo/waves/round-83/w1/ExecC2Gate-receipts/cite-audit.txt`
- `.ufo/waves/round-83/w1/ExecC2Gate-receipts/quote-wc.txt`
