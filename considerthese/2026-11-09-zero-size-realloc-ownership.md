# Kasegi: zero size changes ownership reasoning

[N2438](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2438.htm), August 2019, records unresolved C17 ambiguity: a null realloc result need not establish whether storage survived.

[N3096](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3096.pdf), April 2023 working draft, section 7.24.3.7, makes zero size undefined in the nonnull pointer branch. This is draft evidence, not the final published standard.

[glibc documentation](https://sourceware.org/glibc/manual/latest/html_node/Changing-Block-Size.html), checked November 2026, documents freeing a nonnull allocation and returning NULL for zero size; ordinary allocation failure preserves it.

Interpretation: separate zero size handling from allocation failure before assessing stale references or repeated freeing. A language revision does not establish deployed allocator behavior. No execution or vulnerability finding.

WG14 reuse permission unestablished; ISO copyright applies to N3096. GNU manual uses GFDL with invariant sections. Original commentary only; unassimilated.

Reviewed 2026-11-09. Space hold.

Destination: https://github.com/VeigaPunk/kasegi-shokunin, considerthese/2026-11-09-zero-size-realloc-ownership.md.
