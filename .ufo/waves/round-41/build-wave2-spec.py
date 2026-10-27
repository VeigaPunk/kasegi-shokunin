#!/usr/bin/env python3
"""kasegi round-41 wave-2 (falsify) spec generator. Item list is spliced from
ConnWave2Seed's distilled attack list + the L1's fixed falsification floor after
wave 1 settles. This file is finalized by the L1 (KasegiR41) post-WAVE-DONE."""
import json, sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
# Filled by the L1 after wave-1 integration:
BASE = "5b29ea1439450b712581edf5f0f0bf98dfb262ab"
FREEZE = "fbba3d96cdf8d37c1ea41304a1ba35691329684b"
R40J = "c7aea5ef97902f38289cbdc1cf267068876a62dd"
J = "<J>"
Y = "<Y>"

CONTEXT = f"""# Round
kasegi-shokunin round 41 FALSIFY wave, dispatched by the L1 (agent KasegiR41) via the inline spawn handoff (hyaku run 10). Lane repo {LANE} is the ONLY lane repo. The fleet root /home/vgpnk/Projects/shokunin is read-only to you — never write there. /home/vgpnk/Projects/shokuknow is read-only. Base commit {BASE}; claims-freeze {FREEZE}; frozen claims at {LANE}/.ufo/waves/round-41/claims.json (read first; do not edit). Wave 1 (build) has landed; the integrated tree state is described in your item. Judged head J / verification ref Y are named in your item (Y = J + receipt only).

Frozen claims (summary; claims.json is authoritative):
- C1 depth:verifiability (4 held): suite corpus/instruments/r41-closure.sh export-mode only; at Y prints closed=12/12 exit=0 with I1-I12 payload lines; --selftest --export-ref Y prints twelve graded selftest case lines + selftest cases=12 failures=0; base {BASE} and r40 judged head {R40J} exports red; plain run exit 2. Kill rule incl.: any committed fixture shows a check passing while its defect is present (round-40 T2/T4/T7/T13/T14, the seven CritKillRule escapes, MutH6H10 leaf-capped green base, MutH1H5 count-relative forgery); receipt at Y byte-identical to the teed run+selftest transcript; census exit 0; clean tree at filing; no kasegi-r41* scratch siblings except the passed --work dir.
- C2 coverage (8 held): F24 (RFC 9116) admitted 23->24; S063 mined with capture+manifest passing source-recheck and binding; entry corpus/knowledge/rfc-9116-security-txt.md with provenance trio citing S063; harness entries=27 pass=27 incl PASS F24 ids=S063; binding records=55 bound=55; recheck-audit lines=60 expected=60; registry 63 rows; census exit 0 (W04 S028/S029 only); measure 44/44=1.000, queued 0.

Write scope. Your ONLY allowed writes are (1) your receipt at {LANE}/.ufo/waves/round-41/wave2/<SEATNAME>.md (write it last) and (2) deliverable files your item names beside it as {LANE}/.ufo/waves/round-41/wave2/<SEATNAME>.<suffix>, and (3) scratch under your scratch dir. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Never edit any other file anywhere (no lane/fleet/sibling/shokuknow writes); never run a mutating git/jj command anywhere; read-only git is fine.

Scratch. S=/fast/scratch/hyaku/kasegi-r41/<SEATNAME>/ — create with mkdir -p, bind all work there (TMPDIR=$S), /tmp only for files under 50 MB; remove it before you yield (`trap 'rm -rf -- "$S"' EXIT` / finally rmtree) after copying receipts out. A surviving scratch dir is an I6-class defect. Check `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` before heavy passes.

Tooling. You may install tools per /home/vgpnk/.omp/agent/RULES.md (official channels; record in receipt). pacman is PAUSED host-wide — never run pacman. Never edit ~/.omp/agent/config.yml or mcp.json. Never restart a host service.

Host guard. Your tools start at the fleet root: cd to your scratch first; absolute paths everywhere. Git fixtures: D=$(mktemp -d) && git -C "$D" init -q, verify rev-parse --show-toplevel equals $D before committing; never a throwaway identity elsewhere. Never write PATH directories.

Network fetches: `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`; record HTTP status, bytes, UTC time.

Rules. Leaf seat — no subagent spawning. Do not message agent://all. Godspeed posture governs your work. Your item names what you attack — attack it for real: run the counters, mutate the bytes, re-open the sources. A finding without a reproduced transcript is not a finding.
"""

def item(name, role, task):
    return {"name": name, "role": role, "prompt": "/skill:godspeed\n\n" + task}

# FIXED FALSIFICATION FLOOR (the L1's own list — every round-41 falsify wave carries these)
FIXED = [
 item("RevC1Counters", "reviewer", f"""Re-run every frozen C1 counting command at Y (the L1 names Y in the wave handoff; if your item text lacks it, read .ufo/waves/round-41/final-gates/all-gates.txt header for export-ref): the suite run (closed=12/12 exit=0), the graded selftest (cases=12 failures=0), the base and r40-judged-head negatives (each closed<12/12 exit=1), and the plain-run refusal (exit 2). Record verbatim transcripts. Then re-derive each of the 12 I-check payload values from the export bytes by PLAIN READS (no lane gate): verify every payload value names real tree facts (correction lines exist and carry the evidence tokens; the SKILL registry row is well-formed; density.py byte-identical; declared-blocks exact; census exit 0). Flag any payload that does not re-derive."""),
 item("CritC1KillRule", "critic", f"""Attack the C1 kill rule against the LANDED tree: attempt each committed round-40 defeat fixture (T2 substring, T4 fenced pseudo-row, T7 symlink out-of-export declaration, T13 mention-only row, T14 H6 case/separator escape, the seven CritKillRule escape states, MutH6H10 leaf-capped green base, MutH1H5 count-relative forgery) against the r41 suite in scratch: each must RED its r41 check (I3/I4/I5/I7/I6/I10/I8 respectively). Where a defeat now passes, you have found a live defect — report it with the exact transcript. Also attempt three NEW escape constructions of your own."""),
 item("MutSuite", "mutation-tester", f"""Mutation-test the landed r41 suite: apply at least 12 byte-level mutants across the I1-I12 limbs (comparison weakened, guard dropped, pattern broadened, path canonicalization removed, case-fold removed, fence check removed, token-boundary regex weakened to substring, per-case isolation removed, negative-control acceptance weakened (the M-H8a class), scan depth limited, work-dir exclusion removed, receipt byte-compare removed). Run the graded selftest for every mutant: every mutant must be killed (its case red). Any survivor is a defect — report the mutant bytes (sha256), the survivor transcript, and the owning check."""),
 item("RevReceipt", "reviewer", f"""Verify the receipt at Y: (1) it is byte-identical to a freshly teed run at the same ref (reproduce it in scratch with tee and diff); (2) run-utc equals the ref's committer instant (git show -s --format=%cI) and time-basis=ref-commit; (3) the receipt carries BOTH the 12 run lines and the 12 graded selftest lines (the D2 class); (4) each payload line's values re-derive from the export. Report any mismatch verbatim. Also verify the receipt was produced by the export's own suite bytes (suite-sha256 in the header equals the suite file's sha256 at the ref)."""),
 item("CritC2Live", "critic", f"""Re-open S063 live: fetch https://www.rfc-editor.org/rfc/rfc9116.txt (record HTTP status/bytes/sha256/time); compare sha256 with the committed capture corpus/source-snapshots/round-41/S063.txt — if the RFC changed, that is a finding. Locate all three Gate quotes in the LIVE bytes (whitespace-normalized); locate them in the capture; both must hit exactly once. Read the entry corpus/knowledge/rfc-9116-security-txt.md: every RFC claim must carry a section anchor that exists in the captured text; flag any anchor that does not. Verify the entry teaches ONE grounded benefit and carries the provenance trio first."""),
 item("MutC2Chain", "mutation-tester", f"""Mutation-test the C2 instrument chain on scratch mirrors of the landed tree: (a) F24 row status flipped to `explored` — harness must FAIL F24; (b) entry's `source: S063` removed — recheck-audit must fail it; (c) capture sha256 corrupted — binding/source-recheck must red; (d) knowledge-expected.txt missing the entry — audit expected mismatch; (e) manifest record used-by pointing at a nonexistent entry — binding unbound. Each mutation must red exactly its instrument. Report transcripts; any mutation that stays green is a defect."""),
 item("RevCorrectionsFinal", "reviewer", f"""Final review of the landed Correction (round 41) blocks in SCORECARD.md/LOG.md/SHONEN.md: each must grade r40 C1 NOT verified on the frozen counter, name the firing evidence paths (RevC1Counters.defeats.txt, CritKillRule.md, MutH6H10.md), name the final r40 receipt truth, and note the D2 transcript gap. Verify the I1 grep spec: `grep -c '^Correction (round 41)'` returns >=1 in each of the three records, and the union of the blocks contains the tokens `not verified`, `RevC1Counters.defeats.txt`, `CritKillRule.md`, `MutH6H10.md`. Verify token-boundary discipline: `closed=7/80` and `failures=10` appear in NO record as correction values. Report verbatim."""),
 item("CritFresh", "critic", f"""Fresh-start audit: re-read the three rejected closures (r38/r39/r40 spotchecks section 5) and verify this round did not repeat their classes: (1) no record quotes an uncommitted run value (every quoted tally must have a committed transcript at Y or be marked report-only); (2) the judged-head rule is satisfiable (no self-hashing); (3) the wave-2 defeat fixtures are committed and red; (4) the do-nothing controls are committed and red. Any repeat of a rejected-closure class is a round defect — name it."""),
]

def build(extra_items, out_path, j, y, wave_dir_note):
    items = FIXED + extra_items
    ctx = CONTEXT.replace("<J>", j).replace("<Y>", y) + "\n" + wave_dir_note
    spec = {
        "wave": "kasegi-r41-falsify",
        "reportDir": ".ufo/waves/round-41/wave2",
        "maxLanes": 64,
        "axes": ["depth:verifiability", "coverage"],
        "milestone": "round-41 falsify wave 2: re-run counters, kill-rule attacks, mutation testing, live re-opens, correction review",
        "context": ctx,
        "items": items,
    }
    with open(out_path, "w") as f:
        json.dump(spec, f, indent=1)
    from collections import Counter
    print("items:", len(items), Counter(i["role"] for i in items))

if __name__ == "__main__":
    extra = json.load(open(sys.argv[1]))
    build(extra, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "")
