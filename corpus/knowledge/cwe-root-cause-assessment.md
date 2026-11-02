source: S098–S106 — MITRE mapping guidance https://cwe.mitre.org/documents/cwe_usage/guidance.html v1.1; specific CWE entry URLs in corpus/SOURCES.md; pinned corpus/source-snapshots/round-61/manifest.json
verified-at: 2026-11-02
recheck: python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-61/source-correction01/manifest.json
# Root-cause mapping is a causal explanation, not a label lookup

ground: F05 (deepening existing ranking/mapping discipline, no new frontier row)

## Decide what the evidence establishes before choosing an ID

S098 distinguishes weakness, exploitation prerequisite and technical impact.
First reconstruct a causal chain from the case: operation and resource, defect,
intermediate behavior, consequence. Keep observations separate from necessities.
A crash or privilege gain is not itself a mechanism. A mentioned administrator
might merely be the observer; it does not prove an access check is absent.
Ask for the operation/trace and missing causal link, not simply a CWE name.

Select the most specific supported weakness, not the most specific imaginable
one. Base/Variant is preferred but the entry's own mapping usage and notes also
control. Class is not categorically forbidden; Category is not a weakness.
A bounded vocabulary limits candidate coverage, so acknowledge a potentially
better child rather than claim universal optimality. Multiple supported causes
or chains need explicit roles, not a forced singleton or bag of guesses.

## Bounded distinctions and falsifiers

| Evidence established | Supported reading | What would falsify the reading |
|---|---|---|
| Arithmetic exceeds representable range and wraps, causing undersized allocation | S099/CWE-190 is a causal precursor; S100/CWE-131 can describe the allocation-size defect | Merely using an integer, or seeing a crash, establishes neither wrap nor erroneous size |
| Allocation omits required storage, with no arithmetic wrap | S100/CWE-131 fits incorrect buffer sizing; do not invent190 | Calculation is correct and the later write independently exceeds its intended buffer |
| A write is proven outside the intended buffer; earlier cause unresolved | S101/CWE-787 may be a supported bounded mapping, with careful review and cause/child search outstanding | Read-only evidence or crash-only evidence does not establish a write |
| User-controlled material enters a page for other users without appropriate neutralization | S104/CWE-79 describes the web-output mechanism | Input is merely present, safely neutralized, or never used as a web page |
| A resource/action lacks authorization checking | S105/CWE-862 distinguishes missing authorization; Class/ALLOWED-WITH-REVIEW, examine children | A check exists but makes an incorrect decision, or only the impact is known |
| Authorization checking occurs but is incorrect | S106/CWE-863 distinguishes incorrect authorization; same careful-review obligation | The evidence only says unauthorized access, without explaining the check |

S099 mapping notes warn about overloaded overflow terminology and forced lower
abstraction. Its relationship notes explicitly connect integer overflow to
undersized allocation. S100 notes that calculation defects can involve chains
or perspective differences. Thus190→131→787 is a possible supported chain, not
a universal expansion of the word overflow. Prefer the demonstrated precursor;
if listing downstream weaknesses, say they are resultant, not independent roots.

S101 mapping notes request closer examination, children and CanFollow causes.
Known precursor evidence should not disappear behind787; conversely, absence of
precursor facts does not erase an actually established out-of-bounds write.

S102/CWE-119 and S103/CWE-20 are currently DISCOURAGED, despite familiar labels.
S102 recommends descendant/cause analysis. S103 distinguishes checking whether
input is already safe from transforming/encoding it for safe interpretation.
Calling every dangerous-input case20 loses that distinction. An insufficient
case does not become sound by retreating to a discouraged broad label.

S104 permits79, but does not authorize guessing storage/reflection/DOM subtype.
S105/S106 are Class entries allowed with review, not prohibited solely because
of abstraction. Distinguish authentication (identity) from authorization
(permission for action/resource); finding an identity check does not prove the
permission check exists or is correct. Specific child suitability remains a
question if the bounded evidence cannot resolve it.

## Replayable assessment, not automatic classification

Use `.ufo/waves/round-61/CONTRACT.md` with independent fictional prose cases.
For each mapping record exact case evidence, mechanism, source, abstraction,
usage and alternatives. For uncertainty ask a concrete question whose answer
would distinguish candidates. Separate known causal components from unknown
upstream causes; do not make ignorance into safety or manufacture completeness.
The independent reviewer grades those links and the predeclared acceptable
sets. JSON/schema/count checks do not grade causal truth.

Negative controls are policies, not measured historical incompetence:
constant79, keyword-to-cause and ranking-to-cause must fail. F05's original
Top25 lesson remains valid; this dossier exercises judgment it did not test.
The source defines a weakness but does not prove any actual vulnerability,
program scope, reproducibility, severity, reward or right to test a target.

## Located source anchors
The short-quote/line table in `corpus/lessons/round-61.md` Gate binds each S098–S106 assertion to its opened source; the corrected manifest makes those locations replayable. The original short-token failure is retained, not silently overwritten.
