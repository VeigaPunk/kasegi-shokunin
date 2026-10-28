# R44Review2 — C1 routed defect 2

## Finding

**Not yet falsifiable against a landed correction; no verdict on closure.** Frozen defect 2 is specifically visibility of defect 1's `closed=13/19` correction paragraph to K17 and K18. The baseline finding states K17's escape hatch scans same-round `claims-erratum*.md` and defect 1's superseded value must be named there; K18 accepts a `Correction (round 43)` / claims-erratum supersede record (spot-check §6, lines 101–102). Current visible round-44 tree has no correction/report artifact yet (`.ufo/waves/round-44/` contains only claims, controls, wave metadata; `wave1/` only swarm registry). Thus minimal append-only candidate is a new `.ufo/waves/round-44/claims-erratum-1.md`, with a paragraph explicitly marked `superseded`, naming `closed=13/19` and its provenance, without changing round-43 records or either limb. This is only a proposed minimal fix, not observed landed evidence.

K17's documented rule is direct at `corpus/instruments/r43-limbs/k17-claims-before.sh:28-35`: otherwise-unbacked before token accepted if a same-round claims-erratum paragraph names it and carries `superseded`. K18's documented rule at `corpus/instruments/r43-limbs/k18-transcript.sh:38-43` allows a supersede record containing `Correction (round 43)` or a claims-erratum entry carrying `superseded`. The K18 comments at lines 18-20 exclude SCORECARD/LOG/SHONEN as quote sources, so adding only a correction there would not make its rule grade the original quote; the erratum is the narrowly shared correction surface.

## Do-nothing discrimination

Frozen control `.ufo/waves/round-44/controls/do-nothing.txt:4-7` records eight unresolved routed defects and no r44 correction at freeze. Since the visible r44 tree still lacks an erratum, no append-only correction has yet demonstrated either limb's visibility. Do-nothing therefore remains distinguishable from the proposed change; the proposal alone is not evidence that K17/K18 accept it.

## Evidence / limits

Read-only inspection only; no instrument or tests executed, and no LSP server availability/status was provided, so no semantic references/diagnostics evidence. Evidence: `corpus/lessons/round-43-verifier-spotcheck.md:97-108`; K17 lines 28-35; K18 lines 18-20, 38-43; frozen control lines 4-7. No tools installed. Scratch was not needed/created. Report path is `.ufo/waves/round-44/wave1/R44Review2.md`.
