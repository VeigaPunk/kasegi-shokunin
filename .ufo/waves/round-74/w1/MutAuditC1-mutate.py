#!/usr/bin/env python3
"""mutate.py SRC OUTDIR — write one mutant per entry of MUTANTS into OUTDIR.

Every mutation is an exact, count-checked substitution scoped to one function span,
so a pattern that no longer matches the source aborts instead of silently no-op'ing.
"""
import os
import re
import sys


def fn_span(text, name):
    m = re.search(r"^def %s\(" % re.escape(name), text, re.M)
    if not m:
        raise SystemExit("no def %s" % name)
    nxt = re.search(r"^(def |if __name__)", text[m.end():], re.M)
    end = m.end() + nxt.start() if nxt else len(text)
    return m.start(), end


def sub_in(text, fname, old, new):
    s, e = fn_span(text, fname)
    body = text[s:e]
    n = body.count(old)
    if n != 1:
        raise SystemExit("pattern count %d in %s: %r" % (n, fname, old))
    return text[:s] + body.replace(old, new) + text[e:]


def replace_fn(text, fname, new_fn):
    s, e = fn_span(text, fname)
    body = text[s:e]
    trail = body[len(body.rstrip()):]
    return text[:s] + new_fn.rstrip() + trail + text[e:]


def sub_once(text, old, new):
    n = text.count(old)
    if n != 1:
        raise SystemExit("global pattern count %d: %r" % (n, old))
    return text.replace(old, new)


FIRST_TO_LAST = '''def first_recheck(path):
    found = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("recheck:"):
                found = line[len("recheck:"):].strip()
    return found
'''

MUTANTS = {
    # --- routed round-73 classes (RC-1/2/3 in the claim) ---
    "M4p-forced-conformant-both": lambda t: sub_in(
        t, "main", 'conform = counts["noprefix"] == 0 and counts["exit2_foreign"] == 0',
        "conform = True"),
    "M4b-result-line-only": lambda t: sub_in(
        t, "main", '% ("conformant" if conform else "nonconformant")', '% "conformant"'),
    "M5p-hardcoded-tmp-parent": lambda t: sub_in(
        t, "run_foreign", "dir=env_tmp", 'dir="/tmp"'),
    "M6p-run-foreign-no-rmtree": lambda t: sub_in(
        t, "run_foreign", "shutil.rmtree(scratch, ignore_errors=True)", "pass"),
    "M7p-last-line-reader": lambda t: replace_fn(t, "first_recheck", FIRST_TO_LAST),
    # --- own choices ---
    "M8p-prefix-comparison-removed": lambda t: sub_in(
        t, "census", "noprefix = not value.startswith(prefix)", "noprefix = False"),
    "M8b-cd-only-prefix-no-lane": lambda t: sub_in(
        t, "census", "noprefix = not value.startswith(prefix)",
        'noprefix = not value.startswith("cd ")'),
    "M9p-foreign-cwd-is-lane": lambda t: sub_in(
        t, "run_foreign", "cwd=scratch", "cwd=DEFAULT_LANE"),
    "M10p-exit1-bucketed-as-exit0": lambda t: sub_in(
        t, "census", "elif code == 0:", "elif code in (0, 1):"),
    "M11p-result-exit-always-0": lambda t: sub_in(
        t, "main", "return 0 if conform else 1", "return 0"),
    "M12p-timeout-counted-as-pass": lambda t: sub_in(
        t, "run_foreign", "return -1", "return 0"),
    # --- behaviour-preserving (equivalent) mutants, for step 5 ---
    "E1-equiv-universal-newlines": lambda t: sub_in(
        t, "run_foreign", "text=True", "universal_newlines=True"),
    "E2-equiv-slice-compare": lambda t: sub_in(
        t, "first_recheck", 'line.startswith("recheck:")', 'line[:8] == "recheck:"'),
    "E3-equiv-timeout-121": lambda t: sub_once(t, "TIMEOUT = 120", "TIMEOUT = 121"),
    "E4-equiv-dir-or-none": lambda t: sub_in(
        t, "run_foreign", "dir=env_tmp", "dir=env_tmp or None"),
    "E5-equiv-verbose-operand-order": lambda t: sub_in(
        t, "census", "if verbose or noprefix or code == 2:",
        "if noprefix or code == 2 or verbose:"),
    "E6-equiv-dir-none": lambda t: sub_in(
        t, "run_foreign", "dir=env_tmp", "dir=None"),
}


def main(argv):
    src, outdir = argv[1], argv[2]
    text = open(src, encoding="utf-8").read()
    os.makedirs(outdir, exist_ok=True)
    for name, fn in MUTANTS.items():
        mut = fn(text)
        if mut == text:
            raise SystemExit("mutant %s is a no-op" % name)
        with open(os.path.join(outdir, name + ".py"), "w", encoding="utf-8") as fh:
            fh.write(mut)
        print("wrote %s" % name)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
