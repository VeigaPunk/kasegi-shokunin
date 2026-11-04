import importlib.util, os, sys
S="/fast/scratch/hyaku/kasegi-r68/ReviewC1"; E=S+"/export"
spec=importlib.util.spec_from_file_location("c",E+"/.ufo/waves/round-68/controls/c1-probe-run-r68.py")
c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
gate=E+"/corpus/instruments/figure-audit.py"
work=S+"/adv/w"; os.makedirs(work,exist_ok=True)
fixture,repo,comp,driver=c.build_fixture(work)
cm=work+"/m.c"; tm=work+"/m.t"
env=dict(os.environ,COMP_MARK=cm,TC_MARK=tm,TMPDIR=work)
cases=[("sort --compress-prog=%s -S 1K big.txt | head -n 1"%comp,fixture),
       ("sort --compress=%s -S 1K big.txt | head -n 1"%comp,fixture),
       ("sort --compress %s -S 1K big.txt | head -n 1"%comp,fixture),
       ("git show --textconv HEAD:big.txt | head -n 1",repo),
       ("git show --textc HEAD:big.txt | head -n 1",repo),
       ("git show HEAD | wc -l",repo),
       ("git show --ext-diff HEAD | wc -l",repo),
       ("git show --ext-d HEAD | wc -l",repo)]
for i,(d,root) in enumerate(cases):
    for p in (cm,tm): open(p,"w").close()
    rc,out,err=c.probe(work,gate,root,"a%d"%i,{"id":"a%d"%i,"record":"big.txt:1","recorded":"x","derive":d,"want":"x"},env)
    r=[l for l in (out+err).splitlines() if "reason=" in l or "FIG " in l]
    print("ADV rc=%d comp_runs=%d tc_runs=%d derive=%r :: %s"%(rc,c.marker_lines(cm),c.marker_lines(tm),d.replace(work,"$W"),(r[-1][:110].replace(work,"$W") if r else "")))
