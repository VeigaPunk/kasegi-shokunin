import difflib, os, sys, hashlib
S = "/fast/scratch/hyaku/kasegi-r92/MutC1Counter"
src = open(S + "/W/c1/knowledge-meter.py", encoding="utf-8").read()
MUT = [
 ("m01_qualify_key_equality",
  "\n        if m and m.group(1) == key:\n",
  "\n        if m:\n"),
 ("m02_droptok_off",
  "\n            if (DROPTOK % key) in fix:\n",
  "\n            if False and (DROPTOK % key) in fix:\n"),
 ("m03_fixdash_off",
  "\n        if FIXDASH.match(fix):\n",
  "\n        if False and FIXDASH.match(fix):\n"),
 ("m04_lastcell_index",
  '    return cells[-2].strip() if line.rstrip().endswith("|") and len(cells) >= 3 else None\n',
  '    return cells[-3].strip() if line.rstrip().endswith("|") and len(cells) >= 3 else None\n'),
 ("m05_lastcell_guard",
  '    return cells[-2].strip() if line.rstrip().endswith("|") and len(cells) >= 3 else None\n',
  '    return cells[-2].strip() if len(cells) >= 3 else None\n'),
 ("m06_namedcell_as_named",
  '\n            if "drop the" in fix:\n',
  '\n            if False:\n'),
 ("m07_named_as_namedcell",
  '\n            if "drop the" in fix:\n',
  '\n            if True:\n'),
 ("m08_namedcell_prefix_off",
  '                return "named-cell", cell, "MATCHES: " + new\n',
  '                return "named-cell", cell, new\n'),
 ("m09_m9_site_lookup",
  "            lab = labels.get((site, key))\n",
  "            lab = labels.get(site)\n"),
 ("m10_m9_excluded_off",
  "            if lab is None or (site, key) in EXCLUDED or exp is None or exp[1:] != (old, new):\n",
  "            if lab is None or exp is None or exp[1:] != (old, new):\n"),
 ("m11_m9_new_only",
  "            if lab is None or (site, key) in EXCLUDED or exp is None or exp[1:] != (old, new):\n",
  "            if lab is None or (site, key) in EXCLUDED or exp is None or exp[2:] != (new,):\n"),
 ("m12_m10_unlabelled_off",
  "        unlabelled = sorted(mapped - want)\n",
  "        unlabelled = []\n"),
 ("m13_m10_unapplied_off",
  "        unapplied = sorted(want - mapped)\n",
  "        unapplied = []\n"),
 ("m14_m10_unknown_off",
  "        limbs.append((\"M10\", bool(want) and not unapplied and not unlabelled and not unknown and set(EXCLUDED) <= set(kinds),\n",
  "        limbs.append((\"M10\", bool(want) and not unapplied and not unlabelled and set(EXCLUDED) <= set(kinds),\n"),
 ("m15_m10_excluded_subset_off",
  "        limbs.append((\"M10\", bool(want) and not unapplied and not unlabelled and not unknown and set(EXCLUDED) <= set(kinds),\n",
  "        limbs.append((\"M10\", bool(want) and not unapplied and not unlabelled and not unknown and True,\n"),
 ("m16_m10_want_nonempty_off",
  "bool(want) and not unapplied and not unlabelled and not unknown and set(EXCLUDED) <= set(kinds)",
  "not unapplied and not unlabelled and not unknown and set(EXCLUDED) <= set(kinds)"),
 ("m17_m4_bare_off",
  "                if len(BARE.findall(old)) != 1 or BARE.findall(old)[0] != key:\n",
  "                if False:\n"),
 ("m18_m4_valany_any",
  '            if len(vals) != 1 or ("`%s`" % key) not in old:\n',
  '            if len(vals) < 1 or ("`%s`" % key) not in old:\n'),
 ("m19_m4_bybase_member",
  "bybase.get(name) == [path] and A[\"classify\"](vals[0]) == \"INTERNAL\"",
  "name in bybase and A[\"classify\"](vals[0]) == \"INTERNAL\""),
 ("m20_m4_key_in_old_off",
  '            if len(vals) != 1 or ("`%s`" % key) not in old:\n',
  "            if len(vals) != 1:\n"),
 ("m21_m3_oldcount_zero",
  "                        if b.count(old) != 1:\n",
  "                        if b.count(old) < 1:\n"),
 ("m22_m3_dup_off",
  "            if (f, n) in sites:\n                dup += 1\n",
  "            if (f, n) in sites:\n                pass\n"),
 ("m23_m3_samefiles_true",
  "        same_files = set(bfiles) == set(afiles)\n",
  "        same_files = True\n"),
 ("m24_m6_sha_off",
  '            limbs.append(("M6", got == a.map_sha256.lower(), "sha256=%s" % got))\n',
  '            limbs.append(("M6", True, "sha256=%s" % got))\n'),
 ("m25_m0_base_off",
  '        limbs = [("M0", (bn, bm) == (bn0, bm0), "base=%d/%d" % (bn, bm)),\n',
  '        limbs = [("M0", True, "base=%d/%d" % (bn, bm)),\n'),
 ("m26_m1_after_off",
  '                 ("M1", (an, am) == (tn, tm), "after=%d/%d" % (an, am))]\n',
  '                 ("M1", True, "after=%d/%d" % (an, am))]\n'),
 ("m27_m5_hi_off",
  "            if text is None or not (1 <= lo <= hi <= len(text.splitlines())):\n",
  "            if text is None or not (1 <= lo <= len(text.splitlines())):\n"),
 ("m29_m4_internal_off",
  'bybase.get(name) == [path] and A["classify"](vals[0]) == "INTERNAL"',
  'bybase.get(name) == [path]'),
 ("m28_m5_off",
  "            if text is None or not (1 <= lo <= hi <= len(text.splitlines())):\n",
  "            if False:\n"),
]
os.makedirs(S + "/mut", exist_ok=True)
os.makedirs(S + "/mut-diffs", exist_ok=True)
index = []
for name, old, new in MUT:
    n = src.count(old)
    assert n == 1, (name, n)
    text = src.replace(old, new, 1)
    open(S + "/mut/%s.py" % name, "w", encoding="utf-8").write(text)
    d = "".join(difflib.unified_diff(src.splitlines(True), text.splitlines(True),
                                     "knowledge-meter.py", "mut/%s.py" % name, n=2))
    open(S + "/mut-diffs/%s.diff" % name, "w", encoding="utf-8").write(d)
    import py_compile
    py_compile.compile(S + "/mut/%s.py" % name, cfile=S + "/mut/%s.pyc" % name, doraise=True)
    os.unlink(S + "/mut/%s.pyc" % name)
    index.append(name)
open(S + "/mut/index.txt", "w").write("\n".join(index) + "\n")
print("wrote", len(index), "mutants")
