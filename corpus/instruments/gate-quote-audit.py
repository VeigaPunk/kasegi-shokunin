#!/usr/bin/env python3
"""Audit every stated word count for a located quote in the lane's lessons.

Usage:  python corpus/instruments/gate-quote-audit.py [--root DIR] [--json PATH]
        python corpus/instruments/gate-quote-audit.py --selftest

Round-52 instrument of record for the depth:verifiability claim. QUALITY.md R56
(mined round 48 as M48-3) already says a Gate's stated word count "comes from
`wc -w` on the quoted text ... A hand-typed count is a claim to re-measure, not
evidence" — but R56 is prose, and prose did not hold: round-48 claimed 16 words
where `wc -w` returned 14, and the same class recurred in round-51 (claimed 24,
measured 17), routed this time by the non-author closure. This instrument makes
the rule mechanical over the lesson tree, fail-closed, so the drift class is
caught by a counter instead of by the next closure.

What it audits: every annotation of the shape ``<N> words by `wc -w`...`` in
``corpus/lessons/round-*.md``. For each annotation it locates the associated
quoted string — the nearest straight ``"..."`` or curly quote ``“...”`` span
within a bounded window around the annotation, so both filed shapes work
(rounds 49-51 put the quote after the annotation; round 48 put it before) —
re-measures it with `wc -w` semantics (whitespace-split word count, the same
measure R56 names), and compares.

Verdicts per annotation:

  OK                  claimed == measured and measured <= 25 (the contract bound)
  OVER-CONTRACT-BOUND measured > 25 (the located quote breaks the <=25-word rule)
  MISMATCH            claimed != measured (the drift class itself)
  ERRATUM-ON-RECORD   a MISMATCH acknowledged by BOTH (a) a ledger row
                      ``<lesson-relpath>|<claimed>|<measured>`` in the errata
                      ledger (default: corpus/instruments/gate-quote-errata.txt,
                      the knowledge-expected.txt precedent) and (b) the erratum
                      text actually present in that lesson file (the word
                      "rratum" and the measured figure both occur in it) — so
                      deleting the appended erratum re-fails the audit.

Fail-closed rules (exit 1) beyond per-annotation failures:

  completeness        fewer than --min-quotes (default 4) annotations found in
                      the whole tree — deleting lessons or annotations shrinks
                      the audited set, and a silent shrink is a fail (the
                      recheck-audit.py expected-list precedent);
  ledger-orphans      a ledger row naming a lesson/figure pair that no longer
                      matches any filed annotation — a stale acknowledgement
                      fails instead of passing silently.

Exit codes: 0 all verified (OK / ERRATUM-ON-RECORD only); 1 any failure;
2 unmeasurable (no lessons directory or no lesson files at all).

The instrument reads only local files; it verifies figure hygiene, not that the
quote supports the claim it grounds (anchor/occurrence truth stays with
source-recheck.py, location truth with the capture itself).
"""
import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

WINDOW = 600           # chars searched each side of an annotation for its quote
CONTRACT_BOUND = 25    # the round-contract <=25-word located-quote rule
STRAIGHT_RE = re.compile(r'"([^"]{1,600}?)"')   # spans may wrap lines (r49/r51 quotes do)
CURLY_RE = re.compile(r"\u201c([^\u201d]+?)\u201d")
ANNOTATION_RE = re.compile(r"(\d+)\s+words by\s+`?wc -w`?")


def measure(text):
    """`wc -w` semantics: max() over whitespace-split fields."""
    return len(text.split())


def find_span(raw, match):
    """Nearest quoted span (straight or curly) around an annotation match."""
    lo = max(0, match.start() - WINDOW)
    hi = min(len(raw), match.end() + WINDOW)
    best = None
    for rx in (STRAIGHT_RE, CURLY_RE):
        for m in rx.finditer(raw, lo, hi):
            if m.group(1).strip() == "":
                continue
            dist = abs((m.start() + m.end()) // 2 - (match.start() + match.end()) // 2)
            if best is None or dist < best[0]:
                best = (dist, m.group(1))
    return best[1] if best else None


def load_ledger(path):
    rows = []
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) == 3:
            rows.append((parts[0], parts[1], parts[2]))
    return rows


def audit_root(root, min_quotes, ledger_path):
    lessons = sorted((Path(root) / "corpus" / "lessons").glob("round-*.md"))
    lessons = [p for p in lessons if "spotcheck" not in p.name]
    if not Path(root, "corpus", "lessons").is_dir() or not lessons:
        return None, [], []
    ledger = load_ledger(ledger_path)
    results, matched_ledger = [], set()
    for path in lessons:
        raw = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        for match in ANNOTATION_RE.finditer(raw):
            claimed = int(match.group(1))
            span = find_span(raw, match)
            line_no = raw.count("\n", 0, match.start()) + 1
            if span is None:
                results.append({"file": rel, "line": line_no, "claimed": claimed,
                                "measured": None, "verdict": "QUOTE-NOT-FOUND",
                                "quote": None})
                continue
            measured = measure(span)
            if claimed == measured and measured <= CONTRACT_BOUND:
                verdict = "OK"
            elif measured > CONTRACT_BOUND:
                verdict = "OVER-CONTRACT-BOUND"
            else:
                verdict = "MISMATCH"
                if (rel, str(claimed), str(measured)) in [(a, b, c) for a, b, c in ledger]:
                    ack = ("rratum" in raw) and (str(measured) in raw)
                    if ack:
                        verdict = "ERRATUM-ON-RECORD"
                        matched_ledger.add((rel, str(claimed), str(measured)))
            results.append({"file": rel, "line": line_no, "claimed": claimed,
                            "measured": measured, "verdict": verdict,
                            "quote": span})
    failures = [r for r in results
                if r["verdict"] not in ("OK", "ERRATUM-ON-RECORD")]
    if len(results) < min_quotes:
        failures.append({"file": "-", "line": 0, "claimed": None, "measured": len(results),
                         "verdict": "COMPLETENESS", "quote":
                         f"annotations found {len(results)} < floor {min_quotes}"})
    for row in ledger:
        if row not in matched_ledger:
            failures.append({"file": row[0], "line": 0, "claimed": row[1], "measured": row[2],
                             "verdict": "LEDGER-ORPHAN", "quote":
                             "ledger row matches no filed annotation (stale erratum)"})
    return results, failures, ledger


def run_audit(root, min_quotes, ledger_path, json_path):
    results, failures, ledger = audit_root(root, min_quotes, ledger_path)
    if results is None:
        print("GATE-QUOTE-AUDIT UNAVAILABLE reason=no-lessons", file=sys.stderr)
        return 2
    for r in results:
        print(f"{r['file']}:{r['line']} claimed={r['claimed']} measured={r['measured']} "
              f"{r['verdict']}" + (f" quote={r['quote'][:60]}..." if r["quote"] else ""))
    ok = len(results) - len([r for r in results if r["verdict"] not in ("OK", "ERRATUM-ON-RECORD")])
    print(f"GATE-QUOTE-AUDIT annotated={len(results)} ok={ok} "
          f"erratum-on-record={len([r for r in results if r['verdict'] == 'ERRATUM-ON-RECORD'])} "
          f"failures={len(failures)}")
    if json_path:
        Path(json_path).write_text(json.dumps(
            {"results": results, "failures": failures, "ledger_rows": len(ledger)},
            indent=1), encoding="utf-8")
    return 1 if failures else 0


def selftest():
    tmp = Path(tempfile.mkdtemp(prefix="gate-quote-audit-selftest-"))
    (tmp / "corpus" / "lessons").mkdir(parents=True)
    good_after = "Grounding quote (17 words by `wc -w`): \"the public repository of CISA's " \
                 "enrichment of public CVE records through CISA's own ADP container of records\"."
    good_before = "L9116 file contract row: \u201cthe /.well-known/ location plus the eight fields " \
                  "with Contact and Expires required\u201d (12 words by `wc -w`)."
    good_wrapped = "Located quote grounding `teaches` (10 words by `wc -w`): \"one two three four\n" \
                   "five six seven eight nine ten\" (S000.txt:2)."
    bad = "Located quote (5 words by `wc -w`): \"one two three four five six\"."
    over = "Located quote (30 words by `wc -w`): " + "\"" + " ".join(["word"] * 30) + "\"."
    erratum_lesson = bad + "\n\n## Erratum 1 (round N) — measured 6 words, not 5.\n"
    cases = []
    for name, body, want_fail in [
        ("case-a-annotation-then-quote", good_after, False),
        ("case-b-quote-then-annotation", good_before, False),
        ("case-g-wrapped-quote", good_wrapped, False),
        ("case-c-wrong-claim", bad, True),
        ("case-d-over-bound", over, True),
        ("case-e-erratum-on-record", erratum_lesson, False),
    ]:
        (tmp / "corpus" / "lessons" / f"round-{name}.md").write_text(body, encoding="utf-8")
        cases.append((name, want_fail))
    ledger = tmp / "corpus" / "instruments" / "gate-quote-errata.txt"
    ledger.parent.mkdir(parents=True)
    ledger.write_text(
        f"corpus/lessons/round-case-e-erratum-on-record.md|5|6\n", encoding="utf-8")
    root = str(tmp)
    failures = 0
    # (f) deletion guard: an empty lessons tree must fail the completeness floor
    empty = Path(tempfile.mkdtemp(prefix="gate-quote-audit-empty-"))
    (empty / "corpus" / "lessons").mkdir(parents=True)
    (empty / "corpus" / "lessons" / "round-x.md").write_text("no annotations here", encoding="utf-8")
    res, fails, _ = audit_root(str(empty), 4, ledger)
    got = 1 if (res is not None and fails) else 0
    want = 1
    print(f"case-f-deletion-guard want={want} got={got}")
    failures += 0 if got == want else 1
    for name, want_fail in cases:
        res, fails, _ = audit_root(root, 4, ledger)
        lesson_fail = any(f["file"].endswith(f"round-{name}.md") for f in fails)
        got = 1 if lesson_fail else 0
        want = 1 if want_fail else 0
        print(f"{name} want={want} got={got}")
        failures += 0 if got == want else 1
    print(f"selftest cases={len(cases) + 1} failures={failures}")
    return 0 if failures == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None, help="lane root (default: two levels up from this script)")
    ap.add_argument("--ledger", default=None, help="errata ledger path (default: alongside this script)")
    ap.add_argument("--min-quotes", type=int, default=4)
    ap.add_argument("--json", dest="json_path", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    root = a.root
    if root is None:
        root = str(Path(__file__).resolve().parents[2])
    ledger = Path(a.ledger) if a.ledger else Path(__file__).resolve().parent / "gate-quote-errata.txt"
    sys.exit(run_audit(root, a.min_quotes, ledger, a.json_path))


if __name__ == "__main__":
    main()
