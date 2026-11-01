# Round-51 erratum 1 — the round-50 C1 do-nothing control was not produced on this host (D1 of the round-50 closure)

Routed first-priority by the round-50 non-author closure (verifier spot-check D1). Append-only per R9:
nothing below rewrites a filed byte; the wrong assertions stay in place and this file is the correction
of record.

## The relabel

`.ufo/waves/round-50/controls/do-nothing-c1.txt` is an **imported old-host (Linux) receipt, not a run
produced on the Windows workspace host that committed round 50.** The round-50 report, `claims.v2.json`
(`do_nothing_control`: "committed receipt controls/do-nothing-c1.txt, produced on this host"),
`claims-erratum-1.md` §"What survives unchanged" ("The C1 do-nothing control (`controls/do-nothing-c1.txt`)
is genuine (instrument absent at base export → exit 2) and stays"), and `corpus/lessons/round-50.md` M3
all assert or imply host production. The label is wrong in every one of those places.

What the bytes actually are: `+ python3 corpus/instruments/census-freshness-check.py --root
/fast/scratch/hyaku/kasegi-r50/base-export` followed by a Unix CPython error line naming the `/fast/...`
path and `C1_EXIT=2` — a functioning `python3` resolving a `/fast` scratch path, the old Linux host's
shape. The file's *substance* is genuine (the instrument is genuinely absent at the base export, and the
round-50 verifier independently re-derived that substance from the base trees), which is why C1 itself was
not defeated; only the provenance attribution is wrong. The file is retained **byte-identical** as the
evidence of the mistake (deleting it would destroy the evidence; the round-50 M3 rule "a control imported
from another host is labelled as imported, never pasted in place" is now applied to this file itself).

## The wrong host-distinguishing claim, corrected

`claims-erratum-1.md` said the file "carries a Windows CPython error string for a `/fast/...` path". That
distinguishing claim is **factually wrong**, probed on this host (receipt
`.ufo/waves/round-51/controls/probe-host-r51.txt`):

- `python3 --version` on this host prints the Microsoft Store stub message ("Python was not found; …")
  and exits 49 — there is no functioning `python3` here to print `python3: can't open file …`.
- `/fast` does not exist on this host (`ls /fast` → "No such file or directory", exit 2).
- Windows CPython's own error format differs: `python /fast/...` prints the interpreter's exe path and a
  backslash-quoted target inside single quotes —
  `C:\Users\jpvei\AppData\Local\Programs\Python\Python313\python.exe: can't open file 'C:\\Program Files\\Git\\fast\\…'`
  (Git Bash translates the leading `/fast` against its install mount) — not the imported receipt's
  `python3: can't open file '/fast/…'` Unix form. The verifier's D1 probe reached the same conclusion.

So the round-50 erratum's host-distinguishing evidence actually distinguished the files in the opposite
direction: `do-nothing-c1.txt` and `do-nothing-c2.txt` are BOTH old-host imports (C1 from a `/fast`
scratch run with working `python3`; C2 from the same `/fast/.../base-export` with 30 FRONTIER-PASS rows),
and neither of the round-50 "controls" directory's two original receipts was produced on the host that
committed them. The genuinely host-produced C2 control was `do-nothing-c2-winhost.txt`, as the round-50
erratum already recorded; this erratum extends that finding to C1.

## What replaces it

`.ufo/waves/round-51/controls/do-nothing-c1-winhost.txt` is the C1 do-nothing control **produced on this
host** (round-51 claim C1): the C1' counter command run against a base export of `c5e3636` built here by
per-file `git show` (git archive aborts on this host's NTFS-uncheckoutable paths — the same build method
the round-50 `do-nothing-c2-winhost.txt` receipt records), printing this host's interpreter path, the
backslash-quoted missing-instrument path, and `C1_EXIT=2`. Its reproduce commands are embedded in the
receipt header; a same-host re-run reproduces the error form and exit. The control's semantics are
unchanged from the round-50 freeze: the counter cannot print `CENSUS-FRESH=ok` at a base export where the
instrument does not exist.

## Scope of this correction

- Round-50 frozen predicate C1 (claims.v2.json): unaffected — its expected bytes (`CENSUS-FRESH=ok`
  exit 0 at the tip) and its do-nothing semantics are unchanged; only the control receipt's provenance
  label was wrong, which is why the verifier routed D1 as status-neutral.
- The round-50 report lives in the fleet repo (orchestrator-committed); this erratum cannot append there.
  The round-51 report records the correction against it.
- Freeze pin: `.ufo/waves/round-50/freeze-v2.txt` pins `do-nothing-c1.txt` at sha256
  `6c4bc08bdf415c866fe757e004b4523e92b4eee28189047824f8f2ee900016cf`; that pin stays true of the
  byte-identical retained file. The provenance label is the thing corrected, not the bytes.
