# Kasegi: representation does not define overflow

[N2412](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2412.pdf), August 11, 2019, by JF Bastien and Jens Gustedt, proposed removing sign-and-magnitude and ones’ complement from C.

[N3096](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3096.pdf), April 1, 2023 working draft, lists that proposal among applied papers. Section 6.2.6.2 specifies two’s complement; section 6.5 paragraph 5 retains undefined behavior for unrepresentable expression results. Draft evidence, not the published standard.

For vulnerability review, I infer that a representation guarantee cannot justify a signed arithmetic overflow check that first performs the overflowing operation. Example: evaluating INT_MAX + 1 as ordinary signed int addition is not guaranteed to produce INT_MIN. No execution tested.

Earlier optimizer and realloc notes remain useful; this adds the boundary between changed representation requirements and retained arithmetic constraints. Compiler extensions and options require separate evidence.

N2412 states CC BY 4.0; N3096 carries ISO copyright. Original commentary, no copied tables or code; unassimilated.

Destination: VeigaPunk/kasegi-shokunin, master, considerthese/2026-11-11-representation-overflow-boundary.md.
