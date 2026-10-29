import re, itertools, os
INSTR="/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments"
def norm(s):
    s=re.sub(r"</?u>|\*\*|``","",s); s=s.replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"')
    return " ".join(s.split())
snap=open("/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-46/S073.txt",encoding="utf-8").read().splitlines()
body=norm(" ".join(snap[555:583]))
CORES={"enabled":r"only report vulnerabilities privately for repositories where this feature is enabled",
 "form":r"summary, details, proof of concept, and impact statement","ai":r"I used AI assistance",
 "credit":r"credited user on the proposed advisory","merge":r"only the repository maintainer can merge"}
print("=== G5c EQUIVALENCE: minimum words for ONE <=25-word span to hold TWO cores")
for (n1,c1),(n2,c2) in itertools.combinations(CORES.items(),2):
    i=body.find(c1); j=body.find(c2)
    if i<0 or j<0: print(n1,n2,"NOT FOUND"); continue
    lo,hi=min(i,j),max(i,j)
    end=hi+len(c2 if j==hi else c1)
    w=len(body[lo:end].split())
    print("  %-8s + %-8s combined_words=%3d  >25? %s" % (n1,n2,w,w>25))
print("  => no pair of the 5 cores fits in one <=25-word span (pristine G5b word limit),")
print("     so len(cores)==5 IMPLIES len(passed)>=5; the 'len(passed) >= 4' conjunct is redundant.")
print()
print("=== G6b EQUIVALENCE: can len(names)==65 AND len(everything)==65 hold while nested != 65?")
print("  names    = entries f with f.endswith('.md') and isfile(f)   (top level only)")
print("  everything = all os.listdir(d) entries                        (top level, incl. dirs)")
print("  nested  = .md files found by os.walk(d)                       (recursive)")
print("  If len(everything)==65 and len(names)==65 then ALL 65 top-level entries are .md regular files,")
print("  so NO subdirectory exists at top level -> os.walk finds exactly those 65 -> nested==65.")
print("  => nested==65 is IMPLIED by the two conjuncts the mutant keeps -> the dropped conjunct is dead.")
