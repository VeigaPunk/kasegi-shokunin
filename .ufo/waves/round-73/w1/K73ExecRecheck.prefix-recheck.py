#!/usr/bin/env python3
"""prefix-recheck.py — C1 repair candidate builder for round 73 (seat K73ExecRecheck).

For every corpus/knowledge/*.md under --root whose FIRST `recheck:` line value does not
start with `cd <LANE> && `, prepend that prefix to the value. Changes nothing else:
one line per file, byte-exact elsewhere. Check-only by default; --apply writes.

Aborts (exit 2, no writes) unless the noprefix set equals EXPECTED exactly and every
target has exactly one recheck line that is prefix-less.
"""
import glob
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
PREFIX = "cd %s && " % LANE
EXPECTED = [
    "bugzilla-rest-api-bug-endpoints.md",
    "cisa-vulnrichment-adp-enrichment.md",
    "cisa-vulnrichment-record-list.md",
    "github-repository-security-advisories-rest-api.md",
    "nvd-api-2.0-response-schema.md",
    "nvd-api-2.0-retrieval-interface.md",
    "openssf-scorecard-checks.md",
    "osv-affected-range-events.md",
    "project-zero-big-sleep-sqlite-variant-analysis.md",
    "project-zero-fuzzilli-vs-bigsleep-comparison.md",
    "root-loss-2026-10-12.md",
]


def first_recheck_line(lines):
    for i, line in enumerate(lines):
        if line.startswith("recheck:"):
            return i, line
    return None, None


def main(argv):
    root = os.path.abspath(argv[1])
    apply_mode = "--apply" in argv
    kdir = os.path.join(root, "corpus", "knowledge")
    files = sorted(glob.glob(os.path.join(kdir, "*.md")))
    if len(files) != 88:
        print("ABORT: expected 88 knowledge files, found %d" % len(files))
        return 2
    plans = []
    noprefix_names = []
    for path in files:
        name = os.path.basename(path)
        with open(path, encoding="utf-8", newline="") as fh:
            text = fh.read()
        lines = text.splitlines(keepends=True)
        rechecks = [ln for ln in lines if ln.startswith("recheck:")]
        idx, line = first_recheck_line(lines)
        if line is None:
            print("ABORT: %s has no recheck line" % name)
            return 2
        value = line[len("recheck:"):].strip()
        if not value.startswith(PREFIX):
            noprefix_names.append(name)
            if len(rechecks) != 1:
                print("ABORT: %s has %d recheck lines, expected 1" % (name, len(rechecks)))
                return 2
            if not line.startswith("recheck: "):
                print("ABORT: %s recheck line lacks 'recheck: ' (got %r)" % (name, line[:30]))
                return 2
            new_line = line[:len("recheck: ")] + PREFIX + line[len("recheck: "):]
            new_text = "".join(lines[:idx] + [new_line] + lines[idx + 1:])
            if new_text == text:
                print("ABORT: %s substitution is a no-op" % name)
                return 2
            plans.append((path, name, line, new_line, text, new_text))
    missing = sorted(set(EXPECTED) - set(noprefix_names))
    extra = sorted(set(noprefix_names) - set(EXPECTED))
    if missing or extra:
        print("ABORT: noprefix set mismatch; missing=%s extra=%s" % (missing, extra))
        return 2
    print("SET-OK noprefix=%d exactly the expected 11" % len(noprefix_names))
    for path, name, line, new_line, text, new_text in plans:
        print("FILE %s" % name)
        print("  OLD %s" % line.rstrip("\n")[:200])
        print("  NEW %s" % new_line.rstrip("\n")[:200])
        assert len(new_text) == len(text) + len(PREFIX)
        assert new_text.count(line) == 0
        assert new_text.count(new_line) == 1
        if apply_mode:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(new_text)
    if not apply_mode:
        print("DRY-RUN no files written")
        return 0
    # post-apply verification: rescan; noprefix set must now be empty, bytes otherwise intact
    after = []
    for path, name, line, new_line, text, new_text in plans:
        with open(path, "rb") as fh:
            now = fh.read()
        if now != new_text.encode("utf-8"):
            print("ABORT: %s on-disk bytes differ from planned write" % name)
            return 2
        with open(path, encoding="utf-8", newline="") as fh:
            lines = fh.read().splitlines(keepends=True)
        idx, ln = first_recheck_line(lines)
        if not ln[len("recheck:"):].strip().startswith(PREFIX):
            print("ABORT: %s still prefix-less after write" % name)
            return 2
        others = [x for i, x in enumerate(lines) if x.startswith("recheck:") and i != idx]
        for x in others:
            if x not in text:
                print("ABORT: %s other recheck line changed" % name)
                return 2
        after.append(name)
    print("APPLIED %d files; post-apply noprefix scan clean (0 prefix-less)" % len(after))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
