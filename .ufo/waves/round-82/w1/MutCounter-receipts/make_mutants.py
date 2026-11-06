#!/usr/bin/env python3
"""Build the round-82 counter mutants from the frozen mutbat.py (base) into m/mutants/."""
import hashlib, json, os, sys

S = os.path.dirname(os.path.abspath(__file__))
M = [
 ("MC01","drop-D2-exec","    for decoy in (d1, d2):","    for decoy in (d1,):"),
 ("MC02","drop-D1-exec","    for decoy in (d1, d2):","    for decoy in (d2,):"),
 ("MC03","return-d1-twice","    return ok, [d1, d2]","    return ok, [d1, d1]"),
 ("MC04","hidden-ge-0","and decoy_ok and hidden >= 1)","and decoy_ok and hidden >= 0)"),
 ("MC05","decoy-term-forced-True",'and tally["neutral_ok"] == n_neutral and decoy_ok and hidden >= 1)','and tally["neutral_ok"] == n_neutral and True and hidden >= 1)'),
 ("MC06","run_decoy-returns-True","    return ok, [d1, d2]","    return True, [d1, d2]"),
 ("MC07","rename-args-guard-inverted","                if arg is not None:\n                    local.add(arg.arg)","                if arg is None:\n                    local.add(arg.arg)"),
 ("MC08","rename-includes-module-names",'    rename = local - module_names - keywords - declared - set(dir(builtins)) - {"__file__"}','    rename = local - keywords - declared - set(dir(builtins)) - {"__file__"}'),
 ("MC09","rename-includes-keywords",'    rename = local - module_names - keywords - declared - set(dir(builtins)) - {"__file__"}','    rename = local - module_names - declared - set(dir(builtins)) - {"__file__"}'),
 ("MC10","rename-skips-except-as",'        elif isinstance(n, ast.ExceptHandler) and n.name in rename:\n            n.name += "_d"','        elif isinstance(n, ast.ExceptHandler) and n.name in rename:\n            n.name += ""'),
 ("MC11","hidden-counts-neutral",'    hidden = sum(1 for r in rows if r["class"] != "neutral"\n','    hidden = sum(1 for r in rows if True\n'),
 ("MC12","hidden-threshold-2","and decoy_ok and hidden >= 1)","and decoy_ok and hidden >= 2)"),
 ("MC13","hidden-from-D1-only","for d in decoy_src)))","for d in decoy_src[:1])))"),
 ("MC14","decoy-accumulator-or","        ok = ok and clean_pass(rc, out, expect_cases)","        ok = ok or clean_pass(rc, out, expect_cases)"),
 ("MC15","D2-not-renamed",'        d2 = ast.unparse(rename_locals(ast.parse(src))) + "\\n"','        d2 = ast.unparse(ast.parse(src)) + "\\n"'),
 ("MC16","parse-failure-as-ok","        return False, None","        return True, None"),
 ("MC17","clean-pass-drops-traceback",'    return rc == 0 and exact and not fail_lines(out) and "Traceback" not in out','    return rc == 0 and exact and not fail_lines(out)'),
 ("MC18","rename-skips-args-clean","                if arg is not None:\n                    local.add(arg.arg)","                if arg is not None:\n                    pass"),
]

def main():
    src = open(os.path.join(S, "m/base.py")).read()
    os.makedirs(os.path.join(S, "m/mutants"), exist_ok=True)
    man = []
    for mid, name, old, new in M:
        n = src.count(old)
        assert n == 1, (mid, name, n)
        out = src.replace(old, new, 1)
        compile(out, mid, "exec")
        open(os.path.join(S, "m/mutants/%s.py" % mid), "w").write(out)
        man.append({"id": mid, "change": name, "old": old, "new": new,
                    "occ": n, "sha256": hashlib.sha256(out.encode()).hexdigest(),
                    "bytes": len(out), "delta_bytes": len(out) - len(src)})
    json.dump(man, open(os.path.join(S, "m/manifest.json"), "w"), indent=1)
    for m in man:
        print("%s %s occ=%d %+d sha=%s" % (m["id"], m["change"], m["occ"], m["delta_bytes"], m["sha256"][:16]))
    return 0

if __name__ == "__main__":
    sys.exit(main())
