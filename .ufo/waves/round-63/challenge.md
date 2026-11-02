# KASEGI63 unseen fictional dossiers
Sealed after author freeze6f5d6e4572a3ed7afbe36c1753be7f50b7d4e55d. Reviewer /root/judge_kasegi_round63. These are harmless invented facts, not actual vulnerability claims. Unless a dossier says otherwise, assume an appropriately scoped hypothetical CNA and intended public disclosure; no actual assignment authorized. Respond using frozen contract fields, causal groups and normative qualifications, not merely numbers.

## K63-01
Alder and Birch ship identical vulnerable Cedar library code. A single Cedar authorization defect causes the same established unauthorized-read impact in both products. Each vendor separately upgrades Cedar, publishing two release notes and three patch commits in total. The upgrades introduce no separate security defect. Cedar also serves a third product whose configuration never reaches the defective function; no vulnerability has been established in that third product. How many groups are supported for the described vulnerable products, and do the upgrades or third product add groups?

## K63-02
One omnibus commit to Delta repairs a tenant-authorization omission in its export service and an unrelated out-of-bounds write in its image decoder. Replaying either defect with the other defect eliminated still yields that defect's own established security impact. Each can be fixed without fixing the other. Deployment uses one release artifact and one advisory. Group the two defects and explain what the release packaging changes.

## K63-03
Elm's report labels a length arithmetic error and its downstream out-of-bounds write as two weaknesses. In this dossier they are fully interdependent: the arithmetic condition produces no security impact outside the downstream write, and the write occurs only via that condition. Removing either condition eliminates the described vulnerability. Separately, Elm's management endpoint has an authorization omission that causes established unauthorized access regardless of either parsing condition; it can be fixed independently. Group all three named conditions.

## K63-04
Fir has two observed security-impacting failure paths in one product. Analysts cannot establish whether the paths are independently fixable or two manifestations of one defect. The only current evidence is two failing test names and one workaround that disables the whole service. No shared-code or cross-product question is involved. Give the applicable recommendation, the decisive unresolved fact, and why two test names or the workaround cannot settle it.

## K63-05
Grove and Hazel independently implement the same protocol parsing mistake. Both have established security impact. Source history and comparison conclusively show they do not share the vulnerable code; the dossier treats this as the same independently fixable vulnerability affecting two products, not a compulsory-insecure external specification. Their fixes are released on the same day and use identically worded advisories. State the multi-product allocation guidance and its force.

## K63-06
Iris and Juniper are established vulnerable to the same independently fixable vulnerability. Whether they share the vulnerable code remains unknown; acquisition records and matching stack traces do not answer that question. This is not uncertainty about whether the vulnerability itself is independently fixable, nor a functionality/specification secure-use question. State the applicable recommendation without converting unknown sharing into either known sharing or independent implementation.

## K63-07
Kestrel and Larch use the functionality of external product Maple through independently developed vulnerable implementations. Both implementations are known and have established security impact. A secure way to use Maple's functionality exists and has been demonstrated; both implementations instead use it insecurely. No shared vulnerable implementation is involved. Allocate conditionally under the functionality rule and identify what the secure-use fact does and does not prove.

## K63-08
Nacre and Oak implement another product's functionality in different codebases. The supplied technical determination establishes there is no option to use that functionality securely: every conforming use necessarily exposes the described confidential material. Both products' insecurity is solely this mandatory behavior, with no additional implementation defect alleged. Apply the functionality rule; do different codebases alone settle the count?

## K63-09
Pine and Quartz are two known vulnerable implementations of another product's specification. Security impact is established, but after analysis the hypothetical CNA is uncertain whether there is any secure way to use the specification. This is an explicit unresolved question, not evidence that no secure option exists. There are no other vulnerability groups. Give the appropriate recommendation and contrast the unavailable stronger conclusion.

## K63-10
Rowan's original security-impacting vulnerability already has a hypothetical identifier. A shipped fix is incomplete; the stipulated remaining impact is residual insecurity left by that incomplete fix. No further determination about whether it is a new vulnerability has been made. A manager insists that the second patch must create a second identifier. Separately, a cosmetic log truncation introduced by the patch has no established security impact, and an unrelated established vulnerability in Rowan has no fix yet. Identify the allowable residual-insecurity options and how the latter two facts affect grouping/eligibility. Do not claim an actual assignment.
